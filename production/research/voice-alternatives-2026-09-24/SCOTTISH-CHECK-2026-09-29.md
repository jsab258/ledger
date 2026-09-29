# The accent check on Scottish speech, and Darren through Sopro: measurement, 29 September 2026

The research note ACCENT-KEEPING-2026-09-29.md found the accent check (tools/voice-live/take_gate.py, CommonAccent) calibrated on northern English women but never on genuine Scottish speech. Measured here.

**Genuine Scottish men** (OpenSLR 83 scottish_english_male, CC BY-SA 4.0, on drive F for measurement only; 50 clips of 4 s or longer across its 11 speakers, `--want scotland`, likeness ignored as the speakers differ): 26 of 50 pass on accent; 15 fail as American (mostly the window rule), 8 read as England, 1 Australia, 1 New Zealand. The check cannot judge "Scottish": it fails about half of real Scotsmen.

**Darren's approved voice** (Chatterbox Nano, the game's engine, on the processor; twelve new lines): 0 of 12 read as Scotland (10 England or Australia; 2 American by the window rule only, whole-take American 0.00 and 0.36). **Sopro** (attempt 2's settings: temperature 0.5, top-k 15, his approved in-game line added to the reference), the same twelve lines: 1 of 12 reads Scotland; 4 American, three of them whole takes at 0.93 to 1.00.

**Reading.** For Darren the check can only be used relatively: against his approved Nano voice, Sopro drifts plainly American on a third of the lines. Sopro's third attempt for Darren fails: set aside under the two-tries rule; Darren stays on Nano. For a Scottish voice the gate needs ears or a better classifier (FINDINGS).

Files: F:/LedgerTools/tmp/scots-calib/genuine-report.json, F:/LedgerTools/tmp/darren16/{darren-milner,nano}-report.json and their -gate.json.
