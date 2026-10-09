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
               technique="painted", hand=False, W=None, H=None, bid="b", role="name", face_rgb=None, figure=False):
    """a block dict like the target's, for text that is not on a fascia board: the layout numbers are computed the way make_target.py does"""
    cr = fc.cap_ratio(T, font_key, weight)
    if figure:
        cr = figure_ratio(T, font_key, weight, text)
    px = cap_mm / cr
    f = fc.font_for(T, font_key, weight, px)
    trk = tracking_em * px
    xs = fc.glyph_origins(f, text, trk)
    # ink extent from the pixels of a clean render
    pad = int(px) + 12
    Wd = int(xs[-1] + f.getlength(text[-1]) + 2 * pad)
    Hd = int(px * 1.8) + 2 * pad
    base = pad + int(px * 1.25)
    img = Image.new("L", (Wd, Hd), 0)
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(text):
        if ch != " ":
            d.text((pad + xs[i], base), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
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
             size_px_per_em=px, origin_x_mm=origin, width_mm=w,
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
        kinds = (("streak", 0.38), ("grain", 0.4), ("blot", 0.65), ("iso", 0.3), ("fine", 0.22)) if grain else (("blot", 0.6), ("iso", 0.4), ("fine", 0.25))
        B.rgb[:] = B.mottle(win, rgb, amp, kinds=kinds)
        B.rough[:] = np.clip(rough + B.noise("blot") * 0.025, 0.02, 1)
        B.metal[:] = metal
        B.height[:] = 0.0


def _grime_edge(B, k=0.05):
    rows = np.arange(B.H, dtype=np.float32)
    prof = np.exp(-(B.H - 1 - rows) / 40.0) + 0.7 * np.exp(-rows / 25.0)
    prof -= prof.mean()
    B.rgb += (np.array([88.0, 82.0, 74.0], np.float32) - B.rgb) * (k * prof)[:, None, None]


# ------------------------------------------------------------------ hanging signs
SIGN_FACE_MARGIN = 28.0


def ink_width(T, text, font_key, weight, cap_mm, tracking_em):
    b = make_block(T, text, font_key, weight, cap_mm, tracking_em, 100, 1000, "centre", "sign_black")
    return b["width_mm"]


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
    text = fcs["text"]
    fk, wt = fcs["font"], fcs["weight"] or 400
    cap_t = fcs["cap_mm"]
    trk = fcs["tracking_em"]
    if sid == "steam_laundry_box":
        frame = 20.0
        paint_rect = lambda col, rough, metal, inset: None
        bronze = fc.pal(T, "bronze_anodised")
        white = fc.pal(T, "acrylic_white")
        S.fill(bronze, 0.35, 1.0, amp=1.0)
        win = (0, H, 0, W)
        a = fp.rect_alpha(win, frame, frame, W - frame, H - frame, H=B.H)
        B.paint(win, a, B.mottle(win, white, 0.9, kinds=(("blot", 0.6), ("iso", 0.4), ("fine", 0.3))), rough=0.35, metal=0.0)
        avail = W - 2 * frame - 2 * SIGN_FACE_MARGIN
        inner = [frame, frame, W - frame, H - frame]
        border_inset = frame
        colour_name = fcs["colour"]
        shade = None
        technique = "vinyl"
        hand = False
        light = True
    elif sid == "ironmonger_hanging_board":
        S.fill(fc.pal(T, "buff_board"), 0.55, 0.0, amp=1.5)
        win = (0, H, 0, W)
        inset, rule = 20.0, 6.0
        pts = [[inset, inset], [W - inset, inset], [W - inset, H - inset], [inset, H - inset], [inset, inset]]
        a = fp.poly_alpha(win, pts, rule, H=B.H)
        B.paint(win, a, B.mottle(win, fc.pal(T, "sign_black"), 1.0, kinds=(("blot", 0.7), ("fine", 0.3))), rough=0.45, metal=0.0, height=0.20)
        avail = W - 2 * (inset + rule) - 2 * SIGN_FACE_MARGIN
        technique, hand, light = "painted", True, True
        border_inset = inset + rule
    else:                                                   # chandler
        S.fill(fc.pal(T, "navy"), 0.5, 0.0, amp=1.4)
        win = (0, H, 0, W)
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
        base = B.mottle(win, fc.pal(T, "hemp"), 1.4, kinds=(("fine", 0.6), ("blot", 0.4)))
        B.paint(win, a, np.clip(base * (1.0 + 0.16 * pat[..., None]), 0, 255), rough=0.8, metal=0.0, height=0.15)
        avail = W - 2 * (inset + rope) - 2 * SIGN_FACE_MARGIN
        technique, hand, light = "painted", True, False
        border_inset = inset + rope
    # the word, fitted: the target's cap is kept if it fits, else the cap is reduced (judgement, see the module note)
    w_t = ink_width(T, text, fk, wt, cap_t, trk)
    cap = cap_t if w_t <= avail else math.floor(cap_t * avail / w_t * 2) / 2.0
    rec.update(cap_mm_target=cap_t, cap_mm_built=cap, ink_width_target_cap_mm=round(w_t, 1), available_mm=round(avail, 1))
    sh_cfg = fcs.get("shade")
    shade_d = round(sh_cfg["d_mm"] * cap / cap_t, 1) if sh_cfg else None
    base_y = H / 2.0 - (cap * 0.5)
    colour = fcs["colour"]
    b = make_block(T, text, fk, wt, cap, trk, int(round(base_y)), W / 2.0, "centre", colour, shade_d=shade_d,
                   shade_colour=(sh_cfg["colour"] if sh_cfg else "shade_black"), technique=technique, hand=hand, bid="face", W=W, H=H)
    # the block's windows are clipped to the face's own size
    drawn = fp.paint_block(B, b, ground_rough=0.45 if hand else 0.35)
    rec["block"] = dict(string=text, font=fk, weight=wt, cap_mm=cap, tracking_em=trk, baseline_mm=int(round(base_y)), centre_x_mm=W / 2.0,
                        face=colour, shade=sh_cfg and dict(sh_cfg, d_mm=shade_d), ink_box_mm=[round(v, 1) for v in b["ink_box_mm"]],
                        origin_x_mm=round(b["origin_x_mm"], 2), cap_ratio=round(b["cap_ratio"], 4), size_px_per_em=round(b["size_px_per_em"], 3),
                        width_mm=round(b["width_mm"], 1), hand_jitter=hand, technique=technique)
    rec["b"] = b
    # wear: a grime film at the edges and a run or two; no gull on a sign that hangs over the door
    _grime_edge(B, 0.06)
    free = np.zeros((H, W), bool)
    free[10:-10, 10:-10] = True
    m = np.zeros((H, W), bool)
    x0, y0, x1, y1 = b["effects_box_mm"]
    m[max(0, H - int(y1) - 10):min(H, H - int(y0) + 10), max(0, int(x0) - 10):min(W, int(x1) + 10)] = True
    free &= ~m
    free &= ~ndi.binary_dilation(B.height > 0.1, iterations=3) if sid != "steam_laundry_box" else free
    if sid == "steam_laundry_box":
        free[:30, :] = False
        free[-30:, :] = False
        free[:, :30] = False
        free[:, -30:] = False
    runs, pl = fw.place_runs(B, free, 1 if sid == "steam_laundry_box" else 2, (30, 90), B.rng("runs"), light)
    fw.apply_runs(B, runs, light)
    B.layers["runs"] = runs
    rec["wear"] = dict(runs=len(pl))
    if sid == "steam_laundry_box":
        # lit from inside when the shop is open: face colour x 0.85; the bronze frame does not glow
        level = np.zeros((H, W), np.float32)
        level[int(frame):H - int(frame), int(frame):W - int(frame)] = 0.85
        B.emis = np.clip(B.rgb * level[..., None], 0, 255)
        rec["emissive"] = dict(level=0.85, face_mm=[frame, frame, W - frame, H - frame])
    return S, rec


# ------------------------------------------------------------------ the three gilt balls
def render_ball(T, k, seed):
    """a ball's equirectangular texture: 817 mm round (0.26 m x pi) by 409 mm pole to pole. Gilt paint over sheet metal, scuffed to the metal where hands reach"""
    W, H = 817, 409
    S = Small(T, f"ball_{k}", W, H, seed)
    B = S.B
    gold = fc.pal(T, "gold_leaf")
    S.fill(gold, 0.38, 0.8, amp=2.2, grain=False)
    r = B.rng("scuff")
    # scuffs to bright metal: more on the lower half and the side a hand reaches, long strokes round the ball
    n = fc.fnoise((H, W), 70.0, 2.6, r)
    v = np.arange(H, dtype=np.float32)[:, None] / H
    reach = 0.15 + 0.85 * np.clip((v - 0.35) / 0.4, 0, 1)
    a = np.clip((n - 0.9) * 1.6, 0, 1) * reach
    metal_rgb = np.array([158.0, 156.0, 148.0])
    B.rgb[:] = B.rgb + (metal_rgb[None, None, :] * (1.0 + 0.03 * B.noise("fine")[..., None]) - B.rgb) * a[..., None]
    B.rough[:] = B.rough + (0.42 - B.rough) * a
    B.metal[:] = B.metal + (1.0 - B.metal) * a
    B.height[:] -= 0.15 * a
    # the seam of two pressed halves: a fine groove at the equator, and a rain streak or two from the crown
    seam = np.exp(-((np.arange(H)[:, None] - H / 2.0) / 1.2) ** 2).astype(np.float32)
    B.rgb *= (1.0 - 0.28 * seam)[..., None]
    B.height += -0.2 * seam
    for i in range(int(r.integers(2, 4))):
        x = int(r.integers(30, W - 30))
        L = int(r.integers(80, 170))
        prof = np.exp(-((np.arange(-8, 9)) / 3.0) ** 2)
        for rr in range(L):
            fade = max(0.0, 1.0 - rr / L) ** 1.5
            cols = np.clip(x + np.arange(-8, 9), 0, W - 1)
            B.rgb[rr, cols] *= (1.0 - 0.22 * fade * prof)[:, None]
    _grime_edge(B, 0.03)
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


def render_glass_row(T, g, idx, seed):
    st = glass_style(g)
    fk = g["font"]
    wt = g["weight"] or 400
    cap = g["cap_mm"]
    text = g["text"]
    trk = 0.05 if st["kind"] != "vinyl" else 0.03
    figure = text.isdigit()
    probe = make_block(T, text, fk, wt, cap, trk, 100, 1000, "centre", "sign_black", figure=figure)
    w = probe["width_mm"]
    sd = st["shade"] or 0.0
    capb = cap
    W = int(math.ceil(w + sd + 2 * GLASS_PAD + 6))
    H = int(math.ceil(cap * 1.45 + sd + 2 * GLASS_PAD))
    base = int(GLASS_PAD + cap * 0.18 + sd)
    S = Small(T, f"glass_{idx}", W, H, seed)
    B = S.B
    B.rgb[:] = 0
    B.rough[:] = 0.5
    face_rgb = st.get("face_rgb")
    b = make_block(T, text, fk, wt, cap, trk, base, W / 2.0 - sd / 2.0, "centre", st["face"] or "whitewash", shade_d=sd or None,
                   shade_colour=st.get("shade_colour", "shade_black"), technique=("gilded" if st["kind"] == "gold" else ("vinyl" if st["kind"] == "vinyl" else "painted")),
                   hand=st["hand"], bid="glass", face_rgb=list(face_rgb) if face_rgb else None, figure=figure)
    # paint into an empty board: alpha is tracked separately
    A = np.zeros((H, W), np.float32)
    rng = B.rng("glass")
    face, sh, win = fp.text_layers(T, b, rng, hand=st["hand"], board_wh=(W, H))
    fcol = fp.block_rgb(T, b)
    amp = {"gold": 2.0, "whitewash": 3.0, "paint_red_shade": 1.2, "paint_flaking": 1.5, "vinyl": 0.4}[st["kind"]]
    fimg = B.mottle(win, fcol, amp, kinds=(("blot", 0.7), ("iso", 0.4), ("fine", 0.35)))
    r0, r1, c0, c1 = win
    fa = face.copy()
    if st["kind"] == "whitewash":
        # brush-laid whitewash: streaky, 85 per cent opaque, the edge ragged
        sn = fc.fnoise(fa.shape, 14.0, 1.8, rng)
        fa = np.clip(fa * np.clip(st["opacity"] + 0.07 * sn, 0.62, 1.0), 0, 1)
        fa = np.clip(fa * np.clip(1.0 + 0.12 * fc.fnoise(fa.shape, 1.2, 1.2, rng), 0.8, 1.1), 0, 1)
    elif st.get("flaking"):
        holes = fc.fnoise(fa.shape, 5.0, 3.0, rng)
        fa = fa * np.clip((holes + 2.2) * 0.9, 0, 1) ** 0.6
        fa = np.where(holes < -1.5, 0, fa)
    # rgb and alpha
    out_rgb = np.zeros((H, W, 3), np.float32)
    A_all = np.zeros((H, W), np.float32)
    if sh is not None:
        scol = fp.block_rgb(T, dict(face=b["shade"]["colour"], face_rgb=None))
        sa = np.clip(sh, 0, 1) * (1.0 - fa)
        out_rgb[r0:r1, c0:c1] = np.asarray(scol, np.float32)[None, None, :] * sa[..., None]
        A_all[r0:r1, c0:c1] = np.clip(sh, 0, 1)
    sub = out_rgb[r0:r1, c0:c1]
    A_sub = A_all[r0:r1, c0:c1]
    # straight (non-premultiplied) colour: face over shade
    comb_a = np.clip(fa + A_sub * (1.0 - fa), 0, 1)
    num = fimg * fa[..., None] + (np.asarray(fp.block_rgb(T, dict(face=b["shade"]["colour"], face_rgb=None)), np.float32)[None, None, :] if sh is not None else 0) * (A_sub * (1.0 - fa))[..., None]
    col = np.where(comb_a[..., None] > 1e-4, num / np.maximum(comb_a[..., None], 1e-4), fimg)
    B.rgb[r0:r1, c0:c1] = col
    A[r0:r1, c0:c1] = comb_a
    face_alpha = np.zeros((H, W), np.float32)
    face_alpha[r0:r1, c0:c1] = fa
    # roughness/metal: the leaf's own; shade is paint
    B.rough[:] = st["rough"]
    B.metal[:] = st["metal"]
    if st["kind"] == "gold":
        sh_only = np.zeros((H, W), np.float32)
        sh_only[r0:r1, c0:c1] = A_sub * (1.0 - fa)
        B.rough[:] = st["rough"] * (1 - sh_only) + 0.6 * sh_only
        B.metal[:] = st["metal"] * (1 - sh_only)
    rows = np.where((face_alpha > 0.5).any(axis=1))[0]
    cols = np.where((face_alpha > 0.5).any(axis=0))[0]
    rec = dict(size_mm=[W, H], style=st["kind"], figure_height_sized=figure, baseline_row_from_bottom_mm=base, face_alpha_ink_box_in_tile_mm=[int(cols.min()), int(H - (rows.max() + 1)), int(cols.max() + 1), int(H - rows.min())] if len(rows) else None,
               block=b, tracking_em=trk, cap_mm=cap)
    return S, A, face_alpha, rec


def render_window_wash(T, seed, W=3250, H=1800):
    """the empty unit's whole window whitewashed (ruled 3 Oct): brush arcs, nothing legible"""
    S = Small(T, "empty_window", W, H, seed)
    B = S.B
    r = B.rng("wash")
    k = 4
    img = Image.new("L", (W // k, H // k), 0)
    d = ImageDraw.Draw(img)
    for i in range(34):
        # a sweep of the brush: an arc of a big circle, round at both ends
        cx = r.uniform(-0.2, 1.2) * W / k
        cy = r.uniform(-0.2, 1.2) * H / k
        rad = r.uniform(420, 1100) / k
        th = r.uniform(130, 300) / k
        a0 = r.uniform(0, 360)
        span = r.uniform(60, 140)
        val = int(r.uniform(150, 255))
        d.arc([cx - rad, cy - rad, cx + rad, cy + rad], a0, a0 + span, fill=val, width=int(th))
        for ang in (a0, a0 + span):
            ex, ey = cx + rad * math.cos(math.radians(ang)), cy + rad * math.sin(math.radians(ang))
            d.ellipse([ex - th / 2, ey - th / 2, ex + th / 2, ey + th / 2], fill=val)
    a = np.asarray(img.resize((W, H), Image.BILINEAR), np.float32) / 255.0
    a = ndi.gaussian_filter(a, 14.0)
    streak = fc.fnoise((H, W), 70.0, 2.2, r)
    a = np.clip(0.52 + 0.42 * (a - 0.35) + 0.03 * streak + 0.05 * fc.fnoise((H, W), 45, 45, r), 0.22, 0.90)
    ww = fc.pal(T, "whitewash")
    B.rgb[:] = ww[None, None, :] * (1.0 + 0.02 * fc.fnoise((H, W), 30, 30, r)[..., None])
    B.rough[:] = 0.9
    B.metal[:] = 0.0
    B.height[:] = 0.1 * a
    return S, a


# ------------------------------------------------------------------ the letting board and the hours plates
def render_letting_board(T, seed):
    sp = [p for p in T["small_panels"] if p["id"] == "letting_board"][0]
    W, H = sp["size_mm"]
    S = Small(T, "letting_board", W, H, seed)
    B = S.B
    white = fc.pal(T, "white_paint")
    S.fill(white, 0.55, 0.0, amp=1.4)
    win = (0, H, 0, W)
    # a painted board: a plain edge, a faint inner line
    edge = 14.0
    a = fp.rect_alpha(win, 0, 0, W, H, H=B.H) - fp.rect_alpha(win, edge, edge, W - edge, H - edge, H=B.H)
    B.paint(win, np.clip(a, 0, 1), B.mottle(win, white * 0.92, 1.2, kinds=(("blot", 0.7), ("fine", 0.3))), rough=0.6)
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
    lower = [heads[2], heads[3]]
    rl = fw.place_rust(B, [(x, y - 7) for x, y in lower], [float(r.uniform(38, 52)) for _ in lower], r, True)
    fw.apply_rust(B, rl)
    B.layers["rust"] = rl
    runs_free = np.ones((H, W), bool)
    runs_free[:30, :] = False
    runs_free[-30:, :] = False
    runs_free[:, :30] = False
    runs_free[:, -30:] = False
    tb = b["effects_box_mm"]
    runs_free[max(0, H - int(tb[3]) - 14):min(H, H - int(tb[1]) + 14), max(0, int(tb[0]) - 14):min(W, int(tb[2]) + 14)] = False
    for (x, y) in heads:
        runs_free[max(0, H - int(y) - 30):min(H, H - int(y) + 70), max(0, int(x) - 25):min(W, int(x) + 25)] = False
    runs, pl = fw.place_runs(B, runs_free, 2, (40, 110), B.rng("runs"), True)
    fw.apply_runs(B, runs, True)
    _grime_edge(B, 0.05)
    return S, dict(size_mm=[W, H], block=b, screws=[[round(x, 1), round(y, 1)] for x, y in heads], rust_runs=2, askew_deg=2,
                   centre_on_fascia_mm=sp["centre_on_board_mm"], rust_layer=rl)


def hours_lines(shop_id, cast):
    """MON-SAT / WED / SUN lines from hook-cast.json's hours (the plates' own rule)"""
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
    sp = [p for p in T["small_panels"] if p["id"] == "hours_plate"][0]
    W, H = sp["size_mm"]
    S = Small(T, f"hours_{shop_id}", W, H, seed)
    B = S.B
    enamel = np.array([232.0, 229.0, 218.0])
    S.fill(enamel, 0.30, 0.0, amp=0.9, grain=False)
    win = (0, H, 0, W)
    blue = np.array([34.0, 64.0, 122.0])
    border, rolled = 4.0, 3.0
    inset = 6.0
    outer = fp.rect_alpha(win, inset, inset, W - inset, H - inset, H=B.H) - fp.rect_alpha(win, inset + border, inset + border, W - inset - border, H - inset - border, H=B.H)
    B.paint(win, np.clip(outer, 0, 1), B.mottle(win, blue, 1.0, kinds=(("blot", 0.7), ("fine", 0.3))), rough=0.28, height=0.05)
    # the rolled edge, in the height map: 3 mm
    cols = np.arange(W, dtype=np.float32) + 0.5
    rws = np.arange(H, dtype=np.float32) + 0.5
    d = np.minimum(np.minimum(cols[None, :], W - cols[None, :]), np.minimum(rws[:, None], H - rws[:, None]))
    B.height += (0.8 * np.clip(1.0 - np.abs(d - rolled / 2.0) / (rolled / 2.0), 0, 1)).astype(np.float32)
    lines = hours_lines(shop_id, cast)
    cap_t = sp["cap_mm"]
    avail = W - 2 * (inset + border) - 2 * 10.0
    widest = max(ink_width(T, ln, sp["font"], sp["weight"], cap_t, 0.02) for ln in lines)
    cap = cap_t if widest <= avail else math.floor(cap_t * avail / widest * 2) / 2.0           # JUDGEMENT: the target's 24 mm cap for the plate's longest line does not fit 300 mm
    pitch = cap * 1.7
    top_y = H / 2.0 + (len(lines) * pitch - (pitch - cap)) / 2.0 - cap
    blocks = []
    for i, ln in enumerate(lines):
        base = int(round(top_y - i * pitch))
        b = make_block(T, ln, sp["font"], sp["weight"], cap, 0.02, base, W / 2.0, "centre", "shade_black", technique="painted", bid=f"line{i + 1}", role="hours")
        fp.paint_block(B, b, ground_rough=0.30)
        blocks.append(b)
    # chips to black iron at the corners
    r = B.rng("chips")
    for (x, y) in ((inset + 2, inset + 2), (W - inset - 2, inset + 2), (W - inset - 2, H - inset - 2), (inset + 2, H - inset - 2)):
        if r.random() < 0.8:
            w_ = B.win(x - 9, y - 9, x + 9, y + 9)
            rad = r.uniform(2.5, 5.5)
            al = fp.disc_alpha(w_, x + r.uniform(-2, 2), y + r.uniform(-2, 2), rad, H=B.H)
            B.paint(w_, al, np.array([30.0, 28.0, 28.0]), rough=0.7, height=-0.3)
            rim = fp.disc_alpha(w_, x, y, rad + 1.8, H=B.H) - al
            B.paint(w_, np.clip(rim, 0, 1) * 0.6, np.array([110.0, 72.0, 44.0]), rough=0.8)
    _grime_edge(B, 0.04)
    return S, dict(size_mm=[W, H], lines=lines, blocks=blocks, cap_mm=cap, cap_mm_target=cap_t, available_mm=round(avail, 1), widest_at_target_cap_mm=round(widest, 1))
