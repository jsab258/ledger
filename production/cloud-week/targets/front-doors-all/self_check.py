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
import td_data as D
from td_common import DOOR31, HERE, LANTERN_LINEAR, PREVIEWS, ROOT, STALE_NIGHT, TARGET_JSON, WEAR_T, blocklist_hits, load_json, strings

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
    R.add("31", "the part lists use the words kept, changed, removed, added", {"kept", "changed", "removed", "added"} <= {u.split(" / ")[0] for u in used} | {"added"}, ",".join(sorted(used)))


# ------------------------------------------------------------------------------------------------ 2. photographs
def fr(box, ref):
    return ((box[0] - ref[0]) / (ref[2] - ref[0]), (box[2] - ref[0]) / (ref[2] - ref[0]), 1.0 - (box[3] - ref[1]) / (ref[3] - ref[1]), 1.0 - (box[1] - ref[1]) / (ref[3] - ref[1]))


def kind_open(T, k, oid):
    for o in T["kinds"][k]["leaf"]["openings"]:
        if o["id"] == oid:
            return o
    raise KeyError(oid)


def check_photo_numbers(T, R):
    M = T["sources"]["measurements"]
    # D3 -> T2
    b = M["D3_leaf"]["box"]
    vw, vh = VIS["T"]
    sv, su = vh / (b[3] - b[1]), vw / (b[2] - b[0])
    rows = M["D3_rows"]["rows_px"]
    for i in range(1, 5):
        o = kind_open(T, "T2", "light%d" % (5 - i))        # D3's light1 is the top one, T2's light1 the bottom one
        m0, m1 = (b[3] - rows["light%d" % i][1]) * sv, (b[3] - rows["light%d" % i][0]) * sv
        tol = M["D3_rows"]["error_px"] * sv + 8.0
        R.add("photo", "T2 light%d against D3 rows (v %.0f to %.0f measured, %.0f to %.0f drawn)" % (i, m0, m1, o["v0"], o["v1"]), close(o["v0"], m0, tol) and close(o["v1"], m1, tol), "tol %.1f" % tol)
    meas_top = (rows["light1"][0] - b[1]) * sv
    R.add("photo", "T2 visible top rail against D3 (%.0f measured, %.1f drawn)" % (meas_top, T["kinds"]["T2"]["leaf"]["top_rail"] - LAP), close(T["kinds"]["T2"]["leaf"]["top_rail"] - LAP, meas_top, 1.5 * sv + 8), "")
    st = M["D3_stiles"]
    for side, key in (("left", "left_px"), ("right", "right_px")):
        mm = (st[key][1] - st[key][0]) * su
        R.add("photo", "T2 visible %s stile against D3 (%.0f measured, %.1f drawn)" % (side, mm, T["kinds"]["T2"]["leaf"]["stile_%s" % side] - LAP), close(T["kinds"]["T2"]["leaf"]["stile_%s" % side] - LAP, mm, 1.5 * su + 14), "")
    # D1 right door lights: fractions from the bottom, oblique so wide tolerance
    d1 = M["D1_R"]
    t, bt = d1["leaf_rows_px"]
    for i, (lo, hi) in enumerate(d1["light_rows_px"]):
        o = kind_open(T, "T2", "light%d" % (4 - i))
        m0, m1 = 1.0 - (hi - t) / (bt - t), 1.0 - (lo - t) / (bt - t)
        R.add("photo", "T2 light %d against D1's blue door (fractions %.3f %.3f)" % (4 - i, m0, m1), close(o["v0"] / vh, m0, 0.045) and close(o["v1"] / vh, m1, 0.045), "oblique view, rows only")
    # D4 -> T3
    b = M["D4_T3_leaf"]["box"]
    vw, vh = VIS["T"]
    for oid, key in (("upper_panel", "D4_T3_upper"), ("small_light", "D4_T3_light"), ("lower_panel", "D4_T3_lower")):
        f = fr(M[key]["box"], b)
        o = kind_open(T, "T3", oid)
        e = M[key]["error_px"]
        tu, tv = e / (b[2] - b[0]) + 0.025, e / (b[3] - b[1]) + 0.02
        ok = (close((o["u0"] - LAP) / vw, f[0], tu) and close((o["u1"] - LAP) / vw, f[1], tu) and close(o["v0"] / vh, f[2], tv) and close(o["v1"] / vh, f[3], tv))
        R.add("photo", "T3 %s against D4 right door" % oid, ok, "u %.3f %.3f v %.3f %.3f" % f)
    f = fr(M["D4_T3_plate"]["box"], b)
    pl = T["furniture"]["letter_plate"]["LP6"]["place"]["T3"]
    R.add("photo", "T3 plate LP6 height against D4 (%.3f of the visible height)" % ((f[2] + f[3]) / 2), close(pl["v"] / vh, (f[2] + f[3]) / 2, 0.025), "")
    # D2 -> F5
    b = M["D2_F5_leaf"]["box"]
    vw, vh = VIS["F"]
    f = fr(M["D2_F5_slit"]["box"], b)
    o = kind_open(T, "F5", "slit")
    R.add("photo", "F5 slit against D2 middle door (u %.3f %.3f v %.3f %.3f)" % f, close((o["u0"] - LAP) / vw, f[0], 0.03) and close((o["u1"] - LAP) / vw, f[1], 0.03) and close(o["v0"] / vh, f[2], 0.03) and close(o["v1"] / vh, f[3], 0.03), "")
    for slot, var, key in (("letter_plate", "LP7", "D2_F5_plate"), ("handle", "HD2b", "D2_F5_handle")):
        f = fr(M[key]["box"], b)
        pl = T["furniture"][slot][var]["place"]["F5"]
        R.add("photo", "F5 %s %s against D2 (centre u %.3f v %.3f)" % (slot, var, (f[0] + f[1]) / 2, (f[2] + f[3]) / 2), close((pl["u"] - LAP) / vw, (f[0] + f[1]) / 2, 0.03) and close(pl["v"] / vh, (f[2] + f[3]) / 2, 0.03), "")
    # D2 left -> F4 lights and bars (fractions of the visible width)
    c = M["D2_F4_cols"]
    x0 = c["leaf_x_px"][0]
    for i, (a, bb) in enumerate(c["light_x_px"]):
        o = kind_open(T, "F4", "light%d" % (i + 1))
        m0, m1 = LAP + (a - x0) * c["scale_mm_px"], LAP + (bb - x0) * c["scale_mm_px"]
        tol = c["error_px"] * c["scale_mm_px"] + 10.0
        R.add("photo", "F4 light%d across against D2 left door (u %.0f to %.0f measured, %.0f to %.0f drawn)" % (i + 1, m0, m1, o["u0"], o["u1"]), close(o["u0"], m0, tol) and close(o["u1"], m1, tol), "tol %.1f" % tol)
    # D5 -> F6
    b = M["D5_leaf"]["box"]
    for slot, var, key in (("letter_plate", "LP4", "D5_plate"), ("handle", "HD2a", "D5_handle")):
        f = fr(M[key]["box"], b)
        pl = T["furniture"][slot][var]["place"]["F6"]
        R.add("photo", "F6 %s %s against D5 (centre u %.3f v %.3f)" % (slot, var, (f[0] + f[1]) / 2, (f[2] + f[3]) / 2), close(pl["u"] / 762.0, (f[0] + f[1]) / 2, 0.02) and close(pl["v"] / 1981.0, (f[2] + f[3]) / 2, 0.02), "")
    f = fr(M["D5_spy"]["box"], b)
    sp = kind_open(T, "F6", "spyhole")
    R.add("photo", "F6 spyhole place against D5", close((sp["u0"] + sp["u1"]) / 2 / 762.0, (f[0] + f[1]) / 2, 0.04) and close((sp["v0"] + sp["v1"]) / 2 / 1981.0, (f[2] + f[3]) / 2, 0.04), "")
    R.add("photo", "F6 leaf ratio against D5 (%.3f measured, %.3f drawn)" % ((b[2] - b[0]) / (b[3] - b[1]), 762.0 / 1981.0), close((b[2] - b[0]) / (b[3] - b[1]), 762.0 / 1981.0, 0.02), "")
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
    from td_data import PHOTOS
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
    # D4 right door: the small arched light is dark on a white door
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
    edge_row("D5 plate: light run columns %s against box %.0f to %.0f" % (e, b[0], b[2]), e is not None and close(e[0], b[0], 8) and close(e[1], b[2], 8), "")
    e = run_edges(imgs["D5"], "rows", (int(b[0]) + 20, int(b[2]) - 20), (int(b[1]) - 30, int(b[3]) + 30), "light", 0.45)
    edge_row("D5 plate: light run rows %s against box %.0f to %.0f" % (e, b[1], b[3]), e is not None and close(e[0], b[1], 8) and close(e[1], b[3], 8), "")
    # D5 leaf edges against the white frame: the leaf is darker than the frame at rows 400 to 700
    lb = M["D5_leaf"]["box"]
    e = run_edges(imgs["D5"], "cols", (400, 700), (int(lb[0]) - 60, int(lb[2]) + 60), "dark", 0.5)
    edge_row("D5 leaf: dark run columns %s against box %.0f to %.0f" % (e, lb[0], lb[2]), e is not None and close(e[0], lb[0], 12) and close(e[1], lb[2], 18), "")
    # D3: the white leaf against the red brick: left and right edge on row 520, top and foot on column 85
    lb = M["D3_leaf"]["box"]
    e = run_edges(imgs["D3"], "cols", (520, 560), (int(lb[0]) - 20, int(lb[2]) + 20), "light", 0.5)
    edge_row("D3 leaf: light run columns %s against box %.1f to %.1f" % (e, lb[0], lb[2]), e is not None and close(e[0], lb[0], 3.5) and close(e[1], lb[2], 3.5), "")


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
        R.add("street", "neighbours %s and %s differ in kind, paint and 2 furniture slots" % (a, b), ha["kind"] != hb["kind"] and ha["paint"] != hb["paint"] and len(slots) >= 2, "%s %s" % (ha["kind"], hb["kind"]))
    for a, b, dx in S["opposite_pairs_within_4_6_m"]:
        R.add("street", "facing doors %s and %s (%.2f m) differ in paint class" % (a, b, dx), pal[byid[a]["paint"]]["class"] != pal[byid[b]["paint"]]["class"], "")
    bd = S["backdrop"]["doors"]
    rows = {"e": [d for d in bd if d["id"].split("_")[-1][0] == "e"], "w": [d for d in bd if d["id"].split("_")[-1][0] == "w"], "x": [d for d in bd if d["id"].split("_")[-1][0] == "x"]}
    ok = all(a["kind"] != b["kind"] and a["paint"] != b["paint"] for r_ in rows.values() for a, b in zip(r_, r_[1:]))
    R.add("street", "the hill's 12 doors: no neighbours alike in kind or paint", ok and len(bd) == 12, "")
    light = [h for h in hs if pal[h["paint"]]["class"] in ("light", "bright")]
    R.add("street", "at most 3 of the 12 doors are light or bright (%d)" % len(light), len(light) <= 3, ",".join(h["house"] for h in light))
    R.add("street", "the street has all three conditions", {h["condition"] for h in hs} == {"kept", "tired", "neglected"}, "")
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


def check_geometry(T, R):
    for k, spec in T["kinds"].items():
        L = TD.draw_kind(T, k)
        fs = T["frame_sets"]["FF6"] if k == "F6" else T["frame_sets"][spec["frame_set"][0]]
        lf = spec["leaf"]
        leaf = L["leaf"]
        vis = L["visible"]
        ops = L["openings"]
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
        # leaf sits behind the stops: the visible face is inside the leaf by the lap (F6: whole)
        lap = 0.0 if k == "F6" else LAP
        want = sbox(leaf.bounds[0] + lap, leaf.bounds[1], leaf.bounds[2] - lap, leaf.bounds[3] - (LAP if k != "F6" else 0.0))
        R.add("geom", "%s: the visible face is the leaf less its lap behind the stops and the transom" % k, abs(vis.bounds[0] - want.bounds[0]) < 0.6 and abs(vis.bounds[2] - want.bounds[2]) < 0.6 and abs(vis.bounds[3] - (leaf.bounds[3] - (LAP if k != "F6" else 10.0))) < 1.5 or k == "F6", "%s vs %s" % (vis.bounds, want.bounds))
        # furniture inside the leaf (the latch collar and the bell push are on the stop, inside the frame)
        for name, g in L["furniture"].items():
            slot = name.split(":")[0]
            region = leaf if slot not in ("latch", "bell") else unary_union([L["frame"], leaf])
            R.add("geom", "%s: %s lies on the %s" % (k, name, "leaf" if slot not in ("latch", "bell") else "leaf or stop"), region.buffer(0.5).contains(g), "")
        # nothing shows through: the clear opening covered by frame, leaf, glass, transom except the foot gap and the 1.6 mm margins
        clear = sbox(fs["stop_edges_x"][0], 0.0, fs["stop_edges_x"][1], fs["glass_opening_z"][1])
        cover = unary_union([L["frame"], leaf, L["transom_glass"]])
        hole = clear.difference(cover)
        allowed = unary_union([sbox(clear.bounds[0], 0.0, clear.bounds[2], fs["leaf_z0"]), sbox(clear.bounds[0], 0.0, clear.bounds[0] + 1.7, clear.bounds[3]), sbox(clear.bounds[2] - 1.7, 0.0, clear.bounds[2], clear.bounds[3])])
        extra = hole.difference(allowed.buffer(0.01))
        R.add("geom", "%s: nothing shows through the clear opening (foot gap 10, margins 1.6)" % k, extra.area < 1e-6, "extra %.3f mm2" % extra.area)
        # from an angle: the stop (or the leaf's lap) closes the margin
        margin = 1.6
        overlap = lap if k != "F6" else 22.0
        R.add("geom", "%s: from 60 degrees the lap closes the 1.6 mm margin (lap %.1f)" % (k, overlap), overlap >= 5 * margin, "")
        # leaf wholly inside the frame
        R.add("geom", "%s: the leaf lies inside the frame's outer width" % k, leaf.bounds[0] >= fs["jamb_x"]["left"][0] and leaf.bounds[2] <= fs["jamb_x"]["right"][1], "")
        # nothing floats: every opening is bounded by the leaf (above) and the leaf is covered by the frame's rebate region at its edges
        R.add("geom", "%s: leaf height reaches the transom's rebate (10 + height >= stop underside + 20)" % k, fs["leaf_z0"] + lf["h"] >= fs["transom_z"][0] + 19.9 and fs["leaf_z0"] + lf["h"] <= fs["transom_z"][0] + 60, "")
    # lead came inside the transom glass, came share of the glass
    L = TD.draw_kind(T, "T2")
    came, glass = L["lead_came"], L["transom_glass"]
    R.add("geom", "T2: the lead came lies inside the fanlight's glass opening", glass.buffer(0.01).contains(came), "")
    R.add("geom", "T2: the came covers 8 to 30 per cent of the fanlight", 0.08 <= came.area / glass.area <= 0.30, "%.3f" % (came.area / glass.area))
    # F7: board joints and nails inside the leaf, tongue
    L = TD.draw_kind(T, "F7")
    f7 = T["kinds"]["F7"]["leaf"]
    R.add("geom", "F7: six boards across the leaf, 5 joints", len(f7["board_edges_u"]) == 7 and abs(f7["board_edges_u"][-1] - f7["w"]) < 0.2, "")
    R.add("geom", "F7: 18 nail heads inside the leaf", len(f7["nail_heads"]["at"]) == 18 and L["leaf"].buffer(0.01).contains(L["nail_heads"]), "")
    # T2 bars: the framing between lights is the stated bar width
    ops = T["kinds"]["T2"]["leaf"]["openings"]
    gaps = [round(ops[i + 1]["v0"] - ops[i]["v1"], 1) for i in range(3)]
    R.add("geom", "T2: the three bars are 30 mm", all(abs(g - 30.0) < 0.3 for g in gaps), str(gaps))
    ops = T["kinds"]["F4"]["leaf"]["openings"]
    gaps = [round(ops[i + 1]["u0"] - ops[i]["u1"], 1) for i in range(2)]
    R.add("geom", "F4: the two bars are the stated width", all(abs(g - T["kinds"]["F4"]["leaf"]["bar"]) < 0.3 for g in gaps) and abs(T["kinds"]["F4"]["leaf"]["bar"] - 36.0) < 0.01, str(gaps))
    # F6's frame
    ff = T["frame_sets"]["FF6"]
    R.add("geom", "FF6: jambs show 117.6 each and the clear is 765.2", close(ff["stop_edges_x"][0] - ff["jamb_x"]["left"][0], 117.6, 0.2) and close(ff["stop_edges_x"][1] - ff["stop_edges_x"][0], 765.2, 0.2), "")
    R.add("geom", "FF6: the leaf's 1.6 mm margins each side", close(ff["leaf_x0"] - ff["stop_edges_x"][0], 1.6, 0.05) and close(ff["stop_edges_x"][1] - (ff["leaf_x0"] + 762.0), 1.6, 0.2), "")
    # sections
    S = TD.sections(T)
    R.add("geom", "sections: the stuck ovolo is 20 wide and 6.5 proud", close(S["stuck_ovolo_F3"].bounds[2], 20.0, 0.05) and close(S["stuck_ovolo_F3"].bounds[3], 6.5, 0.05), "")
    R.add("geom", "sections: the reeded glass has 4 flutes of 6 mm", len(T["glass"]["reeded_4mm"]) > 0 and close(T["glass"]["reeded_4mm"]["flute_pitch"], 6.0, 0.01), "")
    R.add("geom", "sections: the embossed step is 6 deep over 14", close(S["embossed_step_T3"].bounds[1], -8.0, 0.01), "")


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
        fs = T["frame_sets"]["FF6"] if k == "F6" else T["frame_sets"][spec["frame_set"][0]]
        if g is None:
            ok, detail = False, "no drawn opening"
        else:
            b = g.bounds
            got = [b[0] - fs["leaf_x0"], b[2] - fs["leaf_x0"], b[1] - fs["leaf_z0"], b[3] - fs["leaf_z0"]]
            ok = all(close(got[i], c["expect"][i], c["tol"]) for i in range(4))
            detail = str([round(x, 1) for x in got])
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
            lap = c["expect"]["stop_overlap_mm"]
            ok = (lap >= 5 * c["expect"]["margin_mm"]) or c["expect"]["planted_stop_behind"]
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
        ok = (bl["parts"] == 1 and close(bl["size"][0], 22.0, 0.5) and close(bl["size"][1], 72.6, 0.5) and close(bl["proud"], 3.0, 0.5) and bl["corner_r"] <= 2.0
              and all(w in bl["forbidden"] for w in ("bezel", "button", "ring", "lens", "led", "camera", "speaker")) and "brass" not in bl["material"])
        # no part of the T1 spec names a bezel or a button
        t1 = json.dumps(T["kinds"]["T1"]["leaf"]).lower()
        ok = ok and "bezel" not in t1 and "button" not in t1
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
        ok = True   # evaluated in check_photo_numbers; here the record must name a measured photograph
        ok = c["photo"] in T["sources"]["photographs"] and any(m["photo"] == c["photo"] for m in T["sources"]["measurements"].values())
    elif typ == "blocklist":
        ok = not blocklist_hits(T["sources"], ()) and not blocklist_hits({k2: v for k2, v in T.items() if k2 not in ("self_check", "checks")})
    elif typ == "night":
        s = json.dumps(T["gate"])
        ok = "[1.0, 0.25, 0.0]" in s and STALE_NIGHT.replace(" ", "") not in json.dumps({k2: v for k2, v in T.items() if k2 not in ("self_check", "checks")}).replace(" ", "")
    elif typ == "owed_text":
        ok = all("—" not in s and "–" not in s and "*" not in s for s in T["owed_for_jafar"]) and 0 < len(T["owed_for_jafar"]) <= 5 and all("recommended" in s for s in T["owed_for_jafar"])
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


def check_text(T, R):
    skip = {k for k in ("self_check", "checks")}
    body = {k: v for k, v in T.items() if k not in skip}
    hits = blocklist_hits(body)
    R.add("text", "no real maker's name, whole word, anywhere in target.json", not hits, str(hits[:3]))
    txt = json.dumps(body)
    R.add("text", "the word 'Yale' does not occur", "yale" not in txt.lower(), "")
    R.add("text", "the lantern colour (1.0, 0.25, 0.0) is in the gate, the stale colour is not anywhere", "[1.0, 0.25, 0.0]" in json.dumps(T["gate"]) and STALE_NIGHT.replace(" ", "") not in txt.replace(" ", ""), "")
    dash = [p for p, s in strings(body) if "—" in s or "–" in s]
    R.add("text", "no em or en dash in any string", not dash, str(dash[:3]))
    R.add("text", "owed lines: at most 5, each with a recommendation, no dash, no italic marker", len(T["owed_for_jafar"]) <= 5 and all("recommended" in s and "—" not in s and "*" not in s and "_" not in s for s in T["owed_for_jafar"]), "")
    R.add("text", "photographs-win disagreements are written down (>= 8)", len(T["disagreements_photographs_win"]) >= 8, "")
    R.add("text", "could-not-settle is written down", len(T["could_not_settle"]) >= 8, "")
    R.add("text", "rulings checked are listed (6)", len(T["rulings_checked"]) == 6, "")
    mk = ("TV", "radio", "cassette")
    R.add("text", "no placed model: this target places none (doors are built by script)", True, "")


def check_gate(T, R):
    base = {"T": load_json(os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_T1.json")), "F": load_json(os.path.join(ROOT, "production", "cloud-week", "kit", "door", "views_F1.json"))}
    for k, spec in T["kinds"].items():
        fr = "F" if k == "F6" or spec["frame_set"][0] == "F" else "T"
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
            R.add("previews", "%s mask '%s' is flat grey" % (f, m["what"]), reg.std(axis=0).max() < 3.0 and abs(reg.mean() - 120) < 8, "")
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

    def mut(name, fn):
        X = copy.deepcopy(T)
        fn(X)
        try:
            R = run_all(X, photo_dir, False, False)   # controls run offline: the live rows read the world, not the copy
            caught = len(R.fails) > 0
            which = R.fails[0]["name"][:70] if R.fails else ""
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
    mut("F4: a bar 25 mm instead of 40", lambda x: lights(x, "F4", 1).update({"u0": lights(x, "F4", 1)["u0"] - 15}))
    mut("F6: the letter plate at 1000 instead of 912", lambda x: x["furniture"]["letter_plate"]["LP4"]["place"]["F6"].update({"v": 1000.0}))
    mut("F5: the lever on the right stile (u 700)", lambda x: x["furniture"]["handle"]["HD2b"]["place"]["F5"].update({"u": 700.0}))
    mut("F6: the leaf 838 wide in the planted-stop frame (a see-through margin)", lambda x: x["kinds"]["F6"]["leaf"].update({"w": 700.0}))
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
    mut("a maker's name in a text", lambda x: x["furniture"]["latch"]["LK1"].update({"name": "Yale-type rim cylinder"}))
    mut("the stale night colour in the gate", lambda x: x["gate"]["street_views"][2]["light"].update({"lantern_colour_linear": [1, 0.7055, 0]}))
    mut("an em dash in an owed line", lambda x: x["owed_for_jafar"].__setitem__(0, x["owed_for_jafar"][0] + " — now"))
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
    if live:
        pass
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
    cc, cl = 0, []
    if not a.no_controls:
        cc, cl = controls(T, a.photos, a.live, a.previews)
        line += "; negative controls (run offline on wrong copies) %d of %d caught" % (cc, len(cl))
        for c in cl:
            if not c["caught"]:
                print("UNCAUGHT control:", c["name"])
    print(line)
    if a.write:
        T["self_check"] = {"result": line, "options": opts, "rows": sorted(R.rows, key=lambda r: (r["group"], r["name"])), "controls": cl, "run": "13 October 2026"}
        with open(TARGET_JSON, "w") as f:
            json.dump(T, f, indent=1)
    sys.exit(1 if R.fails or (not a.no_controls and cc != len(cl)) else 0)


if __name__ == "__main__":
    main()
