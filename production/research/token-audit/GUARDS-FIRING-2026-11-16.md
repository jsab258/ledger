# The three guards shown firing (n16-10), 16 Nov 2026, about 07:08

Method researched: advisor 162 and 163's guards as built (tools/fresh_gate.py, tools/token_measures.py, tools/c_root_guard.py, F:/LedgerTools/tool-dev/outpath.py), each run on its own fail cases.

- Output path: `checked("closeups/x.png")` and `checked("C:/x.png")` both refused ("OUTPATH REFUSED: ... is not absolute under F:/LedgerTools/ or C:/LedgerTools/", exit 3); `F:/LedgerTools/tool-dev/runs/x.png` passed. Self-test 8 of 8.
- C:'s root: self-test 6 of 6 (a new folder at the root fails the round). The live check today: "C-ROOT OK; C: 75.6 GB free (-3.0 since recorded) FELL OVER 1 GB": its free-space alarm fired for real (C: well above its 40 GB floor; the census since 20:00 shows the night's work: the build machine +4.2 GB, the project folder +4.4 GB, C:/LedgerTools +1.9 GB, all places retention covers).
- Model: fresh_gate's self-test passed 68 cases, including "model wrong, work due: GO and says MODEL WRONG" and "model wrong, no Next due line"; token_measures' row line fires "MODEL WRONG" on a Fable model (20 of 20). Live: this run's gate line carried no MODEL WRONG (Opus 5.5).

Not shown: a live C:-root fail (it would need a write at C:'s root, which no session may make).
