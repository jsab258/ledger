# Judge proof: log

- 23 Nov 22:18: started (advisor's brief, his choice of 22:09). Read APPROACH judge sections, STORY-ANATOMY, READER-CHECK.
- 22:25: FORMAT.md (format and recipe v1). Four Sonnet helpers sourced 40 scenes (8 games, 20 admired, 20 forgettable), cited, rewritten.
- 22:35: screen 1, fresh Opus: game named for all 40. Recipe v2 (one shared world, set pieces swapped); four Sonnet rewriters.
- 22:40: screen 2, fresh Opus and Sonnet: 28 recognised. Third, clue-targeted pass on those 28.
- 22:45: screen 3: 22 recognised (12 admired, 10 forgettable), 18 clean. Famous scenes stay known by plot alone. Recognised scenes kept in the run, out of the pass mark (PLAN.md).
- 22:50: PLAN.md (pass mark) and BRIEF-v1.md committed before any judge ran.
- 22:49: half A (brief v1): 80 judgements a model. Clean pairs Opus 19/0/1, Sonnet 19/1/0. Passed.
- 22:50: half B as confirmation with brief v1, and a stakes-only control on half A (Sonnet). Half B clean Opus 19/0/1, Sonnet 17/0/3. Control 63% on clean pairs.
- 22:52: pooled result PASS (RESULTS.md). No mend needed. JUDGE-PROVEN.md and tools/ledger_pairs.py (build and score for LEDGER key scenes, smoke-tested on dummy outputs).
- 22:53: fresh Opus reviewer: does not stand as "proven". Must-fixes: label cues leaked into the rewrites (for example "the mood is routine", "no choice changes the result" in forgettable scenes); position and length must be measured on clean pairs as PLAN says; judge count wrong (16 judges, 8 a model, not 32); runs not committed; LOG times wrong; call it a screen.
- 22:56: blind scrub. One fresh Sonnet, given all 40 texts without labels, removed mood verdicts, commentary on the scene's importance and judgement adjectives, by one rule for all (changes per scene in set/scenes.json). The half A and B runs used the unscrubbed texts and are kept as the first result. Decision: re-run all 40 clean pairs on the scrubbed texts with the same brief and the same pass mark; the re-run is the result. Committed before the re-run.
- 22:58: clean re-run, 8 fresh judges: Opus 36/2/2 (94.7% of decided), Sonnet 34/3/3 (91.9%); position 52.5% and 53.8%; length 60.0% and 58.6% (Opus on the limit); agreement 90%. PASS as a screen. tools/ledger_pairs.py fixed (headings and length check, control rule stated, floor printed). RESULTS.md and JUDGE-PROVEN.md rewritten; "proven" dropped for "passed its mark, as a screen".
- 23:04: second fresh reviewer: numbers all correct; cut the untested 'it can tell' line and label the stakes control (done); ledger_pairs.py now picks shelf scenes within 25 words of the candidate. Finished.
