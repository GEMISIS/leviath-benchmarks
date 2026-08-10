"""Deterministic grading for log-analysis answers.

Public tasks carry a plaintext answer; held-out tasks carry
sha256(salt + normalized answer). Normalization is minimal on purpose
(trim, casefold, collapse a leading answer label) so the agent is graded
on the number it produced, not its prose.
"""
from __future__ import annotations

import hashlib
import re

__all__ = ["normalize", "check"]

_LABEL = re.compile(r"^(final answer|answer)\s*[:=-]\s*", re.IGNORECASE)


def normalize(text: str) -> str:
    text = _LABEL.sub("", str(text).strip())
    text = text.strip().strip(".").strip()
    # Keep only the last line, so "Explanation...\n42" grades on 42.
    if "\n" in text:
        text = text.splitlines()[-1].strip()
        text = _LABEL.sub("", text).strip().strip(".").strip()
    # Integers written with separators still count: "1,204" == "1204".
    compact = text.replace(",", "").replace(" ", "")
    if re.fullmatch(r"-?\d+", compact):
        return compact
    return text.casefold()


def check(task: dict, answer: str, salt: str | None = None) -> dict:
    got = normalize(answer)
    if "answer" in task:
        expected = normalize(task["answer"])
        return {"passed": got == expected,
                "detail": {"expected": expected, "got": got}}
    if "answer_sha256" in task:
        if not salt:
            raise ValueError("held-out grading requires the salt (its "
                             "scheme is committed in "
                             "heldout_answers.sha256)")
        digest = hashlib.sha256((salt + got).encode()).hexdigest()
        return {"passed": digest == task["answer_sha256"],
                "detail": {"got": got}}
    raise ValueError(f"task {task.get('id')} has no answer field")
