# n09-10: fresh first-round review of the two skill additions (8 Nov 2026)

Reviewer: fresh, read-only. Checked against: the builder's note, DECISIONS 27 Oct 05:37 and 06:22, 30 Oct 11:50 and 14:20, 8 Nov 16:30, the dress-the-cast line of 4 Nov, commit 0b2621d00, ue-probe LedgerGarments.h, CrimeProbe.cpp, tools/launch_line_check.py, tools/garments_shipped_check.py, tools/ue/stage_game_data.py, production/specs/mickeys-office.json, RECIPE 27 Oct.

## Verdict: pass with fixes (4 faults, all small; none is a wrong fact)

Confirmed as the sources say: "who", "name", "hides", "raise_mm", "soles" fields; garments.json in stage_game_data.py's list; the log lines "wears", "held back" and "NOT worn (not in this copy of the game)"; the "hold" field and -WearHeld=Name,Name; -WearHeld in no allowed list of launch_line_check.py (an unknown switch reads TEST); verdict words PLAYER and PLAYER+WATCH; the output line garmentsShipped=PASS; the commit's hold-to-released change on the four Ron and Darren jumper and jeans rows; local_exposure 0.6 and 0.6 read by CrimeProbe.cpp; all three office views passing; the radio-shelf shadow set aside after two tries; the "re-shoot every view" and "two tries" lines match RECIPE 27 Oct. No contradiction with RULINGS.md found.

## Faults

1. .claude/skills/game-garment/SKILL.md, step 2 "tools/ue/import_garments.py in C:/LedgerTools/mh-assemble": missing how it is run (the LEDGER_MH_SCRIPT=import_garments setting and the editor opened on the mh-assemble project, unattended, as the script's docstring gives it), and "step 9" does not give it either; a first-time reader cannot do the import from this section. Source: tools/ue/import_garments.py docstring lines 1-5.
2. .claude/skills/game-garment/SKILL.md, step 4 "When the hold's conditions are met ... the row's 'hold' becomes 'released'": on 8 Nov the release came before the packaged walk, which the hold itself named as a condition ("until a packaged walk and his page"), and the sentence does not say so; it reads as if all conditions were met. The commit message says the walk is "the hold's last condition". Also unsaid: nothing in LedgerGarments.h reads "released"; only the absence of "hold" matters. Source: commit 0b2621d00 message; LedgerGarments.h line 284.
3. .claude/skills/game-garment/SKILL.md, step 4 check "the next walk's launch_line_check says PLAYER or PLAYER+WATCH": the command is not given (python tools/launch_line_check.py LOG, one game log per argument); step 3 and step 4 also never say that a -WearHeld picture can never serve as the pass evidence beyond "reads TEST", e.g. that the film for his page may use it but the night walk must not. Source: tools/launch_line_check.py docstring lines 2-6.
4. .claude/skills/street-weathering/SKILL.md, step 6 new bullet "(the shadow under the radio shelf ...)" and "Values for another room: check first": town detail (office, radio shelf) sits in the method text rather than only in data and the spec; and "check first" does not say what to check (the room's own spec key, a burned-pixel count before and after, as the office's local_exposure_note does: 2,316 to 4,907 to 1,753). Source: production/specs/mickeys-office.json "local_exposure_note"; RECIPE 27 Oct (setting-free wording there).

## Not checked or open

- Step 5 of the new section says whether the released men passed the 8 Nov night walk is unrecorded; that is honest and was not resolvable here.
- The page names "dressed-men-look" and "knit-jumpers-look" and the times 06:41 and 13:12 are taken from the DECISIONS 8 Nov 16:30 entry; the page store itself was not read.
- Build 3b3454e appears in DECISIONS 8 Nov 16:30; the review.json it cites on F: was not opened.
- The trigger words added to both descriptions match the sections they point to; no fault found.
