# Phase 2, Quay Street: the pieces (first draft, 8 November 2026)

**Revision, 9 November 2026.** Made after the advisor's independent review of 9 Nov, 11:45. Each of its points was checked against its file on 9 Nov. The points the files did not bear out, and everything outside this plan's text, are in FOR-ORDER-16-NOV-2026-11-09.md. What changed:
- Piece 1 is now the street budget and scale test.
- Piece 2 is a greybox of the whole street, with P20 inside it.
- The order follows the PS5 gap list's ranking: street life and distance come before rooms, upper windows and the slab, with two stated exceptions (§3).
- §2 restates the total in weeks at the one measured week's 57.03 logged hours.

The 8 Nov fresh review and its fixes below judged the 8 Nov text and are unchanged. The 9 Nov revision had one fresh review (REVISION-REVIEW-2026-11-09.md, pass with fixes); its thirteen fixes are applied and listed here.

**Review fixes applied (9 Nov)**
1. §3 states the two exceptions to the gap order (P20 early, shells at step 3) with their reasons.
2. §2's first paragraph labelled as the 8 Nov list; the revised list's low end (266 h) and guesses (about 180 to 330 h) stated; the old week figures' replacement named.
3. A line under §2's table: every range excludes distance beyond the crowns and the crowd beyond the named people.
4. "The likeliest range" reworded to the records' low end; rows at three and four times added.
5. The pace basis named (57.03 h, review included); the main row at production hours alone, 8.4 to 14.3 weeks.
6. Piece 2 given a done line with three counted checks, and a matching §4 line.
7. Piece 2: "Reference: none found"; Mafia's greybox step kept as an unverified lead (one source read, one refused); every "None." row now reads "Reference: none found" or names its study.
8. The greybox's 10 to 20 h stated to exclude the checks' and P20's hours.
9. Piece 1 names its precondition, the DECISIONS.md entry against "nothing is multiplied".
10. The kit-reuse check (s04-04) placed at §3 step 3, with shells.
11. "2.2 weeks behind" corrected to 2.4; question 1 marked settled and removed from the fronts row.
12. FOR-ORDER item 3 now names the progress page's 8 Nov hours note and piece order as well as planned_w.
13. The 8 Nov word note corrected (about 2,380 words before these fixes, not under 1,300).

For n09-4. Our own records, read 8 Nov 2026; one fresh review (below), its fixes applied 8 Nov against their sources. Reference methods: Mafia's kit and dressing counts, Kingdom Come II's weather life (studies/04-street-world.md) and its scale test (MEMORY-PLAN-2026-11-07.md §5). "Guess": unmeasured; "E": estimate. Records run 2 to 4 times plan figures (.claude/skills/shopfront/SKILL.md, "Cost"; CORNER-PLAN-2026-11-02.md line 85).

In the street now: lamp posts, the west row's eaves, eight of ten shop units (progress.json's seven plus Mickey's, the corner; shop-windows TARGET.md line 31); the corner's trims, roof, wear, night and people, passed packaged 6 to 7 Nov (orders/2026-11-02.md).

## 1. Pieces

**Budget and greybox, first (revised 9 Nov)**
- Piece 1, street budget and scale test:
  - It starts from n09-3, 14 h (orders/2026-11-09.md line 24). Its done line should cover card time as well as memory. Today there is 0.21 ms spare by day and 0.19 ms at night against the 14.0 ms line, and the walking memory medians are 6,145 and 6,151 MB (EXIT-D-REVIEW-2026-11-09.md).
  - A ms and MB budget for each of the three views: the hook camera by day, the reverse view, the street at night. This fills in s12-03's missing numbers (people in full detail, draw distance, shadow lights per frame), which have no values yet (RECS-BY-PHASE-2026-11-06.md line 62).
  - Then the scale test. Reference: Kingdom Come II's method (MEMORY-PLAN §5, step 3, its source [12]): a test-only switch that adds street copies and stand-in people. MEMORY-PLAN gives it 2 to 4 days and says it may grow. Guess 16 to 32 h (8 h a day, inferred).
  - Precondition: before the switch is built, a DECISIONS.md entry must rule it allowed against "nothing is multiplied", with its reason (MEMORY-PLAN §5, step 3; FOR-ORDER item 8).
  - Nothing is copied along the street until the scaled street fits its budget.
  - World Partition stays unsized (MEMORY-PLAN §2); its trial is sized after the scale test.
- Piece 2, a greybox of the whole street:
  - The street's 48 m (studies/04 line 57) in plain stand-in blocks, with walking routes, door points, a crowd count and camera collision, walked at the three views.
  - The width and street-end checks (s04-01, s04-06) and P20 are done inside it.
  - Done when: every walker completes each route end to end (none stopped short of a route's end); no frame has the camera inside a wall in a free walk at each of the three views (count 0); and the crowd at piece 2's count stands within piece 1's ms and MB budget at each view (REVISION-REVIEW-2026-11-09.md, fix 6).
  - Reference: none found. Mafia's "greyboxes, then hero buildings" (asset-plan/1-BUILDINGS-AND-INTERIORS.md line 61) is an unverified lead from search snippets. Of its two sources, the PlayStation Blog's "How Hangar 13 remade Mafia" (Alex Cox, 24 Sep 2020, https://blog.playstation.com/2020/09/24/how-hangar-13-remade-mafia/, read 9 Nov 2026 through a page-answering fetch tool) has no sentence on greyboxes, blockouts or building order; Alper Isler's ArtStation page (https://artizan.artstation.com/projects/q9oO6e) refused the request (403, 9 Nov 2026) and is unreached. No study under aaa-reference/studies mentions a greybox (REVISION-REVIEW fix 7, searched 9 Nov). The general step, a blockout right after the target corner with values checked under game light from the start, is from search summaries (production/research/aaa-street/SUMMARY.md lines 39 to 48 and 96), unverified.
  - Why: hidden boxes that block only people, and straight-line walks, stopped the walkers at the quay end (QUAY-END-DIAGNOSIS-2026-11-08.md §1). In a free walk the camera entered the office's walls (EXIT-A-REVIEW-2026-11-09.md, new 1).
  - None measured. Guess 10 to 20 h. This excludes the checks' 3 to 5 h (Shells) and P20's 3 to 5 h (below); each stays priced once in its own row.
- P20 exposure, inside piece 2. The chart method is proved. The chart is read before base colour and wear (street-weathering skill §1, line 15), so P20 comes before any wear on the copied walls. Guess 3 to 5 h.

**Fronts and shops**
- Fishmonger (bay 1): an older front stands in the corner (vignette-scene.json lines 367 to 693; CORNER-PLAN line 7); its design failed review (orders/2026-10-25.md line 357): to replace, designed again. Empty unit (bay 3): review fixes not made. Shopfront skill. Both: 16 to 37 h (UNIT-COSTS-2026-11-02.md). Built in phase 2 (RULINGS line 17, 8 Nov; progress.json line 83).
- Mickey's front dark at night: waiting 3 (orders/2026-11-09.md). Shopfront skill. About 2 h.
- Signage (asset plan family 7). Reference: none found. Guess 6 to 10 h.
- Upper windows: shaded frames, few fake rooms (s05-01, s04-05). Reference: studies/04 and 05 (Mafia 24 fake rooms in about 8,100 windows; RECS-BY-PHASE line 64). Guess 8 to 16 h.
- Real near shop rooms (family 2; P11, 1 to 2 days a room, pre-production/3-PROOFS.md). Reference: none found. Guess 8 to 16 h.

**Shells and roofs**
- Brick course, 75 or 86 mm, "decided before phase 2" (TERRACE-KIT-TABLE-2026-10-29.md §5, 1): question 6; 86's cost unpriced.
- Flemish bond, burnt headers: waiting 5; fixed with the buildings (asset-plan SUMMARY.md, order 2), so before the corner's copy. Reference: none found. Guess 4 to 8 h.
- The corner copied along the street: his keep, 7 Nov. Shopfront, slate-roofs, street-weathering skills. The corner took about 12.6 h (time log, n02-4-corner, people excluded; the reviewer's rough sum, inferred). Guess 10 to 20 h; roofs already street-wide (1.1 h measured).
- The hill's crowns: waiting 4; tries spent. Reference: none found. Guess 8 to 16 h.
- Distance beyond the crowns: far houses, trees, the quay end (PS5-GAP-LIST-2026-11-08.md, Distance, medium to large). Reference: none found. Unpriced, not in the total (added 9 Nov).
- Checks: width, kit reuse, street ends (s04-01, s04-04, s04-06); width and ends run on piece 2's greybox, kit reuse with the shells (§3 step 3). Reference: studies/04 (Mafia 18 to 19 facade pieces, kit meshes about 15 times each; RECS-BY-PHASE line 66). Guess 3 to 5 h.
- The terrace kit's 39 modules (22 to 28 h; TERRACE-KIT-TABLE §5): proposed for phase 5.

**Ground and furniture**
- Wet seam and icy near lane (PLAN.md). Street-weathering skill. Guess 6 to 10 h.
- About 10 furniture kinds (family 4). Reference: none found; nothing measured; each review gate adds 0.5 to 0.85 h (UNIT-COSTS, "Gate"). Guess 20 to 30 h.
- Lamps as Mafia builds them (s05-03). Reference: studies/05 (each lamp a key spot plus a tiny bulb; RECS-BY-PHASE, s05-03 row). Guess 3 to 5 h.
- Vegetation (family 9). Reference: none found. Guess 4 to 8 h.

**Props and dressing**
- Tiers 1 to 3, at least 5 props per 10 m (studies/04, target 2). The street is 48 m, 36 m of frontage (studies/04 line 57), so under 30 m remains: the corner plan's 1.75 h for 30 m, times 2 to 4: 3.5 to 7 h.
- The fishmonger's slab (families 5 and 6, P16). Reference: none found. Guess 8 to 16 h.
- Food beyond the slab (family 6; P16, 1 day). Reference: none found. Guess 4 to 8 h.

**People and clothes**
- This week: Ron 16 h (his clothes included), clothing 18 h (Sheila's included), hair 6 h, people alive 8 h: 48 h (orders/2026-11-09.md).
- Hook rows 1 to 3 less Ron and Sheila: Darren 6.3 h E plus Sheila's remainder after n09-6 (row 10.3 h E): 6.3 to 16.6 h E (HOOK-GARMENT-LIST-2026-11-03.md); 12.6 to 66 h at the records' rate. Game-garment skill (unreviewed).
- Martha, Kate, Leonard: bodies only, 12 h E, outside the list's garment total (same file, line 43); 24 to 48 h at the records' rate; a crowd face first (line 44).
- P7 walking (s07-02, s07-03; RECS-BY-PHASE-2026-11-06.md line 43): proof 1 to 2 days (3-PROOFS.md), partly n09-8. Guess 4 to 8 h.
- P6 plain clothes at 8 m: one coat, three bodies, twelve people's cost (3-PROOFS.md: 3 to 5 days whole). Guess 8 to 16 h.
- The crowd beyond the named people, to piece 2's count and routes; its garments, question 3. Unpriced, not in the total (added 9 Nov).

**Light and weather**
- P20 exposure: moved into piece 2 (9 Nov).
- Weather life: flies, smoke, drips (s04-07). Reference: studies/04 (Kingdom Come II's weather life, small life tied to weather and hour). Guess 4 to 8 h.
- Shop glass dirt mask (s05-02). Reference: studies/05 (s05-02 row). Guess 2 to 3 h.
- s12-05, dynamic resolution with headroom. Reference: studies/12 (s12-05 row). Guess 2 to 4 h.

**Sound**
- P13 ambience: beds exist; spawned voices, activity, doors, echo zones lacking (studies/08-sound.md); his ear owed. Reference: studies/08-sound.md. Guess 12 to 20 h.

**Cars**
- Parked fictional cars, four classes: 50 to 90 h E (N09-13-CAR-COSTS-2026-11-08.md); on his page. With phase 2 (order rule 11), gated on P9 (PLAN.md; RULINGS 2 Oct).

**Budget and exit**
- n09-3 14 h (now inside piece 1), n09-4 5 h; the exit walk and gate, P15 included: guess 6 to 10 h.

## 2. The total, plainly

**The 8 Nov list, as it was judged.** About 240 to 385 h without cars, 290 to 475 h with them, at plan figures. Phase 2's ceiling is 2.00W, W one weekly allowance (PLAN.md lines 5, 28): about 240 h at the order's 120 main-line hours a week (orders/2026-11-09.md §2; inferred). **That list did not fit the ceiling:** its low end only met it. The plan's 3 to 4 weeks (300 to 400 h at 99 production hours a week) held only the low end. About 155 to 280 h were guesses or estimates, which records run 2 to 4 times: at twice, 395 to 660 h without cars, 1.6 to 2.75 times the ceiling; with cars 495 to 840 h. The 2027 line now reads 2.4 weeks behind (progress.json line 558, line2027.behind_w, read 9 Nov). The excess: question 5.

**The revised list, 9 Nov.** Plan figures 266 to 437 h without cars: its low end is above the ceiling of about 240 h, so it does not fit even at plan figures. About 180 to 330 h are guesses or estimates (the 8 Nov 155 to 280 h plus pieces 1 and 2's 26 to 52 h; REVISION-REVIEW fix 2). The 8 Nov text's "4 to 7 weeks" and "5 to 8.5 weeks" were removed on 9 Nov; the weeks in the table below replace them.

**Revised 9 Nov: the total in measured weeks.**
- **The pace.** The one measured week, 2 to 8 Nov, logged 57.03 h: 53.53 production and 3.49 review (SCOREBOARD-2026-11-08.md §4). These are task-hours, which can overlap, and the log has gaps in other weeks. One week is not yet a proven rate (unverified).
- **The basis.** The table's weeks divide by 57.03 h, all logged hours, review included. At production hours alone (53.53 h), the main row, guesses at twice without cars, is 8.4 to 14.3 weeks (447 and 764 divided by 53.53). Which basis the order uses is for the session.
- **What pieces 1 and 2 add:** 26 to 52 h of guesses (the scale test 16 to 32 h, the greybox 10 to 20 h).

At 57 h a week:

| | Hours | Weeks |
|---|---|---|
| Plan figures, without cars | 266 to 437 | 4.7 to 7.7 |
| Plan figures, with cars | 316 to 527 | 5.5 to 9.2 |
| **Guesses at twice, without cars (the records' low end)** | **447 to 764** | **7.8 to 13.4** |
| Guesses at twice, with cars | 547 to 944 | 9.6 to 16.6 |
| Guesses at three times, without cars | about 630 to 1,100 | 11.0 to 19.3 |
| Guesses at four times, without cars | about 810 to 1,430 | 14.2 to 25.1 |
| The 8 Nov list alone, guesses at twice, without cars | 395 to 660 | 6.9 to 11.6, about 7 to 12 |

- **Excluded from every range above:** distance beyond the hill's crowns and the crowd beyond the named people, both unpriced (§1).
- **The three- and four-times rows** are inferred here: plan figures plus two or three further times the guesses of 181 to 332 h (REVISION-REVIEW fix 2); 266 + 2 x 181 = 628, 437 + 2 x 332 = 1,101; 266 + 3 x 181 = 809, 437 + 3 x 332 = 1,433. Their high ends sit about 5 h above the twice row's method, which carried the 8 Nov rounding (660 + 104).
- **The page's figure.** None of these ranges holds the plan's 3 to 4 weeks (planned_w, progress.json line 131). The 99 and 120 h weeks behind that figure are planning figures, not measured.
- **The likeliest overruns:**
  - People: 78 to 101 h at plan figures (this list's People rows summed, inferred).
  - Card memory: n09-3's 14 h covers MEMORY-PLAN's steps 1 and 2; the scale test is 2 to 4 days more and may grow.
  - Furniture: 20 to 30 h, nothing measured.
  - Props: the latest prop review took 2.6 times the first (SCOREBOARD §1).

## 3. Order (revised 9 Nov, by the PS5 gap list's ranking)

The gap list ranks street life 1, distance 2, people 3, buildings 4, night 5, daylight 6 (PS5-GAP-LIST-2026-11-08.md). Two exceptions, with their reasons:
- P20 (daylight, rank 6) comes inside piece 2: the chart is read before base colour and wear (street-weathering skill §1, line 15), so it must precede any wear.
- Shells (buildings, rank 4) come at step 3, ahead of street life and distance: the bond and the wear touch each wall once only if they follow P20 and precede the corner's copy (TERRACE-KIT-TABLE §5; asset-plan SUMMARY, order 2; skill line 15). Street life is not held back by this, since people run from week 1 (step 4; the week's 48 h, orders/2026-11-09.md). Whether this exception stands is the session's to accept (REVISION-REVIEW fix 1).

1. **Piece 1: the street budget and scale test.** n09-3 with card time, s12-05, and s12-03's numbers for each view. These cap what may multiply (RECS-BY-PHASE, "the five", 1). The scale test's DECISIONS.md entry comes before its switch. Nothing is copied along the street until the scaled street fits.
2. **Piece 2: the greybox of the whole street.** Routes, door points, crowd count and camera collision, walked at the three views to its done line. P20 and the width and street-end checks go inside it, then the tuning home (s13-01).
3. **Shells.** Brick course and bond first. Then the corner along the street, within piece 1's budget, with the kit-reuse check (s04-04). Wear goes on with them, after P20, so each wall is touched once.
4. **Street life, the largest gap.**
   - People from week 1, with P7.
   - The crowd, to piece 2's count.
   - P6 and the crowd's garments only after the tailor's sample passes (order rule 10).
   - P9's blind silhouette early; cars only after it and his tap.
   - Weather life.
   - Sound, once his ear is given.
5. **Distance, the second gap.** The hill first; its tries are spent, so a third needs his yes. Then what lies beyond the crowns (unpriced).
6. **Fronts and the rest of the street.** Fronts and signage; ground, furniture, lamps and vegetation; then dressing.
7. **Rooms last.** Near shop rooms, upper windows, the slab, food.
8. **The exit walk,** P15 included.

## 4. Measured weekly on the progress page

- Budget per view: ms and MB at the three views against piece 1's budget; the scaled street's MB (added 9 Nov).
- Greybox: routes walked end to end, of all routes; frames with the camera inside a wall in free walks at the three views (target 0); the crowd count's ms and MB against piece 1's budget (added 9 Nov).
- Fronts: units passed packaged, of ten.
- Shells: kit placements per mesh; distinct facade meshes (s04-04).
- Furniture: kinds passed, of the list.
- Props per 10 m (target 5); ground pieces per 10 m (corner bar 12).
- People in gated clothes; hours per garment, latest against first.
- Light: chart C2 and C3 pass; night clip at most 2%.
- Sound: layers present of the study's table.
- Cars passed blind.
- Across all: the week's hours against this list (the efficiency scoreboard); peak card MB against Windows' budget; worst frame against 33.3 ms.

## 5. PS5 gap list

None found under that name (searched 8 Nov). Nearest: the "PS5 corner" of 23 September changed 2.4% of pixels at over twice the cost; the gap was art: trims, unrepeating brick, wear, dressing, light by values (production/research/aaa-street/SUMMARY.md). Whether he means this: unverified. (9 Nov: the per-element list now exists, PS5-GAP-LIST-2026-11-08.md; §3's order follows its ranking, with the exceptions stated there.)

## 6. Open questions for him (scope or look)

1. Settled 8 Nov: the fishmonger and the empty unit to let are built in phase 2 (RULINGS line 17; progress.json line 83, "your yes, 8 Nov"). Removed 9 Nov; the numbers of questions 2 to 6 are kept so references to them hold.
2. Cars: P9's blind silhouette (about a day) before the 50 to 90 h? Recommended: yes.
3. The crowd's wardrobe: a 35-garment pool (56 to 238 h, RECS-BY-PHASE) or Hook rows 1 to 3 only? Recommended: rows 1 to 3.
4. Upper rooms: few fake rooms (Mafia 24 in about 8,100 windows) or every upper window (asset plan)? Recommended: few, in camera only.
5. The list exceeds the 2.00W ceiling: more weeks, or fewer pieces? Recommended: the hill and cars move first; quality stays (RULINGS 5 and 6 Nov). Moving cars reverses his 6 Nov ruling (order rule 11), so only on his word. (9 Nov: this recommendation now runs against §3's gap order; see FOR-ORDER-16-NOV-2026-11-09.md.)
6. Brick course: 75 mm (today's metric brick, every current map) or 86 mm (two scales on a period photograph give 85 to 88; TERRACE-KIT-TABLE §5)? Recommended: 86, decided before the bond so each wall is touched once.

## Fresh review (8 Nov)

One fresh reviewer, 8 Nov 2026; every cited file opened. Unit-cost sums re-done by hand; the draft's own arithmetic (230 to 340 h, 280 to 430 h, 380 to 600 h) reproduces, with the Hook rows at the 29.0 h estimate at both ends.

**Verdict: pass with fixes.**

Findings:
1. "Ceiling 2.00W ... a unit the lines read do not define (unverified)" is wrong: PLAN.md line 5 defines W as one weekly allowance (0.70W production). 2.00W is about 240 main-line hours at the order's 120 a week, so even the low 230 h meets the ceiling and "on paper it fits without cars" does not hold (PLAN.md lines 5, 28; orders/2026-11-09.md §2).
2. Double count: Hook rows 1 to 3 are Ron, Sheila and Darren (HOOK-GARMENT-LIST rows 1 to 3); Ron's clothes (12.4 h E) sit inside n09-5 and Sheila's inside n09-6, already in the week's 48 h (orders/2026-11-09.md §2).
3. "Fishmonger (bay 1) ... not built" overstates: an older fish-market front with its fascia, crates, awning and A-board stands in the corner's first 30 m (vignette-scene.json lines 367, 478, 520, 693; CORNER-PLAN line 7); its kit design failed its close review (orders/2026-10-25.md line 357), so the upper "designed too" figure is the likely one.
4. "Ten units; seven arrived": the ten include Mickey's (east_parade bay 0, shop-windows TARGET.md line 31), so eight of ten stand; progress.json's arrived list leaves Mickey's out because it is the corner.
5. 28 Oct question: the words do not support "trades on existing bays, so not new". The source order lists exactly these two (and Mickey's front) under "The shops not yet in the street (no new shops this order)" (orders/2026-10-25.md lines 354 to 357; RULINGS line 17 dates it 28 Oct, DECISIONS 25 Oct 19:25). What the words support: they were the shops meant, but the bar was scoped to "this order" and the phase-1 fallback; 2 Oct ("the other eleven shopfronts are made like it") and 3 Oct's trades place them in the street.
6. Missing from PLAN.md's phase 2 list: P7 walking (s07-02, s07-03 moved to phase 2), P6 plain clothes at 8 m, vegetation (asset plan family 9), real near shop rooms and food beyond the slab (families 2 and 6), s12-05 dynamic resolution (PLAN.md line 29; RECS-BY-PHASE line 43).
7. Dependency: the brick course (75 against 86 mm) is to be "decided before phase 2" (TERRACE-KIT-TABLE §5, 1) and the asset plan fixes the bond with the buildings (asset-plan SUMMARY, order 2); the draft copies the corner first and adds the bond after, so every wall would be touched twice; the course decision is not listed.
8. Question 5's recommendation that cars move first reverses his 6 Nov ruling and the order's rule 11 ("parked 1990 cars come with phase 2"); it may be asked, but should say so. Cars stay gated on P9 (RULINGS 2 Oct).
9. Furniture: "a small gate 0.5 h measured, UNIT-COSTS" misreads the source; UNIT-COSTS' 0.5 h is a review gate's session time, not a gate prop.
10. Dressing basis: Quay Street is 48 m with 36 m of frontage (studies/04 line 57), so less than 30 m remains beyond the corner; "1.75 h for 30 m, times 2 to 4" gives 3.5 to 7 h, not 6 to 12 h.
11. "Corner copied along the street" is a guess while a measure exists: a rough sum of the time log's n02-4-corner windows (people excluded) gives about 12.6 h for the corner (inferred by this reviewer, windows mixed); cite it.
12. Citations: "records run 2 to 4 times" is in CORNER-PLAN's post-review section (line 85), not §5; Martha, Kate and Leonard's 12 h is bodies only (HOOK-GARMENT-LIST line 43, "not in the total") and needs a crowd face first (line 44), and is not multiplied by the records' rate as the other estimates are.

Fixes: rewrite §2 against the 2.00W ceiling (about 240 h) and say plainly the list does not fit it; take Ron's and Sheila's rows out of the Hook figure (rows 1 to 3 less n09-5 and n09-6, about 6.3 h E for Darren plus Sheila's remainder); restate the fishmonger as a front to replace, designed again; eight of ten; replace question 1's reason with the scope reading of finding 5; add P7, P6, vegetation, near shop rooms and food, s12-05 with guesses; put the brick course question to him and move the bond ahead of the corner's copy; mark question 5 as reversing rule 11; correct findings 9 to 12's figures and citations.

## Fixes applied (8 Nov)

Each cited source re-opened before the change (PLAN.md, orders of 25 Oct and 9 Nov, HOOK-GARMENT-LIST, vignette-scene.json, CORNER-PLAN, shop-windows TARGET.md, progress.json, RULINGS.md, RECS-BY-PHASE, TERRACE-KIT-TABLE, asset-plan SUMMARY, UNIT-COSTS, studies/04, the time log's n02-4-corner lines, 3-PROOFS.md). The body was shortened to stay under 1,300 words (an estimate by hand; no counter was run). Corrected 9 Nov: that held for the 8 Nov text (about 1,390 words at HEAD by wc, REVISION-REVIEW fix 13); the revised body above the reviews ran about 2,380 words by the same count before the 9 Nov review fixes, and longer after them. It was not shortened; no counter was run for the new length.
1. Applied: §2 rewritten against the 2.00W ceiling, about 240 h (W as the order's 120 h a week marked inferred); the excess put to him as question 5.
2. Applied: the Hook figure is Darren 6.3 h E plus Sheila's remainder, 6.3 to 16.6 h E.
3. Applied: the fishmonger is a front to replace, designed again; both units at the designed figure, 16 to 37 h.
4. Applied: eight of ten.
5. Moved to open questions: question 1 reworded on the scope reading, recommended yes, for his ruling. (9 Nov: settled by his yes of 8 Nov, RULINGS line 17.)
6. Applied: P7, P6, vegetation, near shop rooms, food and s12-05 added with guesses (P7, P6, P11 and P16's day counts from 3-PROOFS.md).
7. Applied, and moved to open questions: the bond now precedes the corner's copy (order step 3); the course, 75 or 86 mm, is question 6, recommended 86.
8. Applied: question 5 says it reverses order rule 11; cars stay gated on P9.
9. Applied: the misread 0.5 h removed; gates' 0.5 to 0.85 h session time cited as such.
10. Applied: dressing 3.5 to 7 h.
11. Applied: the corner's 12.6 h cited as the reviewer's inference; the guess kept at 10 to 20 h.
12. Applied: CORNER-PLAN citation corrected; Martha, Kate and Leonard marked bodies only, a crowd face first, 24 to 48 h at the records' rate; their 12 h E stays in the plan-figure total as before.
