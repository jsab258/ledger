"""Author tool: writes target.json for the Quay Street fascia signs (cloud week 42, 8 October 2026; amended the same day after the target review).

    /home/user/.bpyenv/bin/python make_target.py [--fonts DIR]

The hand-made decisions live in the tables below (SHOPS, PALETTE, ...). Everything that can be
computed is computed here and written down, so that target_drawing.py and self_check.py can read
target.json ALONE: ink widths from the real OFL font files, cap heights, contrast ratios, the aged
colours, the checks' nominal values. The fonts are read from DIR (default: $FASCIA_FONTS, then the
scratch folder this was written in); they are NOT stored in git and NOT added to production/fonts/
(unit 4.1 does that). Fetch them with self_check.py --fetch-fonts DIR (raw.githubusercontent.com).

It keeps the sibling convention: hand numbers are labelled with their kind in "kinds":
  Read = printed; Scaled = measured off a drawing; Photo = measured on a photograph today;
  Sheet = measured on the Hook sheet today (an image-model sheet: mood and palette only);
  Derived = computed from the above; Judgement = mine, to be overturned by a better source.
"""
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
SCRATCH_FONTS = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/fonts"
FONT_DIR = os.environ.get("FASCIA_FONTS", SCRATCH_FONTS)
if "--fonts" in sys.argv:
    FONT_DIR = sys.argv[sys.argv.index("--fonts") + 1]

# --------------------------------------------------------------------------------------------
# 0. Colour maths (sRGB, D65). Used to age colours, to compute contrast and to set tolerances.
# --------------------------------------------------------------------------------------------


def s2l(c):
    c = np.asarray(c, float) / 255.0
    return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)


def l2s(l):
    l = np.clip(np.asarray(l, float), 0, 1)
    c = np.where(l <= 0.0031308, 12.92 * l, 1.055 * np.power(l, 1 / 2.4) - 0.055)
    return np.clip(np.round(c * 255), 0, 255).astype(int)


_M = np.array([[0.4124, 0.3576, 0.1805], [0.2126, 0.7152, 0.0722], [0.0193, 0.1192, 0.9505]])
_W = np.array([0.95047, 1.0, 1.08883])


def lab(rgb):
    xyz = (s2l(rgb) @ _M.T) / _W
    f = np.where(xyz > 0.008856, np.cbrt(xyz), 7.787 * xyz + 16 / 116)
    return np.array([116 * f[1] - 16, 500 * (f[0] - f[1]), 200 * (f[1] - f[2])])


def unlab(L):
    fy = (L[0] + 16) / 116
    fx = fy + L[1] / 500
    fz = fy - L[2] / 200
    f = np.array([fx, fy, fz])
    xyz = np.where(f ** 3 > 0.008856, f ** 3, (f - 16 / 116) / 7.787) * _W
    return l2s(np.linalg.solve(_M, xyz))


def dE(a, b):
    return float(np.linalg.norm(lab(a) - lab(b)))


def rel_lum(rgb):
    l = s2l(rgb)
    return float(0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2])


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return float((hi + 0.05) / (lo + 0.05))


GRIME = (88, 82, 74)  # a street's soot-and-damp film, sRGB (Judgement)

# How 1990 wear moves a colour: share of grime film mixed in (linear light), a chalk lift in L*,
# a chroma factor, a yellowing in b*. By paint class. All Judgement; the sign of each shift is the
# trade's own knowledge (dark gloss chalks lighter, vermilion fades first, cream and white acrylic
# yellow, gilt keeps its colour under a dirt film). The Hook sheet's own two colours are measured,
# not aged (see SHEET).
AGE = {
    "dark_gloss": dict(grime=0.07, chalk=3.0, chroma=0.92, yellow=0.0),
    "red": dict(grime=0.06, chalk=5.0, chroma=0.82, yellow=0.0),
    "cream": dict(grime=0.12, chalk=-2.0, chroma=1.0, yellow=4.0),
    "white_plastic": dict(grime=0.10, chalk=-3.0, chroma=1.0, yellow=7.0),
    "gilt": dict(grime=0.10, chalk=-3.0, chroma=0.9, yellow=0.0),
    "vinyl": dict(grime=0.06, chalk=2.0, chroma=0.92, yellow=0.0),
    "black": dict(grime=0.05, chalk=4.0, chroma=1.0, yellow=0.0),
    "glass": dict(grime=0.04, chalk=1.0, chroma=1.0, yellow=0.0),
    "metal": dict(grime=0.10, chalk=-4.0, chroma=0.9, yellow=0.0),
    "none": dict(grime=0.0, chalk=0.0, chroma=1.0, yellow=0.0),
}


def age(rgb, cls):
    p = AGE[cls]
    lin = s2l(rgb) * (1 - p["grime"]) + s2l(GRIME) * p["grime"]
    L = lab(l2s(lin))
    L[0] += p["chalk"]
    L[1] *= p["chroma"]
    L[2] = L[2] * p["chroma"] + p["yellow"]
    return [int(v) for v in unlab(L)]


# --------------------------------------------------------------------------------------------
# 1. Fonts: the OFL families named, the file read, and how to set them. Licence text was read
#    for each at raw.githubusercontent.com/google/fonts/main/ofl/<dir>/OFL.txt on 8 Oct 2026.
# --------------------------------------------------------------------------------------------
FONTS = {
    "marcellus-sc": dict(family="Marcellus SC", dir="marcellussc", file="MarcellusSC-Regular.ttf", axes={},
                         designer="Astigmatic", rfn="Marcellus", in_repo="production/fonts/marcellus-sc (ruled 30 Sep, allowlist 7)",
                         looks_like="flared humanist capitals after Roman inscriptions; the Hook sheet's Mickey's letter"),
    "abril-fatface": dict(family="Abril Fatface", dir="abrilfatface", file="AbrilFatface-Regular.ttf", axes={},
                          designer="TypeTogether", rfn="Abril, Abril Fatface", in_repo=None,
                          looks_like="19th-century fat-face Didone poster capitals, the pawnbroker's and draper's letter"),
    "old-standard-tt-bold": dict(family="Old Standard TT", dir="oldstandardtt", file="OldStandard-Bold.ttf", axes={},
                                 designer="Alexey Kryukov", rfn=None, in_repo="production/fonts/evening-paper has Regular and Italic only",
                                 looks_like="Victorian 'modern' roman, heavy; old fascias and ghost signs"),
    "oswald": dict(family="Oswald", dir="oswald", file="Oswald[wght].ttf", axes={"Weight": None},
                   designer="Vernon Adams, Kalapi Gajjar, Cyreal", rfn=None, in_repo=None,
                   looks_like="condensed gothic block capitals, the signwriter's plain 'block letter'"),
    "jost": dict(family="Jost", dir="jost", file="Jost[wght].ttf", axes={"Weight": None},
                 designer="Owen Earl", rfn=None, in_repo=None, looks_like="Futura-like geometric sans; 1980s refits, cut vinyl"),
    "libre-franklin": dict(family="Libre Franklin", dir="librefranklin", file="LibreFranklin[wght].ttf", axes={"Weight": None},
                           designer="Impallari Type", rfn=None, in_repo="production/fonts/evening-paper has instances 400 to 800",
                           looks_like="Franklin Gothic; newsagents' and tabloid sans"),
    "fraunces": dict(family="Fraunces", dir="fraunces", file="Fraunces[SOFT,WONK,opsz,wght].ttf",
                     axes={"Weight": None, "Softness": 100, "Optical Size": 144, "Wonky": 0},
                     designer="Undercase Type, Phaedra Charles, Flavia Zimbardi", rfn=None, in_repo=None,
                     looks_like="soft, heavy 'Windsor/Cooper' roman of the 1970s-80s café and tea room"),
    "alfa-slab-one": dict(family="Alfa Slab One", dir="alfaslabone", file="AlfaSlabOne-Regular.ttf", axes={},
                          designer="JM Solé", rfn="Alfa Slab", in_repo=None,
                          looks_like="fat Egyptian slab capitals; chandlers', harbour and market lettering"),
    "josefin-sans": dict(family="Josefin Sans", dir="josefinsans", file="JosefinSans[wght].ttf", axes={"Weight": None},
                         designer="Santiago Orozco", rfn="Josefin Sans", in_repo=None,
                         looks_like="Art Deco geometric capitals; the 1930s shop refit"),
}
_fcache = {}


def font(key, weight, px):
    k = (key, weight, px)
    if k in _fcache:
        return _fcache[k]
    spec = FONTS[key]
    f = ImageFont.truetype(os.path.join(FONT_DIR, spec["dir"], spec["file"]), px, layout_engine=ImageFont.Layout.RAQM)
    if spec["axes"]:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            v = spec["axes"].get(n, a["default"])
            if v is None:
                v = weight
            vals.append(min(max(v, a["minimum"]), a["maximum"]))
        f.set_variation_by_axes(vals)
    _fcache[k] = f
    return f


def cap_ratio(key, weight):
    b = font(key, weight, 1000).getbbox("H", anchor="ls")
    return -b[1] / 1000.0


def measure(key, weight, text, cap_mm, tracking_em):
    """Ink box of a one-line string, in mm, relative to its own pen origin on the baseline:
    (x0, y_bottom, x1, y_top) with y up. The string is RENDERED the way pixel_checks.render_block_mask renders it
    (glyph by glyph, the font's kerning, tracking added between glyphs, 1 px = 1 mm) and its ink read off the pixels,
    because PIL's getbbox returns the advance box, which is wider than the ink by the side bearings."""
    r = cap_ratio(key, weight)
    px = cap_mm / r
    f = font(key, weight, px)
    trk = tracking_em * px
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    pad = int(px) + 12
    Wd = int(xs[-1] + f.getlength(text[-1]) + 2 * pad)
    Hd = int(px * 1.7) + 2 * pad
    base = pad + int(px * 1.2)
    img = Image.new("L", (Wd, Hd), 0)
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(text):
        if ch != " ":
            d.text((pad + xs[i], base), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
    rows = np.where(a.any(axis=1))[0]
    cols = np.where(a.any(axis=0))[0]
    return (round(float(cols.min() - pad), 1), round(float(base - (rows.max() + 1)), 1), round(float(cols.max() + 1 - pad), 1), round(float(base - rows.min()), 1)), px


# --------------------------------------------------------------------------------------------
# 2. The board, and WHICH WAY ROUND IT IS (the review's fault 1, checked against the export).
# --------------------------------------------------------------------------------------------
ROOT = HERE.parents[3]
BOARD_W, BOARD_H = 5410, 550
SAFE = [150, 40, BOARD_W - 150, BOARD_H - 40]
FIELD = [24, 24, BOARD_W - 24, BOARD_H - 24]
CX = BOARD_W / 2.0
CONSOLE_CLEAR_M = 0.295            # the board runs 0.295 to 5.705 of a 6.0 m bay (kit README)

# THE AXIS. terrace-front.py builds Quay Street with east at +y, where a viewer facing the parade
# has +x on the RIGHT (the kit README's "left to right seen from the street"), then _export_street
# REFLECTS y to -y ("mirror": "REFLECTED y to -y AT EXPORT"), so in the game, and in the lettered
# faces' UVs ("running from the reader's left to the reader's right in the reflected street"), a
# viewer facing the EAST parade has low street x on the RIGHT, and a viewer facing the WEST block
# has low street x on the LEFT. Street x itself (along the street) is not changed by the mirror.
# The picture shop-fronts-whole-2026-10-08.jpg shows it: TO LET (x 21-27), PAWNBROKER (15-21),
# FRESH FISH (9-15), MICKEY'S (3-9) from the left, with Mickey's door at its right-hand end.
BAY_DOORS_ON = ("left", "left", "right", "left", "right", "right")   # terrace-front.py line 560, in the Blender frame


def door_end(side, bay, block_doors_on=None):
    """'low' or 'high': which END (in street x) of its bay a shop's doors stand at in the game."""
    d = block_doors_on or BAY_DOORS_ON[bay % len(BAY_DOORS_ON)]
    if side == "east":              # Blender frame x = street x on the east side
        return "low" if d == "left" else "high"
    return "high" if d == "left" else "low"      # the west blocks are turned a half turn


def u0_street_x(side, x0, x1):
    """street x at the board's LEFT edge as a viewer in the game sees it"""
    return (x1 - CONSOLE_CLEAR_M) if side == "east" else (x0 + CONSOLE_CLEAR_M)


def u_mm(side, x0, x1, street_x):
    """board x (mm, from the viewer's left) of a street x"""
    u0 = u0_street_x(side, x0, x1)
    return round(((u0 - street_x) if side == "east" else (street_x - u0)) * 1000, 1)


def mickeys_door_x():
    p = ROOT / "production" / "specs" / "mickeys-office.json"
    try:
        return float(json.loads(p.read_text(encoding="utf-8"))["door"]["x"])
    except Exception:  # noqa: BLE001
        return 4.65


def fan_x(x0, x1, end):
    """side-door centre: 0.82 m in from the bay's door end (the kit's side door is at 0.822 m)"""
    return round(x0 + 0.82, 3) if end == "low" else round(x1 - 0.82, 3)


def win_x(x0, x1, end):
    """window centre: 0.975 m from the bay centre, away from the doors (Rita's: 17.025 in 15-21)"""
    c = (x0 + x1) / 2.0
    return round(c + 0.975, 3) if end == "low" else round(c - 0.975, 3)


# --------------------------------------------------------------------------------------------
# 3. Palette: every colour once, sRGB, a plain name, its wear class and where it came from.
#    "fresh" is what the renderer paints; "y1990" is what the checks expect to find (median).
# --------------------------------------------------------------------------------------------
_P = {}


def pal(key, plain, fresh, cls, kind, note="", y1990=None):
    y = y1990 if y1990 is not None else age(fresh, cls)
    _P[key] = dict(plain=plain, srgb_fresh=list(fresh), srgb_1990=list(y), wear_class=cls, kind=kind, note=note)


pal("slate", "slate blue-grey", (52, 66, 80), "none", "Sheet", "Hook sheet, Mickey's board: mean 62,75,87 (p10 48,60,70; p90 80,91,102), measured 8 Oct; fresh is a dark step of it", y1990=(62, 75, 87))
pal("brass_gilt", "dull brass-gilt", (205, 172, 86), "none", "Sheet", "Hook sheet, Mickey's letters: mean 167,149,109 (p90 193,171,130); the applied letters' aged face", y1990=(167, 149, 109))
pal("brass_side", "darker brass (letter flanks)", (120, 98, 58), "none", "Judgement", "side faces of applied letters, 0.7 of the face value", y1990=(112, 96, 68))
pal("gold_leaf", "gold leaf (oil gilding)", (214, 175, 74), "gilt", "Judgement", "fresh 23-carat leaf on gold size; nothing in a source gives a figure")
pal("shade_black", "sign-writer's black", (22, 20, 20), "black", "Photo", "Leadenhall block shade median 66,53,42 under warm lamps; taken as near-black, a ground-tone black")
pal("oxblood", "oxblood", (88, 32, 38), "dark_gloss", "Scaled", "the game's Rita board today is 92,39,43 (make_vignette_2d.py TRADE_FASCIAS); fresh is a half step darker")
pal("light_board", "pale grey-white board", (236, 238, 236), "none", "Sheet", "the Hook sheet puts a WHITE fascia beside Mickey's (measured 204,204,204 in shade); the review's value for the fish board", y1990=(196, 202, 206))
pal("vermilion", "signwriter's vermilion", (200, 40, 36), "red", "Judgement", "t13138's red lettering; fades first of the paints")
pal("cream_shade", "cream", (230, 220, 192), "cream", "Judgement")
pal("cream", "cream", (236, 226, 198), "cream", "Judgement")
pal("bare_timber", "bare soot-darkened timber", (40, 31, 25), "none", "Scaled", "terrace-front.py FASCIA_PAINT bare_timber 0.021,0.014,0.010 linear = 40,31,25 sRGB: the street already draws the empty unit this dark and DECISIONS 3 Oct keeps it 'as the street already draws it'", y1990=(46, 37, 30))
pal("painted_out", "painted-out buff grey", (176, 170, 150), "cream", "Judgement", "the cream overpaint of a gone trade's lettering")
pal("acrylic_white", "white acrylic face", (238, 236, 228), "white_plastic", "Judgement")
pal("acrylic_red", "red translucent acrylic face", (186, 34, 38), "red", "Judgement", "a 1980s newsagent's lit box; not a brand red")
pal("acrylic_brown", "brown acrylic panel", (132, 82, 50), "none", "Judgement", "the review's value for the tea room's flat panel", y1990=(120, 74, 44))
pal("white_timber", "white-painted timber frame", (236, 234, 226), "cream", "Judgement")
pal("vinyl_blue", "royal blue vinyl", (24, 62, 140), "vinyl", "Scaled", "the game's launderette letters today, 28,64,140")
pal("vinyl_red", "scarlet vinyl", (176, 30, 34), "vinyl", "Scaled", "the game's launderette trade line today, 176,30,34")
pal("vinyl_cream", "cream vinyl", (236, 226, 198), "vinyl", "Judgement")
pal("bronze_anodised", "bronze anodised aluminium", (96, 76, 58), "metal", "Judgement", "the 1970s-80s box sign extrusion and its returns")
pal("powder_black", "black powder-coated aluminium", (34, 34, 32), "black", "Judgement", "the newsagent's box returns")
pal("deco_green_glass", "dark bottle-green back-painted glass", (30, 58, 46), "glass", "Judgement", "reverse-painted clear plate glass, a 1930s refit (FRONTAGE-2026-10-06 s.1 and s.3 date the generation; the method is Judgement, from memory, not checked)")
pal("chrome", "chrome strip", (196, 200, 202), "metal", "Judgement")
pal("mastic", "dark mastic (slab joints)", (30, 30, 28), "none", "Judgement")
pal("buff_board", "buff", (200, 188, 156), "cream", "Scaled", "the game's newsagent board today is 190,176,140")
pal("sign_black", "black", (26, 26, 24), "black", "Judgement")
pal("navy", "navy", (28, 42, 78), "dark_gloss", "Scaled", "the game's chandler letters today are 30,40,70; as a board colour 28,42,78")
pal("white_paint", "signwriter's white", (238, 234, 220), "cream", "Judgement")
pal("hemp", "hemp rope", (196, 176, 136), "cream", "Judgement")
pal("whitewash", "whitewash", (238, 236, 228), "cream", "Read", "'white whitewash lettering on the glass', Picture Sheffield t13138, read on the PC 3 Oct (earlier note)")
PALETTE = _P


def ghost_rgb(ground, dE_, vec):
    """the colour of an older, painted-out lettering: the ground shifted by dE_ in Lab along vec"""
    L = lab(ground)
    v = np.array(vec, float)
    v = v / np.linalg.norm(v) * dE_
    return [int(x) for x in unlab(L + v)]


# --------------------------------------------------------------------------------------------
# 4. The ten fascias. Each block: text, font, weight, cap height (mm), tracking (em), anchor, baseline.
#    x is the board's own x (from the viewer's LEFT in the game, section 2); y is up from the board's bottom.
# --------------------------------------------------------------------------------------------
def blk(id_, text, font_key, weight, cap, trk, baseline, face, anchor="centre", x=None, shade=None, outline=None,
        technique="painted", jitter=None, relief_mm=0.0, role="name", shade_kind="block45", embolden_mm=0.0,
        ghost=False, face_rgb=None, broken=0.0, in_texture=True, layout=None):
    return dict(id=id_, text=text, font=font_key, weight=weight, cap_mm=cap, tracking_em=trk, baseline_mm=baseline,
                anchor=anchor, x_mm=CX if x is None else x, face=face, shade=shade, outline=outline, technique=technique,
                jitter=jitter, relief_mm=relief_mm, role=role, shade_kind=shade_kind, embolden_mm=embolden_mm,
                ghost=ghost, face_rgb=face_rgb, broken_fraction=broken, in_texture=in_texture)


def SH(colour, cap):
    """P1: the block shade is 0.10 of the cap, 45 degrees down and right."""
    return dict(colour=colour, d_mm=round(0.10 * cap, 1))


HAND = dict(baseline_mm=1.6, baseline_sd_mm=[0.6, 1.6], other_sd_mm=[0.0, 0.6], advance_pct=1.5, rotation_deg=0.35, stroke_pct=3.0,
            note="a hand-painted board: each glyph nudged; none on vinyl, applied or glass-gilt letters (their baseline SD is 0 to 0.6 mm at 1 px per mm: the pixel grid alone gives 0.3 to 0.5)")

SHOPS = []
MK_DOOR = mickeys_door_x()


def base(id_, order, block, bay, x0, x1, side, number, **kw):
    end = door_end(side, bay, "right" if block == "east_chandler" else None)
    s = dict(id=id_, order=order, block=block, bay=bay, street_x_m=[x0, x1], side=side, street_number=number,
             door_end_street=end, board_u0_street_x_m=round(u0_street_x(side, x0, x1), 3),
             board_u_rule=("u (board x) grows as street x FALLS: low street x is on the viewer's RIGHT" if side == "east"
                           else "u (board x) grows as street x RISES: low street x is on the viewer's LEFT"),
             fanlight_street_x_m=fan_x(x0, x1, end), window_centre_street_x_m=win_x(x0, x1, end))
    s.update(kw)
    return s


# --- bay 0, Mickey's ------------------------------------------------------------------------
MK_X = u_mm("east", 3.0, 9.0, MK_DOOR)
SHOPS.append(base(
    "mickeys", 0, "east_parade", 0, 3.0, 9.0, "east", "1",
    trade="minicab office", name_minted=True, name_source="canon.md (Brands and law; D19); content/brands/brand-bible-v1.json id mickeys (founded 1962)",
    construction="painted timber board; the name is GEOMETRY, the recipe's raised gilt letters (RAISED_LETTERS), not texture",
    construction_kind="applied_letters", layout_class="name_only_offset",
    ground=dict(colour="slate", finish="eggshell paint, many coats, a little orange-peel", roughness=0.55, metallic=0.0,
                grain=dict(direction="along", amp_L=1.2, scale_mm=[40, 400])),
    blocks=[blk("name", "MICKEY’S", "marcellus-sc", 400, 330, 0.03, 100, "brass_gilt", anchor="centre", x=MK_X,
                technique="applied_geometry", relief_mm=14.0, role="name", embolden_mm=3.0, in_texture=False),
            blk("ghost_name", "MICKEY’S", "marcellus-sc", 400, 245, 0.03, 150, "slate", anchor="centre", x=CX, role="ghost", ghost=True,
                face_rgb=ghost_rgb(PALETTE["slate"]["srgb_1990"], 3.5, (0.6, 0.0, -0.8)), technique="painted_ghost", broken=0.0)],
    border=None,
    notes=["The name stands over the shop door: board x %.0f = the board's viewer-left end (street x 8.705) minus the door's x %.2f (mickeys-office.json door.x) = %.3f m. In the game the door is at the viewer's RIGHT end of the bay (shop-fronts-whole-2026-10-08.jpg; morning-hook-day-2026-10-08.jpg)." % (MK_X, MK_DOOR, MK_X / 1000.0),
           "THE LETTERS ARE NOT IN THE TEXTURE. The recipe already builds MICKEY’S as raised gilt geometry (terrace-front.py RAISED_LETTERS, line 857) over a board picture with no letters; the geometry section amends its cap, centre and stand-off. The texture carries the ground, the ghost of the older sign, ten pin holes and a soft contact shadow under where the letters stand.",
           "'Sign hand-painted and repainted a shade off each time' (brand bible): under the letters a ghost of an older, centred, smaller MICKEY’S in a blue 3.5 dE off the board, a brush-cut edge with a 1 mm ridge, and ten dark pin holes (3 to 4 mm) along its old cap line."],
    ghost=dict(kind="older_lettering", string="MICKEY’S", font="marcellus-sc", cap_mm=245, centre_x_mm=CX, baseline_mm=150, dE=3.5, towards="blue (lighter, bluer)", broken_fraction=0.0,
               edge="brush-cut edge, 1 mm ridge", pinholes=10, pinhole_row="along the old cap line y = 395 mm, evenly across the old ink box"),
    geometry=[dict(id="mickeys_letters", kind="applied_letters", source="tools/art-recipes/terrace-front.py RAISED_LETTERS (line 857), AMENDED here",
                   string="MICKEY’S", font="marcellus-sc", cap_m=0.330, blender_text_size_m=None, tracking_em=0.03, embolden_m=0.003, stand_off_m=0.014,
                   centre_board_x_mm=MK_X, centre_street_x_m=MK_DOOR, baseline_board_y_mm=100,
                   face="brass_gilt", flanks="brass_side", edge="square-cut", roughness=0.38, metallic=0.85,
                   replaces="the recipe's cap 0.24 m, 12 mm stand-off, centred across the whole sign piece",
                   contact_shadow_in_texture=dict(blur_mm=6, opacity=0.35, offset_mm=[-2, -5]),
                   note="a script sets the Blender text size from the font's measured cap ratio (cap_m / 0.701), not from the recipe's 0.66, which makes the letters 6 per cent too tall")],
    age=dict(klass=2, loss_fraction=0.04, chalk_dL=3.0, grime_film=0.07, runs=dict(count=4, len_mm=[40, 160]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=2, kind="two short runs under the console fixings")),
    lit=None, moulding=None))

# --- bay 1, Fish Market ---------------------------------------------------------------------
SHOPS.append(base(
    "fish_market", 1, "east_parade", 1, 9.0, 15.0, "east", "3",
    trade="fishmonger", name_minted=True, name_source="DECISIONS.md 3 Oct 2026 ('the fishmonger (Fish Market)'); production/specs/hook-cast.json fish_market",
    construction="sign-written flat paint on the sheet's pale board; red block capitals with a black block shade; the trade in three lines beside the name; two red rules",
    construction_kind="signwritten", layout_class="name_left_list_right",
    ground=dict(colour="light_board", finish="gloss enamel gone flat and chalky", roughness=0.58, metallic=0.0,
                grain=dict(direction="along", amp_L=1.5, scale_mm=[30, 300])),
    blocks=[blk("name", "FISH MARKET", "oswald", 600, 290, 0.06, 188, "vermilion", anchor="left", x=1270, shade=SH("shade_black", 290), jitter=HAND, role="name"),
            blk("trade_1", "WET FISH", "oswald", 500, 70, 0.10, 408, "sign_black", anchor="left", x=3715, jitter=HAND, role="trade"),
            blk("trade_2", "SHELLFISH", "oswald", 500, 70, 0.10, 298, "sign_black", anchor="left", x=3715, jitter=HAND, role="trade"),
            blk("trade_3", "SMOKED", "oswald", 500, 70, 0.10, 188, "sign_black", anchor="left", x=3715, jitter=HAND, role="trade"),
            blk("ghost_name", "FISHMONGER", "old-standard-tt-bold", 700, 200, 0.0, 160, "light_board", anchor="centre", x=CX, role="ghost", ghost=True,
                face_rgb=ghost_rgb(PALETTE["light_board"]["srgb_1990"], 4.0, (-1.0, 0.0, 0.0)), technique="painted_ghost", broken=0.6)],
    border=dict(kind="rules", rules=[dict(y_mm=[34, 46], x_mm=[120, BOARD_W - 120], colour="vermilion"), dict(y_mm=[BOARD_H - 46, BOARD_H - 34], x_mm=[120, BOARD_W - 120], colour="vermilion")]),
    notes=["RED SIGN-WRITING, AS t13138 (25 Aug 1990, earlier note) shows a fishmonger's, but on the Hook sheet's PALE board beside Mickey's (the review: the nearest two boards in the hook frame must not both be dark blue-grey). The photograph shows red lettering; the sheet shows a white fascia there; the ground is the sheet's, the letters the photograph's.",
           "Layout: name at the viewer's left, the trade in three short lines at its right (name and list centred as a group). Black block shade on the red, the list in black; the vermilion rules stay.",
           "The older sign, FISHMONGER in Old Standard TT Bold, shows through the repaint: trade words only, 4 dE darker than the board, 60 per cent of its strokes painted over."],
    ghost=dict(kind="older_lettering", string="FISHMONGER", font="old-standard-tt-bold", cap_mm=200, centre_x_mm=CX, baseline_mm=160, dE=4.0, towards="darker", broken_fraction=0.6, edge="brush edge", pinholes=0),
    geometry=[], age=dict(klass=2, loss_fraction=0.05, chalk_dL=4.0, grime_film=0.08, runs=dict(count=6, len_mm=[50, 200]), gull=dict(count=3, size_mm=[15, 45]), rust=dict(count=0, kind="")),
    lit=None, moulding=None))

# --- bay 2, Rita's ---------------------------------------------------------------------------
SHOPS.append(base(
    "ritas", 2, "east_parade", 2, 15.0, 21.0, "east", "5",
    trade="pawnbroker", name_minted=True, name_source="production/specs/hook-cast.json (ritas, rita); DECISIONS.md 30 Sep and 6 Oct; RULINGS 2 Oct 'Rita's window is the model'",
    construction="oil-gilded capitals with a black block shade on an oxblood board inside a gilt cut-corner keyline panel; a planted moulding round the board",
    construction_kind="gilded", layout_class="centred_stack_with_ends",
    ground=dict(colour="oxblood", finish="oil gloss, now satin", roughness=0.45, metallic=0.0,
                grain=dict(direction="along", amp_L=1.2, scale_mm=[40, 400])),
    blocks=[blk("name", "RITA’S", "abril-fatface", 400, 230, 0.10, 221, "gold_leaf", shade=SH("shade_black", 230), technique="gilded", jitter=HAND, role="name"),
            blk("trade", "PAWNBROKER", "old-standard-tt-bold", 700, 84, 0.12, 99, "gold_leaf", shade=SH("shade_black", 84), technique="gilded", jitter=HAND, role="trade"),
            blk("end_l", "5", "abril-fatface", 400, 214, 0.0, 168, "gold_leaf", anchor="left", x=200, shade=SH("shade_black", 214), technique="gilded", jitter=HAND, role="end"),
            blk("end_r", "5", "abril-fatface", 400, 214, 0.0, 168, "gold_leaf", anchor="right", x=BOARD_W - 200, shade=SH("shade_black", 214), technique="gilded", jitter=HAND, role="end")],
    border=dict(kind="cutcorner_panel", inset_mm=44, line_mm=13, inner_line_mm=0, gap_mm=0, radius_mm=70, colour="gold_leaf"),
    notes=["The numbers at the two ends are what the photographed Leadenhall boards do (both ends, 0.91 of the name's cap height, P1); the number 5 is proposed, not minted. The keyline is P1's: one line 0.027 of the field thick, inset 0.09, corners cut by a concave quarter circle.",
           "The three balls hang from a bracket at the door end (projecting_signs); the toplight glass carries WATCHES, JEWELLERY and LOANS (glass), so the board stays calm."],
    ghost=dict(kind="repaint_patch", box_mm=[2300, 140, 3300, 340], dE=3.0, edge="brush-cut edge", pinholes=0),
    geometry=[], age=dict(klass=1, loss_fraction=0.03, chalk_dL=3.0, grime_film=0.06, runs=dict(count=3, len_mm=[40, 140]), gull=dict(count=1, size_mm=[15, 35]), rust=dict(count=0, kind="")),
    lit="night_window_lit", moulding=dict(width_mm=24, height_mm=0.6, chamfer_mm=4)))

# --- bay 3, the empty unit ------------------------------------------------------------------
SHOPS.append(base(
    "empty_unit", 3, "east_parade", 3, 21.0, 27.0, "east", "7",
    trade="empty unit to let", name_minted=False, name_source="RULINGS 3 Oct; DECISIONS.md 3 Oct ('whitewashed', 'as the street already draws it')",
    construction="bare soot-darkened timber, the last trade's lettering painted out in buff, a letting board across the middle",
    construction_kind="bare", layout_class="none",
    ground=dict(colour="bare_timber", finish="paint long gone: dark soot-grimed timber with a few patches of old paint", roughness=0.85, metallic=0.0,
                grain=dict(direction="along", amp_L=3.0, scale_mm=[25, 600])),
    blocks=[], border=None,
    notes=["No lettering at all: a painted-out patch 3200 x 300 mm in buff (176,170,150), brush strokes along the board, its edge a thin ridge of old paint, no legible letter.",
           "The board is the street's own dark bare timber (recipe `bare_timber`, 40,31,25; DECISIONS 3 Oct keeps the unit as the street draws it); the buff patch is what lifts it.",
           "The letting board (900 x 450 mm, TO LET) is a separate asset; its place is in 'small_panels'."],
    ghost=dict(kind="painted_out_patch", box_mm=[1105, 120, 4305, 420], dE=0.0, edge="ridge 0.4 mm, ragged", pinholes=6),
    geometry=[], age=dict(klass=3, loss_fraction=0.17, chalk_dL=0.0, grime_film=0.15, runs=dict(count=10, len_mm=[60, 300]), gull=dict(count=6, size_mm=[20, 70]), rust=dict(count=3, kind="three runs from the nail heads of the removed lettering")),
    lit=None, moulding=None))

# --- bay 4, Steam Laundry (launderette) -------------------------------------------------------
SHOPS.append(base(
    "steam_laundry", 4, "east_parade", 4, 27.0, 33.0, "east", "9",
    trade="launderette (the Steam Laundry)", name_minted=True, name_source="DECISIONS.md 3 Oct ('the Steam Laundry as a launderette'); hook-cast.json laundry",
    construction="lit plastic box sign: white acrylic face, a red cut-vinyl panel, blue cut-vinyl name, fluorescent tubes behind; the box is GEOMETRY",
    construction_kind="box_sign", layout_class="panel_left_name_right",
    ground=dict(colour="acrylic_white", finish="acrylic, semi-gloss, yellowing", roughness=0.35, metallic=0.0,
                grain=dict(direction="none", amp_L=0.8, scale_mm=[200, 800])),
    blocks=[blk("name", "STEAM LAUNDRY", "jost", 800, 200, 0.05, 175, "vinyl_blue", anchor="right", x=5030, technique="vinyl", role="name"),
            blk("trade_1", "LAUNDERETTE", "jost", 600, 90, 0.06, 340, "vinyl_cream", anchor="centre", x=1195, technique="vinyl", role="trade"),
            blk("trade_2", "SERVICE WASHES", "jost", 600, 70, 0.06, 230, "vinyl_cream", anchor="centre", x=1195, technique="vinyl", role="trade"),
            blk("trade_3", "DRY CLEANING", "jost", 600, 70, 0.06, 120, "vinyl_cream", anchor="centre", x=1195, technique="vinyl", role="trade")],
    border=dict(kind="box", outer_mm=[105, 35, 5305, 515], frame_mm=26, colour="bronze_anodised", face_colour="acrylic_white",
                panels=[dict(box_mm=[320, 100, 2070, 450], colour="vinyl_red")]),
    notes=["Plastic box sign of the 1970s-80s kind (note 4: 'the backlit Perspex sign was increasingly replacing the old fascias'), screwed over the old board: the old board (cream, timber, chalked) shows 105 mm at each end and 35 mm above and below.",
           "Layout: the trade in a scarlet vinyl panel at the viewer's LEFT (LAUNDERETTE over SERVICE WASHES over DRY CLEANING, cream vinyl), the name in blue vinyl at the right.",
           "THE BOX IS GEOMETRY (section geometry): 5200 x 480 mm, 150 mm deep, bronze returns. The texture is the box's FRONT (the sub-rectangle [105,35,5305,515] of the render) and the old board round it."],
    ghost=None,
    geometry=[dict(id="steam_laundry_box", kind="box_sign", outer_mm=[105, 35, 5305, 515], depth_m=0.15, returns="bronze_anodised", face_texture_rect_mm=[105, 35, 5305, 515],
                   fixing="eight pan-head screws through the frame into the board; the box stands 0.15 m out from the board face (0.27 m from the wall)", kind_of_number="Judgement (the depth)",
                   emissive=dict(face_mm=[131, 61, 5279, 489], tube_rows_y_mm=[168, 382], tube_joints_x_mm=[300, 1800, 3300, 4800], row_band_pct=6, tube_end_shadow=dict(width_mm=60, dim_pct=10),
                                 dead_tube=dict(row="upper", x_mm=[3300, 4800], level_pct=60, why="the lower row still lights it")))],
    age=dict(klass=2, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.10, runs=dict(count=7, len_mm=[60, 220]), gull=dict(count=0, size_mm=[0, 0]), rust=dict(count=0, kind=""),
             old_board=dict(loss_fraction=0.08, note="the visible ring of old board is chalked cream timber with paint loss")),
    lit="tubes", moulding=None, old_board=dict(colour="cream", box_mm=[0, 0, BOARD_W, BOARD_H])))

# --- bay 5, grocer --------------------------------------------------------------------------
SHOPS.append(base(
    "grocer", 5, "east_parade", 5, 33.0, 39.0, "east", "11",
    trade="grocer", name_minted=False, name_source="trade-only: no proprietor minted (DECISIONS.md 3 Oct names the trade only)",
    construction="1930s refit: three slabs of reverse-painted plate glass, dark bottle green, Art Deco cream capitals, chrome edge and speed lines",
    construction_kind="glass_panel", layout_class="centred_stack",
    ground=dict(colour="deco_green_glass", finish="polished glass over matte paint, grimy", roughness=0.08, metallic=0.0,
                grain=dict(direction="none", amp_L=0.6, scale_mm=[300, 900])),
    blocks=[blk("name", "FAMILY GROCER", "josefin-sans", 700, 190, 0.12, 238, "cream", technique="back_painted", role="name"),
            blk("trade", "HIGH CLASS PROVISIONS", "josefin-sans", 600, 70, 0.12, 122, "cream", technique="back_painted", role="trade")],
    border=dict(kind="glass_slab", outer_mm=[40, 25, BOARD_W - 40, BOARD_H - 25], edge_mm=12, colour="chrome", joints_x_mm=[1380, 4030], joint_mm=3,
                speed_lines=dict(y_mm=[262, 282, 302], line_mm=6, x_left_mm=[52, 640], x_right_mm=[BOARD_W - 640, BOARD_W - 52])),
    notes=["A 1930s refit of the parade in glass (FRONTAGE-2026-10-06: 'the 1930s used etched sunrise patterns, bronze, chrome and Vitrolite'). METHOD (the review's fault 10): reverse-painted CLEAR plate glass, the signwriter's glass fascia, so the cream letters are painted on the back and seen through; the trade name Vitrolite (coloured right through, opaque) is NOT used. Judgement, from memory, not checked.",
           "Three slabs: joints at x 1380 and 4030, 3 mm of dark mastic (30,30,28), a 2 mm polished bevel on every slab edge; the name's ink lies inside the middle slab. No crack on the fascia (the note puts the cracks low, at the stallriser).",
           "Chrome edge strip and speed lines are RAISED METAL IN THE HEIGHT MAP: +0.8 mm (not geometry). Joints -0.5 mm, bevels a 2 mm ramp.",
           "FAMILY GROCER is a trade description, not a name."],
    ghost=None,
    geometry=[], age=dict(klass=2, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.06, runs=dict(count=5, len_mm=[60, 240]), gull=dict(count=1, size_mm=[20, 45]), rust=dict(count=0, kind="")),
    lit=None, moulding=None))

# --- west_north bay 0, newsagent (street x 36 to 42, the recipe's turned numbering) ----------
SHOPS.append(base(
    "newsagent", 6, "west_north", 0, 36.0, 42.0, "west", "18",
    trade="newsagent and tobacconist", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct. SEE THE CAST CONFLICT in TARGET.md (hook-cast puts the newsagent at x 30-36)",
    construction="lit plastic box sign: red translucent acrylic face, cream cut-vinyl name only, two vinyl rules; the box is GEOMETRY; the trade is on the door glass",
    construction_kind="box_sign", layout_class="name_only_rules",
    ground=dict(colour="acrylic_red", finish="acrylic, semi-gloss, sun-faded", roughness=0.35, metallic=0.0,
                grain=dict(direction="none", amp_L=0.8, scale_mm=[200, 800])),
    blocks=[blk("name", "NEWSAGENT", "libre-franklin", 900, 260, 0.08, 145, "vinyl_cream", technique="vinyl", role="name")],
    border=dict(kind="box", outer_mm=[95, 40, 5315, 510], frame_mm=24, colour="powder_black", face_colour="acrylic_red",
                rules=[dict(y_mm=[90, 104], x_mm=[220, 5190], colour="vinyl_cream"), dict(y_mm=[446, 460], x_mm=[220, 5190], colour="vinyl_cream")]),
    notes=["The NAME ALONE on the fascia (the review's fault 5); TOBACCONIST & CONFECTIONER is cream cut vinyl on the shop-door glass (cap 70). A second 1980s lit plastic front, with a red face.",
           "THE BOX IS GEOMETRY: 5220 x 470 mm, 140 mm deep, black powder-coated returns. The old board shows 95 mm at the ends and 40 mm above and below.",
           "The newsagent opens 6.00 to 17.30 (hook-cast), so the face is lit when it is open; one corner of the lower vinyl rule curls."],
    ghost=None,
    geometry=[dict(id="newsagent_box", kind="box_sign", outer_mm=[95, 40, 5315, 510], depth_m=0.14, returns="powder_black", face_texture_rect_mm=[95, 40, 5315, 510],
                   fixing="eight pan-head screws through the frame into the board", kind_of_number="Judgement (the depth)",
                   emissive=dict(face_mm=[119, 64, 5291, 486], tube_rows_y_mm=[170, 380], tube_joints_x_mm=[250, 1750, 3250, 4750], row_band_pct=6, tube_end_shadow=dict(width_mm=60, dim_pct=10), dead_tube=None))],
    age=dict(klass=2, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.09, runs=dict(count=5, len_mm=[40, 150]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=0, kind=""),
             old_board=dict(loss_fraction=0.08, note="the visible ring of old board is chalked cream timber with paint loss"),
             vinyl=dict(lifted_corners=1, note="the lower rule's right end lifts 30 mm; no letter is lost")),
    lit="tubes", moulding=None, old_board=dict(colour="cream", box_mm=[0, 0, BOARD_W, BOARD_H])))

# --- west_north bay 1, ironmonger (x 30 to 36) --------------------------------------------------
SHOPS.append(base(
    "ironmonger", 7, "west_north", 1, 30.0, 36.0, "west", "16",
    trade="ironmonger", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct",
    construction="sign-written black roman capitals with a vermilion block shade on a buff board, black rule border, the trade in the two end panels",
    construction_kind="signwritten", layout_class="name_centre_trade_in_ends",
    ground=dict(colour="buff_board", finish="gloss paint, chalked and grimy", roughness=0.55, metallic=0.0,
                grain=dict(direction="along", amp_L=1.5, scale_mm=[30, 300])),
    blocks=[blk("name", "IRONMONGER", "old-standard-tt-bold", 700, 180, 0.08, 185, "sign_black", shade=SH("vermilion", 180), jitter=HAND, role="name"),
            blk("end_l_1", "TOOLS &", "old-standard-tt-bold", 700, 70, 0.06, 285, "sign_black", anchor="centre", x=600, shade=SH("vermilion", 70), jitter=HAND, role="trade"),
            blk("end_l_2", "HARDWARE", "old-standard-tt-bold", 700, 70, 0.06, 190, "sign_black", anchor="centre", x=600, shade=SH("vermilion", 70), jitter=HAND, role="trade"),
            blk("end_r_1", "PAINTS &", "old-standard-tt-bold", 700, 70, 0.06, 285, "sign_black", anchor="centre", x=4810, shade=SH("vermilion", 70), jitter=HAND, role="trade"),
            blk("end_r_2", "PARAFFIN", "old-standard-tt-bold", 700, 70, 0.06, 190, "sign_black", anchor="centre", x=4810, shade=SH("vermilion", 70), jitter=HAND, role="trade"),
            blk("ghost_name", "IRONMONGER", "old-standard-tt-bold", 700, 190, 0.0, 170, "buff_board", anchor="centre", x=CX, role="ghost", ghost=True,
                face_rgb=ghost_rgb(PALETTE["buff_board"]["srgb_1990"], 4.0, (-1.0, 0.0, 0.0)), technique="painted_ghost", broken=0.6)],
    border=dict(kind="double_rule", inset_mm=36, line_mm=8, inner_gap_mm=14, inner_line_mm=3, colour="sign_black", inner_colour="vermilion", corner_block_mm=30),
    notes=["The name stands alone in the middle; TOOLS & HARDWARE at the viewer's left end and PAINTS & PARAFFIN at the right, two lines each, centred at x 600 and 4810 (the review's fault 5). The number 16 is on the fanlight only. EST. 1884 is on the glass (proposed).",
           "Old Standard TT Bold (note 4's list for old fascias) in place of Libre Baskerville (the review's note 6). The older sign, IRONMONGER, shows through the repaint at 4 dE, 60 per cent painted over.",
           "Metal-framed window (recipe SHOPFRONT_REFITS west_north bay 1) under a painted timber fascia: the refit did not reach the board."],
    ghost=dict(kind="older_lettering", string="IRONMONGER", font="old-standard-tt-bold", cap_mm=190, centre_x_mm=CX, baseline_mm=170, dE=4.0, towards="darker", broken_fraction=0.6, edge="brush edge", pinholes=0),
    geometry=[], age=dict(klass=2, loss_fraction=0.06, chalk_dL=4.0, grime_film=0.12, runs=dict(count=6, len_mm=[40, 180]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=2, kind="two runs from the board's own nail heads at the left end")),
    lit=None, moulding=dict(width_mm=24, height_mm=0.6, chamfer_mm=4)))

# --- west_north bay 2, tea rooms, a plain caff (x 24 to 30) -------------------------------------
SHOPS.append(base(
    "tea_rooms", 8, "west_north", 2, 24.0, 30.0, "west", "14",
    trade="tea room", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct ('a tea room'); hook-cast.json calls it the cafe or the caff (open 6.30 to 22.00)",
    construction="a plain 1980s caff front: a flat, unlit brown acrylic panel with a white timber frame screwed over the board, cream cut-vinyl lettering",
    construction_kind="flat_panel", layout_class="trade_above_name",
    ground=dict(colour="acrylic_brown", finish="acrylic, semi-gloss, dulled", roughness=0.35, metallic=0.0,
                grain=dict(direction="none", amp_L=0.8, scale_mm=[200, 800])),
    blocks=[blk("name", "Tea Rooms", "fraunces", 900, 200, 0.02, 118, "vinyl_cream", technique="vinyl", role="name"),
            blk("trade", "BREAKFASTS, LUNCHES & TEAS", "fraunces", 600, 70, 0.06, 362, "vinyl_cream", technique="vinyl", role="trade")],
    border=dict(kind="flat_panel", outer_mm=[90, 40, 5320, 510], frame_mm=25, colour="white_timber", face_colour="acrylic_brown"),
    notes=["The review's fault 6: the tea room is the second 1980s front and a plain caff (hook-cast: 'the caff', open 6.30), not a heritage café. The trade line stands ABOVE the name; the name is the only mixed-case name on the street (cap height is the T's).",
           "Unlit. THE PANEL IS GEOMETRY in a thin way: 5230 x 470 x 30 mm slab screwed over the board; the texture is its face and frame and the old board round it."],
    ghost=None,
    geometry=[dict(id="tea_rooms_panel", kind="flat_panel", outer_mm=[90, 40, 5320, 510], depth_m=0.03, returns="white_timber", face_texture_rect_mm=[90, 40, 5320, 510], fixing="screwed through the frame into the board", kind_of_number="Judgement")],
    age=dict(klass=1, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.07, runs=dict(count=3, len_mm=[40, 120]), gull=dict(count=1, size_mm=[15, 30]), rust=dict(count=0, kind=""),
             old_board=dict(loss_fraction=0.08, note="the visible ring of old board is chalked cream timber with paint loss")),
    lit=None, moulding=None, old_board=dict(colour="cream", box_mm=[0, 0, BOARD_W, BOARD_H])))

# --- east_chandler, ship chandler (x 40 to 46) ------------------------------------------------------
SHOPS.append(base(
    "chandler", 9, "east_chandler", 0, 40.0, 46.0, "east", "13",
    trade="ship chandler", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct",
    construction="white Egyptian capitals with a black block shade on a navy board, a painted rope border",
    construction_kind="signwritten", layout_class="centred_stack_with_ends",
    ground=dict(colour="navy", finish="gloss paint, salt-weathered", roughness=0.5, metallic=0.0,
                grain=dict(direction="along", amp_L=1.4, scale_mm=[30, 350])),
    blocks=[blk("name", "SHIP CHANDLER", "alfa-slab-one", 400, 170, 0.05, 245, "white_paint", shade=SH("shade_black", 170), jitter=HAND, role="name"),
            blk("trade", "ROPE · PAINT · CHARTS · TWINE", "libre-franklin", 700, 70, 0.10, 135, "vinyl_cream", jitter=HAND, role="trade"),
            blk("end_l", "13", "alfa-slab-one", 400, 158, 0.0, 196, "white_paint", anchor="left", x=210, shade=SH("shade_black", 158), jitter=HAND, role="end"),
            blk("end_r", "13", "alfa-slab-one", 400, 158, 0.0, 196, "white_paint", anchor="right", x=BOARD_W - 210, shade=SH("shade_black", 158), jitter=HAND, role="end")],
    border=dict(kind="rope", inset_mm=34, rope_mm=12, corner_radius_mm=40, pitch_mm=28, colour="hemp"),
    notes=["Metal-framed window (recipe: east_chandler is a metal refit) under a painted board. The number 13 is proposed, not minted (EST. 1879 is on the glass). Salt bloom: the board's lower edge is whiter."],
    ghost=None,
    geometry=[], age=dict(klass=2, loss_fraction=0.07, chalk_dL=4.0, grime_film=0.10, runs=dict(count=6, len_mm=[40, 200]), gull=dict(count=4, size_mm=[20, 60]), rust=dict(count=3, kind="three runs under fixings; the quay is near")),
    lit=None, moulding=dict(width_mm=24, height_mm=0.6, chamfer_mm=4)))


# --------------------------------------------------------------------------------------------
# 5. Everything that is not fascia lettering: projecting signs, glass, small panels. Judgement
#    throughout unless a kind says otherwise; sizes are metres for geometry, mm for lettering.
#    The brackets are fixed to the BRICK ABOVE THE CORNICE (the review's fault 9): the kit's cornice
#    stands 3.40 to 3.55 m and projects 0.215 m; plates and arms are above 3.55 m, so nothing is
#    bolted to a console, the cornice or the fascia sign.
# --------------------------------------------------------------------------------------------
CORNICE_TOP_M = 3.55


def side_word(side, street_x, x0, x1):
    """the viewer's side of a street x within its bay, in the game's words"""
    high = street_x > (x0 + x1) / 2.0
    if side == "east":
        return "the viewer's LEFT end of the bay (high street x)" if high else "the viewer's RIGHT end of the bay (low street x)"
    return "the viewer's RIGHT end of the bay (high street x)" if high else "the viewer's LEFT end of the bay (low street x)"


PROJECTING = [
    dict(id="ritas_three_balls", shop="ritas", kind="bracket sign, three balls",
         mount=dict(x_street_m=20.825, bay_end="door end (high street x)", viewer_side=side_word("east", 20.825, 15.0, 21.0), on="the brick above the cornice, over the party-wall pier at the door end of bay 2",
                    plate_foot_m=3.60, plate_centre_m=3.75, arm_height_m=3.75, projection_m=0.85),
         parts=dict(arm="wrought-iron scroll bracket, 20 x 8 mm bar, four scrolls, a hook and a ring; mounting plate 0.18 x 0.30 m, four bolt heads",
                    balls=dict(count=3, diameter_m=0.26, arrangement="two above, one below (a triangle)", centres_m=[[0.57, 3.00, -0.14], [0.57, 3.00, 0.14], [0.57, 2.78, 0.0]],
                               note="x = out from the wall face along the arm (0.57 of 0.85), y up, z along the street from the hanger"),
                    hanger="10 mm iron rod, 0.57 m, from the arm at 3.75 m down to the ring over the top balls (3.18 m)", drop_m=0.57),
         materials=dict(balls=dict(colour="gold_leaf", plain="gilt paint over sheet metal, scuffed to metal where hands reach", roughness=0.38, metallic=0.8),
                        iron=dict(colour="sign_black", plain="black paint on wrought iron, rust at the bolts", roughness=0.6, metallic=0.5)),
         lowest_m=2.65, kind_of_number="Judgement", note="No photograph of one was reached. The three balls are the pawnbroker's traditional sign and not a trade mark; no name or lettering on them."),
    dict(id="steam_laundry_box", shop="steam_laundry", kind="double-sided projecting box sign",
         mount=dict(x_street_m=27.175, bay_end="window end (low street x)", viewer_side=side_word("east", 27.175, 27.0, 33.0), on="its back edge fixed to the brick above the cornice (a fascia-level box sign), 3.60 to 4.05 m",
                    plate_foot_m=None, plate_centre_m=None, arm_height_m=4.05, projection_m=0.62),
         parts=dict(box_m=[0.62, 0.45, 0.14], note="width 0.62 projects from the wall; 0.45 high from 3.60 to 4.05 m; 0.14 thick between the two faces; bronze extrusion 20 mm, white acrylic faces, two tubes inside"),
         faces=dict(text="LAUNDERETTE", font="jost", weight=800, cap_mm=60, tracking_em=0.03, colour="vinyl_blue", ground="acrylic_white",
                    note="each face reads left to right from its own side; faces are mirror-correct, not mirrored"),
         emissive=True, lowest_m=3.60, kind_of_number="Judgement", note="Lit when the shop is open (hours in hook-cast.json)."),
    dict(id="ironmonger_hanging_board", shop="ironmonger", kind="hanging painted board on a forged bracket (the KCD2 frame's kind)",
         mount=dict(x_street_m=35.825, bay_end="door end (high street x)", viewer_side=side_word("west", 35.825, 30.0, 36.0), on="the brick above the cornice, over the pier at the door end of the bay",
                    plate_foot_m=3.60, plate_centre_m=3.75, arm_height_m=3.75, projection_m=0.70),
         parts=dict(board_m=[0.55, 0.38, 0.04], hang="two iron rings, then chains 0.70 m long (drop from the arm to the board's top 0.76 m); scroll bracket as the pawnbroker's but plainer", drop_m=0.76),
         faces=dict(text="KEYS CUT", font="old-standard-tt-bold", weight=700, cap_mm=92, tracking_em=0.08, colour="sign_black", ground="buff_board", shade=dict(colour="vermilion", d_mm=9),
                    border="black rule 6 mm inset 20 mm", note="both faces alike"),
         lowest_m=2.61, kind_of_number="Judgement", note="KEYS CUT: the ironmonger's key-cutting is in its window room (DECISIONS 7 Oct)."),
    dict(id="chandler_hanging_board", shop="chandler", kind="hanging painted board on a forged bracket",
         mount=dict(x_street_m=45.825, bay_end="door end (high street x)", viewer_side=side_word("east", 45.825, 40.0, 46.0), on="the brick above the cornice, over the pier at the door end of the bay",
                    plate_foot_m=3.60, plate_centre_m=3.75, arm_height_m=3.75, projection_m=0.90),
         parts=dict(board_m=[0.80, 0.50, 0.05], hang="two chains of four-link rings, 0.65 m longer than the first design (drop from the arm to the board's top 0.71 m)", drop_m=0.71),
         faces=dict(text="CHANDLERY", font="alfa-slab-one", weight=400, cap_mm=105, tracking_em=0.05, colour="white_paint", ground="navy", shade=dict(colour="shade_black", d_mm=10),
                    border="rope 10 mm inset 24 mm", note="both faces alike"),
         lowest_m=2.54, kind_of_number="Judgement", note="A word not on the fascia, so the street does not repeat itself."),
]
for _p in PROJECTING:
    _p["lowest_computed_m"] = None
    if "balls" in _p["parts"]:
        _p["lowest_computed_m"] = round(min(c[1] for c in _p["parts"]["balls"]["centres_m"]) - _p["parts"]["balls"]["diameter_m"] / 2, 3)
    elif "box_m" in _p["parts"]:
        _p["lowest_computed_m"] = round(_p["mount"]["arm_height_m"] - _p["parts"]["box_m"][1], 3)
    else:
        _p["lowest_computed_m"] = round(_p["mount"]["arm_height_m"] - _p["parts"]["drop_m"] - _p["parts"]["board_m"][1], 3)
    _p["clearance_below_m"] = _p["lowest_computed_m"]


def _g(shop, text, font, cap, technique, z, x, surface, source, kind, weight=None, **kw):
    d = dict(shop=shop, surface=surface, text=text, font=font, weight=weight, cap_mm=cap, technique=technique, z_m=z, x_street_m=x, tol_x_m=0.10, tol_z_m=0.03, source=source, kind=kind)
    d.update(kw)
    return d


_S = {s["id"]: s for s in SHOPS}
GLASS = [
    _g("mickeys", "0632 960418", "marcellus-sc", 170, "gold leaf with black shade 3 per cent of cap", 2.02, None, "window glass, inside face", "tools/art-recipes/shop-room.py lines 1455-1459 (EXISTS: another family's, not approved here)", "Read", existing=True),
    _g("mickeys", "MINICABS · 24 HOURS", "marcellus-sc", 85, "gold leaf with black shade", 1.82, None, "window glass, inside face", "shop-room.py (EXISTS: another family's; it contradicts the cast's hours for Mickey's, so not approved here)", "Read", existing=True),
    _g("mickeys", "1", "marcellus-sc", 110, "gold leaf, black shade", 2.18, _S["mickeys"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement"),
    _g("fish_market", "FRESH DAILY", "patrick-hand", 120, "whitewash brush lettering, uneven, 85 per cent opaque", 0.95, 12.0, "window glass", "Picture Sheffield t13138 (earlier note): window glass hand-lettered in white with the fish and offers", "Read"),
    _g("fish_market", "SHELLFISH", "patrick-hand", 100, "whitewash", 1.52, 13.0, "window glass", "as above", "Read"),
    _g("fish_market", "SMOKED FISH", "patrick-hand", 100, "whitewash", 2.02, 12.0, "window glass", "as above", "Read"),
    _g("fish_market", "3", "oswald", 110, "white paint, red shade", 2.18, _S["fish_market"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=600),
]
_rw = _S["ritas"]["window_centre_street_x_m"]
GLASS += [
    _g("ritas", "WATCHES", "old-standard-tt-bold", 90, "gold leaf, black shade 9 mm", 2.64, round(_rw + 1.117, 3), "toplight pane (viewer's left, high x)", "Judgement", "Judgement", weight=700),
    _g("ritas", "JEWELLERY", "old-standard-tt-bold", 90, "gold leaf, black shade 9 mm", 2.64, round(_rw, 3), "toplight pane (middle)", "Judgement", "Judgement", weight=700),
    _g("ritas", "LOANS", "old-standard-tt-bold", 90, "gold leaf, black shade 9 mm", 2.64, round(_rw - 1.117, 3), "toplight pane (viewer's right, low x)", "Judgement", "Judgement", weight=700),
    _g("ritas", "5", "abril-fatface", 110, "gold leaf, black shade", 2.18, _S["ritas"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement"),
    _g("empty_unit", "", "", 0, "whitewash wash, brush arcs, nothing legible (ruled 3 Oct: whole window whitewashed); the bills on it are the posters' family", None, None, "whole window", "DECISIONS.md 3 Oct", "Read"),
    _g("empty_unit", "7", "oswald", 110, "paint, flaking", 2.18, _S["empty_unit"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=600),
    _g("steam_laundry", "SERVICE WASHES", "jost", 80, "white cut vinyl", 2.05, round(_S["steam_laundry"]["window_centre_street_x_m"] + 0.6, 3), "window glass, upper left (viewer's left, high x)", "Judgement", "Judgement", weight=600),
    _g("steam_laundry", "9", "jost", 110, "white vinyl", 2.18, _S["steam_laundry"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=600),
    _g("grocer", "11", "josefin-sans", 110, "gold leaf", 2.18, _S["grocer"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=700),
    _g("newsagent", "TOBACCONIST & CONFECTIONER", "libre-franklin", 70, "white cut vinyl", 1.35, round(_S["newsagent"]["street_x_m"][1] - 1.8, 3), "shop-door glass (centre at the shop door, 1.8 m in from the door end)", "the review's fault 5: the trade moves from the fascia to the glass", "Judgement", weight=700),
    _g("newsagent", "18", "libre-franklin", 110, "cream vinyl", 2.18, _S["newsagent"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=700),
    _g("ironmonger", "EST. 1884", "old-standard-tt-bold", 60, "gold leaf, black shade 6 mm", 2.64, _S["ironmonger"]["window_centre_street_x_m"], "toplight pane, middle", "proposed year", "Judgement", weight=700),
    _g("ironmonger", "16", "old-standard-tt-bold", 110, "gold leaf", 2.18, _S["ironmonger"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=700),
    _g("tea_rooms", "14", "fraunces", 110, "cream vinyl", 2.18, _S["tea_rooms"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement", weight=900),
    _g("chandler", "EST. 1879", "alfa-slab-one", 60, "gold leaf, black shade 6 mm", 2.64, _S["chandler"]["window_centre_street_x_m"], "toplight pane, middle", "proposed year", "Judgement"),
    _g("chandler", "13", "alfa-slab-one", 110, "gold leaf", 2.18, _S["chandler"]["fanlight_street_x_m"], "side-door fanlight", "proposed number", "Judgement"),
]

HOURS_RULE = dict(pattern=r"^(MON|TUE|WED|THU|FRI|SAT|SUN|MON-SAT|MON-FRI)( [0-9]{1,2}(\.[0-9]{2})?)?(-[0-9]{1,2}(\.[0-9]{2})?)?( (OPEN|CLOSED))?$|^[0-9]{1,2}(\.[0-9]{2})?-[0-9]{1,2}(\.[0-9]{2})?$",
                  words=["OPEN", "CLOSED", "MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN", "MON-SAT", "MON-FRI"],
                  note="the hours plates' own rule (the review's note 11): lines made only of day names, times 'H' or 'H.MM' and a dash, set from hook-cast.json at build time; they are NOT in approved_words")
SMALL_PANELS = [
    dict(id="letting_board", shop="empty_unit", size_mm=[900, 450], centre_on_board_mm=[CX, 275], face="white", text="TO LET", font="libre-franklin", weight=800, cap_mm=130,
         colour="vinyl_red", fixing="four screws through the board, slightly askew (2 degrees); a rust run under each lower screw", exists="board_to_let.png (PT Sans); the font here is an OFL replacement, no agent and no number are minted",
         kind="Judgement"),
    dict(id="hours_plate", shops=["ritas", "fish_market", "steam_laundry", "newsagent", "tea_rooms"], size_mm=[300, 190],
         where="on the shop door's glass or the pilaster, centre 1.45 m up",
         text_rule="read the shop's hours from production/specs/hook-cast.json (Mon-Sat from 'hours', Sunday where it has one) and set them as 'MON-SAT 9-5.30' lines; Wednesday half-day as its own line where the cast has one",
         rule=HOURS_RULE,
         font="libre-franklin", weight=700, cap_mm=24, technique="white enamel plate, black letters, blue border 4 mm, rolled edge 3 mm, chips to black iron at the corners",
         kind="Judgement", note="The hours are the town's; the target gives the plate, not the words."),
]

# --------------------------------------------------------------------------------------------
# 6. Photo-measured template and Hook-sheet numbers (the main photograph is P1).
#    P1's saved preview now holds only the two END crops of the board (numerals, keyline corner, field):
#    the name and the bar's window lettering are not kept (the content rule; the review's fault 13).
#    The name's own numbers were measured on the unmasked rectified view on 8 Oct and are recorded here.
# --------------------------------------------------------------------------------------------
P1 = dict(
    id="P1", file="P1-leadenhall-board-elevation.jpg",
    what="Poly Haven 'Leadenhall Market' (CC0, Andreas Mischok, taken 2019-05-19), 16K panorama as the 8192 x 4096 tone-mapped JPG, a rectilinear view 110 degrees wide at yaw 90, pitch 0 (3600 x 2400), so a level, square-on elevation of the heritage-restored fronts. Used for the craft only: board proportions, letter height, keyline, shade, numerals. A real business's name stands on the board and in the windows and is NEVER copied; the saved preview shows only the two ends of the board (numerals, keyline corners) and nothing that names a business or shows drink.",
    view=dict(yaw_deg=90, pitch_deg=0, hfov_deg=110, size_px=[3600, 2400], horizon_row_px=1200),
    # all in pixels of that 3600 x 2400 view
    px=dict(field_top=179, field_bottom=326, field_left=1230, field_right=2418,
            keyline_top_y=190.5, keyline_bottom_y=311.0, keyline_left_x=1252.0, keyline_right_x=2396.0, keyline_px=[4, 3],
            cap_top=227.0, cap_bottom=272.0, text_x0=1492.0, text_x1=2123.0,
            numeral_left=[1277.0, 1354.0], numeral_right=[2271.0, 2350.0], numeral_top=229.0, numeral_bottom=270.0,
            shade_px=4.5, door_leaf_top=790.0, door_leaf_bottom=1482.0, base_row=1505.0, bead_top=154.0),
    measured_on_unmasked=["cap_top", "cap_bottom", "text_x0", "text_x1", "shade_px", "door_leaf_top", "door_leaf_bottom", "base_row", "bead_top"],
    re_measurable_on_preview=["field_top", "field_bottom", "keyline_top_y", "keyline_bottom_y", "keyline_left_x", "keyline_right_x", "numeral_left", "numeral_right", "numeral_top", "numeral_bottom"],
    preview=dict(file="P1-leadenhall-board-elevation.jpg", scale=2.2, gap_px=20,
                 crops_view_px=dict(left=[1150, 120, 1480, 400], right=[2250, 120, 2440, 400]),
                 note="a composite of two crops of the unmasked view, the board's left end and right end, at 2.2 x; the name (x 1492 to 2123) lies between them and is not kept"),
    scale_note="scale fitted on ONE dimension: the door leaf (692 px) taken as 2.1 to 2.3 m gives 3.03 to 3.32 mm/px, so the lettered field (147 px) is 0.45 to 0.49 m; the panorama's camera height would have to be 0.93 m for that, which is low but not impossible for a pole-mounted rig; every ratio below is scale-free. The door-leaf preview that showed this was removed (it showed a bar's lettering); the door leaf's rows are recorded in px (door_leaf_top, door_leaf_bottom, base_row) and are not re-measurable from any saved preview",
    error_px=3.0,
)
SHEET = dict(
    id="H1", file="H1-hook-sheet-mickeys-board-measure.jpg",
    what="production/reference/hook-sheet.png (2048 x 1088; image-model sheet, approved for mood, palette and composition; photographs win where they disagree)",
    px=dict(board_top=500, board_bottom=548, letters_top=513, letters_bottom=546, letters_x0=630, letters_x1=746, board_left=302, board_right=813),
    colours=dict(board_mean=[62, 75, 87], board_p10=[48, 60, 70], board_p90=[80, 91, 102], gilt_mean=[167, 149, 109], gilt_p90=[193, 171, 130],
                 white_board=[204, 204, 204], dark_board=[99, 81, 72], cream_board=[128, 101, 98]),
    ratios=dict(cap_over_board=round(33 / 48, 3), width_over_cap=round(116 / 33, 2), letter_centre_along_board=round((688 - 302) / (813 - 302), 3)),
    note="the sheet's board is seen obliquely round a bay window, so only vertical ratios and colours are used; its lettering is the one the sheet has, nothing else on it is legible. The sheet's WHITE fascia beside Mickey's is now used (it is the fish board's ground).",
)
PLANKS = dict(
    blue=dict(id="P2", file="P2-bluepaintedplanks-weathering-measure.jpg", what="Poly Haven 'Blue Painted Planks' (CC0, Rob Tuytel, published 2018-07-20), 2K diffuse, 1.0 m square at 0.488 mm/px: flaking paint on weathered timber cladding, a harder environment than a fascia",
              loss_fraction=0.286, patch_eqd_mm_p50=8.9, patch_eqd_mm_p90=17.4, aspect_p50=3.6, aspect_p90=6.7, largest_patch_mm=[577, 88], paint_rgb=[97, 116, 120], exposed_rgb=[64, 78, 69], n_patches=444),
    black=dict(id="P3", file="P3-blackpaintedplanks-scuff-measure.jpg", what="Poly Haven 'Black Painted Planks' (CC0, Dimitrios Savva, published 2025-10-15), 2K diffuse, 1.6 m square: worn black gloss, scuffs and abrasion",
               L_median=8.0, L_p95=21.9, scuff_area_fraction_dL8=0.0907, median_rgb=[21, 23, 29]),
    scaling="a fascia under its cornice, repainted every few years, loses a fraction of these: class 1 (sound) 0.1 x, class 2 (tired) 0.2-0.3 x, class 3 (neglected) 0.6 x of P2's 0.286; the SHAPE of a loss (elongated along the grain, median aspect 3.6, equivalent diameter 9 mm median) is photographed, the AMOUNT is Judgement",
)

# --------------------------------------------------------------------------------------------
# 7. Compute: ink boxes, shapes, contrast, distinctness, approved words, checks.
# --------------------------------------------------------------------------------------------
def cutcorner(x0, y0, x1, y1, r, n=10):
    """Closed polyline of a rectangle whose four corners are cut by CONCAVE quarter circles
    centred on the corners (the Leadenhall keyline's shape)."""
    pts = []

    def arc(cx, cy, a0, a1):
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)))
    arc(x1, y0, 180, 90)
    arc(x1, y1, 270, 180)
    arc(x0, y1, 360, 270)
    arc(x0, y0, 90, 0)
    pts.append(pts[0])
    return pts


def rect_pts(x0, y0, x1, y1):
    return [(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)]


def rounded_rect_pts(x0, y0, x1, y1, r, n=8):
    pts = []

    def arc(cx, cy, a0, a1):
        for i in range(n + 1):
            a = math.radians(a0 + (a1 - a0) * i / n)
            pts.append((round(cx + r * math.cos(a), 2), round(cy + r * math.sin(a), 2)))
    arc(x1 - r, y0 + r, -90, 0)
    arc(x1 - r, y1 - r, 0, 90)
    arc(x0 + r, y1 - r, 90, 180)
    arc(x0 + r, y0 + r, 180, 270)
    pts.append(pts[0])
    return pts


def shapes_for(s):
    sh = []
    if s.get("old_board"):
        sh.append(dict(kind="rect", role="old_board", colour=s["old_board"]["colour"], box=s["old_board"]["box_mm"]))
    b = s["border"]
    if not b:
        return sh
    k = b["kind"]
    if k == "rules":
        for r in b["rules"]:
            sh.append(dict(kind="rect", role="rule", colour=r["colour"], box=[r["x_mm"][0], r["y_mm"][0], r["x_mm"][1], r["y_mm"][1]]))
    elif k == "cutcorner_panel":
        i = b["inset_mm"]
        x0, y0, x1, y1 = FIELD[0] + i, FIELD[1] + i, FIELD[2] - i, FIELD[3] - i
        sh.append(dict(kind="polyline", role="keyline", colour=b["colour"], width_mm=b["line_mm"], pts=cutcorner(x0, y0, x1, y1, b["radius_mm"])))
        if b["inner_line_mm"]:
            d = b["line_mm"] / 2 + b["gap_mm"] + b["inner_line_mm"] / 2
            sh.append(dict(kind="polyline", role="keyline_inner", colour=b["colour"], width_mm=b["inner_line_mm"],
                           pts=cutcorner(x0 + d, y0 + d, x1 - d, y1 - d, b["radius_mm"] - d)))
        b["panel_mm"] = [x0, y0, x1, y1]
    elif k in ("box", "flat_panel"):
        ox0, oy0, ox1, oy1 = b["outer_mm"]
        f = b["frame_mm"]
        sh.append(dict(kind="rect", role="box_frame", colour=b["colour"], box=[ox0, oy0, ox1, oy1]))
        sh.append(dict(kind="rect", role="box_face", colour=b["face_colour"], box=[ox0 + f, oy0 + f, ox1 - f, oy1 - f]))
        for p in b.get("panels", []):
            sh.append(dict(kind="rect", role="vinyl_panel", colour=p["colour"], box=p["box_mm"]))
        for r in b.get("rules", []):
            sh.append(dict(kind="rect", role="rule", colour=r["colour"], box=[r["x_mm"][0], r["y_mm"][0], r["x_mm"][1], r["y_mm"][1]]))
        b["face_mm"] = [ox0 + f, oy0 + f, ox1 - f, oy1 - f]
    elif k == "glass_slab":
        ox0, oy0, ox1, oy1 = b["outer_mm"]
        e = b["edge_mm"]
        sh.append(dict(kind="rect", role="slab_edge", colour=b["colour"], box=[ox0, oy0, ox1, oy1]))
        sh.append(dict(kind="rect", role="slab_face", colour="deco_green_glass", box=[ox0 + e, oy0 + e, ox1 - e, oy1 - e]))
        for jx in b["joints_x_mm"]:
            sh.append(dict(kind="rect", role="slab_joint", colour="mastic", box=[jx - b["joint_mm"] / 2.0, oy0 + e, jx + b["joint_mm"] / 2.0, oy1 - e]))
        for y in b["speed_lines"]["y_mm"]:
            lm = b["speed_lines"]["line_mm"]
            for xr in (b["speed_lines"]["x_left_mm"], b["speed_lines"]["x_right_mm"]):
                sh.append(dict(kind="rect", role="speed_line", colour=b["colour"], box=[xr[0], y - lm / 2, xr[1], y + lm / 2]))
        b["face_mm"] = [ox0 + e, oy0 + e, ox1 - e, oy1 - e]
    elif k == "double_rule":
        i = b["inset_mm"]
        x0, y0, x1, y1 = FIELD[0] + i, FIELD[1] + i, FIELD[2] - i, FIELD[3] - i
        sh.append(dict(kind="polyline", role="rule_outer", colour=b["colour"], width_mm=b["line_mm"], pts=rect_pts(x0, y0, x1, y1)))
        d = b["line_mm"] / 2 + b["inner_gap_mm"] + b["inner_line_mm"] / 2
        sh.append(dict(kind="polyline", role="rule_inner", colour=b["inner_colour"], width_mm=b["inner_line_mm"], pts=rect_pts(x0 + d, y0 + d, x1 - d, y1 - d)))
        cb = b["corner_block_mm"]
        for (cx, cy) in ((x0, y0), (x1, y0), (x1, y1), (x0, y1)):
            sh.append(dict(kind="rect", role="corner_block", colour=b["colour"], box=[cx - cb / 2, cy - cb / 2, cx + cb / 2, cy + cb / 2]))
        b["panel_mm"] = [x0 + d, y0 + d, x1 - d, y1 - d]
    elif k == "rope":
        i = b["inset_mm"]
        x0, y0, x1, y1 = FIELD[0] + i, FIELD[1] + i, FIELD[2] - i, FIELD[3] - i
        sh.append(dict(kind="polyline", role="rope", colour=b["colour"], width_mm=b["rope_mm"], twist_pitch_mm=b["pitch_mm"], pts=rounded_rect_pts(x0, y0, x1, y1, b["corner_radius_mm"])))
        b["panel_mm"] = [x0 + b["rope_mm"], y0 + b["rope_mm"], x1 - b["rope_mm"], y1 - b["rope_mm"]]
    return sh


def compute_shop(s):
    g = PALETTE[s["ground"]["colour"]]
    ground_for_contrast = g["srgb_1990"]
    out_blocks = []
    for b in s["blocks"]:
        gfc = ground_for_contrast
        region = None
        if s["border"] and s["border"]["kind"] in ("box", "flat_panel"):
            gfc = PALETTE[s["border"]["face_colour"]]["srgb_1990"]
            for p in s["border"].get("panels", []):
                bx = p["box_mm"]
                if bx[0] <= b["x_mm"] <= bx[2] and not b["ghost"] and b["role"] == "trade":
                    gfc = PALETTE[p["colour"]]["srgb_1990"]
                    region = [bx[0] + 2, bx[1] + 2, bx[2] - 2, bx[3] - 2]
        box, size = measure(b["font"], b["weight"], b["text"], b["cap_mm"], b["tracking_em"])
        x0r, ybr, x1r, ytr = box
        if b["anchor"] == "centre":
            ox = b["x_mm"] - (x0r + x1r) / 2
        elif b["anchor"] == "left":
            ox = b["x_mm"] - x0r
        else:
            ox = b["x_mm"] - x1r
        ink = [round(ox + x0r, 1), round(b["baseline_mm"] + ybr, 1), round(ox + x1r, 1), round(b["baseline_mm"] + ytr, 1)]
        if b.get("embolden_mm"):
            e_ = b["embolden_mm"]
            ink = [round(ink[0] - e_, 1), round(ink[1] - e_, 1), round(ink[2] + e_, 1), round(ink[3] + e_, 1)]
        eff = list(ink)
        if b["shade"]:
            d = b["shade"]["d_mm"]
            eff[2] += d
            eff[1] -= d
        j = b["jitter"]
        if j:
            m = j["baseline_mm"] + 0.01 * (ink[2] - ink[0]) * j["advance_pct"] / 1.5
            eff = [eff[0] - m, eff[1] - j["baseline_mm"], eff[2] + m, eff[3] + j["baseline_mm"]]
        face = b["face_rgb"] if b.get("face_rgb") else PALETTE[b["face"]]["srgb_1990"]
        cr = contrast(face, gfc)
        out_blocks.append(dict(b, ink_box_mm=ink, effects_box_mm=[round(v, 1) for v in eff], width_mm=round(ink[2] - ink[0], 1),
                               size_px_per_em=round(size, 2), cap_ratio=round(cap_ratio(b["font"], b["weight"]), 4),
                               contrast_1990=round(cr, 2), face_1990=list(face), ground_1990=list(gfc),
                               origin_x_mm=round(ox, 1), cap_over_field=round(b["cap_mm"] / (FIELD[3] - FIELD[1]), 3), region_mm=region))
    s2 = dict(s)
    s2["blocks"] = out_blocks
    s2["shapes"] = shapes_for(s2)
    # geometry: Mickey's letters
    for gpart in s2["geometry"]:
        if gpart["kind"] == "applied_letters":
            nb = [b for b in out_blocks if b["id"] == "name"][0]
            gpart["blender_text_size_m"] = round(gpart["cap_m"] / nb["cap_ratio"], 4)
            gpart["bbox_board_mm"] = nb["ink_box_mm"]
            gpart["width_mm"] = nb["width_mm"]
    if s2.get("ghost") and s2["ghost"].get("pinholes") and s2["ghost"]["kind"] == "older_lettering":
        gb = [b for b in out_blocks if b["ghost"]][0]
        n = s2["ghost"]["pinholes"]
        x0, y0, x1, y1 = gb["ink_box_mm"]
        s2["ghost"]["pinhole_positions_mm"] = [[round(x0 + (i + 0.5) * (x1 - x0) / n, 1), round(gb["baseline_mm"] + gb["cap_mm"], 1)] for i in range(n)]
    return s2


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


SHOPS_C = [compute_shop(s) for s in SHOPS]
for s in SHOPS_C:
    bl = [b for b in s["blocks"] if not b["ghost"]]
    s["overlaps"] = [[a["id"], b["id"]] for i, a in enumerate(bl) for b in bl[i + 1:] if overlap(a["effects_box_mm"], b["effects_box_mm"])]
    s["min_margin_mm"] = None
    if bl:
        m = []
        for b in bl:
            e = b["effects_box_mm"]
            m += [e[0] - SAFE[0], e[1] - SAFE[1], SAFE[2] - e[2], SAFE[3] - e[3]]
        s["min_margin_mm"] = round(min(m), 1)
        main = [b for b in bl if b["role"] == "name"][0]
        s["name_fill_of_field_height"] = main["cap_over_field"]
        s["name_width_of_board"] = round(main["width_mm"] / BOARD_W, 3)

# approved words: every string that may appear on any fascia, glass, panel, projecting sign (exact strings)
APPROVED = set()
GHOST_WORDS = set()
for s in SHOPS_C:
    for b in s["blocks"]:
        (GHOST_WORDS if b["ghost"] else APPROVED).add(b["text"])
for p in PROJECTING:
    if "faces" in p:
        APPROVED.add(p["faces"]["text"])
EXISTING_NOT_APPROVED = []
for g in GLASS:
    if g["text"]:
        if g.get("existing"):
            EXISTING_NOT_APPROVED.append(g["text"])
        else:
            APPROVED.add(g["text"])
for sp in SMALL_PANELS:
    if sp["id"] == "letting_board":
        APPROVED.add(sp["text"])
APPROVED |= GHOST_WORDS
APPROVED.discard("")
APPROVED_PARTS = sorted({w for t in APPROVED for w in re.split(r"[\s·,]+", t) if w})

FORBIDDEN = dict(
    alcohol_gambling_children=["ALE", "BEER", "WINE", "LAGER", "SPIRITS", "WHISKY", "GIN", "BAR", "PUB", "INN", "TAVERN", "OFF-LICENCE", "BET", "BETS", "BETTING", "BOOKMAKER", "POOLS", "BINGO", "LOTTERY", "CASINO", "ARCADE", "COCKTAIL", "RESTAURANT", "CHILD", "CHILDREN", "KIDS", "SCHOOL", "TOYS"],
    real_marks=["ROYAL MAIL", "POST OFFICE", "TELECOM", "BT", "ER", "TESCO", "SAINSBURY", "BOOTS", "WOOLWORTHS", "WH SMITH", "MARLBORO", "SILK CUT", "PERSIL", "TIDE", "OMO"],
    names_not_minted=["CHAMBERLAIN", "BARBOUR", "REISS", "LUC", "PIZZA", "EXPRESS"],
    note="the last list is the real business names on the measured photograph P1: they may never appear on any fascia; the first two lists are the content rule and the brand rule; production/specs and ledger/Assets/Scripts/Core/RealWorld.cs hold the full real-world list the gate checks",
)

# distinctness
pairs = []
for i in range(len(SHOPS_C)):
    for j in range(i + 1, len(SHOPS_C)):
        a, b = SHOPS_C[i], SHOPS_C[j]

        def gnd(x):
            if x["border"] and x["border"]["kind"] in ("box", "flat_panel"):
                return PALETTE[x["border"]["face_colour"]]["srgb_1990"]
            return PALETTE[x["ground"]["colour"]]["srgb_1990"]

        def main_(x):
            nb = [bb for bb in x["blocks"] if bb["role"] == "name" and not bb["ghost"]]
            return nb[0] if nb else None
        ma, mb = main_(a), main_(b)
        fa, fb = (ma["font"] if ma else None), (mb["font"] if mb else None)
        fca = (ma["face_rgb"] or PALETTE[ma["face"]]["srgb_1990"]) if ma else None
        fcb = (mb["face_rgb"] or PALETTE[mb["face"]]["srgb_1990"]) if mb else None
        face_dE = round(dE(fca, fcb), 1) if fca and fcb else None
        pairs.append(dict(a=a["id"], b=b["id"], ground_dE=round(dE(gnd(a), gnd(b)), 1), same_font=(fa is not None and fa == fb),
                          same_construction=a["construction_kind"] == b["construction_kind"], face_dE=face_dE,
                          same_border=((a["border"] or {}).get("kind") == (b["border"] or {}).get("kind")),
                          same_layout=(a["layout_class"] == b["layout_class"] and a["layout_class"] != "none")))
CENTRED = ("centred_stack", "centred_stack_with_ends")
DISTINCT = dict(
    rule="every pair differs in aged ground by dE76 >= 14; no two fascias share a name-line font; two fascias of the same construction kind also differ in name-face colour by dE >= 25 or in border kind; and no more than five boards share the centred name-over-trade skeleton",
    min_ground_dE=min(p["ground_dE"] for p in pairs), pairs=pairs,
    violations=[p for p in pairs if p["ground_dE"] < 14 or p["same_font"] or (p["same_construction"] and p["face_dE"] is not None and p["face_dE"] < 25 and p["same_border"])],
    centred_skeleton_boards=[s["id"] for s in SHOPS_C if s["layout_class"] in CENTRED],
    dotted_trade_lines=[b["id"] + "@" + s["id"] for s in SHOPS_C for b in s["blocks"] if b["role"] == "trade" and " · " in b["text"]],
    layout_classes={s["id"]: s["layout_class"] for s in SHOPS_C},
)

TEXTURES = dict(
    px_per_mm=1, size_px=[BOARD_W, BOARD_H], alt_px_per_mm=2,
    engine_note="5410 x 550 is not a power of two. From memory (NOT checked in the installed 5.8.2 source, which is not on this machine; RULINGS 8 Oct wants file and line): Unreal gives such a texture no mips unless it is padded or stretched at import, and thin letters would then shimmer from the hook camera. The builder checks this FIRST in the 5.8.2 source. If confirmed: either pad to 8192 x 1024 (the render in the top-left 5410 x 550; u 0 to 0.6604, v 0 to 0.5371) or stretch to 5120 x 512 (a 1.7 per cent aspect error, invisible). The automatic checks run on the authored 5410 x 550 render before any packing.",
    maps=[dict(id="base_colour", encoding="sRGB 8-bit", note="paint, gilt, vinyl and glass colours, aged; NO baked frame highlight or shade (the review's fault 11): the cornice's shadow is Unreal's"),
          dict(id="roughness", encoding="linear 8-bit, 0-1", note="per layer values in each shop's ground and block 'technique'; gilt 0.25-0.40, gloss paint 0.35-0.6, chalked 0.6-0.8, acrylic 0.35, glass 0.05-0.10, vinyl 0.45"),
          dict(id="metallic", encoding="linear 8-bit 0 or 1", note="1 on gold leaf, chrome strips and bronze frame; 0 elsewhere (gilt paint on the balls 0.8)"),
          dict(id="height", encoding="8-bit, 128 = board face, 0.01 mm per step (range -1.28 to +1.27 mm)",
               note="letter paint ridge +0.20, keyline +0.15, vinyl +0.08, gilt +0.05, paint loss -0.30 (bare board -0.50), planted moulding +0.60 with a 4 mm chamfer, chrome strips and speed lines +0.80, slab joints -0.50, slab bevels a 2 mm ramp to -0.3. NO relief of 3 mm or more: boxes, panels, Mickey's letters and the hanging signs are geometry (section geometry)"),
          dict(id="emissive", encoding="sRGB 8-bit, only where lit", note="steam_laundry and newsagent only (their box faces): face colour x level; tube rows, tube-end shadows, the dead tube (steam_laundry)"),
          dict(id="layers_manifest", encoding="JSON", note="the renderer writes, per text block, the string, font, size, anchor, ink box and colours it drew, and for each ghost its string: the word checks read it, and the position and mask checks read the PIXELS against it")],
)

# ------------------------------------------------------------------------------------------
# 8. The checks unit 4.1's automatic check runs. 'reads' says what each reads: pixels (the rendered
#    base-colour and maps), manifest, geometry (the placed objects), font (re-rendered from the file).
# ------------------------------------------------------------------------------------------
CHECKS = []


def chk(id_, name, scope, measure_, expected, tol, unit, method, reads="pixels", why=""):
    CHECKS.append(dict(id=id_, name=name, scope=scope, reads=reads, layer=reads, measure=measure_, expected=expected, tolerance=tol, unit=unit, method=method, why=why))


chk("G1", "texture size", "every fascia", "width and height of the base-colour image", [BOARD_W, BOARD_H], 0, "px at 1 px/mm (double at 2)", "image size", "pixels",
    "the board is the kit's 5.41 x 0.55 m; one pixel is one millimetre so a letter's height in pixels is its height in mm")
chk("G2", "planted moulding", "ritas, ironmonger, chandler only", "the HEIGHT MAP: the outer 24 mm ring against the field just inside it, and the chamfer's width", dict(step_mm=0.6, chamfer_mm=4, elsewhere="no step: |height difference| < 0.1 mm on every other board"), dict(step_mm=0.15, chamfer_mm=2), "mm",
    "mean height of the ring minus mean height of the 24 mm band inside it; ramp width at the inner edge", "pixels",
    "the kit's board is a plain box; where a board has a planted moulding it is relief, not a baked highlight (the review's fault 11)")
chk("G3", "no repeated word", "every fascia", "each string of the layers manifest appears once per board; no two ink boxes on one board have the same string", 1, 0, "count", "count strings in the manifest", "manifest",
    "the 3 Sept image-model fascia and the game's FRESH FISH FRESH FISH tiled twice (shop-fronts-whole-2026-10-08.jpg); a board is one picture, not a tile")
chk("G4", "words", "every fascia, glass, hanging-sign and panel layer", "every string in the manifest is in approved_words (exact) or, for an hours plate, matches hours_plate.rule; none in forbidden_patterns (case-insensitive, whole word); a ghost string only in a block whose role is 'ghost'", True, 0, "bool", "set test on the manifest", "manifest",
    "no proprietor name that is not minted; no real mark; the content rule")
chk("G5", "no tiling period", "every ground", "the ground's autocorrelation (text and border masked), at lags 600 to 5000 mm along the board", dict(max_peak=0.55), 0, "correlation", "FFT autocorrelation of L* of the ground only", "pixels",
    "a 5.4 m board must not read as a 1 m texture repeated")
chk("G6", "grain direction", "painted timber boards", "the ground's structure tensor, dominant orientation", dict(angle_deg_from_horizontal=[0, 8]), 0, "deg", "structure tensor on the ground's L* at 4 to 40 mm", "pixels",
    "boards are planed along their length; chips and paint loss follow the grain (P2: median aspect 3.6)")
chk("G7", "distinct fascias", "the ten boards together", "pairwise dE76 between the aged ground medians; shared name-line fonts; shared construction kinds", DISTINCT["rule"], 0, "rule", "see distinctness in target.json", "pixels",
    "so the street reads as ten owners, not one designer")
chk("G8", "contrast of every name line", "every text block", "WCAG contrast ratio between the median face colour and the median ground colour just outside the glyphs (a 4 mm ring beyond the shade)", "see each block's contrast_1990", "0.85 x nominal minimum", "ratio", "contrast of two medians", "pixels")
chk("G9", "relief present", "gilded, vinyl and painted blocks", "mean HEIGHT-MAP step across a glyph edge", dict(gilded_mm=[0.02, 0.15], vinyl_mm=[0.04, 0.2], painted_mm=[0.1, 0.35]), 0, "mm", "height map at glyph edges", "pixels",
    "Mickey's applied letters are not here: they are geometry (G17)")
chk("G10", "glyph mask against the font", "every text block in the texture, ghosts excepted", "re-render the block's string from its font file (font, weight and axes, size from the cap, tracking, anchor, origin) as a mask at the target position; compare it with the rendered face mask inside the block's box dilated 12 mm", dict(iou_min=0.85, flipped_iou_must_be_lower_by=0.15), 0, "IoU",
    "intersection over union of the two masks; and the same against the mask flipped about the block's centre line: the true mask must beat the flipped one by at least 0.15 unless the string is mirror-symmetric (listed in `symmetric_strings`)", "pixels+font",
    "this catches a mirrored board (the recipe has already painted MICKEY'S backwards once), a wrong font, a fallback glyph, a wrong word and a wrong place; the manifest alone cannot")
chk("G11", "layout variety", "the ten boards together", "layout_class of each board; the strings of the trade lines", dict(max_centred_skeleton_boards=5, max_dotted_trade_lines=3, min_distinct_layout_classes=6), 0, "count", "count from target.json's layout_class and the manifest", "manifest",
    "the review's fault 5: no more than five boards share a centred name over a trade line, no more than three trade lines use ' · '")
chk("G12", "hand jitter", "boards whose technique is painted or gilded", "the residual of each glyph's baseline (its measured bottom edge) from the block's straight baseline, SD over the block's glyphs", dict(painted_gilded_sd_mm=[0.6, 1.6], vinyl_applied_glass_sd_mm=[0.0, 0.6]), 0, "mm",
    "glyph-by-glyph bottom edge of flat-bottomed capitals, SD of the residual from a straight line", "pixels", "the review's fault 3")
chk("G13", "wear counts", "every board", "counts of rain runs, gull marks and rust runs in the wear layers (labelled blobs of the right colour and shape)", "each shop's age.runs.count, age.gull.count, age.rust.count", dict(count=1), "count", "label connected components of the wear masks", "pixels")
chk("G14", "ghosts", "mickeys, fish_market, ironmonger (older lettering); empty_unit and ritas (painted-out or repaint patches)", "the ghost block's presence at its position, its dE from the ground, the share of its strokes painted over, and that no OTHER legible string exists", dict(dE=[3, 5], text_only=True), 0, "dE76",
    "mask of the ghost string re-rendered from its font; median dE of the pixels under it against the ground; share of the mask covered by the overpaint; compare the rest with the manifest", "pixels+font",
    "ghost lettering carries trade words only, never a proprietor's name (canon; RULINGS 3 Oct)")
chk("G15", "projecting signs", "the four hanging signs", "the placed object: x, arm height, projection, lowest point, plate foot above the cornice top (3.55 m), and both faces' text reading left to right as seen from their own side", dict(x_street_m="each sign's mount", arm_height_m="each sign's mount", projection_m="each sign's mount", lowest_m_min=2.5, plate_foot_above_cornice_m=0.05), dict(x=0.02, z=0.02, projection=0.02), "m",
    "bounding boxes of the placed meshes; each face's texture checked with G10 against the face's own reading direction", "geometry+pixels")
chk("G16", "glass lettering", "every glass row not marked existing", "the glass layer: the string is in approved_words; cap height; z; and street x", "each row's text, cap_mm, z_m, x_street_m", dict(cap_rel=0.05, z_m=0.03, x_m=0.10), "mm / m",
    "G10 on the glass layer's mask (lettering on glass is in the glass material, not a decal: CLOSE-RANGE-2026-10-03 item 6)", "pixels+font")
chk("G17", "geometry parts", "mickeys letters; steam_laundry and newsagent boxes; tea_rooms panel", "the placed meshes: Mickey's letters' depth, cap and bounding-box centre over the door; each box's outer rectangle and depth; no letter geometry left in the Mickey's texture", dict(letters_depth_mm=14, letters_cap_mm=330, letters_centre_street_x_m=MK_DOOR, box_depth_mm="per geometry row"), dict(depth_mm=2, cap_mm=8, centre_m=0.05, box_mm=10, depth_box_mm=15), "mm / m",
    "bounding boxes in board coordinates; the texture's Mickey's name block count must be 0", "geometry",
    "the review's fault 2: a script must not paint a second set of letters under the recipe's raised ones")
chk("G18", "mirrored board", "every board", "any block whose x position matches the MIRRORED target (W - x) better than the true one", True, 0, "bool", "compare the pixel ink box's centre with x and with W - x (anchor centre) for every block", "pixels",
    "the axis fault of the review's fault 1: on a mirrored board the off-centre blocks (Mickey's ghost aside, the fish list, the laundry panel, the ironmonger's end stacks) land at the other end")
for s in SHOPS_C:
    sid = s["id"]
    g = PALETTE[s["ground"]["colour"]]
    gg = g["srgb_1990"]
    if s["border"] and s["border"]["kind"] in ("box", "flat_panel"):
        gg = PALETTE[s["border"]["face_colour"]]["srgb_1990"]
    chk(f"{sid}.ground", f"{sid}: ground colour", sid, "median sRGB of the ground mask (everything not text, border, ghost, shade, panel or box frame)", gg, 9.0, "dE76", "median in Lab then dE76 to the target", "pixels",
        f"{PALETTE[s['ground']['colour']]['plain']}")
    for b in s["blocks"]:
        bid = f"{sid}.{b['id']}"
        if b["ghost"]:
            chk(f"{bid}.ghost", f"{bid}: ghost lettering", sid, "G14 for this block", dict(string=b["text"], font=b["font"], cap_mm=b["cap_mm"], baseline_mm=b["baseline_mm"], centre_x_mm=b["x_mm"], dE=[3, 5], broken_fraction=b["broken_fraction"]), dict(pos_mm=15, cap_rel=0.05, broken=0.15), "mixed",
                "G14", "pixels+font")
            continue
        if not b["in_texture"]:
            chk(f"{bid}.geometry", f"{bid}: raised letters (geometry)", sid, "G17 for Mickey's letters: depth, cap, bounding box over the door", dict(depth_mm=14, cap_mm=b["cap_mm"], bbox_mm=b["ink_box_mm"], centre_street_x_m=MK_DOOR), dict(depth_mm=2, cap_mm=8, centre_m=0.05), "mm / m", "G17", "geometry")
            chk(f"{bid}.shadow", f"{bid}: contact shadow in the texture", sid, "mean L* in an 8 mm band under the letters' footprint against the board just outside it", dict(footprint_mm=b["ink_box_mm"], dL=[-9, -3]), 0, "L*", "L* of the shadow band minus L* of the ground ring", "pixels")
            continue
        chk(f"{bid}.cap", f"{bid}: cap height", sid, "height of the H-shaped capital (or the T of Tea Rooms) in the layers manifest, in mm; confirmed on the pixels", b["cap_mm"], max(2.0, round(0.03 * b["cap_mm"], 1)), "mm", "rows between the top of the flat-topped capitals and the baseline", "manifest+pixels")
        chk(f"{bid}.width", f"{bid}: ink width", sid, "width of the string's ink box on the PIXELS", b["width_mm"], round(max(6.0, 0.04 * b["width_mm"]), 1), "mm", "pixel ink box of the face mask", "pixels",
            "the font file's real advance widths with the tracking given; hand jitter adds up to 1.5 per cent")
        pos_x = b["x_mm"]
        chk(f"{bid}.pos", f"{bid}: position", sid, "ink box of the face mask READ ON THE PIXELS (pixels within dE 14 of the face colour inside the block's box dilated 40 mm): its centre (anchor centre) or its left or right edge (anchor left or right) in x, and its bottom edge in y",
            dict(anchor=b["anchor"], x_mm=pos_x, baseline_mm=b["baseline_mm"], ink_box_mm=b["ink_box_mm"]), dict(x_mm=15, baseline_mm=3), "mm", "pixel ink box; for round-bottomed strings the baseline is the median bottom of the flat-bottomed letters", "pixels",
            "the review's fault 3: a block at the wrong end, a trade line above its name, or a block 1 m off passed every old check")
        chk(f"{bid}.mask", f"{bid}: glyph mask", sid, "G10 for this block", dict(iou_min=0.85), 0, "IoU", "G10", "pixels+font")
        chk(f"{bid}.fit", f"{bid}: inside the safe zone", sid, "ink box including shade, outline and hand jitter against the safe rectangle", dict(safe_mm=SAFE, min_margin_mm=0), 0, "mm", "min distance from the box to each safe edge >= 0 (the safe rectangle already keeps 150 mm off the ends and 40 mm off the top and bottom)", "manifest")
        chk(f"{bid}.contrast", f"{bid}: contrast", sid, "WCAG ratio, aged face median to aged ground median", b["contrast_1990"], f"not below {round(0.85 * b['contrast_1990'], 2)} and not below 2.2", "ratio", "median face (glyph interior eroded 2 px) vs median ring", "pixels")
        chk(f"{bid}.face", f"{bid}: face colour", sid, "median sRGB of the glyph interior (eroded 2 px)", b["face_1990"], 14.0, "dE76", "median in Lab", "pixels")
        if b["shade"]:
            sc = PALETTE[b["shade"]["colour"]]["srgb_1990"]
            chk(f"{bid}.shade", f"{bid}: block shade", sid, "median colour of the pixels in the shade zone (the glyph shifted along the shade vector, minus the glyph) and the zone's width along (+1,-1)", dict(colour=sc, d_mm=b["shade"]["d_mm"]), dict(dE=16.0, d_mm=2.0), "dE76 / mm", "morphological difference of the manifest's glyph mask shifted by (d,-d)", "pixels",
                "sign-writer's block shade, 45 degrees down and to the right (P1: 4.5 px of a 45 px cap = 0.10 cap)")
        if b["jitter"]:
            chk(f"{bid}.jitter", f"{bid}: hand jitter", sid, "G12 for this block", dict(sd_mm=HAND["baseline_sd_mm"]), 0, "mm", "G12", "pixels")
    if s["border"]:
        chk(f"{sid}.border", f"{sid}: border / panel", sid, "the border's lines, found as the long thin features of colour as given, positions and widths", dict(kind=s["border"]["kind"], panel_mm=s["border"].get("panel_mm") or s["border"].get("face_mm")), 4.0, "mm", "line detection on the border colour mask; compare with the shapes in target.json", "pixels")
    if s.get("moulding"):
        chk(f"{sid}.moulding", f"{sid}: planted moulding", sid, "G2 for this board", s["moulding"], dict(step_mm=0.15, chamfer_mm=2), "mm", "G2", "pixels")
    a = s["age"]
    chk(f"{sid}.age", f"{sid}: paint loss", sid, "area of paint-loss pixels (the substrate or undercoat showing) over the board face; the median aspect of the loss patches (along/across)", dict(loss_fraction=a["loss_fraction"], aspect_median_min=2.0, eqd_mm_median=[4, 16]),
        dict(loss_fraction_abs=0.012, loss_fraction_rel=0.5), "fraction", "classify loss pixels by the substrate colour; label; measure", "pixels",
        "the shape is P2's (median aspect 3.6, equivalent diameter 9 mm); the amount is Judgement")
    chk(f"{sid}.wear", f"{sid}: rain runs, gull marks, rust", sid, "G13 for this board", dict(runs=a["runs"]["count"], gull=a["gull"]["count"], rust=a["rust"]["count"]), dict(count=1), "count", "G13", "pixels")
    if s.get("ghost") and s["ghost"]["kind"] in ("repaint_patch", "painted_out_patch"):
        chk(f"{sid}.ghost_patch", f"{sid}: {s['ghost']['kind'].replace('_', ' ')}", sid, "G14: the patch present in its box, its dE from the ground, NO legible string in it", dict(box_mm=s["ghost"]["box_mm"], dE=s["ghost"]["dE"], legible_text=False), dict(box_mm=15, dE=1.5), "mm / dE76", "G14", "pixels")
    if s["ghost"] and s["ghost"].get("pinholes"):
        chk(f"{sid}.pinholes", f"{sid}: pin holes", sid, "dark dots of 3 to 4 mm", dict(count=s["ghost"]["pinholes"], diameter_mm=[3, 4]), dict(count=1), "count", "label dark dots on the ground", "pixels")
    for gp in s["geometry"]:
        if gp["kind"] in ("box_sign", "flat_panel"):
            chk(f"{sid}.{gp['id']}", f"{sid}: {gp['kind']} geometry", sid, "G17: the placed mesh's outer rectangle in board coordinates and its depth", dict(outer_mm=gp["outer_mm"], depth_mm=round(gp["depth_m"] * 1000)), dict(box_mm=10, depth_mm=15), "mm", "bounding box of the mesh", "geometry")
    if s["lit"] == "tubes":
        e = [gp for gp in s["geometry"] if gp["kind"] == "box_sign"][0]["emissive"]
        chk(f"{sid}.emissive", f"{sid}: lit face", sid, "emissive map: face coverage; tube rows; tube-end shadows; the dead tube",
            dict(face_mm=e["face_mm"], row_band_pct=e["row_band_pct"], tube_end_shadow=e["tube_end_shadow"], tube_joints_x_mm=e["tube_joints_x_mm"], dead_tube=e["dead_tube"], face_coverage=0.97), dict(level_pct=5, x_mm=60), "fraction", "emissive map statistics along each tube row", "pixels",
            "the review's fault 12: a dead tube darkens ONE ROW over ONE TUBE's length, to 60 per cent because the other row still lights it")
for p in PROJECTING:
    chk(f"{p['id']}.mount", f"{p['id']}: mount", p["shop"], "G15: x, arm height, projection and lowest point of the placed hanging sign", dict(x_street_m=p["mount"]["x_street_m"], arm_height_m=p["mount"]["arm_height_m"], projection_m=p["mount"]["projection_m"], lowest_m=p["lowest_computed_m"], viewer_side=p["mount"]["viewer_side"]), dict(x=0.02, z=0.02, projection=0.02), "m", "G15", "geometry")
    chk(f"{p['id']}.faces", f"{p['id']}: faces", p["shop"], "G15/G10: both faces' lettering reads left to right from its own side", dict(text=p["faces"]["text"] if "faces" in p else None), 0, "IoU", "G10 on each face's texture, the second face's reading direction reversed", "pixels+font")
for i_, g in enumerate(GLASS):
    if g["text"] and not g.get("existing"):
        chk(f"{g['shop']}.glass.{i_}", f"{g['shop']}: glass '{g['text']}'", g["shop"], "G16 for this row", dict(text=g["text"], cap_mm=g["cap_mm"], z_m=g["z_m"], x_street_m=g["x_street_m"], font=g["font"]), dict(cap_rel=0.05, z_m=0.03, x_m=0.10), "mm / m", "G16", "pixels+font")
chk("rita.lit", "ritas: the board is not lit at night", "ritas", "the board has no emissive; only the window is ruled lit (DECISIONS 1 Oct)", True, 0, "bool", "emissive map absent or zero", "pixels")
chk("letting_board", "the letting board", "empty_unit", "the board's string TO LET, size 900 x 450, centre on the board", dict(text="TO LET", size_mm=[900, 450], centre_mm=[CX, 275]), dict(pos_mm=15), "mm", "G10 on the board's texture; bounding box", "pixels+font")
chk("hours_plates", "hours plates", "ritas, fish_market, steam_laundry, newsagent, tea_rooms", "every line on the plate matches hours_plate.rule; the plate is 300 x 190 mm centred 1.45 m up", HOURS_RULE["pattern"], 0, "regex", "string test on the manifest", "manifest")

# ------------------------------------------------------------------------------------------
# 9. Assemble target.json
# ------------------------------------------------------------------------------------------
import hashlib


def ofl_text(d):
    p = os.path.join(FONT_DIR, d, "OFL.txt")
    return open(p, encoding="utf-8", errors="replace").read() if os.path.exists(p) else None


def ofl_hash(d):
    t = ofl_text(d)
    return hashlib.sha256(t.encode("utf-8")).hexdigest()[:16] if t else None


def ofl_rfn(d, fallback):
    t = ofl_text(d)
    if not t:
        return fallback
    head = " ".join(t.splitlines()[:14])
    m = re.search(r'Reserved Font Names?\s+(.*?)(?:\s{2,}|\. |$)', head)
    if not m:
        return None
    return m.group(1).strip().strip('"').replace('" and "', ", ").replace('"', "")


FONT_ROWS = {}
for k, v in FONTS.items():
    FONT_ROWS[k] = dict(
        family=v["family"], file_in_google_fonts_repo=f"ofl/{v['dir']}/{v['file']}",
        ofl_url=f"https://raw.githubusercontent.com/google/fonts/main/ofl/{v['dir']}/OFL.txt", ofl_read="8 Oct 2026, whole file, header 'SIL OPEN FONT LICENSE Version 1.1'",
        ofl_sha256_16=ofl_hash(v["dir"]), designer=v["designer"], reserved_font_name=ofl_rfn(v["dir"], v["rfn"]),
        rendering_note="letters are RENDERED into pictures; the OFL puts no restriction on a picture made with the font (earlier note FAQ 1.1/1.13); never modify and redistribute the font file itself",
        in_production_fonts=v["in_repo"], looks_like=v["looks_like"], axes=v["axes"] or None)
FONT_ROWS["patrick-hand"] = dict(family="Patrick Hand", file_in_production_fonts="production/fonts/patrick-hand/PatrickHand-Regular.ttf", ofl="production/fonts/patrick-hand/OFL.txt",
                                 looks_like="neat hand printing; stands in for the fishmonger's whitewash hand with the jitter given in the glass rows")
FONT_ROWS["_not_used"] = dict(overpass="Overpass is the American Highway Gothic and is NOT to be used (asset plan note 0)",
                              dropped="Libre Baskerville (the ironmonger's face in the first draft) is replaced by Old Standard TT Bold, which note 4 lists for old fascias",
                              not_ofl="no Apache or GPL font (Special Elite, Gillius ADF), and no Transport, Gill Sans, Futura, Helvetica or Franklin file: Jost, Libre Franklin and Oswald are the OFL stand-ins")

SOURCES = [
    dict(id="P1", url="https://api.polyhaven.com/files/leadenhall_market  (tone-mapped JPG at https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/leadenhall_market.jpg)", read="2026-10-08",
         author="Andreas Mischok (Poly Haven)", licence="CC0 1.0 (polyhaven.com/license: 'CC0 means absolute freedom')", taken="2019-05-19 (api info date_taken 1558277880)",
         shows="a covered City of London arcade, heritage-restored: red boards, gilt shaded capitals, numbers at both ends, cut-corner keylines. A real business's name is on the board and its windows show a bar's lettering; NEITHER is kept in any preview and the name is never copied.",
         period="NOT 1990: 2019 and restored, so used for the craft (proportions, letter height, keyline, shade) and never for colour or wear",
         used=True, what_used="fascia board proportions; keyline inset, thickness and corner; cap height over field; block shade; numerals; tracking. Measured on a rectilinear view of the panorama.", preview="P1-leadenhall-board-elevation.jpg (the two ends of the board only) and P1-leadenhall-board-target-on-photo.jpg"),
    dict(id="P2", url="https://polyhaven.com/a/blue_painted_planks (file: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/blue_painted_planks/blue_painted_planks_diff_2k.jpg)", read="2026-10-08",
         author="Rob Tuytel (Poly Haven)", licence="CC0 1.0", taken="published 2018-07-20; photograph date not given",
         shows="weathered blue-painted timber cladding, 1.0 m square, flaking paint, exposed grain", period="undated; weathering, not a fascia",
         used=True, what_used="shape and size of paint-loss patches (elongation along the grain, equivalent diameter), the loss fraction as an UPPER bound", preview="P2-bluepaintedplanks-weathering-measure.jpg"),
    dict(id="P3", url="https://polyhaven.com/a/black_painted_planks", read="2026-10-08", author="Dimitrios Savva (Poly Haven)", licence="CC0 1.0", taken="published 2025-10-15",
         shows="black gloss-painted planks, scuffed and abraded, 1.6 m", period="undated", used=True, what_used="scuff fraction and the luminance range of a worn dark gloss", preview="P3-blackpaintedplanks-scuff-measure.jpg"),
    dict(id="H1", url="production/reference/hook-sheet.png (preview production/previews/hook-sheet-2026-10-05.jpg)", read="2026-10-08", author="the project's image lane (generated)", licence="own work, approved 21 Sep and 5 Oct for mood, palette and composition",
         taken="2026-09 / 10-05", shows="Mickey's slate-blue board with standing gilt capitals, three more fascias (white, dark aubergine, cream)", period="a generated picture of 1990, not a photograph",
         used=True, what_used="Mickey's board and letter colours (measured), cap height over board, lettering over the door, the white fascia beside it (the fish board's ground)", preview="H1-hook-sheet-mickeys-board-measure.jpg"),
    dict(id="G1", url="production/previews/proof-2.6-shop-signs-and-bills-2026-10-04.jpg, shop-fronts-whole-2026-10-08.jpg and morning-hook-day-2026-10-08.jpg", read="2026-10-08", author="the project's packaged builds", licence="own work", taken="4 and 8 Oct 2026",
         shows="how the fascias stand in the game today, and which way round the street is: low street x on the viewer's right on the east parade", period="game", used=True, what_used="TARGET.md section 2 and the axis", preview=None),
    dict(id="R1", url="tools/art-recipes/terrace-front.py (lines 560, 837-892, 2127-2180, 7925-7945, 8273 and 8455-8480, 6600-6620)", read="2026-10-08", author="the project", licence="own work", taken="n/a",
         shows="BAY_DOORS_ON; SIGN_OVERRIDE; RAISED_LETTERS; the half turn of the west blocks; the export's y-reflection ('mirror') and the lettered faces' UVs 'reader's left to reader's right'", period="n/a", used=True, what_used="the axis and the door ends", preview=None),
    dict(id="N1", url="production/research/asset-plan/4-SIGNAGE-AND-WEAR.md; 0-SOURCES-AND-LICENCES.md; SUMMARY.md s.7", read="2026-10-08 (written 2026-10-03)", author="project research helper", licence="own work", taken="2026-10-03",
         shows="the font table, the trades' type, the three generations of 1990 fascia (painted, backlit Perspex, cut vinyl), the proof plan", period="1990", used=True, what_used="font choices, the generation mix", preview=None),
    dict(id="N2", url="production/research/shop-window-interiors/FISHMONGER-2026-10-03.md (Picture Sheffield t13138, 25 Aug 1990; t13140, c.1989)", read="2026-10-08 (earlier note: images looked at by the builder on the PC on 3 Oct, not re-reached here)", author="Picture Sheffield, photographer not named", licence="reference only, LINKED not kept (production/reference/photographs.md)",
         taken="1989 and 1990-08-25", shows="a fishmonger's shopfront: a dark fascia sign-written in red; window glass hand-lettered in white", period="1990, the period", used=True, what_used="red sign-writing and the whitewash glass; read as an earlier note, not re-measured", preview=None),
    dict(id="N3", url="production/research/casting/notes/names.md s.4 (Peter Marshall's Hull shop-window photographs 1979-1994, Flashbak 14 Nov 2024, captions); production/reference/photographs.md R05 and R09", read="2026-10-08 (earlier note)", author="Peter Marshall", licence="photographer copyright, LINKED", taken="1979-1994",
         shows="fascia naming patterns on Hull shops, trade-only boards, 'Sail Makers & Ship Chandlers'; painted fascias; METAL SHOPFRONTS; fluorescent strips; patterned tile stallrisers", period="1979-1994", used=True, what_used="that trade-only boards existed beside named ones; that metal fronts and fluorescent strips were the 1989 street", preview=None),
    dict(id="N4", url="production/research/shopfronts/FRONTAGE-2026-10-06.md [CV] [RI]; production/art/shopfront-kit/README.md; production/art/fascia-01/01-SPEC-fascia-package.md", read="2026-10-08", author="project helpers", licence="own work", taken="2026-10-06",
         shows="fascia 0.55 m, 0.12 proud, between consoles 0.295 to 5.705; 'traditionally not more than 600 mm' [CV], 'at most a fifth of the front's height' [RI]; 1930s refits in structural glass; sombre period colours", period="1900-1935 fronts, repainted", used=True, what_used="board size, the glass-panel generation, colours of the parade", preview=None),
    dict(id="F1", url="https://raw.githubusercontent.com/google/fonts/main/ofl/<dir>/OFL.txt and the font files named in fonts{}", read="2026-10-08", author="the font designers named in fonts{}", licence="SIL Open Font Licence 1.1, each OFL.txt read whole",
         taken="n/a", shows="the fonts' licences and files", period="n/a", used=True, what_used="every width and cap height in this target is measured on the real files", preview=None),
]
UNREACHED = [
    "commons.wikimedia.org, www.geograph.org.uk, www.flickr.com, archive.org, en.wikipedia.org, www.picturesheffield.com, flashbak.com, historicengland.org.uk, www.signpainting.co.uk, www.hathitrust.org, www.britishnewspaperarchive.co.uk, www.bygonely.com: the proxy refused every one (403 on the CONNECT) on 8 Oct 2026",
    "ambientcg.com: its API answered (the painted-wood list came back) but the file host refused every download (403), so no ambientCG photograph was measured",
    "Search summaries were not used for any number",
]
WOULD_READ = [
    "Picture Sheffield t13137 (shopfront, undated), t13138 (25 Aug 1990) and t13140 (c.1989): measure the fishmonger's board, the red lettering's height over the board and the glass lettering at full size",
    "Peter Marshall's Hull shop-window set 1979-1994 and the Brixton 1987 fishmonger (Flashbak captions led to Flickr): fascia depth, letter height over board, how many fascias are box signs, painted-out boards, a caff's front",
    "Geograph 1996-2000 views of northern parades (Hull, Grimsby, Whitby, Hartlepool) for the three generations side by side and for the bare, painted-out board",
    "Historic England 'Shopping Parades' and 'Commerce and Exchange' selection guide: fascia depths and lettering of 1900-1935 parades, glass fascias",
    "signpainting.co.uk 'Letters Potent: the modern age' and Designing Buildings 'Shop signs': dates of the shift from signwriting to Perspex and vinyl (note 4 had a sign-makers' summary only)",
    "archive.org / HathiTrust trade manuals of sign-writing and gilding (public domain by age): the proportions of shade, the gilding method, the sizes of numerals, reverse-glass signs",
    "Wikimedia Commons categories for UK shop fronts of the 1980s, with the author, licence and date read on each file page",
]

DISAGREEMENTS = [
    dict(id="D1", element="the fishmonger's colour way", book="the game's board and the recipe's wave: oxblood ground with cream letters (make_vignette_2d.py TRADE_FASCIAS; terrace-front.py FASCIA_PAINT index 1)", photograph="Picture Sheffield t13138 (25 Aug 1990, earlier note): a dark fascia sign-written in red, a different shop", chose="red sign-writing (t13138) on the sheet's white board: the photograph settles the lettering, the sheet settles the ground beside Mickey's (the photograph does not disagree with the sheet about THIS board)"),
    dict(id="D2", element="the shade under signwriting", book="the game: a near-black copy 3.5 per cent of the cap away on every board (make_trade_fascia)", photograph="P1: a solid block shade, 45 degrees down and right, 0.10 of the cap high, near-black brown", chose="photograph, and only on boards that were hand-painted or gilded; none on vinyl, applied letters or back-painted glass"),
    dict(id="D3", element="numbers at the board's two ends", book="none of the game's fascias has them", photograph="P1: both ends, 0.91 of the cap height, 25 to 46 px inside the keyline (a Leadenhall unit-number livery, not necessarily provincial practice)", chose="the photograph, on TWO boards only (Rita's and the chandler; the review's note 3); the numbers are proposed"),
    dict(id="D4", element="the keyline's corner", book="a plain rectangle (every guide drawing and the 3 Sept batch)", photograph="P1: the keyline's corners are cut by a concave quarter circle about 20 px (0.14 of the lettered field) in radius", chose="photograph, on Rita's"),
    dict(id="D5", element="fascia depth", book="FRONTAGE-2026-10-06, read at source: 'traditionally not more than 600 mm' [CV]; 'at most a fifth of the front's height' [RI]. (The 380 mm figure is a search summary in the fascia-01 spec, the PDFs blocked: a lead, not used.)", photograph="P1: lettered field 0.45 to 0.49 m (door-leaf scale), board with bead 0.53 to 0.57 m", chose="NO DISAGREEMENT: the street's 0.55 m is inside both the books and the photograph"),
    dict(id="D6", element="Mickey's name position", book="centred (game today)", photograph="not a photograph: the Hook sheet puts the letters over the door", chose="the sheet, mapped through the export's mirror: over the door at the viewer's RIGHT end of the bay, board x 4055 (variant V4 centres it)"),
    dict(id="D7", element="size of the name", book="200 mm cap on every board (game), 0.43 of the field", photograph="P1 0.31; the sheet 0.69", chose="0.34 to 0.66 by trade (Mickey's 330 mm = 0.66 of the field, 0.60 of the board)"),
]

COULD_NOT_SETTLE = [
    "NO 1990 PHOTOGRAPH OF A FASCIA WAS REACHED TODAY. The only photograph measured is a 2019 restoration of a 19th-century arcade (P1). Letter heights over board, colours, wear and which shops had box signs rest on that, on the Hook sheet, on earlier notes (cited, not re-measured) and on judgement. The list of what to read when the network opens is in would_read_when_network_opens. The reviewer too could not open t13138, t13140 or Marshall's set.",
    "Where the newsagent and the ironmonger stand: the recipe (terrace-front.py SIGN_OVERRIDE, a west block turned a half turn) puts the newsagent at street x 36-42 and the ironmonger at 30-36; hook-cast.json puts the newsagent's pension counter at x 32 and 'Hal's shop, the same block's far end' at x 39 (Hal 'keeps the coin shop that sells no coins'). One of them is wrong; the sign targets are keyed by trade so a swap is a rename. A town task, not mine to rule.",
    "Which shop is Hal's. hook-cast.json has Hal's shop at x 39 but DECISIONS 3 Oct has no coin shop in the west row. If the town keeps Hal's, it needs a fascia of its own (HAL'S is minted in the cast; its trade line is the town's to say) and the street has eleven; RULINGS 2 Oct counts twelve shopfronts and the scene has ten shop bays plus Mickey's.",
    "The shops' street numbers and the EST. years are proposed (Judgement), not minted; the town should mint or strike them (one line each in DECISIONS.md). The fascias work without them: delete the 'end' blocks and the glass rows marked proposed (variant V3).",
    "No proprietor name exists for the grocer, newsagent, ironmonger, tea room or chandler, so each board says only its trade (that is correct, and the target says so); a minted name would add one line to each board and move nothing else (variant V5).",
    "MINICABS · 24 HOURS and 0632 960418 on Mickey's glass (shop-room.py) are another family's and are NOT approved here: the first contradicts the cast's hours for Mickey's (7.00 to 3.00, shut 3 to 7); from memory (not checked) 0632 was Newcastle upon Tyne's STD code until 1992 and Meridian is fictional. For the town and the shop-room builder.",
    "Absolute scale of P1 (door leaf taken as 2.1 to 2.3 m): the camera would be at 0.93 m, low for a panorama; only ratios are used from P1. If a source gives the door leaf or the camera height the board's absolute size comes out of it.",
    "The texture size 5410 x 550 is not a power of two: the engine's treatment (mips, streaming) is from memory and NOT checked in the 5.8.2 source (not on this machine); see textures.engine_note. The builder checks first and pads or stretches if confirmed.",
    "P1's gilt shows a slightly paler rim along the face's edge (about 1 view pixel); at its resolution an outline cannot be told from the tone-map's halo. The gilt edge here is a 3 mm rim 4 L* paler, as P1 shows, not a dark matt edge; whether the rim is gilding or halo is open.",
    "The grocer's glass method (reverse-painted clear plate glass, three jointed slabs) is Judgement from memory; no source was reached for it. The box depths (150 and 140 mm), the panel depth, the hanging signs' drops and the tube layout are Judgement.",
    "Legibility at the game camera: the 70 mm trade lines read to about 15 m straight on (15 arcminutes), the 170 to 330 mm names to about 40 to 75 m straight on; the hook camera sees the boards beyond Rita's at under about 15 degrees, where nothing reads at any size (that matches the sheet). Nobody has looked at these at the game's exposure and internal resolution.",
    "Fascia-lit-at-night policy beyond the pawnbroker's window: only the window is ruled lit (DECISIONS 1 Oct). The box signs' emissive is specified; whether it is on after dark follows the town's hours (the laundry shuts at 17.30, the newsagent at 17.30), not this target.",
]

_R = dict(
    keyline_top_inset=round((P1["px"]["keyline_top_y"] - P1["px"]["field_top"]) / 147.0, 4),
    keyline_bottom_inset=round((P1["px"]["field_bottom"] - P1["px"]["keyline_bottom_y"]) / 147.0, 4),
    keyline_side_inset=round((P1["px"]["keyline_left_x"] - P1["px"]["field_left"]) / 147.0, 4),
    keyline_thickness=round(4 / 147.0, 4),
    cap_over_field=round((P1["px"]["cap_bottom"] - P1["px"]["cap_top"]) / 147.0, 4),
    cap_centre_over_field=round(((P1["px"]["cap_top"] + P1["px"]["cap_bottom"]) / 2 - P1["px"]["field_top"]) / 147.0, 4),
    name_width_over_cap=round((P1["px"]["text_x1"] - P1["px"]["text_x0"]) / 45.0, 2),
    numeral_over_cap=round((P1["px"]["numeral_bottom"] - P1["px"]["numeral_top"]) / 45.0, 3),
    shade_over_cap=round(P1["px"]["shade_px"] / 45.0, 3),
    corner_radius=round(20 / 147.0, 3),
    field_width_over_height=round((P1["px"]["field_right"] - P1["px"]["field_left"]) / 147.0, 2),
    name_centre_offset_over_panel=round(((P1["px"]["text_x0"] + P1["px"]["text_x1"]) / 2 - (P1["px"]["keyline_left_x"] + P1["px"]["keyline_right_x"]) / 2) / (P1["px"]["keyline_right_x"] - P1["px"]["keyline_left_x"]), 4),
    numeral_top_over_field=round((P1["px"]["numeral_top"] - P1["px"]["field_top"]) / 147.0, 4),
    numeral_bottom_over_field=round((P1["px"]["numeral_bottom"] - P1["px"]["field_top"]) / 147.0, 4),
    numeral_left_gap_over_field=round((P1["px"]["numeral_left"][0] - P1["px"]["keyline_left_x"]) / 147.0, 4),
    numeral_left_width_over_field=round((P1["px"]["numeral_left"][1] - P1["px"]["numeral_left"][0]) / 147.0, 4),
    numeral_right_gap_over_field=round((P1["px"]["keyline_right_x"] - P1["px"]["numeral_right"][1]) / 147.0, 4),
    numeral_right_width_over_field=round((P1["px"]["numeral_right"][1] - P1["px"]["numeral_right"][0]) / 147.0, 4),
)
PHOTO_TEMPLATE = dict(
    note="the ratios the photograph P1 gives, laid on our board for the overlay and for the 'photo wins' check; fitted on one dimension only: the lettered field's height. The name's own ratios (cap, width, centre offset, shade) were measured on the UNMASKED view and are not re-measurable on the saved preview (it holds the two ends only).",
    field_height_px=P1["px"]["field_bottom"] - P1["px"]["field_top"], ratios=_R, error_px=P1["error_px"],
)

MATERIALS = dict(
    note="roughness is 0 (mirror) to 1 (dry chalk); metallic 0 or 1 (an alloy or gilt paint may carry 0.8). A fresh paint layer on top of a chalked ground is glossier than the ground: letters are 0.08 to 0.15 below their ground's roughness until aged.",
    gold_leaf_on_size=dict(roughness=0.30, plain="bright, slightly satin", metallic=1.0, colour="gold_leaf", chip="size, 150,110,50 (yellow-brown), roughness 0.7, metallic 0", rim="a 3 mm rim 4 L* paler at the face's edge (P1's 1-pixel pale rim; unresolved whether gilding or halo)"),
    applied_brass_gilt=dict(roughness=0.38, plain="satin, dirt in the corners", metallic=0.85, colour="brass_gilt", flank="brass_side, roughness 0.5", geometry=True),
    signwriters_enamel=dict(roughness="ground minus 0.10 (0.35 to 0.5), 0.55 once chalked", plain="semi-gloss going flat", metallic=0.0),
    cut_vinyl=dict(roughness=0.45, plain="satin plastic", metallic=0.0, edge="a 0.08 mm step with a 1-pixel highlight"),
    reverse_painted_glass=dict(roughness=0.08, plain="polished glass over matte paint", metallic=0.0, letters="0.12, seen through the glass"),
    acrylic_face=dict(roughness=0.35, plain="semi-gloss plastic, a little orange-peel", metallic=0.0, translucent=True),
    anodised_bronze=dict(roughness=0.35, plain="satin metal", metallic=1.0),
    powder_black=dict(roughness=0.5, plain="satin black paint on aluminium", metallic=0.0),
    chrome_strip=dict(roughness=0.15, plain="bright metal, pitted", metallic=1.0, height_mm=0.8),
    hemp_rope=dict(roughness=0.80, plain="dry fibre", metallic=0.0),
    whitewash=dict(roughness=0.90, plain="chalk", metallic=0.0, opacity=0.85),
    bare_timber=dict(roughness=0.85, plain="dry dark wood", metallic=0.0),
    paint_loss=dict(roughness=0.85, plain="undercoat or bare wood showing", metallic=0.0, height_mm=-0.3),
    wrought_iron=dict(roughness=0.60, plain="black paint on iron, rust at fixings", metallic=0.5),
    ball_gilt_paint=dict(roughness=0.38, plain="gilt paint on sheet metal, scuffed", metallic=0.8),
)
VARIANTS = [
    dict(id="V1", name="ten boards", differs="the ten shops of this file, one board each; none repeats (distinctness)", applies_to="all"),
    dict(id="V2", name="day and night", differs="steam_laundry and newsagent: the box face is lit (emissive) when the shop is open, dark and dull when shut; every other board is unlit (only Rita's WINDOW is ruled lit, DECISIONS 1 Oct)", applies_to="steam_laundry, newsagent"),
    dict(id="V3", name="proposed marks off", differs="strip the street numbers on the boards (blocks with role 'end' on Rita's and the chandler; the numerals' place is then empty panel) and the glass rows whose source says proposed, if the town does not mint them", applies_to="ritas, chandler and the glass rows"),
    dict(id="V4", name="Mickey's centred", differs="MICKEY’S centred on the board (board x 2705) instead of over the door (board x 4055), as the game has it today", applies_to="mickeys"),
    dict(id="V5", name="a minted name", differs="when the town mints a proprietor's name, ONE more line (cap 0.5 of the trade line's) goes above the trade line on that board; nothing else moves", applies_to="grocer, newsagent, ironmonger, tea_rooms, chandler"),
    dict(id="V6", name="the street box", differs="if the street keeps its 6.0 m box, centre the 5410 texture on it and paint 295 mm of plain frame colour at each end", applies_to="all"),
]

TARGET = dict(
    schema="ledger.cloud-week-42.target.fascia-signs/2",
    family="fascia-signs",
    status="AMENDED 8 October 2026 (cloud week 42), second and last try, after a fresh reviewer's 13 faults (TARGET-REVIEW.md). Unit 4.1 builds from this file alone. self_check below is written by self_check.py.",
    summary_line="Ten fascias for Quay Street on the kit's 5410 x 550 mm board at 1 mm a pixel, set the way round the GAME shows them (low street x on the viewer's right on the east parade, so MICKEY'S stands over its door at board x 4055), with Mickey's raised letters, the two lit box signs and the tea room's flat panel as geometry, ghosts of older trade lettering with their exact words, nine fonts, layouts that are not all a centred name over a dotted trade line, and checks that read the pixels.",
    units=dict(board="millimetres. x runs from the board's LEFT as a viewer standing in the street and facing it sees it IN THE GAME (after the export's y-reflection): on the EAST parade low street x is on the viewer's RIGHT (board x = street x of the board's left end, 0.295 in from the bay's HIGH end, minus the street x); on the WEST block low street x is on the viewer's LEFT. y is UP from the board's bottom edge",
               geometry="metres where a part hangs in the street (projecting signs, glass heights); street x is along the street, unchanged by the mirror", colour="sRGB 0-255", contrast="WCAG relative-luminance ratio (L1+0.05)/(L2+0.05)", dE="CIE76 on Lab D65"),
    kinds=dict(Read="printed in a source", Scaled="measured off a drawing or the game's own files", Photo="measured on a photograph today", Sheet="measured on the Hook sheet today (a generated picture)",
               Derived="computed from the above", Judgement="mine; to be overturned by a better source"),
    axis=dict(
        rule="terrace-front.py builds the street with east at +y, where a viewer facing the east parade has +x on the RIGHT (the kit README's 'left to right seen from the street'); _export_street then REFLECTS y to -y ('mirror') so that in Unreal east is at +Y on the right when looking north. Street x (along the street) is unchanged; only the viewer's left and right swap. Lettered faces take UVs 'running from the reader's left to the reader's right in the reflected street': the texture's u axis is the viewer's left to right IN THE GAME.",
        evidence=["terrace-front.py lines 7925-7945 and 8455-8480 (the mirror and the UV rule)", "line 6616: 'unmirrored, the first film read S'YEKCIM from the pavement'", "production/previews/shop-fronts-whole-2026-10-08.jpg: from the left, TO LET (x 21-27), PAWNBROKER (15-21), FRESH FISH (9-15), MICKEY'S (3-9) with its door at the right-hand end", "production/previews/morning-hook-day-2026-10-08.jpg: Mickey's window on the left of its bay and its door at the right (the near end, low x)"],
        east=dict(u_grows_as_street_x="falls", u0_street_x_rule="bay high end minus 0.295", low_street_x_is="the viewer's RIGHT"),
        west=dict(u_grows_as_street_x="rises", u0_street_x_rule="bay low end plus 0.295", low_street_x_is="the viewer's LEFT"),
        door_ends={s["id"]: s["door_end_street"] for s in SHOPS_C}, door_ends_source="BAY_DOORS_ON = left, left, right, left, right, right (terrace-front.py line 560, Blender frame) and east_chandler's doors_on right; on the east side left = low street x; the west blocks are turned a half turn, so left = HIGH street x",
        mickeys_door=dict(street_x_m=MK_DOOR, source="production/specs/mickeys-office.json door.x (and DECISIONS 7 and 8 Oct)", board_x_mm=MK_X),
    ),
    board=dict(width_mm=BOARD_W, height_mm=BOARD_H, proud_of_wall_mm=120, z_bottom_m=2.85, z_top_m=3.40, cornice_top_m=CORNICE_TOP_M, between_consoles_in_bay_m=[0.295, 5.705],
               street_box_mm=[6000, 550], field_mm=FIELD, safe_mm=SAFE, px_per_mm=1,
               source="SCENE-SLOTS.md (fascia 2.85 to 3.40, 0.55, 0.12 proud); production/art/shopfront-kit/README.md ('0.295 to 5.705 in Rita's bay'); production/specs/vignette-scene.json (fascia_bottom_m 2.85, fascia_projection_m 0.12, bay_width_m 6.0)",
               note="The kit puts the fascia BETWEEN the consoles, 5.41 m; the street's box today runs the full 6.0 m across the pilaster heads and buries the consoles' feet (README, 'For the session'). This target is for the 5.41 m board. If the street keeps its 6.0 m box, centre the 5410 texture on it and keep 295 mm of plain frame colour each side; nothing in the layouts reaches the outer 150 mm.",
               frame_note="NO baked highlight or shade in the base colour (the review's fault 11): under the cornice the top is in its shadow, which is Unreal's. Where a board has a planted moulding (Rita's, ironmonger, chandler) the outer 24 mm is relief in the height map: +0.6 mm with a 4 mm chamfer. None on vinyl, box, panel or glass.",
               lighting_note="overcast, the camera 1.6 m up, the board 1.25 to 1.8 m over the eye: letters are read from below at 5 to 25 degrees; the texture is flat and square-on, the relief goes in the height map"),
    fonts=FONT_ROWS,
    palette=PALETTE,
    age_rules=dict(note="how srgb_1990 was got from srgb_fresh where it was not measured (Judgement): share of a grime film (88,82,74) mixed in linear light, a chalk lift in L*, a chroma factor, a yellowing in b*", classes=AGE),
    textures=TEXTURES,
    photo=dict(P1=P1, H1=SHEET, planks=PLANKS),
    photo_template=PHOTO_TEMPLATE,
    common_style=dict(
        hand_jitter=HAND,
        gilding=dict(method="oil gilding on size for boards (flat, matte-bright, roughness 0.25-0.4, metallic 1); water gilding on glass (roughness 0.15, metallic 1, seen from the back)", fresh=PALETTE["gold_leaf"]["srgb_fresh"], aged_sheet=PALETTE["brass_gilt"]["srgb_1990"],
                     edge="a 3 mm rim 4 L* paler at the face's edge, as P1 shows (unresolved whether gilding or tone-map halo); chips show the size (150,110,50)"),
        shade=dict(style="block shade, 45 degrees down and to the right, length 0.10 of the cap (P1: 4.5 px of 45); the shade is the extrusion of the glyph, not a blurred drop; colour per block", kind="Photo"),
        keyline=dict(thickness_over_field=_R["keyline_thickness"], inset_over_field=[_R["keyline_top_inset"], _R["keyline_bottom_inset"]], corner="concave quarter circle", radius_over_field=_R["corner_radius"], kind="Photo"),
        spacing=dict(word_space_em=0.32, note="word spaces are the font's, widened by the tracking; the middle dot separator has a word space each side"),
        optical=dict(centre="the block is centred on the ink, not on the advance box; P1's name sits 1.4 per cent of the panel width left of the panel's centre, so +-1.5 per cent is the hand's tolerance", baseline_hang_mm="round capitals (C, O, S, G) overshoot the baseline and the cap line by 1.6 per cent of the cap"),
        trade_line_minimum_cap_mm=70,
        symmetric_strings=[], symmetric_note="strings whose mirror image reads as itself (the mask check cannot tell them from their flip); none is known: self_check group 7 renders every block and lists any whose flipped mask is within 0.15 IoU of the true one",
    ),
    shops=SHOPS_C,
    projecting_signs=PROJECTING,
    glass_lettering=GLASS,
    small_panels=SMALL_PANELS,
    approved_words=sorted(APPROVED),
    approved_word_parts=APPROVED_PARTS,
    ghost_words=sorted(GHOST_WORDS),
    existing_not_approved=sorted(set(EXISTING_NOT_APPROVED)),
    hours_plate_rule=HOURS_RULE,
    forbidden_patterns=FORBIDDEN,
    distinctness=DISTINCT,
    materials=MATERIALS,
    variants=VARIANTS,
    checks=CHECKS,
    disagreements_photographs_win=DISAGREEMENTS,
    sources=SOURCES,
    unreached=UNREACHED,
    would_read_when_network_opens=WOULD_READ,
    could_not_settle=COULD_NOT_SETTLE,
    estimates=dict(
        shop_count=dict(scene_bays=10, listed_in_rulings="twelve shopfronts (RULINGS 2 Oct: 'the other eleven')", note="east parade 6 (Mickey's, fish, Rita's, empty, laundry, grocer), west_north 3, east_chandler 1 = 10; the cast also names Hal's shop and a cafe (the tea room)"),
    ),
    self_check=None,
)

if __name__ == "__main__":
    out = HERE / "target.json"
    prev = None
    if out.exists():
        try:
            prev = json.loads(out.read_text(encoding="utf-8")).get("self_check")
        except Exception:
            prev = None
    TARGET["self_check"] = prev
    out.write_text(json.dumps(TARGET, indent=1, ensure_ascii=False, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o)), encoding="utf-8")
    print("wrote", out, out.stat().st_size, "bytes")
    for s in SHOPS_C:
        names = [(b["id"], b["width_mm"], b["cap_mm"], b["contrast_1990"]) for b in s["blocks"]]
        print(f'{s["id"]:14s} margin={s["min_margin_mm"]} overlaps={s["overlaps"]} blocks={names}')
    print("distinct violations:", DISTINCT["violations"])
    print("min ground dE:", DISTINCT["min_ground_dE"], "centred:", DISTINCT["centred_skeleton_boards"], "dotted:", DISTINCT["dotted_trade_lines"])
    print("checks:", len(CHECKS), "approved:", len(APPROVED))
