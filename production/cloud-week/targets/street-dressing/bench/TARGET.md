# Quay Street's council bench: the exact target

**The council bench is 1800 mm long on three timber supports (a flared slab leg 100 mm thick under each end 146 mm in from the slat end, a 50 mm centre leg, a seat bearer and a back post raked 10 degrees), with five iroko seat slats and five back slats each 63 x 32 mm and 23.5 mm apart, bolted with domed coach-bolt heads, the seat 440 high and the back's top at 854; it does not stand on the 2.0 m footway (the scene file says so and the arithmetic agrees: it needs about 2.4 m) but on the quay apron at x -40.0, z 0.0 (the first version's x -9.0 was on the road arm), facing the basin, 78 m from the reverse camera, so small and seen from behind if at all: it serves the player's walk to the quay; no period bench photograph was measurable, so the slat proportions are measured on a 2011 photograph of the back of a council bench against the light and every absolute size is judged (the bench's length sets the scale).**

Cloud week 42, unit 13, family 3. Written 13 October 2026; the fixes the review asked for are applied, not re-reviewed. `SELF-CHECK bench: 109 checks, 109 passed, 0 failed; negative controls 32 of 33 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/bench/`: p1 (S1 cropped) and its target-on-photo overlay.
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | not a car, skip, pallet or kiosk; furniture the street may carry on its quay |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no free model fits (S4: a farmhouse bench, a modern set, a picnic table in 521 Poly Haven models); so own work by script |
| content rule (canon D18) | what the rule forbids is out of image and text | nobody sits on it, no bottle, no plaque; the data scan finds none |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | dark timber, silvered slats and grime; no bright paint |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the bench stands outside the lamp pools |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/2693537 | 2026-10-13 | Chris Downer | CC BY-SA 2.0 (read on the page) | 2011-11-06 | Poole: a long slatted timber bench seen from behind against a bright harbour: five back slats with their gaps shining through, a centre support about 50 mm wide, end uprights about 75 mm, and a broad flared timber leg about 100 mm thick under each end; the RIGHT end shows it 146 mm in from the slat end (the left end is seen obliquely and its leg flares outward at the slat end, about 35 px outside the drawn leg on the 420 px crop); the seat is hidden | YES | any absolute size (no scale object), the leg's depth and curve (a backlit silhouette), the colours | 2011; a council bench pattern of long standing; used for the slat proportions only |
| S2 | https://www.geograph.org.uk/photo/2672444 | 2026-10-13 | Stefan Czapski | CC BY-SA 2.0 (read on the page) | 2011-10-28 | a cast-iron-ended slatted park bench in side view: raked back, seat bearer, legs joined by a floor stretcher, a scrolled arm | no | everything: its cast ends are Victorian ornament (heritage, not a 1990 council bench) and S1 shows a different, timber-legged type, which wins | 2011 heritage park bench |
| S3 | https://www.geograph.org.uk/photo/2029816 | 2026-10-13 | Chris Downer | CC BY-SA 2.0 (read on the page) | 2010-08-20 | benches in a row on a harbour wall: timber slat seat and back on painted cast end frames with arms, bolted to the paving | no | everything (looked at: it supports benches standing on a harbour wall; they are single-seat cast-frame benches, a different type from S1) | 2010 |
| S4 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | painted_wooden_bench (1165 x 497 x 889 mm, a farmhouse bench), modular_street_seating (4340 x 770 x 950, a modern set), wooden_picnic_table (a table with benches) | no | everything: none is a 1990 council bench (painted farmhouse, modern, picnic) | n/a |
| S5 | production/specs/vignette-scene.json (this repository) | 2026-10-13 | this project | own work | n/a | the held bench models (park_bench, garden_bench_01, ornate_bench, curved_stone_bench) are NOT placed: 'a bench belongs on a wide pavement or a quay, and this footway is 2.0 m' | YES | any shape | n/a |
| S6 | https://api.geograph.org.uk/syndicator.php (terms bench, seat, slatted bench, harbour bench, wooden bench, iron bench; takenyear 1975 to 1996 and without a year) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | for 1975 to 1995 only a 1990 white metal garden bench in a village and a 1993 timber bench in a park (looked at: tiny in frame, one with a person); about 250 later photographs, the survey 'bench marks' flooding the results; no period photograph of a council bench near a harbour was measurable | no | measuring | n/a |

What was searched: Geograph's feed for `bench`, `seat`, `slatted bench`, `harbour bench`, `wooden bench`, `iron bench` with each year 1975 to 1996 and without a year (about 250 later photographs; the survey benchmarks of the OS flood every query). Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| production/specs/vignette-scene.json held props: park_bench, garden_bench_01, ornate_bench, curved_stone_bench (not placed) | four held bench models | NOT USED | each is a park, garden or ornate bench; the scene itself says none belongs on the footway |
| production/research/asset-plan 3 (A3 assemblies: bench, cast ends with timber slats; A5: 2 models, 1 to 2 on the quay) | the plan for the bench | KEPT as the brief, its cast ends REPLACED | S1 shows timber slab legs (W3) |
| Poly Haven models painted_wooden_bench, modular_street_seating, wooden_picnic_table | CC0 benches | REJECTED | S4: not a 1990 council bench |
| tools/art-recipes/south-quay (the quay apron) | the apron the bench stands on | READ (build() run on 13 October) and the slot tested against its surfaces by the placement rows; not edited | x -40.0, z 0.0 lies on apron_setts; the first version's x -9.0 was on the road |
| git branches (git log --all for bench) | none | none to reuse |  |

## The target

Axes: x along the bench (the length), y from the sitter's front (-y) to the back (+y), z up from the ground. Boxes, cylinders and one prism per end frame (the raked back post); the self-check measures every number back off the parts.

### Assembly in words

- **Three supports** (left, right, centre): a flared slab leg of timber (the ends 100 thick and centred 146 in from the slat end, the centre one 50 thick), 372 high, its foot flared 20 each end over the lowest 60; a seat bearer 36 deep at z 372 to 408 carrying the slats and the post; a back post raked 10 degrees from z 408 to 860, 40 deep and 75 wide at the ends (flush 25 in from the slat end), 50 wide at the centre; edges r 3 to 6.
- **The seat**: five iroko slats 63 x 32 x 1800 on the bearers, top at 440, gaps 23.5, arrised 2 mm; the front slat 215 in front of the middle.
- **The back**: five iroko slats 63 x 32 x 1800 raked 10 degrees on the front of the three posts, the lowest at z 445, pitch 86.5, the highest top at 854.
- **Fixings**: a domed coach-bolt head (20 across, 7 high) through each back slat at each post (15), square nuts behind; the seat slats are screwed from above with countersunk heads flush (not modelled).
- **B2** is the same bench 1200 long with two supports and no centre frame.

### Parts, variant B1: B1: three-support council bench, 1800 long, 5 + 5 slats (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| end_l_slab | prism | timber_leg | -804 to -704 | -215 to 245 | 0 to 372 | edges r 6, foot flared 20 each end over the lowest 60 | slab leg, 372 high, flared at the foot |
| end_l_bearer | box | timber_leg | -875 to -704 | -225 to 255 | 372 to 408 | edges r 3 | seat bearer, 36 deep, carries the slats and the post |
| end_l_post | prism | timber_leg | -875 to -800 | 205 to 325 | 408 to 860 | edges r 4 | raked back post, 10 degrees, 40 deep, to z 860 |
| end_r_slab | prism | timber_leg | 704 to 804 | -215 to 245 | 0 to 372 | edges r 6, foot flared 20 each end over the lowest 60 | slab leg, 372 high, flared at the foot |
| end_r_bearer | box | timber_leg | 704 to 875 | -225 to 255 | 372 to 408 | edges r 3 | seat bearer, 36 deep, carries the slats and the post |
| end_r_post | prism | timber_leg | 800 to 875 | 205 to 325 | 408 to 860 | edges r 4 | raked back post, 10 degrees, 40 deep, to z 860 |
| mid_slab | prism | timber_leg | -25 to 25 | -215 to 245 | 0 to 372 | edges r 6, foot flared 20 each end over the lowest 60 | slab leg, 372 high, flared at the foot |
| mid_bearer | box | timber_leg | -25 to 25 | -225 to 255 | 372 to 408 | edges r 3 | seat bearer, 36 deep, carries the slats and the post |
| mid_post | prism | timber_leg | -25 to 25 | 205 to 325 | 408 to 860 | edges r 4 | raked back post, 10 degrees, 40 deep, to z 860 |
| seat_slat_1 | box | timber | -900 to 900 | -215 to -152 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_2 | box | timber | -900 to 900 | -128 to -66 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_3 | box | timber | -900 to 900 | -42 to 21 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_4 | box | timber | -900 to 900 | 44 to 108 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_5 | box | timber | -900 to 900 | 131 to 194 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| back_slat_1 | box | timber | -900 to 900 | 180 to 222 | 443 to 510 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_2 | box | timber | -900 to 900 | 195 to 237 | 529 to 597 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_3 | box | timber | -900 to 900 | 210 to 253 | 616 to 683 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_4 | box | timber | -900 to 900 | 225 to 268 | 702 to 770 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_5 | box | timber | -900 to 900 | 241 to 283 | 789 to 856 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| bolt_l1 | cyl | galvanised | -848 to -828 | 178 to 186 | 466 to 486 |  | coach-bolt head, 20 across |
| bolt_r1 | cyl | galvanised | 828 to 848 | 178 to 186 | 466 to 486 |  | coach-bolt head, 20 across |
| bolt_m1 | cyl | galvanised | -10 to 10 | 178 to 186 | 466 to 486 |  | coach-bolt head, 20 across |
| bolt_l2 | cyl | galvanised | -848 to -828 | 193 to 201 | 553 to 573 |  | coach-bolt head, 20 across |
| bolt_r2 | cyl | galvanised | 828 to 848 | 193 to 201 | 553 to 573 |  | coach-bolt head, 20 across |
| bolt_m2 | cyl | galvanised | -10 to 10 | 193 to 201 | 553 to 573 |  | coach-bolt head, 20 across |
| bolt_l3 | cyl | galvanised | -848 to -828 | 208 to 216 | 640 to 660 |  | coach-bolt head, 20 across |
| bolt_r3 | cyl | galvanised | 828 to 848 | 208 to 216 | 640 to 660 |  | coach-bolt head, 20 across |
| bolt_m3 | cyl | galvanised | -10 to 10 | 208 to 216 | 640 to 660 |  | coach-bolt head, 20 across |
| bolt_l4 | cyl | galvanised | -848 to -828 | 223 to 231 | 726 to 746 |  | coach-bolt head, 20 across |
| bolt_r4 | cyl | galvanised | 828 to 848 | 223 to 231 | 726 to 746 |  | coach-bolt head, 20 across |
| bolt_m4 | cyl | galvanised | -10 to 10 | 223 to 231 | 726 to 746 |  | coach-bolt head, 20 across |
| bolt_l5 | cyl | galvanised | -848 to -828 | 239 to 247 | 812 to 832 |  | coach-bolt head, 20 across |
| bolt_r5 | cyl | galvanised | 828 to 848 | 239 to 247 | 812 to 832 |  | coach-bolt head, 20 across |
| bolt_m5 | cyl | galvanised | -10 to 10 | 239 to 247 | 812 to 832 |  | coach-bolt head, 20 across |

### Parts, variant B2: B2: the two-support short bench, 1200 long, same slats and ends (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| end_l_slab | prism | timber_leg | -504 to -404 | -215 to 245 | 0 to 372 | edges r 6, foot flared 20 each end over the lowest 60 | slab leg, 372 high, flared at the foot |
| end_l_bearer | box | timber_leg | -575 to -404 | -225 to 255 | 372 to 408 | edges r 3 | seat bearer, 36 deep, carries the slats and the post |
| end_l_post | prism | timber_leg | -575 to -500 | 205 to 325 | 408 to 860 | edges r 4 | raked back post, 10 degrees, 40 deep, to z 860 |
| end_r_slab | prism | timber_leg | 404 to 504 | -215 to 245 | 0 to 372 | edges r 6, foot flared 20 each end over the lowest 60 | slab leg, 372 high, flared at the foot |
| end_r_bearer | box | timber_leg | 404 to 575 | -225 to 255 | 372 to 408 | edges r 3 | seat bearer, 36 deep, carries the slats and the post |
| end_r_post | prism | timber_leg | 500 to 575 | 205 to 325 | 408 to 860 | edges r 4 | raked back post, 10 degrees, 40 deep, to z 860 |
| seat_slat_1 | box | timber | -600 to 600 | -215 to -152 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_2 | box | timber | -600 to 600 | -128 to -66 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_3 | box | timber | -600 to 600 | -42 to 21 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_4 | box | timber | -600 to 600 | 44 to 108 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| seat_slat_5 | box | timber | -600 to 600 | 131 to 194 | 408 to 440 | arrised 2 mm all round, ends square | iroko 63 x 32 |
| back_slat_1 | box | timber | -600 to 600 | 180 to 222 | 443 to 510 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_2 | box | timber | -600 to 600 | 195 to 237 | 529 to 597 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_3 | box | timber | -600 to 600 | 210 to 253 | 616 to 683 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_4 | box | timber | -600 to 600 | 225 to 268 | 702 to 770 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| back_slat_5 | box | timber | -600 to 600 | 241 to 283 | 789 to 856 | arrised 2 mm all round | iroko 63 x 32, raked 10 degrees with the posts |
| bolt_l1 | cyl | galvanised | -548 to -528 | 178 to 186 | 466 to 486 |  | coach-bolt head, 20 across |
| bolt_r1 | cyl | galvanised | 528 to 548 | 178 to 186 | 466 to 486 |  | coach-bolt head, 20 across |
| bolt_l2 | cyl | galvanised | -548 to -528 | 193 to 201 | 553 to 573 |  | coach-bolt head, 20 across |
| bolt_r2 | cyl | galvanised | 528 to 548 | 193 to 201 | 553 to 573 |  | coach-bolt head, 20 across |
| bolt_l3 | cyl | galvanised | -548 to -528 | 208 to 216 | 640 to 660 |  | coach-bolt head, 20 across |
| bolt_r3 | cyl | galvanised | 528 to 548 | 208 to 216 | 640 to 660 |  | coach-bolt head, 20 across |
| bolt_l4 | cyl | galvanised | -548 to -528 | 223 to 231 | 726 to 746 |  | coach-bolt head, 20 across |
| bolt_r4 | cyl | galvanised | 528 to 548 | 223 to 231 | 726 to 746 |  | coach-bolt head, 20 across |
| bolt_l5 | cyl | galvanised | -548 to -528 | 239 to 247 | 812 to 832 |  | coach-bolt head, 20 across |
| bolt_r5 | cyl | galvanised | 528 to 548 | 239 to 247 | 812 to 832 |  | coach-bolt head, 20 across |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | bench length (slat length) | 1800 mm | Judgement | a three-seat council bench; it also fixes P1's scale: P1's overall width 356.6 px = 1800 mm gives 0.198 px per mm; error 20 mm | +-20 |
| N2 | seat height (top of the seat slats) | 440 mm | Judgement | 440 mm, the usual public-seat height; the seat is hidden behind the back on P1; error 30 | +-30 |
| N3 | slat width (the seat slat's depth) | 63 mm | Photo | P1 slat height 12.4 px (pitch 17.0 px less gap 4.6 px) at 0.198 px per mm = 63 mm; error 5 | +-5 |
| N4 | slat pitch on the back (centre to centre) | 86.5 mm | Photo | P1 gap tops at 197.7, 214.8, 232.4, 248.6: mean pitch 17.0 px = 86 mm; error 4 | +-4 |
| N5 | slat thickness | 32 mm | Judgement | 32 mm iroko, the usual section; not visible on P1; error 4 | +-4 |
| N6 | top of the highest back slat above the ground | 854 mm | Judgement | five slats from 445 up (the bench's back top is not measurable against the ground on P1); error 40 | +-40 |
| N7 | back post top above the ground | 860 mm | Judgement | 860 mm: the post stands a little above the highest slat; P1 is a back view; error 40 | +-40 |
| N9 | the end legs' centre line in from the slat end | 146 mm | Judgement | P1's right end shows 146 mm (the leg's centre 29 px in at 0.198 px per mm); the left end is seen obliquely and its leg flares about 35 px further out, so the inset rests on the right end alone: Judgement, error 60 | +-60 |
| N8 | centre support thickness along the bench | 50 mm | Photo | P1 mid_left 325.4 to mid_right 335.3 (9.9 px) at 0.198 px per mm = 50 mm; error 10 | +-10 |

### Photograph measurements (P1, S1)

each edge is the strongest grey-level step of the stated sign inside the recorded window, averaged over the recorded band; the scale is fitted on the one span from the back's top edge to the fourth slat's lower edge (62.4 px); the bench is seen from behind against the light (the sea is bright behind it, the gaps between the slats shine through) so the dark slats and the bright gaps give sharp edges; the width (356.6 px) is the unit that gives 0.198 px per mm if the bench is 1800 long (Judgement); the photograph's centre bar is 6 px right of the bench's centre (the camera is a little to the right), so the mid features carry 8 px; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (25 mm).

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P1 | back_top | y | 186.2 | [200, 176, 300, 192] | 5.0 | hi of back_slat_5 |
| P1 | gap1_top | y | 197.7 | [200, 194, 290, 206] | 5.0 | lo of back_slat_5 |
| P1 | gap1_bottom | y | 202.2 | [200, 198, 290, 212] | 5.0 | hi of back_slat_4 |
| P1 | gap2_top | y | 214.8 | [200, 210, 290, 222] | 5.0 | lo of back_slat_4 |
| P1 | gap2_bottom | y | 220.2 | [200, 216, 290, 228] | 5.0 | hi of back_slat_3 |
| P1 | gap3_top | y | 232.4 | [200, 226, 290, 238] | 5.0 | lo of back_slat_3 |
| P1 | gap3_bottom | y | 236.6 | [200, 232, 290, 244] | 5.2 | hi of back_slat_2 |
| P1 | gap4_top | y | 248.6 | [200, 242, 290, 254] | 6.1 | lo of back_slat_2 |
| P1 | gap4_bottom | y | 252.8 | [200, 246, 290, 258] | 6.7 | hi of back_slat_1 |
| P1 | left_end | x | 145.7 | [140, 186, 160, 196] | 7.0 | hi of back_slat_5 |
| P1 | mid_left | x | 325.4 | [316, 217, 334, 221] | 8.0 | hi of mid_post |
| P1 | mid_right | x | 335.3 | [328, 217, 346, 221] | 8.0 | lo of mid_post |
| P1 | right_end | x | 502.3 | [494, 186, 516, 196] | 7.0 | lo of back_slat_5 |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| timber | iroko slats, weathered | 122, 98, 70 | 0.80 (rough, grained) | not metal | silvering on the top faces, dark at the bolt holes, a green algal stain on the back slats' lower edges |
| timber_leg | iroko legs and posts, stained dark | 74, 58, 42 | 0.80 (rough, grained) | not metal | dark with water and ground dirt, lightest at the arrised edges; a green stain at the foot |
| galvanised | galvanised bolt heads | 138, 140, 138 | 0.50 (satin) | metal | domed heads, rust rings |

### Wear

- the iroko is silvered on its top faces and weathered grey-brown on the back slats, with a darker band along each slat's lower edge where water sits; end grain checked and darker, one slat split 300 mm from an end
- the legs and posts are dark with water and ground dirt, green-stained over the lowest 120 mm, the arrised edges lighter; rust rings 20 to 40 mm round the bolt heads and short rust streaks below them
- dirt: a pale bird-lime splash on the top of the back and two on the seat; moss in the joint between end frame and slat; none of anyone's belongings
- carved or scratched marks on the back slats' upper edge (a few initials, never a word that is a name or a firm)
- NOT shown: a person, a bottle or can, any advertisement plate (a bench was often given in memory: no plaque)

### Variants the street needs

- B1 (the sample): three supports, 5 + 5 slats, no arms; one on the quay apron (x -40.0, z 0.0).
- B2: a short bench, 1200 long, two supports, the same slats and ends (a second bench or the south quay's other end; not placed today).
- conditions (materials): C0 sound; C1 worn (the sample's wear); C2 one back slat missing at the right end (a gap 63 mm, a seed).
- colours: the iroko is left unpainted; a repainted bench is a seed (council green on the legs and posts, 40 percent), the slats stay bare.

### Where it stands on Quay Street

**Slot:** the quay apron, the bench's centre at x -40.0 m, z 0.0 m (on the street's axis), the sitter facing -x (south-west over the Old Basin, which lies beyond the cope at x -69.4), the back to the street; one bench. (The first version stood it at x -9.0, z 2.5: that point is on the road arm of Quay Street, 0.5 m inside the east kerb; the apron's setts begin at about x -33.1.)

- the scene file keeps benches off the street: 'a bench belongs on a wide pavement or a quay, and this footway is 2.0 m' (S5); a bench needs its 550 mm of depth plus 900 mm of leg room in front and 1000 mm of clear way behind it, about 2.4 m, against a 2.0 m footway
- the asset plan lists benches 'on the quay' (1 to 2). The apron was read from tools/art-recipes/south-quay/south_quay_geom.py (build(), 13 October): Quay Street runs on south of x 0 as its own 6 m carriageway (road_quay_street_south, x -2.0 to -21.2) to the junction, whose south kerb is at about x -33.0; the apron's setts (apron_setts, level 0.05 m above the crown) begin at about x -33.1 and run to the cope at x -69.4. The first version's point (-9.0, 2.5) lies on the road arm, 0.5 m inside the east kerb face, and its far end on footway_northeast_corner; the row that said 'it stands south' (x below 0) could not tell the apron from the road
- x -40.0, z 0.0: the footprint (600 x 1800) and 1.0 m round it lie only on apron_setts, 6.9 m from its edge at the junction's south kerb, 29.4 m from the cope, clear of the quay's fish boxes, rings and bollards (all beyond x -64); the sitter faces -x, over the basin
- the bench is far from both pictures: it is 78 m from the reverse camera (cam_reverse, x 38, z 1.6) and 37 m from the hook camera (x -3, z -1.6), small and seen from behind or from the side, if at all; it is not put there to be seen in the morning pictures but for the player who walks down to the quay
- clear of the quay's bollards (the bollards target stands them at the quay edge and the corners, 30 m away)

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | where benches stand | the asset plan: benches 1 to 2 on the quay; the scene file's held benches are named for a street | n/a (a placement fact) | the quay apron only; never the 2.0 m footway |
| W2 | the slat's size | none (the usual 70 x 32 iroko) | P1: the slat reads 63 mm (12.4 px at 0.198 px per mm, the scale from an assumed 1800 length) | 63 x 32, gap 23.5, pitch 86.5 (Photo within 5 mm of the assumption) |
| W3 | the ends | the asset plan: cast ends with timber slats; S2 and S3 show cast-iron ends | S1: the end support is a broad flared timber leg about 100 mm thick (20 px at 0.198 px per mm), 146 mm in from the slat end on the right end ONLY (the left end is seen obliquely and its leg lies about 35 px further out), with a 75 mm upright at the end | timber slab legs 100 thick, flared at the foot, a bearer, a 75 wide raked post; the inset 146 mm is a Judgement of plus or minus 60 resting on the right end alone; no cast iron (the photograph wins over the plan) |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: bench length (slat length) | measure it on the built mesh in millimetres (bbox) | 1800.0 mm | +-20.0 mm |
| N2: seat height (top of the seat slats) | measure it on the built mesh in millimetres (edge) | 440.0 mm | +-30.0 mm |
| N3: slat width (the seat slat's depth) | measure it on the built mesh in millimetres (extent) | 63.0 mm | +-5.0 mm |
| N4: slat pitch on the back (centre to centre) | measure it on the built mesh in millimetres (centre_dx) | 86.5 mm | +-4.0 mm |
| N5: slat thickness | measure it on the built mesh in millimetres (extent) | 32.0 mm | +-4.0 mm |
| N6: top of the highest back slat above the ground | measure it on the built mesh in millimetres (edge) | 854.0 mm | +-40.0 mm |
| N7: back post top above the ground | measure it on the built mesh in millimetres (edge) | 860.0 mm | +-40.0 mm |
| N9: the end legs' centre line in from the slat end | measure it on the built mesh in millimetres (edge_to_centre) | 146.0 mm | +-60.0 mm |
| N8: centre support thickness along the bench | measure it on the built mesh in millimetres (extent) | 50.0 mm | +-10.0 mm |
| C1: five seat slats and five back slats, equal gaps | count the slats and measure each gap | 5 + 5; gap 23.5 mm | +-3 mm |
| C2: three identical end frames | compare the three frames' parts | identical | exact |
| C3: no part floats and every join meets | the contact graph of the meshes | all parts reach the ground | 0 floating |
| C4: the bolts sit on the back slats' front faces | each bolt head against its slat | head proud 7 mm | +-3 mm |
| C5: no plaque, no lettering | the model's text | none | exact |

### For the builder

- supports: each is a flared slab leg (prism in the y-z plane, points in the parts table, 100 thick; the centre one 50), a bearer and a raked post (end 75 wide, centre 50); build the two end supports identical, mirrored
- slats: 1800 long, arrised 2 mm; the back slats are rotated 10 degrees about the bench's length axis with the posts; the bolt heads on the back's face at each post, 20 across and 7 high, domed
- the seat slats sit on the bearers (z 408); the slats' underside is the bearer's top
- orientation: the local -y is the way the sitter faces; in the street's frame -y points -x (south-west, towards the basin): the pose is x -40.0, z 0.0, yaw -90 (the bench's length then runs along the street's z)

## Owed to Jafar's page (one line each, with a recommendation)

None.

## Handovers (for the town or the scene's owner, not for his page)

- H1: For the town: hook-cast.json places.quay (x -5.0, z 0.0, 'the quay apron at the street's south end') lies on the road arm (road_quay_street_south spans x -21.2 to -2.0 and the apron's setts begin at about x -33.1), not on the apron; move the place onto the apron (the bench's slot, x -40.0, z 0.0, is on it) or say it is the road's end, and re-check the routines that use it.

## What the target could not settle

- absolute sizes: S1 has no scale object; the 1800 length is Judgement (it sets the slat width at 63 mm); seat height 440, back height 854 and the 10 degree rake are Judgement
- the end frames' exact shape (S1's ends are in silhouette; S2 is ornate; S3 is a plain pedestal type): the plain straight-legged end is a Judgement from S2's construction and S3's plainness
- the apron's extents were read on 13 October from south_quay_geom.build() (setts from x -33.1 to the cope at x -69.4); the town's own quay place (hook-cast.json places.quay, x -5.0, z 0.0) lies on the road arm, not the apron: handover H1
- whether the street had any bench in 1990 (the scene says none on the footway); one on the quay is the asset plan's count

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the bench's depth against the footway (the arithmetic that keeps it off the 2.0 m footway), the pose against the south quay kit's surfaces (the footprint and 1 m round it on the apron's setts, no road or footway, nothing of the quay's furniture within 1 m, 3 m from the cope), the distance to the reverse camera, the slat counts and gaps, the three frames identical, the bolts on the back slats, the legs' inset). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
