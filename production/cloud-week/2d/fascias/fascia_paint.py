"""The painter: the primitives make_fascias.py draws a board with (unit 4.1, cloud week 42).

Everything is deterministic: every random draw comes from a numpy Generator seeded from the board's seed and a name.
A board is H x W float32 planes (colour, roughness, metal, height in mm, optional emissive); row 0 is the TOP of the board,
y in the target is UP from the bottom, so row = H - y (as pixel_checks.to_rows). One pixel is one millimetre.

Letters are drawn glyph by glyph at 4x, from the OFL font files, with the hand jitter of the (amended) target:
baseline SD 1.0 mm clipped at +-1.6, advance within 1.5 per cent of the glyph's own advance (not accumulating),
rotation within 0.35 degrees, stroke within 3 per cent; then reduced to 1x by a box filter.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_common as fc
from fascia_common import H_MM, W_MM

SS = 4                      # text supersampling
GRIME = np.array([88.0, 82.0, 74.0])


# ------------------------------------------------------------------ the board
class Board:
    def __init__(self, T, shop, seed, W=W_MM, H=H_MM, name=None):
        self.T, self.shop, self.seed = T, shop, int(seed)
        self.W, self.H = W, H
        self.name = name or (shop["id"] if shop else "board")
        self.rgb = np.zeros((H, W, 3), np.float32)
        self.rough = np.full((H, W), 0.5, np.float32)
        self.metal = np.zeros((H, W), np.float32)
        self.height = np.zeros((H, W), np.float32)
        self.emis = None
        self.layers = {}               # name -> arrays kept for the checks and the wear png
        self.record = {"blocks": [], "ghosts": [], "shapes": [], "wear": {}}
        self._nz = {}

    def rng(self, *keys):
        return fc.rng_for(self.seed, self.name, *keys)

    # the three noise fields every painted thing borrows its texture from
    def noise(self, kind):
        if kind in self._nz:
            return self._nz[kind]
        r = self.rng("noise", kind)
        sh = (self.H, self.W)
        # a small texture (a sign face, a plate) gets the board's noise at its own proportion, not a patch of a much bigger field
        fx = min(1.0, max(self.W / float(W_MM), 0.04))
        fy = min(1.0, max(self.H / float(H_MM), 0.12))
        if kind == "streak":                    # brush marks and grain lines along the board
            n = fc.fnoise(sh, 48.0 * fx, 2.4 * max(fy, 0.5), r)
        elif kind == "grain":                   # broad grain bands
            n = fc.fnoise(sh, 130.0 * fx, 11.0 * fy, r)
        elif kind == "blot":                    # tonal blotches, roller and brush patches
            n = fc.fnoise(sh, 140.0 * fx, 55.0 * fy, r)
        elif kind == "fine":                    # orange-peel, speckle
            n = fc.fnoise(sh, 0.9, 0.9, r)
        elif kind == "band":                    # long soft bands along the grain (try 2: replaces the cloud-like blot as the ground's slow tone)
            n = fc.fnoise(sh, 300.0 * fx, 17.0 * max(fy, 0.5), r)
        elif kind == "iso":
            n = fc.fnoise(sh, 40.0 * min(fx, fy * 1.0), 40.0 * min(fx, fy * 1.0), r)
        else:
            raise KeyError(kind)
        self._nz[kind] = n
        return n

    # ---- windows
    def win(self, x0, y0, x1, y1, pad=0):
        """array slices (r0, r1, c0, c1) of a box in board mm (y up), padded and clipped"""
        c0 = max(0, int(math.floor(x0)) - pad)
        c1 = min(self.W, int(math.ceil(x1)) + pad)
        r0 = max(0, self.H - int(math.ceil(y1)) - pad)
        r1 = min(self.H, self.H - int(math.floor(y0)) + pad)
        return (r0, r1, c0, c1)

    def paint(self, win, alpha, rgb=None, rough=None, metal=None, height=None, hmode="add"):
        r0, r1, c0, c1 = win
        a = np.clip(alpha, 0.0, 1.0).astype(np.float32)
        if rgb is not None:
            rgb = np.asarray(rgb, np.float32)
            w = self.rgb[r0:r1, c0:c1]
            if rgb.ndim == 1:
                rgb = rgb[None, None, :]
            self.rgb[r0:r1, c0:c1] = w + (rgb - w) * a[..., None]
        if rough is not None:
            w = self.rough[r0:r1, c0:c1]
            self.rough[r0:r1, c0:c1] = w + (np.asarray(rough, np.float32) - w) * a
        if metal is not None:
            w = self.metal[r0:r1, c0:c1]
            self.metal[r0:r1, c0:c1] = w + (np.asarray(metal, np.float32) - w) * a
        if height is not None:
            w = self.height[r0:r1, c0:c1]
            if hmode == "add":
                self.height[r0:r1, c0:c1] = w + np.asarray(height, np.float32) * a
            else:
                self.height[r0:r1, c0:c1] = w + (np.asarray(height, np.float32) - w) * a

    def mottle(self, win, colour, amp_L, kinds=(("grain", 0.5), ("blot", 0.4), ("streak", 0.4), ("fine", 0.25))):
        """a colour with tone variation: amp_L is the SD in L* of the sum of the named noise fields"""
        r0, r1, c0, c1 = win
        colour = np.asarray(colour, np.float32)
        t = np.zeros((r1 - r0, c1 - c0), np.float32)
        for k, w in kinds:
            t += w * self.noise(k)[r0:r1, c0:c1]
        t *= amp_L / max(1e-6, math.sqrt(sum(w * w for _, w in kinds)))
        L = float(fc.lab(colour)[0])
        f = 1.0 + 1.36 * t / max(L, 8.0)
        return np.clip(colour[None, None, :] * f[..., None], 0, 255)


# ------------------------------------------------------------------ shapes
def rect_alpha(win, x0, y0, x1, y1, H=H_MM):
    """exact edge coverage of a box (board mm, y up) over a window"""
    r0, r1, c0, c1 = win
    cols = np.arange(c0, c1, dtype=np.float32)
    ys_top = H - np.arange(r0, r1, dtype=np.float32)          # y (up) of the top edge of each row
    cx = np.clip(np.minimum(cols + 1, x1) - np.maximum(cols, x0), 0, 1)
    cy = np.clip(np.minimum(ys_top, y1) - np.maximum(ys_top - 1, y0), 0, 1)
    return cy[:, None] * cx[None, :]


def poly_alpha(win, pts, width, H=H_MM, closed=False, join="curve"):
    """a polyline stroked at 4x over a window, reduced to 1x"""
    r0, r1, c0, c1 = win
    img = Image.new("L", ((c1 - c0) * SS, (r1 - r0) * SS), 0)
    d = ImageDraw.Draw(img)
    P = [((x - c0) * SS, (H - y - r0) * SS) for x, y in pts]
    d.line(P, fill=255, width=max(1, int(round(width * SS))), joint=join)
    for p in (P[0], P[-1]):
        rr = width * SS / 2.0
        d.ellipse([p[0] - rr, p[1] - rr, p[0] + rr, p[1] + rr], fill=255)
    return np.asarray(img.resize((c1 - c0, r1 - r0), Image.BOX), np.float32) / 255.0


def disc_alpha(win, cx, cy, r, H=H_MM):
    r0, r1, c0, c1 = win
    img = Image.new("L", ((c1 - c0) * SS, (r1 - r0) * SS), 0)
    d = ImageDraw.Draw(img)
    x, y = (cx - c0) * SS, (H - cy - r0) * SS
    d.ellipse([x - r * SS, y - r * SS, x + r * SS, y + r * SS], fill=255)
    return np.asarray(img.resize((c1 - c0, r1 - r0), Image.BOX), np.float32) / 255.0


def to_1x(a_ss, out_shape):
    img = Image.fromarray(a_ss)
    return np.asarray(img.resize((out_shape[1], out_shape[0]), Image.BOX), np.float32) / 255.0


def extrude(face_ss, steps):
    """union of the shifts (0,0) .. (steps,steps) down and right: a block shade, as the target's render_block_mask draws it"""
    out = face_ss.copy()
    covered = 1
    L = int(steps)
    while covered < L + 1:
        s = min(covered, L + 1 - covered)
        sh = np.zeros_like(out)
        sh[s:, s:] = out[:-s, :-s]
        out = np.maximum(out, sh)
        covered += s
    return out


# ------------------------------------------------------------------ text
def block_rgb(T, b):
    if b.get("face_rgb"):
        return np.array(b["face_rgb"], float)
    return fc.pal(T, b["face"])


def jitter_draw(T, b, rng, n):
    """per-glyph jitter draws (amended target: baseline SD 1.0 clipped +-1.6, advance +-1.5 per cent of its own advance not summed,
    rotation +-0.35 deg, stroke +-3 per cent); zeros for vinyl, applied and glass"""
    z = dict(dy=np.zeros(n), dx=np.zeros(n), rot=np.zeros(n), stroke=np.zeros(n))
    j = b.get("jitter")
    if not j:
        return z
    hj = T["common_style"]["hand_jitter"]
    z["dy"] = np.clip(rng.normal(0.0, hj["baseline_sd_mm"][0], n), -hj["baseline_clip_mm"], hj["baseline_clip_mm"])
    z["dx"] = np.clip(rng.normal(0.0, 0.5, n), -1.0, 1.0) * (hj["advance_pct"] / 100.0)      # fraction of own advance
    z["rot"] = np.clip(rng.normal(0.0, 0.5, n), -1.0, 1.0) * hj["rotation_deg"]
    z["stroke"] = np.clip(rng.normal(0.0, 0.5, n), -1.0, 1.0) * (hj["stroke_pct"] / 100.0)
    return z


def stem_px(fS):
    """the vertical stem of the font at this size: the first run of ink across the middle of an H"""
    bb = fS.getbbox("H", anchor="ls")
    l, tp, r, bt = [int(v) for v in bb]
    g = Image.new("L", (r - l + 8, bt - tp + 8), 0)
    ImageDraw.Draw(g).text((4 - l, 4 - tp), "H", font=fS, fill=255, anchor="ls")
    a = np.asarray(g) > 127
    row = a[int(a.shape[0] * 0.28)]            # above the crossbar: the stem alone
    xs = np.where(row)[0]
    if not len(xs):
        return 0.0
    run = 1
    for q in range(1, len(xs)):
        if xs[q] == xs[q - 1] + 1:
            run += 1
        else:
            break
    return float(run)


def squeeze_delta(fS, s, restore=0.55):
    """how many 4x pixels a squeezed glyph's vertical stems are grown by each side, to keep a condensed face's stem weight (a condensed letter is drawn,
    not squeezed: its stems keep most of their weight)"""
    if s >= 0.999:
        return 0
    return int(round(restore * (1.0 - s) * stem_px(fS) / 2.0))


def squeeze_glyph(ga, s, ox, delta):
    """a glyph canvas squeezed to s of its width (origin ox), its stems grown back by `delta` pixels each side"""
    h, w = ga.shape
    nw = max(2, int(round(w * s)))
    a = np.asarray(Image.fromarray(ga).resize((nw, h), Image.BICUBIC))
    if delta > 0:
        a = ndi.maximum_filter1d(a, size=2 * delta + 1, axis=1)
    return a, int(round(ox * s))


def text_layers(T, b, rng=None, hand=True, board_wh=(W_MM, H_MM), dx_mm=0.0, font_key=None, shade=True, extra_pad=24):
    """Draw one block's string from its font at 4x. Returns (face, shade, win): face and shade are float 1x alphas over win.
    hand=False draws it without any jitter (the clean reference)."""
    W, H = board_wh
    key = font_key or b["font"]
    cap = b["cap_mm"]
    px = cap / b["cap_ratio"]
    f1 = fc.font_for(T, key, b["weight"], px)
    fS = fc.font_for(T, key, b["weight"], px * SS)
    trk = b["tracking_em"] * px
    text = b["text"]
    xs = [x for x in fc.glyph_origins(fS, text, trk * SS)]
    xs = [x / SS for x in xs]
    adv = [fS.getlength(ch) / SS for ch in text]
    s_q = float(b.get("squeeze", 1.0) or 1.0)
    d_q = squeeze_delta(fS, s_q) if s_q != 1.0 else 0
    if s_q != 1.0:
        xs = [x * s_q + i * 2.0 * d_q / SS for i, x in enumerate(xs)]
        adv = [a * s_q for a in adv]
    x0, y0, x1, y1 = b["effects_box_mm"]
    pad = extra_pad
    c0 = max(0, int(math.floor(x0)) - pad)
    c1 = min(W, int(math.ceil(x1)) + pad)
    r0 = max(0, H - int(math.ceil(y1)) - pad)
    r1 = min(H, H - int(math.floor(y0)) + pad)
    hh, ww = (r1 - r0) * SS, (c1 - c0) * SS
    canvas = np.zeros((hh, ww), np.uint8)
    n = len(text)
    jd = jitter_draw(T, b, rng, n) if (hand and rng is not None) else jitter_draw(T, dict(b, jitter=None), None, n)
    oy = H - 1 - b["baseline_mm"]
    mpad = int(0.06 * px * SS) + 14
    for i, ch in enumerate(text):
        if ch == " ":
            continue
        bb = fS.getbbox(ch, anchor="ls")
        l, t, r, bt = [int(v) for v in bb]
        gw, gh = r - l + 2 * mpad, bt - t + 2 * mpad
        g = Image.new("L", (gw, gh), 0)
        ImageDraw.Draw(g).text((mpad - l, mpad - t), ch, font=fS, fill=255, anchor="ls")
        ox, oyg = mpad - l, mpad - t                                   # the glyph's origin inside its canvas
        if abs(jd["rot"][i]) > 1e-6:
            g = g.rotate(float(jd["rot"][i]), resample=Image.BICUBIC, center=(ox + adv[i] * SS / 2.0, oyg))
        ga = np.asarray(g)
        if s_q != 1.0:
            ga, ox = squeeze_glyph(ga, s_q, ox, d_q)
            gw = ga.shape[1]
        if abs(jd["stroke"][i]) > 1e-6:
            m = ga > 127
            if m.any():
                dtin = ndi.distance_transform_edt(m)
                stem = 2.2 * float(np.percentile(dtin[m], 90))
                delta = jd["stroke"][i] * stem / 2.0                       # px at 4x, + grows the stroke
                dtout = ndi.distance_transform_edt(~m)
                sd = dtin - dtout
                ga = (np.clip(sd + delta + 0.5, 0.0, 1.0) * 255).astype(np.uint8)
        px_x = (b["origin_x_mm"] + xs[i] + jd["dx"][i] * adv[i] + dx_mm - c0) * SS + d_q
        px_y = (oy - jd["dy"][i] - r0) * SS
        gx = int(round(px_x)) - ox
        gy = int(round(px_y)) - oyg
        # paste with max, clipped to the canvas
        cx0, cy0 = max(0, gx), max(0, gy)
        cx1, cy1 = min(ww, gx + gw), min(hh, gy + gh)
        if cx1 <= cx0 or cy1 <= cy0:
            continue
        sub = ga[cy0 - gy:cy1 - gy, cx0 - gx:cx1 - gx]
        canvas[cy0:cy1, cx0:cx1] = np.maximum(canvas[cy0:cy1, cx0:cx1], sub)
    face = to_1x(canvas, (r1 - r0, c1 - c0))
    sh = None
    if shade and b.get("shade"):
        steps = int(round(b["shade"]["d_mm"] * SS))
        ext = extrude(canvas, steps)
        sh = to_1x(ext, (r1 - r0, c1 - c0))
    return face, sh, (r0, r1, c0, c1)


def face_style(T, b):
    """roughness and metal of a block's face from its technique and the target's materials table"""
    tech = b.get("technique", "painted")
    if tech == "gilded":
        return 0.30, 1.0, 0.05
    if tech == "vinyl":
        return 0.45, 0.0, 0.08
    if tech == "back_painted":
        return 0.12, 0.0, 0.0
    if tech == "painted":
        return None, 0.0, 0.20            # rough set from the ground
    return 0.5, 0.0, 0.0


def paint_block(B, b, ground_rough=0.55, hand=True, dx_mm=0.0, font_key=None):
    """paint a text block (shade, then face) onto the board, record what was drawn"""
    T = B.T
    rng = B.rng("block", b["id"])
    face, sh, win = text_layers(T, b, rng, hand=hand, dx_mm=dx_mm, font_key=font_key, board_wh=(B.W, B.H))
    rough, metal, relief = face_style(T, b)
    if rough is None:
        rough = max(0.35, ground_rough - 0.10)
    fcol = block_rgb(T, b)
    tech = b.get("technique", "painted")
    amp = {"gilded": 2.2, "painted": 1.4, "vinyl": 0.4, "back_painted": 0.7}.get(tech, 1.0)
    face_img = B.mottle(win, fcol, amp, kinds=(("blot", 0.7), ("fine", 0.35), ("iso", 0.4)))
    r0, r1, c0, c1 = win
    if tech == "gilded":
        # leaf joins, a paler rim 3 mm wide (the target's gilding style, P1) and a few chips down to the size
        m = face > 0.5
        if m.any():
            din = ndi.distance_transform_edt(m)
            rim = np.clip(1.0 - (din - 0.5) / 3.0, 0, 1) * m
            face_img = face_img * (1.0 + 0.045 * rim[..., None])
            lx = (np.arange(c0, c1) // 90) % 7
            ly = (np.arange(r0, r1) // 90) % 5
            joins = ((lx[None, :] * 3 + ly[:, None] * 5) % 7) / 6.0 - 0.5
            face_img = face_img * (1.0 + 0.035 * joins[..., None])
            cr = B.rng("chips", b["id"])
            nchip = int(0.0012 * m.sum())
            ys, xs_ = np.where(m & (din > 2.0))
            if len(ys):
                pick = cr.choice(len(ys), size=min(nchip, len(ys)), replace=False)
                chip = np.zeros_like(face)
                chip[ys[pick], xs_[pick]] = 1.0
                chip = ndi.gaussian_filter(chip, 0.8)
                chip = np.clip(chip * 4.0, 0, 1) * (face > 0.9)
                face_img = face_img * (1 - chip[..., None]) + np.array([150, 110, 50], np.float32)[None, None, :] * chip[..., None]
    if sh is not None:
        scol = B.mottle(win, fc.pal(T, b["shade"]["colour"]), 0.8, kinds=(("fine", 0.5), ("blot", 0.5)))
        sa = np.clip(sh, 0, 1)
        B.paint(win, sa, scol, rough=max(0.35, ground_rough - 0.10), metal=0.0)
        if tech in ("painted", "gilded"):
            r0_, r1_, c0_, c1_ = win
            B.height[r0_:r1_, c0_:c1_] += (0.15 * np.clip(sa - face, 0, 1)).astype(np.float32)
    B.paint(win, face, face_img, rough=rough, metal=metal, height=relief)
    return dict(win=win, face=face, shade=sh)


# ------------------------------------------------------------------ ghosts, repaint, loss
def repaint_mask(B, win, target_mask, share, rng, grain_dir="along"):
    """brush-stroke patches of newer paint over a ghost until `share` of the ghost's pixels are covered; returns a 0..1 alpha"""
    r0, r1, c0, c1 = win
    hh, ww = r1 - r0, c1 - c0
    total = float((target_mask > 0.5).sum())
    cover = np.zeros((hh, ww), np.float32)
    if share <= 0 or total == 0:
        return cover
    covered = 0.0
    ys, xs = np.where(target_mask > 0.5)
    tries = 0
    while covered / total < share and tries < 4000:
        tries += 1
        k = rng.integers(len(ys))
        cy, cx = int(ys[k]), int(xs[k])
        L = rng.uniform(70, 230)
        Wd = rng.uniform(16, 38)
        ang = rng.normal(0, 2.5) * math.pi / 180
        img = Image.new("L", (ww * 2, hh * 2), 0)
        d = ImageDraw.Draw(img)
        ux, uy = math.cos(ang), math.sin(ang)
        px, py = cx * 2, cy * 2
        pts = [(px - ux * L, py - uy * L), (px + ux * L, py + uy * L)]
        d.line(pts, fill=255, width=int(Wd * 2))
        a = np.asarray(img.resize((ww, hh), Image.BOX), np.float32) / 255.0
        newc = np.maximum(cover, a)
        cov_now = float(((newc > 0.5) & (target_mask > 0.5)).sum())
        cover = newc
        covered = cov_now
    # ragged brush edge
    n = fc.fnoise((hh, ww), 1.6, 1.6, rng)
    cover = np.clip((ndi.gaussian_filter(cover, 1.0) - 0.5) * 6.0 + 0.5 + 0.35 * n, 0, 1)
    return cover


def loss_patches(B, free, fraction, rng, base_rgb, kind="paint", weight=None, gap=2, big_prob=0.022):
    """flaked paint: elongated patches along the grain, median aspect about 3.6 and equivalent diameter about 9 mm (the target's P2),
    placed without touching, on `free` (a bool H x W plane), until `fraction` of the whole board face is lost.
    Returns the alpha plane of the loss and a plane marking which substrate (0 none, 1 primer, 2 bare wood).
    Where the free ground is nearly full the patches shrink a little (a flake that cannot find room is a smaller flake)."""
    H, W = B.H, B.W
    target_px = fraction * W * H
    alpha = np.zeros((H, W), np.float32)
    sub = np.zeros((H, W), np.uint8)
    occupied = ndi.binary_dilation(~free, iterations=gap)
    got = 0.0
    tries = 0
    fails = 0
    scale = 1.0
    ys, xs = np.where(free)
    if len(ys) == 0 or fraction <= 0:
        return alpha, sub
    if weight is not None:
        cw = np.cumsum(weight[ys, xs].astype(np.float64))
        cw /= cw[-1]
    bank = fc.fnoise((300, 300), 1.6, 1.2, rng)
    while got < target_px and tries < 600000:
        tries += 1
        if weight is not None and tries == 120000 and got < 0.9 * target_px:
            weight = None                                   # the crowded places are full: spread the rest evenly
        eqd = float(np.clip(rng.lognormal(math.log(9.0), 0.62), 3.0, 70.0)) * scale
        if rng.random() < big_prob:
            eqd *= rng.uniform(2.6, 4.5)                     # the odd big sheet that has peeled away (P2's largest patch is 577 x 88 mm)
        eqd = min(max(eqd, 3.0), 90.0)
        aspect = float(np.clip(rng.lognormal(math.log(3.6), 0.28), 2.0, 8.0))
        area = math.pi / 4.0 * eqd * eqd
        b_ = math.sqrt(area / math.pi / aspect)            # semi-minor
        a_ = b_ * aspect                                    # semi-major
        k = int(np.searchsorted(cw, rng.random())) if weight is not None else int(rng.integers(len(ys)))
        k = min(k, len(ys) - 1)
        cy, cx = float(ys[k]), float(xs[k])
        if occupied[int(cy), int(cx)]:
            fails += 1
            if fails > 400:
                scale = max(0.8, scale * 0.985)
                fails = 0
            continue
        ang = rng.normal(0, 4.0) * math.pi / 180
        hr = int(a_ + 4)
        r0, r1 = int(cy) - hr, int(cy) + hr + 1
        c0, c1 = int(cx) - hr, int(cx) + hr + 1
        if r0 < 0 or c0 < 0 or r1 > H or c1 > W or (r1 - r0) > 296:
            continue
        yy, xx = np.mgrid[r0:r1, c0:c1].astype(np.float32)
        u = (xx - cx) * math.cos(ang) + (yy - cy) * math.sin(ang)
        v = -(xx - cx) * math.sin(ang) + (yy - cy) * math.cos(ang)
        dd = np.sqrt((u / a_) ** 2 + (v / b_) ** 2)
        oy, ox = int(rng.integers(0, 300 - dd.shape[0])), int(rng.integers(0, 300 - dd.shape[1]))
        dd = dd + 0.22 * bank[oy:oy + dd.shape[0], ox:ox + dd.shape[1]]
        m = dd < 1.0
        if m.sum() < 6:
            continue
        if (occupied[r0:r1, c0:c1] & m).any():
            fails += 1
            if fails > 60:
                scale = max(0.8, scale * 0.985)
                fails = 0
            continue
        fails = 0
        a = np.clip((1.0 - dd) * min(a_, 6.0) * 0.9, 0, 1) * m
        alpha[r0:r1, c0:c1] = np.maximum(alpha[r0:r1, c0:c1], a.astype(np.float32))
        sub_w = sub[r0:r1, c0:c1]
        sub_w[m] = 1                                        # the older coat shows first ...
        if eqd >= 8.0 and rng.random() < 0.7:               # ... and in the bigger flakes the bare wood shows at the core
            sub_w[dd < 0.5] = 2
        occupied[r0:r1, c0:c1] |= ndi.binary_dilation(m, iterations=gap)
        got += float((a > 0.5).sum())
    return alpha, sub


def sample_free(free, n, rng):
    ys, xs = np.where(free)
    k = rng.integers(len(ys), size=n)
    return list(zip(xs[k], ys[k]))
