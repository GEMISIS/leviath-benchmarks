# Task: Architecture Briefing

A senior engineer is joining this project next week. Your job is to
write the document that gets them productive: an explanation of the
repository's architecture, written for someone who reads code fluently
but has never seen this codebase.

The repository is checked out under `repo/` in this directory. It is a
Rust workspace. Everything you need is in the checkout - no web access
is needed or expected.

## What the document must cover

- **The crates/modules and what each owns.** Walk the workspace
  members: what each crate is responsible for, and what it deliberately
  is not responsible for.
- **How a request/run flows through the system end to end.** From the
  user-facing entry point down through the layers and back out: which
  crate handles each stage, and where the handoffs are.
- **The key abstractions and where they live.** The handful of types,
  traits, and modules a newcomer must understand first, each with the
  file path where it is defined.
- **How the pieces communicate.** Crate-to-crate dependencies, process
  boundaries, sockets/IPC, wire formats - whatever the code actually
  uses.

## Ground rules

- **Ground every claim in the actual code.** Every file path, crate
  name, and symbol you mention must exist in the checkout under
  `repo/`. Cite real paths (e.g. a real `crates/<name>/src/<file>.rs`)
  rather than describing from memory or from what similar projects
  usually do. A document that cites files or symbols that do not exist
  is worse than a shorter document that cites only real ones.
- Read the code to find out what is true; do not guess from names
  alone.

## Deliverable

Write the document to `ARCHITECTURE-EXPLAINED.md` in the working
directory (next to `repo/`, not inside it):

- Markdown, 500-1500 words.
- Use backticks around every file path, crate name, and code symbol.
- Structure it however serves the reader; headings and a short
  flow walkthrough are usually the right shape.
