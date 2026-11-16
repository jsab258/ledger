"""The street's checks (n16-4): width front to front, from the scene spec.

    python tools/street_checks.py              # checks production/specs/vignette-scene.json
    python tools/street_checks.py --selftest

WHY (order of 16 Nov, n16-4; study 04 s04-01): a town street of terraced fronts is 9 to 15 m front to front; a spec
change that narrows or widens it past that reads wrong. Target and design: production/research/street-checks/
N16-4-TARGET-2026-11-16.md section 3a. Width = 2 x (carriageway half width + kerb + footway). A missing field fails,
never skips. Kit reuse (3b) waits for a placement spec; the street's ends (3c) come next.
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCENE = os.path.join(ROOT, "production", "specs", "vignette-scene.json")
LOW, HIGH = 9.0, 15.0


def width_of(scene):
    s = scene.get("street") or {}
    try:
        half = float(s["carriageway"]["half_width_m"])
        kerb = float(s["kerb"]["width_m"])
        foot = float(s["footway"]["width_m"])
    except (KeyError, TypeError, ValueError) as e:
        return None, "missing field %s" % e
    return round(2 * (half + kerb + foot), 3), ""


def check(scene, name="quay_street"):
    w, why = width_of(scene)
    if w is None:
        return False, "street-width: %s %s FAIL" % (name, why)
    ok = LOW - 0.0005 <= w <= HIGH + 0.0005
    return ok, "street-width: %s %.3f m (%.1f-%.1f) %s" % (name, w, LOW, HIGH, "PASS" if ok else "FAIL")


def closers_of(scene):
    """Footprints in plan (x0, x1, z0, z1, top height) of every block and every street_ends entry."""
    out = []
    half = float(scene["street"]["carriageway"]["half_width_m"])
    front = half + float(scene["street"]["kerb"]["width_m"]) + float(scene["street"]["footway"]["width_m"])
    for b in scene.get("blocks", []):
        x0 = float(b["start_x_m"]); x1 = x0 + b["bays"] * float(b["bay_width_m"])
        d = float(b["depth_m"]); top = 0.1 + sum(b["storey_heights_m"])
        z0, z1 = (front, front + d) if b["side"] == "east" else (-front - d, -front)
        out.append((x0, x1, z0, z1, top, b["id"]))
    for e in scene.get("street_ends", []):
        out.append((float(e["x0_m"]), float(e["x1_m"]), float(e["z0_m"]), float(e["z1_m"]), float(e["top_m"]), e["id"]))
    return out


def ray_hit(ox, oz, dx, dz, box):
    """Distance along a plan ray to an axis-aligned box (slab method), or None."""
    x0, x1, z0, z1 = box[:4]
    tmin, tmax = 0.0, 1e9
    for o, dd, lo, hi in ((ox, dx, x0, x1), (oz, dz, z0, z1)):
        if abs(dd) < 1e-12:
            if o < lo or o > hi:
                return None
            continue
        t0, t1 = (lo - o) / dd, (hi - o) / dd
        if t0 > t1:
            t0, t1 = t1, t0
        tmin, tmax = max(tmin, t0), min(tmax, t1)
        if tmin > tmax:
            return None
    return tmin


def ends(scene, cam_ids=None):
    """Rays every 1 degree over +-10 about the street axis from each along-street camera (target 3c, by data)."""
    import math
    length = float(scene["street"]["length_m"])
    closers = closers_of(scene)
    lines, all_ok = [], True
    for c in scene.get("cameras", []):
        yaw = float(c.get("yaw_deg", 0)) % 360
        axis = 0.0 if min(yaw, 360 - yaw) <= 30 else (180.0 if abs(yaw - 180) <= 30 else None)
        if axis is None or (cam_ids and c["id"] not in cam_ids):
            continue
        ox, oz, eye = float(c["x_m"]), float(c["z_m"]), float(c.get("eye_height_m", 1.6))
        end_x = length if axis == 0.0 else 0.0
        closed, nearest = 0, None
        for k in range(-10, 11):
            a = math.radians(axis + k)
            dx, dz = math.cos(a), math.sin(a)
            # the road's end along this ray
            t_end = (end_x - ox) / dx
            best = None
            for box in closers:
                t = ray_hit(ox, oz, dx, dz, box)
                if t is None or t > t_end + 1e-6 or box[4] <= eye:
                    continue
                if best is None or t < best:
                    best = t
            if best is not None:
                closed += 1
                nearest = best if nearest is None else min(nearest, best)
        ok = closed == 21
        all_ok &= ok
        lines.append("street-ends: %s %d/21 rays closed%s %s" % (
            c["id"], closed, " (nearest %.0f m)" % nearest if nearest is not None else "", "PASS" if ok else "FAIL"))
    return all_ok, lines


def selftest():
    base = {"street": {"carriageway": {"half_width_m": 3.0}, "kerb": {"width_m": 0.125}, "footway": {"width_m": 2.0}}}
    import copy
    cases = []
    cases.append(("today's widths pass", base, True))
    c = copy.deepcopy(base); c["street"]["footway"]["width_m"] = 0.5; cases.append(("footway 0.5 fails (7.25 m)", c, False))
    c = copy.deepcopy(base); c["street"]["carriageway"]["half_width_m"] = 6.0; cases.append(("half width 6 fails (16.25 m)", c, False))
    c = copy.deepcopy(base); c["street"]["carriageway"]["half_width_m"] = 2.375; cases.append(("boundary 9.000 passes", c, True))
    c = copy.deepcopy(base); del c["street"]["kerb"]; cases.append(("missing kerb fails", c, False))
    failed = 0
    for label, scene, want in cases:
        got, line = check(scene)
        ok = got == want
        failed += not ok
        print("  %s %s  (%s)" % ("ok  " if ok else "FAIL", label, line))
    # the street's ends, target 3c's fixtures (cam_A only)
    street = dict(base["street"], length_m=48.0)
    blocks = [{"id": "e", "side": "east", "start_x_m": 3.0, "bays": 6, "bay_width_m": 6.0, "depth_m": 8.0,
               "storey_heights_m": [3.4, 2.8]},
              {"id": "w", "side": "west", "start_x_m": 3.0, "bays": 6, "bay_width_m": 6.0, "depth_m": 8.0,
               "storey_heights_m": [3.4, 2.8]}]
    cam = [{"id": "cam_A", "x_m": 4.0, "z_m": 4.0, "yaw_deg": 0.0, "eye_height_m": 1.6}]
    closer = {"id": "end", "x0_m": 47.0, "x1_m": 48.0, "z0_m": -6.0, "z1_m": 6.0, "top_m": 8.0}
    low = dict(closer, top_m=1.2)
    for label, se, want in (("a closer inside the road's end passes", [closer], True),
                            ("no closer fails", [], False),
                            ("a closer below the eye fails", [low], False)):
        got, lines = ends({"street": street, "blocks": blocks, "cameras": cam, "street_ends": se})
        ok = got == want
        failed += not ok
        cases.append(label)
        print("  %s %s  (%s)" % ("ok  " if ok else "FAIL", label, "; ".join(lines)))
    print("street_checks selftest: passed=%d/%d failed=%d" % (len(cases) - failed, len(cases), failed))
    return 1 if failed else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()
    with open(SCENE, encoding="utf-8") as f:
        scene = json.load(f)
    if "--ends" in argv:
        # report only until the ends are designed (the quay end reaches his page): a known shortfall, not in ci
        ok, lines = ends(scene)
        print("\n".join(lines))
        return 0 if ok else 1
    ok, line = check(scene)
    print(line)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
