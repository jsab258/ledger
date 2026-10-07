"""The automatic check: the built Blender model against the target drawing.

    python check_window.py F:/LedgerTools/lab/sash/build/window_v1.npz   -> checks/check_v1.json (git), overlays on F:

Cuts the model exactly where the target is drawn (elevation = outline of the
joinery seen from outside, glass left out; vertical section at a quarter of the
width; horizontal section through the lower sash's middle), compares each with
target.npz in millimetres, and checks the overall dimensions against the
numbers. Pass: every drawing IoU >= 0.97, outline p95 <= 2 mm and max <= 6 mm,
every dimension within 1 mm.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
from outline import compare, load_npz, overlay, section, silhouette  # noqa: E402
from target_drawing import BUILD, FRAMES, load_target, members  # noqa: E402

PASS = {"iou": 0.97, "p95_mm": 2.0, "max_mm": 6.0, "dim_mm": 1.0}


def model_drawings(meshes, T, geo):
    joinery = {k: v for k, v in meshes.items() if not k.endswith("_glass")}
    fr = FRAMES["elev"](T)
    elev = silhouette(joinery, (0, 2), fr)
    # the brick hides everything outside its opening: keep only what shows through it
    h, w = fr.shape
    u = np.arange(w) * fr.mm_per_px / 1000 + fr.u0
    v = (h - np.arange(h)) * fr.mm_per_px / 1000 + fr.v0
    inside = (np.abs(u)[None, :] <= geo["W"] / 2) & (v[:, None] <= geo["H"]) & (v[:, None] >= 0)
    elev &= inside
    vsec = section(joinery, 0, geo["W"] / 4, (1, 2), FRAMES["vsec"](T))
    zmid = (geo["z_lo"][0] + geo["z_lo"][1]) / 2
    hsec = section(joinery, 2, zmid, (0, 1), FRAMES["hsec"](T))
    xs = geo.get("x_sash", geo["x_ps"]) - T["sash"]["stile_width_mm"] / 2000.0
    vst = section(joinery, 0, xs, (1, 2), FRAMES["vsec_stile"](T))
    upper = {k: v for k, v in joinery.items() if k.startswith("upper_")}
    eup = silhouette(upper, (0, 2), FRAMES["elev_upper"](T))
    return {"elev": elev, "vsec": vsec, "hsec": hsec, "vsec_stile": vst, "elev_upper": eup}


def dims(meshes, T, geo):
    """Overall numbers measured off the model's vertices."""
    allv = np.vstack([V for k, (V, F) in meshes.items() if not k.endswith("_glass")])
    s = T["sash"]
    out = {}

    def bb(name):
        V = meshes[name][0]
        return V.min(0), V.max(0)

    lo, hi = bb("upper_stile_L")
    out["sash_thickness_mm"] = ((hi[1] - lo[1]) * 1000, s["thickness_mm"])
    out["stile_width_mm"] = ((hi[0] - lo[0]) * 1000, s["stile_width_mm"])
    hl, hh = bb("upper_horn_L")
    out["horn_length_mm"] = ((hh[2] - hl[2]) * 1000, s["horn_length_mm"])
    lo, hi = bb("lower_bottom_rail")
    out["bottom_rail_mm"] = ((hi[2] - lo[2]) * 1000, s["bottom_rail_mm"])
    lo, hi = bb("upper_top_rail")
    out["top_rail_mm"] = ((hi[2] - lo[2]) * 1000, s["top_rail_mm"])
    lo, hi = bb("lower_top_rail")
    out["meeting_rail_depth_mm"] = ((hi[2] - lo[2]) * 1000, s["meeting_rail_depth_mm"])
    xl = meshes["outer_lining_L"][0][:, 0].max()
    xr = meshes["outer_lining_R"][0][:, 0].min()
    out["opening_width_mm"] = ((xr - xl) * 1000 + 2 * T["frame"]["outer_lining_margin_mm"], T["opening"]["width_mm"])
    out["opening_height_mm"] = (meshes["head_outer_lining"][0][:, 2].max() * 1000, T["opening"]["height_mm"])
    out["reveal_mm"] = ((meshes["outer_lining_L"][0][:, 1].min()) * 1000, T["frame"]["reveal_mm"])
    if "upper_bar" in meshes:
        lo, hi = bb("upper_bar")
        out["glazing_bar_width_mm"] = ((hi[0] - lo[0]) * 1000, s["glazing_bar_width_mm"])
    return {k: {"model": round(float(a), 2), "target": b, "ok": bool(abs(a - b) <= PASS["dim_mm"])} for k, (a, b) in out.items()}


def main(npz):
    T = load_target()
    _, geo = members(T)
    target = np.load(os.path.join(BUILD, "target.npz"))
    meshes = load_npz(npz)
    M = model_drawings(meshes, T, geo)
    ver = os.path.basename(npz).replace("window_", "").replace(".npz", "")
    res = {"model": npz.replace("\\", "/"), "drawings": {}, "dims": dims(meshes, T, geo)}
    ok = True
    for k in ("elev", "vsec", "hsec", "vsec_stile", "elev_upper"):
        m = compare(M[k], target[k], FRAMES[k](T).mm_per_px)
        m["ok"] = bool(m["iou"] >= PASS["iou"] and m["p95_mm"] is not None and m["p95_mm"] <= PASS["p95_mm"]
                   and m["max_mm"] <= PASS["max_mm"])
        ok &= m["ok"]
        res["drawings"][k] = m
        overlay(M[k], target[k], os.path.join(BUILD, "overlay_%s_%s.png" % (ver, k)), scale=0.5 if k not in ("vsec", "vsec_stile", "elev_upper") else 1)
    ok &= all(d["ok"] for d in res["dims"].values())
    res["pass"] = bool(ok)
    res["thresholds"] = PASS
    out = os.path.join(HERE, "checks", "check_%s.json" % ver)
    json.dump(res, open(out, "w"), indent=1)
    print(json.dumps(res, indent=1))
    return res


if __name__ == "__main__":
    main(sys.argv[1])
