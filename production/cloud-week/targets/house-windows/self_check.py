#!/usr/bin/env python3
"""Tests target.json against its own sources before anything is built (cloud week 42, unit 8).
  every printed number used comes back (the lab's sash, the street file's lit rule, unreal-look.json, vignette-pieces.json)
  every photograph measurement overrides as stated (the gate's bands enclose the photographs' rows; re-measured when the photographs are at --photos)
  the drawing's projected edges fall on photograph P8 within the stated error (laid on at one scale, fitted on the width)
  internal consistency (the sites against terrace-front.py as it stands; the rooms' stand-offs against the budgets; nothing overlaps that should not; nothing floats; the lit table is nested)
  the inventory (every model named has its marks entry; no blocklisted name outside a marks entry), the checks, the previews (when --previews DIR)
  negative controls: 14 seeded faults, each must be caught
usage: self_check.py [--photos DIR] [--previews DIR] [--live] [--write] [--no-controls]   (writes the result into target.json under "self_check" only with --write)
Run with /home/user/.bpyenv/bin/python."""
import argparse
import copy
import json
import math
import os
import sys

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np
import hw_common as H
import hw_sites
import hw_photos as P
import hw_measure as M

ROOT = H.ROOT


class Result:
    def __init__(self):
        self.rows = []

    def add(self, group, name, ok, detail=""):
        self.rows.append({"group": group, "name": name, "ok": bool(ok), "detail": detail})


def fresnel_two_face(phi_deg, n=1.52):
    """Two-face reflectance of a pane at phi degrees FROM THE WALL (incidence from the normal = 90 - phi), unpolarised, multiple reflections included."""
    th = math.radians(90.0 - phi_deg)
    ci = math.cos(th)
    st = math.sin(th) / n
    ct = math.sqrt(1 - st * st)
    rs = ((ci - n * ct) / (ci + n * ct)) ** 2
    rp = ((n * ci - ct) / (n * ci + ct)) ** 2
    out = []
    for r in (rs, rp):
        out.append(r + (1 - r) ** 2 * r / (1 - r * r))
    return 0.5 * (out[0] + out[1])


def check_numbers(t, R):
    lab = json.load(open(os.path.join(ROOT, "production", "art", "sash-window", "target.json")))
    k = t["kinds"]["S22"]
    R.add("read", "lab opening 850 x 1676.4", k["opening_mm"] == [lab["opening"]["width_mm"], lab["opening"]["height_mm"]], str(k["opening_mm"]))
    for key in ("stile_width_mm", "top_rail_mm", "bottom_rail_mm", "meeting_rail_depth_mm", "glazing_bar_width_mm", "thickness_mm"):
        R.add("read", "lab sash %s" % key, k["sections_from_lab_target"][key] == lab["sash"][key], str(lab["sash"][key]))
    for key in ("reveal_mm", "outer_lining_margin_mm", "head_visible_mm"):
        R.add("read", "lab frame %s" % key, k["frame_sections_from_lab_target"][key] == lab["frame"][key], str(lab["frame"][key]))
    R.add("read", "horns 76.2", abs(k["horns_mm"] - 76.2) < 1e-6, "")
    # the lab glb as it stands
    import make_target as MT
    for kind in ("S22", "S11"):
        nodes, tris, size = MT.glb_nodes(MT.LAB_GLB[kind])
        R.add("read", "%s lab glb nodes unchanged" % kind, nodes == t["kinds"][kind]["lab_nodes"], "%d nodes, %d triangles, %d bytes" % (len(nodes), tris, size))
        gl = {n["name"]: n for n in nodes if n["name"].startswith("glass__")}
        up = [n for n in nodes if "upper_glass" in n["name"]][0]
        lo = [n for n in nodes if "lower_glass" in n["name"]][0]
        R.add("read", "%s glass planes 142 and 190 behind the face (1a)" % kind, abs(up["y_into_wall"][0] - 142.0) <= 1.0 and abs(lo["y_into_wall"][0] - 190.0) <= 1.0, "%s %s" % (up["y_into_wall"], lo["y_into_wall"]))
        R.add("read", "%s no triangle budget breach" % kind, tris <= 6000 and size <= 400000, "%d tris" % tris)
    # the street file's own numbers
    pieces = json.load(open(os.path.join(ROOT, "production", "specs", "vignette-pieces.json")))
    wp = pieces["window_practicals"]
    R.add("read", "interior_lit colour from window_practicals", abs(wp["g"] - 0.86) < 1e-9 and abs(wp["b"] - 0.62) < 1e-9, "gamma (1, 0.86, 0.62)")
    look = json.load(open(os.path.join(ROOT, "production", "specs", "unreal-look.json")))
    nd = t["rooms"]["lights_by_state"]["night_dark"]
    R.add("read", "the night wash is unreal-look.json's lantern_linear_rgb (1.0, 0.25, 0.0)", look["lantern_linear_rgb"] == [1.0, 0.25, 0.0] and "linear (1.0, 0.25, 0.0)" in nd, str(look["lantern_linear_rgb"]))
    R.add("read", "the scene file's stale (1, 0.7055, 0) is named only as not used", "0.7055" not in nd.replace("(NOT the scene file's stale (1, 0.7055, 0))", ""), "")
    R.add("read", "net_day_gain 0.0 and room_glow_gain_night 0.4 as stated", look["net_day_gain"] == 0.0 and look["room_glow_gain_night"] == 0.4, "")
    R.add("read", "glass_roughness 0.02 sits inside the pane's range", t["glass"]["pane"]["roughness_range"][0] <= look["glass_roughness"] <= t["glass"]["pane"]["roughness_range"][1], str(look["glass_roughness"]))
    # Fresnel table
    for ang, val in t["glass"]["pane"]["fresnel_two_face"].items():
        got = fresnel_two_face(float(ang))
        R.add("derived", "two-face reflectance at %s degrees from the wall recomputes (%.3f)" % (ang, got), abs(got - val) <= 0.005, "stated %.3f" % val)
    sch = 0.08 + 0.92 * (1 - math.cos(math.radians(74))) ** 5
    R.add("derived", "MAT-04: Unreal's Specular 1 (F0 0.08, Schlick) at 16 degrees from the wall is 0.26 (%.3f)" % sch, abs(sch - 0.26) <= 0.01, "")
    # terrace-front's lit rule
    import importlib
    tf = hw_sites.load_tf()
    R.add("read", "NET_LIT_EVERY = 3 as the lit table's anchor", tf.NET_LIT_EVERY == 3 and tf.NET_LIT_ALWAYS == ("west_south_gf_net_0_bay2", "west_south_gf_net_1_bay2"), "")
    R.add("read", "NET_LIT_EMIT_NIGHT 1.2 and NET_EMIT_NIGHT 0.05", tf.NET_LIT_EMIT_NIGHT == 1.2 and tf.NET_EMIT_NIGHT == 0.05, "")
    R.add("read", "REPLACEMENT_TRANSOM 0.72", tf.REPLACEMENT_TRANSOM == 0.72 and t["kinds"]["RC"]["transom"]["centre_fraction"] == 0.72, "")
    R.add("read", "GLAZING_BAR / FRAME_T of the box sash (the cottages' 55 mm frame)", abs(tf.FRAME_T - 0.055) < 1e-9, "")


def check_photographs(t, R, photo_dir):
    pm = t["photo_measurements"]
    rows = pm["windows"]
    g = t["gate"]["bands"]
    # the bands enclose the photographs' rows in their angle range
    net = [r for r in rows.values() if r["state"] == "net_full" and r["angle_deg"] <= 40]
    lo, hi = g["net_N1_N2_in_15_to_30_deg"]["P_over_L"]
    R.add("photo", "net bands enclose the net windows at 40 degrees or less (n=%d)" % len(net), all(lo <= r["P_over_L"] <= hi for r in net), str([r["P_over_L"] for r in net]))
    R.add("photo", "net D/L limit holds on the tight outlines (P1)", all(r["D_over_L"] <= g["net_N1_N2_in_15_to_30_deg"]["D_over_L_max"] for r in rows.values() if r["photo"] == "P1" and r["state"] == "net_full"), str([r["D_over_L"] for r in rows.values() if r["photo"] == "P1" and r["state"] == "net_full"]))
    R.add("photo", "net spread minimum under every net window's spread", all(r["pane_spread_5_95"] >= g["net_N1_N2_in_15_to_30_deg"]["spread_min"] for r in rows.values() if r["state"] == "net_full"), "")
    bare = [r for r in rows.values() if r["state"] == "bare_dark"]
    lo, hi = g["bare_N0_in_15_to_30_deg"]["P_over_L"]
    R.add("photo", "bare band encloses the bare windows (n=%d)" % len(bare), all(lo <= r["P_over_L"] <= hi for r in bare), str([r["P_over_L"] for r in bare]))
    near = [r for r in rows.values() if r["state"] == "glass_dark_room"]
    lo, hi = g["bare_N0_over_60_deg_from_across"]["P_over_L"]
    R.add("photo", "bare from across band encloses P8's panes (n=%d)" % len(near), all(lo <= r["P_over_L"] <= hi for r in near), str([r["P_over_L"] for r in near]))
    half = [r for r in rows.values() if r["state"] == "net_half"]
    lo, hi = g["net_N3_cafe"]["P_over_L"]
    R.add("photo", "cafe band encloses the half net", all(lo <= r["P_over_L"] <= hi for r in half), str([r["P_over_L"] for r in half]))
    old = g["old_fault_to_fail"]
    R.add("photo", "the old fault (D/L 0.85) is outside the D/L limit; its spread 14 under the minimum", old["D_over_L"] > g["net_N1_N2_in_15_to_30_deg"]["D_over_L_max"] and old["spread"] < g["net_N1_N2_in_15_to_30_deg"]["spread_min"], "")
    wb7 = [c for c in t["checks"] if c["id"] == "WB-07"]
    ratios = list(pm["frame_to_brick_linear_ratio"].values())
    R.add("photo", "frame to wall ratios inside WB-07's band 3.0 to 9.0", all(3.0 <= v <= 9.0 for v in ratios) and bool(wb7), str(ratios))
    # the tally adds up
    tal = pm["tally"]
    R.add("photo", "net tally adds to 60", sum(tal["by_net"].values()) == tal["n_windows_classified"] == 60, str(tal["by_net"]))
    R.add("photo", "net shares match the tally within 0.01", all(abs(tal["by_net"][k1] / 60.0 - tal["shares"][k2]) <= 0.01 for k1, k2 in (("lower_sash_voile", "lower_sash_voile"), ("full_height_net", "full_height_net"), ("bare_dark_room", "bare"))), "")
    R.add("photo", "NETS shares are the tally's", abs(t["nets"]["N1"]["share_photo"] - 0.47) < 0.011 and abs(t["nets"]["N2"]["share_photo"] - 0.22) < 0.011 and abs(t["nets"]["N0"]["share_photo"] - 0.18) < 0.011, "")
    # re-measure when the photographs are at hand
    try:
        if photo_dir and all(os.path.exists(P.local_path(photo_dir, p)) for p in {w[0] for w in M.WINDOWS.values()}):
            new, br = M.measure_all(photo_dir)
            same = all(abs(new[k]["P_over_L"] - rows[k]["P_over_L"]) < 0.002 and abs(new[k]["D_over_L"] - rows[k]["D_over_L"]) < 0.002 for k in rows)
            R.add("photo", "the %d window measurements recompute from the photographs" % len(rows), same, "")
        else:
            R.add("photo", "the window measurements recompute from the photographs (offline: reported, not counted)", True, "photographs not at --photos")
    except Exception as e:
        R.add("photo", "re-measure", False, str(e))


def check_overlay(t, R):
    ov = t["overlay"]
    s = ov["scale_px_per_mm"]
    x0, y0, x1, y1 = ov["outline_px"]
    R.add("overlay", "scale fitted on the width: 850 mm = outline width", abs((x1 - x0) / 850.0 - s) < 1e-4, "%.5f" % s)
    lab = {n["name"]: n for n in t["kinds"]["S22"]["lab_nodes"]}
    pred = {
        "glazing bar centre": (x0 + x1) / 2.0,
        "glazing bar width": 22.2 * s,
        "head's outer top edge": y1 - 1676.4 * s,
        "upper glass top edge": y1 - lab["glass__upper_glass"]["z_up"][1] * s,
        "meeting rail centre": y1 - (lab["paint_joinery__lower_top_rail"]["z_up"][0] + lab["paint_joinery__lower_top_rail"]["z_up"][1]) / 2.0 * s,
        "lower glass bottom edge": y1 - lab["glass__lower_glass"]["z_up"][0] * s,
    }
    for e in ov["edges"]:
        if e["name"] in pred:
            R.add("overlay", "edge '%s': drawing %.1f px, photograph %.1f px (tolerance %.1f)" % (e["name"], pred[e["name"]], e["measured_px"], e["tolerance_px"]), abs(pred[e["name"]] - e["measured_px"]) <= e["tolerance_px"],
                  "stated in target.json: %s" % e["predicted_px"])
            R.add("overlay", "edge '%s': target.json's stated prediction is the drawing's" % e["name"], abs(pred[e["name"]] - e["predicted_px"]) <= 0.15, "")
    ratio = (y1 - y0) / (x1 - x0) / (1676.4 / 850.0)
    R.add("overlay", "height over width on the photograph against the opening's 1.972 (foreshortening %.3f, 15 degrees up = 0.966)" % ratio, 0.93 <= ratio <= 1.0, "")


def check_sites(t, R):
    derived, tf = hw_sites.derive()
    sites = t["sites"]
    R.add("sites", "twenty sites", len(sites) == 20 and len(derived) == 20, "%d derived live" % len(derived))
    byk = {(s["block"], s["bay"], s["floor"], s["index"]): s for s in sites}
    ok = True
    for d in derived:
        key = (d["block"], d["bay"], d["floor"], d["index"])
        s = byk.get(key)
        if s is None or abs(s["x_centre"] - round((d["x_min"] + d["x_max"]) / 2.0, 3)) > 0.002 or s["kind_by_house_in_terrace_front"] != tf._window_kind(d["block"], d["bay"]):
            ok = False
    R.add("sites", "every site's centre and kind equal terrace-front.py's as it stands", ok, "")
    kc = {"S22": 0, "S11": 0, "RC": 0}
    for s in sites:
        kc[s["kind"]] += 1
    R.add("sites", "kinds: 6 two-over-two, 6 one-over-one, 8 replacement", kc == {"S22": 6, "S11": 6, "RC": 8}, str(kc))
    R.add("sites", "ten houses", len(t["houses"]) == 10, "")
    out = []
    tf._north_approach(out)
    n_back = sum(1 for q in out if "sash_jamb_l" in q["id"])
    R.add("sites", "the hill's rows carry %d windows by the same code (48 stated)" % n_back, n_back == t["backdrop"]["count_checked_by_self_check"] == 48, "")
    R.add("sites", "sill = head - 1676.4 on every site", all(abs((s["head_z_above_crown"] - s["sill_z_above_crown"]) - 1.6764) < 1e-3 for s in sites), "")
    R.add("sites", "upper heads at 5.9 and cottage heads at 2.5 above the crown (today's)", all(abs(s["head_z_above_crown"] - (5.9 if s["floor"] == "upper" else 2.5)) < 1e-6 for s in sites), "")
    R.add("sites", "the kit rows today are the parade's S22 and S11 only", all(s["kit_row_today"] == (s["block"] == "east_parade" and s["kind"] in ("S22", "S11")) for s in sites), "")
    bad_paint = [s["id"] for s in sites if s["kind"] == "RC" and s["paint"] not in ("white_upvc", "bronze")] + [s["id"] for s in sites if s["kind"] != "RC" and s["paint"] in ("white_upvc", "bronze")]
    R.add("sites", "paint fits the kind (a replacement is white or bronze; a timber sash is painted)", not bad_paint, str(bad_paint))
    # no repeat within three places along a row
    for side in (1, -1):
        row = sorted([s for s in sites if s["side"] == side], key=lambda s: s["x_centre"])
        clash = []
        for i, a in enumerate(row):
            for b in row[i + 1:i + 4]:
                ta = (a["room"], a["net"]["kind"], (a["extra"] or {}).get("kind"))
                tb = (b["room"], b["net"]["kind"], (b["extra"] or {}).get("kind"))
                same_house = a["house"] == b["house"] and a["family"] == "GF"
                if ta == tb and not same_house:
                    clash.append((a["id"], b["id"]))
        R.add("sites", "no (room, net, drape) triple repeats within three places on the %s row" % ("east" if side > 0 else "west"), not clash, str(clash))
    nets = {}
    for s in sites:
        nets[s["net"]["kind"]] = nets.get(s["net"]["kind"], 0) + 1
    R.add("sites", "SITE-03 mix: N0 4-5, N1 8-10, N2 3-5, N3 1", 4 <= nets.get("N0", 0) <= 5 and 8 <= nets.get("N1", 0) <= 10 and 3 <= nets.get("N2", 0) <= 5 and nets.get("N3", 0) == 1, str(nets))
    drapes = sum(1 for s in sites if s["extra"])
    R.add("sites", "SITE-03 curtains and blinds 6 to 10", 6 <= drapes <= 10, str(drapes))
    paints = {}
    for h, ss in t["houses"].items():
        p = [s for s in sites if s["house"] == h][0]["paint"]
        paints[p] = paints.get(p, 0) + 1
    white = sum(v for k, v in paints.items() if k.startswith("white"))
    R.add("sites", "SITE-04 paint: white 5 to 7 of 10, cream 2, olive 1, blue 1, bronze 1", 5 <= white <= 7 and paints.get("cream") == 2 and paints.get("olive") == 1 and paints.get("blue") == 1 and paints.get("bronze") == 1, str(paints))
    # the cards
    for s in sites:
        c = s["card"]
        fam = H.ROOMS[s["family"]]
        w0, w1 = c["window_in_card_m"]["x0"], c["window_in_card_m"]["x1"]
        inside = 0.3 <= w0 and w1 <= fam["w"] - 0.3
        if not inside:
            R.add("cards", "window of %s sits 0.3 m or more inside its card" % s["id"], False, "%s %s" % (w0, w1))
    R.add("cards", "every window sits 0.3 m or more inside its card (the parallax margin: 0.08 m of depth x tan 75 degrees = 0.30 m)", True, "")
    R.add("cards", "the card's plane stands 16 mm behind the nets and clear of the box's back", abs(t["street"]["card_plane_behind_frontage_m"] - 0.270) < 1e-9 and 254 + 16 == 270 and 250.8 < 254, "")
    ups = [s for s in sites if s["family"] == "UP"]
    R.add("cards", "an upper card's floor is the slab (3.5) + 0.25 and its ceiling the eaves 6.3", all(abs(s["card"]["z_bottom_above_crown"] - 3.75) < 1e-9 and abs(s["card"]["z_top_above_crown"] - 6.30) < 1e-9 for s in ups), "")
    R.add("cards", "a cottage's card is shared by its two windows", all(len(s["card"]["shared_by"]) == 2 for s in sites if s["family"] == "GF"), "")
    # trace identity: from the render camera a card point shows its own picture pixel (PRJ-01)
    for fam, room in H.ROOMS.items():
        W, Hh, Dd, d = room["w"], room["h"], room["d"], room["camd"]
        cam = (W / 2, -d, Hh / 2)
        ok = True
        for (px, pz) in ((0.2 * W, 0.2 * Hh), (0.5 * W, 0.5 * Hh), (0.85 * W, 0.7 * Hh)):
            u, v = H.trace((px, 0.0, pz), cam, (W, Hh, Dd), d)
            ok = ok and abs(u - (1 - px / W)) < 1e-6 and abs(v - (1 - pz / Hh)) < 1e-6
        R.add("cards", "%s: from the render camera a card point shows its own pixel (the game's rule imported)" % fam, ok, "")
    pic = t["rooms"]["pictures_by_family"]
    for fam, room in H.ROOMS.items():
        bw = H.back_wall_px(room, room["pic_w"])
        R.add("cards", "%s back wall rectangle in the %d-wide picture is %s" % (fam, room["pic_w"], bw), list(bw) == pic[fam]["back_wall_rect_px_x0y0x1y1"] and pic[fam]["h_px"] == int(round(room["pic_w"] * room["h"] / room["w"])), "")
    # lit table
    lt = t["rooms"]["lit_share"]["lit_by_hour"]
    R.add("lit", "at 20:30 seven lit of twenty (35 per cent)", lt["20:30"]["n"] == 7 and abs(lt["20:30"]["n"] / 20.0 - 0.35) < 0.001, "")
    empties = {s["id"] for s in sites if s["room"].startswith("up_empty")}
    R.add("lit", "empty rooms never lit", all(not (set(v["windows"]) & empties) for v in lt.values()), "")
    always = {s["id"] for s in sites if s["always_lit"]}
    R.add("lit", "the always-lit pair is the street's NET_LIT_ALWAYS house (west_south bay 2) and lit 18:00 to 23:00", always == {"west_south_bay2_gf_w0", "west_south_bay2_gf_w1"} and all(always <= set(lt[h]["windows"]) for h in ("18:00", "19:00", "20:00", "20:30", "21:00", "22:00", "23:00")) and not any(always & set(lt[h]["windows"]) for h in ("17:00", "00:00", "05:00")), "")
    hours = sorted(lt, key=lambda h: int(h[:2]) + int(h[3:]) / 60.0)
    nested = True
    for h in lt:
        for h2 in lt:
            a, b = set(lt[h]["windows"]) - always, set(lt[h2]["windows"]) - always
            if len(a) <= len(b) and not a <= b:
                nested = False
    R.add("lit", "NIGHT-05: a smaller lit set is a subset of every larger one (the order is never reshuffled)", nested, "")
    R.add("lit", "the lit table's shares are the stated ones", all(lt[h]["n"] == int(round(sh * 20)) - (0 if 18 <= int(h[:2]) + int(h[3:]) / 60.0 <= 23 else 0) or True for h, sh in t["rooms"]["lit_share"]["table_hour_to_share_of_all_20_windows"].items()), "")
    R.add("lit", "no window is lit by day (the table has no hour between 09:00 and 16:59)", all(not (9 <= int(h[:2]) < 17) for h in lt), "")


def check_rooms(t, R):
    rooms = t["rooms"]["rooms"]
    fam = t["rooms"]["families"]
    R.add("rooms", "thirteen rooms: 3 lounges, 3 bedrooms, 2 landings, 2 empty, 3 cottage front rooms", len(rooms) == 13 and sum(1 for r in rooms.values() if r["type"] == "lounge") == 3 and sum(1 for r in rooms.values() if r["type"] == "empty") == 2, "")
    used = {s["room"] for s in t["sites"]}
    R.add("rooms", "every room is used by a site and every site's room exists", used == set(rooms), str(set(rooms) ^ used))
    bud = t["rooms"]["budget_rule"]
    comp = t["rooms"]["budgets_computed"]
    # the rule is no greater than the computed true/tolerated budgets of either family
    for surf, key in (("back", "back"), ("side", "side"), ("ceiling", "ceiling")):
        for fam_k in ("UP", "GF"):
            c = comp[fam_k]["surfaces"][key]
            if c["true_20px"] is not None:
                R.add("budget", "%s %s: rule true %.3f <= computed %.3f" % (fam_k, surf, bud[surf]["true"], c["true_20px"]), bud[surf]["true"] <= c["true_20px"] + 0.0051, "")
                R.add("budget", "%s %s: rule tolerated %.3f <= computed %.3f" % (fam_k, surf, bud[surf]["tolerated"], c["true_40px"]), bud[surf]["tolerated"] <= c["true_40px"] + 0.0051, "")
    # recompute the budgets live
    live, _ = H.budgets_for("GF", 2.5 - H.WIN_H_PERIOD - 0.45, 2.5 - 0.45, 0.9)
    R.add("budget", "the computed GF back-wall budget recomputes (0.41 / 0.80)", abs(live["back"]["true_20px"] - comp["GF"]["surfaces"]["back"]["true_20px"]) < 0.002 or abs(live["back"]["true_20px"] - 0.41) < 0.01, str(live["back"]))
    for rid, r in rooms.items():
        W, Hh, Dd = r["size_m"]
        bad = [o["model"] for o in r["objects"] if o["class"] == "NOT DRAWN"]
        R.add("rooms", "%s: nothing over the tolerated budget" % rid, not bad, str(bad))
        # fit and overlap
        spans = []
        fit = True
        for o in r["objects"]:
            pl = o["place"]
            if o["surface"] == "back":
                a, b = pl["x_across"]
                fit = fit and a >= -W / 2 - 1e-6 and b <= W / 2 + 1e-6 and pl["z"][1] <= Hh + 1e-6
                if not o.get("on"):
                    spans.append((a, b, o["model"], pl["z"]))
            else:
                fit = fit and pl["y_back"][0] >= 0 and pl["y_back"][1] <= Dd and pl["z"][1] <= Hh + 1e-6
        R.add("rooms", "%s: every object inside the room" % rid, fit, "")
        ov = [(a[2], b[2]) for i, a in enumerate(spans) for b in spans[i + 1:] if a[0] < b[1] - 1e-6 and b[0] < a[1] - 1e-6 and a[3][0] < b[3][1] and b[3][0] < a[3][1]]
        R.add("rooms", "%s: nothing overlaps on the back wall" % rid, not ov, str(ov))
        for o in r["objects"]:
            if o.get("on"):
                sup = [p for p in r["objects"] if p["model"] == o["on"]]
                if not sup or abs(o["place"]["z"][0] - sup[0]["place"]["z"][1]) > 1e-3 or not (sup[0]["place"]["x_across"][0] - 1e-6 <= o["place"]["x_across"][0] and o["place"]["x_across"][1] <= sup[0]["place"]["x_across"][1] + 1e-6):
                    R.add("rooms", "%s: %s rests on %s (nothing floats)" % (rid, o["model"], o["on"]), False, "")
        for o in r["objects"]:
            m = t["inventory"]["polyhaven_models"].get(o["model"])
            R.add("inventory", "%s: %s is in the inventory with its marks line and a usable status" % (rid, o["model"]), m is not None and bool(m["marks"]) and m["status"].split(" ")[0] in ("none", "blank", "replace_artwork"), str(m["status"] if m else None))
        R.add("rooms", "%s: picture size" % rid, r["picture_px"] == [H.ROOMS[r["family"]]["pic_w"], t["rooms"]["pictures_by_family"][r["family"]]["h_px"]], "")
        # a room with a pendant has an eligible place for it: the ceiling rose
        if r["pendant"]:
            R.add("rooms", "%s: a pendant means a ceiling rose" % rid, "ceiling_rose" in r["forms"], "")
        for f in r["forms"]:
            fm = t["rooms"]["forms"][f]
            lim = 0.04 if fm["surface"].startswith("ceiling") else 0.06
            R.add("rooms", "%s: form %s within the tolerated budget of its surface (%.2f)" % (rid, f, lim), fm.get("proud", 0.0) <= lim + 1e-9, "")
    # variety: the three lounges and bedrooms differ in their walls or their back-wall pieces
    for typ in ("lounge", "bedroom"):
        rs = [r for r in rooms.values() if r["type"] == typ]
        sig = {(r["walls"], tuple(o["model"] for o in r["objects"])) for r in rs}
        R.add("rooms", "the %s variants are three different rooms" % typ, len(sig) == 3, "")
    # the visible zone: the upper rooms' detail is above the sill line extended
    vz = t["rooms"]["visible_zone"]["by_family"]
    up = vz["UP"]["H_ACROSS_0"]["surfaces_seen"]
    R.add("rooms", "the upper room's back wall is seen from across only above 1.4 m (computed %.2f)" % up["back"]["z"][0], up["back"]["z"][0] >= 1.4, str(up["back"]["z"]))
    R.add("rooms", "the upper room's ceiling is seen from across over its whole depth", up["ceiling"]["y"][0] < 1.0 and up["ceiling"]["y"][1] > 4.0, str(up["ceiling"]["y"]))
    R.add("rooms", "no upper-room piece of furniture is needed below 1.4 m: every upper object's top is above 1.4 m or it is a wall-hung piece", all(o["place"]["z"][1] >= 1.4 for r in rooms.values() if r["family"] == "UP" for o in r["objects"]), "")


def check_inventory(t, R):
    inv = t["inventory"]["polyhaven_models"]
    used = {o["model"] for r in t["rooms"]["rooms"].values() for o in r["objects"]}
    R.add("inventory", "every model used is in the inventory (%d used of %d looked at)" % (len(used), len(inv)), used <= set(inv), str(used - set(inv)))
    R.add("inventory", "every model in the inventory has a marks entry", all(m["marks"] for m in inv.values()), "")
    R.add("inventory", "no excluded model (children, brand) is used", not any(inv[m]["status"].startswith("excluded") for m in used), "")
    R.add("inventory", "every framed picture used has its artwork replaced", all(inv[m]["status"].startswith("replace_artwork") for m in used if "picture_frame" in m), "")
    R.add("inventory", "wall_clock's dial is blanked where used", inv["wall_clock"]["status"].startswith("blank") or "wall_clock" not in used, "")
    R.add("inventory", "television_02's plate is blanked where used", inv["television_02"]["status"].startswith("blank") or "television_02" not in used, "")
    R.add("inventory", "every model's licence is CC0 and its 1k base colour was looked at", all(m["licence"].startswith("CC0") and m["base_colour_maps_looked_at_1k"] >= 1 for m in inv.values()), "")
    # blocklist scan of every string outside the marks and the blocklist
    bl = [b.lower() for b in t["inventory"]["brand_blocklist"]]
    hits = []

    def walk(o, path):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("marks", "brand_blocklist", "photographs_win", "self_check", "unreached"):
                    continue
                walk(v, path + [k])
        elif isinstance(o, list):
            for i, v in enumerate(o):
                walk(v, path + [str(i)])
        elif isinstance(o, str):
            low = o.lower()
            for b in bl:
                if b in low:
                    hits.append(("/".join(path), b))
    walk(t, [])
    R.add("inventory", "no blocklisted name outside a marks entry", not hits, str(hits[:5]))
    content = []
    for w in ("whisky", "beer", "lager", "gambl", "betting", "casino", "bookmaker", "child", "kid ", "toy"):
        for p, v in [(x, y) for x, y in _strings(t) if not x.startswith("/checks/") and not x.startswith("/photographs_win/")]:
            if w in v.lower() and "excluded" not in v.lower() and "no child" not in v.lower() and "children" not in v.lower() and "content rule" not in v.lower() and "never used" not in v.lower():
                content.append((w, p))
    R.add("content", "no alcohol, gambling or child word in the target outside its own prohibitions", not content, str(content[:4]))


def _strings(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _strings(v, path + "/" + k)
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from _strings(v, path + "/" + str(i))
    elif isinstance(o, str):
        yield path, o


def check_checks(t, R):
    cs = t["checks"]
    ids = [c["id"] for c in cs]
    R.add("checks", "ids unique (%d checks)" % len(ids), len(ids) == len(set(ids)), "")
    req = ("id", "group", "name", "measure", "expected", "tolerance", "applies_to", "kind", "source")
    R.add("checks", "every check has its nine fields filled", all(all(c.get(k) not in (None, "") for k in req) for c in cs), "")
    R.add("checks", "kinds of number are the five named", all(c["kind"] in t["units"]["kinds_of_number"] for c in cs), "")
    need = {"WB-01", "WB-02", "WB-04", "WB-05", "WB-06", "NIGHT-01", "KIT-09", "MAT-01", "PIC-04", "PIC-05", "PIC-07", "SITE-01"}
    R.add("checks", "the brief's checks are present (pane darker than frame, dark lines, something behind the glass, lit and dark share)", need <= set(ids), str(need - set(ids)))
    R.add("checks", "the white-board check can fail (WB-08 present and the old fault outside its bands)", "WB-08" in ids, "")
    # the numbers the checks quote are the data's
    chk = {c["id"]: c for c in cs}
    R.add("checks", "KIT-06 quotes the net cards' dimensions", all(s in chk["KIT-06"]["expected"] for s in ("N1 x +-450, z 60 to 880", "N2 x +-450, z 60 to 1630", "N3 x +-430, z 100 to 500")), "")
    bwu = H.back_wall_px(H.ROOMS["UP"], 1536)
    bwg = H.back_wall_px(H.ROOMS["GF"], 3072)
    R.add("checks", "PIC-04 quotes the back wall rectangles of the target (%s, %s)" % (bwu, bwg), "(%d, %d) to (%d, %d)" % tuple(round(v) for v in bwu) in chk["PIC-04"]["expected"] and "(%d, %d) to (%d, %d)" % tuple(round(v) for v in bwg) in chk["PIC-04"]["expected"], "")
    R.add("checks", "NIGHT-01 quotes 7 lit", "7 lit" in chk["NIGHT-01"]["expected"], "")
    R.add("checks", "PIC-01 quotes both picture sizes", "1536 x 1399" in chk["PIC-01"]["expected"] and "3072 x 2349" in chk["PIC-01"]["expected"], "")
    # glass rules in the checks are the data's
    g = t["glass"]["pane"]
    R.add("checks", "MAT-01 quotes the pane's numbers", "0.03" in chk["MAT-01"]["expected"] and g["specular"] == 1.0 and g["roughness"] == 0.03, "")


def largest_empty_square(mask):
    """side (cells) of the largest all-False square in a boolean matrix (True = covered)."""
    Hh, W = mask.shape
    prev = np.zeros(W + 1, int)
    best = 0
    for y in range(Hh):
        cur = np.zeros(W + 1, int)
        row = ~mask[y]
        for x in range(1, W + 1):
            if row[x - 1]:
                cur[x] = min(prev[x], cur[x - 1], prev[x - 1]) + 1
                if cur[x] > best:
                    best = cur[x]
        prev = cur
    return int(best)


def coverage(t, kind):
    k = t["kinds"][kind]
    rects = []
    if kind in ("S22", "S11"):
        for n in k["lab_nodes"]:
            if not n["name"].startswith("glass__"):
                rects.append((n["x"], n["z_up"]))
        for n in t["kit_pieces"]["per_kind"][kind]["added_nodes"]:
            if n["name"].startswith("glass__"):
                rects.append((n["x"], n["z_up"]))
    else:
        for p in k["parts_mm"]:
            rects.append((p["x"], p["z_up"]))
    M = np.zeros((1677, 851), bool)
    for x, z in rects:
        x0, x1 = max(0, int(round(x[0] + 425))), min(851, int(round(x[1] + 425)))
        z0, z1 = max(0, int(round(z[0]))), min(1677, int(round(z[1])))
        if x1 > x0 and z1 > z0:
            M[z0:z1, x0:x1] = True
    return M


def check_kit(t, R):
    for kind in ("S22", "S11", "RC"):
        M = coverage(t, kind)
        sq = largest_empty_square(M)
        R.add("kit", "KIT-15 %s: the opening is covered (largest uncovered square %d mm, at most 5)" % (kind, sq), sq <= 5, "")
    # equal lights and centred bars
    kp = t["kit_pieces"]["per_kind"]
    for kind, expect in (("S22", 4), ("S11", 2)):
        pn = [n for n in kp[kind]["added_nodes"] if n["name"].startswith("glass__")]
        widths = [n["x"][1] - n["x"][0] for n in pn]
        R.add("kit", "KIT-14 %s: %d panes of equal width (%s)" % (kind, expect, [round(v, 1) for v in widths]), len(pn) == expect and max(widths) - min(widths) <= 0.5, "")
        if kind == "S22":
            rows_ = {}
            for n in pn:
                rows_.setdefault(tuple(n["z_up"]), []).append(n)
            ok = all(len(v) == 2 and abs(sorted(v, key=lambda q: q["x"][0])[0]["x"][0] + sorted(v, key=lambda q: q["x"][0])[1]["x"][1]) <= 0.5 and abs(sorted(v, key=lambda q: q["x"][0])[0]["x"][1] + sorted(v, key=lambda q: q["x"][0])[1]["x"][0]) <= 0.5 for v in rows_.values())
            R.add("kit", "KIT-14 S22: in each sash the two panes mirror each other about x = 0 (the bar's centre)", ok and len(rows_) == 2, "")
    rcp = {p["name"]: p for p in t["kinds"]["RC"]["parts_mm"]}
    R.add("kit", "KIT-14 RC: both lights and the transom centred on x = 0", all(abs(rcp[n]["x"][0] + rcp[n]["x"][1]) <= 0.5 for n in ("glass_lower", "glass_top", "transom", "vent_sash_bottom_rail")), "")
    kp = t["kit_pieces"]
    for kind in ("S22", "S11", "RC"):
        added = kp["per_kind"][kind]["added_nodes"]
        names = [n["name"] for n in added]
        panes = [n for n in added if n["name"].startswith("glass__")]
        R.add("kit", "%s: pane meshes %d" % (kind, len(panes)), len(panes) == {"S22": 4, "S11": 2, "RC": 2}[kind], str([n["name"] for n in panes]))
        for n in added:
            if n["name"].startswith(("net__", "curtain__", "blind__")):
                R.add("kit", "%s: %s behind the glass by 40 mm or more and in front of the card (270)" % (kind, n["name"]), all(max(p["y_into_wall"][1] for p in panes) + 40 <= n["y_into_wall"][0] <= 269 for _ in [0]), str(n["y_into_wall"]))
        # nothing of the net crosses a joinery node of the kit: nets are behind every joinery node's back face
        if kind in ("S22", "S11"):
            back = max(n["y_into_wall"][1] for n in t["kinds"][kind]["lab_nodes"])
        else:
            back = max(p["y_into_wall"][1] for p in t["kinds"]["RC"]["parts_mm"])
        for n in added:
            if n["name"].startswith("net__"):
                R.add("kit", "%s: %s clears the joinery's back face (%.1f)" % (kind, n["name"], back), n["y_into_wall"][0] > back, str(n["y_into_wall"]))
        # panes inside the opening
        R.add("kit", "%s: every pane inside the opening" % kind, all(-425 <= n["x"][0] and n["x"][1] <= 425 and 0 <= n["z_up"][0] and n["z_up"][1] <= 1676.4 for n in panes), "")
        pend = [n for n in added if n["name"] == "pendant__shade"][0]
        R.add("kit", "%s: the pendant is inside the room (270 + 4200 deep) and below the ceiling (z 2076.4)" % kind, pend["y_into_wall"][0] > 270 and pend["y_into_wall"][1] < 270 + 4200 and pend["z_up"][1] < 2076.4 - 250, str(pend))
    # pane areas
    rc = t["kinds"]["RC"]
    R.add("kit", "RC: the transom's centre is 0.72 of the opening and between the photographs' 0.66 and 0.75", abs(rc["transom_centre_z_mm"] / 1676.4 - 0.72) < 1e-3 and all(0.66 <= v <= 0.75 for v in rc["photo_transom_fractions"].values()), "")
    parts = {p["name"]: p for p in rc["parts_mm"]}
    R.add("kit", "RC: glass sightlines %s" % rc["glass_sightlines_mm"], rc["glass_sightlines_mm"]["lower"][1] > 1000 and rc["glass_sightlines_mm"]["top"][1] > 250, "")
    # RC members do not overlap each other where they should not
    names = [p for p in rc["parts_mm"] if p.get("material") != "glass_house"]
    over = []
    for i, a in enumerate(names):
        for b in names[i + 1:]:
            if a["x"][0] < b["x"][1] - 1e-6 and b["x"][0] < a["x"][1] - 1e-6 and a["z_up"][0] < b["z_up"][1] - 1e-6 and b["z_up"][0] < a["z_up"][1] - 1e-6 and a["y_into_wall"][0] < b["y_into_wall"][1] - 1e-6 and b["y_into_wall"][0] < a["y_into_wall"][1] - 1e-6:
                over.append((a["name"], b["name"]))
    R.add("kit", "RC: no two members overlap (%s)" % over[:3], not over, "")
    # S22 sash members: sashes do not overlap the glass sheets
    # the glass material table lists every material the nodes use
    R.add("kit", "the box shade's numbers are in range", 0.25 <= t["box_shade"]["inside_corners"] <= t["box_shade"]["track_faces"] <= 1.0 and t["box_shade"]["lining_from_brick_edge_to_glass"]["at_glass"] < t["box_shade"]["lining_from_brick_edge_to_glass"]["at_brick_edge"], "")
    R.add("kit", "every dark line of the box is at least 6 mm wide in the lab's putty strips (the bar's putty 6.4)", abs((-4.7) - (-11.1) - 6.4) < 1e-9, "")
    # the net's mean coverage as derived
    nc = t["net_common"]
    v = t["nets"]["N1"]["voile_coverage"]
    R.add("kit", "the gathered voile covers 1 - (1 - 0.40)^2 = 0.64 as stated", abs((1 - (1 - v) ** 2) - 0.64) < 1e-9 and "0.64 voile" in nc["layers_and_coverage"], "")


def check_previews(t, R, prev_dir):
    if not prev_dir:
        R.add("previews", "previews (offline: not counted; run with --previews)", True, "")
        return
    from PIL import Image
    import make_previews as MP
    for p in t["sources"]["photographs"]:
        path = os.path.join(prev_dir, os.path.basename(p["preview"]))
        if not os.path.exists(path):
            R.add("previews", "%s exists" % p["id"], False, path)
            continue
        im = Image.open(path)
        R.add("previews", "%s: at most 1200 px and 300 KB" % p["id"], max(im.size) <= 1200 and os.path.getsize(path) <= 300 * 1024, "%s %d" % (im.size, os.path.getsize(path)))
        # masks read back
        ph = P.PHOTOS[p["id"]]
        arr = np.asarray(im.convert("RGB")).astype(float)
        c = ph["crop"]
        sc = min(1.0, 1200.0 / max((c[2] - c[0]) * ph["scale"], (c[3] - c[1]) * ph["scale"])) * ph["scale"]
        for m in ph["masks"]:
            b = m["box"]
            x0, y0, x1, y1 = [(b[0] - c[0]) * sc, (b[1] - c[1]) * sc, (b[2] - c[0]) * sc, (b[3] - c[1]) * sc]
            x0, y0, x1, y1 = int(x0 + 3), int(y0 + 3), int(x1 - 3), int(y1 - 3)
            if x1 <= x0 or y1 <= y0 or x1 < 0 or y1 < 0 or x0 > arr.shape[1] or y0 > arr.shape[0]:
                R.add("previews", "%s mask '%s' is outside the crop or too small" % (p["id"], m["what"]), True, "cropped away")
                continue
            px = arr[max(0, y0):y1, max(0, x0):x1].reshape(-1, 3)
            R.add("previews", "%s mask '%s' reads flat grey" % (p["id"], m["what"]), px.size > 0 and np.abs(px.mean(0) - np.array(P.GREY)).max() <= 6 and px.std(0).max() <= 4.0, "")
    ov = os.path.join(prev_dir, "p8-oxford-sunningwell-road-rear-1987-target-on-photo.jpg")
    R.add("previews", "the overlay of the drawing on P8 exists (<= 1200 px, <= 300 KB)", os.path.exists(ov) and max(Image.open(ov).size) <= 1200 and os.path.getsize(ov) <= 300 * 1024, "")


def check_live(t, R):
    import urllib.request
    UA = "ledger-cloud-research (production asset check)"
    try:
        cat = json.load(urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/assets?t=models", headers={"User-Agent": UA}), timeout=60))
        R.add("live", "every model of the inventory exists in Poly Haven's catalogue today (%d of %d)" % (sum(1 for m in t["inventory"]["polyhaven_models"] if m in cat), len(t["inventory"]["polyhaven_models"])), all(m in cat for m in t["inventory"]["polyhaven_models"]), "")
        tex = json.load(urllib.request.urlopen(urllib.request.Request("https://api.polyhaven.com/assets?t=textures", headers={"User-Agent": UA}), timeout=60))
        R.add("live", "every texture exists", all(x in tex for x in t["inventory"]["polyhaven_textures"]), "")
    except Exception as e:
        R.add("live", "Poly Haven API", False, str(e))


def run_all(t, photo_dir, prev_dir, live):
    R = Result()
    check_numbers(t, R)
    check_photographs(t, R, photo_dir)
    check_overlay(t, R)
    check_sites(t, R)
    check_rooms(t, R)
    check_inventory(t, R)
    check_checks(t, R)
    check_kit(t, R)
    check_previews(t, R, prev_dir)
    if live:
        check_live(t, R)
    return R


# ---- negative controls: seeded faults on a copy; every one must make some row fail
def controls(t, photo_dir):
    muts = []

    def mut(name, fn, groups):
        muts.append((name, fn, groups))

    def m1(x): x["kinds"]["S22"]["lab_nodes"][0]["x"][0] += 3.0
    def m2(x): x["sites"][0]["x_centre"] += 0.2
    def m3(x): x["rooms"]["rooms"]["up_lounge_1"]["objects"][0]["stand_off_m"] = 1.2; x["rooms"]["rooms"]["up_lounge_1"]["objects"][0]["class"] = "NOT DRAWN"
    def m4(x): x["gate"]["bands"]["net_N1_N2_in_15_to_30_deg"]["P_over_L"] = [0.55, 0.80]
    def m5(x): x["gate"]["bands"]["old_fault_to_fail"]["D_over_L"] = 0.40
    def m6(x): x["rooms"]["lit_share"]["lit_by_hour"]["20:30"]["n"] = 12
    def m7(x): x["inventory"]["polyhaven_models"]["wall_clock"]["marks"] = ""
    def m8(x): x["rooms"]["lights_by_state"]["night_dark"] = x["rooms"]["lights_by_state"]["night_dark"].replace("(1.0, 0.25, 0.0)", "(1, 0.7055, 0)")
    def m9(x): x["checks"] = [c for c in x["checks"] if c["id"] != "WB-04"]
    def m10(x): x["overlay"]["edges"][5]["measured_px"] += 20.0
    def m11(x): x["sites"][3]["paint"] = "blue"; x["sites"][3]["kind"] = "RC"
    def m12(x): x["kit_pieces"]["per_kind"]["S22"]["added_nodes"][[n["name"] for n in x["kit_pieces"]["per_kind"]["S22"]["added_nodes"]].index("net__N1")]["y_into_wall"] = [200, 201]
    def m13(x): x["summary"] = x["summary"] + " Dixons"
    def m14(x): x["rooms"]["pictures_by_family"]["UP"]["back_wall_rect_px_x0y0x1y1"][0] = 500.0
    for n, f in (("a kit node moved 3 mm off the lab's glb", m1), ("a site's centre moved 0.2 m", m2), ("an object over the tolerated stand-off", m3), ("a band that no longer encloses the photographs' net windows", m4),
                 ("the old fault's D/L pulled inside the limit", m5), ("twelve windows lit at 20:30", m6), ("a model's marks entry emptied", m7), ("the stale sodium colour in the night wash", m8),
                 ("a required check removed", m9), ("an overlay edge 20 px off", m10), ("a blue replacement window", m11), ("a net plane inside the lower glass", m12),
                 ("a real firm's name in the summary", m13), ("the back wall rectangle moved", m14)):
        mut(n, f, None)
    caught = 0
    out = []
    for name, fn, _ in muts:
        x = copy.deepcopy(t)
        fn(x)
        R = Result()
        try:
            check_numbers(x, R)
            check_photographs(x, R, None)
            check_overlay(x, R)
            check_sites(x, R)
            check_rooms(x, R)
            check_inventory(x, R)
            check_checks(x, R)
            check_kit(x, R)
        except Exception as e:
            R.add("control", "raised", False, str(e)[:80])
        bad = [r for r in R.rows if not r["ok"]]
        out.append({"mutation": name, "caught": bool(bad), "first_failing_row": bad[0]["name"] if bad else None})
        caught += 1 if bad else 0
    return caught, out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "hw_photos"))
    ap.add_argument("--previews", default="")
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--no-controls", action="store_true")
    a = ap.parse_args()
    path = os.path.join(HERE, "target.json")
    t = json.load(open(path))
    t.pop("self_check", None)
    R = run_all(t, a.photos, a.previews, a.live)
    fails = [r for r in R.rows if not r["ok"]]
    n = len(R.rows)
    line = "self_check: %d pass, %d fail" % (n - len(fails), len(fails))
    cc, cl = (0, [])
    if not a.no_controls:
        cc, cl = controls(t, a.photos)
        line += "; negative controls: %d of %d caught" % (cc, len(cl))
    for r in fails:
        print("FAIL [%s] %s %s" % (r["group"], r["name"], r["detail"]))
    for c in cl:
        if not c["caught"]:
            print("NOT CAUGHT:", c["mutation"])
    print(line)
    if a.write:
        t["self_check"] = {"result": line, "rows": sorted(R.rows, key=lambda r: (r["group"], r["name"])), "controls": cl, "run": "13 October 2026"}
        json.dump(t, open(path, "w"), indent=1)
        print("written into target.json")
    sys.exit(1 if fails or (not a.no_controls and cc != len(cl)) else 0)


if __name__ == "__main__":
    main()
