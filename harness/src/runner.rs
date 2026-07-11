use anyhow::{Context, Result};
use futures_util::{SinkExt, StreamExt};
use serde::{Deserialize, Serialize};
use std::path::{Path, PathBuf};
use std::process::Command;
use tokio::time::{sleep, Duration};
use tokio_tungstenite::connect_async;
use tokio_tungstenite::tungstenite::Message as WsMessage;
use tracing::{info, warn};

use crate::metrics::{BenchmarkResult, InferenceMetrics, Probe, ProbeResponse};

pub struct BenchmarkConfig {
    pub models: Vec<String>,
    pub reps: usize,
    pub leviath_url: String,
    pub results_dir: PathBuf,
    pub temperature: f32,
    pub use_mock: bool,
}

#[derive(Debug, Serialize)]
struct SpawnRequest {
    blueprint: String,
    task: String,
    model: Option<String>,
    yolo: bool,
    workdir: String,
    metadata: serde_json::Value,
}

#[derive(Debug, Deserialize)]
struct SpawnResponse {
    agent_id: String,
    run_id: String,
}

#[derive(Debug, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
enum ServerEvent {
    AgentSpawned {
        agent_id: String,
        run_id: String,
        blueprint: String,
    },
    AgentStatus {
        run_id: String,
        status: String,
        stage: Option<String>,
        iteration: usize,
        #[serde(default)]
        tool_calls: usize,
    },
    Tokens {
        run_id: String,
        prompt_tokens: usize,
        completion_tokens: usize,
        #[serde(default)]
        cached_tokens: usize,
        #[serde(default)]
        cache_write_tokens: usize,
    },
    ContextUpdate {
        run_id: String,
        total_tokens: usize,
        max_tokens: usize,
    },
    AgentCompleted {
        run_id: String,
        status: String,
        result: Option<String>,
    },
    Log {
        run_id: String,
        line: String,
    },
    #[serde(other)]
    Unknown,
}

#[derive(Debug, Deserialize)]
struct RunMeta {
    run_id: String,
    status: String,
    prompt_tokens: usize,
    completion_tokens: usize,
    #[serde(default)]
    cached_tokens: usize,
}

#[derive(Debug, Serialize)]
struct MessageRequest {
    message: String,
}

pub async fn run_retention_benchmarks(config: &BenchmarkConfig) -> Result<()> {
    info!("Running retention benchmarks with {} models, {} reps each", config.models.len(), config.reps);

    let tasks = load_task_list("tasks")?;

    for model in &config.models {
        for task in &tasks {
            for rep in 0..config.reps {
                info!("\n--- Retention: {}, task: {}, rep: {} ---", model, task.name, rep + 1);

                // Run Leviath version
                let leviath_result = run_leviath_task(
                    config,
                    model,
                    &task.path,
                    &format!("retention-leviath-{}-{}-{}", model, task.name, rep),
                )
                .await?;

                save_result(&config.results_dir, &leviath_result)?;

                // Run flat baseline version
                let flat_result = run_flat_baseline_task(
                    config,
                    model,
                    &task.path,
                    &format!("retention-flat-{}-{}-{}", model, task.name, rep),
                )
                .await?;

                save_result(&config.results_dir, &flat_result)?;

                info!("Retention test complete - Leviath: {} probes, Flat: {} probes",
                      leviath_result.probe_count, flat_result.probe_count);
            }
        }
    }

    Ok(())
}

pub async fn run_caching_benchmarks(config: &BenchmarkConfig) -> Result<()> {
    info!("Running caching benchmarks");

    let tasks = load_task_list("tasks")?;

    for model in &config.models {
        for task in &tasks {
            for rep in 0..config.reps {
                info!("\n--- Caching: {}, task: {}, rep: {} ---", model, task.name, rep + 1);

                let result = run_leviath_task(
                    config,
                    model,
                    &task.path,
                    &format!("caching-leviath-{}-{}-{}", model, task.name, rep),
                )
                .await?;

                save_result(&config.results_dir, &result)?;

                info!("Cache hit rate: {:.1}%", result.cache_hit_rate * 100.0);
            }
        }
    }

    Ok(())
}

pub async fn run_resource_benchmarks(config: &BenchmarkConfig) -> Result<()> {
    info!("Running resource benchmarks (mock: {})", config.use_mock);

    // Use smaller tasks for resource benchmarks to reduce API costs
    let tasks = load_task_list("tasks")?
        .into_iter()
        .take(2)
        .collect::<Vec<_>>();

    for model in &config.models {
        for task in &tasks {
            // Only 1 rep for resource benchmarks
            info!("\n--- Resources: {}, task: {} ---", model, task.name);

            let result = run_leviath_task(
                config,
                model,
                &task.path,
                &format!("resources-leviath-{}-{}", model, task.name),
            )
            .await?;

            save_result(&config.results_dir, &result)?;

            info!("Peak RSS: {} MB, Spawn overhead: {} ms",
                  result.peak_rss_mb, result.spawn_overhead_ms);
        }
    }

    Ok(())
}

pub async fn run_token_benchmarks(config: &BenchmarkConfig) -> Result<()> {
    info!("Running token efficiency benchmarks");

    let tasks = load_task_list("tasks")?;

    for model in &config.models {
        for task in &tasks {
            for rep in 0..config.reps {
                info!("\n--- Tokens: {}, task: {}, rep: {} ---", model, task.name, rep + 1);

                let leviath_result = run_leviath_task(
                    config,
                    model,
                    &task.path,
                    &format!("tokens-leviath-{}-{}-{}", model, task.name, rep),
                )
                .await?;

                let flat_result = run_flat_baseline_task(
                    config,
                    model,
                    &task.path,
                    &format!("tokens-flat-{}-{}-{}", model, task.name, rep),
                )
                .await?;

                save_result(&config.results_dir, &leviath_result)?;
                save_result(&config.results_dir, &flat_result)?;

                let leviath_total = leviath_result.total_prompt_tokens + leviath_result.total_completion_tokens;
                let flat_total = flat_result.total_prompt_tokens + flat_result.total_completion_tokens;

                info!("Token usage - Leviath: {}, Flat: {}, Savings: {:.1}%",
                      leviath_total, flat_total,
                      (1.0 - leviath_total as f64 / flat_total as f64) * 100.0);
            }
        }
    }

    Ok(())
}

async fn run_leviath_task(
    config: &BenchmarkConfig,
    model: &str,
    task_path: &Path,
    run_id: &str,
) -> Result<BenchmarkResult> {
    let task_md = std::fs::read_to_string(task_path.join("task.md"))?;
    let probes_path = task_path.join("probes.json");
    let probes: Vec<Probe> = if probes_path.exists() {
        let probes_json = std::fs::read_to_string(&probes_path)?;
        let probes_data: serde_json::Value = serde_json::from_str(&probes_json)?;
        serde_json::from_value(probes_data["probes"].clone())?
    } else {
        Vec::new()
    };

    let workdir = task_path.join("seed-files");

    let client = reqwest::Client::new();

    // Spawn agent
    let spawn_start = std::time::Instant::now();

    let spawn_req = SpawnRequest {
        blueprint: "simple-coder".to_string(), // Simplified blueprint for benchmarking
        task: task_md.clone(),
        model: Some(model.to_string()),
        yolo: true,
        workdir: workdir.to_string_lossy().to_string(),
        metadata: serde_json::json!({
            "benchmark_id": run_id,
            "benchmark_type": "leviath"
        }),
    };

    let spawn_response: SpawnResponse = client
        .post(format!("{}/api/agents", config.leviath_url))
        .json(&spawn_req)
        .send()
        .await?
        .error_for_status()?
        .json()
        .await?;

    let spawn_overhead_ms = spawn_start.elapsed().as_millis() as usize;

    info!("Agent spawned: {} ({})", spawn_response.agent_id, spawn_response.run_id);

    // Connect to WebSocket
    let ws_url = config.leviath_url.replace("http", "ws");
    let (ws_stream, _) = connect_async(format!("{}/ws/agents/{}", ws_url, spawn_response.run_id))
        .await
        .context("Failed to connect to WebSocket")?;

    let (mut _ws_write, mut ws_read) = ws_stream.split();

    // Track metrics
    let mut inference_metrics = Vec::new();
    let mut tool_call_count = 0;
    let mut probe_responses = Vec::new();
    let mut completed = false;
    let mut pending_probe: Option<(Probe, usize)> = None;
    let mut probe_log_buffer = Vec::new();

    // Monitor WebSocket events
    while let Some(msg_result) = ws_read.next().await {
        let msg = msg_result?;

        if let WsMessage::Text(text) = msg {
            let event: ServerEvent = serde_json::from_str(&text)?;

            match event {
                ServerEvent::Tokens {
                    prompt_tokens,
                    completion_tokens,
                    cached_tokens,
                    cache_write_tokens,
                    ..
                } => {
                    inference_metrics.push(InferenceMetrics {
                        iteration: inference_metrics.len() + 1,
                        prompt_tokens,
                        completion_tokens,
                        cached_tokens,
                        cache_write_tokens,
                        timestamp: chrono::Utc::now().to_rfc3339(),
                    });

                    // If we have a pending probe, finalize it with collected logs
                    if let Some((probe, probe_tool_count)) = pending_probe.take() {
                        let answer = probe_log_buffer.join("\n");
                        probe_log_buffer.clear();

                        info!("Probe answer collected: {}", answer);

                        probe_responses.push(ProbeResponse {
                            probe,
                            answer,
                            tool_call_count: probe_tool_count,
                        });
                    }
                }

                ServerEvent::Log { ref line, .. } => {
                    // If we're waiting for a probe response, collect log lines
                    if pending_probe.is_some() {
                        // Skip log lines that are just metadata/status
                        if !line.starts_with('[') && !line.is_empty() {
                            probe_log_buffer.push(line.clone());
                        }
                    }

                    if line.contains("Calling tool:") {
                        tool_call_count += 1;

                        // Check if we should inject a probe
                        for probe in &probes {
                            if probe.after_tool_calls == tool_call_count {
                                info!("Injecting probe at tool call {}: {}", tool_call_count, probe.question);

                                // Inject probe via API
                                let msg_req = MessageRequest {
                                    message: format!("[PROBE QUESTION - answer briefly]: {}", probe.question),
                                };

                                client
                                    .post(format!("{}/api/agents/{}/message", config.leviath_url, spawn_response.run_id))
                                    .json(&msg_req)
                                    .send()
                                    .await?;

                                // Mark that we're waiting for a probe response
                                pending_probe = Some((probe.clone(), tool_call_count));
                                probe_log_buffer.clear();
                            }
                        }
                    }
                }

                ServerEvent::AgentCompleted { status, .. } => {
                    info!("Agent completed with status: {}", status);
                    completed = true;
                    break;
                }

                _ => {}
            }
        }
    }

    // Get final meta
    let meta: RunMeta = client
        .get(format!("{}/api/agents/{}", config.leviath_url, spawn_response.run_id))
        .send()
        .await?
        .error_for_status()?
        .json()
        .await?;

    // Measure RSS (approximate - would need better process tracking)
    let peak_rss_mb = 0; // Placeholder

    let total_cached = meta.cached_tokens;
    let cache_hit_rate = if meta.prompt_tokens > 0 {
        total_cached as f64 / meta.prompt_tokens as f64
    } else {
        0.0
    };

    Ok(BenchmarkResult {
        run_id: run_id.to_string(),
        agent_type: "leviath".to_string(),
        model: model.to_string(),
        task: task_path.file_name().unwrap().to_string_lossy().to_string(),
        total_iterations: inference_metrics.len(),
        total_prompt_tokens: meta.prompt_tokens,
        total_completion_tokens: meta.completion_tokens,
        total_cached_tokens: total_cached,
        total_cache_write_tokens: 0, // Not available from RunMeta
        cache_hit_rate,
        per_call_metrics: inference_metrics,
        probe_count: probe_responses.len(),
        probe_responses,
        tool_call_count,
        peak_rss_mb,
        spawn_overhead_ms,
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

async fn run_flat_baseline_task(
    config: &BenchmarkConfig,
    model: &str,
    task_path: &Path,
    run_id: &str,
) -> Result<BenchmarkResult> {
    let task_md = std::fs::read_to_string(task_path.join("task.md"))?;
    let probes_path = task_path.join("probes.json");
    let workdir = task_path.join("seed-files");

    let output_path = config.results_dir.join(format!("{}.json", run_id));

    // Build path to flat-baseline binary
    let flat_binary = std::env::current_exe()?
        .parent()
        .unwrap()
        .parent()
        .unwrap()
        .join("flat-baseline");

    let mut cmd = Command::new(flat_binary);
    cmd.arg("--task")
        .arg(&task_md)
        .arg("--model")
        .arg(model)
        .arg("--workdir")
        .arg(&workdir)
        .arg("--output")
        .arg(&output_path)
        .arg("--temperature")
        .arg(config.temperature.to_string());

    if probes_path.exists() {
        cmd.arg("--probes").arg(&probes_path);
    }

    info!("Running flat baseline: {:?}", cmd);

    let output = cmd.output()?;

    if !output.status.success() {
        let stderr = String::from_utf8_lossy(&output.stderr);
        anyhow::bail!("Flat baseline failed: {}", stderr);
    }

    // Load the result it wrote
    let result_json = std::fs::read_to_string(&output_path)?;
    let flat_result: serde_json::Value = serde_json::from_str(&result_json)?;

    // Convert to BenchmarkResult
    Ok(BenchmarkResult {
        run_id: run_id.to_string(),
        agent_type: "flat".to_string(),
        model: model.to_string(),
        task: task_path.file_name().unwrap().to_string_lossy().to_string(),
        total_iterations: flat_result["total_iterations"].as_u64().unwrap_or(0) as usize,
        total_prompt_tokens: flat_result["total_prompt_tokens"].as_u64().unwrap_or(0) as usize,
        total_completion_tokens: flat_result["total_completion_tokens"].as_u64().unwrap_or(0) as usize,
        total_cached_tokens: flat_result["total_cached_tokens"].as_u64().unwrap_or(0) as usize,
        total_cache_write_tokens: flat_result["total_cache_write_tokens"].as_u64().unwrap_or(0) as usize,
        cache_hit_rate: flat_result["cache_hit_rate"].as_f64().unwrap_or(0.0),
        per_call_metrics: Vec::new(), // Not converted for brevity
        probe_count: flat_result["probe_responses"].as_array().map(|a| a.len()).unwrap_or(0),
        probe_responses: Vec::new(), // Would need to convert
        tool_call_count: flat_result["tool_call_count"].as_u64().unwrap_or(0) as usize,
        peak_rss_mb: 0,
        spawn_overhead_ms: 0,
        timestamp: chrono::Utc::now().to_rfc3339(),
    })
}

fn save_result(results_dir: &Path, result: &BenchmarkResult) -> Result<()> {
    let path = results_dir.join(format!("{}.json", result.run_id));
    let json = serde_json::to_string_pretty(result)?;
    std::fs::write(&path, json)?;
    info!("Saved result to {}", path.display());
    Ok(())
}

#[derive(Debug, Deserialize)]
struct TaskInfo {
    name: String,
    path: PathBuf,
}

fn load_task_list(tasks_dir: &str) -> Result<Vec<TaskInfo>> {
    let mut tasks = Vec::new();

    for entry in std::fs::read_dir(tasks_dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.is_dir() {
            let name = path.file_name().unwrap().to_string_lossy().to_string();
            tasks.push(TaskInfo { name, path });
        }
    }

    tasks.sort_by(|a, b| a.name.cmp(&b.name));

    Ok(tasks)
}
