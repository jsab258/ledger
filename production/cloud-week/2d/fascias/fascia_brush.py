"""Brushed whitewash lettering and the cloth-laid whitewash of a window (unit 4.1, try 2).

Try 1 filled the clean outlines of a monoline hand font with isotropic grey blotches ("a felt-tip font with a stone texture"). Whitewash lettering is
laid with a flat brush or a finger: strokes run thick to thin with the brush's angle, a loaded blob stands where each stroke starts, the stroke ends in a
dry-brush tail of hair streaks, the edges are uneven, a heavy stroke now and then runs a drip, and every letter is a little different (size, slant, set).

The letters are still Patrick Hand's (the target's font for the fishmonger's glass): each letter is drawn from the font's own centre line, so the word, the
letter shapes and the positions are the font's, and the BRUSH is what is laid along that line. The centre line is found by thinning the glyph (Zhang-Suen);
the width along it is the font's own stroke width, scaled by the brush's angle to the stroke, by a slow pressure wave, by the loaded start and the dry tail.
Everything is drawn from the generator it is given: the same seed gives the same pixels.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc

SS = 3


def thin(mask):
    """Zhang-Suen thinning of a bool image: a one-pixel centre line"""
    img = mask.astype(np.uint8).copy()
    changed = True
    while changed:
        changed = False
        for step in (0, 1):
            P = np.pad(img, 1)
            p2, p3, p4, p5 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:], P[2:, 2:]
            p6, p7, p8, p9 = P[2:, 1:-1], P[2:, :-2], P[1:-1, :-2], P[:-2, :-2]
            Bn = p2.astype(np.int16) + p3 + p4 + p5 + p6 + p7 + p8 + p9
            seq = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            A = np.zeros_like(img, dtype=np.int16)
            for i in range(8):
                A += ((seq[i] == 0) & (seq[i + 1] == 1))
            if step == 0:
                c = ((p2 * p4 * p6) == 0) & ((p4 * p6 * p8) == 0)
            else:
                c = ((p2 * p4 * p8) == 0) & ((p2 * p6 * p8) == 0)
            m = (img == 1) & (Bn >= 2) & (Bn <= 6) & (A == 1) & c
            if m.any():
                img[m] = 0
                changed = True
    return img.astype(bool)


def endpoints(sk):
    P = np.pad(sk.astype(np.uint8), 1)
    nb = (P[:-2, :-2].astype(np.int16) + P[:-2, 1:-1] + P[:-2, 2:] + P[1:-1, :-2] + P[1:-1, 2:] + P[2:, :-2] + P[2:, 1:-1] + P[2:, 2:])
    return sk & (nb == 1)


def draw_glyph_brush(g_mask, rng, brush_deg=18.0, start_blob=1.38, tail_mm=15.0, ss=SS, monoline=False):
    """one glyph (a bool mask at ss times 1 px/mm, monoline) re-drawn as brush strokes along its centre line.
    Returns (alpha at ss, direction angle at every pixel in radians (stroke direction), tail-factor map) all at ss."""
    h, w = g_mask.shape
    sk = thin(g_mask)
    if not sk.any():
        return g_mask.astype(np.float32), None
    dt = ndi.distance_transform_edt(g_mask)
    # stroke direction at every pixel, from the structure tensor of the smoothed mask
    sm = ndi.gaussian_filter(g_mask.astype(np.float32), 2.2 * ss / 3.0)
    gy, gx = np.gradient(sm)
    sig = 5.0 * ss / 3.0
    jxx = ndi.gaussian_filter(gx * gx, sig)
    jyy = ndi.gaussian_filter(gy * gy, sig)
    jxy = ndi.gaussian_filter(gx * gy, sig)
    th_grad = 0.5 * np.arctan2(2 * jxy, jxx - jyy)          # dominant gradient direction
    th = th_grad + math.pi / 2.0                              # the stroke runs across the gradient
    ys, xs = np.where(sk)
    half = dt[ys, xs]
    ang = th[ys, xs]
    # the brush's flat edge is held at brush_deg from the horizontal: a stroke along it is thin, across it thick
    rel = ang - math.radians(brush_deg)
    gfac = (0.78 + 0.70 * np.abs(np.sin(rel))) if not monoline else np.full(rel.shape, 0.92)
    # pressure: slow, along the line (taken from a smooth field of position)
    pr = 1.0 + 0.10 * np.sin(xs / (22.0 * ss / 3.0) + rng.uniform(0, 6.28)) + 0.07 * np.sin(ys / (15.0 * ss / 3.0) + rng.uniform(0, 6.28))
    # starts and tails: the end points of the line, the upper/left one is where the brush came down
    ep = endpoints(sk)
    ey, ex = np.where(ep)
    start = np.zeros_like(sk)
    tail = np.zeros_like(sk)
    for y, x in zip(ey, ex):
        # a stroke starts at its upper end (or its left end if it lies flat)
        a = th[y, x]
        horiz = abs(math.cos(a)) > 0.7
        # find the other end of this stroke approximately: whichever side the line runs to
        ny, nx = np.where(sk[max(0, y - 14 * ss // 3):y + 14 * ss // 3 + 1, max(0, x - 14 * ss // 3):x + 14 * ss // 3 + 1])
        if len(ny) == 0:
            continue
        cy = ny.mean() + max(0, y - 14 * ss // 3) - y
        cx = nx.mean() + max(0, x - 14 * ss // 3) - x
        # (cx, cy) points from the end into the stroke
        if horiz:
            is_start = cx > 0              # the line continues to the right: this is the left end
        else:
            is_start = cy > 0              # the line continues downward: this is the top end
        (start if is_start else tail)[y, x] = True
    d_start = ndi.distance_transform_edt(~start) if start.any() else np.full(sk.shape, 1e3)
    d_tail = ndi.distance_transform_edt(~tail) if tail.any() else np.full(sk.shape, 1e3)
    blob = 1.0 + (start_blob - 1.0) * np.clip(1.0 - d_start[ys, xs] / (8.0 * ss), 0, 1)
    tl = tail_mm * ss
    taper = (0.45 + 0.55 * np.clip(d_tail[ys, xs] / tl, 0, 1)) if not monoline else np.ones_like(blob)
    rad = half * gfac * pr * blob * taper
    rad = np.maximum(rad, 1.3 * ss / 3.0)
    # rasterise: a disc at every centre-line pixel
    img = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(img)
    for x, y, r in zip(xs, ys, rad):
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    alpha = np.asarray(img, np.float32) / 255.0
    tailf = np.clip(d_tail / tl, 0, 1)
    tailf[np.isinf(tailf)] = 1.0
    return alpha, (th, tailf, sk, dt)


def brush_text(T, text, font_key, cap_mm, W, H, baseline_mm, x_centre, rng, weight=400, tracking_em=0.04, slant=0.10, whitewash_alpha=0.88, monoline=False):
    """the string as brushed whitewash on a W x H tile (row 0 the top; baseline_mm up from the bottom). Returns (alpha float32 HxW at 1x, info)."""
    cr = fc.cap_ratio(T, font_key, weight)
    px = cap_mm / cr
    f1 = fc.font_for(T, font_key, weight, px)
    fS = fc.font_for(T, font_key, weight, px * SS)
    trk = tracking_em * px
    xs1 = fc.glyph_origins(f1, text, trk)
    total_w = xs1[-1] + f1.getlength(text[-1])
    x_left = x_centre - total_w / 2.0
    big = np.zeros((H * SS, W * SS), np.float32)
    streak_dir = np.zeros((H * SS, W * SS), np.float32)
    tailmap = np.ones((H * SS, W * SS), np.float32)
    n = len(text)
    base_row = (H - 1 - baseline_mm) * SS
    glyph_info = []
    mpad = int(0.20 * px * SS) + 14
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        bb = fS.getbbox(ch, anchor="ls")
        l, t, r, bt = [int(v) for v in bb]
        gw, gh = r - l + 2 * mpad, bt - t + 2 * mpad
        g = Image.new("L", (gw, gh), 0)
        ImageDraw.Draw(g).text((mpad - l, mpad - t), ch, font=fS, fill=255, anchor="ls")
        ox, oy = mpad - l, mpad - t
        # every letter is its own: size, slant, turn, set and weight of hand
        sx = float(rng.uniform(0.94, 1.07))
        sy = float(rng.uniform(0.94, 1.07))
        shear = slant + float(rng.normal(0, 0.035))
        rot = float(rng.normal(0, 1.8))
        # affine about the glyph's baseline origin: x' = sx*x + shear*(baseline - y)*..., then a rotation
        # PIL's affine maps output coords to input coords; build output = M (input - origin) + origin and invert it
        cx_, cy_ = ox, oy
        # a positive shear leans the letter to the right: x_out = sx*dx - shear*dy (dy is negative above the baseline)
        M = np.array([[sx, -shear], [0.0, sy]], np.float64)
        th = math.radians(rot)
        Rm = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
        Mt = Rm @ M
        Minv = np.linalg.inv(Mt)
        c0 = np.array([cx_, cy_], np.float64) - Minv @ np.array([cx_, cy_], np.float64)
        coeffs = (Minv[0, 0], Minv[0, 1], c0[0], Minv[1, 0], Minv[1, 1], c0[1])
        gt = g.transform((gw, gh), Image.AFFINE, coeffs, resample=Image.BICUBIC)
        gm = np.asarray(gt) > 127
        alpha_g, aux = draw_glyph_brush(gm, rng, brush_deg=float(rng.normal(18, 6)), start_blob=float(rng.uniform(1.12, 1.32)) if not monoline else 1.0, tail_mm=float(rng.uniform(11, 20)), monoline=monoline)
        px_x = (x_left + xs1[i] + float(rng.normal(0, 1.2))) * SS
        px_y = base_row + float(rng.normal(0, 1.5)) * SS
        gx = int(round(px_x)) - ox
        gy = int(round(px_y)) - oy
        cx0, cy0 = max(0, gx), max(0, gy)
        cx1, cy1 = min(W * SS, gx + gw), min(H * SS, gy + gh)
        if cx1 <= cx0 or cy1 <= cy0:
            continue
        sub = alpha_g[cy0 - gy:cy1 - gy, cx0 - gx:cx1 - gx]
        big[cy0:cy1, cx0:cx1] = np.maximum(big[cy0:cy1, cx0:cx1], sub)
        if aux is not None:
            th_map, tailf, sk, dt = aux
            sd = th_map[cy0 - gy:cy1 - gy, cx0 - gx:cx1 - gx]
            tf = tailf[cy0 - gy:cy1 - gy, cx0 - gx:cx1 - gx]
            msk = sub > 0.5
            streak_dir[cy0:cy1, cx0:cx1] = np.where(msk, sd, streak_dir[cy0:cy1, cx0:cx1])
            tailmap[cy0:cy1, cx0:cx1] = np.where(msk, np.minimum(tf, tailmap[cy0:cy1, cx0:cx1]) if False else tf, tailmap[cy0:cy1, cx0:cx1])
        glyph_info.append(dict(ch=ch, sx=round(sx, 3), sy=round(sy, 3), shear=round(shear, 3), rot=round(rot, 2)))
    # down to 1x: a coverage with an uneven, wet edge
    cov = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).resize((W, H), Image.BOX), np.float32) / 255.0
    th1 = np.asarray(Image.fromarray(streak_dir).resize((W, H), Image.NEAREST), np.float32)
    tf1 = np.asarray(Image.fromarray(tailmap).resize((W, H), Image.BOX), np.float32)
    edge = fc.fnoise((H, W), 1.4, 1.4, rng)
    near = ndi.maximum_filter(cov, size=5) > 0.3
    cov = np.clip((cov - 0.5 + 0.16 * edge) * 3.2 + 0.5, 0, 1) * near
    # hair streaks along the stroke: the brush's bristles leave lines of thinner paint along the direction of the stroke
    nh = fc.fnoise((H, W), 22, 0.9, rng)
    nv = fc.fnoise((H, W), 0.9, 22, rng)
    c2 = np.cos(th1) ** 2
    s2 = np.sin(th1) ** 2
    streak = c2 * nh + s2 * nv
    op = whitewash_alpha + 0.06 * fc.fnoise((H, W), 9, 9, rng)
    a = cov * np.clip(op - (0.13 if not monoline else 0.03) * np.clip(streak, -0.5, 2.2), 0.45, 1.0)
    # the dry-brush tail: the paint breaks up into the hair streaks toward the end of a stroke
    dry = np.clip(tf1 * 1.2 + 0.55 * streak, 0, 1)
    if not monoline:
        a = a * np.where(tf1 < 0.999, np.clip(0.30 + 0.9 * dry, 0, 1), 1.0)
    # a run or two below a heavy stroke
    heavy = ndi.binary_erosion(cov > 0.6, iterations=4)
    ys, xs = np.where(heavy)
    n_runs = int(rng.integers(2, 5)) if not monoline else 0
    runs = []
    if len(ys):
        low = np.zeros_like(heavy)
        low[:-1] = heavy[:-1] & ~heavy[1:]
        yl, xl = np.where(low)
        for q in range(min(n_runs, len(yl))):
            k = int(rng.integers(len(yl)))
            x, y0 = int(xl[k]), int(yl[k]) + 2
            L = int(rng.uniform(14, 62))
            wr = float(rng.uniform(1.6, 3.0))
            if y0 + L + 4 >= H:
                continue
            for r in range(L):
                tq = r / L
                ww = max(0.7, wr * (1.0 - 0.45 * tq))
                cols = np.arange(int(x - 3), int(x + 4))
                prof = np.clip(1.0 - (np.abs(cols - x - 0.4 * math.sin(r / 9.0)) - ww / 2) / 1.0, 0, 1)
                a[y0 + r, cols] = np.maximum(a[y0 + r, cols], prof * (0.82 - 0.35 * tq))
            ee = np.clip(1.3 - np.sqrt((np.arange(H)[:, None] - (y0 + L)) ** 2 + (np.arange(W)[None, :] - x) ** 2) / 1.6, 0, 1)
            a = np.maximum(a, ee * 0.8)
            runs.append((x, y0, L))
    return a.astype(np.float32), dict(glyphs=glyph_info, runs=runs, ink_width_font_mm=round(total_w, 1))
