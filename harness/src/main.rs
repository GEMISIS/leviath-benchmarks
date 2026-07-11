mod metrics;
mod mock_provider;
mod reporter;
mod runner;

use anyhow::Result;
use clap::{Parser, Subcommand};
use std::path::PathBuf;
use tracing::info;

#[derive(Parser, Debug)]
#[command(name = "leviath-bench")]
#[command(about = "Benchmark harness for Leviath agent framework")]
struct Args {
    #[command(subcommand)]
    command: Command,
}

#[derive(Subcommand, Debug)]
enum Command {
    /// Run benchmarks
    Run {
        /// Run all benchmark categories
        #[arg(long)]
        all: bool,

        /// Run retention benchmarks
        #[arg(long)]
        retention: bool,

        /// Run caching benchmarks
        #[arg(long)]
        caching: bool,

        /// Run resource benchmarks
        #[arg(long)]
        resources: bool,

        /// Run token efficiency benchmarks
        #[arg(long)]
        tokens: bool,

        /// Number of repetitions
        #[arg(long, default_value = "3")]
        reps: usize,

        /// Models to benchmark (comma-separated)
        #[arg(long, default_value = "claude-sonnet-5")]
        models: String,

        /// Use mock provider for resource benchmarks (free)
        #[arg(long)]
        mock: bool,

        /// Leviath server URL
        #[arg(long, default_value = "http://localhost:3000")]
        leviath_url: String,

        /// Results output directory
        #[arg(long, default_value = "results")]
        results_dir: PathBuf,

        /// Temperature
        #[arg(long, default_value = "0.1")]
        temperature: f32,
    },

    /// Generate report from existing results
    Report {
        /// Results directory
        #[arg(long, default_value = "results")]
        results_dir: PathBuf,

        /// Output directory for reports
        #[arg(long, default_value = "reports")]
        output_dir: PathBuf,
    },

    /// Start mock provider server
    MockProvider {
        /// Port to listen on
        #[arg(long, default_value = "8765")]
        port: u16,

        /// Response delay in milliseconds
        #[arg(long, default_value = "500")]
        delay_ms: u64,
    },
}

#[tokio::main]
async fn main() -> Result<()> {
    tracing_subscriber::fmt()
        .with_env_filter(
            tracing_subscriber::EnvFilter::from_default_env()
                .add_directive(tracing::Level::INFO.into()),
        )
        .init();

    let args = Args::parse();

    match args.command {
        Command::Run {
            all,
            retention,
            caching,
            resources,
            tokens,
            reps,
            models,
            mock,
            leviath_url,
            results_dir,
            temperature,
        } => {
            let model_list: Vec<String> = models.split(',').map(|s| s.trim().to_string()).collect();

            info!("Starting benchmark runs:");
            info!("  Models: {:?}", model_list);
            info!("  Repetitions: {}", reps);
            info!("  Results dir: {}", results_dir.display());

            std::fs::create_dir_all(&results_dir)?;

            let config = runner::BenchmarkConfig {
                models: model_list,
                reps,
                leviath_url,
                results_dir,
                temperature,
                use_mock: mock,
            };

            if all || retention {
                info!("\n=== Running Retention Benchmarks ===");
                runner::run_retention_benchmarks(&config).await?;
            }

            if all || caching {
                info!("\n=== Running Caching Benchmarks ===");
                runner::run_caching_benchmarks(&config).await?;
            }

            if all || resources {
                info!("\n=== Running Resource Benchmarks ===");
                runner::run_resource_benchmarks(&config).await?;
            }

            if all || tokens {
                info!("\n=== Running Token Efficiency Benchmarks ===");
                runner::run_token_benchmarks(&config).await?;
            }

            info!("\nAll benchmarks complete!");
        }

        Command::Report {
            results_dir,
            output_dir,
        } => {
            info!("Generating reports from {}", results_dir.display());
            std::fs::create_dir_all(&output_dir)?;

            reporter::generate_reports(&results_dir, &output_dir)?;

            info!("Reports generated in {}", output_dir.display());
        }

        Command::MockProvider { port, delay_ms } => {
            info!("Starting mock provider on port {}", port);
            mock_provider::start_server(port, delay_ms).await?;
        }
    }

    Ok(())
}
