"""paper_wear.py: what the weather, the wall and the people do to a sheet, a card, a plate or a board (unit 4.2 to 4.4, cloud week 42).

`Surf` holds one rendered item (colour, alpha, height in mm, roughness, metal) and `apply(surf, table, cls)` does what the target's `wear_tables[table]` and `age_rules` say, by class.
Every number is the target's, drawn from the ranges it gives; the class decides how many and how big (A none, B a little, C more, D most).
Tears, lifted corners and the loss of paper keep off the lettering in classes A and B (the reader must still read them); in C and D they may cross it (the target lets the oldest layer fade below legibility).
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import paper_common as pc
import paper_ink as pi

CLS_I = {"A": 0, "B": 1, "C": 2, "D": 3}
GREY_BROWN = (118, 104, 86)
PASTE = (168, 148, 110)
RUST = (140, 84, 44)
STEEL = (44, 40, 38)
ALUM = (150, 150, 146)
LIME = (226, 223, 212)


class Surf(object):
    def __init__(self, geo, P, cls, rgb, alpha, height, rough, metal, rng, tau_scale=1.0):
        self.geo, self.P, self.cls, self.rgb, self.alpha = geo, P, cls, rgb, alpha
        self.height, self.rough, self.metal, self.rng = height, rough, metal, rng
        self.item = geo.item
        self.ppm = geo.ppm
        self.h, self.w = rgb.shape[:2]
        self.H, self.W = self.item["format"]["h_mm"], self.item["format"]["w_mm"]
        self.ci = CLS_I[cls]
        self.tau_scale = tau_scale
        self.text = []              # px boxes of every block (x0, y0, x1, y1), the lettering's own area
        self.text_mm = []           # the same in mm from the top left, without the imprints: what the loss of paper keeps clear of
        for b in self.item["blocks"]:
            if b.get("ghost"):
                continue
            x0, y0, x1, y1 = b["ink_box_mm"]
            ex = ey = 0.0
            if b.get("hand"):       # the reader's window for a hand block is wider (sc.glyph_window)
                hs = self.P.T["hand_styles"][b["hand"]]
                ex, ey = 6.0, 3.5 * hs["baseline_sd_mm"] + 0.6 + 0.12 * b["cap_mm"]
            self.text.append(((x0 - ex) * self.ppm, (self.H - y1 - ey) * self.ppm, (x1 + ex) * self.ppm, (self.H - y0 + ey) * self.ppm))
            if b.get("role") != "imprint":          # the printer's imprint is illegible by design (the target's section 14): the weather may take it
                self.text_mm.append((x0 - ex, self.H - y1 - ey, x1 + ex, self.H - y0 + ey))
        self.log = {}

    # ---- helpers
    def mm(self, v):
        return v * self.ppm

    def win_of(self, box, pad=0):
        return pi.window_around(box, (self.h, self.w), pad)

    def tint(self, win, m, colour, opacity):
        wx0, wx1, wy0, wy1 = win
        a = (m * opacity)[..., None] if np.ndim(opacity) == 0 else (m * opacity)[..., None]
        a = a * self.alpha[wy0:wy1, wx0:wx1, None]
        sub = self.rgb[wy0:wy1, wx0:wx1]
        sub[:] = sub * (1 - a) + np.asarray(colour, np.float32) * a

    def margins(self, margin_mm, wide):
        """(along, up-and-down) in pixels: the reader window (8 mm along the line, 3 mm up and down; a hand card more) and 2 mm for the rim of a tear, when `wide`, else a uniform margin."""
        if wide:
            return 12.0 * self.ppm, 7.0 * self.ppm
        return margin_mm * self.ppm, margin_mm * self.ppm

    def hits_text(self, box, margin_mm=2.0, wide=False):
        mx, my = self.margins(margin_mm, wide)
        x0, y0, x1, y1 = box
        boxes = [(a * self.ppm, b * self.ppm, c * self.ppm, d * self.ppm) for a, b, c, d in self.text_mm] if wide else self.text
        for a, b, c, d in boxes:
            if x0 < c + mx and x1 > a - mx and y0 < d + my and y1 > b - my:
                return True
        return False

    def protect_mask(self, margin_mm=2.0, wide=False):
        m = np.zeros((self.h, self.w), bool)
        mx, my = self.margins(margin_mm, wide)
        for a, b, c, d in self.text:
            m[int(max(0, b - my)):int(min(self.h, d + my)), int(max(0, a - mx)):int(min(self.w, c + mx))] = True
        return m

    def stock_colour(self):
        it = self.item
        if it["stock"]:
            return np.asarray(self.P.stock(it["stock"], self.cls, self.tau_scale), np.float32)
        return np.asarray((226, 224, 215), np.float32)

    def blob(self, cx, cy, r, irregular=0.35, rng=None, win_pad=None):
        """Irregular blob coverage (window, array): a disc with a noisy radius, in pixels."""
        rng = rng or self.rng
        pad = r * (1 + irregular) + 3
        win = self.win_of((cx - pad, cy - pad, cx + pad, cy + pad))
        n = 18
        ang = np.linspace(0, 2 * math.pi, n, endpoint=False)
        rad = r * (1 + irregular * (rng.random(n) - 0.5) * 2)
        pts = [(cx + rr * math.cos(a), cy + rr * math.sin(a)) for rr, a in zip(rad, ang)]
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255))
        return win, cov

    def streak(self, x, y0, y1, width_px, colour, opacity, taper=True, sway=0.0, end_frac=0.55):
        """A vertical dirt or rust run: from y0 down to y1, soft edges, tapering to a point, a little sideways drift."""
        rng = self.rng
        win = self.win_of((x - width_px * 2 - abs(sway) * width_px, y0, x + width_px * 2 + abs(sway) * width_px, y1))
        wx0, wx1, wy0, wy1 = win
        if wx1 <= wx0 or wy1 <= wy0:
            return
        ys = np.arange(wy0, wy1, dtype=np.float32)
        t = np.clip((ys - y0) / max(1.0, y1 - y0), 0, 1)
        xc = x + sway * width_px * 0.5 * np.sin(t * 2.6 + rng.random() * 6)
        wid = width_px * (1.0 - (1.0 - end_frac) * t if taper else np.ones_like(t))
        xs = np.arange(wx0, wx1, dtype=np.float32)
        d = np.abs(xs[None, :] - xc[:, None]) / np.maximum(0.5, wid[:, None] / 2.0)
        prof = 0.5 * (1 + np.cos(np.clip(d, 0, 1) * math.pi))
        fade = (1 - t) ** 0.5 * (0.75 + 0.5 * rng.random())
        m = (prof * fade[:, None]).astype(np.float32)
        self.tint(win, m, colour, opacity)

    # ---- shading from the height map
    def shade(self, k=0.10, light=(-0.6, -0.8)):
        h = pc.smooth(self.height, max(0.7, 0.3 * self.ppm))
        gy, gx = np.gradient(h)
        s = (gx * light[0] + gy * light[1]) * self.ppm            # mm of height per mm
        s = np.clip(s * k * 0.8, -0.08, 0.08)
        self.rgb *= (1.0 + s)[..., None]


# ------------------------------------------------------------------------------------------ paper
def cockle(S, amp_mm, wl_mm, aniso=2.2):
    n = pc.value_noise((S.h, S.w), wl_mm * S.ppm, S.rng, aniso=aniso, octaves=2)
    S.height += ((n - 0.5) * 2.0 * amp_mm).astype(np.float32)


def corner_lift(S, corner, r_mm, back=None, avoid=True):
    """A corner lifting off the wall: its back shows (the stock's own colour, lighter), a fold line and a shadow beyond it."""
    r = r_mm * S.ppm
    h, w = S.h, S.w
    ys, xs = np.mgrid[0:h, 0:w].astype(np.float32)
    # distance from the corner along the two edges
    u = xs if corner in (0, 3) else (w - 1 - xs)
    v = ys if corner in (0, 1) else (h - 1 - ys)
    s_ = u + v
    box = (0 if corner in (0, 3) else w - r, 0 if corner in (0, 1) else h - r, r if corner in (0, 3) else w, r if corner in (0, 1) else h)
    win = S.win_of(box, 0)
    wx0, wx1, wy0, wy1 = win
    ss = s_[wy0:wy1, wx0:wx1]
    inside = np.clip((r - ss) / 1.5, 0, 1)
    sh = np.clip(1 - np.abs(ss - r - 0.02 * r) / max(2.0, 0.12 * r), 0, 1) * (ss > r)
    base = S.stock_colour() if back is None else np.asarray(back, np.float32)
    shade = (1.02 - 0.12 * np.clip(ss / r, 0, 1))[..., None]
    sub = S.rgb[wy0:wy1, wx0:wx1]
    a = inside[..., None] * S.alpha[wy0:wy1, wx0:wx1, None]
    sub[:] = sub * (1 - a) + (base * 1.03 * shade) * a
    sub *= (1 - 0.14 * sh[..., None])
    S.height[wy0:wy1, wx0:wx1] += (inside * (0.5 + 1.3 * (1 - np.clip(ss / r, 0, 1)))).astype(np.float32)
    S.rough[wy0:wy1, wx0:wx1] = S.rough[wy0:wy1, wx0:wx1] * (1 - inside * 0.3) + 0.85 * inside * 0.3


def corner_lifts(S, n, rlo, rhi):
    rng = S.rng
    done = 0
    for _ in range(n * 6):
        if done >= n:
            break
        c = int(rng.integers(0, 4))
        r = float(rng.uniform(rlo, rhi))
        rr = r * S.ppm
        box = (0 if c in (0, 3) else S.w - rr, 0 if c in (0, 1) else S.h - rr, rr if c in (0, 3) else S.w, rr if c in (0, 1) else S.h)
        if S.cls in ("A", "B") and S.hits_text(box, wide=True):
            continue
        corner_lift(S, c, r)
        done += 1
    S.log["corner_lifts"] = done


def rain_runs(S, per_m, colour=GREY_BROWN, opac=(0.15, 0.40), length=(10, 60), width=(0.4, 1.5), from_top=True):
    rng = S.rng
    n = int(round(per_m * S.W / 1000.0))
    k = 0
    for _ in range(n):
        x = rng.uniform(0.03, 0.97) * S.w
        L = rng.uniform(*length) * S.ppm
        y0 = 0.0
        if S.cls in ("A", "B") and S.hits_text((x - 2, 0, x + 2, L), 0.5):
            L = min(L, max(0.0, min([b for (a, b, c, d) in S.text if a - 2 * S.ppm < x < c + 2 * S.ppm] + [L]) - S.ppm))
            if L < 4 * S.ppm:
                continue
        S.streak(x, y0, y0 + L, max(1.0, rng.uniform(*width) * S.ppm), colour, float(rng.uniform(*opac)), sway=0.4)
        k += 1
    S.log["rain_runs"] = k


def protect_coarse(S, mx=12.0, my=7.0):
    """1 px/mm map of where the loss of paper must keep out: every line's reading window (and the hand's wider one) and the clearance round it, the printer's imprint excepted."""
    Hc, Wc = int(math.ceil(S.H)), int(math.ceil(S.W))
    m = np.zeros((Hc, Wc), bool)
    for x0, y0, x1, y1 in S.text_mm:
        m[int(max(0, y0 - my)):int(min(Hc, y1 + my)), int(max(0, x0 - mx)):int(min(Wc, x1 + mx))] = True
    return m


def patch_harmonics(rng, R_ref, amp_mm):
    """The outline of a torn patch: radius x (1 + a sum of harmonics) with wavelengths 30 to 120 mm round a circle of radius R_ref (so k = 2 pi R_ref / wavelength), a total amplitude of
    about amp_mm (10 to 40 mm), and a finer raggedness of a few millimetres."""
    ks = np.maximum(2, np.round(2 * math.pi * R_ref / rng.uniform(30, 120, 6))).astype(int)
    ph = rng.uniform(0, 2 * math.pi, 6)
    am = (amp_mm / max(R_ref, 20.0)) * rng.uniform(0.5, 1.0, 6) * 0.45
    kf = np.maximum(3, np.round(2 * math.pi * R_ref / rng.uniform(10, 25, 4))).astype(int)
    pf = rng.uniform(0, 2 * math.pi, 4)
    af = (3.0 / max(R_ref, 20.0)) * rng.uniform(0.5, 1.0, 4)
    return (ks, ph, am, kf, pf, af)


def polar_patch(shape, centre, R, harm, prot, margin=4.0):
    """A torn patch (bool, 1 px/mm): a closed outline round `centre` (mm from the top left) of mean radius R, kept `margin` mm clear of the protected map along every ray."""
    Hc, Wc = shape
    n = 360
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    ks, ph, am, kf, pf, af = harm
    r = np.full(n, 1.0)
    for k, p, a in zip(ks, ph, am):
        r += a * np.cos(k * th + p)
    for k, p, a in zip(kf, pf, af):
        r += a * np.cos(k * th + p)
    r = np.clip(r, 0.35, 2.0) * R
    if prot is not None and prot.any():
        T = int(r.max()) + 2
        t = np.arange(T, dtype=np.float32)
        px = np.clip((centre[0] + np.outer(np.cos(th), t)).astype(int), 0, Wc - 1)
        py = np.clip((centre[1] + np.outer(np.sin(th), t)).astype(int), 0, Hc - 1)
        hit = prot[py, px] & (np.abs(centre[0] + np.outer(np.cos(th), t) - px) < 2) & (t[None, :] <= r[:, None] + margin)
        first = np.where(hit.any(1), hit.argmax(1), 10 ** 6)
        r = np.minimum(r, np.maximum(first - margin, 0.0))
        r = ndi.gaussian_filter1d(r, 4.0, mode="wrap")
        r = np.minimum(r, np.maximum(first - margin, 0.0))
    pts = [(float(centre[0] + rr * math.cos(a)), float(centre[1] + rr * math.sin(a))) for rr, a in zip(r, th)]
    im = Image.new("L", (Wc, Hc), 0)
    ImageDraw.Draw(im).polygon(pts, fill=255)
    return np.asarray(im) > 127


def shape_loss(lost):
    """No tongue of loss or of paper narrower than 20 mm (the review asked 15): open the loss and the paper with a 20 mm disc."""
    st = gl_disk(10)
    lost = ndi.binary_opening(lost, st, border_value=0)
    paper = ndi.binary_opening(~lost, st, border_value=1)
    return ~paper


def gl_disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def loss_and_tears(S, share_range, n_tears):
    """The loss of paper: a bill pasted on a wall is torn from below, the bottom corners first. 2 to 5 torn patches with ragged outlines (wavelengths 30 to 120 mm); class B keeps to the lower
    corners (a corner of at most 120 mm, half the foot untouched); in C and D also the foot's middle and, in D, an upper corner; the edge tears are small ragged bites; in A and B the lettering's reading
    window and 4 mm round it are never touched. In C and D a ghost of the paste is left (214, 205, 185 at 0.3). The rim is pale paper fibre."""
    rng = S.rng
    lo, hi = share_range
    share = float(rng.uniform(lo, hi)) if hi > 0 else 0.0
    if share <= 0.001 and n_tears <= 0:
        return
    Hc, Wc = int(math.ceil(S.H)), int(math.ceil(S.W))
    prot = protect_coarse(S) if S.cls in ("A", "B") else None
    R0 = math.sqrt(max(share, 0.001) * S.W * S.H / 2.0 * 4.0 / math.pi) if share > 0.001 else 0.0
    specs = []                              # (centre, weight, harmonics)
    if share > 0.001:
        left = rng.random() < 0.5
        corners = [(0.0, S.H), (S.W, S.H)] if S.cls != "B" or rng.random() < 0.5 else [((0.0, S.H) if left else (S.W, S.H))]
        for c in corners:
            specs.append((c, float(rng.uniform(0.8, 1.2)), patch_harmonics(rng, R0, rng.uniform(10, 35))))
        if S.cls in ("C", "D"):
            specs.append(((float(rng.uniform(0.25, 0.75)) * S.W, S.H), float(rng.uniform(0.6, 1.0)), patch_harmonics(rng, R0, rng.uniform(10, 40))))
        if S.cls == "D":
            specs.append(((float(rng.choice([0.0, S.W])), float(rng.uniform(0.0, 0.5)) * S.H), float(rng.uniform(0.5, 0.9)), patch_harmonics(rng, R0, rng.uniform(10, 40))))
            specs.append(((float(rng.uniform(0.1, 0.9)) * S.W, 0.0), float(rng.uniform(0.3, 0.7)), patch_harmonics(rng, R0, rng.uniform(10, 40))))
    R0 = R0 * (2.0 / max(len(specs), 1)) ** 0.5 if specs else 0.0
    bites = []
    for _ in range(n_tears):
        e = int(rng.integers(0, 4))
        t = float(rng.uniform(0.1, 0.9))
        c = (t * S.W, 0.0) if e == 0 else ((S.W, t * S.H) if e == 1 else ((t * S.W, S.H) if e == 2 else (0.0, t * S.H)))
        Rb = float(rng.uniform(14, 35))
        bites.append((c, Rb, patch_harmonics(rng, Rb, rng.uniform(4, 10))))
    scale_hi = 0.9 * max(S.W, S.H)

    def build(f):
        lost = np.zeros((Hc, Wc), bool)
        for c, wgt, hm in specs:
            lost |= polar_patch((Hc, Wc), c, R0 * f * wgt, hm, prot)
        for c, R, hm in bites:
            lost |= polar_patch((Hc, Wc), c, R, hm, prot)
        return lost
    f = 1.0
    if specs:
        lo_f, hi_f = 0.1, 3.0
        for _ in range(12):
            f = (lo_f + hi_f) / 2
            got = float(build(f).mean())
            if got > share:
                hi_f = f
            else:
                lo_f = f
        f = lo_f
    lost = shape_loss(build(f))
    if not lost.any():
        return
    S.log["loss_share"] = float(lost.mean())
    soft = ndi.gaussian_filter(lost.astype(np.float32), 1.2)
    up = np.asarray(Image.fromarray((soft * 255).astype(np.uint8)).resize((S.w, S.h), Image.BILINEAR)).astype(np.float32) / 255.0
    fib = pc.value_noise((S.h, S.w), max(1.0, 0.8 * S.ppm), rng, octaves=2)
    lost_f = (up + (fib - 0.5) * 0.30 > 0.5).astype(np.float32)
    lost_f = pc.smooth(lost_f, 0.6)
    edge = np.clip(ndi.grey_dilation(lost_f, size=(int(1.3 * S.ppm) * 2 + 1,) * 2) - lost_f, 0, 1)
    fibre = 0.6 + 0.4 * pc.value_noise((S.h, S.w), 1.5 * S.ppm, rng)
    S.tint((0, S.w, 0, S.h), edge * (1 - lost_f) * fibre, (244, 241, 231), 0.8)
    if S.cls in ("C", "D"):
        ghost = np.asarray((214, 205, 185), np.float32)
        S.rgb[:] = S.rgb * (1 - lost_f[..., None]) + ghost * lost_f[..., None]
        S.alpha *= (1 - 0.7 * lost_f)
    else:
        S.alpha *= (1 - lost_f)
    S.height -= (lost_f * 0.1).astype(np.float32)
    S.log["tears"] = len(bites)
    S.log["loss_share"] = float(1 - (S.alpha > 0.5).mean())


def paste_halo(S, strength=(0.15, 0.40), width=(2, 10)):
    rng = S.rng
    n = pc.value_noise((S.h, S.w), 20 * S.ppm, rng, octaves=2)
    wpx = rng.uniform(*width) * S.ppm
    ys, xs = np.mgrid[0:S.h, 0:S.w].astype(np.float32)
    d = np.minimum(np.minimum(xs, S.w - 1 - xs), np.minimum(ys, S.h - 1 - ys))
    m = np.clip(1 - d / (wpx * (0.3 + 1.2 * n)), 0, 1)
    S.tint((0, S.w, 0, S.h), m, PASTE, float(rng.uniform(*strength)))


def bleach(S, top_frac=0.33, amount=0.10):
    ys = np.arange(S.h, dtype=np.float32)
    t = np.clip(1 - ys / (S.h * top_frac), 0, 1)
    m = np.ones((S.h, S.w), np.float32) * t[:, None]
    S.tint((0, S.w, 0, S.h), m, S.stock_colour(), amount)


def photocopy_artefacts(S, process):
    """What a copier leaves: toner speckle, a grey band along one edge, one to three vertical streaks (the target's process numbers)."""
    pr = S.geo.item
    p = S.P.T["processes"][process]
    rng = S.rng
    ink = np.asarray(S.P.ink("toner", S.item["stock"], S.cls, S.tau_scale), np.float32)
    area_cm2 = S.W * S.H / 100.0
    n = rng.poisson(p["speckle"]["per_cm2"] * area_cm2)
    d0, d1 = p["speckle"]["diam_mm"]
    for _ in range(int(n)):
        x, y = rng.uniform(0, S.w), rng.uniform(0, S.h)
        r = max(0.55, rng.uniform(d0, d1) * S.ppm / 2)
        win = S.win_of((x - r, y - r, x + r, y + r), 2)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(x - r - ox) * ss, (y - r - oy) * ss, (x + r - ox) * ss, (y + r - oy) * ss], fill=255), ss=4)
        S.tint(win, cov, ink, 0.85)
    es = p["edge_shadow"]
    wmm = float(rng.uniform(*es["width_mm"]))
    left = rng.random() < 0.5
    ys, xs = np.mgrid[0:S.h, 0:S.w].astype(np.float32)
    d = (xs if left else ys) / (wmm * S.ppm)
    grey = np.asarray((130, 130, 128), np.float32)
    m = np.clip(1 - d, 0, 1) ** 1.5 * 0.42 * (0.85 + 0.3 * pc.value_noise((S.h, S.w), 18 * S.ppm, rng))
    S.tint((0, S.w, 0, S.h), m, grey, 1.0)
    S.log["edge_shadow"] = ("left" if left else "top", wmm)
    for _ in range(int(rng.integers(p["streaks"]["count"][0], p["streaks"]["count"][1] + 1))):
        x = rng.uniform(0.05, 0.95) * S.w
        y0 = rng.uniform(0, 0.3) * S.h
        L = p["streaks"]["height_fraction"] * S.h * rng.uniform(0.5, 1.0)
        S.streak(x, y0, y0 + L, max(1.0, rng.uniform(*p["streaks"]["width_mm"]) * S.ppm), (70, 70, 70), float(rng.uniform(*p["streaks"]["opacity"])), taper=False)


def curl_out(S, lo=3, hi=8):
    """The lower edge of a sheet in a window curls out: a pale band with a shadow under it, the height lifting."""
    rng = S.rng
    wmm = float(rng.uniform(lo, hi))
    wpx = wmm * S.ppm
    ys = np.arange(S.h, dtype=np.float32)
    t = np.clip((ys - (S.h - wpx)) / wpx, 0, 1)
    m = (t[:, None] * np.ones((1, S.w), np.float32)) * (0.7 + 0.3 * pc.value_noise((S.h, S.w), 30 * S.ppm, rng)[..., :])
    S.tint((0, S.w, 0, S.h), m, S.stock_colour() * 1.04, 0.5)
    S.height += (t[:, None] * wmm * 0.6).astype(np.float32)
    sh = np.clip((ys - (S.h - 2 * wpx)) / wpx, 0, 1) * (1 - t)
    S.rgb *= (1 - 0.06 * sh)[:, None, None]
    S.log["curl_mm"] = wmm


def condensation(S):
    rng = S.rng
    n = int(rng.integers(5, 9))
    for _ in range(n):
        x = rng.uniform(0.04, 0.96) * S.w
        y0 = rng.uniform(0.62, 0.8) * S.h
        L = rng.uniform(25, 85) * S.ppm
        if S.cls in ("A", "B") and S.hits_text((x - 3, y0, x + 3, y0 + L), 0.5):
            L = min(L, max(0.0, min([b for (a, b, c, d) in S.text if b > y0 and a - 3 * S.ppm < x < c + 3 * S.ppm] + [y0 + L]) - y0 - S.ppm))
            if L < 6 * S.ppm:
                continue
        S.streak(x, y0, min(S.h - 1, y0 + L), max(1.0, rng.uniform(0.8, 2.0) * S.ppm), (150, 142, 124), float(rng.uniform(0.08, 0.18)), sway=0.6)
    ys = np.arange(S.h, dtype=np.float32)
    g = np.clip((ys / S.h - 0.8) / 0.2, 0, 1)
    S.tint((0, S.w, 0, S.h), g[:, None] * np.ones((1, S.w), np.float32), (190, 178, 150), 0.10)


def tape_filter(S, win, cov, spec):
    """A tab of yellowed tape is a translucent filter, not paint: what lies under it (paper, ink) shows through, tinted. The filter is calibrated so that bare stock under it
    reads the target's colour at the target's opacity (spec rgb at spec opacity over the stock); ink under it stays dark."""
    wx0, wx1, wy0, wy1 = win
    stock = S.stock_colour()
    tape = np.asarray(spec["rgb"], np.float32)
    f = (spec["opacity"] * tape + (1 - spec["opacity"]) * stock) / np.maximum(stock, 1.0)
    n = pc.value_noise(cov.shape, max(1.0, 1.5 * S.ppm), S.rng)
    f = f[None, None, :] * (0.97 + 0.06 * n[..., None])
    sub = S.rgb[wy0:wy1, wx0:wx1]
    a = (cov * S.alpha[wy0:wy1, wx0:wx1])[..., None]
    sub[:] = sub * (1 - a) + sub * f * a
    S.height[wy0:wy1, wx0:wx1] += (cov * 0.12).astype(np.float32)
    S.rough[wy0:wy1, wx0:wx1] = S.rough[wy0:wy1, wx0:wx1] * (1 - cov) + 0.35 * cov


def tape_tab(S, centre_mm, flip_x=False, flip_y=False, spec=None, lift=True):
    spec = spec or S.P.T["fixings"]["tape_tab"]
    pts = pc.tape_polygon(centre_mm, S.ppm, S.H, spec, flip_x, flip_y)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    win = S.win_of((min(xs), min(ys), max(xs), max(ys)), 3)
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255))
    tape_filter(S, win, cov, spec)
    return win, cov


def string_cue(S):
    """A rubber sucker and the knot of a string at the top-left; the loop rises from them past the top edge."""
    fx = S.P.T["fixings"]["string_sucker"]
    cx, cy = fx["sucker_centre_in_mm"]
    r = fx["sucker_diameter_mm"] / 2 * S.ppm
    px, py = cx * S.ppm, cy * S.ppm
    win = S.win_of((px - r - 4, py - r - 4, px + r + 4, py + r + 4))
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(px - r - ox) * ss, (py - r - oy) * ss, (px + r - ox) * ss, (py + r - oy) * ss], fill=255))
    S.tint(win, cov, fx["sucker_rgb"], fx["sucker_opacity"])
    # a lighter rim and a darker centre dimple
    gy, gx = np.mgrid[win[2]:win[3], win[0]:win[1]].astype(np.float32)
    rr = np.hypot(gx - px, gy - py) / r
    S.tint(win, cov * np.clip(1 - np.abs(rr - 0.78) * 7, 0, 1), (196, 196, 190), 0.5)
    S.tint(win, cov * np.clip(1 - rr * 3, 0, 1), (112, 112, 108), 0.5)
    wx0, wx1, wy0, wy1 = win
    S.height[wy0:wy1, wx0:wx1] += (cov * 0.9).astype(np.float32)
    # the knot: a small cream lump at the sucker's top edge, and the string running up to the card's top edge
    kr = fx["knot_mm"] / 2 * S.ppm
    kx, ky = px + 2 * S.ppm, py - r - kr * 0.6
    kwin = S.win_of((kx - kr - 3, ky - kr - 3, kx + kr + 3, ky + kr + 3))
    kc = pi.draw_cov(kwin, lambda d, ss, ox, oy: d.ellipse([(kx - kr - ox) * ss, (ky - kr - oy) * ss, (kx + kr - ox) * ss, (ky + kr - oy) * ss], fill=255))
    S.tint(kwin, kc, fx["string_rgb"], 1.0)
    wid = max(1.0, 1.4 * S.ppm)
    sw = S.win_of((kx - wid - 2, 0, kx + wid + 2, ky))
    sc_ = pi.draw_cov(sw, lambda d, ss, ox, oy: d.line([((kx - ox) * ss, (0 - oy) * ss), ((kx - ox) * ss, (ky - oy) * ss)], fill=255, width=max(1, int(wid * ss))))
    S.tint(sw, sc_, fx["string_rgb"], 0.95)
    S.tint(sw, sc_, (120, 114, 100), 0.18)
    S.log["string_cue"] = True


# ------------------------------------------------------------------------------------------ plates and boards
def bolt_head(S, x_mm, y_mm, d_mm=18, hole_mm=10, rust=True):
    px, py = x_mm * S.ppm, (S.H - y_mm) * S.ppm
    r = d_mm / 2 * S.ppm
    win = S.win_of((px - r - 6 * S.ppm, py - r - 6 * S.ppm, px + r + 6 * S.ppm, py + r + 6 * S.ppm))
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(px - r - ox) * ss, (py - r - oy) * ss, (px + r - ox) * ss, (py + r - oy) * ss], fill=255))
    gy, gx = np.mgrid[win[2]:win[3], win[0]:win[1]].astype(np.float32)
    rr = np.hypot(gx - px, gy - py) / r
    if rust:
        halo = np.clip(1 - (rr - 1) * r / (5 * S.ppm), 0, 1) * (rr >= 0.95)
        S.tint(win, halo.astype(np.float32), RUST, 0.45)
    shade = (0.82 + 0.35 * np.clip(1 - rr, 0, 1) ** 0.7 - 0.05 * (gx - px) / r)[..., None]
    sub = S.rgb[win[2]:win[3], win[0]:win[1]]
    sub[:] = sub * (1 - cov[..., None]) + np.asarray((118, 116, 112), np.float32) * shade * cov[..., None]
    S.height[win[2]:win[3], win[0]:win[1]] += (cov * 2.0 * np.clip(1 - rr, 0, 1) ** 0.5).astype(np.float32)
    S.rough[win[2]:win[3], win[0]:win[1]] = S.rough[win[2]:win[3], win[0]:win[1]] * (1 - cov) + 0.45 * cov


def chips(S, n, size_mm, near=None, edge_bias=0.7, colour=STEEL, halo_mm=(3, 8), halo_op=0.5, fade=1.0, spots=None):
    rng = S.rng
    done = 0
    for i in range(n):
        r = float(rng.uniform(size_mm[0], size_mm[1])) / 2 * S.ppm
        if spots and rng.random() < 0.55:
            sx, sy = spots[int(rng.integers(0, len(spots)))]
            x, y = sx * S.ppm + rng.normal(0, 7 * S.ppm), (S.H - sy) * S.ppm + rng.normal(0, 7 * S.ppm)
        elif rng.random() < edge_bias:
            e = int(rng.integers(0, 4))
            t = rng.uniform(0, 1)
            m_ = rng.uniform(1, 9) * S.ppm
            x, y = ((t * S.w, m_) if e == 0 else ((S.w - m_, t * S.h) if e == 1 else ((t * S.w, S.h - m_) if e == 2 else (m_, t * S.h))))
        else:
            x, y = rng.uniform(0, S.w), rng.uniform(0, S.h)
        x, y = float(np.clip(x, 0, S.w - 1)), float(np.clip(y, 0, S.h - 1))
        hm = float(rng.uniform(*halo_mm)) * S.ppm
        win, cov = S.blob(x, y, r + hm, 0.0)
        wx0, wx1, wy0, wy1 = win
        gy, gx = np.mgrid[wy0:wy1, wx0:wx1].astype(np.float32)
        rr = np.hypot(gx - x, gy - y)
        halo = np.clip(1 - (rr - r) / max(1.0, hm), 0, 1) * (rr >= r * 0.8) * (0.6 + 0.4 * pc.value_noise(rr.shape, 2 * S.ppm, rng))
        S.tint(win, halo.astype(np.float32), RUST, halo_op * fade)
        cw, cc = S.blob(x, y, r, 0.45)
        S.tint(cw, cc, colour, 0.95)
        S.height[cw[2]:cw[3], cw[0]:cw[1]] -= (cc * 0.12).astype(np.float32)
        S.rough[cw[2]:cw[3], cw[0]:cw[1]] = S.rough[cw[2]:cw[3], cw[0]:cw[1]] * (1 - cc) + 0.7 * cc
        done += 1
    S.log["chips"] = done


def lime_streak(S, width_mm=(20, 50), length_mm=(60, 140), colour=LIME, opacity=0.8, top=True):
    rng = S.rng
    x = rng.uniform(0.1, 0.9) * S.w
    S.streak(x, 0.0 if top else S.h * 0.3, rng.uniform(*length_mm) * S.ppm, rng.uniform(*width_mm) * S.ppm, colour, opacity, sway=0.3)
    S.log["lime"] = S.log.get("lime", 0) + 1


def grime_gradient(S, amount, bottom=True):
    ys = np.arange(S.h, dtype=np.float32) / S.h
    g = ys if bottom else 1 - ys
    m = (g ** 1.4)[:, None] * np.ones((1, S.w), np.float32)
    S.tint((0, S.w, 0, S.h), m, pc.GRIME, amount)


def crazing(S, x_mm, y_mm, n=3):
    rng = S.rng
    for _ in range(n):
        L = rng.uniform(10, 25) * S.ppm
        ang = rng.uniform(0, 2 * math.pi)
        px, py = x_mm * S.ppm, (S.H - y_mm) * S.ppm
        pts = [(px, py)]
        for _s in range(6):
            ang += rng.normal(0, 0.5)
            px += math.cos(ang) * L / 6
            py += math.sin(ang) * L / 6
            pts.append((px, py))
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        win = S.win_of((min(xs), min(ys), max(xs), max(ys)), 3)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.line([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255, width=max(1, int(0.35 * S.ppm * ss))))
        S.tint(win, cov, (50, 46, 44), 0.55)


# ------------------------------------------------------------------------------------------ the tables
WEAR_OVERRIDE = {("P02", "A"): "glass_bill"}      # the target hangs P02 in the cottage window (SF9) taped inside the glass: it is not a pasted bill there


def apply(S, table, cls):
    it = S.item
    table = WEAR_OVERRIDE.get((it["id"], cls), table)
    if it["process"] == "plastic_print":
        table = "plastic_card"
    rng = S.rng
    ci = S.ci
    R = S.P.T["age_rules"]["paper_wear"]
    fx = S.P.T["fixings"]
    process = it["process"]
    mc = it.get("mirror_cue")
    fixk = (it.get("fixing") or {}).get("kind", "")
    if table in ("bill_pasted", "glass_bill", "notice_sleeve", "sticker"):
        amp = R["wrinkle"]["amplitude_mm"]
        a = amp[0] + (amp[1] - amp[0]) * ci / 3.0
        if table == "sticker":
            a *= 0.3
        if ci > 0 or table != "sticker":
            cockle(S, a if ci > 0 else amp[0] * 0.6, rng.uniform(*R["wrinkle"]["wavelength_mm"]), aniso=2.2 if table == "bill_pasted" else 1.4)
            S.shade(0.10)
    if table == "bill_pasted":
        corner_lifts(S, [0, 1, 1, 2][ci] if ci else 0, 15, 60)
        rain_runs(S, [0, 3, 5, 8][ci], opac=(0.25, 0.40), length=(30, 80), width=(0.9, 1.5))      # visible from the pavement: the top of the target's ranges
        if ci >= 2:
            paste_halo(S)
        loss_and_tears(S, [(0, 0), tuple(R["loss"]["class_B"]), tuple(R["loss"]["class_C"]), tuple(R["loss"]["class_D"])][ci], [0, 0 if rng.random() < 0.6 else 1, 2, 3][ci])
        S.rough[:] = np.minimum(S.rough, 0.9)
    elif table == "glass_bill":
        condensation(S)
        curl_out(S)
        if it["format"]["w_mm"] >= 200:
            four_tabs(S)
        S.rough[:] = S.rough * 0.85
    elif table == "notice_sleeve":
        sleeve(S)
        if it["id"] == "C01a":
            four_tabs(S)               # the appeal hangs inside the empty unit's glass, taped by four tabs (the target's placement)
    elif table == "plastic_card":
        # a printed plastic card on a chain: no folds, no curl, no bleaching, no finger smudge; scratches, a little grime (at most 5 per cent) and the sheen of the plastic
        scratches(S, int(rng.integers(6, 21)), width_mm=(0.2, 0.5), length_mm=(5, 40))
        grime_gradient(S, 0.04 * ci / 1.0 if ci else 0.0)
        S.shade(0.04)
    elif table == "card_felt":
        if ci:
            dog_ears(S, int(rng.integers(0, 3)))
            smudge(S, int(rng.integers(0, 2)))
            bleach(S, 1 / 3, 0.04 + 0.03 * ci)
        warp(S, 1.5)
        S.shade(0.08)
    elif table == "card_ballpoint":
        curl(S, float(rng.uniform(1, 3)))
        S.shade(0.08)
        if ci:
            bleach(S, 1 / 3, 0.03 * ci)
    elif table == "sticker":
        if ci:
            corner_lifts(S, 1, 8, 20)
            scratches(S, int(rng.integers(0, 5)))
            ranges = {"B": (0, 0), "C": (0.05, 0.15), "D": (0.30, 0.60)}
            loss_and_tears(S, ranges[cls], 0)
    elif table == "enamel_plate":
        enamel_plate(S, it)
    elif table == "cast_aluminium_plate":
        cast_plate(S, it)
    elif table == "pressed_plate":
        pressed_plate(S, it)
    elif table == "letting_board":
        letting_board(S, it)
    # photocopier artefacts and fixings belong to the print and the way it hangs
    if process in ("photocopy_a3", "photocopy_a4"):
        photocopy_artefacts(S, process)
    if mc:
        if mc["kind"] == "tape":
            tape_tab(S, mc["tab_centre_mm"])
        else:
            string_cue(S)
    elif fixk == "string":
        string_cue(S)
    S.height += 0.0


TAB_SCALE = {"P02": 1 / 0.585}       # P02 is shown at 0.585 of its size in the cottage window (SF9): its tabs are drawn 1/0.585 bigger so that they are the target's 38 x 16 mm on the glass


def four_tabs(S):
    """A sheet taped in a window by four tabs, one across each corner (the target's four_tabs)."""
    fx = S.P.T["fixings"]["four_tabs"]
    k = TAB_SCALE.get(S.item["id"], 1.0)
    spec = dict(length_mm=fx["length_mm"] * k, width_mm=fx["width_mm"] * k, angle_deg=fx["angle_deg"], rgb=fx["rgb"], opacity=fx["opacity"])
    c = [v * k for v in S.P.T["fixings"]["tape_tab"]["centre_in_mm"]]
    for right in (False, True):
        for bottom in (False, True):
            cx = S.W - c[0] if right else c[0]
            cy_up = c[1] if bottom else S.H - c[1]
            tape_tab(S, (cx, cy_up), flip_x=right, flip_y=bottom, spec=spec)
    S.log["tabs"] = 4


def sleeve(S):
    """A clear polythene sleeve cable-tied to a column: a crease, fog and water beads low down, two ties, the sheet slid down inside it."""
    rng = S.rng
    it = S.item
    # fog on the inside, lower third
    ys = np.arange(S.h, dtype=np.float32) / S.h
    f = np.clip((ys - 0.62) / 0.38, 0, 1)
    n = pc.value_noise((S.h, S.w), 14 * S.ppm, rng, octaves=2)
    fog = f[:, None] * (0.55 + 0.45 * n)
    S.tint((0, S.w, 0, S.h), fog.astype(np.float32), (232, 236, 238), float(rng.uniform(0.10, 0.30)))
    # a crease or two across the sleeve
    for _ in range(int(rng.integers(1, 3))):
        y = rng.uniform(0.15, 0.85) * S.h
        sl = rng.uniform(-0.02, 0.02)
        x = np.arange(S.w, dtype=np.float32)
        yy = y + sl * x
        wid = max(1.0, 0.7 * S.ppm)
        win = (0, S.w, int(max(0, yy.min() - 3 * wid)), int(min(S.h, yy.max() + 3 * wid)))
        gy = np.arange(win[2], win[3], dtype=np.float32)[:, None]
        d = np.abs(gy - yy[None, :]) / wid
        m = np.clip(1 - d, 0, 1).astype(np.float32) * (0.5 + 0.5 * pc.value_noise((win[3] - win[2], S.w), 25 * S.ppm, rng))
        lum = S.rgb[win[2]:win[3], win[0]:win[1]].mean(-1) / 255.0
        S.tint(win, m * (0.3 + 0.7 * np.clip(lum, 0, 1)), (250, 250, 248), 0.55)        # a glint on the polythene lightens dark ink less than paper
        S.tint(win, np.roll(m, int(wid * 1.5), axis=0), (60, 60, 60), 0.10)
    # water beads, lower third
    for _ in range(int(rng.integers(6, 21))):
        r = rng.uniform(1.0, 3.0) * S.ppm
        x, y = rng.uniform(0.05, 0.95) * S.w, rng.uniform(0.66, 0.97) * S.h
        win = S.win_of((x - r - 2, y - r - 2, x + r + 2, y + r + 2))
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(x - r - ox) * ss, (y - r - oy) * ss, (x + r - ox) * ss, (y + r - oy) * ss], fill=255))
        gy, gx = np.mgrid[win[2]:win[3], win[0]:win[1]].astype(np.float32)
        rr = np.hypot(gx - x, gy - y) / r
        S.tint(win, cov * np.clip(1 - np.abs(rr - 0.85) * 6, 0, 1), (60, 62, 66), 0.30)
        lum = S.rgb[win[2]:win[3], win[0]:win[1]].mean(-1) / 255.0
        S.tint(win, cov * np.clip(1 - np.hypot(gx - x + 0.35 * r, gy - y + 0.35 * r) / (0.4 * r), 0, 1) * (0.3 + 0.7 * np.clip(lum, 0, 1)), (255, 255, 255), 0.7)
        S.height[win[2]:win[3], win[0]:win[1]] += (cov * 0.25).astype(np.float32)
    S.rough[:] = np.minimum(S.rough, 0.25)
    # the sheet has slid down inside: a clear band at the top, a highlight along its lower edge (kept inside the top margin)
    top_margin_mm = S.H - it["safe_mm"][3]
    slide = min(float(rng.uniform(5, 20)), max(0.0, top_margin_mm - 3.0))
    if slide > 1.0:
        band = int(slide * S.ppm)
        S.alpha[:band] *= 0.18
        win = (0, S.w, max(0, band - int(1.2 * S.ppm)), min(S.h, band + int(1.2 * S.ppm)))
        S.tint(win, np.ones((win[3] - win[2], S.w), np.float32), (250, 250, 248), 0.65)
        S.log["slide_mm"] = slide
    # two cable ties through the sleeve's top corners, their tails left uncut
    for side in (0, 1):
        x = (9.0 if side == 0 else S.W - 9.0)
        tail = float(rng.uniform(40, 90))
        px = x * S.ppm
        win = S.win_of((px - 3 * S.ppm, 0, px + 3 * S.ppm, (4 + min(tail, 14)) * S.ppm))
        m = pi.rect_cov((px - 2.0 * S.ppm, 0, px + 2.0 * S.ppm, 9 * S.ppm), win)
        S.tint(win, m, (74, 76, 78), 0.95)
        S.height[win[2]:win[3], win[0]:win[1]] += (m * 0.5).astype(np.float32)
    S.log["sleeve"] = True


def dog_ears(S, n):
    rng = S.rng
    done = 0
    for _ in range(n * 6):
        if done >= n:
            break
        c = int(rng.integers(0, 4))
        r = float(rng.uniform(6, 14)) * 1.4
        rr = r * S.ppm
        box = (0 if c in (0, 3) else S.w - rr, 0 if c in (0, 1) else S.h - rr, rr if c in (0, 3) else S.w, rr if c in (0, 1) else S.h)
        if S.hits_text(box, wide=True) or c == 0:             # the top-left corner carries the tape: keep the fold off it
            continue
        corner_lift(S, c, r)
        done += 1
    S.log["dog_ears"] = done


def smudge(S, n):
    """A finger smudge: a warm oval 12 x 18 mm, 3 to 5 per cent darker (multiply 0.97, 0.96, 0.94), within 15 mm of the bottom edge or of the tab, kept off the lettering."""
    rng = S.rng
    for _ in range(n):
        for _t in range(30):
            if rng.random() < 0.5:
                x, y = rng.uniform(0.15, 0.85) * S.W, S.H - rng.uniform(4, 15)
            else:
                x, y = rng.uniform(22, 40), rng.uniform(6, 22)
            ang = rng.uniform(0, math.pi)
            ra, rb = 9.0 * S.ppm, 6.0 * S.ppm
            px, py = x * S.ppm, y * S.ppm
            if not S.hits_text((px - ra, py - ra, px + ra, py + ra), 1.0):
                break
        else:
            continue
        win = S.win_of((px - ra - 4, py - ra - 4, px + ra + 4, py + ra + 4))
        gy, gx = np.mgrid[win[2]:win[3], win[0]:win[1]].astype(np.float32)
        c, s_ = math.cos(ang), math.sin(ang)
        u = ((gx - px) * c + (gy - py) * s_) / ra
        v = (-(gx - px) * s_ + (gy - py) * c) / rb
        m = np.clip(1.0 - np.sqrt(u * u + v * v), 0, 1) ** 0.7
        d = float(rng.uniform(0.03, 0.05))
        wx0, wx1, wy0, wy1 = win
        mult = np.asarray((0.97, 0.96, 0.94), np.float32)
        sub = S.rgb[wy0:wy1, wx0:wx1]
        sub[:] = sub * (1 - m[..., None] * (1 - mult[None, None, :]) * (d / 0.05))
        S.log["smudge"] = True


def warp(S, mm):
    n = pc.value_noise((S.h, S.w), 70 * S.ppm, S.rng)
    S.height += ((n - 0.5) * 2 * mm).astype(np.float32)


def curl(S, mm):
    xs = np.arange(S.w, dtype=np.float32) / S.w
    S.height += (np.clip(xs - 0.6, 0, 1) / 0.4 * mm)[None, :].astype(np.float32)


def scratches(S, n, width_mm=(0.3, 0.5), length_mm=(10, 40)):
    rng = S.rng
    for _ in range(n):
        x, y = rng.uniform(0.1, 0.9) * S.w, rng.uniform(0.1, 0.9) * S.h
        L = rng.uniform(*length_mm) * S.ppm
        a = rng.uniform(0, math.pi)
        wd = rng.uniform(*width_mm)
        x2, y2 = x + L * math.cos(a), y + L * math.sin(a)
        win = S.win_of((min(x, x2), min(y, y2), max(x, x2), max(y, y2)), 3)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.line([((x - ox) * ss, (y - oy) * ss), ((x2 - ox) * ss, (y2 - oy) * ss)], fill=255, width=max(1, int(wd * S.ppm * ss))))
        S.tint(win, cov, (240, 238, 230), 0.55)


def enamel_plate(S, it):
    """H01, H02: vitreous enamel on steel: chips to black steel with a rust halo (at the corners, edges and bolts first), crazing near the bolts, rust tears, bird lime, salt bloom (H02)."""
    W = S.P.T["wear_tables"]["enamel_plate"]
    rng = S.rng
    holes = it["fixing"]["holes_mm"]
    k = {"A": 0.0, "B": 0.45, "C": 0.75, "D": 1.0}[S.cls]
    for hx, hy in holes:
        bolt_head(S, hx, hy, 18, 10, rust=S.cls in ("C", "D"))
        if S.cls != "A":
            crazing(S, hx, hy, 3)
    chips(S, int(round(rng.integers(12, 31) * k)), (2, 9), edge_bias=0.65, spots=holes, fade=k)
    if S.cls in ("C", "D"):
        for hx, hy in [h for h in holes if h[1] < S.H / 2]:
            px = hx * S.ppm
            S.streak(px, (S.H - hy) * S.ppm + 8 * S.ppm, (S.H - hy) * S.ppm + rng.uniform(150, 400) * S.ppm * (0.6 + 0.4 * k), rng.uniform(6, 14) * S.ppm, RUST, 0.30 * k + 0.1, sway=0.5)
        lime_streak(S)
    if it["id"] == "H02":
        n = pc.value_noise((S.h, S.w), 3 * S.ppm, rng, octaves=2)
        ys = np.arange(S.h, dtype=np.float32)
        band = np.clip(1 - (S.h - 1 - ys) / (rng.uniform(10, 22) * S.ppm), 0, 1) ** 1.2
        S.tint((0, S.w, 0, S.h), (band[:, None] * (n > 0.35) * n).astype(np.float32), (236, 234, 226), 0.55 * max(k, 0.4))
    grime_gradient(S, 0.04 + 0.05 * k)
    S.shade(0.05)


def raised_mask(S):
    """Boolean mask of the plate's raised letters and border (from the elements that carry a raised height)."""
    m = np.zeros((S.h, S.w), np.float32)
    for e in S.geo.elems:
        if e.raised:
            wx0, wx1, wy0, wy1 = e.win
            m[wy0:wy1, wx0:wx1] = np.maximum(m[wy0:wy1, wx0:wx1], e.cov)
    return m


def angular_flakes(S, rm, share):
    """The paint of the raised faces lifting as angular flakes of 2 to 12 mm (five to seven straight sides), twice as dense on the upper half of each letter, until `share` of the plate is bare."""
    rng = S.rng
    lab, n = ndi.label(rm > 0.5)
    ys, xs = np.nonzero(rm > 0.5)
    if not len(ys):
        return np.zeros((S.h, S.w), np.float32)
    objs = ndi.find_objects(lab)
    top = np.zeros(n + 1); bot = np.zeros(n + 1)
    for i, sl in enumerate(objs, 1):
        top[i], bot[i] = sl[0].start, sl[0].stop
    comp = lab[ys, xs]
    mid = (top[comp] + bot[comp]) / 2.0
    wgt = np.where(ys < mid, 2.0, 1.0)
    wgt = wgt / wgt.sum()
    ss = 3
    im = Image.new("L", (S.w * ss, S.h * ss), 0)
    d = ImageDraw.Draw(im)
    area_px = share * S.w * S.h
    got = 0.0
    tries = 0
    while got < area_px and tries < 6000:
        tries += 1
        i = rng.choice(len(ys), p=wgt)
        cx, cy = xs[i] + rng.random(), ys[i] + rng.random()
        r = rng.uniform(1.0, 6.0) * S.ppm
        m = int(rng.integers(5, 8))
        ang = np.sort(rng.uniform(0, 2 * math.pi, m))
        rad = r * rng.uniform(0.45, 1.0, m)
        pts = [((cx + rr * math.cos(a)) * ss, (cy + rr * math.sin(a) * rng.uniform(0.5, 1.0)) * ss) for rr, a in zip(rad, ang)]
        d.polygon(pts, fill=255)
        got += 0.5 * m * rad.mean() ** 2 * math.sin(2 * math.pi / m) * 0.7
    a_ = np.asarray(im.resize((S.w, S.h), Image.BOX)).astype(np.float32) / 255.0
    return a_ * (rm > 0.5)


def cast_plate(S, it):
    """S01 n and d: cast aluminium, letters and border raised 3 mm, painted: the paint lifts first at the raised edges, a grime gradient, a rust run under each screw, bird lime on the top border."""
    rng = S.rng
    rm = raised_mask(S)
    edge = np.clip(ndi.grey_dilation(rm, size=(int(1.2 * S.ppm) * 2 + 1,) * 2) - ndi.grey_erosion(rm, size=(int(1.2 * S.ppm) * 2 + 1,) * 2), 0, 1)
    edge = pc.smooth(edge, 1.5 * S.ppm)
    share = float(rng.uniform(0.03, 0.06)) * {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls]
    if share > 0 and rm.sum() > 0:
        flake = angular_flakes(S, rm, share)
        bloom = np.clip(ndi.grey_dilation(flake, size=(int(0.8 * S.ppm) * 2 + 1,) * 2) - flake, 0, 1)
        S.tint((0, S.w, 0, S.h), bloom * (1 - flake), (170, 168, 160), 0.30)
        S.tint((0, S.w, 0, S.h), flake, ALUM, 0.95)
        S.metal = np.maximum(S.metal, flake)
        S.rough[:] = S.rough * (1 - flake * 0.5) + 0.35 * flake * 0.5
        S.height -= (flake * 0.15).astype(np.float32)
        S.log["flake_share"] = float((flake > 0.5).mean())
    grime_gradient(S, 0.12 * {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls])
    if S.cls in ("C", "D"):
        for hx, hy in it["fixing"]["holes_mm"]:
            bolt_head(S, hx, hy, 14, 10, rust=True)
            if hy < S.H / 2:
                S.streak(hx * S.ppm, (S.H - hy) * S.ppm + 6 * S.ppm, (S.H - hy) * S.ppm + rng.uniform(20, 80) * S.ppm * 2.2, rng.uniform(5, 11) * S.ppm, RUST, 0.30, sway=0.4)
        for _ in range(int(rng.integers(1, 3))):
            x = rng.uniform(0.1, 0.9) * S.w
            S.streak(x, 0, rng.uniform(22, 50) * S.ppm, rng.uniform(20, 50) * S.ppm, LIME, 0.6, sway=0.2)
    S.shade(0.05)


def pressed_plate(S, it):
    """S02 and S03: stove enamel on aluminium or vitreous enamel on steel: chips at the corners and screws only (4 to 12 of 2 to 6 mm), a grime gradient, no flaking of the letters."""
    rng = S.rng
    k = {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls]
    holes = it["fixing"]["holes_mm"]
    for hx, hy in holes:
        bolt_head(S, hx, hy, 14, 10, rust=S.cls == "D")
    corners = [(6, 6), (S.W - 6, 6), (6, S.H - 6), (S.W - 6, S.H - 6)]
    chips(S, int(round(rng.integers(4, 13) * max(k, 0.3))), (2, 6), edge_bias=0.0, spots=corners + holes, fade=k, halo_mm=(1, 4), halo_op=0.35)
    grime_gradient(S, 0.10 * k)
    S.shade(0.04)


def peel_bites(S, n, length_mm=(20, 80), depth_mm=(3, 15), colour=(150, 145, 135)):
    """Separate bites of the paint peeled from the foot of a board: grey plywood showing, ragged, the rest of the edge painted."""
    rng = S.rng
    for _ in range(n):
        L = rng.uniform(*length_mm) * S.ppm
        D = rng.uniform(*depth_mm) * S.ppm
        cx = rng.uniform(0.08, 0.92) * S.w
        m = 24
        u = np.linspace(-1, 1, m)
        prof = np.clip(1 - np.abs(u) ** 1.7, 0, 1) ** 0.6 * (0.65 + 0.35 * rng.random(m))
        pts = [(cx + ui * L / 2, S.h + 1 - D * p) for ui, p in zip(u, prof)] + [(cx + L / 2 + 1, S.h + 2), (cx - L / 2 - 1, S.h + 2)]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        win = S.win_of((min(xs), min(ys), max(xs), max(ys)), 3)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255))
        S.tint(win, cov, colour, 0.95)
        S.height[win[2]:win[3], win[0]:win[1]] -= (cov * 0.2).astype(np.float32)
    S.log["peel_bites"] = n


def letting_board(S, it):
    """L01 to L04: painted board: grime streaks from the top edge (15 to 60 mm wide at the top, tapering to 5 to 20, 80 to 250 mm long, 4 to 10 per cent darker, feathered, 2 to 5 to the metre and
    uneven, strongest under the top screws), rust runs under the screws, 2 to 4 separate peeled bites on the foot, algae along the foot (D)."""
    rng = S.rng
    k = {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls]
    W_ = S.W
    sx = [40, W_ - 40]
    sy = [40, S.H - 40]
    for x in sx:
        for y in sy:
            bolt_head(S, x, y, 14 if W_ < 700 else 16, 8, rust=True)
    n_streak = max(2, int(round(rng.uniform(2, 5) * W_ / 1000.0)))
    for i in range(n_streak):
        if i < 2:                              # strongest under the top screws
            x = (sx[i] + rng.normal(0, 25)) * S.ppm
            op = float(rng.uniform(0.09, 0.14))
        else:
            x = rng.uniform(0.08, 0.92) * S.w
            op = float(rng.uniform(0.05, 0.10))
        w_top = rng.uniform(15, 60)
        S.streak(x, 0, rng.uniform(80, 250) * S.ppm, w_top * S.ppm, (48, 44, 38), op, sway=0.5, end_frac=rng.uniform(5, 20) / w_top)
    for x in sx:
        L = rng.uniform(40, 140) * S.ppm
        S.streak(x * S.ppm, (S.H - 40) * S.ppm + 6 * S.ppm, (S.H - 40) * S.ppm + L, rng.uniform(4, 9) * S.ppm, RUST, 0.32, sway=0.4)
    peel_bites(S, int(rng.integers(2, 5)))
    ys, xs = np.mgrid[0:S.h, 0:S.w].astype(np.float32)
    if S.cls == "D":
        n = pc.value_noise((S.h, S.w), 5 * S.ppm, rng, octaves=2)
        g = np.clip(1 - (S.h - 1 - ys) / (20 * S.ppm), 0, 1) * (0.5 + 0.5 * n)
        S.tint((0, S.w, 0, S.h), g.astype(np.float32), (62, 78, 52), 0.3)
    grime_gradient(S, 0.05 * k, bottom=True)
    S.shade(0.05)
