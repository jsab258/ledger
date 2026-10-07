"""Turn the flat pattern into a garment ready for Blender's cloth: pieces meshed,
mirrored for both sides, wrapped round Ron's body at their drafted positions, the
lapel turned over its roll line and the collar's fall over its stand, every seam
listed as vertex pairs, the buttons fastened, canvas stiffness painted.

    python garment.py ron [version]   -> F:/LedgerTools/lab/jacket/garment_<version>.npz (+ .json notes)
"""
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from panel_mesh import mesh_panel  # noqa: E402
from wrap import fold_2d  # noqa: E402
sys.path.insert(0, HERE)
import shell  # noqa: E402

OUT = r"F:/LedgerTools/lab/jacket"
IN = 0.0254
SPACING_IN = 0.6

# Ron's body, posed arms-down (pose_body.py): landmarks in metres
NAPE_Z = 1.622            # C7 on the full body (head on): the back of the neck's base
NECKSIDE_Z = 1.655        # the base of the neck at its side, under the coat's neck point
# sewn in MetaHuman's A-pose (arms clear of the sides); the arms are let down during the run
SHOULDER_JOINT = {"R": np.array([-0.203, 0.02, 1.55]), "L": np.array([0.203, 0.02, 1.55])}
ELBOW = {"R": np.array([-0.387, 0.012, 1.308]), "L": np.array([0.387, 0.012, 1.308])}


def body_sections(path=os.path.join(OUT, "ronfull_apose.npz")):
    """Torso half-widths (x) and depths (y) and centre by height, from the A-pose body
    (arms clear of the torso), for wrapping. Returns a function z -> (cx, cy, a, b)."""
    d = np.load(path)
    V = d["LOD0_V"]
    zs = np.arange(0.70, 1.66, 0.02)
    rows = []
    for z in zs:
        xmax = 0.34 if z > 1.46 else 0.26
        S = V[(np.abs(V[:, 2] - z) < 0.012) & (np.abs(V[:, 0]) < xmax)]
        if len(S) < 8:
            rows.append(rows[-1] if rows else (0, 0, 0.15, 0.12))
            continue
        x0, x1, y0, y1 = S[:, 0].min(), S[:, 0].max(), S[:, 1].min(), S[:, 1].max()
        rows.append(((x0 + x1) / 2, (y0 + y1) / 2, (x1 - x0) / 2, (y1 - y0) / 2))
    rows = np.array(rows)

    def f(z):
        return tuple(np.interp(z, zs, rows[:, i]) for i in range(4))
    return f


def ring_param(V2, ring, stretch):
    a, b = stretch
    idx = list(range(a, b + 1))
    return idx


def place_torso(V2, side, x_cb, x_cf, z_top, sect, gap):
    """Draft (x from CB to CF, y down, inches) -> 3D. Angle by the fraction of the half girth,
    radius from the body's section at that height plus a gap."""
    frac = (V2[:, 0] - x_cb) / (x_cf - x_cb)
    th = math.pi / 2 + frac * math.pi            # right side: back (+y) -> -x -> front (-y)
    if side == "L":
        th = math.pi - th                        # mirror: back -> +x -> front
    z = z_top - V2[:, 1] * IN
    P = np.zeros((len(V2), 3))
    for i, (t, zz) in enumerate(zip(th, z)):
        cx, cy, a, b = sect(zz)
        g = gap[i] if np.ndim(gap) else gap
        P[i] = (cx + (a + g) * math.cos(t), cy + (b + g) * math.sin(t), zz)
    return P


def nearest_on_polyline(Q, pts):
    """For each point, (parameter 0..1 by arc length, distance) of the nearest point on polyline Q."""
    Q = np.asarray(Q, float)
    seg = Q[1:] - Q[:-1]
    L = np.linalg.norm(seg, axis=1)
    cs = np.concatenate([[0], np.cumsum(L)])
    out_t, out_d = [], []
    for p in pts:
        a = p - Q[:-1]
        t = np.clip(np.einsum("ij,ij->i", a, seg) / np.maximum(L ** 2, 1e-12), 0, 1)
        proj = Q[:-1] + seg * t[:, None]
        dd = np.linalg.norm(proj - p, axis=1)
        k = int(np.argmin(dd))
        out_t.append((cs[k] + t[k] * L[k]) / cs[-1])
        out_d.append(dd[k])
    return np.array(out_t), np.array(out_d)


def top_band(V2, V3, edge_flat, edge3d, band_in):
    """Lay the band of a piece under its top edge over the shoulder: each vertex within band_in of
    the edge goes toward the edge's 3D position, fully at the edge, not at all band_in below it."""
    t, d = nearest_on_polyline(edge_flat, V2)
    w = np.clip(1 - d / band_in, 0, 1)
    w = w * w * (3 - 2 * w)                                   # smoothstep
    E = edge3d(t)
    return V3 * (1 - w)[:, None] + E * w[:, None], w


def place_sleeve(V2, side, top, l_x, hand_dir, gap, under=False):
    """Sleeve draft (x along the arm, A at 0, hand toward -x; y across, up = -y) round the arm."""
    sj, el = SHOULDER_JOINT[side], ELBOW[side]
    ax = (el - sj) / np.linalg.norm(el - sj)
    start = sj + np.array([0, 0, 0.05])                       # just above the joint, the cap's top
    fwd = np.array([0, -1.0, 0])
    e1 = fwd - ax * (fwd @ ax); e1 /= np.linalg.norm(e1)        # toward the front of the arm
    e2 = np.cross(ax, e1)                                       # outward (right side) or inward
    if side == "L":
        e2 = -e2
    out_dir = np.array([1.0 if side == "L" else -1.0, 0, 0])
    if e2 @ out_dir < 0:
        e2 = -e2                                                # e2 points away from the body
    along = (l_x - V2[:, 0]) * IN                               # from the cap's top down the arm
    h = top                                                     # width of the piece across (in)
    t = np.clip(-V2[:, 1] / h, 0, 1)                            # 0 at the hind seam, 1 at the forearm
    # top sleeve: from the back of the arm (hind) over the outside to the front (forearm)
    ang = (-math.pi / 2 + t * math.pi) if not under else (math.pi / 2 + (1 - t) * math.pi)
    r = 0.065 + gap
    P = start[None, :] + along[:, None] * ax[None, :] + r * (np.cos(ang)[:, None] * e2[None, :] + np.sin(ang)[:, None] * e1[None, :])
    return P


def pairs_by_length(A3, ia, B3, ib):
    """Sew stretch a (vertex ids ia, in order) to stretch b (ib, same direction), matching by
    normalised arc length on the flat pieces; every vertex of the longer side gets a partner."""
    def s(P):
        d = np.concatenate([[0], np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))])
        return d / max(d[-1], 1e-9)
    sa, sb = s(A3[ia]), s(B3[ib])
    out = []
    if len(ia) >= len(ib):
        for k, v in zip(sa, ia):
            out.append((v, ib[int(np.argmin(np.abs(sb - k)))]))
    else:
        for k, v in zip(sb, ib):
            out.append((ia[int(np.argmin(np.abs(sa - k)))], v))
    return out


def build(tag="ron", ver="v1"):
    pat = json.load(open(os.path.join(HERE, "pattern_%s.json" % tag)))
    P = {k: np.array(v) for k, v in pat["points"].items()}
    sect = body_sections()
    x_cb, x_cf = 0.0, P["J"][0]                 # centre back line to the front (buttoning) line
    z_top = NAPE_Z + 0.5 * IN                   # line A is 1/2 in above D, the nape
    allV, allF, allV2, pieces = [], [], [], {}
    bend, pin = [], []
    l_x_top = float(np.max(np.array(pat["pieces"]["top_sleeve"]["outline_in"])[:, 0]))

    def add(name, V3, F, ring, stretches, bendw, V2):
        off = sum(len(v) for v in allV)
        allV.append(V3)
        allV2.append(V2)
        allF.append(F + off)
        bend.append(bendw)
        pieces[name] = {"offset": off, "n": len(V3), "ring": (ring + off).tolist(), "stretches": stretches}
        return off

    lapel_info, lapel_sets = {}, {}
    for side in ("R", "L"):
        for pname in ("back", "forepart", "top_sleeve", "under_sleeve", "collar"):
            pc = pat["pieces"][pname]
            O = np.array(pc["outline_in"])
            stretches = {k: (a, b) for k, (a, b) in pc["stretches"].items()}
            if np.linalg.norm(O[-1] - O[0]) < 1e-6:          # closed back on its first point
                n0 = len(O) - 1
                O = O[:-1]
                stretches = {k: (a % n0, b % n0 if b < n0 else 0) for k, (a, b) in stretches.items()}
            corners = sorted({a for a, b in stretches.values()} | {b for a, b in stretches.values()})
            V2, F, ring, corner_at = mesh_panel(O, SPACING_IN, corners=corners)
            # outline index -> ring vertex for each stretch end
            st = {k: (corner_at[a], corner_at[b] if b in corner_at else len(ring) - 1) for k, (a, b) in stretches.items()}
            # the last stretch closes on vertex 0
            last = max(st.items(), key=lambda kv: kv[1][0])[0]
            if st[last][1] <= st[last][0]:
                st[last] = (st[last][0], len(ring) + st[last][1])
            bw = np.full(len(V2), 0.15)
            if pname in ("back", "forepart"):
                gap = np.full(len(V2), 0.022)
                if pname == "forepart":
                    # canvassed front: stiffer forward of the fish and above the waist
                    front = (V2[:, 0] > P["T"][0]) & (V2[:, 1] < P["E"][1] + 4)
                    bw[front] = 0.5
                    # the lapel: beyond the crease (JJ -> collar's C), above the break
                    a, b = np.array(pat["lapel"]["break"]), np.array(pat["lapel"]["crease_far"])
                    t = (b - a) / np.linalg.norm(b - a)
                    n = np.array([-t[1], t[0]])
                    if n @ (np.array(pat["lapel"]["lapel_point"]) - a) < 0:
                        n = -n
                    dist = (V2 - a) @ n
                    region = (dist > 0) & (V2[:, 1] < a[1] + 0.2)
                    V2f, h = fold_2d(V2, a, b, region, r=0.45)
                    bw[np.abs(dist) < 1.2] = 1.0              # the roll line, pressed and canvassed
                    bw[region] = np.maximum(bw[region], 0.8)
                    lapel_info[side] = int(region.sum())
                    lapel_sets[side] = (np.where(region)[0], np.where(~region)[0])
                    if side == "L":                           # the left front laps over the right
                        over = V2[:, 0] > P["J"][0]
                        gap[over] += 0.005
                    V3 = place_torso(V2f, side, x_cb, x_cf, z_top, sect, gap + h * IN)
                else:
                    V3 = place_torso(V2, side, x_cb, x_cf, z_top, sect, gap)
                # the band under the top edge laid over the shoulder ridge and round the neck
                def seg(name):
                    a_, b_ = pc["stretches"][name]
                    return O[a_:b_ + 1] if b_ < len(O) else np.vstack([O[a_:], O[:1]])
                if pname == "back":
                    nk, sh = seg("back_neck"), seg("back_shoulder")
                    edge = np.vstack([nk, sh[1:]])
                    ts = np.sum(np.linalg.norm(np.diff(nk, axis=0), axis=1)) / np.sum(np.linalg.norm(np.diff(edge, axis=0), axis=1))
                    def e3d(t, side=side, ts=ts):
                        out = np.zeros((len(t), 3))
                        a_ = t < ts
                        f_ = t[a_] / ts
                        out[a_] = shell.neck_ring(side, 90 + (172 - 90) * f_, NAPE_Z + (NECKSIDE_Z - NAPE_Z) * f_)
                        out[~a_] = shell.ridge(side, (t[~a_] - ts) / (1 - ts))
                        return out
                else:
                    sh, nk = seg("front_shoulder"), seg("neck")
                    edge = np.vstack([sh, nk[1:]])
                    ts = np.sum(np.linalg.norm(np.diff(sh, axis=0), axis=1)) / np.sum(np.linalg.norm(np.diff(edge, axis=0), axis=1))
                    drop = (P["NN"][1] - P["C"][1]) * IN
                    def e3d(t, side=side, ts=ts, drop=drop):
                        out = np.zeros((len(t), 3))
                        a_ = t < ts
                        out[a_] = shell.ridge(side, 1 - t[a_] / ts)
                        f_ = (t[~a_] - ts) / (1 - ts)
                        r_ = shell.neck_ring(side, 172 + (232 - 172) * f_, NECKSIDE_Z - drop * f_)
                        cen = np.array([0.0, shell.NECK_YC, 0.0])
                        out[~a_] = cen + (r_ - cen) * (1 + 0.6 * f_)[:, None]
                        out[~a_, 2] = r_[:, 2]
                        return out
                V3, w_band = top_band(V2, V3, edge, e3d, 5.0)
                low = w_band < 0.5
                V3[low] = shell.hulls().push_out(V3[low], 0.015)
            elif pname in ("top_sleeve", "under_sleeve"):
                width = float(np.max(-V2[:, 1]))
                V3 = place_sleeve(V2, side, width, l_x_top, None, 0.02, under=(pname == "under_sleeve"))
                bw[:] = 0.2
            else:   # collar: round the neck, the fall turned down over the stand on the crease row
                cr = np.array(pat["collar_crease"])
                # along = arc length along the crease from D (centre back); across = signed distance (fall +)
                seg = np.linalg.norm(np.diff(cr, axis=0), axis=1)
                cs = np.concatenate([[0], np.cumsum(seg)])
                along = np.zeros(len(V2)); across = np.zeros(len(V2))
                fpt = np.array(pat["collar_points"]["F"])
                for i, v in enumerate(V2):
                    j = int(np.argmin(np.linalg.norm(cr - v, axis=1)))
                    j = min(j, len(cr) - 2)
                    t = cr[j + 1] - cr[j]; t /= np.linalg.norm(t)
                    nrm = np.array([-t[1], t[0]])
                    along[i] = cs[j] + (v - cr[j]) @ t
                    across[i] = (v - cr[j]) @ nrm
                if np.median(across[np.linalg.norm(V2 - fpt, axis=1) < 1.0]) < 0:
                    across = -across
                neck_r, neck_y = 0.075, 0.0
                ang = math.pi / 2 + along / (cs[-1] + 2.0) * (math.pi * 0.62)
                if side == "L":
                    ang = math.pi - ang
                zc = NAPE_Z + 1.5 * IN                         # the crease row about an inch and a half above the nape
                V3 = np.zeros((len(V2), 3))
                stand = across <= 0
                rr = np.where(stand, neck_r + 0.012, neck_r + 0.012 + 0.008)
                zz = np.where(stand, zc + across * IN, zc - across * IN)
                V3[:, 0] = rr * np.cos(ang)
                V3[:, 1] = neck_y + rr * np.sin(ang) * 1.1
                V3[:, 2] = zz
                bw[:] = 1.0
            if side == "L":
                F = F[:, [0, 2, 1]]                            # keep normals outward after mirroring
            add("%s_%s" % (pname, side), V3, F, ring, st, bw, V2)
    V = np.vstack(allV)
    V2all = np.vstack(allV2)
    Fa = np.vstack(allF)
    bend = np.concatenate(bend)

    def S(piece, name, rev=False):
        pc = pieces[piece]
        a, b = pc["stretches"][name]
        ring = pc["ring"]
        idx = [ring[i % len(ring)] for i in range(a, b + 1)]
        return idx[::-1] if rev else idx

    seams = []
    for side in ("R", "L"):
        f, bk, ts, us, col = ("forepart_" + side, "back_" + side, "top_sleeve_" + side, "under_sleeve_" + side, "collar_" + side)
        seams += pairs_by_length(V, S(bk, "back_shoulder"), V, S(f, "front_shoulder", rev=True))
        seams += pairs_by_length(V, S(bk, "back_side"), V, S(f, "fore_side", rev=True))
        seams += pairs_by_length(V, S(f, "fish_a"), V, S(f, "fish_b", rev=True))
        seams += pairs_by_length(V, S(ts, "forearm_t"), V, S(us, "forearm_u"))
        seams += pairs_by_length(V, S(ts, "hind_t"), V, S(us, "hind_u"))
        # sleeve head K->A into the scye RR -> shoulder -> N; under sleeve K->M into RR -> bottom -> NN
        scye_hi = S(f, "scye_high")                           # fish mouth -> shoulder end
        rr_flat = P["T"] + np.array([0.6, -0.4]) * (pat["scale"] / 18.0)   # forearm pitch (Plate 16)
        rr = int(np.argmin(np.linalg.norm(V2all[scye_hi] - rr_flat, axis=1)))
        back_scye = S(bk, "back_scye")                        # LL -> back side top
        n_i = int(np.argmin(np.linalg.norm(V2all[back_scye] - P["N"], axis=1)))
        nn_i = int(np.argmin(np.linalg.norm(V2all[back_scye] - (P["N"] + np.array([0, 0.5])), axis=1)))
        upper = scye_hi[rr:] + back_scye[:n_i + 1]            # RR -> shoulder end, LL -> N
        seams += pairs_by_length(V, S(ts, "head"), V, upper)
        lower = scye_hi[:rr + 1][::-1] + S(f, "scye_low")[::-1] + back_scye[nn_i:][::-1]   # RR -> bottom -> NN
        seams += pairs_by_length(V, S(us, "under_top"), V, lower)
        # collar: neck edge E -> notch along back neck (D->GG), forepart neck (C->NN) and gorge to the notch
        gorge = S(f, "gorge")
        neckline = S(bk, "back_neck") + S(f, "neck") + gorge[:max(1, len(gorge) // 2)]
        seams += pairs_by_length(V, S(col, "collar_neck"), V, neckline)
    # centre back and the collar's centre back, right to left
    seams += pairs_by_length(V, S("back_R", "back_cb"), V, S("back_L", "back_cb"))
    seams += pairs_by_length(V, S("collar_R", "collar_cb"), V, S("collar_L", "collar_cb"))
    # buttons: the plate's four, on the front line; fasten the top three (a lounge of the period
    # worn with the top buttons done), left front's hole to right front's button
    fronts = {s_: pieces["forepart_" + s_] for s_ in ("R", "L")}
    btn = []
    for bx, by in pat["buttons"][:3]:
        ids = []
        for s_ in ("R", "L"):
            o, n = fronts[s_]["offset"], fronts[s_]["n"]
            ids.append(o + int(np.argmin(np.linalg.norm(V2all[o:o + n] - np.array([bx, by]), axis=1))))
        btn.append(tuple(ids))
    seams += btn
    seams = np.array(sorted({(min(a, b), max(a, b)) for a, b in seams if a != b}), dtype=np.int64)
    pin = np.zeros(len(V))
    path = os.path.join(OUT, "garment_%s.npz" % ver)
    np.savez_compressed(path, V=V, F=Fa, seams=seams, pin=pin, bend=bend)
    lap = {}
    for s_ in ("R", "L"):
        o = pieces["forepart_" + s_]["offset"]
        lap["lapel_" + s_] = lapel_sets[s_][0] + o
        lap["front_" + s_] = lapel_sets[s_][1] + o
    notch = np.array(pat["lapel"]["notch"])
    def nearest(piece, xy):
        o, n = pieces[piece]["offset"], pieces[piece]["n"]
        return o + int(np.argmin(np.linalg.norm(V2all[o:o + n] - np.asarray(xy), axis=1)))
    fe = np.array(pat["pieces"]["forepart"]["outline_in"])
    fe_end = fe[pat["pieces"]["forepart"]["stretches"]["front_edge"][1]]
    bo = np.array(pat["pieces"]["back"]["outline_in"])
    bh = bo[pat["pieces"]["back"]["stretches"]["back_hem"][0]]
    lap["notch"] = np.array([nearest("forepart_R", notch), nearest("forepart_L", notch)])
    lap["front_bottom"] = np.array([nearest("forepart_R", fe_end), nearest("forepart_L", fe_end)])
    lap["back_bottom"] = np.array([nearest("back_R", bh), nearest("back_L", bh)])
    np.savez(path.replace(".npz", "_lapel.npz"), **lap)
    meta = {"pieces": pieces, "lapel_vertices": lapel_info, "buttons": btn, "n_vertices": int(len(V)),
            "n_triangles": int(len(Fa)), "n_seam_pairs": int(len(seams))}
    json.dump(meta, open(path.replace(".npz", ".json"), "w"))
    print("garment", path, len(V), "verts", len(Fa), "tris", len(seams), "seam pairs", "lapel", lapel_info)
    return path


if __name__ == "__main__":
    build(sys.argv[1] if len(sys.argv) > 1 else "ron", sys.argv[2] if len(sys.argv) > 2 else "v1")
