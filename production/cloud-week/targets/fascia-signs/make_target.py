"""Author tool: writes target.json for the Quay Street fascia signs (cloud week 42, 8 October 2026).

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
    "libre-baskerville": dict(family="Libre Baskerville", dir="librebaskerville", file="LibreBaskerville[wght].ttf", axes={"Weight": None},
                              designer="Impallari Type", rfn="Libre Baskerville", in_repo=None,
                              looks_like="sturdy roman capitals; ironmongers' and chemists' boards"),
    "fraunces": dict(family="Fraunces", dir="fraunces", file="Fraunces[SOFT,WONK,opsz,wght].ttf",
                     axes={"Weight": None, "Softness": 100, "Optical Size": 144, "Wonky": 0},
                     designer="Undercase Type, Phaedra Charles, Flavia Zimbardi", rfn=None, in_repo=None,
                     looks_like="soft, heavy 'Windsor/Cooper' roman of the 1970s-80s café and tea room"),
    "alfa-slab-one": dict(family="Alfa Slab One", dir="alfaslabone", file="AlfaSlabOne-Regular.ttf", axes={},
                          designer="JM Solé", rfn="Alfa Slab", in_repo=None,
                          looks_like="fat Egyptian slab capitals; chandlers', harbour and market lettering"),
    "josefin-sans": dict(family="Josefin Sans", dir="josefinsans", file="JosefinSans[wght].ttf", axes={"Weight": None},
                         designer="Santiago Orozco", rfn="Josefin", in_repo=None,
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
    (x0, y_bottom, x1, y_top) with y up. Tracking is added between glyphs (not after the last)."""
    r = cap_ratio(key, weight)
    size = cap_mm / r
    f = font(key, weight, 1000)
    b = f.getbbox(text, anchor="ls")
    n = len(text)
    k = size / 1000.0
    x0 = b[0] * k
    x1 = (b[2] + tracking_em * 1000 * (n - 1)) * k
    return (round(x0, 1), round(-b[3] * k, 1), round(x1, 1), round(-b[1] * k, 1)), size


# --------------------------------------------------------------------------------------------
# 2. The board. Read from the kit README and the scene spec (self_check.py reads them again).
# --------------------------------------------------------------------------------------------
BOARD_W, BOARD_H = 5410, 550
FRAME = 24
SAFE = [150, 40, BOARD_W - 150, BOARD_H - 40]
FIELD = [FRAME, FRAME, BOARD_W - FRAME, BOARD_H - FRAME]
CX = BOARD_W / 2.0

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
pal("charcoal_navy", "charcoal navy", (24, 30, 40), "dark_gloss", "Judgement", "a dark fascia as Picture Sheffield t13138 (25 Aug 1990) describes it: 'dark fascia sign-written in red'; the hue is mine")
pal("vermilion", "signwriter's vermilion", (200, 40, 36), "red", "Judgement", "t13138's red lettering; fades first of the paints")
pal("cream_shade", "cream", (230, 220, 192), "cream", "Judgement")
pal("cream", "cream", (236, 226, 198), "cream", "Judgement")
pal("bare_timber", "bare soot-darkened timber", (92, 80, 68), "none", "Scaled", "terrace-front.py FASCIA_PAINT bare_timber 0.021,0.014,0.010 linear is 40,31,25 sRGB, the freshly bared board; a board left bare for years greys and lightens, 92,80,68 by judgement", y1990=(98,85,72))
pal("painted_out", "painted-out buff grey", (176, 170, 150), "cream", "Judgement", "the cream overpaint of a gone trade's lettering")
pal("acrylic_white", "white acrylic face", (238, 236, 228), "white_plastic", "Judgement")
pal("vinyl_blue", "royal blue vinyl", (24, 62, 140), "vinyl", "Scaled", "the game's launderette letters today, 28,64,140")
pal("vinyl_red", "scarlet vinyl", (176, 30, 34), "vinyl", "Scaled", "the game's launderette trade line today, 176,30,34")
pal("bronze_anodised", "bronze anodised aluminium", (96, 76, 58), "metal", "Judgement", "the 1970s-80s box sign extrusion")
pal("deco_green_glass", "dark bottle-green structural glass", (30, 58, 46), "glass", "Judgement", "back-painted opaque glass; the 1930s refit of FRONTAGE-2026-10-06 sections 1 and 3 (Vitrolite named there; the trade mark is not used here)")
pal("chrome", "chrome strip", (196, 200, 202), "metal", "Judgement")
pal("signal_red", "signal red", (176, 36, 40), "red", "Judgement", "the newsagent's board; a plain red of the 1980s refit, not a brand red")
pal("vinyl_black", "black vinyl", (28, 28, 28), "vinyl", "Judgement")
pal("vinyl_cream", "cream vinyl", (236, 226, 198), "vinyl", "Judgement")
pal("vinyl_orange", "orange vinyl", (214, 116, 38), "vinyl", "Judgement")
pal("buff_board", "buff", (200, 188, 156), "cream", "Scaled", "the game's newsagent board today is 190,176,140")
pal("sign_black", "black", (26, 26, 24), "black", "Judgement")
pal("duck_egg", "duck-egg blue-green", (158, 192, 182), "cream", "Judgement", "a tea room's pastel; the Hook sheet has pale fronts (white 204,204,204; cream 128,101,98 in shade)")
pal("deep_teal", "deep teal", (24, 74, 76), "dark_gloss", "Judgement")
pal("navy", "navy", (28, 42, 78), "dark_gloss", "Scaled", "the game's chandler letters today are 30,40,70; as a board colour 28,42,78")
pal("white_paint", "signwriter's white", (238, 234, 220), "cream", "Judgement")
pal("hemp", "hemp rope", (196, 176, 136), "cream", "Judgement")
pal("whitewash", "whitewash", (238, 236, 228), "cream", "Read", "'white whitewash lettering on the glass', Picture Sheffield t13138, read on the PC 3 Oct (earlier note)")
PALETTE = _P

# --------------------------------------------------------------------------------------------
# 4. The ten fascias. Each block: text, font, weight, cap height (mm), tracking (em), anchor, baseline.
#    y is up from the board's bottom edge, x from its left (low street x) end.
# --------------------------------------------------------------------------------------------


def blk(id_, text, font_key, weight, cap, trk, baseline, face, anchor="centre", x=None, shade=None, outline=None,
        technique="painted", jitter=None, relief_mm=0.0, role="name", shade_kind="block45", embolden_mm=0.0):
    return dict(id=id_, text=text, font=font_key, weight=weight, cap_mm=cap, tracking_em=trk, baseline_mm=baseline,
                anchor=anchor, x_mm=CX if x is None else x, face=face, shade=shade, outline=outline, technique=technique,
                jitter=jitter, relief_mm=relief_mm, role=role, shade_kind=shade_kind, embolden_mm=embolden_mm)


def SH(colour, cap):
    """P1: the block shade is 0.10 of the cap, 45 degrees down and right."""
    return dict(colour=colour, d_mm=round(0.10 * cap, 1))


HAND = dict(baseline_mm=1.6, advance_pct=1.5, rotation_deg=0.35, stroke_pct=3.0, note="a hand-painted board: each glyph nudged; not for vinyl, applied or glass-gilt")

SHOPS = []

# --- bay 0, Mickey's -----------------------------------------------------------------------
SHOPS.append(dict(
    id="mickeys", order=0, block="east_parade", bay=0, street_x_m=[3.0, 9.0], side="east", street_number="1",
    trade="minicab office", name_minted=True, name_source="canon.md (Brands and law; D19); content/brands/brand-bible-v1.json id mickeys (founded 1962)",
    construction="painted timber board, name in applied (stand-off) gilt capitals",
    construction_kind="applied_letters",
    ground=dict(colour="slate", finish="eggshell paint, many coats, a little orange-peel", roughness=0.55, metallic=0.0,
                grain=dict(direction="along", amp_L=1.2, scale_mm=[40, 400])),
    blocks=[blk("name", "MICKEY’S", "marcellus-sc", 400, 270, 0.03, 140, "brass_gilt", anchor="centre", x=1355,
                technique="applied", relief_mm=14.0, role="name", embolden_mm=3.0)],
    border=None,
    notes=["Name over the door (street x 4.65 = board x 1355), as the Hook sheet puts it (letters at 0.755 of the board from the far end, 0.245 x 5410 = 1325 from the door end).",
           "Letters are stand-off: 14 mm off the board (Judgement; the recipe's RAISED_LETTERS stands them off already), square-cut edges, a dark brass flank, a soft contact shadow.",
           "'Sign hand-painted and repainted a shade off each time' (brand bible): a ghost of an older, centred MICKEY’S in a blue 3-4 dE off the board, and ten pin holes of the older lettering."],
    ghost=dict(kind="repaint_patch", box_mm=[1900, 120, 3510, 430], colour_dE=3.5, edge="a brush-cut edge, 1 mm ridge", pinholes=10),
    age=dict(klass=2, loss_fraction=0.04, chalk_dL=3.0, grime_film=0.07, runs=dict(count=4, len_mm=[40, 160]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=2, kind="two short runs under the console fixings")),
    lit=None))

# --- bay 1, Fish Market ---------------------------------------------------------------------
SHOPS.append(dict(
    id="fish_market", order=1, block="east_parade", bay=1, street_x_m=[9.0, 15.0], side="east", street_number="3",
    trade="fishmonger", name_minted=True, name_source="DECISIONS.md 3 Oct 2026 ('the fishmonger (Fish Market)'); production/specs/hook-cast.json fish_market",
    construction="sign-written flat paint on a dark painted board; red block capitals with a cream block shade; two red rules",
    construction_kind="signwritten",
    ground=dict(colour="charcoal_navy", finish="gloss enamel gone flat and chalky", roughness=0.58, metallic=0.0,
                grain=dict(direction="along", amp_L=1.5, scale_mm=[30, 300])),
    blocks=[blk("name", "FISH MARKET", "oswald", 600, 290, 0.06, 188, "vermilion", shade=SH("cream_shade", 290), jitter=HAND, role="name"),
            blk("trade", "WET FISH · SHELLFISH · SMOKED", "oswald", 400, 62, 0.20, 82, "cream", jitter=HAND, role="trade")],
    border=dict(kind="rules", rules=[dict(y_mm=[34, 46], x_mm=[120, BOARD_W - 120], colour="vermilion"), dict(y_mm=[BOARD_H - 46, BOARD_H - 34], x_mm=[120, BOARD_W - 120], colour="vermilion")]),
    notes=["A dark fascia sign-written in red, as the photograph Picture Sheffield t13138 (25 Aug 1990) shows a fishmonger's (earlier note). It replaces the game's oxblood board with cream letters, which the photograph does not support."],
    ghost=dict(kind="faint_older_lettering", box_mm=[900, 90, 4500, 470], colour_dE=4.0, edge="brush edge", pinholes=0),
    age=dict(klass=2, loss_fraction=0.05, chalk_dL=4.0, grime_film=0.08, runs=dict(count=6, len_mm=[50, 200]), gull=dict(count=3, size_mm=[15, 45]), rust=dict(count=0, kind="")),
    lit=None))

# --- bay 2, Rita's ---------------------------------------------------------------------------
SHOPS.append(dict(
    id="ritas", order=2, block="east_parade", bay=2, street_x_m=[15.0, 21.0], side="east", street_number="5",
    trade="pawnbroker", name_minted=True, name_source="production/specs/hook-cast.json (ritas, rita); DECISIONS.md 30 Sep and 6 Oct; RULINGS 2 Oct 'Rita's window is the model'",
    construction="oil-gilded capitals with a black block shade on an oxblood board inside a gilt cut-corner keyline panel",
    construction_kind="gilded",
    ground=dict(colour="oxblood", finish="oil gloss, now satin", roughness=0.45, metallic=0.0,
                grain=dict(direction="along", amp_L=1.2, scale_mm=[40, 400])),
    blocks=[blk("name", "RITA’S", "abril-fatface", 400, 230, 0.10, 221, "gold_leaf", shade=SH("shade_black", 230), technique="gilded", jitter=HAND, role="name"),
            blk("trade", "PAWNBROKER", "old-standard-tt-bold", 700, 84, 0.30, 99, "gold_leaf", shade=SH("shade_black", 84), technique="gilded", jitter=HAND, role="trade"),
            blk("end_l", "5", "abril-fatface", 400, 214, 0.0, 168, "gold_leaf", anchor="left", x=200, shade=SH("shade_black", 214), technique="gilded", jitter=HAND, role="end"),
            blk("end_r", "5", "abril-fatface", 400, 214, 0.0, 168, "gold_leaf", anchor="right", x=BOARD_W - 200, shade=SH("shade_black", 214), technique="gilded", jitter=HAND, role="end")],
    border=dict(kind="cutcorner_panel", inset_mm=44, line_mm=13, inner_line_mm=0, gap_mm=0, radius_mm=70, colour="gold_leaf"),
    notes=["The numbers at the two ends are what the photographed Leadenhall boards do (both ends, 0.91 of the name's cap height, P1); the number 5 is proposed, not minted. The keyline is P1's: one line 0.027 of the field thick, inset 0.09, corners cut by a concave quarter circle.",
           "The three balls hang from a bracket (projecting_signs); the toplight glass carries WATCHES, JEWELLERY and LOANS (glass), so the board stays calm."],
    ghost=dict(kind="repaint_patch", box_mm=[2300, 140, 3300, 340], colour_dE=3.0, edge="brush-cut edge", pinholes=0),
    age=dict(klass=1, loss_fraction=0.03, chalk_dL=3.0, grime_film=0.06, runs=dict(count=3, len_mm=[40, 140]), gull=dict(count=1, size_mm=[15, 35]), rust=dict(count=0, kind="")),
    lit="night_window_lit"))

# --- bay 3, the empty unit ------------------------------------------------------------------
SHOPS.append(dict(
    id="empty_unit", order=3, block="east_parade", bay=3, street_x_m=[21.0, 27.0], side="east", street_number="7",
    trade="empty unit to let", name_minted=False, name_source="RULINGS 3 Oct; DECISIONS.md 3 Oct ('whitewashed')",
    construction="bare soot-darkened timber, the last trade's lettering painted out in buff, a letting board across the middle",
    construction_kind="bare",
    ground=dict(colour="bare_timber", finish="paint long gone, bare grey-brown timber with a few patches of old dark paint", roughness=0.85, metallic=0.0,
                grain=dict(direction="along", amp_L=4.0, scale_mm=[25, 600])),
    blocks=[],
    border=None,
    notes=["No lettering at all: a painted-out patch 3200 x 300 mm in buff (176,170,150, brush strokes along the board) where the last trade's name was, its edge a thin ridge of old paint, no legible letter.",
           "The letting board (900 x 450 mm, TO LET) is a separate asset (board_to_let); its place on the board is in 'small_panels'."],
    ghost=dict(kind="painted_out_patch", box_mm=[1105, 120, 4305, 420], colour_dE=0.0, edge="ridge 0.4 mm, ragged", pinholes=6),
    age=dict(klass=3, loss_fraction=0.17, chalk_dL=0.0, grime_film=0.15, runs=dict(count=10, len_mm=[60, 300]), gull=dict(count=6, size_mm=[20, 70]), rust=dict(count=3, kind="three runs from old bracket bolts")),
    lit=None))

# --- bay 4, Steam Laundry (launderette) -------------------------------------------------------
SHOPS.append(dict(
    id="steam_laundry", order=4, block="east_parade", bay=4, street_x_m=[27.0, 33.0], side="east", street_number="9",
    trade="launderette (the Steam Laundry)", name_minted=True, name_source="DECISIONS.md 3 Oct ('the Steam Laundry as a launderette'); hook-cast.json laundry",
    construction="lit box sign: white acrylic face in a bronze extrusion, cut-vinyl letters, fluorescent tubes behind",
    construction_kind="box_sign",
    ground=dict(colour="acrylic_white", finish="acrylic, semi-gloss, yellowing", roughness=0.35, metallic=0.0,
                grain=dict(direction="none", amp_L=0.8, scale_mm=[200, 800])),
    blocks=[blk("name", "STEAM LAUNDRY", "jost", 800, 205, 0.05, 225, "vinyl_blue", technique="vinyl", role="name"),
            blk("trade", "LAUNDERETTE · SERVICE WASHES · DRY CLEANING", "jost", 600, 66, 0.14, 119, "vinyl_red", technique="vinyl", role="trade")],
    border=dict(kind="box", outer_mm=[105, 35, 5305, 515], frame_mm=26, colour="bronze_anodised", face_colour="acrylic_white"),
    notes=["Plastic box sign of the 1970s-80s kind (note 4: 'the backlit Perspex sign was increasingly replacing the old fascias'), screwed over the old board; the 105 mm each end and 35 mm above and below show old painted timber (cream, chalked).",
           "Emissive: the face glows when the shop is open; hours from hook-cast.json (Mon-Sat 8 to 17.30), so lit on winter afternoons only. Two rows of tubes show as +6 % bands; one tube dead."],
    ghost=None,
    age=dict(klass=2, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.10, runs=dict(count=7, len_mm=[60, 220]), gull=dict(count=0, size_mm=[0, 0]), rust=dict(count=0, kind="")),
    lit="tubes"))

# --- bay 5, grocer --------------------------------------------------------------------------
SHOPS.append(dict(
    id="grocer", order=5, block="east_parade", bay=5, street_x_m=[33.0, 39.0], side="east", street_number="11",
    trade="grocer", name_minted=False, name_source="trade-only: no proprietor minted (DECISIONS.md 3 Oct names the trade only)",
    construction="1930s refit: back-painted bottle-green structural glass slab, Art Deco cream capitals, chrome edge and speed lines",
    construction_kind="glass_panel",
    ground=dict(colour="deco_green_glass", finish="polished opaque glass, crazed in places, grimy", roughness=0.08, metallic=0.0,
                grain=dict(direction="none", amp_L=0.6, scale_mm=[300, 900])),
    blocks=[blk("name", "FAMILY GROCER", "josefin-sans", 700, 190, 0.14, 231, "cream", technique="back_painted", role="name"),
            blk("trade", "PROVISIONS · FRUIT · VEG", "josefin-sans", 600, 58, 0.30, 129, "cream", technique="back_painted", role="trade")],
    border=dict(kind="glass_slab", outer_mm=[40, 25, BOARD_W - 40, BOARD_H - 25], edge_mm=12, colour="chrome",
                speed_lines=dict(y_mm=[262, 282, 302], line_mm=6, x_left_mm=[52, 640], x_right_mm=[BOARD_W - 640, BOARD_W - 52])),
    notes=["One fascia of the parade is a 1930s refit in structural glass (FRONTAGE-2026-10-06: 'the 1930s used etched sunrise patterns, bronze, chrome and Vitrolite'; Vitrolite 'cracks low down ... patched with painted ply or Perspex'); here a diagonal craze crack across the right third, patched with a strip of painted board 120 x 300 mm.",
           "FAMILY GROCER is a trade description, not a name."],
    ghost=None,
    age=dict(klass=2, loss_fraction=0.0, chalk_dL=0.0, grime_film=0.06, runs=dict(count=5, len_mm=[60, 240]), gull=dict(count=1, size_mm=[20, 45]), rust=dict(count=0, kind=""),
             crack=dict(count=1, kind="diagonal craze across the right third, 3 branches", patch_mm=[120, 300])),
    lit=None))

# --- west_north bay 0, newsagent (street x 36 to 42, the recipe's turned numbering) ----------
SHOPS.append(dict(
    id="newsagent", order=6, block="west_north", bay=0, street_x_m=[36.0, 42.0], side="west", street_number="18",
    trade="newsagent and tobacconist", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct. SEE THE CAST CONFLICT in TARGET.md (hook-cast puts the newsagent at x 30-36)",
    construction="cut vinyl letters stuck on a signal-red painted board, one black vinyl stripe",
    construction_kind="vinyl_on_board",
    ground=dict(colour="signal_red", finish="gloss paint, tired", roughness=0.5, metallic=0.0,
                grain=dict(direction="along", amp_L=1.2, scale_mm=[40, 400])),
    blocks=[blk("name", "NEWSAGENT", "libre-franklin", 900, 240, 0.05, 229, "vinyl_cream", technique="vinyl", role="name"),
            blk("trade", "TOBACCONIST · CONFECTIONER", "libre-franklin", 700, 66, 0.16, 123, "vinyl_cream", technique="vinyl", role="trade")],
    border=dict(kind="rules", rules=[dict(y_mm=[40, 66], x_mm=[FRAME, BOARD_W - FRAME], colour="vinyl_black")]),
    notes=["Computer-cut vinyl arrived at the end of the 1980s ([SS], note 4); here it is on a plain red board of a 1980s refit. Edges lift, one corner of the black stripe curls."],
    ghost=None,
    age=dict(klass=2, loss_fraction=0.06, chalk_dL=3.0, grime_film=0.09, runs=dict(count=5, len_mm=[40, 150]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=0, kind=""),
             vinyl=dict(lifted_corners=2, note="the stripe's right end lifts 30 mm; no letter is lost")),
    lit=None))

# --- west_north bay 1, ironmonger (x 30 to 36) --------------------------------------------------
SHOPS.append(dict(
    id="ironmonger", order=7, block="west_north", bay=1, street_x_m=[30.0, 36.0], side="west", street_number="16",
    trade="ironmonger", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct",
    construction="sign-written black roman capitals with a vermilion block shade on a buff board, black rule border",
    construction_kind="signwritten",
    ground=dict(colour="buff_board", finish="gloss paint, chalked and grimy", roughness=0.55, metallic=0.0,
                grain=dict(direction="along", amp_L=1.5, scale_mm=[30, 300])),
    blocks=[blk("name", "IRONMONGER", "libre-baskerville", 700, 180, 0.08, 234, "sign_black", shade=SH("vermilion", 180), jitter=HAND, role="name"),
            blk("trade", "TOOLS · HARDWARE · PARAFFIN", "libre-baskerville", 400, 56, 0.20, 136, "sign_black", jitter=HAND, role="trade"),
            blk("end_l", "16", "libre-baskerville", 700, 167, 0.0, 191, "sign_black", anchor="left", x=210, shade=SH("vermilion", 167), jitter=HAND, role="end"),
            blk("end_r", "16", "libre-baskerville", 700, 167, 0.0, 191, "sign_black", anchor="right", x=BOARD_W - 210, shade=SH("vermilion", 167), jitter=HAND, role="end")],
    border=dict(kind="double_rule", inset_mm=36, line_mm=8, inner_gap_mm=14, inner_line_mm=3, colour="sign_black", inner_colour="vermilion", corner_block_mm=30),
    notes=["The number 16 is proposed, not minted (and EST. 1884 is on the glass, glass_lettering). Metal-framed window (recipe SHOPFRONT_REFITS west_north bay 1) under a painted timber fascia: the refit did not reach the board."],
    ghost=dict(kind="faint_older_lettering", box_mm=[800, 100, 4600, 430], colour_dE=4.0, edge="brush edge", pinholes=0),
    age=dict(klass=2, loss_fraction=0.06, chalk_dL=4.0, grime_film=0.12, runs=dict(count=6, len_mm=[40, 180]), gull=dict(count=2, size_mm=[15, 40]), rust=dict(count=2, kind="under the hanging-sign bracket bolts")),
    lit=None))

# --- west_north bay 2, tea rooms (x 24 to 30) -----------------------------------------------------
SHOPS.append(dict(
    id="tea_rooms", order=8, block="west_north", bay=2, street_x_m=[24.0, 30.0], side="west", street_number="14",
    trade="tea room", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct ('a tea room'); hook-cast.json calls it the cafe or the caff",
    construction="1980s refit: hand-painted deep-teal soft-roman letters on a duck-egg board, a scalloped deep-teal valance along the bottom",
    construction_kind="painted",
    ground=dict(colour="duck_egg", finish="gloss paint, a few years old", roughness=0.42, metallic=0.0,
                grain=dict(direction="along", amp_L=1.0, scale_mm=[40, 400])),
    blocks=[blk("name", "Tea Rooms", "fraunces", 900, 215, 0.02, 248, "deep_teal", jitter=HAND, role="name"),
            blk("trade", "TEAS · LIGHT LUNCHES · HOME BAKING", "fraunces", 600, 52, 0.24, 156, "deep_teal", jitter=HAND, role="trade")],
    border=dict(kind="scallops", y_mm=[24, 76], pitch_mm=80, radius_mm=26, x_mm=[100, BOARD_W - 100], colour="deep_teal"),
    notes=["The only mixed-case name on the street; cap height is the T's. The scalloped valance is painted, not applied. Light ground, dark letters: the one pastel board on the street."],
    ghost=None,
    age=dict(klass=1, loss_fraction=0.02, chalk_dL=3.0, grime_film=0.07, runs=dict(count=3, len_mm=[40, 120]), gull=dict(count=1, size_mm=[15, 30]), rust=dict(count=0, kind="")),
    lit=None))

# --- east_chandler, ship chandler (x 40 to 46) ------------------------------------------------------
SHOPS.append(dict(
    id="chandler", order=9, block="east_chandler", bay=0, street_x_m=[40.0, 46.0], side="east", street_number="13",
    trade="ship chandler", name_minted=False, name_source="trade-only; DECISIONS.md 3 Oct",
    construction="white Egyptian capitals with a black block shade on a navy board, a painted rope border",
    construction_kind="signwritten",
    ground=dict(colour="navy", finish="gloss paint, salt-weathered", roughness=0.5, metallic=0.0,
                grain=dict(direction="along", amp_L=1.4, scale_mm=[30, 350])),
    blocks=[blk("name", "SHIP CHANDLER", "alfa-slab-one", 400, 170, 0.05, 239, "white_paint", shade=SH("shade_black", 170), jitter=HAND, role="name"),
            blk("trade", "ROPE · PAINT · CHARTS · TWINE", "libre-franklin", 700, 58, 0.20, 141, "cream", jitter=HAND, role="trade"),
            blk("end_l", "13", "alfa-slab-one", 400, 158, 0.0, 196, "white_paint", anchor="left", x=210, shade=SH("shade_black", 158), jitter=HAND, role="end"),
            blk("end_r", "13", "alfa-slab-one", 400, 158, 0.0, 196, "white_paint", anchor="right", x=BOARD_W - 210, shade=SH("shade_black", 158), jitter=HAND, role="end")],
    border=dict(kind="rope", inset_mm=34, rope_mm=12, corner_radius_mm=40, pitch_mm=28, colour="hemp"),
    notes=["Metal-framed window (recipe: east_chandler is a metal refit) under a painted board. The number 13 is proposed, not minted (EST. 1879 is on the glass). Salt bloom: the board's lower edge is whiter."],
    ghost=None,
    age=dict(klass=2, loss_fraction=0.07, chalk_dL=4.0, grime_film=0.10, runs=dict(count=6, len_mm=[40, 200]), gull=dict(count=4, size_mm=[20, 60]), rust=dict(count=3, kind="three runs under fixings; the quay is near")),
    lit=None))


# --------------------------------------------------------------------------------------------
# 5. Everything that is not fascia lettering: projecting signs, glass, small panels. Judgement
#    throughout unless a kind says otherwise; sizes are metres for geometry, mm for lettering.
# --------------------------------------------------------------------------------------------
PROJECTING = [
    dict(id="ritas_three_balls", shop="ritas", kind="bracket sign, three balls",
         mount=dict(on="left pilaster of bay 2, face of the shaft", x_street_m=15.175, wall_y_m=0.0, arm_height_m=3.28, projection_m=0.85),
         parts=dict(arm="wrought-iron scroll bracket, 20 x 8 mm bar, four scrolls, a hook and a ring; mounting plate 0.18 x 0.30 m with four bolt heads",
                    balls=dict(count=3, diameter_m=0.26, arrangement="two above, one below (a triangle)", centres_m=[[0.57, 3.00, -0.14], [0.57, 3.00, 0.14], [0.57, 2.78, 0.0]],
                               note="x = out from the wall face along the arm's length (0.57 of 0.85), y up, z along the street from the hanger"),
                    hanger="10 mm iron rod from the arm, 0.10 m, then a ring"),
         materials=dict(balls=dict(colour="gold_leaf", plain="gilt paint over sheet metal, scuffed to metal where hands reach", roughness=0.38, metallic=0.8),
                        iron=dict(colour="sign_black", plain="black paint on wrought iron, rust at the bolts", roughness=0.6, metallic=0.5)),
         clearance_below_m=2.65, kind_of_number="Judgement", note="No photograph of one was reached. The three balls are the pawnbroker's traditional sign and not a trade mark; no name or lettering on them."),
    dict(id="steam_laundry_box", shop="steam_laundry", kind="double-sided projecting box sign",
         mount=dict(on="left pilaster of bay 4", x_street_m=27.175, arm_height_m=2.95, projection_m=0.62),
         parts=dict(box_m=[0.62, 0.45, 0.14], note="width 0.62 projects from the wall; 0.45 high; 0.14 thick between the two faces; bronze extrusion 20 mm, white acrylic faces, two tubes inside"),
         faces=dict(text="LAUNDERETTE", font="jost", weight=800, cap_mm=60, tracking_em=0.03, colour="vinyl_blue", ground="acrylic_white",
                    note="each face reads left to right from its own side; faces are mirror-correct, not mirrored"),
         emissive=True, clearance_below_m=2.70, kind_of_number="Judgement", note="Lit when the shop is open (hours in hook-cast.json)."),
    dict(id="ironmonger_hanging_board", shop="ironmonger", kind="hanging painted board on a forged bracket (the KCD2 frame's kind)",
         mount=dict(on="right pilaster of the ironmonger's bay, wall face", arm_height_m=3.05, projection_m=0.70),
         parts=dict(board_m=[0.55, 0.38, 0.04], hang="two iron rings, 0.06 m; scroll bracket as the pawnbroker's but plainer"),
         faces=dict(text="KEYS CUT", font="libre-baskerville", weight=700, cap_mm=92, tracking_em=0.08, colour="sign_black", ground="buff_board", shade=dict(colour="vermilion", d_mm=9),
                    border="black rule 6 mm inset 20 mm", note="both faces alike"),
         clearance_below_m=2.62, kind_of_number="Judgement", note="KEYS CUT: the ironmonger's key-cutting is in its window room (DECISIONS 7 Oct)."),
    dict(id="chandler_hanging_board", shop="chandler", kind="hanging painted board on a forged bracket",
         mount=dict(on="left pilaster of the chandler's bay", arm_height_m=3.10, projection_m=0.90),
         parts=dict(board_m=[0.80, 0.50, 0.05], hang="two chains of four links"),
         faces=dict(text="CHANDLERY", font="alfa-slab-one", weight=400, cap_mm=105, tracking_em=0.05, colour="white_paint", ground="navy", shade=dict(colour="shade_black", d_mm=10),
                    border="rope 10 mm inset 24 mm", note="both faces alike"),
         clearance_below_m=2.58, kind_of_number="Judgement", note="A word not on the fascia, so the street does not repeat itself."),
]

GLASS = [
    dict(shop="mickeys", surface="window glass, inside face", text="0632 960418", font="marcellus-sc", cap_mm=170, technique="gold leaf with black shade 3 per cent of cap", z_m=2.02, source="tools/art-recipes/shop-room.py lines 1455-1459 (exists)", kind="Read"),
    dict(shop="mickeys", surface="window glass, inside face", text="MINICABS · 24 HOURS", font="marcellus-sc", cap_mm=85, technique="gold leaf with black shade", z_m=1.82, source="shop-room.py (exists)", kind="Read"),
    dict(shop="mickeys", surface="side-door fanlight", text="1", font="marcellus-sc", cap_mm=110, technique="gold leaf, black shade", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="fish_market", surface="window glass, lower left and right panes", text="FRESH DAILY", font="patrick-hand", cap_mm=120, technique="whitewash brush lettering, uneven, 85 per cent opaque", z_m=[0.85, 1.05], source="Picture Sheffield t13138 (earlier note): window glass hand-lettered in white with the fish and offers", kind="Read"),
    dict(shop="fish_market", surface="window glass", text="SHELLFISH", font="patrick-hand", cap_mm=100, technique="whitewash", z_m=[1.45, 1.6], source="as above", kind="Read"),
    dict(shop="fish_market", surface="window glass", text="SMOKED FISH", font="patrick-hand", cap_mm=100, technique="whitewash", z_m=[1.95, 2.1], source="as above", kind="Read"),
    dict(shop="fish_market", surface="side-door fanlight", text="3", font="oswald", cap_mm=110, technique="white paint, red shade", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="ritas", surface="toplight panes, one word to a pane", text="WATCHES", font="old-standard-tt-bold", cap_mm=90, technique="gold leaf, black shade 4 mm", z_m=2.64, source="Judgement", kind="Judgement"),
    dict(shop="ritas", surface="toplight panes", text="JEWELLERY", font="old-standard-tt-bold", cap_mm=90, technique="gold leaf, black shade 4 mm", z_m=2.64, source="Judgement", kind="Judgement"),
    dict(shop="ritas", surface="toplight panes", text="LOANS", font="old-standard-tt-bold", cap_mm=90, technique="gold leaf, black shade 4 mm", z_m=2.64, source="Judgement", kind="Judgement"),
    dict(shop="ritas", surface="side-door fanlight", text="5", font="abril-fatface", cap_mm=110, technique="gold leaf, black shade", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="empty_unit", surface="whole window", text="", font="", cap_mm=0, technique="whitewash wash, brush arcs, nothing legible (ruled 3 Oct: whole window whitewashed); the bills on it are the posters' family", z_m=None, source="DECISIONS.md 3 Oct", kind="Read"),
    dict(shop="empty_unit", surface="side-door fanlight", text="7", font="oswald", cap_mm=110, technique="paint, flaking", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="steam_laundry", surface="window glass, upper left", text="SERVICE WASHES", font="jost", cap_mm=80, technique="white cut vinyl", z_m=2.05, source="Judgement", kind="Judgement"),
    dict(shop="steam_laundry", surface="side-door fanlight", text="9", font="jost", cap_mm=110, technique="white vinyl", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="grocer", surface="side-door fanlight", text="11", font="josefin-sans", cap_mm=110, technique="gold leaf", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="newsagent", surface="shop-door glass", text="NEWSPAPERS · MAGAZINES", font="libre-franklin", cap_mm=60, technique="white cut vinyl", z_m=1.35, source="Judgement", kind="Judgement"),
    dict(shop="newsagent", surface="side-door fanlight", text="18", font="libre-franklin", cap_mm=110, technique="cream vinyl", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="ironmonger", surface="toplight panes, middle pane", text="EST. 1884", font="libre-baskerville", cap_mm=60, technique="gold leaf, black shade 3 mm", z_m=2.64, source="proposed year", kind="Judgement"),
    dict(shop="ironmonger", surface="side-door fanlight", text="16", font="libre-baskerville", cap_mm=110, technique="gold leaf", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="tea_rooms", surface="window glass, upper right", text="Home Baking", font="fraunces", cap_mm=120, technique="gold leaf on the inside face, shaded black 3 mm", z_m=1.9, source="Judgement", kind="Judgement"),
    dict(shop="tea_rooms", surface="side-door fanlight", text="14", font="fraunces", cap_mm=110, technique="gold leaf", z_m=2.18, source="proposed number", kind="Judgement"),
    dict(shop="chandler", surface="toplight panes, middle pane", text="EST. 1879", font="alfa-slab-one", cap_mm=60, technique="gold leaf, black shade 3 mm", z_m=2.64, source="proposed year", kind="Judgement"),
    dict(shop="chandler", surface="side-door fanlight", text="13", font="alfa-slab-one", cap_mm=110, technique="gold leaf", z_m=2.18, source="proposed number", kind="Judgement"),
]

SMALL_PANELS = [
    dict(id="letting_board", shop="empty_unit", size_mm=[900, 450], centre_on_board_mm=[CX, 275], face="white", text="TO LET", font="libre-franklin", weight=800, cap_mm=130,
         colour="vinyl_red", fixing="four screws through the board, slightly askew (2 degrees); a rust run under each lower screw", exists="board_to_let.png (PT Sans); the font here is an OFL replacement, no agent and no number are minted",
         kind="Judgement"),
    dict(id="hours_plate", shops=["ritas", "fish_market", "steam_laundry", "newsagent", "tea_rooms"], size_mm=[300, 190],
         where="on the shop door's glass or the pilaster, centre 1.45 m up",
         text_rule="read the shop's hours from production/specs/hook-cast.json (Mon-Sat from 'hours', Sunday where it has one) and set them as 'MON-SAT 9-5.30' lines; Wednesday half-day as its own line where the cast has one",
         font="libre-franklin", weight=700, cap_mm=24, technique="white enamel plate, black letters, blue border 4 mm, rolled edge 3 mm, chips to black iron at the corners",
         kind="Judgement", note="The hours are the town's; the target gives the plate, not the words."),
]

# --------------------------------------------------------------------------------------------
# 6. Photo-measured template and Hook-sheet numbers (the main photograph is P1).
# --------------------------------------------------------------------------------------------
P1 = dict(
    id="P1", file="P1-leadenhall-chamberlain-board-elevation.jpg",
    what="Poly Haven 'Leadenhall Market' (CC0, Andreas Mischok, taken 2019-05-19), 16K panorama as the 8192 x 4096 tone-mapped JPG, a rectilinear view 110 degrees wide at yaw 90, pitch 0 (3600 x 2400), so a level, square-on elevation of the heritage-restored fronts. Used for the craft only: board proportions, letter height, keyline, shade, numerals. The names on it are a real business's and are NEVER copied.",
    view=dict(yaw_deg=90, pitch_deg=0, hfov_deg=110, size_px=[3600, 2400], horizon_row_px=1200),
    # all in pixels of that 3600 x 2400 view
    px=dict(field_top=179, field_bottom=326, field_left=1230, field_right=2418,
            keyline_top_y=190.5, keyline_bottom_y=311.0, keyline_left_x=1252.0, keyline_right_x=2396.0, keyline_px=[4, 3],
            cap_top=227.0, cap_bottom=272.0, text_x0=1492.0, text_x1=2123.0,
            numeral_left=[1277.0, 1354.0], numeral_right=[2271.0, 2350.0], numeral_top=229.0, numeral_bottom=270.0,
            shade_px=4.5, door_leaf_top=790.0, door_leaf_bottom=1482.0, base_row=1505.0, bead_top=154.0),
    preview=dict(file="P1-leadenhall-chamberlain-board-elevation.jpg", crop_box_in_view_px=[1150, 120, 2450, 400], scale=round(1200.0 / 1300.0, 6)),
    scale_note="scale fitted on ONE dimension: the door leaf (692 px) taken as 2.1 to 2.3 m gives 3.03 to 3.32 mm/px, so the lettered field (147 px) is 0.45 to 0.49 m; the panorama's camera height would have to be 0.93 m for that, which is low but not impossible for a pole-mounted rig; every ratio below is scale-free",
    error_px=3.0,
)
SHEET = dict(
    id="H1", file="H1-hook-sheet-mickeys-board-measure.jpg",
    what="production/reference/hook-sheet.png (2048 x 1088; image-model sheet, approved for mood, palette and composition; photographs win where they disagree)",
    px=dict(board_top=500, board_bottom=548, letters_top=513, letters_bottom=546, letters_x0=630, letters_x1=746, board_left=302, board_right=813),
    colours=dict(board_mean=[62, 75, 87], board_p10=[48, 60, 70], board_p90=[80, 91, 102], gilt_mean=[167, 149, 109], gilt_p90=[193, 171, 130],
                 white_board=[204, 204, 204], dark_board=[99, 81, 72], cream_board=[128, 101, 98]),
    ratios=dict(cap_over_board=round(33 / 48, 3), width_over_cap=round(116 / 33, 2), letter_centre_along_board=round((688 - 302) / (813 - 302), 3)),
    note="the sheet's board is seen obliquely round a bay window, so only vertical ratios and colours are used; its lettering is the one the sheet has, nothing else on it is legible",
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
    # start bottom edge at (x0+r, y0), go right; corners: concave arcs centred on the rectangle corners
    arc(x1, y0, 180, 90)      # bottom-right: from (x1-r,y0) up to (x1,y0+r)
    arc(x1, y1, 270, 180)     # top-right
    arc(x0, y1, 360, 270)     # top-left
    arc(x0, y0, 90, 0)        # bottom-left
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
    elif k == "box":
        ox0, oy0, ox1, oy1 = b["outer_mm"]
        f = b["frame_mm"]
        sh.append(dict(kind="rect", role="box_frame", colour=b["colour"], box=[ox0, oy0, ox1, oy1]))
        sh.append(dict(kind="rect", role="box_face", colour=b["face_colour"], box=[ox0 + f, oy0 + f, ox1 - f, oy1 - f]))
        b["face_mm"] = [ox0 + f, oy0 + f, ox1 - f, oy1 - f]
    elif k == "glass_slab":
        ox0, oy0, ox1, oy1 = b["outer_mm"]
        e = b["edge_mm"]
        sh.append(dict(kind="rect", role="slab_edge", colour=b["colour"], box=[ox0, oy0, ox1, oy1]))
        sh.append(dict(kind="rect", role="slab_face", colour="deco_green_glass", box=[ox0 + e, oy0 + e, ox1 - e, oy1 - e]))
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
    elif k == "scallops":
        x = b["x_mm"][0] + b["radius_mm"]
        cy = (b["y_mm"][0] + b["y_mm"][1]) / 2
        while x <= b["x_mm"][1] - b["radius_mm"]:
            sh.append(dict(kind="circle", role="scallop", colour=b["colour"], c=[round(x, 1), cy], r=b["radius_mm"]))
            x += b["pitch_mm"]
        sh.append(dict(kind="rect", role="rule", colour=b["colour"], box=[b["x_mm"][0], b["y_mm"][1] + 10, b["x_mm"][1], b["y_mm"][1] + 16]))
        b["panel_mm"] = [b["x_mm"][0], b["y_mm"][1] + 16, b["x_mm"][1], FIELD[3]]
    elif k == "rope":
        i = b["inset_mm"]
        x0, y0, x1, y1 = FIELD[0] + i, FIELD[1] + i, FIELD[2] - i, FIELD[3] - i
        sh.append(dict(kind="polyline", role="rope", colour=b["colour"], width_mm=b["rope_mm"], twist_pitch_mm=b["pitch_mm"], pts=rounded_rect_pts(x0, y0, x1, y1, b["corner_radius_mm"])))
        b["panel_mm"] = [x0 + b["rope_mm"], y0 + b["rope_mm"], x1 - b["rope_mm"], y1 - b["rope_mm"]]
    return sh


def compute_shop(s):
    g = PALETTE[s["ground"]["colour"]]
    ground_for_contrast = g["srgb_1990"]
    if s["border"] and s["border"]["kind"] == "box":
        ground_for_contrast = PALETTE[s["border"]["face_colour"]]["srgb_1990"]
    out_blocks = []
    for b in s["blocks"]:
        box, size = measure(b["font"], b["weight"], b["text"], b["cap_mm"], b["tracking_em"])
        x0r, ybr, x1r, ytr = box
        if b["anchor"] == "centre":
            ox = b["x_mm"] - (x0r + x1r) / 2
        elif b["anchor"] == "left":
            ox = b["x_mm"] - x0r
        else:
            ox = b["x_mm"] - x1r
        ink = [round(ox + x0r, 1), round(b["baseline_mm"] + ybr, 1), round(ox + x1r, 1), round(b["baseline_mm"] + ytr, 1)]
        eff = list(ink)
        d = 0.0
        if b.get("embolden_mm"):
            e_ = b["embolden_mm"]
            ink = [round(ink[0] - e_, 1), round(ink[1] - e_, 1), round(ink[2] + e_, 1), round(ink[3] + e_, 1)]
            eff = list(ink)
        if b["shade"]:
            d = b["shade"]["d_mm"]
            eff[2] += d
            eff[1] -= d
        if b.get("outline"):
            o = b["outline"]["w_mm"]
            eff = [eff[0] - o, eff[1] - o, eff[2] + o, eff[3] + o]
        j = b["jitter"]
        if j:
            m = j["baseline_mm"] + 0.01 * (ink[2] - ink[0]) * j["advance_pct"] / 1.5
            eff = [eff[0] - m, eff[1] - j["baseline_mm"], eff[2] + m, eff[3] + j["baseline_mm"]]
        face = PALETTE[b["face"]]["srgb_1990"]
        cr = contrast(face, ground_for_contrast)
        out_blocks.append(dict(b, ink_box_mm=ink, effects_box_mm=[round(v, 1) for v in eff], width_mm=round(ink[2] - ink[0], 1),
                               size_px_per_em=round(size, 2), cap_ratio=round(cap_ratio(b["font"], b["weight"]), 4),
                               contrast_1990=round(cr, 2), face_1990=face, ground_1990=ground_for_contrast,
                               origin_x_mm=round(ox, 1), cap_over_field=round(b["cap_mm"] / (FIELD[3] - FIELD[1]), 3)))
    s2 = dict(s)
    s2["blocks"] = out_blocks
    s2["shapes"] = shapes_for(s2)
    return s2


def overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


SHOPS_C = [compute_shop(s) for s in SHOPS]

# checks that need the shop's own numbers
for s in SHOPS_C:
    bl = s["blocks"]
    s["overlaps"] = [[a["id"], b["id"]] for i, a in enumerate(bl) for b in bl[i + 1:] if overlap(a["effects_box_mm"], b["effects_box_mm"])]
    s["min_margin_mm"] = None
    if bl:
        m = []
        for b in bl:
            e = b["effects_box_mm"]
            m += [e[0] - SAFE[0], e[1] - SAFE[1], SAFE[2] - e[2], SAFE[3] - e[3]]
        s["min_margin_mm"] = round(min(m), 1)
    # fill ratio of the main line
    if bl:
        main = [b for b in bl if b["role"] == "name"][0]
        s["name_fill_of_field_height"] = main["cap_over_field"]
        s["name_width_of_board"] = round(main["width_mm"] / BOARD_W, 3)

# approved words: every string that may appear on any fascia, glass, panel, projecting sign (exact strings)
APPROVED = set()
for s in SHOPS_C:
    for b in s["blocks"]:
        APPROVED.add(b["text"])
for p in PROJECTING:
    APPROVED.add(p["faces"]["text"] if "faces" in p else "")
for g in GLASS:
    if g["text"]:
        APPROVED.add(g["text"])
for sp in SMALL_PANELS:
    if "text" in sp and sp["id"] == "letting_board":
        APPROVED.add(sp["text"])
APPROVED.discard("")
APPROVED_PARTS = sorted({w for t in APPROVED for w in t.replace("·", " ").split()})

FORBIDDEN = dict(
    alcohol_gambling_children=["ALE", "BEER", "WINE", "LAGER", "SPIRITS", "WHISKY", "GIN", "BAR", "PUB", "INN", "TAVERN", "OFF-LICENCE", "BET", "BETS", "BETTING", "BOOKMAKER", "POOLS", "BINGO", "LOTTERY", "CASINO", "ARCADE", "CHILD", "CHILDREN", "KIDS", "SCHOOL", "TOYS"],
    real_marks=["ROYAL MAIL", "POST OFFICE", "TELECOM", "BT", "ER", "TESCO", "SAINSBURY", "BOOTS", "WOOLWORTHS", "WH SMITH", "MARLBORO", "SILK CUT", "PERSIL", "TIDE", "OMO"],
    names_not_minted=["CHAMBERLAIN", "BARBOUR", "REISS", "LUC", "PIZZA", "EXPRESS"],
    note="the last list is the real business names on the measured photograph P1: they may never appear on any fascia; the first two lists are the content rule and the brand rule; production/specs and ledger/Assets/Scripts/Core/RealWorld.cs hold the full real-world list the gate checks",
)

# distinctness
ids = [s["id"] for s in SHOPS_C]
pairs = []
for i in range(len(SHOPS_C)):
    for j in range(i + 1, len(SHOPS_C)):
        a, b = SHOPS_C[i], SHOPS_C[j]
        ga = PALETTE[a["ground"]["colour"]]["srgb_1990"]
        gb = PALETTE[b["ground"]["colour"]]["srgb_1990"]
        if a["border"] and a["border"]["kind"] == "box":
            ga = PALETTE["acrylic_white"]["srgb_1990"]
        if b["border"] and b["border"]["kind"] == "box":
            gb = PALETTE["acrylic_white"]["srgb_1990"]
        fa = a["blocks"][0]["font"] if a["blocks"] else None
        fb = b["blocks"][0]["font"] if b["blocks"] else None
        fca = PALETTE[a["blocks"][0]["face"]]["srgb_1990"] if a["blocks"] else None
        fcb = PALETTE[b["blocks"][0]["face"]]["srgb_1990"] if b["blocks"] else None
        face_dE = round(dE(fca, fcb), 1) if fca and fcb else None
        ba = (a["border"] or {}).get("kind")
        bb = (b["border"] or {}).get("kind")
        pairs.append(dict(a=a["id"], b=b["id"], ground_dE=round(dE(ga, gb), 1), same_font=(fa is not None and fa == fb), same_construction=a["construction_kind"] == b["construction_kind"], face_dE=face_dE, same_border=(ba == bb)))
DISTINCT = dict(
    rule="every pair differs in aged ground by dE76 >= 14; no two fascias share a name-line font; and two fascias of the same construction kind also differ in name-face colour by dE >= 25 or in border kind",
    min_ground_dE=min(p["ground_dE"] for p in pairs), pairs=pairs,
    violations=[p for p in pairs if p["ground_dE"] < 14 or p["same_font"] or (p["same_construction"] and p["face_dE"] is not None and p["face_dE"] < 25 and p["same_border"])],
)

TEXTURES = dict(
    px_per_mm=1, size_px=[BOARD_W, BOARD_H], alt_px_per_mm=2,
    maps=[dict(id="base_colour", encoding="sRGB 8-bit", note="paint, gilt, vinyl and glass colours, aged"),
          dict(id="roughness", encoding="linear 8-bit, 0-1", note="per layer values in each shop's ground and block 'technique'; gilt 0.25-0.40, gloss paint 0.35-0.6, chalked 0.6-0.8, acrylic 0.35, glass 0.05-0.10, vinyl 0.45"),
          dict(id="metallic", encoding="linear 8-bit 0 or 1", note="1 on gold leaf, chrome strips and bronze frame; 0 elsewhere (gilt paint on the balls 0.8)"),
          dict(id="height", encoding="8-bit, 128 = board face, 1 mm over 127 steps", note="letter paint ridge +0.2 mm, keyline +0.15, vinyl +0.08, gilt +0.05, paint loss to substrate -0.3 mm (-0.5 on a bare board), box-sign frame +3 (frame_mm wide), glass face 0"),
          dict(id="emissive", encoding="sRGB 8-bit, only where lit", note="steam_laundry only: face colour x 1 when lit; tube banding; one dead tube"),
          dict(id="layers_manifest", encoding="JSON", note="the renderer writes, per text block, the string, font, size, anchor, ink box and colours it drew: the checks read it")],
)

# ------------------------------------------------------------------------------------------
# 8. The checks unit 4.1's automatic check runs on a rendered fascia texture.
# ------------------------------------------------------------------------------------------
CHECKS = []


def chk(id_, name, scope, measure_, expected, tol, unit, method, layer="pixels", why=""):
    CHECKS.append(dict(id=id_, name=name, scope=scope, layer=layer, measure=measure_, expected=expected, tolerance=tol, unit=unit, method=method, why=why))


chk("G1", "texture size", "every fascia", "width and height of the base-colour image", [BOARD_W, BOARD_H], 0, "px at 1 px/mm (double at 2)", "image size", "image",
    "the board is the kit's 5.41 x 0.55 m; one pixel is one millimetre so a letter's height in pixels is its height in mm")
chk("G2", "frame band", "every painted board", "mean L* of the outer 24 mm top strip minus the 24 mm strip just inside it, and bottom likewise", dict(top_dL=[3, 14], bottom_dL=[-14, -2]), 0, "L*", "strip means of the ground only (text, border and ghost masked out)", "pixels",
    "the baked bevel of the board's frame: lit on top, shaded below (Judgement; the kit's board is a plain box)")
chk("G3", "no repeated word", "every fascia", "each string of the layers manifest appears once; no two ink boxes on one board have the same string", 1, 0, "count", "count strings in the manifest", "manifest",
    "the 3 Sept image-model fascia and the game's FRESH FISH FRESH FISH tiled twice (shop-fronts-whole-2026-10-08.jpg); a board is one picture, not a tile")
chk("G4", "words", "every fascia and glass layer", "every string in the manifest is in approved_words (exact); no forbidden_patterns hit (case-insensitive, whole word)", True, 0, "bool", "set test on the manifest", "manifest",
    "no proprietor name that is not minted; no real mark; the content rule")
chk("G5", "no tiling period", "every ground", "the ground's autocorrelation (text and border masked), at lags 600 to 5000 mm along the board", dict(max_peak=0.55), 0, "correlation", "FFT autocorrelation of L* of the ground only", "pixels",
    "a 5.4 m board must not read as a 1 m texture repeated")
chk("G6", "grain direction", "painted timber boards", "the ground's structure tensor, dominant orientation", dict(angle_deg_from_horizontal=[0, 8]), 0, "deg", "structure tensor on the ground's L* at 4 to 40 mm", "pixels",
    "boards are planed along their length; chips and paint loss follow the grain (P2: median aspect 3.6)")
chk("G7", "distinct fascias", "the ten boards together", "pairwise dE76 between the aged ground medians; shared name-line fonts; shared construction kinds", DISTINCT["rule"], 0, "rule", "see distinctness in target.json", "pixels+json",
    "so the street reads as ten owners, not one designer")
chk("G8", "contrast of every name line", "every text block", "WCAG contrast ratio between the median face colour and the median ground colour just outside the glyphs (a 4 mm ring beyond the shade)", "see each block's contrast_1990", "0.85 x nominal minimum", "ratio", "contrast of two medians", "pixels")
chk("G9", "relief present", "applied letters; vinyl; gilded", "mean height-map step across a glyph edge", dict(applied_mm=[8, 18], gilded_mm=[0.02, 0.15], vinyl_mm=[0.04, 0.2], painted_mm=[0.1, 0.35]), 0, "mm", "height map at glyph edges", "pixels")
for s in SHOPS_C:
    sid = s["id"]
    g = PALETTE[s["ground"]["colour"]]
    gg = g["srgb_1990"]
    if s["border"] and s["border"]["kind"] == "box":
        gg = PALETTE[s["border"]["face_colour"]]["srgb_1990"]
    chk(f"{sid}.ground", f"{sid}: ground colour", sid, "median sRGB of the ground mask (everything not text, border, ghost, shade, or box frame)", gg, 9.0, "dE76", "median in Lab then dE76 to the target", "pixels",
        f"{PALETTE[s['ground']['colour']]['plain']}")
    if s["blocks"]:
        for b in s["blocks"]:
            bid = f"{sid}.{b['id']}"
            chk(f"{bid}.cap", f"{bid}: cap height", sid, "height of the H-shaped capital (or the T of Tea Rooms) in the layers manifest, in mm", b["cap_mm"], max(2.0, round(0.03 * b["cap_mm"], 1)), "mm", "manifest cap_mm, then confirmed on pixels: rows between the top of the flat-topped capitals and the baseline", "manifest+pixels")
            chk(f"{bid}.width", f"{bid}: ink width", sid, "width of the string's ink box", b["width_mm"], round(max(6.0, 0.04 * b["width_mm"]), 1), "mm", "manifest ink box", "manifest",
                "the font file's real advance widths with the tracking given; hand jitter adds up to 1.5 per cent")
            chk(f"{bid}.fit", f"{bid}: inside the safe zone", sid, "ink box including shade, outline and hand jitter against the safe rectangle", dict(safe_mm=SAFE, min_margin_mm=0), 0, "mm", "min distance from the box to each safe edge >= 0 (the safe rectangle already keeps 150 mm off the ends and 40 mm off the top and bottom)", "manifest")
            chk(f"{bid}.contrast", f"{bid}: contrast", sid, "WCAG ratio, aged face median to aged ground median", b["contrast_1990"], f"not below {round(0.85 * b['contrast_1990'], 2)} and not below 2.2", "ratio", "median face (glyph interior eroded 2 px) vs median ring", "pixels")
            chk(f"{bid}.face", f"{bid}: face colour", sid, "median sRGB of the glyph interior (eroded 2 px)", b["face_1990"], 14.0, "dE76", "median in Lab", "pixels")
            if b["shade"]:
                sc = PALETTE[b["shade"]["colour"]]["srgb_1990"]
                chk(f"{bid}.shade", f"{bid}: block shade", sid, "median colour of the pixels in the shade zone (the glyph shifted along the shade vector, minus the glyph) and the zone's width along (+1,-1)", dict(colour=sc, d_mm=b["shade"]["d_mm"]), dict(dE=16.0, d_mm=2.0), "dE76 / mm", "morphological difference of the manifest's glyph mask shifted by (d,-d)", "pixels",
                    "sign-writer's block shade, 45 degrees down and to the right (P1: 4.5 px of a 45 px cap = 0.10 cap)")
    if s["border"]:
        chk(f"{sid}.border", f"{sid}: border / panel", sid, "the border's lines, found as the long thin features of colour as given, positions and widths", dict(kind=s["border"]["kind"], panel_mm=s["border"].get("panel_mm") or s["border"].get("face_mm")), 4.0, "mm", "line detection on the border colour mask; compare with the shapes in target.json", "pixels")
    a = s["age"]
    chk(f"{sid}.age", f"{sid}: paint loss", sid, "area of paint-loss pixels (the substrate or undercoat showing) over the board face; the median aspect of the loss patches (along/across)", dict(loss_fraction=a["loss_fraction"], aspect_median_min=2.0, eqd_mm_median=[4, 16]),
        dict(loss_fraction_abs=0.012, loss_fraction_rel=0.5), "fraction", "classify loss pixels by the substrate colour; label; measure", "pixels",
        "the shape is P2's (median aspect 3.6, equivalent diameter 9 mm); the amount is Judgement")
    if s["lit"] == "tubes":
        chk(f"{sid}.emissive", f"{sid}: lit face", sid, "emissive map: face coverage; tube bands; the dead tube", dict(face_coverage=0.97, band_dL_pct=6, dead_tube_mm=[500, 700], end_dim_pct=12), 0.03, "fraction", "emissive map statistics", "pixels")
chk("rita.lit", "ritas: lit at night", "ritas", "the board is NOT lit (the window is: DECISIONS 1 Oct); no emissive on the board", True, 0, "bool", "emissive map absent or zero", "pixels")


# --------------------------------------------------------------------------------------------
# 9. Assemble target.json
# --------------------------------------------------------------------------------------------
import hashlib


def ofl_hash(d):
    p = os.path.join(FONT_DIR, d, "OFL.txt")
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] if os.path.exists(p) else None


FONT_ROWS = {}
for k, v in FONTS.items():
    FONT_ROWS[k] = dict(
        family=v["family"], file_in_google_fonts_repo=f"ofl/{v['dir']}/{v['file']}",
        ofl_url=f"https://raw.githubusercontent.com/google/fonts/main/ofl/{v['dir']}/OFL.txt", ofl_read="8 Oct 2026, whole file, header 'SIL OPEN FONT LICENSE Version 1.1'",
        ofl_sha256_16=ofl_hash(v["dir"]), designer=v["designer"], reserved_font_name=v["rfn"],
        rendering_note="letters are RENDERED into pictures; the OFL puts no restriction on a picture made with the font (earlier note FAQ 1.1/1.13); never modify and redistribute the font file itself",
        in_production_fonts=v["in_repo"], looks_like=v["looks_like"], axes=v["axes"] or None)
FONT_ROWS["patrick-hand"] = dict(family="Patrick Hand", file_in_production_fonts="production/fonts/patrick-hand/PatrickHand-Regular.ttf", ofl="production/fonts/patrick-hand/OFL.txt",
                                 looks_like="neat hand printing; stands in for the fishmonger's whitewash hand with the jitter given in the glass rows")
FONT_ROWS["_not_used"] = dict(overpass="Overpass is the American Highway Gothic and is NOT to be used (asset plan note 0)",
                              not_ofl="no Apache or GPL font (Special Elite, Gillius ADF), and no Transport, Gill Sans, Futura, Helvetica or Franklin file: Jost, Libre Franklin and Oswald are the OFL stand-ins")

SOURCES = [
    dict(id="P1", url="https://api.polyhaven.com/files/leadenhall_market  (tone-mapped JPG at https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/leadenhall_market.jpg)", read="2026-10-08",
         author="Andreas Mischok (Poly Haven)", licence="CC0 1.0 (polyhaven.com/license: 'CC0 means absolute freedom')", taken="2019-05-19 (api info date_taken 1558277880)",
         shows="a covered Victorian arcade in the City of London, heritage-restored: red-painted fascia boards with gilt shaded capitals, numbers at both ends, cut-corner keylines, consoles, gilt window lettering. Real modern business names stand on it and are never copied.",
         period="NOT 1990: 2019 and restored, so used for the craft (proportions, letter height, keyline, shade) and never for colour or wear",
         used=True, what_used="fascia board proportions; keyline inset, thickness and corner; cap height over field; block shade; numerals; tracking. Measured on a rectilinear view of the panorama.", preview="P1-leadenhall-chamberlain-board-elevation.jpg and P1-leadenhall-chamberlain-board-target-on-photo.jpg"),
    dict(id="P2", url="https://polyhaven.com/a/blue_painted_planks (file: https://dl.polyhaven.org/file/ph-assets/Textures/jpg/2k/blue_painted_planks/blue_painted_planks_diff_2k.jpg)", read="2026-10-08",
         author="Rob Tuytel (Poly Haven)", licence="CC0 1.0", taken="published 2018-07-20; photograph date not given",
         shows="weathered blue-painted timber cladding, 1.0 m square, flaking paint, exposed grain", period="undated; weathering, not a fascia",
         used=True, what_used="shape and size of paint-loss patches (elongation along the grain, equivalent diameter), the loss fraction as an UPPER bound", preview="P2-bluepaintedplanks-weathering-measure.jpg"),
    dict(id="P3", url="https://polyhaven.com/a/black_painted_planks", read="2026-10-08", author="Dimitrios Savva (Poly Haven)", licence="CC0 1.0", taken="published 2025-10-15",
         shows="black gloss-painted planks, scuffed and abraded, 1.6 m", period="undated", used=True, what_used="scuff fraction and the luminance range of a worn dark gloss", preview="P3-blackpaintedplanks-scuff-measure.jpg"),
    dict(id="H1", url="production/reference/hook-sheet.png (preview production/previews/hook-sheet-2026-10-05.jpg)", read="2026-10-08", author="the project's image lane (generated)", licence="own work, approved 21 Sep and 5 Oct for mood, palette and composition",
         taken="2026-09 / 10-05", shows="Mickey's slate-blue board with standing gilt capitals, three more fascias (white, dark aubergine, cream)", period="a generated picture of 1990, not a photograph",
         used=True, what_used="Mickey's board and letter colours (measured), cap height over board, lettering over the door", preview="H1-hook-sheet-mickeys-board-measure.jpg"),
    dict(id="G1", url="production/previews/proof-2.6-shop-signs-and-bills-2026-10-04.jpg and shop-fronts-whole-2026-10-08.jpg", read="2026-10-08", author="the project's packaged builds", licence="own work", taken="2026-10-04, 2026-10-08",
         shows="how the fascias stand in the game today: PAWNBROKER and FRESH FISH in 200 mm Marcellus/Old Standard on oxblood, FRESH FISH set twice across the board, LAUNDERETTE cut off, MICKEY'S flat and centred", period="game", used=True, what_used="what is wrong now (TARGET.md section 'What is wrong in the game today')", preview=None),
    dict(id="N1", url="production/research/asset-plan/4-SIGNAGE-AND-WEAR.md; 0-SOURCES-AND-LICENCES.md; SUMMARY.md section 7", read="2026-10-08 (written 2026-10-03)", author="project research helper", licence="own work", taken="n/a",
         shows="the font table, the trades' type, the three generations of 1990 fascia (painted, backlit Perspex, cut vinyl), the proof plan", period="1990", used=True, what_used="font choices, the generation mix", preview=None),
    dict(id="N2", url="production/research/shop-window-interiors/FISHMONGER-2026-10-03.md (Picture Sheffield t13138, 25 Aug 1990; t13140 c.1989)", read="2026-10-08 (earlier note: images looked at by the builder on the PC on 3 Oct, not re-reached here)", author="Picture Sheffield, photographer not named", licence="reference only, LINKED not kept (production/reference/photographs.md)",
         taken="1989 and 1990-08-25", shows="a fishmonger's shopfront: a dark fascia sign-written in red; window glass hand-lettered in white", period="1990, the period", used=True, what_used="the fishmonger's colour way and the whitewash glass; read as an earlier note, not re-measured", preview=None),
    dict(id="N3", url="production/research/casting/notes/names.md section 4 (Peter Marshall's Hull shop-window photographs 1979-1994, Flashbak 14 Nov 2024, captions)", read="2026-10-08 (earlier note)", author="Peter Marshall", licence="photographer copyright, LINKED", taken="1979-1994",
         shows="fascia naming patterns on Hull shops (owner's name + possessive, surname + trade, place names, 'Sail Makers & Ship Chandlers'); painted fascias; metal fronts; patterned tile stallrisers (R05, R09, West Dock Cafe 1981)", period="1979-1994", used=True, what_used="that trade-only boards ('Fresh Meat', 'Boot Repairs', 'Refreshments') existed beside named ones", preview=None),
    dict(id="N4", url="production/research/shopfronts/FRONTAGE-2026-10-06.md; production/art/shopfront-kit/README.md; production/art/fascia-01/01-SPEC-fascia-package.md", read="2026-10-08", author="project research helpers", licence="own work", taken="2026-10-06",
         shows="fascia 0.55 high from 2.85, 0.12 proud, between the consoles (0.295 to 5.705 in a bay); 1930s refits in structural glass; guides' fascia depth envelope; sombre period colours", period="1900-1935 fronts, repainted", used=True, what_used="board size, the glass-panel fascia, colours of the parade", preview=None),
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
    "Peter Marshall's Hull shop-window set 1979-1994 and the Brixton 1987 fishmonger (Flashbak captions led to Flickr): fascia depth, letter height over board, how many fascias are box signs, painted-out boards",
    "Geograph 1996-2000 views of northern parades (Hull, Grimsby, Whitby, Hartlepool) for the three generations side by side and for the bare, painted-out board",
    "Historic England 'Shopping Parades' and 'Commerce and Exchange' selection guide: fascia depths and lettering of 1900-1935 parades",
    "signpainting.co.uk 'Letters Potent: the modern age' and Designing Buildings 'Shop signs': dates of the shift from signwriting to Perspex and vinyl (note 4 had a sign-makers' summary only)",
    "archive.org / HathiTrust trade manuals of sign-writing and gilding (public domain by age): the proportions of shade, the gilding method, the sizes of numerals",
    "Wikimedia Commons categories for UK shop fronts of the 1980s, with the author, licence and date read on each file page",
]

DISAGREEMENTS = [
    dict(id="D1", element="the fishmonger's colour way", book="the game's board and the recipe's wave: oxblood ground with cream letters (make_vignette_2d.py TRADE_FASCIAS; terrace-front.py FASCIA_PAINT index 1)", photograph="Picture Sheffield t13138 (25 Aug 1990, earlier note): a dark fascia sign-written in red", chose="photograph: dark ground, red letters (the wave stays on the piers and frame, not on this board)"),
    dict(id="D2", element="the shade under signwritten letters", book="the game: a near-black copy 3.5 per cent of the cap down and right (make_trade_fascia), for every board", photograph="P1: a solid block shade, 45 degrees down and right, 0.10 of the cap high, colour near-black brown", chose="photograph, and only on boards that were hand-painted or gilded; none on vinyl, applied letters or back-painted glass"),
    dict(id="D3", element="numbers at the board's two ends", book="none of the game's fascias has them", photograph="P1: both ends carry the street number, 0.91 of the name's cap height, 25 to 46 px inside the keyline", chose="photograph, on three shops (Rita's, the ironmonger and the chandler); the numbers are proposed, not minted"),
    dict(id="D4", element="the keyline's corner", book="a plain rectangle (every guide drawing and the 3 Sept batch)", photograph="P1: the keyline's corners are cut by a concave quarter circle about 20 px (0.14 of the lettered field) in radius", chose="photograph, on Rita's"),
    dict(id="D5", element="fascia depth", book="council guides: 'traditional fascias do not exceed 380 mm' (fascia-01 spec, search-channel summary, the PDFs blocked)", photograph="P1: the lettered field is 0.45 to 0.49 m (door-leaf scale), the board with its top bead 0.53 to 0.57 m", chose="the street's 0.55 m stands; the photograph does not support the guides' envelope for a trading parade"),
    dict(id="D6", element="Mickey's name position", book="the game: centred on the board (shop-fronts-whole-2026-10-08.jpg)", photograph="not a photograph: the Hook sheet puts the letters over the door, 0.245 of the board from the door end", chose="the sheet (it governs composition); ONE flag in shops[mickeys].blocks[name].x_mm to centre it if Jafar prefers"),
    dict(id="D7", element="how big the name is", book="the game: 200 mm caps on a 460 mm board (0.43) on every board, trade line 70 mm", photograph="P1: 0.31 of the field (a restrained heritage board); H1: 0.69 (the generated sheet)", chose="between and varied by trade: 0.20 to 0.60 of the field (cap_over_field in each block); the street reads as ten hands"),
]

COULD_NOT_SETTLE = [
    "NO 1990 PHOTOGRAPH OF A FASCIA WAS REACHED TODAY. The only photograph measured is a 2019 restoration of a 19th-century arcade (P1). Letter heights over board, colours, wear and which shops had box signs rest on that, on the Hook sheet, on earlier notes (cited, not re-measured) and on judgement. The list of what to read when the network opens is in would_read_when_network_opens.",
    "Where the newsagent and the ironmonger stand: the recipe (terrace-front.py SIGN_OVERRIDE, a west block turned a half turn) puts the newsagent at street x 36-42 and the ironmonger at 30-36; hook-cast.json puts the newsagent's pension counter at x 32 and 'Hal's shop, the same block's far end' at x 39 (Hal 'keeps the coin shop that sells no coins'). One of them is wrong; the sign targets are keyed by trade so a swap is a rename. A town task, not mine to rule.",
    "Which shop is Hal's. hook-cast.json has Hal's shop at x 39 but DECISIONS 3 Oct has no coin shop in the west row. If the town keeps Hal's, it needs a fascia of its own (HAL'S is minted in the cast; its trade line is the town's to say) and the street has eleven, as RULINGS 2 Oct counts twelve shopfronts and the scene has ten bays plus Mickey's.",
    "The shops' street numbers and the EST. years are proposed (Judgement), not minted; the town should mint or strike them (one line each in DECISIONS.md). The fascias work without them: delete the 'end' and 'est' blocks.",
    "No proprietor name exists for the grocer, newsagent, ironmonger, tea room or chandler, so each board says only its trade (that is correct, and the target says so); a minted name would add one line to each board and move nothing else.",
    "Absolute scale of P1 (door leaf taken as 2.1 to 2.3 m): the camera would be at 0.93 m, low for a panorama; only ratios are used from P1. If a source gives the door leaf or the camera height the board's absolute size comes out of it.",
    "The existing glass number 0632 960418 (shop-room.py) uses 0632, which from memory (not checked) was Newcastle upon Tyne's STD code until 1992; Meridian is fictional, so the town may want a made-up code. Not changed here: it is the shop-room family's.",
    "Pavement-level legibility: letter heights are chosen by judgement for 3 to 15 m reading; the game camera sees them at about 5 degrees above eye level; nobody has looked at them at the game's exposure (that is for the build's own review).",
    "Fascia-lit-at-night policy beyond the launderette: only the pawnbroker's WINDOW is ruled lit (DECISIONS 1 Oct). The box sign's emissive is specified; whether it is on after dark follows the town's hours (it closes 17.30), not this target.",
]

PHOTO_TEMPLATE = dict(
    note="the ratios the photograph P1 gives, laid on our board for the overlay and for the 'photo wins' check; fitted on one dimension only: the lettered field's height",
    field_height_px=P1["px"]["field_bottom"] - P1["px"]["field_top"],
    ratios=dict(
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
    ),
    error_px=P1["error_px"],
)

MATERIALS = dict(
    note="roughness is 0 (mirror) to 1 (dry chalk); metallic 0 or 1 (an alloy or gilt paint may carry 0.8). A fresh paint layer on top of a chalked ground is glossier than the ground: letters are 0.08 to 0.15 below their ground's roughness until aged.",
    gold_leaf_on_size=dict(roughness=0.30, plain="bright, slightly satin", metallic=1.0, colour="gold_leaf", chip="size, 150,110,50 (yellow-brown), roughness 0.7, metallic 0"),
    applied_brass_gilt=dict(roughness=0.38, plain="satin, dirt in the corners", metallic=0.85, colour="brass_gilt", flank="brass_side, roughness 0.5"),
    signwriters_enamel=dict(roughness="ground minus 0.10 (0.35 to 0.5), 0.55 once chalked", plain="semi-gloss going flat", metallic=0.0),
    cut_vinyl=dict(roughness=0.45, plain="satin plastic", metallic=0.0, edge="a 0.08 mm step with a 1-pixel highlight"),
    back_painted_glass=dict(roughness=0.08, plain="polished glass over matte paint", metallic=0.0, letters="0.12, seen through the glass"),
    acrylic_face=dict(roughness=0.35, plain="semi-gloss plastic, a little orange-peel", metallic=0.0, translucent=True),
    anodised_bronze=dict(roughness=0.35, plain="satin metal", metallic=1.0),
    chrome_strip=dict(roughness=0.15, plain="bright metal, pitted", metallic=1.0),
    hemp_rope=dict(roughness=0.80, plain="dry fibre", metallic=0.0),
    whitewash=dict(roughness=0.90, plain="chalk", metallic=0.0, opacity=0.85),
    bare_timber=dict(roughness=0.85, plain="dry grey wood", metallic=0.0),
    paint_loss=dict(roughness=0.85, plain="undercoat or bare wood showing", metallic=0.0, height_mm=-0.3),
    wrought_iron=dict(roughness=0.60, plain="black paint on iron, rust at fixings", metallic=0.5),
    ball_gilt_paint=dict(roughness=0.38, plain="gilt paint on sheet metal, scuffed", metallic=0.8),
)
VARIANTS = [
    dict(id="V1", name="ten boards", differs="the ten shops of this file, one board each; none repeats (distinctness)", applies_to="all"),
    dict(id="V2", name="day and night", differs="steam_laundry: the box sign's face is lit (emissive) when the shop is open, dark and dull when shut; every other board is unlit (only Rita's WINDOW is ruled lit, DECISIONS 1 Oct)", applies_to="steam_laundry"),
    dict(id="V3", name="proposed marks off", differs="strip the street numbers on the boards (blocks with role 'end'; the numerals' place is then empty panel) and the glass 'est.' and number rows if the town does not mint them", applies_to="ritas, ironmonger, chandler and the glass rows"),
    dict(id="V4", name="Mickey's centred", differs="MICKEY\u2019S centred on the board (x 2705) instead of over the door (x 1355), as the game has it today", applies_to="mickeys"),
    dict(id="V5", name="a minted name", differs="when the town mints a proprietor's name, ONE more line (cap 0.5 of the trade line's) goes above the trade line on that board; nothing else moves", applies_to="grocer, newsagent, ironmonger, tea_rooms, chandler"),
    dict(id="V6", name="the street box", differs="if the street keeps its 6.0 m box, centre the 5410 texture on it and paint 295 mm of plain frame colour at each end", applies_to="all"),
]

TARGET = dict(
    schema="ledger.cloud-week-42.target.fascia-signs/1",
    family="fascia-signs",
    status="WRITTEN 8 October 2026 (cloud week 42) by a target writer from the kit's own numbers, one photograph measured today (P1), two weathered-timber photographs (P2, P3), the Hook sheet and the project's earlier notes. Unit 4.1 builds from this file alone. self_check below is written by self_check.py.",
    summary_line="Ten fascias for Quay Street, each its own trade, hand and construction (applied brass letters, sign-written red on dark, gilt on oxblood, a painted-out bare board, a lit plastic box, Art Deco glass, cut vinyl, shaded black Roman, soft cream roman on teal, white Egyptian on navy), on the kit's 5410 x 550 mm board at 1 mm a pixel, with proportions from one measured photograph and the rest said plainly to be judgement.",
    units=dict(board="millimetres, x from the board's left as a viewer facing it sees it (east shops: low street x on the left; west shops: low street x on the right), y UP from the board's bottom edge",
               geometry="metres where a part hangs in the street (projecting signs, glass heights)", colour="sRGB 0-255", contrast="WCAG relative-luminance ratio (L1+0.05)/(L2+0.05)", dE="CIE76 on Lab D65"),
    kinds=dict(Read="printed in a source", Scaled="measured off a drawing or the game's own files", Photo="measured on a photograph today", Sheet="measured on the Hook sheet today (a generated picture)",
               Derived="computed from the above", Judgement="mine; to be overturned by a better source"),
    board=dict(width_mm=BOARD_W, height_mm=BOARD_H, proud_of_wall_mm=120, z_bottom_m=2.85, z_top_m=3.40, between_consoles_in_bay_m=[0.295, 5.705],
               street_box_mm=[6000, 550], frame_mm=FRAME, field_mm=FIELD, safe_mm=SAFE, px_per_mm=1,
               source="SCENE-SLOTS.md (fascia 2.85 to 3.40, 0.55, 0.12 proud); production/art/shopfront-kit/README.md ('0.295 to 5.705 in Rita's bay'); production/specs/vignette-scene.json (fascia_bottom_m 2.85, fascia_projection_m 0.12, bay_width_m 6.0)",
               note="The kit puts the fascia BETWEEN the consoles, 5.41 m; the street's box today runs the full 6.0 m across the pilaster heads and buries the consoles' feet (README, 'For the session'). This target is for the 5.41 m board. If the street keeps its 6.0 m box, centre the 5410 texture on it and keep 295 mm of plain frame colour each side; nothing in the layouts reaches the outer 150 mm.",
               frame_note="the outer 24 mm is the board's own frame: baked highlight on top (+3 to +14 L*), shade below (-14 to -2 L*); the cornice's shadow and the grime gradient are the wear material's",
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
                     edge="a 3 to 5 mm 'matt' edge: the gilt is edged with the shade or the ground so it cuts crisply; chips show the size (yellow-brown 150,110,50)"),
        shade=dict(style="block shade, 45 degrees down and to the right, length 0.10 of the cap (P1: 4.5 px of 45); the shade is the extrusion of the glyph, not a blurred drop; colour per block", kind="Photo"),
        keyline=dict(thickness_over_field=PHOTO_TEMPLATE["ratios"]["keyline_thickness"], inset_over_field=[PHOTO_TEMPLATE["ratios"]["keyline_top_inset"], PHOTO_TEMPLATE["ratios"]["keyline_bottom_inset"]], corner="concave quarter circle", radius_over_field=PHOTO_TEMPLATE["ratios"]["corner_radius"], kind="Photo"),
        spacing=dict(word_space_em=0.32, note="word spaces are the font's, widened by the tracking; the middle dot separator has a word space each side"),
        optical=dict(centre="the block is centred on the ink, not on the advance box; P1's name sits 1.4 per cent of the panel width left of the panel's centre, so +-1.5 per cent is the hand's tolerance", baseline_hang_mm="round capitals (C, O, S, G) overshoot the baseline and the cap line by 1.6 per cent of the cap"),
    ),
    materials=MATERIALS,
    variants=VARIANTS,
    shops=SHOPS_C,
    projecting_signs=PROJECTING,
    glass_lettering=GLASS,
    small_panels=SMALL_PANELS,
    approved_words=sorted(APPROVED),
    approved_word_parts=APPROVED_PARTS,
    forbidden_patterns=FORBIDDEN,
    distinctness=DISTINCT,
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
    print("min ground dE:", DISTINCT["min_ground_dE"])
