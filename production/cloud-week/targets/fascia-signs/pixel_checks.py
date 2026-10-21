"""Reference implementations of the checks that READ THE RENDERED PIXELS of a fascia texture.

Cloud week 42, written 8 October 2026 after the target review (fault 3: the old checks read only the
renderer's own manifest, so a mirrored board, a block at the wrong end or a wrong font passed them all).
Unit 4.1 may import this file or copy it. It reads target.json and the OFL font files; nothing else.

    from pixel_checks import load_target, check_board, synthetic_board
    T = load_target()
    img = <the rendered base-colour image, H x W x 3 uint8, 1 px per mm, row 0 = the TOP of the board>
    results = check_board(img, T, "ritas", fonts_dir)       # a list of dicts: id, ok, value, note

The checks it implements (target.json 'checks' ids in brackets):
  pos      [{shop}.{block}.pos]    the ink box of the block's face colour, READ ON THE PIXELS, against its anchor and baseline
  mask     [G10, {block}.mask]     the block's string re-rendered from its FONT FILE against the face mask, and against the
                                   mask flipped about the block's centre line: a mirrored board, a wrong font or a wrong word fails
  mirror   [G18]                   an off-centre block that matches W - x better than x
  width    [{block}.width]         pixel ink width
  face     [{block}.face]          median colour of the eroded face mask
  jitter   [G12, {block}.jitter]   the SD of the glyphs' bottom edges about a straight baseline
Y is UP in target.json (mm from the board's bottom); in the image row 0 is the top, so row = H - 1 - y.
"""
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
W_MM, H_MM = 5410, 550


def load_target(path=None):
    return json.loads(Path(path or HERE / "target.json").read_text(encoding="utf-8"))


# ------------------------------------------------------------------ colour
def _lin(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_WP = np.array([0.95047, 1.0, 1.08883])


def lab(rgb):
    rgb = np.asarray(rgb, float)
    xyz = (_lin(rgb) @ _M.T) / _WP
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def dE(a, b):
    return np.linalg.norm(lab(a) - lab(b), axis=-1)


# ------------------------------------------------------------------ fonts
_cache = {}


def font_for(T, key, weight, px, fonts_dir):
    k = (key, weight, round(px, 2))
    if k in _cache:
        return _cache[k]
    row = T["fonts"][key]
    rel = row["file_in_google_fonts_repo"].split("/", 1)[1]            # '<dir>/<file>'
    f = ImageFont.truetype(os.path.join(str(fonts_dir), rel), px, layout_engine=ImageFont.Layout.RAQM)
    axes = row.get("axes")
    if axes:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            v = axes.get(n, a["default"])
            if v is None:
                v = weight
            vals.append(min(max(v, a["minimum"]), a["maximum"]))
        f.set_variation_by_axes(vals)
    _cache[k] = f
    return f


def glyph_origins(font, text, tracking_px):
    """pen x of every glyph (kerning from the font, tracking added between glyphs)"""
    xs = []
    for i, ch in enumerate(text):
        xs.append(font.getlength(text[:i + 1]) - font.getlength(ch) + i * tracking_px)
    return xs


def render_block_mask(T, b, fonts_dir, jitter_sd_mm=0.0, rng=None, dx_mm=0.0, flip=False, shade=False):
    """boolean mask (H x W, row 0 = top) of the block's string re-rendered from its font file at its target place.
    flip=True mirrors the string about the vertical centre line of its ink box (a mirrored board's block)."""
    cap = b["cap_mm"]
    px = cap / b["cap_ratio"]
    f = font_for(T, b["font"], b["weight"], px, fonts_dir)
    trk = b["tracking_em"] * px
    xs = glyph_origins(f, b["text"], trk)
    img = Image.new("L", (W_MM, H_MM), 0)
    d = ImageDraw.Draw(img)
    oy = H_MM - 1 - b["baseline_mm"]
    for i, ch in enumerate(b["text"]):
        if ch == " ":
            continue
        dy = 0.0
        if jitter_sd_mm and rng is not None:
            dy = float(np.clip(rng.normal(0, jitter_sd_mm), -1.6, 1.6))
        d.text((b["origin_x_mm"] + xs[i] + dx_mm, oy - dy), ch, font=f, fill=255, anchor="ls")
    m = np.asarray(img) > 127
    if shade and b.get("shade"):
        s = b["shade"]["d_mm"]
        out = m.copy()
        for k in np.arange(0.5, s + 0.01, 0.5):
            out |= np.roll(np.roll(m, int(round(k)), axis=0), int(round(k)), axis=1)      # down and right
        m = out
    if flip:
        x0, _, x1, _ = b["ink_box_mm"]
        c = (x0 + x1) / 2.0
        mm = np.zeros_like(m)
        cols = np.where(m.any(axis=0))[0]
        for col in cols:
            nc = int(round(2 * c - col))
            if 0 <= nc < W_MM:
                mm[:, nc] |= m[:, col]
        m = mm
    return m


def block_region(b, margin=8, xmargin=None):
    """the part of the board where this block's pixels live: its effects box (shade, outline, hand jitter) dilated by 8 mm
    (hand jitter is at most 1.6 mm), and inside its panel if it sits in one; neighbouring lines are 14 mm or more apart so they do not share it.
    The POSITION read uses xmargin=40: the box is widened 40 mm along the line (not up or down) so a block that is 60 mm out is still seen out"""
    x0, y0, x1, y1 = b["effects_box_mm"]
    xm = margin if xmargin is None else xmargin
    x0, y0, x1, y1 = x0 - xm, y0 - margin, x1 + xm, y1 + margin
    if b.get("region_mm"):
        rx0, ry0, rx1, ry1 = b["region_mm"]
        x0, y0, x1, y1 = max(x0, rx0), max(y0, ry0), min(x1, rx1), min(y1, ry1)
    return [int(max(0, x0)), int(max(0, y0)), int(min(W_MM, x1)), int(min(H_MM, y1))]


def to_rows(y0, y1):
    return H_MM - y1, H_MM - y0


def face_mask(img, b, tol=14.0, xmargin=None):
    """pixels of the block's face colour inside its region, from the PIXELS"""
    x0, y0, x1, y1 = block_region(b, xmargin=xmargin)
    r0, r1 = to_rows(y0, y1)
    patch = img[r0:r1, x0:x1].astype(float)
    m_face = dE(patch, np.array(b["face_1990"], float)) <= tol
    m_gnd = dE(patch, np.array(b["ground_1990"], float)) < dE(patch, np.array(b["face_1990"], float))
    m = m_face & ~m_gnd
    full = np.zeros((H_MM, W_MM), bool)
    full[r0:r1, x0:x1] = m
    return full


def ink_bbox_mm(mask):
    rows = np.where(mask.any(axis=1))[0]
    cols = np.where(mask.any(axis=0))[0]
    if rows.size == 0:
        return None
    return [float(cols.min()), float(H_MM - 1 - rows.max()), float(cols.max() + 1), float(H_MM - rows.min())]


def tolerant_f(true_m, pix_m, tol_mm):
    """mean of recall and precision with a dilation of tol_mm: a jittered hand-painted block still passes"""
    k = max(1, int(round(tol_mm)))
    st = ndi.generate_binary_structure(2, 2)
    dp = ndi.binary_dilation(pix_m, st, iterations=k)
    dt = ndi.binary_dilation(true_m, st, iterations=k)
    if not true_m.any() or not pix_m.any():
        return 0.0
    recall = (true_m & dp).sum() / true_m.sum()
    precision = (pix_m & dt).sum() / pix_m.sum()
    return float((recall + precision) / 2.0)


def glyph_bottoms(mask, bbox_rows=None):
    """bottom row of each connected glyph whose bottom is flat (>= 35 per cent of its width in its last two rows)"""
    lbl, n = ndi.label(mask)
    out = []
    for i, sl in enumerate(ndi.find_objects(lbl), 1):
        h = sl[0].stop - sl[0].start
        w = sl[1].stop - sl[1].start
        if h < 10 or w < 4:
            continue
        comp = (lbl[sl] == i)
        last = comp[-2:].any(axis=0).sum()
        if last >= 0.35 * w:
            out.append((float(sl[0].stop), float((sl[1].start + sl[1].stop) / 2.0)))
    return out


def jitter_sd_mm(mask):
    g = glyph_bottoms(mask)
    if len(g) < 6:
        return None
    ys = np.array([p[0] for p in g])
    xs = np.array([p[1] for p in g])
    keep = np.abs(ys - np.median(ys)) <= 4.5           # drops an apostrophe or a comma, whose 'bottom' is not on the baseline
    ys, xs = ys[keep], xs[keep]
    if len(ys) < 6:
        return None
    A = np.vstack([xs, np.ones_like(xs)]).T
    co, *_ = np.linalg.lstsq(A, ys, rcond=None)
    return float(np.std(ys - A @ co))


# ------------------------------------------------------------------ the checks on one board
def check_board(img, T, shop_id, fonts_dir, jitter=False):
    """run the pixel checks for one shop's texture; returns a list of dicts"""
    s = [x for x in T["shops"] if x["id"] == shop_id][0]
    out = []
    for b in s["blocks"]:
        if b["ghost"] or not b["in_texture"]:
            continue
        pm = face_mask(img, b)
        pmx = face_mask(img, b, xmargin=40)                  # the position and the width: the box widened 40 mm along the line
        bb = ink_bbox_mm(pmx)
        bid = f"{shop_id}.{b['id']}"
        if bb is None:
            out.append(dict(id=bid + ".pos", ok=False, value=None, note="no pixels of the face colour found"))
            out.append(dict(id=bid + ".mask", ok=False, value=0.0, note="no pixels"))
            continue
        x0, y0, x1, y1 = b["ink_box_mm"]
        if b["anchor"] == "centre":
            got, want = (bb[0] + bb[2]) / 2.0, (x0 + x1) / 2.0
        elif b["anchor"] == "left":
            got, want = bb[0], x0
        else:
            got, want = bb[2], x1
        # baseline from the flat bottoms (or the box bottom)
        gb = glyph_bottoms(pm)
        base_got = float(H_MM - np.median([p[0] for p in gb])) if gb else bb[1]
        out.append(dict(id=bid + ".pos", ok=abs(got - want) <= 15 and abs(base_got - b["baseline_mm"]) <= 3.0, value=dict(x_mm=round(got, 1), want=round(want, 1), baseline_mm=round(base_got, 1)), note="ink box read on the pixels"))
        w_ = bb[2] - bb[0]
        out.append(dict(id=bid + ".width", ok=abs(w_ - b["width_mm"]) <= max(6.0, 0.04 * b["width_mm"]) + (2 * b["embolden_mm"] if b.get("embolden_mm") else 0), value=round(w_, 1), note=f"want {b['width_mm']}"))
        tm = render_block_mask(T, b, fonts_dir)
        tol = 2.5 if b.get("jitter") else 1.0
        f_true = tolerant_f(tm, pm, tol)
        fm = render_block_mask(T, b, fonts_dir, flip=True)
        f_flip = tolerant_f(fm, pm, tol)
        sym = b["text"] in (T["common_style"].get("symmetric_strings") or [])
        out.append(dict(id=bid + ".mask", ok=(f_true >= 0.90 and (sym or f_true - f_flip >= 0.15)), value=dict(true=round(f_true, 3), flipped=round(f_flip, 3)), note="G10: re-rendered from the font file"))
        er = ndi.binary_erosion(pm, iterations=2)
        med = np.median(img[er], axis=0) if er.any() else None
        if med is not None:
            out.append(dict(id=bid + ".face", ok=float(dE(med, np.array(b["face_1990"], float))) <= 14.0, value=[int(v) for v in med], note="median of the eroded face mask"))
        sd = jitter_sd_mm(pm)
        if b.get("jitter") and sd is not None:
            lo, hi = T["common_style"]["hand_jitter"]["baseline_sd_mm"]
            out.append(dict(id=bid + ".jitter", ok=(lo <= sd <= hi) if jitter else sd <= T["common_style"]["hand_jitter"]["other_sd_mm"][1], value=round(sd, 2), note="G12: SD of flat glyph bottoms" + ("" if jitter else " (an unjittered reference render: expect <= 0.6, the pixel grid alone gives 0.3 to 0.5)")))
    # G18: an off-centre anchor-centre block that sits at W - x
    for b in s["blocks"]:
        if b["ghost"] or not b["in_texture"] or b["anchor"] != "centre" or abs(b["x_mm"] - W_MM / 2) < 200:
            continue
        pm = face_mask(img, b)
        bb = ink_bbox_mm(pm)
        c_true = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0
        if bb is None:
            out.append(dict(id=f"{shop_id}.{b['id']}.mirror", ok=False, value=None, note="no pixels"))
            continue
        got = (bb[0] + bb[2]) / 2.0
        out.append(dict(id=f"{shop_id}.{b['id']}.mirror", ok=abs(got - c_true) < abs(got - (W_MM - c_true)), value=dict(got=round(got, 1), x=round(c_true, 1), mirrored_x=round(W_MM - c_true, 1)), note="G18"))
    return out


# ------------------------------------------------------------------ a reference render, to test the checks themselves
def _col(T, key_or_rgb):
    if isinstance(key_or_rgb, (list, tuple)):
        return tuple(int(v) for v in key_or_rgb)
    return tuple(T["palette"][key_or_rgb]["srgb_1990"])


def synthetic_board(T, shop_id, fonts_dir, jitter_sd=0.0, seed=1, mirror=False, shift_mm=0.0, wrong_font=None):
    """a crude but honest render of one board from target.json alone: ground, shapes, then every in-texture block
    (block shade, then face). Not a look: a test object for the pixel checks. Row 0 = the top of the board."""
    s = [x for x in T["shops"] if x["id"] == shop_id][0]
    g = _col(T, s["ground"]["colour"])
    img = Image.new("RGB", (W_MM, H_MM), g)
    d = ImageDraw.Draw(img)

    def R(box):
        x0, y0, x1, y1 = box
        return [x0, H_MM - y1, x1 - 1, H_MM - y0 - 1]
    for sh in s["shapes"]:
        c = _col(T, sh["colour"])
        if sh["kind"] == "rect":
            d.rectangle(R(sh["box"]), fill=c)
        elif sh["kind"] == "polyline":
            d.line([(p[0], H_MM - p[1]) for p in sh["pts"]], fill=c, width=max(1, int(round(sh["width_mm"]))), joint="curve")
        elif sh["kind"] == "circle":
            cx, cy = sh["c"]
            r = sh["r"]
            d.ellipse([cx - r, H_MM - cy - r, cx + r, H_MM - cy + r], outline=c, width=3)
    rng = np.random.default_rng(seed)
    arr = np.asarray(img).copy()
    for b in s["blocks"]:
        if b["ghost"] or not b["in_texture"]:
            continue
        bb = dict(b)
        if wrong_font and b["id"] == wrong_font[0]:
            bb["font"] = wrong_font[1]
        m = render_block_mask(T, bb, fonts_dir, jitter_sd_mm=(jitter_sd if b.get("jitter") else 0.0), rng=rng, dx_mm=shift_mm, shade=True)
        if b.get("shade"):
            face_only = render_block_mask(T, bb, fonts_dir, jitter_sd_mm=(jitter_sd if b.get("jitter") else 0.0), rng=np.random.default_rng(seed), dx_mm=shift_mm)
            arr[m & ~face_only] = _col(T, b["shade"]["colour"])
            arr[face_only] = _col(T, b["face_rgb"] if b.get("face_rgb") else b["face"])
        else:
            arr[m] = _col(T, b["face_rgb"] if b.get("face_rgb") else b["face"])
    if mirror:
        arr = arr[:, ::-1].copy()
    return arr


if __name__ == "__main__":
    import sys
    T = load_target()
    fd = sys.argv[1] if len(sys.argv) > 1 else "fonts"
    sid = sys.argv[2] if len(sys.argv) > 2 else "ritas"
    img = synthetic_board(T, sid, fd)
    for r in check_board(img, T, sid, fd):
        print(r)
