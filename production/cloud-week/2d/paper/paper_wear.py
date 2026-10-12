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
LIME = (235, 235, 228)            # the close review's finding 10
STRING = (150, 150, 146)          # the string and its knot (the close review's finding 8): the target's cream (236, 232, 220) does not show on a white card
GROUND_COAT = (190, 190, 185)     # the grey ground coat of vitreous enamel, round a chip (finding 11)


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
def paper_relief(S, table):
    """The relief of a sheet (the close review's finding 12; it replaces a cockle of noise over the whole sheet, which a raking light would show as crumpled): a pasted bill has 4 to 10
    vertical wrinkles (more with age; 50 to 300 mm long, 3 to 8 mm wide, 0.4 to 1.5 mm high) and 2 to 4 paste bubbles (20 to 60 mm across); a sheet behind glass or in a sleeve at most two
    wrinkles; every sheet a ripple of at most 0.15 mm (a sticker 0.05)."""
    rng = S.rng
    ci = S.ci
    n = pc.value_noise((S.h, S.w), rng.uniform(15, 40) * S.ppm, rng, octaves=2)
    amp = 0.05 if table == "sticker" else 0.15 * (0.6 + 0.4 * ci / 3.0)
    S.height += ((n - 0.5) * 2.0 * amp).astype(np.float32)
    if table == "bill_pasted":
        n_w = int(np.clip(round(4 + 2 * ci + rng.uniform(-1, 1)), 4, 10))
        n_b = int(rng.integers(2, 5))
    elif table == "sticker":
        n_w, n_b = 0, 0
    else:
        n_w, n_b = int(rng.integers(0, 3)), 0
    hmax = 0.4 + 1.1 * (0.25 + 0.75 * ci / 3.0)
    for _ in range(n_w):
        L = min(rng.uniform(50, 300), 0.95 * S.H) * S.ppm
        y0 = rng.uniform(0, max(1.0, S.h - L))
        x0 = rng.uniform(0.04, 0.96) * S.w
        sig = rng.uniform(3, 8) * S.ppm / 2.355
        a = float(rng.uniform(0.4, hmax))
        tilt = math.tan(math.radians(rng.normal(0, 3)))
        wan, wl, wp = rng.uniform(0.5, 2.0) * S.ppm, rng.uniform(60, 200) * S.ppm, rng.uniform(0, 2 * math.pi)
        win = S.win_of((x0 - 4 * sig - abs(tilt) * L - wan, y0, x0 + 4 * sig + abs(tilt) * L + wan, y0 + L))
        wx0, wx1, wy0, wy1 = win
        if wx1 <= wx0 or wy1 <= wy0:
            continue
        ys = np.arange(wy0, wy1, dtype=np.float32) + 0.5
        tt = np.clip((ys - y0) / L, 0, 1)
        xc = x0 + tilt * (ys - y0) + wan * np.sin(2 * math.pi * (ys - y0) / wl + wp)
        xs = np.arange(wx0, wx1, dtype=np.float32) + 0.5
        prof = np.exp(-0.5 * ((xs[None, :] - xc[:, None]) / sig) ** 2)
        along = np.clip(np.sin(math.pi * tt), 0, 1) ** 0.5
        S.height[wy0:wy1, wx0:wx1] += (a * prof * along[:, None]).astype(np.float32)
    for _ in range(n_b):
        D = rng.uniform(20, 60) * S.ppm
        x, y = rng.uniform(0.1, 0.9) * S.w, rng.uniform(0.1, 0.9) * S.h
        a = float(rng.uniform(0.3, 0.6 + 0.4 * ci / 3.0))
        e, ang = rng.uniform(0.7, 1.0), rng.uniform(0, math.pi)
        win = S.win_of((x - D, y - D, x + D, y + D))
        wx0, wx1, wy0, wy1 = win
        gy, gx = np.mgrid[wy0:wy1, wx0:wx1].astype(np.float32)
        u = ((gx - x) * math.cos(ang) + (gy - y) * math.sin(ang)) / (D / 2)
        v = (-(gx - x) * math.sin(ang) + (gy - y) * math.cos(ang)) / (D / 2 * e)
        rr = u * u + v * v
        S.height[wy0:wy1, wx0:wx1] += (a * np.clip(1 - rr, 0, 1) ** 2).astype(np.float32)
    S.log["relief"] = dict(wrinkles=n_w, bubbles=n_b)


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


# ------------------------------------------------------------------------------------------ the loss of paper: tear lines (the second street review's finding 1, its exact fix)
def gl_disk(r):
    y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return (x * x + y * y) <= r * r


def _dir(a):
    return np.array([math.cos(a), math.sin(a)])


def jag(rng, pts, levels=3, amp=0.06, cap=None):
    """Midpoint displacement, `levels` deep, each midpoint moved across its segment by amp x the segment's length (a normal draw), at most `cap` mm when given."""
    P = [np.asarray(p, float) for p in pts]
    for _ in range(levels):
        Q = [P[0]]
        for a, b in zip(P[:-1], P[1:]):
            d = b - a
            L = float(np.hypot(*d))
            n = np.array([-d[1], d[0]]) / max(L, 1e-9)
            o = rng.normal(0, amp * L)
            if cap is not None:
                o = float(np.clip(o, -cap, cap))
            Q += [(a + b) / 2 + n * o, b]
        P = Q
    return P


def tear_walk(rng, G, n_seg, cap=110.0):
    """An open tear line (mm, y down) along the guide polyline G (from G[0], on the sheet's edge, to G[-1], on the edge): n_seg segments of 12 to 70 mm, each turned 15 to 75 degrees off
    the guide's heading with the sign alternating at every vertex, two neighbouring turns together at most `cap` degrees; where the guide bends, a vertex sits on the bend with its own turn
    against the bend; one vertex in four a tooth (a jog of 5 to 25 mm out at 90 to 140 degrees, then back to the heading). Built along the guide (s) and across it (y), then laid on it."""
    G = [np.asarray(g, float) for g in G]
    seg = np.array([np.hypot(*(q - p)) for p, q in zip(G[:-1], G[1:])])
    cum = np.concatenate([[0.0], np.cumsum(seg)])
    Lg = float(cum[-1])
    bends = list(cum[1:-1])
    # the stations along the guide: the bends, then the rest spread by random weights
    k_free = max(n_seg - 1 - len(bends), 0)
    w = rng.uniform(0.6, 1.4, k_free + len(bends) + 1)
    st = np.cumsum(w / w.sum() * Lg)[:-1]
    st = np.sort(np.concatenate([st[:k_free], bends])) if bends else st
    for b in bends:                                      # make sure each bend is a station (replace the nearest)
        j = int(np.argmin(np.abs(st - b)))
        st[j] = b
    st = np.unique(np.round(st, 3))

    def frame(s):
        i = int(np.clip(np.searchsorted(cum, s, side="right") - 1, 0, len(seg) - 1))
        tgt = (G[i + 1] - G[i]) / max(seg[i], 1e-9)
        return G[i] + tgt * (s - cum[i]), tgt, np.array([-tgt[1], tgt[0]])

    def bend_turn(s):
        for bi, b in enumerate(bends):
            if abs(s - b) < 1e-6:
                t0 = (G[bi + 1] - G[bi]) / seg[bi]
                t1 = (G[bi + 2] - G[bi + 1]) / seg[bi + 1]
                return math.degrees(math.atan2(t0[0] * t1[1] - t0[1] * t1[0], float(np.dot(t0, t1))))
        return 0.0
    sign = 1 if rng.random() < 0.5 else -1
    prev_t = 0.0
    y = 0.0
    s_prev = 0.0
    pts = [G[0]]
    for k, s in enumerate(list(st) + [Lg]):
        ds = s - s_prev
        last = s >= Lg - 1e-6
        if last:
            dy = -y
        else:
            bt = bend_turn(s)
            if bt:                                       # the vertex on a bend turns against it
                sign = -1 if bt > 0 else 1
            t_c = float(rng.uniform(15.0, max(15.0, min(75.0, cap - prev_t - abs(bt) * 0.5))))
            dy = sign * ds * math.tan(math.radians(t_c))
            prev_t = t_c
        y += dy
        p, tg, nm = frame(min(s, Lg))
        q = p + nm * y
        pts.append(q)
        if not last and (k + 1) % 4 == 0:               # a tooth: a jog out and back to the heading
            hd = math.atan2(dy, ds)
            th = math.radians(rng.uniform(90, 140)) * (-sign)
            d1, d2 = rng.uniform(5, 25), rng.uniform(12, 30)
            ox, oy = math.cos(hd + th) * d1, math.sin(hd + th) * d1
            tip = q + tg * ox + nm * oy
            back = tip + tg * math.cos(hd) * d2 + nm * math.sin(hd) * d2
            pts += [tip, back]
            y += oy + math.sin(hd) * d2
            s = s + ox + math.cos(hd) * d2
        sign = -sign
        s_prev = s
    return pts


def patch_poly(rng, kind, c, a, b, n_seg):
    """The loss region of one torn patch: kind 'corner' (c a corner; a along the foot or top, b up or down the side: a torn corner, its tear running across it) or 'edge' (c on an edge;
    a along it each way, b into the sheet: the tear leaves the edge and meets it again at 30 to 70 degrees). Returns (polygon, tear line)."""
    c = np.asarray(c, float)
    if kind[0] == "corner":
        u, v = np.asarray(kind[1], float), np.asarray(kind[2], float)
        tear = tear_walk(rng, [c + a * u, c + b * v], n_seg)
        return [c] + tear, tear
    e, n = np.asarray(kind[1], float), np.asarray(kind[2], float)
    P0, P1 = c + a * e, c - a * e
    a0, a1 = math.radians(rng.uniform(40, 70)), math.radians(rng.uniform(40, 70))
    d0 = math.cos(a0) * (-e) + math.sin(a0) * n
    d1 = math.cos(a1) * e + math.sin(a1) * n
    s = np.linalg.solve(np.stack([d0, -d1], 1), P1 - P0)
    M = P0 + s[0] * d0
    depth = float(np.dot(M - P0, n))
    if depth > b:                                        # a flat top at depth b
        Q1 = P0 + d0 * (b / math.sin(a0))
        Q2 = P1 + d1 * (b / math.sin(a1))
        G = [P0, Q1, Q2, P1]
    else:
        G = [P0, M, P1]
    tear = tear_walk(rng, G, n_seg)
    return tear, tear


def bite_poly(rng, c, e, n, R):
    """An edge bite: 2 to 4 segments leaving and meeting the edge at 30 to 70 degrees."""
    c, e, n = np.asarray(c, float), np.asarray(e, float), np.asarray(n, float)
    P0, P1 = c - R * e, c + R * e
    a0, a1 = math.radians(rng.uniform(30, 70)), math.radians(rng.uniform(30, 70))
    d0 = math.cos(a0) * e + math.sin(a0) * n
    d1 = -math.cos(a1) * e + math.sin(a1) * n
    k = int(rng.integers(2, 5))
    if k == 2:                                           # the apex where the two rays meet
        M = np.stack([d0, -d1], 1)
        s = np.linalg.solve(M, P1 - P0)
        pts = [P0, P0 + s[0] * d0, P1]
    else:
        depth = R * rng.uniform(0.5, 1.0)
        Q1 = P0 + d0 * depth / max(0.3, math.sin(a0)) * rng.uniform(0.6, 1.0)
        Q2 = P1 + d1 * depth / max(0.3, math.sin(a1)) * rng.uniform(0.6, 1.0)
        pts = [P0, Q1]
        if k == 4:
            m = (Q1 + Q2) / 2
            dd = Q2 - Q1
            pts.append(m + np.array([-dd[1], dd[0]]) * rng.uniform(0.2, 0.4) * (1 if rng.random() < 0.5 else -1))
        pts += [Q2, P1]
    return pts, pts


def poly_mask(polys, shape, cpm):
    im = Image.new("L", (shape[1], shape[0]), 0)
    d = ImageDraw.Draw(im)
    for P in polys:
        d.polygon([(float(x) * cpm, float(y) * cpm) for x, y in P], fill=255)
    return np.asarray(im) > 127


def cut_protrusions(m, cpm, sizes_mm=(4, 8, 16, 32), rng=None):
    """Cut off every tongue of loss or of paper longer than 1.5 times its base width (it replaces the 20 mm disc openings, which rounded every corner). The second close review: the cut
    is a straight torn chord, not the opening's disc arc: of the tongue's pixels touching the body, A and B the two farthest apart; only the tongue's pixels beyond the line AB (jagged 3
    levels deep at 6 per cent, like a tear) change side. The mask is padded by its own edge, so that the sheet's border is neither paper nor loss. Returns (mask, tongues cut)."""
    rng = rng or np.random.default_rng(0)
    cut = 0
    p = int(max(sizes_mm) * cpm) + 2
    for D in sizes_mm:
        r = max(1, int(round(D * cpm / 2)))
        for inv in (False, True):
            a = np.pad(~m if inv else m, p, mode="edge")
            body = ndi.binary_opening(a, gl_disk(r))
            lab, k = ndi.label(a & ~body)
            for i, sl in enumerate(ndi.find_objects(lab) if k else [], 1):
                if math.hypot(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) / cpm <= 1.5 * D:
                    continue
                y0, y1 = max(0, sl[0].start - 3), min(a.shape[0], sl[0].stop + 3)
                x0, x1 = max(0, sl[1].start - 3), min(a.shape[1], sl[1].stop + 3)
                T = lab[y0:y1, x0:x1] == i
                B_ = body[y0:y1, x0:x1]
                touch = T & ndi.binary_dilation(B_, np.ones((3, 3), bool))
                ty, tx = np.nonzero(touch)
                cut += 1
                if len(ty) < 2:
                    a[y0:y1, x0:x1][T] = False
                    continue
                P = np.stack([tx, ty], 1).astype(np.float64)
                if len(P) > 300:
                    P = P[np.linspace(0, len(P) - 1, 300).astype(int)]
                d2 = ((P[:, None, :] - P[None, :, :]) ** 2).sum(-1)
                ia, ib = np.unravel_index(int(np.argmax(d2)), d2.shape)
                A, Bp = P[ia], P[ib]
                AB = Bp - A
                L = float(np.hypot(*AB))
                if L < 1.0:
                    a[y0:y1, x0:x1][T] = False
                    continue
                prof = np.array(jag(rng, [(0.0, 0.0), (L, 0.0)]))
                order = np.argsort(prof[:, 0])
                by, bx = np.nonzero(B_ & ~T)
                cb = np.array([bx.mean(), by.mean()]) if len(by) else A + np.array([-AB[1], AB[0]])
                side_b = np.sign(AB[0] * (cb[1] - A[1]) - AB[1] * (cb[0] - A[0])) or 1.0
                yy, xx = np.nonzero(T)
                tt = ((xx - A[0]) * AB[0] + (yy - A[1]) * AB[1]) / L
                off = np.interp(tt, prof[order, 0], prof[order, 1])
                side = (AB[0] * (yy - A[1]) - AB[1] * (xx - A[0])) / L - off * side_b
                far = np.sign(side) != side_b
                sub = a[y0:y1, x0:x1]
                sub[yy[far], xx[far]] = False
            a = a[p:-p, p:-p]
            m = ~a if inv else a
    return m, cut


def protrusions_left(m, cpm, sizes_mm=(4, 8, 16, 32)):
    n = 0
    p = int(max(sizes_mm) * cpm) + 2
    for D in sizes_mm:
        r = max(1, int(round(D * cpm / 2)))
        for inv in (False, True):
            a = np.pad(~m if inv else m, p, mode="edge")
            lab, k = ndi.label(a & ~ndi.binary_opening(a, gl_disk(r)))
            for sl in ndi.find_objects(lab):
                if math.hypot(sl[0].stop - sl[0].start, sl[1].stop - sl[1].start) / cpm > 1.5 * D:
                    n += 1
    return n


def trace_outline(comp):
    """The ordered outer boundary (x, y pixel centres) of one component (Moore-neighbour tracing)."""
    a = np.pad(comp, 1)
    ys, xs = np.nonzero(a)
    k0 = int(np.lexsort((xs, ys))[0])
    start = (int(ys[k0]), int(xs[k0]))
    nb = [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
    pts = [start]
    cur, back = start, 6                                 # entered from the west
    for _step in range(4 * a.size):
        found = False
        for kk in range(8):
            dd = (back + 1 + kk) % 8
            ny, nx = cur[0] + nb[dd][0], cur[1] + nb[dd][1]
            if a[ny, nx]:
                back = (dd + 4) % 8
                cur = (ny, nx)
                found = True
                break
        if not found or (cur == start and len(pts) > 2):
            break
        pts.append(cur)
    return [(x - 1, y - 1) for y, x in pts]


def outline_runs(lost, cpm):
    """The tear runs of the final loss: each component's outline, cut where it lies on the sheet's border, in mm, simplified at 0.5 mm."""
    from shapely.geometry import LineString
    h, w = lost.shape
    lab, n = ndi.label(lost)
    runs = []
    for i in range(1, n + 1):
        comp = lab == i
        if comp.sum() < 4:
            continue
        P = trace_outline(comp)
        on = [x <= 1 or y <= 1 or x >= w - 2 or y >= h - 2 for x, y in P]
        cur = []
        for (x, y), o in zip(P + P[:1], on + on[:1]):
            if o:
                if len(cur) >= 10:
                    runs.append(cur)
                cur = []
            else:
                cur.append((x / cpm, y / cpm))
        if len(cur) >= 10:
            runs.append(cur)
    out = []
    for r_ in runs:
        ls = LineString(r_)
        s = ls.simplify(0.5)
        out.append((list(s.coords), r_))
    return out


def staircase(T):
    """Two consecutive segments each within 10 degrees of an axis, meeting at 80 to 100 degrees (the second close review's narrow point 8)."""
    Q = np.asarray(T, float)
    h = np.degrees(np.arctan2(*np.diff(Q, axis=0).T[::-1]))
    ax = np.minimum(np.abs(((h + 45) % 90) - 45), 90)
    for k in range(len(h) - 1):
        turn = abs(((h[k + 1] - h[k]) + 180) % 360 - 180)
        if ax[k] <= 10 and ax[k + 1] <= 10 and 80 <= turn <= 100:
            return True
    return False


def tear_tests(lines):
    """The review's tests on the tear lines: (stretches of 40 mm turning more than 150 degrees one way after 3 mm smoothing, tear lines of 60 mm or more with fewer than two vertices turning
    60 degrees or more)."""
    t150 = few = 0
    for raw, jagged in lines:
        P = np.asarray(jagged, float)
        seg = np.hypot(*np.diff(P, axis=0).T)
        s = np.concatenate([[0.0], np.cumsum(seg)])
        if s[-1] < 10:
            continue
        u = np.arange(0.0, s[-1], 1.0)
        R = np.stack([np.interp(u, s, P[:, 0]), np.interp(u, s, P[:, 1])], 1)
        R = ndi.gaussian_filter1d(R, 3.0, axis=0, mode="nearest")
        h = np.unwrap(np.arctan2(*np.diff(R, axis=0).T[::-1]))
        dh = np.diff(h)
        if len(dh) > 40:
            cs = np.concatenate([[0.0], np.cumsum(dh)])
            win = np.abs(cs[40:] - cs[:-40])
            t150 += int(np.degrees(win.max()) > 150)
        Q = np.asarray(raw, float)
        if np.hypot(*np.diff(Q, axis=0).T).sum() >= 60 and len(Q) >= 3:
            hh = np.arctan2(*np.diff(Q, axis=0).T[::-1])
            tv = np.degrees(np.abs((np.diff(hh) + math.pi) % (2 * math.pi) - math.pi))
            few += int((tv >= 60).sum() < 2)
    return t150, few


def loss_and_tears(S, share_range, n_tears):
    """The loss of paper (the second street review's exact fix): each loss is the region between the sheet's edge and one tear line, an open polyline of 4 to 12 segments of 12 to 70 mm
    turned 15 to 75 degrees off its base heading with the sign alternating, one vertex in four a tooth; then a midpoint-displacement jag 3 levels deep at 6 per cent of a segment, the
    fibre fringe and the pale rim. Edge bites are the same walk with 2 to 4 segments, leaving and meeting the edge at 30 to 70 degrees. No disc openings: a tongue of loss or of paper
    longer than 1.5 times its base is cut off at its base. The shares, the corners and the ghost are as before: class B keeps to the lower corners (a corner of at most 120 mm, half the foot
    untouched); C and D also the foot's middle and, in D, an upper side and the top; in A and B the lettering's reading window and 4 mm round it are never touched (a patch shrinks as a whole)."""
    rng = S.rng
    lo, hi = share_range
    share = float(rng.uniform(lo, hi)) if hi > 0 else 0.0
    if share <= 0.001 and n_tears <= 0:
        return
    W_, H_ = S.W, S.H
    Hc, Wc = int(math.ceil(H_)), int(math.ceil(W_))
    prot = protect_coarse(S) if S.cls in ("A", "B") else None
    if prot is not None:
        prot = ndi.binary_dilation(prot, gl_disk(4))
    R0 = math.sqrt(max(share, 0.001) * W_ * H_ / 2.0 * 4.0 / math.pi) if share > 0.001 else 0.0
    specs = []                     # (kind, centre, weight, child seed)
    if share > 0.001:
        left = rng.random() < 0.5
        corners = [(0.0, H_), (W_, H_)] if S.cls != "B" or rng.random() < 0.5 else [((0.0, H_) if left else (W_, H_))]
        for cx, cy in corners:
            specs.append((("corner", (1.0 if cx == 0 else -1.0, 0.0), (0.0, -1.0)), (cx, cy), float(rng.uniform(0.8, 1.2)), int(rng.integers(1 << 30))))
        if S.cls in ("C", "D"):
            specs.append((("edge", (1.0, 0.0), (0.0, -1.0)), (float(rng.uniform(0.25, 0.75)) * W_, H_), float(rng.uniform(0.6, 1.0)), int(rng.integers(1 << 30))))
        if S.cls == "D":
            sx = float(rng.choice([0.0, W_]))
            specs.append((("edge", (0.0, 1.0), (1.0 if sx == 0 else -1.0, 0.0)), (sx, float(rng.uniform(0.15, 0.5)) * H_), float(rng.uniform(0.5, 0.9)), int(rng.integers(1 << 30))))
            specs.append((("edge", (1.0, 0.0), (0.0, 1.0)), (float(rng.uniform(0.15, 0.85)) * W_, 0.0), float(rng.uniform(0.3, 0.7)), int(rng.integers(1 << 30))))
    R0 = R0 * (2.0 / max(len(specs), 1)) ** 0.5 if specs else 0.0
    bites = []
    for _ in range(n_tears):
        e = int(rng.integers(0, 4))
        t_ = float(rng.uniform(0.1, 0.9))
        geo = [((t_ * W_, 0.0), (1, 0), (0, 1)), ((W_, t_ * H_), (0, 1), (-1, 0)), ((t_ * W_, H_), (1, 0), (0, -1)), ((0.0, t_ * H_), (0, 1), (1, 0))][e]
        bites.append((geo, float(rng.uniform(14, 35)), int(rng.integers(1 << 30))))

    def patch(kind, c, R, cs):
        """(polygon, (tear line, jagged tear line)): the first of up to 24 draws whose line passes the review's own tests (no 40 mm turning 150 degrees one way; two sharp vertices)."""
        for k in range(24):
            r2 = np.random.default_rng(cs + 7919 * k)
            a, b = R * r2.uniform(0.8, 1.25), R * r2.uniform(0.8, 1.25)
            arc = (math.pi / 4 if kind[0] == "corner" else math.pi / 2) * (a + b)
            n_seg = int(np.clip(round(arc / r2.uniform(25, 45)), 4, 12))
            P, T = patch_poly(r2, kind, c, a, b, n_seg)
            Tj = jag(r2, T)
            if tear_tests([(T, Tj)]) == (0, 0) and not staircase(T):
                break
        return ([P[0]] + Tj if kind[0] == "corner" else Tj), (T, Tj)

    def bite(c, e, n, Rb, cs):
        for k in range(24):
            r2 = np.random.default_rng(cs + 7919 * k)
            P, T = bite_poly(r2, c, e, n, Rb)
            Tj = jag(r2, T)
            if tear_tests([(T, Tj)]) == (0, 0):
                break
        return Tj, (T, Tj)

    def clear(P):
        if prot is None:
            return True
        return not (poly_mask([P], (Hc, Wc), 1.0) & prot).any()

    def build(f, salt=0):
        polys, lines = [], []
        for kind, c, wgt, cs in specs:
            R = R0 * f * wgt
            for _s in range(16):
                P, L = patch(kind, c, R, cs + salt)
                if clear(P):
                    polys.append(P)
                    lines.append(L)
                    break
                R *= 0.85
        for (c, e, n), Rb, cs in bites:
            for _s in range(8):
                P, L = bite(c, e, n, Rb, cs + salt)
                if clear(P):
                    polys.append(P)
                    lines.append(L)
                    break
                Rb *= 0.8
        return polys, lines
    def size_for(salt):
        f = 1.0
        if specs:
            lo_f, hi_f = 0.1, 3.0
            for _ in range(12):
                f = (lo_f + hi_f) / 2
                got = float(poly_mask(build(f, salt)[0], (Hc, Wc), 1.0).mean())
                if got > share:
                    hi_f = f
                else:
                    lo_f = f
            f = lo_f
        return f
    cpm = 2.0
    shp2 = (int(math.ceil(H_ * cpm)), int(math.ceil(W_ * cpm)))
    for attempt in range(8):                             # a loss whose cutting leaves a tongue (a cut on one side making one on the other) is drawn again from the next seed
        f = size_for(attempt * 104729)
        polys, lines = build(f, attempt * 104729)
        if not polys:
            return
        lost, cut = poly_mask(polys, shp2, cpm), 0
        crng = np.random.default_rng(int(attempt * 7 + 11))
        for _p in range(6):                              # cutting a tongue can leave a shorter one: until none is left
            lost, c_ = cut_protrusions(lost, cpm, rng=crng)
            cut += c_
            if not c_:
                break
        left_ = protrusions_left(lost, cpm)
        t150, few = tear_tests(outline_runs(lost, cpm))   # the review's tests on the final outline, not on the drawn lines
        if not left_ and not t150 and not few:
            break
    S.log["tear_tests"] = dict(turn_over_150=t150, few_sharp_vertices=few, tongues_left=left_, tongues_cut=cut)
    if not lost.any():
        return
    soft = ndi.gaussian_filter(lost.astype(np.float32), 0.6)
    up = np.asarray(Image.fromarray((soft * 255).astype(np.uint8)).resize((S.w, S.h), Image.BILINEAR)).astype(np.float32) / 255.0
    fib = pc.value_noise((S.h, S.w), max(1.0, 0.8 * S.ppm), rng, octaves=2)
    lost_b = up + (fib - 0.5) * 0.30 > 0.5
    lab, n_ = ndi.label(lost_b)                          # specks of loss under 1 mm2 are dropped before the rim (the second close review: a 0.04 mm2 speck drew a square rim)
    if n_:
        sizes = ndi.sum(lost_b, lab, range(1, n_ + 1))
        lost_b &= np.isin(lab, np.nonzero(sizes >= S.ppm * S.ppm)[0] + 1)
    lost_f = pc.smooth(lost_b.astype(np.float32), 0.6)
    wr = np.maximum(1.0, (0.4 + 0.8 * pc.value_noise((S.h, S.w), 6 * S.ppm, rng)) * S.ppm)          # the pale rim: round, 0.4 to 1.2 mm wide, varying
    dist = ndi.distance_transform_edt(~lost_b)
    edge = np.clip(wr - dist + 0.5, 0, 1) * (~lost_b)
    fibre = 0.6 + 0.4 * pc.value_noise((S.h, S.w), 1.5 * S.ppm, rng)
    S.tint((0, S.w, 0, S.h), (edge * (1 - lost_f) * fibre).astype(np.float32), (244, 241, 231), 0.8)
    if S.cls in ("C", "D"):
        ghost = np.asarray((214, 205, 185), np.float32)
        S.rgb[:] = S.rgb * (1 - lost_f[..., None]) + ghost * lost_f[..., None]
        S.alpha *= (1 - 0.7 * lost_f)
    else:
        S.alpha *= (1 - lost_f)
    S.height[:] = (S.height * (1 - lost_f) - 0.1 * lost_f).astype(np.float32)          # where the paper is gone the wall lies the paper's thickness below the face
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


def tape_tab(S, centre_mm, flip_x=False, flip_y=False, spec=None):
    """A tab of tape; where it passes the edge of a shaped card (the star cards) it is the tape alone, at alpha 0.49 (the close review's finding 9: the target's tab passes the card's edge;
    0.49 keeps it under the reader's 0.5, so that it is not read as card)."""
    spec = spec or S.P.T["fixings"]["tape_tab"]
    pts = pc.tape_polygon(centre_mm, S.ppm, S.H, spec, flip_x, flip_y)
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    win = S.win_of((min(xs), min(ys), max(xs), max(ys)), 3)
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255), ss=4)
    tape_filter(S, win, cov, spec)
    wx0, wx1, wy0, wy1 = win
    a_card = S.alpha[wy0:wy1, wx0:wx1]
    a_tab = 0.49 * cov * (1 - a_card)
    if a_tab.max() > 0.02:
        a_new = a_card + a_tab
        sub = S.rgb[wy0:wy1, wx0:wx1]
        mix = (sub * a_card[..., None] + np.asarray(spec["rgb"], np.float32) * a_tab[..., None]) / np.maximum(a_new, 1e-6)[..., None]
        sub[:] = np.where((a_new > 1e-6)[..., None], mix, sub)
        a_card[:] = a_new
    return win, cov


def tabs(S):
    """Every tab of tape the item carries in its class (paper_common.tab_layout: one home for the maker and the reader)."""
    lay = pc.tab_layout(S.P.T, S.item, S.cls)
    for c, fxx, fyy, spec in lay:
        tape_tab(S, c, fxx, fyy, spec)
    if lay:
        S.log["tabs"] = len(lay)


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
    # the string, 1.0 mm, straight up from the knot to the card's top edge, and the 8 mm knot over the sucker's upper half (the close review's finding 8), in STRING
    kr = fx["knot_mm"] / 2 * S.ppm
    kx, ky = px, py - 0.45 * r
    wid = 1.0 * S.ppm
    sw = S.win_of((kx - wid - 2, 0, kx + wid + 2, ky + 1))
    sc_ = pi.rect_cov((kx - wid / 2, 0, kx + wid / 2, ky), sw)
    S.tint(sw, sc_, STRING, 0.95)
    S.height[sw[2]:sw[3], sw[0]:sw[1]] += (sc_ * 0.5).astype(np.float32)
    kwin, kc = S.blob(kx, ky, kr, 0.22)
    S.tint(kwin, kc, STRING, 1.0)
    gy, gx = np.mgrid[kwin[2]:kwin[3], kwin[0]:kwin[1]].astype(np.float32)
    S.tint(kwin, kc * np.clip(((gx - kx) + (gy - ky)) / (2 * kr), 0, 1), (96, 96, 92), 0.35)        # the knot's shaded lower right
    kin = ndi.distance_transform_edt(np.pad(kc > 0.5, 1))[1:-1, 1:-1]
    S.tint(kwin, ((kin > 0) & (kin <= max(1.0, 0.4 * S.ppm))).astype(np.float32) * kc, (88, 88, 84), 0.6)       # its edge, so that it shows on the sucker
    S.height[kwin[2]:kwin[3], kwin[0]:kwin[1]] += (kc * 1.5).astype(np.float32)
    S.log["string_cue"] = True


# ------------------------------------------------------------------------------------------ plates and boards
def bolt_head(S, x_mm, y_mm, d_mm=18, hole_mm=10, rust=True):
    px, py = x_mm * S.ppm, (S.H - y_mm) * S.ppm
    r = d_mm / 2 * S.ppm
    win = S.win_of((px - r - 6 * S.ppm, py - r - 6 * S.ppm, px + r + 6 * S.ppm, py + r + 6 * S.ppm))
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(px - r - ox) * ss, (py - r - oy) * ss, (px + r - ox) * ss, (py + r - oy) * ss], fill=255))
    gy, gx = np.mgrid[win[2]:win[3], win[0]:win[1]].astype(np.float32)
    rr = np.hypot(gx - px, gy - py) / r
    if rust:                # a ring of rust 2 to 4 mm wide at 0.5, three times as strong below the head as above it (the close review's finding 10)
        wr = float(S.rng.uniform(2, 4)) * S.ppm
        dd = (rr - 1) * r
        ring = np.clip(1 - (np.maximum(dd, 0) / wr) ** 2, 0, 1) * (rr >= 0.95)
        below = np.clip(0.5 + 0.5 * (gy - py) / np.maximum(rr * r, 1.0), 0, 1)
        wgt = 1 / 3.0 + (2 / 3.0) * below
        n = 0.65 + 0.35 * pc.value_noise(rr.shape, 1.2 * S.ppm, S.rng)
        S.tint(win, (ring * wgt * n).astype(np.float32), RUST, 0.5)
    shade = (0.82 + 0.35 * np.clip(1 - rr, 0, 1) ** 0.7 - 0.05 * (gx - px) / r)[..., None]
    sub = S.rgb[win[2]:win[3], win[0]:win[1]]
    sub[:] = sub * (1 - cov[..., None]) + np.asarray((118, 116, 112), np.float32) * shade * cov[..., None]
    S.height[win[2]:win[3], win[0]:win[1]] += (cov * 2.0 * np.clip(1 - rr, 0, 1) ** 0.5).astype(np.float32)
    S.rough[win[2]:win[3], win[0]:win[1]] = S.rough[win[2]:win[3], win[0]:win[1]] * (1 - cov) + 0.45 * cov


def chips(S, n, size_mm, near=None, edge_bias=0.7, colour=STEEL, halo_mm=(1, 3), halo_op=0.35, fade=1.0, spots=None):
    """Chips in the enamel (the close reviews): rounded and scalloped (three to six overlapping discs), dark steel; all the chips are gathered into one shape and ringed once by 0.5 to
    1 mm of the grey ground coat (190, 190, 185), so that rings never cross a chip; in classes C and D the steel is rusty and a thin rust stain lies round them, stronger below. The bolt
    heads are drawn after the chips (enamel_plate, pressed_plate), so that no chip lies on a head."""
    rng = S.rng
    rusty = S.cls in ("C", "D")
    steel = np.asarray(colour, np.float32) * 0.55 + np.asarray(RUST, np.float32) * 0.45 if rusty else np.asarray(colour, np.float32)
    allc = np.zeros((S.h, S.w), np.float32)
    done = 0
    for i in range(n):
        r = float(rng.uniform(size_mm[0], size_mm[1])) / 2 * S.ppm
        if spots and rng.random() < 0.55:
            sx, sy = spots[int(rng.integers(0, len(spots)))]
            x, y = sx * S.ppm + rng.normal(0, 7 * S.ppm), (S.H - sy) * S.ppm + rng.normal(0, 7 * S.ppm)
        elif rng.random() < edge_bias:
            e = int(rng.integers(0, 4))
            t_ = rng.uniform(0, 1)
            m_ = rng.uniform(1, 9) * S.ppm
            x, y = ((t_ * S.w, m_) if e == 0 else ((S.w - m_, t_ * S.h) if e == 1 else ((t_ * S.w, S.h - m_) if e == 2 else (m_, t_ * S.h))))
        else:
            x, y = rng.uniform(0, S.w), rng.uniform(0, S.h)
        x, y = float(np.clip(x, 0, S.w - 1)), float(np.clip(y, 0, S.h - 1))
        if S.cls in ("A", "B") and S.hits_text((x - 1.6 * r, y - 1.6 * r, x + 1.6 * r, y + 1.6 * r), 1.5):
            continue
        pad = 1.6 * r + 3
        win = S.win_of((x - pad, y - pad, x + pad, y + pad))
        wx0, wx1, wy0, wy1 = win
        if wx1 <= wx0 or wy1 <= wy0:
            continue
        discs = []
        for _k in range(int(rng.integers(3, 7))):
            a, dd = rng.uniform(0, 2 * math.pi), rng.uniform(0, 0.55) * r
            discs.append((x + dd * math.cos(a), y + dd * math.sin(a), r * rng.uniform(0.45, 0.8)))

        def draw(d, ss, ox, oy, discs=discs):
            for cx, cy, rr_ in discs:
                d.ellipse([(cx - rr_ - ox) * ss, (cy - rr_ - oy) * ss, (cx + rr_ - ox) * ss, (cy + rr_ - oy) * ss], fill=255)
        cc = pi.draw_cov(win, draw)
        allc[wy0:wy1, wx0:wx1] = np.maximum(allc[wy0:wy1, wx0:wx1], cc)
        done += 1
    S.log["chips"] = done
    if not done:
        return
    inside = allc > 0.5
    d_out = ndi.distance_transform_edt(~inside)
    ring_px = (0.5 + 0.5 * pc.value_noise((S.h, S.w), 3 * S.ppm, rng)) * S.ppm
    ring = (np.clip(1 - (d_out - ring_px) / 1.0, 0, 1) * (1 - allc)).astype(np.float32)
    if rusty:
        hm = float(rng.uniform(*halo_mm)) * S.ppm
        low = ndi.shift(inside.astype(np.float32), (0.5 * hm, 0), order=0) > 0.5          # the stain hangs below
        d_low = ndi.distance_transform_edt(~(inside | low))
        halo = np.clip(1 - (d_low - ring_px) / max(hm, 1.0), 0, 1) * (d_out > ring_px)
        S.tint((0, S.w, 0, S.h), (halo * (0.6 + 0.4 * pc.value_noise((S.h, S.w), 1.5 * S.ppm, rng))).astype(np.float32), RUST, halo_op * fade)
    S.tint((0, S.w, 0, S.h), ring, GROUND_COAT, 0.95)
    S.tint((0, S.w, 0, S.h), allc, steel, 0.95)
    S.height -= (allc * 0.12 + ring * 0.05).astype(np.float32)
    S.rough[:] = S.rough * (1 - allc) + 0.7 * allc


def rust_run(S, x, y0, L, op0=0.35, op1=0.05):
    """A rust run from a screw (the close review's finding 10): 4 to 6 mm wide at the screw tapering to 1 mm, wandering up to 2 mm sideways, its opacity falling from 0.35 to 0.05."""
    rng = S.rng
    w0, w1 = float(rng.uniform(4, 6)) * S.ppm, 1.0 * S.ppm
    pad = w0 + 2.5 * S.ppm
    win = S.win_of((x - pad, y0, x + pad, y0 + L))
    wx0, wx1, wy0, wy1 = win
    if wx1 <= wx0 or wy1 <= wy0 or L < 2:
        return
    ys = np.arange(wy0, wy1, dtype=np.float32) + 0.5
    tt = np.clip((ys - y0) / L, 0, 1)
    k = max(4, int(L / (8 * S.ppm)))
    walk = np.cumsum(rng.normal(0, 1, k + 1))
    walk -= walk[0]
    walk *= 2.0 * S.ppm * float(rng.uniform(0.5, 1.0)) / max(1e-6, float(np.abs(walk).max()))
    xc = x + ndi.gaussian_filter1d(np.interp(tt, np.linspace(0, 1, k + 1), walk), max(1.0, 2 * S.ppm))
    wid = w0 + (w1 - w0) * tt ** 0.7
    xs = np.arange(wx0, wx1, dtype=np.float32) + 0.5
    edge = np.clip((wid[:, None] / 2 - np.abs(xs[None, :] - xc[:, None])) / (0.4 * S.ppm), 0, 1)
    prof = edge * edge * (3 - 2 * edge)
    op = op0 * (op1 / op0) ** tt
    streak = 0.8 + 0.2 * pc.value_noise((wy1 - wy0, wx1 - wx0), 3 * S.ppm, rng, aniso=4.0)
    S.tint(win, (prof * op[:, None] * streak).astype(np.float32), RUST, 1.0)


def lime_streak(S, width_mm=None, length_mm=None, colour=LIME, opacity=0.9, top=True):
    """Bird lime (the second street review's exact fix): an irregular splat 8 to 20 mm across on the top edge, (235, 235, 228) at 0.9 with a core of (150, 150, 135) over 20 to 40 per
    cent of it; from it 1 to 3 runs, each 2 to 5 mm wide (its width within 30 per cent along it, no taper from a wide top), 20 to 90 mm long, within 3 degrees of vertical, at 0.85 to
    0.95, ending in a bead of 3 to 5 mm. No lime is wider than 8 mm more than 10 mm below the top edge. (width_mm and length_mm are kept for the callers; the review's numbers rule.)"""
    rng = S.rng
    x0 = rng.uniform(0.1, 0.9) * S.w
    y0 = 0.0 if top else S.h * 0.3
    D = rng.uniform(8, 20) * S.ppm
    lobes = int(rng.integers(5, 10))                   # a lobed splat (the second close review)
    th = np.linspace(0, 2 * math.pi, 72, endpoint=False)
    rr = D / 2 * (1 + 0.22 * np.cos(lobes * th + rng.uniform(0, 2 * math.pi)) + 0.08 * np.cos(2 * th + rng.uniform(0, 2 * math.pi)))
    spl = [(x0 + r_ * math.cos(a_), y0 + D * 0.25 + r_ * math.sin(a_)) for r_, a_ in zip(rr, th)]
    sw = S.win_of((x0 - D, y0 + D * 0.25 - D, x0 + D, y0 + D * 1.25), 2)
    sc_ = pi.draw_cov(sw, lambda d, ss, ox, oy: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in spl], fill=255))
    S.tint(sw, sc_, colour, opacity)
    core = sc_ * (pc.value_noise(sc_.shape, max(1.0, 0.25 * D), rng) > rng.uniform(0.6, 0.8))
    S.tint(sw, core.astype(np.float32), (150, 150, 135), 0.9)
    S.height[sw[2]:sw[3], sw[0]:sw[1]] += (sc_ * 0.3).astype(np.float32)
    S.rough[sw[2]:sw[3], sw[0]:sw[1]] = S.rough[sw[2]:sw[3], sw[0]:sw[1]] * (1 - sc_) + 0.8 * sc_
    for _ in range(int(rng.integers(1, 4))):
        wr = rng.uniform(2, 5) * S.ppm
        L = rng.uniform(20, 90) * S.ppm
        ang = math.radians(rng.uniform(-3, 3))
        sx = x0 + rng.uniform(-0.3, 0.3) * D
        sy = y0 + D * 0.4
        m = 32
        tt = np.linspace(0, 1, m)
        Lmm = L / S.ppm
        wv = 2 * np.clip((0.8 + 1.7 * np.interp(tt * Lmm, np.arange(0, Lmm + 5, 5.0), rng.random(int(Lmm / 5) + 2))) * S.ppm, 0.8 * S.ppm, 2.5 * S.ppm)   # half-width 0.8 to 2.5 mm by noise at 5 mm
        wander = 0.6 * S.ppm * np.interp(tt * Lmm, np.arange(0, Lmm + 15, 15.0), rng.uniform(-1, 1, int(Lmm / 15) + 2))                                  # the line wanders +-0.6 mm over 15 mm
        cx = sx + np.sin(ang) * L * tt + wander * np.cos(ang)
        cy = sy + np.cos(ang) * L * tt
        left = [(cx[k] - wv[k] / 2, cy[k]) for k in range(m)]
        right = [(cx[k] + wv[k] / 2, cy[k]) for k in range(m - 1, -1, -1)]
        pts = left + right
        br = rng.uniform(3, 5) / 2 * S.ppm
        bx, by = cx[-1], cy[-1]
        xs, ys = [p[0] for p in pts] + [bx - br, bx + br], [p[1] for p in pts] + [by - br, by + br]
        win = S.win_of((min(xs), min(ys), max(xs), max(ys)), 3)
        if win[1] <= win[0] or win[3] <= win[2]:
            continue

        def draw(d, ss, ox, oy, pts=pts, bx=bx, by=by, br=br):
            d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in pts], fill=255)
            d.ellipse([(bx - br - ox) * ss, (by - br - oy) * ss, (bx + br - ox) * ss, (by + br - oy) * ss], fill=255)
        cov = pi.draw_cov(win, draw)
        S.tint(win, cov, colour, float(rng.uniform(0.85, 0.95)))
        S.height[win[2]:win[3], win[0]:win[1]] += (cov * 0.2).astype(np.float32)
        S.rough[win[2]:win[3], win[0]:win[1]] = S.rough[win[2]:win[3], win[0]:win[1]] * (1 - cov) + 0.8 * cov
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
def apply(S, table, cls):
    it = S.item
    table = pc.WEAR_OVERRIDE.get((it["id"], cls), table)
    if it["process"] == "plastic_print":
        table = "plastic_card"
    rng = S.rng
    ci = S.ci
    R = S.P.T["age_rules"]["paper_wear"]
    fx = S.P.T["fixings"]
    process = it["process"]
    mc = it.get("mirror_cue")
    fixk = (it.get("fixing") or {}).get("kind", "")
    if table in ("bill_pasted", "glass_bill", "glass_two_tabs", "notice_sleeve", "sticker"):
        if ci > 0 or table != "sticker":
            paper_relief(S, table)
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
        S.rough[:] = S.rough * 0.85
    elif table == "glass_two_tabs":
        curl_out(S, 2, 5)              # hung by its top corners inside the glass: the foot curls out a little; no beads, ties or fog
        S.rough[:] = S.rough * 0.85
    elif table == "notice_sleeve":
        sleeve(S)
    elif table == "plastic_card":
        # a printed plastic card on a chain: no folds, no curl, no bleaching, no finger smudge; scratches (none in class A; the second street review), a little grime (at most 5 per cent)
        # and the sheen of the plastic
        if ci:
            card_scratches(S, int(rng.integers(6, 13)) + 4 * (ci - 1))
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
    tabs(S)                            # the tape lies over the print and the copier's marks
    if (mc and mc["kind"] != "tape") or (not mc and fixk == "string"):
        string_cue(S)


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
        water_bead(S, rng.uniform(0.05, 0.95) * S.w, rng.uniform(0.66, 0.97) * S.h, rng.uniform(1.0, 3.0) * S.ppm)
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


def water_bead(S, x, y, r):
    """A bead of water on polythene, 2 to 6 mm, as a lens (the close review's finding 7: not an outlined ring): the paper under it enlarged 1.08 times, a darker crescent (-12 per cent)
    on its lower 0.3 R, a highlight of radius 0.2 R (+35 per cent) at its upper left, no outline."""
    win = S.win_of((x - r - 2, y - r - 2, x + r + 2, y + r + 2))
    wx0, wx1, wy0, wy1 = win
    if wx1 <= wx0 or wy1 <= wy0:
        return
    cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.ellipse([(x - r - ox) * ss, (y - r - oy) * ss, (x + r - ox) * ss, (y + r - oy) * ss], fill=255))
    gy, gx = np.mgrid[wy0:wy1, wx0:wx1].astype(np.float32) + 0.5
    sx, sy = x + (gx - x) / 1.08 - 0.5, y + (gy - y) / 1.08 - 0.5
    mag = np.stack([ndi.map_coordinates(S.rgb[..., k], [sy, sx], order=1, mode="nearest") for k in range(3)], -1)
    sub = S.rgb[wy0:wy1, wx0:wx1]
    sub[:] = sub * (1 - cov[..., None]) + mag * cov[..., None]
    up = np.hypot(gx - x, gy - (y - 0.3 * r))                                  # the crescent: inside the bead, outside the same disc lifted 0.3 R
    cres = cov * np.clip(up - r + 0.5, 0, 1)
    sub *= (1 - 0.12 * cres)[..., None]
    hl = cov * np.clip(0.2 * r - np.hypot(gx - (x - 0.4 * r), gy - (y - 0.4 * r)) + 0.5, 0, 1)
    sub[:] = np.minimum(255.0, sub * (1 + 0.35 * hl)[..., None])
    rr = np.hypot(gx - x, gy - y) / r
    S.height[wy0:wy1, wx0:wx1] += (cov * 0.4 * np.sqrt(np.clip(1 - rr * rr, 0, 1))).astype(np.float32)


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


def card_scratches(S, n):
    """The plastic sign's scratches (the second street review): opacity 0.25 to 0.4; 70 per cent within 25 mm of the bottom edge or 20 mm of the hole and within 25 degrees of
    horizontal; in classes A and B they keep off the lettering."""
    rng = S.rng
    holes = []
    for win, hole in S.geo.holes:
        ys, xs = np.nonzero(hole > 0.5)
        if len(ys):
            holes.append((win[0] + xs.mean(), win[2] + ys.mean()))
    for _ in range(n):
        for _t in range(25):
            near = rng.random() < 0.7
            if near and holes and rng.random() < 0.4:
                hx, hy = holes[int(rng.integers(len(holes)))]
                r = rng.uniform(0, 20) * S.ppm
                a0 = rng.uniform(0, 2 * math.pi)
                x, y = hx + r * math.cos(a0), hy + r * math.sin(a0)
            elif near:
                x, y = rng.uniform(0.05, 0.95) * S.w, S.h - rng.uniform(1, 25) * S.ppm
            else:
                x, y = rng.uniform(0.05, 0.95) * S.w, rng.uniform(0.05, 0.95) * S.h
            a = math.radians(rng.uniform(-25, 25)) if near else rng.uniform(0, math.pi)
            L = rng.uniform(5, 40) * S.ppm
            x, y = float(np.clip(x, 0, S.w - 1)), float(np.clip(y, 0, S.h - 1))
            x2, y2 = float(np.clip(x + L * math.cos(a), 0, S.w - 1)), float(np.clip(y + L * math.sin(a), 0, S.h - 1))
            if S.cls not in ("A", "B") or not S.hits_text((min(x, x2), min(y, y2), max(x, x2), max(y, y2)), 1.0):
                break
        else:
            continue
        wd = rng.uniform(0.2, 0.5)
        win = S.win_of((min(x, x2), min(y, y2), max(x, x2), max(y, y2)), 3)
        if win[1] <= win[0] or win[3] <= win[2]:
            continue
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.line([((x - ox) * ss, (y - oy) * ss), ((x2 - ox) * ss, (y2 - oy) * ss)], fill=255, width=max(1, int(wd * S.ppm * ss))))
        S.tint(win, cov, (240, 238, 230), float(rng.uniform(0.25, 0.4)))
    S.log["scratches"] = n


def scratches(S, n, width_mm=(0.3, 0.5), length_mm=(10, 40)):
    """Light scratches; in classes A and B they keep off the lettering (a scratch across white-on-black lettering reads as a stroke of ink: P06 in the sixth build's check)."""
    rng = S.rng
    for _ in range(n):
        for _t in range(25):
            x, y = rng.uniform(0.1, 0.9) * S.w, rng.uniform(0.1, 0.9) * S.h
            L = rng.uniform(*length_mm) * S.ppm
            a = rng.uniform(0, math.pi)
            wd = rng.uniform(*width_mm)
            x2, y2 = x + L * math.cos(a), y + L * math.sin(a)
            if S.cls not in ("A", "B") or not S.hits_text((min(x, x2), min(y, y2), max(x, x2), max(y, y2)), 1.0):
                break
        else:
            continue
        win = S.win_of((min(x, x2), min(y, y2), max(x, x2), max(y, y2)), 3)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy: d.line([((x - ox) * ss, (y - oy) * ss), ((x2 - ox) * ss, (y2 - oy) * ss)], fill=255, width=max(1, int(wd * S.ppm * ss))))
        S.tint(win, cov, (240, 238, 230), 0.55)


def enamel_plate(S, it):
    """H01, H02: vitreous enamel on steel: chips to black steel with a rust halo (at the corners, edges and bolts first), crazing near the bolts, rust tears, bird lime, salt bloom (H02)."""
    W = S.P.T["wear_tables"]["enamel_plate"]
    rng = S.rng
    holes = it["fixing"]["holes_mm"]
    k = {"A": 0.0, "B": 0.45, "C": 0.75, "D": 1.0}[S.cls]
    chips(S, int(round(rng.integers(12, 31) * k)), (2, 9), edge_bias=0.65, spots=holes, fade=k)
    for hx, hy in holes:                               # the heads after the chips: no chip lies on a head (the second close review)
        if S.cls != "A":
            crazing(S, hx, hy, 3)
        bolt_head(S, hx, hy, 18, 10, rust=S.cls in ("C", "D"))
    if S.cls in ("C", "D"):
        for hx, hy in [h for h in holes if h[1] > S.H / 2]:          # under the top bolts (y is from the bottom)
            rust_run(S, hx * S.ppm, (S.H - hy) * S.ppm + 6 * S.ppm, rng.uniform(150, 400) * S.ppm * (0.6 + 0.4 * k))
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


def edge_flakes(S, rm, share):
    """The paint of the raised letters and border lifting at their edges first (the close review's finding 6; the first answer, angular flakes spread over every face, read as
    terrazzo): runs of 3 to 8 angular flakes, 6 to 25 mm long, along the raised edges, each flake 1.6 to 4 mm across and set 0.2 to 0.8 mm in from the edge, until `share` of the raised
    area is bare; the share within 2 mm of an edge is logged (at least 0.8)."""
    rng = S.rng
    on = rm > 0.5
    if not on.any():
        return np.zeros((S.h, S.w), np.float32)
    din = ndi.distance_transform_edt(np.pad(on, 1))[1:-1, 1:-1]
    gy_, gx_ = np.gradient(ndi.gaussian_filter(din.astype(np.float32), 1.0))
    eys, exs = np.nonzero(on & (din <= 1.0))
    # the runs start only inside 3 to 6 clusters, each 40 to 120 mm along the plate (the second close review: an even fringe on every edge read as a distressed font)
    keep = np.zeros(len(exs), bool)
    for _c in range(int(rng.integers(3, 7))):
        x0c = rng.uniform(0, S.W) * S.ppm
        keep |= (exs >= x0c) & (exs <= x0c + rng.uniform(40, 120) * S.ppm)
    starts = np.nonzero(keep)[0] if keep.any() else np.arange(len(exs))
    pts = np.stack([exs, eys], 1).astype(np.float32)
    ss = 3
    im = Image.new("L", (S.w * ss, S.h * ss), 0)
    d = ImageDraw.Draw(im)
    target = share * float(on.sum())
    est, runs, flakes = 0.0, 0, 0
    while est < target and runs < 4000:
        runs += 1
        i0 = int(starts[int(rng.integers(len(starts)))])
        c0 = pts[i0]
        L = rng.uniform(6, 25) * S.ppm
        n = int(rng.integers(3, 9))
        near = np.abs(pts - c0).max(1) <= L
        loc = pts[near]
        tan_ = loc[np.hypot(*(loc - c0).T) <= 3 * S.ppm]
        if len(tan_) < 4:
            continue
        w_, v_ = np.linalg.eigh(np.cov((tan_ - tan_.mean(0)).T))
        tdir = v_[:, -1]
        for k in range(n):
            q = c0 + tdir * (k - (n - 1) / 2.0) * L / max(1, n - 1)
            dq = np.hypot(*(loc - q).T)
            j = int(np.argmin(dq))
            if dq[j] > 2 * S.ppm:
                continue
            ex, ey = loc[j]
            nx, ny = gx_[int(ey), int(ex)], gy_[int(ey), int(ex)]
            nn = math.hypot(nx, ny) or 1.0
            sh = rng.uniform(0.2, 0.8) * S.ppm
            cx, cy = ex + 0.5 + nx / nn * sh, ey + 0.5 + ny / nn * sh
            r = rng.uniform(1.25, 2.5) * S.ppm                  # flakes 2.5 to 5 mm
            m = int(rng.integers(5, 8))
            ang = np.sort(rng.uniform(0, 2 * math.pi, m))
            rad = r * rng.uniform(0.5, 1.0, m)
            d.polygon([((cx + rr * math.cos(a)) * ss, (cy + rr * math.sin(a)) * ss) for rr, a in zip(rad, ang)], fill=255)
            est += 0.5 * m * float(np.mean(rad)) ** 2 * math.sin(2 * math.pi / m) * 0.6
            flakes += 1
    a_ = np.asarray(im.resize((S.w, S.h), Image.BOX)).astype(np.float32) / 255.0 * on
    tot = float(a_.sum())
    S.log["flake_runs"] = runs
    S.log["flakes"] = flakes
    S.log["flake_share_of_raised"] = tot / max(1.0, float(on.sum()))
    S.log["flake_within_2mm"] = float((a_ * (din <= 2.0 * S.ppm)).sum()) / max(1e-6, tot)
    return a_


def chalky_ground(S, rm, share=0.01):
    """Chalky patches on the painted ground between the raised letters (the close review's finding 6): 1 per cent of the ground, matt and a shade duller."""
    ground = (rm < 0.5) & (S.alpha > 0.5)
    if not ground.any():
        return
    n = pc.value_noise((S.h, S.w), 25 * S.ppm, S.rng, octaves=3)
    thr = float(np.quantile(n[ground], 1 - share))
    ch = (pc.smooth((n >= thr).astype(np.float32), 1.0 * S.ppm) * ground).astype(np.float32)
    S.tint((0, S.w, 0, S.h), ch, (222, 220, 212), 0.5)
    S.rough[:] = S.rough * (1 - ch) + 0.9 * ch
    S.log["chalky_share"] = float((ch > 0.5).sum()) / float(ground.sum())


def cast_plate(S, it):
    """S01 n and d: cast aluminium, letters and border raised 3 mm, painted: the paint lifts first at the raised edges (a darker rim of lifted paint round each flake), chalky patches on the
    ground, a grime gradient, rust from the screws, bird lime on the top border."""
    rng = S.rng
    rm = raised_mask(S)
    k = {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls]
    share = float(rng.uniform(0.03, 0.06)) * k
    if share > 0 and rm.sum() > 0:
        flake = edge_flakes(S, rm, share)
        rim = np.clip(ndi.grey_dilation(flake, footprint=gl_disk(max(1, int(round(0.4 * S.ppm))))) - flake, 0, 1) * (rm > 0.5)
        S.rgb *= (1 - 0.2 * rim)[..., None]                    # a 0.4 mm rim of lifted paint at 0.8 of its value
        S.tint((0, S.w, 0, S.h), flake, ALUM, 0.95)
        S.metal = np.maximum(S.metal, flake)
        S.rough[:] = S.rough * (1 - flake * 0.5) + 0.35 * flake * 0.5
        S.height -= (flake * 0.15).astype(np.float32)
        S.log["flake_share"] = float((flake > 0.5).mean())
    if k > 0:                                          # the ground lightened 3 per cent at the top, nothing at the foot, a little rougher (it replaces the chalky blobs)
        ground = ((rm < 0.5) & (S.alpha > 0.5)).astype(np.float32)
        ys_ = np.arange(S.h, dtype=np.float32) / max(1, S.h - 1)
        S.rgb *= (1 + 0.03 * (1 - ys_)[:, None] * ground)[..., None]
        S.rough[:] = np.minimum(1.0, S.rough + 0.1 * ground)
    grime_gradient(S, 0.12 * k)
    if S.cls in ("C", "D"):
        holes = it["fixing"]["holes_mm"]
        run = [h for h in holes if rng.random() < 0.6] or [holes[int(rng.integers(len(holes)))]]
        for hx, hy in holes:
            bolt_head(S, hx, hy, 14, 10, rust=True)
        for hx, hy in run:
            L = (rng.uniform(40, 120) if hy > S.H / 2 else rng.uniform(15, 40)) * S.ppm
            rust_run(S, hx * S.ppm, (S.H - hy) * S.ppm + 5 * S.ppm, L)
        for _ in range(int(rng.integers(1, 3))):
            lime_streak(S, width_mm=(12, 30), length_mm=(22, 50))
    S.shade(0.05)


def pressed_plate(S, it):
    """S02 and S03: stove enamel on aluminium or vitreous enamel on steel: chips at the corners and screws only (4 to 12 of 2 to 6 mm), a grime gradient, no flaking of the letters."""
    rng = S.rng
    k = {"A": 0.0, "B": 0.4, "C": 0.7, "D": 1.0}[S.cls]
    holes = it["fixing"]["holes_mm"]
    corners = [(6, 6), (S.W - 6, 6), (6, S.H - 6), (S.W - 6, S.H - 6)]
    chips(S, int(round(rng.integers(4, 13) * max(k, 0.3))), (2, 6), edge_bias=0.0, spots=corners + holes, fade=k, halo_mm=(1, 4), halo_op=0.35)
    for hx, hy in holes:
        bolt_head(S, hx, hy, 14, 10, rust=S.cls == "D")
    grime_gradient(S, 0.10 * k)
    S.shade(0.04)


def peel_bites(S, n, length_mm=(20, 80), depth_mm=(3, 15), colour=(150, 145, 135)):
    """Separate bites of the paint peeled from the foot of a board: grey plywood showing; each bite's top edge a ragged tear line (the walk of the loss of paper at a quarter of its scale) and a
    0.5 mm rim of lifted paint (the paint's colour times 1.08) along it (the second street review)."""
    rng = S.rng
    for _ in range(n):
        L = rng.uniform(*length_mm)
        D = rng.uniform(*depth_mm)
        cx = rng.uniform(0.08, 0.92) * S.W
        a, b = L / 2, D
        r2 = np.random.default_rng(int(rng.integers(1 << 30)))
        guide = lambda t, cx=cx, a=a, b=b: np.array([cx + a * math.cos(t * math.pi), S.H - b * math.sin(t * math.pi)])
        pts = [np.array([cx + a, S.H])]
        p = pts[0]
        sign = 1 if r2.random() < 0.5 else -1
        nseg = int(r2.integers(4, 9))
        for k in range(1, nseg):
            aim = guide(k / nseg)
            base = math.atan2(aim[1] - p[1], aim[0] - p[0])
            tr = math.radians(r2.uniform(15, 75)) * sign
            sign = -sign
            Ls = float(np.clip(np.hypot(*(aim - p)) / max(0.3, math.cos(tr)), 3.0, 17.5))
            p = p + Ls * _dir(base + tr)
            p[1] = min(p[1], S.H)
            pts.append(p)
        pts.append(np.array([cx - a, S.H]))
        pts = jag(r2, pts, cap=1.0)
        poly = [(x * S.ppm, y * S.ppm) for x, y in pts] + [((cx - a) * S.ppm, S.h + 2), ((cx + a) * S.ppm, S.h + 2)]
        xs, ys = [q[0] for q in poly], [q[1] for q in poly]
        win = S.win_of((min(xs), min(ys), max(xs), max(ys)), int(2 * S.ppm) + 3)
        cov = pi.draw_cov(win, lambda d, ss, ox, oy, poly=poly: d.polygon([((x - ox) * ss, (y - oy) * ss) for x, y in poly], fill=255))
        mb, _c = cut_protrusions(cov > 0.5, S.ppm, sizes_mm=(2, 4, 8), rng=r2)          # no needles (the second close review)
        cov = np.minimum(cov, pc.smooth(mb.astype(np.float32), 0.5))
        S.log["bite_tongues_left"] = S.log.get("bite_tongues_left", 0) + protrusions_left(cov > 0.5, S.ppm, sizes_mm=(2, 4, 8))
        rim = np.clip(ndi.grey_dilation(cov, footprint=gl_disk(max(1, int(round(0.5 * S.ppm))))) - cov, 0, 1)
        sub = S.rgb[win[2]:win[3], win[0]:win[1]]
        sub[:] = sub * (1 - rim[..., None]) + np.minimum(255.0, sub * 1.08) * rim[..., None]
        S.height[win[2]:win[3], win[0]:win[1]] += (rim * 0.05).astype(np.float32)
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
    screws = [(x, y) for x in sx for y in sy]
    run = [s for s in screws if rng.random() < 0.6] or [screws[int(rng.integers(len(screws)))]]
    for x, y in run:
        L = (rng.uniform(40, 140) if y > S.H / 2 else rng.uniform(15, 38)) * S.ppm
        rust_run(S, x * S.ppm, (S.H - y) * S.ppm + 5 * S.ppm, L)
    peel_bites(S, int(rng.integers(2, 5)))
    ys, xs = np.mgrid[0:S.h, 0:S.w].astype(np.float32)
    if S.cls == "D":
        n = pc.value_noise((S.h, S.w), 5 * S.ppm, rng, octaves=2)
        g = np.clip(1 - (S.h - 1 - ys) / (20 * S.ppm), 0, 1) * (0.5 + 0.5 * n)
        S.tint((0, S.w, 0, S.h), g.astype(np.float32), (62, 78, 52), 0.3)
    grime_gradient(S, 0.05 * k, bottom=True)
    S.shade(0.05)
