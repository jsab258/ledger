"""The gate's measurements (target 9): per window, from a beauty frame and its flat-colour mask (R: 1 glass, 2 joinery, 3 cloth, 4 brick, 5 card; G: the window's number). Numpy and PIL only.

P the median sRGB luma of the pane pixels (glass, with the net and the room seen through it); L the 90th percentile of the joinery's luma; D the 5th percentile over the window's outline (joinery and pane);
spread the pane's 95th minus 5th percentile; the line profile of WB-04b; the states bare, net or draped (target 9 window_states).
"""
import numpy as np
from PIL import Image

import hw_t as T

MIN_PANE_PX = 150


def luma(a):
    a = a.astype(np.float32)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def load(frame_png, mask_png):
    b = np.asarray(Image.open(frame_png).convert("RGB"))
    m = np.asarray(Image.open(mask_png).convert("RGB"))
    return b, m


def window_state(site):
    """bare / net / draped (target 9): bare is N0 with no curtain and no blind; draped any B1 to B3 or C1; a C2 counts by its net (N0 with C2: bare? the target counts C2 by its net: N0 + C2 is bare)."""
    ex = (site.get("extra") or {}).get("kind")
    if ex in ("B1", "B2", "B3", "C1"):
        return "draped"
    return "bare" if site["net"]["kind"] == "N0" else "net"


def stats_for(b, m, wid, site=None):
    Lm = luma(b)
    R, Gc = m[..., 0], m[..., 1]
    glass = (R == 1) & (Gc == wid)
    joy = (R == 2) & (Gc == wid)
    if glass.sum() < MIN_PANE_PX or joy.sum() < MIN_PANE_PX:
        return None
    pane = Lm[glass]
    jl = Lm[joy]
    both = Lm[glass | joy]
    out = {"pane_px": int(glass.sum()), "joinery_px": int(joy.sum()), "P": float(np.median(pane)), "L": float(np.percentile(jl, 90)), "D": float(np.percentile(both, 5)),
           "spread": float(np.percentile(pane, 95) - np.percentile(pane, 5)), "pane_rgb_mean": [float(v) for v in b[glass].mean(axis=0)]}
    out["P_over_L"] = out["P"] / max(out["L"], 1e-6)
    out["D_over_L"] = out["D"] / max(out["L"], 1e-6)
    ys, xs = np.nonzero(glass | joy)
    out["bbox"] = [int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())]
    return out


def line_profile(b, m, wid, L):
    """WB-04b: a horizontal luma profile across each stile-to-pane edge (through the pane's mid-height) and a vertical profile across each rail-to-pane edge (through the pane's mid-width): the darkest pixel in
    the 3 pixels each side of the edge over L. Returns the lowest of those ratios found over the window's pane edges and the number of edges profiled."""
    Lm = luma(b)
    R, Gc = m[..., 0], m[..., 1]
    glass = (R == 1) & (Gc == wid)
    joy = (R == 2) & (Gc == wid)
    if not glass.any():
        return None
    ys, xs = np.nonzero(glass)
    ym = int(np.median(ys))
    xm = int(np.median(xs))
    ratios = []
    row = glass[ym]
    jrow = joy[ym]
    edges = np.nonzero(np.diff(row.astype(np.int8)) != 0)[0]
    for e in edges:
        seg = Lm[ym, max(e - 2, 0):e + 4]
        near_j = jrow[max(e - 3, 0):e + 5].any()
        if near_j:
            ratios.append(float(seg.min() / max(L, 1e-6)))
    col = glass[:, xm]
    jcol = joy[:, xm]
    edges = np.nonzero(np.diff(col.astype(np.int8)) != 0)[0]
    for e in edges:
        seg = Lm[max(e - 2, 0):e + 4, xm]
        near_j = jcol[max(e - 3, 0):e + 5].any()
        if near_j:
            ratios.append(float(seg.min() / max(L, 1e-6)))
    return {"min_ratio": min(ratios) if ratios else None, "edges": len(ratios)}


def see_through(m, wid_ids=None):
    """No see-through slot: inside each window's outline box (its glass and joinery pixels' bounding box) no pixel of the mask is background (R 0 and G 0): count them."""
    R, Gc = m[..., 0], m[..., 1]
    res = {}
    ids = np.unique(Gc[(R == 1) | (R == 2)])
    for wid in ids:
        if wid == 0:
            continue
        sel = ((R == 1) | (R == 2)) & (Gc == wid)
        ys, xs = np.nonzero(sel)
        if len(xs) < MIN_PANE_PX:
            continue
        x0, x1, y0, y1 = xs.min(), xs.max(), ys.min(), ys.max()
        box = (R[y0:y1 + 1, x0:x1 + 1] == 0) & (Gc[y0:y1 + 1, x0:x1 + 1] == 0)
        res[int(wid)] = int(box.sum())
    return res
