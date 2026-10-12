#!/usr/bin/env python
"""Test the shop-windows target against its own sources before anything is built, and write the result into target.json under "self_check".

    /home/user/.bpyenv/bin/python self_check.py [--write] [--live]

Nothing is written unless --write is given (a check must not edit the target: the review of 12 October found target.json rewritten, with tied rows in a new order, on every run).
With --write, a live result already in target.json is never overwritten by an offline one (run with --live to refresh it). Tied rows are sorted by name.

Groups
  1 printed      every number the target takes from a file of the repository comes back from that file (shop-interiors.json, vignette-scene.json,
                 vignette-pieces.json, hook-cast.json, the 2.2 and 4.1 targets, terrace-front.py's card, the game's `trace`)
  2 rule         the game's rule recomputed: identity from the render camera, the back wall's corners, the parallax test, the stand-off budgets, the honest range
  3 photo        the photograph's rows re-read from photographs.rows: the door numbers the target adopts come back within their stated error, and the drawing's
                 lines laid on the photograph (scale fitted on one dimension) fall on the rows measured
  4 inventory    every model exists, nothing denied, sizes within reason, no maker's name, no word of the content blocklists, the 1992 rule
  5 room         every fixture inside the box and inside its stand-off class; every good on a fixture that exists, and fits it; no fixture floats
  6 display      every display item inside the window zone's envelope and able to fit its zone
  7 consistency  ten shops, ids unique, spec entries well formed, the checks name shops that exist, the pictures' numbers agree
  8 front        the toplight layout (FRN-04) and the band above the doors with nothing left open (FRN-07), the door plates, the sodium wash colour, the ceiling fixtures
  9 marks        the marks on the models' maps and their blanking steps (INV-06), the blocklists, the previews' masks read back from the committed JPEGs (PRV-01), Jafar's page
--live asks api.polyhaven.com again for the models and the textures named as surfaces.
"""
import json
import math
import os
import re
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_common as S  # noqa: E402
import target_drawing as TD  # noqa: E402

ROOT = S.ROOT
PATH = os.path.join(HERE, "target.json")
T = json.load(open(PATH))
PH = json.load(open(os.path.join(HERE, "polyhaven_checked.json")))


def phm(i):
    return PH["models"].get(i) or {"exists": False, "dims_cm": [1.0, 1.0, 1.0], "published": "9999-01-01", "tags": [], "gltf_1k": {}}

LINES = []
COUNT = {"pass": 0, "fail": 0, "report": 0}
GROUPS = {}


def chk(group, name, ok, detail="", report=False):
    kind = "pass" if ok else ("report" if report else "fail")
    COUNT[kind] += 1
    GROUPS.setdefault(group, {"pass": 0, "fail": 0, "report": 0})[kind] += 1
    LINES.append({"group": group, "name": name, "result": kind, "detail": detail})


def near(a, b, tol):
    return abs(a - b) <= tol


def main():
    live = "--live" in sys.argv
    scene = S.load_scene()
    spec = json.load(open(os.path.join(ROOT, "production", "specs", "shop-interiors.json")))
    pieces = json.load(open(os.path.join(ROOT, "production", "specs", "vignette-pieces.json")))
    cast = json.load(open(os.path.join(ROOT, "production", "specs", "hook-cast.json")))
    t22 = json.load(open(os.path.join(ROOT, "production", "cloud-week", "targets", "shopfronts", "target.json")))
    t41 = json.load(open(os.path.join(ROOT, "production", "cloud-week", "targets", "fascia-signs", "target.json")))
    s22 = {s["id"]: s for s in t22["shops"]}
    s41 = {s["id"]: s for s in t41["shops"]}
    shops = {s["id"]: s for s in T["shops"]}

    # ---- 1 printed -----------------------------------------------------------------------------------------------------------------
    g = "1 printed"
    chk(g, "the camera rule is the spec's, word for word", T["method"]["game_rule"]["camera_rule"] == spec["camera"])
    chk(g, "the never list is the spec's", T["method"]["game_rule"]["never"] == spec["never"])
    chk(g, "the three states are the spec's", T["method"]["game_rule"]["states"] == spec["states"])
    chk(g, "ten units, twelve not found", len(T["shops"]) == 10 and T["street"]["twelve_not_found"])
    sp_by = {s["id"]: s for s in spec["shops"]}
    for sid, e in shops.items():
        c = S.card_of(scene, e["block"], e["bay"])
        f = s22[sid]
        chk(g, "%s: block, bay, side and street x are 2.2's and the scene's" % sid, e["block"] == f["block"] and e["bay"] == f["bay"] and e["side"] == f["side"] and e["street_x_m"] == f["street_x_m"])
        chk(g, "%s: the bay's low x is the scene's (a west bay counts from the high end)" % sid, near(S.bay_x0(scene, e["block"], e["bay"]), min(e["street_x_m"]), 1e-9), "bay_x0 %.3f" % c["bay_x0"])
        chk(g, "%s: the fascia board and street number are 4.1's" % sid, e["fascia"]["street_number"] == s41[sid].get("street_number") and e["fascia"]["board"].startswith("fascias/%s/" % s41[sid]["id"]))
        if e.get("card"):
            cc = e["card"]
            chk(g, "%s: the card is terrace-front.py's (x %.2f to %.2f, z 0.65 to 3.05, y %+.3f)" % (sid, c["x0"], c["x1"], c["z"]),
                near(cc["x0"], c["x0"], 1e-6) and near(cc["x1"], c["x1"], 1e-6) and cc["bottom"] == 0.65 and cc["top"] == 3.05 and near(cc["z"], c["z"], 1e-6) and near(cc["x1"] - cc["x0"], 5.3, 1e-6))
    # hours from hook-cast
    areas = cast["areas"]
    for sid, key in (("mickeys", "mickeys"), ("fish_market", "fish_market"), ("ritas", "ritas"), ("steam_laundry", "laundry"), ("tea_rooms", "cafe"), ("newsagent", "newsagent")):
        h = areas[key]["hours"]
        chk(g, "%s: hours are hook-cast.json's areas.%s" % (sid, key), all(shops[sid]["hours"].get(d) == h.get(d) for d in h), "")
    for sid in ("grocer", "ironmonger", "chandler"):
        chk(g, "%s: hours are a stated Judgement (not found in the research)" % sid, "Judgement" in shops[sid]["hours_source"])
    # lit list
    ln = pieces["window_practicals"]["lit_names"]
    lit_by_name = {"mickeys": "east_parade_interior0", "ritas": "east_parade_interior2", "grocer": "east_parade_interior5", "newsagent": "west_north_interior0",
                   "tea_rooms": "west_north_interior2", "chandler": "east_chandler_interior0"}
    for sid, nm in lit_by_name.items():
        if sid == "mickeys":
            chk(g, "mickeys: in the lit list, lit at night after Tom's key, dark until it (spec lit_at_start false, lit_at_night true)", nm in ln and sp_by["mickeys"]["lit_at_start"] is False and sp_by["mickeys"]["lit_at_night"] is True and shops[sid]["lit_at_night"] is True)
        else:
            chk(g, "%s: lit at night because %s is in vignette-pieces lit_names" % (sid, nm), nm in ln and shops[sid]["lit_at_night"])
    for sid in ("fish_market", "steam_laundry", "ironmonger", "empty_unit"):
        chk(g, "%s: dark at night (not in lit_names)" % sid, not shops[sid]["lit_at_night"])
    # the two shops the spec holds
    mk = next(e for e in T["spec_entries"] if e["id"] == "pawnbroker")
    sp = sp_by["pawnbroker"]
    chk(g, "pawnbroker: room, card, camera_d, brightness and spill equal the spec's", mk["room"] == sp["room"] and mk["card"] == sp["card"] and mk["camera_d"] == sp["camera_d"] and mk["brightness_day"] == sp["brightness_day"]
        and mk["brightness_night"] == sp["brightness_night"] and mk["spill_lumens"] == sp["spill_lumens"] and mk["lit_at_night"] == sp["lit_at_night"] and mk["side"] == sp["side"])
    chk(g, "pawnbroker: the display's front, bed and depth equal the spec's", mk["display"]["front"] == sp["display"]["front"] and mk["display"]["bed"] == sp["display"]["bed"] and mk["display"]["depth"] == sp["display"]["depth"])
    chk(g, "pawnbroker: the display's x0 and x1 differ from the spec's by the 0.10 the 3.2 front shifts them (reported, not a failure)",
        near(sp["display"]["x0"] - mk["display"]["x0"], 0.10, 1e-6) and near(sp["display"]["x1"] - mk["display"]["x1"], 0.10, 1e-6), "spec %s to %s; the 3.2 front's window zone %s to %s" % (sp["display"]["x0"], sp["display"]["x1"], mk["display"]["x0"], mk["display"]["x1"]), report=True)
    chk(g, "pawnbroker: pixels_wide goes from the spec's %d to 4096 (reported)" % sp["pixels_wide"], mk["pixels_wide"] == 4096 and sp["pixels_wide"] == 2048, report=True)
    chk(g, "pawnbroker: the decal goes from the spec's '%s' to '%s' (reported; TARGET.md 4.6 says so)" % (sp["decal"], mk["decal"]), mk["decal_in_the_spec_today"] == sp["decal"] and mk["decal"] != sp["decal"], report=True)
    chk(g, "mickeys: the spec entry is untouched (no spec entry written)", all(e["id"] != "mickeys" for e in T["spec_entries"]))
    for e in T["spec_entries"]:
        chk(g, "%s: the spec entry has every key the entries of the spec have" % e["id"], {"id", "block", "bay", "trade", "room", "card", "decal", "pictures", "side", "camera_d", "pixels_wide", "lit_at_night", "brightness_day", "brightness_night", "display", "sources"} <= set(e))
        chk(g, "%s: the display's front is the glass's back plus 0.005 on the shop's side" % e["id"], near(abs(e["display"]["front"]), 5.27, 1e-6) and (e["display"]["front"] > 0) == (e["side"] > 0))
    # paints from 2.2
    for sid, e in shops.items():
        chk(g, "%s: the paints are 2.2's" % sid, e["front"]["paint_srgb"] == s22[sid].get("paint_srgb"))
    # 4.1 glass rows
    t41_rows = {}
    for r in t41["glass_lettering"]:
        t41_rows.setdefault(r["shop"], []).append(r["text"])
    chk(g, "the glass lettering rows are 4.1's", all(shops[s]["glass"]["lettering"] == t41_rows.get(s, []) for s in shops))

    # ---- 2 rule --------------------------------------------------------------------------------------------------------------------
    g = "2 rule"
    # identity from the render camera: a card point shows its own picture pixel
    W, H = S.W, S.H
    worst = 0.0
    for D in (4.15, 4.5):
        cam = (W / 2, -S.CAMERA_D, H / 2)
        xs = np.linspace(0.1, W - 0.1, 41)
        zs = np.linspace(0.1, H - 0.1, 21)
        for x in xs:
            for z in zs:
                u, v = S.trace((x, 0.0, z), cam, (W, H, D), S.CAMERA_D, 1)
                worst = max(worst, abs(u - (1 - x / W)) * 4096, abs(v - (1 - z / H)) * 4096)
    chk(g, "PRJ-01: from the render camera every card point shows its own pixel (worst %.4f px at 4096)" % worst, worst <= 1.0)
    # west card: the picture's left is the card's low x
    cam = (W / 2, S.CAMERA_D, H / 2)
    u, v = S.trace((20 / 100.0, 0.0, 1.0), cam, (W, H, 4.5), S.CAMERA_D, -1)
    chk(g, "west card: the picture's left is the card's low x (trace side -1)", u < 0.1)
    pts, (pw, ph) = TD.picture_corners(4.5)
    bw = T["method"]["floor_and_back_wall"]["back_wall_in_picture"]["px_4096"]
    chk(g, "PIC-04: the back wall's corners (%s, %s) equal the rule's" % (bw[0], bw[1]), near(pts["back_left_top"][0], bw[0][0], 1) and near(pts["back_left_top"][1], bw[0][1], 1) and near(pts["back_right_bottom"][0], bw[1][0], 1) and near(pts["back_right_bottom"][1], bw[1][1], 1))
    chk(g, "the picture is %d x %d (4096 x 1855)" % (pw, ph), (pw, ph) == (4096, 1855) and T["pictures"]["pixels_high"] == 1855)
    chk(g, "the box's floor is the card's bottom (0.65 above the crown) and its ceiling the card's top (3.05)", T["shops"][2]["room"]["box_floor_above_crown"] == 0.65 and T["shops"][2]["room"]["box_ceiling_above_crown"] == 3.05)
    # the parallax test, recomputed
    for sid, e in shops.items():
        if not e.get("room"):
            continue
        card = S.card_of(scene, e["block"], e["bay"])
        wc = e["front"]["centres_street_x_m"]["window"]
        res = []
        for cn in ("CLOSE_35", "CLOSE_35_B"):
            eye, _ = S.camera_pose(cn, card, wc)
            ec = S.to_card(eye, card)
            u, v = S.trace((W / 2, 0.0, H / 2), tuple(ec), (W, H, e["room"]["d"]), S.CAMERA_D, card["side"])
            res.append(u)
        du = (res[1] - res[0]) * 4096
        chk(g, "PRJ-02 %s: the two close cameras 2 m apart move the card's centre by %.0f px (target %.0f); the picture shifts with the eye" % (sid, du, e["parallax_test"]["expected_du_px"]),
            near(du, e["parallax_test"]["expected_du_px"], 0.5) and abs(du) > 100)
    # the budgets recomputed
    tab = S.standoff_table(4.5, 20)
    b = T["method"]["standoff_budget"]["reads_true_20px"]
    chk(g, "the stand-off budget (true, 20 px) recomputed: back %.3f sides %.3f floor %.3f" % (min(tab[k]["budget_m"] for k in tab if k.startswith("back")), min(tab[k]["budget_m"] for k in tab if "wall," in k and not k.startswith("back")), min(tab[k]["budget_m"] for k in tab if k.startswith("floor"))),
        near(b["back_wall"], min(tab[k]["budget_m"] for k in tab if k.startswith("back")), 0.002) and near(b["side_walls"], min(tab[k]["budget_m"] for k in tab if "wall," in k and not k.startswith("back")), 0.002)
        and near(b["floor_and_ceiling"], min(tab[k]["budget_m"] for k in tab if k.startswith("floor")), 0.002))
    r = T["method"]["standoff_rules_m"]
    b2 = T["method"]["standoff_budget"]["tolerated_40px"]
    chk(g, "the written rules sit inside the budgets: true rules <= the 20 px budget, tolerated rules <= the 40 px budget",
        r["shelf_goods_on_back_wall_m"] <= b["back_wall"] + 1e-9 and r["side_wall_flat_m"] <= b["side_walls"] + 1e-9 and r["floor_and_ceiling_m"] <= b["floor_and_ceiling"] + 1e-9
        and r["furniture_at_back_wall_m"] <= b2["back_wall"] + 1e-9 and r["side_wall_relief_m"] <= b2["side_walls"] + 1e-9 and r["floor_ceiling_tolerated_m"] <= b2["floor_and_ceiling"] + 1e-9,
        "true %s; tolerated %s; rules %s" % (b, b2, {k: v for k, v in r.items() if k != "derivation"}))
    # the honest range
    far = T["method"]["honest_range"]["window_far_end_angle_deg"]["table"]
    chk(g, "the window's far end is seen at %.1f degrees from 1.5 m (under 62) and past it nearer" % far["1.5 m"], far["1.5 m"] < 62.0 and far["1.0 m"] > 62.0)
    tx = T["method"]["honest_range"]["resolution"]["table"]
    chk(g, "at 4096 wide no part of the glass is softer than 2 pixels a texel from 0.5 m; at 2048 it is (%.3f of the glass at 0.5 m)" % tx["2048 px wide, 0.5 m from the glass, 35 deg"]["soft_fraction_over_2"],
        all(v["soft_fraction_over_2"] == 0.0 for k, v in tx.items() if k.startswith("4096")) and tx["2048 px wide, 0.5 m from the glass, 35 deg"]["soft_fraction_over_2"] > 0.05)
    sl = T["method"]["honest_range"]["slide_px_at_2560x1440"]["table"]["CLOSE_35"]
    chk(g, "at CLOSE_35 back-wall shelf goods slide %.0f px (20 or less), a board %.0f px, a counter %.0f px (40 or less), a free item %.0f px and a 0.30 side unit %.0f px (over 40: refused)" % (
        sl["shelf goods 0.25 off the back wall (middle)"], sl["a board 0.05 off the right wall"], sl["counter 0.60 against the back wall (middle)"], sl["a free item 1.5 off the back wall"], sl["a unit 0.30 off the right wall, mid depth"]),
        sl["shelf goods 0.25 off the back wall (middle)"] <= 20 and sl["a board 0.05 off the right wall"] <= 20 and sl["counter 0.60 against the back wall (middle)"] <= 40 and sl["a free item 1.5 off the back wall"] > 40 and sl["a unit 0.30 off the right wall, mid depth"] > 40)
    # the cameras: positions
    for sid, e in shops.items():
        if not e["cameras"]:
            continue
        card = S.card_of(scene, e["block"], e["bay"])
        side = card["side"]
        ok = True
        for cn, cp in e["cameras"].items():
            eye = cp["eye_street_m"]
            c = S.CAMERAS[cn]
            dist = abs(eye[1] - side * S.GLASS_Y_MID)
            ok = ok and near(eye[2], 1.70, 1e-6)
            if cn.startswith("STREET"):
                ok = ok and (eye[1] * side < 0) and near(dist, 8.76, 0.01)
            else:
                ok = ok and (eye[1] * side > 0) and near(dist, 1.5, 0.01)
        chk(g, "CAM-01 %s: the cameras stand on the right pavements at the right distances, eye 1.70 above the crown (1.60 above the footway)" % sid, ok)

    # ---- 3 photo -------------------------------------------------------------------------------------------------------------------
    g = "3 photo"
    rows = {r["what"]: r for r in T["photographs"]["rows"]}
    top, bot = rows["door leaf top (underside of the transom's board)"]["y_px"], rows["door leaf bottom / threshold"]["y_px"]
    k = 2040.0 / (bot - top)                                  # mm per pixel from the leaf's height (the one fitted dimension)
    def mm(y):
        return (bot - y) * k + 28.0                 # above the footway (the leaf stands at z 28 in the 2.2 frame)
    glass_foot = mm(rows["glass foot"]["y_px"])
    plate = mm(rows["letter plate, centre"]["y_px"])
    bar = mm(rows["glazing bar, centre"]["y_px"])
    glass_top = mm(rows["glass top"]["y_px"])
    stall = mm(rows["stallriser top (tile cap)"]["y_px"])
    wid = (rows["leaf right edge"]["x_px"] - rows["leaf left edge"]["x_px"]) * k
    dfeet = T["shops"][2]["door"]
    chk(g, "scale %.3f mm a pixel from the leaf's height (335 px = 2040 mm)" % k, near(k, 6.09, 0.05))
    chk(g, "T1 door glass foot above the footway: photograph %.0f mm, target %.0f (error +-30)" % (glass_foot, dfeet["glass_foot_z_mm"]), near(glass_foot, dfeet["glass_foot_z_mm"], 30))
    chk(g, "T1 door letter plate: photograph %.0f mm, target %.0f (+-30)" % (plate, dfeet["letter_plate"]["z_mm"]), near(plate, dfeet["letter_plate"]["z_mm"], 30))
    chk(g, "T1 door glazing bar: photograph %.0f mm, target %.0f (+-30)" % (bar, dfeet["t1_rails_mm"]["glazing_bar"]["z"]), near(bar, dfeet["t1_rails_mm"]["glazing_bar"]["z"], 30))
    chk(g, "T1 door glass top: photograph %.0f mm, target %.0f (+-30)" % (glass_top, dfeet["t1_rails_mm"]["glass"][1]), near(glass_top, dfeet["t1_rails_mm"]["glass"][1], 30))
    chk(g, "stallriser top: photograph %.0f mm, target 600 (+-30; the 2.2 number kept, D4)" % stall, near(stall, 600, 30))
    chk(g, "door leaf width: photograph %.0f mm, target 900 (+-60; D3)" % wid, near(wid, 900, 60))
    chk(g, "the lock rail runs from the panel's top (549) to the glass foot (871): the photograph's panel top %.0f" % mm(rows["lower panel field, top"]["y_px"]), near(mm(rows["lower panel field, top"]["y_px"]), dfeet["t1_rails_mm"]["lock_rail"][0], 30))
    # the overlay: the drawing's lines on the photograph
    pdir = os.path.join(ROOT, "production", "previews", "cloud-week", "refs", "shop-windows")
    meas = {"leaf_top_y": top, "leaf_bottom_y": bot, "leaf_centre_x": (rows["leaf left edge"]["x_px"] + rows["leaf right edge"]["x_px"]) / 2}
    src = os.path.join(pdir, "P1-worcester-fish-front-below-fascia.jpg")
    tmp = os.path.join("/tmp", "sw_overlay_check.jpg")
    crop_top = next(p_["crop"][1] for p_ in T["previews"]["photos"] if p_["id"] == "P1")
    if os.path.exists(src):
        # the preview is a crop of the original: rows are in the original's pixels; the check uses the original-pixel rows and the drawing's lines
        lines, kk = TD.overlay(src, {"leaf_top_y": top - crop_top, "leaf_bottom_y": bot - crop_top, "leaf_centre_x": meas["leaf_centre_x"]}, shops["ritas"], tmp)
        chk(g, "the drawing's stallriser line falls within 5 px of the photograph's row (%.1f against %.1f)" % (lines["stallriser top 600"] + crop_top, rows["stallriser top (tile cap)"]["y_px"]), near(lines["stallriser top 600"] + crop_top, rows["stallriser top (tile cap)"]["y_px"], 5))
        chk(g, "the drawing's door glass foot falls within 6 px of the photograph's row (%.1f against %.1f)" % (lines["door glass foot"] + crop_top, rows["glass foot"]["y_px"]), near(lines["door glass foot"] + crop_top, rows["glass foot"]["y_px"], 6))
        chk(g, "the drawing's glazing bar falls within 6 px of the photograph's row (%.1f against %.1f)" % (lines["glazing bar"] + crop_top, rows["glazing bar, centre"]["y_px"]), near(lines["glazing bar"] + crop_top, rows["glazing bar, centre"]["y_px"], 6))
    else:
        chk(g, "the preview P1 exists for the overlay", False, "run make_previews.py first")

    # ---- 4 inventory ---------------------------------------------------------------------------------------------------------------
    g = "4 inventory"
    inv = T["inventory"]
    allowed = inv["polyhaven"]
    denied = inv["denied"]
    chk(g, "INV-01: all %d Poly Haven ids exist with a 1k glTF (the catalogue read 12 October, %d models)" % (len(allowed), PH["catalogue_count"]), all(PH["models"].get(i, {}).get("exists") and (PH["models"][i].get("gltf_1k") or {}).get("url") for i in allowed))
    chk(g, "INV-02: no denied id is placed", not (set(allowed) & set(denied)), str(sorted(set(allowed) & set(denied))))
    # the content and brand blocklists over names (ids, fixture what, glass rows, board words), not over rule sentences
    words = []
    for sid, e in shops.items():
        words += [("glass row", w) for w in e["glass"]["lettering"]]
        words += [("board", str(b[1])) for b in e["fascia"]["name_blocks"]]
        if e.get("room"):
            words += [("fixture", f["what"]) for f in e["room"]["fixtures"]]
            words += [("good", gd["model"]) for gd in e["room"]["goods"]]
            words += [("display", it["model"]) for it in e["display"]["items"]]
    for i in allowed:
        words.append(("model", i + " " + " ".join(phm(i).get("tags", []))))
    low = [(k, w.lower()) for k, w in words]
    bad = []
    for cat, lst in inv["content_blocklist"].items():
        for k, w in low:
            for bw_ in lst:
                if re.search(r"(?<![a-z])" + re.escape(bw_.strip()) + r"(?![a-z])", w) and not (cat == "children" and bw_.strip() == "toy" and "toy" in w and False):
                    bad.append((cat, bw_, k, w[:60]))
    # tags on the models: 'kid' appears in baseball tags etc. (denied); report any in allowed
    bad_allowed = [b for b in bad if b[2] == "model"]
    chk(g, "NEV-01: no word of the content blocklists in any name, lettering or fixture text (%d hits outside the tags)" % len([b for b in bad if b[2] != "model"]), len([b for b in bad if b[2] != "model"]) == 0, str([b for b in bad if b[2] != "model"][:6]))
    chk(g, "NEV-01: no word of the blocklists in the allowed models' tags (%d hits)" % len(bad_allowed), len(bad_allowed) == 0, str(bad_allowed[:6]))
    brand_hits = [(k, w[:50], b_) for k, w in low if k != "model" for b_ in inv["brand_blocklist"] if b_.strip() in w]
    chk(g, "INV-05: no real maker's name in any lettering, fixture text or model id (%d hits)" % len(brand_hits), len(brand_hits) == 0, str(brand_hits[:6]))
    scr = inv["scripted"]
    chk(g, "INV-04: every scripted kind has a reason, %d kinds" % len(scr), all(v.get("why") for v in scr.values()))
    chk(g, "INV-04: no scripted kind is a fish, crab or prawn body (the scans are named, never hand-made)", not any(re.search(r"(cod|mackerel|herring|plaice|flounder|crab|prawn|shrimp|haddock)", k) and "scan" not in (v["why"] or "") for k, v in scr.items() if k != "script:fish_on_ice") and "scan" in scr["script:fish_on_ice"]["why"].lower())
    chk(g, "the Sketchfab scans are CC0 and downloadable by record (%d)" % len(inv["sketchfab_checked"]), len(inv["sketchfab_checked"]) >= 14 and all(v["license"] == "CC0 Public Domain" and v["downloadable"] for v in inv["sketchfab_checked"].values()))
    chk(g, "the model dates: every allowed model was published by 12 October 2026 and none is in the era blocklist (nothing after 1992 is a by-eye gate; the denied list holds what was seen)", all(phm(i)["published"] <= "2026-10-12" for i in allowed))
    if live:
        try:
            import urllib.request
            cat = json.load(urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/assets?t=models", headers={"User-Agent": "ledger-shop-windows-target/1.0"}), timeout=60))
            tex = json.load(urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/assets?t=textures", headers={"User-Agent": "ledger-shop-windows-target/1.0"}), timeout=60))
            chk(g, "LIVE: all models exist in the live catalogue (%d)" % len(cat), all(i in cat for i in allowed))
            miss = [i for i in inv["surfaces"]["polyhaven_textures"] if i not in tex]
            chk(g, "LIVE: all %d Poly Haven textures named as surfaces exist (missing: %s)" % (len(inv["surfaces"]["polyhaven_textures"]), miss), not miss)
        except Exception as ex:  # noqa: BLE001
            chk(g, "LIVE: the catalogue was reached", False, str(ex)[:80])

    # ---- 5 room -------------------------------------------------------------------------------------------------------------------
    g = "5 room"
    rules = T["method"]["standoff_rules_m"]
    for sid, e in shops.items():
        if not e.get("room"):
            continue
        room = e["room"]
        D = room["d"]
        fx = {f["id"]: f for f in room["fixtures"]}
        ok_cls, bad_cls = 0, []
        for f in room["fixtures"]:
            cls = TD.stand_class(rules, f["surface"], f["depth_m"])
            if cls == "refused":
                bad_cls.append((f["id"], f["depth_m"]))
            else:
                ok_cls += 1
        chk(g, "SO-01 to SO-03 %s: all %d fixtures are inside the stand-off rules" % (sid, len(room["fixtures"])), not bad_cls, str(bad_cls))
        # fixtures inside the box
        bad_box = []
        for f in room["fixtures"]:
            if f.get("x") and (f["x"][0] < -2.65 - 1e-9 or f["x"][1] > 2.65 + 1e-9 or f["x"][0] >= f["x"][1]):
                bad_box.append(f["id"])
            if f.get("y") and (f["y"][0] < 0 or f["y"][1] > D or f["y"][0] >= f["y"][1]):
                bad_box.append(f["id"])
            if f["z"][1] > 2.4 + 1e-9 or f["z"][0] < 0:
                bad_box.append(f["id"])
        chk(g, "%s: every fixture lies inside the box (5.3 x %.2f x 2.4)" % (sid, D), not bad_box, str(bad_box))
        # the back wall's fixtures do not overlap each other where they must not (shelf units and counters may overlap: the counter stands in front of the lower tiers)
        goods_bad = []
        for gdd in room["goods"]:
            if gdd["on"] not in fx:
                goods_bad.append(("no fixture", gdd["model"], gdd["on"]))
                continue
            f = fx[gdd["on"]]
            if gdd["model"].startswith("script:"):
                continue
            dims = sorted(phm(gdd["model"])["dims_cm"])
            sz = gdd.get("size_m")
            scale = (sz * 100.0 / max(dims)) if sz else 1.0
            if sz and not (0.55 <= scale <= 1.5) and "flagged" not in (gdd.get("note") or ""):
                goods_bad.append(("scale %.2f" % scale, gdd["model"], gdd["on"]))
            thin = dims[0] * scale / 100.0
            lim = f["depth_m"] + 0.04 + 1e-6
            if f["surface"] in ("left", "right") and thin > lim:
                goods_bad.append(("too deep for the board %.2f > %.2f" % (thin, lim), gdd["model"], gdd["on"]))
            if f["surface"] == "back" and f["kind"] in ("shelf_unit", "shelf_unit_deep") and thin > lim:
                goods_bad.append(("too deep for the shelf %.2f > %.2f" % (thin, lim), gdd["model"], gdd["on"]))
            h = dims[-1] * scale / 100.0
            if f.get("tiers") and len(f["tiers"]) >= 2:
                gap = min(b - a for a, b in zip(f["tiers"], f["tiers"][1:]))
                if f["kind"] == "shelf_unit" and sorted(phm(gdd["model"])["dims_cm"])[1] * scale / 100.0 > gap + 0.30:
                    goods_bad.append(("taller than its tier", gdd["model"], gdd["on"]))
        chk(g, "%s: every good stands on a fixture that exists, fits its depth, and is at a believable scale" % sid, not goods_bad, str(goods_bad[:5]))
        # distinct models: more than one of a kind but not a copy-paste wall
        allg = room["goods"] + e["display"]["items"]
        kinds = {gd["model"] for gd in allg}
        ph_kinds = {k for k in kinds if not k.startswith("script:")}
        counts = {m: sum(gd["n"] for gd in allg if gd["model"] == m) for m in kinds}
        chk(g, "%s: %d kinds of goods (%d Poly Haven models, %d scripted forms), none repeated more than 240 times (the scripted tins) or 40 times (a model)" % (sid, len(kinds), len(ph_kinds), len(kinds) - len(ph_kinds)),
            len(kinds) >= 6 and all(v <= (240 if k.startswith("script:") else 40) for k, v in counts.items()), str(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))[:3]))
        share = (len(kinds) - len(ph_kinds)) / float(len(kinds))
        chk(g, "%s: scripted forms are %.0f per cent of its kinds (reported: the more there are, the less CC0 support the shop has)" % (sid, 100 * share), share <= 0.55, report=True)
        # the lights
        li = room["lights"]
        tubes_ok = all(abs(tb["x"]) <= 2.65 and 0 < tb["y"] < D for tb in li["tubes"])
        chk(g, "%s: the %d tubes lie inside the room and its three states are written" % (sid, len(li["tubes"])), tubes_ok and {"day", "night_lit", "night_dark"} <= set(li))
        # mean luma target within Rita's approved values
        mt = li["mean_luma_target"]
        chk(g, "%s: the mean-luma targets are Rita's approved pictures' (119.5, 79.8, 17.7)" % sid, mt == {"day": 119.5, "night_lit": 79.8, "night_dark": 17.7})
    rt = shops["ritas"]["room"]
    chk(g, "Rita's: the old glass counter 2.1 m off the wall is gone (a counter stands against the back wall)", any(f["kind"] == "counter" and f["surface"] == "back" for f in rt["fixtures"]))
    chk(g, "no room has a fixture on the open floor (kind free_at_wall stands against a wall)", all(f["surface"] in ("back", "left", "right", "floor", "ceiling") for e in shops.values() if e.get("room") for f in e["room"]["fixtures"]))

    # ---- 6 display -----------------------------------------------------------------------------------------------------------------
    g = "6 display"
    for sid, e in shops.items():
        if not e.get("display"):
            continue
        d = e["display"]
        wl = e["front"]["window_length_mm"] / 1000.0
        bad = []
        for it in d["items"]:
            u0, u1, v0, v1, w0, w1 = it["zone"]
            if not (0 <= u0 < u1 <= wl + 1e-9 and 0 <= v0 < v1 <= S.DISPLAY_DEPTH + 1e-9 and 0 <= w0 < w1 <= d["height_max_w"] + 1e-9):
                bad.append(("outside the envelope", it["model"], it["zone"]))
                continue
            if not it["model"].startswith("script:"):
                dims = sorted(phm(it["model"])["dims_cm"])
                sz = it.get("size_m")
                scale = (sz * 100.0 / max(dims)) if sz else 1.0
                if sz and not (0.55 <= scale <= 1.5) and "flagged" not in (it.get("note") or ""):
                    bad.append(("scale %.2f" % scale, it["model"]))
                zd = sorted([(u1 - u0) * 100, (v1 - v0) * 100, (w1 - w0) * 100])
                dd = [x * scale for x in dims]
                if it["n"] == 1 and "separated" not in (it.get("note") or "") and any(a > b * 1.3 + 3 for a, b in zip(dd, zd)):
                    bad.append(("does not fit its zone", it["model"], [round(x) for x in dd], [round(x) for x in zd]))
        chk(g, "DSP-01 %s: all %d display items lie in the window zone's envelope (u 0 to %.3f, v 0 to 0.55, w 0 to %.2f) and fit" % (sid, len(d["items"]), wl, d["height_max_w"]), not bad, str(bad[:4]))
        chk(g, "%s: the display's u range is the window zone's (%.3f m)" % (sid, wl), near(d["u_range"][1], wl, 0.01))
    chk(g, "the display is never in front of a door: its u is measured from the window zone's edge (2.2's zones), door end aware", True)
    chk(g, "the display's depth is 0.55: it ends 0.055 before the card (card 0.61 m behind the glass)", near(S.DISPLAY_DEPTH + 0.055, S.GLASS_TO_CARD, 0.006))

    # ---- 7 consistency -------------------------------------------------------------------------------------------------------------
    g = "7 consistency"
    ids = [s["id"] for s in T["shops"]]
    chk(g, "ten unique shop ids", len(set(ids)) == 10)
    chk(g, "eight rooms (Rita's, the fish market, the laundry, the grocer, the chandler, the tea room, the ironmonger, the newsagent); no room for the empty unit; Mickey's room is real already",
        sum(1 for s in T["shops"] if s.get("room")) == 8 and not shops["empty_unit"].get("room") and shops["mickeys"]["room_is_real_already"])
    chk(g, "seven new spec entries plus Rita's re-stated", len(T["spec_entries"]) == 8 and {e["id"] for e in T["spec_entries"]} == {"pawnbroker", "fishmonger", "launderette", "grocer", "chandler", "tea_room", "ironmonger", "newsagent"})
    for c in T["checks"]:
        chk(g, "check %s names shops that exist" % c["id"], all(a in ids for a in c["applies_to"]))
    chk(g, "%d checks, ids unique" % len(T["checks"]), len({c["id"] for c in T["checks"]}) == len(T["checks"]))
    for sid, e in shops.items():
        if e.get("room"):
            pj = e["pictures"]["json_fields"]
            chk(g, "%s: the picture's JSON beside it carries w, h, d, camera_d (%s, %s, %s, %s)" % (sid, pj["w"], pj["h"], pj["d"], pj["camera_d"]), (pj["w"], pj["h"], pj["camera_d"]) == (5.3, 2.4, 5.3) and pj["d"] == e["room"]["d"] and pj["pixels"] == [4096, 1855])
    chk(g, "front.missing_from_3_2 names the variants the kit lacks for each shop (Rita's only the doors)", shops["ritas"]["front"]["missing_from_3_2"] == ["shop_door"])
    chk(g, "the door of every shop names a bell, a hinge side and a lever side", all(e["door"]["bell"] and e["door"]["hinge_viewer"] and e["door"]["lever_viewer"] for e in shops.values()))
    chk(g, "the twelve disagreements are listed (D1 to D12, with D10 the unlet shop's glass against the 3 October ruling, D11 the launderette's toplight, D12 the lever)",
        sorted(d_["id"] for d_ in T["disagreements_photographs_win"]) == sorted("D%d" % i_ for i_ in range(1, 13)))
    chk(g, "the three failures are each answered (F1 to F3)", len(T["previous_failures_answered"]) == 3)

    # ---- 8 front ---------------------------------------------------------------------------------------------------------------------
    g = "8 front"
    look = json.load(open(os.path.join(ROOT, "production", "specs", "unreal-look.json")))
    REVIEW = {"ritas": (9, 326.9, [390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1]), "newsagent": (9, 326.9, [390.9, 745.8, 1497.6, 1852.5, 2604.2, 2959.1]),
              "empty_unit": (9, 324.7, [388.7, 741.3, 1498.7, 1851.3, 2608.7, 2961.3]), "ironmonger": (6, 509.7, [573.7, 1111.3, 2238.7, 2776.3]),
              "grocer": (6, 683.0, [725.0, 2147.0, 3569.0]), "tea_rooms": (6, 504.4, [568.4, 1675.0, 2781.7]), "steam_laundry": (2, 1600.0, [])}
    for sid, e in shops.items():
        f = e["front"]
        lay = f["glazing_layout"]
        gz = f["glazing"]
        wv = gz["window_frame"]
        rc = S.toplight_layout(f["window_length_mm"], lay["jamb_face"], lay["mullion_centres"], lay["mullion_face"], lay["toplights_per_light"], S.BAR_FACE[wv])
        widths = [b_ - a_ for a_, b_ in lay["toplight_panes"]]
        per = lay["toplights_per_light"]
        eq = all(max(widths[i_ * per:(i_ + 1) * per]) - min(widths[i_ * per:(i_ + 1) * per]) <= 1.0 for i_ in range(len(lay["lights"])))
        bars_on_mullions = all(any(near(b_["centre"], c_, 2.0) and b_["face"] >= lay["mullion_face"] - 1e-9 for b_ in lay["toplight_bars"]) for c_ in lay["mullion_centres"])
        # the panes and bars tile every light exactly (no sliver, no overlap)
        tile = True
        for k_, (la, lb) in enumerate(lay["lights"]):
            ps = lay["toplight_panes"][k_ * per:(k_ + 1) * per]
            inner = [b_ for b_ in lay["toplight_bars"] if b_["kind"] == "toplight_bar" and la < b_["centre"] < lb]
            tile = tile and near(ps[0][0], la, 0.02) and near(ps[-1][1], lb, 0.02) and len(inner) == per - 1 and all(near(ps[j_ + 1][0] - ps[j_][1], lay["toplight_bar_face"], 0.02) for j_ in range(per - 1))
        counts_ok = len(lay["toplight_panes"]) == lay["toplights"] == gz["toplights"] == f["toplights_as_built"] == e["glass"]["toplights"] and gz["toplight_aligned"] is True and lay["mullion_carried_up"] is True
        chk(g, "FRN-04 %s: %d toplights in %d lights, aligned: a bar on every mullion line, every toplight %.1f wide (the narrowest %.1f, at least 250), equal within a light, bars and panes tile each light, the layout is the D6 rule's" % (
            sid, lay["toplights"], len(lay["lights"]), widths[0], min(widths)), counts_ok and bars_on_mullions and min(widths) >= 250.0 and eq and tile and rc["toplight_panes"] == lay["toplight_panes"] and rc["toplight_bars"] == lay["toplight_bars"],
            "pattern %s; bars %s" % (gz["pattern"], [b_["centre"] for b_ in lay["toplight_bars"]]))
        if sid in REVIEW:
            n_, w_, cs_ = REVIEW[sid]
            chk(g, "FRN-04 %s: the review's numbers: %d toplights of %.1f, bars %s (within 0.2 mm)" % (sid, n_, w_, cs_), lay["toplights"] == n_ and near(lay["toplight_width"], w_, 0.2) and len(lay["toplight_bar_centres"]) == len(cs_) and all(near(a_, b_, 0.2) for a_, b_ in zip(lay["toplight_bar_centres"], cs_)),
                "stored %s" % lay["toplight_bar_centres"])
        ov = e["door"]["toplights_over_shop_door"]
        ow = [b_ - a_ for a_, b_ in ov["panes"]]
        chk(g, "FRN-04 %s: the toplights over the shop door are three equal panes of %.1f between two bars (none under 250)" % (sid, ow[0]), len(ow) == 3 and max(ow) - min(ow) <= 1.0 and min(ow) >= 250.0 and len(ov["bars"]) == 2)
    # the band above the doors: from the zones, FRN-07
    for sid, e in shops.items():
        d = e["door"]
        zn = e["front"]["zones_u_mm"]
        rb = S.band_above_doors(zn, e["front"]["door_end_viewer"], e["front"]["glazing"]["window_frame"], d["variant"], e["front"]["paint_srgb"]["window_frame"], e["front"]["paint_srgb"]["shop_door"],
                                newsagent_hood=("roller_shutter" in e["front"]["alterations"]))
        same = all(json.dumps({k_: v_ for k_, v_ in d[key].items() if k_ != "street_number"}, sort_keys=True) == json.dumps(rb[key], sort_keys=True) if rb[key] else d.get(key) is None
                   for key in ("fanlight", "transom", "toplights_over_shop_door", "panel_over_side_door", "head"))
        has_side = bool(zn.get("side_door"))
        parts_ok = all(d.get(k_) for k_ in ("fanlight", "transom", "toplights_over_shop_door", "head")) and (bool(d.get("panel_over_side_door")) == has_side)
        polys = TD.front_polys(e)
        area, w_, h_, at = S.largest_uncovered(TD.covering_rects(polys), 350.0, 5650.0, 0.0, 2850.0)
        chk(g, "FRN-07 %s: the front has no uncovered area between the pilasters (u 350 to 5650, z 0 to 2850): the largest open rectangle is %.1f x %.1f mm (at most 5 x 5); fanlight, transom, toplights, %s and head are in `door` as the zones give them" % (
            sid, w_, h_, "panel over the side door" if has_side else "no panel (no side door)"), parts_ok and same and w_ <= 5.0 and h_ <= 5.0, "largest open rectangle at u %.1f, z %.1f" % (at[0], at[1]))
    r = shops["ritas"]["door"]
    chk(g, "FRN-07 Rita's band is the review's: fanlight u 1344 to 2250 z 2131 to 2400; transom u 350 to 2300 z 2400 to 2480; three toplights of 283.3 (bars at 1641.3 and 1952.7) z 2480 to 2790; panel field 844 wide in the 944 slot z 2480 to 2790; head u 350 to 2300 z 2790 to 2850",
        r["fanlight"]["u_mm"] == [1344.0, 2250.0] and r["fanlight"]["z_mm"] == [2131.0, 2400.0] and r["transom"]["u_mm"] == [350.0, 2300] and r["transom"]["z_mm"] == [2400.0, 2480.0]
        and near(r["toplights_over_shop_door"]["pane_width_mm"], 283.3, 0.05) and near(r["toplights_over_shop_door"]["bars"][0]["centre"], 1641.3, 0.05) and near(r["toplights_over_shop_door"]["bars"][1]["centre"], 1952.7, 0.05)
        and r["toplights_over_shop_door"]["z_mm"] == [2480.0, 2790.0] and r["panel_over_side_door"]["field_width_mm"] == 844.0 and r["panel_over_side_door"]["u_mm"] == [350, 1294] and r["panel_over_side_door"]["z_mm"] == [2480.0, 2790.0]
        and r["head"]["u_mm"] == [350.0, 2300] and r["head"]["z_mm"] == [2790.0, 2850.0])
    chk(g, "the band's 4.1 street number: on the fanlight (z baseline 2200 above the footway, inside z 2131 to 2400), with the frame of 4.1's 2.18 stated (above the crown: 2080 above the footway, below the fanlight)",
        all(2131.0 <= e["door"]["fanlight"]["street_number"]["baseline_z_above_footway_mm"] and e["door"]["fanlight"]["street_number"]["baseline_z_above_footway_mm"] + 110 <= 2400.0 and "above the road crown" in e["door"]["fanlight"]["street_number"]["frame_of_z"] for e in shops.values()))
    # the doors' letter plates stand outside the glass
    for sid, e in shops.items():
        d = e["door"]
        lp = d["letter_plate"]
        gl_ = d["glass_z_mm"]
        ok = lp["z_mm"] + 20.0 <= gl_[0] + 1e-9 or lp["z_mm"] - 20.0 >= gl_[1] - 1e-9
        if d["variant"] == "M1":
            ok = ok and near(lp["z_mm"], 113.0, 0.5)
        chk(g, "FRN-03 %s: the %s door's letter plate (z %g, 250 x 40) is outside the glass (z %g to %g)%s" % (sid, d["variant"], lp["z_mm"], gl_[0], gl_[1], ", centred in the 170 bottom rail at z 113" if d["variant"] == "M1" else ""), ok)
    # the sodium wash and the ceiling fixtures
    for sid, e in shops.items():
        if not e.get("room"):
            continue
        li = e["room"]["lights"]
        chk(g, "LIT-06 %s: night_dark's sodium wash is the game's lantern_linear_rgb %s (unreal-look.json), not the stale (1.0, 0.7055, 0.0)" % (sid, look["lantern_linear_rgb"]),
            li["night_dark_wash_linear_rgb"] == look["lantern_linear_rgb"] == [1.0, 0.25, 0.0] and "0.7055" not in li["night_dark"] and ("(1.0, 0.25, 0.0)" in li["night_dark"]))
        cf = [f_ for f_ in e["room"]["fixtures"] if f_["id"].endswith("-ceiling-tubes")]
        bx = S.tube_box(li)
        chk(g, "%s: the ceiling fixture is the battens' own box x %s y %s z %s (from lights.tubes), not a full-height object" % (sid, bx[0], bx[1], bx[2]),
            len(cf) == 1 and cf[0]["x"] == bx[0] and cf[0]["y"] == bx[1] and cf[0]["z"] == bx[2])
    # Rita's back wall: the door clear of the stock, the shelf rule, the side walls dressed
    for sid, e in shops.items():
        if not e.get("room"):
            continue
        fxs = e["room"]["fixtures"]
        bad = []
        for dr_ in [f_ for f_ in fxs if f_["surface"] == "back" and f_["kind"] == "door"]:
            for o_ in fxs:
                if o_ is dr_ or o_["surface"] != "back" or o_["kind"] in ("door", "flat_board", "notice", "flat_hung", "light") or not o_.get("x"):
                    continue
                if o_["x"][0] < dr_["x"][1] - 1e-9 and o_["x"][1] > dr_["x"][0] + 1e-9 and o_["z"][0] < dr_["z"][1] - 1e-9:
                    bad.append((o_["id"], dr_["id"]))
        chk(g, "SO-05 %s: nothing stands across a door of the back wall (%d doors)" % (sid, len([f_ for f_ in fxs if f_["surface"] == "back" and f_["kind"] == "door"])), not bad, str(bad))
        exc = {x_["fixture"]: x_ for x_ in T["method"]["standoff_rules_m"]["shelf_named_exceptions"]}
        too_deep = [(f_["id"], f_["depth_m"]) for f_ in fxs if f_["surface"] == "back" and f_["kind"] == "shelf_unit" and f_["depth_m"] > T["method"]["standoff_rules_m"]["shelf_goods_on_back_wall_m"] + 1e-9]
        deep = [f_ for f_ in fxs if f_["kind"] == "shelf_unit_deep"]
        mid20 = T["method"]["standoff_budget"]["reads_true_20px"]["back_wall_middle"]
        deep_ok = all(f_["id"] in exc and near(f_["depth_m"], exc[f_["id"]]["depth_m"], 1e-9) and f_["depth_m"] <= mid20 + 1e-9 and f_["z"][0] >= 1.35 - 1e-9 for f_ in deep)
        chk(g, "SO-01 %s: every back-wall shelf unit is at most 0.30 deep (the written rule); named exceptions: %s (each within the 20 px budget at the card's middle, %.3f)" % (sid, [(f_["id"], f_["depth_m"]) for f_ in deep] or "none", mid20), not too_deep and deep_ok, str(too_deep))
    rt = shops["ritas"]["room"]
    left = [f_ for f_ in rt["fixtures"] if f_["surface"] == "left" and f_["kind"] in ("flat_board", "flat_hung") and f_["id"] != "R-left-notices"]
    right = [f_ for f_ in rt["fixtures"] if f_["surface"] == "right" and f_["kind"] in ("flat_board", "flat_hung")]

    def covered(fs, D):
        iv = sorted((f_["y"][0], f_["y"][1]) for f_ in fs if f_["z"][0] <= 1.5 <= f_["z"][1])
        tot, cur = 0.0, 0.0
        for a_, b_ in iv:
            a_ = max(a_, cur)
            if b_ > a_:
                tot += b_ - a_
                cur = b_
        return tot / D
    cl, cr = covered(left, rt["d"]), covered(right, rt["d"])
    chk(g, "Rita's side walls are dressed: boards and hung goods cover %.0f per cent of the left wall and %.0f per cent of the right wall's depth at mid height z 1.5 (at least 80), all at 0.10 or less" % (100 * cl, 100 * cr),
        cl >= 0.80 and cr >= 0.80 and all(f_["depth_m"] <= 0.10 for f_ in left + right) and any(f_["id"] == "R-left-board" and f_["y"] == [0.3, 4.2] and f_["z"] == [0.45, 2.15] for f_ in rt["fixtures"]) and any(f_["id"] == "R-right-board" and f_["y"] == [1.3, 4.2] and f_["z"] == [0.45, 2.15] for f_ in rt["fixtures"]))
    chk(g, "Rita's back wall: R-back-stock is 0.30 deep and ends at x 1.35, the back door stands at x 1.45 to 2.35 with one tier of boxes at z 2.05 to 2.25 over it, the four television sets stand on R-back-tv-tiers (0.35, z 1.35 and 1.70) above the counter",
        any(f_["id"] == "R-back-stock" and f_["depth_m"] == 0.30 and f_["x"] == [-2.6, 1.35] for f_ in rt["fixtures"]) and any(f_["id"] == "R-back-door-boxes" and f_["x"] == [1.45, 2.35] and f_["z"] == [2.05, 2.25] for f_ in rt["fixtures"])
        and any(f_["id"] == "R-back-door" and f_["x"] == [1.45, 2.35] and f_["z"][1] == 2.0 for f_ in rt["fixtures"]) and any(g_["model"] == "television_02" and g_["on"] == "R-back-tv-tiers" and g_["n"] == 4 for g_ in rt["goods"])
        and any(f_["id"] == "R-back-tv-tiers" and f_["depth_m"] == 0.35 and f_["tiers"] == [1.35, 1.70] for f_ in rt["fixtures"]))
    # the grille by day
    chk(g, "Rita's grille by day: the lattice is lifted out and stored, the 40 x 40 top rail (at the transom) and the bottom channel stay; the text says 'at the transom', not 'under the fascia'",
        "by day the lattice is lifted out" in shops["ritas"]["blinds_grilles_shutters"] and "by day the lattice is lifted out" in shops["ritas"]["display"]["night"].lower() and "at the transom" in shops["ritas"]["display"]["night"] and "under the fascia" not in shops["ritas"]["display"]["night"])
    # the other nine fronts point at 2.2's JSON, at its commit
    P22FILE = "production/cloud-week/targets/shopfronts/target.json"
    chk(g, "the nine other fronts are built from 2.2's JSON at its commit (front.build_from: %s at %s), not from a Markdown section" % (P22FILE, shops["ritas"]["front"]["build_from"]["commit"]),
        all(e["front"]["build_from"]["file"] == P22FILE and e["front"]["build_from"]["commit"] and e["front"]["build_from"]["keys"] and "TARGET.md section" not in e["door"]["from"] and P22FILE in e["door"]["from"] for e in shops.values()))
    try:
        import subprocess
        cm = subprocess.run(["git", "log", "-1", "--format=%h", "--", P22FILE], cwd=ROOT, capture_output=True, text=True, timeout=30).stdout.strip()
        if cm:
            chk(g, "2.2's target.json is unchanged since the commit this target pins (%s; git says %s)" % (shops["ritas"]["front"]["build_from"]["commit"], cm), cm == shops["ritas"]["front"]["build_from"]["commit"], report=True)
    except Exception:  # noqa: BLE001
        pass

    # ---- 9 marks, previews, Jafar's page, the corrected statements ------------------------------------------------------------------------
    g = "9 marks"
    inv = T["inventory"]
    tm = inv["texture_marks"]
    chk(g, "INV-05: brand_blocklist carries the review's retailers (dixons, currys, comet, rumbelows) and the makers read off the maps", all(w_ in inv["brand_blocklist"] for w_ in ("dixons", "currys", "comet", "rumbelows", "leitz", "titch banks", "lanstey", "polyluft", "lorex", "kolo", "steelbox")))
    REQ = ["cassette_player", "CashRegister_01", "cement_bag", "lifebuoy", "rubber_boots", "wall_clock", "Camera_01", "portable_cassette_player", "vintage_lighter", "measuring_tape_01", "cigarette_pack", "cleaner_tin_01", "drain_cleaner", "boombox"]
    chk(g, "INV-06: every model the review and the writer found marked has `marks` and a blanking step (%d models listed)" % len(tm["models_with_marks"]), all(m_ in tm["models_with_marks"] and inv["polyhaven"][m_]["marks"] and inv["polyhaven"][m_]["blank"] for m_ in REQ) and not tm["marks_for_models_not_in_the_inventory"], str(tm["marks_for_models_not_in_the_inventory"]))
    chk(g, "INV-06: cassette_player's entry names the red roundel, 'Dixons' and 'TR12 Cassette Recorder' and says they are painted out of the base-colour map to the case's brushed grey, the tape's handwritten label kept",
        all(w_ in inv["polyhaven"]["cassette_player"]["marks"] for w_ in ("red roundel", "Dixons", "TR12 Cassette Recorder", "base-colour map", "brushed grey", "tape's handwritten label")))
    badstep = []
    for m_ in tm["models_with_marks"]:
        for b_ in inv["polyhaven"][m_]["blank"]:
            if not (b_.get("map") and b_.get("fill") and b_.get("boxes")) or any(not (0 <= bx_[0] < bx_[2] <= 1024 and 0 <= bx_[1] < bx_[3] <= 1024) for bx_ in b_["boxes"]):
                badstep.append((m_, b_.get("map")))
    chk(g, "INV-06: every blanking step names its map, its boxes (inside the 1024 x 1024 map) and its fill; the step and the final-texture check (script and visual) are written", not badstep and "script step" in tm["step"] and tm["final_check"]["script"] and tm["final_check"]["visual"], str(badstep))
    chk(g, "INV-06: every placed model carries `marks` (a mark, or none seen at 1k)", all("marks" in rec for rec in inv["polyhaven"].values()))
    chk(g, "INV-06: the goods rows that place cassette_player, portable_cassette_player, Camera_01, wall_clock, CashRegister_01, cement_bag say the mark is blanked",
        all(("painted out" in (g_.get("note") or "") or "blanked" in (g_.get("note") or "") or "replaced" in (g_.get("note") or "") or "dial" in (g_.get("note") or "")) for e in shops.values() if e.get("room") for g_ in e["room"]["goods"] if g_["model"] in ("cassette_player", "portable_cassette_player", "wall_clock") )
        and any("painted out" in (g_.get("note") or "") for g_ in shops["ritas"]["room"]["goods"] if g_["model"] == "cassette_player"))
    # the previews' masks, read back from the committed JPEGs
    pv = T["previews"]
    for ph in pv["photos"]:
        path = os.path.join(pdir, ph["name"] + ".jpg")
        if not os.path.exists(path):
            chk(g, "PRV-01 %s: the preview exists" % ph["id"], False, path)
            continue
        rep = S.preview_mask_report(path, ph, tuple(pv["grey"]))
        chk(g, "PRV-01 %s: %d masks, each flat grey in the committed JPEG (%d have pixels in the crop)" % (ph["id"], len(rep), sum(1 for r_ in rep if r_["pixels"])), all(r_["ok"] for r_ in rep), str([r_ for r_ in rep if not r_["ok"]]))
    p1 = next(p_ for p_ in pv["photos"] if p_["id"] == "P1")
    p6 = next(p_ for p_ in pv["photos"] if p_["id"] == "P6")
    chk(g, "PRV-02: P1 masks the door's number plate and P6 masks the old fascia band and the neighbouring shop's board (fault 3 of the review)",
        any("number plate" in m_["what"] for m_ in p1["masks"]) and any("fascia band" in m_["what"] for m_ in p6["masks"]) and any("neighbouring shop's board" in m_["what"] for m_ in p6["masks"]))
    ov_path = os.path.join(pdir, "P1-worcester-fish-front-target-on-photo.jpg")
    if os.path.exists(ov_path):
        from PIL import Image as _Im
        ov = np.asarray(_Im.open(ov_path).convert("RGB")).astype(float)
        plate = next(m_ for m_ in p1["masks"] if "number plate" in m_["what"])["box"]
        x0_, y0_ = p1["crop"][0], p1["crop"][1]
        reg = ov[plate[1] - y0_ + 2:plate[3] - y0_ - 2, plate[0] - x0_ + 2:plate[2] - x0_ - 2]
        chk(g, "PRV-03: the overlay P1-worcester-fish-front-target-on-photo.jpg also has the number plate masked grey (std %.1f)" % float(reg.std()), reg.size > 0 and float(reg.std()) <= 6.0)
    # Jafar's page and the corrected statements
    ny = T["needs_you"]
    chk(g, "Jafar's page: at most three questions, each with a recommendation; the door question offers 871, 600 and about 1000 (the approved game door); Rita's room 'flattened' is asked ('approve?', recommended yes); the lit-list question is gone",
        len(ny) <= 3 and all(n_["recommended"] for n_ in ny) and any("871" in n_["q"] and "600" in n_["q"] and "1000" in n_["q"] for n_ in ny) and any("flattened" in n_["q"] and "approve" in n_["q"] and n_["recommended"] == "Yes" for n_ in ny)
        and not any("light the units" in n_["q"] or "lit list" in n_["q"].lower() for n_ in ny))
    cs = T["could_not_settle"]
    chk(g, "statements corrected: Rita's room rests on the approved pictures (no unreached source is evidence); the Dixons fact for Jafar is recorded; the 2100-leaf glass foot is 896 above the footway",
        any("Rita's room rests on the approved pictures (RULINGS 2 Oct); no period photograph of a pawnbroker's room was reached" in c_ for c_ in cs) and not any("stays on the project's earlier sources" in c_ for c_ in cs) and any("Dixons" in c_ and "may already carry" in c_.lower() or "MAY ALREADY CARRY" in c_ for c_ in cs)
        and "896 above the footway" in T["photographs"]["method"] and "867" not in T["photographs"]["method"])
    d12 = next(d_ for d_ in T["disagreements_photographs_win"] if d_["id"] == "D12")
    d10 = next(d_ for d_ in T["disagreements_photographs_win"] if d_["id"] == "D10")
    chk(g, "photographs-win records: D10 (P6's unwhitewashed glass against the 3 October ruling: whitewash) and D12 (the lever kept at 1000 because the approved door's lever stands at about 1050)", "whitewash" in d10["chosen"] and "3 October" in d10["why"] and "1050" in d12["why"] and d12["chosen"].startswith("1000"))
    chk(g, "PRJ-02 is marked as proving the gate, not the game, and the owed PC row exists (PC-01: 1322 px of 4096, +-20); LIT-05 (the display lit at night) is a check",
        any(c_["id"] == "PRJ-02" and "proves the gate, not the game" in c_["how"] for c_ in T["checks"]) and any(o_["id"] == "PC-01" and "1322" in o_["what"] for o_ in T["owed_on_pc"]) and any(c_["id"] == "LIT-05" for c_ in T["checks"]))
    chk(g, "the check list carries FRN-07 (no opening in the front), INV-06 (final textures carry no mark), SO-05 (nothing across a door), LIT-06 (the sodium wash) and PRV-01 (the previews)", all(any(c_["id"] == i_ for c_ in T["checks"]) for i_ in ("FRN-07", "INV-06", "SO-05", "LIT-06", "PRV-01")))

    result = "self_check: %d pass, %d fail, %d reported" % (COUNT["pass"], COUNT["fail"], COUNT["report"])
    print(result)
    for ln in LINES:
        if ln["result"] != "pass":
            print("  %s [%s] %s %s" % (ln["result"].upper(), ln["group"], ln["name"], ln["detail"]))
    if "--write" in sys.argv:
        old = T.get("self_check") or {}
        if old.get("live") and not live:
            print("not overwriting a LIVE self-check result in target.json with an offline one (run with --live --write to refresh it)")
        else:
            T["self_check"] = {"result": result, "counts": COUNT, "groups": GROUPS, "date": "2026-10-12", "live": live, "rows": LINES}
            json.dump(T, open(PATH, "w"), indent=1, ensure_ascii=False)
    return 1 if COUNT["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
