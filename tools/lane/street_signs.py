"""Bus stop and yellow-line time plates for a 1990 street, as data, pure Python.

Written by the lane session, 17 November 2026. No Blender, no network. It
builds two pieces of street furniture as JSON-able dicts of parts (sizes,
positions, text) plus an SVG of each plate face, and places time plates along
a kerb on lamp columns, reporting the gaps that need a short post of their own.

Facts and where they come from (all read 17 Nov 2026):
  - production/research/lane/KERBSIDE-RULES-1990-2026-11-17.md
  - production/research/lane/FURNITURE-SPECS-2026-11-17.md
  - production/lane/S-FURNITURE-BUILD-PLAN-2026-11-17.md (2.1, 2.8)

Sourced:
  - Bus stop flag about 300 x 450 mm ("1ft x 1ft 6in", Commercial Motor,
    30 Apr 1971, Teesside). One town, 1971: general use in 1990 unverified.
    Which side is the width is not stated; tall (300 wide, 450 high) is est.
  - Route numerals 1 in (25.4 mm) high, same 1971 piece.
  - Flag: white, black bus outline, "Bus stop", an operator band (diagram 970
    as described by The Beauty of Transport, 2016). Operator here is invented.
  - Yellow lines in 1990 (HC Deb 11 March 1991 vol 187 c400W): double yellow
    lines restrict waiting for at least eight hours between 7 am and 7 pm on
    at least four days a week, times shown on plates at regular intervals.
    validate_restriction() enforces that for double lines.
  - Commercial Motor, 8 Jan 1965, says times "will be shown on plates
    erected alongside (normally on lamp posts)". That quote is about
    loading-ban kerb marks, not waiting lines; putting waiting-line plates
    on lamp columns is INFERRED from it and marked so in the output.

Not sourced, so every such number is marked "est" in the output: pole height
and diameter, flag mounting height, timetable case size, shelter sizes, the
time plate's size, colour, letter height, mounting height, and the interval
between plates. The 1981 regulations (SI 1981/859) were not reached; plate
wording, colours and size must be checked against them from the PC before
modelling. The wording here is an invented example in period style.

Units: millimetres. Positions: x along the kerb, y across (away from the
carriageway), z up from the footway. SVG y runs down from the plate's top.
"""
import json
import re
from xml.sax.saxutils import escape

# Each dimension: (value_mm, source). "est" means not in the research.
SOURCED = "sourced"
EST = "est"

BUS_STOP = {
    "flag_width": (300, SOURCED),        # 1 ft, Commercial Motor 1971
    "flag_height": (450, SOURCED),       # 1 ft 6 in, Commercial Motor 1971
    "flag_thickness": (3, EST),
    "route_numeral_height": (25.4, SOURCED),  # 1 in, same piece
    "operator_band_height": (90, EST),
    "pole_diameter": (76, EST),          # research: from memory, unverified
    "pole_height": (3000, EST),          # above footway
    "flag_bottom_height": (2250, EST),   # flag lower edge above footway
    "timetable_case_width": (300, EST),
    "timetable_case_height": (400, EST),
    "timetable_case_depth": (40, EST),
    "timetable_case_bottom": (1200, EST),
    "shelter_length": (3000, EST),
    "shelter_depth": (1300, EST),
    "shelter_height": (2200, EST),
    "pole_kerb_offset": (450, EST),      # pole centre back from kerb face
}

TIME_PLATE = {
    "plate_width": (250, EST),
    "plate_height": (200, EST),
    "plate_thickness": (2, EST),
    "letter_height": (25, EST),
    "mount_height": (1800, EST),         # plate lower edge above footway
    "interval": (60000, EST),            # longest gap between plates, along kerb
    "post_diameter": (60, EST),
    "post_height": (2100, EST),
}

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# Words that would date a plate after 1990, or break canon. Lower case.
FORBIDDEN_WORDS = [
    "www", "http", ".com", ".co.uk", "online", "app", "mobile", "phone",
    "text", "sms", "email", "cctv", "camera", "contactless", "card",
    "pcn", "penalty charge", "at any time", "euro",
    # canon: no alcohol or gambling
    "pub", "bar", "beer", "wine", "ale", "lager", "spirits", "off licence",
    "betting", "bet", "bookmaker", "bookies", "casino", "bingo", "lottery",
    "pools", "arcade",
    # canon: no children anywhere
    "school", "school keep clear", "children", "child", "playground",
    "nursery", "kids", "infants",
]

# Invented. A web search (17 Nov 2026) for "Meridian District Buses" found no
# such operator, but "Meridian" is a real place name in several countries, so
# an obviously made-up name is used instead; "Saltmarrow" gave no hits.
DEFAULT_OPERATOR = "Saltmarrow Omnibus Company"


def _v(table, key):
    return table[key][0]


def _dim(table, key):
    value, src = table[key]
    return {"mm": value, "source": src}


def _words(text):
    """Lower-case words, split on anything that is not a letter."""
    return re.findall(r"[a-z]+", text.lower())


def check_text(lines):
    """Return the forbidden words found in the text lines (empty means fine).
    Each line is split on non-letters, so "(pub)", "pub-side" and "beer's"
    are caught; a phrase matches as a run of whole words."""
    found = []
    for line in lines:
        joined = " " + " ".join(_words(line)) + " "
        for entry in FORBIDDEN_WORDS:
            if entry.startswith("."):
                hit = entry in line.lower()
            else:
                hit = " " + " ".join(_words(entry)) + " " in joined
            if hit and entry not in found:
                found.append(entry)
    return found


# ---------------------------------------------------------------- bus stop

def bus_stop(route_numbers=("14",), operator=DEFAULT_OPERATOR, mount="post",
             timetable_case=True, shelter=False):
    """A bus stop as parts. mount is 'post' (own pole) or 'flag' (flag only,
    to hang on an existing column). Shelter is off by default."""
    if mount not in ("post", "flag"):
        raise ValueError("mount must be 'post' or 'flag'")
    for r in route_numbers:
        if not str(r).isdigit() or len(str(r)) > 3:
            raise ValueError("route numbers are 1 to 3 digits: %r" % (r,))
    text = ["Bus stop", operator] + [str(r) for r in route_numbers]
    bad = check_text(text)
    if bad:
        raise ValueError("text not fit for 1990: %s" % bad)

    fw, fh = _v(BUS_STOP, "flag_width"), _v(BUS_STOP, "flag_height")
    pole_d = _v(BUS_STOP, "pole_diameter")
    y0 = _v(BUS_STOP, "pole_kerb_offset")
    fz = _v(BUS_STOP, "flag_bottom_height")
    parts = []
    if mount == "post":
        parts.append({
            "name": "pole", "shape": "cylinder",
            "size": {"diameter": _dim(BUS_STOP, "pole_diameter"),
                     "height": _dim(BUS_STOP, "pole_height")},
            "position": [0, y0, 0],
        })
    # The flag stands out from the pole toward the carriageway (minus y), so
    # its face looks along the kerb (normal along x) and is read by people
    # walking along the footway and by an approaching bus. Facing est.
    # Size 1 ft x 1 ft 6 in is sourced; that it is tall, not wide, is est.
    parts.append({
        "name": "flag", "shape": "box",
        "size": {"width": _dim(BUS_STOP, "flag_width"),
                 "height": _dim(BUS_STOP, "flag_height"),
                 "thickness": _dim(BUS_STOP, "flag_thickness")},
        "position": [0, y0 - pole_d / 2 - fw / 2, fz],
        "width_axis": "y", "face_normal": [1, 0, 0],
        "facing": {"value": "face along the kerb, standing out toward the "
                            "carriageway", "source": EST},
        "orientation": {"value": "tall, not wide", "source": EST},
        "colour": "white", "text": text,
    })
    if timetable_case:
        parts.append({
            "name": "timetable_case", "shape": "box",
            "size": {"width": _dim(BUS_STOP, "timetable_case_width"),
                     "height": _dim(BUS_STOP, "timetable_case_height"),
                     "depth": _dim(BUS_STOP, "timetable_case_depth")},
            "position": [0, y0 + pole_d / 2 + _v(BUS_STOP, "timetable_case_depth") / 2,
                         _v(BUS_STOP, "timetable_case_bottom")],
            "text": ["Times of buses"],
        })
    if shelter:
        parts.append({
            "name": "shelter", "shape": "box",
            "size": {"length": _dim(BUS_STOP, "shelter_length"),
                     "depth": _dim(BUS_STOP, "shelter_depth"),
                     "height": _dim(BUS_STOP, "shelter_height")},
            "position": [-_v(BUS_STOP, "shelter_length") / 2 - 500,
                         y0 + 300, 0],
        })
    return {"piece": "bus_stop", "units": "mm", "mount": mount,
            "parts": parts, "flag_svg": bus_flag_svg(text)}


def bus_flag_svg(text):
    """Flag face: white field, operator band, a plain bus outline box,
    'Bus stop', route numbers. Simple boxes and text only."""
    fw, fh = _v(BUS_STOP, "flag_width"), _v(BUS_STOP, "flag_height")
    band = _v(BUS_STOP, "operator_band_height")
    num_h = _v(BUS_STOP, "route_numeral_height")
    title, operator, routes = text[0], text[1], text[2:]
    out = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%gmm" height="%gmm" '
        'viewBox="0 0 %g %g">' % (fw, fh, fw, fh),
        '<rect x="0" y="0" width="%g" height="%g" fill="#ffffff" '
        'stroke="#000000" stroke-width="4"/>' % (fw, fh),
        '<rect x="30" y="30" width="%g" height="120" fill="none" '
        'stroke="#000000" stroke-width="8"/>' % (fw - 60),
        '<text x="%g" y="210" font-size="45" text-anchor="middle" '
        'font-family="sans-serif">%s</text>' % (fw / 2, escape(title)),
        '<rect x="0" y="240" width="%g" height="%g" fill="#7a1f1f"/>' % (fw, band),
        '<text x="%g" y="%g" font-size="22" text-anchor="middle" fill="#ffffff" '
        'font-family="sans-serif">%s</text>' % (fw / 2, 240 + band / 2 + 8, escape(operator)),
    ]
    y = 240 + band + 50
    out.append('<text x="%g" y="%g" font-size="%g" text-anchor="middle" '
               'font-family="sans-serif">%s</text>'
               % (fw / 2, y, num_h, escape("  ".join(routes))))
    out.append("</svg>")
    return "\n".join(out)


# ------------------------------------------------------------- time plates

def _hour_text(h):
    if h in (0, 24):
        return "midnight"
    if h == 12:
        return "noon"
    return "%d am" % h if h < 12 else "%d pm" % (h - 12)


def validate_restriction(lines, first_day, last_day, start_hour, end_hour):
    """Check a restriction against the 1991 Hansard answer. Returns a list of
    problems (empty means fine). lines is 'double' or 'single'."""
    problems = []
    if lines not in ("double", "single"):
        problems.append("lines must be double or single")
    if first_day not in DAYS or last_day not in DAYS:
        problems.append("unknown day")
        return problems
    n_days = DAYS.index(last_day) - DAYS.index(first_day) + 1
    if n_days < 1:
        problems.append("last day before first day")
    if not (0 <= start_hour < end_hour <= 24):
        problems.append("hours out of order")
    if lines == "double":
        # Hansard: at least eight hours during the period 7 am to 7 pm. Only
        # restricted hours inside that period count; hours outside it are
        # allowed but do not count.
        if n_days < 4:
            problems.append("double lines need at least four days")
        inside = max(0, min(end_hour, 19) - max(start_hour, 7))
        if inside < 8:
            problems.append("double lines need at least eight hours "
                            "inside 7 am to 7 pm")
    return problems


def time_plate(lines="double", first_day="Mon", last_day="Sat",
               start_hour=8, end_hour=18):
    """A yellow-line time plate as data plus its SVG face. Default wording is
    an invented example: No waiting / Mon - Sat / 8 am - 6 pm."""
    problems = validate_restriction(lines, first_day, last_day, start_hour, end_hour)
    if problems:
        raise ValueError("; ".join(problems))
    text = ["No waiting",
            "%s - %s" % (first_day, last_day),
            "%s - %s" % (_hour_text(start_hour), _hour_text(end_hour))]
    bad = check_text(text)
    if bad:
        raise ValueError("text not fit for 1990: %s" % bad)
    return {
        "piece": "time_plate", "units": "mm", "lines": lines,
        "size": {"width": _dim(TIME_PLATE, "plate_width"),
                 "height": _dim(TIME_PLATE, "plate_height"),
                 "thickness": _dim(TIME_PLATE, "plate_thickness")},
        "letter_height": _dim(TIME_PLATE, "letter_height"),
        "mount_height": _dim(TIME_PLATE, "mount_height"),
        "on_lamp_columns": {"value": True, "source": "inferred"},
        "colour": {"value": "white field, black letters", "source": EST},
        "text": text,
        "svg": time_plate_svg(text),
    }


def time_plate_svg(text):
    w, h = _v(TIME_PLATE, "plate_width"), _v(TIME_PLATE, "plate_height")
    lh = _v(TIME_PLATE, "letter_height")
    out = ['<svg xmlns="http://www.w3.org/2000/svg" width="%gmm" height="%gmm" '
           'viewBox="0 0 %g %g">' % (w, h, w, h),
           '<rect x="0" y="0" width="%g" height="%g" fill="#ffffff" '
           'stroke="#000000" stroke-width="6"/>' % (w, h)]
    step = h / (len(text) + 1)
    for i, line in enumerate(text):
        out.append('<text x="%g" y="%g" font-size="%g" text-anchor="middle" '
                   'font-family="sans-serif">%s</text>'
                   % (w / 2, step * (i + 1) + lh / 3, lh, escape(line)))
    out.append("</svg>")
    return "\n".join(out)


def place_time_plates(kerb_length, lamp_columns, interval=None):
    """Place plates along a kerb of kerb_length mm. Plates go on lamp columns
    where they can; wherever no column falls within reach a short post is
    added and reported as a gap.

    Rule used (interval est): the first plate within interval/2 of the start,
    each next plate within interval of the last, the last plate within
    interval/2 of the end. Greedy: take the farthest column in reach, but
    only if the run can go on from it (it reaches the end, or another column
    lies within one interval past it). If not, a post is needed anyway, so
    the post goes at the farthest reach and the dead-end column is skipped:
    two close columns no longer both get plates just before a post. Plates
    on columns may still sit closer than the interval. Columns outside the
    kerb are ignored; duplicates count once. Waiting plates on lamp columns
    are inferred (the 1965 quote is about loading bans)."""
    if interval is None:
        interval = _v(TIME_PLATE, "interval")
    if kerb_length <= 0:
        raise ValueError("kerb length must be positive")
    if interval <= 0:
        raise ValueError("interval must be positive")
    reach = interval / 2.0
    cols = sorted({round(float(c), 3) for c in lamp_columns
                   if 0 <= float(c) <= kerb_length})
    plates, gaps = [], []
    last = None
    while True:
        limit = reach if last is None else last + interval
        if last is not None and last >= kerb_length - reach:
            break
        limit = min(limit, kerb_length)
        lo = -1.0 if last is None else last
        in_reach = [c for c in cols if lo < c <= limit]
        usable = None
        if in_reach:
            c = in_reach[-1]
            if c >= kerb_length - reach or any(c < d <= c + interval for d in cols):
                usable = c
        if usable is not None:
            pos, mount = usable, "lamp_column"
        else:
            pos, mount = round(limit, 3), "post"
            gaps.append({"from": 0.0 if last is None else last, "to": pos,
                         "post_at": pos})
        plates.append({"x": pos, "mount": mount,
                       "z": _v(TIME_PLATE, "mount_height")})
        last = pos
    return {"kerb_length": kerb_length, "interval": {"mm": interval, "source": EST},
            "plates": plates, "gaps_needing_posts": gaps,
            "posts": sum(1 for p in plates if p["mount"] == "post")}


if __name__ == "__main__":
    demo = {"bus_stop": bus_stop(), "time_plate": time_plate(),
            "placement": place_time_plates(48000, [8000, 28000])}
    print(json.dumps(demo, indent=2, sort_keys=True))
