"""Direct provider chat clients for the probe-replay phase.

One-shot calls only: the replay engine reconstructs a full request from
a run's journal (core/assemble.py) and needs a single completion at a
pinned temperature; the grader needs a single text-in/text-out call.
Nothing here streams, retries a run, or touches the daemon. stdlib
urllib only, keys from the same .env the runner loads, and a
``transport`` hook so tests never hit the network.

Message shape in: assemble.py's neutral form -
{"system": [{text, cache_hint}], "messages": [{role, content: [typed
blocks]}]} - plus a list of tool names. Providers that reject tool_use
blocks without tool definitions get permissive stub schemas for every
tool name; if a provider still refuses typed blocks, callers can ask
for ``encoding="flattened"`` which renders tool traffic as plain text
(recorded per probe, so mixed rounds stay auditable).
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request

__all__ = ["ProviderError", "call_chat", "flatten_messages"]

_RETRIES = 4
_BACKOFF_SECS = 5.0
_TIMEOUT_SECS = 300


class ProviderError(RuntimeError):
    pass


def _stub_tools_anthropic(names: list[str]) -> list[dict]:
    return [{"name": n, "description": "recorded tool from the run",
             "input_schema": {"type": "object",
                              "additionalProperties": True}}
            for n in names]


def _stub_tools_openai(names: list[str]) -> list[dict]:
    return [{"type": "function",
             "function": {"name": n,
                          "description": "recorded tool from the run",
                          "parameters": {"type": "object",
                                         "additionalProperties": True}}}
            for n in names]


def flatten_messages(messages: list[dict]) -> list[dict]:
    """Typed tool traffic rendered as plain text turns (fallback
    encoding for providers that refuse reconstructed tool blocks)."""
    out = []
    for msg in messages:
        parts = []
        for block in msg.get("content", []):
            kind = block.get("type")
            if kind == "text":
                parts.append(block.get("text", ""))
            elif kind == "tool_use":
                parts.append(f"[tool call {block.get('name')}: "
                             f"{json.dumps(block.get('input', {}))[:2000]}]")
            elif kind == "tool_result":
                content = block.get("content")
                if isinstance(content, list):
                    content = " ".join(c.get("text", "")
                                       for c in content
                                       if isinstance(c, dict))
                parts.append(f"[tool result: {str(content)[:4000]}]")
        text = "\n".join(p for p in parts if p)
        if text:
            out.append({"role": msg["role"], "content": text})
    return out


def _http_json(url: str, headers: dict, payload: dict,
               transport=None) -> dict:
    if transport is not None:
        return transport(url, headers, payload)
    body = json.dumps(payload).encode()
    last = None
    for attempt in range(_RETRIES):
        req = urllib.request.Request(url, data=body, headers={
            "Content-Type": "application/json", **headers})
        try:
            with urllib.request.urlopen(req, timeout=_TIMEOUT_SECS) as r:
                return json.load(r)
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode(errors="replace")[:500]
            last = ProviderError(f"HTTP {exc.code}: {detail}")
            if exc.code in (429, 500, 502, 503, 529) \
                    and attempt < _RETRIES - 1:
                time.sleep(_BACKOFF_SECS * (2 ** attempt))
                continue
            raise last
        except OSError as exc:
            last = ProviderError(f"network: {exc}")
            if attempt < _RETRIES - 1:
                time.sleep(_BACKOFF_SECS * (2 ** attempt))
                continue
            raise last
    raise last  # pragma: no cover


def call_chat(model_id: str, system_blocks: list[dict],
              messages: list[dict], tool_names: list[str], *,
              temperature: float, max_tokens: int, keys: dict,
              encoding: str = "typed", transport=None) -> dict:
    """One completion. Returns {"text", "usage", "encoding"}.

    ``model_id`` is the roster form (``anthropic/...``, ``openai/...``,
    ``openrouter/<vendor>/<model>``); ``keys`` maps env-style names
    (ANTHROPIC_API_KEY, ...) to values.
    """
    provider, _, model = model_id.partition("/")
    if provider == "anthropic":
        return _call_anthropic(model, system_blocks, messages, tool_names,
                               temperature=temperature,
                               max_tokens=max_tokens, keys=keys,
                               encoding=encoding, transport=transport)
    if provider in ("openai", "openrouter"):
        return _call_openai_style(provider, model, system_blocks, messages,
                                  tool_names, temperature=temperature,
                                  max_tokens=max_tokens, keys=keys,
                                  encoding=encoding, transport=transport)
    raise ProviderError(f"no client for provider {provider!r}")


def _call_anthropic(model: str, system_blocks: list[dict],
                    messages: list[dict], tool_names: list[str], *,
                    temperature, max_tokens, keys, encoding,
                    transport) -> dict:
    key = keys.get("ANTHROPIC_API_KEY")
    if not key:
        raise ProviderError("ANTHROPIC_API_KEY missing")
    system = [{"type": "text", "text": b["text"]} for b in system_blocks]
    if system:
        # One breakpoint at the end of the reconstructed prefix: probes
        # replayed depth-ascending share a growing cached prefix.
        system[-1]["cache_control"] = {"type": "ephemeral"}
    msgs = (flatten_messages(messages) if encoding == "flattened"
            else messages)
    payload = {"model": model, "max_tokens": max_tokens,
               "temperature": temperature, "system": system,
               "messages": msgs}
    if encoding == "typed" and tool_names:
        payload["tools"] = _stub_tools_anthropic(tool_names)
    out = _http_json("https://api.anthropic.com/v1/messages",
                     {"x-api-key": key,
                      "anthropic-version": "2023-06-01"},
                     payload, transport)
    text = " ".join(b.get("text", "") for b in out.get("content", [])
                    if b.get("type") == "text").strip()
    u = out.get("usage", {})
    usage = {"prompt_tokens": u.get("input_tokens", 0),
             "completion_tokens": u.get("output_tokens", 0),
             "cached_tokens": u.get("cache_read_input_tokens", 0),
             "cache_write_tokens": u.get("cache_creation_input_tokens", 0)}
    return {"text": text, "usage": usage, "encoding": encoding}


def _to_openai_messages(system_blocks: list[dict],
                        messages: list[dict]) -> list[dict]:
    out = []
    system_text = "\n\n".join(b["text"] for b in system_blocks)
    if system_text:
        out.append({"role": "system", "content": system_text})
    for msg in messages:
        blocks = msg.get("content", [])
        if msg["role"] == "assistant":
            text = " ".join(b.get("text", "") for b in blocks
                            if b.get("type") == "text").strip()
            calls = [{"id": b.get("id") or f"call_{i}",
                      "type": "function",
                      "function": {"name": b.get("name"),
                                   "arguments": json.dumps(
                                       b.get("input", {}))}}
                     for i, b in enumerate(blocks)
                     if b.get("type") == "tool_use"]
            entry = {"role": "assistant", "content": text or None}
            if calls:
                entry["tool_calls"] = calls
            out.append(entry)
            continue
        # user turn: tool results become role=tool messages, text stays
        results = [b for b in blocks if b.get("type") == "tool_result"]
        texts = [b.get("text", "") for b in blocks
                 if b.get("type") == "text"]
        for b in results:
            content = b.get("content")
            if isinstance(content, list):
                content = " ".join(c.get("text", "") for c in content
                                   if isinstance(c, dict))
            out.append({"role": "tool",
                        "tool_call_id": b.get("tool_use_id")
                        or b.get("tool_call_id") or "call_0",
                        "content": str(content or "")})
        if texts:
            out.append({"role": "user", "content": "\n".join(texts)})
    return out


def _call_openai_style(provider: str, model: str, system_blocks: list[dict],
                       messages: list[dict], tool_names: list[str], *,
                       temperature, max_tokens, keys, encoding,
                       transport) -> dict:
    if provider == "openai":
        key = keys.get("OPENAI_API_KEY")
        url = "https://api.openai.com/v1/chat/completions"
    else:
        key = keys.get("OPENROUTER_API_KEY")
        url = "https://openrouter.ai/api/v1/chat/completions"
    if not key:
        raise ProviderError(f"{provider} API key missing")
    if encoding == "flattened":
        msgs = _to_openai_messages(system_blocks, [])
        msgs += flatten_messages(messages)
    else:
        msgs = _to_openai_messages(system_blocks, messages)
    payload = {"model": model, "messages": msgs}
    # OpenAI's current models reject `max_tokens` in favor of
    # `max_completion_tokens`, and their reasoning models refuse any
    # temperature but the default - so that provider gets neither knob.
    # OpenRouter still speaks the classic names.
    if provider == "openai":
        payload["max_completion_tokens"] = max_tokens
    else:
        payload["max_tokens"] = max_tokens
        payload["temperature"] = temperature
    if encoding == "typed" and tool_names:
        payload["tools"] = _stub_tools_openai(tool_names)
    out = _http_json(url, {"Authorization": f"Bearer {key}"},
                     payload, transport)
    choice = (out.get("choices") or [{}])[0]
    text = ((choice.get("message") or {}).get("content") or "").strip()
    u = out.get("usage", {})
    details = u.get("prompt_tokens_details") or {}
    usage = {"prompt_tokens": u.get("prompt_tokens", 0),
             "completion_tokens": u.get("completion_tokens", 0),
             "cached_tokens": details.get("cached_tokens", 0),
             "cache_write_tokens": details.get("cache_write_tokens", 0)}
    return {"text": text, "usage": usage, "encoding": encoding}
