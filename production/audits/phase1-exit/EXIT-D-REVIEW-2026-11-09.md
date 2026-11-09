# Phase 1's exit, Exit D: fresh review, 9 November 2026

Fresh reviewer (Opus), read only; brief CLOSE-BRIEF-2026-11-09.md. Figures recomputed from the raw CSVs and memory files in F:/LedgerTools/tmp/p1-packaged/ and from the perf-step lines in git (production/d1-probe/ue-perf-verdict.txt).

There was no build on 8 to 9 November. The newest copy is 5ed8f38 (played-game/LEDGER-STABLE-COPY.txt). It has two captures: its 12:57 perf step, and the 21:24 "memwhere" walk, a memory diagnosis with memreport dumps at frames 560 and 1100.

The bars, unchanged:
- P1 packaged: day, night, walking, Windows memory, sustained speech.
- Median frame 16.7 ms or less, p99 25 ms, 6 GB of card memory for the game alone (RULINGS 24 Oct).
- Worst walking frame 33.3 ms or less (order of 21 Oct).
- 60 fps at 3440x1440 with the voice running (RULINGS 23 Sep).
- Measured headroom.

## The 22 October faults

- **Day standing worst frame: gone.** 30.17 ms on the one 3b3454e run (frame 0, start-up).
- **Walk worst frame as a lasting property: not gone.**
  - On 7bef7cf, 2 of 25 walks went over: nomapc 230.8 ms (row 394, render thread 230.5) and rate16 39.2 ms (row 327, render 41.1).
  - The newest copies have only two walks: 3b3454e worst 32.03 ms, and 5ed8f38 worst 32.69 ms once its two self-made memreport frames (1,923 and 1,266 ms) are excluded.
- **The spike about 4.2 m in: not gone.**
  - In 15 of 25 walks on 7bef7cf the worst frame falls at frames 320 to 395.
  - On 3b3454e, a 31.8 ms render-thread frame (row 364) comes just before the worst, 32.03 ms at frame 365. That leaves a 1.3 ms margin, cause unread.
- **Night walk, wet: still not shown.** There is no night-walk capture in runs.jsonl.
- **Card-time headroom: not met, now lower.**
  - 3b3454e standing, card median 13.79 ms by day and 13.81 ms at night: 0.21 and 0.19 ms spare against the 14.0 ms line.
  - It was 0.54/0.28 ms on 22 Oct and 1.62/2.81 ms on 3 Nov, and 0.27 ms since 6 Nov.
- **6 GB line: not met** (see Memory below).
- **Voice pace: gone.** On 5ed8f38, Pocket on the processor spoke 429 lines, 1,949 s of speech made in 660 s: 0.34 of real time, against 0.93 to 0.96 then.
- **Median and p99 with Pocket: met.** Medians 10.9 to 15.2 ms; true p99 18.85 to 21.25 ms. The runs.jsonl "slowest 1%" column is still not the p99 (23.86 against 20.59).
- **Records: not gone.**
  - runs.jsonl still has no build or voice field.
  - The copy is still Development (Binaries/Win64/LedgerProbe.exe).
  - The walk distance still varies (30.9 and 33.7 m).

## New

- **The perf step, with Nano on the card, misses 60 fps and the median.**
  - 5ed8f38: median 17.13 ms, 58.4 fps, BELOW-60. The card median is 15.05 ms, over the 14.0 line.
  - All eight steps from 7 Nov 21:48 to 8 Nov 12:57 had medians of 17.03 to 17.74 ms.
  - Worst frames were 22.4 to 25.6 ms, none over 33.3. The step stands still.
- **FINDINGS line 12 is stale.** It says 1.7 to 1.8 ms of spare card time "not re-measured"; the raw figures have been 0.19 to 0.27 ms since 6 Nov.
- **No voice log for the 3b3454e "sun" runs.** voice-load.log is overwritten each run, so only the voice process's memory (2.1 to 3.2 GB private) shows that it ran.

## Memory (game alone, Windows' dedicated counter; the engine's own count in brackets)

- **Standing: met as steady use.** Medians 5,659 MB by day and 5,983 MB at night (engine 5,209 and 5,532).
- **Walking: not met as steady use.** Medians 6,145 MB (3b3454e) and 6,151 MB (5ed8f38); 34 of 38 and 36 of 44 samples are over 6,000. The engine's count is 5,843 and 5,830 median, peaking at 6,127 and 6,152.
- **Peak: not met in any run.** 6,666, 6,523, 8,716 and 6,749 MB.
- The walking figures exceed both 6,000 MB and 6,144 MiB. With all processes counted, medians are 6,474 to 7,089 MB and peaks reach 9,528 MB.

## Verdict: NOT MET

1. **6 GB line, walking and at peak.** Evidence: packaged-day-walk--3b3454e-sun-memory.jsonl and packaged-day-walk-memwhere-memory.jsonl.
2. **Card-time headroom.** 0.21 and 0.19 ms (runs.jsonl rows 363 and 365, their CSVs). Below zero with the voice on the card (perf step e4d830412).
3. **60 fps with the voice on the card.** 58.4 fps, median 17.13 ms (e4d830412).
4. **Walk worst frame as a lasting property.** 2 of 25 walks over on 7bef7cf; only two walks on the newest copies, both within 1.7 ms of the line.
5. **P1 incomplete.** No night walk.

Met: medians and p99 with Pocket, memory coverage, speech pace.
