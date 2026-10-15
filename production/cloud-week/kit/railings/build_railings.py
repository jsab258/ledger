"""The street's one kerbside guard rail panel (railings target, kind A1; cloud week 42, unit 3.3), built by script from target.json.

    /home/user/.bpyenv/bin/python build_railings.py [--paint galvanised|black] [--out-dir DIR] [--npz-dir DIR]

Reads production/cloud-week/targets/railings/target.json (kinds.A1). Writes production/assets/cloud-week/railings/guard_rail_A1.glb
(the panel: two posts with caps, the top rail laid flat, the bottom rail, 17 bars with welds, four end plates, four M10 studs with nuts)
and guard_rail_A1_ground_patch.glb (the two dark reinstatement patches, a separate mesh, not in the panel's bounding box), and
kit/railings/build/<name>.npz for check_railings.py.

Frame (the target's): x along the panel (0 at its middle), y across (+ toward the carriageway), z up from the flag top at the posts; the
pivot is the middle of the panel on the ground. Millimetres while building, metres in the file. Q2 (the quay tube railing: the jetty only,
not on Quay Street) and R3 (three cast-iron kinds, unplaced reserve) are not built in this unit. The seeds (a lean of 0 to 1 degree,
bent bars, a polished top rail) belong to the engine's variants and masks, not to this model.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_shopfront as bs  # noqa: E402  (the shared mesh helpers: prisms, lofts, finishing, glb export)

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "railings", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "railings")
NPZ_DIR = os.path.join(HERE, "build")


def rrect(w, h, r, n=6):
    """A rounded rectangle w x h, corner radius r, counter-clockwise, centred, as a point list (u, v)."""
    pts = []
    for cx, cy, a0 in ((w / 2 - r, h / 2 - r, 0.0), (-w / 2 + r, h / 2 - r, 90.0), (-w / 2 + r, -h / 2 + r, 180.0), (w / 2 - r, -h / 2 + r, 270.0)):
        for k in range(n + 1):
            a = math.radians(a0 + 90.0 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


class Parts:
    def __init__(self):
        self.objs, self.meta = [], {}

    def add(self, name, VF, mat, bev=bs.BEVEL, min_angle=50.0):
        ob = bs.new_obj(name, VF[0], VF[1])
        self.meta[ob.name] = (mat, bev, min_angle)
        self.objs.append(ob)
        return ob


def prism_x(profile_yz, x0, x1):
    """A (y, z) profile extruded along x."""
    P = np.asarray(profile_yz, float)
    n = len(P)
    V = np.zeros((2 * n, 3))
    for k, x in enumerate((x0, x1)):
        V[k * n:(k + 1) * n] = np.column_stack([np.full(n, x), P[:, 0], P[:, 1]])
    F = [tuple(range(n)), tuple(range(n, 2 * n))[::-1]] + [(i, n + i, n + (i + 1) % n, (i + 1) % n) for i in range(n)]
    return V, F


def cyl_x(x0, x1, y, z, r, n=12):
    rings = []
    for x in (x0, x1):
        rings.append([(x, y + r * math.cos(2 * math.pi * k / n), z + r * math.sin(2 * math.pi * k / n)) for k in range(n)])
    V, F = bs.loft_rings(rings)
    return V, [tuple(f[::-1]) for f in F] if False else F


def bar(x, z0, z1, r=6.0, weld=2.0, n=12):
    """A vertical round bar with a 2 mm weld fillet at each end (a cone from r + 2 to r), its ends 0.5 into the rails."""
    zs = [(z0 - 0.5, r + weld), (z0, r + weld), (z0 + weld, r), (z1 - weld, r), (z1, r + weld), (z1 + 0.5, r + weld)]
    rings = [[(x + rr * math.cos(2 * math.pi * k / n), rr * math.sin(2 * math.pi * k / n), z) for k in range(n)] for z, rr in zs]
    return bs.loft_rings(rings)


def build(T, paint, out_dir, npz_dir):
    import bpy
    A = T["kinds"]["A1"]
    P = A["panel"]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    steel = (118, 120, 122) if paint == "galvanised" else (24, 24, 26)
    rough = 0.55 if paint == "galvanised" else 0.42
    metal = 1.0 if paint == "galvanised" else 0.0
    mname = "galvanised_steel" if paint == "galvanised" else "paint_black"
    mats = {mname: bs.make_material(mname, steel, rough, metal), "bare_zinc": bs.make_material("bare_zinc", (150, 150, 152), 0.5, 1.0),
            "tarmac_patch": bs.make_material("tarmac_patch", (45, 43, 41), 0.85, 0.0)}
    nut_mat = "bare_zinc" if paint == "galvanised" else mname
    B = Parts()
    post, cap = P["post"], P["cap"]
    out = rrect(post["width"], post["depth"], 4.5)
    for sx, tag in ((-1.0, "l"), (1.0, "r")):
        x = sx * 1000.0
        B.add("post_" + tag, bs.prism_ud([(x + p[0], p[1]) for p in out], 0.0, cap["z"][0]), mname, bev=1.0)
        B.add("cap_" + tag, bs.prism_ud([(x + p[0], p[1]) for p in out], cap["z"][0], cap["z"][1]), mname, bev=cap["edge_radius"])
    tr, br = P["top_rail"], P["bottom_rail"]
    pe = P["end_plates"]["thickness"]
    xe = 975.0 - pe                                                   # the rails end 0.3 inside the plates
    for nm, rail, r in (("top_rail", tr, 4.5), ("bottom_rail", br, 3.75)):
        prof = [(p[0], rail["axis_z"] + p[1]) for p in rrect(rail["width"], rail["height"], r)]
        B.add(nm, prism_x(prof, -(xe + 0.3), xe + 0.3), mname, bev=0.8)
        for sx, tag in ((-1.0, "l"), (1.0, "r")):
            x0, x1 = sorted((sx * xe, sx * 975.0))
            B.add("%s_plate_%s" % (nm[:3], tag), prism_x(prof, x0, x1), mname, bev=0.8)
    for i, bx in enumerate(P["infill"]["x"]):
        B.add("bar_%02d" % i, bar(bx, P["infill"]["z"][0], P["infill"]["z"][1], r=P["infill"]["diameter"] / 2.0), mname, bev=None)
    for b in P["bolts"]["list"]:
        sx = 1.0 if b["post_x"] > 0 else -1.0
        tag = ("l" if sx < 0 else "r") + ("t" if b["z"] > 500 else "b")
        x0, x1 = sorted((b["plate_x"][1] - sx * 1.0, b["thread_end_x"]))
        B.add("stud_" + tag, cyl_x(x0, x1, b["y"], b["z"], P["bolts"]["stud"]["diameter"] / 2.0), nut_mat, bev=None)
        af = P["bolts"]["nut"]["across_flats"]
        R = af / math.sqrt(3.0)
        hexp = [(b["y"] + R * math.cos(math.radians(60 * k)), b["z"] + R * math.sin(math.radians(60 * k))) for k in range(6)]
        n0, n1 = sorted(b["nut_x"])
        B.add("nut_" + tag, prism_x(hexp, n0, n1), nut_mat, bev=1.0)
    obs = bs.finish(B, mats, 0.0)
    res = {"A1": bs.write(obs, "guard_rail_A1", 0.0, out_dir, npz_dir)}
    # the ground patches, a separate mesh: one at each post, the target's ragged outline, top 1 proud of the flag
    bpy.ops.wm.read_factory_settings(use_empty=True)
    mats = {"tarmac_patch": bs.make_material("tarmac_patch", (45, 43, 41), 0.85, 0.0)}
    B = Parts()
    op = A["ground"]["patch"]["outline_xy"]
    for sx, tag in ((-1.0, "l"), (1.0, "r")):
        B.add("patch_" + tag, bs.prism_ud([(sx * 1000.0 + p[0], -p[1]) for p in op][::-1], -10.0, 1.0), "tarmac_patch", bev=None)
    obs = bs.finish(B, mats, 0.0)
    res["patch"] = bs.write(obs, "guard_rail_A1_ground_patch", 0.0, out_dir, npz_dir)
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paint", default="galvanised", choices=["galvanised", "black"])
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    res = build(T, a.paint, a.out_dir, a.npz_dir)
    for k, v in res.items():
        print(k, "triangles", v["triangles"], "glb bytes", v["glb_bytes"], flush=True)
    os.makedirs(a.npz_dir, exist_ok=True)
    json.dump(res, open(os.path.join(a.npz_dir, "parts.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
