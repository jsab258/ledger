Shop windows: ten units as built (twelve not found); eight rooms of 104 checked CC0 models and 51 named scripted forms, rendered 4096 wide to the game's own `trace` rule, stock only where that rule can show it and the near 0.55 m a real display; the fish scans wait on one login.

# Shop windows of Quay Street: the exact target

Cloud week 42, part 2, unit 7 (12 October 2026). Written by the target writer from sources reached that day; nothing is built and nothing is committed. Every number below is in `target.json`; the checks that follow from it are its `checks` list and its `self_check` (self_check: 269 pass, 0 fail, 3 reported; 13 of 13 negative controls caught).

## 0. Files, and how to read them

| file | what it is |
|---|---|
| TARGET.md | this page (made by make_doc.py from target.json) |
| target.json | the ten shops (front, door, glass, fascia, room, display, lights, pictures, cameras), the method's numbers, the inventory, the spec entries, the checks, the self-check |
| target_drawing.py | draws target.json alone: each bay's elevation, each room's plan, back wall and picture layout, the ten fronts' sheet, and the elevation laid on the main photograph |
| self_check.py, controls.py | tests the target against its sources (272 rows) and shows the self-check can fail (13 mutations) |
| sw_common.py, sw_shops.py, make_target.py, extras.py, make_doc.py, make_previews.py | author tools: the game's rule and the stand-off budgets; the rooms and displays as data; the builders of target.json, TARGET.md and the previews |
| polyhaven_checked.json, sketchfab_checked.json, ambientcg_checked.json | what the three libraries' APIs answered on 12 October |
| production/previews/cloud-week/refs/shop-windows/ | P1 to P6 (the photographs, cropped to the craft), the overlay, D1 to D4 (drawings) |

Run with `/home/user/.bpyenv/bin/python`: `make_target.py [--refresh]`, `self_check.py [--live]`, `controls.py`, `target_drawing.py OUT_DIR`, `make_previews.py`, `make_doc.py`.

**Units and frames.** Metres for rooms and the street; millimetres for the front, in the 2.2 bay frame (u across the bay from the viewer's LEFT, d out from the wall face toward the street, z up from the footway). Street z is above the road crown (crown + 0.10 = footway). **Kinds of number:** Read (printed in a file), Scaled, Photo (measured on a photograph: method and error given), Derived, Judgement.

## 1. The ten units as found: twelve not found

The street has **ten shop units as built; twelve not found.** east_parade bays 0 to 5 (x 3 to 39, 6 m each), east_chandler bay 0 (x 40 to 46), west_north bays 0 to 2 counted from the high-x end (x 36 to 42, 30 to 36, 24 to 30). canon.md and TOWN.md name no shop count; DECISIONS 3 Oct lists ten; 'twelve' is the superseded atlas proposal (terrace-fronts.md 290 to 322) and 'the other eleven' in RULINGS 2 Oct. One conflict is NOT resolved: hook-cast.json places 'Hals_shop' (keeper hal, hours 10 to 18, Wed 10 to 13) at street x 39, which is inside the newsagent's bay (x 36 to 42): either the coin shop is the newsagent's neighbour (there is none) or one of them is not on the street. Not resolved: the newsagent is built as ruled (3 Oct).

| id | no. | trade | owner | block, bay, side | street x | room picture | at night | spec id |
|---|---|---|---|---|---|---|---|---|
| mickeys | 1 | minicab office (Mickey's) | Mickey (Michael Suddaby, dead); Tom Nowak inherits; Ron Kirby and Sheila Dunn keep it (canon.md) | east_parade bay 0 (east) | 3 to 9 | no: its room is real and walked already | lit after Tom's key | mickeys |
| fish_market | 3 | fishmonger (Fish Market) | none named | east_parade bay 1 (east) | 9 to 15 | yes (4096 x 1855) | dark | fishmonger |
| ritas | 5 | pawnbroker (Rita's) | Rita (hook-cast.json: keeper 'rita'; no surname in canon) | east_parade bay 2 (east) | 15 to 21 | yes (4096 x 1855) | lit | pawnbroker |
| empty_unit | 7 | empty unit to let | none named | east_parade bay 3 (east) | 21 to 27 | no: whitewashed, no card | dark | - |
| steam_laundry | 9 | launderette (Steam Laundry) | none named | east_parade bay 4 (east) | 27 to 33 | yes (4096 x 1855) | dark | launderette |
| grocer | 11 | grocer | none named | east_parade bay 5 (east) | 33 to 39 | yes (4096 x 1855) | lit | grocer |
| chandler | 13 | ship's chandler | none named | east_chandler bay 0 (east) | 40 to 46 | yes (4096 x 1855) | lit | chandler |
| tea_rooms | 14 | tea room | none named | west_north bay 2 (west) | 24 to 30 | yes (4096 x 1855) | lit | tea_room |
| ironmonger | 16 | ironmonger | none named | west_north bay 1 (west) | 30 to 36 | yes (4096 x 1855) | dark | ironmonger |
| newsagent | 18 | newsagent and tobacconist | no keeper named; hook-cast.json puts Hal's shop (the coin shop, keeper 'hal', 10 to 18) at x 39, INSIDE this bay (x 36 to 42): a conflict, not resolved here | west_north bay 0 (west) | 36 to 42 | yes (4096 x 1855) | lit | newsagent |

**Hours and lit windows.** Hours are hook-cast.json's `areas` where they exist (Mickey's 7 to 3 am, Sundays from 9; Rita's 9 to 17:30, Wednesday to 13:00; fish market 7:30 to 14:00; laundry 8 to 17:30; cafe 6:30 to 22:00, Sundays 8 to 12; newsagent 6 to 17:30, Sundays 7 to 12). Not found: the grocer, ironmonger and chandler; settled as a Judgement from the Shops Act (Mon to Sat, 8 to 17:30 or 17:00, early closing Wednesday 13:00), marked in each shop's `hours_source`. Lit at night is vignette-pieces.json's `lit_names` (Mickey's after Tom's key, Rita's, the grocer, the newsagent, the tea room, the chandler); the street file lights three shops that the hours say are shut by then (the newsagent at 17:30, the grocer and the chandler by the Judgement; D8): kept as the street file has it, noted for the town.

**What unit 7 does for Mickey's:** only its front. The room is the real walked room (spec entry untouched, `room_3d`, its lamps and brightness): the front is the A2 painted-steel refit assembled from the 3.2 parts (clad pilasters, M1 window 3L-3T with 2 mullions, patterned-tile stallriser), the 4.1 board with its raised gilt letters (geometry), the glass rows `0632 960418` and `MINICABS . 24 HOURS`.

## 2. Sources

Only sources reached on 12 October are used. Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model; each preview is cropped to the craft, with every person, real firm's name, number and drink merchant's sign cropped away or masked grey. No NoAI source.

| id | what | URL | read | author | licence | taken | shows | used |
|---|---|---|---|---|---|---|---|---|
| P1 | Iddles fishmonger's front, Worcester (Geograph, 'Iddles fishmongers - 2'): an old shop front left as it was: divided timber lights, a black-tiled stallriser, a half-glazed timber door, the slab visible through the glass | https://www.geograph.org.uk/photo/2192169 | 2026-10-12 | Helen Iwanczuk | CC BY-SA 2.0 | May 2000 (the page: 'taken May 2000') | the front a fish shop kept for decades (the author: the premises 'remained in this condition'): door leaf 335 px high by 140 wide (0.42), glass foot 0.413 of the leaf, two panes divided by a bar at 0.685, a letter plate at 0.32, stallriser tiled to 0.28 of the leaf, the window slab and the room dark behind reflections [a period object: a later photograph of a front unchanged since before 1990 (the page says so); 2000 is the earliest dated photograph of a fish-shop window reached] | measured (photo_measurements.json), cropped below the fascia for the preview, the main photograph of the self-check's overlay |
| P2 | Holyoake's grocer's shop, Bath Road (Geograph, March 1999): an open-fronted stock window, tiered stands, goods stacked to the glass, the shop's back shelves visible | https://www.geograph.org.uk/photo/2184467 | 2026-10-12 | Helen Iwanczuk | CC BY-SA 2.0 | March 1999 | density of a grocer's window and the depth of its stock (tins, jars, crates on tiered timber stands); a person stands at the door (masked in the preview) [a long-established shop (the page: established 1898); 1999 shows a 1990 window] | yes: the tiered stand and the density in the grocer's display; preview cropped to the left window and stand (the shop door, with a person at it, and the right-hand shelves are outside the crop) |
| P3 | Shops in Cannon Lane, Pinner (Geograph): a hardware store's and a newsagent's windows, one lit and readable, one dark | https://www.geograph.org.uk/photo/5945841 (and 3403654, the same parade) | 2026-10-12 | Carl Grove | CC BY-SA 2.0 | 20 February 1989 | a 1989 high-street parade: the hardware window's dark interior with stock to the ceiling behind reflections; the newsagent's lit interior with racks; deep recessed doors; cars of 1989 [a photograph of the period itself] | yes: the black-void question (the glass is mostly reflection by day, the room dim; a lit shop reads); preview cropped to the two windows below their fascias (the parade's other signs, a drink merchant's, are outside the crop) |
| P4 | A ship chandler's shut shopfront, High Street, Hull (Geograph): green timber front, lower lights screened inside with woven galvanised mesh | https://www.geograph.org.uk/photo/3378991 | 2026-10-12 | Bernard Sharp | CC BY-SA 2.0 | 1 January 1983 (the feed's date; the page says taken before redevelopment) | the chandler's front: three tall lights, mullions in green, mesh screens over the lower lights, a plaque on the door post [a photograph of the period itself] | yes: the night mesh screens (chandler), the green; preview cropped below the fascia with the glass lettering and the plaque masked (a real firm's name) |
| P5 | Launderette in Hambledon Parade (Geograph): a 1960s-80s aluminium-framed launderette front with a script fascia and a striped blind, the room dark behind the glass | https://www.geograph.org.uk/photo/1633924 | 2026-10-12 | Basher Eyre | CC BY-SA 2.0 | 26 December 2009 | the type of front (full-height glazing, glazed door, machines faintly seen); LATER than 1995: used only for the type and for what a launderette window does by day [a later photograph; the front's pattern is the 1970s-80s one (not dated by the author)] | as a type reference only; preview cropped to the front |
| P6 | A derelict grocer and draper's shop, Kames (Geograph): glass dark or blank, paint gone, a pillar box at the kerb | https://www.geograph.org.uk/photo/27024 | 2026-10-12 | Andrew Longton | CC BY-SA 2.0 | 24 May 1995 | an unlet shop in 1995: the glass reads grey-blue and blank, not black; no whitewash [a photograph of the period itself] | for the empty unit's glass: it must read as a pale blank, not a black hole; preview cropped |
| H1 | Poly Haven catalogue (api.polyhaven.com/assets?t=models, and /files/<id> for each of the 104 models used): 521 models, 868 textures; each model's name, size, triangles, date, authors and glTF file read; thumbnails (cdn.polyhaven.com) looked at on three contact sheets | https://api.polyhaven.com/assets?t=models | 2026-10-12 | Poly Haven contributors | CC0 | n/a | every id in the inventory exists with a 1k glTF  | yes (inventory.polyhaven) |
| H2 | ambientCG API (ambientcg.com/api/v2/full_json): ids checked to exist as CC0 materials | https://ambientcg.com/api/v2/full_json | 2026-10-12 | ambientCG | CC0 | n/a | Tiles032, Tiles040, Ice001, Ice002, Marble012, Rope001, Rope002, Candy001, Candy002, Fabric020, Fabric021, Fabric028, Fabric029, Cardboard002, Wicker010B, Terrazzo004 and the imperfection sets exist (a search call reset twice and is not relied on)  | yes (inventory.ambientcg_checked) |
| H3 | Sketchfab API v3 (anonymous): the ffishAsia / floraZia CC0 scans (cod, mackerel x2, herring, flounder x2, crab, prawn x2, apple, cabbage, potato, satsuma, pear, lemon): name, licence 'CC0 Public Domain', faces, publish date, downloadable true; the download endpoint answers 401 without a login | https://api.sketchfab.com/v3/models/<uid> | 2026-10-12 | ffish.asia / floraZia.com | CC0 Public Domain | scans published 2021 to 2026 | the goods that no Poly Haven model gives are real scans, on the allowlist ('Sketchfab CC0 filter'), and need only Jafar's login  | yes (inventory.sketchfab_checked); not downloaded |
| H4 | Smithsonian Open Access 3D API (3d-api.si.edu/api/v1.0/content/file/search): answers from the cloud; queries for mackerel, flounder, haddock, plaice, lobster, Gadus, Clupea and Scomber return nothing; 'cod' and 'herring' return only unrelated objects (a horseshoe crab, a flight suit); 'crab' returns a king crab (Lithodidae), 'shrimp' a mantis shrimp | https://3d-api.si.edu/ | 2026-10-12 | Smithsonian | CC0 (per item; not on the allowlist by name) | n/a | no British fish are there  | no: nothing fits and it is not named on the allowlist |
| G1 | Wikimedia Commons (API, one request at a time; many 429s): category listings for launderettes, fishmongers, ship chandlers, tea rooms, pawnbrokers; the 1968 'Twthill laundrette, Caernarfon' (CC BY-SA 4.0, Geoff Charles) was seen and has children in the frame | https://commons.wikimedia.org/ | 2026-10-12 | various | various | see text | no photograph from 1975 to 1995 of a pawnbroker's or a launderette's window or room was reached; the Caernarfon launderette (1968) is NOT used (children)  | no |
| R | Project files read: canon.md, TOWN.md, RULINGS.md, DECISIONS.md 236 and 243, production/specs/shop-interiors.json, vignette-scene.json, vignette-pieces.json, hook-cast.json, tools/ue/make_interior_material.py, tools/art-recipes/shop-room.py, fetch_polyhaven.py, make_label_atlas.py, terrace-front.py 2385-2417, production/research/shop-window-interiors/*, shop-hours-1990, targets/shopfronts (2.2), targets/fascia-signs (4.1), kit/shopfront/NOTES.md, 2d/fascias/NOTES.md, HANDOVER.md, commit 2f475f5 and NOW.md as of it | - | 2026-10-12 | studio | own | - | the game's format, the three failures of 3 October, the ten units, the lit list, the hours  | yes |

**Not reached (nothing rests on them):**

- Peter Marshall's Hull and 1990 London photographs (Flickr): named in NOTE.md as links only; not requested in this unit, so no number rests on them.
- Picture Sheffield t13140 and t13138 (the fishmonger of 1989 and 1990): read by the builder on 3 October (FISHMONGER-2026-10-03.md), not re-read today; used only as that note reports them.
- Any photograph from 1975 to 1995 of a pawnbroker's window or room, a launderette's window or room, or a ship chandler's interior: none was reached (Geograph's category 'Pawnbroker' starts in 2006 and 'Launderette' in 2005; Commons returned US, Irish and foreign shops and a 1968 launderette with children).
- Historic England and the Black Country Living Museum's pawnbroker (a 1930s reconstruction): not used.
- A Sketchfab download of any scan: needs Jafar's login (401 without).

## 3. The method, in the game's own numbers

**The game's rule** (production/specs/shop-interiors.json, tools/ue/make_interior_material.py `trace`, kept exactly): on the room's centre line, d in front of the front plane, framing the front rectangle W x H exactly (horizontal field 2 atan(W / 2d)); a room point (x, y, z), z behind the front plane, lands at u = 0.5 + (x / W) d / (d + z), v = 0.5 + (y / H) d / (d + z). The card is 5.3 x 2.4 m at street z 0.65 to 3.05, 5.875 behind the street's midline on its side (y +5.875), 0.61 m behind the glass (glass y 5.245 to 5.265). The picture's left is the viewer's left (an east card: the card's HIGH x; a west card: its LOW x).

**Where the floor line and the back wall land.** The box is W x H x D = 5.3 x 2.4 x D with its floor at the card's bottom edge (0.65 above the crown) and its ceiling at the card's top (3.05): the picture's floor is the window bed carried back, 0.55 above the shop's real floor, which the stallriser hides from the street. For D = 4.5 the back wall is the rectangle u 0.2296 to 0.7704, v 0.2296 to 0.7704 of the picture, in the 4096 x 1855 picture from (940, 426) to (3156, 1429) (check PIC-04, +-8 px). The side walls and floor are the wedges outside it; nothing else is in the picture.

**What a projected room can honestly hold (the answer to the third failure).** An object painted on a surface that stands off it by s metres is drawn where the render camera saw it and slides, as the eye moves, by the angle between the eye's rays to the object and to its painted place. `sw_common.standoff_table` computes, from `trace`'s geometry, the greatest stand-off whose slide stays within N pixels of a 2560 x 1440 frame at STREET_SQUARE, STREET_30 and CLOSE_35 (and their mirror images). Results (D = 4.5):

| surface | reads true (20 px) | tolerated (40 px) | the target's rule |
|---|---|---|---|
| back wall | 0.33 m | 0.64 m | shelf units and goods on them: 0.30 (true); a counter, machine or floor piece against the wall: up to 0.60 (tolerated) |
| side walls | 0.06 m | 0.11 m | boards, posters, pegboards, hung things: 0.05 flat; racks and boards with hung tools: up to 0.10 |
| floor and ceiling | 0.029 m | 0.059 m | flat things only: 0.025 (a mat, a drain, a tile pattern); a ceiling batten fitting 0.045 is tolerated (0.05) |

Anything that would need to stand further off a surface (a counter across the room, a table, a chair, a free-standing unit, a buoy at the side) is NOT drawn in the picture: it stands in the display, which is real geometry, or it is dropped. The slide of the standard objects at the three cameras (px of 2560 x 1440):

| object | STREET_SQUARE | STREET_30 | CLOSE_35 |
|---|---|---|---|
| shelf goods 0.25 off the back wall (middle) | 3 | 14 | 15 |
| counter 0.60 against the back wall (middle) | 7 | 35 | 38 |
| a free item 1.5 off the back wall | 19 | 92 | 110 |
| a unit 0.30 off the right wall, mid depth | 31 | 94 | 60 |
| a board 0.05 off the right wall | 5 | 15 | 9 |
| a floor item 0.03 high, mid | 4 | 14 | 22 |

**From how near the projected room holds, and why the CLOSE view stands at 1.5 m.** the method holds from the far pavement (8.75 m) and from the near pavement down to 1.5 m from the glass at 35 degrees, with 4096-wide pictures and the stand-off rules: there the room's surfaces are sharp (median 0.50 screen pixel a texel at 4096), back-wall stock 0.25 deep slides 3 to 15 px, a 0.05 board 5 to 15 px, a floor item 0.03 high 4 to 22 px (so the floor's rule is 0.025), and the whole window is seen at under 62 degrees. Nearer than 1.5 m the window's far end passes 62 degrees (67 at 1.0 m, 76 at 0.5 m), where the glass's own Fresnel takes over, so part of every nearer view is the glass's and the display's, not the room's. The near 0.55 m is therefore real geometry, and the review's CLOSE view stands at 1.5 m.

Resolution, at the game's 1440 lines, 35 degrees off (screen pixels a texel; above 2 is soft): 2048 px wide, 0.5 m: median 1.33, p95 2.34, 13% soft; 2048 px wide, 1.0 m: median 1.15, p95 2.18, 8% soft; 2048 px wide, 1.5 m: median 1.00, p95 1.95, 4% soft; 2048 px wide, 1.9 m: median 0.93, p95 1.80, 2% soft; 4096 px wide, 0.5 m: median 0.67, p95 1.17, 0% soft; 4096 px wide, 1.0 m: median 0.57, p95 1.09, 0% soft; 4096 px wide, 1.5 m: median 0.50, p95 0.98, 0% soft; 4096 px wide, 1.9 m: median 0.46, p95 0.90, 0% soft. at 4096 wide the picture is never softer than 1.2 screen pixels a texel from 0.5 m; at 2048 it is soft over 13 per cent of the glass at 0.5 m and 4 per cent at 1.5 m: the picture is made 4096 wide.

The window's far end is seen at (degrees off the glass normal, from 35 degrees off the window centre): 0.5 m: 76, 1.0 m: 67, 1.5 m: 61, 1.9 m: 58. the angle off the glass normal at which the window's far end is seen from a pavement point 35 degrees off the window centre: at 1.5 m it is 61 degrees, where the research puts the glass's own Fresnel hand-over (about 60); nearer than 1.5 m part of the window is in the hand-over and the review would judge the glass, which is the game's, not the room.

**The pictures.** 4096 x 1855 px, 8-bit sRGB PNG, three states (day, night_lit, night_dark), named `<spec_id>_<state>.png` with `<spec_id>.json` beside them holding `shop, w, h, d, camera_d, pixels, states, made_by, samples` (the pawnbroker's own file's fields); Cycles, 128 samples, denoised; masters on F:/LedgerTools/shop-rooms, 2048-wide copies in production/art/shop-rooms as for the pawnbroker. The game's brightness values are kept for every shop: **day 0.15, night 0.7**. The mean luma of each approved pawnbroker picture (measured 12 October) is the standard: **day 119.5, night_lit 79.8, night_dark 17.7**; a new picture's mean is within 15 per cent of the state's, and the checks' floors (PIC-02, PIC-03) are 0.7 of them. Composite floors (the picture times the brightness, tone-mapped Standard, glass reflection off): day >= 33, night_lit >= 45, night_dark 10 to 35 (of 255).

**Lights per state, for every room** (each shop's own tubes are in its `room.lights`): day = an overcast area light the size of the card on its plane (6500 K, strength set so the picture's mean matches the standard) plus the battens on (the shop is open); night_lit = the battens only, cool white 4000 K, 5 ft T12, 38 mm (about 12 kcd/m2 on the tube: DRESSING note), no sky; night_dark = a faint sodium wash through the front (linear (1.0, 0.7055, 0.0), 6 per cent of night_lit's energy) and one small practical so the room is not black. Windows are not lit by a second picture's worth of tungsten: the pawnbroker's display spots (2700 K) are the display's, not the picture's.

**The review cameras** (street frame, metres; eye 1.70 above the crown = 1.60 above the footway; 2560 x 1440). STREET_SQUARE: on the far pavement's kerb edge (the brief's 'about 8 m' is 8.76 m to the glass, the nearest the far pavement allows), square to the window's centre, vertical field 39 degrees. STREET_30: the same distance, 30 degrees off the normal toward the quay end (low street x), 39 degrees. CLOSE_35: on the shop's own pavement 1.5 m from the glass, 35 degrees off the normal toward the quay end, aimed at the display's middle (z 1.45), vertical field 60 degrees (the vignette camera's). CLOSE_35_B: CLOSE_35 moved 2.0 m along the street, for the parallax test. By day and by night (night_lit for the lit shops, night_dark for the dark). Every shop's eye and aim are in `shops[].cameras`.

**The gate in the cloud, which has no Unreal.** The builder shows what the game will show without Unreal: the shop's front is assembled in Blender from the 3.2 parts (and the door and lobby of this target), the display's real meshes stand in front of the card where the display is, and the card is a flat quad with an emission picture computed PER CAMERA by tools/ue/make_interior_material.py's `trace` (the Python function, imported, not rewritten): for every pixel of the card the card point and the eye go through `trace` and the picture is sampled at the returned (u, v), bilinear with mips, times the state's brightness (day 0.15, night 0.7). That picture is baked to an image for the camera and set as the card's emission in Cycles, so what is judged is the game's rule pixel for pixel; the glass is the game's job and is left out (a clear 6 mm pane with no reflection) or drawn at the game's day value only if the review asks. What it cannot show: the game's glass reflections, Lumen's light on the display, the card's motion vectors under TSR, the exposure: those stay owed on the PC.

## 4. Rita's shop in full (the pawnbroker; east_parade bay 2, x 15 to 21; the model, RULINGS 2 Oct)

**What it keeps and what it changes.** Keeps: the room's box and finishes (old brown lino, cream plaster over a 1.0 m brown dado, three T12 battens), the stocked back wall, the ticketed goods, the notices, the three approved pictures' look, the display glb and its 23 Poly Haven models. Changes: the glass counter 2.4 m out in the room goes to the back wall (it stood 2.1 m off it and smeared); the units down BOTH side walls (0.40 deep, goods 0.4 off the wall) become flat boards (pegboards and framed notices); the grandfather clock and the vintage cabinet (0.8 and 0.67 deep) go; the doormat stays flat; pictures 4096 wide; the maker-marked models are blanked or dropped.

### 4.1 The front, from the 3.2 parts

Rita's front is the 3.2 kit's own (every part built, `shopfront_ritas.glb`, 34,780 triangles, out of git; `python build_shopfront.py` rebuilds it) except the doors, the lobby and the side door's trim, which are this target's and the door family's. Door end: the viewer's LEFT (street high x). Zones across the bay (u, mm): side door 350 to 1294, shop door 1294 to 2300, window 2300 to 5650 (3350 long). Assembly order, bottom to top, then left to right:

1. pilaster (two, mirrored; plinth 600, shaft 290 x 140 proud)
2. stallriser (panel, z 0 to 600, window zone)
3. sill (75 thick, nose 150, window zone)
4. window_frame (T1 3L-9T as built (3.2 D6; the 2.2 table says 8T), 3350 mm long, z 600 to 2850)
5. shop door (T1, slot 1006, hinge on the viewer's right)
6. side door F1 from 3.1 (slot 944, hinge on the viewer's right)
7. console (scroll, two; both present)
8. fascia_board (5410 x 550 x 120 proud, bed mould 40) carrying the 4.1 board ritas_basecolour/height/orm/wear.png
9. cornice (5892 x 150 x 215 deep, broken forward 85 over each console; 12 Oct ruling: 150 mm as built)

| part | built by 3.2? | size and place (mm, 2.2 frame) | paint (sRGB) |
|---|---|---|---|
| pilaster, panel (two, the right one mirrored) | yes | slot 350; plinth z 0 to 600, 180 proud; shaft 290 x 140 proud, z 600 to 2540; capital 310 high to z 2850, top 350 x 175; base ogee 60 high | oxblood 93,46,49 |
| console, scroll (two) | yes | 240 x 205 x 550 (z 2850 to 3400), at u 175 and 5825; the third review's leaf and rolls as built (3.2 D1 to D3) | oxblood |
| fascia board | yes | 5410 x 550 x 120 proud, u 295 to 5705, z 2850 to 3400; cyma bed mould 40 (3.2 D5); carries the 4.1 board | oxblood (board texture: 4.1 ritas) |
| cornice | yes | 5892 x 150 x 215 deep, z 3400 to 3550, broken forward 85 over each console, mitred returns (3.2 D4); 150 mm as built is Jafar's ruling of 12 Oct | oxblood |
| sill | yes | 75 thick, nose 150, z 525 to 600, u 2300 to 5647 (3 short of the plinth) | white joinery 226,224,214 |
| stallriser, panel | yes (three panels) | z 0 to 600, 125 proud, three raised and fielded panels (1002, 1026, 1002) between 80 stiles | oxblood |
| window frame T1 | yes | jambs 50 x 95; seat 25 (z 600 to 625); 3 lights 625 to 2400; transom 2400 to 2480; **nine toplights as built** (3.2 D6; the 2.2 table says eight) 2480 to 2790; head 2790 to 2850; mullions 70 wide, front d 92, centres 1121.7 and 2228.3 from the frame's left; glass 6 mm at d 30 to 36, ovolo bead 16 x 12 | white joinery |
| shop door T1 | NO: specified here (4.2) | slot 1006, leaf 900 x 2040 at z 28, frame jambs 50 x 100, fanlight z 2131 to 2400 | white joinery |
| side door F1 (3.1) | door_F1.glb, yes | slot 944, mirrored (door end left): hinge on the shop-door side, knob on the pier side; head trimmed at z 2400 | buttermilk 222,212,184 |
| night grille (4.3) | NO: specified here | see 4.3 | black powder-coat 37,35,34 |

### 4.2 The shop door, the side door and the bell (the 3.2 kit has none)

The door is **specified from 2.2's section 10 (T1, M1, M2 in numbers; not built by 3.2)** and changed where a photograph of an untouched timber shop front disagrees (D1: Geograph 2192169, a Worcester fish shop's front, May 2000, scaled on the leaf's height). T1 for Rita's, in millimetres above the footway (the leaf's foot stands at 28 on a terrazzo threshold 25 high):

| member | z (mm) | kind and source |
|---|---|---|
| bottom rail | 28 to 228 | Photo (195 high in the photograph); 2.2 had 230 |
| lower panel, raised and fielded | 241 to 549 | Photo; the 12 mm sticking and the 8 mm bevel as 2.2's raised_field_edge |
| lock rail, carrying the plates | 549 to 871 | Photo: 322 high; **2.2 had the glass starting at 600 (D1 supersedes it)** |
| letter plate 250 x 40, brass | centre 678 | Photo: 0.32 of the leaf; 2.2 had 545; in the lock rail, centred across the leaf |
| lever handle on a 240 x 40 backplate | 1000 (rim latch and escutcheon at 950) | Read (the kit); the photograph's knob sits at 0.42 of the leaf: not adopted (narrow point) |
| glass, two panes | 871 to 1973 | Photo: 6 mm in an ovolo bead 14 x 11; the glass 99.5 px wide = 600 of a leaf 853 wide in the photograph; here the leaf is 900 with stiles 115 |
| glazing bar | centre 1423, 28 wide | Photo: one bar, two panes of about 540 |
| top rail | 1973 to 2068 | Photo: 95 high; 2.2 had 115 |
| kick plate / foot strip | brass 770 x 170 with 8 screws on the lower panel's bottom, a 30 high strip across the foot | Read (the kit); Photo (2.2's P1) |
| hinges | three 100 x 75 butts at 150 / middle / 150 on the window side | Read; the lever is on the viewer's left, the hinge on the right (2.2's game-frame reading of Rita's front) |
| threshold | terrazzo 25 high falling to 12, nose to d 130 | Read (2.2) |
| the bell | inside the leaf's top rail at z 1950 to 2050 | a spring-arm shop bell: a 20 x 3 mm steel strip curved 220 long fixed to the INSIDE face of the leaf's top rail 90 from the hanging stile at z 1950 to 2050, carrying a 70 mm brass bell hung 80 below it; it rings on the door's swing against a fixed clapper on the frame (Judgement: no 1975 to 1995 photograph of a shop-door bell was reached; the part is seen through the door's glass from the street and from the close view) |
| the OPEN / CLOSED sign | inside the glass at z 1500 | the plastic OPEN / CLOSED sign from 4.2 (the paper unit) on the inside of the door's glass at z 1500, hung by a suction cup: closed when the shop is shut; the hours plate (4.1) on the glass beside it |

The side door is the door family's **F1** (3.1: production/assets/cloud-week/door/door_F1.glb), used as 2.2 section 10 places it: slot 944, F1 mirrored where the door end is the viewer's left, its frame's outside face at d 100, trimmed at the shop transom, painted buttermilk (222, 212, 184), letter plate 250 x 40, the bell push the 3.1 fix leaves as a plain oblong. Metal doors (M1 aluminium: full-height glass in a 50 frame, 100 top rail, 170 bottom rail, a 300 chrome D pull and a floor spring; M2 bronze: a bronze kick panel to 600, glass above) are as 2.2 for the shops that have them.

### 4.3 The glass, the fascia, the paint and the grille

- **Glass:** one 6 mm plate per light (three lights, nine toplights), no astragal bars (D2: the photographs split; Rita's approved window is single sheets); a pane's reflectance is the game's (M_LedgerGlass, night 0.2 of day), not set here. Nothing lies across the glass but the 4.1 rows (WATCHES, JEWELLERY, LOANS, the number 5), the OPEN sign and the hours plate (GLS-01).
- **Fascia:** the 4.1 board `fascias/ritas/ritas_basecolour.png`, `_height.png`, `_orm.png`, `_wear.png` (5410 x 550 at 1 px/mm), the name RITA'S and PAWNBROKER, the street number 5; the hanging sign is the three balls on a bracket at street x 20.825 (4.1 `ritas_three_balls`). Rebuilt by `make_fascias.py OUTDIR --seed-base 1`.
- **Paint:** oxblood (93, 46, 49) on piers, consoles, board, cornice and stallriser (rough 0.45); gloss white, yellowed (226, 224, 214) on the window, sill and shop door (0.50); buttermilk on the side door; aged brass (160, 120, 55) fittings.
- **The grille at night:** an external lattice grille closed over the window zone from dusk to dawn: flat bars 20 x 4 mm at 45 degrees, the diamond 120 mm across, rivets at every crossing, a 40 x 40 box top rail under the fascia at z 2.50 and a bottom channel at z 0.70 above the crown, the plane 100 mm in front of the glass front (street y 5.145), powder black (37, 35, 34) rough 0.45; the window behind it stays lit.

### 4.4 The room

|  |  |
|---|---|
| box | W 5.3, H 2.4, D 4.5 m; camera_d 5.3; the card at street z 0.65 to 3.05, y +5.875, x 15.35 to 20.65 |
| floor | Poly Haven old_linoleum_flooring_01, tint (0.62, 0.55, 0.50), 1.2 m tile, worn path darker by hand-painted mask |
| walls | Poly Haven painted_plaster_wall tint (0.95, 0.86, 0.66), 1.5 m tile; dado same plaster tint (0.42, 0.27, 0.17) to z 1.0 m |
| ceiling | plaster off-white (180, 173, 158) |
| lights | day: daylight through the front opening (overcast sky area light 5.3 x 2.4 m on the card plane, 6500 K) PLUS the three battens on: the shop is open (Mon, Tue, Thu to Sat 9 to 17:30, Wed 9 to 13); night_lit: the three T12 battens only (cool white 4000 K, 5 ft, 38 mm), no sky: the window is lit all night (RULINGS 1 Oct); night_dark: a faint sodium wash through the front (linear colour (1.0, 0.7055, 0.0), 6 per cent of night_lit's energy) and one back-room night light through the ajar back door (2700 K, 0.3 m wide strip); rendered although Rita's is lit, so the spec has all three states |

| fixture | surface | stand-off | extent (x, y, z) | what |
|---|---|---|---|---|
| R-back-stock | back | 0.400 | [-2.6, 2.6]  [0.5, 2.25] | the stock wall: five tiers of 25 mm boards 0.40 deep (the television sets are 0.35 deep), filled shoulder to shoulder, a ticket on every piece; the lowest two tiers only at the ends, the counter standing in front of the middle |
| R-back-counter | back | 0.600 | [-1.9, 0.9]  [0.0, 1.05] | the staff counter, glass-topped case on a velvet bed, against the wall (0.6 deep, 1.05 high), 2.8 m long; notices on its front |
| R-back-door | back | 0.040 | [1.45, 2.35]  [0.0, 2.0] | a half-glazed painted door to the back room, ajar 0.15 m, 2.0 m high (flat: leaf 40 mm) |
| R-left-board | left | 0.080 |  [0.9, 2.7] [0.6, 1.8] | pledge board: a pegboard 1.8 x 1.2 m, 20 mm, hung with ticketed small goods flat to it |
| R-left-notices | left | 0.005 |  [3.0, 3.8] [1.5, 1.9] | the licence card and a handwritten UNREDEEMED PLEDGES FOR SALE card (paper, 3 mm) |
| R-right-board | right | 0.080 |  [1.4, 3.6] [0.8, 1.8] | tools hung flat on a pegboard 2.2 x 1.0 m |
| R-right-hung | right | 0.070 |  [0.4, 1.2] [1.2, 2.0] | two ukuleles hung by their heads and an ornate mirror, flat to the wall |
| R-floor-mat | floor | 0.012 | [-2.45, -1.55] [0.15, 0.85] [0.0, 0.012] | a worn door mat (flat) and the lino's own worn path |
| R-ceiling-tubes | ceiling | 0.045 | [-0.75, 0.75]  [0.0, 2.4] | three T12 battens in slim fittings |

| goods (model or scripted form) | n | on | why or note |
|---|---|---|---|
| television_02 | 4 | R-back-stock | CRT sets on the two upper-middle tiers; none on the lowest |
| boombox | 3 | R-back-stock |  |
| cassette_player | 3 | R-back-stock |  |
| portable_cassette_player | 4 | R-back-stock | maker's name painted out |
| Camera_01 | 3 | R-back-stock | lens-ring lettering painted out |
| vintage_video_camera | 2 | R-back-stock |  |
| vintage_binocular | 2 | R-back-stock |  |
| binoculars | 1 | R-back-stock |  |
| mantel_clock_01 | 2 | R-back-stock |  |
| alarm_clock_01 | 3 | R-back-stock |  |
| brass_vase_01 | 2 | R-back-stock |  |
| brass_vase_02 | 1 | R-back-stock |  |
| brass_vase_03 | 2 | R-back-stock |  |
| filmstrip_projector_8mm | 2 | R-back-stock |  |
| metal_toolbox | 2 | R-back-stock |  |
| hand_plane_no4 | 1 | R-back-stock |  |
| cardboard_box_01 | 9 | R-back-stock | the top tier: boxes of stock, a ticket each |
| CashRegister_01 | 1 | R-back-counter | the till at the counter's right end, on the glass |
| script:counter_jewellery | 1 | R-back-counter | rings, chains and watches on velvet in the case: Rita's approved scripted jewellery (tori, discs, links), kept as approved |
| pocket_watch | 3 | R-back-counter |  |
| vintage_pocket_watch | 3 | R-back-counter |  |
| pipe_wrench | 1 | R-right-board |  |
| cross_pein_hammer | 1 | R-right-board |  |
| handsaw_wood | 1 | R-right-board |  |
| hand_plane_no4 | 1 | R-right-board |  |
| Ukulele_01 | 2 | R-right-hung |  |
| ornate_mirror_01 | 1 | R-right-hung |  |
| wall_clock | 1 | R-back-stock | its dial's maker mark painted out (a 60 x 14 px patch under the 12) |
| script:pledge_tickets | 40 | R-left-board | paper tickets 25 x 12 mm with handwritten numbers: texture-printed cards, no model exists |

### 4.5 The near metre: the display

**Keeps:** production/assets/shop-displays/pawnbroker-display.glb as built (23 Poly Haven models on a stepped velvet bed, a ticket on each), 3.35 m long, 0.55 deep. **Changes:** drop digital_wrist_watch (a maker's mark, not in the glb's list today: confirm) and any model whose map shows a maker's name after the 1k inspection; add the night grille; pieces are not repeated more than twice (the third review's copy-paste note). Display frame: u from the window zone's viewer-left edge (0 to 3.35 m), v out from the back of the glass (0 to 0.55), w above the bed (the stallriser's top, 0.70 above the crown), at most 1.55 high.

| model | n | zone u0-u1, v0-v1, w0-w1 (m) | note |
|---|---|---|---|
| pocket_watch | 2 | 0.20-0.90, 0.05-0.35, 0.00-0.12 |  |
| vintage_pocket_watch | 2 | 0.90-1.50, 0.05-0.35, 0.00-0.12 |  |
| Camera_01 | 2 | 0.10-0.90, 0.15-0.50, 0.12-0.40 |  |
| vintage_video_camera | 1 | 1.00-1.50, 0.15-0.50, 0.12-0.40 |  |
| binoculars | 1 | 1.60-2.10, 0.15-0.50, 0.12-0.40 |  |
| round_spectacles | 1 | 2.20-2.60, 0.05-0.30, 0.12-0.30 |  |
| mantel_clock_01 | 1 | 0.20-0.90, 0.20-0.50, 0.40-0.75 |  |
| alarm_clock_01 | 2 | 1.00-1.90, 0.20-0.50, 0.40-0.75 |  |
| brass_vase_01 | 1 | 2.40-2.80, 0.20-0.50, 0.40-1.10 |  |
| brass_vase_02 | 1 | 2.90-3.20, 0.20-0.50, 0.40-0.95 |  |
| brass_vase_03 | 1 | 0.90-1.20, 0.30-0.50, 0.75-0.95 |  |
| ceramic_vase_01 | 1 | 1.30-1.70, 0.25-0.50, 0.75-1.15 |  |
| ceramic_vase_03 | 1 | 1.80-2.00, 0.25-0.45, 0.75-1.15 |  |
| antique_ceramic_vase_01 | 1 | 2.10-2.70, 0.20-0.50, 0.75-1.20 |  |
| standing_picture_frame_01 | 1 | 0.20-0.50, 0.25-0.40, 0.75-1.00 |  |
| standing_picture_frame_02 | 1 | 2.80-3.10, 0.25-0.40, 0.75-1.00 |  |
| portable_cassette_player | 2 | 1.70-2.30, 0.10-0.40, 0.00-0.20 | maker's name painted out |
| seadogs_compass | 1 | 0.40-0.70, 0.05-0.25, 0.12-0.22 |  |
| vintage_flashlight | 1 | 2.00-2.30, 0.05-0.35, 0.12-0.26 |  |
| cigarette_case | 1 | 1.20-1.70, 0.05-0.25, 0.00-0.03 | tobacco is allowed; a plain metal case |
| vintage_lighter | 1 | 1.80-2.00, 0.05-0.20, 0.00-0.07 | the stamp under the base blanked |
| magnifying_glass_01 | 1 | 0.50-0.80, 0.05-0.30, 0.00-0.03 |  |
| carved_wooden_elephant | 1 | 2.50-2.80, 0.05-0.25, 0.12-0.22 |  |
| horse_statue_01 | 1 | 0.40-0.80, 0.30-0.50, 0.75-1.00 |  |
| jug_01 | 1 | 3.00-3.30, 0.05-0.30, 0.12-0.32 |  |
| measuring_tape_01 | 1 | 1.50-1.70, 0.05-0.20, 0.12-0.19 | its label blanked |

### 4.6 The pictures, the spec entry and the cameras

Files `pawnbroker_day.png`, `pawnbroker_night_lit.png`, `pawnbroker_night_dark.png` (4096 x 1855) and `pawnbroker.json` (w 5.3, h 2.4, d 4.5, camera_d 5.3, pixels [4096, 1855]). The spec entry is unchanged except `pixels_wide` 2048 to 4096 and the display's `x0`/`x1` (15.45 to 18.8 measured on the street model's glass; 15.35 to 18.7 with the 3.2 front's window zone): a 0.10 m shift the builder takes from whichever front stands. Lit at night (RULINGS 1 Oct): night_lit is the picture the game shows all night; `spill_lumens` 350 and the display's rect light stay as approved.

| camera | eye (street m) | aim (street m) |
|---|---|---|
| STREET_SQUARE | [17.025, -3.505, 1.7] | [17.025, 5.255, 1.6] |
| STREET_30 | [11.967, -3.505, 1.7] | [17.025, 5.255, 1.6] |
| CLOSE_35 | [15.975, 3.755, 1.7] | [17.025, 5.515, 1.45] |
| CLOSE_35_B | [17.975, 3.755, 1.7] | [17.025, 5.515, 1.45] |

Parallax test (PRJ-02): between CLOSE_35 and CLOSE_35_B the card's centre moves **1322 px** (of 4096) by the rule.

## 5. The other nine, one table each

Each table is the shop's row set from `target.json`: front (variants against what 3.2 built), door, paint, fascia, room box and finishes, contents (grouped by the fixture they stand on), display, lights, and what it keeps and changes. Fixture ids name the stand-off class (`true` up to the 20 px budget, `tolerated` to the 40 px budget).

### 5.1 mickeys: minicab office (Mickey's) (east_parade bay 0, x 3 to 9)

|  |  |
|---|---|
| keeps / changes | Keeps: everything of the room: production/specs/mickeys-office.json, shop-room.py's mickeys branch, room_3d, its lamps and brightness values (spec entry unchanged). Changes: only the front is unit 7's: the A2 painted-steel refit assembled from the 3.2 parts, the 4.1 board with the raised gilt letters, the glass rows. |
| front | Alterations: steel_refit, repaint. Variants: pilaster clad, console scroll, cornice timber, stallriser tile_patterned, window M1 3L-3T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's right. Missing from 3.2: pilaster, stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 545; hinge on the viewer's left, lever on the right; paint powder_slate; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [62, 75, 87]; console [62, 75, 87]; cornice [62, 75, 87]; fascia_board [62, 75, 87]; stallriser [222, 212, 184]; window_frame [60, 74, 88]; shop_door [60, 74, 88]; side_door [93, 46, 49]; metal [170, 172, 174] |
| glass | 3 lights + 3 toplights, 6 mm plate; lettering rows: ['0632 960418', 'MINICABS · 24 HOURS', '1'] |
| fascia (4.1) | fascias/mickeys/mickeys_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'MICKEY’S']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 7:00-3:00 (next day); Tue 7:00-3:00 (next day); Wed 7:00-3:00 (next day); Thu 7:00-3:00 (next day); Fri 7:00-3:00 (next day); Sat 7:00-3:00 (next day); Sun 9:00-3:00 (next day) (hook-cast.json areas.mickeys); at night: lit (dark until Tom's key (spec lit_at_start false, lit_at_night true); after the key it is open to 3 am; in vignette-pieces lit_names) |
| room | the real walked room (mickeys-office.json; shop-room.py's mickeys branch; room_3d; the spec's lamps 150 lm, room 180 day and 300 night): not changed by this unit; the projected picture is only its far fallback |

### 5.2 fish_market: fishmonger (Fish Market) (east_parade bay 1, x 9 to 15)

|  |  |
|---|---|
| keeps / changes | Keeps: the research (FISHMONGER-2026-10-03.md, Picture Sheffield t13140 and t13138), the white-tile walls and red quarry floor of the 3 Oct code (shop-room.py 257, 287). Changes: no hand-made fish (the 3 Oct failure): the fish are CC0 scans or the window shows none; the slab and ice are real meshes in the display; the chiller counter goes against the back wall (it smeared as a black panel across the floor); the white slab no longer burns out at night (the room is dark at night). |
| front | Alterations: aluminium_refit, repaint. Variants: pilaster panel, console scroll, cornice timber, stallriser tile_square, window M1 4L-4T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's right. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 545; hinge on the viewer's left, lever on the right; paint alu_natural; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [196, 202, 206]; console [196, 202, 206]; cornice [196, 202, 206]; fascia_board [196, 202, 206]; stallriser [228, 228, 220]; window_frame [176, 178, 180]; shop_door [176, 178, 180]; side_door [35, 36, 40]; metal [170, 172, 174] |
| glass | 4 lights + 4 toplights, 6 mm plate; lettering rows: ['FRESH DAILY', 'SHELLFISH', 'SMOKED FISH', '3'] |
| fascia (4.1) | fascias/fish_market/fish_market_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'FISH MARKET'], ['trade', 'WET FISH'], ['trade', 'SHELLFISH'], ['trade', 'SMOKED']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 7:30-14:00; Tue 7:30-14:00; Wed 7:30-13:00; Thu 7:30-14:00; Fri 7:30-14:00; Sat 7:30-14:00 (hook-cast.json areas.fish_market); at night: dark (vignette-pieces lit_names omits east_parade_interior1; the shop shuts at 14:00) |
| room box | W 5.3, H 2.4, D 4.5; floor: red quarry tile 150 mm, grout 20 mm, wet (roughness 0.12); Poly Haven terracotta_floor_tiles as the base if it reads red enough, else the script's brick shader; walls: white glazed square tile 152 mm, grey grout, soiled (Poly Haven long_white_tiles or square_tiles), to the ceiling; dado same tile; ceiling painted white board (200, 198, 190) |
| contents of the room | F-back-counter (counter, stand-off 0.60): script:enamel_trays x8, script:fish_on_ice x1 // F-back-shelf (shelf_unit, stand-off 0.15): script:tins_and_jars x24 // F-back-hose (wall_mounted, stand-off 0.25): garden_hose_wall_mounted_01 x1 // F-right-clock (flat_hung, stand-off 0.05): wall_clock x1 // F-left-board (flat_board, stand-off 0.03): script:price_board_chalk x1 |
| display (real, 0.55 deep) | keeps: FISHMONGER-2026-10-03.md: a tilted white slab under crushed ice, fish in rows each with a per-lb ticket, white trays, lettering on the glass. Changes: everything in the display is a real mesh in the near metre; no fish is modelled by hand. Items: script:slab_and_ice x1, script:enamel_trays x6, script:fish_on_ice x1, lemon x8, script:price_stakes x14, script:chiller_pad x1 |
| lights | day: daylight through the front opening (overcast area light) plus two 5 ft battens on (open Mon to Sat 7:30 to 14:00, Wed to 13:00). night_lit: not used: the shop is shut after 14:00 and the street file leaves it dark (rendered for completeness: two battens on). night_dark: a faint sodium wash through the front (6 per cent) and the chiller's small glow lamp (2700 K) at the counter. Tubes: 2 x 5 ft T12. |
| pictures and spec | fishmonger_{day,night_lit,night_dark}.png 4096 x 1855 + fishmonger.json; spec entry in target.json `spec_entries` (id fishmonger, side +1, card x 9.35 to 14.65, display x 11.300 to 14.650) |

### 5.3 empty_unit: empty unit to let (east_parade bay 3, x 21 to 27)

|  |  |
|---|---|
| keeps / changes | Keeps: everything the street already draws: every pane whitewashed from inside, no interior card (terrace-front.py skips bay 3), the 4.1 letting board and whitewash. Changes: the front only: the unit's bare timber front assembled from the 3.2 parts (left console clipped off, paint gone), the whitewash tile from 4.1. |
| front | Alterations: empty_unit. Variants: pilaster panel, console scroll, cornice timber, stallriser boarded, window T2 3L-8T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678; hinge on the viewer's left, lever on the right; paint black_door; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [46, 37, 30]; console [46, 37, 30]; cornice [46, 37, 30]; fascia_board [46, 37, 30]; stallriser [46, 37, 30]; window_frame [170, 166, 156]; shop_door [35, 36, 40]; side_door [35, 36, 40]; metal [160, 120, 55] |
| glass | 3 lights + 8 toplights, 6 mm plate; lettering rows: ['', '7'] |
| fascia (4.1) | fascias/empty_unit/empty_unit_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks []; hanging sign none |
| night furniture | dark; the whitewash tile (glass/empty_unit/window_whitewash, 3250 x 1800 mm) over every pane and the door's glass; no grille |
| hours, lit | none (none: to let); at night: dark (empty; nothing lit) |
| room | none: every pane whitewashed from inside (4.1 `glass/empty_unit/window_whitewash`, 3250 x 1800 mm; the shop door's glass too), no card, no picture; a pale blank by day (LIT-03), dark at night; the letting board and boards as 4.1/4.4 |

### 5.4 steam_laundry: launderette (Steam Laundry) (east_parade bay 4, x 27 to 33)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct decision (a launderette with a service counter: the Steam Laundry), the real-room finding that the dryers and washers must stand against walls. Changes: no slab laundry, no dryer stack standing off the wall: machines stand against the BACK wall only; the side walls carry notices; the near metre is a real display of folded laundry and detergent boxes with fictional labels. |
| front | Alterations: aluminium_refit, box_sign, recessed_lobby, repaint. Variants: pilaster render, console scroll, cornice timber, stallriser tile_square, window M1 2L-1T (3350 mm long), shop door M1, side door F1. Door end the viewer's left. Missing from 3.2: pilaster, stallriser, window_frame, shop_door, lobby. Lobby: recessed 300 deep. |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 545; hinge on the viewer's right, lever on the left; paint alu_bronze; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [222, 209, 175]; console [222, 209, 175]; cornice [222, 209, 175]; fascia_board [222, 209, 175]; stallriser [228, 228, 220]; window_frame [84, 68, 53]; shop_door [84, 68, 53]; side_door [74, 48, 34]; metal [170, 172, 174] |
| glass | 2 lights + 1 toplights, 6 mm plate; lettering rows: ['SERVICE WASHES', '9'] |
| fascia (4.1) | fascias/steam_laundry/steam_laundry_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm), _emissive.png; name blocks [['name', 'STEAM LAUNDRY'], ['trade', 'LAUNDERETTE'], ['trade', 'SERVICE WASHES'], ['trade', 'DRY CLEANING']]; hanging sign steam_laundry_box |
| night furniture | none |
| hours, lit | Mon 8:00-17:30; Tue 8:00-17:30; Wed 8:00-17:30; Thu 8:00-17:30; Fri 8:00-17:30; Sat 8:00-17:30 (hook-cast.json areas.laundry); at night: dark (vignette-pieces lit_names omits east_parade_interior4; its box sign glows (4.1 emissive) but the room is dark) |
| room box | W 5.3, H 2.4, D 4.5; floor: grey vinyl tile 300 mm with a darker worn path (Poly Haven rubber_tiles tinted grey, or worn_tile_floor); walls: cream emulsion (222, 212, 184) above a white glazed tile dado 1.5 m (Poly Haven long_white_tiles); dado white tile to z 1.5; ceiling white board (205, 203, 196) |
| contents of the room | L-back-washers (machines, stand-off 0.60): script:washing_machine x4 // L-back-dryers (machines, stand-off 0.60): script:tumble_dryer x6 // L-back-shelves (shelf_unit, stand-off 0.30): script:wrapped_parcels x18 // L-right-notices (flat_hung, stand-off 0.05): wall_clock x1 |
| display (real, 0.55 deep) | keeps: SERVICE WASHES lettering on the glass (4.1), the research's folded parcels on shelves. Changes: folded laundry in real towers, two wicker baskets, boxed detergents with the project's fictional labels. Items: script:folded_towels x5, wicker_basket_01 x2, script:laundry_in_basket x2, script:detergent_boxes x10, script:laundry_shelf_board x1, script:paper_card_service_washes x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 8 to 17:30). night_lit: not used by the street file (dark); rendered with the three battens on. night_dark: a faint sodium wash and the dryers' two orange 'running' lamps (small, 2000 K, 0.01 m) so the room is not black. Tubes: 3 x 5 ft T12. |
| pictures and spec | launderette_{day,night_lit,night_dark}.png 4096 x 1855 + launderette.json; spec entry in target.json `spec_entries` (id launderette, side +1, card x 27.35 to 32.65, display x 27.350 to 30.700) |

### 5.5 grocer: grocer (east_parade bay 5, x 33 to 39)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct label atlas (production/assets/shop-goods/labels.jpg and .json: 32 fictional products in our OFL fonts) and its tin, packet, jar and bottle shapes. Changes: stock only on the back wall (0.25 deep) and on side shelves 0.10 deep (tins only); the near metre is a real tiered stand of produce and tins with scanned fruit; the printed tiles are on bevelled shapes, never plain blocks; the lobby's 0.6 recess takes nothing from the room. |
| front | Alterations: refit_1930s, recessed_lobby, repaint. Variants: pilaster render, console block, cornice timber, stallriser slab, window M2 3L-5T-sunrise (4294 mm long), shop door M2, side door none (the flat is reached from the rear yard). Door end the viewer's left. Missing from 3.2: pilaster, console, stallriser, window_frame, shop_door, lobby. Lobby: recessed 600 deep. |
| zones across the bay (u, mm) | side door None; shop door [350.0, 1356.0]; window [1356.0, 5650.0] |
| door | M2 leaf 900 x 2040; glass foot 600; letter plate z 545; hinge on the viewer's right, lever on the left; paint bronze_plate; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [222, 209, 175]; console [222, 209, 175]; cornice [222, 209, 175]; fascia_board [36, 61, 49]; stallriser [36, 61, 49]; window_frame [110, 86, 50]; shop_door [110, 86, 50]; metal [170, 172, 174] |
| glass | 3 lights + 5 toplights, 6 mm plate; lettering rows: ['11'] |
| fascia (4.1) | fascias/grocer/grocer_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'FAMILY GROCER'], ['trade', 'HIGH CLASS PROVISIONS']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 8:00-17:30; Tue 8:00-17:30; Wed 8:00-13:00; Thu 8:00-17:30; Fri 8:00-17:30; Sat 8:00-17:30 (Judgement from the Shops Act (shop-hours-1990 NOTE): not found for the grocer); at night: lit (vignette-pieces lit_names east_parade_interior5 (practicals chosen so the parade is not a shopping centre; the hours say it is shut: a conflict, kept as the street file has it)) |
| room box | W 5.3, H 2.4, D 4.5; floor: brown linoleum (Poly Haven linoleum_brown); walls: cream (222, 209, 175) emulsion; dado bottle green (36, 61, 49) to z 1.1; ceiling cream plaster (196, 188, 168) |
| contents of the room | G-back-gantry (shelf_unit, stand-off 0.25): script:tins x160, script:packets x90, plastic_crate_02 x3, wicker_basket_01 x2, hamburger_buns x3, wall_clock x1 // G-back-shelves-right (shelf_unit, stand-off 0.20): script:jars x24, script:bottles x12 // G-back-counter (counter, stand-off 0.60): CashRegister_01 x1, script:counter_scale x1 // G-left-tins (shelf_unit, stand-off 0.10): script:tins x40 // G-right-tins (shelf_unit, stand-off 0.10): script:packets x30 |
| display (real, 0.55 deep) | keeps: the 1930s refit's deep lobby; the research's crate-and-stand dressing; Holyoake's photograph (Geograph 2184467, 1999) for density. Changes: produce is scanned (Poly Haven apple, banana, lemon, onion; Sketchfab ffishAsia CC0 cabbage, potato, satsuma, pear by his login); tins and jars carry atlas labels. Items: script:tiered_stand x1, plastic_crate_02 x3, plastic_crate_03 x2, food_apple_01 x40, lemon x12, yellow_onion x15, bananas x3, script:cabbage_potato_satsuma x1, script:tomatoes x30, script:tin_pyramids x3, script:jars x18, wicker_basket_02 x1, hamburger_buns x2, script:price_cards x14 |
| lights | day: daylight through the front opening plus three battens on (hours not found: settled as Mon to Sat 8 to 17:30, early closing Wed 13:00, Shops Act). night_lit: the three battens on and a pendant opal globe in the lobby (2700 K, 60 W): the street file lights this unit (east_parade_interior5). night_dark: a faint sodium wash and the till's glow lamp. Tubes: 3 x 5 ft T12. |
| pictures and spec | grocer_{day,night_lit,night_dark}.png 4096 x 1855 + grocer.json; spec entry in target.json `spec_entries` (id grocer, side +1, card x 33.35 to 38.65, display x 33.350 to 37.644) |

### 5.6 chandler: ship's chandler (east_chandler bay 0, x 40 to 46)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct trade list (buoys, lifebuoy, life jacket, lanterns, boots, oil, crates) and the CC0 set in fetch_polyhaven.py. Changes: NO explosives-marked drum (Barrel_01 is out); the buoy stands flat against the back wall at a scaled height; nothing hangs from the ceiling; rope is twisted by script with ambientCG Rope textures (no CC0 model): coils stand on shelves. |
| front | Alterations: aluminium_refit, repaint. Variants: pilaster panel, console scroll, cornice timber, stallriser tile_square, window M1 3L-3T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's left. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 545; hinge on the viewer's right, lever on the left; paint alu_natural; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [44, 53, 83]; console [44, 53, 83]; cornice [44, 53, 83]; fascia_board [44, 53, 83]; stallriser [170, 190, 172]; window_frame [176, 178, 180]; shop_door [176, 178, 180]; side_door [44, 53, 83]; metal [170, 172, 174] |
| glass | 3 lights + 3 toplights, 6 mm plate; lettering rows: ['EST. 1879', '13'] |
| fascia (4.1) | fascias/chandler/chandler_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'SHIP CHANDLER'], ['trade', 'ROPE · PAINT · CHARTS · TWINE'], ['end', '13'], ['end', '13']]; hanging sign chandler_hanging_board |
| night furniture | woven galvanised mesh screens (wire 2 mm, 12 mm mesh) inside the lower lights (z 0.70 to 1.55 above the crown), three panels, in place when the shop is shut; the lit night view has them out of the lit lights' way (the E.E. Sharp photograph shows them over the lower lights only) |
| hours, lit | Mon 8:00-17:00; Tue 8:00-17:00; Wed 8:00-13:00; Thu 8:00-17:00; Fri 8:00-17:00; Sat 8:00-17:00 (Judgement from the Shops Act: not found for the chandler); at night: lit (vignette-pieces lit_names east_chandler_interior0 (the hours say shut by 17:00: kept as the street file has it)) |
| room box | W 5.3, H 2.4, D 4.5; floor: oiled boards (Poly Haven old_wooden_floor_02); walls: cream emulsion (214, 204, 178) with a dark green dado 1.0 m (the E.E. Sharp photograph's green); dado (30, 62, 44) to z 1.0; ceiling painted board (192, 186, 168) |
| contents of the room | C-back-shelves (shelf_unit, stand-off 0.30): script:paint_tins x40, oil_tin x5, small_oil_can_01 x4, cleaner_tin_01 x4, rubber_boots x4, signal_flashlight x3, Lantern_01 x4, script:rope_coils x6, script:twine_reels x10 // C-back-counter (counter, stand-off 0.60): CashRegister_01 x1, seadogs_compass x3, Lantern_01 x1 // C-back-hooks (flat_hung, stand-off 0.18): life_jacket x4, lifebuoy x2, script:oilskin_sou_wester x3 // C-right-board (flat_board, stand-off 0.07): script:shackles_blocks x24 // C-left-charts (flat_board, stand-off 0.05): script:chart_posters x6 // C-floor-buoy (free_at_wall, stand-off 0.55): ocean_buoy x1 |
| display (real, 0.55 deep) | keeps: the trade list; E.E. Sharp's window (Geograph 3378991, 1983): a chandler's lower lights were screened inside with woven galvanised mesh when shut. Changes: real ropes, lifebuoy, lanterns, boots and tins in the near metre; no ship model, no explosives drum. Items: lifebuoy x1, life_jacket x2, script:rope_coils x5, rubber_boots x3, Lantern_01 x2, wooden_lantern_01 x1, seadogs_compass x2, oil_tin x4, small_oil_can_01 x3, script:paint_tin_pyramid x1, script:oilskin_sou_wester x2, brass_blowtorch x1 |
| lights | day: daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8 to 17, Wed to 13:00, Shops Act). night_lit: two battens on and a hurricane lamp (Lantern_01, 2200 K, lit) on the counter: the street file lights this unit (east_chandler_interior0). night_dark: a faint sodium wash. Tubes: 2 x 5 ft T12. |
| pictures and spec | chandler_{day,night_lit,night_dark}.png 4096 x 1855 + chandler.json; spec entry in target.json `spec_entries` (id chandler, side +1, card x 40.35 to 45.65, display x 40.350 to 43.700) |

### 5.7 tea_rooms: tea room (west_north bay 2, x 24 to 30)

|  |  |
|---|---|
| keeps / changes | Keeps: the research (Formica tables, a menu board, a half-height cafe curtain, steamed glass) and the 3 Oct food models (carrot cake, strawberry cake, tea set). Changes: NO Gothic chairs, NO empty frames, NO free tables in the picture (they smeared): tables and chairs are real and only in the window; the room is the counter, hatch and shelves on the back wall and flat boards; the cafe curtain hides the outer lights. |
| front | Alterations: repaint, flat_panel_sign. Variants: pilaster flute, console scroll, cornice timber, stallriser render, window T1 3L-6T (3350 mm long), shop door T1, side door F1. Door end the viewer's left. Missing from 3.2: pilaster, stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678; hinge on the viewer's right, lever on the left; paint door_cream; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [120, 74, 44]; console [120, 74, 44]; cornice [120, 74, 44]; fascia_board [222, 209, 175]; stallriser [120, 74, 44]; window_frame [222, 212, 184]; shop_door [222, 212, 184]; side_door [74, 48, 34]; metal [160, 120, 55] |
| glass | 3 lights + 6 toplights, 6 mm plate; lettering rows: ['14'] |
| fascia (4.1) | fascias/tea_rooms/tea_rooms_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'Tea Rooms'], ['trade', 'BREAKFASTS, LUNCHES & TEAS']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 6:30-22:00; Tue 6:30-22:00; Wed 6:30-22:00; Thu 6:30-22:00; Fri 6:30-22:00; Sat 6:30-22:00; Sun 8:00-12:00 (hook-cast.json areas.cafe); at night: lit (vignette-pieces lit_names west_north_interior2; hours-research cafe 6:30 to 22:00) |
| room box | W 5.3, H 2.4, D 4.5; floor: chequered vinyl, cream and brown 300 mm (Poly Haven old_linoleum_flooring_01 tinted, a chequer mask); walls: cream (222, 212, 184); dado brown (120, 74, 44) to z 1.1; ceiling cream board (208, 200, 180) |
| contents of the room | T-back-counter (counter, stand-off 0.55): tea_set_01 x2, carrot_cake x1, strawberry_chocolate_cake x1, hamburger_buns x2, vintage_electric_kettle x1, CashRegister_01 x1, script:cake_dome x1, script:tea_urn x1 // T-back-shelf (shelf_unit, stand-off 0.20): metal_jug x1, script:cups_saucers x24 // T-left-frames (flat_hung, stand-off 0.04): hanging_picture_frame_02 x1, hanging_picture_frame_03 x1, wall_clock x1 // T-right-frames (flat_hung, stand-off 0.04): hanging_picture_frame_01 x1 |
| display (real, 0.55 deep) | keeps: the half-height cafe curtain on a brass rod at z 1.50 above the footway (2.2's tea_rooms glazing note). Changes: the window table set for tea, in real geometry in the middle light (the two outer lights carry the curtain); no chairs or tables anywhere else. Items: round_wooden_table_02 x1, painted_wooden_chair_01 x2, tea_set_01 x1, script:sugar_bowl_menu x1, carrot_cake x1, script:cake_stand x1, strawberry_chocolate_cake x1, potted_plant_04 x1, script:cafe_curtain x2, script:window_card_menu x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 6:30 to 22:00, Sun 8 to 12). night_lit: three battens on, the steam-warm window: the street file lights this unit (west_north_interior2); open to 22:00. night_dark: a faint sodium wash and the counter's pilot lamp. Tubes: 3 x 5 ft T12. |
| pictures and spec | tea_room_{day,night_lit,night_dark}.png 4096 x 1855 + tea_room.json; spec entry in target.json `spec_entries` (id tea_room, side -1, card x 24.35 to 29.65, display x 26.300 to 29.650) |

### 5.8 ironmonger: ironmonger (west_north bay 1, x 30 to 36)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct tools and cleaners set (fetch_polyhaven.py ironmonger), the research's drawer wall, the 4.1 hanging board and 'PARAFFIN' on the fascia. Changes: tools hang FLAT on pegboards on the side walls (they stood on side shelves 0.4 off the wall and smeared); modern aerosols and cleaners with real-brand look-alikes are dropped; paint tins are the project's labelled tins; the drawer wall is a flat front. |
| front | Alterations: repaint. Variants: pilaster flute, console scroll, cornice timber, stallriser panel, window T2 2L-5T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: pilaster, stallriser, window_frame, shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678; hinge on the viewer's left, lever on the right; paint dark_green; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [30, 62, 44]; console [30, 62, 44]; cornice [30, 62, 44]; fascia_board [188, 173, 136]; stallriser [30, 62, 44]; window_frame [30, 62, 44]; shop_door [30, 62, 44]; side_door [35, 36, 40]; metal [160, 120, 55] |
| glass | 2 lights + 5 toplights, 6 mm plate; lettering rows: ['EST. 1884', '16'] |
| fascia (4.1) | fascias/ironmonger/ironmonger_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'IRONMONGER'], ['trade', 'TOOLS &'], ['trade', 'HARDWARE'], ['trade', 'PAINTS &'], ['trade', 'PARAFFIN']]; hanging sign ironmonger_hanging_board |
| night furniture | none |
| hours, lit | Mon 8:30-17:30; Tue 8:30-17:30; Wed 8:30-13:00; Thu 8:30-17:30; Fri 8:30-17:30; Sat 8:30-17:30 (Judgement from the Shops Act: not found for the ironmonger); at night: dark (vignette-pieces lit_names omits west_north_interior1) |
| room box | W 5.3, H 2.4, D 4.5; floor: bare boards, oiled (Poly Haven old_wooden_floor_03); walls: pale green-cream (204, 206, 180); dado dark green (30, 62, 44) to z 1.0; ceiling cream board (200, 192, 172) |
| contents of the room | I-back-drawers (drawer_wall, stand-off 0.10): script:drawer_fronts x60 // I-back-shelves (shelf_unit, stand-off 0.28): script:paint_tins x40, oil_tin x6, small_oil_can_01 x4, cleaner_tin_01 x4, lightbulb_01 x12, watering_can_metal_01 x3, metal_toolbox x2, brass_blowtorch x1, drain_cleaner x3 // I-back-counter (counter, stand-off 0.60): CashRegister_01 x1, measuring_tape_01 x1 // I-left-pegboard (flat_board, stand-off 0.08): adjustable_wrench x2, combination_wrench x3, cross_pein_hammer x2, wooden_hammer_01 x1, pliers x3, tongue_groove_pliers x2, screwdriver x4, screwdrivers_02 x1, flathead_screwdriver x3, handsaw_wood x2, hatchet x1, ratchet_wrench x2, pipe_wrench x1, bolt_cutters_01 x1, crowbar_01 x1 // I-right-pegboard (flat_board, stand-off 0.08): trowel_01 x3, wooden_broom x2, garden_gloves_01 x4, dustpan x2, mousetrap x6 // I-back-floor (free_at_wall, stand-off 0.58): metal_trash_can x1, wooden_ladder x1, cement_bag x3, metal_jerrycan_green x3 |
| display (real, 0.55 deep) | keeps: the 3 Oct idea: tools, cleaners and oils, a watering can, brooms, a blowtorch. Changes: a stack of tin buckets is not in Poly Haven: watering cans and boxes stand for it; every can's label is blanked or the atlas's. Items: script:paint_tin_pyramid x1, watering_can_metal_01 x2, metal_toolbox x2, brass_blowtorch x1, tire_pump x1, sledgehammer_01 x1, garden_gloves_01 x6, trowel_01 x4, oil_tin x4, cleaner_tin_01 x4, lightbulb_01 x12, garden_sprinkler_01 x1, plastic_broom x3, script:price_cards x12 |
| lights | day: daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8:30 to 17:30, Wed to 13:00, Shops Act). night_lit: not used by the street file (dark): two battens on if rendered. night_dark: a faint sodium wash only. Tubes: 2 x 5 ft T12. |
| pictures and spec | ironmonger_{day,night_lit,night_dark}.png 4096 x 1855 + ironmonger.json; spec entry in target.json `spec_entries` (id ironmonger, side -1, card x 30.35 to 35.65, display x 30.350 to 33.700) |

### 5.9 newsagent: newsagent and tobacconist (west_north bay 0, x 36 to 42)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct trade (papers, sweets, cigarettes behind the counter, a pension counter; no pools coupons, no lottery, no drink); Pinner 1989 (Geograph 3403654, 5945841) for the lit shop and the dark glass. Changes: no gold ribbon across the window (a stale card in the engine: the build's check looks for any card in front of the glass); magazines are real thin meshes in the display and flat covers in the room; the cigarette gantry is a back-wall unit 0.12 deep. |
| front | Alterations: repaint, box_sign, roller_shutter. Variants: pilaster panel, console scroll, cornice timber, stallriser panel, window T1 3L-8T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: shop_door. Lobby: flush. |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678; hinge on the viewer's left, lever on the right; paint dove_grey; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [150, 152, 150]; console [150, 152, 150]; cornice [150, 152, 150]; fascia_board [222, 209, 175]; stallriser [150, 152, 150]; window_frame [226, 224, 214]; shop_door [150, 152, 150]; side_door [24, 38, 78]; metal [160, 120, 55] |
| glass | 3 lights + 8 toplights, 6 mm plate; lettering rows: ['TOBACCONIST & CONFECTIONER', '18'] |
| fascia (4.1) | fascias/newsagent/newsagent_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm), _emissive.png; name blocks [['name', 'NEWSAGENT']]; hanging sign none |
| night furniture | the roller shutter (2.2's alterations.roller_shutter) lowered when shut: not used in the lit view |
| hours, lit | Mon 6:00-17:30; Tue 6:00-17:30; Wed 6:00-17:30; Thu 6:00-17:30; Fri 6:00-17:30; Sat 6:00-17:30; Sun 7:00-12:00 (hook-cast.json areas.newsagent); at night: lit (vignette-pieces lit_names west_north_interior0 (the hours say shut at 17:30: kept as the street file has it; the newsagent's box sign is lit by 4.1 anyway)) |
| room box | W 5.3, H 2.4, D 4.5; floor: grey and blue vinyl tile 300 mm (Poly Haven rubber_tiles tinted); walls: white emulsion (226, 224, 214); dado pale grey (150, 152, 150) to z 1.0; ceiling white board (212, 210, 202) |
| contents of the room | N-back-counter (counter, stand-off 0.60): CashRegister_01 x1, script:sweet_jars x10, stationery_supplies x3, office_notepads x4 // N-back-gantry (shelf_unit, stand-off 0.12): script:cigarette_packs x100, cigarette_pack x8 // N-left-racks (flat_board, stand-off 0.04): script:magazine_covers x60 // N-right-racks (flat_board, stand-off 0.04): script:greeting_cards x40, wall_clock x1 |
| display (real, 0.55 deep) | keeps: the 4.2/4.4 window board SB1 (hand cards) on the glass; the sweets, papers and cigarettes trade. Changes: magazines and newspapers are real thin meshes 2 to 4 mm with a curl and a fold; a card rack of fictional cards; no card floats in front of the glass. Items: script:newspapers x10, script:magazines x24, script:sweet_jars x6, script:cigarette_cartons x6, script:card_rack x1, stationery_supplies x2, office_notepads x3, script:postcard_rack x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 6 to 17:30, Sun 7 to 12). night_lit: three battens on, the whole shop bright: the street file lights this unit (west_north_interior0); the roller shutter is up. night_dark: a faint sodium wash through the front; the shutter is down in the shut-up variant (4.1's shutter_down). Tubes: 3 x 5 ft T12. |
| pictures and spec | newsagent_{day,night_lit,night_dark}.png 4096 x 1855 + newsagent.json; spec entry in target.json `spec_entries` (id newsagent, side -1, card x 36.35 to 41.65, display x 36.350 to 39.700) |

**Conflict (not resolved):** hook-cast.json places 'Hals_shop' (keeper hal, hours 10 to 18, Wed 10 to 13) at street x 39, which is inside the newsagent's bay (x 36 to 42): either the coin shop is the newsagent's neighbour (there is none) or one of them is not on the street. Not resolved: the newsagent is built as ruled (3 Oct).

## 6. The three failures of 3 October, answered

Commit 2f475f5 (3 October) set the seven shops aside after three fresh reviews: goods made by hand, then named faults, then what a projected room cannot do at a metre or two.

**F1. goods made by hand (3 Oct, first review: 'toys beside Rita's scanned stock').**

104 Poly Haven models (CC0, each read from the API today) carry every shop's goods; what has no CC0 model is a SCAN named by uid (Sketchfab ffishAsia CC0, checked today) needing Jafar's login, or a short scripted form whose reason is written beside it (`scripted` in target.json: 51 kinds, each with a why); hand-modelled fish are forbidden; packaged goods are bevelled shapes carrying the project's fictional label atlas (production/assets/shop-goods/labels.jpg), never plain colour blocks

**F2. named faults (3 Oct, second round).**

- displays placed as if the door were on Rita's side (half behind the door): each display's range is the window zone of the 2.2 bay table for that shop's door end (DSP-01)
- a black chiller panel smeared across the fish shop's floor: the chiller is a white counter against the back wall, nothing free in the room (SO-01)
- the white slab burnt out at night: the fish shop is dark at night; no picture has more than 1 per cent of pixels at 250 or above (PIC-05)
- Gothic chairs and empty frames in the tea room: WoodenChair_01 and the Gothic set are denied; the frames carry the project's own prints; chairs and tables exist only in the window (INV-02, SO-02)
- an explosives sign on a drum at the chandler's: Barrel_01 is denied; no drum stands in the display (INV-02)
- a gold ribbon drawn across the newsagent's window and every stood card outside the glass: a check that nothing but the listed lettering, the OPEN sign, the hours plate and SB1 lies in front of the glass (GLS-01)
- faceted fruit: fruit are scans (Poly Haven apple, lemon, onion, bananas; ffishAsia cabbage, potato, satsuma, pear); the one scripted fruit, the tomato, is a one-try item set aside if it reads as toys
- slab laundry: laundry is stacks of bevelled towels with a woven-towel material and a lean, parcels with string and tags, baskets of displaced cloth
- counters, chairs and dryers standing off the walls: no fixture stands off a surface by more than the budget (SO-01 to SO-04)

**F3. what a projected room cannot do at a metre or two (3 Oct, third round).**

the numbers from the game's own rule: stock only on the back wall (0.30 deep is true, a 0.60 counter or machine against it is tolerated), the side walls carry boards and racks at most 0.10 (0.05 true), the floor and ceiling only flat things (0.025); anything else stands in the display, which is real geometry in the near 0.55 m. The CLOSE view stands at 1.5 m from the glass, 35 degrees off, because there the whole window is seen at under 62 degrees (the glass's hand-over) and the surfaces are sharp at 4096 wide; the slide numbers are in TARGET.md section 3 (`method.honest_range`); the picture is 4096 wide because at 2048 it is soft over 4 per cent of the glass at 1.5 m and 13 per cent at 0.5 m

## 7. Reuse: what each part keeps and what it changes

| part | keeps | changes |
|---|---|---|
| the method (research NOTE.md, CLOSE-RANGE, GOODS, DRESSING, FISHMONGER, hours, glass reflections, FRONTAGE) | a pre-projected picture per room and state, the near metre real, lights per state, the never-list, the trades' goods and fittings | the room is no longer allowed to hold anything the picture cannot honestly show (the budgets); CLOSE-RANGE's 'real rooms' recommendation is NOT followed here (the brief asks for textures); its 'keep everything flat against the walls' is the rule |
| production/specs/shop-interiors.json | the camera rule, the three states, the never list, the two entries (mickeys unchanged; pawnbroker's room, card, camera_d, brightness, lit values unchanged) | eight entries added (spec_entries in target.json: fishmonger, launderette, grocer, chandler, tea_room, ironmonger, newsagent; the pawnbroker's pixels_wide 2048 to 4096 and its display x0/x1 noted against the 3.2 front); no entry for the empty unit (no card) |
| tools/art-recipes/shop-room.py | the box, the camera rule, the three renders, the JSON beside each, model() from Poly Haven, texmat(), --display, --export-room (inert) | the room builders for the seven trades are rewritten to the fixtures in target.json (free-standing counters and units removed); pixels_wide 4096; the maker-mark pass; the inventory.json |
| tools/ue/make_interior_material.py | everything: its `trace` is the rule the cloud gate imports; the HLSL is unchanged | none |
| tools/art-recipes/fetch_polyhaven.py | the fetcher and the SETS | SETS gain the ids of the inventory; none of the denied |
| production/assets/shop-goods/labels.jpg and make_label_atlas.py | the 32 fictional products | twelve tiles added (paint, varnish, twine, tobacco, crab paste, detergent) in the same fonts |
| production/assets/shop-displays/pawnbroker-display.glb | as built, with its 23 models | maker marks blanked; the night grille added; no piece repeated more than twice |
| the 3.2 kit (production/cloud-week/kit/shopfront) | pilaster (panel), console (scroll), fascia board, cornice (150 as built, 12 Oct), sill, stallriser (panel, three panels), window frame T1 (3 lights, nine toplights as built): Rita's front is complete but for the doors | nine variants are missing for the other fronts (front.missing_from_3_2 in each shop); the doors and the lobbies are specified here, from 2.2 section 10, with three changes (D1) and the bell |
| 2.2 (targets/shopfronts) | the ten fronts' table, paints, glazing layouts, door ends and hinges | T1 door: glass foot, lock rail, letter plate, a glazing bar (D1); the bell |
| 4.1 (2d/fascias) | the ten boards, the four hanging signs, the glass rows, the whitewash and the letting board, unchanged | none; each shop names its board |
| 4.2 to 4.4 (2d/paper) | the OPEN/CLOSED sign, the newsagent's board SB1, the letting boards | none |
| 3.1 doors | F1 for every side door | none |
| the set-aside branch shops-wip-2026-10-03 (a local branch on the PC, not in this clone) | nothing taken: it was not reachable and its goods were made by hand | replaced; the reason is F1 |

## 8. Photographs win: each disagreement

- **D1, where a timber shop door's glass starts.** Target: 600 (level with the sill; Leadenhall 2019 at 0.304 of the leaf; DOR-06). Photograph or research: 871 +-30 above the footway (843 above the leaf's foot: 0.413 of the leaf, Geograph 2192169, a fish shop's untouched front, May 2000); the lock rail runs 549 to 871 with the letter plate in it at 678. Chosen: the photograph: T1 door glass from 871 above the footway (843 above the leaf's foot), the lock rail 549 to 871, the letter plate at 678, one glazing bar at 1423; the aluminium and bronze doors keep 2.2's numbers. Why: Leadenhall is a 2019 heritage restoration of a London arcade; the Worcester front is a working shop in the period's condition and the nearer match; 2.2's DOR-06 (door glass foot = sill top) is replaced for T1 doors only. Flagged for Jafar (Needs you).
- **D2, the glass of the window lights.** Target: one sheet per light, no astragal bars (Rita's approved window). Photograph or research: Geograph 2192169 shows each light divided by one bar at the door's bar height; Pinner 1989 shows single large sheets (hardware) and aluminium-framed sheets (newsagent). Chosen: single sheets per light as 2.2 (Rita's window is the model and approved); the divided pattern is recorded as a possible variant, not adopted. Why: RULINGS 2 Oct; the photographs split
- **D3, the door leaf's width.** Target: 900 in a 1006 slot. Photograph or research: about 853 (140 px of a 335 px leaf) in an older door. Chosen: 900 as 2.2: the slot is fixed by the bay; the photograph is within 6 per cent of it. Why: inside the error
- **D4, the stallriser's height.** Target: 600. Photograph or research: 571 +-18 (94 px of the leaf's 335). Chosen: 600. Why: inside the error (5 per cent)
- **D5, how bright the room reads from the street by day.** Target: the game's day brightness 0.15. Photograph or research: P1 and P3: the glass is mostly reflection, the room dim; only a lit, bright shop (Pinner's newsagent) shows its goods by day. Chosen: the game's 0.15 kept for every shop (the spec's values are the game's). Why: the research (NOTE.md section 3 and 8) and these photographs agree: over-bright day interiors are the commonest giveaway
- **D6, an open-fronted grocer's window.** Target: a glazed window with a 1930s bronze front. Photograph or research: P2 shows stock stood out on stands in an open front. Chosen: glazed, as 2.2. Why: the street's grocer is a 1930s refit with glass; the density and the stands are taken, not the open front
- **D7, mesh over a chandler's lower lights.** Target: none. Photograph or research: P4 shows woven galvanised mesh screens inside the lower lights of a shut chandler's. Chosen: added as the chandler's night furniture (three panels). Why: the photograph shows it
- **D8, the street's lit list against the hours.** Target: vignette-pieces lit_names: 6 units lit at night. Photograph or research: the hours research: everything shut by 8 pm; newsagent 17:30; the grocer, ironmonger and chandler not found. Chosen: the street file's list is kept (RULINGS 1 Oct: lit windows, not one wash); the hours are the town's and are noted. Why: a conflict between two files of the project; not mine to resolve
- **D9, the chandler's paint.** Target: navy on piers, consoles, board and cornice, natural aluminium window. Photograph or research: P4 (Hull, 1983) shows a chandler's front in dark green. Chosen: navy as 2.2 and 4.1 (the street's board is navy); the photograph's green is used for the room's dado. Why: the Hull shop is another shop; the street's colours are fixed by 4.1

**The main photograph's readings** (P1; the photograph is nearly face-on; every edge was read by eye off a 4x enlargement with a 10-pixel grid (error +-3 px); ONE dimension fits the scale: the door leaf's height, 335 px, taken as the street's 2040 mm (6.09 mm a pixel), so every other number is a ratio of the leaf's height and is Photo only to that assumption (a 2100 leaf would move the glass foot to 867)):

| what | pixel |
|---|---|
| door leaf top (underside of the transom's board) | y 122.0 |
| door leaf bottom / threshold | y 457.5 |
| glass top | y 137.5 |
| glazing bar, centre | y 228.0 |
| glass foot | y 319.0 |
| letter plate, centre | y 350.5 |
| number plate, centre | y 338.0 |
| handle, centre | y 316.0 |
| lower panel field, top | y 372.5 |
| lower panel field, bottom | y 422.5 |
| stallriser top (tile cap) | y 362.0 |
| leaf left edge | x 230.0 |
| leaf right edge | x 370.0 |
| glass left | x 251.0 |
| glass right | x 350.5 |

## 9. The inventory

**Every Poly Haven model the target places (104, CC0, each read from api.polyhaven.com on 12 October with a 1k glTF):**

| id | size cm | triangles | published | shops |
|---|---|---|---|---|
| Camera_01 | 21.4x26.3x7.8 | 26987 | 2020-03-30 | ritas |
| CashRegister_01 | 60x62.4x62.1 | 9927 | 2020-03-30 | ritas, grocer, chandler, tea_rooms, ironmonger, newsagent |
| Lantern_01 | 12.2x9.7x29.4 | 33902 | 2020-05-28 | chandler |
| Ukulele_01 | 17.8x5.1x52.7 | 8912 | 2020-03-30 | ritas |
| adjustable_wrench | 6.8x3.1x25.4 | 5390 | 2026-06-30 | ironmonger |
| alarm_clock_01 | 22.8x16.8x17.4 | 13006 | 2021-08-13 | ritas |
| antique_ceramic_vase_01 | 25.5x25.5x44 | 9408 | 2021-06-15 | ritas |
| bananas | 60x24.4x17.9 | 46868 | 2026-06-19 | grocer |
| binoculars | 16.7x28.8x7.7 | 19248 | 2026-06-30 | ritas |
| bolt_cutters_01 | 28.1x3.6x93.8 | 6719 | 2022-12-02 | ironmonger |
| boombox | 72.4x18.6x47 | 10168 | 2023-09-22 | ritas |
| brass_blowtorch | 12.9x25.9x21.1 | 11750 | 2025-08-01 | chandler, ironmonger |
| brass_vase_01 | 22.7x22.7x69.2 | 21440 | 2021-08-26 | ritas |
| brass_vase_02 | 21x21x52.9 | 6890 | 2021-11-17 | ritas |
| brass_vase_03 | 8.3x8.3x20 | 2616 | 2022-02-11 | ritas |
| cardboard_box_01 | 38.7x51.6x34.2 | 16952 | 2022-12-16 | ritas |
| carrot_cake | 22.5x22.5x9.8 | 13790 | 2022-08-17 | tea_rooms |
| carved_wooden_elephant | 10.9x5.8x9.6 | 2752 | 2022-02-02 | ritas |
| cassette_player | 12.9x4.9x23.7 | 4830 | 2020-08-19 | ritas |
| cement_bag | 46.2x70x18 | 844 | 2026-06-08 | ironmonger |
| ceramic_vase_01 | 20.5x20.6x40.1 | 2548 | 2021-06-15 | ritas |
| ceramic_vase_03 | 11.2x11.2x41.4 | 2784 | 2021-06-15 | ritas |
| cigarette_case | 32.3x10.1x2.4 | 16912 | 2026-06-08 | ritas |
| cigarette_pack | 5.6x2.9x10.3 | 7582 | 2026-07-03 | newsagent |
| cleaner_tin_01 | 8.8x8.8x13 | 3560 | 2023-03-06 | chandler, ironmonger |
| combination_wrench | 5.7x33.7x2.2 | 1986 | 2026-07-03 | ironmonger |
| cross_pein_hammer | 9.9x2.4x30 | 2124 | 2026-03-20 | ritas, ironmonger |
| crowbar_01 | 4x12.8x55.5 | 2300 | 2023-01-27 | ironmonger |
| drain_cleaner | 16.5x5.6x17.9 | 4338 | 2023-12-15 | ironmonger |
| dustpan | 33.2x36.8x10 | 4332 | 2026-06-09 | ironmonger |
| filmstrip_projector_8mm | 25.4x60.3x34.5 | 32697 | 2026-06-20 | ritas |
| flathead_screwdriver | 3x3x26.1 | 2300 | 2023-02-15 | ironmonger |
| food_apple_01 | 9.8x9.6x8.5 | 7012 | 2021-07-07 | grocer |
| garden_gloves_01 | 22.7x29.9x7.6 | 6822 | 2022-12-30 | ironmonger |
| garden_hose_wall_mounted_01 | 46.7x25x55.7 | 11684 | 2022-12-12 | fish_market |
| garden_sprinkler_01 | 36x24.9x21.6 | 8192 | 2023-01-23 | ironmonger |
| hamburger_buns | 39.7x11.4x6.3 | 11588 | 2026-03-13 | grocer, tea_rooms |
| hand_plane_no4 | 33.1x8.4x19.8 | 8220 | 2022-11-25 | ritas |
| handsaw_wood | 4.1x63.3x16.7 | 2548 | 2023-03-03 | ritas, ironmonger |
| hanging_picture_frame_01 | 59.4x1.6x84.1 | 2586 | 2021-06-15 | tea_rooms |
| hanging_picture_frame_02 | 75.2x3.3x50 | 3678 | 2021-06-15 | tea_rooms |
| hanging_picture_frame_03 | 38.5x3.2x50.2 | 24348 | 2021-09-15 | tea_rooms |
| hatchet | 2.6x10.4x28.9 | 5250 | 2023-11-25 | ironmonger |
| horse_statue_01 | 16.4x10.8x22 | 22388 | 2021-10-22 | ritas |
| jug_01 | 27.5x16.8x21.1 | 5770 | 2022-08-26 | ritas |
| lemon | 6.9x6.8x9.5 | 4012 | 2024-07-17 | fish_market, grocer |
| life_jacket | 69.6x18.4x99.2 | 8968 | 2026-06-09 | chandler |
| lifebuoy | 78.3x15.5x84.1 | 10728 | 2026-06-30 | chandler |
| lightbulb_01 | 6x6x10 | 4372 | 2022-11-28 | ironmonger |
| magnifying_glass_01 | 13.2x2.7x27.2 | 7240 | 2021-10-06 | ritas |
| mantel_clock_01 | 48.4x25.1x16.1 | 29742 | 2021-09-17 | ritas |
| measuring_tape_01 | 4.1x16.9x7.3 | 2868 | 2021-10-15 | ritas, ironmonger |
| metal_jerrycan_green | 37.4x17.1x50.1 | 9636 | 2026-06-09 | ironmonger |
| metal_jug | 19.7x19.5x28.8 | 6040 | 2024-05-22 | tea_rooms |
| metal_toolbox | 40x29.2x34.7 | 14228 | 2026-04-16 | ritas, ironmonger |
| metal_trash_can | 184.7x55.6x90.6 | 13960 | 2023-09-27 | ironmonger |
| mousetrap | 5.5x10x1.8 | 5136 | 2023-05-19 | ironmonger |
| ocean_buoy | 106.7x95.2x265.6 | 12240 | 2026-04-16 | chandler |
| office_notepads | 110.3x66x2.2 | 666 | 2026-06-09 | newsagent |
| oil_tin | 11.5x15.4x20.5 | 2834 | 2026-06-20 | chandler, ironmonger |
| ornate_mirror_01 | 48.6x2.6x74.4 | 14246 | 2021-09-01 | ritas |
| painted_wooden_chair_01 | 43.2x54x95.6 | 724 | 2021-09-29 | tea_rooms |
| pipe_wrench | 8.4x3.4x40.5 | 10746 | 2023-08-25 | ritas, ironmonger |
| plastic_broom | 41.6x56.7x119.8 | 18736 | 2026-06-20 | ironmonger |
| plastic_crate_02 | 50.6x40.6x25.4 | 5840 | 2026-06-09 | grocer |
| plastic_crate_03 | 48.1x26.5x26.6 | 21740 | 2026-07-03 | grocer |
| pliers | 5.5x1.8x18 | 4540 | 2026-06-20 | ironmonger |
| pocket_watch | 5.8x1.6x7.6 | 15615 | 2026-06-09 | ritas |
| portable_cassette_player | 17.2x4x13 | 13307 | 2026-03-20 | ritas |
| potted_plant_04 | 17x18.6x26.8 | 6097 | 2021-06-15 | tea_rooms |
| ratchet_wrench | 4.4x4.3x24.6 | 8796 | 2022-12-09 | ironmonger |
| round_spectacles | 15.8x14.9x4.6 | 11810 | 2026-03-24 | ritas |
| round_wooden_table_02 | 79.6x79.6x74.6 | 4254 | 2025-03-24 | tea_rooms |
| rubber_boots | 89.1x26.9x37.3 | 35004 | 2026-06-09 | chandler |
| screwdriver | 2.7x2.7x20.9 | 3412 | 2026-06-20 | ironmonger |
| screwdrivers_02 | 10x27x2.7 | 3548 | 2026-07-03 | ironmonger |
| seadogs_compass | 8.1x15x8.7 | 11645 | 2026-04-16 | ritas, chandler |
| signal_flashlight | 7.1x4.5x15 | 9730 | 2026-06-09 | chandler |
| sledgehammer_01 | 20.8x9x100.6 | 2596 | 2023-01-20 | ironmonger |
| small_oil_can_01 | 26.6x10.4x23.7 | 16746 | 2021-06-15 | chandler, ironmonger |
| standing_picture_frame_01 | 20.1x10x25 | 1634 | 2021-06-15 | ritas |
| standing_picture_frame_02 | 21.7x10.2x26.6 | 2986 | 2021-06-15 | ritas |
| stationery_supplies | 30.2x8.4x16.4 | 4412 | 2026-03-24 | newsagent |
| strawberry_chocolate_cake | 24.4x24x7.9 | 27054 | 2024-07-19 | tea_rooms |
| tea_set_01 | 91.8x48.4x16.5 | 40296 | 2021-11-05 | tea_rooms |
| television_02 | 40x35x41.1 | 2310 | 2026-07-03 | ritas |
| tire_pump | 25.5x10.1x58 | 6572 | 2023-02-03 | ironmonger |
| tongue_groove_pliers | 6.3x24.4x1.4 | 2694 | 2026-07-03 | ironmonger |
| trowel_01 | 9.9x34.7x10.3 | 5242 | 2022-12-26 | ironmonger |
| vintage_binocular | 19.4x19.9x6.8 | 19362 | 2026-07-03 | ritas |
| vintage_electric_kettle | 32.1x24.9x30.5 | 14838 | 2026-06-20 | tea_rooms |
| vintage_flashlight | 9.6x30.5x14.4 | 10562 | 2026-07-03 | ritas |
| vintage_lighter | 8.2x1.4x6.6 | 3366 | 2026-03-20 | ritas |
| vintage_pocket_watch | 6.2x1.4x8 | 4200 | 2021-12-01 | ritas |
| vintage_video_camera | 7.1x13.3x14.5 | 18682 | 2025-06-16 | ritas |
| wall_clock | 32x4.7x32 | 3658 | 2026-06-09 | ritas, fish_market, steam_laundry, grocer, tea_rooms, newsagent |
| watering_can_metal_01 | 19.1x45.2x19.7 | 11837 | 2023-01-18 | ironmonger |
| wicker_basket_01 | 38.3x29.5x11.7 | 22276 | 2023-01-06 | steam_laundry, grocer |
| wicker_basket_02 | 37.5x27.1x21.8 | 17850 | 2024-07-31 | grocer |
| wooden_broom | 49x11.3x145.4 | 14258 | 2026-06-20 | ironmonger |
| wooden_hammer_01 | 11.2x2.3x27.9 | 3617 | 2022-07-15 | ironmonger |
| wooden_ladder | 95.9x50x133.5 | 8492 | 2026-06-09 | ironmonger |
| wooden_lantern_01 | 22.1x23.5x53 | 8321 | 2022-03-11 | chandler |
| yellow_onion | 7.2x6.9x8.6 | 5444 | 2024-07-10 | grocer |

**Looked at and refused (denied list; the self-check refuses any of them):**

| id | why |
|---|---|
| ArmChair_01 | a Gothic armchair |
| Barrel_01 | a drum printed with an explosives sign (the 3 Oct chandler fault) |
| CheeseBox_01 | a crate stencilled RADIO: not what its name says |
| Drill_01 | a cordless drill printed '18V 1.3Ah LITHIUM-ION': after 1992 (rule: nothing after 1992) |
| GothicBed_01 | gothic furniture |
| GothicCabinet_01 | gothic furniture |
| SchoolChair_01 | a school chair (the school stands closed; children rule) |
| SchoolDesk_01 | a school desk (children rule) |
| Television_01 | a maker's name ('VTECH' look-alike) on the bezel: television_02 is used instead |
| WoodenChair_01 | a Gothic carved chair (the 3 Oct tea-room fault) |
| all_purpose_cleaner | modern pink cleaner bottle with a printed name ('Planis'): replaced by the label atlas |
| american_football | a toy |
| antique_estoc | a weapon |
| antique_katana_01 | a weapon |
| bar_chair_round_01 | a pub stool |
| barrel_03 | an oil drum, fine, but 0.63 m deep (no room in the display) and not needed |
| baseball_01 | a toy |
| baseball_bat | a toy |
| bleach_bottle | modern thick-bleach bottle with a printed name |
| brass_goblets | drinking vessels |
| camera_security_01 | CCTV is rare in 1990 (canon) |
| chess_set | kept out of the pawnbroker's display only if the builder reads it as a gambling table; allowed in the room (a board game) |
| classic_laptop | a notebook computer: not in a 1990 British shop window and arguably after 1992 |
| dartboard | a pub game |
| digital_wrist_watch | a Casio-style face with the maker's mark; the digital watch is also a 1980s-90s object but the mark is a real brand: not used |
| dirty_football | a toy |
| fishermans_hat | a boonie hat, not a sou'wester (GOODS note) |
| football | a toy |
| gamepad | a modern pad: after 1992 |
| gaming | n/a |
| gaming_console | a games console of the 2010s: after 1992 |
| kite_shield | a weapon |
| korean_public_payphone_01 | a Korean payphone: wrong country and carrier mark |
| leather_cleaner_can | a branded spray can ('RAY'S LEATHER') |
| lubricant_spray | a look-alike of a real spray ('PH 40'): a real brand |
| multi_cleaner_bottle | modern cleaner packaging with a printed logo: replaced by the label atlas |
| ornate_medieval_dagger | a weapon |
| ornate_medieval_mace | a weapon |
| painted_wooden_cabinet | not needed |
| plastic_crate_01 | a drinks crate lettered 'GALLER ...': a brewer's or bottler's crate (alcohol rule) and a maker's mark |
| plastic_jerrycan | a modern fuel can lettered 'The Old Man' |
| rubber_duck_toy | a toy (children rule) |
| russian_food_cans_01 | Cyrillic labels (wrong country) |
| security_camera_01 | CCTV is rare in 1990 (canon) |
| security_camera_02 | CCTV is rare in 1990 (canon) |
| service_pistol | a firearm: not in a shop window |
| stick_grenade | a weapon |
| vintage_cabinet_01 | 0.67 m deep: too far off the wall; dropped from Rita's room |
| vintage_grandfather_clock_01 | 0.8 m deep as modelled: stands too far off the wall (budget); dropped from Rita's room |
| vintage_radio_transceiver | a military transceiver: not period stock for this window |
| wine_barrel_01 | alcohol |
| wine_bottles_01 | alcohol |
| wooden_barrels_01 | cellar barrels: alcohol connotation |

**Made by script because no CC0 model exists (each with its reason; the cheapest method that should read at 1 to 3 m, per the GOODS note; any that fails its first try is set aside):**

| form | shops | why |
|---|---|---|
| script:bottles | grocer | bottles with atlas tiles (washing-up liquid, brown sauce, orange squash, vinegar) |
| script:cabbage_potato_satsuma | grocer | Sketchfab ffishAsia CC0 scans (cabbage x4, potato x20, satsuma x12, pear x6), decimated and baked: REQUIRES Jafar's Sketchfab login |
| script:cafe_curtain | tea_rooms | a half-height curtain: cream cotton gathered on a brass rod, scalloped head; two panels over the outer lights; cloth cannot be a CC0 model |
| script:cake_dome | tea_rooms | an opaque-shelled dome with a faked rim highlight (the GOODS note's rule for glass over goods) |
| script:cake_stand | tea_rooms | a two-tier china stand: lathe forms |
| script:card_rack | newsagent | a wire spinner rack of fictional greetings cards: geometry from dimensions |
| script:chart_posters | chandler | invented chart sheets (no real coast, no real chart maker) |
| script:chiller_pad | fish_market | a white laminate back panel 25 mm at the display's rear edge, so the slab reads as a counter and the picture's counter is not doubled |
| script:cigarette_cartons | newsagent | cartons with atlas tiles: tobacco is allowed |
| script:cigarette_packs | newsagent | bevelled boxes with the label atlas's tobacco tiles (fictional makers), the Poly Haven cigarette_pack is used only as the shape; the model's own 'Kentucky Ace' face is not used |
| script:counter_jewellery | ritas | rings, chains and watches on velvet in the case: Rita's approved scripted jewellery (tori, discs, links), kept as approved |
| script:counter_scale | grocer | a brass and enamel counter scale with a dial: no CC0 model; from dimensions |
| script:cups_saucers | tea_rooms | stacked cups and saucers: lathe forms with a glaze, no CC0 model beyond tea_set_01 |
| script:detergent_boxes | steam_laundry | packets and a bottle with tiles from the label atlas (HOLME Soap Flakes, FERNSIDE Washing-up Liquid): fictional makers |
| script:drawer_fronts | ironmonger | flat drawer fronts with brass label holders and ring pulls: geometry from dimensions, labels are texture |
| script:enamel_trays | fish_market | white enamel trays 0.45 x 0.30 x 0.05 with a rolled rim: no CC0 model; each carries fish (below) |
| script:fish_on_ice | fish_market | the counter's fish: Sketchfab ffishAsia CC0 scans (cod, mackerel, herring, flounder) when Jafar gives the login; NONE are hand-modelled. Until then the trays hold ice and tickets only and the shop's review says so |
| script:folded_towels | steam_laundry | folded towels and sheets as bevelled boxes 0.45 x 0.30 x 0.05 each, ambientCG Fabric020 and Fabric021 (towel weave) tinted, stacked 6 to 9 high with a lean of 1 to 3 degrees |
| script:greeting_cards | newsagent | flat cards with invented seaside and flower art |
| script:jars | grocer | screw-lid jars, opaque contents, atlas tiles (jam, marmalade, pickled onions, honey) |
| script:laundry_in_basket | steam_laundry | soft cloth: a displaced heap per basket, no CC0 model |
| script:laundry_shelf_board | steam_laundry | a laminate bed cover 20 mm |
| script:magazine_covers | newsagent | flat covers drawn by script: invented titles, no real magazine, no children, no betting or drink content, halftone pictures of objects and landscapes |
| script:magazines | newsagent | fanned magazine covers 3 mm: generated pages, no children, no betting |
| script:newspapers | newsagent | folded dailies 4 mm thick in a stepped row with invented mastheads and headlines (the street's own paper, no real titles) |
| script:oilskin_sou_wester | chandler | a sewn pattern of 4 to 6 panels with a back brim, yellow oilskin: no CC0 model (GOODS note: the fishermans_hat model is a boonie hat, wrong) |
| script:packets | grocer | bevelled boxes (2 to 3 mm bevel) with the atlas's 12 packet tiles |
| script:paint_tin_pyramid | chandler, ironmonger | 21 tins in a pyramid, atlas labels |
| script:paint_tins | chandler, ironmonger | lathe tins 0.18 with a lid rim and a wire bail, labels from new atlas tiles (marine varnish, antifouling, deck paint, white spirit: fictional makers) |
| script:paper_card_service_washes | steam_laundry | a hand-lettered card on a stand: texture on a 3 mm card |
| script:pledge_tickets | ritas | paper tickets 25 x 12 mm with handwritten numbers: texture-printed cards, no model exists |
| script:postcard_rack | newsagent | a turning rack with invented seaside postcards (PH postcard_set_01's pictures are world landmarks and are not used) |
| script:price_board_chalk | fish_market | chalk lettering is a texture: numerals and COD, HADDOCK, PLAICE, KIPPERS only (no alcohol, no brand) |
| script:price_cards | grocer, ironmonger | hand-lettered cards 70 x 50 mm on wire stakes |
| script:price_stakes | fish_market | white plastic stick-in tickets 40 x 25 mm on 100 mm stakes with a handwritten price in per-lb (the 1990 price: cod about 2.60 a lb, ONS series CZOL) |
| script:rope_coils | chandler | three-strand twisted sweep with ambientCG Rope001 and Rope002, four colours, standing on edge: no CC0 model |
| script:shackles_blocks | chandler | steel shackles, cleats and blocks: simple extrusions on the board |
| script:slab_and_ice | fish_market | a white marble slab sloping 12 degrees toward the glass, 3.35 x 0.55 m, with a 40 mm lip (Poly Haven marble_01 or ambientCG Marble012 on a box); crushed ice: a displaced bed (ambientCG Ice002) with 300 instanced chunks of four shapes |
| script:sugar_bowl_menu | tea_rooms | a sugar bowl and a card menu on a stand: small lathe and card |
| script:sweet_jars | newsagent | screw-lid jars with opaque sweets (the research's method: real opaque contents, solid lid and label, faked rim): ambientCG Candy001 and Candy002 stripes for humbugs; no CC0 model |
| script:tea_urn | tea_rooms | a stainless urn: a cylinder from dimensions |
| script:tiered_stand | grocer | a three-tier timber display stand 0.18 high a step (Holyoake's photograph), made from dimensions |
| script:tin_pyramids | grocer | three pyramids of 28 tins each with atlas labels |
| script:tins | grocer | 12- to 16-sided cylinders with a rim and a bevelled seam, labels from the atlas (12 tin tiles), turned +-4 degrees, a few pulled forward or missing |
| script:tins_and_jars | fish_market | tins and jars with labels from the project's label atlas (pilchards, salmon, a crab-paste tile to add): shapes by script, print from make_label_atlas.py |
| script:tomatoes | grocer | no CC0 tomato exists: a glossy red flattened sphere with a calyx, varied per instance (the research's cheapest method; set aside after one try if it reads as toys) |
| script:tumble_dryer | steam_laundry | no CC0 dryer: the same cabinet at 0.60 deep with the 0.40 door |
| script:twine_reels | chandler | cylinders with a twine wrap (ambientCG Rope001) |
| script:washing_machine | steam_laundry | no CC0 washing machine exists in Poly Haven or ambientCG: a cabinet, a porthole ring, a dark glass door, a drawer, from dimensions |
| script:window_card_menu | tea_rooms | a hand-lettered card (BREAKFASTS, LUNCHES, TEAS) on the glass's inside: texture on a card |
| script:wrapped_parcels | steam_laundry | brown paper parcels 0.30 x 0.20 x 0.12 tied with string, a numbered tag: boxes with a paper material, no CC0 model |

**Scans (CC0, Sketchfab, on the allowlist as 'Sketchfab CC0 filter'; read 12 October; the download API answers 401 without a login, so none is downloaded):**

| uid | name | licence | faces | published |
|---|---|---|---|---|
| cf5d4d0e5a814a7fad01acde343f0a57 | CC0 マダラ 🐟 ♂ Pacific Cod, Gadus macrocephalus | CC0 Public Domain | 2108513 | 2024-01-16 |
| 14c4b738e74340e395dbf6296a836090 | CC0 マサバ 🐟 Chub Mackerel, Scomber japonicus | CC0 Public Domain | 868666 | 2022-01-08 |
| 6f0c50234b13476aadadffb7a54ce9cf | CC0 マサバ 🐟 Chub Mackerel, Scomber japonicus | CC0 Public Domain | 813004 | 2022-01-09 |
| e36819a39e5841f5971a01e1af6bf399 | CC0 ニシン 🐟 Pacific Herring, Clupea pallasii | CC0 Public Domain | 535752 | 2022-01-13 |
| abaafcb174bc44f1a0206e267925bc8f | CC0 ヒラメ 🐟 Bastard Halibut, P. olivaceus | CC0 Public Domain | 953234 | 2021-11-12 |
| 8865dba23628468198015640b245d551 | CC0 ヌマガレイ 🐟 Starry Flounder, P. stellatus | CC0 Public Domain | 1534210 | 2021-07-11 |
| 4915ee5a2d9f46af9a24d3b8da505d00 | CC0 イシガニ 🦀 ♂ Asian Paddle Crab, C. japonica | CC0 Public Domain | 567578 | 2021-08-21 |
| 7bf09478c7f94b419f1b90261c538e65 | CC0 ホッコクアカエビ 🦐 Alaskan Pink Shrimp, P. eous | CC0 Public Domain | 525166 | 2022-01-25 |
| 371bf54b6d2c40229ec45bca7feb3db6 | CC0 ホッコクアカエビ 🦐 Alaskan Pink Shrimp, P. eous | CC0 Public Domain | 182262 | 2022-01-25 |
| 410b4f06e5e444168d4f6554de3380d2 | CC0 リンゴ 🍎 林檎 Apple, Malus pumila | CC0 Public Domain | 1144524 | 2021-12-20 |
| 5e15ee8fb8ed4aedaf73f9628f3f83a7 | CC0 キャベツ Cabbage, B. oleracea var. capitata | CC0 Public Domain | 1917202 | 2026-03-19 |
| 56eec86c9102494f8ae568ea9c3cc338 | CC0 ジャガイモ 🥔 Potato, Solanum tuberosum | CC0 Public Domain | 2885866 | 2023-01-28 |
| fb8d5cfc74eb4de6bf9df9140b0d4043 | CC0 ミカン 🍊 Satsuma Mandarin, Citrus unshiu | CC0 Public Domain | 841638 | 2022-01-08 |
| d6ca8cf47e7c41509f6aab5c60c8b360 | CC0 セイヨウナシ Pear, Pyrus communis | CC0 Public Domain | 1226002 | 2023-01-03 |
| 6d60d76ab46342a5b79cde89160bc183 | CC0 レモン Lemon, Citrus limon | CC0 Public Domain | 441936 | 2026-02-04 |

**Surfaces:** Poly Haven textures old_linoleum_flooring_01, linoleum_brown, painted_plaster_wall, dirty_carpet, long_white_tiles, square_tiles, terracotta_floor_tiles, marble_01, marble_tiles, rubber_tiles, worn_tile_floor, old_wooden_floor_02, old_wooden_floor_03, white_plaster_02, ceiling_interior, terrazzo_tiles, concrete_floor_painted (all exist: LIVE check); ambientCG Ice001, Ice002, Marble012, Rope001, Rope002, Candy001, Candy002, Fabric020, Fabric021, Fabric028, Fabric029, Cardboard002, Wicker010B, Terrazzo004, Tiles032, Tiles040, SurfaceImperfections001, Smear001, Fingerprints001, Scratches001, Leaking001, Metal042A (the ones read from its API are in ambientcg_checked.json). The packaged goods' labels are the project's atlas (production/assets/shop-goods/labels.jpg: 32 fictional makers in our OFL fonts), twelve tiles to add.

**Rules the inventory enforces.** every model a build places is listed in its inventory.json; each must be in `polyhaven`, `scripted` or a Sketchfab uid of `sketchfab_checked`; none in `denied`; no object, material or text contains a word of the blocklists; every Poly Haven model is inspected at 1k for lettering and any maker's mark is painted out of its base-colour map (thumbnails only were looked at on 12 October: the gate's first check is by eye)

## 10. Checks (target.json `checks`; the cloud gate and the build run them)

| id | name | measure | expected | tolerance | applies to |
|---|---|---|---|---|---|
| PIC-01 | picture files | each state's PNG is 4096 x 1855, 8-bit sRGB, with the JSON beside it holding w, h, d, camera_d, pixels, states | w 5.3, h 2.4, d per shop, camera_d 5.3 | exact | 8 shops |
| PIC-02 | no black void in the picture | mean Rec.709 luma of the day / night_lit picture; the share of pixels under 12; the largest connected region under 12 | day mean >= 83.7 and night_lit mean >= 55.9 (0.7 of Rita's approved 119.5 and 79.8); share under 12 <= 0.03; no region under 12 larger than 3 per cent of the area | none | 8 shops |
| PIC-03 | night_dark is dark, not black | mean luma of the night_dark picture | 12.4 to 40 (Rita's approved 17.7, 0.7 to 2.3 times) | none | 8 shops |
| PIC-04 | the floor line and the back wall where the rule puts them | a flat-colour pass (one colour a surface) of the room; the back wall's four corners in the 4096 x 1855 picture | for D 4.5: top-left and bottom-right corners as method.floor_and_back_wall.back_wall_in_picture.px_4096 (about (940, 426) and (3156, 1429)); for another D recomputed by the rule | +-8 px on each corner | 8 shops |
| PIC-05 | nothing burnt | share of pixels with any channel at 250 or above | <= 0.01 in every picture | none | 8 shops |
| PIC-06 | each surface has texture | the standard deviation of the luma inside the back wall's rectangle, the floor's trapezoid and each side wall's trapezoid | >= 6 levels in each (not a flat colour) | none | 8 shops |
| PRJ-01 | the identity camera | from the render camera (card centre, 5.3 m in front, mid height) every card point shows its own picture pixel | /u - u0/ and /v - v0/ <= 1 px at 4096 | 1 px | 8 shops |
| PRJ-02 | the room shifts with the eye | between CLOSE_35 and CLOSE_35_B (2.0 m apart along the street) the back wall's centre point lands at picture columns that differ by the rule's value, and the whole card picture differs | the column difference equals target.json's `parallax_test.expected_du_px` per shop; the mean absolute difference of the two baked card pictures >= 8 levels | +-1.5 px; none | 8 shops |
| PRJ-03 | the gate shows the game's rule | the baked card picture for a camera equals the picture sampled through trace() for the same camera and card | mean absolute difference <= 0.5 level, no pixel off by more than 3 | none | 8 shops |
| SO-01 | back wall stand-off | the stand-off (depth) of every fixture on the back wall | <= 0.30 true, <= 0.60 tolerated (counters, machines, free pieces at the wall), nothing deeper | none | 8 shops |
| SO-02 | side wall stand-off | the stand-off of every fixture and every placed good on a side wall | <= 0.05 flat, <= 0.10 tolerated, nothing deeper | none | 8 shops |
| SO-03 | floor and ceiling stand-off | the height of every thing on the floor, the drop of every thing from the ceiling | <= 0.025 true, <= 0.05 tolerated (a batten fitting 0.045) | none | 8 shops |
| SO-04 | nothing in the middle of the room | any mesh whose bounding box is more than 0.60 m from every wall and more than 0.05 above the floor | none | none | 8 shops |
| DSP-01 | the display stands in the window | every display item's extent against the window zone and the envelope: u inside the window zone, v 0 to 0.55 from the back of the glass, w from the bed to height_max_w | all inside; none in front of the shop door or the side door | 5 mm | 8 shops |
| DSP-02 | real geometry in the display | every display item is a mesh (no card, no picture), none a flat alpha cut-out except price cards 3 mm thick | true | none | 8 shops |
| INV-01 | inventory exists | each Poly Haven id in the inventory exists with a 1k glTF | true for every model in the inventory | none | 8 shops |
| INV-02 | nothing denied is placed | the build's inventory.json against inventory.denied | no denied id | none | 8 shops |
| INV-03 | every model is allowed | every model placed is in inventory.polyhaven, inventory.scripted or a Sketchfab uid of inventory.sketchfab_checked | true | none | 8 shops |
| INV-04 | scripted goods are the listed ones and carry a why | every scripted object name is a key of inventory.scripted; no fish, crab or prawn is a scripted body | true | none | 8 shops |
| INV-05 | no maker marks | every base-colour map of every placed model and every label tile is searched (OCR by eye on a 2k sheet at the gate; by script: the manifest text) for inventory.brand_blocklist words | none found | none | 8 shops |
| NEV-01 | no people, drink, betting, children | object, material and text names and every glyph string of the build against inventory.content_blocklist | no match | none | 10 shops |
| NEV-02 | nothing after 1992 | no model from inventory.denied; no modern phone, flat screen, cordless-drill or LED lamp in any inventory | true | none | 10 shops |
| FRN-01 | the front's parts at their sizes | the 3.2 check's rows for the assembled bay (pilaster 350 slot / 290 shaft / 140 proud, console 240 x 205 x 550, fascia 5410 x 550 x 120, cornice 150, sill 75, stallriser 600, window frame at the shop's variant, transom 2400 to 2480, head 2790 to 2850) | as 2.2's checks | as 2.2's | 10 shops |
| FRN-02 | window and door zones | u of the window, shop door and side door against front.zones_u_mm; their centres against front.centres_street_x_m | equal | 2 mm; 3 mm | 10 shops |
| FRN-03 | the shop door | T1: leaf 900 x 2040 at z 28, glass 871 to 1973 with one bar at 1423 (28 wide), lock rail 549 to 871, letter plate 250 x 40 at z 678, lever side and hinge side as the table, the bell at z 1950 to 2050 inside; M1 and M2 as 2.2 | equal | 5 mm | 10 shops |
| FRN-04 | the glass | the number of lights and toplights per shop; 6 mm plate at d 30; no pane in front of another | lights = n_mullions + 1; toplights = front.toplights_as_built (Rita's: nine, the 3.2 kit's departure D6; the 2.2 table says eight; the other fronts as front.glazing) | exact | 10 shops |
| FRN-05 | paint colours | the base colour of each painted part against front.paint_srgb | within 6 levels per channel (aged paint: the 2.2 values) | 6 | 10 shops |
| FRN-06 | lobby | the grocer's door recessed 600 and the launderette's 300, floors as 2.2 | equal | 5 mm | grocer, steam_laundry |
| FAS-01 | the fascia's sign in place | the 4.1 board texture on the fascia board (sample 12 points of the board's front: the render's base colour against the PNG at the same u, v); the applied sign (Mickey's letters, laundry and newsagent box, tea room panel) at the 2.2 u and z | equal | 3 levels; 5 mm | 10 shops |
| FAS-02 | hanging signs | Rita's three balls, the laundry's box, the ironmonger's and the chandler's boards at their 4.1 mounts | equal | 10 mm | ritas, steam_laundry, ironmonger, chandler |
| GLS-01 | nothing across the glass | every object between the glass and the street plane is one of: the 4.1 glass rows, the OPEN/CLOSED sign, the hours plate, SB1 (newsagent), the letting board (empty unit), the night grille (Rita's) or mesh (chandler) | true | none | 10 shops |
| LIT-01 | lit shops lit at night, dark shops dark | mean luma of the room-only composite (picture x brightness 0.7, glass reflection off) over the glass lights in STREET_SQUARE at night | lit: >= 45; dark: 10 to 35; the difference between a lit shop and the same shop dark >= 25 | none | 8 shops |
| LIT-02 | no black void in the street view | mean luma of the room-only composite over the glass lights, by day, in STREET_SQUARE, STREET_30 and CLOSE_35 | >= 33 by day; >= 45 at night for the lit shops | none | 8 shops |
| LIT-03 | the empty unit is a pale blank by day, not black | mean luma of the whitewashed glass in STREET_SQUARE by day | >= 150 (4.1's whitewash 214,212,204 under the day light); by night <= 40 | none | empty_unit |
| LIT-04 | Rita's grille at night | the lattice over the window zone: bar 20 x 4, diamond 120, rails 40 x 40 at z 2.50 and 0.70, plane 100 in front of the glass; the lit window seen through it | equal | 5 mm | ritas |
| CAM-01 | the cameras are the named ones | each render's camera against cameras.definitions and the shop's eye and aim | equal | 5 mm; 0.1 degree | 8 shops |

**Self-check** (before anything is built): self_check: 269 pass, 0 fail, 3 reported. Groups: 1 printed: 94 pass 0 fail 0 reported; 2 rule: 28 pass 0 fail 0 reported; 3 photo: 11 pass 0 fail 0 reported; 4 inventory: 11 pass 0 fail 0 reported; 5 room: 55 pass 0 fail 3 reported; 6 display: 18 pass 0 fail 0 reported; 7 consistency: 52 pass 0 fail 0 reported. Negative controls: 13 of 13 mutations of target.json make it fail (controls.py): a counter 2.4 m out, a 0.40 deep side unit, a denied chair, the door's glass back at 600, a display item outside the window, a reworded camera rule, a card 0.1 m off, a changed hour, a brand in lettering, a drink word, a dark shop marked lit, a 2048-wide picture, a good on a missing fixture.

## 11. What the target could not settle

- The fish, crab and prawn scans, and the grocer's cabbage, potato, satsuma and pear: CC0 (Sketchfab, ffishAsia, checked today) but downloadable only with Jafar's login (the API answers 401). Until he gives it the fishmonger's slab and ice and trays are built and the fish row is marked 'goods pending'; the fishmonger cannot pass the CLOSE review without them. Named plainly: a failed capability of the cloud, not a plan to dress the window another way.
- No 1975 to 1995 photograph of a pawnbroker's or a launderette's window or room was reached (Geograph's categories start in 2005 and 2006; Commons returned a 1968 launderette with children in frame, not used). Rita's display and room stay on the project's earlier sources (Marshall's Hull photographs, the Black Country museum, as links); the launderette rests on the research's text and one 2009 front (P5).
- Only thumbnails of the Poly Haven models were looked at. Maker marks seen at that size: wall_clock, digital_wrist_watch, Television_01, vintage_lighter, measuring_tape_01, Camera_01, the portable cassette player, plastic_crate_01, lubricant_spray and others; the list says what was dropped and what is blanked. The gate's first check is a look at every model's 1k maps by eye.
- The T1 door numbers (D1) rest on one photograph of one door, scaled by assuming a 2040 leaf; the door bell is Judgement (no photograph of one was reached). Both are narrow points a reviewer can overturn with a better photograph.
- The hours of the grocer, ironmonger and chandler were not found; they are settled from the Shops Act (a Judgement). The street's lit list lights three shops that the hours (or, for the grocer and chandler, the Judgement from the Shops Act) say are shut by dusk in winter: the newsagent (17:30), the grocer and the chandler; kept as the street file has it; the town should say which is right.
- Hal's shop (hook-cast.json, the coin shop, street x 39) stands inside the newsagent's bay (x 36 to 42): not resolved.
- Canon names no count of twelve shops: the street has ten units as built; 'twelve' and 'the other eleven' are the superseded atlas proposal's words.
- The picture's box floor is the card's bottom edge, 0.55 above the shop's real floor, which the stallriser hides from the street: the room reads as a stage whose floor is the window bed carried back. A truer floor needs a taller card, which terrace-front.py fixes at 0.65 to 3.05.
- The display can be only 0.55 m deep (the card stands 0.61 m behind the glass): the tea room's table and chairs and the launderette's baskets are tight. Moving the card back to the scene file's 1.2 m would give a deeper real zone; the brief fixes the card.
- The game's glass, Lumen's light on the display, the card's motion vectors under TSR, the exposure and the frame time cannot be shown from the cloud; they stay owed on the PC.
- Scripted goods with no CC0 model that may not pass the CLOSE review at the first try and are set aside under the two-tries rule: tomatoes, sweet jars, folded towels, newspapers and magazines, fish fillets. Each is named in `scripted`.

**Needs Jafar (at most three, one line each, recommended first):**

- May the builder have one Sketchfab login (a token, read-only, never in the repository) to download about fifteen CC0 scans (ten kinds: cod, mackerel, herring, flounder, crab, prawn, cabbage, potato, satsuma, pear)? Recommended: Yes. Why: without them the fishmonger and the grocer's produce cannot pass the close view; all are on the allowlist ('Sketchfab CC0 filter') and cost nothing.
- Timber shop doors: glass from 871 mm above the pavement (the Worcester photograph) or 600 mm (the earlier target, from a restored arcade)? Recommended: 871 (the photograph). Why: photographs win; the 8 October door review failed on exactly such details.
- At night, light the units the street file lights (newsagent, grocer, chandler, tea room, Rita's, Mickey's after the key), or only those open late (tea room to 22:00, Rita's by ruling)? Recommended: keep the street file's six. Why: RULINGS 1 Oct asks for lit windows with darkness between; the hours are a research note.

## 12. Previews

Reduced JPEGs in production/previews/cloud-week/refs/shop-windows/ (at most 1200 px, under 300 KB each; credits in section 2): P1 `P1-worcester-fish-front-below-fascia.jpg` and its overlay `P1-worcester-fish-front-target-on-photo.jpg` (the target's door, stallriser, glass-foot and glazing-bar lines at the scale fitted on the leaf's height); P2 `P2-bath-grocer-window-stock.jpg` (the left window and stand only); P3 `P3-pinner-hardware-newsagent-windows.jpg`; P4 `P4-hull-chandler-front-mesh.jpg` (the firm's name and plaque masked grey); P5 `P5-launderette-front-type-2009.jpg`; P6 `P6-kames-unlet-shop-1995.jpg`; D1 `D1-ritas-front.jpg`, D2 `D2-ten-fronts-sheet.jpg`, D3 `D3-ritas-room-plan-picture.jpg`, D4 `D4-standoff-and-cameras.jpg` (drawn from target.json).

