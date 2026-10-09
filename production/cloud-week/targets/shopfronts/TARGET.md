The shopfront kit's target: pilasters (plinth, shaft, necking, capital), consoles, fascia board and cornice, sill and stallriser, window frames with mullions, transom and toplights, the shop door and the F1 side door's slot, ten fronts assembled by a table, with the 1990 alterations by kind; measured today on one reached photograph (Leadenhall Market), which moves the plinth to 800, the shop door's glazing to 0.70 m and the sill to 75 mm.

# Shopfronts of Quay Street, as a kit of parts: the exact target

Cloud week 42, 9 October 2026, FIRST TRY by a fresh target writer for unit 3.2 (the parts) and the builder (the assembly). Not reviewed. Nothing is committed. Everything in this file is in `target.json`; the checks that follow from it are in its `checks` list and its `self_check`.

## 0. Files, and how to read them

Files in `production/cloud-week/targets/shopfronts/`:

| file | what it is |
|---|---|
| `TARGET.md` | this page (written by `make_doc.py` from `target.json` and its own prose) |
| `target.json` | every part with dimensions, profiles as point lists, positions, variants, materials; the paints; the ten fronts' assembly table; the alterations; 81 `checks`; the self-check result |
| `target_drawing.py` | draws target.json ALONE: each part's elevation and sections, an elevation of Rita's whole bay and of the ten, at 1 mm to the pixel, into a folder given on the command line, with the polygons as JSON, and the drawing laid on the photograph's previews |
| `self_check.py` | tests the target against its own sources and the photograph's saved previews; writes `self_check` into target.json |
| `measure_leadenhall.py` | author tool: re-projects the photograph to a level elevation, measures it (43 rows and columns and one notice), writes `photo_measurements.json` and the previews |
| `make_target.py`, `tgt_parts.py`, `tgt_shops.py`, `tgt_text.py`, `tgt_profiles.py` | author tools: build target.json from the parts, shops and prose |
| `make_previews.py`, `make_doc.py` | author tools: the previews; this page |

Run with `/home/user/.bpyenv/bin/python`: `target_drawing.py OUT_DIR [--json drawing.json] [--all-fronts] [--photos PREVIEW_DIR --overlay-out DIR]`, `self_check.py`. Previews: `production/previews/cloud-week/refs/shopfronts/` (section 15).

**Units and axes.** Millimetres; sRGB 0 to 255, aged to 1990; roughness 0 to 1; metal 0 to 1. The frame is the GAME's viewer frame, as the fascia target uses it: **u** across the bay from the viewer's left party-wall line (0) to the right one (6000); **d** out from the wall face toward the street (the kit's y is -d); **z** up from the footway. On the east parade low street x is on the viewer's right, so a front's door end is read off the viewer's side (`shops[].door_end_viewer`), with the street's word (`door_end_street`) and the recipe's `doors_on` word beside it; street x = bay high end - u/1000 on the east parade and bay low end + u/1000 on the west block. Section planes: `d-z` a side section, `u-d` a plan, `a-p` a small moulding, `u-z` an elevation; closed outlines are counter-clockwise.

**Kinds of number.** Read: printed in a source file. Scaled: measured off a drawing or the project's own files. **Photo: measured on a photograph today** (method and error stated). Derived: worked from others. Judgement: nothing else fits; a better source overturns it. A number with no kind is a Read from the street's own files.

## 1. What the target does, in one table

| part | what the target gives | main change from the kit, and why |
|---|---|---|
| pilaster (4 variants) | plinth 800, shaft 290 x 110 proud, necking, capital 310, 350 x 130 at the top; panelled, fluted, rendered on a stepped plinth, flush clad | plinth 600 to 800 (Photo: the plinth stands 1.27 x the sill) |
| console (scroll, block, absent) | 240 x 180 x 550 on the capital; the S silhouette smoothed; a volute on each face and an acanthus leaf | the volute and leaf are Judgement; no photograph of a scrolled console was reached |
| fascia board | 5410 x 550, 120 proud, a 40 bed mould; vertical | the bed mould |
| cornice | 215 x 150 x 5892, 19-point profile with a tall corona | profile only: the fixed envelope stays (the photograph's crown is 3 x taller and is NOT followed) |
| sill, stallriser (8 variants) | sill 75 thick, nose 150; panelled, brick tile, square tile, patterned tile, glass slab, render, boarded, grille | sill 50 to 75; more stallriser kinds for the ten fronts |
| window frame (T1, T2, M1, M2) | mullions 70 / 80 / 50 / 28 wide, transom 80, toplights, glass at d 30 | mullion 55 to 70 (the photograph reads 164: partly followed) |
| shop door (T1, M1, M2) | 900 x 2040 in 1006, **glazed from 700**, brass foot strip | glazed from 1000 to 700 (Photo and the books agree against the scene) |
| side door slot | 944 slot for the front-door family's F1 (not re-targeted): the mapping into the bay | none |
| lobby | recessed 600 (grocer) and 300 (launderette), tiled or terrazzo floors | new |
| ten fronts | an assembly table: trade, bay, original or altered, stallriser, door end, lobby or flush, glazing pattern, paints | new |

## 2. Sources

Only sources actually reached today are used. Search summaries are not used as numbers. Photographs are for measuring only: never placed in the game, never traced into a texture, never fed to an image model. No NoAI source.

| id | what | URL | read | author | licence | taken | shows | used |
|---|---|---|---|---|---|---|---|---|
| P1 | Leadenhall Market, a 360 degree HDRI (16384 x 8192), re-projected here to a level rectilinear elevation of the arcade's right-hand wall (yaw 90, focal 2400 px) | https://polyhaven.com/a/leadenhall_market; files: https://api.polyhaven.com/files/leadenhall_market (16k .hdr read 2026-10-09 from dl.polyhaven.org) | 2026-10-09 (this cloud reached polyhaven.com and its file host) | Andreas Mischok | CC0 (Poly Haven) | 2019-05-19 | heritage-restored Victorian covered market fronts (built c.1881, from memory, not checked): stone- or render-faced pilasters on stepped plinths, pier caps under a fascia, a deep cornice, heavy teal-painted window frames with a mid transom, a cast-iron ornament band over the head, cast-iron lattice stallrisers in frames, red double doors with a brass foot strip | Yes, measured: 43 rows and columns and one notice (photo_measurements.json), 6 joinery-only previews. Lettering (house numerals) is masked; the unmasked views carry real businesses' names and notices and were never saved into the repository |
| P2 | Poly Haven CC0 roller-shutter models (rollershutter_window_01, _02, _03, rollershutter_door): glTF read today | https://polyhaven.com/models (files by https://api.polyhaven.com/files/<id>) | 2026-10-09 | MP (Poly Haven), published 2023-10-11 | CC0 | scanned or modelled 2023 | a steel hood, guide rails and a slatted curtain; hood depth 153, 168, 300 and 300 for curtains 1546, 1561, 1851 and 2400 high | Yes, for the roller-shutter box's depth and the rail width (alterations.roller_shutter); the form, not the date |
| K | the existing shopfront kit: production/art/shopfront-kit/README.md and tools/art-recipes/shopfront-kit/*.py (6 October 2026, by script) | - | 2026-10-09 | studio | own | - | the parts' sizes and profiles as built and the bay's datum | Yes: the starting point; every change is listed in kit_vs_target |
| F | production/research/shopfronts/FRONTAGE-2026-10-06.md (the project's earlier reading: council guides, Historic England entries, Building Conservation Directory, Ellis 1902 Modern Practical Joinery) | - | 2026-10-09 (this file), its sources were read on the PC on 6 October | studio | own | - | anatomy, colours, wear, the four points where research differs from the spec | Yes, cited as the project's earlier reading, NOT re-read at source |
| W | production/research/shop-window-interiors/ (NOTE.md, FISHMONGER-2026-10-03.md ...), production/research/street-wear/PAINTED-FRONTS-2026-10-07.md, production/reference/photographs.md | - | 2026-10-09 | studio | own | - | what the period photographs establish: metal shopfronts beside older frontage, patterned tile stallrisers, recessed doorways with tiled thresholds; white tiles and slabs in fish shops; where a front wears | Yes, cited |
| S | SCENE-SLOTS.md, canon.md, RULINGS.md, production/specs/terrace-fronts.md, production/art/fascia-01/*, production/cloud-week/targets/fascia-signs/target.json, production/cloud-week/targets/front-door/target.json, tools/art-recipes/terrace-front.py (paints, refits, doors_on), production/previews/*.jpg (Rita's day and night, the kit sheet, the whole fronts, the Hook sheet) | - | 2026-10-09 | studio | own | - | the street's fixed numbers, the trades, the fascia's board and cornice, the F1 side door, the door ends, the paints | Yes |

**P1's date and kind.** NOT a 1990 object and not a provincial parade: a 2019 restoration of a London arcade (built c.1881, from memory). Used for proportions and the order of mouldings only, never for colour or wear. Why it still serves: it is the only reached photograph of a Victorian British shopfront in joinery and masonry at a measurable scale, and the parts it shows (plinth, shaft, necking, capital, fascia field, crown, sill, stallriser frame, transom, mullion, door) are the parts of a 1900-1935 parade front; the ratios between them are tested against the street's fixed numbers in section 4 of TARGET.md

**P1's scale.** fitted on ONE dimension: an A5 notice (148 x 210 mm) on the shop door's glass, 78.35 x 108.90 px; the door plane is 1.104 times farther than the pilaster's front plane (the foot rows 604.1 and 547.0); the camera stands about 1.04 m above the footway.

**Unreached (403, no route or not tried): nothing from them is used.**

- Wikimedia Commons and Geograph (the period and modern photographs of British shopfronts; 403 or no route today)
- archive.org (Ellis, Modern Practical Joinery, 1902, and other books; no route)
- historicengland.org.uk (list entries 1488333, 1393627; no route)
- buildingconservation.com, the council guides (Brighton and Hove, Coventry, Westminster, RBKC, Cornwall, Richmond, Dover), Wikipedia, Gutenberg, HathiTrust, Google (no route)
- Flickr, Peter Marshall's Hull set, Picture Sheffield (the project's earlier reading of them is cited, not re-checked)

**What I would read once the network opens:**

- Historic England 'Shopping Parades' (Introductions to Heritage Assets) and its Commerce and Exchange listing guide: the sections of surviving 1900-1935 consoles, cornices and pilasters, with dimensions
- Ellis, Modern Practical Joinery (1902), the shop-front plates: stile, mullion and transom sections, sill sections (the 'stout sill'), the cornice's limits in inches
- Geograph and Commons photographs, 1975-2000, of provincial British shopfronts: scrolled consoles and their leaves, 1970s aluminium fronts and their cover caps, roller-shutter boxes, plastic box signs over old fascias, recessed lobbies with tiled floors, whitewashed empty units (each with author, licence and date read on the file page)
- Peter Marshall's Hull photographs (R05, R09, West Dock Cafe, 1981) at the page: the metal front's section widths, the patterned tile's repeat
- A real surviving 1920s provincial front's measured drawing (a council's survey, or the Building Conservation Directory's 1994 'Retail Detail')
- Manufacturers' 1980s sections for aluminium shopfronts (the extrusion widths: 50 and 75 are Judgement here)

## 3. What was measured on the photograph today, and how far it holds

P1 is re-projected to a level rectilinear elevation of the arcade's right-hand wall (yaw 90, focal 2400 px); a plane parallel to the wall is then at one scale. `measure_leadenhall.py` snaps each edge to the strongest luminance gradient near where it was looked for, averaged along a span chosen to avoid ornament; `self_check.py` re-measures every row and column that can be on the SAVED previews. Scale: fitted on ONE dimension, an A5 notice (148 x 210 mm) on the shop door's glass, 78.35 x 108.92 px, giving 1.9085 mm a pixel in the door's plane; the door's plane is 1.104 times farther than the pilasters' front (the foot rows 604.1 and 547.0), so the pilaster plane is **1.7282 mm a pixel** (the camera about 1044 mm above the footway); error 8 per cent, which is the A5 assumption, the plane ratio and the notice's edges. Ratios carry none of it.

| what | measured (P1, mm at the stated plane; kind Photo, +-8 per cent unless stated) | the street's number | reading |
|---|---|---|---|
| shaft width | 290 | 290 (kit) | the kit's 290 stands: no disagreement |
| shaft projection (from the right return: 30.8 px at 1087 px off axis) | 117 (+-14 per cent) | scene 100; target 110 | D3: 110 is inside both |
| plinth: block tops z | 708 / 886 / 952; cap slab top 1123 | kit 600; target 800 | ratios R1, R2: plinth top is 1.27 x the sill's top and 0.228 of the front's height; at 3.55 m that is 811 |
| capital height (neck ledge to abacus top) | 301 (1.04 x the shaft's width) | kit 330; target 310 | D4 |
| fascia field (between the gilt keylines) | 505 | 550 | no disagreement: the street's 550 is the same order |
| crown (fillet to cap, on the continuous run) | 446 (0.86 of the field) | 150 (0.27 of the fascia) | D7: NOT followed (the fascia target fixes the cornice top at 3550) |
| sill top (wall plane) | 883 (0.18 of the front's height; 0.64 m at 3.55) | 600 | no disagreement (6 per cent) |
| window stile / mullion face (wall plane) | 145 / 164 (the mullion 0.16 of its 1.0 m light) | kit 50 / 55; target 70 / 80 | D5: partly followed |
| transom bar face | 39 | 80 (the street's transom is a high toplight transom) | not comparable: P1's bar is a mid glazing bar |
| stallriser panel (a framed cast grille) | 580 high | 525 (panel zone) | the same order |
| shop door (door plane) | leaf 2624 high; glazed from 0.328 to 0.952 of it | 2040; scene glazed from 1000 (0.49) | D2: 700 (0.343); the books say two-thirds glazed |
| door foot strip | 29 high | - | added: 30 high brass strip |

**Why P1 still holds for a 1900-1935 provincial parade, and where it does not.**

- It holds for the **order and proportion of the members** that every period front shares: a plinth taller than the stallriser, a shaft about 8 to 9 widths high, a necking and a capital about one shaft-width high, a fascia field of about half a metre, a sill group much deeper than a bead, a stallriser panel in a frame, a shop door two-thirds glazed. Each ratio is compared with the street's own fixed numbers in the rules of section 14 (R1 to R8): the seven the target follows agree within 12 per cent and the eighth (the crown) is the stated departure D7, which is the best argument that the street's numbers (the scene's) are of the right kind.
- It does **not** hold for: absolute sizes of a heavy arcade's joinery (its mullion is 0.16 of its light, the street's 0.06); a stone- or cement-faced pier's finish (it has sharp arrises and no panel); the crown's height (three times the street's); anything with a scroll, a leaf, a roller shutter, a box sign, aluminium or a lobby, because P1 shows none; and anything about 1990 (it is a 2019 restoration in fresh gloss).
- Where a P1 proportion and the street's fixed number disagree beyond the error, section 14 says which won and why.

**Which parts rest on what** (the brief asks plainly):

| part | photographs measured today (P1, P2) | the earlier notes (cited, not re-read) | judgement |
|---|---|---|---|
| pilaster | plinth top 800 (ratio to the front's height 0.228 and to the sill 1.27); shaft 290 wide (290.1 +-8 per cent at the measured scale); shaft proud 110 (118 +-14); capital 310 (301 +-24); the order of members: stepped plinth, shaft, necking ledge, die, flare, abacus; the three-boss die (optional) | panelled and fluted timber types; plinth at least the stallriser's height (RBKC); 0.35 slot and 0.10 proud (the scene); the pairs at the party wall (scene, DOWNPIPE note) | every moulding's profile (astragal r 12, flare hollow, ovolo), the sunk panel's depth 12 and bead 10, the flutes' 12, the stepped plinth's set-backs, the clad variant's sheets; the downpipe chase |
| console | nothing | envelope 240 x 180 x 550 and the S silhouette of the built mesh (fascia-01); consoles at each end of the fascia on the capitals (FRONTAGE: CV, KC, CW) | the smoothing, the volute, the acanthus leaf, the block variant; NO PHOTOGRAPH of a scrolled console was reached |
| fascia_board | vertical face; a field with a mould where it meets the capital | 5410 x 550 x 120 (fascia target, kit); not more than 600 and a fifth of the front (CV, RI) | the bed mould's 40 x 12; board thickness 25 |
| cornice | a crown of several members (cyma, corona, fillets) | 215 x 150 x 5892, the drip groove, the 27 degree wash, the lead (fascia-01) | the 19-point profile's member sizes |
| sill | a deep sill group (140 mm: bead, cove, soffit) over the stallriser's frame; sill top 0.18 of the front (0.64 m at 3.55 m; the scene's 600 is 6 per cent under) | weathered top, drip, cill 'substantial' (BH, CW); Ellis's stout sill 3 in | 75 thick, the throat 6 x 6, the weathering 15 degrees |
| stallriser | a framed panel under the sill, a bottom rail above the foot (P1: a cast grille panel, 580 high) | 600 and 0.15 proud (scene); panelled, glazed tile, render; patterned tile and plain glazed tile on metal fronts (R05, R09); white tile and slab in fish shops | tile sizes and courses, the 2 x 2 pattern, the slab, the boarded sheet |
| window_frame | a mid transom bar and a heavy mullion (164 mm, 0.16 of the light): partly followed; stile 145 mm: not followed | sill 600 to head 2850, transom 2400 to 2480, toplights, mullions 40-70 proud of the glass, glass 30 forward (scene, kit, CW) | every section's size and shape (T1, T2, M1, M2), bead sizes, bar positions, toplight counts |
| shop_door | glazed from 0.328 of the leaf (700 on 2040); a 30 mm brass foot strip | 900 x 2040, frame 1006, kick plate, letter plate, levers, hinges (kit); 'two-thirds glazed' (BH); bottom rail 9 in (Ellis) | rail and stile widths, the lock rail, furniture heights, the aluminium and bronze leaves |
| side_door_slot | nothing | the front-door family's F1 (its own photographs P2 and the books) | the mapping into the bay (d 100, z + 45, the trimmed head and threshold) |
| lobby | nothing | recessed lobbies with terrazzo or tiled floors (CW, HE1, HE2); a recessed doorway and tiled threshold in Marshall's West Dock Cafe (R05 reading) | the depths 600 and 300, the returns, the floors' patterns |
| alterations | roller-shutter hood depth (150 to 300) and rail width from CC0 scans (P2) | metal fronts, patterned tile, letting boards, whitewash (R05, R09, DECISIONS 3 Oct) | every section size, every colour, the box sign and flat panel depths (the fascia target's) |

**Edges measured on P1 and laid on it.** The drawing's projected edges (the instance polygons) fall on the saved previews within 4 px (8 px for the weakest edges); 34 edges were tested and the worst is 0.03 px. These edges were measured on the same crops that the previews are made from, so this test shows that the polygons are built from the measurements correctly, that JPEG compression does not move them, and that the snap is reproducible: it is NOT an independent validation of the numbers (that is what the ratio rules and the street's fixed numbers are for). The previews are crops of the joinery only, with the house numerals and one logo fragment masked; no whole frame and no lettering is in any preview.

## 4. The bay: datum, zones, planes

| item | value (mm) | kind | source |
|---|---|---|---|
| bay width, party line to party line | 6000.0 | Read | scene bay_width_m 6.0 |
| pilaster slot at each party wall | 350.0 | Read | scene pilaster_width_m 0.35 |
| opening zone between the piers | 5300.0 | Derived | 6000 - 2 x 350 |
| side-door slot (F1 + 24.4 filler each side) | 944.0 | Read | kit README (944); F1 opening 895.2 + 2 x 24.4 |
| shop-door slot | 1006.0 | Read | kit README (900 leaf + 2 x 3 gap + 2 x 50 jamb) |
| window, with a side door / without | 3350 / 4294 | Derived | 5300 - 944 - 1006; 5300 - 1006 |
| sill top / sill underside | 600 / 525 | Read / Judgement | scene stallriser 0.60; the sill is 75 thick (D8) |
| transom / head / fascia / cornice (z) | 2400-2480 / 2790-2850 / 2850-3400 / 3400-3550 | Read | scene; fascia target; fascia-01 |
| d: shaft front / plinth front / capital top front | 110 / 150 / 130 | Photo (110) / Read / Read | D3; kit |
| d: fascia face / console front / cornice nose | 120 / 180 / 215 | Read | fascia target; fascia-01 |
| d: sill nose / stallriser face / frame fronts / mullion front / glass | 150 / 125 / 95 and 100 / 92 / 30 | Read / Read / Judgement / Judgement / Read | kit; the mullion front is 62 in front of the glass (D5) |

The zones fill the opening: **door end on the viewer's LEFT**: side door [350, 1294], shop door [1294, 2300], window [2300, 5650]; **RIGHT**: window [350, 3700], shop door [3700, 4706], side door [4706, 5650]; with no side door (the grocer) the shop door takes the outer 1006 and the window the other 4294. The side door is the outermost zone, next to the pier, as the street's frames show. Self-check group 5 recomputes all ten fronts' zones.

## 5. Pilaster

**The kit gets right:** plinth, shaft, capital in that order, as every source and P1 show; shaft 290 wide; 350 at the plinth and the capital's top, which makes the party-wall pair stand 0.70 m wide; panelled and fluted shafts as the period's timber types; a necking bead, a die with a raised tablet, a cap moulding; the backing core, so no daylight shows between pilaster and frames.

**The target changes:**

| change | reason | kind |
|---|---|---|
| plinth top 600 -> 800 | P1: the plinth's top stands 1.27 times the sill's top (1.12 m against 0.88 m at the measured scale) and 0.228 of the front's height; scaled to this street's 3.55 m that is 0.81. RBKC (the earlier reading, KC) wants the stallriser not above the pilaster's base: the sill then lands inside the plinth's height | Photo |
| shaft projection 100 -> 110 | P1: the shaft's right return measures 30.8 px at 1087 px from the axis: 118 mm +-14 | Photo |
| capital 330 -> 310 high | P1: neck to the top of the abacus is 174 px, 1.04 times the shaft's width: 301 mm +-24 at the measured scale | Photo |
| a stepped plinth variant (render), a flush clad variant (Mickey's, as built) | P1 shows four stepped members on the plinth; the Hook sheet and the street show Mickey's piers flat and plain | Photo and Sheet |
| the capital's flare (a hollow echinus 90 high) and an optional three-boss die | P1 shows the die with three roundels under a flared cap; the kit's cap is a straight moulding | Photo |

| item | value | kind | source |
|---|---|---|---|
| slot / height / plinth top | 350 / 2850 / 800 | Read / Read / Photo | scene; kit; R1, R2 |
| plinth proud / width | 150 / 350 | Read | kit (the sill's nose is also 150) |
| shaft width and place | 290 at u 30 to 320 of the slot | Photo (290.1 +-8%) and Read | P1; kit |
| shaft proud | 110 | Photo | 118 +-14% (D3) |
| neck z, capital height, capital top z | 2540, 310, 2850 | Derived / Photo / Read | 2850 - 310; P1 301 +-24; the console stands on it |
| capital top face | 350 x 130 | Read | kit; the console's toe (240 x 60) stands wholly on it |
| capital members (z local from the neck) | astragal 0-24 (r 12), fillet 24-34, die 34-154 with a tablet 170 x 80 x 8 proud, hollow flare 154-244 (d 114 to 128), abacus 244-296 (d 130), ovolo top 296-310 | Judgement from P1's order | P1 shows a necking ledge, a die with three roundels, a flared cap, a band |
| optional bosses | 3 x diameter 30, 6 proud, pitch 56, on the die's centre line at z local 94 | Photo (P1's three roundels) | off by default (Rita's is plain); allowed on the ironmonger's and the empty unit's |
| panelled shaft | stiles 45, sunk 12, bead 10 (quarter-round), bottom rail 800-940, top rail 2430-2540 | Judgement (the kit's) | FRONTAGE: raised and fielded or panelled (BC1, BH) |
| fluted shaft | 5 flutes, 43.6 wide, 12 deep, between 12 fillets | Judgement (the kit's) | HE1 Skipton: fluted pilasters with consoles |
| render variant: stepped plinth | blocks to 504 / 631 / 680, cap slab to 800, each 4 to 8 back in depth and 15 / 26 / 38 in on the FREE side only | Photo (P1's four stepped members: tops at 0.63 / 0.79 / 0.85 / 1.0 of the plinth) | R1 |
| clad variant (Mickey's, as built) | 350 wide, 100 proud, no plinth, no capital, sheet joints at z 1200 and 2400, 6 wide | Judgement | the Hook sheet and the street |
| downpipe chase | 76 wide (u +-38) from d 50, through both neighbours' plinths (z 0-800) and capitals (2540-2850) | Judgement | the D5 pipe's own numbers (68 across, axis 94) |

Profiles (target.json `parts.pilaster.profiles`):

| profile | plane | points (mm) | note |
|---|---|---|---|
| `plinth_cap_side` | d-z | (0, 720) (150, 720) (150, 764) (147, 770) (130, 794) (124, 800) (0, 800) | the weathered cap: a 44 mm nose face, a 6 mm bead, then the top falling 30 mm toward the street over 23 mm (the kit's steep weathering); the shaft's foot stands on the flat (d 0 to 124) |
| `plinth_panel_side_through_stile` | d-z | (0, 0) (150, 0) (150, 764) (147, 770) (130, 794) (124, 800) (0, 800) |  |
| `plinth_panel_side_through_field` | d-z | (0, 0) (150, 0) (150, 120) (146, 124) (138, 132) (138, 708) (146, 716) (150, 720) (150, 764) (147, 770) (130, 794) (124, 800) (0, 800) | sunk 12 mm between the stiles; 45 degree sticking at the field's edge; the quarter-round bead is a separate planted piece |
| `plinth_stepped_side` | d-z | (0, 0) (150, 0) (150, 504) (146, 504) (146, 631) (142, 631) (142, 680) (136, 680) (136, 770) (133, 776) (120, 800) (0, 800) | four members as the photograph: block (0 to 504), a step (504 to 631) 4 mm back, a step (631 to 680) 8 mm back, a weathered cap slab (680 to 800) |
| `panel_bead` | a-p | (0, 0) (12, 0) (11.09, 4.59) (8.49, 8.49) (4.59, 11.09) (0, 12) | quarter-round, 12 mm, planted in the angle of the sunk field |
| `shaft_panel_plan` | u-d | (30, 0) (320, 0) (320, 110) (275, 110) (275, 108) (273.5, 102.9) (270, 99) (265, 98) (85, 98) (80, 99) (76.5, 102.9) (75, 108) (75, 110) (30, 110) | through the sunk field: 45 mm stiles at full projection, the field 12 mm down, a 10 mm quarter-round bead each side |
| `shaft_render_plan` | u-d | (30, 0) (320, 0) (320, 108) (317, 110) (33, 110) (30, 108) | plain face, arrises eased 3 mm by paint build-up |
| `clad_plan` | u-d | (0, 0) (350, 0) (350, 96) (346, 100) (4, 100) (0, 96) |  |
| `capital_side` | d-z | (0, 0) (110, 0) (114.59, 0.91) (118.49, 3.51) (121.09, 7.41) (122, 12) (121.09, 16.59) (118.49, 20.49) (114.59, 23.09) (110, 24) (116, 24) (116, 34) (114, 34) (114, 154) (114.27, 171.56) (115.07, 188.44) (116.36, 204) (118.1, 217.64) (120.22, 228.83) (122.64, 237.15) (125.27, 242.27) (128, 244) (130, 244) (130, 296) (129.6, 300) (128, 304) (126, 308) (124, 310) (0, 310) | z is local from the neck (add NECK_Z 2540): astragal (r 12), neck fillet, die, a hollow flare 90 high from d 114 to 128, abacus 52, a small ovolo top; flat top at 310 (z 2850) from the wall to d 130, where the console's toe and the fascia's bed mould meet it |

`shaft_flute_plan` has 59 points. The elevation of each variant is in `variants.<v>.elevation` (rectangles and trapezoids in u, z).

**Joints and meets.**

- **pilaster shaft and plinth:** the shaft stands on the cap's flat; a 3 mm shadow line at the foot where paint has filled the gap; the base mould (a small ogee 25 x 60 in the kit) is dropped: P1 shows none, the plinth's cap takes the shaft directly (Photo).
- **pilaster pair at the party wall:** two 350 piers butt at u = 0 / 6000: a vertical joint 2 mm wide, paint-cracked, 0 to 2850; capitals touch; plinth caps touch. The shafts (290 in a 350 slot) stand 60 apart across the party line. The D5 downpipe (68 across, axis 94 from the wall, so d 60 to 128) stands in that gap, 18 proud of the shafts' faces (110); the plinths and the capitals are notched for it by a chase 76 wide (u +-38) from d 50 to their fronts (z 0 to 800 and 2540 to 2850); the cornice stops 54 short of each side and the consoles stand 110 apart, so the pipe passes all the way up.
- **console and capital:** the toe 240 x 60 stands on the abacus's top at z 2850, centred on u 175 / 5825; 0.0 mm gap; two 12 mm hardwood dowels 40 deep from the toe into the capital; two M10 coach screws through the console's back into the wall plate (hidden).
- **stallriser and plinths:** the stallriser's ends butt the plinths' sides; the plinth is 25 proud of the stallriser face and 0 to 25 of the sill's nose; a 2 mm line.
- **sill and plinth:** the sill's ends are cut round the plinth's cap and stop 3 short of the plinth's side.

**Edges.** Timber: arrises square from the saw, eased 1 to 2.5 by repainting. Render: arrises run to a 1 mm radius. The plinth cap's nose is a 6 mm bead; the astragal a half-round r 12. Painted-over screw heads at 600 pitch in two lines 40 from the edges.

## 6. Console

**The kit gets right:** the 240 x 180 x 550 envelope of the street's built mesh and its toe 60 deep standing on the capital's top; the console centred on the pilaster, gap 0.0 mm.

| change | reason | kind |
|---|---|---|
| the S curve smoothed (53 points) and given a volute on each side face and an acanthus leaf on the face | the built mesh is a few flat steps (README: coarse beside the kit); the brief asks for the scroll and its leaf; NO photograph of a scrolled console was reached | Judgement |
| a plain block variant (the grocer) and an absent variant (the empty unit's left console) | 1930s fronts; fascia-01 spec | Judgement |

| item | value | kind | source |
|---|---|---|---|
| envelope | 240 wide x 180 deep x 550 high, z 2850 to 3400 | Read | fascia-01 (the built mesh) |
| centre | u 175 and 5825; ranges 55-295 and 5705-5945 | Read | the kit's meet; fascia-01 |
| toe | 240 x 60 at z 2850, a rounded nose r 14 to d 74 | Read | fascia-01 profile |
| silhouette | the built profile's 11 key points, Catmull-Rom smoothed to 53 points | Judgement on a Read | self-check: every printed point within 4.5 mm |
| volute (each side face) | groove 5 wide, 4 deep, 1.75 turns from r 3 to r 24 about (d 34, z 82) | Judgement | the brief's 'scroll'; no photograph |
| leaf (the front) | acanthus pendant, z local 120 to 440, up to 120 wide at the top falling to a tip, 3 lobes a side, relief 12 at the rib, a rib 8 wide 4 proud, grooves 4 x 3 between lobes | Judgement | no photograph |
| front chamfer | 12 down each front edge | Read | fascia-01 taper (1 part in 15) |
| variants | scroll (all original fronts); block (the grocer): S straightened to a 45-degree chamfer, no leaf, three bosses; absent (the empty unit's left: a stump 240 x 60 x 90 and two dowel holes) | Judgement | fascia-01 spec (the clipped console) |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `side_silhouette` | d-z | 53 points, see target.json | z local from the console's foot (add 2850); the same envelope as the built fascia_console_01; wall at d=0 (back), the cornice's soffit meets the top |
| `plan_at_neck` | u-d | (-120, 0) (120, 0) (120, 168) (108, 180) (-108, 180) (-120, 168) | 240 wide, 12 mm chamfer down each front edge (the built mesh's per-station taper) |
| `leaf_outline` | u-z | (-58, 440) (-60, 420) (-52, 396) (-46, 384) (-54, 368) (-50, 344) (-42, 330) (-48, 312) (-42, 288) (-34, 272) (-38, 252) (-30, 232) (-24, 212) (-18, 190) (-9, 160) (0, 120) (9, 160) (18, 190) (24, 212) (30, 232) (38, 252) (34, 272) (42, 288) (48, 312) (42, 330) (50, 344) (54, 368) (46, 384) (52, 396) (60, 420) (58, 440) | u from the console's centre line, z local; relief domed 12 mm at the rib, 0 at the outline |

`volute_spiral` is an open curve of 41 points. **Fixings:** two 12 mm hardwood dowels 40 deep from the toe into the capital and two M10 coach screws through the back into the wall plate, all hidden; a rust bleed 20 long under each on the shaded side. **What P1 shows of consoles: nothing** (its pier caps are straight stepped blocks); the scroll and leaf are Judgement and are marked as such in the evidence table.

## 7. Fascia board, bed mould, cornice

**Fascia board** (kit gets right: the board between the consoles, 295 to 5705, 120 proud, z 2850 to 3400 (the fascia target's)). Changes: a 40 high bed mould at the foot, 12 proud of the face (P1 shows the fascia field framed by a mould where it meets the capital; the board's foot would otherwise be a bare box edge on the abacus); the face stays vertical (P1 shows a vertical field; the guide's 'sloped slightly forward' (Coventry, the earlier reading) is a book and the photograph wins (D6)).

| item | value | kind | source |
|---|---|---|---|
| board | u 295 to 5705 (5410), z 2850 to 3400 (550), face d 120, 25 thick on rails | Read | the fascia target (it fixes the board: the lettering and the texture are its); the kit |
| bed mould | z 2850 to 2890, front d 132 (12 proud of the face, 2 proud of the capital's top front) | Judgement (Photo for the idea) | P1's field is framed where it meets the capital |
| face | one vertical plane | Photo | D6: P1; the book's 'sloped slightly forward' loses |
| foot on the capital | 55 each end (u 295 to 350, 5650 to 5705) | Derived | 350 - 295 |
| ends | let into the consoles' inner sides by a 12 rebate | Judgement | - |
| boxed, panelled or glazed | a box sign (laundry 5200 x 480 x 150, newsagent 5220 x 470 x 140) or a flat panel (tea 5230 x 470 x 30) stands on this board; the grocer's board is three glass slabs on a backing in the same plane | Read | the fascia target |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `section` | d-z | (0, 0) (132, 0) (132, 10) (129, 22) (123, 34) (120, 40) (120, 550) (0, 550) | z local from the board's foot (2850); the bed mould's front stands 12 proud of the face and 2 proud of the capital's top front (130), so the board's foot overhangs the capitals by the mould only |

**Cornice** (kit gets right: 215 deep x 150 high x 5892 long, the drip groove outside the board's face, the wash, the lead apron (not geometry)). Changes: the profile redrawn with a tall corona face (52, 0.35 of the height), two fillets, a cyma reversa and a cap ovolo (19 points) inside the same envelope (the built profile has 12 points and one curve; P1 shows a crown of several members); the 150 height is KEPT although P1's crown is 0.86 of its fascia field where the street's is 0.27 (about three times) (the fascia target fixes the cornice top at 3.55 and the hanging signs' brackets at 3.60 over it; an optional tall cornice (300) is recorded in variants for the reviewer to overturn).

| item | value | kind | source |
|---|---|---|---|
| envelope | 5892 long (u 54 to 5946) x 215 deep x 150 high, soffit at z 3400, top at 3550 | Read | fascia-01; the fascia target's cornice top 3.55 |
| drip groove | d 155 to 175, 12 deep (35 outside the board's face) | Read | fascia-01 |
| oversail | 95 past the board's face, 35 past the console's front | Derived | 215 - 120; 215 - 180 |
| corona face | 0 to 52 (0.35 of the height) | Photo (P1's plain face is 0.39 of its crown) | the sequence in section 3 |
| wash | falls 20.0 degrees from d 205 at z 130 to the back at 150; lead 1.8 over it, an apron 100 up the wall, upstands 25 at each end (not geometry) | Judgement on a Read | fascia-01: 27 degrees; the 4.5 degrees of change is for the new profile |
| stops short of each party line | 54 (108 between neighbours; the pipe is 68) | Derived | fascia-01's arithmetic |
| tall variant | 300 high x 280 deep (z 3400 to 3700): offered for a reviewer who reads P1's crown as binding; collides with the signs' brackets at 3.60 | Photo (not followed) | D7 |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `section` | d-z | (0, 0) (155, 0) (155, 12) (175, 12) (175, 0) (215, 0) (215, 52) (211, 56) (211, 60) (205, 68) (201, 76) (200, 86) (203, 90) (207, 98) (208, 110) (207, 124) (205, 130) (150, 150) (0, 150) | z local from the soffit (3400): flat soffit, drip groove 12 deep, a tall corona face 52 (0.35 of the height, as P1's plain face is 0.39 of its crown), a fillet, a cyma reversa back to d 200 at z 86, a fillet, a cap ovolo out to d 208 at z 110, a short face, then the wash falling 20 mm over 55 mm to a flat top at 150 that runs back to the wall |

## 8. Sill and stallriser

**Sill.** Kit gets right: a weathered top falling to a rounded nose with a throat, 150 proud, 600 high. Changes: 50 thick -> 75 thick (z 525 to 600) with the throat 16 back from the nose (Ellis (the earlier reading) calls the stallboard 'the stout sill' (no figure); P1's sill group is 80 px (142 mm) deep with a bead, a wide cove and a soffit; a 50 mm sill reads as a ledge; 75 is Judgement).

| item | value | kind | source |
|---|---|---|---|
| z range / thickness / nose d | 525 to 600 / 75 / 150 | Read (600, 150) / Judgement (75) | scene; Ellis's stout sill (the earlier reading); P1's sill group is 140 deep |
| throat | d 128 to 134, 6 deep, 16 back from the nose | Judgement | - |
| weathering | 24 mm over 82 mm (15 degrees) to a flat bed 60 deep | Judgement | Ellis: top edges bevelled to shed rain |
| length | the window frame's 3350 plus 40 under each jamb (3430) | Judgement | - |
| fixing | No. 12 countersunk screws at 450 (7 along 3350), pellet-plugged, painted over | Judgement | - |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `section` | d-z | (0, 525) (128, 525) (128, 531) (134, 531) (134, 525) (144, 525) (150, 531) (150, 566) (147, 572) (142, 576) (60, 600) (0, 600) | 3 in (75 mm) sill, a bullnose of r 6, a 6 x 6 throat 16 back from the nose, top weathered to a flat bed 60 deep where the frame's bottom rail stands |

**Stallriser** (kit gets right: panelled (raised and fielded, 3 panels) and glazed-tile variants, 600 high, face 125; the plinth, skirting 120). Changes: six more variants: square tile, patterned tile, glass slab, render, boarded, and a grille (available, unused) (the ten fronts need them: P1 shows a framed grille panel, and the earlier reading of R05 a patterned tile).

| variant | use | numbers |
|---|---|---|
| panel | timber panelled: a plinth 120, bottom rail 80, three raised and fielded panels between 80 stiles and muntins, top rail 80 (Rita's; the kit) | {"plinth": 120.0, "stile": 80.0, "bottom_rail": [120, 200], "top_rail": [445, 525], "panel_inset": 14.0, "field_margin": 35.0, "field_rise": 12.0, "bead": 14.0, "panels_rule": "one panel per light of the window above, 3 on 3350 (muntins on the mullion lines)"} |
| tile | glazed brick-shaped tile 152 x 72 in stretcher bond, 3 mm joints, a 120 skirting course of 304 x 117, then 5 courses of 75 (72 + joint), a bullnose capping 30 high (r 12): 120 + 375 + 30 = 525 | {"tile": [152.0, 72.0], "joint": 3.0, "skirting": [304.0, 120.0], "capping_height": 30.0, "capping_r": 12.0, "courses": 5, "course_pitch": 75.0, "bond": "stretcher, half-lap"} |
| tile_square | glazed square tiles 152.4 (6 in), 3 mm joints, a black skirting 100, two full courses and one half course (152.4 x 76.2), a bullnose cap 35: 100 + 2 x 155.4 + 79.2 + 35 = 525 (fish and laundry white, chandler pale green) | {"tile": [152.4, 152.4], "half_course_tile": [152.4, 76.2], "joint": 3.0, "skirting": 100.0, "courses": 2, "half_courses": 1, "course_pitch": 155.4, "half_course_pitch": 79.2, "capping_height": 35.0, "bond": "straight (stack)"} |
| tile_patterned | 6 in tiles with a printed diamond-lattice pattern in a 2 x 2 repeat (Mickey's: cream, mid blue, black), black skirting 100, two full courses patterned, one plain half course, cap 35: as tile_square | {"tile": [152.4, 152.4], "joint": 3.0, "skirting": 100.0, "courses": 2, "half_courses": 1, "course_pitch": 155.4, "half_course_pitch": 79.2, "capping_height": 35.0, "repeat": "2 x 2 tiles = 304.8 square: A cream with a mid-blue diamond whose corners touch the tile's edge midpoints and a black dot at |
| slab | opaque coloured structural glass in three slabs, bottle green, polished, 6 mm chrome capping, 3 mm black mastic joints (the grocer) | {"slabs": 3, "joint": 3.0, "bevel": 2.0, "capping": {"height": 18.0, "material": "chrome strip"}, "z_range": [0, 525]} |
| render | painted render with a rendered cill under the sill (cheap 1920s-50s repair), or hardboard painted (the tea rooms) | {"coat": 12.0} |
| grille | available, not used by the ten fronts: pierced cast-iron or pressed-metal ventilation panels in the panel variant's frame, one per light, as P1's stallriser (a framed grille 580 high at the measured scale); the earlier reading (Dover guide) mentions grilles under the fascia too | {"bars": 12.0, "open_fraction": 0.6, "set_back": 20.0, "backed_by": "black mesh", "field_height": 245.0} |
| boarded | the empty unit: the panelling painted out, a sheet of ply or hardboard screwed over the lower 525 with 12 screws, paint peeling | {"sheet_thickness": 9.0, "screws": 12} |

The stallriser is 0 to 525 under the sill, face d 125 (25 behind the plinth's 150 and the sill's nose). Tiled kinds: joints 3 mm, the tile's cap bullnose r 12 (brick tile) or a 35 high cap tile; courses add to exactly 525 (self-check). The brick-tile section and the panel section are `variants.tile.section` and `variants.panel.section`.

## 9. Window frame, mullions, transom, toplights, glazing

**Kit gets right:** sill 600 to head 2850, transom 2400 to 2480, mullions in front of the glass, glass 30 in front of the wall; toplights in a shallow row; the transom's weathered top, drip and nose (a book detail, also seen in P1).

| change | reason | kind |
|---|---|---|
| mullion 55 -> 70 wide, front at 92 (62 in front of the glass) | P1's mullion is 92 px wide (164 mm at the wall plane) against a 1.0 m light: 0.16 of the light, the kit's 0.05. The guides' 40 to 70 mm is a projection. Not followed in full (D5) | Photo, partly followed |
| a bottom rail 90 high on the sill; glazing beads; four more types: T2, M1, M2 | P1's stallriser frame carries a bottom rail and the lights stand on it; the street needs timber, aluminium and 1930s bronze fronts | Photo and Judgement |

| item | value | kind | source |
|---|---|---|---|
| frame length | 3350 (4294 with no side door), z 600 to 2850 on the sill | Derived | section 4 |
| bottom rail | z 600 to 690 | Photo (P1's stallriser frame carries one) | Judgement for 90 |
| lower lights / transom / toplights / head | 690-2400 / 2400-2480 / 2480-2790 / 2790-2850 | Read | scene transom 2.40, 0.08; kit head |
| jamb | 50 face x 95 deep, glazing rebate 12 x 12 | Read (kit 50, 85) / Judgement | frame fronts at d 95 sit 15 behind the shaft's 110 |
| T1 mullion | 70 x front d 92 (62 in front of the glass), oval nose, rebates 10 x 12 | Judgement; Cornwall guide 40-70 projection | D5 |
| T2 mullion | 80 x d 92, flat face with a quirk bead each edge | Judgement | the older, heavier section |
| M1 / M2 | aluminium 50 x 75 box with glazing pockets; bronze-plated 28 x 40 | Judgement | R05, R09 (the earlier reading) |
| toplight bars | 28 wide (T1, T2, M2) or 50 (M1), counts per fronts[].glazing | Judgement | the kit's 8 lights on Rita's |
| glass | 6 mm plate at d 30, in 12 mm rebates; beads: T1 ovolo 16 x 12 on brass screws at 250; old putty 14 x 10 (T2, the empty unit); M1 snap-in bead 14 x 8 over a black gasket | Read (30) / Judgement | kit; FRONTAGE |
| mullion positions | the kit's default is n = ceil((L - 100) / 1250) - 1, at most 3 (2 on 3350); the table sets the number per front (fish 3, laundry 1, ironmonger 1, grocer 2 on 4294); positions per shop in `shops[].glazing_layout` (mullion centres from the frame's left edge, toplight bars, light widths) | Derived | the kit's rule; the table |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `mullion_t1_plan` | u-d | (35, 0) (35, 24) (25, 24) (25, 36) (35, 36) (35, 60.5) (32.34, 72.55) (24.75, 82.77) (13.39, 89.6) (0, 92) (-13.39, 89.6) (-24.75, 82.77) (-32.34, 72.55) (-35, 60.5) (-35, 36) (-25, 36) (-25, 24) (-35, 24) (-35, 0) | 70 wide, oval nose, front at d 92 (62 in front of the glass at 30); glazing rebates 10 x 12 in both sides |
| `mullion_t2_plan` | u-d | (40, 0) (40, 24) (30, 24) (30, 36) (40, 36) (40, 82) (36, 86) (32, 88) (26, 86) (24, 92) (-24, 92) (-26, 86) (-32, 88) (-36, 86) (-40, 82) (-40, 36) (-30, 36) (-30, 24) (-40, 24) (-40, 0) | 80 wide flat face with a quirk bead at each edge (the heavier, older section; the empty unit and the ironmonger) |
| `mullion_m1_plan` | u-d | (25, 0) (25, 44) (17, 44) (17, 56) (25, 56) (25, 72) (22, 75) (-22, 75) (-25, 72) (-25, 56) (-17, 56) (-17, 44) (-25, 44) (-25, 0) | aluminium box 50 x 75 with glazing pockets 12 deep; a snap-on cover cap 38 wide, front at d 75 (metal fronts) |
| `bar_m2_plan` | u-d | (14, 0) (14, 24) (11, 24) (11, 30) (14, 30) (14, 33) (12.12, 36.5) (7, 39.06) (0, 40) (-7, 39.06) (-12.12, 36.5) (-14, 33) (-14, 30) (-11, 30) (-11, 24) (-14, 24) (-14, 0) | M2 (1930s): a bronze-plated bar 28 wide, front at d 40, rounded; 3 mm rebates; the jamb is the same bar cut square |
| `jamb_t1_plan` | u-d | (0, 0) (50, 0) (50, 24) (38, 24) (38, 36) (50, 36) (50, 95) (3, 95) (0, 92) | 50 face x 95 deep with the glazing rebate on its inner side |
| `jamb_m1_plan` | u-d | (0, 0) (50, 0) (50, 44) (38, 44) (38, 56) (50, 56) (50, 72) (47, 75) (3, 75) (0, 72) | M1: aluminium jamb 50 x 75 with a glazing pocket 12 deep; a snap-on cover cap not drawn |
| `transom_t1` | d-z | (0, 0) (70, 0) (70, 6) (77, 6) (77, 0) (96, 0) (100, 4) (100, 46) (98, 51) (93, 54) (46, 80) (0, 80) | z local from 2400: a 6 x 7 drip groove under the nose at d 70 to 77, the nose at d 100, the top weathered 26 mm over 47 mm to the glass bed; as the kit's |
| `transom_m1` | d-z | (0, 0) (50, 0) (50, 4) (54, 4) (54, 0) (75, 0) (75, 40) (70, 46) (32, 50) (0, 50) | M1: a 50 high box, 75 deep, top sloped 4 mm over 38, a 4 x 4 drip at d 50 to 54 |
| `toplight_bar_plan` | u-d | (14, 0) (14, 24) (8, 24) (8, 36) (14, 36) (14, 38) (12.12, 46.5) (7, 52.72) (0, 55) (-7, 52.72) (-12.12, 46.5) (-14, 38) (-14, 36) (-8, 36) (-8, 24) (-14, 24) (-14, 0) | 28 wide, rounded front at d 55, glazing rebates |
| `glazing_bead_ovolo` | a-p | (0, 0) (16, 0) (16, 2) (14, 7) (10, 10.5) (5, 12) (0, 12) | T1: planted ovolo 16 along the face x 12 proud |
| `glazing_bead_gasket` | a-p | (0, 0) (14, 0) (14, 5) (11, 8) (3, 8) (0, 6) | M1: a snap-in bead 14 x 8 over a black gasket |
| `glazing_putty` | a-p | (0, 0) (14, 0) (0, 10) | old putty-glazed lights: a 45 degree fillet 14 x 10, cracked and painted over |
| `head_section` | d-z | (0, 0) (95, 0) (95, 60) (0, 60) | z local from 2790: a plain 95 x 60 rail under the fascia's foot |

**Joints.** window frame and sill: the bottom rail (z 600 to 690) stands on the sill's flat bed (d 0 to 60), screwed from below through the sill; a mastic line at the junction (1 mm); window frame and pilaster / door frames: the end jambs (50 x 95) close against the pilaster's backing core and the door frames' jambs; a 3 mm paint joint; no daylight; transom and jambs: the transom is housed 10 mm into each jamb with a stub tenon, drawbore-pegged inside; outside only a 1 mm line shows; mullions and transom/bottom rail: mortice and tenon, 25 mm tenon, wedged; end grain not visible after painting; the mullion stops at the transom (z 2400) and the toplight bars start on it.

## 10. Shop door, side-door slot, lobby

**Shop door.** Kit gets right: leaf 900 x 2040, frame 1006 wide, 100 deep, kick plate, letter plate, lever handles, three hinges, terrazzo threshold.

| change | reason | kind |
|---|---|---|
| glazed from 1000 -> 700 | P1's door is glazed from 0.328 of its leaf's height (0.86 of 2.62 m); the books say two-thirds glazed (0.6 to 0.7 m): the photograph and the books agree and the scene's 1.0 is a trade-standard guess. The door's lower portion is then bottom rail 230, panel 360, lock rail 110 | Photo and Read |
| a 30 high brass foot strip across the leaf | P1's door foot carries one (15 px, 29 mm) | Photo |
| aluminium and bronze door variants | the refits | Judgement |

| item | value | kind | source |
|---|---|---|---|
| leaf / slot / thickness | 900 x 2040 / 1006 / 50 | Read (scene, kit) / Read (Ellis 2 in) | - |
| rails and stiles | stile 115, top rail 115 (1925 to 2040), bottom rail 0-230 (9 in, Ellis), lower panel 230-590 raised and fielded, lock rail 590-700, glass 700-1925 | Read (Ellis) / Judgement | P1: glazed from 0.328 of the leaf; BH: two-thirds glazed (D2) |
| glazing | one 6 mm pane, ovolo bead 14 x 11 (T1) | Judgement | - |
| kick plate / foot strip | brass 770 x 170 with 8 screws / brass 30 high across the leaf's foot, 3 proud | Read (kit) / Photo (29 mm, P1) | - |
| furniture | lever handles on 240 x 40 backplates at z 1000; a rim latch and a mortice escutcheon at 950; letter plate 250 x 40 at z 800 on the lower panel's centre | Read (kit) / Judgement | - |
| hinges | three 100 x 75 butts at 150 / middle / 150, 6 No. 8 screws each | Read | kit |
| frame and threshold | jambs 50 x 100, leaf 3 clear; terrazzo threshold 25 high at the leaf falling to 12, nose out to d 130 (flush fronts) | Read | kit |
| fanlight, transom, toplight | fanlight 2131 to 2400 (one pane); the shop's transom runs across 2400-2480; a two-bar toplight 2480-2790; head 2790-2850 | Read | kit |
| variants | T1 timber; M1 aluminium glass door 50 stiles, 100 top rail, 170 bottom rail, a 300 chrome D pull; M2 bronze, 150 kick plate | Judgement | - |

| profile | plane | points (mm) | note |
|---|---|---|---|
| `threshold_section` | d-z | (0, 0) (130, 0) (130, 10) (126, 15) (120, 17) (75, 23) (70, 25) (0, 25) |  |
| `glazing_bead` | a-p | (0, 0) (14, 0) (14, 2) (12, 6) (8, 9.5) (4, 11) (0, 11) | T1: ovolo 14 x 11 |
| `leaf_stile_plan` | u-d | (0, 20) (89, 20) (89, 31) (101, 31) (101, 20) (115, 20) (115, 70) (0, 70) | the leaf's stile (u across, d out; the leaf's outside face at d 70, inside at 20): 115 face, 50 thick; the glass rebate and the ovolo bead are on the glazing side; the 12 mm sticking on the panel side is a_p below |
| `frame_jamb_plan` | u-d | (0, 0) (50, 0) (50, 100) (0, 100) (0, 78) (14, 78) (14, 36) (0, 36) | the door frame's jamb: 50 face x 100 deep, rebated 14 x 42 for the leaf's stop; the leaf's face stands 30 behind the frame's face |
| `raised_field_edge` | a-p | (32, 0) (60, 0) (60, 10) (40, 10) | a raised and fielded panel: a flat margin 32, a bevel 8 rising 10, the field; as the kit |

**Side-door slot (the front-door family's F1, NOT re-targeted).** The slot is 944 wide: F1's opening shows 895.2 (jambs 49 past the shopfront's framing) and a 24.4 filler strip each side (the pier's return, painted the pier's colour). It sits in the bay like this:

- **x:** F1 x 0 is the left edge of the brick reveal; the slot is centred on the F1 opening (x 447.6): u_bay = u_slot_centre + (x_F1 - 447.6).
- **y:** F1 y = 0 is its brick face; its frame's outside face is at F1 y 114.3. In the bay the frame's outside face stands at d = 100 (flush with the shop door's and window's frames, 10 behind the pilaster shaft's face): d = 214.3 - y_F1, i.e. the leaf's outside face (F1 188.3) is at d 26.
- **z:** F1 z 0 is the top of its threshold, 45 above the pavement (F1 ground z -45): z_bay = z_F1 + 45. Its head's visible face (F1 2339.6 to 2400) therefore reaches z 2445: the shop transom (2400 to 2480) covers the top 45, so the builder trims the F1 head at z 2400.
- trim: the threshold board's front (F1 y 0, d 214) is cut back to d 130, flush with the shop door's threshold nose and under the plinth's 150.
- trim: F1's brick arch, quoins, plinth and step are NOT built: the shopfront holds the head.
- Above the F1 head: the shop's transom (2400-2480) runs across the slot, then a raised-and-fielded panel 2480-2790 and the head 2790-2850 (the kit's). The leaf's letter plate is 250 x 40 (scene), at F1's own height.

**Lobby.** Flush fronts have none. Recessed: the door frame's front face stands `100 - recess` (grocer 600: d -500; launderette 300: d -200); the window's end and the pier's side are returned (grocer: a glazed display return with a 600 kick panel in the green glass, and a panelled lining; launderette: both square). Floors: the grocer's terrazzo (grey with white chips, z 25, a 150 border of 20 mm tiles in cream and bottle green, a 30 x 6 brass nosing at the frame line); the launderette's 150 quarry tile, red-brown. Ceiling: plaster or board at z 2400, the toplights running on above. The shop-room's card is behind; the lobby takes 300 to 600 of the shop's depth.

## 11. How the parts meet

| between | how |
|---|---|
| pilaster shaft and plinth | the shaft stands on the cap's flat; a 3 mm shadow line at the foot where paint has filled the gap; the base mould (a small ogee 25 x 60 in the kit) is dropped: P1 shows none, the plinth's cap takes the shaft directly (Photo) |
| pilaster pair at the party wall | two 350 piers butt at u = 0 / 6000: a vertical joint 2 mm wide, paint-cracked, 0 to 2850; capitals touch; plinth caps touch. The shafts (290 in a 350 slot) stand 60 apart across the party line. The D5 downpipe (68 across, axis 94 from the wall, so d 60 to 128) stands in that gap, 18 proud of the shafts' faces (110); the plinths and the capitals are notched for it by a chase 76 wide (u +-38) from d 50 to their fronts (z 0 to 800 and 2540 to 2850); the cornice stops 54 short of each side and the consoles stand 110 apart, so the pipe passes all the way up |
| console and capital | the toe 240 x 60 stands on the abacus's top at z 2850, centred on u 175 / 5825; 0.0 mm gap; two 12 mm hardwood dowels 40 deep from the toe into the capital; two M10 coach screws through the console's back into the wall plate (hidden) |
| fascia board and console | the board's ends are let into the consoles' inner sides by a 12 mm rebate; a 2 mm paint-filled line shows on each side |
| fascia board and capital | the board's foot rests on the abacus for 55 (u 295 to 350 and 5650 to 5705) and its bed mould overhangs the abacus's top front by 2 |
| cornice and fascia | the soffit lies on the board's top and the consoles' tops at z 3400 with 0 gap; the drip groove at d 155 to 175 lies outside the board's face (120) by 35; a lead apron over the wash, 100 up the wall |
| cornice and the party wall | the cornice stops 54 short of each party line (u 54 and 5946) leaving a 108 gap between neighbours for the downpipe |
| window frame and sill | the bottom rail (z 600 to 690) stands on the sill's flat bed (d 0 to 60), screwed from below through the sill; a mastic line at the junction (1 mm) |
| window frame and pilaster / door frames | the end jambs (50 x 95) close against the pilaster's backing core and the door frames' jambs; a 3 mm paint joint; no daylight |
| transom and jambs | the transom is housed 10 mm into each jamb with a stub tenon, drawbore-pegged inside; outside only a 1 mm line shows |
| mullions and transom/bottom rail | mortice and tenon, 25 mm tenon, wedged; end grain not visible after painting; the mullion stops at the transom (z 2400) and the toplight bars start on it |
| stallriser and plinths | the stallriser's ends butt the plinths' sides; the plinth is 25 proud of the stallriser face and 0 to 25 of the sill's nose; a 2 mm line |
| sill and plinth | the sill's ends are cut round the plinth's cap and stop 3 short of the plinth's side |
| shop door frame and threshold | the terrazzo threshold (25 high) runs the frame's width; the leaf clears it by 3 mm over a brass foot strip |
| side-door slot and the shop door frame | the F1 frame's jamb and the shop door's jamb stand 3 apart under a common head strip; the transom runs across both |
| box sign / flat panel and the old board | stands on the board at the fascia target's outer rectangle; eight pan-head screws; the cornice's soffit clears its top by 35 |

**Fixings by part** (what is visible after repainting is stated; the rest is hidden):

| part | fixing |
|---|---|
| pilaster | 100 mm cut nails or No. 10 screws through the core into wall plugs at 600 pitch; heads punched and stopped; after repainting they show as faint round dots 4 mm across at 600 in two lines 40 from the edges (Judgement) |
| console | two 12 mm dowels and two M10 coach screws, hidden; a rust bleed 20 mm long under each screw hole on the shaded side after 70 years (Judgement) |
| fascia board | 50 mm cut nails at 300 along the top and bottom edges into the rails; heads stopped; the fascia target puts ten pin holes along a removed sign |
| cornice | 75 mm brass or galvanised screws through the soffit into the wall plate at 450, pellet-plugged and painted; the lead is fixed with copper clout nails at 25 along its upper edge, pointed into the brick |
| window frame | 100 mm screws through the end jambs into the pilaster core at 450; the sill screwed down through its bed (No. 12 at 450, plugged); beads on brass round-head screws at 250 (T1), snap-in (M1) |
| stallriser | panels screwed from behind into the sill and the plinth; tile on a cement-sand screed on battens; slabs on a stainless or brass clip at 400 |
| doors | three 100 x 75 butt hinges, 6 No. 8 screws each; a mortice lock and a rim night latch; the kick plate with 8 brass screws; the F1 door as its own target |
| seen on P1, not adopted | P1's pilaster shows two small iron hooks on its side return (a later fixing for a flag or a banner) and a bracket-like fixing on the shaft's right edge; the 1990 street hangs its signs from brackets on the brick above the cornice (the fascia target), so none is placed on the shafts |
| roller-shutter box | four M8 bolts per rail through the frame into the pilaster core; the hood on steel angle brackets screwed into the fascia's rail, 600 pitch; rivets on the end caps |

## 12. 1990: condition and the alterations by kind

Wear: FRONTAGE-2026-10-06.md section 3 and PAINTED-FRONTS-2026-10-07.md: paint failing at the sill and the joints, pilaster feet rotting and splashed, stallrisers stained by pavement splash up to 0.45 m, door bottoms decaying, fascias rotting from their backs; the wear layer's work (a height gradient and noise in the material), not the meshes'. The wear target (production/cloud-week/targets/wear) governs it. What the photograph shows of wear on a part: Fine white scuffs on the red plinth up to about 0.4 m, chipped arrises at the cap's edges, the sill group's bead and cove carrying bright worn lines where paint has worn through, the brass foot strip worn, a repaired patch on the plinth's foot. P1 is a 2019 restoration in fresh gloss: it shows what wear looks like on a part, not what 1990 looked like.

Geometry that wear adds to the parts: arris radius 1 to 2.5 mm on every timber edge by repainting; a 3 mm V of rot at the pilaster foot's front arris on the oldest fronts (empty unit, ironmonger); the empty unit's console stub; cracks 0.5 x 80 in a tile or slab at doors on the tiled fronts (tile and slab stallrisers); aluminium: pits and a white corrosion bloom at the foot, 40 to 60 high.

| kind | what | numbers | applies to | evidence |
|---|---|---|---|---|
| repaint | many coats of gloss over decades: arrises rounded, mouldings clogged, brush marks, runs, crazing on the sunny front, bare grey timber at sills and feet | {"arris_radius_mm": [1.0, 2.5], "hollow_fill_fraction": 0.4, "coats_visible": "3 to 6", "bare_timber_at": ["sill nose and drip", "plinth feet", "door bottom rails", "transom top"]} | mickeys, fish_market, ritas, steam_laundry, grocer, chandler, tea_rooms, ironmonger, newsagent | Judgement from FRONTAGE-2026-10-06.md section 3 and PAINTED-FRONTS-2026-10-07.md; P1 (Leadenhall) shows 2019 paint, not 1990 |
| aluminium_refit | a 1960s-80s replacement window and door in anodised aluminium, set in the old frame's opening with the old pilasters, consoles, fascia and cornice kept | {"stile_mullion_transom_face": 50, "section_depth": 75, "frame_front_d": 75, "glass_d": 30, "wall": 3, "finish": "natural silver or bronze anodised, 15 to 20 micron, dulled and pitted, white corrosion at the foot", "fixings": "self-tapping screws through the stiles into the old jambs at 400, hidden by a snap-on cover cap; corner cleats and a bead of grey mas | fish_market, steam_laundry, chandler | Judgement; R05 and R09 (the project's earlier reading of Peter Marshall's Hull photographs: metal shopfront, fluorescent strips, patterned tile) say it existed; no photograph reached today |
| steel_refit | a 1970s painted steel or aluminium front in slate blue-grey, as the Hook sheet shows; the same sections as the aluminium refit, powder-coated | {"stile_mullion_transom_face": 50, "section_depth": 75, "finish": "powder-coat, eggshell, slate (60,74,88)"} | mickeys | Sheet (mood) and the project's earlier reading of R05 |
| refit_1930s | a 1930s modernisation: bronze-plated bars 28 x 40, plate glass, a glass stallriser in three slabs, curved or plain recessed lobby with a terrazzo floor, a glass fascia | {"bar_face": 28, "bar_depth": 40, "glass_thickness": 6, "stallriser_slabs": 3, "joint": 3} | grocer | Read (FRONTAGE-2026-10-06.md: HE2 Muswell Hill 1930s, BC2 Lennie 2012: curved glass lobbies, bronze, chrome, coloured structural glass, tiled lobby floors) and the fascia target's glass board |
| box_sign | a lit plastic box over the old fascia (fascia target's geometry: laundry 5200 x 480 x 150, newsagent 5220 x 470 x 140); the old board stays under it | {"stands_proud_of_board": [140, 150], "front_d": [260, 270], "beyond_cornice_nose": [45, 55], "fixings": "eight pan-head screws through the frame into the board"} | steam_laundry, newsagent | the fascia target (Judgement there) |
| flat_panel_sign | a flat acrylic panel screwed over the old board (fascia target: 5230 x 470 x 30) | {"stands_proud_of_board": 30, "front_d": 150} | tea_rooms | the fascia target |
| roller_shutter | a steel roller shutter over the window and shop door: a hood under the fascia, two guide rails on the frames, a 77 mm slat curtain | {"hood_height": 300, "hood_depth_d": 190, "hood_z_range": [2550, 2850], "hood_front": "five-faced (octagon half)", "hood_ends": "end caps 3 mm, riveted", "guide_rail": {"face": 50, "depth": 40, "fixing": "four M8 bolts per rail through the frame into the pilaster's core, bolt heads visible"}, "curtain_slat_pitch": 77.0, "curtain_front_d": 30, "bottom_rail":  | newsagent | Photo-scan geometry measured today (hood depth, rail width); the slat pitch and the bolts are Judgement |
| empty_unit | an empty unit: the panelling painted out and a ply or hardboard sheet screwed over the stallriser, the glass whitewashed from inside, the door's lower leaf hardboarded, a TO LET board on the fascia, one console gone | {"whitewash_coverage": 1.0, "ply_sheet": [1200, 525, 9], "screws": 12, "console_absent": "viewer's left"} | empty_unit | Judgement; DECISIONS 3 Oct (whitewashed), fascia-01 spec (the clipped console) |
| recessed_lobby | the shop door set back in a lobby with a tiled or terrazzo floor and its own returns | {"grocer": {"depth": 600, "floor": "terrazzo", "mosaic_border": 150}, "steam_laundry": {"depth": 300, "floor": "quarry tile 150"}} | grocer, steam_laundry | Read (FRONTAGE-2026-10-06.md: recessed lobbies with terrazzo or tiled floors; HE1 marble threshold then mosaic; HE2 white mosaic floor) and the project's earlier reading of Marshall's West Dock Cafe: recessed doorway, tiled threshold |

**Roller-shutter box, from the CC0 scans.** The four Poly Haven shutters read today have hoods 153, 168, 300 and 300 deep for curtains 1546, 1561, 1851 and 2400 high, the curtain's plane at z 20 and rails 7 wider than the curtain: the target's hood is 300 high x 190 deep over the window and shop door (z 2550 to 2850), with the curtain at d 30 and the guide rails 50 x 40 on the frames. Raised by day (the box and the rails only); lowered at night (a variant).

## 13. The ten fronts: the assembly table

Twelve shopfronts are RULINGS' count; the scene has ten shop bays (six east, the chandler, three west). Ten are tabled. Door end is the VIEWER's side in the game. Paint columns are plain names; sRGB values are in `shops[].paint_srgb` and `paints`.

| id | trade | bay | original or altered | stallriser | door position | lobby | glazing pattern |
|---|---|---|---|---|---|---|---|
| mickeys | minicab office (Mickey's) | east_parade 0, x 3-9 | altered: A2 painted-steel refit (1970s) | tile_patterned (cream glazed tile) | viewer's RIGHT; recipe doors_on left; side door yes | flush | 3L-3T-aligned: 3 lights, 3 toplights, M1 |
| fish_market | fishmonger (Fish Market) | east_parade 1, x 9-15 | altered: A1 aluminium replacement front (1970s) in an older frame | tile_square (white glazed tile, grout grey) | viewer's RIGHT; recipe doors_on left; side door yes | flush | 4L-4T-aligned: 4 lights, 4 toplights, M1 |
| ritas | pawnbroker (Rita's) | east_parade 2, x 15-21 | original: O original timber front, repainted (the model) | panel (oxblood) | viewer's LEFT; recipe doors_on right; side door yes | flush | 3L-8T: 3 lights, 8 toplights, T1 |
| empty_unit | empty unit to let | east_parade 3, x 21-27 | original: E empty original front, paint gone, glass whitewashed | boarded (bare soot-darkened timber) | viewer's RIGHT; recipe doors_on left; side door yes | flush | 3L-8T: 3 lights, 8 toplights, T2 |
| steam_laundry | launderette (Steam Laundry) | east_parade 4, x 27-33 | altered: A1 aluminium replacement front (1980s) with a plastic box sign | tile_square (white glazed tile, grout grey) | viewer's LEFT; recipe doors_on right; side door yes | recessed 300 | 2L-1T: 2 lights, 1 toplights, M1 |
| grocer | grocer | east_parade 5, x 33-39 | altered: R 1930s refit: bronze bars, glass stallriser, deep recessed lobby | slab (bottle green opaque glass) | viewer's LEFT; recipe doors_on right; side door none | recessed 600 | 3L-5T-sunrise: 3 lights, 5 toplights, M2 |
| chandler | ship's chandler | east_chandler 0, x 40-46 | altered: A1 aluminium replacement front (1970s), plain glazed tile | tile_square (pale green glazed tile) | viewer's LEFT; recipe doors_on right; side door yes | flush | 3L-3T-aligned: 3 lights, 3 toplights, M1 |
| tea_rooms | tea room | west_north 2, x 24-30 | original: O original timber front, repainted, with a flat panel over the fascia | render (mid brown) | viewer's LEFT; recipe doors_on right; side door yes | flush | 3L-6T: 3 lights, 6 toplights, T1 |
| ironmonger | ironmonger | west_north 1, x 30-36 | original: O original timber front, repainted dark green | panel (dark green) | viewer's RIGHT; recipe doors_on left; side door yes | flush | 2L-5T: 2 lights, 5 toplights, T2 |
| newsagent | newsagent and tobacconist | west_north 0, x 36-42 | original: O original timber front with a plastic box sign and a roller-shutter box | panel (dove grey) | viewer's RIGHT; recipe doors_on left; side door yes | flush | 3L-8T: 3 lights, 8 toplights, T1 |

| id | pilaster | console | shop door | alterations | zones (mm) | street x (m) |
|---|---|---|---|---|---|---|
| mickeys | clad | scroll | M1 | steel_refit, repaint | u: window [350.0, 3700.0], shop door [3700.0, 4706.0], side door [4706.0, 5650.0] | window 6.975, side 3.822 |
| fish_market | panel | scroll | M1 | aluminium_refit, repaint | u: window [350.0, 3700.0], shop door [3700.0, 4706.0], side door [4706.0, 5650.0] | window 12.975, side 9.822 |
| ritas | panel | scroll | T1 | repaint | u: window [2300.0, 5650.0], shop door [1294.0, 2300.0], side door [350.0, 1294.0] | window 17.025, side 20.178 |
| empty_unit | panel | scroll (left absent) | T1 | empty_unit | u: window [350.0, 3700.0], shop door [3700.0, 4706.0], side door [4706.0, 5650.0] | window 24.975, side 21.822 |
| steam_laundry | render | scroll | M1 | aluminium_refit, box_sign, recessed_lobby, repaint | u: window [2300.0, 5650.0], shop door [1294.0, 2300.0], side door [350.0, 1294.0] | window 29.025, side 32.178 |
| grocer | render | block | M2 | refit_1930s, recessed_lobby, repaint | u: window [1356.0, 5650.0], shop door [350.0, 1356.0], side door None | window 35.497, side None |
| chandler | panel | scroll | M1 | aluminium_refit, repaint | u: window [2300.0, 5650.0], shop door [1294.0, 2300.0], side door [350.0, 1294.0] | window 42.025, side 45.178 |
| tea_rooms | flute | scroll | T1 | repaint, flat_panel_sign | u: window [2300.0, 5650.0], shop door [1294.0, 2300.0], side door [350.0, 1294.0] | window 27.975, side 24.822 |
| ironmonger | flute | scroll | T1 | repaint | u: window [350.0, 3700.0], shop door [3700.0, 4706.0], side door [4706.0, 5650.0] | window 32.025, side 35.178 |
| newsagent | panel | scroll | T1 | repaint, box_sign, roller_shutter | u: window [350.0, 3700.0], shop door [3700.0, 4706.0], side door [4706.0, 5650.0] | window 38.025, side 41.178 |

| id | piers, consoles, cornice | fascia board | stallriser | window frame | shop door | side door |
|---|---|---|---|---|---|---|
| mickeys | slate blue-grey [62, 75, 87] | slate blue-grey [62, 75, 87] | cream glazed tile [222, 212, 184] | slate powder-coat on steel [60, 74, 88] | slate powder-coat on steel [60, 74, 88] | oxblood [93, 46, 49] |
| fish_market | pale grey-white [196, 202, 206] | pale grey-white [196, 202, 206] | white glazed tile, grout grey [228, 228, 220] | natural anodised aluminium, dulled [176, 178, 180] | natural anodised aluminium, dulled [176, 178, 180] | gloss black, faintly blue [35, 36, 40] |
| ritas | oxblood [93, 46, 49] | oxblood [93, 46, 49] | oxblood [93, 46, 49] | gloss white, yellowed [226, 224, 214] | gloss white, yellowed [226, 224, 214] | buttermilk cream [222, 212, 184] |
| empty_unit | bare soot-darkened timber [46, 37, 30] | bare soot-darkened timber [46, 37, 30] | bare soot-darkened timber [46, 37, 30] | old white, flaked to grey [170, 166, 156] | gloss black, faintly blue [35, 36, 40] | gloss black, faintly blue [35, 36, 40] |
| steam_laundry | cream [222, 209, 175] | cream [222, 209, 175] | white glazed tile, grout grey [228, 228, 220] | bronze anodised aluminium [84, 68, 53] | bronze anodised aluminium [84, 68, 53] | dark brown [74, 48, 34] |
| grocer | cream [222, 209, 175] | bottle green opaque glass [36, 61, 49] | bottle green opaque glass [36, 61, 49] | bronze-plated bar, tarnished [110, 86, 50] | bronze-plated bar, tarnished [110, 86, 50] | none |
| chandler | navy [44, 53, 83] | navy [44, 53, 83] | pale green glazed tile [170, 190, 172] | natural anodised aluminium, dulled [176, 178, 180] | natural anodised aluminium, dulled [176, 178, 180] | navy [44, 53, 83] |
| tea_rooms | mid brown [120, 74, 44] | cream [222, 209, 175] | mid brown [120, 74, 44] | buttermilk cream [222, 212, 184] | buttermilk cream [222, 212, 184] | dark brown [74, 48, 34] |
| ironmonger | dark green [30, 62, 44] | buff [188, 173, 136] | dark green [30, 62, 44] | dark green [30, 62, 44] | dark green [30, 62, 44] | gloss black, faintly blue [35, 36, 40] |
| newsagent | dove grey [150, 152, 150] | dove grey [150, 152, 150] | dove grey [150, 152, 150] | gloss white, yellowed [226, 224, 214] | dove grey [150, 152, 150] | dark blue [24, 38, 78] |

**Why these.** The trades and bays are Jafar's (3 October). Rita's is the model he called the best thing on the page. The refits follow the street's recipe where it has one (Mickey's slate steel front on patterned tile; the fish shop's, the chandler's metal fronts with plain glazed tile) and the fascia target where it fixes a date (the grocer's glass board means a 1930s refit; the laundry's and newsagent's box signs mean 1980s additions; the tea room's flat panel a 1980s caff). The empty unit is the one front nobody repainted. Four of ten are original timber repainted (Rita's, tea, ironmonger, newsagent) and the empty unit is original and derelict; five are altered. Departures from the recipe or the fascia target are in section 16.

**Paints.** Every colour is an aged 1990 sRGB value with a plain name; the source or kind is in `paints.<id>.note`. Rita's oxblood (93, 46, 49) is the fascia target's aged oxblood; the whole palette is in the JSON (31 entries).

## 14. Photographs win: each disagreement and what was chosen

| id | element | book or scene | photograph | chosen |
|---|---|---|---|---|
| D1 | plinth height | kit and scene: the plinth equals the stallriser, 600 | P1: plinth top 0.228 of the front's height, 1.27 times the sill's top | 800 (the photograph scaled to 3.55 m is 811) |
| D2 | shop door glazed from | scene C8: 1.0 m | P1: 0.328 of the leaf (0.67 m on a 2.04 leaf); books 0.6 to 0.7 m | 700 (photograph and books agree, the scene loses) |
| D3 | shaft projection | scene: 100 | P1: 118 +-14 | 110 (inside both) |
| D4 | capital height | kit: 330 | P1: 301 +-24 | 310 |
| D5 | mullion width | kit 55; Cornwall guide: projecting 40-70 from the glass (a projection, not a width) | P1: 164 mm face against a 1.0 m light | 70 (T1), 80 (T2): the photograph is a heavy plate-glass arcade front; not followed in full. If the reviewer reads the photograph as authoritative, 100 to 120 is the next step |
| D6 | fascia face | Coventry 2014 (the earlier reading): sloped slightly forward | P1: vertical | vertical |
| D7 | cornice height | fascia-01: 150; Ellis (the earlier reading, in the London rules of about 1902): a cornice may PROJECT 13 in (330) in a street up to 30 ft wide and 18 in in a wider one (a limit on projection, not height; ours projects 215) | P1: the crown (fillet to cap, measured at the continuous run) is 446 mm, 0.86 of the 505 mm fascia field; the street's 150 over 550 is 0.27 | 150 kept (the fixed envelope); variant 'tall' 300 offered. The photograph is NOT followed here and this is stated |
| D8 | sill thickness | kit: 50 | P1: the sill group 140 deep with a bead, cove and soffit; Ellis: stout sill | 75 |
| D9 | stallriser height | scene 600; guides 400 to 700 | P1: sill top 0.18 of the front's height, 0.64 m at 3.55 | 600 (no disagreement) |
| D10 | the pilasters in pairs at the party wall | scene: a pier at every bay edge (two 0.35 piers butt) | P1 has single piers between shops | pairs kept: the scene is a fixed fact of the street and a parade of separately owned shops did have a pilaster each; they butt with a painted vertical joint |
| D11 | the scrolled console | the brief and the earlier reading: consoles are scrolled brackets | P1's pier caps are straight stepped blocks, not scrolls: the photograph does not show the part | scroll by Judgement; stated as not established by a photograph |

**Ratio rules** (target.json `derived_rules`; self-check group 2 recomputes each):

| rule | photograph | target | within | reading |
|---|---|---|---|---|
| R1 plinth top over sill top | 1.271 | 1.333 | yes | P1's plinth stands about 1.3 times higher than its sill; the street's 800 / 600 is 1.33 |
| R2 plinth top over the front's height | 0.228 | 0.225 | yes | 0.228 against 0.225 |
| R3 sill top over the front's height | 0.18 | 0.169 | yes | no disagreement with the scene's 600 |
| R4 capital height over shaft width | 1.037 | 1.069 | yes | 310 / 290 |
| R5 shaft proud over shaft width | 0.405 | 0.379 | yes | 110 / 290 |
| R6 shop door glazed from, over the leaf | 0.328 | 0.343 | yes | 700 / 2040; the scene's 1000 / 2040 = 0.49 is far outside |
| R8 crown height over the fascia field | 0.859 | 0.273 | NO (not followed) | P1's crown is 0.86 of its field; the street's cornice is 0.27 of its fascia: NOT followed (D7) |
| R7 shaft width, absolute | 290.1 | 290.0 | yes | scale error 8 per cent |

## 15. Checks, previews, drawing, self-check

**Checks for unit 3.2** (`checks`, 81 of them; each has a name, what to measure, the expected value and a tolerance): the pilaster (slot, plinth top, proud, shaft width, neck, capital top and size, panel and flute numbers, the pair's gap and the downpipe chase, profile fit), the console (envelope, centre, foot on the capital, top at the cornice's soffit, silhouette, leaf, volute), the fascia and cornice (size, foot on the abacus, bed mould, oversail, soffit gap, profile, stops), the sill, stallriser, window frame (transom, head, mullion section and positions, glass plane, length per shop), the shop door (leaf, glazed from 700, slot, foot strip, furniture), the side-door slot (944, F1's head meeting the transom, frame face d 100, the threshold's nose d 130), the zones filling 5300, the alterations, and per shop the door end, zones and street x of the window and the side door (the fascia target's own numbers). Materials: at most three plain PBR materials per piece, no textures, paint a per-shop parameter. No lettering, no maker's mark.

**Previews** (`production/previews/cloud-week/refs/shopfronts/`, JPEG, at most 1200 px, under 300 KB; for the reviewers; the photograph is Andreas Mischok's Leadenhall Market HDRI, CC0, taken 2019-05-19, polyhaven.com; the crops show joinery only; the two sets of house numerals and a fragment of a shop-window logo are masked; no business is named; the drawings are the studio's own):

| file | what |
|---|---|
| `P1-leadenhall-pilaster-plinth.jpg` | the plinth's four stepped members and the foot (350 x 700 px at the virtual 2400 px focal length; a logo fragment masked top left) |
| `P1-leadenhall-pilaster-capital.jpg` | shaft top, necking ledge, die with three roundels, flared cap, top band |
| `P1-leadenhall-pier-fascia-cornice.jpg` | the pier head under the fascia and the crown (numerals masked) |
| `P1-leadenhall-cornice-run.jpg` | the continuous crown to the right of the pier |
| `P1-leadenhall-sill-stallriser-stile.jpg` | sill group, framed stallriser panel, foot rail, stile |
| `P1-leadenhall-transom-mullion.jpg` | the mid transom bar and the central mullion |
| `P1-leadenhall-*-target-on-photo.jpg` | the drawing (cyan) laid on each crop: bands built from the measured rows and columns, at the scale fitted on one dimension |
| `D1-ritas-bay-elevation.jpg` | the target's elevation of Rita's whole bay (drawn at 1 mm to the pixel, reduced), with the neighbours' pair of pilasters and consoles in grey and the downpipe between |
| `D2-ten-fronts-sheet.jpg` | the ten fronts assembled from the table |
| `D3-parts-pilaster-console-fascia.jpg` | four pilaster variants, the console's silhouette and front, the capital / console / fascia / cornice section |
| `D4-parts-sections.jpg` | eighteen sections at x0.3 to x3 |

**Credits.** P1: Andreas Mischok, Leadenhall Market, CC0 (Poly Haven), taken 2019-05-19. P2 (numbers only; no picture kept): Poly Haven rollershutter models, author MP, CC0, published 2023-10-11. The drawings are LEDGER's own.

**Self-check (2026-10-09):** **427 of 439 checks pass; 0 fail; 12 departures reported and kept in the open.** Groups: 1 printed 88 pass 0 fail 5 reported; 2 photo 65 pass 0 fail 3 reported; 3 wins 11 pass 0 fail 4 reported; 4 overlay 37 pass 0 fail 0 reported; 5 consistency 218 pass 0 fail 0 reported; 6 faults 8 pass 0 fail 0 reported.

The groups: 1 printed (the numbers read again from SCENE-SLOTS.md, fascia-01's recipe, the kit README, the fascia target and the front-door target); 2 photo (every row and column re-measured on the saved previews; the scale and the ratio rules recomputed); 3 wins (each disagreement recomputed); 4 overlay (the drawing's edges on the previews, worst 0.03 px of 34 edges); 5 consistency (profiles are simple counter-clockwise polygons; the parts add up; the ten fronts' zones; nothing overlaps that should not and nothing floats in any of the ten drawings; paints, shops, alterations and checks well formed; the content rule); 6 faults (eight deliberately broken copies, each noticed).

The reported lines are not failures but departures kept visible:

- 1 printed: shaft proud 110 differs from the scene's 0.10 (disagreement D3 lists it) (photographs win)
- 1 printed: glazed from 700 differs from the scene's 1.0 (D2 lists it) (the photograph and the books agree against the scene)
- 1 printed: kit: mullions 48 in front of the glass (target 62: changed, listed as D5) (the target moves it to 62)
- 1 printed: grocer: no side door here, a side-door fanlight (x 38.18) in the fascia target (reported: the recipe's BAY_WITHOUT_SIDE_DOOR = 5 and terrace-fronts.md give the grocer none; the number belongs on the shop door fanlight, street x 38.147)
- 1 printed: grocer: window centre differs from the fascia target's 35.025 (no side door widens the window) (reported: mine 35.497)
- 2 photo: not re-measurable on a preview (the glass carries lettering): door_foot, door_foot_strip_top, door_glass_bottom, door_glass_top, door_leaf_top, _sign (read on the unmasked view only)
- 2 photo: scale: no cross-check by a second dimension (the door leaf's own 2.62 m is a result) (the A5 assumption and the plane ratio carry +-8 per cent and are not independently confirmed)
- 2 photo: ratio rule R8 crown height over the fascia field: photo 0.859, target 0.273 (NOT followed, stated as D7) (P1's crown is 0.86 of its field; the street's cornice is 0.27 of its fascia: NOT followed (D7))
- 3 wins: D5 mullion 70 is not the photograph's 164 (partly followed, stated) (the photograph reads 164; the target takes 70 (T1) and 80 (T2))
- 3 wins: D7 the cornice stays 150: the photograph's crown is not followed (stated) (the fixed envelope; a tall variant is offered)
- 3 wins: D10 the pairs at the party wall stay (the scene's fact) (P1 has single piers)
- 3 wins: D11 the scrolled console is Judgement, not photographed (no photograph of one was reached)

## 16. What the target could not settle

1. No photograph of a provincial 1900-1935 shopfront was reached (Wikimedia, Geograph, Flickr, archive.org and the council guides all refused). P1 is a London arcade (c.1881, from memory) restored in 2019: it governs proportions and the order of mouldings; it does not govern timber panel layouts, fluting, console scrolls or leaves, aluminium sections, roller-shutter boxes, box signs, lobbies or whitewashed empty units. Those rest on the earlier notes (cited, not re-read) and Judgement, each marked
2. The scrolled console and its leaf (the volute, the acanthus): no photograph at all. The silhouette keeps the street's built envelope; the volute and leaf are Judgement
3. The 1960s-80s aluminium front's sections (50 x 75, cover caps, mastic joints): Judgement; R05 and R09 only say such fronts existed
4. Absolute scale of P1: the A5 notice is assumed to be A5 (148 x 210); its plane ratio to the pilasters (1.104) assumes the door foot and the plinth foot are at the same footway level. The scale is +-8 per cent and every Leadenhall millimetre carries it. Ratios do not
5. Mickey's door: mickeys-office.json puts it at street x 4.65 (the rank spot, the unlock distance); the kit's slots put the shop door's centre at x 4.797, 147 mm farther from the party wall, because the side door slot is 944 and the shop door slot 1006. Rita's front already stands so. A town question (move the door x or narrow the side door's slot)
6. The fascia target puts a street number on every side door's fanlight (the grocer's at x 38.18); the street recipe and terrace-fronts.md give the grocer no side door (BAY_WITHOUT_SIDE_DOOR = 5). This target follows the recipe; the number belongs on the shop door's fanlight (x 38.147). A fascias question
7. The ironmonger: the street recipe makes it a metal refit (SHOPFRONT_REFITS west_north 1); this target keeps it timber to suit its traditional board. A town or art question
8. Twelve fronts or ten: RULINGS 2 Oct counts twelve; the scene has ten shop bays (six east, the chandler, three west). Ten are tabled. A coin shop at x 39 (hook-cast) is not in the scene
9. The Hook sheet shows a recessed Mickey's door and an angled display bay at the corner; the street's Mickey's is a flat front with its door and room walked in the game. This target keeps it flush (as built) and gives the recess to the grocer and the launderette
10. The party-wall downpipe: the 6 October note says it goes 'inside the hollow pilaster'; at the roofline's 94 mm offset it cannot (the shaft is 110 proud and the pipe's front stands at 128). This target leaves the pipe where the roofline has it, in the 60 mm gap between the two shafts and a 76 mm chase through the plinths and capitals; the roofline owner may prefer to move the pipe back
11. Texture size, UVs, material slots and vertex-colour masks are the builder's (the kit's method stands); nothing here changes them
12. Nobody has looked at these parts at the game's exposure and internal resolution; what is visible at 8 m is not judged

Also: the fascia target's boards and glass lettering, the front-door family's F1 door, the wear target's layer and the shop-room's displays are not re-done here; where this target touches them (the board's plane and bed mould, the F1's mapping, the splash band on tiled and slab stallrisers, the sill's display bed) it says how.
