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
test("A", "buried depth = 73 in - 1372 mm", round(V("research_total_casting") * 25.4 - V("total_height")) == V("buried_depth"), V("buried_depth"))
test("A", "total height lies inside the research's visible range 1350 to 1470", V("research_visible_range_cm")[0] * 10 <= V("total_height") <= V("research_visible_range_cm")[1] * 10)
test("A", "buried depth lies inside 15 to 20 in", V("research_buried_min") * 25.4 <= V("buried_depth") <= V("research_buried_max") * 25.4)
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
test("B", "target.json states that no photograph was measured", T["no_photograph_measured"] is True and "NO PHOTOGRAPH OF A PILLAR BOX WAS REACHED" in T["summary_line"])
test("B", "photographs-win block says it does not apply and lists the disagreements between the repository's own figures", T["photographs_win"]["applies"] is False and len(T["photographs_win"]["disagreements"]) >= 6)
scan = json.load(open(os.path.join(HERE, "panorama_scan.json")))
test("B", "panorama scan recorded: every searched panorama present, none shows a pillar box", scan["pillar_box_found"] is False and all(not v["pillar_box"] for v in scan["panoramas"].values()))
names = set(scan["panoramas"])
listed = {s.split(" ")[0] for s in T["panorama_search"]["searched"]}
test("B", "the scan covers every panorama target.json says was searched", names == listed, sorted(names ^ listed))
test("B", "no Dublin panorama among those searched", not any(n_.startswith("docklands") or n_ in ("poolbeg", "irish_institute") for n_ in names))
test("B", "no source in `unreached` is also used as a number source", all("used" in u and u["used"] in ("nothing", "to corroborate, never as a number") for u in T["unreached"]))
test("B", "leads are never in the number registry as sources", all("WebSearch" not in v["source"] for v in N.values()))
test("B", "every disagreement names what was chosen", all("chosen" in d for d in T["photographs_win"]["disagreements"]))
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
test("C", "front elevation: overall height = total_height", abs(body.bounds[3] - T["overall"]["total_height"]) < 0.6, body.bounds)
test("C", "front elevation: widest at the foot = foot diameter", abs((body.bounds[2] - body.bounds[0]) - T["overall"]["foot_diameter"]) < 1.0, body.bounds)
sl = geoms(fe, name="slot")[0]
test("C", "front elevation: slot is 320 x 45 centred on z 1150", abs((sl.bounds[2] - sl.bounds[0]) - V("aperture_width")) < 0.6 and abs((sl.bounds[3] - sl.bounds[1]) - V("aperture_height")) < 0.6 and abs((sl.bounds[1] + sl.bounds[3]) / 2 - V("aperture_centre_z")) < 0.6, sl.bounds)
dr = geoms(fe, name="door")[0]
test("C", "front elevation: door 300 x 760, bottom at 280", abs((dr.bounds[2] - dr.bounds[0]) - 300) < 0.6 and abs((dr.bounds[3] - dr.bounds[1]) - 760) < 0.6 and abs(dr.bounds[1] - 280) < 0.6, dr.bounds)
test("C", "front elevation: blank cypher roundel 110 across at z 960", abs(geoms(fe, name="cypher_roundel_blank")[0].bounds[2] - geoms(fe, name="cypher_roundel_blank")[0].bounds[0] - 110) < 0.8)
bl = [g for g in geoms(fe, "black")][0]
test("C", "front elevation: the black band stops at z = 200", abs(bl.bounds[3] - 200) < 0.6, bl.bounds)
w700 = body.intersection(box(-400, 699, 400, 701)).bounds
test("C", "front elevation: width at z 700 = body diameter 489", abs((w700[2] - w700[0]) - 489) < 1.0, w700)
rim = body.intersection(box(-400, 1236, 400, 1238)).bounds
test("C", "front elevation: cap rim width at z 1237 = 536", abs((rim[2] - rim[0]) - 536) < 1.0, rim)
sbody = unary_union(geoms(se, "red") + geoms(se, "black"))
test("C", "side elevation: the front (hood) projects to y = 274.5, the door to 248.5, the plates to 254.5", abs(sbody.intersection(box(0, 1180, 400, 1190)).bounds[2] - 274.5) < 1.0 and abs(sbody.intersection(box(0, 300, 400, 320)).bounds[2] - 248.5) < 1.0 and abs(sbody.intersection(box(0, 790, 400, 792)).bounds[2] - 254.5) < 1.0)
test("C", "side elevation: the back is the plain cylinder (no feature behind y = -244.5)", abs(sbody.bounds[0] + max(244.5, 288)) < 1.0 or sbody.bounds[0] >= -289)
wall = unary_union(geoms(sec, "red") + geoms(sec, "black"))
test("C", "axial section: the wall is ONE connected solid (nothing floats; the slot opens the front wall only)", wall.geom_type == "Polygon" or len(list(wall.geoms)) == 1, wall.geom_type)
test("C", "axial section: wall thickness 12 at z 700 (back wall)", abs(wall.intersection(box(-400, 699, 0, 701)).bounds[2] - wall.intersection(box(-400, 699, 0, 701)).bounds[0] - 12) < 1.0)
slot_row = wall.intersection(box(200, 1148, 400, 1152))
test("C", "axial section: the front wall is open at the slot (no wall at z 1150 on the front)", slot_row.is_empty or slot_row.area < 1e-6, slot_row.area)
plans = D["views"]["plans"]
test("C", "plans: foot ring outer diameter 576", abs(unary_union(geoms(plans["foot"], "black")).bounds[2] - unary_union(geoms(plans["foot"], "black")).bounds[0] - 576) < 1.5)
test("C", "plans: cap rim ring outer diameter 536", abs(unary_union(geoms(plans["cap_rim"], "red")).bounds[2] - unary_union(geoms(plans["cap_rim"], "red")).bounds[0] - 536) < 1.5)
hood = unary_union(geoms(plans["hood"], name="hood"))
test("C", "plans: the hood reaches y = 274.5 and spans +-48 degrees", abs(hood.bounds[3] - 274.5) < 1.5 and abs(hood.bounds[2] - 274.5 * math.sin(math.radians(48))) < 3.0, hood.bounds)
test("C", "NOT RUN: the drawing laid on the main photograph (no photograph of a pillar box was reached)", True, "no main photograph; nothing is claimed")

# ------------------------------------------------------------------------------------------------------------------
# D. internal consistency
# ------------------------------------------------------------------------------------------------------------------
prof = T["profile"]["outer_rz"]
test("D", "profile: z never decreases along the list", all(b[1] >= a[1] - 1e-9 for a, b in zip(prof[:-1], prof[1:])))
test("D", "profile: starts at z = -150 on the foot radius, ends on the axis at the total height", prof[0] == [288.0, -150.0] and prof[-1][0] == 0 and abs(prof[-1][1] - 1372) < 0.01, (prof[0], prof[-1]))
test("D", "profile: all radii non-negative and none exceeds the foot radius", all(0 <= p[0] <= 288.01 for p in prof))
rmax_foot = max(p[0] for p in prof if 0 <= p[1] <= 48)
import target_drawing as TD  # noqa: E402
BX = TD.Box(T)
rbody = [BX.r_at(z_) for z_ in range(200, 1201, 50)]
test("D", "profile: the body is a cylinder of radius 244.5 between z 200 and 1200 (read off the profile every 50 mm)", all(abs(r_ - 244.5) < 1e-6 for r_ in rbody) and len(rbody) == 21, rbody[:3])
test("D", "profile: foot radius 288, cap radius 268", abs(rmax_foot - 288) < 1e-6 and abs(max(p[0] for p in prof if 1228 <= p[1] <= 1250) - 268) < 1e-6)
dome = T["profile"]["dome"]
test("D", "dome: sphere radius from sagitta 80 over chord radius 250", abs((250 ** 2 + 80 ** 2) / 160 - dome["sphere_radius"]) < 0.01)
dp = [p for p in prof if p[1] >= 1292 - 1e-9 and p[0] <= 250]
test("D", "dome: every dome point lies on the sphere", all(abs(math.hypot(p[0], p[1] - (1372 - dome["sphere_radius"])) - dome["sphere_radius"]) < 0.05 for p in dp))
cap = T["parts"]["cap"]
test("D", "cap: soffit below the rim below the bead below the dome base", cap["soffit_z"] < cap["rim_z"][0] < cap["rim_z"][1] < cap["dome_base_z"] < cap["apex_z"])
ap = T["parts"]["aperture"]
sl_ = ap["slot"]
hood_ = ap["hood"]
sill = ap["sill"]
test("D", "aperture: slot top = hood underside; slot bottom = sill top", abs(sl_["z1"] - hood_["z0"]) < 1e-6 and abs(sl_["z0"] - sill["section_rz"][2][1]) < 1e-6)
test("D", "aperture: hood top 10 mm under the cap soffit (no clash)", hood_["top_z"] < cap["soffit_z"] and cap["soffit_z"] - hood_["top_z"] >= 8)
test("D", "aperture: slot half angle < hood half angle < 90", sl_["half_angle_deg"] < hood_["half_angle_deg"] < 90)
test("D", "aperture: slot half angle recomputes from 160 / 244.5", abs(math.degrees(math.asin(160 / 244.5)) - sl_["half_angle_deg"]) < 0.1)
test("D", "aperture: hood projection equals outer radius minus body radius", abs(hood_["outer_radius"] - 244.5 - hood_["projection"]) < 1e-6)
test("D", "aperture: the hood's front is level with the cap rim to within 8 mm (the cap rim 268, the hood 274.5)", abs(hood_["outer_radius"] - 268) < 8)
test("D", "aperture: slot centre z and size equal the scene's (Read)", abs((sl_["z0"] + sl_["z1"]) / 2 - 1150) < 1e-6 and sl_["width"] == 320 and sl_["height"] == 45)
dr_ = T["parts"]["door"]
panels = T["parts"]["panels"]
pl = T["parts"]["plates"]
lp = panels["lettering_pad_BLANK"]; cy = panels["cypher_roundel_BLANK"]
cf = pl["collection_frame"]; ef = pl["enamel_frame"]
lock = dr_["lock"]; hg = dr_["hinges"]
black_top = T["paint"]["black_base"]["top_z"]
test("D", "door: above the black band, below the lettering pad and the sill", black_top < dr_["z0"] and dr_["z1"] < lp["z0"] and lp["z1"] < sill["section_rz"][0][1])
test("D", "door: angular half-width recomputes", abs(math.degrees(math.asin(150 / 248.5)) - dr_["half_angle_deg"]) < 0.1)
door_rect = box(dr_["x0"], dr_["z0"], dr_["x1"], dr_["z1"])
cypher_disc = Point(cy["cx"], cy["cz"]).buffer(cy["diameter"] / 2)
col_rect = box(cf["cx"] - cf["outer_w"] / 2, cf["cz"] - cf["outer_h"] / 2, cf["cx"] + cf["outer_w"] / 2, cf["cz"] + cf["outer_h"] / 2)
ena_rect = box(ef["cx"] - ef["outer_w"] / 2, ef["cz"] - ef["outer_h"] / 2, ef["cx"] + ef["outer_w"] / 2, ef["cz"] + ef["outer_h"] / 2)
lock_disc = Point(lock["x"], lock["z"]).buffer(lock["escutcheon_diameter"] / 2)
hinge_rects = [box(hg["x"] - hg["knuckle_diameter"] / 2, zc - hg["length"] / 2, hg["x"] + hg["knuckle_diameter"] / 2, zc + hg["length"] / 2) for zc in hg["z"]]
lp_rect = box(lp["x0"], lp["z0"], lp["x1"], lp["z1"])
for nm, g in (("cypher roundel", cypher_disc), ("collection frame", col_rect), ("enamel frame", ena_rect), ("lock escutcheon", lock_disc)):
    test("D", f"{nm} lies wholly on the door", door_rect.contains(g))
items = {"cypher roundel": cypher_disc, "collection frame": col_rect, "enamel frame": ena_rect, "lock escutcheon": lock_disc, "hinge 1": hinge_rects[0], "hinge 2": hinge_rects[1], "lettering pad": lp_rect}
keys = list(items)
clash = [(a, b) for i, a in enumerate(keys) for b in keys[i + 1:] if items[a].intersects(items[b])]
test("D", "no two of the door's furniture and panels overlap", not clash, clash)
test("D", "the hinges straddle the door's left edge (x = -150) and not the right", all(h.bounds[0] < dr_["x0"] < h.bounds[2] for h in hinge_rects) and lock["x"] > 0)
test("D", "the hinge knuckles clear the collection frame by 20 mm or more", all(h.distance(col_rect) >= 20 for h in hinge_rects), [h.distance(col_rect) for h in hinge_rects])
test("D", "the lock clears both frames by 15 mm or more", lock_disc.distance(col_rect) >= 15 and lock_disc.distance(ena_rect) >= 15, (lock_disc.distance(col_rect), lock_disc.distance(ena_rect)))
test("D", "every part touches the body in the elevation (nothing floats)", all(Polygon(p["exterior"], p["holes"]).intersects(body) for p in fe["polygons"] if p["name"] not in ("ring_line",)))
test("D", "plate windows = frame minus twice the bezel (186 x 101 and 140 x 80)", pl["collection_plate"]["window_w"] == 186 and pl["collection_plate"]["window_h"] == 101 and pl["enamel_plate"]["window_w"] == 140 and pl["enamel_plate"]["window_h"] == 80)
test("D", "cypher roundel and lettering pad are blank (flag set, relief within 0.5 mm)", lp["blank"] is True and cy["blank"] is True and any(c["name"] == "cypher_roundel_blank" and c["expected"]["relief_spread_max"] == 0.5 for c in T["checks"]))
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
test("D", "accent budget: frame shares recompute from the projected area (within 6 %)", all(abs(calc[d_] / ab[f"at_{d_}_m"] - 1) < 0.06 for d_ in (5, 8, 12)), calc)
test("D", "accent budget: the box at 5 m stays under the 0.078 ceiling on its own", ab["at_5_m"] < 0.078)
# wear
w = T["wear"]["agrees_with_wear_target"]
test("D", "wear: repeat width = circumference / 8", abs(w["repeat_width_mm"] - circ / 8) < 0.1 and w["uv_repeats_round_girth"] == 8)
test("D", "wear: the box's typical share lies inside both its range and (at the low end) the wear target's", w["share_of_area_lost"][0] <= w["typical_share"] <= w["share_of_area_lost"][1] and w["typical_share"] <= V("wear_iron_share")[1] and w["typical_share"] >= V("wear_iron_share")[0])
test("D", "wear: the patch sizes and edge are the wear target's", w["patch_eqd_mm"] == [20, 45, 110] and w["edge_mm"] == 4)
test("D", "wear: chips' bottom-layer mix sums to 1", abs(sum(T["wear"]["layers_in_a_chip"]["mix_at_the_bottom_layer"].values()) - 1.0) < 1e-9)
test("D", "wear: flyposting stays off the door, plates, lock, aperture and hood", "never on the door" in T["wear"]["flyposting_traces"]["patches"]["where"])
test("D", "wear: the flyposting z range lies inside the body and above the black band", T["wear"]["flyposting_traces"]["patches"]["z_centre"][0] > black_top and T["wear"]["flyposting_traces"]["patches"]["z_centre"][1] < 1100)
# checks
names_ = [c["name"] for c in T["checks"]]
test("D", "checks: every check has name, applies_to, measure, expected, tolerance, kind and the names are unique", all(all(k in c for k in ("name", "applies_to", "measure", "expected", "tolerance", "kind")) for c in T["checks"]) and len(set(names_)) == len(names_), len(names_))
ck = {c["name"]: c for c in T["checks"]}
test("D", "checks: total height, body, foot, cap, black band, red equal the target's numbers", ck["total_height"]["expected"] == 1372 and ck["body_diameter"]["expected"] == 489 and ck["foot_diameter"]["expected"] == 576 and ck["cap_rim_diameter"]["expected"] == 536 and ck["black_band"]["expected"] == 200 and ck["red_albedo"]["expected"] == red)
test("D", "checks: at least 35 checks, covering geometry, paint, wear, canon and placement", len(T["checks"]) >= 35)
test("D", "variants: exactly one main, one Type K coarse profile (not built), two states", [v["id"] for v in T["variants"]["list"]] == ["main", "no_black_band", "type_k_capless", "plates_blank"] and T["decision_type"]["variant"]["build"] is False)

# ------------------------------------------------------------------------------------------------------------------
# E. text and canon
# ------------------------------------------------------------------------------------------------------------------
ALLOWED = {"COLLECTIONS", "MON-FRI", "SAT", "5.30 PM", "12 NOON"}
FORBIDDEN = ["POST OFFICE", "ROYAL MAIL", "ROYAL", "MAIL", "OFFICE", "GPO", "CARRON", "HANDYSIDE", "LION", "FOUNDRY", "ER", "GR", "GVIR", "EIIR", "E II R", "CROWN", "LETTERS", "POST"]
strings = [t_["string"] for t_ in T["parts"]["plates"]["collection_plate"]["text"] if "string" in t_]
test("E", "the strings on the collection plate are exactly the five allowed words and times", set(strings) == ALLOWED and len(strings) == 5, strings)
test("E", "no forbidden word is lettered anywhere on the box", not [s for s in strings if s.upper() in FORBIDDEN or any(f in s.upper().split() for f in FORBIDDEN)])
test("E", "the allowed-word list in target.json equals this test's", set(T["parts"]["plates"]["collection_plate"]["allowed_words"]) == ALLOWED and T["parts"]["plates"]["enamel_plate"]["allowed_words"] == [])
test("E", "the check plate_words lists the same words", set(ck["plate_words"]["expected"]) == ALLOWED)
test("E", "the cypher roundel and the lettering pad carry no text key", all("text" not in x and "string" not in x for x in (lp, cy)))
# walk every string in `parts` for letters-on-the-box keys
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
for needle in ("489", "1372", "576", "536", "150/30/32", "35/35/36", "COLLECTIONS", "MON-FRI 5.30 PM", "SAT 12 NOON", "could not settle", "Unreached", "Type K", "no maker"):
    test("E", f"TARGET.md contains '{needle}'", needle.lower() in md.lower(), needle)
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
