"""Number plates for the parked cars of 1990, as data and geometry, pure Python.

Written by the lane session, 17 November 2026. It needs no Blender and no
network: it invents 1990-style registrations from a seed, lays the characters
out on the plate to the government's V796 spacing, gives each character a
blocky stroke shape, and writes a plate as SVG (for a quick look) and as JSON
(for the Blender side to read later).

Facts: production/research/lane/HATCH-CLASS-AND-PLATES-2026-11-17.md section 3.
  - V796 Group 2 characters (cars first registered 1973 to 2001): 79 mm high,
    57 mm wide except 1 and I, stroke 14 mm, 11 mm between characters, 33 mm
    between groups, margins at least 11 mm.
  - Standard plate 520 x 111 mm. Reflective: white front, yellow rear.
  - Year letters never used: I, O, Q, U, Z. H from August 1990, G before.
  - 1990 format is the prefix style: year letter, 1 to 3 digits, space,
    three letters, e.g. "G123 ABC".

Every registration here is INVENTED. The real DVLA area-code mapping (which
letters belonged to which local office) is deliberately not modelled: the
plates should read as plausible, not be traceable to a real place or car.

Known gaps:
  - Suffix-era plates (ABC 123X, before August 1983) are NOT generated, though
    many cars on a 1990 street still carried them. On the lane list, research
    first.
  - H plates need a game date on or after 1 August 1990 (or allow_h=True):
    canon fixes no month, so by default no H. The exact day is UNVERIFIED.

Real-plate lookalikes: every plate is a format-valid British registration, so
some real car once carried it. To cut plates that read as cherished or joke
plates, numbers start at 21, the serial never has three equal letters (AAA),
69 and 666 are refused, and a blocklist of words is refused.

The character shapes are a PLACEHOLDER font for silhouette and tests only. The
final plate texture is drawn from a licensed or self-made font later.

Units: millimetres. x from the plate's left edge, y DOWN from its top edge
(the same as SVG), so the JSON boxes can be drawn straight onto a texture.
"""
import argparse
import datetime
import json
import random
import re
import sys
import xml.etree.ElementTree as ET

# V796 Group 2 spacing, millimetres.
CHAR_HEIGHT = 79.0
CHAR_WIDTH = 57.0
STROKE = 14.0
GAP_CHAR = 11.0
GAP_GROUP = 33.0
MIN_MARGIN = 11.0

# The narrow "1". V796 says 1 and I are narrower than 57 but the research note
# does not give the figure: 25 mm here is a guess (one stroke plus its flag).
NARROW_WIDTHS = {"1": 25.0, "I": 25.0}

PLATE_STANDARD = (520.0, 111.0)

# Plate colours. White front, yellow rear (V796). The exact yellow of the
# reflective sheet is not in the research note: this hex is a stand-in.
PLATE_COLOURS = {"front": "#ffffff", "rear": "#f6c800"}
INK = "#000000"

# Year letters a car parked in 1990 might carry: prefix era A (1983) to H
# (from August 1990). Weighted toward recent cars, as a street would be; H is
# light because it only began in August, and is used only when the game date
# allows it (see year_weights). Never I, O, Q, U or Z.
YEAR_WEIGHTS = {"A": 4, "B": 5, "C": 6, "D": 7, "E": 8, "F": 9, "G": 10, "H": 3}
YEAR_LETTERS_NEVER = set("IOQUZ")
# H plates began in August 1990 (carreg.co.uk); the day is UNVERIFIED.
H_START = datetime.date(1990, 8, 1)

# Numbers 1 to 20 were often held back for sale and read as cherished plates,
# so numbers start at 21. 69 and 666 read as jokes.
NUMBER_MIN, NUMBER_MAX = 21, 999
NUMBERS_REFUSED = frozenset({69, 666})

# Letters for the three-letter group. I, Q and Z are left out anywhere: that is
# safer than modelling which positions allowed them.
SERIAL_LETTERS = "ABCDEFGHJKLMNOPRSTUVWXY"

# Three-letter groups that must never appear: rude words, slurs, real words
# that would read as a joke or a vanity plate, drink and betting words (canon
# has no alcohol or gambling), drugs, and paramilitary or political initials
# that were sharp in 1990 Britain. Three letters only, since serials are three.
# Add to it as found.
BLOCKLIST = frozenset("""
ASS ARS BUM BOG NOB KNB TIT POO WEE PEE SOD FUK FCK FKU SHT CNT CUM SEX
XXX KKK DIE DED GOD GUN WAR PIG COP FAT POX SOB WTF GAY JEW NUN HAG TWT YOB
WOG FAG FGT PAK WOP POM NIG
ALE GIN RUM BAR PUB BET WIN ODD KEG SOT TOT VAT
LSD POT DOP
UDA UVF IRA BNP KGB PRK
""".split())
assert all(len(w) == 3 for w in BLOCKLIST)

PLATE_RE = re.compile(r"^[A-HJ-NPR-TV-Y][1-9][0-9]{0,2} [A-HJ-PR-Y]{3}$")


class PlateFitError(ValueError):
    """The registration does not fit the plate with V796 margins."""


# ---------------------------------------------------------------------------
# Registrations


def year_weights(game_date=None, allow_h=False):
    """The year letters usable on the given game date, with their weights.

    H only when game_date is on or after 1 August 1990, or allow_h is True.
    With no date, no H: canon fixes no month for 1990.
    """
    if isinstance(game_date, datetime.datetime):
        game_date = game_date.date()
    h_ok = allow_h or (game_date is not None and game_date >= H_START)
    return {k: v for k, v in YEAR_WEIGHTS.items() if k != "H" or h_ok}


def capacity(weights=YEAR_WEIGHTS):
    """Rough count of possible plates (before the blocklist and repeats)."""
    numbers = NUMBER_MAX - NUMBER_MIN + 1 - len(NUMBERS_REFUSED)
    return len(weights) * numbers * len(SERIAL_LETTERS) ** 3


def _random_registration(rng, weights):
    letters = list(weights)
    year = rng.choices(letters, weights=[weights[k] for k in letters])[0]
    number = rng.randint(NUMBER_MIN, NUMBER_MAX)
    serial = "".join(rng.choice(SERIAL_LETTERS) for _ in range(3))
    return f"{year}{number} {serial}"


def is_valid_registration(reg):
    """True if reg has the 1990 prefix shape and none of the banned letters."""
    if not isinstance(reg, str) or not PLATE_RE.match(reg):
        return False
    number = int(reg.split(" ")[0][1:])
    if number < NUMBER_MIN or number in NUMBERS_REFUSED:
        return False
    if reg[0] in YEAR_LETTERS_NEVER or reg[0] not in YEAR_WEIGHTS:
        return False
    serial = reg.split(" ")[1]
    if serial in BLOCKLIST or any(c not in SERIAL_LETTERS for c in serial):
        return False
    if serial[0] == serial[1] == serial[2]:
        return False
    return True


def generate_registrations(seed, count, game_date=None, allow_h=False):
    """count unique invented 1990 registrations. Same seed, same list.

    Raises ValueError for a negative count, a seed of None (not repeatable),
    or a count over half of what exists (the search would crawl or hang).
    """
    if seed is None:
        raise ValueError("seed must be given: None is not repeatable")
    weights = year_weights(game_date, allow_h)
    if count < 0 or count > capacity(weights) // 2:
        raise ValueError(f"count {count} out of range 0 to {capacity(weights) // 2}")
    rng = random.Random(seed)
    seen = set()
    out = []
    attempts = 0
    while len(out) < count:
        attempts += 1
        if attempts > count * 50 + 1000:
            raise RuntimeError("could not find enough unique registrations")
        reg = _random_registration(rng, weights)
        if reg in seen or not is_valid_registration(reg):
            continue
        seen.add(reg)
        out.append(reg)
    return out


# ---------------------------------------------------------------------------
# Layout


def char_width(ch):
    return NARROW_WIDTHS.get(ch, CHAR_WIDTH)


def text_width(reg):
    """Width of the characters and gaps in mm, without margins."""
    total = 0.0
    for gi, group in enumerate(reg.split(" ")):
        if gi:
            total += GAP_GROUP
        for ci, ch in enumerate(group):
            if ci:
                total += GAP_CHAR
            total += char_width(ch)
    return total


def layout(reg, plate_size=PLATE_STANDARD):
    """Each character's box on the plate: list of dicts char, x, y, w, h (mm).

    The text is centred both ways. Raises ValueError for an invalid or blocked
    registration, and PlateFitError if any margin would be under 11 mm.
    """
    if not is_valid_registration(reg):
        raise ValueError(f"{reg!r} is not a valid invented 1990 registration")
    pw, ph = plate_size
    tw = text_width(reg)
    mx = (pw - tw) / 2.0
    my = (ph - CHAR_HEIGHT) / 2.0
    if mx < MIN_MARGIN or my < MIN_MARGIN:
        raise PlateFitError(
            f"{reg!r} needs {tw:.0f} x {CHAR_HEIGHT:.0f} mm; on {pw:.0f} x {ph:.0f} "
            f"the margins are {mx:.1f} and {my:.1f} mm (need {MIN_MARGIN:.0f})")
    boxes = []
    x = mx
    for gi, group in enumerate(reg.split(" ")):
        if gi:
            x += GAP_GROUP - GAP_CHAR
        for ch in group:
            w = char_width(ch)
            boxes.append({"char": ch, "x": round(x, 3), "y": round(my, 3),
                          "w": w, "h": CHAR_HEIGHT})
            x += w + GAP_CHAR
    return boxes


# A full 1990 plate, e.g. "G123 ABC", is 7 characters in groups of 4 and 3:
# 7 x 57 + 5 x 11 + 33 = 487 mm, leaving 16.5 mm each side on 520. If every
# digit were a 1 it is narrower still. Checked here at import, so a change to
# the numbers above that breaks the fit fails loudly.
assert text_width("G888 ABC") == 487.0
assert (PLATE_STANDARD[0] - 487.0) / 2 >= MIN_MARGIN
assert (PLATE_STANDARD[1] - CHAR_HEIGHT) / 2 >= MIN_MARGIN


# ---------------------------------------------------------------------------
# Placeholder stroke font. Each glyph is a list of polylines: stroke centrelines
# in the character's own box, (0,0) top left, y down. Centrelines sit half a
# stroke (7 mm) inside the box, and the strokes are drawn with round ends and
# joins, so the ink stays inside the 57 x 79 box.

_H = STROKE / 2.0
L, R, C = _H, CHAR_WIDTH - _H, CHAR_WIDTH / 2.0
T, B, M = _H, CHAR_HEIGHT - _H, CHAR_HEIGHT / 2.0

GLYPHS = {
    "A": [[(L, B), (L, T), (R, T), (R, B)], [(L, M), (R, M)]],
    "B": [[(L, B), (L, T), (R - 8, T), (R - 8, M), (L, M)],
          [(L, M), (R, M), (R, B), (L, B)]],
    "C": [[(R, T), (L, T), (L, B), (R, B)]],
    "D": [[(L, T), (R - 12, T), (R, T + 12), (R, B - 12), (R - 12, B), (L, B), (L, T)]],
    "E": [[(R, T), (L, T), (L, B), (R, B)], [(L, M), (R - 8, M)]],
    "F": [[(R, T), (L, T), (L, B)], [(L, M), (R - 8, M)]],
    "G": [[(R, T), (L, T), (L, B), (R, B), (R, M), (C, M)]],
    "H": [[(L, T), (L, B)], [(R, T), (R, B)], [(L, M), (R, M)]],
    "J": [[(R, T), (R, B), (L, B), (L, M + 8)]],
    "K": [[(L, T), (L, B)], [(R, T), (L, M), (R, B)]],
    "L": [[(L, T), (L, B), (R, B)]],
    "M": [[(L, B), (L, T), (C, M), (R, T), (R, B)]],
    "N": [[(L, B), (L, T), (R, B), (R, T)]],
    "O": [[(L, T), (R, T), (R, B), (L, B), (L, T)]],
    "P": [[(L, B), (L, T), (R, T), (R, M), (L, M)]],
    "R": [[(L, B), (L, T), (R, T), (R, M), (L, M)], [(C, M), (R, B)]],
    "S": [[(R, T), (L, T), (L, M), (R, M), (R, B), (L, B)]],
    "T": [[(L, T), (R, T)], [(C, T), (C, B)]],
    "U": [[(L, T), (L, B), (R, B), (R, T)]],
    "V": [[(L, T), (C, B), (R, T)]],
    "W": [[(L, T), (L, B), (C, M), (R, B), (R, T)]],
    "X": [[(L, T), (R, B)], [(R, T), (L, B)]],
    "Y": [[(L, T), (C, M), (R, T)], [(C, M), (C, B)]],
    # 0 is O with a slash so the two can be told apart in tests and close up.
    "0": [[(L, T), (R, T), (R, B), (L, B), (L, T)], [(R, T + 10), (L, B - 10)]],
    # The narrow 1: one upright with a short flag, in a 25 mm box.
    "1": [[(_H, T + 10), (NARROW_WIDTHS["1"] - _H, T), (NARROW_WIDTHS["1"] - _H, B)]],
    "2": [[(L, T), (R, T), (R, M), (L, M), (L, B), (R, B)]],
    "3": [[(L, T), (R, T), (R, B), (L, B)], [(L + 10, M), (R, M)]],
    "4": [[(L, T), (L, M), (R, M)], [(R, T), (R, B)]],
    "5": [[(R, T), (L, T), (L, M), (R - 6, M), (R, M + 6), (R, B), (L, B)]],
    "6": [[(R, T), (L, T), (L, B), (R, B), (R, M), (L, M)]],
    "7": [[(L, T), (R, T), (R, B)]],
    "8": [[(L, T), (R, T), (R, B), (L, B), (L, T)], [(L, M), (R, M)]],
    "9": [[(R, M), (L, M), (L, T), (R, T), (R, B), (L, B)]],
}


def glyph_strokes(box):
    """The character's polylines moved onto the plate (mm, plate coordinates)."""
    if box["char"] not in GLYPHS:
        raise KeyError(f"no placeholder glyph for {box['char']!r}")
    return [[(round(box["x"] + px, 3), round(box["y"] + py, 3)) for px, py in line]
            for line in GLYPHS[box["char"]]]


# ---------------------------------------------------------------------------
# Output


def plate_data(reg, side="rear", plate_size=PLATE_STANDARD):
    """Everything the Blender side needs for one plate, as plain data."""
    if side not in PLATE_COLOURS:
        raise ValueError(f"side must be front or rear, not {side!r}")
    boxes = layout(reg, plate_size)
    return {
        "registration": reg,
        "side": side,
        "colour": PLATE_COLOURS[side],
        "ink": INK,
        "plate_mm": [plate_size[0], plate_size[1]],
        "stroke_mm": STROKE,
        "characters": [dict(b, strokes=[[list(p) for p in line] for line in glyph_strokes(b)])
                       for b in boxes],
        "placeholder_font": True,
    }


def plate_json(reg, side="rear", plate_size=PLATE_STANDARD):
    return json.dumps(plate_data(reg, side, plate_size), indent=2)


def plate_svg(reg, side="rear", plate_size=PLATE_STANDARD):
    """An SVG of one plate, 1 unit = 1 mm."""
    if side not in PLATE_COLOURS:
        raise ValueError(f"side must be front or rear, not {side!r}")
    pw, ph = plate_size
    boxes = layout(reg, plate_size)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{pw}mm" height="{ph}mm" '
        f'viewBox="0 0 {pw} {ph}">',
        f'<title>{reg} ({side}, placeholder font)</title>',
        f'<rect x="0" y="0" width="{pw}" height="{ph}" rx="6" '
        f'fill="{PLATE_COLOURS[side]}" stroke="#333333" stroke-width="1.5"/>',
        f'<g fill="none" stroke="{INK}" stroke-width="{STROKE}" '
        f'stroke-linecap="round" stroke-linejoin="round">',
    ]
    for b in boxes:
        for line in glyph_strokes(b):
            pts = " ".join(f"{x:g},{y:g}" for x, y in line)
            parts.append(f'<polyline points="{pts}"/>')
    parts.append("</g></svg>")
    return "\n".join(parts) + "\n"


# ---------------------------------------------------------------------------
# Self-check and command line


def check_plate(reg, plate_size=PLATE_STANDARD):
    """List of problems with one registration (empty means fine)."""
    problems = []
    if not is_valid_registration(reg):
        problems.append(f"{reg}: not a valid invented 1990 registration")
        return problems
    try:
        boxes = layout(reg, plate_size)
    except ValueError as e:
        return [str(e)]
    for b in boxes:
        if b["w"] != char_width(b["char"]):
            problems.append(f"{reg}: {b['char']} is {b['w']} mm wide")
        if b["char"] not in GLYPHS:
            problems.append(f"{reg}: no glyph for {b['char']}")
    try:
        ET.fromstring(plate_svg(reg, "front", plate_size))
    except ET.ParseError as e:
        problems.append(f"{reg}: SVG does not parse ({e})")
    return problems


def main(argv=None):
    ap = argparse.ArgumentParser(description="Invent and check 1990 number plates.")
    ap.add_argument("--seed", type=int, default=1990)
    ap.add_argument("--count", type=int, default=12)
    ap.add_argument("--date", help="game date YYYY-MM-DD (H plates from 1990-08-01)")
    args = ap.parse_args(argv)
    game_date = datetime.date.fromisoformat(args.date) if args.date else None
    regs = generate_registrations(args.seed, args.count, game_date=game_date)
    problems = []
    if len(set(regs)) != len(regs):
        problems.append("registrations are not unique")
    for reg in regs:
        print(reg)
        problems.extend(check_plate(reg))
    if problems:
        for p in problems:
            print("FAIL", p)
        return 1
    print(f"PASS: {len(regs)} plates, seed {args.seed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
