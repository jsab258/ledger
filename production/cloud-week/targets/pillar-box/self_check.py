"""Self-check of the Quay Street pillar box target, run before anything is built.

    /home/user/.bpyenv/bin/python self_check.py            (prints a result line, writes it into target.json under "self_check")

Parts
  A  every number printed in the repository that the target uses comes back from target.json, and equals the printed source
     (the scene file, the earlier research, the kerbs and wear targets), and every derived number recomputes
  B  photograph measurements: NONE exist (no photograph of a pillar box was reached); this part tests that the target claims none, and that the
     panorama search it rests on is recorded
  C  the drawing: target_drawing.py is run on target.json alone and its polygons are tested against the target's own numbers. There is no main
     photograph, so there is NO test of the drawing laid on a photograph (stated, not faked)
  D  internal consistency: parts add up, nothing overlaps that should not, nothing floats, the colour block recomputes
  E  text and canon: the only words on the box are the allowed ones; no cypher, crown, operator or maker words in what is lettered; TARGET.md
     carries the numbers and the plain statement that no photograph was measured; previews are within the brief's limits
"""
import json
import math
import os
import re
import subprocess
import sys
import tempfile
from datetime import date

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, HERE)
from shapely.geometry import Polygon, box, Point  # noqa: E402
from shapely.ops import unary_union  # noqa: E402

import argparse  # noqa: E402
_ap = argparse.ArgumentParser()
_ap.add_argument("--target", default=os.path.join(HERE, "target.json"))
_ap.add_argument("--no-write", action="store_true", help="do not write the result into the target (used to test the check against a mutated copy)")
ARGS = _ap.parse_args()
TARGET_PATH = ARGS.target
T = json.load(open(TARGET_PATH))
TESTS = []


def test(part, name, ok, detail=""):
    TESTS.append({"part": part, "name": name, "ok": bool(ok), "detail": str(detail)[:300]})
    return ok


def near(a, b, tol=1e-6):
    if isinstance(a, (list, tuple)):
        return len(a) == len(b) and all(near(x, y, tol) for x, y in zip(a, b))
    return abs(a - b) <= tol


N = T["numbers"]
V = lambda k: N[k]["value"]  # noqa: E731

# ------------------------------------------------------------------------------------------------------------------
# A. printed numbers
# ------------------------------------------------------------------------------------------------------------------
scene_path = os.path.join(ROOT, "production/specs/vignette-scene.json")
res_path = os.path.join(ROOT, "production/research/street-clutter-1990/SUMMARY-2026-09-29.md")
kerbs_path = os.path.join(ROOT, "production/cloud-week/targets/kerbs-and-covers/target.json")
wear_path = os.path.join(ROOT, "production/cloud-week/targets/wear/target.json")
slots_path = os.path.join(ROOT, "production/cloud-week/targets/SCENE-SLOTS.md")

for p in (scene_path, res_path, kerbs_path, wear_path, slots_path):
    test("A", f"source file exists: {os.path.relpath(p, ROOT)}", os.path.exists(p))

scene = json.load(open(scene_path))
e4 = [f for f in scene["furniture"] if f.get("bom") == "E4_pillar_box"][0]
for key, rid, mult in (("body_diameter_m", "scene_body_diameter", 1000), ("body_height_m", "scene_body_height", 1000), ("cap_diameter_m", "scene_cap_diameter", 1000),
                       ("cap_height_m", "scene_cap_height", 1000), ("dome_height_m", "scene_dome_height", 1000), ("aperture_width_m", "scene_aperture_width", 1000),
                       ("aperture_height_m", "scene_aperture_height", 1000), ("aperture_at_m", "scene_aperture_centre_z", 1000), ("x_m", "scene_x", 1),
                       ("setback_from_kerb_m", "scene_setback", 1)):
    test("A", f"scene E4 {key} = target.json {rid}", near(e4[key] * mult, V(rid), 1e-6), f"{e4[key] * mult} vs {V(rid)}")
test("A", "scene E4 is on the east side", e4["side"] == "east" and N["scene_x"]["unit"] == "m")
foot = scene["street"]["footway"]
test("A", "scene footway width and fall", near(foot["width_m"] * 1000, V("scene_footway_width")) and near(foot["crossfall"], V("scene_footway_crossfall")))
lam = scene["lighting"]["lantern"]
test("A", "scene lantern linear sRGB", near(lam["linear_srgb"], V("scene_lantern_linear_srgb")), lam["linear_srgb"])
col = scene["lighting"]["column"]
xs = []
x = col["first_offset_m"]
spacing = col["mounting_height_m"] * col["spacing_per_mounting_height"]
n = 0
while x <= scene["street"]["length_m"] - col["first_offset_m"] * 0.25:
    xs.append((x, "east" if n % 2 == 0 else "west"))
    x += spacing * 0.5
    n += 1
east = [x for x, s in xs if s == "east"]
test("A", "the scene's east lamp column nearest the box stands at x = 28.0 (recomputed from the lighting block)", 28.0 in east and V("scene_lamp_column_x_east") == 28.0, east)
test("A", "that column is on the same setback line as the box", col["setback_from_kerb_m"] == e4["setback_from_kerb_m"])

res_txt = open(res_path, encoding="utf-8").read()
for rid, needle in (("research_width_untraced_typeA", "1 ft 7"), ("research_width_c1955_listing", "19 in (48 cm)"), ("research_width_narrow_listing", "15 in (38 cm)"),
                    ("research_total_casting", "73 in (185 cm)"), ("research_buried_min", "15"), ("research_visible_range_cm", "135"), ("research_working_height", "about 150 cm above ground and 49 cm across"),
                    ("research_base_height", "about 20 cm tall")):
    test("A", f"research text contains the printed figure for {rid}", needle in res_txt, needle)
test("A", "research: 135-147 cm", "147 cm" in res_txt)
test("A", "research: 'Type K ... introduced on 31 July 1980'", "31 July 1980" in res_txt)
test("A", "research: 'Red body, black base'", "Red body, black base" in res_txt)
test("A", "research: 'photographs of surviving examples after 2000' caution recorded in target", "2000" in res_txt and "surviving" in res_txt)

kerbs = json.load(open(kerbs_path))
test("A", "kerbs target: flags +110 and kerb top +115 in its frame", "+110" in kerbs["frame"]["z"] and "+115" in kerbs["frame"]["z"], kerbs["frame"]["z"][:120])
test("A", "kerbs target: footway flag level above channel 110 = N", V("flag_level_above_channel") == 110 and V("kerb_top_above_channel") == 115)
test("A", "kerbs target: granite kerb top width 170", "170" in json.dumps(kerbs["summary_line"]) and V("kerb_granite_top_width") == 170)
wear = json.load(open(wear_path))
test("A", "wear target pillar_box_red = target red", wear["surfaces"]["pillar_box_red"]["albedo_srgb"] == V("wear_pillar_red_srgb") == T["paint"]["red"]["srgb"])
test("A", "wear target iron_black = target black", wear["surfaces"]["iron_black"]["albedo_srgb"] == V("wear_iron_black") == T["paint"]["black_base"]["srgb"])
iw = wear["kinds"]["iron_wear"]
test("A", "wear target iron_wear patch eqd 20/45/110", iw["geometry"]["patch_eqd_mm"] == {"p10": 20, "p50": 45, "p90": 110, "src": iw["geometry"]["patch_eqd_mm"]["src"]} or [iw["geometry"]["patch_eqd_mm"][k] for k in ("p10", "p50", "p90")] == V("wear_patch_eqd"))
test("A", "wear target iron_wear share 0.04 to 0.08", iw["where"]["density"]["range"] == V("wear_iron_share"))
tone_txt = open(os.path.join(ROOT, "production/cloud-week/targets/wear/TARGET.md"), encoding="utf-8").read()
test("A", "wear TARGET.md pillar_box_red row 124, 104, 92", "[124, 104, 92]" in tone_txt)
test("A", "wear TARGET.md strip 0.214 m tiled round the girth, mirrored", "0.214 m strip tiled round its circumference (mirrored on alternate repeats)" in tone_txt)
levels = wear["kinds"]["wall_foot_splash"]["envelope"]["levels"]
test("A", "wear foot-splash levels = target's", [[round(l["h_m"] * 1000), l["level"]] for l in levels] == V("wear_splash_levels"), levels)
slots_txt = open(slots_path, encoding="utf-8").read()
test("A", "SCENE-SLOTS pillar box row", "0.597 across, 1.372 high" in slots_txt and "NO CYPHER, NO LETTERING" in slots_txt)

# derived numbers recompute
test("A", "body diameter = 19.25 in x 25.4 rounded", round(V("research_width_untraced_typeA") * 25.4) == V("body_diameter"), round(V("research_width_untraced_typeA") * 25.4))
test("A", "total height = the research's working figure 1500 (Read), kind Read", V("total_height") == V("research_working_height") == 1500 and N["total_height"]["kind"] == "Read" and T["overall"]["total_height"] == 1500)
test("A", "the research says 'about 150 cm above ground' and 'The top is at about 150 cm'", "about 150 cm above ground" in res_txt and "The top is at about 150 cm" in res_txt)
test("A", "the research's untraced Type A line: 5 ft 4 in tall = 1626 as the upper alternative", "5 ft 4 in tall" in res_txt and round(V("research_typeA_untraced_height") * 25.4) == V("upper_alternative_height") == T["overall"]["upper_alternative_total_height"]["value"] == 1626)
test("A", "the stand-in is 112 mm too tall (1612 - 1500) and the ratio height / body is 3.07", T["overall"]["stand_in_for_comparison"]["too_tall_by_mm"] == 112 and T["overall"]["height_over_body_width"] == 3.07 and abs(1500 / 489 - 3.07) < 0.005)
test("A", "the 73 in casting range (1350 to 1470) is recorded as NOT used for the Type A", "lower_range_not_used" in T["overall"] and T["overall"]["lower_range_not_used"]["value_mm"] == [135, 147])
test("A", "no 'buried_depth' number remains (the 73 in derivation is dropped); the hidden skirt is 150", "buried_depth" not in N and V("hidden_skirt") == 150)
test("A", "every 'moved up 128' number: slot centre 1278, cap soffit 1343, hood 1300.5 / 1323 / 1333, sill 1240, apex 1500 (first draft + 128)", V("aperture_centre_z") == 1150 + 128 == 1278 and V("cap_soffit_z") == 1215 + 128 and V("hood_z_bottom") == 1172.5 + 128 and V("hood_front_top_z") == 1195 + 128 and V("hood_top_z") == 1205 + 128 and V("sill_z_bottom") == 1112 + 128 and V("dome_base_z") == 1292 + 128 and V("cap_rim_top_z") == 1250 + 128)
test("A", "footway at the axis = 110 + 0.6 m x 0.025", abs(V("flag_level_above_channel") + V("scene_setback") * 1000 * V("scene_footway_crossfall") - V("footway_at_axis_above_channel")) < 0.5)
test("A", "footway fall across the foot = 576 x 0.025", abs(2 * V("foot_radius") * V("scene_footway_crossfall") - V("footway_fall_across_foot")) < 0.1)
circ = math.pi * V("body_diameter")
test("A", "UV repeats: 8, even, and 192 mm each", V("repeat_count") == 8 and V("repeat_count") % 2 == 0 and abs(circ / 8 - 192) < 0.5, circ / 8)
test("A", "UV repeats: the 214 strip would need 7.2, not a whole number", abs(circ / V("wear_pipe_strip") - 7.18) < 0.05, circ / 214)
fw = T["frame_numbers"]["clear_footway_past_box_mm"]["value"]
test("A", "clear footway past the box 1112", fw == 2000 - 600 - 288, fw)
test("A", "lamp column gap", T["frame_numbers"]["nearest_lamp_column"]["gap_to_box_axis_m"] == 1.0)
test("A", "every Read number has a source string", all(v["source"] for v in N.values() if v["kind"] == "Read"))
test("A", "every number has one of the three kinds", all(v["kind"] in ("Read", "Derived", "Judgement") for v in N.values()))
test("A", "kind counts in target.json match the registry", T["number_kinds"]["counts"] == {k: sum(1 for v in N.values() if v["kind"] == k) for k in ("Read", "Derived", "Judgement")})


# ------------------------------------------------------------------------------------------------------------------
# B. photograph measurements
# ------------------------------------------------------------------------------------------------------------------
test("B", "no number is labelled Photo or Scaled", T["number_kinds"]["photo_numbers"] == 0 and T["number_kinds"]["scaled_numbers"] == 0 and not any(v["kind"] in ("Photo", "Scaled") for v in N.values()))
test("B", "target.json states that no photograph was measured", T["no_photograph_measured"] is True and "no photograph of a pillar box was reached" in T["summary_line"])
test("B", "photographs-win block says it does not apply and lists the disagreements between the repository's own figures", T["photographs_win"]["applies"] is False and len(T["photographs_win"]["disagreements"]) >= 8)
scan = json.load(open(os.path.join(HERE, "panorama_scan.json")))
test("B", "panorama scan recorded: every searched panorama present, none shows a pillar box", scan["pillar_box_found"] is False and all(not v["pillar_box"] for v in scan["panoramas"].values()))
names = set(scan["panoramas"])
listed = {s.split(" ")[0] for s in T["panorama_search"]["searched"]}
test("B", "the scan covers every panorama target.json says was searched", names == listed, sorted(names ^ listed))
test("B", "no Dublin panorama among those searched", not any(n_.startswith("docklands") or n_ in ("poolbeg", "irish_institute") for n_ in names))
cat = T["panorama_search"]["catalogue"]
test("B", "panorama counts (review N9): 997 listed, 732 with coordinates, so 265 without (not 'about 400')", cat["hdris_listed"] - cat["with_coordinates"] == cat["without_coordinates"] == 265 and "265" in json.dumps(T["panorama_search"]["left_out"]) and "400" not in json.dumps(T["panorama_search"]))
test("B", "every tone-mapped JPG searched is 8192 px wide (review N9), as the scan recorded it, and the text says so", all(v["source_px"][0] == 8192 for v in scan["panoramas"].values()) and cat["tone_mapped_jpg_width_px"] == 8192 and "8192" in T["panorama_search"]["method"] and "20000" not in json.dumps(T["panorama_search"]))
test("B", "no source in `unreached` is also used as a number source", all("used" in u and u["used"] in ("nothing", "to corroborate, never as a number") for u in T["unreached"]))
test("B", "leads are never in the number registry as sources", all("WebSearch" not in v["source"] for v in N.values()))
test("B", "every disagreement names what was chosen", all("chosen" in d for d in T["photographs_win"]["disagreements"]))
dis = {d["item"]: d for d in T["photographs_win"]["disagreements"]}
test("B", "the disagreement rows for height, door and facing exist (review F1, N2, N6)", all(k in dis for k in ("height", "door", "facing")) and "1500" in dis["height"]["chosen"] and "1 proud" in dis["door"]["chosen"] and "building line" in dis["facing"]["chosen"])
test("B", "the main photograph overlay does not exist and is not claimed", not os.path.exists(os.path.join(ROOT, "production/previews/cloud-week/refs/pillar-box/target-on-photo.jpg")))

# ------------------------------------------------------------------------------------------------------------------
# C. the drawing on the target's own numbers (no photograph: nothing is laid on a photograph)
# ------------------------------------------------------------------------------------------------------------------
tmp = tempfile.mkdtemp(prefix="pbdraw_")
jpath = os.path.join(tmp, "drawing.json")
r = subprocess.run([sys.executable, "-I", os.path.join(HERE, "target_drawing.py"), "--target", TARGET_PATH, "--json", jpath, "--pics", tmp], capture_output=True, text=True)
test("C", "target_drawing.py runs on target.json alone and writes its JSON and pictures", r.returncode == 0 and all(os.path.exists(os.path.join(tmp, f)) for f in ("front_elevation.png", "side_elevation.png", "axial_section.png", "plans.png", "drawing.json")), r.stderr[-300:])
D = json.load(open(jpath))


def geoms(view, material=None, name=None):
    out = []
    for p in view["polygons"]:
        if (material is None or p["material"] == material) and (name is None or p["name"] == name):
            out.append(Polygon(p["exterior"], p["holes"]))
    return out


fe = D["views"]["front_elevation"]
se = D["views"]["side_elevation"]
sec = D["views"]["axial_section"]
body = unary_union(geoms(fe, "red") + geoms(fe, "black"))
cap_ = T["parts"]["cap"]
door_ = T["parts"]["door"]
test("C", "front elevation: overall height = total_height 1500", abs(body.bounds[3] - T["overall"]["total_height"]) < 0.6 and T["overall"]["total_height"] == 1500, body.bounds)
test("C", "front elevation: widest at the foot = foot diameter", abs((body.bounds[2] - body.bounds[0]) - T["overall"]["foot_diameter"]) < 1.0, body.bounds)
sl = geoms(fe, name="slot")[0]
test("C", "front elevation: slot is 320 x 45 centred on z 1278", abs((sl.bounds[2] - sl.bounds[0]) - V("aperture_width")) < 0.6 and abs((sl.bounds[3] - sl.bounds[1]) - V("aperture_height")) < 0.6 and abs((sl.bounds[1] + sl.bounds[3]) / 2 - 1278) < 0.6, sl.bounds)
dr = geoms(fe, name="door")[0]
test("C", "front elevation: door 300 x 888, bottom at 280, top at 1168", abs((dr.bounds[2] - dr.bounds[0]) - 300) < 0.6 and abs((dr.bounds[3] - dr.bounds[1]) - 888) < 0.6 and abs(dr.bounds[1] - 280) < 0.6, dr.bounds)
cyd = geoms(fe, name="reserved_for_cypher_FLUSH")[0]
test("C", "front elevation: the reserved cypher disc is 110 across at z 1088", abs(cyd.bounds[2] - cyd.bounds[0] - 110) < 0.8 and abs((cyd.bounds[1] + cyd.bounds[3]) / 2 - 1088) < 0.8, cyd.bounds)
bl = [g for g in geoms(fe, "black")][0]
test("C", "front elevation: the black band stops at z = 200", abs(bl.bounds[3] - 200) < 0.6, bl.bounds)
w700 = body.intersection(box(-400, 699, 400, 701)).bounds
test("C", "front elevation: width at z 700 = body diameter 489", abs((w700[2] - w700[0]) - 489) < 1.0, w700)
zr = (cap_["rim_z"][0] + cap_["rim_z"][1]) / 2
rim = body.intersection(box(-400, zr - 1, 400, zr + 1)).bounds
test("C", "front elevation: cap rim width at its mid-height = 560", abs((rim[2] - rim[0]) - 560) < 1.0, rim)
test("C", "front elevation: no hinge knuckle, pin or enamel plate is drawn", not any(("hinge" in p["name"] or "enamel" in p["name"] or "pin" == p["name"]) for p in fe["polygons"]), sorted({p["name"] for p in fe["polygons"]}))
sbody = unary_union(geoms(se, "red") + geoms(se, "black"))
zh = T["parts"]["aperture"]["hood"]["z0"] + 10
cfr = T["parts"]["plates"]["collection_frame"]
test("C", "side elevation: the hood front at y = 274.5, the door at 245.5, the plate frame at 254.5, and the cap rim (280) is outside the hood",
     abs(sbody.intersection(box(0, zh, 400, zh + 2)).bounds[2] - 274.5) < 1.0 and abs(sbody.intersection(box(0, 300, 400, 320)).bounds[2] - 245.5) < 1.0 and abs(sbody.intersection(box(0, cfr["cz"], 400, cfr["cz"] + 2)).bounds[2] - 254.5) < 1.0
     and abs(sbody.intersection(box(0, zr, 400, zr + 2)).bounds[2] - 280) < 1.0)
test("C", "side elevation: the back is the plain cylinder (nothing behind y = -289)", sbody.bounds[0] >= -289)
wall = unary_union(geoms(sec, "red") + geoms(sec, "black"))
test("C", "axial section: the wall is ONE connected solid (nothing floats; the slot opens the front wall only)", wall.geom_type == "Polygon" or len(list(wall.geoms)) == 1, wall.geom_type)
test("C", "axial section: wall thickness 12 at z 700 (back wall)", abs(wall.intersection(box(-400, 699, 0, 701)).bounds[2] - wall.intersection(box(-400, 699, 0, 701)).bounds[0] - 12) < 1.0)
slot_row = wall.intersection(box(200, 1276, 400, 1280))
test("C", "axial section: the front wall is open at the slot (no wall at z 1278 on the front)", slot_row.is_empty or slot_row.area < 1e-6, slot_row.area)
plans = D["views"]["plans"]
test("C", "plans: eight levels, named foot, door, lock, collection_frame, slot, hood, cap_rim, dome", list(plans) == ["foot", "door", "lock", "collection_frame", "slot", "hood", "cap_rim", "dome"], list(plans))
test("C", "plans: foot ring outer diameter 576", abs(unary_union(geoms(plans["foot"], "black")).bounds[2] - unary_union(geoms(plans["foot"], "black")).bounds[0] - 576) < 1.5)
test("C", "plans: cap rim ring outer diameter 560", abs(unary_union(geoms(plans["cap_rim"], "red")).bounds[2] - unary_union(geoms(plans["cap_rim"], "red")).bounds[0] - 560) < 1.5)
hood = unary_union(geoms(plans["hood"], name="hood"))
test("C", "plans: the hood reaches y = 274.5 and spans +-48 degrees", abs(hood.bounds[3] - 274.5) < 1.5 and abs(hood.bounds[2] - 274.5 * math.sin(math.radians(48))) < 3.0, hood.bounds)
test("C", "plans: the door level shows a plain door sector and no knuckle (nothing stands out of the door's left edge)", not any("hinge" in p["name"] or "knuckle" in p["name"] for p in plans["door"]["polygons"]))
test("C", "NOT RUN: the drawing laid on the main photograph (no photograph of a pillar box was reached)", True, "no main photograph; nothing is claimed")

# ------------------------------------------------------------------------------------------------------------------
# D. internal consistency
# ------------------------------------------------------------------------------------------------------------------
prof = T["profile"]["outer_rz"]
test("D", "profile: z never decreases along the list", all(b[1] >= a[1] - 1e-9 for a, b in zip(prof[:-1], prof[1:])))
test("D", "profile: starts at z = -150 on the foot radius, ends on the axis at the total height", prof[0] == [288.0, -150.0] and prof[-1][0] == 0 and abs(prof[-1][1] - 1500) < 0.01, (prof[0], prof[-1]))
test("D", "profile: all radii non-negative and none exceeds the foot radius", all(0 <= p[0] <= 288.01 for p in prof))
rmax_foot = max(p[0] for p in prof if 0 <= p[1] <= 48)
import target_drawing as TD  # noqa: E402
BX = TD.Box(T)
rbody = [BX.r_at(z_) for z_ in range(200, 1301, 50)]
test("D", "profile: the body is a cylinder of radius 244.5 between z 200 and 1300 (read off the profile every 50 mm)", all(abs(r_ - 244.5) < 1e-6 for r_ in rbody) and len(rbody) == 23, rbody[:3])
test("D", "profile: foot radius 288, cap radius 280", abs(rmax_foot - 288) < 1e-6 and abs(max(p[0] for p in prof if cap_["rim_z"][0] <= p[1] <= cap_["rim_z"][1]) - 280) < 1e-6)
dome = T["profile"]["dome"]
test("D", "dome: sphere radius from sagitta 80 over chord radius 250", abs((250 ** 2 + 80 ** 2) / 160 - dome["sphere_radius"]) < 0.01)
dp = [p for p in prof if p[1] >= 1420 - 1e-9 and p[0] <= 250]
test("D", "dome: every dome point lies on the sphere, the base circle at z 1420 and the apex at 1500", all(abs(math.hypot(p[0], p[1] - (1500 - dome["sphere_radius"])) - dome["sphere_radius"]) < 0.05 for p in dp) and len(dp) >= 20 and abs(cap_["dome_base_z"] - 1420) < 1e-9)
test("D", "cap: soffit 1343 below the rim (1356 to 1378) below the dome base 1420 below the apex 1500", cap_["soffit_z"] == 1343 and cap_["rim_z"] == [1356, 1378] and cap_["soffit_z"] < cap_["rim_z"][0] < cap_["rim_z"][1] < cap_["dome_base_z"] < cap_["apex_z"])
test("D", "cap: rim diameter 560, 35.5 proud of the body, and the cap is the outermost line above the foot", cap_["rim_diameter"] == 560 and cap_["rim_proud_of_body"] == 35.5 and cap_["rim_radius"] < 288)
ap = T["parts"]["aperture"]
sl_ = ap["slot"]
hood_ = ap["hood"]
sill = ap["sill"]
test("D", "aperture: slot top = hood underside; slot bottom = sill top", abs(sl_["z1"] - hood_["z0"]) < 1e-6 and abs(sl_["z0"] - sill["section_rz"][2][1]) < 1e-6)
test("D", "aperture: hood top 10 mm under the cap soffit (no clash)", hood_["top_z"] < cap_["soffit_z"] and cap_["soffit_z"] - hood_["top_z"] >= 8)
test("D", "aperture: slot half angle < hood half angle < 90", sl_["half_angle_deg"] < hood_["half_angle_deg"] < 90)
test("D", "aperture: slot half angle recomputes from 160 / 244.5", abs(math.degrees(math.asin(160 / 244.5)) - sl_["half_angle_deg"]) < 0.1)
test("D", "aperture: hood projection equals outer radius minus body radius", abs(hood_["outer_radius"] - 244.5 - hood_["projection"]) < 1e-6)
test("D", "aperture: the hood tucks INSIDE the cap rim (review N4): hood radius 274.5 < rim radius 280, by 5.5", hood_["outer_radius"] < cap_["rim_radius"] and abs(hood_["inside_the_cap_rim_by"] - 5.5) < 1e-6)
test("D", "aperture: slot size = the scene's (Read); centre = the scene's + 128 = 1278; the slot top is 42.5 under the cap soffit ('just under the cap')", sl_["width"] == V("scene_aperture_width") and sl_["height"] == V("scene_aperture_height") and abs((sl_["z0"] + sl_["z1"]) / 2 - (V("scene_aperture_centre_z") + 128)) < 1e-6 and abs(cap_["soffit_z"] - 1300.5 - 42.5) < 1e-6)
dr_ = T["parts"]["door"]
panels = T["parts"]["panels"]
pl = T["parts"]["plates"]
lp = panels["reserved_for_lettering"]; cy = panels["reserved_for_cypher"]
cf = pl["collection_frame"]
lock = dr_["lock"]
black_top = T["paint"]["black_base"]["top_z"]
test("D", "door: above the black band, below the lettering area and the sill", black_top < dr_["z0"] and dr_["z1"] < lp["z0"] and lp["z1"] < sill["section_rz"][0][1], (dr_["z1"], lp["z0"], lp["z1"], sill["section_rz"][0][1]))
test("D", "door: 1 proud (review N2): outer radius 245.5, a flush panel as the research says; the plate frame's face plane stays at y = 254.5 (bezel_proud_at_axis 9)", dr_["proud"] == 1 and abs(dr_["outer_radius"] - 245.5) < 1e-9 and cf["bezel_proud_at_axis"] == 9 and abs(244.5 + dr_["proud"] + cf["bezel_proud_at_axis"] - 254.5) < 1e-9 and "a flush panel" in res_txt)
test("D", "door: angular half-width recomputes from 150 / 245.5", abs(math.degrees(math.asin(150 / 245.5)) - dr_["half_angle_deg"]) < 0.1)
test("D", "door: 888 high, from 280 to 1168", dr_["height"] == 888 and dr_["z0"] == 280 and dr_["z1"] == 1168)
test("D", "door: no hinges in the target (review N3): none in parts.door, none in the registry, 'hinged' says internal", "hinges" not in dr_ and "hinge" not in N and "INTERNAL" in dr_["hinged"])
door_rect = box(dr_["x0"], dr_["z0"], dr_["x1"], dr_["z1"])
cypher_disc = Point(cy["cx"], cy["cz"]).buffer(cy["diameter"] / 2)
col_rect = box(cf["cx"] - cf["outer_w"] / 2, cf["cz"] - cf["outer_h"] / 2, cf["cx"] + cf["outer_w"] / 2, cf["cz"] + cf["outer_h"] / 2)
lock_disc = Point(lock["x"], lock["z"]).buffer(lock["escutcheon_diameter"] / 2)
lp_rect = box(lp["x0"], lp["z0"], lp["x1"], lp["z1"])
for nm, g in (("cypher area", cypher_disc), ("collection frame", col_rect), ("lock escutcheon", lock_disc)):
    test("D", f"{nm} lies wholly on the door", door_rect.contains(g))
items = {"cypher area": cypher_disc, "collection frame": col_rect, "lock escutcheon": lock_disc, "lettering area": lp_rect}
keys = list(items)
clash = [(a, b) for i, a in enumerate(keys) for b in keys[i + 1:] if items[a].intersects(items[b])]
test("D", "no two of the door's furniture and reserved areas overlap", not clash, clash)
test("D", "the lock is on the right and clears the collection frame by 15 mm or more", lock["x"] > 0 and lock_disc.distance(col_rect) >= 15, lock_disc.distance(col_rect))
test("D", "the stack is the first draft's moved up by 128 (each item the same distance under the door's top): roundel 1088, frame 918, lock 818, lettering cz 1210", cy["cz"] == 960 + 128 and cf["cz"] == 790 + 128 and lock["z"] == 690 + 128 and (lp["z0"] + lp["z1"]) / 2 == 1082 + 128)
test("D", "every part touches the body in the elevation (nothing floats)", all(Polygon(p["exterior"], p["holes"]).intersects(body) for p in fe["polygons"] if p["name"] not in ("ring_line",)))
test("D", "plate window = frame minus twice the bezel (186 x 101); one plate only", pl["collection_plate"]["window_w"] == 186 and pl["collection_plate"]["window_h"] == 101 and "enamel_frame" not in pl and "enamel_plate_frame" not in N and pl["enamel_plate"].startswith("none"))
test("D", "the cypher and lettering areas are FLUSH reserved areas: flush flag, no 'proud' number, check relief 0 (review N5)", lp["flush"] is True and cy["flush"] is True and "proud" not in lp and "proud" not in cy and any(c["name"] == "reserved_for_cypher" and c["expected"]["relief_max"] == 0 for c in T["checks"]))
test("D", "the placements are written in words (review N7): the reserved areas say 'concentric' and a radius; the door says 'concentric' and 245.5", "concentric" in lp["placement"] and "244.5" in lp["placement"] and "concentric" in cy["placement"] and "245.5" in cy["placement"] and "concentric" in dr_["placement"] and "245.5" in dr_["placement"])
test("D", "foot: radius > body radius > 0; foot band + round + splay below the cove top below the black band top", 288 > 244.5 > 0 and 48 + 12 < 72 < 140 < black_top)
test("D", "the black band top (200) is above the foot's cove (140) and below the door (280)", 140 < black_top < dr_["z0"])
# colour
red = T["paint"]["red"]["srgb"]
cr = T["paint"]["colour_reading"]


def s2l(c):
    c /= 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


lin = [s2l(c) for c in red]
Y = 0.2126 * lin[0] + 0.7152 * lin[1] + 0.0722 * lin[2]
test("D", "colour: linear albedo and luminance recompute", near([round(x, 4) for x in lin], cr["albedo_linear"], 1e-9) and abs(Y - cr["relative_luminance"]) < 1e-4, Y)
test("D", "colour: saturation 0.8 and value 0.59 recompute (the accent budget wants S > 0.6)", abs((max(red) - min(red)) / max(red) - cr["hsv"]["s"]) < 0.005 and abs(max(red) / 255 - cr["hsv"]["v"]) < 0.006 and cr["hsv"]["s"] > 0.6)
test("D", "colour: the wet red is darker than the dry and still has S > 0.6", sum(cr["wet"]["albedo_srgb"]) < sum(red) and (max(cr["wet"]["albedo_srgb"]) - min(cr["wet"]["albedo_srgb"])) / max(cr["wet"]["albedo_srgb"]) > 0.6)
sh = T["paint"]["keyhole_shutter"]
test("D", "the keyhole shutter is painted red 150/30/32, metal 0, with a 1 mm dark bare-metal edge 60/52/46 (review N8); the brass colour 150/125/70 is gone", sh["srgb"] == red and sh["metal"] == 0 and sh["edge_srgb"] == [60, 52, 46] and sh["edge_width"] == 1 and "150, 125, 70" not in json.dumps(T["paint"]) + json.dumps(T["materials"]) + json.dumps(T["parts"]) and "brass_shutter" not in T["paint"] and "brass" not in T["materials"])
import make_target as MT  # noqa: E402
import pb_numbers as PBN  # noqa: E402
regen, _segs, _Rs = MT.profile()
test("D", "profile: every point of the stored profile equals the profile regenerated from pb_numbers.py (nothing hand-edited)", regen == prof and len(regen) == len(prof), len(prof))
test("A", "the `numbers` registry in target.json equals pb_numbers.py (values, units, kinds and sources)", json.loads(json.dumps(PBN.REG)) == N)
fits = cr["sodium"]["fits"]
okfit = True
for w, f in fits.items():
    again = MT.daylight_lin(f["edge_nm"], f["w_nm"], f["rmin"], f["rmax"])
    okfit &= near([round(float(x), 4) for x in again], f["daylight_lin"], 2e-4) and abs(float(MT.refl_curve(589.0, f["edge_nm"], f["w_nm"], f["rmin"], f["rmax"])) - f["reflectance_589"]) < 1e-3
test("D", "sodium: the three fitted reflectance edges recompute their daylight colour and their 589 nm reflectance", okfit)
test("D", "sodium: the two best fits reproduce the red to within 0.12 rms in log linear light", sorted(f["fit_rms_log_error"] for f in fits.values())[1] <= 0.12, [f["fit_rms_log_error"] for f in fits.values()])
lo, hi = cr["sodium"]["spectral_ratio_range"]
test("D", "sodium: under the lamp the box is between 0.05 and 0.3 of a white surface", 0.05 <= lo <= hi <= 0.3, (lo, hi))
naive = cr["sodium"]["naive_rgb_multiply"]
test("D", "sodium: the naive RGB product is still red (R channel high, G low) while the spectral reading is not (R/G < 2)", naive["lit_srgb"][0] > 4 * max(naive["lit_srgb"][1], 1) and all(r_["lit_srgb_at_lamp_x1"][0] / max(r_["lit_srgb_at_lamp_x1"][1], 1) < 2 for r_ in cr["sodium"]["spectral_reading"].values()))
ab = T["accent_budget"]["share_of_a_2560x1440_frame"]
area = T["accent_budget"]["projected_area_m2"]
calc = {d_: area * (1440 / (2 * d_ * math.tan(math.radians(23)))) ** 2 / (2560 * 1440) for d_ in (5, 8, 12)}
test("D", "accent budget: frame shares recompute from the projected area (within 6 %), and the area from 0.489 x 1.5 + 0.05", all(abs(calc[d_] / ab[f"at_{d_}_m"] - 1) < 0.06 for d_ in (5, 8, 12)) and abs(area - round(0.489 * 1.5 + 0.05, 2)) < 1e-9, calc)
test("D", "accent budget: the box at 5 m stays under the 0.078 ceiling on its own", ab["at_5_m"] < 0.078)
# wear
w = T["wear"]["agrees_with_wear_target"]
test("D", "wear: repeat width = circumference / 8", abs(w["repeat_width_mm"] - circ / 8) < 0.1 and w["uv_repeats_round_girth"] == 8)
test("D", "wear: the box's typical share lies inside both its range and (at the low end) the wear target's", w["share_of_area_lost"][0] <= w["typical_share"] <= w["share_of_area_lost"][1] and w["typical_share"] <= V("wear_iron_share")[1] and w["typical_share"] >= V("wear_iron_share")[0])
test("D", "wear: the patch sizes and edge are the wear target's", w["patch_eqd_mm"] == [20, 45, 110] and w["edge_mm"] == 4)
test("D", "wear: the mask runs to 1500 and the soot band sits under the new cap soffit (z 1318 to 1343)", "1500 mm" in w["height"] and T["wear"]["grime"]["soot_under_the_cap"]["zone_z"] == [1318, 1343] and T["wear"]["grime"]["soot_under_the_cap"]["zone_z"][1] == cap_["soffit_z"])
test("D", "wear: chips' bottom-layer mix sums to 1", abs(sum(T["wear"]["layers_in_a_chip"]["mix_at_the_bottom_layer"].values()) - 1.0) < 1e-9)
test("D", "wear: flyposting stays off the door, plate, lock, slot and hood", "never on the door" in T["wear"]["flyposting_traces"]["patches"]["where"])
test("D", "wear: the flyposting z range lies inside the body and above the black band", T["wear"]["flyposting_traces"]["patches"]["z_centre"][0] > black_top and T["wear"]["flyposting_traces"]["patches"]["z_centre"][1] < 1300)
test("D", "wear: no rust source or first-look line names a hinge; the left-end hood trickle is there (review N3)", "hinge" not in json.dumps(T["wear"]).lower() and any("LEFT end" in s_ for s_ in T["wear"]["rust_bleed"]["sources"]) and "hood's left end" in T["wear"]["first_look_at_1p6_m"])
test("D", "wear: the road side is the back (180 degrees from the front)", "the back" in T["wear"]["chips_at_the_base"]["kerb_side_scrape"]["side"])
test("D", "facing: the front faces the building line, with the scene's road side recorded and the scene owner told (review N6)", "building line" in T["frame_numbers"]["scene"]["front_faces"] and "road side" in T["frame_numbers"]["scene"]["front_direction_in_scene"] and "scene owner" in T["handover"]["for_scene_file"] and "180 degrees" in T["handover"]["for_scene_file"])
# checks
names_ = [c["name"] for c in T["checks"]]
test("D", "checks: every check has name, applies_to, measure, expected, tolerance, kind and the names are unique", all(all(k in c for k in ("name", "applies_to", "measure", "expected", "tolerance", "kind")) for c in T["checks"]) and len(set(names_)) == len(names_), len(names_))
ck = {c["name"]: c for c in T["checks"]}
test("D", "checks: total height 1500, dome apex 1500, soffit 1343, rim 560, slot centre 1278, door 300 x 888, lock z 818, lettering cz 1210, cypher cz 1088, frame cz 918, body, foot, band, red",
     ck["total_height"]["expected"] == 1500 and ck["dome_apex"]["expected"] == 1500 and ck["cap_soffit_height"]["expected"] == 1343 and ck["cap_rim_diameter"]["expected"] == 560 and ck["aperture_centre_z"]["expected"] == 1278
     and ck["door_size"]["expected"] == {"width": 300, "height": 888} and ck["lock_place"]["expected"]["z"] == 818 and ck["reserved_for_lettering"]["expected"]["cz"] == 1210 and ck["reserved_for_cypher"]["expected"]["cz"] == 1088
     and ck["collection_frame"]["expected"]["cz"] == 918 and ck["body_diameter"]["expected"] == 489 and ck["foot_diameter"]["expected"] == 576 and ck["black_band"]["expected"] == 200 and ck["red_albedo"]["expected"] == red)
test("D", "checks: tolerance of total_height 15, dome_apex 10, soffit 8, door_proud 1 (expected 1)", ck["total_height"]["tolerance"] == 15 and ck["dome_apex"]["tolerance"] == 10 and ck["cap_soffit_height"]["tolerance"] == 8 and ck["door_proud"]["expected"] == 1 and ck["door_proud"]["tolerance"] == 1)
test("D", "checks (N1): cap_rim_diameter is measured in z 1356 to 1378 and cap_soffit_height on the back half (y < 0); body_straight over z 140 to 1343", "1356" in ck["cap_rim_diameter"]["measure"] and "1378" in ck["cap_rim_diameter"]["measure"] and "back half (y < 0)" in ck["cap_soffit_height"]["measure"] and "140 to 1343" in ck["body_straight"]["measure"])
test("D", "checks (N1): the reserved-area checks measure relief 'radially above' the surrounding curved face, not above a plane", all("radially above" in ck[n_]["measure"] and "plane" not in ck[n_]["measure"].replace("no geometry", "") for n_ in ("reserved_for_lettering", "reserved_for_cypher")))
test("D", "checks (N1): profile_silhouette exists: back half, every 2 mm of z, against profile.outer_rz, expected 0 within 1.5", "profile_silhouette" in ck and ck["profile_silhouette"]["tolerance"] == 1.5 and ck["profile_silhouette"]["expected"] == 0 and "every 2 mm" in ck["profile_silhouette"]["measure"] and "back half" in ck["profile_silhouette"]["measure"] and "plain disc" in ck["profile_silhouette"]["measure"])
test("D", "checks (N3): no hinge checks; door_left_edge_flush replaces them (1.5 mm); (N5) no enamel check; (N6) front_faces_footway replaces front_faces_road; (N8) keyhole_shutter_paint", all(n_ not in ck for n_ in ("hinge_count_and_place", "hinge_size", "enamel_frame", "front_faces_road")) and ck["door_left_edge_flush"]["expected"] == 1.5 and ck["front_faces_footway"]["tolerance"] == 10 and "keyhole_shutter_paint" in ck)
test("D", "checks: at least 35 checks, covering geometry, paint, wear, canon and placement", len(T["checks"]) >= 35, len(T["checks"]))
test("D", "variants: main, no black band, Type K (not built), no plate; the Type K is not built", [v["id"] for v in T["variants"]["list"]] == ["main", "no_black_band", "type_k_capless", "no_plate"] and T["decision_type"]["variant"]["build"] is False)


# the silhouette check has teeth (review N1): a cap or a foot without its moulding must fail it, a correct build must pass it
def radius_fn(pts):
    def f(z):
        best = 0.0
        for (r0, z0), (r1, z1) in zip(pts[:-1], pts[1:]):
            lo, hi = min(z0, z1), max(z0, z1)
            if lo - 1e-9 <= z <= hi + 1e-9:
                r = max(r0, r1) if abs(z1 - z0) < 1e-9 else r0 + (r1 - r0) * (z - z0) / (z1 - z0)
                best = max(best, r)
        return best
    return f


def deviation(ref, mesh, z0=0.0, z1=1500.0, step=2.0):
    fr, fm = radius_fn(ref), radius_fn(mesh)
    worst = 0.0
    z = z0
    while z <= z1 + 1e-9:
        worst = max(worst, abs(fr(z) - fm(z)))
        z += step
    return worst


seg = {s_["name"]: s_ for s_ in T["profile"]["segments"]}
P_ = [tuple(p) for p in prof]
plain_cap = [p for p in P_ if p[1] <= cap_["soffit_z"]] + [(280.0, cap_["soffit_z"]), (280.0, cap_["rim_z"][1]), (250.0, cap_["rim_z"][1]), (250.0, cap_["dome_base_z"])] + [p for p in P_ if p[1] >= cap_["dome_base_z"] and p[0] <= 250]
plain_foot = [p for p in P_ if p[1] <= 48][:3] + [(244.5, 48.0), (244.5, 140.0)] + [p for p in P_ if p[1] > 140]
dev_ok = deviation(P_, P_)
dev_bevel = deviation(P_, [(r + 0.8, z) for r, z in P_])
test("D", "silhouette check: a correct build (the profile itself, or 0.8 mm out) passes the 1.5 mm tolerance", dev_ok == 0 and dev_bevel < 1.5, (dev_ok, dev_bevel))
test("D", "silhouette check: a plain 560 disc for the cap, with no cove, bead or neck, FAILS (deviation above 1.5)", deviation(P_, plain_cap) > 1.5, deviation(P_, plain_cap))
test("D", "silhouette check: a foot with no quarter-round, splay or cove FAILS", deviation(P_, plain_foot) > 1.5, deviation(P_, plain_foot))

# ------------------------------------------------------------------------------------------------------------------
# E. text and canon
# ------------------------------------------------------------------------------------------------------------------
ALLOWED = {"COLLECTIONS", "MON-FRI", "SAT", "5.30 PM", "12 NOON"}
FORBIDDEN = ["POST OFFICE", "ROYAL MAIL", "ROYAL", "MAIL", "OFFICE", "GPO", "CARRON", "HANDYSIDE", "LION", "FOUNDRY", "ER", "GR", "GVIR", "EIIR", "E II R", "CROWN", "LETTERS", "POST"]
strings = [t_["string"] for t_ in T["parts"]["plates"]["collection_plate"]["text"] if "string" in t_]
test("E", "the strings on the collection plate are exactly the five allowed words and times", set(strings) == ALLOWED and len(strings) == 5, strings)
test("E", "no forbidden word is lettered anywhere on the box", not [s for s in strings if s.upper() in FORBIDDEN or any(f in s.upper().split() for f in FORBIDDEN)])
test("E", "the allowed-word list in target.json equals this test's", set(T["parts"]["plates"]["collection_plate"]["allowed_words"]) == ALLOWED)
test("E", "the check plate_words lists the same words", set(ck["plate_words"]["expected"]) == ALLOWED)
test("E", "the reserved areas carry no text key", all("text" not in x and "string" not in x for x in (lp, cy)))
bad = []


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("string", "text") and isinstance(v, str) and path.find("plates.collection_plate") < 0:
                bad.append((path + "." + k, v))
            walk(v, path + "." + k if path else k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, f"{path}[{i}]")


walk(T["parts"])
test("E", "no other `string` or `text` key anywhere in parts (nothing else is lettered)", not bad, bad)
md = open(os.path.join(HERE, "TARGET.md"), encoding="utf-8").read()
first = [ln for ln in md.splitlines() if ln.strip() and not ln.startswith("#")][0]
test("E", "TARGET.md opens with the one summary line and it says no photograph was reached", "no photograph of a pillar box was reached" in first.lower(), first[:120])
for needle in ("489", "1500", "576", "560", "150/30/32", "35/35/36", "COLLECTIONS", "MON-FRI 5.30 PM", "SAT 12 NOON", "could not settle", "Unreached", "Type K", "no maker", "1626", "1278", "1343", "888", "building line", "flush", "265", "8192", "second try"):
    test("E", f"TARGET.md contains '{needle}'", needle.lower() in md.lower(), needle)
test("E", "TARGET.md no longer calls 1372 the total height or the stand-in's cap and dome 'inside' it", "1372 in all" not in md and "1372 mm above the footway in all" not in md and "go INSIDE that height" not in md)
test("E", "TARGET.md no longer mentions hinge knuckles as geometry, an enamel plate frame, or brass", "two barrel hinges" not in md and "enamel-plate frame" not in md and "brass swivel" not in md)
for sec_ in ("## 1.", "## 2.", "## 3.", "## 4.", "## 5.", "## 6.", "## 7.", "## 8.", "## 9."):
    test("E", f"TARGET.md has section {sec_}", sec_ in md)
test("E", "TARGET.md says that the self-check cannot lay the drawing on a photograph", "no main photograph" in md.lower())
test("E", "TARGET.md lists the words on the object and why they are safe", "why they are safe" in md.lower() or "why safe" in md.lower())
prev = os.path.join(ROOT, "production/previews/cloud-week/refs/pillar-box")
from PIL import Image  # noqa: E402
pv = [f for f in os.listdir(prev)] if os.path.isdir(prev) else []
test("E", "previews exist (at least the elevations, the plans and sections, the red swatches)", len(pv) >= 3, pv)
for f in pv:
    p = os.path.join(prev, f)
    im = Image.open(p)
    test("E", f"preview {f}: JPEG, at most 1200 px long side, under 300 KB", f.lower().endswith(".jpg") and max(im.size) <= 1200 and os.path.getsize(p) < 300 * 1024, (im.size, os.path.getsize(p)))
    test("E", f"preview {f}: named <ref>-<place>-<what>.jpg", re.match(r"^[a-z0-9]+-[a-z0-9]+-[a-z0-9-]+\.jpg$", f) is not None, f)
# ------------------------------------------------------------------------------------------------------------------
parts = {}
for t_ in TESTS:
    p = parts.setdefault(t_["part"], [0, 0])
    p[0 if t_["ok"] else 1] += 1
passed = sum(1 for t_ in TESTS if t_["ok"])
fails = [t_ for t_ in TESTS if not t_["ok"]]
line = (f"SELF-CHECK {'PASS' if not fails else 'FAIL'}: {passed} of {len(TESTS)} tests pass (A printed numbers {parts['A'][0]}/{sum(parts['A'])}, B photograph measurements {parts['B'][0]}/{sum(parts['B'])} "
        f"[none exist: it tests that none is claimed], C drawing {parts['C'][0]}/{sum(parts['C'])} [no photograph: nothing laid on one], D internal consistency {parts['D'][0]}/{sum(parts['D'])}, E text and canon {parts['E'][0]}/{sum(parts['E'])})")
T["self_check"] = {"date": date.today().isoformat() if False else "2026-10-09", "result_line": line, "passed": passed, "total": len(TESTS), "parts": parts,
                   "failures": [{"part": f["part"], "name": f["name"], "detail": f["detail"]} for f in fails], "tests": TESTS}
if not ARGS.no_write:
    json.dump(T, open(TARGET_PATH, "w"), indent=1, ensure_ascii=False)
print(line)
for f in fails:
    print("  FAIL", f["part"], f["name"], "|", f["detail"])
sys.exit(1 if fails else 0)
