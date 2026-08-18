#!/usr/bin/env python3
"""Generate the read-only counterparts for the hallucination suite's
log tasks (incident-chronicle, noisy-incident).

The condition: no shell, no writes - agents work from file reads
alone. It exists because script-solvable tasks never create context
pressure (agents compute over files on disk and keep tiny contexts),
so the mechanisms the suite measures never engage. Removing the
scripting escape hatch applies to EVERY arm identically - it is a task
condition, not a baseline handicap - and the footprint suite keeps the
scripted regime, so both worlds stay published.

What changes, symmetrically:
- bash and write_file leave every stage's tool set;
- the structured agent loses its `script` stage whole (a scripting
  stage without a shell would be a strawman), and the analyze stage's
  transition to it disappears with the stage;
- the prompt passages that mandate scripting are replaced with
  read-only equivalents - in both arms, from one substitution table,
  because telling a shell-less agent to use grep would also be a
  strawman;
- read_file/read_files get a per-tool result cap of 16000 tokens in
  the read stages, sized to the corpora's 60KB max-file guarantee, so
  a whole rotated log is one readable result in every arm;
- the flat arms' iteration budget is re-derived as the sum of the
  readonly structured stages, keeping the pair invariant.

check_pairs.py asserts all of it. Run AFTER make_flat.py and
make_mix.py:
    python3 make_readonly.py
"""
from __future__ import annotations

import re
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent

READONLY_STRUCTURED = "loganalyzer-bench-adversarial-scoped-flagship"
READONLY_FLATS = ["flat-loganalyzer", "flat-loganalyzer-compacting",
                  "flat-loganalyzer-hardened",
                  "flat-loganalyzer-compacting-hardened"]
READONLY = [READONLY_STRUCTURED] + READONLY_FLATS

DROPPED_TOOLS = ("bash", "write_file", "edit_file")
READ_CAP = 16000  # tokens; corpora assert files stay under 60KB

# Exact scripted-workflow passages and their read-only replacements.
# Exact-match with a required count, so a reworded source breaks the
# build loudly instead of shipping a prompt that tells a shell-less
# agent to reach for grep.
SUBS_STRUCTURED = [
    ("""Use bash to sample rather than reading whole files into context - the first N
lines, a line count, a file type probe. Reach for whatever your shell actually
provides (`head`/`wc`/`file` on Unix, `Get-Content -TotalCount` and
`Measure-Object` on Windows). The later stages compute over the file on disk with
scripts; pulling the whole log into context buys nothing and costs a lot. Write a""",
     """Work from file reads alone: list the directories first, then read files
selectively - newest and oldest rotations, and whatever the reference
documents point at. Long results are truncated at a fixed size, so pull the
essentials into your notes as you read instead of planning to re-read. Write a"""),
    ("""Keep a running tally in `severity_index`
(context_write), e.g. "critical: 2, warning: 5, info: 3". For precise
parsing/filtering/aggregation, write small scripts via bash (awk/grep/sed or
python on Unix, PowerShell or python on Windows) - never eyeball a count you
can compute. Test each script before building on its output.""",
     """Keep a running tally in `severity_index`
(context_write), e.g. "critical: 2, warning: 5, info: 3". When a count matters,
count it from the file text you actually read and cite the file and time range
it came from."""),
    # verify's re-computation option needs the shell; reads remain.
    ("""re-open the
cited source (read_file, or recompute with a bash one-liner) and confirm the
value character for character.""",
     """re-open the
cited source (read_file) and confirm the value character for
character."""),
    ('description = "Analyzes log files - identifies anomalies, trends, '
     'and error patterns, fact-checks its own report against the sources '
     'before delivering, maintaining a severity-ranked findings index"',
     'description = "Analyzes log files by reading them - identifies '
     'anomalies, trends, and error patterns, fact-checks its own report '
     'against the sources before delivering (read-only condition)"'),
]

SUBS_FLAT = [
    ("""Identify the log format first, then compute your answer with scripts
(grep/awk/python via bash) rather than eyeballing - write small
commands, check their output, and build up to the result. Compute over
the file on disk; pulling the whole log into context buys nothing and
costs a lot. Quantify everything: counts, timestamps, rates.
Double-check the final number by recomputing it a second way when
feasible.""",
     """Identify the log format first, then work from file reads alone: list
the directories, read files selectively - newest and oldest rotations,
and whatever the reference documents point at - and pull the essentials
into a running record as you read, since long results are truncated at
a fixed size and planning to re-read wastes the window. Quantify
everything: counts, timestamps, rates, counted from the file text you
actually read, citing the file and time range."""),
]

_STAGE = re.compile(r"^\[stages\.([A-Za-z0-9_]+)[\].]")
_TOOLS = re.compile(r"^(available_tools = \[)(.*)(\]\s*)$")


def _strip_tools(inner: str) -> str:
    kept = [t for t in re.findall(r'"([^"]+)"', inner)
            if t not in DROPPED_TOOLS]
    return ", ".join(f'"{t}"' for t in kept)


def _apply_subs(text: str, subs: list[tuple[str, str]],
                label: str) -> str:
    for old, new in subs:
        n = text.count(old)
        if n != 1:
            raise SystemExit(f"{label}: substitution source appears "
                             f"{n} times (want 1): {old[:60]!r}...")
        text = text.replace(old, new)
    return text


def _drop_sections(text: str, prefixes: tuple[str, ...]) -> str:
    """Remove whole [stages.*] sections whose header starts with any
    prefix, up to the next top-level [stages.*] or [context...] header."""
    out, skipping = [], False
    for line in text.splitlines(keepends=True):
        if line.startswith("[") and not line.startswith("[["):
            skipping = any(line.startswith(p) for p in prefixes)
        if not skipping:
            out.append(line)
    return "".join(out)


def render(source: str, subs: list[tuple[str, str]],
           structured: bool) -> str:
    text = (HERE / source / "agent.leviath").read_text()
    text = _apply_subs(text, subs, source)
    if structured:
        text = _drop_sections(
            text,
            ("[stages.script]", "[stages.script.",
             "[stages.analyze.transitions.script]",
             "[stages.analyze.transitions.script.",
             "[stages.analysis_review.transitions.script]",
             "[stages.analysis_review.transitions.script."))

    out: list[str] = []
    in_overrides_of: str | None = None
    capped: set[str] = set()

    def cap_lines() -> list[str]:
        return [f'read_file = {{ max_result_tokens = {READ_CAP} }}\n',
                f'read_files = {{ max_result_tokens = {READ_CAP} }}\n']

    for line in text.splitlines(keepends=True):
        m = _STAGE.match(line)
        if line.startswith("[") and in_overrides_of:
            in_overrides_of = None
        if m and line.rstrip().endswith(".tool_routing.overrides]"):
            in_overrides_of = m.group(1)
        t = _TOOLS.match(line)
        if t:
            line = f"{t.group(1)}{_strip_tools(t.group(2))}{t.group(3)}"
        stripped = line.split("=")[0].strip()
        if in_overrides_of and stripped in DROPPED_TOOLS:
            continue  # override for a tool that no longer exists
        if in_overrides_of and stripped == "read_file":
            region = re.search(r'"([^"]+)"', line)
            reg = f'region = "{region.group(1)}", ' if region else ""
            line = (f"read_file = {{ {reg}"
                    f"max_result_tokens = {READ_CAP} }}\n")
            capped.add(in_overrides_of)
        out.append(line)

    text = "".join(out)
    # Stages that read but had no overrides section (the flat work
    # stage) get one carrying just the caps.
    doc = tomllib.loads(text)
    for sname, stage in doc["stages"].items():
        tools = stage.get("available_tools", [])
        if "read_file" not in tools or sname in capped:
            continue
        header = f"[stages.{sname}.tool_routing.overrides]\n"
        if header in text:
            text = text.replace(header, header + "".join(cap_lines()), 1)
        else:
            anchor = f"[stages.{sname}.tool_routing]\n"
            if anchor in text:
                block = text.split(anchor, 1)[1]
                insert_at = len(anchor) + _section_len(block)
                idx = text.index(anchor)
                text = (text[:idx + insert_at]
                        + header + "".join(cap_lines()) + "\n"
                        + text[idx + insert_at:])
            else:
                # A stage with no routing at all (report): appended
                # sections at EOF are still that stage's tables.
                text = (text.rstrip("\n") + "\n\n" + anchor
                        + header + "".join(cap_lines()))
    return text


def _section_len(after_header: str) -> int:
    """Byte length of a section body: up to the next [ header."""
    n = 0
    for line in after_header.splitlines(keepends=True):
        if line.startswith("["):
            break
        n += len(line)
    return n


def main() -> int:
    structured_text = render(READONLY_STRUCTURED, SUBS_STRUCTURED,
                             structured=True)
    docs = {READONLY_STRUCTURED: tomllib.loads(structured_text)}
    budget = sum(int(s.get("max_iterations", 10))
                 for s in docs[READONLY_STRUCTURED]["stages"].values())
    outputs = {READONLY_STRUCTURED: structured_text}

    for flat in READONLY_FLATS:
        text = render(flat, SUBS_FLAT, structured=False)
        doc = tomllib.loads(text)
        old_budget = doc["stages"]["work"]["max_iterations"]
        text = text.replace(f"max_iterations = {old_budget}",
                            f"max_iterations = {budget}", 1)
        outputs[flat] = text

    for source, text in outputs.items():
        doc = tomllib.loads(text)  # must parse before landing
        low = "\n".join(line for line in text.splitlines()
                        if not line.lstrip().startswith("#")).lower()
        for tool in DROPPED_TOOLS:
            if f'"{tool}"' in low:
                raise SystemExit(f"{source}-readonly: {tool} survived")
        if source == READONLY_STRUCTURED and "script" in doc["stages"]:
            raise SystemExit("script stage survived the surgery")
        header = (f"# Read-only counterpart of {source} - GENERATED by "
                  "make_readonly.py for the\n# hallucination suite's "
                  "log tasks; do not edit by hand. No shell, no "
                  "writes,\n# scripted-workflow prompt passages "
                  "replaced, read results capped per tool.\n")
        out_dir = HERE / f"{source}-readonly"
        out_dir.mkdir(exist_ok=True)
        (out_dir / "agent.leviath").write_text(header + text)
        n = len(doc["stages"])
        print(f"{source}-readonly: {n} stages, budget "
              f"{sum(int(s.get('max_iterations', 10)) for s in doc['stages'].values())}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
