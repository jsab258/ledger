"""The prose half of the target as data: sources, what the kit gets right and what changes, the
photographs-win disagreements, joints, fixings, meets, wear, what could not be settled. Read by
make_target.py. Evidence kinds: Read (printed in a source), Scaled (measured off a drawing or the
project's own files), Photo (measured on a photograph today, method and error given), Derived,
Judgement. Millimetres."""

SOURCES = [
    {"id": "P1", "what": "Leadenhall Market, a 360 degree HDRI (16384 x 8192), re-projected here to a level rectilinear elevation of the arcade's right-hand wall (yaw 90, focal 2400 px)",
     "url": "https://polyhaven.com/a/leadenhall_market; files: https://api.polyhaven.com/files/leadenhall_market (16k .hdr read 2026-10-09 from dl.polyhaven.org)",
     "read": "2026-10-09 (this cloud reached polyhaven.com and its file host)", "author": "Andreas Mischok", "licence": "CC0 (Poly Haven)",
     "taken": "2019-05-19", "shows": "heritage-restored Victorian covered market fronts (built c.1881, from memory, not checked): stone- or render-faced pilasters on stepped plinths, pier caps under a fascia, a deep cornice, heavy teal-painted window frames with a mid transom, a cast-iron ornament band over the head, cast-iron lattice stallrisers in frames, red double doors with a brass foot strip",
     "period": "NOT a 1990 object and not a provincial parade: a 2019 restoration of a London arcade (built c.1881, from memory). Used for proportions and the order of mouldings only, never for colour or wear. Why it still serves: it is the only reached photograph of a Victorian British shopfront in joinery and masonry at a measurable scale, and the parts it shows (plinth, shaft, necking, capital, fascia field, crown, sill, stallriser frame, transom, mullion, door) are the parts of a 1900-1935 parade front; the ratios between them are tested against the street's fixed numbers in section 4 of TARGET.md",
     "used": "Yes, measured: 43 rows and columns and one notice (photo_measurements.json), 6 joinery-only previews. Lettering (house numerals) is masked; the unmasked views carry real businesses' names and notices and were never saved into the repository",
     "scale": "fitted on ONE dimension: an A5 notice (148 x 210 mm) on the shop door's glass, 78.35 x 108.90 px; the door plane is 1.104 times farther than the pilaster's front plane (the foot rows 604.1 and 547.0); the camera stands about 1.04 m above the footway"},
    {"id": "P2", "what": "Poly Haven CC0 roller-shutter models (rollershutter_window_01, _02, _03, rollershutter_door): glTF read today",
     "url": "https://polyhaven.com/models (files by https://api.polyhaven.com/files/<id>)", "read": "2026-10-09", "author": "MP (Poly Haven), published 2023-10-11", "licence": "CC0",
     "taken": "scanned or modelled 2023", "shows": "a steel hood, guide rails and a slatted curtain; hood depth 153, 168, 300 and 300 for curtains 1546, 1561, 1851 and 2400 high",
     "used": "Yes, for the roller-shutter box's depth and the rail width (alterations.roller_shutter); the form, not the date"},
    {"id": "K", "what": "the existing shopfront kit: production/art/shopfront-kit/README.md and tools/art-recipes/shopfront-kit/*.py (6 October 2026, by script)", "read": "2026-10-09", "author": "studio", "licence": "own",
     "shows": "the parts' sizes and profiles as built and the bay's datum", "used": "Yes: the starting point; every change is listed in kit_vs_target"},
    {"id": "F", "what": "production/research/shopfronts/FRONTAGE-2026-10-06.md (the project's earlier reading: council guides, Historic England entries, Building Conservation Directory, Ellis 1902 Modern Practical Joinery)", "read": "2026-10-09 (this file), its sources were read on the PC on 6 October",
     "author": "studio", "licence": "own", "shows": "anatomy, colours, wear, the four points where research differs from the spec", "used": "Yes, cited as the project's earlier reading, NOT re-read at source"},
    {"id": "W", "what": "production/research/shop-window-interiors/ (NOTE.md, FISHMONGER-2026-10-03.md ...), production/research/street-wear/PAINTED-FRONTS-2026-10-07.md, production/reference/photographs.md", "read": "2026-10-09",
     "author": "studio", "licence": "own", "shows": "what the period photographs establish: metal shopfronts beside older frontage, patterned tile stallrisers, recessed doorways with tiled thresholds; white tiles and slabs in fish shops; where a front wears", "used": "Yes, cited"},
    {"id": "S", "what": "SCENE-SLOTS.md, canon.md, RULINGS.md, production/specs/terrace-fronts.md, production/art/fascia-01/*, production/cloud-week/targets/fascia-signs/target.json, production/cloud-week/targets/front-door/target.json, tools/art-recipes/terrace-front.py (paints, refits, doors_on), production/previews/*.jpg (Rita's day and night, the kit sheet, the whole fronts, the Hook sheet)", "read": "2026-10-09",
     "author": "studio", "licence": "own", "shows": "the street's fixed numbers, the trades, the fascia's board and cornice, the F1 side door, the door ends, the paints", "used": "Yes"},
]

UNREACHED = [
    "Wikimedia Commons and Geograph (the period and modern photographs of British shopfronts; 403 or no route today)",
    "archive.org (Ellis, Modern Practical Joinery, 1902, and other books; no route)",
    "historicengland.org.uk (list entries 1488333, 1393627; no route)",
    "buildingconservation.com, the council guides (Brighton and Hove, Coventry, Westminster, RBKC, Cornwall, Richmond, Dover), Wikipedia, Gutenberg, HathiTrust, Google (no route)",
    "Flickr, Peter Marshall's Hull set, Picture Sheffield (the project's earlier reading of them is cited, not re-checked)",
]

WOULD_READ = [
    "Historic England 'Shopping Parades' (Introductions to Heritage Assets) and its Commerce and Exchange listing guide: the sections of surviving 1900-1935 consoles, cornices and pilasters, with dimensions",
    "Ellis, Modern Practical Joinery (1902), the shop-front plates: stile, mullion and transom sections, sill sections (the 'stout sill'), the cornice's limits in inches",
    "Geograph and Commons photographs, 1975-2000, of provincial British shopfronts: scrolled consoles and their leaves, 1970s aluminium fronts and their cover caps, roller-shutter boxes, plastic box signs over old fascias, recessed lobbies with tiled floors, whitewashed empty units (each with author, licence and date read on the file page)",
    "Peter Marshall's Hull photographs (R05, R09, West Dock Cafe, 1981) at the page: the metal front's section widths, the patterned tile's repeat",
    "A real surviving 1920s provincial front's measured drawing (a council's survey, or the Building Conservation Directory's 1994 'Retail Detail')",
    "Manufacturers' 1980s sections for aluminium shopfronts (the extrusion widths: 50 and 75 are Judgement here)",
]

KIT_VS_TARGET = {
    "pilaster": {
        "kit_gets_right": ["plinth, shaft, capital in that order, as every source and P1 show", "shaft 290 wide; 350 at the plinth and the capital's top, which makes the party-wall pair stand 0.70 m wide",
                           "panelled and fluted shafts as the period's timber types", "a necking bead, a die with a raised tablet, a cap moulding", "the backing core, so no daylight shows between pilaster and frames"],
        "target_changes": [
            {"what": "plinth top 600 -> 800", "reason": "P1: the plinth's top stands 1.27 times the sill's top (1.12 m against 0.88 m at the measured scale) and 0.228 of the front's height; scaled to this street's 3.55 m that is 0.81. RBKC (the earlier reading, KC) wants the stallriser not above the pilaster's base: the sill then lands inside the plinth's height", "kind": "Photo"},
            {"what": "shaft projection 100 -> 110", "reason": "P1: the shaft's right return measures 30.8 px at 1087 px from the axis: 118 mm +-14", "kind": "Photo"},
            {"what": "capital 330 -> 310 high", "reason": "P1: neck to the top of the abacus is 174 px, 1.04 times the shaft's width: 301 mm +-24 at the measured scale", "kind": "Photo"},
            {"what": "a stepped plinth variant (render), a flush clad variant (Mickey's, as built)", "reason": "P1 shows four stepped members on the plinth; the Hook sheet and the street show Mickey's piers flat and plain", "kind": "Photo and Sheet"},
            {"what": "the capital's flare (a hollow echinus 90 high) and an optional three-boss die", "reason": "P1 shows the die with three roundels under a flared cap; the kit's cap is a straight moulding", "kind": "Photo"},
        ],
    },
    "console": {
        "kit_gets_right": ["the 240 x 180 x 550 envelope of the street's built mesh and its toe 60 deep standing on the capital's top", "the console centred on the pilaster, gap 0.0 mm"],
        "target_changes": [
            {"what": "the S curve smoothed (53 points) and given a volute on each side face and an acanthus leaf on the face", "reason": "the built mesh is a few flat steps (README: coarse beside the kit); the brief asks for the scroll and its leaf; NO photograph of a scrolled console was reached", "kind": "Judgement"},
            {"what": "a plain block variant (the grocer) and an absent variant (the empty unit's left console)", "reason": "1930s fronts; fascia-01 spec", "kind": "Judgement"},
        ],
    },
    "fascia_board": {
        "kit_gets_right": ["the board between the consoles, 295 to 5705, 120 proud, z 2850 to 3400 (the fascia target's)"],
        "target_changes": [{"what": "a 40 high bed mould at the foot, 12 proud of the face", "reason": "P1 shows the fascia field framed by a mould where it meets the capital; the board's foot would otherwise be a bare box edge on the abacus", "kind": "Photo"},
                           {"what": "the face stays vertical", "reason": "P1 shows a vertical field; the guide's 'sloped slightly forward' (Coventry, the earlier reading) is a book and the photograph wins (D6)", "kind": "Photo"}],
    },
    "cornice": {
        "kit_gets_right": ["215 deep x 150 high x 5892 long, the drip groove outside the board's face, the wash, the lead apron (not geometry)"],
        "target_changes": [{"what": "the profile redrawn with a tall corona face (52, 0.35 of the height), two fillets, a cyma reversa and a cap ovolo (19 points) inside the same envelope", "reason": "the built profile has 12 points and one curve; P1 shows a crown of several members", "kind": "Photo"},
                           {"what": "the 150 height is KEPT although P1's crown is 0.86 of its fascia field where the street's is 0.27 (about three times)", "reason": "the fascia target fixes the cornice top at 3.55 and the hanging signs' brackets at 3.60 over it; an optional tall cornice (300) is recorded in variants for the reviewer to overturn", "kind": "Photo not followed, stated"}],
    },
    "sill": {
        "kit_gets_right": ["a weathered top falling to a rounded nose with a throat, 150 proud, 600 high"],
        "target_changes": [{"what": "50 thick -> 75 thick (z 525 to 600) with the throat 16 back from the nose", "reason": "Ellis (the earlier reading) calls the stallboard 'the stout sill' (no figure); P1's sill group is 80 px (142 mm) deep with a bead, a wide cove and a soffit; a 50 mm sill reads as a ledge; 75 is Judgement", "kind": "Read and Photo"}],
    },
    "stallriser": {
        "kit_gets_right": ["panelled (raised and fielded, 3 panels) and glazed-tile variants, 600 high, face 125", "the plinth, skirting 120"],
        "target_changes": [{"what": "six more variants: square tile, patterned tile, glass slab, render, boarded, and a grille (available, unused)", "reason": "the ten fronts need them: P1 shows a framed grille panel, and the earlier reading of R05 a patterned tile", "kind": "Judgement and Photo"}],
    },
    "window_frame": {
        "kit_gets_right": ["sill 600 to head 2850, transom 2400 to 2480, mullions in front of the glass, glass 30 in front of the wall", "toplights in a shallow row", "the transom's weathered top, drip and nose (a book detail, also seen in P1)"],
        "target_changes": [{"what": "mullion 55 -> 70 wide, front at 92 (62 in front of the glass)", "reason": "P1's mullion is 92 px wide (164 mm at the wall plane) against a 1.0 m light: 0.16 of the light, the kit's 0.05. The guides' 40 to 70 mm is a projection. Not followed in full (D5)", "kind": "Photo, partly followed"},
                           {"what": "a bottom rail 90 high on the sill; glazing beads; four more types: T2, M1, M2", "reason": "P1's stallriser frame carries a bottom rail and the lights stand on it; the street needs timber, aluminium and 1930s bronze fronts", "kind": "Photo and Judgement"}],
    },
    "shop_door": {
        "kit_gets_right": ["leaf 900 x 2040, frame 1006 wide, 100 deep, kick plate, letter plate, lever handles, three hinges, terrazzo threshold"],
        "target_changes": [{"what": "glazed from 1000 -> 700", "reason": "P1's door is glazed from 0.328 of its leaf's height (0.86 of 2.62 m); the books say two-thirds glazed (0.6 to 0.7 m): the photograph and the books agree and the scene's 1.0 is a trade-standard guess. The door's lower portion is then bottom rail 230, panel 360, lock rail 110", "kind": "Photo and Read"},
                           {"what": "a 30 high brass foot strip across the leaf", "reason": "P1's door foot carries one (15 px, 29 mm)", "kind": "Photo"},
                           {"what": "aluminium and bronze door variants", "reason": "the refits", "kind": "Judgement"}],
    },
    "side_door": {"kit_gets_right": ["the 944 slot, the fielded panel over the transom"], "target_changes": [{"what": "the leaf is the front-door family's F1 (not re-targeted)", "reason": "the brief", "kind": "Read"}]},
}

DISAGREEMENTS = [
    {"id": "D1", "element": "plinth height", "book_or_scene": "kit and scene: the plinth equals the stallriser, 600", "photograph": "P1: plinth top 0.228 of the front's height, 1.27 times the sill's top", "chosen": "800 (the photograph scaled to 3.55 m is 811)"},
    {"id": "D2", "element": "shop door glazed from", "book_or_scene": "scene C8: 1.0 m", "photograph": "P1: 0.328 of the leaf (0.67 m on a 2.04 leaf); books 0.6 to 0.7 m", "chosen": "700 (photograph and books agree, the scene loses)"},
    {"id": "D3", "element": "shaft projection", "book_or_scene": "scene: 100", "photograph": "P1: 118 +-14", "chosen": "110 (inside both)"},
    {"id": "D4", "element": "capital height", "book_or_scene": "kit: 330", "photograph": "P1: 301 +-24", "chosen": "310"},
    {"id": "D5", "element": "mullion width", "book_or_scene": "kit 55; Cornwall guide: projecting 40-70 from the glass (a projection, not a width)", "photograph": "P1: 164 mm face against a 1.0 m light", "chosen": "70 (T1), 80 (T2): the photograph is a heavy plate-glass arcade front; not followed in full. If the reviewer reads the photograph as authoritative, 100 to 120 is the next step"},
    {"id": "D6", "element": "fascia face", "book_or_scene": "Coventry 2014 (the earlier reading): sloped slightly forward", "photograph": "P1: vertical", "chosen": "vertical"},
    {"id": "D7", "element": "cornice height", "book_or_scene": "fascia-01: 150; Ellis (the earlier reading, in the London rules of about 1902): a cornice may PROJECT 13 in (330) in a street up to 30 ft wide and 18 in in a wider one (a limit on projection, not height; ours projects 215)", "photograph": "P1: the crown (fillet to cap, measured at the continuous run) is 446 mm, 0.86 of the 505 mm fascia field; the street's 150 over 550 is 0.27", "chosen": "150 kept (the fixed envelope); variant 'tall' 300 offered. The photograph is NOT followed here and this is stated"},
    {"id": "D8", "element": "sill thickness", "book_or_scene": "kit: 50", "photograph": "P1: the sill group 140 deep with a bead, cove and soffit; Ellis: stout sill", "chosen": "75"},
    {"id": "D9", "element": "stallriser height", "book_or_scene": "scene 600; guides 400 to 700", "photograph": "P1: sill top 0.18 of the front's height, 0.64 m at 3.55", "chosen": "600 (no disagreement)"},
    {"id": "D10", "element": "the pilasters in pairs at the party wall", "book_or_scene": "scene: a pier at every bay edge (two 0.35 piers butt)", "photograph": "P1 has single piers between shops", "chosen": "pairs kept: the scene is a fixed fact of the street and a parade of separately owned shops did have a pilaster each; they butt with a painted vertical joint"},
    {"id": "D11", "element": "the scrolled console", "book_or_scene": "the brief and the earlier reading: consoles are scrolled brackets", "photograph": "P1's pier caps are straight stepped blocks, not scrolls: the photograph does not show the part", "chosen": "scroll by Judgement; stated as not established by a photograph"},
]

JOINTS = [
    {"between": "pilaster shaft and plinth", "how": "the shaft stands on the cap's flat; a 3 mm shadow line at the foot where paint has filled the gap; the base mould (a small ogee 25 x 60 in the kit) is dropped: P1 shows none, the plinth's cap takes the shaft directly (Photo)"},
    {"between": "pilaster pair at the party wall", "how": "two 350 piers butt at u = 0 / 6000: a vertical joint 2 mm wide, paint-cracked, 0 to 2850; capitals touch; plinth caps touch. The shafts (290 in a 350 slot) stand 60 apart across the party line. The D5 downpipe (68 across, axis 94 from the wall, so d 60 to 128) stands in that gap, 18 proud of the shafts' faces (110); the plinths and the capitals are notched for it by a chase 76 wide (u +-38) from d 50 to their fronts (z 0 to 800 and 2540 to 2850); the cornice stops 54 short of each side and the consoles stand 110 apart, so the pipe passes all the way up"},
    {"between": "console and capital", "how": "the toe 240 x 60 stands on the abacus's top at z 2850, centred on u 175 / 5825; 0.0 mm gap; two 12 mm hardwood dowels 40 deep from the toe into the capital; two M10 coach screws through the console's back into the wall plate (hidden)"},
    {"between": "fascia board and console", "how": "the board's ends are let into the consoles' inner sides by a 12 mm rebate; a 2 mm paint-filled line shows on each side"},
    {"between": "fascia board and capital", "how": "the board's foot rests on the abacus for 55 (u 295 to 350 and 5650 to 5705) and its bed mould overhangs the abacus's top front by 2"},
    {"between": "cornice and fascia", "how": "the soffit lies on the board's top and the consoles' tops at z 3400 with 0 gap; the drip groove at d 155 to 175 lies outside the board's face (120) by 35; a lead apron over the wash, 100 up the wall"},
    {"between": "cornice and the party wall", "how": "the cornice stops 54 short of each party line (u 54 and 5946) leaving a 108 gap between neighbours for the downpipe"},
    {"between": "window frame and sill", "how": "the bottom rail (z 600 to 690) stands on the sill's flat bed (d 0 to 60), screwed from below through the sill; a mastic line at the junction (1 mm)"},
    {"between": "window frame and pilaster / door frames", "how": "the end jambs (50 x 95) close against the pilaster's backing core and the door frames' jambs; a 3 mm paint joint; no daylight"},
    {"between": "transom and jambs", "how": "the transom is housed 10 mm into each jamb with a stub tenon, drawbore-pegged inside; outside only a 1 mm line shows"},
    {"between": "mullions and transom/bottom rail", "how": "mortice and tenon, 25 mm tenon, wedged; end grain not visible after painting; the mullion stops at the transom (z 2400) and the toplight bars start on it"},
    {"between": "stallriser and plinths", "how": "the stallriser's ends butt the plinths' sides; the plinth is 25 proud of the stallriser face and 0 to 25 of the sill's nose; a 2 mm line"},
    {"between": "sill and plinth", "how": "the sill's ends are cut round the plinth's cap and stop 3 short of the plinth's side"},
    {"between": "shop door frame and threshold", "how": "the terrazzo threshold (25 high) runs the frame's width; the leaf clears it by 3 mm over a brass foot strip"},
    {"between": "side-door slot and the shop door frame", "how": "the F1 frame's jamb and the shop door's jamb stand 3 apart under a common head strip; the transom runs across both"},
    {"between": "box sign / flat panel and the old board", "how": "stands on the board at the fascia target's outer rectangle; eight pan-head screws; the cornice's soffit clears its top by 35"},
]

FIXINGS = [
    {"part": "pilaster", "fixing": "100 mm cut nails or No. 10 screws through the core into wall plugs at 600 pitch; heads punched and stopped; after repainting they show as faint round dots 4 mm across at 600 in two lines 40 from the edges (Judgement)"},
    {"part": "console", "fixing": "two 12 mm dowels and two M10 coach screws, hidden; a rust bleed 20 mm long under each screw hole on the shaded side after 70 years (Judgement)"},
    {"part": "fascia board", "fixing": "50 mm cut nails at 300 along the top and bottom edges into the rails; heads stopped; the fascia target puts ten pin holes along a removed sign"},
    {"part": "cornice", "fixing": "75 mm brass or galvanised screws through the soffit into the wall plate at 450, pellet-plugged and painted; the lead is fixed with copper clout nails at 25 along its upper edge, pointed into the brick"},
    {"part": "window frame", "fixing": "100 mm screws through the end jambs into the pilaster core at 450; the sill screwed down through its bed (No. 12 at 450, plugged); beads on brass round-head screws at 250 (T1), snap-in (M1)"},
    {"part": "stallriser", "fixing": "panels screwed from behind into the sill and the plinth; tile on a cement-sand screed on battens; slabs on a stainless or brass clip at 400"},
    {"part": "doors", "fixing": "three 100 x 75 butt hinges, 6 No. 8 screws each; a mortice lock and a rim night latch; the kick plate with 8 brass screws; the F1 door as its own target"},
    {"part": "seen on P1, not adopted", "fixing": "P1's pilaster shows two small iron hooks on its side return (a later fixing for a flag or a banner) and a bracket-like fixing on the shaft's right edge; the 1990 street hangs its signs from brackets on the brick above the cornice (the fascia target), so none is placed on the shafts"},
    {"part": "roller-shutter box", "fixing": "four M8 bolts per rail through the frame into the pilaster core; the hood on steel angle brackets screwed into the fascia's rail, 600 pitch; rivets on the end caps"},
]

WEAR = {
    "photo_P1_2019": "Fine white scuffs on the red plinth up to about 0.4 m, chipped arrises at the cap's edges, the sill group's bead and cove carrying bright worn lines where paint has worn through, the brass foot strip worn, a repaired patch on the plinth's foot. P1 is a 2019 restoration in fresh gloss: it shows what wear looks like on a part, not what 1990 looked like",
    "earlier_notes_1990": "FRONTAGE-2026-10-06.md section 3 and PAINTED-FRONTS-2026-10-07.md: paint failing at the sill and the joints, pilaster feet rotting and splashed, stallrisers stained by pavement splash up to 0.45 m, door bottoms decaying, fascias rotting from their backs; the wear layer's work (a height gradient and noise in the material), not the meshes'. The wear target (production/cloud-week/targets/wear) governs it",
    "geometry_wear_in_this_target": ["arris radius 1 to 2.5 mm on every timber edge by repainting", "a 3 mm V of rot at the pilaster foot's front arris on the oldest fronts (empty unit, ironmonger)",
                                     "the empty unit's console stub", "cracks 0.5 x 80 in a tile or slab at doors on the tiled fronts (tile and slab stallrisers)",
                                     "aluminium: pits and a white corrosion bloom at the foot, 40 to 60 high"],
}

COULD_NOT_SETTLE = [
    "No photograph of a provincial 1900-1935 shopfront was reached (Wikimedia, Geograph, Flickr, archive.org and the council guides all refused). P1 is a London arcade (c.1881, from memory) restored in 2019: it governs proportions and the order of mouldings; it does not govern timber panel layouts, fluting, console scrolls or leaves, aluminium sections, roller-shutter boxes, box signs, lobbies or whitewashed empty units. Those rest on the earlier notes (cited, not re-read) and Judgement, each marked",
    "The scrolled console and its leaf (the volute, the acanthus): no photograph at all. The silhouette keeps the street's built envelope; the volute and leaf are Judgement",
    "The 1960s-80s aluminium front's sections (50 x 75, cover caps, mastic joints): Judgement; R05 and R09 only say such fronts existed",
    "Absolute scale of P1: the A5 notice is assumed to be A5 (148 x 210); its plane ratio to the pilasters (1.104) assumes the door foot and the plinth foot are at the same footway level. The scale is +-8 per cent and every Leadenhall millimetre carries it. Ratios do not",
    "Mickey's door: mickeys-office.json puts it at street x 4.65 (the rank spot, the unlock distance); the kit's slots put the shop door's centre at x 4.797, 147 mm farther from the party wall, because the side door slot is 944 and the shop door slot 1006. Rita's front already stands so. A town question (move the door x or narrow the side door's slot)",
    "The fascia target puts a street number on every side door's fanlight (the grocer's at x 38.18); the street recipe and terrace-fronts.md give the grocer no side door (BAY_WITHOUT_SIDE_DOOR = 5). This target follows the recipe; the number belongs on the shop door's fanlight (x 38.147). A fascias question",
    "The ironmonger: the street recipe makes it a metal refit (SHOPFRONT_REFITS west_north 1); this target keeps it timber to suit its traditional board. A town or art question",
    "Twelve fronts or ten: RULINGS 2 Oct counts twelve; the scene has ten shop bays (six east, the chandler, three west). Ten are tabled. A coin shop at x 39 (hook-cast) is not in the scene",
    "The Hook sheet shows a recessed Mickey's door and an angled display bay at the corner; the street's Mickey's is a flat front with its door and room walked in the game. This target keeps it flush (as built) and gives the recess to the grocer and the launderette",
    "The party-wall downpipe: the 6 October note says it goes 'inside the hollow pilaster'; at the roofline's 94 mm offset it cannot (the shaft is 110 proud and the pipe's front stands at 128). This target leaves the pipe where the roofline has it, in the 60 mm gap between the two shafts and a 76 mm chase through the plinths and capitals; the roofline owner may prefer to move the pipe back",
    "Texture size, UVs, material slots and vertex-colour masks are the builder's (the kit's method stands); nothing here changes them",
    "Nobody has looked at these parts at the game's exposure and internal resolution; what is visible at 8 m is not judged",
]


# which numbers rest on what (the brief: photographs measured today, the earlier notes, judgement)
EVIDENCE = {
    "pilaster": {"photo_today": ["plinth top 800 (ratio to the front's height 0.228 and to the sill 1.27)", "shaft 290 wide (290.1 +-8 per cent at the measured scale)", "shaft proud 110 (118 +-14)", "capital 310 (301 +-24)", "the order of members: stepped plinth, shaft, necking ledge, die, flare, abacus", "the three-boss die (optional)"],
                 "earlier_notes": ["panelled and fluted timber types; plinth at least the stallriser's height (RBKC); 0.35 slot and 0.10 proud (the scene)", "the pairs at the party wall (scene, DOWNPIPE note)"],
                 "judgement": ["every moulding's profile (astragal r 12, flare hollow, ovolo), the sunk panel's depth 12 and bead 10, the flutes' 12, the stepped plinth's set-backs, the clad variant's sheets", "the downpipe chase"]},
    "console": {"photo_today": [], "earlier_notes": ["envelope 240 x 180 x 550 and the S silhouette of the built mesh (fascia-01)", "consoles at each end of the fascia on the capitals (FRONTAGE: CV, KC, CW)"],
                "judgement": ["the smoothing, the volute, the acanthus leaf, the block variant", "NO PHOTOGRAPH of a scrolled console was reached"]},
    "fascia_board": {"photo_today": ["vertical face; a field with a mould where it meets the capital"], "earlier_notes": ["5410 x 550 x 120 (fascia target, kit)", "not more than 600 and a fifth of the front (CV, RI)"], "judgement": ["the bed mould's 40 x 12", "board thickness 25"]},
    "cornice": {"photo_today": ["a crown of several members (cyma, corona, fillets)"], "earlier_notes": ["215 x 150 x 5892, the drip groove, the 27 degree wash, the lead (fascia-01)"], "judgement": ["the 19-point profile's member sizes"]},
    "sill": {"photo_today": ["a deep sill group (140 mm: bead, cove, soffit) over the stallriser's frame; sill top 0.18 of the front (0.64 m at 3.55 m; the scene's 600 is 6 per cent under)"], "earlier_notes": ["weathered top, drip, cill 'substantial' (BH, CW); Ellis's stout sill 3 in"], "judgement": ["75 thick, the throat 6 x 6, the weathering 15 degrees"]},
    "stallriser": {"photo_today": ["a framed panel under the sill, a bottom rail above the foot (P1: a cast grille panel, 580 high)"], "earlier_notes": ["600 and 0.15 proud (scene); panelled, glazed tile, render; patterned tile and plain glazed tile on metal fronts (R05, R09); white tile and slab in fish shops"], "judgement": ["tile sizes and courses, the 2 x 2 pattern, the slab, the boarded sheet"]},
    "window_frame": {"photo_today": ["a mid transom bar and a heavy mullion (164 mm, 0.16 of the light): partly followed", "stile 145 mm: not followed"], "earlier_notes": ["sill 600 to head 2850, transom 2400 to 2480, toplights, mullions 40-70 proud of the glass, glass 30 forward (scene, kit, CW)"], "judgement": ["every section's size and shape (T1, T2, M1, M2), bead sizes, bar positions, toplight counts"]},
    "shop_door": {"photo_today": ["glazed from 0.328 of the leaf (700 on 2040)", "a 30 mm brass foot strip"], "earlier_notes": ["900 x 2040, frame 1006, kick plate, letter plate, levers, hinges (kit); 'two-thirds glazed' (BH); bottom rail 9 in (Ellis)"], "judgement": ["rail and stile widths, the lock rail, furniture heights, the aluminium and bronze leaves"]},
    "side_door_slot": {"photo_today": [], "earlier_notes": ["the front-door family's F1 (its own photographs P2 and the books)"], "judgement": ["the mapping into the bay (d 100, z + 45, the trimmed head and threshold)"]},
    "lobby": {"photo_today": [], "earlier_notes": ["recessed lobbies with terrazzo or tiled floors (CW, HE1, HE2); a recessed doorway and tiled threshold in Marshall's West Dock Cafe (R05 reading)"], "judgement": ["the depths 600 and 300, the returns, the floors' patterns"]},
    "alterations": {"photo_today": ["roller-shutter hood depth (150 to 300) and rail width from CC0 scans (P2)"], "earlier_notes": ["metal fronts, patterned tile, letting boards, whitewash (R05, R09, DECISIONS 3 Oct)"], "judgement": ["every section size, every colour, the box sign and flat panel depths (the fascia target's)"]},
}
