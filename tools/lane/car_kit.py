"""Kit data for the fictional 1990 small family hatch, derived from its loft numbers.

Written by the lane session, 17 November 2026. Pure Python, no Blender, no network.
From one HatchParams (tools/lane/car_loft.py, imported, not changed) it works out
what the Blender side and Unreal need beyond the body mesh: wheels with hub
pivots and bone names, suspension travel and arch room, simple collision boxes,
panel splits with hinges, glass slots, named sockets, and weight and size data.
Everything comes out as one JSON-able dict.

Checklist source: production/research/lane/TRAFFIC-COST-2026-11-17.md, section 5
("The car kit's first build: checklist so stages 2 and 3 redo nothing").

Axes as car_loft: x from the nose (0) to the tail (L), y across (+ is the car's
left), z up from the ground. Metres. Values marked "est." are estimates, not
measured from real cars.

Usage: python tools/lane/car_kit.py [--round3] [--out kit.json]
"""
import json
import os
import sys
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import car_loft  # noqa: E402
from car_loft import HatchParams, build, measure, top_z, half_width_at  # noqa: E402

# Suspension travel from the resting hub height (est., class-typical small hatch).
TRAVEL_UP = 0.08     # est.
TRAVEL_DOWN = 0.10   # est.
# Least gap between tyre top and the visible arch lip at rest (est.): below this
# the tyre rubs the lip when the car rocks or steers.
MIN_LIP_GAP = 0.02   # est.
# Room kept above the raised tyre for the wheelhouse liner and wing top (est.).
WHEELHOUSE_MARGIN = 0.03  # est.
# Kerb mass for the class (est.; the class runs about 850 to 950 kg).
KERB_MASS_KG = 900.0  # est.
MASS_RANGE = (850.0, 950.0)
# Front bumper and rear bumper depth along x (est.).
BUMPER_DEPTH = 0.18  # est.
DOORS = 5            # five-door hatch chosen as the kit's first platform
PLATE_W, PLATE_H = 0.520, 0.111   # British plate, 520 x 111 mm
MAX_COLLISION = 6    # production/specs/asset-budgets.json "car"
BOX_MARGIN = 0.02    # boxes may poke this far past the body's bounding box
MIN_BOX_COVER = 0.85
PANEL_TOL = 0.005    # largest gap or overlap allowed between neighbouring panels
# Bumper tops above the sill (est.).
FRONT_BUMPER_RISE = 0.22  # est.
REAR_BUMPER_RISE = 0.25   # est.
# Material slots as planned (TRAFFIC-COST section 5, item 11).
MATERIALS = ["paint", "glass", "chrome", "black_plastic", "rubber", "lens", "plate", "interior"]

# A plain naming choice after the Chaos Vehicles habit of one bone per wheel;
# Epic's own wheel-bone rules are unread here (see the checklist's sources).
WHEEL_BONES = {"FL": "wheel_front_left", "FR": "wheel_front_right",
               "RL": "wheel_rear_left", "RR": "wheel_rear_right"}
ROOT_BONE = "root"


def _r(v):
    if isinstance(v, (list, tuple)):
        return [_r(q) for q in v]
    return round(v, 4)


def wheels(p):
    """Four wheels with hub pivots, bones, travel and the arch room check data."""
    d = p.derived()
    out = []
    for key in ("FL", "FR", "RL", "RR"):
        x = d["front_axle"] if key[0] == "F" else d["rear_axle"]
        y = p.track / 2 if key[1] == "L" else -p.track / 2
        hub = (x, y, p.wheel_radius)
        tyre_top = 2 * p.wheel_radius
        # car_loft has arch data: the arch is a circle about the resting hub,
        # radius wheel_radius + arch_clearance, so the lip gap is arch_clearance.
        lip_gap = p.arch_clearance
        # The wheelhouse behind the lip runs up to the wing or deck top above the
        # axle. Approximation: the loft's top line at the axle stands for it.
        wheelhouse_top = top_z(p, x)
        room_up = wheelhouse_top - WHEELHOUSE_MARGIN - tyre_top
        out.append({
            "name": key,
            "bone": WHEEL_BONES[key],
            "hub": _r(hub),
            "spin_axis": [0.0, 1.0, 0.0],
            "radius": _r(p.wheel_radius),
            "width": _r(p.tyre_width),
            "steers": key[0] == "F",
            "driven": key[0] == "F",   # front-wheel drive, est. for the class
            "travel_up": TRAVEL_UP,
            "travel_down": TRAVEL_DOWN,
            "arch_radius": _r(p.wheel_radius + lip_gap),
            "arch_lip_gap": _r(lip_gap),
            "wheelhouse_room_up": _r(room_up),
            "wheelhouse_room_note": "approximate: loft top line at the axle minus a liner margin",
            # the tyre rises past the visible lip at full bump; the wheelhouse
            # must be cut at least this high above the ground
            "wheelhouse_cut_top_z": _r(tyre_top + TRAVEL_UP + WHEELHOUSE_MARGIN),
            "parts": {"hub": "chrome", "tyre": "rubber", "trim": "chrome"},
        })
    return out


def _box(name, x0, x1, y_half, z0, z1):
    return {"name": name,
            "centre": _r(((x0 + x1) / 2, 0.0, (z0 + z1) / 2)),
            "half_extent": _r(((x1 - x0) / 2, y_half, (z1 - z0) / 2))}


def _mean_top(p, x0, x1, n=12):
    return sum(top_z(p, x0 + (x1 - x0) * i / (n - 1)) for i in range(n)) / n


def _mean_hw(p, x0, x1, n=12):
    return sum(half_width_at(p, x0 + (x1 - x0) * i / (n - 1)) for i in range(n)) / n


def collision(p):
    """Five boxes: nose, lower body, cabin, hatch slope, tail.

    The checklist says "one box plus arch shapes"; boxes only are used here,
    within the 6-shape cap (a recorded deviation, review finding 7).
    """
    d = p.derived()
    L, belt = p.length, p.belt_z
    sill = p.sill_z
    roof = p.height - p.roof_crown - p.roof_drop / 2
    cabin_hw = p.width / 2 - p.shoulder_in - p.glass_inset / 2
    return [
        _box("nose", 0.0, d["screen_base"], _mean_hw(p, 0.0, d["screen_base"]),
             sill, _mean_top(p, 0.0, d["screen_base"])),
        _box("lower_body", d["screen_base"], d["hatch_base"], p.width / 2, sill, belt),
        _box("cabin", (d["screen_base"] + d["roof_front"]) / 2, d["roof_back"], cabin_hw, belt, roof),
        _box("hatch_slope", d["roof_back"], d["hatch_base"], cabin_hw, belt,
             (roof - p.roof_drop / 2 + p.tail_top_z) / 2),
        _box("tail", d["hatch_base"], L, _mean_hw(p, d["hatch_base"], L), sill, p.tail_top_z),
    ]


def lines(p):
    """The shut lines along x: A-pillar foot, B-pillar, rear door end (est.)."""
    d = p.derived()
    a_line = d["screen_base"] + 0.05
    rear_door_end = d["rear_axle"] - (p.wheel_radius + p.arch_clearance)
    # front door about 58% of the door run (est., five-door hatch)
    b_line = a_line + 0.58 * (rear_door_end - a_line)
    return {"a_line": a_line, "b_line": b_line, "rear_door_end": rear_door_end}


def panels(p):
    """Panel splits, each an x range and a z band (side view), with hinge axes
    for the opening panels and a material slot. Data only."""
    d = p.derived()
    L, belt = p.length, p.belt_z
    hw = p.width / 2
    ln = lines(p)
    a_line, b_line, rear_door_end = ln["a_line"], ln["b_line"], ln["rear_door_end"]
    sill = p.sill_z
    roof = p.height - p.roof_crown
    fb_top = sill + FRONT_BUMPER_RISE
    rb_top = sill + REAR_BUMPER_RISE
    tail_end = max(d["hatch_base"], L - 0.02)
    out = [
        {"name": "front_bumper", "x": [0.0, BUMPER_DEPTH], "z": [sill, fb_top], "sides": "both",
         "material": "black_plastic"},
        # grille and lamp panel above the bumper, ahead of the wings
        {"name": "front_panel", "x": [0.0, BUMPER_DEPTH], "z": [fb_top, top_z(p, BUMPER_DEPTH) + p.deck_crown],
         "sides": "both", "material": "black_plastic"},
        {"name": "bonnet", "x": [BUMPER_DEPTH, d["screen_base"]],
         "z": [p.nose_top_z - 0.05, belt + p.deck_crown], "sides": "top", "material": "paint",
         "hinge": {"point": _r((d["screen_base"], 0.0, belt)), "axis": [0.0, 1.0, 0.0],
                   "note": "at the screen base"}},
        {"name": "front_wing_left", "x": [BUMPER_DEPTH, a_line], "z": [sill, belt], "sides": "left",
         "material": "paint"},
        {"name": "front_wing_right", "x": [BUMPER_DEPTH, a_line], "z": [sill, belt], "sides": "right",
         "material": "paint"},
    ]
    if DOORS == 5:
        for side, sy in (("left", 1), ("right", -1)):
            out.append({"name": "front_door_" + side, "x": [a_line, b_line], "z": [sill, roof],
                        "sides": side, "material": "paint",
                        "hinge": {"point": _r((a_line, sy * hw, belt - 0.1)), "axis": [0.0, 0.0, 1.0],
                                  "note": "at the A-pillar line"}})
        for side, sy in (("left", 1), ("right", -1)):
            out.append({"name": "rear_door_" + side, "x": [b_line, rear_door_end], "z": [sill, roof],
                        "sides": side, "material": "paint",
                        "hinge": {"point": _r((b_line, sy * hw, belt - 0.1)), "axis": [0.0, 0.0, 1.0],
                                  "note": "at the B-pillar line"}})
    for side in ("left", "right"):
        # the quarter wraps round to the tail above the rear bumper
        out.append({"name": "rear_quarter_" + side, "x": [rear_door_end, L], "z": [rb_top, roof],
                    "sides": side, "material": "paint"})
        # the quarter below the bumper line, ahead of the bumper
        out.append({"name": "rear_quarter_lower_" + side, "x": [rear_door_end, L - BUMPER_DEPTH],
                    "z": [sill, rb_top], "sides": side, "material": "paint"})
    out += [
        {"name": "roof", "x": [d["roof_front"], d["roof_back"]], "z": [roof - 0.06, roof + p.roof_crown],
         "sides": "top", "material": "paint"},
        {"name": "tailgate", "x": [d["roof_back"], tail_end], "z": [rb_top, top_z(p, d["roof_back"])],
         "sides": "top", "material": "paint",
         "hinge": {"point": _r((d["roof_back"], 0.0, top_z(p, d["roof_back"]))), "axis": [0.0, 1.0, 0.0],
                   "note": "at the roof back"}},
        {"name": "rear_bumper", "x": [L - BUMPER_DEPTH, L], "z": [sill, rb_top], "sides": "both",
         "material": "black_plastic"},
    ]
    for q in out:
        q["x"], q["z"] = _r(q["x"]), _r(q["z"])
        q["welded_in_stage_1"] = True
    return out


def glass(p):
    """One glass slot per window, each with the panel it belongs to."""
    d = p.derived()
    belt = p.belt_z
    ln = lines(p)
    roof = p.height - p.roof_crown
    g = [{"name": "windscreen", "x": [d["screen_base"], d["roof_front"]], "z": [belt, roof],
          "part_of": None}]
    for side in ("left", "right"):
        g.append({"name": "front_side_window_" + side, "x": [ln["a_line"], ln["b_line"]],
                  "z": [belt, roof], "part_of": "front_door_" + side})
    for side in ("left", "right"):
        g.append({"name": "rear_side_window_" + side,
                  "x": [ln["b_line"], min(ln["rear_door_end"], d["roof_back"])],
                  "z": [belt, roof], "part_of": "rear_door_" + side})
    g.append({"name": "rear_screen", "x": [d["roof_back"], d["hatch_base"]],
              "z": [p.tail_top_z, top_z(p, d["roof_back"])], "part_of": "tailgate"})
    for q in g:
        q["x"], q["z"] = _r(q["x"]), _r(q["z"])
        q["material"] = "glass"
    return g


LAMP_PREFIXES = ("headlamp_", "indicator_", "tail_lamp_", "brake_lamp_", "reverse_lamp_")


def sockets(p):
    """Named sockets: position (x, y, z) and a short note. Heights are est."""
    d = p.derived()
    L, hw, belt = p.length, p.width / 2, p.belt_z
    ln = lines(p)
    nose_hw = half_width_at(p, 0.03)
    tail_hw = half_width_at(p, L - 0.03)
    s = {}

    def add(name, pos, note="", **extra):
        s[name] = dict({"pos": _r(pos), "note": note}, **extra)

    def lamp(name, pos, note="est."):
        # lens material, its glow switched by a value (checklist item 10)
        add(name, pos, note, material="lens", glow=0.0)
    lamp_z = p.nose_top_z - 0.10
    for side, sy in (("left", 1), ("right", -1)):
        lamp("headlamp_" + side, (0.03, sy * nose_hw * 0.62, lamp_z), "est. height")
        lamp("indicator_front_" + side, (0.04, sy * nose_hw * 0.88, lamp_z - 0.03))
        lamp("tail_lamp_" + side, (L - 0.03, sy * tail_hw * 0.80, p.tail_top_z - 0.12))
        lamp("brake_lamp_" + side, (L - 0.03, sy * tail_hw * 0.80, p.tail_top_z - 0.06))
        lamp("indicator_rear_" + side, (L - 0.03, sy * tail_hw * 0.90, p.tail_top_z - 0.09))
        lamp("reverse_lamp_" + side, (L - 0.03, sy * tail_hw * 0.62, p.tail_top_z - 0.12))
    add("plate_front", (0.0, 0.0, p.sill_z + FRONT_BUMPER_RISE / 2), "520 x 111 mm, on the bumper, est.",
        size=[PLATE_W, PLATE_H], material="plate")
    add("plate_rear", (L, 0.0, p.tail_top_z - 0.30), "520 x 111 mm, est. height",
        size=[PLATE_W, PLATE_H], material="plate")
    # Right-hand drive: the driver sits on the car's right, y negative. The hip
    # point sits just ahead of the B-pillar (est.).
    seat = (ln["b_line"] - 0.10, -0.36, p.sill_z + 0.22)
    add("driver_seat", seat, "hip point, right-hand drive, est.")
    add("driver_hands", (seat[0] - 0.45, seat[1], belt + 0.05), "wheel centre, est.")
    add("camera_driver_head", (seat[0] - 0.05, seat[1], seat[2] + 0.62), "eye point, est.")
    add("camera_chase_anchor", (L / 2, 0.0, p.height), "boom root, est.", boom_length=5.0)
    add("camera_bonnet", (d["screen_base"] - 0.2, 0.0, belt + 0.05), "est.")
    add("engine_sound", (d["front_axle"] - 0.25, 0.0, 0.55), "transverse front engine, est.")
    add("exhaust", (L + 0.02, -0.45, p.sill_z - 0.05), "tailpipe, est.")
    add("horn", (0.12, 0.25, 0.45), "est.")
    for side, sy in (("left", 1), ("right", -1)):
        add("door_handle_front_" + side, (ln["b_line"] - 0.12, sy * hw, belt - 0.06), "est.")
        if DOORS == 5:
            add("door_handle_rear_" + side, (ln["rear_door_end"] - 0.10, sy * hw, belt - 0.06), "est.")
    add("interior", (d["screen_base"], 0.0, p.sill_z), "slot origin; bounds follow",
        material="interior",
        bounds={"x": _r([d["screen_base"], d["hatch_base"]]),
                "y": _r([-(hw - 0.08), hw - 0.08]),
                "z": _r([p.sill_z, p.height - p.roof_crown - 0.04])})
    return s


def mass_and_size(p):
    d = p.derived()
    com_x = d["front_axle"] + 0.40 * p.wheelbase   # about 60:40 front weight, est.
    return {
        "kerb_mass_kg": KERB_MASS_KG,
        "kerb_mass_note": "est. for the class (about 850 to 950 kg)",
        "centre_of_mass": _r((com_x, 0.0, 0.48)),
        "centre_of_mass_note": "est.: slightly ahead of mid-wheelbase and low",
        "length": _r(p.length), "width": _r(p.width), "height": _r(p.height),
        "wheelbase": _r(p.wheelbase), "track": _r(p.track),
        "wheel_radius": _r(p.wheel_radius), "tyre_width": _r(p.tyre_width),
        "root_bone": {"name": ROOT_BONE, "pos": _r((p.length / 2, 0.0, 0.0))},
    }


def derive(p):
    """The whole kit as one JSON-able dict."""
    return {
        "source": "car_kit.py, lane session, 17 November 2026",
        "params": asdict(p),
        "materials": list(MATERIALS),
        "wheels": wheels(p),
        "collision": collision(p),
        "panels": panels(p),
        "glass": glass(p),
        "sockets": sockets(p),
        "mass_and_size": mass_and_size(p),
    }


def _inside(item, x, z, tol=1e-6):
    return item["x"][0] - tol <= x <= item["x"][1] + tol and item["z"][0] - tol <= z <= item["z"][1] + tol


def _overlap(a, b):
    ox = min(a["x"][1], b["x"][1]) - max(a["x"][0], b["x"][0])
    oz = min(a["z"][1], b["z"][1]) - max(a["z"][0], b["z"][0])
    return ox > PANEL_TOL and oz > PANEL_TOL


def box_side_cover(p, boxes, n=20):
    """Share of the loft's side area (sill to top line, sampled at n stations)
    that the boxes' side outlines cover."""
    L = p.length
    total = covered = 0.0
    for i in range(n):
        x = L * (i + 0.5) / n
        z0, z1 = p.sill_z, top_z(p, x)
        if z1 <= z0:
            continue
        total += z1 - z0
        spans = []
        for b in boxes:
            c, h = b["centre"], b["half_extent"]
            if c[0] - h[0] <= x <= c[0] + h[0]:
                a, e = max(z0, c[2] - h[2]), min(z1, c[2] + h[2])
                if e > a:
                    spans.append((a, e))
        spans.sort()
        cur = None
        for a, e in spans:
            if cur is None or a > cur[1]:
                if cur:
                    covered += cur[1] - cur[0]
                cur = [a, e]
            else:
                cur[1] = max(cur[1], e)
        if cur:
            covered += cur[1] - cur[0]
    return covered / total if total else 0.0


def check(p, kit=None):
    """Every failure as a plain sentence; an empty list means it passes. The
    checks read the kit data, so a kit with wrong data fails."""
    kit = kit or derive(p)
    fails = ["loft: " + f for f in car_loft.check(p)]
    m = measure(p, build(p))
    L = p.length
    d = p.derived()
    ln = lines(p)
    mats = set(kit.get("materials", []))
    if mats != set(MATERIALS):
        fails.append("material slots differ from the plan: %s" % sorted(mats))
    # wheels
    w = kit["wheels"]
    if len(w) != 4:
        fails.append("not four wheels")
    by = {q["name"]: q for q in w}
    for f, r in (("FL", "FR"), ("RL", "RR")):
        if f in by and r in by and (abs(by[f]["hub"][1] + by[r]["hub"][1]) > 1e-6 or by[f]["hub"][1] <= 0):
            fails.append("wheels %s and %s not mirrored across the centreline" % (f, r))
    if len({q["bone"] for q in w}) != len(w):
        fails.append("wheel bone names not unique")
    for q in w:
        front = q["name"].startswith("F")
        axle = d["front_axle"] if front else d["rear_axle"]
        if abs(q["hub"][0] - axle) > 1e-3:
            fails.append("%s: hub not on its axle" % q["name"])
        if abs(q["hub"][2] - q["radius"]) > 1e-3:
            fails.append("%s: hub height is not the wheel radius" % q["name"])
        if q["spin_axis"] != [0.0, 1.0, 0.0]:
            fails.append("%s: spin axis is not across the car" % q["name"])
        if q["steers"] != front or q["driven"] != front:
            fails.append("%s: steering or drive not on the front wheels only" % q["name"])
        for part, mat in q["parts"].items():
            if mat not in MATERIALS:
                fails.append("%s %s: material %s not a slot" % (q["name"], part, mat))
        if q["arch_lip_gap"] < MIN_LIP_GAP:
            fails.append("%s: arch lip gap %.3f under %.3f" % (q["name"], q["arch_lip_gap"], MIN_LIP_GAP))
        if q["wheelhouse_room_up"] < q["travel_up"]:
            fails.append("%s: wheelhouse room %.3f under the up travel %.3f"
                         % (q["name"], q["wheelhouse_room_up"], q["travel_up"]))
        if q["hub"][2] - q["travel_down"] < 0.1:
            fails.append("%s: droop takes the hub too low" % q["name"])
    # collision
    boxes = kit["collision"]
    if len(boxes) > MAX_COLLISION:
        fails.append("collision has %d shapes, over %d" % (len(boxes), MAX_COLLISION))
    lo = (0.0, -m["width"] / 2, p.keel_z)
    hi = (L, m["width"] / 2, m["height"])
    for b in boxes:
        c, h = b["centre"], b["half_extent"]
        for i in range(3):
            if c[i] - h[i] < lo[i] - BOX_MARGIN or c[i] + h[i] > hi[i] + BOX_MARGIN:
                fails.append("collision box %s outside the body bounds" % b["name"])
                break
        if min(h) <= 0:
            fails.append("collision box %s is flat or inverted" % b["name"])
    cover = box_side_cover(p, boxes)
    if cover < MIN_BOX_COVER:
        fails.append("collision covers %.0f%% of the side area, under %.0f%%" % (100 * cover, 100 * MIN_BOX_COVER))
    # panels: every point of each side's outline lies in some panel or glass,
    # and no two panels seen from the same side overlap
    pn = {q["name"]: q for q in kit["panels"]}
    for q in kit["panels"]:
        if q["x"][1] <= q["x"][0] or q["z"][1] <= q["z"][0]:
            fails.append("panel %s has no size" % q["name"])
        if q.get("material") not in MATERIALS:
            fails.append("panel %s has no planned material" % q["name"])
    for side in ("left", "right"):
        seen = [q for q in kit["panels"] if q["sides"] in (side, "both", "top")]
        flat = [q for q in kit["panels"] if q["sides"] in (side, "both")]
        holes = 0
        for i in range(60):
            x = 0.02 + (L - 0.04) * i / 59
            z0, z1 = p.sill_z + 0.01, top_z(p, x) - 0.01
            for j in range(12):
                z = z0 + (z1 - z0) * j / 11
                if not any(_inside(q, x, z) for q in seen + kit["glass"]):
                    holes += 1
        if holes:
            fails.append("side %s: %d sampled points of the outline in no panel" % (side, holes))
        for i, a in enumerate(flat):
            for b in flat[i + 1:]:
                if _overlap(a, b):
                    fails.append("side %s: %s and %s overlap" % (side, a["name"], b["name"]))
    tops = [q for q in kit["panels"] if q["sides"] == "top"]
    for i, a in enumerate(tops):
        for b in tops[i + 1:]:
            if _overlap(a, b):
                fails.append("%s and %s overlap" % (a["name"], b["name"]))
    for q in kit["panels"]:
        opening = q["name"] in ("bonnet", "tailgate") or q["name"].startswith(("front_door", "rear_door"))
        if opening and "hinge" not in q:
            fails.append("%s has no hinge" % q["name"])
        if "door" in q["name"] and q["x"][1] - q["x"][0] < 0.55:
            fails.append("%s only %.2f m long" % (q["name"], q["x"][1] - q["x"][0]))
    # glass
    for g in kit["glass"]:
        if g["x"][1] <= g["x"][0] or g["z"][1] <= g["z"][0]:
            fails.append("glass %s has no size" % g["name"])
        host = g.get("part_of")
        if host:
            if host not in pn:
                fails.append("glass %s belongs to a missing panel %s" % (g["name"], host))
            elif not all(_inside(pn[host], x, z, PANEL_TOL) for x in g["x"] for z in g["z"]):
                fails.append("glass %s not inside its panel %s" % (g["name"], host))
    # sockets
    s = kit["sockets"]
    need = ["headlamp_left", "headlamp_right", "tail_lamp_left", "tail_lamp_right",
            "brake_lamp_left", "brake_lamp_right", "indicator_front_left", "indicator_front_right",
            "indicator_rear_left", "indicator_rear_right", "plate_front", "plate_rear",
            "driver_seat", "camera_driver_head", "camera_chase_anchor", "engine_sound",
            "exhaust", "interior", "door_handle_front_left", "door_handle_front_right"]
    if DOORS == 5:
        need += ["door_handle_rear_left", "door_handle_rear_right"]
    for n in need:
        if n not in s:
            fails.append("socket %s missing" % n)
    names = list(s) + [g["name"] for g in kit["glass"]] + [q["name"] for q in kit["panels"]]
    if len(names) != len(set(names)):
        fails.append("names not unique across sockets, glass and panels")
    for n, v in s.items():
        if n.startswith(LAMP_PREFIXES) and (v.get("material") != "lens" or "glow" not in v):
            fails.append("lamp %s has no lens material or glow value" % n)
    if "driver_seat" in s:
        sx, sy = s["driver_seat"]["pos"][0], s["driver_seat"]["pos"][1]
        if sy >= 0:
            fails.append("driver seat not on the car's right (right-hand drive)")
        if not ln["a_line"] + 0.3 < sx < ln["b_line"]:
            fails.append("driver seat not in the front door's span (A-pillar to B-pillar)")
        if abs(sy) + 0.25 > p.width / 2 - p.shoulder_in:
            fails.append("driver seat too near the side for the driver's shoulders")
    for side in ("left", "right"):
        h = s.get("door_handle_front_" + side)
        if h and not ln["a_line"] < h["pos"][0] < ln["b_line"]:
            fails.append("front door handle %s not on the front door" % side)
        h = s.get("door_handle_rear_" + side)
        if h and not ln["b_line"] < h["pos"][0] < ln["rear_door_end"]:
            fails.append("rear door handle %s not on the rear door" % side)
    if "camera_driver_head" in s and s["camera_driver_head"]["pos"][2] > p.height - p.roof_crown - 0.08:
        fails.append("driver head camera above the headlining")
    for n in ("plate_front", "plate_rear"):
        if n in s and s[n]["size"][0] / 2 > half_width_at(p, s[n]["pos"][0]) - 0.05:
            fails.append("%s wider than the body at its station" % n)
    # mass and size (read from the kit data)
    ms = kit["mass_and_size"]
    if not MASS_RANGE[0] <= ms["kerb_mass_kg"] <= MASS_RANGE[1]:
        fails.append("kerb mass %.0f outside the class estimate" % ms["kerb_mass_kg"])
    cx = ms["centre_of_mass"][0]
    if not (d["front_axle"] < cx < (d["front_axle"] + d["rear_axle"]) / 2):
        fails.append("centre of mass not slightly forward of mid-wheelbase")
    if not 0.3 < ms["centre_of_mass"][2] < 0.6:
        fails.append("centre of mass not low")
    for k in ("wheelbase", "track", "wheel_radius"):
        if abs(ms[k] - getattr(p, k)) > 1e-3:
            fails.append("size data %s disagrees with the params" % k)
    return fails


def main(argv):
    p = HatchParams(**car_loft.ROUND3_PROPOSAL) if "--round3" in argv else HatchParams()
    kit = derive(p)
    if "--out" in argv:
        path = argv[argv.index("--out") + 1]
        with open(path, "w") as f:
            json.dump(kit, f, indent=1)
        print("wrote", path)
    fails = check(p, kit)
    print("PASS" if not fails else "FAIL:\n- " + "\n- ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
