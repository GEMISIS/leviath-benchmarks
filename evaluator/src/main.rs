use anyhow::{Context, Result};
use clap::Parser;
use serde::{Deserialize, Serialize};
use std::fs;
use std::path::PathBuf;
use tracing::info;

#[derive(Parser, Debug)]
#[command(name = "evaluator")]
#[command(about = "Grade probe responses using LLM")]
struct Args {
    /// Command to execute
    #[command(subcommand)]
    command: Command,
}

#[derive(Parser, Debug)]
enum Command {
    /// Grade probe responses
    Grade {
        /// Path to results JSON file containing probe responses
        #[arg(long)]
        results: PathBuf,

        /// LLM provider to use for grading (different from tested provider)
        #[arg(long)]
        provider: String,

        /// Model to use for grading
        #[arg(long)]
        model: String,

        /// API key (or use env var)
        #[arg(long)]
        api_key: Option<String>,

        /// Output path for graded results
        #[arg(long)]
        output: Option<PathBuf>,
    },
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

#[derive(Debug, Clone, Serialize, Deserialize)]
struct GradedResponse {
    probe: Probe,
    answer: String,
    tool_call_count: usize,
    score: f64,
    grade: String,
    reasoning: String,
}

#[derive(Debug, Deserialize)]
struct ResultsFile {
    probe_responses: Vec<ProbeResponse>,
}

struct Grader {
    provider: String,
    model: String,
    api_key: String,
    client: reqwest::Client,
}

impl Grader {
    fn new(provider: String, model: String, api_key: String) -> Self {
        Self {
            provider,
            model,
            api_key,
            client: reqwest::Client::new(),
        }
    }

    async fn grade_response(&self, response: &ProbeResponse) -> Result<GradedResponse> {
        let prompt = format!(
            r#"You are grading an agent's response to a probe question during a benchmark test.

**Probe Question:** {}

**Expected Answer:** {}

**Grading Rubric:** {}

**Agent's Answer:** {}

Grade the agent's answer on this 4-point scale:
- **Correct (1.0)**: Accurate and references the right information
- **Partially Correct (0.5)**: Right direction but missing details
- **Wrong (0.0)**: Confident but incorrect
- **Hallucinated (-0.5)**: Invented information not present in the original context

Respond with a JSON object in this exact format:
{{
  "grade": "correct" | "partial" | "wrong" | "hallucinated",
  "score": 1.0 | 0.5 | 0.0 | -0.5,
  "reasoning": "Brief explanation of your grade"
}}

Be strict but fair. The agent should demonstrate factual recall, not just plausible guesses."#,
            response.probe.question,
            response.probe.expected,
            response.probe.rubric,
            response.answer
        );

        let (grade, score, reasoning) = match self.provider.as_str() {
            "anthropic" => self.grade_with_anthropic(&prompt).await?,
            "openai" => self.grade_with_openai(&prompt).await?,
            _ => anyhow::bail!("Unsupported grading provider: {}", self.provider),
        };

        Ok(GradedResponse {
            probe: response.probe.clone(),
            answer: response.answer.clone(),
            tool_call_count: response.tool_call_count,
            score,
            grade,
            reasoning,
        })
    }

    async fn grade_with_anthropic(&self, prompt: &str) -> Result<(String, f64, String)> {
        #[derive(Serialize)]
        struct AnthropicRequest {
            model: String,
            max_tokens: usize,
            temperature: f32,
            messages: Vec<Message>,
        }

        #[derive(Serialize)]
        struct Message {
            role: String,
            content: String,
        }

        #[derive(Deserialize)]
        struct AnthropicResponse {
            content: Vec<ContentBlock>,
        }

        #[derive(Deserialize)]
        #[serde(tag = "type")]
        enum ContentBlock {
            #[serde(rename = "text")]
            Text { text: String },
        }

        let request = AnthropicRequest {
            model: self.model.clone(),
            max_tokens: 1024,
            temperature: 0.0,
            messages: vec![Message {
                role: "user".to_string(),
                content: prompt.to_string(),
            }],
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

        // Extract text from first content block
        let text = response
            .content
            .iter()
            .find_map(|block| match block {
                ContentBlock::Text { text } => Some(text.clone()),
            })
            .context("No text in response")?;

        // Parse JSON from the response (might be wrapped in markdown)
        let json_str = if text.contains("```json") {
            text.split("```json")
                .nth(1)
                .and_then(|s| s.split("```").next())
                .unwrap_or(&text)
                .trim()
        } else if text.contains("```") {
            text.split("```")
                .nth(1)
                .and_then(|s| s.split("```").next())
                .unwrap_or(&text)
                .trim()
        } else {
            text.trim()
        };

        #[derive(Deserialize)]
        struct GradeResult {
            grade: String,
            score: f64,
            reasoning: String,
        }

        let result: GradeResult = serde_json::from_str(json_str)
            .context(format!("Failed to parse grade JSON: {}", json_str))?;

        Ok((result.grade, result.score, result.reasoning))
    }

    async fn grade_with_openai(&self, prompt: &str) -> Result<(String, f64, String)> {
        #[derive(Serialize)]
        struct OpenAIRequest {
            model: String,
            messages: Vec<Message>,
            temperature: f32,
            response_format: ResponseFormat,
        }

        #[derive(Serialize)]
        struct Message {
            role: String,
            content: String,
        }

        #[derive(Serialize)]
        struct ResponseFormat {
            #[serde(rename = "type")]
            format_type: String,
        }

        #[derive(Deserialize)]
        struct OpenAIResponse {
            choices: Vec<Choice>,
        }

        #[derive(Deserialize)]
        struct Choice {
            message: ResponseMessage,
        }

        #[derive(Deserialize)]
        struct ResponseMessage {
            content: String,
        }

        let request = OpenAIRequest {
            model: self.model.clone(),
            messages: vec![Message {
                role: "user".to_string(),
                content: prompt.to_string(),
            }],
            temperature: 0.0,
            response_format: ResponseFormat {
                format_type: "json_object".to_string(),
            },
        };

        let response = self
            .client
            .post("https://api.openai.com/v1/chat/completions")
            .header("Authorization", format!("Bearer {}", self.api_key))
            .json(&request)
            .send()
            .await?
            .error_for_status()?
            .json::<OpenAIResponse>()
            .await?;

        let content = &response.choices[0].message.content;

        #[derive(Deserialize)]
        struct GradeResult {
            grade: String,
            score: f64,
            reasoning: String,
        }

        let result: GradeResult = serde_json::from_str(content)
            .context(format!("Failed to parse grade JSON: {}", content))?;

        Ok((result.grade, result.score, result.reasoning))
    }
}

async fn grade_command(
    results_path: PathBuf,
    provider: String,
    model: String,
    api_key: Option<String>,
    output: Option<PathBuf>,
) -> Result<()> {
    // Resolve API key
    let api_key = api_key
        .or_else(|| match provider.as_str() {
            "anthropic" => std::env::var("ANTHROPIC_API_KEY").ok(),
            "openai" => std::env::var("OPENAI_API_KEY").ok(),
            _ => None,
        })
        .context("API key not provided and not found in environment")?;

    // Load results
    let results_json = fs::read_to_string(&results_path)
        .context("Failed to read results file")?;
    let results: ResultsFile = serde_json::from_str(&results_json)?;

    info!("Loaded {} probe responses from {}", results.probe_responses.len(), results_path.display());
    info!("Grading with {}/{}", provider, model);

    let grader = Grader::new(provider, model, api_key);

    let mut graded_responses = Vec::new();

    for (i, response) in results.probe_responses.iter().enumerate() {
        info!("Grading probe {}/{}: {}", i + 1, results.probe_responses.len(), response.probe.question);

        let graded = grader.grade_response(response).await?;

        info!("  Score: {} ({})", graded.score, graded.grade);
        info!("  Reasoning: {}", graded.reasoning);

        graded_responses.push(graded);
    }

    // Calculate aggregate score
    let total_score: f64 = graded_responses.iter().map(|g| g.score).sum();
    let avg_score = total_score / graded_responses.len() as f64;
    let max_score = graded_responses.len() as f64;
    let retention_score = (avg_score / 1.0) * 100.0; // Normalize to percentage

    info!("\nGrading Summary:");
    info!("  Total responses: {}", graded_responses.len());
    info!("  Average score: {:.2}", avg_score);
    info!("  Retention score: {:.1}%", retention_score);

    #[derive(Serialize)]
    struct GradedResults {
        graded_responses: Vec<GradedResponse>,
        total_responses: usize,
        average_score: f64,
        retention_score: f64,
    }

    let output_data = GradedResults {
        graded_responses,
        total_responses: results.probe_responses.len(),
        average_score: avg_score,
        retention_score,
    };

    let output_json = serde_json::to_string_pretty(&output_data)?;

    if let Some(output_path) = output {
        fs::write(&output_path, &output_json)?;
        info!("Graded results written to {}", output_path.display());
    } else {
        println!("{}", output_json);
    }

    Ok(())
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
        Command::Grade {
            results,
            provider,
            model,
            api_key,
            output,
        } => grade_command(results, provider, model, api_key, output).await?,
    }

    Ok(())
}
