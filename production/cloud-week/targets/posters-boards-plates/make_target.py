"""Author tool: writes target.json for Quay Street's paper and small boards (cloud week 42, 8 to 9 October 2026; SECOND TRY).

    /home/user/.bpyenv/bin/python make_target.py [--fonts DIR]

Three 2D units in one target:
  4.2  posters and notices (fly-posters, shop-window cards, council, police and Harbour Board notices,
       the poll-tax bills, the Tivoli's bills, the chapel hall's bills, the ferry timetable);
  4.3  "To Let" boards (the empty unit's board, the flats' and the house's boards);
  4.4  street name plates.

The hand-made decisions live in the tables below. Everything that can be computed is computed here and
written down, so that target_drawing.py and self_check.py can read target.json ALONE: ink widths from the
real OFL font files, cap heights, contrast ratios, aged colours, weekdays of every dated bill, the plates'
lengths, the pixel scale each item needs to be read glyph by glyph (glyphlib.py), the checks' nominal values.

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
sys.path.insert(0, str(HERE))
sys.dont_write_bytecode = True
import glyphlib as gl
SQUARE_TOL_DEG = 0.3          # ITEM.square: ONE tolerance for every item, print or hand-lettered (self_check.SQUARE_TOL_DEG is the same number; PLACE.built uses it too)
SQUARE_MARGIN = 0.02          # the estimate reports 0 unless F at the best angle beats F at 0 degrees by this much
CLEAN_MAX_MM2 = 2.0           # ITEM.clean: the area of ink outside every place lettering may stand
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
    "A": dict(label="fresh, 0 to 7 days", t_days=3, grime=0.00, yellow=0.00, days=[0, 7]),
    "B": dict(label="weeks, 8 to 35 days", t_days=18, grime=0.05, yellow=0.20, days=[8, 35]),
    "C": dict(label="months, 36 to 120 days", t_days=70, grime=0.12, yellow=0.50, days=[36, 120]),
    "D": dict(label="old, over 120 days", t_days=200, grime=0.22, yellow=1.00, days=[121, 400]),
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
    "vinyl_red": dict(rgb=(176, 30, 34), name="vinyl red (the fascia target's vinyl_red, 176,30,34)"),
    "brass": dict(rgb=(176, 140, 60), name="brass paper-fastener"),
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
    "archivo": dict(family="Archivo", file="Archivo-var.ttf", dir="archivo", axes={"Weight": None, "Width": 100}, designer="Omnibus-Type", rfn=None,
                    in_repo=False, looks_like="neutral grotesque: council notices, enamel signs, the police appeal"),
    "courier-prime": dict(family="Courier Prime", file="CourierPrime-Regular.ttf", dir="courierprime", axes={}, designer="Alan Dague-Greene", rfn=None,
                          in_repo=False, looks_like="IBM Courier: typed notices (Harbour Board, police, council)"),
    "courier-prime-bold": dict(family="Courier Prime", file="CourierPrime-Bold.ttf", dir="courierprime", axes={}, designer="Alan Dague-Greene",
                               rfn=None, in_repo=False, looks_like="Courier struck twice for a heading"),
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


STREET_DATE = datetime.date(1990, 10, 29)     # Monday 29 October 1990: the one day every dated placement allows (TARGET-REVIEW fault 8)


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
              blocks=[], shapes=[], art=[], placements=[], variants={}, wear={}, notes=[], words=[], proposed_names=[], paper_class=None, dated=None)
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
             overlap_ok=overlap_ok, note=note, min_contrast=min_contrast, glyph_check=(role != "imprint"))
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
GENERIC_FOOTER = "STAND TOGETHER"                   # what the default poll-tax bills carry where the named ones carry CAMPAIGN
PROPOSED = [
    dict(name="MERIDIAN AGAINST THE POLL TAX", what="the invented local anti-poll-tax campaign (ruling 3 Oct: an invented local campaign, never real parties or people). First proposed by the asset plan note 4, used by the 4 Oct bills.", mint="town task"),
    dict(name="QUAY PRINT", what="the jobbing printer named in the imprint of every printed bill (an imprint was the custom and is expected on political and campaign matter); 2.4 mm, illegible, allowed on the default street", mint="town task"),
    dict(name="ARMITAGE & STOBBS", what="the estate agent on the named letting boards L01 and L03 (the brief asks for a proposed name, marked 'proposed, not minted')", mint="town task"),
    dict(name="THE SANDERLING TRIO", what="the dance band on the named chapel-hall dance bill", mint="town task"),
    dict(name="THE HARPOONER", what="a ring name on the named wrestling bill (renamed from the first try's THE SEA WOLF, which is Jack London's novel; not checked against real lists: the network is closed)", mint="town task"),
    dict(name="TED HOLROYD", what="a ring name on the named wrestling bill (TIGER JIM LARKIN carried a real dock-union leader's name; the first rewrite, BIG TED HOLROYD, is gone too: \"Big Ted\" is the teddy bear of the BBC children's programme Play School, a real programme's character and a child-coded name; not checked against real lists)", mint="town task"),
    dict(name="SPANNER SMITH", what="a ring name on the named wrestling bill (renamed from MAD MAURICE; not checked against real lists)", mint="town task"),
    dict(name="THE STEVEDORE", what="a ring name on the named wrestling bill (renamed from THE BARON, a real television series' title; not checked against real lists)", mint="town task"),
    dict(name="THE FOURTH WITNESS", what="an invented film at the Tivoli, on the named bills T01 and T03 (a film of that name was not checkable: the network is closed)", mint="town task"),
    dict(name="A WEEK AT GULLWING", what="an invented film at the Tivoli, on the named bills T02 and T03 (Gullwing is a minted district)", mint="town task"),
    dict(name="WHITEWELL", what="an invented washday powder on the four-sheet G01", mint="town task"),
    dict(name="QUAYSIDE", what="an invented tea on the bill G02", mint="town task"),
    dict(name="MARSHLAND PICTURES", what="the invented studio in the named films' billing block (6 to 12 mm)", mint="town task"),
    dict(name="A. VENN", what="an invented credit in the named films' billing block", mint="town task"),
    dict(name="R. CORLEY", what="an invented credit in the named films' billing block", mint="town task"),
    dict(name="H. MADDOX", what="an invented credit in the named films' billing block", mint="town task"),
    dict(name="THE DRILL HALL", what="the hall where the boxing and the named wrestling bills are held (a generic building, no street given)", mint="town task"),
]
HELD_CAP_MM = 10.0     # a proposed name in a block of this cap or more is READABLE from across the street (about 8 px a capital at 8 m): the item is held until the town mints it


# The NAMELESS bills (second review, fault 3): a Tivoli quad whose title is "A NEW COMEDY", a programme that names no film, a wrestling bill that names no ring and no hall read as
# placeholders by another name. They are held like their named twins and built only once the town mints the names the twin carries. (D01's LIVE MUSIC and the poll-tax bills'
# STAND TOGETHER read naturally and stay.)
STAND_INS = {"T01": "T01-named", "T02": "T02-named", "T03": "T03-named", "W01": "W01-named"}
STAND_IN_WHY = ("a bill that names no film, no hall and no ring names reads as a placeholder by another name (second review, fault 3; the 3 October ruling keeps placeholders off his page): "
                "held with its named twin and built only once the town mints the names the twin carries")


def held_names(item):
    """The proposed names an item carries in blocks of cap 10 mm or more, alone or running over consecutive lines (empty: the item may stand on the default street)."""
    out = []
    big = [b for b in item["blocks"] if b["role"] != "imprint" and b["cap_mm"] >= HELD_CAP_MM and not b.get("ghost")]
    texts = [b["text"] for b in big] + [" ".join(b["text"] for b in big)]
    for t in texts:
        for p in PROPOSED:
            if p["name"].lower() in t.lower() and p["name"] not in out:
                out.append(p["name"])
    return out


def nid(base, named):
    return base + "-named" if named else base




# --------------------------------------------------------------------------------------------
# 5. Printed bills (unit 4.2): the poll-tax set, the chapel hall's, the fights, the market, the Tivoli, the goods.
# --------------------------------------------------------------------------------------------

OSW, FRK, JOS, ALF, FRA, OST, OSTR, ARC = ("oswald", "libre-franklin", "jost", "alfa-slab-one", "fraunces", "old-standard-tt",
                                           "old-standard-tt-regular", "archivo")
CPR, CPB, PAT, MAR = "courier-prime", "courier-prime-bold", "patrick-hand", "marcellus-sc"
OSI = "old-standard-tt-italic"
SKEW_NOTE = "skew is the PLACEMENT's rot_deg only: every texture is square-on"


def L(text, f, w, cap=None, gap=None, ink="black", on="stock", trk=0.0, tech=None, role="text", **kw):
    d = dict(text=text, f=f, w=w, cap=(cap if cap is not None else 10), ink=ink, on=on, trk=trk, tech=tech, role=role)
    if gap is not None:
        d["gap"] = gap
    d.update(kw)
    return d


def meta(it, paper_class, dated_kind=None, d=None, m=None, label=None, named_of=None):
    it["paper_class"] = paper_class
    if dated_kind:
        it["dated"] = dict(kind=dated_kind, date="1990-%02d-%02d" % (m, d), label=label)
    if named_of:
        it["named_of"] = named_of
    return it


def imprint(item, text, y=20, cx=None, cap=2.4, ink="black", on="stock"):
    """The printer's imprint, set in 7 point (cap 2.4 mm): legal matter on printed bills, texture at game distance. Proposed names are allowed here
    (illegible, under the 10 mm line); the glyph check does not read imprints."""
    cx = item["format"]["w_mm"] / 2.0 if cx is None else cx
    return T(item, "imprint", text, FRK, 500, cap, y, cx, "centre", ink=ink, on=on, role="imprint", tech="7 point, below the legibility floor at 3 m by design")


def footer_bar(it, box, text=CAMPAIGN, cap=None, ink="paper", bar_fill="black", f=OSW, w=600, trk=0.06):
    S(it, "footer_bar", "rect", box=box, fill=bar_fill, fill_kind="ink")
    cx = (box[0] + box[2]) / 2.0
    cap = cap or capfit(f, w, text, (box[2] - box[0]) - 24, trk)
    cap = min(cap, 0.45 * (box[3] - box[1]))
    T(it, "campaign", text, f, w, cap, (box[1] + box[3]) / 2.0 - cap / 2.0, cx, "centre", ink=ink, on="ink:" + bar_fill, trk=trk, role="name")


def bill_poll_meeting(named=False):
    it = new_item(nid("P01", named), "4.2", "poll_tax_bills", "Poll tax: public meeting bill" + (" (named campaign, held)" if named else ""), 508, 762, stock="fluor_yellow", process="screen_2col", fmt="double_crown", margin=18)
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
    footer_bar(it, [18, 30, 490, 82], text=(CAMPAIGN if named else GENERIC_FOOTER))
    imprint(it, PUBLISHER + " " + IMPRINT, y=20)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "red pass shifted 0.3 to 0.8 mm", "one has a top corner torn 60 to 140 mm", SKEW_NOTE])
    it["event"] = dict(date="THURSDAY 25 OCTOBER", d=25, m=10)
    it["bottom_y"] = y
    return meta(it, "poll_tax_bill", "event", 25, 10, "the public meeting", named_of=("P01" if named else None))


def bill_dont_pay(named=False):
    it = new_item(nid("P02", named), "4.2", "poll_tax_bills", "Poll tax: don't pay bill" + (" (named campaign, held)" if named else ""), 508, 762, stock="fluor_orange", process="screen_1col", fmt="double_crown", margin=18)
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
    footer_bar(it, [18, 30, 490, 82], text=(CAMPAIGN if named else GENERIC_FOOTER))
    imprint(it, PUBLISHER + " " + IMPRINT, y=20)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "one overposted by P03 over its lower third", SKEW_NOTE,
                                     "the A3 window version (placement scale 0.585: 297 x 446 mm, taped inside the glass) is this texture scaled by the placement, not a new item"])
    it["bottom_y"] = y
    return meta(it, "poll_tax_bill", named_of=("P02" if named else None))


def bill_march(named=False):
    it = new_item(nid("P03", named), "4.2", "poll_tax_bills", "Poll tax: march bill" + (" (named campaign, held)" if named else ""), 508, 762, stock="white_poster", process="letterpress_2col", fmt="double_crown", margin=18)
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
    footer_bar(it, [64, 30, 490, 82], text=(CAMPAIGN if named else GENERIC_FOOTER))
    imprint(it, PUBLISHER + " " + IMPRINT, y=20, cx=277)
    it["variants"] = dict(n=3, vary=["age class A, B, C", "ink density", "overposted by P01 at the foot in one", SKEW_NOTE])
    it["event"] = dict(date=dated(10, 11), d=10, m=11)
    it["bottom_y"] = y
    return meta(it, "poll_tax_bill", "event", 10, 11, "the march", named_of=("P03" if named else None))


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
    typed_lines = ["Bring your summons and any letters you have had.", "We will go through them with you.", "Free and confidential. Come on your own", "or bring a neighbour."]
    for i, t in enumerate(typed_lines):
        T(it, "typed%d" % (i + 1), t, CPR, 400, 2.455, y - 6 - i * 8.47, 16, "left", ink="toner", tech="typed, 10 pitch, photocopied", role="body")
    y2 = y - 6 - len(typed_lines) * 8.47 - 8
    T(it, "campaign", CAMPAIGN, ARC, 800, 6.0, 22, 105, "centre", ink="toner", trk=0.06, role="name", tech="photocopied")
    it["variants"] = dict(n=3, vary=["paper: pale green, pale yellow, white", "toner speckle and a copier edge shadow", SKEW_NOTE + " (0.2 to 1.5 degrees)"])
    it["event"] = dict(date="TUESDAY 30 OCTOBER", d=30, m=10)
    it["bottom_y"] = y2
    return meta(it, "poll_tax_bill", "event", 30, 10, "the advice evening")


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
    return meta(it, "sticker")


def sticker_cantpay():
    it = new_item("P06", "4.2", "poll_tax_bills", "Poll tax: sticker, 148 x 52", 148, 52, stock="white_poster", process="sticker_print", fmt=None, margin=4, kind="sticker")
    S(it, "bar", "rect", box=[2, 2, 146, 50], fill="black", fill_kind="ink")
    T(it, "slogan", "CAN’T PAY — WON’T PAY", OSW, 700, capfit(OSW, 700, "CAN’T PAY — WON’T PAY", 130, 0.03), 24, 74, "centre", ink="paper", on="ink:black", trk=0.03, role="name")
    T(it, "campaign", CAMPAIGN, OSW, 600, 4.0, 10, 74, "centre", ink="paper", on="ink:black", trk=0.06)
    it["variants"] = dict(n=2, vary=["as P05"])
    return meta(it, "sticker")


def bill_jumble():
    """A photocopied A3 notice (TARGET-REVIEW fault 7: a 1990 jumble-sale notice 'is Letraset, photocopy or two-colour screen print', asset-plan note 4)."""
    it = new_item("J01", "4.2", "chapel_hall", "Jumble sale notice (chapel hall), A3 photocopy", 297, 420, stock="pale_pink", process="photocopy_a3", fmt="A3", margin=12)
    S(it, "frame", "frame", box=[8, 8, 289, 412], fill="toner", fill_kind="ink", width_mm=2.4, note="two rules photocopied from a printed original, 2.4 mm; hairline gaps at the corner joints")
    y = stack(it, "L", [
        L("GRAND", OST, 700, 22, gap=6, ink="toner", trk=0.30, tech="Letraset-style heading, photocopied"),
        L("JUMBLE SALE", OSW, 700, fitw=240, gap=8, ink="toner"),
        L("THE CHAPEL HALL", OSW, 600, 16, gap=10, ink="toner", trk=0.08),
    ], 148.5, 402, fill_bottom=290)
    S(it, "rule_a", "rule", box=[24, y - 2, 273, y + 0.6], fill="toner", fill_kind="ink")
    y = stack(it, "M", [
        L(dated(20, 10), OSW, 700, fitw=230, gap=8, ink="toner", trk=0.02),
        L("DOORS OPEN 2 PM", OSW, 600, 15, gap=12, ink="toner", trk=0.06),
        L("CLOTHING · BOOKS · BRIC-A-BRAC · HOUSEHOLD", OSTR, 400, fitw=245, gap=10, ink="toner", trk=0.02),
        L("Teas and cakes", OSI, 400, 10, gap=12, ink="toner"),
        L("ADMISSION 20p", FRK, 800, 11, gap=8, ink="toner", trk=0.05),
        L("IN AID OF THE CHAPEL ROOF FUND", FRK, 700, 8, gap=6, ink="toner", trk=0.05),
    ], 148.5, y - 10, fill_bottom=36)
    imprint(it, IMPRINT, y=17)
    it["variants"] = dict(n=3, vary=["age class A, B", "toner density and edge shadow (processes.photocopy_a3)", "one half-covered by P03 or W01 (never placed so by default)", SKEW_NOTE + " (0.2 to 1.5 degrees)"])
    it["event"] = dict(date=dated(20, 10), d=20, m=10)
    it["bottom_y"] = y
    return meta(it, "fly_poster", "event", 20, 10, "the jumble sale")


def bill_dance(named=False):
    """A photocopied A3 notice, as J01. The nameless default says LIVE MUSIC where the named variant names the band."""
    it = new_item(nid("D01", named), "4.2", "chapel_hall", "Old-time and sequence dance notice (chapel hall), A3 photocopy" + (" (named band, held)" if named else ""), 297, 420, stock="pale_yellow", process="photocopy_a3", fmt="A3", margin=12)
    S(it, "frame", "frame", box=[8, 8, 289, 412], fill="toner", fill_kind="ink", width_mm=2.8, note="a double-width rule photocopied from a printed original")
    y = stack(it, "L", [
        L("OLD TIME", OST, 700, fitw=230, gap=5, ink="toner", tech="photocopied from a printed original"),
        L("and", OSI, 400, 15, gap=4, ink="toner"),
        L("SEQUENCE", OST, 700, fitw=230, gap=14, ink="toner"),
        L("DANCING", ALF, 400, fitw=230, gap=12, ink="toner"),
    ], 148.5, 402, fill_bottom=270)
    lines = [
        L(dated(17, 11), OSW, 700, fitw=210, gap=8, ink="toner", trk=0.02),
        L("7.30 TO 11 PM", OSW, 600, 24, gap=9, ink="toner", trk=0.04),
        L("THE CHAPEL HALL", OSW, 600, 17, gap=14, ink="toner", trk=0.06),
    ]
    if named:
        lines += [L("Music by", OSI, 400, 11, gap=5, ink="toner"), L("THE SANDERLING TRIO", OST, 700, fitw=210, gap=14, ink="toner", trk=0.04)]
    else:
        lines += [L("LIVE MUSIC", OST, 700, fitw=170, gap=14, ink="toner", trk=0.04)]
    lines += [L("TEA AND SANDWICHES", FRK, 800, 9.5, gap=6, ink="toner", trk=0.06),
              L("ADMISSION £1.50", FRK, 800, 9.5, gap=6, ink="toner", trk=0.06),
              L("ALL WELCOME", FRK, 800, 9.5, gap=6, ink="toner", trk=0.08)]
    y = stack(it, "M", lines, 148.5, y - 12, fill_bottom=34)
    imprint(it, IMPRINT, y=17)
    it["variants"] = dict(n=3, vary=["age class A, B", "toner density and edge shadow", SKEW_NOTE + " (0.2 to 1.5 degrees)"])
    it["event"] = dict(date=dated(17, 11), d=17, m=11)
    it["bottom_y"] = y
    return meta(it, "fly_poster", "event", 17, 11, "the dance", named_of=("D01" if named else None))


def bill_wrestling(named=False):
    it = new_item(nid("W01", named), "4.2", "fights", "Professional wrestling bill" + (" (ring names and venue named, held)" if named else ""), 508, 762, stock="pale_yellow", process="letterpress_2col", fmt="double_crown", margin=18)
    top = [L("PROFESSIONAL", OSW, 700, fitw=428, gap=8, ink="black", trk=0.12),
           L("WRESTLING", OSW, 700, fitw=460, gap=14, ink="red", tech="letterpress red")]
    if named:
        top.append(L("THE DRILL HALL", OSW, 600, 34, gap=12, ink="black", trk=0.08))
    top += [L(dated(2, 11), OSW, 700, fitw=420, gap=8, ink="black", trk=0.02), L("BELL 7.30 PM", OSW, 600, 34, gap=24, ink="red", trk=0.06)]
    y = stack(it, "L", top, 254, 738, fill_bottom=452)
    S(it, "rule_a", "rule", box=[40, y + 6, 468, y + 9.4], fill="black")
    if named:
        mid = [L("THE HARPOONER", OSW, 700, fitw=380, gap=4, ink="black"), L("v", OSI, 400, 14, gap=4, ink="red"),
               L("SPANNER SMITH", OSW, 700, fitw=380, gap=18, ink="black"), L("TED HOLROYD", OSW, 700, fitw=295, gap=4, ink="black"),
               L("v", OSI, 400, 14, gap=4, ink="red"), L("THE STEVEDORE", OSW, 700, fitw=300, gap=14, ink="black")]
    else:
        mid = [L("HEAVYWEIGHT CONTEST", OSW, 700, fitw=380, gap=14, ink="black"), L("TAG TEAM CONTEST", OSW, 700, fitw=380, gap=16, ink="black")]
    mid += [L("AND SUPPORT BOUTS", OSW, 600, 20, gap=22, ink="black", trk=0.08),
            L("RINGSIDE £4 · UNRESERVED £2.50", FRK, 800, 17, gap=8, ink="red", trk=0.04),
            L("TICKETS AT THE DOOR", FRK, 700, 14, gap=8, ink="black", trk=0.08)]
    y = stack(it, "M", mid, 254, y - 6, fill_bottom=50)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=3, vary=["age class A, B", "red pass shifted", "one with the date line struck through by a hand-painted band (event over): a red felt-pen stripe, NO new words", SKEW_NOTE])
    it["event"] = dict(date=dated(2, 11), d=2, m=11)
    it["bottom_y"] = y
    return meta(it, "fly_poster", "event", 2, 11, "the wrestling night", named_of=("W01" if named else None))


def bill_boxing():
    it = new_item("B01", "4.2", "fights", "Boxing night bill (venue named, held)", 508, 762, stock="pale_blue", process="letterpress_2col", fmt="double_crown", margin=18)
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
    it["variants"] = dict(n=2, vary=["age class A, B", SKEW_NOTE])
    it["event"] = dict(date=dated(16, 11), d=16, m=11)
    it["bottom_y"] = y
    return meta(it, "fly_poster", "event", 16, 11, "the boxing night")


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
    it["variants"] = dict(n=2, vary=["age class B, D (the old one is mostly paste and one torn half)", SKEW_NOTE])
    it["bottom_y"] = y
    return meta(it, "fly_poster")


def goods_whitewell():
    it = new_item("G01", "4.2", "goods", "Washday powder four-sheet (invented brand, held)", 1016, 1524, stock="white_poster", process="litho_4col", fmt="four_sheet", margin=30)
    it["art"].append(dict(id="art", box_mm=[0, 420, 1016, 1524], kind="litho_picture", seed="G01", nominal_rgb=[196, 214, 232],
                          describe="a washing line of white sheets and towels in a bright cold wind over a terraced back-yard wall, the sky pale blue; no people, no faces, no lettering anywhere in the picture",
                          forbidden="people, hands, faces, children, text, lettering, numerals, logos, crowns, kiosk lettering, operator marks, bottles, glasses, arcade or amusement signs, any real product",
                          zone_note="the sheets are the whitest area; the sky is behind the title"))
    S(it, "title_band", "rect", box=[0, 0, 1016, 420], fill="blue", fill_kind="ink")
    T(it, "name", "WHITEWELL", ALF, 400, capfit(ALF, 400, "WHITEWELL", 900), 250, 508, "centre", ink="paper", on="ink:blue", trk=0.02, role="name")
    T(it, "line1", "WASHES WHITE", OSW, 700, 70, 150, 508, "centre", ink="paper", on="ink:blue", trk=0.1, role="line")
    T(it, "line2", "FOR TWIN-TUB, AUTOMATIC AND HAND WASHING", FRK, 700, 24, 90, 508, "centre", ink="paper", on="ink:blue", trk=0.06)
    imprint(it, IMPRINT, y=40, cap=4.0, ink="paper", on="ink:blue")
    it["variants"] = dict(n=2, vary=["age class C, D", "one with the lower half pasted over by P03 and P01"])
    it["notes"].append("A national-style four-sheet advertisement belongs in a contractor's framed panel in 1990, not pasted under fly-posters (TARGET-REVIEW note): this item is held AND not placed on Quay Street.")
    return meta(it, "fly_poster")


RING = dict(kind="ring", note="a white ring: centre, inner and outer radius in mm")


def goods_tea():
    it = new_item("G02", "4.2", "goods", "Tea bill (invented brand, held)", 508, 762, stock="cream", process="letterpress_2col", fmt="double_crown", margin=18)
    y = stack(it, "L", [
        L("QUAYSIDE", ALF, 400, fitw=440, gap=10, ink="red", tech="letterpress red"),
        L("TEA", ALF, 400, fitw=300, gap=22, ink="black"),
        L("A good strong cup", FRA, 700, fitw=420, gap=24, ink="black"),
    ], 254, 738)
    cx, cy, R = 254.0, y - 130.0, 120.0
    S(it, "cup", "roundel", box=[cx - R, cy - R, cx + R, cy + R], fill="red", fill_kind="ink", note="a flat red disc standing for a cup seen from above; our own drawing, no photograph")
    S(it, "cup_ring", "ring", centre_mm=[cx, cy], r_inner_mm=0.70 * R - 8.0, r_outer_mm=0.70 * R + 8.0, fill="paper", fill_kind="stock",
      note="the cup's white ring: 16 mm wide, centred on 0.70 of the disc's radius (TARGET-REVIEW fault 11)")
    T(it, "price", "80 BAGS · £1.35", OSW, 700, 52, 100, 254, "centre", ink="black", role="line", trk=0.03)
    imprint(it, IMPRINT, y=30)
    it["variants"] = dict(n=2, vary=["age class B, C", SKEW_NOTE])
    it["bottom_y"] = y
    return meta(it, "fly_poster")


# ---- the Tivoli ------------------------------------------------------------------------------------
STRIP_H = 90.0


def tivoli_strip(film, d, m):
    """The venue and date strip pasted across the top band of a quad (TARGET-REVIEW fault 7: a distributor's quad carried no venue; the cinema pasted its own strip)."""
    it = new_item("%ss" % film, "4.2", "tivoli", "Tivoli venue strip for %s, 1016 x 90, letterpress black on white" % film, 1016, 90, stock="white_poster", process="letterpress_1col", fmt=None, margin=8)
    T(it, "tivoli", "THE TIVOLI", OSW, 700, 36, 27, 30, "left", ink="black", trk=0.20, role="name", tech="letterpress black")
    T(it, "start", "FROM " + dated(d, m), OSW, 600, 30, 29, 986, "right", ink="black", trk=0.12, role="line", tech="letterpress black")
    it["variants"] = dict(n=2, vary=["age class B (the quad's own class) and A", "set 2 to 6 mm off square on the quad's top band: the placement's rot_deg carries it; the strip's own texture is square-on"])
    it["event"] = dict(date=dated(d, m), d=d, m=m)
    return meta(it, "strip", "event", d, m, "the film's first day")


def tivoli_witness(named=False):
    it = new_item(nid("T01", named), "4.2", "tivoli", "Tivoli quad: " + ("THE FOURTH WITNESS (named film, held)" if named else "a new thriller (no title minted)"), 1016, 762, stock="white_poster", process="litho_4col", fmt="quad_crown", margin=26)
    it["art"].append(dict(id="art", box_mm=[0, 0, 1016, 762], kind="litho_picture", seed="T01", nominal_rgb=[16, 20, 34],
                          describe="a narrow wet cobbled street at night seen from a first-floor window, lamplight in orange pools on the cobbles, one lit window far down the street, rain on the glass in the near corner; dark blue and black with orange; no people, no faces, no lettering, no signs, no telephone box",
                          forbidden="people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks or telephone boxes, operator marks, real brands, real places, vehicles with plates, bottles, glasses, arcade or amusement signs",
                          zone_note="the top 90 mm stays blank and dark (the venue strip T01s is pasted there); the lower third and the left must stay dark and low in detail: a scrim is laid there for the words"))
    S(it, "scrim_bottom", "scrim", box=[0, 0, 1016, 300], rgb=[10, 14, 26], alpha_top=0.0, alpha_bottom=0.85, note="gradient, fully dark at the foot")
    S(it, "scrim_top", "scrim", box=[0, 672, 1016, 762], rgb=[10, 14, 26], alpha_top=0.9, alpha_bottom=0.9, note="the top band is flat dark and BLANK: no lettering of any kind in the litho; the strip T01s is pasted over it")
    ART = "art:16,20,34"
    T(it, "tag", "Somebody saw. Somebody will pay.", FRA, 600, 30, 628, 508, "centre", ink_paint="agent_white", on=ART, role="tagline")
    if named:
        T(it, "title1", "THE FOURTH", OSW, 700, 128, 250, 70, "left", ink_paint="agent_white", on=ART, trk=0.02, role="title")
        T(it, "title2", "WITNESS", OSW, 700, 128, 98, 70, "left", ink_paint="lamp_orange", on=ART, trk=0.02, role="title")
        T(it, "billing1", "A MARSHLAND PICTURES PRODUCTION · SCREENPLAY BY A. VENN", OSW, 500, 12.0, 62, 70, "left", ink_paint="agent_white", on=ART, trk=0.06, role="billing")
        T(it, "billing2", "MUSIC BY R. CORLEY · DIRECTED BY H. MADDOX", OSW, 500, 12.0, 40, 70, "left", ink_paint="agent_white", on=ART, trk=0.06, role="billing")
    else:
        T(it, "title1", "A NEW", OSW, 700, 128, 250, 70, "left", ink_paint="agent_white", on=ART, trk=0.02, role="title")
        T(it, "title2", "THRILLER", OSW, 700, 128, 98, 70, "left", ink_paint="lamp_orange", on=ART, trk=0.02, role="title")
    it["variants"] = dict(n=2, vary=["age class B, C", "one cut in half by a torn edge, the title half left", SKEW_NOTE])
    it["event"] = dict(date="THURSDAY 18 OCTOBER", d=18, m=10)
    return meta(it, "fly_poster", "event", 18, 10, "the film's first day", named_of=("T01" if named else None))


def tivoli_gullwing(named=False):
    it = new_item(nid("T02", named), "4.2", "tivoli", "Tivoli quad: " + ("A WEEK AT GULLWING (named film, held)" if named else "a new comedy (no title minted)"), 1016, 762, stock="white_poster", process="litho_4col", fmt="quad_crown", margin=26)
    it["art"].append(dict(id="art", box_mm=[0, 0, 1016, 762], kind="litho_picture", seed="T02", nominal_rgb=[50, 100, 168],
                          describe="a pale empty beach under a high pale-blue sky with a row of striped deckchairs lined up empty on the sand and a wooden breakwater running to a calm sea, bright flat colours like a saucy postcard; no buildings, no pier, no people, no faces, no lettering",
                          forbidden="people, hands, faces, children, text, lettering, numerals, signs, crowns, kiosks, operator marks, real brands, buildings, a pier, arcade or amusement signs, drink, bottles, glasses, gambling machines",
                          zone_note="the top 90 mm stays clear flat sky (the venue strip T02s is pasted there); the sky across the top 40 per cent stays clear and flat for the title"))
    ART = "art:50,100,168"
    if named:
        T(it, "title1", "A WEEK AT", FRA, 900, 80, 585, 508, "centre", ink_paint="agent_white", on=ART, trk=0.0, role="title")
        T(it, "title2", "GULLWING", FRA, 900, min(125.0, capfit(FRA, 900, "GULLWING", 760)), 415, 508, "centre", ink_paint="agent_red", on="paint:agent_white", role="title")
    else:
        T(it, "title1", "A NEW", FRA, 900, 80, 585, 508, "centre", ink_paint="agent_white", on=ART, trk=0.0, role="title")
        T(it, "title2", "COMEDY", FRA, 900, min(125.0, capfit(FRA, 900, "COMEDY", 760)), 415, 508, "centre", ink_paint="agent_red", on="paint:agent_white", role="title")
    T(it, "tag", "The funniest week of their lives.", FRA, 600, 30, 70, 508, "centre", ink_paint="agent_navy", on="art:236,214,150", role="tagline")
    if named:
        T(it, "billing", "A MARSHLAND PICTURES PRODUCTION · DIRECTED BY H. MADDOX", OSW, 500, 12.0, 36, 508, "centre", ink_paint="agent_navy", on="art:236,214,150", trk=0.06, role="billing")
    S(it, "title_panel", "rect", box=[110, 385, 906, 560], fill="agent_white", fill_kind="paint", note="a pale panel behind the red title so the red holds; the sky shows round it")
    it["variants"] = dict(n=2, vary=["age class A, B", "one with the sky bleached to near white", SKEW_NOTE])
    it["event"] = dict(date="THURSDAY 25 OCTOBER", d=25, m=10)
    return meta(it, "fly_poster", "event", 25, 10, "the film's first day", named_of=("T02" if named else None))


def tivoli_programme(named=False):
    it = new_item(nid("T03", named), "4.2", "tivoli", "Tivoli programme bill" + (" (named films, held)" if named else " (no titles minted)"), 508, 762, stock="white_poster", process="letterpress_2col", fmt="double_crown", margin=18)
    t1, t2 = ("THE FOURTH WITNESS", "A WEEK AT GULLWING") if named else ("A NEW THRILLER", "A NEW COMEDY")
    y = stack(it, "L", [
        L("THE TIVOLI", OSW, 700, fitw=440, gap=18, ink="red", trk=0.10, tech="letterpress red"),
        L("FROM THURSDAY 18 OCTOBER", OSW, 600, fitw=420, gap=10, ink="black", trk=0.06),
        L(t1, OSW, 700, fitw=440, gap=30, ink="black"),
        L("FROM THURSDAY 25 OCTOBER", OSW, 600, fitw=420, gap=10, ink="black", trk=0.06),
        L(t2, OSW, 700, fitw=440, gap=34, ink="black"),
    ], 254, 736, fill_bottom=330)
    S(it, "rule_a", "rule", box=[40, y + 12, 468, y + 15.4], fill="black")
    y = stack(it, "M", [
        L("PERFORMANCES 5.15 AND 8.00", OSW, 600, fitw=440, gap=14, ink="black", trk=0.05),
        L("SATURDAY ALSO 2.30", OSW, 600, fitw=330, gap=30, ink="black", trk=0.05),
        L("ALL SEATS £2.80", FRK, 800, fitw=300, gap=10, ink="red", trk=0.04),
        L("O.A.P. AND UNWAGED £1.50", FRK, 800, fitw=440, gap=8, ink="red", trk=0.04),
    ], 254, y - 10, fill_bottom=70)
    imprint(it, IMPRINT, y=24)
    it["variants"] = dict(n=2, vary=["age class A, B", "one with the lower half torn away", SKEW_NOTE])
    it["event"] = dict(date="THURSDAY 18 OCTOBER", d=18, m=10)
    it["bottom_y"] = y
    return meta(it, "fly_poster", "event", 18, 10, "the first film's first day", named_of=("T03" if named else None))
def typed(item, prefix, lines, x, top, pitch=4.233, f=CPR, wt=400, cap=2.455, ink="typed", tech="typed, 10 pitch", role="body", on="stock", anchor="left"):
    """Typewritten lines at a fixed pitch: Courier Prime at 12 point (cap 2.455 mm, 10 characters to the inch = 2.54 mm advance)."""
    for i, t in enumerate(lines):
        if t == "":
            continue
        T(item, "%s%d" % (prefix, i + 1), t, f, wt, cap, top - i * pitch, x, anchor, ink=ink, on=on, tech=tech, role=role)
    return top - len(lines) * pitch


def ferry_times():
    """The timetable as numbers, so the check can prove it is a service ONE vessel could run: the boat crosses in 15 minutes, leaves the Hook at :00 and :30
    by day and the far side 15 minutes later, and each day ENDS where the next day's first sailing LEAVES (TARGET-REVIEW fault 12): the far side's last
    crossing is 11.15 PM, so the boat is back at the Hook at 11.30 PM and the street's 'last crossing's at eleven' still holds from the Hook."""
    return dict(
        crossing_minutes=15,
        mon_sat=dict(hook_first=["6.30", "7.00", "7.30"], hook_half_hourly_until="5.30 PM", hook_then=["6.30", "7.30", "8.30", "9.30", "10.30"], hook_last="11.00",
                     far_first=["6.45", "7.15", "7.45"], far_half_hourly_until="5.45 PM", far_then=["6.45", "7.45", "8.45", "9.45", "10.45"], far_last="11.15"),
        sunday=dict(hook_from="9.00 AM", hook_until="6.00 PM", far_from="9.15 AM", far_until="6.15 PM", hourly=True),
        boat_overnight_at="the Hook (Monday to Saturday: in at 11.30 PM, out at 6.30 AM; Sunday: in at 6.30 PM, out at 9.00 AM)",
        fares=dict(single_p=60, return_pounds=1.00, cycle_p=30, oap="half fare"),
        note="Last crossing: the Hook at 11.00 PM, matching the street's own line 'Last crossing's at eleven' (game-design/tier2-batch-1.json line 2893); the far side's last, 11.15 PM, brings the one vessel home.")


def ferry_timetable():
    it = new_item("F01", "4.2", "harbour_and_ferry", "Meridian Ferry winter timetable (A2 sheet for the ramp board)", 420, 594, stock="white_poster", process="litho_2col", fmt="A2", margin=12)
    BB = "paint:enamel_blue"
    S(it, "head_band", "rect", box=[0, 490, 420, 594], fill="enamel_blue", fill_kind="paint")
    T(it, "name", "MERIDIAN FERRY", ALF, 400, capfit(ALF, 400, "MERIDIAN FERRY", 384), 536, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.02, role="name")
    T(it, "season", "WINTER SERVICE", OSW, 700, 24, 504, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.14, role="line")
    T(it, "from", "FROM MONDAY 1 OCTOBER", OSW, 600, 17, 458, 210, "centre", ink="blue", trk=0.08, role="line")
    CX = (110, 310)
    S(it, "col_rule", "rule", box=[208.5, 130, 211.5, 440], fill="blue", fill_kind="ink")
    for col, (hdr, x) in enumerate((("FROM THE HOOK", CX[0]), ("FROM THE FAR SIDE", CX[1]))):
        T(it, "h%d" % col, hdr, OSW, 700, 15, 425, x, "centre", ink="black", trk=0.06, role="line")
    T(it, "ms", "MONDAY TO SATURDAY", OSW, 700, 13, 398, 210, "centre", ink="blue", trk=0.08, role="line")
    hook = ["6.30  7.00  7.30", "and every half hour", "until 5.30 PM", "then 6.30  7.30  8.30", "9.30  10.30", "LAST CROSSING 11.00"]
    far = ["6.45  7.15  7.45", "and every half hour", "until 5.45 PM", "then 6.45  7.45  8.45", "9.45  10.45", "LAST CROSSING 11.15"]
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
    it["variants"] = dict(n=2, vary=["PASTED over the summer sheet F02 (offset +14 mm right, -16 mm down) on the ramp board FC1 in both", "age class B and C; the C one has two drawing-pin holes and a rain stain from the top"])
    it["event"] = dict(date="MONDAY 1 OCTOBER", d=1, m=10)
    return meta(it, "notice", "event", 1, 10, "the winter service starts")


def ferry_summer():
    it = new_item("F02", "4.2", "harbour_and_ferry", "Meridian Ferry summer timetable (older sheet under F01)", 420, 594, stock="white_poster", process="litho_2col", fmt="A2", margin=12)
    BB = "paint:enamel_blue"
    S(it, "head_band", "rect", box=[0, 490, 420, 594], fill="enamel_blue", fill_kind="paint")
    T(it, "name", "MERIDIAN FERRY", ALF, 400, capfit(ALF, 400, "MERIDIAN FERRY", 384), 536, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.02, role="name")
    T(it, "season", "SUMMER SERVICE", OSW, 700, 24, 504, 210, "centre", ink_paint="enamel_white", on=BB, trk=0.14, role="line")
    T(it, "dates", "14 MAY TO 30 SEPTEMBER", OSW, 600, 17, 458, 210, "centre", ink="blue", trk=0.08, role="line")
    for bb in it["blocks"]:
        bb["ghost"] = True
        bb["glyph_check"] = False
        bb["note"] = "Mostly covered by F01 (offset +14 mm right, -16 mm down): at most the top strip of the blue band and a torn window show. Any word that shows is one of these three."
    S(it, "col_rule", "rule", box=[208.5, 130, 211.5, 440], fill="blue", fill_kind="ink")
    it["notes"].append("The older sheet carries the same table in other numbers. Nothing of it is legible: it is covered. Only the three ghost words may show, and only through a tear.")
    it["variants"] = dict(n=1, vary=["age class D: brown paste halo, loose at the left edge"])
    return meta(it, "notice")


def harbour_head(it):
    T(it, "head", "MERIDIAN HARBOUR BOARD", OST, 700, capfit(OST, 700, "MERIDIAN HARBOUR BOARD", 176, 0.06), 274, 105, "centre", ink="typed", role="name", trk=0.06)
    S(it, "rule_a", "rule", box=[20, 268, 190, 269.2], fill="typed", fill_kind="ink")


def harbour_notice_berths():
    it = new_item("H03", "4.2", "harbour_and_ferry", "Harbour Board notice: berths closed (typed A4)", 210, 297, stock="white_bond", process="typed_carbon", fmt="A4", margin=14)
    harbour_head(it)
    T(it, "kind", "NOTICE TO MARINERS", CPB, 700, 3.6, 255, 105, "centre", ink="typed", role="line", tech="typed twice for bold")
    lines = ["Berths 3 and 4 on the Hook quay will be closed to all", "shipping from Monday 5 November until further notice,", "for repairs to the quay wall.", "",
             "Masters should apply to the Harbour Master's office", "for other berths.", "", "By order of the Board.", "", "26 October 1990"]
    typed(it, "t", lines, 24, 238, pitch=8.466)
    it["variants"] = dict(n=2, vary=["pinned in the case: four drawing pins; a tan tape tab; one curling top corner (held: the case HC1 is not built until the dock office is)"])
    it["event"] = dict(date="26 OCTOBER 1990", d=26, m=10)
    return meta(it, "notice", "notice", 26, 10, "dated 26 October")


# Heights of the day's higher high water, Thursday 1 to Wednesday 7 November 1990: the full moon of 2 to 3 November puts the springs' peak on Sunday 4 November
# (TARGET-REVIEW note). The day's other high water is 0.1 m lower. Judgement: invented, in the right shape.
TIDE_DAY_M = [4.4, 4.6, 4.7, 4.8, 4.7, 4.5, 4.2]


def tide_table():
    """Seven days of invented high waters: successive highs 12 h 25 min apart (a semi-diurnal tide), the heights peaking on Sunday 4 November."""
    t0 = datetime.datetime(1990, 11, 1, 5, 42)
    rows = []
    for k in range(14):
        t = t0 + datetime.timedelta(minutes=745 * k)
        day = (t.date() - datetime.date(1990, 11, 1)).days
        base = TIDE_DAY_M[min(day, 6)]
        rows.append((t, round(base if t.hour < 12 else base - 0.1, 1)))
    return rows


def harbour_notice_tides():
    it = new_item("H04", "4.2", "harbour_and_ferry", "Harbour Board notice: tide table (typed A4)", 210, 297, stock="white_bond", process="typed_carbon", fmt="A4", margin=14)
    harbour_head(it)
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
    it["variants"] = dict(n=1, vary=["pinned in the case, a corner curling (held: the case HC1 is not built until the dock office is)"])
    return meta(it, "notice")


def harbour_notice_vacancy():
    it = new_item("H05", "4.2", "harbour_and_ferry", "Harbour Board notice: vacancy (typed A4)", 210, 297, stock="pale_yellow", process="typed_carbon", fmt="A4", margin=14)
    harbour_head(it)
    T(it, "kind", "VACANCY", CPB, 700, 9, 244, 105, "centre", ink="typed", role="line")
    T(it, "job", "QUAY LABOURER", CPB, 700, 5.4, 224, 105, "centre", ink="typed", role="line")
    lines = ["Applications in writing, giving age and experience,", "to the Secretary, Meridian Harbour Board,", "to arrive by Friday 16 November.", "", "Wages by agreement."]
    typed(it, "t", lines, 24, 202, pitch=8.466)
    it["variants"] = dict(n=1, vary=["pinned in the case (held: the case HC1 is not built until the dock office is)"])
    return meta(it, "notice")


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
    it["variants"] = dict(n=2, vary=["photocopy: a grey edge band 3 to 6 mm at the left, toner speckle", "taped inside a window with four tabs of yellowed tape (the empty unit's glass, SF2: C01a), or in a polythene sleeve cable-tied to a lamp column", SKEW_NOTE + " (0.2 to 1.5 degrees)"])
    it["sample_slot"] = suffix
    it["bottom_y"] = y
    return meta(it, "notice", "notice", d, m, "the night of the offence")


def police_notices():
    return [police_notice(k, *v) for k, v in POLICE_ROWS.items()]


def planning_notice():
    it = new_item("C02", "4.2", "council_police", "Planning application notice (A4 in a sleeve)", 210, 297, stock="white_bond", process="photocopy_a4", fmt="A4", margin=14)
    T(it, "head", "PLANNING APPLICATION", ARC, 900, capfit(ARC, 900, "PLANNING APPLICATION", 180), 270, 105, "centre", ink="toner", role="name")
    S(it, "rule_a", "rule", box=[16, 262, 194, 264], fill="toner", fill_kind="ink")
    T(it, "kind", "NOTICE", ARC, 700, 6.5, 250, 105, "centre", ink="toner", role="line", trk=0.3)
    body = [("PROPOSAL", 700), ("Change of use of the ground floor, 7 Quay Street,", 400), ("from shop to estate agent's office.", 400), ("", 0),
            ("COMMENTS", 700), ("Anyone wishing to comment may write to the Planning", 400), ("Officer by Friday 9 November.", 400), ("", 0),
            ("THE PLANS", 700), ("may be seen at the Planning Department, Monday to", 400), ("Friday, 9 a.m. to 4.30 p.m.", 400)]
    y = 232
    for i, (t, w) in enumerate(body):
        if t:
            T(it, "b%d" % (i + 1), t, OSTR if w == 400 else ARC, 400 if w == 400 else 800, 3.6 if w == 400 else 3.4, y, 22, "left", ink="toner", role="body", tech="typeset, photocopied")
        y -= 8.2
    it["event"] = dict(date="FRIDAY 9 NOVEMBER", d=9, m=11)
    it["variants"] = dict(n=2, vary=["in a clear polythene sleeve, cable-tied to a lamp column or taped inside the empty unit's glass (SF2, number 7); water beads in the lower sleeve; a yellowing", SKEW_NOTE])
    it["notes"].append("The empty unit is number 7 (the fascia target: street_number 7); the first try's '21 to 27 Quay Street' used street x in metres as house numbers.")
    return meta(it, "notice", "event", 9, 11, "the comment deadline")


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
    T(it, "sorry", "We apologise for any inconvenience.", OSTR, 400, 6.0, 40, 148.5, "centre", ink="toner", role="body")
    it["event"] = dict(date=dated(4, 11), d=4, m=11)
    it["variants"] = dict(n=2, vary=["cable-tied in a sleeve to a lamp column at 1.6 to 2.0 m, facing the street", "the sleeve fogged inside, the notice yellowed, a cable tie tail left long"])
    return meta(it, "notice", "event", 4, 11, "the closure")
# --------------------------------------------------------------------------------------------
# 6. Shop-window cards and the newsagent's board (unit 4.2). Hand lettering is Patrick Hand (production/fonts).
#    EVERY hand-lettered card carries one mirror cue that matches its fixing and sits on ONE half only (TARGET-REVIEW fault 9):
#    a taped or stuck card: one tab of yellowed tape across its top-LEFT corner; a string-hung card: the knot and sucker at its top-LEFT.
# --------------------------------------------------------------------------------------------
HAND_FELT = dict(stroke_mm=2.6, baseline_sd_mm=1.2, rotation_sd_deg=1.0, size_sd=0.04, word_gap_sd=0.12, density_sd=0.08, embolden_mm=0.30,
                 note="felt-tip marker: a fat even line, ends a shade darker where the nib rested, a little bleed into the card")
HAND_FELT_FINE = dict(stroke_mm=1.4, baseline_sd_mm=0.8, rotation_sd_deg=0.8, size_sd=0.04, word_gap_sd=0.10, density_sd=0.08, embolden_mm=0.15,
                      note="fine felt tip for the small lines")
HAND_BALL = dict(stroke_mm=0.55, baseline_sd_mm=0.6, rotation_sd_deg=1.4, size_sd=0.06, word_gap_sd=0.15, density_sd=0.12, embolden_mm=0.05,
                 note="ballpoint: a thin line, pressure shows (lighter on joins), a blot at some stroke ends")

TAPE = dict(kind="tape", what="one tab of yellowed adhesive tape across the card's top-LEFT corner only", cue="top-left")
STRING = dict(kind="string", what="a string loop 220 mm long from a knot and a rubber sucker, at the card's top-LEFT only", cue="top-left")


def fixing_for(kind):
    return dict(TAPE if kind == "tape" else STRING)


def card_closed_lunch():
    it = new_item("K01", "4.2", "window_cards", "Closed for lunch card (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(it, "l1", "CLOSED FOR LUNCH", PAT, 400, capfit(PAT, 400, "CLOSED FOR LUNCH", 186), 92, 105, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(it, "l2", "BACK AT 2 O’CLOCK", PAT, 400, 14, 52, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    it["variants"] = dict(n=3, vary=["the hour line is the one approved string 'BACK AT 2 O’CLOCK' (BACK AT 1.30 and 2.30 are not separate cards)", "hung on a string with a rubber sucker; slightly tilted (the placement's rot_deg); age class A to C"])
    it["fixing"] = fixing_for("string")
    return meta(it, "card")


def card_back_at():
    """Unplaced (TARGET-REVIEW fault 10): the newsagent never closes at midday (hook-cast 6 to 17.30) and Hal's shop is not on the built street."""
    it = new_item("K02", "4.2", "window_cards", "BACK AT clock card (printed; not placed)", 130, 170, stock="buff_card", process="litho_2col", fmt=None, margin=8, kind="card")
    T(it, "l1", "BACK AT", ALF, 400, capfit(ALF, 400, "BACK AT", 108), 140, 65, "centre", ink="red", role="line")
    cx, cy, R = 65.0, 57.0, 45.0
    S(it, "clock", "roundel", box=[cx - R, cy - R, cx + R, cy + R], fill="white", note="a printed clock face: white disc 90 mm across, black rim 2 mm")
    ticks = []
    for k in range(12):
        a = math.radians(90 - 30 * k)
        r0, r1 = 35.0, 43.0
        ticks.append(dict(p0=[round(cx + r0 * math.cos(a), 2), round(cy + r0 * math.sin(a), 2)], p1=[round(cx + r1 * math.cos(a), 2), round(cy + r1 * math.sin(a), 2)]))
    S(it, "ticks", "ticks", fill="black", fill_kind="ink", segments_mm=ticks, width_mm=2.0, note="twelve ticks 2 x 8 mm, from 35 to 43 mm out from the centre (no numerals: the hands would cover the 12)")
    S(it, "hand_hour", "hand", centre_mm=[cx, cy], length_mm=30.0, width_mm=5.0, pointing="by variant", fill="buff_card", note="hour hand, buff card, 30 x 5 mm, rounded end, set by the variant (12 or 2 o'clock)")
    S(it, "hand_min", "hand", centre_mm=[cx, cy], length_mm=40.0, width_mm=4.0, pointing="12", fill="buff_card", note="minute hand, buff card, 40 x 4 mm, pointing at 12")
    S(it, "fastener", "roundel", box=[cx - 3.0, cy - 3.0, cx + 3.0, cy + 3.0], fill="brass", fill_kind="paint", note="a brass paper-fastener, 6 mm across, through both hands and the card")
    it["variants"] = dict(n=2, vary=["hands at 12 and at 2", "hung on a string with a rubber sucker (NOT PLACED: hook-cast gives the newsagent no midday break, and Hal's shop is not on the built street)"])
    it["fixing"] = fixing_for("string")
    it["notes"].append("Not placed on Quay Street (TARGET-REVIEW fault 10).")
    return meta(it, "card")


def card_open_closed():
    its = []
    for face, text, paint, id_ in (("OPEN", "OPEN", "agent_green", "K03a"), ("CLOSED", "CLOSED", "agent_red", "K03b")):
        it = new_item(id_, "4.2", "window_cards", "OPEN / CLOSED hanging sign, face %s" % face, 200, 110, stock="white_card", process="plastic_print", fmt=None, margin=8, kind="card")
        S(it, "face", "rect", box=[0, 0, 200, 110], fill=paint, fill_kind="paint", corner_radius_mm=8.0,
          note="a plastic card, corners rounded 8 mm; a hole 5 mm across at the top centre, 8 mm down; a bead chain of 2.5 mm beads on a loop 60 mm long through the hole")
        S(it, "hole", "roundel", box=[97.5, 100.5, 102.5, 105.5], fill="paper", fill_kind="stock", note="the hanging hole, 5 mm across, centre 8 mm below the top edge")
        T(it, "word", text, ARC, 800, capfit(ARC, 800, text, 168), 40, 100, "centre", ink_paint="agent_white", on="paint:" + paint, trk=0.06, role="line")
        it["variants"] = dict(n=1, vary=["one face outward at a time, from the shop's hours (hook-cast.json); the chain shows"])
        its.append(meta(it, "card"))
    return its


def card_no_dogs():
    it = new_item("K04", "4.2", "window_cards", "NO DOGS sticker, 150 x 105", 150, 105, stock="white_poster", process="sticker_print", fmt=None, margin=6, kind="sticker")
    cx, cy, R, ring = 43.0, 52.0, 35.0, 7.0
    S(it, "roundel", "ring", centre_mm=[cx, cy], r_inner_mm=R - ring, r_outer_mm=R, fill="red", fill_kind="ink", note="a red ring 7 mm wide, 70 mm across; no dog silhouette (TARGET-REVIEW fault 11: the L3 sheet shows a bare ring)")
    a = math.radians(45)
    r_in = R - ring
    p0 = (cx - r_in * math.cos(a), cy + r_in * math.sin(a))       # inside top-left
    p1 = (cx + r_in * math.cos(a), cy - r_in * math.sin(a))       # inside bottom-right
    hw = 3.5                                                       # half of the 7 mm bar
    nx, ny = math.sin(a) * hw, math.cos(a) * hw
    pts = [[round(p0[0] - nx, 2), round(p0[1] - ny, 2)], [round(p0[0] + nx, 2), round(p0[1] + ny, 2)], [round(p1[0] + nx, 2), round(p1[1] + ny, 2)], [round(p1[0] - nx, 2), round(p1[1] - ny, 2)]]
    S(it, "bar", "poly", pts=pts, fill="red", fill_kind="ink", note="a bar 7 mm wide at 45 degrees from the ring's inside top-left to its inside bottom-right, same red")
    T(it, "l1", "NO", ARC, 900, 12, 58, 112, "centre", ink="black", role="line")
    T(it, "l2", "DOGS", ARC, 900, 12, 36, 112, "centre", ink="black", role="line")
    it["variants"] = dict(n=2, vary=["inside the glass of a shop door at 1.1 to 1.4 m, or outside on the door; one half peeled at a corner"])
    return meta(it, "sticker")


def card_shut_door():
    it = new_item("K05", "4.2", "window_cards", "PLEASE SHUT THE DOOR (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(it, "l1", "PLEASE SHUT", PAT, 400, 22, 96, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    T(it, "l2", "THE DOOR", PAT, 400, 22, 56, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    it["variants"] = dict(n=2, vary=["taped to a door's glass, bottom at 1.42 m (centre 1.494 m: just above the shop's vinyl trade lettering, which tops out at 1.385 m +- 0.03 on the fascia target); one with the second line underlined in red felt"])
    it["fixing"] = fixing_for("tape")
    return meta(it, "card")


def cards_launderette():
    a = new_item("K06a", "4.2", "window_cards", "Launderette: LAST WASH (felt pen)", 210, 148, stock="white_card", process="felt_pen", fmt="A5L", margin=8, kind="card")
    T(a, "l1", "LAST WASH", PAT, 400, 22, 92, 105, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(a, "l2", "4.30 PM", PAT, 400, 26, 50, 105, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    a["variants"] = dict(n=2, vary=["the hour comes from the shop's closing time in hook-cast.json (laundry 8 to 5.30): LAST WASH is an hour before", "hung inside the glass on a string and a rubber sucker"])
    a["fixing"] = fixing_for("string")
    meta(a, "card")
    b = new_item("K06b", "4.2", "window_cards", "Launderette: PLEASE DO NOT OVERLOAD (printed sticker)", 210, 148, stock="white_poster", process="sticker_print", fmt="A5L", margin=8, kind="sticker")
    stack(b, "L", [L("PLEASE DO NOT", ARC, 800, 15, gap=8, ink="black", trk=0.04), L("OVERLOAD", ARC, 900, fitw=186, gap=8, ink="red"), L("THE MACHINES", ARC, 800, 15, gap=8, ink="black", trk=0.04)], 105, 134)
    b["variants"] = dict(n=2, vary=["stuck on the glass above a machine door"])
    meta(b, "sticker")
    c = new_item("K06c", "4.2", "window_cards", "OUT OF ORDER (felt pen)", 148, 105, stock="white_card", process="felt_pen", fmt="A6L", margin=6, kind="card")
    T(c, "l1", "OUT OF", PAT, 400, 14, 66, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(c, "l2", "ORDER", PAT, 400, 14, 38, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    c["variants"] = dict(n=3, vary=["taped on a machine door or the glass; the tab lifting at one end"])
    c["fixing"] = fixing_for("tape")
    meta(c, "card")
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
        S(it, "star", "star", pts=star_pts(85, 85, 84, 62, 14), fill="paper", note="the card is cut to a 14-point burst (outer radius 84, inner 62); the stock colour is the star; outside it the card is transparent")
        n = len(lines)
        y0 = 85 + (n * 21) / 2.0 - 12
        for i, (t, cap, ink) in enumerate(lines):
            T(it, "l%d" % (i + 1), t, PAT, 400, cap, y0 - i * 21 - cap / 2.0, 85, "centre", ink=ink, tech="felt pen", hand=HAND_FELT, role="line")
        it["variants"] = dict(n=2, vary=["taped inside the grocer's glass at 1.2 to 1.9 m; the fluorescent stock fades within weeks"])
        it["fixing"] = fixing_for("tape")
        out.append(meta(it, "card"))
    return out


def card_no_credit():
    it = new_item("K08", "4.2", "window_cards", "SORRY NO CREDIT GIVEN (printed card)", 210, 148, stock="white_card", process="letterpress_2col", fmt="A5L", margin=8, kind="card")
    stack(it, "L", [L("SORRY", ARC, 900, 20, gap=10, ink="red"), L("NO CREDIT GIVEN", ARC, 900, fitw=186, gap=8, ink="black", trk=0.04)], 105, 128)
    it["variants"] = dict(n=2, vary=["on a shop counter's glass screen or the door"])
    return meta(it, "card")


def cards_fish():
    # smoked haddock is dearer than fresh (TARGET-REVIEW note); cockles are sold by the tub (the unit the trade used, 'pint', is a banned word in this project)
    items = [("K09a", "COD FILLET", "£2.70 lb"), ("K09b", "HADDOCK", "£2.50 lb"), ("K09c", "PLAICE", "£2.30 lb"), ("K09d", "KIPPERS", "95p PAIR"),
             ("K09e", "SMOKED HADDOCK", "£2.90 lb"), ("K09f", "COCKLES", "45p TUB")]
    out = []
    for id_, a, b in items:
        it = new_item(id_, "4.2", "window_cards", "Fish price ticket: %s" % a, 105, 74, stock="white_card", process="felt_pen", fmt=None, margin=6, kind="card")
        T(it, "l1", a, PAT, 400, min(13, capfit(PAT, 400, a, 90)), 46, 52.5, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT_FINE, role="line")
        T(it, "l2", b, PAT, 400, 15, 16, 52.5, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
        it["variants"] = dict(n=2, vary=["taped inside the glass at the slab's height, one tab at the top-left; a wet corner"])
        it["fixing"] = fixing_for("tape")
        it["notes"].append("Price: ONS average cod fillet 1990 574 p/kg, about 2.60 a lb, January 2.42, December 2.85 (production/research/shop-window-interiors/FISHMONGER-2026-10-03.md, read in this repository); the other prices are Judgement (smoked haddock is dearer than fresh).")
        out.append(meta(it, "card"))
    return out


SMALL_ADS = [
    ("SA01", "index_white", (127, 76), [("ROOM TO LET", "head"), ("Clean, quiet, gas fire.", ""), ("£28 per week. No pets.", ""), ("Ring 960 471 after 5.", "")]),
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
        it["variants"] = dict(n=1, vary=["taped on the newsagent's board: one tab of yellowed tape across the top-LEFT corner; slight tilt (the card board's rot_deg)"])
        it["fixing"] = fixing_for("tape")
        out.append(meta(it, "card"))
    tariff = new_item("SA15", "4.2", "newsagent_board", "Newsagent: ADVERTISE HERE card", 148, 105, stock="white_card", process="felt_pen", fmt="A6L", margin=6, kind="card")
    T(tariff, "l1", "ADVERTISE HERE", PAT, 400, 12, 80, 74, "centre", ink="felt_red", tech="felt pen", hand=HAND_FELT, role="line")
    T(tariff, "l2", "20p PER WEEK", PAT, 400, 14, 56, 74, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT, role="line")
    T(tariff, "l3", "PAY AT THE COUNTER", PAT, 400, 8, 34, 74, "centre", ink="felt_black", tech="felt pen", hand=HAND_FELT_FINE, role="line")
    tariff["variants"] = dict(n=1, vary=["top of the board, taped by one tab at the top-left"])
    tariff["fixing"] = fixing_for("tape")
    tariff["notes"].append("20p a week is Judgement; the one search lead for it (a forum comment) is undated and not used.")
    out.append(meta(tariff, "card"))
    return out
# --------------------------------------------------------------------------------------------
# 7. Boards and plates (units 4.2 enamel, 4.3 letting boards, 4.4 street name plates).
# --------------------------------------------------------------------------------------------
ENAMEL_EDGE_R = 6.0     # mm: the rolled edge of a vitreous enamel sign is a roll of 6 mm radius (TARGET-REVIEW fault 11; Judgement)


def enamel_no_admittance():
    it = new_item("H01", "4.2", "harbour_and_ferry", "Harbour Board enamel sign: NO ADMITTANCE", 600, 450, stock=None, process="enamel", ppm=1, margin=40, fmt=None, kind="plate")
    it["stock"] = "white_poster"      # unused: plate colours are paints
    B = "paint:enamel_blue"
    S(it, "face", "rect", box=[0, 0, 600, 450], fill="enamel_blue", fill_kind="paint", corner_radius_mm=25.0, edge_roll_radius_mm=ENAMEL_EDGE_R,
      note="vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge of 6 mm radius")
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
    return meta(it, "plate")


def enamel_danger_water():
    it = new_item("H02", "4.2", "harbour_and_ferry", "Harbour Board enamel sign: DANGER DEEP WATER", 600, 450, stock=None, process="enamel", ppm=1, margin=40, fmt=None, kind="plate")
    it["stock"] = "white_poster"
    S(it, "face", "rect", box=[0, 0, 600, 450], fill="enamel_white", fill_kind="paint", corner_radius_mm=25.0, edge_roll_radius_mm=ENAMEL_EDGE_R,
      note="vitreous enamel on 1.6 mm pressed steel; corners rounded 25 mm; rolled edge of 6 mm radius")
    S(it, "danger_band", "rect", box=[0, 300, 600, 450], fill="enamel_red", fill_kind="paint")
    S(it, "border", "frame", box=[14, 14, 586, 436], fill="enamel_blue", fill_kind="paint", width_mm=10)
    T(it, "danger", "DANGER", ARC, 900, capfit(ARC, 900, "DANGER", 450, 0.1), 332, 300, "centre", ink_paint="enamel_white", on="paint:enamel_red", trk=0.1, role="title")
    T(it, "deep", "DEEP WATER", ARC, 900, capfit(ARC, 900, "DEEP WATER", 470, 0.04), 220, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.04, role="line")
    T(it, "swim", "NO SWIMMING", ARC, 800, capfit(ARC, 800, "NO SWIMMING", 420, 0.04), 130, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.04, role="line")
    T(it, "board", "MERIDIAN HARBOUR BOARD", ARC, 800, capfit(ARC, 800, "MERIDIAN HARBOUR BOARD", 400, 0.06), 56, 300, "centre", ink_paint="enamel_blue", on="paint:enamel_white", trk=0.06, role="name")
    it["fixing"] = dict(kind="four holes 10 mm across at 36 mm in from each corner; bolts to a quay-edge post or the railing", holes_mm=[[36, 36], [564, 36], [36, 414], [564, 414]])
    it["wear"] = dict(chips="as H01, plus salt bloom (white fur) along the lower edge and rust bleeding from the bolt holes in long tears, 150 to 400 mm")
    it["variants"] = dict(n=2, vary=["age class B, D"])
    return meta(it, "plate")


AGENT = "ARMITAGE & STOBBS"
AGENT_LINE = "CHARTERED SURVEYORS · ESTATE AGENTS"
PHONE = "960 335"


def letting_board(id_, title, w, h, named, name_cap, to_cap, sub, sub_cap, band_h, enq_cap, mount, variants):
    it = new_item(id_, "4.3", "letting_boards", title, w, h, stock=None, process="agent_board", ppm=1, margin=10, fmt=None, kind="board")
    it["stock"] = "white_poster"
    W = "paint:agent_white"
    S(it, "face", "rect", box=[0, 0, w, h], fill="agent_white", fill_kind="paint", corner_radius_mm=4.0, thickness_mm=18.0,
      note="18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end")
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
    return meta(it, "board")


def letting_board_fascia(mount):
    """L02: the fascia target's board EXACTLY (TARGET-REVIEW fault 5): 900 x 450, white face, TO LET alone in Libre Franklin 800, cap 130, vinyl red, no agent, no number."""
    it = new_item("L02", "4.3", "letting_boards", "Letting board, empty unit (the fascia target's board: 900 x 450, TO LET)", 900, 450, stock=None, process="agent_board", ppm=1, margin=10, fmt=None, kind="board")
    it["stock"] = "white_poster"
    S(it, "face", "rect", box=[0, 0, 900, 450], fill="agent_white", fill_kind="paint", corner_radius_mm=4.0, thickness_mm=18.0,
      note="18 mm exterior plywood painted white gloss, corners rounded 4 mm, the cut edges painted, a 25 x 18 mm batten on the back at each end; no border, no band (the fascia target's board has none)")
    T(it, "tolet", "TO LET", FRK, 800, 130, 160, 450, "centre", ink_paint="vinyl_red", on="paint:agent_white", trk=0.0, role="title")
    it["mount"] = mount
    it["fascia_target"] = dict(id="small_panels.letting_board", size_mm=[900, 450], text="TO LET", font="libre-franklin", weight=800, cap_mm=130, colour="vinyl_red", agent=None, number=None)
    it["variants"] = dict(n=3, vary=["askew -2, 0, +2 degrees (the placement's rot_deg)", "age class B, C, D (the D board has the white yellowed and the red faded to rust-pink)", "four screws, a rust run under each lower one (fascia target)"])
    return meta(it, "board")


def letting_boards():
    mount_shop = dict(surface="the empty unit's fascia (bay 3, east, street x 21 to 27; number 7)", centre_street_x_m=24.0, z_bottom_m=2.90, z_top_m=3.35,
                      screws="four 8 mm dome-head coach screws at 40 mm in from each corner; a rust run 40 to 140 mm under each lower screw",
                      askew_deg="-2 to +2", proud_of_fascia_m=0.043, note="the fascia is 0.55 m tall (2.85 to 3.40): the board leaves 50 mm above and below; its centre is the fascia target's own letting-board centre (board x 2705, y 275)")
    b = letting_board_fascia(mount_shop)
    a = letting_board("L01", "Letting board, shop, with agent (1200 x 450; NOT the fascia target's board; named agent, held)", 1200, 450, True, 52, 150, "SHOP AND PREMISES · APPROX. 520 SQ. FT.", 24, 118, 46, mount_shop,
                      dict(n=3, vary=["askew -2, 0, +2 degrees", "age class B, C, D (the D board has the white yellowed and the red faded to rust-pink)", "NOT used by default: it disagrees with the fascia target (900 x 450, TO LET only); using it needs the fascia target changed in the same batch with one DECISIONS line"]))
    mount_flat = dict(surface="first-floor brick above the empty unit's cornice, between the two upper windows", centre_street_x_m=24.0, z_bottom_m=3.70, z_top_m=4.10,
                      screws="four 6 mm screws and plugs", askew_deg="-1.5 to +1.5", note="the cornice top is 3.55 m, the upper sill about 4.3 m (facade: head 0.4 below the ceiling, window 1.5 high): 0.75 m of plain brick; Rita's hanging sign is at street x 20.825 and the laundry's at 27.175, both outside bay 3")
    c = letting_board("L03", "Letting board, flat, with agent (600 x 400; named agent, held)", 600, 400, True, 30, 106, "SELF-CONTAINED FLAT", 24, 84, 34, mount_flat,
                      dict(n=2, vary=["age class C, D", "the agent's board has been up a long time: grime streaks from the top edge"]))
    c2 = letting_board("L03n", "Letting board, flat, no agent (600 x 400)", 600, 400, False, 0, 104, "SELF-CONTAINED FLAT", 26, 0, 32, mount_flat,
                       dict(n=2, vary=["age class C, D", "grime streaks from the top edge"]))
    mount_house = dict(surface="the west terrace (bay 2 of the plain block, street x 15 to 21): the brick pier between the two windows", centre_street_x_m=16.8, z_bottom_m=2.15, z_top_m=2.55,
                       screws="four 6 mm screws and plugs", askew_deg="-1.5 to +1.5", note="pier 16.35 to 17.25 (window 15.9 and 17.7, 0.85 wide, from the plain row's bay layout, mirrored in bay 2); the board is 0.6 wide")
    d = letting_board("L04", "Letting board, house, no agent (600 x 400)", 600, 400, False, 0, 104, "TWO BEDROOMS", 30, 0, 32, mount_house,
                      dict(n=2, vary=["age class B, D"]))
    return [a, b, c, c2, d]


# ---- street name plates ----------------------------------------------------------------
PLATE_CAP = 90.0       # Judgement: 90 mm capitals, the South Kesteven and Charnwood specs' figure (Lead, search summary) and the project's own plate
PLATE_MIN_DEPTH = 200  # mm: the street-clutter note's 20 to 25 cm (TARGET-REVIEW fault 13)
RELIEF = dict(raised_mm=None, draft_deg=10.0, top_radius_mm=0.8, note="raised letters and border: 10 degrees of draft each side and a 0.8 mm radius on the top edge (Judgement)")


def stroke_stats(name, cap_mm=PLATE_CAP):
    """Thinnest and thickest strokes of the name set in Marcellus SC at the plate's cap, from the distance transform of the rendered glyphs (Derived)."""
    ppm = 2.0
    bb, px = measure(MAR, 400, name, cap_mm, 0.04)
    r = cap_ratio(MAR, 400)
    f = font(MAR, 400, px * ppm)
    pad = int(px * ppm * 0.5)
    img = Image.new("L", (int(f.getlength(name) + 2 * pad), int(px * ppm * 1.9)), 0)
    ImageDraw.Draw(img).text((pad, int(px * ppm * 1.2)), name, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
    from scipy import ndimage as ndi
    e = ndi.distance_transform_edt(a)
    ridge = (e == ndi.maximum_filter(e, size=5)) & (e >= 1.0)
    vals = e[ridge] * 2.0 / ppm
    return dict(thin_mm=round(float(np.percentile(vals, 5)), 1), median_mm=round(float(np.percentile(vals, 50)), 1), thick_mm=round(float(np.percentile(vals, 95)), 1))


def street_plate(id_, name, district, variant, material):
    """A plate whose length follows its name. variant: 'n' name only (the DEFAULT and the placed one), 'd' name and a district line (a variant until a dated photograph shows one)."""
    bb, px = measure(MAR, 400, name, PLATE_CAP, 0.04)
    ink_w = bb[2] - bb[0]
    EDGE, BORDER = 6, 12
    side_margin = EDGE + BORDER + 44
    w = int(math.ceil((ink_w + 2 * side_margin) / 10.0) * 10)
    desc = max(24, int(math.ceil(-bb[1] + 6)))   # room under the baseline for a Q's tail (it dips 0.4 of the cap) and the border
    have_dist = variant == "d"
    dist_cap = 30.0
    h_min = EDGE + BORDER + 16 + (dist_cap + 22 if have_dist else 0) + PLATE_CAP + desc + BORDER + EDGE
    h = max(PLATE_MIN_DEPTH, int(math.ceil(h_min / 5.0) * 5))
    slack = h - h_min
    it = new_item(id_, "4.4", "street_name_plates", "Street name plate: %s (%s)" % (name, "name only: the default" if variant == "n" else "name and district line: a variant"),
                  w, h, stock=None, process=material, ppm=1, margin=EDGE, fmt=None, kind="plate")
    it["stock"] = "white_poster"
    P = "paint:plate_white"
    S(it, "face", "rect", box=[0, 0, w, h], fill="plate_white", fill_kind="paint", corner_radius_mm=6.0, note="corners rounded 6 mm")
    S(it, "border", "frame", box=[EDGE, EDGE, w - EDGE, h - EDGE], fill="plate_black", fill_kind="paint", width_mm=BORDER, note="the border band 12 mm wide, 6 mm in from the edge (the South Kesteven figure, Lead)")
    base = EDGE + BORDER + desc - 2 + slack / 2.0
    T(it, "name", name, MAR, 400, PLATE_CAP, round(base, 1), w / 2.0, "centre", ink_paint="plate_black", on=P, trk=0.04, role="name",
      note="Marcellus SC, ruled 30 Sep for the street name plates (the earlier note's Kindersley MOT serif has no allowed free version); tracking 0.04 em")
    if have_dist:
        T(it, "district", district, MAR, 400, dist_cap, round(base + PLATE_CAP + 22, 1), w / 2.0, "centre", ink_paint="plate_black", on=P, trk=0.18, role="line")
    it["fixing"] = dict(kind="four fixings at the corners, 30 mm in", holes_mm=[[30, 30], [w - 30, 30], [30, h - 30], [w - 30, h - 30]],
                        head="10 mm dome-head galvanised screw into fibre plugs (brick); the cast plate has the holes cast in 12 mm across")
    it["variants"] = dict(n=3, vary=["age class C, D, D", "paint flake share 0.03 to 0.06 at the letter edges", "rust runs under the screws: 0 to 4 of 4", "a sticker or its ghost (P05 or P06) in one, never over the name"])
    st = stroke_stats(name)
    relief = dict(RELIEF)
    if material == "cast_aluminium_raised":
        relief["raised_mm"] = 3.0
        relief["edge"] = "a plain cast edge 6 mm thick with a 2 mm arris radius; face 6 mm thick; letters and border raised 3 mm"
    elif material == "pressed_aluminium_enamel":
        relief["raised_mm"] = 1.5
        relief["edge"] = "rolled edge, radius 3 mm; 2 mm sheet; letters and border raised 1.5 mm by the press"
    else:
        relief["raised_mm"] = 0.0
        relief["edge"] = "rolled edge, radius %g mm; flat vitreous enamel, no relief" % ENAMEL_EDGE_R
        relief["draft_deg"] = None
        relief["top_radius_mm"] = None
    top_w = None
    if relief["raised_mm"]:
        top_w = round(st["thin_mm"] - 2 * relief["raised_mm"] * math.tan(math.radians(relief["draft_deg"])), 2)
    it["relief"] = relief
    it["lettering_suit"] = dict(strokes_mm=st, top_width_of_thinnest_stroke_mm=top_w,
                                rule="a cast or pressed letter needs a top width of 1.5 mm or more on its thinnest stroke after the draft; thinnest = the 5th percentile of the ridge widths of the glyphs' distance transform at 2 px/mm; Marcellus SC's hairlines at 90 mm capitals are thicker than that, so the ruled letter suits every make here",
                                ok=(top_w is None or top_w >= 1.5))
    it["name_plate"] = dict(street=name, district=district, variant=variant, material=material, plate_w_mm=w, plate_h_mm=h, ink_w_mm=round(ink_w, 1), cap_mm=PLATE_CAP, min_depth_mm=PLATE_MIN_DEPTH)
    return meta(it, "plate")


PLATE_STREETS = [("QUAY STREET", "THE HOOK", "cast_aluminium_raised"), ("WEIGHHOUSE LANE", "COPPER ROW", "pressed_aluminium_enamel"), ("TANNERY ROW", "IRONSIDE", "vitreous_enamel_steel")]


def street_plates():
    out = []
    for n, (name, dist, mat) in enumerate(PLATE_STREETS, start=1):
        for v in ("n", "d"):
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
    "enamel": dict(name="vitreous enamel on pressed steel", roughness=0.12, metallic=0.0, chips="to black steel with a rust halo", edge="rolled edge of 6 mm radius", edge_roll_radius_mm=6.0, thickness_mm=1.6,
                   lead="the Harbour Board's 'blue and white enamel signage on gates, cranes and the weighbridge' (content/brands/brand-bible-v1.json)"),
    "agent_board": dict(name="painted exterior plywood, sign-written or screen-printed vinyl", roughness=0.35, metallic=0.0, edge="cut edge painted, swells and darkens at the bottom",
                        peel_fraction=[0.01, 0.03], note="gloss gone to satin outdoors in a few years"),
    "cast_aluminium_raised": dict(name="cast aluminium, letters and border raised 3 mm, painted white with black letters (by the 1950s raised plates were cast aluminium, not iron: TARGET-REVIEW fault 13)", roughness=0.5, metallic=0.5, relief_mm=3.0, draft_deg=10.0, top_radius_mm=0.8,
                                  face_thickness_mm=6.0, edge="a plain cast edge 6 mm thick, arris radius 2 mm",
                                  flake=dict(fraction=[0.03, 0.06], note="paint flakes first from the raised letter edges, showing bare grey aluminium and a thin pale oxide bloom"),
                                  lead="Hull's cast plates of the 1920s were black on white and the paint faded or flaked, needing regular repainting (search summary of a Geograph caption); a Lead only: that was iron"),
    "pressed_aluminium_enamel": dict(name="die-pressed aluminium sheet, letters and border raised 1.5 mm, stove enamelled black on white", roughness=0.3, metallic=0.6,
                                     thickness_mm=2.0, relief_mm=1.5, draft_deg=10.0, top_radius_mm=0.8, edge="rolled edge, radius 3 mm", edge_roll_radius_mm=3.0, lead="current specs: 11 SWG aluminium, die-pressed, stove-enamelled (South Kesteven, Charnwood: search summaries)"),
    "vitreous_enamel_steel": dict(name="vitreous enamel on pressed steel, rolled edge of 6 mm radius", roughness=0.12, metallic=0.0, chips="to black steel with a rust halo", edge_roll_radius_mm=6.0),
    "letterpress_1col": dict(name="one-colour letterpress from metal type (a pasted venue strip)", passes=["black"], impression_mm=[0.10, 0.18], ink_mottle=dict(amount=0.10, scale_mm=[3, 8]), baseline_error_mm=0.4, edge_rag_mm=0.2, tone="flat black on white poster paper, slightly uneven"),
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
    """HC1 and FC1. NEITHER IS PLACED on Quay Street (TARGET-REVIEW fault 10): the Harbour Board's case belongs 'by the dock office' (brand bible; hook-cast's
    harbour_office is in the docks), the ferry's board at a ramp; neither is built. FC1 is a painted timber board with no glazing (the brand bible: 'a timetable
    board at each ramp with the winter service pasted over the summer one')."""
    harbour = dict(
        id="HC1", title="Harbour Board notice case (not placed until the dock office is built)", kind="case", unit="4.2",
        outer_mm=[640, 880], depth_mm=60, frame_mm=dict(left=46, right=46, top=52, bottom=52), window_radius_mm=6,
        rail_section_mm=[46, 60], chamfer_mm=4.0, chamfer_where="the outer arris of every rail",
        glass=dict(thickness_mm=4.0, bead_mm=[10, 10], note="4 mm glass held in a 10 x 10 mm timber bead on the inside of the door's frame, putty-run on the outside"),
        colours=dict(frame="case_timber", lining="cork", glass="4 mm clear glass, a little green at the edge, dirty on the outside"),
        construction="varnished timber frame (rails 46 x 60 mm, a 4 mm chamfer on the outer arris; dark, grain showing, varnish crazed and lifting at the lower rails), mitred corners, one glazed door hinged on the left with two brass butt hinges, a brass lock and escutcheon 20 mm across on the right stile at 0.5 of the height, a cork lining 8 mm thick, a drip rail on top 14 mm proud",
        fixing="four 8 mm coach screws through the back rails at 40 mm in from the corners, on 20 mm timber battens; rust runs 40 to 180 mm below each screw",
        wear="a crack across one lower corner of the glass (30 per cent of the cases), a brown water line inside the lower glass, flies and dead leaves on the cork foot, varnish lifted at the bottom rail, one hinge screw missing",
        inside_mm=[548, 776],
        children=[dict(item="H03", x_mm=24, y_mm=470, rot_deg=0.8, pins=4), dict(item="H04", x_mm=300, y_mm=455, rot_deg=-1.2, pins=4),
                  dict(item="H05", x_mm=160, y_mm=100, rot_deg=0.5, pins=4)],
        scraps="two older yellowed sheets behind the new ones, showing 20 to 40 per cent; NO legible word (their ink is gone to brown)",
        place=None, not_placed="by the dock office (brand bible; hook-cast harbour_office): neither is built",
        photo_proportions=dict(note="the photographed case is blue steel with a 0.152 header and a 0.085 foot; the target is a 1990 timber case with 52 mm top and bottom rails (0.059 each of the height), 46 mm stiles (0.072 of the width each): the photograph's wide crest header and thick steel frame are replacement-stock features and are NOT taken (Judgement: photograph of a later object); the council crest on the photographed header is masked in the preview"))
    ferry = dict(
        id="FC1", title="Ferry timetable board at the ramp (painted timber, no glazing; not placed until the ramp is built)", kind="board", unit="4.2",
        outer_mm=[600, 800], depth_mm=22, frame_mm=dict(left=40, right=40, top=40, bottom=40), window_radius_mm=0,
        colours=dict(frame="enamel_blue", lining="white backing board", glass="none: the sheets are pasted straight on the board"),
        construction="a 22 mm exterior plywood board, 600 x 800 mm, painted Board blue (24,68,140) with a 40 mm border all round and a 520 x 720 mm white panel; NO glazing, no frame lip; the winter sheet F01 pasted over the summer sheet F02 with wallpaper paste; two 60 x 40 mm timber battens on the back",
        fixing="four 8 mm screws at the corners, 30 mm in, into plugs; a rust run under each lower screw",
        wear="paste halo round both sheets, the older sheet's edge peeling at the left and the top, rain stains from the top edge, paint chipped at the lower corners, salt bloom along the foot, rust at the lower screws",
        inside_mm=[520, 720],
        children=[dict(item="F02", x_mm=50, y_mm=82, rot_deg=0.0, pins=0, note="older sheet, 14 mm left and 16 mm higher than F01 so its edges peek out at the left and the top"),
                  dict(item="F01", x_mm=64, y_mm=66, rot_deg=0.0, pins=0)],
        place=None, not_placed="at each ramp (brand bible): the ramp is not built",
        photo_proportions=dict(note="a board, not a case: no photograph proportions apply"))
    return [harbour, ferry]


# --------------------------------------------------------------------------------------------
# 9. Where everything goes on the street. Street x is metres along Quay Street (0 south, the quay end), the same in the
#    recipe and in the game. Surfaces carry their own 2D frame; every placement names the item, a surface and numbers.
#    Left and right are the VIEWER'S, in the game (the fascia target's rule: low street x is on the viewer's RIGHT looking
#    at the east parade, on the viewer's LEFT looking at the west block).
#
#    THE AMOUNT OF PAPER is the asset plan's, AT MOST (note 4, table A5, Quay Street, the proof view): 8 fly-posters and 4 poll-tax bills. The default street carries 5 and 3. The quay gable
#    is BARE, as the Hook sheet shows it (a black downpipe 0.3 m from the front corner, a render patch high up, a dark damp foot): no paper and no plate on it (second review, accepted by Jafar's
#    ruling of 9 October). The plan's proof wall (three bills in one layer) is HELD, for the case that he chooses the gable for the sample; the empty unit's glass SF2 (one layer of six sheets)
#    is the proof sample in the default street; NOTHING MORE until he has approved a sample in the assembled game (CLAUDE.md).
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
                reach_note="a billposter pastes to about 2.7 m from the ground",
                fixtures=[dict(id="downpipe", kind="round cast-iron downpipe, black", u_m=0.30, diameter_mm=75, z_m=[0.0, 6.0], keep_paper_clear_mm=150,
                               source="the Hook sheet's gable: a black downpipe about 0.2 to 0.4 m from the front corner, full height (TARGET-REVIEW fault 4, read off the sheet by the reviewer)"),
                          dict(id="render_patch", kind="a patch of pale render high up", z_m=[3.6, 5.0], note="above the paste zone: nothing pasted there"),
                          dict(id="damp_foot", kind="dark damp foot", z_m=[0.0, 0.45], note="below the paste zone: nothing pasted there")],
                sheet_note="The Hook sheet's gable is bare old brick, a downpipe, a render patch and a damp foot, and it is the biggest near surface in the hook frame: THE GABLE IS BARE (second review, accepted by Jafar's ruling of 9 October). No paper and no plate on it in the default street. The plan's proof wall (P01, W01, T02 with its strip T02s, in ONE layer at z 1.00 to 1.76, u 0.70 to 2.92, and a second QUAY STREET plate at u 1.0) is kept as HELD placements flagged proof_wall = true, used only if he chooses the gable for the sample; the empty unit's glass SF2 is the proof sample in the default street (the asset plan allows 'the nearest gable, or the empty unit's stallriser')."),
    "SF2": dict(id="SF2", name="the empty unit's whitened display glass (bay 3, east, number 7, street x 21 to 27)", plane="the street face of the glazing, set back 0.12 m",
                frame="u in metres from the glass's viewer's-LEFT edge (the high-x end, street x 26.65), z up from the pavement; glass 3.562 m wide, z 0.60 to 2.40",
                u_range=[0.0, 3.562], z_range=[0.60, 2.40], glass_street_x=[23.088, 26.65], note="the recipe's fx counts from the viewer's RIGHT: u = 3.562 x (1 - fx)"),
    "SF4": dict(id="SF4", name="the lamp columns", plane="the shaft, 0.114 m across", frame="street x of the column, z up the shaft", columns_street_x=[8.0, 28.0, 48.0],
                note="SCENE-SLOTS: every 20 m, alternate sides, first at 8 m, 0.6 m back from the kerb; a bill wraps the shaft, so the middle 0.17 m of an A3 shows face-on"),
    "SF5": dict(id="SF5", name="the empty unit's fascia", plane="fascia face, 0.12 m proud", frame="centre street x and z", fascia_z=[2.85, 3.40], bay_centre_street_x=24.0),
    "SF6": dict(id="SF6", name="first-floor brick above the empty unit's cornice", plane="brick face", frame="centre street x and z", z_range=[3.55, 4.3], window_gap_street_x=[22.93, 25.07]),
    "SF7": dict(id="SF7", name="name-plate walls", note="the west corner pier (street x 19.92 to 21.0, brick to 3.12 m): the street's one QUAY STREET plate (the quay gable carries none: the Hook sheet shows none there; a second plate at u 1.0 is a HELD placement); the yard entrance (street x 21 to 24, the dropped kerb at 22.5) carries NO plate: vignette-scene.json and atlas-01 call it the yard entrance and canon does not name it"),
    "SF8": dict(id="SF8", name="the quay-edge post", plane="a 100 mm post at the quay end, street x about -0.6", frame="z up the post", note="no quay geometry in SCENE-SLOTS: proposed, the builder places the post"),
    "SF9": dict(id="SF9", name="the plain west row's bay-1 window", plane="the glass of the cottage sash at street x 12.3 (centre), 0.85 m wide, sill 0.9 m", frame="street x of the window's centre, z up from the pavement",
                window_street_x=[11.875, 12.725], z_range=[0.9, 2.4], note="bay 1 of the plain row (street x 9 to 15): door at 10.5, windows at 12.3 and 14.1 (terrace-front.py _plain_ground; the scene file's poster slot at x 11.4 is the pier between)"),
}


def poly_overlap_area(a, b):
    ax0, ay0, ax1, ay1 = a
    bx0, by0, bx1, by1 = b
    w = min(ax1, bx1) - max(ax0, bx0)
    h = min(ay1, by1) - max(ay0, by0)
    return max(0.0, w) * max(0.0, h)


def _dims_m(item_id, items_by_id, scale=1.0):
    f = items_by_id[item_id]["format"]
    return f["w_mm"] * scale / 1000.0, f["h_mm"] * scale / 1000.0


def plan_all(items_by_id):
    P = []

    def add(item, surface, age, z, rot=0.0, layer=0, u=None, x=None, scale=1.0, **kw):
        w, h = _dims_m(item, items_by_id, scale)
        d = dict(item=item, surface=surface, z_bottom_m=round(z, 3), rot_deg=round(rot, 3), layer=layer, age_class=age, w_m=round(w, 4), h_m=round(h, 4))
        if u is not None:
            d["u_m"] = u
        if x is not None:
            d["street_x_m"] = x
        if scale != 1.0:
            d["scale"] = scale
        d.update(kw)
        P.append(d)
        return d

    # ---- the quay gable SF1 is BARE, as the Hook sheet shows it (second review, accepted by Jafar's ruling of 9 October): the plan's proof wall (three bills in one layer, bottoms at z 1.00, and a
    #      second QUAY STREET plate above) is HELD, not in the default street. P01, W01 and T02 with its strip are the proof wall; W01 and T02 are also nameless stand-ins (held with their named twins).
    GABLE = "HELD: the quay gable is bare as the Hook sheet shows it (second review; Jafar's ruling of 9 October). This was the plan's proof wall; it is used only if he chooses the gable for the proof sample instead of the empty unit's glass"
    add("P01", "SF1", "B", 1.00, rot=-0.6, u=0.70, proof_wall=True, held=True, held_why=GABLE, note="poll tax; the meeting of Thursday 25 October is four days gone on the street date (a stale bill, class B)")
    add("W01", "SF1", "A", 1.00, rot=0.5, u=1.30, proof_wall=True, held=True, held_why=GABLE, note="professional wrestling, Friday 2 November: class A")
    w02, h02 = _dims_m("T02", items_by_id)
    add("T02", "SF1", "A", 1.00, rot=-0.4, u=1.90, proof_wall=True, held=True, held_why=GABLE, note="the Tivoli quad, from Thursday 25 October: class A, four days up")
    add("T02s", "SF1", "A", 1.00 + h02 - STRIP_H / 1000.0 + 0.004, rot=-0.4 + 0.25, u=1.90 + 0.003, layer=1, proof_wall=True, held=True, held_why=GABLE, parent="T02",
        note="the venue strip across the quad's top band: set 4 mm high and 3 mm in, 0.25 degrees off the quad's own square (TARGET-REVIEW fault 7: 2 to 6 mm off square)")
    # ---- the empty unit's glass SF2: one layer (u from the glass's viewer's-left edge)
    add("C01a", "SF2", "B", 1.30, rot=0.3, u=0.30, layer=1, fixing="four tabs of yellowed tape, one at each corner", note="the police appeal for Friday 12 October, inside the empty unit's glass (TARGET-REVIEW fault 10)")
    add("M01", "SF2", "C", 0.80, rot=0.8, u=0.75)
    add("P03", "SF2", "B", 0.85, rot=1.2, u=1.35, note="the march of Saturday 10 November")
    add("P02", "SF2", "B", 0.82, rot=0.6, u=1.95)
    add("J01", "SF2", "B", 1.05, rot=-0.8, u=2.60, note="the jumble sale of Saturday 20 October is nine days gone: stale, class B")
    add("C02", "SF2", "A", 1.50, rot=0.0, u=3.01, layer=1, note="planning notice for number 7, in its sleeve, taped inside the glass")
    # ---- the plain west row: the scene's own poster slot (x 11.4 = pier W1.0) and one window bill
    piers = {p["id"]: p for p in west_piers()}
    pr = piers["W1.0"]
    add("M01", "WEST_PIER", "B", 1.00, x=pr["cx"], pier="W1.0", pier_w_m=pr["w"], note="the scene file's poster slot, x 11.4: the market bill (a second seed of M01, class B), which needs no unminted name (second review, fault 3: the wrestling bill that stood here named no ring and no hall)")
    pr = piers["W2.0"]
    add("L04", "WEST_PIER", "C", 2.15, x=pr["cx"], pier="W2.0", pier_w_m=pr["w"], layer=2)
    add("P02", "SF9", "A", 1.90 - 0.4458, x=12.3, scale=0.585, taped_inside=True, inside=True,
        note="P02 scaled by 297/508 (0.585) to 297 x 446 mm, taped inside the glass, top at 1.90 m (TARGET-REVIEW fault 4)")
    # ---- the lamp columns
    add("C03", "SF4", "A", 1.55, x=8.0, layer=1)
    add("P05", "SF4", "C", 1.25, x=8.0, layer=1)
    add("P06", "SF4", "B", 1.45, x=28.0, layer=1)
    add("P05", "SF4", "D", 1.85, x=28.0, layer=1)
    # ---- the letting boards: the fascia target's board on the fascia; a no-agent flat board above
    add("L02", "SF5", "C", 2.90, rot=-1.5, x=24.0, note="the fascia target's own board (900 x 450, TO LET); L01 (a named agent, 1200 x 450) is the held alternative")
    add("L03n", "SF6", "C", 3.70, rot=1.0, x=24.0, note="no agent, no name; L03 (a named agent) is the held alternative")
    # ---- name plates: the nameless plate `n`, ONE QUAY STREET plate (the west corner pier's) and NO plate on the yard entrance or the gable
    h = _dims_m("S01n", items_by_id)[1]
    add("S01n", "SF7", "D", 2.63 - h / 2, x=20.47, note="west corner pier (x 19.92 to 21.0, brick to 3.12 m): the existing plate's place, kept; 80 mm of pier either side")
    add("S01n", "SF7", "D", 2.63 - h / 2, u=1.0 - _dims_m("S01n", items_by_id)[0] / 2, host="SF1", u_centre_m=1.0, proof_wall=True, held=True, held_why=GABLE,
        note="HELD: a second QUAY STREET plate on the quay gable, centre 1.0 m from the front corner, centre z 2.63 (above the proof wall's tops, 1.76 m). The sheet shows none on the gable; the street's one plate is on the west corner pier")
    # ---- harbour enamel
    add("H02", "SF8", "C", 1.20, x=-0.6, note="PROPOSED: on a post at the quay edge; no quay geometry in SCENE-SLOTS")
    return P


def held_alternates(placements, items_by_id):
    """Every placement whose item has a NAMED variant gets a held twin: the named item at the same place, held_until_minted. The named letting boards are twins of the nameless ones too
    (L02 -> L01, L03n -> L03). (A nameless STAND-IN has a twin too: the stand-in's own placement is held as well, see finish_held.)"""
    out = []
    twin = {"L02": "L01", "L03n": "L03"}
    for p in placements:
        alt = twin.get(p["item"]) or (p["item"] + "-named" if (p["item"] + "-named") in items_by_id else None)
        if alt and alt in items_by_id:
            q = dict(p)
            q["item"] = alt
            q["held_until_minted"] = True
            q["held"] = True
            q["names"] = items_by_id[alt].get("held_names", [])
            q["alt_of"] = p["item"]
            w_, h_ = _dims_m(alt, items_by_id, p.get("scale", 1.0))
            q["w_m"], q["h_m"] = round(w_, 4), round(h_, 4)          # the twin's own size (L01 is 1200 x 450, the fascia target's board 900 x 450)
            q["note"] = "HELD: the named variant of the placement above; built only after the town mints " + ", ".join(q["names"])
            out.append(q)
    return out


def finish_held(placements, items_by_id):
    """Flag the held placements for the checks and the drawing: `held` is 'not in the default street' for any reason; `held_until_minted` (with `names`) is the reason of unminted names. A nameless
    stand-in's placement waits for the names its named twin carries."""
    for p in placements:
        it = items_by_id.get(p["item"])
        if it is not None and it.get("stand_in_of"):
            p["held_until_minted"] = True
            p["stand_in"] = True
            p["names"] = list(it["waits_for"])
            p["held_why"] = STAND_IN_WHY
        if p.get("held_until_minted") or p.get("held_why"):
            p["held"] = True
    return placements


# --------------------------------------------------------------------------------------------
# 10. Assemble.
# --------------------------------------------------------------------------------------------
def all_items():
    ITEMS.clear()
    bill_poll_meeting(); bill_poll_meeting(True); bill_dont_pay(); bill_dont_pay(True); bill_march(); bill_march(True); bill_summons_a4(); sticker_polltax(); sticker_cantpay()
    bill_jumble(); bill_dance(); bill_dance(True); bill_wrestling(); bill_wrestling(True); bill_boxing(); bill_market(); goods_whitewell(); goods_tea()
    tivoli_witness(); tivoli_witness(True); tivoli_gullwing(); tivoli_gullwing(True); tivoli_programme(); tivoli_programme(True)
    tivoli_strip("T01", 18, 10); tivoli_strip("T02", 25, 10)
    ferry_timetable(); ferry_summer(); enamel_no_admittance(); enamel_danger_water()
    harbour_notice_berths(); harbour_notice_tides(); harbour_notice_vacancy()
    police_notices(); planning_notice(); road_closure_notice()
    card_closed_lunch(); card_back_at(); card_open_closed(); card_no_dogs(); card_shut_door(); cards_launderette(); cards_stars(); card_no_credit(); cards_fish(); small_ads()
    letting_boards(); street_plates()
    return list(ITEMS)


FORBIDDEN_WORDS = dict(
    alcohol_gambling_children=["beer", "beers", "lager", "ale", "stout", "pint", "pints", "whisky", "whiskey", "vodka", "gin", "rum", "wine", "cider", "champagne", "cocktail", "liquor", "spirits",
                               "booze", "pub", "pubs", "bar", "bars", "inn", "tavern", "licensed", "brewery", "shandy", "bitter", "nightclub", "disco", "happy hour",
                               "bingo", "raffle", "tombola", "lottery", "pools", "bet", "betting", "bookie", "bookies", "bookmaker", "odds", "stake", "casino", "gamble", "gambling",
                               "jackpot", "dice", "poker", "whist", "whist drive", "beetle drive", "draw", "prize", "sweepstake", "tote", "scratchcard", "fruit machine", "amusements", "arcade",
                               "lucky dip", "darts", "quiz", "quiz night",
                               "child", "children", "kid", "kids", "baby", "babies", "babysitter", "toddler", "toddlers", "pram", "pushchair", "school", "schools", "pupil", "playground",
                               "playgroup", "nursery", "creche", "christening", "teenage", "teenagers", "junior", "juniors", "infant", "family", "families", "toy", "toys", "santa",
                               "grotto", "youth", "boys", "girls", "scout", "scouts", "cubs", "brownies", "guides", "student", "students", "son", "sons", "daughter", "daughters",
                               "babysitters", "inns", "playgroups", "teens", "lad", "lass", "kiddies"],
    real_marks=["ROYAL MAIL", "POST OFFICE", "BRITISH RAIL", "BRITISH TELECOM", "BRITISH GAS", "NATIONAL LOTTERY", "CRIMESTOPPERS", "NEIGHBOURHOOD WATCH", "LETRASET", "DYMO",
                "BBC", "ITV", "THATCHER", "KINNOCK", "LABOUR", "CONSERVATIVE", "TORY", "TORIES", "SDP", "LIBERAL", "FEDERATION",
                "LARKIN", "SEA WOLF", "SEA WOLVES", "BIG TED", "MILITANT", "SOCIALIST WORKER", "ANTI-POLL TAX UNION", "ALL BRITAIN",
                "PERSIL", "DAZ", "ARIEL", "OMO", "BOLD", "SURF", "ODEON", "ABC", "RANK", "PG TIPS", "TYPHOO", "BROOKE BOND", "TETLEY",
                "BIG DADDY", "GIANT HAYSTACKS", "KENDO NAGASAKI", "MICK MCMANUS", "JACKIE PALLO", "ROLLERBALL ROCCO",
                "CROWN", "KIOSK", "TELEPHONE BOX", "PHONE BOX", "OPERATOR", "BBFC", "CERTIFICATE", "TRANSCO", "NORTHERN GAS",
                "HULL", "GRIMSBY", "SUNDERLAND", "NEWCASTLE", "LIVERPOOL", "LONDON", "LEEDS", "MANCHESTER", "SHEFFIELD", "BRISTOL", "CARDIFF", "GLASGOW", "EDINBURGH", "DOVER", "HARWICH", "FELIXSTOWE", "SOUTHAMPTON",
                "PLYMOUTH", "WHITBY", "HARTLEPOOL", "MIDDLESBROUGH", "TEESSIDE", "TYNESIDE", "MERSEYSIDE", "YORKSHIRE", "LANCASHIRE", "ENGLAND", "BRITAIN", "SCOTLAND", "WALES", "UK"],
    names_not_minted=["MERIDIAN TOWN", "AFC", "ARGUS", "TIDELINE", "COASTWAY", "COUNCIL", "BOROUGH", "CITY OF", "CONSTABULARY", "METROPOLITAN"],
    after_1992=["MOBILE", "INTERNET", "EMAIL", "E-MAIL", "WWW", "WEBSITE", "EURO", "DVD", "TEXT"],
    note="word-boundary, case-insensitive. The names in 'proposed_names' are PLACEHOLDERS allowed on the sheets and NEVER on his page, and a proposed name in a block of cap 10 mm or more holds its item (held_until_minted). "
         "self_check.py also runs tools/content-gate.py's rule table and RealWorld.cs's AnyCase names and imagegen's forbidden tokens over every string.")


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")


def hand_jit(b):
    """The jitter of a hand block's style that moves a glyph's shape: (size_sd, rotation_sd_deg); (0, 0) for print."""
    h = b.get("hand")
    return (h["size_sd"], h["rotation_sd_deg"]) if h else (0.0, 0.0)


def choose_ppm(items):
    """Each item's pixel scale is the smallest at which every glyph of every block (but the imprints) is told from every other glyph of its font by at least
    glyphlib.N_MIN pixels, and never under 2 px/mm (glyphlib.needed_ppm; self_check.py re-derives the same table and fails the item if its scale is lower). A HAND block's pairs are
    measured over glyphs jittered to 3.5 sd of its style (size and rotation); self_check.py group 12 then reads 20 true jittered seeds of every hand card, and HAND_PPM_FLOOR holds the
    scale of any card that needed a raise to pass them."""
    unions = {}
    for it in items:
        for b in it["blocks"]:
            if not b.get("glyph_check") or b.get("ghost"):
                continue
            emb = (b["hand"] or {}).get("embolden_mm", 0.0) if b.get("hand") else 0.0
            unions.setdefault((b["font"], b["weight"], b["cap_mm"], emb) + hand_jit(b), set()).update(b["text"])
    need = {}
    cache_p = Path(os.environ.get("PBP_PPM_CACHE", "")) if os.environ.get("PBP_PPM_CACHE") else None
    cache = json.loads(cache_p.read_text()) if cache_p and cache_p.exists() else {}
    for k, chars in sorted(unions.items()):
        key, wt, cap, emb, ssd, rsd = k
        ck = json.dumps([key, wt, cap, emb, ssd, rsd, "".join(sorted(chars)), gl.N_MIN, gl.TOL_PX, "jit3.5"])
        if ck in cache:
            need[k] = cache[ck]
            continue
        jit = dict(size_sd=ssd, rotation_sd_deg=rsd) if (ssd or rsd) else None
        ppm, _t = gl.needed_ppm(font, key, wt, cap, cap_ratio(key, wt), sorted(chars), emb_mm=emb, jit=jit)
        need[k] = ppm if ppm else 16
        cache[ck] = need[k]
    if cache_p:
        cache_p.write_text(json.dumps(cache))
    for it in items:
        m = HAND_PPM_FLOOR.get(it["id"], 2)
        for b in it["blocks"]:
            if not b.get("glyph_check") or b.get("ghost"):
                continue
            emb = (b["hand"] or {}).get("embolden_mm", 0.0) if b.get("hand") else 0.0
            m = max(m, need[(b["font"], b["weight"], b["cap_mm"], emb) + hand_jit(b)])
        it["px_per_mm"] = m
        mp = it["format"]["w_mm"] * it["format"]["h_mm"] * m * m / 1e6
        assert mp <= 60, "%s would be %.0f megapixels at %d px/mm" % (it["id"], mp, m)
        it["megapixels"] = round(mp, 1)


HAND_PPM_FLOOR = {}      # item id -> px/mm: the least scale at which the 20-seed true-render test of group 12 passes (raised by hand_tune when a card needed more than needed_ppm gave)


def build():
    items = all_items()
    by_id = {it["id"]: it for it in items}
    for it in items:
        it["held_names"] = held_names(it)
        it["held"] = bool(it["held_names"])
    for k, tw in STAND_INS.items():
        by_id[k]["held"] = True
        by_id[k]["stand_in_of"] = tw
        by_id[k]["waits_for"] = list(by_id[tw]["held_names"])
        by_id[k]["held_why"] = STAND_IN_WHY
    choose_ppm(items)
    # every hand-lettered card carries ONE cue that matches its fixing and sits on the left half only (TARGET-REVIEW fault 9)
    for it in items:
        if it["blocks"] and all(b.get("hand") for b in it["blocks"]):
            fx = it["fixing"]
            w, h = it["format"]["w_mm"], it["format"]["h_mm"]
            stars = [s for s in it["shapes"] if s["kind"] == "star"]
            if stars:
                tip = max(stars[0]["pts_mm"][0::2], key=lambda p: p[1] - p[0])      # the outer point nearest the top-left corner
                cx, cy = round(tip[0] + 3.0, 1), round(tip[1] - 6.0, 1)
                left = [round(cx - 12.5, 1), round(cy - 12.5, 1), round(cx + 12.5, 1), round(cy + 12.5, 1)]
            else:
                cx, cy = 12.0, h - 12.0
                left = [0.0, h - 25.0, 25.0, h]
            right = [round(w - left[2], 1), left[1], round(w - left[0], 1), left[3]]
            it["mirror_cue"] = dict(kind=fx["kind"], what=fx["what"], side="left", corner="top-left", patch_mm=25, tab_centre_mm=[cx, cy], patch_left_mm=left, patch_right_mm=right,
                                    rule="drawn at the card's top-LEFT as the viewer sees it in the game, nothing on the right half; G.mirror.cues compares the two 25 mm patches (non-text pixels)")
    problems = []
    for it in items:
        problems += check_fit(it)
    assert not problems, problems
    cases = make_cases()
    placements = plan_all(by_id)
    placements += held_alternates(placements, by_id)
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
        C.append(chk(iid + ".size", "image size", iid, "width and height of the base-colour image", [int(round(w * ppm)), int(round(h * ppm))], 0, "px at %g px/mm" % ppm, "image size",
                     why="1 pixel is 1/%g mm" % ppm))
        words = sorted({norm(b["text"]) for b in it["blocks"]})
        C.append(chk(iid + ".words", "words exactly as approved", iid, "the strings in the glyph manifest (every character as drawn), apostrophes and dashes normalised",
                     words, 0, "strings", "the manifest's characters, joined per block, equal the approved string; a missing or unreadable <ITEM>.glyphs.json FAILS (it never crashes the reader); THIS IS NOT THE PIXEL CHECK: ITEM.glyphs reads the pixels", reads="manifest",
                     why="the words are ours; the image model never draws one"))
        blocks = [b for b in it["blocks"] if not b.get("ghost")]
        if not blocks:
            continue
        C.append(chk(iid + ".pos", "block positions", iid, "ink box of each block's glyph mask read off the pixels, widened 8 mm along the line (other blocks' glyphs excluded)",
                     [[b["id"], block_tols(b, ppm)["pos_mm"], block_tols(b, ppm)["base_mm"]] for b in blocks], "per block [id, centre tol mm, baseline tol mm]", "mm",
                     "centre (anchor centre) or left/right edge within the tolerance; baseline within the baseline tolerance (the median bottom of flat-bottomed letters)"))
        C.append(chk(iid + ".cap", "letter heights at scale", iid, "cap height of each block read off its flat-bottomed capitals",
                     [[b["id"], b["cap_mm"], block_tols(b, ppm)["cap_frac"]] for b in blocks], "per block [id, cap mm, tolerance as a fraction]", "fraction of the cap",
                     "height of the tallest flat-topped, flat-bottomed capital in the block's mask / cap_mm; also cap_px = cap_mm x px_per_mm"))
        C.append(chk(iid + ".mask", "glyph mask of the line against the font", iid, "the block re-rendered from its font file compared with the ink-coloured pixels",
                     [[b["id"], block_tols(b, ppm)["F"]] for b in blocks], "per block [id, min F]", "F score",
                     "mean of recall and precision, each against the other mask dilated 2.5 mm (hand) or 1 mm (print); a PRINT line must also keep every single glyph at F 0.85 or more at 0.5 mm. A HAND line's mask catches a wrong font or a shift, not a wrong word (TARGET-REVIEW fault 1): ITEM.glyphs reads those from the manifest"))
        gb = [b for b in blocks if b.get("glyph_check")]
        if gb:
            C.append(chk(iid + ".glyphs", "every glyph read from the pixels", iid,
                         "each character of the manifest read in its own cell: F at 0.5 mm against the glyph re-rendered from the manifest, SEP against every other glyph of its font and its own mirror (render_contract.glyph_gate)",
                         [[b["id"], len(b["text"])] for b in gb], "per block [id, characters]", "F >= 0.85 and SEP >= 0.70 (a margin of 0.40) against every alternative the pixels can tell apart",
                         "glyphlib.py: a missing or unreadable manifest FAILS; the characters equal the approved string; each glyph lies in the block's envelope; spaces carry no ink (beyond 0.6 mm of every glyph); a neighbour's ink that the neighbour explains and the glyph does not is the neighbour's",
                         why="a changed date, TEA for ALE, LUNCH for BINGO passed the line mask at F 0.94 to 1.00"))
        C.append(chk(iid + ".square", "the texture is square-on", iid,
                     "rotation of the render found against the render of the item's own glyph manifest, jitter included (render_contract.texture)",
                     0.0, SQUARE_TOL_DEG, "degrees", "|angle| <= 0.3 degrees, one tolerance for print and hand-lettered items alike; 0 unless F at the best angle beats F at 0 by 0.02",
                     why="skew lives only in the placement's rot_deg"))
        C.append(chk(iid + ".clean", "no ink outside the places lettering stands", iid,
                     "ink-coloured pixels on the class-A render before wear, outside every block's glyph window, the item's own shapes, the cue patch and the art slots (render_contract.clean)",
                     CLEAN_MAX_MM2, CLEAN_MAX_MM2, "mm2", "total area <= 2 mm2", why="a line drawn on a margin, a held name left on a default item"))
        cons = []
        for b in blocks:
            nominal = b["contrast"]["B"]
            floor = 3.0 if b["cap_mm"] >= 12 else 4.5
            mn = max(2.2, min(floor, 0.9 * nominal))
            if b["role"] == "imprint":
                mn = 1.8
            cons.append([b["id"], round(mn, 2), nominal])
        C.append(chk(iid + ".contrast", "contrast", iid, "WCAG ratio of the block's mean ink colour to the mean ground colour in its box, on the aged render (class B)", cons,
                     "per block [id, min ratio, nominal ratio in class B]", "ratio", "ink = pixels nearer the ink colour than the ground; ground = the rest of the box"))
        if it["art"]:
            C.append(chk("ART.eye." + iid, "the art picture carries no person, hand, face, lettering, numeral, crown, kiosk mark, bottle, glass or arcade sign", iid,
                         "a fresh reviewer looks at the generated picture at 1:1 (the art slot's box), before any text is laid", "none of the listed things", 0, "count",
                         "a pass needs a person who has not seen the prompt; the first pass of the picture is the one judged", reads="eye",
                         why="an image model that draws a pier or a phone box adds people, lettering, a crown or AMUSEMENTS signs (TARGET-REVIEW fault 1c); there is no pixel test for it"))
    # ---- global checks
    C.append(chk("G.words.approved", "no word outside the approved list", "all items", "every token of every manifest string", "tokens subset of approved_word_parts", 0, "tokens",
                 "split on spaces; apostrophes, dashes and the middle dot normalised; digits and times match the number patterns", reads="manifest"))
    C.append(chk("G.forbidden", "no forbidden word", "all items", "forbidden_patterns (alcohol, gambling, children, real marks, names not minted, after 1992) and tools/content-gate.py's rule table over every manifest string",
                 0, 0, "hits", "word-boundary, case-insensitive", reads="manifest"))
    C.append(chk("G.dates", "every dated bill's weekday is right for the year", "bills with an event", "weekday of the printed date in 1990", "equal", 0, "days", "datetime.date", reads="manifest"))
    C.append(chk("G.dates.age", "a placed dated item's age class agrees with its event and the street date", "placed items with a date",
                 "calendar.street_date minus the days of the placement's age class (age_classes[class].days)",
                 dict(street_date="1990-10-29", event="the class's earliest posting date must fall at or before the event and no more than 42 days before it; a notice at or after its date"),
                 0, "days", "for each placement of an item with `dated`: exists an age a in the class's days with event - 42 <= street_date - a <= event (kind event) or street_date - a >= date (kind notice)",
                 reads="geometry", why="the first try put T03 in class D under T01 in class A for the same week (TARGET-REVIEW fault 8)"))
    C.append(chk("G.mirror", "no sheet is mirrored", "all items", "for each asymmetric block, the glyph mask scores higher at its own position than at the position mirrored about the item's centre line", "true", 0.0, "bool",
                 "the fascia family's first try drew its board the wrong way round; ITEM.glyphs also fails a mirrored block at its own cells"))
    cue_items = [it["id"] for it in items if it.get("mirror_cue")]
    C.append(chk("G.mirror.cues", "a hand-lettered card carries its one cue on the left half", "cards: %s" % ", ".join(cue_items),
                 "the 25 mm top-left and top-right corner patches (non-text pixels): the yellowed tape tab, or the knot and sucker, shows in the left one only",
                 {it["id"]: it["mirror_cue"]["side"] for it in items if it.get("mirror_cue")}, 0.0, "bool",
                 "left patch differs from the card's own colour by dE >= 6 and the right by <= 2.5; mirrored: the opposite", reads="pixels",
                 why="the words of a centred hand-lettered card read alike mirrored at line level; ITEM.glyphs also fails them, this is the second guard"))
    C.append(chk("G.fonts", "fonts are the OFL list", "all items", "the font name of every block", sorted(FONTS), 0, "names", "block.font in this list; Overpass, Apache and GPL faces refused", reads="manifest"))
    C.append(chk("G.proposed", "proposed names stay where listed", "all items", "each proposed name appears only on the items proposed_names lists for it", "listed", 0, "strings", "manifest", reads="manifest",
                 why="placeholders, never on his page (RULINGS 3 Oct)"))
    C.append(chk("G.page.placeholders", "no held placement is built while its name has no DECISIONS.md minting line", "the built street's placed-decals manifest",
                 "every placement with held_until_minted: true", "none in the built street unless DECISIONS.md carries a line 'MINTED: <NAME>' for each name in the placement's `names`", 0, "placements",
                 "the builder writes placed_decals.json; the check fails any held placement found in it whose names are not all minted (a line of DECISIONS.md that starts '- ' and holds 'MINTED:' then the name)",
                 reads="manifest", why="placeholders are never on his page; whole street frames go on his page (RULINGS 3 Oct; TARGET-REVIEW fault 2)"))
    C.append(chk("G.ferry.schedule", "the ferry timetable is a service one boat can run, and each day ends where the next begins", "F01",
                 "crossing 15 minutes; Hook departures at :00/:30 by day, far side at :15/:45; last Hook crossing 11.00 PM, last far-side crossing 11.15 PM; the boat ends each day at the Hook",
                 "consistent", 0, "minutes", "parse the printed blocks, simulate the one vessel through Monday to Saturday, Sunday and Monday", reads="manifest"))
    C.append(chk("G.tides", "the tide table advances 12 h 25 min a high water and peaks on Sunday 4 November", "H04", "difference between successive HW times; the day's higher height", [745, [4.4, 4.6, 4.7, 4.8, 4.7, 4.5, 4.2]], 5, "minutes", "parse the rows", reads="manifest"))
    # placements
    C.append(chk("G.place.inside", "each placement lies inside its surface's paste zone", "placements", "rectangle inside the zone", "inside", 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.place.layers", "same-layer bills do not overlap; every older bill keeps its share of face", "SF1, SF2", "visible fraction by raster", dict(layer0=0.30, layer1=0.45, top=0.97), 0.0, "fraction", "visible_fractions()", reads="geometry"))
    C.append(chk("G.place.piers", "a bill on a west pier fits the brick with 40 mm each side, and clears the openings", "WEST_PIER", "bill width <= pier width - 0.08", "true", 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.place.height", "nothing pasted above 2.75 m", "SF1", "top edge of every full bill and plate", 2.75, 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("G.place.paper", "the amount of paper is at most the asset plan's: 8 fly-posters and 4 poll-tax bills on Quay Street", "default placements (not held)",
                 "count of placed items by paper_class: fly_poster, poll_tax_bill", dict(fly_poster_at_most=8, poll_tax_bill_at_most=4, default_street_carries=dict(fly_poster=5, poll_tax_bill=3)), 0, "count", "geometry", reads="geometry",
                 why="asset-plan note 4, table A5, row 'Fly-posters and gig bills 8' and 'Poll-tax and election bills 4' (TARGET-REVIEW fault 4); AT MOST, since the bare gable took three bills off the street (second review)"))
    C.append(chk("G.place.gable", "the gable is bare, as the Hook sheet shows it", "SF1", "no paper and no plate on SF1 in the default street; the downpipe (75 mm at u 0.30, full height), the render patch (z 3.6 to 5.0) and the damp foot (z 0 to 0.45) stand as fixtures, and the held proof-wall placements, if ever used, keep 150 mm clear of the pipe, below 2.75 m and out of the foot", "true", 0.0, "m", "geometry", reads="geometry",
                 why="the Hook sheet shows old brick, a downpipe, a render patch and a damp foot; the review's decision, accepted by Jafar's ruling of 9 October"))
    C.append(chk("G.place.shops", "shop cards lie inside their glass or door glass, clear the hours plate and each other", "SHOP", "rectangles", "true", 0.0, "m", "geometry", reads="geometry"))
    C.append(chk("PLACE.built", "each placed decal is where the target puts it and reads the right way round in the placed street", "the built street's placed-decals manifest and one render of each surface",
                 "centre of each decal against the placement's u and z (or street x); its rotation; the decal's largest block read in the render after turning back by rot_deg",
                 dict(centre_mm=20, rot_deg=0.3, read="the glyph check on the largest block of the item, run on the surface render at 1 px per mm after turning the decal back by the placement's rot_deg"),
                 20, "mm", "locate the decal by correlation of the item's expected ink in a +-60 mm window; rotation by the best angle in +-1.5 degrees; then ITEM.glyphs on the largest block; a mirrored decal or a decal turned more than 0.3 degrees off fails",
                 reads="pixels", why="TARGET-REVIEW fault 1e"))
    C.append(chk("G.letting.mount", "the default letting board IS the fascia target's board", "L02 and the fascia target's small_panels.letting_board",
                 "size 900 x 450, text TO LET, font libre-franklin 800, cap 130, colour vinyl_red (176,30,34), no agent, no number; sits z 2.90 to 3.35 inside the fascia 2.85 to 3.40",
                 dict(size_mm=[900, 450], font="libre-franklin", weight=800, cap_mm=130, z=[2.90, 3.35]), 0.01, "m", "compare with fascia-signs/target.json", reads="geometry",
                 why="TARGET-REVIEW fault 5; a different board changes the fascia target's entry in the same batch with a DECISIONS line"))
    C.append(chk("G.plates.length", "plate length follows the name", "S**", "ink width + 2 x 62 mm margins, rounded up to 10 mm", "see name_plate", 10, "mm", "geometry", reads="geometry"))
    C.append(chk("G.plates.depth", "no plate is shallower than 200 mm", "S**", "plate height", 200, 0, "mm", "geometry", reads="geometry", why="the street-clutter note's 20 to 25 cm (TARGET-REVIEW fault 13)"))
    C.append(chk("G.plates.cap", "plate capitals are 90 mm", "S**", "cap height of the name block", PLATE_CAP, 3.0, "mm", "pixels at 2 px/mm"))
    C.append(chk("G.plates.border", "border band 12 mm, 6 mm in from the edge", "S**", "dark band width on a scan line through the plate's middle", 12, 1.0, "mm", "pixels at 2 px/mm"))
    C.append(chk("G.plates.make", "the plate's relief suits the make", "S**", "raised mm, draft, top radius, edge radius; the thinnest stroke's top width after the draft >= 1.5 mm", "see relief and lettering_suit", 0, "mm", "geometry", reads="geometry"))
    C.append(chk("G.glyph.scale", "each item's pixel scale is enough to tell its glyphs apart", "all items", "glyphlib.needed_ppm for every (font, weight, cap) of the item", "item.px_per_mm >= needed", 0, "px/mm", "separation_table", reads="geometry"))
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
    dict(topic="postal district and district line on a plate", wins="the project's own street-clutter note (a plain name plate; 'postcodes' wrong for 1990) and the absence of any source", others="a search summary: London plates carried the borough and the postal district; the first try's default carried the district's name as a small line",
         choice="the default and the placed plate is `n` (the name only); `d` (the name and a district line) stays as a variant until a dated photograph shows one; the postal-district variant (MR1) is deleted (TARGET-REVIEW fault 13)"),
    dict(topic="the 4 October bills", wins="this target", others="tools/props/make_vignette_2d.py: clean flat bills, League Gothic, all four on one generic layout, a spring date (SATURDAY 31 MARCH), 'Admission 10p', 'WEIGHHOUSE LANE HALL', the bills' own fine print readable and straight",
         choice="autumn 1990 dates with computed weekdays, the chapel hall named as hook-cast.json names it, imprints, ageing in four classes, layered pasting, different processes and layouts"),
    dict(topic="the letting board", wins="the fascia target (cloud week 42, same batch): 900 x 450, TO LET alone, Libre Franklin 800 cap 130, vinyl red, no agent, no number", others="the first try's 1200 x 450 board with an agent band and a number; the game's board_to_let.png (900 x 450, PT Sans, no agent, no number)",
         choice="L02 IS the fascia target's board. The 1200 x 450 agent board L01 stays as a held variant that would need the fascia target changed in the same batch with one DECISIONS line (TARGET-REVIEW fault 5)"),
    dict(topic="the poster prop's place", wins="the plain row's bay layout (terrace-front.py _plain_ground)", others="vignette-scene.json's held-prop notes put a poster at west x 11.4 and a case at west x 26.4 'between a side door at 25.5 and a window at 27.3' (written before the west_north block became shops)",
         choice="x 11.4 is the pier W1.0 (10.919 to 11.875) and stays; the case at 26.4 would stand on the tea room's glass: both cases move to the quay gable"),
    dict(topic="the glyph check's margin", wins="the computation (glyph_table() in self_check.py; glyphlib.py's docstring)", others="TARGET-REVIEW fault 1(b): each glyph must out-score every other glyph of its font and its own mirror by at least 0.05 on F at 0.5 mm",
         choice="F is a mean over the whole glyph, so glyphs that share most of their ink score alike: O against D in Oswald 700 at 34 mm capitals scores 0.987 against the true glyph's 1.000 (a margin of 0.013), 6 against 8 0.964, and 14 of the 36 capitals and digits cannot meet 0.05 even at that size. The check therefore keeps F >= 0.85 at 0.5 mm for the glyph itself and scores the separation from each alternative on the PIXELS WHERE THE TWO GLYPHS DIFFER (SEP, 0.70 to pass: a margin of 0.40), with every item's pixel scale chosen so that at least 8 such pixels exist for every pair that is not a shape twin. The reviewer's wrong renders all fail it"),
    dict(topic="paper on the quay gable", wins="the asset plan's own proof wall and the Hook sheet together", others="the Hook sheet's gable is bare old brick with a downpipe, a render patch and a damp foot; the plan's proof wants 'three bills from three templates' on one wall (the nearest gable or the empty unit's stallriser)",
         choice="THE GABLE IS BARE, as the sheet shows it (second review, by Jafar's ruling of 9 October): the three bills (P01, W01, T02 with its strip) and the second QUAY STREET plate are HELD placements flagged proof_wall; the downpipe, the render patch and the damp foot stand as fixtures; the proof sample is the empty unit's glass (six sheets in one layer). Nothing more until he has approved the sample in the assembled game"),
    dict(topic="the one photograph measured", wins="judgement", others="the photographed notice case is a modern blue steel replacement with a wide crest header",
         choice="only its vertical fractions inform the glazed case's proportions; the 1990 case is a timber one with thinner rails (HC1)"),
]
COULD_NOT_SETTLE = [
    "No photograph of a 1990 street name plate, letting board, fly-posted wall or paper notice was reached. Every size of those is Judgement on search-summary leads (90 mm capitals, 150 to 230 mm plates, 12 mm borders: modern specs).",
    "Whether provincial plates of 1990 carried a postal district, a district line, the council's name or a crest: not found. The default plate is the name only.",
    "The side opening at street x 21 to 24 is the YARD ENTRANCE (vignette-scene.json, the dropped kerb at x 22.5) and atlas-01 gives it `yard_gap_x [21, 24]`: no plate names it, and the road closure sends traffic round by WEIGHHOUSE LANE and TANNERY ROW, which the atlas does name.",
    "Whether the scene has a quay-edge post, a hoarding, a gable wall at x = 3 that faces the hook camera with the geometry assumed here (8 m deep, eaves 6.3 m): read from vignette-scene.json and the recipe, not from the mesh.",
    "Tobacco bills (cigarettes were advertised on hoardings in 1990): omitted: they need a minted brand and the exact government health-warning wording, which was not read.",
    "The BBFC certificate roundels on film bills are real marks and are not drawn; the 1990 bills carried them.",
    "A police appeal board (the yellow A-board) in 1990: the only dated photograph found is from 2007; this target uses an A3 photocopy taped inside the empty unit's glass or sleeved on a column instead.",
    "The local paper's contents bill, the football club's bills and the radio station's stickers: the names are owed (canon), so none is drawn; the brand bible's proposals (Meridian Town AFC, the Argus, Radio Tideline, Coastway) are NOT used.",
    "Real-name coincidence: the network was closed, so NOTHING proposed was checked against real lists: QUAY PRINT, ARMITAGE & STOBBS, THE FOURTH WITNESS (a film of that name), the four ring names (renamed after TARGET-REVIEW found LARKIN and THE SEA WOLF real), MARSHLAND PICTURES and the three credits. Each is listed in proposed_names for the town to mint or strike, and none stands on the default street.",
    "Prices (cinema 2.80, wrestling 4 and 2.50, ferry 60p, tea 1.35) are Judgement except cod (ONS via the earlier note); smoked haddock 2.90 is dearer than fresh by Judgement.",
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



# --------------------------------------------------------------------------------------------
# 13. Shop windows and doors: the cards. Geometry from the fascia target (street x, door ends) and the recipe's shopfront numbers.
# --------------------------------------------------------------------------------------------
PIL_W, GLASS_W, DOOR_W, SIDE_W = 0.35, 3.562, 0.90, 0.838
HOURS_PLATE = dict(w_mm=300, h_mm=190, z_m=[1.355, 1.545], assumed_centre_u_m=0.45, note="the fascia target: a 300 x 190 plate centred 1.45 m up, on the shop door's glass or the pilaster; its horizontal place is not fixed there, so this target ASSUMES it centred on the door glass (u 0.30 to 0.60) and keeps door cards off that column in z 1.355 to 1.545")
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
    """The newsagent's window board: 15 cards laid on a 760 x 560 mm area of the glass, no overlaps beyond a corner. EVERY card is taped, by one tab at its top-LEFT
    (TARGET-REVIEW fault 9): pins are for a cork board, and the cue of a taped card is one tab across the top-left corner."""
    rng = np.random.RandomState(seed)
    ids = [i for i in items_by_id if i.startswith("SA")]
    W, H = 760.0, 560.0
    placed = []
    order = ["SA15"] + [i for i in ids if i != "SA15"]
    x, y, rowh = 20.0, H - 20.0, 0.0
    for iid in order:
        w, h = items_by_id[iid]["format"]["w_mm"], items_by_id[iid]["format"]["h_mm"]
        if x + w > W - 20:
            x, y, rowh = 20.0, y - rowh - 28, 0.0
        jitter = float(rng.uniform(-6, 6)), float(rng.uniform(-8, 8))
        placed.append(dict(item=iid, x_mm=round(x + jitter[0], 1), y_mm=round(y - h + jitter[1], 1), w_mm=w, h_mm=h, rot_deg=round(float(rng.uniform(-2.5, 2.5)), 1),
                           fixing="tape: one tab across the top-left corner"))
        x += w + 26 + float(rng.uniform(0, 14))
        rowh = max(rowh, h)
    return dict(id="SB1", title="the newsagent's window board of cards", area_mm=[W, H], glass_u_m=1.95, z_bottom_m=0.90, cards=placed, seed=seed,
                note="cards are taped to the inside of the glass, each by ONE tab of yellowed tape across its top-left corner (pins are for a cork board); 15 cards; no card overlaps another by more than a corner; the area sits at glass u 1.95 to 2.71 m from the glass's viewer's-left edge, z 0.90 to 1.46 m")


def shop_placements(items_by_id):
    P = []

    def add(item, shop, where, u, z, rot=0.0, age="B", inside=False, note=None, show_when=None, layer=1):
        it = items_by_id[item]
        P.append(dict(item=item, surface="SHOP", shop=shop, where=where, u_m=u, z_bottom_m=z, w_m=it["format"]["w_mm"] / 1000.0, h_m=it["format"]["h_mm"] / 1000.0,
                      rot_deg=rot, layer=layer, age_class=age, inside=inside, note=note, show_when=show_when))
    # u for where="glass": metres from the glass's viewer's-left edge; for where="door": from the shop door's viewer's-left edge
    for k, (iid, u) in enumerate((("K09a", 0.30), ("K09b", 0.95), ("K09c", 1.60), ("K09d", 2.25), ("K09e", 2.80), ("K09f", 3.30))):
        add(iid, "fish_market", "glass", u, 0.66, rot=[-2, 3, -1, 2, -3, 1][k], inside=True, note="taped inside the glass at the slab's height (one tab at the top-left): the shop-room builder's slab is at about 0.6 m; decal cards on the interior card")
    add("K04", "fish_market", "door", 0.375, 1.05, note="NO DOGS, on the shop door's glass below the hours plate")
    add("K03a", "fish_market", "door", 0.35, 1.62, inside=True, show_when="open", note="the OPEN face when the shop is open (hook-cast hours); K03b when it is shut")
    add("K03a", "ritas", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "steam_laundry", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K06a", "steam_laundry", "glass", 0.20, 1.25, rot=1.0, inside=True, note="LAST WASH: the hour is an hour before the closing time in hook-cast.json (laundry 8 to 5.30); hung on a string and a sucker")
    add("K06b", "steam_laundry", "glass", 1.85, 1.00, rot=-0.8, note="a printed sticker on the outside of the glass")
    add("K06c", "steam_laundry", "interior", 0.0, 0.85, rot=2.0, inside=True, note="on a machine door, inside: the shop-room builder's; the card is the item")
    for k, (iid, u, z) in enumerate((("K07a", 0.20, 1.55), ("K07b", 0.95, 1.20), ("K07c", 1.70, 1.60), ("K07d", 2.45, 1.25))):
        add(iid, "grocer", "glass", u, z, rot=[-3, 2, -2, 4][k], inside=True, note="taped inside the glass; the fluorescent stock fades within weeks (tau 45 to 50 days)")
    add("K08", "grocer", "glass", 3.00, 0.95, inside=True, note="SORRY NO CREDIT GIVEN, A5 landscape, low in the glass")
    add("D01", "grocer", "glass", 1.25, 0.80, rot=0.8, inside=True, age="B", note="the chapel hall's dance notice (A3 photocopy), taped inside the grocer's glass")
    add("K04", "grocer", "door", 0.375, 1.05)
    add("K03a", "grocer", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "chandler", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K03a", "ironmonger", "door", 0.35, 1.62, inside=True, show_when="open")
    add("T03", "ironmonger", "glass", 1.20, 0.80, rot=-0.6, inside=True, age="B", note="the Tivoli's programme as a window bill: a cinema gave shops its bill for the window (Judgement)")
    add("K03a", "newsagent", "door", 0.35, 1.62, inside=True, show_when="open")
    add("K05", "newsagent", "door", 0.64, 1.42, rot=1.5, age="B", note="PLEASE SHUT THE DOOR, taped to the door glass, bottom 1.42 m (centre 1.494 m). TARGET-REVIEW fault 10 asked bottom 1.38 so that its centre is the 1.45 m of its own words; the fascia target's vinyl row TOBACCONIST & CONFECTIONER on the same glass is at z 1.35, cap 70 mm (top 1.385, tolerance 0.03), so the card sits just above it and the words now say bottom 1.42. To the right of the assumed hours plate (300 mm centred on the door glass: u 0.30 to 0.60)")
    add("J01", "newsagent", "glass", 2.80, 1.00, rot=0.5, inside=True, age="B", note="the chapel hall's jumble-sale notice (A3 photocopy), taped inside the newsagent's glass beside the card board SB1 (u 1.95 to 2.71)")
    add("K04", "tea_rooms", "door", 0.375, 1.05)
    add("K03a", "tea_rooms", "door", 0.35, 1.62, inside=True, show_when="open")
    return P


def wear_tables():
    return dict(
        bill_pasted=dict(applies="P01 to P03, W01, B01, M01, G01, G02, T01 to T03 (and their named variants), T01s, T02s: pasted bills", classes="age_rules", gable_extra="soot streaks from the eaves on the upper edge of every bill (opacity 0.1 to 0.25, 20 to 120 mm long), splash-back dirt in the lower 0.4 m (class C and D: 0.2 to 0.35 darker), bills lie over brick courses: the mortar lines show through as a 0.5 mm relief at 75 mm pitch"),
        glass_bill=dict(applies="bills and photocopies on the empty unit's whitened glass or a shop's window", note="smooth, no brick relief; condensation runs stain the lower third of the paper, whitewash shows round and under, the lower edge curls out 3 to 8 mm, sun-fade is stronger (tau x 0.7); every taped sheet: four tabs of yellowed tape at its corners (the hand cards: one tab at the top-left)"),
        notice_sleeve=dict(applies="C01 a to c, C02, C03", sleeve="clear polythene 80 microns; a crease line across the sleeve 1 or 2 per sheet; fog on the inside 0.1 to 0.3 opacity in the lower third; water beads 6 to 20, 2 to 6 mm across, in the lower third; cable ties: 2, tails 40 to 90 mm left uncut; the paper inside yellows to class C within a season; the sheet slides down 5 to 20 mm inside the sleeve"),
        card_felt=dict(applies="K01, K05, K06 a and c, K09, SA15 and the star cards", dog_ears="0 to 2 corners, radius 6 to 14 mm", smudge="0 or 1 finger smudge 5 to 12 mm", sun="the top third bleaches first (tau x 0.8)", tape="the ONE tab of yellowed tape at the top-left is the cue; older tape ghosts may show only on the LEFT half", warp_mm=1.5),
        card_ballpoint=dict(applies="SA01 to SA14", note="record cards curl 1 to 3 mm, one tab of tape yellowing at the top-left, the ballpoint blue fades (tau 250 d), the felt heading fades slower; some cards sit crooked by 1 to 4 degrees; the board's oldest cards are class C"),
        sticker=dict(applies="P05, P06, K04, K06b", edge_lift_mm=[8, 20], scratches=[0, 4], loss_class_C=[0.05, 0.15], loss_class_D=[0.3, 0.6], note="a sticker on a lamp column wraps the shaft; peeled strips leave white paper-fibre residue"),
        enamel_plate=dict(applies="H01, H02", chips=[12, 30], chip_mm=[2, 9], rust_halo_mm=[3, 8], crazing="short crack lines 10 to 25 mm near the bolt holes", rust_tears_mm=[150, 400], bird_lime="1 streak from the top edge, 20 to 50 mm wide", salt_bloom="H02: white fur along the lower edge"),
        cast_aluminium_plate=dict(applies="S01 n, d (QUAY STREET)", flake_share=[0.03, 0.06], flake_note="paint lifts first at the raised letter and border edges, showing bare grey aluminium and a pale oxide bloom (150,150,146)", face="white yellowed to class C/D (232,230,220 -> 214,208,190)", letters="black faded to 44,44,48", grime_gradient=0.12, screw_rust_mm=[20, 80], bird_lime="1 or 2 patches 20 to 50 mm on the top border"),
        pressed_plate=dict(applies="S02 and S03 (WEIGHHOUSE LANE, TANNERY ROW)", note="stove enamel on aluminium or vitreous enamel on steel: chips at the corners and at the screws only (4 to 12 chips of 2 to 6 mm), a grime gradient, no flaking of the letters; the enamel keeps its gloss (roughness 0.3 or 0.12)"),
        letting_board=dict(applies="L01 to L04 (L03n too)", peel_bottom_edge="1 to 3 per cent of the area along the bottom edge, 2 to 6 mm bites", grime_streaks="3 to 7 streaks 100 to 300 mm from the top edge, 0.15 to 0.3 opacity", algae="class D: a 20 mm film along the foot, (62,78,52) at 0.3", rust_runs_mm=[40, 140], red_fade="the red fades towards chalk-pink (196,128,118) by 0.3 at class D", white_yellowing="white (236,236,230) to (214,206,184) at class D"),
        case=dict(applies="HC1, FC1 (neither placed)", note="see the cases' own wear strings"),
    )


# --------------------------------------------------------------------------------------------
# 14. The render contract, the fixings, the second-try answers.
# --------------------------------------------------------------------------------------------
RENDER_CONTRACT = dict(
    texture="EVERY TEXTURE IS SQUARE-ON: no skew, no rotation and no perspective is baked into any base-colour image. Skew and rotation live ONLY in the placement's rot_deg (a hand card's tilt and the A3 sheet's crookedness too). ITEM.square fails a texture turned by more than 0.3 degrees (ONE tolerance, print and hand-lettered alike); the angle is found against the render of the item's own glyph manifest, jitter included, and is 0 unless F at the best angle beats F at 0 degrees by 0.02; PLACE.built checks the placed decal's rot_deg to 0.3 degrees.",
    scale="Each item is rendered at its own px_per_mm (items[].px_per_mm, chosen so that every glyph can be told from every other: glyphlib.needed_ppm). Row 0 of the image is the TOP edge; x runs from the viewer's left; y in the item frame runs up from the bottom edge.",
    ink_mask="The reader's ink mask is the set of pixels nearer (CIE76) the block's aged ink colour than its aged ground colour. Imprints (role imprint, cap 2.4 mm) are not read glyph by glyph: they are illegible by design.",
    clean="ITEM.clean reads the class-A render before wear: the ink-coloured pixels (the ink mask) outside the union of every block's glyph window, the item's own shapes (a rule, a bar of solid ink, a frame's line, a ring, ticks, a hand, a star, a polygon, a roundel, each dilated 1 mm), the card's cue patch and the art slots total at most 2 mm2. A ground (a paint or stock rectangle that lettering stands on) is not such a shape. A line drawn on a margin, a held name left on a default item, a forbidden word anywhere else on the sheet adds its whole area and fails.",
    glyph_manifest=dict(
        file="<ITEM>.glyphs.json, written by the renderer beside every base-colour image (target_drawing.py and self_check.py show a reference writer)",
        schema="{item, px_per_mm, size_px:[w,h], blocks:{<block id>:[{ch, font, weight, em_mm, ox_mm, baseline_mm, rot_deg, emb_mm}, ...]}}: ONE ENTRY PER CHARACTER OF THE APPROVED STRING, SPACES INCLUDED, IN ORDER. "
               "em_mm: the em of the glyph as drawn (mm, x the glyph's own size jitter); ox_mm: the pen origin from the item's left edge; baseline_mm: up from the item's bottom edge (the hand jitter included); rot_deg: counter-clockwise about the pen origin plus half the advance, on the baseline; emb_mm: the stroke added to the font's own (a felt pen), never over 0.6.",
        rule="The checker re-renders every glyph from the manifest and reads the pixels in the glyph's own cell. A manifest that is not the approved string, or whose glyphs lie outside the block's envelope, fails before any pixel is read. A MISSING, EMPTY OR UNREADABLE <ITEM>.glyphs.json FAILS .words and .glyphs (and the square estimate, which then reads the layout): the reader reports the failure and never crashes.",
        envelope=dict(print=dict(ox_mm=0.6, baseline_mm=0.5, rot_deg=0.1, em_frac=0.01, emb_mm=0.2),
                      hand="the block's hand style: baseline within 3.5 sd + 0.6 mm, rotation within 3.5 sd, size within 3.5 sd of 1, origin within 6 mm of the layout at the first glyph and within 6 mm + 5 per cent of the distance along the line, emb_mm within 0.6")),
    glyph_gate=dict(F_min=gl.F_MIN, dilation_mm=0.5, sep_gate=gl.SEP_GATE, n_min_px=gl.N_MIN, tol_px=gl.TOL_PX, alternatives="A-Z a-z 0-9 £ . , ' ’ - — – & · ? : ! (the font's own glyphs only)",
                    twins="shape twins (I and l, ' and ’, and any pair differing by under 0.03 mm2 at 24 px/mm) and a glyph that is its own mirror are listed and not scored",
                    why="see glyphlib.py's docstring and the disagreement 'the glyph check's margin'"),
    placed_street="PLACE.built: the builder writes placed_decals.json (item, surface, centre u and z or street x, rot_deg, scale); each decal lies within 20 mm of the placement's centre and 0.3 degrees of its rot_deg, and its largest block, read in a render of the surface at 1 px per mm after turning the decal back by rot_deg, passes the glyph check.",
)
FIXINGS = dict(
    tape_tab=dict(kind="a tab of yellowed adhesive tape", length_mm=38, width_mm=16, angle_deg=40, centre_in_mm=[12, 12], from_corner="top-left", rgb=[196, 164, 84], opacity=0.85, lifting_edge_mm=3,
                  note="lies across the corner on the 40-degree diagonal, centre 12 mm in from the top edge and 12 mm in from the left edge; part of it passes the card's edge. THE CUE of every taped or stuck hand card (K05, K06c, K07a-d, K09a-f, SA01-SA15): this ONE tab at the top-LEFT, nothing on the right half. (A sheet taped by its four corners, as the A3 notices are, carries four such tabs and no cue is needed: they are printed or photocopied, not hand-lettered.)"),
    string_sucker=dict(kind="a string loop and a rubber sucker", loop_mm=220, knot_mm=8, sucker_diameter_mm=22, sucker_centre_in_mm=[14, 14], from_corner="top-left", sucker_rgb=[150, 150, 146], sucker_opacity=0.90, string_rgb=[236, 232, 220],
                       note="THE CUE of the string-hung hand cards (K01, K06a): the knot and the sucker at the top-LEFT, the loop rising from them past the card's top edge; nothing on the right half"),
    four_tabs=dict(kind="four tabs of yellowed tape, one at each corner of an A3 or A4 sheet", length_mm=38, width_mm=16, angle_deg=40, rgb=[196, 164, 84], opacity=0.85),
    cue_patch_mm=25,
)
PLACEHOLDER_RULE = dict(
    rule="A placement whose item carries a proposed (unminted) name in a block of cap 10 mm or more is HELD: held_until_minted true, `names` listing the names. G.page.placeholders fails while any held placement is in the built street and any of its names lacks a DECISIONS.md line of the form '- ... MINTED: <NAME> ...'.",
    why="the 3 October ruling: placeholders never reach his page; whole street frames do; from across the street an agent's name at 52 mm capitals is about 8 px a capital at 8 m",
    default_street="carries only items that read naturally without an unminted name: P02 and P03 say STAND TOGETHER, D01 says LIVE MUSIC, M01 needs no name, L02 and L03n have no agent. The NAMELESS bills that would read as stand-ins (T01 to T03 'A NEW THRILLER' / 'A NEW COMEDY', W01 with no ring names and no hall) are HELD like the named versions (-named, L01, L03, B01, G01, G02): built only once the town mints the names the named twin carries (second review, fault 3).",
    allowed_unheld="proposed names under the 10 mm line stay: the 2.4 mm imprints (QUAY PRINT, the campaign, the publisher), the 3.6 to 6 mm campaign lines on P04 to P06")

UNPLACED_WHY = {
    "HC1": "the Harbour Board's case belongs by the dock office (brand bible; hook-cast harbour_office): not built",
    "FC1": "the timetable board belongs at each ramp (brand bible): not built",
    "H03": "pinned in HC1", "H04": "pinned in HC1", "H05": "pinned in HC1", "F01": "on FC1", "F02": "under F01 on FC1",
    "K02": "the newsagent never closes at midday (hook-cast 6 to 17.30) and Hal's shop is not on the built street",
    "B01": "held (THE DRILL HALL); a spare for the town", "G01": "held (WHITEWELL); a national four-sheet belongs in a contractor's panel",
    "G02": "held (QUAYSIDE)", "T01": "held: a nameless stand-in, with T01-named", "T03": "held: a nameless stand-in, with T03-named", "T01s": "the strip of T01, which is not placed",
    "P01": "held: the quay gable is bare; P01 was the proof wall's poll-tax bill (a spare template for the town)",
    "P04": "a spare sheet for the town (the advice evening)", "C01b": "a slot filler: the simulation's other appeals", "C01c": "a slot filler",
    "K03b": "the CLOSED face of K03a, shown when the shop is shut", "L01": "held (the agent's name); disagrees with the fascia target", "L03": "held (the agent's name)",
    "K01": "for a shop that shuts for lunch: none on the built street does (hook-cast hours)", "H01": "a gate or wall of the docks: not built",
    "S02n": "a kit plate: no street plate on the yard entrance", "S02d": "a kit plate", "S03n": "a kit plate", "S03d": "a kit plate", "S01d": "a variant of S01n",
}


def second_try_answers():
    return [
        dict(fault=1, short="the checks could not see a wrong word, date or price in the pixels",
             answer="ITEM.glyphs reads one glyph at a time in its own cell (glyphlib.py, self_check.py group 12): F >= 0.85 at 0.5 mm against the glyph re-rendered from the manifest, and SEP >= 0.70 against every other glyph of the font and its own mirror, on the pixels where they differ; each item's pixel scale is chosen so that every non-twin pair differs by at least 8 pixels. Every wrong render the reviewer built (a changed date, a changed price or time, TEA for ALE, Teas for Beer, LUNCH for BINGO, a mirrored hand card, a misspelt plate) FAILS; a true render, jittered hand renders (20 seeds each of K01 and SA06, 8 each of K07a, K09a and SA15) and a true render turned 1.2 degrees and read in the placed street PASS. The reviewer's own harness, run unchanged, now also fails every PRINT wrong render (the line score includes the worst glyph); hand lines need the renderer's manifest, which is the review's own amendment (a). ART.eye, PLACE.built, ITEM.square and the square-on rule are added. (After the second review, by Jafar's ruling of 9 October: the true jittered renders of all 29 hand cards, 20 seeds each, and a true render of every item pass all pixel checks; ITEM.clean reads ink outside every block; a missing manifest fails.)"),
        dict(fault=2, short="unminted placeholder names were the street's default dressing",
             answer="the default street carries nameless items only where they read naturally (STAND TOGETHER, LIVE MUSIC, no agent); the named versions are -named variants and L01, L03, B01, G01, G02, each held_until_minted with its names; their placements are held twins; G.page.placeholders added and tested. (After the second review: the nameless T02, T03 and W01, which read as stand-ins, are held like their twins.)"),
        dict(fault=3, short="the WEIGHHOUSE LANE plate named the yard entrance",
             answer="the S02d placement and every 'proposed because canon does not name the opening' line are deleted; S02 is a kit plate like S03; the side opening is the yard entrance and carries no plate; C03 keeps DIVERSION VIA WEIGHHOUSE LANE."),
        dict(fault=4, short="the paste plan was far denser than the asset plan and covered the gable the sheet shows bare",
             answer="at most eight fly-posters and four poll-tax bills (G.place.paper; the default street carries 5 and 3). First answer: SF1 carried one layer of three bills with the 75 mm cast-iron downpipe at u 0.30 and paper 150 mm clear. After the second review, by Jafar's ruling of 9 October, the gable is BARE as the Hook sheet shows it: the three bills, the strip and the second plate are held placements (G.place.gable: no paper and no plate on SF1; the downpipe, the render patch and the damp foot stay as fixtures). SF2 carries M01, P03, P02, J01, C02 and C01a; the west pier W1.0 (the scene's poster slot) takes M01 at class B; P02 is also an A3 window bill in the bay-1 window at x 12.3 (scale 0.585, top 1.90 m); no sticker on the gable, no bill on the other piers."),
        dict(fault=5, short="two targets gave two letting boards, and C02 used the wrong address",
             answer="L02 is the fascia target's board exactly (900 x 450, TO LET, Libre Franklin 800 cap 130, vinyl red, no agent, no number) and is the default on SF5; L01 (1200 x 450 with an agent) is a held variant that would need the fascia target changed in the same batch; G.letting.mount compares size, font, weight, cap and colour with the fascia target; C02 reads 'Change of use of the ground floor, 7 Quay Street,'."),
        dict(fault=6, short="two proposed names collided with real ones",
             answer="TIGER JIM LARKIN is TED HOLROYD (first BIG TED HOLROYD, withdrawn after the second review: 'Big Ted' is the bear of the BBC children's programme Play School; BIG TED is in real_marks) and THE SEA WOLF is THE HARPOONER (and MAD MAURICE and THE BARON, a television series, are SPANNER SMITH and THE STEVEDORE), all held and listed for the town to check; LARKIN, SEA WOLF and SEA WOLVES are in forbidden_patterns.real_marks, with the real wrestlers, soap powders, cinema chains and campaigns the probe listed."),
        dict(fault=7, short="period wording and process read as the wrong decade or country",
             answer="D01 says SEQUENCE; W01 says PROFESSIONAL (Oswald 700 fitted to the 428 mm measure); the Tivoli's weeks start on Thursday (T01 from THURSDAY 18 OCTOBER, T02 from THURSDAY 25 OCTOBER, T03 four lines); the venue and date are a separate letterpress strip (T01s, T02s, 1016 x 90 mm, black on white, own class, 0.25 degrees off the quad's square) and the litho's top band is blank; J01 and D01 are photocopy A3 notices in shop windows; H03 reads NOTICE TO MARINERS."),
        dict(fault=8, short="no street date, so the age classes contradicted each other",
             answer="calendar.street_date is Monday 29 October 1990; T03 and D01 are class B, J01 class B everywhere; G.dates.age checks every placed dated item against its class's days (event - 42 <= street date - age <= event; a notice at or after its date) and is tested on the first try's contradiction."),
        dict(fault=9, short="the mirror guard of the 29 hand cards contradicted their fixings",
             answer="every SA card is taped (no pins); each hand card has ONE cue matching its fixing and nothing on the right half: one tab of yellowed tape across the top-LEFT corner (K05, K06c, K07a-d, K09a-f, SA01-SA15) or the knot and sucker at the top-LEFT (K01, K06a); every crease, tear and pin-hole cue is gone; G.mirror.cues reads the 25 mm top-left and top-right patches only and is tested on all 29 cards, true and mirrored; ITEM.glyphs also fails a mirrored hand card."),
        dict(fault=10, short="placements contradicted the brand bible and the items' own words",
             answer="HC1 and FC1 are not placed (FC1 is a painted timber board, 600 x 800, F01 over F02, no glazing); C01a is inside the empty unit's glass (SF2, u 0.30, z 1.30, four tape tabs); K02 is unplaced; K05's bottom is 1.42 m (not 1.38: the fascia target's vinyl lettering on the same glass tops out at 1.385) at u 0.64, beside the assumed hours plate."),
        dict(fault=11, short="parts a script could not make from target.json alone",
             answer="K04: ring 7 mm and a 7 mm bar at 45 degrees, polygon given; G02: a white ring 16 mm wide at 0.70 of the disc's radius; K02: ticks 2 x 8, hour hand 30 x 5, minute hand 40 x 4 (buff card), a 6 mm brass fastener; plates: 10 degrees of draft and a 0.8 mm top radius on raised letters and border, pressed aluminium rolled edge radius 3 mm, enamel rolled edge 6 mm, cast edge 6 mm with a 2 mm arris; HC1: rails 46 x 60 with a 4 mm chamfer, glass 4 mm in a 10 x 10 mm bead; also K03's hole and chain, and every enamel board's corner and roll radii."),
        dict(fault=12, short="the ferry stranded its one boat",
             answer="the far-side column ends '9.45 10.45 / LAST CROSSING 11.15', so the boat is at the Hook at 11.30 each night and the street's 'last crossing's at eleven' holds from the Hook; G.ferry.schedule simulates the one vessel from the printed blocks and checks that each day ends where the next day's first sailing leaves (Monday to Saturday, Sunday, Monday)."),
        dict(fault=13, short="name plates against the project's own note",
             answer="the default and placed variant is `n` (name only); `d` stays a variant; S01p, S02p, S03p and MR1 are deleted; QUAY STREET is cast aluminium with letters and border raised 3 mm, painted white with black letters, the paint flaking at the raised edges; every plate is at least 200 mm deep; the relief, draft and edge radii are in numbers and G.plates.make checks the lettering against them (Marcellus SC's thinnest stroke at 90 mm capitals is thick enough for a cast or pressed letter)."),
    ]


def fixes_after_second_review():
    return [
        dict(fix=1, short="the checks failed correct items and never read ink outside the blocks",
             answer="ITEM.square finds the angle against the render of the item's own glyph manifest (jitter included) and reports 0 unless F at the best angle beats F at 0 degrees by 0.02: exactly square P05, K04, K03a, K03b, K02, K08 and P06 read 0 and every jittered hand card reads 0; ONE tolerance, 0.3 degrees, in target.json and TARGET.md. "
                    "The glyph reader gives a pixel a neighbour's ink explains and the glyph's does not to the neighbour, even where hand-lettered glyphs touch (SA01 and SA03 had failed 11 and 15 of 20 true seeds at 8 px/mm; both now pass 20 of 20), reads big capitals at a reduced scale with the same area rule that draws its reference, and counts a space's ink only where it lies beyond 0.6 mm of every glyph (T01-named's true render passes). "
                    "glyphlib.needed_ppm measures each hand pair over glyphs jittered to 3.5 sd of the block's hand style (size and rotation, four corners). ITEM.clean (new, per item): the ink-coloured pixels outside every block's glyph window, the item's own shapes, the cue patch and the art slots total at most 2 mm2; the reviewer's four planted lines (K01 BINGO TONIGHT, SA11 Babysitter, evenings., L02 ARMITAGE & STOBBS, C02 BETTING SHOP) and D01 + LICENSED BAR fail it. A missing or unreadable <ITEM>.glyphs.json fails .words and .glyphs and never crashes the reader (render contract). Group 12 reads a true render of EVERY item and 20 jittered seeds of all 29 hand cards through .pos, .mask, .glyphs, .square and .clean; any failure is a self-check failure."),
        dict(fix=2, short="the nameless defaults read as stand-ins",
             answer="T01, T02, T03 and W01 (the nameless Tivoli quads and programme and the wrestling bill with no ring names and no hall) are HELD like their named twins (item.held, stand_in_of, waits_for): their placements are held_until_minted with the names the twin carries, so G.page.placeholders keeps them off the built street until DECISIONS.md mints the films, the hall and the ring names. "
                    "Pier W1.0 (the scene's poster slot) takes M01 at class B, a bill that needs no unminted name. G.place.paper is 'at most 8 fly-posters and 4 poll-tax bills' (the default street carries 5 and 3)."),
        dict(fix=3, short="BIG TED HOLROYD collides with a real children's programme",
             answer="TED HOLROYD on the named wrestling bill, in PROPOSED and in every check; BIG TED is in forbidden_patterns.real_marks ('Big Ted' is the bear of the BBC children's programme Play School)."),
        dict(fix=4, short="the quay gable is bare, as the Hook sheet shows it",
             answer="P01, W01, T02 with its strip T02s and the second QUAY STREET plate (the five proof_wall placements) are held, not in the default street; the west corner pier keeps its plate at x 20.47. G.place.gable is now 'no paper and no plate on SF1' and still checks the downpipe, the render patch and the damp foot as fixtures; the check that demanded exactly three gable bills and the one that demanded exactly 8 and 4 are reworded."),
    ]


def font_decisions():
    return [
        dict(font="Libre Franklin", plan="not on asset-plan note 4's table (Helvetica and Arial stand-ins: Arimo, Inter, Archivo, Hanken Grotesk, Work Sans)", why="the fascia target (same batch) already sets the letting board's TO LET in Libre Franklin 800; this target compares L02 with it, and Libre Franklin is in production/fonts; Franklin Gothic is also the right 1990 newsagent and notice face",
             decisions_line="9 Oct 2026 | Libre Franklin (OFL, already in production/fonts) is used for notice, card and bill copy and the letting board's TO LET, though not on asset-plan note 4's font table | the fascia target already does; Franklin Gothic is the period face | the cloud's target writer | production/cloud-week/targets/posters-boards-plates/TARGET.md"),
        dict(font="Patrick Hand", plan="not on the table (Caveat Brush, Kalam, Gochi Hand are the 'hand-marked tickets and bills' faces)", why="Patrick Hand is a neat adult print capital with plain figures, which is what a shopkeeper's felt-pen ticket and a ballpoint record card are; Kalam and Caveat Brush are slanted and read as script, and the reviewer notes they look more like a felt marker; Patrick Hand is already in production/fonts. Judgement: the town may swap the hand face without touching the checks (they read whatever face the manifest names)",
             decisions_line="9 Oct 2026 | Patrick Hand (OFL, already in production/fonts) is the hand-lettering face for felt-pen cards and ballpoint record cards, though the asset plan's table names Caveat Brush, Kalam and Gochi Hand | neat print capitals and plain figures read as a shopkeeper's felt pen; the table's faces are scripts | the cloud's target writer | production/cloud-week/targets/posters-boards-plates/TARGET.md"),
        dict(font="Libre Baskerville and Josefin Sans", plan="not on the table", why="REMOVED in the second try: the typeset notices use Old Standard TT Regular and Bold (the table's 'Old Standard'), and the Tivoli's strip and programme use Oswald (the table's 'the Tivoli's letters'); Abril Fatface, defined but never used, is removed too", decisions_line=None),
    ]


WEAR_OF = {}


def wear_table_for(it):
    k = it["id"]
    base = k.replace("-named", "")
    if base in ("P01", "P02", "P03", "W01", "B01", "M01", "G01", "G02", "T01", "T02", "T03", "T01s", "T02s", "F01", "F02"):
        return "bill_pasted", None
    if base in ("J01", "D01", "P04"):
        return "glass_bill", None
    if base in ("C01a", "C01b", "C01c", "C02", "C03", "H03", "H04", "H05"):
        return "notice_sleeve", None
    if base.startswith("SA"):
        return "card_ballpoint", ["B", "C"]
    if base in ("P05", "P06", "K04", "K06b"):
        return "sticker", ["B", "C", "D"]
    if base in ("K03a", "K03b", "K08"):
        return "card_felt", ["A", "B", "C"]
    if base.startswith("K"):
        return "card_felt", ["A", "B", "C"]
    if base in ("H01", "H02"):
        return "enamel_plate", ["B", "D"]
    if base.startswith("S01"):
        return "cast_aluminium_plate", ["C", "D"]
    if base.startswith("S0"):
        return "pressed_plate", ["C", "D"]
    if base.startswith("L"):
        return "letting_board", ["B", "C", "D"]
    return "bill_pasted", None


def main():
    items, by_id, cases, placements = build()
    sp = shop_placements(by_id)
    placements = finish_held(placements + sp + held_alternates(sp, by_id), by_id)
    cb = card_board(by_id)
    placements.append(dict(item="SB1", surface="SHOP", shop="newsagent", where="glass", u_m=cb["glass_u_m"], z_bottom_m=cb["z_bottom_m"], w_m=cb["area_mm"][0] / 1000.0,
                           h_m=cb["area_mm"][1] / 1000.0, rot_deg=0.0, layer=1, age_class="B", inside=True, note="the card board: 15 cards, see card_board"))
    wt = wear_tables()
    for it in items:
        k = it["id"]
        tbl, default_classes = wear_table_for(it)
        cl = sorted({p["age_class"] for p in placements if p["item"] == k})
        it["wear"] = dict(table=tbl, classes=(cl or default_classes or ["B", "C"]))
    # which proposed names stand on which items
    prop = []
    for p in PROPOSED:
        q = dict(p)
        q["items"] = sorted(it["id"] for it in items if any(p["name"].lower() in b["text"].lower() for b in it["blocks"]))
        q["held_items"] = sorted(it["id"] for it in items if p["name"] in it.get("held_names", []))
        q["max_cap_mm"] = max([b["cap_mm"] for it in items for b in it["blocks"] if p["name"].lower() in b["text"].lower()] or [0])
        prop.append(q)
    fonts = {}
    for k, v in FONTS.items():
        d = dict(v)
        d["ofl"] = ofl_info(v["dir"])
        d["cap_ratio_700"] = round(cap_ratio(k, 700), 3)
        d["path_hint"] = ("production/fonts/" + v["file"]) if v["in_repo"] else "NOT in production/fonts: the builder adds it with its OFL.txt (fetch: self_check.py --fetch-fonts DIR)"
        d["coverage"] = {ch: glyph_ok(k, ch) for ch in "£’·—–&.,?:0123456789"}
        fonts[k] = d
    words = sorted({norm(b["text"]) for it in items for b in it["blocks"] if not b.get("ghost")})
    ghosts = sorted({norm(b["text"]) for it in items for b in it["blocks"] if b.get("ghost")})
    tokens = sorted({t for w in words + ghosts for t in re.findall(r"[A-Za-z0-9£'&.\-]+", w)})
    items_out = []
    hand_key = {id(HAND_FELT): "felt", id(HAND_FELT_FINE): "felt_fine", id(HAND_BALL): "ballpoint"}
    for it in items:
        o = dict(it)
        if it["kind"] in ("plate", "board"):
            o["stock"] = None
        o["words"] = sorted({norm(b["text"]) for b in it["blocks"]})
        nb = []
        for b in it["blocks"]:
            c = dict(b)
            c.pop("ink_colour", None)
            c.pop("ground", None)
            c["hand"] = hand_key.get(id(b["hand"])) if b.get("hand") else None
            c["contrast"] = {k: v for k, v in b["contrast"].items()}
            c["tol"] = block_tols(b, it["px_per_mm"])
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
    default_pl = [p for p in placements if not p.get("held")]
    placed_ids = {p["item"] for p in placements}
    on_board = {c["item"] for c in cb["cards"]}
    unplaced = {}
    for it in items:
        k = it["id"]
        if k in placed_ids:
            continue
        if k in UNPLACED_WHY:
            unplaced[k] = UNPLACED_WHY[k]
        elif k in on_board:
            unplaced[k] = "on the newsagent's card board SB1 (card_board)"
        elif it.get("named_of"):
            unplaced[k] = "the named twin of %s: held (its placements are the held twins)" % it["named_of"]
        else:
            unplaced[k] = "not placed by default"
    for c in cases:
        unplaced[c["id"]] = c["not_placed"]
    n_held = sum(1 for p in placements if p.get("held"))
    target = dict(
        schema="ledger.cloud-week-42.target.posters-boards-plates/2", family="posters-boards-plates",
        status="SECOND AND LAST TRY, 9 October 2026 (cloud week 42), after TARGET-REVIEW.md (FAIL, 13 faults), with the four fixes of the second review applied by Jafar's ruling of 9 October and NOT re-reviewed (fixes_after_second_review); unit 4.2, 4.3 and 4.4 build from this file alone. self_check below is written by self_check.py.",
        summary_line=("%d sheets, cards, boards and plates for Quay Street's paper and small boards: the poll-tax set, the chapel hall's two photocopied notices, the fights, the market, the Tivoli's quads, strips and programme "
                      "(the named variants held, and the nameless ones too where they would read as stand-ins), 7 ferry and Harbour Board sheets, 5 police and council notices, 35 shop-window and newsagent cards, 5 letting boards (the default is the fascia target's), "
                      "6 street name plates (name only by default); the default street carries no unminted name and a BARE quay gable: %d placements (%d default, %d held), at most 8 fly-posters and 4 poll-tax bills as the asset plan says (5 and 3 carried), "
                      "the street date Monday 29 October 1990, every item read glyph by glyph in its own pixels, %d checks." % (len(items), len(placements), len(default_pl), n_held, len(checks))),
        units=dict(mm="every item's own frame: x from the viewer's LEFT edge as seen in the game, y UP from the bottom edge; baseline_mm is measured up from the bottom edge",
                   m="surfaces: u from the surface's viewer's-left edge, z up from the pavement; street x along the street (0 south)", colour="sRGB 0..255; contrast is WCAG; dE is CIE76 on Lab D65",
                   px_per_mm="each item's own (items[].px_per_mm, 2 to 16): the scale at which every glyph can be told from every other"),
        kinds=dict(Read="printed in a source file", Scaled="measured off a drawing or the game's own files", Photo="measured on a photograph today", Derived="computed from the above",
                   Judgement="the writer's, overturned by a better source", Lead="a search summary: never a number"),
        axis=dict(rule="as the fascia target: the game mirrors the recipe, so low street x is on the viewer's RIGHT looking at the east parade and on the viewer's LEFT looking at the west block; every item's x runs from the viewer's left; the gable SF1 is read looking +x with the front corner at the viewer's left",
                  evidence=["production/cloud-week/targets/fascia-signs/TARGET.md section 2", "production/previews/morning-hook-day-2026-10-08.jpg: the quay gable is the big brick wall at the right of the hook frame"]),
        calendar=dict(year=YEAR, street_date="Monday 29 October 1990", street_date_iso="1990-10-29",
                      window="1 October to 30 November 1990 by default; the dated bills' weekdays are computed, so any date in 1988 to 1992 can be set with date_slot rules",
                      note="1 October 1990 was a Monday. 29 October is a day every placed dated item allows (G.dates.age; the held proof wall's P01 and T02 allow it too: the meeting of Thursday 25 October is four days gone, the film started on Thursday 25). GMT began on Sunday 28 October. Every printed weekday is computed from datetime.date and checked by G.dates; G.dates.age checks each placed item's age class against the street date."),
        formats={k: dict(v) for k, v in FORMATS.items()},
        fonts=fonts, font_decisions=font_decisions(), palette=palette, age_classes=ages,
        age_rules=dict(note="Four classes by days on the wall (age_classes[class].days). Colour fade by ink: f = 1 - exp(-t / tau), tau in days (palette.inks, palette.stocks); paper yellows 30 per cent of YELLOWED at class D; grime film GRIME mixed 0, 5, 12, 22 per cent over the paper and 35 per cent of that over ink. Order of fastness (Judgement): fluorescent stock, then red, then blue, then black, then photocopier toner.",
                       paper_wear=dict(wrinkle=dict(amplitude_mm=[0.4, 1.5], wavelength_mm=[12, 40], note="wallpaper-paste cockling in the height map, stronger along the paste's brush direction (vertical)"),
                                       edge_lift=dict(corners=[0, 3], radius_mm=[15, 60], class_A=0, class_D=3), tears=dict(count=[0, 4], width_mm=[20, 140], from_edge=True),
                                       rain_runs=dict(count_per_m=[2, 8], length_mm=[10, 60], width_mm=[0.4, 1.5], opacity=[0.15, 0.4], direction="down from the top edge and from any lifted corner", ink="red and dye inks run first"),
                                       paste_halo=dict(width_mm=[2, 10], colour=[168, 148, 110], opacity=[0.15, 0.4], note="class C and D only, round the edges where a bill is lifting"),
                                       glue_stain=dict(note="dark (60,50,40) 0.25 opacity patches where a later bill has pasted over a lower one's tear"),
                                       loss=dict(class_B=[0, 0.05], class_C=[0.03, 0.2], class_D=[0.3, 0.6], note="share of the sheet lost: bottom corners and lower third first"),
                                       wet=dict(darken=0.12, saturation=1.1, note="a runtime hint for the material: bills darken and saturate when the wall is wet; roughness drops to 0.55 for a shower"),
                                       skew_deg=[-1.5, 1.5], skew_note="the PLACEMENT's rot_deg only: every texture is square-on",
                                       overposting=dict(layers=[1, 3], note="each newer bill may cover up to 55 per cent of an older one; edges overlap 0 to 40 mm; the newer bill lies flatter; NOT used on the quay gable's one layer"))),
        render_contract=RENDER_CONTRACT, fixings=FIXINGS, placeholders=PLACEHOLDER_RULE,
        processes=PROCESSES, surfaces=SURFACES, west_piers=west_piers(), shops=shop_geometry(), hours_plate=HOURS_PLATE, card_board=cb, wear_tables=wt, placements=placements, unplaced=unplaced, cases=cases,
        photo=dict(P1=CASE_PHOTO, ratios=CASE_RATIOS, preview=["production/previews/cloud-week/refs/posters-boards-plates/P1-urban-street-01-notice-case.jpg",
                                                              "production/previews/cloud-week/refs/posters-boards-plates/P1-urban-street-01-notice-case-target-on-photo.jpg"]),
        items=items_out, approved_words=words, approved_word_parts=tokens, ghost_words=ghosts, proposed_names=prop,
        forbidden_patterns=FORBIDDEN_WORDS, checks=checks, disagreements_photographs_win=DISAGREEMENTS, sources=SOURCES, unreached=UNREACHED,
        would_read_when_network_opens=WOULD_READ, could_not_settle=COULD_NOT_SETTLE, second_try=second_try_answers(), fixes_after_second_review=fixes_after_second_review(),
        evidence_split=dict(
            photographs_measured_today="the vertical proportions of one glazed notice case (P1); nothing else",
            earlier_notes="the 1990 mix of print (Letraset, photocopy, two-colour), the Kindersley recommendation of 1952, the 1 October 1990 winter timetable date, cod at about 2.60 a lb, the Harbour Board's blue and white enamel, the ferry's pasted winter sheets, the pound-and-pence prices of 1990 (all cited from the repository, not re-measured)",
            judgement="every size, colour, layout, wording, price, ageing number and placement not listed above"),
        self_check=None)
    target["hand_styles"] = dict(felt=HAND_FELT, felt_fine=HAND_FELT_FINE, ballpoint=HAND_BALL)
    write_json(target)
    print("wrote target.json", len(items), "items", len(checks), "checks", len(placements), "placements")


if __name__ == "__main__":
    main()
