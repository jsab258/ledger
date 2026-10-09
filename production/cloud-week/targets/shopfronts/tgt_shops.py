"""The ten fronts of Quay Street, their paints, their alterations and the assembly arithmetic.
Millimetres, the game's viewer frame (u from the viewer's left). Read by make_target.py."""
from tgt_parts import BAY, SIDE_SLOT, SHOP_SLOT, SLOT, ZONE

# ---- paints (sRGB 0-255, aged to 1990; fresh values are the fascia target's where it has them) ---------
PAINTS = {
    "oxblood": {"srgb": [93, 46, 49], "plain": "oxblood", "rough": 0.45, "metal": 0.0, "kind": "Scaled",
                "note": "the fascia target's aged oxblood (the game's Rita board today is 92,39,43); the street's linear 0.105, 0.020, 0.024 is sRGB 91, 40, 44"},
    "white_joinery": {"srgb": [226, 224, 214], "plain": "gloss white, yellowed", "rough": 0.50, "metal": 0.0, "kind": "Judgement",
                      "note": "the front-door target's aged white (P1 240,239,245 fresh, P2 222,225,229 old)"},
    "cream": {"srgb": [222, 209, 175], "plain": "cream", "rough": 0.50, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's aged cream"},
    "door_cream": {"srgb": [222, 212, 184], "plain": "buttermilk cream", "rough": 0.50, "metal": 0.0, "kind": "Scaled",
                   "note": "Rita's side door in the game's frame (rita-day-kit-2026-10-06.jpg)"},
    "bare_timber": {"srgb": [46, 37, 30], "plain": "bare soot-darkened timber", "rough": 0.85, "metal": 0.0, "kind": "Scaled", "note": "terrace-front.py bare_timber, aged"},
    "bleached_white": {"srgb": [170, 166, 156], "plain": "old white, flaked to grey", "rough": 0.75, "metal": 0.0, "kind": "Judgement",
                       "note": "the empty unit's window joinery: a paint of the 1960s, chalking, half gone"},
    "dark_green": {"srgb": [30, 62, 44], "plain": "dark green", "rough": 0.45, "metal": 0.0, "kind": "Judgement",
                   "note": "the front-door target's dark green 28,59,41, lifted a step for 1990 fading"},
    "navy": {"srgb": [44, 53, 83], "plain": "navy", "rough": 0.45, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's aged navy"},
    "slate": {"srgb": [62, 75, 87], "plain": "slate blue-grey", "rough": 0.55, "metal": 0.0, "kind": "Sheet", "note": "the Hook sheet's Mickey's board, mean 62,75,87"},
    "dove_grey": {"srgb": [150, 152, 150], "plain": "dove grey", "rough": 0.50, "metal": 0.0, "kind": "Judgement", "note": "a 1980s repaint, chosen to sit with the red box sign"},
    "brown": {"srgb": [120, 74, 44], "plain": "mid brown", "rough": 0.45, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's tea-room panel colour, aged"},
    "pale_grey": {"srgb": [196, 202, 206], "plain": "pale grey-white", "rough": 0.55, "metal": 0.0, "kind": "Sheet", "note": "the fascia target's fish board, aged (the Hook sheet's white fascia is 204,204,204)"},
    "black_door": {"srgb": [35, 36, 40], "plain": "gloss black, faintly blue", "rough": 0.40, "metal": 0.0, "kind": "Photo", "note": "the front-door target's P2 median (39,40,45)"},
    "dark_brown": {"srgb": [74, 48, 34], "plain": "dark brown", "rough": 0.45, "metal": 0.0, "kind": "Judgement", "note": "the front-door target's brown"},
    "dark_blue": {"srgb": [24, 38, 78], "plain": "dark blue", "rough": 0.45, "metal": 0.0, "kind": "Judgement", "note": "the front-door target's dark blue"},
    "alu_natural": {"srgb": [176, 178, 180], "plain": "natural anodised aluminium, dulled", "rough": 0.38, "metal": 0.9, "kind": "Judgement",
                    "note": "1960s-80s extrusions; the fish front's pale frames in shop-fronts-whole-2026-10-08.jpg"},
    "alu_bronze": {"srgb": [84, 68, 53], "plain": "bronze anodised aluminium", "rough": 0.40, "metal": 0.85, "kind": "Scaled", "note": "the fascia target's bronze_anodised returns"},
    "bronze_plate": {"srgb": [110, 86, 50], "plain": "bronze-plated bar, tarnished", "rough": 0.40, "metal": 0.9, "kind": "Judgement", "note": "1930s bars; the grocer"},
    "powder_slate": {"srgb": [60, 74, 88], "plain": "slate powder-coat on steel", "rough": 0.40, "metal": 0.3, "kind": "Sheet", "note": "Mickey's refit frame (terrace-front.py frame_painted)"},
    "tile_white": {"srgb": [228, 228, 220], "plain": "white glazed tile, grout grey", "rough": 0.12, "metal": 0.0, "kind": "Judgement", "note": "a fishmonger's and a launderette's tile"},
    "tile_green": {"srgb": [170, 190, 172], "plain": "pale green glazed tile", "rough": 0.12, "metal": 0.0, "kind": "Judgement", "note": "the chandler's plain glazed tile"},
    "glass_green": {"srgb": [36, 61, 49], "plain": "bottle green opaque glass", "rough": 0.08, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's deco_green_glass, aged"},
    "tile_cream": {"srgb": [222, 212, 184], "plain": "cream glazed tile", "rough": 0.12, "metal": 0.0, "kind": "Judgement", "note": "Mickey's patterned tile, ground"},
    "tile_blue": {"srgb": [46, 68, 136], "plain": "mid blue glaze", "rough": 0.12, "metal": 0.0, "kind": "Judgement", "note": "Mickey's patterned tile, motif"},
    "tile_black": {"srgb": [30, 30, 32], "plain": "black glaze", "rough": 0.12, "metal": 0.0, "kind": "Judgement", "note": "skirting courses"},
    "buff_board": {"srgb": [188, 173, 136], "plain": "buff", "rough": 0.50, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's aged buff board"},
    "whitewash": {"srgb": [214, 212, 204], "plain": "whitewash on the glass, streaky", "rough": 0.9, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's whitewash"},
    "brass": {"srgb": [160, 120, 55], "plain": "aged brass", "rough": 0.38, "metal": 1.0, "kind": "Judgement", "note": "the kit's brass: linear 0.55, 0.40, 0.17 (sRGB 194,170,112 lit), here the worn mid-tone"},
    "chrome": {"srgb": [170, 172, 174], "plain": "chrome, spotted", "rough": 0.20, "metal": 1.0, "kind": "Judgement", "note": "the kit's chrome"},
    "terrazzo": {"srgb": [190, 184, 170], "plain": "grey terrazzo with white chips", "rough": 0.30, "metal": 0.0, "kind": "Judgement", "note": "the kit's terrazzo threshold"},
    "acrylic_white": {"srgb": [225, 217, 197], "plain": "white acrylic, yellowed", "rough": 0.30, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's acrylic_white, aged"},
    "acrylic_red": {"srgb": [197, 75, 62], "plain": "red acrylic face, faded", "rough": 0.30, "metal": 0.0, "kind": "Scaled", "note": "the fascia target's vermilion, aged (the newsagent's box face)"},
    "powder_black": {"srgb": [37, 35, 34], "plain": "black powder-coat", "rough": 0.40, "metal": 0.2, "kind": "Scaled", "note": "the fascia target's shade black; the newsagent box's returns"},
    "steel_grey": {"srgb": [88, 90, 90], "plain": "galvanised steel, painted grey", "rough": 0.55, "metal": 0.6, "kind": "Judgement", "note": "roller shutter box and curtain"},
}

# ---- the layout arithmetic -----------------------------------------------------------------------
def layout(door_end, side_door):
    """u-intervals of the three zones between the piers. door_end is the VIEWER's side the doors are on."""
    L0, R0 = SLOT, BAY - SLOT
    if door_end == "L":
        if side_door:
            return {"side_door": [L0, L0 + SIDE_SLOT], "shop_door": [L0 + SIDE_SLOT, L0 + SIDE_SLOT + SHOP_SLOT],
                    "window": [L0 + SIDE_SLOT + SHOP_SLOT, R0]}
        return {"side_door": None, "shop_door": [L0, L0 + SHOP_SLOT], "window": [L0 + SHOP_SLOT, R0]}
    if side_door:
        return {"window": [L0, R0 - SIDE_SLOT - SHOP_SLOT], "shop_door": [R0 - SIDE_SLOT - SHOP_SLOT, R0 - SIDE_SLOT],
                "side_door": [R0 - SIDE_SLOT, R0]}
    return {"window": [L0, R0 - SHOP_SLOT], "shop_door": [R0 - SHOP_SLOT, R0], "side_door": None}


def street_x(side, x_low, x_high, u):
    """street x for a bay u: east parade u grows as street x FALLS (low street x is the viewer's right);
    the west block's u grows as street x rises (the fascia target's axis rule)."""
    return round((x_high - u / 1000.0) if side == "east" else (x_low + u / 1000.0), 3)


def window_layout(length, n_mull, mull_w, jamb_w, tl_n, tl_bar_w, aligned=False):
    """Mullion and toplight-bar centres (mm from the window frame's left edge) and the light widths."""
    clear = length - 2 * jamb_w
    light = (clear - n_mull * mull_w) / (n_mull + 1)
    mulls = [round(jamb_w + light * (k + 1) + mull_w * k + mull_w / 2, 1) for k in range(n_mull)]
    if aligned:
        bars = list(mulls)
        tl_light = light
    else:
        tl_light = (clear - (tl_n - 1) * tl_bar_w) / tl_n
        bars = [round(jamb_w + tl_light * (k + 1) + tl_bar_w * k + tl_bar_w / 2, 1) for k in range(tl_n - 1)]
    return {"mullion_centres": mulls, "light_width": round(light, 1), "toplight_bar_centres": bars,
            "toplight_width": round(tl_light, 1), "toplights": (len(bars) + 1)}


def shop(id_, order, trade, block, bay, side, x_low, x_high, door_end, side_door, kind, **kw):
    lay = layout(door_end, side_door)
    win = lay["window"]
    d = {
        "id": id_, "order": order, "trade": trade, "block": block, "bay": bay, "side": side, "street_x_m": [x_low, x_high],
        "kind": kind, "door_end_viewer": door_end,
        "door_end_street": (("low" if door_end == "R" else "high") if side == "east" else ("low" if door_end == "L" else "high")),
        "recipe_doors_on": "left" if door_end == "R" else "right",
        "side_door": side_door, "zones_u": lay,
        "window_length": round(win[1] - win[0], 1),
        "centres_street_x_m": {
            "window": street_x(side, x_low, x_high, (win[0] + win[1]) / 2),
            "shop_door": street_x(side, x_low, x_high, sum(lay["shop_door"]) / 2),
            "side_door": street_x(side, x_low, x_high, sum(lay["side_door"]) / 2) if lay["side_door"] else None},
    }
    d.update(kw)
    opp = "R" if door_end == "L" else "L"
    # the door handing, from Rita's front in the game today (rita-day-kit-2026-10-06.jpg): both leaves' levers / knobs are on the leaf's
    # edge toward the door end (the viewer's left in Rita's), so both are hinged on the opposite edge (the window / shop-door side)
    d["shop_door_hinge_viewer"] = opp
    d["shop_door_lever_viewer"] = door_end
    d["side_door_hinge_viewer"] = opp if side_door else None
    d["side_door_knob_viewer"] = door_end if side_door else None
    d["letter_plate_viewer"] = "centre"
    d["shop_door_glass_foot_z"] = {"T1": 600.0, "M2": 600.0, "M1": 198.0}[d["shop_door"]]
    d["door_glass_rule_applies"] = d["shop_door"] in ("T1", "M2")
    return d


def fronts():
    S = []
    S.append(shop("mickeys", 0, "minicab office (Mickey's)", "east_parade", 0, "east", 3.0, 9.0, "R", True,
                  "A2 painted-steel refit (1970s)",
                  original_or_altered="altered",
                  alterations=["steel_refit", "repaint"],
                  stallriser={"variant": "tile_patterned", "paint": "tile_cream", "motif": "tile_blue", "skirting": "tile_black", "height": 600},
                  lobby={"kind": "flush", "note": "kept as built and walked (mickeys-office.json: the leaf at depth 5.0, 0.125 proud of the wall); the Hook sheet's recessed Mickey's door is NOT adopted (see could_not_settle)"},
                  glazing={"pattern": "3L-3T-aligned", "window_frame": "M1", "mullion": "M1", "mullion_face": 50, "n_mullions": 2,
                           "toplights": 3, "toplight_aligned": True, "glazing": "gasket, snap-in bead, 6 mm plate"},
                  pilaster="clad", console="scroll", cornice="timber",
                  shop_door="M1", side_door_variant="F1",
                  paints={"pilaster": "slate", "console": "slate", "cornice": "slate", "fascia_board": "slate", "stallriser": "tile_cream",
                          "window_frame": "powder_slate", "shop_door": "powder_slate", "side_door": "oxblood", "metal": "chrome"},
                  fascia_target_id="mickeys",
                  notes="The approved sheet's front: slate blue-grey frame on a patterned tile, the piers and fascia painted as a unit. The old board stays under."))
    S.append(shop("fish_market", 1, "fishmonger (Fish Market)", "east_parade", 1, "east", 9.0, 15.0, "R", True,
                  "A1 aluminium replacement front (1970s) in an older frame",
                  original_or_altered="altered",
                  alterations=["aluminium_refit", "repaint"],
                  stallriser={"variant": "tile_square", "paint": "tile_white", "skirting": "tile_black", "height": 600,
                              "note": "washable white glazed tile (the fishmonger research); a marble slab sill inside the glass, not modelled"},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "4L-4T-aligned", "window_frame": "M1", "mullion": "M1", "mullion_face": 50, "n_mullions": 3,
                           "toplights": 4, "toplight_aligned": True, "glazing": "gasket, snap-in bead, 6 mm plate, whitewash lettering on the glass (fascia target)"},
                  pilaster="panel", console="scroll", cornice="timber",
                  shop_door="M1", side_door_variant="F1",
                  paints={"pilaster": "pale_grey", "console": "pale_grey", "cornice": "pale_grey", "fascia_board": "pale_grey", "stallriser": "tile_white",
                          "window_frame": "alu_natural", "shop_door": "alu_natural", "side_door": "black_door", "metal": "chrome"},
                  fascia_target_id="fish_market",
                  notes="The old timber pilasters and consoles stay, repainted pale to match the new board; the window and door were replaced in aluminium."))
    S.append(shop("ritas", 2, "pawnbroker (Rita's)", "east_parade", 2, "east", 15.0, 21.0, "L", True,
                  "O original timber front, repainted (the model)",
                  original_or_altered="original",
                  alterations=["repaint"],
                  stallriser={"variant": "panel", "paint": "oxblood", "height": 600, "panels": 3},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "3L-8T", "window_frame": "T1", "mullion": "T1", "mullion_face": 70, "n_mullions": 2,
                           "toplights": 8, "toplight_aligned": False, "glazing": "ovolo beads, 6 mm plate; a lattice grille at night is the shop-room's, not the joinery's"},
                  pilaster="panel", console="scroll", cornice="timber",
                  shop_door="T1", side_door_variant="F1",
                  paints={"pilaster": "oxblood", "console": "oxblood", "cornice": "oxblood", "fascia_board": "oxblood", "stallriser": "oxblood",
                          "window_frame": "white_joinery", "shop_door": "white_joinery", "side_door": "door_cream", "metal": "brass"},
                  fascia_target_id="ritas",
                  notes="Rita's window is the model (Jafar, 2 October). Oxblood on piers, consoles, fascia and stallriser, white joinery inside, the side door in the door paint, brass fittings."))
    S.append(shop("empty_unit", 3, "empty unit to let", "east_parade", 3, "east", 21.0, 27.0, "R", True,
                  "E empty original front, paint gone, glass whitewashed",
                  original_or_altered="original",
                  alterations=["empty_unit"],
                  stallriser={"variant": "boarded", "paint": "bare_timber", "height": 600},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "3L-8T", "window_frame": "T2", "mullion": "T2", "mullion_face": 80, "n_mullions": 2,
                           "toplights": 8, "toplight_aligned": False, "glazing": "old putty, cracked; every pane whitewashed from inside"},
                  pilaster="panel", console="scroll", cornice="timber",
                  shop_door="T1", side_door_variant="F1",
                  console_absent_viewer="L",
                  paints={"pilaster": "bare_timber", "console": "bare_timber", "cornice": "bare_timber", "fascia_board": "bare_timber", "stallriser": "bare_timber",
                          "window_frame": "bleached_white", "shop_door": "black_door", "side_door": "black_door", "metal": "brass"},
                  fascia_target_id="empty_unit",
                  whitewash={"over": "every pane of the window and the shop door's glass", "colour": "whitewash"},
                  notes="The left console (high street x, viewer's left: u 55 to 295) was clipped off and never put back (fascia-01 spec, bay x 26.825). The street draws this front bare."))
    S.append(shop("steam_laundry", 4, "launderette (Steam Laundry)", "east_parade", 4, "east", 27.0, 33.0, "L", True,
                  "A1 aluminium replacement front (1980s) with a plastic box sign",
                  original_or_altered="altered",
                  alterations=["aluminium_refit", "box_sign", "recessed_lobby", "repaint"],
                  stallriser={"variant": "tile_square", "paint": "tile_white", "skirting": "tile_black", "height": 600},
                  lobby={"kind": "recessed", "depth": 300, "splay_deg": 0, "floor": "quarry tile 150 square, red-brown, with a brass nosing",
                         "note": "a shallow recess for the glass door, 300 deep, the window's end returned square in the same frame"},
                  glazing={"pattern": "2L-1T", "window_frame": "M1", "mullion": "M1", "mullion_face": 50, "n_mullions": 1,
                           "toplights": 1, "toplight_aligned": False, "glazing": "gasket, snap-in bead, 6 mm plate; one long toplight pane over both lights"},
                  pilaster="render", console="scroll", cornice="timber",
                  shop_door="M1", side_door_variant="F1",
                  paints={"pilaster": "cream", "console": "cream", "cornice": "cream", "fascia_board": "cream", "stallriser": "tile_white",
                          "window_frame": "alu_bronze", "shop_door": "alu_bronze", "side_door": "dark_brown", "metal": "chrome"},
                  fascia_target_id="steam_laundry",
                  fascia_sign={"kind": "box_sign", "u": [400.0, 5600.0], "z": [2885.0, 3365.0], "depth": 150.0, "front_d": 270.0, "face": "acrylic_white", "returns": "alu_bronze", "source": "the fascia target (steam_laundry_box: outer 105, 35, 5305, 515)"},
                  notes="The lit box sign (fascia target: 5200 x 480 x 150, bronze returns) stands on the old cream board between the consoles."))
    S.append(shop("grocer", 5, "grocer", "east_parade", 5, "east", 33.0, 39.0, "L", False,
                  "R 1930s refit: bronze bars, glass stallriser, deep recessed lobby",
                  original_or_altered="altered",
                  alterations=["refit_1930s", "recessed_lobby", "repaint"],
                  stallriser={"variant": "slab", "paint": "glass_green", "height": 600},
                  lobby={"kind": "recessed", "depth": 600, "splay_deg": 0, "floor": "terrazzo, grey with white chips, a 150 mosaic border in cream and green",
                         "window_side_return": "glazed display return, frame 28, kick panel 600 in the green glass",
                         "pier_side_return": "panelled lining, painted cream",
                         "ceiling": "plaster, one pendant opal globe (not modelled)",
                         "door_frame_front_d": -500,
                         "note": "no side door on this bay (the street recipe's BAY_WITHOUT_SIDE_DOOR = 5; terrace-fronts.md): the flat is reached from the rear yard"},
                  glazing={"pattern": "3L-5T-sunrise", "window_frame": "M2", "mullion": "M2", "mullion_face": 28, "n_mullions": 2,
                           "toplights": 5, "toplight_aligned": False, "glazing": "plate glass in bronze-plated bars; the toplights etched with a sunrise (5 sectors)"},
                  pilaster="render", console="block", cornice="timber",
                  shop_door="M2", side_door_variant=None,
                  paints={"pilaster": "cream", "console": "cream", "cornice": "cream", "fascia_board": "glass_green", "stallriser": "glass_green",
                          "window_frame": "bronze_plate", "shop_door": "bronze_plate", "side_door": None, "metal": "chrome"},
                  fascia_target_id="grocer",
                  notes="The fascia target's three-slab glass board (bottle green, cream letters) fixes this front's date. The consoles are plain blocks; the window is 4294 wide."))
    S.append(shop("chandler", 6, "ship's chandler", "east_chandler", 0, "east", 40.0, 46.0, "L", True,
                  "A1 aluminium replacement front (1970s), plain glazed tile",
                  original_or_altered="altered",
                  alterations=["aluminium_refit", "repaint"],
                  stallriser={"variant": "tile_square", "paint": "tile_green", "skirting": "tile_black", "height": 600},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "3L-3T-aligned", "window_frame": "M1", "mullion": "M1", "mullion_face": 50, "n_mullions": 2,
                           "toplights": 3, "toplight_aligned": True, "glazing": "gasket, snap-in bead, 6 mm plate"},
                  pilaster="panel", console="scroll", cornice="timber",
                  shop_door="M1", side_door_variant="F1",
                  paints={"pilaster": "navy", "console": "navy", "cornice": "navy", "fascia_board": "navy", "stallriser": "tile_green",
                          "window_frame": "alu_natural", "shop_door": "alu_natural", "side_door": "navy", "metal": "chrome"},
                  fascia_target_id="chandler",
                  notes="D06 gave the Hook's shops a metal refit; R05's plain glazed tile under the glass (terrace-front.py SHOPFRONT_REFITS)."))
    S.append(shop("tea_rooms", 7, "tea room", "west_north", 2, "west", 24.0, 30.0, "L", True,
                  "O original timber front, repainted, with a flat panel over the fascia",
                  original_or_altered="original",
                  alterations=["repaint", "flat_panel_sign"],
                  stallriser={"variant": "render", "paint": "brown", "height": 600},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "3L-6T", "window_frame": "T1", "mullion": "T1", "mullion_face": 70, "n_mullions": 2,
                           "toplights": 6, "toplight_aligned": False, "glazing": "ovolo beads; a brass café-curtain rod across the lower lights at z 1500 (the shop-room's)"},
                  pilaster="flute", console="scroll", cornice="timber",
                  shop_door="T1", side_door_variant="F1",
                  paints={"pilaster": "brown", "console": "brown", "cornice": "brown", "fascia_board": "cream", "stallriser": "brown",
                          "window_frame": "door_cream", "shop_door": "door_cream", "side_door": "dark_brown", "metal": "brass"},
                  fascia_target_id="tea_rooms",
                  fascia_sign={"kind": "flat_panel", "u": [385.0, 5615.0], "z": [2890.0, 3360.0], "depth": 30.0, "front_d": 150.0, "face": "brown", "returns": "white_joinery", "source": "the fascia target (tea_rooms_panel: outer 90, 40, 5320, 510)"},
                  notes="A 1980s caff: the brown acrylic panel on the old board (fascia target), the timber painted brown and cream."))
    S.append(shop("ironmonger", 8, "ironmonger", "west_north", 1, "west", 30.0, 36.0, "R", True,
                  "O original timber front, repainted dark green",
                  original_or_altered="original",
                  alterations=["repaint"],
                  stallriser={"variant": "panel", "paint": "dark_green", "height": 600, "panels": 2},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "2L-5T", "window_frame": "T2", "mullion": "T2", "mullion_face": 80, "n_mullions": 1,
                           "toplights": 5, "toplight_aligned": False, "glazing": "putty-glazed, an old display of two big lights"},
                  pilaster="flute", console="scroll", cornice="timber",
                  shop_door="T1", side_door_variant="F1",
                  paints={"pilaster": "dark_green", "console": "dark_green", "cornice": "dark_green", "fascia_board": "buff_board", "stallriser": "dark_green",
                          "window_frame": "dark_green", "shop_door": "dark_green", "side_door": "black_door", "metal": "brass"},
                  fascia_target_id="ironmonger",
                  notes="The street's recipe has a metal refit here (SHOPFRONT_REFITS west_north 1); the traditional sign-written board in the fascia target is better matched by an original front, so this target keeps it timber. Reported."))
    S.append(shop("newsagent", 9, "newsagent and tobacconist", "west_north", 0, "west", 36.0, 42.0, "R", True,
                  "O original timber front with a plastic box sign and a roller-shutter box",
                  original_or_altered="original",
                  alterations=["repaint", "box_sign", "roller_shutter"],
                  stallriser={"variant": "panel", "paint": "dove_grey", "height": 600, "panels": 3},
                  lobby={"kind": "flush"},
                  glazing={"pattern": "3L-8T", "window_frame": "T1", "mullion": "T1", "mullion_face": 70, "n_mullions": 2,
                           "toplights": 8, "toplight_aligned": False, "glazing": "ovolo beads; the shutter's hood is set into the toplight zone: the head, bars and glass are cut away above 2550 behind it and 70 of the toplights shows"},
                  pilaster="panel", console="scroll", cornice="timber",
                  shop_door="T1", side_door_variant="F1",
                  paints={"pilaster": "dove_grey", "console": "dove_grey", "cornice": "dove_grey", "fascia_board": "cream", "stallriser": "dove_grey",
                          "window_frame": "white_joinery", "shop_door": "dove_grey", "side_door": "dark_blue", "metal": "brass"},
                  fascia_target_id="newsagent",
                  roller_shutter={"over": "window and shop door (u 350 to 4706)", "state": "raised by day: hood and guide rails only; lowered by night (variant shutter_down)"},
                  fascia_sign={"kind": "box_sign", "u": [390.0, 5610.0], "z": [2890.0, 3360.0], "depth": 140.0, "front_d": 260.0, "face": "acrylic_red", "returns": "powder_black", "source": "the fascia target (newsagent_box: outer 95, 40, 5315, 510 on a 5410 x 550 board)"},
                  notes="The lit box sign (fascia target, 5220 x 470 x 140, powder-black returns) stands on the old CREAM board (the fascia target's old_board colour; the board's edges, ends and bed mould are cream like its face), the piers, consoles and cornice dove grey; the steel hood under it over window and door."))
    return S


ALTERATIONS = {
    "repaint": {
        "what": "many coats of gloss over decades: arrises rounded, mouldings clogged, brush marks, runs, crazing on the sunny front, bare grey timber at sills and feet",
        "numbers": {"arris_radius_mm": [1.0, 2.5], "hollow_fill_fraction": 0.4, "coats_visible": "3 to 6", "bare_timber_at": ["sill nose and drip", "plinth feet", "door bottom rails", "transom top"]},
        "applies_to": ["mickeys", "fish_market", "ritas", "steam_laundry", "grocer", "chandler", "tea_rooms", "ironmonger", "newsagent"],
        "applies_to_note": "every timber part of every front except the empty unit, whose paint is gone (it has its own kind)",
        "kind": "Judgement from FRONTAGE-2026-10-06.md section 3 and PAINTED-FRONTS-2026-10-07.md; P1 (Leadenhall) shows 2019 paint, not 1990",
    },
    "aluminium_refit": {
        "what": "a 1960s-80s replacement window and door in anodised aluminium, set in the old frame's opening with the old pilasters, consoles, fascia and cornice kept",
        "numbers": {"stile_mullion_transom_face": 50, "section_depth": 75, "frame_front_d": 75, "glass_d": 30, "wall": 3,
                    "finish": "natural silver or bronze anodised, 15 to 20 micron, dulled and pitted, white corrosion at the foot",
                    "fixings": "self-tapping screws through the stiles into the old jambs at 400, hidden by a snap-on cover cap; corner cleats and a bead of grey mastic visible round the edge against the old timber",
                    "stallriser": "tile or laminate over a stud wall, 600, the tile's cap and a 10 mm aluminium channel",
                    "door": "full-height glass in a 50 aluminium frame, 100 top rail, 170 bottom rail, a 300 chrome D handle and a push plate, a floor spring and a lower tape of rubber"},
        "meets_old_joinery": "the new frame's outer edge covers the old jamb by 12; a 15 x 6 mastic joint round the head under the old fascia's foot; the sill is an aluminium cill 40 proud over the old sill",
        "applies_to": ["fish_market", "steam_laundry", "chandler"],
        "kind": "Judgement; R05 and R09 (the project's earlier reading of Peter Marshall's Hull photographs: metal shopfront, fluorescent strips, patterned tile) say it existed; no photograph reached today",
    },
    "steel_refit": {
        "what": "a 1970s painted steel or aluminium front in slate blue-grey, as the Hook sheet shows; the same sections as the aluminium refit, powder-coated",
        "numbers": {"stile_mullion_transom_face": 50, "section_depth": 75, "finish": "powder-coat, eggshell, slate (60,74,88)"},
        "applies_to": ["mickeys"],
        "kind": "Sheet (mood) and the project's earlier reading of R05",
    },
    "refit_1930s": {
        "what": "a 1930s modernisation: bronze-plated bars 28 x 40, plate glass, a glass stallriser in three slabs, curved or plain recessed lobby with a terrazzo floor, a glass fascia",
        "numbers": {"bar_face": 28, "bar_depth": 40, "glass_thickness": 6, "stallriser_slabs": 3, "joint": 3},
        "applies_to": ["grocer"],
        "kind": "Read (FRONTAGE-2026-10-06.md: HE2 Muswell Hill 1930s, BC2 Lennie 2012: curved glass lobbies, bronze, chrome, coloured structural glass, tiled lobby floors) and the fascia target's glass board",
    },
    "box_sign": {
        "what": "a lit plastic box over the old fascia (fascia target's geometry: laundry 5200 x 480 x 150, newsagent 5220 x 470 x 140); the old board stays under it",
        "numbers": {"stands_proud_of_board": [140, 150], "front_d": [260, 270], "beyond_cornice_nose": [45, 55], "fixings": "eight pan-head screws through the frame into the board",
                    "u_z": {"steam_laundry": {"u": [400, 5600], "z": [2885, 3365]}, "newsagent": {"u": [390, 5610], "z": [2890, 3360]}},
                    "board": "the old CREAM board stays under it on both fronts (the fascia target's old_board colour)"},
        "applies_to": ["steam_laundry", "newsagent"],
        "kind": "the fascia target (Judgement there)",
    },
    "flat_panel_sign": {
        "what": "a flat acrylic panel screwed over the old board (fascia target: 5230 x 470 x 30)",
        "numbers": {"stands_proud_of_board": 30, "front_d": 150, "u_z": {"tea_rooms": {"u": [385, 5615], "z": [2890, 3360]}}, "board": "the old cream board stays under it"},
        "applies_to": ["tea_rooms"],
        "kind": "the fascia target",
    },
    "roller_shutter": {
        "what": "a steel roller shutter over the window and shop door: a hood under the fascia set into the toplight zone (the head, bars and glass cut away behind it), two guide rails standing out in front of the frames on spacer brackets, a 77 mm slat curtain running in front of the sill and the stallriser to the footway",
        "numbers": {"hood_height": 300, "hood_depth_d": 210, "hood_z_range": [2550, 2850], "hood_front": "five-faced (octagon half)", "hood_ends": "end caps 3 mm, riveted",
                    "hides": "the toplights above 2550 (the hood is 300 high over toplights at 2480 to 2790): 70 of the toplights' 310 shows",
                    "hood_sits": "SET INTO the toplight zone, not in front of the frames: the window's and the shop door's head (z 2790 to 2850), the toplight bars and the toplight glass are CUT AWAY at z 2550 behind the hood over its width (u 350 to 4706), so the hood (d 0 to 210) shares no space with them; the jambs stop at 2550 under it and the fascia's rail carries it",
                    "cut_away": {"z_from": 2550, "u_range": [350, 4706], "parts": ["window head", "shop-door head", "window toplight bars", "window toplight glass", "door toplight bars", "door toplight glass"], "toplights_showing_z": [2480, 2550]},
                    "guide_rail": {"face": 50, "depth": 40, "d_range": [150, 190], "z_range": [0, 2550],
                                   "fixing": "steel spacer brackets bolted through the frames into the pilaster core, four M8 bolts per rail, bolt heads visible"},
                    "curtain_slat_pitch": 77.0, "curtain_plane_d": 170, "curtain_clear_of_sill_nose": 20,
                    "curtain_runs": "across window and door in one plane, to the footway, between the rails; it clears the sill's nose (150), the stallriser (125), the threshold (130), the transom (100), the door frame (100) and the mullions (92)",
                    "bottom_rail": {"height": 50, "locks": 2},
                    "colours": "galvanised steel painted grey (88,90,90)"},
        "applies_to": ["newsagent"],
        "source": "Poly Haven CC0 roller shutters (rollershutter_window_01/02/03, rollershutter_door; author MP, published 2023-10-11): the glTFs read today give a hood 150 deep for a 1.55 m shutter and 300 deep for 1.85 and 2.4 m, a curtain plane at z 20 and rails 7 wider than the curtain. They are 2023 products: the form, not the date, is used. The target's 210 deep hood is the reviewer's Judgement between the two",
        "kind": "Photo-scan geometry measured today (hood depths, rail width); the curtain plane, the rail depth range and the hood's 210 are Judgement fixed by clearing the frames; the slat pitch and the bolts are Judgement",
    },
    "empty_unit": {
        "what": "an empty unit: the panelling painted out and a ply or hardboard sheet screwed over the stallriser, the glass whitewashed from inside, the door's lower leaf hardboarded, a TO LET board on the fascia, one console gone",
        "numbers": {"whitewash_coverage": 1.0, "ply_sheet": [1200, 525, 9], "screws": 12, "console_absent": "viewer's left"},
        "applies_to": ["empty_unit"],
        "kind": "Judgement; DECISIONS 3 Oct (whitewashed), fascia-01 spec (the clipped console)",
    },
    "recessed_lobby": {
        "what": "the shop door set back in a lobby with a tiled or terrazzo floor and its own returns",
        "numbers": {"grocer": {"depth": 600, "floor": "terrazzo", "mosaic_border": 150}, "steam_laundry": {"depth": 300, "floor": "quarry tile 150"}},
        "applies_to": ["grocer", "steam_laundry"],
        "kind": "Read (FRONTAGE-2026-10-06.md: recessed lobbies with terrazzo or tiled floors; HE1 marble threshold then mosaic; HE2 white mosaic floor) and the project's earlier reading of Marshall's West Dock Cafe: recessed doorway, tiled threshold",
    },
}
