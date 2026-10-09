"""Wear: rain runs, gull marks, rust runs, paint loss, the repaint of ghosts (unit 4.1, cloud week 42).

The counts and sizes are each shop's `age` numbers; the SHAPE of paint loss is the target's P2 measure (median aspect 3.6,
median equivalent diameter 9 mm). Everything is placed by the board's seed with rejection sampling, so nothing touches a letter,
a rule or another mark, and the three mark layers can be counted by connected components (check G13).
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc
import fascia_paint as fp
from fascia_common import H_MM, W_MM

RUST = np.array([128.0, 66.0, 34.0])
RUST_EDGE = np.array([150.0, 100.0, 62.0])
CHALK_DUST = np.array([150.0, 147.0, 138.0])
GRIME_DARK = np.array([54.0, 50.0, 44.0])


def down_len(free):
    """for every pixel, how many free pixels run unbroken downward from it"""
    H, W = free.shape
    out = np.zeros((H, W), np.int32)
    run = np.zeros(W, np.int32)
    for r in range(H - 1, -1, -1):
        run = np.where(free[r], run + 1, 0)
        out[r] = run
    return out


def _dilate(m, r):
    return ndi.binary_dilation(m, structure=ndi.generate_binary_structure(2, 1), iterations=int(r))


def place_runs(B, free, count, len_rng, rng, light_ground):
    """vertical rain runs hanging from the top of a free stretch"""
    H, W = B.H, B.W
    layer = np.zeros((H, W), np.float32)
    placed = []
    f = free.copy()
    fw = ndi.binary_erosion(f, structure=np.ones((1, 17), bool))
    dl = down_len(fw)
    top = fw & ~np.roll(fw, 1, axis=0)
    top[0] = fw[0]
    ys, xs = np.where(top)
    if len(ys) == 0:
        return layer, placed
    for i in range(count):
        for _ in range(400):
            L = int(rng.uniform(*len_rng))
            k = int(rng.integers(len(ys)))
            r, c = int(ys[k]), int(xs[k])
            if dl[r, c] < L + 6:
                continue
            w = rng.uniform(5.0, 11.0)
            # a streak: gaussian across, fading along, a small sway
            rr = np.arange(L)
            sway = 1.4 * np.sin(2 * math.pi * (rr / rng.uniform(70, 160)) + rng.uniform(0, 6.28))
            a_len = np.clip(1.0 - (rr / L) ** 1.6, 0, 1) * (0.55 + 0.45 * np.clip(rr / 10.0, 0, 1))
            xx = np.arange(-int(w * 2) - 3, int(w * 2) + 4)
            prof = np.exp(-(xx / (w / 2.0)) ** 2)
            strip = a_len[:, None] * prof[None, :]
            cx = c + sway
            rowsel = r + rr
            cols = (np.round(cx).astype(int)[:, None] + xx[None, :])
            ok = (cols >= 0) & (cols < W)
            if not ok.all():
                continue
            layer[rowsel[:, None], cols] = np.maximum(layer[rowsel[:, None], cols], strip.astype(np.float32))
            placed.append((c, r, L, w))
            # keep every other mark away
            blk = np.zeros((H, W), bool)
            blk[max(0, r - 8):min(H, r + L + 8), max(0, c - int(w * 2) - 12):min(W, c + int(w * 2) + 13)] = True
            f &= ~blk
            fw = ndi.binary_erosion(f, structure=np.ones((1, 17), bool))
            dl = down_len(fw)
            top = fw & ~np.roll(fw, 1, axis=0)
            top[0] = fw[0]
            ys, xs = np.where(top)
            break
        if len(ys) == 0:
            break
    return layer, placed


def apply_runs(B, layer, light_ground=None):
    """rain runs: grime carried down a pale board darkens it; on a dark board (or dark patch) the dried run shows as a pale dust. Chosen by the local luminance."""
    a = np.clip(layer, 0, 1)
    m = a > 0.001
    if not m.any():
        return
    px = B.rgb[m]
    luma = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
    pale = luma > 105.0
    out = np.where(pale[:, None], px * 0.62 + GRIME_DARK[None, :] * 0.38, px * 0.50 + CHALK_DUST[None, :] * 0.50)
    k = np.where(pale, 0.62, 0.55) * a[m]
    B.rgb[m] = px + (out - px) * k[:, None]
    B.rough[m] = np.clip(B.rough[m] + 0.12 * a[m], 0, 1)


def place_gull(B, free, count, size_rng, rng):
    """gull droppings: an irregular off-white splash with a grey-brown ring, a few faint satellite specks and a thin drip or two from its lower rim.
    Returns the (core, halo) alpha planes; the core is ONE connected mark (what G13 counts), the specks live in the halo only."""
    H, W = B.H, B.W
    core = np.zeros((H, W), np.float32)
    halo = np.zeros((H, W), np.float32)
    placed = []
    f = free.copy()
    for i in range(count):
        ys_f = xs_f = None
        for _ in range(500):
            size = rng.uniform(*size_rng)
            R = int(size * 1.4 + 26)
            if ys_f is None:
                ys_f, xs_f = np.where(f)
            ys, xs = ys_f, xs_f
            if len(ys) == 0:
                return core, halo, placed
            k = int(rng.integers(len(ys)))
            cy, cx = int(ys[k]), int(xs[k])
            r0, r1 = cy - R, cy + R
            c0, c1 = cx - R, cx + R
            if r0 < 4 or c0 < 4 or r1 > H - 4 or c1 > W - 4:
                continue
            if not f[r0:r1, c0:c1].all():
                continue
            S4 = 4
            img = Image.new("L", (2 * R * S4, 2 * R * S4), 0)
            d = ImageDraw.Draw(img)
            ctr = R * S4
            # the splash: a lobed outline, wider than tall (it hit the board and ran a little)
            ph = rng.uniform(0, 6.28, 6)
            pts = []
            Rm = size * 0.5 * S4
            for t in np.linspace(0, 2 * math.pi, 96, endpoint=False):
                rr = Rm * (1.0 + 0.13 * math.sin(2 * t + ph[0]) + 0.11 * math.sin(3 * t + ph[1]) + 0.09 * math.sin(5 * t + ph[2])
                           + 0.07 * math.sin(7 * t + ph[3]) + 0.05 * math.sin(11 * t + ph[4]) + 0.04 * math.sin(17 * t + ph[5]))
                pts.append((ctr + rr * math.cos(t) * 1.22, ctr + rr * math.sin(t) * 0.82))
            d.polygon(pts, fill=255)
            # drips from the lower rim: tapering, fading
            drip = Image.new("L", (2 * R * S4, 2 * R * S4), 0)
            dd_ = ImageDraw.Draw(drip)
            for j in range(int(rng.integers(1, 3))):
                lx = ctr + rng.uniform(-0.45, 0.45) * Rm
                ln = rng.uniform(0.6, 1.3) * size * S4
                w0 = rng.uniform(2.6, 4.0) * S4
                y0_ = ctr + Rm * 0.55
                for q in range(int(ln)):
                    t = q / ln
                    wq = max(1.0, w0 * (1.0 - 0.7 * t))
                    val = int(255 * (1.0 - 0.75 * t))
                    dd_.line([(lx + 0.6 * math.sin(t * 5), y0_ + q), (lx + 0.6 * math.sin(t * 5), y0_ + q + 1)], fill=val, width=int(wq))
            dripa = ndi.gaussian_filter(np.asarray(drip.resize((2 * R, 2 * R), Image.BOX), np.float32) / 255.0, 1.1) * 1.25
            dripa = np.clip(dripa, 0, 1)
            a = np.asarray(img.resize((2 * R, 2 * R), Image.BOX), np.float32) / 255.0
            a = np.maximum(ndi.gaussian_filter(a, 0.7), dripa)
            if a.max() <= 0:
                continue
            # the ring and the faint specks round it
            sp = np.zeros_like(a)
            for j in range(int(rng.integers(3, 7))):
                ang = rng.uniform(0, 6.28)
                dist = rng.uniform(1.0, 1.5) * size * 0.5
                px_, py_ = R + math.cos(ang) * dist * 1.1, R + math.sin(ang) * dist * 0.9
                rr_ = rng.uniform(0.8, 1.8)
                yy, xx = np.ogrid[:2 * R, :2 * R]
                sp = np.maximum(sp, np.clip(rr_ + 0.5 - np.sqrt((yy - py_) ** 2 + (xx - px_) ** 2), 0, 1))
            h = np.clip(np.maximum(ndi.gaussian_filter(a, 2.4) * 1.7, sp * 0.8), 0, 1)
            core[r0:r1, c0:c1] = np.maximum(core[r0:r1, c0:c1], a)
            halo[r0:r1, c0:c1] = np.maximum(halo[r0:r1, c0:c1], h)
            placed.append((cx, cy, size))
            blk = np.zeros((H, W), bool)
            blk[max(0, cy - R - 14):cy + R + 14, max(0, cx - R - 14):cx + R + 14] = True
            f &= ~blk
            break
    return core, halo, placed


def apply_gull(B, core, halo):
    white = np.array([222.0, 218.0, 202.0])
    grey = np.array([168.0, 158.0, 136.0])
    h = np.clip(halo, 0, 1) * 0.62
    m = h > 0.002
    B.rgb[m] = B.rgb[m] + (grey[None, :] - B.rgb[m]) * h[m][:, None]
    mott = 0.90 + 0.035 * B.noise("fine") + 0.06 * B.noise("iso")
    c = np.clip(core, 0, 1) * np.clip(mott, 0.5, 1.0)
    m = c > 0.002
    B.rgb[m] = B.rgb[m] + (white[None, :] - B.rgb[m]) * c[m][:, None]
    B.rough = B.rough + (0.72 - B.rough) * np.clip(core, 0, 1) * 0.9
    B.height += 0.15 * np.clip(core, 0, 1)


def place_rust(B, heads, lens, rng, light_ground):
    """rust runs from given heads [(x, y_up)], each running down `len` mm; heads are drawn as small dark rusty rings"""
    H, W = B.H, B.W
    layer = np.zeros((H, W), np.float32)
    for (x, y), L in zip(heads, lens):
        r = H - int(y)
        L = int(L)
        rr = np.arange(L)
        w = rng.uniform(3.0, 4.6)
        sway = 0.8 * np.sin(2 * math.pi * rr / rng.uniform(40, 90) + rng.uniform(0, 6.28))
        a_len = 0.32 + 0.68 * np.clip(1.0 - rr / L, 0, 1) ** 1.2
        xx = np.arange(-8, 9)
        prof = np.exp(-(xx / (w / 2.0)) ** 2)
        cols = np.round(x + sway).astype(int)[:, None] + xx[None, :]
        rows = (r + rr)[:, None] + np.zeros_like(xx)[None, :]
        ok = (rows >= 0) & (rows < H) & (cols >= 0) & (cols < W)
        val = (a_len[:, None] * prof[None, :]).astype(np.float32)
        layer[rows[ok], cols[ok]] = np.maximum(layer[rows[ok], cols[ok]], val[ok])
        # the nail head
        rrh = np.arange(max(0, r - 5), min(H, r + 6))
        cch = np.arange(max(0, int(x) - 5), min(W, int(x) + 6))
        yy, xx2 = np.meshgrid(rrh, cch, indexing="ij")
        dd = np.sqrt((yy - r) ** 2 + (xx2 - x) ** 2)
        head = (np.clip(4.4 - dd, 0, 1) * (dd > 2.1)).astype(np.float32)          # a rusty ring: the nail hole's own black stays
        layer[yy, xx2] = np.maximum(layer[yy, xx2], head)
    return layer


def apply_rust(B, layer):
    a = np.clip(layer, 0, 1)
    k = 0.8 * a
    m = k > 0.002
    col = RUST[None, :] * (0.45 + 0.55 * np.clip(a[m], 0, 1)[:, None]) + RUST_EDGE[None, :] * (0.55 - 0.55 * np.clip(a[m], 0, 1)[:, None])
    B.rgb[m] = B.rgb[m] + (col - B.rgb[m]) * k[m][:, None]
    B.rough[m] = 0.8
    B.metal[m] = 0.0


def gather_free(B, blocks_mask, margin=10):
    """free pixels: inside the field, not blocked"""
    free = ~blocks_mask
    free[:margin, :] = False
    free[-margin:, :] = False
    free[:, :margin] = False
    free[:, -margin:] = False
    return free


def components(layer, thr=0.25, min_px=4):
    lab_, n = ndi.label(layer > thr)
    if n == 0:
        return 0, lab_
    sizes = ndi.sum(layer > thr, lab_, range(1, n + 1))
    keep = [i + 1 for i, s in enumerate(sizes) if s >= min_px]
    return len(keep), lab_
