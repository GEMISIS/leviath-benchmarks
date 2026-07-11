use anyhow::Result;
use axum::{
    extract::State,
    http::StatusCode,
    response::IntoResponse,
    routing::post,
    Json, Router,
};
use serde::{Deserialize, Serialize};
use std::sync::Arc;
use tokio::time::{sleep, Duration};
use tracing::info;

#[derive(Clone)]
struct MockProviderState {
    delay_ms: u64,
}

#[derive(Debug, Deserialize)]
struct MessagesRequest {
    model: String,
    messages: Vec<serde_json::Value>,
    #[serde(default)]
    max_tokens: usize,
}

#[derive(Debug, Serialize)]
struct MessagesResponse {
    id: String,
    #[serde(rename = "type")]
    response_type: String,
    role: String,
    content: Vec<ContentBlock>,
    model: String,
    stop_reason: String,
    usage: Usage,
}

#[derive(Debug, Serialize)]
#[serde(tag = "type")]
enum ContentBlock {
    #[serde(rename = "text")]
    Text { text: String },
    #[serde(rename = "tool_use")]
    ToolUse {
        id: String,
        name: String,
        input: serde_json::Value,
    },
}

#[derive(Debug, Serialize)]
struct Usage {
    input_tokens: usize,
    output_tokens: usize,
    #[serde(skip_serializing_if = "Option::is_none")]
    cache_creation_input_tokens: Option<usize>,
    #[serde(skip_serializing_if = "Option::is_none")]
    cache_read_input_tokens: Option<usize>,
}

pub async fn start_server(port: u16, delay_ms: u64) -> Result<()> {
    let state = Arc::new(MockProviderState { delay_ms });

    let app = Router::new()
        .route("/v1/messages", post(handle_messages))
        .with_state(state);

    let addr = format!("0.0.0.0:{}", port);
    let listener = tokio::net::TcpListener::bind(&addr).await?;

    info!("Mock provider listening on {}", addr);

    axum::serve(listener, app).await?;

    Ok(())
}

async fn handle_messages(
    State(state): State<Arc<MockProviderState>>,
    Json(req): Json<MessagesRequest>,
) -> impl IntoResponse {
    // Simulate processing delay
    sleep(Duration::from_millis(state.delay_ms)).await;

    // Determine which iteration this is based on message count
    // Count assistant messages to know which response to send
    let iteration = req.messages.iter()
        .filter(|m| m.get("role").and_then(|r| r.as_str()) == Some("assistant"))
        .count();

    let input_tokens = estimate_tokens(&req.messages);

    // State machine: first response uses list_dir, next 3-5 use read_file, then final text
    let (content, stop_reason) = if iteration == 0 {
        // First response: list_dir tool call
        (vec![ContentBlock::ToolUse {
            id: format!("toolu_{}", uuid::Uuid::new_v4()),
            name: "list_dir".to_string(),
            input: serde_json::json!({"path": "."}),
        }], "tool_use".to_string())
    } else if iteration < 5 {
        // Next 3-4 responses: read_file tool calls
        (vec![ContentBlock::ToolUse {
            id: format!("toolu_{}", uuid::Uuid::new_v4()),
            name: "read_file".to_string(),
            input: serde_json::json!({"path": format!("file{}.txt", iteration)}),
        }], "tool_use".to_string())
    } else {
        // Final response: text only to signal completion
        (vec![ContentBlock::Text {
            text: "I have completed the analysis of the project structure.".to_string(),
        }], "end_turn".to_string())
    };

    // Simulate realistic cache behavior
    let (cache_creation, cache_read) = if iteration == 0 {
        // First request: cache is being created
        (Some(input_tokens), Some(0))
    } else {
        // Subsequent requests: simulate 60-80% cache hit
        let cache_hit_portion = (input_tokens as f64 * 0.7) as usize;
        let new_tokens = input_tokens - cache_hit_portion;
        (Some(new_tokens), Some(cache_hit_portion))
    };

    let response = MessagesResponse {
        id: format!("msg_{}", uuid::Uuid::new_v4()),
        response_type: "message".to_string(),
        role: "assistant".to_string(),
        content,
        model: req.model.clone(),
        stop_reason,
        usage: Usage {
            input_tokens,
            output_tokens: 150,
            cache_creation_input_tokens: cache_creation,
            cache_read_input_tokens: cache_read,
        },
    };

    (StatusCode::OK, Json(response))
}
fn estimate_tokens(messages: &[serde_json::Value]) -> usize {
    // Rough estimate: 4 chars per token
    messages
        .iter()
        .map(|msg| {
            msg.get("content")
                .and_then(|c| c.as_str())
                .map(|s| s.len() / 4)
                .unwrap_or(100)
        })
        .sum()
}
