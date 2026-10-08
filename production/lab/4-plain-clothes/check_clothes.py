"""The automatic checks on the modelled clothes, against the target writer's target.

    python check_clothes.py F:/LedgerTools/lab/clothes/clothes_v1.npz   -> checks/check_v1.json

1. Outline: each garment's silhouette from the front, side and back, against the target's
   outline polygons (target/target.json, rasterised by target/target_outline.py at 2 mm a
   pixel). Pass: every point of each outline within 10 mm of the target's (both ways).
2. Poke-through: every body point the garment must cover (target.json's covered regions,
   or the default bands below) tested against the garment: the nearest garment point and its
   outward normal; a body point on the outside counts. Pass: none.
3. Seams: each modelled seam against the target's seam polyline of the same name. Pass:
   every point within 10 mm.
"""
import json
import os
import sys

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from outline import Frame, compare, overlay, silhouette  # noqa: E402

OUT = r"F:/LedgerTools/lab/clothes"
TOL_MM = 10.0


def vnormals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    vn = np.zeros_like(V)
    for k in range(3):
        np.add.at(vn, F[:, k], n)
    return vn / np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)


def load_parts(path):
    d = np.load(path)
    parts = {k[:-2]: (d[k], d[k[:-2] + "_F"]) for k in d.files if k.endswith("_V")}
    seams = {k[5:]: d[k] for k in d.files if k.startswith("seam_")}
    return parts, seams


def garment_of(name):
    return "trousers" if name.startswith("trouser") else "jumper"


def _basis(a):
    e1 = np.cross(a, [0, 0, 1.0]) if abs(a[2]) < 0.99 else np.array([1.0, 0, 0])
    e1 /= np.linalg.norm(e1)
    return e1, np.cross(a, e1)


def _in_poly(P, Q):
    """Crossing-number test: which 2D points P lie inside the closed polygon Q."""
    x, y = P[:, 0][:, None], P[:, 1][:, None]
    x1, y1 = Q[:, 0][None], Q[:, 1][None]
    x2, y2 = np.roll(Q[:, 0], -1)[None], np.roll(Q[:, 1], -1)[None]
    c = ((y1 > y) != (y2 > y)) & (x < (x2 - x1) * (y - y1) / np.where(y2 == y1, 1e-12, y2 - y1) + x1)
    return (c.sum(1) % 2) == 1


def inside_tube(P, R, C, A, reach=0.35, slab=0.008):
    """Which points P lie inside a tube of rings R (m,n,3) with centres C and axes A: the
    nearest ring plane (among rings within `reach`) must be within `slab`, and the point,
    seen along that ring's axis, inside the ring."""
    D = np.einsum("pmk,mk->pm", P[:, None, :] - C[None], A)
    far = np.linalg.norm(P[:, None, :] - C[None], axis=2) > reach
    D = np.where(far, np.inf, np.abs(D))
    i = np.argmin(D, axis=1)
    ok = D[np.arange(len(P)), i] <= slab
    out = np.zeros(len(P), bool)
    for r in np.unique(i[ok]):
        sel = np.where(ok & (i == r))[0]
        e1, e2 = _basis(A[r])
        q = P[sel] - C[r]
        Q = R[r] - C[r]
        out[sel] = _in_poly(np.stack([q @ e1, q @ e2], 1), np.stack([Q @ e1, Q @ e2], 1))
    return out


def under_surface(P, Vs, Fs, body_V, reach=0.03):
    """Which points P lie beneath an open offset surface: nearest surface point within reach,
    and the point behind it along the surface's outward normal."""
    N = vnormals(Vs, Fs)
    j = cKDTree(body_V).query(Vs)[1]
    if np.mean(np.einsum("ij,ij->i", Vs - body_V[j], N)) < 0:
        N = -N
    d, k = cKDTree(Vs).query(P)
    return (d < reach) & (np.einsum("ij,ij->i", P - Vs[k], N[k]) < 0)


def poke_through(npz, body, covered):
    """Count covered body points not inside the garment, by two tests: the garment's filled
    solid (the same solid its surface was taken from), and the finished surface itself (the
    nearest surface point and its outward normal). A point failing either counts."""
    d = np.load(npz)
    V = body["V"]
    res = {}
    for g in ("jumper", "trousers"):
        m = covered[g]
        P = V[m]
        field = d["sdf_" + g].astype(np.float32)
        q = (P - d["sdf_" + g + "_lo"]) / float(d["sdf_" + g + "_h"])
        from scipy import ndimage
        in_solid = ndimage.map_coordinates(field, q.T, order=1, mode="constant", cval=1.0) < 0.0
        GV, GF = d[g + "_V"], d[g + "_F"]
        N = vnormals(GV, GF)
        j = cKDTree(V).query(GV)[1]
        if np.mean(np.einsum("ij,ij->i", GV - V[j], N)) < 0:
            N = -N
        dist, k = cKDTree(GV).query(P)
        side = np.einsum("ij,ij->i", P - GV[k], N[k])
        in_surface = side <= 0.0005
        bad = ~(in_solid & in_surface)
        res[g] = {"covered_points": int(m.sum()), "through": int(bad.sum()),
                  "outside_solid": int((~in_solid).sum()), "outside_surface": int((~in_surface).sum()),
                  "closest_gap_mm": round(float((-side[in_surface]).min() * 1000), 1)}
        if bad.any():
            res[g]["worst_mm"] = round(float(dist[bad].max() * 1000), 1)
        res[g]["_mask"] = np.where(m)[0][bad]
    return res


def target_covered(body):
    """The body points the target says each garment must cover (cover_lod0.npz, LOD0 indices)."""
    c = np.load(os.path.join(OUT, "target", "cover_lod0.npz"))
    n = len(body["V"])
    out = {}
    for g in ("jumper", "trousers"):
        m = np.zeros(n, bool)
        m[c[g]] = True
        out[g] = m
    return out


def default_covered(body, T):
    V = body["V"]
    cov = T.get("covered", {}) if T else {}
    z = V[:, 2]
    jz0 = cov.get("jumper_z_min", 1.02)
    jz1 = cov.get("jumper_z_max_back", 1.62)
    wrist_z = cov.get("wrist_z", 1.06)
    jumper = ((body["torso"] & (z > jz0) & (z < jz1)) | (body["arm"] & (z > wrist_z) & (z < jz1)))
    tz0 = cov.get("trousers_z_min", 0.08)
    tz1 = cov.get("trousers_z_max", 1.12)
    trousers = (body["legs"] | body["torso"]) & (z > tz0) & (z < tz1)
    return {"jumper": jumper, "trousers": trousers}


def main(npz):
    ver = os.path.basename(npz).replace("clothes_", "").replace(".npz", "")
    parts, seams = load_parts(npz)
    body = np.load(os.path.join(OUT, "ron_parts.npz"))
    tpath = os.path.join(HERE, "target", "target.json")
    T = json.load(open(tpath)) if os.path.exists(tpath) else None
    res = {"model": npz.replace("\\", "/"), "tolerance_mm": TOL_MM}
    # 2. poke-through
    pt = poke_through(npz, body, target_covered(body))
    res["poke_through"] = {g: {k: v for k, v in d.items() if not k.startswith("_")} for g, d in pt.items()}
    ok = all(d["through"] == 0 for d in pt.values())
    # layering: the trousers' surface under the jumper (above its hem) must lie inside the jumper
    d = np.load(npz)
    TV = d["trousers_V"]
    jz = float(d["jumper_V"][:, 2].min()) + 0.005
    under = TV[TV[:, 2] > jz]
    q = (under - d["sdf_jumper_lo"]) / float(d["sdf_jumper_h"])
    from scipy import ndimage
    inside = ndimage.map_coordinates(d["sdf_jumper"].astype(np.float32), q.T, order=1, mode="constant", cval=1.0) < 0.0
    res["trousers_through_jumper"] = {"trouser_points_under_jumper": int(len(under)), "through": int((~inside).sum())}
    ok &= bool(inside.all())
    # 1. outline: each garment's silhouette against the target's outline polygons, both
    #    rasterised at 2 mm a pixel in the target's frames (front and back share a silhouette)
    from PIL import Image, ImageDraw
    res["outline"] = {}
    for g in ("jumper", "trousers"):
        for view in ("front", "side", "back"):
            frd = T["masks"]["side_frame" if view == "side" else "front_frame"]
            fr = Frame(**frd)
            img = Image.new("1", (fr.shape[1], fr.shape[0]), 0)
            dr = ImageDraw.Draw(img)
            for poly in T["views"][g][view]:
                P2 = np.asarray(poly, float)
                Q = np.stack(fr.to_px(P2[:, 0], P2[:, 1]), 1)
                dr.polygon([tuple(q) for q in Q], fill=1, outline=1)
            tgt = np.array(img, dtype=bool)
            axes = (1, 2) if view == "side" else (0, 2)
            M = silhouette({g: parts[g]}, axes, fr)
            c = compare(M, tgt, fr.mm_per_px)
            c["ok"] = bool(c["max_mm"] is not None and c["max_mm"] <= TOL_MM)
            ok &= c["ok"]
            res["outline"]["%s_%s" % (g, view)] = c
            overlay(M, tgt, os.path.join(OUT, "checks", "overlay_%s_%s_%s.png" % (ver, g, view)))
    # 3. seams: each target seam against the modelled seam of the same name
    res["seams"] = {}
    for g in ("jumper", "trousers"):
        for name, poly in T["seams"][g].items():
            if name not in seams:
                res["seams"][name] = {"ok": False, "note": "not modelled"}
                ok = False
                continue
            A = np.asarray(poly, float)
            Bm = seams[name]
            d1 = cKDTree(A).query(Bm)[0]
            d2 = cKDTree(Bm).query(A)[0]
            mx = float(max(d1.max(), d2.max()) * 1000)
            res["seams"][name] = {"max_mm": round(mx, 1), "mean_mm": round(float(np.r_[d1, d2].mean() * 1000), 1), "ok": mx <= TOL_MM}
            ok &= mx <= TOL_MM
    res["pass"] = bool(ok)
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "checks", "check_%s.json" % ver), "w"), indent=1)
    print(json.dumps(res, indent=1)[:4000])
    return res


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "checks"), exist_ok=True)
    main(sys.argv[1])
