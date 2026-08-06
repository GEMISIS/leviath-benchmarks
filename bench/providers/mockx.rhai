// @name mockx
// @max_context_tokens 200000
// Stage-aware deterministic provider for realistic multi-stage load tests.
// No network, no cost. It recognises the four request shapes the engine
// sends and answers each so any bundled blueprint traverses its whole
// stage graph and completes:
//   1. transition routing (no tools, <=256 max_tokens, "Respond with ONLY"):
//      answer with the FIRST listed edge - revisit budgets guarantee the
//      graph still converges, while maximising stage churn.
//   2. fan-out split (system prompt carries the <short-slug> JSON template):
//      answer with a 3-worker JSON array.
//   3. output stages (submit_output offered): call it once, then finish.
//   4. normal stage turns: two ~2KB context_append calls into the
//      conversation region (declared by every bundled agent), then finish
//      the stage so the transition fires.

fn initialize(config) {
    #{}
}

fn text_of(content) {
    if type_of(content) == "string" {
        content
    } else {
        let s = "";
        for b in content {
            if b["type"] == "text" {
                s += b.text;
            }
        }
        s
    }
}

fn usage(pt, ct) {
    #{
        prompt_tokens: pt,
        completion_tokens: ct,
        total_tokens: pt + ct,
        cached_tokens: 0,
        cache_write_tokens: 0
    }
}

fn payload(tag) {
    let chunk = "mockx payload " + tag + " ------------------------------ ";
    let s = "";
    let i = 0;
    while i < 40 {
        s += chunk;
        i += 1;
    }
    s
}

fn inference(state, request) {
    // Optional simulated model latency: when the daemon is started with
    // LEVMOCK_LATENCY_MS set, every call blocks that long against a local
    // latency server, so agents overlap the way they do against a real
    // provider instead of draining at mock speed. Unset = instant (the
    // throughput-benchmark mode).
    let lat = 0;
    try { lat = parse_int(env_var("LEVMOCK_LATENCY_MS")); } catch(e) { lat = 0; }
    if lat > 0 {
        try { http_get("http://127.0.0.1:18742/?ms=" + lat); } catch(e) {}
    }

    let tool_names = [];
    for t in request.tools {
        tool_names.push(t.name);
    }

    let last_user = "";
    let assistants = 0;
    let submitted = false;
    let appends_visible = 0;
    let last_is_tool_result = false;
    for msg in request.messages {
        if msg.role == "assistant" {
            assistants += 1;
            last_is_tool_result = false;
            if type_of(msg.content) != "string" {
                for b in msg.content {
                    if b["type"] == "tool_use" {
                        if b.name == "submit_output" {
                            submitted = true;
                        }
                        if b.name == "context_append" {
                            appends_visible += 1;
                        }
                    }
                }
            }
        }
        if msg.role == "user" {
            let t = text_of(msg.content);
            last_user = t;
            last_is_tool_result = false;
            if type_of(msg.content) != "string" {
                for b in msg.content {
                    if b["type"] == "tool_result" {
                        last_is_tool_result = true;
                        if b.content.contains("invalid arguments for 'submit_output'") {
                            submitted = false;
                        }
                    }
                }
            }
        }
    }

    // 1. Transition routing call.
    if request.tools.len() == 0 && request.max_tokens <= 256
        && last_user.contains("Respond with ONLY") {
        let target = "DONE";
        for line in last_user.split("\n") {
            if line.index_of("- ") == 0 {
                let rest = line.sub_string(2, line.len() - 2);
                let ci = rest.index_of(":");
                if ci >= 0 {
                    rest = rest.sub_string(0, ci);
                }
                let cs = rest.index_of(" ");
                if cs >= 0 {
                    rest = rest.sub_string(0, cs);
                }
                target = rest;
                break;
            }
        }
        return #{
            content: target,
            tool_calls: [],
            tokens_used: usage(500, 5),
            finish_reason: "Complete"
        };
    }

    // 2. Fan-out split: emit the worker array the split prompt asks for.
    let sys = "";
    for b in request.system {
        sys += b.text;
    }
    if sys.contains("<short-slug>") {
        let items = "[";
        let w = 0;
        while w < 3 {
            if w > 0 { items += ","; }
            items += "{\"id\":\"worker" + w + "\",\"context\":{\"slice\":\"partition " + w + "\",\"schema\":\"name, value, source\"}}";
            w += 1;
        }
        items += "]";
        return #{
            content: items,
            tool_calls: [],
            tokens_used: usage(1200, 80),
            finish_reason: "Complete"
        };
    }

    // 3. Output stage: submit once, then finish.
    if "submit_output" in tool_names {
        if submitted {
            return #{
                content: "Output submitted; nothing further.",
                tool_calls: [],
                tokens_used: usage(800, 10),
                finish_reason: "Complete"
            };
        }
        return #{
            content: "Submitting the final result.",
            tool_calls: [
                #{
                    id: "call_submit_" + assistants,
                    name: "submit_output",
                    arguments: #{
                        content: "## Mock deliverable\n\nDeterministic summary produced after " + assistants + " visible turns. Findings: the mock landscape has three approaches; approach B wins on tradeoffs."
                    }
                }
            ],
            tokens_used: usage(900, 120),
            finish_reason: "ToolCall"
        };
    }

    // 4. Normal stage turn. The FIRST response of any stage visit is always a
    // tool call so the engine can never treat a carried-over completion as
    // this stage's answer; right after our own tool result comes back, finish
    // the stage so the transition fires. Net: two inferences per stage visit.
    if !last_is_tool_result && appends_visible < 12 && "context_append" in tool_names {
        return #{
            content: "Working: recording findings, turn " + assistants + ".",
            tool_calls: [
                #{
                    id: "call_append_" + assistants,
                    name: "context_append",
                    arguments: #{
                        region: "notes",
                        content: payload(assistants)
                    }
                }
            ],
            tokens_used: usage(1000, 150),
            finish_reason: "ToolCall"
        };
    }

    #{
        content: "Stage objective met after " + assistants + " visible turns; ready to move on.",
        tool_calls: [],
        tokens_used: usage(1000, 30),
        finish_reason: "Complete"
    }
}
