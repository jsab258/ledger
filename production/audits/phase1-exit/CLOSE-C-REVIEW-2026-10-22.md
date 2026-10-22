# Phase 1's close, Exit C (P2, the voice, and the speech line): the fresh review, 22 October 2026

A fresh reviewer (Opus), given CLOSE-BRIEF-2026-10-22.md and the outputs, not the maker's verdict; read only, figures recomputed from the raw lines where they survive. Its report, verbatim in substance:

**Verdicts.**
- **Two measured approaches, shared card and CPU or quantised: MET.**
  - The card voice's own share beside the game was 3.66 s (EVIDENCE-2026-10-01.md line 57; RESULTS-2026-10-06.md line 93).
  - On the CPU: A (8-bit) 4.18 s, B (a lighter decoder) 3.36 s, and Pocket 0.13 s outside the game and 0.23 s in the editor's game (recomputed from F:/LedgerTools/latency).
  - "At most two" was exceeded: A, B and Pocket, plus streaming and a compiled step on 1 October. Pocket came by his 21 October order.
  - Only Pocket reaches P2's own pass line (the voice's share at most 1.0 s), and that with stand-in talk.
- **Timed beside checked talk: NOT MET for the CPU arm.** A and B were handed fixed cast lines. Pocket used the stand-in talk (pocket-2026-10-21.json: live false, fixed replies). Only the card voice was timed on checked talk (CLOUD-VOICE lines 49 to 59; DECISIONS.md line 395).
- **Median first meaningful speech two seconds or less, no prepared openings: NOT MET.**
  - In the packaged copy, 4.63 s (7 October, Sheila, the card voice, five checked replies; 3.99 s with the faster first-sentence model; recomputed).
  - The best whole-path median with today's check and an approved voice: 3.25 s (8 October, latency.py on the real path, Sonnet 5 replies, Haiku 5.5 check, the card voice, 20 turns). Its "heard" is computed, not heard in the game; nothing records whether the game was open; no raw record survives.

**Faults and gaps the maker does not name.**
- FINDINGS.md's speech line is out of date: it gives 4.6 s and a "2.4 s floor", where 8 October measured 3.25 s with the first checked sentence ready at 1.78 s.
- That leaves about 0.2 s for the voice. Pocket (0.16 to 0.23 s) would land at about 1.94 to 2.01 s, right on the line. This is an estimate, never measured.
- POCKET-CPU says the real path "cannot be measured yet", but September measured it:
  - F:/LedgerTools/latency/ingame-pocket2.json (26 September, in the game): median 2.02 s;
  - after-pocket.json (outside the game): 1.55 s, on the real model.
  - Both used an older, lighter check and a voice set aside on 26 and 28 September. Neither proves two seconds.
- Pocket's "first sound" is a fixed 0.16 s first chunk: a fragment, not necessarily meaningful speech.
- The opener run's 0.23 s and 2.81 s were taken with prepared openers on, in the editor, not the packaged build.
- Adopting Pocket would reopen RULINGS.md line 11 ("Not reopened: the voices in the game") and the 3 October voice choices.
- Pocket's frame cost has no silent run to compare against, so P2's "no more than 1 ms worse while speaking" is not shown. The card voice's slowest 1% on the walk, 27.66 ms, fails P2's under-25 ms line.
- "Slowest 1%" in these files is the mean of the worst 1% of frames, not the 99th percentile (21.53 and 17.19 ms for the two runs).
- The Gemini figures recompute exactly, but they are one check call per detail outside the game, not first sound, and their Haiku comparison is from 7 October.
- runs.jsonl starts with a byte-order mark, so a strict JSONL reader fails on line 1.

**Not reached.**
- talk-runs.jsonl holds costs and tokens only, no timings.
- The 7 October transcripts (F:/LedgerTools/tmp/builder/real-talk/...), the 6 October A/B run folders and the 8 October run's raw record are gone.

**Verdict.** Exit C does not pass: the two-second line is not met. The stop rule was invoked and reported (7 October), but under that rule a failure halts expansion; it is not a pass.

**Measured after the review (22 October, the maker).** The reviewer's estimate for Pocket on the real path (about 1.94 to 2.01 s) was tested: 20 checked replies, with the game open, gave a first sound heard of 2.41 s at the median (1.95 to 6.18). The first checked sentence alone took 2.10 s (POCKET-CPU-2026-10-21.md, "The real path with Pocket"). The verdict stands.
