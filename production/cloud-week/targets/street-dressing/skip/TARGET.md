# Quay Street's skip: the exact target

**The skip is a 6-yard builder's skip with the hexagonal side profile of the photograph (3015 mm long at its widest line 793 up, 1850 along the floor, 2320 along the top, 1200 high, 1700 wide), 5 mm plates, an 86 mm folded top rim, a stiffening rib at 923, four chain lugs, two amber lamps lit in the lantern colour at night, two red-and-yellow striped marking plates on each end (the plates the Builders' Skips (Markings) Regulations 1984 required from 1 January 1986: 270 x 380 mm, stripes at 45 degrees and 140 mm broad) and the invented stencil of a placeholder hire firm and a British telephone number, yellow; it stands in the west carriageway before the yard mouth at x 22.5, 0.30 m off the kerb on the road's camber, which puts the 2 October ruling's skip back as a real skip (owed: one line); the scene's two cones stay where they are (on the west footway; the first version's move of them was a misreading); the profile is measured on a 2021 side view (turned 7.2 degrees to level it) and the scale is the assumed height of 1.2 m, so the lengths are judged; no period skip photograph exists in the feed.**

Cloud week 42, unit 13, family 6. Written 13 October 2026, not yet reviewed. `SELF-CHECK skip: 126 checks, 126 passed, 0 failed; negative controls 0 of 0 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/skip/`: p1 (S1 turned and cropped, the firm's name painted out), its target-on-photo overlay, and s8 (Schedule 1 of the 1984 Regulations: the marking plate diagram).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | 'skip and pallets off until real': this target is the skip made real; it goes back to the street only after the gate, and the owed line asks for the yes |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no CC0 skip exists (S5); so own work by script from S1's profile |
| content rule (canon D18) | what the rule forbids is out of image and text | no person, no drink container; an invented firm and number; the data scan finds none of what the rule forbids |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | yellow paint, grime, dents and mud: a saturated patch in a grey street |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; its two amber lamps are the only lit things on it |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/6875634 | 2026-10-13 | Ian Taylor | CC BY-SA 2.0 (read on the page) | 2021-06-15 | a yellow builder's skip standing tilted on a grass slope, seen from its long side: the hexagonal side profile (two stacked trapezia, widest at about two thirds up), a folded top rim, a stiffening rib below it, two lifting lugs near the top, a stencilled firm's name and telephone number; behind it a temporary fence panel; two walkers and a dog on the left (outside the crop) | YES | absolute size (no scale object; the height 1200 is assumed), the firm's name and number (painted out), the people, the fence | 2021; the builder's skip's shape has not changed since the 1960s (cantilever-lorry skips) |
| S2 | https://www.geograph.org.uk/photo/1144136 | 2026-10-13 | Rossographer | CC BY-SA 2.0 (read on the page) | 2009-01-26 | a yellow skip from its end in a terraced street at the kerb: the end plates slope inward, a painted FILL LEVEL line below the rim, a telephone number, traffic cones at the end | YES | any number (oblique, with a number and a house for sale in the frame); the number and the street (not previewed) | 2009 |
| S3 | https://www.geograph.org.uk/photo/1116404 | 2026-10-13 | David Wright | CC BY-SA 2.0 (read on the page) | 2009-01-11 | an orange skip beside a kerb on double yellow lines at a crossroads with a firm's name on its side (the orange colour variant) | no | everything (looked at only: it carries a firm's name) | 2009 |
| S4 | https://en.wikipedia.org/wiki/Skip_(container) | 2026-10-13 (raw wikitext) | Wikipedia contributors | CC BY-SA 4.0 | n/a (a text) | the skip's side is a trapezium or two stacked trapezia, the smaller edge at the bottom of the lower one and at the top of the upper one; usually two lugs on each side for chains; drop-door skips; sizes from 2 to 40 cubic yards (mini to roll-on) | YES | any picture | n/a |
| S5 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | no skip; concrete_road_barrier, industrial_storage_cart, plastic_container: none a skip | no | everything: no CC0 skip exists, so it is made by script | n/a |
| S6 | production/specs/vignette-scene.json and production/research/period-vehicles-and-props (this repository) | 2026-10-13 | this project | own work | n/a | the held skip (stood at x 22.5 in the west carriageway, off since 2 October: 'a granite box in the carriageway'); the research note's skip 'about 2.6 x 1.5 x 1.2 m'; two cones at x 21.3 and 23.7 at 0.35 m from the kerb; a crowd-control barrier across the yard mouth | YES | the box shape | n/a |
| S8 | https://www.legislation.gov.uk/uksi/1984/1933/made | 2026-10-13 (the made text and the original print PDF, page 5686 for Schedule 1's diagram) | the Secretary of State for Transport and the Secretary of State for Wales (a statutory instrument: The Builders' Skips (Markings) Regulations 1984, SI 1984/1933) | Open Government Licence v3.0 (legislation.gov.uk) | 1984-12-11 (made; in force 21 January 1985; the marking required from 1 January 1986) | every end of a builder's skip any part of which stands on a highway other than a footway or verge must from 1 January 1986 carry a marking of two plates of equal size and shape (BS AU 152: 1970, the rear marking plate standard), red fluorescent stripes and yellow reflex-reflecting ground as Schedule 1's diagram shows (each plate 140 to 280 wide, 350 to 700 long, area at least 980 square cm, stripes 40 to 50 degrees to the vertical and 133 to 147 broad, rising toward the inner edge); Schedule 2 places them: as near an outer edge as the skip allows, innermost edges equidistant from the skip's axis, upper edges level with each other and not lower than the skip's upper edge unless the construction needs it, at most 1.5 m above the ground, never on a lid, on a door only if nowhere else will do | YES | BS AU 152 itself (not freely readable: the plate's own small marking is a Judgement); no picture | in force in 1990: a skip in Quay Street's road carries these plates on both ends |
| S7 | https://api.geograph.org.uk/syndicator.php (terms skip, skip hire, builders skip, skip in the street; takenyear 1980 to 1996 and without a year) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1980 to 1996 searched | no skip photograph before 1998 (a 1998 hit is a house named Skipness); about 100 photographs from 2009 on, most of Skip Bridge (a place name) | no | measuring | n/a |

What was searched: Poly Haven's model list (no skip); Geograph's feed for `skip`, `skip hire`, `builders skip`, `skip in the street` with each year 1980 to 1996 and without a year (none before 2009 apart from a house called Skipness). Wikimedia Commons was not asked.

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| vignette-scene.json: the held skip (off since 2 Oct), its cones and its barrier | a granite box, two cones, a crowd-control barrier | REPLACED (the box); the cones and the barrier KEPT where they are (the cones stand on the footway at z -3.35, clear of the skip) | W1; the cones' z |
| production/research/period-vehicles-and-props NOTE.md and asset-plan: skip 2.6 x 1.5 x 1.2 m | a size | REPLACED by the photograph's profile (6-yard); the 4-yard is a scale | W1 |
| Poly Haven models | no skip | NOT USED | S5 |
| git branches (git log --all for skip) | none | none to reuse |  |

## The target

Axes: x along the skip (the firm's name faces -y), y across, z up from the floor's underside on the ground. The side plates are prisms of the hexagonal profile in the x-z plane; everything else is boxes (the end plates rotated about y).

### Assembly in words

- **Profile (x, z)**: floor edge (+-924, 0) up to the widest line (+-1508, 793) up to the top (+-1160, 1200): two stacked trapezia, the lower one's smaller edge at the bottom, the upper one's at the top.
- **Plates**: two side plates 5 mm at y -850 to -845 and 845 to 850, a floor 5 mm, four end plates 5 mm (lower: floor edge to the widest line, upper: widest line to the top) sloping out and in with the sides.
- **Rim**: a folded bar 50 wide and 86 deep along both top edges and across the ends, its lower edge at 1114.
- **Rib**: a bar 50 high, 10 proud along each side at 923 (P1's line under the rim).
- **Lugs**: four, 80 x 60 x 25 at x -990 and 990, z 1090 to 1150, corners r 10 with a 30 mm hole (a texture mask).
- **Lamps**: two amber battery lamps 90 x 95 x 150 hung on the road side's rim by a hook, at x -1100 and 1100, z 1000 to 1150.
- **Edges and fixings**: plate edges folded or square, corners r 12 at the profile's points (a bevel on the mesh), welds not modelled (a seam texture along every plate joint, 6 mm wide).

### Parts, variant SK1: SK1: a 6-yard builder's skip, 3.0 m long, yellow, empty (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| side_f | prism | skip_paint | -1508 to 1508 | -850 to -845 | 0 to 1200 | folded top edge, corners r 12 | side plate, 5 mm, hexagonal profile |
| side_b | prism | skip_paint | -1508 to 1508 | 845 to 850 | 0 to 1200 | folded top edge | the other side plate |
| floor | box | skip_paint | -924 to 924 | -845 to 845 | 0 to 5 |  | floor plate 5 mm |
| end_low_r | box | skip_paint | 922 to 1510 | -845 to 845 | -1 to 794 |  | lower end plate, sloping out and up to the widest line |
| end_up_r | box | skip_paint | 1158 to 1510 | -845 to 845 | 791 to 1202 |  | upper end plate, sloping in and up to the top rim |
| end_low_l | box | skip_paint | -1510 to -922 | -845 to 845 | -1 to 794 |  | lower end plate, sloping out and up to the widest line |
| end_up_l | box | skip_paint | -1510 to -1158 | -845 to 845 | 791 to 1202 |  | upper end plate, sloping in and up to the top rim |
| mark_s1 | box | marking_red_yellow | 1238 to 1487 | -840 to -570 | 824 to 1115 | corners r 5, a 2 mm yellow border | end marking plate 1 of 2 on the south end (Schedule 1: red fluorescent stripes on yellow reflex), 270 x 380 x 3, upper edge 4 mm under the rim bar |
| mark_s2 | box | marking_red_yellow | 1238 to 1487 | 570 to 840 | 824 to 1115 | corners r 5, a 2 mm yellow border | end marking plate 2 of 2 on the south end (Schedule 1: red fluorescent stripes on yellow reflex), 270 x 380 x 3, upper edge 4 mm under the rim bar |
| mark_n1 | box | marking_red_yellow | -1487 to -1238 | -840 to -570 | 824 to 1115 | corners r 5, a 2 mm yellow border | end marking plate 1 of 2 on the north end (Schedule 1: red fluorescent stripes on yellow reflex), 270 x 380 x 3, upper edge 4 mm under the rim bar |
| mark_n2 | box | marking_red_yellow | -1487 to -1238 | 570 to 840 | 824 to 1115 | corners r 5, a 2 mm yellow border | end marking plate 2 of 2 on the north end (Schedule 1: red fluorescent stripes on yellow reflex), 270 x 380 x 3, upper edge 4 mm under the rim bar |
| rim_f | box | skip_paint | -1160 to 1160 | -855 to -805 | 1114 to 1200 | outer corners r 8 | top rim bar 86 deep, 50 wide, folded |
| rim_b | box | skip_paint | -1160 to 1160 | 805 to 855 | 1114 to 1200 | outer corners r 8 | top rim bar 86 deep, 50 wide, folded |
| rim_end_r | box | skip_paint | 1135 to 1185 | -805 to 805 | 1114 to 1200 |  | top rim across the end |
| rim_end_l | box | skip_paint | -1185 to -1135 | -805 to 805 | 1114 to 1200 |  | top rim across the end |
| rib_f | box | skip_paint | -1397 to 1397 | -860 to -850 | 898 to 948 |  | stiffening rib 50 high, 10 proud, along the side (P1's line below the rim) |
| rib_b | box | skip_paint | -1397 to 1397 | 850 to 860 | 898 to 948 |  |  |
| lug_f1 | box | skip_paint | -1030 to -950 | -875 to -850 | 1090 to 1150 | corners r 10 | chain lug, 80 x 60 x 25 |
| lug_f2 | box | skip_paint | 950 to 1030 | -875 to -850 | 1090 to 1150 | corners r 10 | chain lug, 80 x 60 x 25 |
| lug_b1 | box | skip_paint | -1030 to -950 | 850 to 875 | 1090 to 1150 | corners r 10 | chain lug, 80 x 60 x 25 |
| lug_b2 | box | skip_paint | 950 to 1030 | 850 to 875 | 1090 to 1150 | corners r 10 | chain lug, 80 x 60 x 25 |
| lamp_1 | box | lamp_amber | -1145 to -1055 | -950 to -855 | 1000 to 1150 |  | amber battery lamp 90 x 95 x 150 hung on the rim bar at the end |
| lamp_hook_1 | box | galvanised | -1115 to -1085 | -858 to -845 | 1140 to 1200 |  | hook over the rim |
| lamp_2 | box | lamp_amber | 1055 to 1145 | -950 to -855 | 1000 to 1150 |  | amber battery lamp 90 x 95 x 150 hung on the rim bar at the end |
| lamp_hook_2 | box | galvanised | 1085 to 1115 | -858 to -845 | 1140 to 1200 |  | hook over the rim |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | source error (what the source can tell) | builder tolerance (what the check allows) |
|---|---|---|---|---|---|---|
| N1 | overall height | 1200 mm | Judgement | 1200 mm: the research note and the scene's earlier skip give about 1.2 m; it also fixes P1's scale (the skip's height from its top edge row 197.5 to its foot row 331.5 = 134 px, 0.1117 px per mm); error 100 | +-100 | +-100 |
| N2 | widest length (at the junction of the two trapezia) | 3016 mm | Photo, scaled on the assumed height | P1 tip_left_x 559.6 to tip_right_x 896.4 = 336.7 px at 0.1117 px per mm (the height is the assumed unit); error 150 | +-255 | +-150 |
| N3 | floor length (the bottom edge) | 1848 mm | Photo, scaled on the assumed height | P1 bottom_left_x 624.8 from the centre 728.0 = 924 mm half length (the right corner is faint; symmetry assumed); error 120 | +-155 | +-120 |
| N4 | rim bar depth | 86 mm | Photo, scaled on the assumed height | P1 rim_under_y 207.1 below the top edge 197.5: 9.6 px = 86 mm; error 20 | +-20 | +-20 |
| N5 | stiffening rib centre above the floor | 923 mm | Photo, scaled on the assumed height | P1 rim_line_y 228.4 above the foot 331.5: 103.1 px = 923 mm; error 40 | +-80 | +-40 |
| N6 | height of the widest line | 793 mm | Photo, scaled on the assumed height | P1 tips at row 243 of the turned copy: (331.5 - 243) / 0.1117 = 792; error 50 | +-70 | +-50 |
| N7 | width across the skip (the floor plus the side plates) | 1690 mm | Judgement | a 6-yard builder's skip is about 1.7 m wide over its side plates; the photograph is a side view and gives none; error 150 | +-150 | +-150 |

### Photograph measurements (P1, S1)

the photograph is turned 7.2 degrees about (730, 270) because the skip stands tilted on a slope (the top rim's slope), then each edge is the strongest grey-level step inside the recorded window on the turned copy; the scale is fitted on the one span from the rim bar's lower edge to the foot (124.4 px for 1114 mm if the skip is 1200 high: 0.1117 px per mm); the height of 1200 is Judgement (it sets the scale), so the proportions are checked and the absolute lengths are judged; the right bottom corner and the top corners are against fence wire and sky and faint, so they are not used; the tolerance is the measured spread times 3 plus 2 px, at least 6 px (54 mm).

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P1 | rim_under_y | y | 207.1 | [650, 202, 780, 212] | 7.0 | lo of rim_f |
| P1 | rim_line_y | y | 228.4 | [650, 222, 700, 242] | 6.0 | lo of rib_f |
| P1 | bottom_y | y | 331.5 | [670, 326, 740, 345] | 6.0 | lo of floor |
| P1 | tip_left_x | x | 559.6 | [536, 238, 562, 246] | 6.0 | lo of side_f |
| P1 | tip_right_x | x | 896.4 | [894, 236, 914, 244] | 6.1 | hi of side_f |
| P1 | bottom_left_x | x | 624.8 | [606, 326, 640, 332] | 6.0 | lo of floor |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| skip_paint | skip yellow, chalked and dented | 226, 188, 24 | 0.60 (semi-matt) | metal | steel under paint: dents, chipped to rust at the rim, mud to knee height, black rubber and tar splashes; yellow in the sample (variants: orange, blue-green) |
| lamp_amber | amber battery lamp lens | 220, 120, 20 | 0.20 (glossy) | not metal | emissive at night: the lantern colour (1.0, 0.25, 0.0) linear; off by day |
| galvanised | galvanised hook | 140, 142, 140 | 0.50 (satin) | metal |  |
| marking_red_yellow | end marking plate: red fluorescent stripes on yellow reflex-reflecting sheet | 243, 205, 24 | 0.30 (smooth, retro-reflective sheet) | not metal | the yellow is the plate's reflex ground (a little brighter and cleaner than the skip's chalked yellow), the red the fluorescent stripes: 45 degrees to the vertical, 140 mm breadth up the plate, rising toward the plate's inner edge (the two plates of an end make a chevron pointing up); the stripe pattern is a texture (numbers in marking); the colours are Judgement from the regulation's words; scuffed, dirt-streaked, the red faded toward orange-red, one plate cracked across a corner |

### Wear

- yellow paint chalked, dented along the rim and the lower plates (a hundred dents 20 to 80 mm, seeds), chipped to rust at the rim's top edge and the lugs, rust runs 30 to 120 mm below the chipped places
- mud and cement to knee height (a mask from the floor up, 0.4 m on the side plates), black tar and bitumen splashes, lime-white splashes
- the stencilled name worn, a few letters chipped; the paint on the end plates scraped by the lorry's chains
- the lamps: dirty lenses, one cracked (a seed)
- the four end marking plates: scuffed and dirt-streaked (the regulation asks them to be clean and efficient, so a dirty one is a street fact, not the target), the fluorescent red faded toward orange-red, one plate cracked across a corner (a seed), mud splashes on the lowest 100 mm
- contents: empty in the sample (a variant carries a heap of plasterboard, bricks and timber lath, never a person or a drink container: a seed in the builder's decals)
- NOT shown: a real firm's name or number, a person, any drink container

### Variants the street needs

- SK1 (the sample): the 6-yard skip, yellow, empty, on the road at the yard mouth.
- colours: yellow (the sample), orange, blue-green; each firm paints all its skips one colour.
- SK2 (not written as geometry): the 4-yard skip is SK1 scaled by 0.8 in x and y and 0.85 in z; its lugs move with it.
- contents (seeds, never a mesh in the target): empty; half full of rubble; full with a heap above the rim. Nothing else.

### Where it stands on Quay Street

**Slot:** west carriageway, the long side parallel to the kerb, centre x 22.5 m (in front of the yard mouth, x 21 to 24), 0.30 m from the kerb face (the skip's near side at z -2.70, its centre line at z -1.85), the firm's name and the lamps on the road side (street +z); its floor lies on the road's camber, tilted 1.4 degrees with the kerb side low; the south end (street -x) faces the hook camera with two striped marking plates on each end

- the 2 October ruling took the skip off the street 'until real'; the scene's story ('the yard is shut': a barrier across the mouth, cones, a skip) places it before the yard mouth, one event with the pallets behind the barrier (the pallets target)
- the near lane is 3.0 m: a skip 1700 mm wide at 0.30 m from the kerb leaves 3.0 - 0.30 - 1.70 = 1.0 m in its own lane and the whole 3.0 m other lane: the street stays passable (2.8 m is the least a bus needs; cars are off in any case); the shared placement rows measure the widest free width across the road
- its length is 3.0 m, the width of the yard mouth: it fills the street frontage of the gap without crossing a shop front
- THE CONES DO NOT MOVE. The first version moved the scene's two cones to x 20.7 and 24.3 on a misreading: they stand on the west FOOTWAY, 0.35 m behind the kerb face (vignette-pieces.json prop_traffic_cone_01_0 and _02_0 at z -3.35), not inside the skip's length; the skip (z -2.70 to -1.00) does not touch them, and cones moved to x 20.7 and 24.3 at that depth would stand inside the bollards there (prop_decorative_bollard_02_0 and _1, z -3.40 to -3.60). If cones are wanted at the skip's road ends they go at z -1.85, in the carriageway on the skip's centre line, at x 20.7 and 24.3; the cones are off the drawn street since 3 October
- a skip on the highway needs lamps at night and a permit: the two amber lamps are on the skip; the double yellow lines (0.25 m from the kerb) lie under it: a skip on the lines is a street fact (a permit, Judgement)
- a skip any part of which stands on the carriageway carried, from 1 January 1986, a marking of two striped plates on each end (SI 1984/1933, S8): the south end faces the hook camera, about 24 m away and 20 degrees off its axis, well inside the frame, so four striped plates are among the first things a 1990 skip in the road shows; they are on the upper end plates, level with each other (their upper edges 4 mm under the rim bar, about 1.1 m above the road), 270 wide, 380 long, 5 mm inside the end's outer edges and mirror images about the skip's axis
- the floor lies on the road's camber: 1 in 40 is 1.43 degrees, the kerb side low, 42 mm across the 1690 width

### Lettering and text

- Firm: TIDEWAY SKIP HIRE (invented: a fictional placeholder until the town mints one, kept in the stencil's own texture layer and blank in any picture for his page), number: TEL. 0632 960142 (invented, a British number: the period STD code 0632 and the exchange 960, the range British drama uses): stencilled black capitals, name 120 mm and number 90 mm tall, on the side plate between z 450 and 760, centred; FILL LEVEL 40 mm tall 120 below the rim on the end plates.

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the skip's size and shape | the research note and the scene: about 2.6 x 1.5 x 1.2 m, a plain box ('a granite box in the carriageway') | S1: a hexagonal side profile, widest at 793 up, 3.0 m long at its widest if 1.2 m high (the ratio 2.5 holds in S1), bottom 1.85 m long, top 2.3 m long | the S1 profile at 3015 x 1200 (a 6-yard); a mini skip is a scale of the same profile (variant) |
| W2 | the rim | none | S1: a folded rim bar about 86 mm deep, a stiffening rib line 190 below it (923 above the floor) | rim 86 deep and 50 wide, a rib 50 high 10 proud |
| W3 | the lugs | S4: usually two on each side | S1: two small lugs near the top at about x -990 and +990 | two on each side at x -990 and +990, 80 x 60 x 25 |
| W4 | the end markings | the first version: none (it named lamps and a permit for a skip on the highway and nothing else) | S2 shows a skip from its end in a terraced street with its end plates and a FILL LEVEL line; the law (S8, Schedules 1 and 2) puts two striped plates on each end of a skip standing on a highway from 1 January 1986 | two plates 270 x 380 on each end's upper end plate, red fluorescent stripes on yellow reflex, 45 degrees, 140 broad, rising toward the inner edges (the review of 13 October found their absence) |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: overall height | measure it on the built mesh in millimetres (bbox) | 1200 mm | +-100 mm |
| N2: widest length (at the junction of the two trapezia) | measure it on the built mesh in millimetres (extent) | 3016 mm | +-150 mm |
| N3: floor length (the bottom edge) | measure it on the built mesh in millimetres (extent) | 1848 mm | +-120 mm |
| N4: rim bar depth | measure it on the built mesh in millimetres (extent) | 86 mm | +-20 mm |
| N5: stiffening rib centre above the floor | measure it on the built mesh in millimetres (centre) | 923 mm | +-40 mm |
| N6: height of the widest line | measure it on the built mesh in millimetres (edge) | 793 mm | +-50 mm |
| N7: width across the skip (the floor plus the side plates) | measure it on the built mesh in millimetres (extent) | 1690 mm | +-150 mm |
| C1: the side profile has six corners, the widest line at 793 up | the side plate's outline | hexagon | +-50 mm |
| C2: no part floats; the end plates meet the floor and the sides | the contact graph | connected | 0 floating |
| C3: the side plate is closed from the side at 0, 30 and 45 degrees | rays at the side plate | 0 get through | exact |
| C4: the name and number are the invented ones | the stencil text layer | the placeholder firm and a British number of the form TEL. 0632 960nnn (no 555) | exact |
| C6: both ends carry two marking plates | count the marking plates on each end plate; their size, stripe angle and breadth, their upper edges | 2 + 2 plates, 270 x 380 (140 to 280 by 350 to 700, area at least 980 square cm), stripes 45 degrees (40 to 50), breadth 140 (133 to 147), upper edges level, under 1500 above the ground | exact |
| C5: two lamps lit at night in the lantern colour | emissive colour | (1.0, 0.25, 0.0) | +-0.02 |

### For the builder

- build by script: the two side plates are prisms of the hexagonal profile in the x-z plane (5 mm), the floor and the four end plates are boxes (the end plates' rotations are in target.json), the rim a folded bar along the top edge
- texture: yellow paint with the stencil on the side plate as a SEPARATE texture layer, blank in any picture for his page (the firm and the number are fictional placeholders in text.hire_firm and text.number_line); the marking plates have their own texture (see marking); no real mark
- lamps: emissive amber (1.0, 0.25, 0.0) linear at night, off by day; the lens 90 across
- keep the hexagonal profile exact: its widest line is at 793 and its bottom edge shorter than its top

## Owed to Jafar's page (one line each, with a recommendation)

1. Put the skip back in the road before the yard, with its two lamps lit at night, the striped end plates the law asked for, and a made-up hire firm's name on it, now that it is a real skip? (recommended: Yes, put it back)

## Handovers (for the town or the scene's owner, not for his page)

- H1: For the town: mint the skip hire firm's name and a telephone number in the town's own STD code for the skip's stencil (now the placeholders 'Tideway Skip Hire' and 'TEL. 0632 960142', kept in the stencil's own texture layer and never shown on Jafar's page).

## What the target could not settle

- absolute size: S1 has no scale object, the height 1200 is assumed and sets 0.1117 px per mm; the profile's proportions are measured, its lengths follow
- the width across (1700, Judgement: no end view was measured; S2's end view is oblique)
- the right bottom corner and the top corners (faint against fence and sky in S1): the profile is taken symmetric about the centre of the widest line
- whether a skip stood on Quay Street in 1990 (the scene's story says one did; the ruling put it back as soon as it is real)
- the marking plates' own colours and small mark: the regulation names red fluorescent and yellow reflex-reflecting and the Standard BS AU 152: 1970, which was not read; the sRGB values and the small 'BS AU 152' marking are Judgements
- the skip's share of the hook frame is a projection of the target's own parts with nothing hiding it, not a render
- the lamps' exact fixing (a hook over the rim: Judgement)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the profile against the photograph's edges, the lengths from the parts, the width and gaps in the lane, the scene's cones against the skip, the optional road-end cones, the stencil text and its placeholders, the lamps' colour, the four marking plates against the regulation's ranges (size, area, stripe angle and breadth, symmetry, level upper edges, height), the camber, the skip's share of the hook frame by projection). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
