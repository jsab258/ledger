# Quay Street's milk crates: the exact target

**The milk crates are a stack of three 408 x 298 x 264 mm plastic crates (the measured box of the CC0 crate on Poly Haven, whose lattice sides and printed storage name are not used) built by script with a 28 mm rim, a 24 mm base rail, ribs and slots, a 66 mm name band carrying only the invented COPPER ROW DAIRY, stacking lugs 9 mm high and a pitch of 264, red, with six empty glass pint bottles in the top crate because the grocer and the tea room took a daily delivery (a Judgement: no float is drawn); the stack stands against the grocer's window at east x 37.30, 0.14 m clear of its shop door (the first version stood it across the door at x 38.0; the scene's wooden yard crates stay); no 1975 to 1995 crate photograph was reached and the one photograph (2021, oblique) gives form only, so the slots, rim and band are judged.**

Cloud week 42, unit 13, family 4. Written 13 October 2026; the fixes the review asked for are applied, not re-reviewed. `SELF-CHECK milk-crates: 91 checks, 91 passed, 0 failed; negative controls 0 of 0 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/milk-crates/`: p1 (S2 cropped, the dairy's name and labels masked); no overlay: the photograph is oblique and no ratio could be fitted.
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | no car, skip or pallet; a float is not drawn, only the crates it leaves |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | a CC0 crate exists (S1) and was checked first; its mesh and texture are rejected for stated reasons (W1), its measured box is kept; the rest is own work by script |
| content rule (canon D18) | what the rule forbids is out of image and text | milk, not drink: a dairy's crate and empty milk bottles only; the data scan finds none of what the rule forbids |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 is CC0 with no NoAI tag; S2 and S3 are CC BY-SA 2.0 photographs used only to look at; nothing is traced |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | red plastic, grime and scuffs; one saturated patch of colour in a grey doorway |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the crates read near black |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://polyhaven.com/a/plastic_crate_01 (api.polyhaven.com/info/plastic_crate_01 and /files/plastic_crate_01) | 2026-10-13 | PierreB3D (Poly Haven) | CC0 1.0 | model published 2026-06 | a deep red plastic crate with lattice sides, cutout handles and a worn storage print, 298 x 408 x 264 mm, 18,320 triangles, tagged milk crate; its 1k base colour carries the lettering GALLER STORAGE (looked at at 100 percent on 13 October) | YES | its mesh and texture: the lattice sides and the print disagree with the photographs and the rules; ONLY its box (298 x 408 x 264) is used as the measured size | a modern storage crate; the 12-pint milk crate's box is the same |
| S2 | https://www.geograph.org.uk/photo/6898849 | 2026-10-13 | Jaggery | CC BY-SA 2.0 (read on the page) | 2021-07-14 | two blue crates stacked on a pavement against a shutter, seen from about 45 degrees above: a deep rim band, a name band on the front wall, slots between ribs, a stack with the upper crate's base on the lower rim; four plastic bottles in the top crate (a 2021 pack, not glass pints) | YES | any number (oblique; the view's foreshortening makes every vertical ratio unusable); the dairy's name (masked); the plastic bottles | 2021; the crate form is that of 1990 (the design has not changed) but the bottles are modern |
| S3 | https://www.geograph.org.uk/photo/4802548 | 2026-10-13 | Robert Lamb | CC BY-SA 2.0 (read on the page) | 2016-01-23 | stacks of red, blue, green and orange crates used as benches: shows the colour range and the stacking in courses | no | everything (looked at only: two people in the frame; a stall's lettering) | 2016 |
| S4 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | plastic_crate_01 (298 x 408 x 264), plastic_crate_02 (506 x 406 x 254), plastic_crate_03 (481 x 265 x 266), wooden_crate_01 and 02, cardboard_box_01; no pint bottle | YES | any other model | n/a |
| S5 | https://api.geograph.org.uk/syndicator.php (terms milk crates, crates, milk float, milk bottles, each with takenyear 1975 to 1996) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | milk floats of 1975 to 1995 in village and town photographs, none showing crates closely; the term 'crates' alone returned nothing | no | measuring | n/a |
| S6 | production/specs/vignette-scene.json (this repository) | 2026-10-13 | this project | own work | n/a | the yard mouth holds two wooden crates (wooden_crate_01 twice, x 22.4 and 23.1 west) and a barrel; no milk crates, no pallet, no skip | YES | any shape | n/a |

What was searched: Poly Haven's model list (521 models, 13 October; the info and files of plastic_crate_01, 02, 03 and wooden_crate_01, 02 read); Geograph's feed for `milk crates`, `crates`, `milk float`, `milk bottles` with each year 1975 to 1996. Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| Poly Haven plastic_crate_01 (CC0) | a red plastic crate 298 x 408 x 264 with lattice sides, handle cutouts and a printed storage name | BOX KEPT, mesh and texture REJECTED | W1: the lattice and the lettering (its base colour reads GALLER STORAGE at 100 percent); the builder may still use it as a size reference |
| Poly Haven plastic_crate_02 and 03 | 506 x 406 x 254 and 481 x 265 x 266 crates | NOT USED | other sizes |
| vignette-scene.json: wooden_crate_01 twice at the yard mouth (west, x 22.4 and 23.1) | wooden crates for the yard | KEPT, unchanged | a different family; these are the grocer's plastic crates |
| production/research/asset-plan 3 and period-vehicles-and-props | no milk crate line (the 29 September research note put two kinds of crate under one exclusion) | READ | milk is not drink: the 29 September exclusion of milk crates is lifted by this target (a DECISIONS entry); the crates carry milk bottles only |
| git branches (git log --all for milk, crate) | none | none to reuse |  |

## The target

Axes: x along the crate's length (the dairy band faces -y), y across, z up from the ground at the bottom crate's floor. Boxes and cylinders; the self-check measures every number back off the parts.

### Assembly in words

- **One crate (408 x 298 x 264)**: a 10 mm floor plate with 36 drain slots (a mask), a base rail 24 high and 4 thick all round, a rim 28 high and 6 thick all round, four corner posts 16 x 16, ribs 14 wide (three inner on each long wall, one centre rib on each end wall) between rail and rim, a solid name band 66 high on each long wall at z 118 to 184, and four stacking lugs 14 x 14 x 9 on the rim's corners. The openings between the ribs are open (slots about 88 wide); the end walls' two openings are the hand holds.
- **The stack**: three crates at z 0, 264, 528: each base rail rests on the rim below and the lugs enter the next floor's recesses (the floor plate, 10 thick, has a 14 x 14 x 9 recess under each lug: Judgement). Overall 408 x 298 x 801.
- **The empties**: six glass pint bottles standing on the top crate's floor, a body 64 across and 128 high, a neck 28 across and 56 high, in the cells of a 4 x 3 grid at 100 mm, no caps, a faint lip ring (not modelled).
- **Edges and fixings**: all outer edges r 2, the rim's top edge r 3, vertical post edges r 4; no fixings (moulded in one piece).

### Parts, variant MC1: MC1: one 12-pint crate, empty (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| c1_floor | box | crate_plastic | -200 to 200 | -145 to 145 | 0 to 10 | edges r 2 | floor plate, 10 thick, with 36 drain slots 20 x 8 (a mask in the build; see the text) |
| c1_rail_f | box | crate_plastic | -204 to 204 | -149 to -145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_b | box | crate_plastic | -204 to 204 | 145 to 149 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_l | box | crate_plastic | -204 to -200 | -145 to 145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_r | box | crate_plastic | 200 to 204 | -145 to 145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rim_f | box | crate_plastic | -204 to 204 | -149 to -143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_b | box | crate_plastic | -204 to 204 | 143 to 149 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_l | box | crate_plastic | -204 to -198 | -143 to 143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_r | box | crate_plastic | 198 to 204 | -143 to 143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_post_fl | box | crate_plastic | -204 to -188 | -149 to -133 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_fr | box | crate_plastic | 188 to 204 | -149 to -133 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_bl | box | crate_plastic | -204 to -188 | 133 to 149 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_br | box | crate_plastic | 188 to 204 | 133 to 149 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_rib_f0 | box | crate_plastic | -109 to -95 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b0 | box | crate_plastic | -109 to -95 | 145 to 149 | 24 to 236 |  |  |
| c1_rib_f1 | box | crate_plastic | -7 to 7 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b1 | box | crate_plastic | -7 to 7 | 145 to 149 | 24 to 236 |  |  |
| c1_rib_f2 | box | crate_plastic | 95 to 109 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b2 | box | crate_plastic | 95 to 109 | 145 to 149 | 24 to 236 |  |  |
| c1_band_f | box | crate_plastic | -188 to 188 | -149 to -145 | 118 to 184 |  | solid band 66 high that carries the dairy's name |
| c1_band_b | box | crate_plastic | -188 to 188 | 145 to 149 | 118 to 184 |  |  |
| c1_rib_l | box | crate_plastic | -204 to -200 | -7 to 7 | 24 to 236 |  | centre rib of each end wall; the two openings beside it are the hand holds |
| c1_rib_r | box | crate_plastic | 200 to 204 | -7 to 7 | 24 to 236 |  |  |
| c1_lug_fl | box | crate_plastic | -198 to -184 | -143 to -129 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_fr | box | crate_plastic | 184 to 198 | -143 to -129 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_bl | box | crate_plastic | -198 to -184 | 129 to 143 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_br | box | crate_plastic | 184 to 198 | 129 to 143 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |

### Parts, variant MC3: MC3: a stack of three crates, six empty pint bottles in the top one (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| c1_floor | box | crate_plastic | -200 to 200 | -145 to 145 | 0 to 10 | edges r 2 | floor plate, 10 thick, with 36 drain slots 20 x 8 (a mask in the build; see the text) |
| c1_rail_f | box | crate_plastic | -204 to 204 | -149 to -145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_b | box | crate_plastic | -204 to 204 | 145 to 149 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_l | box | crate_plastic | -204 to -200 | -145 to 145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rail_r | box | crate_plastic | 200 to 204 | -145 to 145 | 0 to 24 | lower edge r 2 | base rail 24 high, 4 thick |
| c1_rim_f | box | crate_plastic | -204 to 204 | -149 to -143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_b | box | crate_plastic | -204 to 204 | 143 to 149 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_l | box | crate_plastic | -204 to -198 | -143 to 143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_rim_r | box | crate_plastic | 198 to 204 | -143 to 143 | 236 to 264 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c1_post_fl | box | crate_plastic | -204 to -188 | -149 to -133 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_fr | box | crate_plastic | 188 to 204 | -149 to -133 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_bl | box | crate_plastic | -204 to -188 | 133 to 149 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_post_br | box | crate_plastic | 188 to 204 | 133 to 149 | 24 to 236 | vertical edge r 4 | corner post 16 x 16 |
| c1_rib_f0 | box | crate_plastic | -109 to -95 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b0 | box | crate_plastic | -109 to -95 | 145 to 149 | 24 to 236 |  |  |
| c1_rib_f1 | box | crate_plastic | -7 to 7 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b1 | box | crate_plastic | -7 to 7 | 145 to 149 | 24 to 236 |  |  |
| c1_rib_f2 | box | crate_plastic | 95 to 109 | -149 to -145 | 24 to 236 |  | rib 14 wide between the slots |
| c1_rib_b2 | box | crate_plastic | 95 to 109 | 145 to 149 | 24 to 236 |  |  |
| c1_band_f | box | crate_plastic | -188 to 188 | -149 to -145 | 118 to 184 |  | solid band 66 high that carries the dairy's name |
| c1_band_b | box | crate_plastic | -188 to 188 | 145 to 149 | 118 to 184 |  |  |
| c1_rib_l | box | crate_plastic | -204 to -200 | -7 to 7 | 24 to 236 |  | centre rib of each end wall; the two openings beside it are the hand holds |
| c1_rib_r | box | crate_plastic | 200 to 204 | -7 to 7 | 24 to 236 |  |  |
| c1_lug_fl | box | crate_plastic | -198 to -184 | -143 to -129 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_fr | box | crate_plastic | 184 to 198 | -143 to -129 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_bl | box | crate_plastic | -198 to -184 | 129 to 143 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c1_lug_br | box | crate_plastic | 184 to 198 | 129 to 143 | 264 to 273 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c2_floor | box | crate_plastic | -200 to 200 | -145 to 145 | 264 to 274 | edges r 2 | floor plate, 10 thick, with 36 drain slots 20 x 8 (a mask in the build; see the text) |
| c2_rail_f | box | crate_plastic | -204 to 204 | -149 to -145 | 264 to 288 | lower edge r 2 | base rail 24 high, 4 thick |
| c2_rail_b | box | crate_plastic | -204 to 204 | 145 to 149 | 264 to 288 | lower edge r 2 | base rail 24 high, 4 thick |
| c2_rail_l | box | crate_plastic | -204 to -200 | -145 to 145 | 264 to 288 | lower edge r 2 | base rail 24 high, 4 thick |
| c2_rail_r | box | crate_plastic | 200 to 204 | -145 to 145 | 264 to 288 | lower edge r 2 | base rail 24 high, 4 thick |
| c2_rim_f | box | crate_plastic | -204 to 204 | -149 to -143 | 500 to 528 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c2_rim_b | box | crate_plastic | -204 to 204 | 143 to 149 | 500 to 528 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c2_rim_l | box | crate_plastic | -204 to -198 | -143 to 143 | 500 to 528 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c2_rim_r | box | crate_plastic | 198 to 204 | -143 to 143 | 500 to 528 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c2_post_fl | box | crate_plastic | -204 to -188 | -149 to -133 | 288 to 500 | vertical edge r 4 | corner post 16 x 16 |
| c2_post_fr | box | crate_plastic | 188 to 204 | -149 to -133 | 288 to 500 | vertical edge r 4 | corner post 16 x 16 |
| c2_post_bl | box | crate_plastic | -204 to -188 | 133 to 149 | 288 to 500 | vertical edge r 4 | corner post 16 x 16 |
| c2_post_br | box | crate_plastic | 188 to 204 | 133 to 149 | 288 to 500 | vertical edge r 4 | corner post 16 x 16 |
| c2_rib_f0 | box | crate_plastic | -109 to -95 | -149 to -145 | 288 to 500 |  | rib 14 wide between the slots |
| c2_rib_b0 | box | crate_plastic | -109 to -95 | 145 to 149 | 288 to 500 |  |  |
| c2_rib_f1 | box | crate_plastic | -7 to 7 | -149 to -145 | 288 to 500 |  | rib 14 wide between the slots |
| c2_rib_b1 | box | crate_plastic | -7 to 7 | 145 to 149 | 288 to 500 |  |  |
| c2_rib_f2 | box | crate_plastic | 95 to 109 | -149 to -145 | 288 to 500 |  | rib 14 wide between the slots |
| c2_rib_b2 | box | crate_plastic | 95 to 109 | 145 to 149 | 288 to 500 |  |  |
| c2_band_f | box | crate_plastic | -188 to 188 | -149 to -145 | 382 to 448 |  | solid band 66 high that carries the dairy's name |
| c2_band_b | box | crate_plastic | -188 to 188 | 145 to 149 | 382 to 448 |  |  |
| c2_rib_l | box | crate_plastic | -204 to -200 | -7 to 7 | 288 to 500 |  | centre rib of each end wall; the two openings beside it are the hand holds |
| c2_rib_r | box | crate_plastic | 200 to 204 | -7 to 7 | 288 to 500 |  |  |
| c2_lug_fl | box | crate_plastic | -198 to -184 | -143 to -129 | 528 to 537 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c2_lug_fr | box | crate_plastic | 184 to 198 | -143 to -129 | 528 to 537 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c2_lug_bl | box | crate_plastic | -198 to -184 | 129 to 143 | 528 to 537 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c2_lug_br | box | crate_plastic | 184 to 198 | 129 to 143 | 528 to 537 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c3_floor | box | crate_plastic | -200 to 200 | -145 to 145 | 528 to 538 | edges r 2 | floor plate, 10 thick, with 36 drain slots 20 x 8 (a mask in the build; see the text) |
| c3_rail_f | box | crate_plastic | -204 to 204 | -149 to -145 | 528 to 552 | lower edge r 2 | base rail 24 high, 4 thick |
| c3_rail_b | box | crate_plastic | -204 to 204 | 145 to 149 | 528 to 552 | lower edge r 2 | base rail 24 high, 4 thick |
| c3_rail_l | box | crate_plastic | -204 to -200 | -145 to 145 | 528 to 552 | lower edge r 2 | base rail 24 high, 4 thick |
| c3_rail_r | box | crate_plastic | 200 to 204 | -145 to 145 | 528 to 552 | lower edge r 2 | base rail 24 high, 4 thick |
| c3_rim_f | box | crate_plastic | -204 to 204 | -149 to -143 | 764 to 792 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c3_rim_b | box | crate_plastic | -204 to 204 | 143 to 149 | 764 to 792 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c3_rim_l | box | crate_plastic | -204 to -198 | -143 to 143 | 764 to 792 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c3_rim_r | box | crate_plastic | 198 to 204 | -143 to 143 | 764 to 792 | top edge r 3 | rim 28 high, 6 thick, a stiffening band |
| c3_post_fl | box | crate_plastic | -204 to -188 | -149 to -133 | 552 to 764 | vertical edge r 4 | corner post 16 x 16 |
| c3_post_fr | box | crate_plastic | 188 to 204 | -149 to -133 | 552 to 764 | vertical edge r 4 | corner post 16 x 16 |
| c3_post_bl | box | crate_plastic | -204 to -188 | 133 to 149 | 552 to 764 | vertical edge r 4 | corner post 16 x 16 |
| c3_post_br | box | crate_plastic | 188 to 204 | 133 to 149 | 552 to 764 | vertical edge r 4 | corner post 16 x 16 |
| c3_rib_f0 | box | crate_plastic | -109 to -95 | -149 to -145 | 552 to 764 |  | rib 14 wide between the slots |
| c3_rib_b0 | box | crate_plastic | -109 to -95 | 145 to 149 | 552 to 764 |  |  |
| c3_rib_f1 | box | crate_plastic | -7 to 7 | -149 to -145 | 552 to 764 |  | rib 14 wide between the slots |
| c3_rib_b1 | box | crate_plastic | -7 to 7 | 145 to 149 | 552 to 764 |  |  |
| c3_rib_f2 | box | crate_plastic | 95 to 109 | -149 to -145 | 552 to 764 |  | rib 14 wide between the slots |
| c3_rib_b2 | box | crate_plastic | 95 to 109 | 145 to 149 | 552 to 764 |  |  |
| c3_band_f | box | crate_plastic | -188 to 188 | -149 to -145 | 646 to 712 |  | solid band 66 high that carries the dairy's name |
| c3_band_b | box | crate_plastic | -188 to 188 | 145 to 149 | 646 to 712 |  |  |
| c3_rib_l | box | crate_plastic | -204 to -200 | -7 to 7 | 552 to 764 |  | centre rib of each end wall; the two openings beside it are the hand holds |
| c3_rib_r | box | crate_plastic | 200 to 204 | -7 to 7 | 552 to 764 |  |  |
| c3_lug_fl | box | crate_plastic | -198 to -184 | -143 to -129 | 792 to 801 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c3_lug_fr | box | crate_plastic | 184 to 198 | -143 to -129 | 792 to 801 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c3_lug_bl | box | crate_plastic | -198 to -184 | 129 to 143 | 792 to 801 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c3_lug_br | box | crate_plastic | 184 to 198 | 129 to 143 | 792 to 801 |  | stacking lug 14 x 14 x 9 on the rim; it enters the recess in the next crate's base rail |
| c3_bottle1 | cyl | glass | -182 to -118 | -132 to -68 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck1 | cyl | glass | -164 to -136 | -114 to -86 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |
| c3_bottle2 | cyl | glass | -82 to -18 | -32 to 32 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck2 | cyl | glass | -64 to -36 | -14 to 14 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |
| c3_bottle3 | cyl | glass | 18 to 82 | 68 to 132 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck3 | cyl | glass | 36 to 64 | 86 to 114 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |
| c3_bottle4 | cyl | glass | 118 to 182 | -132 to -68 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck4 | cyl | glass | 136 to 164 | -114 to -86 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |
| c3_bottle5 | cyl | glass | -182 to -118 | 68 to 132 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck5 | cyl | glass | -164 to -136 | 86 to 114 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |
| c3_bottle6 | cyl | glass | -82 to -18 | -132 to -68 | 538 to 666 |  | empty pint bottle body (glass, no cap, foil gone) |
| c3_neck6 | cyl | glass | -64 to -36 | -114 to -86 | 666 to 722 |  | neck 28 across with a lip ring (transparent) |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | crate outer length | 408 mm | Read | Poly Haven plastic_crate_01 (CC0, tagged beverage crate and milk crate): dimensions [298.0, 408.0, 264.2] read from api.polyhaven.com/info on 13 October 2026; the self-check's --live re-reads them | +-1 |
| N2 | crate outer width | 298 mm | Read | same record: 298.0 | +-1 |
| N3 | crate height to the rim (lugs excluded) | 264 mm | Read | same record: 264.2; 264 kept | +-1 |
| N4 | stack pitch: one crate's base on the next one's rim | 264 mm | Derived | the base rail's underside rests on the rim top; the lugs (9 high) enter the next floor's recesses; so the pitch is the crate height | +-1 |
| N5 | stack height of three crates with lugs | 801 mm | Derived | 3 x 264 + 9 | +-1.5 |
| N6 | bottle body diameter | 64 mm | Judgement | a pint milk bottle's body is about 64 mm across (twelve fit a 4 x 3 grid of 100 mm cells with room); not measured on a photograph; error 6 | +-6 |
| N7 | bottle height (body and neck) | 184 mm | Judgement | about 184 mm for a pint (128 body + 56 neck); error 15 | +-15 |
| N8 | name band height | 66 mm | Judgement | P1's name panel on the front wall reads about 60 to 70 mm (oblique view); error 12 | +-12 |
| N9 | rim height | 28 mm | Judgement | P1's rim band reads 13 px of 105 for 528 mm = 65 mm including the rim's top face seen from 45 degrees above; the front face alone is taken as 28 (error 12) | +-12 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| crate_plastic | moulded crate plastic, faded | 168, 40, 36 | 0.50 (semi-gloss) | not metal | the sample crate is red: a JUDGEMENT (a dairy chose one colour for all its crates and dairies used many: red, blue, yellow, green, orange; the red was first seen on the rejected Poly Haven crate and S2's photograph shows blue crates, which stay the first variant); UV-faded to a lighter, chalky red on the top rim; grime in every slot; NO printed brand (the CC0 texture's 'GALLER STORAGE' print is not used) |
| glass | clear glass, milk-filmed | 210, 218, 214 | 0.05 (smooth) | not metal | a faint milky film on the inside, a dull ring where the cap sat; embossed dairy name on the shoulder |

### Wear

- the plastic is scuffed white along the rim's top edge and the lugs, and along the base rail's lower edge where crates are dragged; the faded top rim is chalkier than the body
- dirt in every slot and in the floor's drain slots (a darker mask), a milky film on the floor under the bottles, a dried ring where bottles stood
- the bottles: cap-less, a dull ring on each lip, embossed shoulder, a smear of old milk inside the lowest 10 mm (a mask on the glass)
- one crate in the stack is a different colour (blue) from the other two: crates were swapped between dairies' rounds only within a dairy, so the stack is one colour in the sample and a blue one is a variant
- NOT shown: any lettering but the dairy's name, a person, any other drink, a sticker

### Variants the street needs

- MC3 (the sample): three crates, six empty pint bottles in the top one, one colour (red).
- MC1: a single crate, empty (a spare for the yard or a doorstep).
- colours: red (the sample, a Judgement), blue (S2's photograph), yellow, green, orange (a dairy's crates are all one colour); fade and grime as wear.
- a crate on its side or two stacked with bottles in the lower one (a seed, not a mesh): the builder may place the MC1 mesh as it likes.

### Where it stands on Quay Street

**Slot:** east side, bay 5 (the grocer, x 33 to 39): one stack of three crates against the window's stallriser, centre x 37.30 (the stack's x 37.096 to 37.504, 0.14 m from the door jamb at x 37.644; the grocer has NO side door: its shop door is the 1006 mm at the high-x end, x 37.644 to 38.650, in a 600 mm recessed lobby), back 0.05 m clear of the stallriser line (z 4.975), long side facing the road; a second, single crate (MC1) is the street's spare, not placed

- crates stand at the shop that sells milk: the grocer (bay 5) takes a daily delivery; the stack stands 50 mm clear of the stallriser line (z 4.975) so it never leans on the glass, its 298 mm width taking 4.627 to 4.925 of the footway and leaving 1.50 m clear from the kerb's back edge (3.125)
- THE FIRST VERSION STOOD IT ACROSS THE SHOP DOOR (x 38.0, 'the grocer's side-door end'): the grocer has no side door (terrace-front.py BAY_WITHOUT_SIDE_DOOR = 5); its shop door is the outer 1006 mm at the high-x end, x 37.644 to 38.650 (centre 38.147), in a 600 mm recessed lobby (shopfronts target, shops[grocer]), and the stack (x 37.796 to 38.204) stood in the lobby's mouth; the placement rows tested only that it lay inside x 33 to 39 and the strip to the kerb. At x 37.30 it stands against the window's stallriser (x 33.35 to 37.644), 0.14 m from the door's jamb; the shared placement rows now test it against the shopfronts target's door zones and every piece of the scene
- it stands at the shop's door end, clear of the door, beside the litter and bin traffic of the east parade's end, 6.4 m from the chandler's shop door (x 43.70 to 44.71; the chandler's doors are at x 43.70 to 45.65)
- the scene's yard-mouth crates are wooden and stay (one family's yard stuff); these are the grocer's

### Lettering and text

- Dairy: COPPER ROW DAIRY (a fictional placeholder until the town mints one): a SEPARATE swappable layer (a normal and colour decal, not mesh), blank in any picture for his page: capitals 18 mm tall, centred on each long wall's band; the second line on the band's lower half 6 mm tall: PROPERTY OF THE DAIRY, then the warning line.
- Bottles: the same name on the shoulder in the same kind of layer, 6 mm capitals.

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the crate model | S1 (CC0): a lattice-sided storage crate with a printed brand-like name; the asset plan wants CC0 first | S2: slot-sided crates with a solid name band on the front wall and a deep rim | built by script to S1's box with slot sides and a name band; S1's mesh and texture are not used (its base colour carries the lettering GALLER STORAGE) |
| W2 | the bottles | the photograph's four-pint plastic bottles | S2 shows 2021 plastic bottles; 1990's were glass pints | glass pint bottles, empty, no cap, an embossed fictional name |
| W3 | the stacking | none | S2 shows the upper crate's base resting on the lower crate's rim with the lugs inside | pitch = crate height 264, lugs 9 high entering the next floor |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: crate outer length | measure it on the built mesh in millimetres (bbox) | 408.0 mm | +-1.0 mm |
| N2: crate outer width | measure it on the built mesh in millimetres (bbox) | 298.0 mm | +-1.0 mm |
| N3: crate height to the rim (lugs excluded) | measure it on the built mesh in millimetres (bbox) | 264.0 mm | +-1.0 mm |
| N4: stack pitch: one crate's base on the next one's rim | measure it on the built mesh in millimetres (centre_dx) | 264.0 mm | +-1.0 mm |
| N5: stack height of three crates with lugs | measure it on the built mesh in millimetres (bbox) | 801.0 mm | +-1.5 mm |
| N6: bottle body diameter | measure it on the built mesh in millimetres (extent) | 64.0 mm | +-6.0 mm |
| N7: bottle height (body and neck) | measure it on the built mesh in millimetres (span) | 184.0 mm | +-15.0 mm |
| N8: name band height | measure it on the built mesh in millimetres (extent) | 66.0 mm | +-12.0 mm |
| N9: rim height | measure it on the built mesh in millimetres (extent) | 28.0 mm | +-12.0 mm |
| C1: the crate's box | outer box of one crate without its lugs | 408 x 298 x 264 | +-1 mm |
| C2: three crates stacked, six bottles | count crates and bottles | 3 and 6 | exact |
| C3: the walls closed where they should be | rays at the front band, the rim and the base rail at 0, 30 and 45 degrees | 0 get through | exact |
| C4: no part floats, every join meets | the contact graph | all parts reach the ground | 0 floating |
| C5: the text | the lettering layer (a swappable decal, not mesh) | the placeholder dairy only, blank in pictures for his page | exact |
| C7: the stack clear of the shop door | the stack's x range against the grocer's shop door zone | x 37.096 to 37.504, 0.14 m from the jamb at 37.644 | +-0.05 m |
| C6: the CC0 model's lettering is not in the base colour | the crate colour map at 100 percent | no GALLER or STORAGE | exact |

### For the builder

- build the crate by script in one mesh: floor plate with 36 drain slots cut (a mask or real holes), four walls as ribs and slots (the gaps between the ribs are open), rim, base rail with four recesses under the corners for the lugs, name band with the raised text
- stack by instancing the crate at z 0, 264, 528 (no scale), rotate each crate by a seed of 0 to 2 degrees about z (not more: they interlock)
- bottles: glass, a body 128 and neck 56 with a lip ring; six in the top crate in a 4 x 3 grid of 100 mm cells (six of the twelve cells)
- texture: our own colour map for the crate; the CC0 model's texture is NOT used (its lettering); the dairy's name is a separate swappable decal layer (normal and colour), blank in any picture for his page
- stand the stack at x 37.30, z 4.776 (its centre), 0.14 m clear of the grocer's door jamb; never in front of the lobby (x 37.644 to 38.650)

## Owed to Jafar's page (one line each, with a recommendation)

None.

## Handovers (for the town or the scene's owner, not for his page)

- H1: For the town: mint the dairy that supplies the grocer and the tea room (its name for the crates' bands and the bottles' shoulders; now the placeholder 'Copper Row Dairy' in a swappable lettering layer, never shown on Jafar's page), within canon's naming rules.

## What the target could not settle

- no photograph of a 1975 to 1995 crate was reached; P1 is a 2021 oblique view, so the slot layout, the rim depth (28 mm, error 12) and the name band (66 mm, error 12) are judged; the box is Poly Haven's measured 298 x 408 x 264
- whether a 1990 12-pint crate is 264 high (the CC0 record, a storage crate tagged milk crate) or nearer 200: the bottles then stand fully inside (their tops 70 mm below the rim); one number for the builder to confirm against a period crate if one is ever reached
- the stack's lettering layer is not yet textured (a decal on the band and the shoulders): the dairy is a placeholder (handover H1)
- the crate's slot sizes and the floor's drain slots (36 slots 20 x 8 are a Judgement written as a texture mask, not geometry)
- whether a milk float served Quay Street: stated as a Judgement; the empties are the only sign of it
- the pint bottle's exact shape (body 64 across, neck 28, 184 high: Judgement)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the crate's box against the CC0 record read live, the stack pitch, the bottles inside the top crate, the dairy's name as a placeholder in its own layer, the stack against the street's pieces and the shopfronts' door zones (the grocer's door), the clear strip). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
