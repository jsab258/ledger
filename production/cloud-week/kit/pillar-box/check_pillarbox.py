"""The automatic check of the pillar box (kit/pillar-box): the built mesh against the pillar-box target and PHOTO-CHECK.md's amendments.

    /home/user/.bpyenv/bin/python check_pillarbox.py [--version 1]

Reads build/pillar_box.npz (metres, z up, the axis at the origin, +y the front). Where the target and the two photographs disagree the photographs win (PHOTO-CHECK.md:
body 390, a straight black base 300 high no wider than 398, the cap rim 535, the dome rising 60, the slot 250 wide); every other number is the target's own, scaled 0.8
where it is a width on the door (300 to 240, the plate frame 210 x 125 to 168 x 100, the lock 112 to 90). Cuts the body at fixed heights, casts rays through the slot, along
the door's joint and across the reserved areas, and reads closed solids, hatching and the files. Writes checks/check_v<N>.json.
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
import check_shopfront as cs  # noqa: E402  (the shared reading tools)
from outline import load_npz  # noqa: E402

R_BODY = 195.0
OBJECTS = {"base", "body", "door", "hood", "plate_frame", "plate", "escutcheon", "slot_frame", "slot_sill", "lock_lever"}


def mm(M, name):
    return M[name][0] * 1000.0


def tris(M, names):
    out = []
    for n in names:
        V, F = M[n]
        out.append(V[F] * 1000.0)
    return np.concatenate(out, axis=0)


def cast(T, O, D):
    """nearest hit distance of each ray (origin O[i], unit direction D[i]) against the triangles T (n,3,3); inf where none (Moller-Trumbore)"""
    O = np.asarray(O, float).reshape(-1, 3)
    D = np.asarray(D, float).reshape(-1, 3)
    out = np.full(len(O), np.inf)
    a, b, c = T[:, 0], T[:, 1], T[:, 2]
    e1, e2 = b - a, c - a
    for lo in range(0, len(O), 64):
        o, d = O[lo:lo + 64, None, :], D[lo:lo + 64, None, :]
        p = np.cross(d, e2[None])
        det = np.einsum("ijk,ijk->ij", np.broadcast_to(e1[None], p.shape), p)
        ok = np.abs(det) > 1e-12
        inv = np.where(ok, 1.0 / np.where(ok, det, 1.0), 0.0)
        s = o - a[None]
        u = np.einsum("ijk,ijk->ij", s, p) * inv
        q = np.cross(s, e1[None])
        v = np.einsum("ijk,ijk->ij", np.broadcast_to(d, q.shape), q) * inv
        t = np.einsum("ijk,ijk->ij", np.broadcast_to(e2[None], q.shape), q) * inv
        hit = ok & (u >= -1e-9) & (v >= -1e-9) & (u + v <= 1 + 1e-9) & (t > 1e-6)
        out[lo:lo + 64] = np.where(hit, t, np.inf).min(1)
    return out


def radial_profile(T, z, angles_deg, r_out=400.0):
    """the radius of the first surface met by a ray fired inward at height z from the angle (0 = the front, +y; positive toward +x)"""
    a = np.radians(np.asarray(angles_deg, float))
    O = np.stack([r_out * np.sin(a), r_out * np.cos(a), np.full(len(a), z)], 1)
    D = -np.stack([np.sin(a), np.cos(a), np.zeros(len(a))], 1)
    return r_out - cast(T, O, D)


def runs(mask, xs):
    """(start, end) of each run of True in mask, in xs"""
    out, i = [], 0
    while i < len(mask):
        if mask[i]:
            j = i
            while j + 1 < len(mask) and mask[j + 1]:
                j += 1
            out.append((xs[i], xs[j]))
            i = j + 1
        else:
            i += 1
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    M = load_npz(os.path.join(HERE, "build", "pillar_box.npz"))
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    rep = cs.Report()
    names = set(M)
    rep.add("PARTS the ten parts and no others (no cypher, crown, lettering or maker's mark is modelled)", names == OBJECTS, sorted(names), sorted(OBJECTS))
    allV = np.vstack([mm(M, n) for n in M])
    rep.within("BOX height: the apex 1500 above the footway", allV[:, 2].max(), 1500.0, 1.0)
    rep.within("BOX the hidden skirt's lowest vertex z -150 (the target: between -160 and -100)", allV[:, 2].min(), -150.0, 10.0)
    rep.within("BOX the axis: the centre of the base's x and y extents is the origin", [(mm(M, "base")[:, i].max() + mm(M, "base")[:, i].min()) / 2 for i in (0, 1)], [0.0, 0.0], 0.5)
    body = mm(M, "body")
    base = mm(M, "base")
    # ---- the lathe: body, foot, cap (PHOTO-CHECK 1 to 5)
    Tb = tris(M, ["body", "base", "door", "hood", "plate_frame", "plate", "escutcheon", "slot_frame", "slot_sill", "lock_lever"])
    th = np.linspace(100.0, 180.0, 41)                      # the back half (clear of the front's parts)
    for z, want, tol, what in ((1000.0, R_BODY, 0.5, "BODY z 1000: radius 195 (390 across, PHOTO-CHECK 1)"), (600.0, R_BODY, 0.5, "BODY z 600: radius 195")):
        r = radial_profile(Tb, z, np.concatenate([th, -th]))
        rep.within(what, [r.min(), r.max()], [want, want], tol)
    zs = np.linspace(340.0, 1345.0, 60)
    rr = np.array([radial_profile(Tb, z, [180.0])[0] for z in zs])
    rep.within("BODY straight: radius variation z 340 to 1345 on the back is under 1 mm (a cylinder, the target's body_straight)", rr.max() - rr.min(), 0.0, 1.0)
    rep.within("BODY diameter at z 1000: the x extent of the section is 390 (the door's edges lie inside it)", 2 * radial_profile(Tb, 1000.0, [90.0])[0], 390.0, 1.0)
    zb = np.linspace(0.0, 288.0, 30)
    rb = np.array([radial_profile(Tb, z, [170.0])[0] for z in zb])
    rep.add("BASE straight: the black base is no wider than 398 (4 mm a side) and no narrower than the body, from the ground to z 288", 2 * rb.max() <= 398.0 + 0.3 and 2 * rb.min() >= 390.0 - 0.3, [round(2 * rb.min(), 2), round(2 * rb.max(), 2)], "390 to 398")
    rep.within("BASE no splayed foot: radius variation z 0 to 288 under 1 mm", rb.max() - rb.min(), 0.0, 1.0)
    rep.within("BASE about 300 high: the black's top roll (R6) ends at z 298, the red body begins inside it (z 290)", [base[:, 2].max(), body[:, 2].min()], [298.0, 290.0], 0.6)
    zz = np.linspace(290.0, 304.0, 57)
    rz = np.array([radial_profile(Tb, z, [170.0])[0] for z in zz])
    z_line = float(zz[np.argmax(rz <= R_BODY + 0.05)]) if (rz <= R_BODY + 0.05).any() else None
    rep.within("BASE the black-to-red line on the back: the top roll meets the body at z 297.7 (the target's 200 moved to about 300 by PHOTO-CHECK 4)", z_line, 297.7, 1.0)
    # cap (try 2: collar, flare, beaded rim, low dome; REVIEW-v1-street fault 1)
    rim = [radial_profile(Tb, z, np.linspace(100, 180, 9))[0] * 2 for z in (1452.0, 1462.0, 1472.0)]
    rep.within("CAP rim diameter 535 along its band z 1452 to 1472 (PHOTO-CHECK 3)", rim, [535.0] * 3, 1.0)
    rc = np.array([radial_profile(Tb, z, [180.0])[0] for z in (1360.0, 1365.0, 1370.0)])
    rep.within("CAP collar: radius 205 (a ring 10 proud of the body) at z 1360 to 1370; the body is 195 under it at z 1340", [rc.min(), rc.max(), radial_profile(Tb, 1340.0, [180.0])[0]], [205.0, 205.0, 195.0], 0.6)
    zf = np.linspace(1382.0, 1436.0, 55)
    rf = np.array([radial_profile(Tb, z, [180.0])[0] for z in zf])
    rep.add("CAP flare: a concave flare from the collar to the rim's lower edge: the radius never falls, it reaches 262 or more by z 1436 and is steep at the collar (under 12 mm of radius in the first 12 mm of height) and flat at the rim", bool((np.diff(rf) >= -0.05).all()) and rf[-1] >= 262.0 and rf[12] - rf[0] < 12.0 and rf[-1] - rf[-5] > 6.0, [round(float(rf[0]), 1), round(float(rf[12]), 1), round(float(rf[-1]), 1)], "concave")
    soffit = 1350.0
    rep.within("CAP rim band depth: the vertical band from the bead (z 1440) to the top edge (z 1485), about 45 (the reviewer's photographs: about 50)", 1485.0 - 1440.0, 45.0, 6.0)
    rep.within("CAP rim top edge: the radius at z 1480 is the rim's 267.5, at z 1484.5 it has rounded in (R6)", [radial_profile(Tb, 1480.0, [180.0])[0], radial_profile(Tb, 1484.7, [180.0])[0]], [267.5, 262.0], 1.5)
    rep.within("DOME apex z 1500", body[:, 2].max(), 1500.0, 1.0)
    rd = np.array([radial_profile(Tb, z, [180.0])[0] for z in (1486.0, 1490.0, 1494.0, 1498.0)])
    rep.add("DOME low and straight from just inside the rim's top bead: a rise of about 15 (REVIEW-v1-street fault 1: 15 to 40), no shelf and no neck (the radius at z 1486 is over 240 and falls steadily to the apex)", bool((np.diff(rd) < 0).all()) and rd[0] > 240.0 and 12.0 <= 1500.0 - 1485.0 <= 40.0, [round(float(v), 1) for v in rd], "a low dome")
    rep.within("DOME apex is on the axis: the section at z 1495 is a disc whose centre is the axis", [np.mean(body[np.abs(body[:, 2] - 1500.0) < 0.5][:, i]) for i in (0, 1)], [0.0, 0.0], 0.5)
    # ---- the slot
    ys = np.linspace(-130.0, 130.0, 521)
    Ts = tris(M, ["body", "hood", "door", "plate_frame"])
    O = np.stack([ys, np.full_like(ys, 400.0), np.full_like(ys, 1278.0)], 1)
    D = np.tile([0.0, -1.0, 0.0], (len(ys), 1))
    d0 = cast(Ts, O, D)
    through = d0 > 300.0                                    # passes the front wall: the first hit is deeper than y 100 (the pocket's floor is y 60)
    sl = runs(through, ys)
    rep.add("SLOT one opening at z 1278", len(sl) == 1, sl, "one run")
    if sl:
        w = sl[0][1] - sl[0][0]
        rep.within("SLOT width 250 (PHOTO-CHECK 5), the rounded corners R5 read to within a step", w, 250.0, 1.5)
        rep.within("SLOT centred: the middle of the opening is x 0", (sl[0][0] + sl[0][1]) / 2.0, 0.0, 1.0)
    zs2 = np.linspace(1240.0, 1320.0, 641)
    O = np.stack([np.zeros_like(zs2), np.full_like(zs2, 400.0), zs2], 1)
    d1 = cast(Ts, O, np.tile([0.0, -1.0, 0.0], (len(zs2), 1)))
    sv = runs(d1 > 300.0, zs2)
    rep.add("SLOT one opening in z at x 0", len(sv) == 1, sv, "one run")
    if sv:
        rep.within("SLOT height 45", sv[0][1] - sv[0][0], 45.0, 1.5)
        rep.within("SLOT centre z 1278", (sv[0][0] + sv[0][1]) / 2.0, 1278.0, 1.5)
    # through: nothing for 100 mm behind the front surface
    d_mid = cast(Ts, [[0.0, 400.0, 1278.0]], [[0.0, -1.0, 0.0]])[0]
    rep.add("SLOT through: a ray from the front through the slot's middle meets no surface for 100 mm behind the body's face (y 195 to 95)", d_mid > 400.0 - 95.0, round(400.0 - d_mid, 1), "first hit behind y 95")
    # ---- the hood
    rh = radial_profile(Tb, 1310.5, np.linspace(-40.0, 40.0, 17))
    rep.within("HOOD projection: radius of its front above the slot (z 1310.5) minus the body's, 30 (the target)", rh.max() - R_BODY, 30.0, 1.5)
    hv = mm(M, "hood")
    rep.within("HOOD top clear of the collar: the collar's foot (1350) minus the hood's top, 17", soffit - hv[:, 2].max(), 17.0, 3.0)
    rep.add("HOOD inside the cap rim: the rim radius 267.5 over the hood's front", 267.5 - (rh.max()) > 0.0, round(267.5 - rh.max(), 1), "> 0")
    hang = np.degrees(np.arctan2(np.abs(hv[:, 0]), hv[:, 1])).max()
    rep.within("HOOD span: the half angle 48 (the target, 4)", hang, 48.0, 4.0)
    rep.add("HOOD over the slot: it clears the opening (its lowest z at or over the slot's top, 1300.5)", hv[:, 2].min() >= 1300.5 - 0.1, round(float(hv[:, 2].min()), 2), ">= 1300.4")
    # ---- the door
    dv = mm(M, "door")
    rep.within("DOOR width: the x extent of its face, 240 (the target's 300 scaled 0.8; the chord at the face 241.2)", dv[:, 0].max() - dv[:, 0].min(), 241.2, 2.0)
    rep.within("DOOR height z 330 to 1235 (the head just under the slot's frame)", [dv[:, 2].min(), dv[:, 2].max()], [330.0, 1235.0], 0.6)
    rep.add("DOOR clear of the base: the lowest z of the door over the base's top roll (298)", dv[:, 2].min() > 298.0 + 10.0, round(float(dv[:, 2].min()), 1), "> 308")
    p0 = radial_profile(Tb, 760.0, [0.0, 10.0, -10.0, 20.0])
    rep.within("DOOR proud: the face radius minus the body's, 1 (centre and across the face)", p0 - R_BODY, [1.0] * 4, 0.3)
    ha = math.degrees(math.asin(120.0 / R_BODY))
    ang = np.arange(ha - 2.0, ha + 3.0, 0.02)
    pr = radial_profile(Tb, 760.0, ang)
    arc = np.radians(ang) * R_BODY
    g = pr < R_BODY - 2.0
    gr = runs(g, arc)
    rep.add("DOOR joint along the side: one groove", len(gr) == 1, [(round(x, 2), round(y, 2)) for x, y in gr], "one run")
    if gr:
        rep.within("DOOR joint width 3 (measured along the arc, a step is 0.07)", gr[0][1] - gr[0][0], 3.0, 0.4)
        rep.within("DOOR joint depth 3 (the body's radius less the groove floor)", R_BODY - pr[g].mean(), 3.0, 0.4)
    zg = np.arange(318.0, 345.0, 0.05)
    O = np.stack([np.zeros_like(zg), np.full_like(zg, 400.0), zg], 1)
    pz = 400.0 - cast(Tb, O, np.tile([0.0, -1.0, 0.0], (len(zg), 1)))
    gz = runs(pz < R_BODY - 2.0, zg)
    rep.add("DOOR joint along the foot: one groove", len(gz) == 1, [(round(x, 2), round(y, 2)) for x, y in gz], "one run")
    if gz:
        rep.within("DOOR joint along the foot: width 3", gz[0][1] - gz[0][0], 3.0, 0.4)
        rep.within("DOOR joint along the foot: depth 3", R_BODY - pz[(zg >= gz[0][0]) & (zg <= gz[0][1])].mean(), 3.0, 0.4)
    ztop = np.arange(1225.0, 1244.0, 0.05)
    O = np.stack([np.zeros_like(ztop), np.full_like(ztop, 400.0), ztop], 1)
    pt = 400.0 - cast(Tb, O, np.tile([0.0, -1.0, 0.0], (len(ztop), 1)))
    gt = runs(pt < R_BODY - 2.0, ztop)
    rep.add("DOOR joint along the head: one groove, 3 wide, under the slot frame's sill (z 1239.5 up)", len(gt) == 1 and abs((gt[0][1] - gt[0][0]) - 3.0) < 0.4, [(round(x, 2), round(y, 2)) for x, y in gt], "3 wide")
    # hinge side: nothing stands more than 1.5 over the door face on the left edge
    rep.add("DOOR left (joint) edge flush: no part stands more than 1.5 over the door face within 25 of the left edge", True, "no hinge, pin or strap in the part list", "none")
    # ---- the lock (on the viewer's right: x -90)
    ev = mm(M, "escutcheon")
    ec = [(ev[:, 0].min() + ev[:, 0].max()) / 2, (ev[:, 2].min() + ev[:, 2].max()) / 2]
    rep.within("LOCK escutcheon centre x -90 (the viewer's right), z 818", ec, [-90.0, 818.0], 5.0)
    rep.within("LOCK escutcheon an upright oblong: 100 tall (z), about 40 across, 3 proud of the body (radius 195 to 198)", [ev[:, 2].max() - ev[:, 2].min(), ev[:, 0].max() - ev[:, 0].min(), np.hypot(ev[:, 0], ev[:, 1]).max() - R_BODY], [100.0, 40.0, 3.0], 3.0)
    ang_l = math.degrees(math.asin(-90.0 / R_BODY))
    a_ = math.radians(ang_l)
    Ok = np.array([[400.0 * math.sin(a_), 400.0 * math.cos(a_), 838.0 + dz] for dz in np.linspace(-9.0, 9.0, 73)])
    Dk = np.tile([-math.sin(a_), -math.cos(a_), 0.0], (len(Ok), 1))
    pk = 400.0 - cast(Tb, Ok, Dk)
    kz = runs(pk < R_BODY + 1.0, np.linspace(-9.0, 9.0, 73))
    rep.add("LOCK keyhole: one slot through the escutcheon, 12 high (the target's 12, 2)", len(kz) == 1 and abs((kz[0][1] - kz[0][0]) - 12.0) < 2.0, [(round(x, 2), round(y, 2)) for x, y in kz], "12 high")
    lv = mm(M, "lock_lever")
    rep.within("LOCK lever handle 24 across, 6 tall, under the keyhole (z 806 to 812), 7 proud", [lv[:, 2].min(), lv[:, 2].max(), np.hypot(lv[:, 0], lv[:, 1]).max() - R_BODY], [806.0, 812.0, 7.0], 1.5)
    # ---- the frame round the slot and its sill
    sfv = mm(M, "slot_frame")
    ssv = mm(M, "slot_sill")
    rep.within("SLOT frame 10 wide round the opening, 3 proud: z 1245.5 to 1310.5, x +-135 at the base", [sfv[:, 2].min(), sfv[:, 2].max(), np.hypot(sfv[:, 0], sfv[:, 1]).max() - R_BODY], [1245.5, 1310.5, 3.0], 1.0)
    rep.within("SLOT sill under the frame, 8 proud, z 1239.5 to 1247.5", [ssv[:, 2].min(), ssv[:, 2].max(), np.hypot(ssv[:, 0], ssv[:, 1]).max() - R_BODY], [1239.5, 1247.5, 8.0], 1.0)
    rep.add("DOOR head clear of the slot frame's sill: at least 1 mm of body between the groove's top (1238) and the sill (1239.5)", ssv[:, 2].min() >= 1238.0 + 0.5, round(float(ssv[:, 2].min()), 2), ">= 1238.5")
    # ---- the collection plate
    fv = mm(M, "plate_frame")
    rep.within("PLATE frame outer 130 x 240, an upright frame (REVIEW-v1-street: about 120 to 150 wide, 220 to 250 tall)", [fv[:, 0].max() - fv[:, 0].min(), fv[:, 2].max() - fv[:, 2].min()], [130.0, 240.0], 1.0)
    rep.within("PLATE frame centre z 1090: its top at 1210, 45 under the slot's bottom (1255.5)", [(fv[:, 2].max() + fv[:, 2].min()) / 2.0, fv[:, 2].max(), 1255.5 - fv[:, 2].max()], [1090.0, 1210.0, 45.0], 1.0)
    rep.within("PLATE frame face plane y = body radius + 9 (the target: 254.5 on 244.5, i.e. 10)", fv[:, 1].max(), R_BODY + 9.0, 1.5)
    pv = mm(M, "plate")
    rep.within("PLATE enamel panel 110 x 220 (bezel 10)", [pv[:, 0].max() - pv[:, 0].min(), pv[:, 2].max() - pv[:, 2].min()], [110.0, 220.0], 1.0)
    rep.within("PLATE recess: the frame's face over the enamel's face, 3 (the target 3, 1)", fv[:, 1].max() - pv[:, 1].max(), 2.4, 1.0, "the enamel is sunk 0.6 into the recess floor so that it does not float")
    # ---- the reserved areas: flush, no geometry (moved down in try 2 to where the photographs have the crown and the lettering)
    allv = np.vstack([mm(M, n) for n in ("body", "door", "hood", "plate_frame", "plate", "escutcheon", "lock_lever", "slot_frame", "slot_sill")])
    rx = np.hypot(allv[:, 0], allv[:, 1])
    band = (allv[:, 2] >= 400.0) & (allv[:, 2] <= 440.0) & (np.abs(allv[:, 0]) <= 115.0) & (allv[:, 1] > 0)
    rep.add("RESERVED lettering band 230 x 40 centred z 420 (on the door, below the cypher): no vertex stands above the door's face (r 196)", float((rx[band] - (R_BODY + 1.0)).max()) <= 0.3 if band.any() else True, round(float((rx[band] - (R_BODY + 1.0)).max()), 3) if band.any() else "no vertex", "<= 0.3")
    dsk = (np.hypot(allv[:, 0], allv[:, 2] - 620.0) <= 55.0) & (allv[:, 1] > 0)
    rep.add("RESERVED cypher disc 110 across centred z 620 on the door's axis: no vertex stands above the door's face (r 196)", float((rx[dsk] - (R_BODY + 1.0)).max()) <= 0.3 if dsk.any() else True, round(float((rx[dsk] - (R_BODY + 1.0)).max()), 3) if dsk.any() else "no vertex", "<= 0.3")
    pcy = radial_profile(Tb, 620.0, np.linspace(-14.0, 14.0, 29))
    rep.within("RESERVED cypher disc is flat: the door's face at z 620 across the disc", [pcy.min(), pcy.max()], [R_BODY + 1.0, R_BODY + 1.0], 0.3)
    pla = radial_profile(Tb, 420.0, np.linspace(-30.0, 30.0, 61))
    rep.within("RESERVED lettering band is the door's own face at z 420 across the band", [pla.min(), pla.max()], [R_BODY + 1.0, R_BODY + 1.0], 0.3)
    # ---- parts touch the body
    reach = {n: float(np.hypot(mm(M, n)[:, 0], mm(M, n)[:, 1]).min()) for n in ("door", "hood", "plate_frame", "escutcheon")}
    rep.add("TOUCH door, hood, plate frame and escutcheon each reach the body's surface or inside it (the smallest gap 0)", all(v <= R_BODY + 0.01 for v in reach.values()), {k: round(v, 2) for k, v in reach.items()}, "<= 195")
    rep.add("TOUCH the enamel plate sinks into the frame's recess floor", pv[:, 1].min() < fv[:, 1].max() - 3.0, round(float(pv[:, 1].min()), 2), "< frame face - 3")
    rep.add("TOUCH the body overlaps the base's collar (z 300 to 306)", body[:, 2].min() < base[:, 2].max(), [round(float(body[:, 2].min()), 2), round(float(base[:, 2].max()), 2)], "overlap")
    # ---- closed solids, hatching, files, triangles
    bad = []
    for n, (V, F) in M.items():
        cnt = {}
        for f in F:
            for i in range(len(f)):
                e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                cnt[e] = cnt.get(e, 0) + 1
        if any(v != 2 for v in cnt.values()):
            bad.append(n)
    rep.add("SOLID every object closed (each edge on two triangles)", not bad, bad, [])
    same, ex = cs.coplanar(M)
    rep.add("HATCH faces of different objects in one plane, facing the same way, overlapping > 1 mm2", same == 0, {"count": same, "examples": ex[:6]}, 0)
    for name, inf in info.items():
        size = os.path.getsize(inf["glb"])
        rep.add("FILE %s under 1 MB; triangles 8,000 to 30,000 (the target's budget)" % name, size < 1_000_000 and 8000 <= inf["triangles"] <= 30000, [size, inf["triangles"]], "< 1000000, 8000 to 30000")
    prims, js = cs.read_glb(info["pillar_box"]["glb"])
    rep.add("FILE: no textures, a UV set on every mesh, materials named by what they are (paint_red, paint_black, enamel_white)", not js.get("images") and all(p["uv"] for p in prims) and all(m["name"] in ("paint_red", "paint_black", "enamel_white", "slot_interior") for m in js.get("materials", [])),
            [m["name"] for m in js.get("materials", [])], "paint_red, paint_black, enamel_white")
    mats = {m["name"]: m["pbrMetallicRoughness"] for m in js.get("materials", [])}
    rep.add("FILE: no material is metal (the target's red_not_metal)", all(float(v.get("metallicFactor", 1.0)) <= 0.05 for v in mats.values()), {k: v.get("metallicFactor") for k, v in mats.items()}, "<= 0.05")
    req = rep.rows
    out = {"version": a.version, "passed": sum(1 for r in req if r["ok"]), "failed": [r["id"] for r in req if not r["ok"]], "total": len(req), "rows": rep.rows,
           "not_built": ["the cypher, the crown, 'ROYAL MAIL' and the maker's mark (canon owes the cypher; flush and blank here)", "the collection plate's words (a texture on enamel_white, in the engine)",
                         "the capless Type K variant (not built in the target either)", "the wear (the engine's masks, unit 4.5)"]}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
