# Risk register for the whole game: draft (18 November 2026)

Blind-spots recommendation 9, adopted 18 Nov. Draft by the cloud lane, not yet reviewed. It would replace production/research/pre-production/6-RISKS.md, which covers only the thirty-minute friends' build and was last reviewed 5 Oct.

The aim at risk: one full release late in 2027, 15 to 20 hours, the Hook plus the docks, combat, one main story, live talk (RULINGS.md, 28 Oct). L = likelihood, I = impact (low, med, high). Hours are estimates unless a file is named. "If not retired" names one choice for him: change method, spend, or cut.

## The ten, ranked

**1. Combat does not reach AAA.** Canon says fighting must look and feel AAA (canon.md line 158); nothing has been thrown in Unreal.
- Evidence: production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md (unreviewed; "most bands rest on judgement"); phase 6 is a sketch at 6 to 8 weeks (production/progress-page/progress.json, advisor's estimate); his option pick is still open (production/lane/COMBAT-END-STATE-OPTIONS.md).
- L high, I high.
- Test: one room in Unreal, Tom against one man: jab, heavy blow, block, hit-stop and reel, timed against the sheet's bands and filmed; a rough feel check for him, judged only on fun (RULINGS 5 and 6 Nov). About 14 session hours, 4 PC hours (estimate).
- By 1 Feb 2027. Owner: lane (sheet review), main session (the room).
- If not retired: change method (Epic's Game Animation Sample with physics hit reactions as the base).

**2. Scope outruns the date.** 15 to 20 hours and 44 named people (14 principals plus about 30 regulars, progress.json phase 5), but the cost of one complete person is not measured.
- Evidence: phases 2 to 10 forecast at 52 to 71 weeks from today (sum of progress.json's fc_w, estimate), against about 54 weeks to the release target of 30 Nov 2027 (progress.json); his 1 Feb rule: if cost per piece has not clearly fallen, scope moves first (RULINGS 5 and 6 Nov).
- L high, I high.
- Test: time Ron as one complete person (n16-2) with tools/timelog.py, then Sheila; multiply the second by 44 with B12's ratios. About 2 session hours after Ron lands, no PC hours (estimate).
- By 1 Feb 2027. Owner: main session; Jafar for the scope page.
- If not retired: cut (the docks to the first update, as his 28 Oct ruling allows).

**3. Live talk costs too much per played hour at release.**
- Evidence: $0.12 an hour at 15 replies, small talk only, nothing cached (production/research/llm-inference-economics/COST-PER-HOUR-2026-11-02.md); the budget counter's own figure for the same run is $0.327, unexplained; real questions go to Sonnet 5 at twice the price. At release each copy's allowance must sit above a playthrough's measured cost (RULINGS.md, 28 Oct). Estimate from its run D and the bake-off prices (production/research/lane/TALK-BAKEOFF-CANDIDATES-2026-11-18.md): today about $1.80 to 2.40 a 15 to 20 hour playthrough; with replies on gpt-6-luna (a tenth of Haiku's talk share, a floor; the talk share is not yet split from the checker's, so unverified) perhaps $0.05 an hour, $0.75 to 1.00 a playthrough; at four times as many replies an hour (unverified), four times that. Real replies per hour of play are not measured. Speed sits at 2.02 s against 2.0 (progress.json).
- L med, I high.
- Test: the bake-off arms (n16-6, under its $4 cap) plus a replies-per-hour count from his own play. About 4 session hours, 2 PC hours (estimate).
- By 7 Dec 2026, the first monthly re-forecast (progress.json). Owner: main session.
- If not retired: change method (cache the briefing and move small talk to the cheapest arm or the local model).

**4. Accents fail a native ear.** The VCTK voices (RULINGS, voices) have been judged only by his ear; the checker is a screen.
- Evidence: RULINGS.md, "Faces, hair and voices" (30 Sep, 3 Oct, 26 and 27 Oct); VCTK consent a stated risk (24 Sep).
- L med, I high.
- Test: a blind listening sheet, ten clips per cast voice, each asked "where is this speaker from, and does it fit 1990": the friends' evening plus at least three native listeners. About 4 session hours, 1 PC hour (estimate).
- By 15 Jan 2027. Owner: lane writes the sheet; Jafar only for who listens.
- If not retired: spend (a paid native listener panel, priced first).

**5. The recipe does not transfer.** RECIPE.md has never been re-run by a session without the history.
- Evidence: RECIPE.md (phase 1 rewrite, 9 Nov); re-reading history was 53% of spend in the week to 1 Nov (production/research/token-audit/MONDAY-AUDIT-2026-11-09.md line 53), 40% the next week and 24% in the week to 15 Nov (progress.json), so sessions lean on what they remember.
- L med, I high.
- Test: a fresh session given only one chapter and its skill rebuilds one finished small unit in a sandbox; hours and pass compared with the original (the launderette front, 3.6 h, progress.json). About 5 session hours, 2 PC hours (estimate).
- By 21 Dec 2026. Owner: lane brief, main session run.
- If not retired: change method (chapters rewritten as runnable step lists).

**6. Clothing stalls on the cloth engine.**
- Evidence: Kiln's wrist tangle set aside 18 Nov after three routes (production/research/lane/KILN-WRIST-ANOTHER-DIRECTION-2026-11-18.md); Tom's jacket and Sheila's collar set aside (progress.json, The Tailor); M5 planned at 31 to 62 h (production/lane/KILN-M5-THREE-GARMENTS-PLAN-2026-11-17.md); M7 is the Hook's whole list.
- L high, I med.
- Test: the researched cuff-start method on the nylon jacket to a packaged walk. About 6 session hours, 3 PC hours (estimate).
- By 14 Dec 2026. Owner: clothing task.
- If not retired: change method (reuse first: Epic's MetaHuman garments and CC BY clothes).

**7. Card memory runs out** with the voice on the card and the crowd added.
- Evidence: 6,005 MB in the 8 Nov walk (progress.json); the binding line on 16 Nov was about 4.7 GB, not 6.0, and it moves (production/lane/CROWD-MEMORY-CHECK-2026-11-17.md); the crowd beyond the named people is not priced.
- L high, I high.
- Test: the packaged walk with peak memory logged at 0, 5, 10 and 20 visible people (PLAN.md phase 5's steps), stand-ins allowed. About 3 session hours, 3 PC hours (estimate).
- By 14 Dec 2026. Owner: main session.
- If not retired: change method (the voice off the card for the release).

**8. Hair never passes.**
- Evidence: no character's hair has passed; Houdini's free licence cannot export hair to Unreal, Indie about $299 a year (progress.json, Hair; price unverified).
- L high, I med.
- Test: one character's hair through production/art/hair-2026-09-29/PASS-LIST.md to the packaged walk. About 10 session hours, 4 PC hours (estimate).
- By 1 Feb 2027. Owner: main session.
- If not retired: spend (Houdini Indie, his money).

**9. Estimates keep running two to five times over.**
- Evidence: phase 1 took 4.9 weeks against 1 to 2 (progress.json); phase 2 forecast 4.5 to 7.7 against 3 to 4; 95% of logged hours carry no item code (production/lane/B12-FORECASTING-METHOD-2026-11-17.md).
- L high, I med.
- Test: two weekly orders forecast at P80 with tools/lane/forecast.py, every logged hour coded, both landing under. About 1 session hour a week, no PC hours (estimate).
- By 4 Jan 2027. Owner: main session.
- If not retired: cut (scope moved at his 1 Feb check, not 1 July).

**10. Process overhead eats production.**
- Evidence: records 13% of spend in the week to 8 Nov, a floor, and 11% the week after (progress.json), against the 15% line; reviews of records unmeasured (MONDAY-AUDIT-2026-11-09.md section 1; RULINGS 11 Nov).
- L med, I med.
- Test: tag record and record-review steps in tools/token_audit.py for one week. About 2 session hours, no PC hours (estimate).
- By 7 Dec 2026. Owner: main session.
- If not retired: change method (fewer record kinds; one home per fact).

## How it is reviewed

- Monthly with the re-forecast, first Monday of each month, first on 7 Dec 2026: L and I reset from test results, not plans; a risk closes only when its test passed; new ones come from FINDINGS.md and audits; always ten.
- Each Monday's audit carries five lines: the top three, any date missed, any new risk.
- A missed date goes to his page as its one choice, recommended.

## Old register mapped

- R1 talk empty or unchecked, R2 replies slow, R10 friends' talk cover: merged into 3; quality and speed stay on the talk bench (RULINGS, Speech: the 2 s bar on a newcomer's real questions).
- R3 street to the bar, R4 people break the illusion: merged into 2, 6 and 8; phase 2's bosses carry them.
- R5 frame rate and memory: kept as 7.
- R6 thirty minutes worth playing: retired to phase 3's exit (PLAN.md).
- R7 the night's build: retired to phase 4's exit and production/lane/G1-FRIENDS-PLAYTEST-PLAN-2026-11-17.md.
- R8 licences and terms: retired to the allowlist's own checks; kept on the watch list.
- R9 way of working: split into 9 and 10.
- Watch list W1 to W7 (one PC, small F:, model retirement, Epic's cloud rigging, VCTK consent, his eye as only judge, content breach): kept as the watch list; W5 merged into 4.

## Not verified

Every L and I is the lane's judgement; 44 is 14 plus "about 30"; talk cost assumes 15 replies an hour.
