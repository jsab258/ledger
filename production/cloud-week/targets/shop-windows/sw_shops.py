"""The ten shops' rooms, displays and lights as data (author tool; make_target.py reads it and writes target.json).

Room frame (as tools/art-recipes/shop-room.py): x across with 0 at the card's centre and +x the PICTURE's right (-2.65 .. +2.65), y back from
the card (0 .. D), z up from the box floor (0 .. 2.4; the floor is the card's bottom, 0.65 above the crown). Display frame: u from the window
zone's viewer-left edge (metres, 0 .. window length), v out from the back of the glass (0 .. 0.55), w above the bed (0.70 above the crown).

A fixture stands on one surface and has a depth (its stand-off): the self-check holds it to the budgets that the game's own `trace` gives
(sw_common.standoff_table): a fixture is "true" up to the 20 px budget, "tolerated" up to the 40 px budget, else it is refused.
A goods line is a model id from Poly Haven (checked by make_target.py against api.polyhaven.com), or "script:<name>" for a thing that is
made by script because no CC0 model exists (the line says why). `size` is the largest side as placed (m); None means the model's own size.
"""

D_ROOM = 4.5
HALF_W = 2.65


def fx(id_, surface, what, depth, x=None, y=None, z=(0.0, 2.4), kind="fixture", **kw):
    d = {"id": id_, "surface": surface, "what": what, "depth_m": depth, "x": list(x) if x else None, "y": list(y) if y else None,
         "z": list(z), "kind": kind}
    d.update(kw)
    return d


def gd(model, n, on, size=None, note="", why=None):
    d = {"model": model, "n": n, "on": on, "size_m": size, "note": note}
    if why:
        d["why"] = why
    return d


def di(model, n, zone, size=None, note="", why=None):
    """zone = [u0, u1, v0, v1, w0, w1] in the display frame (m)."""
    d = {"model": model, "n": n, "zone": list(zone), "size_m": size, "note": note}
    if why:
        d["why"] = why
    return d


# ======================================================================================================================================
# THE ROOMS
# ======================================================================================================================================
SHOPS = {}

# ---- 2 RITA'S, the pawnbroker (spec id pawnbroker) -------------------------------------------------------------------------------
SHOPS["ritas"] = {
    "spec_id": "pawnbroker", "room_D": 4.5, "needs_room": True,
    "keeps": "the room's box and finishes (old brown lino, cream plaster over a 1.0 m brown dado, three T12 battens), the stocked back wall, the "
             "ticketed goods, the notices, the three approved pictures' look, the display glb and its 23 Poly Haven models",
    "changes": "the glass counter 2.4 m out in the room goes to the back wall (it stood 2.1 m off it and smeared); the units down BOTH side walls "
               "(0.40 deep, goods 0.4 off the wall) become flat boards (pegboards and framed notices); the grandfather clock and the vintage cabinet "
               "(0.8 and 0.67 deep) go; the doormat stays flat; pictures 4096 wide; the maker-marked models are blanked or dropped",
    "floor": {"material": "Poly Haven old_linoleum_flooring_01, tint (0.62, 0.55, 0.50), 1.2 m tile, worn path darker by hand-painted mask", "base": (76, 64, 48)},
    "walls": {"above": "Poly Haven painted_plaster_wall tint (0.95, 0.86, 0.66), 1.5 m tile", "dado": "same plaster tint (0.42, 0.27, 0.17) to z 1.0 m"},
    "ceiling": "plaster off-white (180, 173, 158)",
    "lights": {
        "day": "daylight through the front opening (overcast sky area light 5.3 x 2.4 m on the card plane, 6500 K) PLUS the three battens on: the shop is open "
               "(Mon, Tue, Thu to Sat 9 to 17:30, Wed 9 to 13)",
        "night_lit": "the three T12 battens only (cool white 4000 K, 5 ft, 38 mm), no sky: the window is lit all night (RULINGS 1 Oct)",
        "night_dark": "a faint sodium wash through the front (linear colour (1.0, 0.7055, 0.0), 6 per cent of night_lit's energy) and one back-room night "
                      "light through the ajar back door (2700 K, 0.3 m wide strip); rendered although Rita's is lit, so the spec has all three states",
        "tubes": [{"x": 0.0, "y": 1.0, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 2.0, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 3.0, "z_below_ceiling": 0.045}],
        "tube_length_m": 1.5, "tube_diameter_m": 0.038, "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7},
        "mean_luma_note": "the three approved pictures' own means (measured 12 October on production/art/shop-rooms/pawnbroker_*.png): the new pictures keep to "
                          "within 15 per cent of them",
    },
    "lit_at_night": True, "lit_why": "RULINGS 1 Oct (the pawnbroker's window lit at night); vignette-pieces lit_names east_parade_interior2",
    "hours": {"mon": [9, 17.5], "tue": [9, 17.5], "wed": [9, 13], "thu": [9, 17.5], "fri": [9, 17.5], "sat": [9, 17.5]}, "hours_source": "hook-cast.json areas.ritas",
    "fixtures": [
        fx("R-back-stock", "back", "the stock wall: five tiers of 25 mm boards 0.40 deep (the television sets are 0.35 deep), filled shoulder to shoulder, a ticket on every piece; the lowest two tiers only at the "
           "ends, the counter standing in front of the middle", 0.40, x=(-2.60, 2.60), z=(0.50, 2.25), tiers=[0.50, 0.85, 1.35, 1.70, 2.05], kind="shelf_unit"),
        fx("R-back-counter", "back", "the staff counter, glass-topped case on a velvet bed, against the wall (0.6 deep, 1.05 high), 2.8 m long; notices on its front",
           0.60, x=(-1.90, 0.90), z=(0.0, 1.05), kind="counter"),
        fx("R-back-door", "back", "a half-glazed painted door to the back room, ajar 0.15 m, 2.0 m high (flat: leaf 40 mm)", 0.04, x=(1.45, 2.35), z=(0.0, 2.0), kind="door"),
        fx("R-left-board", "left", "pledge board: a pegboard 1.8 x 1.2 m, 20 mm, hung with ticketed small goods flat to it", 0.08, y=(0.9, 2.7), z=(0.6, 1.8), kind="flat_board"),
        fx("R-left-notices", "left", "the licence card and a handwritten UNREDEEMED PLEDGES FOR SALE card (paper, 3 mm)", 0.005, y=(3.0, 3.8), z=(1.5, 1.9), kind="notice"),
        fx("R-right-board", "right", "tools hung flat on a pegboard 2.2 x 1.0 m", 0.08, y=(1.4, 3.6), z=(0.8, 1.8), kind="flat_board"),
        fx("R-right-hung", "right", "two ukuleles hung by their heads and an ornate mirror, flat to the wall", 0.07, y=(0.4, 1.2), z=(1.2, 2.0), kind="flat_hung"),
        fx("R-floor-mat", "floor", "a worn door mat (flat) and the lino's own worn path", 0.012, x=(-2.45, -1.55), y=(0.15, 0.85), z=(0.0, 0.012), kind="floor_flat"),
        fx("R-ceiling-tubes", "ceiling", "three T12 battens in slim fittings", 0.045, x=(-0.75, 0.75), kind="light"),
    ],
    "goods": [
        gd("television_02", 4, "R-back-stock", note="CRT sets on the two upper-middle tiers; none on the lowest"),
        gd("boombox", 3, "R-back-stock"), gd("cassette_player", 3, "R-back-stock"), gd("portable_cassette_player", 4, "R-back-stock", note="maker's name painted out"),
        gd("Camera_01", 3, "R-back-stock", note="lens-ring lettering painted out"), gd("vintage_video_camera", 2, "R-back-stock"),
        gd("vintage_binocular", 2, "R-back-stock"), gd("binoculars", 1, "R-back-stock"), gd("mantel_clock_01", 2, "R-back-stock"), gd("alarm_clock_01", 3, "R-back-stock"),
        gd("brass_vase_01", 2, "R-back-stock"), gd("brass_vase_02", 1, "R-back-stock"), gd("brass_vase_03", 2, "R-back-stock"), gd("filmstrip_projector_8mm", 2, "R-back-stock"),
        gd("metal_toolbox", 2, "R-back-stock"), gd("hand_plane_no4", 1, "R-back-stock"), gd("cardboard_box_01", 9, "R-back-stock", size=0.36, note="the top tier: boxes of stock, a ticket each"),
        gd("CashRegister_01", 1, "R-back-counter", size=0.42, note="the till at the counter's right end, on the glass"),
        gd("script:counter_jewellery", 1, "R-back-counter", why="rings, chains and watches on velvet in the case: Rita's approved scripted jewellery (tori, discs, links), kept as approved"),
        gd("pocket_watch", 3, "R-back-counter", size=0.06), gd("vintage_pocket_watch", 3, "R-back-counter", size=0.06),
        gd("pipe_wrench", 1, "R-right-board"), gd("cross_pein_hammer", 1, "R-right-board"), gd("handsaw_wood", 1, "R-right-board"), gd("hand_plane_no4", 1, "R-right-board"),
        gd("Ukulele_01", 2, "R-right-hung", size=0.62), gd("ornate_mirror_01", 1, "R-right-hung", size=0.42),
        gd("wall_clock", 1, "R-back-stock", size=0.30, note="its dial's maker mark painted out (a 60 x 14 px patch under the 12)"),
        gd("script:pledge_tickets", 40, "R-left-board", why="paper tickets 25 x 12 mm with handwritten numbers: texture-printed cards, no model exists"),
    ],
    "display": {
        "keeps": "production/assets/shop-displays/pawnbroker-display.glb as built (23 Poly Haven models on a stepped velvet bed, a ticket on each), 3.35 m long, 0.55 deep",
        "changes": "drop digital_wrist_watch (a maker's mark, not in the glb's list today: confirm) and any model whose map shows a maker's name after the 1k "
                   "inspection; add the night grille; pieces are not repeated more than twice (the third review's copy-paste note)",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.55,
        "items": [
            di("pocket_watch", 2, [0.2, 0.9, 0.05, 0.35, 0.0, 0.12], size=0.06), di("vintage_pocket_watch", 2, [0.9, 1.5, 0.05, 0.35, 0.0, 0.12], size=0.06),
            di("Camera_01", 2, [0.1, 0.9, 0.15, 0.50, 0.12, 0.40]), di("vintage_video_camera", 1, [1.0, 1.5, 0.15, 0.50, 0.12, 0.40]),
            di("binoculars", 1, [1.6, 2.1, 0.15, 0.50, 0.12, 0.40]), di("round_spectacles", 1, [2.2, 2.6, 0.05, 0.30, 0.12, 0.30]),
            di("mantel_clock_01", 1, [0.2, 0.9, 0.20, 0.50, 0.40, 0.75]), di("alarm_clock_01", 2, [1.0, 1.9, 0.20, 0.50, 0.40, 0.75]),
            di("brass_vase_01", 1, [2.4, 2.8, 0.20, 0.50, 0.40, 1.10]), di("brass_vase_02", 1, [2.9, 3.2, 0.20, 0.50, 0.40, 0.95]), di("brass_vase_03", 1, [0.9, 1.2, 0.30, 0.50, 0.75, 0.95]),
            di("ceramic_vase_01", 1, [1.3, 1.7, 0.25, 0.50, 0.75, 1.15]), di("ceramic_vase_03", 1, [1.8, 2.0, 0.25, 0.45, 0.75, 1.15]),
            di("antique_ceramic_vase_01", 1, [2.1, 2.7, 0.20, 0.50, 0.75, 1.20]),
            di("standing_picture_frame_01", 1, [0.2, 0.5, 0.25, 0.40, 0.75, 1.0]), di("standing_picture_frame_02", 1, [2.8, 3.1, 0.25, 0.40, 0.75, 1.0]),
            di("portable_cassette_player", 2, [1.7, 2.3, 0.10, 0.40, 0.0, 0.20], note="maker's name painted out"),
            di("seadogs_compass", 1, [0.4, 0.7, 0.05, 0.25, 0.12, 0.22]), di("vintage_flashlight", 1, [2.0, 2.3, 0.05, 0.35, 0.12, 0.26]),
            di("cigarette_case", 1, [1.2, 1.7, 0.05, 0.25, 0.0, 0.03], note="tobacco is allowed; a plain metal case"),
            di("vintage_lighter", 1, [1.8, 2.0, 0.05, 0.20, 0.0, 0.07], note="the stamp under the base blanked"),
            di("magnifying_glass_01", 1, [0.5, 0.8, 0.05, 0.30, 0.0, 0.03]), di("carved_wooden_elephant", 1, [2.5, 2.8, 0.05, 0.25, 0.12, 0.22]),
            di("horse_statue_01", 1, [0.4, 0.8, 0.30, 0.50, 0.75, 1.00]), di("jug_01", 1, [3.0, 3.3, 0.05, 0.30, 0.12, 0.32]),
            di("measuring_tape_01", 1, [1.5, 1.7, 0.05, 0.20, 0.12, 0.19], note="its label blanked"),
        ],
        "night": "an external lattice grille closed over the window zone from dusk to dawn: flat bars 20 x 4 mm at 45 degrees, the diamond 120 mm across, "
                 "rivets at every crossing, a 40 x 40 box top rail under the fascia at z 2.50 and a bottom channel at z 0.70 above the crown, the plane 100 mm in front of "
                 "the glass front (street y 5.145), powder black (37, 35, 34) rough 0.45; the window behind it stays lit",
    },
}

# ---- 1 MICKEY'S (spec id mickeys): the room stays the real walked room ---------------------------------------------------------------
SHOPS["mickeys"] = {
    "spec_id": "mickeys", "room_D": 4.15, "needs_room": False, "room_real": True,
    "keeps": "everything of the room: production/specs/mickeys-office.json, shop-room.py's mickeys branch, room_3d, its lamps and brightness values (spec entry unchanged)",
    "changes": "only the front is unit 7's: the A2 painted-steel refit assembled from the 3.2 parts, the 4.1 board with the raised gilt letters, the glass rows",
    "lit_at_night": True, "lit_why": "dark until Tom's key (spec lit_at_start false, lit_at_night true); after the key it is open to 3 am; in vignette-pieces lit_names",
    "hours": {"mon": [7, 27], "tue": [7, 27], "wed": [7, 27], "thu": [7, 27], "fri": [7, 27], "sat": [7, 27], "sun": [9, 27]}, "hours_source": "hook-cast.json areas.mickeys",
    "fixtures": [], "goods": [], "display": None,
}

# ---- 3 FISH MARKET (spec id fishmonger) --------------------------------------------------------------------------------------------------
SHOPS["fish_market"] = {
    "spec_id": "fishmonger", "room_D": 4.5, "needs_room": True,
    "keeps": "the research (FISHMONGER-2026-10-03.md, Picture Sheffield t13140 and t13138), the white-tile walls and red quarry floor of the 3 Oct code (shop-room.py 257, 287)",
    "changes": "no hand-made fish (the 3 Oct failure): the fish are CC0 scans or the window shows none; the slab and ice are real meshes in the display; the chiller "
               "counter goes against the back wall (it smeared as a black panel across the floor); the white slab no longer burns out at night (the room is dark at night)",
    "floor": {"material": "red quarry tile 150 mm, grout 20 mm, wet (roughness 0.12); Poly Haven terracotta_floor_tiles as the base if it reads red enough, else the script's brick shader", "base": (82, 26, 15)},
    "walls": {"above": "white glazed square tile 152 mm, grey grout, soiled (Poly Haven long_white_tiles or square_tiles), to the ceiling", "dado": "same tile"},
    "ceiling": "painted white board (200, 198, 190)",
    "lights": {
        "day": "daylight through the front opening (overcast area light) plus two 5 ft battens on (open Mon to Sat 7:30 to 14:00, Wed to 13:00)",
        "night_lit": "not used: the shop is shut after 14:00 and the street file leaves it dark (rendered for completeness: two battens on)",
        "night_dark": "a faint sodium wash through the front (6 per cent) and the chiller's small glow lamp (2700 K) at the counter",
        "tubes": [{"x": -0.6, "y": 1.6, "z_below_ceiling": 0.045}, {"x": 0.6, "y": 3.2, "z_below_ceiling": 0.045}], "tube_length_m": 1.5, "tube_diameter_m": 0.038,
        "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": False, "lit_why": "vignette-pieces lit_names omits east_parade_interior1; the shop shuts at 14:00",
    "hours": {"mon": [7.5, 14], "tue": [7.5, 14], "wed": [7.5, 13], "thu": [7.5, 14], "fri": [7.5, 14], "sat": [7.5, 14]}, "hours_source": "hook-cast.json areas.fish_market",
    "fixtures": [
        fx("F-back-counter", "back", "the serve-over chiller: a white glass-fronted counter 0.6 deep, 1.0 high, 3.0 m long, a sloping glass front, white enamel trays in the well", 0.60,
           x=(-2.45, 0.55), z=(0.0, 1.0), kind="counter"),
        fx("F-back-shelf", "back", "two shelves 0.15 deep high on the back wall with tins and jars (Picture Sheffield t13140)", 0.15, x=(-2.45, 0.55), z=(1.55, 2.2), tiers=[1.55, 1.90], kind="shelf_unit"),
        fx("F-back-door", "back", "a white plastic-faced cold-room door 0.9 x 2.0, chrome lever, rubber seal (flat, 70 mm)", 0.07, x=(1.40, 2.30), z=(0.0, 2.0), kind="door"),
        fx("F-back-hose", "back", "a coiled green hose on a wall bracket at the right end of the back wall", 0.25, x=(0.80, 1.30), z=(0.8, 1.4), kind="wall_mounted"),
        fx("F-left-board", "left", "a blackboard price list 0.8 x 0.6 m (chalk numerals only), 25 mm", 0.03, y=(1.4, 2.2), z=(1.2, 1.8), kind="flat_board"),
        fx("F-right-clock", "right", "a wall clock and a hanging scale's chart (flat)", 0.05, y=(1.0, 1.5), z=(1.8, 2.1), kind="flat_hung"),
        fx("F-floor-drain", "floor", "a stainless drain grating 0.3 x 0.3 m flush in the quarry tile, a hosed dark patch", 0.01, x=(-0.4, -0.1), y=(2.6, 2.9), z=(0.0, 0.01), kind="floor_flat"),
        fx("F-ceiling-tubes", "ceiling", "two T12 battens in slim fittings", 0.045, x=(-0.6, 0.6), kind="light"),
    ],
    "goods": [
        gd("script:enamel_trays", 8, "F-back-counter", why="white enamel trays 0.45 x 0.30 x 0.05 with a rolled rim: no CC0 model; each carries fish (below)"),
        gd("script:fish_on_ice", 1, "F-back-counter", why="the counter's fish: Sketchfab ffishAsia CC0 scans (cod, mackerel, herring, flounder) when Jafar gives the login; NONE are hand-modelled. Until then the trays hold ice and tickets only and the shop's review says so"),
        gd("script:tins_and_jars", 24, "F-back-shelf", why="tins and jars with labels from the project's label atlas (pilchards, salmon, a crab-paste tile to add): shapes by script, print from make_label_atlas.py"),
        gd("garden_hose_wall_mounted_01", 1, "F-back-hose"), gd("wall_clock", 1, "F-right-clock", size=0.30, note="dial maker mark painted out"),
        gd("script:price_board_chalk", 1, "F-left-board", why="chalk lettering is a texture: numerals and COD, HADDOCK, PLAICE, KIPPERS only (no alcohol, no brand)"),
    ],
    "display": {
        "keeps": "FISHMONGER-2026-10-03.md: a tilted white slab under crushed ice, fish in rows each with a per-lb ticket, white trays, lettering on the glass",
        "changes": "everything in the display is a real mesh in the near metre; no fish is modelled by hand",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.10,
        "items": [
            di("script:slab_and_ice", 1, [0.0, 3.35, 0.0, 0.55, 0.0, 0.14], why="a white marble slab sloping 12 degrees toward the glass, 3.35 x 0.55 m, with a 40 mm lip (Poly Haven marble_01 or ambientCG Marble012 on a box); crushed ice: a displaced bed (ambientCG Ice002) with 300 instanced chunks of four shapes"),
            di("script:enamel_trays", 6, [0.1, 3.2, 0.10, 0.50, 0.06, 0.12], why="white enamel trays on the slab, rolled rim, the front rank tilted"),
            di("script:fish_on_ice", 1, [0.1, 3.2, 0.10, 0.50, 0.10, 0.30], why="cod x4, mackerel x8, herring x6, flounder-for-plaice x4, crab x5, prawns x60 instanced: Sketchfab ffishAsia CC0 scans (uids in the sources), decimated to 20 to 50 thousand triangles and baked; REQUIRES Jafar's Sketchfab login (the download API answers 401 without it): the one item of this unit the cloud cannot fetch"),
            di("lemon", 8, [0.3, 3.0, 0.30, 0.50, 0.08, 0.16], note="whole lemons beside the trays"),
            di("script:price_stakes", 14, [0.1, 3.2, 0.05, 0.45, 0.10, 0.22], why="white plastic stick-in tickets 40 x 25 mm on 100 mm stakes with a handwritten price in per-lb (the 1990 price: cod about 2.60 a lb, ONS series CZOL)"),
            di("script:chiller_pad", 1, [0.0, 3.35, 0.52, 0.55, 0.0, 0.30], why="a white laminate back panel 25 mm at the display's rear edge, so the slab reads as a counter and the picture's counter is not doubled"),
        ],
        "night": None,
    },
}

# ---- 4 EMPTY UNIT -----------------------------------------------------------------------------------------------------------------------
SHOPS["empty_unit"] = {
    "spec_id": None, "room_D": None, "needs_room": False,
    "keeps": "everything the street already draws: every pane whitewashed from inside, no interior card (terrace-front.py skips bay 3), the 4.1 letting board and whitewash",
    "changes": "the front only: the unit's bare timber front assembled from the 3.2 parts (left console clipped off, paint gone), the whitewash tile from 4.1",
    "lit_at_night": False, "lit_why": "empty; nothing lit", "hours": None, "hours_source": "none: to let",
    "fixtures": [], "goods": [], "display": None,
}

# ---- 5 STEAM LAUNDRY (spec id launderette) ------------------------------------------------------------------------------------------------
SHOPS["steam_laundry"] = {
    "spec_id": "launderette", "room_D": 4.5, "needs_room": True,
    "keeps": "the 3 Oct decision (a launderette with a service counter: the Steam Laundry), the real-room finding that the dryers and washers must stand against walls",
    "changes": "no slab laundry, no dryer stack standing off the wall: machines stand against the BACK wall only; the side walls carry notices; the near metre is a real "
               "display of folded laundry and detergent boxes with fictional labels",
    "floor": {"material": "grey vinyl tile 300 mm with a darker worn path (Poly Haven rubber_tiles tinted grey, or worn_tile_floor)", "base": (92, 94, 96)},
    "walls": {"above": "cream emulsion (222, 212, 184) above a white glazed tile dado 1.5 m (Poly Haven long_white_tiles)", "dado": "white tile to z 1.5"},
    "ceiling": "white board (205, 203, 196)",
    "lights": {
        "day": "daylight through the front opening plus three battens on (open Mon to Sat 8 to 17:30)",
        "night_lit": "not used by the street file (dark); rendered with the three battens on",
        "night_dark": "a faint sodium wash and the dryers' two orange 'running' lamps (small, 2000 K, 0.01 m) so the room is not black",
        "tubes": [{"x": 0.0, "y": 1.0, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 2.2, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 3.4, "z_below_ceiling": 0.045}],
        "tube_length_m": 1.5, "tube_diameter_m": 0.038, "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": False, "lit_why": "vignette-pieces lit_names omits east_parade_interior4; its box sign glows (4.1 emissive) but the room is dark",
    "hours": {"mon": [8, 17.5], "tue": [8, 17.5], "wed": [8, 17.5], "thu": [8, 17.5], "fri": [8, 17.5], "sat": [8, 17.5]}, "hours_source": "hook-cast.json areas.laundry",
    "fixtures": [
        fx("L-back-washers", "back", "a row of four front-loading washers, white enamel, 0.60 x 0.60 x 0.85, a round glass door 0.30, a coin-slot plate and a powder drawer (blank plates)", 0.60, x=(-2.55, -0.15), z=(0.0, 0.85), kind="machines"),
        fx("L-back-dryers", "back", "three stacks of two tumble dryers, 0.60 deep, each 0.70 wide x 0.85 high, round door 0.40, a timer dial and a coin slot", 0.60, x=(0.20, 2.35), z=(0.0, 1.75), kind="machines"),
        fx("L-back-shelves", "back", "wall shelves 0.30 deep above the machines carrying paper-wrapped parcels tied with string (the service wash)", 0.30, x=(-2.55, -0.15), z=(1.30, 2.10), tiers=[1.30, 1.70], kind="shelf_unit"),
        fx("L-left-notices", "left", "a price list, a rules card and a 'service washes' card, paper on a cork board 0.9 x 0.6 (30 mm)", 0.03, y=(1.5, 2.6), z=(1.2, 1.9), kind="flat_board"),
        fx("L-right-notices", "right", "a wash-care chart 0.6 x 0.8 and a wall clock, flat", 0.05, y=(1.2, 2.2), z=(1.1, 2.0), kind="flat_hung"),
        fx("L-floor-mat", "floor", "a black rubber mat 1.0 x 0.6 flat at the door and a worn path", 0.012, x=(-0.5, 0.5), y=(0.2, 0.8), z=(0.0, 0.012), kind="floor_flat"),
        fx("L-ceiling-tubes", "ceiling", "three T12 battens", 0.045, x=(-0.75, 0.75), kind="light"),
    ],
    "goods": [
        gd("script:washing_machine", 4, "L-back-washers", why="no CC0 washing machine exists in Poly Haven or ambientCG: a cabinet, a porthole ring, a dark glass door, a drawer, from dimensions"),
        gd("script:tumble_dryer", 6, "L-back-dryers", why="no CC0 dryer: the same cabinet at 0.60 deep with the 0.40 door"),
        gd("script:wrapped_parcels", 18, "L-back-shelves", why="brown paper parcels 0.30 x 0.20 x 0.12 tied with string, a numbered tag: boxes with a paper material, no CC0 model"),
        gd("wall_clock", 1, "L-right-notices", size=0.30, note="dial maker mark painted out"),
    ],
    "display": {
        "keeps": "SERVICE WASHES lettering on the glass (4.1), the research's folded parcels on shelves",
        "changes": "folded laundry in real towers, two wicker baskets, boxed detergents with the project's fictional labels",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.30,
        "items": [
            di("script:folded_towels", 5, [0.1, 1.5, 0.10, 0.50, 0.0, 0.45], why="folded towels and sheets as bevelled boxes 0.45 x 0.30 x 0.05 each, ambientCG Fabric020 and Fabric021 (towel weave) tinted, stacked 6 to 9 high with a lean of 1 to 3 degrees"),
            di("wicker_basket_01", 2, [1.7, 2.5, 0.10, 0.45, 0.0, 0.12]), di("script:laundry_in_basket", 2, [1.7, 2.5, 0.10, 0.45, 0.10, 0.30], why="soft cloth: a displaced heap per basket, no CC0 model"),
            di("script:detergent_boxes", 10, [2.6, 3.3, 0.10, 0.45, 0.0, 0.35], why="packets and a bottle with tiles from the label atlas (HOLME Soap Flakes, FERNSIDE Washing-up Liquid): fictional makers"),
            di("script:laundry_shelf_board", 1, [0.0, 3.35, 0.0, 0.55, 0.0, 0.02], why="a laminate bed cover 20 mm"),
            di("script:paper_card_service_washes", 1, [1.3, 2.0, 0.45, 0.46, 0.50, 0.70], why="a hand-lettered card on a stand: texture on a 3 mm card"),
        ],
        "night": None,
    },
}

# ---- 6 GROCER (spec id grocer) ------------------------------------------------------------------------------------------------------------
SHOPS["grocer"] = {
    "spec_id": "grocer", "room_D": 4.5, "needs_room": True,
    "keeps": "the 3 Oct label atlas (production/assets/shop-goods/labels.jpg and .json: 32 fictional products in our OFL fonts) and its tin, packet, jar and bottle shapes",
    "changes": "stock only on the back wall (0.25 deep) and on side shelves 0.10 deep (tins only); the near metre is a real tiered stand of produce and tins with "
               "scanned fruit; the printed tiles are on bevelled shapes, never plain blocks; the lobby's 0.6 recess takes nothing from the room",
    "floor": {"material": "brown linoleum (Poly Haven linoleum_brown)", "base": (84, 62, 40)},
    "walls": {"above": "cream (222, 209, 175) emulsion", "dado": "bottle green (36, 61, 49) to z 1.1"},
    "ceiling": "cream plaster (196, 188, 168)",
    "lights": {
        "day": "daylight through the front opening plus three battens on (hours not found: settled as Mon to Sat 8 to 17:30, early closing Wed 13:00, Shops Act)",
        "night_lit": "the three battens on and a pendant opal globe in the lobby (2700 K, 60 W): the street file lights this unit (east_parade_interior5)",
        "night_dark": "a faint sodium wash and the till's glow lamp",
        "tubes": [{"x": -0.6, "y": 1.2, "z_below_ceiling": 0.045}, {"x": 0.6, "y": 2.4, "z_below_ceiling": 0.045}, {"x": -0.6, "y": 3.6, "z_below_ceiling": 0.045}],
        "tube_length_m": 1.5, "tube_diameter_m": 0.038, "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": True, "lit_why": "vignette-pieces lit_names east_parade_interior5 (practicals chosen so the parade is not a shopping centre; the hours say it is shut: a conflict, kept as the street file has it)",
    "hours": {"mon": [8, 17.5], "tue": [8, 17.5], "wed": [8, 13], "thu": [8, 17.5], "fri": [8, 17.5], "sat": [8, 17.5]}, "hours_source": "Judgement from the Shops Act (shop-hours-1990 NOTE): not found for the grocer",
    "fixtures": [
        fx("G-back-gantry", "back", "the grocer's gantry: floor-to-2.2 shelving 0.25 deep, five tiers, tins and packets in front rows two deep", 0.25, x=(-2.60, 0.10), z=(0.0, 2.2), tiers=[0.45, 0.85, 1.25, 1.65, 2.05], kind="shelf_unit"),
        fx("G-back-counter", "back", "the counter at the back wall's right end, 0.6 deep, 1.0 high, 2.4 m long, a till and a scale", 0.60, x=(0.20, 2.60), z=(0.0, 1.0), kind="counter"),
        fx("G-back-shelves-right", "back", "shelves 0.20 deep above the counter: jars, biscuit tins, bottles of sauce and squash", 0.20, x=(0.20, 2.60), z=(1.40, 2.15), tiers=[1.40, 1.78], kind="shelf_unit"),
        fx("G-left-tins", "left", "a shallow shelf unit 0.10 deep, four tiers, tins only (diameter 0.075)", 0.10, y=(1.0, 3.0), z=(0.7, 1.9), tiers=[0.7, 1.05, 1.4, 1.75], kind="shelf_unit"),
        fx("G-right-tins", "right", "a shallow shelf unit 0.10 deep, four tiers, packets of tea and sugar standing on edge", 0.10, y=(1.0, 3.0), z=(0.7, 1.9), tiers=[0.7, 1.05, 1.4, 1.75], kind="shelf_unit"),
        fx("G-ceiling-tubes", "ceiling", "three T12 battens", 0.045, x=(-0.75, 0.75), kind="light"),
        fx("G-floor", "floor", "worn lino with a darker path to the counter", 0.01, x=(-2.0, 2.0), y=(0.3, 3.8), z=(0.0, 0.01), kind="floor_flat"),
    ],
    "goods": [
        gd("script:tins", 160, "G-back-gantry", why="12- to 16-sided cylinders with a rim and a bevelled seam, labels from the atlas (12 tin tiles), turned +-4 degrees, a few pulled forward or missing"),
        gd("script:packets", 90, "G-back-gantry", why="bevelled boxes (2 to 3 mm bevel) with the atlas's 12 packet tiles"),
        gd("script:jars", 24, "G-back-shelves-right", why="screw-lid jars, opaque contents, atlas tiles (jam, marmalade, pickled onions, honey)"),
        gd("script:bottles", 12, "G-back-shelves-right", why="bottles with atlas tiles (washing-up liquid, brown sauce, orange squash, vinegar)"),
        gd("plastic_crate_02", 3, "G-back-gantry", note="the bottom tier's crates (yellow), loaded with potatoes (below)"),
        gd("wicker_basket_01", 2, "G-back-gantry", note="loaf baskets on the second tier"), gd("hamburger_buns", 3, "G-back-gantry", note="bread rolls, three sets"),
        gd("CashRegister_01", 1, "G-back-counter", size=0.42), gd("script:counter_scale", 1, "G-back-counter", why="a brass and enamel counter scale with a dial: no CC0 model; from dimensions"),
        gd("script:tins", 40, "G-left-tins", why="tins only on the 0.10 side shelves"), gd("script:packets", 30, "G-right-tins"),
        gd("wall_clock", 1, "G-back-gantry", size=0.30, note="above the gantry's top tier; dial maker mark painted out"),
    ],
    "display": {
        "keeps": "the 1930s refit's deep lobby; the research's crate-and-stand dressing; Holyoake's photograph (Geograph 2184467, 1999) for density",
        "changes": "produce is scanned (Poly Haven apple, banana, lemon, onion; Sketchfab ffishAsia CC0 cabbage, potato, satsuma, pear by his login); tins and jars carry atlas labels",
        "u_range": [0.0, 4.294], "depth": 0.55, "height_max_w": 1.45,
        "items": [
            di("script:tiered_stand", 1, [0.0, 4.294, 0.0, 0.55, 0.0, 0.50], why="a three-tier timber display stand 0.18 high a step (Holyoake's photograph), made from dimensions"),
            di("plastic_crate_02", 3, [0.2, 1.7, 0.05, 0.50, 0.0, 0.25], note="produce crates"), di("plastic_crate_03", 2, [1.8, 2.6, 0.10, 0.36, 0.0, 0.27]),
            di("food_apple_01", 40, [0.2, 1.7, 0.05, 0.50, 0.20, 0.34], note="three sizes of scale 0.9 to 1.1, a per-instance tint"),
            di("lemon", 12, [1.8, 2.6, 0.10, 0.36, 0.22, 0.32]), di("yellow_onion", 15, [2.7, 3.4, 0.10, 0.45, 0.0, 0.14]), di("bananas", 3, [3.5, 4.2, 0.10, 0.40, 0.16, 0.30]),
            di("script:cabbage_potato_satsuma", 1, [0.2, 4.0, 0.10, 0.50, 0.10, 0.35], why="Sketchfab ffishAsia CC0 scans (cabbage x4, potato x20, satsuma x12, pear x6), decimated and baked: REQUIRES Jafar's Sketchfab login"),
            di("script:tomatoes", 30, [2.7, 3.4, 0.15, 0.40, 0.16, 0.26], why="no CC0 tomato exists: a glossy red flattened sphere with a calyx, varied per instance (the research's cheapest method; set aside after one try if it reads as toys)"),
            di("script:tin_pyramids", 3, [0.4, 3.9, 0.10, 0.30, 0.50, 0.95], why="three pyramids of 28 tins each with atlas labels"),
            di("script:jars", 18, [1.6, 3.0, 0.30, 0.50, 0.55, 0.85], why="jam, marmalade, honey with atlas tiles"),
            di("wicker_basket_02", 1, [3.6, 4.2, 0.15, 0.45, 0.50, 0.72]), di("hamburger_buns", 2, [3.65, 4.1, 0.20, 0.40, 0.66, 0.74]),
            di("script:price_cards", 14, [0.1, 4.2, 0.05, 0.50, 0.15, 0.60], why="hand-lettered cards 70 x 50 mm on wire stakes"),
        ],
        "night": None,
    },
}

# ---- 7 CHANDLER (spec id chandler) -------------------------------------------------------------------------------------------------------
SHOPS["chandler"] = {
    "spec_id": "chandler", "room_D": 4.5, "needs_room": True,
    "keeps": "the 3 Oct trade list (buoys, lifebuoy, life jacket, lanterns, boots, oil, crates) and the CC0 set in fetch_polyhaven.py",
    "changes": "NO explosives-marked drum (Barrel_01 is out); the buoy stands flat against the back wall at a scaled height; nothing hangs from the ceiling; rope is twisted by "
               "script with ambientCG Rope textures (no CC0 model): coils stand on shelves",
    "floor": {"material": "oiled boards (Poly Haven old_wooden_floor_02)", "base": (72, 52, 34)},
    "walls": {"above": "cream emulsion (214, 204, 178) with a dark green dado 1.0 m (the E.E. Sharp photograph's green)", "dado": "(30, 62, 44) to z 1.0"},
    "ceiling": "painted board (192, 186, 168)",
    "lights": {
        "day": "daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8 to 17, Wed to 13:00, Shops Act)",
        "night_lit": "two battens on and a hurricane lamp (Lantern_01, 2200 K, lit) on the counter: the street file lights this unit (east_chandler_interior0)",
        "night_dark": "a faint sodium wash",
        "tubes": [{"x": -0.7, "y": 1.6, "z_below_ceiling": 0.045}, {"x": 0.7, "y": 3.0, "z_below_ceiling": 0.045}], "tube_length_m": 1.5, "tube_diameter_m": 0.038,
        "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": True, "lit_why": "vignette-pieces lit_names east_chandler_interior0 (the hours say shut by 17:00: kept as the street file has it)",
    "hours": {"mon": [8, 17], "tue": [8, 17], "wed": [8, 13], "thu": [8, 17], "fri": [8, 17], "sat": [8, 17]}, "hours_source": "Judgement from the Shops Act: not found for the chandler",
    "fixtures": [
        fx("C-back-shelves", "back", "tall shelving 0.30 deep, five tiers, floor to 2.2: paint tins, varnish, oil cans, twine, lamp glasses, boots on the lowest", 0.30, x=(-2.60, 0.20), z=(0.0, 2.2), tiers=[0.40, 0.80, 1.20, 1.60, 2.00], kind="shelf_unit"),
        fx("C-back-counter", "back", "the counter 0.6 deep, 1.0 high, 2.2 m long, a brass-edged top, a chart drawer; the hurricane lamp and a brass compass on it", 0.60, x=(0.40, 2.60), z=(0.0, 1.0), kind="counter"),
        fx("C-back-hooks", "back", "a board of pegs 2.0 x 0.3 m above the counter hung with life jackets, a lifebuoy and oilskins", 0.18, x=(0.40, 2.50), z=(1.35, 2.20), kind="flat_hung"),
        fx("C-left-charts", "left", "chart posters and a tide table card, paper (3 mm), and a coil-rope board (rope laid flat on the board, 40 mm)", 0.05, y=(1.2, 3.0), z=(0.9, 1.9), kind="flat_board"),
        fx("C-right-board", "right", "a pegboard 1.6 x 1.1 m with shackles, blocks, cleats and chain hung flat (60 mm)", 0.07, y=(1.2, 2.8), z=(0.9, 2.0), kind="flat_board"),
        fx("C-floor-buoy", "back", "a marker buoy, scaled to 1.5 m tall, standing on the floor against the back wall at the left end (depth 0.55)", 0.55, x=(-2.60, -2.05), z=(0.0, 1.5), kind="free_at_wall"),
        fx("C-ceiling-tubes", "ceiling", "two T12 battens", 0.045, x=(-0.7, 0.7), kind="light"),
    ],
    "goods": [
        gd("script:paint_tins", 40, "C-back-shelves", why="lathe tins 0.18 with a lid rim and a wire bail, labels from new atlas tiles (marine varnish, antifouling, deck paint, white spirit: fictional makers)"),
        gd("oil_tin", 5, "C-back-shelves"), gd("small_oil_can_01", 4, "C-back-shelves"), gd("cleaner_tin_01", 4, "C-back-shelves", note="label to the atlas"),
        gd("rubber_boots", 4, "C-back-shelves", note="four pairs on the lowest tier"), gd("signal_flashlight", 3, "C-back-shelves"), gd("Lantern_01", 4, "C-back-shelves"),
        gd("script:rope_coils", 6, "C-back-shelves", why="three-strand twisted sweep with ambientCG Rope001 and Rope002, four colours, standing on edge: no CC0 model"),
        gd("script:twine_reels", 10, "C-back-shelves", why="cylinders with a twine wrap (ambientCG Rope001)"),
        gd("CashRegister_01", 1, "C-back-counter", size=0.42), gd("seadogs_compass", 3, "C-back-counter"), gd("Lantern_01", 1, "C-back-counter", note="lit at night"),
        gd("life_jacket", 4, "C-back-hooks", note="hung on pegs, flat"), gd("lifebuoy", 2, "C-back-hooks"), gd("script:oilskin_sou_wester", 3, "C-back-hooks", why="a sewn pattern of 4 to 6 panels with a back brim, yellow oilskin: no CC0 model (GOODS note: the fishermans_hat model is a boonie hat, wrong)"),
        gd("script:shackles_blocks", 24, "C-right-board", why="steel shackles, cleats and blocks: simple extrusions on the board"), gd("script:chart_posters", 6, "C-left-charts", why="invented chart sheets (no real coast, no real chart maker)"),
        gd("ocean_buoy", 1, "C-floor-buoy", size=1.5, note="the model is 2.66 m tall: scaled to 1.5 m as a marker buoy (flagged); its lamp unlit"),
    ],
    "display": {
        "keeps": "the trade list; E.E. Sharp's window (Geograph 3378991, 1983): a chandler's lower lights were screened inside with woven galvanised mesh when shut",
        "changes": "real ropes, lifebuoy, lanterns, boots and tins in the near metre; no ship model, no explosives drum",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.55,
        "items": [
            di("lifebuoy", 1, [0.2, 1.0, 0.10, 0.28, 0.05, 0.90], note="leaning on its edge against the glass-side of the bed, 0.16 thick"), di("life_jacket", 2, [1.1, 1.9, 0.15, 0.35, 0.0, 0.95]),
            di("script:rope_coils", 5, [2.0, 3.3, 0.10, 0.50, 0.0, 0.26], why="coils in natural fibre, blue, orange, white and green, on the bed"),
            di("rubber_boots", 3, [0.2, 1.1, 0.30, 0.50, 0.0, 0.40]), di("Lantern_01", 2, [1.3, 1.7, 0.25, 0.45, 0.0, 0.29]), di("wooden_lantern_01", 1, [1.8, 2.2, 0.20, 0.45, 0.0, 0.53]),
            di("seadogs_compass", 2, [2.4, 2.9, 0.10, 0.30, 0.0, 0.09]), di("oil_tin", 4, [0.3, 1.2, 0.05, 0.30, 0.0, 0.21]), di("small_oil_can_01", 3, [1.3, 2.0, 0.05, 0.30, 0.0, 0.24]),
            di("script:paint_tin_pyramid", 1, [2.2, 3.2, 0.25, 0.50, 0.0, 0.60], why="21 tins in a pyramid, atlas labels"), di("script:oilskin_sou_wester", 2, [1.0, 1.8, 0.35, 0.50, 0.95, 1.40], why="hung from a rail in the display"),
            di("brass_blowtorch", 1, [0.4, 0.7, 0.30, 0.50, 0.0, 0.21]),
        ],
        "night": "woven galvanised mesh screens (wire 2 mm, 12 mm mesh) inside the lower lights (z 0.70 to 1.55 above the crown), three panels, in place when the shop is shut; "
                 "the lit night view has them out of the lit lights' way (the E.E. Sharp photograph shows them over the lower lights only)",
    },
}

# ---- 8 TEA ROOMS (spec id tea_room) ------------------------------------------------------------------------------------------------------
SHOPS["tea_rooms"] = {
    "spec_id": "tea_room", "room_D": 4.5, "needs_room": True,
    "keeps": "the research (Formica tables, a menu board, a half-height cafe curtain, steamed glass) and the 3 Oct food models (carrot cake, strawberry cake, tea set)",
    "changes": "NO Gothic chairs, NO empty frames, NO free tables in the picture (they smeared): tables and chairs are real and only in the window; the room is the counter, "
               "hatch and shelves on the back wall and flat boards; the cafe curtain hides the outer lights",
    "floor": {"material": "chequered vinyl, cream and brown 300 mm (Poly Haven old_linoleum_flooring_01 tinted, a chequer mask)", "base": (150, 130, 100)},
    "walls": {"above": "cream (222, 212, 184)", "dado": "brown (120, 74, 44) to z 1.1"},
    "ceiling": "cream board (208, 200, 180)",
    "lights": {
        "day": "daylight through the front opening plus three battens on (open Mon to Sat 6:30 to 22:00, Sun 8 to 12)",
        "night_lit": "three battens on, the steam-warm window: the street file lights this unit (west_north_interior2); open to 22:00",
        "night_dark": "a faint sodium wash and the counter's pilot lamp",
        "tubes": [{"x": 0.0, "y": 1.0, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 2.2, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 3.4, "z_below_ceiling": 0.045}],
        "tube_length_m": 1.5, "tube_diameter_m": 0.038, "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": True, "lit_why": "vignette-pieces lit_names west_north_interior2; hours-research cafe 6:30 to 22:00", "hours": {"mon": [6.5, 22], "tue": [6.5, 22], "wed": [6.5, 22], "thu": [6.5, 22], "fri": [6.5, 22], "sat": [6.5, 22], "sun": [8, 12]},
    "hours_source": "hook-cast.json areas.cafe",
    "fixtures": [
        fx("T-back-counter", "back", "the serving counter against the back wall 0.55 deep, 1.0 high, 3.0 m long: a glass cake dome, a tea urn (a steel cylinder), a till", 0.55, x=(-2.55, 0.45), z=(0.0, 1.0), kind="counter"),
        fx("T-back-shelf", "back", "two shelves 0.20 deep behind the counter: cups and saucers in stacks, plates, a kettle", 0.20, x=(-2.55, 0.45), z=(1.35, 2.0), tiers=[1.35, 1.75], kind="shelf_unit"),
        fx("T-back-hatch", "back", "the kitchen hatch 1.2 x 0.9 with a roller flap and a shelf (flat, 80 mm)", 0.08, x=(1.20, 2.40), z=(0.95, 1.85), kind="hatch"),
        fx("T-back-menu", "back", "a hung menu board and a price card (flat)", 0.03, x=(0.55, 1.10), z=(1.4, 2.0), kind="flat_board"),
        fx("T-left-frames", "left", "three framed prints (flat, 30 mm) and a wall clock", 0.04, y=(1.0, 3.2), z=(1.4, 2.0), kind="flat_hung"),
        fx("T-right-frames", "right", "a notice board and two framed prints (flat)", 0.04, y=(1.0, 3.2), z=(1.3, 2.0), kind="flat_hung"),
        fx("T-ceiling-tubes", "ceiling", "three T12 battens", 0.045, x=(-0.75, 0.75), kind="light"),
        fx("T-floor", "floor", "chequer vinyl, worn paths between counter and door", 0.01, x=(-2.0, 2.0), y=(0.3, 3.6), z=(0.0, 0.01), kind="floor_flat"),
    ],
    "goods": [
        gd("tea_set_01", 2, "T-back-counter"), gd("carrot_cake", 1, "T-back-counter", note="under the dome"), gd("strawberry_chocolate_cake", 1, "T-back-counter", note="under the dome"),
        gd("hamburger_buns", 2, "T-back-counter", note="bread rolls"), gd("vintage_electric_kettle", 1, "T-back-counter"), gd("metal_jug", 1, "T-back-shelf"),
        gd("CashRegister_01", 1, "T-back-counter", size=0.42), gd("script:cups_saucers", 24, "T-back-shelf", why="stacked cups and saucers: lathe forms with a glaze, no CC0 model beyond tea_set_01"),
        gd("script:cake_dome", 1, "T-back-counter", why="an opaque-shelled dome with a faked rim highlight (the GOODS note's rule for glass over goods)"), gd("script:tea_urn", 1, "T-back-counter", why="a stainless urn: a cylinder from dimensions"),
        gd("hanging_picture_frame_02", 1, "T-left-frames", note="its picture replaced with the project's own invented print"), gd("hanging_picture_frame_03", 1, "T-left-frames", note="its picture replaced"),
        gd("wall_clock", 1, "T-left-frames", size=0.30, note="dial maker mark painted out"), gd("hanging_picture_frame_01", 1, "T-right-frames", note="its poster text replaced"),
    ],
    "display": {
        "keeps": "the half-height cafe curtain on a brass rod at z 1.50 above the footway (2.2's tea_rooms glazing note)",
        "changes": "the window table set for tea, in real geometry in the middle light (the two outer lights carry the curtain); no chairs or tables anywhere else",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.50,
        "items": [
            di("round_wooden_table_02", 1, [1.1, 1.9, 0.08, 0.55, 0.0, 0.75], size=0.55, note="scaled to a 0.55 m cafe table (the model is 0.80): flagged; a laminate top replaces the wood"),
            di("painted_wooden_chair_01", 2, [0.7, 1.15, 0.05, 0.50, 0.0, 0.90], note="two chairs at the table"),
            di("tea_set_01", 1, [1.3, 1.7, 0.18, 0.45, 0.75, 0.84], size=0.80, note="pieces separated: a teapot, two cups and saucers laid on the table; the rest of the set is the counter's"), di("script:sugar_bowl_menu", 1, [1.7, 1.9, 0.10, 0.25, 0.75, 0.85], why="a sugar bowl and a card menu on a stand: small lathe and card"),
            di("carrot_cake", 1, [0.2, 0.6, 0.15, 0.50, 0.0, 0.10], note="on a cake stand (script)"), di("script:cake_stand", 1, [0.2, 0.6, 0.15, 0.50, 0.0, 0.12], why="a two-tier china stand: lathe forms"),
            di("strawberry_chocolate_cake", 1, [2.4, 2.9, 0.15, 0.50, 0.0, 0.10]), di("potted_plant_04", 1, [2.9, 3.2, 0.15, 0.40, 0.0, 0.27], note="in the right light"),
            di("script:cafe_curtain", 2, [0.0, 1.0, 0.04, 0.10, 0.35, 0.85], why="a half-height curtain: cream cotton gathered on a brass rod, scalloped head; two panels over the outer lights; cloth cannot be a CC0 model"),
            di("script:window_card_menu", 1, [2.4, 3.2, 0.04, 0.05, 0.85, 1.35], why="a hand-lettered card (BREAKFASTS, LUNCHES, TEAS) on the glass's inside: texture on a card"),
        ],
        "night": None,
    },
}

# ---- 9 IRONMONGER (spec id ironmonger) -------------------------------------------------------------------------------------------------
SHOPS["ironmonger"] = {
    "spec_id": "ironmonger", "room_D": 4.5, "needs_room": True,
    "keeps": "the 3 Oct tools and cleaners set (fetch_polyhaven.py ironmonger), the research's drawer wall, the 4.1 hanging board and 'PARAFFIN' on the fascia",
    "changes": "tools hang FLAT on pegboards on the side walls (they stood on side shelves 0.4 off the wall and smeared); modern aerosols and cleaners with real-brand look-alikes are dropped; "
               "paint tins are the project's labelled tins; the drawer wall is a flat front",
    "floor": {"material": "bare boards, oiled (Poly Haven old_wooden_floor_03)", "base": (86, 66, 44)},
    "walls": {"above": "pale green-cream (204, 206, 180)", "dado": "dark green (30, 62, 44) to z 1.0"},
    "ceiling": "cream board (200, 192, 172)",
    "lights": {
        "day": "daylight through the front opening plus two battens on (hours not found: settled as Mon to Sat 8:30 to 17:30, Wed to 13:00, Shops Act)",
        "night_lit": "not used by the street file (dark): two battens on if rendered",
        "night_dark": "a faint sodium wash only",
        "tubes": [{"x": -0.6, "y": 1.6, "z_below_ceiling": 0.045}, {"x": 0.6, "y": 3.0, "z_below_ceiling": 0.045}], "tube_length_m": 1.5, "tube_diameter_m": 0.038,
        "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": False, "lit_why": "vignette-pieces lit_names omits west_north_interior1", "hours": {"mon": [8.5, 17.5], "tue": [8.5, 17.5], "wed": [8.5, 13], "thu": [8.5, 17.5], "fri": [8.5, 17.5], "sat": [8.5, 17.5]},
    "hours_source": "Judgement from the Shops Act: not found for the ironmonger",
    "fixtures": [
        fx("I-back-drawers", "back", "a run of small drawers 0.10 deep, 6 x 10, each with a brass label holder and a ring pull (nails, screws, hinges), flat front", 0.10, x=(-2.60, -0.60), z=(0.30, 2.15), kind="drawer_wall"),
        fx("I-back-shelves", "back", "shelves 0.28 deep, floor to 2.1, tins, oils, cleaners, bulbs in boxes", 0.28, x=(-0.45, 2.60), z=(0.0, 2.1), tiers=[0.40, 0.80, 1.20, 1.60, 1.95], kind="shelf_unit"),
        fx("I-back-counter", "back", "a counter 0.6 deep, 1.0 high, 1.6 m long between the drawers and the shelves, a brass rule let into its top", 0.60, x=(-0.45, 1.15), z=(0.0, 1.0), kind="counter"),
        fx("I-left-pegboard", "left", "a pegboard 2.4 x 1.2 m hung with hand tools flat to it: wrenches, hammers, pliers, saws, screwdrivers", 0.08, y=(0.9, 3.3), z=(0.7, 1.9), kind="flat_board"),
        fx("I-right-pegboard", "right", "a pegboard 2.4 x 1.2 m hung with garden and cleaning tools: trowels, brooms, gloves", 0.08, y=(0.9, 3.3), z=(0.7, 1.9), kind="flat_board"),
        fx("I-back-floor", "back", "dustbins, a step ladder, cement bags, paraffin cans stood against the back wall at the right end", 0.58, x=(1.30, 2.60), z=(0.0, 1.1), kind="free_at_wall"),
        fx("I-ceiling-tubes", "ceiling", "two T12 battens", 0.045, x=(-0.6, 0.6), kind="light"),
    ],
    "goods": [
        gd("script:drawer_fronts", 60, "I-back-drawers", why="flat drawer fronts with brass label holders and ring pulls: geometry from dimensions, labels are texture"),
        gd("script:paint_tins", 40, "I-back-shelves", why="the project's labelled tins (emulsion, gloss, primer, white spirit: fictional makers)"),
        gd("oil_tin", 6, "I-back-shelves"), gd("small_oil_can_01", 4, "I-back-shelves"), gd("cleaner_tin_01", 4, "I-back-shelves", note="label to the atlas"),
        gd("lightbulb_01", 12, "I-back-shelves", note="in a box (script: box)"), gd("watering_can_metal_01", 3, "I-back-shelves"), gd("metal_toolbox", 2, "I-back-shelves"),
        gd("brass_blowtorch", 1, "I-back-shelves"), gd("drain_cleaner", 3, "I-back-shelves", note="label to the atlas (the yellow can)"),
        gd("CashRegister_01", 1, "I-back-counter", size=0.42), gd("measuring_tape_01", 1, "I-back-counter", note="label blanked"),
        gd("adjustable_wrench", 2, "I-left-pegboard"), gd("combination_wrench", 3, "I-left-pegboard"), gd("cross_pein_hammer", 2, "I-left-pegboard"), gd("wooden_hammer_01", 1, "I-left-pegboard"),
        gd("pliers", 3, "I-left-pegboard"), gd("tongue_groove_pliers", 2, "I-left-pegboard"), gd("screwdriver", 4, "I-left-pegboard"), gd("screwdrivers_02", 1, "I-left-pegboard"),
        gd("flathead_screwdriver", 3, "I-left-pegboard"), gd("handsaw_wood", 2, "I-left-pegboard"), gd("hatchet", 1, "I-left-pegboard"), gd("ratchet_wrench", 2, "I-left-pegboard"),
        gd("pipe_wrench", 1, "I-left-pegboard"), gd("bolt_cutters_01", 1, "I-left-pegboard"), gd("crowbar_01", 1, "I-left-pegboard"),
        gd("trowel_01", 3, "I-right-pegboard"), gd("wooden_broom", 2, "I-right-pegboard"), gd("garden_gloves_01", 4, "I-right-pegboard"),
        gd("dustpan", 2, "I-right-pegboard"), gd("mousetrap", 6, "I-right-pegboard"),
        gd("metal_trash_can", 1, "I-back-floor", note="the pair as modelled (185 cm is the pair's span)"), gd("wooden_ladder", 1, "I-back-floor"), gd("cement_bag", 3, "I-back-floor", note="its red logo replaced by a plain stamp"),
        gd("metal_jerrycan_green", 3, "I-back-floor", note="paraffin"),
    ],
    "display": {
        "keeps": "the 3 Oct idea: tools, cleaners and oils, a watering can, brooms, a blowtorch",
        "changes": "a stack of tin buckets is not in Poly Haven: watering cans and boxes stand for it; every can's label is blanked or the atlas's",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.50,
        "items": [
            di("script:paint_tin_pyramid", 1, [0.2, 1.0, 0.15, 0.50, 0.0, 0.70], why="a pyramid of 36 labelled tins: the window's centrepiece in 1990 ironmongers"),
            di("watering_can_metal_01", 2, [1.1, 1.9, 0.05, 0.50, 0.0, 0.20]), di("metal_toolbox", 2, [2.0, 2.9, 0.10, 0.40, 0.0, 0.35]), di("brass_blowtorch", 1, [1.2, 1.5, 0.30, 0.50, 0.20, 0.41]),
            di("tire_pump", 1, [2.9, 3.2, 0.05, 0.20, 0.0, 0.58]), di("sledgehammer_01", 1, [3.0, 3.3, 0.10, 0.30, 0.0, 0.88], size=0.85, note="standing against the inside of the right-hand mullion, head down"),
            di("garden_gloves_01", 6, [0.2, 1.0, 0.05, 0.14, 0.70, 0.78], note="on a hung card (script)"), di("trowel_01", 4, [1.0, 1.9, 0.10, 0.30, 0.0, 0.05]),
            di("oil_tin", 4, [2.0, 2.6, 0.20, 0.45, 0.35, 0.56]), di("cleaner_tin_01", 4, [2.6, 3.2, 0.20, 0.45, 0.35, 0.48], note="label to the atlas"),
            di("lightbulb_01", 12, [0.2, 0.9, 0.30, 0.50, 0.70, 0.80], note="in an open box"), di("garden_sprinkler_01", 1, [1.9, 2.4, 0.30, 0.50, 0.40, 0.62]),
            di("plastic_broom", 3, [3.1, 3.35, 0.35, 0.50, 0.0, 1.20], note="leaning in a corner"), di("script:price_cards", 12, [0.1, 3.2, 0.05, 0.50, 0.0, 0.40], why="hand-lettered cards on wire stakes"),
        ],
        "night": None,
    },
}

# ---- 10 NEWSAGENT (spec id newsagent) ---------------------------------------------------------------------------------------------------
SHOPS["newsagent"] = {
    "spec_id": "newsagent", "room_D": 4.5, "needs_room": True,
    "keeps": "the 3 Oct trade (papers, sweets, cigarettes behind the counter, a pension counter; no pools coupons, no lottery, no drink); Pinner 1989 (Geograph 3403654, 5945841) for the lit shop and the dark glass",
    "changes": "no gold ribbon across the window (a stale card in the engine: the build's check looks for any card in front of the glass); magazines are real thin meshes in the display and flat covers in the room; the cigarette gantry is a back-wall unit 0.12 deep",
    "floor": {"material": "grey and blue vinyl tile 300 mm (Poly Haven rubber_tiles tinted)", "base": (110, 112, 116)},
    "walls": {"above": "white emulsion (226, 224, 214)", "dado": "pale grey (150, 152, 150) to z 1.0"},
    "ceiling": "white board (212, 210, 202)",
    "lights": {
        "day": "daylight through the front opening plus three battens on (open Mon to Sat 6 to 17:30, Sun 7 to 12)",
        "night_lit": "three battens on, the whole shop bright: the street file lights this unit (west_north_interior0); the roller shutter is up",
        "night_dark": "a faint sodium wash through the front; the shutter is down in the shut-up variant (4.1's shutter_down)",
        "tubes": [{"x": 0.0, "y": 1.0, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 2.2, "z_below_ceiling": 0.045}, {"x": 0.0, "y": 3.4, "z_below_ceiling": 0.045}],
        "tube_length_m": 1.5, "tube_diameter_m": 0.038, "mean_luma_target": {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7}, "mean_luma_note": "Rita's approved means, within 15 per cent",
    },
    "lit_at_night": True, "lit_why": "vignette-pieces lit_names west_north_interior0 (the hours say shut at 17:30: kept as the street file has it; the newsagent's box sign is lit by 4.1 anyway)",
    "hours": {"mon": [6, 17.5], "tue": [6, 17.5], "wed": [6, 17.5], "thu": [6, 17.5], "fri": [6, 17.5], "sat": [6, 17.5], "sun": [7, 12]}, "hours_source": "hook-cast.json areas.newsagent",
    "fixtures": [
        fx("N-back-counter", "back", "the counter 0.6 deep, 1.0 high, 2.6 m long: a till, a sweet-jar row, a toast-rack of cards, a glass cabinet end", 0.60, x=(-2.55, 0.05), z=(0.0, 1.0), kind="counter"),
        fx("N-back-gantry", "back", "the cigarette gantry: three shelves 0.12 deep from z 1.35 to 2.15, cartons and packets, a locked sliding glass front", 0.12, x=(-2.55, 0.05), z=(1.35, 2.15), tiers=[1.35, 1.70, 2.00], kind="shelf_unit"),
        fx("N-back-pensions", "back", "the pension counter: a counter 0.55 deep with a glazed screen 1.0 x 0.8, a brass-edged slot, a hours card (flat 0.10)", 0.55, x=(0.45, 1.60), z=(0.0, 1.9), kind="counter"),
        fx("N-back-door", "back", "a plain painted door to the stockroom (flat, 40 mm)", 0.04, x=(1.85, 2.55), z=(0.0, 2.0), kind="door"),
        fx("N-left-racks", "left", "a wall magazine rack seen face-on: covers in rows, 40 mm", 0.04, y=(0.9, 3.5), z=(0.8, 2.0), kind="flat_board"),
        fx("N-right-racks", "right", "a card rack and a postcard board, flat 40 mm, and a wall clock", 0.04, y=(0.9, 3.5), z=(0.8, 2.0), kind="flat_board"),
        fx("N-ceiling-tubes", "ceiling", "three T12 battens", 0.045, x=(-0.75, 0.75), kind="light"),
        fx("N-floor", "floor", "vinyl tile with a worn path and a rubber mat at the door", 0.012, x=(-2.0, 2.0), y=(0.2, 3.8), z=(0.0, 0.012), kind="floor_flat"),
    ],
    "goods": [
        gd("CashRegister_01", 1, "N-back-counter", size=0.42), gd("script:sweet_jars", 10, "N-back-counter", why="screw-lid jars with opaque sweets (the research's method: real opaque contents, solid lid and label, faked rim): ambientCG Candy001 and Candy002 stripes for humbugs; no CC0 model"),
        gd("script:cigarette_packs", 100, "N-back-gantry", why="bevelled boxes with the label atlas's tobacco tiles (fictional makers), the Poly Haven cigarette_pack is used only as the shape; the model's own 'Kentucky Ace' face is not used"),
        gd("cigarette_pack", 8, "N-back-gantry", size=0.10, note="shape only: its face replaced by the atlas"),
        gd("script:magazine_covers", 60, "N-left-racks", why="flat covers drawn by script: invented titles, no real magazine, no children, no betting or drink content, halftone pictures of objects and landscapes"),
        gd("script:greeting_cards", 40, "N-right-racks", why="flat cards with invented seaside and flower art"), gd("wall_clock", 1, "N-right-racks", size=0.30, note="dial maker mark painted out"),
        gd("stationery_supplies", 3, "N-back-counter"), gd("office_notepads", 4, "N-back-counter"),
    ],
    "display": {
        "keeps": "the 4.2/4.4 window board SB1 (hand cards) on the glass; the sweets, papers and cigarettes trade",
        "changes": "magazines and newspapers are real thin meshes 2 to 4 mm with a curl and a fold; a card rack of fictional cards; no card floats in front of the glass",
        "u_range": [0.0, 3.35], "depth": 0.55, "height_max_w": 1.50,
        "items": [
            di("script:newspapers", 10, [0.1, 1.2, 0.20, 0.50, 0.0, 0.05], why="folded dailies 4 mm thick in a stepped row with invented mastheads and headlines (the street's own paper, no real titles)"),
            di("script:magazines", 24, [1.3, 2.3, 0.12, 0.50, 0.05, 0.40], why="fanned magazine covers 3 mm: generated pages, no children, no betting"),
            di("script:sweet_jars", 6, [2.4, 3.3, 0.15, 0.45, 0.0, 0.26], why="the same jars as the room's, a lid and a label each"),
            di("script:cigarette_cartons", 6, [0.2, 0.9, 0.30, 0.50, 0.40, 0.52], why="cartons with atlas tiles: tobacco is allowed"),
            di("script:card_rack", 1, [2.4, 3.3, 0.30, 0.50, 0.30, 1.10], why="a wire spinner rack of fictional greetings cards: geometry from dimensions"),
            di("stationery_supplies", 2, [0.2, 0.9, 0.10, 0.28, 0.0, 0.16]), di("office_notepads", 3, [1.0, 1.7, 0.08, 0.30, 0.0, 0.02]),
            di("script:postcard_rack", 1, [1.2, 2.0, 0.35, 0.50, 0.50, 1.20], why="a turning rack with invented seaside postcards (PH postcard_set_01's pictures are world landmarks and are not used)"),
        ],
        "night": "the roller shutter (2.2's alterations.roller_shutter) lowered when shut: not used in the lit view",
    },
}
