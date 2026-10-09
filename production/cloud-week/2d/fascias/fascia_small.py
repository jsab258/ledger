"""The small things (unit 4.1): the four hanging signs' faces, the three gilt balls, the glass lettering rows, the empty unit's whitewashed
window, the letting board and the hours plates. Every one is a texture set at one pixel a millimetre, drawn from target.json (amended).

JUDGEMENTS made here (each is repeated in NOTES.md):
  - three hanging-sign faces are narrower than the target's lettering asks (LAUNDERETTE 644 mm on a 620 mm face, KEYS CUT 739 mm on a
    550 mm board, CHANDLERY 997 mm on an 800 mm board): the target's board sizes, mounts and lowest points are kept and the CAP is reduced
    until the word fits inside its border with a margin; the built cap is written next to the target's in the manifest;
  - z_m of a glass row is the height of the letters' BASELINE above the pavement (shop-room.py sets its glass lettering by its baseline) and
    x_street_m is the centre of the ink;
  - glass-lettering tiles are RGBA, drawn as seen from the street (they read left to right from the pavement).
"""
import json
import math
import re

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage as ndi

import fascia_age as fa
import fascia_brush as fb
import fascia_common as fc
import fascia_paint as fp
import fascia_wear as fw
from fascia_boards import lab_shift, rope_alpha_and_pattern


def figure_ratio(T, font_key, weight, text):
    """height of a string of figures over its font size (their own height, which is not always the capital's: Josefin Sans' figures stand at 0.9 of its H)"""
    f = fc.font_for(T, font_key, weight, 1000)
    bb = f.getbbox(text, anchor="ls")
    return -bb[1] / 1000.0


def make_block(T, text, font_key, weight, cap_mm, tracking_em, baseline_mm, x_mm, anchor, face, shade_d=None, shade_colour="shade_black",
               technique="painted", hand=False, W=None, H=None, bid="b", role="name", face_rgb=None, figure=False, squeeze=1.0):
    """a block dict like the target's, for text that is not on a fascia board: the layout numbers are computed the way make_target.py does.
    squeeze < 1 draws a CONDENSED face (the font squeezed to that share of its width, its stems grown back toward their weight)."""
    cr = fc.cap_ratio(T, font_key, weight)
    if figure:
        cr = figure_ratio(T, font_key, weight, text)
    px = cap_mm / cr
    f = fc.font_for(T, font_key, weight, px)
    trk = tracking_em * px
    xs = fc.glyph_origins(f, text, trk)
    # ink extent from the pixels of a clean render
    pad = int(px) + 12
    if squeeze == 1.0:
        Wd = int(xs[-1] + f.getlength(text[-1]) + 2 * pad)
        Hd = int(px * 1.8) + 2 * pad
        base = pad + int(px * 1.25)
        img = Image.new("L", (Wd, Hd), 0)
        d = ImageDraw.Draw(img)
        for i, ch in enumerate(text):
            if ch != " ":
                d.text((pad + xs[i], base), ch, font=f, fill=255, anchor="ls")
        a = np.asarray(img) > 100
    else:
        Wd = int((xs[-1] + f.getlength(text[-1])) + 2 * pad)
        Hd = int(px * 1.8) + 2 * pad
        base = pad + int(px * 1.25)
        b0 = dict(text=text, font=font_key, weight=weight, cap_mm=cap_mm, tracking_em=tracking_em, cap_ratio=cr, jitter=None, origin_x_mm=float(pad),
                  baseline_mm=Hd - 1 - base, effects_box_mm=[0, 0, Wd, Hd], shade=None, squeeze=squeeze)
        fa_, _, win_ = fp.text_layers(T, b0, None, hand=False, board_wh=(Wd, Hd), shade=False, extra_pad=0)
        a = np.zeros((Hd, Wd), bool)
        r0_, r1_, c0_, c1_ = win_
        a[r0_:r1_, c0_:c1_] = fa_ > 0.4
    cols = np.where(a.any(axis=0))[0]
    rows = np.where(a.any(axis=1))[0]
    ink_l, ink_r = float(cols.min() - pad), float(cols.max() + 1 - pad)
    ink_b, ink_t = float(base - (rows.max() + 1)), float(base - rows.min())
    w = ink_r - ink_l
    if anchor == "centre":
        origin = x_mm - (ink_l + ink_r) / 2.0
    elif anchor == "left":
        origin = x_mm - ink_l
    else:
        origin = x_mm - ink_r
    x0 = origin + ink_l
    x1 = origin + ink_r
    sd = shade_d or 0.0
    b = dict(id=bid, text=text, font=font_key, weight=weight, cap_mm=cap_mm, tracking_em=tracking_em, baseline_mm=baseline_mm, anchor=anchor, x_mm=x_mm,
             face=face, face_rgb=face_rgb, shade=(dict(colour=shade_colour, d_mm=sd) if sd else None), technique=technique,
             jitter=(T["common_style"]["hand_jitter"] if hand else None), ghost=False, in_texture=True, role=role, cap_ratio=cr,
             size_px_per_em=px, origin_x_mm=origin, width_mm=w, squeeze=squeeze,
             ink_box_mm=[x0, baseline_mm + ink_b, x1, baseline_mm + ink_t],
             effects_box_mm=[x0 - 3 - (1.6 if hand else 0), baseline_mm + ink_b - 1.6 - (0 if not sd else sd), x1 + sd + 3, baseline_mm + ink_t + 3 + (1.6 if hand else 0)])
    return b


class Small:
    """a plain texture set with the painter's tools, for a sign face, a plate, a tile"""

    def __init__(self, T, name, W, H, seed):
        self.T, self.W, self.H, self.name = T, W, H, name
        self.B = fp.Board(T, None, seed, W=W, H=H, name=name)

    def fill(self, rgb, rough, metal=0.0, amp=1.0, grain=True):
        B = self.B
        win = (0, self.H, 0, self.W)
        kinds = (("streak", 0.50), ("grain", 0.34), ("band", 0.40), ("iso", 0.10), ("fine", 0.22)) if grain else (("band", 0.40), ("iso", 0.15), ("fine", 0.25))
        B.rgb[:] = B.mottle(win, rgb, amp, kinds=kinds)
        B.rough[:] = np.clip(rough + B.noise("band") * 0.025, 0.02, 1)
        B.metal[:] = metal
        B.height[:] = 0.0


def _grime_edge(B, k=0.05):
    rows = np.arange(B.H, dtype=np.float32)
    prof = np.exp(-(B.H - 1 - rows) / 40.0) + 0.7 * np.exp(-rows / 25.0)
    prof -= prof.mean()
    B.rgb += (np.array([88.0, 82.0, 74.0], np.float32) - B.rgb) * (k * prof)[:, None, None]


# ------------------------------------------------------------------ the small wear: how a hanging board or a plate really weathers
def age_small(B, mode_key, frac, grime, anchors=None, drips=(1, (40, 110)), prim=None, wood=None, crack=0.0, scale=0.2, allowed=None, rim=3,
              dark=False, runs_allowed=True):
    """grime that gathers at the foot and corners, paint lost where water and hands work it (the foot, the corners, the chain eyes), cracks along the
    grain, and a drip or two from the top edge; returns the drips layer (the wear layer R) and the info"""
    H, W = B.H, B.W
    mode = fa.MODES[mode_key]
    F = fa.Fields(B, scale=scale, mid=(240, 15), long=(105, 2.0), strip=(26, 1.3))
    fa.grime_film(B, mode, dict(grime_film=grime), [])
    if allowed is None:
        allowed = np.ones((H, W), bool)
        allowed[:rim] = allowed[-rim:] = False
        allowed[:, :rim] = allowed[:, -rim:] = False
    weight = fa.damp_weight(H, W, mode, [], anchors or [], [])
    if crack > 0:
        fa.cracks(B, crack, allowed, weight=weight, dark_board=dark, prim=np.array(prim) if prim is not None else None, strength=0.5)
    info = {}
    if frac > 0:
        a1, a2, S, thr = fa.loss_alpha(F, weight, allowed, allowed, frac, mode, min_px=6)
        fa.apply_loss(B, a1, a2, np.array(prim, np.float32), np.array(wood, np.float32))
        B.layers["loss"] = a1
        info["loss_drawn_fraction"] = round(float((a1 > 0.5).sum() / (H * W)), 4)
        info["substrate_primer"] = [int(v) for v in prim]
        info["substrate_wood"] = [int(v) for v in wood]
    drip_layer = np.zeros((H, W), np.float32)
    placed = []
    if runs_allowed and drips[0]:
        drip_layer, tracks, placed = fa.place_drips(B, drips[0], drips[1], B.rng("drips"), anchors or [], not dark)
        fa.apply_drips(B, drip_layer, tracks, not dark, strength=0.30)
    B.layers["runs"] = drip_layer
    info["drips"] = len(placed)
    return drip_layer, info


# ------------------------------------------------------------------ hanging signs
SIGN_FACE_MARGIN = 24.0


def ink_width(T, text, font_key, weight, cap_mm, tracking_em, squeeze=1.0):
    b = make_block(T, text, font_key, weight, cap_mm, tracking_em, 100, 1000, "centre", "sign_black", squeeze=squeeze)
    return b["width_mm"]


def fit_squeeze(T, text, font_key, weight, cap_mm, tracking_em, avail, s_min=0.5):
    """the least squeeze (nearest 1.0) at which the string at this cap fits `avail` mm: a drawn, condensed face"""
    w1 = ink_width(T, text, font_key, weight, cap_mm, tracking_em, 1.0)
    if w1 <= avail:
        return 1.0, w1
    lo, hi = s_min, 1.0
    w_lo = ink_width(T, text, font_key, weight, cap_mm, tracking_em, lo)
    if w_lo > avail:
        return None, w_lo
    for _ in range(7):
        mid = (lo + hi) / 2.0
        w_m = ink_width(T, text, font_key, weight, cap_mm, tracking_em, mid)
        if w_m <= avail:
            lo = mid
        else:
            hi = mid
    s = round(lo - 0.005, 3)
    return s, ink_width(T, text, font_key, weight, cap_mm, tracking_em, s)


# the signwriter's fills (try 2, the fresh review): a hanging board is lettered to its edges, in two lines where the legend is two words and in a
# condensed face where the word is long. `cap_hi` is the cap asked for; the squeeze is the least that fits.
SIGN_LAYOUT = {
    "steam_laundry_box": dict(lines=["LAUNDERETTE"], cap_hi=80, cap_lo=70),
    "ironmonger_hanging_board": dict(lines=["KEYS", "CUT"], cap_hi=108, cap_lo=70),
    "chandler_hanging_board": dict(lines=["CHANDLERY"], cap_hi=115, cap_lo=90),
}


def render_sign_face(T, sign, face_label, seed, lit_off=False):
    """one face of a hanging sign. Returns (Small, record)"""
    sid = sign["id"]
    fcs = sign["faces"]
    if sid == "steam_laundry_box":
        W, H = 620, 450
    else:
        bm = sign["parts"]["board_m"]
        W, H = int(round(bm[0] * 1000)), int(round(bm[1] * 1000))
    S = Small(T, f"{sid}_{face_label}", W, H, seed)
    B = S.B
    rec = dict(face=face_label, size_mm=[W, H])
    fk, wt = fcs["font"], fcs["weight"] or 400
    cap_t = fcs["cap_mm"]
    trk = fcs["tracking_em"]
    lay = SIGN_LAYOUT[sid]
    lines = lay["lines"]
    win = (0, H, 0, W)
    if sid == "steam_laundry_box":
        frame = 20.0
        bronze = fc.pal(T, "bronze_anodised")
        white = fc.pal(T, "acrylic_white")
        S.fill(bronze, 0.35, 1.0, amp=1.0)
        a = fp.rect_alpha(win, frame, frame, W - frame, H - frame, H=B.H)
        B.paint(win, a, B.mottle(win, white, 0.45, kinds=(("band", 0.7), ("fine", 0.3))), rough=0.35, metal=0.0)
        avail_w = W - 2 * frame - 2 * SIGN_FACE_MARGIN
        avail_h = H - 2 * frame - 2 * 52
        technique, hand, light = "vinyl", False, True
        shade_cfg = None
        sq_lo = 0.5
        trk = 0.02
    elif sid == "ironmonger_hanging_board":
        S.fill(fc.pal(T, "buff_board"), 0.55, 0.0, amp=1.0)
        inset, rule = 20.0, 6.0
        pts = [[inset, inset], [W - inset, inset], [W - inset, H - inset], [inset, H - inset], [inset, inset]]
        a = fp.poly_alpha(win, pts, rule, H=B.H)
        B.paint(win, a, B.mottle(win, fc.pal(T, "sign_black"), 1.0, kinds=(("band", 0.7), ("fine", 0.3))), rough=0.45, metal=0.0, height=0.20)
        avail_w = W - 2 * (inset + rule) - 2 * SIGN_FACE_MARGIN
        avail_h = H - 2 * (inset + rule) - 2 * 26
        technique, hand, light = "painted", True, True
        shade_cfg = fcs.get("shade")
        sq_lo = 0.8
    else:                                                   # chandler
        S.fill(fc.pal(T, "navy"), 0.5, 0.0, amp=1.0)
        inset, rope = 24.0, 10.0
        x0, y0, x1, y1 = inset + rope / 2, inset + rope / 2, W - inset - rope / 2, H - inset - rope / 2
        r = 30.0
        pts = []
        for (cx, cy, a0, a1) in ((x1 - r, y0 + r, -90, 0), (x1 - r, y1 - r, 0, 90), (x0 + r, y1 - r, 90, 180), (x0 + r, y0 + r, 180, 270)):
            for k in range(9):
                ang = math.radians(a0 + (a1 - a0) * k / 8)
                pts.append([cx + r * math.cos(ang), cy + r * math.sin(ang)])
        pts.append(pts[0])
        a, pat = rope_alpha_and_pattern(win, pts, rope, 22.0, H=H)
        base = B.mottle(win, fc.pal(T, "hemp"), 1.2, kinds=(("fine", 0.6), ("band", 0.4)))
        B.paint(win, a, np.clip(base * (1.0 + 0.16 * pat[..., None]), 0, 255), rough=0.8, metal=0.0, height=0.15)
        avail_w = W - 2 * (inset + rope) - 2 * SIGN_FACE_MARGIN
        avail_h = H - 2 * (inset + rope) - 2 * 30
        technique, hand, light = "painted", True, False
        shade_cfg = fcs.get("shade")
        sq_lo = 0.5
    # the lettering, fitted: the biggest cap (down from cap_hi) at which the longest line fits the width at the least squeeze, and the lines the height
    colour = fcs["colour"]
    cap = lay["cap_hi"]
    n_l = len(lines)
    gap_k = 0.26
    while True:
        longest = max(lines, key=lambda x: ink_width(T, x, fk, wt, cap, trk))
        s_q, w_fit = fit_squeeze(T, longest, fk, wt, cap, trk, avail_w, s_min=sq_lo)
        sd = round(shade_cfg["d_mm"] * cap / cap_t, 1) if shade_cfg else 0.0
        tot_h = n_l * cap + (n_l - 1) * gap_k * cap + sd
        if s_q is not None and tot_h <= avail_h:
            break
        cap -= 2.0
        if cap < lay["cap_lo"]:
            raise ValueError(f"{sid}: the legend does not fit at any cap down to {lay['cap_lo']} mm")
    rec.update(cap_mm_target=cap_t, cap_mm_built=cap, ink_width_target_cap_mm=round(ink_width(T, longest, fk, wt, cap_t, trk), 1), available_mm=round(avail_w, 1),
               squeeze=s_q, lines=lines)
    blocks, recs = [], []
    top_y = H / 2.0 + tot_h / 2.0 - sd
    for i, ln in enumerate(lines):
        base_y = top_y - cap - i * (cap * (1 + gap_k))
        b = make_block(T, ln, fk, wt, cap, trk, int(round(base_y)), W / 2.0, "centre", colour, shade_d=sd or None,
                       shade_colour=(shade_cfg["colour"] if shade_cfg else "shade_black"), technique=technique, hand=hand, bid=f"face{i + 1}", W=W, H=H, squeeze=s_q)
        blocks.append(b)
        drawn = fp.paint_block(B, b, ground_rough=0.45 if hand else 0.35)
        recs.append(dict(string=ln, font=fk, weight=wt, cap_mm=cap, tracking_em=trk, baseline_mm=int(round(base_y)), centre_x_mm=W / 2.0, face=colour,
                         shade=shade_cfg and dict(shade_cfg, d_mm=sd), ink_box_mm=[round(v, 1) for v in b["ink_box_mm"]], origin_x_mm=round(b["origin_x_mm"], 2),
                         cap_ratio=round(b["cap_ratio"], 4), size_px_per_em=round(b["size_px_per_em"], 3), width_mm=round(b["width_mm"], 1), hand_jitter=hand,
                         technique=technique, squeeze=s_q))
    rec["block"] = recs[0]
    rec["blocks"] = recs
    rec["b"] = blocks[0]
    rec["bs"] = blocks
    # the laundry's other lettering device: two blue vinyl rules, so the long narrow word is framed and no ground is left blank
    if sid == "steam_laundry_box":
        for yy in (H / 2.0 + cap / 2.0 + 62.0, H / 2.0 - cap / 2.0 - 62.0):
            ra = fp.rect_alpha(win, frame + 36, yy - 3.0, W - frame - 36, yy + 3.0, H=B.H)
            B.paint(win, ra, B.mottle(win, fc.pal(T, colour), 0.4, kinds=(("fine", 0.5),)), rough=0.45, height=0.08)
        rec["rules_y_mm"] = [round(H / 2.0 + cap / 2.0 + 62.0, 1), round(H / 2.0 - cap / 2.0 - 62.0, 1)]
    # ---- wear: from the edges, not in the open field
    if sid == "steam_laundry_box":
        # acrylic: it yellows at the edges, the grime gathers at the foot, dead flies lie along the foot inside, a weep from the top seal
        fa.grime_film(B, fa.MODES["hanging"], dict(grime_film=0.16), [], amp=1.0)
        rows = np.arange(H, dtype=np.float32)[:, None]
        cols = np.arange(W, dtype=np.float32)[None, :]
        edge = np.minimum(np.minimum(rows - frame, H - frame - rows), np.minimum(cols - frame, W - frame - cols))
        yel = np.clip(1.0 - edge / 70.0, 0, 1) * 0.55
        B.rgb[..., 2] *= (1.0 - 0.08 * yel)
        B.rgb[..., 1] *= (1.0 - 0.020 * yel)
        fly_rng = B.rng("flies")
        nfl = int(fly_rng.integers(9, 17))
        for q in range(nfl):
            fx = float(fly_rng.uniform(frame + 14, W - frame - 14))
            fy = float(fly_rng.uniform(frame + 6, frame + 46))
            wf = B.win(fx - 6, fy - 6, fx + 6, fy + 6)
            al = fp.disc_alpha(wf, fx, fy, float(fly_rng.uniform(0.9, 2.0)), H=B.H)
            B.paint(wf, al * 0.8, np.array([58.0, 52.0, 44.0]), rough=0.6)
        free_top = np.zeros((H, W), bool)
        drips, tracks, pl = fa.place_drips(B, 1, (60, 140), B.rng("drips"), [W * 0.3, W * 0.7], True)
        fa.apply_drips(B, drips, tracks, True, strength=0.30)
        B.layers["runs"] = drips
        rec["wear"] = dict(runs=len(pl), flies=nfl, edges="yellowing at the edges, grime at the foot")
        # lit from inside when the shop is open: face colour x 0.85; the bronze frame does not glow
        level = np.zeros((H, W), np.float32)
        level[int(frame):H - int(frame), int(frame):W - int(frame)] = 0.85
        # two tubes inside a 140 mm box: a soft bright band along each, the light falling off toward the frame and into the corners (try 2, signs note 1)
        yy_, xx_ = np.mgrid[0:H, 0:W].astype(np.float32)
        band = 1.0 + 0.09 * np.exp(-((yy_ - H * 0.32) / 42.0) ** 2) + 0.09 * np.exp(-((yy_ - H * 0.68) / 42.0) ** 2)
        edge_fall = 1.0 - 0.12 * np.exp(-np.minimum(np.minimum(xx_ - frame, W - frame - xx_), np.minimum(yy_ - frame, H - frame - yy_)) / 45.0)
        level = level * band * edge_fall
        B.emis = np.clip(B.rgb * level[..., None], 0, 255)
        rec["emissive"] = dict(level=0.85, face_mm=[frame, frame, W - frame, H - frame])
    else:
        prim, wood = ((150, 144, 122), (112, 98, 82)) if sid == "ironmonger_hanging_board" else ((140, 146, 150), (118, 104, 90))
        frac = 0.04 if sid == "ironmonger_hanging_board" else 0.035
        chain_x = [W * 0.14, W * 0.86] if sid == "chandler_hanging_board" else [W * 0.18, W * 0.82]
        drips, info = age_small(B, "hanging", frac, 0.16, anchors=chain_x, drips=(2, (40, 120)), prim=prim, wood=wood, crack=0.15 if sid == "ironmonger_hanging_board" else 0.10,
                                scale=0.25, dark=not light)
        rec["wear"] = dict(runs=info["drips"], loss_fraction_drawn=info.get("loss_drawn_fraction"), substrate_primer=info.get("substrate_primer"), substrate_wood=info.get("substrate_wood"))
    return S, rec


# ------------------------------------------------------------------ the three gilt balls
def render_ball(T, k, seed):
    """a ball's equirectangular texture: 817 mm round (0.26 m x pi) by 409 mm pole to pole. Gilt paint over sheet metal: it dulls and darkens with grime, flakes
    along the seam of the two pressed halves and round the crown where the hanger rod comes in, and rusts there (nobody reaches 2.65 m: no 'scuffed where hands reach')"""
    W, H = 817, 409
    S = Small(T, f"ball_{k}", W, H, seed)
    B = S.B
    gold = fc.pal(T, "gold_leaf")
    S.fill(gold, 0.45, 0.7, amp=1.4, grain=False)
    r = B.rng("tarnish")
    rows = np.arange(H, dtype=np.float32)[:, None]
    # the gilt has dulled: a smoky film, more on the lower half (the road's spray) and under the crown
    dull = np.clip(0.18 + 0.30 * (rows / H) + 0.10 * fc.fnoise((H, W), 60, 14, r), 0, 0.6)
    B.rgb[:] = B.rgb * (1.0 - 0.40 * dull[..., None]) + np.array([92.0, 78.0, 52.0])[None, None, :] * 0.40 * dull[..., None]
    B.rough[:] = np.clip(B.rough + 0.25 * dull, 0, 1)
    B.metal[:] = np.clip(B.metal - 0.35 * dull, 0, 1)
    # the pressed halves' seam at the equator: the gilt cracks along it; rust at the crown, where the rod comes in (v = 0 is the pole)
    mode = dict(fa.MODES["hanging"], bottom=(0.0, 20), top=(0.0, 20), ends=(0.0, 40), joint=(0.0, 20), nail=(0.0, 20), base=0.12)
    seam = np.exp(-((rows - H / 2.0) / 5.0) ** 2) * 2.4
    crown = np.exp(-rows / 22.0) * 4.0 + np.exp(-(H - rows) / 14.0) * 2.0
    weight = (0.10 + seam + crown).astype(np.float32) * np.ones((1, W), np.float32)
    F = fa.Fields(B, scale=0.2, mid=(240, 15), long=(105, 2.2), strip=(26, 1.6))
    allowed = np.ones((H, W), bool)
    a1, a2, Sx, thr = fa.loss_alpha(F, weight, allowed, allowed, 0.045, mode, min_px=6)
    fa.apply_loss(B, a1, a2, np.array([120.0, 100.0, 70.0], np.float32), np.array([112.0, 74.0, 46.0], np.float32), relief=(-0.2, -0.35))
    # rust streaks run down from the crown
    rr = B.rng("rust")
    for i in range(int(rr.integers(5, 9))):
        x = int(rr.integers(10, W - 10))
        L = int(rr.integers(30, 120))
        prof = np.exp(-((np.arange(-6, 7)) / rr.uniform(2.0, 3.6)) ** 2)
        for q in range(L):
            fade = max(0.0, 1.0 - q / L) ** 1.4
            cols = np.clip(x + int(2 * math.sin(q / 17.0 + i)) + np.arange(-6, 7), 0, W - 1)
            B.rgb[q, cols] = B.rgb[q, cols] + (np.array([112.0, 62.0, 34.0]) - B.rgb[q, cols]) * (0.55 * fade * prof)[:, None]
    # the equator seam: a fine groove
    sm = np.exp(-((rows - H / 2.0) / 1.2) ** 2).astype(np.float32)
    B.rgb *= (1.0 - 0.11 * sm)[..., None]
    B.height += -0.2 * sm
    fa.grime_film(B, fa.MODES["hanging"], dict(grime_film=0.10), [], amp=1.0)
    return S, dict(size_mm=[W, H], note="equirectangular: u round the ball, v pole to pole; one texture per ball, each with its own seed")


# ------------------------------------------------------------------ glass lettering rows
GLASS_COL = {
    "gold leaf": "gold_leaf", "whitewash": "whitewash", "white paint": "white_paint", "cream vinyl": "vinyl_cream", "paint": "white_paint",
}
GLASS_PAD = 14


def glass_style(g):
    t = g["technique"].lower()
    m = re.search(r"shade (\d+(?:\.\d+)?) mm", t)
    shade = float(m.group(1)) if m else None
    if "black shade" in t and shade is None:
        shade = round(0.03 * g["cap_mm"], 1)
    if "gold leaf" in t:
        return dict(kind="gold", face="gold_leaf", shade=shade, shade_colour="shade_black", rough=0.15, metal=1.0, hand=False)
    if "whitewash" in t:
        return dict(kind="whitewash", face="whitewash", shade=None, rough=0.90, metal=0.0, hand=True, opacity=0.85)
    if "red shade" in t:
        return dict(kind="paint_red_shade", face="white_paint", shade=round(0.06 * g["cap_mm"], 1), shade_colour="vermilion", rough=0.5, metal=0.0, hand=True)
    if "flaking" in t:
        return dict(kind="paint_flaking", face="white_paint", shade=None, rough=0.7, metal=0.0, hand=True, flaking=True)
    if "cream vinyl" in t:
        return dict(kind="vinyl", face="vinyl_cream", shade=None, rough=0.45, metal=0.0, hand=False)
    if "white" in t and "vinyl" in t:
        return dict(kind="vinyl", face=None, face_rgb=(236, 233, 224), shade=None, rough=0.45, metal=0.0, hand=False)
    raise ValueError(t)


def glass_tracking(g, st):
    """the tracking of a glass row: the row's own (a gilder closes the 1 of '16' up to its partner) or the style's"""
    if g.get("tracking_em") is not None:
        return float(g["tracking_em"])
    return 0.05 if st["kind"] != "vinyl" else 0.03


def glass_lines(g):
    if g.get("hours"):
        cast = json.loads(fc.HOOK_CAST.read_text(encoding="utf-8"))
        return hours_lines(g["shop"], cast)
    return list(g.get("lines") or [g["text"]])


LINE_PITCH = 1.55


def flake_mask(shape, rng, fraction=0.16):
    """sharp-edged flakes of paint lifting off glass: irregular, angular, some lost at the letter's edges"""
    n1 = fc.fnoise(shape, 7.0, 4.5, rng)
    n2 = fc.fnoise(shape, 2.6, 2.6, rng)
    s = n1 + 0.55 * n2
    thr = float(np.quantile(s, 1.0 - fraction))
    m = s > thr
    # angular: threshold hard, then a slight opening so the flakes are polygons and not fuzz
    m = ndi.binary_opening(m, iterations=1) | ndi.binary_dilation(ndi.binary_erosion(m, iterations=2), iterations=2) & m
    return m


def render_glass_row(T, g, idx, seed):
    st = glass_style(g)
    fk = g["font"]
    wt = g["weight"] or 400
    cap = g["cap_mm"]
    lines = glass_lines(g)
    n_l = len(lines)
    trk = glass_tracking(g, st)
    figure = all(ln.replace(" ", "").isdigit() for ln in lines)
    probes = [make_block(T, ln, fk, wt, cap, trk, 100, 1000, "centre", "sign_black", figure=figure) for ln in lines]
    w = max(pb["width_mm"] for pb in probes)
    sd = st["shade"] or 0.0
    pitch = cap * LINE_PITCH
    W = int(math.ceil(w + sd + 2 * GLASS_PAD + 6 + (22 if st["kind"] == "whitewash" else 0)))
    H = int(math.ceil(cap * 1.45 + (n_l - 1) * pitch + sd + 2 * GLASS_PAD))
    base = int(GLASS_PAD + cap * 0.18 + sd)
    S = Small(T, f"glass_{idx}", W, H, seed)
    B = S.B
    B.rgb[:] = 0
    B.rough[:] = 0.5
    face_rgb = st.get("face_rgb")
    rng = B.rng("glass")
    technique = "gilded" if st["kind"] == "gold" else ("vinyl" if st["kind"] == "vinyl" else "painted")
    A = np.zeros((H, W), np.float32)
    face_alpha = np.zeros((H, W), np.float32)
    shade_col = None
    blocks = []
    line_recs = []
    brush_info = []
    for li, ln in enumerate(lines):
        # the first line is the top one: the lowest line stands on `base`
        base_i = base + int(round((n_l - 1 - li) * pitch))
        b = make_block(T, ln, fk, wt, cap, trk, base_i, W / 2.0 - sd / 2.0, "centre", st["face"] or "whitewash", shade_d=sd or None,
                       shade_colour=st.get("shade_colour", "shade_black"), technique=technique,
                       hand=st["hand"], bid=f"glass{li + 1}", face_rgb=list(face_rgb) if face_rgb else None, figure=figure)
        blocks.append(b)
        line_recs.append(dict(string=ln, baseline_from_bottom_mm=base_i, ink_box_mm=[round(v, 1) for v in b["ink_box_mm"]]))
        if st["kind"] == "whitewash":
            # brushed whitewash: the letters are laid stroke by stroke along the font's own centre line (fascia_brush)
            a_b, binfo = fb.brush_text(T, ln, fk, cap, W, H, base_i, W / 2.0, rng, weight=wt, tracking_em=trk, whitewash_alpha=st["opacity"])
            brush_info.append(binfo)
            fa_ = a_b
            sh_ = None
            win = (0, H, 0, W)
        else:
            face, sh_, win = fp.text_layers(T, b, rng, hand=st["hand"], board_wh=(W, H))
            fa_ = face.copy()
            if st.get("flaking"):
                fl = flake_mask(fa_.shape, rng)
                fa_ = np.where(fl, 0.0, fa_)
                fa_ = fa_ * np.clip(1.0 - 0.25 * ndi.gaussian_filter(fl.astype(np.float32), 1.5), 0, 1)
        fcol = fp.block_rgb(T, b)
        amp = {"gold": 2.0, "whitewash": 1.6, "paint_red_shade": 1.2, "paint_flaking": 1.5, "vinyl": 0.4}[st["kind"]]
        r0, r1, c0, c1 = win
        fimg = B.mottle(win, fcol, amp, kinds=(("band", 0.6), ("iso", 0.4), ("fine", 0.35)))
        # shade (gold and painted blocks): under the face
        if sh_ is not None:
            scol = np.asarray(fp.block_rgb(T, dict(face=b["shade"]["colour"], face_rgb=None)), np.float32)
            sa = np.clip(sh_, 0, 1)
            cur_a = A[r0:r1, c0:c1]
            cur_rgb = B.rgb[r0:r1, c0:c1]
            new_a = np.clip(sa + cur_a * (1.0 - sa), 0, 1)
            B.rgb[r0:r1, c0:c1] = np.where(new_a[..., None] > 1e-4, (scol[None, None, :] * sa[..., None] + cur_rgb * (cur_a * (1.0 - sa))[..., None]) / np.maximum(new_a[..., None], 1e-4), cur_rgb)
            A[r0:r1, c0:c1] = new_a
            shade_col = scol
        cur_a = A[r0:r1, c0:c1]
        cur_rgb = B.rgb[r0:r1, c0:c1]
        fa_c = np.clip(fa_, 0, 1)
        new_a = np.clip(fa_c + cur_a * (1.0 - fa_c), 0, 1)
        B.rgb[r0:r1, c0:c1] = np.where(new_a[..., None] > 1e-4, (fimg * fa_c[..., None] + cur_rgb * (cur_a * (1.0 - fa_c))[..., None]) / np.maximum(new_a[..., None], 1e-4), fimg)
        A[r0:r1, c0:c1] = new_a
        fa_full = np.zeros((H, W), np.float32)
        fa_full[r0:r1, c0:c1] = fa_c
        face_alpha = np.maximum(face_alpha, fa_full)
    # roughness/metal: the leaf's own; shade is paint
    B.rough[:] = st["rough"]
    B.metal[:] = st["metal"]
    if st["kind"] == "gold":
        sh_only = np.clip(A - face_alpha, 0, 1)
        B.rough[:] = st["rough"] * (1 - sh_only) + 0.6 * sh_only
        B.metal[:] = st["metal"] * (1 - sh_only)
    rows = np.where((face_alpha > 0.5).any(axis=1))[0]
    cols = np.where((face_alpha > 0.5).any(axis=0))[0]
    rec = dict(size_mm=[W, H], style=st["kind"], figure_height_sized=figure, baseline_row_from_bottom_mm=base, face_alpha_ink_box_in_tile_mm=[int(cols.min()), int(H - (rows.max() + 1)), int(cols.max() + 1), int(H - rows.min())] if len(rows) else None,
               block=blocks[0], blocks=blocks, lines=line_recs, line_pitch_mm=round(pitch, 1), tracking_em=trk, cap_mm=cap, brush=brush_info or None)
    return S, A, face_alpha, rec


def render_window_wash(T, seed, W=3250, H=1800):
    """the empty unit's whole window whitewashed (ruled 3 Oct): try 2 -- whiting laid on with a wet cloth. Near-opaque white to cream from across the street;
    the hand leaves overlapping circular and fan-shaped swirls 0.3 to 0.9 m across whose edges are a faint tide mark; thin and clear spots where the cloth
    went over twice; a clear margin that is ragged along the glazing, corners the cloth missed; dribbles hanging from the foot. Nothing legible."""
    S = Small(T, "empty_window", W, H, seed)
    B = S.B
    r = B.rng("wash")
    k = 2                                               # drawn at half size, then up
    w2, h2 = W // k, H // k
    canvas = np.full((h2, w2), 0.875, np.float32)
    # the cloth goes round: each stroke is a circular or fan-shaped sweep of the hand, 150 to 450 mm in radius, a band 60 to 170 mm wide with soft edges,
    # fading at both ends. It levels the coat to a thickness of its own and leaves fine concentric grooves along its path; the next stroke goes over it
    n_stroke = 90
    strokes = []
    for i in range(n_stroke):
        cx, cy = float(r.uniform(-0.1, 1.1) * w2), float(r.uniform(-0.1, 1.1) * h2)
        R = float(r.uniform(150, 450)) / k
        wd = float(r.uniform(60, 170)) / k
        a0 = float(r.uniform(0, 2 * math.pi))
        span = float(r.uniform(1.4, 4.6))
        lvl = float(np.clip(r.normal(0.885, 0.042), 0.78, 0.96))
        gscale = float(r.uniform(3.0, 8.0)) / k
        phase = float(r.uniform(0, 6.28))
        gamp = float(r.uniform(0.012, 0.03))
        x0, x1 = int(max(0, cx - R - wd)), int(min(w2, cx + R + wd + 1))
        y0, y1 = int(max(0, cy - R - wd)), int(min(h2, cy + R + wd + 1))
        if x1 <= x0 + 4 or y1 <= y0 + 4:
            continue
        yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
        dx, dy = xx - cx, yy - cy
        rr = np.sqrt(dx * dx + dy * dy)
        th = (np.arctan2(dy, dx) - a0) % (2 * math.pi)
        u = np.clip(th / span, 0, 1) * (th < span)
        ang_fade = np.clip(np.sin(math.pi * u) * 2.2, 0, 1)
        rad_prof = np.clip(1.0 - np.abs(rr - R) / (wd * 0.5), 0, 1)
        rad_prof = rad_prof * rad_prof * (3 - 2 * rad_prof)
        m = rad_prof * ang_fade
        # the concentric grooves: a ring texture, a function of the radius only (the hand goes round, the cloth's weave follows the circle)
        g = np.sin(rr / gscale * 2 * math.pi / 3.0 + phase) * 0.6 + np.sin(rr / (gscale * 0.37) + 2.0 * phase) * 0.4
        sub = canvas[y0:y1, x0:x1]
        w_ = np.clip(m * 0.82, 0, 1)
        canvas[y0:y1, x0:x1] = sub * (1 - w_) + (lvl + gamp * g) * w_
        # the tide mark at the outer edge of a stroke: a hair of thicker whiting where the cloth stopped
        ridge = np.exp(-(((np.abs(rr - R) - wd * 0.48) / (1.6 / k + 0.6)) ** 2)) * ang_fade * 0.030
        canvas[y0:y1, x0:x1] += ridge.astype(np.float32)
        strokes.append((round(cx * k), round(cy * k), round(R * k)))
    n_c = fc.fnoise((h2, w2), 95, 40, r)
    a = canvas + 0.020 * n_c
    a = np.asarray(Image.fromarray(a.astype(np.float32)).resize((W, H), Image.BICUBIC), np.float32)
    a = np.clip(a + 0.012 * fc.fnoise((H, W), 1.3, 1.3, r), 0, 1.0)
    # thin and clear spots: finger-wiped, cloth-wiped places where the coat is thin
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    spot_noise = fc.fnoise((H, W), 34, 24, r)
    for i in range(int(r.integers(10, 16))):
        cx, cy = r.uniform(80, W - 80), r.uniform(80, H - 80)
        rx, ry = r.uniform(60, 200), r.uniform(28, 95)
        ang = r.uniform(0, math.pi)
        u = (xx - cx) * math.cos(ang) + (yy - cy) * math.sin(ang)
        v = -(xx - cx) * math.sin(ang) + (yy - cy) * math.cos(ang)
        dd = np.sqrt((u / rx) ** 2 + (v / ry) ** 2)
        dd = dd + 0.40 * spot_noise                                   # irregular, not a neat ellipse
        spot = np.clip((1.0 - dd) * 1.3, 0, 1) * r.uniform(0.12, 0.26)
        a = a - spot
    # the margin: the wash does not reach the glazing everywhere; the edge is ragged, corners are missed
    edge_n = [np.abs(fc.fnoise((1, max(W, H) + 16), 70, 0.01, r)[0]) * 0.7 + np.abs(fc.fnoise((1, max(W, H) + 16), 14, 0.01, r)[0]) * 0.5 + np.abs(fc.fnoise((1, max(W, H) + 16), 4, 0.01, r)[0]) * 0.25
              for _ in range(4)]
    mt = 12 + 24 * edge_n[0][:W]                   # top, left-right
    mb = 44 + 36 * edge_n[1][:W]                   # bottom (room for the dribbles)
    ml = 10 + 22 * edge_n[2][:H]
    mr = 10 + 22 * edge_n[3][:H]
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32) if False else (yy, xx)
    d_top = yy
    d_bot = (H - 1 - yy)
    d_l = xx
    d_r = (W - 1 - xx)
    marg = np.minimum(np.minimum((d_top - mt[None, :]) / 12.0, (d_bot - mb[None, :]) / 12.0), np.minimum((d_l - ml[:, None]) / 12.0, (d_r - mr[:, None]) / 12.0))
    a = a * np.clip(marg, 0, 1)
    for (cx, cy, sz) in ((0, 0, r.uniform(80, 200)), (W, 0, r.uniform(60, 160)), (0, H, r.uniform(90, 220)), (W, H, r.uniform(70, 180))):
        if r.random() < 0.8:
            dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) + 18 * fc.fnoise((H, W), 22, 22, r)
            a = a * np.clip((dd - sz) / 10.0, 0, 1)
    # dribbles: a thin run of whiting hanging from the foot of the coat
    for i in range(int(r.integers(22, 32))):
        x = int(r.uniform(60, W - 60))
        y0 = int(H - mb[x] - 4)
        L = int(r.uniform(35, 190))
        wd = r.uniform(2.0, 6.5)
        for q in range(L):
            tq = q / L
            ww = max(0.8, wd * (1.0 - 0.5 * tq))
            cols = np.arange(int(x - 6), int(x + 7))
            prof = np.clip(1.0 - (np.abs(cols - x - 1.2 * math.sin(q / 14.0)) - ww / 2) / 1.0, 0, 1)
            yq = y0 + q
            if yq < H - 3:
                a[yq, cols] = np.maximum(a[yq, cols], prof * (0.88 - 0.25 * tq))
        yb = min(H - 3, y0 + L)
        a[max(0, yb - 3):yb + 3, max(0, x - 4):x + 5] = np.maximum(a[max(0, yb - 3):yb + 3, max(0, x - 4):x + 5], np.clip(1.4 - np.sqrt((np.arange(max(0, yb - 3), yb + 3)[:, None] - yb) ** 2 + (np.arange(max(0, x - 4), x + 5)[None, :] - x) ** 2) / (wd * 0.7 + 0.8), 0, 1) * 0.85)
    a = np.clip(a, 0, 0.985)
    ww_ = fc.pal(T, "whitewash")
    cream = np.array([226.0, 219.0, 200.0])
    # whiter where the coat is thick, a little grey and cream where thin
    tone = np.clip((a - 0.6) / 0.35, 0, 1)
    rgb = (cream[None, None, :] * (1 - tone[..., None]) + ww_[None, None, :] * 1.02 * tone[..., None]) * (1.0 + 0.015 * fc.fnoise((H, W), 30, 30, r)[..., None])
    B.rgb[:] = rgb
    B.rough[:] = 0.9
    B.metal[:] = 0.0
    B.height[:] = (0.1 * a).astype(np.float32)
    return S, a


# ------------------------------------------------------------------ the letting board and the hours signs
def render_letting_board(T, seed):
    sp = [p for p in T["small_panels"] if p["id"] == "letting_board"][0]
    W, H = sp["size_mm"]
    S = Small(T, "letting_board", W, H, seed)
    B = S.B
    white = fc.pal(T, "white_paint")
    S.fill(white, 0.55, 0.0, amp=0.9)
    win = (0, H, 0, W)
    # a painted board: a plain edge, a faint inner line
    edge = 14.0
    a = fp.rect_alpha(win, 0, 0, W, H, H=B.H) - fp.rect_alpha(win, edge, edge, W - edge, H - edge, H=B.H)
    B.paint(win, np.clip(a, 0, 1), B.mottle(win, white * 0.94, 0.8, kinds=(("band", 0.7), ("fine", 0.3))), rough=0.6)
    b = make_block(T, sp["text"], sp["font"], sp["weight"], sp["cap_mm"], 0.06, int(H / 2 - sp["cap_mm"] / 2), W / 2.0, "centre", sp["colour"], technique="vinyl",
                   bid="letting")
    fp.paint_block(B, b, ground_rough=0.55)
    # four screws, slightly proud; a rust run under each lower screw (the target)
    inset = 55.0
    r = B.rng("screws")
    heads = [(inset, H - inset), (W - inset, H - inset), (inset, inset), (W - inset, inset)]
    for (x, y) in heads:
        w_ = B.win(x - 10, y - 10, x + 10, y + 10)
        al = fp.disc_alpha(w_, x, y, 6.5, H=B.H)
        B.paint(w_, al, np.array([120.0, 118.0, 112.0]), rough=0.4, metal=1.0, height=0.6)
        slot = fp.rect_alpha(w_, x - 5, y - 0.8, x + 5, y + 0.8, H=B.H)
        B.paint(w_, slot * al, np.array([40.0, 38.0, 36.0]), height=-0.4)
    # the board weathers from its edges: a bare foot rail and corners, grime at the foot, a drip or two from the top edge (none in the open field)
    allowed_l = np.ones((H, W), bool)
    allowed_l[:3] = allowed_l[-3:] = False
    allowed_l[:, :3] = allowed_l[:, -3:] = False
    tb = b["effects_box_mm"]
    allowed_l[max(0, H - int(tb[3]) - 6):min(H, H - int(tb[1]) + 6), max(0, int(tb[0]) - 6):min(W, int(tb[2]) + 6)] = False      # the vinyl letters are stuck fast
    drips, winfo = age_small(B, "hanging", 0.035, 0.16, anchors=[W * 0.25, W * 0.75], drips=(1, (50, 130)), prim=(190, 184, 166), wood=(132, 118, 100), crack=0.0,
                             scale=0.3, allowed=allowed_l)
    lower = [heads[2], heads[3]]
    rl = fw.place_rust(B, [(x, y - 7) for x, y in lower], [float(r.uniform(38, 52)) for _ in lower], r, True)
    fw.apply_rust(B, rl)
    B.layers["rust"] = rl
    return S, dict(size_mm=[W, H], block=b, screws=[[round(x, 1), round(y, 1)] for x, y in heads], rust_runs=2, askew_deg=2,
                   centre_on_fascia_mm=sp["centre_on_board_mm"], rust_layer=rl, wear=winfo)


def hours_lines(shop_id, cast, ampm=False):
    """MON-SAT / WED / SUN lines from hook-cast.json's hours. ampm (the caff's card): '6.30 AM - 10 PM' and '8 AM - 12 NOON', so no one reads 6.30 to 10 in the morning"""
    area = {"ritas": "ritas", "fish_market": "fish_market", "steam_laundry": "laundry", "newsagent": "newsagent", "tea_rooms": "cafe"}[shop_id]
    hrs = cast["areas"][area]["hours"]

    def t(h):
        if h >= 24:
            h -= 24
        h12 = h if h <= 12 else h - 12
        whole = int(h12)
        frac = int(round((h12 - whole) * 60))
        return f"{whole}" if frac == 0 else f"{whole}.{frac:02d}"

    def span(o_c):
        if ampm:
            o, c = o_c
            def part(x, closing):
                s_ = t(x)
                if x == 12:
                    return "12 NOON"
                return f"{s_} {'PM' if x >= 12 else 'AM'}"
            return f"{part(o, False)} - {part(c, True)}"
        return f"{t(o_c[0])}-{t(o_c[1])}"
    days = ["mon", "tue", "wed", "thu", "fri", "sat"]
    base = hrs.get("mon")
    lines = [f"MON-SAT {span(base)}"]
    for d in days:
        if d in hrs and hrs[d] != base:
            lines.append(f"{d.upper()} {span(hrs[d])}")
    if "sun" in hrs:
        lines.append(f"SUN {span(hrs['sun'])}")
    else:
        lines.append("SUN CLOSED")
    return lines


def render_hours_plate(T, shop_id, cast, seed):
    """the launderette's hours: an engraved black laminate plate (white core showing through the cut letters), bevelled edge, four screws"""
    sp = [p for p in T["small_panels"] if p["id"] == "hours_plate"][0]
    W, H = sp["size_mm"]
    S = Small(T, f"hours_{shop_id}", W, H, seed)
    B = S.B
    black = np.array([34.0, 34.0, 36.0])
    S.fill(black, 0.35, 0.0, amp=0.8, grain=False)
    win = (0, H, 0, W)
    # the bevelled edge: the white core shows as a hair line round the plate
    bev = 3.0
    edge = fp.rect_alpha(win, 0, 0, W, H, H=B.H) - fp.rect_alpha(win, bev, bev, W - bev, H - bev, H=B.H)
    B.paint(win, np.clip(edge, 0, 1), np.array([196.0, 192.0, 180.0]), rough=0.4)
    lines = hours_lines(shop_id, cast)
    cap_t = 30.0
    avail = W - 2 * 30.0
    widest = max(ink_width(T, ln, "libre-franklin", 600, cap_t, 0.05) for ln in lines)
    cap = cap_t if widest <= avail else math.floor(cap_t * avail / widest * 2) / 2.0
    pitch = cap * 1.8
    top_y = H / 2.0 + (len(lines) * pitch - (pitch - cap)) / 2.0 - cap
    blocks = []
    for i, ln in enumerate(lines):
        base = int(round(top_y - i * pitch))
        b = make_block(T, ln, "libre-franklin", 600, cap, 0.05, base, W / 2.0, "centre", "vinyl_cream", technique="vinyl", bid=f"line{i + 1}", role="hours",
                       face_rgb=[232, 228, 210])
        face, _, wn = fp.text_layers(T, b, None, hand=False, board_wh=(W, H), shade=False)
        # engraved: the letter is cut into the black skin, the white core shows, a hair darker in the cut's walls
        B.paint(wn, face, np.array([226.0, 222.0, 204.0]), rough=0.5, height=-0.35)
        blocks.append(b)
    # four countersunk screws and the plate's wear: scratches, grime at the foot, a worn edge
    inset = 14.0
    for (x, y) in ((inset, inset), (W - inset, inset), (W - inset, H - inset), (inset, H - inset)):
        w_ = B.win(x - 8, y - 8, x + 8, y + 8)
        al = fp.disc_alpha(w_, x, y, 4.2, H=B.H)
        B.paint(w_, al, np.array([150.0, 140.0, 110.0]), rough=0.35, metal=1.0, height=0.2)
        slot = fp.rect_alpha(w_, x - 3, y - 0.6, x + 3, y + 0.6, H=B.H)
        B.paint(w_, slot * al, np.array([50.0, 46.0, 40.0]), height=-0.3)
    r = B.rng("scratch")
    for i in range(int(r.integers(10, 18))):
        x0, y0 = r.uniform(10, W - 10), r.uniform(10, H - 10)
        ln = r.uniform(12, 60)
        ang = r.normal(0.1, 0.5)
        pts = [(x0, y0), (x0 + ln * math.cos(ang), y0 + ln * math.sin(ang))]
        wn = B.win(min(p[0] for p in pts) - 2, min(p[1] for p in pts) - 2, max(p[0] for p in pts) + 2, max(p[1] for p in pts) + 2)
        al = fp.poly_alpha(wn, pts, 0.7, H=B.H)
        B.paint(wn, al * r.uniform(0.25, 0.5), np.array([120.0, 118.0, 112.0]), rough=0.5)
    _grime_edge(B, 0.05)
    return S, dict(size_mm=[W, H], lines=lines, blocks=blocks, cap_mm=cap, cap_mm_target=cap_t, available_mm=round(avail, 1), widest_at_target_cap_mm=round(widest, 1),
                   kind="engraved black laminate plate with white core, bevelled edge, four screws")


def render_hours_card(T, shop_id, cast, seed):
    """the caff's hours: a card written in marker pen and stuck inside the door glass with Sellotape: '6.30 AM - 10 PM' and '8 AM - 12 NOON'"""
    W, H = 300, 190
    S = Small(T, f"hours_{shop_id}", W, H, seed)
    B = S.B
    card = np.array([236.0, 231.0, 214.0])
    S.fill(card, 0.7, 0.0, amp=0.9, grain=False)
    win = (0, H, 0, W)
    # sun-yellowed at the edges, a fold line, a curl at the top corners
    rows = np.arange(H, dtype=np.float32)[:, None]
    cols = np.arange(W, dtype=np.float32)[None, :]
    edge = np.minimum(np.minimum(rows, H - rows), np.minimum(cols, W - cols))
    yel = np.clip(1.0 - edge / 40.0, 0, 1) * 0.5
    B.rgb[..., 2] *= (1.0 - 0.10 * yel)
    B.rgb[..., 1] *= (1.0 - 0.025 * yel)
    lines = hours_lines(shop_id, cast, ampm=True)
    cap_t = 24.0
    avail = W - 2 * 12.0
    widest = max(ink_width(T, ln, "patrick-hand", 400, cap_t, 0.04) for ln in lines)
    cap = cap_t if widest <= avail else math.floor(cap_t * avail / widest * 2) / 2.0
    pitch = cap * 2.0
    top_y = H / 2.0 + (len(lines) * pitch - (pitch - cap)) / 2.0 - cap
    r = B.rng("marker")
    blocks = []
    ink = np.array([24.0, 28.0, 52.0])
    for i, ln in enumerate(lines):
        base = int(round(top_y - i * pitch))
        b = make_block(T, ln, "patrick-hand", 400, cap, 0.04, base, W / 2.0, "centre", "sign_black", technique="painted", bid=f"line{i + 1}", role="hours", face_rgb=[24, 28, 52])
        a_m, binfo = fb.brush_text(T, ln, "patrick-hand", cap, W, H, base, W / 2.0, r, weight=400, tracking_em=0.04, whitewash_alpha=0.96, monoline=True, slant=0.04)
        # marker ink soaks a little into the card: a soft bleed round the line, a darker core
        bleed = ndi.gaussian_filter(a_m, 0.9)
        B.rgb += (ink[None, None, :] - B.rgb) * np.clip(a_m * 0.94 + 0.12 * bleed, 0, 1)[..., None]
        blocks.append(b)
    # Sellotape strips at the two top corners: a pale translucent band across the corner, a yellowed rim
    for (cx, cy, sgn) in ((18, H - 8, 1), (W - 18, H - 8, -1)):
        wn = B.win(cx - 28, cy - 14, cx + 28, cy + 14)
        al = fp.rect_alpha(wn, cx - 24, cy - 7, cx + 24, cy + 7, H=B.H)
        n = fc.fnoise(al.shape, 6, 4, r)
        B.paint(wn, al * 0.55, np.array([205.0, 196.0, 160.0]) * (1.0 + 0.03 * n[..., None]), rough=0.2, height=0.15)
    _grime_edge(B, 0.03)
    return S, dict(size_mm=[W, H], lines=lines, blocks=blocks, cap_mm=cap, cap_mm_target=cap_t, available_mm=round(avail, 1), widest_at_target_cap_mm=round(widest, 1),
                   kind="a card written in marker pen, taped inside the door glass")
