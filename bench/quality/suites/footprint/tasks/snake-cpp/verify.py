"""Functional verification for snake-cpp: compile, then four scenarios.

Compilation is a gate, not a point. The four scored scenarios drive the
binary's --test mode:

  1. movement    - a safe path; HEAD/TICKS/STATUS must match a reference
                   simulation of the spec's movement rules, and the
                   LENGTH == 3 + SCORE invariant must hold.
  2. wall        - march straight into the right wall; STATUS DEAD_WALL
                   with TICKS no greater than the move count.
  3. no-reverse  - opposite-direction inputs must be ignored; checked the
                   same way as movement. This scenario replaces a direct
                   self-collision probe: with the no-reverse rule a snake
                   cannot hit itself until it has grown, and growth
                   depends on seed-driven food placement the spec leaves
                   to the implementation, so no move string guarantees
                   DEAD_SELF. The reversal rule is the half of the
                   self-collision machinery that IS seed-independent.
  4. determinism - the same seed and moves twice must produce
                   byte-identical stdout.

Food positions are seed-dependent by design, so the reference simulator
ignores food entirely; scenario paths are chosen so that no growth can
change HEAD, TICKS, or STATUS (the head never re-enters a previously
occupied cell). score = points/4; functional_pass = compiled and
points >= 3.
"""
from __future__ import annotations

import re
import subprocess
from pathlib import Path

GRID_W, GRID_H = 20, 15
START = [(10, 7), (9, 7), (8, 7)]  # head first, moving right
DIRS = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)}

COMPILE_TIMEOUT = 120
RUN_TIMEOUT = 10
FUNCTIONAL_BAR = 3  # of 4 points


def _sweep_moves() -> str:
    """A lawnmower sweep covering nearly the whole grid.

    Used only by the determinism scenario, where the outcome is never
    predicted - two runs must merely match byte for byte. Sweeping most
    cells means the snake almost certainly crosses food wherever the
    implementation places it, so nondeterministic placement (e.g. a
    random_device seed) shows up as differing SCORE/LENGTH or a
    different death.
    """
    moves = "U" * 7 + "L" * 10  # climb to (10,0), slide to (0,0)
    for row in range(1, GRID_H):
        moves += "D" + ("R" if row % 2 else "L") * (GRID_W - 1)
    return moves


def _simulate(moves: str) -> dict:
    """Reference simulation of the spec's movement rules, food ignored.

    Only valid for move strings whose head path never revisits an
    occupied cell (then growth cannot alter head, ticks, or status).
    """
    snake = list(START)
    dx, dy = 1, 0
    ticks = 0
    status = "ALIVE"
    for ch in moves:
        ndx, ndy = DIRS[ch]
        if (ndx, ndy) != (-dx, -dy):
            dx, dy = ndx, ndy
        hx, hy = snake[0][0] + dx, snake[0][1] + dy
        ticks += 1
        if not (0 <= hx < GRID_W and 0 <= hy < GRID_H):
            status = "DEAD_WALL"
            break
        snake.pop()  # tail moves first (no growth in the reference)
        if (hx, hy) in snake:
            status = "DEAD_SELF"
            snake.insert(0, (hx, hy))
            break
        snake.insert(0, (hx, hy))
    return {"ticks": ticks, "head": snake[0], "status": status}


def _parse(stdout: str) -> dict | None:
    """Tolerantly pull the five report fields from anywhere in stdout."""
    patterns = {
        "ticks": r"^\s*TICKS\s+(-?\d+)\s*$",
        "length": r"^\s*LENGTH\s+(-?\d+)\s*$",
        "score": r"^\s*SCORE\s+(-?\d+)\s*$",
        "head": r"^\s*HEAD\s+(-?\d+)\s+(-?\d+)\s*$",
        "status": r"^\s*STATUS\s+(ALIVE|DEAD_WALL|DEAD_SELF)\s*$",
    }
    out = {}
    for key, pat in patterns.items():
        m = re.search(pat, stdout, re.MULTILINE)
        if not m:
            return None
        if key == "head":
            out[key] = (int(m.group(1)), int(m.group(2)))
        elif key == "status":
            out[key] = m.group(1)
        else:
            out[key] = int(m.group(1))
    return out


def _run(binary: Path, seed: int, moves: str,
         artifacts_dir: Path, label: str) -> tuple[str | None, str]:
    """Run one --test invocation; returns (stdout or None, note)."""
    cmd = [str(binary), "--test", "--seed", str(seed), "--moves", moves]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        (artifacts_dir / f"scenario-{label}.txt").write_text(
            f"TIMEOUT after {RUN_TIMEOUT}s: {' '.join(cmd)}\n")
        return None, f"timed out after {RUN_TIMEOUT}s"
    except OSError as exc:
        (artifacts_dir / f"scenario-{label}.txt").write_text(
            f"FAILED TO RUN: {exc}\n")
        return None, f"failed to run: {exc}"
    (artifacts_dir / f"scenario-{label}.txt").write_text(
        proc.stdout + (f"\n--- stderr ---\n{proc.stderr}"
                       if proc.stderr else ""))
    note = "ok" if proc.returncode == 0 else f"exit code {proc.returncode}"
    return proc.stdout, note


def _check_movement(binary: Path, artifacts_dir: Path,
                    seed: int, moves: str, label: str) -> dict:
    expected = _simulate(moves)
    stdout, note = _run(binary, seed, moves, artifacts_dir, label)
    detail = {"seed": seed, "moves": moves, "run": note,
              "expected": {"head": list(expected["head"]),
                           "ticks": expected["ticks"],
                           "status": expected["status"]}}
    if stdout is None:
        detail["pass"] = False
        return detail
    parsed = _parse(stdout)
    if parsed is None:
        detail["pass"] = False
        detail["error"] = "report lines not found"
        return detail
    detail["got"] = {"head": list(parsed["head"]), "ticks": parsed["ticks"],
                     "status": parsed["status"], "length": parsed["length"],
                     "score": parsed["score"]}
    ok = (parsed["head"] == expected["head"]
          and parsed["ticks"] == expected["ticks"]
          and parsed["status"] == expected["status"]
          and parsed["length"] == 3 + parsed["score"])
    detail["pass"] = ok
    return detail


def _check_wall(binary: Path, artifacts_dir: Path,
                seed: int, moves: str, label: str) -> dict:
    expected = _simulate(moves)
    stdout, note = _run(binary, seed, moves, artifacts_dir, label)
    detail = {"seed": seed, "moves": moves, "run": note,
              "expected": {"status": "DEAD_WALL",
                           "ticks_at_most": len(moves),
                           "reference_ticks": expected["ticks"]}}
    if stdout is None:
        detail["pass"] = False
        return detail
    parsed = _parse(stdout)
    if parsed is None:
        detail["pass"] = False
        detail["error"] = "report lines not found"
        return detail
    detail["got"] = {"status": parsed["status"], "ticks": parsed["ticks"]}
    detail["pass"] = (parsed["status"] == "DEAD_WALL"
                      and 1 <= parsed["ticks"] <= len(moves))
    return detail


def _check_determinism(binary: Path, artifacts_dir: Path,
                       seed: int, moves: str, label: str) -> dict:
    out_a, note_a = _run(binary, seed, moves, artifacts_dir, f"{label}-a")
    out_b, note_b = _run(binary, seed, moves, artifacts_dir, f"{label}-b")
    detail = {"seed": seed, "moves": moves,
              "run": f"first {note_a}; second {note_b}"}
    if out_a is None or out_b is None:
        detail["pass"] = False
        return detail
    parsed = _parse(out_a)
    detail["identical"] = out_a == out_b
    detail["report_found"] = parsed is not None
    detail["pass"] = detail["identical"] and detail["report_found"]
    return detail


def verify(task_dir: Path, workdir: Path, artifacts_dir: Path,
           answer) -> dict:
    workdir = Path(workdir)
    artifacts_dir = Path(artifacts_dir)
    artifacts_dir.mkdir(parents=True, exist_ok=True)

    source = None
    for candidate in (workdir / "snake.cpp", workdir / "src" / "snake.cpp"):
        if candidate.is_file():
            source = candidate
            break
    if source is None:
        return {"functional_pass": False, "score": 0.0,
                "detail": {"error": "snake.cpp not found (looked at top "
                                    "level and in src/)"}}

    binary = artifacts_dir / "snake"
    cmd = ["c++", "-std=c++17", "-O2", "-o", str(binary), str(source)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True,
                              timeout=COMPILE_TIMEOUT)
        compile_log = (f"$ {' '.join(cmd)}\nexit {proc.returncode}\n"
                       f"{proc.stdout}{proc.stderr}")
        compiled = proc.returncode == 0
    except (subprocess.TimeoutExpired, OSError) as exc:
        compile_log = f"$ {' '.join(cmd)}\nfailed: {exc}\n"
        compiled = False
    (artifacts_dir / "compile.txt").write_text(compile_log)
    if not compiled:
        return {"functional_pass": False, "score": 0.0,
                "detail": {"error": "snake.cpp did not compile",
                           "source": str(source),
                           "compile_log": "compile.txt"}}

    scenarios = {
        "movement": _check_movement(binary, artifacts_dir,
                                    seed=7, moves="UULL", label="movement"),
        "wall": _check_wall(binary, artifacts_dir,
                            seed=3, moves="RRRRRRRRRRRR", label="wall"),
        "no_reverse": _check_movement(binary, artifacts_dir,
                                      seed=11, moves="LLDD",
                                      label="no-reverse"),
        "determinism": _check_determinism(binary, artifacts_dir,
                                          seed=42, moves=_sweep_moves(),
                                          label="determinism"),
    }
    points = sum(1 for s in scenarios.values() if s["pass"])
    return {
        "functional_pass": points >= FUNCTIONAL_BAR,
        "score": round(points / 4, 4),
        "detail": {"source": str(source), "compiled": True,
                   "points": points, "of": 4, "scenarios": scenarios},
    }
