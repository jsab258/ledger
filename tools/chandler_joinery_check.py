#!/usr/bin/env python3
"""THE CHANDLER'S JOINERY WEAR MEASURED IN THE GAME'S OWN BASE-COLOUR VIEW (his order D11, the look; production/research/
street-wear/MAFIA-WEAR-2026-10-28.md, section 5, S2 joinery, and the calibration's C6).

    python tools/chandler_joinery_check.py buffers WITH_DIR WITHOUT_DIR      # the front with its paint over wood, and without
    python tools/chandler_joinery_check.py sheets OUT_DIR DAY_DIR NIGHT_DIR  # the side-by-side sheets for the reviewers
    python tools/chandler_joinery_check.py --selftest

Each DIR of `buffers` is a tools/office_look.py --editor --buffers run at one camera (basecolor.png and look-lines.txt,
whose camera line places the front on screen), anti-aliasing and texture streaming off (-ExecCmds "r.AntiAliasingMethod
0,r.TextureStreaming 0": the S1 helper's finding of 30 October, a 3% drift a column otherwise); WITHOUT_DIR the same view
with the front's previous copy (the shop's entry naming chandler-front-worn).

THE CHECK (the method's S2): worn or bare paint 3 to 10% of the joinery's area, all within 5 cm of an edge or a handle;
C6: albedo 0.03 to 0.88, wood's median 0.09 to 0.36. Measured so:
  * WHERE THE JOINERY IS ON SCREEN: the front's own glb (production/specs/shop-fronts/chandler-front-joinery.json's out,
    on F:'s game inputs) drawn through the logged camera with a depth test over all its parts, where the game stands it
    (shop-interiors.json: street x 43.0, its wall face 5.295, 0.1 up, turned to face the road), each pixel keeping its
    part's material and its place on the model; the joinery is the pixels whose nearest surface is a named paint.
  * WORN OR BARE: a joinery pixel whose base colour changed by more than CHANGED (the largest of its three channels'
    change over that channel's old value, linear); its share of the joinery's pixels is the area the eye sees.
  * WITHIN 5 CM: each worn pixel's place on the model against the paints' convex arrises (as front_joinery.py finds them),
    the fascia's box edges and the knob; the share within 5 cm (and 3 mm for the pixel's own size).
  * THE PAINT KEPT: the median ratio, new over old, of the joinery's unworn pixels' luminance (1.00 is his colour kept).
  * C6: the worn pixels' luminance from their 2nd to their 98th percentile in 0.03 to 0.88; the bare wood's (worn pixels
    turned warm: red over blue by more than WARM) median in 0.09 to 0.36.
"""
import json
import math
import os
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "tools"))
sys.path.insert(0, os.path.join(REPO, "tools", "art-recipes"))
import chandler_wear_check as cwc  # noqa: E402
import front_joinery as fj  # noqa: E402

SPEC = os.path.join(REPO, "production", "specs", "shop-fronts", "chandler-front-joinery.json")
FRONT_AT = (43.0, 5.295, 0.1)      # shop-interiors.json's chandler front: x, z (its wall face), up; east side, turned 180
CHANGED = 0.30
WARM = 0.05
AREA_BAND, NEAR_M, PIXEL_M = (0.03, 0.10), 0.05, 0.003
ALBEDO_BAND, WOOD_BAND = (0.03, 0.88), (0.09, 0.36)
LAST_GOOD = "F:/LedgerTools/gate/last-good/chandler"
AFTER_S1 = "F:/LedgerTools/gate/new/chandler-wear/after"


def to_unreal_cm(p):
    """The front's glTF frame (x across, y up, z out, metres) to the street in Unreal cm, as VignetteShot.cpp stands it."""
    x, z, up = FRONT_AT
    p = np.asarray(p, dtype=np.float64)
    return np.stack([(x - p[..., 0]) * 100.0, (z - p[..., 2]) * 100.0, (up + p[..., 1]) * 100.0], axis=-1)


def project_many(cam, P, w, h):
    """stain_check.project for many points: (x, y) pixels and the depth along the view, cm."""
    cx, cy, cz, pitch, yaw, fov = cam
    th, ps = math.radians(pitch), math.radians(yaw)
    f = np.array([math.cos(th) * math.cos(ps), math.cos(th) * math.sin(ps), math.sin(th)])
    r = np.array([-math.sin(ps), math.cos(ps), 0.0])
    u = np.array([-math.sin(th) * math.cos(ps), -math.sin(th) * math.sin(ps), math.cos(th)])
    d = P - np.array([cx, cy, cz])
    depth = d @ f
    k = (w / 2.0) / math.tan(math.radians(fov) / 2.0)
    safe = np.where(depth > 1.0, depth, np.nan)
    return np.stack([w / 2.0 + k * (d @ r) / safe, h / 2.0 - k * (d @ u) / safe], axis=-1), depth


def draw(cam, tris_world, tris_model, mat_ids, w, h):
    """A depth-tested drawing of triangles: per pixel its material id (-1 none) and its place on the model (glTF m),
    by perspective-correct weights at the pixel's centre."""
    zbuf = np.full((h, w), np.inf)
    mid = -np.ones((h, w), dtype=np.int32)
    pos = np.zeros((h, w, 3))
    flat = tris_world.reshape(-1, 3)
    xy, depth = project_many(cam, flat, w, h)
    xy = xy.reshape(-1, 3, 2)
    depth = depth.reshape(-1, 3)
    for t in range(len(xy)):
        a, b, c = xy[t]
        if not np.isfinite(xy[t]).all():
            continue
        x0, x1 = max(0, int(math.floor(min(a[0], b[0], c[0])))), min(w - 1, int(math.ceil(max(a[0], b[0], c[0]))))
        y0, y1 = max(0, int(math.floor(min(a[1], b[1], c[1])))), min(h - 1, int(math.ceil(max(a[1], b[1], c[1]))))
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        dd = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(dd) < 1e-12:
            continue
        l1 = ((b[1] - c[1]) * (gx - c[0]) + (c[0] - b[0]) * (gy - c[1])) / dd
        l2 = ((c[1] - a[1]) * (gx - c[0]) + (a[0] - c[0]) * (gy - c[1])) / dd
        l3 = 1.0 - l1 - l2
        m = (l1 >= 0) & (l2 >= 0) & (l3 >= 0)
        if not m.any():
            continue
        iz = l1[m] / depth[t, 0] + l2[m] / depth[t, 1] + l3[m] / depth[t, 2]
        z = 1.0 / iz
        yy, xx = (gy[m] - 0.5).astype(int), (gx[m] - 0.5).astype(int)
        closer = z < zbuf[yy, xx]
        if not closer.any():
            continue
        yy, xx, z = yy[closer], xx[closer], z[closer]
        wb = np.stack([l1[m][closer] / depth[t, 0], l2[m][closer] / depth[t, 1], l3[m][closer] / depth[t, 2]], axis=1) * z[:, None]
        zbuf[yy, xx] = z
        mid[yy, xx] = mat_ids[t]
        pos[yy, xx] = wb @ tris_model[t]
    return mid, pos


def front_geometry(spec):
    """Every triangle of the front's glb (model metres), its material index, the material names; the joinery's convex
    arrises (sampled) and the knob's points; the box paints' boxes."""
    j, binbuf = fj.read_glb(os.path.join(fj.GAME_INPUTS, fj.FRONTS_REL, spec["out"] + ".glb"))
    names = [m.get("name") for m in j["materials"]]
    tris, mats, edges, boxes, hand = [], [], [], {}, [np.asarray(spec["handles"]["points"], dtype=np.float64).reshape(-1, 3)]
    for pr in j["meshes"][0]["primitives"]:
        P = fj.accessor(j, binbuf, pr["attributes"]["POSITION"]).astype(np.float64)
        I = fj.accessor(j, binbuf, pr["indices"]).astype(np.int64).reshape(-1, 3)
        name = names[pr["material"]]
        tris.append(P[I])
        mats.append(np.full(len(I), pr["material"]))
        if name in spec["handles"].get("materials", []):
            hand.append(P)
        cfg = spec["paints"].get(name)
        if cfg is None:
            continue
        if cfg["edges"] == "box":
            boxes[pr["material"]] = (P.min(axis=0), P.max(axis=0))
            continue
        V = P[I]
        N, area = fj.face_normals(V)
        keep = area > 1e-12
        w = fj.weld(P, spec["weld_m"])
        Pw = np.zeros((w.max() + 1, 3))
        Pw[w] = P
        convex, _ = fj.sharp_edges(w[I[keep]], Pw, N[keep], spec["sharp_deg"])
        edges.append(fj.edge_samples(Pw, convex))
    paint_ids = [i for i, n in enumerate(names) if n in spec["paints"]]
    return (np.concatenate(tris), np.concatenate(mats), names, paint_ids, np.concatenate(edges), boxes, np.concatenate(hand))


def measure(base_with, base_without, mid, pos, names, paint_ids, edge_pts, boxes, hand_pts):
    from scipy.spatial import cKDTree
    lw, lo = cwc.stain_check.srgb_to_linear(base_with), cwc.stain_check.srgb_to_linear(base_without)
    joinery = np.isin(mid, paint_ids)
    rel = (np.abs(lw - lo) / np.maximum(lo, 0.01)).max(axis=2)
    worn = joinery & (rel > CHANGED)
    lum_w, lum_o = lw @ cwc.LUM, lo @ cwc.LUM
    ys, xs = np.nonzero(worn)
    p = pos[ys, xs]
    d = np.full(len(p), np.inf)
    if len(edge_pts):
        d = np.minimum(d, cKDTree(edge_pts).query(p)[0])
    if len(hand_pts):
        d = np.minimum(d, cKDTree(hand_pts).query(p)[0])
    for m, (lo_b, hi_b) in boxes.items():
        on = mid[ys, xs] == m
        d[on] = np.minimum(d[on], fj.box_edge(p[on], lo_b, hi_b))
    out = {"joinery_px": int(joinery.sum()), "worn_px": int(worn.sum()),
           "worn_share": round(float(worn.sum() / max(joinery.sum(), 1)), 4),
           "within_5cm_share": round(float((d <= NEAR_M + PIXEL_M).mean()) if len(d) else 1.0, 4),
           "worn_distance_p50_p95_max_cm": [round(float(np.percentile(d, q)) * 100, 2) for q in (50, 95, 100)] if len(d) else None,
           "by_paint": {}}
    for m in paint_ids:
        j_m = mid == m
        if j_m.sum() == 0:
            continue
        out["by_paint"][names[m]] = {"joinery_px": int(j_m.sum()), "worn_share": round(float((worn & j_m).sum() / j_m.sum()), 4)}
    keep = joinery & ~worn & (lum_o > 0.002)
    out["paint_kept_ratio_median"] = round(float(np.median(lum_w[keep] / lum_o[keep])), 4) if keep.any() else None
    out["paint_kept_ratio_p5_p95"] = ([round(float(np.percentile(lum_w[keep] / lum_o[keep], q)), 4) for q in (5, 95)]
                                      if keep.any() else None)
    if worn.any():
        lv = lum_w[worn]
        out["worn_lum_p2_p98"] = [round(float(np.percentile(lv, 2)), 4), round(float(np.percentile(lv, 98)), 4)]
        warm = worn & ((lw[..., 0] - lw[..., 2]) > WARM)
        out["bare_px"] = int(warm.sum())
        out["bare_lum_median"] = round(float(np.median(lum_w[warm])), 4) if warm.any() else None
        # AND THE BARE WOOD'S AREA AS COVER, not pixels: a pixel part chip and part paint counts as its part, read from
        # the red-over-blue shift against the bare pixels' own (a lower bound: the worn rim counts only as far as it
        # warmed); the pixel share above counts every pixel changed past CHANGED whole
        rb_w, rb_o = lw[..., 0] - lw[..., 2], lo[..., 0] - lo[..., 2]
        if warm.any():
            full = float(np.median(rb_w[warm]))
            f = np.clip((rb_w - rb_o) / np.maximum(full - rb_o, 1e-3), 0.0, 1.0)
            out["bare_cover_share"] = round(float(f[joinery].mean()), 4)
    else:
        out["worn_lum_p2_p98"], out["bare_px"], out["bare_lum_median"] = None, 0, None
    out["area_ok"] = bool(AREA_BAND[0] <= out["worn_share"] <= AREA_BAND[1])
    out["near_ok"] = bool(out["within_5cm_share"] >= 0.999)
    out["c6_ok"] = bool(out["worn_lum_p2_p98"] is not None and ALBEDO_BAND[0] <= out["worn_lum_p2_p98"][0]
                        and out["worn_lum_p2_p98"][1] <= ALBEDO_BAND[1] and out["bare_lum_median"] is not None
                        and WOOD_BAND[0] <= out["bare_lum_median"] <= WOOD_BAND[1])
    out["ok"] = out["area_ok"] and out["near_ok"] and out["c6_ok"]
    return out


def run_buffers(with_dir, without_dir, spec_path=SPEC):
    spec = json.load(open(spec_path, encoding="utf-8"))
    cam = cwc.camera(with_dir)
    bw = cwc.stain_check.load(os.path.join(with_dir, "basecolor.png"))
    bo = cwc.stain_check.load(os.path.join(without_dir, "basecolor.png"))
    h, w = bw.shape[:2]
    tris, mats, names, paint_ids, edge_pts, boxes, hand_pts = front_geometry(spec)
    mid, pos = draw(cam, to_unreal_cm(tris), tris, mats, w, h)
    res = measure(bw, bo, mid, pos, names, paint_ids, edge_pts, boxes, hand_pts)
    res["camera"] = list(cam)
    # a picture of what was counted: the joinery grey, the worn pixels red, the rest dark
    from PIL import Image
    show = (bw * 0.25 * 255).astype(np.uint8)
    show[np.isin(mid, paint_ids)] = (110, 110, 110)
    rel = (np.abs(cwc.stain_check.srgb_to_linear(bw) - cwc.stain_check.srgb_to_linear(bo))
           / np.maximum(cwc.stain_check.srgb_to_linear(bo), 0.01)).max(axis=2)
    show[np.isin(mid, paint_ids) & (rel > CHANGED)] = (255, 40, 40)
    Image.fromarray(show).save(os.path.join(with_dir, "joinery-counted.png"))
    json.dump(res, open(os.path.join(with_dir, "joinery-check.json"), "w", encoding="utf-8"), indent=1)
    print("joineryWear worn-or-bare %.1f%% of %d joinery px (band 3 to 10%%) %s; within 5 cm %.1f%% (median %.1f cm, "
          "p95 %.1f, max %.1f) %s; paint kept: unworn new/old %.3f (p5 %.3f, p95 %.3f); C6 worn %s, bare wood median %s "
          "over %d px (0.09 to 0.36) %s; bare wood as cover %.1f%%; by paint %s => %s" % (
              100 * res["worn_share"], res["joinery_px"], "PASS" if res["area_ok"] else "FAIL", 100 * res["within_5cm_share"],
              *(res["worn_distance_p50_p95_max_cm"] or [0, 0, 0]), "PASS" if res["near_ok"] else "FAIL",
              res["paint_kept_ratio_median"] or 0, *(res["paint_kept_ratio_p5_p95"] or [0, 0]), res["worn_lum_p2_p98"],
              res["bare_lum_median"], res["bare_px"], "PASS" if res["c6_ok"] else "FAIL", 100 * res.get("bare_cover_share", 0.0),
              {k: v["worn_share"] for k, v in res["by_paint"].items()}, "PASS" if res["ok"] else "FAIL"))
    return 0 if res["ok"] else 1


def sheets(out_dir, day_dir, night_dir):
    """Each view by day and at night: the 23 October last good, today's after S1, and this, side by side, labelled."""
    from PIL import Image, ImageDraw, ImageFont
    os.makedirs(out_dir, exist_ok=True)
    try:
        font = ImageFont.truetype("arial.ttf", 26)
    except Exception:
        font = ImageFont.load_default()
    made = []
    for view in ("left", "right", "front", "square"):
        for when, d, s1 in (("day", day_dir, "shop-day"), ("night", night_dir, "shop-night")):
            leaf = "chandler-%s-%s.png" % (view, "shop" if when == "day" else "shopnight")
            panels = [("last good, 23 October", os.path.join(LAST_GOOD, leaf)),
                      ("after S1 (wear marks), today", os.path.join(AFTER_S1, s1, leaf)),
                      ("after S2 (paint over wood)", os.path.join(d, leaf))]
            if not all(os.path.exists(p) for _, p in panels):
                continue
            ims = [Image.open(p).convert("RGB") for _, p in panels]
            hh = 720
            ims = [im.resize((int(im.width * hh / im.height), hh), Image.LANCZOS) for im in ims]
            gap = 10
            sheet = Image.new("RGB", (sum(im.width for im in ims) + gap * (len(ims) - 1), hh), "white")
            x = 0
            dr = ImageDraw.Draw(sheet)
            for (label, _), im in zip(panels, ims):
                sheet.paste(im, (x, 0))
                tw = dr.textlength(label, font=font) if hasattr(dr, "textlength") else 300
                dr.rectangle([x, 0, x + tw + 16, 36], fill="black")
                dr.text((x + 8, 4), label, fill="white", font=font)
                x += im.width + gap
            path = os.path.join(out_dir, "chandler-%s-%s.jpg" % (view, when))
            sheet.save(path, quality=88)
            made.append(path)
    print("joinerySheets=%d out=%s" % (len(made), out_dir))
    return 0 if made else 1


def selftest():
    ok = []
    # the front's frame lands where the game stands it: its middle at street x 43, its wall face at 5.295, 0.1 up
    ok.append(np.allclose(to_unreal_cm([0.0, 0.0, 0.0]), [4300.0, 529.5, 10.0]))
    ok.append(np.allclose(to_unreal_cm([1.0, 2.0, 0.3]), [4200.0, 499.5, 210.0]))   # its right is street x 42, its out the road
    cam = (4300.0, 100.0, 150.0, 0.0, 90.0, 90.0)
    xy, dep = project_many(cam, np.array([[4300.0, 600.0, 150.0], [4200.0, 600.0, 150.0]]), 200, 100)
    one = cwc.stain_check.project(cam, (4200.0, 600.0, 150.0), 200, 100)
    ok.append(abs(xy[0, 0] - 100) < 1e-6 and abs(xy[1, 0] - one[0]) < 1e-6 and abs(xy[1, 1] - one[1]) < 1e-6)
    # a square in front of another: the nearer wins the depth test
    sq = lambda z, s: np.array([[[-s, -s, z], [s, -s, z], [s, s, z]], [[-s, -s, z], [s, s, z], [-s, s, z]]])  # noqa: E731
    model = np.concatenate([sq(0.0, 1.0), sq(0.5, 0.2)])
    world = to_unreal_cm(model)
    mid, pos = draw((4300.0, 200.0, 10.0, 0.0, 90.0, 60.0), world, model, np.array([0, 0, 1, 1]), 64, 64)
    ok.append(mid[32, 32] == 1 and mid[20, 32] == 0 and abs(pos[32, 32, 2] - 0.5) < 1e-6)
    # the measure: one pixel worn at an edge of a box paint, the rest unchanged
    h = w = 20
    bo = np.full((h, w, 3), 0.2)
    bw = bo.copy()
    bw[5, 5] = [0.55, 0.45, 0.35]
    midm = np.zeros((h, w), dtype=np.int32)
    posm = np.zeros((h, w, 3))
    posm[5, 5] = [0.01, 0.5, 0.0]
    r = measure(bw, bo, midm, posm, ["fascia"], [0], np.zeros((0, 3)), {0: (np.zeros(3), np.ones(3))}, np.zeros((0, 3)))
    ok.append(r["worn_px"] == 1 and r["within_5cm_share"] == 1.0 and r["paint_kept_ratio_median"] == 1.0)
    print("chandler_joinery_check selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if not a or "--selftest" in a:
        sys.exit(selftest())
    if a[0] == "buffers":
        sys.exit(run_buffers(a[1], a[2]))
    if a[0] == "sheets":
        sys.exit(sheets(a[1], a[2], a[3]))
    print(__doc__)
    sys.exit(2)
