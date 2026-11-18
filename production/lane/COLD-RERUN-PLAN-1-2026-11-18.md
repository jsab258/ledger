# Cold re-run 1: plan (18 Nov 2026, revised after review)

Blind-spots recommendation 2, adopted by Jafar on 18 Nov, revisits the "no recipe tests" line (CLAUDE.md, Records; undated there, so "13 Oct" is unverified). That line must be replaced the same day the ruling is written. Review: production/lane/reviews/REVIEW-COLD-RERUN-PLAN-1-2026-11-18.md.

## The skill: street weathering

Both candidates are graded High on the recipe map (C2, C4; the "LEDGER Recipe: end-to-end structure" doc, read 18 Nov, rechecked by the round 2 review). The lane recommends the weathering skill (.claude/skills/street-weathering/SKILL.md):

- Cheaper, with a measured original: the chandler's wear redo and gate, 1.77 h elapsed by a session that knew the piece (production/time-log.jsonl, 30 Oct 11:28 to 13:14; US$40.48, production/research/unit-costs/UNIT-COSTS-2026-11-02.md). A shopfront: 4.3 h plus 4 to about 14 h design (same file).
- Clearer pass line: numbers from tools (skill §1 to §4).
- No scope clash: no new shops beyond the fishmonger and the empty unit (RULINGS 3 Oct trades, 22 Oct, 8 Nov).

## The surface and the brief

Every wall in production/specs/street-wear.json already carries rule-placed marks (counted 18 Nov: 13 walls, 5 to 12 each). So the piece is the cottage with the fewest, west_south_bay2, 7 marks (1 damp, 1 splash, 4 streaks, 1 wash), inside the corner's 33 m he has seen, so kept out of the played game.

Brief: replace that wall's rule marks with a hand-led 1990 port-town set: coal soot washed down from the sills, one rust leak from a downpipe bracket, one sill streak, a worn paint band at the door's lock and foot. No damp band (the street's rule marks already carry one, and street-level dirt runs along its foot to 48 m, street_wear.py). No lettering, posters or signs; nothing touching alcohol, gambling or children.

## Kept out of the played game

The new marks live in their own file, production/specs/wear-cold1.json, which the shipped build never loads unless told to. What the main session must add before 1 Dec (all unverified, never built):

1. In VignetteShot.cpp's wear spawning, a game argument -WearExtra=cold1 that loads that file and, only then, hides west_south_bay2's rule marks (as -NoWearOn does today when passed). The new marks carry their own owner name in "on" (not west_south_bay2), so -NoWearOn can take them out alone for stain_check's run without them.
2. The file in tools/ue/stage_game_data.py's list, or the packaged copy never has it.
3. The tester's walk run twice that night: with -WearExtra=cold1, and without it, the second matched against the previous night within 0.2 of 255 (borrowed: on 6 Nov 6:01 that was packaged against editor, not night against night, production/archive/DECISIONS-to-2026-11-09.md; whether two nights' walks agree that closely is unverified) to show the played game unchanged.

## What the cold session receives, and what it does not

Receives, copied into its folder: the three skills (weathering, gate, packaged walk); the project's helper definitions (.claude/agents), which the gate's reviewers run as (RULINGS 8 Nov); the brief; canon.md (setting, not history); a current-rules RULINGS copy; the research the skill cites (production/research/street-wear/, production/research/aaa-reference/studies/05-visuals.md); tools, specs, the Unreal project's source; the Hook sheet; on F:, read in place by name, the KCD2 frames, the wall's last good pictures and the game inputs; a short CLAUDE.md (project facts, content rule, gate, two tries, disk rules).

Does not receive: git history, the handover, NOW.md, DECISIONS.md, NOTEBOOK.md, RECIPE.md, FINDINGS.md, audits, lane files, the shopfront skill, memory notes, the recipe map, any chat. Needing one of them is a finding.

The RULINGS copy: the main session strips each line's dated history (leading date tags, "narrowed 13 Oct", superseded clauses), keeps each rule as it stands, and one fresh reviewer checks it against RULINGS.md: no meaning changed, no history left.

Some history still arrives in the skill's words and the code comments; accepted, and stated in the result.

## How "fresh" is guaranteed

- A new folder holding only the received list: no .git, no remote, so no memory folder for that path.
- GitHub, Google Drive and Docs, Claude Docs and the memory tool off; a new session, never resumed.
- The isolation check reads the session's own log (its tool calls, not Unreal's own file reads) and voids the run on: any git command; any read outside the folder and the named F: folders, the C: memory path included; any fetch of a claude.ai link.
- The cold session cannot push, so the main session carries its output files unchanged into main behind the switch for that night's build, changing nothing in them.

## The gate it must pass

The same as the original (skill §7, gate skill):

1. Readings, each line kept or marked "unmeasured": chart (MAFIA-WEAR's checks C2, C3, not the recipe map's C2); surface bands base and lit; stain_check per new mark (roughness moves 0.1 or more, darkens 40% or less); worn paint 3 to 10% of the door within 5 cm of an edge; night pool clip 2% or under. Counts judge the new owner's marks only: at most 6 on the wall, about 2 in 5 leaks or streaks. The neighbouring cottages' excess (12 and 9 marks) is a known shortfall and fails nothing. Brick streak tint is not asked, so it is not measured.
2. One fresh reviewer per view, day and night, beside its last good picture, the Hook sheet and the KCD2 frames; a new fault blocks.
3. The packaged walk with -WearExtra=cold1, plus the walk without it.

Lines: draft after one blind pass with a clean isolation check; proven after a second, by another fresh session on another surface the next month. Cost within 1.5 times 1.77 h, 2.7 h of session time, reading the skill logged apart. Fail: a gate step failed after two tries, a void check, or the cost over 2.7 h.

## Cost estimate

About 3.5 to 7 session hours (estimate: reading 1 h; a target 1 to 2 h, RECIPE.md §1; a surface 1.5 to 4 h, §2) plus 1 to 1.5 PC hours (estimate); the main session's switch and RULINGS copy about 1 h more (estimate). A cost fail is likely, itself a measure of the skill used cold.

## Cloud lane and PC

Cloud: target rows with a wrong copy each, the wear file, mask pictures (tools/make_wear_masks.py), self-tests, the isolation check, the write-up. PC: every Unreal run, reviewers on full-size pictures, the build and both walks.

## Date

On the order of Monday 30 Nov; run Tuesday 1 Dec 2026, walks that night, verdict 2 Dec, in the week's 10% review share. It runs after step S2 of production/research/street-checks/N16-5-PLAN-2026-11-17.md (a new row for the parade's grey walls; the cottages keep brick_grey, but shared gains and the corner's views move). If S2 has not landed by 30 Nov, the folder is copied from main that day, pinned to the current brick, and the result says so.

## What a failure produces

A gap list: each stall or guess, its step, and the withheld file that held the answer (found afterwards by the lead), written into the skill as missing steps with one fresh review and a NOTEBOOK.md entry (RULINGS 9 Nov); the recipe map's C2 drops to Medium until a cold pass; game faults to FINDINGS.md.

## Open questions

1. Does the 2.7 h line leave out reading the skill? Recommended: yes, logged apart.
2. Can the walk take a game argument? Yes for route_walk.py and play.py (--game-arg, packaged-walk skill); whether the scheduled nightly job passes one is unverified.
