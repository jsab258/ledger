# The accent check's window rule, calibrated on genuine English speech (29 September)

The question: the voice gate (tools/voice-live/take_gate.py) was changed on the
morning of 29 September to reject a take if any 2.5 s window of it read 0.30 or
more American on the project's accent classifier (CommonAccent, through
tools/voice-live/accent_check.py), after whole-take checks had let voices
through that drift inside a line. That rule had never been run on speech known
to be English. When new voices for Sheila were tried the same afternoon, three
of the four ten-second references (real northern English women from OpenSLR 83)
failed it.

## What was measured (tools/voice-live/accent_windows.py)

For each recording: the American share over the whole take; over 2.5 s windows
every 0.5 s, the worst window, the share of windows at 0.30 or more, and the
longest run of such windows in seconds.

- **Genuine English speech**: 50 clips of the five northern English women in
  OpenSLR 83 (ten each, 4 s or longer; CC BY-SA 4.0, on drive F). Whole take:
  median 0.00 American, but one clip reads 0.99. Worst window: median 0.03,
  90th percentile 0.74, maximum 1.00. Longest American run: 90th percentile
  2.5 s, maximum 4.5 s. **11 of the 50 fail the single-window rule.**
- **Speech the project had already judged American**: the 39 casting clips taken
  out on 25 September (voices designed from written descriptions, restored from
  git c2626975^ into scratch) and Pocket's rejected take of Sheila, 40 in all.
  Whole take: median 1.00 American; longest run median 5.2 s.

| rule | catches American | flags genuine English |
|---|---|---|
| any window at 0.30 (the rule of the morning) | 40 of 40 | 11 of 50 |
| a run over 2.5 s, or 0.5 over the whole take | 40 of 40 | 5 of 50 |
| **a run over 3 s, or 0.5 over the whole take** | **40 of 40** | **3 of 50** |
| a run over 4.5 s, or 0.5 over the whole take | 40 of 40 | 2 of 50 |

Taken: a run over 3 s or 0.5 over the whole take, the strictest rule that no
longer rejects one genuine English clip in five. Caveat: the American set was
labelled by the same classifier (whole takes), so the whole-take half is not an
independent test; the run half is what the calibration adds, and it keeps all
40 while dropping the false alarms from 22% to 6%.

## What changes

- Sheila's voice D: under the calibrated rule it still fails 4 of 7 lines (her
  sheet's three and the acting test's four, in the game's own voice engine):
  two read another accent over the whole take ("African" on the classifier),
  one has an American run over 3 s and one reads American throughout. At a 6%
  false alarm rate that is her voice, not the check.
- A new voice for her, nof_06136 (OpenSLR 83, a northern English woman), passes
  all seven.
- The morning's verdicts on the acting test's takes stand where they failed on
  runs over 3 s or whole takes; the recheck is in F:/LedgerTools/tmp/voxcpm-trial
  and nano-acting (*-calibrated.json).

## Sources

- OpenSLR 83, Crowdsourced high-quality UK and Ireland English Dialect speech
  data set (Google; Demirsahin, Kjartansson, Gutkin, Rivera, LREC 2020),
  https://www.openslr.org/83/, CC BY-SA 4.0; on this PC since 26 September.
- CommonAccent (Zuluaga-Gomez and others, 2023), the classifier in
  tools/voice-live/accent_check.py.

## New voices for Sheila, two attempts, and what they show

Both cloned by the game's own voice engine (Chatterbox Nano, tools/voice-live/speak_lines.py)
from real northern English women in OpenSLR 83, and gated with the calibrated rule on her
sheet's three lines and the acting test's four:

1. From ten-second references of two clips each: nof_06136 passed all seven, but a blind
   reviewer (who measured what it could not hear) found it far higher than its own
   reference (median 228 to 269 Hz against 198; five pitch jumps to 400 Hz and more) and
   quick (up to 6.7 syllables a second), not the sheet's "low, dry, unhurried"; the
   reference held only about 5 s of speech. D, the same seven lines, failed 4 (confirmed).
2. From references rebuilt of 14 to 15 s of calm, continuous speech: nof_03397 came out
   low (median 186 to 206 Hz) but off English on 4 of 7 lines (three American, one
   "African"); nof_06136 off English on 2 of 7 (Australian, Irish), still high on some.

Every voice tried for her, designed or real, drifts off English in the engine on some
lines; the references themselves read English. So the engine is the limit, not the
voice: Sheila's voice waits on the paid-voice decision (Jafar's list, item 6), and new
candidates through Nano stop here under the two-attempt rule.
