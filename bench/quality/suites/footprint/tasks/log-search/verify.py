"""Functional verification for log-search: the four incident facts.

The generator's answers.json carries nine lines (the corpus is shared
with the retention suite's fuller report); this task asks for the first
four - root service, config key, T0, propagation chain. Functional bar:
at least 3 of 4 exactly right. The chain line gets partial credit when
the root and terminal services are right but an intermediate hop is
missing - finding the wrong ROOT is a fail, missing one echo of the
cascade is the kind of imperfection this suite tolerates.
"""
from __future__ import annotations

import json
from pathlib import Path

FUNCTIONAL_BAR = 3.0  # of 4


def verify(task_dir: Path, workdir: Path, artifacts_dir: Path,
           answer) -> dict:
    key = json.loads((task_dir / "answers.json").read_text())["answers"]
    expected = [str(a).strip() for a in key[:4]]
    got = [line.strip() for line in (str(answer or "")).splitlines()
           if line.strip()][:4]
    got += [""] * (4 - len(got))

    scores = []
    detail = {}
    for i, (e, g) in enumerate(zip(expected, got), 1):
        if i < 4:
            score = 1.0 if g == e else 0.0
        else:
            if g == e:
                score = 1.0
            else:
                e_parts, g_parts = e.split(","), g.split(",")
                score = 0.5 if (g_parts and e_parts
                                and g_parts[0] == e_parts[0]
                                and g_parts[-1] == e_parts[-1]) else 0.0
        scores.append(score)
        detail[f"line_{i}"] = {"expected": e, "got": g, "score": score}

    total = sum(scores)
    return {
        "functional_pass": total >= FUNCTIONAL_BAR,
        "score": round(total / 4, 4),
        "detail": {"lines": detail, "points": total, "of": 4},
    }
