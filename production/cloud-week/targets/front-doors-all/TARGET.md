Front doors for every house kind of Quay Street: from the passed 3.1 door (T1 cottage four-panel, F1 flat four-panel, its bell push fixed to one plain dark oblong), 10 door kinds (cottage T1 T2 T3, flat F1 to F7) fitted to the street's 12 household doors by house, 8 furniture slots with 28 variants (letter plates, handles, rim night latches, plugged keyholes, knockers, bells, numbers, a boot scraper), 15 paints and 3 conditions, a street order in which no two neighbours match, and a gate of 7 views a kind plus the street rows. Self-check: --live --previews: 716 pass, 0 fail; negative controls (wrong copies, offline rows) 83 of 83 caught; live controls (wrong copies, live rows) 17 of 17 caught.

# Front doors for every house kind: the target (cloud week 42, unit 9)

Files in this folder: `TARGET.md` (this), `target.json` (the same numbers: frame sets, 10 kinds, the furniture, paints, wear, the street's house table, the gate and 162 checks, with the self-check result), `target_drawing.py` (draws target.json alone: an elevation of each kind in the 3.1 frame, the sections, the street's rows; `OUT_DIR [--json F] [--overlay KIND PHOTO OUT BOX]`), `self_check.py` (`--live --previews --photos DIR --write`), the makers (`td_data.py`, `td_kinds.py`, `td_furn.py`, `td_checks.py`, `td_sites.py`, `td_photos.py`, `make_target.py`, `make_doc.py`, `make_previews.py`) and `pages_read.json`. Run with `/home/user/.bpyenv/bin/python`. Previews: `production/previews/cloud-week/refs/front-doors-all/`.

Units and axes as the 3.1 target: millimetres; frame x across the opening from the left reveal, z up from the top of the threshold; leaf u across from the leaf's left edge seen from outside, v up from its bottom. The leaf laps behind each stop and behind the transom by 20.4 mm, so a photograph's visible face is the leaf less that lap: `u_structural = 20.4 + fraction x visible width`, `v = fraction x visible height` (visible T 772 x 1927.6, F 797.2 x 1960.6). Kinds of number: Read (printed), Scaled, Photo (with its box and error), Derived, Judgement.

## 1. What was asked, and what is reused

Jafar, 12 October: "Front doors for every house kind, from the 3.1 door with its bell push fixed, with door furniture variants." The 3.1 door is built and passed (try 2, one narrow point): `production/cloud-week/targets/front-door/` (target and photographs), `production/cloud-week/kit/door/` (build_door.py, departures.py, check_door.py, views, NOTES.md, the reviews), `production/assets/cloud-week/door/door_T1.glb` and `door_F1.glb`, HANDOVER.md row 3.1. Every number taken from 3.1 here is its target.json with `departures.py` applied (the build's moulding widths 46 and 43, the collar standing 5.0 proud, the vertical keyway): the self-check re-reads both and fails on a difference.

The handover's fix is the first line of the work: **delete the parts `iron_bellpush_bezel` and `iron_bellpush_button` from door_T1 (rebuild without them) so a plain dark oblong remains.** The two-part push read as a modern video doorbell (the 3.1 close review). The only bell push in this target is BL1, one part, 22 x 72.6 x 3 proud, square-cornered (radius at most 1), a 14 x 2 groove 1 deep a little below its middle (the darker band P1 shows), no bezel, no button, no ring, no bright element; it is on T1 only. Checks BP-form, BP-none-elsewhere, BP-no-modern and BP-houses hold it, and the negative controls build a push with a bezel, a push on F1 and a brass push to prove they fail.

The new kinds are made from 3.1's script and method: the frame sets T (the cottage's brick opening, cambered head, transom 65, step) and F (the flat's side slot, flat head at 2400, transom 102, jambs showing 49) are 3.1's unchanged (every kind, F6 included, stands in one of them: the stops in front of the leaf, an inward-opening door); the leaf is rebuilt per kind from the same members (stiles 114.3, rails, 1.6 mm margins, panels floating in their grooves where there are panels); the fittings are 3.1's parts with new places. Section 5 says part by part, kind by kind, what is kept, changed, removed or added and why.

## 2. Sources

| id | photograph and page | read | author, licence | taken | shows | used for |
|---|---|---|---|---|---|---|
| P1 | Front door, 69 Lower Brimley Road, Teignmouth, front-door target (3.1) | 13 Oct 2026 (preview only (3.1's page not reachable then)) | Robin Stott, CC BY-SA 2.0 | 2012-05-06 | 69 Lower Brimley Road: a red four-panel door with bolection mouldings, a lock-rail band, a weatherboard, a white frame with a single-pane transom, a plain dark bell oblong on the right jamb, a brass letter plate and a rim night latch | T1 and F1 (kept), the bell push's plain oblong, the brass plate, the rim night latch |
| P2 | Doorway Philip Lane Tottenham London England, front-door target (3.1) | 13 Oct 2026 (preview only) | Acabashi, CC BY-SA 4.0 | 2024-02-03 | 178 Philip Lane: an unrestored black six-panel door beside a shop, a deep moulded transom with a full round nose, a centre knob, a knurled rim night latch collar, a plugged keyhole, a horizontal brass plate, crazed and chipped paint | F2 six-panel, centre knob, plugged keyhole, wear |
| D1 | Carrville Terrace, https://www.geograph.org.uk/photo/7292055 | 13 Oct 2026 (page opened, file measured) | David M Clark, CC BY-SA 2.0 | 1975-01-22 | two doors in white frames under painted-cement hoods, each with a transom light: a deep teal door of two long panels whose heads are raked, rising toward the muntin (the left panel's top line runs from (47.5, 526.7) to (56.7, 522.9)), and a blue-grey door of four stacked lights with a low letter plate in its bottom rail; a white painted step | F3 two long panels and their raked heads (a rise of 50 mm, Photo, +-25), the low letter plate, the stacked lights (vertical rows only: the leaves are seen at an angle from the right) |
| D2 | Terraced housing in Railway Street, https://www.geograph.org.uk/photo/2238747 | 13 Oct 2026 (page opened, file measured) | P L Chadwick, CC BY-SA 2.0 | 1987-08-09 | a stone terrace: a mustard door of three long narrow lights, its timber door frame and the window frames of the same house painted mustard too; a khaki flush door with a tall slit light, a lever handle and a small plate under the slit (white frame, dark transom), its leaf ending at row 360 above the sill lines (rows 360 to 366 are the sill, not the door); a white door with an oval plaque | F4 three long lights, F5 slit-light flush door, the lever handle, the slit plate; the mustard-painted frames are a finding set against the white-frames ruling (owed line 2) |
| D3 | Terraced House - Ratcliffe Street, Levenshulme, https://www.geograph.org.uk/photo/2321423 | 13 Oct 2026 (page opened, file measured) | Anthony Parkes, CC BY-SA 2.0 | 1994-06-10 | a brick terrace front square on: a white door of four stacked lights with nets, a fanlight with a plain upper pane over a band of crossed diagonal leading (lozenges about 145 mm across) and an upright under each lozenge point, small dark numerals centred on the leaf's top rail, a dark vertical pull handle on the left stile, a small dark two-part fitting on the right (hinge) stile; the leaf's edges lean about 1 px every 40 rows | T2 four stacked lights, the stiles (84 and 58 mm of white), the leaded fanlight, the numerals on the top rail, the bar pull, the small fitting on the hinge stile |
| D4 | Nos. 34, 32 and 30, Frederick Street, Barnoldswick, https://www.geograph.org.uk/photo/689253 | 13 Oct 2026 (page opened, file measured) | Dr Neil Clifton, CC BY-SA 2.0 | 1990-04-10 | three doors of a stone terrace: a pale flush door with a tall slit light, a dark flush door in a white frame about 5.7 px (about 120 mm) wide with a transom and a low plate at its foot, a white moulded door with a small flat-topped dark light (the moulding round it is arched), an oblong letter plate, a short lever at the lock edge, and two moulded panels each with two outlines | T3 moulded modern door, the slit light's height, the low letter plate, an outdoor flush door in a white street frame (the middle door: F6's evidence for a flush face in a street) |
| D5 | Hazlehead I, Provost Graham Avenue (SC 1141987), https://commons.wikimedia.org/wiki/File:Hazlehead_I,_Provost_Graham_Avenue_(SC_1141987).png | 13 Oct 2026 (file page via the Commons API (date 1987, CC BY 4.0, uploaded with the University of Edinburgh); the 1920 px copy was measured) | Miles Glendinning (Tower Block Archive, Edinburgh College of Art), CC BY 4.0 | 1987 | an indoor landing of a tower block (a carpeted landing, a plant on a side table, a large floor number on the wall) and an olive-green flush door in a white lining with an oblong letter plate at its middle, a lever handle on the right stile, a small dark lock under the lever (columns 766 to 771, rows 617 to 626), a spyhole above the plate, a reeded transom and a reeded sidelight | an indoor landing door of a 1960s tower block (Commons description); used for the flush face and its plate, lever, lock and spyhole only (their places as fractions of the face), NOT for the frame, the leaf's width, its stops or its transom: those are Judgement (the street frame F, an inward-opening 838 leaf) |
| D6 | Rensburg Street, Kingston upon Hull, https://www.geograph.org.uk/photo/7982731 | 13 Oct 2026 (page opened, file measured) | Bernard Sharp, CC BY-SA 2.0 | 1982-03-19 | a Hull terrace in 1982: recessed doorways under painted hoods in blue and red, a bright blue door with a white numeral painted on it, a black door with a yellow foot, painted brick surrounds | the bright blue door colour (a box inside the leaf), the painted numeral, the painted hood |
| D7 | Abbey Street, Kingston upon Hull, https://www.geograph.org.uk/photo/3462921 | 13 Oct 2026 (page opened, file measured) | Bernard Sharp, CC BY-SA 2.0 | 1986-06-08 | a street of Hull terraces: arched recessed doorways under rendered arches with the doors standing deep inside; the left reveal's brickwork is painted lime green, the next arch's brick left bare | the recessed doorway and painted reveal (wall kit's, listed in could-not-settle); no door colour is taken from it (the green is the reveal's, not a door) |
| D8 | Brazil Street, Kingston upon Hull, https://www.geograph.org.uk/photo/3462940 | 13 Oct 2026 (page opened, file measured) | Bernard Sharp, CC BY-SA 2.0 | 1986-06-08 | a street of Hull terraces with brightly painted frames, canopies and doors (red, blue, yellow, sky blue) | the finding that these streets paint frames and doors in bright colours, set against Jafar's white-frames ruling (owed line 2); no number taken from it |
| D9 | Newburn Council Houses, https://www.geograph.org.uk/photo/2876894 | 13 Oct 2026 (page opened, file measured) | Kevin Hall, CC BY-SA 2.0 | 1989-08-01 | 1960s council houses with small concrete canopies; the door under the canopy at column 396 is 6 px wide, so the reading is a best reading: half-glazed (its face is pale grey-teal, about 85,122,130, which reads as glass, from row 583 to 619, and turquoise only from row 621 to 640) | the council turquoise: the hue of the lower panel only (a box inside the leaf); not evidence of a flush door |
| D10 | Old Town, Poole: in search of the boot scraper, https://www.geograph.org.uk/photo/3911943 | 13 Oct 2026 (page opened, file measured) | Mike Searle, CC BY-SA 2.0 | 2014-03-30 | a cast-iron boot scraper beside a painted step: a straight blade with a notched underside between two end standards with scroll tops | the boot scraper's form (the sizes are Judgement, the photograph has no scale in its plane) |

All photographs are references for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source is used. Each Geograph page was opened by this writer and its title, author, taken date and CC BY-SA 2.0 read there (`pages_read.json`; `self_check.py --live` reads them again). D5 is a Wikimedia Commons file (the Tower Block Archive of Edinburgh College of Art, uploaded with the University of Edinburgh), page read through the Commons API: date 1987, licence CC BY 4.0, author Miles Glendinning; the 1920 px copy served by Commons (`?width=1920`) was measured, the original is 4000 x 2646. **D5 is an indoor landing door** (the file's own description: "View of hallway and door inside one of Hazlehead I blocks"; the frame shows a carpeted landing, a plant and a floor number): it is used for the flush face and the places of the plate, lever, lock and spyhole only, never for a street frame, a leaf width, stops or a transom. D9's door is 6 px wide, so "half-glazed" is a best reading; only its lower panel's turquoise is used. D10 is a later photograph (2014) of a cast-iron fixture left in place since the 19th century; P1 (2012) and P2 (2024) are 3.1's, their previews only (the lab's pages could not be reached then).

Books (public domain by age): Hasluck, Cassell's Carpentry and Joinery (1907), pp.312-317, Figs. 1015-1039 (ledged and braced doors), read as the OCR text from archive.org, page images not opened; Ellis (1902) and Riley (1905) only through the 3.1 target.

Repository files read: canon.md and RULINGS.md (section 11), `production/specs/vignette-scene.json`, `production/specs/vignette-pieces.json`, `production/assets/street/quay-street.json`, `tools/art-recipes/terrace-front.py` (the street's doors, derived live by `td_sites.py`), `production/cloud-week/targets/SCENE-SLOTS.md`, the house-windows target (which houses were modernised), the wear target and `production/cloud-week/2d/wear/NOTES.md`, the Hook sheet (`production/reference/hook-sheet.png`: dark doors in white surrounds, a blue-grey shop door, a cream house; no household door is large enough in it to measure).

**Dating.** Photographs D1 to D9 were taken between 1975 and 1994, as stated on their pages; all show the period object. D3's door is a 1930s type kept in 1994; D4 is black and white; D2, D6 to D9 are slides whose colour shifts, so no paint value is taken from a photograph except as a hue family (section 8).

**Unreached or not usable.** Geograph's search page refuses the session (its syndicator feed does not); Commons' API answered 429 repeatedly and its text search returned nothing usable for doors, so only the Hazlehead file and one category listing were used; no photograph of a knocker, bell pull, wired glass, frosted door glass, black iron plate or a ledged service door of these streets was reached. A search summary is a lead, never a number.

## 3. The house kinds: every household door of the street

From `tools/art-recipes/terrace-front.py plan_street` (the drawn street; `td_sites.py` re-derives it) with `vignette-scene.json` and `vignette-pieces.json`. The files give each household door a leaf 0.838 x 1.981 m (SCENE-SLOTS: the imperial 2 ft 9 in x 6 ft 6 in; the parade's drawn leaf is 766 between 36 mm casings, the cottages' 678 between 80 mm casings; head casing to 2.117 above the footway in the parade, 2.161 in the cottages; the cottages stand on a stone step 998 x 352.5 x 70 mm; the stand-in letter plate is 250 x 40 at 1.0 m). The scene's coarse side doors (`east_parade_sidedoor0..5`, `west_south_door0..2`, `west_north_sidedoor0..2`, `east_chandler_sidedoor0`) have the same sizes; the drawn street omits east_parade_bay5's side door (the grocer's flat is reached from the rear yard).

**The house kinds.** (1) The plain terraces across from Mickey's: three cottages whose doors open onto the footway over a stone step (frame set T). (2) The flats' side doors beside the shops: five in the parade (bay 2 is the shopfront kit's own door with a fanlight), the chandler's, and three in the west shop row, which the drawn street makes one storey (frame set F). (3) The modernised houses: those the windows target gave replacement windows (east_parade bays 2 and 4, the chandler's flat, the cottage west_south bay 1); they may take a modern door (T3, F5, F6). (4) Council-owned: none; no file names a council house on Quay Street, so the council-style flush door F6 goes on a modernised flat. (5) The yard slot between the west blocks (x 21 to 24) is a gap in the data with no door piece; any gate there belongs to the gate family. (6) The hill's 12 doors (backdrop rows e, w, x, seen at 44 m and more) take kind and paint only.

| house | side, door centre x (m) | trade | the files' opening (mm) | kind | frame | paint | condition | fittings | windows |
|---|---|---|---|---|---|---|---|---|---|
| east_parade_bay0 | east 3.77 | Mickey's, the minicab office (the quay end of the parade) | 838, leaf 766 x 1981 | F1 | F | maroon | tired | plate LP1, handle HD1, latch LK2, keyhole KH1 |  |
| east_parade_bay1 | east 9.77 | the fishmonger | 838, leaf 766 x 1981 | F2 | F | black | kept | plate LP2, handle HD1, latch LK2, number NM1, keyhole KH1 |  |
| east_parade_bay2 | east 20.18 | Rita's, the pawnbroker | 844, the kit's | F1 | F | navy | kept | plate LP1, handle HD1, latch LK2, keyhole KH1 | modernised |
| east_parade_bay3 | east 21.77 | the empty unit to let | 838, leaf 678 x 1981 | F4 | F | brown | neglected | plate LP5, handle HD2b |  |
| east_parade_bay4 | east 32.23 | the launderette | 838, leaf 678 x 1981 | F6 | F | council_turquoise | tired | plate LP4, handle HD2a, latch LK3 | modernised |
| east_chandler_bay0 | east 45.23 | the ship chandler | 838, leaf 766 x 1981 | F5 | F | black | kept | plate LP7, handle HD2b | modernised |
| west_south_bay2 | west 4.50 | a cottage of the plain terraces (quay end) | 838, leaf 678 x 1981, step | T1 | T | navy | tired | plate LP1, latch LK1, bell BL1, number NM1, scraper BS1 |  |
| west_south_bay1 | west 13.50 | a cottage of the plain terraces | 838, leaf 678 x 1981, step | T3 | T | white_gloss | kept | plate LP6, handle HD2c | modernised |
| west_south_bay0 | west 19.50 | a cottage of the plain terraces (by the yard slot) | 838, leaf 678 x 1981, step | T2 | T | maroon | tired | plate LP5, handle HD3, number NM6, keyhole KH1 |  |
| west_north_bay2 | west 24.77 | a shop of the west shop row (by the yard slot) | 838, leaf 678 x 1981 | F7 | F | deep_teal | neglected | handle HD4 |  |
| west_north_bay1 | west 35.23 | a shop of the west shop row | 838, leaf 766 x 1981 | F3 | F | brown (13 Oct, from the try 1 reviews; was dark_green) | tired | plate LP1, handle HD3, number NM3, keyhole KH1 |  |
| west_north_bay0 | west 41.23 | a shop of the west shop row (north end) | 838, leaf 678 x 1981 | F1 | F | dark_green (13 Oct, from the try 1 reviews; was maroon) | kept | plate LP1, handle HD1, latch LK2, keyhole KH1 |  |

Why each house has its kind, paint and fittings:

- east_parade_bay0: Mickey's side door, the four-panel door as built in 3.1 (the recipe already gave it four panels and a knob: a plain slab failed a review on 4 October); maroon is the sheet's deep red.
- east_parade_bay1: the fishmonger's flat, an old six-panel door as P2 shows; kept because a working shop keeps its own door.
- east_parade_bay2: Rita's: the shopfront kit's own side door (a fanlight over it); four-panel as built, dark blue against the cream painted front (the 4 October reading of the sheet's third house).
- east_parade_bay3: the empty unit to let (whitewashed): its flat is empty too; an old three-light glazed door, neglected, with a low plate in its bottom rail.
- east_parade_bay4: the launderette's flat, modernised (the windows target gave it replacement windows): a council-style flush door in the 1980s turquoise of D9's lower panel (D9's own door is half-glazed, a best reading), in the street frame F, an inward-opening 838 leaf; the fittings' places come from D5, an indoor landing door, and an outdoor flush door in a white frame is D4's middle door; the only bright door on the east side.
- east_chandler_bay0: the chandler's flat, modernised (replacement windows, a metal refit below): a flush door with a slit light as D2 and D4 show.
- west_south_bay2: the cottage nearest the quay, four-panel as built in 3.1 with its plain oblong bell push; dark blue; the one boot scraper, by the step (owed: no period photograph shows one here).
- west_south_bay1: the cottage with replacement windows: the white moulded door with a small flat-topped light that D4 shows next to its replacement windows.
- west_south_bay0: the cottage by the yard slot: the 1930s four-light glazed door of D3 with its fanlight (a plain pane over a band of leaded lozenges) and small dark numerals on its top rail; D3's own door is white, but west_south_bay1 beside it is white gloss, and two pale doors side by side break the neighbour rule (paint class), so this door is maroon (its neighbours white_gloss and deep_teal, the doors facing it navy and brown).
- west_north_bay2: beside the yard slot, in a one-storey shop row: a service door to the back passage, ledged and braced, in the sheet's deep teal (owed line 3: if the PC wants flats in this row it takes F1 instead).
- west_north_bay1: a household door in the row: two long panels as D1's left door, a bar pull on the left stile.
- west_north_bay0: the north end of the row: the four-panel door as built.

**The street's order and the neighbours rule.** East side, quay end to chandler: east_parade_bay0, east_parade_bay1, east_parade_bay2, east_parade_bay3, east_parade_bay4, east_chandler_bay0. West side, quay end to north: west_south_bay2, west_south_bay1, west_south_bay0, west_north_bay2, west_north_bay1, west_north_bay0. Neighbours are consecutive doors on a side (east_parade_bay5 has none, so bay 4 and the chandler's are neighbours; the yard slot has none, so west_south bay 0 and west_north bay 2 are). Every neighbouring pair differs in kind, in paint, and in at least 2 of the slots letter plate, handle, latch, number (checks AD-adjacent-east and -west); every pair facing each other within 4.6 m across the street differs in paint class (AD-opposite): east_parade_bay0 / west_south_bay2 (0.73 m); east_parade_bay1 / west_south_bay1 (3.73 m); east_parade_bay2 / west_south_bay0 (0.68 m); east_parade_bay2 / west_north_bay2 (4.59 m); east_parade_bay3 / west_south_bay0 (2.27 m); east_parade_bay3 / west_north_bay2 (3.00 m); east_parade_bay4 / west_north_bay1 (3.00 m); east_chandler_bay0 / west_north_bay0 (4.00 m). A new house takes a kind its frame set allows (cottage frame T: T1 T2 T3; flat frame F: F1 to F7), a paint that is not its neighbours' on the same side nor the paint of a door within 4.6 m across the street, and furniture so that each neighbour differs in at least 2 of the slots letter plate, handle, latch, number. A modernised house (replacement windows) takes T3, F5 or F6 or keeps its old kind. Knockers, bells (except T1's oblong), black iron plates, bell pulls, frosted and wired glass and numerals in black metal are not placed on any house today.

**The hill's 12 doors.** The 12 doors of the hill's rows (backdrop_rise_approach_e0 e1, w0 to w4, x0 to x4) are seen at 44 m and more: leaf kind and paint, nothing else. Door i takes kind BACKDROP_KINDS[i mod 6] and paint BACKDROP_PAINTS[(i + 2) mod 6], so that no two doors of a row, taken in their order, share a kind or a paint. No furniture, no step, no wear mask beyond the foot band. Table: e0 F1 navy; e1 F2 dark_green; w0 F3 brown; w1 F4 deep_teal; w2 T1 black; w3 T2 maroon; w4 F1 navy; x0 F2 dark_green; x1 F3 brown; x2 F4 deep_teal; x3 T1 black; x4 T2 maroon.

## 4. The reading of the photographs, element by element

What the photographs show on a door, and where it is in this target: panel layout and counts (section 5, per kind); mouldings and profiles (T1 F1 F2 the 3.1 bolection at 46 and 43; F3 a stuck ovolo; T3 an embossed step; the rest none); glazing (plain, reeded, leaded; section 5); the fanlight (a plain dark light over D2's doors and D4's; a leaded light over D3's; a reeded light on F6, Judgement; the T and F frames' transoms carry them); the frame and its stops (frame sets T and F); the number (forms NM1, NM3, NM6; the digits are the town's); furniture (section 6); paint and wear (sections 7 and 8). Hoods over the doors, arched recesses and painted reveals (D1, D6, D7) belong to the wall and are listed for the wall kit.

**The brief's door types, and where each is.** Four-panel: T1, F1 (3.1). Six-panel: F2. Two long panels (a 1930s door, D1): F3. Half-glazed: F4 (three long lights over a low rail, D2) and T2 (four stacked lights, D3, D1); half-glazed with a small light: T3 (a small flat-topped light in a moulded panel, D4) and F5 (a tall slit light, D2, D4). A council replacement flush door of the 1970s or 1980s: F6 (the fittings' places from D5, an indoor door; the hue from D9; a flush leaf in a white street frame as D4's middle door). A ledged door to a yard or a service passage: F7 (Hasluck only). A fanlight: every door has one, the frame sets' transom light (plain dark over D2's and D4's doors, leaded over D3's, reeded on F6 as Judgement); a door with no fanlight is not offered, because every door read (D1 to D4, P1, P2) has a light or a panel above its leaf. Glazing: plain (T2, F4, F5, T3, every transom but two), leaded diamond (T2's fanlight), reeded (F6's transom); frosted and wired are listed and placed nowhere. The frame and its stops: frame sets T and F as 3.1 (rebate 22 x 53, stop 74 deep, a 5 x 2.5 stop bead on F), every kind in one of them. Letter plates, knockers, knobs and levers, the rim night latch with its escutcheon (the collar), the bell, house numbers, the boot scraper: section 6.

## 5. The doors, kind by kind

**Covering every opening.** Nothing may show through (check CV): in elevation the frame, the leaf, the glass and the transom cover the clear opening except the 10 mm foot gap and the leaf's 1.6 mm margins; at 60 degrees in plan the leaf laps 20.4 behind each stop and behind the transom's stop (the rows compute the lap from the frame's stop edges and the leaf's edges, and the setback of the leaf behind the stops from their depth), which closes the margin; every leaf lies behind its stops and opens inward; F7's boards are tongued and grooved with a tongue of at least 6 mm; the reveals' returns are the wall kit's (T: buff brick, 3.1 L1 to L5) and the shopfront's pilaster return (F: 24.4 a side); the 3.1 door review's dark hall is the render aid.

### T1: four-panel front door with a transom, in its brick opening (3.1 T1)

Frame set T. Houses: west_south_bay2. Photographs: P1.

Leaf 812.8 x 1948 x 50.8 mm, framed, lock on the right as seen from outside. Members (structural, mm): stile_left 114.30, stile_right 114.30, top_rail 127, bottom_rail 192.80, lock_rail 228.60, muntin 120.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| top_left | panel | 114.3 | 346.4 | 901.3 | 1821 | bolection_outside |
| top_right | panel | 466.4 | 698.5 | 901.3 | 1821 | bolection_outside |
| bottom_left | panel | 114.3 | 346.4 | 192.8 | 672.7 | bolection_outside |
| bottom_right | panel | 466.4 | 698.5 | 192.8 | 672.7 | bolection_outside |

Mouldings: bolection, 46 mm on the face (3.1 as built (departures D7: 46, target 36)).

Profile (d across the face from the moulding's outer edge, h above the framing face, mm): (0,0) (0,3.50) (1.79,5.80) (4.47,6.90) (7.03,7) (9.58,6.40) (13.42,4.60) (18.53,1) (24.28,-4.50) (30.67,-10.50) (37.06,-14.50) (42.17,-16.30) (46,-16.95).

Glazing: transom plain_3mm; leaf none.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_jamb_l/r, frame_head, frame_transom, glass_fanlight, frame_glazing_bead | kept | the passed frame set T and its transom, untouched |
| leaf_frame, panel_*, moulding_bolection_*, moulding_single_*, moulding_band, moulding_weatherboard | kept | passed in 3.1 (fresh reviews of 9 October) |
| iron_letter_plate, flap, lip | kept | LP1, the vertical brass plate |
| iron_lock, collar, plug | kept | LK1, the rim night latch, as built in 3.1 |
| iron_bellpush | changed | rebuilt square-cornered (r 1, was r 6), groove added: the plain dark oblong of P1, one part, 22 x 72.6, 3 proud, with the 14 x 2 x 1 groove a little below its middle; 3.1 built it with r 6 corners and no groove (build_door.py line 664); the handover's fix |
| iron_bellpush_bezel, iron_bellpush_button | removed | the two-part push read as a modern video doorbell (3.1 review v2 close); deleted, not replaced by any ring or lens |
| stone_threshold, stone_riser, stone_tread | kept | the step of 3.1; the wall's plinth returns stay with the wall kit |
| iron_keyhole_*, iron_knob_* | not present | T1 never had them |

### T2: four stacked lights over a low rail, a fanlight with a plain pane over a band of leaded lozenges (D3, D1)

Frame set T. Houses: west_south_bay0. Photographs: D3, D1.

Leaf 812.8 x 1948 x 50.8 mm, framed, glazed, lock on the left as seen from outside. Members (structural, mm): stile_left 94, stile_right 69, top_rail 78.40, bottom_rail 205, bar 30, light_h 393.65.

structural numbers; the visible top rail is 58 (78.4 less the 20.4 behind the transom's stop) and the visible stiles 73.6 (lock side, left) and 48.6 (hinge side, right), which with the 10 mm bead are 84 and 59 of white (D3 reads 84 and 58).

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| light1 | light | 94 | 743.8 | 205 | 598.6 | plain_3mm |
| light2 | light | 94 | 743.8 | 628.6 | 1022.3 | plain_3mm |
| light3 | light | 94 | 743.8 | 1052.3 | 1445.9 | plain_3mm |
| light4 | light | 94 | 743.8 | 1475.9 | 1869.6 | plain_3mm |

Small fitting that is no furniture variant: a small dark two-part fitting on the hinge stile (D3) at u 753, v 1390, 20 x 60 mm, 8 proud, dark (40,40,42). Photo D3 box [116.5, 492.5, 118.5, 498.5]: its centre 2.2 px (22 mm) beyond the glass edge and 4.2 px (42 mm) in from the leaf's right edge, so u about 753 (+-10) on the white of the hinge stile (733.8 to 792.4), v about 1390 (+-15), about 25 x 60 mm. What it is not: not a rim night latch, a bell push, a knocker, a letter plate or a handle (none of those is read on the hinge stile); what it is cannot be told at 10 mm a pixel (a bolt keep or a stop screw): it is added as a small dark box, two parts 20 x 25 mm apart, and no more.

Mouldings: glazing bars 30 wide x 22 deep, square, eased 1 mm; stiles and rails square, eased 1.5; the bead is the 3.1 planted quarter-round 10 x 8 on all four sides of each light.

Glazing: transom leaded_diamond; leaf plain_3mm; white net card behind the lights (D3 shows one), the windows target's net N1 white.

Photograph numbers behind it (measured_fractions_of_leaf_height): {top_rail: 0.036, bar: 0.015, light: 0.203, bottom_rail: 0.106}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_jamb_l/r, frame_head, frame_transom, frame_glazing_bead (transom) | kept | frame set T |
| glass_fanlight | changed | plain 3 mm glass becomes a leaded light as D3 shows it: the upper 144 of the 267 one plain pane; under it a band 83 high of crossed diagonal came at a 145 pitch (lozenges 145 x 83, 5 whole, a tip of a lozenge at each end); a horizontal came 40 above the foot with an upright under each lozenge point; came 6 wide. The T frame's 267 mm light is kept (the wall kit owns the head) |
| leaf_frame | changed | stiles 94.0 (lock side, left) and 69.0 (hinge side, right), visible 73.6 and 48.6, with the bead 84 and 59 of white (D3: 84 and 58); top rail 78.4 (visible 58), bottom rail 205, no lock rail, no muntin; four openings 649.8 x 393.7 with 30 mm bars (D3's fractions of the visible face 0.030, 0.2066, 0.0158, 0.105) |
| iron_numerals (new) | added | NM6: small dark metal numerals 30 high centred on the visible top rail, v 1898.6 (D3; the number is not on the fanlight glass) |
| small fitting on the hinge stile (new) | added | the small dark two-part fitting D3 shows on the hinge stile (T2_hinge_fixing, u 753, v 1390): what it is cannot be told, so it is a small dark box and nothing more |
| panel_*, moulding_bolection_*, moulding_single_*, moulding_band, moulding_weatherboard | removed | a glazed door has no panels or mouldings; D3 and D1 show none |
| glass (new parts glass_light1..4) and bead | added | four panes of 3 mm glass, each with the 3.1 planted bead |
| iron_letter_plate | changed | LP5, a pale low plate in the bottom rail, as D1 and D4 show (the vertical brass plate has no muntin to sit on) |
| iron_lock, collar, plug | removed | no latch cylinder is read on D3's leaf; a bar pull stands in (HD3) |
| iron_bellpush | removed | none on D3 |
| stone_* | kept | the step of 3.1 under the same opening |

### T3: white moulded modern door with a small flat-topped light (D4 right door)

Frame set T. Houses: west_south_bay1. Photographs: D4.

Leaf 812.8 x 1948 x 44 mm, moulded flush sheet over a core, painted-look gloss, lock on the right as seen from outside. Members (structural, mm): border 62.5 (13 Oct, from the try 1 reviews).

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| upper_panel | embossed_panel | 119.9 | 692.9 | 920.5 | 1776.1 | embossed_step |
| upper_panel, inner outline | outline, head segmental, springing 22 below the crown | 182.4 | 630.4 | 996.4 | 1646.2 | a 6 mm step over 6 mm at this line too (13 Oct, from the try 1 reviews) |
| small_light | small_light, head flat, top corners r 20 | 297.4 | 515.4 | 1109 | 1555.2 | plain_3mm |
| lower_panel | embossed_panel | 119.9 | 692.9 | 324.9 | 725.6 | embossed_step |
| lower_panel, inner outline | outline, head flat | 182.4 | 630.4 | 400.7 | 639 | a 6 mm step over 6 mm at this line too (13 Oct, from the try 1 reviews) |

Mouldings: each moulded panel has TWO outlines (D4): an outer and an inner outline, a margin of about 62.5 between them at the sides; the margin is a flat raised border with a quirked (quarter-circle) cove at each line, each step 6 mm deep over 6 mm across (6 mm down at the outer line to the margin, 6 mm more at the inner line to the field, which is 12 below the border face) (13 Oct, from the try 1 reviews); the border is 62.5 wide at the sides; the upper panel's inner outline has a segmental head (crown v 1646, springing 22 lower) under a flat outer top; no applied mouldings.

Profile (d across the face from the moulding's outer edge, depth below the border face, mm) (13 Oct, from the try 1 reviews): (0,0) (0.12,1.17) (0.46,2.3) (1.01,3.33) (1.76,4.24) (2.67,4.99) (3.7,5.54) (4.83,5.88) (6,6) (60,6) (62.5,6) (62.62,7.17) (62.96,8.3) (63.51,9.33) (64.26,10.24) (65.17,10.99) (66.2,11.54) (67.33,11.88) (68.5,12) (110,12).

Glazing: transom plain_3mm; leaf plain_3mm.

Photograph numbers behind it (measured_fractions_of_leaf): {upper: {u: [0.154, 0.941], v: [0.478, 0.921]}, upper_inner: {u: [0.243, 0.852], v: [0.517, 0.854]}, light: {u: [0.392, 0.674], v: [0.575, 0.807]}, plate: {u: [0.377, 0.733], v: [0.437, 0.472]}, lower: {u: [0.154, 0.941], v: [0.169, 0.376]}, lower_inner: {u: [0.243, 0.852], v: [0.208, 0.331]}, handle: {u: [0.941, 0.985], v: [0.433, 0.522]}}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_jamb_l/r, frame_head, frame_transom, glass_fanlight, frame_glazing_bead | kept | frame set T; D4's door has a plain dark transom light over it |
| leaf_frame, panel_*, moulding_* | changed | no stiles or rails: one moulded sheet 44 thick with two moulded panels, each with two outlines, and a small flat-topped light (D4, re-measured on the leaf's own face) |
| glass_light (new part) | added | one pane 218 x 446 with a flat head (top corners r 20; the head rises at most 22 mm), glazed from inside with a moulded bead; the arch D4 shows is the moulding round it |
| iron_letter_plate | changed | LP6, a white oblong 270 x 50 in the margin between the panels (D4: 0.45 of the visible height) |
| iron_lock, collar, plug | removed | D4 shows none outside; a small lever HD2c at the lock edge, v 910 |
| iron_bellpush, stone_* | removed / kept | no push; the step of 3.1 stays |

### F1: four-panel flat door (3.1 F1)

Frame set F. Houses: east_parade_bay0, east_parade_bay2, west_north_bay0. Photographs: P2, P1.

Leaf 838 x 1981 x 50.8 mm, framed, lock on the right as seen from outside. Members (structural, mm): stile_left 114.30, stile_right 114.30, top_rail 127, bottom_rail 192.80, lock_rail 228.60, muntin 120.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| top_left | panel | 114.3 | 359 | 901.3 | 1854 | bolection_outside |
| top_right | panel | 479 | 723.7 | 901.3 | 1854 | bolection_outside |
| bottom_left | panel | 114.3 | 359 | 192.8 | 672.7 | bolection_outside |
| bottom_right | panel | 479 | 723.7 | 192.8 | 672.7 | bolection_outside |

Mouldings: bolection, 43 mm on the face (3.1 as built (departures D8: 43)).

Profile (d across the face from the moulding's outer edge, h above the framing face, mm): (0,0) (0,3.50) (1.43,5.80) (3.58,6.90) (5.63,7) (8.21,6.40) (11.88,4.60) (16.76,1) (22.25,-4.50) (28.35,-10.50) (34.45,-14.50) (39.34,-16.30) (43,-16.95).

Glazing: transom plain_3mm; leaf none.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| everything of door_F1.glb | kept | passed in 3.1 (street and close views); the street's F1 is that model, unchanged |
| iron_knob_*, iron_keyhole_*, iron_lock_* | kept | F1's turned centre knob (HD1), plugged keyhole and knurled rim night latch (LK2) as built |

### F2: six-panel flat door (P2)

Frame set F. Houses: east_parade_bay1. Photographs: P2.

Leaf 838 x 1981 x 50.8 mm, framed, lock on the right as seen from outside. Members (structural, mm): stile_left 101.70, stile_right 101.70, top_rail 96.90, bottom_rail 188.20, lock_rail 205.90, frieze_rail 100, muntin 104.40.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| bottom_l | panel | 101.7 | 366.8 | 188.2 | 505.8 | bolection_outside |
| bottom_r | panel | 471.2 | 736.3 | 188.2 | 505.8 | bolection_outside |
| long_l | panel | 101.7 | 366.8 | 711.7 | 1507.7 | bolection_outside |
| long_r | panel | 471.2 | 736.3 | 711.7 | 1507.7 | bolection_outside |
| small_upper_l | panel | 101.7 | 366.8 | 1607.7 | 1884.1 | bolection_outside |
| small_upper_r | panel | 471.2 | 736.3 | 1607.7 | 1884.1 | bolection_outside |

Mouldings: bolection, 43 mm on the face (3.1 F1 as built (P2, 43)).

Profile (d across the face from the moulding's outer edge, h above the framing face, mm): (0,0) (0,3.50) (1.43,5.80) (3.58,6.90) (5.63,7) (8.21,6.40) (11.88,4.60) (16.76,1) (22.25,-4.50) (28.35,-10.50) (34.45,-14.50) (39.34,-16.30) (43,-16.95).

Glazing: transom plain_3mm; leaf none.

Photograph numbers behind it (fractions_of_visible_height): {top_rail: 0.039, small_upper_panels: 0.141, frieze_rail: 0.051, long_panels: 0.406, lock_rail: 0.105, bottom_panels: 0.162, bottom_rail: 0.096}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, glass_fanlight, timber sill | kept | frame set F, the 49 mm jambs, the weathered transom, the sill |
| leaf_frame, panel_*, moulding_bolection_* | changed | six panels (two small, two long, two small) from 3.1's option_six_panel fractions of P2; the same bolection profile at 43 |
| iron_knob_*, iron_keyhole_*, iron_lock_* | kept | the centre knob on the lock rail and the plugged keyhole, at P2's heights (fractions 0.305, 0.606, cylinder 0.546) |
| iron_letter_plate | changed | LP2, the horizontal brass plate 195 x 70 at 0.788 of the height, P2's |

### F3: two long panels (D1 left door)

Frame set F. Houses: west_north_bay1. Photographs: D1.

Leaf 838 x 1981 x 50.8 mm, framed, lock on the left as seen from outside. Members (structural, mm): stile_left 114.30, stile_right 114.30, top_rail 127, bottom_rail 192.80, muntin 120.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| long_l | panel, head raked (50 lower at the outer corner, high toward the right) | 114.3 | 359 | 192.8 | 1854 | stuck_ovolo |
| long_r | panel, head raked (50 lower at the outer corner, high toward the left) | 479 | 723.7 | 192.8 | 1854 | stuck_ovolo |

Mouldings: stuck ovolo, 20 mm on the face (Judgement: D1 shows two long flat panels with narrow lit edges, no bolection).

Profile (d across the face from the moulding's outer edge, h above the framing face, mm): (0,0) (0,1.50) (1.67,2.28) (2.19,3.05) (3.03,3.77) (4.17,4.44) (5.60,5.04) (7.27,5.55) (9.14,5.96) (11.17,6.26) (13.31,6.44) (15.50,6.50) (18,6.50) (20,5.50) (20,0).

Glazing: transom plain_3mm; leaf none.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, glass_fanlight, sill | kept | frame set F |
| leaf_frame, panel_* | changed | no lock rail: the muntin runs the full height between the 127 top rail and the 192.8 bottom rail; two panels 244.7 x 1661.2 (D1 shows no cross rail on this door) |
| moulding_bolection_* | changed | a stuck ovolo moulding 20 wide, 6.5 proud, replaces the 43 mm bolection (D1 shows thin lit edges); each panel's head is raked, 50 mm lower at the stile than at the muntin (D1) |
| iron_letter_plate | kept | LP1 on the muntin, at the 3.1 height 1617 |
| iron_knob_*, iron_keyhole_* | removed | a bar pull HD3 on the left stile (D1 shows a vertical metal strip on that stile) |

### F4: three long narrow lights over a low rail (D2 left door)

Frame set F. Houses: east_parade_bay3. Photographs: D2.

Leaf 838 x 1981 x 50.8 mm, framed, glazed, lock on the left as seen from outside. Members (structural, mm): stile_left 184, stile_right 114.30, top_rail 90.40, bottom_rail 200, bar 36, light_w 155.90.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| light1 | light | 184 | 339.9 | 200 | 1890.6 | plain_3mm |
| light2 | light | 375.9 | 531.8 | 200 | 1890.6 | plain_3mm |
| light3 | light | 567.8 | 723.7 | 200 | 1890.6 | plain_3mm |

Mouldings: bars 36 wide, square; putty fillet on the glass as F1's.

Glazing: transom plain_3mm; leaf plain_3mm; none (D2 shows a dark hall).

Photograph numbers behind it (measured_from_left_edge_mm): {lights: [[183.5, 323.3], [369.9, 521.4], [579.6, 719.4]], bars: [[334.9, 369.9], [533.0, 568.0]], scale_mm_px: 23.3}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, glass_fanlight, sill | kept | frame set F |
| leaf_frame, panel_*, moulding_* | changed | stiles 184 and 114.3 (visible 164 and 93.9), top rail 90.4 (visible 70), bottom rail 200, three lights 155.9 wide with 36 mm bars (D2 at 23.3 mm a pixel: lights 140 to 152, bars 35) |
| glass_light1..3 | added | three tall panes of 3 mm glass, putty fillet as F1's |
| iron_letter_plate | changed | LP5, the low plate in the bottom rail |
| iron_knob_*, iron_keyhole_*, iron_lock_* | removed | a lever HD2b at the left stile |

### F5: flush door with a tall slit light (D2 middle door, D4 left door)

Frame set F. Houses: east_chandler_bay0. Photographs: D2, D4.

Leaf 838 x 1981 x 44 mm, flush, hardboard-faced, lipped, lock on the left as seen from outside. Members (structural, mm): lipping 6.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| slit | slit_light | 329.8 | 539.2 | 870 | 1789 | plain_3mm |

Mouldings: flat painted face; a 1 mm hairline round the lipping; the slit has a 15 mm square timber bead, 4 proud.

Glazing: transom plain_3mm; leaf plain_3mm.

Photograph numbers behind it (measured_fractions_of_leaf): {slit: {u: [0.388, 0.651], v: [0.447, 0.918]}, plate: {u: [0.343, 0.672], v: [0.384, 0.409]}, handle: {u: [0.015, 0.119], v: [0.516, 0.56]}}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, glass_fanlight, sill | kept | frame set F |
| leaf_frame, panel_*, moulding_* | changed | one flush slab 44 thick, lipped; no panels or mouldings |
| glass_slit (new) | added | one pane about 210 x 920 (v 870 to 1789) on the leaf's face (D2: 8.8 x 37.5 px at 24.7 mm a pixel, on the leaf's own box, foot at row 360) |
| iron_letter_plate | changed | LP7, a pale 265 x 50 plate under the slit, centre v 772 |
| iron_knob_*, iron_keyhole_*, iron_lock_* | removed | a lever HD2b at the left edge, v 1048 |

### F6: council-style flush door: a plain flush leaf in the street frame F (fittings placed from D5, an indoor door; the turquoise from D9; a flush face in a white street frame as D4's middle door)

Frame set F. Houses: east_parade_bay4. Photographs: D4, D5, D9.

Leaf 838 x 1981 x 44 mm, flush, plywood-faced, lipped, lock on the right as seen from outside. Members (structural, mm): lipping 6.

| opening | type | u0 | u1 | v0 | v1 | moulding or glass |
|---|---|---|---|---|---|---|
| spyhole | spyhole | 411.4 | 425.4 | 1491.9 | 1505.9 | lens_14 |

Mouldings: flat face; the lipping line 1 mm; no panel, no moulding.

Glazing: transom reeded_4mm; leaf none.

Photograph numbers behind it (measured_fractions_of_leaf): {plate: {u: [0.342, 0.669], v: [0.452, 0.488]}, handle: {u: [0.843, 0.98], v: [0.455, 0.473]}, lock: {u: [0.968, 0.983], v: [0.421, 0.432]}, spy: {u: [0.446, 0.553], v: [0.757, 0.772]}}.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, sill | kept | frame set F unchanged: the stops stand in front of the leaf, which laps 20.4 behind each stop and the transom (an inward-opening door, hinges inside); the jambs show 49, the visible face is 797.2 x 1960.6; D5's indoor lining is not copied |
| glass_fanlight | changed | reeded 4 mm glass in the transom: Judgement (D5's ribbed light is indoors; no outdoor photograph read shows one) |
| leaf_frame, panel_*, moulding_* | changed | one flush slab 838 x 1981 x 44, lipped (a flush leaf in a white street frame: D4's middle door) |
| iron_letter_plate | changed | LP4, a chrome-look oblong 250 x 70, flush, by D5's fractions of the visible face |
| iron_knob_*, iron_keyhole_* | removed | lever HD2a at the right stile; a spyhole 14 across above the plate (D5, places only) |
| iron_lock_* | changed | LK3, a small dark 18 mm lock face under the lever (D5 columns 766 to 771, rows 617 to 626), by D5's fractions of the visible face |

### F7: ledged and braced service door (Hasluck; no period photograph read)

Frame set F. Houses: west_north_bay2. Photographs: none reached (Hasluck's figures only).

Leaf 838 x 1981 x 47 mm (13 Oct, from the try 1 reviews), ledged and braced matchboarding (boards 22, ledges 25, braces 25), lock on the right as seen from outside. Members (structural, mm): board_w 139.67, board_t 22.

Mouldings: no applied moulding; a V joint 6 wide and 2 deep between tongued and grooved matchboards (profile (d across, h from the face) in target.json).

Boards: edges at u 0, 139.7, 279.3, 419, 558.7, 698.3, 838; ledges (v) 100 to 240; 920 to 1060; 1741 to 1881; nail heads 9 across, 3 proud, one per board at each ledge (18 in all). Read: Hasluck pp.312-317, Figs. 1015-1039: boards 3 to 7 in wide (139.7 mm = 5.5 in used, six across 838), 3/4 to 1 1/4 in thick (22.2 used), grooved and tongued, V joint; ledges nailed with wrought nails driven from the face and clenched; hook-and-plate hinges inside for an inward door. Sizes of ledges, nail heads and leaf: Judgement (no photograph of such a door on these streets was reached).

Glazing: transom plain_3mm; leaf none.

Part by part against the 3.1 door (door_T1.glb, door_F1.glb):

| 3.1 part | status | why |
|---|---|---|
| frame_*, glass_fanlight, sill | kept | frame set F; a service door also takes the transom light |
| leaf_frame, panel_*, moulding_* | changed | six matchboards 139.7 wide, V-jointed, 22 thick, three ledges and two braces behind (not visible), nail heads in rows on the face |
| iron_letter_plate, iron_knob_*, iron_keyhole_*, iron_lock_* | removed | a service door has no letter plate; HD4, a thumb latch, on the lock side |

## 6. Door furniture variants

Every variant with its size, place by kind, material, colour and source. Positions are the fitting's centre in the leaf frame (u, v mm). No real maker's name or mark on any fitting: the lock is a rim night latch.

**letter plate**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| LP0 | none |  |  |  | F7, the service door, has no plate |
| LP1 | brass plate, vertical, on the muntin | [76.0, 242.0] | T1: u leaf centre, v 1617; F1: u leaf centre, v 1617; F3: u leaf centre, v 1617 | brass (181,150,85) | 3.1 as built (P1: 76 x 242, centre 1617) |
| LP2 | chrome plate, horizontal, above the lock rail (13 Oct, from the try 1 reviews) | [195.0, 70.0] | F2: u leaf centre, v 1545 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | 3.1 option_six_panel (P2: 195 x 70 at 0.788 of the height) |
| LP3 | black iron plate, horizontal (reserve, not placed) | [230.0, 60.0] | not placed | cast iron, black (30,30,32) | Judgement: cast-iron plates were common but none is read in a photograph here; listed so a script may place one; the check rejects it on any house today |
| LP4 | chrome-look oblong, flush | [250.0, 70.0] | F6: u 423.3, v 921.1 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | Photo D5 (an indoor landing door: the place only, as fractions of its face): 107 x 30 px at 2.34 mm a pixel = 250 x 70 (the size is Judgement), centre at 0.505 of the face's width and 0.470 of its height |
| LP5 | pale low plate in the bottom rail | [250.0, 50.0] | T2: u leaf centre, v 100; F4: u leaf centre, v 100 | anodised aluminium, pale (190,190,185) | Photo D1 right door (rows 659 to 662.5 of a 150 px leaf: centre 83 above the foot, 46 high) and D4 black door (a 10 x 3 px plate at the foot, 90): centre 100 chosen to sit mid-rail (+-20) |
| LP6 | white plastic oblong in a moulded door | [270.0, 50.0] | T3: u leaf centre, v 876.1 | white moulded plastic (226,224,214) | Photo D4 right door: 12 x 3.1 px at 21.7 mm a pixel = 260 x 67, centre 0.448 of the visible height (+-25) |
| LP7 | small pale plate under a slit light | [265.0, 50.0] | F5: u 424.9, v 772 | anodised aluminium, pale (190,190,185) | Photo D2 middle door: 11 x 2 px at 24.7 mm a pixel = 272 x 49 (+-25), centre v 772 (the review's number; the leaf's own box gives 777) |

**handle**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| HD0 | none |  |  |  | T1, T2's lock side has HD3, F7 HD4 |
| HD1 | turned centre knob on a dished rose | 69.0 | F1: u leaf centre, v 787; F2: u leaf centre, v 598 | black-painted wood, brass cap (35,36,40) | 3.1 as built (P2 8x crop) |
| HD2a | lever handle on a round rose, chrome-look, right stile | [105.0, 18.0] | F6: u 747, v 909.5 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | Photo D5 (an indoor landing door: the place only): lever 45 px = 105 at 2.34 mm a pixel, centre at 0.911 of the face's width and 0.457 of its height, on the right stile |
| HD2b | lever handle on a long backplate 40 x 170 with a keyhole 57 below its centre (13 Oct, from the try 1 reviews), chrome-look, left stile | [100.0, 18.0] | F5: u 73.9, v 1048; F4: u 95, v 1228 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | Photo D2: a small pale handle at the left stile of the middle door, v 1048 (the review's number, 0.535 of the visible height; the leaf's own box gives 1054; +-24); the left door's at about 1228 (+-30) |
| HD2c | short lever on a long backplate 40 x 170 with a keyhole 57 below its centre (13 Oct, from the try 1 reviews), at the lock edge of a moulded door | [80.0, 16.0] | T3: u 757, v 910 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | Photo D4 right door: a dark mark at columns 577 to 578.5, rows 388 to 396, ON the door (the first box lay on the reveal), v 910 (the review's number; the box gives 921; +-32); lever size Judgement |
| HD3 | vertical bar pull on the lock stile: a round grip 19 across on two posts flaring into roses, 30 clear behind the grip (its axis 39.5 off the face) (14 Oct, from the try 2 reviews) | [25.0, 270.0] | T2: u 57.2, v 1236.6; F3: u 67, v 1255 | dark steel (40,40,42) | Photo D3: a dark vertical handle on the left stile, rows 498.25 to 524.25 of a 191.5 px visible leaf = 262 long (+-30), centred on the visible lock stile (u 57.2: the stile is 94.0 structural, 73.6 visible); D1 left door shows a vertical metal strip on its left stile |
| HD4 | thumb latch on a ledged door: a plate with cusped ends, a round bow 19 across on posts 120 apart, 30 clear behind it, a thumb lever 14 x 45 leaving the plate at 75 degrees to the face with a 20 pad (14 Oct, from the try 2 reviews) | [38.0, 190.0] | F7: u 738, v 1000 | dark steel (40,40,42) | Judgement: the usual iron thumb latch for a ledged door; Hasluck draws only the hinges |

**latch**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| LK0 | none |  |  |  |  |
| LK1 | rim night latch, plain collar (the escutcheon), 3.1 T1 | [43.5, 43.5] | T1: u 46.6 from the stop face, right, v 1235 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | 3.1 as built (P1: collar 43.5, 8.4 px) |
| LK2 | rim night latch, knurled collar (the escutcheon), 3.1 F1 | [37.0, 37.0] | F1: u 46.3 from the stop face, right, v 1040; F2: u 46.3 from the stop face, right, v 1070.5 | nickel or chrome-look (196,197,196; 14 Oct, from the try 2 reviews) | 3.1 as built (P2: collar 37, scalloped) |
| LK3 | rim night latch, bare dark cylinder face under the lever, no collar | [18.0, 18.0] | F6: u 798.1, v 836.4 | dark steel (40,40,42) | Photo D5 (an indoor landing door: the place only): a small dark mark under the lever, columns 766 to 771, rows 617 to 626, an 18 mm dark cylinder face at 0.976 of the face's width and 0.427 of its height (the review's u 743, v 845 were on the old 762 x 1981 basis) |

**keyhole**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| KH0 | none |  |  |  |  |
| KH1 | plugged mortice keyhole: a round head over a parallel slot, a dark recess 2 mm sunk (a blind pocket 2.2 deep in the leaf), a pale metal blank filling the slot | [23.0, 32.0] | F1: u 782.8, v 1151; F2: u 782.8, v 1188.1; T2: u 57.2, v 1031.6; F3: u 67, v 1050 (13 Oct, from the try 1 reviews) | dark recess, pale metal blank (60,60,62) | 3.1 as built (P2 5x crop: (493, 447) px, 10 x 14 px = 23 x 32; head 15, slot 8); F1 at 3.1's v 1151, F2 at 0.606 of the visible height (P2) |

**knocker**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| KN0 | none |  |  |  | the default on every house |
| KN1 | ring knocker on a back plate (reserve, not placed) | [70.0, 110.0] | not placed | brass or iron | Judgement: no period photograph read shows a knocker on these streets; the check refuses it on every house today |
| KN2 | plain bar knocker (reserve, not placed) | [150.0, 30.0] | not placed | brass | Judgement, as KN1 |
| KN3 | lion's head knocker [NOT OFFERED] |  | not placed |  | NOT OFFERED: the photographs read (D1 to D9, P1, P2) show no lion's head on any door of these streets; the brief allows one only if they do |

**bell**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| BL0 | none |  |  |  |  |
| BL1 | plain dark oblong push, one part | [22.0, 72.6] | T1: u , v the right jamb's stop face (3.1 as built: x 859.4, z 1120.3 to 1192.9) | dark steel or dark plastic (60,60,62) | Photo P1 16x crop rows 300.3 to 314.4: a dark-grey oblong 22 x 72.6, no bright element, a darker band a little below its middle; 3.1 review v2 (close) and the handover's fix: the two-part push is deleted |
| BL2 | old brass bell pull (reserve, not placed) |  | not placed | brass | Judgement: no photograph read shows one; refused on every house today |

**number**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| NM0 | none |  |  |  |  |
| NM1 | screwed metal numerals in a row on the top rail | [51.0, 56.0] | T1: u leaf centre, v two digits 39 x 72 on the muntin, v 1207 to 1277.6 and 1300 to 1373; F1: u leaf centre, v 1917; F2: u leaf centre, v 1922 | brass (181,150,85) | 3.1 (P1 stacked on the muntin, P2 in a row on the top rail: 56 high); F2 at v 1922, the middle of the visible top rail, so the digits (to v 1950) stay under the visible top 1960.6 and in front of the transom |
| NM2 | black metal screwed numerals (reserve) | [51.0, 56.0] | not placed | cast iron, black (30,30,32) | Judgement |
| NM3 | numerals painted white on the leaf's top rail |  | F3: u leaf centre, v 1925 | white gloss paint (226,224,214) | Photo D6: a white numeral painted on a blue door (size Judgement, 60 +-15) |
| NM4 | numerals painted white on the transom glass (reserve, not placed) |  | not placed | white gloss paint (226,224,214) | Judgement: a fanlight number is usual on such houses, but D3 shows its numerals on the leaf's top rail and none on the glass; refused on every house today (see NM6) |
| NM6 | small dark metal numerals on the leaf's top rail | [26.0, 30.0] | T2: u leaf centre, v 1898.6 | dark steel (40,40,42) | Photo D3: small dark numerals centred on the leaf's top rail, 3 to 4 px high at 10.07 mm a pixel = 30 (+-10), box [78, 443, 84.5, 446.5] (masked in the preview); v 1898.6 is the middle of the visible top rail (the review's number) |
| NM5 | oval plaque with a relief ornament, no digits (reserve) | [230.0, 154.0] | not placed | dark moulded plastic with a pale rim | Photo D2 white door: an oval 9.5 x 6.4 px at 24 mm a pixel (a house number's place); not placed |

**scraper**

| id | variant | size (mm) | place | material (sRGB) | source |
|---|---|---|---|---|---|
| BS0 | none |  |  |  |  |
| BS1 | cast-iron boot scraper beside the step | [404.0, 130.0, 200.0] (13 Oct, from the try 1 reviews) | T1: u , v  | cast iron, black (30,30,32) | Photo D10 (2014, said why: iron fittings of this kind were never renewed): scrolled standards and a blade with a notched underside; every size and the profile are Judgement, the photograph has no scale in its plane (+-25 per cent) |

Bell push BL1 in full: {name: plain dark oblong push, one part, size: [22.0, 72.6], proud: 3.0, corner_r: 1.0, groove: {w: 14.0, h: 2.0, depth: 1.0, below_centre: 8.0}, parts: 1, material: dark steel or dark plastic, srgb: [60, 60, 62], metal: 0.0, roughness: 0.6, place: {T1: {x: 859.4, z_range: [1120.3, 1192.9], on: the right jamb's stop face (3.1 as built: x 859.4, z 1120.3 to 1192.9)}}, forbidden: [bezel, button, ring, lens, led, camera, speaker, any second part, rounded pill corners above 2 mm, any bright or lit element], src: Photo P1 16x crop rows 300.3 to 314.4: a dark-grey oblong 22 x 72.6, no bright element, a darker band a little below its middle; 3.1 review v2 (close) and the handover's fix: the two-part push is deleted}.

Glass: plain_3mm: {thickness: 3.0, ior: 1.5, roughness: 0.05, transmission: 1.0, src: 3.1}; reeded_4mm: {thickness: 4.0, flute_pitch: 6.0, flute_depth: 1.2, section: circular segments, vertical, roughness: 0.08, transmission: 0.9, src: Judgement: reeded glass in F6's transom (D5's ribbed transom and sidelight are an indoor lining's, not a street door's); pitch and depth Judgement}; leaded_diamond: {came_w: 6.0, came_proud: 3.0, plain_pane_h: 144.0, band_h: 83.0, lozenge: [145.0, 83.0], foot_came_above_foot: 40.0, uprights: one under each lozenge point (5), whole_lozenges: 5, layout: in a light 772 x 267: the upper 144 plain; under it the band 83 high of two families of diagonal came crossing in a lattice of lozenges 145 wide and 83 high, the lozenge points (their lower vertices) on x = centre + k x 145 for k = -2 to 2 (5 whole lozenges, a tip of the next at each end, 23.5 wide), a horizontal came at the top of the band; a horizontal came 40 above the foot with an upright under each lozenge point down to the glass foot, glass_t: 3.0, came_material: dull lead-grey (90, 92, 95), roughness 0.5, src: Photo D3 (fanlight rows 376 to 436 at 10.07 mm a pixel): the upper 54 per cent one plain pane (rows 376 to 408), a band of crossed diagonals at a 14.3 px (144 mm) pitch (rows 408 to 427), a foot strip with an upright under each lozenge point (rows 427 to 436); the T frame's 267 mm light is kept; came 6 wide is Judgement}; frosted: {thickness: 4.0, roughness: 0.35, transmission: 0.6, src: Judgement; no photograph read shows it}; wired: {thickness: 6.0, mesh: 12.5, wire_dia: 0.6, src: Judgement; a stair door of a council block; none read}; lens_14: {dia: 14.0, src: Photo D5, place only}.

## 7. Paint and condition

**Door colours** (sRGB as the engine takes them; plain names; gloss paint roughness 0.35 kept, 0.55 tired, 0.65 neglected on the weather side low down; metal 0). Class is used by the facing rule.

| id | name | sRGB | class | on | source |
|---|---|---|---|---|---|
| black | gloss black, faintly blue | 35,36,40 | dark_neutral | east_parade bay 1; east_chandler bay 0 | 3.1 (P2 median 39,40,45) |
| dark_green | dark green | 28,59,41 | dark_chroma | west_north bay 1 | 3.1; the shopfront kit's door green |
| maroon | maroon, the sheet's deep red | 92,26,32 | dark_chroma | east_parade bay 0; west_south bay 0; west_north bay 0 | 3.1; terrace-front.py reads the sheet's doors as 'a deep teal and a deep red' |
| navy | dark blue | 24,38,78 | dark_neutral | east_parade bay 2; west_south bay 2 | 3.1 |
| brown | dark brown | 74,48,34 | dark_neutral | east_parade bay 3 | 3.1 |
| deep_teal | deep teal, the sheet's other door | 22,64,66 | dark_chroma | west_north bay 2 | terrace-front.py comment on the Hook sheet; D1 left door (a teal gone dark in shade, median 28,39,29); value Judgement |
| cream | cream | 222,212,184 | light | no house today | 3.1 frame cream; D3's door reads white-cream; held in reserve (no house takes it today: two pale doors side by side broke the neighbour rule) |
| white_gloss | white gloss (plastic-look moulded door) | 226,224,214 | light | west_south bay 1 | 3.1 frame white; D3, D4, D2 white doors |
| council_turquoise | council turquoise | 30,112,128 | bright | east_parade bay 4 | D9 box median (22,108,126) lifted for film; value Judgement |
| olive | olive (the 1960s council colour) | 114,102,65 | mid | no house today | D5 box median (the paint of an indoor door: Judgement for a street door); on no house today |
| khaki | khaki | 128,124,78 | mid | no house today | D2 middle door box median (136,132,83) darkened a little for film |
| mustard | mustard | 140,128,40 | bright | no house today | D2 left door box median (142,136,39) |
| bright_blue | bright blue (Hull 1980s) | 30,78,140 | bright | no house today | D6 box median (26,67,117) lifted for film; value Judgement |
| red | bright red | 201,41,32 | bright | no house today | 3.1 (P1 median) |
| varnish | natural varnished timber (a stained door) | 122,76,40 | mid | no house today | Judgement: no photograph read shows one on these streets |

**Frames:** white 226,224,214 (3.1 (P1 240,239,245 fresh; P2 222,225,229 old); the Hook sheet's surrounds are white); white_grimy 208,205,192 (3.1 white x 0.92, the windows target's white_grimy). Cream is dropped (3.1 allowed it at 0.3): see section 10.

**Colour boxes measured** (median RGB of a box inside the door leaf, film slides of 1975 to 1994, so a hue family and never a target value): D1_L_teal [48, 525, 66, 640] median [28, 39, 29] (shade; almost black-green); D2_F4_mustard [375, 282, 380, 330] median [142, 136, 39] (yellow-olive); D2_F5_khaki [563, 290, 572, 325] median [136, 132, 83] (grey-olive); D5_olive [470, 200, 740, 500] median [114, 102, 65] (olive, inside; flat); D6_blue [838, 335, 850, 415] median [26, 67, 117] (strong blue); D9_turquoise [393, 620, 399, 630] median [22, 108, 126] (turquoise, a small box low on the leaf). D7's green is a painted brick reveal, not a door, and is not used.

**Wear by condition** (kept, tired, neglected):

| mark | kept | tired | neglected |
|---|---|---|---|
| paint_flake_share | 0.03 | 0.063 | 0.4 |
| paint_fade | 0.3 | 0.6 | 1.0 |
| crazing | none | cells 2 to 4 mm over 30 per cent of the leaf (P2's) | cells 2 to 4 mm over the whole leaf (P2's old door) |
| chips | 0 to 2 chips of 8 to 15 mm on the leaf's lower arrises | 4 to 8 chips of 10 to 40 mm on arrises and the mouldings' lower lips, bare wood or undercoat showing | 12 to 20 chips and two sheets of 80 to 250 mm off the rail and stile feet, grey bare timber below |
| bottom_rail | clean; a dark splash band to 0.24 m only | darkened by splash to 0.33 m, a paint loss of 20 per cent on the rail | rotted: an eroded notch 25 mm high and 60 to 200 mm wide, 3 mm deep, in the lower arris at the hinge side, bare grey wood, a soft dark wet stain to 0.5 m |
| kick_marks | 0 to 2 scuffs, 20 to 40 mm, on the bottom rail | 3 to 6 scuffs and one boot print band 60 mm high at the lock side | 8 to 15 scuffs and dents, a split 120 mm long in the bottom panel's lower edge |
| polish | the brass is polished: a bright ring 12 mm wide round the letter plate's flap and the knob (kept bright), the rest dull gold | brass dull; a brighter ring where the flap is pushed (10 to 14 mm wide), a dark grease halo 0.17 m round the handle (handle_wear) | brass dark and green-brown; the plate's flap rubbed bright in a ring 10 mm wide only where fingers push; no polish elsewhere |
| frame | white, sound, a yellowing at the foot | yellowed, a hairline crack at the stop's foot | peeling down to a darker undercoat, a dirty foot |
| roughness | 0.35 | 0.55 | 0.65 |

Houses: east_parade bay 0 tired; east_parade bay 1 kept; east_parade bay 2 kept; east_parade bay 3 neglected; east_parade bay 4 tired; east_chandler bay 0 kept; west_south bay 2 tired; west_south bay 1 kept; west_south bay 0 tired; west_north bay 2 neglected; west_north bay 1 tired; west_north bay 0 kept.

**The wear layer of unit 4.5** (`production/cloud-week/2d/wear/`, its target `production/cloud-week/targets/wear/target.json`) is named for the PC and covers these marks by its kinds: paint_flake, paint_fade, handle_wear, wall_foot_splash, iron_wear (paint_flake on door bottoms and arrises at the shares above, handle_wear's grease halo p50 0.17 m round plates and handles, wall_foot_splash for the dark splash band to 0.24 m, 1.2 x higher within 0.6 m of a door, iron_wear on the boot scraper, paint_fade on the leaf). The check WR-wear-target and `self_check.py --live` compare the shares with that target's numbers. **Not covered by the layer, owed to it or to the door's build:** crazing in 2 to 4 mm cells: the layer's paint_flake crazing cells are 0.14 to 0.23 m (render); a timber-door tile is owed; kick marks and boot prints on a bottom rail: not a kind of the layer (the nearest is wall_foot_splash); a letter plate's bright polish ring: not a kind (the layer's handle_wear is a dark grease halo); owed as a small brightening mask in the brass's own material; rot as geometry (the eroded notch): the layer is a texture, so the notch is a build parameter of the door.

## 8. Photograph measurements, with their boxes

Every row a reviewer can reproduce: the box is [x0, y0, x1, y1] in the pixels of the file named in section 2 (Geograph's largest size, or Commons' 1920 px copy for D5). The leaf boxes are the visible face of the door as the gate will measure it: the white or painted leaf only, no neighbouring stone, brick or frame inside the box (a box that held brick gave the numbers of the windows target's first draft). Scales are the visible face's height over the box's height.

| record | photo | boxes and rows (px) | error (px) | what |
|---|---|---|---|---|
| D3_leaf | D3 | {box: [45.4, 442.6, 121.1, 634.1], at_row: 470, edges_by_row_px: {445: [44.9, 120.1], 470: [45.4, 121.1], 549: [47.4, 122.5]}, leaf_mm: [772.0, 1927.6], scale_mm_px: 10.07} | 1.5 | the door leaf on its own face: left stile's outer edge and right stile's outer edge at row 470 (white against the dark gap, never the brick beyond), top of the top rail, foot of the bottom rail |
| D3_rows | D3 | {rows_px: {light1: [449.5, 488.75], light2: [491.75, 531.25], light3: [534.25, 574.25], light4: [577.0, 613.75]}} | 2.5 | the four lights, top and foot row of each (the glass between the bars; soft against the nets, so 2.5 px) |
| D3_stiles | D3 | {at_row: 470, left_px: [45.4, 53.7], right_px: [115.3, 121.1], glass_mm: 625.0} | 1.5 | the white beside the glass on each side at row 470 (stile plus bead): 8.3 px = 84 mm on the lock side, 5.8 px = 58 mm on the hinge side; the glass between is about 625 mm |
| D3_handle | D3 | {box: [46.0, 498.25, 52.0, 524.25]} | 1.5 | the dark vertical pull handle on the left stile |
| D3_fixing | D3 | {box: [116.5, 492.5, 118.5, 498.5]} | 1.5 | a small dark two-part fitting on the right (hinge) stile, about 25 x 60 mm, centre v about 1390: not identified (a bolt keep or a stop screw): added as a small dark fitting, no more |
| D3_numbers | D3 | {box: [78.0, 443.0, 84.5, 446.5]} | 1.5 | the small dark numerals centred on the leaf's top rail (3 to 4 px high = about 30 mm; masked in the preview) |
| D3_fanlight | D3 | {box: [42.0, 376.0, 122.0, 436.0], rows_px: {plain_pane: [376.0, 408.0], diagonal_band: [408.0, 427.0], foot_strip: [427.0, 436.0]}, lozenge_pitch_px: 14.3} | 2.0 | the leaded fanlight over the leaf: the upper 54 per cent one plain pane (rows 376 to 408); below it a band of crossed diagonals forming lozenges at a 14.3 px (about 145 mm) pitch (rows 408 to 427); at the foot a strip with an upright under each lozenge point (rows 427 to 436). The T frame's 267 mm light is kept, the pattern is taken |
| D4_T3_leaf | D4 | {box: [545.3, 345.5, 579.0, 434.5], leaf_mm: [772.0, 1927.6], scale_mm_px: 21.66} | 1.0 | the white moulded door's outer edges (left 545.3; right 578.5 at row 375 to 579.5 at row 410: columns 580 to 583 are the dark reveal), top 345.5, foot 434.5 |
| D4_T3_light | D4 | {box: [558.5, 362.7, 568.0, 383.3]} | 1.0 | the small dark light: a flat head (row 363 is already dark over 8 of its 9.5 px, rows 361 and 362 are bright), top corners slightly rounded, the arch is the moulding round it (its line lies on row 358 in the middle and 359 at the sides) |
| D4_T3_plate | D4 | {box: [558.0, 392.5, 570.0, 395.6]} | 1.0 | the oblong letter plate |
| D4_T3_upper | D4 | {box: [550.5, 352.5, 577.0, 392.0]} | 1.5 | the upper panel's OUTER outline: columns 551 and 576 (rows 375 and 410 dip there), top line row 352.5, foot about 3.5 rows under the inner outline's foot (row 388.5: the stored first box ended on that inner line) |
| D4_T3_upper_inner | D4 | {box: [553.5, 358.5, 574.0, 388.5]} | 1.5 | the upper panel's INNER outline: columns 554 and 573.5, the arched line over the light on row 358.5 (crown), its foot on row 388.5; a margin of about 70 to 85 mm to the outer line |
| D4_T3_lower | D4 | {box: [550.5, 401.0, 577.0, 419.5]} | 1.5 | the lower panel's OUTER outline: as wide as the upper panel's (the same columns 551 and 576), rows 401 and 419.5 |
| D4_T3_lower_inner | D4 | {box: [553.5, 405.0, 574.0, 416.0]} | 1.5 | the lower panel's INNER outline: rows 405 and 416, columns 554 and 573.5 |
| D4_T3_handle | D4 | {box: [577.0, 388.0, 578.5, 396.0]} | 1.5 | the small lever at the lock edge: the dark mark at columns 577 to 578.5, rows 388 to 396, on the door (the first box, 581 to 583, lay on the dark reveal) |
| D4_slit | D4 | {box: [357.0, 340.0, 363.0, 383.75], leaf_box: [345.5, 334.5, 368.5, 407.5]} | 1.5 | the pale door's slit light and its leaf (the leaf is seen a little obliquely: rows only; rows 332 to 333 are the transom rail, columns 369 to 373 the jamb); the slit is 0.336 to 0.925 of the leaf |
| D4_low_plate | D4 | {box: [392.0, 405.0, 402.0, 408.0], leaf_box: [384.0, 335.0, 407.0, 410.0]} | 1.0 | the low letter plate at the dark door's foot (rows only) |
| D4_mid_frame | D4 | {frame_px_wide: 5.7} | 1.0 | the dark middle door is a flush door in a white frame about 5.7 px (about 120 mm) wide: the outdoor evidence for a flush face and a white street frame (F6) |
| D2_F5_leaf | D2 | {box: [561.0, 280.5, 594.5, 360.0], leaf_mm: [797.2, 1960.6]} | 1.5 | the khaki flush door, top edge below the transom rail, foot at row 360 (the khaki leaf ends at row 359.5 to 360; the pale sill lines at rows 360 to 362 and 365 to 366 are not part of it) |
| D2_F5_slit | D2 | {box: [574.0, 287.0, 582.8, 324.5]} | 1.0 | the slit light |
| D2_F5_plate | D2 | {box: [572.5, 327.5, 583.5, 329.5]} | 1.0 | the small pale plate under the slit |
| D2_F5_handle | D2 | {box: [561.5, 315.5, 565.0, 319.0]} | 1.0 | the small pale handle at the left stile |
| D2_F4_cols | D2 | {leaf_x_px: [374.5, 404.5], scale_mm_px: 23.3, light_x_px: [[381.5, 387.5], [389.5, 396.0], [398.5, 404.5]], bar_x_px: [[388.0, 389.5], [396.5, 398.0]]} | 1.0 | the three long narrow lights and the two bars between them, across, from the leaf's visible left edge (x 374.5); the scale 23.3 mm a pixel is the middle door's, in the same photograph at the same wall plane (797.2 / 34.2 px); the right stile is hidden in the reveal's shadow |
| D2_F4_top | D2 | {rows_px: {top_rail: [270.0, 273.0]}} | 1.0 | the top rail |
| D5_leaf | D5 | {box: [449.0, 137.0, 776.5, 982.0], leaf_mm: [762.0, 1981.0]} | 3.0 | the indoor leaf: left edge, right edge, top, the floor line (row 982: the mat starts at 984); used as the reference for fractions only |
| D5_plate | D5 | {box: [561.0, 570.0, 668.0, 600.0]} | 3.0 | the oblong letter plate |
| D5_handle | D5 | {box: [725.0, 582.5, 770.0, 597.5]} | 3.0 | the lever handle on the right stile |
| D5_lock | D5 | {box: [766.0, 617.0, 771.0, 626.0]} | 3.0 | the small dark lock under the lever (an 18 mm dark cylinder face) |
| D5_spy | D5 | {box: [595.0, 330.0, 630.0, 342.0]} | 5.0 | the round spyhole, its place only (blurred) |
| D1_L | D1 | {leaf_rows_px: [517.0, 667.0], transom_rows_px: [480.0, 509.0]} | 1.5 | the teal door: leaf top and foot, the transom light |
| D1_R | D1 | {leaf_rows_px: [517.0, 667.0], light_rows_px: [[517.0, 548.0], [552.0, 582.0], [588.0, 617.0], [622.0, 655.0]], plate_rows_px: [659.0, 662.5]} | 1.5 | the blue-grey door: the four lights and the low plate |

The photograph rows of the self-check (group photo) compare each kind's numbers with these records: T2's four lights and rails against D3 and D1, T3's panels, light and plate against D4, F5's slit, plate and lever against D2, F4's three lights against D2, F6's plate, lever, lock and spyhole against D5 (an indoor door: places only), the lozenge pattern and the stiles' white against D3's re-measured leaf, LP5's height against D1 and D4. Each of the six PH records of the checks list carries those fractions as its expected values with a tolerance, and the self-check recomputes both sides (the recorded boxes, the kind's own drawn parts). The live rows then re-measure the boxes on the pixels: the small light's flat head and the seven outline rows (D4), the lever's mark on the door (D4), the slit's dark run and the leaf's foot above the sill (D2), the plate's light run and the lock's dark mark (D5), the leaf's own edges row by row, its top, its foot, the stiles' white and the fanlight's plain pane against its lozenge band (D3), and the colour medians.

## 9. The gate in the cloud

The same views and checks as 3.1 (`kit/door/views_T1.json` for the cottage kinds, `views_F1.json` for the flat kinds): front (orthographic), street (3.5 m out, 2 m along, eye 1.6 m), close, low (7 m along, 2.7 m out), front_head, front_foot, close_plate, with the close and close_plate cameras lowered or raised to each kind's own fittings (T1 close at 1.25 m; T2 close at 1.58 m; T3 close at 0.92 m; F1 close at 1.00 m; F2 close at 1.40 m; F3 close at 1.60 m; F4 close at 1.24 m; F5 close at 1.06 m; F6 close at 0.88 m; F7 close at 1.01 m) and a close_foot view for a kind with a low plate. Pass rule as 3.1: front view by layer IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm; sections the same; profiles p95 <= 1.5, worst <= 3. One fresh reviewer per view, never bundled, its last good picture beside; the photographs of each kind beside the render (below). Street views: hook_day (vignette-scene.json cameras cam_A (x 4 east footway, looking up +x), condition overcast_day); reverse_day (the reverse camera of the same file); street_night (cam_A, condition wet_night); row_east (an orthographic elevation at 1.6 m of the east side, x 3 to 46, from the west footway); row_west (the same for the west side). Night light is the game's lantern colour, linear (1.0, 0.25, 0.0).

No model from a library is placed by this target (the doors are built by script from numbers), so there are no base-colour maps to read for lettering; the previews and the gate's renders carry no firm's name, house number or vehicle plate, and "rim night latch" is the only name for the lock anywhere in the text, data or pictures.

Photograph pairs for the reviewer: T2 against D3, D1: four lights equal, bars thin, stiles 84 and 58 of white, a low plate, a bar pull on the left stile, small dark numerals on the top rail, a fanlight with a plain pane over a band of leaded lozenges; T3 against D4: a small flat-topped light in a moulded upper panel (two outlines, the inner one arched over the light), an oblong plate between the panels, a lower panel as wide as the upper with two outlines, a short lever at the lock edge; F5 against D2, D4: a tall slit light centred on a flat door, a small plate under it, a lever on the left; F6 against D4, D5, D9: a flat door with an oblong plate at the middle, a lever on the right, a small dark lock under it, a spyhole, in the street frame F (the fittings from an indoor door, the colour from D9, a flush face in a white frame from D4's middle door); F4 against D2: three long narrow lights; F3 against D1: two long panels with raked heads, no cross rail; T1/F1/F2 against P1, P2: as 3.1's reviews; F7 against no photograph: no photograph reached; reads against Hasluck's figures only, listed as a known shortfall.

**The checks** (`target.json` checks, 162 records, each with name, what to measure, expected value, tolerance and source):

| group | count | what | examples |
|---|---|---|---|
| AD | 7 | the street: neighbours, facing doors, every house, frame sets, every kind used, the hill | AD-adjacent-east; AD-adjacent-west; AD-opposite; AD-coverage |
| BP | 4 | the bell push: one plain part, only on T1, no two-part modern push on any variant | BP-form; BP-none-elsewhere; BP-no-modern; BP-houses |
| CV | 31 | nothing shows through, in elevation and from 60 degrees, per kind; F7's joints | CV-T1-elevation; CV-T1-angle; CV-T1-inward; CV-T2-elevation |
| FU | 30 | furniture size and place per kind and variant (8 mm) | FU-F1-letter_plate-LP1; FU-F1-handle-HD1; FU-F1-latch-LK2; FU-F1-keyhole-KH1 |
| GA | 10 | the gate's views per kind | GA-T1-views; GA-T2-views; GA-T3-views; GA-F1-views |
| GL | 3 | glass types and values | GL-types; GL-reeded; GL-leaded |
| NM | 3 | no maker's name, the lantern colour, the lines for Jafar | NM-maker; NM-night; NM-dash |
| PH | 6 | each kind against its photograph | PH-T2-D3; PH-T2-D1; PH-T3-D4; PH-F5-D2 |
| PL | 61 | panel layout per kind (counts, every opening's bounds to 3 mm, members to 2 mm, framing) | PL-T1-count; PL-T1-top_left; PL-T1-top_right; PL-T1-bottom_left |
| PN | 4 | paint palette, white frames, at most 3 light doors, the 3.1 colours' values | PN-palette; PN-frames; PN-light-doors; PN-srgb |
| WR | 3 | wear numbers equal the wear target's | WR-order; WR-wear-target; WR-houses |

**For the builder.** (1) First: rebuild door_T1 without iron_bellpush_bezel and iron_bellpush_button (the handover's fix); the oblong iron_bellpush stays, one part, rebuilt square-cornered with corners r 1 (3.1 built r 6) and the BL1 groove 14 x 2 x 1 (3.1 built none). (2) build_door.py takes a kind (T1 T2 T3 F1 to F7) as well as the colour: the leaf, openings, mouldings and fittings come from target.json kinds and furniture; the frame set is T or F (every kind, F6 included, in its stops-in-front frame: the leaf opens inward, hinges inside). (3) New paints for --door-colour: deep_teal, cream, white_gloss, council_turquoise, olive, khaki, mustard, bright_blue, red, varnish (with the 3.1 six); --frame-colour takes white or white_grimy only (cream is dropped). (4) A condition parameter (kept, tired, neglected) sets the roughness and, for neglected, the eroded notch in the bottom rail (25 high, 60 to 200 wide, 3 deep, at the hinge side); the 2D wear layer's masks do the rest. (5) Behind every glazed kind (T2, T3, F4, F5 and every transom) the scene needs its own dark hall: the engine shows whatever is behind the glass (3.1 NOTES). (6) Check every kind with the 3.1 pass rule and the records of target.json checks; a push, a knocker or a plate the table does not place on a house is a fault.

## 10. Photographs win: where a photograph and the scene, a book or a ruling differ

| id | what | scene or book | photograph | chosen |
|---|---|---|---|---|
| W2 | the letter plate on every household door | the scene's 0.25 x 0.04 at 1.0 on every side door (west_north and east_chandler included) | D1, D4: a low plate at the foot; D2: a plate under a slit at 0.79; D5 (indoor, place only): 250 x 70 at 0.47 of the face; D4 right: 260 x 67 at 0.45; a service door has none | per kind (LP1 to LP7); none on F7 |
| W3 | the stand-in leaf is 766 or 678 wide in the drawn street; 3.1's leaves are 812.8 and 838 | terrace-front.py: leaf = 838 less two 36 casings (parade) or 838 less two 80 (cottages) | P1, P2, D3 (a 2 ft 8 in to 2 ft 9 in leaf) | 3.1's frame sets T and F replace the stand-ins; the wall kit meets their openings |
| W4 | the brass kick plate on the drawn parade doors | terrace-front.py draws a brass kick plate 726 x 140 on each side door | no photograph read (P1, P2, D1 to D6) shows a kick plate | none; kick marks are wear |
| W5 | hinges outside a ledged door | Hasluck Fig. 1027 draws hook-and-plate hinges on the face of a frame set in a wall | none reached | an inward-opening door, hinges inside (3.1's rule for all its doors, F6 included); the face shows boards and nail heads |
| W6 | the 3.1 cream frame (weight 0.3) | 3.1's frame_colours | the Hook sheet's door surrounds are white; Jafar 3 Oct: windows with white frames; D8 (Hull) and D2 (Railway Street: a mustard door frame and mustard window frames) show painted frames | white and grimed white only; the painted frames of D8 and D2 are an owed line |
| W7 | the bell push of 3.1's try 2 | build_door.py: oblong plus a brass bezel plus a dark button | P1: a plain dark oblong with a darker band, nothing bright | BL1: one plain part, square-cornered; the two-part push is a fault |
| W8 | the leaded fanlight's height | the T frame's glass opening 267 high | D3: a leaded light about 604 high over a 1948 leaf (rows 376 to 436) | the T frame's 267 stays (the wall kit owns the head); only the leaded glazing pattern is taken (a plain pane over a band of lozenges) |
| W9 | where a T2 door's house number goes | the earlier draft (and a common habit): a number painted on the fanlight glass (NM4) | D3: small dark numerals centred on the leaf's top rail, none on the glass | NM6, small dark metal numerals on the top rail; NM4 is a reserve, placed nowhere |
| W10 | the frame and stops of a council-style flush door | the first draft took a lining with the stops behind the leaf from D5 | D5 is an indoor landing door (Commons description): it is not evidence for a street frame; D4's middle door is an outdoor flush door in a white frame | F6 stands in the street frame F, an inward-opening 838 leaf with the stops in front; D5 gives the places of the fittings only |

Where a photograph disagrees with a ruling of Jafar's the ruling stands and the disagreement goes to him on his page (section 12). The Hull streets (D6 to D8) show window frames and surrounds painted in blue, red and yellow; his ruling of 3 October is windows with white frames, so every frame here is white or grimed white and the finding is owed line 2. "Photographs win" settles books and the scene's stand-ins against photographs; it does not settle a tally against his word.

## 11. Rulings checked

| ruling | how this target keeps it |
|---|---|
| 3 Oct: the proof view's bars: windows with white frames, sash bars, sky in the glass | the fanlights are windows and the Hook sheet's door surrounds are white: every frame colour is white or grimed white; 3.1's cream frame option is dropped; the Hull streets' painted surrounds (D8) are NOT adopted: owed line 2 |
| 21 Sep and 1 Oct: the Hook sheet governs mood, palette and composition; dated photographs govern what things looked like and win | dark doors lead (black, dark green, maroon, navy, brown, deep teal); the bright 1980s colours the photographs show are limited to 2 doors of 12: owed line 1 |
| 8 Oct: kit pieces period books draw (doors): a fresh helper writes the target; photographs win over books | this target; Hasluck is followed only for the ledged door, for which no photograph was reached |
| 2 Oct: Rita's window is the model; the other shopfronts are made like it | Rita's side door is the shopfront kit's own; the target gives it F1 and the kit keeps its fanlight |
| 4 Oct (terrace-front.py, Jafar: every house on the right is the same): each house its own door colour, never its neighbour's | the adjacency rule; the 12 doors share no colour with a neighbour on their side |
| 13 Oct: no alcohol or gambling shown; no children; no real firm or maker; night light (1.0, 0.25, 0.0) linear | no pub, sign or drink in any preview; 'rim night latch'; the gate's night view uses the lantern colour |

## 12. Owed to Jafar's page (one line each, recommendation first)

- Door colours: dark doors as the Hook sheet shows, with up to three lighter ones from 1980s photographs (two today: white, council turquoise; cream held back)? Yes, up to three (recommended), or all dark?
- Door surrounds: all white as you ruled for windows on 3 October (recommended), or the painted surrounds the 1980s Hull streets and Railway Street (D2, a mustard door frame and mustard window frames) show, as on the windows line?
- The west shop row has one storey: its three side doors become a service door and two household doors (recommended), or flats in its roof with household doors on all three?

## 13. Self-check

`python self_check.py [--live] [--photos DIR] [--previews] [--write]` writes its result into target.json under self_check. Result recorded: **--live --previews: 716 pass, 0 fail; negative controls (wrong copies, offline rows) 83 of 83 caught; live controls (wrong copies, live rows) 17 of 17 caught** (options: --live --previews; run 13 October 2026).

Groups: 31 (3.1's numbers as built, the handover's fix), meta (each photograph's title, author, licence, date and period note; every box inside its image), photo (the fractions above), street (the 12 doors, kinds, paints, neighbours, facing doors, the hill, no knocker, no council house), geom (the drawing: openings inside the leaf and not overlapping, fittings on the leaf, nothing shows through in elevation or at 60 degrees, the leaf's lap computed from the stop edges and the leaf's edges at 60 degrees in plan, every leaf behind its stops, the margins of each kind's leaf in its frame, the lead came's uprights and crossings counted on the drawing, the numerals inside the top rail, the boards and nails, the bars, the sections), checks (every record of the list, and that every opening and every placed fitting has one), wear (the numbers, and live against the wear target), text (no maker's name, no dash, the lantern colour, owed lines), gate, live (the street re-derived from terrace-front.py and the windows target, the photographs fetched and measured again on their pixels, the pages read again), previews (sizes, flat grey masks, credits).

**Negative controls** (wrong copies of the target, each run offline, each must make some row fail): T2: a bar moved 20 mm; T2: three lights instead of four; T2: the fanlight glass plain instead of leaded; T3: the small light 60 mm lower; F5: the slit 50 mm wider on each side; F4: a bar 21 mm instead of 36; F6: the letter plate at 1000 instead of 912; F5: the lever on the right stile (u 700); F6: the old 762 leaf in the street frame (a see-through slot beside it); F7: the leaf 700 wide in the F frame (a slot beside it); the bell push given a bezel part; a bell push on F1; the push made brass; two neighbours given one paint; two neighbours given one kind; two neighbours given the same furniture; a door facing another in the same paint class; a cottage given a flat kind; a house missing from the street; east_parade_bay5 given a side door; a cream frame colour on a house; a paint outside the palette; five bright doors; a knocker on a house; a lion's head knocker offered; a maker's name in a text; the stale night colour in the gate; an em dash in an owed line; an owed line without a recommendation; a photograph's date after 1995 used as period; a measurement box outside its image; D3's light row moved 12 px; a check removed from the list; neglected wear share 0.20 instead of 0.40; the T1 bolection width 36 instead of 3.1's built 46; the gate lacks a view; a kind never used; the backdrop's neighbours alike; reeded glass pitch changed to 9 mm; the leaded came 10 wide; LK1's collar 40 instead of 3.1's 43.5; F2 given 8 openings; a house given a lion's head knocker and a bell pull together; the wear layer's typical share changed; the hill's list shortened; the three owed lines made six; the T1 letter plate moved 40 mm; a placed fitting outside its leaf; F6: the leaf 838 in the rejected narrow frame (stops moved in to a clear of 765.2, an 838 leaf); the flat frame's leaf hung in front of its stops (the rejected planted-stop frame of F6: it would open outward); a leaf shifted 14 mm (the left stop laps it by only 6.4: the 60 degree row); a leaf set back 12 mm behind the stops (a 60 degree ray reaches 20.8 sideways, past the 20.4 lap); F1's leaf 40 mm shorter (the lap under the transom lost); the record CV-F1-angle with a right lap of 30 instead of 20.4; T2: stiles 114.3 on both sides (the first draft's 93.9 visible, 104 of white on each side); T2: the fanlight lozenges all over (no plain upper pane); T2: the lozenge pitch 95 and 70 high (the first draft); T2: three lozenge points instead of five; T2: the house number back on the fanlight glass (NM4); T2: the small dark fitting on the hinge stile left out; T3: the small light given a semicircular head (corner radius 109); T3: the lower panel 160 mm narrower than the upper (the first draft's u 234.8 to 642.3); T3: the upper panel with one outline only; T3: the lever on the reveal (v 823 as the first draft); F5: the slit at the first draft's v 914.9 to 1806.1; F5: D2's leaf box taken down to the sill (foot row 363); D3's leaf box on the first draft's span (a box that spans the lean); F3: the panel heads square (the first draft); F6: the lock under the lever left out; F1: the plugged keyhole left out; F2: the numerals at v 1943, behind the transom (the first draft); the bell push with r 6 corners (3.1's build); T1's parts table says the bell push is kept; two pale doors side by side (west_south_bay0 back to cream beside white gloss); a maker's name in TARGET.md; the lock's old name in a part table; the lock's old name in a script's prose; D5 named again as the evidence for the frame; D9 called a flush door again; F6 given a frame_change again (the rejected FF6); a photograph record with nothing to compare (PH-F6-D5 expect null); owed line 2 without Railway Street's mustard frames; the boot scraper's standard without its profile. Counts are printed with the options named, offline and with --live (the controls always run offline, since the live rows read the world and not the copy).

**How to read it honestly.** The photograph fractions that are independent of the numbers drawn from them are T2's bottom rail and bars (3.1's frame, not the photograph, gives 205 and 30), D1's lights against T2 (a second photograph, oblique), D4's panels and plates, D2's slit and plate (the live rows measure them on pixels), and the stiles' white and the fanlight's three parts (D3, re-measured on the leaf's own face; the stiles 94.0 and 69.0 and the fanlight pattern were set from the review's re-measure, then compared with the boxes). T2's lights, T3's panels, F5's slit and F6's fittings were fitted to the same photographs, so their near-zero differences are by construction; the live edge rows are what test them, and the first draft's wrong boxes (D3's, D2's, D4's) are among the live negative controls. F5's slit, plate and lever and T3's lever are the review's numbers, 5 to 12 mm from what the recorded boxes give (inside the stated error), and the photograph rows hold that difference. Everything not measured is marked Judgement, and section 14 lists it.

## 14. Could not settle

1. No dated photograph read shows a door knocker, a bell pull, a black iron letter plate, frosted or wired door glass, or a ledged service door on these streets. KN1, KN2, BL2, LP3, frosted, wired and NM2 are listed with Judgement sizes and refused on every house by the checks; F7 is built from Hasluck and Judgement alone.
2. Door colours of 1990: the slides of 1975 to 1994 shift hue and exposure, so the palette's bright and mid values (turquoise, bright blue, lime, khaki, mustard, olive) are Judgement from boxes whose medians are recorded; the dark classics are 3.1's.
3. Small hardware at 22 to 27 mm a pixel (plates, levers, a small light) carries +-24 to +-35 mm; the positions are fractions of the visible face with that error written in each check.
4. D1's doors stand in deep recesses and are seen from the right: only their vertical rows are used; the leaves' widths and the letter plate's length are not taken from it.
5. Whether the west shop row (one storey in the drawn street) has flats: its side doors are 1 service door and 2 household doors until Jafar answers owed line 3.
6. The painted cement hoods over Hull doorways (D1, D6) and their arched recesses (D7) are wall features; not in the door piece, listed for the wall kit.
7. A house number's digits are the town's; the target fixes only the form (NM1, NM3, NM6).
8. F6: no outdoor photograph read shows a council-style flush door close enough to measure its fittings. The places of its plate, lever, lock and spyhole come from an indoor landing door (D5) as fractions of its face, +-35 mm; D9's door (6 px wide) reads as half-glazed, so only its lower panel's turquoise is used; the leaf is the street's 838 in the frame F.
9. T2's fanlight pattern is read at 10 mm a pixel with 14 px lozenges: the pitch (145) and the band's height (83) are Photo within 1 px, the came's width (6) and the two end tips (23.5) are Judgement; the small two-part fitting on D3's hinge stile cannot be identified.
10. The shopfront kit's own side door at east_parade bay 2 (Rita's) has its own geometry and a fanlight (unit 2.2); this target gives it kind F1 and expects the builder to put F1's leaf in that slot.
11. The boot scraper: one cast-iron scraper by the nearest cottage's step; no period photograph of these streets shows one (D10 is 2014); the sizes are Judgement +-25 per cent.

## 15. Credits for the previews in `production/previews/cloud-week/refs/front-doors-all/`

Reduced crops of the doors only (at most 1200 px, under 300 KB), for measuring and for the reviewers, never placed in the game. Masked flat grey by script and recorded in `preview_masks.json`: a pole-mounted board and an oval plaque (D2), small numerals (D3), a small label (D5), a painted numeral (D6), a board on a fence (D8). No people, no child, no drink or betting, no firm's name, no house number and no vehicle plate in any preview; each was looked at in full.

| file | credit |
|---|---|
| d1-durham-carrville-terrace-1975-two-doors.jpg | David M Clark, CC BY-SA 2.0, https://www.geograph.org.uk/photo/7292055, taken 1975-01-22 (Carrville Terrace); cropped, reduced, masked as above |
| d2-railway-street-1987-three-doors.jpg | P L Chadwick, CC BY-SA 2.0, https://www.geograph.org.uk/photo/2238747, taken 1987-08-09 (Terraced housing in Railway Street); cropped, reduced, masked as above |
| d3-levenshulme-ratcliffe-street-1994-four-light-door.jpg | Anthony Parkes, CC BY-SA 2.0, https://www.geograph.org.uk/photo/2321423, taken 1994-06-10 (Terraced House - Ratcliffe Street, Levenshulme); cropped, reduced, masked as above |
| d4-barnoldswick-frederick-street-1990-three-doors.jpg | Dr Neil Clifton, CC BY-SA 2.0, https://www.geograph.org.uk/photo/689253, taken 1990-04-10 (Nos. 34, 32 and 30, Frederick Street, Barnoldswick); cropped, reduced, masked as above |
| d5-aberdeen-hazlehead-1987-council-flush-door.jpg | Miles Glendinning (Tower Block Archive, Edinburgh College of Art), CC BY 4.0, https://commons.wikimedia.org/wiki/File:Hazlehead_I,_Provost_Graham_Avenue_(SC_1141987).png, taken 1987 (Hazlehead I, Provost Graham Avenue (SC 1141987)); cropped, reduced, masked as above |
| d6-hull-rensburg-street-1982-blue-door.jpg | Bernard Sharp, CC BY-SA 2.0, https://www.geograph.org.uk/photo/7982731, taken 1982-03-19 (Rensburg Street, Kingston upon Hull); cropped, reduced, masked as above |
| d7-hull-abbey-street-1986-arched-doorways.jpg | Bernard Sharp, CC BY-SA 2.0, https://www.geograph.org.uk/photo/3462921, taken 1986-06-08 (Abbey Street, Kingston upon Hull); cropped, reduced, masked as above |
| d8-hull-brazil-street-1986-painted-frames.jpg | Bernard Sharp, CC BY-SA 2.0, https://www.geograph.org.uk/photo/3462940, taken 1986-06-08 (Brazil Street, Kingston upon Hull); cropped, reduced, masked as above |
| d9-newburn-council-houses-1989-turquoise-door.jpg | Kevin Hall, CC BY-SA 2.0, https://www.geograph.org.uk/photo/2876894, taken 1989-08-01 (Newburn Council Houses); cropped, reduced, masked as above |
| d10-poole-boot-scraper-2014.jpg | Mike Searle, CC BY-SA 2.0, https://www.geograph.org.uk/photo/3911943, taken 2014-03-30 (Old Town, Poole: in search of the boot scraper); cropped, reduced, masked as above |
| d3-levenshulme-ratcliffe-street-1994-target-on-photo.jpg | the target's drawing of T2 (own work) laid on the photograph it was measured from (D3), the scale fitted on the visible height only; yellow the visible face, red the openings, orange the mouldings, green the fittings |
| d2-railway-street-1987-target-on-photo.jpg | the target's drawing of F5 (own work) laid on the photograph it was measured from (D2), the scale fitted on the visible height only; yellow the visible face, red the openings, orange the mouldings, green the fittings |
| d5-aberdeen-hazlehead-1987-target-on-photo.jpg | the target's drawing of F6 (own work) laid on the photograph it was measured from (D5), fitted on height and width because D5 is an indoor door with a narrower leaf and only the fittings' places are taken from it; yellow the visible face, red the openings, orange the mouldings, green the fittings |
| target-ten-door-kinds-elevations.jpg | the target's own drawing of the ten kinds (own work), each in its house's first paint |
| target-street-rows-east-and-west.jpg | the target's own drawing of the street's two rows of doors in street order (own work) |

## 16. Changes after the build (13 Oct, from the try 1 reviews)

The doors were built (production/cloud-week/kit/front-doors-all/) and two fresh reviews, one of the street view and one of the close view (REVIEW-doors-v1-street.md and REVIEW-doors-v1-close.md in that folder), failed the first build. Each correction to THIS target that they list is made below, in `target.json` (its `status` and a `changes_after_the_build` list say so) and, where it superseded a statement, in the body above, marked "(13 Oct, from the try 1 reviews)". The kit's script `kit/front-doors-all/target_changes_try2.py` applies them and can be run again (it changes nothing the second time). The target's makers (`td_*.py`, `make_target.py`, `make_doc.py`) and its reference drawing (`target_drawing.py`) are NOT changed: they are not this unit's files, and regenerating the target from them would undo these changes; they are owed the same changes (the drawing's moulding ring starts 4.8 outside the opening's edge, its `reeded_section` has a 2.8 base).

| change | why |
|---|---|
| T3: profile_dh: each of the two steps 6 mm deep over 6 mm across (the margin 6 below the face, the field 12 below); the outlines (u 119.9 / 182.4 / 630.4 / 692.9) and the 44 mm leaf are kept; the second cove at d 62.5 to 68.5 | street review, fault 1: the outlines dipped 1 to 3 per cent in the street view; D4's dip 14 to 40 per cent. Also narrow point 12(c) of the close review (the second cove at 62.5, not 76) |
| T3: border 65 becomes 62.5 (row PL-T3-members) | street review point 10, close review 12(a): the flat margin of the target's own outlines is 62.5 at the sides |
| T3: new row PL-T3-street-dip: in the street view every outline dips at least 10 per cent of the face's brightness | street review, fault 1 |
| T1, F1, F2: the bolection ring starts 4.8 outside the opening's edge (lap_over_framing_mm 4.8) | street review 11, close review 12(b); target_drawing.py (the reference drawing, not this unit's file) still draws the literal ring: the check's required rows read the lap from this field, its three literal extras keep failing for that reason only |
| F7: leaf 47 thick (boards 22, ledges 25, braces 25) instead of 38 with thin ledges | street review 13, close review 12(d): 22 + 25 cannot make 38; 16 mm ledges are thin against Hasluck's |
| BS1: the point list is mirrored so each scroll sits outside its standard and curls outward; the overall length is 404 (the blade 300 between bars 140 either side of the middle, the scrolls to 202); the feet stand 0.4 into the ground and the standards 0.55 | street review 9 (D10's scrolls sit outboard of the blade's ends and curl outward; the photograph shows it); the close review's 12(e) reads D10 the other way, and is wrong: the left scroll's centre is about 70 px outboard of the blade's end in D10 |
| reeded glass: a base 2.8 thick under flutes 1.2 deep (4.0 in all) | street review 14, close review 12(f) |
| LP2: chrome (nickel or chrome-look, sRGB 170, 170, 168) instead of brass | close review 12(h): P2's plate is chrome-coloured |
| F5: the hairline is kept and said to show only at the foot (under the stops' lap on three sides) | close review 12(h) |
| HD2a, HD2b, HD2c: the lever bar tapers from 16 at the neck to 12 at the end and its last 25 mm curve back 9 toward the door | close review 5 |
| HD2b and HD2c: a backplate 40 x 170 with a keyhole 57 below the lever's centre in place of the round rose (HD2a, F6, keeps its rose) | street review 2 (and its 1990 photograph); the close review's 'keep the round rose' rests on D5, which is F6's door, HD2a |
| HD3: a round grip 19 across on posts that flare into 25 roses, stand-off 30 (face to the grip's axis), 25 x 270 overall kept; HD4: cusped plate, a 19 round bow standing 30 off on posts 120 apart, a thumb lever 14 x 45 at 15 degrees through a slot in the head | close review 3 and 4 |
| a lever's u, v (rows FU-*-handle-HD2a, HD2b, HD2c) is the centre of its rose, or of its boss on the backplate | close review 12(g) |
| KH1 is sunk (a blind pocket 2.2 deep in the leaf, plate face 2.0 and blank 0.5 below the leaf's face); T2 and F3 carry one, 70 below the foot of the bar pull | close review 10; street review 2 (the keyhole 70 below the pull's CENTRE would lie behind the 270 mm bar, 135 each way: placed below its foot) |
| T2: the hinge-stile fitting is built (two boxes 20 x 25, 10 apart, centred u 753, v 1390, 8 proud) and has a row, FU-T2-hinge_fixing | street review 5, close review 1 |
| west_north_bay1 (F3) is brown (was dark green); west_north_bay0 (F1) is dark green (was maroon) | street review 7: F3 dark green next to F7 deep teal measured a colour difference of 8.4 against 15 to 60 for every other neighbouring pair; the two maroon F1s were twins |
| house numbers: odd on one side and even on the other, rising from the quay, two digits at most (T1 17, T2 21, F3 29, F2 14); strokes with round bowls | street review 3 and 4, close review 8 |
| glass: base colour (235, 238, 236) for every clear pane; reeded glass its own material glass_reeded; T2's net cards take the windows' net material net_voile (white 238, 238, 232) | street review 1 and 6, close review 7 |

Still as the first target had it, because the reviews found it right: T2's four lights and its fanlight, F2's plate (placed 5 mm above its number in the kit, see NOTES.md), the frame sets, F1, F4, F5, F6's plate, lever and lock, the 15 paints and the three conditions.

## 17. Changes after the try 2 reviews (14 Oct, from the try 2 reviews)

Two fresh try 2 reviews (the street view and the close view, REVIEW-doors-v2-street.md and REVIEW-doors-v2-close.md in kit/front-doors-all/) passed the doors with no fault and 4 and 7 narrow points. Each correction to THIS target is made in `target.json` (its `status` and `changes_after_the_build` say so) by `kit/front-doors-all/target_changes_try3.py`, which can be run again (it changes nothing the second time). target.json is the home of the numbers: `make_target.py` and `make_doc.py` hold the first draft and are frozen (they refuse to run without `--first-draft`, which writes `target.first-draft.json` and `TARGET.first-draft.md` instead); `target_drawing.py` draws the bolection ring with its lap.

| change | why |
|---|---|
| chrome_nickel (LP2, LP4, HD2a, HD2b, HD2c, LK1, LK2 and F6's spyhole ring) is sRGB (196, 197, 196), roughness 0.35, in place of (170, 170, 168) | close review 4: the chrome-look parts read at about half the brightness of P2's plate (ratio to the black door 2.3 against P2's 3.7 to 4.1); (170, 170, 168) is linear 0.40, measured chromium 0.55 |
| HD3: the grip's axis 39.5 off the face (stand_off), 49 proud, the clear gap behind the grip 30; HD4: the bow's axis 39.5 off the plate, 30 clear behind it | close review 2: 'stand-off' is the clear gap behind the grip; the first build read it as face to axis and left 20.5 clear, too tight for a hand (30 to 40) |
| HD4: the thumb lever leaves the plate at 75 degrees to the face (15 above the horizontal), 45 long, its last 20 mm a pad 20 across; it reaches at least 40 out and rises at most 15 above its slot | close review 1: it stood upright above the plate (13.7 out, 17 degrees off the face) like a fin; a thumb lever points at the street and is pressed down |
| T3: a quirk, a groove 5 wide and 3 deep outside each of the four outlines of both panels (the head's arc included), its inner edge 0.1 off the outline; PL-T3-street-dip stays at 10 per cent | street review 1 (left-hand outlines dip 1 to 2 per cent against D4's 22 and 5; tested 11 to 17 with the grooves); the close review's 3 (a 3 x 3 quirk on the outer outlines only, a 10 and 3 per cent split) is superseded by the street review's, the view the lines are seen from |
| BS1: both spirals of the scroll resampled every 7.5 degrees (a point list of 78 points; it was 24): no facet longer than 5 mm | close review 6: the scrolls read as 8 to 10 straight facets of 16 to 18 mm |
| new rows: FU-T2-grip_gap, FU-F3-grip_gap, FU-F7-grip_gap, FU-F7-thumb, FU-T1-scraper-facets, PL-T3-quirk, GA-T2-nets-lit (0.80 to 0.90 of the transom bar), MAT-chrome_nickel, TG-makers-frozen | the reviews' tests for their points |
| the target's makers (make_target.py, make_doc.py) are frozen with a guard; target_drawing.py draws the bolection ring with its lap and the T3 section closes at 16 deep | street review 3, close review 7: the makers hold the first draft and would undo the fixes (1,659 differences); the three literal moulding extras failed only because the drawing's ring started at the opening's edge |
| T2's nets (a render aid, not in any file): random folds 30 to 70 mm apart, brightness 0.78 plus or minus 0.11, scaled so the lights read 0.85 of the transom bar's face | street review 2: they read 0.95 to 1.0 of the transom bar (brighter than the white frame) and the folds repeated every 48 mm like a pleated blind |
