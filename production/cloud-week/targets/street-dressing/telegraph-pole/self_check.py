"""telegraph-pole: the self-check. python self_check.py [--live] [--previews] [--no-controls]"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF
import sd_place as PL

V = "TP1"


def part(T, pid):
    return [p for p in T["variants"][V]["parts"] if p["id"] == pid][0]


def extra(T, rows):
    ps = K._ps_cache(T["variants"][V]["parts"])
    pl = T["placement"]
    pole = part(T, "pole")
    rows.near("pole", "pole/radius at the ground is half the stated 230", pole["r0"] * 2, 230.0, 0.5)
    rows.add("pole", "pole/it tapers: the top radius is less than the foot's by at least 25 percent", pole["r1"] <= 0.75 * pole["r0"], "%s to %s" % (pole["r0"], pole["r1"]))
    steps = sorted(n for n in ps.names if n.startswith("step_"))
    zs = [(ps.part_bbox(n)[0][2] + ps.part_bbox(n)[1][2]) / 2 for n in steps]
    sides = [(ps.part_bbox(n)[0][0] + ps.part_bbox(n)[1][0]) / 2 for n in steps]
    rows.add("pole", "pole/the steps are 450 apart, from 2400, to 7200 at most", abs(zs[0] - 2400.0) < 1 and all(abs(b - a - 450.0) < 1 for a, b in zip(zs, zs[1:])) and zs[-1] <= 7200.0, "%d steps" % len(steps))
    rows.add("pole", "pole/the steps alternate sides", all(sides[i] * sides[i + 1] < 0 for i in range(len(sides) - 1)), "")
    # wires
    wires = [p for p in T["variants"][V]["parts"] if p["type"] == "wire"]
    for w in wires:
        pts = w["pts"]
        a, b = pts[0], pts[-1]
        span = math.hypot(b[0] - a[0], b[1] - a[1])
        sag = max((a[2] + (b[2] - a[2]) * k / (len(pts) - 1)) - pts[k][2] for k in range(len(pts)))
        frac = sag / span
        rows.add("wire", "wire/%s sags 1.5 to 3.5 percent of its span" % w["id"], 0.015 <= frac <= 0.035, "%.2f percent (%.0f over %.0f)" % (100 * frac, sag, span))
        # starts on a knob tip and ends at an anchor face
        knobs = [n for n in ps.names if n.startswith("knob_")]
        dmin = min(math.dist(a, [(ps.part_bbox(k)[0][i] + ps.part_bbox(k)[1][i]) / 2 if i != 1 else ps.part_bbox(k)[1][1] for i in range(3)]) for k in knobs)
        rows.at_most("wire", "wire/%s starts on a knob tip" % w["id"], dmin, 6.0)
        anch = ps.part_bbox("anchor_" + w["id"])
        rows.add("wire", "wire/%s ends on its anchor's face" % w["id"], anch[0][0] - 3 <= b[0] <= anch[1][0] + 3 and anch[0][1] - 3 <= b[1] <= anch[1][1] + 3 and anch[0][2] - 3 <= b[2] <= anch[1][2] + 3, "")
    zmin = min(p[2] for w in wires for p in w["pts"] if 725.0 <= p[1] <= 6725.0)
    rows.at_least("wire", "wire/the lowest point over the carriageway is at least 5.5 m", zmin, 5500.0)
    top = ps.part_bbox("pole")[1][2]
    rows.add("wire", "wire/every wire starts below the pole top and above the carriageway line", all(w["pts"][0][2] < top for w in wires), "")
    # placement
    clear = pl["footway_mm"] - pl["set_back_mm"] - pole["r0"]
    rows.at_least("placement", "placement/the footway keeps a metre beside the foot", clear, pl["min_clear_mm"])
    rows.near("placement", "placement/the set-back is from the kerb's back edge to the pole's centre", abs(pl["z_m"] - pl["kerb_back_z_m"]) * 1000.0, pl["set_back_mm"], 1.0)
    for nm, lx in (("east", pl["lamp_columns"]["east_x_m"]), ("west", pl["lamp_columns"]["west_x_m"])):
        rows.at_least("placement", "placement/at least 4 m from the %s lamp column" % nm, abs(pl["x_m"] - lx), 4.0, unit="m")
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    rows.near("placement", "placement/the street's carriageway is 6 m (the road span)", sc["street"]["carriageway"]["half_width_m"] * 2000.0, 6000.0, 1.0)
    rows.near("placement", "placement/the span to the east is the building line's distance", (pl["east_building_z_m"] - pl["z_m"]) * 1000.0, pl["span_to_east_mm"], 1.0)
    # the pose is the stated slot; the bracket faces the street's axis; the foot clears the litter bin; the pole stays off the street
    pose = pl["poses"][0]
    rows.add("placement", "placement/the pose is the stated slot", abs(pose["x_m"] - pl["x_m"]) < 1e-6 and abs(pose["z_m"] - pl["z_m"]) < 1e-6, "pose x %.3f z %.3f, slot x %.3f z %.3f" % (pose["x_m"], pose["z_m"], pl["x_m"], pl["z_m"]))
    bk = ps.part_bbox("bracket")
    bx, bz = PL.to_street(pose, 0.0, (bk[0][1] + bk[1][1]) / 2.0)
    rows.add("placement", "placement/the bracket stands on the pole's street face (towards +z, the street's axis)", bz > pose["z_m"] + 0.05 and abs(bx - pose["x_m"]) < 0.2, "bracket centre at street z %.3f, the pole at %.3f" % (bz, pose["z_m"]))
    pieces = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-pieces.json")))["pieces"]
    prisms, base = PL.object_prisms(T, pose)
    body = [q for q in prisms if q.part in ("pole", "cap") or q.part.startswith("step_") or q.part.startswith("knob") or q.part == "bracket"]
    near = []
    for o in PL.scene()["obs"]:
        if o.bom.startswith("C1_") or o.kind == "awning":
            continue
        d = min(PL.separation(q.poly, q.y0, q.y1, o.poly, o.y0, o.y1) for q in body)
        if d < 1.0:
            near.append((o.name, round(d, 3)))
    rows.add("placement", "placement/the pole and its steps are 0.30 m or more (3D) from every scene piece within 1 m", all(d >= 0.30 for n, d in near), "within 1 m: %s" % near)
    bin_ = next(p for p in pieces if p["name"] == pl["litter_bin"]["piece"])
    rows.add("placement", "placement/the litter bin the target names is the scene's", abs(bin_["x_m"] - pl["litter_bin"]["x_m"]) < 0.01 and abs(bin_["z_m"] - pl["litter_bin"]["z_m"]) < 0.01, "scene x %.2f z %.2f" % (bin_["x_m"], bin_["z_m"]))
    tf = open(os.path.join(L.REPO, "tools", "art-recipes", "terrace-front.py"), encoding="utf-8").read()
    dec = open(os.path.join(L.REPO, "DECISIONS.md"), encoding="utf-8").read()
    removed = "THE TELEGRAPH POLE IS OFF THE STREET" in tf and "telegraph pole and its drop wires taken off the street" in dec
    rows.add("placement", "placement/the 3 October removal stands in its homes (terrace-front.py and DECISIONS)", removed, "the note in terrace-front.py and the 2026-10-03 entry are both present: %s" % removed)
    rows.add("placement", "placement/the pole stays off the street until he rules, with the owed line", pl.get("on_street") is False and any(o["id"] == "O1" and o["recommended"].lower().startswith("no") for o in T["owed"]) and bool(pl.get("conflict")), "on_street %s; owed %s" % (pl.get("on_street"), [o["id"] for o in T["owed"]]))
    rows.add("placement", "placement/the conflict names the Hook sheet and the 3 October ruling", "Hook sheet" in pl["conflict"]["hook_sheet"] and "2026-10-03" in pl["conflict"]["ruling"], "")
    rows.add("detail", "detail/six knobs", len([n for n in ps.names if n.startswith("knob_")]) == 6, "")
    rows.add("detail", "detail/no plate, no tag, no lettering part", not any(("plate" in n or "tag" in n or "text" in n or "label" in n) for n in ps.names), "")
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for p in T["variants"][V]["parts"]), "")


def extra_controls(T):
    def straight(t):
        w = part(t, "w1")
        a, b = w["pts"][0], w["pts"][-1]
        w["pts"] = [[a[i] + (b[i] - a[i]) * k / (len(w["pts"]) - 1) for i in range(3)] for k in range(len(w["pts"]))]

    def low(t):
        w = part(t, "w2")
        w["pts"] = [[p[0], p[1], p[2] - 1200.0] for p in w["pts"]]
    return [
        ("wire: a taut wire with no sag", straight, "wire/w1 sags"),
        ("wire: the second wire hung 1.2 m too low", low, "wire/the lowest point over the carriageway"),
        ("wire: a wire that starts away from any knob", lambda t: part(t, "w3").__setitem__("pts", [[p[0], p[1], p[2] + 300.0] if i == 0 else p for i, p in enumerate(part(t, "w3")["pts"])]), "wire/w3 starts on a knob tip"),
        ("pole: no taper", lambda t: part(t, "pole").__setitem__("r1", 115.0), "pole/it tapers"),
        ("pole: steps 600 apart", lambda t: [K.shift_part(t, V, "step_%02d" % i, [0, 0, (i - 1) * 150.0]) for i in range(2, 12)], "pole/the steps are 450 apart"),
        ("pole: steps on one side", lambda t: K.shift_part(t, V, "step_02", [-2 * 100.0, 0, 0]) if False else [K.shift_part(t, V, "step_%02d" % i, [(0 if (i % 2) else 300.0), 0, 0]) for i in range(1, 12)], "pole/the steps alternate sides"),
        ("placement: the pole moved to the lamp column's x", lambda t: t["placement"].__setitem__("x_m", 28.5), "placement/at least 4 m from the east lamp column"),
        ("placement: set back only 100 mm and the foot wider", lambda t: (t["placement"].__setitem__("set_back_mm", 1500.0), t["placement"].__setitem__("z_m", -4.625 - 0.115 + 0.0)), "placement/the footway keeps a metre"),
        ("placement: the east span stated 9.5 m", lambda t: t["placement"].__setitem__("span_to_east_mm", 9500.0), "placement/the span to the east"),
        PL.ctl("placement: the first version's x 33.0 puts the foot inside the west shops' litter bin", "pole", "place/pole/clear of every street piece", x_m=33.0),
        ("placement: the first version's x 33.0 stated again", lambda t: (t["placement"].__setitem__("x_m", 33.0)), "placement/the pose is the stated slot"),
        ("placement: a west wire back at 6.5 m, 3 m above the one-storey row's eaves", lambda t: K.shift_part(t, V, "anchor_w3", [0, 0, 3200.0]), "place/pole/every anchor lies on a modelled wall below its eaves"),
        ("placement: the pole turned so the bracket faces the wall", lambda t: PL.set_pose(t, "pole", yaw_deg=180.0), "placement/the bracket stands on the pole's street face"),
        ("placement: the pole put back on the street without the owed line", lambda t: t["placement"].__setitem__("on_street", True), "placement/the pole stays off the street"),
        ("placement: the owed line dropped", lambda t: t.__setitem__("owed", []), "placement/the pole stays off the street"),
        ("placement: the pole standing in the ironmonger's door approach (x 34.2, z -4.6)", lambda t: PL.set_pose(t, "pole", x_m=34.2, z_m=-4.6), "place/pole/clear of every shop and house door zone"),
        ("placement: the pole in the carriageway", lambda t: PL.set_pose(t, "pole", z_m=-2.0), "place/pole/feet lie in zone"),
        ("placement: the east anchor above its eaves", lambda t: K.shift_part(t, V, "anchor_w2", [0, 0, 300.0]), "place/pole/every anchor lies on a modelled wall below its eaves"),
        ("detail: a plate part on the pole", lambda t: t["variants"][V]["parts"].append({"id": "owner_plate", "type": "box", "c": [0, -120, 2000], "s": [100, 4, 100], "material": "galvanised"}), "detail/no plate"),
        ("numbers: the pole 800 mm short", lambda t: [part(t, "pole").__setitem__("p1", [0, 0, 7200.0]), part(t, "cap").__setitem__("p0", [0, 0, 7200.0]), part(t, "cap").__setitem__("p1", [0, 0, 7245.0])], "numbers/N1"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="knob_21", leaf_move=[0, 60, 0], bridge="pole", join=("pole", "bracket"), join_move=[0, 50, 0], overlap=("knob_12", [0, -100, 0]), blocker={}, number_id="N1")
    sys.exit(1 if SF.selfcheck_main(HERE, "telegraph-pole", extra, extra_controls, spec) else 0)
