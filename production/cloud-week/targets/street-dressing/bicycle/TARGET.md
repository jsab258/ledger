# Quay Street's bicycle against a wall: the exact target

**The bicycle is an adult's gent's roadster (26 x 1 3/8 wheels 660 mm over the tyre, a 1097 mm wheelbase, a level top tube on a 72 degree seat tube and a 68 degree head tube, swept-back bars 790 over the grips, a sprung saddle at 1035, mudguards with their stays and a red reflector, a plain bell, 170 mm cranks, a chain on an 18 tooth rear sprocket under a chainguard, rims as their own rings, rod brakes with 120 mm bar levers and stirrups under the rims, and a rear carrier 340 x 130 at 780) in the enamel-chipped, dull-chromed state of a street bicycle, no badge or lettering, shown leaning 12 degrees toward the soot-brick wall of the cottages (centre x 15.0, its left grip end on brick between the door at x 13.5 and the window at x 15.9: the wall is not blank, and the first version's lean was away from its wall); no period photograph was measurable (the two street photographs are oblique and low in contrast), so every number is Judgement within stated ranges and the target is checked for internal consistency, the tube angles and the ranges, not against pixels; an adult's bicycle only.**

Cloud week 42, unit 13, family 7. Written 13 October 2026, not yet reviewed. `SELF-CHECK bicycle: 79 checks, 77 passed, 2 failed; negative controls 0 of 0 caught (offline)`

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
| S1 | https://www.geograph.org.uk/photo/2932507 | 2026-10-13 | Jeremy Bolwell | CC BY-SA 2.0 (read on the page) | 2012-05-06 | a rusted gent's roadster leaning on a stone wall in a ruined building: a diamond frame with a level top tube, two big spoked wheels with mudguards, swept-back bars, a sprung saddle, a rear carrier; the rear wheel nearer the camera so the perspective is strong | YES | any number (the camera is oblique and close, the picture low in contrast); the rust is a wear state, not the sample's; the layout of the missing parts (no brake rod, chain or carrier reads in the 430 px crop, a rusted dark machine) | 2012, and an INTERIOR: the machine rests in a ruined chapel room, on its page 'maybe 50 years' (the Pant y Celyn Baptist ruin), so it dates the type, a roadster of the 1950s or before, not the street; the roadster for 1990 stays a Judgement (an older rider's bicycle, plausible in a port town); the alternative, named and not written, is a 1980s utility frame (a town bicycle on 26 x 1 3/8 wheels with cable callipers and a rear rack) |
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

Axes: x forward (the front wheel at +x), y to the rider's right, z up from the ground at the tyres' contact. Cylinders for tubes, spokes and the hub, boxes for the tyre and rim segments, the chain strips, the saddle, the cranks and the pedals; BI2 adds a transform that tips the top toward -y and a wall on that side.

### Assembly in words

- **Wheels**: 26 x 1 3/8, 660 over the tyre (a ring of 16 segments 38 x 38), a hub 44 across and 100 long, spokes 2.4 across (8 drawn of 36), mudguards 60 wide and 2 thick 8 mm over the tyre round the top 140 degrees.
- **Frame**: seat tube 28 across, 560 from the bottom bracket centre, 72 degrees; level top tube 28 across, 570 long; down tube 30 across; head tube 36 across and 150 long at 68 degrees; chain stays 16 across and 450 long, seat stays 16 across; the bottom bracket 300 up (30 below the axles).
- **Fork**: two blades 22 across with 45 rake at the foot, a crown 24 x 124 x 24.
- **Cockpit**: a stem 22 across rising 170 along the steering axis, a bar of 22 across, 380 straight between swept-back ends to 580 over the bends and 790 over the 105 mm grips, a bell 52 across.
- **Saddle and post**: a post 22 across to z 985, a saddle 280 x 180 x 50 at 985 to 1035.
- **Drive**: a spindle 24 across, a chainring 180 across (44 teeth, pitch circle 177.8), cranks 170, pedals 100 x 105 x 24; an 18 tooth sprocket 73 across on the rear hub; a chain 8 wide and 6 thick on the pitch circles (88.9 and 36.6 radius) with two runs on the common tangents (446.9 long) and 26 wrap strips, 102 links of 12.7 in all, in the plane y = 55, outboard of the chain stays at y = +-40; a chainguard of sheet steel 60 deep and 1 thick, 13 over the top run, from the sprocket's centre to 40 mm behind the chainring's front, on a clip to the right chain stay and a strap to the seat tube.
- **Rims and brakes**: each wheel has its own rim ring of 16 segments, 25 wide and 10 deep (radial) inside the tyre (outer face 292); rod brakes: two bar levers 120 long clamped under the grips (the left works the front), two rods 8 across running to a stirrup under each rim (a crossbar 56 wide at radius 270 with two arms to the fork blades and the seat stays, a bridge above the mudguard, two pads against the rim's inner face at 281); Judgement, the review's list.
- **Mudguard stays, reflector and carrier**: two 5 mm stays per mudguard to the drop-outs; a red reflector 60 across on the rear mudguard's tail; a rear carrier of 10 mm tube with a 340 x 130 platform at 780 over the rear wheel, its two stays running to the drop-outs (S1's own row lists a carrier; no number reads in the photograph).

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
| rw_rim1 | box | steel | 282 to 292 | -12 to 12 | 273 to 387 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim2 | box | steel | 239 to 292 | -12 to 12 | 385 to 494 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim3 | box | steel | 159 to 247 | -12 to 12 | 489 to 577 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim4 | box | steel | 55 to 164 | -12 to 12 | 569 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim5 | box | steel | -57 to 57 | -12 to 12 | 612 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim6 | box | steel | -164 to -55 | -12 to 12 | 569 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim7 | box | steel | -247 to -159 | -12 to 12 | 489 to 577 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim8 | box | steel | -292 to -239 | -12 to 12 | 385 to 494 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim9 | box | steel | -292 to -282 | -12 to 12 | 273 to 387 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim10 | box | steel | -292 to -239 | -12 to 12 | 166 to 275 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim11 | box | steel | -247 to -159 | -12 to 12 | 83 to 171 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim12 | box | steel | -164 to -55 | -12 to 12 | 38 to 91 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim13 | box | steel | -57 to 57 | -12 to 12 | 38 to 48 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim14 | box | steel | 55 to 164 | -12 to 12 | 38 to 91 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim15 | box | steel | 159 to 247 | -12 to 12 | 83 to 171 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim16 | box | steel | 239 to 292 | -12 to 12 | 166 to 275 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
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
| fw_rim1 | box | steel | 1379 to 1389 | -12 to 12 | 273 to 387 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim2 | box | steel | 1336 to 1388 | -12 to 12 | 385 to 494 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim3 | box | steel | 1256 to 1344 | -12 to 12 | 489 to 577 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim4 | box | steel | 1152 to 1261 | -12 to 12 | 569 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim5 | box | steel | 1040 to 1154 | -12 to 12 | 612 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim6 | box | steel | 932 to 1042 | -12 to 12 | 569 to 622 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim7 | box | steel | 850 to 938 | -12 to 12 | 489 to 577 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim8 | box | steel | 805 to 858 | -12 to 12 | 385 to 494 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim9 | box | steel | 805 to 815 | -12 to 12 | 273 to 387 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim10 | box | steel | 805 to 858 | -12 to 12 | 166 to 275 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim11 | box | steel | 850 to 938 | -12 to 12 | 83 to 171 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim12 | box | steel | 932 to 1042 | -12 to 12 | 38 to 91 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim13 | box | steel | 1040 to 1154 | -12 to 12 | 38 to 48 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim14 | box | steel | 1152 to 1261 | -12 to 12 | 38 to 91 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim15 | box | steel | 1256 to 1344 | -12 to 12 | 83 to 171 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim16 | box | steel | 1336 to 1388 | -12 to 12 | 166 to 275 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
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
| chain_stay_l | cyl | paint_black | -1 to 450 | -48 to -32 | 292 to 338 |  | chain stay 16, 450 long, 40 off the centre line (80 apart): the chain runs outboard of the right one |
| seat_stay_l | cyl | paint_black | -7 to 283 | -48 to -32 | 326 to 836 |  | seat stay 16 |
| chain_stay_r | cyl | paint_black | -1 to 450 | 32 to 48 | 292 to 338 |  | chain stay 16, 450 long, 40 off the centre line (80 apart): the chain runs outboard of the right one |
| seat_stay_r | cyl | paint_black | -7 to 283 | 32 to 48 | 326 to 836 |  | seat stay 16 |
| fork_l | cyl | paint_black | 892 to 1107 | -69 to -47 | 325 to 706 |  | fork blade 22, rake 45 at the foot |
| fork_r | cyl | paint_black | 892 to 1107 | 47 to 69 | 325 to 706 |  | fork blade 22, rake 45 at the foot |
| seat_bridge | box | paint_black | 268 to 284 | -45 to 45 | 823 to 843 |  | seat-stay bridge |
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
| sprocket | cyl | steel | -36 to 36 | 48 to 58 | 294 to 366 |  | rear sprocket: 18 teeth, 73 across (pitch circle 73.1), 10 thick, on the hub's drive end; Judgement (the review's 18 tooth, 73 mm) |
| chain_top | box | chain_dark | -2 to 445 | 51 to 59 | 364 to 392 |  | chain run (top): 446.9 long = 35.2 links of 12.7, 8 wide, 6 thick, on the pitch circles' common tangent; Judgement |
| chain_bot | box | chain_dark | -7 to 433 | 51 to 59 | 210 to 297 |  | chain run (bot): 446.9 long = 35.2 links of 12.7, 8 wide, 6 thick, on the pitch circles' common tangent; Judgement |
| chain_c01 | box | chain_dark | 433 to 454 | 51 to 59 | 208 to 215 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c02 | box | chain_dark | 454 to 476 | 51 to 59 | 208 to 218 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c03 | box | chain_dark | 474 to 496 | 51 to 59 | 212 to 226 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c04 | box | chain_dark | 493 to 513 | 51 to 59 | 221 to 239 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c05 | box | chain_dark | 509 to 527 | 51 to 59 | 235 to 255 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c06 | box | chain_dark | 522 to 537 | 51 to 59 | 252 to 274 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c07 | box | chain_dark | 531 to 541 | 51 to 59 | 272 to 295 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c08 | box | chain_dark | 534 to 541 | 51 to 59 | 294 to 316 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c09 | box | chain_dark | 528 to 540 | 51 to 59 | 315 to 337 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c10 | box | chain_dark | 517 to 533 | 51 to 59 | 334 to 356 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c11 | box | chain_dark | 502 to 522 | 51 to 59 | 352 to 372 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c12 | box | chain_dark | 485 to 506 | 51 to 59 | 367 to 383 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c13 | box | chain_dark | 465 to 487 | 51 to 59 | 378 to 390 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c14 | box | chain_dark | 444 to 466 | 51 to 59 | 384 to 392 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_s01 | box | chain_dark | -11 to -1 | 51 to 59 | 362 to 369 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s02 | box | chain_dark | -20 to -9 | 51 to 59 | 359 to 368 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s03 | box | chain_dark | -27 to -17 | 51 to 59 | 354 to 364 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s04 | box | chain_dark | -34 to -23 | 51 to 59 | 347 to 358 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s05 | box | chain_dark | -38 to -28 | 51 to 59 | 340 to 350 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s06 | box | chain_dark | -39 to -32 | 51 to 59 | 332 to 342 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s07 | box | chain_dark | -39 to -33 | 51 to 59 | 323 to 333 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s08 | box | chain_dark | -39 to -31 | 51 to 59 | 314 to 324 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s09 | box | chain_dark | -36 to -26 | 51 to 59 | 306 to 317 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s10 | box | chain_dark | -31 to -21 | 51 to 59 | 299 to 310 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s11 | box | chain_dark | -24 to -14 | 51 to 59 | 294 to 304 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s12 | box | chain_dark | -16 to -6 | 51 to 59 | 291 to 300 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chainguard | box | paint_black | -1 to 498 | 25 to 85 | 379 to 405 | edges rolled 3 mm | chainguard: sheet steel 60 deep, 1 thick, from the sprocket's centre (x 0) to x 499 (40 mm behind the chainring's front), 13 over the chain's pitch line; Judgement (the review's numbers) |
| chainguard_clip | box | paint_black | 8 to 22 | 36 to 44 | 336 to 380 |  | clip 14 x 8 from the right chain stay up to the guard's rear end |
| chainguard_strap | cyl | paint_black | 430 to 496 | 7 to 39 | 381 to 407 |  | strap rod 6 across from the guard's front end to the seat tube |
| fw_stirrup_bar | cyl | steel | 968 to 974 | -28 to 28 | 566 to 572 |  | stirrup crossbar 6 across, 56 wide, under the rim at radius 270 (the rim's inner face is 282), at 117.7 degrees on the wheel; Judgement |
| fw_stirrup_arm_l | cyl | steel | 927 to 974 | -58 to -25 | 567 to 650 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| fw_stirrup_arm_r | cyl | steel | 927 to 974 | 25 to 58 | 567 to 650 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| fw_brake_bridge | box | paint_black | 921 to 937 | -55 to 55 | 641 to 657 |  | brake bridge 16 x 16 between the two members at radius 360, above the mudguard |
| fw_pad_l | box | grip_black | 948 to 990 | -19 to -5 | 557 to 588 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| fw_pad_r | box | grip_black | 948 to 990 | 5 to 19 | 557 to 588 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| rw_stirrup_bar | cyl | steel | 127 to 133 | -28 to 28 | 564 to 570 |  | stirrup crossbar 6 across, 56 wide, under the rim at radius 270 (the rim's inner face is 282), at 61.2 degrees on the wheel; Judgement |
| rw_stirrup_arm_l | cyl | steel | 127 to 176 | -43 to -25 | 565 to 647 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| rw_stirrup_arm_r | cyl | steel | 127 to 176 | 25 to 43 | 565 to 647 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| rw_brake_bridge | box | paint_black | 165 to 181 | -40 to 40 | 638 to 654 |  | brake bridge 16 x 16 between the two members at radius 360, above the mudguard |
| rw_pad_l | box | grip_black | 111 to 153 | -19 to -5 | 554 to 586 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| rw_pad_r | box | grip_black | 111 to 153 | 5 to 19 | 554 to 586 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| brake_lever_l | cyl | steel | 692 to 797 | -336 to -324 | 922 to 1001 |  | bar lever 120 long, 12 across, clamped under the grip's inner end; the left works the front brake, the right the rear; Judgement |
| brake_rod_f | cyl | steel | 790 to 933 | -333 to -52 | 646 to 930 |  | brake rod 8 across from the lever's tip to the stirrup's joint on the fork blade; Judgement |
| brake_lever_r | cyl | steel | 692 to 797 | 324 to 336 | 922 to 1001 |  | bar lever 120 long, 12 across, clamped under the grip's inner end; the left works the front brake, the right the rear; Judgement |
| brake_rod_r | cyl | steel | 171 to 796 | 36 to 334 | 642 to 931 |  | brake rod 8 across from the lever's tip to the stirrup's joint on the seat stay; Judgement |
| fw_guard_stay_l | cyl | paint_black | 1096 to 1423 | -59 to -26 | 328 to 452 |  | mudguard stay 5 across from the guard's front end to the drop-out; Judgement |
| fw_guard_stay_r | cyl | paint_black | 1096 to 1423 | 26 to 59 | 328 to 452 |  | mudguard stay 5 across from the guard's front end to the drop-out; Judgement |
| rw_guard_stay_l | cyl | paint_black | -328 to 1 | -59 to -26 | 328 to 452 |  | mudguard stay 5 across from the guard's rear end to the drop-out; Judgement |
| rw_guard_stay_r | cyl | paint_black | -328 to 1 | 26 to 59 | 328 to 452 |  | mudguard stay 5 across from the guard's rear end to the drop-out; Judgement |
| rw_reflector | cyl | reflector_red | -239 to -233 | -30 to 30 | 558 to 618 |  | rear reflector 60 across, 6 thick, on the rear mudguard's tail, facing back; Judgement |
| carrier_deck | box | paint_black | -101 to 239 | -65 to 65 | 776 to 780 |  | carrier platform 340 x 130, a 4 mm sheet on the tube frame, top at 780; Judgement |
| carrier_rail_l | cyl | paint_black | -101 to 239 | -70 to -60 | 766 to 776 |  | carrier side rail, 10 mm tube, 340 long |
| carrier_rail_r | cyl | paint_black | -101 to 239 | 60 to 70 | 766 to 776 |  | carrier side rail, 10 mm tube, 340 long |
| carrier_cross_rear | cyl | paint_black | -106 to -96 | -65 to 65 | 766 to 776 |  | carrier rear cross rail, 10 mm tube |
| carrier_stay_l | cyl | paint_black | -106 to -37 | -70 to -52 | 339 to 772 |  | carrier stay, 10 mm tube, from the rail's rear end to the drop-out; Judgement |
| carrier_stay_r | cyl | paint_black | -106 to -37 | 52 to 70 | 339 to 772 |  | carrier stay, 10 mm tube, from the rail's rear end to the drop-out; Judgement |

### Parts, variant BI2: BI2: the roadster leaning 12 degrees toward a brick wall, its left grip end against it (the sample) (millimetres)

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
| rw_rim1 | box | steel | 282 to 292 | -93 to -45 | 264 to 381 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim2 | box | steel | 239 to 292 | -115 to -68 | 374 to 486 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim3 | box | steel | 159 to 247 | -132 to -89 | 476 to 567 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim4 | box | steel | 55 to 164 | -141 to -106 | 554 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim5 | box | steel | -57 to 57 | -142 to -115 | 596 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim6 | box | steel | -164 to -55 | -141 to -106 | 554 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim7 | box | steel | -247 to -159 | -132 to -89 | 476 to 567 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim8 | box | steel | -292 to -239 | -115 to -68 | 374 to 486 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim9 | box | steel | -292 to -282 | -93 to -45 | 264 to 381 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim10 | box | steel | -292 to -239 | -69 to -22 | 159 to 271 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim11 | box | steel | -247 to -159 | -48 to -5 | 79 to 170 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim12 | box | steel | -164 to -55 | -31 to 4 | 35 to 92 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim13 | box | steel | -57 to 57 | -22 to 4 | 35 to 50 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim14 | box | steel | 55 to 164 | -31 to 4 | 35 to 92 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim15 | box | steel | 159 to 247 | -48 to -5 | 79 to 170 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| rw_rim16 | box | steel | 239 to 292 | -69 to -22 | 159 to 271 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
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
| fw_rim1 | box | steel | 1379 to 1389 | -93 to -45 | 264 to 381 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim2 | box | steel | 1336 to 1388 | -115 to -68 | 374 to 486 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim3 | box | steel | 1256 to 1344 | -132 to -89 | 476 to 567 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim4 | box | steel | 1152 to 1261 | -141 to -106 | 554 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim5 | box | steel | 1040 to 1154 | -142 to -115 | 596 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim6 | box | steel | 932 to 1042 | -141 to -106 | 554 to 611 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim7 | box | steel | 850 to 938 | -132 to -89 | 476 to 567 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim8 | box | steel | 805 to 858 | -115 to -68 | 374 to 486 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim9 | box | steel | 805 to 815 | -93 to -45 | 264 to 381 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim10 | box | steel | 805 to 858 | -69 to -22 | 159 to 271 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim11 | box | steel | 850 to 938 | -48 to -5 | 79 to 170 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim12 | box | steel | 932 to 1042 | -31 to 4 | 35 to 92 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim13 | box | steel | 1040 to 1154 | -22 to 4 | 35 to 50 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim14 | box | steel | 1152 to 1261 | -31 to 4 | 35 to 92 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim15 | box | steel | 1256 to 1344 | -48 to -5 | 79 to 170 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
| fw_rim16 | box | steel | 1336 to 1388 | -69 to -22 | 159 to 271 |  | rim segment (16 round the wheel): 25 wide, 10 deep, dull steel, the tyre's seat; Judgement |
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
| chain_stay_l | cyl | paint_black | -1 to 450 | -116 to -94 | 277 to 322 |  | chain stay 16, 450 long, 40 off the centre line (80 apart): the chain runs outboard of the right one |
| seat_stay_l | cyl | paint_black | -7 to 283 | -220 to -100 | 310 to 810 |  | seat stay 16 |
| chain_stay_r | cyl | paint_black | -1 to 450 | -37 to -15 | 294 to 339 |  | chain stay 16, 450 long, 40 off the centre line (80 apart): the chain runs outboard of the right one |
| seat_stay_r | cyl | paint_black | -7 to 283 | -142 to -22 | 327 to 827 |  | seat stay 16 |
| fork_l | cyl | paint_black | 892 to 1107 | -213 to -114 | 305 to 679 |  | fork blade 22, rake 45 at the foot |
| fork_r | cyl | paint_black | 892 to 1107 | -100 to -1 | 329 to 703 |  | fork blade 22, rake 45 at the foot |
| seat_bridge | box | paint_black | 268 to 284 | -219 to -127 | 795 to 834 |  | seat-stay bridge |
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
| sprocket | cyl | steel | -36 to 36 | -29 to -4 | 297 to 371 |  | rear sprocket: 18 teeth, 73 across (pitch circle 73.1), 10 thick, on the hub's drive end; Judgement (the review's 18 tooth, 73 mm) |
| chain_top | box | chain_dark | -2 to 445 | -32 to -18 | 366 to 396 |  | chain run (top): 446.9 long = 35.2 links of 12.7, 8 wide, 6 thick, on the pitch circles' common tangent; Judgement |
| chain_bot | box | chain_dark | -7 to 433 | -12 to 14 | 216 to 303 |  | chain run (bot): 446.9 long = 35.2 links of 12.7, 8 wide, 6 thick, on the pitch circles' common tangent; Judgement |
| chain_c01 | box | chain_dark | 433 to 454 | 5 to 14 | 214 to 223 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c02 | box | chain_dark | 454 to 476 | 5 to 14 | 214 to 225 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c03 | box | chain_dark | 474 to 496 | 3 to 14 | 218 to 234 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c04 | box | chain_dark | 493 to 513 | 0 to 12 | 227 to 246 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c05 | box | chain_dark | 509 to 527 | -3 to 9 | 240 to 262 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c06 | box | chain_dark | 522 to 537 | -7 to 5 | 257 to 281 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c07 | box | chain_dark | 531 to 541 | -11 to 1 | 277 to 300 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c08 | box | chain_dark | 534 to 541 | -16 to -3 | 298 to 321 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c09 | box | chain_dark | 528 to 540 | -20 to -8 | 318 to 342 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c10 | box | chain_dark | 517 to 533 | -24 to -12 | 338 to 360 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c11 | box | chain_dark | 502 to 522 | -27 to -16 | 355 to 376 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c12 | box | chain_dark | 485 to 506 | -30 to -19 | 370 to 387 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c13 | box | chain_dark | 465 to 487 | -31 to -21 | 380 to 394 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_c14 | box | chain_dark | 444 to 466 | -32 to -22 | 387 to 396 |  | chain on the chainring: 1.7 links of 12.7 in this strip; Judgement |
| chain_s01 | box | chain_dark | -11 to -1 | -27 to -18 | 365 to 374 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s02 | box | chain_dark | -20 to -9 | -27 to -17 | 361 to 372 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s03 | box | chain_dark | -27 to -17 | -26 to -16 | 357 to 368 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s04 | box | chain_dark | -34 to -23 | -25 to -14 | 350 to 362 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s05 | box | chain_dark | -38 to -28 | -23 to -13 | 343 to 355 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s06 | box | chain_dark | -39 to -32 | -21 to -11 | 335 to 346 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s07 | box | chain_dark | -39 to -33 | -19 to -10 | 327 to 338 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s08 | box | chain_dark | -39 to -31 | -18 to -8 | 318 to 330 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s09 | box | chain_dark | -36 to -26 | -16 to -6 | 310 to 322 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s10 | box | chain_dark | -31 to -21 | -15 to -4 | 303 to 315 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s11 | box | chain_dark | -24 to -14 | -13 to -3 | 298 to 309 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chain_s12 | box | chain_dark | -16 to -6 | -12 to -3 | 295 to 305 |  | chain on the sprocket: 0.7 links of 12.7 in this strip; Judgement |
| chainguard | box | paint_black | -1 to 498 | -60 to 4 | 376 to 414 | edges rolled 3 mm | chainguard: sheet steel 60 deep, 1 thick, from the sprocket's centre (x 0) to x 499 (40 mm behind the chainring's front), 13 over the chain's pitch line; Judgement (the review's numbers) |
| chainguard_clip | box | paint_black | 8 to 22 | -44 to -27 | 336 to 381 |  | clip 14 x 8 from the right chain stay up to the guard's rear end |
| chainguard_strap | cyl | paint_black | 430 to 496 | -73 to -46 | 375 to 405 |  | strap rod 6 across from the guard's front end to the seat tube |
| fw_stirrup_bar | cyl | steel | 968 to 974 | -146 to -90 | 548 to 565 |  | stirrup crossbar 6 across, 56 wide, under the rim at radius 270 (the rim's inner face is 282), at 117.7 degrees on the wheel; Judgement |
| fw_stirrup_arm_l | cyl | steel | 927 to 974 | -191 to -143 | 549 to 625 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| fw_stirrup_arm_r | cyl | steel | 927 to 974 | -94 to -78 | 561 to 647 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| fw_brake_bridge | box | paint_black | 921 to 937 | -190 to -79 | 615 to 654 |  | brake bridge 16 x 16 between the two members at radius 360, above the mudguard |
| fw_pad_l | box | grip_black | 948 to 990 | -141 to -121 | 541 to 574 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| fw_pad_r | box | grip_black | 948 to 990 | -117 to -97 | 546 to 579 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| rw_stirrup_bar | cyl | steel | 127 to 133 | -146 to -90 | 546 to 563 |  | stirrup crossbar 6 across, 56 wide, under the rim at radius 270 (the rim's inner face is 282), at 61.2 degrees on the wheel; Judgement |
| rw_stirrup_arm_l | cyl | steel | 127 to 176 | -176 to -142 | 547 to 625 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| rw_stirrup_arm_r | cyl | steel | 127 to 176 | -98 to -87 | 559 to 641 |  | stirrup arm 6 across from the crossbar's end to the frame member |
| rw_brake_bridge | box | paint_black | 165 to 181 | -175 to -93 | 615 to 648 |  | brake bridge 16 x 16 between the two members at radius 360, above the mudguard |
| rw_pad_l | box | grip_black | 111 to 153 | -140 to -120 | 538 to 572 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| rw_pad_r | box | grip_black | 111 to 153 | -117 to -97 | 543 to 577 |  | brake pad 40 x 14 x 14 on the stirrup, against the rim's inner face (rod brake); Judgement |
| brake_lever_l | cyl | steel | 692 to 797 | -536 to -510 | 834 to 911 |  | bar lever 120 long, 12 across, clamped under the grip's inner end; the left works the front brake, the right the rear; Judgement |
| brake_rod_f | cyl | steel | 790 to 933 | -518 to -186 | 620 to 842 |  | brake rod 8 across from the lever's tip to the stirrup's joint on the fork blade; Judgement |
| brake_lever_r | cyl | steel | 692 to 797 | 110 to 136 | 971 to 1048 |  | bar lever 120 long, 12 across, clamped under the grip's inner end; the left works the front brake, the right the rear; Judgement |
| brake_rod_r | cyl | steel | 171 to 796 | -99 to 134 | 636 to 979 |  | brake rod 8 across from the lever's tip to the stirrup's joint on the seat stay; Judgement |
| fw_guard_stay_l | cyl | paint_black | 1096 to 1423 | -127 to -118 | 309 to 436 |  | mudguard stay 5 across from the guard's front end to the drop-out; Judgement |
| fw_guard_stay_r | cyl | paint_black | 1096 to 1423 | -69 to -10 | 332 to 448 |  | mudguard stay 5 across from the guard's front end to the drop-out; Judgement |
| rw_guard_stay_l | cyl | paint_black | -328 to 1 | -127 to -118 | 309 to 437 |  | mudguard stay 5 across from the guard's rear end to the drop-out; Judgement |
| rw_guard_stay_r | cyl | paint_black | -328 to 1 | -69 to -10 | 332 to 448 |  | mudguard stay 5 across from the guard's rear end to the drop-out; Judgement |
| rw_reflector | cyl | reflector_red | -239 to -233 | -152 to -92 | 545 to 605 |  | rear reflector 60 across, 6 thick, on the rear mudguard's tail, facing back; Judgement |
| carrier_deck | box | paint_black | -101 to 239 | -226 to -98 | 746 to 776 |  | carrier platform 340 x 130, a 4 mm sheet on the tube frame, top at 780; Judgement |
| carrier_rail_l | cyl | paint_black | -101 to 239 | -229 to -219 | 736 to 746 |  | carrier side rail, 10 mm tube, 340 long |
| carrier_rail_r | cyl | paint_black | -101 to 239 | -102 to -92 | 763 to 773 |  | carrier side rail, 10 mm tube, 340 long |
| carrier_cross_rear | cyl | paint_black | -106 to -96 | -225 to -96 | 736 to 773 |  | carrier rear cross rail, 10 mm tube |
| carrier_stay_l | cyl | paint_black | -106 to -37 | -229 to -122 | 319 to 742 |  | carrier stay, 10 mm tube, from the rail's rear end to the drop-out; Judgement |
| carrier_stay_r | cyl | paint_black | -106 to -37 | -102 to -10 | 343 to 769 |  | carrier stay, 10 mm tube, from the rail's rear end to the drop-out; Judgement |
| wall | box | wall_brick | -600 to 2000 | -799 to -599 | -50 to 2400 |  | the wall (a stand-in slab) on the side the bicycle leans toward (-y) |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | tyre outer diameter (the wheel) | 660 mm | Judgement | a 26 x 1 3/8 inch roadster tyre: 590 mm bead seat plus two 35 mm sections is about 660 (the ISO number is from memory: not reached on a page this session); error 10 | +-10 |
| N2 | wheelbase (axle to axle) | 1096.8 mm | Judgement | a gent's roadster's wheelbase is about 1100 to 1140; from the stated tube lengths and angles: 1097; error 40 | +-40 |
| N3 | saddle top above the ground | 1035 mm | Judgement | a rider of 1.75 m sits with the saddle about 1.0 m up; error 40 | +-40 |
| N4 | handlebar grips above the ground | 1024.2 mm | Judgement | roadster bars stand about as high as the saddle or just above it; error 40 | +-40 |
| N5 | bottom bracket height | 300 mm | Judgement | a roadster's bottom bracket is about 300 mm up (30 mm below the axles); error 15 | +-15 |
| N6 | handlebar width over the grips | 790 mm | Judgement | swept-back roadster bars are 560 to 620 between the bends and about 790 over the grips' ends; error 50 | +-50 |
| N8 | rear sprocket diameter (18 teeth) | 73 mm | Judgement | the review of 13 October: an 18 tooth sprocket 73 mm across (12.7 pitch: pitch circle 73.2); S1 shows a rusted wheel in which no sprocket reads; error 3 | +-3 |
| N9 | chainguard depth across the bicycle | 60 mm | Judgement | the review: sheet steel 60 deep, 1 thick; no chainguard reads in S1; error 5 | +-5 |
| N10 | rim width | 25 mm | Judgement | the review: rims 25 wide, 10 deep, as their own ring (a 26 x 1 3/8 steel rim is about 22 to 25 wide); S1's rims read as thin rings; error 3 | +-3 |
| N11 | carrier platform length | 340 mm | Judgement | the review: a 340 x 130 platform of 10 mm tube at 780 over the rear wheel; S1's own row lists a rear carrier but at 430 px no number reads; error 20 | +-20 |
| N12 | carrier platform width | 130 mm | Judgement | the review (130); error 15 | +-15 |
| N13 | carrier platform top above the ground | 780 mm | Judgement | the review (780 over the rear wheel, 120 over the mudguard's top at 668); error 30 | +-30 |
| N14 | rear reflector diameter | 60 mm | Judgement | the review: a red reflector 60 across on the rear mudguard; error 3 | +-3 |
| N7 | crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle) | 340 mm | Judgement | 170 mm, the usual crank; error 6 | +-6 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| paint_black | black enamel, chipped and rusting at the welds | 24, 26, 26 | 0.45 (semi-gloss) | metal | frame, forks, mudguards: chipped to red-brown rust at the dropouts, the lower head tube and the mudguard stays |
| steel | chrome-plated steel gone dull | 150, 152, 150 | 0.40 (dull satin) | metal | bars, stem, cranks, hubs, spokes: pitted with orange rust spots, never mirror bright |
| tyre | black rubber tyre, cracked, grey-white dust | 30, 30, 30 | 0.80 (matt) | not metal | a pale grey bloom of dust on the sidewalls; the rim is its own ring inside it (steel) |
| saddle_black | saddle black leather-look, cracked | 34, 30, 28 | 0.55 (semi-matt) | not metal | cracked and shiny at the nose, a worn nose edge |
| grip_black | grips black rubber, worn | 22, 22, 22 | 0.70 (matt) | not metal | also the brake pads |
| chain_dark | chain, brown with oil and rust | 62, 46, 34 | 0.60 (matt) | metal | the plates rust-brown, the rollers oily black; a line of oil spots on the right chain stay below it |
| reflector_red | rear reflector, red plastic, scratched | 150, 18, 22 | 0.30 (glossy, scratched) | not metal | the only saturated colour on the bicycle: 60 mm across |
| wall_brick | soot-blackened brick (the street's) | 78, 64, 58 | 0.90 (rough) | not metal | a stand-in |

### Wear

- enamel chipped to red-brown rust at the dropouts, the head tube's lower end, the seat-stay bridge and the mudguard stays; paint dulled, a few small dents in the mudguards
- chrome gone to dull grey with orange pitting on the bars, rims and spokes; the chain brown with oil and rust, a line of oil spots below the lower run
- tyres hard, cracked at the sidewalls, one slightly soft (flat at the ground by 8 mm: a seed), grey dust bloom
- the saddle cracked and shiny at the nose; the grips worn smooth at their ends
- a wet street under it: darkness on the lowest 150 mm of the tyres and a grit splash on the mudguard
- NOT shown: a lock or chain bar (a chain through the wheel is a variant, a seed), a basket, stabilisers, any maker's badge on the head tube (a real bicycle has one; this has a blank plate)

### Variants the street needs

- BI2 (the sample): the roadster leaning 12 degrees toward the wall, its left grip end against the brick.
- BI1: the same upright (for a bicycle held by a figure or standing on a stand).
- a ten-speed with drop bars is the second kind of adult bicycle of 1990: not written (its frame would be a new target); one kind only, as the street needs one bicycle.
- conditions (materials): C0 sound, C1 worn (the sample's wear), C2 rusted solid (S1's state, a derelict leaning for years).

### Where it stands on Quay Street

**Slot:** west side, against the soot-brick wall of the west_south block (the plain ground floor: no shopfront), the bicycle parallel to the wall facing +x (up the street), its LEFT grip end touching the brick, leaning 12 degrees toward the wall (the first version leaned it away from the wall: the wall stood on the side the top tips away from), its tyres 0.60 m from the wall at the ground; the rear tyre's back at x 14.12, the front tyre's front at x 15.88 (centre x 15.0), the grip's contact at x 15.15 on brick between the cottage door at x 13.5 (the doorstep to x 14.0) and the cottage window at x 15.9 (its sill from x 15.425); the wall at z -5.125

- the soot-brick wall of the cottages is where small things lean (the poster wall of the scene, x 11.4); it is NOT blank at x 14.1 to 15.9: the drawn plain row has a household door at x 13.5 (opening 13.08 to 13.92, a doorstep 0.998 wide and 0.35 m deep to x 14.0), a cottage window at x 15.9 (opening 15.475 to 16.325, sill 0.82 m above the crown, its stone sill 50 mm proud from x 15.425) and another at x 17.7; the first version's 'no door (the side door is at x 25.5)' read x 25.5 on the west_north block and missed all of it
- the slot keeps the grip's contact on brick: the left grip's end touches the wall at x 15.15, 0.28 m from the window's sill and 1.15 m from the doorstep's edge; both tyres stand clear of the door: the rear tyre's back (x 14.12) is 0.2 m past the door's approach (x 13.92) and 0.12 m past the doorstep's end (x 14.0), and the tyres stand 0.6 m out, 0.25 m beyond the step's front edge (0.35 m)
- leaning, it takes a footway depth of its roll: a 12 degree lean puts the left grip end 0.60 m from the tyres' line and the right pedal and grip 0.18 m on the other side, so the bicycle takes 0.78 m of the 2.0 m footway and leaves 1.22 m clear on the kerb side (the first version's 0.34 m and 1.64 m came from the same wall on the wrong side)
- it is an adult's bicycle, ambient dressing that belongs to no one on the street's list of residents

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | which bicycle | the research notes list none; the brief asks for a bicycle against a wall | S1 shows an old roadster leaning on a wall (the type of the period's older riders); S2 shows the leaning pose with a modern bicycle | the roadster, upright geometry from the tube lengths and angles, the leaning pose from S2 |
| W3 | the missing parts | the first version: a frame, wheels, bars, saddle, cranks and bell only; 'the carrier, lamp and chain guard are textures; the chain is not modelled' | S1's own row lists a rear carrier; a street bicycle always shows brakes, a chain and rims (the review of 13 October); none reads at the 430 px of the crop, so every added number is the review's Judgement | the chain, sprocket, chainguard, rims, rod brakes, mudguard stays, carrier and reflector are geometry, each with a row |
| W4 | the wall's side | the first version leaned the bicycle toward -y and put the wall on the +y side, against the right grip | n/a (arithmetic): the roll [0, 0, +12] tips a point (0, 0, 1000) to y -208, so the top moves toward -y and only a wall on the -y side can hold it | the wall on the -y side, the left grip's end against it (found while checking the slot's neighbours; the review did not list it) |
| W2 | the lean | none | S2: the rear tyre on the ground, the front tyre and the bar end on the wall, a lean of about 12 degrees | 12 degrees, the wall touching the left grip's end |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: tyre outer diameter (the wheel) | measure it on the built mesh in millimetres (bbox) | 660 mm | +-10 mm |
| N2: wheelbase (axle to axle) | measure it on the built mesh in millimetres (centre_dx) | 1097 mm | +-40 mm |
| N3: saddle top above the ground | measure it on the built mesh in millimetres (edge) | 1035 mm | +-40 mm |
| N4: handlebar grips above the ground | measure it on the built mesh in millimetres (edge) | 1024 mm | +-40 mm |
| N5: bottom bracket height | measure it on the built mesh in millimetres (centre) | 300 mm | +-15 mm |
| N6: handlebar width over the grips | measure it on the built mesh in millimetres (span) | 790 mm | +-50 mm |
| N8: rear sprocket diameter (18 teeth) | measure it on the built mesh in millimetres (extent) | 73 mm | +-3 mm |
| N9: chainguard depth across the bicycle | measure it on the built mesh in millimetres (extent) | 60 mm | +-5 mm |
| N10: rim width | measure it on the built mesh in millimetres (extent) | 25 mm | +-3 mm |
| N11: carrier platform length | measure it on the built mesh in millimetres (extent) | 340 mm | +-20 mm |
| N12: carrier platform width | measure it on the built mesh in millimetres (extent) | 130 mm | +-15 mm |
| N13: carrier platform top above the ground | measure it on the built mesh in millimetres (edge) | 780 mm | +-30 mm |
| N14: rear reflector diameter | measure it on the built mesh in millimetres (extent) | 60 mm | +-3 mm |
| N7: crank span: the two arms' outer ends along x (two cranks of 170, crossing at the spindle) | measure it on the built mesh in millimetres (span) | 340 mm | +-6 mm |
| C1: both wheels the same diameter, on the ground | the tyres' bounding boxes | 660 mm, z 0 | +-10 mm |
| C2: no part floats; the bicycle touches the ground and the wall | the contact graph | connected | 0 floating |
| C3: the frame's tube angles | seat tube 72 degrees, head tube 68 degrees | 72 and 68 | +-2 degrees |
| C4: no lettering, no badge | textures and text | none | exact |
| C5: the drive | chain 8 x 6 on the pitch circles of the 44 tooth ring (88.9) and the 18 tooth sprocket (36.6, 73 across), 102 links of 12.7 (within half a link), outboard of the stays | as stated | +-1.5 mm |
| C6: the chainguard, rims, brakes, stays, carrier and reflector are present with their numbers | guard 60 deep 1 thick over the top run; two 25 x 10 rim rings; two 120 levers, two 8 rods, two stirrups under the rims; two 5 mm stays per mudguard; carrier 340 x 130 at 780; reflector 60 | as stated | see numbers |
| C7: the contact on brick | the left grip's end touches the wall at a street x outside every drawn opening (door, doorstep, window and its sill) | x 15.15 on brick | 0.1 m clear |

### For the builder

- build by script: the tubes as cylinders from the end points in target.json (a part's p0 and p1), the tyres as one torus of section 38 (the 16 boxes are the engine's approximation), the 36 spokes (8 drawn) in the real wheel; the mudguards as one swept strip per wheel
- BI2 is BI1 with the part transform (a roll of 12 degrees about the x axis through the tyre contacts) and the wall; the builder places the bicycle with the transform
- no maker's badge, no transfer, no lettering of any kind
- the left grip end is the point that touches the wall (the lean tips the top toward -y, the rider's left; the first version put the wall on the other side); stand the sample at the pose in target.json (yaw 0, x 14.45, z from the wall less the grip's reach)
- the chain: strips of 8 x 6 mm on the pitch circles (88.9 and 36.6 radius) joined by two runs on the common tangents; build real links of 12.7 pitch along the same path (102 links); the chain, ring and sprocket lie in the plane y = 55, outboard of the chain stays at y = +-40

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- no 1975 to 1995 bicycle photograph was measurable and S1 and S2 are oblique and low in contrast: every number is Judgement (a gent's roadster's usual geometry), checked for internal consistency and against ranges, not against pixels
- the 26 x 1 3/8 wheel's exact tyre diameter (660 mm is from memory; the page that gives the ISO 590 bead seat was not reached)
- whether the street's bicycle should be a roadster or a ten-speed (the roadster is chosen because S1 is a street-leaning roadster)
- added after the review of 13 October (each a Judgement from its list, none readable in S1 or S3 at the size they are seen): the chain on its pitch circles, the 18 tooth sprocket, the chainguard, the rims as their own ring, rod brakes (two 120 mm levers, two 8 mm rods, a stirrup under each rim), two 5 mm stays on each mudguard, the 340 x 130 carrier at 780 and the 60 mm red reflector; the lamp is not modelled (a dynamo lamp, a texture and decal if wanted); the chain's links are lumped in strips (each says how many links it stands for)
- the brake type: rod brakes with stirrups under the rims are the review's first choice and fit a roadster; side-pull callipers with a 60 mm reach are the cable alternative (a 1980s town bicycle) and are not written
- the lean's wall contact is by the left grip end (S2 shows the front tyre against the wall): either is a seed

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the tube angles from the parts' own end points, the ranges for a roadster, the drive (pitch circles, tangent runs, 102 links, the plane outboard of the stays), the chainguard, rims, rod brakes, mudguard stays, carrier and reflector with their numbers, the lean toward the wall and the wall contact, the contact on brick clear of every drawn opening, the slot against the street's pieces and door zones). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
