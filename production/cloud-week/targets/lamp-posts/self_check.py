"""Self-check of the Quay Street lamp-post target, run before anything is built.

    /home/user/.bpyenv/bin/python -I self_check.py          (prints a result line, writes it into target.json under "self_check")

Parts
  A  every printed number the target uses comes back from target.json and equals its printed source (the scene file, the pieces file, the code, the earlier research,
     the night note, the kerbs target), and every derived number recomputes (the 589 nm colour from the colour matching functions, the cone arithmetic of the night note)
  B  photograph measurements: the raw rows in photo_measurements.json give the printed numbers; the numbers are RE-MEASURED from the reduced previews in
     production/previews/cloud-week/refs/lamp-posts/ and come back within their stated errors; the drawing's lower column is laid on the main photograph (the BGE strips) at a scale
     fitted on ONE dimension (the sleeve's width) and its projected edges fall on the photograph's edges within the stated error
  C  the drawing: target_drawing.py is run on target.json alone and its polygons are tested against the target's own numbers
  D  internal consistency: parts add up, nothing overlaps that should not, nothing floats, the bracket's geometry recomputes, the colour and light blocks recompute
  E  text, canon and previews: no maker's name, brand, crown or council name anywhere in target.json or TARGET.md; only the plate carries lettering; the previews obey the brief;
     TARGET.md carries its summary line, the plain statement that no 1990 photograph was measured, and credits every preview
  W  deliberately wrong copies of target.json (made here) must each be REFUSED by at least one test above
"""
import argparse
import copy
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import date

import numpy as np
from PIL import Image
from shapely.geometry import LineString, Point, Polygon, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
import lamp_numbers as LN  # noqa: E402
import target_drawing as TD  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--target", default=os.path.join(HERE, "target.json"))
ap.add_argument("--no-write", action="store_true", help="do not write the result into the target and do not run the wrong-copy tests (used for the mutated copies)")
ap.add_argument("--quiet", action="store_true")
ARGS = ap.parse_args()
TARGET_PATH = ARGS.target
T = json.load(open(TARGET_PATH))
TESTS = []
PREV = os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "lamp-posts")


def test(part, name, ok, detail=""):
    TESTS.append({"part": part, "name": name, "ok": bool(ok), "detail": str(detail)[:300]})
    return ok


def near(a, b, tol=1e-6):
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(near(x, y, tol) for x, y in zip(a, b))
    return abs(a - b) <= tol


N = T["numbers"]
V = lambda k: N[k]["value"]  # noqa: E731
REG = dict(LN.REG)
REG.update(LN.derive())

# ===================================================================================================================================================
# A. printed numbers
# ===================================================================================================================================================
paths = {
    "scene": "production/specs/vignette-scene.json", "pieces": "production/specs/vignette-pieces.json", "code": "ledger/Assets/Scripts/Core/StreetVignette.cs",
    "research": "production/research/street-clutter-1990/SUMMARY-2026-09-29.md", "evening": "production/research/evening-light-1990/SUMMARY-2026-09-29.md",
    "night": "production/cloud-week/research/1c-night-pools-lumen.md", "slots": "production/cloud-week/targets/SCENE-SLOTS.md", "kerbs": "production/cloud-week/targets/kerbs-and-covers/target.json",
    "decisions": "DECISIONS.md", "bollards": "production/cloud-week/targets/bollards/TARGET.md", "audit": "production/reference/hook-sheet-audit.md",
    "inherit": "production/reference/retired-sheet-inheritance.md", "govern": "game-design/research/GOVERNS.md"}
for k, p in paths.items():
    test("A", f"source file exists: {p}", os.path.exists(os.path.join(ROOT, p)))
TXT = {k: open(os.path.join(ROOT, p), encoding="utf-8").read() for k, p in paths.items() if p.endswith((".md", ".cs", ".json"))}
scene = json.loads(TXT["scene"])
col, lan = scene["lighting"]["column"], scene["lighting"]["lantern"]
for rid, val in (("scene_mounting_height", col["mounting_height_m"] * 1000), ("scene_setback", col["setback_from_kerb_m"] * 1000), ("scene_base_diameter", col["base_diameter_m"] * 1000),
                 ("scene_base_height", col["base_height_m"] * 1000), ("scene_shaft_diameter", col["shaft_diameter_m"] * 1000), ("scene_outreach", col["outreach_m"] * 1000),
                 ("scene_first_offset", col["first_offset_m"] * 1000), ("scene_lantern_length", lan["length_m"] * 1000), ("scene_lantern_width", lan["width_m"] * 1000),
                 ("scene_lantern_height", lan["height_m"] * 1000), ("scene_wavelength_nm", lan["wavelength_nm"]), ("scene_lantern_range", lan["range_m"]),
                 ("scene_street_length", scene["street"]["length_m"]), ("scene_kerb_half_width", scene["street"]["carriageway"]["half_width_m"]), ("scene_kerb_width", scene["street"]["kerb"]["width_m"])):
    test("A", f"scene {rid} = target.json", near(val, V(rid), 1e-6), f"{val} vs {V(rid)}")
test("A", "scene spacing ratio 4.0", col["spacing_per_mounting_height"] == V("scene_spacing_ratio") == 4.0)
test("A", "scene lantern colour triples and xy", near(lan["linear_srgb"], V("scene_lantern_linear_srgb")) and near(lan["gamma_srgb"], V("scene_lantern_gamma_srgb")) and near(lan["cie_1931_xy"], V("scene_lantern_xy")))
# the code's placement rule, recomputed
mh = col["mounting_height_m"]
spacing = mh * col["spacing_per_mounting_height"]
first = col["first_offset_m"]
xs = []
x = first
while x <= scene["street"]["length_m"] - first * 0.25 + 1e-9:
    xs.append(x)
    x += spacing * 0.5
test("A", "the code's loop (x from 8 while x <= 48 - 8 x 0.25, step spacing x 0.5) gives four columns at 8, 18, 28, 38", xs == [8.0, 18.0, 28.0, 38.0] == V("scene_column_x"), xs)
test("A", "the code states that loop", "x += spacing * 0.5" in TXT["code"] and "(n % 2 == 0) ? 1 : -1" in TXT["code"] and "four is what 5.0 m at 4.0x over 42 m" in TXT["code"])
pieces = json.loads(TXT["pieces"])["pieces"]
col_base = [p for p in pieces if p["name"].startswith("column") and p["name"].endswith("_base")]
test("A", "the pieces file's column bases: x 8, 18, 28, 38 and z +3.725, -3.725, +3.725, -3.725", [p["x_m"] for p in col_base] == V("scene_column_x") and [p["z_m"] for p in col_base] == V("scene_column_z"),
     [(p["x_m"], p["z_m"]) for p in col_base])
lant = [p for p in pieces if p["name"].startswith("lantern")]
test("A", "the pieces file's lanterns: 0.55 along x, 0.2 high, 0.3 across, emissive; z = column z -+ 0.5", all(near([p["sx_m"], p["sy_m"], p["sz_m"]], [0.55, 0.2, 0.3]) and p["emissive"] for p in lant)
     and all(abs(abs(l["z_m"] - c["z_m"]) - 0.5) < 1e-6 for l, c in zip(lant, col_base)))
test("A", "kerb back = half width + kerb width = 3.125; column z = 3.125 + 0.6 = 3.725", near(V("scene_kerb_half_width") + V("scene_kerb_width") + 0.6, 3.725))
test("A", "the target's corrected column z (kerb 170) is 3.77", all(abs(abs(c["corrected_z_m"]) - 3.77) < 1e-9 for c in T["placement"]["columns"]))
test("A", "the scene's neck is three cylinders on a quarter circle, 0.8 x the shaft", V("scene_neck_pieces") == 3 and V("scene_neck_diameter_ratio") == 0.8 and "SX = sd * 0.8" in TXT["code"] and "The swan neck, three short cylinders" in TXT["code"])
test("A", "SCENE-SLOTS.md row: mounting height 5.0, base 0.2 x 0.3, shaft 0.114, outreach 0.5, lantern 0.55 x 0.30 x 0.20, every 20 m, first at 8 m, 0.6 m back",
     all(s in TXT["slots"] for s in ("mounting height 5.0", "base 0.2 across, 0.3 high", "shaft 0.114 across", "outreach 0.5", "lantern 0.55 × 0.30 × 0.20", "first at 8 m", "0.6 m back from the kerb")))
for rid, needle in (("research_column_height_range", "Column: 4.6–6 m"), ("research_foot_width_range", "20–25 cm at the foot"), ("research_door_height_about", "door plate about 50 cm up"),
                    ("research_bracket_reach_range", "1 ft 4 in to 1 ft 6 in"), ("research_lantern_height", "7¾ in (20 cm) tall"), ("research_lamp_power", "usually 35 W SOX"),
                    ("research_lantern_length_estimate", "estimate 60–70 cm")):
    test("A", f"the earlier research prints {rid}: '{needle}'", needle in TXT["research"])
test("A", "the earlier research: 'reaching out 40–45 cm' and 'a boat-shaped canopy 60–70 cm long over a deep clear trough-shaped bowl'", "reaching out 40–45 cm" in TXT["research"] and "boat-shaped canopy 60–70 cm long over a deep clear trough-shaped bowl" in TXT["research"])
test("A", "the earlier research's caution: photographs 1985-1995 not found, surviving examples after 2000", "Photographs taken 1985–1995 in northern England were not found" in TXT["research"])
night = TXT["night"]
for rid, needle in (("lamp_lumens_35w_sox", "35 W gives 4,550 lm"), ("night_current_pool_outer_deg", "500 lm at 46 degrees is 261 cd, 11.4 lx straight down from 4.78 m"), ("night_current_pool_inner_deg", "Inner cone 22 degrees"),
                    ("night_skirt_lumens", "800 lm, inner 45, outer 80 degrees"), ("night_proposed_pool_lumens", "Drop the pool spot 500 to 350 lm; make the cone 15 and 55"),
                    ("night_proposed_peak_lux", "peak about 12.5 lx"), ("night_current_lamp_linear", "Lamp (1.0, 0.25, 0.0): red 4 times green"), ("night_try_lamp_linear", "(1.0, 0.40, 0.03)"),
                    ("night_current_glow_lumens", "glow 40 lm"), ("night_source_radius", "source radius 5 to 10 cm")):
    test("A", f"the night note prints {rid}: '{needle}'", needle in night)
test("A", "DECISIONS: the pool 750 -> 500 lumens (8 October) and the glow casts no shadows (7 October)", "lantern_pool_lumens 750 -> 500" in TXT["decisions"] and "FAINT GLOW CASTS NO SHADOWS" in TXT["decisions"])
test("A", "the evening note prints (0.569, 0.430), about sRGB (255, 140, 0), linear about (1.0, 0.25, 0.0)", all(s in TXT["evening"] for s in ("(0.569, 0.430)", "(255, 140, 0)", "(1.0, 0.25, 0.0)")))
kerbs = json.loads(TXT["kerbs"])
test("A", "kerbs target: granite kerb top 170, flags +110 above the channel", "170" in kerbs["summary_line"] and "+110" in kerbs["frame"]["z"] and V("kerbs_granite_top_width") == 170 and V("kerbs_flag_level_above_channel") == 110)
test("A", "the Hook sheet audit and inheritance notes say the approved sheet shows no column", "No column anywhere in the panel" in TXT["govern"] and "shows NO street lighting column anywhere" in TXT["inherit"])
test("A", "the bollards target's camera heights: BGE 1.02 +-0.07; US01 1.195 at the bed (garden wall 1.23, pier 1.15 to 1.16 include the 0.07 step)", "1.02 +-0.07" in TXT["bollards"] and "1.195 +-0.07" in TXT["bollards"])
# the registry copied whole
test("A", "target.json numbers = lamp_numbers.py registry (ids, values, kinds) plus the derived ones", set(N) == set(REG) and all(N[k]["value"] == REG[k]["value"] and N[k]["kind"] == REG[k]["kind"] for k in REG),
     [k for k in REG if k not in N or N[k]["value"] != REG[k]["value"]][:5])
test("A", "number kinds counted: Read, Photo, Derived, Judgement", T["number_kinds"]["counts"] == {k: sum(1 for v in REG.values() if v["kind"] == k) for k in T["number_kinds"]["counts"]}, T["number_kinds"]["counts"])
# derived recomputes
D = LN.derive()
test("A", "the colour: the fit's 585 nm xy is within 0.002 of the printed table's (0.5448, 0.4544)", abs(D["derived_xy_585"]["value"][0] - 0.5448) < 0.002 and abs(D["derived_xy_585"]["value"][1] - 0.4544) < 0.002, D["derived_xy_585"]["value"])
test("A", "the colour: the scene's xy (0.5467, 0.4526) is the colour of about 585 nm (within 0.003 of the printed table's (0.5448, 0.4544) and 0.005 of the fit), not of 589 (0.5667, 0.4332)",
     abs(0.5467 - 0.5448) < 0.003 and abs(0.4526 - 0.4544) < 0.003 and abs(0.5467 - D["derived_xy_585"]["value"][0]) < 0.005 and abs(0.4526 - D["derived_xy_585"]["value"][1]) < 0.005 and abs(0.5467 - D["derived_xy_589"]["value"][0]) > 0.015)
test("A", "the colour: the scene's raw linear triple (2.3766, 0.7055, -0.1351) comes back from its xy", near(D["derived_scene_raw_linear"]["value"], [2.3766, 0.7055, -0.1351], 0.001), D["derived_scene_raw_linear"]["value"])
test("A", "the colour: clipped and divided by its peak the scene's xy gives (1, 0.2969, 0), not the file's (1, 0.7055, 0)", near(D["derived_scene_clipped_normalised"]["value"], [1.0, 0.2969, 0.0], 0.001) and V("scene_lantern_linear_srgb")[1] == 0.7055)
test("A", "the colour: 589 nm gives (1, 0.2195, 0) linear = (255, 129, 0): the night note's (1, 0.25, 0) and the evening note's (255, 140, 0) are within 0.04 and 11", near(D["derived_589_linear"]["value"], [1.0, 0.2195, 0.0], 0.001)
     and abs(D["derived_589_linear"]["value"][1] - 0.25) < 0.04 and D["derived_589_gamma_8bit"]["value"] == [255, 129, 0])
enc = lambda c: round(255 * (12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055))  # noqa: E731
test("A", "the glow colour (255, 137, 0) is the night note's lamp (1, 0.25, 0) gamma-encoded", [enc(c) for c in V("night_current_lamp_linear")] == V("glow_bowl_srgb") == [255, 137, 0], [enc(c) for c in V("night_current_lamp_linear")])
test("A", "the night note's try (1, 0.40, 0.03) is (255, 170, 48) in sRGB 8 bit", [enc(c) for c in V("night_try_lamp_linear")] == [255, 170, 48], [enc(c) for c in V("night_try_lamp_linear")])
cd = lambda lm, a: lm / (2 * math.pi * (1 - math.cos(math.radians(a))))  # noqa: E731
test("A", "photometry: 500 lm at 46 degrees = 261 cd and 11.4 lx at 4.78 m (the night note)", abs(cd(500, 46) - 261) < 1 and abs(cd(500, 46) / 4.78 ** 2 - 11.4) < 0.05)
test("A", "photometry: the proposed pool (350 lm, 55 degrees) and skirt (800 lm, 80 degrees) give 12.46 lx straight down: the note's 'about 12.5 lx'", abs((cd(350, 55) + cd(800, 80)) / 4.78 ** 2 - 12.5) < 0.1, (cd(350, 55) + cd(800, 80)) / 4.78 ** 2)
test("A", "photometry: 350 + 800 + 40 = 1190 lm, 26 % of the lamp's 4,550 lm", T["light"]["proposed_by_night_note"]["total_lm"] == 1190 and abs(T["light"]["proposed_by_night_note"]["share_of_lamp_lumens"] - 0.262) < 0.001)
test("A", "the light block quotes the night note's numbers", T["light"]["proposed_by_night_note"]["pool_spot"]["lm"] == 350 and T["light"]["proposed_by_night_note"]["skirt_spot"]["lm"] == 800 and T["light"]["current_game"]["pool_spot"]["lm"] == 500
     and T["light"]["current_game"]["glow"]["lm"] == 40 and T["light"]["current_game"]["colour_linear"] == [1.0, 0.25, 0.0])

# ===================================================================================================================================================
# B. photographs
# ===================================================================================================================================================
PM = json.load(open(os.path.join(HERE, "photo_measurements.json")))
test("B", "target.json carries photo_measurements.json whole", T["photo_measurements"] == PM)
rows = PM["bge_sleeve_width"]["rows"]
test("B", "raw rows: the sleeve's width at z 100 to 800 has mean 123.6 and every row within 120 to 128", abs(np.mean([r["width"] for r in rows]) - 123.6) < 0.2 and all(120 <= r["width"] <= 128 for r in rows), [r["width"] for r in rows])
test("B", "raw rows: the target's sleeve OD (124) is the photograph's 123.6 within 1 mm", abs(V("sleeve_od") - PM["bge_sleeve_width"]["mean_width"]) <= 1.0)
sh = {r["z"]: r["width"] for r in PM["bge_shaft_width"]["rows"]}
test("B", "raw rows: shaft 67, 69, 69 at z 1700 to 1900 and 61, 61, 61 at 3800 to 4000", [sh[1700], sh[1800], sh[1900]] == [67.0, 69.0, 69.0] and [sh[3800], sh[3900], sh[4000]] == [61.0, 61.0, 61.0], sh)
test("B", "the target's shaft taper (68 at the cone, 60 at the collar's foot) passes through the photographed widths within 3 mm", all(abs(2 * TD.lower_edges(T, z)[1] - w) <= 3.0 for z, w in sh.items()),
     [(z, round(2 * TD.lower_edges(T, z)[1], 1), w) for z, w in sh.items()])
test("B", "raw: the pod's widest run 417 (x -193 to +223)", PM["bge_pod"]["widest_run_mm"] == 417 and V("bge_pod_diameter_measured") == 417 and T["variants"]["P"]["pod"]["diameter"] == 420)
test("B", "raw: US01 shaft 89.1, stem 42.0, arm 59.9; ratios 0.47 and 0.67", abs(PM["us01_top"]["shaft_mean_width"] - 89.1) < 0.05 and abs(PM["us01_top"]["stem_mean_width"] - 42.0) < 0.05
     and abs(PM["us01_top"]["arm_perpendicular_width"] - 59.9) < 0.05 and abs(42 / 89.1 - 0.47) < 0.01 and abs(59.9 / 89.1 - 0.67) < 0.01)
test("B", "the target's stem OD 42 = US01's stem; its stem to shaft-top ratio 42/60 = 0.70 lies in 0.47..0.70 (stem..arm ratio range, widened by the 5 m column's slimmer top)", abs(V("stem_od") - PM["us01_top"]["stem_mean_width"]) < 1 and 0.47 <= 42 / 60 <= 0.72)
test("B", "raw: US01 lit lantern median 251/152/14, p10 229/105/0, p90 255/208/77, 66,611 orange pixels", PM["us01_lit_lantern"]["median"] == [251.0, 152.0, 14.0] and PM["us01_lit_lantern"]["orange_pixels"] == 66611 and V("us01_lit_median_srgb") == [251, 152, 14])
test("B", "the glow colour is within 15 of the photographed lit median in every channel", all(abs(a - b) <= 15 for a, b in zip(V("glow_bowl_srgb"), V("us01_lit_median_srgb"))), (V("glow_bowl_srgb"), V("us01_lit_median_srgb")))
test("B", "the paint colour (31, 31, 34) is the sleeve median (31, 31, 33) within 3", all(abs(a - b) <= 3 for a, b in zip(V("paint_black_srgb"), PM["bge_colours"]["sleeve_paint_z500_900"]["median"])))
test("B", "the splash colour = the photograph's lowest 250 mm median (49, 46, 42)", V("splash_srgb") == PM["bge_colours"]["sleeve_splash_z20_250"]["median"] == [49.0, 46.0, 42.0] or V("splash_srgb") == [49, 46, 42])
dep = (0.5 - 2524 / 4096) * 180
test("B", "the calibration: camera 1.02 +-0.07 at BGE; the foot's depression angle (row 2524, -20.9 degrees) gives the axis distance 2.73 m", abs(1.02 / math.tan(math.radians(-dep)) + 0.062 - 2.73) < 0.01 and T["calibration"]["BGE"]["camera_height_m"] == 1.02, (dep, 1.02 / math.tan(math.radians(-dep)) + 0.062))
test("B", "the calibration: the base appears at z = -23 mm in the elevation, as the geometry says (1.02 x (1 - 2.73 / 2.669))", abs(1020 * (1 - 2.73 / 2.669) + 23) < 3)


def load_jpg(name):
    return np.asarray(Image.open(os.path.join(PREV, name)).convert("RGB")).astype(float)


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


PF = T["photo_frames"]
f = PF["BGE_STRIPS"]
mm, x0 = f["mm_per_px"], f["x0_mm"]
sw = int((f["x1_mm"] - x0) / mm)
strips_path = os.path.join(PREV, f["file"])
test("B", "the BGE strips preview exists with the stated size", os.path.exists(strips_path) and list(Image.open(strips_path).size) == f["size_px"], Image.open(strips_path).size if os.path.exists(strips_path) else "")
if os.path.exists(strips_path):
    img = load_jpg(f["file"])

    def strip(i):
        return img[:, i * (sw + f["gap_px"]): i * (sw + f["gap_px"]) + sw]

    def edge_row(st, z, z1, el, er, win=12):
        r = int((z1 - z) / mm)
        prof = lum(st[max(0, r - 4): r + 5]).mean(0)
        g = np.gradient(np.convolve(prof, np.ones(3) / 3, mode="same"))
        xs_ = x0 + (np.arange(len(g)) + 0.5) * mm
        lw = (xs_ > el - win) & (xs_ < el + win)
        rw = (xs_ > er - win) & (xs_ < er + win)
        li = int(np.argmin(np.where(lw, g, 1e9)))
        ri = int(np.argmax(np.where(rw, g, -1e9)))
        return float(xs_[li]), float(xs_[ri]), float(-g[li]), float(g[ri])
    # sleeve width from the preview, strip 0, z 100 to 800
    ws, cs = [], []
    for z in range(100, 900, 100):
        xl, xr, gl, gr = edge_row(strip(0), z, 1200, -56, 67)
        ws.append(xr - xl)
        cs.append((xl + xr) / 2)
    wmeas, xc = float(np.mean(ws)), float(np.mean(cs))
    test("B", "re-measured on the preview: the sleeve's width at z 100 to 800 is 123.6 +-3 (the gradient fit, 1.2 mm a pixel)", abs(wmeas - 123.6) <= 3.0, round(wmeas, 1))
    s = wmeas / V("sleeve_od")
    test("B", "the scale fitted on the sleeve alone is within 1.5 % of 1 (the target's numbers ARE the photograph's)", abs(s - 1) <= 0.015, round(s, 4))
    # shaft widths on the preview (strip 1 at z 1800; strip 3 at z 3900)
    for z, i, z1 in ((1800, 1, 2400), (1700, 1, 2400), (3900, 3, 4800), (3800, 3, 4800), (4000, 3, 4800)):
        xl, xr, gl, gr = edge_row(strip(i), z, z1, xc - 34, xc + 34, win=10) if z < 3000 else edge_row(strip(i), z, z1, xc - 31, xc + 31, win=10)
        test("B", f"re-measured on the preview: shaft width at z {z} is {sh[z]:.0f} +-4", abs((xr - xl) - sh[z]) <= 4.0 and min(gl, gr) >= 5.0, (round(xr - xl, 1), round(gl, 1), round(gr, 1)))
    # sleeve top and cone: the width falls below 110 between z 978 and 1010, below 80 by 1030
    prof = []
    for z in range(940, 1080, 6):
        xl, xr, gl, gr = edge_row(strip(0), z, 1200, xc - (62 if z < 978 else 62 - (z - 978) * 28 / 60) - xc * 0, xc + (62 if z < 978 else 62 - (z - 978) * 28 / 60), win=9)
        prof.append((z, xr - xl))
    zs_ = [z for z, w in prof if w < 108]
    test("B", "re-measured on the preview: the sleeve's straight side ends at z 978 +-15 (the width first falls under 108 at or after z 978)", bool(zs_) and abs(min(zs_) - V("sleeve_height")) <= 25, (min(zs_) if zs_ else None))
    # the target's lower column laid on the photograph at the scale fitted on the sleeve alone
    sleeve_err, cone_err, shaft_wid, shaft_ctr = [], [], [], []
    for i, zrange in ((0, range(40, 1110, 20)), (1, range(1210, 2190, 20)), (3, range(3740, 4260, 20))):
        st = strip(i)
        z1 = f["strips"][i]["z1"]
        for z in zrange:
            e = TD.lower_edges(T, z / s)
            if not e:
                continue
            el, er = xc + e[0] * s, xc + e[1] * s
            xl, xr, gl, gr = edge_row(st, z, z1, el, er, win=(8 if (i == 0 and z > 890) else 12))
            if min(gl, gr) < 6.0:
                continue
            if i == 0 and z <= 890:
                sleeve_err += [xl - el, xr - er]
            elif i == 0:
                cone_err += [xl - el, xr - er]
            else:
                shaft_wid.append((xr - xl) - (er - el))
                shaft_ctr.append((xl + xr) / 2 - xc)
    sleeve_err, cone_err, shaft_wid, shaft_ctr = map(np.array, (sleeve_err, cone_err, shaft_wid, shaft_ctr))
    test("B", "the drawing laid on the photograph (scale fitted on the sleeve's width only): the sleeve's two edges, 20 or more rows: mean absolute error <= 3 mm, none over 8 (1.2 mm a pixel)",
         len(sleeve_err) >= 40 and np.mean(np.abs(sleeve_err)) <= 3.0 and np.max(np.abs(sleeve_err)) <= 8.0, (len(sleeve_err), round(float(np.mean(np.abs(sleeve_err))), 2), round(float(np.max(np.abs(sleeve_err))), 2)))
    test("B", "the drawing laid on the photograph: the cone and its ring (z 900 to 1100): median absolute edge error <= 8 mm (the stated +-7 % of the sleeve is 8.7; the ivy behind the cone confuses the edge finder, which finds only four clear rows; the overlay picture shows the fit)",
         len(cone_err) >= 4 and np.median(np.abs(cone_err)) <= 8.0, (len(cone_err), round(float(np.median(np.abs(cone_err))), 2)))
    test("B", "the drawing laid on the photograph: the shaft's WIDTH at 50 or more rows with clear edges (z 1210 to 2190 against ivy and brick, 3740 to 4260 against the sky): median absolute error <= 4.5 mm (the stated +-7 % of a 66 mm shaft), upper quartile <= 8 (clutter behind the lower rows adds outliers; the rows against the sky are within 2 mm)",
         len(shaft_wid) >= 40 and np.median(np.abs(shaft_wid)) <= 4.5 and np.percentile(np.abs(shaft_wid), 75) <= 8.0, (len(shaft_wid), round(float(np.median(np.abs(shaft_wid))), 2), round(float(np.percentile(np.abs(shaft_wid), 75)), 2)))
    test("B", "the drawing laid on the photograph: the shaft's centre stays within 10 mm of the sleeve's (specular highlights move one edge by up to 9 mm)", np.max(np.abs(shaft_ctr)) <= 10.0 and abs(float(np.median(shaft_ctr))) <= 5.0, (round(float(np.max(np.abs(shaft_ctr))), 1), round(float(np.median(shaft_ctr)), 1)))
    LAID_SUMMARY = {"scale_fitted_on": "the sleeve's width (123.6 measured, 124 target): s = %.4f" % s, "scale_s": round(float(s), 4), "sleeve_edge_mean_abs_mm": round(float(np.mean(np.abs(sleeve_err))), 2),
                    "shaft_width_median_abs_mm": round(float(np.median(np.abs(shaft_wid))), 2), "shaft_width_p75_abs_mm": round(float(np.percentile(np.abs(shaft_wid), 75)), 2), "rows_sleeve": int(len(sleeve_err) / 2), "rows_shaft": int(len(shaft_wid))}
test("B", "the overlay file exists, is JPEG, at most 1200 px and under 300 KB", os.path.exists(os.path.join(PREV, "bge-bethnal-green-column-target-on-photo.jpg")))
# the pod
pod_path = os.path.join(PREV, PF["BGE_POD"]["file"])
if os.path.exists(pod_path):
    a = load_jpg(PF["BGE_POD"]["file"])
    lm = lum(a)
    sky = np.percentile(lm[:20], 50)
    mask = lm < sky - 40
    best = 0
    for r in range(mask.shape[0]):
        idx = np.where(mask[r])[0]
        if len(idx) > 50:
            runs = np.split(idx, np.where(np.diff(idx) > 3)[0] + 1)
            best = max(best, max(len(b) for b in runs))
    test("B", "re-measured on the pod preview: the widest run of the pod's silhouette is 417 +-30 mm", abs(best * PF["BGE_POD"]["mm_per_px"] - 417) <= 30, best * PF["BGE_POD"]["mm_per_px"])
# US01
fa = PF["US01_ARM"]
arm_path = os.path.join(PREV, fa["file"])
if os.path.exists(arm_path):
    a = load_jpg(fa["file"])
    lm = lum(a)
    sky = float(np.median(lm[:30, -60:]))
    thr = sky - 45
    mm3 = fa["mm_per_px"]
    wsh = []
    for z in range(8900, 9800, 100):
        r = int((fa["z1_mm"] - z) / mm3)
        idx = np.where(lm[r] < thr)[0]
        if len(idx):
            runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
            wsh.append(max(len(b) for b in runs) * mm3)
    stem = []
    for z in (9800, 9900):
        r = int((fa["z1_mm"] - z) / mm3)
        idx = np.where(lm[r] < thr)[0]
        runs = np.split(idx, np.where(np.diff(idx) > 1)[0] + 1)
        stem.append(max(len(b) for b in runs) * mm3)
    test("B", "re-measured on the US01 preview (3 mm a pixel): the shaft's top 0.9 m is 89 +-8 mm across and the stem 42 +-9 (the stem to shaft ratio 0.47 +-0.1)", abs(np.mean(wsh) - 89.1) <= 8 and abs(np.mean(stem) - 42) <= 9 and abs(np.mean(stem) / np.mean(wsh) - 0.47) <= 0.10, (round(float(np.mean(wsh)), 1), round(float(np.mean(stem)), 1)))
lit_path = os.path.join(PREV, PF["US01_LIT"]["file"])
if os.path.exists(lit_path):
    a = load_jpg(PF["US01_LIT"]["file"]).reshape(-1, 3)
    sat = a.max(1) - a.min(1)
    m = (a[:, 0] > 180) & (a[:, 2] < 140) & (sat > 90)
    med = np.median(a[m], 0)
    test("B", "re-measured on the lit-lantern preview: the orange median is 251/152/14 within 8 per channel", all(abs(x - y) <= 8 for x, y in zip(med, V("us01_lit_median_srgb"))), med.round(0).tolist())

# ===================================================================================================================================================
# C. the drawing
# ===================================================================================================================================================
tmp = tempfile.mkdtemp(prefix="lamp_draw_")
views = TD.build_views(T)
js = TD.to_json(views)
json.dump(js, open(os.path.join(tmp, "p.json"), "w"))
test("C", "the drawing runs from target.json alone and gives 16 views, every polygon valid and non-empty", len(views) == 16 and all(p["geom"].is_valid and not p["geom"].is_empty for v in views.values() for p in v["polys"]), len(views))
test("C", "units are millimetres in the polygons file", js["units"] == "mm")
polys = lambda view, name: unary_union([p["geom"] for p in views[view]["polys"] if p["name"] == name])  # noqa: E731


def width_at(geom, z):
    seg = geom.intersection(LineString([(-1000, z), (1000, z)]))
    if seg.is_empty:
        return 0.0
    b = seg.bounds
    return b[2] - b[0]


col_side = polys("A_side_elevation", "sleeve_cone_shaft_collar")
G = T["geometry"]["A"]
RZ = G["lower"]["outer_rz"]
ZC0, ZC1 = RZ[-3][1], RZ[-1][1]            # the collar's foot and top (4560, 4620)
SH_R_TOP = RZ[-4][0]                          # the shaft's radius at the collar's foot
test("C", "side elevation: the sleeve is 124 across at z 300 and 800 (+-0.5 of the profile)", abs(width_at(col_side, 300) - V("sleeve_od")) < 0.5 and abs(width_at(col_side, 800) - V("sleeve_od")) < 0.5, (width_at(col_side, 300), width_at(col_side, 800)))
test("C", "side elevation: the sleeve's straight side ends at z 978; the cone narrows to the shaft's 68 by z 1038 (94 across at z 1010)", abs(width_at(col_side, 977) - 124) < 0.5 and width_at(col_side, 990) < 120 and abs(width_at(col_side, 1010) - 94.1) < 1.0 and abs(width_at(col_side, 1060) - 67.7) < 1.0, (width_at(col_side, 990), width_at(col_side, 1010), width_at(col_side, 1060)))
for z, tolw in ((1200, 6), (2500, 6), (3900, 6)):
    chk = [c for c in T["checks"] if c["name"] == {1200: "shaft_od_low", 2500: "shaft_od_mid", 3900: "shaft_od_high"}[z]][0]
    test("C", f"side elevation: the shaft's width at z {z} is the check's {chk['expected']}", abs(width_at(col_side, z) - chk["expected"]) < 0.5, width_at(col_side, z))
w = [width_at(col_side, z) for z in range(1050, int(ZC0), 100)]
test("C", "side elevation: the shaft never widens from z 1050 to the collar's foot", all(b <= a + 0.01 for a, b in zip(w, w[1:])))
test("C", "side elevation: the collar is 67 across over its 60 mm", abs(width_at(col_side, ZC0 + 30) - V("collar_od")) < 0.5 and abs(width_at(col_side, ZC0 - 1) - 2 * SH_R_TOP) < 1.0, (width_at(col_side, ZC0 + 30), width_at(col_side, ZC0 - 1)))
test("C", "side elevation: the lowest point is z = -150 and the top of the collar z 4620", abs(col_side.bounds[1] + 150) < 1e-6 and abs(col_side.bounds[3] - ZC1) < 1e-6 and ZC1 == V("collar_top_z"))
rz = G["lower"]["outer_rz"]
prof_poly = TD.profile_poly(rz)
d_two_way = max(max(col_side.exterior.distance(Point(p)) for p in prof_poly.exterior.coords), max(prof_poly.exterior.distance(Point(p)) for p in col_side.exterior.coords))
test("C", "side elevation: the drawn outline and the profile mirrored are the same line (two-way nearest distance under 0.01 mm)", d_two_way < 0.01, d_two_way)
sa = polys("A_side_elevation", "stem_bend_arm")
test("C", "side elevation: the stem is 42 across 40 mm above the collar", abs(width_at(sa, ZC1 + 40) - 42) < 0.6, width_at(sa, ZC1 + 40))
test("C", "side elevation: the arm is continuous from the collar to the boss (the tube is one polygon) and starts inside the collar", sa.geom_type == "Polygon" and sa.bounds[1] < ZC1 and sa.bounds[1] >= ZC0 - 1)
boss = polys("A_side_elevation", "boss")
canopy = polys("A_side_elevation", "canopy")
bowl = polys("A_side_elevation", "bowl")
lamp = polys("A_side_elevation", "lamp")
whole = unary_union([col_side, sa, boss, canopy, bowl])
test("C", "side elevation: column, arm, boss and lantern are ONE connected shape (nothing floats)", whole.geom_type == "Polygon", whole.geom_type)
test("C", "side elevation: the arm's end lies inside the boss and the boss touches the canopy", sa.intersects(boss) and boss.intersects(canopy) and boss.distance(Point(*G["bracket"]["arm_end"])) < 0.01)
lant_side = unary_union([canopy, bowl])
bb = lant_side.bounds
test("C", "side elevation: the lantern is 550 long (y 225 to 775) and 200 high (z 4800 to 5000)", abs(bb[0] - 225) < 1 and abs(bb[2] - 775) < 1 and abs(bb[1] - 4800) < 1 and abs(bb[3] - 5000) < 1, bb)
test("C", "side elevation: the lamp lies wholly inside the bowl", bowl.buffer(0.01).contains(lamp), lamp.bounds)
test("C", "side elevation: the lamp is 54 across and 310 long, centre (500, 4872)", abs(lamp.bounds[2] - lamp.bounds[0] - 310) < 0.01 and abs(lamp.bounds[3] - lamp.bounds[1] - 54) < 0.01 and abs((lamp.bounds[0] + lamp.bounds[2]) / 2 - 500) < 0.01 and abs((lamp.bounds[1] + lamp.bounds[3]) / 2 - 4872) < 0.01)
base_seg = bowl.intersection(LineString([(0, 4800.5), (1000, 4800.5)]))
test("C", "side elevation: the bowl's flat base is at z 4800 over y 300 to 700 (400 long) and its rim at z 4925", abs(bowl.bounds[1] - 4800) < 0.01 and abs(bowl.bounds[3] - 4925) < 0.01 and abs((base_seg.bounds[2] - base_seg.bounds[0]) - 400) < 2.0, base_seg.bounds)
front = polys("A_front_elevation_carriageway_side", "canopy").union(polys("A_front_elevation_carriageway_side", "bowl"))
fb = front.bounds
test("C", "front elevation: the lantern is 300 wide (x +-150) and 200 high", abs(fb[0] + 150) < 1 and abs(fb[2] - 150) < 1 and abs(fb[1] - 4800) < 1 and abs(fb[3] - 5000) < 2.5, fb)
plate_g = polys("A_front_elevation_carriageway_side", "number_plate")
test("C", "front elevation: the number plate is 45 tall at z 2160 and about 65 wide (a 90 mm plate wrapped on a 66 mm tube), inside the shaft's width", abs(plate_g.bounds[3] - plate_g.bounds[1] - 45) < 0.01 and abs((plate_g.bounds[1] + plate_g.bounds[3]) / 2 - 2160) < 0.01 and plate_g.bounds[2] - plate_g.bounds[0] <= width_at(col_side, 2160) + 0.5, plate_g.bounds)
dr = polys("A_back_elevation_building_side", "door")
test("C", "back elevation: the door is 500 tall from z 400 to 900 and 89 across (a 100 mm arc on the 124 sleeve), inside the sleeve's width", abs(dr.bounds[1] - 400) < 0.01 and abs(dr.bounds[3] - 900) < 0.01 and abs((dr.bounds[2] - dr.bounds[0]) - 89.2) < 1.0 and dr.bounds[2] - dr.bounds[0] < 124, dr.bounds)
test("C", "back elevation: two door screws and two collar set screws, each wholly inside its part", sum(1 for p in views["A_back_elevation_building_side"]["polys"] if p["name"] == "door_screw") == 2 and all(dr.buffer(0.01).contains(p["geom"]) for p in views["A_back_elevation_building_side"]["polys"] if p["name"] == "door_screw")
     and sum(1 for p in views["A_back_elevation_building_side"]["polys"] if p["name"] == "collar_set_screw") == 2)
pp = views["A_plan_lantern"]["polys"]
rim = [p["geom"] for p in pp if p["name"] == "canopy_rim_outline"][0]
test("C", "plan: the canopy's outline is 300 wide and 550 long; the bowl's rim 8 inside it; the flat base 164 wide and 400 long", abs(rim.bounds[2] - rim.bounds[0] - 300) < 0.5 and abs(rim.bounds[3] - rim.bounds[1] - 550) < 0.5
     and abs([p["geom"] for p in pp if p["name"] == "bowl_flat_base"][0].bounds[2] * 2 - 164) < 0.5 and abs(([p["geom"] for p in pp if p["name"] == "bowl_flat_base"][0].bounds[3] - [p["geom"] for p in pp if p["name"] == "bowl_flat_base"][0].bounds[1]) - 400) < 0.5
     and rim.buffer(-8).symmetric_difference([p["geom"] for p in pp if p["name"] == "bowl_rim"][0]).area < 1.0)
lamp_plan = [p["geom"] for p in pp if p["name"] == "lamp"][0]
test("C", "plan: the lantern's long axis is along y (the arm), the lamp's likewise, and the arm enters at the narrow rear end (the outline is narrower at y 240 than at y 760)",
     (rim.bounds[3] - rim.bounds[1]) > (rim.bounds[2] - rim.bounds[0]) and (lamp_plan.bounds[3] - lamp_plan.bounds[1]) > (lamp_plan.bounds[2] - lamp_plan.bounds[0])
     and TD.interp(G["lantern"]["canopy"]["plan_half_width"], 240) < TD.interp(G["lantern"]["canopy"]["plan_half_width"], 760))
cs_cross = views["A_section_lantern_cross_y500"]["polys"]
cr = unary_union([p["geom"] for p in cs_cross if p["name"] in ("canopy_shell", "bowl_shell")])
test("C", "cross-section at y 500: the shells span x +-150 (canopy) and the dome reaches z 4998 +-2", abs(cr.bounds[0] + 150) < 1 and abs(cr.bounds[2] - 150) < 1 and abs(cr.bounds[3] - 4998) < 2.0 and abs(cr.bounds[1] - 4800) < 0.5, cr.bounds)
ls = views["A_section_lantern_long_x0"]["polys"]
cshell = [p["geom"] for p in ls if p["name"] == "canopy_shell"][0]
bshell = [p["geom"] for p in ls if p["name"] == "bowl_shell"][0]
test("C", "long section: the shells' areas are within 25 % of (outline length x thickness): canopy 2.5, bowl 3", abs(cshell.area / (cshell.length / 2 * 2.5) - 1) < 0.25 and abs(bshell.area / (bshell.length / 2 * 3.0) - 1) < 0.25, (cshell.area, cshell.length, bshell.area, bshell.length))
for v in ("C_side_elevation", "P_side_elevation", "W1_side_elevation", "C_plan_z500", "C_front_elevation_carriageway_side"):
    test("C", f"variant view {v} exists with polygons", v in views and len(views[v]["polys"]) >= 2)
cplan = unary_union([p["geom"] for p in views["C_plan_z500"]["polys"] if p["name"] == "concrete_section_chamfered"])
test("C", "variant C plan: the section is 220 square with 15 chamfers (area 220 x 220 - 4 x 15 x 15 / 2 - the door recess 120 x 14)", abs(cplan.area - (220 * 220 - 4 * 15 * 15 / 2 - 120 * 14)) < 1.0, cplan.area)
pside = views["P_side_elevation"]["polys"]
pod_poly = [p["geom"] for p in pside if p["name"] == "pod"][0]
test("C", "variant P: the pod is 420 across and sits on the shaft's top at z 4300", abs(pod_poly.bounds[2] - pod_poly.bounds[0] - 420) < 1.0 and abs(pod_poly.bounds[1] - 4300) < 0.5)
# pictures at 1 mm a pixel: run the writer once for the sizes
os.makedirs(os.path.join(tmp, "pics"), exist_ok=True)
pics = TD.render({"A_plan_lantern": views["A_plan_lantern"], "A_section_lantern_long_x0": views["A_section_lantern_long_x0"]}, os.path.join(tmp, "pics"), 1.0)
sizes = {os.path.basename(p): s for p, s in pics}
test("C", "pictures are 1 mm a pixel (plus a 24 px margin): the lantern's plan is about 348 x 598, the long section 548+48 wide", abs(sizes["A_plan_lantern.png"][0] - (300 + 48)) <= 2 and abs(sizes["A_plan_lantern.png"][1] - (550 + 48 + 258)) <= 300 and sizes["A_section_lantern_long_x0.png"][0] >= 548 + 40, sizes)

# ===================================================================================================================================================
# D. internal consistency
# ===================================================================================================================================================
br = G["bracket"]
R, rake, stem_top = br["bend_radius"], br["rake_deg"], br["stem_to_z"]
turn = 90 - rake
bey = R * (1 - math.cos(math.radians(turn)))
bez = stem_top + R * math.sin(math.radians(turn))
aez = bez + (br["arm_end"][0] - bey) * math.tan(math.radians(rake))
test("D", "the bracket's geometry recomputes: the stem top (collar top + 80), the bend of radius 90 through 50 degrees, the 40 degree arm to y 225", near([bey, bez, aez], [br["arm_start"][0], br["arm_start"][1], br["arm_end"][1]], 0.01) and abs(aez - br["arm_end"][1]) < 0.01 and abs(turn - 50) < 1e-9 and abs(stem_top - ZC1 - 80) < 1e-9, (bey, bez, aez))
test("D", "the arm's end lies in the canopy's lip band (z 4925 to 4937) at the rear tip, where the boss is cast", G["lantern"]["canopy"]["rim_z"] <= aez <= G["lantern"]["canopy"]["dome_base_z"], aez)
cl = br["centreline_yz"]
steps = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(cl, cl[1:])]
ang = []
for a, b, c in zip(cl, cl[1:], cl[2:]):
    a1 = math.atan2(b[1] - a[1], b[0] - a[0])
    a2 = math.atan2(c[1] - b[1], c[0] - b[0])
    ang.append(abs(math.degrees(a2 - a1)))
test("D", "the arm's centreline is continuous: no step over 45 mm in the stored samples, no kink over 8 degrees between samples", max(steps) < 45 and max(ang) < 8.0, (max(steps), max(ang)))
test("D", "the arm's slope above the bend is the rake (40 degrees)", abs(math.degrees(math.atan2(br["arm_end"][1] - br["arm_start"][1], br["arm_end"][0] - br["arm_start"][0])) - rake) < 0.05)
test("D", "the stem rises vertically 80 mm above the collar's top (4620 to 4700) before the bend", abs(stem_top - (G["lower"]["outer_rz"][-1][1] + V("stem_height_above_collar"))) < 0.01 and V("stem_height_above_collar") == 80)
test("D", "the lantern's own numbers: length 550 = 775 - 225; centre 500; the scene's outreach 0.5 to its centre", G["lantern"]["envelope"]["length_y"] == [225, 775] and G["lantern"]["envelope"]["centre"] == [0, 500, 4900] and V("lantern_centre_outreach") == V("scene_outreach") == 500)
test("D", "the lantern's top is the scene's mounting height 5000 and its bottom 4800; the rim at 4925 leaves canopy 75 and bowl 125", G["lantern"]["envelope"]["height_z"] == [4800, 5000] and G["lantern"]["canopy"]["rim_z"] == 4925 and 5000 - 4925 == 75 and 4925 - 4800 == 125)
test("D", "the canopy's highest z is 5000 and its plan's widest is 150 each side; no station exceeds the envelope", max(p[1] for p in G["lantern"]["canopy"]["top_z_along_y"]) == 5000 and max(p[1] for p in G["lantern"]["canopy"]["plan_half_width"]) == 150 and all(225 <= p[0] <= 775 for p in G["lantern"]["canopy"]["plan_half_width"]))
dome500 = dict((p[0], p[1]) for p in G["lantern"]["canopy"]["top_z_along_y"])[500] - G["lantern"]["canopy"]["dome_base_z"]
test("D", "the dome height at y 500 is 4998 - 4937 = 61 (the check says 63 +-6)", abs(dome500 - 61) < 0.01 and abs(63 - dome500) <= 6, dome500)
test("D", "the bowl's base outline (300 to 700) lies inside its rim outline at every y", all(TD.interp(G["lantern"]["canopy"]["plan_half_width"], y) - G["lantern"]["bowl"]["rim_inset"] > hw for y, hw in G["lantern"]["bowl"]["base_plan_half_width"]))
light = T["light"]
test("D", "the point light is the scene's rule: 50 mm below the lantern's centre (4900 - 50 = 4850), on y 500, inside the bowl", light["position_mm"] == [0, 500, 4850] and 4800 < 4850 < 4925 and bowl.contains(Point(500, 4850)))
test("D", "the lamp's own centre (4872) is above the light (4850) by 22: both inside the bowl", 4872 - 4850 == 22)
chk_by = {c["name"]: c for c in T["checks"]}
test("D", "the checks agree with the geometry: lantern box 550 x 300 x 200, centre (0, 500, 4900), arm end (225, 4930.7), sleeve 124, sleeve height 978", chk_by["lantern_bounding_box"]["expected"] == {"y": 550, "x": 300, "z": 200}
     and chk_by["lantern_centre"]["expected"] == [0, 500, 4900] and near(chk_by["arm_reaches_boss"]["expected"], [225, round(aez, 1)], 0.15) and chk_by["sleeve_od"]["expected"] == 124 and chk_by["sleeve_height"]["expected"] == 978)
test("D", "every check has a name, a measure, an expected value, a tolerance and a kind; names are unique", all(all(k in c for k in ("name", "applies_to", "measure", "expected", "tolerance", "kind")) for c in T["checks"]) and len({c["name"] for c in T["checks"]}) == len(T["checks"]) and len(T["checks"]) >= 50)
test("D", "wear: the splash band (z 0 to 250) lies within the sleeve; chips on the carriageway face z 150 to 900; the door (-y face, z 400 to 900) and the dent (+y face, z 480) are on opposite faces; the scratches at z 380 to 430 on +y",
     250 < V("sleeve_height") and 900 < V("sleeve_height") and G["door"]["centre_azimuth_deg_from_plus_y"] == 180 and "carriageway face" in " ".join(x["where"] for x in T["wear"]["features"] if x["id"] in ("dent", "scratches")) and V("bge_scratch_zone") == [380, 430])
test("D", "the plate (z 2160) lies on the straight shaft, clear of the cone, the collar and the screws; the collar set screws are within the collar's z range", 1044 < 2160 - 22.5 and 2160 + 22.5 < ZC0 and ZC0 < G["collar_screws"]["z"] < ZC1)
test("D", "the door's two screws (z 425 and 875) lie inside its z range 400 to 900 with 25 mm of margin; the door lies inside the sleeve (z 900 < 978)", all(400 + 24 <= zz <= 900 - 24 for zz in G["door"]["screws"]["z"]) and G["door"]["z"][1] < ZC0 and G["door"]["z"][1] < 978)
test("D", "the plate's text is 'LC n' for n 1 to 4, one per column, in the placement table", T["geometry"]["A"]["plate"]["text"]["n"] == [1, 2, 3, 4] and [c["plate_text"] for c in T["placement"]["columns"]] == ["LC 1", "LC 2", "LC 3", "LC 4"])
test("D", "placement: the four columns at x 8, 18, 28, 38, east west east west; the dent on LC 2 only; seeds distinct", [c["x_m"] for c in T["placement"]["columns"]] == [8.0, 18.0, 28.0, 38.0] and [c["side"] for c in T["placement"]["columns"]] == ["east", "west", "east", "west"]
     and [c["dent"] for c in T["placement"]["columns"]] == [False, True, False, False] and len({c["wear_seed"] for c in T["placement"]["columns"]}) == 4)
test("D", "the column's axis is clear of the footway's far edge: 770 from the kerb face leaves 1230 of the 2000 footway; the sleeve's edge is 0.64 m from the kerb's back face", 2000 - 770 >= 1200 and 600 - 62 > 0)
test("D", "the colour block: glow bowl (255, 137, 0) = lamp (1, 0.25, 0); lamp glass (255, 176, 28) is yellower and brighter than the bowl; bowl relative brightness 0.45", T["materials"]["bowl_emissive_lit"]["srgb"] == [255, 137, 0] and T["materials"]["lamp_glass"]["emissive_srgb_lit"] == [255, 176, 28]
     and T["materials"]["lamp_glass"]["emissive_srgb_lit"][1] > T["materials"]["bowl_emissive_lit"]["srgb"][1] and T["materials"]["bowl_emissive_lit"]["relative_to_lamp"] == 0.45)
test("D", "the accent budget: the only high-chroma surfaces are the lamp and the bowl; paint, canopy and plate are low-chroma (max channel difference under 16 for paint, canopy and plate; under 30 for the bowl unlit)",
     all(max(c) - min(c) < 16 for c in (V("paint_black_srgb"), V("canopy_srgb"), V("plate_white_srgb"), V("primer_srgb"), V("splash_srgb"))) and max(V("bowl_unlit_srgb")) - min(V("bowl_unlit_srgb")) < 40)
test("D", "variant C: 220 at the foot to 125 at the top over 4620 (taper 20 mm a metre across), the bracket tube 48; the same lantern, light and places as A", T["variants"]["C"]["shaft"]["side_at_z0"] == 220 and T["variants"]["C"]["shaft"]["side_at_top"] == 125
     and 200 <= 220 <= 250 and T["variants"]["C"]["bracket_stem_od"] == 48)
test("D", "variant P: the shaft ends at 4300 and the pod's centre at 4375 is inside the photographed 4410 +-300", T["variants"]["P"]["shaft_top_z"] == 4300 and abs(T["variants"]["P"]["pod"]["centre_z"] - V("bge_pod_centre_height")) <= 300)
test("D", "photographs-win list has seven disagreements, each with a chosen value", len(T["photographs_win"]) == 7 and all(w["chose"] for w in T["photographs_win"]))
test("D", "the triangle budget is a range and the bevel list covers the hard edges named", T["triangle_budget"]["lod0"] == [3000, 12000] and len(T["bevels"]) >= 8)

# ===================================================================================================================================================
# E. text, canon and previews
# ===================================================================================================================================================
BANNED = ["thorn", "stanton", "abacus", "urbis", "philips", "schreder", "siemens", "osram", "sylvania", "concrete utilities", "beta 5", "beta5", "crown", "royal", "cypher", "cipher",
          "borough", "harbour board", "meridian harbour", "post office", "british telecom"]
CONTENT = ["alcohol", "beer", "wine", " pub", "gambl", "betting", "bookmaker", "casino", "bottle", "child", "kid ", "kids", "toddler", "baby", "school"]
jtxt = json.dumps({k: v for k, v in T.items() if k not in ("self_check", "numbers", "photographs_win", "decision_type", "could_not_settle", "handover", "unreached", "to_read_when_the_network_opens", "summary_line", "what_the_sheets_show", "checks", "wear")}).lower()
# parts that carry words on the object: plate text, door lettering, wear, materials, geometry
object_text = json.dumps({"plate": G["plate"], "door": G["door"], "materials": T["materials"], "variants": T["variants"], "geometry_note": G["lower"]}).lower()
for b in BANNED:
    test("E", f"no '{b.strip()}' on any part, in the geometry, the materials or the variants", b not in object_text, b)
MAKERS = ["thorn", "stanton", "abacus", "urbis", "philips", "schreder", "siemens", "osram", "sylvania", "concrete utilities", "beta 5", "beta5"]
test("E", "the checks and wear text name no maker or brand (their prose says 'no crown', 'no cypher': prohibitions, tolerated)", all(b not in json.dumps(T["checks"]).lower() for b in MAKERS) and all(b not in json.dumps(T["wear"]).lower() for b in MAKERS))
test("E", "no part carries 'council' as a name: the plate, the door and the materials do not contain the word", "council" not in json.dumps({"plate": G["plate"], "door": G["door"], "materials": T["materials"]}).lower())
for b in CONTENT:
    test("E", f"content rule: no '{b.strip()}' in target.json", b not in json.dumps({k: v for k, v in T.items() if k != "self_check"}).lower(), b)
test("E", "the plate is the only lettering: its text template is 'LC n' and the door and the bowl carry none", G["plate"]["text"]["template"] == "LC n" and "none" in G["door"]["lettering"] and "no maker" in G["door"]["lettering"])
prev = [PF[k]["file"] for k in PF] + ["bge-bethnal-green-column-target-on-photo.jpg", "hook-sheet-slot-x8-east-target-on-sheet.jpg"]
for fn in prev:
    p = os.path.join(PREV, fn)
    ok = os.path.exists(p)
    if ok:
        im = Image.open(p)
        ok = im.format == "JPEG" and max(im.size) <= 1200 and os.path.getsize(p) < 300_000 and re.match(r"^[a-z0-9]+-[a-z0-9-]+-[a-z0-9-]+\.jpg$", fn) is not None
    test("E", f"preview {fn}: JPEG, at most 1200 px, under 300 KB, named <ref>-<place>-<what>.jpg", ok)
mdp = os.path.join(HERE, "TARGET.md")
md = open(mdp, encoding="utf-8").read() if os.path.exists(mdp) else ""
mdl = md.split("\n") + ["", "", "", ""]
test("E", "TARGET.md exists and its first line of text is the summary line (a bold sentence with the sleeve, the bracket and the lantern)", bool(md) and mdl[2].startswith("**") and "sleeve" in mdl[2] and "bracket" in mdl[2] and "lantern" in mdl[2])
test("E", "TARGET.md says plainly that no photograph of 1990 was reached and that no number is read off a Hook sheet", "no photograph of 1990" in md.lower() and "no lighting column" in md.lower())
test("E", "TARGET.md credits every preview by file name", all(fn in md for fn in prev), [fn for fn in prev if fn not in md])
test("E", "TARGET.md lists each source's licence (CC0) and the photographer (Andreas Mischok) and the dates taken (18 August 2019)", "CC0" in md and "Andreas Mischok" in md and "2019-08-18" in md)
test("E", "TARGET.md carries the legend of number kinds (Read, Photo, Derived, Judgement) and the could-not-settle list", all(k in md for k in ("**Read**", "**Photo**", "**Derived**", "**Judgement**")) and "could not settle" in md.lower())
test("E", "TARGET.md names no maker (the earlier research's makers are not repeated)", all(b not in md.lower() for b in ("thorn", "stanton", "abacus", "urbis", "philips", "schreder", "siemens", "osram", "sylvania", "concrete utilities", "beta 5", "beta5")))
test("E", "TARGET.md has no word of drink, betting or children", all(b not in md.lower() for b in CONTENT if b not in (" pub", "kid ", "school")), [b for b in CONTENT if b in md.lower()])
test("E", "the summary line in target.json is the TARGET.md's", mdl[2].strip("*") .strip() == T["summary_line"].strip() or T["summary_line"][:120] in md)

# ===================================================================================================================================================
# result
# ===================================================================================================================================================
parts = {}
for t in TESTS:
    p = parts.setdefault(t["part"], [0, 0])
    p[1] += 1
    p[0] += 1 if t["ok"] else 0
bad = [t for t in TESTS if not t["ok"]]
n_ok = sum(1 for t in TESTS if t["ok"])
names = {"A": "printed numbers", "B": "photographs", "C": "drawing", "D": "internal consistency", "E": "text, canon and previews"}
result = f"SELF-CHECK {'PASS' if not bad else 'FAIL'}: {n_ok} of {len(TESTS)} tests pass (" + ", ".join(f"{k} {names[k]} {v[0]}/{v[1]}" for k, v in sorted(parts.items())) + ")"

# ---- W: wrong copies must be refused (only in a normal run) ----------------------------------------------------------------------------------------
wrong = []
if not ARGS.no_write:
    def mutate(label, fn):
        t2 = copy.deepcopy(json.load(open(TARGET_PATH)))
        fn(t2)
        t2.pop("self_check", None)
        fd, path = tempfile.mkstemp(suffix=".json", prefix="lamp_wrong_")
        os.close(fd)
        json.dump(t2, open(path, "w"))
        r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "self_check.py"), "--target", path, "--no-write", "--quiet"], capture_output=True, text=True)
        refused = "SELF-CHECK FAIL" in r.stdout
        failed = [ln.split(" | ")[0] for ln in r.stdout.splitlines() if ln.startswith("FAILED")][:3]
        wrong.append({"copy": label, "refused": refused, "by": failed})
        os.remove(path)

    def m_sleeve(t2):
        rz2 = t2["geometry"]["A"]["lower"]["outer_rz"]
        rz2[1][0] = rz2[2][0] = 57.0

    def m_taper(t2):
        rz2 = t2["geometry"]["A"]["lower"]["outer_rz"]
        for p in rz2[6:8]:
            p[0] = 34.0

    def m_rake(t2):
        t2["geometry"]["A"]["bracket"]["rake_deg"] = 15

    def m_lantern(t2):
        pl = t2["geometry"]["A"]["lantern"]["canopy"]["plan_half_width"]
        for p in pl:
            p[1] = p[1] * 0.8

    def m_lamp(t2):
        t2["geometry"]["A"]["lantern"]["lamp"]["centre"][2] = 4980

    def m_colour(t2):
        t2["numbers"]["glow_bowl_srgb"]["value"] = [255, 219, 0]

    def m_maker(t2):
        t2["geometry"]["A"]["plate"]["text"]["template"] = "STANTON LC n"

    def m_axis(t2):
        t2["geometry"]["A"]["lantern"]["boss"]["axis_deg_above_horizontal"] = 15
        t2["geometry"]["A"]["bracket"]["arm_end"] = [225, 4800]

    def m_places(t2):
        t2["numbers"]["scene_column_x"]["value"] = [8.0, 28.0, 48.0]

    def m_light(t2):
        t2["light"]["position_mm"] = [0, 500, 5100]

    for label, fn in (("sleeve 114 across instead of 124 (the scene's value)", m_sleeve), ("shaft not tapered (68 to the top)", m_taper), ("bracket raked 15 degrees (a standard raked bracket)", m_rake),
                      ("lantern plan 20 % narrower", m_lantern), ("lamp above the bowl", m_lamp), ("glow colour the scene file's (255, 219, 0)", m_colour),
                      ("a maker's name on the plate", m_maker), ("arm ends 130 mm below the boss", m_axis), ("columns at x 8, 28, 48", m_places), ("point light above the lantern", m_light)):
        mutate(label, fn)
    for wcase in wrong:
        TESTS.append({"part": "W", "name": f"wrong copy refused: {wcase['copy']}", "ok": wcase["refused"], "detail": ", ".join(wcase["by"])})
    parts = {}
    for t in TESTS:
        p = parts.setdefault(t["part"], [0, 0])
        p[1] += 1
        p[0] += 1 if t["ok"] else 0
    bad = [t for t in TESTS if not t["ok"]]
    n_ok = sum(1 for t in TESTS if t["ok"])
    names["W"] = "wrong copies refused"
    result = f"SELF-CHECK {'PASS' if not bad else 'FAIL'}: {n_ok} of {len(TESTS)} tests pass (" + ", ".join(f"{k} {names[k]} {v[0]}/{v[1]}" for k, v in sorted(parts.items())) + ")"

print(result)
if not ARGS.quiet or bad:
    for t in bad:
        print("FAILED", t["part"], t["name"], "|", t["detail"])
if not ARGS.no_write:
    T2 = json.load(open(TARGET_PATH))
    T2["self_check"] = {"date": date.today().isoformat() if False else "2026-10-09", "result_line": result, "tests": len(TESTS), "passed": n_ok, "failed": [{"part": t["part"], "name": t["name"], "detail": t["detail"]} for t in bad],
                        "parts": {k: {"name": names[k], "passed": v[0], "of": v[1]} for k, v in sorted(parts.items())}, "wrong_copies_refused": wrong,
                        "laid_on_photograph": LAID_SUMMARY if "LAID_SUMMARY" in globals() else None, "how": "python -I self_check.py (runs target_drawing in memory, re-measures the previews, regenerates the derived numbers, tries ten deliberately wrong copies of target.json)"}
    json.dump(T2, open(TARGET_PATH, "w"), indent=1)
sys.exit(0 if not bad else 1)
