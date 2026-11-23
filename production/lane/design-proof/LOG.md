# Design proof log

## Run 1, 20 November 2026, 21:23 to 21:55 (Opus 5.5, configured claude-opus-5-5)

Done:
- Step 0: start row 2026-11-20-2123-design. Budget 66% at 21:20 (newest main row), stop line 95%.
- Step 1: repository already cloned; on lane-2026-11; wip fetched read-only. The add_repo tool was not offered in this session; not needed.
- Step 2: read the description's structure, VISION, canon, RULINGS, the parts tree (by script), the research items, the teardown brief, the walkthrough study (from wip: results not filled yet). STORY-PATTERNS-STEAM not landed. Note: RULINGS.md on lane-2026-11 carries unresolved merge-conflict markers in the models line (not touched: not ours).
- Step 3: coverage.json and COVERAGE.md built by script from the parts tree (group 9 left out, Unreal-only looks marked OUTSIDE) with a hand pass over the 104 rule-only rows (lists in the build script: guards MEASURED, judgement numbers UNMEASURED, pointer-only UNMEASURED).
- Step 4: four Sonnet helpers: Steam themes (sources/themes-steam.json), critics (themes-critics.json, 17 KCD2, 16 GTA V, 16 RDR2 reviews' themes), accessibility and PC standards (a11y-pc.json, 137 items), design-document categories (categories.json, 126). Mapped into themes.json and new rows AX-01 to 11, GD-01 to 08, OUT-01 to 13. Reference mechanics (c) were already mapped item by item in parts-tree/MECHANICS-MAP-2026-11-20.md (289 of 289); not redone.
- Step 5: MEASUREMENTS-NEEDED.md.
- Step 6: planted.json; redteam/ (copy, A-v1, B-v1, triage, real gaps, SCORE-1). Catch A 10/10, B 9/10; 19 material gaps added as RT-01 to RT-19.
- Step 7: DESIGN-COMPLETE.md. Step 9: REPORT.md. Steps were committed together in one push (21542b17), not one by one; the report trimmed under 300 words after.

Next run starts here:
1. When STEAM-WALKTHROUGH-GAMES (on wip) has its results table: one Sonnet helper maps the six games' themes as sources/themes-steam.json was made (same schema), then rerun themes.py logic (see build notes below) and add to themes.json.
2. When STORY-PATTERNS-STEAM lands on lane-2026-11: map its patterns to 3.1.x, 3.3, 3.5.x and RT-01 to RT-06, RT-19.
3. After the design pass writes definitions (AX, RT, GD rows) and the PC measuring reports: update statuses row by row, then red team 2 with a fresh copy (sections renumbered; ten different planted parts; the same two briefs as round 1, kept in this log's history via redteam/SCORE-1.md).

Build notes: the map is made by scripts/classify.py, build.py, themes.py and covmd.py (in that order; they read helper outputs from a scratchpad path at their top, so point S at this folder's sources/ and redteam/ before rerunning). A later run may also edit coverage.json directly and rerun covmd.py.

## Run 2, 20 to 21 November 2026, from 22:53 (Opus 5.5, configured claude-opus-5-5)

- Step 0: start row 2026-11-20-2253-design. Allowance 71% at 22:38 (newest row with a reading); stop line 95%.
- Step (a) done: DEFINITIONS-2026-11-21.md defines all 44 UNDEFINED rows; scripts/apply_definitions.py wrote them into coverage.json (field run2 = "defined"). Result: UNDEFINED 0; of the 44, 27 MEASURED (17 design decisions he may overturn, 10 on guidelines or guards), 13 PENDING, 2 UNMEASURED (GD-04, RT-14), 1 OUT (GD-06 mods, his ruling 22:08), 1 OUTSIDE (10.12 price and demo).
- Fresh Opus reviewer checked the definitions against canon, RULINGS and the description: 22 points, all fixed in place (list at the top of the file); AX-03's field-of-view setting moved to a point for his ruling (it would change the 86 degree ruling).
- Step (b) done: scripts/run2_map.py. GTAVI-MAP-2026-11-21.md maps all 34 yardstick standards and every mechanic line of MECHANICS.md to rows (met, raised, gap added, out, outside). Six gap rows added (GV-01 the boot, GV-02 shedding slot by slot, GV-03 the passenger who knows the way, GV-04 places stay open, GV-05 bugs at release, GV-06 how a deed is told), all MEASURED as design decisions. Ten standards raised and marked "Raised by Y..." (1.2.4, 1.2.10, 1.2.9, 6.1.1, 6.2.1, 2.6.10, 2.5.3, 2.7.6, 3.6.3, 7.8); RT-10 and the AX rows raised in step (a). Not raised: Y5.3 local radio news, because the press works only through Alison (D56). themes.json: 44 walkthrough rows (WT, 36 general and 8 mechanic) and 14 story-pattern rows (SP) added, each on parts with a test; every theme's weakest status recomputed from the current rows.
- Step (c) done: scripts/run2_plan.py gives every one of the 71 UNMEASURED rows a measure_how and measure_when (groups in scripts/plan_groups.json: teardown 23, design pass 2 tests 15, listening 8, feel-sheet extras 6, story measure 5, 1990 sources 4, guides 4, feel block 3, panel bar 2, typed-talk set 1). MEASUREMENTS-NEEDED.md rewritten for the order of 23 Nov: GTA VI's full footage pass first (about 24.5 PC hours), then the feel block, the teardown (GTA IV in Mafia's place), section A (about 14.5 h) and the listening pass (about 2 h); cloud work listed with dates.
- Design pass 2 done (beyond the brief's list, cheap and in the design's words): the 15 pointer-only rows given tests (second part of DEFINITIONS-2026-11-21.md); 14 MEASURED, 2.7.3 PENDING with GD-07.
- Step (d) done: coverage.json has a counts block (341 rows: 184 MEASURED, 30 PENDING, 56 UNMEASURED, 0 UNDEFINED, 14 OUT, 57 OUTSIDE); COVERAGE.md regenerated; themes recomputed (242: 91 with an UNMEASURED part, 45 PENDING); DESIGN-COMPLETE.md lists what stands before the gate with dates; REPORT.md rewritten (under 300 words).

Next run starts here:
1. Red team 2 (the definitions are in): build a fresh copy of the game description with DEFINITIONS-2026-11-21.md and the GV rows folded in, sections renumbered so no gap shows by numbering; plant ten different parts (not those of planted.json round 1) and record them in planted-2.json; two fresh Opus helpers with the briefs in redteam/BRIEFS.md; score as SCORE-1.md did; add real gaps as rows.
2. Cloud items dated in MEASUREMENTS-NEEDED.md: section B (1990 figures), section C (guides), the privacy check (8.2.1, 10.11), the panel bar for 7.2 and 7.3 from the players study, the typed-talk set (RT-14).
3. When the PC measuring reports (from 24 Nov) and the story measure lands (by 28 Nov 12:00): update statuses row by row, then red team 3 on the measured design.
4. Point for his ruling carried by the advisor: AX-03's field-of-view setting.
Scripts, in order when rebuilding: classify.py, build.py, themes.py (run 1); apply_definitions.py, run2_map.py, run2_plan.py (run 2; each is safe to rerun); covmd.py last.

## Run 3, 21 November 2026, from 07:35 (Opus 5.5, configured claude-opus-5-5)

- Step 0: start row 2026-11-21-0735-design. Allowance 74% at 05:22 (newest row with a reading); stop line 95%.
- Step (a) done: PANEL-BAR-2026-11-21.md. 7.2 and 7.3 MEASURED: at least 7 of 8 panel players recommend (KCD2-grade passes 89% of the time), M1 milestones 4 and 5 of 8 kept. scripts/run3_apply.py with scripts/run3_changes.json applies run 3's row changes by step (a, b, c, d, e); covmd.py after.
- Step (b) done: CLOUD-FIGURES-2026-11-21.md. MEASURED: 2.7.4 rent (council £23.36, private £65), 2.6.4 custody (inside PACE limits; 'then bail' after a killing corrected), 2.7.6 fence about a third (was 0.4), 2.4.2 cooling (KCD2 a few game days), 8.3.1 display list, GD-04 replay. PENDING: 7.13 (references 48 to 144 min a day against our 18; his C11 and A5). Still UNMEASURED: 2.1.2 (no hourly 1990 figure found; ONS tables next, by Thu 26 Nov).
- Step (c) done: PRIVACY-CHECK-2026-11-21.md. 8.2.1 and 10.11 MEASURED; consent route for crash reports (not strictly necessary), what the question must say, no identifiers, 30-day local deletion; the AI notice as its own screen meeting Article 50 (in force 2 Aug 2026).
- Step (d) done: typed-talk/ (RT14-SET-2026-11-21.jsonl, README.md, agreement-2026-11-21.json, the blind copy and the second labels). 300 lines, content rule checked; second blind labeller agreed 98.3%; bar 95% overall, 90% hard, amounts exact. RT-14 MEASURED.
- Step (e) done: red team 2. scripts/rt2_build.py builds redteam2/GAME-DESCRIPTION-COPY-2.md (definitions and GV rows folded in, ids removed, renumbered) and planted-2.json (ten new parts). Round 2a (briefs unchanged): A 10/10, B 8/10. Brief improved once (redteam/BRIEFS.md, round 2 change); round 2b: A 9/10, B 10/10. Triage by two Sonnet helpers (redteam2/triage-v2.json, triage-v3.json): 22 material topics, rows RT2-01 to RT2-22 UNDEFINED (redteam2/real-gaps-v2.md, SCORE-2.md). Clean rounds still 0.
- Step (f) done: DESIGN-COMPLETE.md (where it stands after run 3, the list with dates; gate now 30 Nov to 1 Dec at the earliest), REPORT.md (third report), MEASUREMENTS-NEEDED.md sections B and C marked. themes.json not recomputed (no theme mapping changed; RT2 rows hang on existing parts' themes only through the next pass).

Next run starts here:
1. Design pass 3: define RT2-01 to RT2-22 (redteam2/real-gaps-v2.md; triage-v2.json and triage-v3.json hold each line's missing part) in the design's own words inside canon and his rulings, each with a pass-or-fail standard and source, a fresh Opus reviewer, then set statuses (scripts/run3_apply.py pattern: add a step to run3_changes.json or a run4 file). Sun 22 Nov.
2. 2.1.2: read the ONS time in and out of home tables (ad hoc 2655) and scale back; by Thu 26 Nov.
3. When the PC measuring and the story measure report: update statuses row by row.
4. Red team 3 (Sun 29 Nov): rerun scripts/rt2_build.py adapted (fold in design pass 3, ten new planted parts not in planted.json or planted-2.json, refer to sections by name), the improved briefs in redteam/BRIEFS.md (round 2 change), two fresh Opus helpers, triage as triage-v2/v3. Red team 4 the next day if 3 is clean.
5. Point for his ruling carried by the advisor: AX-03's field of view.

Fit check of 21 Nov: 34 pairs (13 fit, 5 do not fit, 14 cannot tell yet, 1 gap, 1 contradiction), 10 new number gaps, 61 players' questions (35 answered, 16 gaps, 10 fit problems), 4 scope questions; its gaps and misfits are to be added to the coverage map by the next design proof run, and the fit check and the players' questions run again before red team 3.

## Run 4, 21 November 2026, from 09:05 (Opus 5.5, configured claude-opus-5-5)

- Step 0: start row 2026-11-21-0905-design. Allowance 78% at 08:52 (newest row with a reading); stop line 95%.
- Step (a) done: DESIGN-COMPLETE.md carries the process guards G-A (MEASURED only on a real figure; DECIDED for design decisions, listed for him; the gate reports real-figure rows), G-B (material gap: first week, stuck, breaks a ruling, blocks a playthrough check), G-C (at most four red-team rounds, then scope to him), G-D (the clock before red team 3). scripts/run4_guard.py split the 195 MEASURED rows (field real_basis; force_decided list for rows judged by hand). covmd.py shows DECIDED and the real-basis counts.
- Step (b) done: DEFINITIONS-2026-11-21.md, new heading "Design pass 3": the advisor's decisions D-Q2 to D-Q4 (DECIDED), G1 the road plan in metres (on the built 48 m Quay Street and its bend; crossings 548 m by road, 475 m on foot; chase loop 1,528 m), G2 to G10, the text fixes F03, F20, F13, F15, the open pairs given measurements (F04 with GTA IV, F05, F16, F19, F21, F24, F32), the players' gaps P04, P09, P17, P18, P34, P45, P52, L-01, and RT2-01 to RT2-22. FIT-CHECK's F04 names GTA IV in Mafia DE's place.
- Step (c) done: the clock both ways (CLK-01 to CLK-07, a table A against B), rows PENDING his C11. AX-03's field of view taken as his ruling (75 to 100, default 86).
- Fresh Opus reviewer: 30 points, fixed once (list at the top of design pass 3). Kept: D-Q2 to D-Q4 as DECIDED, as the brief directs.
- Step (d) done: scripts/run4_apply.py writes the RT2 statuses and adds 35 rows (FIT-*, CLK-*); counts block in coverage.json (398 rows: 101 MEASURED, of them 35 on reference or real-world figures and 66 on his rulings or canon; 131 DECIDED; 49 PENDING; 46 UNMEASURED; 0 UNDEFINED; 14 OUT; 57 OUTSIDE). COVERAGE.md regenerated; DESIGN-COMPLETE.md's table with dates and the DECIDED list; REPORT.md (fourth). themes.json not recomputed (new rows hang on mapped parts).

Next run starts here:
1. When he answers C11: drop the chosen column of the clock table into the definitions (and RT-04's fail-safe week, F13), set CLK-01 to CLK-07, 7.13 and FIT-F13 to DECIDED or MEASURED by the guard; rerun run4_apply.py's counts and covmd.py.
2. Cloud by Thu 26 Nov: 1990 prices (G8, RT2-14) from dated sources; 2.1.2 and G9 from the ONS tables; F19 the line-table count.
3. When the PC measuring and the story measure report (24 to 28 Nov): update rows; F24 money run once G8 is in.
4. Sat 28 Nov: the fit check and the players' questions again on the defined design.
5. Red team 3 (Sun 29 Nov) and 4 (Mon 30 Nov): rt2_build.py adapted (fold in passes 2 and 3; ten new planted parts not in planted.json or planted-2.json; refer to sections by name); triage line by line against G-B's four tests, naming the test met. No round 5 (G-C).
Scripts in order when rebuilding: run 1 to 3 scripts, then run4_guard.py, run4_apply.py, covmd.py last.

## Run 5, 23 November 2026, from 13:18 (Opus 5.5, configured claude-opus-5-5)

Launched as "design proof run 2: the design pass" with run 1's steps (a) to (d). Those steps were already done by runs 2 to 4 (20 to 21 Nov): the 44 undefined parts defined, GTA VI, the walkthrough themes and the story patterns mapped, every unmeasured row given a plan, the counts and gate list written. So this run took up where run 4's log stopped and did what the order of 23 Nov names for design proof run 5 (his clock B, the chase against the chase sheet, the crowd against measured views).
- Step 0: start row 2026-11-23-1318-design. Allowance: the newest row with a reading says 95% at 12:08 on 22 Nov, but the week reset at 13:00 today, so that reading is last week's; this week's line (0 to 90% by Mon 30 Nov 07:00) applies and spend was kept small (one Opus reviewer).
- Design pass 4 (DEFINITIONS-2026-11-21.md, last heading): clock B written in (CLK-01 to CLK-07, 7.13, FIT-F13 MEASURED on his ruling; RT-04's fail-safe in Act II week 5); chases: no timer (DP5-C01 DECIDED, raised by GTA VI), length and search bands (DP5-C02, DP5-C03 PENDING); the busiest view 12 to 20 and G9's bands rescaled (GD-02, FIT-G9 PENDING, bands DECIDED); 1.2.3 MEASURED on GTA VI's five parked-car entries. Fresh Opus reviewer: 14 points, fixed once (list at the top of pass 4). scripts/run5_apply.py writes the rows (safe to rerun); covmd.py after.
- GTAVI-MAP: run 5 additions. MEASUREMENTS-NEEDED.md: new top section for the order as adopted (installed games first, five-sample rule, GTA VI first, about 134 PC hours left against n23-1's 60, the lean order); run 2's list kept below as history; every UNMEASURED row's measure_when dated to the order.
- Counts: 401 rows: 111 MEASURED (21 reference game, 15 real-world, 75 his rulings or canon), 132 DECIDED, 42 PENDING, 45 UNMEASURED, 0 UNDEFINED, 14 OUT, 57 OUTSIDE. DESIGN-COMPLETE.md and REPORT.md (fifth) updated.

Next run starts here:
1. When the PC measuring reports (STATUS.md on wip, from Mon 23 Nov): set rows only on solid numbers; first DP5-C02 and FIT-F04 (chase lengths), DP5-C03 (search length), GD-02 and FIT-G9 (crowd counts, KCD2 from the installed game), the feel rows. Rerun run5_apply.py's counts and covmd.py.
2. Cloud by Thu 26 Nov: 1990 prices (FIT-G8, RT2-14), 2.1.2 and FIT-G9 from the ONS tables, FIT-F19; then FIT-F24's money run.
3. The text fixes design pass 4 lists (every "within 90 real seconds", 45 s, 18 minutes, 9 weeks, "eighth game week") go into the blueprint, not the old description: give them to the blueprint keeper's next fold (BLUEPRINT-CHANGELOG), since the giant prompt is written from BLUEPRINT.md.
4. Sat 28 Nov: the fit check and the players' questions again; then red teams 3 (Sun 29) and 4 (Mon 30) on the blueprint, rt2_build.py adapted, ten new planted parts, triage by G-B. No round 5.
5. Read on arrival: production/research/lane/aaa-studies/ (studies A and B, landing this week) and production/lane/blueprint/PRIOR-RESEARCH-INDEX.md; map their standards to rows.
Scripts in order when rebuilding: runs 1 to 4 scripts, run5_apply.py, covmd.py last.

## Run 5, second pass (job fire, 23 Nov from 13:28)

- Start row 2026-11-23-1328-designproof. The job's points 1 (clock B), 2 (only solid numbers count; two solid so far) and 7 were already done in the first pass at 13:18 to 13:27.
- Built on the research folders on wip (no PRIOR-RESEARCH-INDEX.md yet): study 01-npc-life, performance-budget, street-life finding 5.
- GD-02 settled by the counts: one frame 4 to 10 at busy bands, 2 to 7 other daytime, 0 to 2 quiet night, 15 to 25 at the market and match; the first pass's 12 to 20 withdrawn; GTA VI's 100+ tram-stop claim goes to block 1 to count on full-size frames.
- Chases against the map: the Hook holds 1 to 3 minutes without repeating roads; the references' 4 to 8 do not. Rulings to revisit written (R1 map, R2 clock), keep recommended for both, in DEFINITIONS run 5 second pass and DESIGN-COMPLETE. No fresh reviewer for this short pass (arithmetic checked by hand); the next run's reviewer reads it with the measuring updates.
- Counts unchanged: 401 rows, 111 MEASURED, 132 DECIDED, 42 PENDING, 45 UNMEASURED, 0 UNDEFINED.
Next run starts at "Next run starts here" of run 5 above, plus: put R1 and R2 to him through the advisor; count GTA VI's tram stop in block 1.
- 23 Nov (blueprint keeper): From 23 Nov the design proof checks BLUEPRINT.md, and red teams 3 and 4 are given the blueprint, not the old description.
- 2026-11-23, studies set B (cloud): five new files for the next design proof run in production/research/lane/aaa-studies/: WHERE-PLAYERS-QUIT.md (WQ-01 to WQ-07), MISSIONS-AND-SIDE-QUESTS.md (MS-01 to MS-09), MONEY-AND-PROGRESSION.md (MP-01 to MP-07; MP-01 likely clashes with G8's top price), FAILURE-AND-FRUSTRATION.md (FF-01 to FF-07), IMMERSION-FEATURES.md (IM-01 to IM-07); each standard names the coverage rows it touches.
- 23 Nov 2026 13:53, AAA studies set A (cloud, Opus 5.5): for the next design proof run, read production/research/lane/aaa-studies/MEMORY-SYSTEMS.md (MEM-01 to 11), TALK-AS-PLAY.md (TALK-01 to 11), PLAYERS-STORIES.md (STORY-01 to 08) and DENSE-DISTRICT-REVIEWS.md (DENSE-01 to 10, footage table owed by the PC); each standard names the coverage rows it touches. Player counts are thin and marked.
- 23 Nov 2026 13:59, AAA studies set A second pass: the four set A files now end with requests for the builder's PC measuring (KCD2 memory and talk pace, RDR2 greet and memory, four-part moments per evening in KCD2, GTA V and RDR2, Sleeping Dogs district crossings); for MEASUREMENTS-NEEDED.md at the next run. No ruling argued against.
