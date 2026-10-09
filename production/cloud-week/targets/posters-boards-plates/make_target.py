"""Author tool: writes target.json for Quay Street's paper and small boards (cloud week 42, 8 October 2026).

    /home/user/.bpyenv/bin/python make_target.py [--fonts DIR]

Three 2D units in one target:
  4.2  posters and notices (fly-posters, shop-window cards, council, police and Harbour Board notices,
       the poll-tax bills, the Tivoli's bills, the chapel hall's bills, the ferry timetable);
  4.3  "To Let" boards (the empty unit's board and the flats' boards, an invented agent);
  4.4  street name plates.

The hand-made decisions live in the tables below. Everything that can be computed is computed here and
written down, so that target_drawing.py and self_check.py can read target.json ALONE: ink widths from the
real OFL font files, cap heights, contrast ratios, aged colours, weekdays of every dated bill, the plates'
lengths, the checks' nominal values.

The fonts are read from DIR (default: $PBP_FONTS, then the scratch folder this was written in, then
production/fonts for the ones the repository already holds). They are NOT stored in git and NOT added to
production/fonts/. Fetch the missing ones with self_check.py --fetch-fonts DIR (raw.githubusercontent.com).

Evidence kinds on every number that matters (the sibling targets' convention):
  Read = printed in a source file; Scaled = measured off a drawing or the game's own files;
  Photo = measured on a photograph today; Derived = computed from the above;
  Judgement = the writer's, to be overturned by a better source; Lead = a search summary, never a number.
"""
import datetime
import json
import math
import os
import re
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
SCRATCH_FONTS = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/posters/fonts"
FONT_DIR = os.environ.get("PBP_FONTS", SCRATCH_FONTS)
if "--fonts" in sys.argv:
    FONT_DIR = sys.argv[sys.argv.index("--fonts") + 1]
REPO_FONTS = ROOT / "production" / "fonts"

# --------------------------------------------------------------------------------------------
# 0. Colour maths (sRGB, D65): contrast, dE, ageing.
# --------------------------------------------------------------------------------------------


def s2l(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def l2s(l):
    l = max(0.0, min(1.0, l))
    return 255.0 * (12.92 * l if l <= 0.0031308 else 1.055 * l ** (1 / 2.4) - 0.055)


def rel_lum(rgb):
    r, g, b = [s2l(v) for v in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a, b):
    la, lb = rel_lum(a), rel_lum(b)
    hi, lo = max(la, lb), min(la, lb)
    return round((hi + 0.05) / (lo + 0.05), 2)


def lab(rgb):
    r, g, b = [s2l(v) for v in rgb]
    x = (0.4124 * r + 0.3576 * g + 0.1805 * b) / 0.95047
    y = (0.2126 * r + 0.7152 * g + 0.0722 * b)
    z = (0.0193 * r + 0.1192 * g + 0.9505 * b) / 1.08883
    f = lambda t: t ** (1 / 3) if t > 0.008856 else 7.787 * t + 16 / 116
    fx, fy, fz = f(x), f(y), f(z)
    return (116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz))


def dE(a, b):
    la, lb = lab(a), lab(b)
    return round(math.sqrt(sum((p - q) ** 2 for p, q in zip(la, lb))), 1)


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def rgb_hex(c):
    return "#%02X%02X%02X" % tuple(c)


# Ageing. Four classes, by the days a sheet has been on the wall. Judgement throughout (no 1990 photograph
# of a pasted bill was reached); the shape of the numbers follows the usual order of fastness: fluorescent
# dyes go first, then red and magenta, yellow, blue, and black carbon last.
AGE = {
    "A": dict(label="fresh, 0 to 7 days", t_days=3, grime=0.00, yellow=0.00),
    "B": dict(label="weeks, 8 to 35 days", t_days=18, grime=0.05, yellow=0.20),
    "C": dict(label="months, 36 to 120 days", t_days=70, grime=0.12, yellow=0.50),
    "D": dict(label="old, over 120 days", t_days=200, grime=0.22, yellow=1.00),
}
GRIME = (62, 58, 52)
YELLOWED = (214, 200, 168)

# Stocks: fresh sRGB; what a fluorescent or coloured stock fades towards; the half-life-like tau in days.
STOCKS = {
    "white_poster": dict(rgb=(236, 235, 228), fade_to=None, tau=None, name="white poster paper", gsm=80),
    "white_bond": dict(rgb=(240, 240, 234), fade_to=None, tau=None, name="white copier paper, A4 or A3", gsm=80),
    "cream": dict(rgb=(236, 226, 196), fade_to=None, tau=None, name="cream poster paper", gsm=80),
    "fluor_yellow": dict(rgb=(250, 238, 52), fade_to=(236, 226, 150), tau=60, name="fluorescent yellow poster paper", gsm=80),
    "fluor_orange": dict(rgb=(255, 120, 52), fade_to=(238, 176, 130), tau=60, name="fluorescent orange poster paper", gsm=80),
    "pale_pink": dict(rgb=(240, 206, 210), fade_to=(236, 220, 214), tau=150, name="pale pink poster paper", gsm=80),
    "pale_green": dict(rgb=(204, 226, 202), fade_to=(222, 228, 210), tau=200, name="pale green copier paper", gsm=80),
    "pale_yellow": dict(rgb=(246, 238, 176), fade_to=(238, 232, 196), tau=150, name="pale yellow copier paper", gsm=80),
    "pale_blue": dict(rgb=(204, 220, 238), fade_to=(222, 228, 232), tau=200, name="pale blue poster paper", gsm=80),
    "white_card": dict(rgb=(242, 240, 232), fade_to=None, tau=None, name="white card, about 250 gsm", gsm=250),
    "buff_card": dict(rgb=(224, 204, 160), fade_to=None, tau=None, name="buff card, about 250 gsm", gsm=250),
    "index_white": dict(rgb=(244, 242, 234), fade_to=None, tau=None, name="white record card", gsm=200),
    "index_pink": dict(rgb=(240, 196, 204), fade_to=(236, 214, 212), tau=150, name="pink record card", gsm=200),
    "index_blue": dict(rgb=(196, 214, 236), fade_to=(220, 226, 230), tau=200, name="blue record card", gsm=200),
    "index_yellow": dict(rgb=(246, 232, 150), fade_to=(238, 230, 190), tau=150, name="yellow record card", gsm=200),
    "index_green": dict(rgb=(196, 226, 196), fade_to=(222, 228, 208), tau=200, name="green record card", gsm=200),
    "star_yellow": dict(rgb=(252, 240, 40), fade_to=(238, 226, 140), tau=50, name="fluorescent yellow star card", gsm=200),
    "star_pink": dict(rgb=(255, 92, 140), fade_to=(238, 176, 176), tau=45, name="fluorescent pink star card", gsm=200),
    "star_orange": dict(rgb=(255, 130, 40), fade_to=(238, 180, 130), tau=50, name="fluorescent orange star card", gsm=200),
}
# Inks: fresh sRGB and tau in days.
INKS = {
    "black": dict(rgb=(24, 24, 27), tau=1500, name="black ink"),
    "red": dict(rgb=(196, 34, 38), tau=150, name="poster red"),
    "blue": dict(rgb=(28, 58, 138), tau=400, name="poster blue"),
    "navy": dict(rgb=(26, 38, 82), tau=900, name="navy"),
    "toner": dict(rgb=(30, 30, 33), tau=4000, name="photocopier toner"),
    "typed": dict(rgb=(34, 34, 38), tau=1500, name="typewriter ribbon, black"),
    "felt_black": dict(rgb=(30, 30, 36), tau=900, name="felt pen, black"),
    "felt_red": dict(rgb=(200, 32, 40), tau=120, name="felt pen, red"),
    "felt_blue": dict(rgb=(28, 62, 150), tau=300, name="felt pen, blue"),
    "felt_green": dict(rgb=(24, 110, 60), tau=300, name="felt pen, green"),
    "ballpoint_blue": dict(rgb=(30, 52, 150), tau=250, name="ballpoint, blue"),
    "ballpoint_black": dict(rgb=(40, 40, 46), tau=900, name="ballpoint, black"),
    "paper": dict(rgb=None, tau=None, name="the unprinted stock (reversed-out lettering)"),
}
# Painted and enamelled parts (plates, boards): no fade, a grime film and a chalk lift by class.
PAINTS = {
    "enamel_white": dict(rgb=(238, 238, 230), name="vitreous enamel, white"),
    "enamel_blue": dict(rgb=(24, 68, 140), name="vitreous enamel, Harbour Board blue"),
    "enamel_red": dict(rgb=(176, 30, 34), name="vitreous enamel, red"),
    "enamel_black": dict(rgb=(20, 20, 22), name="vitreous enamel, black"),
    "plate_white": dict(rgb=(232, 230, 220), name="plate paint, white, oil gloss gone satin"),
    "plate_black": dict(rgb=(22, 22, 26), name="plate paint, black"),
    "agent_white": dict(rgb=(236, 236, 230), name="agent's board, white gloss"),
    "agent_navy": dict(rgb=(28, 46, 94), name="agent's navy"),
    "agent_red": dict(rgb=(178, 34, 40), name="agent's red"),
    "agent_green": dict(rgb=(30, 92, 66), name="OPEN face, green"),
    "lamp_orange": dict(rgb=(240, 170, 64), name="lamplight orange, the Tivoli's title colour on dark art"),
    "case_timber": dict(rgb=(74, 50, 34), name="varnished timber, dark"),
    "cork": dict(rgb=(176, 138, 96), name="cork board"),
    "sleeve": dict(rgb=(226, 230, 232), name="polythene sleeve highlight"),
    "vinyl_white": dict(rgb=(238, 238, 232), name="printed adhesive vinyl, white"),
}


def age_paint(rgb, cls):
    a = AGE[cls]
    c = mix(rgb, YELLOWED, 0.25 * a["yellow"])
    return mix(c, GRIME, a["grime"] * 1.1)


def age_stock(key, cls):
    s = STOCKS[key]
    a = AGE[cls]
    rgb = s["rgb"]
    if s["fade_to"] is not None:
        f = 1 - math.exp(-a["t_days"] / s["tau"])
        rgb = mix(rgb, s["fade_to"], f)
    rgb = mix(rgb, YELLOWED, 0.30 * a["yellow"])
    return mix(rgb, GRIME, a["grime"])


def age_ink(key, stock, cls):
    """Aged colour of an ink on a stock, in class cls. 'paper' is the unprinted stock itself."""
    if key == "paper":
        return age_stock(stock, cls)
    ink = INKS[key]
    a = AGE[cls]
    f = 1 - math.exp(-a["t_days"] / ink["tau"])
    base = mix(ink["rgb"], age_stock(stock, cls), f)
    return mix(base, GRIME, a["grime"] * 0.35)


# --------------------------------------------------------------------------------------------
# 1. Fonts. Eleven OFL families, each OFL.txt read whole on raw.githubusercontent.com (8 Oct 2026).
# --------------------------------------------------------------------------------------------
FONTS = {
    "marcellus-sc": dict(family="Marcellus SC", file="marcellus-sc/MarcellusSC-Regular.ttf", dir="marcellussc", axes={},
                         designer="Astigmatic", rfn="Marcellus", in_repo=True,
                         looks_like="flared humanist capitals after Roman inscriptions; the street plates' letter (ruled 30 Sep, allowlist 7)"),
    "oswald": dict(family="Oswald", file="oswald/Oswald[wght].ttf", dir="oswald", axes={"Weight": None}, designer="Vernon Adams, Kalapi Gajjar, Cyreal",
                   rfn=None, in_repo=True, looks_like="condensed gothic capitals: the jobbing printer's and the signwriter's block letter"),
    "jost": dict(family="Jost", file="jost/Jost[wght].ttf", dir="jost", axes={"Weight": None}, designer="Owen Earl", rfn=None, in_repo=True,
                 looks_like="Futura-like geometric sans: estate agents' and chemists' boards of the 1980s"),
    "libre-franklin": dict(family="Libre Franklin", file="libre-franklin/LibreFranklin[wght].ttf", dir="librefranklin", axes={"Weight": None},
                           designer="Impallari Type", rfn=None, in_repo=True, looks_like="Franklin Gothic: newsagents', notices, enamel signs"),
    "alfa-slab-one": dict(family="Alfa Slab One", file="alfa-slab-one/AlfaSlabOne-Regular.ttf", dir="alfaslabone", axes={}, designer="JM Sole",
                          rfn="Alfa Slab", in_repo=True, looks_like="fat Egyptian slab: market and sale posters"),
    "fraunces": dict(family="Fraunces", file="fraunces/Fraunces[SOFT,WONK,opsz,wght].ttf", dir="fraunces",
                     axes={"Weight": None, "Softness": 100, "Optical Size": 144, "Wonky": 0}, designer="Undercase Type", rfn=None, in_repo=True,
                     looks_like="soft heavy roman near Cooper and Windsor: the 1970s-80s comedy bill"),
    "old-standard-tt": dict(family="Old Standard TT", file="old-standard-tt/OldStandard-Bold.ttf", dir="oldstandardtt", axes={},
                            designer="Alexey Kryukov", rfn=None, in_repo=True, looks_like="Victorian modern roman: chapel hall and market bills"),
    "old-standard-tt-regular": dict(family="Old Standard TT", file="evening-paper/OldStandard-Regular.ttf", dir="oldstandardtt", axes={},
                                    designer="Alexey Kryukov", rfn=None, in_repo=True, looks_like="the regular cut, for body lines"),
    "old-standard-tt-italic": dict(family="Old Standard TT", file="evening-paper/OldStandard-Italic.ttf", dir="oldstandardtt", axes={},
                                   designer="Alexey Kryukov", rfn=None, in_repo=True, looks_like="the italic, for 'and' and 'by'"),
    "abril-fatface": dict(family="Abril Fatface", file="abril-fatface/AbrilFatface-Regular.ttf", dir="abrilfatface", axes={}, designer="TypeTogether",
                          rfn="Abril, Abril Fatface", in_repo=True, looks_like="fat-face Didone poster capitals"),
    "josefin-sans": dict(family="Josefin Sans", file="josefin-sans/JosefinSans[wght].ttf", dir="josefinsans", axes={"Weight": None},
                         designer="Santiago Orozco", rfn="Josefin Sans", in_repo=True, looks_like="Art Deco geometric capitals: the Tivoli (founded 1937)"),
    "archivo": dict(family="Archivo", file="Archivo-var.ttf", dir="archivo", axes={"Weight": None, "Width": 100}, designer="Omnibus-Type", rfn=None,
                    in_repo=False, looks_like="neutral grotesque: council notices, enamel signs, the police appeal"),
    "courier-prime": dict(family="Courier Prime", file="CourierPrime-Regular.ttf", dir="courierprime", axes={}, designer="Alan Dague-Greene", rfn=None,
                          in_repo=False, looks_like="IBM Courier: typed notices (Harbour Board, police, council)"),
    "courier-prime-bold": dict(family="Courier Prime", file="CourierPrime-Bold.ttf", dir="courierprime", axes={}, designer="Alan Dague-Greene",
                               rfn=None, in_repo=False, looks_like="Courier struck twice for a heading"),
    "libre-baskerville": dict(family="Libre Baskerville", file="LibreBaskerville-var.ttf", dir="librebaskerville", axes={"Weight": None},
                              designer="Impallari Type", rfn="Libre Baskerville", in_repo=False,
                              looks_like="Baskerville text roman: typeset official notices"),
    "patrick-hand": dict(family="Patrick Hand", file="patrick-hand/PatrickHand-Regular.ttf", dir="patrickhand", axes={}, designer="Patrick Wagesreiter",
                         rfn=None, in_repo=True, looks_like="neat adult print capitals and figures: felt-pen and ballpoint cards"),
}
_fcache = {}


def font_path(key):
    spec = FONTS[key]
    for base in (Path(FONT_DIR), REPO_FONTS):
        p = base / spec["file"]
        if p.exists():
            return p
        p2 = base / Path(spec["file"]).name
        if p2.exists():
            return p2
    raise FileNotFoundError("font %s (%s) not found under %s or %s" % (key, spec["file"], FONT_DIR, REPO_FONTS))


def font(key, weight, px):
    k = (key, weight, round(px, 2))
    if k in _fcache:
        return _fcache[k]
    spec = FONTS[key]
    f = ImageFont.truetype(str(font_path(key)), px, layout_engine=ImageFont.Layout.RAQM)
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
    """Ink box of a one-line string in mm relative to its pen origin on the baseline: (x0, y_bottom, x1, y_top), y up.
    Rendered glyph by glyph with the font's own advance and tracking added, 1 px = 1 mm of a scaled-up render, ink read off the pixels."""
    r = cap_ratio(key, weight)
    px = cap_mm / r
    # render at 4x for sub-mm precision on small caps
    sc = 4.0 if cap_mm < 30 else 1.0
    f = font(key, weight, px * sc)
    trk = tracking_em * px * sc
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    pad = int(px * sc) + 12
    Wd = int(xs[-1] + f.getlength(text[-1]) + 2 * pad)
    Hd = int(px * sc * 1.7) + 2 * pad
    base = pad + int(px * sc * 1.2)
    img = Image.new("L", (Wd, Hd), 0)
    d = ImageDraw.Draw(img)
    for i, ch in enumerate(text):
        if ch != " ":
            d.text((pad + xs[i], base), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
    rows = np.where(a.any(axis=1))[0]
    cols = np.where(a.any(axis=0))[0]
    return ((round(float(cols.min() - pad) / sc, 1), round(float(base - (rows.max() + 1)) / sc, 1),
             round(float(cols.max() + 1 - pad) / sc, 1), round(float(base - rows.min()) / sc, 1)), px)


def capfit(key, weight, text, width, tracking_em=0.0, lo=2.0, hi=260.0):
    """Largest cap height (0.5 mm steps) whose ink width is at most width mm."""
    a, b = int(lo * 2), int(hi * 2)
    while a < b:
        mid = (a + b + 1) // 2
        bb, _ = measure(key, weight, text, mid / 2.0, tracking_em)
        if bb[2] - bb[0] <= width:
            a = mid
        else:
            b = mid - 1
    return a / 2.0


_missing_glyph_cache = {}


def glyph_ok(key, ch):
    """True when the font has a real glyph for ch (renders differently from the notdef box)."""
    if ch in "  ":
        return True
    k = (key, ch)
    if k in _missing_glyph_cache:
        return _missing_glyph_cache[k]
    f = font(key, 400, 60)
    def mask(c):
        im = Image.new("L", (120, 120), 0)
        ImageDraw.Draw(im).text((10, 90), c, font=f, fill=255, anchor="ls")
        return np.asarray(im)
    m = mask(ch)
    bad = mask("")
    ok = bool(m.any()) and not np.array_equal(m, bad)
    _missing_glyph_cache[k] = ok
    return ok


# --------------------------------------------------------------------------------------------
# 2. The calendar. Every dated bill carries its weekday, checked against the 1990 calendar.
# --------------------------------------------------------------------------------------------
YEAR = 1990
MONTHS = {"JANUARY": 1, "FEBRUARY": 2, "MARCH": 3, "APRIL": 4, "MAY": 5, "JUNE": 6, "JULY": 7, "AUGUST": 8, "SEPTEMBER": 9,
          "OCTOBER": 10, "NOVEMBER": 11, "DECEMBER": 12}
DAYS = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]


def weekday_name(d, m, year=YEAR):
    return DAYS[datetime.date(year, m, d).weekday()]


def dated(d, m, short=False, year=YEAR):
    """'SATURDAY 20 OCTOBER' for 20 October 1990 (the weekday is computed, never typed)."""
    names = {v: k for k, v in MONTHS.items()}
    return "%s %d %s" % (weekday_name(d, m, year), d, names[m])


# --------------------------------------------------------------------------------------------
# 3. Items. One dict per item; blocks are single lines at an explicit baseline.
# --------------------------------------------------------------------------------------------
ITEMS = []
FORMATS = {
    # British paper and poster sizes of the period. Imperial names are exact multiples of 25.4 mm (Derived).
    "crown": dict(w=381, h=508, std="Crown 15 x 20 in (Derived: 25.4 mm to the inch)"),
    "double_crown": dict(w=508, h=762, std="Double Crown 20 x 30 in, portrait (Derived)"),
    "quad_crown": dict(w=1016, h=762, std="Quad Crown 40 x 30 in, landscape (Derived; the British 'quad')"),
    "four_sheet": dict(w=1016, h=1524, std="Four-sheet 40 x 60 in, portrait (Derived)"),
    "A3": dict(w=297, h=420, std="ISO 216 A3"),
    "A4": dict(w=210, h=297, std="ISO 216 A4"),
    "A5": dict(w=148, h=210, std="ISO 216 A5"),
    "A6": dict(w=105, h=148, std="ISO 216 A6"),
    "A2": dict(w=420, h=594, std="ISO 216 A2"),
    "A5L": dict(w=210, h=148, std="ISO 216 A5 turned landscape"),
    "A6L": dict(w=148, h=105, std="ISO 216 A6 turned landscape"),
}


def new_item(id_, unit, part, title, w, h, stock=None, process=None, ppm=2, margin=14, fmt=None, kind="sheet", **kw):
    it = dict(id=id_, unit=unit, part=part, title=title, kind=kind, format=dict(name=fmt, w_mm=w, h_mm=h,
              std=(FORMATS[fmt]["std"] if fmt in FORMATS else "as stated")),
              px_per_mm=ppm, stock=stock, process=process, safe_mm=[margin, margin, w - margin, h - margin],
              blocks=[], shapes=[], art=[], placements=[], variants={}, wear={}, notes=[], words=[], proposed_names=[])
    it.update(kw)
    ITEMS.append(it)
    return it


def stock_colours(stock):
    if stock is None:
        return None
    return dict(key=stock, name=STOCKS[stock]["name"], fresh=list(STOCKS[stock]["rgb"]),
                aged={c: list(age_stock(stock, c)) for c in AGE})


def ink_colours(key, stock):
    if key == "paper":
        return dict(key="paper", fresh=list(STOCKS[stock]["rgb"]), aged={c: list(age_stock(stock, c)) for c in AGE})
    return dict(key=key, fresh=list(INKS[key]["rgb"]), aged={c: list(age_ink(key, stock, c)) for c in AGE})


def ground_colours(item, on):
    """The colour behind a block: 'stock' (the sheet), 'ink:KEY' (a printed solid), 'paint:KEY' (a painted board)."""
    if on is None or on == "stock":
        return dict(on="stock", fresh=list(STOCKS[item["stock"]]["rgb"]), aged={c: list(age_stock(item["stock"], c)) for c in AGE})
    kind, key = on.split(":")
    if kind == "art":
        rgb = tuple(int(v) for v in key.split(","))
        return dict(on=on, fresh=list(rgb), aged={c: list(age_paint(rgb, c)) for c in AGE}, note="the art's guaranteed colour behind this line (a scrim is laid over the picture there)")
    if kind == "ink":
        return dict(on=on, fresh=list(INKS[key]["rgb"]), aged={c: list(age_ink(key, item["stock"], c)) for c in AGE})
    return dict(on=on, fresh=list(PAINTS[key]["rgb"]), aged={c: list(age_paint(PAINTS[key]["rgb"], c)) for c in AGE})


def paint_colours(key):
    return dict(key=key, name=PAINTS[key]["name"], fresh=list(PAINTS[key]["rgb"]), aged={c: list(age_paint(PAINTS[key]["rgb"], c)) for c in AGE})


def T(item, id_, text, fkey, wt, cap, base, x, anchor="centre", ink="black", on="stock", trk=0.0, tech=None, hand=None, role="text",
      rot=0.0, overlap_ok=False, ink_paint=None, note=None, min_contrast=None):
    """Add one line of lettering. anchor: 'centre' | 'left' | 'right' refers to the INK box. x and base in item mm (x from the
    viewer's left, base is the baseline measured UP from the item's bottom edge)."""
    bb, px = measure(fkey, wt, text, cap, trk)
    wd = bb[2] - bb[0]
    if anchor == "centre":
        ox = x - (bb[0] + bb[2]) / 2.0
    elif anchor == "left":
        ox = x - bb[0]
    else:
        ox = x - bb[2]
    box = [round(ox + bb[0], 1), round(base + bb[1], 1), round(ox + bb[2], 1), round(base + bb[3], 1)]
    for ch in text:
        assert glyph_ok(fkey, ch), "glyph %r missing in %s (%s)" % (ch, fkey, text)
    if ink_paint:
        col = paint_colours(ink_paint)
        gc = ground_colours(item, on)
        cr = {c: contrast(col["aged"][c], gc["aged"][c]) for c in AGE}
    else:
        col = ink_colours(ink, item["stock"])
        gc = ground_colours(item, on)
        cr = {c: contrast(col["aged"][c], gc["aged"][c]) for c in AGE}
    b = dict(id=id_, text=text, font=fkey, weight=wt, cap_mm=cap, tracking_em=trk, anchor=anchor, x_mm=round(x, 1), baseline_mm=round(base, 1),
             origin_x_mm=round(ox, 1), ink_box_mm=box, width_mm=round(wd, 1), size_px_per_em=round(px, 2), cap_ratio=round(cap_ratio(fkey, wt), 3),
             ink=(ink_paint or ink), on=on, ink_colour=col, ground=gc, contrast=cr, role=role, technique=tech, hand=hand, rotation_deg=rot,
             overlap_ok=overlap_ok, note=note, min_contrast=min_contrast)
    item["blocks"].append(b)
    item["words"].append(text)
    return b


def S(item, id_, kind, box=None, pts=None, fill="black", on="stock", note=None, **kw):
    """A printed or painted shape. kind: rect | rule | roundel | poly | frame | star."""
    sh = dict(id=id_, kind=kind, box_mm=box, pts_mm=pts, fill=fill, note=note)
    sh.update(kw)
    item["shapes"].append(sh)
    return sh


def stack(item, prefix, lines, cx, top, anchor="centre", maxw=None, left=None, fill_bottom=None):
    """Lay lines top-down. Each line: dict(text, f, w, cap, gap, ink, on, trk, tech, hand, role). Returns the y of the cursor below the last line.
    anchor centre uses cx; anchor left uses left. Baseline = cursor - cap (capitals sit on the baseline; descenders hang into the gap).
    fill_bottom: stretch the gaps (not the letters) so that the last baseline lands on this y."""
    prepared = []
    for ln in lines:
        if "fitw" in ln:
            ln = dict(ln, cap=capfit(ln["f"], ln["w"], ln["text"], ln["fitw"], ln.get("trk", 0.0)))
        cap = ln["cap"]
        if maxw is not None and not ln.get("nofit"):
            bb0, _ = measure(ln["f"], ln["w"], ln["text"], cap, ln.get("trk", 0.0))
            w0 = bb0[2] - bb0[0]
            if w0 > maxw:
                cap = math.floor(cap * maxw / w0 * 0.995 * 2) / 2.0
                ln = dict(ln, cap_requested=ln["cap"])
        prepared.append(dict(ln, cap=cap))
    gaps = [ln.get("gap", ln["cap"] * 0.35) for ln in prepared]
    if fill_bottom is not None:
        used = sum(ln["cap"] for ln in prepared) + sum(gaps[:-1])
        avail = top - fill_bottom
        if avail > used and sum(gaps[:-1]) > 0:
            k = 1.0 + (avail - used) / sum(gaps[:-1])
            gaps = [g * k for g in gaps[:-1]] + [gaps[-1]]
    y = top
    for i, ln in enumerate(prepared):
        cap = ln["cap"]
        base = y - cap
        x = cx if anchor == "centre" else left
        b = T(item, "%s%d" % (prefix, i + 1) if "id" not in ln else ln["id"], ln["text"], ln["f"], ln["w"], cap, base, x, anchor=anchor,
              ink=ln.get("ink", "black"), on=ln.get("on", "stock"), trk=ln.get("trk", 0.0), tech=ln.get("tech"), hand=ln.get("hand"),
              role=ln.get("role", "text"), ink_paint=ln.get("paint"), note=ln.get("note"))
        if ln.get("cap_requested"):
            b["cap_requested_mm"] = ln["cap_requested"]
        y = base - gaps[i]
    return y


def check_fit(item):
    """Every ink box inside the safe zone; report overlaps between blocks that are not allowed to overlap."""
    sx0, sy0, sx1, sy1 = item["safe_mm"]
    problems = []
    for b in item["blocks"]:
        x0, y0, x1, y1 = b["ink_box_mm"]
        if b.get("ghost") or b.get("outside_safe_ok"):
            continue
        if x0 < sx0 - 0.5 or y0 < sy0 - 0.5 or x1 > sx1 + 0.5 or y1 > sy1 + 0.5:
            problems.append("%s/%s outside safe zone %s: box %s" % (item["id"], b["id"], item["safe_mm"], b["ink_box_mm"]))
    bl = item["blocks"]
    for i in range(len(bl)):
        for j in range(i + 1, len(bl)):
            a, c = bl[i], bl[j]
            if a["overlap_ok"] or c["overlap_ok"] or a.get("ghost") or c.get("ghost"):
                continue
            ax0, ay0, ax1, ay1 = a["ink_box_mm"]
            bx0, by0, bx1, by1 = c["ink_box_mm"]
            # ignore descender overlaps of under 4 mm vertically (baseline boxes include tails of Q and J)
            if ax0 < bx1 and bx0 < ax1 and ay0 + 4 < by1 and by0 + 4 < ay1:
                problems.append("%s: blocks %s and %s overlap" % (item["id"], a["id"], c["id"]))
    return problems


# --------------------------------------------------------------------------------------------
# 4. The words that recur. Names the town has not minted are PLACEHOLDERS, listed in PROPOSED and never to
#    reach Jafar's page until the town mints them (RULINGS 3 Oct).
# --------------------------------------------------------------------------------------------
CAMPAIGN = "MERIDIAN AGAINST THE POLL TAX"          # invented local campaign (ruling 3 Oct); name proposed, not minted
HALL = "THE CHAPEL HALL"                            # hook-cast.json: places chapel_hall, "the chapel hall"; no street minted for it
PRINTER = "QUAY PRINT"                              # proposed printer's imprint, not minted
IMPRINT = "Printed by Quay Print, Meridian."
PUBLISHER = "Published by Meridian Against the Poll Tax."
PROPOSED = [
    dict(name="MERIDIAN AGAINST THE POLL TAX", what="the invented local anti-poll-tax campaign (ruling 3 Oct: an invented local campaign, never real parties or people). First proposed by the asset plan note 4, used by the 4 Oct bills.", mint="town task"),
    dict(name="QUAY PRINT", what="the jobbing printer named in the imprint of every printed bill (an imprint was the custom and is expected on political and campaign matter)", mint="town task"),
    dict(name="ARMITAGE & STOBBS", what="the estate agent on the letting boards (the brief asks for a proposed name, marked 'proposed, not minted')", mint="town task"),
    dict(name="THE SANDERLING TRIO", what="the dance band on the chapel hall's bill", mint="town task"),
    dict(name="THE SEA WOLF, MAD MAURICE, TIGER JIM LARKIN, THE BARON", what="four invented ring names on the wrestling bill", mint="town task"),
    dict(name="THE FOURTH WITNESS, A WEEK AT GULLWING", what="two invented films at the Tivoli (Gullwing is a minted district)", mint="town task"),
    dict(name="WHITEWELL, QUAYSIDE TEA", what="two invented goods on hoarding bills (a washday powder and a tea)", mint="town task"),
    dict(name="MARSHLAND PICTURES; A. VENN, R. CORLEY, H. MADDOX", what="the invented studio and three invented credits on the two film bills' billing block", mint="town task"),
    dict(name="THE DRILL HALL", what="the hall where the boxing and wrestling bills are held (generic building, no street given)", mint="town task"),
    dict(name="MR1", what="a placeholder postal district for one variant of the street plates (MR is not a real UK postcode area)", mint="town task; NEVER on his page"),
]


# --------------------------------------------------------------------------------------------
# 5. Printed bills (unit 4.2): the poll-tax set, the chapel hall's, the fights, the market, the Tivoli, the goods.
# --------------------------------------------------------------------------------------------
OSW, FRK, JOS, ALF, FRA, OST, OSTR, ABR, JSF, ARC = ("oswald", "libre-franklin", "jost", "alfa-slab-one", "fraunces", "old-standard-tt",
                                                       "old-standard-tt-regular", "abril-fatface", "josefin-sans", "archivo")
CPR, CPB, LBK, PAT, MAR = "courier-prime", "courier-prime-bold", "libre-baskerville", "patrick-hand", "marcellus-sc"


def L(text, f, w, cap=None, gap=None, ink="black", on="stock", trk=0.0, tech=None, role="text", **kw):
    d = dict(text=text, f=f, w=w, cap=(cap if cap is not None else 10), ink=ink, on=on, trk=trk, tech=tech, role=role)
    if gap is not None:
        d["gap"] = gap
    d.update(kw)
    return d


def imprint(item, text, y=20, cx=None, cap=2.4, ink="black", on="stock"):
    """The printer's imprint, set in 7 point (cap 2.4 mm): legal matter on printed bills, texture at game distance."""
    cx = item["format"]["w_mm"] / 2.0 if cx is None else cx
    return T(item, "imprint", text, FRK, 500, cap, y, cx, "centre", ink=ink, on=on, role="imprint", tech="7 point, below the legibility floor at 3 m by design")


def footer_bar(it, box, text=CAMPAIGN, cap=None, ink="paper", bar_fill="black", f=OSW, w=600, trk=0.06):
    S(it, "footer_bar", "rect", box=box, fill=bar_fill, fill_kind="ink")
    cx = (box[0] + box[2]) / 2.0
    cap = cap or capfit(f, w, text, (box[2] - box[0]) - 24, trk)
    cap = min(cap, 0.55 * (box[3] - box[1]))
    T(it, "campaign", text, f, w, cap, (box[1] + box[3]) / 2.0 - cap / 2.0, cx, "centre", ink=ink, on="ink:" + bar_fill, trk=trk, role="name")


def bill_poll_meeting():
    it = new_item("P01", "4.2", "poll_tax_bills", "Poll tax: public meeting bill", 508, 762, stock="fluor_yellow", process="screen_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("NO", OSW, 700, 190, gap=12, ink="black", tech="screen black"),
        L("POLL TAX", OSW, 700, fitw=462, gap=14, ink="red", tech="screen red", trk=0.02),
    ], 254, 738, fill_bottom=470)
    S(it, "rule_top", "rule", box=[40, y - 4, 468, y + 1], fill="black")
    y = stack(it, "M", [
        L("PUBLIC MEETING", OSW, 600, 34, gap=14, ink="black", trk=0.04),
        L("THURSDAY 25 OCTOBER", OSW, 700, fitw=400, gap=14, ink="red", trk=0.02),
        L("7.30 PM", OSW, 700, 76, gap=16, ink="black"),
        L("THE CHAPEL HALL", OSW, 600, 38, gap=20, ink="black", trk=0.04),
    ], 254, y - 16, fill_bottom=210)
    S(it, "rule_mid", "rule", box=[40, y - 4, 468, y + 1], fill="black")
    y = stack(it, "N", [
        L("WHAT TO DO IF YOU GET A SUMMONS", FRK, 800, fitw=400, gap=8, ink="black", trk=0.03),
        L("EVERYONE WELCOME", FRK, 700, 15, gap=8, ink="black", trk=0.05),
    ], 254, y - 14)
    footer_bar(it, [18, 30, 490, 82])
    imprint(it, PUBLISHER + " " + IMPRINT, y=20)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "skew -1.2 to +1.2 degrees", "red pass shifted 0.3 to 0.8 mm", "one has a top corner torn 60 to 140 mm"])
    it["event"] = dict(date="THURSDAY 25 OCTOBER", d=25, m=10)
    it["bottom_y"] = y
    return it


def bill_dont_pay():
    it = new_item("P02", "4.2", "poll_tax_bills", "Poll tax: don't pay bill", 508, 762, stock="fluor_orange", process="screen_1col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("DON’T", OSW, 700, fitw=440, gap=10, ink="black", tech="screen black"),
        L("PAY", OSW, 700, fitw=330, gap=18, ink="black"),
        L("THE POLL TAX", OSW, 700, fitw=440, gap=16, ink="black", trk=0.03),
    ], 254, 738)
    S(it, "rule_a", "rule", box=[30, y - 2, 478, y + 4], fill="black")
    y = stack(it, "M", [
        L("CAN’T PAY — WON’T PAY", OSW, 600, fitw=440, gap=22, ink="black", trk=0.03),
        L("JOIN US EVERY THURSDAY", FRK, 800, 19, gap=12, ink="black", trk=0.05),
        L("7.30 PM · THE CHAPEL HALL", FRK, 800, 19, gap=10, ink="black", trk=0.05),
    ], 254, y - 18, fill_bottom=130)
    footer_bar(it, [18, 30, 490, 82])
    imprint(it, PUBLISHER + " " + IMPRINT, y=20)
    it["variants"] = dict(n=3, vary=["age class B, C, C", "skew", "one overposted by P03 over its lower third"])
    it["bottom_y"] = y
    return it


def bill_march():
    it = new_item("P03", "4.2", "poll_tax_bills", "Poll tax: march bill", 508, 762, stock="white_poster", process="letterpress_2col", fmt="double_crown", margin=18)
    S(it, "bar_left", "rect", box=[18, 100, 46, 744], fill="red", fill_kind="ink")
    L0 = 64
    y = stack(it, "L", [
        L("MARCH", OSW, 700, fitw=420, gap=12, ink="red", tech="letterpress red"),
        L("AGAINST THE", OSW, 600, 40, gap=8, ink="black", trk=0.06),
        L("POLL TAX", OSW, 700, fitw=420, gap=24, ink="black"),
    ], 0, 738, anchor="left", left=L0)
    y = stack(it, "M", [
        L("SATURDAY", OSW, 700, fitw=330, gap=10, ink="black", trk=0.02),
        L("10 NOVEMBER", OSW, 700, fitw=420, gap=24, ink="black", trk=0.02),
        L("ASSEMBLE 11 AM", OSW, 600, fitw=330, gap=10, ink="black", trk=0.04),
        L("THE EXCHANGE", OSW, 600, fitw=330, gap=24, ink="black", trk=0.04),
        L("BRING YOUR NEIGHBOURS", FRK, 800, 20, gap=8, ink="red", trk=0.04),
        L("BRING A BANNER", FRK, 800, 20, gap=8, ink="red", trk=0.04),
    ], 0, y - 16, anchor="left", left=L0, fill_bottom=118)
    footer_bar(it, [64, 30, 490, 82])
    imprint(it, PUBLISHER + " " + IMPRINT, y=20, cx=277)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "ink density", "overposted by P01 at the foot in one"])
    it["event"] = dict(date=dated(10, 11), d=10, m=11)
    it["bottom_y"] = y
    return it


def bill_summons_a4():
    it = new_item("P04", "4.2", "poll_tax_bills", "Poll tax: summons advice sheet (photocopy)", 210, 297, stock="pale_green", process="photocopy_a4", fmt="A4", margin=10)
    y = stack(it, "L", [
        L("GOT A POLL TAX", ARC, 900, fitw=186, gap=6, ink="toner", tech="Letraset-style heading, photocopied"),
        L("SUMMONS?", ARC, 900, fitw=186, gap=10, ink="toner"),
        L("DON’T PANIC.", ARC, 900, fitw=150, gap=12, ink="toner"),
    ], 105, 284, fill_bottom=190)
    S(it, "rule_a", "rule", box=[12, y + 6, 198, y + 7.6], fill="toner", fill_kind="ink")
    y = stack(it, "M", [
        L("ADVICE EVENING", ARC, 800, 11, gap=6, ink="toner", trk=0.02),
        L("TUESDAY 30 OCTOBER, 7 PM", ARC, 800, 8.5, gap=5, ink="toner"),
        L("THE CHAPEL HALL", ARC, 800, 8.5, gap=12, ink="toner"),
    ], 16, y - 6, anchor="left", left=16)
    typed = ["Bring your summons and any letters you have had.", "We will go through them with you.", "Free and confidential. Come on your own", "or bring a neighbour."]
    for i, t in enumerate(typed):
        T(it, "typed%d" % (i + 1), t, CPR, 400, 2.455, y - 6 - i * 8.47, 16, "left", ink="toner", tech="typed, 10 pitch, photocopied", role="body")
    y2 = y - 6 - len(typed) * 8.47 - 8
    T(it, "campaign", CAMPAIGN, ARC, 800, 6.0, 22, 105, "centre", ink="toner", trk=0.06, role="name", tech="photocopied")
    it["variants"] = dict(n=3, vary=["paper: pale green, pale yellow, white", "skew 0.2 to 1.5 degrees", "toner speckle and a copier edge shadow"])
    it["event"] = dict(date="TUESDAY 30 OCTOBER", d=30, m=10)
    it["bottom_y"] = y2
    return it


def sticker_polltax():
    it = new_item("P05", "4.2", "poll_tax_bills", "Poll tax: sticker, 95 x 60", 95, 60, stock="white_poster", process="sticker_print", fmt=None, margin=4, kind="sticker")
    S(it, "frame", "frame", box=[2, 2, 93, 58], fill="red", fill_kind="ink", width_mm=2.2)
    y = stack(it, "L", [
        L("NO", OSW, 700, 20, gap=3, ink="red"),
        L("POLL TAX", OSW, 700, fitw=76, gap=4, ink="black", trk=0.03),
    ], 47.5, 54)
    T(it, "campaign", CAMPAIGN, OSW, 600, 3.6, 7, 47.5, "centre", ink="black", trk=0.06, role="name")
    it["variants"] = dict(n=2, vary=["on a lamp column, pillar, kiosk or wall: corners lifting, one scratched, one half scraped"])
    it["bottom_y"] = y
    return it


def sticker_cantpay():
    it = new_item("P06", "4.2", "poll_tax_bills", "Poll tax: sticker, 148 x 52", 148, 52, stock="white_poster", process="sticker_print", fmt=None, margin=4, kind="sticker")
    S(it, "bar", "rect", box=[2, 2, 146, 50], fill="black", fill_kind="ink")
    T(it, "slogan", "CAN’T PAY — WON’T PAY", OSW, 700, capfit(OSW, 700, "CAN’T PAY — WON’T PAY", 130, 0.03), 24, 74, "centre", ink="paper", on="ink:black", trk=0.03, role="name")
    T(it, "campaign", CAMPAIGN, OSW, 600, 4.0, 10, 74, "centre", ink="paper", on="ink:black", trk=0.06)
    it["variants"] = dict(n=2, vary=["as P05"])
    return it


OSI = "old-standard-tt-italic"


def bill_jumble():
    it = new_item("J01", "4.2", "chapel_hall", "Jumble sale bill (chapel hall)", 381, 508, stock="pale_pink", process="letterpress_2col", fmt="crown", margin=14)
    S(it, "frame", "frame", box=[12, 12, 369, 496], fill="black", fill_kind="ink", width_mm=3.2, note="two brass rules, 3 pt, mitred at the corners; hairline gaps at the joints")
    y = stack(it, "L", [
        L("GRAND", OST, 700, 34, gap=10, ink="red", trk=0.30, tech="letterpress red"),
        L("JUMBLE SALE", OSW, 700, fitw=320, gap=12, ink="black"),
        L("THE CHAPEL HALL", OSW, 600, 26, gap=16, ink="black", trk=0.08),
    ], 190.5, 486, fill_bottom=380)
    S(it, "rule_a", "rule", box=[40, y - 2, 341, y + 1.2], fill="black")
    y = stack(it, "M", [
        L(dated(20, 10), OSW, 700, fitw=300, gap=10, ink="red", trk=0.02),
        L("DOORS OPEN 2 PM", OSW, 600, 24, gap=18, ink="black", trk=0.06),
        L("CLOTHING · BOOKS · BRIC-A-BRAC · HOUSEHOLD", OSTR, 400, fitw=300, gap=14, ink="black", trk=0.02),
        L("Teas and cakes", OSI, 400, 15, gap=20, ink="black"),
        L("ADMISSION 20p", FRK, 800, 19, gap=12, ink="black", trk=0.05),
        L("IN AID OF THE CHAPEL ROOF FUND", FRK, 700, 10, gap=8, ink="black", trk=0.05),
    ], 190.5, y - 14, fill_bottom=70)
    imprint(it, IMPRINT, y=22)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "skew +-1.5 degrees", "red pass shifted 0.3 to 0.6 mm", "one half-covered by P03 or W01"])
    it["event"] = dict(date=dated(20, 10), d=20, m=10)
    it["bottom_y"] = y
    return it


def bill_dance():
    it = new_item("D01", "4.2", "chapel_hall", "Old-time dance bill (chapel hall)", 508, 762, stock="cream", process="letterpress_2col", fmt="double_crown", margin=18)
    S(it, "frame", "frame", box=[16, 16, 492, 746], fill="blue", fill_kind="ink", width_mm=4.0)
    y = stack(it, "L", [
        L("OLD TIME", OST, 700, fitw=400, gap=8, ink="blue", tech="letterpress blue"),
        L("and", OSI, 400, 26, gap=6, ink="black"),
        L("NEW VOGUE", OST, 700, fitw=400, gap=10, ink="blue"),
        L("DANCING", ALF, 400, fitw=400, gap=22, ink="black"),
    ], 254, 728, fill_bottom=520)
    y = stack(it, "M", [
        L(dated(17, 11), OSW, 700, fitw=360, gap=14, ink="black", trk=0.02),
        L("7.30 TO 11 PM", OSW, 600, 42, gap=16, ink="blue", trk=0.04),
        L("THE CHAPEL HALL", OSW, 600, 30, gap=26, ink="black", trk=0.06),
        L("Music by", OSI, 400, 18, gap=8, ink="black"),
        L("THE SANDERLING TRIO", OST, 700, fitw=360, gap=26, ink="black", trk=0.04),
        L("TEA AND SANDWICHES", FRK, 800, 16, gap=10, ink="black", trk=0.06),
        L("ADMISSION £1.50", FRK, 800, 16, gap=10, ink="black", trk=0.06),
        L("ALL WELCOME", FRK, 800, 16, gap=8, ink="blue", trk=0.08),
    ], 254, y - 20, fill_bottom=60)
    imprint(it, IMPRINT, y=28)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "blue pass shifted 0.3 to 0.7 mm", "skew"])
    it["event"] = dict(date=dated(17, 11), d=17, m=11)
    it["bottom_y"] = y
    return it


def bill_wrestling():
    it = new_item("W01", "4.2", "fights", "All-in wrestling bill", 508, 762, stock="pale_yellow", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("ALL-IN", OSW, 700, 60, gap=8, ink="black", trk=0.12),
        L("WRESTLING", OSW, 700, fitw=460, gap=14, ink="red", tech="letterpress red"),
        L("THE DRILL HALL", OSW, 600, 34, gap=12, ink="black", trk=0.08),
        L(dated(2, 11), OSW, 700, fitw=420, gap=8, ink="black", trk=0.02),
        L("BELL 7.30 PM", OSW, 600, 34, gap=24, ink="red", trk=0.06),
    ], 254, 738, fill_bottom=452)
    S(it, "rule_a", "rule", box=[40, y + 6, 468, y + 9.4], fill="black")
    y = stack(it, "M", [
        L("THE SEA WOLF", OSW, 700, fitw=380, gap=4, ink="black"),
        L("v", OSI, 400, 14, gap=4, ink="red"),
        L("MAD MAURICE", OSW, 700, fitw=380, gap=18, ink="black"),
        L("TIGER JIM LARKIN", OSW, 700, fitw=380, gap=4, ink="black"),
        L("v", OSI, 400, 14, gap=4, ink="red"),
        L("THE BARON", OSW, 700, fitw=300, gap=14, ink="black"),
        L("AND SUPPORT BOUTS", OSW, 600, 20, gap=22, ink="black", trk=0.08),
        L("RINGSIDE £4 · UNRESERVED £2.50", FRK, 800, 17, gap=8, ink="red", trk=0.04),
        L("TICKETS AT THE DOOR", FRK, 700, 14, gap=8, ink="black", trk=0.08),
    ], 254, y - 6, fill_bottom=50)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "red pass shifted", "one with the date line struck through by a hand-painted band (event over): a red felt-pen stripe, NO new words"])
    it["event"] = dict(date=dated(2, 11), d=2, m=11)
    it["bottom_y"] = y
    return it


def bill_boxing():
    it = new_item("B01", "4.2", "fights", "Boxing night bill", 508, 762, stock="pale_blue", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("BOXING", ALF, 400, fitw=440, gap=24, ink="black", tech="letterpress black"),
        L("TEN BOUTS", OSW, 700, fitw=400, gap=34, ink="red", trk=0.06),
        L("THE DRILL HALL", OSW, 600, 44, gap=16, ink="black", trk=0.08),
        L(dated(16, 11), OSW, 700, fitw=440, gap=14, ink="black", trk=0.02),
        L("FIRST BOUT 7.30 PM", OSW, 600, fitw=420, gap=36, ink="red", trk=0.05),
    ], 254, 738, fill_bottom=300)
    S(it, "rule_a", "rule", box=[40, y + 12, 468, y + 15.4], fill="black")
    y = stack(it, "M", [
        L("RINGSIDE £3 · UNRESERVED £1.50", FRK, 800, fitw=440, gap=24, ink="black", trk=0.04),
        L("TICKETS AT THE DOOR", FRK, 700, 18, gap=8, ink="black", trk=0.08),
    ], 254, y - 6, fill_bottom=90)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=2, vary=["age class B, C", "skew"])
    it["event"] = dict(date=dated(16, 11), d=16, m=11)
    it["bottom_y"] = y
    return it


def bill_market():
    it = new_item("M01", "4.2", "market", "Market day bill", 508, 762, stock="white_poster", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("COPPER ROW", ALF, 400, fitw=450, gap=12, ink="blue", tech="letterpress blue"),
        L("MARKET", ALF, 400, fitw=450, gap=30, ink="black"),
        L("TUESDAYS · FRIDAYS · SATURDAYS", OSW, 700, fitw=450, gap=30, ink="black", trk=0.02),
        L("8 AM TO 4 PM", OSW, 700, fitw=400, gap=30, ink="blue"),
    ], 254, 738, fill_bottom=330)
    S(it, "rule_a", "rule", box=[40, y + 12, 468, y + 15.4], fill="black")
    y = stack(it, "M", [
        L("FRUIT · VEG · FISH · HOUSEHOLD · CLOTHING", OSW, 600, fitw=450, gap=30, ink="black", trk=0.04),
        L("NEW STALLS WELCOME", FRK, 800, 20, gap=10, ink="black", trk=0.06),
        L("ENQUIRIES: THE MARKET OFFICE", FRK, 700, 14, gap=8, ink="black", trk=0.06),
    ], 254, y - 10, fill_bottom=70)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=2, vary=["age class B, D (the old one is mostly paste and one torn half)", "skew"])
    it["bottom_y"] = y
    return it


def goods_whitewell():
    it = new_item("G01", "4.2", "goods", "Washday powder four-sheet (invented brand)", 1016, 1524, stock="white_poster", process="litho_4col", fmt="four_sheet", margin=30)
    it["art"].append(dict(id="art", box_mm=[0, 420, 1016, 1524], kind="litho_picture", seed="G01", nominal_rgb=[196, 214, 232],
                          describe="a washing line of white sheets and towels in a bright cold wind over a terraced back-yard wall, the sky pale blue; no people, no faces, no lettering anywhere in the picture",
                          forbidden="people, hands, faces, children, text, numerals, logos, any real product", zone_note="the sheets are the whitest area; the sky is behind the title"))
    S(it, "title_band", "rect", box=[0, 0, 1016, 420], fill="blue", fill_kind="ink")
    T(it, "name", "WHITEWELL", ALF, 400, capfit(ALF, 400, "WHITEWELL", 900), 250, 508, "centre", ink="paper", on="ink:blue", trk=0.02, role="name")
    T(it, "line1", "WASHES WHITE", OSW, 700, 70, 150, 508, "centre", ink="paper", on="ink:blue", trk=0.1, role="line")
    T(it, "line2", "FOR TWIN-TUB, AUTOMATIC AND HAND WASHING", FRK, 700, 24, 90, 508, "centre", ink="paper", on="ink:blue", trk=0.06)
    imprint(it, IMPRINT, y=40, cap=4.0, ink="paper", on="ink:blue")
    it["variants"] = dict(n=2, vary=["age class C, D", "one with the lower half pasted over by P03 and P01"])
    return it


def goods_tea():
    it = new_item("G02", "4.2", "goods", "Tea bill (invented brand)", 508, 762, stock="cream", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("QUAYSIDE", ALF, 400, fitw=440, gap=10, ink="red", tech="letterpress red"),
        L("TEA", ALF, 400, fitw=300, gap=22, ink="black"),
        L("A good strong cup", FRA, 700, fitw=420, gap=24, ink="black"),
    ], 254, 738)
    S(it, "cup", "roundel", box=[134, y - 250, 374, y - 10], fill="red", fill_kind="ink", note="a flat red disc standing for a cup seen from above, a white ring inside; our own drawing, no photograph")
    T(it, "price", "80 BAGS · £1.35", OSW, 700, 52, 100, 254, "centre", ink="black", role="line", trk=0.03)
    imprint(it, IMPRINT, y=30)
    it["variants"] = dict(n=2, vary=["age class B, C", "skew"])
    it["bottom_y"] = y
    return it


def tivoli_witness():
    it = new_item("T01", "4.2", "tivoli", "Tivoli quad: THE FOURTH WITNESS", 1016, 762, stock="white_poster", process="litho_4col", fmt="quad_crown", margin=26)
    it["art"].append(dict(id="art", box_mm=[0, 0, 1016, 762], kind="litho_picture", seed="T01", nominal_rgb=[16, 20, 34],
                          describe="a narrow wet street at night seen from a first-floor window, lamplight in orange pools on the cobbles, a telephone box lit at the far end, rain on the glass in the near corner; dark blue and black with orange; no people, no faces, no lettering",
                          forbidden="people, hands, faces, children, text, numerals, signs, real brands, real places, vehicles with plates",
                          zone_note="the lower third and a top strip must stay dark and low in detail: a scrim is laid there for the words"))
    S(it, "scrim_bottom", "scrim", box=[0, 0, 1016, 300], rgb=[10, 14, 26], alpha_top=0.0, alpha_bottom=0.85, note="gradient, fully dark at the foot")
    S(it, "scrim_top", "scrim", box=[0, 690, 1016, 762], rgb=[10, 14, 26], alpha_top=0.8, alpha_bottom=0.0)
    ART = "art:16,20,34"
    T(it, "tivoli", "THE TIVOLI", JSF, 700, 20, 706, 70, "left", ink_paint="agent_white", on=ART, trk=0.3, role="name")
    T(it, "start", "FROM SUNDAY 21 OCTOBER", JSF, 600, 20, 706, 990, "right", ink_paint="agent_white", on=ART, trk=0.2)
    T(it, "tag", "Somebody saw. Somebody will pay.", FRA, 600, 30, 640, 508, "centre", ink_paint="agent_white", on=ART, role="tagline")
    T(it, "title1", "THE FOURTH", OSW, 700, 128, 250, 70, "left", ink_paint="agent_white", on=ART, trk=0.02, role="title")
    T(it, "title2", "WITNESS", OSW, 700, 128, 98, 70, "left", ink_paint="lamp_orange", on=ART, trk=0.02, role="title")
    T(it, "billing", "A MARSHLAND PICTURES PRODUCTION · SCREENPLAY BY A. VENN · MUSIC BY R. CORLEY · DIRECTED BY H. MADDOX", OSW, 500, 6.0, 40, 70, "left", ink_paint="agent_white", on=ART, trk=0.06, role="billing")
    it["variants"] = dict(n=2, vary=["age class B, C", "one cut in half by a torn edge, the title half left"])
    it["event"] = dict(date="SUNDAY 21 OCTOBER", d=21, m=10)
    return it


def tivoli_gullwing():
    it = new_item("T02", "4.2", "tivoli", "Tivoli quad: A WEEK AT GULLWING", 1016, 762, stock="white_poster", process="litho_4col", fmt="quad_crown", margin=26)
    it["art"].append(dict(id="art", box_mm=[0, 0, 1016, 762], kind="litho_picture", seed="T02", nominal_rgb=[50, 100, 168],
                          describe="a faded seaside pier under a high pale-blue sky with striped deckchairs lined up empty on the sand in the foreground, bright flat colours like a saucy postcard; no people, no faces, no lettering",
                          forbidden="people, hands, faces, children, text, numerals, signs, real brands, drink, bottles, glasses, gambling machines",
                          zone_note="the sky across the top 40 per cent stays clear and flat for the title"))
    ART = "art:50,100,168"
    T(it, "tivoli", "THE TIVOLI", JSF, 700, 20, 706, 70, "left", ink_paint="agent_white", on=ART, trk=0.3, role="name")
    T(it, "start", "FROM THURSDAY 25 OCTOBER", JSF, 600, 20, 706, 990, "right", ink_paint="agent_white", on=ART, trk=0.2)
    T(it, "title1", "A WEEK AT", FRA, 900, 90, 600, 508, "centre", ink_paint="agent_white", on=ART, trk=0.0, role="title")
    T(it, "title2", "GULLWING", FRA, 900, capfit(FRA, 900, "GULLWING", 760), 440, 508, "centre", ink_paint="agent_red", on="paint:agent_white", role="title")
    T(it, "tag", "The funniest week of their lives.", FRA, 600, 30, 70, 508, "centre", ink_paint="agent_navy", on="art:236,214,150", role="tagline")
    T(it, "billing", "A MARSHLAND PICTURES PRODUCTION · DIRECTED BY H. MADDOX", OSW, 500, 6.0, 36, 508, "centre", ink_paint="agent_navy", on="art:236,214,150", trk=0.06, role="billing")
    S(it, "title_panel", "rect", box=[110, 410, 906, 590], fill="agent_white", fill_kind="paint", note="a pale panel behind GULLWING so the red holds; the sky shows round it")
    it["variants"] = dict(n=2, vary=["age class B, C", "one with the sky bleached to near white"])
    it["event"] = dict(date="THURSDAY 25 OCTOBER", d=25, m=10)
    return it


def tivoli_programme():
    it = new_item("T03", "4.2", "tivoli", "Tivoli programme bill", 508, 762, stock="white_poster", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("THE TIVOLI", JSF, 700, fitw=440, gap=18, ink="red", trk=0.10, tech="letterpress red"),
        L("FROM SUNDAY 21 OCTOBER", OSW, 600, 32, gap=34, ink="black", trk=0.06),
        L("SUNDAY TO WEDNESDAY", OSW, 600, 30, gap=10, ink="red", trk=0.06),
        L("THE FOURTH WITNESS", OSW, 700, fitw=440, gap=30, ink="black"),
        L("THURSDAY TO SATURDAY", OSW, 600, 30, gap=10, ink="red", trk=0.06),
        L("A WEEK AT GULLWING", OSW, 700, fitw=440, gap=34, ink="black"),
    ], 254, 736, fill_bottom=330)
    S(it, "rule_a", "rule", box=[40, y + 12, 468, y + 15.4], fill="black")
    y = stack(it, "M", [
        L("PERFORMANCES 5.15 AND 8.00", OSW, 600, fitw=440, gap=14, ink="black", trk=0.05),
        L("SATURDAY ALSO 2.30", OSW, 600, fitw=330, gap=30, ink="black", trk=0.05),
        L("ALL SEATS £2.80", FRK, 800, fitw=300, gap=10, ink="red", trk=0.04),
        L("O.A.P. AND UNWAGED £1.50", FRK, 800, fitw=440, gap=8, ink="red", trk=0.04),
    ], 254, y - 10, fill_bottom=70)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=2, vary=["age class A, B", "one with the lower half torn away"])
    it["bottom_y"] = y
    return it


def typed(item, prefix, lines, x, top, pitch=4.233, f=CPR, wt=400, cap=2.455, ink="typed", tech="typed, 10 pitch", role="body", on="stock", anchor="left"):
    """Typewritten lines at a fixed pitch: Courier Prime at 12 point (cap 2.455 mm, 10 characters to the inch = 2.54 mm advance)."""
    for i, t in enumerate(lines):
        if t == "":
            continue
        T(item, "%s%d" % (prefix, i + 1), t, f, wt, cap, top - i * pitch, x, anchor, ink=ink, on=on, tech=tech, role=role)
    return top - len(lines) * pitch


def ferry_times():
    """The timetable as numbers, so the check can prove it is a service one vessel could run: the boat crosses in 15 minutes, leaves
    the Hook at :00 and :30 and the far side at :15 and :45 by day, and ends the night on the far side."""
    mon_sat_hook = ["6.30", "7.00", "7.30"]
    return dict(
        crossing_minutes=15,
        mon_sat=dict(hook_first=["6.30", "7.00", "7.30"], hook_half_hourly_until="5.30 PM", hook_then=["6.30", "7.30", "8.30", "9.30", "10.30"], hook_last="11.00",
                     far_first=["6.45", "7.15", "7.45"], far_half_hourly_until="5.45 PM", far_then=["6.45", "7.45", "8.45", "9.45"], far_last="10.45"),
        sunday=dict(hook_from="9.00 AM", hook_until="6.00 PM", far_from="9.15 AM", far_until="6.15 PM", hourly=True),
        fares=dict(single_p=60, return_pounds=1.00, cycle_p=30, oap="half fare"),
        note="Last crossing: the Hook at 11.00 PM, matching the street's own line 'Last crossing's at eleven' (game-design/tier2-batch-1.json line 2893).")


def ferry_timetable():
    it = new_item("F01", "4.2", "harbour_and_ferry", "Meridian Ferry winter timetable (A2 sheet in the ramp case)", 420, 594, stock="white_poster", process="litho_2col", fmt="A2", margin=12)
    BB = "paint:enamel_blue"
    S(it, "head_band", "rect", box=[0, 490, 420, 594], fill="enamel_blue", fill_kind="paint")
    T(it, "name", "MERIDIAN FERRY", ALF, 400, capfit(ALF, 400, "MERIDIAN FERRY", 384), 536, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.02, role="name")
    T(it, "season", "WINTER SERVICE", OSW, 700, 24, 504, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.14, role="line")
    T(it, "from", "FROM MONDAY 1 OCTOBER", OSW, 600, 17, 458, 210, "centre", ink="blue", trk=0.08, role="line")
    # two columns
    CX = (110, 310)
    S(it, "col_rule", "rule", box=[208.5, 130, 211.5, 440], fill="blue", fill_kind="ink")
    for col, (hdr, x) in enumerate((("FROM THE HOOK", CX[0]), ("FROM THE FAR SIDE", CX[1]))):
        T(it, "h%d" % col, hdr, OSW, 700, 15, 425, x, "centre", ink="black", trk=0.06, role="line")
    T(it, "ms", "MONDAY TO SATURDAY", OSW, 700, 13, 398, 210, "centre", ink="blue", trk=0.08, role="line")
    hook = ["6.30  7.00  7.30", "and every half hour", "until 5.30 PM", "then 6.30  7.30  8.30", "9.30  10.30", "LAST CROSSING 11.00"]
    far = ["6.45  7.15  7.45", "and every half hour", "until 5.45 PM", "then 6.45  7.45  8.45", "9.45", "LAST CROSSING 10.45"]
    for col, (lines, x) in enumerate(((hook, CX[0]), (far, CX[1]))):
        for i, t in enumerate(lines):
            T(it, "ms%d_%d" % (col, i), t, FRK, 700 if i in (0, 3, 4, 5) else 500, 10.5, 372 - i * 21, x, "centre", ink="black", role="times")
    T(it, "sun", "SUNDAYS", OSW, 700, 13, 236, 210, "centre", ink="blue", trk=0.08, role="line")
    for col, (lines, x) in enumerate((("9.00 AM and hourly|until 6.00 PM".split("|"), CX[0]), ("9.15 AM and hourly|until 6.15 PM".split("|"), CX[1]))):
        for i, t in enumerate(lines):
            T(it, "su%d_%d" % (col, i), t, FRK, 700 if i == 0 else 500, 10.5, 210 - i * 21, x, "centre", ink="black", role="times")
    S(it, "fare_rule", "rule", box=[12, 150, 408, 152.4], fill="blue", fill_kind="ink")
    T(it, "fares", "FARES · FOOT PASSENGERS", OSW, 700, 13, 124, 210, "centre", ink="blue", trk=0.08, role="line")
    T(it, "fares1", "SINGLE 60p · RETURN £1.00 · CYCLES 30p", FRK, 700, 11, 98, 210, "centre", ink="black", role="times")
    T(it, "fares2", "O.A.P. HALF FARE", FRK, 700, 11, 76, 210, "centre", ink="black", role="times")
    T(it, "fog", "CROSSINGS MAY BE CANCELLED IN FOG OR HIGH WIND", OSW, 600, 11, 40, 210, "centre", ink="red", trk=0.06, role="line", min_contrast=3.9)
    imprint(it, IMPRINT, y=20, cap=2.4)
    it["schedule"] = ferry_times()
    it["variants"] = dict(n=2, vary=["pasted over the summer sheet F02 (offset +14 mm right, -16 mm down) in both", "age class B and C; the C one has two drawing-pin holes and a rain stain from the top"])
    return it


def ferry_summer():
    it = new_item("F02", "4.2", "harbour_and_ferry", "Meridian Ferry summer timetable (older sheet under F01)", 420, 594, stock="white_poster", process="litho_2col", fmt="A2", margin=12)
    BB = "paint:enamel_blue"
    S(it, "head_band", "rect", box=[0, 490, 420, 594], fill="enamel_blue", fill_kind="paint")
    T(it, "name", "MERIDIAN FERRY", ALF, 400, capfit(ALF, 400, "MERIDIAN FERRY", 384), 536, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.02, role="name")
    b = T(it, "season", "SUMMER SERVICE", OSW, 700, 24, 504, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.14, role="line")
    b2 = T(it, "dates", "14 MAY TO 30 SEPTEMBER", OSW, 600, 17, 458, 210, "centre", ink="blue", trk=0.08, role="line")
    for bb in it["blocks"]:
        bb["ghost"] = True
        bb["note"] = "Mostly covered by F01 (offset +14 mm right, -16 mm down): at most the top strip of the blue band and a torn window show. Any word that shows is one of these three."
    S(it, "col_rule", "rule", box=[208.5, 130, 211.5, 440], fill="blue", fill_kind="ink")
    it["notes"].append("The older sheet carries the same table in other numbers. Nothing of it is legible: it is covered. Only the three ghost words may show, and only through a tear.")
    it["variants"] = dict(n=1, vary=["age class D: brown paste halo, loose at the left edge"])
    return it


def harbour_notice_berths():
    it = new_item("H03", "4.2", "harbour_and_ferry", "Harbour Board notice: berths closed (typed A4)", 210, 297, stock="white_bond", process="typed_carbon", fmt="A4", margin=14)
    T(it, "head", "MERIDIAN HARBOUR BOARD", LBK, 700, capfit(LBK, 700, "MERIDIAN HARBOUR BOARD", 176, 0.06), 274, 105, "centre", ink="typed", role="name", trk=0.06)
    S(it, "rule_a", "rule", box=[20, 268, 190, 269.2], fill="typed", fill_kind="ink")
    T(it, "kind", "NOTICE TO SHIPMASTERS", CPB, 700, 3.6, 255, 105, "centre", ink="typed", role="line", tech="typed twice for bold")
    lines = ["Berths 3 and 4 on the Hook quay will be closed to all", "shipping from Monday 5 November until further notice,", "for repairs to the quay wall.", "",
             "Masters should apply to the Harbour Master's office", "for other berths.", "", "By order of the Board.", "", "26 October 1990"]
    typed(it, "t", lines, 24, 238, pitch=8.466)
    it["variants"] = dict(n=2, vary=["pinned in the case: four drawing pins; a tan tape tab; one curling top corner"])
    it["event"] = dict(date="26 OCTOBER 1990", d=26, m=10)
    return it


def tide_table():
    """Seven days of invented high waters: successive highs 12 h 25 min apart (a semi-diurnal tide), heights on a spring-neap swing."""
    t0 = datetime.datetime(1990, 11, 1, 5, 42)
    rows = []
    for k in range(14):
        t = t0 + datetime.timedelta(minutes=745 * k)
        h = 4.05 + 0.65 * math.cos(2 * math.pi * k / 29.5)
        rows.append((t, round(h, 1)))
    return rows


def harbour_notice_tides():
    it = new_item("H04", "4.2", "harbour_and_ferry", "Harbour Board notice: tide table (typed A4)", 210, 297, stock="white_bond", process="typed_carbon", fmt="A4", margin=14)
    T(it, "head", "MERIDIAN HARBOUR BOARD", LBK, 700, capfit(LBK, 700, "MERIDIAN HARBOUR BOARD", 176, 0.06), 274, 105, "centre", ink="typed", role="name", trk=0.06)
    S(it, "rule_a", "rule", box=[20, 268, 190, 269.2], fill="typed", fill_kind="ink")
    T(it, "kind", "HIGH WATER, THE HOOK", CPB, 700, 3.6, 255, 105, "centre", ink="typed", role="line")
    T(it, "month", "NOVEMBER 1990", CPB, 700, 3.6, 247, 105, "centre", ink="typed", role="line")
    rows = tide_table()
    lines = ["DAY       HW     m     HW     m"]
    byday = {}
    for t, h in rows:
        byday.setdefault(t.date(), []).append((t, h))
    table = []
    for d in sorted(byday):
        hs = byday[d]
        cells = ["%02d%02d %.1f" % (t.hour, t.minute, h) for t, h in hs]
        while len(cells) < 2:
            cells.append("---- ---")
        table.append(("%s %d" % (weekday_name(d.day, d.month)[:3], d.day), cells))
    for name, cells in table:
        lines.append("%-4s    %s   %s" % (name.upper(), cells[0], cells[1]))
    lines += ["", "Heights in metres above chart datum.", "Times are Greenwich Mean Time."]
    typed(it, "t", lines, 30, 232, pitch=8.466)
    it["tide_rows"] = [dict(t=t.strftime("%Y-%m-%d %H:%M"), m=h) for t, h in rows]
    it["variants"] = dict(n=1, vary=["pinned in the case, a corner curling"])
    return it


def harbour_notice_vacancy():
    it = new_item("H05", "4.2", "harbour_and_ferry", "Harbour Board notice: vacancy (typed A4)", 210, 297, stock="pale_yellow", process="typed_carbon", fmt="A4", margin=14)
    T(it, "head", "MERIDIAN HARBOUR BOARD", LBK, 700, capfit(LBK, 700, "MERIDIAN HARBOUR BOARD", 176, 0.06), 274, 105, "centre", ink="typed", role="name", trk=0.06)
    S(it, "rule_a", "rule", box=[20, 268, 190, 269.2], fill="typed", fill_kind="ink")
    T(it, "kind", "VACANCY", CPB, 700, 9, 244, 105, "centre", ink="typed", role="line")
    T(it, "job", "QUAY LABOURER", CPB, 700, 5.4, 224, 105, "centre", ink="typed", role="line")
    lines = ["Applications in writing, giving age and experience,", "to the Secretary, Meridian Harbour Board,", "to arrive by Friday 16 November.", "", "Wages by agreement."]
    typed(it, "t", lines, 24, 202, pitch=8.466)
    it["variants"] = dict(n=1, vary=["pinned in the case"])
    return it


POLICE_ROWS = {
    "a": (12, 10, "BETWEEN 11 PM AND 1 AM,", ["A SHOP WINDOW ON QUAY STREET", "WAS SMASHED."]),
    "b": (20, 10, "BETWEEN MIDNIGHT AND 6 AM,", ["A VAN WAS STOLEN FROM THE QUAY."]),
    "c": (28, 10, "BETWEEN 10 PM AND 11 PM,", ["A MAN WAS ASSAULTED NEAR THE QUAY."]),
}
POLICE_REST = ["IF YOU SAW OR HEARD ANYTHING,", "HOWEVER SMALL, PLEASE TELEPHONE", "THE INCIDENT ROOM ON 960 640,", "OR CALL AT ANY POLICE STATION."]


def police_body_cap():
    """One body cap for all three sheets: the largest at which the widest line of any of them fits 250 mm."""
    rows = list(POLICE_REST)
    for d, m, hours, off in POLICE_ROWS.values():
        rows += ["ON THE NIGHT OF %s," % dated(d, m), hours] + off
    return min(capfit(ARC, 700, t, 250) for t in rows)


def police_notice(suffix, d, m, hours, offence_lines):
    it = new_item("C01" + suffix, "4.2", "council_police", "Police appeal for witnesses (%s)" % suffix, 297, 420, stock="white_bond", process="photocopy_a3", fmt="A3", margin=12)
    S(it, "head_band", "rect", box=[12, 340, 285, 408], fill="toner", fill_kind="ink")
    T(it, "head", "POLICE", ARC, 900, 36, 358, 148.5, "centre", ink="paper", on="ink:toner", trk=0.18, role="name")
    T(it, "appeal", "APPEAL FOR WITNESSES", ARC, 900, capfit(ARC, 900, "APPEAL FOR WITNESSES", 273), 300, 148.5, "centre", ink="toner", role="line")
    T(it, "did", "DID YOU SEE ANYTHING?", ARC, 800, capfit(ARC, 800, "DID YOU SEE ANYTHING?", 270), 262, 148.5, "centre", ink="toner", role="line")
    CAP = police_body_cap()
    PITCH = CAP * 1.9
    rows = ["ON THE NIGHT OF %s," % dated(d, m), hours] + list(offence_lines)
    y = 238
    for i, t in enumerate(rows):
        T(it, ("when" if i == 0 else "hours" if i == 1 else "off%d" % (i - 1)), t, ARC, 700, CAP, y - CAP, 24, "left", ink="toner", role="body")
        y -= PITCH
    y -= PITCH * 0.7
    for i, t in enumerate(POLICE_REST):
        T(it, "rest%d" % (i + 1), t, ARC, 700, CAP, y - CAP, 24, "left", ink="toner", role="body")
        y -= PITCH
    T(it, "conf", "YOUR INFORMATION WILL BE TREATED IN CONFIDENCE.", ARC, 600, 6.5, 30, 148.5, "centre", ink="toner", role="body")
    it["event"] = dict(date=dated(d, m), d=d, m=m)
    it["variants"] = dict(n=2, vary=["photocopy: a grey edge band 3 to 6 mm at the left, toner speckle", "taped inside a window with four tabs of yellowed tape, or in a polythene sleeve cable-tied to a lamp column"])
    it["sample_slot"] = suffix
    it["bottom_y"] = y
    return it


def police_notices():
    return [police_notice(k, *v) for k, v in POLICE_ROWS.items()]


def planning_notice():
    it = new_item("C02", "4.2", "council_police", "Planning application notice (A4 in a sleeve)", 210, 297, stock="white_bond", process="photocopy_a4", fmt="A4", margin=14)
    T(it, "head", "PLANNING APPLICATION", ARC, 900, capfit(ARC, 900, "PLANNING APPLICATION", 180), 270, 105, "centre", ink="toner", role="name")
    S(it, "rule_a", "rule", box=[16, 262, 194, 264], fill="toner", fill_kind="ink")
    T(it, "kind", "NOTICE", ARC, 700, 6.5, 250, 105, "centre", ink="toner", role="line", trk=0.3)
    body = [("PROPOSAL", 700), ("Change of use of the ground floor, 21 to 27 Quay Street,", 400), ("from shop to estate agent's office.", 400), ("", 0),
            ("COMMENTS", 700), ("Anyone wishing to comment may write to the Planning", 400), ("Officer by Friday 9 November.", 400), ("", 0),
            ("THE PLANS", 700), ("may be seen at the Planning Department, Monday to", 400), ("Friday, 9 a.m. to 4.30 p.m.", 400)]
    y = 232
    for i, (t, w) in enumerate(body):
        if t:
            T(it, "b%d" % (i + 1), t, LBK if w == 400 else ARC, w if w == 400 else 800, 3.6 if w == 400 else 3.4, y, 22, "left", ink="toner", role="body", tech="typeset, photocopied")
        y -= 8.2
    it["event"] = dict(date="FRIDAY 9 NOVEMBER", d=9, m=11)
    it["variants"] = dict(n=2, vary=["in a clear polythene sleeve, cable-tied to a lamp column or taped inside the empty unit's glass; water beads in the lower sleeve; a yellowing"])
    return it


def road_closure_notice():
    it = new_item("C03", "4.2", "council_police", "Temporary road closure notice (A3 in a sleeve)", 297, 420, stock="pale_yellow", process="photocopy_a3", fmt="A3", margin=12)
    T(it, "head", "HIGHWAYS DEPARTMENT", ARC, 800, 9, 396, 148.5, "centre", ink="toner", role="name", trk=0.18)
    T(it, "kind", "NOTICE OF TEMPORARY ROAD CLOSURE", ARC, 900, capfit(ARC, 900, "NOTICE OF TEMPORARY ROAD CLOSURE", 273), 364, 148.5, "centre", ink="toner", role="line")
    S(it, "rule_a", "rule", box=[12, 352, 285, 355], fill="toner", fill_kind="ink")
    T(it, "street", "QUAY STREET", ARC, 900, capfit(ARC, 900, "QUAY STREET", 270), 300, 148.5, "centre", ink="toner", role="title")
    rows = ["WILL BE CLOSED TO VEHICLES ON", dated(4, 11), "FROM 8 AM TO 6 PM", "FOR GAS MAIN RENEWAL."]
    sizes = [8.5, 16, 14, 8.5]
    y = 262
    for i, (t, c) in enumerate(zip(rows, sizes)):
        T(it, "r%d" % (i + 1), t, ARC, 800 if c > 10 else 700, c, y, 148.5, "centre", ink="toner", role="body")
        y -= c + 18
    T(it, "ped", "PEDESTRIAN ACCESS WILL BE MAINTAINED.", ARC, 700, 8.0, y - 4, 148.5, "centre", ink="toner", role="body")
    T(it, "div", "DIVERSION VIA WEIGHHOUSE LANE.", ARC, 700, 8.0, y - 26, 148.5, "centre", ink="toner", role="body")
    T(it, "sorry", "We apologise for any inconvenience.", LBK, 400, 6.0, 40, 148.5, "centre", ink="toner", role="body")
    it["event"] = dict(date=dated(4, 11), d=4, m=11)
    it["variants"] = dict(n=2, vary=["cable-tied in a sleeve to a lamp column at 1.6 to 2.0 m, facing the street", "the sleeve fogged inside, the notice yellowed, a cable tie tail left long"])
    return it


# --------------------------------------------------------------------------------------------
# 6. Shop-window cards and the newsagent's board (unit 4.2). Hand lettering is Patrick Hand (production/fonts).
# --------------------------------------------------------------------------------------------
HAND_FELT = dict(stroke_mm=2.6, baseline_sd_mm=1.2, rotation_sd_deg=1.0, size_sd=0.04, word_gap_sd=0.12, density_sd=0.08,
                 note="felt-tip marker: a fat even line, ends a shade darker where the nib rested, a little bleed into the card")
HAND_FELT_FINE = dict(stroke_mm=1.4, baseline_sd_mm=0.8, rotation_sd_deg=0.8, size_sd=0.04, word_gap_sd=0.10, density_sd=0.08,
                      note="fine felt tip for the small lines")
HAND_BALL = dict(stroke_mm=0.55, baseline_sd_mm=0.6, rotation_sd_deg=1.4, size_sd=0.06, word_gap_sd=0.15, density_sd=0.12,
                 note="ballpoint: a thin line, pressure shows (lighter on joins), a blot at some stroke ends")


def card_closed_lunch():
    it = new_item("K01", "4.2", "window_cards", "Closed for lunch card (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(it, "l1", "CLOSED FOR LUNCH", PAT, 400, capfit(PAT, 400, "CLOSED FOR LUNCH", 186), 92, 105, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(it, "l2", "BACK AT 2 O’CLOCK", PAT, 400, 14, 52, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    it["variants"] = dict(n=3, vary=["BACK AT 1.30 / 2 / 2.30 are not separate cards: the hour line is one of the approved strings 'BACK AT 2 O’CLOCK'", "hung on a string with a rubber sucker or taped; slightly tilted; age class A to C"])
    it["fixing"] = dict(kind="string loop 220 mm and a rubber sucker, or two strips of tape at the top corners")
    return it


def card_back_at():
    it = new_item("K02", "4.2", "window_cards", "BACK AT clock card (printed)", 130, 170, stock="buff_card", process="litho_2col", fmt=None, margin=8, kind="card")
    T(it, "l1", "BACK AT", ALF, 400, capfit(ALF, 400, "BACK AT", 108), 140, 65, "centre", ink="red", role="line")
    S(it, "clock", "roundel", box=[20, 12, 110, 102], fill="white", note="a printed clock face: white disc, black rim 2 mm, 12 tick marks, two cardboard hands on a brass paper-fastener, set to 12 o'clock", hands_deg=dict(hour=0, minute=0))
    for k, (t, x, y) in enumerate((("12", 65, 90), ("3", 100, 52), ("6", 65, 20), ("9", 30, 52))):
        T(it, "n%s" % t, t, OSW, 700, 8, y, x, "centre", ink="black", role="numeral")
    it["variants"] = dict(n=2, vary=["hands at 12 (Hal's Monday break ends at 12 in hook-cast.json) and at 2", "hung on a string"])
    it["fixing"] = dict(kind="string loop and a rubber sucker")
    return it


def card_open_closed():
    its = []
    for face, text, paint, id_ in (("OPEN", "OPEN", "agent_green", "K03a"), ("CLOSED", "CLOSED", "agent_red", "K03b")):
        it = new_item(id_, "4.2", "window_cards", "OPEN / CLOSED hanging sign, face %s" % face, 200, 110, stock="white_card", process="plastic_print", fmt=None, margin=8, kind="card")
        S(it, "face", "rect", box=[0, 0, 200, 110], fill=paint, fill_kind="paint", note="rounded corners 8 mm; a hole at the top centre; a bead chain")
        T(it, "word", text, ARC, 800, capfit(ARC, 800, text, 168), 40, 100, "centre", ink_paint="agent_white", on="paint:" + paint, trk=0.06, role="line")
        it["variants"] = dict(n=1, vary=["one face outward at a time, from the shop's hours (hook-cast.json); the chain shows"])
        its.append(it)
    return its


def card_no_dogs():
    it = new_item("K04", "4.2", "window_cards", "NO DOGS sticker, 150 x 105", 150, 105, stock="white_poster", process="sticker_print", fmt=None, margin=6, kind="sticker")
    S(it, "roundel", "roundel", box=[8, 17, 78, 87], fill="red", fill_kind="ink", note="a red ring 7 mm wide with a diagonal bar; inside it a black dog silhouette seen from the side, our own drawing")
    T(it, "l1", "NO", ARC, 900, 12, 58, 112, "centre", ink="black", role="line")
    T(it, "l2", "DOGS", ARC, 900, 12, 36, 112, "centre", ink="black", role="line")
    it["variants"] = dict(n=2, vary=["inside the glass of a shop door at 1.1 to 1.4 m, or outside on the door; one half peeled at a corner"])
    return it


def card_shut_door():
    it = new_item("K05", "4.2", "window_cards", "PLEASE SHUT THE DOOR (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(it, "l1", "PLEASE SHUT", PAT, 400, 22, 96, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    T(it, "l2", "THE DOOR", PAT, 400, 22, 56, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    it["variants"] = dict(n=2, vary=["taped to a door's glass at 1.45 m; one with a second line underlined in red felt"])
    return it


def cards_launderette():
    a = new_item("K06a", "4.2", "window_cards", "Launderette: LAST WASH (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(a, "l1", "LAST WASH", PAT, 400, 22, 92, 105, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(a, "l2", "4.30 PM", PAT, 400, 26, 50, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    a["variants"] = dict(n=2, vary=["the hour comes from the shop's closing time in hook-cast.json (laundry 8 to 5.30): LAST WASH is an hour before"])
    b = new_item("K06b", "4.2", "window_cards", "Launderette: PLEASE DO NOT OVERLOAD (printed sticker)", 210, 148, stock="white_poster", process="sticker_print", fmt="A5L", margin=8, kind="sticker")
    stack(b, "L", [L("PLEASE DO NOT", ARC, 800, 15, gap=8, ink="black", trk=0.04), L("OVERLOAD", ARC, 900, fitw=186, gap=8, ink="red"), L("THE MACHINES", ARC, 800, 15, gap=8, ink="black", trk=0.04)], 105, 134)
    b["variants"] = dict(n=2, vary=["stuck on the glass above a machine door"])
    c = new_item("K06c", "4.2", "window_cards", "OUT OF ORDER (felt pen)", 148, 105, stock="white_card", process="felt_pen", fmt="A6L", margin=6, kind="card")
    T(c, "l1", "OUT OF", PAT, 400, 14, 66, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(c, "l2", "ORDER", PAT, 400, 14, 38, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    c["variants"] = dict(n=3, vary=["taped on a machine door or the glass, a corner of tape lifting"])
    return [a, b, c]


def star_pts(cx, cy, r_out, r_in, n=14, rot=0.0):
    pts = []
    for k in range(2 * n):
        r = r_out if k % 2 == 0 else r_in
        a = rot + math.pi * k / n
        pts.append((round(cx + r * math.cos(a), 1), round(cy + r * math.sin(a), 1)))
    return pts


def cards_stars():
    specs = [("K07a", "star_yellow", [("SPECIAL OFFER", 9, "felt_black"), ("TEA BAGS", 13, "felt_black"), ("80 FOR 99p", 15, "felt_red")]),
             ("K07b", "star_pink", [("NEW SEASON", 9, "felt_black"), ("CABBAGE", 14, "felt_black"), ("20p lb", 15, "felt_black")]),
             ("K07c", "star_orange", [("BIG SAVER", 10, "felt_black"), ("TINNED PEARS", 11, "felt_black"), ("2 FOR 69p", 15, "felt_black")]),
             ("K07d", "star_yellow", [("FRESH EGGS", 13, "felt_black"), ("85p DOZEN", 15, "felt_red")])]
    out = []
    for id_, stock, lines in specs:
        it = new_item(id_, "4.2", "window_cards", "Grocer's star card", 170, 170, stock=stock, process="felt_pen", fmt=None, margin=36, kind="card")
        S(it, "star", "star", pts=star_pts(85, 85, 84, 62, 14), fill="paper", note="the card is cut to a 14-point burst; the stock colour is the star")
        n = len(lines)
        y0 = 85 + (n * 21) / 2.0 - 12
        for i, (t, cap, ink) in enumerate(lines):
            T(it, "l%d" % (i + 1), t, PAT, 400, cap, y0 - i * 21 - cap / 2.0, 85, "centre", ink=ink, tech="felt pen", hand=HAND_FELT, role="line")
        it["variants"] = dict(n=2, vary=["taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks"])
        out.append(it)
    return out


def card_no_credit():
    it = new_item("K08", "4.2", "window_cards", "SORRY NO CREDIT GIVEN (printed card)", 210, 148, stock="white_card", process="letterpress_2col", fmt="A5L", margin=8, kind="card")
    stack(it, "L", [L("SORRY", ARC, 900, 20, gap=10, ink="red"), L("NO CREDIT GIVEN", ARC, 900, fitw=186, gap=8, ink="black", trk=0.04)], 105, 128)
    it["variants"] = dict(n=2, vary=["on a shop counter's glass screen or the door"])
    return it


def cards_fish():
    items = [("K09a", "COD FILLET", "£2.70 lb"), ("K09b", "HADDOCK", "£2.50 lb"), ("K09c", "PLAICE", "£2.30 lb"), ("K09d", "KIPPERS", "95p PAIR"),
             ("K09e", "SMOKED HADDOCK", "£2.40 lb"), ("K09f", "COCKLES", "45p")]
    out = []
    for id_, a, b in items:
        it = new_item(id_, "4.2", "window_cards", "Fish price ticket: %s" % a, 105, 74, stock="white_card", process="felt_pen", fmt=None, margin=6, kind="card")
        T(it, "l1", a, PAT, 400, min(13, capfit(PAT, 400, a, 90)), 46, 52.5, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT_FINE, role="line")
        T(it, "l2", b, PAT, 400, 15, 16, 52.5, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
        it["variants"] = dict(n=2, vary=["stuck in the fish on the slab, or taped to the glass; a wet corner"])
        it["notes"].append("Price: ONS average cod fillet 1990 574 p/kg, about 2.60 a lb, January 2.42, December 2.85 (production/research/shop-window-interiors/FISHMONGER-2026-10-03.md, read in this repository); the other prices are Judgement.")
        out.append(it)
    return out


SMALL_ADS = [
    ("SA01", "index_white", (127, 76), [("ROOM TO LET", "head"), ("Clean, quiet, gas fire.", ""), ("£28 per week. No pets.", ""), ("Ring 960 417 after 5.", "")]),
    ("SA02", "index_blue", (127, 76), [("GENTS BICYCLE", "head"), ("3-speed, good tyres.", ""), ("£18 or nearest offer.", ""), ("Tel. 960 233.", "")]),
    ("SA03", "index_yellow", (148, 105), [("PIANO FOR SALE", "head"), ("Upright, good tone.", ""), ("Buyer collects. £120.", ""), ("Ring 960 528.", "")]),
    ("SA04", "index_white", (127, 76), [("WINDOW CLEANER", "head"), ("Reliable. Free estimates.", ""), ("Tel. 960 361.", "")]),
    ("SA05", "index_pink", (127, 76), [("DECORATING", "head"), ("Indoor and out.", ""), ("Fair prices. 960 774.", "")]),
    ("SA06", "index_white", (148, 105), [("LOST", "head"), ("Black and white cat,", ""), ("answers to Smudge.", ""), ("Last seen on Quay Street.", ""), ("Reward. 960 189.", "")]),
    ("SA07", "index_green", (127, 76), [("FOUND", "head"), ("Bunch of keys on", ""), ("Quay Street. Enquire within.", "")]),
    ("SA08", "index_white", (127, 76), [("TYPING DONE AT HOME", "head"), ("Letters and CVs.", ""), ("960 842.", "")]),
    ("SA09", "index_blue", (148, 105), [("MAN WITH VAN", "head"), ("Removals and house", ""), ("clearance. Anywhere.", ""), ("960 655.", "")]),
    ("SA10", "index_yellow", (127, 76), [("GAS COOKER", "head"), ("4 ring, hardly used.", ""), ("£35. Ring 960 307.", "")]),
    ("SA11", "index_white", (127, 76), [("WANTED", "head"), ("Part-time help, mornings.", ""), ("Apply within.", "")]),
    ("SA12", "index_pink", (127, 76), [("SEWING MACHINE", "head"), ("Electric. £25.", ""), ("Tel. 960 912.", "")]),
    ("SA13", "index_white", (127, 76), [("COLOUR TV", "head"), ("22 inch, working. £40.", ""), ("Ring 960 483.", "")]),
    ("SA14", "index_green", (127, 76), [("CHIMNEY SWEEP", "head"), ("Clean and tidy.", ""), ("960 596.", "")]),
]


def small_ads():
    out = []
    for n, (id_, stock, (w, h), lines) in enumerate(SMALL_ADS):
        it = new_item(id_, "4.2", "newsagent_board", "Newsagent window card %s" % id_[2:], w, h, stock=stock, process="ballpoint_card", fmt=None, margin=5, kind="card")
        y = h - 8.5
        for i, (t, kind) in enumerate(lines):
            if kind == "head":
                cap = 7.0
                ink, hand, tech = ("felt_black" if n % 3 else "felt_blue"), HAND_FELT_FINE, "felt pen"
                T(it, "l%d" % (i + 1), t, PAT, 400, cap, y - cap, 8, "left", ink=ink, tech=tech, hand=hand, role="line", on="stock")
                y -= cap + 6.5
            else:
                cap = 4.4
                ink = "ballpoint_blue" if n % 4 else "ballpoint_black"
                T(it, "l%d" % (i + 1), t, PAT, 400, cap, y - cap, 8, "left", ink=ink, tech="ballpoint", hand=HAND_BALL, role="body", on="stock")
                y -= cap + 4.6
        it["bottom_y"] = y
        it["variants"] = dict(n=1, vary=["pinned or taped on the newsagent's board: a pin or a tab of tape at the top; slight tilt"])
        out.append(it)
    tariff = new_item("SA15", "4.2", "newsagent_board", "Newsagent: ADVERTISE HERE card", 148, 105, stock="white_card", process="felt_pen", fmt="A6L", margin=6, kind="card")
    T(tariff, "l1", "ADVERTISE HERE", PAT, 400, 12, 80, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(tariff, "l2", "20p PER WEEK", PAT, 400, 14, 56, 74, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    T(tariff, "l3", "PAY AT THE COUNTER", PAT, 400, 8, 34, 74, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT_FINE, role="line")
    tariff["variants"] = dict(n=1, vary=["top of the board, taped"])
    tariff["notes"].append("20p a week is Judgement; the one search lead for it (a forum comment) is undated and not used.")
    out.append(tariff)
    return out


# --------------------------------------------------------------------------------------------
# 7. Boards and plates (units 4.2 enamel, 4.3 letting boards, 4.4 street name plates). 1 px to the mm.
# --------------------------------------------------------------------------------------------
def enamel_no_admittance():
    it = new_item("H01", "4.2", "harbour_and_ferry", "Harbour Board enamel sign: NO ADMITTANCE", 600, 450, stock=None, process="enamel", ppm=1, margin=40, fmt=None, kind="plate")
    it["stock"] = "white_poster"      # unused: plate colours are paints
    B = "paint:enamel_blue"
    S(it, "face", "rect", box=[0, 0, 600, 450], fill="enamel_blue", fill_kind="paint", note="vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge 12 mm")
    S(it, "border", "frame", box=[18, 18, 582, 432], fill="enamel_white", fill_kind="paint", width_mm=10, note="white band 10 mm, 18 mm in from the edge")
    stack(it, "L", [
        L("NO ADMITTANCE", ARC, 900, fitw=470, gap=22, paint="enamel_white", on=B, trk=0.04),
        L("EXCEPT ON BUSINESS", ARC, 700, fitw=470, gap=34, paint="enamel_white", on=B, trk=0.04),
    ], 300, 395)
    S(it, "rule", "rule", box=[70, 190, 530, 194], fill="enamel_white", fill_kind="paint")
    T(it, "board", "MERIDIAN HARBOUR BOARD", ARC, 800, capfit(ARC, 800, "MERIDIAN HARBOUR BOARD", 470, 0.04), 140, 300, "centre", ink_paint="enamel_white", on=B, trk=0.04, role="name")
    it["fixing"] = dict(kind="four holes 10 mm across at 36 mm in from each corner; bolts through the plate to a gate post or a wall plug", holes_mm=[[36, 36], [564, 36], [36, 414], [564, 414]])
    it["wear"] = dict(chips="12 to 30 chips 2 to 9 mm to black steel, at the corners, the bolt holes and the lower edge; a rust halo 3 to 8 mm round each; crazing near the holes; a bird-lime streak down from the top edge")
    it["variants"] = dict(n=2, vary=["clean to grimy (age classes B and D)", "one shot-peppered by the old catapult: six small chips in a loose group (a chip is not a bullet hole)"])
    return it


def enamel_danger_water():
    it = new_item("H02", "4.2", "harbour_and_ferry", "Harbour Board enamel sign: DANGER DEEP WATER", 600, 450, stock=None, process="enamel", ppm=1, margin=40, fmt=None, kind="plate")
    it["stock"] = "white_poster"
    B = "paint:enamel_blue"
    S(it, "face", "rect", box=[0, 0, 600, 450], fill="enamel_white", fill_kind="paint", note="vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge 12 mm")
    S(it, "danger_band", "rect", box=[0, 300, 600, 450], fill="enamel_red", fill_kind="paint")
    S(it, "border", "frame", box=[14, 14, 586, 436], fill="enamel_blue", fill_kind="paint", width_mm=10)
    T(it, "danger", "DANGER", ARC, 900, capfit(ARC, 900, "DANGER", 450, 0.1), 332, 300, "centre", ink_paint="enamel_white", on="paint:enamel_red", trk=0.1, role="title")
    T(it, "deep", "DEEP WATER", ARC, 900, capfit(ARC, 900, "DEEP WATER", 470, 0.04), 220, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.04, role="line")
    T(it, "swim", "NO SWIMMING", ARC, 800, capfit(ARC, 800, "NO SWIMMING", 420, 0.04), 130, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.04, role="line")
    T(it, "board", "MERIDIAN HARBOUR BOARD", ARC, 800, capfit(ARC, 800, "MERIDIAN HARBOUR BOARD", 400, 0.06), 56, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.06, role="name")
    it["fixing"] = dict(kind="four holes 10 mm across at 36 mm in from each corner; bolts to a quay-edge post or the railing", holes_mm=[[36, 36], [564, 36], [36, 414], [564, 414]])
    it["wear"] = dict(chips="as H01, plus salt bloom (white fur) along the lower edge and rust bleeding from the bolt holes in long tears, 150 to 400 mm")
    it["variants"] = dict(n=2, vary=["age class B, D"])
    return it


AGENT = "ARMITAGE & STOBBS"
AGENT_LINE = "CHARTERED SURVEYORS · ESTATE AGENTS"
PHONE = "960 335"


def letting_board(id_, title, w, h, named, name_cap, to_cap, sub, sub_cap, band_h, enq_cap, mount, variants):
    it = new_item(id_, "4.3", "letting_boards", title, w, h, stock=None, process="agent_board", ppm=1, margin=10, fmt=None, kind="board")
    it["stock"] = "white_poster"
    W = "paint:agent_white"
    S(it, "face", "rect", box=[0, 0, w, h], fill="agent_white", fill_kind="paint", note="18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end")
    if named:
        S(it, "band", "rect", box=[0, h - band_h, w, h], fill="agent_navy", fill_kind="paint")
        T(it, "agent", AGENT, JOS, 700, name_cap, h - 14 - name_cap, w / 2.0, "centre", ink_paint="agent_white", on="paint:agent_navy", trk=0.12, role="name")
        T(it, "agent2", AGENT_LINE, JOS, 500, round(name_cap * 0.36, 1), h - band_h + 10, w / 2.0, "centre", ink_paint="agent_white", on="paint:agent_navy", trk=0.12, role="line")
        top = h - band_h
    else:
        S(it, "hairline", "frame", box=[12, 12, w - 12, h - 12], fill="agent_navy", fill_kind="paint", width_mm=4)
        top = h - 12
    lines = [("tolet", "TO LET", 800, to_cap, "agent_red", "title")]
    if sub:
        lines.append(("sub", sub, 600, sub_cap, "agent_navy", "line"))
    lines.append(("enq", "ENQUIRIES " + PHONE, 700, enq_cap, "agent_navy", "line"))
    bottom_margin = 26
    free = (top - bottom_margin - 14) - sum(l[3] for l in lines)
    gap = max(12.0, min(48.0, free / (len(lines) + 1.0)))
    y = top - gap
    for id2, text, wt, cap, paint, role in lines:
        y -= cap
        T(it, id2, text, JOS, wt, cap, y, w / 2.0, "centre", ink_paint=paint, on=W, trk=0.04 if id2 == "tolet" else 0.06, role=role)
        y -= gap * (0.7 if id2 == "tolet" else 1.0)
    it["bottom_y"] = y
    it["mount"] = mount
    it["variants"] = variants
    return it


def letting_boards():
    mount_shop = dict(surface="the empty unit's fascia (bay 3, east, street x 21 to 27)", centre_street_x_m=24.0, z_bottom_m=2.90, z_top_m=3.35,
                      screws="four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw",
                      askew_deg="-2 to +2", proud_of_fascia_m=0.043, note="the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)")
    a = letting_board("L01", "Letting board, shop, with agent (1200 x 450)", 1200, 450, True, 52, 150, "SHOP AND PREMISES · APPROX. 520 SQ. FT.", 24, 118, 46, mount_shop,
                      dict(n=3, vary=["askew -2, 0, +2 degrees", "age class B, C, D (the D board has the white yellowed and the red faded to rust-pink)", "one with a diagonal LET strip: NOT USED (no new word)"]))
    b = letting_board("L02", "Letting board, shop, no agent (1200 x 450)", 1200, 450, False, 0, 190, None, 0, 0, 56, mount_shop,
                      dict(n=2, vary=["askew", "age class B, D"]))
    mount_flat = dict(surface="first-floor brick above the empty unit's cornice, between the two upper windows", centre_street_x_m=24.0, z_bottom_m=3.70, z_top_m=4.10,
                      screws="four 6 mm screws and plugs", askew_deg="-1.5 to +1.5", note="the cornice top is 3.55 m, the upper sill about 4.3 m (facade: head 0.4 below the ceiling, window 1.5 high): 0.75 m of plain brick; Rita's hanging sign is at street x 20.825 and the laundry's at 27.175, both outside bay 3")
    c = letting_board("L03", "Letting board, flat, with agent (600 x 400)", 600, 400, True, 30, 106, "SELF-CONTAINED FLAT", 24, 84, 34, mount_flat,
                      dict(n=2, vary=["age class C, D", "the agent's board has been up a long time: grime streaks from the top edge"]))
    mount_house = dict(surface="the west terrace (bay 2 of the plain block, street x 15 to 21): the brick pier between the two windows", centre_street_x_m=16.8, z_bottom_m=2.15, z_top_m=2.55,
                       screws="four 6 mm screws and plugs", askew_deg="-1.5 to +1.5", note="pier 16.35 to 17.25 (window 15.9 and 17.7, 0.85 wide, from the plain row's bay layout, mirrored in bay 2); the board is 0.6 wide")
    d = letting_board("L04", "Letting board, house, no agent (600 x 400)", 600, 400, False, 0, 104, "TWO BEDROOMS", 30, 0, 32, mount_house,
                      dict(n=2, vary=["age class B, D"]))
    return [a, b, c, d]


# ---- street name plates ----------------------------------------------------------------
PLATE_CAP = 90.0       # Judgement: 90 mm capitals, the South Kesteven and Charnwood specs' figure (Lead, search summary) and the project's own plate


def street_plate(id_, name, district, variant, material):
    """A plate whose length follows its name. variant: 'd' name and district line (default), 'n' name only, 'p' name, district, and a placeholder postal district."""
    bb, px = measure(MAR, 400, name, PLATE_CAP, 0.04)
    ink_w = bb[2] - bb[0]
    EDGE, BORDER, GAP = 6, 12, 22
    side_margin = EDGE + BORDER + 44
    w = int(math.ceil((ink_w + 2 * side_margin) / 10.0) * 10)
    desc = max(24, int(math.ceil(-bb[1] + 6)))   # room under the baseline for a Q's tail (it dips 0.4 of the cap) and the border
    have_dist = variant in ("d", "p")
    dist_cap = 30.0
    h = EDGE + BORDER + 20 + (dist_cap + 22 if have_dist else 0) + PLATE_CAP + desc + BORDER + EDGE
    h = int(math.ceil(h / 5.0) * 5)
    it = new_item(id_, "4.4", "street_name_plates", "Street name plate: %s (%s)" % (name, {"d": "name and district", "n": "name only", "p": "name, district and placeholder postal district"}[variant]),
                  w, h, stock=None, process=material, ppm=1, margin=EDGE, fmt=None, kind="plate")
    it["stock"] = "white_poster"
    P = "paint:plate_white"
    S(it, "face", "rect", box=[0, 0, w, h], fill="plate_white", fill_kind="paint", note="corners rounded 6 mm")
    S(it, "border", "frame", box=[EDGE, EDGE, w - EDGE, h - EDGE], fill="plate_black", fill_kind="paint", width_mm=BORDER, note="the border band 12 mm wide, 6 mm in from the edge (the South Kesteven figure, Lead)")
    base = EDGE + BORDER + desc - 2
    T(it, "name", name, MAR, 400, PLATE_CAP, base, w / 2.0, "centre", ink_paint="plate_black", on=P, trk=0.04, role="name",
      note="Marcellus SC, ruled 30 Sep for the street name plates (the earlier note's Kindersley MOT serif has no allowed free version); tracking 0.04 em")
    if have_dist:
        T(it, "district", district, MAR, 400, dist_cap, base + PLATE_CAP + 22, w / 2.0, "centre", ink_paint="plate_black", on=P, trk=0.18, role="line")
    if variant == "p":
        T(it, "postal", "MR1", MAR, 400, 22, base + PLATE_CAP + 22 + 4, EDGE + BORDER + 22, "left", ink_paint="plate_black", on=P, trk=0.1, role="line",
          note="PLACEHOLDER postal district, not minted, never on his page; MR is not a real UK postcode area")
    it["fixing"] = dict(kind="four fixings at the corners, 30 mm in", holes_mm=[[30, 30], [w - 30, 30], [30, h - 30], [w - 30, h - 30]], head="10 mm dome-head galvanised screw into fibre plugs (brick); the cast plate has the holes cast in 12 mm across")
    it["variants"] = dict(n=3, vary=["age class C, D, D", "paint flake share 0.03 to 0.06 at the letter edges", "rust runs under the screws: 0 to 4 of 4", "a sticker or its ghost (P05 or P06) in one, never over the name"])
    it["name_plate"] = dict(street=name, district=district, variant=variant, material=material, plate_w_mm=w, plate_h_mm=h, ink_w_mm=round(ink_w, 1), cap_mm=PLATE_CAP)
    return it


PLATE_STREETS = [("QUAY STREET", "THE HOOK", "cast_iron_raised"), ("WEIGHHOUSE LANE", "COPPER ROW", "pressed_aluminium_enamel"), ("TANNERY ROW", "IRONSIDE", "vitreous_enamel_steel")]


def street_plates():
    out = []
    for n, (name, dist, mat) in enumerate(PLATE_STREETS, start=1):
        for v in ("d", "n", "p"):
            out.append(street_plate("S%02d%s" % (n, v), name, dist, v, mat))
    return out


# --------------------------------------------------------------------------------------------
# 8. Processes: how each kind of sheet was printed or lettered, and what that looks like. Judgement unless marked:
#    the one-line "Lead" notes come from search summaries read today (never numbers).
# --------------------------------------------------------------------------------------------
PROCESSES = {
    "screen_2col": dict(name="two-colour screen print on fluorescent stock", passes=["black", "red"], edge_softness_mm=0.15, registration_offset_mm=[0.3, 0.8],
                        ink_mottle=dict(amount=0.06, scale_mm=[4, 10]), pinholes=dict(per_cm2=0.02, diam_mm=[0.2, 0.5]),
                        film_height_mm=0.03, show_through=0.0, tone="flat colour, no halftone; black over red where they meet",
                        lead="Hackney Museum holds a 1990 'Pay No Poll Tax' single sheet on yellow paper with red ink (search summary, unreached page): the colour way is the lead"),
    "screen_1col": dict(name="one-colour screen print on fluorescent stock", passes=["black"], edge_softness_mm=0.15, ink_mottle=dict(amount=0.06, scale_mm=[4, 10]),
                        pinholes=dict(per_cm2=0.02, diam_mm=[0.2, 0.5]), film_height_mm=0.03, tone="flat black on orange"),
    "letterpress_2col": dict(name="two-colour letterpress from metal and wood type (a small jobbing printer)", passes=["first colour", "second colour"],
                             impression_mm=[0.10, 0.18], impression_note="a darker rim 0.15 mm wide at every letter edge where the type bit the stock, and a faint raised ghost on the back",
                             ink_mottle=dict(amount=0.12, scale_mm=[3, 8]), registration_offset_mm=[0.3, 0.7], rule_joint_gap_mm=[0.2, 0.4],
                             baseline_error_mm=0.4, edge_rag_mm=0.2, height_map_mm=-0.06, tone="flat colour, slightly uneven; thick rules; many typefaces"),
    "litho_4col": dict(name="four-colour offset litho, a quad or four-sheet", halftone="about 100 lines to the inch: NOT resolved at 2 px to the mm, so drawn as continuous tone with 3 per cent grain",
                       dot_gain=0.08, registration_fringe_mm=[0.1, 0.3], stock_note="uncoated poster paper, slightly absorbent: blacks 4 per cent lifted"),
    "litho_2col": dict(name="two-colour offset litho", passes=["black", "blue"], registration_offset_mm=[0.1, 0.3], ink_mottle=dict(amount=0.04, scale_mm=[3, 8])),
    "photocopy_a4": dict(name="photocopy on A4", toner_density=0.92, speckle=dict(per_cm2=0.2, diam_mm=[0.15, 0.4]), edge_shadow=dict(width_mm=[3, 6], grey=0.55, side="left or top"),
                         streaks=dict(count=[1, 3], width_mm=[0.5, 1.2], opacity=[0.04, 0.08], height_fraction=0.6), skew_deg=[0.2, 1.5], paper_cast=0.93,
                         tone="hard black, no halftones; letters slightly fattened and rounded at the corners"),
    "photocopy_a3": dict(name="photocopy on A3", toner_density=0.92, speckle=dict(per_cm2=0.25, diam_mm=[0.15, 0.4]), edge_shadow=dict(width_mm=[3, 6], grey=0.55, side="left or top"),
                         streaks=dict(count=[1, 3], width_mm=[0.5, 1.2], opacity=[0.04, 0.08], height_fraction=0.6), skew_deg=[0.2, 1.5], paper_cast=0.93,
                         fold="a centre fold or crease across the middle in one in three"),
    "typed_carbon": dict(name="electric typewriter, then photocopied or used as the top copy", pitch="Courier 10 characters to the inch (2.54 mm), 12 point", line_pitch_mm=[4.233, 8.466],
                         ribbon_density_sd=0.15, baseline_wobble_mm=0.15, letter_dropout=0.02, tone="even, slightly fat letters, 'o' and 'e' filling in on a worn ribbon",
                         lead="by 1990 an office letter is a crisp daisy-wheel or golfball impression (period note PERIOD-PRINT-AND-FONTS, 1 Oct)"),
    "felt_pen": dict(name="felt-tip marker on card", **HAND_FELT),
    "ballpoint_card": dict(name="ballpoint on a record card, felt-tip heading", ballpoint=HAND_BALL, heading=HAND_FELT_FINE),
    "sticker_print": dict(name="printed self-adhesive label or sticker, die-cut", corner_radius_mm=3, edge_lift_mm=[8, 20], adhesive_ring_mm=0.5, scratch_lines=[0, 4], uv_fade="as the ink tau"),
    "plastic_print": dict(name="screen-printed plastic card on a chain", gloss=0.5, corner_radius_mm=8),
    "enamel": dict(name="vitreous enamel on pressed steel", roughness=0.12, metallic=0.0, chips="to black steel with a rust halo", edge="rolled 12 mm", thickness_mm=1.6,
                   lead="the Harbour Board's 'blue and white enamel signage on gates, cranes and the weighbridge' (content/brands/brand-bible-v1.json)"),
    "agent_board": dict(name="painted exterior plywood, sign-written or screen-printed vinyl", roughness=0.35, metallic=0.0, edge="cut edge painted, swells and darkens at the bottom",
                        peel_fraction=[0.01, 0.03], note="gloss gone to satin outdoors in a few years"),
    "cast_iron_raised": dict(name="cast iron, raised lettering and border, painted white with black letters", roughness=0.55, metallic=0.2, relief_mm=4.0, face_thickness_mm=8.0,
                             flake=dict(fraction=[0.03, 0.06], note="paint flakes first from the raised letter edges, showing grey iron and a thin rust film"),
                             lead="Hull's cast plates of the 1920s were black on white and the paint faded or flaked, needing regular repainting (search summary of a Geograph caption)"),
    "pressed_aluminium_enamel": dict(name="die-pressed aluminium sheet, letters and border raised 1.5 mm, stove enamelled black on white", roughness=0.3, metallic=0.6,
                                     thickness_mm=2.0, relief_mm=1.5, edge="rolled", lead="current specs: 11 SWG aluminium, die-pressed, stove-enamelled (South Kesteven, Charnwood: search summaries)"),
    "vitreous_enamel_steel": dict(name="vitreous enamel on pressed steel, rolled edge", roughness=0.12, metallic=0.0, chips="to black steel with a rust halo"),
}

# ---- the two cases --------------------------------------------------------------------------
CASE_PHOTO = dict(
    id="P1", what="four glazed notice cases on posts, a council noticeboard, blue powder-coated steel, arched-corner glazed doors, a small crest in the head, silver posts",
    where="Urban Street 01 (Poly Haven), a London street (51.528, -0.054), panorama taken 18 August 2019 by Andreas Mischok, CC0 (polyhaven.com/license read today)",
    period="NOT 1990: a replacement of the 2000s or later. Used for the PROPORTIONS of a glazed case only (header, window, foot, side bands), never for finish or colour.",
    view="rectilinear view rendered from the 8192 x 4096 tonemapped panorama: yaw 84.6, pitch 2, 18 degrees wide, 1200 x 900",
    px=dict(c2=dict(outer=[527, 312, 711, 730], window=[549, 377, 695, 704]), c3=dict(outer=[744, 334, 904, 720], window=[764, 392, 891, 686]),
            c4=dict(outer=[934, 347, 1074, 711], window=[952, 401, 1062, 676]), c1=dict(outer=[247, 292, 487, 742], window=[298, 362, 469, 701])),
    crop_origin=[470, 280], crop_scale=2.0, crop_size=[300, 500],
    method="blue-frame mask (blue > red + 45, blue > green + 25), outer box by the mask's rows and columns, window by the rows and columns where the mask is absent inside; cases 2 to 4 are in a row receding to the right, so widths are foreshortened and only VERTICAL fractions are exact",
    error_px=3)
CASE_RATIOS = dict(top_band_over_h=0.152, window_over_h=0.763, bottom_band_over_h=0.085, side_bands_sum_over_w=0.205, apparent_w_over_h_case2=0.440,
                   tolerance=dict(top_band_over_h=0.008, window_over_h=0.025, bottom_band_over_h=0.026, side_bands_sum_over_w=0.02),
                   per_case=dict(c1=dict(top=0.155, window=0.754, bottom=0.091), c2=dict(top=0.155, window=0.783, bottom=0.062), c3=dict(top=0.150, window=0.762, bottom=0.088), c4=dict(top=0.148, window=0.753, bottom=0.096)),
                   note="mean of cases 2 to 4 for the vertical fractions (top 0.155, 0.150, 0.148; window 0.783, 0.762, 0.753); side bands 0.205 to 0.213 of the apparent width; apparent aspect 0.44, 0.42, 0.39 and falling: the true aspect is not measurable from this view (about 0.5, Judgement)")


def make_cases():
    harbour = dict(
        id="HC1", title="Harbour Board notice case", kind="case", unit="4.2",
        outer_mm=[640, 880], depth_mm=60, frame_mm=dict(left=46, right=46, top=52, bottom=52), window_radius_mm=6,
        colours=dict(frame="case_timber", lining="cork", glass="4 mm clear glass, a little green at the edge, dirty on the outside"),
        construction="varnished timber frame (dark, grain showing, varnish crazed and lifting at the lower rails), mitred corners, one glazed door hinged on the left with two brass butt hinges, a brass lock and escutcheon 20 mm across on the right stile at 0.5 of the height, a cork lining 8 mm thick, a drip rail on top 14 mm proud",
        fixing="four 8 mm coach screws through the back rails at 40 mm in from the corners, on 20 mm timber battens; rust runs 40 to 180 mm below each screw",
        wear="a crack across one lower corner of the glass (30 per cent of the cases), a brown water line inside the lower glass, flies and dead leaves on the cork foot, varnish lifted at the bottom rail, one hinge screw missing",
        inside_mm=[548, 776],
        children=[dict(item="H03", x_mm=24, y_mm=470, rot_deg=0.8, pins=4), dict(item="H04", x_mm=300, y_mm=455, rot_deg=-1.2, pins=4),
                  dict(item="H05", x_mm=160, y_mm=100, rot_deg=0.5, pins=4)],
        scraps="two older yellowed sheets behind the new ones, showing 20 to 40 per cent; NO legible word (their ink is gone to brown)",
        place=dict(surface="SF1", u_m=6.95, z_bottom_m=1.20),
        photo_proportions=dict(note="the photographed case is blue steel with a 0.152 header and a 0.085 foot; the target is a 1990 timber case with 52 mm top and bottom rails (0.059 each of the height), 46 mm stiles (0.072 of the width each): the photograph's wide crest header and thick steel frame are replacement-stock features and are NOT taken (Judgement: photograph of a later object)"))
    ferry = dict(
        id="FC1", title="Ferry timetable case at the ramp", kind="case", unit="4.2",
        outer_mm=[530, 710], depth_mm=45, frame_mm=dict(left=34, right=34, top=36, bottom=36), window_radius_mm=4,
        colours=dict(frame="enamel_blue", lining="white backing board", glass="3 mm perspex, scratched and crazed in places"),
        construction="a painted steel frame in Board blue, a hinged perspex door on the left, a cylinder lock on the right at mid height, the timetable sheet F01 held behind the perspex by the frame lip; F02 underneath",
        fixing="four 8 mm screws at the corners into plugs",
        wear="perspex yellowed and scratched, a hairline crack from one corner, white salt bloom along the foot, paint chipped at the lock, rust at the lower screws",
        inside_mm=[462, 638],
        children=[dict(item="F02", x_mm=7, y_mm=38, rot_deg=0.0, pins=0, note="older sheet, 14 mm left and 16 mm higher than F01 so its edges peek out at the left and the top"),
                  dict(item="F01", x_mm=21, y_mm=22, rot_deg=0.0, pins=0)],
        place=dict(surface="SF1", u_m=6.20, z_bottom_m=1.20),
        photo_proportions=dict(note="as HC1: only vertical fractions of the photograph are exact; this frame is a thin painted steel one"))
    return [harbour, ferry]


# --------------------------------------------------------------------------------------------
# 9. Where everything goes on the street. Street x is metres along Quay Street (0 south, the quay end), the same in the
#    recipe and in the game. Surfaces carry their own 2D frame; every placement names the item, a surface and numbers.
#    Left and right are the VIEWER'S, in the game (the fascia target's rule: low street x is on the viewer's RIGHT looking
#    at the east parade, on the viewer's LEFT looking at the west block).
# --------------------------------------------------------------------------------------------
BAY_DOOR = 0.419      # side door 0.838 / 2
BAY_WIN = 0.425       # window 0.85 / 2
PLAIN_DOOR_AT = [1.5, 1.5, 4.5]      # bay 0,1 unmirrored, bay 2 mirrored (BAY_DOORS_ON left, left, right; bay 1 measured in the scene note)


def west_piers():
    """The brick piers between the openings of the plain west block (x 3 to 21), computed from the recipe's bay layout."""
    out = []
    for bay in range(3):
        s = 3.0 + 6.0 * bay
        mirrored = bay == 2
        if not mirrored:
            door = s + 1.5
            wins = [s + 3.3, s + 5.1]
        else:
            door = s + 4.5
            wins = [s + 0.9, s + 2.7]
        ops = sorted([(door - BAY_DOOR, door + BAY_DOOR, "door")] + [(w - BAY_WIN, w + BAY_WIN, "window") for w in wins])
        for k in range(len(ops) - 1):
            lo, hi = ops[k][1], ops[k + 1][0]
            if hi - lo > 0.5:
                out.append(dict(id="W%d.%d" % (bay, k), bay=bay, x0=round(lo, 3), x1=round(hi, 3), cx=round((lo + hi) / 2, 3), w=round(hi - lo, 3),
                                between=ops[k][2] + " and " + ops[k + 1][2]))
    return out


SURFACES = {
    "SF1": dict(id="SF1", name="the quay gable: east parade's south end wall", plane="x = 3.0 m, facing -x (toward the quay and the hook camera)",
                frame="u in metres from the FRONT CORNER along the wall into the block (the viewer's left edge, looking +x), z in metres up from the pavement",
                u_range=[0.0, 8.0], z_range=[0.0, 6.3], paste_zone=dict(u=[0.15, 6.0], z=[0.45, 2.75]), wall="brick_red, the parade's gable (plan_end_walls); the pavement turns the corner at it",
                reach_note="a billposter pastes to about 2.7 m from the ground; scraps of older bills higher up are allowed to 3.5 m"),
    "SF2": dict(id="SF2", name="the empty unit's whitened display glass (bay 3, east, street x 21 to 27)", plane="the street face of the glazing, set back 0.12 m",
                frame="u in metres from the glass's viewer's-LEFT edge (the high-x end, street x 26.65), z up from the pavement; glass 3.562 m wide, z 0.60 to 2.40",
                u_range=[0.0, 3.562], z_range=[0.60, 2.40], glass_street_x=[23.088, 26.65], note="the recipe's fx counts from the viewer's RIGHT: u = 3.562 x (1 - fx)"),
    "SF4": dict(id="SF4", name="the lamp columns", plane="the shaft, 0.114 m across", frame="street x of the column, z up the shaft", columns_street_x=[8.0, 28.0, 48.0],
                note="SCENE-SLOTS: every 20 m, alternate sides, first at 8 m, 0.6 m back from the kerb; a bill wraps the shaft, so the middle 0.17 m of an A3 shows face-on"),
    "SF5": dict(id="SF5", name="the empty unit's fascia", plane="fascia face, 0.12 m proud", frame="centre street x and z", fascia_z=[2.85, 3.40], bay_centre_street_x=24.0),
    "SF6": dict(id="SF6", name="first-floor brick above the empty unit's cornice", plane="brick face", frame="centre street x and z", z_range=[3.55, 4.3], window_gap_street_x=[22.93, 25.07]),
    "SF7": dict(id="SF7", name="name-plate walls", note="see the plate placements"),
    "SF8": dict(id="SF8", name="the quay-edge post", plane="a 100 mm post at the quay end, street x about -0.6", frame="z up the post", note="no quay geometry in SCENE-SLOTS: proposed, the builder places the post"),
}


def poly_overlap_area(a, b):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    w = min(ax1, bx1) - max(ax0, bx0)
    h = min(ay1, by1) - max(ay0, by0)
    return max(0.0, w) * max(0.0, h)


def _dims_m(item_id, items_by_id):
    f = items_by_id[item_id]["format"]
    return f["w_mm"] / 1000.0, f["h_mm"] / 1000.0


def _gable_try(items_by_id, seed):
    rng = np.random.RandomState(seed)
    layers = [
        [("M01", "D"), ("T03", "D"), ("G01", "C")],
        [("W01", "B"), ("J01", "B"), ("D01", "C"), ("T02", "B"), ("B01", "B")],
        [("P01", "A"), ("P03", "A"), ("P02", "B"), ("T01", "A")],
    ]
    placed = []
    for li, layer in enumerate(layers):
        u = 0.20 + 0.30 * li + float(rng.uniform(0.0, 0.15))
        for item, age in layer:
            w, h = _dims_m(item, items_by_id)
            zb = float(round(rng.uniform(0.50 + 0.22 * li, 1.00 + 0.20 * li), 2))
            if h < 2.0:
                zb = min(zb, round(2.75 - h, 2))
            placed.append(dict(item=item, surface="SF1", u_m=round(u, 2), z_bottom_m=round(zb, 2), rot_deg=round(float(rng.uniform(-1.4, 1.4)), 1), layer=li,
                               age_class=age, w_m=w, h_m=h))
            u += w + float(rng.uniform(0.02, 0.12)) + (0.25 if li == 1 else 0.0)
    return placed


def plan_gable(items_by_id, seed=20261008):
    """Three layers of bills on SF1, laid by a seeded packer and kept only if every older bill keeps enough of its face
    (layer 0 at least 30 per cent, layer 1 at least 45, the top layer all of it). The seed that passed is written into the target."""
    for k in range(400):
        placed = _gable_try(items_by_id, seed + k)
        vf = visible_fractions(placed)
        ok = all((v >= 0.30 if p["layer"] == 0 else v >= 0.45 if p["layer"] == 1 else v >= 0.97) for p, v in zip(placed, vf))
        extent = max(p["u_m"] + p["w_m"] for p in placed)
        if ok and extent <= 6.0:
            for p in placed:
                p["seed"] = seed + k
            return placed
    raise RuntimeError("no gable packing satisfied the visibility rule")


def plan_all(items_by_id):
    P = []
    P += plan_gable(items_by_id)
    # stickers on top of the gable's bills
    for item, u, zb, age in (("P05", 0.34, 1.02, "B"), ("P06", 2.55, 0.52, "C"), ("P05", 3.10, 1.45, "D")):
        w, h = _dims_m(item, items_by_id)
        P.append(dict(item=item, surface="SF1", u_m=u, z_bottom_m=zb, rot_deg=0.0, layer=3, age_class=age, w_m=w, h_m=h))
    # cases
    for case in make_cases():
        pl = case["place"]
        P.append(dict(item=case["id"], surface=pl["surface"], u_m=pl["u_m"], z_bottom_m=pl["z_bottom_m"], rot_deg=0.0, layer=0, age_class="C",
                      w_m=case["outer_mm"][0] / 1000.0, h_m=case["outer_mm"][1] / 1000.0, kind="case"))
    # the empty unit's glass
    for item, u, zb, rot, layer, age in (("M01", 0.10, 0.78, 0.8, 0, "C"), ("P03", 0.62, 0.90, 1.2, 1, "B"), ("P01", 1.20, 0.82, 0.0, 1, "B"), ("P01", 1.55, 0.78, -1.5, 2, "A"),
                                         ("P02", 2.20, 0.95, 0.6, 1, "B"), ("J01", 2.74, 1.05, -0.8, 1, "C"), ("C02", 3.10, 1.50, 0.0, 2, "A"), ("P06", 1.02, 0.66, 0.0, 3, "B")):
        w, h = _dims_m(item, items_by_id)
        P.append(dict(item=item, surface="SF2", u_m=u, z_bottom_m=zb, rot_deg=rot, layer=layer, age_class=age, w_m=w, h_m=h))
    # the plain west block's piers
    piers = {p["id"]: p for p in west_piers()}
    for pid, item, zb, age in (("W0.0", "C01a", 1.30, "B"), ("W0.1", "M01", 0.85, "C"), ("W1.0", "W01", 1.00, "B"), ("W1.1", "P02", 0.95, "B"), ("W2.0", "J01", 1.00, "C"),
                               ("W2.1", "D01", 0.90, "C")):
        pr = piers[pid]
        w, h = _dims_m(item, items_by_id)
        P.append(dict(item=item, surface="WEST_PIER", pier=pid, street_x_m=pr["cx"], z_bottom_m=zb, rot_deg=0.0, layer=1, age_class=age, w_m=w, h_m=h, pier_w_m=pr["w"]))
    for pid, item, zb in (("W2.0", "L04", 2.15),):
        pr = piers[pid]
        w, h = _dims_m(item, items_by_id)
        P.append(dict(item=item, surface="WEST_PIER", pier=pid, street_x_m=pr["cx"], z_bottom_m=zb, rot_deg=0.0, layer=2, age_class="C", w_m=w, h_m=h, pier_w_m=pr["w"]))
    # the lamp columns
    for item, x, zb, age in (("C03", 8.0, 1.55, "A"), ("P05", 8.0, 1.25, "C"), ("P06", 28.0, 1.45, "B"), ("P05", 28.0, 1.85, "D")):
        w, h = _dims_m(item, items_by_id)
        P.append(dict(item=item, surface="SF4", street_x_m=x, z_bottom_m=zb, rot_deg=0.0, layer=1, age_class=age, w_m=w, h_m=h))
    # the letting boards
    w, h = _dims_m("L01", items_by_id)
    P.append(dict(item="L01", surface="SF5", street_x_m=24.0, z_bottom_m=2.90, rot_deg=-1.5, layer=0, age_class="C", w_m=w, h_m=h, note="L02 is the alternative (no agent)"))
    w, h = _dims_m("L03", items_by_id)
    P.append(dict(item="L03", surface="SF6", street_x_m=24.0, z_bottom_m=3.70, rot_deg=1.0, layer=0, age_class="C", w_m=w, h_m=h))
    # the name plates
    for pid, surface, x, zc, note in (("S01d", "SF7", 20.47, 2.63, "west corner pier (x 19.92 to 21.0, brick to 3.12 m): the existing plate's place, kept; 80 mm of pier either side"),
                                       ("S01d", "SF7", None, 2.63, "second QUAY STREET plate on the quay gable, centre 1.0 m from the front corner; z centre 2.63"),
                                       ("S02d", "SF7", None, 2.63, "WEIGHHOUSE LANE plate on the near flank of the first shop beyond the side opening (x = 24.0 plane, facing -x), centre 0.9 m from its front corner; PROPOSED: the opening's name is not decided in canon")):
        w, h = _dims_m(pid, items_by_id)
        P.append(dict(item=pid, surface=surface, street_x_m=x, z_bottom_m=round(zc - h / 2, 3), rot_deg=0.0, layer=0, age_class="D", w_m=w, h_m=h, note=note))
    # harbour enamel
    w, h = _dims_m("H02", items_by_id)
    P.append(dict(item="H02", surface="SF8", street_x_m=-0.6, z_bottom_m=1.20, rot_deg=0.0, layer=0, age_class="C", w_m=w, h_m=h, note="PROPOSED: on a post at the quay edge; no quay geometry in SCENE-SLOTS"))
    return P


# --------------------------------------------------------------------------------------------
# 10. Assemble.
# --------------------------------------------------------------------------------------------
def all_items():
    ITEMS.clear()
    bill_poll_meeting(); bill_dont_pay(); bill_march(); bill_summons_a4(); sticker_polltax(); sticker_cantpay()
    bill_jumble(); bill_dance(); bill_wrestling(); bill_boxing(); bill_market(); goods_whitewell(); goods_tea()
    tivoli_witness(); tivoli_gullwing(); tivoli_programme()
    ferry_timetable(); ferry_summer(); enamel_no_admittance(); enamel_danger_water()
    harbour_notice_berths(); harbour_notice_tides(); harbour_notice_vacancy()
    police_notices(); planning_notice(); road_closure_notice()
    card_closed_lunch(); card_back_at(); card_open_closed(); card_no_dogs(); card_shut_door(); cards_launderette(); cards_stars(); card_no_credit(); cards_fish(); small_ads()
    letting_boards(); street_plates()
    return list(ITEMS)


FORBIDDEN_WORDS = dict(
    alcohol_gambling_children=["beer", "lager", "ale", "stout", "pint", "whisky", "whiskey", "vodka", "gin", "rum", "wine", "cider", "champagne", "cocktail", "liquor", "spirits",
                               "booze", "pub", "bar", "licensed", "brewery", "bingo", "raffle", "tombola", "lottery", "pools", "bet", "betting", "bookie", "bookmaker", "odds",
                               "stake", "casino", "gamble", "gambling", "jackpot", "dice", "poker", "whist", "draw", "prize", "child", "children", "kid", "kids", "baby", "toddler",
                               "pram", "school", "pupil", "playground", "nursery", "teenage", "junior", "infant", "family", "toy", "toys", "santa", "grotto", "youth", "boys", "girls"],
    real_marks=["ROYAL MAIL", "POST OFFICE", "BRITISH RAIL", "BRITISH TELECOM", "BRITISH GAS", "NATIONAL LOTTERY", "CRIMESTOPPERS", "NEIGHBOURHOOD WATCH", "LETRASET", "DYMO",
                "BBC", "ITV", "THATCHER", "KINNOCK", "LABOUR", "CONSERVATIVE", "TORY", "TORIES", "SDP", "LIBERAL", "FEDERATION"],
    names_not_minted=["MERIDIAN TOWN", "AFC", "ARGUS", "TIDELINE", "COASTWAY", "COUNCIL", "BOROUGH", "CITY OF", "CONSTABULARY", "METROPOLITAN"],
    after_1992=["MOBILE", "INTERNET", "EMAIL", "E-MAIL", "WWW", "WEBSITE", "EURO", "DVD", "TEXT"],
    note="word-boundary, case-insensitive. ARMITAGE & STOBBS, QUAY PRINT, MERIDIAN AGAINST THE POLL TAX and the others in 'proposed_names' are PLACEHOLDERS allowed on the sheets and NEVER on his page. "
         "self_check.py also runs tools/content-gate.py's rule table and RealWorld.cs's AnyCase names and imagegen's forbidden tokens over every string.")


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")


def build():
    items = all_items()
    by_id = {it["id"]: it for it in items}
    # hand-lettered cards cannot be told from a mirror image by their words: each carries one asymmetric cue the renderer must draw
    cues = [("a tab of yellowed tape across the top-LEFT corner only", "top-left"), ("a drawing-pin hole at the top-RIGHT only and a torn lower-LEFT corner", "top-right"),
            ("a string loop and rubber sucker at the top-LEFT, a crease running from the top-right corner", "top-left"),
            ("two tape tabs, a long one at the top-LEFT and a short one at the top-RIGHT, the left one lifting", "top-left")]
    n = 0
    for it in items:
        if it["blocks"] and all(b.get("hand") for b in it["blocks"]):
            what, side = cues[n % len(cues)]
            it["mirror_cue"] = dict(what=what, side=side, rule="drawn at the stated side of the card as the viewer sees it in the game; the check G.mirror.cues reads the corner's brightness against the opposite corner")
            n += 1
    # check fit
    problems = []
    for it in items:
        problems += check_fit(it)
    assert not problems, problems
    cases = make_cases()
    placements = plan_all(by_id)
    return items, by_id, cases, placements


def visible_fractions(pls, res=0.01):
    """For each placement on one surface, the share of its face (rectangle, rotation ignored) not covered by a later placement
    (higher layer, or the same layer later in the list)."""
    out = []
    for i, p in enumerate(pls):
        x0, y0 = p["u_m"], p["z_bottom_m"]
        x1, y1 = x0 + p["w_m"], y0 + p["h_m"]
        nx, ny = max(1, int(round((x1 - x0) / res))), max(1, int(round((y1 - y0) / res)))
        xs = x0 + (np.arange(nx) + 0.5) * res
        ys = y0 + (np.arange(ny) + 0.5) * res
        cov = np.zeros((ny, nx), bool)
        for j, q in enumerate(pls):
            if j == i:
                continue
            above = (q["layer"] > p["layer"]) or (q["layer"] == p["layer"] and j > i)
            if not above:
                continue
            qx0, qy0 = q["u_m"], q["z_bottom_m"]
            qx1, qy1 = qx0 + q["w_m"], qy0 + q["h_m"]
            mx = (xs >= qx0) & (xs <= qx1)
            my = (ys >= qy0) & (ys <= qy1)
            cov |= my[:, None] & mx[None, :]
        out.append(round(1.0 - cov.mean(), 3))
    return out


# --------------------------------------------------------------------------------------------
# 11. The checks (what the 2D builder's automatic check must pass on a rendered item).
# --------------------------------------------------------------------------------------------
def chk(id_, name, scope, measure_, expected, tol, unit, method, reads="pixels", why=""):
    return dict(id=id_, name=name, scope=scope, measure=measure_, expected=expected, tolerance=tol, unit=unit, method=method, reads=reads, why=why)


def is_hand(b):
    return bool(b.get("hand"))


def block_tols(b, ppm):
    hand = is_hand(b)
    if b["role"] == "imprint":
        return dict(pos_mm=2.5, base_mm=1.5, cap_frac=0.25, F=0.55)
    if b["technique"] and "typed" in str(b["technique"]):
        return dict(pos_mm=1.5, base_mm=1.2, cap_frac=0.10, F=0.85)
    if hand:
        return dict(pos_mm=7.0, base_mm=3.5, cap_frac=0.14, F=0.78)
    if b["cap_mm"] < 8:
        return dict(pos_mm=2.0, base_mm=1.2, cap_frac=0.10, F=0.85)
    return dict(pos_mm=max(2.5, 0.006 * b["width_mm"]), base_mm=2.0, cap_frac=0.06, F=0.90)


def make_checks(items, by_id, cases, placements):
    C = []
    for it in items:
        iid = it["id"]
        ppm = it["px_per_mm"]
        w, h = it["format"]["w_mm"], it["format"]["h_mm"]
        C.append(chk(iid + ".size", "image size", iid, "width and height of the base-colour image", [int(round(w * ppm)), int(round(h * ppm))], 0, "px at %d px/mm" % ppm, "image size",
                     why="1 pixel is 1/%d mm so a letter's height in pixels is its height in millimetres times %d" % (ppm, ppm)))
        words = sorted({norm(b["text"]) for b in it["blocks"]})
        C.append(chk(iid + ".words", "words exactly as approved", iid, "the strings the renderer drew for this item (its manifest), apostrophes and dashes normalised",
                     words, 0, "strings", "set equality with the manifest; then, if an OCR pass is run, every token it reads is in approved_word_parts", reads="manifest",
                     why="the words are ours; the image model never draws one"))
        if not it["blocks"]:
            continue
        pos = []
        caps = []
        masks = []
        cons = []
        for b in it["blocks"]:
            t = block_tols(b, ppm)
            pos.append(dict(block=b["id"], ink_box_mm=b["ink_box_mm"], anchor=b["anchor"], tol_mm=round(t["pos_mm"], 1), baseline_tol_mm=t["base_mm"]))
            caps.append(dict(block=b["id"], cap_mm=b["cap_mm"], tol_frac=t["cap_frac"], cap_px=round(b["cap_mm"] * ppm, 1)))
            masks.append(dict(block=b["id"], min_F=t["F"], font=b["font"], weight=b["weight"], tracking_em=b["tracking_em"], size_px_per_em=round(b["size_px_per_em"] * ppm, 2)))
            nominal = b["contrast"]["B"]
            floor = 3.0 if b["cap_mm"] >= 12 else 4.5
            mn = max(2.2, min(floor, 0.9 * nominal))
            if b["role"] == "imprint":
                mn = 1.8
            cons.append(dict(block=b["id"], nominal_B=nominal, nominal_C=b["contrast"]["C"], min_B=round(mn, 2), cap_mm=b["cap_mm"]))
        C.append(chk(iid + ".pos", "block positions", iid, "ink box of each block's glyph mask read off the pixels, widened 8 mm along the line", pos, "per block", "mm",
                     "centre (anchor centre) or left/right edge within tol_mm; baseline within baseline_tol_mm (the median bottom of flat-bottomed letters)"))
        C.append(chk(iid + ".cap", "letter heights at scale", iid, "cap height of each block read off its flat-bottomed capitals", caps, "per block", "fraction of the cap",
                     "height of the tallest flat-topped, flat-bottomed capital in the block's mask / cap_mm; also cap_px = cap_mm x px_per_mm"))
        C.append(chk(iid + ".mask", "glyph mask against the font", iid, "the block re-rendered from its font file (font, weight, size, tracking, anchor) compared with the ink-coloured pixels",
                     masks, "per block", "F score, mean of recall and precision, each against the other mask dilated 2.5 mm (hand), 1 mm (print)",
                     "pass at min_F, and the same re-render FLIPPED about the item's vertical centre line must score lower by 0.15"))
        C.append(chk(iid + ".contrast", "contrast", iid, "WCAG ratio of the block's mean ink colour to the mean ground colour in its box, on the aged render (class B)", cons, "per block", "ratio",
                     "ink = pixels nearer the ink colour than the ground; ground = the rest of the box; min_B per block"))
    # global checks
    C.append(chk("G.words.approved", "no word outside the approved list", "all items", "every token of every manifest string", "tokens subset of approved_word_parts", 0, "tokens",
                 "split on spaces; apostrophes, dashes and the middle dot normalised; digits and times match the number patterns", reads="manifest"))
    C.append(chk("G.forbidden", "no forbidden word", "all items", "forbidden_patterns (alcohol, gambling, children, real marks, names not minted, after 1992) and tools/content-gate.py's rule table over every manifest string",
                 0, 0, "hits", "word-boundary, case-insensitive", reads="manifest"))
    C.append(chk("G.dates", "every dated bill's weekday is right for the year", "bills with an event", "weekday of the printed date in 1990", "equal", 0, "days", "datetime.date", reads="manifest"))
    C.append(chk("G.mirror", "no sheet is mirrored", "all items", "for each asymmetric block, the glyph mask scores higher at its own position than at the position mirrored about the item's centre line", "true", 0.0, "bool",
                 "the fascia family's first try drew its board the wrong way round; the same fault on a bill or a plate would put MICKEY'S backwards"))
    cue_items = [it["id"] for it in items if it.get("mirror_cue")]
    C.append(chk("G.mirror.cues", "a hand-lettered card carries its asymmetric cue on the stated side", "cards: %s" % ", ".join(cue_items), "the corner patch at the cue's side differs from the opposite corner (tape, pin hole, tear, crease)",
                 {it["id"]: it["mirror_cue"]["side"] for it in items if it.get("mirror_cue")}, 0.0, "bool", "mean luminance and edge density of the 40 mm corner patches", reads="pixels",
                 why="the words of a centred hand-lettered card read the same mirrored; this cue is the only thing that can tell"))
    C.append(chk("G.fonts", "fonts are the OFL list", "all items", "the font name of every block", sorted(FONTS), 0, "names", "block.font in this list; Overpass, Apache and GPL faces refused", reads="manifest"))
    C.append(chk("G.proposed", "proposed names stay where listed", "all items", "ARMITAGE & STOBBS, QUAY PRINT, MERIDIAN AGAINST THE POLL TAX etc. appear only on the items that list them", "listed", 0, "strings", "manifest", reads="manifest",
                 why="placeholders, never on his page (RULINGS 3 Oct)"))
    C.append(chk("G.ferry.schedule", "the ferry timetable is a service one boat can run", "F01", "crossing 15 minutes; Hook departures at :00/:30 by day, far side at :15/:45; last crossing 11.00 PM from the Hook", "consistent", 0, "minutes", "parse the schedule", reads="manifest"))
    C.append(chk("G.tides", "the tide table advances 12 h 25 min a high water", "H04", "difference between successive HW times", 745, 5, "minutes", "parse the rows", reads="manifest"))
    # placements
    C.append(chk("G.place.inside", "each placement lies inside its surface's paste zone", "placements", "rectangle inside the zone", "inside", 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.place.layers", "same-layer bills do not overlap; every older bill keeps its share of face", "SF1, SF2", "visible fraction by raster", dict(layer0=0.30, layer1=0.45, top=0.97), 0.0, "fraction", "visible_fractions()", reads="geometry"))
    C.append(chk("G.place.piers", "a bill on a west pier fits the brick with 40 mm each side, and clears the openings", "WEST_PIER", "bill width <= pier width - 0.08", "true", 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.place.height", "nothing pasted above 2.75 m except scraps", "SF1", "top edge of every full bill", 2.75, 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.letting.mount", "letting board sits on the fascia with 50 mm clear above and below", "L01, L02", "z range 2.90 to 3.35 inside 2.85 to 3.40", [2.90, 3.35], 0.01, "m", "geometry", reads="geometry"))
    C.append(chk("G.plates.length", "plate length follows the name", "S**", "ink width + 2 x 62 mm margins, rounded up to 10 mm", "see name_plate", 10, "mm", "geometry", reads="geometry"))
    C.append(chk("G.plates.cap", "plate capitals are 90 mm", "S**", "cap height of the name block", PLATE_CAP, 3.0, "mm", "pixels at 1 px/mm"))
    C.append(chk("G.plates.border", "border band 12 mm, 6 mm in from the edge", "S**", "dark band width on a scan line through the plate's middle", 12, 1.0, "mm", "pixels at 1 px/mm"))
    return C


# --------------------------------------------------------------------------------------------
# 12. Sources, disagreements, what could not be settled.
# --------------------------------------------------------------------------------------------
SOURCES = [
    dict(id="P1", kind="photograph", url="https://polyhaven.com/a/urban_street_01 ; file https://dl.polyhaven.org/file/ph-assets/HDRIs/extra/Tonemapped%20JPG/urban_street_01.jpg ; info https://api.polyhaven.com/info/urban_street_01",
         read="8 October 2026 (tonemapped panorama 8192 x 4096, 10.6 MB)", author="Andreas Mischok", licence="CC0 (polyhaven.com/license read 8 Oct: 'all licensed as CC0')", taken="18 August 2019 (info: date_taken 1566112140)",
         shows="a London street (E2); four glazed notice cases on posts, blue steel, in a dwarf brick wall; the interiors are masked in the preview", used="YES: proportions of a glazed case only (a 2000s replacement, not 1990)"),
    dict(id="P2", kind="photograph", url="https://polyhaven.com/a/bethnal_green_entrance", read="8 October 2026 (tonemapped 8192 x 4096)", author="Andreas Mischok", licence="CC0", taken="18 August 2019",
         shows="a park gate and a lamp column carrying a modern blue pole plate that is stickered over, a small white plate reading RSE 3, and a council byelaw sign about alcohol", used="NO: nothing measured; the byelaw sign names alcohol, so NO crop of it is kept anywhere"),
    dict(id="P3", kind="photographs", url="https://polyhaven.com/hdris (urban_street_02, 03, 04, adams_place_bridge, birbeck_street_underpass, cambridge, docklands_02, limehouse; canary_wharf, docklands_01 and leadenhall_market were NOT looked at here)",
         read="8 October 2026 (2048 x 1024 tonemapped previews in /home/user/cache/ph/scout)", author="Andreas Mischok and others (each page)", licence="CC0", taken="2019 to 2025",
         shows="no street name plate, letting board or poster hoarding that could be measured", used="NO"),
    dict(id="F1", kind="licence texts", url="https://raw.githubusercontent.com/google/fonts/main/ofl/<family>/OFL.txt and https://raw.githubusercontent.com/liberationfonts/liberation-fonts/main/LICENSE",
         read="8 October 2026, whole", author="each family's authors (copyright lines in fonts[].copyright)", licence="SIL OFL 1.1 (Liberation: OFL 1.1 with Reserved Font Name Liberation)", taken="n/a",
         shows="Jost, Libre Franklin, Oswald, Alfa Slab One, Fraunces, Libre Baskerville, Old Standard TT, Abril Fatface, Josefin Sans, Archivo, Courier Prime, Marcellus SC, Patrick Hand, Arimo; UnifrakturMaguntia read, not used",
         used="YES: fonts (Liberation's font files were NOT reached: github.com file downloads return 403; its LICENSE was read; it is not used here)"),
    dict(id="R1", kind="repository", url="canon.md; RULINGS.md; production/cloud-week/targets/BRIEF.md and SCENE-SLOTS.md", read="8 October 2026", author="the project", licence="project", taken="n/a", shows="the world, the content rule, the rulings, the street's slots", used="YES"),
    dict(id="R2", kind="repository", url="production/specs/hook-cast.json; production/specs/vignette-scene.json; tools/art-recipes/terrace-front.py; tools/props/make_vignette_2d.py; production/assets/vignette/decals2d/",
         read="8 October 2026", author="the project", licence="project", taken="n/a", shows="shop hours, the market's days, the chapel hall, the street's blocks, the plain row's bay layout, today's bills, plate and letting board (900 x 260, 900 x 450)", used="YES"),
    dict(id="R3", kind="repository", url="production/cloud-week/targets/fascia-signs/TARGET.md and target.json", read="8 October 2026", author="the fascia target writer", licence="project", taken="n/a",
         shows="the ten shops' street x, door ends, hanging signs, the letting board's centre, the glass lettering rows, the hours plates", used="YES: positions and the left-right rule"),
    dict(id="R4", kind="repository", url="production/research/asset-plan/4-SIGNAGE-AND-WEAR.md; production/research/ui-design/PERIOD-PRINT-AND-FONTS.md; production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/art/atlas-02/research/transport-timetables.md; production/research/shop-window-interiors/FISHMONGER-2026-10-03.md; content/brands/brand-bible-v1.json",
         read="8 October 2026", author="earlier research helpers (they read period photographs and search summaries on the PC)", licence="project", taken="n/a",
         shows="Letraset and photocopy for 1990 bills, the 1952 Kindersley recommendation, the winter timetable date of 1 October 1990, cod at about 2.60 a lb in 1990, the Harbour Board's blue and white enamel and glass case, the ferry's pasted winter over summer sheets", used="YES, cited, not re-measured"),
    dict(id="L1", kind="search summaries (leads, never numbers)", url="WebSearch 8 Oct 2026: street name plate specs (South Kesteven https://www.southkesteven.gov.uk/sites/default/files/2023-09/STREET_NAME_PLATE_SPECIFICATIONv2.pdf; Charnwood; Fareham; Cotswold; Wigan), DfT circular 3/93 (west-norfolk.gov.uk copy), London street signs (spitalfieldslife.com/2020/09/14/london-street-signs/), UK poster sizes (artofthemovies.co.uk, vintageposterblog.com), letting board rules (estatesgazette.co.uk, basingstoke.gov.uk), anti-poll-tax material (museum-collection.hackney.gov.uk object-1991-115)",
         read="8 October 2026: the pages themselves were NOT fetched (DNS or 403); only the search summaries were read", author="various", licence="n/a", taken="n/a",
         shows="90 mm capitals, 150 mm plates and 12 mm borders as modern specs; black on white default; no national design, each council its own; no source for 1980s postal districts on provincial plates; Hull 1920s cast plates black on white, flaking; Double Crown 20 x 30 in; 1984 regulations allowed one letting board per property, 2 sq m a board before the 1990s cut; a 1990 Hackney 'Pay No Poll Tax' sheet on yellow paper in red ink",
         used="LEADS ONLY"),
]
UNREACHED = ["en.wikipedia.org (DNS and 403)", "commons.wikimedia.org, geograph.org.uk, flickr.com, archive.org (403)", "thebeautyoftransport.com (403)", "legislation.gov.uk, gov.uk (403)",
             "historicengland.org.uk, nationalarchives.gov.uk (403)", "www.west-norfolk.gov.uk and www.wigan.gov.uk PDFs (DNS)", "github.com file downloads for Liberation's TTFs (403)"]
WOULD_READ = [
    "Geograph and Commons photographs of street name plates dated 1985 to 1995 in a northern English port or mill town: plate depth, letter height, border, fixings, whether a postal district or the council's name is on it (the biggest gap: nothing about plates is measured in this target)",
    "Photographs of estate agents' and commercial letting boards of 1988 to 1992 (Peter Marshall's Hull set; Picture Sheffield): size, layout, colours, how it is fixed to a fascia",
    "Photographs of fly-posted hoardings and gable walls, 1988 to 1992 (Hackney Museum and Picture Sheffield): the share of the wall covered, layer count, bill sizes in use, how torn and faded",
    "A 1990 provincial cinema bill and quad, and a 1990 wrestling or boxing bill (Sheffield's National Fairground and Circus Archive; V&A): type, colours, billing block",
    "1990 council notices: planning notices, road closure orders, police appeal sheets (local archives, Hackney Archives 2020/26): layout, paper, how fixed to a column",
    "The Hackney 'Pay No Poll Tax' sheet and the Wandsworth screenprint (V&A O203232/3): colours, type, the imprint line",
    "The DfT circular 3/93 itself and Alistair Hall's London Street Signs (2020): plate sizes and postal districts",
    "Liberation Sans/Serif TTFs, if the builder wants them over Archivo and Libre Baskerville",
]
DISAGREEMENTS = [
    dict(topic="street plate lettering", wins="the 30 September ruling (Marcellus SC)", others="the street-clutter note (Kindersley MOT serif, recommended 1952) and a search summary of a Hull caption (1920s to 1930s cast plates used the MOT SANS alphabets; Kindersley from 1951)",
         choice="Marcellus SC capitals, 90 mm, tracking +0.04 em. No photograph reached: the ruling stands until one disagrees."),
    dict(topic="postal district on a plate", wins="judgement", others="the street-clutter note lists 'postcodes' as wrong for 1990; a search summary found NO source of 1980s provincial plates carrying a postal district; London plates did carry the district",
         choice="the default plate carries the DISTRICT NAME as a small line (THE HOOK, COPPER ROW, IRONSIDE: canon's minted districts) and no postcode; the postcode-style variant (MR1) exists as a placeholder, never default; the council's name and crest are omitted (canon owes the council's name)"),
    dict(topic="the 4 October bills", wins="this target", others="tools/props/make_vignette_2d.py: clean flat bills, League Gothic, all four on one generic layout, a spring date (SATURDAY 31 MARCH), 'Admission 10p', 'WEIGHHOUSE LANE HALL', the bills' own fine print readable and straight",
         choice="autumn 1990 dates with computed weekdays, the chapel hall named as hook-cast.json names it, imprints, ageing in four classes, layered pasting, different processes and layouts"),
    dict(topic="the letting board", wins="this target", others="board_to_let.png: 900 x 450, PT Sans, no agent, no number, a white box with a red border",
         choice="1200 x 450 with an agent band, TO LET, size, a number; the no-agent variant keeps a number; 900 x 450 would need cap 110 and drop the agent band"),
    dict(topic="the poster prop's place", wins="the plain row's bay layout (terrace-front.py _plain_ground)", others="vignette-scene.json's held-prop notes put a poster at west x 11.4 and a case at west x 26.4 'between a side door at 25.5 and a window at 27.3' (written before the west_north block became shops)",
         choice="x 11.4 is the pier W1.0 (10.919 to 11.875) and stays; the case at 26.4 would stand on the tea room's glass: both cases move to the quay gable"),
    dict(topic="the one photograph measured", wins="judgement", others="the photographed notice case is a modern blue steel replacement with a wide crest header",
         choice="only its vertical fractions inform the glazed case's proportions; the 1990 case is a timber one with thinner rails (HC1)"),
]
COULD_NOT_SETTLE = [
    "No photograph of a 1990 street name plate, letting board, fly-posted wall or paper notice was reached. Every size of those is Judgement on search-summary leads (90 mm capitals, 150 to 230 mm plates, 12 mm borders: modern specs).",
    "Whether provincial plates of 1990 carried a postal district, the council's name or a crest: not found. The target omits the council and uses a district-name line.",
    "The name of the side opening at street x 21 to 24 on the west: not in canon. The WEIGHHOUSE LANE plate there is proposed; the town may name it otherwise.",
    "Whether the scene has a quay-edge post, a hoarding, a gable wall at x = 3 that faces the hook camera with the geometry assumed here (8 m deep, eaves 6.3 m): read from vignette-scene.json and the recipe, not from the mesh.",
    "Tobacco bills (cigarettes were advertised on hoardings in 1990): omitted: they need a minted brand and the exact government health-warning wording, which was not read.",
    "The BBFC certificate roundels on film bills are real marks and are not drawn; the 1990 bills carried them.",
    "A police appeal board (the yellow A-board) in 1990: the only dated photograph found is from 2007; this target uses an A3 photocopy taped in a window or sleeved on a column instead.",
    "The local paper's contents bill, the football club's bills and the radio station's stickers: the names are owed (canon), so none is drawn; the brand bible's proposals (Meridian Town AFC, the Argus, Radio Tideline, Coastway) are NOT used.",
    "Real-name coincidence: the invented film titles, ring names, credits, brands and the agent's name were not checked against real lists (the network refused the sources); each is listed in proposed_names for the town to mint or strike.",
    "Prices (cinema 2.80, wrestling 4 and 2.50, ferry 60p, tea 1.35) are Judgement except cod (ONS via the earlier note).",
    "Texture size and mip: not checked in the 5.8.2 source; the builder checks whether bills need padding to powers of two (the fascia target has the same open question).",
]


def ofl_info(d):
    p = Path(FONT_DIR) / ("OFL-%s.txt" % d)
    if not p.exists():
        return dict(read=False)
    t = p.read_text(errors="replace")
    import hashlib
    m = re.search(r"^Copyright[^\n]*", t, re.M)
    rfn = re.findall(r'Reserved Font Names?\s+"?([^".\n]+)"?', t)
    return dict(read=True, sha256=hashlib.sha256(t.encode()).hexdigest()[:16], copyright=(m.group(0)[:160] if m else None), reserved_font_names=sorted(set(r.strip() for r in rfn)), bytes=len(t))


def _default(o):
    return o.item() if hasattr(o, "item") else str(o)


def write_json(target, path=None):
    """Top-level keys one per line; big lists with one element per line, each element compact (the git size guard's limit is 1 MB a file)."""
    path = path or (HERE / "target.json")
    parts = []
    for k, v in target.items():
        if isinstance(v, list) and len(v) > 3:
            body = "[\n" + ",\n".join(json.dumps(e, ensure_ascii=False, separators=(",", ":"), default=_default) for e in v) + "\n]"
        elif isinstance(v, dict) and len(json.dumps(v, default=_default)) > 3000:
            body = "{\n" + ",\n".join(json.dumps(kk, ensure_ascii=False) + ": " + json.dumps(vv, ensure_ascii=False, separators=(",", ":"), default=_default) for kk, vv in v.items()) + "\n}"
        else:
            body = json.dumps(v, ensure_ascii=False, indent=1, default=_default)
        parts.append(json.dumps(k) + ": " + body)
    Path(path).write_text("{\n" + ",\n".join(parts) + "\n}\n", encoding="utf-8")


def main():
    items, by_id, cases, placements = build()
    placements = placements + shop_placements(by_id)
    cb = card_board(by_id)
    placements.append(dict(item="SB1", surface="SHOP", shop="newsagent", where="glass", u_m=cb["glass_u_m"], z_bottom_m=cb["z_bottom_m"], w_m=cb["area_mm"][0] / 1000.0,
                           h_m=cb["area_mm"][1] / 1000.0, rot_deg=0.0, layer=1, age_class="B", inside=True, note="the card board: 15 cards, see card_board"))
    wt = wear_tables()
    wmap = {}
    for iid in ("P01", "P02", "P03", "J01", "D01", "W01", "B01", "M01", "G01", "G02", "T01", "T02", "T03", "F01", "F02", "P04"):
        wmap[iid] = "bill_pasted"
    for iid in ("C01a", "C01b", "C01c", "C02", "C03", "H03", "H04", "H05"):
        wmap[iid] = "notice_sleeve"
    for it in items:
        k = it["id"]
        if k in wmap:
            it["wear"] = dict(table=wmap[k], classes=[p["age_class"] for p in placements if p["item"] == k])
        elif k.startswith("SA"):
            it["wear"] = dict(table="card_ballpoint", classes=["B", "C"])
        elif k in ("P05", "P06", "K04", "K06b"):
            it["wear"] = dict(table="sticker", classes=["B", "C", "D"])
        elif k.startswith("K"):
            it["wear"] = dict(table="card_felt", classes=["A", "B", "C"])
        elif k in ("H01", "H02"):
            it["wear"] = dict(table="enamel_plate", classes=["B", "D"])
        elif k.startswith("S01"):
            it["wear"] = dict(table="cast_iron_plate", classes=["C", "D"])
        elif k.startswith("S0"):
            it["wear"] = dict(table="pressed_plate", classes=["C", "D"])
        elif k.startswith("L"):
            it["wear"] = dict(table="letting_board", classes=["B", "C", "D"])
    fonts = {}
    for k, v in FONTS.items():
        d = dict(v)
        d["ofl"] = ofl_info(v["dir"])
        d["cap_ratio_700"] = round(cap_ratio(k, 700), 3)
        d["path_hint"] = ("production/fonts/" + v["file"]) if v["in_repo"] else "NOT in production/fonts: the builder adds it with its OFL.txt (fetch: self_check.py --fetch-fonts DIR)"
        d["coverage"] = {ch: glyph_ok(k, ch) for ch in "£’·—–&.,?:0123456789"}
        fonts[k] = d
    # word lists
    words = sorted({norm(b["text"]) for it in items for b in it["blocks"] if not b.get("ghost")})
    ghosts = sorted({norm(b["text"]) for it in items for b in it["blocks"] if b.get("ghost")})
    tokens = sorted({t for w in words + ghosts for t in re.findall(r"[A-Za-z0-9£'&.\-]+", w)})
    # items out
    items_out = []
    hand_key = {id(HAND_FELT): "felt", id(HAND_FELT_FINE): "felt_fine", id(HAND_BALL): "ballpoint"}
    for it in items:
        o = dict(it)
        if it["kind"] in ("plate", "board"):
            o["stock"] = None      # painted faces: the colours are in the shapes and the paint table, not a paper stock
        o["words"] = sorted({norm(b["text"]) for b in it["blocks"]})
        nb = []
        for b in it["blocks"]:
            c = dict(b)
            c.pop("ink_colour", None)
            c.pop("ground", None)
            c["hand"] = hand_key.get(id(b["hand"])) if b.get("hand") else None
            c["contrast"] = {k: v for k, v in b["contrast"].items()}
            nb.append(c)
        o["blocks"] = nb
        items_out.append(o)
    ages = {c: dict(AGE[c]) for c in AGE}
    palette = dict(
        stocks={k: dict(name=v["name"], fresh=list(v["rgb"]), fade_to=(list(v["fade_to"]) if v["fade_to"] else None), tau_days=v["tau"], gsm=v["gsm"], aged={c: list(age_stock(k, c)) for c in AGE}) for k, v in STOCKS.items()},
        inks={k: dict(name=v["name"], fresh=(list(v["rgb"]) if v["rgb"] else None), tau_days=v["tau"]) for k, v in INKS.items()},
        paints={k: dict(name=v["name"], fresh=list(v["rgb"]), aged={c: list(age_paint(v["rgb"], c)) for c in AGE}) for k, v in PAINTS.items()},
        grime=list(GRIME), yellowed=list(YELLOWED))
    checks = make_checks(items, by_id, cases, placements)
    target = dict(
        schema="ledger.cloud-week-42.target.posters-boards-plates/1", family="posters-boards-plates",
        status="FIRST TRY, 8 October 2026 (cloud week 42), written from the PC's earlier notes, the repository and one reached photograph set; unit 4.2, 4.3 and 4.4 build from this file alone. self_check below is written by self_check.py.",
        summary_line=("%d sheets, cards, boards and plates for Quay Street's paper and small boards: 16 bills and stickers (the poll-tax set, the chapel hall's, the fights, the market, the Tivoli, two goods), "
                      "7 ferry and Harbour Board sheets, 5 police and council notices, 35 shop-window and newsagent cards, 4 letting boards with a proposed agent, 9 street name plates, 2 notice cases; every word ours and listed, "
                      "autumn 1990 dates with the weekdays computed, four ageing classes, a layered paste plan for the quay gable and the empty unit's glass, %d placements and %d checks." % (len(items), len(placements), len(checks))),
        units=dict(mm="every item's own frame: x from the viewer's LEFT edge as seen in the game, y UP from the bottom edge; baseline_mm is measured up from the bottom edge",
                   m="surfaces: u from the surface's viewer's-left edge, z up from the pavement; street x along the street (0 south)", colour="sRGB 0..255; contrast is WCAG; dE is CIE76 on Lab D65",
                   px_per_mm="2 for paper and cards (so 2.4 mm of fine print is 4.8 px), 1 for boards and plates"),
        kinds=dict(Read="printed in a source file", Scaled="measured off a drawing or the game's own files", Photo="measured on a photograph today", Derived="computed from the above",
                   Judgement="the writer's, overturned by a better source", Lead="a search summary: never a number"),
        axis=dict(rule="as the fascia target: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block; every item's x runs from the viewer's left; the gable SF1 is read looking +x with the front corner at the viewer's left",
                  evidence=["production/cloud-week/targets/fascia-signs/TARGET.md section 2", "production/previews/morning-hook-day-2026-10-08.jpg: the quay gable is the big brick wall at the right of the hook frame"]),
        calendar=dict(year=YEAR, window="1 October to 30 November 1990 by default; the dated bills' weekdays are computed, so any date in 1988 to 1992 can be set with date_slot rules",
                      note="1 October 1990 was a Monday. Every printed weekday is computed from datetime.date and checked by G.dates."),
        formats={k: dict(v) for k, v in FORMATS.items()},
        fonts=fonts, palette=palette, age_classes=ages,
        age_rules=dict(note="Four classes by days on the wall. Colour fade by ink: f = 1 - exp(-t / tau), tau in days (palette.inks, palette.stocks); paper yellows 30 per cent of YELLOWED at class D; grime film GRIME mixed 0, 5, 12, 22 per cent over the paper and 35 per cent of that over ink. Order of fastness (Judgement): fluorescent stock, then red, then blue, then black, then photocopier toner.",
                       paper_wear=dict(wrinkle=dict(amplitude_mm=[0.4, 1.5], wavelength_mm=[12, 40], note="wallpaper-paste cockling in the height map, stronger along the paste's brush direction (vertical)"),
                                       edge_lift=dict(corners=[0, 3], radius_mm=[15, 60], class_A=0, class_D=3), tears=dict(count=[0, 4], width_mm=[20, 140], from_edge=True),
                                       rain_runs=dict(count_per_m=[2, 8], length_mm=[10, 60], width_mm=[0.4, 1.5], opacity=[0.15, 0.4], direction="down from the top edge and from any lifted corner", ink="red and dye inks run first"),
                                       paste_halo=dict(width_mm=[2, 10], colour=[168, 148, 110], opacity=[0.15, 0.4], note="class C and D only, round the edges where a bill is lifting"),
                                       glue_stain=dict(note="dark (60,50,40) 0.25 opacity patches where a later bill has pasted over a lower one's tear"),
                                       loss=dict(class_B=[0, 0.05], class_C=[0.03, 0.2], class_D=[0.3, 0.6], note="share of the sheet gone: bottom corners and lower third first"),
                                       wet=dict(darken=0.12, saturation=1.1, note="a runtime hint for the material: bills darken and saturate when the wall is wet; roughness drops to 0.55 for a shower"),
                                       skew_deg=[-1.5, 1.5], overposting=dict(layers=[1, 3], note="each newer bill may cover up to 55 per cent of an older one; edges overlap 0 to 40 mm; the newer bill lies flatter"))),
        processes=PROCESSES, surfaces=SURFACES, west_piers=west_piers(), shops=shop_geometry(), card_board=cb, wear_tables=wt, placements=placements, cases=cases,
        photo=dict(P1=CASE_PHOTO, ratios=CASE_RATIOS, preview=["production/previews/cloud-week/refs/posters-boards-plates/P1-urban-street-01-notice-case.jpg",
                                                              "production/previews/cloud-week/refs/posters-boards-plates/P1-urban-street-01-notice-case-target-on-photo.jpg"]),
        items=items_out, approved_words=words, approved_word_parts=tokens, ghost_words=ghosts, proposed_names=PROPOSED,
        forbidden_patterns=FORBIDDEN_WORDS, checks=checks, disagreements_photographs_win=DISAGREEMENTS, sources=SOURCES, unreached=UNREACHED,
        would_read_when_network_opens=WOULD_READ, could_not_settle=COULD_NOT_SETTLE,
        evidence_split=dict(
            photographs_measured_today="the vertical proportions of one glazed notice case (P1); nothing else",
            earlier_notes="the 1990 mix of print (Letraset, photocopy, two-colour), the Kindersley recommendation of 1952, the 1 October 1990 winter timetable date, cod at about 2.60 a lb, the Harbour Board's blue and white enamel, the ferry's pasted winter sheets, the pound-and-pence prices of 1990 (all cited from the repository, not re-measured)",
            judgement="every size, colour, layout, wording, price, ageing number and placement not listed above"),
        self_check=None)
    target["hand_styles"] = dict(felt=HAND_FELT, felt_fine=HAND_FELT_FINE, ballpoint=HAND_BALL)
    write_json(target)
    print("wrote target.json", len(items), "items", len(checks), "checks", len(placements), "placements")



# --------------------------------------------------------------------------------------------
# 13. Shop windows and doors: the cards. Geometry from the fascia target (street x, door ends) and the recipe's shopfront numbers.
# --------------------------------------------------------------------------------------------
PIL_W, GLASS_W, DOOR_W, SIDE_W = 0.35, 3.562, 0.90, 0.838
SHOPS = {
    # id: (side, street x range, door end as the VIEWER sees it, the shop's name in hook-cast.json)
    "fish_market": ("east", (9.0, 15.0), "right"), "ritas": ("east", (15.0, 21.0), "left"), "steam_laundry": ("east", (27.0, 33.0), "left"),
    "grocer": ("east", (33.0, 39.0), "left"), "chandler": ("east", (40.0, 46.0), "left"),
    "tea_rooms": ("west", (24.0, 30.0), "left"), "ironmonger": ("west", (30.0, 36.0), "right"), "newsagent": ("west", (36.0, 42.0), "right"),
}


def shop_geometry():
    out = {}
    for sid, (side, (lo, hi), door) in SHOPS.items():
        if door == "right":      # glass at the viewer's left, then the shop door, then the side door
            g0 = PIL_W
            glass = (g0, g0 + GLASS_W)
            sdoor = (glass[1], glass[1] + DOOR_W)
            side_door = (sdoor[1], sdoor[1] + SIDE_W)
        else:                    # side door at the viewer's left, then the shop door, then the glass
            side_door = (PIL_W, PIL_W + SIDE_W)
            sdoor = (side_door[1], side_door[1] + DOOR_W)
            glass = (sdoor[1], sdoor[1] + GLASS_W)

        def sx(u):               # bay u (viewer's left) -> street x
            return round(hi - u, 3) if side == "east" else round(lo + u, 3)
        out[sid] = dict(id=sid, side=side, street_x_m=[lo, hi], door_end_viewer=door,
                        glass_u_bay_m=[round(v, 3) for v in glass], shop_door_u_bay_m=[round(v, 3) for v in sdoor], side_door_u_bay_m=[round(v, 3) for v in side_door],
                        glass_street_x_m=sorted([sx(glass[0]), sx(glass[1])]), shop_door_street_x_m=sorted([sx(sdoor[0]), sx(sdoor[1])]),
                        glass_z_m=[0.60, 2.40], door_glass_z_m=[1.00, 1.95], hours_plate_z_m=[1.355, 1.545],
                        note="u is metres from the bay's viewer's-left edge; glass 3.562 m, shop door 0.9, side door 0.838, pilasters 0.35 (shopfront C5, C8, C9); the order of the doors follows the fascia target's door ends")
    return out


def card_board(items_by_id, seed=1990):
    """The newsagent's window board: 15 cards laid on a 1100 x 900 mm area of the glass, no overlaps beyond the pins' corners."""
    rng = np.random.RandomState(seed)
    ids = [i for i in items_by_id if i.startswith("SA")]
    W, H = 760.0, 560.0
    placed = []
    # the tariff card first, top left; then rows from the top
    order = ["SA15"] + [i for i in ids if i != "SA15"]
    x, y, rowh = 20.0, H - 20.0, 0.0
    for iid in order:
        w, h = items_by_id[iid]["format"]["w_mm"], items_by_id[iid]["format"]["h_mm"]
        if x + w > W - 20:
            x, y, rowh = 20.0, y - rowh - 28, 0.0
        jitter = float(rng.uniform(-6, 6)), float(rng.uniform(-8, 8))
        placed.append(dict(item=iid, x_mm=round(x + jitter[0], 1), y_mm=round(y - h + jitter[1], 1), w_mm=w, h_mm=h, rot_deg=round(float(rng.uniform(-2.5, 2.5)), 1),
                           fixing=["pin top", "tape top-left", "tape top-right", "pin top and tape"][int(rng.randint(0, 4))]))
        x += w + 26 + float(rng.uniform(0, 14))
        rowh = max(rowh, h)
    return dict(id="SB1", title="the newsagent's window board of cards", area_mm=[W, H], glass_u_m=1.95, z_bottom_m=0.90, cards=placed, seed=seed,
                note="cards are taped to the inside of the glass (pins are for a cork board); 15 cards; no card overlaps another by more than a pin's corner; the area sits at glass u 1.95 to 2.71 m from the glass's viewer's-left edge, z 0.90 to 1.46 m")


def shop_placements(items_by_id):
    P = []

    def add(item, shop, where, u, z, rot=0.0, age="B", inside=False, note=None, show_when=None):
        it = items_by_id[item]
        P.append(dict(item=item, surface="SHOP", shop=shop, where=where, u_m=u, z_bottom_m=z, w_m=it["format"]["w_mm"] / 1000.0, h_m=it["format"]["h_mm"] / 1000.0,
                      rot_deg=rot, layer=1, age_class=age, inside=inside, note=note, show_when=show_when))
    # u for where="glass": metres from the glass's viewer's-left edge; for where="door": from the shop door's viewer's-left edge
    for k, (iid, u) in enumerate((("K09a", 0.30), ("K09b", 0.95), ("K09c", 1.60), ("K09d", 2.25), ("K09e", 2.80), ("K09f", 3.30))):
        add(iid, "fish_market", "glass", u, 0.66, rot=[-2, 3, -1, 2, -3, 1][k], inside=True, note="stuck in the fish on the slab, behind the glass: the shop-room builder's slab at about 0.6 m; decal cards on the interior card")
    add("K04", "fish_market", "door", 0.375, 1.05, note="NO DOGS, on the shop door's glass below the hours plate")
    add("K03a", "fish_market", "door", 0.35, 1.62, inside=True, show_when="open", note="the OPEN face when the shop is open (hook-cast hours); K03b when it is shut")
    add("K03a", "ritas", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "steam_laundry", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K06a", "steam_laundry", "glass", 0.20, 1.25, rot=1.0, inside=True, note="LAST WASH: the hour is an hour before the closing time in hook-cast.json (laundry 8 to 5.30)")
    add("K06b", "steam_laundry", "glass", 1.85, 1.00, rot=-0.8, note="a printed sticker on the outside of the glass")
    add("K06c", "steam_laundry", "interior", 0.0, 0.85, rot=2.0, inside=True, note="on a machine door, inside: the shop-room builder's; the card is the item")
    for k, (iid, u, z) in enumerate((("K07a", 0.20, 1.55), ("K07b", 0.95, 1.20), ("K07c", 1.70, 1.60), ("K07d", 2.45, 1.25))):
        add(iid, "grocer", "glass", u, z, rot=[-3, 2, -2, 4][k], inside=True, note="taped inside the glass; the fluorescent stock fades within weeks (tau 45 to 50 days)")
    add("K08", "grocer", "glass", 3.00, 0.95, inside=True, note="SORRY NO CREDIT GIVEN, A5 landscape, low in the glass")
    add("K04", "grocer", "door", 0.375, 1.05)
    add("K03a", "grocer", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "chandler", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "ironmonger", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "newsagent", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K05", "newsagent", "door", 0.345, 1.12, rot=1.5, note="PLEASE SHUT THE DOOR, taped to the door glass below the hours plate (1.355 to 1.545)")
    add("K02", "newsagent", "glass", 0.30, 1.20, inside=True, show_when="Monday 11.00 to 12.00 (hook-cast.json hals hours_breaks mon [11, 12]); hands at 12", note="BACK AT, hands at 12 o'clock")
    add("K04", "tea_rooms", "door", 0.375, 1.05)
    add("K03a", "tea_rooms", "door", 0.35, 1.62, inside=True, show_when="open")
    return P


def wear_tables():
    return dict(
        bill_pasted=dict(applies="P01 to P03, J01, D01, W01, B01, M01, G01, G02, T01 to T03: pasted bills", classes="age_rules", gable_extra="soot streaks from the eaves on the upper edge of every bill (opacity 0.1 to 0.25, 20 to 120 mm long), splash-back dirt in the lower 0.4 m (class C and D: 0.2 to 0.35 darker), bills lie over brick courses: the mortar lines show through as a 0.5 mm relief at 75 mm pitch"),
        glass_bill=dict(applies="bills on the empty unit's whitened glass", note="pasted on the outside of the glass: smooth, no brick relief; condensation runs stain the lower third of the paper, whitewash shows round and under, the lower edge curls out 3 to 8 mm, sun-fade is stronger (tau x 0.7)"),
        notice_sleeve=dict(applies="C01 a to c, C02, C03", sleeve="clear polythene 80 microns; a crease line across the sleeve 1 or 2 per sheet; fog on the inside 0.1 to 0.3 opacity in the lower third; water beads 6 to 20, 2 to 6 mm across, in the lower third; cable ties: 2, tails 40 to 90 mm left uncut; the paper inside yellows to class C within a season; the sheet slides down 5 to 20 mm inside the sleeve"),
        card_felt=dict(applies="K01, K02, K05, K06 a and c, K09, SA15 and the star cards", dog_ears="0 to 2 corners, radius 6 to 14 mm", smudge="0 or 1 finger smudge 5 to 12 mm", sun="the top third bleaches first (tau x 0.8)", tape="yellowed tape ghosts 25 x 40 mm at two corners where an older card hung", warp_mm=1.5),
        card_ballpoint=dict(applies="SA01 to SA14", note="record cards curl 1 to 3 mm, a pin hole top-centre, tape tabs yellowing, the ballpoint blue fades (tau 250 d), the felt heading fades slower; some cards sit crooked by 1 to 4 degrees; the board's oldest cards are class C"),
        sticker=dict(applies="P05, P06, K04, K06b", edge_lift_mm=[8, 20], scratches=[0, 4], loss_class_C=[0.05, 0.15], loss_class_D=[0.3, 0.6], note="a sticker on a lamp column wraps the shaft; peeled strips leave white paper-fibre residue"),
        enamel_plate=dict(applies="H01, H02", chips=[12, 30], chip_mm=[2, 9], rust_halo_mm=[3, 8], crazing="short crack lines 10 to 25 mm near the bolt holes", rust_tears_mm=[150, 400], bird_lime="1 streak from the top edge, 20 to 50 mm wide", salt_bloom="H02: white fur along the lower edge"),
        cast_iron_plate=dict(applies="S01 a, n, p (QUAY STREET)", flake_share=[0.03, 0.06], flake_note="paint lifts first at the raised letter edges, showing grey iron and a rust film (110,70,45)", face="white yellowed to class C/D (232,230,220 -> 214,208,190)", letters="black faded to 44,44,48", grime_gradient=0.12, screw_rust_mm=[20, 80], bird_lime="1 or 2 patches 20 to 50 mm on the top border"),
        pressed_plate=dict(applies="S02 and S03 (WEIGHHOUSE LANE, TANNERY ROW)", note="stove enamel on aluminium or vitreous enamel on steel: chips at the corners and at the screws only (4 to 12 chips of 2 to 6 mm), a grime gradient, no flaking of the letters; the enamel keeps its gloss (roughness 0.3 or 0.12)"),
        letting_board=dict(applies="L01 to L04", peel_bottom_edge="1 to 3 per cent of the area along the bottom edge, 2 to 6 mm bites", grime_streaks="3 to 7 streaks 100 to 300 mm from the top edge, 0.15 to 0.3 opacity", algae="class D: a 20 mm film along the foot, (62,78,52) at 0.3", rust_runs_mm=[40, 140], red_fade="the agent's red (178,34,40) fades towards chalk-pink (196,128,118) by 0.3 at class D", white_yellowing="agent white (236,236,230) to (214,206,184) at class D"),
        case=dict(applies="HC1, FC1", note="see the cases' own wear strings"),
    )


if __name__ == "__main__":
    main()
