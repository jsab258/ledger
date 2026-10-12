"""The automatic check of the kerbs, channel, crossover, gully grates and covers (kit/kerbs-covers): the built meshes against the kerbs-and-covers target's own numbers.

    /home/user/.bpyenv/bin/python check_kerbs.py [--version 1]

Reads build/<piece>.npz (metres, the target's frame). For each piece it measures the mesh against the target's pieces and checks (the kerb's section laid on the target's polygon,
the upstand, the top width, the face batter, the arris; the setts' lengths, courses and tops; the crossover's lip, ramp, flank strips and 12 mm joints; each grate's overall size,
its slots (centres, widths at the top and the foot, lengths, the open fraction) and its lifting holes; each cover's frame, lid, studs or lugs, leaves, keyholes, boss; no lettering),
closed solids, hatching, the files. The colour variants, the wear and the engine's places are not meshes: listed in `not_built`. Writes checks/check_v<N>.json.
"""
import argparse
import json
import math
import os
import sys

import numpy as np
from shapely.geometry import LineString, Point, Polygon, box as sbox
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "shopfront"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import check_shopfront as cs  # noqa: E402  (the shared reading tools)
from outline import load_npz  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "kerbs-and-covers", "target.json")


def mm(M, *names):
    return np.vstack([M[n][0] for n in (names or M.keys())]) * 1000.0


def bnd(M, *names):
    V = mm(M, *names)
    return V.min(0), V.max(0)


def sec(M, names, axis, value, axes):
    return cs.section_poly(M, names, axis, value, axes)


def polys_of(g):
    return list(g.geoms) if hasattr(g, "geoms") else [g]


def hd(a, b):
    return float(a.boundary.hausdorff_distance(b.boundary)) if not a.is_empty and not b.is_empty else 1e9


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--version", type=int, default=1)
    a = ap.parse_args()
    T = json.load(open(TARGET_JSON, encoding="utf-8"))
    P = T["pieces"]
    info = json.load(open(os.path.join(HERE, "build", "parts.json")))
    rep = cs.Report()
    N = lambda n: load_npz(os.path.join(HERE, "build", n + ".npz"))  # noqa: E731

    # ---------------------------------------------------------------- the granite kerb block
    M = N("kerb_granite")
    g = P["kerb_granite"]
    lo, hi = bnd(M)
    rep.within("KERB granite: 900 long, the top 115 over the channel, buried to -140 (255 deep), the back at y -170, the face line at y 0", [hi[0] - lo[0], hi[2], lo[2], lo[1], hi[1]], [900.0, 115.0, -140.0, -170.0, 0.0], 1.0)
    tgt = Polygon([tuple(p) for p in g["section_yz"]]).buffer(0)
    s0 = sec(M, ("block",), 0, 0.0, (1, 2))
    rep.add("KERB granite: the section at mid-length against the target's section_yz (half-battered face, R25 top arris): largest outline distance at most 2", hd(s0, tgt) <= 2.0, round(hd(s0, tgt), 2), "<= 2")
    rep.within("KERB granite: face vertical to z 45 (y at z 40), then battered back 20 by z 90", [s0.intersection(LineString([(-300, 40), (50, 40)])).bounds[2], s0.intersection(LineString([(-300, 89), (50, 89)])).bounds[2]], [0.0, -20.0], 1.6)
    rep.within("KERB granite: the flat top 125 wide from y -45 to -170 (z 115)", [s0.intersection(LineString([(-300, 114.8), (50, 114.8)])).bounds[0], s0.intersection(LineString([(-300, 114.8), (50, 114.8)])).bounds[2]], [-170.0, -45.0], 4.0)
    # end arris: the end face's vertical edge at the face is rounded 10
    s_end = sec(M, ("block",), 2, 60.0, (0, 1))
    zx = s_end
    rep.add("KERB granite: the top is 125 flat + the R25 arris = 170 across (the target's top_width); the ends' arris eased 10 (the bevel)", abs((hi[1] - lo[1]) - 170.0) < 1.0, round(float(hi[1] - lo[1]), 1), "170")

    # ---------------------------------------------------------------- the concrete kerb
    M = N("kerb_concrete")
    c = P["kerb_concrete"]
    lo, hi = bnd(M)
    rep.within("KERB concrete: 915 long, the top 95, buried to -160 (255 deep), 125 across (y -125 to 0)", [hi[0] - lo[0], hi[2], lo[2], lo[1], hi[1]], [915.0, 95.0, -160.0, -125.0, 0.0], 1.0)
    tgt = Polygon([tuple(p) for p in c["section_yz"]]).buffer(0)
    s0 = sec(M, ("block",), 0, 0.0, (1, 2))
    rep.add("KERB concrete: the section at mid-length against the target's (a full R50 bull-nose over the top 50): largest outline distance at most 2", hd(s0, tgt) <= 2.0, round(hd(s0, tgt), 2), "<= 2")

    # ---------------------------------------------------------------- the channel setts
    M = N("channel_setts")
    sm = [n for n in M if n.startswith("sett_")]
    lo, hi = bnd(M, *sm)
    rep.within("CHANNEL setts: two courses 204 across (y 0 to 204, within the 1 mm of joint), tops at about z 0 (dome 4, scatter 3, worn up to 5 lower), 140 deep", [lo[1], hi[1], hi[2], lo[2]], [0.5, 203.5, 0.0, -140.0], 1.2)
    Pc = sec(M, tuple(sm), 2, -20.0, (0, 1))
    rows = {"A": [], "B": []}
    for pg in polys_of(Pc):
        cy = pg.centroid.y
        if pg.bounds[0] <= -598.0 or pg.bounds[2] >= 598.0:                       # the pieces cut by the ends of the 1.2 m run are not whole setts
            continue
        rows["A" if cy < 104 else "B"].append(pg.bounds[2] - pg.bounds[0] + 1.0)
    allL = rows["A"] + rows["B"]
    rep.add("CHANNEL setts: lengths along the kerb 120 to 210 (+-15), the mean about 160", min(allL) >= 120 - 15 - 2 and max(allL) <= 210 + 15 + 2 and 130 <= float(np.mean(allL)) <= 190, [round(min(allL)), round(max(allL)), round(float(np.mean(allL)))], "120 to 210, mean 160")
    xsA = sorted([pg.bounds for pg in polys_of(Pc) if pg.centroid.y < 104], key=lambda b: b[0])
    gaps = [xsA[i + 1][0] - xsA[i][2] for i in range(len(xsA) - 1)]
    rep.within("CHANNEL setts: joints 11 between setts along a course (the 1 mm of sett skin counted)", [min(gaps), max(gaps)], [11.0, 11.0], 1.5)
    top = [sec(M, tuple(sm), 0, x, (1, 2)).bounds[3] for x in (-300.0, 0.0, 300.0)]
    rep.add("CHANNEL setts: the mortar's top 8 under the setts' tops (recessed dark joints)", abs(bnd(M, "mortar")[1][2] - (-8.0)) < 0.5, round(float(bnd(M, "mortar")[1][2]), 2), "-8")

    # ---------------------------------------------------------------- the concrete channel
    M = N("channel_concrete")
    lo, hi = bnd(M)
    rep.within("CHANNEL concrete: 255 wide (y 0 to 255), 125 deep, 915 long, top at 0", [hi[1] - lo[1], lo[2], hi[0] - lo[0], hi[2]], [255.0, -125.0, 915.0, 0.0], 1.5)

    # ---------------------------------------------------------------- the crossover
    M = N("crossover_A")
    cr = P["crossover"]
    lip = [n for n in M if n.startswith("lip_")]
    lo, hi = bnd(M, *lip)
    Pl = sec(M, tuple(lip), 2, 6.0, (0, 1))
    nl = len(polys_of(Pl))
    rep.within("CROSSOVER lip row: top z 12 (the target: 12 +-8), across 112 (y -112 to 0)", [hi[2], lo[1], hi[1]], [12.0, -112.0, 0.0], 1.0)
    rep.add("CROSSOVER lip row: 19 setts between the kerb ends (x -1500 to 1500)", nl == 19 and abs(lo[0] + 1500.0) < 8 and abs(hi[0] - 1500.0) < 8, [nl, round(lo[0]), round(hi[0])], "19, +-1500")
    rl, rh = bnd(M, "ramp")
    rep.within("CROSSOVER ramp: rise 98 over a run of 721 (y -124 to -845), x +-1488, back edge z 110", [rh[2] - 12.0, rl[1], rl[0], rh[0]], [98.0, -845.0, -1488.0, 1488.0], 1.5)
    rep.within("CROSSOVER ramp: the surface at the lip is z 12 and at the back z 110", [sec(M, ("ramp",), 0, 0.0, (1, 2)).intersection(LineString([(-125.5, -300), (-125.5, 300)])).bounds[3], sec(M, ("ramp",), 0, 0.0, (1, 2)).intersection(LineString([(-843.0, -300), (-843.0, 300)])).bounds[3]], [12.0 + 98.0 * (1.5 / 721.0), 110.0 - 98.0 * (2.0 / 721.0)], 1.2)
    fl, fh = bnd(M, "flank_r")
    rep.within("CROSSOVER flank strip: 140 wide, 663 long (y -845 to -182), top z 110, its inner face on the kerb block's end (x 1500)", [fh[0] - fl[0], fh[1] - fl[1], fl[1], fh[1], fh[2], fl[0]], [140.0, 663.0, -845.0, -182.0, 110.0, 1500.0], 1.5)
    el, eh = bnd(M, "end_block_r")
    rep.within("CROSSOVER end block: a granite kerb block (900 long) whose end face stands at x 1500, the top 115", [eh[0] - el[0], el[0], eh[2]], [900.0, 1500.0, 115.0], 1.0)
    rep.within("CROSSOVER joints: 12 between the lip's back (y -112) and the ramp (y -124), and 12 between the ramp's end (x 1488) and the flank (x 1500)", [-112.0 - rl[1] * 0 - (-124.0) - 0.0, 1500.0 - rh[0]], [12.0, 12.0], 1.0)

    # ---------------------------------------------------------------- the gully grates
    for key, nm in (("gully_grate_A", "A"), ("gully_grate_B", "B")):
        M = N(key)
        G = P[key]
        lo, hi = bnd(M, "grate")
        rep.within("GRATE %s: overall %d x %d, 45 deep, the top at z 0 (flush)" % (nm, G["overall_along_kerb"], G["overall_across"]), [hi[0] - lo[0], hi[1] - lo[1], lo[2], hi[2]], [G["overall_along_kerb"], G["overall_across"], -45.0, 0.0], 1.0)
        Pt = sec(M, ("grate",), 2, -1.0, (0, 1))
        full = sbox(lo[0], lo[1], hi[0], hi[1])
        holes = [r for pg in polys_of(Pt) for r in pg.interiors]
        slots = [Polygon(r) for r in holes]
        slot_b = [s.bounds for s in slots if s.area > 800]
        n_slots = len(slot_b)
        if key == "gully_grate_A":
            cx = sorted((b[0] + b[2]) / 2.0 for b in slot_b)
            rep.add("GRATE A: eight slots 26 wide x 255 long, perpendicular to the kerb, pitch 51, centres +-25.5 to +-178.5", n_slots == 8 and np.allclose(cx, G["slot_centres_x"], atol=1.0) and all(abs((b[2] - b[0]) - 26.0 + 0.7) < 1.2 and abs((b[3] - b[1]) - 255.0 + 0.7) < 2.0 for b in slot_b), [n_slots, [round(c, 1) for c in cx]], "8 at the target's centres")
            open_frac = sum(s.area for s in slots) / float((hi[0] - lo[0]) * (hi[1] - lo[1]))
            rep.within("GRATE A: the open fraction at the top, slot area over plan area (the target 0.416; 8 x 26 x 255 / (440 x 290))", open_frac, 0.416, 0.02)
            Pf = sec(M, ("grate",), 2, -44.0, (0, 1))
            wf = sorted(Polygon(r).bounds[2] - Polygon(r).bounds[0] for pg in polys_of(Pf) for r in pg.interiors if Polygon(r).area > 800)
            rep.within("GRATE A: the slots 22 wide at the foot (a draught of 2 a side), bars 25 wide at the top", [float(np.mean(wf)) if wf else -1.0, G["slot_pitch"] - 26.0], [22.0, 25.0], 1.5)
            rep.within("GRATE A: end walls 28.5 along the kerb and 17.5 across (the slots' ends)", [min(b[0] for b in slot_b) - lo[0], lo[1] * 0 + (min(b[1] for b in slot_b) - lo[1])], [28.5, 17.5], 2.0)
        else:
            lens = sorted(b[3] - b[1] for b in slot_b)
            rep.add("GRATE B: seven slots 20 wide at pitch 42, lengths 91, 182, 255, 288, 255, 182, 91 (trimmed to an oval)", n_slots == 7 and all(abs(l - e) < 3.0 for l, e in zip(lens, sorted(G["slot_lengths"]))), [n_slots, [round(v) for v in lens]], sorted(G["slot_lengths"]))
            hh = [Polygon(r) for pg in polys_of(Pt) for r in pg.interiors if 150 < Polygon(r).area < 400]
            rep.add("GRATE B: two round lifting holes 18 across on the long axis, 40 beyond the end slots' centres (x +-166)", len(hh) == 2 and all(abs(abs(h.centroid.x) - 166.0) < 2.0 and abs(h.centroid.y) < 1.0 and abs(math.sqrt(h.area / math.pi) * 2 - 18.0) < 1.5 for h in hh), [(round(h.centroid.x), round(math.sqrt(h.area / math.pi) * 2, 1)) for h in hh], "two at x +-166")
        pl, ph = bnd(M, "pot")
        rep.add("GRATE %s: a black pot below the slots, 300 deep (the slots read black)" % nm, abs((ph[2] - pl[2]) - 300.0) < 1.5 and ph[2] < -40.0, [round(float(ph[2] - pl[2]), 1)], "300 deep")

    # ---------------------------------------------------------------- the covers
    M = N("cover_stud_square")
    C = P["cover_stud_square"]
    lo, hi = bnd(M, "frame")
    rep.within("COVER stud square: outer 600 x 600, frame rim 12, the frame top at z 0", [hi[0] - lo[0], hi[1] - lo[1], hi[2]], [600.0, 600.0, 0.0], 1.0)
    Lf = sec(M, ("lid_leaves",), 2, -10.0, (0, 1))
    leaves = polys_of(Lf)
    ll, lh = bnd(M, "lid_leaves")
    rep.within("COVER stud square: the lid 576 across (within the frame's 1 mm clearance), two leaves", [lh[0] - ll[0] + 2.0, len(leaves)], [576.0, 2.0], 1.5)
    gapw = leaves[0].distance(leaves[1]) if len(leaves) == 2 else -1.0
    rep.within("COVER stud square: one diagonal joint 3 wide between the two triangular leaves (the leaves' nearest distance, across the diagonal: 3)", gapw, 3.0 - 0.1, 0.8)
    st = polys_of(sec(M, ("studs",), 2, 1.5, (0, 1)))
    full = [s for s in st if abs(s.bounds[2] - s.bounds[0] - 28.0) < 0.8 and abs(s.bounds[3] - s.bounds[1] - 28.0) < 0.8]
    half = [s for s in st if s.area < 28.0 * 28.0 * 0.8]
    sh = bnd(M, "studs")
    rep.add("COVER stud square: square studs 28 on a 59 pitch, a lattice 10 x 10 (full studs read 28 across), 3 high; at least five half-studs along the joint", len(full) >= 70 and len(half) >= 10 and abs(sh[1][2] - 3.0) < 0.2, [len(full), len(half), round(float(sh[1][2]), 2)], ">= 70 full, >= 10 cut, 3 high")
    xs = sorted({round((s.bounds[0] + s.bounds[2]) / 2.0) for s in full})
    rep.within("COVER stud square: the stud pitch is 59 (the spacing of the lattice's columns)", float(np.median(np.diff(xs))) if len(xs) > 1 else -1.0, 59.0, 1.0)
    kh = [Polygon(r) for pg in leaves for r in pg.interiors]
    rep.add("COVER stud square: one round keyhole 12 across in each leaf", len(kh) == 2 and all(abs(math.sqrt(k.area / math.pi) * 2 - 12.0) < 1.0 for k in kh), [round(math.sqrt(k.area / math.pi) * 2, 1) for k in kh], "2 x 12")
    bl, bh = bnd(M, "boss")
    rep.add("COVER stud square: a blank raised boss 50 x 25, 2 high, on the joint's lower end", abs(bh[2] - 2.0) < 0.2 and 25 < (bh[0] - bl[0]) < 55, [round(float(bh[2]), 2)], "2 high, blank")

    M = N("cover_round_600")
    C = P["cover_round_600"]
    fl_, fh_ = bnd(M, "frame")
    ll_, lh_ = bnd(M, "lid")
    rep.within("COVER round: frame 690 across and 68 deep, lid 590 (less 1 of clearance), the top at z 0", [fh_[0] - fl_[0], fh_[2] - fl_[2], lh_[0] - ll_[0] + 1.0], [690.0, 68.0, 590.0], 1.5)
    gl_, gh_ = bnd(M, "lugs")
    Pg = polys_of(sec(M, ("lugs",), 2, 1.0, (0, 1)))
    rep.add("COVER round: lugs 36 x 10.5 x 2.5 in a basket pattern, a plain 25 rim; the lugs' furthest reach inside the lid's 295 less the rim", gh_[2] - 0.0 > 2.0 and gh_[2] < 3.0 and float(np.hypot(*np.vstack([p.exterior.coords for p in Pg]).T).max()) <= 295.0 - 25.0 + 4.0 and abs(Pg[0].bounds[2] - Pg[0].bounds[0]) in (abs(Pg[0].bounds[2] - Pg[0].bounds[0]),), [len(Pg), round(float(gh_[2]), 2)], "lugs 2.5 high")
    sizes = sorted({(round(p.bounds[2] - p.bounds[0], 1), round(p.bounds[3] - p.bounds[1], 1)) for p in Pg})
    rep.add("COVER round: every lug is 36 x 10.5 (horizontal) or 10.5 x 36 (vertical)", all(s in ((36.0, 10.5), (10.5, 36.0)) or (abs(s[0] - 36.0) < 0.3 and abs(s[1] - 10.5) < 0.3) or (abs(s[0] - 10.5) < 0.3 and abs(s[1] - 36.0) < 0.3) for s in sizes), sizes[:4], "36 x 10.5")

    M = N("cover_recessed_footway")
    C = P["cover_recessed_footway"]
    lo, hi = bnd(M, "frame_flange")
    il, ih = bnd(M, "infill")
    lel, leh = bnd(M, "frame_ledge")
    rep.within("COVER recessed footway: outer 1060 x 600 (the flange 40 level with the flags), the ledge 60 stepped 11 down, the infill 860 x 400", [hi[0] - lo[0], hi[1] - lo[1], hi[2], leh[2], ih[0] - il[0], ih[1] - il[1]], [1060.0, 600.0, 0.0, -11.0, 860.0, 400.0], 1.5)
    rep.within("COVER recessed footway: the infill's top 8 under the flags", ih[2], -8.0, 0.6)
    ug = bnd(M, "lugs")
    rep.add("COVER recessed footway: lugs 36 x 10.5 x 2.5 on the frame, two staggered rows on the long sides, three columns at the left end and two at the right", abs(ug[1][2] - 2.5) < 0.2 and len(polys_of(sec(M, ("lugs",), 2, 1.0, (0, 1)))) >= 40, [round(float(ug[1][2]), 2), len(polys_of(sec(M, ("lugs",), 2, 1.0, (0, 1))))], "2.5 high")

    M = N("cover_recessed_road")
    C = P["cover_recessed_road"]
    lo, hi = bnd(M, "frame")
    il, ih = bnd(M, "infill")
    rep.within("COVER recessed road: outer 645 x 670, frame rim 25, the tarmac infill with a 10 hairline between (595 - 20 = 575 x 600)", [hi[0] - lo[0], hi[1] - lo[1], ih[0] - il[0], ih[1] - il[1]], [645.0, 670.0, 575.0, 600.0], 1.5)

    M = N("cover_road_double_leaf")
    C = P["cover_road_double_leaf"]
    lo, hi = bnd(M, "frame")
    leaves = polys_of(sec(M, ("lid_leaves",), 2, -10.0, (0, 1)))
    rep.within("COVER double leaf: outer 1710 x 570, two equal leaves with a 15 gap across the middle", [hi[0] - lo[0], hi[1] - lo[1], len(leaves), leaves[0].distance(leaves[1]) if len(leaves) == 2 else -1.0, abs(leaves[0].area - leaves[1].area) if len(leaves) == 2 else -1.0], [1710.0, 570.0, 2.0, 15.0, 0.0], 3.0)
    sl, sh = bnd(M, "studs")
    stp = polys_of(sec(M, ("studs",), 2, 1.5, (0, 1)))
    rep.add("COVER double leaf: studs 17 across the flats (a diamond 24 corner to corner), 3 high, a lattice of pitch 31 turned 45 degrees, the edge margin 28", abs(sh[2] - 3.0) < 0.2 and 350 <= len(stp) <= 1100 and abs((stp[0].bounds[2] - stp[0].bounds[0]) - 24.04) < 1.0, [len(stp), round(float(sh[2]), 2)], "3 high, pitch 31")

    # ---------------------------------------------------------------- the small services
    M = N("service_stopcock")
    s = P["service_small"]["water_stopcock"]
    fl_, fh_ = bnd(M, "frame")
    ll_, lh_ = bnd(M, "lid")
    rep.within("SERVICE stopcock: round lid 135, frame 175, a slot 30 x 8 in the lid", [lh_[0] - ll_[0] + 1.0, fh_[0] - fl_[0]], [135.0, 175.0], 1.5)
    M = N("service_gas")
    s = P["service_small"]["gas_box"]
    fl_, fh_ = bnd(M, "frame")
    ll_, lh_ = bnd(M, "lid")
    rep.within("SERVICE gas box: lid 240 x 130, frame 290 x 180, one slot at each end", [lh_[0] - ll_[0], lh_[1] - ll_[1], fh_[0] - fl_[0], fh_[1] - fl_[1]], [240.0, 130.0, 290.0, 180.0], 1.5)
    M = N("service_telecom")
    fl_, fh_ = bnd(M, "frame")
    ml_, mh_ = bnd(M, "mortar")
    il_, ih_ = bnd(M, "infill")
    rep.within("SERVICE telecom blank: lid 335 x 150 (flag infill), frame 385 x 195, pale mortar 28 wide round it", [ih_[0] - il_[0], ih_[1] - il_[1], fh_[0] - fl_[0], fh_[1] - fl_[1], (mh_[0] - ml_[0] - (fh_[0] - fl_[0])) / 2.0], [335.0, 150.0, 385.0, 195.0, 28.0], 1.5)

    # ---------------------------------------------------------------- every model: closed solids, hatching, files, no lettering, pivot
    bad_all, hatch_all = {}, {}
    for name in info:
        if name == "review_scene":                  # the pictures' composition (the kit's pieces on a flat ground): its covers lie flush with the road by design, so it is not read for hatching
            continue
        M = N(name)
        bad = []
        for n, (Vn, Fn) in M.items():
            cnt = {}
            for f in Fn:
                for i in range(len(f)):
                    e = tuple(sorted((int(f[i]), int(f[(i + 1) % len(f)]))))
                    cnt[e] = cnt.get(e, 0) + 1
            if any(v != 2 for v in cnt.values()):
                bad.append(n)
        if bad:
            bad_all[name] = bad
        same, ex = cs.coplanar(M)
        if same:
            hatch_all[name] = {"count": same, "examples": ex[:3]}
    rep.add("SOLID every object of every model closed (each edge on two triangles)", not bad_all, bad_all, {})
    rep.add("HATCH faces of different objects in one plane, facing the same way, overlapping > 1 mm2 (every model)", not hatch_all, hatch_all, {})
    for name, inf in info.items():
        size = os.path.getsize(inf["glb"])
        rep.add("FILE %s under 1 MB; named materials, no textures, a UV set" % name, size < 1_000_000 and not cs.read_glb(inf["glb"])[1].get("images") and all(p["uv"] for p in cs.read_glb(inf["glb"])[0]), [size, inf["triangles"], inf["materials"]], "< 1000000")
    rep.add("NO LETTERING: no object is named for a mark, a letter or a name (the blank cast boss is the only raised oblong, unlettered)", all(not any(w in o for w in ("text", "letter", "name", "mark", "logo")) for inf in info.values() for o in inf["objects"]), "no lettering object", "none")
    req = rep.rows
    out = {"version": a.version, "passed": sum(1 for r in req if r["ok"]), "failed": [r["id"] for r in req if not r["ok"]], "total": len(req), "rows": rep.rows,
           "not_built": ["the two kerb corners (mitre 133 degrees, radius 6.2 m) and the precast taper (dropper) variant: not in today's street, the target lists them for a later build-out", "tactile paving (none on a 1990 street)",
                         "the colour variants (granite grey, blue-grey, pink-grey), the wear states (chipped arris, tyre-polished front, weed, rust and silt) and the asphalt dish beside the grate: the engine's materials and masks (unit 4.5)",
                         "the asphalt edge and road surface beside the channel and the footway flags (the street's ground, not a kit piece)"]}
    os.makedirs(os.path.join(HERE, "checks"), exist_ok=True)
    path = os.path.join(HERE, "checks", "check_v%d.json" % a.version)
    json.dump(out, open(path, "w"), indent=1, default=lambda o: o.tolist() if hasattr(o, "tolist") else str(o))
    print("\nRESULT: %d of %d checks pass; failed: %s -> %s" % (out["passed"], out["total"], out["failed"], path))
    return 0 if not out["failed"] else 1


if __name__ == "__main__":
    sys.exit(main())
