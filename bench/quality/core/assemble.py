"""Provider-request reconstruction from a folded run point.

Port of ``ContextWindow::assemble_with_meta``
(crates/leviath-runtime/src/components/context_window.rs) for the region
kinds the benchmark blueprints use: pinned, compacting,
compact_history, clearable, temporary, sliding_window, hashmap
(accepting both the blueprint spellings and the snapshot spellings
"history"/"sliding" the persistence layer writes). Output is a neutral
dict; a separate provider layer adapts it to HTTP requests.

Faithfully reproduced, in the Rust's order:

- empty non-custom regions emit nothing;
- pinned / compact_history render as unlabeled system blocks (entries
  joined with a blank line) at cache tier "always";
- compacting -> ``[{name}]:\\n{joined}`` at "until_changed";
- temporary and clearable -> the same label format at "never";
- hashmap -> keyed entries rendered ``### [{key}]\\n{content}`` (bare
  content when keyless), joined, wrapped ``[{name}]:\\n...`` at
  "until_changed";
- sliding_window entries become typed messages: user_message -> user
  turn; assistant_turn -> assistant turn (tool calls as tool_use blocks
  with id/name/input); tool_result -> tool_result block, with
  consecutive tool results merged into ONE user message; text entries
  fall back to the ``Assistant: `` / ``User: `` prefix parse (default
  role user);
- system blocks then stably sorted by cache-tier priority
  (always=0, sliding_prefix=1, until_changed=recently_changed=2,
  never=3), i.e. ``cache_hint_sort_priority``;
- orphaned tool_use / tool_result blocks stripped (a block-content
  message left empty by the strip is dropped);
- one message cache breakpoint: 4th-from-last when >= 5 messages, else
  the first when >= 2;
- a ``Begin.`` user message when no user message exists, and a
  ``Continue.`` user message when the conversation ends on an
  assistant turn.

Knowingly NOT reproduced:

- framework hint blocks (the batch/shell hints inference.rs prepends to
  the system prompt) - they are added at request-build time and are not
  journaled;
- per-stage hidden-region filtering (scoped blueprints): the set of
  regions a stage hides is blueprint state, not journal state, so every
  region present at the point is rendered;
- ``mark_recently_changed_run`` (the cache-breakpoint split of the
  volatile system tier): it keys off per-entry timestamps, which the
  snapshot format does not carry. It never reorders blocks (it runs
  after the sort and "recently_changed" shares "until_changed"'s sort
  tier), so only cache-breakpoint metadata differs;
- checklist and custom (script-backed) regions: raise
  ``ValueError("unsupported region kind: ...")``.

``tool_names`` in the output is derived from the tool_use blocks present
in the assembled messages (first-use order). The tool list actually
offered to the provider comes from the blueprint stage and is not
journaled.
"""
from __future__ import annotations

from typing import Iterable, Mapping

# cache_hint_sort_priority, ported verbatim (lower = earlier).
_HINT_PRIORITY = {
    "always": 0,
    "sliding_prefix": 1,
    "until_changed": 2,
    "recently_changed": 2,
    "never": 3,
}

# Snapshot spellings (persistence.rs region_kind_str) + blueprint spellings.
_KIND_ALIASES = {
    "pinned": "pinned",
    "compacting": "compacting",
    "history": "compact_history",
    "compact_history": "compact_history",
    "clearable": "clearable",
    "temporary": "temporary",
    "sliding": "sliding_window",
    "sliding_window": "sliding_window",
    "hashmap": "hashmap",
    "checklist": "checklist",
    "custom": "custom",
}


def _join(entries: list[dict]) -> str:
    return "\n\n".join(e.get("content", "") for e in entries)


def _sliding_window_messages(entries: Iterable[dict],
                             messages: list[dict]) -> None:
    """Port of the SlidingWindow arm: typed entries -> messages, with
    consecutive tool results merged into one user message."""
    pending_tool_results: list[dict] = []

    def flush() -> None:
        if pending_tool_results:
            messages.append({"role": "user",
                             "content": list(pending_tool_results),
                             "cache_breakpoint": False})
            pending_tool_results.clear()

    for entry in entries:
        kind = entry.get("kind", "text")
        if kind != "tool_result":
            flush()
        content = entry.get("content", "")
        if kind == "user_message":
            messages.append({"role": "user", "content": content,
                             "cache_breakpoint": False})
        elif kind == "assistant_turn":
            tool_calls = entry.get("tool_calls") or []
            if not tool_calls:
                messages.append({"role": "assistant", "content": content,
                                 "cache_breakpoint": False})
            else:
                blocks: list[dict] = []
                if content:
                    blocks.append({"type": "text", "text": content})
                for tc in tool_calls:
                    block = {"type": "tool_use", "id": tc.get("id", ""),
                             "name": tc.get("name", ""),
                             "input": tc.get("arguments")}
                    if tc.get("thought_signature") is not None:
                        block["thought_signature"] = tc["thought_signature"]
                    blocks.append(block)
                messages.append({"role": "assistant", "content": blocks,
                                 "cache_breakpoint": False})
        elif kind == "tool_result":
            pending_tool_results.append({
                "type": "tool_result",
                "tool_use_id": entry.get("tool_call_id", ""),
                "content": content,
                "is_error": bool(entry.get("is_error", False)),
            })
        else:  # text: prefix-parse fallback
            trimmed = content.strip()
            if trimmed.startswith("Assistant: "):
                messages.append({"role": "assistant",
                                 "content": trimmed[len("Assistant: "):],
                                 "cache_breakpoint": False})
            elif trimmed.startswith("User: "):
                messages.append({"role": "user",
                                 "content": trimmed[len("User: "):],
                                 "cache_breakpoint": False})
            else:
                messages.append({"role": "user", "content": content,
                                 "cache_breakpoint": False})
    flush()


def _sanitize_orphans(messages: list[dict]) -> list[dict]:
    """Strip tool_use/tool_result blocks without a matching pair; drop a
    block-content message the strip leaves empty."""
    tool_use_ids = set()
    tool_result_ids = set()
    for msg in messages:
        if isinstance(msg["content"], list):
            for block in msg["content"]:
                if block.get("type") == "tool_use":
                    tool_use_ids.add(block["id"])
                elif block.get("type") == "tool_result":
                    tool_result_ids.add(block["tool_use_id"])
    orphaned_uses = tool_use_ids - tool_result_ids
    orphaned_results = tool_result_ids - tool_use_ids
    if not orphaned_uses and not orphaned_results:
        return messages
    out = []
    for msg in messages:
        if not isinstance(msg["content"], list):
            out.append(msg)
            continue
        filtered = [
            b for b in msg["content"]
            if not (b.get("type") == "tool_use" and b["id"] in orphaned_uses)
            and not (b.get("type") == "tool_result"
                     and b["tool_use_id"] in orphaned_results)
        ]
        if filtered:
            out.append({**msg, "content": filtered})
    return out


def assemble(point) -> dict:
    """Assemble a folded :class:`~core.lvr.RunPoint` (or any object/dict
    with a ``regions`` mapping in region order) into the provider-neutral
    request shape::

        {"system": [{"text": .., "cache_hint": ..}, ...],
         "messages": [{"role": .., "content": [block, ...],
                       "cache_breakpoint": bool}, ...],
         "tool_names": [..]}

    Message content is normalized to a list of blocks (``text`` /
    ``tool_use`` / ``tool_result``) after the faithful string-vs-blocks
    processing the Rust applies.
    """
    if isinstance(point, Mapping):
        regions = point["regions"]
    else:
        regions = point.regions

    system_blocks: list[dict] = []
    messages: list[dict] = []

    for name, region in regions.items():
        raw_kind = region.get("kind", "")
        kind = _KIND_ALIASES.get(raw_kind)
        if kind is None:
            raise ValueError(f"unsupported region kind: {raw_kind}")
        entries = region.get("entries", [])
        # Every non-custom kind skips an empty region (custom would render
        # even when empty in the Rust, but custom is unsupported here).
        if not entries and kind != "custom":
            continue
        if kind in ("checklist", "custom"):
            raise ValueError(f"unsupported region kind: {raw_kind}")

        if kind in ("pinned", "compact_history"):
            system_blocks.append({"text": _join(entries),
                                  "cache_hint": "always"})
        elif kind == "compacting":
            system_blocks.append({"text": f"[{name}]:\n{_join(entries)}",
                                  "cache_hint": "until_changed"})
        elif kind in ("temporary", "clearable"):
            system_blocks.append({"text": f"[{name}]:\n{_join(entries)}",
                                  "cache_hint": "never"})
        elif kind == "hashmap":
            text = "\n\n".join(
                f"### [{e['key']}]\n{e.get('content', '')}"
                if e.get("key") is not None else e.get("content", "")
                for e in entries)
            system_blocks.append({"text": f"[{name}]:\n{text}",
                                  "cache_hint": "until_changed"})
        elif kind == "sliding_window":
            _sliding_window_messages(entries, messages)

    # Stable sort by cache-tier priority (Python's sort is stable, like
    # Rust's sort_by_key).
    system_blocks.sort(key=lambda b: _HINT_PRIORITY[b["cache_hint"]])

    messages = _sanitize_orphans(messages)

    # One cache breakpoint on the stable message prefix.
    if len(messages) >= 5:
        messages[len(messages) - 4]["cache_breakpoint"] = True
    elif len(messages) >= 2:
        messages[0]["cache_breakpoint"] = True

    if not any(m["role"] == "user" for m in messages):
        messages.append({"role": "user", "content": "Begin.",
                         "cache_breakpoint": False})
    if messages and messages[-1]["role"] == "assistant":
        messages.append({"role": "user", "content": "Continue.",
                         "cache_breakpoint": False})

    # Normalize plain-string content to a single text block.
    for msg in messages:
        if not isinstance(msg["content"], list):
            msg["content"] = [{"type": "text", "text": msg["content"]}]

    tool_names: list[str] = []
    for msg in messages:
        for block in msg["content"]:
            if block.get("type") == "tool_use" and block["name"] not in tool_names:
                tool_names.append(block["name"])

    return {"system": system_blocks, "messages": messages,
            "tool_names": tool_names}
