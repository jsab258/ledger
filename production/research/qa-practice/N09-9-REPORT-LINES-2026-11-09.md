# n09-9: the night report's three lean-QA lines (9 Nov 2026)

Source: QA-LEAN-PROPOSAL-2026-11-07.md part 4 (three read-only lines in tools/nightly_walk.py); QA-FIRST-STEPS-2026-11-08.md steps 1 to 3.

## What existed
- **Legs that never arrived:** `legs_never_arrived()` (commit 276d2f423, corrected 2cad25a44). Stores "fired".
- **Launch switches:** `launch_sentence()` through launch_line_check.describe (2cad25a44); a switch beyond the allowed list reads "a test launch: ...".
- **Memory's peak:** built 8 Nov in tools/slice-perf.py (commit 2587d1a1d; reviewed in MEMORY-PEAK-REVIEW-2026-11-08.md). The build machine commits its line to production/d1-probe/ue-perf-verdict.txt with each build. It was **not** in the night report.

## What was added (tools/nightly_walk.py)
- `parse_perf()`, `perf_level()`, `memory_peak(at_ts)`, `memory_sentence()`; `report()` stores `summary["memory_peak"]`; `paragraph()` prints it.
- It reads the newest perf line on origin/wip at or before the report time, and gives peak, median and settled peak against 5,650. Fired means OVER-LINE.
- **It reports only.** Any failure becomes a note, never a failed walk.
- **Level is labelled honestly:** the perf step carries no "scalability 2" (yml, the csvprofile step), so the line says "at Highest, the perf step's level, not the played High". It switches to "High" by itself once the step carries scalability 2. That change is still held for Monday's order.
- **Self-test:** 22/22 (4 new cases).

## Real nights checked
The report part was run on each night's state.json, with the time set to that file's time. Output went to F:/LedgerTools/tmp/n09-9-check/; the real reports kept their times.

| Night | Legs | Launch | Memory |
|---|---|---|---|
| 7 Nov | fired, one run of 14 legs (the proposal's done-when) | not recorded (a walk from before 8 Nov) | not measured: the line for build 3b548c1 came before the peak; fired no |
| 8 Nov | fired, four runs of 14 | not recorded | not measured (build fa46ab0); fired no |
| 9 Nov | fired, one run of 14 | PLAYER+WATCH (talk is the stand-in) | not measured (build 5ed8f38, 8 Nov 12:57); fired no |

- **Newest perf line (build 09701ac, 9 Nov 11:03):** peak 6,332 MB at Highest, OVER-LINE, fired yes. Median 5,864; peak after the first 300 frames 5,868.
- **Tonight:** the next night's report is the first to carry all three lines with a real peak (not yet seen).

## ci-checks
`ci-checks done: passed=99/99 failed=none` (run before this note was written; the catalogue check re-run after it: entries=170 missing=0 outcome=PASS).
