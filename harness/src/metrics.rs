use serde::{Deserialize, Serialize};

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct InferenceMetrics {
    pub iteration: usize,
    pub prompt_tokens: usize,
    pub completion_tokens: usize,
    pub cached_tokens: usize,
    pub cache_write_tokens: usize,
    pub timestamp: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct ProbeResponse {
    pub probe: Probe,
    pub answer: String,
    pub tool_call_count: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct Probe {
    pub after_tool_calls: usize,
    #[serde(rename = "type")]
    pub probe_type: String,
    pub question: String,
    pub expected: String,
    pub rubric: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
pub struct BenchmarkResult {
    pub run_id: String,
    pub agent_type: String, // "leviath" or "flat"
    pub model: String,
    pub task: String,

    pub total_iterations: usize,
    pub total_prompt_tokens: usize,
    pub total_completion_tokens: usize,
    pub total_cached_tokens: usize,
    pub total_cache_write_tokens: usize,
    pub cache_hit_rate: f64,

    pub per_call_metrics: Vec<InferenceMetrics>,

    pub probe_count: usize,
    pub probe_responses: Vec<ProbeResponse>,

    pub tool_call_count: usize,
    pub peak_rss_mb: usize,
    pub spawn_overhead_ms: usize,

    pub timestamp: String,
}

impl BenchmarkResult {
    /// Calculate Context Efficiency Score (CES)
    /// Formula: (1 - cache_hit_rate) * token_efficiency
    pub fn context_efficiency_score(&self, baseline: &BenchmarkResult) -> f64 {
        let total_tokens = self.total_prompt_tokens + self.total_completion_tokens;
        let baseline_total = baseline.total_prompt_tokens + baseline.total_completion_tokens;

        if baseline_total == 0 {
            return 0.0;
        }

        let token_efficiency = baseline_total as f64 / total_tokens as f64;
        let cache_benefit = 1.0 + self.cache_hit_rate;

        token_efficiency * cache_benefit
    }

    /// Calculate cost in USD (Anthropic pricing as of 2026)
    pub fn calculate_cost(&self) -> f64 {
        let (input_price, output_price, cache_write_price, cache_read_price) = match self.model.as_str() {
            "claude-sonnet-5" => (3.0, 15.0, 3.75, 0.30),
            "claude-sonnet-4-5" | "claude-sonnet-4-6" => (3.0, 15.0, 3.75, 0.30),
            "claude-opus-4-8" => (15.0, 75.0, 18.75, 1.50),
            _ => (3.0, 15.0, 3.75, 0.30), // Default to Sonnet pricing
        };

        let input_cost = (self.total_prompt_tokens - self.total_cached_tokens) as f64 * input_price / 1_000_000.0;
        let output_cost = self.total_completion_tokens as f64 * output_price / 1_000_000.0;
        let cache_write_cost = self.total_cache_write_tokens as f64 * cache_write_price / 1_000_000.0;
        let cache_read_cost = self.total_cached_tokens as f64 * cache_read_price / 1_000_000.0;

        input_cost + output_cost + cache_write_cost + cache_read_cost
    }
}

#[derive(Debug, Clone)]
pub struct AggregateMetrics {
    pub mean_prompt_tokens: f64,
    pub mean_completion_tokens: f64,
    pub mean_cached_tokens: f64,
    pub mean_cache_hit_rate: f64,
    pub mean_probe_count: f64,
    pub mean_cost: f64,
    pub mean_ces: f64,

    pub std_prompt_tokens: f64,
    pub std_completion_tokens: f64,
    pub std_cache_hit_rate: f64,
    pub std_probe_count: f64,
    pub std_cost: f64,
    pub std_ces: f64,
}

impl AggregateMetrics {
    pub fn from_results(results: &[BenchmarkResult], baselines: Option<&[BenchmarkResult]>) -> Self {
        let n = results.len() as f64;

        let prompt_tokens: Vec<f64> = results.iter().map(|r| r.total_prompt_tokens as f64).collect();
        let completion_tokens: Vec<f64> = results.iter().map(|r| r.total_completion_tokens as f64).collect();
        let cached_tokens: Vec<f64> = results.iter().map(|r| r.total_cached_tokens as f64).collect();
        let cache_hit_rates: Vec<f64> = results.iter().map(|r| r.cache_hit_rate).collect();
        let probe_counts: Vec<f64> = results.iter().map(|r| r.probe_count as f64).collect();
        let costs: Vec<f64> = results.iter().map(|r| r.calculate_cost()).collect();

        let ces_scores: Vec<f64> = if let Some(baselines) = baselines {
            results
                .iter()
                .zip(baselines.iter())
                .map(|(r, b)| r.context_efficiency_score(b))
                .collect()
        } else {
            vec![0.0; results.len()]
        };

        Self {
            mean_prompt_tokens: mean(&prompt_tokens),
            mean_completion_tokens: mean(&completion_tokens),
            mean_cached_tokens: mean(&cached_tokens),
            mean_cache_hit_rate: mean(&cache_hit_rates),
            mean_probe_count: mean(&probe_counts),
            mean_cost: mean(&costs),
            mean_ces: mean(&ces_scores),

            std_prompt_tokens: std_dev(&prompt_tokens),
            std_completion_tokens: std_dev(&completion_tokens),
            std_cache_hit_rate: std_dev(&cache_hit_rates),
            std_probe_count: std_dev(&probe_counts),
            std_cost: std_dev(&costs),
            std_ces: std_dev(&ces_scores),
        }
    }
}

fn mean(values: &[f64]) -> f64 {
    if values.is_empty() {
        return 0.0;
    }
    values.iter().sum::<f64>() / values.len() as f64
}

fn std_dev(values: &[f64]) -> f64 {
    if values.is_empty() {
        return 0.0;
    }

    let mean = mean(values);
    let variance = values.iter().map(|v| (v - mean).powi(2)).sum::<f64>() / values.len() as f64;
    variance.sqrt()
}
