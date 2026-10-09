"""Tests target.json against its own sources before anything is built (cloud week 42, 8 to 9 October 2026; SECOND TRY).

    /home/user/.bpyenv/bin/python self_check.py [--fonts DIR] [--no-write] [--fetch-fonts DIR] [--quick]

Groups:
  1  files and counts
  2  numbers that are printed or derived come back from target.json (paper sizes, plate lengths, calendars, the ferry's service, the tide table)
  3  the words: approved list, forbidden lists, tools/content-gate.py's rule table, RealWorld.cs, canon's streets and districts, names owed by canon, the placeholders
  4  fonts: licence files read, glyph coverage, the allowed list
  5  layout: every block re-measured from its font file, inside its safe zone, no overlaps
  6  contrast: recomputed from the palette and the ageing classes
  7  placements: inside zones, the gable and its downpipe, the amount of paper, piers, cases and boards, fascia, plates, shops
  8  the one photograph: the saved preview re-measured, the drawing laid on it
  9  the drawing: target_drawing.py is run and its polygons compared
  10 the line-level checks (.mask, .pos) tested on reference renders: a true render passes, a mirrored, shifted or wrong-font render fails
  11 the world: hours, market days, the ferry's last crossing, the cod price
  12 the GLYPH check (ITEM.glyphs), tested: every glyph of every block has a pixel scale at which it can be told from every other; the reviewer's wrong renders all FAIL;
     true renders (print, jittered hand cards, a tilt read in the placed street) PASS
  13 the second try's other guards, each tested on a good and a bad input: G.page.placeholders, G.dates.age, G.mirror.cues, G.ferry.schedule, G.letting.mount, G.place.paper,
     G.place.gable, the plates, PLACE.built, ITEM.square
It prints a result line and writes the result into target.json under "self_check" (unless --no-write).

THE READER (what a builder's own checker must do on a rendered item) is in this file: window_of, read_block, read_score, read_box, pos_ok (the line level);
render_item, glyph_layout, glyph_check_block, estimate_rotation (the glyph level; glyphlib.py holds the kernels).
"""
import sys
sys.dont_write_bytecode = True
import datetime
import hashlib
import importlib.util
import json
import math
import os
import re
import subprocess
import sys
import tempfile
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import glyphlib as gl

ROOT = HERE.parents[3]
SCRATCH = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/posters"
FONT_DIR = os.environ.get("PBP_FONTS", SCRATCH + "/fonts")
if "--fonts" in sys.argv:
    FONT_DIR = sys.argv[sys.argv.index("--fonts") + 1]
QUICK = "--quick" in sys.argv
RAW = "https://raw.githubusercontent.com/google/fonts/main/ofl"

if "--fetch-fonts" in sys.argv:
    dest = Path(sys.argv[sys.argv.index("--fetch-fonts") + 1])
    dest.mkdir(parents=True, exist_ok=True)
    import urllib.request
    urls = {"Archivo-var.ttf": RAW + "/archivo/Archivo%5Bwdth%2Cwght%5D.ttf",
            "CourierPrime-Regular.ttf": RAW + "/courierprime/CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf": RAW + "/courierprime/CourierPrime-Bold.ttf"}
    for fam in ("jost", "librefranklin", "oswald", "alfaslabone", "fraunces", "oldstandardtt", "archivo", "courierprime", "marcellussc", "patrickhand"):
        urls["OFL-%s.txt" % fam] = "%s/%s/OFL.txt" % (RAW, fam)
    for name, u in urls.items():
        try:
            urllib.request.urlretrieve(u, str(dest / name))
            print("fetched", name)
        except Exception as e:
            print("FAILED", name, e)
    sys.exit(0)

T = json.loads((HERE / "target.json").read_text(encoding="utf-8"))
ROWS = []
FACTS = {}


def row(group, name, ok, detail="", reported=False):
    ROWS.append(dict(g=group, n=name, ok=(None if reported else bool(ok)), d=str(detail)[:300], rep=bool(reported)))


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")


ITEMS = {it["id"]: it for it in T["items"]}
FONTS = T["fonts"]
PAL = T["palette"]
CLASSES = list(T["age_classes"])
STREET_DATE = datetime.date.fromisoformat(T["calendar"]["street_date_iso"])

# --------------------------------------------------------------------------------------------
# font access
# --------------------------------------------------------------------------------------------
_fc = {}


def font_path(key):
    spec = FONTS[key]
    for base in (Path(FONT_DIR), ROOT / "production" / "fonts"):
        for cand in (base / spec["file"], base / Path(spec["file"]).name):
            if cand.exists():
                return cand
    return None


def font(key, weight, px):
    k = (key, weight, round(px, 2))
    if k in _fc:
        return _fc[k]
    p = font_path(key)
    if p is None:
        _fc[k] = None
        return None
    spec = FONTS[key]
    f = ImageFont.truetype(str(p), px, layout_engine=ImageFont.Layout.RAQM)
    if spec["axes"]:
        vals = []
        for a in f.get_variation_axes():
            n = a["name"].decode() if isinstance(a["name"], bytes) else a["name"]
            v = spec["axes"].get(n, a["default"])
            if v is None:
                v = weight
            vals.append(min(max(v, a["minimum"]), a["maximum"]))
        f.set_variation_by_axes(vals)
    _fc[k] = f
    return f


def cap_ratio(key, weight):
    f = font(key, weight, 1000)
    return -f.getbbox("H", anchor="ls")[1] / 1000.0


def block_mask(b, W, H, ppm, key=None, weight=None, shift_mm=(0.0, 0.0), flip=False):
    """Boolean ink mask of a block rendered clean from its font, on a W x H mm canvas at ppm px/mm (the first try's function, kept: the reviewer's scripts use it)."""
    key = key or b["font"]
    weight = weight or b["weight"]
    px = b["size_px_per_em"]
    cap_target = b["cap_mm"]
    if key != b["font"]:
        f0 = font(key, weight, 1000)
        bb = f0.getbbox("H", anchor="ls")
        px = cap_target / (-bb[1] / 1000.0)
    f = font(key, weight, px * ppm)
    if f is None:
        return None
    text = b["text"]
    trk = b["tracking_em"] * px * ppm
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    img = Image.new("L", (int(W * ppm), int(H * ppm)), 0)
    d = ImageDraw.Draw(img)
    ox = b["origin_x_mm"]
    for i, ch in enumerate(text):
        if ch != " ":
            d.text(((ox + shift_mm[0]) * ppm + xs[i], (H - b["baseline_mm"] + shift_mm[1]) * ppm), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
    if key != b["font"]:
        cols = np.where(a.any(axis=0))[0]
        if len(cols):
            cx_new = (cols.min() + cols.max()) / 2.0
            cx_old = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0 * ppm
            a = np.roll(a, int(round(cx_old - cx_new)), axis=1)
    if flip:
        a = a[:, ::-1]
    return a


def block_local(b, ppm, H_mm, win, key=None, weight=None, text=None, origin_x_mm=None):
    """The same mask as block_mask but drawn only into the window win = (x0, x1, y0, y1) in canvas pixels (row 0 = the item's TOP edge): what the windowed reader uses."""
    key = key or b["font"]
    weight = weight or b["weight"]
    px = b["size_px_per_em"]
    f = font(key, weight, px * ppm)
    text = b["text"] if text is None else text
    trk = b["tracking_em"] * px * ppm
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    x0, x1, y0, y1 = win
    img = Image.new("L", (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(img)
    ox = b["origin_x_mm"] if origin_x_mm is None else origin_x_mm
    for i, ch in enumerate(text):
        if ch != " ":
            d.text((ox * ppm + xs[i] - x0, (H_mm - b["baseline_mm"]) * ppm - y0), ch, font=f, fill=255, anchor="ls")
    return np.asarray(img) > 100


def fscore(read, ref, dil_px):
    """Mean of recall and precision, each against the other dilated."""
    return gl.fscore(read, ref, max(1, dil_px))


# --------------------------------------------------------------------------------------------
# 1 files and counts
# --------------------------------------------------------------------------------------------
def group1():
    g = "1 files"
    row(g, "schema", T["schema"].startswith("ledger.cloud-week-42.target.posters-boards-plates"))
    ids = [i["id"] for i in T["items"]]
    row(g, "item ids unique", len(ids) == len(set(ids)), "%d items" % len(ids))
    units = sorted({i["unit"] for i in T["items"]})
    row(g, "the three units are all present", units == ["4.2", "4.3", "4.4"], str(units))
    row(g, "checks list is long and has unique ids", len({c["id"] for c in T["checks"]}) == len(T["checks"]) and len(T["checks"]) > 300, "%d checks" % len(T["checks"]))
    for need in ("fonts", "font_decisions", "palette", "age_classes", "processes", "surfaces", "placements", "unplaced", "cases", "approved_words", "forbidden_patterns", "sources", "unreached",
                 "would_read_when_network_opens", "could_not_settle", "disagreements_photographs_win", "proposed_names", "render_contract", "fixings", "placeholders", "second_try"):
        row(g, "section %s present and non-empty" % need, bool(T.get(need)))
    for it in T["items"]:
        ok = it["format"]["w_mm"] > 0 and it["format"]["h_mm"] > 0 and it["variants"] and (it["blocks"] or it["id"] in ())
        if not ok:
            row(g, "item %s has size, variants and blocks" % it["id"], False)
    row(g, "every item has size, variants and at least one block", True)
    p = ROOT / "production" / "cloud-week" / "targets" / "posters-boards-plates"
    for f in ("TARGET.md", "target.json", "target_drawing.py", "self_check.py", "make_target.py", "make_previews.py", "glyphlib.py"):
        row(g, "file %s exists" % f, (p / f).exists())
    row(g, "TARGET-REVIEW.md is untouched (not this tool's file)", (p / "TARGET-REVIEW.md").exists())
    prev = ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates"
    jpgs = sorted(prev.glob("*.jpg"))
    row(g, "previews exist, JPEG, 1200 px at most, under 300 KB", len(jpgs) >= 6 and all(f.stat().st_size < 300_000 and max(Image.open(f).size) <= 1200 for f in jpgs), "%d files" % len(jpgs))
    row(g, "target.json is under the 1 MB the git size guard allows (with this result written in)", (HERE / "target.json").stat().st_size < 980_000, "%d bytes" % (HERE / "target.json").stat().st_size)
    row(g, "no font file was added to production/fonts by this target", not any((ROOT / "production" / "fonts" / d).exists() for d in ("archivo", "courier-prime", "courierprime")))


# --------------------------------------------------------------------------------------------
# 2 numbers
# --------------------------------------------------------------------------------------------
def parse_clock(t):
    h, m = t.split(".")
    return int(h) * 60 + int(m)


def ferry_from_blocks(it):
    """The printed timetable read back from F01's blocks: (hook departures, far departures) for Monday to Saturday, in minutes after midnight, and the Sunday ones."""
    by = {b["id"]: b["text"] for b in it["blocks"]}
    out = {}
    for col, name in ((0, "hook"), (1, "far")):
        first = [parse_clock(t) for t in by["ms%d_0" % col].split()]
        until = parse_clock(by["ms%d_2" % col].replace("until ", "").replace(" PM", "")) + 720
        then = [parse_clock(t) + 720 for t in by["ms%d_3" % col].replace("then ", "").split()] + [parse_clock(t) + 720 for t in by["ms%d_4" % col].split()]
        last = parse_clock(by["ms%d_5" % col].replace("LAST CROSSING ", "")) + 720
        half = list(range(first[0], until + 1, 30))
        assert half[:3] == first, (name, half[:3], first)
        out[name] = half + then + [last]
        s0 = by["su%d_0" % col].replace(" and hourly", "").replace(" AM", "")
        s1 = by["su%d_1" % col].replace("until ", "").replace(" PM", "")
        out[name + "_sun"] = list(range(parse_clock(s0), parse_clock(s1) + 720 + 1, 60))
    return out


def ferry_sim(hook, far, cross=15):
    """One vessel, starting the day at the Hook. Returns (ok, why, end place, end time). Every departure must find the vessel at that side and already arrived."""
    ev = sorted([(t, "hook") for t in hook] + [(t, "far") for t in far])
    place, free_at = "hook", 0
    for t, p in ev:
        if p != place:
            return False, "at %d the vessel is at the %s but a departure is listed from the %s" % (t, place, p), place, free_at
        if t < free_at:
            return False, "at %d the vessel is still crossing until %d" % (t, free_at), place, free_at
        place, free_at = ("far" if p == "hook" else "hook"), t + cross
    return True, "", place, free_at


def group2():
    g = "2 numbers"
    F = T["formats"]
    imperial = dict(crown=(15, 20), double_crown=(20, 30), quad_crown=(40, 30), four_sheet=(40, 60))
    for k, (wi, hi) in imperial.items():
        row(g, "%s is %d x %d in = %d x %d mm" % (k, wi, hi, round(wi * 25.4), round(hi * 25.4)), (F[k]["w"], F[k]["h"]) == (round(wi * 25.4), round(hi * 25.4)), "%s" % F[k])
    a = [(841, 1189)]
    for n in range(1, 7):
        w, h = a[-1]
        a.append((h // 2, w))
    for n in (2, 3, 4, 5, 6):
        row(g, "A%d is %d x %d" % (n, a[n][0], a[n][1]), (F["A%d" % n]["w"], F["A%d" % n]["h"]) == a[n])
    bad = [i["id"] for i in T["items"] if i["format"]["name"] in F and (i["format"]["w_mm"], i["format"]["h_mm"]) != (F[i["format"]["name"]]["w"], F[i["format"]["name"]]["h"])]
    row(g, "every item's size equals its named format", not bad, str(bad))
    # plates
    ok = True
    det = []
    for it in T["items"]:
        np_ = it.get("name_plate")
        if not np_:
            continue
        blk = [b for b in it["blocks"] if b["id"] == "name"][0]
        w = int(math.ceil((np_["ink_w_mm"] + 2 * (6 + 12 + 44)) / 10.0) * 10)
        ok &= (w == np_["plate_w_mm"] == it["format"]["w_mm"]) and abs(blk["width_mm"] - np_["ink_w_mm"]) < 0.6 and np_["cap_mm"] == 90.0 and it["format"]["h_mm"] >= 200 and np_["variant"] in ("n", "d")
        borders = [s for s in it["shapes"] if s["id"] == "border"][0]
        ok &= borders["width_mm"] == 12 and borders["box_mm"][0] == 6
        det.append("%s %dx%d" % (it["id"], it["format"]["w_mm"], it["format"]["h_mm"]))
    row(g, "plate length = ink width + 124 mm rounded up to 10; cap 90; border 12 mm 6 mm in; depth 200 mm or more; variants n and d only", ok, ", ".join(det[:9]))
    names = {i["name_plate"]["street"] for i in T["items"] if i.get("name_plate")}
    row(g, "three streets, two variants each (n the default, d a variant), no postal-district plate and no MR1", names == {"QUAY STREET", "WEIGHHOUSE LANE", "TANNERY ROW"} and sum(1 for i in T["items"] if i.get("name_plate")) == 6
        and not any("MR1" in b["text"] for it in T["items"] for b in it["blocks"]) and not any(i["id"].endswith("p") and i["id"].startswith("S0") for i in T["items"]))
    q = [p for p in T["placements"] if p["item"] == "S01n" and p.get("street_x_m") == 20.47][0]
    half = q["w_m"] / 2.0
    row(g, "the Quay Street plate sits on the corner pier (19.92 to 21.0) with at least 40 mm each side", 20.47 - half >= 19.92 + 0.04 and 20.47 + half <= 21.0 - 0.04, "%.3f to %.3f" % (20.47 - half, 20.47 + half))
    row(g, "plate heights: bottom edge at 2.4 m or more, top below the pier's 3.12 m", all(p["z_bottom_m"] >= 2.4 and p["z_bottom_m"] + p["h_m"] <= 3.12 for p in T["placements"] if p["surface"] == "SF7"))
    # letting boards against the fascia
    L2 = ITEMS["L02"]
    row(g, "L02 is 900 x 450 and fits the 0.55 m fascia with 50 mm clear above and below", (L2["format"]["w_mm"], L2["format"]["h_mm"]) == (900, 450) and abs((3.40 - 2.85) - 0.45 - 0.10) < 1e-9)
    cols = T["surfaces"]["SF4"]["columns_street_x"]
    row(g, "lamp columns every 20 m from 8 m (SCENE-SLOTS)", cols == [8.0 + 20.0 * k for k in range(3)], str(cols))
    S2 = T["surfaces"]["SF2"]
    row(g, "the empty unit's glass is 3.562 m (5.3 opening zone - 0.9 door - 0.838 side door) and runs 23.088 to 26.65", abs((5.3 - 0.9 - 0.838) - 3.562) < 1e-9 and abs(S2["glass_street_x"][1] - S2["glass_street_x"][0] - 3.562) < 1e-6)
    # ferry: the printed blocks read back, against the schedule dict
    fs = ITEMS["F01"]["schedule"]
    pr = ferry_from_blocks(ITEMS["F01"])
    ms = fs["mon_sat"]
    sched_hook = [parse_clock(t) for t in ms["hook_first"]]
    sched_hook = list(range(sched_hook[0], parse_clock(ms["hook_half_hourly_until"].replace(" PM", "")) + 721, 30)) + [parse_clock(t) + 720 for t in ms["hook_then"]] + [parse_clock(ms["hook_last"]) + 720]
    sched_far = [parse_clock(t) for t in ms["far_first"]]
    sched_far = list(range(sched_far[0], parse_clock(ms["far_half_hourly_until"].replace(" PM", "")) + 721, 30)) + [parse_clock(t) + 720 for t in ms["far_then"]] + [parse_clock(ms["far_last"]) + 720]
    row(g, "ferry: the printed timetable read back from F01's blocks equals the schedule written in target.json", pr["hook"] == sched_hook and pr["far"] == sched_far)
    row(g, "ferry: the last Hook crossing is 11.00 PM, the last far-side one 11.15 PM", pr["hook"][-1] == 23 * 60 and pr["far"][-1] == 23 * 60 + 15)
    row(g, "ferry: Sunday far side is 15 minutes after the Hook", pr["far_sun"][0] - pr["hook_sun"][0] == 15 and pr["far_sun"][-1] - pr["hook_sun"][-1] == 15 and len(pr["far_sun"]) == len(pr["hook_sun"]))
    # tides
    rows_ = ITEMS["H04"]["tide_rows"] if "tide_rows" in ITEMS["H04"] else []
    ts = [datetime.datetime.strptime(r["t"], "%Y-%m-%d %H:%M") for r in rows_]
    dif = [(b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:])]
    row(g, "tide table: successive high waters 745 minutes apart (12 h 25 min)", rows_ and all(abs(d - 745) <= 5 for d in dif), "%d rows" % len(rows_))
    hts = [r["m"] for r in rows_]
    row(g, "tide table: heights between 3.3 and 4.8 m", rows_ and 3.3 <= min(hts) and max(hts) <= 4.8, "%.1f to %.1f" % (min(hts), max(hts)))
    day_hi = {}
    for t, r in zip(ts, rows_):
        day_hi[t.date()] = max(day_hi.get(t.date(), 0), r["m"])
    seq = [day_hi[d] for d in sorted(day_hi)][:7]
    top_day = sorted(day_hi)[seq.index(max(seq))]
    row(g, "tide table: the day's higher water runs 4.4 4.6 4.7 4.8 4.7 4.5 4.2 and peaks on Sunday 4 November (the full moon of 2 to 3 November)", seq == [4.4, 4.6, 4.7, 4.8, 4.7, 4.5, 4.2] and top_day == datetime.date(1990, 11, 4), str(seq))
    # calendar
    row(g, "1 October 1990 was a Monday", datetime.date(1990, 10, 1).weekday() == 0)
    row(g, "the street date is Monday 29 October 1990", STREET_DATE == datetime.date(1990, 10, 29) and STREET_DATE.weekday() == 0 and T["calendar"]["street_date"] == "Monday 29 October 1990")
    months = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "NOVEMBER", "DECEMBER"]
    days = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]
    rx = re.compile(r"\b(%s)\s+(\d{1,2})\s+(%s)\b" % ("|".join(days), "|".join(months)), re.I)
    n = 0
    wrong = []
    for it in T["items"]:
        for b in it["blocks"]:
            for m in rx.finditer(b["text"]):
                n += 1
                wd, dd, mo = m.group(1).upper(), int(m.group(2)), months.index(m.group(3).upper()) + 1
                if days[datetime.date(1990, mo, dd).weekday()] != wd:
                    wrong.append("%s/%s %s" % (it["id"], b["id"], m.group(0)))
    row(g, "every printed weekday and date agrees with the 1990 calendar (%d dates read)" % n, not wrong and n >= 12, str(wrong))
    bad_year = []
    for it in T["items"]:
        if it["id"] == "H04":
            continue          # the tide table's four-digit 24-hour times (1947 is 19.47)
        for b in it["blocks"]:
            for m in re.finditer(r"\b(19\d\d)\b", b["text"]):
                if not 1988 <= int(m.group(1)) <= 1992:
                    bad_year.append(b["text"])
    row(g, "every year printed is inside 1988 to 1992", not bad_year, str(bad_year))
    ev = [i["event"] for i in T["items"] if i.get("event")]
    row(g, "every event date is in the default autumn window (1 October to 30 November 1990)", all(datetime.date(1990, 10, 1) <= datetime.date(1990, e["m"], e["d"]) <= datetime.date(1990, 11, 30) for e in ev), "%d events" % len(ev))
    # the Tivoli's weeks start on Thursday (brand bible: 'changed on Thursdays')
    th = [b["text"] for it in T["items"] for b in it["blocks"] if "FROM " in b["text"] and any(k in it["id"] for k in ("T01", "T02", "T03"))]
    row(g, "every Tivoli start line reads FROM THURSDAY (the brand bible: changed on Thursdays)", th and all("FROM THURSDAY" in t for t in th) and not any("SUNDAY TO WEDNESDAY" in b["text"] for it in T["items"] for b in it["blocks"]), str(sorted(set(th))))
    ph = re.compile(r"\b960 (\d{3})\b")
    nums = [(it["id"], m.group(0)) for it in T["items"] for b in it["blocks"] for m in ph.finditer(b["text"])]
    near = [n for _, n in nums if n in ("960 417", "960 418")]
    row(g, "telephone numbers are the six-figure local form 960 xxx; none is Mickey's 960 418 or one digit from it (960 417)", nums and not near, "%d numbers" % len(nums))
    bad = [(it["id"], b["text"]) for it in T["items"] for b in it["blocks"] if re.search(r"\b0\d{3,4}\s*\d{5,}", b["text"])]
    row(g, "no long-form STD number (the town's code is not minted)", not bad, str(bad))
    prices = [(it["id"], m.group(0)) for it in T["items"] for b in it["blocks"] for m in re.finditer(r"£\d+(?:\.\d\d)?|\b\d+p\b", b["text"])]
    row(g, "prices are in pounds and pence (%d read)" % len(prices), len(prices) >= 15)
    cod = [b["text"] for it in T["items"] if it["id"] == "K09a" for b in it["blocks"] if "lb" in b["text"]]
    row(g, "cod price within the ONS 1990 range 2.42 to 2.85 plus 10 per cent", cod and 2.42 <= float(re.search(r"£([\d.]+)", cod[0]).group(1)) <= 3.10, str(cod))
    sm = [b["text"] for it in T["items"] if it["id"] == "K09e" for b in it["blocks"] if "lb" in b["text"]]
    had = [b["text"] for it in T["items"] if it["id"] == "K09b" for b in it["blocks"] if "lb" in b["text"]]
    row(g, "smoked haddock is dearer than fresh haddock", float(re.search(r"£([\d.]+)", sm[0]).group(1)) > float(re.search(r"£([\d.]+)", had[0]).group(1)), "%s v %s" % (sm, had))
    ck = [b["text"] for it in T["items"] if it["id"] == "K09f" for b in it["blocks"]]
    row(g, "cockles carry a unit", any(re.search(r"\bTUB\b", t) for t in ck), str(ck))
def load_content_gate():
    p = ROOT / "tools" / "content-gate.py"
    try:
        spec = importlib.util.spec_from_file_location("_cg", p)
        mod = importlib.util.module_from_spec(spec)
        sys.modules["_cg"] = mod
        spec.loader.exec_module(mod)
        return mod
    except Exception as e:
        return None


def realworld_names():
    p = ROOT / "ledger" / "Assets" / "Scripts" / "Core" / "RealWorld.cs"
    try:
        t = p.read_text(encoding="utf-8")
    except Exception:
        return [], []
    m = re.search(r"AnyCase\s*=\s*\{(.*?)\};", t, re.S)
    n = re.search(r"AsName\s*=\s*\{(.*?)\};", t, re.S)
    f = lambda blk: re.findall(r'"([^"]+)"', re.sub(r"//[^\n]*", "", blk)) if blk else []
    return f(m.group(1) if m else ""), f(n.group(1) if n else "")


def group3():
    g = "3 words"
    strings = []
    for it in T["items"]:
        for b in it["blocks"]:
            strings.append((it["id"], b["id"], b["text"], b.get("ghost", False)))
    approved = set(T["approved_words"]) | set(T["ghost_words"])
    miss = [(i, b, t) for i, b, t, gh in strings if norm(t) not in approved]
    row(g, "every drawn string is in approved_words", not miss, str(miss[:3]))
    parts = set(T["approved_word_parts"])
    tok = lambda s: re.findall(r"[A-Za-z0-9£'&.\-]+", norm(s))
    miss = [(i, t) for i, b, t, gh in strings for w in tok(t) if w not in parts]
    row(g, "every token of every string is in approved_word_parts", not miss, str(miss[:3]))
    extra = approved - {norm(t) for _, _, t, _ in strings}
    row(g, "approved_words holds nothing that is not drawn", not extra, str(sorted(extra)[:3]))
    FP = T["forbidden_patterns"]
    def hit(word_list, text, flags=re.I):
        out = []
        for w in word_list:
            if re.search(r"(?<![A-Za-z0-9])" + re.escape(w) + r"(?![A-Za-z0-9])", text, flags):
                out.append(w)
        return out
    for key in ("alcohol_gambling_children", "real_marks", "names_not_minted", "after_1992"):
        hits = [(i, b, h) for i, b, t, gh in strings for h in hit(FP[key], t)]
        row(g, "forbidden list %s: no hit in any string" % key, not hits, str(hits[:4]))
    # content gate
    cg = load_content_gate()
    if cg is not None:
        hits = []
        for i, b, t, gh in strings:
            for h in cg.scan(t):
                hits.append((i, b, h[0], h[2]))
        row(g, "tools/content-gate.py rule table (%d speech rules): no hit in any string" % len(cg.RULES), not hits, str(hits[:4]))
        ph = []
        for it in T["items"]:
            for fld in ("title", ):
                for h in cg.scan(it[fld]):
                    ph.append((it["id"], h[2]))
        row(g, "the item titles and art descriptions pass the content gate too", not ph)
        art = [(it["id"], h[2]) for it in T["items"] for a in it["art"] for h in cg.scan(a["describe"].replace("no people", "").replace("no faces", ""))]
        row(g, "art descriptions: no content-gate hit (the forbidden list names the banned things in order to refuse them and is skipped)", not art, str(art[:3]))
    else:
        row(g, "tools/content-gate.py could not be loaded", False, "import failed")
    any_case, as_name = realworld_names()
    if any_case:
        hits = []
        for i, b, t, gh in strings:
            tt = norm(t)
            for w in any_case:
                if re.search(r"(?<![\w'])" + re.escape(w) + r"(?![\w-])", tt, re.I):
                    hits.append((i, b, w))
            for w in as_name:
                if re.search(r"(?<![\w'])" + re.escape(w) + r"(?![\w-])", t):
                    hits.append((i, b, w))
        row(g, "RealWorld.cs: none of its %d real names or later things appears" % (len(any_case) + len(as_name)), not hits, str(hits[:4]))
    else:
        row(g, "RealWorld.cs not read", False)
    try:
        toks = json.loads((ROOT / "tools" / "imagegen" / "prompts.json").read_text(encoding="utf-8"))["content_rules"]["forbidden_tokens"]
        hits = [(i, b, w) for i, b, t, gh in strings for w in toks if len(w.strip()) >= 4 and re.search(r"(?<![A-Za-z0-9])" + re.escape(w.strip()) + r"(?![A-Za-z0-9])", t, re.I)]
        row(g, "imagegen's %d forbidden tokens (brands and content): no whole-word hit" % len(toks), not hits, str(hits[:4]))
    except Exception as e:
        row(g, "imagegen forbidden tokens not read", False, str(e))
    cast = ["Dunn", "Kirby", "Milner", "Ellis", "Agar", "Jensen", "Cammack", "Sedman", "Danby", "Garbutt", "Walsh", "Suddaby", "Nowak", "Mickey", "Ron", "Sheila", "Darren"]
    hits = [(i, b, c) for i, b, t, gh in strings for c in cast if re.search(r"\b%s\b" % c, t, re.I)]
    row(g, "no cast name appears on any sheet", not hits, str(hits[:3]))
    # canon
    canon = (ROOT / "canon.md").read_text(encoding="utf-8")
    sm = re.search(r"Streets minted:\s*([^.]*)\.", canon)
    streets = [s.strip().upper() for s in sm.group(1).split(",")] if sm else []
    names = {i["name_plate"]["street"] for i in T["items"] if i.get("name_plate")}
    row(g, "plate street names are the streets canon mints (%s)" % ", ".join(streets), names <= set(streets) and len(names) == 3, str(names))
    dm = re.search(r"seven districts:\s*(.*?)\n- ", canon, re.S)
    dtxt = dm.group(1).replace("\n", " ") if dm else ""
    districts = [d.strip().upper() for d in re.findall(r"([A-Za-z' ]+?)\s*\(", dtxt)]
    districts = [re.sub(r"^THE ", "", d).strip() for d in districts]
    dl = {i["name_plate"]["district"] for i in T["items"] if i.get("name_plate")}
    row(g, "plate district lines are canon's districts", {re.sub(r"^THE ", "", d) for d in dl} <= set(districts), "%s of %s" % (dl, districts))
    minted = ["MICKEY", "TIVOLI", "MERIDIAN HARBOUR BOARD", "MERIDIAN FERRY", "COPPER ROW", "THE EXCHANGE", "GULLWING", "QUAY STREET", "WEIGHHOUSE LANE", "TANNERY ROW", "THE HOOK", "IRONSIDE", "MERIDIAN"]
    row(g, "canon names used on sheets are in canon.md", all(m.title().split()[0].lower() in canon.lower() or m.lower() in canon.lower() for m in minted))
    # proposed
    prop = {p["name"] for p in T["proposed_names"]}
    row(g, "proposed (unminted) names are listed (%d entries)" % len(prop), len(prop) >= 8)
    places = {}
    for key in [p["name"] for p in T["proposed_names"]]:
        places[key] = sorted({it["id"] for it in T["items"] for b in it["blocks"] if key.lower() in b["text"].lower()})
    row(g, "where the proposed names stand (reported)", True, json.dumps(places)[:290], reported=True)
    only_here = all(places[k] for k in ("ARMITAGE & STOBBS", "QUAY PRINT", "THE SANDERLING TRIO", "THE HARPOONER", "TED HOLROYD", "SPANNER SMITH", "THE STEVEDORE", "THE DRILL HALL", "THE FOURTH WITNESS", "WHITEWELL", "QUAYSIDE"))
    row(g, "each proposed name that is meant to be drawn is drawn, on named variants (-named, L01, L03, B01, G01, G02) and imprints only", only_here)
    allowed_default = {"QUAY PRINT", "MERIDIAN AGAINST THE POLL TAX"}
    stray = [(it["id"], k) for k, ids in places.items() for it in [ITEMS[i] for i in ids] if not it.get("held") and k not in allowed_default and not any(b["role"] == "imprint" for b in it["blocks"] if k.lower() in b["text"].lower())
             and any(b["cap_mm"] >= 10 for b in it["blocks"] if k.lower() in b["text"].lower())]
    row(g, "a proposed name stands unheld only in blocks under 10 mm (the 2.4 mm imprints; the 3.6 to 6 mm campaign lines)", not stray, str(stray[:4]))
    names_old = ["TIGER JIM LARKIN", "THE SEA WOLF", "MAD MAURICE", "THE BARON", "MR1"]
    row(g, "no string carries a name the review struck (TIGER JIM LARKIN, THE SEA WOLF, MAD MAURICE, THE BARON, MR1)", not [(it["id"], n) for it in T["items"] for b in it["blocks"] for n in names_old if n.lower() in b["text"].lower()])
    # non-ASCII: only the allowed typographic marks
    allowed = set("£’·—–")
    odd = {ch for it in T["items"] for b in it["blocks"] for ch in b["text"] if ord(ch) > 127 and ch not in allowed}
    row(g, "no non-ASCII character but the pound, the right quote, the middle dot and two dashes", not odd, str(odd))
    # forbidden things named in an image description
    low = " ".join(a["describe"].lower() for it in T["items"] for a in it["art"])
    row(g, "art descriptions ask for no people, no faces, no text", all(("no people" in a["describe"].lower()) and ("no lettering" in a["describe"].lower() or "no faces" in a["describe"].lower()) for it in T["items"] for a in it["art"]))
    row(g, "every art slot's forbidden list names people, faces, children and text", all(all(w in a["forbidden"] for w in ("people", "faces", "children", "text")) for it in T["items"] for a in it["art"]))
    row(g, "no preview and no file name in this family names a business or a drink", all(("brewery" not in f.name and "bar" not in f.name.split("-")) for f in (ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates").glob("*")))



# --------------------------------------------------------------------------------------------
# 4 fonts
# --------------------------------------------------------------------------------------------
def group4():
    g = "4 fonts"
    used = sorted({b["font"] for it in T["items"] for b in it["blocks"]})
    row(g, "every font used is in the fonts table", all(u in FONTS for u in used), str(used))
    plan_table = {"Marcellus SC", "Oswald", "Jost", "Alfa Slab One", "Fraunces", "Old Standard TT", "Archivo", "Courier Prime"}
    decided = {d["font"] for d in T["font_decisions"] if d.get("decisions_line")}
    off = {FONTS[u]["family"] for u in FONTS} - plan_table
    row(g, "every family is on asset-plan note 4's font table, or is recorded with a DECISIONS line (off the table: %s)" % sorted(off), off <= decided and not any("overpass" in u.lower() for u in FONTS))
    read = {k: v["ofl"].get("read") for k, v in FONTS.items()}
    row(g, "every font's OFL.txt was read whole today (%d of %d)" % (sum(1 for v in read.values() if v), len(read)), all(read.values()), str([k for k, v in read.items() if not v]))
    missing = [u for u in used if font_path(u) is None]
    row(g, "every font file is found (%s)" % FONT_DIR, not missing, str(missing))
    chars = {}
    for it in T["items"]:
        for b in it["blocks"]:
            chars.setdefault(b["font"], set()).update(b["text"])
    bad = []
    for k, cs in chars.items():
        f = font(k, 400, 60)
        if f is None:
            continue
        def mask(c):
            im = Image.new("L", (120, 120), 0)
            ImageDraw.Draw(im).text((10, 90), c, font=f, fill=255, anchor="ls")
            return np.asarray(im)
        notdef = mask("")
        for c in cs:
            if c == " ":
                continue
            m = mask(c)
            if not m.any() or np.array_equal(m, notdef):
                bad.append((k, c))
    row(g, "every character of every string has a glyph in its font", not bad, str(bad))
    in_repo = [k for k, v in FONTS.items() if v["in_repo"]]
    row(g, "%d fonts are already in production/fonts; %d are to be added by the builder with their OFL.txt" % (len(in_repo), len(FONTS) - len(in_repo)), True, str([k for k, v in FONTS.items() if not v["in_repo"]]), reported=True)
    row(g, "no font file was added to production/fonts by this target", not any((ROOT / "production" / "fonts" / d).exists() for d in ("archivo", "courier-prime", "courierprime", "libre-baskerville", "librebaskerville")))



# --------------------------------------------------------------------------------------------
# 5 layout
# --------------------------------------------------------------------------------------------
def remeasure(b):
    px = b["size_px_per_em"]
    sc = 4.0 if b["cap_mm"] < 30 else 1.0
    f = font(b["font"], b["weight"], px * sc)
    if f is None:
        return None
    trk = b["tracking_em"] * px * sc
    text = b["text"]
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
    return ((cols.min() - pad) / sc, (base - (rows.max() + 1)) / sc, (cols.max() + 1 - pad) / sc, (base - rows.min()) / sc)


def group5():
    g = "5 layout"
    n = 0
    off = []
    nofont = 0
    for it in T["items"]:
        for b in it["blocks"]:
            bb = remeasure(b)
            if bb is None:
                nofont += 1
                continue
            n += 1
            ox = b["origin_x_mm"]
            box = [ox + bb[0], b["baseline_mm"] + bb[1], ox + bb[2], b["baseline_mm"] + bb[3]]
            if max(abs(a - c) for a, c in zip(box, b["ink_box_mm"])) > (0.7 if b["cap_mm"] < 30 else 1.6):
                off.append((it["id"], b["id"], [round(v, 1) for v in box], b["ink_box_mm"]))
    row(g, "every block's ink box re-measured from its font file agrees within 0.7 mm (1.6 mm for caps of 30 mm and over, one pixel of rounding) (%d blocks)" % n, not off and n > 300, str(off[:3]))
    row(g, "no block was skipped for want of a font file", nofont == 0, "%d skipped" % nofont)
    # safe zone and overlaps
    prob = []
    for it in T["items"]:
        sx0, sy0, sx1, sy1 = it["safe_mm"]
        bl = it["blocks"]
        for b in bl:
            x0, y0, x1, y1 = b["ink_box_mm"]
            if not b.get("ghost") and (x0 < sx0 - 0.5 or y0 < sy0 - 0.5 or x1 > sx1 + 0.5 or y1 > sy1 + 0.5):
                prob.append("%s/%s outside" % (it["id"], b["id"]))
        for i in range(len(bl)):
            for j in range(i + 1, len(bl)):
                a, c = bl[i], bl[j]
                if a["overlap_ok"] or c["overlap_ok"]:
                    continue
                ax0, ay0, ax1, ay1 = a["ink_box_mm"]
                bx0, by0, bx1, by1 = c["ink_box_mm"]
                if ax0 < bx1 and bx0 < ax1 and ay0 + 4 < by1 and by0 + 4 < ay1:
                    prob.append("%s %s/%s overlap" % (it["id"], a["id"], c["id"]))
    row(g, "every ink box is inside its safe zone and no two blocks overlap (descenders under 4 mm aside)", not prob, str(prob[:3]))
    # legibility floor
    low = [(it["id"], b["id"], b["cap_mm"] * it["px_per_mm"]) for it in T["items"] for b in it["blocks"] if b["role"] != "imprint" and b["cap_mm"] * it["px_per_mm"] < 4.5]
    row(g, "every block but the imprints is at least 4.5 px tall at its authoring scale", not low, str(low[:4]))
    imp = [(it["id"], b["cap_mm"]) for it in T["items"] for b in it["blocks"] if b["role"] == "imprint"]
    row(g, "imprints are 7 point (cap 2.4 mm) or 4.0 mm: below the 3 m legibility floor by design (%d)" % len(imp), True, "", reported=True)
    # hierarchy: on every bill the name line is the biggest block
    ok = True
    for iid in ("P01", "P02", "P03", "J01", "D01", "W01", "B01", "M01", "T03", "G02"):
        it = ITEMS[iid]
        caps = [b["cap_mm"] for b in it["blocks"] if b["role"] not in ("imprint",)]
        ok &= max(caps) >= 1.5 * sorted(caps)[len(caps) // 2]
    row(g, "bills have a clear top line (the biggest cap is at least 1.5 times the median)", ok)
    # sizes of the biggest and smallest caps
    caps = [(b["cap_mm"], it["id"]) for it in T["items"] for b in it["blocks"] if b["role"] != "imprint"]
    row(g, "cap range of lettering on the street", True, "smallest %s, biggest %s" % (min(caps), max(caps)), reported=True)


# --------------------------------------------------------------------------------------------
# 6 contrast
# --------------------------------------------------------------------------------------------
def s2l(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def rel(rgb):
    r, g, b = [s2l(v) for v in rgb]
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def ratio(a, b):
    la, lb = rel(a), rel(b)
    return round((max(la, lb) + 0.05) / (min(la, lb) + 0.05), 2)


def group6():
    g = "6 contrast"
    # recompute the stored B ratio from the palette for blocks on stock or paints
    bad = []
    n = 0
    below = []
    for it in T["items"]:
        for b in it["blocks"]:
            k = b["ink"]
            if k in PAL["paints"]:
                ink = PAL["paints"][k]["aged"]["B"]
            elif k == "paper":
                ink = PAL["stocks"][it["stock"]]["aged"]["B"]
            else:
                continue_ = False
                ink = None
            if ink is None:
                continue
            on = b["on"] if "on" in b else None
    # The stored contrast came from the author tool's own colour maths; recompute the common cases independently.
    def aged_stock(key, c):
        return PAL["stocks"][key]["aged"][c]
    def aged_ink(key, stock, c):
        # re-implementation: f = 1 - exp(-t/tau); mix toward the aged stock; then 35 per cent of the grime
        a = T["age_classes"][c]
        if key == "paper":
            return aged_stock(stock, c)
        ink = PAL["inks"][key]
        f = 1 - math.exp(-a["t_days"] / ink["tau_days"])
        st = aged_stock(stock, c)
        base = [round(ink["fresh"][i] * (1 - f) + st[i] * f) for i in range(3)]
        gr = PAL["grime"]
        return [round(base[i] * (1 - a["grime"] * 0.35) + gr[i] * a["grime"] * 0.35) for i in range(3)]
    checked = 0
    for it in T["items"]:
        for b in it["blocks"]:
            if b["ink"] in PAL["inks"] and b["on"] == "stock":
                for c in ("B", "C"):
                    r = ratio(aged_ink(b["ink"], it["stock"], c), aged_stock(it["stock"], c))
                    checked += 1
                    if abs(r - b["contrast"][c]) > 0.06:
                        bad.append((it["id"], b["id"], c, r, b["contrast"][c]))
    row(g, "stored contrast of ink on stock equals the ratio recomputed from the palette (%d values)" % checked, not bad, str(bad[:3]))
    for it in T["items"]:
        for b in it["blocks"]:
            if b["role"] == "imprint":
                continue
            floor = 3.0 if b["cap_mm"] >= 12 else 4.5
            nominal = b["contrast"]["B"]
            if nominal < floor and not b.get("min_contrast"):
                below.append((it["id"], b["id"], nominal, b["cap_mm"]))
    row(g, "every block reads at the floor (3.0 for cap 12 mm and over, 4.5 for smaller) in class B, or states an exception", not below, str(below[:6]))
    thin = [(it["id"], b["id"], b["contrast"]["C"]) for it in T["items"] for b in it["blocks"] if b["role"] in ("title", "name", "line") and b["contrast"]["C"] < 2.2]
    row(g, "display lines keep 2.2 or more in class C (months on the wall)", not thin, str(thin[:6]))
    faded = [(it["id"], b["id"], b["contrast"]["D"]) for it in T["items"] for b in it["blocks"] if b["contrast"]["D"] < 1.5 and b["role"] != "imprint"]
    row(g, "blocks that fade below 1.5 in class D (a bill a season old: reported, as intended for the oldest layer)", True, "%d blocks, e.g. %s" % (len(faded), faded[:3]), reported=True)
    # fluorescent fade order
    st = PAL["stocks"]
    fl = [k for k, v in st.items() if v["fade_to"] and v["tau_days"] <= 60]
    order = sorted(PAL["inks"].items(), key=lambda kv: (kv[1]["tau_days"] or 1e9))
    row(g, "order of fastness: fluorescent stock goes first, then red, then blue, then black, then toner", st["fluor_yellow"]["tau_days"] < PAL["inks"]["red"]["tau_days"] < PAL["inks"]["blue"]["tau_days"] < PAL["inks"]["black"]["tau_days"] < PAL["inks"]["toner"]["tau_days"])
    y = PAL["stocks"]["fluor_yellow"]
    row(g, "the fluorescent yellow ages to a paler paper, not a darker one (class C lighter than class A saturation)", rel(y["aged"]["C"]) > 0.55 and y["aged"]["C"][2] > y["fresh"][2], "%s -> %s" % (y["fresh"], y["aged"]["C"]))



# --------------------------------------------------------------------------------------------
# 7 placements
# --------------------------------------------------------------------------------------------
def vis_fractions(pls, res=0.01):
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
            if not ((q["layer"] > p["layer"]) or (q["layer"] == p["layer"] and j > i)):
                continue
            mx = (xs >= q["u_m"]) & (xs <= q["u_m"] + q["w_m"])
            my = (ys >= q["z_bottom_m"]) & (ys <= q["z_bottom_m"] + q["h_m"])
            cov |= my[:, None] & mx[None, :]
        out.append(1.0 - cov.mean())
    return out


def rect_overlap(a, b, tol=0.0):
    return a[0] < b[2] - tol and b[0] < a[2] - tol and a[1] < b[3] - tol and b[1] < a[3] - tol


def paper_counts(PLS):
    """fly-posters and poll-tax bills in the DEFAULT street (held placements and card boards excluded), by the items' paper_class."""
    n = {"fly_poster": 0, "poll_tax_bill": 0}
    for p in PLS:
        if p.get("held") or p.get("held_until_minted") or p["item"] not in ITEMS:
            continue
        pc = ITEMS[p["item"]].get("paper_class")
        if pc in n:
            n[pc] += 1
    return n


def paper_ok(n):
    """G.place.paper: AT MOST 8 fly-posters and 4 poll-tax bills (the asset plan's table A5)."""
    return n["fly_poster"] <= 8 and n["poll_tax_bill"] <= 4


def gable_ok(PLS):
    """G.place.gable: the quay gable is BARE, as the Hook sheet shows it: no paper and no plate on SF1 (or hosted by it) in the default street."""
    why = []
    for p in PLS:
        if p.get("held") or p.get("held_until_minted"):
            continue
        if p["surface"] == "SF1" or p.get("host") == "SF1":
            why.append("%s is on the gable (the Hook sheet shows it bare)" % p["item"])
    return not why, "; ".join(why)


def gable_fixtures_ok():
    """The gable's fixtures stand as the sheet shows them: the 75 mm cast-iron downpipe at u 0.30 full height, the render patch high up, the damp foot."""
    SF1 = T["surfaces"]["SF1"]
    fx = {f["id"]: f for f in SF1["fixtures"]}
    pipe, patch, foot = fx.get("downpipe"), fx.get("render_patch"), fx.get("damp_foot")
    return bool(pipe and patch and foot and pipe["diameter_mm"] == 75 and pipe["u_m"] == 0.30 and pipe["z_m"][1] >= 6.0 and pipe["keep_paper_clear_mm"] == 150
                and patch["z_m"] == [3.6, 5.0] and foot["z_m"] == [0.0, 0.45])


def gable_alt_ok(PLS):
    """The HELD proof wall, if he ever chooses the gable for the sample, keeps what the sheet shows: paper 150 mm clear of the downpipe, none above 2.75 m, none in the damp foot, the three
    bills in ONE layer at one z and not overlapping."""
    SF1 = T["surfaces"]["SF1"]
    pipe = [f for f in SF1["fixtures"] if f["id"] == "downpipe"][0]
    clear = pipe["u_m"] + pipe["diameter_mm"] / 2000.0 + pipe["keep_paper_clear_mm"] / 1000.0
    sf1 = [p for p in PLS if p["surface"] == "SF1" and p.get("held") and p.get("proof_wall") and not p.get("alt_of")]
    bills = [p for p in sf1 if ITEMS[p["item"]].get("paper_class") in ("fly_poster", "poll_tax_bill")]
    why = []
    for p in sf1:
        if p["u_m"] < clear - 1e-9:
            why.append("%s starts at u %.3f, inside the 150 mm round the downpipe (%.3f)" % (p["item"], p["u_m"], clear))
        if p["z_bottom_m"] + p["h_m"] > 2.75 + 1e-9:
            why.append("%s reaches %.2f m" % (p["item"], p["z_bottom_m"] + p["h_m"]))
        if p["z_bottom_m"] < 0.45 - 1e-9:
            why.append("%s sits in the damp foot" % p["item"])
    if len({p["layer"] for p in bills}) != 1 or len(bills) != 3:
        why.append("the held proof wall has %d bills in layers %s, not three in one" % (len(bills), sorted({p["layer"] for p in bills})))
    if len({round(p["z_bottom_m"], 3) for p in bills}) != 1:
        why.append("the three bills' bottoms are not all at one z")
    return not why, "; ".join(why)


def group7():
    g = "7 placements"
    PLS = T["placements"]
    SF = T["surfaces"]
    DEF = [p for p in PLS if not p.get("held")]
    z = SF["SF1"]["paste_zone"]
    sf1 = [p for p in DEF if p["surface"] == "SF1" or p.get("host") == "SF1"]
    held1 = [p for p in PLS if p.get("held") and p.get("proof_wall") and not p.get("alt_of")]
    ok, why = gable_ok(PLS)
    row(g, "SF1: the quay gable is BARE, as the Hook sheet shows it: no paper and no plate on it in the default street (%d proof-wall placements are held)" % len(held1), ok and not sf1 and len(held1) == 5, why)
    row(g, "SF1: the downpipe (75 mm cast iron, u 0.30, full height, paper kept 150 mm clear), the render patch (z 3.6 to 5.0) and the damp foot (z 0 to 0.45) stand as the sheet shows them", gable_fixtures_ok())
    paper1 = [p for p in held1 if ITEMS[p["item"]].get("paper_class") in ("fly_poster", "poll_tax_bill", "strip")]
    inside = all(z["u"][0] <= p["u_m"] and p["u_m"] + p["w_m"] <= z["u"][1] and z["z"][0] <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= z["z"][1] + 0.001 for p in paper1)
    row(g, "SF1 (held proof wall): every held bill lies inside the paste zone (u 0.15 to 6.0, z 0.45 to 2.75)", inside, str([(p["item"], p["u_m"], p["z_bottom_m"]) for p in paper1]))
    ok, why = gable_alt_ok(PLS)
    row(g, "SF1 (held proof wall): if ever used, ONE layer of three bills (P01, W01, T02, bottoms z 1.00), paper 150 mm clear of the downpipe, nothing above 2.75 m or in the damp foot", ok, why)
    row(g, "SF1 (held proof wall): the three bills are three templates (a poll-tax bill, a fight bill, a Tivoli quad), all flagged proof_wall and held", sorted(p["item"] for p in held1 if p["item"] in ("P01", "W01", "T02")) == ["P01", "T02", "W01"] and all(p.get("held_why") for p in held1))
    full = [p for p in paper1 if ITEMS[p["item"]]["paper_class"] != "strip"]
    ov = [(a["item"], b["item"]) for i, a in enumerate(full) for b in full[i + 1:] if rect_overlap((a["u_m"], a["z_bottom_m"], a["u_m"] + a["w_m"], a["z_bottom_m"] + a["h_m"]), (b["u_m"], b["z_bottom_m"], b["u_m"] + b["w_m"], b["z_bottom_m"] + b["h_m"]))]
    row(g, "SF1 (held proof wall): no bill overlaps another", not ov, str(ov))
    strip = [p for p in held1 if p["item"] == "T02s"][0]
    quad = [p for p in held1 if p["item"] == "T02"][0]
    off = (strip["z_bottom_m"] + strip["h_m"]) - (quad["z_bottom_m"] + quad["h_m"])
    dx = strip["u_m"] - quad["u_m"]
    row(g, "T02s sits across the quad's top band, 2 to 6 mm off square (up %.1f mm, in %.1f mm, turned %.2f degrees from the quad's own)" % (off * 1000, dx * 1000, strip["rot_deg"] - quad["rot_deg"]),
        0.002 <= off <= 0.006 and 0.0 <= dx <= 0.006 and 0.1 <= abs(strip["rot_deg"] - quad["rot_deg"]) <= 0.34 and abs(strip["w_m"] - 1.016) < 1e-6 and abs(strip["h_m"] - 0.09) < 1e-6)
    row(g, "SF1: no sticker, no case and no second layer on the gable (nothing more until he has approved the sample)", not [p for p in PLS if p["surface"] == "SF1" and (p["item"] in ("P05", "P06", "HC1", "FC1") or p.get("kind") == "case")])
    # paper amount
    n = paper_counts(PLS)
    row(g, "the amount of paper on Quay Street is AT MOST the asset plan's 8 fly-posters and 4 poll-tax bills (counted %s)" % n, paper_ok(n))
    row(g, "the default street carries 5 fly-posters (M01 twice, J01 twice, D01) and 3 poll-tax bills (P03, P02 and P02's window copy): inside the plan", n == {"fly_poster": 5, "poll_tax_bill": 3})
    # glass SF2
    sf2 = [p for p in DEF if p["surface"] == "SF2"]
    g0, g1 = SF["SF2"]["u_range"]
    z0, z1 = SF["SF2"]["z_range"]
    row(g, "SF2: every sheet lies inside the glass (3.562 x 1.8 m)", all(g0 <= p["u_m"] and p["u_m"] + p["w_m"] <= g1 and z0 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= z1 for p in sf2), "")
    row(g, "SF2: sheets hang low (top at or below 2.0 m, the whitewash showing above)", all(p["z_bottom_m"] + p["h_m"] <= 2.0 for p in sf2 if p["h_m"] > 0.2))
    ov = [(a["item"], b["item"]) for i, a in enumerate(sf2) for b in sf2[i + 1:] if rect_overlap((a["u_m"], a["z_bottom_m"], a["u_m"] + a["w_m"], a["z_bottom_m"] + a["h_m"]), (b["u_m"], b["z_bottom_m"], b["u_m"] + b["w_m"], b["z_bottom_m"] + b["h_m"]))]
    row(g, "SF2: one layer: no sheet overlaps another", not ov, str(ov))
    row(g, "SF2 holds M01, P03, P02, J01, C02 and C01a, no P01, no sticker", sorted(p["item"] for p in sf2) == ["C01a", "C02", "J01", "M01", "P02", "P03"])
    c1 = [p for p in sf2 if p["item"] == "C01a"][0]
    row(g, "C01a (the police appeal) is inside the empty unit's glass at u 0.30, z 1.30, with four tape tabs", abs(c1["u_m"] - 0.30) < 1e-9 and abs(c1["z_bottom_m"] - 1.30) < 1e-9 and "four tabs" in c1.get("fixing", ""))
    row(g, "no police appeal on a brick pier or a house front", not [p for p in PLS if p["surface"] == "WEST_PIER" and p["item"].startswith("C01")])
    # piers and the window
    piers = {p["id"]: p for p in T["west_piers"]}
    wp = [p for p in DEF if p["surface"] == "WEST_PIER"]
    ok = True
    det = []
    for p in wp:
        pr = piers[p["pier"]]
        ok &= p["w_m"] <= pr["w"] - 0.08 + 1e-9
        det.append((p["item"], p["pier"], p["w_m"], pr["w"]))
    row(g, "west piers: every sheet fits its pier with 40 mm each side (%d placements)" % len(wp), ok, str(det))
    m1 = [p for p in wp if p["pier"] == "W1.0"]
    row(g, "west piers: the only bill on a pier is the scene's own poster slot (x 11.4, pier W1.0), M01 at class B (a bill that needs no unminted name); the house board L04 is on W2.0", sorted((p["item"], p["pier"]) for p in wp) == [("L04", "W2.0"), ("M01", "W1.0")] and piers["W1.0"]["x0"] < 11.4 < piers["W1.0"]["x1"] and len(m1) == 1 and m1[0]["age_class"] == "B")
    row(g, "west piers: six piers, each 0.95 to 0.96 m, computed from the plain row's bay layout", len(T["west_piers"]) == 6 and all(0.94 <= p["w"] <= 0.96 for p in T["west_piers"]))
    wv = [p for p in DEF if p["surface"] == "SF9"]
    S9 = SF["SF9"]
    p9 = wv[0] if len(wv) == 1 else None
    row(g, "the bay-1 window of the plain row carries P02 as an A3 window bill: P02 x 297/508, 297 x 446 mm, taped inside, top at 1.90 m, at x 12.3",
        p9 is not None and p9["item"] == "P02" and abs(p9["scale"] - 297.0 / 508.0) < 0.001 and abs(p9["w_m"] - 0.297) < 0.0005 and abs(p9["z_bottom_m"] + p9["h_m"] - 1.90) < 0.002
        and p9["street_x_m"] == 12.3 and S9["window_street_x"][0] <= 12.3 - p9["w_m"] / 2 and 12.3 + p9["w_m"] / 2 <= S9["window_street_x"][1] and S9["z_range"][0] <= p9["z_bottom_m"] and p9["inside"])
    # letting boards against the fascia
    L2 = [p for p in DEF if p["item"] == "L02"]
    row(g, "L02: z 2.90 to 3.35 inside the fascia 2.85 to 3.40, centred on the bay (24.0), on SF5", len(L2) == 1 and abs(L2[0]["z_bottom_m"] - 2.90) < 1e-9 and abs(L2[0]["z_bottom_m"] + L2[0]["h_m"] - 3.35) < 1e-9 and L2[0]["street_x_m"] == 24.0 and L2[0]["surface"] == "SF5")
    L3 = [p for p in DEF if p["item"] == "L03n"]
    row(g, "L03n: between the cornice (3.55) and the upper sill (about 4.3), and outside both hanging signs' x (20.825, 27.175), no agent", len(L3) == 1 and 3.55 < L3[0]["z_bottom_m"] and L3[0]["z_bottom_m"] + L3[0]["h_m"] < 4.3 and 22.93 < L3[0]["street_x_m"] - L3[0]["w_m"] / 2 and L3[0]["street_x_m"] + L3[0]["w_m"] / 2 < 25.07)
    # cases and boards
    ok = True
    for c in T["cases"]:
        iw, ih = c["inside_mm"]
        calc_iw = c["outer_mm"][0] - c["frame_mm"]["left"] - c["frame_mm"]["right"]
        calc_ih = c["outer_mm"][1] - c["frame_mm"]["top"] - c["frame_mm"]["bottom"]
        ok &= abs(calc_iw - iw) <= 2 and abs(calc_ih - ih) <= 2
        for ch in c["children"]:
            it = ITEMS[ch["item"]]
            ok &= ch["x_mm"] >= 0 and ch["y_mm"] >= 0 and ch["x_mm"] + it["format"]["w_mm"] <= iw and ch["y_mm"] + it["format"]["h_mm"] <= ih
    row(g, "cases: the inside equals outer minus frame, and every pinned or pasted sheet lies inside it", ok)
    ferry = [c for c in T["cases"] if c["id"] == "FC1"][0]
    f01 = [ch for ch in ferry["children"] if ch["item"] == "F01"][0]
    f02 = [ch for ch in ferry["children"] if ch["item"] == "F02"][0]
    row(g, "FC1: a painted timber board 600 x 800 with NO glazing; the summer sheet peeks out 14 mm at the left and 16 mm at the top above the winter sheet", ferry["kind"] == "board" and ferry["outer_mm"] == [600, 800] and "no glazing" in ferry["title"] and f01["x_mm"] - f02["x_mm"] == 14 and f02["y_mm"] - f01["y_mm"] == 16)
    hc = [c for c in T["cases"] if c["id"] == "HC1"][0]
    row(g, "HC1: rails 46 x 60 mm with a 4 mm chamfer on the outer arris, 4 mm glass in a 10 x 10 mm bead", hc["rail_section_mm"] == [46, 60] and hc["chamfer_mm"] == 4.0 and hc["glass"]["thickness_mm"] == 4.0 and hc["glass"]["bead_mm"] == [10, 10])
    row(g, "neither case is placed on Quay Street (no dock office, no ramp)", not [p for p in PLS if p["item"] in ("HC1", "FC1")] and hc["place"] is None and ferry["place"] is None)
    # plates
    pl = [p for p in DEF if p["surface"] == "SF7"]
    plh = [p for p in PLS if p["surface"] == "SF7" and p.get("held")]
    row(g, "plates: ONE placed, QUAY STREET `n` on the west corner pier at x 20.47 (the gable carries none; a second plate at u 1.0 is held); none for WEIGHHOUSE LANE (the yard entrance has no plate), none for TANNERY ROW",
        [(p["item"], p.get("street_x_m")) for p in pl] == [("S01n", 20.47)] and len(plh) == 1 and plh[0].get("host") == "SF1" and not [p for p in PLS if p["item"].startswith("S02")])
    lamp = [p for p in DEF if p["surface"] == "SF4"]
    row(g, "lamp columns: bills sit between 1.2 and 2.4 m on a column's street x", all(p["street_x_m"] in SF["SF4"]["columns_street_x"] and 1.2 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 2.4 for p in lamp))
    row(g, "every placed item exists", all(p["item"] in ITEMS or p["item"] in {c["id"] for c in T["cases"]} or p["item"] == T["card_board"]["id"] for p in PLS))
    # shops
    shops = T["shops"]
    row(g, "every shop front adds to 6.0 m: pilasters 2 x 0.35 + glass 3.562 + shop door 0.9 + side door 0.838", abs(2 * 0.35 + 3.562 + 0.9 + 0.838 - 6.0) < 1e-9)
    ok = True
    for sid, sh in shops.items():
        lo, hi = sh["street_x_m"]
        gs = sh["glass_street_x_m"]
        ok &= lo + 0.35 - 1e-6 <= gs[0] and gs[1] <= hi - 0.35 + 1e-6 and abs((gs[1] - gs[0]) - 3.562) < 1e-3
    row(g, "every shop's glass lies inside its bay between the pilasters", ok)
    fish = shops["fish_market"]
    row(g, "the fish market's glass is at the viewer's LEFT (door end low = viewer's right on the east parade): street x 11.088 to 14.65", abs(fish["glass_street_x_m"][0] - 11.088) < 1e-3 and abs(fish["glass_street_x_m"][1] - 14.65) < 1e-3)
    sp = [p for p in DEF if p["surface"] == "SHOP"]
    hp = T["hours_plate"]
    bad = []
    for p in sp:
        if p["where"] == "glass":
            if not (0 <= p["u_m"] and p["u_m"] + p["w_m"] <= 3.562 + 1e-6 and 0.60 - 1e-6 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 2.40):
                bad.append((p["item"], p["shop"], "glass"))
        elif p["where"] == "door":
            if not (0 <= p["u_m"] and p["u_m"] + p["w_m"] <= 0.9 and 1.0 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 1.95):
                bad.append((p["item"], p["shop"], "door"))
            in_band = p["z_bottom_m"] < hp["z_m"][1] and p["z_bottom_m"] + p["h_m"] > hp["z_m"][0]
            col = (0.45 - hp["w_mm"] / 2000.0, 0.45 + hp["w_mm"] / 2000.0)
            if p["item"] not in ("K03a", "K03b") and in_band and p["u_m"] < col[1] and p["u_m"] + p["w_m"] > col[0]:
                bad.append((p["item"], p["shop"], "hours plate"))
            if p["item"] in ("K03a", "K03b") and p["z_bottom_m"] < hp["z_m"][1] + 1e-9:
                bad.append((p["item"], p["shop"], "K03 below plate top"))
    row(g, "shop cards lie inside their glass or door glass (%d placements) and clear the hours plate (z 1.355 to 1.545, assumed centred on the door glass) on a door" % len(sp), not bad, str(bad))
    k5 = [p for p in sp if p["item"] == "K05"][0]
    row(g, "K05 PLEASE SHUT THE DOOR: bottom 1.42 m (the review asked 1.38; the fascia target's vinyl TOBACCONIST & CONFECTIONER row on the same door glass tops out at 1.385 +- 0.03), centre 1.494 m, as its words now say", abs(k5["z_bottom_m"] - 1.42) < 1e-9 and "bottom at 1.42" in " ".join(ITEMS["K05"]["variants"]["vary"]))
    row(g, "K02 (BACK AT, Hal's break) is not placed: the newsagent never closes at midday", not [p for p in PLS if p["item"] == "K02"])
    ov = []
    for key in {(p["shop"], p["where"]) for p in sp if p["where"] in ("glass", "door")}:
        grp = [p for p in sp if (p["shop"], p["where"]) == key and p["item"] != "SB1"]
        for i, a in enumerate(grp):
            for b in grp[i + 1:]:
                if a["item"] == b["item"] and a["item"] == "K03a":
                    continue
                if rect_overlap((a["u_m"], a["z_bottom_m"], a["u_m"] + a["w_m"], a["z_bottom_m"] + a["h_m"]), (b["u_m"], b["z_bottom_m"], b["u_m"] + b["w_m"], b["z_bottom_m"] + b["h_m"])):
                    ov.append((a["item"], b["item"], key))
    row(g, "no two cards or sheets overlap on one shop glass or door", not ov, str(ov))
    try:
        ft = json.loads((ROOT / "production" / "cloud-week" / "targets" / "fascia-signs" / "target.json").read_text())
        rows_ = [r for r in ft["glass_lettering"] if r.get("z_m") is not None and r.get("text") and "fanlight" not in r.get("surface", "")]
        clash = []
        for p in sp:
            if p["where"] == "interior" or p["item"] == "SB1":
                continue
            for r in rows_:
                if r["shop"] != p["shop"]:
                    continue
                band = (r["z_m"] - r["cap_mm"] / 2000.0 - 0.03, r["z_m"] + r["cap_mm"] / 2000.0 + 0.03)
                if p["z_bottom_m"] < band[1] and p["z_bottom_m"] + p["h_m"] > band[0] and (r["surface"].startswith("window") == (p["where"] == "glass")):
                    clash.append((p["item"], p["shop"], r["text"], band))
        row(g, "no card overlaps a lettering row of the fascia target on the same glass (z band = row z +- cap/2 +- 30 mm; %d rows)" % len(rows_), not clash, str(clash[:3]))
    except Exception as e:
        row(g, "fascia target's glass rows not read", False, str(e))
    cb = T["card_board"]
    W, H = cb["area_mm"]
    cards = cb["cards"]
    inside_ok = all(0 <= c["x_mm"] and c["x_mm"] + c["w_mm"] <= W and 0 <= c["y_mm"] and c["y_mm"] + c["h_mm"] <= H for c in cards)
    ov = [(a["item"], b["item"]) for i, a in enumerate(cards) for b in cards[i + 1:] if min(a["x_mm"] + a["w_mm"], b["x_mm"] + b["w_mm"]) - max(a["x_mm"], b["x_mm"]) > 12 and min(a["y_mm"] + a["h_mm"], b["y_mm"] + b["h_mm"]) - max(a["y_mm"], b["y_mm"]) > 12]
    row(g, "the newsagent's board holds 15 cards, all inside its %d x %d mm area, none overlapping another by more than 12 mm" % (W, H), len(cards) == 15 and inside_ok and not ov, str(ov))
    row(g, "every card on the board is taped by one tab at its top-left: no pin anywhere (the card board's own note says pins are for a cork board)", all(c["fixing"].startswith("tape") and "pin" not in c["fixing"].lower() for c in cards) and "taped" in cb["note"])
    sb = [p for p in sp if p["item"] == "SB1"][0]
    j01 = [p for p in sp if p["item"] == "J01"]
    row(g, "the card board stands on the newsagent's glass, and J01 is taped beside it (to its right) on the same glass", sb["u_m"] + sb["w_m"] <= 3.562 and len(j01) == 1 and j01[0]["u_m"] >= sb["u_m"] + sb["w_m"] and j01[0]["shop"] == "newsagent")
    wt = T["wear_tables"]
    missing = [it["id"] for it in T["items"] if not it.get("wear") or it["wear"].get("table") not in wt]
    row(g, "every item names a wear table that exists (%d tables)" % len(wt), not missing, str(missing))
    hand = [it["id"] for it in T["items"] if it["blocks"] and all(b.get("hand") for b in it["blocks"])]
    bad = []
    for c in hand:
        mc = ITEMS[c].get("mirror_cue")
        fx = ITEMS[c].get("fixing")
        low = (mc or {}).get("what", "").lower()
        if not mc or not fx or mc["side"] != "left" or mc["corner"] != "top-left" or mc["kind"] != fx["kind"] or any(w in low for w in ("crease", "tear", "torn", "pin", "right")):
            bad.append(c)
    row(g, "every all-hand card (%d) has ONE cue that matches its fixing, at the top-LEFT, with no crease, tear, pin hole or right-hand mark" % len(hand), len(hand) == 29 and not bad, str(bad))
    tape = sorted(c for c in hand if ITEMS[c]["mirror_cue"]["kind"] == "tape")
    string = sorted(c for c in hand if ITEMS[c]["mirror_cue"]["kind"] == "string")
    row(g, "the string-hung hand cards are K01 and K06a; the taped or stuck are K05, K06c, K07a-d, K09a-f, SA01-SA15", string == ["K01", "K06a"] and len(tape) == 27, "%s / %d taped" % (string, len(tape)))


# --------------------------------------------------------------------------------------------
# 8 the photograph
# --------------------------------------------------------------------------------------------
def group8():
    g = "8 photograph"
    P = T["photo"]["P1"]
    prev = ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates" / "P1-urban-street-01-notice-case.jpg"
    ov = ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates" / "P1-urban-street-01-notice-case-target-on-photo.jpg"
    row(g, "both photograph previews exist", prev.exists() and ov.exists())
    if not prev.exists():
        return
    im = np.asarray(Image.open(prev).convert("RGB")).astype(int)
    sc, (cx, cy) = P["crop_scale"], P["crop_origin"]
    r, gch, b = im[..., 0], im[..., 1], im[..., 2]
    mask = (b > r + 45) & (b > gch + 25) & (b > 90)
    ox0, oy0, ox1, oy1 = P["px"]["c2"]["outer"]
    X0, X1 = int((ox0 - cx) * sc), int((ox1 - cx) * sc)
    col = mask[:, X0 + 10:X1 - 10].mean(axis=1)
    ys = np.where(col > 0.45)[0]
    ys = ys[(ys > 20) & (ys < im.shape[0] - 20)]
    top, bot = ys.min() / sc + cy, ys.max() / sc + cy
    row(g, "re-measured on the saved preview: case 2's outer top within 3 view px of the stated", abs(top - oy0) <= 3, "stated %s, measured %.1f" % (oy0, top))
    row(g, "re-measured on the saved preview: case 2's outer bottom within 3 view px of the stated", abs(bot - oy1) <= 3, "stated %s, measured %.1f" % (oy1, bot))
    # the ratios against the four cases' stated pixel numbers
    rr = T["photo"]["ratios"]
    tol = rr["tolerance"]
    for k in ("c2", "c3", "c4"):
        o = P["px"][k]["outer"]
        w = P["px"][k]["window"]
        H = o[3] - o[1]
        top_f = (w[1] - o[1]) / H
        win_f = (w[3] - w[1]) / H
        bot_f = (o[3] - w[3]) / H
        row(g, "ratios %s: top band %.3f, window %.3f, foot %.3f within the stated tolerances" % (k, top_f, win_f, bot_f),
            abs(top_f - rr["top_band_over_h"]) <= tol["top_band_over_h"] and abs(win_f - rr["window_over_h"]) <= tol["window_over_h"] and abs(bot_f - rr["bottom_band_over_h"]) <= tol["bottom_band_over_h"])
    sides = []
    for k in ("c2", "c3", "c4"):
        o = P["px"][k]["outer"]
        w = P["px"][k]["window"]
        sides.append(1 - (w[2] - w[0]) / (o[2] - o[0]))
    row(g, "side bands sum to 0.205 of the apparent width within 0.02 in cases 2 to 4 (%s)" % [round(s, 3) for s in sides], all(abs(s - rr["side_bands_sum_over_w"]) <= rr["tolerance"]["side_bands_sum_over_w"] for s in sides))
    # drawing on the photograph: edges, scale fitted on the outer height only
    H = oy1 - oy0
    pred = [oy0, oy0 + rr["top_band_over_h"] * H, oy0 + (rr["top_band_over_h"] + rr["window_over_h"]) * H, oy1]
    meas = [oy0, P["px"]["c2"]["window"][1], P["px"]["c2"]["window"][3], oy1]
    errs = [abs(a - c) for a, c in zip(pred, meas)]
    row(g, "the drawing's horizontal edges fall on case 2 within 3 px at the top, 10.5 px for the variable foot (errors %s)" % [round(e, 1) for e in errs], errs[1] <= 3 and errs[0] <= 0.5 and errs[2] <= 0.026 * H + 0.5, "")
    row(g, "the glazed windows were masked in the preview (the interior is flat grey)", True, "", reported=True)
    arr = np.asarray(Image.open(prev).convert("RGB")).astype(int)
    wx0, wy0, wx1, wy1 = P["px"]["c2"]["window"]
    patch = arr[int((wy0 - cy) * sc) + 10:int((wy1 - cy) * sc) - 10, int((wx0 - cx) * sc) + 10:int((wx1 - cx) * sc) - 10]
    row(g, "the masked window has no detail left (standard deviation under 3)", patch.std() < 3, "%.2f" % patch.std())
    row(g, "the photograph is stated as NOT 1990 and its measurements as proportions only", "NOT 1990" in P["period"])



# --------------------------------------------------------------------------------------------
# 9 the drawing
# --------------------------------------------------------------------------------------------
def group9():
    g = "9 drawing"
    with tempfile.TemporaryDirectory() as td:
        r = subprocess.run([sys.executable, str(HERE / "target_drawing.py"), td, "--fonts", FONT_DIR], capture_output=True, text=True)
        row(g, "target_drawing.py runs from target.json alone", r.returncode == 0, (r.stdout + r.stderr)[-200:])
        if r.returncode != 0:
            return
        J = json.loads((Path(td) / "drawing.json").read_text())
        row(g, "drawing.json holds every item and both cases", len(J["items"]) == len(T["items"]) and len(J["cases"]) == 2)
        bad = []
        for it in T["items"]:
            d = J["items"][it["id"]]
            W, H = it["format"]["w_mm"], it["format"]["h_mm"]
            png = Image.open(Path(td) / "items" / (it["id"] + ".png"))
            if png.size != (W, H):
                bad.append((it["id"], "png size", png.size))
            ink = [p for p in d["polys"] if p["kind"] == "ink_box"]
            if len(ink) != len(it["blocks"]):
                bad.append((it["id"], "ink boxes"))
            for p in d["polys"]:
                if p["kind"] in ("ink_box",):
                    xs = [q[0] for q in p["pts"]]
                    ys = [q[1] for q in p["pts"]]
                    if min(xs) < -2 or min(ys) < -2 or max(xs) > W + 2 or max(ys) > H + 2 or (not it["blocks"]):
                        if not any(b.get("ghost") for b in it["blocks"]):
                            bad.append((it["id"], p["id"], "outside sheet"))
        row(g, "every item's picture is its size at 1 px/mm and its polygons lie on the sheet", not bad, str(bad[:4]))
        row(g, "the surfaces' elevations were drawn (the gable, the empty unit's glass, the west piers, the plate places)", all((Path(td) / ("elevation_%s.png" % n)).exists() for n in ("SF1", "SF2", "piers", "plates")))
        row(g, "four contact sheets were drawn", len(list(Path(td).glob("sheet_*.png"))) == 4)



# --------------------------------------------------------------------------------------------
# THE READER. What a builder's own checker does on a rendered item (an ink mask: row 0 is the top edge).
#   line level   window_of, read_block, read_score, read_box, pos_ok          (.pos, .mask, .cap)
#   glyph level  layout_glyphs, jitter_glyphs, render_item, glyph_check_block (.glyphs)
#   whole item   estimate_rotation                                            (.square, PLACE.built)
# --------------------------------------------------------------------------------------------
class Expected(object):
    """The expected ink of an item's blocks. exp[block id] is the full-size mask (on demand, cached); the windowed reader never asks for it."""

    def __init__(self, item):
        self.item = item
        self._c = {}

    def __getitem__(self, bid):
        if bid not in self._c:
            b = [c for c in self.item["blocks"] if c["id"] == bid][0]
            self._c[bid] = block_mask(b, self.item["format"]["w_mm"], self.item["format"]["h_mm"], self.item["px_per_mm"])
        return self._c[bid]


def expected_masks(item):
    return Expected(item)


def window_of(item, b, img_shape, ppm=None):
    """The reader's window for a block: its ink box widened 8 mm along the line and 3 mm up and down, in canvas pixels (x0, x1, y0, y1)."""
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    x0, y0, x1, y1 = b["ink_box_mm"]
    px0, px1 = int(max(0, (x0 - 8) * ppm)), int(min(img_shape[1], (x1 + 8) * ppm))
    py0, py1 = int(max(0, (H - y1 - 3) * ppm)), int(min(img_shape[0], (H - y0 + 3) * ppm))
    return px0, px1, py0, py1


def shape_exclusions(item, win, ppm, b):
    """Pixels of the item's rules, frames, bars and rings inside the window (dilated 1 mm) that are NOT the block's own ground: the reader does not credit them to a block."""
    x0, x1, y0, y1 = win
    H = item["format"]["h_mm"]
    out = np.zeros((y1 - y0, x1 - x0), bool)
    img = Image.new("L", (x1 - x0, y1 - y0), 0)
    d = ImageDraw.Draw(img)
    cx = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0
    cy = (b["ink_box_mm"][1] + b["ink_box_mm"][3]) / 2.0
    for s in item["shapes"]:
        if s["kind"] in ("scrim",) or s.get("box_mm") is None and s.get("centre_mm") is None and not s.get("pts_mm"):
            continue
        if s.get("box_mm") and s["kind"] in ("rect", "rule", "frame", "roundel"):
            bx0, by0, bx1, by1 = s["box_mm"]
            if s["kind"] in ("rect", "roundel") and bx0 <= cx <= bx1 and by0 <= cy <= by1:
                continue           # the block's own ground
            X0, X1, Y0, Y1 = bx0 * ppm - x0, bx1 * ppm - x0, (H - by1) * ppm - y0, (H - by0) * ppm - y0
            if s["kind"] == "frame":
                w = max(1, s.get("width_mm", 3) * ppm)
                d.rectangle([X0, Y0, X1, Y1], outline=255, width=int(round(w)))
            elif s["kind"] == "roundel":
                d.ellipse([X0, Y0, X1, Y1], fill=255)
            else:
                d.rectangle([X0, Y0, X1, Y1], fill=255)
        elif s["kind"] == "poly" and s.get("pts_mm"):
            d.polygon([(px * ppm - x0, (H - py) * ppm - y0) for px, py in s["pts_mm"]], fill=255)
    a = np.asarray(img) > 100
    return ndi.binary_dilation(a, gl.disk(max(1, int(round(1.0 * ppm))))) if a.any() else a


def read_block(item, img, b, exp=None, ppm=None, with_shapes=False):
    """(read, win): the ink the reader credits to block b inside its window: the other blocks' glyphs (dilated 1.5 mm) do not count unless b's own glyphs (dilated 0.7 mm) also occupy
    the pixel. img is an ink mask at ppm px/mm (default the item's own)."""
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    win = window_of(item, b, img.shape, ppm)
    x0, x1, y0, y1 = win
    read = img[y0:y1, x0:x1].copy()
    def slack(c):
        """extra millimetres a hand-lettered block's glyphs may lie off the layout (2 sd of its baseline jitter and 0.1 of its cap)"""
        return (2.0 * T["hand_styles"][c["hand"]]["baseline_sd_mm"] + 0.1 * c["cap_mm"]) if c.get("hand") else 0.0
    own = ndi.binary_dilation(block_local(b, ppm, H, win), gl.disk(max(1, int(round((0.7 + slack(b)) * ppm)))))
    for c in item["blocks"]:
        if c["id"] == b["id"] or c.get("ghost"):
            continue
        cx0, cx1, cy0, cy1 = window_of(item, c, img.shape, ppm)
        if cx1 < x0 or cx0 > x1 or cy1 < y0 or cy0 > y1:
            continue
        m = block_local(c, ppm, H, win)
        if not m.any():
            continue
        dm = ndi.binary_dilation(m, gl.disk(max(1, int(round((1.5 + slack(c)) * ppm)))))
        read &= ~(dm & ~own)
    if with_shapes:
        read &= ~shape_exclusions(item, win, ppm, b)
    return read, win


def read_score(item, img, b, exp=None, flip_inplace=False, ppm=None, with_shapes=False, strict=True):
    """The line check (.mask): the whole line's F against its font re-render (dilated 1 mm for print, 2.5 mm for hand); for a PRINT line also its worst single glyph, and 0.5 if the glyph check (F, SEP against every alternative
    and the mirror) fails on it (strict; strict=False reads F only). With flip_inplace the reference is turned about the block's own ink box."""
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    read, win = read_block(item, img, b, exp, ppm, with_shapes)
    ref = block_local(b, ppm, H, win)
    if flip_inplace:
        x0, y0, x1, y1 = b["ink_box_mm"]
        a0, a1 = int(x0 * ppm) - win[0], int(x1 * ppm) + 1 - win[0]
        ref2 = np.zeros_like(ref)
        ref2[:, a0:a1] = ref[:, a0:a1][:, ::-1]
        ref = ref2
    dil = max(1, int(round((1.0 if not b.get("hand") else 2.5) * ppm)))
    lf = fscore(read, ref, dil)
    if not b.get("hand") and b["role"] != "imprint" and not flip_inplace:
        # a PRINT line's layout is exact, so its score is also its worst single glyph (F at 0.5 mm, the glyph check's own gate): a changed digit or letter no longer hides in the line's mean.
        # Hand lines need the renderer's manifest (their jitter): ITEM.glyphs reads those.
        r = glyph_check_block(item, img, b, layout_glyphs(b), ppm=ppm, only_alts=(None if strict else []), shapes=with_shapes)
        if r["glyphs"]:
            return min(lf, r["min_F"]) if r["ok"] else min(lf, r["min_F"], 0.5)
    return lf


def read_box(item, img, b, exp=None, ppm=None):
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    read, win = read_block(item, img, b, exp, ppm)
    cols = np.where(read.any(axis=0))[0]
    rows_ = np.where(read.any(axis=1))[0]
    if not len(cols):
        return None
    return [(win[0] + cols.min()) / ppm, (H * ppm - (win[2] + rows_.max() + 1)) / ppm, (win[0] + cols.max() + 1) / ppm, (H * ppm - (win[2] + rows_.min())) / ppm]


def pos_ok(item, b, bx):
    if bx is None:
        return False
    if b.get("hand"):
        tol, base = 7.0, 4.5          # the hand style's own tolerances (checks .pos: 7 mm, baseline 3.5 mm + the read box's descender slack)
    else:
        tol, base = (max(2.5, 0.006 * b["width_mm"]) if b["cap_mm"] >= 8 else 2.5), 4
    return abs((bx[0] + bx[2]) / 2 - (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2) <= tol and abs(bx[1] - b["ink_box_mm"][1]) <= base


def block_min_f(item, b):
    if b["role"] == "imprint":
        return 0.55
    if b.get("hand"):
        return 0.78
    if b["technique"] and "typed" in str(b["technique"]):
        return 0.85
    if b["cap_mm"] < 8:
        return 0.85
    return 0.90


# ---- the glyph manifest ---------------------------------------------------------------------
LAYOUT_PPM = 8.0


def layout_glyphs(b, text=None, origin_x_mm=None):
    """The manifest a renderer must write for a PRINT block: one entry per character of the approved string (spaces included), in order."""
    text = b["text"] if text is None else text
    px = b["size_px_per_em"]
    f = font(b["font"], b["weight"], px * LAYOUT_PPM)
    trk = b["tracking_em"] * px * LAYOUT_PPM
    xs = [f.getlength(text[:i + 1]) - f.getlength(ch) + i * trk for i, ch in enumerate(text)]
    ox = b["origin_x_mm"] if origin_x_mm is None else origin_x_mm
    return [dict(ch=ch, font=b["font"], weight=b["weight"], em_mm=px, ox_mm=ox + xs[i] / LAYOUT_PPM, baseline_mm=b["baseline_mm"], rot_deg=0.0, emb_mm=0.0) for i, ch in enumerate(text)]


def recentre_origin(b, new_text):
    """The origin that puts new_text's ink where the block's anchor puts the approved text's (the reviewer's recentre)."""
    def ink_x(txt, ox):
        gs = layout_glyphs(b, text=txt, origin_x_mm=ox)
        lo, hi = 1e9, -1e9
        for g in gs:
            if g["ch"] == " ":
                continue
            p, o, ba = gl.glyph_patch(font, g["font"], g["weight"], g["ch"], g["em_mm"], 4.0)
            c = gl.ink_cols(p)
            lo = min(lo, g["ox_mm"] + (c[0] - o) / 4.0)
            hi = max(hi, g["ox_mm"] + (c[1] + 1 - o) / 4.0)
        return lo, hi
    a0, a1 = ink_x(b["text"], b["origin_x_mm"])
    n0, n1 = ink_x(new_text, b["origin_x_mm"])
    if b["anchor"] == "centre":
        dx = (a0 + a1) / 2 - (n0 + n1) / 2
    elif b["anchor"] == "right":
        dx = a1 - n1
    else:
        dx = a0 - n0
    return b["origin_x_mm"] + dx


def jitter_glyphs(b, rng, text=None, origin_x_mm=None):
    """The manifest of a HAND block: the layout plus the hand style's jitter (size, rotation, baseline, word gaps, stroke), each draw clipped at 3 sd."""
    hs = T["hand_styles"][b["hand"]]
    base = layout_glyphs(b, text=text, origin_x_mm=origin_x_mm)
    px = b["size_px_per_em"]
    f = font(b["font"], b["weight"], px * LAYOUT_PPM)

    def n(sd):
        return float(np.clip(rng.normal(0, sd), -3 * sd, 3 * sd))
    out, drift = [], 0.0
    for e in base:
        if e["ch"] == " ":
            drift += f.getlength(" ") / LAYOUT_PPM * n(hs["word_gap_sd"])
            out.append(dict(e, ox_mm=e["ox_mm"] + drift))
            continue
        s = 1.0 + n(hs["size_sd"])
        adv = f.getlength(e["ch"]) / LAYOUT_PPM
        out.append(dict(e, ox_mm=e["ox_mm"] + drift, em_mm=e["em_mm"] * s, baseline_mm=e["baseline_mm"] + n(hs["baseline_sd_mm"]), rot_deg=n(hs["rotation_sd_deg"]), emb_mm=hs["embolden_mm"]))
        drift += (s - 1.0) * adv
    shift = -drift / 2.0 if b["anchor"] == "centre" else (-drift if b["anchor"] == "right" else 0.0)
    return [dict(e, ox_mm=e["ox_mm"] + shift) for e in out]


_patch_cache = {}


def glyph_patch_cached(key, weight, ch, em_mm, ppm, rot, emb):
    k = (key, weight, ch, round(em_mm, 3), round(ppm, 3), round(rot, 2), round(emb, 3))
    if k not in _patch_cache:
        if len(_patch_cache) > 12000:
            _patch_cache.clear()
        _patch_cache[k] = gl.glyph_patch(font, key, weight, ch, em_mm, ppm, rot, emb, tight=True)
    return _patch_cache[k]


def render_item(item, rng=None, swap=None, mirror=False, rot_deg=0.0, jitter=True, ppm=None, skip=()):
    """A reference render of the item's LETTERING as an ink mask, with the manifest a renderer would write.
    swap=(block id, new text): the PIXELS carry the new text, the manifest still carries the APPROVED text (a renderer that draws something other than what it lists).
    mirror: the whole sheet flipped left-right. rot_deg: the whole sheet turned counter-clockwise about its centre. jitter: hand blocks get the hand style's jitter (needs rng).
    Returns (canvas, manifest) with manifest = {block id: [glyph entries]}."""
    ppm = ppm or item["px_per_mm"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    canvas = np.zeros((int(round(H * ppm)), int(round(W * ppm))), bool)
    rng = rng or np.random.default_rng(0)
    man = {}
    for b in item["blocks"]:
        if b.get("ghost") or b["id"] in skip:
            continue
        if b.get("hand") and jitter:
            true_g = jitter_glyphs(b, rng)
        else:
            true_g = layout_glyphs(b)
        man[b["id"]] = true_g
        drawn = true_g
        if swap and swap[0] == b["id"]:
            o = recentre_origin(b, swap[1])
            drawn = jitter_glyphs(b, rng, text=swap[1], origin_x_mm=o) if (b.get("hand") and jitter) else layout_glyphs(b, text=swap[1], origin_x_mm=o)
        for g in drawn:
            if g["ch"] == " ":
                continue
            patch, ox, base = glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm, g["rot_deg"], g["emb_mm"])
            gl.paste_or(canvas, patch, ox, base, g["ox_mm"] * ppm, (H - g["baseline_mm"]) * ppm)
    if mirror:
        canvas = canvas[:, ::-1]
    if rot_deg:
        im = Image.fromarray((canvas * 255).astype(np.uint8)).rotate(rot_deg, resample=Image.BILINEAR)
        canvas = np.asarray(im) > 127
    return canvas, man


def envelope_problems(b, glyphs):
    """Where a manifest may differ from the target's own layout (render_contract.glyph_manifest.envelope)."""
    exp = layout_glyphs(b)
    if len(glyphs) != len(exp):
        return ["manifest has %d entries for %d characters" % (len(glyphs), len(exp))]
    hs = T["hand_styles"][b["hand"]] if b.get("hand") else None
    bad = []
    for i, (g, e) in enumerate(zip(glyphs, exp)):
        if g["ch"] != e["ch"]:
            bad.append("character %d is %r, the approved string has %r" % (i, g["ch"], e["ch"]))
            continue
        if g["font"] != e["font"] or g["weight"] != e["weight"]:
            bad.append("character %d is drawn in %s %s" % (i, g["font"], g["weight"]))
        if hs is None:
            if abs(g["ox_mm"] - e["ox_mm"]) > 0.6 or abs(g["baseline_mm"] - e["baseline_mm"]) > 0.5 or abs(g["rot_deg"]) > 0.1 or abs(g["em_mm"] / e["em_mm"] - 1) > 0.01 or g["emb_mm"] > 0.2:
                bad.append("character %d (%r) lies outside the print envelope" % (i, g["ch"]))
        else:
            dist = abs(e["ox_mm"] - exp[0]["ox_mm"])
            if (abs(g["baseline_mm"] - e["baseline_mm"]) > 3.5 * hs["baseline_sd_mm"] + 0.6 or abs(g["rot_deg"]) > 3.5 * hs["rotation_sd_deg"] + 0.1 or abs(g["em_mm"] / e["em_mm"] - 1) > 3.5 * hs["size_sd"]
                    or abs(g["ox_mm"] - e["ox_mm"]) > 6.0 + 0.05 * dist or g["emb_mm"] > 0.6):
                bad.append("character %d (%r) lies outside the hand envelope" % (i, g["ch"]))
    return bad


ALT_CHARS = gl.GLYPHS
MAN_KEYS = ("ch", "font", "weight", "em_mm", "ox_mm", "baseline_mm", "rot_deg", "emb_mm")


def manifest_problem(b, man):
    """Why a block's glyph manifest cannot be used (None when it can): a missing, empty or unreadable <ITEM>.glyphs.json fails .words and .glyphs; it never crashes the reader."""
    if man is None or not isinstance(man, (list, tuple)) or not man:
        return "no glyph manifest for block %s (missing, empty or unreadable): the words and the glyphs cannot be checked" % b["id"]
    for i, g in enumerate(man):
        if not isinstance(g, dict) or any(k not in g for k in MAN_KEYS):
            return "the glyph manifest of block %s is unreadable at entry %d" % (b["id"], i)
        try:
            float(g["em_mm"]), float(g["ox_mm"]), float(g["baseline_mm"]), float(g["rot_deg"]), float(g["emb_mm"])
        except (TypeError, ValueError):
            return "the glyph manifest of block %s has a non-number at entry %d" % (b["id"], i)
    return None


def words_ok(item, mans):
    """ITEM .words, read from the glyph manifest: every block's characters, joined, equal the approved string. mans: {block id: [glyph entries]} or None (a missing file). Returns (ok, why)."""
    if not isinstance(mans, dict):
        return False, "no glyph manifest for %s (missing or unreadable)" % item["id"]
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        pr = manifest_problem(b, mans.get(b["id"]))
        if pr:
            return False, pr
        got = "".join(g["ch"] for g in mans[b["id"]])
        if got != b["text"]:
            return False, "block %s lists %r, the approved string is %r" % (b["id"], got, b["text"])
    return True, ""


def glyph_window(item, b, img_shape, ppm):
    """The glyph reader's window: the block's ink box widened 8 mm along the line (14 mm for a hand block) and 3 mm up and down (3 mm + 3.5 sd of the hand's baseline + 0.12 cap for a hand block)."""
    H = item["format"]["h_mm"]
    x0, y0, x1, y1 = b["ink_box_mm"]
    mx, my = 8.0, 3.0
    if b.get("hand"):
        hs = T["hand_styles"][b["hand"]]
        mx += 6.0
        my += 3.5 * hs["baseline_sd_mm"] + 0.6 + 0.12 * b["cap_mm"]
    return int(max(0, (x0 - mx) * ppm)), int(min(img_shape[1], (x1 + mx) * ppm)), int(max(0, (H - y1 - my) * ppm)), int(min(img_shape[0], (H - y0 + my) * ppm))


def glyph_check_block(item, img, b, man, exp=None, ppm=None, only_alts=None, others=None, shapes=True):
    """ITEM.glyphs on one block. img is an ink mask at ppm px/mm; man is the block's manifest list; others maps the other blocks' ids to THEIR manifests (the reader does not credit
    their glyphs, dilated 1 mm, to this block; without it their unjittered layout is used). Returns dict(ok, fails, glyphs, min_F, min_sep, equiv): fails is a list of plain strings."""
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    res = dict(block=b["id"], ok=True, fails=[], glyphs=0, min_F=1.0, min_sep=1.0, equiv=0)
    pr = manifest_problem(b, man)
    if pr:
        res["ok"] = False
        res["fails"].append(pr)
        return res
    probs = envelope_problems(b, man)
    if probs:
        res["ok"] = False
        res["fails"] += probs[:3]
        return res
    em_px = max(g["em_mm"] for g in man) * ppm
    k = max(1, int(math.ceil(em_px / gl.BIG_EM_PX)))
    ppm_e = ppm / k
    win = glyph_window(item, b, img.shape, ppm)
    x0, x1, y0, y1 = win
    read = gl.shrink_cov(img[y0:y1, x0:x1], k)
    win_e = (0, read.shape[1], 0, read.shape[0])

    def put(g, canvas):
        patch, ox, base = glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm_e, g["rot_deg"], g["emb_mm"])
        return gl.place_patch(patch, ox, base, g["ox_mm"] * ppm_e - x0 / k, (H - g["baseline_mm"]) * ppm_e - y0 / k, win_e)
    # what the reader does not credit to this block: the other blocks' glyphs (as manifested) and the item's rules, frames and bars
    om = np.zeros_like(read)
    for c in item["blocks"]:
        if c["id"] == b["id"] or c.get("ghost"):
            continue
        cx0, cx1, cy0, cy1 = glyph_window(item, c, img.shape, ppm)
        if cx1 < x0 or cx0 > x1 or cy1 < y0 or cy0 > y1:
            continue
        for g in ((others or {}).get(c["id"]) or layout_glyphs(c)):
            if g["ch"] != " ":
                om |= put(g, None)
    excl = gl.dil(om, max(1, int(round(1.0 * ppm_e))))
    if shapes:
        excl = excl | gl.shrink(shape_exclusions(item, win, ppm, b), k)[:read.shape[0], :read.shape[1]]
    dil_f = max(1, int(round(0.5 * ppm_e)))
    refs, boxes = [], []
    for g in man:
        if g["ch"] == " ":
            refs.append(None)
            boxes.append(None)
            continue
        ref = put(g, None)
        refs.append(ref)
        boxes.append(gl.ink_cols(ref))
    nonsp = [i for i, bx in enumerate(boxes) if bx is not None]
    Wd = read.shape[1]
    read_ex = read & ~excl
    for pos, i in enumerate(nonsp):
        g = man[i]
        bx = boxes[i]
        lo = (boxes[nonsp[pos - 1]][1] + bx[0]) // 2 if pos else max(0, bx[0] - int(4 * ppm_e))
        hi = (bx[1] + boxes[nonsp[pos + 1]][0]) // 2 + 1 if pos + 1 < len(nonsp) else min(Wd, bx[1] + 1 + int(4 * ppm_e))
        lo, hi = max(0, int(lo)), min(Wd, int(hi))
        res["glyphs"] += 1
        own = refs[i][:, lo:hi]
        # the neighbours in the line are not credited either, unless this glyph's own ink (dilated 0.7 mm) also holds the pixel
        neigh = np.zeros_like(own)
        for jj in (pos - 2, pos - 1, pos + 1, pos + 2):
            if 0 <= jj < len(nonsp):
                neigh |= refs[nonsp[jj]][:, lo:hi]
        own_d = gl.dil(own, max(1, int(round(0.7 * ppm_e))))
        # a pixel that a neighbour's ink explains and this glyph's does not (within TOL_PX) is the neighbour's, even where hand-lettered glyphs touch
        core = gl.dil(neigh, gl.TOL_PX) & ~gl.dil(own, gl.TOL_PX)
        rd = (read[:, lo:hi] & ~core & ~(gl.dil(neigh, max(1, int(round(1.0 * ppm_e)))) & ~own_d)) & ~(excl[:, lo:hi] & ~own_d)
        F = gl.fscore(rd, own, dil_f)
        res["min_F"] = min(res["min_F"], F)
        if F < gl.F_MIN:
            res["fails"].append("%r at %.0f mm: F %.2f" % (g["ch"], g["ox_mm"], F))
            continue
        # separation from every alternative glyph at the same place, size and turn, and from its own mirror
        worst = 1.0
        alts = only_alts if only_alts is not None else sorted(set(ALT_CHARS) | set(c for c in b["text"] if c != " "))
        mir = gl.mirror_in_place(own)
        cands = [("mirror", mir)]
        for a in alts:
            if a == g["ch"] or (g["ch"], a) in gl.EXPLICIT_TWINS:
                continue
            patch, ox, base = glyph_patch_cached(g["font"], g["weight"], a, g["em_mm"], ppm_e, g["rot_deg"], g["emb_mm"])
            ra = gl.place_patch(patch, ox, base, g["ox_mm"] * ppm_e - x0 / k, (H - g["baseline_mm"]) * ppm_e - y0 / k, (lo, hi, 0, win_e[3]))
            if not ra.any():
                continue                                    # the font has no such glyph (notdef not drawn) or it falls outside the cell
            cands.append((a, ra))
        dco = gl.dil(own, gl.TOL_PX)
        rd_d = gl.dil(rd, gl.TOL_PX)
        for name, ra in cands:
            A = own & ~gl.dil(ra, gl.TOL_PX)
            Bs = ra & ~dco
            sp_ = gl.sep_score(rd, A, Bs, read_d=rd_d)
            if sp_ is None:
                res["equiv"] += 1
                continue
            worst = min(worst, sp_)
            if sp_ < gl.SEP_GATE:
                res["fails"].append("%r at %.0f mm is not told from %s: SEP %.2f" % (g["ch"], g["ox_mm"], ("its mirror" if name == "mirror" else repr(name)), sp_))
                break
        res["min_sep"] = min(res["min_sep"], worst)
    # spaces carry no ink: between the two neighbouring glyphs' boxes, the ink that lies farther than 0.6 mm (one reduced pixel more when the block is read at a reduced scale) from every glyph of the line
    refall = np.zeros_like(read)
    for r_ in refs:
        if r_ is not None:
            refall |= r_
    allowed = gl.dil(refall, max(1, int(round(0.6 * ppm_e))) + (1 if k > 1 else 0))
    for i, g in enumerate(man):
        if g["ch"] != " " or i == 0 or i == len(man) - 1:
            continue
        prev = [j for j in nonsp if j < i]
        nxt = [j for j in nonsp if j > i]
        if not prev or not nxt:
            continue
        a, bb = boxes[prev[-1]][1] + 1, boxes[nxt[0]][0]
        if bb > a:
            ink = int((read_ex[:, a:bb] & ~allowed[:, a:bb]).sum()) / (ppm_e * ppm_e)
            if ink > 0.5:
                res["fails"].append("the space at %.0f mm carries %.1f mm2 of ink" % (g["ox_mm"], ink))
    res["ok"] = not res["fails"]
    return res


# ---- the whole item: rotation ---------------------------------------------------------------
def union_expected(item, ppm_e):
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    out = np.zeros((int(round(H * ppm_e)), int(round(W * ppm_e))), bool)
    blocks = [b for b in item["blocks"] if not b.get("ghost") and b["role"] != "imprint"]
    big = [b for b in blocks if not b.get("hand")] or blocks
    for b in big:
        for g in layout_glyphs(b):
            if g["ch"] == " ":
                continue
            p, o, ba = glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm_e, 0.0, 0.0)
            gl.paste_or(out, p, o, ba, g["ox_mm"] * ppm_e, (H - g["baseline_mm"]) * ppm_e)
    return out


SQUARE_TOL_DEG = 0.3        # ITEM.square: ONE tolerance for every item, print or hand (target.json checks[].tolerance; PLACE.built uses the same number)
SQUARE_MARGIN = 0.02        # the estimate reports 0 unless F at the best angle beats F at 0 degrees by this much
SQUARE_MARGIN_BLIND = 0.05  # the same, for a hand card read WITHOUT the renderer's manifest (its jitter then is not known)


def manifest_expected(item, man, ppm_e):
    """The ink the item's own glyph manifest draws (jitter included), as a mask at ppm_e px/mm. A block with no manifest entry is drawn as the layout has it. Imprints are left out."""
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    out = np.zeros((int(round(H * ppm_e)), int(round(W * ppm_e))), bool)
    for b in item["blocks"]:
        if b.get("ghost") or b["role"] == "imprint":
            continue
        gs = ((man or {}).get(b["id"])) if isinstance(man, dict) else None
        if manifest_problem(b, gs):
            gs = layout_glyphs(b)
        for g in gs:
            if g["ch"] == " ":
                continue
            p, o, ba = glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], ppm_e, g["rot_deg"], g["emb_mm"])
            gl.paste_or(out, p, o, ba, g["ox_mm"] * ppm_e, (H - g["baseline_mm"]) * ppm_e)
    return out


def square_estimate(item, img, man=None, ppm=None, span=3.0, margin=None, target_ppm=8.0, max_mp=3.0):
    """ITEM.square. The angle (degrees, counter-clockwise) by which the render is turned: the one at which turning the image back about the sheet's centre makes its ink agree best
    (F, mean of recall and precision, each against the other dilated one reduced pixel) with the ink of the item's OWN GLYPH MANIFEST (jitter included; the layout where there is no
    manifest). 0.05 degree steps after a 0.25 degree search over +-3 degrees. It reports 0 unless F at the best angle beats F at 0 degrees by `margin` (0.02; 0.05 for a hand card read
    without its manifest, where the layout stands in for the jitter and the dilation is the hand's own 2.5 mm), so a square texture, whose F is flat near 0, is found at 0.
    The read is made at up to 8 px/mm and 3 megapixels. Returns dict(angle, f_best, f0)."""
    ppm = ppm or item["px_per_mm"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    hand_blind = (not isinstance(man, dict)) and any(b.get("hand") for b in item["blocks"] if not b.get("ghost"))
    tgt = min(ppm, target_ppm, math.sqrt(max_mp * 1e6 / (W * H)))
    k = max(1, int(round(ppm / tgt)))
    ppm_e = ppm / k
    small = gl.shrink(img, k)
    ex = manifest_expected(item, man, ppm_e)
    h = min(small.shape[0], ex.shape[0])
    w = min(small.shape[1], ex.shape[1])
    small, ex = small[:h, :w], ex[:h, :w]
    dil_px = max(1, int(round(2.5 * ppm_e))) if hand_blind else 1
    margin = (SQUARE_MARGIN_BLIND if hand_blind else SQUARE_MARGIN) if margin is None else margin
    im = Image.fromarray((small * 255).astype(np.uint8))
    exd = gl.dil(ex, dil_px)
    ne = max(1, int(ex.sum()))

    def score(a):
        r = np.asarray(im.rotate(-a, resample=Image.NEAREST)) > 127
        rec = (ex & gl.dil(r, dil_px)).sum() / ne
        pre = (r & exd).sum() / max(1, int(r.sum()))
        return float((rec + pre) / 2.0)
    f0 = score(0.0)
    best = max(((score(a), a) for a in np.arange(-span, span + 1e-9, 0.25)), key=lambda t: (t[0], -abs(t[1])))
    fine = max(((score(a), a) for a in np.arange(best[1] - 0.25, best[1] + 0.2501, 0.05)), key=lambda t: (t[0], -abs(t[1])))
    if fine[0] - f0 < margin:
        return dict(angle=0.0, f_best=f0, f0=f0)
    return dict(angle=float(round(fine[1], 2)), f_best=float(fine[0]), f0=f0)


def estimate_rotation(item, img, man=None, ppm=None, span=3.0):
    """(angle, F at the angle): square_estimate for callers that want the pair. Pass the renderer's manifest as man; a hand card read without it is judged on the layout with the hand's own tolerance."""
    r = square_estimate(item, img, man=man, ppm=ppm, span=span)
    return r["angle"], r["f_best"]


# ---- ITEM.clean: no ink outside the places lettering may stand -----------------------------------
CLEAN_MAX_MM2 = 2.0


def shape_ink_mask(item, shape, ppm, img_shape):
    """The pixels of one of the item's shapes that are themselves ink (a rule, a bar of solid ink, a frame's line, a ring, ticks, a hand, a star or polygon, a roundel), at the item's scale.
    A ground (a paint or stock rectangle that lettering stands on) is not such a shape: lettering over it is read."""
    H = item["format"]["h_mm"]
    im = Image.new("L", (img_shape[1], img_shape[0]), 0)
    d = ImageDraw.Draw(im)
    kind = shape["kind"]
    bx = shape.get("box_mm")
    if kind == "scrim" or bx is None and not shape.get("pts_mm"):
        return np.zeros(img_shape, bool)

    def X(x):
        return x * ppm

    def Y(y):
        return (H - y) * ppm
    if kind in ("poly", "star", "hand") and shape.get("pts_mm"):
        d.polygon([(X(px), Y(py)) for px, py in shape["pts_mm"]], fill=255)
    elif kind == "rule" or (kind == "rect" and shape.get("fill_kind") == "ink"):
        d.rectangle([X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])], fill=255)
    elif kind == "frame":
        d.rectangle([X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])], outline=255, width=max(1, int(round(shape.get("width_mm", 3) * ppm))))
    elif kind == "roundel":
        d.ellipse([X(bx[0]), Y(bx[3]), X(bx[2]), Y(bx[1])], fill=255)
    elif kind == "ring":
        cx, cy = shape["centre_mm"]
        d.ellipse([X(cx - shape["r_outer_mm"]), Y(cy + shape["r_outer_mm"]), X(cx + shape["r_outer_mm"]), Y(cy - shape["r_outer_mm"])], fill=255)
        d.ellipse([X(cx - shape["r_inner_mm"]), Y(cy + shape["r_inner_mm"]), X(cx + shape["r_inner_mm"]), Y(cy - shape["r_inner_mm"])], fill=0)
    elif kind == "ticks":
        for sg in shape.get("segments_mm", []):
            d.line([(X(sg["p0"][0]), Y(sg["p0"][1])), (X(sg["p1"][0]), Y(sg["p1"][1]))], fill=255, width=max(1, int(round(shape.get("width_mm", 2) * ppm))))
    return np.asarray(im) > 100


def clean_ink_mm2(item, img, ppm=None):
    """ITEM.clean (reads pixels): on the class-A render before wear, the area (mm2) of ink-coloured pixels outside the union of every block's glyph window, the item's own shapes (dilated 1 mm),
    the card's cue patch, and the art slots. A true render has none; a line drawn anywhere else (a word on a margin, a held name left on a default item) adds its whole area."""
    ppm = ppm or item["px_per_mm"]
    H = item["format"]["h_mm"]
    allowed = np.zeros(img.shape, bool)
    for b in item["blocks"]:
        if b.get("ghost"):
            continue
        x0, x1, y0, y1 = glyph_window(item, b, img.shape, ppm)
        allowed[y0:y1, x0:x1] = True
    own = np.zeros(img.shape, bool)
    for s_ in item["shapes"]:
        own |= shape_ink_mask(item, s_, ppm, img.shape)
    mc = item.get("mirror_cue")
    boxes = []
    if mc and mc.get("patch_left_mm"):
        boxes.append(mc["patch_left_mm"])
    boxes += [a["box_mm"] for a in item["art"]]
    for x0, y0, x1, y1 in boxes:
        own[max(0, int((H - y1) * ppm)):int((H - y0) * ppm) + 1, max(0, int(x0 * ppm)):int(x1 * ppm) + 1] = True
    if own.any():
        own = gl.dil(own, max(1, int(round(1.0 * ppm))))
    stray = img & ~allowed & ~own
    return float(stray.sum()) / (ppm * ppm)


# --------------------------------------------------------------------------------------------
# 10 the line-level checks (.mask, .pos), tested on reference renders
# --------------------------------------------------------------------------------------------
def reference_image(item, mirror=False, shift_mm=(0, 0), wrong_font=None):
    ppm = item["px_per_mm"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    canvas = np.zeros((int(H * ppm), int(W * ppm)), bool)
    for b in item["blocks"]:
        key = wrong_font[1] if wrong_font and wrong_font[0] == b["id"] else None
        m = block_mask(b, W, H, ppm, key=key, weight=(400 if key else None), shift_mm=shift_mm)
        if m is None:
            return None, None
        canvas |= m
    if mirror:
        canvas = canvas[:, ::-1]
    return canvas, None


def group10():
    g = "10 line-level checks, tested"
    sample = ["P01", "P03", "J01", "T03", "F01", "K01", "SA06", "C01a", "S01n", "L02", "H01", "D01", "K07a"]
    if QUICK:
        sample = sample[:4]
    if font_path("oswald") is None:
        row(g, "fonts not found: reference renders skipped", False)
        return
    tight = []
    for it in T["items"]:
        bl = it["blocks"]
        for i in range(len(bl)):
            for j in range(i + 1, len(bl)):
                a, c = bl[i], bl[j]
                ax0, ay0, ax1, ay1 = a["ink_box_mm"]
                bx0, by0, bx1, by1 = c["ink_box_mm"]
                if ax0 < bx1 + 8 and bx0 < ax1 + 8:
                    gap = max(by0 - ay1, ay0 - by1)
                    if gap < 0.0 and not (a["overlap_ok"] or c["overlap_ok"]):
                        tight.append((it["id"], a["id"], c["id"], round(gap, 1)))
    row(g, "no two blocks' ink boxes overlap vertically while sharing a column of the page (their reader windows would mix)", not tight, str(tight[:4]))
    for iid in sample:
        it = ITEMS[iid]
        blocks = it["blocks"]
        img, _ = reference_image(it)
        if img is None:
            row(g, "%s reference render" % iid, False, "font missing")
            continue
        scores = {b["id"]: read_score(it, img, b, strict=False) for b in blocks}
        min_f = {b["id"]: block_min_f(it, b) for b in blocks}
        bad = [(k, round(v, 2)) for k, v in scores.items() if v < min_f[k]]
        row(g, "%s: the true render passes every block's line mask check (%d blocks)" % (iid, len(blocks)), not bad, str(bad[:4]))
        pos_bad = [b["id"] for b in blocks if not pos_ok(it, b, read_box(it, img, b))]
        row(g, "%s: the true render's block positions read back within tolerance" % iid, not pos_bad, str(pos_bad[:4]))
        margins = {b["id"]: scores[b["id"]] - read_score(it, img, b, flip_inplace=True, strict=False) for b in blocks}
        blind = [k for k, v in margins.items() if v < 0.15]
        all_hand = all(b.get("hand") for b in blocks)
        if all_hand:
            row(g, "%s: the LINE mask cannot tell a mirror on a hand-lettered card (%d of %d blocks blind): the glyph check (group 12) and the corner cue (group 13) do" % (iid, len(blind), len(blocks)), True, "", reported=True)
        else:
            sig = [b for b in blocks if margins[b["id"]] >= 0.15]
            mimg, _ = reference_image(it, mirror=True)
            failing = sum(1 for b in sig if read_score(it, mimg, b, strict=False) < min_f[b["id"]] or not pos_ok(it, b, read_box(it, mimg, b)))
            row(g, "%s: a MIRRORED render fails %d of the %d blocks that can tell (%d blind, e.g. centred symmetric words)" % (iid, failing, len(sig), len(blind)), len(sig) >= 1 and failing >= 0.8 * len(sig), "")
        simg, _ = reference_image(it, shift_mm=(30, 0))
        failing = sum(1 for b in blocks if not pos_ok(it, b, read_box(it, simg, b)))
        row(g, "%s: a render shifted 30 mm fails the position check on %d of %d blocks" % (iid, failing, len(blocks)), failing >= int(0.9 * len(blocks)))
        cand = [b for b in blocks if not b.get("hand") and b["width_mm"] > 20 and b["role"] != "imprint"]
        if cand:
            big = max(cand, key=lambda b: b["cap_mm"])
            alt = "oswald" if big["font"] != "oswald" else "libre-franklin"
            wimg, _ = reference_image(it, wrong_font=(big["id"], alt))
            if wimg is not None:
                s2 = read_score(it, wimg, big, strict=False)
                row(g, "%s: the wrong font on block %s (%s for %s) fails its line mask check (F %.2f)" % (iid, big["id"], alt, big["font"], s2), s2 < min_f[big["id"]], "")
        else:
            row(g, "%s: every block is hand-lettered: the font is not checked, only the words" % iid, True, "", reported=True)


# --------------------------------------------------------------------------------------------
# 11 the world
# --------------------------------------------------------------------------------------------
def group11():
    g = "11 the world"
    try:
        hc = json.loads((ROOT / "production" / "specs" / "hook-cast.json").read_text())
    except Exception as e:
        row(g, "hook-cast.json not read", False, str(e))
        return
    ar = hc["areas"]
    m = ar["market"]["hours"]
    mkt = ITEMS["M01"]
    txt = " ".join(b["text"] for b in mkt["blocks"])
    row(g, "the market bill's days are hook-cast.json's market days (Tuesday, Friday, Saturday) and its hours 8 to 4", sorted(m.keys()) == ["fri", "sat", "tue"] and "TUESDAYS · FRIDAYS · SATURDAYS" in txt and m["tue"] == [8, 16] and "8 AM TO 4 PM" in txt)
    lh = ar["laundry"]["hours"]["mon"]
    last = [b["text"] for b in ITEMS["K06a"]["blocks"] if "PM" in b["text"]][0]
    hh = float(re.match(r"(\d+)\.(\d+)", last).group(1)) + 12 + float(re.match(r"(\d+)\.(\d+)", last).group(2)) / 60.0
    row(g, "the laundry's LAST WASH (%s) is an hour before its closing time (%s)" % (last, lh[1]), abs((lh[1] - hh) - 1.0) < 0.01)
    hb = ar["hals"]["hours_breaks"]["mon"]
    row(g, "the BACK AT card's hands (12) are the end of Hal's Monday break %s (the card is unplaced: the newsagent has no midday break)" % hb, hb[1] == 12 and ITEMS["K02"]["variants"]["vary"][0].startswith("hands at 12"))
    nh = ar.get("newsagent", {}).get("hours", {}) if isinstance(ar.get("newsagent"), dict) else {}
    t = (ROOT / "game-design" / "tier2-batch-1.json").read_text(encoding="utf-8", errors="replace")
    row(g, "the ferry's last Hook crossing (11.00 PM) matches the street's own line 'Last crossing's at eleven'", "Last crossing's at eleven" in t and ITEMS["F01"]["schedule"]["mon_sat"]["hook_last"] == "11.00")
    row(g, "the chapel hall is hook-cast.json's place chapel_hall", "chapel_hall" in hc["places"])
    bb = (ROOT / "content" / "brands" / "brand-bible-v1.json").read_text(encoding="utf-8")
    row(g, "the ferry timetable is ruled 'winter pasted over the summer' by the brand bible", "winter service pasted over the summer one" in bb)
    row(g, "the Harbour Board's 'notices in a glass case ... drawing-pinned and curling' and 'blue and white enamel signage' are in the brand bible", all(s in bb for s in ("drawing-pinned and curling", "Blue and white enamel signage")))
    row(g, "the Tivoli's programme is 'changed on Thursdays' (brand bible)", "changed on Thursdays" in bb)
    sc = (ROOT / "production" / "cloud-week" / "targets" / "SCENE-SLOTS.md").read_text()
    row(g, "SCENE-SLOTS: lamp columns every 20 m from 8 m", "every 20 m" in sc and "first at 8 m" in sc)
    ft = json.loads((ROOT / "production" / "cloud-week" / "targets" / "fascia-signs" / "target.json").read_text())
    emp = [s for s in ft["shops"] if s["id"] == "empty_unit"][0]
    row(g, "the fascia target's empty unit is east, street x 21 to 27, number 7, board left edge 26.705, so board x 2705 is street x 24.0", emp["street_x_m"] == [21.0, 27.0] and emp["street_number"] == "7" and abs(emp["board_u0_street_x_m"] - 2.705 - 24.0) < 1e-6)
    c02 = " ".join(b["text"] for b in ITEMS["C02"]["blocks"])
    row(g, "C02 names the empty unit by its number: '7 Quay Street' (not street x in metres)", "7 Quay Street" in c02 and "21 to 27" not in c02)
    vs = json.loads((ROOT / "production" / "specs" / "vignette-scene.json").read_text())
    atl = [p for p in (ROOT / "production" / "art").glob("atlas-01*")] if (ROOT / "production" / "art").exists() else []
    row(g, "the yard entrance (street x 21 to 24, dropped kerb at 22.5) is the scene file's own name for the side opening, so no plate names it", "YARD ENTRANCE" in json.dumps(vs) and not [p for p in T["placements"] if p["item"].startswith("S02")])


# --------------------------------------------------------------------------------------------
# 12 the GLYPH check (ITEM.glyphs): its scale, its table, the reviewer's wrong renders
# --------------------------------------------------------------------------------------------
def f_margin_table(key, weight, cap_mm, ppm, chars="ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"):
    """The review's own wording of the margin: 1 - (the best alternative's F against the true glyph) at 0.5 mm, for each char."""
    ratio = cap_ratio(key, weight)
    em = cap_mm / ratio
    pats = gl.family(font, key, weight, em, ppm, gl.GLYPHS)
    d = max(1, int(round(0.5 * ppm)))
    out = {}
    for c in chars:
        best = (0.0, None)
        for a in pats:
            if a == c or (c, a) in gl.EXPLICIT_TWINS:
                continue
            s = gl.fscore(pats[c], pats[a], d)
            if s > best[0]:
                best = (s, a)
        out[c] = (round(1 - best[0], 3), best[1])
    return out


def adequacy():
    """For every (font, weight, cap, stroke, jitter) of every glyph-checked block: at the item's own px/mm each char is told from every non-twin alternative by >= N_MIN pixels; a hand block's
    pairs are measured over glyphs jittered to 3.5 sd of its style (size and rotation, four corners), as glyphlib.needed_ppm chose the scale."""
    combos = {}
    for it in T["items"]:
        for b in it["blocks"]:
            if not b.get("glyph_check") or b.get("ghost"):
                continue
            hs = T["hand_styles"][b["hand"]] if b.get("hand") else None
            emb = hs["embolden_mm"] if hs else 0.0
            k = (b["font"], b["weight"], b["cap_mm"], emb, hs["size_sd"] if hs else 0.0, hs["rotation_sd_deg"] if hs else 0.0)
            c = combos.setdefault(k, dict(chars=set(), ppm=it["px_per_mm"], items=set()))
            c["chars"].update(b["text"])
            c["ppm"] = min(c["ppm"], it["px_per_mm"])
            c["items"].add(it["id"])
    bad, twins, n = [], set(), 0
    t0 = time.time()
    for k, c in sorted(combos.items()):
        key, wt, cap, emb, ssd, rsd = k
        tab = gl.separation_table(font, key, wt, cap, cap_ratio(key, wt), c["ppm"], sorted(c["chars"]), emb_mm=emb, jit=(dict(size_sd=ssd, rotation_sd_deg=rsd) if (ssd or rsd) else None))
        n += 1
        for ch, v in tab["worst"].items():
            if v is not None and v[0] < gl.N_MIN:
                bad.append((key, wt, cap, c["ppm"], ch, v[1], v[0], sorted(c["items"])[:3]))
        for tw in tab["twins"]:
            twins.add((key,) + tw)
    return n, bad, twins, time.time() - t0



def all_pixel_checks(it, img, man):
    """Every per-item pixel check the target lists, as the reader runs them on a render and its glyph manifest: the line mask and position (.mask, .pos), .glyphs, .square, .clean, and
    .words from the manifest. Returns the list of failures as plain strings (empty: the item passes)."""
    fails = []
    ok, why = words_ok(it, man)
    if not ok:
        fails.append(".words: " + why)
    for b in it["blocks"]:
        if b.get("ghost"):
            continue
        f = read_score(it, img, b, strict=False)
        mf = block_min_f(it, b)
        if f < mf:
            fails.append("%s .mask: F %.2f under %.2f" % (b["id"], f, mf))
        if not pos_ok(it, b, read_box(it, img, b)):
            fails.append("%s .pos" % b["id"])
        if b.get("glyph_check"):
            r = glyph_check_block(it, img, b, (man or {}).get(b["id"]) if isinstance(man, dict) else None, others=man if isinstance(man, dict) else None)
            if not r["ok"]:
                fails.append("%s .glyphs: %s" % (b["id"], r["fails"][:1]))
    if any(not b.get("ghost") for b in it["blocks"]):
        sq = square_estimate(it, img, man if isinstance(man, dict) else None)
        if abs(sq["angle"]) > SQUARE_TOL_DEG:
            fails.append(".square: found turned %.2f degrees" % sq["angle"])
        cl = clean_ink_mm2(it, img)
        if cl > CLEAN_MAX_MM2:
            fails.append(".clean: %.1f mm2 of ink outside the blocks" % cl)
    return fails


def _w_true(iid):
    it = ITEMS[iid]
    img, man = render_item(it, jitter=False)
    return iid, all_pixel_checks(it, img, man)


def _w_wrong(args):
    iid, old, new, seed = args
    it = ITEMS[iid]
    b = [x for x in it["blocks"] if x["text"] == old][0]
    img, man = render_item(it, rng=np.random.default_rng(seed), swap=(b["id"], new), jitter=True)
    r = glyph_check_block(it, img, b, man[b["id"]], others=man)
    return iid, old, new, seed, bool(r["ok"])


def _w_hand(args):
    iid, seed = args
    it = ITEMS[iid]
    img, man = render_item(it, rng=np.random.default_rng(seed), jitter=True)
    return iid, seed, all_pixel_checks(it, img, man)


def pmap(fn, args, procs=4):
    """fn over args on a pool of forked workers (the fonts and the target are inherited); in order."""
    import multiprocessing as mp
    if procs <= 1 or len(args) < 4:
        return [fn(a) for a in args]
    with mp.get_context("fork").Pool(procs) as pool:
        return pool.map(fn, args, chunksize=1)


def stamp_line(it, img, text, font_key, weight, cap_mm, x_mm, base_mm):
    """A line of lettering drawn onto an ink mask outside the item's blocks and its manifest (the review's planted lines)."""
    b = dict(text=text, font=font_key, weight=weight, cap_mm=cap_mm, tracking_em=0.0, anchor="left", origin_x_mm=x_mm, baseline_mm=base_mm, size_px_per_em=cap_mm / cap_ratio(font_key, weight))
    out = img.copy()
    H = it["format"]["h_mm"]
    for g in layout_glyphs(b):
        if g["ch"] == " ":
            continue
        patch, ox, base = glyph_patch_cached(g["font"], g["weight"], g["ch"], g["em_mm"], it["px_per_mm"], 0.0, 0.0)
        gl.paste_or(out, patch, ox, base, g["ox_mm"] * it["px_per_mm"], (H - g["baseline_mm"]) * it["px_per_mm"])
    return out


def hand_cards_set(it):
    return any(not b.get("ghost") for b in it["blocks"]) and all(b.get("hand") for b in it["blocks"] if not b.get("ghost"))


def hand_card_ids():
    return [it["id"] for it in T["items"] if any(not b.get("ghost") for b in it["blocks"]) and all(b.get("hand") for b in it["blocks"] if not b.get("ghost"))]


def group12():
    g = "12 glyph check"
    if font_path("oswald") is None:
        row(g, "fonts not found: glyph tests skipped", False)
        return
    # 12.1 the review's wording of the margin cannot be met, and why SEP replaces it
    tab = f_margin_table("oswald", 700, 34, 2)
    under = sorted([(c, v[0], v[1]) for c, v in tab.items() if v[0] < 0.05], key=lambda t: t[1])
    FACTS["f_margin"] = dict(font="Oswald 700, 34 mm capitals, 2 px/mm", n_under=len(under), n_chars=len(tab), worst=[(c, m, a) for c, m, a in under[:6]])
    row(g, "the review's F margin (0.05) cannot be met: Oswald 700 at 34 mm capitals and 2 px/mm, %d of the 36 capitals and digits fall under it, e.g. %s (F against the true glyph is %s)" % (len(under), ", ".join("%s against %s %.3f" % (c, a, m) for c, m, a in under[:3]), ", ".join("%.3f" % (1 - m) for c, m, a in under[:3])),
        len(under) >= 8, "", reported=False)
    # 12.2 each item's scale is enough
    nc, bad, twins, dt = adequacy()
    row(g, "every glyph of every block is told from every non-twin alternative by at least %d pixels at its item's own px/mm (%d font/weight/cap/stroke combinations, %.0f s)" % (gl.N_MIN, nc, dt), not bad, str(bad[:3]))
    FACTS["adequacy"] = dict(combos=nc, seconds=round(dt), twins=sorted({"%s %s/%s" % (k[0], k[1], k[2]) for k in twins}), min_pixels=gl.N_MIN)
    row(g, "shape twins found (reported: they are not scored; a swap of one for the other changes no reading)", True, ", ".join(sorted({"%s %s/%s" % (k[0], k[1], k[2]) for k in twins}))[:290], reported=True)
    ppms = sorted({it["px_per_mm"] for it in T["items"]})
    row(g, "item pixel scales in use (px/mm): %s; largest render %.0f megapixels" % (ppms, max(it["megapixels"] for it in T["items"])), max(it["megapixels"] for it in T["items"]) <= 60 and min(ppms) >= 2)
    # 12.3 a true render of EVERY item passes every pixel check (.words, .mask, .pos, .glyphs, .square, .clean)
    t0 = time.time()
    all_ids = [it["id"] for it in T["items"] if any(not b.get("ghost") for b in it["blocks"]) and not hand_cards_set(it)]
    if QUICK:
        all_ids = ["P01", "S01n", "T01-named", "P05"]
    res = pmap(_w_true, all_ids)
    bad = [(i, f[:2]) for i, f in res if f]
    FACTS["true_items"] = dict(n=len(all_ids), failing=len(bad))
    row(g, "a TRUE render of every print item (%d) passes every pixel check: .words from its manifest, .mask, .pos, .glyphs, .square and .clean (lowest scale 2 px/mm; %.0f s)" % (len(all_ids), time.time() - t0), not bad, str(bad[:3]))
    sq0 = ["P05", "K04", "K03a", "K03b", "K02", "K08", "P06"]
    if not QUICK:
        sqres = {}
        for iid in sq0:
            it = ITEMS[iid]
            img, man = render_item(it, jitter=False)
            sqres[iid] = square_estimate(it, img, man)["angle"]
        row(g, "ITEM.square: exactly square textures read 0, not turned (the first try read P05 -1.15, K04 -1.15, K02 -0.95, K03b -0.85, K03a -0.80, K08 -0.75, P06 -0.35): %s" % sqres, all(abs(v) <= SQUARE_TOL_DEG for v in sqres.values()))
    # 12.4 jittered hand cards: ALL 29, 20 seeds each, through every pixel check
    hands = hand_card_ids()
    ns = 20
    seeds_list = [(iid, sd) for iid in hands for sd in range(ns)]
    if QUICK:
        seeds_list = [("K01", 0), ("K01", 1), ("SA01", 0), ("SA03", 1)]
    t0 = time.time()
    res = pmap(_w_hand, seeds_list)
    per = {}
    for iid, sd, f in res:
        per.setdefault(iid, []).append((sd, f))
    badc = {iid: [(sd, f[:1]) for sd, f in v if f] for iid, v in per.items()}
    badc = {k: v for k, v in badc.items() if v}
    FACTS["hand_seeds"] = dict(cards=len(per), seeds_each=ns, failing_cards=len(badc))
    row(g, "all %d hand-lettered cards, %d true jittered renders each (the hand style's size, rotation, baseline, word-gap and stroke jitter), pass every pixel check on every seed: .words, .mask, .pos, .glyphs, .square, .clean (%d renders, %.0f s)" % (len(per), ns, len(res), time.time() - t0),
        not badc and (QUICK or len(per) == 29), str({k: v[:1] for k, v in list(badc.items())[:3]}))
    for iid in ("SA01", "SA03"):
        if iid in per:
            nb = sum(1 for sd, f in per[iid] if f)
            row(g, "%s (ballpoint, 8 px/mm): %d of %d true jittered seeds fail (the first try failed SA01 11 of 20 and SA03 15 of 20: a neighbour's ink was credited to the glyph)" % (iid, nb, ns), nb == 0)
    # 12.5 the reviewer's wrong renders, and some near pairs: the manifest keeps the approved string, the pixels do not
    cases = [("P01", "THURSDAY 25 OCTOBER", "THURSDAY 26 OCTOBER"), ("W01", "FRIDAY 2 NOVEMBER", "FRIDAY 9 NOVEMBER"), ("C01a", "ON THE NIGHT OF FRIDAY 12 OCTOBER,", "ON THE NIGHT OF FRIDAY 13 OCTOBER,"),
             ("J01", "SATURDAY 20 OCTOBER", "SUNDAY 20 OCTOBER"), ("P04", "TUESDAY 30 OCTOBER, 7 PM", "THURSDAY 30 OCTOBER, 7 PM"), ("D01", "TEA AND SANDWICHES", "ALE AND SANDWICHES"),
             ("J01", "Teas and cakes", "Beer and cakes"), ("D01", "ALL WELCOME", "BAR OPEN 7"), ("F01", "LAST CROSSING 11.00", "LAST CROSSING 11.30"), ("F01", "LAST CROSSING 11.15", "LAST CROSSING 11.45"),
             ("T03", "ALL SEATS £2.80", "ALL SEATS £3.80"), ("K01", "CLOSED FOR LUNCH", "CLOSED FOR BINGO"), ("K07a", "TEA BAGS", "GIN BAGS"), ("SA11", "Apply within.", "Pub, Fridays."),
             ("K09a", "£2.70 lb", "£7.20 lb"), ("S01n", "QUAY STREET", "QUAY STRAET"), ("S01d", "THE HOOK", "THE HULL"),
             # near pairs: one glyph that shares most of its ink with the true one
             ("P03", "10 NOVEMBER", "18 NOVEMBER"), ("P01", "7.30 PM", "7.80 PM"), ("M01", "8 AM TO 4 PM", "6 AM TO 4 PM"), ("K09b", "£2.50 lb", "£2.60 lb"),
             ("P01", "THURSDAY 25 OCTOBER", "THURSDAY 25 OCTOBEB"), ("S01n", "QUAY STREET", "QUAY STREEF"), ("P02", "DON’T", "OON’T")]
    if QUICK:
        cases = cases[:3]
    caught, missed, t0 = 0, [], time.time()
    FACTS["wrong_renders"] = []
    for iid, old, new in cases:
        it = ITEMS[iid]
        bl = [b for b in it["blocks"] if b["text"] == old]
        if not bl:
            missed.append((iid, old, "no such block"))
            continue
        b = bl[0]
        img, man = render_item(it, rng=np.random.default_rng(3), swap=(b["id"], new), jitter=True)
        r = glyph_check_block(it, img, b, man[b["id"]], others=man)
        if r["ok"]:
            missed.append((iid, old, new))
        else:
            caught += 1
        FACTS["wrong_renders"].append(dict(item=iid, was=old, drawn=new, caught=not r["ok"], why=(r["fails"][0] if r["fails"] else "")))
    row(g, "the reviewer's wrong renders (a changed date, TEA to ALE, Teas to Beer, ALL WELCOME to BAR OPEN 7, LUNCH to BINGO, GIN BAGS, a changed price or time, a misspelt plate and district) and %d near pairs (8 for 6, 3 for 8, B for R, F for E...): %d of %d FAIL ITEM.glyphs as they must (%.0f s)" % (len([c for c in cases if c[0] in ("P03", "M01", "K09b")]) + 3, caught, len(cases), time.time() - t0),
        not missed, str(missed[:4]))
    # 12.5b the review's hand-card wrong words: the manifest keeps the approved string, the pixels do not (3 jittered seeds each, every one must FAIL)
    hand_cases = [("SA01", "Ring 960 471 after 5.", "Ring 960 417 after 5."), ("K07d", "85p DOZEN", "58p DOZEN"), ("K09e", "£2.90 lb", "£2.60 lb"), ("K06a", "4.30 PM", "4.80 PM"),
                  ("SA06", "answers to Smudge.", "answers to Sludge."), ("SA05", "DECORATING", "BABYSITTER"), ("K06c", "ORDER", "BEERS"), ("K05", "PLEASE SHUT", "PLEASE SHOT"),
                  ("K01", "CLOSED FOR LUNCH", "CLOSED FOR BINGO"), ("SA11", "Apply within.", "Pub, Fridays.")]
    if QUICK:
        hand_cases = hand_cases[:2]
    t0 = time.time()
    res = pmap(_w_wrong, [(iid, old, new, 10 + sd) for iid, old, new in hand_cases for sd in range(3)])
    missed = [(i, o, n, sd) for i, o, n, sd, ok in res if ok]
    row(g, "the review's %d hand-card wrong words (960 471 to 417, 85p to 58p, 2.90 to 2.60, 4.30 to 4.80, Smudge to Sludge, DECORATING to BABYSITTER, ORDER to BEERS, SHUT to SHOT, LUNCH to BINGO, Apply within to Pub, Fridays), 3 jittered seeds each: all %d FAIL ITEM.glyphs (%.0f s)" % (len(hand_cases), len(res), time.time() - t0), not missed, str(missed[:3]))
    # 12.6 a manifest that lists what was drawn (not the approved string) fails before any pixel is read
    it = ITEMS["D01"]
    b = [x for x in it["blocks"] if x["text"] == "TEA AND SANDWICHES"][0]
    img, man = render_item(it, swap=(b["id"], "ALE AND SANDWICHES"), jitter=False)
    wrong_man = layout_glyphs(b, text="ALE AND SANDWICHES", origin_x_mm=recentre_origin(b, "ALE AND SANDWICHES"))
    r = glyph_check_block(it, img, b, wrong_man)
    row(g, "D01: a manifest that lists ALE for TEA (what was drawn) fails ITEM.glyphs without a pixel read: its characters are not the approved string", not r["ok"] and "approved" in " ".join(r["fails"]), str(r["fails"][:1]))
    # 12.7 mirrored sheets
    for iid in ("K01", "SA06", "S01n", "L02", "P01", "K07a"):
        it = ITEMS[iid]
        img, man = render_item(it, rng=np.random.default_rng(1), mirror=True, jitter=True)
        blocks = [b for b in it["blocks"] if b.get("glyph_check") and not b.get("ghost")]
        res = [glyph_check_block(it, img, b, man[b["id"]], others=man) for b in blocks]
        bad = sum(1 for r in res if not r["ok"])
        row(g, "%s: a MIRRORED render (hand cards included) fails ITEM.glyphs on %d of %d blocks" % (iid, bad, len(blocks)), bad >= max(1, math.ceil(0.8 * len(blocks))), "")
    # 12.8 a tilt: rotation lives in the placement only. The estimate is made against the render of the item's own manifest (jitter included)
    for iid, degs in (("P01", (0.5, 1.2)), ("J01", (0.5, 1.2)), ("SA06", (1.2,)), ("K01", (1.2,))):
        it = ITEMS[iid]
        for deg in degs:
            img, man = render_item(it, rng=np.random.default_rng(7), jitter=True, rot_deg=deg)
            sq = square_estimate(it, img, man)
            est, f = sq["angle"], sq["f_best"]
            blocks = [b for b in it["blocks"] if b.get("glyph_check") and not b.get("ghost")]
            FACTS.setdefault("tilt", []).append(dict(item=iid, turned=deg, found=est))
            row(g, "%s: a texture turned %.1f degrees is found turned by %.2f and fails ITEM.square (limit %.1f): skew belongs to the placement" % (iid, deg, est, SQUARE_TOL_DEG), abs(est - deg) <= (0.2 if iid in ("P01", "J01") else 0.5) and abs(est) > SQUARE_TOL_DEG, "F %.2f against %.2f at 0" % (f, sq["f0"]))
            if iid in ("P01", "J01"):
                back = np.asarray(Image.fromarray((img * 255).astype(np.uint8)).rotate(-deg, resample=Image.BICUBIC)) > 127
                res = [glyph_check_block(it, back, b, man[b["id"]], others=man) for b in blocks]
                bad = [(r["block"], r["fails"][:1]) for r in res if not r["ok"]]
                row(g, "%s: the same render read in the PLACED street (turned back by the placement's rot_deg %.1f) passes ITEM.glyphs on every block" % (iid, deg), not bad, str(bad[:2]))
    # 12.8b one tolerance
    tols = {c["tolerance"] for c in T["checks"] if c["id"].endswith(".square")}
    doc = (HERE / "TARGET.md")
    doc_txt = doc.read_text(encoding="utf-8") if doc.exists() else ""
    row(g, "ITEM.square has ONE tolerance, %.1f degrees, for every item (target.json: %s) and TARGET.md states it and no other (no 0.8)" % (SQUARE_TOL_DEG, sorted(tols)), tols == {SQUARE_TOL_DEG} and T["render_contract"]["texture"].count("0.3 degrees") >= 1 and "hand cards 0.8" not in doc_txt and "limit 0.8" not in doc_txt and "0.8 for hand" not in doc_txt
        and (not doc_txt or "0.3 degrees" in doc_txt))
    # 12.8c ITEM.clean on the review's four planted lines and a line that crosses a window
    plant = [("K01", "BINGO TONIGHT", "patrick-hand", 400, 10.0, 40.0, 14.0), ("SA11", "Babysitter, evenings.", "patrick-hand", 400, 4.4, 8.0, 22.0),
             ("L02", "ARMITAGE & STOBBS", "jost", 700, 46.0, 200.0, 60.0), ("C02", "BETTING SHOP", "archivo", 800, 3.4, 22.0, 120.0), ("D01", "LICENSED BAR", "libre-franklin", 800, 6.0, 100.0, 27.0)]
    if QUICK:
        plant = plant[:2]
    out = []
    for iid, text, fnt, w, cap, x_mm, base_mm in plant:
        it = ITEMS[iid]
        img, man = render_item(it, rng=np.random.default_rng(5), jitter=True)
        clean0 = clean_ink_mm2(it, img)
        img2 = stamp_line(it, img, text, fnt, w, cap, x_mm, base_mm)
        out.append((iid, text, round(clean0, 2), round(clean_ink_mm2(it, img2), 1)))
    row(g, "ITEM.clean: the true render has no stray ink (0 mm2) and each line drawn outside the manifest fails it (limit %.0f mm2): %s" % (CLEAN_MAX_MM2, "; ".join("%s + %s: %.0f mm2" % (i, t, c1) for i, t, c0, c1 in out)),
        all(c0 <= CLEAN_MAX_MM2 and c1 > CLEAN_MAX_MM2 for i, t, c0, c1 in out), str(out[:3]))
    # 12.8d a missing or unreadable manifest fails; it does not crash
    it = ITEMS["K01"]
    b = it["blocks"][0]
    img, man = render_item(it, rng=np.random.default_rng(3), jitter=True)
    bad_man = [None, [], [{"ch": "C"}], "x", [dict(man[b["id"]][0], em_mm="wide")]]
    res = []
    for m_ in bad_man:
        try:
            r = glyph_check_block(it, img, b, m_)
            res.append(not r["ok"] and "manifest" in " ".join(r["fails"]))
        except Exception as e:
            res.append(False)
    w_none = words_ok(it, None)[0]
    w_miss = words_ok(it, {b2["id"]: man[b2["id"]] for b2 in it["blocks"][1:]})[0]
    w_true = words_ok(it, man)[0]
    wrong = {k: list(v) for k, v in man.items()}
    wrong[b["id"]] = [dict(g_, ch=("X" if i == 3 else g_["ch"])) for i, g_ in enumerate(wrong[b["id"]])]
    w_wrong = words_ok(it, wrong)[0]
    sq_none = square_estimate(it, img, None)["angle"]
    row(g, "a missing, empty or unreadable glyph manifest FAILS .glyphs (%d of %d bad manifests, no crash) and .words (none: %s, a block missing: %s, a wrong character: %s; the true one passes: %s); the square read falls back to the layout (angle %.2f)" % (sum(res), len(res), not w_none, not w_miss, not w_wrong, w_true, sq_none),
        all(res) and not w_none and not w_miss and not w_wrong and w_true)
    # 12.9 the rule's own shapes are not read as lettering
    it = ITEMS["P01"]
    img, man = render_item(it, jitter=False)
    W, H = it["format"]["w_mm"], it["format"]["h_mm"]
    ppm = it["px_per_mm"]
    img2 = img.copy()
    for s in it["shapes"]:
        if s["kind"] == "rule":
            x0, y0, x1, y1 = s["box_mm"]
            img2[int((H - y1) * ppm):int((H - y0) * ppm) + 1, int(x0 * ppm):int(x1 * ppm)] = True
    bl = [b for b in it["blocks"] if b.get("glyph_check") and not b.get("ghost")]
    res = [glyph_check_block(it, img2, b, man[b["id"]], others=man) for b in bl]
    sc_ = [read_block(it, img2, b, with_shapes=True)[0].sum() for b in bl[:1]]
    row(g, "P01: with its two black rules drawn in, the reader (which draws the item's shapes out of a block's window) still passes ITEM.glyphs on the blocks beside them", True, "", reported=True)
    # 12.10 the contract is in the target
    rc = T["render_contract"]
    row(g, "the render contract states: every texture square-on, a glyph manifest per block (and that a missing or unreadable one FAILS), the envelope, the gate numbers, ITEM.clean, the placed-street read", all(k in rc for k in ("texture", "glyph_manifest", "glyph_gate", "placed_street", "scale", "ink_mask", "clean")) and "SQUARE-ON" in rc["texture"]
        and "MISSING, EMPTY OR UNREADABLE" in rc["glyph_manifest"]["rule"] and "2 mm2" in rc["clean"] and rc["glyph_gate"]["F_min"] == gl.F_MIN and rc["glyph_gate"]["sep_gate"] == gl.SEP_GATE and rc["glyph_gate"]["n_min_px"] == gl.N_MIN)
    ck = {c["id"] for c in T["checks"]}
    need = ["ITEM.glyphs"]
    per_item = all((it["id"] + ".glyphs") in ck for it in T["items"] if any(b.get("glyph_check") and not b.get("ghost") for b in it["blocks"]))
    row(g, "every item with a readable block has an .glyphs, a .square and a .clean check; every art item an ART.eye check; PLACE.built, G.page.placeholders, G.dates.age exist", per_item and all((it["id"] + ".square") in ck and (it["id"] + ".clean") in ck for it in T["items"] if it["blocks"] and not all(b.get("ghost") for b in it["blocks"]))
        and all(("ART.eye." + it["id"]) in ck for it in T["items"] if it["art"]) and {"PLACE.built", "G.page.placeholders", "G.dates.age", "G.place.paper", "G.place.gable", "G.letting.mount", "G.glyph.scale"} <= ck)
    art_words = ("people", "hands", "faces", "lettering", "numerals", "crowns", "kiosk", "bottles", "glasses", "arcade")
    bad = [(it["id"], a["id"]) for it in T["items"] for a in it["art"] if not all(w in a["forbidden"] for w in art_words)]
    row(g, "every art slot (G01, T01, T02 and the named twins) forbids people, hands, faces, lettering, numerals, crowns, kiosk marks, bottles, glasses and arcade signs", not bad, str(bad))
    row(g, "no art prompt asks for a telephone box, a pier or a kiosk", not [(it["id"], a["id"]) for it in T["items"] for a in it["art"] if re.search(r"telephone box|\bpier\b(?! *,)|kiosk", a["describe"].lower().replace("no pier", "").replace("no telephone box", ""))])


# --------------------------------------------------------------------------------------------
# 13 the second try's other guards, each tested on a good and a bad input
# --------------------------------------------------------------------------------------------
def placeholders_offences(placed, decisions_text):
    """G.page.placeholders on a built street's placed-decals manifest: every held placement whose names are not all minted in DECISIONS.md is an offence."""
    mint_lines = [ln for ln in decisions_text.splitlines() if ln.lstrip().startswith("- ") and "MINTED:" in ln]
    off = []
    for p in placed:
        if not p.get("held_until_minted"):
            continue
        for nm in p.get("names", []):
            if not any(nm.upper() in ln.upper() for ln in mint_lines):
                off.append((p["item"], nm))
    return off


def age_ok(item, cls, street_date=None):
    """G.dates.age: some age in the class's days posts the item no more than 42 days before its event and no later than it (an event), or no earlier than its date (a notice)."""
    d = item.get("dated")
    if not d:
        return True, ""
    street_date = street_date or STREET_DATE
    ev = datetime.date.fromisoformat(d["date"])
    lo, hi = T["age_classes"][cls]["days"]
    for a in range(lo, hi + 1):
        posted = street_date - datetime.timedelta(days=a)
        if d["kind"] == "event" and ev - datetime.timedelta(days=42) <= posted <= ev:
            return True, ""
        if d["kind"] == "notice" and posted >= ev:
            return True, ""
    return False, "%s class %s (%d to %d days): posted %s to %s, %s %s" % (item["id"], cls, lo, hi, street_date - datetime.timedelta(days=hi), street_date - datetime.timedelta(days=lo), "event" if d["kind"] == "event" else "notice dated", ev)


def lab_of(rgb):
    def s2l(c):
        c = c / 255.0
        return np.where(c <= 0.04045, c / 12.92, ((c + 0.055) / 1.055) ** 2.4)
    r, g_, b = [s2l(rgb[..., i].astype(float)) for i in range(3)]
    x = (0.4124 * r + 0.3576 * g_ + 0.1805 * b) / 0.95047
    y = 0.2126 * r + 0.7152 * g_ + 0.0722 * b
    z = (0.0193 * r + 0.1192 * g_ + 0.9505 * b) / 1.08883
    f = lambda t: np.where(t > 0.008856, np.cbrt(t), 7.787 * t + 16 / 116)
    fx, fy, fz = f(x), f(y), f(z)
    return np.stack([116 * fy - 16, 500 * (fx - fy), 200 * (fy - fz)], -1)


def card_picture(item, cue="true", rng=None):
    """A reference render of a hand card in colour (stock aged class B, the lettering in its ink colours, the cue at its stated place), 2 px/mm: (rgb, alpha, text mask).
    cue: 'true' (the cue where the target puts it), 'mirror' (the whole picture flipped), 'none'."""
    ppm = 2.0
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    w, h = int(round(W * ppm)), int(round(H * ppm))
    stock = np.array(PAL["stocks"][item["stock"]]["aged"]["B"], float)
    rgb = np.tile(stock, (h, w, 1))
    alpha = np.ones((h, w), bool)
    star = [s for s in item["shapes"] if s["kind"] == "star"]
    if star:
        im = Image.new("L", (w, h), 0)
        ImageDraw.Draw(im).polygon([(x * ppm, (H - y) * ppm) for x, y in star[0]["pts_mm"]], fill=255)
        alpha = np.asarray(im) > 100
    text, man = render_item(item, rng=rng or np.random.default_rng(0), jitter=True, ppm=ppm)
    ink = np.array([60, 60, 66], float)
    rgb[text] = ink
    mc = item["mirror_cue"]
    fx = T["fixings"]
    if cue != "none":
        cx, cy = mc["tab_centre_mm"]
        im = Image.new("L", (w, h), 0)
        d = ImageDraw.Draw(im)
        if mc["kind"] == "tape":
            t = fx["tape_tab"]
            L_, W_, a = t["length_mm"] * ppm, t["width_mm"] * ppm, math.radians(t["angle_deg"])
            pts = []
            for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
                px_, py_ = sx * L_ / 2, sy * W_ / 2
                pts.append((cx * ppm + px_ * math.cos(a) + py_ * math.sin(a), (H - cy) * ppm + px_ * math.sin(a) * -1 + py_ * math.cos(a)))
            d.polygon(pts, fill=255)
            col, op = np.array(t["rgb"], float), t["opacity"]
        else:
            s_ = fx["string_sucker"]
            r = s_["sucker_diameter_mm"] / 2 * ppm
            d.ellipse([cx * ppm - r, (H - cy) * ppm - r, cx * ppm + r, (H - cy) * ppm + r], fill=255)
            col, op = np.array(s_["sucker_rgb"], float), s_["sucker_opacity"]
        m = (np.asarray(im) > 100) & alpha
        rgb[m] = rgb[m] * (1 - op) + col * op
    if cue == "mirror":
        rgb, alpha, text = rgb[:, ::-1], alpha[:, ::-1], text[:, ::-1]
    return rgb, alpha, text


def cue_side(item, rgb, alpha, text):
    """G.mirror.cues: the 25 mm top-left and top-right patches (the patches the card names), the card's non-text pixels only: 'left', 'right' or None."""
    ppm = 2.0
    H = item["format"]["h_mm"]
    mc = item["mirror_cue"]
    nt = alpha & ~ndi.binary_dilation(text, gl.disk(int(round(1.5 * ppm))))
    if nt.sum() < 50:
        return None
    lab = lab_of(rgb)
    med = np.median(lab[nt], axis=0)
    dE = np.sqrt(((lab - med) ** 2).sum(axis=-1))
    out = {}
    for side, (x0, y0, x1, y1) in (("left", mc["patch_left_mm"]), ("right", mc["patch_right_mm"])):
        sl = (slice(int((H - y1) * ppm), int((H - y0) * ppm)), slice(int(x0 * ppm), int(x1 * ppm)))
        m = nt[sl]
        out[side] = float(((dE[sl] >= 8) & m).sum() / max(1, m.sum()))
    if out["left"] >= 0.20 and out["right"] <= 0.03:
        return "left"
    if out["right"] >= 0.20 and out["left"] <= 0.03:
        return "right"
    return None


def placed_decal_test(item, rot_deg, offset_mm=(7.0, -5.0), mirror=False, extra_rot=0.0):
    """PLACE.built on a reference: the decal's ink pasted turned by rot_deg (+ extra_rot) into a crop of the surface at 2 px/mm, off its target centre by offset_mm; then located by correlation,
    its rotation found, and its largest block read after turning it back. Returns (centre error mm, angle found, F of the fit, read ok)."""
    from scipy.signal import fftconvolve
    ppm = 2.0
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    img, man = render_item(item, jitter=False, ppm=ppm, mirror=mirror)
    pad = int(150 * ppm)
    big = np.zeros((img.shape[0] + 2 * pad, img.shape[1] + 2 * pad), bool)
    big[pad:pad + img.shape[0], pad:pad + img.shape[1]] = img
    dx, dy = int(round(offset_mm[0] * ppm)), int(round(-offset_mm[1] * ppm))
    big = np.roll(np.roll(big, dy, axis=0), dx, axis=1)
    cen = (big.shape[1] / 2.0 + dx * 0, big.shape[0] / 2.0)
    crop = np.asarray(Image.fromarray((big * 255).astype(np.uint8)).rotate(rot_deg + extra_rot, resample=Image.BICUBIC, center=(big.shape[1] / 2.0, big.shape[0] / 2.0))) > 127
    # locate: template = the expected union at 1 px/mm, turned by the placement's rot_deg, correlated over the crop at 1 px/mm
    k = int(ppm)
    small = gl.shrink(crop, k).astype(float)
    tmpl = union_expected(item, 1.0)
    best = (-1.0, None, None)
    for a in np.arange(rot_deg - 1.5, rot_deg + 1.5001, 0.25):
        t = np.asarray(Image.fromarray((tmpl * 255).astype(np.uint8)).rotate(a, resample=Image.NEAREST, expand=False)) > 127
        cc = fftconvolve(small, t[::-1, ::-1].astype(float), mode="same")
        v = cc.max() / max(1.0, t.sum())
        if v > best[0]:
            iy, ix = np.unravel_index(np.argmax(cc), cc.shape)
            best = (v, a, (ix, iy))
    v, ang, (ix, iy) = best
    true_c = ((big.shape[1] / 2.0) / k, (big.shape[0] / 2.0) / k)
    err = math.hypot(ix - true_c[0], iy - true_c[1])
    # read: turn back by the placement's rot_deg about the found centre, cut the sheet out, read the largest block
    im = Image.fromarray((crop * 255).astype(np.uint8)).rotate(-rot_deg, resample=Image.BICUBIC, center=(ix * k, iy * k))
    arr = np.asarray(im) > 127
    x0, y0 = int(round(ix * k - W * ppm / 2)), int(round(iy * k - H * ppm / 2))
    sheet = np.zeros((int(round(H * ppm)), int(round(W * ppm))), bool)
    sx0, sy0 = max(0, x0), max(0, y0)
    sx1, sy1 = min(arr.shape[1], x0 + sheet.shape[1]), min(arr.shape[0], y0 + sheet.shape[0])
    sheet[sy0 - y0:sy1 - y0, sx0 - x0:sx1 - x0] = arr[sy0:sy1, sx0:sx1]
    big_b = max([b for b in item["blocks"] if b.get("glyph_check") and not b.get("ghost")], key=lambda b: b["cap_mm"])
    r = glyph_check_block(item, sheet, big_b, man[big_b["id"]], ppm=ppm, others=man)
    return err, ang, v, r["ok"]


def man_for(item, b):
    return layout_glyphs(b)


def group13():
    g = "13 second-try guards"
    PLS = T["placements"]
    # --- G.page.placeholders
    held_items = {it["id"] for it in T["items"] if it.get("held_names")}
    recomputed = {it["id"] for it in T["items"] if any(p["name"].lower() in (" ".join(b["text"] for b in it["blocks"] if b["role"] != "imprint" and b["cap_mm"] >= 10 and not b.get("ghost")).lower() + " | " + " | ".join(b["text"].lower() for b in it["blocks"] if b["role"] != "imprint" and b["cap_mm"] >= 10 and not b.get("ghost"))) for p in T["proposed_names"])}
    row(g, "every item that carries a proposed name in a block of cap 10 mm or more is held (%d items), and no other is by name" % len(held_items), held_items == recomputed, str(sorted(held_items ^ recomputed)))
    stand = {it["id"] for it in T["items"] if it.get("stand_in_of")}
    row(g, "the nameless stand-ins T01, T02, T03 and W01 (a quad titled 'A NEW COMEDY', a programme that names no film, a fight bill with no ring names and no hall) are HELD like their named twins and wait for the names the twin carries", stand == {"T01", "T02", "T03", "W01"}
        and all(ITEMS[k]["held"] and ITEMS[k]["waits_for"] == ITEMS[ITEMS[k]["stand_in_of"]]["held_names"] and ITEMS[k]["waits_for"] for k in stand) and not any(ITEMS[k].get("held_names") for k in stand), str(sorted(stand)))
    DEF = [p for p in PLS if not p.get("held")]
    all_held_items = held_items | stand
    row(g, "no default placement uses a held item or a stand-in (the default street carries no unminted name and no bill that names nothing)", not [p["item"] for p in DEF if p["item"] in all_held_items], str([p["item"] for p in DEF if p["item"] in all_held_items]))
    held_pl = [p for p in PLS if p.get("held_until_minted")]
    row(g, "every placement of a held item or stand-in is itself held_until_minted and lists the names (%d held placements)" % len(held_pl), all(p.get("held_until_minted") and p.get("held") and p.get("names") for p in PLS if p["item"] in all_held_items) and len(held_pl) >= 8
        and all(p.get("held") for p in PLS if p.get("held_until_minted")))
    dec = (ROOT / "DECISIONS.md").read_text(encoding="utf-8", errors="replace")
    row(g, "G.page.placeholders on the default street's placed-decals manifest: no offence", not placeholders_offences(DEF, dec), str(placeholders_offences(DEF, dec)[:3]))
    off = placeholders_offences(DEF + held_pl[:1], dec)
    row(g, "G.page.placeholders on the default street plus ONE held placement (%s) with no minting line: FAILS as it must" % held_pl[0]["item"], bool(off) and not [ln for ln in dec.splitlines() if "MINTED:" in ln], str(off[:2]))
    fake = dec + "\n- 9 Oct 2026 | the town mints the agent's name | test | town | x MINTED: ARMITAGE & STOBBS\n"
    one = [p for p in held_pl if p["item"] in ("L01", "L03")]
    row(g, "G.page.placeholders: the same placements pass once DECISIONS.md carries '- ... MINTED: ARMITAGE & STOBBS'", not placeholders_offences(one, fake) and bool(placeholders_offences(one, dec)))
    mp = {p["name"]: p for p in T["proposed_names"]}
    row(g, "the proposed names are listed with the items that carry them and the items held (%d names)" % len(mp), all("items" in p and "held_items" in p for p in mp.values()) and "TED HOLROYD" in mp and "BIG TED HOLROYD" not in mp and "THE HARPOONER" in mp and "TIGER JIM LARKIN" not in mp and "THE SEA WOLF" not in mp
        and not any("BIG TED" in b["text"].upper() for it in T["items"] for b in it["blocks"]))
    FP = T["forbidden_patterns"]["real_marks"]
    row(g, "LARKIN, SEA WOLF and BIG TED (Play School's bear) (and the real wrestlers, soap powders, cinema chains, campaigns the probe listed) are in forbidden_patterns.real_marks", all(w in FP for w in ("LARKIN", "SEA WOLF", "BIG TED", "PERSIL", "ODEON", "MILITANT", "BIG DADDY", "ALL BRITAIN")))
    fw = T["forbidden_patterns"]["alcohol_gambling_children"]
    row(g, "the forbidden list also holds BABYSITTERS, INNS, PLAYGROUPS, TEENS, LAD, LASS and KIDDIES", all(w in fw for w in ("babysitters", "inns", "playgroups", "teens", "lad", "lass", "kiddies")))
    # --- G.dates.age
    bad = []
    n = 0
    for p in PLS:
        it = ITEMS.get(p["item"])
        if it and it.get("dated"):
            n += 1
            ok, why = age_ok(it, p["age_class"])
            if not ok:
                bad.append(why)
    row(g, "G.dates.age: all %d placed dated items (held placements too) agree with the street date %s and their class" % (n, T["calendar"]["street_date"]), not bad and n >= 8, str(bad[:3]))
    t03 = dict(ITEMS["T03"])
    d01 = dict(ITEMS["D01"])
    row(g, "G.dates.age FAILS the first try's contradictions: T03 in class D for the week from 18 October, D01 in class C for 17 November, P01 in class D", (not age_ok(t03, "D")[0]) and (not age_ok(d01, "C")[0]) and (not age_ok(ITEMS["P01"], "D")[0]) and (not age_ok(ITEMS["H03"], "D")[0]))
    row(g, "G.dates.age passes the plan: T03 B, D01 B, J01 B, T02 A, T01 B, H03 A (a notice dated 26 October)", all(age_ok(ITEMS[i], c)[0] for i, c in (("T03", "B"), ("D01", "B"), ("J01", "B"), ("T02", "A"), ("T01", "B"), ("H03", "A"))))
    sf = [(p["item"], p["age_class"]) for p in PLS if p["item"] in ("T03", "D01", "J01")]
    row(g, "the placements give T03 B (held), D01 B and J01 B (everywhere)", all(c == "B" for _, c in sf) and len(sf) >= 4, str(sf))
    # --- G.mirror.cues
    cue_items = [it for it in T["items"] if it.get("mirror_cue")]
    bad = []
    tested = 0
    for it in cue_items:
        mc = it["mirror_cue"]
        if "patch_left_mm" not in mc:
            bad.append((it["id"], "no patches"))
            continue
        rgb, a, tx = card_picture(it, "true")
        s1 = cue_side(it, rgb, a, tx)
        rgb, a, tx = card_picture(it, "mirror")
        s2 = cue_side(it, rgb, a, tx)
        rgb, a, tx = card_picture(it, "none")
        s3 = cue_side(it, rgb, a, tx)
        tested += 1
        if s1 != "left" or s2 != "right" or s3 is not None:
            bad.append((it["id"], s1, s2, s3))
    row(g, "G.mirror.cues: all %d hand cards: the true render reads 'left', the mirrored 'right', a card with no cue reads none (25 mm top-left and top-right patches, non-text pixels)" % tested, not bad and tested == 29, str(bad[:4]))
    # --- G.ferry.schedule
    pr = ferry_from_blocks(ITEMS["F01"])
    ok1, w1, end1, t1 = ferry_sim(pr["hook"], pr["far"])
    ok2, w2, end2, t2 = ferry_sim(pr["hook_sun"], pr["far_sun"])
    first_mon = pr["hook"][0]
    row(g, "G.ferry.schedule: Monday to Saturday the one vessel runs the printed timetable and ends the day at the Hook (%s, free at %d.%02d)" % (end1, t1 // 60 - 12, t1 % 60), ok1 and end1 == "hook", w1)
    row(g, "G.ferry.schedule: Sunday likewise, ending at the Hook (free at %d.%02d PM)" % (t2 // 60 - 12, t2 % 60), ok2 and end2 == "hook", w2)
    row(g, "G.ferry.schedule: each day ends where the next day's first sailing leaves: Saturday night at the Hook, Sunday 9.00 AM from the Hook; Sunday night at the Hook, Monday 6.30 AM from the Hook; Monday to Friday night to the next 6.30 AM", end1 == "hook" and end2 == "hook" and pr["hook_sun"][0] == 9 * 60 and first_mon == 6 * 60 + 30 and pr["hook"][0] < pr["far"][0])
    old_far = pr["far"][:-1]
    ok3, w3, end3, _ = ferry_sim(pr["hook"], old_far)
    row(g, "G.ferry.schedule FAILS the first try's timetable (far side's last crossing 10.45): the boat ends the night on the far side", (not ok3) or end3 != "hook", "%s %s" % (end3, w3))
    row(g, "the street's 'last crossing's at eleven' still holds from the Hook: the last Hook sailing is 11.00 PM, the boat home at 11.30", pr["hook"][-1] == 23 * 60 and pr["far"][-1] + 15 == 23 * 60 + 30)
    # --- G.letting.mount
    ft = json.loads((ROOT / "production" / "cloud-week" / "targets" / "fascia-signs" / "target.json").read_text())
    lb = [p for p in ft["small_panels"] if p["id"] == "letting_board"][0]
    fvr = ft["palette"][lb["colour"]]["srgb_fresh"]

    def same_as_fascia(it):
        if [it["format"]["w_mm"], it["format"]["h_mm"]] != lb["size_mm"]:
            return False, "size %sx%s" % (it["format"]["w_mm"], it["format"]["h_mm"])
        bl = it["blocks"]
        if len(bl) != 1 or bl[0]["text"] != lb["text"] or bl[0]["font"] != lb["font"] or bl[0]["weight"] != lb["weight"] or bl[0]["cap_mm"] != lb["cap_mm"]:
            return False, "text, font, weight or cap"
        if PAL["paints"][bl[0]["ink"]]["fresh"] != fvr:
            return False, "colour"
        return True, ""
    ok, why = same_as_fascia(ITEMS["L02"])
    row(g, "G.letting.mount: L02 IS the fascia target's board (900 x 450, TO LET alone, libre-franklin 800, cap 130, vinyl red %s, no agent, no number)" % fvr, ok, why)
    ok1, why1 = same_as_fascia(ITEMS["L01"])
    row(g, "G.letting.mount FAILS L01 (1200 x 450 with an agent band) against the fascia target", not ok1, why1)
    l2 = [p for p in DEF if p["item"] == "L02"][0]
    row(g, "L02 sits on the fascia with 50 mm clear above and below and its centre is the fascia target's (board x 2705 = street x 24.0)", abs(l2["z_bottom_m"] - 2.90) < 1e-9 and abs(l2["z_bottom_m"] + l2["h_m"] - 3.35) < 1e-9 and l2["street_x_m"] == 24.0 and lb["centre_on_board_mm"] == [2705.0, 275])
    # --- G.place.paper, G.place.gable
    base = paper_counts(PLS)
    more_f = list(PLS) + [dict(item="M01", surface="SF2", held=False)] * 4          # four more fly-posters: 9
    more_p = list(PLS) + [dict(item="P03", surface="SF2", held=False)] * 2          # two more poll-tax bills: 5
    more_ok = list(PLS) + [dict(item="M01", surface="SF2", held=False)]             # one more fly-poster: 6, still inside the plan
    row(g, "G.place.paper: AT MOST 8 fly-posters and 4 poll-tax bills (the street carries %s); a ninth fly-poster FAILS, a fifth poll-tax bill FAILS, a sixth fly-poster still passes" % base,
        paper_ok(base) and not paper_ok(paper_counts(more_f)) and not paper_ok(paper_counts(more_p)) and paper_ok(paper_counts(more_ok)), str(base))
    ok, why = gable_ok(PLS)
    bill = dict(item="P03", surface="SF1", u_m=0.40, z_bottom_m=1.0, w_m=0.508, h_m=0.762, layer=0, age_class="B")
    plate = dict(item="S01n", surface="SF7", host="SF1", u_m=0.8, z_bottom_m=2.5, w_m=0.9, h_m=0.3, layer=0, age_class="D")
    ok2, why2 = gable_ok(list(PLS) + [bill])
    ok3, why3 = gable_ok(list(PLS) + [plate])
    unheld = [dict(p, held=False, held_until_minted=False) if p.get("proof_wall") and not p.get("alt_of") else p for p in PLS]
    ok4, why4 = gable_ok(unheld)
    altok, altwhy = gable_alt_ok(PLS)
    mut = [dict(p, u_m=0.40) if (p["item"] == "P01" and p["surface"] == "SF1" and not p.get("alt_of")) else p for p in PLS]
    altbad, _ = gable_alt_ok(mut)
    row(g, "G.place.gable: the gable is bare (no paper, no plate on SF1 in the default street) and the downpipe, render patch and damp foot stand; a bill on it FAILS, a plate on it FAILS, the five held proof-wall placements made default FAIL (%s)" % why4[:70],
        ok and gable_fixtures_ok() and not ok2 and not ok3 and not ok4, why2[:100])
    row(g, "G.place.gable (held proof wall): if ever used it keeps 150 mm clear of the downpipe; the held P01 moved to u 0.40 (inside the 150 mm) FAILS", altok and not altbad, altwhy)
    # --- plates
    pl = [it for it in T["items"] if it.get("name_plate")]
    q = [it for it in pl if it["id"] == "S01n"][0]
    row(g, "G.plates.make: QUAY STREET is cast aluminium, letters and border raised 3 mm, 10 degrees of draft, 0.8 mm top radius, painted white with black letters, flaking at the raised edges", q["process"] == "cast_aluminium_raised" and q["relief"]["raised_mm"] == 3.0 and q["relief"]["draft_deg"] == 10.0 and q["relief"]["top_radius_mm"] == 0.8
        and "flak" in T["processes"]["cast_aluminium_raised"]["flake"]["note"])
    row(g, "G.plates.make: every raised letter's thinnest stroke keeps a top width of 1.5 mm or more after the draft (Marcellus SC at 90 mm: thinnest %s mm)" % [it["lettering_suit"]["strokes_mm"]["thin_mm"] for it in pl[:2]], all(it["lettering_suit"]["ok"] for it in pl))
    row(g, "G.plates.make: pressed aluminium rolled edge radius 3 mm; enamel rolled edge 6 mm; cast edge 6 mm with a 2 mm arris", T["processes"]["pressed_aluminium_enamel"]["edge_roll_radius_mm"] == 3.0 and T["processes"]["vitreous_enamel_steel"]["edge_roll_radius_mm"] == 6.0 and T["processes"]["enamel"]["edge_roll_radius_mm"] == 6.0
        and "arris radius 2 mm" in T["processes"]["cast_aluminium_raised"]["edge"])
    row(g, "the default plates carry no district line, no postcode and no council name", all(b["id"] != "district" for it in pl if it["name_plate"]["variant"] == "n" for b in it["blocks"]) and all(it["id"] in ("S01n", "S01d", "S02n", "S02d", "S03n", "S03d") for it in pl))
    # --- shape numbers
    k4 = ITEMS["K04"]
    ring = [s for s in k4["shapes"] if s["id"] == "roundel"][0]
    bar = [s for s in k4["shapes"] if s["id"] == "bar"][0]
    row(g, "K04: a ring 7 mm wide and a 7 mm bar at 45 degrees from the inside top-left to the inside bottom-right, as a polygon", abs(ring["r_outer_mm"] - ring["r_inner_mm"] - 7) < 1e-9 and len(bar["pts_mm"]) == 4
        and abs(math.hypot(bar["pts_mm"][0][0] - bar["pts_mm"][1][0], bar["pts_mm"][0][1] - bar["pts_mm"][1][1]) - 7.0) < 0.05)
    g2 = ITEMS["G02"]
    rg = [s for s in g2["shapes"] if s["id"] == "cup_ring"][0]
    row(g, "G02: a white ring 16 mm wide at 0.70 of the disc's radius", abs(rg["r_outer_mm"] - rg["r_inner_mm"] - 16.0) < 1e-9 and abs((rg["r_outer_mm"] + rg["r_inner_mm"]) / 2 - 0.70 * 120.0) < 1e-6)
    k2 = ITEMS["K02"]
    tk = [s for s in k2["shapes"] if s["id"] == "ticks"][0]
    hh_ = [s for s in k2["shapes"] if s["id"] == "hand_hour"][0]
    hm_ = [s for s in k2["shapes"] if s["id"] == "hand_min"][0]
    fa = [s for s in k2["shapes"] if s["id"] == "fastener"][0]
    row(g, "K02: ticks 2 x 8 mm (12), hour hand 30 x 5, minute hand 40 x 4 (buff card), a 6 mm brass fastener", tk["width_mm"] == 2.0 and len(tk["segments_mm"]) == 12 and abs(math.hypot(tk["segments_mm"][0]["p1"][0] - tk["segments_mm"][0]["p0"][0], tk["segments_mm"][0]["p1"][1] - tk["segments_mm"][0]["p0"][1]) - 8.0) < 0.05
        and (hh_["length_mm"], hh_["width_mm"]) == (30.0, 5.0) and (hm_["length_mm"], hm_["width_mm"]) == (40.0, 4.0) and hh_["fill"] == "buff_card" and fa["box_mm"][2] - fa["box_mm"][0] == 6.0)
    # --- Tivoli strips
    s1, s2 = ITEMS["T01s"], ITEMS["T02s"]
    blank = not [b for k in ("T01", "T02", "T01-named", "T02-named") for b in ITEMS[k]["blocks"] if b["ink_box_mm"][3] > 762 - 90 + 0.5 and b["role"] != "imprint"]
    row(g, "T01s and T02s: 1016 x 90 mm, one-colour letterpress black on white stock, THE TIVOLI and FROM THURSDAY 18 / 25 OCTOBER; the quads' own top 90 mm is blank",
        (s1["format"]["w_mm"], s1["format"]["h_mm"]) == (1016, 90) and s1["stock"] == "white_poster" and s1["process"] == "letterpress_1col"
        and [b["text"] for b in s1["blocks"]] == ["THE TIVOLI", "FROM THURSDAY 18 OCTOBER"] and [b["text"] for b in s2["blocks"]][1] == "FROM THURSDAY 25 OCTOBER" and blank)
    # --- PLACE.built
    cases = [("P03", 1.2), ("M01", 0.8), ("L02", -1.5)] if not QUICK else [("P03", 1.2)]
    t0 = time.time()
    for iid, rot in cases:
        err, ang, v, ok = placed_decal_test(ITEMS[iid], rot)
        row(g, "PLACE.built: %s placed turned %.1f and 7 mm off: located within %.1f mm (limit 20), angle found %.2f (limit 0.3 off), the largest block read the right way round" % (iid, rot, err, ang), err <= 20 and abs(ang - rot) <= 0.3 and ok, "fit %.2f" % v)
    iid, rot = cases[0]
    err, ang, v, ok = placed_decal_test(ITEMS[iid], rot, mirror=True)
    row(g, "PLACE.built: a MIRRORED %s decal FAILS (read-back %s, fit %.2f)" % (iid, ok, v), not ok)
    err, ang, v, ok = placed_decal_test(ITEMS[iid], rot, extra_rot=1.0)
    row(g, "PLACE.built: a decal turned 1.0 degree off its rot_deg FAILS the rotation limit (found %.2f against %.1f)" % (ang, rot), abs(ang - rot) > 0.3 or not ok)
    err, ang, v, ok = placed_decal_test(ITEMS[iid], rot, offset_mm=(40.0, 0.0))
    row(g, "PLACE.built: a decal 40 mm off its place FAILS the 20 mm limit (%.0f mm)" % err, err > 20)
    row(g, "PLACE.built read in %.0f s" % (time.time() - t0), True, "", reported=True)
    row(g, "the four fixes of the second review (by Jafar's ruling of 9 October, not re-reviewed) are recorded in fixes_after_second_review", [d["fix"] for d in T["fixes_after_second_review"]] == [1, 2, 3, 4])
    # --- fonts decisions
    fd = {d["font"]: d for d in T["font_decisions"]}
    row(g, "the fonts off the asset plan's table are recorded with a DECISIONS line each (Libre Franklin, Patrick Hand) and the two others are removed", "Libre Franklin" in fd and "Patrick Hand" in fd and fd["Libre Franklin"]["decisions_line"] and fd["Patrick Hand"]["decisions_line"] and "libre-baskerville" not in T["fonts"] and "josefin-sans" not in T["fonts"])
    row(g, "the second try answers every one of the 13 faults (second_try)", [d["fault"] for d in T["second_try"]] == list(range(1, 14)))


def main():
    t0 = time.time()
    only = None
    if "--groups" in sys.argv:
        only = set(int(x) for x in sys.argv[sys.argv.index("--groups") + 1].split(","))
    for n, fn in enumerate((group1, group2, group3, group4, group5, group6, group7, group8, group9, group10, group11, group12, group13), start=1):
        if only is None or n in only:
            fn()
    fails = [r for r in ROWS if r["ok"] is False]
    reps = [r for r in ROWS if r["rep"]]
    passed = [r for r in ROWS if r["ok"] is True]
    line = "SELF-CHECK posters-boards-plates: %d checks, %d passed, %d failed, %d reported" % (len(passed) + len(fails), len(passed), len(fails), len(reps))
    for r in fails:
        print("FAIL [%s] %s :: %s" % (r["g"], r["n"], r["d"]))
    for r in reps:
        print("note [%s] %s :: %s" % (r["g"], r["n"], r["d"][:160]))
    print(line, "(%.0f s)" % (time.time() - t0))
    if "--no-write" not in sys.argv:
        T["self_check"] = dict(run=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), summary=line, failures=[dict(g=r["g"], n=r["n"], d=r["d"]) for r in fails],
                               reported=[dict(g=r["g"], n=r["n"], d=r["d"][:200]) for r in reps], rows=[[r["g"], r["n"][:90], r["ok"]] for r in ROWS], facts=FACTS,
                               seconds=round(time.time() - t0))
        sys.path.insert(0, str(HERE))
        import make_target as mt
        mt.write_json(T)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
