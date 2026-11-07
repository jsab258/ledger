# Exit D rehearsal, fresh review, 7 November 2026

Recomputed from raw frames (7bef7cf, evening hair captures: 54,000 frames), memory series, perf history.

## 22 October's faults

- Gone: 42 to 55 ms at 5.4 s; voice short of real time (Pocket makes speech in 0.40 of its length).
- Not gone: walk worst frame; card spare time, now worse (day 0.22 to 0.27 ms, night 0.09 to 0.15; then 0.54, 0.28); other programs on the card (1.7 GB, then 1.5); no build or voice field in runs.jsonl; Development and off-screen only; night walk unmeasured.

## Verdict: NOT MET

- **Measured headroom: missed.** Spare card time as above, against PLAN's 2.5 and 1.4 and the 1.7 ms accepted on 24 October (runs.jsonl). No memory margin.
- **Walk worst 33.3 ms, never below 30: missed.** 25 walks, 45,000 frames: 230.8 ms (nomapc), 39.2 ms (rate16). Cause unread.
- **6 GB, game alone, steady use: met on captures, missed on the latest build.** Medians 5,566 to 5,936 MB (game's own figure), 5,775 to 5,983 (Windows'). Today's perf line, median: 6,089. About 290 of each walk's 1,800 frames exceed 6,000, highest 6,192.
- **6 GB as a peak: missed.** Windows' counter, game alone: 6,161 to 8,481 MB in all 32 captures; game's own figure 6.1 to 6.2 GB at launch. All processes: median 7.5 to 7.7 GB, peak 7.9 to 10.2. LAUNCH-PEAK's "not the game's own" conflicts with DIAGNOSIS (private memory moves too) and the series.
- **Median 16.7 ms: met with Pocket, missed in the perf step.** Pocket: 15.12 to 15.27 standing, 11.64 to 12.02 walking. Perf line: 17.61, BELOW-60, 56.8 fps, 1,260 of 1,500 frames over.
- **p99 25 ms: met.** True p99 18.7 to 22.2; perf line 21.85.

## Gaps for Monday

- No p1-packaged capture on 3b548c1: the walk bar rests on 7bef7cf; hair captures carry no build.
- The brief says the perf step "walked" the map's removal; the workflow stands still. The brief also omits BELOW-60.
- The perf step speaks Nano on the card, not the cast's Pocket, at 50% not 55%.
- The overnight rise, 5,844 to 6,089 MB, is unexplained.
- Stale: the brief's "5,960 after the hill"; FINDINGS' headroom line.
- Night with the voice speaking: latest 3641d53; hair captures' voice load unrecorded. Voice log overwritten.
- Could not judge: wet night, full population, real play's present, Shipping. None measured.
