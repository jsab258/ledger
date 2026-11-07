# Exit C, rehearsal: fresh review, 7 November 2026

Recomputed from ask-script.json and talk-transcript.jsonl, F:/LedgerTools/latency/askreal-2026-11-04f and -07h, i, j, k.

## 22 October's faults

- 3.25 s best path: gone; these figures are packaged.
- Processor voice untimed beside checked talk: gone for Pocket (first words to sound, median 0.07 to 0.15 s; 3 of 150 lines over 0.25 s, worst 1.69, I13). A and B stay untimed, set aside.
- Prepared openings: none (opener -1 on all 150 rows).

## Verdict: MET WITH LISTED SHORTFALLS, narrowly

Median first sound, all 30 lines, then the 23 real questions (leaving out, on this reviewer's reading, greetings, quiet, smoke, rain):

- F, uncached, 4 Nov: 2.02; 2.03
- J, uncached: 2.42; 3.17
- H, cached: 2.035; 2.55
- I, cached: 1.675; 1.67
- K, cached: 1.58; 1.78
- **H, I, K pooled: 1.78 (56 of 90 at or under 2.0); 1.81 (39 of 69)**

The bar is read from H, I, K pooled: the talk that ships, one build. F and J are not shipped. The maker's table recomputes; "3 of 113 against 0 of 76" does not (raw: 3 of 90 lines, 0 of 60).

Shortfalls:

1. Not robust. H alone misses. Resampled 95% range, real questions: 1.67 to 2.24. All five pooled, real questions: 2.02, a miss. Caching's time gain is unshown: only J and K alternate; the check's cache saved nothing (cache-screen-2026-11-04).
2. Every model-written line came from the small-talk model. No held question matches TalkRules' concepts, so better-model questions ("how did Mickey die") went untimed. Run E, better model: 2.33 s, repeated questions.
3. Tail: 15 of 90 at 4 s or more; 4 timed out to a brush-off at about 8.2 s.
4. Fall-backs 3 of 90 against 0 of 60; all non-answers 7 of 90 against 7 of 60.
5. Some fast first sentences are not meaningful: "You're not Mickey's nephew, friend" (I21); "Quiet?" (K15).

## Gaps for Monday

- FINDINGS.md, NOW.md and IN-GAME still record the bar missed on run F.
- talk-runs.jsonl: no 7 November rows, no timings.
- P2's "1 ms worse while it speaks" unjudgeable: no runs.jsonl row says speech played. Voice up against off, 3641d53: median 12.00, 11.98; slowest 1% 23.84, 20.37.
- Logs name no commit; the copy's stamp reads 3b548c1 only. "Heard" is the game's timestamp, no recorded audio. Any talk change voids H, I, K.
