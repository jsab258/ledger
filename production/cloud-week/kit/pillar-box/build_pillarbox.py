"""Quay Street's pillar box (pillar-box target; cloud week 42, unit 3.6), built by script, to the proportions of the two dated photographs.

    /home/user/.bpyenv/bin/python build_pillarbox.py [--out-dir DIR] [--npz-dir DIR]

Reads production/cloud-week/targets/pillar-box/target.json for what the target fixes (the colours, the slot's height and centre, the door's 1 mm and its 3 x 3 groove, the
plate frame's bezel and recess, the 1500 total height, no cypher, no lettering, no maker's mark) and builds it with PHOTO-CHECK.md's amendments, which win over the target's
body, foot and cap numbers (two Geograph photographs, 2009 and 2012; DECISIONS 11 Oct 21:55): body 390 across, a straight black base 300 high no wider than 398, the cap
rim 535 across and 60 deep, the dome rising 15, the slot 250 wide. The door is the target's 300 wide; the plate frame and the escutcheon are scaled to the narrower body.

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

R_BODY, R_BASE, Z_BASE = 195.0, 199.0, 290.0                  # PHOTO-CHECK: body 390, a straight black base about 300 high at most 4 wider; the body starts inside the base's roll
Z_ROLL = 298.0                                                # the base's top roll (R6) ends here: the black-to-red line reads at about 297.7
R_RIM = 267.5                                                 # the cap rim 535 across
# try 2 after REVIEW-v1-street (fault 1), measured on five Geograph photographs, as fractions of the 1500: collar 1350 to 1380 (a ring a little proud of the body, just over the
# slot's hood), a deep concave flare from the collar to the rim's lower edge at 1425 (REVIEW-v2-close point 2: the rim band as deep as the flare, 60), the rim band 1425 to 1485
# with a bead on its lower edge and an R8 round on its top edge, then a low dome (15 rise) straight from just inside the rim's top bead: no shelf, no neck
Z_COLLAR0, Z_COLLAR1, R_COLLAR = 1350.0, 1380.0, 205.0
Z_RIM0, Z_RIM1, Z_TOP = 1425.0, 1485.0, 1500.0
DOME_RISE = Z_TOP - Z_RIM1
SLOT_W, SLOT_H, SLOT_Z = 250.0, 45.0, 1278.0
HOOD_P, HOOD_ZTOP = 40.0, 1347.0                              # the deep hood: 40 proud, its face 1301 to 1347 (REVIEW-v2-close point 1)
TAB_Z, TAB_W, TAB_H, TAB_WW, TAB_WH = 1324.0, 55.0, 38.0, 40.0, 28.0   # the tablet's frame and its window
DOOR_W, DOOR_Z0, DOOR_Z1 = 300.0, 330.0, 1224.0               # the target's 300 (REVIEW-v2-close point 4: the photographs' door is about 0.8 of the seen width); the head rises to just under the slot's frame (REVIEW-v1-street fault 2; the frame's borders widened to 22 after REVIEW-v2-street)
SIDES = 96                                                    # the lathe's sides (the target asks for 8,000 to 30,000 triangles)
LOCK_X, LOCK_Z, GRIP_Z = -90.0, 818.0, 745.0                                              # on the viewer's right: with +y the front and z up, the viewer's right is -x (the target's frame line is mirrored)
FRAME_W, FRAME_H, FRAME_Z = 130.0, 240.0, 1090.0              # an upright frame under the slot, its top at 1210 (REVIEW-v1-street fault 2)
CYPHER_Z, LETTER_Z, LETTER_W = 620.0, 420.0, 230.0            # the reserved flush areas, moved down to where the photographs have the crown and the lettering


def body_profile():
    """(r, z) from the foot of the red body to the apex: the body to the collar, the collar, the deep concave flare out to the rim's lower bead, the vertical rim with its
    rounded top, the low dome"""
    pts = [(0.0, Z_BASE), (R_BODY, Z_BASE), (R_BODY, Z_COLLAR0), (R_COLLAR, Z_COLLAR0), (R_COLLAR, Z_COLLAR1), (R_COLLAR - 5.0, Z_COLLAR1)]
    i_col0, i_col1 = 3, 4
    r0 = R_COLLAR - 5.0
    for k in range(1, 13):                                    # the flare: tangent to the vertical at the collar, turning to the horizontal at the rim's lower edge
        a = math.radians(90.0 * k / 12)
        pts.append((r0 + (R_RIM - 4.0 - r0) * (1 - math.cos(a)), Z_COLLAR1 + (Z_RIM0 - 4.0 - Z_COLLAR1) * math.sin(a)))
    for k in range(1, 5):                                     # the bead on the rim's lower edge, R4
        a = math.radians(-90.0 + 90.0 * k / 4)
        pts.append((R_RIM - 4.0 + 4.0 * math.cos(a), Z_RIM0 + 4.0 * math.sin(a)))
    pts += [(R_RIM, Z_RIM1 - 8.0)]
    for k in range(1, 7):                                     # the rim's top edge, R8 (REVIEW-v2-close point 2)
        a = math.radians(90.0 * k / 6)
        pts.append((R_RIM - 8.0 + 8.0 * math.cos(a), Z_RIM1 - 8.0 + 8.0 * math.sin(a)))
    r1 = R_RIM - 8.0
    Rd = (r1 ** 2 + DOME_RISE ** 2) / (2 * DOME_RISE)
    for k in range(1, 17):
        r = r1 * (1 - k / 16.0)
        pts.append((r, Z_TOP - (Rd - math.sqrt(max(Rd * Rd - r * r, 0.0)))))
    return fillet(pts, {i_col0: 2.5, i_col1: 2.5})


def base_profile():
    """the black base: straight, 199 across, to its top roll (R6), which meets the body at about z 297.7"""
    pts = [(0.0, -150.0), (R_BASE, -150.0), (R_BASE, Z_ROLL - 6.0)]
    for k in range(1, 7):
        a = math.radians(90.0 * k / 6)
        pts.append((R_BASE - 6.0 + 6.0 * math.cos(a), Z_ROLL - 6.0 + 6.0 * math.sin(a)))
    pts.append((0.0, Z_ROLL))
    return pts


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
    # the door: a cylindrical panel 1 mm proud (it fills the inside of the groove, 3 deep)
    Vd, Fd = arc_solid([(R_BODY - 3.0, DOOR_Z0), (R_BODY + 1.0, DOOR_Z0), (R_BODY + 1.0, DOOR_Z1), (R_BODY - 3.0, DOOR_Z1)], -ha, ha)
    B.add("door", (Vd, Fd), "paint_red", bev=None)
    # the hood over the slot: the Elizabeth II pattern of REVIEW-v2-close point 1 (G1, P1, P2: a deep box about 46 high in its face and 40 proud, its top under the collar, the tablet
    # set in its face), wrapped round the front, its cheeks radial planes at +-50 degrees; the roof slopes up to the body at 1351
    hood = [(R_BODY - 3.0, 1301.0), (R_BODY + HOOD_P, 1301.0), (R_BODY + HOOD_P, HOOD_ZTOP), (R_BODY - 3.0, 1351.0)]   # 0.5 over the slot's ceiling (1300.5): no two faces in one plane
    B.add("hood", arc_solid(hood, -50.0, 50.0), "paint_red", bev=1.5)
    # the tablet: a frame 55 x 38 standing 3 proud of the hood's face at its middle round a window 40 x 28 through it to the hood's own face (the cast words are the engine's texture:
    # the window is a flush reserved area)
    tf = B.add("tablet_frame", prism_y([(p[0], TAB_Z + p[1]) for p in rrect(TAB_W, TAB_H, 4.0, 3)], R_BODY - 10.0, R_BODY + HOOD_P + 3.0), "paint_red", bev=1.0)
    Vtw, Ftw = prism_y([(p[0], TAB_Z + p[1]) for p in rrect(TAB_WW, TAB_WH, 2.5, 3)], R_BODY - 12.0, R_BODY + HOOD_P + 8.0)
    bs.bool_op(tf, Vtw, Ftw, "DIFFERENCE")
    # the frame round the slot: borders 22 wide, 12 proud (REVIEW-v2-street narrow point 3: the photographs' raised oblong about 300 x 110 under a heavy hood), wrapped on the body, the slot
    # cut through it; its bottom border is the sill
    bw_ = 22.0
    af = math.degrees(math.asin((SLOT_W / 2.0 + bw_) / R_BODY))
    z0f, z1f = SLOT_Z - SLOT_H / 2.0 - bw_, SLOT_Z + SLOT_H / 2.0 + bw_
    Vfr, Ffr = arc_solid([(R_BODY - 2.5, z0f), (R_BODY + 12.0, z0f), (R_BODY + 12.0, z1f), (R_BODY - 2.5, z1f)], -af, af)
    sf = B.add("slot_frame", (Vfr, Ffr), "paint_red", bev=1.5)
    spf = [(p[0], SLOT_Z + p[1]) for p in rrect(SLOT_W + 2.0, SLOT_H + 2.0, 6.0, 3)]                      # 1 mm larger all round than the body's slot: no two faces in one plane
    Vsf, Fsf = prism_y(spf, 60.0, R_BODY + 45.0)
    bs.bool_op(sf, Vsf, Fsf, "DIFFERENCE")
    # the collection plate: an upright flat-faced frame 130 x 240 (bezel 10, face plane 9 proud of the door at the axis), a 3 mm recess, the enamel plate in it
    y_face = R_BODY + 9.0
    outer = [(p[0], FRAME_Z + p[1]) for p in rrect(FRAME_W, FRAME_H, 6.0, 4)]
    fr = B.add("plate_frame", prism_y(outer, 150.0, y_face), "paint_red", bev=1.5)
    inner = [(p[0], FRAME_Z + p[1]) for p in rrect(FRAME_W - 20.0, FRAME_H - 20.0, 3.0, 3)]
    Vr, Fr = prism_y(inner, y_face - 3.0, y_face + 5.0)
    bs.bool_op(fr, Vr, Fr, "DIFFERENCE")
    B.add("plate", prism_y(inner, y_face - 3.4, y_face - 2.4), "enamel_white", bev=None)
    # the lock, on the viewer's right (x -90, z 818), REVIEW-v2-close point 3: an upright oblong escutcheon 45 x 70, 9 proud, with a true keyhole 10 x 20 (a round top and a slot) cut
    # through it, and the door's grip as its own part below it (70 x 25, 25 proud); built on the front and turned about the axis
    ang = math.degrees(math.asin(LOCK_X / R_BODY))
    ew = math.degrees(22.5 / R_BODY)
    Ve, Fe = arc_solid([(R_BODY - 4.0, LOCK_Z - 35.0), (R_BODY + 9.0, LOCK_Z - 35.0), (R_BODY + 9.0, LOCK_Z + 35.0), (R_BODY - 4.0, LOCK_Z + 35.0)], ang - ew, ang + ew)
    es = B.add("escutcheon", (Ve, Fe), "paint_red", bev=1.0)
    c, sn = math.cos(math.radians(ang)), math.sin(math.radians(ang))
    def turned(V):
        return np.array([(x * c + y * sn, -x * sn + y * c, z) for x, y, z in V])        # the front (+y) turned to the viewer's right, to x = R sin(ang)
    cz = LOCK_Z + 10.0
    kh_round = [(5.0 * math.cos(2 * math.pi * i / 24), cz + 5.0 * math.sin(2 * math.pi * i / 24)) for i in range(24)]
    kh_slot = [(p[0], LOCK_Z + 2.5 + p[1]) for p in rrect(4.0, 15.0, 1.0, 2)]               # z LOCK_Z -5 to +10: under the round top, which ends at +15
    for kh in (kh_round, kh_slot):
        Vk, Fk = prism_y(kh, R_BODY - 1.0, R_BODY + 14.0)
        bs.bool_op(es, turned(Vk), Fk, "DIFFERENCE")
    lw = math.degrees(35.0 / R_BODY)
    B.add("lock_grip", arc_solid([(R_BODY - 4.5, GRIP_Z - 12.5), (R_BODY + 25.0, GRIP_Z - 12.5), (R_BODY + 25.0, GRIP_Z + 12.5), (R_BODY - 4.5, GRIP_Z + 12.5)], ang - lw, ang + lw), "paint_red", bev=5.0)
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
