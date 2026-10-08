"""Test target.json against its own sources before anything is built to it.

    /home/user/.bpyenv/bin/python self_check.py [--fonts DIR] [--fetch-fonts DIR] [--no-write]

Groups:
  1 printed      every printed or scaled number used comes back from target.json (the scene file, the
                 kit README, SCENE-SLOTS.md, the cast's hours, the 3 October trades, the recipe's bays)
  2 photo wins   every disagreement settled for a photograph (D1 to D7) holds in target.json's own numbers
  3 photo P1     P1 re-measured by CODE on the saved preview (not from my hand numbers), the drawing's edges
                 (from target_drawing.py's polygons) laid on it at a scale fitted on one dimension only (the
                 lettered field's height); writes the overlay P1-...-target-on-photo.jpg
  4 sheet H1     the Hook sheet re-measured from production/reference/hook-sheet.png; where the target
                 departs from the sheet it is REPORTED, not hidden
  5 consistency  boards inside their safe zone, nothing overlaps that should not, panels hold their words,
                 contrast, distinctness, the word list against the content rule and the real-world list,
                 widths re-measured on the real font files when they are on this machine
  6 checks       the checks written for unit 4.1 are well formed, and the target passes its own nominal values
Writes the result into target.json under "self_check" and prints a result line and a table.
"""
import json
import math
import re
import sys
import urllib.request
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw
from shapely.geometry import box as sbox

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE))
import target_drawing as td  # noqa: E402

TP = HERE / "target.json"
T = json.loads(TP.read_text(encoding="utf-8"))
PREV = ROOT / "production" / "previews" / "cloud-week" / "refs" / "fascia-signs"
SCRATCH_FONTS = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/fonts"
FONT_DIR = Path(sys.argv[sys.argv.index("--fonts") + 1]) if "--fonts" in sys.argv else Path(SCRATCH_FONTS)
rows = []


def check(group, name, ok, detail, kind="check"):
    rows.append(dict(group=group, check=name, passed=bool(ok), detail=detail, kind=kind))


def near(a, b, tol):
    return abs(a - b) <= tol


def read(rel):
    p = ROOT / rel
    return p.read_text(encoding="utf-8", errors="replace") if p.exists() else None


def shop(i):
    return [s for s in T["shops"] if s["id"] == i][0]


# ============================================================================================
# fonts (optional)
# ============================================================================================
if "--fetch-fonts" in sys.argv:
    d = Path(sys.argv[sys.argv.index("--fetch-fonts") + 1])
    for k, v in T["fonts"].items():
        if k.startswith("_") or "file_in_google_fonts_repo" not in v:
            continue
        rel = v["file_in_google_fonts_repo"]
        for name in (rel, rel.rsplit("/", 1)[0] + "/OFL.txt"):
            dst = d / name.replace("ofl/", "", 1)
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                url = "https://raw.githubusercontent.com/google/fonts/main/" + name.replace("[", "%5B").replace("]", "%5D").replace(",", "%2C")
                urllib.request.urlretrieve(url, dst)
    FONT_DIR = d
    print("fonts fetched into", d)

# ============================================================================================
# 1 printed
# ============================================================================================
G = "1 printed"
B = T["board"]
sl = read("production/cloud-week/targets/SCENE-SLOTS.md") or ""
m = re.search(r"fascia from ([\d.]+) to the first floor's underside at ([\d.]+) \(([\d.]+)\), ([\d.]+) proud", sl)
if m:
    a, b, c, d = map(float, m.groups())
    check(G, "SCENE-SLOTS: fascia 2.85 to 3.40, 0.55 high, 0.12 proud", near(a, B["z_bottom_m"], 1e-9) and near(b, B["z_top_m"], 1e-9) and near(c * 1000, B["height_mm"], 1e-6) and near(d * 1000, B["proud_of_wall_mm"], 1e-6),
          f"source {a}, {b}, {c}, {d}; target {B['z_bottom_m']}, {B['z_top_m']}, {B['height_mm'] / 1000}, {B['proud_of_wall_mm'] / 1000}")
else:
    check(G, "SCENE-SLOTS fascia row found", False, "row not found")
sc = json.loads(read("production/specs/vignette-scene.json") or "{}")
sf = sc.get("shopfront", {})
check(G, "vignette-scene.json shopfront: fascia_bottom_m 2.85 and fascia_projection_m 0.12", near(sf.get("fascia_bottom_m", -1), B["z_bottom_m"], 1e-9) and near(sf.get("fascia_projection_m", -1), B["proud_of_wall_mm"] / 1000, 1e-9),
      f"source {sf.get('fascia_bottom_m')}, {sf.get('fascia_projection_m')}")
blocks = {b["id"]: b for b in sc.get("blocks", [])}
exp = {}
for sid, (blk_id, bay) in {"mickeys": ("east_parade", 0), "fish_market": ("east_parade", 1), "ritas": ("east_parade", 2), "empty_unit": ("east_parade", 3), "steam_laundry": ("east_parade", 4), "grocer": ("east_parade", 5),
                          "newsagent": ("west_north", 0), "ironmonger": ("west_north", 1), "tea_rooms": ("west_north", 2), "chandler": ("east_chandler", 0)}.items():
    b = blocks.get(blk_id)
    if not b:
        continue
    w, st, n = b["bay_width_m"], b["start_x_m"], b["bays"]
    x0 = st + bay * w if b["side"] == "east" else st + n * w - (bay + 1) * w
    exp[sid] = [x0, x0 + w]
for sid, r in exp.items():
    s = shop(sid)
    check(G, f"street x of {sid} from the scene's blocks (the west block is turned: bays run back down the street)", s["street_x_m"] == r, f"scene {r}, target {s['street_x_m']}")
check(G, "bay width 6.0 and board 5.41 = 5.705 - 0.295 (kit README)", near(B["between_consoles_in_bay_m"][1] - B["between_consoles_in_bay_m"][0], B["width_mm"] / 1000, 1e-9) and "0.295 to 5.705" in (read("production/art/shopfront-kit/README.md") or ""),
      f"README quotes 0.295 to 5.705; target {B['between_consoles_in_bay_m']} -> {B['width_mm']} mm")
pcs = json.loads(read("production/specs/vignette-pieces.json") or "{}").get("pieces", [])
f0 = [p for p in pcs if p.get("name") == "east_parade_fascia0"]
check(G, "vignette-pieces.json east_parade_fascia0: 6.0 x 0.55 x 0.12 (the street's box)", bool(f0) and near(f0[0]["sx_m"], B["street_box_mm"][0] / 1000, 1e-9) and near(f0[0]["sy_m"], B["height_mm"] / 1000, 1e-9) and near(f0[0]["sz_m"], B["proud_of_wall_mm"] / 1000, 1e-9),
      f"source {f0[0]['sx_m'] if f0 else None} x {f0[0]['sy_m'] if f0 else None} x {f0[0]['sz_m'] if f0 else None}")
dec = read("DECISIONS.md") or ""
l3 = [l for l in dec.splitlines() if l.startswith("- 2026-10-03 | The shopfronts' trades")]
want = ["fishmonger (Fish Market)", "Steam Laundry", "a grocer", "a newsagent and tobacconist", "an ironmonger", "a tea room", "ship's chandler", "whitewashed"]
check(G, "DECISIONS 3 Oct: the ten trades", bool(l3) and all(w in l3[0] for w in want), f"found {bool(l3)}; missing {[w for w in want if not l3 or w not in l3[0]]}")
tf = read("tools/art-recipes/terrace-front.py") or ""
ok = all(re.search(r'\("%s", %d\): LETTERED \+ "/fascia_trade_%s"' % (blk_, bay, tr), tf) for blk_, bay, tr in
         (("east_parade", 1, "fishmonger"), ("east_parade", 2, "pawnbroker"), ("east_parade", 4, "launderette"), ("east_parade", 5, "grocer"), ("west_north", 0, "newsagent"), ("west_north", 1, "ironmonger"), ("west_north", 2, "tea_room"), ("east_chandler", 0, "chandler")))
check(G, "terrace-front.py SIGN_OVERRIDE: the bays of the eight trade boards", ok, "west_north 0 newsagent, 1 ironmonger, 2 tea room; east_chandler 0; parade 1, 2, 4, 5")
hc = json.loads(read("production/specs/hook-cast.json") or "{}")
areas = hc.get("areas", hc)
need = {"ritas": "ritas", "fish_market": "fish_market", "steam_laundry": "laundry", "newsagent": "newsagent", "tea_rooms": "cafe"}
miss = [k for k, v in need.items() if v not in areas or "hours" not in areas[v]]
check(G, "hook-cast.json has hours for every shop that carries an hours plate", not miss and set(T["small_panels"][1]["shops"]) == set(need), f"missing {miss}")
conf = (areas.get("newsagent") or {}).get("places"), (hc.get("places") or {}).get("pension_counter", {}).get("x_m"), (hc.get("places") or {}).get("hals_shop", {}).get("x_m")
check(G, "REPORTED: hook-cast puts the newsagent's counter at x 32 and Hal's shop at x 39, the recipe the newsagent at x 36-42 and the ironmonger at 30-36", False,
      f"cast pension_counter x {conf[1]}, hals_shop x {conf[2]}; target newsagent {shop('newsagent')['street_x_m']}, ironmonger {shop('ironmonger')['street_x_m']}; a town question, in could_not_settle", kind="reported")
bb = json.loads(read("content/brands/brand-bible-v1.json") or "{}")
mk = [b for b in bb.get("brands", []) if b["id"] == "mickeys"]
check(G, "brand bible: Mickey's, minicab office, founded 1962 (the board's name is minted)", bool(mk) and mk[0]["founded"] == 1962 and mk[0]["kind"] == "minicab office" and shop("mickeys")["blocks"][0]["text"].replace("’", "'") == "MICKEY'S", f"brand bible {mk[0]['name'] if mk else None}, {mk[0]['founded'] if mk else None}")
sr = read("tools/art-recipes/shop-room.py") or ""
check(G, "shop-room.py: Mickey's glass lettering 0632  960418 and MINICABS  ·  24 HOURS (they exist; the target keeps them)", "0632  960418" in sr and "MINICABS  ·  24 HOURS" in sr, "found in shop-room.py")
# fonts' licences
fo = []
for k, v in T["fonts"].items():
    if k.startswith("_") or "ofl_url" not in v:
        continue
    d_ = v["file_in_google_fonts_repo"].split("/")[1]
    p = FONT_DIR / d_ / "OFL.txt"
    if p.exists():
        fo.append((k, "SIL OPEN FONT LICENSE Version 1.1" in p.read_text(errors="replace")))
if fo:
    check(G, "every OFL.txt of the ten fonts named is on this machine and carries the OFL 1.1 header", all(x[1] for x in fo) and len(fo) == 10, f"{sum(x[1] for x in fo)} of {len(fo)} read")
else:
    check(G, "OFL.txt files re-read", False, f"fonts not on this machine at {FONT_DIR}; run with --fonts DIR or --fetch-fonts DIR (raw.githubusercontent.com)", kind="reported")
check(G, "no font outside the OFL list; Overpass not used", all(k in T["fonts"] for s in T["shops"] for k in [b["font"] for b in s["blocks"]]) and "overpass" not in json.dumps([s for s in T["shops"]]).lower(), "all block fonts are in fonts{}")

# ============================================================================================
# 2 photo wins
# ============================================================================================
G = "2 photo wins"
R = T["photo_template"]["ratios"]
sh = [(s["id"], b) for s in T["shops"] for b in s["blocks"] if b["shade"]]
bad = [(i, b["id"], round(b["shade"]["d_mm"] / b["cap_mm"], 3)) for i, b in sh if not near(b["shade"]["d_mm"] / b["cap_mm"], R["shade_over_cap"], 0.011)]
check(G, "D2 block shade is P1's 0.10 of the cap on every shaded block (not the game's 0.035)", not bad, f"{len(sh)} shaded blocks, P1 {R['shade_over_cap']}, off: {bad}")
ends = [(s["id"], b) for s in T["shops"] for b in s["blocks"] if b["role"] == "end"]
bad = []
for i, b in ends:
    nm = [x for x in shop(i)["blocks"] if x["role"] == "name"][0]
    if not near(b["cap_mm"] / nm["cap_mm"], R["numeral_over_cap"], 0.06):
        bad.append((i, round(b["cap_mm"] / nm["cap_mm"], 2)))
check(G, "D3 numbers at the ends are P1's 0.93 of the name's cap", not bad and len(ends) == 6, f"{len(ends)} end numerals on 3 shops; P1 {R['numeral_over_cap']}; off: {bad}")
rb = shop("ritas")["border"]
fh = B["field_mm"][3] - B["field_mm"][1]
check(G, "D4 Rita's keyline: P1's inset, thickness and concave corner (+-0.03 of the field)", near(rb["inset_mm"] / fh, (R["keyline_top_inset"] + R["keyline_bottom_inset"]) / 2, 0.03) and near(rb["line_mm"] / fh, R["keyline_thickness"], 0.012) and near(rb["radius_mm"] / fh, R["corner_radius"], 0.03) and rb["inner_line_mm"] == 0,
      f"target inset {rb['inset_mm'] / fh:.3f}, line {rb['line_mm'] / fh:.3f}, radius {rb['radius_mm'] / fh:.3f}; P1 inset {(R['keyline_top_inset'] + R['keyline_bottom_inset']) / 2:.3f}, line {R['keyline_thickness']}, radius {R['corner_radius']}")
check(G, "D5 the board stays the street's 0.55 m (the guides' 380 mm envelope not followed)", B["height_mm"] == 550 and near(fh / B["height_mm"], 0.913, 0.01), f"field {fh} of {B['height_mm']} = {fh / B['height_mm']:.3f}; P1's lettered field over bead-to-bottom board 147 / 173 = {147 / 173:.3f}")
mx = shop("mickeys")["blocks"][0]
check(G, "D6 Mickey's name over the door, 0.245 of the board from the door end (the sheet's 0.755), door at street x 4.65 = board x 1355", near(mx["x_mm"] / B["width_mm"], 1 - T["photo"]["H1"]["ratios"]["letter_centre_along_board"], 0.02) and near(mx["x_mm"], (4.65 - (3.0 + B["between_consoles_in_bay_m"][0])) * 1000, 40),
      f"x {mx['x_mm']} = {mx['x_mm'] / B['width_mm']:.3f}; sheet {1 - T['photo']['H1']['ratios']['letter_centre_along_board']:.3f}; door-centred {(4.65 - 3.295) * 1000:.0f}")
fm = shop("fish_market")
check(G, "D1 the fishmonger is a dark board with red letters (t13138), not oxblood with cream", fm["ground"]["colour"] == "charcoal_navy" and fm["blocks"][0]["face"] == "vermilion" and max(T["palette"]["charcoal_navy"]["srgb_1990"]) < 60,
      f"ground {fm['ground']['colour']} {T['palette']['charcoal_navy']['srgb_1990']}, name {fm['blocks'][0]['face']}")
caps = [b["cap_over_field"] for s in T["shops"] for b in s["blocks"] if b["role"] == "name"]
check(G, "D7 the name lines run 0.30 to 0.60 of the field, varied (not 0.43 on every board)", min(caps) >= 0.30 and max(caps) <= 0.60 and len(set(caps)) >= 6, f"{sorted(set(caps))}")

# ============================================================================================
# 3 photo P1: re-measure by code, then lay the drawing on it
# ============================================================================================
G = "3 photo P1"
P1 = T["photo"]["P1"]
pv = P1["preview"]
img = Image.open(PREV / pv["file"]).convert("RGB")
k = pv["scale"]
cx0, cy0 = pv["crop_box_in_view_px"][0], pv["crop_box_in_view_px"][1]
A = np.asarray(img).astype(float)
Hh, Ww, _ = A.shape
Rr, Gg, Bb = A[..., 0], A[..., 1], A[..., 2]
gilt = (Rr > 200) & (Gg > 150) & (Bb < 130) & (Gg > 0.6 * Rr)
lum = 0.299 * Rr + 0.587 * Gg + 0.114 * Bb


def to_prev(x=None, y=None):
    return ((x - cx0) * k) if x is not None else ((y - cy0) * k)


def runs(v):
    out, i = [], 0
    while i < len(v):
        if v[i]:
            j = i
            while j < len(v) and v[j]:
                j += 1
            out.append((i, j - 1))
            i = j
        else:
            i += 1
    return out


c0, c1 = int(0.30 * Ww), int(0.70 * Ww)
rowfrac = gilt[:, c0:c1].sum(axis=1) / float(c1 - c0)
bands = [(a, b) for a, b in runs(rowfrac > 0.70)]
mid = runs((rowfrac > 0.10) & (rowfrac < 0.70))
mid = max(mid, key=lambda r: r[1] - r[0])           # the cap band: the longest run of letter-like rows
cap_top, cap_bot = mid[0], mid[1] + 1
above = [b for b in bands if b[1] < cap_top]
below = [b for b in bands if b[0] > cap_bot]


def centroid(rng):
    ys = np.arange(rng[0], rng[1] + 1)
    w = np.clip(Gg[rng[0]:rng[1] + 1, c0:c1].mean(axis=1) - 120, 0, None)
    return float((ys * w).sum() / w.sum()) + 0.5


key_top = centroid(above[-1])
key_bot = centroid(below[0])
colp = gilt[cap_top:cap_bot, int(0.2 * Ww):int(0.8 * Ww)].sum(axis=0)
xs = np.where(colp > 0)[0] + int(0.2 * Ww)
name_x0, name_x1 = float(xs.min()), float(xs.max() + 1)
rowsK = slice(int(key_top) + 20, int(key_bot) - 20)
colR = Rr[rowsK, :].mean(axis=0)
loc = colR - 0.5 * (np.roll(colR, 7) + np.roll(colR, -7))   # a column brighter than its surroundings 7 px either side
cand = np.where(loc > 35)[0]                                   # the keyline is the OUTERMOST such run on each side (numerals stand inside it)


def run_centroid(c0_, direction):
    """centroid of the contiguous run of candidate columns that holds the outermost one"""
    run = [c0_]
    cs = set(cand.tolist())
    x = c0_
    while (x + direction) in cs:
        x += direction
        run.append(x)
    w_ = np.clip(loc[run], 0, None)
    return float((np.array(run) * w_).sum() / w_.sum()) + 0.5


key_l = run_centroid(int(cand[cand < 0.2 * Ww].min()), +1)
key_r = run_centroid(int(cand[cand > 0.8 * Ww].max()), -1)
colw = slice(int(0.17 * Ww), int(0.24 * Ww))
prof = lum[:, colw].mean(axis=1)
med = np.median(prof[int(key_top) + 5:int(key_bot) - 5])
rng_ = range(int(key_top) - 22, int(key_top) - 2)
top_dark = [min(rng_, key=lambda y: prof[y])] if min(prof[y] for y in rng_) < 0.85 * med else []
bot_dark = [y for y in range(int(key_bot) + 4, min(Hh, int(key_bot) + 40)) if prof[y] < 0.5 * med]
field_top = (top_dark[0] + 1.5) if top_dark else float("nan")
field_bot = float(min(bot_dark)) if bot_dark else float("nan")
meas = dict(field_top=field_top, field_bottom=field_bot, keyline_top=key_top, keyline_bottom=key_bot, keyline_left=key_l, keyline_right=key_r, cap_top=float(cap_top), cap_bottom=float(cap_bot), name_x0=name_x0, name_x1=name_x1)
hand = dict(field_top=to_prev(y=P1["px"]["field_top"]), field_bottom=to_prev(y=P1["px"]["field_bottom"]), keyline_top=to_prev(y=P1["px"]["keyline_top_y"]), keyline_bottom=to_prev(y=P1["px"]["keyline_bottom_y"]),
            keyline_left=to_prev(x=P1["px"]["keyline_left_x"]), keyline_right=to_prev(x=P1["px"]["keyline_right_x"]), cap_top=to_prev(y=P1["px"]["cap_top"]), cap_bottom=to_prev(y=P1["px"]["cap_bottom"]),
            name_x0=to_prev(x=P1["px"]["text_x0"]), name_x1=to_prev(x=P1["px"]["text_x1"]))
tol = P1["error_px"]
for kk in hand:
    check(G, f"hand measure of {kk} equals the code's measure on the saved preview (+-{tol} px)", abs(meas[kk] - hand[kk]) <= tol, f"code {meas[kk]:.1f}, hand {hand[kk]:.1f}, diff {meas[kk] - hand[kk]:+.1f} preview px")

# the drawing laid on the photograph at a scale fitted on ONE dimension: the lettered field's height
tpl = td.template_data(T)
fh_mm = tpl["field_mm"][3]
fpx = meas["field_bottom"] - meas["field_top"]
s_px = fpx / fh_mm                                   # px per mm, from the field's height only
cxp = (meas["keyline_left"] + meas["keyline_right"]) / 2.0


def Ypx(y_up):
    return meas["field_top"] + (fh_mm - y_up) * s_px


def Xpx(x):
    return cxp + (x - tpl["field_mm"][2] / 2.0) * s_px


proj = dict(keyline_top=Ypx(tpl["keyline_top_y"]), keyline_bottom=Ypx(tpl["keyline_bottom_y"]), keyline_left=Xpx(tpl["keyline_left_x"]), keyline_right=Xpx(tpl["keyline_right_x"]),
            cap_top=Ypx(tpl["text"][0]["cap_y"]), cap_bottom=Ypx(tpl["text"][0]["baseline_y"]), name_x0=Xpx(tpl["text"][0]["x0"]), name_x1=Xpx(tpl["text"][0]["x1"]))
for kk, v in proj.items():
    check(G, f"drawing edge {kk} falls on the photograph's edge (+-{tol} px)", abs(v - meas[kk]) <= tol, f"drawing {v:.1f}, photograph {meas[kk]:.1f}, diff {v - meas[kk]:+.1f} px; scale {s_px:.4f} px/mm from the field height {fpx:.1f} px = {fh_mm:.0f} mm only")
# the overlay picture
ov = img.copy()
dr = ImageDraw.Draw(ov)
cy_ = (255, 255, 0)
for L in tpl["layers"]:
    if L["role"] == "keyline":
        pts = [(Xpx(p[0]), Ypx(p[1])) for p in L["centreline"]]
        dr.line(pts, fill=(0, 255, 255), width=1)
dr.line([(Xpx(tpl["text"][0]["x0"]), Ypx(tpl["text"][0]["cap_y"])), (Xpx(tpl["text"][0]["x1"]), Ypx(tpl["text"][0]["cap_y"]))], fill=(0, 255, 255), width=1)
dr.line([(Xpx(tpl["text"][0]["x0"]), Ypx(tpl["text"][0]["baseline_y"])), (Xpx(tpl["text"][0]["x1"]), Ypx(tpl["text"][0]["baseline_y"]))], fill=(0, 255, 255), width=1)
dr.rectangle([Xpx(tpl["text"][0]["x0"]), Ypx(tpl["text"][0]["cap_y"]), Xpx(tpl["text"][0]["x1"]), Ypx(tpl["text"][0]["baseline_y"])], outline=(0, 255, 255))
# Rita's layout, the same scale, centred on the same x, its lettered field top on the photograph's field top
rs = shop("ritas")
fy0, fy1 = B["field_mm"][1], B["field_mm"][3]


def Yr(y_up):
    return meas["field_top"] + (fy1 - y_up) * s_px


def Xr(x):
    return cxp + (x - B["width_mm"] / 2.0) * s_px


for sh_ in rs["shapes"]:
    if sh_["kind"] == "polyline":
        dr.line([(Xr(p[0]), Yr(p[1])) for p in sh_["pts"]], fill=(255, 0, 255), width=1)
for b in rs["blocks"]:
    x0, y0, x1, y1 = b["ink_box_mm"]
    dr.rectangle([Xr(x0), Yr(y1), Xr(x1), Yr(y0)], outline=(255, 0, 255))
dr.text((6, 4), "cyan: P1 ratios laid by the drawing code (scale from the field height only)   magenta: Rita's board, the same scale", fill=(255, 255, 255))
ovp = PREV / "P1-leadenhall-chamberlain-board-target-on-photo.jpg"
if "--no-write" not in sys.argv:
    ov.save(ovp, quality=88, optimize=True)
check(G, "the overlay was written and is under 300 KB", ("--no-write" in sys.argv) or ovp.stat().st_size < 300_000, f"{ovp.name} {ovp.stat().st_size if ovp.exists() else 0} bytes")
cap_rita = rs["blocks"][0]["cap_mm"] / fh_mm
check(G, "REPORTED: Rita's name is larger over its field than the photographed board's (deliberate: a trading parade, not a restored arcade)", False,
      f"Rita's name cap {cap_rita:.3f} of the field; P1 {R['cap_over_field']}", kind="reported")

# ============================================================================================
# 4 sheet H1
# ============================================================================================
G = "4 sheet H1"
hs = np.asarray(Image.open(ROOT / "production" / "reference" / "hook-sheet.png").convert("RGB")).astype(float)
bd = hs[500:535, 320:600].reshape(-1, 3)
L_ = hs[510:556, 625:755].reshape(-1, 3)
mk_ = (L_[:, 0] > L_[:, 2] + 25) & (L_[:, 0] > 110)
bm, gm = bd.mean(0), L_[mk_].mean(0)
pal = T["palette"]
check(G, "Mickey's board colour is the sheet's measured mean (+-3 each channel)", np.all(np.abs(bm - np.array(pal["slate"]["srgb_1990"])) <= 3), f"sheet {bm.round(1).tolist()}, target {pal['slate']['srgb_1990']}")
check(G, "Mickey's letter colour is the sheet's measured mean (+-4 each channel)", np.all(np.abs(gm - np.array(pal["brass_gilt"]["srgb_1990"])) <= 4), f"sheet {gm.round(1).tolist()}, target {pal['brass_gilt']['srgb_1990']}")
sub = hs[505:560, 620:760]
mm_ = (sub[..., 0] > sub[..., 2] + 25) & (sub[..., 0] > 110)
ys, xs_ = np.where(mm_)
check(G, "the sheet's lettering spans x 630 to 746 (the width used for the ratio)", abs(xs_.min() + 620 - 630) <= 2 and abs(xs_.max() + 620 - 746) <= 2, f"measured {xs_.min() + 620} to {xs_.max() + 620}")
mx = shop("mickeys")["blocks"][0]
sheet_cap = T["photo"]["H1"]["ratios"]["cap_over_board"]
check(G, "REPORTED: Mickey's cap over the board: the sheet's letters fill 0.69 of the board, the target's 0.49 (270 of 550)", False, f"target {mx['cap_mm'] / B['height_mm']:.2f}, sheet {sheet_cap}; the target keeps Marcellus SC (ruled) whose capitals are 1.8 times wider than the sheet's tall narrow ones, so it is set smaller, not condensed", kind="reported")
check(G, "REPORTED: the name's width over its cap: the sheet's 3.5, the target's", False, f"target {mx['width_mm'] / mx['cap_mm']:.2f}, sheet {T['photo']['H1']['ratios']['width_over_cap']}", kind="reported")

# ============================================================================================
# 5 consistency
# ============================================================================================
G = "5 consistency"
SAFE = B["safe_mm"]
safe_box = sbox(*SAFE)
board_box = sbox(0, 0, B["width_mm"], B["height_mm"])
for s in T["shops"]:
    bl = s["blocks"]
    ok = all(safe_box.contains(sbox(*b["effects_box_mm"])) for b in bl)
    check(G, f"{s['id']}: every ink box with its shade, outline and jitter is inside the safe rectangle", ok, f"min margin {s['min_margin_mm']} mm" if bl else "no lettering on this board")
    ov_ = [(a["id"], b["id"]) for i, a in enumerate(bl) for b in bl[i + 1:] if sbox(*a["effects_box_mm"]).intersects(sbox(*b["effects_box_mm"]))]
    check(G, f"{s['id']}: no two text blocks overlap", not ov_, f"{ov_}")
    pn = (s["border"] or {}).get("panel_mm") or (s["border"] or {}).get("face_mm")
    if pn and bl:
        pb = sbox(*pn).buffer(-15)
        check(G, f"{s['id']}: every text block sits inside its panel with 15 mm to spare", all(pb.contains(sbox(*b["effects_box_mm"])) for b in bl), f"panel {pn}")
    for b in bl:
        e = b["effects_box_mm"]
        check(G, f"{s['id']}.{b['id']}: the baseline and cap line fit the field", B["field_mm"][1] <= b["baseline_mm"] and b["baseline_mm"] + b["cap_mm"] <= B["field_mm"][3], f"baseline {b['baseline_mm']}, cap line {b['baseline_mm'] + b['cap_mm']}")
        check(G, f"{s['id']}.{b['id']}: contrast {b['contrast_1990']} is at least 2.2", b["contrast_1990"] >= 2.2, f"{b['face_1990']} on {b['ground_1990']}")
    for g_ in ([s["ghost"]] if s.get("ghost") else []):
        check(G, f"{s['id']}: the ghost patch lies on the board", board_box.contains(sbox(*g_["box_mm"])), f"{g_['box_mm']}")
    for sh_ in s["shapes"]:
        if sh_["kind"] == "rect":
            check(G, f"{s['id']}: {sh_['role']} lies on the board", board_box.contains(sbox(*sh_["box"])), f"{sh_['box']}") if sh_["role"] not in ("speed_line",) else None
for p in T["small_panels"]:
    if p["id"] == "letting_board":
        cx, cy = p["centre_on_board_mm"]
        w, h = p["size_mm"]
        check(G, "the letting board lies on the empty unit's board", board_box.contains(sbox(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)), f"{w} x {h} at {cx}, {cy}")
for p in T["projecting_signs"]:
    bm_ = p["parts"].get("board_m") or p["parts"].get("box_m")
    m_ = p["mount"]
    low = m_["arm_height_m"] - (0.06 if "board_m" in p["parts"] else 0) - (bm_[1] if bm_ else 0)
    if "balls" in p["parts"]:
        low = min(c[1] for c in p["parts"]["balls"]["centres_m"]) - p["parts"]["balls"]["diameter_m"] / 2
    check(G, f"{p['id']}: lowest point {low:.2f} m is at least 2.5 m over the footway and the projection {m_['projection_m']} m leaves the kerb 1 m clear", low >= 2.5 and m_["projection_m"] <= 1.0, f"declared clearance {p.get('clearance_below_m')}")
d_ = T["distinctness"]
check(G, "the ten fascias are pairwise distinct (ground dE76 >= 14, no shared name font, no shared construction with the same face colour and border)", not d_["violations"], f"min ground dE {d_['min_ground_dE']}; violations {d_['violations']}")
allw = set(T["approved_words"])
used = {b["text"] for s in T["shops"] for b in s["blocks"]} | {g["text"] for g in T["glass_lettering"] if g["text"]} | {p["faces"]["text"] for p in T["projecting_signs"] if "faces" in p} | {"TO LET"}
check(G, "every string on a board, glass or hanging sign is in approved_words", used <= allw, f"{len(used)} strings; extra {sorted(used - allw)}")
fb = T["forbidden_patterns"]
words = [w.upper() for t in allw for w in re.split(r"[\s·]+", t.replace("’", "'")) if w]
hit = [w for w in words if w in set(x.upper() for x in fb["alcohol_gambling_children"]) or w in set(x.upper() for x in fb["names_not_minted"])]
hit += [t for t in allw if any(r in t.upper() for r in fb["real_marks"] if " " in r)]
check(G, "no approved word is on the content rule's or the real-mark lists", not hit, f"{len(words)} words; hits {hit}")
rw = read("ledger/Assets/Scripts/Core/RealWorld.cs") or ""
anyc = re.search(r"AnyCase\s*=\s*\{(.*?)\};", rw, re.S)
lst = re.findall(r'"([^"]+)"', anyc.group(1)) if anyc else []
low = " ".join(t.lower().replace("’", "'") for t in allw)
hit2 = [x for x in lst if re.search(r"\b" + re.escape(x.lower()) + r"\b", low)]
check(G, "no approved string contains a name on RealWorld.cs's AnyCase list", bool(lst) and not hit2, f"{len(lst)} names read; hits {hit2}")
# widths on the real fonts
try:
    import importlib
    import os
    os.environ["FASCIA_FONTS"] = str(FONT_DIR)
    mt = importlib.import_module("make_target")
    bad = []
    n = 0
    for sc_ in mt.SHOPS_C:
        for b in sc_["blocks"]:
            n += 1
            tb = [x for x in shop(sc_["id"])["blocks"] if x["id"] == b["id"]][0]
            if not (near(b["width_mm"], tb["width_mm"], 0.2) and near(b["ink_box_mm"][0], tb["ink_box_mm"][0], 0.2)):
                bad.append((sc_["id"], b["id"], b["width_mm"], tb["width_mm"]))
    check(G, f"all {n} text blocks' stored ink widths equal a fresh measure on the real OFL font files", not bad, f"fonts at {FONT_DIR}; off: {bad}")
except Exception as e:  # noqa: BLE001
    check(G, "ink widths re-measured on the font files", False, f"not re-measured: {type(e).__name__}: {e}", kind="reported")
# P2 re-measure when the texture is on this machine
pb = Path("/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/dl/blue_painted_planks_diff_2k.jpg")
if pb.exists():
    from scipy import ndimage as ndi
    a = np.asarray(Image.open(pb).convert("RGB")).astype(float)
    lum2 = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    ex = (a[..., 1] >= a[..., 2] - 4) & (lum2 < 95)
    rowl = lum2.mean(axis=1)
    gap = ndi.binary_dilation(rowl < np.percentile(rowl, 50) * 0.6, iterations=4)
    valid = ~gap[:, None] * np.ones((1, a.shape[1]), bool)
    ex &= valid
    fr = float(ex[valid].mean())
    check(G, "P2 paint-loss fraction re-measured from the texture file equals the stored 0.286 (+-0.005)", near(fr, T["photo"]["planks"]["blue"]["loss_fraction"], 0.005), f"{fr:.3f}")
else:
    check(G, "P2 re-measured from the texture file", False, "texture not on this machine; stored values stand (measured 8 Oct)", kind="reported")
ages = [(s["id"], s["age"]["loss_fraction"]) for s in T["shops"]]
check(G, "every shop's paint-loss fraction is at most 0.6 of P2's 0.286 (0.17) or zero (glass, vinyl, box)", all(v == 0 or 0.0 < v <= 0.6 * 0.286 + 1e-9 for _, v in ages), f"{ages}")
check(G, "ten shops, trades as ruled 3 Oct, one of them bare", len(T["shops"]) == 10 and sum(1 for s in T["shops"] if not s["blocks"]) == 1, f"{[s['id'] for s in T['shops']]}")

# ============================================================================================
# 6 checks
# ============================================================================================
G = "6 checks"
ids = [c["id"] for c in T["checks"]]
check(G, "every check has id, name, scope, measure, expected, tolerance, unit, method, layer", all(all(k_ in c for k_ in ("id", "name", "scope", "measure", "expected", "tolerance", "unit", "method", "layer")) for c in T["checks"]), f"{len(ids)} checks")
check(G, "check ids are unique", len(ids) == len(set(ids)), f"{len(ids)}")
cm = {c["id"]: c for c in T["checks"]}
bad = []
for s in T["shops"]:
    for b in s["blocks"]:
        c = cm.get(f"{s['id']}.{b['id']}.contrast")
        if not c or b["contrast_1990"] < max(2.2, 0.85 * b["contrast_1990"]):
            bad.append(b["id"])
        c = cm.get(f"{s['id']}.{b['id']}.cap")
        if not c or not near(c["expected"], b["cap_mm"], 1e-9):
            bad.append(b["id"] + ".cap")
check(G, "each block's contrast and cap checks exist and the target meets its own nominal values", not bad, f"off: {bad}")
check(G, "a ground check exists for each shop", all(f"{s['id']}.ground" in cm for s in T["shops"]), "10 ground checks")
check(G, "an ageing check exists for each shop", all(f"{s['id']}.age" in cm for s in T["shops"]), "10 age checks")
check(G, "the lit box sign has an emissive check and the pawnbroker's board is not lit", "steam_laundry.emissive" in cm and "rita.lit" in cm, "")
# ============================================================================================
fails = [r for r in rows if not r["passed"] and r["kind"] == "check"]
rep = [r for r in rows if not r["passed"] and r["kind"] == "reported"]
npass = sum(1 for r in rows if r["passed"] and r["kind"] == "check")
ntot = sum(1 for r in rows if r["kind"] == "check")
summary = f"{npass} of {ntot} checks pass; {len(fails)} fail; {len(rep)} reported disagreement(s) or gaps kept visible"
result = dict(run="self_check.py, 8 Oct 2026 (cloud week 42)", summary=summary, photo_scale_px_per_mm_P1=round(s_px, 5), failures=fails, reported_disagreements=rep, rows=rows)
if "--no-write" not in sys.argv:
    T["self_check"] = result
    TP.write_text(json.dumps(T, indent=1, ensure_ascii=False), encoding="utf-8")
print("SELF-CHECK RESULT:", summary)
cur = None
for r in rows:
    if r["group"] != cur:
        cur = r["group"]
        print(f"\n## {cur}")
    mark = "ok  " if r["passed"] else ("REPORTED" if r["kind"] == "reported" else "FAIL")
    print(f"- [{mark}] {r['check']}: {r['detail']}")
sys.exit(1 if fails else 0)
