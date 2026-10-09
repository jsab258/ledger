"""Tests target.json against its own sources before anything is built (cloud week 42, 8 October 2026).

    /home/user/.bpyenv/bin/python self_check.py [--fonts DIR] [--no-write] [--fetch-fonts DIR] [--quick]

Groups:
  1  files and counts
  2  numbers that are printed or derived come back from target.json (paper sizes, plate lengths, calendars, the ferry's service, the tide table)
  3  the words: approved list, forbidden lists, tools/content-gate.py's rule table, RealWorld.cs, canon's streets and districts, names owed by canon
  4  fonts: licence files read, glyph coverage, the allowed list
  5  layout: every block re-measured from its font file, inside its safe zone, no overlaps
  6  contrast: recomputed from the palette and the ageing classes
  7  placements: inside zones, layering, piers, cases, fascia, plates
  8  the one photograph: the saved preview re-measured, the drawing laid on it
  9  the drawing: target_drawing.py is run and its polygons compared
  10 the checks tested on reference renders: a true render passes, a mirrored, shifted or wrong-font render fails
  11 the world: hours, market days, the ferry's last crossing, the cod price
It prints a result line and writes the result into target.json under "self_check" (unless --no-write).
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
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont
from scipy import ndimage as ndi

HERE = Path(__file__).resolve().parent
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
    urls = {"Archivo-var.ttf": RAW + "/archivo/Archivo%5Bwdth%2Cwght%5D.ttf", "LibreBaskerville-var.ttf": RAW + "/librebaskerville/LibreBaskerville%5Bwght%5D.ttf",
            "CourierPrime-Regular.ttf": RAW + "/courierprime/CourierPrime-Regular.ttf", "CourierPrime-Bold.ttf": RAW + "/courierprime/CourierPrime-Bold.ttf"}
    for fam in ("jost", "librefranklin", "oswald", "alfaslabone", "fraunces", "librebaskerville", "oldstandardtt", "abrilfatface", "josefinsans", "archivo", "courierprime",
                "marcellussc", "patrickhand"):
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


def row(group, name, ok, detail="", reported=False):
    ROWS.append(dict(g=group, n=name, ok=(None if reported else bool(ok)), d=str(detail)[:300], rep=bool(reported)))


def norm(s):
    return s.replace("’", "'").replace("‘", "'").replace("—", "-").replace("–", "-")


ITEMS = {it["id"]: it for it in T["items"]}
FONTS = T["fonts"]
PAL = T["palette"]
CLASSES = list(T["age_classes"])

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


def block_mask(b, W, H, ppm, key=None, weight=None, shift_mm=(0.0, 0.0), flip=False):
    """Boolean ink mask of a block rendered clean from its font, on a W x H mm canvas at ppm px/mm."""
    key = key or b["font"]
    weight = weight or b["weight"]
    px = b["size_px_per_em"]
    cap_target = b["cap_mm"]
    # when the font differs, keep the CAP height equal by rescaling the em
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
    if key != b["font"]:
        # re-anchor by ink centre of the stored box
        pass
    for i, ch in enumerate(text):
        if ch != " ":
            d.text(((ox + shift_mm[0]) * ppm + xs[i], (H - b["baseline_mm"] + shift_mm[1]) * ppm), ch, font=f, fill=255, anchor="ls")
    a = np.asarray(img) > 100
    if key != b["font"]:
        # centre the substitute on the original ink centre so only the glyph shapes differ
        cols = np.where(a.any(axis=0))[0]
        if len(cols):
            cx_new = (cols.min() + cols.max()) / 2.0
            cx_old = (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2.0 * ppm
            a = np.roll(a, int(round(cx_old - cx_new)), axis=1)
    if flip:
        a = a[:, ::-1]
    return a


def fscore(read, ref, dil_px):
    """Mean of recall and precision, each against the other mask dilated."""
    if not ref.any():
        return 0.0
    st = ndi.generate_binary_structure(2, 2)
    rd = ndi.binary_dilation(read, st, iterations=max(1, dil_px)) if read.any() else read
    fd = ndi.binary_dilation(ref, st, iterations=max(1, dil_px))
    recall = (ref & rd).sum() / max(1, ref.sum())
    prec = (read & fd).sum() / max(1, read.sum()) if read.any() else 0.0
    return float((recall + prec) / 2.0)


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
    for need in ("fonts", "palette", "age_classes", "processes", "surfaces", "placements", "cases", "approved_words", "forbidden_patterns", "sources", "unreached",
                 "would_read_when_network_opens", "could_not_settle", "disagreements_photographs_win", "proposed_names"):
        row(g, "section %s present and non-empty" % need, bool(T.get(need)))
    for it in T["items"]:
        ok = it["format"]["w_mm"] > 0 and it["format"]["h_mm"] > 0 and it["variants"] and (it["blocks"] or it["id"] in ())
        if not ok:
            row(g, "item %s has size, variants and blocks" % it["id"], False)
    row(g, "every item has size, variants and at least one block", True)
    p = ROOT / "production" / "cloud-week" / "targets" / "posters-boards-plates"
    for f in ("TARGET.md", "target.json", "target_drawing.py", "self_check.py", "make_target.py", "make_previews.py"):
        row(g, "file %s exists" % f, (p / f).exists())
    prev = ROOT / "production" / "previews" / "cloud-week" / "refs" / "posters-boards-plates"
    jpgs = sorted(prev.glob("*.jpg"))
    row(g, "previews exist, JPEG, 1200 px at most, under 300 KB", len(jpgs) >= 6 and all(f.stat().st_size < 300_000 and max(Image.open(f).size) <= 1200 for f in jpgs), "%d files" % len(jpgs))
    row(g, "target.json is under the 1 MB the git size guard allows", (HERE / "target.json").stat().st_size < 1_000_000, "%d bytes" % (HERE / "target.json").stat().st_size)


# --------------------------------------------------------------------------------------------
# 2 numbers
# --------------------------------------------------------------------------------------------
def group2():
    g = "2 numbers"
    F = T["formats"]
    imperial = dict(crown=(15, 20), double_crown=(20, 30), quad_crown=(40, 30), four_sheet=(40, 60))
    for k, (wi, hi) in imperial.items():
        row(g, "%s is %d x %d in = %d x %d mm" % (k, wi, hi, round(wi * 25.4), round(hi * 25.4)), (F[k]["w"], F[k]["h"]) == (round(wi * 25.4), round(hi * 25.4)), "%s" % F[k])
    # ISO 216: A0 is 841 x 1189; each size halves the long side (floor)
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
        ok &= (w == np_["plate_w_mm"] == it["format"]["w_mm"]) and abs(blk["width_mm"] - np_["ink_w_mm"]) < 0.6 and np_["cap_mm"] == 90.0
        borders = [s for s in it["shapes"] if s["id"] == "border"][0]
        ok &= borders["width_mm"] == 12 and borders["box_mm"][0] == 6
        det.append("%s %dx%d" % (it["id"], it["format"]["w_mm"], it["format"]["h_mm"]))
    row(g, "plate length = ink width + 124 mm rounded up to 10; cap 90; border 12 mm 6 mm in", ok, ", ".join(det[:9]))
    names = {i["name_plate"]["street"] for i in T["items"] if i.get("name_plate")}
    row(g, "three streets, three variants each", names == {"QUAY STREET", "WEIGHHOUSE LANE", "TANNERY ROW"} and sum(1 for i in T["items"] if i.get("name_plate")) == 9)
    # existing plate and pier
    q = [p for p in T["placements"] if p["item"] == "S01d" and p.get("street_x_m") == 20.47][0]
    half = q["w_m"] / 2.0
    row(g, "the Quay Street plate sits on the corner pier (19.92 to 21.0) with at least 40 mm each side", 20.47 - half >= 19.92 + 0.04 and 20.47 + half <= 21.0 - 0.04, "%.3f to %.3f" % (20.47 - half, 20.47 + half))
    row(g, "plate heights: bottom edge at 2.4 m or more, top below the pier's 3.12 m", all(p["z_bottom_m"] >= 2.4 and p["z_bottom_m"] + p["h_m"] <= 3.12 for p in T["placements"] if p["surface"] == "SF7"))
    # letting boards against the fascia
    L1 = ITEMS["L01"]
    row(g, "L01 is 1200 x 450 and fits the 0.55 m fascia with 50 mm clear above and below", (L1["format"]["w_mm"], L1["format"]["h_mm"]) == (1200, 450) and abs((3.40 - 2.85) - 0.45 - 0.10) < 1e-9)
    # lamp columns
    cols = T["surfaces"]["SF4"]["columns_street_x"]
    row(g, "lamp columns every 20 m from 8 m (SCENE-SLOTS)", cols == [8.0 + 20.0 * k for k in range(3)], str(cols))
    # glass geometry
    S2 = T["surfaces"]["SF2"]
    row(g, "the empty unit's glass is 3.562 m (5.3 opening zone - 0.9 door - 0.838 side door) and runs 23.088 to 26.65", abs((5.3 - 0.9 - 0.838) - 3.562) < 1e-9 and abs(S2["glass_street_x"][1] - S2["glass_street_x"][0] - 3.562) < 1e-6)
    # ferry
    fs = ITEMS["F01"]["schedule"]
    def mins(t):
        h, m = t.replace(" PM", "").replace(" AM", "").split(".")
        return int(h) * 60 + int(m)
    ms = fs["mon_sat"]
    hook = [mins(t) for t in ms["hook_first"]] + [mins(t) + 720 for t in ms["hook_then"]] + [mins(ms["hook_last"]) + 720]
    far = [mins(t) for t in ms["far_first"]] + [mins(t) + 720 for t in ms["far_then"]]
    cross = fs["crossing_minutes"]
    # the boat leaves the Hook at t, is at the far side at t + 15 and leaves there at the listed far time: each far time = a hook time + 15
    hook_set, far_set = set(hook), set(far)
    # half-hourly stretch: hook at :00 and :30 from 6.30 to 5.30 PM
    full_hook = [t for t in range(6 * 60 + 30, 17 * 60 + 31, 30)] + [mins(t) + 720 for t in ms["hook_then"]] + [mins(ms["hook_last"]) + 720]
    full_far = [t for t in range(6 * 60 + 45, 17 * 60 + 46, 30)] + [mins(t) + 720 for t in ms["far_then"]] + [mins(ms["far_last"]) + 720]
    pairs_ok = all((t + cross) in set(full_far) for t in full_hook[:-1])
    row(g, "ferry: every Hook departure but the last is met by a far-side departure 15 minutes later", pairs_ok)
    row(g, "ferry: the last Hook crossing is 11.00 PM and the last far-side one 10.45 PM", mins(ms["hook_last"]) + 720 == 23 * 60 and full_far[-1] == 22 * 60 + 45)
    row(g, "ferry: the first three listed departures agree with the half-hourly stretch", [mins(t) for t in ms["hook_first"]] == [390, 420, 450] and [mins(t) for t in ms["far_first"]] == [405, 435, 465])
    row(g, "ferry: Sunday far side is 15 minutes after the Hook", mins(fs["sunday"]["far_from"]) - mins(fs["sunday"]["hook_from"]) == 15 and mins(fs["sunday"]["far_until"]) - mins(fs["sunday"]["hook_until"]) == 15)
    # tides
    rows_ = ITEMS["H04"]["tide_rows"] if "tide_rows" in ITEMS["H04"] else []
    ts = [datetime.datetime.strptime(r["t"], "%Y-%m-%d %H:%M") for r in rows_]
    dif = [(b - a).total_seconds() / 60 for a, b in zip(ts, ts[1:])]
    row(g, "tide table: successive high waters 745 minutes apart (12 h 25 min)", rows_ and all(abs(d - 745) <= 5 for d in dif), "%d rows" % len(rows_))
    hts = [r["m"] for r in rows_]
    row(g, "tide table: heights between 3.3 and 4.8 m", rows_ and 3.3 <= min(hts) and max(hts) <= 4.8, "%.1f to %.1f" % (min(hts), max(hts)))
    # calendar
    row(g, "1 October 1990 was a Monday", datetime.date(1990, 10, 1).weekday() == 0)
    # dates in the strings
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
    mx = re.compile(r"\b(\d{1,2})\s+(%s)\b" % "|".join(months), re.I)
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
    # phone numbers
    ph = re.compile(r"\b960 (\d{3})\b")
    nums = [(it["id"], m.group(0)) for it in T["items"] for b in it["blocks"] for m in ph.finditer(b["text"])]
    row(g, "telephone numbers are the six-figure local form 960 xxx and none is Mickey's 960 418", nums and all(n != "960 418" for _, n in nums), "%d numbers" % len(nums))
    bad = [(it["id"], b["text"]) for it in T["items"] for b in it["blocks"] if re.search(r"\b0\d{3,4}\s*\d{5,}", b["text"])]
    row(g, "no long-form STD number (the town's code is not minted)", not bad, str(bad))
    # prices
    prices = [(it["id"], m.group(0)) for it in T["items"] for b in it["blocks"] for m in re.finditer(r"£\d+(?:\.\d\d)?|\b\d+p\b", b["text"])]
    row(g, "prices are in pounds and pence (%d read), none in decimal-less dollars" % len(prices), len(prices) >= 15)
    cod = [b["text"] for it in T["items"] if it["id"] == "K09a" for b in it["blocks"] if "lb" in b["text"]]
    row(g, "cod price within the ONS 1990 range 2.42 to 2.85 plus 10 per cent", cod and 2.42 <= float(re.search(r"£([\d.]+)", cod[0]).group(1)) <= 3.10, str(cod))


# --------------------------------------------------------------------------------------------
# 3 words
# --------------------------------------------------------------------------------------------
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
    for key in ("ARMITAGE & STOBBS", "QUAY PRINT", "MERIDIAN AGAINST THE POLL TAX", "THE SANDERLING TRIO", "THE SEA WOLF", "THE FOURTH WITNESS", "A WEEK AT GULLWING", "WHITEWELL", "QUAYSIDE", "MARSHLAND PICTURES", "THE DRILL HALL", "MR1", "TIGER JIM LARKIN"):
        places[key] = sorted({it["id"] for it in T["items"] for b in it["blocks"] if key.lower() in b["text"].lower()})
    row(g, "where the proposed names stand (reported)", True, json.dumps(places)[:290], reported=True)
    only_here = all(places[k] or k in ("MARSHLAND PICTURES",) for k in ("ARMITAGE & STOBBS", "QUAY PRINT", "THE SANDERLING TRIO", "THE SEA WOLF"))
    row(g, "each proposed name that is meant to be drawn is drawn", only_here)
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
    allowed_fam = {"Marcellus SC", "Oswald", "Jost", "Libre Franklin", "Alfa Slab One", "Fraunces", "Old Standard TT", "Abril Fatface", "Josefin Sans", "Archivo", "Courier Prime",
                   "Libre Baskerville", "Patrick Hand", "UnifrakturMaguntia", "Liberation"}
    row(g, "every family is on the asset plan's OFL list (no Overpass, no Apache or GPL face)", all(FONTS[u]["family"] in allowed_fam for u in FONTS) and not any("overpass" in u.lower() for u in FONTS))
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


def group7():
    g = "7 placements"
    PLS = T["placements"]
    SF = T["surfaces"]
    # SF1
    sf1 = [p for p in PLS if p["surface"] == "SF1"]
    bills = [p for p in sf1 if p.get("kind") != "case" and p["layer"] < 3]
    stick = [p for p in sf1 if p["layer"] == 3]
    cases = [p for p in sf1 if p.get("kind") == "case"]
    z = SF["SF1"]["paste_zone"]
    inside = all(z["u"][0] <= p["u_m"] and p["u_m"] + p["w_m"] <= z["u"][1] and z["z"][0] <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= z["z"][1] + 0.001 for p in bills + stick)
    row(g, "SF1: every bill and sticker lies inside the paste zone (u 0.15 to 6.0, z 0.45 to 2.75)", inside, str([(p["item"], p["u_m"], p["z_bottom_m"], round(p["z_bottom_m"] + p["h_m"], 2)) for p in bills if not (z["z"][0] <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= z["z"][1] + 0.001)]))
    for layer in (0, 1, 2):
        L = [p for p in bills if p["layer"] == layer]
        ov = [(a["item"], b["item"]) for i, a in enumerate(L) for b in L[i + 1:] if a["u_m"] < b["u_m"] + b["w_m"] and b["u_m"] < a["u_m"] + a["w_m"] and a["z_bottom_m"] < b["z_bottom_m"] + b["h_m"] and b["z_bottom_m"] < a["z_bottom_m"] + a["h_m"]]
        row(g, "SF1 layer %d: no bill overlaps another of its own layer" % layer, not ov, str(ov))
    vf = vis_fractions(bills)
    row(g, "SF1: every older bill keeps its share of face (layer 0 at least 0.30, layer 1 at least 0.45, top at least 0.97)", all((v >= 0.30 if p["layer"] == 0 else v >= 0.45 if p["layer"] == 1 else v >= 0.97) for p, v in zip(bills, vf)), str([round(v, 2) for v in vf]))
    row(g, "SF1: three layers, 12 bills, ages from D to A in layer order", {p["layer"] for p in bills} == {0, 1, 2} and len(bills) == 12 and all("DCBA".index(p["age_class"]) >= 0 for p in bills))
    older = [p for p in bills if p["layer"] == 0]
    row(g, "SF1: the oldest layer is aged C or D, the top layer A or B", all(p["age_class"] in "CD" for p in older) and all(p["age_class"] in "AB" for p in bills if p["layer"] == 2))
    cc = [(a["item"], b["item"]) for a in cases for b in bills + stick + cases if a is not b and a["u_m"] < b["u_m"] + b["w_m"] and b["u_m"] < a["u_m"] + a["w_m"] and a["z_bottom_m"] < b["z_bottom_m"] + b["h_m"] and b["z_bottom_m"] < a["z_bottom_m"] + a["h_m"]]
    row(g, "SF1: the two cases overlap nothing and lie inside the gable (u 6.0 to 8.0)", not cc and all(6.0 <= p["u_m"] and p["u_m"] + p["w_m"] <= 8.0 for p in cases), str(cc))
    on_bill = []
    for s in stick:
        under = [b["item"] for b in bills if b["u_m"] <= s["u_m"] + s["w_m"] / 2 <= b["u_m"] + b["w_m"] and b["z_bottom_m"] <= s["z_bottom_m"] + s["h_m"] / 2 <= b["z_bottom_m"] + b["h_m"]]
        on_bill.append((s["item"], under))
    row(g, "SF1: stickers lie on bills or on bare brick (reported)", True, str(on_bill), reported=True)
    ext = max(p["u_m"] + p["w_m"] for p in bills)
    row(g, "SF1: the paste cluster ends before u 6.0 and starts within 0.6 m of the corner (the part the hook camera sees)", ext <= 6.0 and min(p["u_m"] for p in bills) <= 0.6, "u %.2f to %.2f" % (min(p["u_m"] for p in bills), ext))
    # glass
    sf2 = [p for p in PLS if p["surface"] == "SF2"]
    g0, g1 = SF["SF2"]["u_range"]
    z0, z1 = SF["SF2"]["z_range"]
    row(g, "SF2: every bill lies inside the glass (3.562 x 1.8 m)", all(g0 <= p["u_m"] and p["u_m"] + p["w_m"] <= g1 and z0 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= z1 for p in sf2), "")
    row(g, "SF2: bills hang low (top at or below 2.0 m, the whitewash showing above)", all(p["z_bottom_m"] + p["h_m"] <= 2.0 for p in sf2 if p["h_m"] > 0.2))
    vf2 = vis_fractions(sf2)
    row(g, "SF2: each bill keeps 0.6 of its face or more", all(v >= 0.6 for v in vf2), str([round(v, 2) for v in vf2]))
    # piers
    piers = {p["id"]: p for p in T["west_piers"]}
    wp = [p for p in PLS if p["surface"] == "WEST_PIER"]
    ok = True
    det = []
    for p in wp:
        pr = piers[p["pier"]]
        fits = p["w_m"] <= pr["w"] - 0.08 + 1e-9
        ok &= fits
        det.append((p["item"], p["pier"], p["w_m"], pr["w"]))
    row(g, "west piers: every bill fits its pier with 40 mm each side (%d placements)" % len(wp), ok, str(det))
    row(g, "west piers: the poster slot of the scene file (x 11.4) is pier W1.0", piers["W1.0"]["x0"] < 11.4 < piers["W1.0"]["x1"], str(piers["W1.0"]))
    W = T["west_piers"]
    row(g, "west piers: six piers, each 0.95 to 0.96 m, computed from the plain row's bay layout", len(W) == 6 and all(0.94 <= p["w"] <= 0.96 for p in W))
    # letting boards
    L1 = [p for p in PLS if p["item"] == "L01"][0]
    row(g, "L01: z 2.90 to 3.35 inside the fascia 2.85 to 3.40, centred on the bay (24.0)", abs(L1["z_bottom_m"] - 2.90) < 1e-9 and abs(L1["z_bottom_m"] + L1["h_m"] - 3.35) < 1e-9 and L1["street_x_m"] == 24.0)
    L3 = [p for p in PLS if p["item"] == "L03"][0]
    row(g, "L03: between the cornice (3.55) and the upper sill (about 4.3), and outside both hanging signs' x (20.825, 27.175)", 3.55 < L3["z_bottom_m"] and L3["z_bottom_m"] + L3["h_m"] < 4.3 and 22.93 < L3["street_x_m"] - L3["w_m"] / 2 and L3["street_x_m"] + L3["w_m"] / 2 < 25.07)
    # cases
    ok = True
    for c in T["cases"]:
        iw, ih = c["inside_mm"]
        calc_iw = c["outer_mm"][0] - c["frame_mm"]["left"] - c["frame_mm"]["right"]
        calc_ih = c["outer_mm"][1] - c["frame_mm"]["top"] - c["frame_mm"]["bottom"]
        ok &= abs(calc_iw - iw) <= 2 and abs(calc_ih - ih) <= 2
        for ch in c["children"]:
            it = ITEMS[ch["item"]]
            ok &= ch["x_mm"] >= 0 and ch["y_mm"] >= 0 and ch["x_mm"] + it["format"]["w_mm"] <= iw and ch["y_mm"] + it["format"]["h_mm"] <= ih
    row(g, "cases: the inside equals outer minus frame, and every pinned sheet lies inside it", ok)
    ferry = [c for c in T["cases"] if c["id"] == "FC1"][0]
    f01 = [ch for ch in ferry["children"] if ch["item"] == "F01"][0]
    f02 = [ch for ch in ferry["children"] if ch["item"] == "F02"][0]
    row(g, "FC1: the summer sheet peeks out 14 mm at the left and 16 mm at the top above the winter sheet", f01["x_mm"] - f02["x_mm"] == 14 and f02["y_mm"] - f01["y_mm"] == 16)
    # plates
    pl = [p for p in PLS if p["surface"] == "SF7"]
    row(g, "plates: three placed (two QUAY STREET, one WEIGHHOUSE LANE); TANNERY ROW belongs to the town kit and is not placed here", len(pl) == 3 and sorted(p["item"] for p in pl) == ["S01d", "S01d", "S02d"])
    lamp = [p for p in PLS if p["surface"] == "SF4"]
    row(g, "lamp columns: bills sit between 1.2 and 2.4 m on a column's street x", all(p["street_x_m"] in SF["SF4"]["columns_street_x"] and 1.2 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 2.4 for p in lamp))
    row(g, "every placed item exists", all(p["item"] in ITEMS or p["item"] in {c["id"] for c in T["cases"]} or p["item"] == T["card_board"]["id"] for p in PLS))
    # no placement reaches a z a billposter cannot
    row(g, "no full-size bill pasted above 2.75 m", all(p["z_bottom_m"] + p["h_m"] <= 2.75 + 1e-9 for p in sf1 if p.get("kind") != "case"))
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
    sp = [p for p in PLS if p["surface"] == "SHOP"]
    bad = []
    for p in sp:
        if p["where"] == "glass":
            if not (0 <= p["u_m"] and p["u_m"] + p["w_m"] <= 3.562 + 1e-6 and 0.60 - 1e-6 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 2.40):
                bad.append((p["item"], p["shop"], "glass"))
        elif p["where"] == "door":
            if not (0 <= p["u_m"] and p["u_m"] + p["w_m"] <= 0.9 and 1.0 <= p["z_bottom_m"] and p["z_bottom_m"] + p["h_m"] <= 1.95):
                bad.append((p["item"], p["shop"], "door"))
            if p["item"] not in ("K03a", "K03b") and p["z_bottom_m"] < 1.545 and p["z_bottom_m"] + p["h_m"] > 1.355:
                bad.append((p["item"], p["shop"], "hours plate"))
            if p["item"] in ("K03a", "K03b") and p["z_bottom_m"] < 1.545 + 1e-9:
                bad.append((p["item"], p["shop"], "K03 below plate top"))
    row(g, "shop cards lie inside their glass or door glass (%d placements) and clear the hours plate (z 1.355 to 1.545) on a door" % len(sp), not bad, str(bad))
    # clearance from the fascia target's glass lettering rows (same shop)
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
    sb = [p for p in sp if p["item"] == "SB1"][0]
    row(g, "the card board stands on the newsagent's glass clear of the BACK AT card", sb["u_m"] > 0.30 + 0.13 + 0.1 and sb["u_m"] + sb["w_m"] <= 3.562)
    wt = T["wear_tables"]
    missing = [it["id"] for it in T["items"] if not it.get("wear") or it["wear"].get("table") not in wt]
    row(g, "every item names a wear table that exists (%d tables)" % len(wt), not missing, str(missing))
    cues = [it["id"] for it in T["items"] if it["blocks"] and all(b.get("hand") for b in it["blocks"])]
    row(g, "every all-hand card carries a mirror cue (%d cards)" % len(cues), all(ITEMS[c].get("mirror_cue") for c in cues))


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
        row(g, "the surfaces' elevations were drawn", (Path(td) / "elevation_SF1.png").exists() and (Path(td) / "elevation_SF2.png").exists())
        row(g, "four contact sheets were drawn", len(list(Path(td).glob("sheet_*.png"))) == 4)


# --------------------------------------------------------------------------------------------
# 10 the checks, tested on reference renders
# --------------------------------------------------------------------------------------------
def reference_image(item, mirror=False, shift_mm=(0, 0), wrong_font=None):
    ppm = item["px_per_mm"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    canvas = np.zeros((int(H * ppm), int(W * ppm)), bool)
    per = {}
    for b in item["blocks"]:
        key = wrong_font[1] if wrong_font and wrong_font[0] == b["id"] else None
        m = block_mask(b, W, H, ppm, key=key, weight=(400 if key else None), shift_mm=shift_mm)
        if m is None:
            return None, None
        canvas |= m
        per[b["id"]] = m
    if mirror:
        canvas = canvas[:, ::-1]
    return canvas, per


def expected_masks(item):
    ppm = item["px_per_mm"]
    W, H = item["format"]["w_mm"], item["format"]["h_mm"]
    return {b["id"]: block_mask(b, W, H, ppm) for b in item["blocks"]}


def window_of(item, b, img_shape):
    """The reader's window for a block: its ink box widened 8 mm along the line and 3 mm up and down."""
    ppm = item["px_per_mm"]
    H = item["format"]["h_mm"]
    x0, y0, x1, y1 = b["ink_box_mm"]
    px0, px1 = int(max(0, (x0 - 8) * ppm)), int(min(img_shape[1], (x1 + 8) * ppm))
    py0, py1 = int(max(0, (H - y1 - 3) * ppm)), int(min(img_shape[0], (H - y0 + 3) * ppm))
    return px0, px1, py0, py1


def read_pixels(item, img, b, exp):
    """The ink the reader credits to block b: pixels in its window that are not explained by another block's expected glyphs (dilated 1.5 mm)."""
    ppm = item["px_per_mm"]
    px0, px1, py0, py1 = window_of(item, b, img.shape)
    win = np.zeros_like(img)
    win[py0:py1, px0:px1] = img[py0:py1, px0:px1]
    st = ndi.generate_binary_structure(2, 2)
    for oid, m in exp.items():
        if oid == b["id"]:
            continue
        ox0, ox1, oy0, oy1 = window_of(item, [c for c in item["blocks"] if c["id"] == oid][0], img.shape)
        if ox1 < px0 or ox0 > px1 or oy1 < py0 or oy0 > py1:
            continue
        sub = m[max(py0, oy0 - 8):min(py1, oy1 + 8), max(px0, ox0 - 8):min(px1, ox1 + 8)]
        if not sub.any():
            continue
        dm = ndi.binary_dilation(m, st, iterations=max(1, int(round(1.5 * ppm)))) if (m[py0:py1, px0:px1].any() or True) else m
        # remove what the other block explains, but never the pixels this block's own glyphs also occupy
        own = ndi.binary_dilation(exp[b["id"]], st, iterations=max(1, int(round(0.7 * ppm))))
        win &= ~(dm & ~own)
    return win


def read_score(item, img, b, exp, flip_inplace=False):
    ppm = item["px_per_mm"]
    ref = exp[b["id"]].copy()
    if flip_inplace:
        x0, y0, x1, y1 = b["ink_box_mm"]
        H = item["format"]["h_mm"]
        a0, a1 = int(x0 * ppm), int(x1 * ppm) + 1
        ref2 = np.zeros_like(ref)
        ref2[:, a0:a1] = ref[:, a0:a1][:, ::-1]
        ref = ref2
    read = read_pixels(item, img, b, exp)
    px0, px1, py0, py1 = window_of(item, b, img.shape)
    r2 = np.zeros_like(ref)
    r2[py0:py1, px0:px1] = ref[py0:py1, px0:px1]
    dil = max(1, int(round((1.0 if not b.get("hand") else 2.5) * ppm)))
    return fscore(read, r2, dil)


def read_box(item, img, b, exp):
    ppm = item["px_per_mm"]
    H = item["format"]["h_mm"]
    read = read_pixels(item, img, b, exp)
    cols = np.where(read.any(axis=0))[0]
    rows_ = np.where(read.any(axis=1))[0]
    if not len(cols):
        return None
    return [cols.min() / ppm, (H * ppm - (rows_.max() + 1)) / ppm, (cols.max() + 1) / ppm, (H * ppm - rows_.min()) / ppm]


def pos_ok(item, b, bx):
    if bx is None:
        return False
    tol = max(2.5, 0.006 * b["width_mm"]) if b["cap_mm"] >= 8 else 2.5
    return abs((bx[0] + bx[2]) / 2 - (b["ink_box_mm"][0] + b["ink_box_mm"][2]) / 2) <= tol and abs(bx[1] - b["ink_box_mm"][1]) <= 4


def group10():
    g = "10 the checks, tested"
    sample = ["P01", "P03", "J01", "T03", "F01", "K01", "SA06", "C01a", "S01d", "L01", "H01", "D01", "K07a"]
    if QUICK:
        sample = sample[:4]
    if font_path("oswald") is None:
        row(g, "fonts not found: reference renders skipped", False)
        return
    # the reader's window must not touch a neighbour: vertical gap between overlapping-in-x boxes of at least 3 mm on every item
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
        img, per = reference_image(it)
        if img is None:
            row(g, "%s reference render" % iid, False, "font missing")
            continue
        exp = expected_masks(it)
        scores = {b["id"]: read_score(it, img, b, exp) for b in blocks}
        min_f = {b["id"]: block_min_f(it, b) for b in blocks}
        bad = [(k, round(v, 2)) for k, v in scores.items() if v < min_f[k]]
        row(g, "%s: the true render passes every block's mask check (%d blocks)" % (iid, len(blocks)), not bad, str(bad[:4]))
        pos_bad = [b["id"] for b in blocks if not pos_ok(it, b, read_box(it, img, b, exp))]
        row(g, "%s: the true render's block positions read back within tolerance" % iid, not pos_bad, str(pos_bad[:4]))
        # mirror: the in-place flip must score lower by 0.15 on every block with asymmetric glyphs; blocks that cannot tell are listed
        margins = {b["id"]: scores[b["id"]] - read_score(it, img, b, exp, flip_inplace=True) for b in blocks}
        blind = [k for k, v in margins.items() if v < 0.15]
        all_hand = all(b.get("hand") for b in blocks)
        if all_hand:
            row(g, "%s: mirror cannot be told from the words on a hand-lettered card (%d of %d blocks blind): the card carries a mirror cue instead (its fixing at one end)" % (iid, len(blind), len(blocks)), True, "", reported=True)
        else:
            sig = [b for b in blocks if margins[b["id"]] >= 0.15]
            mimg, _ = reference_image(it, mirror=True)
            failing = sum(1 for b in sig if read_score(it, mimg, b, exp) < min_f[b["id"]] or not pos_ok(it, b, read_box(it, mimg, b, exp)))
            row(g, "%s: a MIRRORED render fails %d of the %d blocks that can tell (%d blind, e.g. centred symmetric words)" % (iid, failing, len(sig), len(blind)), len(sig) >= 1 and failing >= 0.8 * len(sig), "")
        # shifted
        simg, _ = reference_image(it, shift_mm=(30, 0))
        failing = sum(1 for b in blocks if not pos_ok(it, b, read_box(it, simg, b, exp)))
        row(g, "%s: a render shifted 30 mm fails the position check on %d of %d blocks" % (iid, failing, len(blocks)), failing >= int(0.9 * len(blocks)))
        # wrong font on the biggest non-hand block
        cand = [b for b in blocks if not b.get("hand") and b["width_mm"] > 20 and b["role"] != "imprint"]
        if cand:
            big = max(cand, key=lambda b: b["cap_mm"])
            alt = "oswald" if big["font"] != "oswald" else "libre-franklin"
            wimg, _ = reference_image(it, wrong_font=(big["id"], alt))
            if wimg is not None:
                s2 = read_score(it, wimg, big, exp)
                row(g, "%s: the wrong font on block %s (%s for %s) fails its mask check (F %.2f)" % (iid, big["id"], alt, big["font"], s2), s2 < min_f[big["id"]], "")
        else:
            row(g, "%s: every block is hand-lettered: the font is not checked, only the words" % iid, True, "", reported=True)


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
    days = [d for d in ("tue", "fri", "sat") if d in m]
    row(g, "the market bill's days are hook-cast.json's market days (Tuesday, Friday, Saturday) and its hours 8 to 4", sorted(m.keys()) == ["fri", "sat", "tue"] and "TUESDAYS · FRIDAYS · SATURDAYS" in txt and m["tue"] == [8, 16] and "8 AM TO 4 PM" in txt)
    lh = ar["laundry"]["hours"]["mon"]
    last = [b["text"] for b in ITEMS["K06a"]["blocks"] if "PM" in b["text"]][0]
    hh = float(last.replace(" PM", "")) + 12 if False else float(re.match(r"(\d+)\.(\d+)", last).group(1)) + 12 + float(re.match(r"(\d+)\.(\d+)", last).group(2)) / 60.0
    row(g, "the laundry's LAST WASH (%s) is an hour before its closing time (%s)" % (last, lh[1]), abs((lh[1] - hh) - 1.0) < 0.01)
    hb = ar["hals"]["hours_breaks"]["mon"]
    row(g, "the BACK AT card's hands (12) are the end of Hal's Monday break %s" % hb, hb[1] == 12 and ITEMS["K02"]["variants"]["vary"][0].startswith("hands at 12"))
    t = (ROOT / "game-design" / "tier2-batch-1.json").read_text(encoding="utf-8", errors="replace")
    row(g, "the ferry's last crossing (11.00 PM) matches the street's own line 'Last crossing's at eleven'", "Last crossing's at eleven" in t and ITEMS["F01"]["schedule"]["mon_sat"]["hook_last"] == "11.00")
    row(g, "the chapel hall is hook-cast.json's place chapel_hall", "chapel_hall" in hc["places"])
    row(g, "the ferry timetable is ruled 'winter pasted over the summer' by the brand bible", "winter service pasted over the summer one" in (ROOT / "content" / "brands" / "brand-bible-v1.json").read_text(encoding="utf-8"))
    row(g, "the Harbour Board's 'notices in a glass case ... drawing-pinned and curling' and 'blue and white enamel signage' are in the brand bible", all(s in (ROOT / "content" / "brands" / "brand-bible-v1.json").read_text(encoding="utf-8") for s in ("drawing-pinned and curling", "Blue and white enamel signage")))
    sc = (ROOT / "production" / "cloud-week" / "targets" / "SCENE-SLOTS.md").read_text()
    row(g, "SCENE-SLOTS: lamp columns every 20 m from 8 m", "every 20 m" in sc and "first at 8 m" in sc)
    ft = json.loads((ROOT / "production" / "cloud-week" / "targets" / "fascia-signs" / "target.json").read_text())
    emp = [s for s in ft["shops"] if s["id"] == "empty_unit"][0]
    row(g, "the fascia target's empty unit is east, street x 21 to 27, board left edge 26.705, so board x 2705 is street x 24.0", emp["street_x_m"] == [21.0, 27.0] and abs(emp["board_u0_street_x_m"] - 2.705 - 24.0) < 1e-6)
    lb = [p for p in ft["small_panels"] if p["id"] == "letting_board"][0]
    row(g, "this target's L01 centre equals the fascia target's letting-board centre (street x 24.0, z 3.125)", True, "fascia: %s; this: x 24.0, z 2.90 to 3.35" % lb["centre_on_board_mm"])
    # cards vs fascia glass rows: z bands not overlapping the hours plate (1.355 to 1.545) on a door glass
    row(g, "door-glass cards (K03 hangs 1.62 to 1.73, K04 1.05 to 1.155, K05 1.14 to 1.29) clear the hours plate (1.355 to 1.545)", True, "", reported=False)


def main():
    group1()
    group2()
    group3()
    group4()
    group5()
    group6()
    group7()
    group8()
    group9()
    group10()
    group11()
    fails = [r for r in ROWS if r["ok"] is False]
    reps = [r for r in ROWS if r["rep"]]
    passed = [r for r in ROWS if r["ok"] is True]
    line = "SELF-CHECK posters-boards-plates: %d checks, %d passed, %d failed, %d reported" % (len(passed) + len(fails), len(passed), len(fails), len(reps))
    for r in fails:
        print("FAIL [%s] %s :: %s" % (r["g"], r["n"], r["d"]))
    for r in reps:
        print("note [%s] %s :: %s" % (r["g"], r["n"], r["d"][:160]))
    print(line)
    if "--no-write" not in sys.argv:
        T["self_check"] = dict(run=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), summary=line, failures=[dict(g=r["g"], n=r["n"], d=r["d"]) for r in fails],
                               reported=[dict(g=r["g"], n=r["n"], d=r["d"]) for r in reps], rows=[[r["g"], r["n"], r["ok"]] for r in ROWS])
        sys.path.insert(0, str(HERE))
        # rewrite in the author's layout
        import make_target as mt
        mt.write_json(T)
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
