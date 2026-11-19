# Review 06: Kiln and the tools (full audit, 19 November 2026)

One fresh reviewer, read only. Sources: Kiln's notes, round reports, evaluation, plans and reviews in production/research/tool-tests-2026-11/ and production/lane/, DECISIONS.md, RULINGS.md, NOW.md, the handover, production/time-log.jsonl, the token audits, tools/ (all 157 top-level scripts mapped against the git hooks, .claude/settings.json, .github/workflows and tools/ci-checks.sh), the GitHub Actions run history (read only, through gh), production/rulings-enforcers.json and production/audits/full-2026-11/pc-inventory.json. Kiln's own code, LOOP.md and the v1 checklist live on F: on his PC and were not readable from here; every claim about them below comes from repository records that quote them.

## Summary

Kiln is meant to be the clothing tool that lets LEDGER dress its whole cast without Marvelous Designer, and clothing on people does serve the immersive game he asked for. But in six days (13 to 19 Nov) Kiln grew from "at most 15% of a week" to "everything else serves it or waits", and it has not yet put one garment into the game: Kiln v1 is 0 of 6 lines, M5 and M6 are not reached, the M7 count is 0, and the cost-per-garment table is still empty, so the checkpoint rule that should park it if it saves nothing cannot even be applied today. Its early "milestones met" rested on an engine whose stiffness turned out to be about forty hand-set solver counts tuned to land just under the bars. The professional method was researched only after nine rounds. The same engine was the Drape Studio engine, which the design note had ruled out on the day it was adopted. On the tools side the picture is many checks, little enforcement. The cloud test job has been red on 544 pushes in a row since 29 October, and nobody has written it down. 62 of the 85 ruling lines lean on a Monday audit that has never run. A new hook is quietly corrupting the time log that the 1 February cost check depends on. Two Kiln-share tools give opposite verdicts, and the stated caps disagree with the cap tool. Kiln alone holds about 24 GB on C:, and C: is below its floor. Findings: 4 high, 5 medium, 2 low.

## Findings, ranked

### 1. Kiln's "milestones met" rested on a method nobody had researched (high)

Impact: high for the game and for him. His 70% pick of 17 Nov and the Thursday checkpoint both rest on M2 to M4 being met. The method review later showed those passes were tuned counts, and step 4 says they "will not hold".

Evidence:
- Round 3 (13 Nov) adopted the Drape Studio engine because its look passed, "decided: the look decides, and only this path passed" (production/research/tool-tests-2026-11/KILN-ROUND1-2026-11-13.md line 92). Round 1 had already found that "every measured bar passes, the look fails" (same file, Round 1 verdict).
- On 15 Nov the evaluation for him said "The checkpoint (M3 by about 22 Nov) was passed eight days early" (KILN-EVALUATION-2026-11-16.md line 15), while line 30 admits "Marvelous still looks better close up".
- The method review came on 16 Nov, after nine rounds. It found: "Kiln's drape engine has no material stiffness of its own: every stiffness in it is a count of solver passes" (KILN-METHOD-REVIEW-2026-11-16.md line 9). It also found "Why the counts sit just under the bars" (line 48), and that step 4 "moves everything at once ... M2 to M4 will not hold byte for byte" (line 75).
- What it cost afterwards: step 4 capped at 32 h (DECISIONS.md line 282); a 15 to 20 h re-tune plan (KILN-RETUNE-PLAN-2026-11-17.md section 5); stiffness tries "2/2 (Fable)" failed (production/handover/HANDOVER.md line 62; TRIED-ARCHIVE.md line 105).
- CLAUDE.md requires "the professional method end to end, dated, before any symptom". The design note's "Method researched" line read only the four tools' own sources (TOOLCHAIN-CORE-DESIGN-2026-11-13.md line 1), never the cloth-simulation literature (XPBD, VBD).

Proposed end: rule. Before any tool adopts or switches an engine or solver, a dated method review of the professional technique is written and reviewed. No milestone is reported to him as "met" until held-back jobs pass on the same run and a reviewer has compared it with the references by eye.

### 2. Six days of Kiln, no garment in the game, and no savings measured for the checkpoint (high)

Impact: high on money, scope and his attention. Today's checkpoint and the Marvelous renewal ($39 a month, last safe stop on 24 Nov) have to be decided without the one number the ruling asks for.

Evidence:
- How the share grew: 15% on 13 Nov (design note line 10; RULINGS.md line 39); about 23% in the order (production/orders/2026-11-16.md line 15); 70% on 17 Nov (production/week-shape.json "kiln_share": 70); then "Kiln v1 by Mon 23 Nov 13:00; everything else serves it or waits" (HANDOVER.md line 11).
- Where it stands: "Kiln v1 0 of 6"; the coat blocked; paused by the guard (NOW.md line 14). M5 and M6 "not started" (KILN-EVALUATION-2026-11-16.md, milestones table; KILN-PARITY-LIST-2026-11-16.md: "M7 count: 0"). The garment closest to the game, Ron's trousers, sits on an unpushed local branch (DECISIONS.md lines 354, 361) and has not been packaged or walked.
- Cost recorded: 28.8 h of session time logged on Kiln tasks from 13 to 18 Nov (time-log.jsonl, rows naming kiln, tool loop or n16-1, the automatic rows of finding 5 left out). Helpers are not in the time log. Kiln took 27.3% of the week's spend at 18 Nov 02:55 (DECISIONS.md line 353). The day's spend was US$153, US$327 and US$503 on 16 to 18 Nov at list price, which measures usage, not his bill (DAILY-2026-11-16.md line 43; DAILY-2026-11-18.md line 7). Another 6.1 h went on testing his other tools, 11 to 13 Nov.
- The savings rule: "no savings by its checkpoint parks it" (RULINGS.md line 39). Yet every Kiln row in the cost-per-garment table still reads "job written, drape not run" (TOOLCHAIN-CORE-DESIGN-2026-11-13.md lines 57 to 60).
- His own stance on 13 Nov was that Kiln must not become its own project (his memory record, 13 Nov). RULINGS line 39 still says "game never waits on it", while the order item for Ron as a complete person (n16-2) waits on Kiln.

Proposed end: ruling for him (money and scope). At today's checkpoint, which way? (A, recommended) Keep Marvelous one more month ($39), cut Kiln back to 15% until Ron walks the packaged game in one Kiln garment with its hours and cost filled in, and resume the other order items. (B) Keep Kiln at 70% to Monday and let Marvelous lapse on 25 Nov. (C) Park Kiln and dress the cast through Marvelous.

### 3. Kiln's engine is Drape Studio's, against Kiln's own design note, and licence questions went to him against his written word (high)

Impact: high. Kiln carried values taken from a decompiled commercial program for five days without anyone noticing. Cleaning it up cost a night of helper lanes, and two page items took his attention on a point he had already settled.

Evidence:
- 10 Nov: the studio recorded that Drape Studio was built by "decompiling it and taking 59 of 82 values from Marvelous's preset files" (DECISIONS.md line 34). He answered that it is his own tool, to be tested with "no licence check, his written word" (line 36).
- 13 Nov design note: "Nothing of Drape Studio's engine, presets or files is copied" (TOOLCHAIN-CORE-DESIGN-2026-11-13.md line 23). The same line still sends "Copying its interface is a licence question that is his" to him "as one tap".
- 13 Nov round 2 copied "Drape Studio's solver ... into kiln/engines/drapestudio", and round 3 made it the drape engine (KILN-ROUND1-2026-11-13.md, Round 2 "What was tried" and line 92). The design note was never updated. Kiln's default program is "cargo-target/kiln/release/drape-studio.exe" (production/research/disk/KILN-DISK-2026-11-17.md section 1).
- 18 Nov 03:13 to 03:14, five days later: "Kiln's engine is the Drape Studio engine", with "78 address references" to decompiled code (DECISIONS.md lines 358 and 359). A 58-row list followed, a "28 helper h" plan, and replacement by 09:30 (lines 364, 368, 402).
- 18 Nov 12:13, his message: the interface "is his own tool, not a licence"; both page items withdrawn (DECISIONS.md line 414).

Proposed end: rule. Any change of a tool's base or engine reopens its design note and the note's review the same day, and each round report names the engine source path beside the note's exclusions. His own tools are never put to him as licence questions (his word of 10 Nov). needs_you_page.py's category check enforces this only in part.

### 4. The cloud test job has been red on every push for three weeks, and no record says so (high)

Impact: high. All the cheap checks that enforce his rulings run in this job. Red every time, it can no longer tell a real fault from noise, which is exactly the failure its own header describes.

Evidence:
- "LEDGER core tests": last green on 29 Oct at 06:39 (wip). Since then 544 runs in a row have failed: 463 on wip, 81 on lane-2026-11 (gh run list, read 19 Nov).
- The newest wip run: "passed=96/107 failed=brick-ids-selftest, needs-you-selftest, stain-check-selftest, surface-values-selftest, cuff-faults-selftest, build-cuffs-selftest, chart-read-selftest, wet-ground-selftest, film-webp-selftest, spec-test, retention-selftest". Most fail with "No module named 'numpy'" or "'PIL'" on the cloud runner. One is a real fault: "a drawn surface the sidecar names is on disk : production/assets/street/surfaces/cover_iron". The first red, on 29 Oct, was one check (stain-check-selftest).
- tools/ci-checks.sh header: "Six checks reporting NOTHING looked exactly like six checks reporting fine".
- CLAUDE.md: "never on a failing check". HOURLY-TASK.md: "push to wip only when the checks end failed=none". tools/hooks/pre-push runs only push_guard.py and order_ledger.py, not ci-checks. FINDINGS.md, NOW.md, the handover and DECISIONS.md never mention the red job.

Proposed end: list item: install numpy and Pillow in .github/workflows/ledger-core-tests.yml (or mark the PC-only checks plainly), fix the missing cover_iron surface and the retention selftest, and get back to green. Then a rule: a red core-tests run on wip becomes a FINDINGS.md line within the hour, and the hourly row reports the job's state.

### 5. The new session-start hook corrupts the time log the 1 February cost check needs (medium)

Impact: medium. The time log is the only source for hours per item and Kiln's share. On 18 Nov it booked about 9.5 h to Kiln as "session startup" and cut real tasks short.

Evidence:
- tools/lane/item_tags.py hook_session (lines 116 to 131) writes a "start" row at every session start. It skips only compactions and resumes. .claude/settings.json runs it on SessionStart, switched on 18 Nov 12:27 (commit 44099988f).
- The gate now starts a session every 15 minutes (DAILY-2026-11-17.md line 35: "the 15-minute start"). The result on 18 Nov: 43 rows "n16-1 session startup (auto)" between 12:15 and 22:36, from 43 different sessions. Each one closes the open task. "n16-1 Kiln v1 lanes: eight helpers briefed", started at 12:33, was cut to about 2 minutes by the 12:35 row.
- The module's own docstring says token_audit "closes the open task on ANY time-log line", which is why it keeps helper rows out of the log (lines 17 to 19). Session rows do the same thing.

Proposed end: list item: write the row only when fresh_gate says GO (never on WAIT starts), close it on the session's stop, and rebuild 18 Nov's windows from the session logs.

### 6. Most rulings have no working enforcer (medium)

Impact: medium. He was told that every standing ruling names its enforcer (advisor 205). In practice most rest on judgement, on a job that has never run, or on the red job of finding 4.

Evidence:
- production/rulings-enforcers.json: 85 ruling lines. 62 name "monday-audit", whose first run is Monday 23 Nov (production/audits/full-2026-11/work/scheduled-tasks-2026-11-19.md, item 3). 35 lines name no tool at all. Of the named tools, 11 run from no hook, CI or workflow, among them settings_check.py (named 5 times), pace_line.py (4), token_measures.py (3), api_batch.py and voice-cast-check.py.
- Of the 107 checks in tools/ci-checks.sh, 67 are selftests: the checkers checking themselves, not the project.
- Of 157 top-level scripts in tools/, 70 are wired to something (CI, git hooks, Claude hooks, workflows or the hourly task); 87 run only by hand or never; 56 of those have not changed since before 20 Oct.
- The Fable cap check (item_tags.py fable_refusal) reads production/handover/pace-state.json, which is gitignored, and allows the helper when the file is missing or unreadable, so it fails open.
- Kiln's own code (the week's biggest product) is outside the repository, in F:/LedgerTools/tool-dev/kiln, backed up only as a Dropbox bundle (tools/backup-to-dropbox.py line 59). Apart from outside_only_check.py's name scan, no repository check reads it.

Proposed end: rule. A ruling counts as enforced only when its check runs on its own (hook, CI or scheduled task) and is currently green. rulings_check.py reports enforced lines by that test, and the hourly row carries that count beside "monday-audit only".

### 7. Tools contradict each other and the records (medium)

Impact: medium. The sessions get opposite verdicts on the same question, and CLAUDE.md teaches the wrong number.

Evidence:
- Kiln share: item_tags.py kiln-share fails over a fixed `KILN_CAP = 15.0` (tools/lane/item_tags.py lines 57 and 329), while token_measures.py --kiln-share reads 70 from week-shape.json for this week (tools/token_measures.py lines 565 to 578). At 27% one says "KILN OVER 15%" and exits 1; the other passes.
- Caps: CLAUDE.md line 31 says "this file 1,000", while tools/doc-caps.py line 31 sets CLAUDE.md at 1,625 (the file is 1,622 words). Every capped file sits at its cap: RULINGS.md 4,899 of 4,900, FINDINGS.md 2,000 of 2,000, NOW.md 195 of 200, CLAUDE.md 1,622 of 1,625. That suggests trimming to fit rather than pruning.
- Tries: CLAUDE.md line 53 says "a third try needs his yes first". RULINGS.md line 27 allows "up to four", and the handover tells sessions to "correct" helpers who quote CLAUDE.md (HANDOVER.md line 29). Kiln's tries on 18 Nov ran under the RULINGS count (HANDOVER.md line 62).

Proposed end: list item: make item_tags read the week's share through token_measures.kiln_cap, and update CLAUDE.md's cap figure and tries line from RULINGS. Then a rule: when a ruling changes a number, the same commit updates every tool constant and every CLAUDE.md line that carries it (doc-caps or rulings_check to fail on a mismatch).

### 8. Kiln holds about 24 GB on C:, and C: is below its floor (medium)

Impact: medium. A full or near-full C: stops builds, and his rule is "nothing large on C:".

Evidence:
- pc-inventory.json (19 Nov 00:56): C:\LedgerTools\cargo-target 19.78 GB, C:\LedgerTools\kiln-lanes 4.09 GB, C:\LedgerTools\kiln-runs 0.29 GB (named by nothing). Together that is about half of C:\LedgerTools (48.9 GB). C: had 37.41 GB free, against a floor of 40 (RULINGS.md line 123).
- cargo-target was 11.3 GB on 17 Nov (KILN-DISK-2026-11-17.md section 1) and nearly doubled in two days: one Rust build folder per lane and per gate.

Proposed end: list item: one shared build folder for Kiln's lanes with a size limit in retention.json, kiln-runs added to the storage map, old lane targets pruned through retention.py, and Kiln's build folder moved to F: when there is room.

### 9. What he raised himself about Kiln, and what should have caught it first (medium)

Impact: medium on his attention. Each of these was a gap in the studio's own design review that he had to close by message.

Evidence (dates from DECISIONS.md, the design note and DECISIONS-TRACE.md, checked against DECISIONS.md):
- 14 Nov 08:32: "no special cases" and held-back jobs, so that Kiln is not taught to the test (design note, "Breadth by design"). The studio's design review of 13 Nov (TOOLCHAIN-CORE-DESIGN-REVIEW-2026-11-13.md) has no word on held-back jobs or overfitting. Finding 1 shows the risk was real.
- 14 Nov 12:33: M7, a finish line tied to the Hook's garment list, "so that 'fully working' is measured" (design note, M7). Until then Kiln's milestones ended at one outfit.
- 16 Nov 10:16: "massive Kiln progress expected; it must turn into game progress soon" (DECISIONS-TRACE line 184).
- 17 Nov 22:12: Kiln's efficiency as a product, measured per garment (DECISIONS.md line 340). His 11 Nov philosophy already asked for efficiency checks "on their own". The design note had a cost goal (line 9) but no measure until he asked, and the table is still empty (finding 2).
- 18 Nov 12:13: licence items about his own tool, against his word of 10 Nov (finding 3).

The check that should have caught these: the fresh review of the design note on 13 Nov, if it had been asked to check the note against RULINGS (efficiency, the game item each piece unblocks) and against the risk of tuning to the test.

Proposed end: rule. Every new tool or module's design note carries, from day one, held-back jobs, a finish line drawn from the game's own list, and cost per item measured in every round. Its fresh reviewer checks those three against RULINGS before the first round.

### 10. Dead tools that can go (low)

Impact: low. They cost a little at each search and blur what "the tools" are.

Evidence: nothing outside themselves names these, and their subjects are retired. town_page.py and town_day_page.py are the Town session's pages; the Town session became bounded tasks on 1 Nov, and town_day_page.py alone has 43 commits. suit_page.py, casting_pictures.py, report-frame.py and test-blender-hash-parse.py each have zero references. gamecheck.py and its eight lint-*.py scripts date from August, are wired to nothing, and ci-checks.sh dropped them. weekend_page.py is used only as a model inside day_page.py and candidate_page.py. All were made by Claude.

Proposed end: deletion. Move these to legacy/ (or delete them, under RULINGS 29 Oct: Claude-made, nothing uses them), with one DECISIONS line. This is safe because no hook, workflow, CI entry or other tool calls them (checked against all four on 19 Nov). If the C# lint rules are still wanted for ledger/, add gamecheck.py to ci-checks instead of keeping it idle.

### 11. The stage 1 PC inventory's "named by" column is unreliable (low)

Impact: low. It feeds deletion and keep decisions.

Evidence: pc-inventory.json matches folder names as plain text, so F:\LedgerTools\tool-dev\reports counts as "named by" tools/body-proportions.py, tools/clip-from-frames.py and tools/container-setup.sh, and tool-dev\vendor as named by tools/attribution-check.py, tools/brand-verify.py and others. None of those refer to those folders. Meanwhile C:\LedgerTools\kiln-runs, which Kiln writes, is "named by nothing" (INVENTORY.md line 337).

Proposed end: rule. The inventory matches full paths, never a bare folder name, before its counts are used for any deletion.

## The brief's seven questions, in short

1. Same game: clothing serves the immersion he wants; Kiln's wider plans (overnight wardrobes; props, buildings, motion and sound modules) point at a studio toolchain, held back only on paper by his 18 Nov "three proofs first".
2. Still true: no (findings 1, 3, 7).
3. Used: Kiln heavily, with no garment in the game; 87 of 157 tools by hand or never; the CI verdict ignored for three weeks.
4. Cost: 28.8 h logged on Kiln plus helpers; 27.3% of the week's spend on 18 Nov; about 24 GB on C:; his attention as in finding 9; hours and dollars per garment not recorded.
5. Missing: cost per garment, a held-back result, a green CI, working enforcers, Kiln's code in any reviewed place.
6. Contradictions: findings 3 and 7. 7. Raised by him first: finding 9.
