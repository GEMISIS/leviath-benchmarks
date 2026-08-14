"""Probe-answer grading for the Context Retention Suite.

The grading prompt is the July harness's (suites/crs/recovered/
evaluator-main.rs), verbatim: a 4-point taxonomy including a
hallucinated rung. Two things changed around it, both documented in
CRS-METHODOLOGY.md:

- the retention CURVE uses accuracy in {0, 0.5, 1}; `hallucinated` is
  carried as a flag and published as a rate, never as -0.5 in a mean;
- probes may declare an ``exact`` string; when the reader's answer
  contains it (case/whitespace-insensitive), the probe is graded
  correct deterministically and no model is consulted. Recovered probes
  have no ``exact`` field and always go to the grader.

The grader model is frozen in arms.json's ``probes`` block and must be
a different vendor from the reader model. Every grader request and
response is retained beside the probe replay for publication.
"""
from __future__ import annotations

import hashlib
import json
import re

from . import providers

__all__ = ["GRADE_PROMPT", "grade_prompt_sha256", "grade_answer"]

GRADE_PROMPT = """You are grading an agent's response to a probe question during a benchmark test.

**Probe Question:** {question}

**Expected Answer:** {expected}

**Grading Rubric:** {rubric}

**Agent's Answer:** {answer}

Grade the agent's answer on this 4-point scale:
- **Correct (1.0)**: Accurate and references the right information
- **Partially Correct (0.5)**: Right direction but missing details
- **Wrong (0.0)**: Confident but incorrect
- **Hallucinated (-0.5)**: Invented information not present in the original context

Respond with a JSON object in this exact format:
{{
  "grade": "correct" | "partial" | "wrong" | "hallucinated",
  "score": 1.0 | 0.5 | 0.0 | -0.5,
  "reasoning": "Brief explanation of your grade"
}}

Be strict but fair. The agent should demonstrate factual recall, not just plausible guesses."""

_GRADE_SCORES = {"correct": 1.0, "partial": 0.5, "wrong": 0.0,
                 "hallucinated": -0.5}


def grade_prompt_sha256() -> str:
    return hashlib.sha256(GRADE_PROMPT.encode()).hexdigest()


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def _extract_json(text: str) -> dict:
    """The fenced-JSON extraction the Rust evaluator used, ported."""
    fenced = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.S)
    candidate = fenced.group(1) if fenced else None
    if candidate is None:
        brace = re.search(r"\{.*\}", text, re.S)
        candidate = brace.group(0) if brace else None
    if candidate is None:
        raise ValueError(f"no JSON object in grader reply: {text[:200]!r}")
    return json.loads(candidate)


def grade_answer(probe: dict, answer: str, *, grader_model_id: str,
                 keys: dict, transport=None) -> dict:
    """Grade one probe answer.

    Returns {"score": float in {0, 0.5, 1}, "grade": str,
    "hallucinated": bool, "reasoning": str, "method":
    "exact"|"model"|"grading_error", "usage": {...}, "transcript": ...}.
    """
    exact = probe.get("exact")
    if exact and _norm(exact) in _norm(answer or ""):
        return {"score": 1.0, "grade": "correct", "hallucinated": False,
                "reasoning": f"deterministic: answer contains {exact!r}",
                "method": "exact", "usage": {}, "transcript": None}

    prompt = GRADE_PROMPT.format(question=probe["question"],
                                 expected=probe["expected"],
                                 rubric=probe["rubric"],
                                 answer=answer or "(no answer)")
    usage_total = {"prompt_tokens": 0, "completion_tokens": 0,
                   "cached_tokens": 0, "cache_write_tokens": 0}
    transcript = []
    last_error = None
    for _ in range(2):  # one re-ask on an inconsistent verdict
        # Reasoning graders spend output tokens thinking before the
        # JSON verdict; 512 starves them into a provider 400.
        out = providers.call_chat(
            grader_model_id, [], [{"role": "user", "content": [
                {"type": "text", "text": prompt}]}], [],
            temperature=0, max_tokens=4096, keys=keys,
            transport=transport)
        for k in usage_total:
            usage_total[k] += out["usage"].get(k, 0)
        transcript.append({"prompt": prompt, "reply": out["text"]})
        try:
            verdict = _extract_json(out["text"])
            grade = str(verdict.get("grade", "")).lower()
            score = verdict.get("score")
            if grade not in _GRADE_SCORES:
                raise ValueError(f"unknown grade {grade!r}")
            if score is not None and float(score) != _GRADE_SCORES[grade]:
                raise ValueError(
                    f"grade {grade!r} disagrees with score {score!r}")
            return {
                # Curve scale: hallucinated counts as 0 accuracy; the
                # -0.5 taxonomy survives in `grade` and the flag.
                "score": max(_GRADE_SCORES[grade], 0.0),
                "grade": grade,
                "hallucinated": grade == "hallucinated",
                "reasoning": str(verdict.get("reasoning", ""))[:1000],
                "method": "model",
                "usage": usage_total,
                "transcript": transcript,
            }
        except (ValueError, json.JSONDecodeError) as exc:
            last_error = exc
            continue
    # Recorded as a grading error, never a silent zero-that-looks-real.
    return {"score": None, "grade": "grading_error",
            "hallucinated": False,
            "reasoning": f"grader output unusable: {last_error}",
            "method": "grading_error", "usage": usage_total,
            "transcript": transcript}
