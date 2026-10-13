# Quay Street's A-board outside the fish market: the exact target

**The A-board is the fish market's painted plywood pavement board: two leaves 600 x 990 x 12 hinged at the top and standing 12 degrees off the vertical (972 high, 435 deep), each with two feet cut with a flared arch 58 high, back battens, a screw eye in the right edge and one loose steel chain hanging 242 below the eyes; a fish list painted on both faces (cod at 2.60 a pound is the only sourced price) with the market's own hours; it stands on the east pavement outside the fish market at x 14.45 against the stallriser, 1.16 m clear on the kerb side, and is out only from 7.30 to 14.00 (Wednesday 13.00); a second, smaller framed notice board (508 x 762) after a 1978 photograph is written for a second shop; it replaces the scene's 0.68 x 0.90 x 0.36 placeholder and moves it off a line that left under 0.68 m of walking room on both sides; no photograph of 1975 to 1995 shows a painted ply board, so its construction rests on a 2013 photograph and its proportions are checked on a 1978 one.**

Cloud week 42, unit 13, family 9. Written 13 October 2026; the fixes the review asked for are applied, not re-reviewed. `SELF-CHECK a-board: 171 checks, 171 passed, 0 failed; negative controls 56 of 58 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/a-board/`: p1 (S1, the board's face blurred), its target-on-photo overlay, and p2 (S2, the 1978 notice board).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | not a car, skip or pallet and not the phone box; the A-board is a shop's pavement furniture, so none of the 2 October lines is touched |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no free model fits: Poly Haven has one chalkboard (1.5 m, a cafe's, held for the tea room) and a hazard sign (S6), so the board is our own, scripted from S1 and S2 |
| content rule (canon D18) | what the rule forbids is out of image and text | no shop name, drink, bet, person or advertisement on any face; the list is fish and its prices per pound; the data scan finds none |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S4 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | off-white ply, black capitals, grey splash and rust weeping: grime is the strategy; the board is a worn thing in a damp street |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the board is indoors at night (the market shuts at 14.00) |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |
| RULINGS 3 Oct (trades) | bay 1 fishmonger, bay 3 empty unit, bay 4 launderette, bay 5 grocer; west_north newsagent and tobacconist, ironmonger, tea room; east_chandler a chandler | the board is the fishmonger's and stands in bay 1; AB2 is a spare for the newsagent or the tea room |
| RULINGS 3 Oct (poll-tax posters) | an invented local campaign, never real parties or people | no poster on any face; the notice card of AB2 is left to the street's decals |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/3671864 | 2026-10-13 | Walter Baxter | CC BY-SA 2.0 (read on the page) | 2013-09-14 | a painted plywood A-board on a village pavement, front leaf square on: a plain rectangle with two feet and a flared arch cut in its lower edge, painted lettering in black, pink and blue, a bare-ply edge strip on its right side, the back leaf's edge beside it, and a loose steel chain hanging from a screw eye in the right edge | YES | any lettering or name (it names a tea room and carries a hard-hat picture; none is copied), the colours of the lettering, any absolute size (no scale object; the leaf's width is assumed), the lean (a front view) | 2013 photograph of a home-made board of a type that was common long before 1990 (ply, hinges, chain, foot arch); it is the construction that is used, never its date |
| S2 | https://www.geograph.org.uk/photo/6913397 | 2026-10-13 | Alan Murray-Rust | CC BY-SA 2.0 (read on the page) | 1978-08-04 | a framed white notice board leaning against the front of an open-top tour bus on a bus station apron: a thin timber frame holding a white panel with a printed card, standing on the ground at a lean; people and a bus operator's marks are in the picture | YES | the people (not drawn, not in any preview), the operator's name and plates (real marks, masked), the card's wording, the board's absolute size (the bus tyre as a scale is judged to 15 percent) | 1978: the only 1975 to 1995 photograph of a pavement board that was found; 12 years before the game but the same trade type |
| S3 | https://www.geograph.org.uk/photo/2783627 | 2026-10-13 | HelenK | CC BY-SA 2.0 (read on the page) | 2012-01-27 | a green-bordered black chalkboard on an A-frame with an arched top outside a cafe, on a wet pavement beside a road | no | everything: looked at and set aside; a painted chalk menu board with an arched top is a 2010s fashion that no 1975 to 1995 photograph found here supports, and it is not a fishmonger's board | 2012 |
| S4 | https://www.geograph.org.uk/photo/2808162 | 2026-10-13 | John Baker | CC BY-SA 2.0 (read on the page) | 1984-04-13 | a narrow shopping street in York in 1984 with hanging signs and a plain board fixed to a wall; no pavement board is in the picture | no | everything: looked at for 1980s street signage; it shows no A-board | 1984 |
| S5 | https://api.geograph.org.uk/syndicator.php (terms sandwich board, pavement board, a-board, shop, shops, cafe, pavement, street, market, fish, chip, takeaway, butcher, bakery, newsagent, board, sign, blackboard, menu; each with takenyear 1975 to 1996) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | no 1980 to 1995 photograph whose caption or text names an A-board, sandwich board or pavement board; the year-filtered search for sandwich board gave two hits (a 1978 bus station, which is S2, and a 1985 dock view in Hull, read by caption only); the unfiltered searches gave 200 distinct photographs, 197 of them taken in 2006 or later, the other three being S2, that Hull dock view and a 1986 York street named Pavement | no | measuring (the hits were read for what they show, S2 aside) | n/a |
| S6 | https://api.polyhaven.com/assets?t=models and /info/standing_chalkboard_01 (this folder's polyhaven_checked_raw.json) | 2026-10-13 | ParzivalCG (Poly Haven) | CC0 1.0 | published 2021-12-24 | of 521 models only two are signs: standing_chalkboard_01 (an A-frame chalkboard 920 x 759 x 1509 mm, a cafe menu board; base colour checked at 100 percent: dark grey with chalk smudges and bare wood, no lettering) and WetFloorSign_01 (a yellow hazard sign 300 x 359 x 630 mm) | no | this board: the chalkboard is 1.5 m tall and a cafe's, not a fishmonger's 0.97 m painted board; it stays held for the tea room (the asset plan's line) | n/a |
| S7 | production/specs/vignette-scene.json (held_props pavement_sign at east x 15.2, the railing note, the awning at x 12.0, the decals block) and production/specs/vignette-bill-of-materials.json (E12, G6) (this repository) | 2026-10-13 | this project | own work | n/a | the placeholder board 0.68 x 0.90 x 0.36 m at x 15.2, 1.1 m from the kerb face, its faces turned along the pavement; the awning over the fish market at x 12.0; the 29 September finding that a gap under 0.68 m is too narrow to walk; the board's text is to come from the gig-bill decals (G6) | YES | the board's size and place (both are replaced) and its text (the fish list replaces the gig bill) | n/a |
| S8 | production/research/shop-window-interiors/FISHMONGER-2026-10-03.md (this repository) | 2026-10-13 | this project | own work | 3 October 2026 | the ONS cod fillet price of 1990 (574p/kg, about 2.60 a pound), prices per pound, hand-lettered tickets and whitewash lettering, the fish a 1990 shop sold | YES | any price except cod (no 1990 figure was found for the other fish: they are marked invented in text.lines) | 1990 figures |
| S9 | production/specs/hook-cast.json (places fish_front, fish_counter; area fish_market hours) and RULINGS.md (3 Oct trades) (this repository) | 2026-10-13 | this project | own work | n/a | the fish market's hours (Monday to Saturday, opening 7.30, closing 14.00, Wednesday 13.00), its pavement spot at x 12.0, z 4.2 and, in its note, a doorway about x 9.4 (replaced here by the shopfronts target's door slots: shop door x 10.294 to 11.300, side door x 9.35 to 10.294); bay 1 is the fishmonger | YES | the board's design | n/a |

What was searched: Geograph's feed for sandwich board, pavement board, a-board, blackboard, menu and a score of street words for each year 1975 to 1996, then unfiltered. Two period photographs were found and read in full: S2 (1978, the one used) and S4 (1984, no board). Every other hit with a board in it was 2005 or later. Wikimedia Commons and archive.org were not asked (the container's access is limited and Commons rate-limits). Sketchfab was not reached; Poly Haven's list was read in full (S6).

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| vignette-scene.json held_props pavement_sign (0.68 x 0.90 x 0.36, x 15.2, 1.1 m from the kerb face, yaw 90) | a placeholder board outside the fish market | REPLACED as a mesh (the leaf is 600 wide and 990 long); MENDED as a slot: the side, the faces along the pavement and 'outside the fish market' are kept, the line is moved to x 14.45 against the stallriser | its size disagrees with S1 and S2 (W1) and its place leaves under 0.68 m on both sides (W5) |
| vignette-scene.json decals, BOM line G6 (fly-posted gig bills and notices) | the board's text was to be a gig bill | NOT USED for this board; kept for the walls and the glazed case | a shop's board carries the shop's own trade (W3) |
| production/research/asset-plan 3-FURNITURE-PROPS-FOOD.md: Chalk A-board = Poly Haven standing_chalkboard_01 (held), the cafe's menu board | a CC0 chalkboard 920 x 759 x 1509 | KEPT for the tea room (not this target) | it is 1.5 m tall, an easel, and no 1975 to 1995 photograph supports a chalkboard of its kind (S3, S6) |
| production/assets/street/clutter/ (bollard, dustbin, grit bin, kx100, litter bin, pillar box, telegraph pole) | scripted street clutter | none to reuse | no A-board is among them |
| CATALOGUE.md, production/research (street-clutter-1990, asset-plan), every git branch (git log --all) | the newsagent's wire-fronted A-board is a reserve line; nothing was built | none to reuse | only research lines; no mesh or script for an A-board exists on any branch |
| Poly Haven models, WetFloorSign_01 | a yellow plastic hazard sign 300 x 359 x 630 | NOT USED | a different object (S6) |

## The target

Axes: x across the leaf (right is +x seen from the front leaf's face), y from the front leaf's painted face (-y) to the back leaf's (+y), z up from the paving, the pivot at the middle of the feet's line. Each leaf is built in its own frame and hung from the ridge line by its xf (a roll of -12 and +12 degrees about the pivot (0, 0, 990) and a lift that sets its inner foot edge on the paving). Parts are boxes, prisms (the feet), cylinders and one wire (the chain); the self-check measures every number back off the parts, in the part's own frame where the part is rotated.

### Assembly in words

- **The leaf**: a 12 mm ply panel 600 wide from 58 mm above the foot line to the ridge, and below it two feet, each 118 wide at the ground, whose inner edge flares from 182 mm out from the middle at the ground to 138 mm at the arch's flat top (58 high): the foot arch is 364 wide at the base and 276 at the top. Arrises eased 2 mm.
- **The back of each leaf**: two softwood battens 34 x 18 at 245 mm either side of the middle from 120 to 840 mm up, a cross batten 34 x 18 at 380 to 414 between them; two hinge leaves 50 x 52 x 3 near the top on the inner face. The inside is bare wood.
- **The ridge**: the two leaves meet along the line (0, 0, 968) and are held by two 8 mm knuckles, 54 long, 205 mm either side of the middle.
- **The chain**: a screw eye (r 5, 16 long, 12 mm proud) in each leaf's right edge 605 up the leaf (592 mm above the paving) and 5 mm links hanging free between them in a catenary 242 mm deep.
- **AB2**: a frame of 28 x 18 softwood strips, 508 x 762, a 4 mm white panel set 6 mm back, the same hinges, eyes and a chain (170 deep).
- **Pose and size**: each leaf stands 12 degrees off the vertical, 435 deep foot to foot, 972 high to the knuckles; AB2 is 352 deep and 749 high.

### Parts, variant AB1: AB1: painted plywood board with a foot arch, fish list on both faces (the sample; the fish market's) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| f_main | box | ply_paint | -300 to 300 | -206 to 0 | 57 to 971 | arrises eased 2 mm; cut edges bare ply, one long strip of bare edge on the right | 12 mm plywood leaf, 600 wide, from the arch's top to the ridge; the painted face is the front |
| f_foot_l | prism | ply_paint | -300 to -138 | -218 to -194 | -0 to 59 |  | left foot, 118 wide at the ground, the arch's flared side up to the flat top |
| f_foot_r | prism | ply_paint | 138 to 300 | -218 to -194 | -0 to 59 |  | right foot, the left one mirrored |
| f_stile_l | box | timber | -262 to -228 | -181 to -14 | 114 to 822 |  | back batten 34 x 18, stops the ply bowing (Judgement, hidden) |
| f_stile_r | box | timber | 228 to 262 | -181 to -14 | 114 to 822 |  |  |
| f_rail | box | timber | -228 to 228 | -127 to -102 | 368 to 405 |  | cross batten between the two |
| f_hplate_l | box | zinc | -230 to -180 | -12 to 1 | 909 to 961 |  | hinge leaf, 50 x 52 x 3, two screws (Judgement) |
| f_hplate_r | box | zinc | 180 to 230 | -12 to 1 | 909 to 961 |  |  |
| f_eye | cyl | zinc | 296 to 312 | -91 to -81 | 588 to 598 |  | screw eye in the right edge, 12 mm proud, holds the chain |
| f_eye_l | cyl | zinc | -312 to -296 | -91 to -81 | 588 to 598 |  | second screw eye in the left edge, level with the right one and the same size (S1 shows it, x -312 to -296); the chain does not use it |
| r_main | box | ply_paint | -300 to 300 | 0 to 206 | 57 to 971 | arrises eased 2 mm; cut edges bare ply, one long strip of bare edge on the right | 12 mm plywood leaf, 600 wide, from the arch's top to the ridge; the painted face is the front |
| r_foot_l | prism | ply_paint | -300 to -138 | 194 to 218 | -0 to 59 |  | left foot, 118 wide at the ground, the arch's flared side up to the flat top |
| r_foot_r | prism | ply_paint | 138 to 300 | 194 to 218 | -0 to 59 |  | right foot, the left one mirrored |
| r_stile_l | box | timber | -262 to -228 | 14 to 181 | 114 to 822 |  | back batten 34 x 18, stops the ply bowing (Judgement, hidden) |
| r_stile_r | box | timber | 228 to 262 | 14 to 181 | 114 to 822 |  |  |
| r_rail | box | timber | -228 to 228 | 102 to 127 | 368 to 405 |  | cross batten between the two |
| r_hplate_l | box | zinc | -230 to -180 | -1 to 12 | 909 to 961 |  | hinge leaf, 50 x 52 x 3, two screws (Judgement) |
| r_hplate_r | box | zinc | 180 to 230 | -1 to 12 | 909 to 961 |  |  |
| r_eye | cyl | zinc | 296 to 312 | 81 to 91 | 588 to 598 |  | screw eye in the right edge, 12 mm proud, holds the chain |
| r_eye_l | cyl | zinc | -312 to -296 | 81 to 91 | 588 to 598 |  | second screw eye in the left edge, level with the right one and the same size (S1 shows it, x -312 to -296); the chain does not use it |
| hinge_pin_l | cyl | zinc | -232 to -178 | -4 to 4 | 964 to 972 |  | hinge knuckle on the ridge line, 8 mm |
| hinge_pin_r | cyl | zinc | 178 to 232 | -4 to 4 | 964 to 972 |  |  |
| chain | wire | steel | 310 to 314 | -88 to 88 | 349 to 593 |  | a slack chain between the two screw eyes, 5 mm links, hanging free |

### Parts, variant AB2: AB2: framed notice board of the 1978 type (smaller; for the newsagent or the tea room, not placed today) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| f_frame_l | box | timber_frame | -254 to -226 | -176 to 0 | 0 to 749 | arrises eased 2 mm | softwood frame strip 28 x 18, painted white, worn to the grain on the arrises |
| f_frame_r | box | timber_frame | 226 to 254 | -176 to 0 | 0 to 749 |  |  |
| f_frame_t | box | timber_frame | -226 to 226 | -23 to 0 | 718 to 749 |  |  |
| f_frame_b | box | timber_frame | -226 to 226 | -176 to -153 | 0 to 31 |  |  |
| f_panel | box | card_white | -226 to 226 | -164 to -14 | 29 to 720 |  | 4 mm white board set 6 mm back from the frame's face, holds the notice |
| f_hplate_l | box | zinc | -200 to -150 | -12 to 1 | 686 to 738 |  |  |
| f_hplate_r | box | zinc | 150 to 200 | -12 to 1 | 686 to 738 |  |  |
| f_eye | cyl | zinc | 250 to 266 | -72 to -62 | 466 to 476 |  | screw eye in the right edge for the chain |
| r_frame_l | box | timber_frame | -254 to -226 | 0 to 176 | 0 to 749 | arrises eased 2 mm | softwood frame strip 28 x 18, painted white, worn to the grain on the arrises |
| r_frame_r | box | timber_frame | 226 to 254 | 0 to 176 | 0 to 749 |  |  |
| r_frame_t | box | timber_frame | -226 to 226 | 0 to 23 | 718 to 749 |  |  |
| r_frame_b | box | timber_frame | -226 to 226 | 153 to 176 | 0 to 31 |  |  |
| r_panel | box | card_white | -226 to 226 | 14 to 164 | 29 to 720 |  | 4 mm white board set 6 mm back from the frame's face, holds the notice |
| r_hplate_l | box | zinc | -200 to -150 | -1 to 12 | 686 to 738 |  |  |
| r_hplate_r | box | zinc | 150 to 200 | -1 to 12 | 686 to 738 |  |  |
| r_eye | cyl | zinc | 250 to 266 | 62 to 72 | 466 to 476 |  | screw eye in the right edge for the chain |
| hinge_pin_l | cyl | zinc | -202 to -148 | -4 to 4 | 741 to 749 |  |  |
| hinge_pin_r | cyl | zinc | 148 to 202 | -4 to 4 | 741 to 749 |  |  |
| chain | wire | steel | 264 to 268 | -70 to 70 | 299 to 472 |  | a slack chain between the two screw eyes |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | source error (what the source can tell) | builder tolerance (what the check allows) |
|---|---|---|---|---|---|---|
| N1 | leaf width | 600 mm | Judgement | a 600 mm (2 ft) board, assumed: P1 shows the board on asphalt beside a grating with no object of known size, so a pavement board anywhere from 500 to 700 wide fits; it sets P1's scale (0.6124 px per mm from the leaf's width of 367.4 px); source error 100 (builder tolerance 15) | +-100 | +-15 |
| N2 | leaf length along the slope | 990 mm | Photo, scaled on the assumed width | P1: leaf height 592.3 px (top edge to the foot's lower edge) = 967 mm projected; over the lean's cosine (0.978) with a 2.5 mm thickness term gives about 986; 990 kept (error 25); source error 17 percent of the value (the assumed width is 600 +-100), so +-168.3 | +-168.3 | +-25 |
| N3 | ply thickness | 12 mm | Judgement | 12 mm plywood (P1's bare edge strip is about 6 px = 10 mm at the lean; the standard sheet is 12); error 3 |  | +-3 |
| N4 | foot arch height | 58 mm | Photo, scaled on the assumed width | P1: from the feet (mean of two, 631.2 px) up to the arch top (596.9 px) is 34.3 px = 56 mm projected; builder tolerance 6; source error 17 percent of the value (the assumed width is 600 +-100), so +-9.9 | +-9.9 | +-6 |
| N5 | each foot's width at the ground | 118 mm | Photo, scaled on the assumed width | P1: the left foot 72.4 px and the right foot 73.9 px at 0.612 px per mm = 118 and 121 mm; builder tolerance 8; source error 17 percent of the value (the assumed width is 600 +-100), so +-20.1 | +-20.1 | +-8 |
| N6 | half width of the arch's flat top | 138 mm | Judgement | read by eye on a 3 times crop of P1 (the flat top ends about 85 px from the centre); not measured by the algorithm; error 15 |  | +-15 |
| N7 | lean of each leaf off the vertical (degrees) | 12 deg | Judgement | 12 degrees, the usual set of a pavement board; P1 is a front view and cannot show the lean; error 3 |  | +-3 |
| N8 | height to the ridge (top of the hinge knuckles) | 972.4 mm | Photo, scaled on the assumed width | P1: 592.3 px from the top edge to the lower foot edge = 967 mm projected (the front leaf's own top is 2.5 mm over the ridge line); the hinge knuckles 4 mm over; builder tolerance 30; source error 17 percent of the value (the assumed width is 600 +-100), so +-165.3 | +-165.3 | +-30 |
| N9 | depth of the standing board (foot to foot) | 435.1 mm | Judgement | from the lean and the length: 2 x (990 x sin 12 + 12 x cos 12) = 435; the scene's placeholder was 357 deep; error 40 |  | +-40 |
| N10 | chain: from its lowest point up to the top of its eye | 249.5 mm | Photo, scaled on the assumed width | P1: the ring at y 272 and the chain's lower end at y 420, read by eye on a 4 times crop (+-8 px): 148 px = 242 mm below the eye; the eye's radius 5 and the chain's 2.5 added; builder tolerance 40; source error 17 percent of the value (the assumed width is 600 +-100), so +-42.4 | +-42.4 | +-40 |
| N11 | screw eye's height above the paving | 590 mm | Photo, scaled on the assumed width | P1: the ring at y 272 (read by eye) is 361 px above the left foot's lower edge = 590 mm; builder tolerance 30; source error 17 percent of the value (the assumed width is 600 +-100), so +-100.3 | +-100.3 | +-30 |
| N12 | distance between the two hinges | 410 mm | Judgement | two butt hinges 205 mm either side of the middle (hidden on the inner faces; typical); error 30 |  | +-30 |
| N20 | AB2 leaf width | 508 mm | Judgement | 20 inches; P2's board is 60.6 px wide beside a bus tyre of about 128 px (taken as 1.0 m): about 0.47 m (+-15 percent), so the 508 mm board is the nearest standard; error 60 |  | +-60 |
| N21 | AB2 leaf length | 762 mm | Judgement | 30 inches; P2's board is 91.3 px high (projected) = about 0.71 m of tyre-scaled height, 0.73 m along the slope; error 70 |  | +-70 |
| N22 | AB2 frame strip width | 28 mm | Judgement | 28 mm softwood strip; P2's frame is about 3 px wide, below the pixel's reach; error 6 |  | +-6 |
| N23 | AB2 frame depth | 18 mm | Judgement | 18 mm; error 4 |  | +-4 |

### Photograph measurements (P1, S1)

the photograph was first turned 2.6 degrees about (265, 335) because the board's vertical edges ran 2 to 3 degrees off the picture's vertical (the left edge moved 22 px and the right edge 14 px over 420 rows); each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; the scale is fitted on the one height from the leaf's top edge to the left foot's lower edge (592.3 px) and the width, the right foot, the arch and the centre are predicted from it; the leaf's width of 600 mm is the unit that sets the absolute size (Judgement), so the check is of proportions; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (8 mm); the right foot sits 4.2 px higher than the left in the picture (the ground slopes), inside the tolerance.

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P1 | left_top | x | 70.4 | [62, 100, 80, 140] | 5.0 | lo of f_main |
| P1 | left_bot | x | 68.2 | [62, 500, 78, 540] | 5.0 | lo of f_foot_l |
| P1 | right_top | x | 435.9 | [430, 100, 439, 140] | 5.0 | hi of f_main |
| P1 | right_bot | x | 437.7 | [430, 500, 441, 540] | 5.0 | hi of f_foot_r |
| P1 | top_y | y | 41.0 | [200, 30, 300, 48] | 5.3 | hi of f_main |
| P1 | foot_left_y | y | 633.3 | [75, 620, 115, 640] | 5.0 | lo of f_foot_l |
| P1 | foot_right_y | y | 629.1 | [385, 620, 425, 640] | 6.0 | lo of f_foot_r |
| P1 | arch_top_y | y | 596.9 | [200, 588, 290, 606] | 5.0 | lo of f_main |

### Photograph measurements (P2, S2)

each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; no scale is fitted (the board's plane is neither square on nor level); only the projected width over the projected height is used, against the same ratio of the AB2 front leaf's drawing.

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P2 | left_x | x | 490.4 | [482, 500, 500, 520] | 5.8 | lo of f_frame_l |
| P2 | right_x | x | 551.0 | [540, 500, 560, 520] | 5.7 | hi of f_frame_r |
| P2 | top_y | y | 468.0 | [505, 464, 535, 471] | 4.0 | hi of f_frame_t |
| P2 | bottom_y | y | 559.3 | [505, 552, 535, 566] | 4.3 | lo of f_frame_b |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| ply_paint | painted plywood, off-white, weathered | 212, 213, 206 | 0.60 (satin to matt, chalking) | not metal | emulsion over ply (P1: grey-white, a blue cast in shade); the lower 150 mm streaked grey with splash, the top edge and the right arris rust-brown where the ply's glue line weeps (P1) |
| timber | softwood batten, bare | 176, 140, 96 | 0.80 (rough) | not metal | back of the board, grey-brown, never painted |
| timber_frame | softwood frame, white gloss, worn | 226, 224, 214 | 0.45 (gloss, chipped) | not metal | knocked to bare wood on the arrises and the lower rail |
| card_white | board panel, white | 236, 235, 228 | 0.70 (matt) | not metal | holds a notice card; the notice is a decal, never part of this mesh |
| zinc | zinc-plated steel, dull | 140, 142, 140 | 0.50 (satin) | metal | hinge leaves and knuckles, screw eyes: grey, a little rust at the screws |
| steel | chain, bright steel gone dull | 118, 118, 114 | 0.45 (semi-gloss) | metal | 5 mm links, a few with rust |

### Wear

- the leaf's paint is chalking off-white with a grey splash band to 150 mm above the paving, the lower arris and the feet's edges worn to bare ply; the top edge and the right arris carry rust-brown weeping from the glue line (P1)
- lettering is hand-painted and slightly uneven; one letter is overpainted in a second colour (P1 shows a word corrected in blue): a decal detail, not a mesh one
- the feet's arch is dirty to its flared edges; the ply swells at the foot's corners (a 2 mm lift) and the lower 40 mm of the bare edge is dark
- the screw eyes are grey with a rust ring; the chain is dull, two links rusted, hanging in a deep loop between the leaves (P1)
- the back of each leaf is bare grey-brown batten and ply, never painted
- NOT shown: a shop name, an advertisement, a person, a drink, a bet, a real brand on any face

### Variants the street needs

- AB1 (the sample): the fish market's painted board, one outside the fish market, out in its hours (7.30 to 14.00, Wednesday 13.00).
- AB2: the smaller framed notice board of S2's type (508 x 762, thin frame, white panel, a notice card); for the newsagent or the tea room if the town wants one; not placed today. The newsagent's wire-fronted headline board of the asset plan is a different object (its paper's name is owed by canon) and is not written here.
- conditions (materials): C0 sound; C1 worn (the sample's wear); C2 a leaf with a corner chipped to bare ply and the chain missing (a seed, not a mesh).
- lettering: T1 the fish list as written; T2 the same list with one price overpainted (a decal mask over T1, never other words).

### Where it stands on Quay Street

**Slot:** east pavement outside the fish market (bay 1, x 9 to 15): centre x 14.45 m, centre z 4.600 m (1.60 m from the kerb face), the board's two faces looking up and down the pavement (the scene's yaw 90), its leaves' side edges 0.063 m clear of the stallriser line (measured to the screw eye's tip; the leaf's own edge is 0.075 m clear); it replaces the scene's line at x 15.2, 1.1 m from the kerb face

- the scene's line stood at x 15.2 with its 0.68 m width across the pavement and its centre 1.1 m from the kerb face: it left 0.64 m on the kerb side and 0.54 m on the shop side of a 1.85 m footway, both under the 0.68 m of a walking person (the 29 September walk found the footway walled by a smaller obstruction), and its depth put it on the line of the party pilaster between the fish market and Rita's
- against the stallriser the board leaves 1.16 m clear on the kerb side, over the 1.0 m this target requires; the board is a shopkeeper's, put where the pavement is widest beside the shop
- x 14.45 is in front of the fish market's own window (bay 1 is x 9 to 15, RULINGS 3 Oct) and clear of Rita's (the pilaster face is 0.157 m beyond the board's end); the awning (x 10.5 to 13.5) is 0.73 m away and the pavement spot where the cast stands (x 12.0, z 4.2) is 2.5 m away, so nobody who waits at the fish market stands behind the board
- the fish market's shop door is at x 10.294 to 11.300 (centre 10.797) and its side door at x 9.35 to 10.294 (the shopfronts target); the board (x 14.23 to 14.67) stands 2.9 m from the shop door, so no door is blocked; the railing by the gully (x 10 to 12) is 2.2 m away
- the faces look along the pavement, as the scene had them: a board read by people walking up or down the street; the leaf's long side lies across the pavement
- the board is out only in the market's hours (Monday to Saturday from 7.30, shut at 14.00, Wednesday 13.00); a night frame has no board

### Lettering and text

- No shop name and no logo. Hand-painted capitals in black on both outer faces of AB1: heading FRESH FISH 70 mm; five lines of 36 mm, the fish at the left margin and the price at the right (cod fillet 2.60 LB, haddock 2.35 LB, plaice 2.10 LB, kippers 1.45 LB, dressed crab 95P EACH); then the market's hours: MON TO SAT 7.30 TO 2 and WED SHUT 1 (30 mm gap below the list).
- Prices: only the cod's is sourced (ONS 1990, 574p/kg, about 2.60 a pound, S8); the others are invented within a few percent and marked so in text.lines. The hours are the fish market's own from the town's cast file (S9).
- Letters are 0.62 of their height wide (a narrow signwriter's capital) with a 40 mm margin and at least a 60 mm gap between a fish's name and its price: every line is checked to fit the 600 mm leaf above the arch.

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the board's size | the scene's placeholder: 0.68 x 0.90 x 0.36 m | S1: a leaf about 600 wide and 1.65 times as long, two feet, a chain between the leaves; S2: a smaller framed board about 0.5 m wide | AB1 600 x 990 (the sample) and AB2 508 x 762; the placeholder is not used |
| W2 | the foot | none (a plain board in the plan) | S1: the foot is cut with a flared arch, 58 mm high, the base 364 mm wide | the arch as photographed (two feet, the arch's flat top 276 mm wide) |
| W3 | what the board carries | the scene file: the carrier gets a fly-posted gig bill (BOM line G6) | S1 and S8: a shop's own board carries its own trade in hand-painted capitals, and a fishmonger lists fish and prices per pound; gig bills are for blank walls | a painted fish list with the market's hours on both faces; G6 stays for the walls and the glazed case |
| W4 | the chain | none | S1: one loose chain hangs in a deep loop from a screw eye in each leaf's right edge, seen as one vertical line from the front | one catenary chain between two eyes at 592 mm, hanging 242 mm below them |
| W5 | the board's place | the scene's line at x 15.2, 1.1 m from the kerb face | no photograph can say (the scene gives 0.54 and 0.64 m of walking room on either side; the 29 September finding says 0.68 m) | x 14.45 against the stallriser, 1.16 m clear on the kerb side |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: leaf width | measure it on the built mesh in millimetres (local) | 600 mm | +-15 |
| N2: leaf length along the slope | measure it on the built mesh in millimetres (local) | 990 mm | +-25 |
| N3: ply thickness | measure it on the built mesh in millimetres (local) | 12 mm | +-3 |
| N4: foot arch height | measure it on the built mesh in millimetres (local) | 58 mm | +-6 |
| N5: each foot's width at the ground | measure it on the built mesh in millimetres (local) | 118 mm | +-8 |
| N6: half width of the arch's flat top | measure it on the built mesh in millimetres (local) | 138 mm | +-15 |
| N7: lean of each leaf off the vertical (degrees) | measure it on the built mesh in millimetres (xf) | 12 deg | +-3 |
| N8: height to the ridge (top of the hinge knuckles) | measure it on the built mesh in millimetres (bbox) | 972 mm | +-30 |
| N9: depth of the standing board (foot to foot) | measure it on the built mesh in millimetres (bbox) | 435 mm | +-40 |
| N10: chain: from its lowest point up to the top of its eye | measure it on the built mesh in millimetres (span) | 250 mm | +-40 |
| N11: screw eye's height above the paving | measure it on the built mesh in millimetres (centre) | 590 mm | +-30 |
| N12: distance between the two hinges | measure it on the built mesh in millimetres (centre_dx) | 410 mm | +-30 |
| N20: AB2 leaf width | measure it on the built mesh in millimetres (local_span) | 508 mm | +-60 |
| N21: AB2 leaf length | measure it on the built mesh in millimetres (local) | 762 mm | +-70 |
| N22: AB2 frame strip width | measure it on the built mesh in millimetres (local) | 28 mm | +-6 |
| N23: AB2 frame depth | measure it on the built mesh in millimetres (local) | 18 mm | +-4 |
| C1: no part floats | the contact graph of the meshes (touching within 2 mm) | all parts reach the ground through the feet | 0 floating |
| C2: both leaves' outer faces and feet are closed | rays at each leaf's face at 0, 30 and 45 degrees; the arch is the only opening | 0 get through | exact |
| C3: the chain is slack, hangs free and ends on both eyes | the chain's polyline: ends on the eye tips, length over span at least 1.15, lowest point over 150 mm above the paving | all three | exact |
| C4: the text fits the leaf and says what the market says | line widths at 0.62 of the letter height against the leaf's width less 80 mm; hours against hook-cast.json; cod price against the research note | fits and agrees | exact |
| C5: the board stands where the placement says and leaves 1.0 m | the footprint against the kerb, stallriser, pilaster, awning, doorway and the cast's spot | x 14.45, z 4.600, 1.16 m clear | +-50 mm |

### For the builder

- leaf: a 12 mm ply panel 600 wide from the arch's top to the ridge plus two feet cut with the flared arch, all one mesh of one material; the arch's flared sides are the polygon in the foot parts; the painted face is the decal (text.lines) laid on the outer face, 3 px per mm
- pose: both leaves hang from the ridge line (the pivot in each part's xf) and lean 12 degrees, the front leaf's face looking -y; the lowest edge of each leaf is its inner foot edge on the paving; build in the leaf's own frame and use the xf as given
- the chain: 16 straight 5 mm segments along the catenary in the wire part (a chain of links is a texture on a tube); it hangs free of both leaves and of the ground (its lowest point is 350 mm up)
- hinges: two butt hinges on the inner faces, knuckles on the ridge line; the leaves' top inner edges meet there
- orientation: the local -y faces up the pavement for the front leaf; the street's yaw 90 turns the board so the two faces look along the pavement

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- absolute sizes: S1 has no scale object, the leaf's width (600 mm) is assumed and sets 0.612 px per mm; every size from S1 is Judgement or Photo within the stated error; AB2's size rests on S2's tyre as a scale, good to about 15 percent
- the lean (12 degrees): neither photograph is a side view; a real board stands between 10 and 15 degrees
- the 1975 to 1995 date of S1's type: the only dated photograph (S2, 1978) shows a framed board, not a painted ply board with a foot arch; a home-made painted board is certainly older than 1990, but no 1990 photograph of one was found
- the hinges and the back battens: both are hidden from the front and no photograph shows them (Judgement)
- the other fish's 1990 prices (only the cod's is sourced); and the wording a real fishmonger would have painted
- whether Quay Street's fishmonger put the board out every day (the hours say when it could be out; the town has no rule)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the lean from the parts' transform, the two leaves as mirrors, the foot arch against P1's arch ratio, the chain's ends, slack and clearance, the text's fit and its hours and cod price against the town's files and the research note, AB2's ratio against P2's measured edges, the slot against the kerb, stallriser, pilaster, awning, doorway and the cast's spot, and the scene's old line against the 0.68 m walking width). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
