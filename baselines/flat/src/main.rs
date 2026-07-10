use anyhow::{Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::{Path, PathBuf};
use std::process::Command;
use tracing::{info, warn};

#[derive(Parser, Debug)]
#[command(name = "flat-baseline")]
#[command(about = "Flat-context baseline agent for benchmarking")]
struct Args {
    /// Task description
    #[arg(long)]
    task: String,

    /// Model to use (e.g., claude-sonnet-4-5, gpt-4o)
    #[arg(long)]
    model: String,

    /// Working directory
    #[arg(long)]
    workdir: PathBuf,

    /// Path to probes JSON file
    #[arg(long)]
    probes: Option<PathBuf>,

    /// API provider (anthropic or openai)
    #[arg(long, default_value = "anthropic")]
    provider: String,

    /// API key (or use ANTHROPIC_API_KEY / OPENAI_API_KEY env var)
    #[arg(long)]
    api_key: Option<String>,

    /// Max iterations
    #[arg(long, default_value = "100")]
    max_iterations: usize,

    /// Temperature
    #[arg(long, default_value = "0.1")]
    temperature: f32,

    /// Context window size in tokens
    #[arg(long, default_value = "100000")]
    context_window: usize,

    /// Output JSON file for metrics
    #[arg(long)]
    output: Option<PathBuf>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Message {
    role: String,
    content: Vec<ContentBlock>,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
#[serde(tag = "type", rename_all = "snake_case")]
enum ContentBlock {
    Text { text: String },
    ToolUse { id: String, name: String, input: serde_json::Value },
    ToolResult { tool_use_id: String, content: String, is_error: Option<bool> },
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct TokenUsage {
    prompt_tokens: usize,
    completion_tokens: usize,
    #[serde(default)]
    cached_tokens: usize,
    #[serde(default)]
    cache_write_tokens: usize,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct InferenceMetrics {
    iteration: usize,
    prompt_tokens: usize,
    completion_tokens: usize,
    cached_tokens: usize,
    cache_write_tokens: usize,
    timestamp: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct Probe {
    after_tool_calls: usize,
    #[serde(rename = "type")]
    probe_type: String,
    question: String,
    expected: String,
    rubric: String,
}

#[derive(Debug, Clone, Serialize, Deserialize)]
struct ProbeResponse {
    probe: Probe,
    answer: String,
    tool_call_count: usize,
}

#[derive(Debug, Serialize)]
struct RunMetrics {
    model: String,
    provider: String,
    task: String,
    total_iterations: usize,
    total_prompt_tokens: usize,
    total_completion_tokens: usize,
    total_cached_tokens: usize,
    total_cache_write_tokens: usize,
    cache_hit_rate: f64,
    per_call_metrics: Vec<InferenceMetrics>,
    probe_responses: Vec<ProbeResponse>,
    tool_call_count: usize,
    truncation_events: usize,
}

struct Agent {
    provider: String,
    model: String,
    api_key: String,
    workdir: PathBuf,
    temperature: f32,
    context_window: usize,
    client: reqwest::Client,

    messages: Vec<Message>,
    system_prompt: String,

    tool_call_count: usize,
    probes: Vec<Probe>,
    probe_responses: Vec<ProbeResponse>,

    metrics: Vec<InferenceMetrics>,
    iteration: usize,
    truncation_events: usize,
}

impl Agent {
    fn new(
        provider: String,
        model: String,
        api_key: String,
        workdir: PathBuf,
        task: String,
        temperature: f32,
        context_window: usize,
        probes: Vec<Probe>,
    ) -> Self {
        let system_prompt = format!(
            r#"You are an autonomous coding agent. Your task is:

{}

You have access to these tools:
- read_file: Read file contents
- write_file: Create or overwrite a file
- edit_file: Make exact string replacements in a file
- list_dir: List directory contents
- bash: Execute shell commands (60s timeout)

Working directory: {}

When you complete the task, respond with a final summary message with no tool calls."#,
            task,
            workdir.display()
        );

        Self {
            provider,
            model,
            api_key,
            workdir,
            temperature,
            context_window,
            client: reqwest::Client::new(),
            messages: Vec::new(),
            system_prompt,
            tool_call_count: 0,
            probes,
            probe_responses: Vec::new(),
            metrics: Vec::new(),
            iteration: 0,
            truncation_events: 0,
        }
    }

    async fn run(&mut self, max_iterations: usize) -> Result<()> {
        info!("Starting flat baseline agent - {} iterations max", max_iterations);

        for i in 0..max_iterations {
            self.iteration = i + 1;
            info!("Iteration {}/{}", self.iteration, max_iterations);

            // Check if we should inject a probe
            self.check_and_inject_probe().await?;

            // Make inference call
            let response = self.call_llm().await?;

            // Check if assistant wants to use tools
            let tool_uses: Vec<_> = response
                .iter()
                .filter_map(|block| match block {
                    ContentBlock::ToolUse { id, name, input } => Some((id.clone(), name.clone(), input.clone())),
                    _ => None,
                })
                .collect();

            // Add assistant response to messages
            self.messages.push(Message {
                role: "assistant".to_string(),
                content: response.clone(),
            });

            if tool_uses.is_empty() {
                info!("No tool calls - agent finished");
                break;
            }

            // Execute tools
            let mut tool_results = Vec::new();
            for (id, name, input) in tool_uses {
                info!("Executing tool: {}", name);
                self.tool_call_count += 1;

                let result = self.execute_tool(&name, input).await?;
                tool_results.push(ContentBlock::ToolResult {
                    tool_use_id: id,
                    content: result.content,
                    is_error: Some(result.is_error),
                });
            }

            // Add tool results
            self.messages.push(Message {
                role: "user".to_string(),
                content: tool_results,
            });

            // Truncate if needed
            self.truncate_if_needed();
        }

        info!("Agent finished after {} iterations, {} tool calls", self.iteration, self.tool_call_count);
        Ok(())
    }

    async fn check_and_inject_probe(&mut self) -> Result<()> {
        // Find probes that should fire now
        let probes_to_inject: Vec<_> = self
            .probes
            .iter()
            .filter(|p| p.after_tool_calls == self.tool_call_count)
            .cloned()
            .collect();

        for probe in probes_to_inject {
            info!("Injecting probe at tool call {}: {}", self.tool_call_count, probe.question);

            // Add probe question as user message
            self.messages.push(Message {
                role: "user".to_string(),
                content: vec![ContentBlock::Text {
                    text: format!("[PROBE QUESTION - answer briefly]: {}", probe.question),
                }],
            });

            // Get response
            let response = self.call_llm().await?;

            // Extract text answer
            let answer = response
                .iter()
                .filter_map(|block| match block {
                    ContentBlock::Text { text } => Some(text.clone()),
                    _ => None,
                })
                .collect::<Vec<_>>()
                .join("\n");

            info!("Probe answer: {}", answer);

            self.probe_responses.push(ProbeResponse {
                probe: probe.clone(),
                answer,
                tool_call_count: self.tool_call_count,
            });

            // Add assistant response
            self.messages.push(Message {
                role: "assistant".to_string(),
                content: response,
            });
        }

        Ok(())
    }

    async fn call_llm(&mut self) -> Result<Vec<ContentBlock>> {
        let start = std::time::Instant::now();

        let (response_content, usage) = match self.provider.as_str() {
            "anthropic" => self.call_anthropic().await?,
            "openai" => self.call_openai().await?,
            _ => anyhow::bail!("Unsupported provider: {}", self.provider),
        };

        let elapsed = start.elapsed();
        info!("LLM call took {:?} - tokens: {} prompt, {} completion, {} cached",
              elapsed, usage.prompt_tokens, usage.completion_tokens, usage.cached_tokens);

        self.metrics.push(InferenceMetrics {
            iteration: self.iteration,
            prompt_tokens: usage.prompt_tokens,
            completion_tokens: usage.completion_tokens,
            cached_tokens: usage.cached_tokens,
            cache_write_tokens: usage.cache_write_tokens,
            timestamp: chrono::Utc::now().to_rfc3339(),
        });

        Ok(response_content)
    }

    async fn call_anthropic(&self) -> Result<(Vec<ContentBlock>, TokenUsage)> {
        #[derive(Serialize)]
        struct AnthropicRequest {
            model: String,
            max_tokens: usize,
            temperature: f32,
            system: Vec<SystemBlock>,
            messages: Vec<AnthropicMessage>,
            tools: Vec<serde_json::Value>,
        }

        #[derive(Serialize)]
        struct SystemBlock {
            #[serde(rename = "type")]
            block_type: String,
            text: String,
            #[serde(skip_serializing_if = "Option::is_none")]
            cache_control: Option<CacheControl>,
        }

        #[derive(Serialize)]
        struct CacheControl {
            #[serde(rename = "type")]
            control_type: String,
        }

        #[derive(Serialize)]
        struct AnthropicMessage {
            role: String,
            content: Vec<serde_json::Value>,
        }

        #[derive(Deserialize)]
        struct AnthropicResponse {
            content: Vec<serde_json::Value>,
            usage: AnthropicUsage,
        }

        #[derive(Deserialize)]
        struct AnthropicUsage {
            input_tokens: usize,
            output_tokens: usize,
            #[serde(default)]
            cache_creation_input_tokens: usize,
            #[serde(default)]
            cache_read_input_tokens: usize,
        }

        let tools = self.get_tool_definitions();

        let request = AnthropicRequest {
            model: self.model.clone(),
            max_tokens: 4096,
            temperature: self.temperature,
            system: vec![SystemBlock {
                block_type: "text".to_string(),
                text: self.system_prompt.clone(),
                cache_control: Some(CacheControl {
                    control_type: "ephemeral".to_string(),
                }),
            }],
            messages: self.messages.iter().map(|m| AnthropicMessage {
                role: m.role.clone(),
                content: m.content.iter().map(|c| serde_json::to_value(c).unwrap()).collect(),
            }).collect(),
            tools,
        };

        let response = self
            .client
            .post("https://api.anthropic.com/v1/messages")
            .header("x-api-key", &self.api_key)
            .header("anthropic-version", "2023-06-01")
            .json(&request)
            .send()
            .await?
            .error_for_status()?
            .json::<AnthropicResponse>()
            .await?;

        let content: Vec<ContentBlock> = response
            .content
            .iter()
            .filter_map(|v| serde_json::from_value(v.clone()).ok())
            .collect();

        let usage = TokenUsage {
            prompt_tokens: response.usage.input_tokens,
            completion_tokens: response.usage.output_tokens,
            cached_tokens: response.usage.cache_read_input_tokens,
            cache_write_tokens: response.usage.cache_creation_input_tokens,
        };

        Ok((content, usage))
    }

    async fn call_openai(&self) -> Result<(Vec<ContentBlock>, TokenUsage)> {
        // OpenAI implementation - simplified for now
        anyhow::bail!("OpenAI provider not yet implemented")
    }

    fn get_tool_definitions(&self) -> Vec<serde_json::Value> {
        vec![
            serde_json::json!({
                "name": "read_file",
                "description": "Read the contents of a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file to read (relative to workdir)"
                        }
                    },
                    "required": ["path"]
                }
            }),
            serde_json::json!({
                "name": "write_file",
                "description": "Create or overwrite a file with given content",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file to write"
                        },
                        "content": {
                            "type": "string",
                            "description": "Content to write to the file"
                        }
                    },
                    "required": ["path", "content"]
                }
            }),
            serde_json::json!({
                "name": "edit_file",
                "description": "Make an exact string replacement in a file",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to the file to edit"
                        },
                        "old_str": {
                            "type": "string",
                            "description": "Exact string to find (must be unique in file)"
                        },
                        "new_str": {
                            "type": "string",
                            "description": "Replacement string"
                        }
                    },
                    "required": ["path", "old_str", "new_str"]
                }
            }),
            serde_json::json!({
                "name": "list_dir",
                "description": "List contents of a directory",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "path": {
                            "type": "string",
                            "description": "Path to directory (optional, defaults to workdir root)"
                        }
                    }
                }
            }),
            serde_json::json!({
                "name": "bash",
                "description": "Execute a shell command (60 second timeout)",
                "input_schema": {
                    "type": "object",
                    "properties": {
                        "command": {
                            "type": "string",
                            "description": "Shell command to execute"
                        }
                    },
                    "required": ["command"]
                }
            }),
        ]
    }

    async fn execute_tool(&self, name: &str, input: serde_json::Value) -> Result<ToolResult> {
        match name {
            "read_file" => self.tool_read_file(input),
            "write_file" => self.tool_write_file(input),
            "edit_file" => self.tool_edit_file(input),
            "list_dir" => self.tool_list_dir(input),
            "bash" => self.tool_bash(input),
            _ => Ok(ToolResult {
                content: format!("Unknown tool: {}", name),
                is_error: true,
            }),
        }
    }

    fn tool_read_file(&self, input: serde_json::Value) -> Result<ToolResult> {
        let path: String = serde_json::from_value(input["path"].clone())?;
        let full_path = self.resolve_path(&path)?;

        match fs::read_to_string(&full_path) {
            Ok(content) => Ok(ToolResult {
                content,
                is_error: false,
            }),
            Err(e) => Ok(ToolResult {
                content: format!("Failed to read {}: {}", path, e),
                is_error: true,
            }),
        }
    }

    fn tool_write_file(&self, input: serde_json::Value) -> Result<ToolResult> {
        let path: String = serde_json::from_value(input["path"].clone())?;
        let content: String = serde_json::from_value(input["content"].clone())?;
        let full_path = self.resolve_path(&path)?;

        if let Some(parent) = full_path.parent() {
            fs::create_dir_all(parent)?;
        }

        match fs::write(&full_path, &content) {
            Ok(()) => Ok(ToolResult {
                content: format!("Successfully wrote to {}", path),
                is_error: false,
            }),
            Err(e) => Ok(ToolResult {
                content: format!("Failed to write {}: {}", path, e),
                is_error: true,
            }),
        }
    }

    fn tool_edit_file(&self, input: serde_json::Value) -> Result<ToolResult> {
        let path: String = serde_json::from_value(input["path"].clone())?;
        let old_str: String = serde_json::from_value(input["old_str"].clone())?;
        let new_str: String = serde_json::from_value(input["new_str"].clone())?;
        let full_path = self.resolve_path(&path)?;

        match fs::read_to_string(&full_path) {
            Ok(content) => {
                let matches: Vec<_> = content.match_indices(&old_str).collect();

                if matches.is_empty() {
                    return Ok(ToolResult {
                        content: format!("String not found in {}", path),
                        is_error: true,
                    });
                }

                if matches.len() > 1 {
                    return Ok(ToolResult {
                        content: format!("String appears {} times in {} - must be unique", matches.len(), path),
                        is_error: true,
                    });
                }

                let new_content = content.replace(&old_str, &new_str);

                match fs::write(&full_path, &new_content) {
                    Ok(()) => Ok(ToolResult {
                        content: format!("Successfully edited {}", path),
                        is_error: false,
                    }),
                    Err(e) => Ok(ToolResult {
                        content: format!("Failed to write {}: {}", path, e),
                        is_error: true,
                    }),
                }
            }
            Err(e) => Ok(ToolResult {
                content: format!("Failed to read {}: {}", path, e),
                is_error: true,
            }),
        }
    }

    fn tool_list_dir(&self, input: serde_json::Value) -> Result<ToolResult> {
        let path = if input["path"].is_null() {
            self.workdir.clone()
        } else {
            let path_str: String = serde_json::from_value(input["path"].clone())?;
            self.resolve_path(&path_str)?
        };

        match fs::read_dir(&path) {
            Ok(entries) => {
                let mut items: Vec<String> = entries
                    .filter_map(|e| e.ok())
                    .map(|e| {
                        let name = e.file_name().to_string_lossy().to_string();
                        let is_dir = e.file_type().map(|t| t.is_dir()).unwrap_or(false);
                        if is_dir {
                            format!("{}/", name)
                        } else {
                            name
                        }
                    })
                    .collect();

                items.sort();

                Ok(ToolResult {
                    content: items.join("\n"),
                    is_error: false,
                })
            }
            Err(e) => Ok(ToolResult {
                content: format!("Failed to list directory: {}", e),
                is_error: true,
            }),
        }
    }

    fn tool_bash(&self, input: serde_json::Value) -> Result<ToolResult> {
        let command: String = serde_json::from_value(input["command"].clone())?;

        let output = Command::new("sh")
            .arg("-c")
            .arg(&command)
            .current_dir(&self.workdir)
            .output();

        match output {
            Ok(output) => {
                let stdout = String::from_utf8_lossy(&output.stdout).to_string();
                let stderr = String::from_utf8_lossy(&output.stderr).to_string();

                let combined = if stderr.is_empty() {
                    stdout
                } else {
                    format!("STDOUT:\n{}\n\nSTDERR:\n{}", stdout, stderr)
                };

                Ok(ToolResult {
                    content: combined,
                    is_error: !output.status.success(),
                })
            }
            Err(e) => Ok(ToolResult {
                content: format!("Failed to execute command: {}", e),
                is_error: true,
            }),
        }
    }

    fn resolve_path(&self, path: &str) -> Result<PathBuf> {
        let path = Path::new(path);

        // Prevent path traversal
        if path.components().any(|c| matches!(c, std::path::Component::ParentDir)) {
            anyhow::bail!("Path traversal not allowed: {}", path.display());
        }

        Ok(self.workdir.join(path))
    }

    fn truncate_if_needed(&mut self) {
        // Estimate token count (rough: 1 token ≈ 4 chars)
        let estimated_tokens: usize = self.messages.iter().map(|m| {
            m.content.iter().map(|c| match c {
                ContentBlock::Text { text } => text.len() / 4,
                ContentBlock::ToolUse { input, .. } => input.to_string().len() / 4 + 100,
                ContentBlock::ToolResult { content, .. } => content.len() / 4 + 50,
            }).sum::<usize>()
        }).sum();

        let system_tokens = self.system_prompt.len() / 4;
        let total = estimated_tokens + system_tokens;

        if total > self.context_window {
            info!("Context size {} exceeds window {} - truncating", total, self.context_window);

            // Remove oldest messages (keep at least the last 5 exchanges)
            while self.messages.len() > 10 && total > self.context_window {
                self.messages.remove(0);
                self.truncation_events += 1;
            }

            warn!("Truncated to {} messages", self.messages.len());
        }
    }

    fn generate_metrics(&self) -> RunMetrics {
        let total_prompt = self.metrics.iter().map(|m| m.prompt_tokens).sum();
        let total_completion = self.metrics.iter().map(|m| m.completion_tokens).sum();
        let total_cached = self.metrics.iter().map(|m| m.cached_tokens).sum();
        let total_cache_write = self.metrics.iter().map(|m| m.cache_write_tokens).sum();

        let cache_hit_rate = if total_prompt > 0 {
            total_cached as f64 / total_prompt as f64
        } else {
            0.0
        };

        RunMetrics {
            model: self.model.clone(),
            provider: self.provider.clone(),
            task: "flat-baseline".to_string(),
            total_iterations: self.iteration,
            total_prompt_tokens: total_prompt,
            total_completion_tokens: total_completion,
            total_cached_tokens: total_cached,
            total_cache_write_tokens: total_cache_write,
            cache_hit_rate,
            per_call_metrics: self.metrics.clone(),
            probe_responses: self.probe_responses.clone(),
            tool_call_count: self.tool_call_count,
            truncation_events: self.truncation_events,
        }
    }
}

struct ToolResult {
    content: String,
    is_error: bool,
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

    // Resolve API key
    let api_key = args.api_key.or_else(|| {
        match args.provider.as_str() {
            "anthropic" => std::env::var("ANTHROPIC_API_KEY").ok(),
            "openai" => std::env::var("OPENAI_API_KEY").ok(),
            _ => None,
        }
    }).context("API key not provided and not found in environment")?;

    // Load probes if provided
    let probes = if let Some(probe_path) = args.probes {
        let probe_json = fs::read_to_string(&probe_path)
            .context("Failed to read probes file")?;
        let probe_data: serde_json::Value = serde_json::from_str(&probe_json)?;
        serde_json::from_value(probe_data["probes"].clone())?
    } else {
        Vec::new()
    };

    info!("Starting flat baseline: model={}, workdir={}", args.model, args.workdir.display());
    info!("Loaded {} probes", probes.len());

    let mut agent = Agent::new(
        args.provider,
        args.model,
        api_key,
        args.workdir,
        args.task,
        args.temperature,
        args.context_window,
        probes,
    );

    agent.run(args.max_iterations).await?;

    let metrics = agent.generate_metrics();

    info!("Flat baseline completed:");
    info!("  Total iterations: {}", metrics.total_iterations);
    info!("  Total tool calls: {}", metrics.tool_call_count);
    info!("  Prompt tokens: {}", metrics.total_prompt_tokens);
    info!("  Completion tokens: {}", metrics.total_completion_tokens);
    info!("  Cached tokens: {}", metrics.total_cached_tokens);
    info!("  Cache hit rate: {:.2}%", metrics.cache_hit_rate * 100.0);
    info!("  Truncation events: {}", metrics.truncation_events);
    info!("  Probe responses: {}", metrics.probe_responses.len());

    if let Some(output_path) = args.output {
        let json = serde_json::to_string_pretty(&metrics)?;
        fs::write(&output_path, &json)?;
        info!("Metrics written to {}", output_path.display());
    }

    Ok(())
}
