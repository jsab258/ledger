# Phase 1's exit re-checked, Exit C (the voice and the speech line): the fresh review, 9 November 2026

One fresh final reviewer (Opus), read only. Given CLOSE-BRIEF-2026-11-09.md (Exit C), the 22 October requirement, CLOSE-2026-10-22.md and CLOSE-C-REVIEW-2026-10-22.md; not the rehearsal files or other exit reviews. Every figure below is recomputed from the raw files (ask-script.json, talk-transcript.jsonl, LedgerProbe.log in F:/LedgerTools/latency/askreal-2026-11-04f and -07h, i, j, k; runs.jsonl). The bar (RULINGS.md, Speech): median first meaningful speech 2.0 s or less on a newcomer's real questions, no prepared openings; small talk beside, never instead.

## The 22 October faults

- **Measured outside the game, not heard in it: gone.** Runs F and H to K are inside the packaged copy (logs: "LedgerTalk: live, on LEDGER's own key", "LedgerVoice: ready, Pocket voices" for all three), live checked talk, no walk-away lines, budget never refused, opener -1.00 on all 150 lines (no prepared openings).
- **Processor voice never timed beside checked talk: gone.** Pocket is timed on live, checked replies.
- **3.25 s against 2.0 s: much reduced, not cleared.** See below.
- **No raw record survives: gone.** All five runs keep their raw files.
- **Pocket's frame cost with no silent run to compare against: partly open.** Build 3641d53: voice program up but silent (gamenovoice a to e) slowest 1% 20.3 to 20.7 ms, worst 22 to 25, none over 33.3; speaking (lazy a to e) 22.4 to 24.2 ms, worst 26 to 38, 4 frames over in 5 walks; medians equal (11.9 to 12.1). Newest measured build 3b3454e (-sun, speaking): median 11.83, slowest 1% 23.86, worst 32.03, none over; no silent arm on that build. Speaking costs nothing at the median and about 2 to 4 ms in the slowest 1% where both arms exist.

## The bar, from the raw files

| Run (build) | Talk | Median first sound | At or under 2.0 s | 4 s or more | Worst |
|---|---|---|---|---|---|
| F (6c808a1) | not cached | 2.02 | 14 of 30 | 7 | 8.22 |
| H (e998e06) | cached (as shipped) | 2.035 | 14 | 6 | 8.21 |
| I | cached | 1.675 | 21 (20 meaningful) | 5 | 8.26 |
| J | not cached | 2.42 | 14 | 8 | 8.22 |
| K | cached | 1.58 | 21 | 4 | 8.22 |

The maker's table matches, except H's median (2.035, written 2.04) and I's count (21 at or under, one an exact 2.00 s fall-back). The shipped talk caches (TalkHelper/Program.cs line 1596, on unless LEDGER_TALK_CACHE=0); no talk code changed between e998e06 and the newest build 5ed8f38 or HEAD (git log on ledger/TalkHelper and Assets/Scripts/Core).

- Shipped talk, three runs pooled: 90 lines, median 1.78 s, 56 at or under 2.0 s, 15 at 4 s or more.
- All five runs pooled (the cache's screen of 4 Nov saved no check time, so cached and not are likely one population): 150 lines, median 1.89 s.
- Taking out the four lines of the held set that are greetings or small talk ("Morning. I'm Tom...", "Is it always this quiet?", "Mind if I smoke?", "Does it ever stop raining here?"; this reviewer's split, the question order assumed from -AskSet, the log not naming the text): shipped 75 lines, 1.78 s; all five runs, 125 lines, 1.97 s.
- Counting timed-out brush-offs ("Later, yeah? There's a fella waiting on me" at 8.2 s) and plain fall-backs as no meaningful speech leaves every median unchanged.

**Judgement.** The bar's own measure, agreed before it ran (run F, his yes of 4 November), missed it at 2.02 s. The later runs were a cost lever, not a try. On one build and one talk program, single runs range 1.58 to 2.04 s cached and 2.42 s not; the pooled medians (1.78 to 1.97 s) sit under the line by less than the spread between runs. One of three shipped-talk runs misses on its own. The figures show speech near the line, not past it. **A missed bar stays missed.**

## New since 22 October

- **The tail (shortfall, not new in kind).** Every run has a worst line of 8.2 s (the 8 s limit). 30 of 150 lines took 4 s or more. One question, "Where's the nearest phone box?", has a median of 6.69 s over its five asks (5.87 to 8.22). 10 of 150 replies are timed-out brush-offs, 3 are fall-backs (H 1, I 2; F and J none).
- **The voice is now and then the delay (new, narrow).** Of 150 lines, first words to first sound are within 0.17 s, except three: I line 13 1.69 s, J line 21 0.99 s, I line 10 0.44 s. The maker's "the voice is not the delay" holds for 147 of 150.
- **No speech run on the newest build** (5ed8f38, 8 Nov). The talk code is unchanged since the runs; the game around it is not. Unmeasured, not a fault.
- **Every newcomer question goes to the small-talk model** (Haiku 4.5 on all model-written replies in F to K). The held set is the bar's own; whether a newcomer's harder questions would go to Sonnet 5 and run slower (run E: 2.33 s on Sonnet 5) is not shown.
- talk-runs.jsonl holds cost only, no timings (as on 22 October).

## Verdict: NOT MET

Shortfalls, each with its evidence:
1. Median first speech: the agreed run F 2.02 s against 2.0 s; one of three shipped-talk runs over (H 2.035 s); pooled 1.78 to 1.97 s, inside the run-to-run spread (askreal-2026-11-04f, -07h to k, ask-script.json).
2. Tail: 15 of 90 shipped-talk lines at 4 s or more, 8.2 s worst in every run (same files).
3. Voice frame cost: speaking adds about 2 to 4 ms to the slowest 1% where a silent arm exists; no silent arm on the newest measured build (runs.jsonl, 3641d53 gamenovoice and lazy rows; 3b3454e -sun rows).
4. No speech run on the newest packaged build, 5ed8f38.
