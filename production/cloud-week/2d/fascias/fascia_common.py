"""Shared by make_fascias.py and check_fascias.py (unit 4.1, cloud week 42, 9 October 2026).

Three things live here and nowhere else:

  1. THE AMENDMENTS. production/cloud-week/targets/fascia-signs/ is not edited (the brief). The two narrow faults of its
     second review (TARGET-REVIEW.md, "Re-review (try 2)", applied by DECISIONS 9 Oct) are applied here, on a copy of
     target.json loaded in memory, and every one of them is written into the manifest and NOTES.md:
       A1  the hand jitter is drawn at a fixed baseline SD of 1.0 mm (each glyph clipped at +-1.6 mm) and judged PER BOARD,
           the flat-bottomed glyphs of all its painted and gilded blocks pooled: accept 0.45 to 2.0 mm; vinyl, applied and
           glass blocks pooled: at most 0.6 mm
       A2  advance jitter does not accumulate: each glyph's pen is off by at most 1.5 per cent of ITS OWN advance
       A3  glyph-mask tolerance (G10) 3.5 mm for hand-painted letters (was 2.5), 1 mm for vinyl, applied, glass
       A4  a string with no flat-bottomed glyph is compared by its pixel ink bottom against ink_box_mm[1], +-3 mm
       A5  Tea Rooms is sized by its H like every other block: cap_mm 200 means the H (the T then measures 204.8 mm)
       A6  the grocer's number "11" goes on the SHOP door's fanlight (the grocer has no side door), at the shop door's own
           street x, 38.147; the target's glass spec allows it (a fanlight of the kit's shop door: z 2.131 to 2.400,
           x +-0.453 about the door; "11" stands at z 2.18, cap 110, so 2.18 to 2.29)
  2. THE FONTS. One resolver from (font key, weight) to a file under production/fonts/ (in git), so the renderer and the
     checks use exactly the same outlines. No network is needed to rebuild.
  3. SMALL TOOLS: colour maths (the same sRGB / Lab D65 / WCAG formulas as the target), seeded noise, board geometry.
"""
import copy
import hashlib
import json
import os
from pathlib import Path

import numpy as np
from PIL import Image, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]                                            # the repository root
TARGET_DIR = ROOT / "production" / "cloud-week" / "targets" / "fascia-signs"
TARGET_JSON = TARGET_DIR / "target.json"
FONTS_DIR = ROOT / "production" / "fonts"
HOOK_CAST = ROOT / "production" / "specs" / "hook-cast.json"
W_MM, H_MM = 5410, 550                                           # the board, one pixel a millimetre
SCRIPT_VERSION = "fascias-v1"


# ------------------------------------------------------------------ the target, amended in memory
def load_target(path=None, amend=True):
    T = json.loads(Path(path or TARGET_JSON).read_text(encoding="utf-8"))
    if amend:
        apply_amendments(T)
    return T


AMENDMENT_TEXT = [
    "A1 hand jitter drawn at baseline SD 1.0 mm, each glyph clipped at +-1.6 mm; judged per board, painted and gilded flat-bottomed glyphs pooled, accepted 0.45 to 2.0 mm; vinyl, applied and glass blocks pooled at most 0.6 mm",
    "A2 advance jitter does not accumulate: each glyph's pen is off by at most 1.5 per cent of its own advance from its true pen position",
    "A3 glyph-mask tolerance 3.5 mm for hand-painted (painted and gilded) letters, 1 mm for vinyl, applied and glass",
    "A4 for a string with no flat-bottomed glyph the pixel ink bottom is compared with ink_box_mm[1], +-3 mm, not with the baseline",
    "A5 Tea Rooms is sized by its H like every other block: 285.31 px an em, cap_mm 200 meaning the H-height (the T then measures 204.8 mm)",
    "A6 the grocer's street number 11 stands on the shop door's fanlight (the grocer has no side door), centred on the shop door's own street x, 38.147 (bay 33 to 39, door at the high end, kit pilaster 0.35 + shop door 1.006 / 2), cap 110, z 2.18 (the fanlight glass is z 2.131 to 2.400)",
]


def apply_amendments(T):
    hj = T["common_style"]["hand_jitter"]
    hj["baseline_sd_mm"] = [1.0, 1.0]
    hj["baseline_clip_mm"] = 1.6
    hj["advance_accumulates"] = False
    hj["advance_note"] = "each glyph's pen is off by at most advance_pct of its own advance from its true pen position (not a running sum)"
    hj["judged"] = "per board, the flat-bottomed glyphs of all its painted and gilded blocks pooled"
    hj["pooled_sd_mm"] = [0.45, 2.0]
    hj["other_pooled_max_mm"] = 0.6
    for s in T["shops"]:
        for b in s["blocks"]:
            if b.get("jitter"):
                b["jitter"] = copy.deepcopy(hj)
    for c in T["checks"]:
        if c["id"] == "G10":
            c["expected"]["tolerance_mm"] = {"painted_gilded": 3.5, "vinyl_applied_glass": 1.0}
            c["measure"] = c["measure"].replace("2.5 mm", "3.5 mm")
        elif c["id"] == "G12":
            c["expected"] = {"painted_gilded_pooled_sd_mm": [0.45, 2.0], "vinyl_applied_glass_pooled_sd_max_mm": 0.6, "drawn_sd_mm": 1.0, "clip_mm": 1.6}
            c["measure"] = ("per BOARD, the residuals of every flat-bottomed glyph's bottom edge from its block's straight baseline, pooled over the board's "
                            "painted and gilded blocks (vinyl, applied and glass blocks pooled separately)")
        elif c["id"].endswith(".jitter"):
            c["expected"] = {"board_pooled_sd_mm": [0.45, 2.0]}
            c["method"] = "G12, judged per board (amendment A1)"
        elif c["id"].endswith(".pos"):
            c["method"] = c["method"] + " [A4: a string with no flat-bottomed glyph is compared by its pixel ink bottom with ink_box_mm[1], +-3 mm]"
        elif c["id"] == "tea_rooms.name.cap":
            c["measure"] = "H-height 200 mm (the T then measures 204.8 mm): the H-shaped capital in the layers manifest, confirmed on the pixels"
        elif c["id"] == "grocer.glass.15":
            c["expected"]["x_street_m"] = 38.147
            c["name"] = "grocer: glass '11' (shop-door fanlight)"
    for g in T["glass_lettering"]:
        if g["shop"] == "grocer" and g["text"] == "11":
            g["x_street_m"] = 38.147
            g["surface"] = "shop-door fanlight (the grocer has no side door: BAY_WITHOUT_SIDE_DOOR = 5)"
    for s in T["shops"]:
        if s["id"] == "grocer":
            s["fanlight_street_x_m"] = 38.147
            s["fanlight_note"] = "the SHOP door's fanlight (amendment A6): the grocer has no side door"
    T["_amendments"] = AMENDMENT_TEXT
    return T


# ------------------------------------------------------------------ colour (the target's own formulas)
def s2l(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(l):
    l = np.clip(np.asarray(l, float), 0, 1)
    return np.where(l <= 0.0031308, 12.92 * l, 1.055 * np.power(l, 1 / 2.4) - 0.055) * 255.0


_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_WP = np.array([0.95047, 1.0, 1.08883])


def lab(rgb):
    rgb = np.asarray(rgb, float)
    xyz = (s2l(rgb) @ _M.T) / _WP
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.stack([116 * f[..., 1] - 16, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])], -1)


def unlab(L):
    L = np.asarray(L, float)
    fy = (L[..., 0] + 16) / 116
    fx = fy + L[..., 1] / 500
    fz = fy - L[..., 2] / 200
    f = np.stack([fx, fy, fz], -1)
    xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * _WP
    lin = xyz @ np.linalg.inv(_M).T
    return l2s(lin)


def dE(a, b):
    return np.linalg.norm(lab(a) - lab(b), axis=-1)


def rel_lum(rgb):
    l = s2l(rgb)
    return 0.2126 * l[..., 0] + 0.7152 * l[..., 1] + 0.0722 * l[..., 2]


def contrast(a, b):
    la, lb = float(rel_lum(np.asarray(a, float))), float(rel_lum(np.asarray(b, float)))
    hi, lo = max(la, lb), min(la, lb)
    return (hi + 0.05) / (lo + 0.05)


def pal(T, key, which="srgb_1990"):
    return np.array(T["palette"][key][which], float)


# ------------------------------------------------------------------ fonts
FONT_FILES = {
    "marcellus-sc": "marcellus-sc/MarcellusSC-Regular.ttf",
    "abril-fatface": "abril-fatface/AbrilFatface-Regular.ttf",
    "old-standard-tt-bold": "old-standard-tt/OldStandard-Bold.ttf",
    "oswald": "oswald/Oswald[wght].ttf",
    "jost": "jost/Jost[wght].ttf",
    "libre-franklin": "libre-franklin/LibreFranklin[wght].ttf",
    "fraunces": "fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf",
    "alfa-slab-one": "alfa-slab-one/AlfaSlabOne-Regular.ttf",
    "josefin-sans": "josefin-sans/JosefinSans[wght].ttf",
    "patrick-hand": "patrick-hand/PatrickHand-Regular.ttf",
}
# evening-paper's Libre Franklin statics are REUSED (not duplicated) for the weights they hold; 900 comes from the variable file.
LIBRE_FRANKLIN_STATIC = {700: "evening-paper/LibreFranklin-700.ttf", 800: "evening-paper/LibreFranklin-800.ttf"}
_fcache = {}


def font_file(key, weight):
    if key == "libre-franklin" and weight in LIBRE_FRANKLIN_STATIC:
        return FONTS_DIR / LIBRE_FRANKLIN_STATIC[weight], False
    return FONTS_DIR / FONT_FILES[key], True


def font_for(T, key, weight, px):
    k = (key, weight, round(float(px), 3))
    if k in _fcache:
        return _fcache[k]
    path, variable = font_file(key, weight)
    f = ImageFont.truetype(str(path), float(px), layout_engine=ImageFont.Layout.RAQM)
    axes = T["fonts"].get(key, {}).get("axes") if variable else None
    if axes:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            v = axes.get(n, a["default"])
            if v is None:
                v = weight
            vals.append(min(max(v, a["minimum"]), a["maximum"]))
        f.set_variation_by_axes(vals)
    _fcache[k] = f
    return f


def font_for_pc(T, key, weight, px, fonts_dir=None):
    """the signature pixel_checks.font_for has; fonts_dir is ignored (the resolver above is the one source)"""
    return font_for(T, key, weight, px)


def glyph_origins(font, text, tracking_px):
    """pen x of every glyph: the font's kerning (prefix lengths) plus tracking between glyphs, as pixel_checks.glyph_origins does"""
    xs = []
    for i, ch in enumerate(text):
        xs.append(font.getlength(text[:i + 1]) - font.getlength(ch) + i * tracking_px)
    return xs


def cap_ratio(T, key, weight):
    b = font_for(T, key, weight, 1000).getbbox("H", anchor="ls")
    return -b[1] / 1000.0


def font_sha(key, weight):
    path, _ = font_file(key, weight)
    h = hashlib.sha256(Path(path).read_bytes()).hexdigest()
    return str(path.relative_to(ROOT)).replace(os.sep, "/"), h


# ------------------------------------------------------------------ seeds and noise
def seed_for(*keys):
    """a stable 32-bit seed from names (the same on every machine)"""
    h = hashlib.sha256("|".join(str(k) for k in keys).encode("utf-8")).digest()
    return int.from_bytes(h[:4], "big")


def rng_for(seed, *keys):
    return np.random.default_rng(np.random.SeedSequence([int(seed) & 0xFFFFFFFF, seed_for(*keys)]))


def fnoise(shape, sx, sy, rng):
    """unit-SD Gaussian-filtered noise (sx, sy: sigma in pixels along x and y), by FFT; periodic, which a board of this size cannot show"""
    H, W = shape
    n = rng.standard_normal((H, W)).astype(np.float32)
    F = np.fft.rfft2(n)
    fy = np.fft.fftfreq(H)[:, None]
    fx = np.fft.rfftfreq(W)[None, :]
    G = np.exp(-2.0 * np.pi ** 2 * ((sx * fx) ** 2 + (sy * fy) ** 2)).astype(np.float32)
    out = np.fft.irfft2(F * G, s=(H, W)).astype(np.float32)
    sd = float(out.std())
    return out / (sd if sd > 1e-9 else 1.0)


# ------------------------------------------------------------------ board geometry
def rows_of(y0, y1):
    """board y (up, mm) to array rows (row 0 = the top of the board), as pixel_checks.to_rows"""
    return H_MM - int(round(y1)), H_MM - int(round(y0))


def street_x_to_board(T, shop, street_x):
    """board x (mm from the viewer's left, as the game shows it) of a street x (the target's section 2)"""
    u0 = shop["board_u0_street_x_m"]
    return (u0 - street_x) * 1000.0 if shop["side"] == "east" else (street_x - u0) * 1000.0


def shop_by_id(T, sid):
    return [s for s in T["shops"] if s["id"] == sid][0]


def hand_blocks(s):
    return [b for b in s["blocks"] if b.get("jitter") and not b["ghost"] and b["in_texture"]]


def free_zone_mask(s, pad=12, W=W_MM, H=H_MM):
    """where a loss patch can be counted: the field less text boxes, ghosts, lines, frames (the check's own definition, without the wear marks).
    The renderer calibrates its paint loss on this zone and check_fascias.py reads it back from the pixels."""
    from scipy import ndimage as ndi
    m = np.ones((H, W), bool)
    m[:24] = m[-24:] = False
    m[:, :24] = m[:, -24:] = False
    for b in s["blocks"]:
        x0, y0, x1, y1 = b["effects_box_mm"]
        m[max(0, H - int(y1 + pad) - 1):H - int(y0 - pad), max(0, int(x0 - pad)):int(x1 + pad) + 1] = False
    gh = s.get("ghost")
    if gh and gh.get("box_mm"):
        x0, y0, x1, y1 = gh["box_mm"]
        m[H - int(y1) - 6:H - int(y0) + 6, int(x0) - 6:int(x1) + 6] = False
    for sh in s["shapes"]:
        if sh["role"] in ("old_board", "box_face", "slab_face"):
            continue
        if sh["kind"] == "rect":
            x0, y0, x1, y1 = sh["box"]
            if sh["role"] in ("box_frame", "slab_edge"):
                fr = (s["border"].get("frame_mm") or s["border"].get("edge_mm") or 12)
                ring = np.zeros((H, W), bool)
                ring[H - int(y1) - 1:H - int(y0) + 1, int(x0) - 1:int(x1) + 2] = True
                inner = np.zeros((H, W), bool)
                inner[H - int(y1 - fr) - 1:H - int(y0 + fr) + 1, int(x0 + fr) - 1:int(x1 - fr) + 2] = True
                m &= ~(ring & ~inner)
            else:
                m[max(0, H - int(y1) - 6):H - int(y0) + 6, max(0, int(x0) - 6):int(x1) + 7] = False
        else:
            pts = np.array(sh["pts"])
            for p_, q_ in zip(pts[:-1], pts[1:]):
                n = max(2, int(np.hypot(*(q_ - p_)) / 2))
                for t in np.linspace(0, 1, n):
                    x, y = p_ + (q_ - p_) * t
                    r, c = H - int(y), int(x)
                    m[max(0, r - 10):r + 10, max(0, c - 10):c + 10] = False
    return m
