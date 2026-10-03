# Checked talk, measured in the finished game (3 October 2026, P3)

Jafar's order of 3 October: "P3: the claim check switches off when a spending cap wraps the talk client. Fix it, with a failing test first, then measure checked talk on the real path within the dollar-a-day measurement rule."

**The fix** (d3d0f48, packaged by the build machine at 14:26): the talk program attaches the claim check whenever the client underneath is the real one, a spending cap or not (`ChecksReplies`, its failing test first).

**The run.** The packaged game of d3d0f48 (F:/LedgerTools/played-game). The AI tester typed lines with real key presses (tools/ai-tester/play.py start --real-talk, the talk program's $0.50 cap). LEDGER's key was read only by the game's own talk. Today's voice (Chatterbox Nano on the graphics card) ran beside it, started from its installed copy, since the played copy has no voice folder of its own (P5 makes one).
- Run 1, 14:35: no voice. Three replies, then the walking between lines let the game's clock run to night, and Ron and Sheila went home.
- Run 2, 14:49: the voice on. Eight lines to Ron in a row; then the cap refused the paid calls, and Ron answered eight more with his written brush-offs.
- Sheila was never reached: T went to Ron each time.

## Every paid reply was checked

- All **11 of 11** paid replies went through the check: the talk program's own steps per reply (its transcript, F:/LedgerTools/tmp/builder/real-talk/2026-10-03-1435 and -1448/talk.jsonl). None came back unchecked, none fell back, none timed out.
- **The check caught something invented in 6 of the 11. None of it was said:**
  - four second drafts: Mickey's office "behind" Ron and Sheila "here now"; the pawn shop "just down the way"; Ron away from the rank in the mornings; the café "at the north end";
  - two replies cut to their checked first sentence: "the nephew would be along", "the warehouse burned right down".

## Timings (the session record's "heard": Enter pressed to the first words, and to the first sound)

| # | Enter to words (s) | to the voice asked (s) | to first sound (s) | how it went |
|---|---|---|---|---|
| 1 | 3.99 | 1.85 | 6.33 | passed first time |
| 2 | 6.07 | 6.07 | 10.48 | second draft |
| 3 | 3.21 | 7.21 | (7.88) | passed first time |
| 4 | 5.28 | 5.28 | 13.02 | second draft |
| 5 | 2.41 | 1.07 | 5.72 | cut to its first sentence |
| 6 | 2.09 | 1.00 | 4.29 | passed first time |
| 7 | 6.34 | 6.34 | 16.06 | second draft |
| 8 | 7.02 | 7.02 | (8.16) | second draft |

Lines 3 and 8 in brackets: their "first sound" is the previous answer's last sentence still playing when the next line was typed (the same voice work and length as the line before, no sound file of their own). That is a fault in the game's timing line, recorded in FINDINGS.md.

- **Enter to words:** median 4.64 s (2.09 to 7.02); run 1 without the voice, 4.72, 4.10 and 3.01. Unchecked on 30 September: 1.91.
- **Enter to first sound** (the six clean lines): median 8.4 s (4.29 to 16.06). Unchecked on 30 September: 5.41.
  - Passing first time: 5.7 s (4.29 to 6.33), the voice making the first sentence while it is checked. That is about the unchecked figure.
  - A second draft: 13.0 s (10.48 to 16.06). Half the replies needed one.
- **Within 2 s of Enter:** none of 8, as on 30 September.
- **At the cap,** Ron's written brush-off: words at once, first sound 1.2 to 3.0 s.

## What it costs

- **Run 2,** eight checked lines with Tom's suggested lines: $0.316 by the talk program's tally, $0.496 by the cap's own count. The cap keeps the worst case of drafts stopped part-way (the abandoned first drafts); the tally leaves them out. The truth lies between; the log takes the higher.
  - A checked line: **4 to 6 cents.** Unchecked on 30 September: 0.8 cents.
  - The $0.50 cap held eight lines. A friends' evening's $5 holds about 80.
- **Today's measurement spend:** $0.66 of the dollar (production/playtest/talk-runs.jsonl, both runs at the cap's figure). A third run would pass the dollar, so the sample stops at 11.

## Seen on the way (FINDINGS.md)

- The first letter typed into a talk box that has just opened lands at its end ("orning. You look like you know this street.M"), twice in two runs. Later lines in an open box were typed correctly.
- Sheila, Ron and Darren wear only the MetaHuman tool's white base layer (Sheila in a white T-shirt and shorts), which fails his clothes floor (the overview's Q3).
