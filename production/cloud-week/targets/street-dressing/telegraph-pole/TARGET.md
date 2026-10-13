# Quay Street's telegraph pole with its wires: the exact target

**The telegraph pole is a creosoted pine pole 8.0 m above the pavement, 230 mm across at the ground tapering to 150, with a galvanised cap, a distribution bracket of six porcelain knobs just under the top, eleven climbing pegs every 450 mm on alternate sides from 2.4 m, and four black drop wires of real length (two across the street to the east parade at 6.1 and 6.2 m, two to its own side) each sagging about 3 percent of its span and never below 6.1 m; it stands on the west pavement at x 33.0, 0.60 m behind the kerb (the earlier pole at x 12 is dropped), 5 m from both lamp columns; it replaces the 29 September pole's ring and stubs, which the photographs do not show; no period street-pole photograph exists in the feed and the two 2009 and 2011 photographs have no scale, so the height rests on a written range and every other number is judged, checked for consistency only.**

Cloud week 42, unit 13, family 8. Written 13 October 2026, not yet reviewed. `SELF-CHECK telegraph-pole: 73 checks, 73 passed, 0 failed; negative controls 19 of 24 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/telegraph-pole/`: p1 (S1 cropped to the pole's upper part).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | not a car, skip or pallet; plain street furniture |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no CC0 telephone pole exists (S5: electricity poles with crossarms only); so own work by script |
| content rule (canon D18) | what the rule forbids is out of image and text | no notice or person; the data scan finds none of what the rule forbids |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to look at; no NoAI source |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | grey-brown timber, black wires against a grey sky: the street's vertical grain |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the wires vanish; the road-side face of the pole catches the lantern light |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/2630310 | 2026-10-13 | Basher Eyre | CC BY-SA 2.0 (read on the page) | 2011-09-21 | a tall slender creosoted pole on a pavement beside a road of brick houses, tapered, a small cap, a dark bracket box at the top from which about ten wires fan out and down to houses on both sides, and climbing pegs on alternate sides; a car with a number plate on the left (outside the crop) | YES | any measured number (no scale object, the pole's foot is out of frame); the car and its plate; the colours (a bright day) | 2011; the pole is a pre-1990 creosoted pine of the standard kind (they stand for 40 to 60 years) |
| S2 | https://www.geograph.org.uk/photo/1385902 | 2026-10-13 | Basher Eyre | CC BY-SA 2.0 (read on the page) | 2009-06-21 | a pole on the pavement in a terraced street (Percy Road): the pole stands level with the front wall of the terrace, wires leave its top to houses on both sides, the pole's top reaches above the first-floor windows' heads | YES | any number; the white car and its number plate (masked/outside the crop) | 2009; a terraced street of the same period as Quay Street |
| S3 | https://www.geograph.org.uk/photo/2775748 | 2026-10-13 | Basher Eyre | CC BY-SA 2.0 (read on the page) | 2012-01-17 | a pole with a cross-bracket and wires to a cottage's eaves in a village; the wire fans leave one bracket | no | everything (looked at only) | 2012 |
| S4 | https://en.wikipedia.org/wiki/Utility_pole | 2026-10-13 (raw wikitext) | Wikipedia contributors | CC BY-SA 4.0 | n/a (a text) | UK poles typically 8 to 10 m long; marked with the owner, the length and the preservative; creosote was the traditional preservative; the UK sets brackets up the pole as hand and foot holds | YES | any picture, any owner's mark | n/a |
| S5 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | modular_electricity_poles (13119 x 1957 x 7000: a run of poles with crossarms on a wire layout, an electricity kind) and modular_electric_cables (2077 x 215 x 757); no British telephone pole | no | everything: the crossarm electricity poles are not the street's telephone pole and no check of their lettering was needed | n/a |
| S6 | tools/meshgen/blender/clutter/telegraph_pole.py and production/assets/street/clutter/telegraph-pole.glb (this repository); production/specs (the street's stand) | 2026-10-13 | this project | own work | 29 September 2026 | an earlier pole: 8.5 m, 0.24 across at the foot and 0.17 at the top, steps from 2.4 m every 0.45 m, a steel ring with seven 1.6 m stub wires, a number plate; stands at the west kerb, x 12 (terrace-front.py) | YES | its ring and its stubs | n/a |
| S7 | https://api.geograph.org.uk/syndicator.php (terms telegraph pole, telegraph poles, wooden telegraph pole, overhead wires, poles and wires; takenyear 1975 to 1996 and without a year) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | for 1975 to 1996 about 55 photographs with poles in railway and moorland scenes, none a street pole close up; for no year about 300 'Telegraph pole in ...' photographs of 2007 to 2022 of surviving creosoted poles in streets | no | measuring | n/a |

What was searched: Poly Haven's models (modular_electricity_poles and modular_electric_cables: electricity kinds, not used); Geograph's feed for `telegraph pole`, `telegraph poles`, `wooden telegraph pole crossarm insulators`, `overhead wires`, `poles and wires`, `telephone pole` with each year 1980 to 1995 and without a year. Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| tools/meshgen/blender/clutter/telegraph_pole.py and production/assets/street/clutter/telegraph-pole.glb (29 Sep) | an 8.5 m pole with steps, a steel ring and seven stubs | MENDED: the pole, taper and steps are kept (230 and 150 across, steps from 2.4 m every 0.45 m) but the height is 8.0, the ring and stubs are REPLACED by the bracket and the wires | W1, W2, W3 |
| tools/art-recipes/terrace-front.py: the pole placed at the west kerb x 12 | its stand | REPLACED by x 33.0 | the placement reasons |
| Poly Haven modular_electricity_poles, modular_electric_cables | electricity poles with crossarms | NOT USED | S5 |
| git branches (git log --all for telegraph, pole) | the 29 September commit only | none other |  |

## The target

Axes: z up from the pavement at the pole's centre; the bracket faces -y; in the street local +y points across the street. The pole and knobs are cylinders (frustums), the bracket and anchors boxes, the wires polylines of cylinders with the sag as a parabola.

### Assembly in words

- **Pole**: a frustum 230 across at the ground and 150 at 8000, a galvanised cap 45 high (162 across at its foot, 100 at the top).
- **Bracket**: a plate 300 x 22 x 170 on the pole's front just under the top (z 7670 to 7840) with six porcelain knobs 40 across and 46 long in two rows of three at 100 centres and 85 apart.
- **Steps**: eleven galvanised pegs 16 across and 150 out of the pole, on alternate sides from 2400 to 6900 every 450.
- **Wires**: four drop wires 6 across from knobs to wall brackets 80 x 90 x 100 on the facades (the stand-in slabs): two to the east parade 8850 away at 6100 and 6200 high, sag 280 and 270, two to the west block 1400 away at 6500 and 6600, sag 140 and 120.
- **Edges and fixings**: bracket corners r 6; two bolts through the bracket; knob necks r 15; the pole's butt square-cut.

### Parts, variant TP1: TP1: the pole with its bracket, 6 knobs, 11 steps and four drop wires (two across the street, two to its own side) (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| pole | cyl | creosote_timber | -115 to 115 | -115 to 115 | 0 to 8000 |  | creosoted pine pole, 8.0 m above the ground, 230 across at the ground, 150 at the top; the buried 1.6 m is not modelled |
| cap | cyl | galvanised | -81 to 81 | -81 to 81 | 8000 to 8045 |  | galvanised cap, 45 high, 162 across at its foot, shed-roofed |
| bracket | box | iron_dark | -150 to 150 | -105 to -74 | 7670 to 7840 | corners r 6 | distribution bracket 300 x 22 x 170, galvanised iron painted black, two bolts into the pole |
| knob_11 | cyl | porcelain | -120 to -80 | -151 to -105 | 7695 to 7735 |  | porcelain insulator knob 40 across, 46 long |
| knob_12 | cyl | porcelain | -20 to 20 | -151 to -105 | 7695 to 7735 |  | porcelain insulator knob 40 across, 46 long |
| knob_13 | cyl | porcelain | 80 to 120 | -151 to -105 | 7695 to 7735 |  | porcelain insulator knob 40 across, 46 long |
| knob_21 | cyl | porcelain | -120 to -80 | -151 to -105 | 7780 to 7820 |  | porcelain insulator knob 40 across, 46 long |
| knob_22 | cyl | porcelain | -20 to 20 | -151 to -105 | 7780 to 7820 |  | porcelain insulator knob 40 across, 46 long |
| knob_23 | cyl | porcelain | 80 to 120 | -151 to -105 | 7780 to 7820 |  | porcelain insulator knob 40 across, 46 long |
| step_01 | cyl | galvanised | 83 to 233 | -8 to 8 | 2392 to 2408 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_02 | cyl | galvanised | -231 to -81 | -8 to 8 | 2842 to 2858 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_03 | cyl | galvanised | 78 to 228 | -8 to 8 | 3292 to 3308 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_04 | cyl | galvanised | -226 to -76 | -8 to 8 | 3742 to 3758 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_05 | cyl | galvanised | 74 to 224 | -8 to 8 | 4192 to 4208 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_06 | cyl | galvanised | -222 to -72 | -8 to 8 | 4642 to 4658 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_07 | cyl | galvanised | 70 to 220 | -8 to 8 | 5092 to 5108 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_08 | cyl | galvanised | -217 to -67 | -8 to 8 | 5542 to 5558 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_09 | cyl | galvanised | 65 to 215 | -8 to 8 | 5992 to 6008 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_10 | cyl | galvanised | -213 to -63 | -8 to 8 | 6442 to 6458 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| step_11 | cyl | galvanised | 60 to 210 | -8 to 8 | 6892 to 6908 |  | pole step: a 16 mm peg, 150 out of the pole, alternate sides |
| facade_east | box | wall_brick | -9000 to 15000 | 8850 to 9150 | 0 to 9000 |  | the east parade's front (a stand-in slab) |
| facade_west | box | wall_brick | -9000 to 15000 | -1700 to -1400 | 0 to 8500 |  | the west block's front (a stand-in slab) |
| anchor_w1 | box | iron_dark | -3040 to -2960 | 8760 to 8850 | 6050 to 6150 |  | wall bracket 80 x 90 x 100 with an insulator eye, on the eaves course |
| anchor_w2 | box | iron_dark | 2460 to 2540 | 8760 to 8850 | 6150 to 6250 |  | wall bracket 80 x 90 x 100 with an insulator eye, on the eaves course |
| anchor_w3 | box | iron_dark | -4540 to -4460 | -1400 to -1310 | 6450 to 6550 |  | wall bracket 80 x 90 x 100 with an insulator eye, on the eaves course |
| anchor_w4 | box | iron_dark | 3460 to 3540 | -1400 to -1310 | 6550 to 6650 |  | wall bracket 80 x 90 x 100 with an insulator eye, on the eaves course |
| w1 | wire | wire_black | -3002 to 2 | -152 to 8761 | 6097 to 7718 |  | drop wire 6 across, black PVC over copper, across to the east parade |
| w2 | wire | wire_black | 97 to 2503 | -152 to 8761 | 6197 to 7718 |  | drop wire 6 across, black PVC over copper, across to the east parade |
| w3 | wire | wire_black | -4501 to -99 | -1313 to -148 | 6497 to 7803 |  | drop wire 6 across, black PVC over copper, along to the west block, a bay down the street |
| w4 | wire | wire_black | 99 to 3501 | -1312 to -148 | 6597 to 7803 |  | drop wire 6 across, black PVC over copper, to the west block, the other way |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | pole height above the pavement (to the cap's foot) | 8000 mm | Read | Wikipedia 'Utility pole' (read raw 13 Oct): UK poles are typically 8 to 10 m long (a pole's length is marked on it); 8.0 m above the ground is the lowest of that range for a terraced street (error 500) | +-500 |
| N2 | pole diameter at the ground | 230 mm | Judgement | 230 across at the ground and 150 at the top, a stout tapered pine; P2 (Selborne) and P1 (Wilmott Close) both show a visibly tapered pole; error 30 | +-30 |
| N3 | step pitch | 450 mm | Judgement | pole steps every 450 mm on alternate sides from 2.4 m (Wikipedia 'Utility pole': the UK has standard brackets up the pole as hand and foot holds); P1's pegs read about 0.5 m apart; error 60 | +-60 |
| N4 | lowest point of the across wires (at the east parade, their ends) | 6100 mm | Judgement | the wires land on the first-floor eaves brackets of the east parade at 6.1 and 6.2 m (above the 5.5 m a wire must keep over a road: the regulation was not reached on a page this session); error 300 | +-300 |
| N5 | the pole's own height to the bracket's lower edge | 7670 mm | Photo | P1 (Wilmott Close): the bracket (the dark box at the top) lies in the top 8 percent of the pole; error 120 | +-120 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| creosote_timber | creosoted pine, grey-brown, weathered | 92, 78, 62 | 0.85 (rough, checked) | not metal | darker brown-black with tar at the foot (lowest 1.5 m), silvered grey above with vertical checks 100 to 400 long; a dark stain below the bracket where rain runs |
| galvanised | galvanised steel, dull | 128, 130, 128 | 0.55 (matt satin) | metal | steps, cap: white rust, never bright |
| iron_dark | bracket iron, black paint, rusted | 30, 30, 32 | 0.55 (semi-matt) | metal |  |
| porcelain | porcelain knob, brown glaze, dirty | 112, 80, 56 | 0.25 (glazed) | not metal | a brown glaze (period) darkened with soot; cracked glaze at the neck |
| wire_black | drop wire, black sheath | 18, 18, 18 | 0.60 (matt) | not metal | the sheath chalks grey in sun, 6 mm across |
| wall_brick | soot-blackened brick (the street's) | 78, 64, 58 | 0.90 (rough) | not metal | stand-in slabs for the two facades |

### Wear

- the pole: silver-grey weathered above 2 m with vertical checks, dark tar-brown and sticky below 1.5 m, a green-black damp stain at the foot, a pale rub where people lean; nails and staples (old notices, never legible) at 1.4 to 1.8 m; a split along 800 mm near the top
- the steps: white-rust, bent a few degrees; the lowest two missing (a seed): the climbing pegs start at 2.4 m so nobody climbs from the pavement
- the bracket and knobs: rust runs 100 to 300 below the bracket's bolts; bird lime on the cap and the bracket's top face; a cracked knob glaze
- the wires: drooping unevenly (the sag seeds 100 to 300 mm), one slack; bird lime on the lowest span; none touching any wall except at the anchors
- NOT shown: any owner's tag or number plate, any notice with lettering

### Variants the street needs

- TP1 (the sample): the pole with 4 wires (two across, two to its own side). One on the street.
- wear states (materials and seeds): C0 sound; C1 worn (the sample); C2 leaning 2 degrees with one wire slack (a transform seed).
- a pole with two more wires or one fewer is a seed on the wire list: the rule is each wire sags 1.5 to 3.5 percent of its span and keeps 5.5 m over the carriageway.
- NOT written: a crossarm pole (the electricity kind), a stay wire, a transformer pole: none stands in the street.

### Where it stands on Quay Street

**Slot:** west side, pole centre x 33.0 m, z -3.725 (0.60 m behind the kerb's back edge), the bracket facing the street's axis (+z in the street's frame), wires to the east parade (the bays at x 30 to 36) and to the west block; the earlier pole at x 12 west is dropped

- the earlier pole stood at x 12 on the west kerb, beside the poster wall at x 11.4 and 8 m from the lamp column at 18; x 33.0 is 5 m from both the lamp column at 28 east and at 38 west, in the span of the grocer's bay (east x 27 to 39)
- the pole is set back 0.60 m so its 230 mm foot leaves 2.0 - 0.60 - 0.115 = 1.29 m of footway clear (at least 1.0 m)
- its wires cross the street at 6.1 and 6.2 m at the east parade, never lower than 6.1 m: above the lamp columns' 5.0 m mounting height with 1.1 m to spare, and clear of the lamp column at x 28 (the wires land at x 30 and 35.5)
- the wires carry no lettering or mark; the real poles' owner marks are left off (S4 lists them; none is copied)

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the pole's top | the 29 September script: a steel band and ring with seven 1.6 m stub wires fanning from just under the top | S1 and S2: a small capped top, a dark bracket box with insulator knobs, wires leaving from the knobs to the houses; no ring | cap, bracket with six knobs, four full wires to the buildings |
| W2 | the height | the script: 8.5 m | S2: the pole's top reaches above the terrace's first-floor window heads; S4: 8 to 10 m | 8.0 m above the pavement (the buried length not modelled) |
| W3 | the wires | the script: the wires drawn by the street to each house (short stubs only) | S1: about ten wires reach well beyond the pole in a fan across the road | four modelled wires of real length with sag; the street may add more by the same rule (sag 1.5 to 3.5 percent of the span) |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: pole height above the pavement (to the cap's foot) | measure it on the built mesh in millimetres (edge) | 8000 mm | +-500 mm |
| N2: pole diameter at the ground | measure it on the built mesh in millimetres (extent) | 230 mm | +-30 mm |
| N3: step pitch | measure it on the built mesh in millimetres (centre_dx) | 450 mm | +-60 mm |
| N4: lowest point of the across wires (at the east parade, their ends) | measure it on the built mesh in millimetres (wire_min_z) | 6100 mm | +-300 mm |
| N5: the pole's own height to the bracket's lower edge | measure it on the built mesh in millimetres (edge) | 7670 mm | +-120 mm |
| C1: each wire sags 1.5 to 3.5 percent of its span and ends on a knob and an anchor | the polyline's deepest drop below the chord over its length | 1.5 to 3.5 percent | exact |
| C2: the wires over the carriageway stay above 5.5 m | the lowest z of the across wires | >= 5500 | exact |
| C3: no part floats; every wire touches a knob and an anchor | the contact graph | connected | 0 floating |
| C4: no lettering, no plate | textures and text | none | exact |

### For the builder

- pole: a 20-sided tapered cylinder (230 at the ground, 150 at the top), UVs along its length with vertical checks in the height map; the cap and bracket separate meshes; the steps as pegs
- wires: tubes of 6 mm along the polylines in target.json (each point listed), the sag a parabola; hang them as splines in the engine if it prefers; the two ends are on a knob tip and on the wall bracket's face
- the two facades in the file are stand-ins for the street's own walls; the anchors bolt to the eaves course at the stated heights
- no lettering, no plate, no mark

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- no 1975 to 1995 street pole photograph was reached; S1 and S2 are 2009 and 2011 photographs of surviving poles; the pole's foot is out of frame in S1 and no scale object stands beside it in either, so no number is measured on pixels: the height (8.0 m) rests on the Wikipedia range, the rest is Judgement
- the bracket's exact shape (S1 shows a dark box about 8 percent of the pole's height; modelled as a plate with six knobs: Judgement)
- the minimum height of wires over a road (5.5 m is from memory: the regulation was not reached on a page)
- how many wires a real terrace pole carried (S1 shows about ten): four are modelled, more are a seed
- the pole's lean and the buried depth (not modelled)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (each wire's sag as a percent of its span from its own polyline, the clearance over the carriageway, the taper and step pitch from the parts, the foot's footway clearance and the distance to the lamp columns). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
