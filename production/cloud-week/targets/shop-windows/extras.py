"""Author tool: the prose and the check list of target.json (sources, photographs, disagreements, the failures answered, reuse, checks, what is not settled)."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DATE = "2026-10-12"

SOURCES = [
    {"id": "P1", "what": "Iddles fishmonger's front, Worcester (Geograph, 'Iddles fishmongers - 2'): an old shop front left as it was: divided timber lights, a black-tiled stallriser, a half-glazed timber door, the slab visible through the glass",
     "url": "https://www.geograph.org.uk/photo/2192169", "read": DATE, "author": "Helen Iwanczuk", "licence": "CC BY-SA 2.0", "taken": "May 2000 (the page: 'taken May 2000')",
     "shows": "the front a fish shop kept for decades (the author: the premises 'remained in this condition'): door leaf 335 px high by 140 wide (0.42), glass foot 0.413 of the leaf, two panes divided by a bar at 0.685, a letter plate at 0.32, stallriser tiled to 0.28 of the leaf, the window slab and the room dark behind reflections",
     "dated_object": "a period object: a later photograph of a front unchanged since before 1990 (the page says so); 2000 is the earliest dated photograph of a fish-shop window reached", "used": "measured (photo_measurements.json), cropped below the fascia for the preview, the main photograph of the self-check's overlay"},
    {"id": "P2", "what": "Holyoake's grocer's shop, Bath Road (Geograph, March 1999): an open-fronted stock window, tiered stands, goods stacked to the glass, the shop's back shelves visible",
     "url": "https://www.geograph.org.uk/photo/2184467", "read": DATE, "author": "Helen Iwanczuk", "licence": "CC BY-SA 2.0", "taken": "March 1999",
     "shows": "density of a grocer's window and the depth of its stock (tins, jars, crates on tiered timber stands); a person stands at the door (masked in the preview)", "dated_object": "a long-established shop (the page: established 1898); 1999 shows a 1990 window",
     "used": "yes: the tiered stand and the density in the grocer's display; preview cropped to the left window and stand (the shop door, with a person at it, and the right-hand shelves are outside the crop)"},
    {"id": "P3", "what": "Shops in Cannon Lane, Pinner (Geograph): a hardware store's and a newsagent's windows, one lit and readable, one dark",
     "url": "https://www.geograph.org.uk/photo/5945841 (and 3403654, the same parade)", "read": DATE, "author": "Carl Grove", "licence": "CC BY-SA 2.0", "taken": "20 February 1989",
     "shows": "a 1989 high-street parade: the hardware window's dark interior with stock to the ceiling behind reflections; the newsagent's lit interior with racks; deep recessed doors; cars of 1989", "dated_object": "a photograph of the period itself",
     "used": "yes: the black-void question (the glass is mostly reflection by day, the room dim; a lit shop reads); preview cropped to the two windows below their fascias (the parade's other signs, a drink merchant's, are outside the crop)"},
    {"id": "P4", "what": "A ship chandler's shut shopfront, High Street, Hull (Geograph): green timber front, lower lights screened inside with woven galvanised mesh",
     "url": "https://www.geograph.org.uk/photo/3378991", "read": DATE, "author": "Bernard Sharp", "licence": "CC BY-SA 2.0", "taken": "1 January 1983 (the feed's date; the page says taken before redevelopment)",
     "shows": "the chandler's front: three tall lights, mullions in green, mesh screens over the lower lights, a plaque on the door post", "dated_object": "a photograph of the period itself",
     "used": "yes: the night mesh screens (chandler), the green; preview cropped below the fascia with the glass lettering and the plaque masked (a real firm's name)"},
    {"id": "P5", "what": "Launderette in Hambledon Parade (Geograph): a 1960s-80s aluminium-framed launderette front with a script fascia and a striped blind, the room dark behind the glass",
     "url": "https://www.geograph.org.uk/photo/1633924", "read": DATE, "author": "Basher Eyre", "licence": "CC BY-SA 2.0", "taken": "26 December 2009",
     "shows": "the type of front (full-height glazing, glazed door, machines faintly seen); LATER than 1995: used only for the type and for what a launderette window does by day", "dated_object": "a later photograph; the front's pattern is the 1970s-80s one (not dated by the author)",
     "used": "as a type reference only; preview cropped to the front"},
    {"id": "P6", "what": "A derelict grocer and draper's shop, Kames (Geograph): glass dark or blank, paint gone, a pillar box at the kerb",
     "url": "https://www.geograph.org.uk/photo/27024", "read": DATE, "author": "Andrew Longton", "licence": "CC BY-SA 2.0", "taken": "24 May 1995",
     "shows": "an unlet shop in 1995: the glass reads grey-blue and blank, not black; no whitewash", "dated_object": "a photograph of the period itself", "used": "for the empty unit's glass: it must read as a pale blank, not a black hole; preview cropped"},
    {"id": "H1", "what": "Poly Haven catalogue (api.polyhaven.com/assets?t=models, and /files/<id> for each of the 105 models used): 521 models, 868 textures; each model's name, size, triangles, date, authors and glTF file read; thumbnails (cdn.polyhaven.com) looked at on three contact sheets",
     "url": "https://api.polyhaven.com/assets?t=models", "read": DATE, "author": "Poly Haven contributors", "licence": "CC0", "taken": "n/a", "shows": "every id in the inventory exists with a 1k glTF", "dated_object": "n/a", "used": "yes (inventory.polyhaven)"},
    {"id": "H2", "what": "ambientCG API (ambientcg.com/api/v2/full_json): ids checked to exist as CC0 materials", "url": "https://ambientcg.com/api/v2/full_json", "read": DATE, "author": "ambientCG", "licence": "CC0", "taken": "n/a",
     "shows": "Tiles032, Tiles040, Ice001, Ice002, Marble012, Rope001, Rope002, Candy001, Candy002, Fabric020, Fabric021, Fabric028, Fabric029, Cardboard002, Wicker010B, Terrazzo004 and the imperfection sets exist (a search call reset twice and is not relied on)", "dated_object": "n/a", "used": "yes (inventory.ambientcg_checked)"},
    {"id": "H3", "what": "Sketchfab API v3 (anonymous): the ffishAsia / floraZia CC0 scans (cod, mackerel x2, herring, flounder x2, crab, prawn x2, apple, cabbage, potato, satsuma, pear, lemon): name, licence 'CC0 Public Domain', faces, publish date, downloadable true; the download endpoint answers 401 without a login",
     "url": "https://api.sketchfab.com/v3/models/<uid>", "read": DATE, "author": "ffish.asia / floraZia.com", "licence": "CC0 Public Domain", "taken": "scans published 2021 to 2026", "shows": "the goods that no Poly Haven model gives are real scans, on the allowlist ('Sketchfab CC0 filter'), and need only Jafar's login",
     "dated_object": "n/a", "used": "yes (inventory.sketchfab_checked); not downloaded"},
    {"id": "H4", "what": "Smithsonian Open Access 3D API (3d-api.si.edu/api/v1.0/content/file/search): answers from the cloud; queries for mackerel, flounder, haddock, plaice, lobster, Gadus, Clupea and Scomber return nothing; 'cod' and 'herring' return only unrelated objects (a horseshoe crab, a flight suit); 'crab' returns a king crab (Lithodidae), 'shrimp' a mantis shrimp",
     "url": "https://3d-api.si.edu/", "read": DATE, "author": "Smithsonian", "licence": "CC0 (per item; not on the allowlist by name)", "taken": "n/a", "shows": "no British fish are there", "dated_object": "n/a", "used": "no: nothing fits and it is not named on the allowlist"},
    {"id": "G1", "what": "Wikimedia Commons (API, one request at a time; many 429s): category listings for launderettes, fishmongers, ship chandlers, tea rooms, pawnbrokers; the 1968 'Twthill laundrette, Caernarfon' (CC BY-SA 4.0, Geoff Charles) was seen and has children in the frame",
     "url": "https://commons.wikimedia.org/", "read": DATE, "author": "various", "licence": "various", "taken": "see text", "shows": "no photograph from 1975 to 1995 of a pawnbroker's or a launderette's window or room was reached; the Caernarfon launderette (1968) is NOT used (children)", "dated_object": "n/a", "used": "no"},
    {"id": "R", "what": "Project files read: canon.md, TOWN.md, RULINGS.md, DECISIONS.md 236 and 243, production/specs/shop-interiors.json, vignette-scene.json, vignette-pieces.json, hook-cast.json, tools/ue/make_interior_material.py, tools/art-recipes/shop-room.py, fetch_polyhaven.py, make_label_atlas.py, terrace-front.py 2385-2417, production/research/shop-window-interiors/*, shop-hours-1990, targets/shopfronts (2.2), targets/fascia-signs (4.1), kit/shopfront/NOTES.md, 2d/fascias/NOTES.md, HANDOVER.md, commit 2f475f5 and NOW.md as of it",
     "url": "-", "read": DATE, "author": "studio", "licence": "own", "taken": "-", "shows": "the game's format, the three failures of 3 October, the ten units, the lit list, the hours", "dated_object": "-", "used": "yes"},
]

UNREACHED = [
    "Peter Marshall's Hull and 1990 London photographs (Flickr): named in NOTE.md as links only; not requested in this unit, so no number rests on them.",
    "Picture Sheffield t13140 and t13138 (the fishmonger of 1989 and 1990): read by the builder on 3 October (FISHMONGER-2026-10-03.md), not re-read today; used only as that note reports them.",
    "Any photograph from 1975 to 1995 of a pawnbroker's window or room, a launderette's window or room, or a ship chandler's interior: none was reached (Geograph's category 'Pawnbroker' starts in 2006 and 'Launderette' in 2005; Commons returned US, Irish and foreign shops and a 1968 launderette with children).",
    "Historic England and the Black Country Living Museum's pawnbroker (a 1930s reconstruction): not used.",
    "A Sketchfab download of any scan: needs Jafar's login (401 without).",
]

PHOTO_MEASUREMENTS = {
    "main_photograph": "P1 (Geograph 2192169, 640 x 480)",
    "method": "the photograph is nearly face-on; every edge was read by eye off a 4x enlargement with a 10-pixel grid (error +-3 px); ONE dimension fits the scale: the door leaf's height, 335 px, taken as the street's 2040 mm (6.09 mm a pixel), so every other number is a ratio of the leaf's height and is Photo only to that assumption (a 2100 leaf would move the glass foot to 867)",
    "rows": [
        {"what": "door leaf top (underside of the transom's board)", "y_px": 122.0}, {"what": "door leaf bottom / threshold", "y_px": 457.5},
        {"what": "glass top", "y_px": 137.5}, {"what": "glazing bar, centre", "y_px": 228.0}, {"what": "glass foot", "y_px": 319.0},
        {"what": "letter plate, centre", "y_px": 350.5}, {"what": "number plate, centre", "y_px": 338.0}, {"what": "handle, centre", "y_px": 316.0},
        {"what": "lower panel field, top", "y_px": 372.5}, {"what": "lower panel field, bottom", "y_px": 422.5}, {"what": "stallriser top (tile cap)", "y_px": 362.0},
        {"what": "leaf left edge", "x_px": 230.0}, {"what": "leaf right edge", "x_px": 370.0}, {"what": "glass left", "x_px": 251.0}, {"what": "glass right", "x_px": 350.5},
    ],
    "derived_mm_from_the_leaf_height_2040": {},
}

DISAGREEMENTS = [
    {"id": "D1", "what": "where a timber shop door's glass starts", "target_2_2": "600 (level with the sill; Leadenhall 2019 at 0.304 of the leaf; DOR-06)", "photograph": "871 +-30 above the footway (843 above the leaf's foot: 0.413 of the leaf, Geograph 2192169, a fish shop's untouched front, May 2000); the lock rail runs 549 to 871 with the letter plate in it at 678",
     "chosen": "the photograph: T1 door glass from 871 above the footway (843 above the leaf's foot), the lock rail 549 to 871, the letter plate at 678, one glazing bar at 1423; the aluminium and bronze doors keep 2.2's numbers",
     "why": "Leadenhall is a 2019 heritage restoration of a London arcade; the Worcester front is a working shop in the period's condition and the nearer match; 2.2's DOR-06 (door glass foot = sill top) is replaced for T1 doors only. Flagged for Jafar (Needs you)."},
    {"id": "D2", "what": "the glass of the window lights", "target_2_2": "one sheet per light, no astragal bars (Rita's approved window)", "photograph": "Geograph 2192169 shows each light divided by one bar at the door's bar height; Pinner 1989 shows single large sheets (hardware) and aluminium-framed sheets (newsagent)",
     "chosen": "single sheets per light as 2.2 (Rita's window is the model and approved); the divided pattern is recorded as a possible variant, not adopted", "why": "RULINGS 2 Oct; the photographs split"},
    {"id": "D3", "what": "the door leaf's width", "target_2_2": "900 in a 1006 slot", "photograph": "about 853 (140 px of a 335 px leaf) in an older door", "chosen": "900 as 2.2: the slot is fixed by the bay; the photograph is within 6 per cent of it", "why": "inside the error"},
    {"id": "D4", "what": "the stallriser's height", "target_2_2": "600", "photograph": "571 +-18 (94 px of the leaf's 335)", "chosen": "600", "why": "inside the error (5 per cent)"},
    {"id": "D5", "what": "how bright the room reads from the street by day", "target_2_2": "the game's day brightness 0.15", "photograph": "P1 and P3: the glass is mostly reflection, the room dim; only a lit, bright shop (Pinner's newsagent) shows its goods by day",
     "chosen": "the game's 0.15 kept for every shop (the spec's values are the game's)", "why": "the research (NOTE.md section 3 and 8) and these photographs agree: over-bright day interiors are the commonest giveaway"},
    {"id": "D6", "what": "an open-fronted grocer's window", "target": "a glazed window with a 1930s bronze front", "photograph": "P2 shows stock stood out on stands in an open front", "chosen": "glazed, as 2.2", "why": "the street's grocer is a 1930s refit with glass; the density and the stands are taken, not the open front"},
    {"id": "D7", "what": "mesh over a chandler's lower lights", "target_2_2": "none", "photograph": "P4 shows woven galvanised mesh screens inside the lower lights of a shut chandler's", "chosen": "added as the chandler's night furniture (three panels)", "why": "the photograph shows it"},
    {"id": "D9", "what": "the chandler's paint", "target_2_2": "navy on piers, consoles, board and cornice, natural aluminium window", "photograph": "P4 (Hull, 1983) shows a chandler's front in dark green", "chosen": "navy as 2.2 and 4.1 (the street's board is navy); the photograph's green is used for the room's dado", "why": "the Hull shop is another shop; the street's colours are fixed by 4.1"},
    {"id": "D8", "what": "the street's lit list against the hours", "target": "vignette-pieces lit_names: 6 units lit at night", "photograph/research": "the hours research: everything shut by 8 pm; newsagent 17:30; the grocer, ironmonger and chandler not found", "chosen": "the street file's list is kept (RULINGS 1 Oct: lit windows, not one wash); the hours are the town's and are noted", "why": "a conflict between two files of the project; not mine to resolve"},
]

FAILURES = [
    {"id": "F1", "failure": "goods made by hand (3 Oct, first review: 'toys beside Rita's scanned stock')",
     "answer": "105 Poly Haven models (CC0, each read from the API today) carry every shop's goods; what has no CC0 model is a SCAN named by uid (Sketchfab ffishAsia CC0, checked today) needing Jafar's login, or a short scripted form whose reason is written beside it (`scripted` in target.json: 52 kinds, each with a why); hand-modelled fish are forbidden; packaged goods are bevelled shapes carrying the project's fictional label atlas (production/assets/shop-goods/labels.jpg), never plain colour blocks",
     "checks": ["INV-01", "INV-02", "INV-03", "INV-04", "INV-05"]},
    {"id": "F2", "failure": "named faults (3 Oct, second round)",
     "answer": [
         "displays placed as if the door were on Rita's side (half behind the door): each display's range is the window zone of the 2.2 bay table for that shop's door end (DSP-01)",
         "a black chiller panel smeared across the fish shop's floor: the chiller is a white counter against the back wall, nothing free in the room (SO-01)",
         "the white slab burnt out at night: the fish shop is dark at night; no picture has more than 1 per cent of pixels at 250 or above (PIC-05)",
         "Gothic chairs and empty frames in the tea room: WoodenChair_01 and the Gothic set are denied; the frames carry the project's own prints; chairs and tables exist only in the window (INV-02, SO-02)",
         "an explosives sign on a drum at the chandler's: Barrel_01 is denied; no drum stands in the display (INV-02)",
         "a gold ribbon drawn across the newsagent's window and every stood card outside the glass: a check that nothing but the listed lettering, the OPEN sign, the hours plate and SB1 lies in front of the glass (GLS-01)",
         "faceted fruit: fruit are scans (Poly Haven apple, lemon, onion, bananas; ffishAsia cabbage, potato, satsuma, pear); the one scripted fruit, the tomato, is a one-try item set aside if it reads as toys",
         "slab laundry: laundry is stacks of bevelled towels with a woven-towel material and a lean, parcels with string and tags, baskets of displaced cloth",
         "counters, chairs and dryers standing off the walls: no fixture stands off a surface by more than the budget (SO-01 to SO-04)"]},
    {"id": "F3", "failure": "what a projected room cannot do at a metre or two (3 Oct, third round)",
     "answer": "the numbers from the game's own rule: stock only on the back wall (0.30 deep is true, a 0.60 counter or machine against it is tolerated), the side walls carry boards and racks at most 0.10 (0.05 true), the floor and ceiling only flat things (0.025); anything else stands in the display, which is real geometry in the near 0.55 m. The CLOSE view stands at 1.5 m from the glass, 35 degrees off, because there the whole window is seen at under 62 degrees (the glass's hand-over) and the surfaces are sharp at 4096 wide; the slide numbers are in TARGET.md section 3 (`method.honest_range`); the picture is 4096 wide because at 2048 it is soft over 4 per cent of the glass at 1.5 m and 13 per cent at 0.5 m",
     "checks": ["SO-01", "SO-02", "SO-03", "SO-04", "PIC-01", "PRJ-01", "PRJ-02", "PRJ-03"]},
]

REUSE = [
    {"part": "the method (research NOTE.md, CLOSE-RANGE, GOODS, DRESSING, FISHMONGER, hours, glass reflections, FRONTAGE)", "keeps": "a pre-projected picture per room and state, the near metre real, lights per state, the never-list, the trades' goods and fittings",
     "changes": "the room is no longer allowed to hold anything the picture cannot honestly show (the budgets); CLOSE-RANGE's 'real rooms' recommendation is NOT followed here (the brief asks for textures); its 'keep everything flat against the walls' is the rule"},
    {"part": "production/specs/shop-interiors.json", "keeps": "the camera rule, the three states, the never list, the two entries (mickeys unchanged; pawnbroker's room, card, camera_d, brightness, lit values unchanged)",
     "changes": "eight entries added (spec_entries in target.json: fishmonger, launderette, grocer, chandler, tea_room, ironmonger, newsagent; the pawnbroker's pixels_wide 2048 to 4096 and its display x0/x1 noted against the 3.2 front); no entry for the empty unit (no card)"},
    {"part": "tools/art-recipes/shop-room.py", "keeps": "the box, the camera rule, the three renders, the JSON beside each, model() from Poly Haven, texmat(), --display, --export-room (inert)",
     "changes": "the room builders for the seven trades are rewritten to the fixtures in target.json (free-standing counters and units removed); pixels_wide 4096; the maker-mark pass; the inventory.json"},
    {"part": "tools/ue/make_interior_material.py", "keeps": "everything: its `trace` is the rule the cloud gate imports; the HLSL is unchanged", "changes": "none"},
    {"part": "tools/art-recipes/fetch_polyhaven.py", "keeps": "the fetcher and the SETS", "changes": "SETS gain the ids of the inventory; none of the denied"},
    {"part": "production/assets/shop-goods/labels.jpg and make_label_atlas.py", "keeps": "the 32 fictional products", "changes": "twelve tiles added (paint, varnish, twine, tobacco, crab paste, detergent) in the same fonts"},
    {"part": "production/assets/shop-displays/pawnbroker-display.glb", "keeps": "as built, with its 23 models", "changes": "maker marks blanked; the night grille added; no piece repeated more than twice"},
    {"part": "the 3.2 kit (production/cloud-week/kit/shopfront)", "keeps": "pilaster (panel), console (scroll), fascia board, cornice (150 as built, 12 Oct), sill, stallriser (panel, three panels), window frame T1 (3 lights, nine toplights as built): Rita's front is complete but for the doors", "changes": "nine variants are missing for the other fronts (front.missing_from_3_2 in each shop); the doors and the lobbies are specified here, from 2.2 section 10, with three changes (D1) and the bell"},
    {"part": "2.2 (targets/shopfronts)", "keeps": "the ten fronts' table, paints, glazing layouts, door ends and hinges", "changes": "T1 door: glass foot, lock rail, letter plate, a glazing bar (D1); the bell"},
    {"part": "4.1 (2d/fascias)", "keeps": "the ten boards, the four hanging signs, the glass rows, the whitewash and the letting board, unchanged", "changes": "none; each shop names its board"},
    {"part": "4.2 to 4.4 (2d/paper)", "keeps": "the OPEN/CLOSED sign, the newsagent's board SB1, the letting boards", "changes": "none"},
    {"part": "3.1 doors", "keeps": "F1 for every side door", "changes": "none"},
    {"part": "the set-aside branch shops-wip-2026-10-03 (a local branch on the PC, not in this clone)", "keeps": "nothing taken: it was not reachable and its goods were made by hand", "changes": "replaced; the reason is F1"},
]

COULD_NOT_SETTLE = [
    "The fish, crab and prawn scans, and the grocer's cabbage, potato, satsuma and pear: CC0 (Sketchfab, ffishAsia, checked today) but downloadable only with Jafar's login (the API answers 401). Until he gives it the fishmonger's slab and ice and trays are built and the fish row is marked 'goods pending'; the fishmonger cannot pass the CLOSE review without them. Named plainly: a failed capability of the cloud, not a plan to dress the window another way.",
    "No 1975 to 1995 photograph of a pawnbroker's or a launderette's window or room was reached (Geograph's categories start in 2005 and 2006; Commons returned a 1968 launderette with children in frame, not used). Rita's display and room stay on the project's earlier sources (Marshall's Hull photographs, the Black Country museum, as links); the launderette rests on the research's text and one 2009 front (P5).",
    "Only thumbnails of the Poly Haven models were looked at. Maker marks seen at that size: wall_clock, digital_wrist_watch, Television_01, vintage_lighter, measuring_tape_01, Camera_01, the portable cassette player, plastic_crate_01, lubricant_spray and others; the list says what was dropped and what is blanked. The gate's first check is a look at every model's 1k maps by eye.",
    "The T1 door numbers (D1) rest on one photograph of one door, scaled by assuming a 2040 leaf; the door bell is Judgement (no photograph of one was reached). Both are narrow points a reviewer can overturn with a better photograph.",
    "The hours of the grocer, ironmonger and chandler were not found; they are settled from the Shops Act (a Judgement). The street's lit list lights three shops that the hours (or, for the grocer and chandler, the Judgement from the Shops Act) say are shut by dusk in winter: the newsagent (17:30), the grocer and the chandler; kept as the street file has it; the town should say which is right.",
    "Hal's shop (hook-cast.json, the coin shop, street x 39) stands inside the newsagent's bay (x 36 to 42): not resolved.",
    "Canon names no count of twelve shops: the street has ten units as built; 'twelve' and 'the other eleven' are the superseded atlas proposal's words.",
    "The picture's box floor is the card's bottom edge, 0.55 above the shop's real floor, which the stallriser hides from the street: the room reads as a stage whose floor is the window bed carried back. A truer floor needs a taller card, which terrace-front.py fixes at 0.65 to 3.05.",
    "The display can be only 0.55 m deep (the card stands 0.61 m behind the glass): the tea room's table and chairs and the launderette's baskets are tight. Moving the card back to the scene file's 1.2 m would give a deeper real zone; the brief fixes the card.",
    "The game's glass, Lumen's light on the display, the card's motion vectors under TSR, the exposure and the frame time cannot be shown from the cloud; they stay owed on the PC.",
    "Scripted goods with no CC0 model that may not pass the CLOSE review at the first try and are set aside under the two-tries rule: tomatoes, sweet jars, folded towels, newspapers and magazines, fish fillets. Each is named in `scripted`.",
]

NEEDS_YOU = [
    {"q": "May the builder have one Sketchfab login (a token, read-only, never in the repository) to download about fifteen CC0 scans (ten kinds: cod, mackerel, herring, flounder, crab, prawn, cabbage, potato, satsuma, pear)?", "recommended": "Yes", "why": "without them the fishmonger and the grocer's produce cannot pass the close view; all are on the allowlist ('Sketchfab CC0 filter') and cost nothing"},
    {"q": "Timber shop doors: glass from 871 mm above the pavement (the Worcester photograph) or 600 mm (the earlier target, from a restored arcade)?", "recommended": "871 (the photograph)", "why": "photographs win; the 8 October door review failed on exactly such details"},
    {"q": "At night, light the units the street file lights (newsagent, grocer, chandler, tea room, Rita's, Mickey's after the key), or only those open late (tea room to 22:00, Rita's by ruling)?", "recommended": "keep the street file's six", "why": "RULINGS 1 Oct asks for lit windows with darkness between; the hours are a research note"},
]


def checks(t):
    C = []

    def add(id_, name, what, expected, tol, applies, kind, how):
        C.append({"id": id_, "name": name, "what": what, "expected": expected, "tolerance": tol, "applies_to": applies, "kind": kind, "how": how})
    rooms = [s["id"] for s in t["shops"] if s.get("room")]
    lit = [s["id"] for s in t["shops"] if s.get("room") and s["lit_at_night"]]
    dark = [s["id"] for s in t["shops"] if s.get("room") and not s["lit_at_night"]]
    allshops = [s["id"] for s in t["shops"]]
    add("PIC-01", "picture files", "each state's PNG is 4096 x 1855, 8-bit sRGB, with the JSON beside it holding w, h, d, camera_d, pixels, states", "w 5.3, h 2.4, d per shop, camera_d 5.3", "exact", rooms, "picture", "read the files")
    add("PIC-02", "no black void in the picture", "mean Rec.709 luma of the day / night_lit picture; the share of pixels under 12; the largest connected region under 12",
        "day mean >= 83.7 and night_lit mean >= 55.9 (0.7 of Rita's approved 119.5 and 79.8); share under 12 <= 0.03; no region under 12 larger than 3 per cent of the area", "none", rooms, "picture", "numpy on the PNG")
    add("PIC-03", "night_dark is dark, not black", "mean luma of the night_dark picture", "12.4 to 40 (Rita's approved 17.7, 0.7 to 2.3 times)", "none", rooms, "picture", "numpy")
    add("PIC-04", "the floor line and the back wall where the rule puts them", "a flat-colour pass (one colour a surface) of the room; the back wall's four corners in the 4096 x 1855 picture",
        "for D 4.5: top-left and bottom-right corners as method.floor_and_back_wall.back_wall_in_picture.px_4096 (about (940, 426) and (3156, 1429)); for another D recomputed by the rule", "+-8 px on each corner", rooms, "picture", "project(x, y, z) of tools/ue/make_interior_material.py against the pass")
    add("PIC-05", "nothing burnt", "share of pixels with any channel at 250 or above", "<= 0.01 in every picture", "none", rooms, "picture", "numpy")
    add("PIC-06", "each surface has texture", "the standard deviation of the luma inside the back wall's rectangle, the floor's trapezoid and each side wall's trapezoid", ">= 6 levels in each (not a flat colour)", "none", rooms, "picture", "from the flat-colour pass masks")
    add("PRJ-01", "the identity camera", "from the render camera (card centre, 5.3 m in front, mid height) every card point shows its own picture pixel", "|u - u0| and |v - v0| <= 1 px at 4096", "1 px", rooms, "projection", "trace() on a grid of 41 x 21 card points")
    add("PRJ-02", "the room shifts with the eye", "between CLOSE_35 and CLOSE_35_B (2.0 m apart along the street) the back wall's centre point lands at picture columns that differ by the rule's value, and the whole card picture differs",
        "the column difference equals target.json's `parallax_test.expected_du_px` per shop; the mean absolute difference of the two baked card pictures >= 8 levels", "+-1.5 px; none", rooms, "projection", "trace() for both cameras; compare to the builder's render")
    add("PRJ-03", "the gate shows the game's rule", "the baked card picture for a camera equals the picture sampled through trace() for the same camera and card", "mean absolute difference <= 0.5 level, no pixel off by more than 3", "none", rooms, "projection", "recompute with the imported trace")
    add("SO-01", "back wall stand-off", "the stand-off (depth) of every fixture on the back wall", "<= 0.30 true, <= 0.60 tolerated (counters, machines, free pieces at the wall), nothing deeper", "none", rooms, "room", "fixtures[].depth_m against method.standoff_rules_m (the builder also measures the built meshes' bounding boxes)")
    add("SO-02", "side wall stand-off", "the stand-off of every fixture and every placed good on a side wall", "<= 0.05 flat, <= 0.10 tolerated, nothing deeper", "none", rooms, "room", "as SO-01")
    add("SO-03", "floor and ceiling stand-off", "the height of every thing on the floor, the drop of every thing from the ceiling", "<= 0.025 true, <= 0.05 tolerated (a batten fitting 0.045)", "none", rooms, "room", "as SO-01")
    add("SO-04", "nothing in the middle of the room", "any mesh whose bounding box is more than 0.60 m from every wall and more than 0.05 above the floor", "none", "none", rooms, "room", "scan the built scene")
    add("DSP-01", "the display stands in the window", "every display item's extent against the window zone and the envelope: u inside the window zone, v 0 to 0.55 from the back of the glass, w from the bed to height_max_w", "all inside; none in front of the shop door or the side door", "5 mm", rooms, "display", "bounding boxes of the built display against the 2.2 zones")
    add("DSP-02", "real geometry in the display", "every display item is a mesh (no card, no picture), none a flat alpha cut-out except price cards 3 mm thick", "true", "none", rooms, "display", "scan the glb")
    add("INV-01", "inventory exists", "each Poly Haven id in the inventory exists with a 1k glTF", "true for every model in the inventory", "none", rooms, "inventory", "self_check.py (offline from polyhaven_checked.json; --live re-asks the API)")
    add("INV-02", "nothing denied is placed", "the build's inventory.json against inventory.denied", "no denied id", "none", rooms, "inventory", "set difference")
    add("INV-03", "every model is allowed", "every model placed is in inventory.polyhaven, inventory.scripted or a Sketchfab uid of inventory.sketchfab_checked", "true", "none", rooms, "inventory", "set difference")
    add("INV-04", "scripted goods are the listed ones and carry a why", "every scripted object name is a key of inventory.scripted; no fish, crab or prawn is a scripted body", "true", "none", rooms, "inventory", "set difference and a name scan ('fish', 'cod', 'mackerel', 'crab', 'prawn' only from a scan uid)")
    add("INV-05", "no maker marks", "every base-colour map of every placed model and every label tile is searched (OCR by eye on a 2k sheet at the gate; by script: the manifest text) for inventory.brand_blocklist words", "none found", "none", rooms, "inventory", "text scan of manifests and the glyph lists; eyes on the sheet")
    add("NEV-01", "no people, drink, betting, children", "object, material and text names and every glyph string of the build against inventory.content_blocklist", "no match", "none", allshops, "never", "string scan")
    add("NEV-02", "nothing after 1992", "no model from inventory.denied; no modern phone, flat screen, cordless-drill or LED lamp in any inventory", "true", "none", allshops, "never", "inventory")
    add("FRN-01", "the front's parts at their sizes", "the 3.2 check's rows for the assembled bay (pilaster 350 slot / 290 shaft / 140 proud, console 240 x 205 x 550, fascia 5410 x 550 x 120, cornice 150, sill 75, stallriser 600, window frame at the shop's variant, transom 2400 to 2480, head 2790 to 2850)", "as 2.2's checks", "as 2.2's", allshops, "front", "check_shopfront.py rows that apply")
    add("FRN-02", "window and door zones", "u of the window, shop door and side door against front.zones_u_mm; their centres against front.centres_street_x_m", "equal", "2 mm; 3 mm", allshops, "front", "bounding boxes")
    add("FRN-03", "the shop door", "T1: leaf 900 x 2040 at z 28, glass 871 to 1973 with one bar at 1423 (28 wide), lock rail 549 to 871, letter plate 250 x 40 at z 678, lever side and hinge side as the table, the bell at z 1950 to 2050 inside; M1 and M2 as 2.2", "equal", "5 mm", allshops, "front", "bounding boxes")
    add("FRN-04", "the glass", "the number of lights and toplights per shop; 6 mm plate at d 30; no pane in front of another", "lights = n_mullions + 1; toplights = front.toplights_as_built (Rita's: nine, the 3.2 kit's departure D6; the 2.2 table says eight; the other fronts as front.glazing)", "exact", allshops, "front", "count")
    add("FRN-05", "paint colours", "the base colour of each painted part against front.paint_srgb", "within 6 levels per channel (aged paint: the 2.2 values)", "6", allshops, "front", "material values")
    add("FRN-06", "lobby", "the grocer's door recessed 600 and the launderette's 300, floors as 2.2", "equal", "5 mm", ["grocer", "steam_laundry"], "front", "bounding boxes")
    add("FAS-01", "the fascia's sign in place", "the 4.1 board texture on the fascia board (sample 12 points of the board's front: the render's base colour against the PNG at the same u, v); the applied sign (Mickey's letters, laundry and newsagent box, tea room panel) at the 2.2 u and z", "equal", "3 levels; 5 mm", allshops, "fascia", "render with the shop's light off; compare")
    add("FAS-02", "hanging signs", "Rita's three balls, the laundry's box, the ironmonger's and the chandler's boards at their 4.1 mounts", "equal", "10 mm", ["ritas", "steam_laundry", "ironmonger", "chandler"], "fascia", "bounding boxes")
    add("GLS-01", "nothing across the glass", "every object between the glass and the street plane is one of: the 4.1 glass rows, the OPEN/CLOSED sign, the hours plate, SB1 (newsagent), the letting board (empty unit), the night grille (Rita's) or mesh (chandler)", "true", "none", allshops, "glass", "scan")
    add("LIT-01", "lit shops lit at night, dark shops dark", "mean luma of the room-only composite (picture x brightness 0.7, glass reflection off) over the glass lights in STREET_SQUARE at night", "lit: >= 45; dark: 10 to 35; the difference between a lit shop and the same shop dark >= 25", "none", rooms, "night", "the cloud gate's render; lit = %s; dark = %s" % (", ".join(lit), ", ".join(dark)))
    add("LIT-02", "no black void in the street view", "mean luma of the room-only composite over the glass lights, by day, in STREET_SQUARE, STREET_30 and CLOSE_35", ">= 33 by day; >= 45 at night for the lit shops", "none", rooms, "composite", "the cloud gate's render; room-only = picture x 0.15 (day) or x 0.7 (night), tone-mapped Standard")
    add("LIT-03", "the empty unit is a pale blank by day, not black", "mean luma of the whitewashed glass in STREET_SQUARE by day", ">= 150 (4.1's whitewash 214,212,204 under the day light); by night <= 40", "none", ["empty_unit"], "composite", "the cloud gate's render")
    add("LIT-04", "Rita's grille at night", "the lattice over the window zone: bar 20 x 4, diamond 120, rails 40 x 40 at z 2.50 and 0.70, plane 100 in front of the glass; the lit window seen through it", "equal", "5 mm", ["ritas"], "night", "bounding boxes and the night render")
    add("CAM-01", "the cameras are the named ones", "each render's camera against cameras.definitions and the shop's eye and aim", "equal", "5 mm; 0.1 degree", rooms, "camera", "read the render's camera")
    return C


def merge(t):
    n_models = len(t["inventory"]["polyhaven"])
    n_scripted = len(t["inventory"]["scripted"])
    t["summary_line"] = ("Shop windows: ten units as built (twelve not found); eight rooms of %d checked CC0 models and %d named scripted forms, rendered 4096 wide to the game's own `trace` rule, "
                         "stock only where that rule can show it and the near 0.55 m a real display; the fish scans wait on one login." % (n_models, n_scripted))
    for fl in FAILURES:
        if isinstance(fl["answer"], str):
            fl["answer"] = fl["answer"].replace("105 Poly Haven models", "%d Poly Haven models" % n_models).replace("52 kinds", "%d kinds" % n_scripted)
    for s_ in SOURCES:
        s_["what"] = s_["what"].replace("each of the 105 models used", "each of the %d models used" % n_models)
    t["sources"] = SOURCES
    t["unreached"] = UNREACHED
    pm = json.loads(json.dumps(PHOTO_MEASUREMENTS))
    rr = {r_["what"]: r_ for r_ in pm["rows"]}
    top_, bot_ = rr["door leaf top (underside of the transom's board)"]["y_px"], rr["door leaf bottom / threshold"]["y_px"]
    k_ = 2040.0 / (bot_ - top_)
    def zz(w_):
        return round((bot_ - rr[w_]["y_px"]) * k_ + 28.0, 0)
    pm["derived_mm_from_the_leaf_height_2040"] = {"mm_per_pixel": round(k_, 4), "heights_above_the_footway_mm": {w_: zz(w_) for w_ in ("glass top", "glazing bar, centre", "glass foot", "letter plate, centre", "number plate, centre", "handle, centre", "lower panel field, top", "lower panel field, bottom", "stallriser top (tile cap)")},
                                                  "leaf_width_mm": round((rr["leaf right edge"]["x_px"] - rr["leaf left edge"]["x_px"]) * k_), "glass_width_mm": round((rr["glass right"]["x_px"] - rr["glass left"]["x_px"]) * k_),
                                                  "error": "+-3 px = +-18 mm a row, plus the assumption that the leaf is 2040 high (a 2100 leaf moves every height by 3 per cent)"}
    t["photographs"] = pm
    t["disagreements_photographs_win"] = DISAGREEMENTS
    t["previous_failures_answered"] = FAILURES
    t["reuse"] = REUSE
    t["could_not_settle"] = COULD_NOT_SETTLE
    t["needs_you"] = NEEDS_YOU
    t["checks"] = checks(t)
    # the parallax test per shop: the predicted shift of the back wall's centre point between the two close cameras
    import sw_common as S
    scene = S.load_scene()
    for s in t["shops"]:
        if not s.get("room"):
            continue
        card = S.card_of(scene, s["block"], s["bay"])
        D = s["room"]["d"]
        res = {}
        for cn in ("CLOSE_35", "CLOSE_35_B"):
            import numpy as np
            wc = s["front"]["centres_street_x_m"]["window"]
            eye, _ = S.camera_pose(cn, card, wc)
            # the game's trace on a card of this side: the eye and the point in the card frame; for a west card trace's own side=-1 rule applies
            side = card["side"]
            ec = S.to_card(eye, card)
            P = np.array([S.W / 2.0, 0.0, S.H / 2.0])                       # the card's centre
            u, v = S.trace(tuple(P), tuple(ec), (S.W, S.H, D), S.CAMERA_D, side)
            res[cn] = [u, v]
        du = (res["CLOSE_35_B"][0] - res["CLOSE_35"][0]) * 4096.0
        s["parallax_test"] = {"point": "the card's centre", "u_v_close_35": [round(x, 5) for x in res["CLOSE_35"]], "u_v_close_35_b": [round(x, 5) for x in res["CLOSE_35_B"]], "expected_du_px": round(du, 2),
                              "rule": "tools/ue/make_interior_material.py trace(), side %+d, card frame" % (1 if s["side"] == "east" else -1)}
