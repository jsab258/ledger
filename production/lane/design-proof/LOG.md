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
