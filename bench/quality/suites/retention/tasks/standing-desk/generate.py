#!/usr/bin/env python3
"""Generate the standing-desk corpus (retention suite).

A twelve-phase event-operations session: the agent runs the ops desk
for a fictional conference, the scripted user serves one request after
another, and LATER requests silently depend on results the agent
DERIVED in earlier phases (which caterer it shortlisted, what budget
remainder it computed). The reference files alone do not answer the
dependent phases without redoing the earlier work - retention of the
agent's own conclusions is exactly what the task prices.

Two hard constraints shape this file, same as the sibling suites:

- Determinism: the corpus is a pure function of --seed. Same seed,
  byte-identical bytes (--check verifies against the committed copy).
  Feasibility constraints (a venue big enough exists, five keynotes
  fit the budget, the schedule places) are met by deterministic
  salted redraw (random.Random(f"{seed}:{attempt}")), never by
  wall-clock or ambient state. All money is integer cents.
- The self-test is a symbolic perfect agent: it re-parses the EMITTED
  bytes and walks all twelve phases in order, computing each phase's
  deliverable from the corpus plus the prior phases' results, and the
  answer key must match line for line. A corpus that cannot support
  its own key is never written.

Usage:
    python3 generate.py [--seed N] [--out DIR] [--check]
"""
from __future__ import annotations

import argparse
import json
import random
import sys
import tempfile
from pathlib import Path

DEFAULT_SEED = 7451
MAX_FILE_BYTES = 60_000
MAX_ATTEMPTS = 200

# The five dietary requirements every catering partner must cover
# (fixed - constraints.md quotes them, and the phase-2 rule needs a
# stable universe).
DIETS = ["vegetarian", "vegan", "gluten-free", "kosher", "halal"]
EVENT_DAYS = 3  # Sep 14-16, 2026: days 1..3

FIRST = ["Ada", "Bruno", "Carmen", "Deepak", "Elif", "Farid", "Greta",
         "Hiro", "Ines", "Jonas", "Keiko", "Lars", "Mireille", "Nadia",
         "Omar", "Priya", "Quentin", "Rosa", "Sven", "Tamar", "Umut",
         "Vera", "Wendell", "Xiomara", "Yusuf", "Zofia"]
LAST = ["Abbasi", "Bergstrom", "Castellanos", "Dimitrov", "Eriksen",
        "Fontaine", "Grigoryan", "Hashimoto", "Iyer", "Jankowski",
        "Kovacs", "Lindqvist", "Moreau", "Nakamura", "Okonkwo",
        "Petrov", "Quispe", "Rasmussen", "Sorensen", "Tanaka",
        "Ustinov", "Vasquez", "Wieland", "Xu", "Yamada", "Zielinski"]


def money(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"


def parse_money(text: str) -> int:
    text = text.strip().replace(",", "")
    sign = -1 if text.startswith("-") else 1
    text = text.lstrip("-").lstrip("$")
    whole, _, frac = text.partition(".")
    return sign * (int(whole) * 100 + int((frac + "00")[:2]))


def ceil_div(a: int, b: int) -> int:
    return -(-a // b)


class Redraw(Exception):
    """This attempt cannot satisfy a feasibility constraint."""


# ---------------------------------------------------------------------
# Fixed reference documents (seed-independent).
# ---------------------------------------------------------------------

CONSTRAINTS_MD = """\
# Meridian Summit 2026 - Standing Constraints (rev 4)

- Event dates: 2026-09-14 through 2026-09-16 (three days; referred to
  as day 1, day 2 and day 3 throughout the planning files).
- Dietary requirements the event MUST cover, per the attendee survey:
  vegetarian, vegan, gluten-free, kosher, halal. A catering partner
  that cannot cover all five is not eligible, whatever it costs.
- Every dollar figure in the planning files is USD with two decimal
  places. Deliverables must report money the same way.
- Registration status meanings: `confirmed` counts toward attendance;
  `waitlist` and `cancelled` do not.
- A registration's dietary value of `none` means no accommodation is
  required; anything else counts toward the dietary-accommodation
  tally.
"""

POLICIES_MD = """\
# Events Desk Working Policies (rev 9)

1. Work from the reference files in this workspace; do not assume
   figures from past events.
2. Report every deliverable in exactly the format the request gives.
   A correct figure in the wrong shape cannot be booked by the desk.
3. When a request references an earlier decision ("the caterer you
   shortlisted", "the remainder you computed"), it means YOUR earlier
   result from this session, not a fresh reading of the files.
4. Round only where a request says to round; otherwise keep exact
   cents.
5. After writing each phase deliverable, ask the desk for the next
   assignment. Do not invent follow-on work.
"""

PAST_EVENTS_MD = """\
# Prior Summits - Desk Notes (background only)

2024: 2,100 attendees, single-track, venue feedback poor (two rooms
short). 2025: 3,400 attendees, catering complaints traced to a partner
that quietly dropped kosher coverage after contracting; the desk now
requires full dietary coverage before shortlisting. Both years the
transport plan was improvised late - shuttles this year are to be
planned as soon as hotel blocks are chosen.

None of the figures in this file are current. Use the 2026 reference
files for all numbers.
"""


# ---------------------------------------------------------------------
# Corpus construction
# ---------------------------------------------------------------------


def _name(rng: random.Random) -> str:
    return f"{rng.choice(FIRST)} {rng.choice(LAST)}"


def _build_once(rng: random.Random) -> dict[str, str]:
    """Emit one candidate corpus (relative path -> text)."""
    corpus: dict[str, str] = {
        "reference/constraints.md": CONSTRAINTS_MD,
        "reference/policies.md": POLICIES_MD,
        "reference/past-events.md": PAST_EVENTS_MD,
    }

    # --- registrations (the bulk of the corpus) ---------------------
    reg_rows_by_file: list[list[str]] = []
    reg_id = 10000
    for _ in range(8):
        rows = []
        for _ in range(rng.randrange(1150, 1250)):
            reg_id += 1
            roll = rng.random()
            status = ("confirmed" if roll < 0.66
                      else "waitlist" if roll < 0.85 else "cancelled")
            diet = ("none" if rng.random() < 0.70
                    else rng.choice(DIETS))
            rows.append(f"REG-{reg_id},{_name(rng)},{status},{diet}")
        reg_rows_by_file.append(rows)
    for i, rows in enumerate(reg_rows_by_file, 1):
        corpus[f"registrations/batch-{i}.csv"] = \
            "id,name,status,dietary\n" + "\n".join(rows) + "\n"

    # Late additions: the phase-9 headcount delta. Kept in reference/
    # so phase 1 (which the packs scope to registrations/) is stable.
    late_rows = []
    for _ in range(rng.randrange(18, 42)):
        reg_id += 1
        status = "confirmed" if rng.random() < 0.8 else "waitlist"
        diet = "none" if rng.random() < 0.7 else rng.choice(DIETS)
        late_rows.append(f"REG-{reg_id},{_name(rng)},{status},{diet}")
    corpus["reference/late-additions.csv"] = \
        "id,name,status,dietary\n" + "\n".join(late_rows) + "\n"

    # --- venues ------------------------------------------------------
    venue_rows = []
    used_rates: set[int] = set()
    for i in range(1, 7):
        cap = rng.randrange(5200, 9801, 50)
        rooms = rng.randrange(10, 25)
        while True:
            rate = rng.randrange(600_000, 1_600_001, 2500)
            if rate not in used_rates:
                used_rates.add(rate)
                break
        venue_rows.append((f"VEN-{i}", cap, rooms, rate))
    corpus["reference/venues.md"] = (
        "# Venue Options (per-day rate, all-in)\n\n"
        "| code | capacity | rooms | daily_rate |\n|---|---|---|---|\n"
        + "\n".join(f"| {c} | {cap} | {rooms} | {money(rate)} |"
                    for c, cap, rooms, rate in venue_rows) + "\n")

    # --- caterers ----------------------------------------------------
    cat_rows = []
    n_full = rng.randrange(3, 5)  # full-coverage caterers
    full_idx = set(rng.sample(range(8), n_full))
    for i in range(8):
        code = f"CAT-{i + 1}"
        per_head = rng.randrange(5200, 8201)
        fee = rng.randrange(180_000, 420_001, 500)
        min_heads = rng.randrange(600, 5201, 100)
        if i in full_idx:
            cover = list(DIETS)
        else:
            cover = sorted(rng.sample(DIETS, rng.randrange(2, 5)))
        cat_rows.append((code, per_head, fee, min_heads, cover))
    corpus["reference/catering-quotes.md"] = (
        "# Catering Quotes 2026\n\n"
        "Effective per-head cost at a given headcount = per_head plus\n"
        "service_fee divided by headcount, rounded DOWN to the cent.\n\n"
        "| code | per_head | service_fee | min_heads | dietary_coverage |\n"
        "|---|---|---|---|---|\n"
        + "\n".join(
            f"| {c} | {money(ph)} | {money(fee)} | {mh} | "
            f"{';'.join(cov)} |"
            for c, ph, fee, mh, cov in cat_rows) + "\n")

    # --- speakers ----------------------------------------------------
    spk_rows = []
    for i in range(1, 121):
        rating = rng.randrange(300, 501)  # 3.00-5.00, two decimals
        fee = rng.randrange(520_000, 1_600_001, 2500)
        n_days = rng.randrange(0, 4)
        days = sorted(rng.sample([1, 2, 3], n_days)) if n_days else []
        spk_rows.append((f"SPK-{i:03d}", _name(rng), rating, fee, days))
    corpus["reference/speakers.csv"] = (
        "code,name,rating,fee,available_days\n"
        + "\n".join(
            f"{c},{n},{r // 100}.{r % 100:02d},{money(f)},"
            f"{';'.join(map(str, d))}"
            for c, n, r, f, d in spk_rows) + "\n")

    # --- AV vendors --------------------------------------------------
    av_rows = []
    used_tot: set[int] = set()
    for i in range(5):
        code = f"AV-{chr(65 + i)}"
        rooms_cov = rng.randrange(8, 31)
        while True:
            total = rng.randrange(800_000, 2_200_001, 2500)
            if total not in used_tot:
                used_tot.add(total)
                break
        av_rows.append((code, rooms_cov, total))
    corpus["reference/av-vendors.md"] = (
        "# AV Vendor Packages (event total, all three days)\n\n"
        "| vendor | rooms_covered | total |\n|---|---|---|\n"
        + "\n".join(f"| {c} | {rc} | {money(t)} |"
                    for c, rc, t in av_rows) + "\n")

    # --- hotels ------------------------------------------------------
    hot_rows = []
    used_dist: set[int] = set()
    for i in range(1, 7):
        while True:
            dist = rng.randrange(200, 4001, 10)
            if dist not in used_dist:
                used_dist.add(dist)
                break
        rate = rng.randrange(11_000, 26_001, 250)
        rooms = rng.randrange(400, 1801, 25)
        hot_rows.append((f"HTL-{i}", dist, rate, rooms))
    corpus["reference/hotels.md"] = (
        "# Hotel Blocks On Offer\n\n"
        "| code | distance_m | nightly_rate | rooms_available |\n"
        "|---|---|---|---|\n"
        + "\n".join(f"| {c} | {d} | {money(r)} | {rm} |"
                    for c, d, r, rm in hot_rows) + "\n")

    # --- transport ---------------------------------------------------
    seats = rng.randrange(28, 47)
    shuttle_daily = rng.randrange(28_000, 45_001, 500)
    corpus["reference/transport.md"] = (
        "# Shuttle Contractor Terms\n\n"
        f"- seats_per_shuttle: {seats}\n"
        f"- daily_cost_per_shuttle: {money(shuttle_daily)}\n"
        "- Shuttles are hired per hotel; a shuttle cannot serve two\n"
        "  hotels in one rotation.\n")

    # --- sponsors ----------------------------------------------------
    spn_rows = []
    for i in range(1, 56):
        tier = rng.choice(["gold", "silver", "silver", "bronze",
                           "bronze", "bronze"])
        commit = rng.randrange(200_000, 3_000_001, 5000)
        signed = "yes" if rng.random() < 0.6 else "no"
        spn_rows.append((f"SPN-{i:02d}", _name(rng) + " Group", tier,
                         commit, signed))
    corpus["reference/sponsors.csv"] = (
        "code,name,tier,commitment,signed\n"
        + "\n".join(f"{c},{n},{t},{money(cm)},{s}"
                    for c, n, t, cm, s in spn_rows) + "\n")

    # --- insurance ---------------------------------------------------
    tier_rows = []
    prem = rng.randrange(250_000, 400_001, 2500)
    cov = rng.randrange(24_000_000, 30_000_001, 50_000)
    for label in ("TIER-A", "TIER-B", "TIER-C", "TIER-D"):
        tier_rows.append((label, prem, cov))
        prem += rng.randrange(120_000, 260_001, 2500)
        cov += rng.randrange(10_000_000, 16_000_001, 50_000)
    corpus["reference/insurance.md"] = (
        "# Event Liability Policies\n\n"
        "| tier | premium | coverage |\n|---|---|---|\n"
        + "\n".join(f"| {t} | {money(p)} | {money(c)} |"
                    for t, p, c in tier_rows) + "\n")

    # --- budget ------------------------------------------------------
    speaker_budget = rng.randrange(5_500_000, 8_500_001, 25_000)
    total_budget = rng.randrange(78_000_000, 95_000_001, 100_000)
    corpus["reference/budget.md"] = (
        "# Meridian Summit 2026 - Budget Sheet\n\n"
        f"- total_budget: {money(total_budget)}\n"
        f"- speaker_budget: {money(speaker_budget)}\n"
        "- Amounts are event totals. The speaker budget is a carve-out\n"
        "  inside the total, not an addition to it.\n")

    return corpus


# ---------------------------------------------------------------------
# Parsing the emitted corpus (the only data source the walk sees).
# ---------------------------------------------------------------------


def _table_rows(text: str) -> list[list[str]]:
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if cells and set(cells[0]) <= {"-", " "}:
            continue  # separator row
        rows.append(cells)
    return rows[1:]  # drop header


def _kv_lines(text: str) -> dict[str, str]:
    out = {}
    for line in text.splitlines():
        line = line.strip().lstrip("- ")
        if ":" in line:
            k, _, v = line.partition(":")
            if " " not in k.strip():
                out[k.strip()] = v.strip()
    return out


def parse_corpus(corpus: dict[str, str]) -> dict:
    data: dict = {}

    regs = []
    for path in sorted(corpus):
        if path.startswith("registrations/"):
            for line in corpus[path].splitlines()[1:]:
                rid, name, status, diet = line.split(",")
                regs.append((rid, name, status, diet))
    data["registrations"] = regs

    late = []
    for line in corpus["reference/late-additions.csv"].splitlines()[1:]:
        rid, name, status, diet = line.split(",")
        late.append((rid, name, status, diet))
    data["late"] = late

    data["venues"] = [
        {"code": c, "capacity": int(cap), "rooms": int(rooms),
         "daily_rate": parse_money(rate)}
        for c, cap, rooms, rate in
        _table_rows(corpus["reference/venues.md"])]

    data["caterers"] = [
        {"code": c, "per_head": parse_money(ph),
         "service_fee": parse_money(fee), "min_heads": int(mh),
         "coverage": set(cov.split(";"))}
        for c, ph, fee, mh, cov in
        _table_rows(corpus["reference/catering-quotes.md"])]

    speakers = []
    for line in corpus["reference/speakers.csv"].splitlines()[1:]:
        code, name, rating, fee, days = line.split(",")
        speakers.append({
            "code": code, "name": name,
            "rating": int(rating.replace(".", "")),
            "fee": parse_money(fee),
            "days": [int(d) for d in days.split(";")] if days else []})
    data["speakers"] = speakers

    data["av"] = [
        {"vendor": c, "rooms_covered": int(rc), "total": parse_money(t)}
        for c, rc, t in _table_rows(corpus["reference/av-vendors.md"])]

    data["hotels"] = [
        {"code": c, "distance": int(d), "rate": parse_money(r),
         "rooms": int(rm)}
        for c, d, r, rm in _table_rows(corpus["reference/hotels.md"])]

    tr = _kv_lines(corpus["reference/transport.md"])
    data["seats"] = int(tr["seats_per_shuttle"])
    data["shuttle_daily"] = parse_money(tr["daily_cost_per_shuttle"])

    sponsors = []
    for line in corpus["reference/sponsors.csv"].splitlines()[1:]:
        code, name, tier, commit, signed = line.split(",")
        sponsors.append({"code": code, "tier": tier,
                         "commitment": parse_money(commit),
                         "signed": signed == "yes"})
    data["sponsors"] = sponsors

    data["tiers"] = [
        {"tier": t, "premium": parse_money(p), "coverage": parse_money(c)}
        for t, p, c in _table_rows(corpus["reference/insurance.md"])]

    bd = _kv_lines(corpus["reference/budget.md"])
    data["total_budget"] = parse_money(bd["total_budget"])
    data["speaker_budget"] = parse_money(bd["speaker_budget"])
    return data


# ---------------------------------------------------------------------
# The symbolic perfect agent: twelve phases, each a pure function of
# the parsed corpus plus the prior phases' results.
# ---------------------------------------------------------------------


def walk_phases(data: dict) -> tuple[dict, dict]:
    """Return (phases, registry). Raises Redraw on infeasibility."""
    phases: dict[str, dict] = {}
    alt: dict[str, dict[str, list[str]]] = {}

    # -- phase 1: attendance + venue ---------------------------------
    att = sum(1 for _, _, s, _ in data["registrations"]
              if s == "confirmed")
    diet = sum(1 for _, _, s, d in data["registrations"]
               if s == "confirmed" and d != "none")
    need = att + ceil_div(att, 10)
    fitting = [v for v in data["venues"] if v["capacity"] >= need]
    if not fitting:
        raise Redraw("no venue fits")
    venue = min(fitting, key=lambda v: v["daily_rate"])
    phases["01"] = {"lines": {
        "attendance": str(att), "dietary": str(diet),
        "venue": venue["code"],
        "venue_daily_rate": money(venue["daily_rate"])}}

    # -- phase 2: catering shortlist ---------------------------------
    qual = [c for c in data["caterers"]
            if c["coverage"] >= set(DIETS) and c["min_heads"] <= att]
    if len(qual) < 2:
        raise Redraw("fewer than two qualifying caterers")

    def eff(c: dict) -> int:
        return c["per_head"] + c["service_fee"] // att

    qual.sort(key=lambda c: (eff(c), c["min_heads"], c["code"]))
    if eff(qual[0]) == eff(qual[1]):
        raise Redraw("effective-cost tie in shortlist")
    c1, c2 = qual[0], qual[1]
    phases["02"] = {"lines": {
        "shortlist_1": f"{c1['code']} {money(eff(c1))}",
        "shortlist_2": f"{c2['code']} {money(eff(c2))}"}}
    alt["02"] = {"shortlist_1": [f"{c2['code']} {money(eff(c2))}"]}

    # -- phase 3: keynote selection ----------------------------------
    eligible = [s for s in data["speakers"] if s["days"]]
    eligible.sort(key=lambda s: (-s["rating"], s["name"]))
    picked, spent = [], 0
    for s in eligible:
        if len(picked) == 5:
            break
        if spent + s["fee"] <= data["speaker_budget"]:
            picked.append(s)
            spent += s["fee"]
    if len(picked) != 5:
        raise Redraw("keynote budget does not seat five")
    names = {s["name"] for s in picked}
    if len(names) != 5:
        raise Redraw("duplicate keynote names")
    phases["03"] = {"lines": {
        "keynotes": "; ".join(s["name"] for s in picked),
        "keynote_fees": money(spent)}}

    # -- phase 4: AV package -----------------------------------------
    covering = [a for a in data["av"]
                if a["rooms_covered"] >= venue["rooms"]]
    if not covering:
        raise Redraw("no AV package covers the venue")
    av = min(covering, key=lambda a: (a["total"], a["vendor"]))
    phases["04"] = {"lines": {
        "av_vendor": av["vendor"], "av_total": money(av["total"])}}
    # The stale twin: the AV pick for the SECOND-cheapest fitting venue
    # (the plausible wrong memory of phase 1's choice).
    fitting_sorted = sorted(fitting, key=lambda v: v["daily_rate"])
    if len(fitting_sorted) > 1:
        v2 = fitting_sorted[1]
        cov2 = [a for a in data["av"]
                if a["rooms_covered"] >= v2["rooms"]]
        if cov2:
            av2 = min(cov2, key=lambda a: (a["total"], a["vendor"]))
            if av2["vendor"] != av["vendor"]:
                alt["04"] = {"av_vendor": [av2["vendor"]],
                             "av_total": [money(av2["total"])]}

    # -- phase 5: first reconciliation -------------------------------
    venue_total = venue["daily_rate"] * EVENT_DAYS
    estimate = eff(c1) * att
    remaining = (data["total_budget"] - venue_total - spent
                 - av["total"] - estimate)
    if remaining <= 0:
        raise Redraw("phase-5 remainder not positive")
    phases["05"] = {"lines": {
        "venue_total": money(venue_total),
        "speaker_total": money(spent),
        "av_total": money(av["total"]),
        "catering_estimate": money(estimate),
        "remaining": money(remaining)}}

    # -- phase 6: hotel blocks ---------------------------------------
    target = ceil_div(att * 6, 10)
    hotels = sorted(data["hotels"],
                    key=lambda h: (h["distance"], h["code"]))
    taken: list[tuple[dict, int]] = []
    left = target
    for h in hotels:
        if left <= 0:
            break
        take = min(h["rooms"], left)
        taken.append((h, take))
        left -= take
    if left > 0:
        raise Redraw("hotel supply below 60% target")
    rooms_tot = sum(t for _, t in taken)
    blended = sum(h["rate"] * t for h, t in taken) // rooms_tot
    hotels_val = ",".join(
        f"{h['code']}={t}" for h, t in
        sorted(taken, key=lambda ht: ht[0]["code"]))
    phases["06"] = {"lines": {
        "hotels": hotels_val, "blended_rate": money(blended)}}

    # -- phase 7: sponsors -------------------------------------------
    unsigned_gold = sum(1 for s in data["sponsors"]
                        if s["tier"] == "gold" and not s["signed"])
    signed_rev = sum(s["commitment"] for s in data["sponsors"]
                     if s["signed"])
    phases["07"] = {"lines": {
        "unsigned_gold": str(unsigned_gold),
        "signed_revenue": money(signed_rev)}}

    # -- phase 8: keynote schedule -----------------------------------
    per_day: dict[int, list[str]] = {1: [], 2: [], 3: []}
    for s in picked:  # rank order
        placed = False
        for d in sorted(s["days"]):
            if len(per_day[d]) < 2:
                per_day[d].append(s["name"])
                placed = True
                break
        if not placed:
            raise Redraw("keynote schedule does not place")
    phases["08"] = {"lines": {
        f"day{d}": "; ".join(per_day[d]) if per_day[d] else "none"
        for d in (1, 2, 3)}}

    # -- phase 9: catering booking -----------------------------------
    late_conf = sum(1 for _, _, s, _ in data["late"]
                    if s == "confirmed")
    final_head = att + late_conf
    cost9 = c1["per_head"] * final_head + c1["service_fee"]
    delta = cost9 - estimate
    if delta == 0:
        raise Redraw("phase-9 delta is zero")
    phases["09"] = {"lines": {
        "caterer": c1["code"],
        "final_headcount": str(final_head),
        "catering_cost": money(cost9),
        "delta_vs_estimate": money(delta)}}
    cost9_alt_head = c1["per_head"] * att + c1["service_fee"]
    cost9_alt_cat = c2["per_head"] * final_head + c2["service_fee"]
    alt["09"] = {
        "caterer": [c2["code"]],
        "final_headcount": [str(att)],
        "catering_cost": [money(cost9_alt_head),
                          money(cost9_alt_cat)],
        "delta_vs_estimate": [money(cost9_alt_head - estimate),
                              money(cost9_alt_cat - estimate)]}

    # -- phase 10: shuttles ------------------------------------------
    shuttles = [(h["code"], ceil_div(t, data["seats"]))
                for h, t in taken]
    shuttles.sort()
    n_shuttles = sum(n for _, n in shuttles)
    daily = n_shuttles * data["shuttle_daily"]
    phases["10"] = {"lines": {
        "shuttles": ",".join(f"{c}={n}" for c, n in shuttles),
        "transport_daily": money(daily)}}

    # -- phase 11: insurance -----------------------------------------
    contracted = venue_total + spent + av["total"] + cost9
    qual_tiers = [t for t in data["tiers"]
                  if t["coverage"] >= contracted]
    if not qual_tiers:
        raise Redraw("no insurance tier covers contracted spend")
    tier = min(qual_tiers, key=lambda t: t["premium"])
    phases["11"] = {"lines": {
        "insurance_tier": tier["tier"],
        "premium": money(tier["premium"])}}
    # Stale twin: coverage for contracted-minus-catering (the wrong
    # memory that phase 9 never happened).
    qual_wo = [t for t in data["tiers"]
               if t["coverage"] >= contracted - cost9]
    if qual_wo:
        t_wo = min(qual_wo, key=lambda t: t["premium"])
        if t_wo["tier"] != tier["tier"]:
            alt["11"] = {"insurance_tier": [t_wo["tier"]],
                         "premium": [money(t_wo["premium"])]}

    # -- phase 12: final close ---------------------------------------
    deposit = (blended * rooms_tot * 3) // 10
    transport3 = daily * EVENT_DAYS
    lines_by_label = {
        "venue": venue_total, "keynotes": spent, "av": av["total"],
        "catering": cost9, "hotels": deposit, "transport": transport3,
        "insurance": tier["premium"]}
    final_rem = data["total_budget"] - sum(lines_by_label.values())
    if final_rem <= 0:
        raise Redraw("final remainder not positive")
    ordered = sorted(lines_by_label.items(), key=lambda kv: -kv[1])
    if ordered[0][1] == ordered[1][1]:
        raise Redraw("largest line is ambiguous")
    phases["12"] = {"lines": {
        "final_remaining": money(final_rem),
        "largest_line": ordered[0][0]}}

    # -- dependency registry -----------------------------------------
    deps = {"01": [], "02": ["01"], "03": [], "04": ["01"],
            "05": ["01", "02", "03", "04"], "06": ["01"], "07": [],
            "08": ["03"], "09": ["01", "02", "05"],
            "10": ["01", "06"], "11": ["03", "04", "05", "09"],
            "12": ["05", "06", "09", "10", "11"]}
    for nn, meta in phases.items():
        meta["dependent"] = bool(deps[nn])
        meta["depends_on"] = deps[nn]

    registry = {
        "dependencies": deps,
        "known_alternatives": alt,
        "code_universe": {
            "venues": sorted(v["code"] for v in data["venues"]),
            "caterers": sorted(c["code"] for c in data["caterers"]),
            "av_vendors": sorted(a["vendor"] for a in data["av"]),
            "hotels": sorted(h["code"] for h in data["hotels"]),
            "insurance_tiers": sorted(t["tier"] for t in data["tiers"]),
            "speakers": sorted(s["name"] for s in data["speakers"]),
        },
    }
    return phases, registry


# ---------------------------------------------------------------------
# build / self-test / output
# ---------------------------------------------------------------------


def build(seed: int) -> tuple[dict[str, str], dict, dict]:
    for attempt in range(MAX_ATTEMPTS):
        rng = random.Random(f"{seed}:{attempt}")
        corpus = _build_once(rng)
        for rel, text in corpus.items():
            if len(text.encode()) > MAX_FILE_BYTES:
                break
        else:
            try:
                phases, registry = walk_phases(parse_corpus(corpus))
            except Redraw:
                continue
            return corpus, phases, registry
    raise SystemExit(f"no feasible corpus in {MAX_ATTEMPTS} attempts "
                     f"for seed {seed}")


def self_test(corpus: dict[str, str], phases: dict) -> None:
    """Re-parse the emitted bytes and re-walk; the key must match."""
    rephases, _ = walk_phases(parse_corpus(corpus))
    for nn in sorted(phases):
        if rephases[nn]["lines"] != phases[nn]["lines"]:
            print(f"  phase {nn}: derived {rephases[nn]['lines']!r}"
                  f" != key {phases[nn]['lines']!r}", file=sys.stderr)
            raise SystemExit("self-test FAILED: corpus does not "
                             "support the answer key")


def write_out(out_dir: Path, corpus: dict[str, str], phases: dict,
              registry: dict, seed: int) -> None:
    for rel, text in sorted(corpus.items()):
        path = out_dir / "seed-files" / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode("utf-8"))
    (out_dir / "answers.json").write_bytes(json.dumps(
        {"seed": seed, "phases": phases, "registry": registry},
        indent=1, sort_keys=True).encode("utf-8") + b"\n")


def _tree(root: Path) -> dict[str, bytes]:
    return {str(p.relative_to(root)): p.read_bytes()
            for p in sorted(root.rglob("*")) if p.is_file()}


def run_check(task_dir: Path, seed: int) -> int:
    corpus, phases, registry = build(seed)
    self_test(corpus, phases)
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp)
        write_out(tmp_dir, corpus, phases, registry, seed)
        fresh = _tree(tmp_dir)
    committed = {k: v for k, v in _tree(task_dir).items()
                 if k == "answers.json" or k.startswith("seed-files/")}
    problems = []
    for rel in sorted(set(fresh) | set(committed)):
        if rel not in committed:
            problems.append(f"missing from committed corpus: {rel}")
        elif rel not in fresh:
            problems.append(f"stale committed file: {rel}")
        elif fresh[rel] != committed[rel]:
            problems.append(f"byte mismatch: {rel}")
    if problems:
        print("\n".join(problems), file=sys.stderr)
        print(f"check FAILED for seed {seed}", file=sys.stderr)
        return 1
    print(f"check OK: {len(fresh)} files byte-identical for seed {seed}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=DEFAULT_SEED)
    parser.add_argument("--out",
                        default=str(Path(__file__).resolve().parent))
    parser.add_argument("--check", action="store_true",
                        help="regenerate into a temp dir and diff "
                             "against the committed corpus")
    args = parser.parse_args()
    task_dir = Path(args.out)
    if args.check:
        return run_check(task_dir, args.seed)
    corpus, phases, registry = build(args.seed)
    self_test(corpus, phases)
    write_out(task_dir, corpus, phases, registry, args.seed)
    total = sum(len(t.encode()) for t in corpus.values())
    n_dep = sum(1 for p in phases.values() if p["dependent"])
    print(f"seed {args.seed}: {len(corpus)} files, "
          f"{total / 1024:.0f} KiB, {n_dep}/12 dependent phases")
    for nn in sorted(phases):
        lines = phases[nn]["lines"]
        first = next(iter(lines.items()))
        print(f"  {nn}: {first[0]}={first[1]}"
              + ("  [dep]" if phases[nn]["dependent"] else ""))
    print("self-test OK: all twelve phases re-derived from the "
          "emitted corpus")
    return 0


if __name__ == "__main__":
    sys.exit(main())
