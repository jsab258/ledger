"""paper_ink.py: an item's geometry and its inks, class-free (unit 4.2 to 4.4, cloud week 42).

build(sc, gl, P, item, seed) lays every shape and every line of lettering of one item at the item's own pixel scale and returns an `ItemGeo`: the card's alpha, an
ordered list of elements (a float coverage in a window, the colour it is printed in, how dense, whether it has a darker rim), the glyph manifests, the registration offsets and the
height each process leaves. Nothing here ages anything: paper_render.py takes the elements and a class and makes the colours.

The look of each process follows target.json `processes`; what the numbers of the target are not specific about is in LOOK below, each with its reason.
"""
import math

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import paper_common as pc

# Per process: edge blur sigma (mm), ink density loss by mottle (amount, feature size mm), rim (letterpress: a darker rim at the letter edges), rag (mm, edge roughness),
# film (mm: the height the ink leaves, + raised, - pressed in), rough (the ink's own roughness for the ORM map), pin (pinholes per cm2, diameter mm).
LOOK = {
    "screen_2col": dict(sigma=0.15, mottle=(0.06, 7), film=0.03, rough=0.55, pin=(0.02, (0.2, 0.5))),
    "screen_1col": dict(sigma=0.15, mottle=(0.06, 7), film=0.03, rough=0.55, pin=(0.02, (0.2, 0.5))),
    "letterpress_2col": dict(sigma=0.12, mottle=(0.12, 5), rim=0.16, rag=0.2, film=-0.06, rough=0.80),
    "letterpress_1col": dict(sigma=0.12, mottle=(0.12, 5), rim=0.16, rag=0.2, film=-0.06, rough=0.80),
    "litho_4col": dict(sigma=0.10, mottle=(0.04, 5), grain=0.03, film=0.01, rough=0.70),
    "litho_2col": dict(sigma=0.10, mottle=(0.04, 5), film=0.01, rough=0.70),
    "photocopy_a4": dict(sigma=0.12, density=0.92, fat=0.06, film=0.01, rough=0.60),
    "photocopy_a3": dict(sigma=0.12, density=0.92, fat=0.06, film=0.01, rough=0.60),
    "typed_carbon": dict(sigma=0.10, strike=(0.88, 1.0), film=0.01, rough=0.55),
    "felt_pen": dict(sigma=0.22, pool=0.14, film=0.0, rough=0.65),
    "ballpoint_card": dict(sigma=0.12, pressure=0.25, blots=True, film=0.0, rough=0.45),     # the density along the stroke 0.75 to 1.0 (the close review)
    "sticker_print": dict(sigma=0.10, mottle=(0.03, 5), film=0.01, rough=0.45),
    "plastic_print": dict(sigma=0.10, film=0.01, rough=0.30),
    "enamel": dict(sigma=0.08, film=0.0, rough=0.12),
    "vitreous_enamel_steel": dict(sigma=0.08, film=0.0, rough=0.12),
    "agent_board": dict(sigma=0.10, film=0.05, rough=0.35),
    "cast_aluminium_raised": dict(sigma=0.20, film=0.0, rough=0.50),
    "pressed_aluminium_enamel": dict(sigma=0.15, film=0.0, rough=0.30),
}
SECOND_PASS_INKS = ("red", "blue")
REG_PROCESSES = ("screen_2col", "letterpress_2col", "litho_2col")
ART_STANDINS = "the picture the image model is to make: a flat stand-in in the target's nominal colour"


class Elem(object):
    __slots__ = ("id", "kind", "win", "cov", "spec", "dens", "rim", "film", "rough", "second", "cap", "hand", "tech", "block", "raised")

    def __init__(self, id, kind, win, cov, spec, dens=None, rim=None, film=0.0, rough=None, second=False, cap=0.0, hand=None, tech=None, block=None, raised=0.0):
        self.id, self.kind, self.win, self.cov, self.spec, self.dens, self.rim = id, kind, win, cov, spec, dens, rim
        self.film, self.rough, self.second, self.cap, self.hand, self.tech, self.block, self.raised = film, rough, second, cap, hand, tech, block, raised


class ItemGeo(object):
    pass


# ------------------------------------------------------------------------------------------ coverage helpers
def rect_cov(box_px, win):
    """Exact fractional coverage of an axis-aligned box (x0, y0, x1, y1 in canvas pixels, row 0 the top) inside the window (x0, x1, y0, y1)."""
    wx0, wx1, wy0, wy1 = win
    x0, y0, x1, y1 = box_px
    xs = np.arange(wx0, wx1, dtype=np.float32)
    ys = np.arange(wy0, wy1, dtype=np.float32)
    cx = np.clip(np.minimum(xs + 1, x1) - np.maximum(xs, x0), 0, 1)
    cy = np.clip(np.minimum(ys + 1, y1) - np.maximum(ys, y0), 0, 1)
    return (cy[:, None] * cx[None, :]).astype(np.float32)


def draw_cov(win, drawer, ss=4):
    """Coverage of anything PIL can draw (a callable taking (ImageDraw, scale, ox, oy)) inside the window, supersampled by ss."""
    wx0, wx1, wy0, wy1 = win
    w, h = wx1 - wx0, wy1 - wy0
    if w <= 0 or h <= 0:
        return np.zeros((max(h, 0), max(w, 0)), np.float32)
    ss = ss if w * h * ss * ss <= 40e6 else (2 if w * h * 4 <= 40e6 else 1)
    im = Image.new("L", (w * ss, h * ss), 0)
    d = ImageDraw.Draw(im)
    drawer(d, ss, wx0, wy0)
    a = np.asarray(im, dtype=np.float32) / 255.0
    if ss > 1:
        a = a.reshape(h, ss, w, ss).mean(axis=(1, 3))
    return a


def smoothstep(x):
    x = np.clip(x, 0, 1)
    return x * x * (3 - 2 * x)


def px_box(box_mm, ppm, H):
    x0, y0, x1, y1 = box_mm
    return (x0 * ppm, (H - y1) * ppm, x1 * ppm, (H - y0) * ppm)


def window_around(box, shape, pad):
    x0, y0, x1, y1 = box
    return (int(max(0, math.floor(x0 - pad))), int(min(shape[1], math.ceil(x1 + pad))), int(max(0, math.floor(y0 - pad))), int(min(shape[0], math.ceil(y1 + pad))))


# ------------------------------------------------------------------------------------------ the fill of a shape
def shape_spec(item, s):
    """(type, key) of the colour a shape is printed or painted in: ink / paint / stock, by the shape's fill_kind (the table of the target's palette), and the few named by their own word."""
    k, f = s.get("fill_kind"), s.get("fill")
    if k in ("ink", "paint", "stock"):
        if k == "stock" or f == "paper":
            return ("ink", "paper")
        return (k, f)
    if f == "black":
        return ("ink", "black")
    if f == "white":
        return ("stockkey", "white_card")
    if f == "buff_card":
        return ("stockkey", "buff_card")
    if f == "brass":
        return ("paint", "brass")
    if f == "paper":
        return ("ink", "paper")
    raise ValueError("fill of shape %s on %s is not understood: %r %r" % (s["id"], item["id"], k, f))


# ------------------------------------------------------------------------------------------ lettering
def reg_offset(rng):
    """The second colour's registration offset, kept inside what the target's own line reader holds: 0.28 to 0.36 mm along the line and 0.05 to 0.25 mm up (the bottom of the target's process range,
    0.3 to 0.8: at 4 px/mm a print line shifted by more than about 0.4 mm from its layout fails the reader's .mask)."""
    sx = 1 if rng.random() < 0.5 else -1
    sy = 1 if rng.random() < 0.5 else -1
    return (sx * float(rng.uniform(0.28, 0.36)), sy * float(rng.uniform(0.05, 0.25)))


# A person's line (the close review's finding 3): the target's `jitter_glyphs` draws every glyph's baseline and size on its own (ballpoint: baseline sd 0.6 mm, size sd 0.06), so the
# letters jump one by one. Here the baseline is a slope per line, one slow wave and a small per-glyph wobble, and the size varies per word with a smaller per-glyph part; every draw is
# clipped at 3 sd as the target's are, and the whole stays inside the target's hand envelope (`envelope_problems`), which the check proves.
HAND = dict(slope_sd_deg=0.5, wave_mm=0.4, wave_len_mm=(60.0, 120.0), glyph_sd_cap=0.03, word_size_sd=0.03, glyph_size_sd=0.025, rotation_sd_deg=0.8)
BALLPOINT_EMB_MM = -0.2       # a ballpoint line is 0.3 to 0.45 mm wide: Patrick Hand's own stroke (about 0.85 mm at a 4.4 mm cap) thinned by 0.2 mm on each side


def hand_glyphs(sc, b, rng):
    """The manifest of a HAND block by the smooth model above (the target's layout, word gaps by the hand style's word_gap_sd)."""
    hs = sc.T["hand_styles"][b["hand"]]
    base = sc.layout_glyphs(b)
    f = sc.font(b["font"], b["weight"], b["size_px_per_em"] * sc.LAYOUT_PPM)

    def n(sd):
        return float(np.clip(rng.normal(0, sd), -3 * sd, 3 * sd))
    slope = math.tan(math.radians(n(HAND["slope_sd_deg"])))
    lam = float(rng.uniform(*HAND["wave_len_mm"]))
    ph = float(rng.uniform(0, 2 * math.pi))
    amp = HAND["wave_mm"] * float(rng.uniform(0.6, 1.0))
    xs = [e["ox_mm"] for e in base]
    xc = (min(xs) + max(xs)) / 2.0 if xs else 0.0
    lim = 0.85 * (3.5 * hs["baseline_sd_mm"] + 0.6)          # inside the target's envelope with a margin
    emb = BALLPOINT_EMB_MM if b["hand"] == "ballpoint" else hs["embolden_mm"]
    out, drift = [], 0.0
    word = 1.0 + n(HAND["word_size_sd"])
    for e in base:
        if e["ch"] == " ":
            drift += f.getlength(" ") / sc.LAYOUT_PPM * n(hs["word_gap_sd"])
            word = 1.0 + n(HAND["word_size_sd"])
            out.append(dict(e, ox_mm=e["ox_mm"] + drift))
            continue
        s = word * (1.0 + n(HAND["glyph_size_sd"]))
        s = float(np.clip(s, 1 - 3.0 * hs["size_sd"], 1 + 3.0 * hs["size_sd"]))
        adv = f.getlength(e["ch"]) / sc.LAYOUT_PPM
        x = e["ox_mm"] + drift
        dy = slope * (x - xc) + amp * math.sin(2 * math.pi * x / lam + ph) + n(HAND["glyph_sd_cap"] * b["cap_mm"])
        dy = float(np.clip(dy, -lim, lim))
        out.append(dict(e, ox_mm=x, em_mm=e["em_mm"] * s, baseline_mm=e["baseline_mm"] + dy, rot_deg=n(HAND["rotation_sd_deg"]), emb_mm=emb))
        drift += (s - 1.0) * adv
    shift = -drift / 2.0 if b["anchor"] == "centre" else (-drift if b["anchor"] == "right" else 0.0)
    return [dict(e, ox_mm=e["ox_mm"] + shift) for e in out]


def pick_reg_offset(sc, gl, item, seed, ppm, shp, tries=8):
    """The second colour's offset, drawn from reg_offset, kept only if the target's own reader still reads every line with it (its glyph check holds less than the process's 0.3 mm at
    4 px/mm in some directions: F01's red lines failed at two of five seeds); else the next draw. Returns (offset, draws taken)."""
    rng = pc.rng_for(seed, item["id"], "register")
    H = item["format"]["h_mm"]
    imprints = {b["id"] for b in item["blocks"] if b.get("role") == "imprint"}
    off = (0.0, 0.0)
    for t in range(tries):
        off = reg_offset(rng)
        canvas = np.zeros(shp, bool)
        man = {}
        for b in item["blocks"]:
            if b.get("ghost"):
                continue
            o = off if b["ink"] in SECOND_PASS_INKS else (0.0, 0.0)
            g = lay_block(sc, b, pc.rng_for(seed, item["id"], "block", b["id"]), o)
            man[b["id"]] = g
            win = block_window(item, b, shp, ppm)
            canvas[win[2]:win[3], win[0]:win[1]] |= paste_block(sc, gl, g, ppm, H, win)
        fails = [f for f in sc.all_pixel_checks(item, canvas, man) if not f.startswith(".clean") and f.split(" ")[0] not in imprints]
        if not fails:
            return off, t + 1
    return off, tries


def lay_block(sc, b, rng, off=(0.0, 0.0)):
    """The manifest of one block (the target's own layout or a person's hand, plus the registration offset)."""
    g = hand_glyphs(sc, b, rng) if b.get("hand") else sc.layout_glyphs(b)
    if off != (0.0, 0.0):
        g = [dict(e, ox_mm=e["ox_mm"] + off[0], baseline_mm=e["baseline_mm"] + off[1]) for e in g]
    return g


def glyph_patch(sc, g, ppm):
    """The glyph's patch, by the target's own glyph maker (a negative emb_mm thins the stroke: the target's glyphlib takes it since the close review)."""
    return sc.glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm, g["rot_deg"], g["emb_mm"])


def paste_block(sc, gl, glyphs, ppm, H, win):
    wx0, wx1, wy0, wy1 = win
    canvas = np.zeros((wy1 - wy0, wx1 - wx0), bool)
    for g in glyphs:
        if g["ch"] == " ":
            continue
        patch, ox, base = glyph_patch(sc, g, ppm)
        gl.paste_or(canvas, patch, ox, base, g["ox_mm"] * ppm - wx0, (H - g["baseline_mm"]) * ppm - wy0)
    return canvas


INK_EDGE = 100.0 / 255.0     # the coverage at which a pixel is ink: the target's glyph maker draws a glyph and keeps the pixels over 100 of 255, so the reader's reference is that
                             # bold; at 0.5 the anti-aliased strokes were a tenth of a pixel thinner each side and some glyphs no longer told apart (the tenth build's check)


def aa_factor(ppm):
    return 4 if ppm <= 6 else 2


def paste_block_aa(sc, gl, glyphs, ppm, H, win):
    """The lettering's coverage, 0 to 1 (the second close review's finding 2: a bool mask at the item's scale stepped every edge by a whole pixel): every glyph drawn at s times the
    scale (s = 4 to 6 px/mm, else 2) and each s x s block averaged."""
    s = aa_factor(ppm)
    wx0, wx1, wy0, wy1 = win
    hh, ww = wy1 - wy0, wx1 - wx0
    hi = np.zeros((hh * s, ww * s), bool)
    for g in glyphs:
        if g["ch"] == " ":
            continue
        patch, ox, base = glyph_patch(sc, g, ppm * s)
        gl.paste_or(hi, patch, ox, base, g["ox_mm"] * ppm * s - wx0 * s, (H - g["baseline_mm"]) * ppm * s - wy0 * s)
    return hi.reshape(hh, s, ww, s).mean(axis=(1, 3)).astype(np.float32)


def block_window(item, b, shape, ppm):
    H = item["format"]["h_mm"]
    x0, y0, x1, y1 = b["ink_box_mm"]
    mx = 4.0 + (8.0 if b.get("hand") else 0.0)
    my = 3.0 + 0.3 * b["cap_mm"] + (6.0 if b.get("hand") else 0.0)
    return (int(max(0, (x0 - mx) * ppm)), int(min(shape[1], (x1 + mx) * ppm)), int(max(0, (H - y1 - my) * ppm)), int(min(shape[0], (H - y0 + my) * ppm)))


def look_of(item):
    return LOOK.get(item["process"], dict(sigma=0.12, film=0.0, rough=0.6))


def block_coverage(sc, covf, look, item, b, rng, ppm, mottle_field, win, mask_b=None):
    """(cov, dens, rim): the ink's coverage, its density and a rim-darkening, from the lettering's anti-aliased coverage in a window, by the item's process (the second close review: a
    blur of 0.35 px and no smoothstep, which hardened every edge back to a step)."""
    mask = covf >= INK_EDGE
    sig = max(0.55, min(0.62, look["sigma"] * ppm * 0.7))
    blur = ndi.gaussian_filter(covf.astype(np.float32), 0.35)
    bias = look.get("fat", 0.0)
    jitter = 0.0
    if look.get("rag"):
        n = pc.value_noise(mask.shape, max(1.0, 0.6 * ppm), rng)
        jitter = (n - 0.5) * min(0.6, look["rag"] * ppm * 0.35)
    x = np.clip(blur + bias + jitter, 0, 1)
    cov = np.where(x <= INK_EDGE, 0.5 * x / INK_EDGE, 0.5 + 0.5 * (x - INK_EDGE) / (1 - INK_EDGE)).astype(np.float32)    # bare paper 0, full ink 1, the reader's edge (INK_EDGE) at the middle
    if mask_b is not None:
        # which pixels are ink is the target's own bitmap at the item's scale (its glyph maker hints small type; the anti-aliased outline differs from it by fractions of a pixel,
        # enough that the reader could not tell some glyphs apart): the side is decided as before the second close review, and only the edge's shading is anti-aliased (ink pixels
        # full, paper pixels 0 to 0.3: the smoothing is on the paper side of the edge, where it costs the ink colour nothing)
        bb = ndi.gaussian_filter(mask_b.astype(np.float32), sig)
        side = smoothstep((bb - (0.5 - bias) + jitter) * 1.6 + 0.5) >= 0.5
        fringe = 0.3 if ppm <= 2.0 else 0.0              # the paper-side shading only on the 2 px/mm door cards, where the review saw the steps: elsewhere any fringe moved the reader's
        cov = np.where(side, 1.0, np.clip(cov, 0.0, fringe)).astype(np.float32)          # ink colour (W01-named's small italic v, dE 15 to 16); set aside there, named in NOTES
    dens = np.ones(mask.shape, np.float32)
    if look.get("density"):
        dens *= look["density"]
    if look.get("mottle") and mottle_field is not None:
        amt, _ = look["mottle"]
        dens -= (0.8 * amt * mottle_field[win[2]:win[3], win[0]:win[1]]).astype(np.float32)
    if look.get("grain"):
        dens -= look["grain"] * rng.random(mask.shape).astype(np.float32)
    if look.get("pressure"):
        n = pc.value_noise(mask.shape, max(2.0, 1.4 * ppm), rng, octaves=2)
        dens -= look["pressure"] * n
    rim = None
    edgesrc = (mask_b if mask_b is not None else covf).astype(np.float32)        # the letterpress rim and the felt pool from the reader's own ink pixels, as before
    if look.get("rim"):
        wide = ndi.gaussian_filter(edgesrc, max(1.0, 3 * sig))
        rim = np.clip(cov - wide, 0, 1) * look["rim"] * 4.0
    if look.get("pool"):
        wide = ndi.gaussian_filter(edgesrc, max(1.2, 0.5 * ppm))
        rim = np.clip(cov - wide, 0, 1) * look["pool"] * 4.0
    if look.get("pin"):
        per_cm2, (d0, d1) = look["pin"]
        area_cm2 = mask.size / (ppm * ppm) / 100.0
        n_pin = rng.poisson(per_cm2 * area_cm2)
        for _ in range(n_pin):
            yy, xx = rng.integers(0, mask.shape[0]), rng.integers(0, mask.shape[1])
            r = max(0.5, rng.uniform(d0, d1) * ppm / 2.0)
            y0, y1 = int(max(0, yy - r - 1)), int(min(mask.shape[0], yy + r + 2))
            x0, x1 = int(max(0, xx - r - 1)), int(min(mask.shape[1], xx + r + 2))
            gy, gx = np.mgrid[y0:y1, x0:x1]
            hole = ((gy - yy) ** 2 + (gx - xx) ** 2) <= r * r
            dens[y0:y1, x0:x1][hole] = 0.0
    return cov, np.clip(dens, 0.0, 1.0), rim


def typed_strike(sc, glyphs, ppm, H, win, rng, strike):
    """A typewriter's impression varies a little from one character to the next: a density per glyph, pasted into one map."""
    wx0, wx1, wy0, wy1 = win
    d = np.ones((wy1 - wy0, wx1 - wx0), np.float32)
    for g in glyphs:
        if g["ch"] == " ":
            continue
        patch, ox, base = glyph_patch(sc, g, ppm)
        px0 = int(round(g["ox_mm"] * ppm - wx0 - ox))
        py0 = int(round((H - g["baseline_mm"]) * ppm - wy0 - base))
        h, w = patch.shape
        sx0, sy0 = max(0, -px0), max(0, -py0)
        sx1, sy1 = min(w, d.shape[1] - px0), min(h, d.shape[0] - py0)
        if sx1 > sx0 and sy1 > sy0:
            v = float(rng.uniform(*strike))
            sub = d[py0 + sy0:py0 + sy1, px0 + sx0:px0 + sx1]
            sub[patch[sy0:sy1, sx0:sx1]] = v
    return d


def thin(mask):
    """Zhang-Suen thinning of a boolean mask to a one-pixel skeleton (numpy, no scikit-image here)."""
    s = np.pad(mask, 1).astype(np.uint8)
    while True:
        moved = False
        for step in (0, 1):
            P = [s[0:-2, 1:-1], s[0:-2, 2:], s[1:-1, 2:], s[2:, 2:], s[2:, 1:-1], s[2:, 0:-2], s[1:-1, 0:-2], s[0:-2, 0:-2]]       # p2 .. p9, clockwise from north
            B = sum(p.astype(np.int16) for p in P)
            A = sum(((P[i] == 0) & (P[(i + 1) % 8] == 1)).astype(np.int16) for i in range(8))
            c = s[1:-1, 1:-1] == 1
            if step == 0:
                c2 = (P[0] * P[2] * P[4] == 0) & (P[2] * P[4] * P[6] == 0)
            else:
                c2 = (P[0] * P[2] * P[6] == 0) & (P[0] * P[4] * P[6] == 0)
            kill = c & (B >= 2) & (B <= 6) & (A == 1) & c2
            if kill.any():
                s[1:-1, 1:-1][kill] = 0
                moved = True
        if not moved:
            break
    return s[1:-1, 1:-1].astype(bool)


def stroke_ends(mask):
    """(ys, xs) of the stroke ends: the skeleton's pixels with one neighbour."""
    sk = thin(mask)
    nb = ndi.convolve(sk.astype(np.int16), np.ones((3, 3), np.int16), mode="constant") - sk
    return np.nonzero(sk & (nb == 1))


def blot_ballpoint(mask, ppm, rng):
    """Ballpoint: a blot where the pen stopped, at one stroke end in ten (the second close review): an ellipse 0.5 to 0.8 mm long, 1.5 to 1, along the stroke, reaching 0.2 mm past its
    end. Returns its coverage (0 to 1); it is drawn at full density, against the stroke's 0.75 to 1.0."""
    sk = thin(mask)
    nb = ndi.convolve(sk.astype(np.int16), np.ones((3, 3), np.int16), mode="constant") - sk
    ys, xs = np.nonzero(sk & (nb == 1))
    out = np.zeros(mask.shape, np.float32)
    sy, sx = np.nonzero(sk)
    for i in range(len(ys)):
        if rng.random() >= 0.10:
            continue
        y, x = ys[i], xs[i]
        near = (np.abs(sy - y) <= 4) & (np.abs(sx - x) <= 4)
        v = np.array([x - sx[near].mean(), y - sy[near].mean()], float)
        nv = float(np.hypot(*v))
        v = v / nv if nv > 1e-6 else np.array([1.0, 0.0])
        L = rng.uniform(0.5, 0.8) * ppm
        a, b_ = L / 2, L / 3
        cx, cy = x + v[0] * (0.2 * ppm - a), y + v[1] * (0.2 * ppm - a)
        r = int(math.ceil(a)) + 2
        y0, y1 = max(0, int(cy) - r), min(mask.shape[0], int(cy) + r + 1)
        x0, x1 = max(0, int(cx) - r), min(mask.shape[1], int(cx) + r + 1)
        if y1 <= y0 or x1 <= x0:
            continue
        gy, gx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        u = ((gx - cx) * v[0] + (gy - cy) * v[1]) / a
        w = (-(gx - cx) * v[1] + (gy - cy) * v[0]) / b_
        out[y0:y1, x0:x1] = np.maximum(out[y0:y1, x0:x1], np.clip((1 - np.sqrt(u * u + w * w)) * max(a, 1.0), 0, 1))
    return out


# ------------------------------------------------------------------------------------------ the item
def build(sc, gl, P, item, seed, mottle_cache=None):
    """Lay out every shape and line of an item. Returns an ItemGeo (see the module's docstring)."""
    ppm = float(item["px_per_mm"])
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    w, h = int(round(W * ppm)), int(round(H * ppm))
    shp = (h, w)
    look = look_of(item)
    iid = item["id"]
    geo = ItemGeo()
    geo.item, geo.ppm, geo.shape, geo.look = item, ppm, shp, look
    rng_m = pc.rng_for(seed, iid, "mottle")
    mf = None
    if look.get("mottle"):
        mf = pc.value_noise(shp, look["mottle"][1] * ppm, rng_m, octaves=2)
    geo.mottle = mf
    # --- the card's own shape: alpha
    alpha = np.ones(shp, np.float32)
    star = [s for s in item["shapes"] if s["kind"] == "star"]
    face = [s for s in item["shapes"] if s["id"] == "face" and s.get("corner_radius_mm")]
    if star:
        pts = star[0]["pts_mm"]
        alpha = draw_cov((0, w, 0, h), lambda d, ss, ox, oy: d.polygon([(x * ppm * ss - ox * ss, (H - y) * ppm * ss - oy * ss) for x, y in pts], fill=255))
    elif item["kind"] == "sticker":
        r = 2.5 * ppm                       # a die-cut label: corners rounded 2.5 mm (Judgement; the target gives none)
        alpha = draw_cov((0, w, 0, h), lambda d, ss, ox, oy: d.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255))
    elif face:
        r = face[0]["corner_radius_mm"] * ppm
        alpha = draw_cov((0, w, 0, h), lambda d, ss, ox, oy: d.rounded_rectangle([0, 0, w * ss - 1, h * ss - 1], radius=r * ss, fill=255))
    geo.alpha = alpha
    elems = []
    second_off, geo.reg_tries = pick_reg_offset(sc, gl, item, seed, ppm, shp) if item["process"] in REG_PROCESSES else ((0.0, 0.0), 0)
    geo.second_off = second_off
    geo.holes = []
    # --- art slots: a stand-in (flat nominal colour; the picture itself is the image model's)
    geo.art = []
    for a in item["art"]:
        x0, y0, x1, y1 = px_box(a["box_mm"], ppm, H)
        win = window_around((x0, y0, x1, y1), shp, 0)
        geo.art.append(dict(id=a["id"], win=win, rgb=tuple(a["nominal_rgb"]), seed=a["seed"]))
    # --- shapes
    for s in item["shapes"]:
        kind = s["kind"]
        if kind == "star":
            continue
        if kind == "scrim":
            x0, y0, x1, y1 = px_box(s["box_mm"], ppm, H)
            win = window_around((x0, y0, x1, y1), shp, 0)
            ys = np.arange(win[2], win[3], dtype=np.float32)
            t = np.clip((ys - y0) / max(1.0, y1 - y0), 0, 1)
            a = (s["alpha_top"] + (s["alpha_bottom"] - s["alpha_top"]) * t)[:, None] * np.ones((1, win[1] - win[0]), np.float32)
            elems.append(Elem(s["id"], "scrim", win, a.astype(np.float32), ("rgb", tuple(s["rgb"]))))
            continue
        spec = shape_spec(item, s)
        if kind == "roundel" and spec == ("ink", "paper") and s["id"] == "hole":
            bx = px_box(s["box_mm"], ppm, H)
            win = window_around(bx, shp, 2)
            hole = draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(bx[0] - ox) * ss, (bx[1] - oy) * ss, (bx[2] - ox) * ss, (bx[3] - oy) * ss], fill=255))
            geo.holes.append((win, hole))
            continue
        second = item["process"] in REG_PROCESSES and spec[0] == "ink" and spec[1] in SECOND_PASS_INKS
        off = second_off if second else (0.0, 0.0)
        cov, win = shape_cov(s, ppm, H, shp, off)
        if cov is None:
            continue
        if kind == "rule":
            knock_out(item, cov, win, ppm, H)
        is_ink = spec[0] == "ink"
        dens = np.ones(cov.shape, np.float32)
        if is_ink and mf is not None and look.get("mottle"):
            dens -= (look["mottle"][0] * mf[win[2]:win[3], win[0]:win[1]]).astype(np.float32)
        raised = 0.0
        if item.get("relief") and s["id"] in ("border",):
            raised = item["relief"]["raised_mm"]
        elems.append(Elem(s["id"], "shape", win, cov, spec, dens=dens, film=(look.get("film", 0.0) if is_ink else 0.0), rough=look["rough"] if is_ink else None, second=second, raised=raised))
    # --- lettering
    geo.man = {}
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        rng = pc.rng_for(seed, iid, "block", b["id"])
        second = item["process"] in REG_PROCESSES and b["ink"] in SECOND_PASS_INKS
        off = second_off if second else (0.0, 0.0)
        glyphs = lay_block(sc, b, rng, off)
        geo.man[b["id"]] = glyphs
        win = block_window(item, b, shp, ppm)
        covf = paste_block_aa(sc, gl, glyphs, ppm, H, win)
        mask_b = paste_block(sc, gl, glyphs, ppm, H, win)
        blot = None
        if look.get("blots") and b.get("hand") == "ballpoint":
            blot = blot_ballpoint(mask_b, ppm, rng)
            covf = np.maximum(covf, blot)
            mask_b = mask_b | (blot > 0.5)
        cov, dens, rim = block_coverage(sc, covf, look, item, b, rng, ppm, mf, win, mask_b=mask_b)
        if blot is not None:
            dens = np.where(blot > 0.5, 1.0, dens).astype(np.float32)
        if look.get("strike"):
            dens = dens * typed_strike(sc, glyphs, ppm, H, win, rng, look["strike"])
        spec = ("ink", b["ink"])
        raised = item["relief"]["raised_mm"] if item.get("relief") else 0.0
        elems.append(Elem(b["id"], "block", win, cov, spec, dens=dens, rim=rim, film=look.get("film", 0.0), rough=look["rough"], second=second, cap=b["cap_mm"], hand=b.get("hand"),
                          tech=b.get("technique"), block=b, raised=raised))
    geo.elems = elems
    return geo


def knock_out(item, cov, win, ppm, H):
    """A rule that runs through a line of lettering is cut round it (2 mm clear), as a compositor would set it."""
    wx0, wx1, wy0, wy1 = win
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        x0, y0, x1, y1 = b["ink_box_mm"]
        px0, px1 = int((x0 - 2.0) * ppm) - wx0, int((x1 + 2.0) * ppm) - wx0
        py0, py1 = int((H - y1 - 2.0) * ppm) - wy0, int((H - y0 + 2.0) * ppm) - wy0
        if px1 <= 0 or py1 <= 0 or px0 >= cov.shape[1] or py0 >= cov.shape[0]:
            continue
        cov[max(0, py0):max(0, py1), max(0, px0):max(0, px1)] = 0.0


def shape_cov(s, ppm, H, shp, off):
    """Coverage of one shape (window, exact for boxes, supersampled for the rest), shifted by a registration offset (mm)."""
    kind = s["kind"]
    dx, dy = off[0] * ppm, -off[1] * ppm
    bx = s.get("box_mm")

    def X(x):
        return x * ppm + dx

    def Y(y):
        return (H - y) * ppm + dy
    if kind in ("rect", "rule", "frame", "roundel") and bx:
        x0, y0, x1, y1 = X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])
        win = window_around((x0, y0, x1, y1), shp, 2)
        if kind in ("rect", "rule"):
            return rect_cov((x0, y0, x1, y1), win), win
        if kind == "frame":
            t = s.get("width_mm", 3) * ppm
            return np.clip(rect_cov((x0, y0, x1, y1), win) - rect_cov((x0 + t, y0 + t, x1 - t, y1 - t), win), 0, 1), win
        return draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(x0 - ox) * ss, (y0 - oy) * ss, (x1 - ox) * ss, (y1 - oy) * ss], fill=255)), win
    if kind == "ring":
        cx, cy = s["centre_mm"]
        ro, ri = s["r_outer_mm"], s["r_inner_mm"]
        x0, y0, x1, y1 = X(cx - ro), Y(cy + ro), X(cx + ro), Y(cy - ro)
        win = window_around((x0, y0, x1, y1), shp, 2)

        def dr(d, ss, ox, oy):
            d.ellipse([(x0 - ox) * ss, (y0 - oy) * ss, (x1 - ox) * ss, (y1 - oy) * ss], fill=255)
            d.ellipse([(X(cx - ri) - ox) * ss, (Y(cy + ri) - oy) * ss, (X(cx + ri) - ox) * ss, (Y(cy - ri) - oy) * ss], fill=0)
        return draw_cov(win, dr), win
    if kind == "poly" and s.get("pts_mm"):
        pts = [(X(x), Y(y)) for x, y in s["pts_mm"]]
        xs, ys = [p[0] for p in pts], [p[1] for p in pts]
        win = window_around((min(xs), min(ys), max(xs), max(ys)), shp, 2)
        return draw_cov(win, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255)), win
    if kind == "ticks":
        segs = s["segments_mm"]
        wd = s.get("width_mm", 2) * ppm
        pts = [(X(g["p0"][0]), Y(g["p0"][1]), X(g["p1"][0]), Y(g["p1"][1])) for g in segs]
        xs = [p[0] for p in pts] + [p[2] for p in pts]
        ys = [p[1] for p in pts] + [p[3] for p in pts]
        win = window_around((min(xs), min(ys), max(xs), max(ys)), shp, wd + 2)

        def dr(d, ss, ox, oy):
            for a, b_, c, e in pts:
                d.line([((a - ox) * ss, (b_ - oy) * ss), ((c - ox) * ss, (e - oy) * ss)], fill=255, width=max(1, int(round(wd * ss))))
        return draw_cov(win, dr), win
    if kind == "hand":
        cx, cy = s["centre_mm"]
        L, wd = s["length_mm"], s["width_mm"]
        ang = s.get("angle_deg")
        if ang is None:
            ang = 60.0 if s.get("pointing") == "by variant" else 0.0      # K02's default variant: the hour hand at two o'clock (the other variant is the target's 'hands at 12')
        a = math.radians(ang)       # clockwise from 12 o'clock
        ex, ey = cx + L * math.sin(a), cy + L * math.cos(a)
        x0, y0, x1, y1 = X(min(cx, ex) - wd), Y(max(cy, ey) + wd), X(max(cx, ex) + wd), Y(min(cy, ey) - wd)
        win = window_around((x0, y0, x1, y1), shp, 2)

        def dr(d, ss, ox, oy):
            d.line([((X(cx) - ox) * ss, (Y(cy) - oy) * ss), ((X(ex) - ox) * ss, (Y(ey) - oy) * ss)], fill=255, width=max(1, int(round(wd * ppm * ss))))
            r = wd * ppm * ss / 2
            for px, py in ((X(cx), Y(cy)), (X(ex), Y(ey))):
                d.ellipse([(px - ox) * ss - r, (py - oy) * ss - r, (px - ox) * ss + r, (py - oy) * ss + r], fill=255)
        return draw_cov(win, dr), win
    return None, None
