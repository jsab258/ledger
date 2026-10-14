"""Try 2 checks of the first three shops (14 October 2026: the ironmonger, the newsagent and the tea rooms, after both fresh reviews of try 1; the brief's step 0). Rows that are the same for every shop built after Rita's;
Rita's own check (check_ritas.py) never calls this file, so her 60 of 61 stay as they were.

    FRN-13   the shop door's glass: 560 rays from each street camera's eye through it, none ends on a reveal slab, the sky or nothing (step 0 h)
    PIC-03s  the street frame at night_dark: no toplight strip brighter than the brick above the fascia (step 0 b)
    SIGN-01  the door's OPEN / CLOSED card in the gate frames follows the shop's hours (step 0 g)
    DSP-09   no display support carries a flat base-colour factor (the ironmonger's close review, narrow 1; the tea rooms')
    DSP-10   every cord, wire or chain of the display ends within 2 mm of a solid part (ironmonger close narrow 2)
    FLT-01   the largest uniform patch of the window in the day frames (the ironmonger's street review 5: the crate; 9 px, a standard deviation under 1)
    INV-07   the baked atlases (the images inside the glbs) show no maker's mark in the exact boxes of step 0 d
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage as _nd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import check_try2 as X  # noqa: E402
import sw_assets as A  # noqa: E402
import sw_gate as G  # noqa: E402


def luma(a):
    return X.luma(a)


# --------------------------------------------------------------------------------------------------------------------------------------------- the card under a frame pixel
def card_luma_map(ctx, R, cam, state, shape, res_full=(2560, 1440)):
    """For a frame of `shape` (h, w) from camera `cam`: the luma (0 to 255, at full brightness) of the card's baked picture (gate/card_<cam>_<state>.png) under each pixel, nan where the ray misses the card. The card
    is the plane y = the card's y in the front model, x -2.65 to 2.65, z 0.55 to 2.95 (sw_gate); the picture's pixel (i, j) is at x = -2.65 + (i + 0.5) / nw x 5.3, z = 2.95 - (j + 0.5) / nh x 2.4."""
    p = os.path.join(ctx.gate, "card_%s_%s.png" % (cam, state))
    if not os.path.exists(p):
        return None
    card = luma(np.asarray(Image.open(p).convert("RGB")).astype(np.float32))
    nh, nw = card.shape
    h, w = shape
    cp = X.cam_params(R, cam, (w, h))
    ys, xs = np.mgrid[0:h, 0:w]
    d = X.pixel_ray(cp, xs.ravel().astype(np.float64) + 0.5, ys.ravel().astype(np.float64) + 0.5)
    yc = ctx.ym(ctx.card_y)
    with np.errstate(divide="ignore", invalid="ignore"):
        t = (yc - cp["eye"][1]) / d[:, 1]
    x = cp["eye"][0] + t * d[:, 0]
    z = cp["eye"][2] + t * d[:, 2]
    i = np.floor((x + 2.65) / 5.3 * nw).astype(np.int64)
    j = np.floor((2.95 - z) / 2.4 * nh).astype(np.int64)
    ok = (t > 0) & (i >= 0) & (i < nw) & (j >= 0) & (j < nh)
    out = np.full(h * w, np.nan, np.float32)
    out[ok] = card[j[ok], i[ok]]
    return out.reshape(h, w)


# --------------------------------------------------------------------------------------------------------------------------------------------- FRN-13
def frn13_rows(ctx, R, assets, rows, members):
    """FRN-13 (the grocer's close review, the launderette's: a slab of the gate's floor stood in the recessed doorway and showed through the door's glass as a dark box; the brief's step 0 h and the coordinator's
    correction of the same day): 560 rays (40 across, 14 up) from each street camera's eye through the shop door's glass (the front's `door_glass_*` panes, 15 mm in from their edges). The scene is the gate's: the front's
    opaque parts, the gate's reveal slabs (sw_gate.reveal_specs, read from this front) and the card. Each ray must end on the card, on the front's hall or lobby floor, or on a part of the door (its stops, frame, bead or
    leaf); none may end on a reveal slab, on the sky (misses everything) or beyond the card."""
    import bpy
    from mathutils import Vector
    from mathutils.bvhtree import BVHTree
    glass = {k: v for k, v in members.items() if k.startswith("door_glass_")}
    if not glass:
        rows.na("FRN-13", "the shop door's glass shows the card and the floor, never a reveal", "this front has no shop door glass")
        return
    bvh, owner = X.front_bvh(X.front_glb(assets))
    front_objs = [o for o in bpy.data.objects if o.type == "MESH"]
    yc = ctx.ym(ctx.card_y)
    specs = G.reveal_specs(ctx, front_objs, yc)
    W_ = G.W
    boxes = [("reveal_l", -W_ / 2 - 0.012, -W_ / 2, 0.0, yc + 0.02, 0.0, 2.97), ("reveal_r", W_ / 2, W_ / 2 + 0.012, 0.0, yc + 0.02, 0.0, 2.97), ("reveal_top", -W_ / 2, W_ / 2, 0.0, yc + 0.02, 2.95, 2.97)] + list(specs)
    verts, polys, names = [], [], []
    for (nm, x0, x1, y0, y1, z0, z1) in boxes:
        off = len(verts)
        verts += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        for q in ((0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)):
            polys.append(tuple(off + k for k in q))
            names.append(nm)
    sl = BVHTree.FromPolygons(verts, polys, epsilon=0.0)
    ends = {}
    tot, bad = 0, {}
    per_cam = []
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        cp = X.cam_params(R, cam)
        n_cam, n_bad = 0, 0
        for gk, gv in glass.items():
            us = np.linspace(gv["u"][0] + 15, gv["u"][1] - 15, 40)
            zs = np.linspace(gv["z"][0] + 15, gv["z"][1] - 15, 14)
            dmid = -(gv["d"][0] + gv["d"][1]) / 2000.0
            for u in us:
                for z in zs:
                    p = np.array([(u - 3000.0) / 1000.0, dmid, z / 1000.0])
                    dd = p - cp["eye"]
                    dd /= np.linalg.norm(dd)
                    o = tuple(p + dd * 0.002)
                    h1 = bvh.ray_cast(o, tuple(dd))
                    h2 = sl.ray_cast(o, tuple(dd))
                    d1 = h1[3] if h1[0] is not None else 1e9
                    d2 = h2[3] if h2[0] is not None else 1e9
                    n_cam += 1
                    if d1 <= d2 and h1[0] is not None:
                        what = owner[h1[2]]
                        kind = "floor" if what.startswith(("hall_floor", "lobby_floor", "door_hall_floor")) else "front"
                    elif h2[0] is not None:
                        what = names[h2[2]]
                        kind = "bad"
                    else:
                        # on to the card: the plane y = yc
                        t = (yc - o[1]) / dd[1] if abs(dd[1]) > 1e-9 else -1
                        xx, zz = o[0] + t * dd[0], o[2] + t * dd[2]
                        if t > 0 and -W_ / 2 <= xx <= W_ / 2 and 0.55 <= zz <= 2.95:
                            what, kind = "card", "card"
                        else:
                            what, kind = "nothing (sky or beyond the card)", "bad"
                    ends[what] = ends.get(what, 0) + 1
                    if kind == "bad":
                        n_bad += 1
                        bad[what] = bad.get(what, 0) + 1
        tot += n_cam
        per_cam.append("%s %d of %d on the reveal or nothing" % (cam, n_bad, n_cam))
    rows.add("FRN-13", "the shop door's glass shows the card and the floor, never a reveal", tot > 0 and not bad,
             "%d rays (40 x 14 over each of the %d door panes, 15 mm in) from the four review cameras through the shop door's glass into the gate's scene (the front's opaque parts, the gate's reveal slabs %s, the card): %s; where they end: %s; none may end on a reveal slab, the sky or beyond the card (try 1: the grocer's and the launderette's door-zone slab stood 60 mm in front of the door leaf and read as a dark box through the glass)" % (
                 tot, len(glass), [s_[0] + " y %.3f" % s_[3] for s_ in specs], "; ".join(per_cam), ", ".join("%s %d" % kv for kv in sorted(ends.items(), key=lambda kv: -kv[1])[:8])))


# --------------------------------------------------------------------------------------------------------------------------------------------- PIC-03 street clause
def pic03_toplight_text(ctx, R, members):
    """(ok, text) for PIC-03's second clause: in the STREET_SQUARE night_dark gate frame no toplight strip (the window's `win_glass_top_*` lights) has a mean luma above the brick above the fascia (the wall above the
    cornice, the same width as the window, 0.25 m high)."""
    p = os.path.join(ctx.gate, "STREET_SQUARE_night_dark.png")
    if not os.path.exists(p):
        return (ctx.lit, "the STREET_SQUARE night_dark frame was not rendered" + ("" if ctx.lit else " (a dark shop's real night: owed)"))
    im = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
    lum = luma(im)
    h, w = lum.shape
    cp = X.cam_params(R, "STREET_SQUARE", (w, h))
    tops = sorted(k for k in members if k.startswith("win_glass_top_"))
    if not tops:
        return (True, "no toplight strips")
    cor = members.get("cor_cornice")
    z_c = (cor["z"][1] / 1000.0 + 0.05) if cor else 3.60
    u0 = min(members[k]["u"][0] for k in tops)
    u1 = max(members[k]["u"][1] for k in tops)

    def rect_mean(ua, ub, za, zb, d_m, shrink=8):
        pts = np.array([[(u - 3000.0) / 1000.0, -d_m, z] for u in (ua, ub) for z in (za, zb)])
        x, y, zc = X.project_np(cp, pts)
        xa, xb = int(max(0, x.min() + shrink)), int(min(w, x.max() - shrink))
        ya, yb = int(max(0, y.min() + shrink)), int(min(h, y.max() - shrink))
        if xb <= xa or yb <= ya:
            return None
        return float(lum[ya:yb, xa:xb].mean())
    brick = rect_mean(u0 + 200, u1 - 200, z_c, z_c + 0.25, 0.0)
    vals = []
    for k in tops:
        m_ = members[k]
        v = rect_mean(m_["u"][0], m_["u"][1], m_["z"][0] / 1000.0, m_["z"][1] / 1000.0, (m_["d"][0] + m_["d"][1]) / 2000.0)
        if v is not None:
            vals.append((k, v))
    if brick is None or not vals:
        return (False, "the strips or the brick could not be projected")
    worst = max(v for _, v in vals)
    ok = worst <= brick
    return (ok, "in the STREET_SQUARE night_dark frame the toplight strips read %s against the brick above the fascia %.1f (none above it: the strongest %.1f; the pre-fix frame: the first toplight's end 75.1 and the sixth's 90.7 against the brick 26.4)" % (
        ", ".join("%.1f" % v for _, v in vals), brick, worst))


# --------------------------------------------------------------------------------------------------------------------------------------------- SIGN-01
def sign01_rows(ctx, rows):
    """SIGN-01 (the brief's step 0 g; the tea rooms' street review N1): the door's OPEN / CLOSED card in each gate frame's camera file (`door_sign`) follows the shop's hours: by day OPEN; at night_lit OPEN where
    the shop's hours run past the night hour (20:00: the tea rooms to 22:00), CLOSED where they do not (the newsagent's 17:30, the ironmonger's); at night_dark CLOSED for every shop."""
    det, ok, n = [], True, 0
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        for st in ("day", "night_lit", "night_dark"):
            pj = os.path.join(ctx.gate, "%s_%s.camera.json" % (cam, st))
            if not os.path.exists(pj):
                continue
            rec = json.load(open(pj))
            got = rec.get("door_sign")
            want = "OPEN" if st == "day" else ("CLOSED" if (st == "night_dark" or not ctx.open_at_night) else "OPEN")
            n += 1
            if got != want:
                ok = False
                det.append("%s %s reads %s, wants %s" % (cam, st, got, want))
    rows.add("SIGN-01", "the door's sign follows the shop's hours", ok and n > 0,
             "%d gate frames' camera files: the sign by day OPEN; at night_lit %s (the shop's last closing hour %.1f, the night hour %.0f); at night_dark CLOSED%s" % (
                 n, "OPEN (it is open at night)" if ctx.open_at_night else "CLOSED (it is shut at night)", ctx.close_hour, 20.0, ("; WRONG: " + "; ".join(det)) if det else "; all as wanted"))


# --------------------------------------------------------------------------------------------------------------------------------------------- DSP-09, DSP-10
def _glb_materials_of_nodes(path):
    """{node name: [(material name, has a base-colour picture)]} from the glb's JSON."""
    g, raw, off = X.glb_json(path)
    out = {}
    for n in g.get("nodes", []):
        if "mesh" not in n:
            continue
        ms = []
        for pr in g["meshes"][n["mesh"]]["primitives"]:
            m = g["materials"][pr["material"]] if "material" in pr else {}
            ms.append((m.get("name", "?"), "baseColorTexture" in m.get("pbrMetallicRoughness", {})))
        out[n.get("name", "")] = ms
    return out


def dsp09_rows(ctx, assets, rows, di):
    """DSP-09 (the ironmonger's close review, narrow 1; Rita's try 1 narrow 6, repeated): no display support carries a flat base-colour factor. Every mesh of a `support` group (the crates, trays, shelves, boards and the
    bed) and the bed's own parts must have a base-colour PICTURE in the glb (a painted plywood, a plank map): a colour factor alone reads as a CG panel. The return walls take the room's plaster in the gate; cords, rods
    and stakes are wire, not supports."""
    mats = _glb_materials_of_nodes(X.display_glb(assets))
    by_name = {}
    for gi, g in enumerate(di["groups"]):
        if g["kind"] == "support":
            for nm in g["objs"]:
                by_name[nm] = g["model"]
    for st in di.get("structure", []):
        if st["kind"] in ("bed", "bed_top"):
            by_name[st["obj"]] = "script:" + st["kind"]
    flat, n = [], 0
    for nm, mdl in by_name.items():
        ms = mats.get(nm)
        if not ms:
            continue
        if mdl in ("script:hang_rod",):
            continue
        n += 1
        if not all(has for _, has in ms):
            flat.append("%s(%s: %s)" % (mdl, nm, ", ".join(m_ for m_, has in ms if not has)))
    rows.add("DSP-09", "every display support has a picture", not flat and n > 0, "%d support meshes (crates, trays, shelves, boards, the bed and its top) read from the glb: each carries a base-colour picture%s (a flat factor reads as a CG panel: the ironmonger's crate was 85,931 px at sd under 1.5 at CLOSE_35_B)" % (n, ("; FLAT: " + "; ".join(flat[:8])) if flat else ""))


def dsp10_rows(ctx, assets, rows, di):
    """DSP-10 (the ironmonger's close review, narrow 2: the glove shelf's four cords ended in mid-air): every cord, wire or chain of the display (the parts the layout names kind `cords`) ends within 2 mm of a solid
    part. Each rod of the mesh (a connected piece) gives its two end centres (the extremes along its own axis); each must be inside or within 2 mm of another mesh of the display."""
    import bpy
    from mathutils.bvhtree import BVHTree
    from scipy.sparse import coo_matrix
    from scipy.sparse.csgraph import connected_components
    cords = [s_["obj"] for s_ in di.get("structure", []) if s_["kind"] == "cords"]
    if not cords:
        rows.na("DSP-10", "every cord ends on something", "this display has no cords")
        return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = X.load_glb_objects(X.display_glb(assets))
    deps = bpy.context.evaluated_depsgraph_get()
    data = {}
    for ob in objs:
        if ob.type != "MESH":
            continue
        V, T_, N = X.mesh_world(ob, deps)
        if len(V) and len(T_):
            data[ob.name] = (V, T_, BVHTree.FromPolygons(V.tolist(), T_.tolist(), epsilon=0.0))
    ends, loose = 0, []
    for nm in cords:
        if nm not in data:
            continue
        V, T_, _ = data[nm]
        n = len(V)
        a = np.concatenate([T_[:, 0], T_[:, 1], T_[:, 2]])
        b = np.concatenate([T_[:, 1], T_[:, 2], T_[:, 0]])
        g_ = coo_matrix((np.ones(len(a)), (a, b)), shape=(n, n))
        nc, lab = connected_components(g_, directed=False)
        for c in range(nc):
            P = V[lab == c]
            if len(P) < 4:
                continue
            ctr = P.mean(axis=0)
            w_, vec = np.linalg.eigh(np.cov((P - ctr).T))
            ax = vec[:, -1]
            t = (P - ctr) @ ax
            for tv in (t.min(), t.max()):
                e = ctr + ax * tv * 0.999
                best = 1e9
                for nm2, (V2, T2, bv2) in data.items():
                    if nm2 == nm:
                        continue
                    hit = bv2.find_nearest(tuple(e))
                    if hit[0] is not None:
                        best = min(best, hit[3])
                    # inside a closed mesh: a ray count along +z is odd
                    cnt, o_, d_ = 0, tuple(e), (0.0, 0.0, 1.0)
                    while True:
                        h_ = bv2.ray_cast(o_, d_)
                        if h_[0] is None:
                            break
                        cnt += 1
                        o_ = (h_[0][0], h_[0][1], h_[0][2] + 1e-5)
                    if cnt % 2 == 1:
                        best = 0.0
                ends += 1
                if best > 0.002:
                    loose.append("%s end at (%.3f, %.3f, %.3f) is %.1f mm from the nearest part" % (nm, e[0], e[1], e[2], best * 1000.0))
    rows.add("DSP-10", "every cord ends on something", ends > 0 and not loose, "%d cord ends (%d rods in %d meshes): each inside or within 2 mm of another part of the display (the rod under the transom, the shelf's top)%s" % (ends, ends // 2, len(cords), ("; LOOSE: " + "; ".join(loose[:6])) if loose else ""))


# --------------------------------------------------------------------------------------------------------------------------------------------- FLT-01
FLAT_LIMIT = {"ironmonger": 0.01, "newsagent": 0.03, "tea_rooms": 0.025}


def flt01_rows(ctx, rows):
    """FLT-01 (the ironmonger's street review, narrow 5: the crate was the window's largest flat tone, 2.2 per cent of the glass at STREET_SQUARE, with the return wall's 2.6 per cent at STREET_30): in the day gate frames
    (2560 x 1440) over the window's glass (the check's glass mask), the pixels whose 9 x 9 neighbourhood has a luma standard deviation under 1; the largest connected patch of them, as a share of the glass. Limits: the
    ironmonger 1 per cent (the review's), the newsagent 3, the tea rooms 2.5 (the dado)."""
    lim = FLAT_LIMIT.get(ctx.id, 0.03)
    det, ok, n = [], True, 0
    for cam in ("STREET_SQUARE", "STREET_30"):
        pf = os.path.join(ctx.gate, "%s_day.png" % cam)
        pm = os.path.join(ctx.gate, "check_%s_day_mask.png" % cam)
        if not (os.path.exists(pf) and os.path.exists(pm)):
            ok = False
            continue
        im = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
        mk = np.asarray(Image.open(pm).convert("L").resize((im.shape[1], im.shape[0]), Image.NEAREST)) > 128
        mk = _nd.binary_erosion(mk, iterations=3)
        m1 = _nd.uniform_filter(im, 9)
        m2 = _nd.uniform_filter(im * im, 9)
        sd = np.sqrt(np.maximum(m2 - m1 * m1, 0.0))
        flat = (sd < 1.0) & mk
        lab, nl = _nd.label(flat)
        sizes = np.bincount(lab.ravel())[1:] if nl else np.array([0])
        big = int(sizes.max()) if nl else 0
        share = big / float(max(int(mk.sum()), 1))
        ys, xs = np.nonzero(lab == (int(np.argmax(sizes)) + 1)) if nl else (np.array([0]), np.array([0]))
        mean_l = float(im[lab == (int(np.argmax(sizes)) + 1)].mean()) if nl else 0.0
        n += 1
        ok &= share <= lim
        det.append("%s: largest uniform patch %d px = %.2f per cent of %d glass px (x %d to %d, y %d to %d, luma %.0f)" % (cam, big, 100.0 * share, int(mk.sum()), xs.min(), xs.max(), ys.min(), ys.max(), mean_l))
    rows.add("FLT-01", "no large flat tone in the window", ok and n == 2, "day frames, 9 x 9 px standard deviation under 1, the largest connected patch over the glass: " + "; ".join(det) + " (limit %.1f per cent for this shop)" % (100.0 * lim))


# --------------------------------------------------------------------------------------------------------------------------------------------- INV-07
def inv07_rows(ctx, assets, rows, di):
    """INV-07 (the ironmonger's close review, fault 3; the brief's step 0 d: a maker's mark survived blanking in the glb: the tyre pump's roundel, the trowels' stamped word): the blanking boxes of every placed model
    are read in the pictures the build USES, not the source maps: (a) the images inside the display glb (the baked atlases: `<model>_diff_1k_clean`, JPEG at q 85), (b) the maps the room loads (the model's clean glTF
    points at `<map>_clean.jpg`, which is opened here). In each box (1k pixel boxes of target.json and the kit's extra boxes, scaled to the image) the luma's standard deviation must be at most 1.6 times that of the ring
    10 px round it plus 5 (a printed mark is a few dozen levels of contrast on a plain ground; the ring carries the ground's own grain)."""
    import io
    T = A.load_target()
    A.set_shop(ctx.id)
    placed = json.load(open(os.path.join(ctx.rooms, "placed.json"))) if ctx.has_room and os.path.exists(os.path.join(ctx.rooms, "placed.json")) else []
    models = sorted({str(p["model"]).split("#")[0] for p in placed if "model" in p and not str(p["model"]).startswith("script:")} | {str(i["model"]).split("#")[0] for i in (di or {}).get("items", [])})
    glb_imgs = {}
    dp = X.display_glb(assets)
    if ctx.has_room and os.path.exists(dp):
        g, raw, off = X.glb_json(dp)
        for k, im in enumerate(g["images"]):
            glb_imgs[im.get("name", "")] = k
    bad, n_box, n_img, lines = [], 0, 0, []
    for m in models:
        for e in A.entries(T, m) if m in T["inventory"]["polyhaven"] else []:
            mp = e["map"]
            if "_diff_" not in mp:
                continue
            boxes = [b for b in e["boxes"] if b != [0, 0, 1024, 1024]]
            if not boxes:
                continue
            srcs = []
            stem = os.path.splitext(mp)[0] + "_clean"
            if stem in glb_imgs:
                srcs.append(("glb", Image.open(io.BytesIO(X.glb_image_bytes(dp, glb_imgs[stem]))).convert("L")))
            try:
                gj = json.load(open(A.gltf_path(m), encoding="utf-8"))
                uri = next((i_["uri"] for i_ in gj["images"] if os.path.basename(i_["uri"]).startswith(os.path.splitext(mp)[0])), None)
                if uri and uri.endswith("_clean.jpg"):
                    srcs.append(("room map", Image.open(os.path.join(A.POLY, m, "1k", uri)).convert("L")))
                else:
                    bad.append("%s: the room's glTF still points at %s" % (m, uri))
            except Exception as ex_:                                  # noqa: BLE001
                bad.append("%s: %s" % (m, ex_))
            for kind, im in srcs:
                n_img += 1
                a = np.asarray(im).astype(np.float32)
                s_ = a.shape[1] / 1024.0
                for (x0, y0, x1, y1) in boxes:
                    X0, Y0, X1, Y1 = int(x0 * s_), int(y0 * s_), int(x1 * s_), int(y1 * s_)
                    if X1 - X0 < 2 or Y1 - Y0 < 2:
                        continue
                    reg = a[Y0:Y1, X0:X1]
                    pad = max(4, int(10 * s_))
                    outer = a[max(0, Y0 - pad):Y1 + pad, max(0, X0 - pad):X1 + pad].copy()
                    mask = np.ones(outer.shape, bool)
                    ya, xa = Y0 - max(0, Y0 - pad), X0 - max(0, X0 - pad)
                    mask[ya:ya + (Y1 - Y0), xa:xa + (X1 - X0)] = False
                    ring = outer[mask]
                    sd_in, sd_ring = float(reg.std()), float(ring.std())
                    n_box += 1
                    if sd_in > 1.6 * sd_ring + 5.0:
                        bad.append("%s %s box %s: sd %.1f in the box against %.1f in its ring" % (m, kind, [x0, y0, x1, y1], sd_in, sd_ring))
    rows.add("INV-07", "no maker's mark in the pictures the build uses", n_box > 0 and not bad,
             "%d blanking boxes of %d placed models read in %d pictures actually used (the display glb's own images and the room's clean maps): in each box the luma's standard deviation is at most 1.6 times its ring's plus 5%s (the pump's roundel, the trowels' stamped word, the till's glyph and the clock's dash were found at 100 per cent by the close review; INV-06 reads the source maps)" % (
                 n_box, len(models), n_img, ("; STILL MARKED: " + "; ".join(bad[:8])) if bad else "; none marked"))


# --------------------------------------------------------------------------------------------------------------------------------------------- DSP-11
def dsp11_rows(ctx, rows, di):
    """DSP-11 (the ironmonger's street review, narrow 4: the pyramid's backing board was primer grey, luma 86 to 111, the palest flat field in the left light): the board's VISIBLE pixels (the object-index render of the
    display from STREET_SQUARE, the front's bars and the goods in front of it drawn black) read luma 25 to 45 in the day gate frame, so the tins' coloured labels stand out against it."""
    gi = next((i for i, g in enumerate(di["groups"]) if g["model"] == "script:backing_board"), None)
    if gi is None:
        rows.na("DSP-11", "the backing board is dark", "this display has no backing board")
        return
    pi = os.path.join(ctx.gate, "check_STREET_SQUARE_object_index.png")
    pf = os.path.join(ctx.gate, "STREET_SQUARE_day.png")
    if not (os.path.exists(pi) and os.path.exists(pf)):
        rows.add("DSP-11", "the backing board is dark", False, "the object-index render or the day frame is missing")
        return
    idx = np.asarray(Image.open(pi).convert("RGB")).astype(np.float32) / 255.0
    fr = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
    c = np.array(((gi + 1) % 17 / 17.0 + 0.03, ((gi + 1) // 17) % 17 / 17.0 + 0.03, ((gi + 1) // 289) % 17 / 17.0 + 0.03))
    mk = np.abs(idx - c[None, None, :]).max(axis=2) < 0.02
    mk = np.asarray(Image.fromarray((mk * 255).astype(np.uint8)).resize((fr.shape[1], fr.shape[0]), Image.NEAREST)) > 128
    mk = _nd.binary_erosion(mk, iterations=3)
    n = int(mk.sum())
    if n < 200:
        rows.add("DSP-11", "the backing board is dark", False, "only %d visible pixels of the backing board at STREET_SQUARE" % n)
        return
    v = fr[mk]
    rows.add("DSP-11", "the backing board is dark", 25.0 <= float(v.mean()) <= 45.0,
             "the pyramid's backing board, %d visible pixels (an object-index render from STREET_SQUARE, eroded 3 px) in the day gate frame: mean luma %.1f (p5 %.1f, p95 %.1f); wanted 25 to 45 (try 1: 86 to 111, primer grey)" % (n, float(v.mean()), float(np.percentile(v, 5)), float(np.percentile(v, 95))))
