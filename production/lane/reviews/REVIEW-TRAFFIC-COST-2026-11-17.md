# Review: Traffic cost (17 November 2026)

Fresh reviewer, 17 Nov 2026, about 15 minutes. Reviewed: production/research/lane/TRAFFIC-COST-2026-11-17.md (not edited).

## Verdict: PASS WITH FIXES

The method is the right one, the sources hold up when checked, the licence and ruling lines are right, and the hours add up. Fix the points below before it goes into an order. None of them changes the recommendation.

## What was checked

Facts checked at the source today:
- Midtown Madness 2 method (Adzima, Game Developer, 24 Jan 2001), fetched: spline rails, a fixed pool, a bubble round the player, a pointer only to the car ahead in the lane, partial physics that switches to full physics on a collision and then a spline back to the rail. Matches the file. (The byline spells it both "Adzima" and "Azdima"; harmless.)
- ZoneGraph forum thread, fetched: "ZoneGraph does not support runtime generation or modification in its current state" (3 Nov 2025); MassTraffic "was built specifically for The Matrix Awakens demo" and "is very complex" (20 Dec 2023). Matches. The page does not show that the poster is a moderator.
- Chaos Modular Vehicles page, fetched: it is the 5.9 page; it builds a car from Geometry Collection parts under a Cluster Union, which can be broken off or removed. Matches. A search shows forum threads about Modular Vehicles in 5.4 [search only], so it very likely exists in 5.8. "Check on the PC" stays correct.
- DfT 2016 estimates, fetched: urban minor roads 2,200 vehicles a day. Matches. No 1990 minor-road figure is in that release, as the file says.

Project checks:
- D26 "sound is a lane, CC0 only" is in RULINGS.md (the D-list line with D56, D26, D13). The claim is right. DECISIONS.md has no D26 entry by that label; RULINGS is the home and is enough.
- 16 Sep (nothing bought for the street or cars), 23 Sep genre (others drive traffic and the firm's cars; buses scenery), Cars (17 Nov) and canon's 17 Nov driving lines: all quoted correctly. City Sample content kept out, code read as method only: correct.
- Memory line: 5,072 MB used against 4,711 MB at the peak matches PACKING-PLAN-2026-11-16.md line 57 exactly.
- Performance exit (PLAN.md): 16.7 ms, 25 ms, 6 GB, 2.5 ms by day and 1.4 ms at night: quoted correctly.
- Sums: section 7 adds to 41 and 52 hours. Section 4 rows add to 0.15 to 0.35 ms by day and 0.25 to 0.55 at night, fairly rounded to 0.2 to 0.4 and 0.3 to 0.6.
- No em-dashes, no italics found. Length 3,187 words against about 2,200 asked.

## Findings and fixes

1. **The night fallback does nothing.** Section 4 says "if night costs more than 0.4 ms, drop to one car at night", but section 2's table already allows at most one car in view from 19:00. Fix: replace that sentence with "If night costs more than 0.4 ms, first make the headlamps lit lamp cards with no real lights, then halve the night rate; if still over, no traffic after 23:00."

2. **"Up to 40 percent of the night's spare" is wrong.** 0.6 of 1.4 ms is 43 percent. Fix: write "up to about 45 percent of the night's spare" (or "up to 0.6 of the 1.4 ms").

3. **The millisecond figures are guesses with no anchor, though the project has measured anchors.** The table cites 4-BUDGETS only for "Nanite and virtual shadows are off". 4-BUDGETS has measured numbers that fit: static meshes with their LODs 0.6 ms, and the three MetaHumans 0.63 ms together, measured. The car budget is 40,000 triangles at LOD0 with 4 LODs (asset-budgets.json). Fix: add one line under the table: "Anchor: three MetaHumans measured 0.63 ms together and all static meshes 0.6 ms (4-BUDGETS); one or two 40,000-triangle cars at a far LOD should sit well below one MetaHuman, hence 0.1 to 0.2 ms [I]." Also mark the Lumen row [I], not just "not measured".

4. **The sound line puts the rule in the wrong place.** Section 3 says CC BY car recordings are not allowed "by the allowlist". The allowlist has no sound line. The bar comes from D26 (RULINGS), and the 3 Oct sources ruling allows CC BY with credit in general. Fix: write "which D26 does not allow (sound is CC0 only); the allowlist is silent on sound effects".

5. **The checklist's kit work has no hours.** Section 7 leaves out "the car kit itself" (4 to 6 days in 2-VEHICLES). The 12 checklist items (split panels with hinges, glass per window, damage topology, interior slot, sockets) are extra work on top of that, are what stops rework later, and are costed nowhere. Fix: add one row or line: "Checklist additions to the kit's first build: est. 10 to 20 hours machine-free, 6 to 12 on the PC, charged to the kit item, not to traffic."

6. **Checklist items 2 and 5 aim at two different vehicle systems.** Chaos Vehicles needs one skeletal mesh with wheel bones. Modular Vehicles builds a car from Geometry Collection parts. A kit that bakes one in will be redone for the other. Fix: add a line to section 5: "The kit keeps each panel, wheel and glass piece as its own mesh in the source file and assembles two exports from it: a skinned mesh with wheel bones for Chaos Vehicles, and loose parts for Modular Vehicles if 5.8 has it. Which one stage 2 uses is decided when stage 2 starts."

7. **Item 6's "placeholder" damage shape key goes against the gate.** The gate allows no placeholder. Fix: delete "as a placeholder later". Keep only "even edge spacing on panels so dents can deform them".

8. **Pulling into a bay is not part of his stage 1.** His stage 1 is parked cars plus cars passing at the street's end. A car pulling in and becoming a parked car costs 8 hours. It also brings save, reload and seed rules for a parked car that was not there before. Fix: move "Pulling into a bay" out of the stage 1 table into the later options, beside the van and minicabs. Stage 1 then becomes about 38 hours machine-free and 47 on the PC. Change the ranges in the brief to match.

9. **Numbering slips.** Section 5 has two items numbered 12. The sources list has two 13s and no 12. Fix: number the lanes item 13, and the sources 12 (Audiokinetic), 13, 14, 15, 16.

10. **Session wording is out of date.** Section 6 and section 7 say "the town session". The current CLAUDE.md has one production session, with town work handed out as a bounded task. Fix: write "a bounded town task (C# core, with goldens)".

11. **Too long (3,187 words against about 2,200).** Cuts, about 1,000 words in all:
   - Section 1: drop the Hitman/Yakuza row (it belongs under Unreached already) and merge the two Mafia rows into one.
   - Section 2: cut the minicab and bus lines to one line, "Later options: a stopping van, a minibus, the minicabs (each a separate item)".
   - Section 3: drop the City Sample paragraph to one sentence, and the marketplace line to "Nothing bought (16 Sep)".
   - Section 6: cut the "Later, when cars belong to people" paragraph to one sentence.
   - Section 8: cut each "what drives the cost" cell to its four biggest items.
   - Unreached: keep only the DfT 1990 figure, the wheel-bone page and the millisecond note.

## Hours plausibility

Stage 1 at 35 to 45 hours machine-free and 45 to 60 on the PC is believable for a three-car follower with no physics, given the 10 PC hours of tests. It assumes the car kit and its variant already pass, which the file says. Stage 2 at 150 to 300 hours is plausible for one handling model and one car. Getting a MetaHuman in and out of a car is the likely overrun, as the file says. Stage 3 at 1,000 to 2,500 hours is honest as a scale marker only, and it is labelled ROUGH.

Sources read by this reviewer (17 Nov 2026): the Game Developer article, the Epic forum ZoneGraph thread, the Epic Modular Vehicles page and the DfT 2016 release cited in the file; a web search for "Chaos Modular Vehicle UE 5.4" (forum thread titles only, not read).
