"""The thirteen rooms behind the street's house windows (cloud week 42, unit 8): what each holds, where, and the rule that decides what may be painted.
Room frame: x across from the room's centre, + toward the PICTURE's right; y back from the card plane (0) to the back wall (D); z up from the floor.
Objects are placed by their footprint (w across, d deep, h high, from the Poly Haven catalogue's dimensions, real scale) and carry the surface they
stand on and their stand-off from it (the depth of what sticks out). The class follows from the budgets of hw_common (true: reads true at 20 pixels
of slide; tolerated: 40 pixels; a stand-off over the tolerated budget is not drawn)."""

# budgets used as the RULE (the smaller of the two room families' computed ones, rounded down); the computed tables are in target.json
BUDGET = {
    "back": {"true": 0.40, "tolerated": 0.80},
    "side": {"true": 0.03, "tolerated": 0.06},
    "ceiling": {"true": 0.03, "tolerated": 0.06},
    "floor": {"true": 0.018, "tolerated": 0.037},
}

FINISH = {
    "emulsion_magnolia": {"base_lin": [0.60, 0.52, 0.38], "texture": "painted_plaster_wall", "rough": 0.8, "what": "matt magnolia emulsion"},
    "emulsion_cream": {"base_lin": [0.66, 0.60, 0.42], "texture": "plastered_wall_04", "rough": 0.8, "what": "matt cream emulsion"},
    "emulsion_pale_green": {"base_lin": [0.40, 0.48, 0.36], "texture": "plastered_wall_04", "rough": 0.8, "what": "pale green emulsion (a landing)"},
    "wallpaper_floral": {"base_lin": [0.42, 0.33, 0.26], "texture": "floral_jacquard", "tile_m": 0.55, "rough": 0.7, "what": "a damask-pattern paper from the jacquard texture tinted fawn"},
    "wallpaper_stripe": {"base_lin": [0.55, 0.50, 0.36], "texture": None, "stripe_period_mm": 90, "stripe_alt": [0.40, 0.34, 0.24], "rough": 0.7, "what": "a script-drawn vertical stripe: cream and fawn, 90 mm period"},
    "stripped_paper": {"base_lin": [0.30, 0.27, 0.22], "texture": "decrepit_wallpaper", "rough": 0.9, "what": "old paper stripped in strips, bare plaster between"},
    "peeling_paint": {"base_lin": [0.38, 0.22, 0.20], "texture": "peeling_painted_wall", "rough": 0.9, "what": "paint peeling to grey plaster"},
    "ceiling_white": {"base_lin": [0.72, 0.70, 0.64], "texture": "ceiling_interior", "rough": 0.9, "what": "white emulsion on a textured ceiling, yellowed by tobacco in the lived-in rooms (x 0.92)"},
    "boards": {"base_lin": [0.20, 0.12, 0.06], "texture": "old_wooden_floor_02", "rough": 0.6, "what": "dark-stained floorboards"},
    "carpet_brown": {"base_lin": [0.12, 0.08, 0.05], "texture": "dirty_carpet", "rough": 0.95, "what": "a worn brown carpet tinted from the dirty-carpet texture"},
    "lino": {"base_lin": [0.30, 0.20, 0.10], "texture": "linoleum_brown", "rough": 0.5, "what": "brown linoleum (a landing)"},
}

# scripted flat forms (named); every one under the side/ceiling tolerated budget (0.06)
FORMS = {
    "skirting": {"h": 0.15, "proud": 0.020, "surface": "side+back", "note": "painted white, on all three walls"},
    "picture_rail": {"h": 0.040, "proud": 0.020, "z": 2.15, "surface": "side+back"},
    "coving": {"h": 0.055, "proud": 0.055, "surface": "ceiling edge", "note": "tolerated class (0.055 under 0.06)"},
    "ceiling_rose": {"d": 0.30, "proud": 0.030, "surface": "ceiling", "note": "a plaster rose at the pendant's place"},
    "bare_bulb": {"d": 0.06, "proud": 0.03, "surface": "ceiling", "note": "a flat glowing disc (a pendant of bare bulb on its flex: the flex is not drawn)"},
    "fire_surround_flat": {"w": 1.30, "h": 1.10, "proud": 0.03, "surface": "side", "note": "a tiled fire surround drawn flat (the real one stands 0.18 off the wall: over the budget)"},
    "internal_door_flat": {"w": 0.78, "h": 1.98, "proud": 0.02, "surface": "back or side", "note": "a four-panel internal door, panels 0.02 proud"},
    "radiator_flat": {"w": 0.80, "h": 0.55, "proud": 0.03, "surface": "side", "note": "a pressed-steel radiator drawn flat (the real one stands 0.08 off: tolerated, over true)"},
    "stair_flat": {"proud": 0.03, "surface": "side", "note": "the stringer and handrail of the flight along the side wall drawn as flat strips (the handrail 0.9 to 1.0 above the nosings, rising 36 degrees); balusters not drawn"},
    "chimney_breast_flat": {"w": 1.20, "h": 2.55, "proud": 0.03, "surface": "back", "note": "a chimney breast drawn flat (the real one stands 0.23 off the wall)"},
    "picture_ghost": {"w": 0.45, "h": 0.60, "proud": 0.0, "surface": "back", "note": "a pale rectangle on a stripped wall where a picture hung (painted, no stand-off)"},
}

# model placements: id, surface, x (centre, across), z0 (height of its base above the floor), plus footprint from the catalogue (filled by make_target)
# class is derived from the stand-off = the model's depth for back-wall pieces, its thickness for wall-hung ones
ROOMS = {
    # ---- upper-floor lounges (UP family: W 2.8, H 2.55, D 4.2); what shows from the street: the ceiling, the back wall above 1.4 m, the side walls above 0.8 m
    "up_lounge_1": {"family": "UP", "type": "lounge", "variant": 1, "walls": "wallpaper_floral", "ceiling": "ceiling_white", "floor": "boards",
                    "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                    "objects": [
                        {"model": "wooden_bookshelf_worn", "surface": "back", "x": -0.70, "z0": 0.0},
                        {"model": "ornate_mirror_01", "surface": "back", "x": 0.55, "z0": 1.18},
                        {"model": "hanging_picture_frame_03", "surface": "left", "y": 2.0, "z0": 1.45},
                    ], "pendant": True},
    "up_lounge_2": {"family": "UP", "type": "lounge", "variant": 2, "walls": "emulsion_magnolia", "ceiling": "ceiling_white", "floor": "boards",
                    "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                    "objects": [
                        {"model": "vintage_cabinet_01", "surface": "back", "x": -0.20, "z0": 0.0},
                        {"model": "mantel_clock_01", "surface": "back", "x": 0.30, "z0": 2.235, "on": "vintage_cabinet_01"},
                        {"model": "hanging_picture_frame_01", "surface": "right", "y": 1.6, "z0": 1.30},
                    ], "pendant": True},
    "up_lounge_3": {"family": "UP", "type": "lounge", "variant": 3, "walls": "wallpaper_stripe", "ceiling": "ceiling_white", "floor": "carpet_brown",
                    "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                    "objects": [
                        {"model": "Shelf_01", "surface": "back", "x": 0.85, "z0": 0.0},
                        {"model": "hanging_picture_frame_02", "surface": "back", "x": -0.55, "z0": 1.45},
                        {"model": "wall_clock", "surface": "left", "y": 1.2, "z0": 1.75},
                    ], "pendant": True},
    # ---- upper-floor bedrooms
    "up_bedroom_1": {"family": "UP", "type": "bedroom", "variant": 1, "walls": "wallpaper_floral", "ceiling": "ceiling_white", "floor": "carpet_brown",
                     "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                     "objects": [
                         {"model": "vintage_cabinet_01", "surface": "back", "x": 0.35, "z0": 0.0},
                         {"model": "hanging_picture_frame_03", "surface": "back", "x": -0.95, "z0": 1.45},
                     ], "pendant": True},
    "up_bedroom_2": {"family": "UP", "type": "bedroom", "variant": 2, "walls": "emulsion_cream", "ceiling": "ceiling_white", "floor": "boards",
                     "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                     "objects": [
                         {"model": "drawer_cabinet", "surface": "back", "x": -0.55, "z0": 0.0},
                         {"model": "ornate_mirror_01", "surface": "back", "x": 0.60, "z0": 1.25},
                         {"model": "hanging_picture_frame_01", "surface": "left", "y": 2.2, "z0": 1.30},
                     ], "pendant": True},
    "up_bedroom_3": {"family": "UP", "type": "bedroom", "variant": 3, "walls": "wallpaper_stripe", "ceiling": "ceiling_white", "floor": "carpet_brown",
                     "forms": ["skirting", "picture_rail", "coving", "ceiling_rose"],
                     "objects": [
                         {"model": "Shelf_01", "surface": "back", "x": -0.75, "z0": 0.0},
                         {"model": "hanging_picture_frame_03", "surface": "back", "x": 0.45, "z0": 1.50},
                         {"model": "wall_clock", "surface": "right", "y": 1.5, "z0": 1.80},
                     ], "pendant": True},
    # ---- stair landings
    "up_landing_1": {"family": "UP", "type": "landing", "variant": 1, "walls": "emulsion_pale_green", "ceiling": "ceiling_white", "floor": "lino",
                     "forms": ["skirting", "picture_rail", "coving", "stair_flat", "internal_door_flat", "bare_bulb"],
                     "objects": [
                         {"model": "hanging_picture_frame_01", "surface": "left", "y": 2.9, "z0": 1.55},
                         {"model": "wall_clock", "surface": "back", "x": 0.60, "z0": 1.85},
                     ], "pendant": False},
    "up_landing_2": {"family": "UP", "type": "landing", "variant": 2, "walls": "emulsion_cream", "ceiling": "ceiling_white", "floor": "lino",
                     "forms": ["skirting", "picture_rail", "coving", "radiator_flat", "bare_bulb"],
                     "objects": [
                         {"model": "Shelf_01", "surface": "back", "x": -0.80, "z0": 0.0},
                         {"model": "hanging_picture_frame_02", "surface": "back", "x": 0.50, "z0": 1.45},
                     ], "pendant": False},
    # ---- empty rooms of an unlet flat
    "up_empty_1": {"family": "UP", "type": "empty", "variant": 1, "walls": "stripped_paper", "ceiling": "ceiling_white", "floor": "boards",
                   "forms": ["skirting", "coving", "chimney_breast_flat", "bare_bulb", "picture_ghost"], "objects": [], "pendant": False},
    "up_empty_2": {"family": "UP", "type": "empty", "variant": 2, "walls": "peeling_paint", "ceiling": "ceiling_white", "floor": "boards",
                   "forms": ["skirting", "coving", "bare_bulb", "radiator_flat"], "objects": [], "pendant": False},
    # ---- cottage front rooms (GF family: W 3.4, H 2.6, D 4.2); eye-level views: the whole back wall shows
    "gf_front_1": {"family": "GF", "type": "front_room", "variant": 1, "walls": "wallpaper_floral", "ceiling": "ceiling_white", "floor": "carpet_brown",
                   "forms": ["skirting", "picture_rail", "coving", "ceiling_rose", "fire_surround_flat"],
                   "objects": [
                       {"model": "Sofa_01", "surface": "back", "x": -0.60, "z0": 0.0},
                       {"model": "side_table_01", "surface": "back", "x": 0.95, "z0": 0.0},
                       {"model": "television_02", "surface": "back", "x": 0.95, "z0": 0.45, "on": "side_table_01"},
                       {"model": "hanging_picture_frame_02", "surface": "back", "x": -0.60, "z0": 1.35},
                       {"model": "hanging_picture_frame_03", "surface": "left", "y": 1.9, "z0": 1.35},
                   ], "pendant": True, "tv_glow": True},
    "gf_front_2": {"family": "GF", "type": "front_room", "variant": 2, "walls": "emulsion_magnolia", "ceiling": "ceiling_white", "floor": "boards",
                   "forms": ["skirting", "picture_rail", "coving", "ceiling_rose", "internal_door_flat"],
                   "objects": [
                       {"model": "wooden_bookshelf_worn", "surface": "back", "x": -1.00, "z0": 0.0},
                       {"model": "ArmChair_01", "surface": "back", "x": 0.30, "z0": 0.0},
                       {"model": "potted_plant_01", "surface": "back", "x": 1.30, "z0": 0.0},
                       {"model": "ornate_mirror_01", "surface": "right", "y": 2.1, "z0": 1.10},
                   ], "pendant": True, "tv_glow": False},
    "gf_front_3": {"family": "GF", "type": "front_room", "variant": 3, "walls": "wallpaper_stripe", "ceiling": "ceiling_white", "floor": "carpet_brown",
                   "forms": ["skirting", "picture_rail", "coving", "ceiling_rose", "fire_surround_flat"],
                   "objects": [
                       {"model": "painted_wooden_cabinet", "surface": "back", "x": -0.70, "z0": 0.0},
                       {"model": "mantel_clock_01", "surface": "back", "x": -1.00, "z0": 1.18, "on": "painted_wooden_cabinet"},
                       {"model": "vintage_oil_lamp", "surface": "back", "x": -0.35, "z0": 1.18, "on": "painted_wooden_cabinet"},
                       {"model": "painted_wooden_bench", "surface": "back", "x": 0.95, "z0": 0.0},
                       {"model": "hanging_picture_frame_01", "surface": "back", "x": 0.95, "z0": 1.30},
                   ], "pendant": True, "tv_glow": False},
}

# who has which room: set per site in make_target (SITE_PLAN)
