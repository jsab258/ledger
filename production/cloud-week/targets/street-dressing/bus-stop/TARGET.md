# Quay Street's bus stop with its timetable: the exact target

**The bus stop is a 76 mm pole 3.0 m high (black foot, white length, black top, a concrete collar) carrying an old-style enamel flag 300 x 285 with BUS and STOP in two lines and a black border, and below it a dark-green timetable case 260 x 875 x 60 whose window holds one 200 x 470 card: the fictional Weighhouse Motor Services, services 4, 9 and 12 to stops that are on the town's own map; it stands on the west pavement at x 46.0 (the cast's stop) 0.50 m behind the kerb, with no shelter, its flag and case facing the bus; it replaces the 29 September script's flag and case; no 1975 to 1995 photograph of a stop was measurable, so the proportions are measured on a 2018 photograph of an old-style stop and the absolute sizes are judged (the plate's width sets the scale).**

Cloud week 42, unit 13, family 2. Written 13 October 2026, not yet reviewed. `SELF-CHECK bus-stop: 105 checks, 105 passed, 0 failed; negative controls 28 of 28 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the front faces -y; pivot at the base's centre on the ground; the .glb is metres). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` and `photo_measurements.json` (the pixel measurements), `target_drawing.py` (draws target.json alone: `target_drawing.json` and pictures), `self_check.py` (checks and negative controls), `make_previews.py` (preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/bus-stop/`: p1 (S1 cropped, the card's print blurred) and its target-on-photo overlay.
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`, `../sd_photo.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | no cars until real; skip and pallets off until real; the KX100 phone box stays | not a car, skip or pallet; the kiosk is another unit; the stop is the town's own furniture |
| RULINGS 3 Oct (sources order) | free assets that fit first (Poly Haven, ambientCG, CC0), else our own in Blender from real photographs | no free model (S6: no bus stop in 521 Poly Haven models); so own work by script, from S1's photograph |
| content rule (canon D18) | what the rule forbids is out of image and text | nothing the rule forbids on the case or card: the stops are streets and landmarks of the town (a seaside pier, a market hall, a works); the data scan finds none |
| NoAI and licences | nothing marked NoAI; photographs only free licences, for measuring, never placed in the game or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure and look at; no NoAI source; nothing is placed or traced |
| RULINGS 1 Oct, 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening grime | black, off-white and green: no saturated colour except the case's faded green; grime and chips are the strategy |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the stop has no light of its own |
| RULINGS 8 Oct | photographs win over books, element by element | see 'Where the photographs win' |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |
| canon (brands) | every brand fictional; no real operator, council or maker | the operator is Weighhouse Motor Services, a placeholder named for a minted street; no logo; the routes and stops are the town's own (atlas.json) |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/5668101 | 2026-10-13 | Jaggery | CC BY-SA 2.0 (read on the page) | 2018-01-16 | an old-style bus stop in a Cotswold village: an enamel flag with BUS STOP in two lines on a black pole with white bands, a dark-green timetable case with a clear window (blank upper half, a paper card in the lower half) clamped below the flag; the foot is in shadow | YES | any absolute size (no scale object; the flag's width is assumed), the colours (a winter evening, strong shadow), the ground | 2018 photograph of a sign of an older type that was still in use in 1990 (a Gloucestershire village stop; the type is far older than 1990) |
| S2 | https://www.geograph.org.uk/photo/1981245 | 2026-10-13 | Rob Candlish | CC BY-SA 2.0 (read on the page) | 2010-07-25 | a stop pole with a tall case holding two printed timetables stacked and a notice; shows how a card fills a case and how text blocks stack | YES | any number; the operator's logo and the notice's wording (real marks, not copied) | 2010; the paper-in-a-case idea is older |
| S3 | https://www.geograph.org.uk/photo/4340832 | 2026-10-13 | Jaggery | CC BY-SA 2.0 (read on the page) | 2015-02-05 | a plain black pole in a terraced street with a small flag plate with a bus pictogram and a two-line text; shows how a stop sits against a kerb in a street of houses | no | everything (looked at; the plate is of a later type) | 2015 |
| S4 | production/art/atlas-01/data/atlas.json and production/specs/hook-cast.json (this repository) | 2026-10-13 | this project | own work | n/a | the town's roads and landmarks (Weighhouse Lane, Tannery Row, Civic Rise, Sea Road, Market Hall, Retort works, Winter Rooms, Short pier) and the cast's bus stop at x 46.0, z -4.3 on the west pavement | YES | the stop's design | n/a |
| S5 | tools/meshgen/blender/clutter/bus_stop.py, production/research/street-clutter-1990 (this repository) | 2026-10-13 | this project | own work | 29 September 2026 | an earlier scripted stop: a 3.0 m 76 mm pole, a 450 x 375 flag of diagram 970, a grey case at eye height | YES | its flag and case (they disagree with S1) | n/a |
| S6 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | no bus stop, bus shelter or timetable model; the nearest is a wet-floor sign and two chalkboards | no | everything: so the stop is made by script | n/a |
| S7 | https://api.geograph.org.uk/syndicator.php (terms bus stop, bus shelter, bus stop timetable, bus stop sign, bus stop pole, each with takenyear 1975 to 1996) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | about 100 photographs of 1975 to 1996 with a bus or a stop in them; the nearest to a close view of a stop is a Belfast flag of 1990 (a different country's operator flag, with a real logo) and a 1996 supermarket stop that shows a person and a real brand; none was measurable and none is used | no | measuring | n/a |

What was searched: Geograph's feed for `bus stop`, `bus shelter`, `bus stop timetable`, `bus stop sign`, `bus stop pole` with each year 1975 to 1995 (about 100 candidates; no measurable close view). Wikimedia Commons was not asked. The hobby pages for the bus flag standard were not reached (the standards' text is not in the repository; the 450 x 375 figure rests on the research note alone and is not used).

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| tools/meshgen/blender/clutter/bus_stop.py (29 Sep) and its model on F: | a 3.0 m 76 mm pole, a 450 x 375 diagram-970 flag, a grey case | MENDED: the pole (76 mm, 3.0 m) is kept; the flag and the case are REPLACED | S1 shows an older plate and a taller green case (W1, W2, W3) |
| production/research/street-clutter-1990 item 5 | the flag and pole as a research item | KEPT for the pole's size | its flag size is unverified and not used |
| production/specs/hook-cast.json: bus_stop at x 46.0, z -4.3 | the cast's stop | KEPT as the slot | no scene line exists, so this target adds one |
| production/cloud-week/targets/litter-bins (B3, the hooded drum, at x 44.0 west) | a hooded bin beside the stop | KEPT, read by the self-check | the asset plan puts a bin at the stop |
| Poly Haven models, git branches (git log --all for bus stop, timetable) | nothing relevant | none to reuse | S6; only the 29 September commit |

## The target

Axes: x across the flag (right is +x seen from the front), y from the front (-y, towards the bus) to the back (+y), z up from the paving at the pole's centre. Every part is a box or a cylinder; the self-check measures every number back off the parts.

### Assembly in words

- **The pole**: a 76 mm steel tube, black from the paving to 554, white from 554 to 2118, black to the top at 3000, with a plug cap 8 mm high; a concrete collar r 95, 22 high, round the foot.
- **The flag**: a 300 x 285 x 3 enamel plate on two flat galvanised clamps (two bolts each), its top at 3000 and its lower edge at 2715; the border 12 wide and 2 mm raised, corners r 20, the edge rolled back 4 mm; BUS over STOP in black capitals 62 mm tall; the plate faces -y.
- **The case**: four folded dark-green bars 20 wide and 60 deep make a frame 260 x 875 from 1008 to 1883, a 6 mm back sheet against the pole, a 2 mm clear sheet in the front rebate and, behind it, one printed card 200 x 470 held low in the window (its lower edge 40 above the frame's bottom); a round lock head on the right bar 400 above the foot; two clamp straps round the pole at the case's top and bottom.
- **Edges and fixings**: tube ends square; bar corners r 4; the plate's rolled edge; clamp bolts 10 mm hex heads (Judgement); the card is held by the sheet, no fixings.
- **The timetable** is data (text.services): three services, each with its stops and minutes from the stop, Mondays to Fridays, Saturdays and Sundays as a first time, an interval and a last time.

### Parts, variant BS1: BS1: pole, old-style flag and timetable case (the sample) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| pole_foot | cyl | paint_black | -38 to 38 | -38 to 38 | 0 to 554 |  | 76 mm steel tube, black lower part |
| pole_white | cyl | paint_white | -38 to 38 | -38 to 38 | 554 to 2118 |  | white-painted length, hidden behind the case between its ends |
| pole_upper | cyl | paint_black | -38 to 38 | -38 to 38 | 2118 to 3000 |  | black upper length carrying the flag |
| pole_cap | cyl | paint_black | -40 to 40 | -40 to 40 | 3000 to 3008 |  | plug cap, 8 mm, slightly proud of the tube |
| pole_collar | cyl | concrete | -95 to 95 | -95 to 95 | 0 to 22 |  | a small concrete collar round the foot, 22 mm proud of the paving |
| flag_plate | box | enamel_white | -150 to 150 | -48 to -45 | 2705 to 3000 | corners r 20, edge rolled back 4 mm | old-style enamel plate, 3 mm steel |
| flag_border_top | box | enamel_black | -138 to 138 | -50 to -48 | 2976 to 2988 |  | black border 12 wide, 2 mm raised |
| flag_border_bottom | box | enamel_black | -138 to 138 | -50 to -48 | 2717 to 2729 |  |  |
| flag_border_left | box | enamel_black | -138 to -126 | -50 to -48 | 2729 to 2976 |  |  |
| flag_border_right | box | enamel_black | 126 to 138 | -50 to -48 | 2729 to 2976 |  |  |
| flag_clamp_top | box | galvanised | -34 to 34 | -48 to -36 | 2930 to 2950 |  | flat clamp bracket, two bolts |
| flag_clamp_bottom | box | galvanised | -34 to 34 | -48 to -36 | 2735 to 2755 |  |  |
| case_bar_top | box | case_green | -130 to 130 | -98 to -38 | 1863 to 1883 | corners r 4 | case frame 20 wide, 60 deep, folded sheet |
| case_bar_bottom | box | case_green | -130 to 130 | -98 to -38 | 1008 to 1028 |  |  |
| case_bar_left | box | case_green | -130 to -110 | -98 to -38 | 1028 to 1863 |  |  |
| case_bar_right | box | case_green | 110 to 130 | -98 to -38 | 1028 to 1863 |  |  |
| case_back | box | case_green | -110 to 110 | -44 to -38 | 1028 to 1863 |  | back sheet, 6 mm with its lining |
| case_glass | box | glass | -112 to 112 | -98 to -96 | 1026 to 1865 |  | 2 mm clear sheet in the front rebate (acrylic) (transparent) |
| case_card | box | paper | -100 to 100 | -96 to -96 | 1048 to 1518 |  | the printed timetable card, 200 x 470, behind the sheet (film) |
| case_lock | box | galvanised | 112 to 124 | -104 to -98 | 1408 to 1420 |  | a round lock head on the right bar, 12 mm |
| case_strap_top | cyl | galvanised | -41 to 41 | -41 to 41 | 1859 to 1871 |  | stainless clamp strap round the pole, 12 wide |
| case_strap_bottom | cyl | galvanised | -41 to 41 | -41 to 41 | 1020 to 1032 |  |  |

### Parts, variant BS2: BS2: pole and flag without a case (a second stop elsewhere; not placed today) (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| pole_foot | cyl | paint_black | -38 to 38 | -38 to 38 | 0 to 554 |  | 76 mm steel tube, black lower part |
| pole_white | cyl | paint_white | -38 to 38 | -38 to 38 | 554 to 2118 |  | white-painted length, hidden behind the case between its ends |
| pole_upper | cyl | paint_black | -38 to 38 | -38 to 38 | 2118 to 3000 |  | black upper length carrying the flag |
| pole_cap | cyl | paint_black | -40 to 40 | -40 to 40 | 3000 to 3008 |  | plug cap, 8 mm, slightly proud of the tube |
| pole_collar | cyl | concrete | -95 to 95 | -95 to 95 | 0 to 22 |  | a small concrete collar round the foot, 22 mm proud of the paving |
| flag_plate | box | enamel_white | -150 to 150 | -48 to -45 | 2705 to 3000 | corners r 20, edge rolled back 4 mm | old-style enamel plate, 3 mm steel |
| flag_border_top | box | enamel_black | -138 to 138 | -50 to -48 | 2976 to 2988 |  | black border 12 wide, 2 mm raised |
| flag_border_bottom | box | enamel_black | -138 to 138 | -50 to -48 | 2717 to 2729 |  |  |
| flag_border_left | box | enamel_black | -138 to -126 | -50 to -48 | 2729 to 2976 |  |  |
| flag_border_right | box | enamel_black | 126 to 138 | -50 to -48 | 2729 to 2976 |  |  |
| flag_clamp_top | box | galvanised | -34 to 34 | -48 to -36 | 2930 to 2950 |  | flat clamp bracket, two bolts |
| flag_clamp_bottom | box | galvanised | -34 to 34 | -48 to -36 | 2735 to 2755 |  |  |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | pole length above the paving to the cap's top | 3008 mm | Judgement | a 3.0 m stop pole (the repository's research note and the 29 September script agree; P1's span flag top to foot gives 3.0 m only if the plate is 300 wide); error 150 mm | +-150 |
| N2 | pole diameter | 76 mm | Judgement | 76 mm (3 inch) tube, the standard stop post; P1's pole is 7 to 8 px wide = 50 mm at 6.56 mm per px which is too coarse to read, so the standard is kept (+-10) | +-10 |
| N3 | flag plate width | 300 mm | Judgement | assumed 300 mm: it sets P1's scale (6.56 mm per px); P1 flag_left 526.0 to flag_right 571.7 = 45.7 px | +-30 |
| N4 | flag plate height | 285 mm | Photo | P1 flag_top 70.6 to flag_bottom 117.1 (46.5 px, includes the yellow lichen and clamp below the plate) at 6.56 mm per px = 305; the plate itself 285 (+-25) | +-25 |
| N5 | case height | 875 mm | Photo | P1 case_top 240.8 to case_bottom 374.2 (133.4 px) at 6.56 mm per px; error 60 | +-60 |
| N6 | case bottom above the paving | 1008 mm | Photo | P1 case_bottom 374.2 below flag_top 70.6: 303.6 px = 1992 mm below the flag's top at 3000 (+-130) | +-130 |
| N7 | case top above the paving | 1883 mm | Photo | P1 case_top 240.8: 170.2 px below the flag's top = 1117 mm; error 130 | +-130 |
| N8 | case width | 260 mm | Judgement | P1 case x 535 to 577 = 42 px = 275 mm by eye (low contrast, not measured by the algorithm); 260 kept for an A3-card case (+-35) | +-35 |
| N9 | case depth (from the pole's front face) | 60 mm | Judgement | typical stop case 60 mm; not measurable on P1 (+-20) | +-20 |
| N10 | flag bottom above the paving | 2705 mm | Photo | P1 flag_bottom 117.1 below the top: 46.5 px = 305 mm; the plate's own bottom edge at 2715 (+-30) | +-30 |

### Photograph measurements (P1, S1)

each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band; the scale is fitted on the one span from the flag plate's top edge to the case's lower edge (303.6 px); the plate's width is the unit that sets 6.56 mm per px (Judgement), so the absolute sizes are judged within the stated errors and the photograph checks the proportions; case sides were too faint to measure; the band-2 foot (the white band's lower end) has a spread of 3.6 px; the tolerance is the measured spread times 3 plus 2 px, at least 5 px (33 mm).

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P1 | flag_top | y | 70.6 | [535, 60, 565, 80] | 5.0 | hi of flag_plate |
| P1 | flag_bottom | y | 117.1 | [535, 100, 565, 120] | 5.0 | lo of flag_plate |
| P1 | case_top | y | 240.8 | [530, 226, 570, 246] | 5.0 | hi of case_bar_top |
| P1 | case_bottom | y | 374.2 | [530, 364, 570, 386] | 5.0 | lo of case_bar_bottom |
| P1 | band2_bottom | y | 443.5 | [538, 430, 546, 456] | 12.7 | lo of pole_white |
| P1 | flag_left | x | 526.0 | [515, 78, 535, 98] | 5.0 | lo of flag_plate |
| P1 | flag_right | x | 571.7 | [565, 78, 590, 98] | 5.0 | hi of flag_plate |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| paint_black | pole black gloss, chalked | 28, 28, 30 | 0.50 (semi-gloss) | not metal | paint over steel, chipped to grey primer at the foot |
| paint_white | pole white, dirty | 214, 212, 200 | 0.55 (semi-matt) | not metal | street-grey, splashed to knee height |
| enamel_white | enamel plate, cream-yellow, dirty | 226, 214, 170 | 0.30 (glossy, crazed) | not metal | vitreous enamel on steel, yellowed with age (P1: cream with a yellow cast), chipped at the bolt holes and edges |
| enamel_black | enamel dark brown-black | 38, 28, 24 | 0.30 (glossy) | not metal | border and lettering |
| galvanised | galvanised steel | 140, 142, 140 | 0.50 (satin) | metal | clamps, straps, lock |
| case_green | case dark green | 44, 66, 52 | 0.50 (semi-matt) | not metal | the 1980s council green, faded to grey-green |
| glass | clear acrylic sheet, scratched | 214, 220, 222 | 0.08 (smooth) | not metal | crazed at the corners, a dirt line along the lower edge |
| paper | timetable card, white paper | 236, 234, 224 | 0.80 (matt) | not metal | black print, a yellowed edge; no operator logo |
| concrete | concrete collar | 128, 126, 120 | 0.90 (rough) | not metal | cracked at the pole |

### Wear

- the pole's paint is chipped to grey primer within 300 mm of the paving (kicks, bicycle pedals); the lowest 120 mm has a dark splash line; the white band is street-grey
- scraps of old sticker and tape on the pole between 1.2 and 1.6 m, never legible; a few dog marks at the foot (nothing else at the foot)
- the flag plate: chips at the bolt holes with rust runs 30 to 80 mm long, a bent corner, a patch of yellow-green lichen and bird lime along its lower edge and clamp (P1 shows yellow lichen under the plate), the plate off square by 2 to 3 degrees (the sample's lean; BS1 is built square and the lean is a seed)
- the case: green faded to grey-green on its top bar, a dirt line along the window's lower edge, two fine scratches on the sheet, one cracked corner of the sheet in the worn variant, the card yellowed at the edges with its top corner curled
- NOT shown: any advertisement on the case, any person, any drink, any real operator's logo

### Variants the street needs

- BS1 (the sample): pole, old-style flag, timetable case. One on the street.
- BS2: pole and flag only (no case), the same pole and flag: for a second stop if the town wants one (none today).
- conditions (materials): C0 sound; C1 worn (the sample's wear); C2 flag knocked 3 degrees off square with a bent corner and a cracked case sheet (a seed, not a mesh).
- timetable cards: T1 as written; T2 the same card yellowed with a curled corner and one service struck through in ink (a mask over T1, never other times).

### Where it stands on Quay Street

**Slot:** west pavement, pole centre at x 46.0 m (the cast's bus stop, hook-cast.json), 0.50 m behind the kerb's back edge (z -3.625), the flag and the case facing -x (south, towards the bus coming up the street); the waiting spot z -4.3 is behind it; no shelter

- the cast already puts the stop at x 46.0, z -4.3 on the west pavement (production/specs/hook-cast.json: 'the bus stop at the top of Quay Street'), and Rita's, the newsagent's and Hal's shop lie below it; the scene file has no stop, so this is a new slot (the 29 September README said the street had none)
- a bus on the west lane travels north (+x) with the kerb on its left; the flag must face the bus coming from the south, so it faces -x; waiting people read the case from the road side of the pole
- no shelter: a shelter is 1.2 to 1.5 m deep and would leave 0.5 to 0.8 m of a 2.0 m footway, under the 1.0 m this target requires behind a pole (the tester's walk found 0.65 m too narrow on 29 September); the stop is a pole with a case
- the litter bin B3 of the litter-bins target (the hooded drum K2) stands at x 44.0 west, z -3.8, 2.0 m from the pole, inside the 3 m the asset plan asks for
- the stop is beyond the west block's end (x 39), so no shopfront is hidden by the pole or the queue

### Lettering and text

- Operator: WEIGHHOUSE MOTOR SERVICES (invented; named for the town's Weighhouse Lane); the stop: QUAY STREET (TOP).
- Card: 200 x 470 mm, margin 10; heading 11 mm capitals; service numbers 16 mm; body 3.6 mm in Liberation Sans (SIL OFL 1.1) with a 4.6 mm line pitch; times as four digits on the 24-hour clock.
- Service 4: Quay Street (top) +0, Weighhouse Lane +6, Market Hall +11, Civic Rise +19. Quay Street (top) departures: Mondays to Fridays 0710 then every 20 minutes until 1750; Saturdays 0750 then every 30 minutes until 1750; Sundays no service.
- Service 9: Quay Street (top) +0, Tannery Row +5, Retort Works +14. Quay Street (top) departures: Mondays to Fridays 0710 then every 30 minutes until 1710; Saturdays 0750 then every 60 minutes until 1350; Sundays no service.
- Service 12: Quay Street (top) +0, Sea Road +7, Winter Rooms +15, Short Pier +18. Quay Street (top) departures: Mondays to Fridays 0900 then every 60 minutes until 1700; Saturdays 0900 then every 60 minutes until 1800; Sundays 1100 then every 120 minutes until 1700.

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | the flag | the 29 September script and the research note: a 450 x 375 plate of diagram 970 (a bus pictogram over a Bus Stop panel) | S1: an old-style enamel plate, about 300 wide, two lines BUS and STOP, a black border, a rolled edge; S3 shows the later pictogram type on a street of houses | the S1 plate as the sample; the diagram-970 plate is a later flag and not written (a variant if the street wants a second stop) |
| W2 | the case | the script: a grey case with a perspex window at eye height | S1: a dark-green framed case, tall (about 875 mm), with a blank upper half and the paper card in the lower half, its foot at about 1.0 m | the S1 case: green, 260 x 875 x 60, the card low in the window |
| W3 | the pole's paint | the script: one galvanised grey tube | S1: black tube with a white band above the case and below it, black foot | black foot to 554, white 554 to 2118, black above |
| W4 | the collar | none | S1's foot is in shadow and S2/S3 show the pole entering the paving with a small collar | a 22 mm concrete collar r 95 (Judgement) |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: pole length above the paving to the cap's top | measure it on the built mesh in millimetres (bbox) | 3008 mm | +-150 mm |
| N2: pole diameter | measure it on the built mesh in millimetres (extent) | 76 mm | +-10 mm |
| N3: flag plate width | measure it on the built mesh in millimetres (extent) | 300 mm | +-30 mm |
| N4: flag plate height | measure it on the built mesh in millimetres (extent) | 285 mm | +-25 mm |
| N5: case height | measure it on the built mesh in millimetres (span) | 875 mm | +-60 mm |
| N6: case bottom above the paving | measure it on the built mesh in millimetres (edge) | 1008 mm | +-130 mm |
| N7: case top above the paving | measure it on the built mesh in millimetres (edge) | 1883 mm | +-130 mm |
| N8: case width | measure it on the built mesh in millimetres (extent) | 260 mm | +-35 mm |
| N9: case depth (from the pole's front face) | measure it on the built mesh in millimetres (extent) | 60 mm | +-20 mm |
| N10: flag bottom above the paving | measure it on the built mesh in millimetres (edge) | 2705 mm | +-30 mm |
| C1: no part floats | the contact graph of the meshes (touching within 2 mm) | all parts reach the ground | 0 floating |
| C2: the flag plate is closed from the front, square on and leaning | rays at the plate face at 0, 30 and 45 degrees | 0 get through | exact |
| C3: the card lies inside the case's window | the card's box inside the clear sheet's box | inside | exact |
| C4: the card has no logo and carries exactly the services of text.services | the card texture's text | services 4, 9 and 12 as written | exact |
| C5: the stop stands where the placement says | pole centre against the placement | x 46.0, z -3.625 | +-50 mm |

### For the builder

- pole: three tubes (black, white, black) of 76 mm and a cap; the paving collar is a short cylinder; weld the three tubes into one mesh with one material id each
- flag plate: 3 mm with corners r 20 and the edge rolled back 4 mm; the border and the two lines of capitals are texture on the plate, not meshes; the border strips in the parts table are the raised edge's guide (2 mm)
- case: four folded bars (60 deep), a 6 mm back sheet, a 2 mm clear sheet, the card 4 px per mm (800 x 1880 px) with the text from text.services set in the stated font; the card has no logo
- orientation: the local -y faces the bus (towards -x in the street's frame, yaw 90 degrees)

## Owed to Jafar's page (one line each, with a recommendation)

None.

## What the target could not settle

- absolute sizes: S1 has no scale object, the plate's width (300 mm) is assumed and sets 6.56 mm per px; every size from S1 is Judgement within the stated error (the flag's height, the case's height and its height above the paving, the white band's lower end)
- the case's width and depth (the sides were too faint to measure; 260 wide and 60 deep are typical)
- the 1990 flag type on the real street (S1's old enamel plate or the pictogram plate of S3): either is period; S1 is chosen because a photograph exists
- the real timetable's look (S2 is 2010 and carries an operator's logo, so only its stacking of text blocks is used)
- whether Quay Street's stop had a shelter in the cast's mind (the cast gives only the stop)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry from target.json and tests: the overall box against the printed numbers; every number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face shot with rays square on and leaning 30 and 45 degrees (fine across one direction and coarse along the other); the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; the family's own rows (the timetable's arithmetic and its stops against atlas.json, the card's capacity, the card inside the window, the stop's slot against hook-cast.json and the bin's slot, the clear footway behind the pole). `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each negative control is a deliberately wrong copy that must make its named row fail.
