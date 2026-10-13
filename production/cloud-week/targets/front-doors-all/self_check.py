"""Tests the front-doors-all target against its own sources before anything is built.
  usage: self_check.py [--live] [--photos DIR] [--previews] [--write] [--no-controls]
Without options it runs offline: numbers equal 3.1's as built, every photograph's recorded boxes give the fractions the kinds use, the street's table, the geometry
of the drawing (nothing overlaps that should not, nothing shows through, nothing floats), every record of the checks list, the texts (no maker's name, the lantern colour,
no em dash), and the negative controls (wrong copies that must each make a row fail).
  --live      re-derives the street from tools/art-recipes/terrace-front.py and the windows target, compares the wear numbers with the wear target, fetches the photographs
              (Geograph and one Commons file) and re-reads their pages, and re-measures the recorded boxes on the pixels (sizes, colour medians, edges of the leaf, the slit, the plates).
  --photos D  the directory of fetched photographs (default $TMPDIR/td_photos); --live fetches what is missing.
  --previews  checks the preview files in production/previews/cloud-week/refs/front-doors-all/ (size, pixels, masks) and their credits in TARGET.md.
  --write     writes the result into target.json under self_check.
Prints a result line naming the options and both counts; exits 1 on any failure or any uncaught control."""
import argparse
import copy
import json
import os
import re
import sys

import numpy as np
from shapely.geometry import box as sbox
from shapely.ops import unary_union

import target_drawing as TD
import td_checks as TC
import td_data as D
import td_kinds as TK
from td_common import BLOCKLIST, DOOR31, HERE, LANTERN_LINEAR, PREVIEWS, ROOT, STALE_NIGHT, TARGET_JSON, WEAR_T, blocklist_hits, load_json, strings, words

sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(ROOT, "production", "cloud-week", "kit", "door"))
import departures  # noqa: E402

LAP = 20.4
VIS = {"T": (772.0, 1927.6), "F": (797.2, 1960.6)}
ALLOWED_LICENCES = {"CC BY-SA 2.0", "CC BY-SA 4.0", "CC BY 4.0", "CC0", "CC BY 2.0"}


class Rows:
    def __init__(self):
        self.rows = []

    def add(self, group, name, ok, detail=""):
        self.rows.append({"group": group, "name": name, "ok": bool(ok), "detail": str(detail)[:240]})

    @property
    def fails(self):
        return [r for r in self.rows if not r["ok"]]


def close(a, b, tol):
    return abs(float(a) - float(b)) <= tol + 1e-9


# ------------------------------------------------------------------------------------------------ 1. 3.1 as built
def check_31(T, R):
    A, _ = departures.apply(load_json(DOOR31))
    F = A["variants"]["flat_door_over_shop"]["parts"]
    for k, P in (("T1", A), ("F1", F)):
        lf = T["kinds"][k]["leaf"]
        R.add("31", "%s leaf size is 3.1's" % k, lf["w"] == P["leaf"]["width_mm"] and lf["h"] == P["leaf"]["height_mm"], "%s x %s" % (lf["w"], lf["h"]))
        want = P["panels"]["openings_leaf_uv_mm"]
        got = {o["id"]: o for o in lf["openings"]}
        ok = all(k2 in got and all(close(got[k2][a], want[k2][a], 0.05) for a in ("u0", "u1", "v0", "v1")) for k2 in want)
        R.add("31", "%s four panel openings are 3.1's" % k, ok, "")
        bol = P["mouldings"]["outside_bolection"]["width_on_face_mm"]
        R.add("31", "%s bolection width is the 3.1 build's (departures: 46 and 43)" % k, T["kinds"][k]["mouldings"]["outside"]["width_on_face"] == bol, "%s" % bol)
    lp = A["ironmongery"]["letter_plate"]
    LP1 = T["furniture"]["letter_plate"]["LP1"]
    R.add("31", "LP1 = 3.1 brass plate 76 x 242, aperture 48 x 190, centre 1617", LP1["outer"] == [lp["outer_w_mm"], lp["outer_h_mm"]] and LP1["aperture"] == [lp["aperture_w_mm"], lp["aperture_h_mm"]]
          and LP1["place"]["T1"]["v"] == lp["centre_above_leaf_bottom_mm"], "")
    cl = A["ironmongery"]["cylinder_lock"]
    R.add("31", "LK1 = 3.1 T1 latch (collar 43.5, plug 28, 5.0 proud)", T["furniture"]["latch"]["LK1"]["collar"] == cl["outer_diameter_mm"] and T["furniture"]["latch"]["LK1"]["plug"] == cl["plug_diameter_mm"]
          and T["furniture"]["latch"]["LK1"]["collar_proud"] == cl["collar_proud_mm"], "")
    fcl = F["ironmongery"]["cylinder_lock"]
    R.add("31", "LK2 = 3.1 F1 latch (collar 37, plug 18, 8 scallops)", T["furniture"]["latch"]["LK2"]["collar"] == fcl["outer_diameter_mm"] and T["furniture"]["latch"]["LK2"]["plug"] == fcl["plug_diameter_mm"], "")
    kp = A["ironmongery"]["keep"]
    BL = T["furniture"]["bell"]["BL1"]
    R.add("31", "BL1 oblong = 3.1's push back 22 x 72.6, 3 proud, at x 859.4, z 1120.3 to 1192.9", BL["size"] == [kp["w_mm"], kp["h_mm"]] and BL["proud"] == kp["proud_mm"] and BL["place"]["T1"]["x"] == kp["centre_x_mm"]
          and BL["place"]["T1"]["z_range"] == kp["z_range_mm"], "")
    for fk, P in (("T", A), ("F", F)):
        fs = T["frame_sets"][fk]
        R.add("31", "frame set %s equals 3.1's frame" % fk, fs["jamb_x"] == P["frame"]["jamb_x_mm"] and fs["transom_z"] == [P["frame"]["transom"]["z_stop_underside"], P["frame"]["transom"]["z_top"]]
              and fs["glass_opening_z"] == P["frame"]["glazing"]["opening_z_mm"] and fs["leaf_x0"] == P["leaf"]["x0_mm"], "")
    removed = [p for p in T["kinds"]["T1"]["parts_vs_3_1"] if p[1] == "removed" and "iron_bellpush_bezel" in p[0] and "iron_bellpush_button" in p[0]]
    R.add("31", "the handover's fix is written: bezel and button removed from T1", len(removed) == 1, "")
    R.add("31", "every kind lists part by part what is kept, changed, removed or added", all(len(v["parts_vs_3_1"]) >= 2 for v in T["kinds"].values()), "")
    used = {st for v in T["kinds"].values() for _, st, _ in v["parts_vs_3_1"]}
    R.add("31", "the part lists use the words kept, changed, removed, added", {"kept", "changed", "removed", "added"} <= {u.split(" / ")[0] for u in used}, ",".join(sorted(used)))
    bp = [p for p in T["kinds"]["T1"]["parts_vs_3_1"] if p[0] == "iron_bellpush"]
    R.add("31", "T1's parts table says the bell push is rebuilt square-cornered (changed, r 1, groove), not kept (3.1 built r 6 and no groove)", len(bp) == 1 and bp[0][1] == "changed" and "r 1" in bp[0][2] and "groove" in bp[0][2], "")
    R.add("31", "the builder's list item 1 names the corners r 1 (3.1 built r 6) and the groove", "r 1" in T["for_builder"][0] and "r 6" in T["for_builder"][0] and "groove" in T["for_builder"][0], "")


# ------------------------------------------------------------------------------------------------ 2. photographs
def fr(box, ref):
    return ((box[0] - ref[0]) / (ref[2] - ref[0]), (box[2] - ref[0]) / (ref[2] - ref[0]), 1.0 - (box[3] - ref[1]) / (ref[3] - ref[1]), 1.0 - (box[1] - ref[1]) / (ref[3] - ref[1]))


def kind_open(T, k, oid):
    for o in T["kinds"][k]["leaf"]["openings"]:
        if o["id"] == oid:
            return o
    raise KeyError(oid)


def check_photo_numbers(T, R):
    """Every photograph feature, from the table of td_kinds.photo_table: the kind's drawn fractions of its visible face against the fractions measured in the recorded boxes, each within
    its own tolerance; and the PH record of the checks list holds the same measured fractions and tolerances (a record with nothing to compare cannot pass)."""
    M = T["sources"]["measurements"]
    tab = TK.photo_table(T)
    recs = {c["id"]: c for c in T["checks"] if c["group"] == "PH"}
    R.add("photo", "the six photograph records exist, one for each of the six (kind, photograph) pairs", sorted(recs) == sorted("PH-%s-%s" % kp for kp in tab) and len(tab) == 6, ",".join(sorted(recs)))
    for (k, ph), feats in tab.items():
        rec = recs.get("PH-%s-%s" % (k, ph))
        R.add("photo", "PH-%s-%s holds expected fractions and a tolerance for every feature (%d features)" % (k, ph, len(feats)),
              rec is not None and isinstance(rec["expect"], dict) and isinstance(rec["tol"], dict) and sorted(rec["expect"]) == sorted(feats) and sorted(rec["tol"]) == sorted(feats), "")
        for name, f in feats.items():
            diffs, ok = [], True
            for a_ in ("u", "v"):
                if f["meas"][a_] is not None:
                    d = max(abs(m - dd) for m, dd in zip(f["meas"][a_], f["drawn"][a_]))
                    diffs.append("%s %.4f of %.4f" % (a_, d, f["tol"][a_]))
                    ok = ok and d <= f["tol"][a_] + 1e-9
            R.add("photo", "%s %s against %s: drawn within the tolerance of the measured fractions" % (k, name, ph), ok, "; ".join(diffs))
            same = (rec is not None and isinstance(rec["expect"], dict) and isinstance(rec["tol"], dict) and rec["expect"].get(name) == {"u": f["meas"]["u"], "v": f["meas"]["v"]} and rec["tol"].get(name) == f["tol"])
            R.add("photo", "PH-%s-%s's record of %s equals the fractions measured in the boxes, with their tolerance" % (k, ph, name), same, "")
    # T2's bars and rails in mm: the self-check recomputes the facts the review corrected
    lf = T["kinds"]["T2"]["leaf"]
    R.add("photo", "T2's structural stiles are 94.0 (lock side, left) and 69.0 (hinge side, right): the white 84 and 59 less the 10 mm bead, plus the 20.4 behind the stops", close(lf["stile_left"], 94.0, 0.05) and close(lf["stile_right"], 69.0, 0.05), "%s %s" % (lf["stile_left"], lf["stile_right"]))
    R.add("photo", "T2's four lights share one width, u0 94.0 to u1 743.8", all(close(o["u0"], 94.0, 0.05) and close(o["u1"], 743.8, 0.05) for o in lf["openings"]), "")
    # T3: the lower panel is as wide as the upper, the inner outline sits inside the outer with the photograph's margin, the arch is the inner outline's
    up, lo, sl = kind_open(T, "T3", "upper_panel"), kind_open(T, "T3", "lower_panel"), kind_open(T, "T3", "small_light")
    R.add("photo", "T3: the lower panel is as wide as the upper (u %.1f to %.1f against %.1f to %.1f)" % (lo["u0"], lo["u1"], up["u0"], up["u1"]), close(lo["u0"], up["u0"], 1.0) and close(lo["u1"], up["u1"], 1.0), "")
    if up.get("inner") and lo.get("inner"):
        mg = [up["inner"]["u0"] - up["u0"], up["u1"] - up["inner"]["u1"], lo["inner"]["u0"] - lo["u0"], lo["u1"] - lo["inner"]["u1"], lo["inner"]["v0"] - lo["v0"], lo["v1"] - lo["inner"]["v1"]]
        R.add("photo", "T3: every panel has two outlines with a margin of 60 to 90 mm between them at the sides and the lower panel's head and foot (%s)" % ", ".join("%.0f" % x for x in mg), all(60.0 <= x <= 90.0 for x in mg), "")
        R.add("photo", "T3: the upper panel's inner outline has a segmental head (springing 22 below the crown) over the light, the lower one is flat", up["inner"]["head"] == "segmental" and close(up["inner"]["springing_below_crown"], 22.0, 0.01) and lo["inner"]["head"] == "flat", "")
        R.add("photo", "T3: the small light lies inside the upper panel's inner outline, centred on the leaf", up["inner"]["u0"] < sl["u0"] and sl["u1"] < up["inner"]["u1"] and close((sl["u0"] + sl["u1"]) / 2.0, T["kinds"]["T3"]["leaf"]["w"] / 2.0, 1.0)
              and up["inner"]["v0"] < sl["v0"] and sl["v1"] < up["inner"]["v1"] - up["inner"]["springing_below_crown"], "")
    else:
        R.add("photo", "T3: every panel has two outlines (an inner outline is missing)", False, "")
    # D4 low plate and D1 low plate against LP5
    lp = T["furniture"]["letter_plate"]["LP5"]["place"]["T2"]["v"]
    d1 = M["D1_R"]
    t, bt = d1["leaf_rows_px"]
    mid = 1.0 - ((d1["plate_rows_px"][0] + d1["plate_rows_px"][1]) / 2 - t) / (bt - t)
    R.add("photo", "LP5 low plate height against D1 (%.3f of the leaf height, drawn %.3f)" % (mid, lp / 1927.6), close(lp / 1927.6, mid, 0.04), "")
    m4 = M["D4_low_plate"]
    lb = m4["leaf_box"]
    mid4 = 1.0 - ((m4["box"][1] + m4["box"][3]) / 2 - lb[1]) / (lb[3] - lb[1])
    R.add("photo", "LP5 low plate height against D4's dark door (%.3f, drawn %.3f)" % (mid4, lp / 1927.6), close(lp / 1927.6, mid4, 0.04), "")


def check_photo_metadata(T, R):
    P = T["sources"]["photographs"]
    pages = load_json(os.path.join(HERE, "pages_read.json")) if os.path.exists(os.path.join(HERE, "pages_read.json")) else {}
    for pid, ph in P.items():
        has = all(ph.get(k) for k in ("title", "author", "licence", "taken", "period"))
        R.add("meta", "%s has title, author, licence, date and a period note" % pid, has, ph.get("title", ""))
        R.add("meta", "%s licence is free" % pid, ph.get("licence") in ALLOWED_LICENCES, ph.get("licence"))
        year = int(str(ph["taken"])[:4])
        if re.match(r"D([1-9])$", pid):
            R.add("meta", "%s taken 1975 to 1995 (%d)" % (pid, year), 1975 <= year <= 1995, ph["taken"])
        else:
            R.add("meta", "%s is later (%d) and says why" % (pid, year), year > 1995 and len(ph["period"]) > 20, ph["period"][:60])
        if ph.get("gid") and pid in pages:
            pg = pages[pid]
            ok = pg.get("title_on_page", "").split("&")[0].strip()[:20].lower() in ph["title"].lower() or ph["title"].lower()[:20] in pg.get("title_on_page", "").lower()
            R.add("meta", "%s page title as recorded (%s)" % (pid, pg.get("title_on_page")), ok, "")
            R.add("meta", "%s page author as recorded" % pid, (pg.get("author_on_page") or "").lower() == ph["author"].lower(), pg.get("author_on_page"))
            iso = pg.get("taken_iso")
            R.add("meta", "%s page date as recorded (%s)" % (pid, iso), (iso or "").startswith(str(ph["taken"])[:4]) if iso else True, ph["taken"])
            R.add("meta", "%s page licence by-sa/2.0" % pid, "by-sa/2.0" in (pg.get("licence_on_page") or []) or pg.get("licence_on_page") == "by-sa/2.0", pg.get("licence_on_page"))
        if ph.get("size_px"):
            pass
    d5, d9 = P["D5"], P["D9"]
    R.add("meta", "D5 is recorded as an indoor landing door, used for the fittings' places only and not for the frame", "indoor" in (d5["period"] + d5["shows"]).lower() and "not for the frame" in d5["used_for"].lower()
          and "frame" in d5["used_for"].lower(), d5["used_for"][:80])
    R.add("meta", "D9 is recorded as half-glazed (a best reading, the door 6 px wide), used for the lower panel's hue only", "half-glazed" in d9["shows"] and "best reading" in d9["shows"] and "6 px" in d9["shows"] and "hue" in d9["used_for"], "")
    R.add("meta", "the photographs' source rows no longer call D9's door flush or D5's a council house leaf", "flush door" not in d9["shows"].replace("not evidence of a flush door", "") and "council flat" not in d5["period"], "")
    M = T["sources"]["measurements"]
    for key, m in M.items():
        ph = P[m["photo"]]
        sz = ph["size_px"]
        boxes = [m[k] for k in ("box", "leaf_box") if k in m]
        ok = all(0 <= bb[0] < bb[2] <= sz[0] and 0 <= bb[1] < bb[3] <= sz[1] for bb in boxes)
        R.add("meta", "measurement %s boxes lie inside %s's image (%dx%d)" % (key, m["photo"], sz[0], sz[1]), ok, "")
        R.add("meta", "measurement %s has a stated error" % key, "error_px" in m, "")
    for key, cb in T["sources"]["colour_boxes"].items():
        sz = P[cb["photo"]]["size_px"]
        b = cb["box"]
        R.add("meta", "colour box %s lies inside its image" % key, 0 <= b[0] < b[2] <= sz[0] and 0 <= b[1] < b[3] <= sz[1], "")


# ------------------------------------------------------------------------------------------------ 2b. live: the pixels
def load_img(path):
    from PIL import Image
    return Image.open(path).convert("RGB")


def lum(a):
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def run_edges(img, axis, fixed, rng, mode, thresh_rel=0.5):
    """Scan along a column (axis 'rows') or a row (axis 'cols'): the mean luminance over the band `fixed` = (c0, c1), over the span rng = (s0, s1); returns (first, last)
    of the span where the signal is on the dark (mode 'dark') or bright (mode 'light') side of the midpoint between its 10th and 90th percentile."""
    a = np.asarray(img).astype(float)
    if axis == "rows":
        band = lum(a[rng[0]:rng[1], fixed[0]:fixed[1], :]).mean(axis=1)
    else:
        band = lum(a[fixed[0]:fixed[1], rng[0]:rng[1], :]).mean(axis=0)
    lo, hi = np.percentile(band, 10), np.percentile(band, 90)
    mid = lo + (hi - lo) * thresh_rel
    idx = np.where(band < mid)[0] if mode == "dark" else np.where(band > mid)[0]
    if len(idx) == 0:
        return None
    # the longest run
    runs, start = [], idx[0]
    for p, q in zip(idx, idx[1:]):
        if q != p + 1:
            runs.append((start, p))
            start = q
    runs.append((start, idx[-1]))
    s, e = max(runs, key=lambda t: t[1] - t[0])
    return rng[0] + s, rng[0] + e + 1


def check_live_photos(T, R, photo_dir):
    import td_photos as TP
    PHOTOS = T["sources"]["photographs"]
    try:
        paths = TP.fetch_all(photo_dir)
    except Exception as e:
        R.add("live", "photographs fetched", False, str(e)[:120])
        return
    R.add("live", "photographs fetched (%d files)" % len(paths), True, photo_dir)
    pages = {}
    for pid, ph in PHOTOS.items():
        if not ph.get("gid"):
            continue
        facts = TP.page_facts(photo_dir, ph["gid"])
        R.add("live", "%s page: title, author, date, licence as recorded" % pid,
              ph["title"].lower()[:16] in facts["title_on_page"].lower() and (facts["author_on_page"] or "").lower() == ph["author"].lower() and (facts["taken_iso"] or "").startswith(ph["taken"][:4])
              and facts["licence_on_page"] == "by-sa/2.0", json.dumps(facts)[:160])
    imgs = {pid: load_img(p) for pid, p in paths.items()}
    for pid, im in imgs.items():
        R.add("live", "%s size is as recorded" % pid, list(im.size) == list(T["sources"]["photographs"][pid]["size_px"]), "%s" % (im.size,))
    # colour boxes
    for key, cb in T["sources"]["colour_boxes"].items():
        a = np.asarray(imgs[cb["photo"]].crop(tuple(cb["box"]))).reshape(-1, 3)
        med = np.median(a, axis=0)
        R.add("live", "colour box %s median %s (recorded %s)" % (key, med.astype(int).tolist(), cb["median_rgb"]), all(abs(med[i] - cb["median_rgb"][i]) <= 4 for i in range(3)), "")
    M = T["sources"]["measurements"]
    # edges
    def edge_row(name, ok, detail=""):
        R.add("live", name, ok, detail)
    # D4 right door: the small flat-topped light is dark on a white door
    b = M["D4_T3_light"]["box"]
    e = run_edges(imgs["D4"], "rows", (int(b[0]) + 1, int(b[2]) - 1), (int(b[1]) - 8, int(b[3]) + 8), "dark")
    edge_row("D4 small light: dark run rows %s against box %.1f to %.1f" % (e, b[1], b[3]), e is not None and close(e[0], b[1], 2.5) and close(e[1], b[3], 2.5), "")
    # D2 middle door: the slit is dark on khaki, the plate under it light
    b = M["D2_F5_slit"]["box"]
    e = run_edges(imgs["D2"], "rows", (int(b[0]) + 2, int(b[2]) - 2), (int(b[1]) - 8, int(b[3]) + 5), "dark")
    edge_row("D2 slit: dark run rows %s against box %.1f to %.1f" % (e, b[1], b[3]), e is not None and close(e[0], b[1], 2.5) and close(e[1], b[3], 2.5), "")
    e = run_edges(imgs["D2"], "cols", (int(b[1]) + 5, int(b[3]) - 5), (int(b[0]) - 8, int(b[2]) + 8), "dark")
    edge_row("D2 slit: dark run columns %s against box %.1f to %.1f" % (e, b[0], b[2]), e is not None and close(e[0], b[0], 2.5) and close(e[1], b[2], 2.5), "")
    # D5: the oblong plate is lighter than the olive leaf; the handle is darker
    b = M["D5_plate"]["box"]
    e = run_edges(imgs["D5"], "cols", (int(b[1]) + 8, int(b[3]) - 8), (int(b[0]) - 40, int(b[2]) + 40), "light", 0.45)
    edge_row("D5 plate: light run columns %s against box %.0f to %.0f (the plate's darker rim is inside the box, so 14 px)" % (e, b[0], b[2]), e is not None and close(e[0], b[0], 14) and close(e[1], b[2], 14), "")
    e = run_edges(imgs["D5"], "rows", (int(b[0]) + 20, int(b[2]) - 20), (int(b[1]) - 30, int(b[3]) + 30), "light", 0.45)
    edge_row("D5 plate: light run rows %s against box %.0f to %.0f" % (e, b[1], b[3]), e is not None and close(e[0], b[1], 8) and close(e[1], b[3], 8), "")
    # D5 leaf edges against the white frame: the leaf is darker than the frame at rows 400 to 700
    lb = M["D5_leaf"]["box"]
    e = run_edges(imgs["D5"], "cols", (400, 700), (int(lb[0]) - 60, int(lb[2]) + 60), "dark", 0.5)
    edge_row("D5 leaf: dark run columns %s against box %.0f to %.0f" % (e, lb[0], lb[2]), e is not None and close(e[0], lb[0], 12) and close(e[1], lb[2], 18), "")
    # D3: the white leaf against the dark gap, measured ROW BY ROW (the edges lean about 1 px every 40 rows): each recorded row's left and right edge to 1.5 px, then the top and the foot
    lb = M["D3_leaf"]["box"]
    a3 = np.asarray(imgs["D3"]).astype(float)
    l3 = lum(a3)

    def row_edges(r):
        seg = l3[r - 2:r + 3, :].mean(axis=0)
        Lx = Rx = None
        for x in range(40, 60):
            if seg[x] < 130 <= seg[x + 1]:
                Lx = x + (130 - seg[x]) / (seg[x + 1] - seg[x]) + 0.5
                break
        for x in range(112, 128):
            if seg[x] >= 130 > seg[x + 1]:
                Rx = x + (seg[x] - 130) / (seg[x] - seg[x + 1]) + 0.5
                break
        return Lx, Rx

    for rr, (el, er) in M["D3_leaf"]["edges_by_row_px"].items():
        Lx, Rx = row_edges(int(rr))
        edge_row("D3 leaf row %s: left edge %s, right edge %s against the recorded %.1f and %.1f (1.5 px: the leaf's own edges, not the dark gap or the brick)" % (rr, None if Lx is None else round(Lx, 1), None if Rx is None else round(Rx, 1), el, er),
                 Lx is not None and Rx is not None and close(Lx, el, 1.5) and close(Rx, er, 1.5), "")
    Lx, Rx = row_edges(M["D3_leaf"]["at_row"])
    edge_row("D3 leaf: the box [%.1f, %.1f] at row %d is on the leaf's own edges (left %s, right %s; 1.5 px)" % (lb[0], lb[2], M["D3_leaf"]["at_row"], None if Lx is None else round(Lx, 1), None if Rx is None else round(Rx, 1)),
             Lx is not None and Rx is not None and close(Lx, lb[0], 1.5) and close(Rx, lb[2], 1.5), "")
    col = l3[:, 80:90].mean(axis=1)
    ti = next(r_ for r_ in range(430, 460) if col[r_] < 130 <= col[r_ + 1])
    top = ti + (130 - col[ti]) / (col[ti + 1] - col[ti]) + 0.5
    edge_row("D3 leaf: the top of the top rail at row %.1f against the recorded %.1f (1.5 px)" % (top, lb[1]), close(top, lb[1], 1.5), "")
    foot = next((r_ for r_ in range(620, 645) if col[r_] >= 130 > col[r_ + 1]), None)
    edge_row("D3 leaf: the foot of the bottom rail at row %s against the recorded %.1f (1.5 px)" % (foot, lb[3]), foot is not None and close(foot + 0.6, lb[3], 1.5), "")
    st = M["D3_stiles"]
    seg = l3[st["at_row"] - 2:st["at_row"] + 3, :].mean(axis=0)
    edge_row("D3 stiles: the white beside the glass at row %d is bright (>= 225) over columns %.0f to %.0f and %.0f to %.0f" % (st["at_row"], st["left_px"][0] + 1, st["left_px"][1] - 1, st["right_px"][0] + 1, st["right_px"][1] - 1),
             seg[int(st["left_px"][0]) + 2:int(st["left_px"][1]) - 1].mean() >= 225 and seg[int(st["right_px"][0]) + 1:int(st["right_px"][1]) - 1].mean() >= 225, "")
    # D3: the fanlight's upper pane is plain (little structure) and the lozenge band below it has the structure
    fr_ = M["D3_fanlight"]["rows_px"]
    box = M["D3_fanlight"]["box"]
    sd = lambda r0, r1: float(l3[int(r0) + 1:int(r1) - 1, int(box[0]) + 6:int(box[2]) - 6].std())
    edge_row("D3 fanlight: the plain upper pane (rows %.0f to %.0f) has less structure than the lozenge band (rows %.0f to %.0f): std %.1f against %.1f" % (fr_["plain_pane"][0], fr_["plain_pane"][1], fr_["diagonal_band"][0], fr_["diagonal_band"][1], sd(*fr_["plain_pane"]), sd(*fr_["diagonal_band"])),
             sd(*fr_["plain_pane"]) < 0.7 * sd(*fr_["diagonal_band"]), "")
    # D4: the small light's head is flat: at row 363 (the first dark row) at least 8 of its 9.5 px are dark, and rows 361 and 362 over the same columns are bright
    g4 = np.asarray(imgs["D4"].convert("L")).astype(float)
    lb4 = M["D4_T3_light"]["box"]
    c0, c1 = int(lb4[0]) + 1, int(lb4[2])
    t4 = int(np.ceil(lb4[1]))
    r363 = (g4[t4, c0:c1] < 100).sum()
    r362 = (g4[t4 - 1, c0:c1] < 100).sum()
    edge_row("D4 small light: its first row %d is dark over %d of %d px and the row above over %d (a flat head; a semicircular head would be dark over about 4 px at its first row)" % (t4, r363, c1 - c0, r362), r363 >= 8 and r362 <= 1, "")
    # D4: the outlines dip on the centre column (the recorded rows of the two outlines of each panel)
    prof = g4[:, 561:566].mean(axis=1)

    def dip(r):
        r0 = int(round(r))
        return float(np.mean([prof[r0 - 4], prof[r0 - 3], prof[r0 + 3], prof[r0 + 4]]) - prof[r0 - 1:r0 + 2].min())

    rows4 = [M["D4_T3_upper"]["box"][1], M["D4_T3_upper_inner"]["box"][1], M["D4_T3_upper_inner"]["box"][3], M["D4_T3_lower"]["box"][1], M["D4_T3_lower_inner"]["box"][1], M["D4_T3_lower_inner"]["box"][3], M["D4_T3_lower"]["box"][3]]
    ds = [dip(r_) for r_ in rows4]
    edge_row("D4 outlines: each of the seven recorded outline rows %s dips on the centre column (depths %s, at least 8)" % (rows4, [round(d_) for d_ in ds]), all(d_ >= 8.0 for d_ in ds), "")
    # D4: the lever's box is on the door (dark mark, columns 577 to 578.5) and the leaf is bright just left of it; the old box on the reveal read 35 to 60 everywhere
    hb = M["D4_T3_handle"]["box"]
    mark = g4[int(hb[1]):int(hb[3]) + 1, 578].mean()
    left = g4[int(hb[1]):int(hb[3]) + 1, 574].mean()
    edge_row("D4 lever: the dark mark at column 578 (mean %.0f) with the bright leaf at column 574 (mean %.0f): the box lies on the door" % (mark, left), mark < 100 and left > 150 and hb[2] <= 579.5, "")
    # D4: the right edge of the leaf at rows 375 and 410 (578.5 to 579.5): the first dark column of the reveal
    for rr in (375, 410):
        seg4 = g4[rr - 1:rr + 2, :].mean(axis=0)
        xr = next(x for x in range(574, 586) if seg4[x] >= 100 > seg4[x + 1]) + 0.5
        edge_row("D4 leaf right edge at row %d is %.1f (recorded right edge %.1f, 1 px)" % (rr, xr, M["D4_T3_leaf"]["box"][2]), close(xr, M["D4_T3_leaf"]["box"][2], 1.0), "")
    # D2: the khaki leaf ends at row 360 (the pale sill lines are rows 361 to 362 and 365 to 366)
    a2 = np.asarray(imgs["D2"]).astype(float)
    colr = a2[:, 566:572, :].mean(axis=1)
    sill = next(r_ for r_ in range(340, 375) if colr[r_].mean() > 150)
    fb = M["D2_F5_leaf"]["box"]
    edge_row("D2 middle door: the first pale sill row is %d, so the khaki leaf ends at row %d (recorded foot %.1f, 1.5 px)" % (sill, sill - 1, fb[3]), close(sill - 0.5, fb[3], 1.5), "")
    # D5: the small dark lock under the lever
    g5 = lum(np.asarray(imgs["D5"]).astype(float))
    lk = M["D5_lock"]["box"]
    inner = g5[int(lk[1]):int(lk[3]), int(lk[0]):int(lk[2])].mean()
    ring = np.mean([g5[int(lk[1]) - 12:int(lk[1]) - 4, int(lk[0]):int(lk[2])].mean(), g5[int(lk[3]) + 4:int(lk[3]) + 12, int(lk[0]):int(lk[2])].mean()])
    edge_row("D5 lock: the box [766, 617, 771, 626] is dark (mean %.0f) against the face above and below it (mean %.0f): the small dark lock" % (inner, ring), inner < ring - 8.0, "")


# ------------------------------------------------------------------------------------------------ 3. the street
def allowed_kinds(house):
    return {"west_south": {"T1", "T2", "T3"}}.get(house.rsplit("_bay", 1)[0], {"F1", "F2", "F3", "F4", "F5", "F6", "F7"})


def check_street(T, R, live):
    S = T["street"]
    hs = S["houses"]
    ids = [h["house"] for h in hs]
    R.add("street", "12 household doors, each once", len(ids) == 12 and len(set(ids)) == 12, str(len(ids)))
    R.add("street", "east_parade_bay5 has no side door", "east_parade_bay5" not in ids, "")
    for h in hs:
        R.add("street", "%s: kind %s fits its frame set" % (h["house"], h["kind"]), h["kind"] in allowed_kinds(h["house"]), "")
        R.add("street", "%s: paint %s is in the palette, frame colour is white-family" % (h["house"], h["paint"]),
              h["paint"] in {p["id"] for p in T["paints"]} and h["frame_colour"] in {p["id"] for p in T["frame_colours"]}, "")
    R.add("street", "every kind is used at least once", set(T["kinds"]) == {h["kind"] for h in hs}, "")
    pal = {p["id"]: p for p in T["paints"]}
    byid = {h["house"]: h for h in hs}
    for a, b in S["adjacent_pairs"]:
        ha, hb = byid[a], byid[b]
        slots = [s for s in ("letter_plate", "handle", "latch", "number") if ha["furniture"][s]["variant"] != hb["furniture"][s]["variant"]]
        pale = pal[ha["paint"]]["class"] in ("light", "bright") and pal[hb["paint"]]["class"] in ("light", "bright")
        R.add("street", "neighbours %s and %s differ in kind, paint and 2 furniture slots, and are not both light or bright (paint class)" % (a, b), ha["kind"] != hb["kind"] and ha["paint"] != hb["paint"] and len(slots) >= 2 and not pale,
              "%s %s %s %s" % (ha["kind"], hb["kind"], pal[ha["paint"]]["class"], pal[hb["paint"]]["class"]))
    for a, b, dx in S["opposite_pairs_within_4_6_m"]:
        R.add("street", "facing doors %s and %s (%.2f m) differ in paint class" % (a, b, dx), pal[byid[a]["paint"]]["class"] != pal[byid[b]["paint"]]["class"], "")
    bd = S["backdrop"]["doors"]
    rows = {"e": [d for d in bd if d["id"].split("_")[-1][0] == "e"], "w": [d for d in bd if d["id"].split("_")[-1][0] == "w"], "x": [d for d in bd if d["id"].split("_")[-1][0] == "x"]}
    ok = all(a["kind"] != b["kind"] and a["paint"] != b["paint"] for r_ in rows.values() for a, b in zip(r_, r_[1:]))
    R.add("street", "the hill's 12 doors: no neighbours alike in kind or paint", ok and len(bd) == 12, "")
    light = [h for h in hs if pal[h["paint"]]["class"] in ("light", "bright")]
    R.add("street", "at most 3 of the 12 doors are light or bright (%d)" % len(light), len(light) <= 3, ",".join(h["house"] for h in light))
    R.add("street", "the street has all three conditions", {h["condition"] for h in hs} == {"kept", "tired", "neglected"}, "")
    # fittings that the photographs put on particular kinds
    f6 = [h for h in hs if h["kind"] == "F6"]
    ok = len(f6) == 1
    if ok:
        lk, hd = f6[0]["furniture"]["latch"], f6[0]["furniture"]["handle"]
        ok = lk["variant"] == "LK3" and lk["place"] and hd["place"] and lk["place"]["v"] < hd["place"]["v"] and abs(lk["place"]["u"] - hd["place"]["u"]) < 120.0
    R.add("street", "F6 has the small dark lock under its lever (D5: LK3, lower than the lever HD2a and within 120 mm of it across)", ok, "")
    kh = [h for h in hs if h["kind"] in ("F1", "F2")]
    R.add("street", "every F1 and F2 door keeps 3.1's plugged keyhole with a place, and no other kind has one", all(h["furniture"]["keyhole"]["variant"] == "KH1" and h["furniture"]["keyhole"]["place"] for h in kh)
          and all(h["furniture"]["keyhole"]["variant"] == "KH0" for h in hs if h["kind"] not in ("F1", "F2")), str(len(kh)))
    t2 = [h for h in hs if h["kind"] == "T2"]
    lf = T["kinds"]["T2"]["leaf"]
    nm = t2[0]["furniture"]["number"] if t2 else None
    vis_top = VIS["T"][1]
    R.add("street", "T2's house number is NM6, small dark numerals on the visible top rail (D3), not on the fanlight glass", bool(nm) and nm["variant"] == "NM6" and nm["place"] is not None and isinstance(nm["place"].get("v"), (int, float))
          and lf["h"] - lf["top_rail"] < nm["place"]["v"] - T["furniture"]["number"]["NM6"]["digit"][1] / 2.0 and nm["place"]["v"] + T["furniture"]["number"]["NM6"]["digit"][1] / 2.0 <= vis_top, "")
    R.add("street", "NM4 (a number on the transom glass) is placed on no house", all(h["furniture"]["number"]["variant"] != "NM4" for h in hs) and not T["furniture"]["number"]["NM4"]["place"], "")
    R.add("street", "no knocker, bell pull, black iron plate, frosted or wired glass is placed", all(h["furniture"][s]["variant"] in ("KN0", "BL0", "BL1", "LP0", "LP1", "LP2", "LP4", "LP5", "LP6", "LP7") or s not in ("knocker", "bell", "letter_plate") for h in hs for s in h["furniture"]), "")
    R.add("street", "knockers: every house has none (no photograph shows one)", all(h["furniture"]["knocker"]["variant"] == "KN0" for h in hs), "")
    R.add("street", "the push BL1 is on one house, a T1", [h["house"] for h in hs if h["furniture"]["bell"]["variant"] == "BL1"] == ["west_south_bay2"] and byid["west_south_bay2"]["kind"] == "T1", "")
    R.add("street", "the boot scraper is on one house only", sum(1 for h in hs if h["furniture"]["scraper"]["variant"] == "BS1") == 1, "")
    R.add("street", "no lion's head knocker is offered", T["furniture"]["knocker"]["KN3"].get("offered") is False, "")
    R.add("street", "no council-owned house is claimed", "none" in S["council_owned"].lower()[:10], "")
    if live:
        import td_sites as TS
        hl, _ = TS.derive()
        mod = TS.modernised_houses()
        R.add("live", "the street derives the same 12 houses from terrace-front.py", sorted(h["house"] for h in hl) == sorted(ids), "")
        for h in hl:
            mine = byid.get(h["house"])
            if mine:
                R.add("live", "%s door centre %.3f m as derived" % (h["house"], h["x_centre_m"]), close(mine["x_centre_m"], h["x_centre_m"], 0.002) and mine["side"] == h["side"], "")
                R.add("live", "%s modernised flag as the windows target (%s)" % (h["house"], mod.get(h["house"])), mine["windows_modernised"] == ("white_upvc" in mod.get(h["house"], [])), "")
    # modernised houses
    for h in hs:
        if h["windows_modernised"] and h["house"] != "east_parade_bay2":
            R.add("street", "%s is modernised and takes a modern kind (T3 F5 F6)" % h["house"], h["kind"] in ("T3", "F5", "F6"), h["kind"])


# ------------------------------------------------------------------------------------------------ 4. geometry
_cache = {}


def layers(T, k):
    key = (id(T), k)
    if key not in _cache:
        _cache[key] = TD.draw_kind(T, k)
    return _cache[key]


def count_runs(g, axis, at, lo, hi):
    """How many separate pieces of geometry g a thin line crosses: the line at fixed z (axis 'x') across x in [lo, hi], or at fixed x (axis 'z'). Returns the list of (start, end)."""
    line = sbox(lo, at - 0.05, hi, at + 0.05) if axis == "x" else sbox(at - 0.05, lo, at + 0.05, hi)
    inter = g.intersection(line)
    parts = list(inter.geoms) if hasattr(inter, "geoms") else ([inter] if not inter.is_empty else [])
    out = []
    for p in parts:
        bx = p.bounds
        out.append((bx[0], bx[2]) if axis == "x" else (bx[1], bx[3]))
    return sorted(out)


def check_geometry(T, R):
    for k, spec in T["kinds"].items():
        L = TD.draw_kind(T, k)
        fs = T["frame_sets"][spec["frame_set"][0]]
        lf = spec["leaf"]
        leaf = L["leaf"]
        vis = L["visible"]
        ops = L["openings"]
        R.add("geom", "%s: no frame_change and no frame set of its own: every kind stands in frame set T or F" % k, "frame_change" not in spec and spec["frame_set"] in ("T", "F"), spec["frame_set"])
        # openings inside the leaf with at least 20 mm framing, disjoint
        ok = True
        detail = ""
        items = list(ops.items())
        for i, g in items:
            inner = leaf.buffer(-20.0, join_style=2)
            if not inner.contains(g.buffer(-0.01)):
                ok, detail = False, "opening %s not 20 mm inside the leaf" % i
        for (i, g), (j, h) in [(items[a], items[b]) for a in range(len(items)) for b in range(a + 1, len(items))]:
            if g.intersection(h).area > 1e-6 and not (g.contains(h) or h.contains(g)):
                ok, detail = False, "%s overlaps %s" % (i, j)
        R.add("geom", "%s: openings inside the leaf, none overlapping" % k, ok, detail)
        # the inner outlines lie inside their panels
        for oid, ig in L["inner_outlines"].items():
            R.add("geom", "%s: the inner outline of %s lies inside the panel's outer outline" % (k, oid), ops[oid].buffer(0.01).contains(ig), "")
        # leaf sits behind the stops: the visible face is inside the leaf by the lap, on every kind
        R.add("geom", "%s: the visible face is the leaf less its lap behind the stops and the transom" % k,
              abs(vis.bounds[0] - (leaf.bounds[0] + LAP)) < 0.6 and abs(vis.bounds[2] - (leaf.bounds[2] - LAP)) < 0.6 and abs(vis.bounds[3] - (leaf.bounds[3] - LAP)) < 1.5, "%s vs leaf %s" % (vis.bounds, leaf.bounds))
        # furniture inside the leaf (the latch collar and the bell push are on the stop, inside the frame; the bare cylinder LK3 is on the leaf)
        for name, g in L["furniture"].items():
            slot = name.split(":")[0]
            on_stop = slot in ("bell",) or (slot == "latch" and name != "latch:LK3")
            region = leaf if not on_stop else unary_union([L["frame"], leaf])
            R.add("geom", "%s: %s lies on the %s" % (k, name, "leaf or stop" if on_stop else "leaf"), region.buffer(0.5).contains(g), "")
        # nothing shows through: the clear opening covered by frame, leaf, glass, transom except the foot gap and the 1.6 mm margins
        clear = sbox(fs["stop_edges_x"][0], 0.0, fs["stop_edges_x"][1], fs["glass_opening_z"][1])
        cover = unary_union([L["frame"], leaf, L["transom_glass"]])
        hole = clear.difference(cover)
        allowed = unary_union([sbox(clear.bounds[0], 0.0, clear.bounds[2], fs["leaf_z0"]), sbox(clear.bounds[0], 0.0, clear.bounds[0] + 1.7, clear.bounds[3]), sbox(clear.bounds[2] - 1.7, 0.0, clear.bounds[2], clear.bounds[3])])
        extra = hole.difference(allowed.buffer(0.01))
        R.add("geom", "%s: nothing shows through the clear opening (foot gap 10, margins 1.6)" % k, extra.area < 1e-6, "extra %.3f mm2" % extra.area)
        # from an angle: the lap of each stop over the leaf's edge, computed from the frame set and this leaf (the 60 degree ray in plan)
        pl = TC.plan_laps(T, k)
        R.add("geom", "%s: from 60 degrees the stops and the transom lap the leaf by at least %.1f (left %.1f, right %.1f, head %.1f; setback %.1f, reach %.1f)" % (k, pl["min_lap_mm"], pl["lap_left_mm"], pl["lap_right_mm"], pl["lap_head_mm"], pl["setback_mm"], pl["sideways_reach_mm"]),
              min(pl["lap_left_mm"], pl["lap_right_mm"], pl["lap_head_mm"]) >= pl["min_lap_mm"], "")
        R.add("geom", "%s: the leaf lies behind its stops (front face at or behind the stops' rear face) and the transom: it opens inward" % k,
              fs["leaf_front_y"] >= fs["frame_front_y"] + fs["stop_depth"] - 1e-6 and pl["lap_head_mm"] > 0.0, "setback %.1f" % pl["setback_mm"])
        # the leaf's side margins in its frame: the left margin is the frame's 1.6, the right one is 1.6 plus whatever this kind's leaf lacks against the frame's leaf
        ml = fs["leaf_edge_clearance"]
        mr = fs["leaf_edge_clearance"] + (fs["leaf_w"] - lf["w"])
        R.add("geom", "%s: the leaf's side margins in its frame are 1.6 each (left %.1f, right %.1f)" % (k, ml, mr), close(ml, 1.6, 0.05) and close(mr, 1.6, 0.2), "")
        # leaf wholly inside the frame
        R.add("geom", "%s: the leaf lies inside the frame's outer width" % k, leaf.bounds[0] >= fs["jamb_x"]["left"][0] and leaf.bounds[2] <= fs["jamb_x"]["right"][1], "")
        # nothing floats: every opening is bounded by the leaf (above) and the leaf is covered by the frame's rebate region at its edges
        R.add("geom", "%s: leaf height reaches the transom's rebate (10 + height >= stop underside + 20)" % k, fs["leaf_z0"] + lf["h"] >= fs["transom_z"][0] + 19.9 and fs["leaf_z0"] + lf["h"] <= fs["transom_z"][0] + 60, "")
        # a house number lies on the visible top rail, in front of the transom (below the visible top) and above the rail's foot
        for name in L["furniture"]:
            if name.startswith("number:"):
                var = name.split(":")[1]
                cat = T["furniture"]["number"][var]
                h0 = [h for h in T["street"]["houses"] if h["kind"] == k][0]
                p = h0["furniture"]["number"]["place"]
                if p and isinstance(p.get("v"), (int, float)) and k != "T1":
                    dh = cat["digit"][1] if "digit" in cat else cat["digit_h"]
                    top_rail_foot = lf["h"] - lf.get("top_rail", 0.0)
                    vis_top = fs["visible_leaf_z"][1] - fs["leaf_z0"]
                    R.add("geom", "%s: the numerals %s (v %.1f, %.0f high) lie on the visible top rail, under the visible top %.1f and in front of the transom" % (k, var, p["v"], dh, vis_top),
                          p["v"] + dh / 2.0 <= vis_top + 1e-6 and p["v"] - dh / 2.0 >= top_rail_foot - 1e-6, "rail foot %.1f" % top_rail_foot)
    # lead came inside the transom glass, came share of the glass; the pattern counted on the drawing
    L = TD.draw_kind(T, "T2")
    came, glass = L["lead_came"], L["transom_glass"]
    g = T["glass"]["leaded_diamond"]
    gx0, gx1 = T["frame_sets"]["T"]["glass_opening_x"]
    gz0, gz1 = T["frame_sets"]["T"]["glass_opening_z"]
    R.add("geom", "T2: the lead came lies inside the fanlight's glass opening", glass.buffer(0.01).contains(came), "")
    R.add("geom", "T2: the came covers 8 to 30 per cent of the fanlight", 0.08 <= came.area / glass.area <= 0.30, "%.3f" % (came.area / glass.area))
    zt, zb = gz1 - g["plain_pane_h"], gz0 + g["foot_came_above_foot"]
    R.add("geom", "T2: the fanlight's upper %.0f of %.0f is one plain pane (no came above the band's top came)" % (g["plain_pane_h"], gz1 - gz0), came.intersection(sbox(gx0, zt + g["came_w"] / 2.0 + 0.01, gx1, gz1)).area < 1e-6, "")
    ups = count_runs(came, "x", gz0 + g["foot_came_above_foot"] / 2.0, gx0, gx1)
    cx = (gx0 + gx1) / 2.0
    R.add("geom", "T2: one upright under each of the 5 lozenge points, 145 apart (found %d at %s)" % (len(ups), ", ".join("%.0f" % ((a + b) / 2.0 - cx) for a, b in ups)),
          len(ups) == g["whole_lozenges"] and all(close(((ups[i + 1][0] + ups[i + 1][1]) - (ups[i][0] + ups[i][1])) / 2.0, g["lozenge"][0], 1.0) for i in range(len(ups) - 1)), "")
    cr = count_runs(came, "x", (zb + zt) / 2.0, gx0, gx1)
    R.add("geom", "T2: the diagonals cross 6 times at the band's mid height (5 lozenges, a tip at each end), %.0f apart (found %d)" % (g["lozenge"][0], len(cr)),
          len(cr) == g["whole_lozenges"] + 1 and all(close(((cr[i + 1][0] + cr[i + 1][1]) - (cr[i][0] + cr[i][1])) / 2.0, g["lozenge"][0], 1.0) for i in range(len(cr) - 1)), "")
    R.add("geom", "T2: the band is %.0f high and its foot came stands %.0f above the glass foot" % (g["band_h"], g["foot_came_above_foot"]), close(zt - zb, g["band_h"], 0.5) and close(zb - gz0, g["foot_came_above_foot"], 0.5), "")
    # T2: the small fitting on the hinge stile lies on the visible hinge stile, not in a light
    fx = T["kinds"]["T2"].get("small_fixings", [])
    lf2 = T["kinds"]["T2"]["leaf"]
    if len(fx) == 1:
        R.add("geom", "T2: the small dark fitting on the hinge stile lies on the white of the visible hinge stile, glass edge to visible edge (u %.1f to %.1f of %.1f to %.1f)" % (fx[0]["u"] - fx[0]["size_mm"][0] / 2.0, fx[0]["u"] + fx[0]["size_mm"][0] / 2.0, lf2["w"] - lf2["stile_right"] - 10.0, lf2["w"] - LAP),
              lf2["w"] - lf2["stile_right"] - 10.0 <= fx[0]["u"] - fx[0]["size_mm"][0] / 2.0 and fx[0]["u"] + fx[0]["size_mm"][0] / 2.0 <= lf2["w"] - LAP and 0 < fx[0]["v"] < lf2["h"], "")
    else:
        R.add("geom", "T2: the small dark fitting on the hinge stile is recorded (D3 shows one)", False, "%d recorded" % len(fx))
    # T3: the small light's head is flat (a semicircular head would fill 0.95 of its box, a flat one with r 20 corners 0.998)
    L3 = TD.draw_kind(T, "T3")
    sl = L3["openings"]["small_light"]
    bx = sl.bounds
    frac = sl.area / ((bx[2] - bx[0]) * (bx[3] - bx[1]))
    R.add("geom", "T3: the small light has a flat head with rounded top corners (%.4f of its box; a semicircular head would be 0.95)" % frac, frac > 0.99 and kind_open(T, "T3", "small_light")["head"] == "flat", "")
    R.add("geom", "T3: each moulded panel has two outlines (an outer and an inner one)", all(kind_open(T, "T3", i).get("inner") for i in ("upper_panel", "lower_panel")) and set(L3["inner_outlines"]) == {"upper_panel", "lower_panel"}, "")
    # F3: raked heads, lower at the outer corner by 50, the high end at the muntin
    L = TD.draw_kind(T, "F3")
    heads = []
    for o in T["kinds"]["F3"]["leaf"]["openings"]:
        gg = L["openings"][o["id"]]
        zs = sorted(p[1] for p in gg.exterior.coords)
        left_z = max(p[1] for p in gg.exterior.coords if abs(p[0] - gg.bounds[0]) < 0.01)
        right_z = max(p[1] for p in gg.exterior.coords if abs(p[0] - gg.bounds[2]) < 0.01)
        heads.append((o["id"], round(right_z - left_z, 1)))
    R.add("geom", "F3: each panel's head is raked 50 mm, high at the muntin (long_l rises to the right, long_r to the left: %s)" % heads, heads[0][1] == 50.0 and heads[1][1] == -50.0, "")
    # F7: board joints and nails inside the leaf, tongue
    L = TD.draw_kind(T, "F7")
    f7 = T["kinds"]["F7"]["leaf"]
    R.add("geom", "F7: six boards across the leaf, 5 joints", len(f7["board_edges_u"]) == 7 and abs(f7["board_edges_u"][-1] - f7["w"]) < 0.2, "")
    R.add("geom", "F7: 18 nail heads inside the leaf", len(f7["nail_heads"]["at"]) == 18 and L["leaf"].buffer(0.01).contains(L["nail_heads"]), "")
    # T2 bars: the framing between lights is the stated bar width
    ops = T["kinds"]["T2"]["leaf"]["openings"]
    gaps = [round(ops[i + 1]["v0"] - ops[i]["v1"], 1) for i in range(3)]
    R.add("geom", "T2: the three bars are 30 mm", all(abs(g_ - 30.0) < 0.3 for g_ in gaps), str(gaps))
    ops = T["kinds"]["F4"]["leaf"]["openings"]
    gaps = [round(ops[i + 1]["u0"] - ops[i]["u1"], 1) for i in range(2)]
    R.add("geom", "F4: the two bars are the stated width", all(abs(g_ - T["kinds"]["F4"]["leaf"]["bar"]) < 0.3 for g_ in gaps) and abs(T["kinds"]["F4"]["leaf"]["bar"] - 36.0) < 0.01, str(gaps))
    # the boot scraper's profile: a closed outline 25 wide at the foot, 200 high with a scroll of radius 35, and the blade's notch
    bs = T["furniture"]["scraper"]["BS1"]
    pts = bs["standard_profile_xz"]
    zmax = max(p[1] for p in pts)
    R.add("geom", "BS1: the standard's profile is a point list (%d points) of a bar 25 wide with a scroll of radius 35 reaching %.0f high; the blade has an underside notch" % (len(pts), zmax),
          len(pts) >= 12 and close(pts[1][0] - pts[0][0], 25.0, 0.1) and close(zmax, bs["size"][2], 1.5) and close(max(p[0] for p in pts) - min(p[0] for p in pts), 62.0, 3.0) and bs["blade_underside_notch"]["depth"] < bs["blade"][1], "")
    # sections
    S = TD.sections(T)
    ep = T["kinds"]["T3"]["mouldings"]["outside"]["profile_dh"]
    h_at = lambda d: min(h for dd, h in ep if abs(dd - d) < 1e-6)
    R.add("geom", "sections: the stuck ovolo is 20 wide and 6.5 proud", close(S["stuck_ovolo_F3"].bounds[2], 20.0, 0.05) and close(S["stuck_ovolo_F3"].bounds[3], 6.5, 0.05), "")
    R.add("geom", "sections: the reeded glass flutes are 6 mm apart and 1.2 deep", close(T["glass"]["reeded_4mm"]["flute_pitch"], 6.0, 0.01) and close(T["glass"]["reeded_4mm"]["flute_depth"], 1.2, 0.01), "")
    R.add("geom", "sections: the moulded panel's edge is two coves 14 wide and 3 deep each (the field 6 below the border face) round a flat raised margin of 62", close(max(h for _, h in ep), 6.0, 0.01)
          and close(h_at(14.0), 3.0, 0.01) and close(h_at(76.0), 3.0, 0.01) and close(h_at(90.0), 6.0, 0.01) and close(S["embossed_step_T3"].bounds[1], -8.0, 0.01), "")


# ------------------------------------------------------------------------------------------------ 5. the checks list, evaluated
def evaluate(T, c, R):
    typ, k = c["type"], c.get("kind")
    ok, detail = True, ""
    if typ == "count":
        n = len(T["kinds"][k]["leaf"]["openings"])
        ok, detail = n == c["expect"], "%d" % n
    elif typ == "opening_bounds":
        L = TD.draw_kind(T, k)
        g = L["openings"].get(c["opening"])
        spec = T["kinds"][k]
        fs = T["frame_sets"][spec["frame_set"][0]]
        if g is None:
            ok, detail = False, "no drawn opening"
        else:
            b = g.bounds
            got = [b[0] - fs["leaf_x0"], b[2] - fs["leaf_x0"], b[1] - fs["leaf_z0"], b[3] - fs["leaf_z0"]]
            ok = all(close(got[i], c["expect"][i], c["tol"]) for i in range(4))
            detail = str([round(x, 1) for x in got])
    elif typ == "inner_bounds":
        L = TD.draw_kind(T, k)
        g = L["inner_outlines"].get(c["opening"])
        fs = T["frame_sets"][T["kinds"][k]["frame_set"][0]]
        if g is None:
            ok, detail = False, "no inner outline"
        else:
            b = g.bounds
            got = [b[0] - fs["leaf_x0"], b[2] - fs["leaf_x0"], b[1] - fs["leaf_z0"], b[3] - fs["leaf_z0"]]
            ok = all(close(got[i], c["expect"][i], c["tol"]) for i in range(4))
            detail = str([round(x, 1) for x in got])
    elif typ == "raked_head":
        L = TD.draw_kind(T, k)
        gg = L["openings"][c["opening"]]
        left_z = max(p[1] for p in gg.exterior.coords if abs(p[0] - gg.bounds[0]) < 0.01)
        right_z = max(p[1] for p in gg.exterior.coords if abs(p[0] - gg.bounds[2]) < 0.01)
        rise = (right_z - left_z) if c["expect"]["rise_toward"] == "right" else (left_z - right_z)
        ok = close(rise, c["expect"]["head_rise"], c["tol"])
        detail = "rise %.1f" % rise
    elif typ == "inward":
        fs = T["frame_sets"][T["kinds"][k]["frame_set"][0]]
        e = c["expect"]
        ok = (fs["frame_front_y"] == e["frame_front_y"] and fs["stop_depth"] == e["stop_depth"] and fs["leaf_front_y"] == e["leaf_front_y"]
              and fs["leaf_front_y"] >= fs["frame_front_y"] + fs["stop_depth"] - 1e-6)
        detail = "leaf front %.1f, stops' rear %.1f" % (fs["leaf_front_y"], fs["frame_front_y"] + fs["stop_depth"])
    elif typ == "members":
        lf = T["kinds"][k]["leaf"]
        ok = all(close(lf.get(m), v, c["tol"]) for m, v in c["expect"].items())
        detail = str({m: lf.get(m) for m in c["expect"]})
    elif typ == "framing":
        L = TD.draw_kind(T, k)
        leaf = L["leaf"]
        ok = all(leaf.buffer(-20.0, join_style=2).contains(g.buffer(-0.01)) for g in L["openings"].values())
    elif typ in ("coverage_elevation", "coverage_angle", "joints"):
        ok = True   # evaluated in check_geometry for every kind; here the record's own numbers must equal the 3.1 frame's
        if typ == "coverage_elevation":
            ok = c["expect"]["foot_gap_mm"] == 10.0 and c["expect"]["margin_mm"] == 1.6
        if typ == "coverage_angle":
            # the record's laps are recomputed from the frame set and this kind's own leaf, and every lap must reach the minimum
            pl = TC.plan_laps(T, k)
            ok = c["expect"]["margin_mm"] == 1.6 and c["expect"]["angle_deg"] == 60.0 and all(close(pl[a], c["expect"][a], c["tol"]) for a in pl) and min(pl["lap_left_mm"], pl["lap_right_mm"], pl["lap_head_mm"]) >= pl["min_lap_mm"]
            detail = str(pl)
        if typ == "joints":
            ok = T["kinds"]["F7"]["leaf"]["joint"].startswith("tongued and grooved") and c["expect"]["tongue_mm"] >= 6.0
    elif typ == "furniture":
        spec = T["kinds"][k]
        cat = T["furniture"][c["slot"]][c["variant"]]
        pl = cat["place"][k]
        ok = pl == c["expect"]["place"]
        for a in ("u", "v"):
            if isinstance(pl.get(a), (int, float)) and isinstance(c["expect"].get(a), (int, float)):
                ok = ok and close(pl[a], c["expect"][a], c["tol"])
        lf = spec["leaf"]
        if isinstance(pl.get("v"), (int, float)):
            ok = ok and 0 < pl["v"] < lf["h"]
        if isinstance(pl.get("u"), (int, float)):
            ok = ok and 0 < pl["u"] < lf["w"]
        detail = str(pl)[:100]
    elif typ == "bell_form":
        bl = T["furniture"]["bell"]["BL1"]
        txt = json.dumps(bl).lower()
        ok = (bl["parts"] == 1 and close(bl["size"][0], 22.0, 0.5) and close(bl["size"][1], 72.6, 0.5) and close(bl["proud"], 3.0, 0.5) and bl["corner_r"] <= 1.0
              and [bl["groove"]["w"], bl["groove"]["h"], bl["groove"]["depth"]] == [14.0, 2.0, 1.0]
              and all(w in bl["forbidden"] for w in ("bezel", "button", "ring", "lens", "led", "camera", "speaker")) and "brass" not in bl["material"])
        # no part of the T1 spec names a bezel or a button
        t1 = json.dumps(T["kinds"]["T1"]["leaf"]).lower()
        ok = ok and "bezel" not in t1 and "button" not in t1
        ok = ok and c["expect"]["corner_r_max"] <= 1.0 and c["expect"]["groove"] == [14.0, 2.0, 1.0]
        detail = "parts %s corner %s" % (bl["parts"], bl["corner_r"])
    elif typ == "bell_kinds":
        users = {h["kind"] for h in T["street"]["houses"] if h["furniture"]["bell"]["variant"] != "BL0"}
        ok = users == set(c["expect"]["kinds_with_bell"])
        for kk, spec in T["kinds"].items():
            if kk != "T1" and "bellpush" in json.dumps(spec).lower().replace("iron_bellpush", "") + "":
                ok = False
        detail = str(users)
    elif typ == "bell_modern":
        bad = [v for v in T["furniture"]["bell"].values() if v.get("parts", 1) > c["expect"]["max_parts_per_bell"] or v.get("name", "").find("video") >= 0 or v.get("name", "").find("two-part") >= 0]
        ok = not bad
    elif typ == "bell_houses":
        ok = c["expect"]["houses"] == [h["house"] for h in T["street"]["houses"] if h["furniture"]["bell"]["variant"] == "BL1"]
    elif typ in ("adjacent", "opposite", "houses", "frame_set", "kinds_used", "backdrop"):
        ok = True   # evaluated in check_street over the same data; here the record must still describe the street
        if typ == "adjacent":
            ok = c["expect"] == T["street"]["order"][c["side"]]
        if typ == "houses":
            ok = c["expect"] == [h["house"] for h in T["street"]["houses"]]
        if typ == "kinds_used":
            ok = c["expect"] == sorted({h["kind"] for h in T["street"]["houses"]})
        if typ == "opposite":
            ok = c["expect"] == T["street"]["opposite_pairs_within_4_6_m"]
        if typ == "backdrop":
            ok = c["expect"] == T["street"]["backdrop"]["doors"]
    elif typ == "palette":
        ok = set(c["expect"]) == {p["id"] for p in T["paints"]} and all(h["paint"] in c["expect"] for h in T["street"]["houses"])
    elif typ == "frames":
        ok = set(c["expect"]) == {p["id"] for p in T["frame_colours"]} and set(c["expect"]) <= {"white", "white_grimy"} and all(h["frame_colour"] in c["expect"] for h in T["street"]["houses"])
    elif typ == "light_count":
        pal = {p["id"]: p for p in T["paints"]}
        ok = sum(1 for h in T["street"]["houses"] if pal[h["paint"]]["class"] in ("light", "bright")) <= c["expect"]
    elif typ == "srgb":
        pal = {p["id"]: p["srgb"] for p in T["paints"]}
        ok = all(pal[n] == v for n, v in c["expect"].items()) and all(len(v) == 3 and all(0 <= x <= 255 for x in v) for v in pal.values())
    elif typ == "glass_keys":
        used = {v["glass"]["transom"] for v in T["kinds"].values()} | {v["glass"]["leaf"] for v in T["kinds"].values() if v["glass"]["leaf"]}
        ok = used <= set(T["glass"].keys())
    elif typ == "glass_values":
        g = T["glass"][c["glass"]]
        ok = all((g.get(a) == v) for a, v in c["expect"].items() if a != "pitch" and a != "depth") and (c["glass"] != "reeded_4mm" or (g["flute_pitch"] == c["expect"]["pitch"] and g["flute_depth"] == c["expect"]["depth"]))
        ok = ok and T["kinds"][k]["glass"]["transom"] == c["glass"]
    elif typ == "wear_order":
        cn = T["conditions"]
        ok = [cn["kept"]["paint_flake_share"], cn["tired"]["paint_flake_share"], cn["neglected"]["paint_flake_share"]] == c["expect"]
    elif typ == "wear_numbers":
        ok = T["conditions"]["kept"]["paint_flake_share"] == c["expect"]["flake_low"] and T["conditions"]["tired"]["paint_flake_share"] == c["expect"]["typical"] and T["conditions"]["neglected"]["paint_flake_share"] == c["expect"]["neglected"]
    elif typ == "wear_houses":
        cnt = {kk: sum(1 for h in T["street"]["houses"] if h["condition"] == kk) for kk in ("kept", "tired", "neglected")}
        ok = cnt == c["expect"] and all(v > 0 for v in cnt.values())
    elif typ == "photo":
        # the record must name a measured photograph and hold, for every feature of the table, the measured fractions and a tolerance; the drawn side is compared in check_photo_numbers
        feats = TK.photo_table(T).get((k, c["photo"]), {})
        ok = (c["photo"] in T["sources"]["photographs"] and any(m["photo"] == c["photo"] for m in T["sources"]["measurements"].values()) and isinstance(c["expect"], dict) and isinstance(c["tol"], dict)
              and sorted(c["expect"]) == sorted(feats) and all(c["expect"][n] == {"u": f["meas"]["u"], "v": f["meas"]["v"]} and c["tol"][n] == f["tol"]
                                                                  and all(max(abs(m - d) for m, d in zip(f["meas"][a], f["drawn"][a])) <= f["tol"][a] + 1e-9 for a in ("u", "v") if f["meas"][a] is not None) for n, f in feats.items()))
        detail = "%d features" % len(feats)
    elif typ == "blocklist":
        ok = not blocklist_hits(T["sources"], ()) and not blocklist_hits({k2: v for k2, v in T.items() if k2 not in ("self_check", "checks", "_prose")}) and not prose_hits(T)
        detail = str(prose_hits(T)[:2])
    elif typ == "night":
        s = json.dumps(T["gate"])
        ok = "[1.0, 0.25, 0.0]" in s and STALE_NIGHT.replace(" ", "") not in json.dumps({k2: v for k2, v in T.items() if k2 not in ("self_check", "checks")}).replace(" ", "")
    elif typ == "owed_text":
        ok = all("\u2014" not in s and "\u2013" not in s and "*" not in s for s in T["owed_for_jafar"]) and 0 < len(T["owed_for_jafar"]) <= 5 and all("recommended" in s for s in T["owed_for_jafar"])
    elif typ == "views":
        ok = len(T["gate"]["views"][k]) == c["expect"]
    R.add("checks", "%s %s" % (c["id"], c["name"]), ok, detail)


def check_checks(T, R):
    ids = [c["id"] for c in T["checks"]]
    R.add("checks", "check ids are unique (%d records)" % len(ids), len(ids) == len(set(ids)), "")
    R.add("checks", "every record has a name, what, expect, tolerance and source", all(all(k in c for k in ("name", "what", "expect", "tol", "src", "type")) for c in T["checks"]), "")
    # every opening of every kind has an opening check; every placed furniture variant of a kind has one
    have = {c["id"] for c in T["checks"]}
    miss = [o["id"] for k, s in T["kinds"].items() for o in s["leaf"]["openings"] if "PL-%s-%s" % (k, o["id"]) not in have]
    R.add("checks", "every opening of every kind has a check", not miss, str(miss))
    miss = []
    for h in T["street"]["houses"]:
        for slot, d in h["furniture"].items():
            if d["place"] and "FU-%s-%s-%s" % (h["kind"], slot, d["variant"]) not in have:
                miss.append((h["kind"], slot, d["variant"]))
    R.add("checks", "every placed fitting of every kind has a check", not miss, str(miss))
    groups = {c["group"] for c in T["checks"]}
    R.add("checks", "the groups PL CV FU BP AD PN GL WR PH NM GA are all present", {"PL", "CV", "FU", "BP", "AD", "PN", "GL", "WR", "PH", "NM", "GA"} <= groups, ",".join(sorted(groups)))
    for c in T["checks"]:
        evaluate(T, c, R)


# ------------------------------------------------------------------------------------------------ 6. wear, text, gate
def check_wear(T, R, live):
    cn = T["conditions"]
    R.add("wear", "paint_flake shares kept < tired < neglected", cn["kept"]["paint_flake_share"] < cn["tired"]["paint_flake_share"] < cn["neglected"]["paint_flake_share"], "")
    R.add("wear", "roughness kept 0.35, tired 0.55, neglected 0.65 as 3.1", [cn["kept"]["roughness"], cn["tired"]["roughness"], cn["neglected"]["roughness"]] == [0.35, 0.55, 0.65], "")
    R.add("wear", "each condition names crazing, chips, bottom rail, kick marks, polish and frame", all(all(k in v for k in ("crazing", "chips", "bottom_rail", "kick_marks", "polish", "frame")) for v in cn.values()), "")
    R.add("wear", "the layer's kinds are named and what it cannot do is listed", len(T["wear_kinds_used"]) == 5 and len(T["wear_not_covered"]) == 4, "")
    if live:
        W = load_json(WEAR_T)
        pf = W["kinds"]["paint_flake"]["where"]["density"]
        R.add("live", "wear target: paint_flake range %s typical %s" % (pf["range"], pf["typical"]), pf["range"][0] == cn["kept"]["paint_flake_share"] and pf["typical"] == cn["tired"]["paint_flake_share"], "")
        R.add("live", "wear target: neglected up to 0.40 stated", "0.40" in W["kinds"]["paint_flake"]["where"]["rule"] or "40 %" in W["kinds"]["paint_flake"]["where"]["rule"] or "0.40" in str(pf), "")
        hw = W["kinds"]["handle_wear"]["geometry"]["halo_eqd_mm"]
        R.add("live", "wear target: handle_wear halo p50 170 mm", hw["p50"] == 170, "")
        R.add("live", "wear target has every kind this target names", all(k in W["kinds"] for k in T["wear_kinds_used"]), "")


def prose_texts(T):
    """The texts the maker-name scan reads besides target.json: TARGET.md and the prose of the scripts in this folder (the blocklist's own lines in td_common.py excepted)."""
    if "_prose" in T:
        return T["_prose"]
    out = {}
    for fn in sorted(os.listdir(HERE)):
        if fn.endswith(".py") or fn == "TARGET.md":
            txt = open(os.path.join(HERE, fn)).read()
            if fn == "td_common.py":
                txt = re.sub(r"BLOCKLIST = \[.*?\]\n", "", txt, flags=re.S)
            out[fn] = txt
    return out


def prose_hits(T):
    hits = []
    for fn, txt in prose_texts(T).items():
        low = txt.lower()
        for b in BLOCKLIST:
            if re.search(r"(?<![a-z0-9'])" + re.escape(b) + r"(?![a-z0-9'])", low):
                hits.append((fn, b))
    return hits


CYL = "cylinder" + " lock"      # built here so that this file does not contain the phrase it forbids


def cylinder_hits(T):
    body = {k: v for k, v in T.items() if k not in ("self_check", "checks", "_prose")}
    hits = [(p, "target.json") for p, s_ in strings(body) if CYL in s_.lower()]
    hits += [(fn, "prose") for fn, txt in prose_texts(T).items() if CYL in txt.lower()]
    return hits


def check_text(T, R):
    skip = {k for k in ("self_check", "checks")}
    body = {k: v for k, v in T.items() if k not in skip}
    hits = blocklist_hits(body)
    R.add("text", "no real maker's name, whole word, anywhere in target.json", not hits, str(hits[:3]))
    txt = json.dumps(body)
    R.add("text", "no real maker's name, whole word, in TARGET.md or in the prose of this folder's scripts (the blocklist's own lines excepted)", not prose_hits(T), str(prose_hits(T)[:3]))
    R.add("text", "the blocklist's first word does not occur anywhere in target.json", BLOCKLIST[0] not in txt.lower(), "")
    R.add("text", "the lock is a rim night latch: its old name is in no string of target.json, in TARGET.md or in the scripts' prose", not cylinder_hits(T), str(cylinder_hits(T)[:3]))
    R.add("text", "owed line 2 names D2's mustard-painted frames with the Hull streets, and W6 names D2", "Railway Street" in T["owed_for_jafar"][1] and "mustard" in T["owed_for_jafar"][1]
          and any(d["id"] == "W6" and "D2" in d["photograph"] for d in T["disagreements_photographs_win"]), "")
    R.add("text", "the lantern colour (1.0, 0.25, 0.0) is in the gate, the stale colour is not anywhere", "[1.0, 0.25, 0.0]" in json.dumps(T["gate"]) and STALE_NIGHT.replace(" ", "") not in txt.replace(" ", ""), "")
    dash = [p for p, s in strings(body) if "\u2014" in s or "\u2013" in s]
    R.add("text", "no em or en dash in any string", not dash, str(dash[:3]))
    R.add("text", "owed lines: at most 5, each with a recommendation, no dash, no italic marker", len(T["owed_for_jafar"]) <= 5 and all("recommended" in s and "\u2014" not in s and "*" not in s and "_" not in s for s in T["owed_for_jafar"]), "")
    R.add("text", "photographs-win disagreements are written down (>= 8)", len(T["disagreements_photographs_win"]) >= 8, "")
    R.add("text", "could-not-settle is written down", len(T["could_not_settle"]) >= 8, "")
    R.add("text", "rulings checked are listed (6)", len(T["rulings_checked"]) == 6, "")


def check_gate(T, R):
    base = {"T": load_json(os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_T1.json")), "F": load_json(os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_F1.json"))}
    for k, spec in T["kinds"].items():
        fr = spec["frame_set"][0]
        vs = {v["name"]: v for v in T["gate"]["views"][k]}
        want = {v["name"]: v for v in base[fr]}
        ok = set(want) <= set(vs)
        same = all(vs[n]["loc"][:2] == want[n]["loc"][:2] and vs[n]["lens"] == want[n].get("lens", vs[n].get("lens")) for n in want if n in vs and "lens" in want[n])
        R.add("gate", "%s: the 3.1 views are all there, cameras as 3.1's (close heights aside)" % k, ok and same, str(sorted(vs)))
    R.add("gate", "the street views name the hook day, reverse day, night and the two rows", [v["name"] for v in T["gate"]["street_views"]] == ["hook_day", "reverse_day", "street_night", "row_east", "row_west"], "")
    R.add("gate", "every kind has a photograph pair or says it has none", {p["kind"] for p in T["gate"]["photograph_pairs"]} >= {"T2", "T3", "F5", "F6", "F4", "F3", "F7"}, "")


def check_previews(T, R):
    from PIL import Image
    if not os.path.isdir(PREVIEWS):
        R.add("previews", "the preview folder exists", False, PREVIEWS)
        return
    files = [f for f in os.listdir(PREVIEWS) if f.lower().endswith((".jpg", ".png"))]
    R.add("previews", "previews exist (%d)" % len(files), len(files) >= 10, "")
    doc = open(os.path.join(HERE, "TARGET.md")).read() if os.path.exists(os.path.join(HERE, "TARGET.md")) else ""
    for f in sorted(files):
        p = os.path.join(PREVIEWS, f)
        im = Image.open(p)
        kb = os.path.getsize(p) / 1024.0
        R.add("previews", "%s is at most 1200 px and 300 KB (%dx%d, %.0f KB)" % (f, im.size[0], im.size[1], kb), max(im.size) <= 1200 and kb < 300, "")
        R.add("previews", "%s is credited in TARGET.md" % f, f in doc, "")
    mk = json.load(open(os.path.join(HERE, "preview_masks.json"))) if os.path.exists(os.path.join(HERE, "preview_masks.json")) else {}
    for f, ms in mk.items():
        p = os.path.join(PREVIEWS, f)
        if not os.path.exists(p):
            R.add("previews", "%s (masked) exists" % f, False, "")
            continue
        a = np.asarray(Image.open(p).convert("RGB")).astype(int)
        for m in ms:
            x0, y0, x1, y1 = m["box_in_preview"]
            reg = a[y0:y1, x0:x1].reshape(-1, 3)
            R.add("previews", "%s mask '%s' is flat grey" % (f, m["what"]), reg.std(axis=0).max() < 6.0 and abs(reg.mean() - 120) < 8, "")
    R.add("previews", "no preview file is named after a street number, a firm or a plate", not any(re.search(r"\d{2,}-(street|road)|plate|ltd|co\b", f.lower()) for f in files), "")


# ------------------------------------------------------------------------------------------------ 7. negative controls
def run_all(T, photo_dir=None, live=False, previews=False):
    R = Rows()
    check_31(T, R)
    check_photo_metadata(T, R)
    check_photo_numbers(T, R)
    check_street(T, R, live)
    check_geometry(T, R)
    check_checks(T, R)
    check_wear(T, R, live)
    check_text(T, R)
    check_gate(T, R)
    if live:
        check_live_photos(T, R, photo_dir)
    if previews:
        check_previews(T, R)
    return R


def controls(T, photo_dir, live, previews):
    out = []

    def mut(name, fn, row=None):
        """A wrong copy of the target; caught when some row fails (and, when `row` is given, when a failing row's name contains it: the control then proves that one row can fail)."""
        X = copy.deepcopy(T)
        fn(X)
        try:
            R = run_all(X, photo_dir, False, False)   # controls run offline: the live rows read the world, not the copy
            fails = [r for r in R.fails if row is None or row in r["name"]]
            caught = len(fails) > 0
            which = fails[0]["name"][:70] if fails else ("no failing row named %r" % row if R.fails else "")
        except Exception as e:                       # a crash is a catch too, with its reason
            caught, which = True, "raised %s" % str(e)[:50]
        out.append({"name": name, "caught": caught, "first_failure": which})

    def lights(x, k, i):
        return x["kinds"][k]["leaf"]["openings"][i]

    mut("T2: a bar moved 20 mm", lambda x: lights(x, "T2", 1).update({"v0": lights(x, "T2", 1)["v0"] + 20, "v1": lights(x, "T2", 1)["v1"] + 20}))
    mut("T2: three lights instead of four", lambda x: x["kinds"]["T2"]["leaf"]["openings"].pop())
    mut("T2: the fanlight glass plain instead of leaded", lambda x: x["kinds"]["T2"]["glass"].update({"transom": "plain_3mm"}))
    mut("T3: the small light 60 mm lower", lambda x: lights(x, "T3", 1).update({"v0": lights(x, "T3", 1)["v0"] - 60, "v1": lights(x, "T3", 1)["v1"] - 60}))
    mut("F5: the slit 50 mm wider on each side", lambda x: lights(x, "F5", 0).update({"u0": lights(x, "F5", 0)["u0"] - 50, "u1": lights(x, "F5", 0)["u1"] + 50}))
    mut("F4: a bar 21 mm instead of 36", lambda x: lights(x, "F4", 1).update({"u0": lights(x, "F4", 1)["u0"] - 15}))
    mut("F6: the letter plate at 1000 instead of 912", lambda x: x["furniture"]["letter_plate"]["LP4"]["place"]["F6"].update({"v": 1000.0}))
    mut("F5: the lever on the right stile (u 700)", lambda x: x["furniture"]["handle"]["HD2b"]["place"]["F5"].update({"u": 700.0}))
    mut("F6: the old 762 leaf in the street frame (a see-through slot beside it)", lambda x: x["kinds"]["F6"]["leaf"].update({"w": 762.0}), row="the leaf's side margins")
    mut("F7: the leaf 700 wide in the F frame (a slot beside it)", lambda x: x["kinds"]["F7"]["leaf"].update({"w": 700.0}))
    mut("the bell push given a bezel part", lambda x: x["furniture"]["bell"]["BL1"].update({"parts": 3, "name": "oblong push with a brass bezel and a button"}))
    mut("a bell push on F1", lambda x: x["street"]["houses"][0]["furniture"]["bell"].update({"variant": "BL1"}))
    mut("the push made brass", lambda x: x["furniture"]["bell"]["BL1"].update({"material": "brass bezel"}))
    mut("two neighbours given one paint", lambda x: x["street"]["houses"][1].update({"paint": x["street"]["houses"][0]["paint"]}))
    mut("two neighbours given one kind", lambda x: x["street"]["houses"][1].update({"kind": x["street"]["houses"][0]["kind"]}))
    mut("two neighbours given the same furniture", lambda x: x["street"]["houses"][1]["furniture"].update({k: dict(v) for k, v in x["street"]["houses"][0]["furniture"].items()}))
    mut("a door facing another in the same paint class", lambda x: [h.update({"paint": "maroon"}) for h in x["street"]["houses"] if h["house"] in ("west_south_bay2",)])
    mut("a cottage given a flat kind", lambda x: [h.update({"kind": "F2"}) for h in x["street"]["houses"] if h["house"] == "west_south_bay0"])
    mut("a house missing from the street", lambda x: x["street"]["houses"].pop())
    mut("east_parade_bay5 given a side door", lambda x: x["street"]["houses"].append(dict(x["street"]["houses"][0], house="east_parade_bay5")))
    mut("a cream frame colour on a house", lambda x: x["street"]["houses"][0].update({"frame_colour": "cream"}))
    mut("a paint outside the palette", lambda x: x["street"]["houses"][2].update({"paint": "hot_pink"}))
    mut("five bright doors", lambda x: [h.update({"paint": "bright_blue"}) for h in x["street"]["houses"][:5]])
    mut("a knocker on a house", lambda x: x["street"]["houses"][0]["furniture"]["knocker"].update({"variant": "KN1"}))
    mut("a lion's head knocker offered", lambda x: x["furniture"]["knocker"]["KN3"].update({"offered": True}))
    mut("a maker's name in a text", lambda x: x["furniture"]["latch"]["LK1"].update({"name": BLOCKLIST[0].capitalize() + "-type rim cylinder"}))
    mut("the stale night colour in the gate", lambda x: x["gate"]["street_views"][2]["light"].update({"lantern_colour_linear": [1, 0.7055, 0]}))
    mut("an em dash in an owed line", lambda x: x["owed_for_jafar"].__setitem__(0, x["owed_for_jafar"][0] + " \u2014 now"))
    mut("an owed line without a recommendation", lambda x: x["owed_for_jafar"].__setitem__(1, "Door surrounds: white or coloured?"))
    mut("a photograph's date after 1995 used as period", lambda x: x["sources"]["photographs"]["D3"].update({"taken": "2012-05-06"}))
    mut("a measurement box outside its image", lambda x: x["sources"]["measurements"]["D4_T3_light"].update({"box": [559.0, 363.0, 700.0, 384.0]}))
    mut("D3's light row moved 12 px", lambda x: x["sources"]["measurements"]["D3_rows"]["rows_px"].update({"light2": [503.0, 543.0]}))
    mut("a check removed from the list", lambda x: x.update({"checks": [c for c in x["checks"] if c["id"] != "PL-T2-light1"]}))
    mut("neglected wear share 0.20 instead of 0.40", lambda x: x["conditions"]["neglected"].update({"paint_flake_share": 0.20}))
    mut("the T1 bolection width 36 instead of 3.1's built 46", lambda x: x["kinds"]["T1"]["mouldings"]["outside"].update({"width_on_face": 36.0}))
    mut("the gate lacks a view", lambda x: x["gate"]["views"]["T2"].pop(0))
    mut("a kind never used", lambda x: [h.update({"kind": "F1"}) for h in x["street"]["houses"] if h["kind"] == "F7"])
    mut("the backdrop's neighbours alike", lambda x: x["street"]["backdrop"]["doors"][1].update(kind=x["street"]["backdrop"]["doors"][0]["kind"], paint=x["street"]["backdrop"]["doors"][0]["paint"]))
    mut("reeded glass pitch changed to 9 mm", lambda x: x["glass"]["reeded_4mm"].update({"flute_pitch": 9.0}))
    mut("the leaded came 10 wide", lambda x: x["glass"]["leaded_diamond"].update({"came_w": 10.0}))
    mut("LK1's collar 40 instead of 3.1's 43.5", lambda x: x["furniture"]["latch"]["LK1"].update({"collar": 40.0}))
    mut("F2 given 8 openings", lambda x: x["kinds"]["F2"]["leaf"]["openings"].append(dict(x["kinds"]["F2"]["leaf"]["openings"][0], id="extra", u0=300.0, u1=340.0)))
    mut("a house given a lion's head knocker and a bell pull together", lambda x: x["street"]["houses"][3]["furniture"].update({"knocker": {"variant": "KN3", "place": None}, "bell": {"variant": "BL2", "place": None}}), row="no knocker, bell pull")
    mut("the wear layer's typical share changed", lambda x: x["conditions"]["tired"].update({"paint_flake_share": 0.08}))
    mut("the hill's list shortened", lambda x: x["street"]["backdrop"]["doors"].pop())
    mut("the three owed lines made six", lambda x: x["owed_for_jafar"].extend(["Door frames: yes (recommended)?"] * 3))
    mut("the T1 letter plate moved 40 mm", lambda x: x["furniture"]["letter_plate"]["LP1"]["place"]["T1"].update({"v": 1657.0}))
    mut("a placed fitting outside its leaf", lambda x: x["furniture"]["letter_plate"]["LP5"]["place"]["T2"].update({"v": 5000.0}))

    # ---- controls added with the fixes of the review (each one names the row that must fail)
    def house(x, hid):
        return [h for h in x["street"]["houses"] if h["house"] == hid][0]

    def narrow_frame(x):
        fs = x["frame_sets"]["F"]
        cx = (fs["stop_edges_x"][0] + fs["stop_edges_x"][1]) / 2.0
        fs["stop_edges_x"] = [cx - 382.6, cx + 382.6]
        fs["jamb_x"] = {"left": [fs["jamb_x"]["left"][0], cx - 382.6], "right": [cx + 382.6, fs["jamb_x"]["right"][1]]}
        fs["visible_leaf_x"] = list(fs["stop_edges_x"])
        fs["glass_opening_x"] = list(fs["stop_edges_x"])

    def alter_record(x, cid, key, val):
        for c in x["checks"]:
            if c["id"] == cid:
                c["expect"][key] = val

    mut("F6: the leaf 838 in the rejected narrow frame (stops moved in to a clear of 765.2, an 838 leaf)", narrow_frame, row="the visible face is the leaf less its lap")
    mut("the flat frame's leaf hung in front of its stops (the rejected planted-stop frame of F6: it would open outward)", lambda x: x["frame_sets"]["F"].update({"leaf_front_y": x["frame_sets"]["F"]["frame_front_y"]}), row="opens inward")
    mut("a leaf shifted 14 mm (the left stop laps it by only 6.4: the 60 degree row)", lambda x: x["frame_sets"]["F"].update({"leaf_x0": x["frame_sets"]["F"]["leaf_x0"] + 14.0}), row="from 60 degrees")
    mut("a leaf set back 12 mm behind the stops (a 60 degree ray reaches 20.8 sideways, past the 20.4 lap)", lambda x: x["frame_sets"]["F"].update({"leaf_front_y": x["frame_sets"]["F"]["leaf_front_y"] + 12.0}), row="from 60 degrees")
    mut("F1's leaf 40 mm shorter (the lap under the transom lost)", lambda x: x["kinds"]["F1"]["leaf"].update({"h": x["kinds"]["F1"]["leaf"]["h"] - 40.0}), row="from 60 degrees")
    mut("the record CV-F1-angle with a right lap of 30 instead of 20.4", lambda x: alter_record(x, "CV-F1-angle", "lap_right_mm", 30.0), row="CV-F1-angle")
    mut("T2: stiles 114.3 on both sides (the first draft's 93.9 visible, 104 of white on each side)", lambda x: [x["kinds"]["T2"]["leaf"].update({"stile_left": 114.3, "stile_right": 114.3})] + [o.update({"u0": 114.3, "u1": 698.5}) for o in x["kinds"]["T2"]["leaf"]["openings"]], row="T2 white_left")
    mut("T2: the fanlight lozenges all over (no plain upper pane)", lambda x: x["glass"]["leaded_diamond"].update({"plain_pane_h": 0.0, "band_h": 227.0}), row="fan_plain_pane")
    mut("T2: the lozenge pitch 95 and 70 high (the first draft)", lambda x: x["glass"]["leaded_diamond"].update({"lozenge": [95.0, 70.0]}), row="fan_lozenge_pitch")
    mut("T2: three lozenge points instead of five", lambda x: x["glass"]["leaded_diamond"].update({"whole_lozenges": 3}), row="GL-leaded")
    mut("T2: the house number back on the fanlight glass (NM4)", lambda x: house(x, "west_south_bay0")["furniture"].update({"number": {"variant": "NM4", "place": None}}), row="T2's house number is NM6")
    mut("T2: the small dark fitting on the hinge stile left out", lambda x: x["kinds"]["T2"].update({"small_fixings": []}), row="hinge stile")
    mut("T3: the small light given a semicircular head (corner radius 109)", lambda x: lights(x, "T3", 1).update({"corner_r": 109.0}), row="the small light has a flat head")
    mut("T3: the lower panel 160 mm narrower than the upper (the first draft's u 234.8 to 642.3)", lambda x: lights(x, "T3", 2).update({"u0": 234.8, "u1": 642.3}), row="the lower panel is as wide as the upper")
    mut("T3: the upper panel with one outline only", lambda x: lights(x, "T3", 0).pop("inner"), row="two outlines")
    mut("T3: the lever on the reveal (v 823 as the first draft)", lambda x: x["furniture"]["handle"]["HD2c"]["place"]["T3"].update({"v": 823.0}), row="T3 lever_v")
    mut("F5: the slit at the first draft's v 914.9 to 1806.1", lambda x: lights(x, "F5", 0).update({"v0": 914.9, "v1": 1806.1}), row="F5 slit against D2")
    mut("F5: D2's leaf box taken down to the sill (foot row 363)", lambda x: x["sources"]["measurements"]["D2_F5_leaf"].update({"box": [561.0, 280.5, 595.5, 363.0]}), row="PH-F5-D2")
    mut("D3's leaf box on the first draft's span (a box that spans the lean)", lambda x: x["sources"]["measurements"]["D3_leaf"].update({"box": [45.75, 443.75, 124.25, 633.75]}), row="PH-T2-D3")
    mut("F3: the panel heads square (the first draft)", lambda x: [o.update({"head": "square"}) for o in x["kinds"]["F3"]["leaf"]["openings"]], row="F3")
    mut("F6: the lock under the lever left out", lambda x: house(x, "east_parade_bay4")["furniture"].update({"latch": {"variant": "LK0", "place": None}}), row="F6 has the small dark lock")
    mut("F1: the plugged keyhole left out", lambda x: house(x, "east_parade_bay0")["furniture"].update({"keyhole": {"variant": "KH0", "place": None}}), row="plugged keyhole")
    mut("F2: the numerals at v 1943, behind the transom (the first draft)", lambda x: house(x, "east_parade_bay1")["furniture"]["number"]["place"].update({"v": 1943.0}), row="the numerals NM1")
    mut("the bell push with r 6 corners (3.1's build)", lambda x: x["furniture"]["bell"]["BL1"].update({"corner_r": 6.0}), row="BP-form")
    mut("T1's parts table says the bell push is kept", lambda x: [p.__setitem__(1, "kept") for p in x["kinds"]["T1"]["parts_vs_3_1"] if p[0] == "iron_bellpush"], row="T1's parts table says the bell push")
    mut("two pale doors side by side (west_south_bay0 back to cream beside white gloss)", lambda x: house(x, "west_south_bay0").update({"paint": "cream"}), row="not both light or bright")
    mut("a maker's name in TARGET.md", lambda x: x.update({"_prose": {"TARGET.md": "the lock is a " + BLOCKLIST[0] + " lock"}}), row="TARGET.md or in the prose")
    mut("the lock's old name in a part table", lambda x: x["kinds"]["T1"]["parts_vs_3_1"][2].__setitem__(2, x["kinds"]["T1"]["parts_vs_3_1"][2][2] + " (" + CYL + ")"), row="its old name")
    mut("the lock's old name in a script's prose", lambda x: x.update({"_prose": {"td_furn.py": "# the " + CYL + " of 3.1"}}), row="its old name")
    mut("D5 named again as the evidence for the frame", lambda x: x["sources"]["photographs"]["D5"].update({"used_for": "F6 council flush door, its frame and its stops, the plate, the lever"}), row="D5 is recorded as an indoor")
    mut("D9 called a flush door again", lambda x: x["sources"]["photographs"]["D9"].update({"shows": "council flush doors under small concrete canopies, one painted turquoise"}), row="D9 is recorded as half-glazed")
    mut("F6 given a frame_change again (the rejected FF6)", lambda x: x["kinds"]["F6"].update({"frame_change": {"clear_between_faces": 765.2}}), row="no frame_change")
    mut("a photograph record with nothing to compare (PH-F6-D5 expect null)", lambda x: [c.update({"expect": None}) for c in x["checks"] if c["id"] == "PH-F6-D5"], row="PH-F6-D5")
    mut("owed line 2 without Railway Street's mustard frames", lambda x: x["owed_for_jafar"].__setitem__(1, "Door surrounds: all white as you ruled for windows on 3 October (recommended), or the painted surrounds the 1980s Hull streets show, as on the windows line?"), row="owed line 2 names")
    mut("the boot scraper's standard without its profile", lambda x: x["furniture"]["scraper"]["BS1"].update({"standard_profile_xz": [[0.0, 0.0], [25.0, 0.0], [25.0, 100.0]]}), row="BS1: the standard's profile")
    return sum(1 for c in out if c["caught"]), out


def live_controls(T, photo_dir):
    """Wrong copies that only the live rows can catch (the street re-derived, the pixels re-measured, the pages and the wear target re-read)."""
    out = []

    def mut(name, fn):
        X = copy.deepcopy(T)
        fn(X)
        try:
            R = Rows()
            check_street(X, R, True)
            check_wear(X, R, True)
            check_live_photos(X, R, photo_dir)
            caught = any((not r["ok"]) and r["group"] == "live" for r in R.rows)
            which = next((r["name"][:70] for r in R.rows if not r["ok"] and r["group"] == "live"), "")
        except Exception as e:
            caught, which = True, "raised %s" % str(e)[:50]
        out.append({"name": name, "caught": caught, "first_failure": which})

    mut("a colour box's recorded median is wrong", lambda x: x["sources"]["colour_boxes"]["D5_olive"].update({"median_rgb": [200, 102, 65]}))
    mut("D2's slit box is 12 px too low", lambda x: x["sources"]["measurements"]["D2_F5_slit"].update({"box": [574.0, 299.0, 582.8, 336.5]}))
    mut("D4's small light box is 12 px too high", lambda x: x["sources"]["measurements"]["D4_T3_light"].update({"box": [559.0, 351.0, 568.0, 372.0]}))
    mut("D3's leaf box is 8 px too far left", lambda x: x["sources"]["measurements"]["D3_leaf"].update({"box": [37.75, 443.75, 116.25, 633.75]}))
    mut("D5's plate box is 40 px too far left", lambda x: x["sources"]["measurements"]["D5_plate"].update({"box": [521.0, 570.0, 628.0, 600.0]}))
    mut("a photograph's recorded size is wrong", lambda x: x["sources"]["photographs"]["D2"].update({"size_px": [800, 600]}))
    mut("a photograph's recorded author is wrong", lambda x: x["sources"]["photographs"]["D3"].update({"author": "Someone Else"}))
    mut("a house's door centre moved 0.5 m", lambda x: x["street"]["houses"][0].update({"x_centre_m": x["street"]["houses"][0]["x_centre_m"] + 0.5}))
    mut("a modernised flag flipped", lambda x: x["street"]["houses"][2].update({"windows_modernised": not x["street"]["houses"][2]["windows_modernised"]}))
    mut("the wear target's typical share not as recorded", lambda x: x["conditions"]["kept"].update({"paint_flake_share": 0.05}))
    mut("D3's leaf box right edge on the dark gap and the brick (124.25)", lambda x: x["sources"]["measurements"]["D3_leaf"].update({"box": [45.4, 442.6, 124.25, 634.1]}))
    mut("D3's recorded edges at row 549 three pixels off", lambda x: x["sources"]["measurements"]["D3_leaf"]["edges_by_row_px"].update({"549": [47.4, 126.0]}))
    mut("D4's lever box back on the dark reveal (columns 581 to 583)", lambda x: x["sources"]["measurements"]["D4_T3_handle"].update({"box": [581.0, 394.0, 583.0, 398.0]}))
    mut("D4's small light box 3 rows higher (its first row bright)", lambda x: x["sources"]["measurements"]["D4_T3_light"].update({"box": [558.5, 359.7, 568.0, 380.3]}))
    mut("D4's lower panel's inner outline moved to a flat row (410)", lambda x: x["sources"]["measurements"]["D4_T3_lower_inner"].update({"box": [553.5, 410.0, 574.0, 416.0]}))
    mut("D2's middle door box taken down to the sill (foot 363)", lambda x: x["sources"]["measurements"]["D2_F5_leaf"].update({"box": [561.0, 280.5, 594.5, 363.0]}))
    mut("D5's lock box 40 px too far left", lambda x: x["sources"]["measurements"]["D5_lock"].update({"box": [726.0, 617.0, 731.0, 626.0]}))
    return sum(1 for c in out if c["caught"]), out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default=os.path.join(os.environ.get("TMPDIR", "/tmp"), "td_photos"))
    ap.add_argument("--live", action="store_true")
    ap.add_argument("--previews", action="store_true")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--no-controls", action="store_true")
    a = ap.parse_args()
    T = load_json(TARGET_JSON)
    R = run_all(T, a.photos, a.live, a.previews)
    n_pass = sum(1 for r in R.rows if r["ok"])
    opts = ("offline" if not a.live else "--live") + (" --previews" if a.previews else "")
    for r in R.fails:
        print("FAIL [%s] %s | %s" % (r["group"], r["name"], r["detail"]))
    line = "%s: %d pass, %d fail" % (opts, n_pass, len(R.fails))
    cc, cl, lcc, lcl = 0, [], 0, []
    if not a.no_controls:
        cc, cl = controls(T, a.photos, a.live, a.previews)
        line += "; negative controls (wrong copies, offline rows) %d of %d caught" % (cc, len(cl))
        for c in cl:
            if not c["caught"]:
                print("UNCAUGHT control:", c["name"])
        if a.live:
            lcc, lcl = live_controls(T, a.photos)
            line += "; live controls (wrong copies, live rows) %d of %d caught" % (lcc, len(lcl))
            for c in lcl:
                if not c["caught"]:
                    print("UNCAUGHT live control:", c["name"])
    print(line)
    if a.write:
        T["self_check"] = {"result": line, "options": opts, "rows": sorted(R.rows, key=lambda r: (r["group"], r["name"])), "controls": cl, "live_controls": lcl, "run": "13 October 2026"}
        with open(TARGET_JSON, "w") as f:
            json.dump(T, f, indent=1)
    sys.exit(1 if R.fails or (not a.no_controls and (cc != len(cl) or lcc != len(lcl))) else 0)


if __name__ == "__main__":
    main()
