"""The automatic check: the built door against the target's drawings.

    python check_door.py F:/LedgerTools/lab/door/build/door_v1.npz   -> checks/check_v1.json (git), overlays on F:

The target writer's target_drawings.json holds each drawing as filled polygons in millimetres
(the outside elevation, a horizontal section through the lower panels, a vertical section
through the left-hand panels). The model is cut exactly where each is drawn (tools/outline.py:
silhouette for the elevation, section for the cuts), both are rasterised at 0.5 mm a pixel in
one frame, and compared: overlap (IoU) and the distance between outlines both ways.
Pass, as the sash window's: IoU >= 0.97, outline p95 <= 2 mm and max <= 6 mm, and every
overall dimension within 1 mm.
"""
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from outline import Frame, compare, load_npz, overlay, section, silhouette  # noqa: E402

PASS = {"iou": 0.97, "p95_mm": 2.0, "max_mm": 6.0, "dim_mm": 1.0}
MMPX = 0.5
OUT = "F:/LedgerTools/lab/door/checks"


def frame_for(polys, margin=20.0):
    P = np.vstack([np.asarray(p, float) for p in polys])
    lo, hi = P.min(0) - margin, P.max(0) + margin
    return Frame(u0=lo[0] / 1000, v0=lo[1] / 1000, width=(hi[0] - lo[0]) / 1000, height=(hi[1] - lo[1]) / 1000, mm_per_px=MMPX)


def raster(polys, fr):
    img = Image.new("1", (fr.shape[1], fr.shape[0]), 0)
    dr = ImageDraw.Draw(img)
    for p in polys:
        P = np.asarray(p, float) / 1000.0
        Q = np.stack(fr.to_px(P[:, 0], P[:, 1]), 1)
        dr.polygon([tuple(q) for q in Q], fill=1, outline=1)
    return np.array(img, bool)


JOINERY = ("frame", "glass", "leaf", "panel", "moulding")   # ironmongery ("iron") and context are left out


def target_layers(polys, fr):
    """The target's front view as a label image: polygons in the order drawn, later on top."""
    lab = np.zeros(fr.shape, np.int8)
    for p in polys:
        if p["layer"] not in JOINERY:
            continue
        m = raster([p["pts"]], fr)
        for h in p.get("holes", []):
            m &= ~raster([h], fr)
        lab[m] = JOINERY.index(p["layer"]) + 1
    return lab


def model_layers(meshes, fr):
    """The model's front view as a label image: at each pixel the part nearest the street."""
    lab = np.zeros(fr.shape, np.int8)
    depth = np.full(fr.shape, np.inf)
    for name, (V, F) in meshes.items():
        layer = name.split("_")[0]
        if layer not in JOINERY:
            continue
        m = silhouette({name: (V, F)}, (0, 2), fr)
        y = V[:, 1].min()
        sel = m & (y < depth)
        lab[sel] = JOINERY.index(layer) + 1
        depth[sel] = y
    return lab


def main(npz):
    ver = os.path.basename(npz).replace("door_", "").replace(".npz", "")
    meshes = load_npz(npz)
    T = json.load(open(os.path.join(HERE, "target", "target.json"), encoding="utf-8"))
    D = json.load(open("F:/LedgerTools/lab/door/target/target_drawings.json"))
    os.makedirs(OUT, exist_ok=True)
    res = {"model": npz, "pass_rule": PASS, "drawings": {}, "dims": {}}
    ok = True
    # 1. the front view, layer by layer, inside the brick opening
    E = D["elevation"]["polygons"]
    fr = frame_for([p["pts"] for p in E if p["layer"] in JOINERY])
    tl, ml = target_layers(E, fr), model_layers(meshes, fr)
    W, H = T["opening"]["brick_width_mm"], T["opening"]["brick_height_mm"]
    hh, ww = fr.shape
    u = (fr.u0 + (np.arange(ww) + 0.5) * fr.mm_per_px / 1000) * 1000
    v = (fr.v0 + fr.height - (np.arange(hh) + 0.5) * fr.mm_per_px / 1000) * 1000
    inside = (u[None, :] >= 0) & (u[None, :] <= W) & (v[:, None] >= 0) & (v[:, None] <= H)
    for i, layer in enumerate(JOINERY, 1):
        a, b = (ml == i) & inside, (tl == i) & inside
        if not b.any():
            continue
        c = compare(a, b, MMPX)
        c["ok"] = bool(c["iou"] >= PASS["iou"] and c["p95_mm"] is not None and c["p95_mm"] <= PASS["p95_mm"] and c["max_mm"] <= PASS["max_mm"])
        ok &= c["ok"]
        res["drawings"]["elevation_" + layer] = c
        overlay(a, b, os.path.join(OUT, "overlay_%s_elevation_%s.png" % (ver, layer)))
    # 2. the two sections, all joinery together
    for key, axis, axes, at in (("section_h", 2, (0, 1), D["section_h"]["cut_z_mm"]), ("section_v", 0, (1, 2), D["section_v"]["cut_x_mm"])):
        P = [p for p in D[key]["polygons"] if p["layer"] in JOINERY]
        fr = frame_for([p["pts"] for p in P])
        b = raster([p["pts"] for p in P], fr)
        joinery = {k: v for k, v in meshes.items() if k.split("_")[0] in JOINERY}
        a = section(joinery, axis, at / 1000.0, axes, fr)
        c = compare(a, b, MMPX)
        c["ok"] = bool(c["iou"] >= PASS["iou"] and c["p95_mm"] is not None and c["p95_mm"] <= PASS["p95_mm"] and c["max_mm"] <= PASS["max_mm"])
        ok &= c["ok"]
        res["drawings"][key] = c
        overlay(a, b, os.path.join(OUT, "overlay_%s_%s.png" % (ver, key)))
    # 3. the overall dimensions, off the model's vertices
    def bb(name):
        V = meshes[name][0] * 1000
        return V.min(0), V.max(0)
    lf, fr_ = T["leaf"], T["frame"]
    lo = np.min([bb(k)[0] for k in meshes if k.startswith(("leaf_",))], 0)
    hi = np.max([bb(k)[1] for k in meshes if k.startswith(("leaf_",))], 0)
    checks = {
        "leaf_width": (hi[0] - lo[0], lf["width_mm"]),
        "leaf_height": (hi[2] - lo[2], lf["height_mm"]),
        "leaf_thickness": (hi[1] - lo[1], lf["thickness_mm"]),
        "stile": (bb("leaf_stile_L")[1][0] - bb("leaf_stile_L")[0][0], lf["stile_mm"]),
        "muntin": (bb("leaf_muntin_low")[1][0] - bb("leaf_muntin_low")[0][0], lf["muntin_mm"]),
        "top_rail": (bb("leaf_top_rail")[1][2] - bb("leaf_top_rail")[0][2], lf["top_rail_mm"]),
        "lock_rail": (bb("leaf_lock_rail")[1][2] - bb("leaf_lock_rail")[0][2], lf["lock_rail_mm"]),
        "bottom_rail": (bb("leaf_bottom_rail")[1][2] - bb("leaf_bottom_rail")[0][2], lf["bottom_rail_mm"]),
        "jamb_face": (bb("frame_jamb_L")[1][0] - bb("frame_jamb_L")[0][0], fr_["jamb_face_mm"]),
        "jamb_depth": (bb("frame_jamb_L")[1][1] - bb("frame_jamb_L")[0][1], fr_["jamb_depth_mm"]),
        "panel_thickness": (bb("panel_panel_bottom_left")[1][1] - bb("panel_panel_bottom_left")[0][1], T["panels"]["thickness_mm"]),
    }
    for k, (got, want) in checks.items():
        d = abs(got - want)
        res["dims"][k] = {"model_mm": round(float(got), 2), "target_mm": want, "ok": bool(d <= PASS["dim_mm"])}
        ok &= d <= PASS["dim_mm"]
    res["pass"] = bool(ok)
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    json.dump(res, open(os.path.join(HERE, "checks", "check_%s.json" % ver), "w"), indent=1)
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1])
