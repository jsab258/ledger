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
    gj, _, _ = X.glb_json(X.display_glb(assets))
    metal = {m_.get("name", ""): m_.get("pbrMetallicRoughness", {}).get("metallicFactor", 1.0) for m_ in gj.get("materials", [])}   # (glTF: an absent factor is 1.0)
    transm = {m_.get("name", "") for m_ in gj.get("materials", []) if "KHR_materials_transmission" in (m_.get("extensions") or {})}
    PLAIN = ("china", "cast_black", "suction_pvc", "stake")          # a glazed plate, a black cast base, a clear PVC disc: one colour by nature, not a board that reads as a CG panel
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
        flat_ms = [m_ for m_, has in ms if not has and metal.get(m_, 0.0) < 0.5 and m_ not in transm and m_ not in PLAIN]       # metal, glass and a plain glaze are one colour by nature (the rule is for boards and timber)
        if flat_ms:
            flat.append("%s(%s: %s)" % (mdl, nm, ", ".join(flat_ms)))
    rows.add("DSP-09", "every display support has a picture", not flat and n > 0, "%d support meshes (crates, trays, shelves, boards, the bed and its top) read from the glb: each carries a base-colour picture%s, except metal, glass and plain china, black cast and clear plastic, which are one colour by nature (a flat factor on a board reads as a CG panel: the ironmonger's crate was 85,931 px at sd under 1.5 at CLOSE_35_B)" % (n, ("; FLAT: " + "; ".join(flat[:8])) if flat else ""))


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
        Vu, inv = np.unique(np.round(V, 5), axis=0, return_inverse=True)           # the exported mesh has its own vertices a face (flat shading): weld them, so a cord is one piece again
        V, T_ = Vu, inv.reshape(-1)[T_]
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
    """FLT-01 and FLT-02 (the ironmonger's street review, narrow 5: the crate was the window's largest flat tone, 2.2 per cent of the glass at STREET_SQUARE; the newsagent's street review, narrow 3: the stockroom
    door was 6.7 per cent; the tea rooms' narrow 4: the dado): in the day gate frames (2560 x 1440) over the window's glass (the check's glass mask), the pixels whose 9 x 9 neighbourhood has a luma standard
    deviation under 1; the largest connected patch of them as a share of the glass. 15 Oct (the ironmonger's try 2 street review, narrow 6): the row is split by what the check's mask_room render shows there. FLT-01
    counts the DISPLAY'S OWN PIECES only (the supports and goods the build makes; limit 1 per cent of the glass at each street camera); FLT-02 counts the whole glass, the room's picture and the return walls too
    (the review's wording over the whole glass: the newsagent 3 per cent, the tea rooms 2.5 (the dado), the ironmonger 3), and names what shows there, so a room panel in shade is seen apart from a flat display piece."""
    lim_room = FLAT_LIMIT.get(ctx.id, 0.03)
    if ctx.id == "ironmonger":
        lim_room = 0.03
    lim_disp = 0.01
    det_d, det_a, ok_d, ok_a, n = [], [], True, True, 0
    for cam in ("STREET_SQUARE", "STREET_30"):
        pf = os.path.join(ctx.gate, "%s_day.png" % cam)
        pm = os.path.join(ctx.gate, "check_%s_day_mask.png" % cam)
        pr = os.path.join(ctx.gate, "check_%s_day_room.png" % cam)
        if not (os.path.exists(pf) and os.path.exists(pm) and os.path.exists(pr)):
            ok_d = ok_a = False
            continue
        im = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
        mk = np.asarray(Image.open(pm).convert("L").resize((im.shape[1], im.shape[0]), Image.NEAREST)) > 128
        mk = _nd.binary_erosion(mk, iterations=3)
        rm = np.asarray(Image.open(pr).convert("RGB").resize((im.shape[1], im.shape[0]), Image.NEAREST)).astype(int)
        blue = (rm[..., 2] > 128) & (rm[..., 0] < 128)
        red = (rm[..., 0] > 128) & (rm[..., 2] < 128)
        m1 = _nd.uniform_filter(im, 9)
        m2 = _nd.uniform_filter(im * im, 9)
        sd = np.sqrt(np.maximum(m2 - m1 * m1, 0.0))
        flat = (sd < 1.0) & mk
        gl = float(max(int(mk.sum()), 1))

        def biggest(sel):
            lab, nl = _nd.label(sel)
            if not nl:
                return 0.0, (0, 0, 0, 0), 0.0
            sizes = np.bincount(lab.ravel())[1:]
            k = int(np.argmax(sizes)) + 1
            ys, xs = np.nonzero(lab == k)
            return sizes.max() / gl, (int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())), float(im[lab == k].mean())
        sh_all, bb_all, l_all = biggest(flat)
        sh_d, bb_d, l_d = biggest(flat & blue)
        sh_r, bb_r, l_r = biggest(flat & red)
        n += 1
        ok_d &= sh_d <= lim_disp
        ok_a &= sh_all <= lim_room
        det_d.append("%s: the display's pieces' largest uniform patch %.2f per cent of %d glass px (x %d to %d, y %d to %d, luma %.0f)" % ((cam, 100 * sh_d, int(gl)) + bb_d + (l_d,)))
        det_a.append("%s: the largest uniform patch of all %.2f per cent of %d glass px (x %d to %d, y %d to %d, luma %.0f); of it the room's picture and return walls %.2f, the display's pieces %.2f" % ((cam, 100 * sh_all, int(gl)) + bb_all + (l_all, 100 * sh_r, 100 * sh_d)))
    rows.add("FLT-01", "no large flat tone in the display", ok_d and n == 2, "day frames, 9 x 9 px standard deviation under 1, the largest connected patch among the DISPLAY'S OWN PIECES (the check's mask_room render): " + "; ".join(det_d) + " (limit 1.0 per cent of the glass; the ironmonger's street review, try 2 narrow 6: the row counts the display, the room's flat tones are FLT-02 and PIC-06)")
    rows.add("FLT-02", "no large flat tone in the window's room", ok_a and n == 2, "day frames, the same test over the whole glass, the room's picture and the return walls included: " + "; ".join(det_a) + " (limit %.1f per cent for this shop: the review's)" % (100 * lim_room))


# --------------------------------------------------------------------------------------------------------------------------------------------- INV-07
def inv08_rows(ctx, assets, rows, di):
    """INV-08 (the ironmonger's try 2 close review, narrow 1, content rule: "Polybubble" with a registered-mark sign survived twice on the sprinkler's top, outside every blanking box, and INV-05 to INV-07 read only the
    boxes): a SECOND READER over every placed model's base-colour map as the build uses it (the clean map where there is one): a text reader (`ocr_words.py`, run under the OCR venv: a tool of the check, nothing of it is
    shipped) reads each map three ways (as it is, at twice the size with the contrast stretched, with the local contrast lifted: that is what shows a moulded word), and every line it finds with three letters or more at
    a confidence of 0.5 or over is a legible word left on a model. The row fails on any word not on the project's own list (`checks/ocr_word_list.json`: each entry says which model, where and why it is not a maker's
    or a brand's: a generic instruction or a material, read at 100 per cent by a person). The results are cached by file size and time in the shop's work folder."""
    import re
    import subprocess
    placed = json.load(open(os.path.join(ctx.rooms, "placed.json"))) if ctx.has_room and os.path.exists(os.path.join(ctx.rooms, "placed.json")) else []
    models = sorted({str(p["model"]).split("#")[0] for p in placed if "model" in p and not str(p["model"]).startswith("script:")} | {str(i["model"]).split("#")[0] for i in (di or {}).get("items", [])})
    A.set_shop(ctx.id)
    paths = []
    for m in models:
        folder = os.path.join(A.POLY, m, A.RES)
        try:
            rels = A.base_maps(m)
        except Exception:  # noqa: BLE001
            continue
        for rel in rels:
            c = os.path.join(folder, os.path.dirname(rel), os.path.splitext(os.path.basename(rel))[0] + "_clean.jpg")
            paths.append((m, c if os.path.exists(c) else os.path.join(folder, rel)))
    py = "/home/user/.ocrenv/bin/python"
    if not os.path.exists(py):
        rows.add("INV-08", "someone else reads every map", False, "the second reader is not installed (%s: rapidocr-onnxruntime)" % py)
        return
    cache_p = os.path.join(ctx.work, "ocr_cache.json")
    cache = json.load(open(cache_p)) if os.path.exists(cache_p) else {}
    todo = [p for _, p in paths if cache.get(p, {}).get("sig") != [os.path.getsize(p), int(os.path.getmtime(p))]]
    if todo:
        tmp = os.path.join(ctx.work, "ocr_out.json")
        env = dict(os.environ, OMP_NUM_THREADS="2")
        subprocess.run(["nice", "-n", "15", py, os.path.join(os.path.dirname(os.path.abspath(__file__)), "ocr_words.py"), tmp] + todo, check=True, env=env)
        out = json.load(open(tmp))
        for p_, found in out.items():
            cache[p_] = {"sig": [os.path.getsize(p_), int(os.path.getmtime(p_))], "found": found}
        json.dump(cache, open(cache_p, "w"))
    allow = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "checks", "ocr_word_list.json")))["allowed"]
    ok_words = {re.sub(r"[^A-Z0-9]", "", a["words"].upper()) for a in allow}
    bad, seen = [], 0
    for m, p_ in paths:
        for f in cache[p_]["found"]:
            if f["conf"] >= 0.5 and len(re.findall(r"[A-Za-z]", f["text"])) >= 3:
                seen += 1
                if re.sub(r"[^A-Z0-9]", "", f["text"].upper()) not in ok_words:
                    bad.append("%s %s %r conf %.2f at %s" % (m, os.path.basename(p_), f["text"], f["conf"], f["box"]))
    rows.add("INV-08", "someone else reads every map", not bad,
             "%d base-colour maps of %d placed models read by the second reader (three readings each): %d legible lines in all, %d of them on the project's word list (%s); not on the list: %s" % (
                 len(paths), len(models), seen, seen - len(bad), "; ".join(sorted({a["words"] for a in allow})) or "none", ("; ".join(bad[:12]) + (" ..." if len(bad) > 12 else "")) if bad else "none"))


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


# --------------------------------------------------------------------------------------------------------------------------------------------- PRT-01 to PRT-04 (the printed goods)
ATLAS_GRID = {"magazines": (6, 4), "papers": (2, 4), "cards": (5, 2), "postcards": (3, 4), "cartons": (2, 9), "jar_labels": (2, 5)}


def _prints_json(ctx):
    out = {}
    for p in (os.path.join(ctx.work, "display_work", "prints_used.json"), os.path.join(ctx.rooms, "prints_used_room.json"), os.path.join(ctx.work, "rooms_scene", "prints_used_room.json")):
        if os.path.exists(p):
            j = json.load(open(p))
            for k, v in j.get("used", {}).items():
                out[k] = v
            out.setdefault("__fit__", {}).update(j.get("fit", {}))
            out.setdefault("__head__", {}).update(j.get("headlines", {}))
            out.setdefault("__post__", {}).update(j.get("postcards", {}))
            out.setdefault("__subj__", {}).update(j.get("subjects", {}))
    return out


def prt_rows(ctx, rows):
    """PRT-01 to PRT-04 (the newsagent's close review, fault 2; the brief's step 0 i): the printed goods are made from photographs and script, not repeated vector clip-art.
    PRT-01 no two covers (magazines, newspapers, greetings cards, postcards of one kind) share a picture;
    PRT-02 no printed good's flat tone is more than 40 per cent of its area (each tile of each atlas: the pixels whose 7 x 7 neighbourhood has a luma standard deviation under 1.5);
    PRT-03 the postcards' captions name what their photographs show (the photograph's own words, `sw_prints.PHOTOS`, are in the caption);
    PRT-04 each newspaper's headline is drawn whole: the lines the generator set, joined, are the headline (no word lost to the edge: the close review's 'RAIN FORECAST FOR THE ...')."""
    pj = _prints_json(ctx)
    used = {k: v for k, v in pj.items() if not k.startswith("__")}
    kinds = {}
    for k, v in used.items():
        kinds.setdefault(k.split(":")[0], []).append((k, v))
    dup = []
    for kd, lst in kinds.items():
        seen = {}
        for k, v in lst:
            if v in seen:
                dup.append("%s and %s: %s" % (seen[v], k, v))
            seen[v] = k
    n_pic = len(set(used.values()))
    rows.add("PRT-01", "no two covers share a picture", bool(used) and not dup,
             "%d printed goods (%s), %d distinct photographs (crops of Poly Haven's CC0 HDRIs, tone-mapped, no person): within each kind no two share one%s" % (len(used), ", ".join("%d %s" % (len(v), k) for k, v in sorted(kinds.items())), n_pic, ("; SHARED: " + "; ".join(dup[:6])) if dup else ""))
    det, ok, n = [], True, 0
    for tex_dir in (os.path.join(ctx.work, "display_work", "tex"), os.path.join(ctx.work, "rooms_scene", "tex")):
        if not os.path.isdir(tex_dir):
            continue
        for nm, (cols, rws) in ATLAS_GRID.items():
            p = os.path.join(tex_dir, nm + ".png")
            if not os.path.exists(p):
                continue
            a = luma(np.asarray(Image.open(p).convert("RGB")).astype(np.float32))
            h, w = a.shape
            tw, th = w // cols, h // rws
            worst = 0.0
            for r_ in range(rws):
                for c_ in range(cols):
                    t = a[r_ * th:(r_ + 1) * th, c_ * tw:(c_ + 1) * tw]
                    if nm == "cartons":
                        # 15 Oct: tiles 0..5 are the fronts, 6..11 the tops (the tile's top 560 x 100 px are the face), 12..17 the ends (its top-left 180 x 100 px): only the face that is printed is tested
                        k_ = r_ * cols + c_
                        if k_ >= 12:
                            t = t[:100, :180]
                        elif k_ >= 6:
                            t = t[:100, :]
                    m1 = _nd.uniform_filter(t, 7)
                    m2 = _nd.uniform_filter(t * t, 7)
                    sd = np.sqrt(np.maximum(m2 - m1 * m1, 0.0))
                    worst = max(worst, float((sd < 1.5).mean()))
            n += 1
            ok &= worst <= 0.40
            det.append("%s/%s %.2f" % (os.path.basename(os.path.dirname(tex_dir)).replace("_work", ""), nm, worst))
    rows.add("PRT-02", "no printed good is mostly a flat tone", ok and n > 0, "each tile of %d atlases: the largest share of flat pixels (7 x 7 luma sd under 1.5) in any tile: %s (limit 0.40; try 1's eight flat pictures)" % (n, ", ".join(det)))
    post, subj = pj.get("__post__", {}), pj.get("__subj__", {})
    bad = []
    for cap, pid in post.items():
        sw = subj.get(pid, "")
        if sw and sw.lower() not in cap.lower():
            bad.append("'%s' over %s (%s)" % (cap, pid, sw))
    rows.add("PRT-03", "the postcards' captions match their photographs", bool(post) and not bad, "%d postcards: each caption holds the words of what its photograph shows%s (try 1: THE HARBOUR AT DUSK was a bed of flowers in daylight, MERIDIAN FROM THE HILL a duck)" % (len(post), ("; MISMATCH: " + "; ".join(bad)) if bad else ""))
    fit, head = pj.get("__fit__", {}), pj.get("__head__", {})
    bad = [nm for nm, ls in fit.items() if " ".join(ls) != head.get(nm)]
    rows.add("PRT-04", "the headlines are whole", bool(fit) and not bad, "%d newspapers: the headline's lines as set, joined, are the headline%s (try 1: RAIN FORECAST FOR THE ... and NEW LIBRARY OPENS ON ... lost their last word)" % (len(fit), ("; CUT: " + "; ".join(bad)) if bad else ""))


# --------------------------------------------------------------------------------------------------------------------------------------------- CUR-01 (the tea rooms' curtains)
def _index_mask(ctx, cam, gi, shape):
    pi = os.path.join(ctx.gate, "check_%s_object_index.png" % cam)
    if not os.path.exists(pi):
        return None
    idx = np.asarray(Image.open(pi).convert("RGB")).astype(np.float32) / 255.0
    c = np.array(((gi + 1) % 17 / 17.0 + 0.03, ((gi + 1) // 17) % 17 / 17.0 + 0.03, ((gi + 1) // 289) % 17 / 17.0 + 0.03))
    mk = np.abs(idx - c[None, None, :]).max(axis=2) < 0.02
    return np.asarray(Image.fromarray((mk * 255).astype(np.uint8)).resize((shape[1], shape[0]), Image.NEAREST)) > 128


def cur_rows(ctx, assets, rows, di):
    """CUR-01 (the tea rooms' close review, fault 3 (f); the street review N3): (a) each curtain's head touches its rod (the nearest cloth vertex to the rod within 2 mm); (b) no face of the cloth is flat-shaded
    (the exported mesh shares its vertices: fewer than one vertex a triangle; a flat-shaded export has three a triangle); (c) in the close day frames the share of 32 px blocks inside the cloth with a luma standard
    deviation under 0.8 is under 2 per cent; (d) at STREET_SQUARE night_lit each curtain's mean luma is at least 0.8 of the glass above it (a lit cafe's cotton glows from behind)."""
    import bpy
    from mathutils.bvhtree import BVHTree
    curt = [(gi, g) for gi, g in enumerate(di["groups"]) if g["model"] == "script:cafe_curtain" and g["kind"] == "scripted"]
    rods = [(gi, g) for gi, g in enumerate(di["groups"]) if g["model"] == "script:cafe_curtain" and g["kind"] == "support"]
    if not curt:
        rows.na("CUR-01", "the curtains are cloth", "this display has no curtain")
        return
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = X.load_glb_objects(X.display_glb(assets))
    deps = bpy.context.evaluated_depsgraph_get()
    mesh = {}
    for ob in objs:
        if ob.type == "MESH":
            V, T_, N = X.mesh_world(ob, deps)
            if len(V) and len(T_):
                mesh[ob.name] = (V, T_)
    gaps, vt = [], []
    rod_bvh = []
    for gi, g in rods:
        for nm in g["objs"]:
            if nm in mesh and nm.startswith("curtain_rod"):
                V, T_ = mesh[nm]
                rod_bvh.append(BVHTree.FromPolygons(V.tolist(), T_.tolist(), epsilon=0.0))
    for gi, g in curt:
        for nm in g["objs"]:
            if nm not in mesh:
                continue
            V, T_ = mesh[nm]
            vt.append(len(V) / float(len(T_)))
            top = V[V[:, 2] > V[:, 2].max() - 0.03]
            best = 1e9
            for p_ in top[::3]:
                for bv in rod_bvh:
                    hit = bv.find_nearest(tuple(p_))
                    if hit[0] is not None:
                        best = min(best, hit[3])
            gaps.append(best)
    ok_a = bool(gaps) and max(gaps) <= 0.002
    ok_b = bool(vt) and max(vt) < 1.0
    # (c) and (d) from the gate's frames and the index renders
    det_c, ok_c, det_d, ok_d = [], True, [], True
    for cam in ("CLOSE_35", "CLOSE_35_B"):
        pf = os.path.join(ctx.gate, "%s_day.png" % cam)
        if not os.path.exists(pf):
            ok_c = False
            continue
        lum = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
        flat_n, tot_n = 0, 0
        for gi, g in curt:
            mk = _index_mask(ctx, cam, gi, lum.shape)
            if mk is None:
                continue
            for y in range(0, lum.shape[0] - 32, 32):
                for x in range(0, lum.shape[1] - 32, 32):
                    if mk[y:y + 32, x:x + 32].all():
                        tot_n += 1
                        if lum[y:y + 32, x:x + 32].std() < 0.8:
                            flat_n += 1
        share = flat_n / float(max(tot_n, 1))
        ok_c &= tot_n > 0 and share < 0.02
        det_c.append("%s %d of %d blocks (%.2f per cent)" % (cam, flat_n, tot_n, 100.0 * share))
    pf = os.path.join(ctx.gate, "STREET_SQUARE_night_lit.png")
    pm = os.path.join(ctx.gate, "check_STREET_SQUARE_night_lit_mask.png")
    if os.path.exists(pf) and os.path.exists(pm):
        lum = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
        glass = np.asarray(Image.open(pm).convert("L").resize((lum.shape[1], lum.shape[0]), Image.NEAREST)) > 128
        for gi, g in curt:
            mk = _index_mask(ctx, "STREET_SQUARE", gi, lum.shape)
            if mk is None or mk.sum() < 500:
                ok_d = False
                continue
            ys, xs = np.nonzero(mk)
            y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
            band = np.zeros_like(mk)
            band[max(0, y0 - (y1 - y0)):max(0, y0 - 4), x0:x1 + 1] = True
            band &= glass & ~mk
            cur_l = float(lum[mk].mean())
            room_l = float(lum[band].mean()) if band.any() else 0.0
            ratio = cur_l / max(room_l, 1e-6)
            ok_d &= ratio >= 0.8
            det_d.append("%s %.1f against %.1f above it (%.2f)" % (g["objs"][0], cur_l, room_l, ratio))
    else:
        ok_d = False
    rows.add("CUR-01", "the curtains are cloth, hung from the rod, lit from behind", ok_a and ok_b and ok_c and ok_d,
             "(a) the cloth's head to its rod: nearest %.1f mm (at most 2); (b) vertices a triangle in the exported cloth %s (under 1: smooth-shaded; a flat-shaded export has 3); (c) close day frames, 32 px blocks inside the cloth with a luma sd under 0.8: %s (under 2 per cent); (d) STREET_SQUARE night_lit, each curtain against the glass above it: %s (at least 0.8)" % (
                 (max(gaps) * 1000.0) if gaps else -1, ", ".join("%.2f" % v for v in vt), "; ".join(det_c), "; ".join(det_d)))


# --------------------------------------------------------------------------------------------------------------------------------------------- DSP-12, DSP-13 (the newsagent's racks and board)
def news_rows(ctx, R, assets, rows, di, members):
    """DSP-12 (the newsagent's street review, narrow 2: the postcard rack's pole stood on the mullion's edge): from STREET_SQUARE no rack's pole projects within 10 px (of 2560 x 1440) of a mullion or a jamb: the pole's
    silhouette (the vertices of the rack's frame between w 0.05 and 0.45, where only the pole is) and each `win_mullion_*` / `win_jamb*` member's projected box are separated by at least 10 px.
    DSP-13 (the street review, narrow 1: "a bare grey band shows above the covers"): along the sloping board no more than 20 mm of bare board shows above the top row of covers (the highest cover vertex against the board's
    top edge, measured along the board's slope)."""
    import bpy
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = X.load_glb_objects(X.display_glb(assets))
    deps = bpy.context.evaluated_depsgraph_get()
    mesh = {}
    for ob in objs:
        if ob.type == "MESH":
            V, T_, N = X.mesh_world(ob, deps)
            if len(V):
                mesh[ob.name] = V
    off = np.array([ctx.window_cx_m, -0.025, 0.600])
    cp = X.cam_params(R, "STREET_SQUARE", (2560, 1440))

    def px_x(P):
        x, y, zc = X.project_np(cp, P)
        return float(x.min()), float(x.max())
    stops = []
    for k, v in members.items():
        if k.startswith(("win_mullion_", "win_jamb", "frame_jamb", "pil")) and "u" in v:
            cs = np.array([[(u_ - 3000.0) / 1000.0, -d_ / 1000.0, z_ / 1000.0] for u_ in v["u"] for d_ in v["d"] for z_ in v["z"]])
            stops.append((k, px_x(cs)))
    det, ok, n = [], True, 0
    for g in di["groups"]:
        if g["model"] in ("script:postcard_rack", "script:card_rack") and g["kind"] == "support":
            for nm in g["objs"]:
                V = mesh.get(nm)
                if V is None:
                    continue
                # 15 Oct, try 2 (the newsagent's try 2 street review, narrow 7: the row measured the card spinner only: the postcard rack's pole is one long rod with vertices at its two ends and none between w 0.05 and
                # 0.45): the pole is every vertex within 7.5 mm of the rack's axis (the mean of the vertices on the bed), over the pole's whole height
                low_ = V[V[:, 2] < 0.002]
                if not len(low_):
                    continue
                ax_ = low_[:, :2].mean(axis=0)
                pole = V[np.linalg.norm(V[:, :2] - ax_[None, :], axis=1) <= 0.0075]
                if not len(pole):
                    continue
                a, b = px_x(pole + off)
                gap = min([max(sa - b, a - sb) for _, (sa, sb) in stops] or [999.0])
                n += 1
                ok &= gap >= 10.0
                det.append("%s pole at x %.0f to %.0f px, %.0f px from the nearest mullion or jamb" % (g["model"].replace("script:", ""), a, b, gap))
    found_ = {d_.split(" pole")[0] for d_ in det}
    missing_ = sorted({"postcard_rack", "card_rack"} - found_)                # 15 Oct: both racks must be measured (the row once read the card spinner only)
    if missing_:
        det.append("NOT MEASURED: %s" % ", ".join(missing_))
        ok = False
    rows.add("DSP-12", "no rack's pole stands on a mullion", ok and n > 0, "STREET_SQUARE (2560 x 1440): " + "; ".join(det) + " (at least 10 px; try 1: the postcard rack's pole 0.8 px behind the mullion's edge)")
    board = next((mesh[nm] for g in di["groups"] if g["model"] == "script:magazine_board" for nm in g["objs"] if nm in mesh), None)
    covers = [mesh[nm] for g in di["groups"] if g["model"] == "script:magazines" for nm in g["objs"] if nm in mesh]
    if board is None or not covers:
        rows.add("DSP-13", "no bare board above the covers", False, "the board or the covers are missing from the glb")
        return
    lean = math.radians(35.0)
    sb_, cb_ = math.sin(lean), math.cos(lean)
    mid = board[:, 0].mean()
    sl = lambda P: (P[:, 1] * sb_ + P[:, 2] * cb_)                      # the coordinate along the board's up-slope (v and w in the display frame)
    # the slab's own vertices: those on the slope (not the cheeks' foot and back points): the board's top edge is the largest along-slope coordinate among vertices above w 0.3
    top_board = float(sl(board[board[:, 2] > 0.30]).max())
    top_cov = max(float(sl(c).max()) for c in covers)
    bare = top_board - top_cov
    rows.add("DSP-13", "no bare board above the covers", bare <= 0.020 + 1e-6, "along the board's slope the board's top edge stands %.1f mm above the highest cover vertex (at most 20 mm; try 1: a third row hidden behind the board and a grey band of about 130 mm showed); %d covers" % (bare * 1000.0, len(covers)))
