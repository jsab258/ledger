"""Numbers off the draped jacket: does the lapel hold, and how do its front and side
outlines compare with the period photographs (photo-landmarks.json)?

    python measure_drape.py v1      -> checks/drape_v1.json and outline pictures on F:

The lapel: each turned-over lapel vertex is looked for on the outside of the
forepart beneath it. Held = it still lies outside the front, within 0.3 to 4 cm of
it, and the turned part's normal still faces away from the chest; collapsed = it
has fallen through, stands off, or flipped back.

The outlines: front and side silhouettes of the jacket alone, computed from its
triangles (no renderer); landmarks read off them and off the mesh's own vertices
(buttons, notch) as ratios of the jacket's length, the same ratios read off the
photographs.
"""
import json
import os
import sys

import numpy as np
from scipy.spatial import cKDTree

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from outline import Frame, silhouette  # noqa: E402

OUT = r"F:/LedgerTools/lab/jacket"


def tri_normals(V, F):
    n = np.cross(V[F[:, 1]] - V[F[:, 0]], V[F[:, 2]] - V[F[:, 0]])
    return n / np.maximum(np.linalg.norm(n, axis=1, keepdims=True), 1e-12)


def vertex_normals(V, F):
    tn = tri_normals(V, F)
    vn = np.zeros_like(V)
    for k in range(3):
        np.add.at(vn, F[:, k], tn)
    return vn / np.maximum(np.linalg.norm(vn, axis=1, keepdims=True), 1e-12)


def main(ver):
    g = np.load(os.path.join(OUT, "garment_%s.npz" % ver))
    s = np.load(os.path.join(OUT, "sewn_%s.npz" % ver))
    meta = json.load(open(os.path.join(OUT, "garment_%s.json" % ver)))
    lap = np.load(os.path.join(OUT, "garment_%s_lapel.npz" % ver))
    V0, F = g["V"], g["F"]
    V = s["garment_V"]
    res = {"version": ver, "lapel": {}, "outline": {}}
    # ---- the lapel ---------------------------------------------------------------
    for side in ("R", "L"):
        lv = lap["lapel_" + side]                    # turned-over vertex ids
        fv = lap["front_" + side]                    # the forepart's vertices that are not turned
        tree = cKDTree(V[fv])
        d, j = tree.query(V[lv])
        under = fv[j]
        # outward direction: from the body's axis through the front point beneath
        radial = V[under][:, :2] - np.array([0.0, -0.02])
        radial = np.c_[radial / np.linalg.norm(radial, axis=1, keepdims=True), np.zeros(len(radial))]
        sep = np.einsum("ij,ij->i", V[lv] - V[under], radial)
        held = (sep > 0.003) & (sep < 0.04)
        d0, j0 = cKDTree(V0[fv]).query(V0[lv])
        res["lapel"][side] = {"turned_vertices": int(len(lv)), "held_fraction": round(float(held.mean()), 3),
                              "lies_outside_mean_cm": round(float(np.median(sep) * 100), 2),
                              "gap_start_cm": round(float(np.median(d0) * 100), 2), "gap_end_cm": round(float(np.median(d) * 100), 2)}
    # ---- outlines ------------------------------------------------------------------
    M = {"jacket": (V, F)}
    fr_front = Frame(-0.5, 0.6, 1.0, 1.2, 2.0)
    fr_side = Frame(-0.45, 0.6, 0.9, 1.2, 2.0)
    front = silhouette(M, (0, 2), fr_front)
    side = silhouette(M, (1, 2), fr_side)
    from PIL import Image
    Image.fromarray((~front * 255).astype(np.uint8)).save(os.path.join(OUT, "renders", "outline_front_%s.png" % ver))
    Image.fromarray((~side * 255).astype(np.uint8)).save(os.path.join(OUT, "renders", "outline_side_%s.png" % ver))
    z = V[:, 2]
    top_z = z.max()                                   # the collar at the back of the neck
    # neck points: highest jacket vertices near the side of the neck
    neck = V[(np.abs(V[:, 0]) > 0.05) & (np.abs(V[:, 0]) < 0.12)]
    neck_z = float(np.percentile(neck[:, 2], 98))
    # hem at the side: lowest vertex with |x| > 0.15
    sidev = V[np.abs(V[:, 0]) > 0.15]
    hem_side_z = float(np.percentile(sidev[:, 2], 1))
    L = neck_z - hem_side_z
    shoulder_z_band = (V[:, 2] > neck_z - 0.12) & (V[:, 2] < neck_z - 0.02)
    sh_w = float(V[shoulder_z_band, 0].max() - V[shoulder_z_band, 0].min())
    btn = meta["buttons"]
    top_btn_z = float(np.mean([V[b[0], 2] for b in btn[:1]]))
    notch_ids = lap["notch"]
    notch_z = float(np.mean(V[notch_ids, 2]))
    front_hem_z = float(V[lap["front_bottom"], 2].mean())
    back_hem_z = float(V[lap["back_bottom"], 2].mean())
    ratios = {"shoulder_over_L": sh_w / L, "notch_over_L": (neck_z - notch_z) / L, "button_over_L": (neck_z - top_btn_z) / L}
    bands = json.load(open(os.path.join(HERE, "photo-landmarks.json")))["bands"]
    res["outline"] = {"L_m": round(L, 4), "shoulder_width_m": round(sh_w, 4),
                      "hem_front_minus_back_cm": round((back_hem_z - front_hem_z) * 100, 2),
                      "ratios": {k: round(v, 3) for k, v in ratios.items()},
                      "bands": bands,
                      "in_band": {k: bool(bands[k][0] <= v <= bands[k][1]) for k, v in ratios.items()}}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "checks", "drape_%s.json" % ver), "w"), indent=1)
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "v1")
