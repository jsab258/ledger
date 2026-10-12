Shop windows: ten units as built (twelve not found); eight rooms of 104 checked CC0 models and 51 named scripted forms, rendered 4096 wide to the game's own `trace` rule, stock only where that rule can show it and the near 0.55 m a real display; the fish scans wait on one login.

# Shop windows of Quay Street: the exact target

**Status: fixes applied, not re-reviewed.** The fresh review of 12 October (TARGET-REVIEW.md: 3 faults, 15 narrow points) failed this target; every exact amendment is applied here and in `target.json`, the author scripts, the self-check and the previews. By Jafar's rule of 11 October (no more polishing of targets) it is not reviewed a second time: the build's gate holds it to the checks in section 10.

Cloud week 42, part 2, unit 7 (12 October 2026). Written by the target writer from sources reached that day; nothing is built and nothing is committed. Every number below is in `target.json`; the checks that follow from it are its `checks` list and its `self_check` (self_check: 381 pass, 0 fail, 3 reported; 33 of 33 negative controls caught).

## 0. Files, and how to read them

| file | what it is |
|---|---|
| TARGET.md | this page (made by make_doc.py from target.json) |
| target.json | the ten shops (front, door, glass, fascia, room, display, lights, pictures, cameras), the method's numbers, the inventory, the spec entries, the checks, the self-check |
| target_drawing.py | draws target.json alone: each bay's elevation, each room's plan, back wall and picture layout, the ten fronts' sheet, and the elevation laid on the main photograph |
| self_check.py, controls.py | tests the target against its sources (384 rows; it writes nothing unless --write) and shows the self-check can fail (33 mutations of target.json, every one caught) |
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

Only sources reached on 12 October are used. Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model; each preview is cropped to the craft, with every person, real firm's name, number and drink merchant's sign cropped away or masked grey (exactly what is masked in each preview is in section 12; the masks are drawn on every rebuild and read back from the JPEG). No NoAI source.

| id | what | URL | read | author | licence | taken | shows | used |
|---|---|---|---|---|---|---|---|---|
| P1 | A fishmonger's front, Worcester (a Geograph photograph; the page's title names the real firm, which this target does not repeat): an old shop front left as it was: divided timber lights, a black-tiled stallriser, a half-glazed timber door, the slab visible through the glass | https://www.geograph.org.uk/photo/2192169 | 2026-10-12 | Helen Iwanczuk | CC BY-SA 2.0 | May 2000 (the page: 'taken May 2000') | the front a fish shop kept for decades (the author: the premises 'remained in this condition'): door leaf 335 px high by 140 wide (0.42), glass foot 0.413 of the leaf, two panes divided by a bar at 0.685, a letter plate at 0.32, stallriser tiled to 0.28 of the leaf, the window slab and the room dark behind reflections [a period object: a later photograph of a front unchanged since before 1990 (the page says so); 2000 is the earliest dated photograph of a fish-shop window reached] | measured (photo_measurements.json), cropped below the fascia for the preview with the door's number plate and two window stickers masked grey, the main photograph of the self-check's overlay |
| P2 | A grocer's shop, Bath Road (a Geograph photograph, March 1999; the page names the real firm, which this target does not repeat): an open-fronted stock window, tiered stands, goods stacked to the glass, the shop's back shelves visible | https://www.geograph.org.uk/photo/2184467 | 2026-10-12 | Helen Iwanczuk | CC BY-SA 2.0 | March 1999 | density of a grocer's window and the depth of its stock (tins, jars, crates on tiered timber stands); a person stands at the door (masked in the preview) [a long-established shop (the page: established 1898); 1999 shows a 1990 window] | yes: the tiered stand and the density in the grocer's display; preview cropped to the left window and stand (the shop door, with a person at it, and the right-hand shelves are outside the crop) |
| P3 | Shops in Cannon Lane, Pinner (Geograph): a hardware store's and a newsagent's windows, one lit and readable, one dark | https://www.geograph.org.uk/photo/5945841 (and 3403654, the same parade) | 2026-10-12 | Carl Grove | CC BY-SA 2.0 | 20 February 1989 | a 1989 high-street parade: the hardware window's dark interior with stock to the ceiling behind reflections; the newsagent's lit interior with racks; deep recessed doors; cars of 1989 [a photograph of the period itself] | yes: the black-void question (the glass is mostly reflection by day, the room dim; a lit shop reads); preview cropped to the two windows below their fascias (the parade's other signs, a drink merchant's, are outside the crop) |
| P4 | A ship chandler's shut shopfront, High Street, Hull (Geograph): green timber front, lower lights screened inside with woven galvanised mesh | https://www.geograph.org.uk/photo/3378991 | 2026-10-12 | Bernard Sharp | CC BY-SA 2.0 | 1 January 1983 (the feed's date; the page says taken before redevelopment) | the chandler's front: three tall lights, mullions in green, mesh screens over the lower lights, a plaque on the door post [a photograph of the period itself] | yes: the night mesh screens (chandler), the green; preview cropped below the fascia with the door-post board, the glass lettering and a red sign masked grey (a real firm's name) |
| P5 | Launderette in Hambledon Parade (Geograph): a 1960s-80s aluminium-framed launderette front with a script fascia and a striped blind, the room dark behind the glass | https://www.geograph.org.uk/photo/1633924 | 2026-10-12 | Basher Eyre | CC BY-SA 2.0 | 26 December 2009 | the type of front (full-height glazing, glazed door, machines faintly seen); LATER than 1995: used only for the type and for what a launderette window does by day [a later photograph; the front's pattern is the 1970s-80s one (not dated by the author)] | as a type reference only; preview cropped to the front |
| P6 | A derelict grocer and draper's shop, Kames (Geograph): glass dark or blank, paint gone, a pillar box at the kerb | https://www.geograph.org.uk/photo/27024 | 2026-10-12 | Andrew Longton | CC BY-SA 2.0 | 24 May 1995 | an unlet shop in 1995: the glass reads grey-blue and blank, not black; no whitewash [a photograph of the period itself] | for the empty unit's glass: it must read as a pale blank, not a black hole; preview cropped below the eaves with the old fascia band (the firm's name and trades) and the neighbouring shop's board masked grey (disagreement D10) |
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

**Lights per state, for every room** (each shop's own tubes are in its `room.lights`): day = an overcast area light the size of the card on its plane (6500 K, strength set so the picture's mean matches the standard) plus the battens on (the shop is open); night_lit = the battens only, cool white 4000 K, 5 ft T12, 38 mm (about 12 kcd/m2 on the tube: DRESSING note), no sky; night_dark = a faint sodium wash through the front (linear (1.0, 0.25, 0.0): the game's `lantern_linear_rgb` in production/specs/unreal-look.json; the scene file's (1, 0.7055, 0) is stale, QUEUE.md 9 Oct 12:10; 6 per cent of night_lit's energy) and one small practical so the room is not black. Windows are not lit by a second picture's worth of tungsten: the pawnbroker's display spots (2700 K) are the display's, not the picture's.

**The review cameras** (street frame, metres; eye 1.70 above the crown = 1.60 above the footway; 2560 x 1440). STREET_SQUARE: on the far pavement's kerb edge (the brief's 'about 8 m' is 8.76 m to the glass, the nearest the far pavement allows), square to the window's centre, vertical field 39 degrees. STREET_30: the same distance, 30 degrees off the normal toward the quay end (low street x), 39 degrees. CLOSE_35: on the shop's own pavement 1.5 m from the glass, 35 degrees off the normal toward the quay end, aimed at the display's middle (z 1.45), vertical field 60 degrees (the vignette camera's). CLOSE_35_B: CLOSE_35 moved 2.0 m along the street, for the parallax test. By day and by night (night_lit for the lit shops, night_dark for the dark). Every shop's eye and aim are in `shops[].cameras`.

**The gate in the cloud, which has no Unreal.** The builder shows what the game will show without Unreal: the shop's front is assembled in Blender from the 3.2 parts (and the door and lobby of this target), the display's real meshes stand in front of the card where the display is, and the card is a flat quad with an emission picture computed PER CAMERA by tools/ue/make_interior_material.py's `trace` (the Python function, imported, not rewritten): for every pixel of the card the card point and the eye go through `trace` and the picture is sampled at the returned (u, v), bilinear with mips, times the state's brightness (day 0.15, night 0.7). That picture is baked to an image for the camera and set as the card's emission in Cycles, so what is judged is the game's rule pixel for pixel; the glass is the game's job and is left out (a clear 6 mm pane with no reflection) or drawn at the game's day value only if the review asks. What it cannot show: the game's glass reflections, Lumen's light on the display, the card's motion vectors under TSR, the exposure: those stay owed on the PC.

## 4. Rita's shop in full (the pawnbroker; east_parade bay 2, x 15 to 21; the model, RULINGS 2 Oct)

**What it keeps and what it changes.** Keeps: the room's box and finishes (old brown lino, cream plaster over a 1.0 m brown dado, three T12 battens), the stocked back wall, the ticketed goods, the notices, the three approved pictures' look, the display glb and its 23 Poly Haven models. Changes: the glass counter 2.4 m out in the room goes to the back wall (it stood 2.1 m off it and smeared); the units down BOTH side walls (0.40 deep, goods 0.4 off the wall) become flat boards (pegboards, clocks, framed pictures and notices over most of each wall); the stock wall is 0.30 deep (the four television sets on 0.35 boards above the counter) and stands clear of the back door; the grandfather clock and the vintage cabinet (0.8 and 0.67 deep) go; the doormat stays flat; pictures 4096 wide; every model that carries a maker's mark is blanked as its inventory entry says (`marks`).

### 4.1 The front, from the 3.2 parts

Rita's front is the 3.2 kit's own (every part built, `shopfront_ritas.glb`, 34,780 triangles, out of git; `python build_shopfront.py` rebuilds it) except the doors, the lobby, the side door's trim and the band above the doors (4.1a), which are this target's and the door family's. Door end: the viewer's LEFT (street high x). Zones across the bay (u, mm): side door 350 to 1294, shop door 1294 to 2300, window 2300 to 5650 (3350 long). Assembly order, bottom to top, then left to right:

1. pilaster (two, mirrored; plinth 600, shaft 290 x 140 proud)
2. stallriser (panel, z 0 to 600, window zone)
3. sill (75 thick, nose 150, window zone)
4. window_frame (T1 3L-9T (3.2 kit departure D6; the 2.2 table said 3L-8T), 3350 mm long, z 600 to 2850)
5. shop door (T1, slot 1006, hinge on the viewer's right)
6. side door F1 from 3.1 (slot 944, hinge on the viewer's right)
7. the band above the doors: transom (z 2400 to 2480) across the door slots, the fanlight under it, three toplights over the shop door, a raised-and-fielded panel over the side door, the head (z 2790 to 2850): `door.fanlight`, `.transom`, `.toplights_over_shop_door`, `.panel_over_side_door`, `.head`
8. console (scroll, two; both present)
9. fascia_board (5410 x 550 x 120 proud, bed mould 40) carrying the 4.1 board ritas_basecolour/height/orm/wear.png
10. cornice (5892 x 150 x 215 deep, broken forward 85 over each console; 12 Oct ruling: 150 mm as built)

| part | built by 3.2? | size and place (mm, 2.2 frame) | paint (sRGB) |
|---|---|---|---|
| pilaster, panel (two, the right one mirrored) | yes | slot 350; plinth z 0 to 600, 180 proud; shaft 290 x 140 proud, z 600 to 2540; capital 310 high to z 2850, top 350 x 175; base ogee 60 high | oxblood 93,46,49 |
| console, scroll (two) | yes | 240 x 205 x 550 (z 2850 to 3400), at u 175 and 5825; the third review's leaf and rolls as built (3.2 D1 to D3) | oxblood |
| fascia board | yes | 5410 x 550 x 120 proud, u 295 to 5705, z 2850 to 3400; cyma bed mould 40 (3.2 D5); carries the 4.1 board | oxblood (board texture: 4.1 ritas) |
| cornice | yes | 5892 x 150 x 215 deep, z 3400 to 3550, broken forward 85 over each console, mitred returns (3.2 D4); 150 mm as built is Jafar's ruling of 12 Oct | oxblood |
| sill | yes | 75 thick, nose 150, z 525 to 600, u 2300 to 5647 (3 short of the plinth) | white joinery 226,224,214 |
| stallriser, panel | yes (three panels) | z 0 to 600, 125 proud, three raised and fielded panels (1002, 1026, 1002) between 80 stiles | oxblood |
| window frame T1 | yes | jambs 50 x 95; seat 25 (z 600 to 625); 3 lights 625 to 2400; transom 2400 to 2480; **nine toplights of 326.9 as built** (3.2 D6: each mullion carried up as a 70 wide bar, two 28 wide bars a light at 390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1; the 2.2 table said eight, unaligned) 2480 to 2790; head 2790 to 2850; mullions 70 wide, front d 92, centres 1121.7 and 2228.3 from the frame's left; glass 6 mm at d 30 to 36, ovolo bead 16 x 12 | white joinery |
| shop door T1 | NO: specified here (4.2) | slot 1006, leaf 900 x 2040 at z 28, frame jambs 50 x 100 running up to the head; fanlight z 2131 to 2400 between the jambs (u 1344 to 2250), three toplights over it (4.1a) | white joinery |
| transom over both door slots | NO: specified here (4.1a) | transom_t1, u 350 to 2300, z 2400 to 2480, meeting the window frame's left jamb | white joinery |
| panel over the side door | NO: specified here (4.1a) | one raised-and-fielded panel, field 844 wide (944 - 2 x 50), z 2480 to 2790, raised_field_edge | white joinery 226,224,214 |
| head across the door slots | NO: specified here (4.1a) | head_section 95 x 60, u 350 to 2300, z 2790 to 2850 | white joinery |
| side door F1 (3.1) | door_F1.glb, yes | slot 944, mirrored (door end left): hinge on the shop-door side, knob on the pier side; head trimmed at z 2400; 24.4 filler strip each side | buttermilk 222,212,184 |
| night grille (4.3) | NO: specified here | see 4.3 | black powder-coat 37,35,34 |

### 4.1a The band above the doors (transom line 2400 to the fascia 2850) and the toplights: the fault the review found

The 3.2 kit built the window only and left the door slots empty on purpose; this target takes the doors on, so it also puts in what stands above them. The numbers are 2.2's (`targets/shopfronts/target.json` `parts.shop_door.dims` and `parts.side_door_slot.dims.above`, at commit dd706f6), resolved per shop from `front.zones_u_mm` and written into each shop's `door` (keys `fanlight`, `transom`, `toplights_over_shop_door`, `panel_over_side_door`, `head`). Rita's, in millimetres in the 2.2 bay frame (u from the viewer's left, z above the footway):

| part | u (mm) | z (mm) | what it is |
|---|---|---|---|
| fanlight | 1344 to 2250 | 2131 to 2400 | one 6 mm pane in a timber ovolo bead, between the shop door frame's jambs (50 face each side of the 1006 slot). The street number 5 goes on it (4.1; see the note below) |
| transom (door slots) | 350 to 2300 | 2400 to 2480 | `transom_t1`, across both door slots, meeting the window frame's left jamb; the window's own transom continues it |
| toplights over the shop door | 1344 to 2250 | 2480 to 2790 | three panes of 283.3 between two 28 wide `toplight_bar_plan` bars at u 1641.3 and 1952.7; glass and beads as the window's toplights; the door frame's jambs run up beside them |
| panel over the side door | 350 to 1294 | 2480 to 2790 | one raised-and-fielded panel, field 844 wide (944 - 2 x 50), `raised_field_edge`, painted white joinery (226, 224, 214) as on the approved front (2.2 gives it 2480 to 2850; here the head takes 2790 to 2850, as the approved front shows) |
| head (door slots) | 350 to 2300 | 2790 to 2850 | the window's `head_section` (95 x 60) carried across the door slots under the fascia |

**On the other nine fronts** the same, mirrored where the door end is the viewer's right (the band runs from the window frame's right jamb to the pilaster); the metal fronts (M1: Mickey's, the fish market, the laundry and the chandler; M2: the grocer) take their own variant's transom section (`transom_m1`, a 50 high box carrying a 30 mm cover plate to keep 2.2's 80 high band: Judgement) and 2.2's numbers for their doors' tops; the grocer has no side door and so no panel; the newsagent's roller-shutter hood (u 350 to 4706, z 2550 to 2850) cuts the toplights, bars and head away behind it and leaves 70 of the toplights showing. **FRN-07 (no opening in the front):** on the elevation drawn from `target.json` (D1 and D2), every point between the pilasters' inner edges (u 350 to 5650) from z 0 to 2850 lies on a part; the largest uncovered rectangle is at most 5 x 5 mm. Computed here, per shop (width x height, mm):

| shop | glazing pattern | window toplights | 28 wide toplight bars (u from the frame's left) | mullions carried up as bars (centres) | over the shop door | largest open rectangle |
|---|---|---|---|---|---|---|
| mickeys | 3L-3T-aligned | 3 of 1050.0 | none (the mullions carry up) | 1125.0, 2225.0 (50 wide) | 3 of 268.7 | 0.0 x 0.0 |
| fish_market | 4L-4T-aligned | 4 of 775.0 | none (the mullions carry up) | 850.0, 1675.0, 2500.0 (50 wide) | 3 of 268.7 | 0.0 x 0.0 |
| ritas | 3L-9T | 9 of 326.9 | 390.9, 745.8, 1497.6, 1852.4, 2604.2, 2959.1 | 1121.7, 2228.3 (70 wide) | 3 of 283.3 | 0.0 x 0.0 |
| empty_unit | 3L-9T | 9 of 324.7 | 388.7, 741.3, 1498.7, 1851.3, 2608.7, 2961.3 | 1120.0, 2230.0 (80 wide) | 3 of 283.3 | 0.0 x 0.0 |
| steam_laundry | 2L-2T-aligned | 2 of 1600.0 | none (the mullions carry up) | 1675.0 (50 wide) | 3 of 268.7 | 0.0 x 0.0 |
| grocer | 3L-6T-sunrise | 6 of 683.0 | 725.0, 2147.0, 3569.0 | 1436.0, 2858.0 (28 wide) | 3 of 283.3 | 0.0 x 0.0 |
| chandler | 3L-3T-aligned | 3 of 1050.0 | none (the mullions carry up) | 1125.0, 2225.0 (50 wide) | 3 of 268.7 | 0.0 x 0.0 |
| tea_rooms | 3L-6T | 6 of 504.4 | 568.4, 1675.0, 2781.7 | 1121.7, 2228.3 (70 wide) | 3 of 283.3 | 0.0 x 0.0 |
| ironmonger | 2L-6T | 6 of 509.7 | 573.7, 1111.3, 2238.7, 2776.3 | 1675.0 (80 wide) | 3 of 283.3 | 0.0 x 0.0 |
| newsagent | 3L-9T | 9 of 326.9 | 390.9, 745.8, 1497.6, 1852.4, 2604.2, 2959.1 | 1121.7, 2228.3 (70 wide) | 3 of 283.3 | 0.0 x 0.0 |

**The toplight rule (3.2 street review fault 1, kit departure D6), now on every front:** each mullion is carried up through the toplight row as a bar of its own width, and each light's toplight is split equally by 28 wide bars. 2.2's table (a fixed pitch of bars, slivers of 91 to 95 mm beside the mullions on five fronts, the grocer's 256 mm panes beside both mullions, the launderette's one long pane) is replaced; the launderette's divided upper lights are P5's (disagreement D11); the grocer's sunrise is etched one to a light across its two toplights (Judgement). FRN-04 checks the bar centres (+-2 mm), a bar on every mullion line, equal widths in a light and no toplight under 250, not only the count. (The kit's D6 and the review list the second light's second bar of Rita's at 1852.5; the rule gives 1852.43, a rounding of 0.07 mm, far inside the check's 2 mm.)

**The street number on the fanlight.** on the SHOP door's fanlight, as the review reads it, at the shop door's centre (street x 19.203), not at 4.1's x (the side door's centre): a move of 4.1's x recorded for its owner; the side door's fanlight carries no number here. 4.1's z 2.18 is in the street frame, metres above the road crown: 2.18 above the crown is 2080 above the footway (crown + 0.10 = footway), which is BELOW this fanlight (z 2131 to 2400 above the footway). The number is therefore set in the fanlight: baseline 2200 above the footway, cap 110 (2200 to 2310, centred in the pane) = 2.30 above the crown: Judgement, 0.12 m above 4.1's z.

### 4.2 The shop door, the side door and the bell (the 3.2 kit has none)

The door is **specified from 2.2's JSON (`targets/shopfronts/target.json` at commit dd706f6: `parts.shop_door`, its `variants` T1, M1, M2 and its `profiles`; not built by 3.2)** and changed where a photograph of an untouched timber shop front disagrees (D1: Geograph 2192169, a Worcester fish shop's front, May 2000, scaled on the leaf's height). T1 for Rita's, in millimetres above the footway (the leaf's foot stands at 28 on a terrazzo threshold 25 high):

| member | z (mm) | kind and source |
|---|---|---|
| bottom rail | 28 to 228 | Photo (195 high in the photograph); 2.2 had 230 |
| lower panel, raised and fielded | 241 to 549 | Photo; the 12 mm sticking and the 8 mm bevel as 2.2's raised_field_edge |
| lock rail, carrying the plates | 549 to 871 | Photo: 322 high; **2.2 had the glass starting at 600 (D1 supersedes it)** |
| letter plate 250 x 40, brass | centre 678 | Photo: 0.32 of the leaf; 2.2 had 545; in the lock rail, centred across the leaf |
| lever handle on a 240 x 40 backplate | 1000 (rim latch and escutcheon at 950) | Read (the kit); the photograph's handle sits at 0.42 of the leaf (about 890) and is not adopted because the approved game door's lever (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) stands at about 1050 (D12) |
| glass, two panes | 871 to 1973 | Photo: 6 mm in an ovolo bead 14 x 11; the glass 99.5 px wide = 600 of a leaf 853 wide in the photograph; here the leaf is 900 with stiles 115 |
| glazing bar | centre 1423, 28 wide | Photo: one bar, two panes of about 540 |
| top rail | 1973 to 2068 | Photo: 95 high; 2.2 had 115 |
| kick plate / foot strip | brass 770 x 170 with 8 screws on the lower panel's bottom, a 30 high strip across the foot | Read (the kit); Photo (2.2's P1) |
| hinges | three 100 x 75 butts at 150 / middle / 150 on the window side | Read; the lever is on the viewer's left, the hinge on the right (2.2's game-frame reading of Rita's front) |
| threshold | terrazzo 25 high falling to 12, nose to d 130 | Read (2.2) |
| the bell | inside the leaf's top rail at z 1950 to 2050 | a spring-arm shop bell: a 20 x 3 mm steel strip curved 220 long fixed to the INSIDE face of the leaf's top rail 90 from the hanging stile at z 1950 to 2050, carrying a 70 mm brass bell hung 80 below it; it rings on the door's swing against a fixed clapper on the frame (Judgement: no 1975 to 1995 photograph of a shop-door bell was reached; the part is seen through the door's glass from the street and from the close view) |
| the OPEN / CLOSED sign | inside the glass at z 1500 | the plastic OPEN / CLOSED sign from 4.2 (the paper unit) on the inside of the door's glass at z 1500, hung by a suction cup: closed when the shop is shut; the hours plate (4.1) on the glass beside it |

The side door is the door family's **F1** (3.1: production/assets/cloud-week/door/door_F1.glb), used as 2.2's `parts.side_door_slot` (and its `mapping_from_F1`) places it: slot 944, F1 mirrored where the door end is the viewer's left, its frame's outside face at d 100, trimmed at the shop transom, painted buttermilk (222, 212, 184), letter plate 250 x 40, the bell push the 3.1 fix leaves as a plain oblong. Metal doors (M1 aluminium: full-height glass in a 50 frame, 100 top rail, 170 bottom rail, a 300 chrome D pull and a floor spring; M2 bronze: a bronze kick panel to 600, glass above) are as 2.2 for the shops that have them, with one change: an M1 door's letter plate is centred in the 170 bottom rail at z 113, outside the glass (2.2's 545 stood inside it); the M2 door's plate stays in the kick panel at 545.

### 4.3 The glass, the fascia, the paint and the grille

- **Glass:** one 6 mm plate per light (three lights, nine toplights), no astragal bars (D2: the photographs split; Rita's approved window is single sheets); a pane's reflectance is the game's (M_LedgerGlass, night 0.2 of day), not set here. Nothing lies across the glass but the 4.1 rows (WATCHES, JEWELLERY, LOANS, the number 5), the OPEN sign and the hours plate (GLS-01).
- **Fascia:** the 4.1 board `fascias/ritas/ritas_basecolour.png`, `_height.png`, `_orm.png`, `_wear.png` (5410 x 550 at 1 px/mm), the name RITA'S and PAWNBROKER, the street number 5; the hanging sign is the three balls on a bracket at street x 20.825 (4.1 `ritas_three_balls`). Rebuilt by `make_fascias.py OUTDIR --seed-base 1`.
- **Paint:** oxblood (93, 46, 49) on piers, consoles, board, cornice and stallriser (rough 0.45); gloss white, yellowed (226, 224, 214) on the window, sill and shop door (0.50); buttermilk on the side door; aged brass (160, 120, 55) fittings.
- **The grille at night:** an external lattice grille closed over the window zone from dusk to dawn: flat bars 20 x 4 mm at 45 degrees, the diamond 120 mm across, rivets at every crossing, a 40 x 40 box top rail at the transom (z 2.50 above the crown, 2400 above the footway) and a bottom channel at z 0.70 above the crown (600 above the footway), the plane 100 mm in front of the glass front (street y 5.145), powder black (37, 35, 34) rough 0.45; the window behind it stays lit. By day the lattice is lifted out and stored inside; the 40 x 40 top rail and the bottom channel stay, powder black, with their fixing plates on the pilaster shafts.

### 4.4 The room

|  |  |
|---|---|
| box | W 5.3, H 2.4, D 4.5 m; camera_d 5.3; the card at street z 0.65 to 3.05, y +5.875, x 15.35 to 20.65 |
| floor | Poly Haven old_linoleum_flooring_01, tint (0.62, 0.55, 0.50), 1.2 m tile, worn path darker by hand-painted mask |
| walls | Poly Haven painted_plaster_wall tint (0.95, 0.86, 0.66), 1.5 m tile; dado same plaster tint (0.42, 0.27, 0.17) to z 1.0 m |
| ceiling | plaster off-white (180, 173, 158) |
| lights | day: daylight through the front opening (overcast sky area light 5.3 x 2.4 m on the card plane, 6500 K) PLUS the three battens on: the shop is open (Mon, Tue, Thu to Sat 9 to 17:30, Wed 9 to 13); night_lit: the three T12 battens only (cool white 4000 K, 5 ft, 38 mm), no sky: the window is lit all night (RULINGS 1 Oct); night_dark: a faint sodium wash through the front (linear colour (1.0, 0.25, 0.0): the game's lantern_linear_rgb, production/specs/unreal-look.json; 6 per cent of night_lit's energy) and one back-room night light through the ajar back door (2700 K, 0.3 m wide strip, at x 1.45 to 2.35: the door stands clear of the stock wall); rendered although Rita's is lit, so the spec has all three states |

| fixture | surface | stand-off | extent (x, y, z) | what |
|---|---|---|---|---|
| R-back-stock | back | 0.300 | [-2.6, 1.35]  [0.5, 2.25] | the stock wall: five tiers of 25 mm boards 0.30 deep, filled shoulder to shoulder from the left wall to x 1.35, a ticket on every piece; the lowest two tiers only at the ends, the counter standing in front of the middle; the wall from x 1.35 to the back door's frame (1.45) is plain, the door's frame runs to x 2.40, and the strip x 2.40 to 2.6 is plain wall |
| R-back-tv-tiers | back | 0.350 | [-1.9, 0.9]  [1.35, 2.05] | the two tiers above the counter (z 1.35 and 1.70, x -1.90 to 0.90) are 0.35 deep boards for the four television sets (television_02 is 0.35 deep at its size; 0.35 stays inside the 20 px budget at the card's middle): a named exception to the 0.30 shelf rule |
| R-back-door-boxes | back | 0.300 | [1.45, 2.35]  [2.05, 2.25] | one tier of boxes of stock over the back door only, at z 2.05 to 2.25 (x 1.45 to 2.35), 0.30 deep, a ticket on each |
| R-back-counter | back | 0.600 | [-1.9, 0.9]  [0.0, 1.05] | the staff counter, glass-topped case on a velvet bed, against the wall (0.6 deep, 1.05 high), 2.8 m long; notices on its front |
| R-back-door | back | 0.040 | [1.45, 2.35]  [0.0, 2.0] | a half-glazed painted door to the back room, ajar 0.15 m, 2.0 m high (flat: leaf 40 mm); nothing stands across it below z 2.05 |
| R-left-board | left | 0.080 |  [0.3, 4.2] [0.45, 2.15] | pledge board: pegboard panels and hung boards over the whole left wall (0.3 to 4.2 back, 0.45 to 2.15 up), 0.08 deep: ticketed small goods flat to it, wall clocks and framed pictures; the notices hang on it |
| R-left-notices | left | 0.005 |  [3.0, 3.8] [1.5, 1.9] | the licence card and a handwritten UNREDEEMED PLEDGES FOR SALE card (paper, 3 mm), hung on R-left-board |
| R-right-board | right | 0.080 |  [1.3, 4.2] [0.45, 2.15] | tools hung flat on pegboard panels over the right wall's far part (1.3 to 4.2 back, 0.45 to 2.15 up), 0.08 deep |
| R-right-hung | right | 0.070 |  [0.4, 1.2] [1.2, 2.0] | two ukuleles hung by their heads and an ornate mirror, flat to the wall, at the near end (0.4 to 1.2 back) |
| R-floor-mat | floor | 0.012 | [-2.45, -1.55] [0.15, 0.85] [0.0, 0.012] | a worn door mat (flat) and the lino's own worn path |
| R-ceiling-tubes | ceiling | 0.045 | [-0.75, 0.75] [0.9, 3.1] [2.355, 2.4] | three T12 battens in slim fittings |

| goods (model or scripted form) | n | on | why or note |
|---|---|---|---|
| television_02 | 4 | R-back-tv-tiers | CRT sets on the two tiers above the counter; none elsewhere; mark blanked as `inventory.polyhaven[television_02].marks` says |
| boombox | 3 | R-back-stock | mark blanked as `inventory.polyhaven[boombox].marks` says |
| cassette_player | 3 | R-back-stock | maker's name painted out |
| portable_cassette_player | 4 | R-back-stock | maker's name painted out |
| Camera_01 | 3 | R-back-stock | maker's lettering painted out (lens ring and body plate: inventory marks) |
| vintage_video_camera | 2 | R-back-stock | mark blanked as `inventory.polyhaven[vintage_video_camera].marks` says |
| vintage_binocular | 2 | R-back-stock |  |
| binoculars | 1 | R-back-stock |  |
| mantel_clock_01 | 2 | R-back-stock |  |
| alarm_clock_01 | 3 | R-back-stock |  |
| brass_vase_01 | 2 | R-back-stock |  |
| brass_vase_02 | 1 | R-back-stock |  |
| brass_vase_03 | 2 | R-back-stock |  |
| filmstrip_projector_8mm | 2 | R-back-stock | mark blanked as `inventory.polyhaven[filmstrip_projector_8mm].marks` says |
| metal_toolbox | 2 | R-back-stock |  |
| hand_plane_no4 | 1 | R-back-stock |  |
| cardboard_box_01 | 6 | R-back-stock | the top tier: boxes of stock, a ticket each |
| cardboard_box_01 | 3 | R-back-door-boxes | the one tier over the back door |
| CashRegister_01 | 1 | R-back-counter | the till at the counter's right end, on the glass; mark blanked as `inventory.polyhaven[CashRegister_01].marks` says |
| script:counter_jewellery | 1 | R-back-counter | rings, chains and watches on velvet in the case: Rita's approved scripted jewellery (tori, discs, links), kept as approved |
| pocket_watch | 3 | R-back-counter | mark blanked as `inventory.polyhaven[pocket_watch].marks` says |
| vintage_pocket_watch | 3 | R-back-counter | mark blanked as `inventory.polyhaven[vintage_pocket_watch].marks` says |
| pipe_wrench | 1 | R-right-board | mark blanked as `inventory.polyhaven[pipe_wrench].marks` says |
| cross_pein_hammer | 2 | R-right-board |  |
| handsaw_wood | 2 | R-right-board |  |
| hand_plane_no4 | 1 | R-right-board |  |
| adjustable_wrench | 2 | R-right-board | mark blanked as `inventory.polyhaven[adjustable_wrench].marks` says |
| pliers | 3 | R-right-board |  |
| combination_wrench | 3 | R-right-board |  |
| Ukulele_01 | 2 | R-right-hung | mark blanked as `inventory.polyhaven[Ukulele_01].marks` says |
| ornate_mirror_01 | 1 | R-right-hung |  |
| wall_clock | 1 | R-back-stock | its dial's maker mark painted out (the box under the 12 on the dial map: inventory marks) |
| script:pledge_tickets | 90 | R-left-board | paper tickets 25 x 12 mm with handwritten numbers: texture-printed cards, no model exists |
| wall_clock | 2 | R-left-board | hung flat; dial maker mark painted out |
| hanging_picture_frame_02 | 2 | R-left-board | framed pictures hung flat; the picture replaced with the project's own invented print |

### 4.5 The near metre: the display

**Keeps:** production/assets/shop-displays/pawnbroker-display.glb as built (23 Poly Haven models on a stepped velvet bed, a ticket on each), 3.35 m long, 0.55 deep. **Changes:** drop digital_wrist_watch (a maker's mark, not in the glb's list today: confirm) and any model whose map shows a maker's name after the 1k inspection; add the night grille; pieces are not repeated more than twice (the third review's copy-paste note). Display frame: u from the window zone's viewer-left edge (0 to 3.35 m), v out from the back of the glass (0 to 0.55), w above the bed (the stallriser's top, 0.70 above the crown), at most 1.55 high.

| model | n | zone u0-u1, v0-v1, w0-w1 (m) | note |
|---|---|---|---|
| pocket_watch | 2 | 0.20-0.90, 0.05-0.35, 0.00-0.12 | mark blanked as `inventory.polyhaven[pocket_watch].marks` says |
| vintage_pocket_watch | 2 | 0.90-1.50, 0.05-0.35, 0.00-0.12 | mark blanked as `inventory.polyhaven[vintage_pocket_watch].marks` says |
| Camera_01 | 2 | 0.10-0.90, 0.15-0.50, 0.12-0.40 | mark blanked as `inventory.polyhaven[Camera_01].marks` says |
| vintage_video_camera | 1 | 1.00-1.50, 0.15-0.50, 0.12-0.40 | mark blanked as `inventory.polyhaven[vintage_video_camera].marks` says |
| binoculars | 1 | 1.60-2.10, 0.15-0.50, 0.12-0.40 |  |
| round_spectacles | 1 | 2.20-2.60, 0.05-0.30, 0.12-0.30 |  |
| mantel_clock_01 | 1 | 0.20-0.90, 0.20-0.50, 0.40-0.75 |  |
| alarm_clock_01 | 2 | 1.00-1.90, 0.20-0.50, 0.40-0.75 |  |
| brass_vase_01 | 1 | 2.40-2.80, 0.20-0.50, 0.40-1.10 |  |
| brass_vase_02 | 1 | 2.90-3.20, 0.20-0.50, 0.40-0.95 |  |
| brass_vase_03 | 1 | 0.90-1.20, 0.30-0.50, 0.75-0.95 |  |
| ceramic_vase_01 | 1 | 1.30-1.70, 0.25-0.50, 0.75-1.15 | mark blanked as `inventory.polyhaven[ceramic_vase_01].marks` says |
| ceramic_vase_03 | 1 | 1.80-2.00, 0.25-0.45, 0.75-1.15 |  |
| antique_ceramic_vase_01 | 1 | 2.10-2.70, 0.20-0.50, 0.75-1.20 |  |
| standing_picture_frame_01 | 1 | 0.20-0.50, 0.25-0.40, 0.75-1.00 | mark blanked as `inventory.polyhaven[standing_picture_frame_01].marks` says |
| standing_picture_frame_02 | 1 | 2.80-3.10, 0.25-0.40, 0.75-1.00 | mark blanked as `inventory.polyhaven[standing_picture_frame_02].marks` says |
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

Files `pawnbroker_day.png`, `pawnbroker_night_lit.png`, `pawnbroker_night_dark.png` (4096 x 1855) and `pawnbroker.json` (w 5.3, h 2.4, d 4.5, camera_d 5.3, pixels [4096, 1855]). The spec entry is unchanged except `pixels_wide` 2048 to 4096, the display's `x0`/`x1` (15.45 to 18.8 measured on the street model's glass; 15.35 to 18.7 with the 3.2 front's window zone: a 0.10 m shift the builder takes from whichever front stands) and its `decal`, which goes from `production/art/interiors-2026-09-23/int23_pawn` to `production/art/shop-rooms/pawnbroker_day`. Lit at night (RULINGS 1 Oct): night_lit is the picture the game shows all night; `spill_lumens` 350 and the display's rect light stay as approved.

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
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.clad with parts.pilaster.profiles ['clad_plan', 'plinth_cap_side'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.tile_patterned (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.M1, .profiles ['mullion_m1_plan', 'jamb_m1_plan', 'transom_m1', 'glazing_bead_gasket', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door M1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.steel_refit; alterations.repaint |
| toplights (D6) | 3L-3T-aligned: 3 toplights of 1050.0 in 3 lights; 50 wide bars between a light's toplights at no; each mullion carried up as a bar (centres 1125.0, 2225.0, 50 wide); 2.2 had pattern 3L-3T-aligned (3 toplights, aligned: True) |
| band above the doors (FRN-07) | fanlight u [3750.0, 4656.0] z [2131.0, 2400.0]; transom u [3700.0, 5650.0] z [2400.0, 2480.0]; three toplights of 268.7 over the shop door (bars at 4043.7, 4362.3) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [4706.0, 5650.0] z [2480.0, 2790.0]; head u [3700.0, 5650.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 113 (M1 (aluminium, glazed from 198): the plate is centred in the 170 high bottom rail (z 28 to 198), outside the glass; 2.2's 545 stood inside the glass (narrow point 7 of the review)); hinge on the viewer's left, lever on the right; paint powder_slate; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [62, 75, 87]; console [62, 75, 87]; cornice [62, 75, 87]; fascia_board [62, 75, 87]; stallriser [222, 212, 184]; window_frame [60, 74, 88]; shop_door [60, 74, 88]; side_door [93, 46, 49]; metal [170, 172, 174] |
| glass | 3 lights + 3 toplights, 6 mm plate; lettering rows: ['0632 960418', 'MINICABS · 24 HOURS', '1']; blinds, grilles, shutters: none |
| fascia (4.1) | fascias/mickeys/mickeys_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'MICKEY’S']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 7:00-3:00 (next day); Tue 7:00-3:00 (next day); Wed 7:00-3:00 (next day); Thu 7:00-3:00 (next day); Fri 7:00-3:00 (next day); Sat 7:00-3:00 (next day); Sun 9:00-3:00 (next day) (hook-cast.json areas.mickeys); at night: lit (dark until Tom's key (spec lit_at_start false, lit_at_night true); after the key it is open to 3 am; in vignette-pieces lit_names) |
| room | the real walked room (mickeys-office.json; shop-room.py's mickeys branch; room_3d; the spec's lamps 150 lm, room 180 day and 300 night): not changed by this unit; the projected picture is only its far fallback |

### 5.2 fish_market: fishmonger (Fish Market) (east_parade bay 1, x 9 to 15)

|  |  |
|---|---|
| keeps / changes | Keeps: the research (FISHMONGER-2026-10-03.md, Picture Sheffield t13140 and t13138), the white-tile walls and red quarry floor of the 3 Oct code (shop-room.py 257, 287). Changes: no hand-made fish (the 3 Oct failure): the fish are CC0 scans or the window shows none; the slab and ice are real meshes in the display; the chiller counter goes against the back wall (it smeared as a black panel across the floor); the white slab no longer burns out at night (the room is dark at night). |
| front | Alterations: aluminium_refit, repaint. Variants: pilaster panel, console scroll, cornice timber, stallriser tile_square, window M1 4L-4T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's right. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.panel with parts.pilaster.profiles ['shaft_panel_plan', 'plinth_panel_side_through_stile', 'plinth_panel_side_through_field', 'panel_bead'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.tile_square (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.M1, .profiles ['mullion_m1_plan', 'jamb_m1_plan', 'transom_m1', 'glazing_bead_gasket', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door M1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.aluminium_refit; alterations.repaint |
| toplights (D6) | 4L-4T-aligned: 4 toplights of 775.0 in 4 lights; 50 wide bars between a light's toplights at no; each mullion carried up as a bar (centres 850.0, 1675.0, 2500.0, 50 wide); 2.2 had pattern 4L-4T-aligned (4 toplights, aligned: True) |
| band above the doors (FRN-07) | fanlight u [3750.0, 4656.0] z [2131.0, 2400.0]; transom u [3700.0, 5650.0] z [2400.0, 2480.0]; three toplights of 268.7 over the shop door (bars at 4043.7, 4362.3) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [4706.0, 5650.0] z [2480.0, 2790.0]; head u [3700.0, 5650.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 113 (M1 (aluminium, glazed from 198): the plate is centred in the 170 high bottom rail (z 28 to 198), outside the glass; 2.2's 545 stood inside the glass (narrow point 7 of the review)); hinge on the viewer's left, lever on the right; paint alu_natural; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [196, 202, 206]; console [196, 202, 206]; cornice [196, 202, 206]; fascia_board [196, 202, 206]; stallriser [228, 228, 220]; window_frame [176, 178, 180]; shop_door [176, 178, 180]; side_door [35, 36, 40]; metal [170, 172, 174] |
| glass | 4 lights + 4 toplights, 6 mm plate; lettering rows: ['FRESH DAILY', 'SHELLFISH', 'SMOKED FISH', '3']; blinds, grilles, shutters: a retractable awning's arms and blind rail across the front at the transom, canvas stowed or absent (Photo, P1: two diagonal arms and a black rail at about z 2080, +-40; the arms and the 40 mm rail are Judgement); no grille |
| fascia (4.1) | fascias/fish_market/fish_market_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'FISH MARKET'], ['trade', 'WET FISH'], ['trade', 'SHELLFISH'], ['trade', 'SMOKED']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 7:30-14:00; Tue 7:30-14:00; Wed 7:30-13:00; Thu 7:30-14:00; Fri 7:30-14:00; Sat 7:30-14:00 (hook-cast.json areas.fish_market); at night: dark (vignette-pieces lit_names omits east_parade_interior1; the shop shuts at 14:00) |
| room box | W 5.3, H 2.4, D 4.5; floor: red quarry tile 150 mm, grout 20 mm, wet (roughness 0.12); Poly Haven terracotta_floor_tiles as the base if it reads red enough, else the script's brick shader; walls: white glazed square tile 152 mm, grey grout, soiled (Poly Haven long_white_tiles or square_tiles), to the ceiling; dado same tile; ceiling painted white board (200, 198, 190) |
| contents of the room | F-back-counter (counter, stand-off 0.60): script:enamel_trays x8, script:fish_on_ice x1 // F-back-shelf (shelf_unit, stand-off 0.15): script:tins_and_jars x24 // F-back-hose (wall_mounted, stand-off 0.25): garden_hose_wall_mounted_01 x1 // F-right-clock (flat_hung, stand-off 0.05): wall_clock x1 // F-left-board (flat_board, stand-off 0.03): script:price_board_chalk x1 |
| display (real, 0.55 deep) | keeps: FISHMONGER-2026-10-03.md: a tilted white slab under crushed ice, fish in rows each with a per-lb ticket, white trays, lettering on the glass. Changes: everything in the display is a real mesh in the near metre; no fish is modelled by hand. Items: script:slab_and_ice x1, script:enamel_trays x6, script:fish_on_ice x1, lemon x8, script:price_stakes x14, script:chiller_pad x1 |
| lights | day: daylight through the front opening (overcast area light) plus two 5 ft battens on (open Mon to Sat 7:30 to 14:00, Wed to 13:00). night_lit: not used: the shop is shut after 14:00 and the street file leaves it dark (rendered for completeness: two battens on). night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) through the front (6 per cent) and the chiller's small glow lamp (2700 K) at the counter. Tubes: 2 x 5 ft T12. |
| pictures and spec | fishmonger_{day,night_lit,night_dark}.png 4096 x 1855 + fishmonger.json; spec entry in target.json `spec_entries` (id fishmonger, side +1, card x 9.35 to 14.65, display x 11.300 to 14.650) |

### 5.3 empty_unit: empty unit to let (east_parade bay 3, x 21 to 27)

|  |  |
|---|---|
| keeps / changes | Keeps: everything the street already draws: every pane whitewashed from inside, no interior card (terrace-front.py skips bay 3), the 4.1 letting board and whitewash. Changes: the front only: the unit's bare timber front assembled from the 3.2 parts (left console clipped off, paint gone), the whitewash tile from 4.1. |
| front | Alterations: empty_unit. Variants: pilaster panel, console scroll, cornice timber, stallriser boarded, window T2 3L-9T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.panel with parts.pilaster.profiles ['shaft_panel_plan', 'plinth_panel_side_through_stile', 'plinth_panel_side_through_field', 'panel_bead'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.boarded (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.T2, .profiles ['mullion_t2_plan', 'jamb_t1_plan', 'transom_t1 (2.2 gives no T2 transom)', 'toplight_bar_plan', 'glazing_putty', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door T1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.empty_unit |
| toplights (D6) | 3L-9T: 9 toplights of 324.7 in 3 lights; 28 wide bars between a light's toplights at 388.7, 741.3, 1498.7, 1851.3, 2608.7, 2961.3; each mullion carried up as a bar (centres 1120.0, 2230.0, 80 wide); 2.2 had pattern 3L-8T (8 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [3750.0, 4656.0] z [2131.0, 2400.0]; transom u [3700.0, 5650.0] z [2400.0, 2480.0]; three toplights of 283.3 over the shop door (bars at 4047.3, 4358.7) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [4706.0, 5650.0] z [2480.0, 2790.0]; head u [3700.0, 5650.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678 (T1: Photo, the plate sits 0.32 of the leaf up in a lock rail that runs 549 to 871 above the footway (520 to 843 above the leaf's foot); 2.2 had 545 in a lock rail 490 to 600); hinge on the viewer's left, lever on the right; paint black_door; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [46, 37, 30]; console [46, 37, 30]; cornice [46, 37, 30]; fascia_board [46, 37, 30]; stallriser [46, 37, 30]; window_frame [170, 166, 156]; shop_door [35, 36, 40]; side_door [35, 36, 40]; metal [160, 120, 55] |
| glass | 3 lights + 9 toplights, 6 mm plate; lettering rows: ['', '7']; blinds, grilles, shutters: every pane whitewashed from inside (4.1) |
| fascia (4.1) | fascias/empty_unit/empty_unit_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks []; hanging sign none |
| night furniture | dark; the whitewash tile (glass/empty_unit/window_whitewash, 3250 x 1800 mm) over every pane and the door's glass; no grille |
| hours, lit | none (none: to let); at night: dark (empty; nothing lit) |
| room | none: every pane whitewashed from inside (4.1 `glass/empty_unit/window_whitewash`, 3250 x 1800 mm; the shop door's glass too), no card, no picture; a pale blank by day (LIT-03), dark at night; the letting board and boards as 4.1/4.4 |

### 5.4 steam_laundry: launderette (Steam Laundry) (east_parade bay 4, x 27 to 33)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct decision (a launderette with a service counter: the Steam Laundry), the real-room finding that the dryers and washers must stand against walls. Changes: no slab laundry, no dryer stack standing off the wall: machines stand against the BACK wall only; the side walls carry notices; the near metre is a real display of folded laundry and detergent boxes with fictional labels. |
| front | Alterations: aluminium_refit, box_sign, recessed_lobby, repaint. Variants: pilaster render, console scroll, cornice timber, stallriser tile_square, window M1 2L-2T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's left. Missing from 3.2: pilaster, stallriser, window_frame, shop_door, lobby. Lobby: recessed 300 deep. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.render with parts.pilaster.profiles ['shaft_render_plan', 'plinth_cap_side'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.tile_square (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.M1, .profiles ['mullion_m1_plan', 'jamb_m1_plan', 'transom_m1', 'glazing_bead_gasket', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door M1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); parts.lobby.dims.steam_laundry and parts.lobby.profiles.plan_laundry; alterations.recessed_lobby.numbers.steam_laundry; alterations.aluminium_refit; alterations.box_sign; alterations.recessed_lobby; alterations.repaint |
| toplights (D6) | 2L-2T-aligned: 2 toplights of 1600.0 in 2 lights; 50 wide bars between a light's toplights at no; each mullion carried up as a bar (centres 1675.0, 50 wide); 2.2 had pattern 2L-1T (1 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [1344.0, 2250.0] z [2131.0, 2400.0]; transom u [350.0, 2300.0] z [2400.0, 2480.0]; three toplights of 268.7 over the shop door (bars at 1637.7, 1956.3) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [350.0, 1294.0] z [2480.0, 2790.0]; head u [350.0, 2300.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 113 (M1 (aluminium, glazed from 198): the plate is centred in the 170 high bottom rail (z 28 to 198), outside the glass; 2.2's 545 stood inside the glass (narrow point 7 of the review)); hinge on the viewer's right, lever on the left; paint alu_bronze; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [222, 209, 175]; console [222, 209, 175]; cornice [222, 209, 175]; fascia_board [222, 209, 175]; stallriser [228, 228, 220]; window_frame [84, 68, 53]; shop_door [84, 68, 53]; side_door [74, 48, 34]; metal [170, 172, 174] |
| glass | 2 lights + 2 toplights, 6 mm plate; lettering rows: ['SERVICE WASHES', '9']; blinds, grilles, shutters: none (its lit box sign and hanging box are 4.1's) |
| fascia (4.1) | fascias/steam_laundry/steam_laundry_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm), _emissive.png; name blocks [['name', 'STEAM LAUNDRY'], ['trade', 'LAUNDERETTE'], ['trade', 'SERVICE WASHES'], ['trade', 'DRY CLEANING']]; hanging sign steam_laundry_box |
| night furniture | none |
| hours, lit | Mon 8:00-17:30; Tue 8:00-17:30; Wed 8:00-17:30; Thu 8:00-17:30; Fri 8:00-17:30; Sat 8:00-17:30 (hook-cast.json areas.laundry); at night: dark (vignette-pieces lit_names omits east_parade_interior4; its box sign glows (4.1 emissive) but the room is dark) |
| room box | W 5.3, H 2.4, D 4.5; floor: grey vinyl tile 300 mm with a darker worn path (Poly Haven rubber_tiles tinted grey, or worn_tile_floor); walls: cream emulsion (222, 212, 184) above a white glazed tile dado 1.5 m (Poly Haven long_white_tiles); dado white tile to z 1.5; ceiling white board (205, 203, 196) |
| contents of the room | L-back-washers (machines, stand-off 0.60): script:washing_machine x4 // L-back-dryers (machines, stand-off 0.60): script:tumble_dryer x6 // L-back-shelves (shelf_unit, stand-off 0.30): script:wrapped_parcels x18 // L-right-notices (flat_hung, stand-off 0.05): wall_clock x1 |
| display (real, 0.55 deep) | keeps: SERVICE WASHES lettering on the glass (4.1), the research's folded parcels on shelves. Changes: folded laundry in real towers, two wicker baskets, boxed detergents with the project's fictional labels. Items: script:folded_towels x5, wicker_basket_01 x2, script:laundry_in_basket x2, script:detergent_boxes x10, script:laundry_shelf_board x1, script:paper_card_service_washes x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 8 to 17:30). night_lit: not used by the street file (dark); rendered with the three battens on. night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) and the dryers' two orange 'running' lamps (small, 2000 K, 0.01 m) so the room is not black. Tubes: 3 x 5 ft T12. |
| pictures and spec | launderette_{day,night_lit,night_dark}.png 4096 x 1855 + launderette.json; spec entry in target.json `spec_entries` (id launderette, side +1, card x 27.35 to 32.65, display x 27.350 to 30.700) |

### 5.5 grocer: grocer (east_parade bay 5, x 33 to 39)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct label atlas (production/assets/shop-goods/labels.jpg and .json: 32 fictional products in our OFL fonts) and its tin, packet, jar and bottle shapes. Changes: stock only on the back wall (0.25 deep) and on side shelves 0.10 deep (tins only); the near metre is a real tiered stand of produce and tins with scanned fruit; the printed tiles are on bevelled shapes, never plain blocks; the lobby's 0.6 recess takes nothing from the room. |
| front | Alterations: refit_1930s, recessed_lobby, repaint. Variants: pilaster render, console block, cornice timber, stallriser slab, window M2 3L-6T-sunrise (4294 mm long), shop door M2, side door none (the flat is reached from the rear yard). Door end the viewer's left. Missing from 3.2: pilaster, console, stallriser, window_frame, shop_door, lobby. Lobby: recessed 600 deep. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.render with parts.pilaster.profiles ['shaft_render_plan', 'plinth_cap_side'] and base_ogee, capital_side; parts.console.variants.block; parts.stallriser.variants.slab (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.M2, .profiles ['bar_m2_plan', 'transom_m1 (the only metal transom in 2.2: Judgement)', 'glazing_bead_gasket', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door M2); parts.lobby.dims.grocer and parts.lobby.profiles.plan_grocer; alterations.recessed_lobby.numbers.grocer; alterations.refit_1930s; alterations.recessed_lobby; alterations.repaint |
| toplights (D6) | 3L-6T-sunrise: 6 toplights of 683.0 in 3 lights; 28 wide bars between a light's toplights at 725.0, 2147.0, 3569.0; each mullion carried up as a bar (centres 1436.0, 2858.0, 28 wide); 2.2 had pattern 3L-5T-sunrise (5 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [400.0, 1306.0] z [2131.0, 2400.0]; transom u [350.0, 1356.0] z [2400.0, 2480.0]; three toplights of 283.3 over the shop door (bars at 697.3, 1008.7) z [2480.0, 2790.0]; panel over the side door: none (no side door); head u [350.0, 1356.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door None; shop door [350.0, 1356.0]; window [1356.0, 5650.0] |
| door | M2 leaf 900 x 2040; glass foot 600; letter plate z 545 (M2 (bronze, glazed from 600): the plate sits in the bronze kick panel (z 28 to 600), centred at 545 as 2.2, below the glass); hinge on the viewer's right, lever on the left; paint bronze_plate; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [222, 209, 175]; console [222, 209, 175]; cornice [222, 209, 175]; fascia_board [36, 61, 49]; stallriser [36, 61, 49]; window_frame [110, 86, 50]; shop_door [110, 86, 50]; metal [170, 172, 174] |
| glass | 3 lights + 6 toplights, 6 mm plate; lettering rows: ['11']; blinds, grilles, shutters: none |
| fascia (4.1) | fascias/grocer/grocer_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'FAMILY GROCER'], ['trade', 'HIGH CLASS PROVISIONS']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 8:00-17:30; Tue 8:00-17:30; Wed 8:00-13:00; Thu 8:00-17:30; Fri 8:00-17:30; Sat 8:00-17:30 (Judgement from the Shops Act (shop-hours-1990 NOTE): not found for the grocer); at night: lit (vignette-pieces lit_names east_parade_interior5 (practicals chosen so the parade is not a shopping centre; the hours say it is shut: a conflict, kept as the street file has it)) |
| room box | W 5.3, H 2.4, D 4.5; floor: brown linoleum (Poly Haven linoleum_brown); walls: cream (222, 209, 175) emulsion; dado bottle green (36, 61, 49) to z 1.1; ceiling cream plaster (196, 188, 168) |
| contents of the room | G-back-gantry (shelf_unit, stand-off 0.25): script:tins x160, script:packets x90, plastic_crate_02 x3, wicker_basket_01 x2, hamburger_buns x3, wall_clock x1 // G-back-shelves-right (shelf_unit, stand-off 0.20): script:jars x24, script:bottles x12 // G-back-counter (counter, stand-off 0.60): CashRegister_01 x1, script:counter_scale x1 // G-left-tins (shelf_unit, stand-off 0.10): script:tins x40 // G-right-tins (shelf_unit, stand-off 0.10): script:packets x30 |
| display (real, 0.55 deep) | keeps: the 1930s refit's deep lobby; the research's crate-and-stand dressing; the Bath grocer's photograph P2 (Geograph 2184467, 1999) for density. Changes: produce is scanned (Poly Haven apple, banana, lemon, onion; Sketchfab ffishAsia CC0 cabbage, potato, satsuma, pear by his login); tins and jars carry atlas labels. Items: script:tiered_stand x1, plastic_crate_02 x3, plastic_crate_03 x2, food_apple_01 x40, lemon x12, yellow_onion x15, bananas x3, script:cabbage_potato_satsuma x1, script:tomatoes x30, script:tin_pyramids x3, script:jars x18, wicker_basket_02 x1, hamburger_buns x2, script:price_cards x14 |
| lights | day: daylight through the front opening plus three battens on (hours not found: settled as Mon to Sat 8 to 17:30, early closing Wed 13:00, Shops Act). night_lit: the three battens on and a pendant opal globe in the lobby (2700 K, 60 W): the street file lights this unit (east_parade_interior5). night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) and the till's glow lamp. Tubes: 3 x 5 ft T12. |
| pictures and spec | grocer_{day,night_lit,night_dark}.png 4096 x 1855 + grocer.json; spec entry in target.json `spec_entries` (id grocer, side +1, card x 33.35 to 38.65, display x 33.350 to 37.644) |

### 5.6 chandler: ship's chandler (east_chandler bay 0, x 40 to 46)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct trade list (buoys, lifebuoy, life jacket, lanterns, boots, oil, crates) and the CC0 set in fetch_polyhaven.py. Changes: NO explosives-marked drum (Barrel_01 is out); the buoy stands flat against the back wall at a scaled height; nothing hangs from the ceiling; rope is twisted by script with ambientCG Rope textures (no CC0 model): coils stand on shelves. |
| front | Alterations: aluminium_refit, repaint. Variants: pilaster panel, console scroll, cornice timber, stallriser tile_square, window M1 3L-3T-aligned (3350 mm long), shop door M1, side door F1. Door end the viewer's left. Missing from 3.2: stallriser, window_frame, shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.panel with parts.pilaster.profiles ['shaft_panel_plan', 'plinth_panel_side_through_stile', 'plinth_panel_side_through_field', 'panel_bead'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.tile_square (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.M1, .profiles ['mullion_m1_plan', 'jamb_m1_plan', 'transom_m1', 'glazing_bead_gasket', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door M1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.aluminium_refit; alterations.repaint |
| toplights (D6) | 3L-3T-aligned: 3 toplights of 1050.0 in 3 lights; 50 wide bars between a light's toplights at no; each mullion carried up as a bar (centres 1125.0, 2225.0, 50 wide); 2.2 had pattern 3L-3T-aligned (3 toplights, aligned: True) |
| band above the doors (FRN-07) | fanlight u [1344.0, 2250.0] z [2131.0, 2400.0]; transom u [350.0, 2300.0] z [2400.0, 2480.0]; three toplights of 268.7 over the shop door (bars at 1637.7, 1956.3) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [350.0, 1294.0] z [2480.0, 2790.0]; head u [350.0, 2300.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | M1 leaf 900 x 2040; glass foot 198; letter plate z 113 (M1 (aluminium, glazed from 198): the plate is centred in the 170 high bottom rail (z 28 to 198), outside the glass; 2.2's 545 stood inside the glass (narrow point 7 of the review)); hinge on the viewer's right, lever on the left; paint alu_natural; the bell and the OPEN / CLOSED sign as 4.2 |
| paint (sRGB) | pilaster [44, 53, 83]; console [44, 53, 83]; cornice [44, 53, 83]; fascia_board [44, 53, 83]; stallriser [170, 190, 172]; window_frame [176, 178, 180]; shop_door [176, 178, 180]; side_door [44, 53, 83]; metal [170, 172, 174] |
| glass | 3 lights + 3 toplights, 6 mm plate; lettering rows: ['EST. 1879', '13']; blinds, grilles, shutters: woven galvanised mesh screens inside the lower lights when shut (Photo, P4): three panels, wire 2 mm, mesh 12 mm, z 0.70 to 1.55 above the crown |
| fascia (4.1) | fascias/chandler/chandler_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'SHIP CHANDLER'], ['trade', 'ROPE · PAINT · CHARTS · TWINE'], ['end', '13'], ['end', '13']]; hanging sign chandler_hanging_board |
| night furniture | woven galvanised mesh screens (wire 2 mm, 12 mm mesh) inside the lower lights (z 0.70 to 1.55 above the crown), three panels, in place when the shop is shut; the lit night view has them out of the lit lights' way (the Hull chandler photograph (P4) shows them over the lower lights only) |
| hours, lit | Mon 8:00-17:00; Tue 8:00-17:00; Wed 8:00-13:00; Thu 8:00-17:00; Fri 8:00-17:00; Sat 8:00-17:00 (Judgement from the Shops Act: not found for the chandler); at night: lit (vignette-pieces lit_names east_chandler_interior0 (the hours say shut by 17:00: kept as the street file has it)) |
| room box | W 5.3, H 2.4, D 4.5; floor: oiled boards (Poly Haven old_wooden_floor_02); walls: cream emulsion (214, 204, 178) with a dark green dado 1.0 m (the Hull chandler photograph's (P4) green); dado (30, 62, 44) to z 1.0; ceiling painted board (192, 186, 168) |
| contents of the room | C-back-shelves (shelf_unit, stand-off 0.30): script:paint_tins x40, oil_tin x5, small_oil_can_01 x4, cleaner_tin_01 x4, rubber_boots x4, signal_flashlight x3, Lantern_01 x4, script:rope_coils x6, script:twine_reels x10 // C-back-counter (counter, stand-off 0.60): CashRegister_01 x1, seadogs_compass x3, Lantern_01 x1 // C-back-hooks (flat_hung, stand-off 0.18): life_jacket x4, lifebuoy x2, script:oilskin_sou_wester x3 // C-right-board (flat_board, stand-off 0.07): script:shackles_blocks x24 // C-left-charts (flat_board, stand-off 0.05): script:chart_posters x6 // C-floor-buoy (free_at_wall, stand-off 0.55): ocean_buoy x1 |
| display (real, 0.55 deep) | keeps: the trade list; the Hull chandler's window P4 (Geograph 3378991, 1983): a chandler's lower lights were screened inside with woven galvanised mesh when shut. Changes: real ropes, lifebuoy, lanterns, boots and tins in the near metre; no ship model, no explosives drum. Items: lifebuoy x1, life_jacket x2, script:rope_coils x5, rubber_boots x3, Lantern_01 x2, wooden_lantern_01 x1, seadogs_compass x2, oil_tin x4, small_oil_can_01 x3, script:paint_tin_pyramid x1, script:oilskin_sou_wester x2, brass_blowtorch x1 |
| lights | day: daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8 to 17, Wed to 13:00, Shops Act). night_lit: two battens on and a hurricane lamp (Lantern_01, 2200 K, lit) on the counter: the street file lights this unit (east_chandler_interior0). night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json). Tubes: 2 x 5 ft T12. |
| pictures and spec | chandler_{day,night_lit,night_dark}.png 4096 x 1855 + chandler.json; spec entry in target.json `spec_entries` (id chandler, side +1, card x 40.35 to 45.65, display x 40.350 to 43.700) |

### 5.7 tea_rooms: tea room (west_north bay 2, x 24 to 30)

|  |  |
|---|---|
| keeps / changes | Keeps: the research (Formica tables, a menu board, a half-height cafe curtain, steamed glass) and the 3 Oct food models (carrot cake, strawberry cake, tea set). Changes: NO Gothic chairs, NO empty frames, NO free tables in the picture (they smeared): tables and chairs are real and only in the window; the room is the counter, hatch and shelves on the back wall and flat boards; the cafe curtain hides the outer lights. |
| front | Alterations: repaint, flat_panel_sign. Variants: pilaster flute, console scroll, cornice timber, stallriser render, window T1 3L-6T (3350 mm long), shop door T1, side door F1. Door end the viewer's left. Missing from 3.2: pilaster, stallriser, window_frame, shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.flute with parts.pilaster.profiles ['shaft_flute_plan', 'plinth_stepped_side'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.render (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.T1, .profiles ['mullion_t1_plan', 'jamb_t1_plan', 'transom_t1', 'toplight_bar_plan', 'glazing_bead_ovolo', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door T1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.repaint; alterations.flat_panel_sign |
| toplights (D6) | 3L-6T: 6 toplights of 504.4 in 3 lights; 28 wide bars between a light's toplights at 568.4, 1675.0, 2781.7; each mullion carried up as a bar (centres 1121.7, 2228.3, 70 wide); 2.2 had pattern 3L-6T (6 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [1344.0, 2250.0] z [2131.0, 2400.0]; transom u [350.0, 2300.0] z [2400.0, 2480.0]; three toplights of 283.3 over the shop door (bars at 1641.3, 1952.7) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [350.0, 1294.0] z [2480.0, 2790.0]; head u [350.0, 2300.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [350.0, 1294.0]; shop door [1294.0, 2300.0]; window [2300.0, 5650.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678 (T1: Photo, the plate sits 0.32 of the leaf up in a lock rail that runs 549 to 871 above the footway (520 to 843 above the leaf's foot); 2.2 had 545 in a lock rail 490 to 600); hinge on the viewer's right, lever on the left; paint door_cream; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [120, 74, 44]; console [120, 74, 44]; cornice [120, 74, 44]; fascia_board [222, 209, 175]; stallriser [120, 74, 44]; window_frame [222, 212, 184]; shop_door [222, 212, 184]; side_door [74, 48, 34]; metal [160, 120, 55] |
| glass | 3 lights + 6 toplights, 6 mm plate; lettering rows: ['14']; blinds, grilles, shutters: a half-height cafe curtain on a brass rod at z 1500 above the footway over the two outer lights (2.2's glazing note; the research) |
| fascia (4.1) | fascias/tea_rooms/tea_rooms_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'Tea Rooms'], ['trade', 'BREAKFASTS, LUNCHES & TEAS']]; hanging sign none |
| night furniture | none |
| hours, lit | Mon 6:30-22:00; Tue 6:30-22:00; Wed 6:30-22:00; Thu 6:30-22:00; Fri 6:30-22:00; Sat 6:30-22:00; Sun 8:00-12:00 (hook-cast.json areas.cafe); at night: lit (vignette-pieces lit_names west_north_interior2; hours-research cafe 6:30 to 22:00) |
| room box | W 5.3, H 2.4, D 4.5; floor: chequered vinyl, cream and brown 300 mm (Poly Haven old_linoleum_flooring_01 tinted, a chequer mask); walls: cream (222, 212, 184); dado brown (120, 74, 44) to z 1.1; ceiling cream board (208, 200, 180) |
| contents of the room | T-back-counter (counter, stand-off 0.55): tea_set_01 x2, carrot_cake x1, strawberry_chocolate_cake x1, hamburger_buns x2, vintage_electric_kettle x1, CashRegister_01 x1, script:cake_dome x1, script:tea_urn x1 // T-back-shelf (shelf_unit, stand-off 0.20): metal_jug x1, script:cups_saucers x24 // T-left-frames (flat_hung, stand-off 0.04): hanging_picture_frame_02 x1, hanging_picture_frame_03 x1, wall_clock x1 // T-right-frames (flat_hung, stand-off 0.04): hanging_picture_frame_01 x1 |
| display (real, 0.55 deep) | keeps: the half-height cafe curtain on a brass rod at z 1.50 above the footway (2.2's tea_rooms glazing note). Changes: the window table set for tea, in real geometry in the middle light (the two outer lights carry the curtain); no chairs or tables anywhere else. Items: round_wooden_table_02 x1, painted_wooden_chair_01 x2, tea_set_01 x1, script:sugar_bowl_menu x1, carrot_cake x1, script:cake_stand x1, strawberry_chocolate_cake x1, potted_plant_04 x1, script:cafe_curtain x2, script:window_card_menu x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 6:30 to 22:00, Sun 8 to 12). night_lit: three battens on, the steam-warm window: the street file lights this unit (west_north_interior2); open to 22:00. night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) and the counter's pilot lamp. Tubes: 3 x 5 ft T12. |
| pictures and spec | tea_room_{day,night_lit,night_dark}.png 4096 x 1855 + tea_room.json; spec entry in target.json `spec_entries` (id tea_room, side -1, card x 24.35 to 29.65, display x 26.300 to 29.650) |

### 5.8 ironmonger: ironmonger (west_north bay 1, x 30 to 36)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct tools and cleaners set (fetch_polyhaven.py ironmonger), the research's drawer wall, the 4.1 hanging board and 'PARAFFIN' on the fascia. Changes: tools hang FLAT on pegboards on the side walls (they stood on side shelves 0.4 off the wall and smeared); modern aerosols and cleaners with real-brand look-alikes are dropped; paint tins are the project's labelled tins; the drawer wall is a flat front. |
| front | Alterations: repaint. Variants: pilaster flute, console scroll, cornice timber, stallriser panel, window T2 2L-6T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: pilaster, stallriser, window_frame, shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.flute with parts.pilaster.profiles ['shaft_flute_plan', 'plinth_stepped_side'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.panel (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.T2, .profiles ['mullion_t2_plan', 'jamb_t1_plan', 'transom_t1 (2.2 gives no T2 transom)', 'toplight_bar_plan', 'glazing_putty', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door T1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.repaint |
| toplights (D6) | 2L-6T: 6 toplights of 509.7 in 2 lights; 28 wide bars between a light's toplights at 573.7, 1111.3, 2238.7, 2776.3; each mullion carried up as a bar (centres 1675.0, 80 wide); 2.2 had pattern 2L-5T (5 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [3750.0, 4656.0] z [2131.0, 2400.0]; transom u [3700.0, 5650.0] z [2400.0, 2480.0]; three toplights of 283.3 over the shop door (bars at 4047.3, 4358.7) z [2480.0, 2790.0]; panel over the side door: one raised-and-fielded panel, field 844 wide, u [4706.0, 5650.0] z [2480.0, 2790.0]; head u [3700.0, 5650.0] z [2790.0, 2850.0] |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678 (T1: Photo, the plate sits 0.32 of the leaf up in a lock rail that runs 549 to 871 above the footway (520 to 843 above the leaf's foot); 2.2 had 545 in a lock rail 490 to 600); hinge on the viewer's left, lever on the right; paint dark_green; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [30, 62, 44]; console [30, 62, 44]; cornice [30, 62, 44]; fascia_board [188, 173, 136]; stallriser [30, 62, 44]; window_frame [30, 62, 44]; shop_door [30, 62, 44]; side_door [35, 36, 40]; metal [160, 120, 55] |
| glass | 2 lights + 6 toplights, 6 mm plate; lettering rows: ['EST. 1884', '16']; blinds, grilles, shutters: none |
| fascia (4.1) | fascias/ironmonger/ironmonger_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm); name blocks [['name', 'IRONMONGER'], ['trade', 'TOOLS &'], ['trade', 'HARDWARE'], ['trade', 'PAINTS &'], ['trade', 'PARAFFIN']]; hanging sign ironmonger_hanging_board |
| night furniture | none |
| hours, lit | Mon 8:30-17:30; Tue 8:30-17:30; Wed 8:30-13:00; Thu 8:30-17:30; Fri 8:30-17:30; Sat 8:30-17:30 (Judgement from the Shops Act: not found for the ironmonger); at night: dark (vignette-pieces lit_names omits west_north_interior1) |
| room box | W 5.3, H 2.4, D 4.5; floor: bare boards, oiled (Poly Haven old_wooden_floor_03); walls: pale green-cream (204, 206, 180); dado dark green (30, 62, 44) to z 1.0; ceiling cream board (200, 192, 172) |
| contents of the room | I-back-drawers (drawer_wall, stand-off 0.10): script:drawer_fronts x60 // I-back-shelves (shelf_unit, stand-off 0.28): script:paint_tins x40, oil_tin x6, small_oil_can_01 x4, cleaner_tin_01 x4, lightbulb_01 x12, watering_can_metal_01 x3, metal_toolbox x2, brass_blowtorch x1, drain_cleaner x3 // I-back-counter (counter, stand-off 0.60): CashRegister_01 x1, measuring_tape_01 x1 // I-left-pegboard (flat_board, stand-off 0.08): adjustable_wrench x2, combination_wrench x3, cross_pein_hammer x2, wooden_hammer_01 x1, pliers x3, tongue_groove_pliers x2, screwdriver x4, screwdrivers_02 x1, flathead_screwdriver x3, handsaw_wood x2, hatchet x1, ratchet_wrench x2, pipe_wrench x1, bolt_cutters_01 x1, crowbar_01 x1 // I-right-pegboard (flat_board, stand-off 0.08): trowel_01 x3, wooden_broom x2, garden_gloves_01 x4, dustpan x2, mousetrap x6 // I-back-floor (free_at_wall, stand-off 0.58): metal_trash_can x1, wooden_ladder x1, cement_bag x3, metal_jerrycan_green x3 |
| display (real, 0.55 deep) | keeps: the 3 Oct idea: tools, cleaners and oils, a watering can, brooms, a blowtorch. Changes: a stack of tin buckets is not in Poly Haven: watering cans and boxes stand for it; every can's label is blanked or the atlas's. Items: script:paint_tin_pyramid x1, watering_can_metal_01 x2, metal_toolbox x2, brass_blowtorch x1, tire_pump x1, sledgehammer_01 x1, garden_gloves_01 x6, trowel_01 x4, oil_tin x4, cleaner_tin_01 x4, lightbulb_01 x12, garden_sprinkler_01 x1, plastic_broom x3, script:price_cards x12 |
| lights | day: daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8:30 to 17:30, Wed to 13:00, Shops Act). night_lit: not used by the street file (dark): two battens on if rendered. night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) only. Tubes: 2 x 5 ft T12. |
| pictures and spec | ironmonger_{day,night_lit,night_dark}.png 4096 x 1855 + ironmonger.json; spec entry in target.json `spec_entries` (id ironmonger, side -1, card x 30.35 to 35.65, display x 30.350 to 33.700) |

### 5.9 newsagent: newsagent and tobacconist (west_north bay 0, x 36 to 42)

|  |  |
|---|---|
| keeps / changes | Keeps: the 3 Oct trade (papers, sweets, cigarettes behind the counter, a pension counter; no pools coupons, no lottery, no drink); Pinner 1989 (Geograph 3403654, 5945841) for the lit shop and the dark glass. Changes: no gold ribbon across the window (a stale card in the engine: the build's check looks for any card in front of the glass); magazines are real thin meshes in the display and flat covers in the room; the cigarette gantry is a back-wall unit 0.12 deep. |
| front | Alterations: repaint, box_sign, roller_shutter. Variants: pilaster panel, console scroll, cornice timber, stallriser panel, window T1 3L-9T (3350 mm long), shop door T1, side door F1. Door end the viewer's right. Missing from 3.2: shop_door. Lobby: flush. |
| built from | `front.build_from`: production/cloud-week/targets/shopfronts/target.json at commit dd706f6 (a script builds the front from this target.json and that one versioned input): parts.pilaster.variants.panel with parts.pilaster.profiles ['shaft_panel_plan', 'plinth_panel_side_through_stile', 'plinth_panel_side_through_field', 'panel_bead'] and base_ogee, capital_side; parts.console.variants.scroll; parts.stallriser.variants.panel (and profiles.panel_bead for panel); parts.window_frame.dims, .variants.T1, .profiles ['mullion_t1_plan', 'jamb_t1_plan', 'transom_t1', 'toplight_bar_plan', 'glazing_bead_ovolo', 'head_section']; parts.shop_door.dims, .variants, .profiles threshold_section, leaf_stile_plan, frame_jamb_plan, raised_field_edge, glazing_bead (door T1); parts.side_door_slot (dims, mapping_from_F1, bay_parts_around_it); alterations.repaint; alterations.box_sign; alterations.roller_shutter |
| toplights (D6) | 3L-9T: 9 toplights of 326.9 in 3 lights; 28 wide bars between a light's toplights at 390.9, 745.8, 1497.6, 1852.4, 2604.2, 2959.1; each mullion carried up as a bar (centres 1121.7, 2228.3, 70 wide); 2.2 had pattern 3L-8T (8 toplights, aligned: False) |
| band above the doors (FRN-07) | fanlight u [3750.0, 4656.0] z [2131.0, 2400.0]; transom u [3700.0, 5650.0] z [2400.0, 2480.0]; three toplights of 283.3 over the shop door (bars at 4047.3, 4358.7) z [2480.0, 2790.0] (visible [2480.0, 2550.0] only: the roller-shutter hood stands over u [350.0, 4706.0], z [2550.0, 2850.0]); panel over the side door: one raised-and-fielded panel, field 844 wide, u [4706.0, 5650.0] z [2480.0, 2790.0]; head u [4706.0, 5650.0] z [2790.0, 2850.0]; the head over the shop door is cut away behind the hood (u [3700.0, 4706.0]) |
| zones across the bay (u, mm) | side door [4706.0, 5650.0]; shop door [3700.0, 4706.0]; window [350.0, 3700.0] |
| door | T1 leaf 900 x 2040; glass foot 871; letter plate z 678 (T1: Photo, the plate sits 0.32 of the leaf up in a lock rail that runs 549 to 871 above the footway (520 to 843 above the leaf's foot); 2.2 had 545 in a lock rail 490 to 600); hinge on the viewer's left, lever on the right; paint dove_grey; the bell and the OPEN / CLOSED sign as 4.2; T1 rails as Rita's |
| paint (sRGB) | pilaster [150, 152, 150]; console [150, 152, 150]; cornice [150, 152, 150]; fascia_board [222, 209, 175]; stallriser [150, 152, 150]; window_frame [226, 224, 214]; shop_door [150, 152, 150]; side_door [24, 38, 78]; metal [160, 120, 55] |
| glass | 3 lights + 9 toplights, 6 mm plate; lettering rows: ['TOBACCONIST & CONFECTIONER', '18']; blinds, grilles, shutters: the roller shutter of 2.2 (hood 300 x 210 deep, rails, 77 mm slats): up by day, down in the shut-up variant |
| fascia (4.1) | fascias/newsagent/newsagent_basecolour.png, _height.png, _orm.png, _wear.png (5410 x 550 at 1 px/mm), _emissive.png; name blocks [['name', 'NEWSAGENT']]; hanging sign none |
| night furniture | the roller shutter (2.2's alterations.roller_shutter) lowered when shut: not used in the lit view |
| hours, lit | Mon 6:00-17:30; Tue 6:00-17:30; Wed 6:00-17:30; Thu 6:00-17:30; Fri 6:00-17:30; Sat 6:00-17:30; Sun 7:00-12:00 (hook-cast.json areas.newsagent); at night: lit (vignette-pieces lit_names west_north_interior0 (the hours say shut at 17:30: kept as the street file has it; the newsagent's box sign is lit by 4.1 anyway)) |
| room box | W 5.3, H 2.4, D 4.5; floor: grey and blue vinyl tile 300 mm (Poly Haven rubber_tiles tinted); walls: white emulsion (226, 224, 214); dado pale grey (150, 152, 150) to z 1.0; ceiling white board (212, 210, 202) |
| contents of the room | N-back-counter (counter, stand-off 0.60): CashRegister_01 x1, script:sweet_jars x10, stationery_supplies x3, office_notepads x4 // N-back-gantry (shelf_unit, stand-off 0.12): script:cigarette_packs x100, cigarette_pack x8 // N-left-racks (flat_board, stand-off 0.04): script:magazine_covers x60 // N-right-racks (flat_board, stand-off 0.04): script:greeting_cards x40, wall_clock x1 |
| display (real, 0.55 deep) | keeps: the 4.2/4.4 window board SB1 (hand cards) on the glass; the sweets, papers and cigarettes trade. Changes: magazines and newspapers are real thin meshes 2 to 4 mm with a curl and a fold; a card rack of fictional cards; no card floats in front of the glass. Items: script:newspapers x10, script:magazines x24, script:sweet_jars x6, script:cigarette_cartons x6, script:card_rack x1, stationery_supplies x2, office_notepads x3, script:postcard_rack x1 |
| lights | day: daylight through the front opening plus three battens on (open Mon to Sat 6 to 17:30, Sun 7 to 12). night_lit: three battens on, the whole shop bright: the street file lights this unit (west_north_interior0); the roller shutter is up. night_dark: a faint sodium wash (linear (1.0, 0.25, 0.0): the game's lantern_linear_rgb, unreal-look.json) through the front; the shutter is down in the shut-up variant (4.1's shutter_down). Tubes: 3 x 5 ft T12. |
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
| the 3.2 kit (production/cloud-week/kit/shopfront) | pilaster (panel), console (scroll), fascia board, cornice (150 as built, 12 Oct), sill, stallriser (panel, three panels), window frame T1 (3 lights, nine toplights as built): Rita's front is complete but for the doors and the band above them | nine variants are missing for the other fronts (front.missing_from_3_2 in each shop; front.build_from names the exact keys of 2.2's target.json, at commit dd706f6, that build each); the doors, the lobbies and the band above the doors are specified here, from that JSON, with three changes (D1, D11, D12) and the bell |
| 2.2 (targets/shopfronts/target.json, at commit dd706f6) | the ten fronts' table, paints, door ends and hinges; its JSON is the second versioned input of every front's build (`front.build_from`) | T1 door: glass foot, lock rail, letter plate, a glazing bar (D1); the bell; the toplight layout on seven fronts (the kit's D6 rule: mullions carried up, each light's toplight split equally); the band above the doors (fanlight, transom, three toplights over the shop door, a panel over the side door, the head) written into every shop's `door`; M1 letter plate in the bottom rail |
| 4.1 (2d/fascias) | the ten boards, the four hanging signs, the glass rows, the whitewash and the letting board, unchanged | none; each shop names its board |
| 4.2 to 4.4 (2d/paper) | the OPEN/CLOSED sign, the newsagent's board SB1, the letting boards | none |
| 3.1 doors | F1 for every side door | none |
| the set-aside branch shops-wip-2026-10-03 (a local branch on the PC, not in this clone) | nothing taken: it was not reachable and its goods were made by hand | replaced; the reason is F1 |

## 8. Photographs win: each disagreement

- **D1, where a timber shop door's glass starts.** Target: 600 (level with the sill; Leadenhall 2019 at 0.304 of the leaf; DOR-06); the approved game door (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) has its glass from about 1000, one pane, no bar. Photograph or research: 871 +-30 above the footway (843 above the leaf's foot: 0.413 of the leaf, Geograph 2192169, a fish shop's untouched front, May 2000); the lock rail runs 549 to 871 with the letter plate in it at 678. Chosen: the photograph: T1 door glass from 871 above the footway (843 above the leaf's foot), the lock rail 549 to 871, the letter plate at 678, one glazing bar at 1423; the aluminium and bronze doors keep 2.2's numbers. Why: Leadenhall is a 2019 heritage restoration of a London arcade; the Worcester front is a working shop in the period's condition and the nearer match; 2.2's DOR-06 (door glass foot = sill top) is replaced for T1 doors only. Flagged for Jafar (Needs you) with three options: 871, 600, about 1000.
- **D2, the glass of the window lights.** Target: one sheet per light, no astragal bars (Rita's approved window). Photograph or research: Geograph 2192169 shows each light divided by one bar at the door's bar height; Pinner 1989 shows single large sheets (hardware) and aluminium-framed sheets (newsagent). Chosen: single sheets per light as 2.2 (Rita's window is the model and approved); the divided pattern is recorded as a possible variant, not adopted. Why: RULINGS 2 Oct; the photographs split
- **D3, the door leaf's width.** Target: 900 in a 1006 slot. Photograph or research: about 853 (140 px of a 335 px leaf) in an older door. Chosen: 900 as 2.2: the slot is fixed by the bay; the photograph is within 6 per cent of it. Why: inside the error
- **D4, the stallriser's height.** Target: 600. Photograph or research: 571 +-18 (94 px of the leaf's 335). Chosen: 600. Why: inside the error (5 per cent)
- **D5, how bright the room reads from the street by day.** Target: the game's day brightness 0.15. Photograph or research: P1 and P3: the glass is mostly reflection, the room dim; only a lit, bright shop (Pinner's newsagent) shows its goods by day. Chosen: the game's 0.15 kept for every shop (the spec's values are the game's). Why: the research (NOTE.md section 3 and 8) and these photographs agree: over-bright day interiors are the commonest giveaway
- **D6, an open-fronted grocer's window.** Target: a glazed window with a 1930s bronze front. Photograph or research: P2 shows stock stood out on stands in an open front. Chosen: glazed, as 2.2. Why: the street's grocer is a 1930s refit with glass; the density and the stands are taken, not the open front
- **D7, mesh over a chandler's lower lights.** Target: none. Photograph or research: P4 shows woven galvanised mesh screens inside the lower lights of a shut chandler's. Chosen: added as the chandler's night furniture (three panels). Why: the photograph shows it
- **D8, the street's lit list against the hours.** Target: vignette-pieces lit_names: 6 units lit at night. Photograph or research: the hours research: everything shut by 8 pm; newsagent 17:30; the grocer, ironmonger and chandler not found. Chosen: the street file's list is kept (RULINGS 1 Oct: lit windows, not one wash); the hours are the town's and are noted. Why: a conflict between two files of the project; not mine to resolve
- **D9, the chandler's paint.** Target: navy on piers, consoles, board and cornice, natural aluminium window. Photograph or research: P4 (Hull, 1983) shows a chandler's front in dark green. Chosen: navy as 2.2 and 4.1 (the street's board is navy); the photograph's green is used for the room's dado. Why: the Hull shop is another shop; the street's colours are fixed by 4.1
- **D10, an unlet shop's glass: whitewashed or not.** Target: 4.1 and Jafar's ruling of 3 October (DECISIONS 3 Oct; 4.1 `glass/empty_unit/window_whitewash`; 2.2 alterations.empty_unit, whitewash coverage 1.0): every pane of the empty unit is whitewashed from inside. Photograph or research: P6 (Kames, 24 May 1995) shows an unlet shop's glass blank and grey-blue with no whitewash at all. Chosen: whitewash, as the ruling. Why: Jafar's ruling of 3 October settles it, and a ruling outranks a photograph; P6 is used only for what the glass reads like (a pale blank, not black: LIT-03)
- **D11, the launderette's toplight: one long pane or divided.** Target: one long toplight pane over both lights (pattern 2L-1T). Photograph or research: P5 (Hambledon Parade, a 2009 photograph of a front of the 1970s to 80s pattern, used as a type reference only) shows the upper lights divided on the lower lights' lines. Chosen: the photograph: the mullion is carried up and the toplight is two panes of 1600 (pattern 2L-2T-aligned), the same rule as every other front (kit departure D6, the 3.2 street review's fault 1). Why: photographs win; P5 is later than 1995 but its pattern is the earlier one, and the rule for the other nine fronts says the same
- **D12, the door lever's height.** Target: 1000 on a 240 x 40 backplate (the kit's). Photograph or research: P1's handle stands at 0.42 of the leaf, about 890 above the footway (a different door: a rim knob, not a lever). Chosen: 1000, the kit's and 2.2's. Why: the approved game door's lever (rita-day-kit-2026-10-06.jpg, the door Jafar has seen) stands at about 1050, so the kit and the game agree against one photograph of one door; a lever 160 mm lower would change a door he has approved

**The main photograph's readings** (P1; the photograph is nearly face-on; every edge was read by eye off a 4x enlargement with a 10-pixel grid (error +-3 px); ONE dimension fits the scale: the door leaf's height, 335 px, taken as the street's 2040 mm (6.09 mm a pixel), so every other number is a ratio of the leaf's height and is Photo only to that assumption (a 2100 leaf would put the glass foot at 896 above the footway: 0.413 x 2100 + 28)):

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
| adjustable_wrench | 6.8x3.1x25.4 | 5390 | 2026-06-30 | ritas, ironmonger |
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
| combination_wrench | 5.7x33.7x2.2 | 1986 | 2026-07-03 | ritas, ironmonger |
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
| hanging_picture_frame_02 | 75.2x3.3x50 | 3678 | 2021-06-15 | ritas, tea_rooms |
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
| pliers | 5.5x1.8x18 | 4540 | 2026-06-20 | ritas, ironmonger |
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
| script:tiered_stand | grocer | a three-tier timber display stand 0.18 high a step (the Bath grocer's photograph, P2), made from dimensions |
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

**Marks on the models' base-colour maps, and how each is blanked (the second fault of the review: the real retailer's name 'Dixons' stood on `cassette_player`).** After the review the writer opened the 1k base-colour map of every one of the 104 models (25 contact sheets at 512 px; the marked ones at 1k with the boxes drawn on them) and found the marks below; thumbnails alone had missed them. Every model carries `marks` in `inventory.polyhaven` (a mark, or none seen at 1k). The step, for every map below: script step (one per listed map, before the model is placed): open the map; for each box, take the fill (the median colour of a 6 px ring just outside the box, the sampled value is given for reference), paint the whole box to it, then copy a same-size patch of the map's own grain from the nearest clean area over it (no flat patch); write <map>_clean.jpg beside it; point the glTF material's baseColorTexture at the clean map. 'Whole label area' means every box listed for that map. The normal and roughness maps are not touched (a print has no relief at 1k).

| model | what is printed on it | map (1k, 1024 x 1024) | boxes [x0, y0, x1, y1] | fill | what the boxes hold |
|---|---|---|---|---|---|
| Camera_01 | a Leica look-alike with the real firm's names: 'LEICA SUMMILUX-M 1:1.4/50 ASPH. E 46 4004490' on the lens ring, 'ERNST LEITZ GMBH WETZLAR GERMANY', 'DEP' and 'M3-785000' on the body plate, a red-and-white emblem on the film-speed dial, 'close - zu / open - auf' on the shutter ring, and a red island on the lens map: maker's lettering painted out | Camera_01_lens_body_diff_1k.jpg | [16, 203, 604, 237]; [828, 88, 1024, 462] | the lens ring's black (sampled 10, 10, 10) | the whole lens-ring engraving line (LEICA SUMMILUX ...) and the red island (a red-dot emblem) |
| Camera_01 | (as above) | Camera_01_body_diff_1k.jpg | [748, 566, 902, 624]; [620, 646, 737, 680]; [398, 196, 460, 258]; [833, 428, 927, 550] | the body leatherette black (sampled 19, 16, 15); the dial emblem to the dial's white | ERNST LEITZ GMBH WETZLAR GERMANY / DEP, M3-785000, the dial's emblem, 'close - zu', 'open - auf' |
| CashRegister_01 | the readout's '$' ('$021.37'), the drawer plate 'TITCH BANKS', a 'TITCH CO.' label, a Canadian banknote, three place badges ('I (heart) LAS VEGAS', 'I (heart) TORONTO', 'I (heart) QUEBEC': a gambling place and two foreign places), and printed receipt slips: the '$' painted out (no '(pound)' is drawn: the readout shows digits only), every name, badge and slip blanked | CashRegister_01_diff_1k.jpg | [468, 227, 486, 248] | the readout panel's dark grey (sampled 52, 52, 52) | the dollar sign in the readout |
| CashRegister_01 | (as above) | CashRegister_01_diff_1k.jpg | [780, 438, 802, 532] | the plate's dark grey (sampled 52, 52, 52) | TITCH BANKS (the plate on the drawer, printed upright on the map) |
| CashRegister_01 | (as above) | CashRegister_01_diff_1k.jpg | [905, 317, 942, 386] | the label paper's grey (sampled 190, 192, 196) | TITCH CO. and its small print |
| CashRegister_01 | (as above) | CashRegister_01_diff_1k.jpg | [195, 338, 232, 380]; [222, 490, 300, 532] | the brass-brown of the surround (sampled 150, 105, 60) for the first, the dark grey (sampled 30, 30, 30) for the second | I (heart) LAS VEGAS; I (heart) TORONTO, I (heart) QUEBEC |
| CashRegister_01 | (as above) | CashRegister_01_diff_1k.jpg | [395, 85, 450, 184]; [778, 165, 862, 238]; [855, 545, 920, 603] | the surrounding dark grey (sampled 52, 52, 52) for the banknote; the slips' paper (sampled 215, 205, 195) for the slips | a Canadian banknote ('CANADA'); printed receipt slips with 'TOTAL' and amounts |
| Ukulele_01 | a 'KOLO' maker's label inside the headstock area | Ukulele_01_diff_1k.jpg | [520, 195, 640, 305] | the wood's brown (sampled 150, 95, 50) | KOLO label |
| adjustable_wrench | a 'STEELBOX TOOLS' diamond logo on the jaw ('DROP FORGED STEEL' is a stamp, not a name, and stays) | adjustable_wrench_diff_1k.jpg | [612, 358, 724, 422] | the steel's mid grey (sampled 120, 120, 118) | STEELBOX TOOLS (diamond) |
| boombox | a maker's plate with 'Tv - Mw/Fm STEREO CASSETTE RECORDER' and a logo at the top left of the map, and three stickers: a cartoon figure playing a guitar (a young person: the children rule), a skull and a cartoon skeleton | boombox_diff_1k.jpg | [0, 100, 320, 230] | the case's dark grey (sampled 52, 52, 52) | the plate's printed legends and logo |
| boombox | (as above) | boombox_diff_1k.jpg | [555, 385, 685, 505]; [740, 515, 830, 635]; [720, 775, 835, 890] | the case's grey (sampled 112, 112, 112) | the guitar-playing cartoon (a child-like figure), the skull, the skeleton |
| cassette_player | red roundel, 'Dixons' and 'TR12 Cassette Recorder' above the cassette window: painted out of the base-colour map to the case's brushed grey; the tape's handwritten label kept | cassette_player_body_diff_1k.jpg | [380, 794, 540, 820] | the case's brushed grey (sampled 151, 152, 151) | a red roundel, the word 'Dixons' and the line 'TR12 Cassette Recorder', printed upside down on the map at the foot of the light-grey panel |
| cement_bag | the bag's print is post-1992: a red logo (an arrow and 'CEMENT' in red), 'CEM I 42,5 R / CEM 42.5 N' (the EN 197-1 designation of 2000), 'EN 197-1', a green panel of modern safety pictograms, a barcode, a maker's name ('SOLIDUS RESOURCES') and a 'CE' mark: all of the print is replaced by a plain stamp | cement_bag_diff_1k.jpg | [60, 138, 618, 566]; [52, 568, 618, 1004]; [662, 398, 924, 994]; [66, 44, 380, 118]; [602, 40, 914, 110] | the kraft paper (sampled 194, 164, 135); the red areas around the panels and in the two top bands are painted to the same kraft colour with a faint warm stain from the map's own luma | every printed panel (back, front, side) and the two red top bands with 'CEMENT' reversed out |
| ceramic_vase_01 | a price label with a barcode stuck on the vase | ceramic_vase_01_diff_1k.jpg | [580, 84, 626, 164] | the glaze's off-white (sampled 232, 230, 224) | a barcode sticker |
| cigarette_pack | the real brand 'Kentucky Ace' with 'PREMIUM FILTERS', 'KING SIZE' and a 'SURGEON GENERAL'S WARNING' (a US pack): the whole map is replaced by the atlas's tobacco tile | cigarette_pack_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: the map is replaced by the atlas tile laid on the pack's net (shape only is kept) | the whole pack |
| cleaner_tin_01 | the 'PolyClean' brand, 'ANTISEPTIC HAND CLEANSER', a price '1'9', a barcode and a flame warning: the whole label area is replaced by the project's atlas tile | cleaner_tin_01_diff_1k.jpg | [0, 0, 372, 490]; [0, 590, 1024, 1024] | the tin's red (sampled 234, 36, 15) for the label band, the lid's white-grey (sampled 200, 200, 196) for the lid | the lid print and the whole red label band |
| drain_cleaner | 'DRAIN UNBLOCKER', hazard text, pictograms and a 'Keep out of reach of children' line: the whole label area is replaced by the project's atlas tile | drain_cleaner_diff_1k.jpg | [0, 636, 152, 1004]; [286, 640, 646, 792] | the tin's yellow (sampled 168, 144, 59) | the two printed labels |
| filmstrip_projector_8mm | a 'SIRIUS steering' label plate (a maker's name) | filmstrip_projector_8mm_diff_1k.jpg | [270, 474, 400, 574] | the plate's cream (sampled 230, 220, 190) | SIRIUS steering |
| garden_gloves_01 | a printed size-and-maker label on the glove | garden_gloves_01_diff_1k.jpg | [172, 690, 286, 770] | the glove's teal (sampled 70, 190, 160) | a printed label ('S.BOX' / size) |
| garden_sprinkler_01 | small print ('Polyplast ...') at the foot of the body map | garden_sprinkler_01_diff_1k.jpg | [30, 960, 210, 996] | the body's yellow (sampled 230, 185, 40) | a maker's line of small print |
| hanging_picture_frame_01 | the artwork map is a placeholder reading 'Ray Homes / Photo: 76cm x 51cm / Frame: 84cm x 59cm' (an artist's name) | hanging_picture_frame_01_artwork_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: the whole artwork map is replaced by one of the project's own invented prints (an oil-painted seascape or flower piece by script) | the placeholder and its credit |
| hanging_picture_frame_02 | the artwork is a painting of a real palace signed 'Celine F.' (an artist's name and a real landmark) | hanging_picture_frame_02_artwork_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: the whole artwork map is replaced by the project's own invented print | the painting and its signature |
| hanging_picture_frame_03 | the artwork is a photograph of a real foreign castle (a landmark: the project's pictures show nothing foreign) | hanging_picture_frame_03_artwork_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: replaced by the project's own invented print | the photograph |
| hatchet | a 'UC' trademark with (R) stamped on the blade | hatchet_diff_1k.jpg | [490, 964, 534, 1010] | the blade's grey (sampled 110, 110, 110) | UC (R) |
| lifebuoy | 'Lighthouse' and 'PH . SA . 20' lettered round the ring: replaced by a made-up vessel name or blanked | lifebuoy_diff_1k.jpg | [780, 190, 962, 402]; [630, 690, 782, 902]; [560, 612, 750, 696] | the ring's red (sampled 163, 50, 50) for the first two, the white band's grey (sampled 190, 190, 190) for the third | 'Lighthouse' (rotated) and 'PH . SA . 20' (rotated), and the lettering that runs on over the white band |
| lightbulb_01 | a 'Lumen' print with a wattage line on the bulb's cap | lightbulb_01_diff_1k.jpg | [90, 110, 230, 200] | the cap's dark grey (sampled 40, 40, 42) | Lumen and its small print |
| measuring_tape_01 | a yellow label '3m / Q-TECH / QC PASSED': makers' names painted out (the label's yellow kept as a plain tape-case sticker) | measuring_tape_01_diff_1k.jpg | [555, 255, 725, 422] | the case's black-grey (sampled 28, 28, 28); a plain 60 x 40 yellow sticker may stand over the middle of the box | 3m, Q-TECH, QC PASSED |
| pipe_wrench | 'SES' and '18' stamped on the handles (a maker's initials) | pipe_wrench_diff_1k.jpg | [40, 100, 100, 175]; [320, 100, 380, 175] | the handle's red-grey (sampled 150, 90, 80) | SES / 18 |
| plastic_broom | a 'MICKY' label on the handle | plastic_broom_diff_1k.jpg | [728, 830, 772, 926] | the handle's cream (sampled 240, 235, 220) | MICKY |
| pocket_watch | the dial reads 'Lorex' (a look-alike of a real watchmaker's name) | pocket_watch_diff_1k.jpg | [220, 132, 294, 170] | the dial's cream (sampled 228, 226, 214) | Lorex |
| portable_cassette_player | 'SDQ' logos and 'SUPER PRECISION RIGID CASSETTE MECHANISM' on the cassette inserts, 'PORTABLE CASSETTE PLAYER' printed along the side, 'pro' on the speaker plate: maker's name painted out | portable_cassette_player_diff_1k.jpg | [45, 515, 345, 695]; [0, 700, 300, 775]; [95, 330, 145, 510]; [735, 765, 760, 815] | the cassette's dark blue-grey (sampled 52, 57, 60) for the first two; the case's grey-blue (sampled 90, 105, 110) for the others | SDQ, SUPER PRECISION RIGID CASSETTE MECHANISM, SIDE A / SIDE B, the side lettering, 'pro' |
| rubber_boots | two small embossed 'MICKY' badges (a maker's logo) on the boot map | rubber_boots_diff_1k.jpg | [446, 48, 502, 74]; [648, 400, 704, 424] | the boot's dark green (sampled 13, 52, 33) | MICKY (two badges) |
| screwdriver | 'LANSTEY' on the handle (a look-alike of a real tool maker) | screwdriver_diff_1k.jpg | [168, 630, 400, 692] | the handle's red-orange (sampled 232, 66, 40) | LANSTEY |
| standing_picture_frame_01 | the artwork is a photograph of a canal street of a foreign city with a parked van | standing_picture_frame_01_artwork_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: replaced by the project's own invented print | the photograph |
| standing_picture_frame_02 | the artwork is a beach photograph with small figures on the sand (no person may be recognisable, and none may be a child: they are 3 to 6 px high but the rule is no persons) | standing_picture_frame_02_artwork_diff_1k.jpg | [0, 0, 1024, 1024] | not a fill: replaced by the project's own invented print | the photograph with its figures |
| stationery_supplies | pencil boxes and pads printed 'Nova Presents HB' and similar (a maker's name) | stationery_supplies_diff_1k.jpg | [0, 20, 840, 420]; [820, 0, 1024, 1024] | each box is painted to the median of its own band (blue, yellow, red, cream): whole label area | the pencil boxes' lettering and the pads' printing |
| television_02 | a rotated model-plate strip on the back/side panel (about 10 px high, unreadable at 1k scale on the screen) | television_02_diff_1k.jpg | [268, 452, 296, 542] | the case's dark brown-grey (sampled 54, 52, 48) | a model number strip |
| tire_pump | 'POLYLUFT' and a round logo on the pump's label plate, and an orange label | tire_pump_diff_1k.jpg | [570, 520, 664, 880]; [800, 20, 900, 100] | the label plate's grey (sampled 150, 150, 150); the dark body grey for the second | POLYLUFT (rotated), the roundel logo, the orange label |
| vintage_lighter | 'TROP(R)' (a trademark) on the case and a logo plate: maker's mark painted out | vintage_lighter_diff_1k.jpg | [60, 452, 295, 522]; [20, 700, 296, 1002] | the brushed brass-grey (sampled 147, 125, 112) | TROP(R), and the engraved logo plate with its triangle emblem |
| vintage_pocket_watch | 'AVVENTURA' lettered on the inner dial (a watch brand name) | vintage_pocket_watch_diff_1k.jpg | [620, 630, 765, 790] | the inner dial's grey (sampled 180, 182, 184) | AVVENTURA (rotated) |
| vintage_video_camera | 'PH JNL 7' and 'PH.JNL - OPTICAL CO., LTD' plates and a red-and-black label (a maker's marks) | vintage_video_camera_diff_1k.jpg | [10, 388, 202, 650]; [28, 808, 192, 932] | the body's dark olive (sampled 60, 62, 50) | PH JNL 7; PH.JNL - OPTICAL CO., LTD; the red and black label |
| wall_clock | 'URBAN quartz' under the 12 on the dial: maker's mark painted out | wall_clock_diff_1k.jpg | [248, 616, 312, 664] | the dial's white (sampled 224, 224, 224) | URBAN / quartz |

**What is kept:** Camera_01: the distance and aperture numerals (no maker), the film-speed numerals; CashRegister_01: the key legends (digits, A, B, R, X, Y, Z) and the receipt roll's plain paper; boombox: the speaker grilles and the cassette door; cassette_player: the tape's own label (cassette_player_tape_orangeblue_diff_1k.jpg: 'Classic Rock Vol. 1', 'HIGH FIDELITY', '90 MINUTES': no maker) and the control legends (Record, Play, Rewind, MIC, VOLUME); cement_bag: nothing of the print; pocket_watch: the numerals; portable_cassette_player: the cassette's window and the control symbols without words; rubber_boots: the sole and the lining; vintage_lighter: the scratches and wear; wall_clock: the numerals and ticks.

**Notes on particular models:** Camera_01: 'leica' and 'leitz' are in brand_blocklist; CashRegister_01: the register stands in six shops (not in Mickey's real room): at the close view its readout is about 3 px high; the rule is applied anyway; cassette_player: the real British high-street retailer's name; 'dixons' is in brand_blocklist; the same model is in the approved recipe's stock (see could_not_settle); cement_bag: then a plain stamp is drawn: the single word 'CEMENT' and '50 kg' in a dark grey sans (the project's OFL font, 70 px tall) centred on the front panel [52, 568, 618, 1004] and on the back panel [60, 138, 618, 566]; no maker, no standard, no pictogram, no barcode; cigarette_pack: 'kentucky' is in brand_blocklist; cleaner_tin_01: then the atlas tile (a fictional maker) is laid over the label band; drain_cleaner: then the atlas tile (the yellow can's fictional label) is laid over the front label; lifebuoy: the made-up name, if the builder wants lettering: 'MARY ANN' in white sans on the ring, drawn by script over the first box.

**The final texture is checked (INV-06).** Script: after the step, for each listed box of the FINAL texture: the largest difference from the ring colour on any channel is at most 24 levels and fewer than 2 per cent of the box's pixels have a gradient above 40 levels: an erased box is the ring colour plus grain, with no glyph edge in it; a box that fails fails the build; where a whole map is replaced (boxes [0, 0, 1024, 1024]: cigarette_pack, the picture frames' artworks) the script checks that the final map is a different file from the downloaded one (its hash differs) and that the glTF points at the project's print. Visual: the builder opens the final map at 100 per cent beside the original and reads every printed word (a mark outside the listed boxes, a half-erased glyph and a seam are what no script can test); any word, number, logo, face or sticker still legible is a fault, and a new mark found goes into this list with its box.

**The brand blocklist** (`inventory.brand_blocklist`, searched by INV-05 and the self-check): 'dixons', 'currys', 'comet', 'rumbelows', 'titch banks', 'titch co', 'leitz', 'wetzlar', 'summilux', 'lanstey', 'polyluft', 'polyclean', 'kolo', 'steelbox', 'lorex', 'avventura', 'sirius', 'solidus', 'sdq', 'q-tech', 'jnl', 'micky', 'polyplast', 'urban quartz', 'nova presents', 'casio', 'sony', 'braun', 'zippo', 'leica', 'vtech', 'kentucky', 'snap-on', 'stanley', 'wd-40', 'ph 40', 'galler', 'philips', 'panasonic', 'sanyo', 'ncr', 'coca', 'pepsi', 'heinz', 'kellogg', 'lipton', 'tesco', 'woolworth', 'w h smith', 'wh smith', 'marlboro', 'benson', 'silk cut', 'embassy', 'players', 'rizla', 'post office', 'royal mail', 'bt '. The first four are the real British high-street retailers the review named; the next group are the makers and look-alikes read off the maps.

**Surfaces:** Poly Haven textures old_linoleum_flooring_01, linoleum_brown, painted_plaster_wall, dirty_carpet, long_white_tiles, square_tiles, terracotta_floor_tiles, marble_01, marble_tiles, rubber_tiles, worn_tile_floor, old_wooden_floor_02, old_wooden_floor_03, white_plaster_02, ceiling_interior, terrazzo_tiles, concrete_floor_painted (all exist: LIVE check); ambientCG Ice001, Ice002, Marble012, Rope001, Rope002, Candy001, Candy002, Fabric020, Fabric021, Fabric028, Fabric029, Cardboard002, Wicker010B, Terrazzo004, Tiles032, Tiles040, SurfaceImperfections001, Smear001, Fingerprints001, Scratches001, Leaking001, Metal042A (the ones read from its API are in ambientcg_checked.json). The packaged goods' labels are the project's atlas (production/assets/shop-goods/labels.jpg: 32 fictional makers in our OFL fonts), twelve tiles to add.

**Rules the inventory enforces.** every model a build places is listed in its inventory.json; each must be in `polyhaven`, `scripted` or a Sketchfab uid of `sketchfab_checked`; none in `denied`; no object, material or text contains a word of the blocklists; every Poly Haven model's 1k maps are looked at BEFORE the build (step 0) and every maker's mark is painted out of its base-colour map exactly as that model's `blank` step says (`texture_marks`); the gate then tests the listed boxes and the builder looks at the final map (INV-06); the approved pawnbroker pictures are searched by eye at full size for the same marks (INV-05)

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
| SO-01 | back wall stand-off | the stand-off (depth) of every fixture on the back wall | shelf units and their goods <= 0.30 (the written rule; the named exceptions in method.standoff_rules_m.shelf_named_exceptions: Rita's R-back-tv-tiers 0.35, within the 20 px budget at the card's middle), counters, machines and free pieces at the wall <= 0.60 tolerated, nothing deeper | none | 8 shops |
| SO-02 | side wall stand-off | the stand-off of every fixture and every placed good on a side wall | <= 0.05 flat, <= 0.10 tolerated, nothing deeper | none | 8 shops |
| SO-03 | floor and ceiling stand-off | the height of every thing on the floor, the drop of every thing from the ceiling | <= 0.025 true, <= 0.05 tolerated (a batten fitting 0.045) | none | 8 shops |
| SO-04 | nothing in the middle of the room | any mesh whose bounding box is more than 0.60 m from every wall and more than 0.05 above the floor | none | none | 8 shops |
| SO-05 | nothing stands across a door | back-wall fixtures of kind door against every other back-wall fixture: no shelf unit, counter or machine overlaps a door's x range below the door's top (Rita's back door x 1.45 to 2.35, z 0 to 2.0: the stock wall ends at x 1.35 and only one tier of boxes at z 2.05 to 2.25 stands over it); the built shelves stop at the door and the night_dark back-room light has its opening | no overlap | none | 8 shops |
| DSP-01 | the display stands in the window | every display item's extent against the window zone and the envelope: u inside the window zone, v 0 to 0.55 from the back of the glass, w from the bed to height_max_w | all inside; none in front of the shop door or the side door | 5 mm | 8 shops |
| DSP-02 | real geometry in the display | every display item is a mesh (no card, no picture), none a flat alpha cut-out except price cards 3 mm thick | true | none | 8 shops |
| INV-01 | inventory exists | each Poly Haven id in the inventory exists with a 1k glTF | true for every model in the inventory | none | 8 shops |
| INV-02 | nothing denied is placed | the build's inventory.json against inventory.denied | no denied id | none | 8 shops |
| INV-03 | every model is allowed | every model placed is in inventory.polyhaven, inventory.scripted or a Sketchfab uid of inventory.sketchfab_checked | true | none | 8 shops |
| INV-04 | scripted goods are the listed ones and carry a why | every scripted object name is a key of inventory.scripted; no fish, crab or prawn is a scripted body | true | none | 8 shops |
| INV-05 | no maker marks | every base-colour map of every placed model and every label tile is searched (by eye on a 2k sheet at the gate; by script: the manifest text, which cannot see a printed word) for inventory.brand_blocklist words; the approved pawnbroker pictures (pawnbroker_day, _night_lit, _night_dark) are searched by eye at full size for the same mark ('Dixons' on cassette_player, 4 px high at 2048 wide); every model's 1k maps are looked at before the build (step 0), not only at the gate | none found | none | 8 shops |
| INV-06 | the final textures carry no mark | for every model with `marks` in the inventory: the blanking step ran on the listed map and boxes (inventory.texture_marks.step) and the model's glTF points at the clean map; the final texture is tested in each listed box and looked at in full | script: in each box the largest difference from the ring colour is at most 24 levels and under 2 per cent of the pixels have a gradient above 40; visual (where a script cannot test it): the builder reads the final map at 100 per cent beside the original and no word, number, logo, face or sticker is legible | 24 levels; 2 per cent | 8 shops |
| NEV-01 | no people, drink, betting, children | object, material and text names and every glyph string of the build against inventory.content_blocklist | no match | none | 10 shops |
| NEV-02 | nothing after 1992 | no model from inventory.denied; no modern phone, flat screen, cordless-drill or LED lamp in any inventory | true | none | 10 shops |
| FRN-01 | the front's parts at their sizes | the 3.2 check's rows for the assembled bay (pilaster 350 slot / 290 shaft / 140 proud, console 240 x 205 x 550, fascia 5410 x 550 x 120, cornice 150, sill 75, stallriser 600, window frame at the shop's variant, transom 2400 to 2480 and head 2790 to 2850 over the window; what stands over the DOORS is FRN-07's) | as 2.2's checks | as 2.2's | 10 shops |
| FRN-02 | window and door zones | u of the window, shop door and side door against front.zones_u_mm; their centres against front.centres_street_x_m | equal | 2 mm; 3 mm | 10 shops |
| FRN-03 | the shop door | T1: leaf 900 x 2040 at z 28, glass 871 to 1973 with one bar at 1423 (28 wide), lock rail 549 to 871, letter plate 250 x 40 at z 678, lever side and hinge side as the table, the bell at z 1950 to 2050 inside; M1: glass 198 to 1968 and the letter plate centred in the 170 bottom rail at z 113 (outside the glass); M2: glass from 600 and the plate at 545 in the kick panel; the plate's z range never overlaps the door's glass (door.glass_z_mm) | equal | 5 mm | 10 shops |
| FRN-04 | the glass and the toplight layout | per shop: the number of lights and toplights; 6 mm plate at d 30; no pane in front of another; the toplight bars' centres, the bar on every mullion line and the width of every toplight (D6: each mullion carried up as a bar of its own width, each light's toplight split equally) | lights = n_mullions + 1; toplights = front.toplights_as_built = glazing_layout.toplights (Rita's and the newsagent's: nine of 326.9, bars at 390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1 plus the two mullions carried up; the empty unit nine of 324.7; the ironmonger six of 509.7; the grocer six of 683.0; the tea room six of 504.4; the launderette two of 1600); a bar on every mullion line; every toplight at least 250 wide; the toplights of one light equal within 1 mm; no toplight sliver beside a mullion; the over-door toplights are three equal panes (door.toplights_over_shop_door) | bar centres +-2 mm; widths +-1 mm | 10 shops |
| FRN-05 | paint colours | the base colour of each painted part against front.paint_srgb | within 6 levels per channel (aged paint: the 2.2 values) | 6 | 10 shops |
| FRN-06 | lobby | the grocer's door recessed 600 and the launderette's 300, floors as 2.2 | equal | 5 mm | grocer, steam_laundry |
| FRN-07 | no opening in the front | on the elevation drawn from target.json (target_drawing.front_polys), every point between the pilasters' inner edges (u 350 to 5650) from z 0 to 2850 lies on a part: stallriser, sill, window frame, glass, door (threshold, jambs, stop, leaf), fanlight, transom, toplight, panel, head, hood; Rita's: the band above the doors is door.fanlight (u 1344 to 2250, z 2131 to 2400), door.transom (u 350 to 2300, z 2400 to 2480), door.toplights_over_shop_door (three of 283.3, bars at 1641.3 and 1952.7, z 2480 to 2790), door.panel_over_side_door (844 wide field in a 944 slot, z 2480 to 2790) and door.head (u 350 to 2300, z 2790 to 2850) | the largest uncovered rectangle is at most 5 x 5 mm | 5 x 5 mm | 10 shops |
| FAS-01 | the fascia's sign in place | the 4.1 board texture on the fascia board (sample 12 points of the board's front: the render's base colour against the PNG at the same u, v); the applied sign (Mickey's letters, laundry and newsagent box, tea room panel) at the 2.2 u and z | equal | 3 levels; 5 mm | 10 shops |
| FAS-02 | hanging signs | Rita's three balls, the laundry's box, the ironmonger's and the chandler's boards at their 4.1 mounts | equal | 10 mm | ritas, steam_laundry, ironmonger, chandler |
| GLS-01 | nothing across the glass | every object between the glass and the street plane is one of: the 4.1 glass rows, the OPEN/CLOSED sign, the hours plate, SB1 (newsagent), the letting board (empty unit), the night grille (Rita's) or mesh (chandler) | true | none | 10 shops |
| LIT-01 | lit shops lit at night, dark shops dark | mean luma of the room-only composite (picture x brightness 0.7, glass reflection off) over the glass lights in STREET_SQUARE at night | lit: >= 45; dark: 10 to 35; the difference between a lit shop and the same shop dark >= 25 | none | 8 shops |
| LIT-02 | no black void in the street view | mean luma of the room-only composite over the glass lights, by day, in STREET_SQUARE, STREET_30 and CLOSE_35 | >= 33 by day; >= 45 at night for the lit shops | none | 8 shops |
| LIT-03 | the empty unit is a pale blank by day, not black | mean luma of the whitewashed glass in STREET_SQUARE by day | >= 150 (4.1's whitewash 214,212,204 under the day light); by night <= 40 | none | empty_unit |
| LIT-04 | Rita's grille | AT NIGHT the lattice over the window zone: bar 20 x 4, diamond 120, rails 40 x 40 at the transom (z 2.50 above the crown, 2400 above the footway) and 0.70 above the crown, plane 100 in front of the glass; the lit window seen through it. BY DAY the lattice is lifted out and stored inside and only the top rail and the bottom channel (powder black, with their fixing plates on the pilaster shafts) stand | equal | 5 mm | ritas |
| LIT-05 | the display is lit at night | in STREET_SQUARE at night, for each of the six lit shops, the display zone (the window lights' lowest 0.85 m, over the bed: z 0.70 to 1.55 above the crown, across the window zone) has a mean luma of at least 45, with the spec's spill modelled in the gate (the 350 lm rect light in the window head, tipped 62 degrees down, lighting channel 1: shop-interiors.json pawnbroker.lit_note); LIT-01 and LIT-02 are room-only and cannot see a dark window bed in a lit shop | >= 45 for chandler, grocer, mickeys, newsagent, ritas, tea_rooms | none | 6 shops |
| LIT-06 | the sodium wash is the game's | every room's night_dark sodium wash colour against production/specs/unreal-look.json lantern_linear_rgb (linear 1.0, 0.25, 0.0; the scene file's 1.0, 0.7055, 0.0 is stale: QUEUE.md 9 Oct 12:10) | equal | 0.01 | 8 shops |
| PRV-01 | the previews show nothing they must not | every mask of the photograph previews (extras.PREVIEW_PHOTOS, original pixels) is flat grey in the committed JPEG; no real firm's name, door number, face, drink or gambling sign or child is legible in any of the eleven previews | flat grey (120) in each mask; nothing legible | 6 levels, std 4 | 10 shops |
| CAM-01 | the cameras are the named ones | each render's camera against cameras.definitions and the shop's eye and aim | equal | 5 mm; 0.1 degree | 8 shops |

**Self-check** (before anything is built): self_check: 381 pass, 0 fail, 3 reported. Groups: 1 printed: 95 pass 0 fail 0 reported; 2 rule: 28 pass 0 fail 0 reported; 3 photo: 11 pass 0 fail 0 reported; 4 inventory: 11 pass 0 fail 0 reported; 5 room: 55 pass 0 fail 3 reported; 6 display: 18 pass 0 fail 0 reported; 7 consistency: 58 pass 0 fail 0 reported; 8 front: 86 pass 0 fail 0 reported; 9 marks: 19 pass 0 fail 0 reported. Negative controls: 33 of 33 mutations of target.json make it fail (controls.py): a free counter 2.4 m out in Rita's room; a unit 0.40 deep on a side wall; a denied model (WoodenChair_01) in the tea room's display; the T1 door's glass foot back at 600; a display item outside the window zone; the camera rule's wording changed; a card 0.1 m off; a hook-cast hour changed; a brand in the lettering; a pub word on a fixture; a dark shop marked lit; the picture 2048 wide; a good on a missing fixture; a hole in the front: Rita's panel over the side door only 220 high (FRN-07); no head across the doors: Rita's head only 40 wide (FRN-07); the over-door toplights gone from the grocer (FRN-07); a toplight bar 20 mm off its place (FRN-04); a toplight sliver 94.5 wide beside a mullion (FRN-04); the unaligned 2.2 toplights back on the ironmonger (FRN-04); 'dixons' out of the brand blocklist (INV-05); cassette_player's mark forgotten (INV-06); a blanking step with no boxes (INV-06); the stale sodium wash (1.0, 0.7055, 0.0) in Rita's night_dark (LIT-06); Rita's stock wall across her back door (SO-05); Rita's stock wall 0.40 deep again (SO-01); an M1 door's letter plate back in the glass at 545 (FRN-03); a ceiling fixture that fills the whole height (z 0 to 2.4); P6's fascia band left unmasked (PRV-02); a mask that is not grey in the committed JPEG (PRV-01); Rita's left wall bare again (a board only 1.8 m long); a fourth question on Jafar's page (the lit list); the nine other fronts pointing at a Markdown section again; Rita's grille with no daytime state.

## 11. What the target could not settle

- FOR JAFAR (a fact, no decision): the Poly Haven model `cassette_player` carries the real British retailer's name 'Dixons' (with a red roundel and 'TR12 Cassette Recorder') on its base-colour map. The same model is in the approved recipe's stock pool (tools/art-recipes/shop-room.py, `pool`), so the approved pawnbroker pictures (production/art/shop-rooms/pawnbroker_day.png, _night_lit.png, _night_dark.png, 6 October) MAY ALREADY CARRY THE FIRM'S NAME on the back wall, about 4 px high at 2048 wide (the writer looked at pawnbroker_day.png's back wall at 2x on 12 October and read no word on the small cassette players, but a 4 px mark cannot be ruled out; the two night pictures were not looked at). The builder must look at those three pictures' back wall at full size before anything else and report what it finds; this target blanks the mark on every new picture (inventory `marks`, check INV-06).
- The fish, crab and prawn scans, and the grocer's cabbage, potato, satsuma and pear: CC0 (Sketchfab, ffishAsia, checked today) but downloadable only with Jafar's login (the API answers 401). Until he gives it the fishmonger's slab and ice and trays are built and the fish row is marked 'goods pending'; the fishmonger cannot pass the CLOSE review without them. Named plainly: a failed capability of the cloud, not a plan to dress the window another way.
- No 1975 to 1995 photograph of a pawnbroker's or a launderette's window or room was reached (Geograph's categories start in 2005 and 2006; Commons returned a 1968 launderette with children in frame, not used). Rita's room rests on the approved pictures (RULINGS 2 Oct); no period photograph of a pawnbroker's room was reached. The launderette rests on the research's text and one 2009 front (P5).
- Maker marks: only thumbnails of the Poly Haven models were looked at on 12 October by the writer and the reviewer (about 45 at 384 to 1200 px), and thumbnails missed 'Dixons'. After the review the writer opened the 1k base-colour maps (see `inventory.polyhaven[id].marks`: every mark found, its map, its region and its blanking step). The builder looks at every one of the inventory's models at 1k BEFORE placing it (step 0 of the build, a contact sheet of 12 maps at a time), not at the gate.
- The T1 door numbers (D1) rest on one photograph of one door, scaled by assuming a 2040 leaf; the door bell is Judgement (no photograph of one was reached). Both are narrow points a reviewer can overturn with a better photograph.
- 4.1's fanlight street number: 4.1 puts it on the SIDE door's fanlight (x 20.18 for Rita's, the side door's centre) at z 2.18 in its street frame (above the crown: 2080 above the footway, below the shop door's fanlight). The review reads it as on the shop door's fanlight; this target follows the review (the number at the shop door's centre, baseline 2200 above the footway) and records the move of 4.1's x and z for its owner (`door.fanlight.street_number`).
- The hours of the grocer, ironmonger and chandler were not found; they are settled from the Shops Act (a Judgement). The street's lit list lights three shops that the hours (or, for the grocer and chandler, the Judgement from the Shops Act) say are shut by dusk in winter: the newsagent (17:30), the grocer and the chandler; kept as the street file has it (the street file and RULINGS 1 Oct settle it); the town should say which is right.
- Hal's shop (hook-cast.json, the coin shop, street x 39) stands inside the newsagent's bay (x 36 to 42): not resolved.
- Canon names no count of twelve shops: the street has ten units as built; 'twelve' and 'the other eleven' are the superseded atlas proposal's words.
- The picture's box floor is the card's bottom edge, 0.55 above the shop's real floor, which the stallriser hides from the street: the room reads as a stage whose floor is the window bed carried back. A truer floor needs a taller card, which terrace-front.py fixes at 0.65 to 3.05.
- The display can be only 0.55 m deep (the card stands 0.61 m behind the glass): the tea room's table and chairs and the launderette's baskets are tight. Moving the card back to the scene file's 1.2 m would give a deeper real zone; the brief fixes the card.
- The game's glass, Lumen's light on the display, the card's motion vectors under TSR, the exposure and the frame time cannot be shown from the cloud; they stay owed on the PC (`owed_on_pc`). PRJ-02 runs on the gate's own `trace` bake, so it proves the gate, not the game.
- Scripted goods with no CC0 model that may not pass the CLOSE review at the first try and are set aside under the two-tries rule: tomatoes, sweet jars, folded towels, newspapers and magazines, fish fillets. Each is named in `scripted`.

**Needs Jafar (at most three, one line each, recommended first):**

- May the builder have one Sketchfab login (a token, read-only, never in the repository) to download about fifteen CC0 scans (ten kinds: cod, mackerel, herring, flounder, crab, prawn, cabbage, potato, satsuma, pear)? Recommended: Yes. Why: without them the fishmonger and the grocer's produce cannot pass the close view; all are on the allowlist ('Sketchfab CC0 filter') and cost nothing.
- Timber shop doors: glass from 871 mm above the pavement (the Worcester photograph), from 600 mm (the earlier target, from a restored arcade), or from about 1000 mm (the door he has already approved in the game, one pane and no bar: rita-day-kit-2026-10-06.jpg)? Recommended: 871 (the photograph). Why: photographs win; the 8 October door review failed on exactly such details; 1000 would keep the approved door as it is, 600 is the earlier target's.
- Rita's room flattened so nothing smears at 1.5 m (the counter goes to the back wall, both side units go and become flat boards, the long-case clock and the cabinet go, the stock wall is 0.30 deep): approve? Recommended: Yes. Why: Rita's room is the approved model (RULINGS 2 Oct) and its composition changes, so it comes to him on one page before merging; before: the approved pawnbroker_day.png (6 October); after: D3 (production/previews/cloud-week/refs/shop-windows/D3-ritas-room-plan-picture.jpg) until the builder's first render replaces it.

## 12. Previews

Eleven JPEGs in production/previews/cloud-week/refs/shop-windows/ (at most 1200 px, under 300 KB each; credits in section 2). **What is masked in each, exactly** (flat grey 120, 120, 120, drawn on the original before the crop by `make_previews.py` on every rebuild from the list `extras.PREVIEW_PHOTOS`, then read back from the JPEG it wrote; `self_check.py` reads the committed JPEGs against the same list, checks PRV-01 to PRV-03; every preview was looked at by eye after the rebuild of 12 October and none shows a real firm's name, a door number, a face, alcohol, a gambling sign or a child):

- **P1 `P1-worcester-fish-front-below-fascia.jpg`** (original crop [0, 108, 640, 480]). The fascia board (the shop's name, its street number and telephone number) is above the crop; the red car at the left edge shows only its rear lamp and bumper (no number plate is in the picture). Masked: the orange window sticker (a fish picture and a fish merchant's firm name) on the right-hand window's left pane (box [383, 108, 436, 146]); the second orange sticker of the same fish merchant's firm name, on the right-hand window's right pane (box [557, 94, 611, 134]); the door's number plate (the street number of the real shop), the oval at the foot of the glass (box [284, 329, 313, 347]).
- **P2 `P2-bath-grocer-window-stock.jpg`** (original crop [30, 388, 192, 582]). The shop's fascia, its door and the person standing at it, and the right-hand shelves are outside the crop; no lettering in the crop is large enough to read (162 x 194 px). Masked: nothing needed masking (nothing legible is in the crop).
- **P3 `P3-pinner-hardware-newsagent-windows.jpg`** (original crop [300, 326, 690, 520]). The parade's fascias and a drink merchant's sign are above and beside the crop; the one strip of a fascia at the top right and a notice at the top of the hardware window are a few pixels high and not legible. Masked: nothing needed masking (nothing legible is in the crop).
- **P4 `P4-hull-chandler-front-mesh.jpg`** (original crop [225, 548, 600, 990]). The shop's fascia and sign are above the crop. Masked: the painted board on the door post, which names the firm, its office and its trades (the large grey box in the middle) (box [405, 655, 478, 748]); the gilt lettering on the upper glass at the left, which names the firm (the grey box at the top left) (box [300, 580, 350, 645]); the red sign on the glass below that lettering (a firm's or an alarm company's mark) (box [308, 644, 332, 690]).
- **P5 `P5-launderette-front-type-2009.jpg`** (original crop [0, 262, 330, 425]). Only the trade word 'Launderet(te)' of the fascia and a small notice on the door are in the crop; neither is a firm's name. Masked: nothing needed masking (nothing legible is in the crop).
- **P6 `P6-kames-unlet-shop-1995.jpg`** (original crop [56, 296, 417, 420]). The upper floors and the roof are above the crop (they carry no lettering). Masked: the whole fascia band of the old shop, which carries the firm's name and its trades in painted lettering (the Geograph page's own title repeats them): a slanted band from the eaves line to the window heads (polygon [[66, 284], [272, 262], [272, 306], [258, 306], [212, 303], [165, 315], [125, 319], [66, 326]]); the neighbouring shop's board, at the right (a second firm's name) (box [346, 290, 417, 327]).
- **P1 overlay `P1-worcester-fish-front-target-on-photo.jpg`**: made from the masked P1 crop, so it carries the same three masks (the door's number plate included) with the target's door, stallriser, glass-foot and glazing-bar lines laid on at the scale fitted on the leaf's height.
- **D1 `D1-ritas-front.jpg`, D2 `D2-ten-fronts-sheet.jpg`, D3 `D3-ritas-room-plan-picture.jpg`, D4 `D4-standoff-and-cameras.jpg`**: drawn from target.json alone; no photograph is in them and nothing in them is masked. D1 and D2 now show the band above the doors (fanlight, transom, three toplights, panel, head) and the aligned toplights on every front.
- The earlier P6 (it showed the old fascia's lettering and the neighbouring board) and the earlier P1 (it showed the door's number) were deleted from the folder and rebuilt as above; the earlier files remain in the history of the commit that first added them.

