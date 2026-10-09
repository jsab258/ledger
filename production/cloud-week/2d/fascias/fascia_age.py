"""Ageing, try 2 (unit 4.1, cloud week 42): how a painted board really fails, after the fresh review of try 1.

Try 1 laid one even speckle of 5 mm flakes, a stamp of one gull mark and a few pale scratch-like runs on every board. A real board fails
where water sits and runs and hands work it: the bottom rail and its drip, the board's ends and corners, the joints between its lengths, the
fixings, along the grain, under the cornice. The loss there is long strips along the grain that join into bare runs, heavy on some stretches
and nearly absent on others (the target's P2: 60 per cent of the lost paint lies in joined strips over 50 mm across, 28 per cent in strips over
200 mm, the largest 1000 mm long; plank to plank the loss varies 0.13 to 0.51). Grime builds up in the same places, and the lettering wears with
the ground, because it is paint on the same board.

The model here is one score field per board:  S = ln(damp weight) + long grain bands + grain strips + a ragged fine term.
The paint is gone where S is above a threshold chosen so that exactly the target's share of the free ground is lost (the target's
`loss_fraction`, read on the pixels by check_fascias.py); a second, higher threshold lets the bare wood show in the core of the big sheets.
Because the loss is a threshold of ONE smooth field it joins up where the field is high and thins out where it is low, in clusters of
every size, which is what P2 and the wear photographs show, and not an even confetti of equal ellipses.
Every draw comes from the board's seeded generators: the same seed gives the same pixels.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc

GRIME = np.array([84.0, 78.0, 70.0], np.float32)
DUST = np.array([178.0, 174.0, 162.0], np.float32)

# where each board's paint lets go: (amplitude, decay mm) of the damp weight along the bottom rail, the top (the cornice drip),
# the ends, a joint and a fixing; `base` is the weight of the open middle; `cluster` scales the long bands (more = more uneven);
# `sheet` is the share of the loss that is bare wood in the core of the big sheets; `crack` the density of cracks along the grain.
MODES = {
    # Mickey's: sound, chalky slate eggshell; a little loss at the foot and the left end (the quay side), almost no cracks
    "mickeys": dict(bottom=(3.4, 52), top=(0.8, 28), ends=(2.2, 210), joint=(2.0, 40), nail=(1.1, 22), base=0.34, cluster=1.0, core=0.30, crack=0.06, plank=0.9),
    # the fish market: white gloss gone crazed, chipped hard along its foot; fine cracks along the grain
    "fish_market": dict(bottom=(5.2, 46), top=(1.0, 26), ends=(1.4, 190), joint=(2.0, 38), nail=(1.0, 22), base=0.24, cluster=1.0, core=0.38, crack=0.50, plank=1.0),
    # Rita's: oil gloss, now satin: little, at the ends and the foot
    "ritas": dict(bottom=(3.0, 50), top=(0.7, 26), ends=(2.8, 230), joint=(1.8, 36), nail=(1.0, 22), base=0.28, cluster=0.9, core=0.28, crack=0.18, plank=0.9),
    # the ironmonger's buff gloss, chalked and grimy: along the planks, round the nails at its left end
    "ironmonger": dict(bottom=(3.4, 56), top=(1.2, 30), ends=(2.4, 240), joint=(2.4, 44), nail=(1.5, 26), base=0.32, cluster=1.1, core=0.34, crack=0.30, plank=1.1),
    # the chandler's navy gloss, salt-weathered: lets go at its ends in big sheets, and along the foot
    "chandler": dict(bottom=(3.4, 56), top=(1.0, 28), ends=(3.4, 280), joint=(2.2, 44), nail=(1.2, 24), base=0.26, cluster=1.15, core=0.40, crack=0.22, plank=1.0),
    # the old board round a lit box or a flat panel: the ring only; chalked cream timber that has lost paint at its foot and ends
    "ring": dict(bottom=(3.4, 24), top=(1.0, 14), ends=(2.8, 90), joint=(1.0, 30), nail=(0.8, 20), base=0.35, cluster=0.8, core=0.30, crack=0.10, plank=0.8),
    # a hanging board, a letting board: its foot and corners, the chain eyes; weathered from every side
    "hanging": dict(bottom=(3.6, 34), top=(1.4, 16), ends=(3.2, 40), joint=(0.0, 20), nail=(1.0, 16), base=0.30, cluster=0.8, core=0.30, crack=0.15, plank=0.8),
}


# ------------------------------------------------------------------ noise
def band_noise(H, W, rng, sx, sy):
    return fc.fnoise((H, W), sx, sy, rng)


class Fields:
    """the multi-scale noise one board's loss, grime and cracks are made of (a field is made once). `grain` = (sx, sy) of the strips along the grain,
    `long` of the long bands, `mid` of the damp zones: the bare timber's silvered strips are fatter and longer than a paint flake."""

    def __init__(self, B, scale=1.0, mid=(240, 15), long=(105, 3.0), strip=(26, 1.9)):
        self.B = B
        self.H, self.W = B.H, B.W
        self.scale = scale
        self.par = dict(mid=mid, long=long, strip=strip)
        self._f = {}

    def get(self, key, sx, sy):
        if key not in self._f:
            self._f[key] = band_noise(self.H, self.W, self.B.rng("age", key), max(sx, 0.6), max(sy, 0.6))
        return self._f[key]

    def mid(self):
        sx, sy = self.par["mid"]
        return self.get("mid", sx * self.scale, sy * max(self.scale, 0.6))

    def long(self):
        sx, sy = self.par["long"]
        return self.get("long", sx * self.scale, sy)

    def strip(self):
        sx, sy = self.par["strip"]
        return self.get("strip", sx * self.scale, sy)

    def fine(self):
        return self.get("fine", 4.2, 1.0)

    def iso(self):
        return self.get("iso", 6.0, 6.0)


# ------------------------------------------------------------------ the damp weights
def fixings(W, rng, lo=520, hi=900):
    """x of the nails along an edge, spaced like a carpenter's, a little irregular"""
    xs = []
    x = float(rng.uniform(150, 420))
    while x < W - 120:
        xs.append(x)
        x += float(rng.uniform(lo, hi))
    return xs


def joint_positions(W, avoid_x, rng, n=2, lo=0.26, hi=0.76, clear=70):
    """x of the butt joints between the lengths a long board is made of, away from every block (a joint never splits a letter)"""
    out = []
    targets = np.linspace(lo, hi, n) if n > 1 else [0.5]
    for tfrac in targets:
        best = None
        for _ in range(60):
            x = (tfrac + float(rng.uniform(-0.07, 0.07))) * W
            if all(not (a - clear <= x <= b + clear) for a, b in avoid_x) and all(abs(x - o) > 900 for o in out):
                best = x
                break
        if best is not None:
            out.append(best)
    return sorted(out)


def damp_weight(H, W, mode, joints, nails_top, nails_bot, top_y=None, bot_y=None):
    """the weight of the paint failing at every point: higher where water sits"""
    rows = (np.arange(H, dtype=np.float32) + 0.5)[:, None]
    cols = (np.arange(W, dtype=np.float32) + 0.5)[None, :]
    d_top = rows - (0 if top_y is None else top_y)
    d_bot = (H - rows) - (0 if bot_y is None else bot_y)
    d_top = np.maximum(d_top, 0.0)
    d_bot = np.maximum(d_bot, 0.0)
    d_end = np.minimum(cols, W - cols)
    ab, sb = mode["bottom"]
    at, st = mode["top"]
    ae, se = mode["ends"]
    aj, sj = mode["joint"]
    an, sn = mode["nail"]
    w = mode["base"] + ab * np.exp(-d_bot / sb) + at * np.exp(-d_top / st) + ae * np.exp(-d_end / se)
    w = w.astype(np.float32)
    for xj in joints:
        w += (aj * np.exp(-np.abs(cols - xj) / sj)).astype(np.float32)
    # nails: a round halo where the paint cracks round the head (upper row 33 mm down, lower row 33 mm up)
    for xs, row_y in ((nails_top, 33.0), (nails_bot, H - 33.0)):
        for xn in xs:
            c0, c1 = int(max(0, xn - 5 * sn)), int(min(W, xn + 5 * sn))
            r0, r1 = int(max(0, row_y - 5 * sn)), int(min(H, row_y + 5 * sn))
            if c1 <= c0 or r1 <= r0:
                continue
            yy = rows[r0:r1]
            xx = cols[:, c0:c1]
            w[r0:r1, c0:c1] += (an * np.exp(-((xx - xn) ** 2 + (yy - row_y) ** 2) / (2.0 * sn * sn))).astype(np.float32)
    return w


# ------------------------------------------------------------------ the loss
def loss_alpha(F, weight, allowed, calib, frac, mode, min_px=8):
    """alpha planes (older coat, bare wood) of the paint lost; the older coat covers exactly `frac` of the whole board in the calibration zone"""
    H, W = F.H, F.W
    S = (np.log(np.maximum(weight, 1e-3)) + 1.15 * mode["cluster"] * F.mid() + 0.95 * F.long() + 0.70 * F.strip() + 0.34 * F.fine() + 0.32 * F.iso()).astype(np.float32)
    zone = calib & allowed
    n_zone = int(zone.sum())
    target = frac * H * W
    if frac <= 0 or n_zone == 0:
        return np.zeros((H, W), np.float32), np.zeros((H, W), np.float32), S, None
    q = 1.0 - min(0.95, target / n_zone)
    t1 = float(np.quantile(S[zone], q))
    # settle the threshold so the connected marks of fewer than min_px pixels (which the check does not count) are not part of the share
    for _ in range(3):
        m = (S > t1) & allowed
        lbl, n = ndi.label(m)
        if n:
            sizes = ndi.sum(m, lbl, np.arange(1, n + 1))
            small = np.zeros(n + 1, bool)
            small[1:] = sizes < min_px
            m &= ~small[lbl]
        got = float((m & zone).sum())
        if got <= 0:
            break
        # the whole of what is lost in the zone should equal the target
        qq = np.clip(q + (got - target) / n_zone, 0.0, 0.999)
        if abs(got - target) / max(target, 1.0) < 0.02:
            break
        q = float(qq)
        t1 = float(np.quantile(S[zone], q))
    m = (S > t1) & allowed
    lbl, n = ndi.label(m)
    if n:
        sizes = ndi.sum(m, lbl, np.arange(1, n + 1))
        small = np.zeros(n + 1, bool)
        small[1:] = sizes < min_px
        m &= ~small[lbl]
    a1 = np.clip((S - t1) / 0.16 + 0.5, 0.0, 1.0).astype(np.float32) * ndi.binary_dilation(m, iterations=1)
    a1 *= allowed
    inside = m & zone
    t2 = float(np.quantile(S[inside], 1.0 - mode["core"])) if inside.any() else t1 + 9.0
    a2 = np.clip((S - t2) / 0.14 + 0.5, 0.0, 1.0).astype(np.float32) * (a1 > 0.01)
    return a1, a2, S, dict(t1=t1, t2=t2)


def apply_loss(B, a1, a2, prim, wood, relief=(-0.30, -0.50), rim=True, tex=None):
    """show the older coat, then bare wood, where the paint is gone; dirt collects in the edge of every flake, the lip of the paint stands a little proud"""
    rgb, rough, metal, height = B.rgb, B.rough, B.metal, B.height
    sel = a1 > 0.002
    if not sel.any():
        return
    fine = B.noise("fine")
    iso = B.noise("iso")
    sub_col = prim[None, :] * (1.0 + 0.035 * fine[sel][:, None] + 0.045 * iso[sel][:, None])
    wood_col = wood[None, :] * (1.0 + 0.05 * fine[sel][:, None] + 0.06 * iso[sel][:, None])
    k2 = a2[sel][:, None]
    col = sub_col * (1 - k2) + wood_col * k2
    if tex is not None:
        col = col * tex[sel][:, None]
    a = a1[sel][:, None]
    rgb[sel] = rgb[sel] + (col - rgb[sel]) * a
    r_t = 0.85
    rough[sel] = rough[sel] + (r_t - rough[sel]) * a1[sel]
    metal[sel] = metal[sel] * (1 - a1[sel])
    h_t = relief[0] * (1 - a2[sel]) + relief[1] * a2[sel]
    height[sel] = height[sel] + (h_t - height[sel]) * a1[sel]
    if rim:
        # a thin dark edge (trapped dirt) just inside every flake and a raised lip of paint just outside it
        m = a1 > 0.5
        er = ndi.binary_erosion(m, iterations=2)
        edge_in = m & ~er
        dil = ndi.binary_dilation(m, iterations=2) & ~m
        e_soft = ndi.gaussian_filter(edge_in.astype(np.float32), 0.8)
        rgb *= (1.0 - 0.22 * np.clip(e_soft, 0, 1))[..., None]
        lip = ndi.gaussian_filter(dil.astype(np.float32), 0.8)
        height += (0.10 * np.clip(lip, 0, 1)).astype(np.float32)


# ------------------------------------------------------------------ grime that builds up where the paint is damp
def grime_film(B, spec_mode, age, joints, amp=1.0, tops=True, modulation=0.30):
    """a film of grime, darker down the lower edge, at the ends, under the cornice and round the joints, broken by the grain (zero-mean on the board,
    so the ground's aged median -- the target's palette, which already holds the grime film -- is kept)"""
    H, W = B.H, B.W
    rows = (np.arange(H, dtype=np.float32) + 0.5)[:, None]
    cols = (np.arange(W, dtype=np.float32) + 0.5)[None, :]
    d_top, d_bot = rows, H - rows
    d_end = np.minimum(cols, W - cols)
    ab, sb = spec_mode["bottom"]
    f = 0.80 * np.exp(-d_bot / (sb * 1.8)) * (1.0 + 0.25 * ab) + (0.30 if tops else 0.0) * np.exp(-d_top / 38.0) + 0.65 * np.exp(-d_end / 220.0)
    for xj in joints:
        f = f + 0.18 * np.exp(-np.abs(cols - xj) / 22.0)
    n = B.rng("age", "grime-n")
    band = fc.fnoise((H, W), 160 * max(W / 5410.0, 0.15), 6.0, n)
    f = f * np.clip(1.0 - 0.25 * modulation / 0.30 + modulation * band, 0.2, 1.5)
    f = f.astype(np.float32)
    f = f - float(f.mean())
    k = age["grime_film"] * 3.0 * amp
    # grime darkens: down the lower edge, at the ends, under the cornice and round the joints; elsewhere the board is a shade cleaner (zero-mean: the ground's aged median,
    # which the target's palette already holds, is kept). Darker on every board, pale or dark: a film of soot and road spray, not a tint.
    # a pale ground takes less: a cream board darkened by a quarter turns the colour of the older coat under it (and of bare wood), which is not dirt but loss
    Lg = float(fc.lab(B.rgb[::8, ::8].reshape(-1, 3).mean(axis=0))[0])
    cap = 0.26 - 0.08 * float(np.clip((Lg - 50.0) / 20.0, 0.0, 1.0))
    k = k * (1.0 + 0.9 * float(np.clip((42.0 - Lg) / 17.0, 0.0, 1.0)))           # on a dark ground the same film shows half as much in L*: the soot of a navy or a green board is built a little heavier
    fac = np.where(f > 0, 1.0 - np.minimum(0.9 * k * f, cap), 1.0 + np.minimum(0.5 * k * (-f), 0.08)).astype(np.float32)
    B.rgb *= fac[..., None]
    np.clip(B.rgb, 0, 255, out=B.rgb)


# ------------------------------------------------------------------ cracks along the grain, joints
def cracks(B, density, allowed, weight=None, rng_key="crack", prim=None, dark_board=False, strength=0.5):
    """cracks along the grain: long hair-fine lines that wander a fraction of a millimetre, start and stop in the paint, now and then fork; more of them where the
    board is damp (the weight), and a few very short ones across the grain. `density` is the number per metre of board length at the foot."""
    if density <= 0:
        return None
    H, W = B.H, B.W
    rng = B.rng("age", rng_key)
    S = 3
    img = Image.new("L", (W * S // 2, H * S // 2), 0)          # half-size canvas at 3x of that: 1.5 px per mm
    k = S / 2.0
    d = ImageDraw.Draw(img)
    n = int(density * W / 1000.0 * 70)
    if weight is not None:
        rowp = weight.mean(axis=1) ** 1.3
        rowp = rowp / rowp.sum()
    else:
        rowp = np.full(H, 1.0 / H)
    for i in range(n):
        y = float(rng.choice(H, p=rowp)) + float(rng.uniform(-0.5, 0.5))
        x = float(rng.uniform(10, W - 10))
        L = float(np.clip(rng.lognormal(math.log(70), 0.75), 20, 520))
        dy = 0.0
        dirx = 1.0 if rng.random() < 0.5 else -1.0
        step = 6.0
        pts = [(x, y)]
        drift = float(rng.normal(0, 0.012))
        cx, cy = x, y
        for q in range(int(L / step)):
            dy += rng.normal(0, 0.10) + drift
            dy = float(np.clip(dy, -0.30, 0.30))
            cx += dirx * step
            cy += dy * step * 0.45
            if cx < 6 or cx > W - 6 or cy < 6 or cy > H - 6:
                break
            pts.append((cx, cy))
            if rng.random() < 0.035:                        # a fork
                ang = rng.choice([-1.0, 1.0]) * rng.uniform(0.25, 0.6)
                fl = float(rng.uniform(10, 45))
                d.line([(cx * k, cy * k), ((cx + dirx * fl * math.cos(ang)) * k, (cy + fl * math.sin(ang)) * k)], fill=int(rng.uniform(110, 190)), width=1)
        if len(pts) >= 2:
            a = int(rng.uniform(120, 230))
            d.line([(px * k, py * k) for px, py in pts], fill=a, width=1)
    lines = np.asarray(img.resize((W, H), Image.BOX), np.float32) / 255.0
    lines = np.clip(lines * 3.2, 0, 1) * allowed
    # the cracks are part of the paint: they fade where the paint is thin
    lines = ndi.gaussian_filter(lines, 0.35)
    if dark_board:
        col = (prim if prim is not None else np.array([138.0, 134.0, 126.0]))
        B.rgb += (col[None, None, :] - B.rgb) * (strength * 0.50 * lines)[..., None]
    else:
        col = np.array([54.0, 48.0, 42.0], np.float32)
        B.rgb += (col[None, None, :] - B.rgb) * (strength * lines)[..., None]
    B.height -= (0.12 * lines).astype(np.float32)
    return lines


def draw_joints(B, xs, dark_board=False):
    """a butt joint between two lengths: a hair-fine dark groove, 2 mm, a hair of light beside it; the paint has bridged it"""
    H, W = B.H, B.W
    if not xs:
        return
    rng = B.rng("age", "joints")
    cols = np.arange(W, dtype=np.float32)[None, :] + 0.5
    for xj in xs:
        wob = np.cumsum(rng.normal(0, 0.18, H)).astype(np.float32)
        wob -= wob.mean()
        wob = np.clip(wob, -2.5, 2.5)[:, None]
        d = np.abs(cols - (xj + wob))
        groove = np.clip(1.4 - d / 1.0, 0, 1)
        hi = np.clip(1.0 - np.abs(d - 2.2) / 0.9, 0, 1)
        col = np.array([40.0, 36.0, 32.0], np.float32)
        B.rgb += (col[None, None, :] - B.rgb) * (0.34 * groove)[..., None]
        B.rgb *= (1.0 + (0.035 if not dark_board else 0.05) * hi)[..., None]
        B.height -= (0.35 * groove).astype(np.float32)


# ------------------------------------------------------------------ rain runs from the top edge
def place_drips(B, count, len_rng, rng, anchors, light, strength=0.30, avoid_boxes=()):
    """soft wide drips of carried dirt that begin at the top edge (the cornice's drip, a fixing) and run down; the dark core is the wear layer R, the paler
    washed tracks beside it are in the base colour only. Returns the layer R (the core, peak 1) and the list of runs (x, r0, length, width)."""
    H, W = B.H, B.W
    layer = np.zeros((H, W), np.float32)
    tracks = np.zeros((H, W), np.float32)
    placed = []
    taken = []
    for i in range(count):
        for attempt in range(300):
            if anchors and rng.random() < 0.65:
                x = float(rng.choice(anchors)) + float(rng.uniform(-18, 18))
            else:
                x = float(rng.uniform(70, W - 70))
            L = int(rng.uniform(*len_rng))
            w = float(rng.uniform(13, 30))
            if any(abs(x - tx) < 90 for tx in taken):
                continue
            r0 = int(rng.uniform(1, 10))
            if x - 3 * w < 2 or x + 3 * w > W - 2 or r0 + L >= H - 4:
                continue
            # a run stops short of the lettering: (x0, x1, top row) of each text box; one that would reach a letter is not placed
            if any((x + 1.6 * w >= bx0 and x - 1.6 * w <= bx1 and r0 + L >= btop - 3) for bx0, bx1, btop in avoid_boxes):
                continue
            rr = np.arange(L, dtype=np.float32)
            sway = 2.2 * np.sin(2 * math.pi * rr / rng.uniform(90, 200) + rng.uniform(0, 6.28))
            wob = 1.0 + 0.18 * np.sin(2 * math.pi * rr / rng.uniform(25, 70) + rng.uniform(0, 6.28))
            a_len = np.clip(1.0 - (rr / L) ** 1.3, 0, 1) * np.clip(0.55 + rr / 14.0, 0, 1)
            xx = np.arange(int(-3 * w), int(3 * w) + 1, dtype=np.float32)
            wr = (w / 2.3) * wob
            core = np.exp(-(xx[None, :] / wr[:, None]) ** 2) * a_len[:, None]
            tr = (np.exp(-((np.abs(xx[None, :]) - 1.25 * w) / (0.45 * w)) ** 2) * 0.55 * np.clip(a_len[:, None] * 1.3, 0, 1)).astype(np.float32)
            cols = (np.round(x + sway).astype(int)[:, None] + xx.astype(int)[None, :])
            rows = (r0 + rr.astype(int))[:, None] + np.zeros_like(xx.astype(int))[None, :]
            ok = (cols >= 0) & (cols < W) & (rows >= 0) & (rows < H)
            layer[rows[ok], cols[ok]] = np.maximum(layer[rows[ok], cols[ok]], core[ok].astype(np.float32))
            tracks[rows[ok], cols[ok]] = np.maximum(tracks[rows[ok], cols[ok]], tr[ok])
            placed.append((int(x), r0, L, round(w, 1)))
            taken.append(x)
            break
    return layer, tracks, placed


def apply_drips(B, layer, tracks, light, strength=0.30):
    """the carried dirt darkens a pale board and dusts a dark one; beside it the rain has washed a paler track"""
    a = np.clip(layer, 0, 1)
    m = a > 0.001
    if m.any():
        px = B.rgb[m]
        luma = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
        pale = luma > 105.0
        tgt = np.where(pale[:, None], GRIME[None, :] * 0.8 + px * 0.2, DUST[None, :])
        k = (strength * a[m])[:, None]
        B.rgb[m] = px + (tgt - px) * k
        B.rough[m] = np.clip(B.rough[m] + 0.10 * a[m], 0, 1)
    t = np.clip(tracks, 0, 1) * (1.0 - np.clip(layer * 2.0, 0, 1))
    mt = t > 0.002
    if mt.any():
        px = B.rgb[mt]
        luma = 0.2126 * px[:, 0] + 0.7152 * px[:, 1] + 0.0722 * px[:, 2]
        pale = luma > 105.0
        tgt = np.where(pale[:, None], np.minimum(px * 1.05 + 5, 255), np.minimum(px * 1.0 + 7, 255))
        B.rgb[mt] = px + (tgt - px) * (0.28 * t[mt])[:, None]


# ------------------------------------------------------------------ gull droppings
def gull_mark(size, rng, S=4):
    """one dropping, drawn until it is ONE connected mark (the wear layer counts connected marks)"""
    for _ in range(40):
        out = _gull_mark(size, rng, S)
        lbl, n = ndi.label(out[0] > 0.25)
        if n == 1:
            return out
    # never a broken mark: keep the biggest piece (the wear layer counts connected marks, and a run's detached tip would be one more)
    core, centre, sp, R = out
    sizes = ndi.sum(core > 0.25, lbl, np.arange(1, n + 1))
    keep = ndi.binary_dilation(lbl == (1 + int(np.argmax(sizes))), iterations=2)
    return core * keep, centre * keep, sp, R


def _gull_mark(size, rng, S=4):
    """one dropping: an irregular chalky-white splash with a darker grey-green centre, a ragged edge, a few thin splash rays and satellite drops,
    one or two short thin runs below. Returns (core, centre, spatter, R): float planes (2R x 2R) at 1x; `core` is ONE connected mark (the wear layer),
    the satellites live in `spatter`."""
    R = int(size * 2.1 + 36)
    ctr = R * S
    img = Image.new("L", (2 * R * S, 2 * R * S), 0)
    d = ImageDraw.Draw(img)
    ph = rng.uniform(0, 6.28, 9)
    amp = rng.uniform(0.6, 1.4, 9)
    sx = rng.uniform(1.0, 1.55)
    sy = rng.uniform(0.62, 0.95)
    tilt = rng.uniform(-0.35, 0.35)
    pts = []
    Rm = size * 0.5 * S
    for t_ in np.linspace(0, 2 * math.pi, 140, endpoint=False):
        rr = Rm * (1.0 + 0.20 * amp[0] * math.sin(2 * t_ + ph[0]) + 0.15 * amp[1] * math.sin(3 * t_ + ph[1]) + 0.09 * amp[2] * math.sin(4 * t_ + ph[2])
                   + 0.045 * amp[3] * math.sin(7 * t_ + ph[3]) + 0.03 * amp[4] * math.sin(13 * t_ + ph[4]) + 0.025 * amp[5] * math.sin(21 * t_ + ph[5]))
        x_, y_ = rr * math.cos(t_) * sx, rr * math.sin(t_) * sy
        pts.append((ctr + x_ * math.cos(tilt) - y_ * math.sin(tilt), ctr + x_ * math.sin(tilt) + y_ * math.cos(tilt)))
    d.polygon(pts, fill=255)
    # splash rays: thin tapered spikes thrown out from the edge, mostly sideways and down
    for j in range(int(rng.integers(3, 8))):
        ang = rng.uniform(-0.3, math.pi + 0.3) if rng.random() < 0.7 else rng.uniform(0, 2 * math.pi)
        r_in = Rm * rng.uniform(0.6, 0.9)
        ln = Rm * rng.uniform(0.45, 1.25)
        wd = Rm * rng.uniform(0.05, 0.12)
        ca, sa = math.cos(ang), math.sin(ang)
        tip = (ctr + (r_in + ln) * ca * sx, ctr + (r_in + ln) * sa * sy)
        b1 = (ctr + r_in * ca * sx - wd * sa, ctr + r_in * sa * sy + wd * ca)
        b2 = (ctr + r_in * ca * sx + wd * sa, ctr + r_in * sa * sy - wd * ca)
        d.polygon([b1, tip, b2], fill=255)
    # the second, smaller splash that fell with it, touching the first
    if rng.random() < 0.75:
        a2 = rng.uniform(0, 6.28)
        dist = Rm * rng.uniform(0.55, 0.85)
        cx2, cy2 = ctr + math.cos(a2) * dist * sx, ctr + abs(math.sin(a2)) * dist * sy * 0.8
        r2 = Rm * rng.uniform(0.28, 0.5)
        pts2 = [(cx2 + r2 * (1 + 0.3 * math.sin(3 * t_ + ph[7])) * math.cos(t_), cy2 + r2 * (1 + 0.25 * math.sin(4 * t_ + ph[6])) * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
        d.polygon(pts2, fill=255)
    # runs below: tapering, fading, a drop at the end
    for j in range(int(rng.integers(1, 3))):
        lx = ctr + rng.uniform(-0.55, 0.55) * Rm * sx
        ln = rng.uniform(0.6, 1.4) * size * S
        w0 = rng.uniform(1.8, 3.4) * S
        y0 = ctr + Rm * sy * 0.45
        for q in range(int(ln)):
            tq = q / ln
            wq = max(1.5 * S, w0 * (1.0 - 0.75 * tq) * (1.0 + 0.2 * math.sin(tq * 14 + j)))      # never under 1.5 mm: a thinner run breaks into pieces in the wear layer
            xq = lx + 1.4 * S * math.sin(tq * 5.0 + j)
            d.line([(xq, y0 + q), (xq, y0 + q + 1.5)], fill=255, width=int(max(1, wq)))
        d.ellipse([lx - w0 * 0.8, y0 + ln - w0 * 0.6, lx + w0 * 0.8, y0 + ln + w0 * 1.0], fill=255)
    core = np.asarray(img.resize((2 * R, 2 * R), Image.BOX), np.float32) / 255.0
    # the centre: one or two darker grey-green patches inside the splash (the faecal part)
    c_img = Image.new("L", (2 * R * S, 2 * R * S), 0)
    dc = ImageDraw.Draw(c_img)
    for j in range(int(rng.integers(1, 3))):
        a3 = rng.uniform(0, 6.28)
        off = Rm * rng.uniform(0.0, 0.35)
        cx3, cy3 = ctr + math.cos(a3) * off, ctr + math.sin(a3) * off * 0.7
        rx, ry = Rm * rng.uniform(0.22, 0.42) * sx, Rm * rng.uniform(0.15, 0.32)
        pts3 = [(cx3 + rx * (1 + 0.3 * math.sin(2 * t_ + j)) * math.cos(t_), cy3 + ry * (1 + 0.3 * math.sin(3 * t_ + j)) * math.sin(t_)) for t_ in np.linspace(0, 2 * math.pi, 40, endpoint=False)]
        dc.polygon(pts3, fill=255)
    centre = np.asarray(c_img.resize((2 * R, 2 * R), Image.BOX), np.float32) / 255.0
    centre = ndi.gaussian_filter(centre, 0.9) * (core > 0.6)
    # satellite drops: more below and round the splash than above it
    sp = np.zeros((2 * R, 2 * R), np.float32)
    n_sat = int(rng.integers(6, 16))
    yy, xx = np.ogrid[:2 * R, :2 * R]
    for j in range(n_sat):
        ang = rng.uniform(-0.4, math.pi + 0.4) if rng.random() < 0.7 else rng.uniform(0, 2 * math.pi)
        dist = rng.uniform(1.1, 2.0) * size * 0.5 * (sx if abs(math.cos(ang)) > 0.5 else sy)
        px_, py_ = R + math.cos(ang) * dist, R + math.sin(ang) * dist
        r_ = rng.uniform(0.7, 2.0)
        sp = np.maximum(sp, np.clip(r_ + 0.5 - np.sqrt((yy - py_) ** 2 + (xx - px_) ** 2), 0, 1) * rng.uniform(0.5, 0.95))
    sp *= (ndi.binary_dilation(core > 0.3, iterations=3) == 0)
    return core, centre, sp, R


WHITE_GULL = np.array([226.0, 223.0, 209.0], np.float32)
GREEN_GREY = np.array([112.0, 112.0, 96.0], np.float32)


def _paste_max(dst, src, r0, c0):
    h, w = src.shape
    rr0, cc0 = max(0, r0), max(0, c0)
    rr1, cc1 = min(dst.shape[0], r0 + h), min(dst.shape[1], c0 + w)
    if rr1 <= rr0 or cc1 <= cc0:
        return
    dst[rr0:rr1, cc0:cc1] = np.maximum(dst[rr0:rr1, cc0:cc1], src[rr0 - r0:rr1 - r0, cc0 - c0:cc1 - c0])


def place_gulls(B, count, size_rng, rng, zone, forbid, big_ok=False):
    """gull droppings on the top edge (they fall from the cornice or a ledge and run a little down the face); `zone` is where a splash's centre may land.
    Returns the wear layer (the connected core), the centre and satellite planes, the placed list."""
    H, W = B.H, B.W
    core = np.zeros((H, W), np.float32)
    centre = np.zeros((H, W), np.float32)
    spat = np.zeros((H, W), np.float32)
    placed = []
    f = zone.copy()
    for i in range(count):
        for attempt in range(300):
            size_t = float(rng.uniform(*size_rng))                  # the target's size is the mark's overall width (the splash alone is 1/1.8 of it: rays, a second splash and runs)
            if not big_ok:
                size_t = min(size_t, 36.0)                           # nothing over about 40 mm wide but on the empty unit, where neglect explains it
            size = size_t / 1.8
            ys, xs = np.where(f)
            if len(ys) == 0:
                return core, centre, spat, placed
            k = int(rng.integers(len(ys)))
            cy, cx = int(ys[k]), int(xs[k])
            c_, ce_, sp_, R = gull_mark(size, rng)
            r0, c0 = cy - R, cx - R
            cm = ndi.binary_dilation(c_ > 0.3, iterations=8)
            yy, xx = np.where(cm)
            gy, gx = yy + r0, xx + c0
            inb = (gy >= 0) & (gy < H) & (gx >= 0) & (gx < W)
            if (gy < 2).any() or (gy > H - 3).any() or (gx < 2).any() or (gx > W - 3).any():
                continue
            if (core[gy[inb], gx[inb]] > 0.01).any() or forbid[gy[inb], gx[inb]].any():
                continue
            _paste_max(core, c_, r0, c0)
            _paste_max(centre, ce_, r0, c0)
            _paste_max(spat, sp_, r0, c0)
            f[max(0, cy - 20):cy + 30, max(0, cx - int(size * 1.6) - 40):cx + int(size * 1.6) + 40] = False
            placed.append((cx, cy, round(size_t, 1)))
            break
    return core, centre, spat, placed


def apply_gulls(B, core, centre, spat):
    n = B.noise("fine")
    mott = np.clip(0.93 + 0.05 * n + 0.04 * B.noise("iso"), 0.7, 1.0)
    c = np.clip(core, 0, 1)
    m = c > 0.002
    B.rgb[m] = B.rgb[m] + (WHITE_GULL[None, :] * mott[m][:, None] - B.rgb[m]) * (0.94 * c[m])[:, None]
    # thin runs are partly see-through: the core's alpha already fades, nothing more to do
    ce = np.clip(centre, 0, 1)
    mc = ce > 0.002
    B.rgb[mc] = B.rgb[mc] + (GREEN_GREY[None, :] - B.rgb[mc]) * (0.78 * ce[mc])[:, None]
    sp = np.clip(spat, 0, 1)
    ms = sp > 0.002
    B.rgb[ms] = B.rgb[ms] + (np.array([196.0, 192.0, 178.0], np.float32)[None, :] - B.rgb[ms]) * (0.7 * sp[ms])[:, None]
    B.rough += (0.78 - B.rough) * np.clip(core, 0, 1) * 0.8
    B.height += (0.12 * np.clip(core, 0, 1)).astype(np.float32)
