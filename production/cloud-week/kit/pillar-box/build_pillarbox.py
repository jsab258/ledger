"""Quay Street's pillar box (pillar-box target; cloud week 42, unit 3.6), built by script, to the proportions of the two dated photographs.

    /home/user/.bpyenv/bin/python build_pillarbox.py [--out-dir DIR] [--npz-dir DIR]

Reads production/cloud-week/targets/pillar-box/target.json for what the target fixes (the colours, the slot's height and centre, the door's 1 mm and its 3 x 3 groove, the
plate frame's bezel and recess, the 1500 total height, no cypher, no lettering, no maker's mark) and builds it with PHOTO-CHECK.md's amendments, which win over the target's
body, foot and cap numbers (two Geograph photographs, 2009 and 2012; DECISIONS 11 Oct 21:55): body 390 across, a straight black base 300 high no wider than 398, the cap
rim 535 across and about 65 deep, the dome rising 60, the slot 250 wide. Door, plate frame and escutcheon are the target's scaled 0.8 to the narrower body.

Writes production/assets/cloud-week/pillar-box/pillar_box.glb (metres, z up, the axis at the footway, +y the front, the hidden skirt to z -150) and build/pillar_box.npz.
The cypher and the operator's lettering are FLUSH reserved areas (no geometry); the collection plate's words are a texture, the plate is a plain enamel panel here.
"""
import argparse
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "railings"))
sys.path.insert(0, os.path.join(HERE, "..", "bollards"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import build_shopfront as bs  # noqa: E402
from build_railings import Parts, rrect  # noqa: E402
from build_bollards import lathe, prism_y, fillet  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "pillar-box", "target.json")
ASSET_DIR = os.path.join(REPO, "production", "assets", "cloud-week", "pillar-box")
NPZ_DIR = os.path.join(HERE, "build")

R_BODY, R_BASE, Z_BASE = 195.0, 199.0, 300.0                  # PHOTO-CHECK: body 390, a straight black base 300 high at most 4 wider
R_RIM = 267.5                                                 # the cap rim 535 across
Z_COVE0, Z_RIM0, Z_RIM1, Z_NECK1 = 1342.0, 1362.0, 1420.0, 1440.0
R_SHELF, DOME_RISE, Z_TOP = 245.0, 60.0, 1500.0
SLOT_W, SLOT_H, SLOT_Z = 250.0, 45.0, 1278.0
DOOR_W, DOOR_Z0, DOOR_Z1 = 240.0, 330.0, 1180.0               # the target's 300 wide scaled 0.8; the top stops 10 under the lettering band (1190 to 1230)
SIDES = 96                                                    # the lathe's sides (the target asks for 8,000 to 30,000 triangles)
LOCK_X, LOCK_Z = 90.0, 818.0                                  # the target's 112 scaled 0.8, on the right as seen from the front
FRAME_W, FRAME_H, FRAME_Z = 168.0, 100.0, 950.0


def body_profile():
    """(r, z) from the foot of the red body up to the apex: the body to the cap's soffit, a cove out to the rim, the vertical rim with its rounded top, a flat shelf, a short
    neck and the shallow dome (sagitta 60 on r 245)"""
    pts = [(0.0, Z_BASE), (R_BODY, Z_BASE), (R_BODY, Z_COVE0)]
    for k in range(1, 9):                                     # the cove: a quarter ellipse, concave, out to the rim
        a = math.radians(90.0 * k / 8)
        pts.append((R_BODY + (R_RIM - R_BODY) * math.sin(a), Z_COVE0 + (Z_RIM0 - Z_COVE0) * (1 - math.cos(a))))
    pts += [(R_RIM, Z_RIM1 - 6.0)]
    for k in range(1, 5):                                     # the rim's top edge, R6
        a = math.radians(90.0 * k / 4)
        pts.append((R_RIM - 6.0 + 6.0 * math.cos(a), Z_RIM1 - 6.0 + 6.0 * math.sin(a)))
    pts += [(R_SHELF, Z_RIM1), (R_SHELF, Z_NECK1)]
    Rs = (R_SHELF ** 2 + DOME_RISE ** 2) / (2 * DOME_RISE)
    for k in range(1, 17):
        r = R_SHELF * (1 - k / 16.0)
        pts.append((r, Z_TOP - (Rs - math.sqrt(max(Rs * Rs - r * r, 0.0)))))
    i = [j for j, p in enumerate(pts) if abs(p[0] - R_SHELF) < 1e-9 and abs(p[1] - Z_NECK1) < 1e-9][0]
    return fillet(pts, {i: 2.5})                              # the neck's top edge eased (the target's 1.5 lips, a little more on a 62 degree turn)


def base_profile():
    return [(0.0, -150.0), (R_BASE, -150.0), (R_BASE, Z_BASE - 3.0), (R_BASE - 0.6, Z_BASE - 0.1), (R_BASE - 2.2, Z_BASE + 2.0), (R_BODY, Z_BASE + 6.0), (0.0, Z_BASE + 6.0)]


def arc_solid(sect_rz, a0, a1, n=None):
    """a closed section (r, z) swept about the axis from angle a0 to a1 (degrees from the front, +y; positive toward +x)"""
    n = n or max(4, int(math.ceil(abs(a1 - a0) / 3.0)))
    P = np.asarray(sect_rz, float)
    m = len(P)
    V = []
    for k in range(n + 1):
        a = math.radians(a0 + (a1 - a0) * k / n)
        for r, z in P:
            V.append((r * math.sin(a), r * math.cos(a), z))
    F = []
    for k in range(n):
        for i in range(m):
            j = (i + 1) % m
            F.append((k * m + i, k * m + j, (k + 1) * m + j, (k + 1) * m + i))
    F.append(tuple(range(m))[::-1])
    F.append(tuple(range(n * m, (n + 1) * m)))
    Vn = np.array(V)
    vol = sum(np.dot(Vn[f[0]], np.cross(Vn[f[i]], Vn[f[i + 1]])) / 6.0 for f in F for i in range(1, len(f) - 1))
    if vol < 0:
        F = [tuple(f[::-1]) for f in F]
    return Vn, F


def build(T, out_dir, npz_dir):
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    red = T["paint"]
    mats = {"paint_red": bs.make_material("paint_red", (150, 30, 32), 0.35, 0.0), "paint_black": bs.make_material("paint_black", (35, 35, 36), 0.4, 0.0),
            "enamel_white": bs.make_material("enamel_white", (232, 229, 218), 0.12, 0.0), "slot_interior": bs.make_material("slot_interior", (8, 8, 8), 0.9, 0.0)}
    B = Parts()
    B.add("base", lathe(base_profile(), SIDES), "paint_black", bev=None)
    body = B.add("body", lathe(body_profile(), SIDES), "paint_red", bev=None)
    # the slot: through the front wall into the box (a pocket 100 deep), rounded corners R5
    sp = [(p[0], SLOT_Z + p[1]) for p in rrect(SLOT_W, SLOT_H, 5.0, 3)]
    Vs, Fs = prism_y(sp, 60.0, R_BODY + 45.0)
    # the door's joint groove: a ring 3 wide, 3 deep round the door's outline, cut in the body
    ha = math.degrees(math.asin(DOOR_W / 2.0 / R_BODY))
    def ring(w_extra):
        a = ha + math.degrees(w_extra / R_BODY)
        return arc_solid([(R_BODY - 3.0, DOOR_Z0 - w_extra), (R_BODY + 2.0, DOOR_Z0 - w_extra), (R_BODY + 2.0, DOOR_Z1 + w_extra), (R_BODY - 3.0, DOOR_Z1 + w_extra)], -a, a)
    Vo, Fo = ring(3.0)
    Vi, Fi = arc_solid([(R_BODY - 4.0, DOOR_Z0), (R_BODY + 3.0, DOOR_Z0), (R_BODY + 3.0, DOOR_Z1), (R_BODY - 4.0, DOOR_Z1)], -ha, ha)
    bs.bool_op(body, Vs, Fs, "DIFFERENCE")
    bs.bool_op(body, Vo, Fo, "DIFFERENCE")
    B2 = Parts()
    # the door: a cylindrical panel 1 mm proud (it fills the inside of the groove, 3 deep)
    Vd, Fd = arc_solid([(R_BODY - 3.0, DOOR_Z0), (R_BODY + 1.0, DOOR_Z0), (R_BODY + 1.0, DOOR_Z1), (R_BODY - 3.0, DOOR_Z1)], -ha, ha)
    B.add("door", (Vd, Fd), "paint_red", bev=None)
    # the hood over the slot: a curved lip wrapped round the front, 30 proud, its cheeks radial planes at +-47 degrees
    hood = [(R_BODY - 3.0, 1301.0), (R_BODY + 30.0, 1301.0), (R_BODY + 30.0, 1323.0), (R_BODY - 3.0, 1333.0)]   # 0.5 over the slot's ceiling (1300.5): no two faces in one plane
    B.add("hood", arc_solid(hood, -47.0, 47.0), "paint_red", bev=1.5)
    # the collection plate: a flat-faced frame (bezel 10, face plane 9 proud of the door at the axis), a 3 mm recess, the enamel plate in it
    y_face = R_BODY + 9.0
    outer = [(p[0], FRAME_Z + p[1]) for p in rrect(FRAME_W, FRAME_H, 6.0, 4)]
    fr = B.add("plate_frame", prism_y(outer, 150.0, y_face), "paint_red", bev=1.5)
    inner = [(p[0], FRAME_Z + p[1]) for p in rrect(FRAME_W - 20.0, FRAME_H - 20.0, 3.0, 3)]
    Vr, Fr = prism_y(inner, y_face - 3.0, y_face + 5.0)
    bs.bool_op(fr, Vr, Fr, "DIFFERENCE")
    B.add("plate", prism_y(inner, y_face - 3.4, y_face - 2.4), "enamel_white", bev=None)
    # the escutcheon: a round-cornered plate 36 across and 3 proud at the lock (x 90, z 818), with its keyhole 4 x 12; built on the front and turned about the axis to x 90
    ang = math.degrees(math.asin(LOCK_X / R_BODY))
    ew = math.degrees(18.0 / R_BODY)
    Ve, Fe = arc_solid([(R_BODY - 3.0, LOCK_Z - 18.0), (R_BODY + 3.0, LOCK_Z - 18.0), (R_BODY + 3.0, LOCK_Z + 18.0), (R_BODY - 3.0, LOCK_Z + 18.0)], ang - ew, ang + ew)
    es = B.add("escutcheon", (Ve, Fe), "paint_red", bev=1.0)
    kh = [(p[0], LOCK_Z + p[1]) for p in rrect(4.0, 12.0, 1.5, 2)]
    Vk, Fk = prism_y(kh, R_BODY - 1.0, R_BODY + 8.0)
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    Vk = np.array([(x * c + y * sn, -x * sn + y * c, z) for x, y, z in Vk])        # the front (+y) turned to the right, to x = R sin(ang)
    bs.bool_op(es, Vk, Fk, "DIFFERENCE")
    obs = bs.finish(B, mats, 0.0)
    return bs.write(obs, "pillar_box", 0.0, out_dir, npz_dir)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=ASSET_DIR)
    ap.add_argument("--npz-dir", default=NPZ_DIR)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    res = build(T, a.out_dir, a.npz_dir)
    print("pillar_box triangles", res["triangles"], "glb bytes", res["glb_bytes"])
    os.makedirs(a.npz_dir, exist_ok=True)
    json.dump({"pillar_box": res}, open(os.path.join(a.npz_dir, "parts.json"), "w"), indent=1)


if __name__ == "__main__":
    main()
