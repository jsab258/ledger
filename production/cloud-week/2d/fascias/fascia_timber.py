"""The empty unit's bare timber, try 2 (unit 4.1, cloud week 42).

Try 1 drew it as 18,000 scale-shaped flecks packed edge to edge: crazy paving, not wood. It is wood: soot-dark planks (the target's palette:
"paint long gone: dark soot-grimed timber with a few patches of old paint", ground 46,37,30, grain strong, amplitude 3 L*) with the grain as the
main feature: long dark grain lines that flow round a few knots, hair-fine checks and splits along the length, the seams between the three
planks the board is made of, the nail holes. Where the soot has weathered off the exposed lower half the timber shows silver and open-grained (those
strips are the target's 17 per cent `loss`, drawn along the grain by fascia_age.loss_alpha). A handful of islands of the last owner's paint
survive (10 to 30 of them, each 50 to 400 mm long along the grain), mostly in the sheltered upper half and round nail heads.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc
from fascia_common import H_MM, W_MM

OLD_PAINT = np.array([84.0, 82.0, 68.0], np.float32)       # a dull green, the last owner's: far from the silvered timber and from the soot
SILVER = np.array([112.0, 100.0, 86.0], np.float32)
SILVER_CORE = np.array([98.0, 86.0, 72.0], np.float32)


def _warp(n0, B, key, amp, sx, sy):
    dy = amp * fc.fnoise(n0.shape, sx, sy, B.rng("timber", key))
    rows = np.arange(n0.shape[0], dtype=np.float32)[:, None] + dy
    cols = np.broadcast_to(np.arange(n0.shape[1], dtype=np.float32)[None, :], n0.shape)
    return ndi.map_coordinates(n0, [np.clip(rows, 0, n0.shape[0] - 1), cols], order=1, mode="nearest")


def plank_seams(H, rng):
    """y (from the top, mm) of the two seams between the three planks"""
    return [float(rng.uniform(158, 182)), float(rng.uniform(348, 372))]


def paint_bare_timber(B, T, s):
    """the soot-dark planked timber, the grain, knots, checks. Returns a dict of what was drawn."""
    H, W = B.H, B.W
    rng = B.rng("timber", "layout")
    base = fc.pal(T, s["ground"]["colour"])
    amp = s["ground"]["grain"]["amp_L"]
    seams = plank_seams(H, rng)
    edges = [0.0] + seams + [float(H)]
    L0 = float(fc.lab(base)[0])
    # the grain: hair fibres, bands of late-wood and a broad flowing figure, all warped so the lines converge and part like real boards do
    g1 = _warp(fc.fnoise((H, W), 520, 1.1, B.rng("timber", "g1")), B, "w1", 9.0, 650, 34)
    g2 = _warp(fc.fnoise((H, W), 260, 2.4, B.rng("timber", "g2")), B, "w2", 11.0, 500, 30)
    g3 = _warp(fc.fnoise((H, W), 700, 7.5, B.rng("timber", "g3")), B, "w3", 16.0, 800, 60)
    g4 = _warp(fc.fnoise((H, W), 90, 0.9, B.rng("timber", "g4")), B, "w4", 5.0, 400, 25)
    rows = np.arange(H, dtype=np.float32)[:, None]
    tone = np.zeros((H, 1), np.float32)
    pl_off = [float(rng.uniform(-2.4, 2.4)) for _ in range(3)]
    for i in range(3):
        tone[int(edges[i]):int(edges[i + 1])] = pl_off[i]
    t = 0.60 * g1 + 0.70 * g2 + 0.85 * g3 + 0.45 * g4
    t *= amp / max(1e-6, math.sqrt(0.60 ** 2 + 0.70 ** 2 + 0.85 ** 2 + 0.45 ** 2))
    t = t + tone * (amp / 3.0)
    f = 1.0 + 1.36 * t / max(L0, 8.0)
    # a plank is a little darker at its upper edge (the shadow of the plank above) and silvers toward its lower edge
    for i in range(3):
        a, b = int(edges[i]), int(edges[i + 1])
        prof = np.linspace(-1.0, 1.0, b - a, dtype=np.float32)[:, None]
        f[a:b] *= (1.0 + 0.05 * prof)
    rgb = np.clip(base[None, None, :] * f[..., None], 0, 255)
    # dark grain lines: the hard late-wood of the grain
    dl = np.clip((-g2 - 0.7) / 0.9, 0, 1) * 0.55 + np.clip((-g4 - 1.0) / 0.9, 0, 1) * 0.30 + np.clip((-g1 - 1.1) / 1.0, 0, 1) * 0.35
    dl = np.clip(dl, 0, 1)
    rgb *= (1.0 - 0.34 * dl)[..., None]
    B.rgb[:] = rgb
    B.rough[:] = np.clip(0.85 + 0.04 * g2, 0.55, 1.0)
    B.metal[:] = 0.0
    B.height[:] = (0.05 * g2 - 0.18 * dl + 0.015 * B.noise("fine")).astype(np.float32)
    B.layers["timber_dl"] = dl.astype(np.float32)
    # knots
    knots = []
    for k in range(int(rng.integers(3, 6))):
        for _ in range(40):
            x = float(rng.uniform(220, W - 220))
            pl = int(rng.integers(0, 3))
            y = float(rng.uniform(edges[pl] + 36, edges[pl + 1] - 36))
            if all(abs(x - kx) > 400 for kx, _, _, _ in knots):
                knots.append((x, y, float(rng.uniform(15, 30)), float(rng.uniform(8, 15))))
                break
    for (kx, ky, a_, b_) in knots:
        r0, r1, c0, c1 = max(0, int(ky - 5 * b_)), min(H, int(ky + 5 * b_)), max(0, int(kx - 4 * a_)), min(W, int(kx + 4 * a_))
        yy, xx = np.mgrid[r0:r1, c0:c1].astype(np.float32)
        d = np.sqrt(((xx - kx) / a_) ** 2 + ((yy - ky) / b_) ** 2)
        rings = 0.5 + 0.5 * np.cos(d * 2 * math.pi * 1.6)
        env = np.clip(1.0 - (d - 1.0) / 2.4, 0, 1)
        core = np.clip(1.2 - d, 0, 1)
        dark = np.clip(0.50 * env * rings + 0.55 * core, 0, 0.85)
        B.rgb[r0:r1, c0:c1] *= (1.0 - dark)[..., None]
        B.height[r0:r1, c0:c1] -= (0.2 * core).astype(np.float32)
        # the grain flows round it: a lighter halo above and below
        hal = np.clip(1.0 - np.abs(d - 1.9) / 0.7, 0, 1) * 0.08
        B.rgb[r0:r1, c0:c1] *= (1.0 + hal)[..., None]
    return dict(seams_from_top_mm=[round(v, 1) for v in seams], knots=[[round(x), round(H - y), round(a)] for x, y, a, _ in knots], plank_edges=edges)


def draw_seams(B, seams, strength=0.9):
    """the joints between the planks: a 3 mm dark groove with a thin light arris under it (and the paint cracked along it)"""
    H, W = B.H, B.W
    rng = B.rng("timber", "seams")
    cols = np.arange(W, dtype=np.float32)
    for y in seams:
        wob = fc.fnoise((1, W), 160, 0.01, rng)[0] * 1.6 + fc.fnoise((1, W), 20, 0.01, rng)[0] * 0.5
        yy = (y + wob)[None, :]
        rws = (np.arange(H, dtype=np.float32) + 0.5)[:, None]
        d = rws - yy
        groove = np.clip(1.0 - np.abs(d + 0.0) / 1.9, 0, 1)
        arris = np.clip(1.0 - np.abs(d - 3.0) / 1.2, 0, 1)
        shade = np.clip(1.0 - np.abs(d + 4.5) / 2.2, 0, 1)
        col = np.array([7.0, 5.0, 4.0], np.float32)
        B.rgb += (col[None, None, :] - B.rgb) * (strength * groove)[..., None]
        B.rgb *= (1.0 + 0.10 * arris - 0.12 * shade)[..., None]
        B.height -= (0.55 * groove).astype(np.float32)
        B.height += (0.06 * arris).astype(np.float32)


def place_islands(B, avoid, rng, n_range=(14, 24)):
    """the islands of old paint that survive: elongated along the grain, ragged, mostly in the sheltered upper half and near the ends and nails.
    Returns the alpha plane and the list of boxes (x0, y0, x1, y1 in board mm, y up)."""
    H, W = B.H, B.W
    alpha = np.zeros((H, W), np.float32)
    boxes = []
    n = int(rng.integers(*n_range))
    bank = fc.fnoise((260, 600), 3.2, 1.6, rng)
    for i in range(n):
        for _ in range(80):
            L = float(np.clip(rng.lognormal(math.log(150), 0.55), 55, 400))
            Wd = float(np.clip(L * rng.uniform(0.10, 0.28), 11, 62))
            x = float(rng.uniform(40, W - 40 - L))
            # sheltered: weight toward the upper 55 per cent of the board
            yfrac = float(np.clip(rng.beta(2.0, 3.2), 0.05, 0.95))
            y = 28 + yfrac * (H - 56 - Wd)
            r0, r1, c0, c1 = int(y), int(y + Wd) + 1, int(x), int(x + L) + 1
            if r1 > H - 24 or r0 < 24 or c1 > W - 24:
                continue
            if avoid[max(0, r0 - 6):r1 + 6, max(0, c0 - 6):c1 + 6].any():
                continue
            if alpha[max(0, r0 - 14):r1 + 14, max(0, c0 - 20):c1 + 20].max() > 0.3:
                continue
            yy, xx = np.mgrid[r0:r1, c0:c1].astype(np.float32)
            cx, cy = x + L / 2, y + Wd / 2
            d = np.sqrt(((xx - cx) / (L / 2.0)) ** 2 + ((yy - cy) / (Wd / 2.0)) ** 2)
            oy, ox = int(rng.integers(0, 260 - (r1 - r0))), int(rng.integers(0, 600 - (c1 - c0)))
            d = d + 0.28 * bank[oy:oy + (r1 - r0), ox:ox + (c1 - c0)] + 0.10 * np.sin(xx / 17.0 + i)
            m = d < 1.0
            if m.sum() < 60:
                continue
            a = np.clip((1.0 - d) * min(Wd / 2.0, 7.0), 0, 1) * m
            alpha[r0:r1, c0:c1] = np.maximum(alpha[r0:r1, c0:c1], a.astype(np.float32))
            boxes.append((round(x), round(H - (y + Wd)), round(x + L), round(H - y)))
            break
    return alpha, boxes


def apply_islands(B, alpha):
    sel = alpha > 0.002
    if not sel.any():
        return
    col = OLD_PAINT[None, :] * (1.0 + 0.06 * B.noise("iso")[sel][:, None] + 0.05 * B.noise("fine")[sel][:, None])
    # the old paint is chalky grey-green and carries the grain through it
    col = col * (1.0 + 0.10 * B.noise("streak")[sel][:, None])
    a = np.clip(alpha[sel], 0, 1)[:, None]
    B.rgb[sel] = B.rgb[sel] + (col - B.rgb[sel]) * a
    B.rough[sel] = B.rough[sel] + (0.62 - B.rough[sel]) * alpha[sel]
    B.height[sel] += (0.14 * alpha[sel]).astype(np.float32)
