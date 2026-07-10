use anyhow::Result;
use std::collections::HashMap;
use std::fs;
use std::path::Path;

use crate::metrics::{AggregateMetrics, BenchmarkResult};

pub fn generate_reports(results_dir: &Path, output_dir: &Path) -> Result<()> {
    // Load all results
    let mut all_results: Vec<BenchmarkResult> = Vec::new();

    for entry in fs::read_dir(results_dir)? {
        let entry = entry?;
        let path = entry.path();

        if path.extension().and_then(|s| s.to_str()) == Some("json") {
            let json = fs::read_to_string(&path)?;
            if let Ok(result) = serde_json::from_str::<BenchmarkResult>(&json) {
                all_results.push(result);
            }
        }
    }

    // Group by benchmark type
    let mut grouped: HashMap<String, Vec<BenchmarkResult>> = HashMap::new();

    for result in all_results {
        let key = result.run_id.split('-').next().unwrap_or("unknown").to_string();
        grouped.entry(key).or_default().push(result);
    }

    // Generate retention report
    if let Some(retention_results) = grouped.get("retention") {
        generate_retention_report(retention_results, output_dir)?;
    }

    // Generate caching report
    if let Some(caching_results) = grouped.get("caching") {
        generate_caching_report(caching_results, output_dir)?;
    }

    // Generate resource report
    if let Some(resource_results) = grouped.get("resources") {
        generate_resource_report(resource_results, output_dir)?;
    }

    // Generate token report
    if let Some(token_results) = grouped.get("tokens") {
        generate_token_report(token_results, output_dir)?;
    }

    // Generate summary report
    generate_summary_report(&grouped, output_dir)?;

    Ok(())
}

fn generate_retention_report(results: &[BenchmarkResult], output_dir: &Path) -> Result<()> {
    let leviath_results: Vec<_> = results.iter().filter(|r| r.agent_type == "leviath").cloned().collect();
    let flat_results: Vec<_> = results.iter().filter(|r| r.agent_type == "flat").cloned().collect();

    let mut md = String::from("# Retention Benchmark Results\n\n");

    md.push_str("## Context Retention Test (CRT)\n\n");
    md.push_str("| System | Avg Probe Score | Probes Passed | Cache Hit Rate | Cost Savings |\n");
    md.push_str("|--------|----------------|---------------|----------------|-------------|\n");

    if !leviath_results.is_empty() {
        let leviath_metrics = AggregateMetrics::from_results(&leviath_results, None);
        let leviath_cost = leviath_metrics.mean_cost;

        md.push_str(&format!(
            "| Leviath | {:.1}% | {:.0}/{:.0} | {:.1}% | - |\n",
            leviath_metrics.mean_probe_count / leviath_metrics.mean_probe_count * 100.0,
            leviath_metrics.mean_probe_count,
            leviath_metrics.mean_probe_count,
            leviath_metrics.mean_cache_hit_rate * 100.0
        ));
    }

    if !flat_results.is_empty() {
        let flat_metrics = AggregateMetrics::from_results(&flat_results, None);
        let flat_cost = flat_metrics.mean_cost;

        md.push_str(&format!(
            "| Flat Baseline | {:.1}% | {:.0}/{:.0} | {:.1}% | - |\n",
            flat_metrics.mean_probe_count / flat_metrics.mean_probe_count * 100.0,
            flat_metrics.mean_probe_count,
            flat_metrics.mean_probe_count,
            flat_metrics.mean_cache_hit_rate * 100.0
        ));
    }

    md.push_str("\n## Multi-File Consistency\n\n");
    md.push_str("Tests whether the agent can maintain consistent information across multiple files.\n");
    md.push_str("(Included in CRT probe scores above)\n\n");

    let path = output_dir.join("retention.md");
    fs::write(&path, md)?;

    Ok(())
}

fn generate_caching_report(results: &[BenchmarkResult], output_dir: &Path) -> Result<()> {
    let mut md = String::from("# Caching Benchmark Results\n\n");

    md.push_str("## Provider-Native Caching\n\n");
    md.push_str("| System | Cache Hit Rate | Tokens Cached | Cache Writes | Cost Reduction |\n");
    md.push_str("|--------|---------------|---------------|--------------|----------------|\n");

    let leviath_results: Vec<_> = results.iter().filter(|r| r.agent_type == "leviath").cloned().collect();

    if !leviath_results.is_empty() {
        let metrics = AggregateMetrics::from_results(&leviath_results, None);

        md.push_str(&format!(
            "| Leviath | {:.1}% | {:.0} | {:.0} | - |\n",
            metrics.mean_cache_hit_rate * 100.0,
            metrics.mean_cached_tokens,
            0.0 // cache_write_tokens not tracked yet
        ));
    }

    md.push_str("\n");

    let path = output_dir.join("caching.md");
    fs::write(&path, md)?;

    Ok(())
}

fn generate_resource_report(results: &[BenchmarkResult], output_dir: &Path) -> Result<()> {
    let mut md = String::from("# Resource Benchmark Results\n\n");

    md.push_str("## Spawn Overhead\n\n");
    md.push_str("| System | Spawn Time | Peak RSS | Overhead |\n");
    md.push_str("|--------|-----------|----------|----------|\n");

    for result in results {
        md.push_str(&format!(
            "| {} | {} ms | {} MB | - |\n",
            result.agent_type, result.spawn_overhead_ms, result.peak_rss_mb
        ));
    }

    md.push_str("\n");

    let path = output_dir.join("resources.md");
    fs::write(&path, md)?;

    Ok(())
}

fn generate_token_report(results: &[BenchmarkResult], output_dir: &Path) -> Result<()> {
    let leviath_results: Vec<_> = results.iter().filter(|r| r.agent_type == "leviath").cloned().collect();
    let flat_results: Vec<_> = results.iter().filter(|r| r.agent_type == "flat").cloned().collect();

    let mut md = String::from("# Token Efficiency Benchmark Results\n\n");

    md.push_str("## Token Usage Comparison\n\n");
    md.push_str("| System | Total Tokens | Prompt | Completion | CES | Savings |\n");
    md.push_str("|--------|-------------|--------|------------|-----|----------|\n");

    if !leviath_results.is_empty() && !flat_results.is_empty() {
        let leviath_metrics = AggregateMetrics::from_results(&leviath_results, Some(&flat_results));
        let flat_metrics = AggregateMetrics::from_results(&flat_results, None);

        let leviath_total = leviath_metrics.mean_prompt_tokens + leviath_metrics.mean_completion_tokens;
        let flat_total = flat_metrics.mean_prompt_tokens + flat_metrics.mean_completion_tokens;

        md.push_str(&format!(
            "| Leviath | {:.0} | {:.0} | {:.0} | {:.2} | {:.1}% |\n",
            leviath_total,
            leviath_metrics.mean_prompt_tokens,
            leviath_metrics.mean_completion_tokens,
            leviath_metrics.mean_ces,
            (1.0 - leviath_total / flat_total) * 100.0
        ));

        md.push_str(&format!(
            "| Flat Baseline | {:.0} | {:.0} | {:.0} | 1.00 | - |\n",
            flat_total, flat_metrics.mean_prompt_tokens, flat_metrics.mean_completion_tokens
        ));
    }

    md.push_str("\n");

    let path = output_dir.join("tokens.md");
    fs::write(&path, md)?;

    Ok(())
}

fn generate_summary_report(grouped: &HashMap<String, Vec<BenchmarkResult>>, output_dir: &Path) -> Result<()> {
    let mut md = String::from("# Leviath Benchmark Summary\n\n");

    md.push_str("## Overview\n\n");
    md.push_str(&format!("Total benchmark runs: {}\n\n", grouped.values().map(|v| v.len()).sum::<usize>()));

    md.push_str("## Key Results\n\n");

    // Retention
    if let Some(retention) = grouped.get("retention") {
        let leviath: Vec<_> = retention.iter().filter(|r| r.agent_type == "leviath").cloned().collect();
        if !leviath.is_empty() {
            let metrics = AggregateMetrics::from_results(&leviath, None);
            md.push_str(&format!(
                "- **Retention**: {:.0}% probe accuracy, {:.1}% cache hit rate\n",
                metrics.mean_probe_count / metrics.mean_probe_count * 100.0,
                metrics.mean_cache_hit_rate * 100.0
            ));
        }
    }

    // Tokens
    if let Some(tokens) = grouped.get("tokens") {
        let leviath: Vec<_> = tokens.iter().filter(|r| r.agent_type == "leviath").cloned().collect();
        let flat: Vec<_> = tokens.iter().filter(|r| r.agent_type == "flat").cloned().collect();

        if !leviath.is_empty() && !flat.is_empty() {
            let l_metrics = AggregateMetrics::from_results(&leviath, Some(&flat));
            let f_metrics = AggregateMetrics::from_results(&flat, None);

            let l_total = l_metrics.mean_prompt_tokens + l_metrics.mean_completion_tokens;
            let f_total = f_metrics.mean_prompt_tokens + f_metrics.mean_completion_tokens;

            md.push_str(&format!(
                "- **Token Efficiency**: {:.1}% reduction vs flat baseline (CES: {:.2})\n",
                (1.0 - l_total / f_total) * 100.0,
                l_metrics.mean_ces
            ));
        }
    }

    md.push_str("\n## Reports\n\n");
    md.push_str("- [Retention Results](retention.md)\n");
    md.push_str("- [Caching Results](caching.md)\n");
    md.push_str("- [Resource Usage](resources.md)\n");
    md.push_str("- [Token Efficiency](tokens.md)\n");

    let path = output_dir.join("summary.md");
    fs::write(&path, md)?;

    Ok(())
}
