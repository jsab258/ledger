"""The checks the builder's automatic check must pass for the front-doors-all target. Each is a record with an id, a group, a name, the kind(s) it
applies to, what to measure, the expected value and tolerance, and where the value comes from. self_check.py evaluates every record on the target's own drawing
(and, for the photograph and street groups, on the photographs and the street's source); the builder's check evaluates the same records on its mesh."""
import sys

sys.dont_write_bytecode = True


def build_checks(T):
    kinds = T["kinds"]
    furn = T["furniture"]
    C = []

    def add(id_, group, name, what, expect, tol, src, kind=None, **extra):
        d = {"id": id_, "group": group, "name": name, "kind": kind, "what": what, "expect": expect, "tol": tol, "src": src}
        d.update(extra)
        C.append(d)

    # ---- PL: panel layout per kind
    for k, spec in kinds.items():
        lf = spec["leaf"]
        ops = lf["openings"]
        add("PL-%s-count" % k, "PL", "%s: number of leaf openings" % k, "count the panel, light, slit and small-light openings cut in the leaf", len(ops), 0,
            "kind spec", kind=k, type="count", types=sorted({o["type"] for o in ops}))
        for o in ops:
            add("PL-%s-%s" % (k, o["id"]), "PL", "%s: opening %s" % (k, o["id"]), "bounds of the opening in the leaf frame: u0, u1, v0, v1",
                [o["u0"], o["u1"], o["v0"], o["v1"]], 3.0, "kind spec (photograph fractions for T2 T3 F4 F5 F6, 3.1 for T1 F1 F2 F3)", kind=k, type="opening_bounds", opening=o["id"])
        keys = [x for x in ("stile_left", "stile_right", "top_rail", "bottom_rail", "lock_rail", "muntin", "bar", "frieze_rail", "border") if x in lf]
        add("PL-%s-members" % k, "PL", "%s: stiles, rails, muntin and bars" % k, "member widths on the face, mm", {x: lf[x] for x in keys}, 2.0, "kind spec", kind=k, type="members")
        if ops:
            add("PL-%s-framing" % k, "PL", "%s: framing between openings" % k, "no two openings overlap and each lies inside the leaf with at least 20 mm of framing to the edge (the spyhole and slit are inside)",
                {"min_framing_mm": 20.0}, 0.0, "construction", kind=k, type="framing")
    # ---- CV: nothing shows through
    for k, spec in kinds.items():
        add("CV-%s-elevation" % k, "CV", "%s: no see-through slot in elevation" % k,
            "inside the clear opening (jamb to jamb, sill to head) the frame, leaf, glass and transom cover everything except the leaf's 1.6 mm margins, the 10 mm foot gap and the glass itself",
            {"max_hole_mm2": 0.0, "foot_gap_mm": 10.0, "margin_mm": 1.6}, 0.0, "3.1 NOTES (the dark hall behind the door is a render aid, the engine needs its own dark hall)", kind=k, type="coverage_elevation")
        add("CV-%s-angle" % k, "CV", "%s: no see-through slot from an angle" % k,
            "a ray at 60 degrees from the normal, in the plan section through each jamb and the leaf's edge, meets the stop, the leaf or the jamb: the 1.6 mm margin is closed behind by the stop (22 wide, 74 deep) or by a planted stop (F6)",
            {"angle_deg": 60.0, "margin_mm": 1.6, "stop_overlap_mm": 20.4 if k != "F6" else 0.0, "planted_stop_behind": k == "F6"}, 0.0, "3.1 frame (rebate 22 x 53, stop 74)", kind=k, type="coverage_angle")
    add("CV-F7-joints", "CV", "F7: board joints are tongued and grooved", "no through-gap between boards from the front or at 60 degrees: the tongue is at least 6 mm", {"tongue_mm": 6.0, "v_joint_depth": 2.0}, 0.5,
        "Hasluck p.316", kind="F7", type="joints")
    # ---- FU: furniture positions and sizes, by kind and variant as used on the houses
    seen = set()
    for h in T["street"]["houses"]:
        for slot, d in h["furniture"].items():
            var = d["variant"]
            pl = d["place"]
            if not pl or (h["kind"], slot, var) in seen:
                continue
            seen.add((h["kind"], slot, var))
            cat = furn[slot][var]
            size = cat.get("outer") or cat.get("size") or ([cat.get("collar"), cat.get("collar")] if "collar" in cat else None) or cat.get("digit")
            add("FU-%s-%s-%s" % (h["kind"], slot, var), "FU", "%s: %s %s" % (h["kind"], slot, var), "centre of the fitting in the leaf frame (u, v) and its outer size",
                {"u": pl.get("u"), "v": pl.get("v"), "size": size, "place": pl}, 8.0, cat.get("src", ""), kind=h["kind"], type="furniture", slot=slot, variant=var)
    # ---- BP: the bell push
    bp = furn["bell"]["BL1"]
    add("BP-form", "BP", "bell push: one plain part", "the T1 push is exactly one mesh part named iron_bellpush, 22 x 72.6 x 3 proud, corner radius at most 2 mm, no part named bezel, button, ring, lens, led, camera or speaker, no metallic ring, nothing bright",
        {"parts": 1, "size": bp["size"], "proud": bp["proud"], "corner_r_max": 2.0, "forbidden": bp["forbidden"]}, 0.5, "P1 16x crop; 3.1 review v2 close; HANDOVER 3.1 fix", kind="T1", type="bell_form")
    add("BP-none-elsewhere", "BP", "no push on any other kind", "no part of any other kind is named iron_bellpush* or carries a bell", {"kinds_with_bell": ["T1"]}, 0, "target", type="bell_kinds")
    add("BP-no-modern", "BP", "no two-part modern push on any variant", "on every kind and variant no part of a bell fitting beyond the one oblong; no part name or material of the 'modern video doorbell' family", {"max_parts_per_bell": 1}, 0,
        "3.1 review v2 close: the two-part push reads as a modern video doorbell", type="bell_modern")
    add("BP-houses", "BP", "the push is placed on one house only", "the houses whose bell is BL1", {"houses": [h["house"] for h in T["street"]["houses"] if h["furniture"].get("bell", {}).get("variant") == "BL1"]}, 0, "house table", type="bell_houses")
    # ---- AD: the street's order
    for side in ("east", "west"):
        add("AD-adjacent-%s" % side, "AD", "no two neighbours alike on the %s side" % side, "each consecutive pair of doors differs in kind, in paint and in at least 2 of letter plate, handle, latch, number",
            T["street"]["order"][side], 0, "Jafar 4 Oct: every house its own door; the brief", type="adjacent", side=side)
    add("AD-opposite", "AD", "doors facing within 4.6 m differ in paint class", "paint class (dark_neutral, dark_chroma, mid, light, bright) differs", T["street"]["opposite_pairs_within_4_6_m"], 0, "the brief", type="opposite")
    add("AD-coverage", "AD", "every household door of the street has a kind", "the 12 houses derived from terrace-front.py all appear, east_parade_bay5 has none", [h["house"] for h in T["street"]["houses"]], 0, "terrace-front.py", type="houses")
    add("AD-frame-set", "AD", "a kind sits in its frame set", "cottages (west_south) take T kinds, every other house takes F kinds", {"west_south": ["T1", "T2", "T3"]}, 0, "frame sets", type="frame_set")
    add("AD-kinds-used", "AD", "every kind is used at least once", "10 kinds", sorted(kinds.keys()), 0, "the brief: every house kind", type="kinds_used")
    add("AD-backdrop", "AD", "the hill's 12 doors: no neighbours alike", "kind and paint differ between consecutive doors of a row", T["street"]["backdrop"]["doors"], 0, "backdrop rule", type="backdrop")
    # ---- PN: paint and frames
    add("PN-palette", "PN", "every door paint is in the palette", "paint ids", [p["id"] for p in T["paints"]], 0, "palette", type="palette")
    add("PN-frames", "PN", "frames are white or grimed white", "frame colour ids", [p["id"] for p in T["frame_colours"]], 0, "Jafar 3 Oct: windows with white frames", type="frames")
    add("PN-light-doors", "PN", "at most 3 of 12 doors are light or bright", "paint class light or bright", 3, 0, "the Hook sheet's dark doors; owed line 1", type="light_count")
    add("PN-srgb", "PN", "paint values are sRGB triples in range and the dark classics are 3.1's", "the 6 colours of 3.1 keep their numbers", {"black": [35, 36, 40], "dark_green": [28, 59, 41], "maroon": [92, 26, 32], "navy": [24, 38, 78], "brown": [74, 48, 34], "red": [201, 41, 32]}, 0,
        "3.1 door_colours", type="srgb")
    # ---- GL: glass
    add("GL-types", "GL", "glass types used exist", "every glass key named by a kind", sorted(T["glass"].keys()), 0, "glass table", type="glass_keys")
    add("GL-reeded", "GL", "reeded glass: 6 mm flutes, 1.2 deep", "pitch and depth", {"pitch": 6.0, "depth": 1.2}, 0.1, "D5", kind="F6", type="glass_values", glass="reeded_4mm")
    add("GL-leaded", "GL", "leaded light: came 6 wide, diamonds 95 x 70", "came and diamond size", {"came_w": 6.0, "diamond": [95.0, 70.0]}, 0.1, "D3, scaled", kind="T2", type="glass_values", glass="leaded_diamond")
    # ---- WR: wear
    add("WR-order", "WR", "conditions order", "paint_flake share kept < tired < neglected", [0.03, 0.063, 0.40], 0, "wear target paint_flake range and neglected 0.40", type="wear_order")
    add("WR-wear-target", "WR", "numbers equal the wear target's", "paint_flake density range, typical and neglected share; handle_wear halo p50", {"flake_low": 0.03, "typical": 0.063, "neglected": 0.40, "halo_p50_m": 0.17}, 0,
        "production/cloud-week/targets/wear/target.json", type="wear_numbers")
    add("WR-houses", "WR", "every house has a condition; the street has all three", "kept, tired, neglected counts", {k: sum(1 for h in T["street"]["houses"] if h["condition"] == k) for k in ("kept", "tired", "neglected")}, 0,
        "house table", type="wear_houses")
    # ---- PH: photographs (fractions of the visible face)
    for k, ph in (("T2", "D3"), ("T3", "D4"), ("F5", "D2"), ("F6", "D5"), ("F4", "D2"), ("T2", "D1")):
        add("PH-%s-%s" % (k, ph), "PH", "%s against photograph %s" % (k, ph), "the kind's features as fractions of its visible face against the fractions measured in the photograph's recorded boxes", None, "the measurement's own error plus 8 mm",
            "Photo " + ph, kind=k, type="photo", photo=ph)
    # ---- NM: texts and data
    add("NM-maker", "NM", "no maker's name in any text or data", "whole-word blocklist over every string in target.json", [], 0, "brief: no real maker's names or marks", type="blocklist")
    add("NM-night", "NM", "night light is the lantern colour", "(1.0, 0.25, 0.0) linear present, (1, 0.7055, 0) absent", [1.0, 0.25, 0.0], 0, "Jafar 13 Oct lesson", type="night")
    add("NM-dash", "NM", "no em dash or italic marker in the lines for Jafar", "owed lines", None, 0, "Jafar 13 Oct lesson", type="owed_text")
    # ---- GA: the gate
    for k in kinds:
        add("GA-%s-views" % k, "GA", "%s: the gate's views" % k, "front, street, close, low, front_head, front_foot, close_plate (and close_foot for a low plate), cameras as 3.1's views json with the close height at the kind's furniture", 7 + (1 if any(
            v["name"] == "close_foot" for v in T["gate"]["views"][k]) else 0), 0, "kit/door/views_T1.json, views_F1.json", kind=k, type="views")
    return C
