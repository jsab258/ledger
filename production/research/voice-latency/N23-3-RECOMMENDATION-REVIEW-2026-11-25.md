# n23-3 recommendation: fresh review (25 Nov 2026)

Checked: N23-3-RECOMMENDATION-2026-11-25.md against N23-3-QUESTIONS, the five raw run folders (ask-script.json, talk.jsonl, recomputed in Python), order item n23-3, RULINGS (1 Oct, 12 Nov, 23 Sep/24 Nov, Speech) and the code. Read only.

**Verdict: pass with fixes.**

## Numbers recomputed
- Medians, under-2.0 s counts, 90th (nearest rank) and worst all match for every row: 1.59/19/5.66/8.24; 1.73/17/6.67/8.23; 5.335/1/8.22/8.27; 1.705/17/6.54/8.23; 2.63/8/7.57/7.67; 1.855/17/4.57/7.56.
- Lines not live: Haiku 4.5 (05:53) 3 = 1 fall-back + 2 time-out brush-offs, correct as "lines lost". Sonnet 5.5 with thinking: **0 fall-backs, 5 time-out brush-offs**. The table's "Fall-backs 5/30" mislabels these.
- Fast-first's 8 are 5 redraft first sentences flagged, 1 time-out brush-off during the redraft and 2 paused by the cap. The table and QUESTIONS say "6 flagged", and QUESTIONS' own list adds up to 9.
- First written: thinking on 3202 ms, correct but from **only 11 of 30 turns** (the slow ones timed out, so it is likely low). Thinking lowest 1241 ms over 30 entries, or 1188 over the 25 live lines, not 1276/1.28. Haiku 4.5: 674 ms (0.67, not 0.68). Haiku 5.5: 720, matches.
- Voice share (first heard minus first words): the three runs quoted give 0.015-0.055 s. But Sonnet 5.5 with thinking reads a 0.145 s median, and with thinking lowest the worst is 0.52 s. The conclusion stands; the range quoted is too narrow.
- Code facts confirmed: the switch is default off and sets ReplyThinkingOff. AcceptsThinkingOff covers Sonnet 5 and the Haiku models, and Sonnet 5.5 gets "between_tools". Models.Core is Sonnet 5, Ambient is Haiku 4.5. The Program.cs switch is still uncommitted.

## Fixes
1. Recommendation 1: "the only arm under the 2 s bar on the median" is false. Fast-first (1.71) and Haiku 5.5 (1.85) are also under. The case for Haiku 4.5 is the most lines under 2 s and the fewest lost, one run each.
2. Correct the table: the thinking-on row has 5 time-outs, not fall-backs. Fast-first is 5 flagged, 1 time-out, 2 cap. First written with thinking lowest is 1.24 s, with thinking 3.20 s from 11 turns, and that caveat must be stated.
3. Recommendation 4 over-reaches. It was measured on the held newcomer questions forced into the conversation path on Sonnet 5.5, not on real-conversation moments, and not on shipped Sonnet 5. Lines not live stayed at 5: time-outs went 5 to 0 while written fall-backs went 0 to 4. Say both.
4. Recommendation 3: Sonnet 5 was never measured inside the game, with thinking on or off. Say so plainly.
5. Rulings: the Speech ruling sets the 2 s bar on a newcomer's real questions, with small talk "beside, never instead". The game routes those questions as small talk by the 1 Oct moment rule, so the bar is met only on the light path. The recommendation should name this tension. If the rulings do not settle whether such questions are real conversation, it is his question.
6. Order still open: "lines recorded for his ear later" is not done, and needs a plan before 4 Dec. Cost is bench-only: the talk transcripts carry no usd and in-game spend is logged only as cap upper bounds. Mark it as such.
7. Narrow: widen the voice range (median up to 0.15 s, worst 0.52 s). The 12 Nov monthly check runs on the talk bench, so the plan to run Haiku 5.5 "as small talk" on 7 Dec should say on the bench or in the game. Commit the switch before the recommendation is cited.

Nothing stated as measured was found unmeasured, apart from the caveats above.
