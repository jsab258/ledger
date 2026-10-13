"""a-board: the self-check. python self_check.py [--live] [--previews] [--photos DIR] [--no-controls]"""
import json
import math
import os
import re
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_check as K
import sd_family as SF
import sd_place as PL

V = "AB1"
LIVE = "--live" in sys.argv


def photos_dir():
    if "--photos" in sys.argv:
        return sys.argv[sys.argv.index("--photos") + 1]
    return os.path.join(L.REPO, "..", "ledger-scratch", "street-dressing", "a-board")


EYES = ("f_eye", "r_eye", "f_eye_l", "r_eye_l")


def world_local(ps, name):
    i = ps.index[name]
    W = np.vstack([pc.V for pc in ps.pieces[i]])
    return W, K.local_vertices(ps, name)


def tip(ps, name):
    """The outer end of a screw eye in world coordinates: the vertices furthest from the leaf's middle (largest local x for a right eye, smallest for a left one), averaged."""
    W, Lc = world_local(ps, name)
    if name.endswith("_l"):
        m = Lc[:, 0] <= Lc[:, 0].min() + 0.01
    else:
        m = Lc[:, 0] >= Lc[:, 0].max() - 0.01
    return W[m].mean(0)


def lean_of(ps, name, top_local_z, bot_local_z):
    """The leaf's lean off the vertical, from the world positions of its inner top and inner bottom edges."""
    W, Lc = world_local(ps, name)
    inner = np.abs(Lc[:, 1]) < 0.05
    mt, mb = inner & (Lc[:, 2] > top_local_z - 0.05), inner & (Lc[:, 2] < bot_local_z + 0.05)
    if not mt.any() or not mb.any():
        raise ValueError("%s has no inner top or bottom edge to read the lean from" % name)
    top = W[mt].mean(0)
    bot = W[mb].mean(0)
    d = top - bot
    return math.degrees(math.atan2(abs(d[1]), abs(d[2]))), top, bot


def hours_lines(hours):
    days = ["mon", "tue", "wed", "thu", "fri", "sat"]
    opens = {hours[d][0] for d in days}
    closes = [hours[d][1] for d in days]
    c0 = max(set(closes), key=closes.count)

    def op(h):
        return ("%d.%02d" % (int(h), int(round((h - int(h)) * 60)))) if h != int(h) else "%d" % int(h)

    def cl(h):
        return "%d" % (h - 12 if h > 12 else h)
    out = ["MON TO SAT %s TO %s" % (op(min(opens)), cl(c0))] if len(opens) == 1 else []
    for d in days:
        if hours[d][1] != c0:
            out.append("%s SHUT %s" % (d.upper(), cl(hours[d][1])))
    return out


def line_width(text, h, f):
    return len(text) * f * h


def extra(T, rows):
    ps = K._ps_cache(T["variants"]["AB1"]["parts"])
    p2 = K._ps_cache(T["variants"]["AB2"]["parts"])
    tx = T["text"]
    pl = T["placement"]
    pm = json.load(open(os.path.join(HERE, "photo_measurements.json")))
    F1, A1 = pm["P1"]["features"], pm["P1"]["arch_features"]
    # ---- the leaf and the pose, from the built parts
    ml, mh = K.local_bbox(ps, "f_main")
    LW = float(mh[0] - ml[0])
    LLn = float(mh[2])
    ARCH = float(ml[2])
    lean_f, topf, botf = lean_of(ps, "f_main", mh[2], ml[2])
    lean_r, topr, botr = lean_of(ps, "r_main", mh[2], ml[2])
    rows.near("detail", "detail/the front leaf stands 12 degrees off the vertical (worked from its edges' world positions)", lean_f, 12.0, 0.05, unit="deg")
    rows.near("detail", "detail/the back leaf stands the same (12 degrees)", lean_r, 12.0, 0.05, unit="deg")
    rows.near("detail", "detail/the leaves meet on the ridge line (their inner top edges, in y)", abs(topf[1] - topr[1]), 0.0, 0.6)
    rows.near("detail", "detail/the leaves meet on the ridge line (their inner top edges, in z)", abs(topf[2] - topr[2]), 0.0, 0.6)
    flo, fhi = ps.bbox(only=[n for n in ps.names if n.startswith("f_") and n not in EYES])
    rlo, rhi = ps.bbox(only=[n for n in ps.names if n.startswith("r_") and n not in EYES])
    rows.near("detail", "detail/the two leaves mirror each other across y = 0", abs(flo[1] + rhi[1]) + abs(fhi[1] + rlo[1]), 0.0, 0.3)
    same = all(np.allclose(np.sort(np.ptp(K.local_vertices(ps, "f_" + s), axis=0)), np.sort(np.ptp(K.local_vertices(ps, "r_" + s), axis=0)), atol=0.05) for s in ("main", "foot_l", "foot_r", "stile_l", "stile_r", "rail", "hplate_l", "hplate_r", "eye", "eye_l"))
    rows.add("detail", "detail/every part of the back leaf is the front leaf's size", same, "")
    lo, hi = ps.bbox()
    rows.near("detail", "detail/the board stands on the paving (lowest point z = 0)", lo[2], 0.0, 0.5)
    ground = [ps.part_bbox(n)[0][2] for n in ("f_foot_l", "f_foot_r", "r_foot_l", "r_foot_r")]
    rows.add("detail", "detail/all four feet reach the paving", max(ground) <= 0.5, str([round(g, 2) for g in ground]))
    rows.add("detail", "detail/ply is 12 mm and the leaf is 600 wide (read in its own frame)", abs(float(mh[1] - ml[1]) - 12.0) < 0.05 and abs(LW - 600.0) < 0.05, "%.2f x %.2f" % (mh[1] - ml[1], LW))
    # ---- the foot arch: wider at the ground than at the top, symmetrical, and the photograph's ratio of arch to leaf at the same rows
    fl_lo, fl_hi = K.local_bbox(ps, "f_foot_l")
    fr_lo, fr_hi = K.local_bbox(ps, "f_foot_r")
    bl_lo, bl_hi = K.local_bbox(ps, "f_foot_l", {"axis": "z", "lo": -1, "hi": 1})
    br_lo, br_hi = K.local_bbox(ps, "f_foot_r", {"axis": "z", "lo": -1, "hi": 1})
    base = float(br_lo[0] - bl_hi[0])
    top = float(fr_lo[0] - fl_hi[0])
    rows.add("detail", "detail/the arch is wider at the ground than at its flat top (it flares)", base > top + 40.0, "base %.1f, top %.1f" % (base, top))
    rows.near("detail", "detail/the arch is centred on the leaf", float(fl_hi[0] + fr_lo[0]), 0.0, 0.5)
    rows.near("detail", "detail/the feet reach the arch's height (58) and the main panel begins there", float(fl_hi[2] - ARCH), 0.0, 0.5)
    leaf_px = F1["right_bot"]["px"] - F1["left_bot"]["px"]
    arch_px = A1["arch_base_right_x"]["px"] - A1["arch_base_left_x"]["px"]
    rows.near("photo", "photo/arch width over leaf width at the feet against P1 (same rows)", base / LW, arch_px / leaf_px, 0.025, unit="")
    # the photograph's own numbers: two feet of equal width in the picture
    lf = A1["arch_base_left_x"]["px"] - F1["left_bot"]["px"]
    rf = F1["right_bot"]["px"] - A1["arch_base_right_x"]["px"]
    rows.add("photo", "photo/P1's two feet are of equal width within 3 px (the arch is centred)", abs(lf - rf) <= 3.0, "%.1f and %.1f px" % (lf, rf))
    rows.add("photo", "photo/P1's turned copy: the left and right edges are within 3 px of vertical", abs(F1["left_top"]["px"] - F1["left_bot"]["px"]) <= 3.0 and abs(F1["right_top"]["px"] - F1["right_bot"]["px"]) <= 3.0,
             "left %.1f and %.1f, right %.1f and %.1f" % (F1["left_top"]["px"], F1["left_bot"]["px"], F1["right_top"]["px"], F1["right_bot"]["px"]))
    # ---- the second screw eye (S1 shows one in each edge): level with and the mirror of the right one, the chain on the right only
    el_f, er_f = tip(ps, "f_eye_l"), tip(ps, "f_eye")
    el_r, er_r = tip(ps, "r_eye_l"), tip(ps, "r_eye")
    xlo, xhi = K.local_bbox(ps, "f_eye_l")
    rlo_, rhi_ = K.local_bbox(ps, "f_eye")
    rows.near("detail", "detail/the left screw eye runs from x -312 to -296 in the leaf's frame (the right one's mirror)", float(abs(xlo[0] + 312.0) + abs(xhi[0] + 296.0)), 0.0, 0.1)
    rows.near("detail", "detail/the left eye is the right eye's mirror (same height, same depth in the edge)", float(abs(xlo[2] - rlo_[2]) + abs(xhi[2] - rhi_[2]) + abs(xlo[1] - rlo_[1]) + abs(xhi[1] - rhi_[1])), 0.0, 0.1)
    rows.add("detail", "detail/the left eyes are level with the right ones (the tips at one height, z about 592)", abs(el_f[2] - er_f[2]) < 0.5 and abs(el_r[2] - er_r[2]) < 0.5,
             "left tips z %.1f and %.1f, right tips z %.1f and %.1f" % (el_f[2], el_r[2], er_f[2], er_r[2]))
    chp = [p for p in T["variants"]["AB1"]["parts"] if p["id"] == "chain"][0]["pts"]
    rows.add("detail", "detail/the chain stays on the right eyes only (no chain point near a left eye)", min(float(np.linalg.norm(np.array(q, float) - t)) for q in chp for t in (el_f, el_r)) > 200.0,
             "nearest chain point to a left tip %.0f mm" % min(float(np.linalg.norm(np.array(q, float) - t)) for q in chp for t in (el_f, el_r)))
    # ---- the chain: ends on the eyes, slack, hangs free
    ch = [p for p in T["variants"]["AB1"]["parts"] if p["id"] == "chain"][0]["pts"]
    P = np.array(ch, float)
    ta, tb = tip(ps, "f_eye"), tip(ps, "r_eye")
    rows.near("detail", "detail/the chain starts on the front eye's tip", float(np.linalg.norm(P[0] - ta)), 0.0, 1.5)
    rows.near("detail", "detail/the chain ends on the back eye's tip", float(np.linalg.norm(P[-1] - tb)), 0.0, 1.5)
    ln = float(np.linalg.norm(np.diff(P, axis=0), axis=1).sum())
    span = float(np.linalg.norm(ta - tb))
    rows.at_least("detail", "detail/the chain is slack: its length over the span between the eyes is at least 1.15", ln / span, 1.15, unit="")
    rows.at_least("detail", "detail/the chain hangs clear of the paving (lowest axis point above 150 mm)", float(P[:, 2].min()), 150.0)
    rows.add("detail", "detail/the chain's eyes are level (the two tips at the same height)", abs(ta[2] - tb[2]) < 1.0, "%.2f" % abs(ta[2] - tb[2]))
    others = [p for p in T["variants"]["AB1"]["parts"] if p["id"] not in ("chain", "f_eye", "r_eye")]
    po = K._ps_cache(others)
    pts = []
    for a, b in zip(P[:-1], P[1:]):
        n = max(2, int(np.linalg.norm(b - a) // 4))
        for t in np.linspace(0, 1, n):
            pts.append(a + (b - a) * t)
    inside = L.solid_inside(po, np.array(pts))
    rows.add("detail", "detail/the chain's axis passes through no leaf, batten, hinge or foot", not inside.any(), "%d of %d sample points inside" % (int(inside.sum()), len(pts)))
    # ---- the text
    W_leaf = LW
    ok_fit, bad = True, []
    for ln_ in tx["lines"]:
        w = line_width(ln_["text"], ln_["h"], tx["cap_width_factor"])
        if ln_["price"]:
            w += line_width(ln_["price"], ln_["h"], tx["cap_width_factor"]) + tx["gap_mm"]
        if w > W_leaf - 2 * tx["margin_mm"]:
            ok_fit = False
            bad.append((ln_["id"], round(w)))
    rows.add("text", "text/every line fits the leaf's width less the margins", ok_fit, "too wide: %s" % bad if bad else "widest %.0f of %.0f" % (max(line_width(l["text"], l["h"], tx["cap_width_factor"]) + (line_width(l["price"], l["h"], tx["cap_width_factor"]) + tx["gap_mm"] if l["price"] else 0) for l in tx["lines"]), W_leaf - 2 * tx["margin_mm"]))
    ls = sorted(tx["lines"], key=lambda l: -l["z_top"])
    gaps = [ls[i]["z_top"] - ls[i]["h"] - ls[i + 1]["z_top"] for i in range(len(ls) - 1)]
    rows.add("text", "text/no two lines touch (at least 10 mm between)", min(gaps) >= 10.0, "smallest gap %.0f" % min(gaps))
    rows.add("text", "text/the lines lie between the arch's top plus margin and the ridge less margin", ls[-1]["z_top"] - ls[-1]["h"] >= ARCH + tx["margin_mm"] and ls[0]["z_top"] <= LLn - tx["margin_mm"], "lowest %.0f, highest %.0f" % (ls[-1]["z_top"] - ls[-1]["h"], ls[0]["z_top"]))
    hc = json.load(open(os.path.join(L.REPO, "production", "specs", "hook-cast.json")))
    want = hours_lines(hc["areas"]["fish_market"]["hours"])
    have = [l["text"] for l in tx["lines"] if l["id"].startswith("hours")]
    rows.add("text", "text/the hours lines are the fish market's own hours in hook-cast.json", have == want, "board %s, cast %s" % (have, want))
    rows.add("text", "text/no Sunday hours on the board (the market does not open)", not any("SUN" in l["text"] for l in tx["lines"]) and "sun" not in hc["areas"]["fish_market"]["hours"], "")
    note = open(os.path.join(L.REPO, "production", "research", "shop-window-interiors", "FISHMONGER-2026-10-03.md"), encoding="utf-8").read()
    m = re.search(r"about £(\d\.\d\d)/lb", note)
    cod = [l for l in tx["lines"] if l["id"] == "cod"][0]
    rows.add("text", "text/the cod price is the research note's figure (2.60 a pound)", bool(m) and cod["price"] == "%s LB" % m.group(1), "note %s, board %s" % (m.group(1) if m else None, cod["price"]))
    priced = [l for l in tx["lines"] if l["price"]]
    rows.add("text", "text/every price names its basis and only the cod is sourced", all(l.get("basis") for l in priced) and [l["id"] for l in priced if l["basis"].startswith("sourced")] == ["cod"], str([l["id"] for l in priced if l["basis"].startswith("sourced")]))
    rows.add("text", "text/every price is per pound or each", all(l["price"].endswith(" LB") or l["price"].endswith(" EACH") for l in priced), "")
    rows.add("text", "text/no shop name on the board", tx["shop_name"] is None and not any(re.search(r"LTD|& SON|SONS|BROS", l["text"]) for l in tx["lines"]), "")
    # ---- AB2 and P2: ratio of the front leaf's drawing to the photograph's edges
    f2lo, f2hi = p2.bbox(only=[n for n in p2.names if n.startswith("f_") and n != "f_eye"])
    ratio_d = float((f2hi[0] - f2lo[0]) / (f2hi[2] - f2lo[2]))
    ph2 = [p for p in T["photos"] if p["id"] == "P2"][0]
    F2 = {f["id"]: f for f in ph2["features"]}
    wpx = F2["right_x"]["px"] - F2["left_x"]["px"]
    hpx = F2["bottom_y"]["px"] - F2["top_y"]["px"]
    rows.near("photo", "photo/P2 width over height against AB2's front leaf drawing", ratio_d, wpx / hpx, ph2["ratio"]["tol"], unit="")
    rows.near("photo", "photo/P2's stored ratio is its own recorded edges'", ph2["ratio"]["width_over_height"], wpx / hpx, 0.001, unit="")
    ob = ph2["object_box"]
    rows.add("photo", "photo/P2's measuring boxes lie on the board (inside the object box with 8 px margin)", all(f["box"][0] >= ob[0] - 8 and f["box"][1] >= ob[1] - 8 and f["box"][2] <= ob[2] + 8 and f["box"][3] <= ob[3] + 8 for f in ph2["features"]), str(ob))
    # ---- the slot
    kerb_clear = (pl["z_m"] - pl["across_half_mm"] / 1000.0 - pl["kerb_back_z_m"]) * 1000.0
    shop_gap = (pl["stallriser_line_z_m"] - (pl["z_m"] + pl["across_half_mm"] / 1000.0)) * 1000.0
    rows.at_least("placement", "placement/clear walking width on the kerb side", kerb_clear, pl["min_clear_mm"])
    rows.at_least("placement", "placement/the board does not touch the stallriser line (gap on the shop side)", shop_gap, 20.0)
    along = (hi[1] - lo[1]) / 2.0
    rows.near("placement", "placement/half the depth used in the slot is the built board's", pl["along_half_mm"], along, 1.0)
    rows.near("placement", "placement/half the width used in the slot is the leaf and the eye's", pl["across_half_mm"], (W_leaf / 2.0 + 12.0), 0.5)
    x0, x1 = pl["x_m"] - pl["along_half_mm"] / 1000.0, pl["x_m"] + pl["along_half_mm"] / 1000.0
    rows.at_least("placement", "placement/the board's end is clear of the party pilaster (Rita's side)", (pl["pilaster_x_m"] - pl["pilaster_half_mm"] / 1000.0 - x1) * 1000.0, pl["pilaster_gap_min_mm"])
    rows.at_least("placement", "placement/the board is clear of the awning's end", (x0 - pl["awning_x_m"][1]) * 1000.0, pl["awning_gap_min_mm"])
    ff = hc["places"]["fish_front"]
    d = ((pl["x_m"] - ff["x_m"]) ** 2 + (pl["z_m"] - ff["z_m"]) ** 2) ** 0.5
    rows.near("placement", "placement/the cast's fish_front spot is the one in hook-cast.json", ff["x_m"], pl["fish_front"]["x_m"], 0.001, unit="m")
    rows.at_least("placement", "placement/the board is at least 1 m from where the cast stands outside the fish market", d, pl["fish_front"]["min_m"], unit="m")
    shopsT = json.load(open(os.path.join(L.REPO, PL.SHOPS_REL)))
    fish = [s for s in shopsT["shops"] if s["id"] == "fish_market"][0]
    dc, sc_ = fish["centres_street_x_m"]["shop_door"], fish["centres_street_x_m"]["side_door"]
    rows.near("placement", "placement/the fish market's shop door is the shopfronts target's (centre 10.797), not the cast's note (9.4)", pl["fish_door_x_m"], dc, 0.001, unit="m")
    rows.near("placement", "placement/the fish market's side door is the shopfronts target's (centre 9.822)", pl["fish_side_door_x_m"], sc_, 0.001, unit="m")
    door_edge = dc + pl["fish_door_w_m"] / 2.0
    rows.at_least("placement", "placement/the board's near end is clear of the fish market's shop door edge (x %.3f)" % door_edge, x0 - door_edge, pl["door_gap_min_m"], unit="m")
    rows.add("placement", "placement/the reasons name the shop door's x 10.294 to 11.300 and 2.9 m, and no longer 'about x 9.4' or '5 m'", "10.294 to 11.300" in " ".join(pl["reasons"]) and abs(round(x0 - door_edge, 1) - 2.9) < 1e-9 and "2.9 m from the shop door" in " ".join(pl["reasons"])
             and "about x 9.4" not in " ".join(pl["reasons"]) and "stands 5 m from it" not in " ".join(pl["reasons"]), "gap %.2f m" % (x0 - door_edge))
    rows.add("placement", "placement/the slot's wording says the leaves' side edges face the stallriser, not the feet", "side edges" in pl["slot"] and "back leaf's feet" not in pl["slot"], "")
    n1 = [n for n in T["numbers"] if n["id"] == "N1"][0]
    rows.add("numbers", "numbers/N1's source error is the pavement board's band (500 to 700 wide: at least +-100) and its kind is Judgement", n1["kind"] == "Judgement" and n1.get("source_error", 0) >= 100.0, "source error %s" % n1.get("source_error"))
    scaled = [n["id"] for n in T["numbers"] if n.get("scaled_on") == "N1"]
    rows.add("numbers", "numbers/N2, N4, N5, N8, N10 and N11 are marked scaled on the assumed width, each with a 17 percent source error and its own builder tolerance", scaled == ["N2", "N4", "N5", "N8", "N10", "N11"]
             and all(abs(n["source_error"] - 0.17 * n["value"]) < 0.06 and "tol" in n and n["kind"] == "Photo, scaled on the assumed width" for n in T["numbers"] if n["id"] in scaled), str(scaled))
    pose = pl["poses"][0]
    rows.add("placement", "placement/the pose is the stated slot (x, z, yaw 90)", abs(pose["x_m"] - pl["x_m"]) < 1e-9 and abs(pose["z_m"] - pl["z_m"]) < 1e-9 and pose["yaw_deg"] == pl["yaw_deg"], "")
    rows.add("placement", "placement/the board is in bay 1 (x 9 to 15) of the east parade, the fishmonger's (RULINGS 3 Oct)", 9.0 <= x0 and x1 <= 15.0, "x %.2f to %.2f" % (x0, x1))
    sc = json.load(open(os.path.join(L.REPO, "production", "specs", "vignette-scene.json")))
    old = [i for i in sc["held_props"]["items"] if i.get("asset") == "pavement_sign"][0]
    oz = 3.0 + old["z_from_kerb_face_m"]
    oh = old["dims_m"][0] / 2.0
    o_kerb = (oz - oh - pl["kerb_back_z_m"]) * 1000.0
    o_shop = (pl["stallriser_line_z_m"] - (oz + oh)) * 1000.0
    rows.add("reuse", "reuse/the scene's old line leaves under a walking person's 0.68 m on both sides", o_kerb < pl["walking_person_mm"] and o_shop < pl["walking_person_mm"], "kerb side %.0f, shop side %.0f" % (o_kerb, o_shop))
    rows.add("reuse", "reuse/the old line is the one this slot replaces (x 15.2, 1.1 m from the kerb face, yaw 90)", abs(old["x_m"] - pl["old"]["x_m"]) < 1e-6 and abs(old["z_from_kerb_face_m"] - pl["old"]["z_from_kerb_face_m"]) < 1e-6 and old["yaw_deg"] == pl["yaw_deg"], "")
    rows.add("reuse", "reuse/the scene's placeholder is not the target's size (0.68 x 0.90 x 0.36)", abs(old["dims_m"][0] * 1000 - W_leaf) > 50.0 and abs(old["dims_m"][2] * 1000 - (hi[1] - lo[1])) > 50.0, str(old["dims_m"]))
    rec = json.load(open(os.path.join(HERE, "polyhaven_checked_raw.json")))["standing_chalkboard_01"]
    rows.add("reuse", "reuse/Poly Haven's standing chalkboard is 1.5 m tall, taller than this board by 400 mm or more", rec["dimensions"][2] - (hi[2] - lo[2]) >= 400.0, "%.0f against %.0f" % (rec["dimensions"][2], hi[2] - lo[2]))
    rows.add("reuse", "reuse/the chalkboard record is CC0 and not NoAI-tagged", "CC0" in rec["licence"] and "noai" not in json.dumps(rec).lower(), str(rec.get("authors")))
    rows.add("detail", "detail/every part's material is defined", all(p["material"] in T["materials"] for v in T["variants"].values() for p in v["parts"]), "")
    rows.add("detail", "detail/no mark: no stamp, label or sign part", not any(any(w in n for w in ("stamp", "label", "logo", "sign")) for n in ps.names), "")
    # ---- live
    if LIVE:
        pdir = photos_dir()
        pr = [x for x in T["photos"] if x["id"] == "P2"][0]
        p = os.path.join(pdir, pr["file"])
        if os.path.exists(p):
            g = L.load_gray(p)
            for f in pr["features"]:
                spec = f["measure"]
                pos, con, spread = L.edge_pos(g, spec["axis"], spec["band"], spec["win"], spec.get("pol", "any"))
                rows.add("live", "live/P2/%s re-measured" % f["id"], abs(pos - f["px"]) <= 0.75, "pixels give %.2f, recorded %.2f" % (pos, f["px"]))
        else:
            rows.add("live", "live/P2/photograph present", False, "not found: %s" % p)
        pr1 = os.path.join(pdir, "P1rot.jpg")
        if os.path.exists(pr1):
            g1 = L.load_gray(pr1)
            for fid, f in A1.items():
                pos, con, spread = L.edge_pos(g1, f["axis"], f["band"], f["win"], f.get("pol", "any"))
                rows.add("live", "live/P1/%s re-measured (the arch's base)" % fid, abs(pos - f["px"]) <= 0.75, "pixels give %.2f, recorded %.2f" % (pos, f["px"]))
        else:
            rows.add("live", "live/P1/turned copy present for the arch's base", False, "not found: %s" % pr1)
        tmp = tempfile.mkdtemp()
        for sid, gid in (("S1", "3671864"), ("S2", "6913397")):
            pg = L.geograph_page(gid, tmp)
            s = [x for x in T["sources"] if x["id"] == sid][0]
            rows.add("live", "live/%s page still says %s and %s, free licence" % (sid, s["taken"], s["author"]), pg.get("taken") == s["taken"] and s["author"] in (pg.get("author") or "") and "by-sa/2.0" in (pg.get("licence") or ""),
                     "page: %s, %s, %s" % (pg.get("taken"), pg.get("author"), pg.get("licence")))


def extra_controls(T):
    def chain_mut(t, f):
        for p in t["variants"][V]["parts"]:
            if p["id"] == "chain":
                f(p)

    def shift_chain(p):
        p["pts"] = [[q[0] - 330.0, q[1], q[2]] for q in p["pts"]]

    def straighten(p):
        a, b = p["pts"][0], p["pts"][-1]
        n = len(p["pts"]) - 1
        p["pts"] = [[a[i] + (b[i] - a[i]) * k / n for i in range(3)] for k in range(n + 1)]

    def lift(p):
        p["pts"] = [[q[0], q[1], q[2] - 560.0] for q in p["pts"]]

    def leaf_roll(t, deg):
        for p in t["variants"][V]["parts"]:
            if p["id"].startswith("f_"):
                p["xf"]["rot"][2] = -deg

    return [
        ("detail: the front leaf leaning 25 degrees", lambda t: leaf_roll(t, 25.0), "detail/the front leaf stands 12 degrees"),
        ("detail: the back leaf's foot made 10 mm longer than the front's", lambda t: [p.__setitem__("s", [p["s"][0], p["s"][1], p["s"][2] + 10.0]) for p in t["variants"][V]["parts"] if p["id"] == "r_hplate_l"], "detail/every part of the back leaf is the front leaf's size"),
        ("detail: the left foot cut back (the arch 302 wide at the ground)", lambda t: [p.__setitem__("poly", [[(-120.0 if q[0] > -299 and q[1] == 0.0 else q[0]), q[1]] for q in p["poly"]]) for p in t["variants"][V]["parts"] if p["id"] == "f_foot_l"], "photo/arch width over leaf width"),
        ("detail: the arch's flare taken out (both feet's sides straight)", lambda t: [p.__setitem__("poly", [[((-138.0 if p["id"] == "f_foot_l" else 138.0) if (abs(q[0]) < 299 and q[1] < 58.0) else q[0]), q[1]] for q in p["poly"]]) for p in t["variants"][V]["parts"] if p["id"] in ("f_foot_l", "f_foot_r")], "detail/the arch is wider at the ground"),
        ("detail: the chain pulled through the leaves", lambda t: chain_mut(t, shift_chain), "detail/the chain's axis passes through no"),
        ("detail: the chain pulled straight (no slack)", lambda t: chain_mut(t, straighten), "detail/the chain is slack"),
        ("detail: the chain dropped onto the paving", lambda t: chain_mut(t, lift), "detail/the chain hangs clear of the paving"),
        ("detail: the chain's end off the back eye", lambda t: chain_mut(t, lambda p: p["pts"].__setitem__(-1, [p["pts"][-1][0], p["pts"][-1][1] + 30.0, p["pts"][-1][2]])), "detail/the chain ends on the back eye"),
        ("text: a line made too long for the leaf", lambda t: t["text"]["lines"][5].__setitem__("text", "DRESSED CRAB AND LOBSTER"), "text/every line fits the leaf"),
        ("text: a line pushed onto its neighbour", lambda t: t["text"]["lines"][2].__setitem__("z_top", 790.0), "text/no two lines touch"),
        ("text: the hours changed to a Sunday opening", lambda t: t["text"]["lines"][6].__setitem__("text", "SUN TO SAT 8 TO 4"), "text/the hours lines are the fish market's"),
        ("text: the cod price changed", lambda t: t["text"]["lines"][1].__setitem__("price", "3.60 LB"), "text/the cod price is the research note's"),
        ("text: a second price marked as sourced", lambda t: t["text"]["lines"][2].__setitem__("basis", "sourced: a shop's price list"), "text/every price names its basis and only the cod is sourced"),
        ("text: a shop name added to a line", lambda t: t["text"]["lines"][0].__setitem__("text", "SMITH & SON FRESH FISH"), "text/no shop name on the board"),
        ("photograph: AB2 made 30 percent wider", lambda t: K.scale_all(t, "AB2", 0, 1.3), "photo/P2 width over height"),
        ("photograph: P2's stored ratio changed", lambda t: [p["ratio"].__setitem__("width_over_height", 0.5) for p in t["photos"] if p["id"] == "P2"], "photo/P2's stored ratio is its own"),
        ("photograph: P1's right foot 25 mm shorter", lambda t: K.shift_part(t, V, "f_foot_r", [0, 0, 25.0]), "photo/P1/foot_right_y"),
        ("placement: the board moved to the line of the pilaster", lambda t: t["placement"].__setitem__("x_m", 14.9), "placement/the board's end is clear of the party pilaster"),
        ("placement: the board moved under the awning's end", lambda t: t["placement"].__setitem__("x_m", 13.7), "placement/the board is clear of the awning"),
        ("placement: the board put where the cast stands", lambda t: t["placement"].__setitem__("x_m", 12.2), "placement/the board is at least 1 m from where the cast stands"),
        ("placement: the board in the middle of the pavement (the scene's old line)", lambda t: t["placement"].__setitem__("z_m", 4.1), "placement/clear walking width on the kerb side"),
        ("placement: the board against the stallriser", lambda t: t["placement"].__setitem__("z_m", 4.7), "placement/the board does not touch the stallriser line"),
        ("detail: the left screw eye moved 10 mm along the edge", lambda t: K.shift_part(t, V, "f_eye_l", [10.0, 0, 0]), "detail/the left screw eye runs from x -312 to -296"),
        ("detail: the left screw eye 40 mm lower than the right", lambda t: K.shift_part(t, V, "f_eye_l", [0, 0, -40.0]), "detail/the left eyes are level with the right ones"),
        ("detail: the left screw eye set deeper in the edge than the right", lambda t: K.shift_part(t, V, "r_eye_l", [0, 3.0, 0]), "detail/the left eye is the right eye's mirror"),
        ("detail: the chain hooked to the left eye as well", lambda t: chain_mut(t, lambda p: p["pts"].__setitem__(8, [float(v) for v in tip(K._ps_cache(t["variants"][V]["parts"]), "f_eye_l")])), "detail/the chain stays on the right eyes only"),
        ("numbers: N1 given the old +-15 source error", lambda t: [n.__setitem__("source_error", 15.0) for n in t["numbers"] if n["id"] == "N1"], "numbers/N1's source error is the pavement board's band"),
        ("numbers: N1 made a measured Photo number", lambda t: [n.__setitem__("kind", "Photo") for n in t["numbers"] if n["id"] == "N1"], "numbers/N2 source error covers"),
        ("numbers: N5 marked plain Photo again", lambda t: [(n.__setitem__("kind", "Photo"), n.pop("scaled_on", None)) for n in t["numbers"] if n["id"] == "N5"], "numbers/N2, N4, N5, N8, N10 and N11 are marked scaled"),
        ("placement: the fish market's door put back at the cast's x 9.4", lambda t: t["placement"].__setitem__("fish_door_x_m", 9.4), "placement/the fish market's shop door is the shopfronts target's"),
        ("placement: the fish market's side door moved", lambda t: t["placement"].__setitem__("fish_side_door_x_m", 9.4), "placement/the fish market's side door is the shopfronts target's"),
        ("placement: the board moved to 0.9 m from the shop door's edge", lambda t: t["placement"].__setitem__("x_m", 12.4), "placement/the board's near end is clear of the fish market's shop door edge"),
        ("placement: the old 'about x 9.4 and 5 m' wording put back in the reasons", lambda t: t["placement"]["reasons"].append("the fish market's doorway is at about x 9.4 and the board stands 5 m from it"), "placement/the reasons name the shop door's"),
        ("placement: the old 'back leaf's feet' wording put back", lambda t: t["placement"].__setitem__("slot", t["placement"]["slot"] + " its back leaf's feet 0.063 m clear"), "placement/the slot's wording says"),
        ("placement: the pose moved off the stated slot", lambda t: PL.set_pose(t, "AB1", x_m=14.0), "placement/the pose is the stated slot"),
        PL.ctl("placement (shared check): the board turned to face the road (yaw 0)", "AB1", "place/AB1/front faces", yaw_deg=0.0),
        PL.ctl("placement (shared check): the board stood in the carriageway", "AB1", "place/AB1/feet lie in zone", z_m=2.5),
        PL.ctl("placement (shared check): the board stood against the party pilaster", "AB1", "place/AB1/clear of every street piece", x_m=14.75),
        PL.ctl("placement (shared check): the board stood in the shop door's approach", "AB1", "place/AB1/clear of every shop and house door zone", x_m=11.0),
        PL.ctl("placement (shared check): the board stood mid-pavement (no 0.68 m either side)", "AB1", "place/AB1/walking strip", z_m=4.05),
        ("placement: the board's width wrong in the slot", lambda t: t["placement"].__setitem__("across_half_mm", 400.0), "placement/half the width used in the slot"),
    ]


if __name__ == "__main__":
    spec = dict(V=V, leaf="f_hplate_l", leaf_move=[0, -40, 0], bridge=["f_foot_l", "f_foot_r", "r_foot_l", "r_foot_r"], join=("f_stile_l", "f_main"), join_move=[0, 40, 0], overlap=("f_rail", [0, -14, 0]), photo_squeeze=0.7,
                blocker={"front leaf outer face": "f_main", "front leaf feet": "f_foot_l"}, number_id="N2")
    sys.exit(1 if SF.selfcheck_main(HERE, "a-board", extra, extra_controls, spec) else 0)
