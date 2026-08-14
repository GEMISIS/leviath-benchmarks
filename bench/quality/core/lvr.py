"""run.lvr journal parser + fold.

Port of the reader half of leviath's run-archive codec
(crates/leviath-core/src/run_archive.rs) plus the point replay
(``visit_points``/``replay_points``), stdlib only.

File format (from the Rust module docs and ``write_archive_start`` /
``write_record``)::

    MAGIC ("LVR1") | version (u16 BE) | frame*
    frame := len (u64 BE) | JSON-encoded RunRecord

``RunRecord`` is an externally-tagged serde enum, so every frame's JSON
is ``{"VariantName": {...fields...}}``. The variants that change the
replayed state are Header, Checkpoint, Progress, ContextCheckpoint,
ContextDiff and StatusChanged; ToolBatch / ToolCallDone / Message /
Inference / OwnershipChanged do not produce timeline points (mirroring
``PointFolder::push``). Unknown variants are skipped with a warning,
never a crash.

Reading is lenient like ``read_archive_lenient``: the preamble is
validated strictly, then any torn or unreadable frame (short length
prefix, short payload, oversized length claim, bad JSON) ends the
stream with the records collected so far. Both plain ``run.lvr`` and
gzipped ``run.lvr.gz`` are accepted (sniffed by the gzip magic, not the
file name).
"""
from __future__ import annotations

import gzip
import io
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import BinaryIO, Iterable, Union

MAGIC = b"LVR1"

# Sanity bound on a frame's claimed length, mirroring MAX_RECORD_BYTES in
# the Rust: a torn length prefix must not be taken at its word.
MAX_RECORD_BYTES = 256 * 1024 * 1024

Source = Union[str, Path, bytes, bytearray, BinaryIO]


@dataclass
class RunPoint:
    """The run's context window at one recorded point, with the metadata
    (stage, iteration, tool_calls, status, ...) in effect then."""

    meta: dict
    regions: dict  # name -> {kind, current_tokens, max_tokens, entries: [...]}
    at: int
    stage_name: str = ""
    total_tokens: int = 0
    max_tokens: int = 0


# ─── entry / snapshot conversion ────────────────────────────────────────


def entry_dict(raw: dict) -> dict:
    """Convert one RegionEntrySnapshot JSON object to the neutral dict form.

    The serde shape of ``EntryKind`` is internally tagged
    (``#[serde(tag = "type")]``, variant names verbatim):
    ``{"type": "Text"}``, ``{"type": "UserMessage"}``,
    ``{"type": "AssistantTurn", "tool_calls": [...]}`` and
    ``{"type": "ToolResult", "tool_call_id": .., "tool_name": ..,
    "is_error": ..}``. A missing ``kind`` defaults to Text (serde
    default), matching older snapshots.
    """
    out = {"content": raw.get("content", ""), "tokens": raw.get("tokens", 0)}
    kind = raw.get("kind") or {"type": "Text"}
    tag = kind.get("type", "Text") if isinstance(kind, dict) else str(kind)
    if tag == "UserMessage":
        out["kind"] = "user_message"
    elif tag == "AssistantTurn":
        out["kind"] = "assistant_turn"
        out["tool_calls"] = [
            {
                "id": tc.get("id", ""),
                "name": tc.get("name", ""),
                "arguments": tc.get("arguments"),
                "thought_signature": tc.get("thought_signature"),
            }
            for tc in kind.get("tool_calls", [])
        ]
    elif tag == "ToolResult":
        out["kind"] = "tool_result"
        out["tool_call_id"] = kind.get("tool_call_id", "")
        out["tool_name"] = kind.get("tool_name", "")
        out["is_error"] = bool(kind.get("is_error", False))
    else:  # "Text" and anything unrecognized falls back to text
        out["kind"] = "text"
    if raw.get("key") is not None:
        out["key"] = raw["key"]
    if raw.get("metadata") is not None:
        out["metadata"] = raw["metadata"]
    out["taint"] = raw.get("taint", "Public")
    return out


def snapshot_regions(snapshot: dict) -> dict:
    """Convert a raw ContextSnapshot JSON object (the shape of both the
    journal's checkpoint records and the persisted ``context.json``) into
    the ``RunPoint.regions`` dict form, preserving region order."""
    regions: dict = {}
    for r in snapshot.get("regions", []):
        regions[r["name"]] = {
            "kind": r.get("kind", ""),
            "current_tokens": r.get("current_tokens", 0),
            "max_tokens": r.get("max_tokens", 0),
            # `entries` is skip_serializing_if empty in the Rust.
            "entries": [entry_dict(e) for e in r.get("entries", [])],
        }
    return regions


# ─── framed reader ──────────────────────────────────────────────────────


def _open(source: Source) -> tuple[BinaryIO, list[BinaryIO]]:
    """A binary stream over `source`, transparently gunzipping (sniffed by
    the gzip magic bytes, so bytes input needs no file name), plus the
    streams the caller must close (only ones opened here)."""
    to_close: list[BinaryIO] = []
    if isinstance(source, (bytes, bytearray)):
        stream: BinaryIO = io.BytesIO(bytes(source))
    elif isinstance(source, (str, Path)):
        stream = open(source, "rb")
        to_close.append(stream)
    else:
        stream = source
    head = stream.read(2)
    stream.seek(-len(head), io.SEEK_CUR)
    if head == b"\x1f\x8b":
        stream = gzip.GzipFile(fileobj=stream)  # type: ignore[assignment]
        to_close.append(stream)
    return stream, to_close


def _read_exact_or_eof(stream: BinaryIO, n: int) -> bytes | None:
    """`n` bytes, or None on a clean zero-byte EOF. A *partial* read
    (truncation) raises EOFError, mirroring `read_exact_or_eof`."""
    buf = stream.read(n)
    if len(buf) == n:
        return buf
    if len(buf) == 0:
        return None
    raise EOFError("truncated run-archive frame")


def read_archive(source: Source) -> tuple[int, list[dict], list[str]]:
    """Read an archive leniently: ``(version, records, warnings)``.

    The preamble (magic + version) is validated strictly; frames are read
    until a clean end-of-stream or the first unreadable frame, like the
    Rust ``read_archive_lenient``. Each record is the raw parsed JSON
    object ``{"VariantName": {...}}``. Unrecognized variants are kept in
    ``records`` untouched (fold skips them) but noted in ``warnings``.
    """
    stream, to_close = _open(source)
    try:
        preamble = stream.read(6)
        if len(preamble) < 4 or preamble[:4] != MAGIC:
            raise ValueError("not a leviath run archive (bad magic)")
        if len(preamble) < 6:
            raise ValueError("truncated run-archive preamble")
        version = int.from_bytes(preamble[4:6], "big")
        records: list[dict] = []
        warnings: list[str] = []
        while True:
            try:
                len_bytes = _read_exact_or_eof(stream, 8)
                if len_bytes is None:
                    break
                length = int.from_bytes(len_bytes, "big")
                if length > MAX_RECORD_BYTES:
                    warnings.append(
                        f"frame claims {length} bytes, over the "
                        f"{MAX_RECORD_BYTES} cap; stopping at torn tail")
                    break
                payload = _read_exact_or_eof(stream, length)
                if payload is None:
                    raise EOFError("truncated run-archive frame")
                record = json.loads(payload)
            except (EOFError, OSError, json.JSONDecodeError, UnicodeDecodeError):
                # Torn tail: keep everything intact before it.
                break
            if not (isinstance(record, dict) and len(record) == 1):
                warnings.append(f"malformed record (not a tagged object): "
                                f"{str(record)[:80]}")
            elif next(iter(record)) not in _KNOWN_VARIANTS:
                warnings.append(f"unknown record variant: {next(iter(record))}")
            records.append(record)
        return version, records, warnings
    finally:
        for s in reversed(to_close):
            s.close()


_KNOWN_VARIANTS = frozenset({
    "Header", "OwnershipChanged", "Inference", "ToolBatch", "ToolCallDone",
    "ContextCheckpoint", "ContextDiff", "Message", "StatusChanged",
    "Checkpoint", "Progress",
    # lev 0.3.10 (leviath#445): per-provider-call usage, written as it
    # lands - the exact per-request record the footprint fold prefers.
    "InferenceUsage",
})


# ─── delta application (port of apply_delta) ────────────────────────────


def _apply_delta(state: "_FoldState", delta: dict) -> None:
    """Apply a ContextDelta to the running region list in place. Lenient:
    a delta naming an absent region is skipped, mirroring the Rust."""
    state.stage_name = delta.get("stage_name", "")
    state.total_tokens = delta.get("total_tokens", 0)
    state.max_tokens = delta.get("max_tokens", 0)
    for region_delta in delta.get("regions", []):
        if not (isinstance(region_delta, dict) and len(region_delta) == 1):
            continue
        tag, body = next(iter(region_delta.items()))
        if tag == "Set":
            replacement = {
                "name": body["name"],
                "kind": body.get("kind", ""),
                "current_tokens": body.get("current_tokens", 0),
                "max_tokens": body.get("max_tokens", 0),
                "entries": list(body.get("entries", [])),
            }
            for i, r in enumerate(state.regions):
                if r["name"] == body["name"]:
                    state.regions[i] = replacement
                    break
            else:
                state.regions.append(replacement)
        elif tag == "Append":
            for r in state.regions:
                if r["name"] == body["name"]:
                    r["entries"] = r["entries"] + list(body.get("entries", []))
                    r["current_tokens"] = body.get("current_tokens", 0)
                    break
        elif tag == "Clear":
            for r in state.regions:
                if r["name"] == body["name"]:
                    r["entries"] = []
                    r["current_tokens"] = 0
                    break
        elif tag == "Remove":
            state.regions = [r for r in state.regions
                             if r["name"] != body["name"]]


@dataclass
class _FoldState:
    meta: dict
    stage_name: str = ""
    total_tokens: int = 0
    max_tokens: int = 0
    regions: list = field(default_factory=list)

    def load_snapshot(self, snapshot: dict) -> None:
        self.stage_name = snapshot.get("stage_name", "")
        self.total_tokens = snapshot.get("total_tokens", 0)
        self.max_tokens = snapshot.get("max_tokens", 0)
        self.regions = [
            {
                "name": r["name"],
                "kind": r.get("kind", ""),
                "current_tokens": r.get("current_tokens", 0),
                "max_tokens": r.get("max_tokens", 0),
                "entries": list(r.get("entries", [])),
            }
            for r in snapshot.get("regions", [])
        ]

    def to_point(self, at: int) -> RunPoint:
        regions = {
            r["name"]: {
                "kind": r["kind"],
                "current_tokens": r["current_tokens"],
                "max_tokens": r["max_tokens"],
                "entries": [entry_dict(e) for e in r["entries"]],
            }
            for r in self.regions
        }
        return RunPoint(meta=dict(self.meta), regions=regions, at=at,
                        stage_name=self.stage_name,
                        total_tokens=self.total_tokens,
                        max_tokens=self.max_tokens)


# ─── fold ───────────────────────────────────────────────────────────────


def fold(source: Source, warnings: list[str] | None = None) -> list[RunPoint]:
    """Replay a run journal into its timeline of context-window points.

    One :class:`RunPoint` per record that changes the context (a
    ContextCheckpoint, ContextDiff, Checkpoint or Progress step), in
    order - mirroring ``visit_points``/``replay_points`` in the Rust.
    Header and StatusChanged update the carried metadata without adding a
    point. Returns ``[]`` when the journal does not start with a Header.

    `warnings`, when given, collects the parse warnings (unknown record
    variants, torn-tail notes) from :func:`read_archive`.
    """
    _version, records, warns = read_archive(source)
    if warnings is not None:
        warnings.extend(warns)
    it = iter(records)
    first = next(it, None)
    if not (isinstance(first, dict) and "Header" in first):
        return []
    state = _FoldState(meta=dict(first["Header"].get("meta", {})))
    points: list[RunPoint] = []
    for record in it:
        if not (isinstance(record, dict) and len(record) == 1):
            continue
        tag, body = next(iter(record.items()))
        if tag == "Header":
            state.meta = dict(body.get("meta", {}))
        elif tag == "StatusChanged":
            state.meta["status"] = body.get("status")
        elif tag == "ContextCheckpoint":
            state.load_snapshot(body.get("snapshot", {}))
            points.append(state.to_point(body.get("at", 0)))
        elif tag == "ContextDiff":
            _apply_delta(state, body.get("delta", {}))
            points.append(state.to_point(body.get("at", 0)))
        elif tag == "Checkpoint":
            state.meta = dict(body.get("meta", {}))
            state.load_snapshot(body.get("context", {}))
            points.append(state.to_point(body.get("at", 0)))
        elif tag == "Progress":
            state.meta = dict(body.get("meta", {}))
            _apply_delta(state, body.get("delta", {}))
            points.append(state.to_point(body.get("at", 0)))
        # Every other variant (known or unknown) adds no timeline point.
    return points


def point_at_depth(points: Iterable[RunPoint],
                   n_tool_calls: int) -> tuple[RunPoint, int] | None:
    """The first point whose ``meta.tool_calls`` has reached
    `n_tool_calls`, with the actual count there - or None if the run
    never made that many calls."""
    for point in points:
        actual = point.meta.get("tool_calls", 0)
        if actual >= n_tool_calls:
            return point, actual
    return None
