# Terrace kit table and period targets: one plain house family (29 October 2026)

His order D14, step 1 of the town kit's first use (production/orders/2026-10-25.md, o28c-d14-town-kit), written by a fresh helper, not the builder. It applies MAFIA-KIT-2026-10-28.md sections 5.1 to 5.6 and its review. A research trial outside the game: Quay Street as built is read, never changed. Every file below was read on 29 October 2026. Tags: **M** measured here on a repository picture; **R** read in a file; **I** inferred; **U** unverified.

Revised after its fresh review (TERRACE-KIT-TABLE-REVIEW-2026-10-29.md); section 7 lists the changes.

Short names:
- TF: tools/art-recipes/terrace-front.py
- VS: production/specs/vignette-scene.json
- SW: tools/art-recipes/sash-window (window_design.py) and production/art/sash-window/target.json
- HW: production/cloud-week/targets/house-windows/TARGET.md; its kit is production/cloud-week/kit/house-windows/build_windows.py, with hw_t.py
- DR: production/cloud-week/targets/front-door/TARGET.md (door 3.1); its kit is production/cloud-week/kit/door/build_door.py
- FD: production/cloud-week/targets/front-doors-all/TARGET.md; its kit is production/cloud-week/kit/front-doors-all/build_doors.py
- A2: production/art/atlas-02/research/hillside-housing-dated-series.md

## 1. The photographs measured

Nothing was downloaded. Two dated photographs held as previews in production/previews/cloud-week/refs/ were measured by script. Each is scaled by the door leaf FD boxed on it.

- **G1: Geograph 2321423, Ratcliffe Street, Levenshulme, 10 June 1994** (A. Parkes, CC BY-SA 2.0). A brick terrace seen square on.
  - Previews: p6-levenshulme… (×1.6) and d3-levenshulme… (×4.0).
  - Scale: 10.07 mm per original pixel (FD's D3 leaf).
  - Both crops give the same course pitch (8.44 and 8.6 px), so they share one pixel frame.
  - The reviewer re-measured G1 with an independent brick-length scale and agrees within 3%, at most 10%.
- **G2: Geograph 689253, Frederick Street, Barnoldswick, 10 April 1990** (N. Clifton, CC BY-SA 2.0). A stone terrace.
  - Preview: p7-barnoldswick… (×2.4).
  - Scale: 21.66 mm per original pixel, from FD's D4_T3 leaf.
  - **That scale does not carry to the middle house**, where the figures were taken. There, its own door leaf reads 1.68 m and its neighbour's 1.57 m, so the view is oblique or stepped.
  - Every G2 size is therefore **U**. Only its shapes are used: flat heads, and a small window over the door.

| Measure (M) | G1 (brick, 1994) | G2 (stone, 1990) |
|---|---|---|
| Brick course | **85 to 88 mm**: 85.0 on the upper wall, 86.9 beside the door; the reviewer, by brick length, 85 to 87. Brick plus joint 216 to 224 | stone, none |
| Upper window opening | 1.00 to 1.06 × 1.62 to 1.69 m | U (read 1.14 × 1.6, likely 15% low) |
| Threshold to upper sill / to eaves | 3.70 to 3.72 m / 5.66 to 5.71 m; the lintel sits directly under the gutter | U (read 4.7 m eaves, likely 5.4) |
| Door opening | 0.86 to 0.89 m between reveals; head 2.60 m above the leaf's foot | – |
| Plot, party line to party line | 3.88 to 3.90 m | U |
| Upper sill | face 150 to 190 mm; 90 to 97 mm past each jamb | – |
| Upper lintel | flat stone, about 330 mm deep; 70 to 79 mm past each jamb | – |
| Downpipe | 70 to 95 mm (one pixel is 10 mm) | – |

HW (D4) adds that G1's ground bay sill stands 0.85 ±0.05 m above the step (R).

**G1's ground floor is a canted bay** (about 1.96 m wide), and its doors pair around a 0.36 m pier. This family is flat-fronted, as HW's P1 and P2 (Hull, 1985 and 1986) show, so no bay (a bay would add four to six meshes). Its doors stand 1,125 mm apart when two handed houses meet. The session records both choices in DECISIONS.

## 2. Period targets

Photographs win over books and trade sizes (RULINGS, 8 October). His rulings stand over photographs until he answers.

| Target | Value | Sources (R) | Photograph | Status |
|---|---|---|---|---|
| Grid | course 75, brick 225 | VS facade: brick_course 0.075, "65 mm brick plus a 10 mm bed joint": today's metric brick, trade_standard, not a period source | G1: **85 to 88** by two independent scales | **Disagrees**: open item 1. The trial keeps 75 |
| Storeys, floor to floor | ground 2,925 (39 c); repeatable upper 2,925; top 2,775 + 150 eaves course. Eaves 5,850 (2 storeys) or 8,775 (3) | VS 3.4 / 2.8 (shop parade). A2: clear heights 2.62 to 2.74 / 2.54 to 2.62 (forum, via search summary: weak); by-law minimum 8 ft. TF hill houses 3.3 / 2.7 (judgement) | G1: upper sill 3.70 to 3.72 (ours 3.724); eaves 5.66 to 5.71 (ours +2.5 to 3.4%) | **Changed** from MAFIA-KIT 5.1's 3.375 / 2.775 |
| Main window | **1,012.5 × 1,676.4**, head 2,475 (33 c) on the grid; sill 798.6 above the floor | RULINGS 8 Oct: "1.68 m" (his ruling builds the height). SW and HW: 850 × 1,676.4 (850 is the street's width) | G1: 1.00 to 1.06 × 1.62 to 1.69 | Width **changed** 850 → 1,012.5 (4½ bricks). Height kept by his ruling: a 26.4 mm grid exception, recorded in DECISIONS |
| Small window over the door | 450 × 1,200, sill 1,275 | none | G2 shows one (size U) | **U** |
| Door | opening 900 × 2,475 (4 × 33), head in line with the window heads; leaf 812.8 × 1,948; fanlight 452 | DR: opening 882, crown 2,340, from DR's P1 (Teignmouth, 2012: outside the period). FD W8: G1's leaded light about 604. VS side door 838 × 1,981 | G1: 0.86 to 0.89 wide, head 2.60 | Head 5% under G1; the built doors' 2,340 is 10% under, hence the re-run (section 3) |
| Plot width | mid-terrace 4,050 (18 bricks); three-storey end house 5,400 (24) | VS 6.0 bays are shop units (judgement). procedural-density.md: 4.5 to 6 m (search summaries). A2 HOLE 1. MAFIA-KIT 5.1: 5.4 to 6.075 (I) | G1: 3.88 to 3.90 | Mid **changed** (+4% on G1); end house **U** |
| Sill | 150 high (2 c), 50 proud, **112.5 past each jamb** | VS 75 thick, 50 proud, 50 past. SW stone sill 127 × 50.8, 76.2 past (Rivington: 4 to 6 in thick) | G1: 150 to 190; 90 to 97 past | Height **changed** (127 → 150). Overhang **16 to 25% over G1**, set by the half-brick step: flagged |
| Head | flat stone lintel 300 (4 c), 12 proud, **56 past each jamb**; or a camber arch, ring 225, rise 1/50 (245 at the crown) | VS lintel 150. TF segmental arch, rise 1/7, ring 215 (Quay Street's). DR §4.7: DR's P1 camber, 13 bricks on end, camber 18 over 882 | G1: about 330 deep, 70 to 79 past. HW's P1 and P2 (Hull): flat painted heads, by eye | Lintel **changed** 150 → 300. Overhang **20 to 29% under G1**, quarter-brick step: flagged. The 1/50 arch rests on a 2012 photograph: **U**. TF's 1/7 arch would rise 86 mm into the floor band |
| Chimney | stack 900 × 450 (4 × 2 bricks), 975 above the ridge; cap 2 courses each stepping out 56, top 1,125 × 675 | VS 0.9 × 0.45, 1.0 above the ridge (trade_standard). TF cap and pots: 600 high, 280 to 240 across, three or four a stack. TF rejects the held pot files: at 0.67 and 0.95 m across they are whole stacks | none measurable | **U** |
| Gutter, fascia | 112 half-round; fascia 200 × 25 | VS (trade_standard); TF 115 × 75 | not measurable | **U** |
| Downpipe, hopper, shoe | Ø 68; 250 × 200 × 200; 150 | VS (trade_standard) | G1 pipe 70 to 95 (a pixel is 10 mm) | **U** |
| Roof, depth, plinth, air brick | 35°; 7,875 deep; plinth 450; air brick 225 × 75 | VS (trade_standard and judgement); WINDOWS-FACADES item 7 (I); A2: the 1878 Act's under-floor ventilation (search summary) | none | **U** |

## 3. The kit table: 39 meshes

**Rows.** Each storey is one row of modules 2,775 high (37 courses). Ground and repeatable upper floors add a 150 floor band; the top floor adds a 150 eaves course. Bricks are 225 across and courses 75 high.

**Fitting.** "Fitted" pieces scale within 10%; everything else is fixed.

**Pivots** (MAFIA-KIT 5.1):
- Wall and linear pieces: bottom-left, on the wall face.
- Joinery, sills, lintels and arches: the opening's bottom centre.
- Doors: the hinge side of the frame's foot.
- Pipes, stacks, pots and the air brick: bottom centre.

**Sheets.** W is the tiling wall: kit-materials.json's "brick" kind, the new "render" kind as a material swap, and engineering brick for the plinth. R is the tiling roof. T, S and M are the timber, stone-and-stucco and metal trim sheets.

**Names.** Opening pieces are named by their opening, as MAFIA-KIT 5.1 does.

**Counts** are for house C (5,400 wide, three storeys, at the row's right end): G ground, U repeatable upper, T top, R/E roof and end.

| # | Mesh (SM_TK_…) | Size (bricks × courses) | Fixed / fitted | Sheet | From (re-run, or new) | G·U·T·R/E |
|---|---|---|---|---|---|---|
| 1 | Wall_450x2775 | 2 × 37 | fitted | W | re-run: TF piers (`_plain_ground`, `_upper_floor`) | 1·2·2·3 |
| 2 | Wall_675x2775 | 3 × 37 | fitted | W | re-run: TF piers | 2·2·2·3 |
| 3 | Wall_1350x2775 | 6 × 37 | fitted | W | re-run: TF `plan_end_walls`. The side is 5 × #3 + #2 + #1 = 7,875 | –·–·–·15 |
| 4 | WallWindow_1125x2775: opening 1,012.5 × 1,676.4 centred, head 2,475, half-brick reveals | 5 × 37 | fixed | W | re-run: TF bands and piers round openings | 2·2·2·– |
| 5 | WallWindow_450x2775: opening 450 × 1,200 | 2 × 37 | fixed | W | re-run: same | –·1·1·– |
| 6 | WallDoor_900x2775: opening 900 × 2,475 | 4 × 37 | fixed | W | re-run: TF `_plain_ground` | 1·–·–·– |
| 7 | PartyPier_225x2775: a straight joint, one per plot boundary | 1 × 37 | fixed | W | new | 1·1·1·– |
| 8 | Corner_225x2775: a one-brick return at each row end | 1 × 37 | fixed | W | new | 1·1·1·– |
| 9 | Gable_7875x2925: 150 straight, then a 2,775 rise (35.2°) | 35 × 39 | fitted | W | re-run: TF `plan_end_walls` gable | –·–·–·1 |
| 10 | FloorBand_1350x150, 25 proud | 6 × 2 | fitted | W | new (TF's bands are flush panels) | 4+6·4+6·–·– |
| 11 | Plinth_1350x450, 12 proud | 6 × 6 | fitted | W | new | 4+6·–·–·– |
| 12 | Eaves_1350x150, oversails 56 | 6 × 2 | fitted | W | re-run: TF eaves_course | –·–·4·– |
| 13 | Sash22_1012x1676: two-over-two | opening | fixed | T | re-run: SW window_design.py through LEDGER_SASH_TARGET, on a new target file; width only changes | one kind a house: 1 per #4 |
| 14 | Sash11_1012x1676: one-over-one | opening | fixed | T | re-run: same | C: 2·2·2·– |
| 15 | Casement_1012x1676: 1980s replacement (HW RC) | opening | fixed | T | re-run: build_windows.py (hw_t.py), on a new target file | (house B) |
| 16 | Sash11_450x1200 | opening | fixed | T | re-run: SW, new target file | –·1·1·– |
| 17 | Door_T1_900x2475: a whole door (frame, four-panel leaf, transom, 452 fanlight, stone step) | opening | fixed | T | re-run: build_door.py, on a new target file | one kind a house |
| 18 | Door_T2_900x2475: four lights (FD T2) | opening | fixed | T | re-run: build_doors.py, new target file | (house B) |
| 19 | Door_T3_900x2475: moulded modern (FD T3) | opening | fixed | T | re-run: same | C: 1·–·–·– |
| 20 | Fascia_1350x200, 25 thick | 6 × – | fitted | T | new (no recipe) | –·–·4·– |
| 21 | Sill_1012: 1,237.5 long × 150 | 5½ × 2 | fixed | S | re-run: TF upper_sill | 2·2·2·– |
| 22 | Sill_450: 675 long | 3 × 2 | fixed | S | re-run: TF upper_sill | –·1·1·– |
| 23 | Lintel_1012: 1,125 × 300 | 5 × 4 | fixed | S | new | flat-headed terraces |
| 24 | Lintel_450: 562.5 × 300 | 2½ × 4 | fixed | S | new | |
| 25 | Lintel_900: 1,012.5 × 300 | 4½ × 4 | fixed | S | new | |
| 26 | CamberArch_1012: ring 225, rise 20 | 245 at the crown | fixed | S | re-run: TF `_segmental_arch` at a new rise and ring | C: 2·2·2·– |
| 27 | CamberArch_900 | 243 at the crown | fixed | S | re-run: same | C: 1·–·–·– |
| 28 | CamberArch_450 | 234 at the crown | fixed | S | re-run: same | C: –·1·1·– |
| 29 | Verge_4800 | – | fitted | S | new | –·–·–·2 |
| 30 | RoofSlope_1350x4800 | 6 × – | fitted | R | re-run: TF roof_front | –·–·–·4 (+4 back) |
| 31 | Ridge_1350 | 6 × – | fitted | R | new (TF has no ridge piece) | –·–·–·4 |
| 32 | Gutter_1350, 112 half-round | 6 × – | fitted | M | re-run: TF gutter. Poly Haven modular_metal_gutter (CC0) is a candidate | –·–·4·– |
| 33 | Downpipe_68x2925, on #7 only | – × 39 | fitted | M | re-run: TF downpipe | 1·1·1·– |
| 34 | Hopper_250x200 | – | fixed | M | new (VS sizes) | –·–·1·– |
| 35 | Shoe_150 | – | fixed | M | new (VS sizes) | 1·–·–·– |
| 36 | AirBrick_225x75 | 1 × 1 | fixed | M | new | 2·–·–·– |
| 37 | Stack_900x450 | 4 × 2 plan | fitted (height) | W | re-run: TF chimney_stack | –·–·–·2 (party, end) |
| 38 | StackCap: 2 courses, each stepping out 56; top 1,125 × 675 | 5 × 3 at the top | fixed | W | re-run: TF chimney_cap (oversail 60 → 56) | –·–·–·2 |
| 39 | Pot_280x600: a roll-top; terracotta or buff by material | – | fixed | own | re-run: TF `_pot_mesh` and `plan_pots` | three or four a stack |

**Where the meshes come from.**
- Reused as built: 0.
- Re-run from a named recipe: 26.
- New: 13 (#7, 8, 10, 11, 20, 23, 24, 25, 29, 31, 34, 35, 36).
- The reviewer expected about 3 reused, the doors as built. They are re-run because their 2,340 head and 267 fanlight sit 10% under G1, a 1994 photograph; their passed numbers are 3.1's, from a 2012 photograph. The session records this in DECISIONS.

**No re-run reads Quay Street's targets.**
- The sash goes only through LEDGER_SASH_TARGET, set to a new target file.
- build_door.py (line 46), hw_t.py (line 13) and build_doors.py read fixed target paths today. A target switch like the sash's must be added before any re-run.

**Fitted pieces.** 14 of 39, all walls, linear runs and the stack's height. Every opening and its parts keeps its size, as Mafia keeps 88% of its windows and doors within 10%.

**Off-grid exceptions** (fixed). Everything else (piers, walls, bands, openings 900 and 450, storeys, plots) is on the grid.
- The main window opening, 1,012.5 × 1,676.4: half a brick across, his ruling up (sill line 26.4 mm off the grid).
- Sill and lintel lengths, on half- and quarter-brick steps.
- The stack cap's quarter-brick steps.
- The arches' crowns.
- Made objects that are not coursed: doors (leaf 812.8; their step 300 deep), fascia 200, gutter, pipes, hopper, shoe and pots.

**Decal anchors** (MAFIA-KIT 5.3, by WEAR's rule): the sills, the hopper and the shoe. A median of 1 decal per front, and at most 6 on the walked path.

## 4. The trial's three houses

All three use the grammar [Ground][Upper]*[Top] and are written left to right.

**The boundary rule.**
- Every plot starts with #7 (its left boundary), whichever way the house is handed.
- A row's ends take #8.
- Downpipes and party stacks stand on #7 only.
- A check: each internal boundary has exactly one #7 and one downpipe, and no row end has either.

**A. Two-storey mid-terrace, seed 1.** 4,050 wide; flat lintels, Sash22, Door_T1, brick.
- G: 7, 1, 6, 2, 4, 2
- T: 7, 2, 5, 1, 1, 4, 2
- The small window is centred over the door, and the main windows line up above each other.

**B. The same, seed 2.** Handed (its contents mirrored inside its boundaries) with no small window; Casement, Door_T2, render wall.
- G: 7, 2, 4, 2, 6, 1
- T: 7, 2, 4, 1, 1, 1, 2
- B differs from A in its module string, wall variant and door: MAFIA-KIT 5.2's neighbour rule and check 5.5.3.

**C. Three-storey end house, at the row's right end.** 5,400 wide; camber arches, Sash11, Door_T3.
- G: 7, 2, 4, 1, 6, 2, 4, 8
- U and T: 7, 2, 4, 2, 5, 1, 1, 4, 8
- Side wall: 3, 3, 3, 3, 3, 2, 1 a storey, with its bands, the gable (#9), two verges and the end stack.

**Distinct meshes on each whole front** (front, roof and stacks; the target is at least 15):

| House | Whole front | Facade alone |
|---|---|---|
| A | **28** | 23 |
| B | **24** | 19 |
| C | **32** | 27 |

## 5. Open (for the owner)

1. **Brick course (the look).** Should it stay at 75 mm (Quay Street, and every brick map) or move to 86 mm?
   - The case for 86 is stronger than first written. Two independent scales on G1 give 85 to 88 mm. VS's 75 is arithmetic on today's 65 mm brick, not a period figure.
   - *Recommended: 75 for this trial only*, so it can be judged beside Quay Street. The course stays one number in the kit's data, and 86 is decided before phase 2.
2. **Scope and hours.** The module step was budgeted at about 25 modules and 12 to 16 hours, against MAFIA-KIT's own 30 to 45 meshes. With 39 meshes, 26 of them re-runs needing new target files, *expect 22 to 28 hours*. That raises the trial to about 60 to 82 hours. Cutting meshes does not close the gap. *Recommended: keep 39.*
3. **Licences.** Copying structure from Epic's PCG sample is still open (MAFIA-KIT question 3; recommended: structure only). Poly Haven's gutter is CC0 and allowed (allowlist item 2). G1 and G2 are measured only, never shipped. No new question.
4. **Quay Street stays untouched.** TF, VS and the built sashes and doors are only read. Every re-run writes new files through a new target. If this family later stands beside Quay Street, its wider windows, lower storeys and flat lintels will differ from the cottages drawn from the Hook sheet. That goes to his page in phase 2.

## 6. Unverified and not reached

- **Scale.** G1's mm figures rest on FD's assumed leaf of 1,927.6 mm (±3%). Only the brick-length check is independent of it.
- **G2.** Its sizes are unverified; its scale fails away from its scale door.
- **Sample.** Every size target rests on one brick terrace in a northern mill town, not a port.
  - The Hull photographs (HW's P1 and P2; FD's D6 to D8) are oblique, and their courses do not resolve.
  - Thicker northern bricks have no source here (U).
  - A2's and procedural-density's figures are search summaries.
- **Not reached:** full-size originals (downloads need his yes); any measurable stack, gutter or eaves; a measured drawing of a by-law terrace; Historic England's pages.
- **Measuring.** The script ran inline and was not kept; the figures can be re-measured from the two previews.

## 7. Revised after review (29 October 2026)

1. **G2.** Its window, storey, eaves and plot sizes are now unverified (the scale fails away from its door), and it is dropped as evidence.
2. **Window.** It is built at his ruling, 1,676.4 high, with the head on the grid at 2,475 and a 26.4 mm exception for DECISIONS. The window-height open item is gone. With G2 gone, the width follows G1: 1,125 → 1,012.5.
3. **Pots.** The held pots are dropped (TF rejected them as whole stacks). One pot from TF's builder replaces them, three or four a stack.
4. **Doors.** They are whole doors (#17 to 19), re-run at G1's head; the separate frame and step are gone. The fascia, floor band and ridge are new, and the hopper and shoe are new too. Every re-run names its recipe and a new target file. Counts: 0 reused, 26 re-run, 13 new.
5. **Grid.**
   - The end wall is 5 × #3 + #2 + #1.
   - The gable carries the 150 course.
   - The cap tops out at 1,125 × 675.
   - The arches are named by their real crown height.
   - The remaining off-grid sizes are listed as fixed exceptions.
6. **Overhangs.** Sill and lintel overhangs are flagged against G1: lintels moved to 56.
7. **Party piers.** One per boundary, by the boundary rule and its check. House B is re-strung, and house C stands at the row's right end.
8. **Ground bay.** G1's ground bay and paired doors are noted, and the flat-front choice goes to DECISIONS.
9. **Small fixes.**
   - The d3 zoom is 4.0, giving 86.9 mm.
   - "P1" now names its file (Teignmouth 2012 against Hull 1985).
   - House C's count sits on #14.
   - Opening pieces are named by their opening.
10. **Hours and fronts.** The module step is now 22 to 28 hours, and item 1's evidence is restated. Module count 42 → 39; fronts 31/27/35 → 28/24/32.
