"""Forecast an order's real hours from the project's own past overruns.

Method: reference class forecasting (Flyvbjerg) done the evidence-based
scheduling way (Spolsky 2007). For every finished item we know its planned
hours and its logged hours; actual / planned is that item's ratio. A new
plan's total is forecast by Monte Carlo: each planned item draws a random
past ratio, the drawn hours are summed, and this is repeated many times.
The 50th and 80th percentiles of the sums are P50 and P80. Seeded, so the
same inputs always give the same answer. Standard library only.

Inputs
  --log   production/time-log.jsonl ("start" has task, phase, kind; "stop" follows)
  --plan  JSON or CSV of planned hours per item:
          JSON {"items": [{"code": "n09-2", "planned_h": 3, "done": true}, ...]}
          CSV  header code,planned_h,done
  Items are matched to log tasks by the item code at the start of the task
  name (for example "n09-2 Tom as one whole person"). A plan item can also
  list "aliases": extra task-name prefixes that count towards it.

Usage
  python tools/lane/forecast.py --log production/time-log.jsonl \
      --plan tools/lane/forecast_example_plan.json [--extra-ratio 4.3] [--json]
  The forecast is for the plan's open (not done) items unless --new names
  another plan file.
"""
from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
import re
import sys
from collections import defaultdict

MIN_OWN_RATIOS = 8  # below this the ratio pool is too thin to trust (see the B12 note)
CODE_RE = re.compile(r"^\s*`?(n\d{2}-\d+)(?!\d)")


def task_code(task: str):
    m = CODE_RE.match(task or "")
    return m.group(1) if m else None


def read_log(path):
    """Return ({task name: hours}, unclosed, backwards) from start/stop pairs.
    A start with no stop before the next start is closed at that next start
    (and counted in unclosed). An interval that runs backwards in time (a
    clock or typing slip) is skipped and counted in backwards."""
    hours = defaultdict(float)
    open_ev = None
    unclosed = 0
    backwards = 0

    def add(task, start, end):
        nonlocal backwards
        h = (end - start).total_seconds() / 3600
        if h < 0:
            backwards += 1
        else:
            hours[task] += h

    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            ev = json.loads(line)
            at = dt.datetime.fromisoformat(ev["at"])
            if ev.get("event") == "start":
                if open_ev is not None:
                    unclosed += 1
                    add(open_ev[0], open_ev[1], at)
                open_ev = (ev.get("task", ""), at)
            elif ev.get("event") == "stop" and open_ev is not None:
                add(open_ev[0], open_ev[1], at)
                open_ev = None
    return dict(hours), unclosed, backwards


def read_plan(path):
    if path.lower().endswith(".csv"):
        with open(path, encoding="utf-8", newline="") as f:
            rows = list(csv.DictReader(f))
        items = []
        for r in rows:
            items.append({
                "code": r["code"].strip(),
                "planned_h": float(r["planned_h"]),
                "done": str(r.get("done", "")).strip().lower() in ("1", "true", "yes", "done"),
            })
        return items
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    return data["items"] if isinstance(data, dict) else data


def actual_per_item(task_hours, items):
    """Sum logged hours onto plan items. Returns (per-code hours, unmatched task hours)."""
    per = {it["code"]: 0.0 for it in items}
    aliases = [(a, it["code"]) for it in items for a in it.get("aliases", [])]
    unmatched = {}
    for task, h in task_hours.items():
        code = task_code(task)
        if code in per:
            per[code] += h
            continue
        hit = next((c for a, c in aliases if task.startswith(a)), None)
        if hit:
            per[hit] += h
        else:
            unmatched[task] = h
    return per, unmatched


def ratios(items, per):
    """actual / planned for finished items with hours on both sides."""
    out = []
    for it in items:
        if it.get("done") and it["planned_h"] > 0 and per.get(it["code"], 0) > 0:
            out.append((it["code"], per[it["code"]] / it["planned_h"]))
    return out


def percentile(sorted_vals, p):
    """Nearest-rank percentile, p in 0..100."""
    if not sorted_vals:
        raise ValueError("no values")
    k = max(1, -(-len(sorted_vals) * p // 100))  # ceil
    return sorted_vals[int(k) - 1]


def forecast(planned, ratio_list, sims=20000, seed=1990):
    """Monte Carlo: each planned item takes a random past ratio; sum; repeat."""
    if not ratio_list:
        raise ValueError("no ratios to resample")
    rng = random.Random(seed)
    totals = sorted(
        sum(p * rng.choice(ratio_list) for p in planned) for _ in range(sims)
    )
    return {
        "plan_h": sum(planned),
        "p50_h": percentile(totals, 50),
        "p80_h": percentile(totals, 80),
        "sims": sims,
        "seed": seed,
    }


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--log", required=True)
    ap.add_argument("--plan", required=True)
    ap.add_argument("--new", help="plan to forecast (default: open items of --plan)")
    ap.add_argument("--extra-ratio", type=float, action="append", default=[],
                    help="add an outside ratio (for example phase 1's 4.3)")
    ap.add_argument("--sims", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=1990)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    task_hours, unclosed, backwards = read_log(a.log)
    items = read_plan(a.plan)
    per, unmatched = actual_per_item(task_hours, items)
    rs = ratios(items, per)
    pool = [r for _, r in rs] + a.extra_ratio
    new_items = read_plan(a.new) if a.new else [i for i in items if not i.get("done")]
    planned = [i["planned_h"] for i in new_items]

    result = {
        "matched_ratios": [{"code": c, "ratio": round(r, 3)} for c, r in rs],
        "extra_ratios": a.extra_ratio,
        "logged_h_matched": round(sum(per.values()), 2),
        "logged_h_unmatched": round(sum(unmatched.values()), 2),
        "unclosed_starts": unclosed,
        "backwards_intervals_skipped": backwards,
        "done_items_without_log": [i["code"] for i in items
                                   if i.get("done") and per.get(i["code"], 0) == 0],
    }
    warnings = []
    if len(rs) < MIN_OWN_RATIOS:
        warnings.append(f"only {len(rs)} own ratios (fewer than {MIN_OWN_RATIOS}): "
                        "the forecast is not yet trustworthy")
    if any(r < 0.25 for _, r in rs):
        warnings.append("a ratio under 0.25: check the log for missing hours on that item")
    result["warnings"] = warnings
    if pool and planned:
        f = forecast(planned, pool, a.sims, a.seed)
        result["forecast"] = {k: round(v, 1) if isinstance(v, float) else v for k, v in f.items()}
    else:
        result["forecast"] = None
    if a.json:
        print(json.dumps(result, indent=2))
    else:
        for k, v in result.items():
            print(f"{k}: {v}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
