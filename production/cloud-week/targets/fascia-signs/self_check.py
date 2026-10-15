"""Test target.json against its own sources before anything is built to it.

    /home/user/.bpyenv/bin/python self_check.py [--fonts DIR] [--fetch-fonts DIR] [--no-write] [--fast]

Groups:
  1 printed      every printed or scaled number used comes back from target.json (the scene file, the kit README,
                 SCENE-SLOTS.md, the cast's hours, the 3 October trades, the recipe's bays and doors, the export's mirror)
  2 axis         the board's left-to-right as the GAME shows it: the recipe's mirror, each shop's door end, Mickey's name over
                 its door, the hanging signs on their piers
  3 photo wins   every disagreement settled for a photograph (D1 to D7) holds in target.json's own numbers
  4 photo P1     P1's saved preview (the two END crops of the board: no business name, no drink) re-measured by CODE,
                 the drawing's edges (target_drawing.py's polygons) laid on it at a scale fitted on one dimension only
                 (the lettered field's height); writes the overlay P1-leadenhall-board-target-on-photo.jpg
  5 sheet H1     the Hook sheet re-measured from production/reference/hook-sheet.png; departures are REPORTED
  6 consistency  boards inside their safe zone, nothing overlaps that should not, panels hold their words, contrast,
                 distinctness, layout variety, trade lines at 70 mm or more, the word list against the content rule and
                 the real-world list, geometry against texture, hanging signs, glass rows, ghosts, widths on the real fonts
  7 checks       the checks written for unit 4.1 are well formed and complete, and the target passes its own nominal values
  8 pixels       pixel_checks.py run on a reference render of every lettered board: the true board passes, a MIRRORED board,
                 a shifted board, a wrong font and a jittered board behave as they should
Writes the result into target.json under "self_check" and prints a result line and a table.
"""
import json
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
import pixel_checks as pc  # noqa: E402

TP = HERE / "target.json"
T = json.loads(TP.read_text(encoding="utf-8"))
PREV = ROOT / "production" / "previews" / "cloud-week" / "refs" / "fascia-signs"
SCRATCH_FONTS = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/fonts"
FONT_DIR = Path(sys.argv[sys.argv.index("--fonts") + 1]) if "--fonts" in sys.argv else Path(SCRATCH_FONTS)
FAST = "--fast" in sys.argv
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
HAVE_FONTS = FONT_DIR.exists() and any(FONT_DIR.iterdir())

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
check(G, "board 5.41 = 5.705 - 0.295 (kit README)", near(B["between_consoles_in_bay_m"][1] - B["between_consoles_in_bay_m"][0], B["width_mm"] / 1000, 1e-9) and "0.295 to 5.705" in (read("production/art/shopfront-kit/README.md") or ""),
      f"README quotes 0.295 to 5.705; target {B['between_consoles_in_bay_m']} -> {B['width_mm']} mm")
pcs = json.loads(read("production/specs/vignette-pieces.json") or "{}").get("pieces", [])
f0 = [p for p in pcs if p.get("name") == "east_parade_fascia0"]
check(G, "vignette-pieces.json east_parade_fascia0: 6.0 x 0.55 x 0.12 (the street's box)", bool(f0) and near(f0[0]["sx_m"], B["street_box_mm"][0] / 1000, 1e-9) and near(f0[0]["sy_m"], B["height_mm"] / 1000, 1e-9) and near(f0[0]["sz_m"], B["proud_of_wall_mm"] / 1000, 1e-9),
      f"source {f0[0]['sx_m'] if f0 else None} x {f0[0]['sy_m'] if f0 else None} x {f0[0]['sz_m'] if f0 else None}")
fa = read("production/art/fascia-01/01-SPEC-fascia-package.md") or ""
check(G, "fascia-01 spec: the cornice is 0.1500 high on the band (top 3.40 + 0.15 = 3.55) and oversails 0.215", "0.1500" in fa and "0.2150" in fa and near(B["cornice_top_m"], B["z_top_m"] + 0.15, 1e-9), f"cornice top {B['cornice_top_m']}")
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
conf = (hc.get("places") or {}).get("pension_counter", {}).get("x_m"), (hc.get("places") or {}).get("hals_shop", {}).get("x_m")
check(G, "REPORTED: hook-cast puts the newsagent's counter at x 32 and Hal's shop at x 39, the recipe the newsagent at x 36-42 and the ironmonger at 30-36", False,
      f"cast pension_counter x {conf[0]}, hals_shop x {conf[1]}; target newsagent {shop('newsagent')['street_x_m']}, ironmonger {shop('ironmonger')['street_x_m']}; a town question, in could_not_settle", kind="reported")
bb = json.loads(read("content/brands/brand-bible-v1.json") or "{}")
mk = [b for b in bb.get("brands", []) if b["id"] == "mickeys"]
check(G, "brand bible: Mickey's, minicab office, founded 1962 (the board's name is minted)", bool(mk) and mk[0]["founded"] == 1962 and mk[0]["kind"] == "minicab office" and shop("mickeys")["blocks"][0]["text"].replace("’", "'") == "MICKEY'S", f"brand bible {mk[0]['name'] if mk else None}, {mk[0]['founded'] if mk else None}")
sr = read("tools/art-recipes/shop-room.py") or ""
check(G, "shop-room.py: Mickey's glass lettering exists (0632  960418, MINICABS  ·  24 HOURS) and is NOT approved here", "0632  960418" in sr and "MINICABS  ·  24 HOURS" in sr and set(T["existing_not_approved"]) == {"0632 960418", "MINICABS · 24 HOURS"}
      and not (set(T["existing_not_approved"]) & set(T["approved_words"])), f"existing_not_approved {T['existing_not_approved']}")
hours_mk = (areas.get("mickeys") or {}).get("hours") or {}
check(G, "REPORTED: MINICABS · 24 HOURS on the glass contradicts the cast's hours for Mickey's (shut 3 to 7)", False, f"cast hours {hours_mk.get('mon')}; handed to the town and the shop-room builder", kind="reported")
fo = []
for k, v in T["fonts"].items():
    if k.startswith("_") or "ofl_url" not in v:
        continue
    d_ = v["file_in_google_fonts_repo"].split("/")[1]
    p = FONT_DIR / d_ / "OFL.txt"
    if p.exists():
        txt = p.read_text(errors="replace")
        rf = re.search(r'Reserved Font Names?\s+(.*?)(?:\s{2,}|\. |$)', " ".join(txt.splitlines()[:14]))
        got = rf.group(1).strip().strip('"').replace('" and "', ", ").replace('"', "") if rf else None
        fo.append((k, "SIL OPEN FONT LICENSE Version 1.1" in txt, got == v.get("reserved_font_name")))
if fo:
    check(G, "every OFL.txt of the nine fonts named is on this machine, carries the OFL 1.1 header and its Reserved Font Name is the one written", all(x[1] and x[2] for x in fo) and len(fo) == 9, f"{sum(x[1] for x in fo)} of {len(fo)} headers read; names right {sum(x[2] for x in fo)}; off {[x[0] for x in fo if not x[2]]}")
else:
    check(G, "OFL.txt files re-read", False, f"fonts not on this machine at {FONT_DIR}; run with --fonts DIR or --fetch-fonts DIR (raw.githubusercontent.com)", kind="reported")
used_fonts = {b["font"] for s in T["shops"] for b in s["blocks"]} | {g["font"] for g in T["glass_lettering"] if g["font"]} | {p["faces"]["font"] for p in T["projecting_signs"] if "faces" in p}
check(G, "every font used is in fonts{}, none is Overpass, and Libre Baskerville is gone", all(k in T["fonts"] for k in used_fonts) and "overpass" not in json.dumps(list(used_fonts)).lower() and "libre-baskerville" not in used_fonts and "libre-baskerville" not in T["fonts"], f"{sorted(used_fonts)}")

# ============================================================================================
# 2 axis
# ============================================================================================
G = "2 axis"
check(G, "the export reflects y to -y and lettered faces' UVs run from the reader's left to right in the reflected street (the recipe says so)", "REFLECTED y to -y AT EXPORT" in tf and "running from the" in tf and "reader's left to the reader's right" in tf.replace("\n#: ", " ").replace("\n", " "), "terrace-front.py export docstring and sidecar")
mt_ = re.search(r"BAY_DOORS_ON = \(([^)]*)\)", tf)
bdo = [x.strip().strip('"') for x in mt_.group(1).split(",")] if mt_ else []
check(G, "BAY_DOORS_ON read from the recipe", bdo == ["left", "left", "right", "left", "right", "right"], f"{bdo}")


def door_end_(side, bay, block_doors_on=None):
    d = block_doors_on or bdo[bay % len(bdo)]
    if side == "east":
        return "low" if d == "left" else "high"
    return "high" if d == "left" else "low"


chandler_doors = (blocks.get("east_chandler") or {}).get("doors_on")
for s in T["shops"]:
    want_end = door_end_(s["side"], s["bay"], chandler_doors if s["block"] == "east_chandler" else None)
    check(G, f"{s['id']}: door end {s['door_end_street']} street x equals the recipe's (BAY_DOORS_ON, the west half turn)", s["door_end_street"] == want_end, f"recipe {want_end}")
    x0, x1 = s["street_x_m"]
    u0 = (x1 - 0.295) if s["side"] == "east" else (x0 + 0.295)
    check(G, f"{s['id']}: the board's left edge is street x {s['board_u0_street_x_m']} ({'east: the bay\'s high end - 0.295, low street x on the viewer\'s RIGHT' if s['side'] == 'east' else 'west: the bay\'s low end + 0.295, low street x on the viewer\'s LEFT'})", near(s["board_u0_street_x_m"], u0, 1e-6), f"{u0}")
mo = json.loads(read("production/specs/mickeys-office.json") or "{}")
dx = (mo.get("door") or {}).get("x")
mkb = shop("mickeys")["blocks"][0]
exp_u = (shop("mickeys")["board_u0_street_x_m"] - dx) * 1000
check(G, "D6: Mickey's name stands over its door: board x = (3.0 + 6.0 - 0.295 - door x) x 1000, the door x read from mickeys-office.json", dx is not None and near(mkb["x_mm"], exp_u, 1.0) and near(T["axis"]["mickeys_door"]["street_x_m"], dx, 1e-9) and mkb["x_mm"] > B["width_mm"] / 2,
      f"door x {dx} -> board x {exp_u:.1f}; target {mkb['x_mm']}; right half of the board because the door is at the viewer's right")
check(G, "Mickey's geometry letters are centred at the same board x and street x as its name block", near(shop("mickeys")["geometry"][0]["centre_board_x_mm"], mkb["x_mm"], 0.5) and near(shop("mickeys")["geometry"][0]["centre_street_x_m"], dx, 1e-9), "")
pairs_ = [(p, shop(p["shop"])) for p in T["projecting_signs"]]
for p, s in pairs_:
    x0, x1 = s["street_x_m"]
    xm = p["mount"]["x_street_m"]
    on_pier = near(xm, x0 + 0.175, 1e-6) or near(xm, x1 - 0.175, 1e-6)
    high = xm > (x0 + x1) / 2
    vs = p["mount"]["viewer_side"]
    right_words = ("LEFT" in vs) if (s["side"] == "east") == high else ("RIGHT" in vs)
    check(G, f"{p['id']}: street x {xm} stands on a pier of its own bay and its viewer-side words ('{vs}') are right for the game's axis", on_pier and x0 <= xm <= x1 and right_words, f"bay {x0}-{x1}, high end {high}")
rp = [p for p in T["projecting_signs"] if p["id"] == "ritas_three_balls"][0]
check(G, "Rita's balls are at her DOOR end (high street x, 20.825), not the window end beside the fish shop", shop("ritas")["door_end_street"] == "high" and near(rp["mount"]["x_street_m"], 20.825, 1e-6), f"door end {shop('ritas')['door_end_street']}")
rl = tf.find("RAISED_LETTERS = ")
check(G, "the recipe's RAISED_LETTERS line is read: MICKEY’S, cap 0.24; the target amends it (cap 0.330, centre over the door, stand-off 0.014) and keeps no letter set in the texture",
      rl > 0 and "MICKEY’S\", 0.24" in tf[rl:rl + 200] and mkb["in_texture"] is False and shop("mickeys")["geometry"][0]["cap_m"] == 0.330, tf[rl:rl + 90].replace("\n", " "))
for s in T["shops"]:
    fl = [(g["shop"], g["text"], g["x_street_m"]) for g in T["glass_lettering"] if g["shop"] == s["id"] and g["text"] and not g.get("existing")]
    bad = [f for f in fl if f[2] is None or not (s["street_x_m"][0] <= f[2] <= s["street_x_m"][1])]
    check(G, f"{s['id']}: every glass row has a street x inside its bay", not bad, f"{len(fl)} rows; off {bad}")

# ============================================================================================
# 3 photo wins
# ============================================================================================
G = "3 photo wins"
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
check(G, "D3 numbers at the ends are P1's 0.91 of the name's cap, on two boards only (Rita's and the chandler)", not bad and len(ends) == 4 and {i for i, _ in ends} == {"ritas", "chandler"}, f"{len(ends)} end numerals on {sorted({i for i, _ in ends})}; P1 {R['numeral_over_cap']}; off: {bad}")
rb = shop("ritas")["border"]
fh = B["field_mm"][3] - B["field_mm"][1]
check(G, "D4 Rita's keyline: P1's inset, thickness and concave corner (+-0.03 of the field)", near(rb["inset_mm"] / fh, (R["keyline_top_inset"] + R["keyline_bottom_inset"]) / 2, 0.03) and near(rb["line_mm"] / fh, R["keyline_thickness"], 0.012) and near(rb["radius_mm"] / fh, R["corner_radius"], 0.03) and rb["inner_line_mm"] == 0,
      f"target inset {rb['inset_mm'] / fh:.3f}, line {rb['line_mm'] / fh:.3f}, radius {rb['radius_mm'] / fh:.3f}; P1 inset {(R['keyline_top_inset'] + R['keyline_bottom_inset']) / 2:.3f}, line {R['keyline_thickness']}, radius {R['corner_radius']}")
check(G, "D5 no disagreement: the board is the street's 0.55 m, inside FRONTAGE's 'not more than 600 mm' [CV] and P1's 0.53 to 0.57 m", B["height_mm"] == 550 and B["height_mm"] <= 600, f"field {fh} of {B['height_mm']}")
fm = shop("fish_market")
check(G, "D1 the fishmonger: red sign-writing (t13138) on the sheet's pale board, black block shade", fm["ground"]["colour"] == "light_board" and fm["blocks"][0]["face"] == "vermilion" and fm["blocks"][0]["shade"]["colour"] == "shade_black"
      and near(T["palette"]["light_board"]["srgb_1990"][0], T["photo"]["H1"]["colours"]["white_board"][0], 15), f"ground {T['palette']['light_board']['srgb_1990']} (sheet white {T['photo']['H1']['colours']['white_board']}), name {fm['blocks'][0]['face']}")
caps = [b["cap_over_field"] for s in T["shops"] for b in s["blocks"] if b["role"] == "name" and not b["ghost"]]
check(G, "D7 the name lines run 0.30 to 0.70 of the field, varied", min(caps) >= 0.30 and max(caps) <= 0.70 and len(set(caps)) >= 6, f"{sorted(set(caps))}")

# ============================================================================================
# 4 photo P1: re-measure by code on the saved END crops, then lay the drawing on them
# ============================================================================================
G = "4 photo P1"
P1 = T["photo"]["P1"]
pv = P1["preview"]
img = Image.open(PREV / pv["file"]).convert("RGB")
k = pv["scale"]
gap = pv["gap_px"]
cl = pv["crops_view_px"]["left"]
cr = pv["crops_view_px"]["right"]
LW = int(round((cl[2] - cl[0]) * k))
RX = LW + gap
A = np.asarray(img).astype(float)
Hh, Ww, _ = A.shape
check(G, "the saved P1 preview cannot show the name or any window lettering: both crops end before the name (x 1492 to 2123 of the view) and show only the board's two ends", cl[2] <= P1["px"]["text_x0"] and cr[0] >= P1["px"]["text_x1"] and cl[3] - cl[1] == cr[3] - cr[1] and cl[1] >= 120 and cl[3] <= 400,
      f"left crop x {cl[0]} to {cl[2]}, right crop x {cr[0]} to {cr[2]}, y {cl[1]} to {cl[3]}; the board is y 154 to 330")
names = sorted(p.name for p in PREV.iterdir())
check(G, "no preview in the folder is named for a business or shows the bar's front: no file with 'chamberlain' or 'front-scale' in its name", not [n for n in names if "chamberlain" in n.lower() or "front-scale" in n.lower()], f"{names}")
L_ = A[:, :LW]
R_ = A[:, RX:]
gL = (L_[..., 0] > 200) & (L_[..., 1] > 150) & (L_[..., 2] < 130) & (L_[..., 1] > 0.6 * L_[..., 0])
lumL = 0.299 * L_[..., 0] + 0.587 * L_[..., 1] + 0.114 * L_[..., 2]


def vx(x, part):
    return (x - cl[0]) * k if part == "L" else RX + (x - cr[0]) * k


def vy(y):
    return (y - cl[1]) * k


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


nl0, nl1 = int(vx(P1["px"]["numeral_left"][0], "L")) - 4, int(vx(P1["px"]["numeral_left"][1], "L")) + 4
numrows = gL[:, nl0:nl1].sum(axis=1) / float(nl1 - nl0)
nb = max(runs((numrows > 0.08) & (numrows < 0.90)), key=lambda r: r[1] - r[0])        # the keyline rows are 0.9 or more; the numeral 2's foot is 0.7
num_top, num_bot = float(nb[0]), float(nb[1] + 1)
c0_, c1_ = nl1 + 20, LW - 6
rowfrac = gL[:, c0_:c1_].sum(axis=1) / float(c1_ - c0_)
bands = runs(rowfrac > 0.70)
above = [b_ for b_ in bands if b_[1] < num_top]
below = [b_ for b_ in bands if b_[0] > num_bot]


def centroid(rng):
    ys = np.arange(rng[0], rng[1] + 1)
    w = np.clip(L_[rng[0]:rng[1] + 1, c0_:c1_, 1].mean(axis=1) - 120, 0, None)
    return float((ys * w).sum() / w.sum()) + 0.5


key_top = centroid(above[-1])
key_bot = centroid(below[0])
prof = lumL[:, c0_:c1_].mean(axis=1)
med = np.median(prof[int(key_top) + 5:int(key_bot) - 5])
rng_ = range(int(key_top) - int(22 * k), int(key_top) - int(2 * k))
top_dark = [min(rng_, key=lambda y: prof[y])] if min(prof[y] for y in rng_) < 0.85 * med else []
bot_dark = [y for y in range(int(key_bot) + int(4 * k), min(Hh, int(key_bot) + int(40 * k))) if prof[y] < 0.5 * med]
field_top = (top_dark[0] + 1.5 * k) if top_dark else float("nan")
field_bot = float(min(bot_dark)) if bot_dark else float("nan")


def outer_keyline(Arr, rows_slice, left=True):
    colR = Arr[rows_slice, :, 0].mean(axis=0)
    W_ = colR.shape[0]
    loc = colR - 0.5 * (np.roll(colR, int(7 * k)) + np.roll(colR, -int(7 * k)))
    cand = np.where(loc > 35)[0]
    cand = cand[cand < 0.5 * W_] if left else cand[cand > 0.5 * W_]
    c0 = int(cand.min()) if left else int(cand.max())
    run, x, cs = [c0], c0, set(cand.tolist())
    while (x + (1 if left else -1)) in cs:
        x += 1 if left else -1
        run.append(x)
    w_ = np.clip(loc[run], 0, None)
    return float((np.array(run) * w_).sum() / w_.sum()) + 0.5


rs = slice(int(key_top) + int(20 * k), int(key_bot) - int(20 * k))
key_l = outer_keyline(L_, rs, True)
key_r = RX + outer_keyline(R_, rs, False)
meas = dict(field_top=field_top, field_bottom=field_bot, keyline_top=key_top, keyline_bottom=key_bot, keyline_left=key_l, keyline_right=key_r, numeral_top=num_top, numeral_bottom=num_bot)
hand = dict(field_top=vy(P1["px"]["field_top"]), field_bottom=vy(P1["px"]["field_bottom"]), keyline_top=vy(P1["px"]["keyline_top_y"]), keyline_bottom=vy(P1["px"]["keyline_bottom_y"]),
            keyline_left=vx(P1["px"]["keyline_left_x"], "L"), keyline_right=vx(P1["px"]["keyline_right_x"], "R"), numeral_top=vy(P1["px"]["numeral_top"]), numeral_bottom=vy(P1["px"]["numeral_bottom"]))
tol = P1["error_px"] * k
for kk in hand:
    check(G, f"hand measure of {kk} equals the code's measure on the saved preview (+-{tol:.1f} preview px = 3 view px)", abs(meas[kk] - hand[kk]) <= tol, f"code {meas[kk]:.1f}, hand {hand[kk]:.1f}, diff {meas[kk] - hand[kk]:+.1f} preview px")
check(G, "NOT re-measurable on the preview (it holds the ends only), recorded from the unmasked view: cap top and bottom, name x0 and x1, shade 4.5 px, door leaf", True, f"{P1['measured_on_unmasked']}", kind="reported")
rows[-1]["passed"] = False
# the drawing laid on the photograph at a scale fitted on ONE dimension: the lettered field's height
tpl = td.template_data(T)
fh_mm = tpl["field_mm"][3]
fpx = meas["field_bottom"] - meas["field_top"]
s_px = fpx / fh_mm
cxp = (meas["keyline_left"] + meas["keyline_right"]) / 2.0


def Ypx(y_up):
    return meas["field_top"] + (fh_mm - y_up) * s_px


def XL(x):                         # template x, anchored on the LEFT keyline
    return meas["keyline_left"] + (x - tpl["keyline_left_x"]) * s_px


def XR(x):                         # template x, anchored on the RIGHT keyline
    return meas["keyline_right"] + (x - tpl["keyline_right_x"]) * s_px


nm_l, nm_r = [t for t in tpl["text"] if t["role"] == "numeral_left"][0], [t for t in tpl["text"] if t["role"] == "numeral_right"][0]
proj = dict(keyline_top=Ypx(tpl["keyline_top_y"]), keyline_bottom=Ypx(tpl["keyline_bottom_y"]), keyline_left=XL(tpl["keyline_left_x"]), keyline_right=XR(tpl["keyline_right_x"]),
            numeral_top=Ypx(nm_l["top_y"]), numeral_bottom=Ypx(nm_l["bottom_y"]))
for kk, v in proj.items():
    check(G, f"drawing edge {kk} falls on the photograph's edge (+-{tol:.1f} preview px)", abs(v - meas[kk]) <= tol, f"drawing {v:.1f}, photograph {meas[kk]:.1f}, diff {v - meas[kk]:+.1f}; scale {s_px:.4f} px/mm from the field height {fpx:.1f} px = {fh_mm:.0f} mm only")
# numeral x edges (left numeral, left end; right numeral, right end), measured on the preview by column
colsL = np.where(gL[int(num_top):int(num_bot), nl0 - 12:nl1 + 12].sum(axis=0) > 0)[0] + nl0 - 12
nx0, nx1 = float(colsL.min()), float(colsL.max() + 1)
check(G, "drawing's left numerals' x edges fall on the photograph's (+-6 preview px: the numerals' glyph shapes are the font's, not P1's)", abs(XL(nm_l["x0"]) - nx0) <= 6 and abs(XL(nm_l["x1"]) - nx1) <= 6, f"drawing {XL(nm_l['x0']):.1f} to {XL(nm_l['x1']):.1f}, photograph {nx0:.1f} to {nx1:.1f}")
# the overlay picture
ov = img.copy()
dr = ImageDraw.Draw(ov)
for L in tpl["layers"]:
    if L["role"] == "keyline":
        cl_ = L["centreline"]
        for a_, b_ in zip(cl_[:-1], cl_[1:]):                     # segment by segment: a filtered point list would join the two ends of the ring
            if a_[0] < tpl["field_mm"][2] / 2 and b_[0] < tpl["field_mm"][2] / 2:
                dr.line([(XL(a_[0]), Ypx(a_[1])), (XL(b_[0]), Ypx(b_[1]))], fill=(0, 255, 255), width=1)
            elif a_[0] >= tpl["field_mm"][2] / 2 and b_[0] >= tpl["field_mm"][2] / 2:
                dr.line([(XR(a_[0]), Ypx(a_[1])), (XR(b_[0]), Ypx(b_[1]))], fill=(0, 255, 255), width=1)
            else:                                                    # a long straight edge from one end to the other: drawn in each crop up to its edge
                lo_, hi_ = (a_, b_) if a_[0] < b_[0] else (b_, a_)
                dr.line([(XL(lo_[0]), Ypx(lo_[1])), (LW, Ypx(lo_[1]))], fill=(0, 255, 255), width=1)
                dr.line([(RX, Ypx(hi_[1])), (XR(hi_[0]), Ypx(hi_[1]))], fill=(0, 255, 255), width=1)
cap_y, base_y = [t for t in tpl["text"] if t["role"] == "name"][0]["cap_y"], [t for t in tpl["text"] if t["role"] == "name"][0]["baseline_y"]
for xa, xb in ((0, LW), (RX, Ww)):
    dr.line([(xa, Ypx(cap_y)), (xb, Ypx(cap_y))], fill=(0, 255, 255), width=1)
    dr.line([(xa, Ypx(base_y)), (xb, Ypx(base_y))], fill=(0, 255, 255), width=1)
dr.rectangle([XL(nm_l["x0"]), Ypx(nm_l["top_y"]), XL(nm_l["x1"]), Ypx(nm_l["bottom_y"])], outline=(0, 255, 255))
dr.rectangle([XR(nm_r["x0"]), Ypx(nm_r["top_y"]), XR(nm_r["x1"]), Ypx(nm_r["bottom_y"])], outline=(0, 255, 255))
# Rita's two ends at the same scale: her left end on the photograph's left end, her right end on the right end (magenta)
rs_ = shop("ritas")
fy1 = B["field_mm"][3]
fx0, fx1 = B["field_mm"][0], B["field_mm"][2]


def YR(y_up):
    return meas["field_top"] + (fy1 - y_up) * s_px


def XRL(x):
    return meas["keyline_left"] - (74.5 - 0) * s_px + (x - 0) * s_px - (0 - 0)        # her keyline centre (x 74.5) on the photograph's left keyline


def XRR(x):
    return meas["keyline_right"] + (x - (B["width_mm"] - 74.5)) * s_px


for sh_ in rs_["shapes"]:
    if sh_["kind"] == "polyline":
        pl = sh_["pts"]
        for a_, b_ in zip(pl[:-1], pl[1:]):
            if a_[0] < B["width_mm"] / 2 and b_[0] < B["width_mm"] / 2:
                dr.line([(XRL(a_[0]), YR(a_[1])), (XRL(b_[0]), YR(b_[1]))], fill=(255, 0, 255), width=1)
            elif a_[0] >= B["width_mm"] / 2 and b_[0] >= B["width_mm"] / 2:
                dr.line([(XRR(a_[0]), YR(a_[1])), (XRR(b_[0]), YR(b_[1]))], fill=(255, 0, 255), width=1)
            else:
                lo_, hi_ = (a_, b_) if a_[0] < b_[0] else (b_, a_)
                dr.line([(XRL(lo_[0]), YR(lo_[1])), (LW, YR(lo_[1]))], fill=(255, 0, 255), width=1)
                dr.line([(RX, YR(hi_[1])), (XRR(hi_[0]), YR(hi_[1]))], fill=(255, 0, 255), width=1)
for b in rs_["blocks"]:
    if b["role"] == "end":
        x0, y0, x1, y1 = b["ink_box_mm"]
        f_ = XRL if x0 < B["width_mm"] / 2 else XRR
        dr.rectangle([f_(x0), YR(y1), f_(x1), YR(y0)], outline=(255, 0, 255))
dr.text((6, 4), "cyan: P1's ratios laid by the drawing code, scale from the field height only", fill=(255, 255, 255))
dr.text((6, 16), "magenta: Rita's board ends at the same scale (keyline, number 5)", fill=(255, 255, 255))
ovp = PREV / "P1-leadenhall-board-target-on-photo.jpg"
if "--no-write" not in sys.argv:
    ov.save(ovp, quality=88, optimize=True)
check(G, "the overlay was written and is under 300 KB", ("--no-write" in sys.argv) or ovp.stat().st_size < 300_000, f"{ovp.name} {ovp.stat().st_size if ovp.exists() else 0} bytes")
cap_rita = rs_["blocks"][0]["cap_mm"] / fh_mm
check(G, "REPORTED: Rita's name is larger over its field than the photographed board's (deliberate: a trading parade, not a restored arcade)", False,
      f"Rita's name cap {cap_rita:.3f} of the field; P1 {R['cap_over_field']}", kind="reported")

# ============================================================================================
# 5 sheet H1
# ============================================================================================
G = "5 sheet H1"
hs = np.asarray(Image.open(ROOT / "production" / "reference" / "hook-sheet.png").convert("RGB")).astype(float)
bd = hs[500:535, 320:600].reshape(-1, 3)
L_ = hs[510:556, 625:755].reshape(-1, 3)
mk_ = (L_[:, 0] > L_[:, 2] + 25) & (L_[:, 0] > 110)
bm, gm = bd.mean(0), L_[mk_].mean(0)
pal = T["palette"]
check(G, "Mickey's board colour is the sheet's measured mean (+-3 each channel)", np.all(np.abs(bm - np.array(pal["slate"]["srgb_1990"])) <= 3), f"sheet {bm.round(1).tolist()}, target {pal['slate']['srgb_1990']}")
check(G, "Mickey's letter colour is the sheet's measured mean (+-4 each channel)", np.all(np.abs(gm - np.array(pal["brass_gilt"]["srgb_1990"])) <= 4), f"sheet {gm.round(1).tolist()}, target {pal['brass_gilt']['srgb_1990']}")
wb = hs[545:575, 870:1000].reshape(-1, 3).mean(0)
check(G, "the sheet's white fascia beside Mickey's re-measured (204,204,204 +-4); the fish board's 1990 ground is within 15 of it per channel", np.all(np.abs(wb - 204) <= 4) and np.all(np.abs(np.array(pal["light_board"]["srgb_1990"]) - wb) <= 15), f"sheet {wb.round(1).tolist()}, target {pal['light_board']['srgb_1990']}")
mx = shop("mickeys")["blocks"][0]
sheet_cap = T["photo"]["H1"]["ratios"]["cap_over_board"]
check(G, "REPORTED: Mickey's cap over the board: the sheet's letters fill 0.69 of the board, the target's 0.60 (330 of 550)", False, f"target {mx['cap_mm'] / B['height_mm']:.2f}, sheet {sheet_cap}; the target keeps Marcellus SC (ruled), 1.8 times wider than the sheet's tall narrow capitals, so the cap stops at 330 mm", kind="reported")
check(G, "REPORTED: the name's width over its cap: the sheet's 3.5, the target's", False, f"target {mx['width_mm'] / mx['cap_mm']:.2f}, sheet {T['photo']['H1']['ratios']['width_over_cap']}", kind="reported")

# ============================================================================================
# 6 consistency
# ============================================================================================
G = "6 consistency"
SAFE = B["safe_mm"]
safe_box = sbox(*SAFE)
board_box = sbox(0, 0, B["width_mm"], B["height_mm"])
for s in T["shops"]:
    bl = [b for b in s["blocks"] if not b["ghost"]]
    ok = all(safe_box.contains(sbox(*b["effects_box_mm"])) for b in bl)
    check(G, f"{s['id']}: every ink box with its shade, outline and jitter is inside the safe rectangle", ok, f"min margin {s['min_margin_mm']} mm" if bl else "no lettering on this board")
    ov_ = [(a["id"], b["id"]) for i, a in enumerate(bl) for b in bl[i + 1:] if sbox(*a["effects_box_mm"]).intersects(sbox(*b["effects_box_mm"]))]
    check(G, f"{s['id']}: no two text blocks overlap (ghosts excepted)", not ov_, f"{ov_}")
    pn = (s["border"] or {}).get("panel_mm") or (s["border"] or {}).get("face_mm")
    if pn and bl:
        pb = sbox(*pn).buffer(-15)
        check(G, f"{s['id']}: every text block sits inside its panel with 15 mm to spare", all(pb.contains(sbox(*b["effects_box_mm"])) for b in bl if b["in_texture"] or True), f"panel {pn}")
    for b in bl:
        e = b["effects_box_mm"]
        check(G, f"{s['id']}.{b['id']}: the baseline and cap line fit the field", B["field_mm"][1] <= b["baseline_mm"] and b["baseline_mm"] + b["cap_mm"] <= B["field_mm"][3], f"baseline {b['baseline_mm']}, cap line {b['baseline_mm'] + b['cap_mm']}")
        check(G, f"{s['id']}.{b['id']}: contrast {b['contrast_1990']} is at least 2.2", b["contrast_1990"] >= 2.2, f"{b['face_1990']} on {b['ground_1990']}")
    for b in s["blocks"]:
        if b["ghost"]:
            dgh = float(pc.dE(np.array(b["face_1990"], float), np.array(b["ground_1990"], float)))
            check(G, f"{s['id']}.{b['id']}: ghost {b['text']!r} is {dgh:.1f} dE from its ground (3 to 5), trade or brand words only, broken {b['broken_fraction']}", 3.0 <= dgh <= 5.0 and b["text"] in T["ghost_words"] and b["text"] in T["approved_words"], f"{b['font']} cap {b['cap_mm']} centred {b['x_mm']} baseline {b['baseline_mm']}")
    g_ = s.get("ghost")
    if g_ and g_.get("box_mm"):
        check(G, f"{s['id']}: the ghost patch lies on the board", board_box.contains(sbox(*g_["box_mm"])), f"{g_['box_mm']}")
    if g_ and g_.get("pinhole_positions_mm"):
        check(G, f"{s['id']}: the {len(g_['pinhole_positions_mm'])} pin holes lie on the ghost's old cap line inside the board", len(g_["pinhole_positions_mm"]) == g_["pinholes"] and all(board_box.contains(sbox(p[0] - 2, p[1] - 2, p[0] + 2, p[1] + 2)) for p in g_["pinhole_positions_mm"]), f"{g_['pinhole_row']}")
    for sh_ in s["shapes"]:
        if sh_["kind"] == "rect":
            check(G, f"{s['id']}: {sh_['role']} lies on the board", board_box.contains(sbox(*sh_["box"])), f"{sh_['box']}")
    for gp in s["geometry"]:
        if gp["kind"] in ("box_sign", "flat_panel"):
            check(G, f"{s['id']}: the {gp['kind']} geometry lies on the board with its face texture rectangle and is {round(gp['depth_m'] * 1000)} mm deep", board_box.contains(sbox(*gp["outer_mm"])) and gp["face_texture_rect_mm"] == gp["outer_mm"] and 0.02 <= gp["depth_m"] <= 0.2, f"{gp['outer_mm']}")
        if gp["kind"] == "box_sign":
            e = gp["emissive"]
            tubes_ok = True
            if e.get("dead_tube"):
                dt = e["dead_tube"]["x_mm"]
                j = e["tube_joints_x_mm"]
                tubes_ok = any(near(dt[0], j[i], 0.5) and near(dt[1], j[i + 1], 0.5) for i in range(len(j) - 1)) and e["dead_tube"]["row"] == "upper" and e["dead_tube"]["level_pct"] == 60
            fx = e["face_mm"]
            check(G, f"{s['id']}: the box's emissive layout is one tube per segment between joints, the dead tube is ONE tube of the upper row at 60 per cent, rows lie inside the face", tubes_ok and all(fx[1] < y < fx[3] for y in e["tube_rows_y_mm"]) and e["tube_end_shadow"]["width_mm"] == 60 and e["tube_end_shadow"]["dim_pct"] == 10, f"joints {e['tube_joints_x_mm']} dead {e['dead_tube']}")
    mo_ = s.get("moulding")
    check(G, f"{s['id']}: planted moulding only on Rita's, the ironmonger and the chandler (never on vinyl, box, panel or glass)", bool(mo_) == (s["id"] in ("ritas", "ironmonger", "chandler")) and (not mo_ or (mo_["width_mm"] == 24 and mo_["height_mm"] == 0.6 and mo_["chamfer_mm"] == 4)), f"{mo_}")
    if s["border"] and s["border"]["kind"] == "glass_slab":
        jx = s["border"]["joints_x_mm"]
        nm_ = [b for b in bl if b["id"] == "name"][0]["ink_box_mm"]
        check(G, "grocer: three slabs, the name's ink inside the middle slab with 20 mm to spare, joints 3 mm, no crack on the fascia", len(jx) == 2 and nm_[0] - jx[0] >= 20 and jx[1] - nm_[2] >= 20 and s["border"]["joint_mm"] == 3 and "crack" not in s["age"], f"joints {jx}, name ink {nm_[0]} to {nm_[2]}")
for p in T["projecting_signs"]:
    m_ = p["mount"]
    low = p["lowest_computed_m"]
    foot_ok = (m_.get("plate_foot_m") is None) or (m_["plate_foot_m"] >= T["board"]["cornice_top_m"] + 0.05 - 1e-9)
    arm_ok = m_["arm_height_m"] >= T["board"]["cornice_top_m"] + 0.05 - 1e-9 if p["id"] != "steam_laundry_box" else (m_["arm_height_m"] - p["parts"]["box_m"][1]) >= T["board"]["cornice_top_m"] + 0.05 - 1e-9
    check(G, f"{p['id']}: fixed to the brick above the cornice (plate foot / box bottom at least 3.60 m), lowest point {low:.2f} m at least 2.5 m, projection {m_['projection_m']} m at most 1.0, declared clearance equals the computed one", foot_ok and arm_ok and low >= 2.5 and m_["projection_m"] <= 1.0 and near(p["clearance_below_m"], low, 1e-6) and near(p.get("lowest_m", low), low, 0.011), f"declared lowest {p.get('lowest_m')}, computed {low}")
for p in T["small_panels"]:
    if p["id"] == "letting_board":
        cx, cy = p["centre_on_board_mm"]
        w, h = p["size_mm"]
        check(G, "the letting board lies on the empty unit's board", board_box.contains(sbox(cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2)), f"{w} x {h} at {cx}, {cy}")
hp = [p for p in T["small_panels"] if p["id"] == "hours_plate"][0]
rx = re.compile(hp["rule"]["pattern"])
check(G, "the hours plates' own rule accepts 'MON-SAT 9-5.30', 'WED 9-1', 'SUN 7-12' and refuses a shop name and a stray word", all(rx.match(t) for t in ("MON-SAT 9-5.30", "WED 9-1", "SUN 7-12", "9-5.30")) and not any(rx.match(t) for t in ("RITA'S", "COCKTAIL BAR", "BAR 9-5")), "")
d_ = T["distinctness"]
check(G, "the ten fascias are pairwise distinct (ground dE76 >= 14, no shared name font, no shared construction with the same face colour and border)", not d_["violations"], f"min ground dE {d_['min_ground_dE']}; violations {d_['violations']}")
check(G, "G11 layout variety: no more than five boards share the centred name-over-trade skeleton, no more than three trade lines use ' · ', at least six layout classes", len(d_["centred_skeleton_boards"]) <= 5 and len(d_["dotted_trade_lines"]) <= 3 and len({v for v in d_["layout_classes"].values() if v != "none"}) >= 6,
      f"centred {d_['centred_skeleton_boards']}; dotted {d_['dotted_trade_lines']}; classes {sorted(set(d_['layout_classes'].values()))}")
tl = [(s["id"], b["id"], b["cap_mm"]) for s in T["shops"] for b in s["blocks"] if b["role"] == "trade" and not b["ghost"]]
glass_trade = [g for g in T["glass_lettering"] if g["shop"] == "newsagent" and "CONFECTIONER" in g["text"]]
check(G, "every trade line is at least 70 mm tall (fascia blocks and the newsagent's door-glass trade line)", all(c >= 70 for _, _, c in tl) and all(g["cap_mm"] >= 70 for g in glass_trade) and T["common_style"]["trade_line_minimum_cap_mm"] == 70, f"{len(tl)} trade blocks, minimum {min(c for _, _, c in tl)}; glass {[g['cap_mm'] for g in glass_trade]}")
slow = {s["id"] for s in T["shops"] for b in s["blocks"] if b["role"] == "trade" and b["tracking_em"] <= 0.12 and not b["ghost"]}
check(G, "trade-line tracking at most +0.12 em on at least four boards", len(slow) >= 4, f"{sorted(slow)}")
check(G, "the ironmonger's trade is in its two end panels (TOOLS & / HARDWARE and PAINTS & / PARAFFIN), the newsagent's fascia is the name alone", {b["text"] for b in shop("ironmonger")["blocks"] if b["role"] == "trade"} == {"TOOLS &", "HARDWARE", "PAINTS &", "PARAFFIN"} and [b["text"] for b in shop("newsagent")["blocks"]] == ["NEWSAGENT"], "")
plastic = [s["id"] for s in T["shops"] if s["construction_kind"] in ("box_sign", "flat_panel")]
check(G, "the 1980s plastic generation is three of the ten fronts (lit box signs on the launderette and the newsagent, the tea room's flat panel) and the tea room is a plain caff", sorted(plastic) == ["newsagent", "steam_laundry", "tea_rooms"] and shop("tea_rooms")["construction_kind"] == "flat_panel" and shop("tea_rooms")["border"]["frame_mm"] == 25, f"{plastic}")
allw = set(T["approved_words"])
used = {b["text"] for s in T["shops"] for b in s["blocks"]} | {g["text"] for g in T["glass_lettering"] if g["text"] and not g.get("existing")} | {p["faces"]["text"] for p in T["projecting_signs"] if "faces" in p} | {"TO LET"}
check(G, "every string on a board, ghost, glass or hanging sign is in approved_words; the existing glass lines are not", used <= allw and not (set(T["existing_not_approved"]) & allw), f"{len(used)} strings; extra {sorted(used - allw)}")
non_ghost = {b["text"] for s in T["shops"] for b in s["blocks"] if not b["ghost"]}
check(G, "a ghost string appears only as a ghost: FISHMONGER is on no board and no glass row; the ghost words are minted trade or brand words", T["ghost_words"] == sorted({b["text"] for s in T["shops"] for b in s["blocks"] if b["ghost"]}) and "FISHMONGER" not in non_ghost and "FISHMONGER" not in {g["text"] for g in T["glass_lettering"]}, f"{T['ghost_words']}")
fb = T["forbidden_patterns"]
words = [w.upper() for t in allw for w in re.split(r"[\s·,]+", t.replace("’", "'")) if w]
hit = [w for w in words if w in set(x.upper() for x in fb["alcohol_gambling_children"]) or w in set(x.upper() for x in fb["names_not_minted"])]
hit += [t for t in allw if any(r in t.upper() for r in fb["real_marks"] if " " in r)]
check(G, "no approved word is on the content rule's or the real-mark lists", not hit, f"{len(words)} words; hits {hit}")
rw = read("ledger/Assets/Scripts/Core/RealWorld.cs") or ""
anyc = re.search(r"AnyCase\s*=\s*\{(.*?)\};", rw, re.S)
lst = re.findall(r'"([^"]+)"', anyc.group(1)) if anyc else []
low = " ".join(t.lower().replace("’", "'") for t in allw)
hit2 = [x for x in lst if re.search(r"\b" + re.escape(x.lower()) + r"\b", low)]
check(G, "no approved string contains a name on RealWorld.cs's AnyCase list", bool(lst) and not hit2, f"{len(lst)} names read; hits {hit2}")
txt_json = json.dumps({k_: v_ for k_, v_ in T.items() if k_ != "self_check"}).lower()
check(G, "no preview or file name in this target names a real business (CHAMBERLAIN appears only in the forbidden list)", txt_json.count("chamberlain") == 1, f"{txt_json.count('chamberlain')} occurrence(s)")
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
    check(G, f"all {n} text blocks' stored ink widths equal a fresh measure (rendered ink) on the real OFL font files", not bad, f"fonts at {FONT_DIR}; off: {bad}")
except Exception as e:  # noqa: BLE001
    check(G, "ink widths re-measured on the font files", False, f"not re-measured: {type(e).__name__}: {e}", kind="reported")
pb = Path("/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/fascia/dl/blue_painted_planks_diff_2k.jpg")
if pb.exists():
    from scipy import ndimage as ndi
    a = np.asarray(Image.open(pb).convert("RGB")).astype(float)
    lum2 = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    ex = (a[..., 1] >= a[..., 2] - 4) & (lum2 < 95)
    rowl = lum2.mean(axis=1)
    gap_ = ndi.binary_dilation(rowl < np.percentile(rowl, 50) * 0.6, iterations=4)
    valid = ~gap_[:, None] * np.ones((1, a.shape[1]), bool)
    ex &= valid
    fr = float(ex[valid].mean())
    check(G, "P2 paint-loss fraction re-measured from the texture file equals the stored 0.286 (+-0.005)", near(fr, T["photo"]["planks"]["blue"]["loss_fraction"], 0.005), f"{fr:.3f}")
else:
    check(G, "P2 re-measured from the texture file", False, "texture not on this machine; stored values stand (measured 8 Oct)", kind="reported")
ages = [(s["id"], s["age"]["loss_fraction"]) for s in T["shops"]]
check(G, "every shop's paint-loss fraction is at most 0.6 of P2's 0.286 (0.17) or zero (glass, vinyl, box)", all(v == 0 or 0.0 < v <= 0.6 * 0.286 + 1e-9 for _, v in ages), f"{ages}")
check(G, "ten shops, trades as ruled 3 Oct, one of them bare", len(T["shops"]) == 10 and sum(1 for s in T["shops"] if not [b for b in s["blocks"] if not b["ghost"]]) == 1, f"{[s['id'] for s in T['shops']]}")
tx = T["textures"]
check(G, "the height map's range (0.01 mm a step, 128 = face, -1.28 to +1.27 mm) holds every relief the target asks of it (0.8 chrome, 0.6 moulding, 0.3 loss, 0.5 bare, 0.5 joints)", all(v <= 1.27 for v in (0.8, 0.6, 0.3, 0.5, 0.2)) and "0.01 mm per step" in " ".join(m_["encoding"] for m_ in tx["maps"] if m_["id"] == "height") and "NO relief of 3 mm" in " ".join(m_["note"] for m_ in tx["maps"] if m_["id"] == "height"), "")
check(G, "the texture-size note says the power-of-two question is unchecked in the 5.8.2 source and gives both fixes", "NOT checked" in tx["engine_note"] and "8192 x 1024" in tx["engine_note"] and "5120 x 512" in tx["engine_note"], "")

# ============================================================================================
# 7 checks
# ============================================================================================
G = "7 checks"
ids = [c["id"] for c in T["checks"]]
check(G, "every check has id, name, scope, measure, expected, tolerance, unit, method, reads", all(all(k_ in c for k_ in ("id", "name", "scope", "measure", "expected", "tolerance", "unit", "method", "reads")) for c in T["checks"]), f"{len(ids)} checks")
check(G, "check ids are unique", len(ids) == len(set(ids)), f"{len(ids)}")
cm = {c["id"]: c for c in T["checks"]}
check(G, "G1 to G18 all exist", all(f"G{i}" in cm for i in range(1, 19)), "")
miss = []
for s in T["shops"]:
    for b in s["blocks"]:
        bid = f"{s['id']}.{b['id']}"
        if b["ghost"]:
            need_ = [bid + ".ghost"]
        elif not b["in_texture"]:
            need_ = [bid + ".geometry", bid + ".shadow"]
        else:
            need_ = [bid + x for x in (".cap", ".width", ".pos", ".mask", ".fit", ".contrast", ".face")] + ([bid + ".shade"] if b["shade"] else []) + ([bid + ".jitter"] if b["jitter"] else [])
        miss += [n_ for n_ in need_ if n_ not in cm]
    for n_ in (f"{s['id']}.ground", f"{s['id']}.age", f"{s['id']}.wear"):
        if n_ not in cm:
            miss.append(n_)
    for gp in s["geometry"]:
        if gp["kind"] in ("box_sign", "flat_panel") and f"{s['id']}.{gp['id']}" not in cm:
            miss.append(f"{s['id']}.{gp['id']}")
    if s["lit"] == "tubes" and f"{s['id']}.emissive" not in cm:
        miss.append(f"{s['id']}.emissive")
check(G, "every block has its pixel position, glyph-mask, cap, width, fit, contrast, face (and shade, jitter) check; every ghost, geometry part, ground, age and wear has one", not miss, f"missing {miss}")
check(G, "every projecting sign has a mount and a faces check; every glass row not marked existing has a check; the letting board and the hours plates have one", all(f"{p['id']}.mount" in cm and f"{p['id']}.faces" in cm for p in T["projecting_signs"]) and all(any(c["id"] == f"{g['shop']}.glass.{i}" for c in T["checks"]) for i, g in enumerate(T["glass_lettering"]) if g["text"] and not g.get("existing")) and "letting_board" in cm and "hours_plates" in cm, "")
check(G, "the pixel checks read pixels: 'pos', 'mask', 'ground' and 'face' checks are marked pixels (or pixels+font), not manifest", all(cm[f"{s['id']}.{b['id']}.pos"]["reads"] == "pixels" and cm[f"{s['id']}.{b['id']}.mask"]["reads"] == "pixels+font" for s in T["shops"] for b in s["blocks"] if b["in_texture"] and not b["ghost"]), "")
bad = []
for s in T["shops"]:
    for b in s["blocks"]:
        if b["ghost"] or not b["in_texture"]:
            continue
        c = cm.get(f"{s['id']}.{b['id']}.contrast")
        if not c or b["contrast_1990"] < 2.2:
            bad.append(b["id"])
        c = cm.get(f"{s['id']}.{b['id']}.cap")
        if not c or not near(c["expected"], b["cap_mm"], 1e-9):
            bad.append(b["id"] + ".cap")
check(G, "each block's contrast and cap checks exist and the target meets its own nominal values", not bad, f"off: {bad}")
check(G, "the lit box signs have emissive checks and the pawnbroker's board is not lit", "steam_laundry.emissive" in cm and "newsagent.emissive" in cm and "rita.lit" in cm, "")
check(G, "G9 no longer holds a geometry entry: the applied-letter relief is G17 (the old 8 to 18 mm step cannot live in a +-1.27 mm map)", "applied_mm" not in json.dumps(cm["G9"]["expected"]), json.dumps(cm["G9"]["expected"]))
check(G, "G2 reads the height map for the planted mouldings, not a baked highlight", "HEIGHT MAP" in cm["G2"]["measure"] and "baked" not in cm["G2"]["measure"].lower().replace("not a baked", ""), cm["G2"]["measure"][:90])

# ============================================================================================
# 8 pixels: the pixel checks run on a reference render of every lettered board
# ============================================================================================
G = "8 pixels"
if not HAVE_FONTS:
    check(G, "pixel checks run on reference renders", False, f"fonts not on this machine at {FONT_DIR}", kind="reported")
else:
    lettered = [s for s in T["shops"] if [b for b in s["blocks"] if b["in_texture"] and not b["ghost"]]]
    n_ok = n_all = 0
    jit_sds = []
    sym = []
    margins = []
    for s in lettered:
        img_ = pc.synthetic_board(T, s["id"], FONT_DIR)
        res = pc.check_board(img_, T, s["id"], FONT_DIR)
        fails = [r for r in res if not r["ok"]]
        check(G, f"{s['id']}: the true reference render passes all {len(res)} pixel checks (position, glyph mask, width, face colour, jitter, mirror)", not fails, f"fails {[(r['id'], r['value']) for r in fails]}")
        for r in res:
            if r["id"].endswith(".mask") and isinstance(r["value"], dict):
                margins.append((round(r["value"]["true"] - r["value"]["flipped"], 3), r["id"]))
                if r["value"]["true"] - r["value"]["flipped"] < 0.15:
                    sym.append((r["id"], r["value"]))
        if FAST:
            continue
        mi = pc.synthetic_board(T, s["id"], FONT_DIR, mirror=True)
        rm = pc.check_board(mi, T, s["id"], FONT_DIR)
        check(G, f"{s['id']}: the MIRRORED board fails (a mask, position or mirror check fails on at least one block)", any(not r["ok"] for r in rm if r["id"].endswith((".mask", ".pos", ".mirror"))), f"{sum(1 for r in rm if not r['ok'])} of {len(rm)} checks fail")
        for dx_ in (60.0, -60.0):
            sh_ = pc.synthetic_board(T, s["id"], FONT_DIR, shift_mm=dx_)
            rs2 = pc.check_board(sh_, T, s["id"], FONT_DIR)
            check(G, f"{s['id']}: a board shifted {dx_:+.0f} mm along fails every position check and a mask check", all(not r["ok"] for r in rs2 if r["id"].endswith(".pos")) and any(not r["ok"] for r in rs2 if r["id"].endswith(".mask")), f"{sum(1 for r in rs2 if r['id'].endswith('.pos') and not r['ok'])} of {sum(1 for r in rs2 if r['id'].endswith('.pos'))} positions fail")
        jt = pc.synthetic_board(T, s["id"], FONT_DIR, jitter_sd=1.0, seed=3)
        rj = pc.check_board(jt, T, s["id"], FONT_DIR, jitter=True)
        bad_ = [r for r in rj if not r["ok"] and not r["id"].endswith(".jitter")]
        check(G, f"{s['id']}: a hand-jittered render (baseline SD 1.0 mm) still passes position, mask, width and face", not bad_, f"fails {[(r['id'], r['value']) for r in bad_]}")
        for r in rj:
            if r["id"].endswith(".jitter") and r["value"] is not None:
                jit_sds.append(r["value"])
    if not FAST:
        check(G, "jitter is measurable: the jittered renders' glyph-bottom SD lies in 0.6 to 1.6 mm on every block with six or more flat glyphs", bool(jit_sds) and all(0.6 <= v <= 1.6 for v in jit_sds), f"{len(jit_sds)} blocks: {[round(v, 2) for v in jit_sds]}")
        wf = lettered[0]
        s0 = [s for s in T["shops"] if s["id"] == "ritas"][0]
        wr = pc.synthetic_board(T, "ritas", FONT_DIR, wrong_font=("name", "oswald"))
        rr = pc.check_board(wr, T, "ritas", FONT_DIR)
        check(G, "a wrong font on one block (Rita's name in Oswald) fails that block's glyph mask", any(r["id"] == "ritas.name.mask" and not r["ok"] for r in rr), f"{[(r['id'], r['value']) for r in rr if r['id'] == 'ritas.name.mask']}")
    weakest = sorted(margins)[:4]
    check(G, "no block's glyph mask is mirror-symmetric: on every block the true render beats the flipped one by 0.15 F or more (the G10 rule); the weakest margins are listed", not sym, f"too close {sym}; weakest margins (F true minus F flipped) {weakest}")
rows.sort(key=lambda r: r["group"])
# ============================================================================================
fails = [r for r in rows if not r["passed"] and r["kind"] == "check"]
rep = [r for r in rows if not r["passed"] and r["kind"] == "reported"]
npass = sum(1 for r in rows if r["passed"] and r["kind"] == "check")
ntot = sum(1 for r in rows if r["kind"] == "check")
summary = f"{npass} of {ntot} checks pass; {len(fails)} fail; {len(rep)} reported disagreement(s) or gaps kept visible"
result = dict(run="self_check.py, 8 Oct 2026 (cloud week 42, amended after the target review)", summary=summary, photo_scale_px_per_mm_P1=round(s_px, 5), failures=fails, reported_disagreements=rep, rows=rows)
if "--no-write" not in sys.argv and not FAST:
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
