# Street furniture and lamps: a build plan per piece (lane, 17 Nov 2026)

For waiting item 4 of the order of 16 November. Machine-free part only: what to reuse, what to build, how each piece is checked, and what the lane's research of today changes in the target. Nothing here was built or rendered. Written by the cloud lane, which did not write the target.

Inputs: production/research/phase2-plan/TARGET-STREET-FURNITURE-2026-11-17.md (rows S1 to S13, W); the street as emitted (production/specs/vignette-pieces.json); the built models (production/assets/street/clutter/*.glb); today's two research files, production/research/lane/FURNITURE-SPECS-2026-11-17.md and production/research/lane/KERBSIDE-RULES-1990-2026-11-17.md (all pages opened 17 Nov 2026).

New screen: tools/lane/furniture_check.py (21 tests pass, `python -m unittest tools/lane/test_furniture_check.py`). It reads the emitted street, imports the street recipe read-only for what it really draws in place of the held props (clutter_placements: the bin moved 0.9 m clear of column 0, the grit bin and milk crates it adds, the name plate it hangs), and measures each built model from its own glTF bounds, then prints PASS, FAIL, MISSING or UNMEASURED per target row. It is a screen before a rebuild, never a pass: pieces pass only in the packaged walk.

## 1. What the screen found on today's street (run 17 Nov, 19:45, after a fresh review's fixes)

| Row | Line | Found | Target | Verdict |
|---|---|---|---|---|
| S1 | four columns, 10 m staggered, axis 3.725 m | x 8 E, 18 W, 28 E, 38 W, axis 3.725 | same | PASS |
| W | walker's gap at every footed thing on a footway, pieces overlapping along the street taken together | smallest 0.788 m (the west yard mouth's barrier, crates and barrel together) | 0.68 m (the tester's walker, scene note of 29 Sep) | PASS, all 27; drawn models' depth across the street is their box size, an approximation of their turn |
| S5 | public bins on 48 m | 3, as drawn at 8.9 E, 30 E, 33 W | at most 3 (the litter-bins target asks 6.6 and 35.2 E) | PASS on count |
| S5 | litter-bin.glb overall height | 1.000 m | post 1.255 m, rim 1.050 m | FAIL |
| S6 | bollards at the yard mouth only | 20.7 and 24.3 W | same | PASS |
| S6 | bollard.glb height (open question 2 of the target) | 0.765 m | 1.082 m | FAIL |
| S7 | kiosk place | x 16.5, centre 3.675 | same | PASS |
| S7 | kx100-kiosk.glb plan and height | 0.890 x 0.918 x 2.192 (the extra 28 mm on one side is not explained; a door handle or lid skirt is a guess) | 0.890 x 2.192 | PASS within 30 mm |
| S8 | pillar-box.glb height | 1.48 m (footprint 0.558 m, cap included) | 1.50 m | PASS against the target, but see 2.2 |
| S11 | guard rail panels and post axis | 1 panel, axis 0.375 m | same | PASS |
| S11 | infill bars per panel | 5 tubes | 17 bars | FAIL (the known tube rail) |
| S12 | gully grate plan | 0.400 x 0.400 | 0.440 x 0.290 | FAIL, but see 2.4 |
| S9 | street name plate | drawn by the recipe (NAME_PLATE_AT): 0.90 x 0.26 m, centre 2.63 m, west corner pier, lettered | 0.98 x 0.20 m | DIFFERS in size only (advisory) |
| S10 | bus stop | none | one | MISSING (known) |

Not measured by the screen: colours, wear, the lanterns' light (S2 to S4 stay with the street-weathering skill's own tools, pool_clip.py and measure_night_pools.py), and the rim height of the bin (needs the mesh, not its box).

## 2. What today's research changes in the target (for the main session to accept or reject)

2.1 Yellow lines need time plates in 1990. Confirmed from a primary source, re-read by the lane itself: a written answer in the Commons, 11 March 1991, says double yellow lines restrict waiting "for at least eight hours" "between 7 am and 7 pm on at least four days per week", and "the timing and direction of the prohibition or restrictions are displayed on plates placed at regular intervals along the length of the carriageway so restricted" (https://api.parliament.uk/historic-hansard/written-answers/1991/mar/11/parking, read 17 Nov 2026; a Scottish Office minister answering, under regulations that applied across Great Britain). Double yellows came to mean "at any time" only with the 1994 rules (in force 12 August 1994), which still required plates; double yellows without plates came with the 2002 rules. So the scene's line "double yellows mean no waiting at any time" (vignette-scene.json, the parking meter's not_placed reason) is wrong for 1990, and target row S13's "none is placed" should become: small upright time plates at intervals along both kerbs, on the lamp columns where they stand (a 1965 trade report on the then new system says the times "will be shown on plates erected alongside (normally on lamp posts)", and of yellow lines "with plates on the lamp posts stating the hours and days of operation": https://archive.commercialmotor.com/article/8th-january-1965/28/markings-for-loading-bans, read by the lane 17 Nov 2026). The plate's 1981 diagram, colours and wording were not reached (the 1981 regulations on legislation.gov.uk did not open from the cloud): read them from the PC before modelling. Recommended: accept, plates on the four columns plus at most two short posts, words only from the 1981 diagram once read.

2.2 Pillar box: the target's 1.50 m and 489 mm body mix two box types. A Type B (Carron, about 1966) stands about 1,346 mm above ground with a body about 381 to 388 mm across; a Type K (installed 1980 to about 2000) stands about 1,346 mm with a 483 mm body and no separate cap. Type A boxes were cast only from 1991, so not in 1990. The built model is 1.48 m tall and 0.558 m across at its widest (cap included; the body alone needs the mesh): taller than either. Its place is not checked: the target says front to the building line, while the scene stands it 0.725 m from the kerb. Recommended: a Type K (about 1.35 m, 483 mm, one-piece top), because the target's body width already fits it and a 1980s street would have new ones; the slot height (target 1,278 mm) must then come down below the top and is still unverified. Sources in FURNITURE-SPECS (ukaa 9231 and 10326, salvoweb 29780, lbsg.org, all read 17 Nov).

2.3 Bollard: the built model (0.765 m) is far under the target's 1,082 mm; the only makers reached (modern cast reproductions) give 1,140 to 1,223 mm high and 210 to 225 mm across. No 1980s source. Recommended: rebuild to about 1.10 m (the target's number nudged into the makers' range), foot 210 mm, keeping the target's bead and domed cap.

2.4 Gully grate: 440 x 290 mm matches no UK size found; common kerbside clear openings are 430 x 370 and 450 x 450 mm (BS 497's own table, withdrawn and paywalled, not read). The present grate is 400 x 400. Recommended: 450 x 450 mm overall with 430 x 370 as the alternative, eight slots kept; this also means the target's "a 400 mm square grate, to replace" should read "a grate under about 430 mm".

2.5 Lamp: a mounting height of about 4.6 to 5 m and the 35 W low-pressure sodium lamp are confirmed for 1990 (Thorn's own Beta 5 sheet: "Recommended height 5m", "Lamp: 35W SOX"; note 5 m is a mounting height, while the target puts the lantern top at 5.0 m, so the target sits at the top of the range; made from about 1970 to August 2008, common on side streets from the early 1980s). Note: on a cranked bracket the lantern was the top-entry Beta 5; on a straight side arm, as lamp_post_C has, the side-entry one (the target does not name the entry; lamp_post_C's scene note calls it a side-entry lantern). Canopy size, shaft section, arm length and door position: still unverified (no maker catalogue reached).

2.6 Kiosk: 890 x 890 x 2,192 mm confirmed (britishtelephones.com, KX series from 1985). Nothing to change.

2.7 Guard rail: BS 3049 (1976 to 1995) was in force in 1990; its text was not read. Later drawings of the same design give 2,000 mm panels about 1.0 m high with 12 mm round bars at about 110 mm centres (about 17 per panel, matching the target), unverified for 1990. A high-visibility variant built to BS 3049 existed (date unknown). Nothing to change; the row stays Judgement.

2.8 Bus stop: the flag outside London was diagram 970 (Calvert's bus symbol and "Bus stop" in the Transport typeface), and after 1986 several operators' flags often shared one pole; a 1971 flag measured about 1 ft x 1 ft 6 in. The target's 300 x 285 mm flag is smaller than that 1971 flag (about 300 x 450 mm) and has no 1980s source; it stays Judgement, and 300 x 450 mm is the better-sourced size; the operator on the flag must be fictional (canon).

2.9 Name plate (already drawn by the recipe, Kindersley-style capitals per its own note): street name plates were not traffic signs; the Ministry's 1950 Kindersley serif capitals were widespread on plates from the 1970s to the 1990s, and the sans-serif guidance (Circular 3/93) came three years after 1990. His ruling of 30 Sep (Marcellus SC, a serif capital) fits that. Plate size: no source; the target's 980 x 200 mm stays Judgement.

2.10 Litter bin: no 1980s source; modern post bins hold about 40 L. The built model is 1.00 m tall overall against the target's 1.255 m post (itself Judgement). Recommended: leave the bin until a dated photograph is found; it is the weakest-sourced piece and the screen's FAIL here is against a judged number.

## 3. The plan per piece (reuse first; who does what)

Hours are lane estimates (Judgement), for the next order to cost. "Main" means the main session on the PC; "lane" means this cloud lane can do it without a machine.

| Piece | Route | Steps | Check | Hours |
|---|---|---|---|---|
| S1 lamp columns | Reuse lamp_post_C as it is | none for placement | screen S1 PASS; gate already passed 21 Oct | 0 |
| S2 column staining | Finish the baked StainMap (owed: plain middle 2.4 m, lime that reads painted, chipped arris) | main: bake round in Blender, gate views close and street | gate against the Geograph crops and last-good picture | 3 to 4 |
| S3, S4 lanterns and light | Keep; the bowl drift (12 levels) is a listed shortfall | main: measure C4 (pool at least 4x gap) once with measure_night_pools.py | pool_clip 2% or less; C4 measured | 1 |
| S5 litter bins | Keep litter-bin.glb; move places to the target's 6.6 and 35.2 E (open question 1) only after a placement check | main: one scene edit; lane can pre-check with the screen | screen S5 and W lines | 0.5 |
| S6 bollards | Rebuild bollard.glb in its own script to about 1.10 m (2.3) | main: Blender script run, re-export | screen S6 height within 5%; gate street view | 1.5 |
| S7 phone box | Keep kx100-kiosk.glb | none | screen S7 PASS; known faults stay in FINDINGS | 0 |
| S8 pillar box | Re-proportion pillar-box.glb as a Type K (2.2) after the main session accepts | main: script change and re-export; slot height from a photograph | screen S8 (research line) PASS; gate close view | 1.5 |
| S9 name plate | Reuse: the recipe already hangs a lettered plate (0.90 x 0.26 m) on the west corner pier | main: decide target size or built size; if the target's, one constant changes (NAME_PLATE_AT) and the picture is re-made | gate close view; screen S9 | 0 to 1 |
| S10 bus stop | New: pole, diagram 970 style flag with a fictional operator, timetable case | main: script build, place at x 46 W | screen S10 PASS; W gap; gate street view | 3 |
| S11 guard rail | Replace the 5-tube rail with a 17-bar panel | main: emitter change in the street recipe | screen S11 infill PASS; W gap | 1.5 |
| S12 gully and covers | Replace the 400 mm grate with 450 x 450 (2.4); covers stay as decals | main: model and re-export, set_in place kind unchanged | screen S12 PASS against the new size; flush check | 1.5 |
| S13 time plates | New: plates for the yellow lines (2.1), only after the 1981 diagram is read from the PC | main: read SI 1981/859 Schedule 2 first, then a small plate model on the columns | gate street view; screen line to add when the diagram is known | 2 |

Total about 16 to 18 hours, of which about 11 are Blender and scene work on the PC. The lane can take next: the bus stop's and the time plate's generator code (pure Python geometry with tests, Blender side untested, as for the parked car), and the screen's line for the time plates once the diagram is read.

## 4. For the main session to decide

1. Accept 2.1 (time plates on the yellow lines, after reading the 1981 diagram). Recommended: yes.
2. Pillar box as a Type K at about 1.35 m (2.2). Recommended: yes.
3. Bollard to about 1.10 m; gully grate to 450 x 450 mm (2.3, 2.4). Recommended: yes.
4. The name plate: keep the built 0.90 x 0.26 m or move to the target's 0.98 x 0.20 m. Recommended: keep the built one (no source sets either size; it is lettered and placed).
5. Merge tools/lane/furniture_check.py as a screen (not a ci gate until the target's corrections are settled).

None of these is his: they are period facts and sizes within the target, decided by the main session under its rulings.

## Review

A fresh read-only reviewer (17 Nov, about 19:40) passed this plan and the screen WITH FIXES: the name plate the recipe already draws, the walker's gap taken from the scene rather than what the recipe draws (bin move, grit bin, milk crates, A-board, pieces side by side), the bus flag size, the lamp height wording, the 1965 quote, the pillar box footprint label, the bin places, the 1994 and 2002 split, and the kiosk's extra width. All applied above and in the screen; five tests added for them.

## Unreached (17 Nov)

The 1981 traffic sign regulations' text (legislation.gov.uk did not open from the cloud); BS 3049, BS 497 and BS 1308 (paywalled); any Concrete Utilities or Stanton column catalogue; Wikipedia's pillar box and parking restriction pages (the helpers' permission prompts timed out); any 1985 to 1995 photograph of a bollard, litter bin, guard rail or name plate.
