"""Builds target.json of the front-doors-all target from td_data.py, td_kinds.py, td_furn.py, the 3.1 door as built (target.json plus
kit/door/departures.py) and the street (td_sites.py, which reads tools/art-recipes/terrace-front.py). Run:
  /home/user/.bpyenv/bin/python make_target.py
then make_doc.py (TARGET.md) and self_check.py --write (the result into target.json)."""
import copy
import json
import os
import sys

from td_common import DOOR31, HERE, ROOT, TARGET_JSON, VIEWS_F1, VIEWS_T1, LANTERN_LINEAR, load_json, r
import td_data as D
import td_furn as FU
import td_kinds as K
import td_sites as S

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, "production", "cloud-week", "kit", "door"))
import departures  # noqa: E402

LAP = K.LAP


def frame_sets(A):
    F = A["variants"]["flat_door_over_shop"]["parts"]
    T = A
    def one(P, name, src):
        fr = P["frame"]
        tr = fr["transom"]
        gl = fr["glazing"]
        op = P["opening"]
        return {
            "id": name, "from": src, "opening_w": op["width_mm"], "head_top": op["crown_height_mm"], "head_ends": op["springing_height_mm"],
            "clear_between_stops": op["clear_between_stops_mm"], "reveal_depth": op["reveal_depth_mm"],
            "jamb_x": fr["jamb_x_mm"], "stop_edges_x": [fr["jamb_x_mm"]["left"][1], fr["jamb_x_mm"]["right"][0]],
            "head_z": [fr["head_section_mm"]["z0"], op["crown_height_mm"]],
            "transom_z": [tr["z_stop_underside"], tr["z_top"]], "transom_x": tr["x_mm"], "transom_face_h": tr["face_height_mm"],
            "glass_opening_x": gl["opening_x_mm"], "glass_opening_z": gl["opening_z_mm"],
            "leaf_x0": P["leaf"]["x0_mm"], "leaf_z0": P["leaf"]["z0_mm"], "leaf_w": P["leaf"]["width_mm"], "leaf_h": P["leaf"]["height_mm"],
            "visible_leaf_x": [fr["jamb_x_mm"]["left"][1], fr["jamb_x_mm"]["right"][0]], "visible_leaf_z": [P["leaf"]["z0_mm"], tr["z_stop_underside"]],
            "jamb_face": fr["jamb_face_mm"], "jamb_depth": fr["jamb_depth_mm"], "rebate": [fr["rebate_width_mm"], fr["rebate_depth_mm"]], "stop_depth": fr["stop_depth_mm"],
        }
    ts = one(T, "T", "3.1 T1 (production/assets/cloud-week/door/door_T1.glb): the brick opening, the cambered head, the stone step")
    ts["glb_pivot"] = A["glb_pivot"]["terrace_four_panel"]
    ts["ground_z"] = A["step"]["ground_z_mm"]
    fs = one(F, "F", "3.1 F1 (door_F1.glb): the shop bay's side slot, a flat head at 2400, a timber sill 45 above the paving")
    fs["glb_pivot"] = A["glb_pivot"]["flat_door_over_shop"]
    fs["ground_z"] = F["brick"] and -45.0
    ff6 = copy.deepcopy(fs)
    ff6["id"] = "FF6"
    ff6["from"] = "frame set F with the stops planted on the inside face, for F6 (leaf shown whole)"
    cx = (fs["stop_edges_x"][0] + fs["stop_edges_x"][1]) / 2.0
    ff6["clear_between_stops"] = 765.2
    ff6["stop_edges_x"] = [r(cx - 382.6, 2), r(cx + 382.6, 2)]
    ff6["jamb_x"] = {"left": [fs["jamb_x"]["left"][0], ff6["stop_edges_x"][0]], "right": [ff6["stop_edges_x"][1], fs["jamb_x"]["right"][1]]}
    ff6["visible_leaf_x"] = list(ff6["stop_edges_x"])
    ff6["glass_opening_x"] = list(ff6["stop_edges_x"])
    ff6["transom_x"] = [r(ff6["stop_edges_x"][0] - 28.0, 2), r(ff6["stop_edges_x"][1] + 28.0, 2)]
    ff6["leaf_x0"] = r(ff6["stop_edges_x"][0] + 1.6, 2)
    ff6["leaf_w"] = 762.0
    ff6["leaf_h"] = 1981.0
    return {"T": ts, "F": fs, "FF6": ff6}


def resolve_house(h, choice, kinds, furn):
    kind = choice["kind"]
    ks = kinds[kind]
    fr = "FF6" if kind == "F6" else ks["frame_set"][0]
    placements = {}
    for slot, var in choice["furniture"].items():
        cat = furn[slot]
        if var not in cat:
            raise KeyError("%s: variant %s not in %s" % (h["house"], var, slot))
        pl = cat[var].get("place", {}).get(kind)
        placements[slot] = {"variant": var, "place": pl}
    return {"house": h["house"], "side": h["side"], "x_centre_m": h["x_centre_m"], "stand_in": {"opening_w_mm": h["opening_w_mm"], "leaf_w_mm": h["leaf_w_mm"], "leaf_h_mm": h["leaf_h_mm"],
                                                                                       "step": h["step"], "letterplate_mm": h["letterplate_stand_in_mm"], "kit_side_door": h["kit_side_door"]},
            "kind": kind, "frame_set": fr, "paint": choice["paint"], "frame_colour": choice["frame"], "condition": choice["condition"], "furniture": placements, "why": choice["why"]}


def order_and_pairs(houses):
    """Street order per side by x; adjacent pairs are consecutive doors on a side; opposite pairs are doors of the two sides within 4.6 m along."""
    sides = {}
    for h in houses:
        sides.setdefault(h["side"], []).append(h)
    order = {}
    adj = []
    for sd, hs in sides.items():
        hs.sort(key=lambda h: h["x_centre_m"])
        order[sd] = [h["house"] for h in hs]
        for a, b in zip(hs, hs[1:]):
            adj.append([a["house"], b["house"]])
    opp = []
    east, west = sides.get("east", []), sides.get("west", [])
    for a in east:
        for b in west:
            if abs(a["x_centre_m"] - b["x_centre_m"]) <= 4.6:
                opp.append([a["house"], b["house"], r(abs(a["x_centre_m"] - b["x_centre_m"]), 3)])
    return order, adj, opp


def backdrop_table():
    out = []
    for i, bid in enumerate(D.BACKDROP_IDS):
        out.append({"id": "backdrop_rise_approach_" + bid, "kind": D.BACKDROP_KINDS[i % 6], "paint": D.BACKDROP_PAINTS[(i % 6 + 2) % 6]})
    return out


def furn_name(furn, var):
    for cat in furn.values():
        if var in cat:
            return cat[var].get("name")
    return None


def views(kind, frame):
    base = load_json(VIEWS_T1 if frame == "T" else VIEWS_F1)
    out = copy.deepcopy(base)
    return out


def main():
    T31 = load_json(DOOR31)
    A, dep_log = departures.apply(T31)
    kinds = K.build_kinds(A)
    furn = FU.furniture(A)
    fsets = frame_sets(A)
    houses_live, _ = S.derive()
    mod = S.modernised_houses()
    houses_live = [h for h in houses_live]
    resolved = []
    for h in houses_live:
        resolved.append(resolve_house(h, D.HOUSE_CHOICES[h["house"]], kinds, furn))
    for h in resolved:
        h["windows_modernised"] = "white_upvc" in mod.get(h["house"], [])
    order, adj, opp = order_and_pairs(houses_live)
    uses = {}
    for h in resolved:
        uses.setdefault(h["kind"], []).append(h["house"])

    N_VARIANTS = sum(1 for slot, cat in furn.items() for k, v in cat.items() if v.get("name") != "none" and v.get("offered", True))
    T = {}
    T["family"] = "front-doors-all"
    T["title"] = "Front doors for every house kind (cloud week 42, unit 9)"
    T["summary"] = ("Front doors for every house kind of Quay Street: from the passed 3.1 door (T1 cottage four-panel, F1 flat four-panel, its bell push fixed to one plain dark oblong), "
                    "10 door kinds (cottage T1 T2 T3, flat F1 to F7) fitted to the street's 12 household doors by house, 7 furniture slots with %d variants "
                    "(letter plates, handles, rim night latches, knockers, bells, numbers, a boot scraper), 16 paints and 3 conditions, a street order in which no two neighbours "
                    "match, and a gate of 7 views a kind plus the street rows." % N_VARIANTS)
    T["status"] = "WRITTEN 13 October 2026, not yet reviewed"
    T["units"] = "mm; leaf frame u across from the leaf's left edge seen from outside, v up from its bottom; frame frame x across the opening from the left reveal, z up from the threshold top (the 3.1 axes)"
    T["axes"] = {"leaf": "u, v as above (structural leaf, including the 20.4 that laps behind each stop and the head)", "frame": "x, z as target 3.1: x 0 at the left brick reveal, z 0 at the top of the threshold",
                 "visible_face": {"T": list(K.VIS["T"]), "F": list(K.VIS["F"]), "lap": LAP, "rule": "u_struct = 20.4 + fraction x visible width; v_struct = fraction x visible height"}}
    T["reuse"] = {
        "from": "production/cloud-week/targets/front-door/ (TARGET.md, target.json: the passed 3.1 door), production/cloud-week/kit/door/ (build_door.py, departures.py, check_door.py, views_T1.json, views_F1.json, NOTES.md), "
                "production/assets/cloud-week/door/door_T1.glb and door_F1.glb, HANDOVER.md row 3.1",
        "as_built": "every number taken from 3.1 is the target.json value with kit/door/departures.py applied (moulding width 46 and 43, collar 5.0 proud, keyway vertical 3 x 9, bell push a plain oblong)",
        "handover_fix": "delete the parts iron_bellpush_bezel and iron_bellpush_button from door_T1 (rebuild without them) so a plain dark oblong remains",
        "departures_applied": [d["id"] for d in dep_log],
    }
    T["frame_sets"] = fsets
    T["kinds"] = kinds
    T["kind_use"] = uses
    T["glass"] = FU.GLASS
    T["furniture"] = furn
    T["furniture_counts"] = {slot: len([k for k in cat if cat[k].get("name") != "none" and cat[k].get("offered", True)]) for slot, cat in furn.items()}
    T["furniture_placed_today"] = sorted({d2["variant"] for h in resolved for d2 in h["furniture"].values() if furn_name(furn, d2["variant"]) != "none"})
    T["paints"] = D.PALETTE
    T["frame_colours"] = D.FRAME_COLOURS
    T["conditions"] = D.CONDITIONS
    T["wear_kinds_used"] = D.WEAR_KINDS_USED
    T["wear_not_covered"] = D.WEAR_NOT_COVERED
    T["street"] = {"source": "tools/art-recipes/terrace-front.py plan_street (the drawn street), production/specs/vignette-scene.json (blocks), production/specs/vignette-pieces.json (the coarse side doors), the house-windows target (modernised = white_upvc)",
                   "houses": resolved, "order": order, "adjacent_pairs": adj, "opposite_pairs_within_4_6_m": opp,
                   "no_side_door": [{"house": "east_parade_bay5", "why": "the grocer's flat is reached from the rear yard (terrace-front.py BAY_WITHOUT_SIDE_DOOR 5; the coarse piece east_parade_sidedoor5 is not drawn)"}],
                   "yard_slot": {"x_m": [21.0, 24.0], "note": "the 3.0 m yard entrance between the west blocks is a gap in the data, no door piece; a gate there belongs to the gate family, not this one"},
                   "council_owned": "none: no file names a council-owned house on Quay Street; the council-style flush door F6 is used on a modernised flat, not on a council house",
                   "backdrop": {"rule": D.BACKDROP_RULE, "doors": backdrop_table()}}
    T["mix_rule"] = {
        "text": ("A new house takes a kind its frame set allows (cottage frame T: T1 T2 T3; flat frame F: F1 to F7), a paint that is not its neighbours' on the same side nor the paint of a door "
                 "within 4.6 m across the street, and furniture so that each neighbour differs in at least 2 of the slots letter plate, handle, latch, number. A modernised house (replacement windows) "
                 "takes T3, F5 or F6 or keeps its old kind. Knockers, bells (except T1's oblong), black iron plates, bell pulls, frosted and wired glass and numerals in black metal are not placed on any house today."),
        "adjacent_rule": {"differ_in_kind": True, "differ_in_paint": True, "min_furniture_slots_differing": 2},
        "opposite_rule": {"within_m": 4.6, "paint_class_differs": True},
    }
    T["owed_for_jafar"] = D.OWED
    T["sources"] = {"photographs": D.PHOTOS, "books": D.BOOKS, "measurements": D.MEAS, "colour_boxes": D.COLOUR_BOXES}
    T["rulings_checked"] = [
        {"ruling": "3 Oct: the proof view's bars: windows with white frames, sash bars, sky in the glass", "applies": "the fanlights are windows and the Hook sheet's door surrounds are white: every frame colour is white or grimed white; 3.1's cream frame option is dropped; the Hull streets' painted surrounds (D8) are NOT adopted: owed line 2"},
        {"ruling": "21 Sep and 1 Oct: the Hook sheet governs mood, palette and composition; dated photographs govern what things looked like and win", "applies": "dark doors lead (black, dark green, maroon, navy, brown, deep teal); the bright 1980s colours the photographs show are limited to 2 doors of 12: owed line 1"},
        {"ruling": "8 Oct: kit pieces period books draw (doors): a fresh helper writes the target; photographs win over books", "applies": "this target; Hasluck is followed only for the ledged door, for which no photograph was reached"},
        {"ruling": "2 Oct: Rita's window is the model; the other shopfronts are made like it", "applies": "Rita's side door is the shopfront kit's own; the target gives it F1 and the kit keeps its fanlight"},
        {"ruling": "4 Oct (terrace-front.py, Jafar: every house on the right is the same): each house its own door colour, never its neighbour's", "applies": "the adjacency rule; the 12 doors share no colour with a neighbour on their side"},
        {"ruling": "13 Oct: no alcohol or gambling shown; no children; no real firm or maker; night light (1.0, 0.25, 0.0) linear", "applies": "no pub, sign or drink in any preview; 'rim night latch'; the gate's night view uses the lantern colour"},
    ]
    # ---- the gate
    gate = {"views": {}, "pass_rule": {"front_view_by_layer": "IoU >= 0.97, outline p95 <= 2 mm, worst <= 6 mm (3.1's rule)", "sections": "IoU >= 0.97, p95 <= 2 mm, worst <= 6 mm", "profiles": "p95 <= 1.5 mm, worst <= 3 mm"}}
    for k, spec in kinds.items():
        fr = "FF6" if k == "F6" else spec["frame_set"][0]
        base = "T" if fr == "T" else "F"
        v = copy.deepcopy(load_json(VIEWS_T1 if base == "T" else VIEWS_F1))
        # close view at the kind's own furniture: the handle and latch heights when they stand above 0.7 m, else the plate; a foot view for a low plate
        hz, plate_z = [], None
        low_plate = False
        h0 = [kk for kk in resolved if kk["kind"] == k][0]
        for slot, d2 in h0["furniture"].items():
            pl = furn[slot][d2["variant"]].get("place", {}).get(k)
            if not pl or not isinstance(pl.get("v"), (int, float)):
                continue
            if slot == "letter_plate":
                plate_z = pl["v"] / 1000.0
                low_plate = pl["v"] < 300.0
            elif pl["v"] >= 700.0:
                hz.append(pl["v"] / 1000.0)
        close_z = r(sum(hz) / len(hz) + 0.01, 2) if hz else r((plate_z or 1.2) + 0.01, 2)
        for vw in v:
            if vw["name"] == "close":
                vw["target"][2] = close_z
                vw["loc"][2] = close_z
            if vw["name"] == "close_plate":
                zz = r((plate_z if plate_z is not None else close_z) + 0.01, 2)
                vw["target"][2] = zz
                vw["loc"][2] = zz
        if low_plate:
            v.append({"name": "close_foot", "loc": [0.1, -1.0, 0.25], "target": [0.0, 0.19, 0.2], "lens": 50})
        gate["views"][k] = v
    gate["street_views"] = [
        {"name": "hook_day", "from": "vignette-scene.json cameras cam_A (x 4 east footway, looking up +x), condition overcast_day", "sees": "the west cottages' near doors and the east parade's side doors in perspective"},
        {"name": "reverse_day", "from": "the reverse camera of the same file", "sees": "the east parade's row from the quay end"},
        {"name": "street_night", "from": "cam_A, condition wet_night", "light": {"lantern_colour_linear": LANTERN_LINEAR, "note": "the game's lantern colour (linear red 1.0, green 0.25, blue 0.0), never the older yellow value"}},
        {"name": "row_east", "from": "an orthographic elevation at 1.6 m of the east side, x 3 to 46, from the west footway", "reads": "no two neighbours alike (checks AD1 to AD6)"},
        {"name": "row_west", "from": "the same for the west side", "reads": "as above"},
    ]
    gate["photograph_pairs"] = [
        {"kind": "T2", "photographs": ["D3", "D1"], "reads": "four lights equal, bars thin, a low plate, a bar pull on the left stile, a leaded fanlight"},
        {"kind": "T3", "photographs": ["D4"], "reads": "a small arched light in an embossed upper panel, an oblong plate between the panels"},
        {"kind": "F5", "photographs": ["D2", "D4"], "reads": "a tall slit light centred on a flat door, a small plate under it, a lever on the left"},
        {"kind": "F6", "photographs": ["D5", "D9"], "reads": "a flat door with an oblong plate at the middle, a lever on the right, a wide white frame, reeded transom"},
        {"kind": "F4", "photographs": ["D2"], "reads": "three long narrow lights"},
        {"kind": "F3", "photographs": ["D1"], "reads": "two long panels, no cross rail"},
        {"kind": "T1/F1/F2", "photographs": ["P1", "P2"], "reads": "as 3.1's reviews"},
        {"kind": "F7", "photographs": [], "reads": "no photograph reached; reads against Hasluck's figures only, listed as a known shortfall"},
    ]
    gate["near_misses_to_report"] = ["F7 has no photograph", "the knockers, bell pulls, black iron plates, frosted and wired glass are listed and not placed"]
    T["gate"] = gate
    import td_checks
    T["checks"] = td_checks.build_checks(T)
    T["disagreements_photographs_win"] = [
        {"id": "W1", "what": "the leaf width of a council flush door", "scene_or_book": "the scene's side door 0.838 x 1.981 (SCENE-SLOTS)", "photograph": "D5: 0.389 of the height, a 762 leaf shown whole in a wide white frame", "chosen": "F6: 762, frame set FF6"},
        {"id": "W2", "what": "the letter plate on every household door", "scene_or_book": "the scene's 0.25 x 0.04 at 1.0 on every side door (west_north and east_chandler included)", "photograph": "D1, D4: a low plate at the foot; D2: a plate under a slit at 0.83; D5: 250 x 70 at 0.91; D4 right: 260 x 67 at 0.87; a service door has none", "chosen": "per kind (LP1 to LP7); none on F7"},
        {"id": "W3", "what": "the stand-in leaf is 766 or 678 wide in the drawn street; 3.1's leaves are 812.8 and 838", "scene_or_book": "terrace-front.py: leaf = 838 less two 36 casings (parade) or 838 less two 80 (cottages)", "photograph": "P1, P2, D3 (a 2 ft 8 in to 2 ft 9 in leaf)", "chosen": "3.1's frame sets T and F replace the stand-ins; the wall kit meets their openings"},
        {"id": "W4", "what": "the brass kick plate on the drawn parade doors", "scene_or_book": "terrace-front.py draws a brass kick plate 726 x 140 on each side door", "photograph": "no photograph read (P1, P2, D1 to D6) shows a kick plate", "chosen": "none; kick marks are wear"},
        {"id": "W5", "what": "hinges outside a ledged door", "scene_or_book": "Hasluck Fig. 1027 draws hook-and-plate hinges on the face of a frame set in a wall", "photograph": "none reached", "chosen": "an inward-opening door, hinges inside (3.1's rule for all its doors); the face shows boards and nail heads"},
        {"id": "W6", "what": "the 3.1 cream frame (weight 0.3)", "scene_or_book": "3.1's frame_colours", "photograph": "the Hook sheet's door surrounds are white; Jafar 3 Oct: windows with white frames", "chosen": "white and grimed white only; the Hull painted surrounds (D8) are an owed line"},
        {"id": "W7", "what": "the bell push of 3.1's try 2", "scene_or_book": "build_door.py: oblong plus a brass bezel plus a dark button", "photograph": "P1: a plain dark oblong with a darker band, nothing bright", "chosen": "BL1: one plain part; the two-part push is a fault"},
        {"id": "W8", "what": "the leaded fanlight's height", "scene_or_book": "the T frame's glass opening 267 high", "photograph": "D3: a leaded light about 624 high over a 1981 leaf", "chosen": "the T frame's 267 stays (the wall kit owns the head); only the leaded diamond glazing is taken"},
    ]
    T["could_not_settle"] = [
        "No dated photograph read shows a door knocker, a bell pull, a black iron letter plate, frosted or wired door glass, or a ledged service door on these streets. KN1, KN2, BL2, LP3, frosted, wired and NM2 are listed with Judgement sizes and refused on every house by the checks; F7 is built from Hasluck and Judgement alone.",
        "Door colours of 1990: the slides of 1975 to 1994 shift hue and exposure, so the palette's bright and mid values (turquoise, bright blue, lime, khaki, mustard, olive) are Judgement from boxes whose medians are recorded; the dark classics are 3.1's.",
        "Small hardware at 22 to 27 mm a pixel (plates, levers, a small light) carries +-24 to +-35 mm; the positions are fractions of the visible face with that error written in each check.",
        "D1's doors stand in deep recesses and are seen from the right: only their vertical rows are used; the leaves' widths and the letter plate's length are not taken from it.",
        "Whether the west shop row (one storey in the drawn street) has flats: its side doors are 1 service door and 2 household doors until Jafar answers owed line 3.",
        "The painted cement hoods over Hull doorways (D1, D6) and their arched recesses (D7) are wall features; not in the door piece, listed for the wall kit.",
        "A house number's digits are the town's; the target fixes only the form (NM1, NM3, NM4).",
        "The shopfront kit's own side door at east_parade bay 2 (Rita's) has its own geometry and a fanlight (unit 2.2); this target gives it kind F1 and expects the builder to put F1's leaf in that slot.",
        "The boot scraper: one cast-iron scraper by the nearest cottage's step; no period photograph of these streets shows one (D10 is 2014); the sizes are Judgement +-25 per cent.",
    ]
    T["self_check"] = {"result": "not run yet"}
    with open(TARGET_JSON, "w") as f:
        json.dump(T, f, indent=1)
    print("wrote", TARGET_JSON, os.path.getsize(TARGET_JSON))


if __name__ == "__main__":
    main()
