# Quay Street's pallets: the exact target

**The pallets are the plain softwood stringer pallet, 1000 x 1200 x 144 mm (seven 85 x 22 top boards 67.5 apart, three 95 x 100 stringers, three 100 x 22 bottom boards), unmarked: the sample is one leaning 12 degrees on the gable wall of the west block in the yard mouth with one flat at its foot (variants: one flat, two stacked), which replaces the flat slab the 2 October ruling took off the street; the board proportion is measured on a 2011 photograph of a leaning pallet (width over pitch 0.545, spread 0.06) because no period pallet photograph exists in the feed; the size is the European standard, not measured.**

Cloud week 42, unit 13, family 5. Written 13 October 2026, not yet reviewed. `SELF-CHECK pallets: 75 checks, 73 passed, 2 failed; negative controls 0 of 0 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/pallets/`: p1 (S1 cropped to the leaning pallets).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | 'skip and pallets off until real': this target is the pallet made real (a form from a photograph, no mark), to go back into the scene only after the gate |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no CC0 pallet exists (S4); so own work by script |
| content rule (canon D18) | what the rule forbids is out of image and text | no person, no drink, no betting; the data scan finds none of what the rule forbids |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 and S2 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | weathered grey-brown timber and grime |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the pallets read as pale slats and black gaps |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/2660949 | 2026-10-13 | Brian Robert Marshall | CC BY-SA 2.0 (read on the page) | 2011-10-20 | three timber pallets standing on their long edges against a wall beside a doorway on a paved pavement, one leaning about 12 degrees with seven deck boards seen from the front and three cross members (stringers) between; beside them a stack of plastic fish boxes carrying real firms' names | YES | any absolute size (no scale object); the fish boxes and their lettering (masked); the plastic crates | 2011; a softwood stringer pallet is the same object in 1990 |
| S2 | https://www.geograph.org.uk/photo/3572620 | 2026-10-13 | Jonathan Billinger | CC BY-SA 2.0 (read on the page) | 2013-07-21 | heaps of old pallets in an outhouse yard: the edges of stacked pallets show a bottom board, stringer blocks and a top board; boards split and grey | YES | any number | 2013, old pallets of the 1980s and 1990s kind |
| S3 | https://en.wikipedia.org/wiki/Pallet | 2026-10-13 (raw wikitext) | Wikipedia contributors | CC BY-SA 4.0 | n/a (a text) | stringer pallets (three or more stringers, deck boards on top); the pallet measurement convention (first number the stringer length, second the deckboard length); the European sizes EUR 1 800 x 1200 x 144, EUR 2 1200 x 1000 x 144, EUR 3 1000 x 1200 x 144 | YES | any picture | n/a |
| S4 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | no pallet; wooden_crate_01, wooden_crate_02 and wooden_military_crate (crates, not pallets) | no | everything: no CC0 pallet exists, so it is made by script | n/a |
| S5 | production/specs/vignette-scene.json (this repository) | 2026-10-13 | this project | own work | n/a | the held pallet (stood at x 21.8 west, off since 2 October: 'it read as a slab at the yard mouth'), large_pallet 2.00 x 1.10 m and small_pallet (neither placed) | YES | any shape | n/a |
| S6 | https://api.geograph.org.uk/syndicator.php (terms pallets, wooden pallets, stack of pallets, pallets yard; takenyear 1980 to 1995 and without a year) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1980 to 1995 searched | for 1980 to 1995 one photograph (a 1977 feed hit that is not a pallet photograph); about 250 photographs from 2006 on; no period pallet photograph | no | measuring | n/a |

What was searched: Poly Haven's model list (no pallet); Geograph's feed for `pallets`, `wooden pallets`, `stack of pallets`, `pallets yard` with years 1980 to 1995 and without a year (none before 2006 measurable). Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| vignette-scene.json: held pallet (off since 2 Oct), large_pallet 2.00 x 1.10, small_pallet | slab-like stand-ins | REPLACED | W1 |
| Poly Haven models | no pallet; wooden crates only | NOT USED | S4 |
| production/research/period-vehicles-and-props NOTE.md (pallet 1,200 x 1,000) | the size | KEPT as a Read number (S3 confirms it) | oriented 1000 x 1200 after S1 |
| git branches (git log --all for pallet) | none | none to reuse |  |

## The target

Axes: x along the stringers (1000), y along the deck boards (1200), z up; the stringers sit on the bottom boards and carry the top boards. Boxes; the leaning pallet is the same parts with one transform (a roll of 78 degrees about x and a lift of 586.9 mm).

### Assembly in words

- **Top deck**: seven boards 85 wide, 22 thick, 1200 long, at a 152.5 pitch across 1000 (gaps 67.5), arrised 1 mm, the underside of each end chamfered 15 x 15.
- **Stringers**: three, 95 wide, 100 high, 1000 long, along x: one flush with each board end and one in the middle (P1's middle member sits at the middle of the board length).
- **Bottom deck**: three boards 100 x 22 x 1200 under the stringers' crossings, at the two edges and the middle.
- **Fixings**: two ring-shank nails through each board into each stringer (not modelled: texture and decals); nail heads 6 mm.
- **PA3**: the leaning pallet rests on its lower edge on the ground and on the gable wall at its upper edge (12 degrees from the vertical); the flat pallet lies in front of its foot, touching it.

### Parts, variant PA1: PA1: one pallet, flat (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| p1_top1 | box | pallet_wood | -500 to -415 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top2 | box | pallet_wood | -348 to -262 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top3 | box | pallet_wood | -195 to -110 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top4 | box | pallet_wood | -42 to 42 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top5 | box | pallet_wood | 110 to 195 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top6 | box | pallet_wood | 262 to 348 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top7 | box | pallet_wood | 415 to 500 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_str1 | box | pallet_wood | -500 to 500 | -600 to -505 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str2 | box | pallet_wood | -500 to 500 | -48 to 48 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str3 | box | pallet_wood | -500 to 500 | 505 to 600 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_bot1 | box | pallet_wood | -500 to -400 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot2 | box | pallet_wood | -50 to 50 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot3 | box | pallet_wood | 400 to 500 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |

### Parts, variant PA2: PA2: two pallets stacked flat (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| p1_top1 | box | pallet_wood | -500 to -415 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top2 | box | pallet_wood | -348 to -262 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top3 | box | pallet_wood | -195 to -110 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top4 | box | pallet_wood | -42 to 42 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top5 | box | pallet_wood | 110 to 195 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top6 | box | pallet_wood | 262 to 348 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top7 | box | pallet_wood | 415 to 500 | -600 to 600 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_str1 | box | pallet_wood | -500 to 500 | -600 to -505 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str2 | box | pallet_wood | -500 to 500 | -48 to 48 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str3 | box | pallet_wood | -500 to 500 | 505 to 600 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_bot1 | box | pallet_wood | -500 to -400 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot2 | box | pallet_wood | -50 to 50 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot3 | box | pallet_wood | 400 to 500 | -600 to 600 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_top1 | box | pallet_wood | -500 to -415 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top2 | box | pallet_wood | -348 to -262 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top3 | box | pallet_wood | -195 to -110 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top4 | box | pallet_wood | -42 to 42 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top5 | box | pallet_wood | 110 to 195 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top6 | box | pallet_wood | 262 to 348 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top7 | box | pallet_wood | 415 to 500 | -600 to 600 | 266 to 288 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_str1 | box | pallet_wood | -500 to 500 | -600 to -505 | 166 to 266 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_str2 | box | pallet_wood | -500 to 500 | -48 to 48 | 166 to 266 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_str3 | box | pallet_wood | -500 to 500 | 505 to 600 | 166 to 266 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_bot1 | box | pallet_wood | -500 to -400 | -600 to 600 | 144 to 166 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_bot2 | box | pallet_wood | -50 to 50 | -600 to 600 | 144 to 166 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_bot3 | box | pallet_wood | 400 to 500 | -600 to 600 | 144 to 166 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |

### Parts, variant PA3: PA3: one flat at the foot and one leaning 12 degrees on the gable wall (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| p1_top1 | box | pallet_wood | -500 to -415 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top2 | box | pallet_wood | -348 to -262 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top3 | box | pallet_wood | -195 to -110 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top4 | box | pallet_wood | -42 to 42 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top5 | box | pallet_wood | 110 to 195 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top6 | box | pallet_wood | 262 to 348 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_top7 | box | pallet_wood | 415 to 500 | -1465 to -265 | 122 to 144 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p1_str1 | box | pallet_wood | -500 to 500 | -1465 to -1370 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str2 | box | pallet_wood | -500 to 500 | -912 to -818 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_str3 | box | pallet_wood | -500 to 500 | -360 to -265 | 22 to 122 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p1_bot1 | box | pallet_wood | -500 to -400 | -1465 to -265 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot2 | box | pallet_wood | -50 to 50 | -1465 to -265 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p1_bot3 | box | pallet_wood | 400 to 500 | -1465 to -265 | 0 to 22 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_top1 | box | pallet_wood | -500 to -415 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top2 | box | pallet_wood | -348 to -262 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top3 | box | pallet_wood | -195 to -110 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top4 | box | pallet_wood | -42 to 42 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top5 | box | pallet_wood | 110 to 195 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top6 | box | pallet_wood | 262 to 348 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_top7 | box | pallet_wood | 415 to 500 | -266 to 5 | 25 to 1204 | arrised 1 mm, ends chamfered 15 x 15 on the underside | top deck board 85 x 22 x 1200, softwood |
| p2_str1 | box | pallet_wood | -500 to 500 | -244 to -127 | 5 to 118 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_str2 | box | pallet_wood | -500 to 500 | -129 to -12 | 545 to 659 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_str3 | box | pallet_wood | -500 to 500 | -14 to 103 | 1085 to 1199 | arrised 1 mm | stringer 95 x 100 x 1000, softwood |
| p2_bot1 | box | pallet_wood | -500 to -400 | -146 to 125 | 0 to 1178 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_bot2 | box | pallet_wood | -50 to 50 | -146 to 125 | 0 to 1178 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| p2_bot3 | box | pallet_wood | 400 to 500 | -146 to 125 | 0 to 1178 | arrised 1 mm, ends chamfered | bottom board 100 x 22 x 1200 |
| wall_gable | box | wall_brick | -1500 to 1500 | 125 to 325 | 0 to 2600 |  | the gable end of the west block (a stand-in slab; the building is the street's) |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | stringer length (the pallet's width) | 1000 mm | Read | Wikipedia 'Pallet' (read raw, 13 Oct): the standard European sizes 1200 x 1000 (EUR 2) and 1000 x 1200 (EUR 3) and their 144 mm height; P1's pallet is the 1000 x 1200 kind (boards 1200, stringers 1000: the board length is 1.2 times the width in the photograph) | +-1 |
| N2 | deck board length | 1200 mm | Read | same | +-1 |
| N3 | overall height | 144 mm | Read | same: 144 mm = 22 + 100 + 22 | +-0.5 |
| N4 | top board width | 85 mm | Photo | P1 board width over pitch 0.545 mean (0.59, 0.53, 0.53, 0.53 over five boards: the near boards are nearer the camera) at the 152.5 pitch that 7 boards on 1000 give: 83 mm; 85 chosen (+-6) | +-6 |
| N5 | top board pitch | 152.5 mm | Derived | 7 boards of 85 across 1000 leave 6 gaps of 67.5; pitch 152.5 | +-1 |
| N6 | stringer section height | 100 mm | Read | EUR pallet: boards 22 each, stringers 100 (the 144 total) | +-1 |
| N7 | the middle stringer's centre from the pallet's centre | 0 mm | Photo | P1: the middle cross member of the leaning pallet sits at 345 to 390 px of a 345 px board length: its centre at 0.49 of the board length (+-0.03) | +-12 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| pallet_wood | softwood pallet timber, grey-brown, weathered | 150, 124, 92 | 0.85 (rough, fibrous) | not metal | new boards pale (190, 165, 120) at the ends, weathered grey-brown (130, 112, 90) on the faces; nail heads rust-stained; NO printed mark, no stamp, no brand (a real pallet carries IPPC and owner marks: left off) |
| wall_brick | soot-blackened brick (the street's) | 78, 64, 58 | 0.90 (rough) | not metal | a stand-in for the gable wall |

### Wear

- boards: weathered grey-brown on the faces, paler at freshly broken or sawn ends; one board split along 400 mm; one board missing on the flat pallet's top deck (a gap of 85 mm: a seed), edges rounded by use and grey with grime on the underside
- nail heads (not modelled) rust-stained with a 15 mm brown halo; a few sawn-off nail stubs standing 3 mm proud
- damp green stain along the lowest 120 mm of the leaning pallet and on the flat pallet's bottom boards; wet-street darkening on everything below 150 mm
- NOT shown: any owner's brand, any stamp, any hire company's colour (a real pallet carries marks; this one is plain)

### Variants the street needs

- PA3 (the sample): one flat, one leaning on the gable wall.
- PA1: a single flat pallet (for the loading aprons and the chandler's).
- PA2: two stacked flat pallets.
- conditions (materials and seeds): C0 new and pale (a few), C1 weathered (the sample), C2 one board broken and one missing. A leaning pallet's lean is 10 to 14 degrees by seed.

### Where it stands on Quay Street

**Slot:** west side, in the yard mouth (x 21 to 24), behind the crowd-control barrier the scene puts across it: the leaning pallet against the gable end of the west_south block (its wall face at x 21.0, facing +x), centred at z -6.2; one pallet flat on the yard floor in front of its foot (street x 21.13 to 22.33)

- the scene's story is that the yard is shut (a barrier across the mouth, cones, a skip): the pallets behind the barrier are the yard's stuff, one event with the skip; the 2 October ruling took the pallet off the street until real, and this target is the 'real' (RULINGS 2 Oct): a decision for DECISIONS, not a question
- the earlier slot (x 21.8 on the west pavement, a flat slab) is dropped: a flat pallet on the footway read as a slab; leaning on a wall it reads as a pallet (S1)
- the scene's two wooden crates stand on the pavement at z -4.3 (far edges at -4.76), the pallets inside the yard from z -5.7: 0.94 m clear; the self-check reads the crates' places from the scene and measures the clearance
- the scene's large_pallet (2.00 x 1.10) is not a British pallet and is not used

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the pallet's size and form | the scene file's held large_pallet 2.00 x 1.10 m and small_pallet (a slab) | S1: a 1000 x 1200 stringer pallet with seven boards, three stringers (a middle one at the middle of the boards), the usual look | 1000 x 1200 x 144, 7 top boards of 85, 3 stringers, 3 bottom boards |
| W2 | where it stands | the scene: flat on the west pavement at x 21.8 | S1: leaning on a wall beside a door | leaning on the gable wall in the yard mouth, one flat at its foot |
| W3 | block or stringer | the asset plan's pallet 1,200 x 1,000 | S2 shows both stringer pallets and some with block feet; S1's is a stringer pallet | stringer pallet; a block-footed pallet is not written |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: stringer length (the pallet's width) | measure it on the built mesh in millimetres (bbox) | 1000.0 mm | +-1.0 mm |
| N2: deck board length | measure it on the built mesh in millimetres (extent) | 1200.0 mm | +-1.0 mm |
| N3: overall height | measure it on the built mesh in millimetres (bbox) | 144.0 mm | +-0.5 mm |
| N4: top board width | measure it on the built mesh in millimetres (extent) | 85.0 mm | +-6.0 mm |
| N5: top board pitch | measure it on the built mesh in millimetres (centre_dx) | 152.5 mm | +-1.0 mm |
| N6: stringer section height | measure it on the built mesh in millimetres (extent) | 100.0 mm | +-1.0 mm |
| N7: the middle stringer's centre from the pallet's centre | measure it on the built mesh in millimetres (centre) | 0.0 mm | +-12.0 mm |
| C1: seven top boards, three stringers, three bottom boards | count them | 7, 3, 3 | exact |
| C2: board width over pitch matches P1 | top board width / pitch | 0.557 | +-0.06 of the photograph's 0.545 |
| C3: the leaning pallet rests on the ground and touches the wall | the contact graph | connected | 0 floating |
| C4: no mark on any board | textures and text | none | exact |

### For the builder

- one mesh per pallet by script: 7 + 3 boards and 3 stringers, boards arrised 1 mm, ends chamfered 15 on the underside; the nails are texture
- the leaning pallet is the flat one rotated 78 degrees about its stringer axis (x) with its lowest edge on the ground; the transform is in the part xf of target.json
- the gable wall in PA3 is a stand-in: the street's own wall carries the contact
- no mark of any kind on any board

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- absolute size: S1 has no scale object, so the 1000 x 1200 x 144 is the European standard (Read), supported by S1's proportions (board length to width of the pallet 1.2), not measured
- the board width (85 mm, error 6) comes from a ratio on a perspective view
- whether pallets of 1990 were mostly hire pallets with owners' marks (they were; the target leaves every mark off)
- the exact yard-mouth clearance: it depends on the crates' places at x 22.4 and 23.1 and the barrier at 22.5, which the scene owns

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the board width over pitch against P1's measured edges, the board and stringer counts, the pallet's size against the standard, the lean from the transform, the contact with the wall and the ground, the pallet inside the yard mouth against the scene's barrier). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
