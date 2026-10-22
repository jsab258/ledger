# Phase 1's close, Exit D (P1 packaged and the render and voice pairing's headroom): the fresh review, 22 October 2026

A fresh reviewer (Opus), given CLOSE-BRIEF-2026-10-22.md and the outputs, not the maker's verdict; read only, every figure recomputed from the raw frame captures (perf-hook.py). Its report, verbatim in substance:

**Builds and voices.** The 21 October "final" runs are build 00f81b1 with the cast voice on the card. The 22 October runs (pocket-below, pocket-below-4t, card-today) are 35e10a9: the same frame path, since only the ask script and tools changed between them. runs.jsonl does not record either.

**Verdicts.**
- **Day standing (00f81b1, card): MET** on the median, 15.19 ms, and the true p99, 23.35. But the worst frame is 35.63 and two frames are over 33.3, against RULINGS 23 September's "never below 30". runs.jsonl still says MEETS; today's tool would say SPIKES.
- **Night standing: MET** at 15.36 / 23.57 / worst 32.98. **Night walking, wet: NOT SHOWN.**
- **Walking by day: MET once, NOT MET on the repeat.** 00f81b1 with the card voice gave 14.38 / 23.96 / worst 30.34. 35e10a9 with the card voice gave worst 87.17, with 2 frames over 33.3.
- **Windows memory: MET as coverage.** Counters were read every 2 s, 20 to 23 samples a run.
- **Sustained speech: MET as a load on the card, partly unkept.** The kept voice log in latency/p1-2026-10-21 is a Pocket run; the 00f81b1 card-voice log is not kept. The 22 October card log is kept: 325.2 s made in 301.9 s.
- **Median ≤16.7 ms: MET**, but only for dry, partial-population runs. The exit's own conditions (a wet night, the full population) are NOT SHOWN.
- **p99 ≤25 ms: MET by true percentile** (23.35 to 23.96). The tables' "slowest 1%" is the mean of the slowest 18 frames (25.44 to 26.52), not the p99.
- **6 GB with the voice on the card: NOT MET.** The card in all, with the voice, has a median of 7.06 to 7.19 GB and a peak of 9.16 to 9.42 GB (00f81b1); 7.92 and 9.92 GB on 35e10a9. The game alone peaks at 5.37 GB. The files read this line two ways: 7 October counted the game alone, 21 October the total.
- **Walk worst ≤33.3: NOT MET as a lasting property.** It passed once (30.34) and failed the repeat (87.17).
- **Measured headroom: NOT MET.**
  - The card's spare time against the 14.0 ms planning line, standing on 00f81b1, is 0.54 ms by day and 0.28 at night. PLAN budgets about 2.5 and 1.4, and 7 October (67c51f5) had 2.65 and 2.95. The 21 October file left out the card-time column, so the fall was never named.
  - Card memory has about 0.5 GB spare at peak (0.06 GB on 22 October).
  - The voice keeps up at only 0.93 to 0.96 of real time.

**Repeats of the same code.**
- With any voice on the final game code, 1 of 5 counted walks keeps every frame under 33.3: 174.68, 47.37, 47.50 and 87.17 fail.
- The run-to-run spread (tens of ms on the worst frame, 1.6 ms on the median) is larger than every claimed margin, so with one run per condition no headroom can be claimed.
- The standing views were not repeated.

**Faults and gaps the maker's files do not name.**
- **The spikes keep landing on the same moment.** In every walk, at 5.43 to 5.47 s (about 4.2 m), the capture's events show FlushAsyncLoading and then a first-use graphics pipeline (PSOMisses=1). The slow frame follows 3 to 4 frames later in 10 of 14 walk captures.
  - Before the occlusion setting it showed as the slow frames blamed on occlusion queries near Mickey's office; after it, as the RHI-thread waits (frames 368, 376 and 418).
  - The 80 ms wait at frame 1221 is followed by compute and graphics pipeline misses.
  - This points to shader-pipeline compile hitches, which the occlusion setting may have hidden rather than removed: a lead, not a proof.
- **The 22 October runs were not on a quiet PC.** Other processes held 1.52 to 1.56 GB of the card (0.29 to 0.38 GB on 21 October), and the PC used 2 to 4 GB more memory.
- **POCKET-CPU misread one frame.** Its 21 October section says the 43.3 ms frame had "the game's threads short", but that frame's RHI wait was 31.7 ms, the same kind of wait as on 22 October.
- **The walk is 1,800 frames, not a fixed route.** It covered 34.6 m on 21 October and 27.8 to 30.2 m on 22 October.
- runs.jsonl has no build or voice field. Everything ran on the Development package, off screen; nothing on a Shipping build. No AI tester walk of the final package is on record.

**Not reached.** walk-b414e8c.utrace (not opened).

**Verdict.** Exit D does not pass phase 1's exit.
