# Quay Street's bicycle against a wall: the exact target

**The bicycle is an adult's gent's roadster (26 x 1 3/8 wheels 660 mm over the tyre, a 1097 mm wheelbase, a level top tube on a 72 degree seat tube and a 68 degree head tube, swept-back bars 790 over the grips, a sprung saddle at 1035, mudguards, a plain bell, 170 mm cranks) in the enamel-chipped, dull-chromed state of a street bicycle, no badge or lettering, shown leaning 12 degrees on the blank west wall at x 15.0 with its right grip end against the brick; no period photograph was measurable (the two street photographs are oblique and low in contrast), so every number is Judgement within stated ranges and the target is checked for internal consistency, the tube angles and the ranges, not against pixels; an adult's bicycle only.**

Cloud week 42, unit 13, family 7. Written 13 October 2026, not yet reviewed. `SELF-CHECK bicycle: 71 checks, 71 passed, 0 failed; negative controls 23 of 23 caught (--live --previews)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/bicycle/`: p1 (S1 cropped; no overlay: the photograph is too oblique and low in contrast to lay a drawing on).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | not a car, skip or pallet; plain street dressing |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no CC0 bicycle exists (S4); so own work by script |
| content rule (canon D18) | what the rule forbids is out of image and text | an adult's bicycle only; the data scan finds none of what the rule forbids |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | dull chrome, rust spots and a wet street: grime is the strategy |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; chrome glints, the frame vanishes |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/2932507 | 2026-10-13 | Jeremy Bolwell | CC BY-SA 2.0 (read on the page) | 2012-05-06 | a rusted gent's roadster leaning on a stone wall in a ruined building: a diamond frame with a level top tube, two big spoked wheels with mudguards, swept-back bars, a sprung saddle, a rear carrier; the rear wheel nearer the camera so the perspective is strong | YES | any number (the camera is oblique and close, the picture low in contrast); the rust is a wear state, not the sample's | 2012; a roadster of the 1950s to 1970s kind, the type an old man or a dock worker still rode in 1990 |
| S2 | https://www.geograph.org.uk/photo/4155634 | 2026-10-13 | DS Pugh | CC BY-SA 2.0 (read on the page) | 2014-09-01 | a modern road bicycle leaning with its front tyre against a dry-stone wall: shows how a bicycle leans on a wall (front wheel and bar end against the stone, the rear wheel on the ground at a lean of about 10 to 15 degrees); a pannier and a bottle (brands masked) | YES | the bicycle's form (modern: 700c wheels, derailleur, drop frame) and any number | 2014; used only for the leaning pose |
| S3 | https://www.geograph.org.uk/photo/4811433 | 2026-10-13 | Bill Nicholls | CC BY-SA 2.0 (read on the page) | 2014-09-21 | a black gent's roadster on a display stand in a museum room: the diamond frame in a clean side view, swept bars, a plain saddle, 28 inch wheels | no | everything (an interior display of an older machine, not a street photograph: looked at for the frame's layout only) | 2014 interior of a heritage machine |
| S4 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | no bicycle | no | everything: no CC0 bicycle exists, so it is made by script | n/a |
| S5 | https://api.geograph.org.uk/syndicator.php (terms bicycle, bicycles, bicycle wall, bike leaning; takenyear 1975 to 1996 and without a year) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | 1975 to 1996: a 1991 timbered house with a bicycle at its door, a 1992 station platform with cyclists, a 1993 night view of parked bicycles, a 1994 trail rider, a 1996 sporting photograph; none of a bicycle against a wall close up | no | measuring | n/a |
| S6 | canon.md, the content rule (D18) | 2026-10-13 | this project | own work | n/a | the content rule keeps young people out of every image and every prop: the bicycle is an adult's, the frame 560 mm, no small wheels, no stabilisers, no basket | YES | shape | n/a |

What was searched: Poly Haven's model list (no bicycle); Geograph's feed for `bicycle`, `bicycles`, `bicycle wall`, `bike leaning` with each year 1975 to 1996 and without a year. Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| Poly Haven models | no bicycle | NOT USED | S4 |
| vignette-scene.json, the asset plan, the research notes | no bicycle anywhere | NONE to reuse | this is a new prop |
| git branches (git log --all for bicycle, bike) | none | none to reuse |  |

## The target

Axes: x forward (the front wheel at +x), y to the rider's right, z up from the ground at the tyres' contact. Cylinders for tubes, spokes and the hub, boxes for the tyre segments, the saddle, the cranks and the pedals; BI2 adds a transform and a wall.

### Assembly in words

- **Wheels**: 26 x 1 3/8, 660 over the tyre (a ring of 16 segments 38 x 38), a hub 44 across and 100 long, spokes 2.4 across (8 drawn of 36), mudguards 60 wide and 2 thick 8 mm over the tyre round the top 140 degrees.
- **Frame**: seat tube 28 across, 560 from the bottom bracket centre, 72 degrees; level top tube 28 across, 570 long; down tube 30 across; head tube 36 across and 150 long at 68 degrees; chain stays 16 across and 450 long, seat stays 16 across; the bottom bracket 300 up (30 below the axles).
- **Fork**: two blades 22 across with 45 rake at the foot, a crown 24 x 124 x 24.
- **Cockpit**: a stem 22 across rising 170 along the steering axis, a bar of 22 across, 380 straight between swept-back ends to 580 over the bends and 790 over the 105 mm grips, a bell 52 across.
- **Saddle and post**: a post 22 across to z 985, a saddle 280 x 180 x 50 at 985 to 1035.
- **Drive**: a spindle 24 across, a chainring 180 across, cranks 170, pedals 100 x 105 x 24 (the chain, the chain guard, the carrier and the lamp are textures or not modelled).

### Parts, variant BI1: BI1: an adult's roadster standing upright (a stand-in for a bicycle held up by its rider) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| rw_tyre1 | box | tyre | 292 to 330 | -19 to 19 | 268 to 392 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre2 | box | tyre | 246 to 329 | -19 to 19 | 385 to 513 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre3 | box | tyre | 163 to 277 | -19 to 19 | 493 to 607 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre4 | box | tyre | 55 to 183 | -19 to 19 | 576 to 659 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre5 | box | tyre | -62 to 62 | -19 to 19 | 622 to 660 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre6 | box | tyre | -183 to -55 | -19 to 19 | 576 to 659 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre7 | box | tyre | -277 to -163 | -19 to 19 | 493 to 607 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre8 | box | tyre | -329 to -246 | -19 to 19 | 385 to 513 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre9 | box | tyre | -330 to -292 | -19 to 19 | 268 to 392 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre10 | box | tyre | -329 to -246 | -19 to 19 | 147 to 275 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre11 | box | tyre | -277 to -163 | -19 to 19 | 53 to 167 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre12 | box | tyre | -183 to -55 | -19 to 19 | 1 to 84 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre13 | box | tyre | -62 to 62 | -19 to 19 | -0 to 38 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre14 | box | tyre | 55 to 183 | -19 to 19 | 1 to 84 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre15 | box | tyre | 163 to 277 | -19 to 19 | 53 to 167 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre16 | box | tyre | 246 to 329 | -19 to 19 | 147 to 275 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_hub | cyl | steel | -22 to 22 | -50 to 50 | 308 to 352 |  | hub 44 across, 100 long |
| rw_spoke1 | cyl | steel | 22 to 268 | -1 to 1 | 338 to 442 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke2 | cyl | steel | 8 to 112 | -1 to 1 | 352 to 598 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke3 | cyl | steel | -112 to -8 | -1 to 1 | 352 to 598 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke4 | cyl | steel | -268 to -22 | -1 to 1 | 338 to 442 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke5 | cyl | steel | -268 to -22 | -1 to 1 | 218 to 322 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke6 | cyl | steel | -112 to -8 | -1 to 1 | 62 to 308 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke7 | cyl | steel | 8 to 112 | -1 to 1 | 62 to 308 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke8 | cyl | steel | 22 to 268 | -1 to 1 | 218 to 322 |  | spoke 2.4 across (8 drawn of 36) |
| fw_tyre1 | box | tyre | 1389 to 1427 | -19 to 19 | 268 to 392 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre2 | box | tyre | 1343 to 1425 | -19 to 19 | 385 to 513 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre3 | box | tyre | 1260 to 1374 | -19 to 19 | 493 to 607 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre4 | box | tyre | 1151 to 1280 | -19 to 19 | 576 to 659 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre5 | box | tyre | 1035 to 1159 | -19 to 19 | 622 to 660 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre6 | box | tyre | 913 to 1042 | -19 to 19 | 576 to 659 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre7 | box | tyre | 820 to 934 | -19 to 19 | 493 to 607 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre8 | box | tyre | 768 to 851 | -19 to 19 | 385 to 513 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre9 | box | tyre | 767 to 805 | -19 to 19 | 268 to 392 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre10 | box | tyre | 768 to 851 | -19 to 19 | 147 to 275 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre11 | box | tyre | 820 to 934 | -19 to 19 | 53 to 167 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre12 | box | tyre | 913 to 1042 | -19 to 19 | 1 to 84 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre13 | box | tyre | 1035 to 1159 | -19 to 19 | -0 to 38 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre14 | box | tyre | 1151 to 1280 | -19 to 19 | 1 to 84 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre15 | box | tyre | 1260 to 1374 | -19 to 19 | 53 to 167 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre16 | box | tyre | 1343 to 1425 | -19 to 19 | 147 to 275 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_hub | cyl | steel | 1075 to 1119 | -50 to 50 | 308 to 352 |  | hub 44 across, 100 long |
| fw_spoke1 | cyl | steel | 1119 to 1365 | -1 to 1 | 338 to 442 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke2 | cyl | steel | 1105 to 1209 | -1 to 1 | 352 to 598 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke3 | cyl | steel | 985 to 1089 | -1 to 1 | 352 to 598 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke4 | cyl | steel | 828 to 1075 | -1 to 1 | 338 to 442 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke5 | cyl | steel | 828 to 1075 | -1 to 1 | 218 to 322 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke6 | cyl | steel | 985 to 1089 | -1 to 1 | 62 to 308 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke7 | cyl | steel | 1105 to 1209 | -1 to 1 | 62 to 308 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke8 | cyl | steel | 1119 to 1365 | -1 to 1 | 218 to 322 |  | spoke 2.4 across (8 drawn of 36) |
| rw_guard1 | box | paint_black | 232 to 329 | -30 to 30 | 448 to 590 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard2 | box | paint_black | 83 to 234 | -30 to 30 | 588 to 669 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard3 | box | paint_black | -85 to 85 | -30 to 30 | 667 to 669 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard4 | box | paint_black | -234 to -83 | -30 to 30 | 588 to 669 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard5 | box | paint_black | -329 to -232 | -30 to 30 | 448 to 590 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard1 | box | paint_black | 1336 to 1424 | -30 to 30 | 447 to 581 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard2 | box | paint_black | 1203 to 1339 | -30 to 30 | 578 to 661 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard3 | box | paint_black | 1047 to 1205 | -30 to 30 | 659 to 675 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard4 | box | paint_black | 902 to 1050 | -30 to 30 | 616 to 675 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard5 | box | paint_black | 795 to 904 | -30 to 30 | 502 to 619 |  | mudguard segment, 60 wide, 2 thick |
| seat_tube | cyl | paint_black | 263 to 462 | -14 to 14 | 296 to 837 |  | seat tube 28 across, 560 centre to top, 72 degrees |
| top_tube | cyl | paint_black | 276 to 846 | -14 to 14 | 819 to 854 |  | top tube 28, 570 long, level |
| down_tube | cyl | paint_black | 439 to 912 | -15 to 15 | 289 to 712 |  | down tube 30 |
| head_tube | cyl | paint_black | 829 to 919 | -18 to 18 | 694 to 846 |  | head tube 36 across, 150 long, 68 degrees |
| chain_stay_l | cyl | paint_black | -1 to 450 | -63 to -47 | 292 to 338 |  | chain stay 16, 450 long |
| seat_stay_l | cyl | paint_black | -7 to 283 | -63 to -47 | 326 to 836 |  | seat stay 16 |
| fork_l | cyl | paint_black | 892 to 1107 | -69 to -47 | 325 to 706 |  | fork blade 22, rake 45 at the foot |
| chain_stay_r | cyl | paint_black | -1 to 450 | 47 to 63 | 292 to 338 |  | chain stay 16, 450 long |
| seat_stay_r | cyl | paint_black | -7 to 283 | 47 to 63 | 326 to 836 |  | seat stay 16 |
| fork_r | cyl | paint_black | 892 to 1107 | 47 to 69 | 325 to 706 |  | fork blade 22, rake 45 at the foot |
| seat_bridge | box | paint_black | 268 to 284 | -60 to 60 | 823 to 843 |  | seat-stay bridge |
| fork_crown | box | paint_black | 890 to 914 | -62 to 62 | 671 to 695 |  | fork crown |
| seat_post | cyl | steel | 220 to 287 | -11 to 11 | 829 to 988 |  | seat post 22 |
| saddle | box | saddle_black | 81 to 361 | -90 to 90 | 985 to 1035 | nose r 30, edges r 8 | saddle 280 x 180 x 50, leather-look, springs not modelled |
| stem | cyl | steel | 772 to 856 | -11 to 11 | 835 to 1001 |  | stem 22, 170 above the head tube |
| bar_mid | cyl | steel | 771 to 793 | -190 to 190 | 986 to 1008 |  | handlebar: the straight middle, 22 across, 380 wide |
| bar_sweep_l | cyl | steel | 689 to 791 | -297 to -183 | 986 to 1020 |  | swept-back end, 100 across to 580 over the grips |
| grip_l | cyl | grip_black | 678 to 711 | -396 to -289 | 995 to 1025 |  | grip 28 across, 105 long |
| bar_sweep_r | cyl | steel | 689 to 791 | 183 to 297 | 986 to 1020 |  | swept-back end, 100 across to 580 over the grips |
| grip_r | cyl | grip_black | 678 to 711 | 289 to 396 | 995 to 1025 |  | grip 28 across, 105 long |
| bell | cyl | steel | 761 to 813 | -176 to -124 | 1011 to 1037 |  | bell 52 across, a plain dome |
| bb_spindle | cyl | steel | 437 to 461 | -70 to 70 | 288 to 312 |  | bottom bracket spindle |
| chainring | cyl | steel | 359 to 539 | 52 to 58 | 210 to 390 |  | chainring 180 across, 6 thick (the chainguard is not modelled) |
| crank_r | box | steel | 439 to 619 | 58 to 70 | 290 to 310 |  | right crank arm 170 long |
| crank_l | box | steel | 279 to 459 | -70 to -58 | 290 to 310 |  | left crank arm 170 long |
| pedal_r | box | steel | 549 to 649 | 70 to 175 | 288 to 312 |  | pedal 100 x 105 x 24, rubber blocks not modelled |
| pedal_l | box | steel | 249 to 349 | -175 to -70 | 288 to 312 |  |  |

### Parts, variant BI2: BI2: the roadster leaning 12 degrees against a brick wall, handlebar end and pedal against it (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| rw_tyre1 | box | tyre | 292 to 330 | -100 to -37 | 258 to 387 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre2 | box | tyre | 246 to 329 | -125 to -61 | 372 to 506 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre3 | box | tyre | 163 to 277 | -145 to -84 | 478 to 598 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre4 | box | tyre | 55 to 183 | -156 to -101 | 560 to 648 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre5 | box | tyre | -62 to 62 | -156 to -111 | 604 to 650 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre6 | box | tyre | -183 to -55 | -156 to -101 | 560 to 648 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre7 | box | tyre | -277 to -163 | -145 to -84 | 478 to 598 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre8 | box | tyre | -329 to -246 | -125 to -61 | 372 to 506 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre9 | box | tyre | -330 to -292 | -100 to -37 | 258 to 387 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre10 | box | tyre | -329 to -246 | -76 to -12 | 139 to 273 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre11 | box | tyre | -277 to -163 | -53 to 8 | 48 to 168 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre12 | box | tyre | -183 to -55 | -36 to 18 | -3 to 86 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre13 | box | tyre | -62 to 62 | -26 to 19 | -4 to 41 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre14 | box | tyre | 55 to 183 | -36 to 18 | -3 to 86 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre15 | box | tyre | 163 to 277 | -53 to 8 | 48 to 168 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_tyre16 | box | tyre | 246 to 329 | -76 to -12 | 139 to 273 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| rw_hub | cyl | steel | -22 to 22 | -122 to -15 | 291 to 355 |  | hub 44 across, 100 long |
| rw_spoke1 | cyl | steel | 22 to 268 | -93 to -69 | 331 to 432 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke2 | cyl | steel | 8 to 112 | -125 to -72 | 344 to 585 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke3 | cyl | steel | -112 to -8 | -125 to -72 | 344 to 585 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke4 | cyl | steel | -268 to -22 | -93 to -69 | 331 to 432 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke5 | cyl | steel | -268 to -22 | -68 to -44 | 213 to 315 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke6 | cyl | steel | -112 to -8 | -65 to -12 | 60 to 302 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke7 | cyl | steel | 8 to 112 | -65 to -12 | 60 to 302 |  | spoke 2.4 across (8 drawn of 36) |
| rw_spoke8 | cyl | steel | 22 to 268 | -68 to -44 | 213 to 315 |  | spoke 2.4 across (8 drawn of 36) |
| fw_tyre1 | box | tyre | 1389 to 1427 | -100 to -37 | 258 to 387 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre2 | box | tyre | 1343 to 1425 | -125 to -61 | 372 to 506 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre3 | box | tyre | 1260 to 1374 | -145 to -84 | 478 to 598 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre4 | box | tyre | 1151 to 1280 | -156 to -101 | 560 to 648 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre5 | box | tyre | 1035 to 1159 | -156 to -111 | 604 to 650 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre6 | box | tyre | 913 to 1042 | -156 to -101 | 560 to 648 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre7 | box | tyre | 820 to 934 | -145 to -84 | 478 to 598 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre8 | box | tyre | 768 to 851 | -125 to -61 | 372 to 506 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre9 | box | tyre | 767 to 805 | -100 to -37 | 258 to 387 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre10 | box | tyre | 768 to 851 | -76 to -12 | 139 to 273 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre11 | box | tyre | 820 to 934 | -53 to 8 | 48 to 168 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre12 | box | tyre | 913 to 1042 | -36 to 18 | -3 to 86 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre13 | box | tyre | 1035 to 1159 | -26 to 19 | -4 to 41 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre14 | box | tyre | 1151 to 1280 | -36 to 18 | -3 to 86 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre15 | box | tyre | 1260 to 1374 | -53 to 8 | 48 to 168 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_tyre16 | box | tyre | 1343 to 1425 | -76 to -12 | 139 to 273 |  | tyre and rim segment (16 round the wheel), section 38 x 38 |
| fw_hub | cyl | steel | 1075 to 1119 | -122 to -15 | 291 to 355 |  | hub 44 across, 100 long |
| fw_spoke1 | cyl | steel | 1119 to 1365 | -93 to -69 | 331 to 432 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke2 | cyl | steel | 1105 to 1209 | -125 to -72 | 344 to 585 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke3 | cyl | steel | 985 to 1089 | -125 to -72 | 344 to 585 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke4 | cyl | steel | 828 to 1075 | -93 to -69 | 331 to 432 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke5 | cyl | steel | 828 to 1075 | -68 to -44 | 213 to 315 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke6 | cyl | steel | 985 to 1089 | -65 to -12 | 60 to 302 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke7 | cyl | steel | 1105 to 1209 | -65 to -12 | 60 to 302 |  | spoke 2.4 across (8 drawn of 36) |
| fw_spoke8 | cyl | steel | 1119 to 1365 | -68 to -44 | 213 to 315 |  | spoke 2.4 across (8 drawn of 36) |
| rw_guard1 | box | paint_black | 232 to 329 | -152 to -64 | 432 to 584 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard2 | box | paint_black | 83 to 234 | -169 to -93 | 568 to 661 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard3 | box | paint_black | -85 to 85 | -168 to -109 | 646 to 661 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard4 | box | paint_black | -234 to -83 | -169 to -93 | 568 to 661 |  | mudguard segment, 60 wide, 2 thick |
| rw_guard5 | box | paint_black | -329 to -232 | -152 to -64 | 432 to 584 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard1 | box | paint_black | 1336 to 1424 | -150 to -64 | 431 to 574 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard2 | box | paint_black | 1203 to 1339 | -167 to -91 | 559 to 653 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard3 | box | paint_black | 1047 to 1205 | -170 to -108 | 638 to 666 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard4 | box | paint_black | 902 to 1050 | -170 to -99 | 597 to 666 |  | mudguard segment, 60 wide, 2 thick |
| fw_guard5 | box | paint_black | 795 to 904 | -158 to -75 | 485 to 612 |  | mudguard segment, 60 wide, 2 thick |
| seat_tube | cyl | paint_black | 263 to 462 | -187 to -49 | 288 to 820 |  | seat tube 28 across, 560 centre to top, 72 degrees |
| top_tube | cyl | paint_black | 276 to 846 | -189 to -159 | 800 to 835 |  | top tube 28, 570 long, level |
| down_tube | cyl | paint_black | 439 to 912 | -160 to -48 | 282 to 697 |  | down tube 30 |
| head_tube | cyl | paint_black | 829 to 919 | -192 to -128 | 678 to 829 |  | head tube 36 across, 150 long, 68 degrees |
| chain_stay_l | cyl | paint_black | -1 to 450 | -130 to -108 | 274 to 319 |  | chain stay 16, 450 long |
| seat_stay_l | cyl | paint_black | -7 to 283 | -235 to -115 | 307 to 807 |  | seat stay 16 |
| fork_l | cyl | paint_black | 892 to 1107 | -213 to -114 | 305 to 679 |  | fork blade 22, rake 45 at the foot |
| chain_stay_r | cyl | paint_black | -1 to 450 | -23 to -1 | 297 to 342 |  | chain stay 16, 450 long |
| seat_stay_r | cyl | paint_black | -7 to 283 | -127 to -7 | 330 to 830 |  | seat stay 16 |
| fork_r | cyl | paint_black | 892 to 1107 | -100 to -1 | 329 to 703 |  | fork blade 22, rake 45 at the foot |
| seat_bridge | box | paint_black | 268 to 284 | -234 to -112 | 792 to 837 |  | seat-stay bridge |
| fork_crown | box | paint_black | 890 to 914 | -205 to -79 | 643 to 692 |  | fork crown |
| seat_post | cyl | steel | 220 to 287 | -216 to -162 | 811 to 967 |  | seat post 22 |
| saddle | box | saddle_black | 81 to 361 | -303 to -117 | 945 to 1031 | nose r 30, edges r 8 | saddle 280 x 180 x 50, leather-look, springs not modelled |
| stem | cyl | steel | 772 to 856 | -218 to -164 | 817 to 980 |  | stem 22, 170 above the head tube |
| bar_mid | cyl | steel | 771 to 793 | -395 to -19 | 925 to 1026 |  | handlebar: the straight middle, 22 across, 380 wide |
| bar_sweep_l | cyl | steel | 689 to 791 | -501 to -386 | 916 to 947 |  | swept-back end, 100 across to 580 over the grips |
| grip_l | cyl | grip_black | 678 to 711 | -599 to -491 | 893 to 941 |  | grip 28 across, 105 long |
| bar_sweep_r | cyl | steel | 689 to 791 | -29 to 81 | 1004 to 1058 |  | swept-back end, 100 across to 580 over the grips |
| grip_r | cyl | grip_black | 678 to 711 | 71 to 179 | 1034 to 1085 |  | grip 28 across, 105 long |
| bell | cyl | steel | 761 to 813 | -388 to -332 | 953 to 989 |  | bell 52 across, a plain dome |
| bb_spindle | cyl | steel | 437 to 461 | -133 to 9 | 267 to 320 |  | bottom bracket spindle |
| chainring | cyl | steel | 359 to 539 | -30 to 13 | 216 to 394 |  | chainring 180 across, 6 thick (the chainguard is not modelled) |
| crank_r | box | steel | 439 to 619 | -8 to 8 | 296 to 318 |  | right crank arm 170 long |
| crank_l | box | steel | 279 to 459 | -133 to -117 | 269 to 291 |  | left crank arm 170 long |
| pedal_r | box | steel | 549 to 649 | 4 to 111 | 296 to 342 |  | pedal 100 x 105 x 24, rubber blocks not modelled |
| pedal_l | box | steel | 249 to 349 | -236 to -128 | 245 to 291 |  |  |
| wall | box | wall_brick | -600 to 2000 | 179 to 379 | -50 to 2400 |  | the wall (a stand-in slab) |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | tyre outer diameter (the wheel) | 660 mm | Judgement | a 26 x 1 3/8 inch roadster tyre: 590 mm bead seat plus two 35 mm sections is about 660 (the ISO number is from memory: not reached on a page this session); error 10 | +-10 |
| N2 | wheelbase (axle to axle) | 1096.8 mm | Judgement | a gent's roadster's wheelbase is about 1100 to 1140; from the stated tube lengths and angles: 1097; error 40 | +-40 |
| N3 | saddle top above the ground | 1035 mm | Judgement | a rider of 1.75 m sits with the saddle about 1.0 m up; error 40 | +-40 |
| N4 | handlebar grips above the ground | 1024.2 mm | Judgement | roadster bars stand about as high as the saddle or just above it; error 40 | +-40 |
| N5 | bottom bracket height | 300 mm | Judgement | a roadster's bottom bracket is about 300 mm up (30 mm below the axles); error 15 | +-15 |
| N6 | handlebar width over the grips | 790 mm | Judgement | swept-back roadster bars are 560 to 620 between the bends and about 790 over the grips' ends; error 50 | +-50 |
| N7 | crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle) | 340 mm | Judgement | 170 mm, the usual crank; error 6 | +-6 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| paint_black | black enamel, chipped and rusting at the welds | 24, 26, 26 | 0.45 (semi-gloss) | metal | frame, forks, mudguards: chipped to red-brown rust at the dropouts, the lower head tube and the mudguard stays |
| steel | chrome-plated steel gone dull | 150, 152, 150 | 0.40 (dull satin) | metal | bars, stem, cranks, hubs, spokes: pitted with orange rust spots, never mirror bright |
| tyre | black rubber tyre, cracked, grey-white dust | 30, 30, 30 | 0.80 (matt) | not metal | a pale grey bloom of dust on the sidewalls; the rim (not separate) is dull steel in the 2 mm inner edge |
| saddle_black | saddle black leather-look, cracked | 34, 30, 28 | 0.55 (semi-matt) | not metal | cracked and shiny at the nose, a worn nose edge |
| grip_black | grips black rubber, worn | 22, 22, 22 | 0.70 (matt) | not metal |  |
| wall_brick | soot-blackened brick (the street's) | 78, 64, 58 | 0.90 (rough) | not metal | a stand-in |

### Wear

- enamel chipped to red-brown rust at the dropouts, the head tube's lower end, the seat-stay bridge and the mudguard stays; paint dulled, a few small dents in the mudguards
- chrome gone to dull grey with orange pitting on the bars, rims and spokes; the chain brown with oil and rust (not modelled)
- tyres hard, cracked at the sidewalls, one slightly soft (flat at the ground by 8 mm: a seed), grey dust bloom
- the saddle cracked and shiny at the nose; the grips worn smooth at their ends
- a wet street under it: darkness on the lowest 150 mm of the tyres and a grit splash on the mudguard
- NOT shown: a lock or chain bar (a chain through the wheel is a variant, a seed), a basket, stabilisers, any maker's badge on the head tube (a real bicycle has one; this has a blank plate)

### Variants the street needs

- BI2 (the sample): the roadster leaning 12 degrees on the wall.
- BI1: the same upright (for a bicycle held by a figure or standing on a stand).
- a ten-speed with drop bars is the second kind of adult bicycle of 1990: not written (its frame would be a new target); one kind only, as the street needs one bicycle.
- conditions (materials): C0 sound, C1 worn (the sample's wear), C2 rusted solid (S1's state, a derelict leaning for years).

### Where it stands on Quay Street

**Slot:** west side, against the blank soot-brick wall of the west_south block (the plain ground floor: no shopfront), centre x 15.0 m, the bicycle parallel to the wall with its handlebar end touching it, leaning 12 degrees, its tyres 0.34 m from the wall at the ground (the wall at z -5.125)

- the blank west wall is where the street's small things lean (the poster wall of the scene, x 11.4); a bicycle there blocks no shopfront and no door (the side door is at x 25.5)
- leaning, it takes a footway depth of its roll: a 12 degree lean puts the bar end and pedal 0.36 m from the tyres' line, leaving 1.64 m of the 2.0 m footway clear
- it is an adult's bicycle, ambient dressing that belongs to no one on the street's list of residents

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | which bicycle | the research notes list none; the brief asks for a bicycle against a wall | S1 shows an old roadster leaning on a wall (the type of the period's older riders); S2 shows the leaning pose with a modern bicycle | the roadster, upright geometry from the tube lengths and angles, the leaning pose from S2 |
| W2 | the lean | none | S2: the rear tyre on the ground, the front tyre and the bar end on the wall, a lean of about 12 degrees | 12 degrees, the wall touching the right grip's end |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: tyre outer diameter (the wheel) | measure it on the built mesh in millimetres (bbox) | 660 mm | +-10 mm |
| N2: wheelbase (axle to axle) | measure it on the built mesh in millimetres (centre_dx) | 1097 mm | +-40 mm |
| N3: saddle top above the ground | measure it on the built mesh in millimetres (edge) | 1035 mm | +-40 mm |
| N4: handlebar grips above the ground | measure it on the built mesh in millimetres (edge) | 1024 mm | +-40 mm |
| N5: bottom bracket height | measure it on the built mesh in millimetres (centre) | 300 mm | +-15 mm |
| N6: handlebar width over the grips | measure it on the built mesh in millimetres (span) | 790 mm | +-50 mm |
| N7: crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle) | measure it on the built mesh in millimetres (span) | 340 mm | +-6 mm |
| C1: both wheels the same diameter, on the ground | the tyres' bounding boxes | 660 mm, z 0 | +-10 mm |
| C2: no part floats; the bicycle touches the ground and the wall | the contact graph | connected | 0 floating |
| C3: the frame's tube angles | seat tube 72 degrees, head tube 68 degrees | 72 and 68 | +-2 degrees |
| C4: no lettering, no badge | textures and text | none | exact |

### For the builder

- build by script: the tubes as cylinders from the end points in target.json (a part's p0 and p1), the tyres as one torus of section 38 (the 16 boxes are the engine's approximation), the 36 spokes (8 drawn) in the real wheel; the mudguards as one swept strip per wheel
- BI2 is BI1 with the part transform (a roll of 12 degrees about the x axis through the tyre contacts) and the wall; the builder places the bicycle with the transform
- no maker's badge, no transfer, no lettering of any kind
- the right pedal and the right grip end are the two points that can touch the wall

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- no 1975 to 1995 bicycle photograph was measurable and S1 and S2 are oblique and low in contrast: every number is Judgement (a gent's roadster's usual geometry), checked for internal consistency and against ranges, not against pixels
- the 26 x 1 3/8 wheel's exact tyre diameter (660 mm is from memory; the page that gives the ISO 590 bead seat was not reached)
- whether the street's bicycle should be a roadster or a ten-speed (the roadster is chosen because S1 is a street-leaning roadster)
- the rear carrier, lamp and chain guard are not modelled (they are textures and decals); the chain is not modelled
- the lean's wall contact is by the handlebar end (S2 shows the front tyre against the wall): either is a seed

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the tube angles from the parts' own end points, the ranges for a roadster, the lean and the wall contact, the footway clearance). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
