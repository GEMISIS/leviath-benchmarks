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

    // Generate canned response
    let response = MessagesResponse {
        id: format!("msg_{}", uuid::Uuid::new_v4()),
        response_type: "message".to_string(),
        role: "assistant".to_string(),
        content: vec![ContentBlock::Text {
            text: generate_canned_response(&req),
        }],
        model: req.model.clone(),
        stop_reason: "end_turn".to_string(),
        usage: Usage {
            input_tokens: estimate_tokens(&req.messages),
            output_tokens: 150,
            cache_creation_input_tokens: Some(0),
            cache_read_input_tokens: Some(0),
        },
    };

    (StatusCode::OK, Json(response))
}

fn generate_canned_response(req: &MessagesRequest) -> String {
    // Detect what kind of request this is based on messages
    let last_message = req.messages.last();

    if let Some(msg) = last_message {
        let content = msg.get("content").and_then(|c| c.as_str()).unwrap_or("");

        if content.contains("read_file") || content.contains("list_dir") {
            return "I've examined the codebase structure.".to_string();
        }

        if content.contains("write_file") || content.contains("edit_file") {
            return "I've made the necessary changes to the code.".to_string();
        }

        if content.contains("bash") || content.contains("test") {
            return "The tests are passing successfully.".to_string();
        }
    }

    // Default response
    "I understand the task and will proceed with the implementation.".to_string()
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
