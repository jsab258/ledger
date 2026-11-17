"""Summarise a PresentMon CSV capture into the budget table's frame numbers.

For n16-11 (numbers from the games' files): frame times are measured from
outside the game with Intel PresentMon (MIT, ETW, nothing injected), then
this script turns one capture into one row: frames, median, P95 and P99
frame time, the 1% low average, the time-weighted 1% low, and spikes.

Columns accepted (matched case-insensitively, first found wins):
  MsBetweenAppStart  (PresentMon 2.x default; GamersNexus' hardware frame time)
  FrameTime          (PresentMon 2.x with --v2_metrics)
  MsBetweenPresents  (2.x default and 1.x as msBetweenPresents; cross-check)
Process filter column: Application (2.x) or ProcessName (1.x).
Source of column names: production/research/lane/FRAMETIME-METHOD-2026-11-17.md.

Definitions (same file, section 4):
  P99 frame time       nearest-rank 99th percentile of frame times.
  1% low average fps   1000 / mean of the slowest 1% of frames (by count).
  1% low time-weighted 1000 / the frame time at which the slowest frames,
                       summed from the slowest down, first reach 1% of the
                       run's total time (CapFrameX's "1% low").
  spikes               frames longer than twice the median.

Usage: python tools/lane/frametime_summary.py capture.csv [--process X.exe]
       [--skip-seconds 5] [--column MsBetweenAppStart]
Prints one JSON object. Python 3 standard library only; no build needed.
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import sys
from typing import Iterable

FRAME_COLUMNS = ("MsBetweenAppStart", "FrameTime", "MsBetweenPresents")
PROCESS_COLUMNS = ("Application", "ProcessName")


def _find(header: Iterable[str], wanted: Iterable[str]) -> str | None:
    lower = {h.strip().lower(): h for h in header}
    for w in wanted:
        if w.lower() in lower:
            return lower[w.lower()]
    return None


def nearest_rank(sorted_values: list[float], pct: float) -> float:
    """Nearest-rank percentile (pct in 0..100) of an ascending list."""
    if not sorted_values:
        raise ValueError("no values")
    rank = max(1, math.ceil(pct / 100.0 * len(sorted_values)))
    return sorted_values[rank - 1]


def median(sorted_values: list[float]) -> float:
    n = len(sorted_values)
    if n == 0:
        raise ValueError("no values")
    mid = n // 2
    if n % 2:
        return sorted_values[mid]
    return (sorted_values[mid - 1] + sorted_values[mid]) / 2.0


def summarise(frame_ms: list[float]) -> dict:
    """The table's frame numbers from a list of frame times in ms."""
    values = [v for v in frame_ms if v > 0 and math.isfinite(v)]
    if len(values) < 100:
        raise ValueError(f"only {len(values)} usable frames; need at least 100")
    asc = sorted(values)
    desc = asc[::-1]
    total = sum(values)
    med = median(asc)

    slow_n = max(1, len(values) // 100)
    low_avg_ms = sum(desc[:slow_n]) / slow_n

    acc = 0.0
    tw_ms = desc[0]
    for v in desc:
        acc += v
        tw_ms = v
        if acc >= 0.01 * total:
            break

    return {
        "frames": len(values),
        "seconds": round(total / 1000.0, 2),
        "median_ms": round(med, 2),
        "p95_ms": round(nearest_rank(asc, 95), 2),
        "p99_ms": round(nearest_rank(asc, 99), 2),
        "worst_ms": round(asc[-1], 2),
        "avg_fps": round(1000.0 * len(values) / total, 1),
        "low1_avg_fps": round(1000.0 / low_avg_ms, 1),
        "low1_timeweighted_fps": round(1000.0 / tw_ms, 1),
        "spikes_over_2x_median": sum(1 for v in values if v > 2 * med),
        "reliable_0_1_percent": len(values) > 1000,
    }


def pass_spread_pct(pass_medians: list[float]) -> float:
    """Spread of the passes' medians, (max - min) / min in percent.
    The method re-runs a game's passes when this is over about 3%."""
    if len(pass_medians) < 2 or min(pass_medians) <= 0:
        raise ValueError("need at least two positive pass medians")
    return round(100.0 * (max(pass_medians) - min(pass_medians)) / min(pass_medians), 2)


def read_capture(path: str, process: str | None = None, column: str | None = None,
                 skip_seconds: float = 0.0) -> tuple[list[float], str]:
    """Frame times (ms) from a PresentMon CSV, optionally one process only,
    dropping the first skip_seconds of the run (warm-up)."""
    with open(path, newline="", encoding="utf-8-sig") as fh:
        reader = csv.DictReader(fh)
        header = reader.fieldnames or []
        col = _find(header, (column,) if column else FRAME_COLUMNS)
        if col is None:
            raise ValueError(f"no frame time column in {path}; header: {header}")
        pcol = _find(header, PROCESS_COLUMNS) if process else None
        if process and pcol is None:
            raise ValueError("a process filter was asked but the CSV has no process column")
        out: list[float] = []
        elapsed = 0.0
        for row in reader:
            if pcol and row[pcol].strip().lower() != process.lower():
                continue
            raw = (row.get(col) or "").strip()
            try:
                v = float(raw)
            except ValueError:
                continue  # "NA" and blanks in PresentMon output
            elapsed += v / 1000.0
            if elapsed <= skip_seconds:
                continue
            out.append(v)
    return out, col


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("csv")
    ap.add_argument("--process")
    ap.add_argument("--column")
    ap.add_argument("--skip-seconds", type=float, default=0.0)
    a = ap.parse_args(argv)
    frames, col = read_capture(a.csv, a.process, a.column, a.skip_seconds)
    result = summarise(frames)
    result["column"] = col
    result["source"] = a.csv
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
