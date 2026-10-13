"""The try 2 checks (13 October): the rows the two fresh reviews asked for, run on what the build made. Used by check_ritas.py (every row prints in the same "N of M rows pass").

  FAS-01n/FAS-01c  the fascia's normal map is a real tangent-space map; the board reads by day (street review F1)
  GLS-02           no ink pixel of a glass row lies behind a bar, mullion or bead at STREET_SQUARE and STREET_30 (F2)
  LIT-07           the night spill's three conditions (N1); LIT-05 is measured on the glass only
  FRN-07 (extended), FRN-08  the elevation over the whole bay with the gate's piers; the front alone against a white backdrop from the close cameras (N2, fault 5)
  FRN-09           the hall behind the side door hides the card from STREET_SQUARE (N3)
  FAS-03           every textured primitive carries TEXCOORD_0, every texCoord is 0 or more (N4)
  DSP-03, DSP-04   no display mesh intersects another; every piece shows half its silhouette; no free run along a tier over 0.20 m (close fault 1, 2)
  LIT-02b          the rendered frames with the glass's reflection off: at most 1 per cent of the window-glass pixels under luma 12 (close fault 3)
  PIC-05g          the gate's rendered review frames: at most 1 per cent at 250 or above (close fault 4)
  SO-06, ROOM-01/02  the stock wall's scales 0.9 to 1.1; the boards' coverage (close narrow 2, 3)
13 October, from the try 2 reviews (the narrow points):
  FRN-10           no two parts of the front share a face plane where a camera can see it; nothing on the front under luma 8 by day outside the glass (street 1, close 2)
  GLS-03           at night, p95 of |frame - the reflection-off render| over the glass at most 15 levels at every camera (street 2, close 3)
  LIT-08           at night from the two close cameras every display piece's mean luma over the lattice's gaps is at least 0.6 of the room's mean luma round it (close 1)
  SO-07            no room mesh intersects another, 2 mm tolerance (close 5)
  DSP-03 (changed) every front-row piece shows at least half its silhouette from STREET_SQUARE itself (street 3)
  LIT-02b (changed) a slab test at the street cameras: the largest patch of dark room pixels at most 1 per cent of the glass (street 6, close 8)
  LIT-07 (changed) the pavement-pool condition is struck (street 5)
  ROOM-02 (changed) each row of the right board filled to 80 per cent of its width (close 6); ROOM-03 the risers and the boxes on the sets; ROOM-04 the left board's clocks (close 4)
"""
import json
import math
import os
import struct
import hashlib
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_assets as A  # noqa: E402
import sw_gate as G  # noqa: E402
import sw_ctx  # noqa: E402

CHECK_RES = (1280, 720)
_LAST = {}

# 13 October (batch A): the rows are for any shop. `use(ctx)` names the shop (Rita's when never called, so her checks run as they did); the file names, the frames and the shop's own numbers come from it.
_CTX = [None]


def use(ctx):
    _CTX[0] = ctx


def ctx():
    if _CTX[0] is None:
        _CTX[0] = sw_ctx.rita()
    return _CTX[0]


def to_model(p):
    return ctx().to_model(p)


def front_glb(assets):
    return os.path.join(assets, ctx().front_glb)


def display_glb(assets):
    return os.path.join(assets, ctx().display_glb)


def glbs_of(assets):
    """The shop's own glbs that exist (the front always; the lattice and the display where the shop has them)."""
    c = ctx()
    out = [c.front_glb]
    if c.has_grille:
        out.append(c.grille_glb)
    if c.has_room:
        out.append(c.display_glb)
    return [n for n in out if os.path.exists(os.path.join(assets, n))]


def picture(work, state):
    c = ctx()
    return os.path.join(c.rooms if c.id != "ritas" else os.path.join(work, "rooms"), "%s_%s.png" % (c.picture_name or "pawnbroker", state))


def luma(arr):
    return 0.2126 * arr[..., 0] + 0.7152 * arr[..., 1] + 0.0722 * arr[..., 2]


def glb_json(path):
    raw = open(path, "rb").read()
    jl = struct.unpack("<I", raw[12:16])[0]
    return json.loads(raw[20:20 + jl]), raw, 20 + jl


def glb_image_bytes(path, index):
    g, raw, off = glb_json(path)
    bl = struct.unpack("<I", raw[off:off + 4])[0]
    bin0 = off + 8
    bv = g["bufferViews"][g["images"][index]["bufferView"]]
    return raw[bin0 + bv.get("byteOffset", 0): bin0 + bv.get("byteOffset", 0) + bv["byteLength"]]


# ------------------------------------------------------------------------------------------------------------------------- cameras and projection
def cam_params(R, cam, res=CHECK_RES):
    cd = R["cameras"][cam]
    eye = np.array(to_model(cd["eye_street_m"]))
    aim = np.array(to_model(cd["aim_street_m"]))
    fwd = (aim - eye) / np.linalg.norm(aim - eye)
    right = np.cross(fwd, np.array([0, 0, 1.0]))
    right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    f = (res[1] / 2.0) / math.tan(math.radians(G.VFOV[cam]) / 2.0)
    return {"eye": eye, "fwd": fwd, "right": right, "up": up, "f": f, "res": res}


def project_np(cp, pts):
    """pixel positions (x, y) and depth of model-frame points (n, 3)."""
    d = pts - cp["eye"]
    zc = d @ cp["fwd"]
    zc_safe = np.where(np.abs(zc) < 1e-9, 1e-9, zc)
    x = cp["res"][0] / 2.0 + cp["f"] * (d @ cp["right"]) / zc_safe
    y = cp["res"][1] / 2.0 - cp["f"] * (d @ cp["up"]) / zc_safe
    return x, y, zc


def pixel_ray(cp, x, y):
    """unit ray directions for pixel coordinates (arrays)."""
    dx = (x - cp["res"][0] / 2.0) / cp["f"]
    dy = -(y - cp["res"][1] / 2.0) / cp["f"]
    d = cp["fwd"][None, :] + dx[:, None] * cp["right"][None, :] + dy[:, None] * cp["up"][None, :]
    return d / np.linalg.norm(d, axis=1, keepdims=True)


# ------------------------------------------------------------------------------------------------------------------------- a BVH of the front
def load_glb_objects(path):
    import bpy
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    bpy.context.view_layer.update()
    return [o for o in bpy.data.objects if o not in before]


def mesh_world(ob, deps):
    me = ob.evaluated_get(deps).to_mesh()
    mw = ob.matrix_world
    n = len(me.vertices)
    co = np.empty(n * 3, np.float64)
    me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3)
    M = np.array(mw)
    V = co @ M[:3, :3].T + M[:3, 3]
    me.calc_loop_triangles()
    T = np.empty(len(me.loop_triangles) * 3, np.int32)
    me.loop_triangles.foreach_get("vertices", T)
    T = T.reshape(-1, 3)
    nrm = np.empty(n * 3, np.float64)
    me.vertices.foreach_get("normal", nrm)
    nrm = nrm.reshape(-1, 3) @ M[:3, :3].T
    ob.evaluated_get(deps).to_mesh_clear()
    return V, T, nrm


def front_bvh(glb, skip=("glass", "sign_", "door_sign", "grille_lattice"), skip_names=()):
    """(BVHTree, [object name of each triangle]) of the front's opaque parts, world (model frame) coordinates."""
    import bpy
    from mathutils.bvhtree import BVHTree
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = load_glb_objects(glb)
    deps = bpy.context.evaluated_depsgraph_get()
    verts, polys, owner = [], [], []
    off = 0
    for ob in objs:
        if ob.type != "MESH":
            continue
        low = ob.name.lower()
        if low.startswith(skip) or "glass" in low or ob.name in skip_names:
            continue
        V, T, _ = mesh_world(ob, deps)
        verts.extend(V.tolist())
        polys.extend((T + off).tolist())
        owner.extend([ob.name] * len(T))
        off += len(V)
    return BVHTree.FromPolygons(verts, polys, epsilon=1e-6), owner


# ------------------------------------------------------------------------------------------------------------------------- the rows
def fascia_rows(R, work, assets, rows, front_png_day_sq, members):
    """FAS-01n: every normalTexture in the front's glb is RGB, mean within 10 levels of (128, 128, 255), blue 200 or more on 99 per cent of pixels.
    FAS-01c: by day at STREET_SQUARE the board's ground luma is within 15 per cent of the stallriser's and the letters are 2.0 or more times the ground."""
    import io
    glb = front_glb(assets)
    g, _, _ = glb_json(glb)
    det, ok = [], True
    ntex = 0
    for m in g["materials"]:
        nt = m.get("normalTexture")
        if nt is None:
            continue
        ntex += 1
        src = g["textures"][nt["index"]]["source"]
        im = Image.open(io.BytesIO(glb_image_bytes(glb, src)))
        a = np.asarray(im.convert("RGB")).astype(np.float32)
        mean = a.reshape(-1, 3).mean(axis=0)
        blue = float((a[..., 2] >= 200).mean())
        good = im.mode in ("RGB", "RGBA") and np.abs(mean - np.array([128, 128, 255])).max() <= 10 and blue >= 0.99
        ok &= bool(good)
        det.append("%s: %s %dx%d, mean (%.1f, %.1f, %.1f), blue 200+ on %.2f%%" % (m["name"], im.mode, im.size[0], im.size[1], mean[0], mean[1], mean[2], blue * 100))
    rows.add("FAS-01n", "the fascia's normal map is a normal map", ok and ntex > 0, "%d normalTexture(s) in the glb: %s (RGB, mean within 10 levels of 128, 128, 255, blue 200 or more on 99 per cent of pixels)" % (ntex, "; ".join(det) or "none"))
    # contrast on the render: project the board and the stallriser; the letters from the base-colour map
    if not os.path.exists(front_png_day_sq):
        rows.add("FAS-01c", "the board reads by day", False, "STREET_SQUARE_day.png was not rendered")
        return
    im = np.asarray(Image.open(front_png_day_sq).convert("RGB")).astype(np.float32)
    res = (im.shape[1], im.shape[0])
    cp = cam_params(R, "STREET_SQUARE", res)
    fb = members["fas_board"]
    d_face = 0.001 * fb["d"][1] if False else None
    # the board's front face: u 295..5705, z 2850..3400, at d = 120 (the face; the bed mould stands further out): take the rectangle at the face's depth
    d_face = 120.0
    X0, X1 = (295.0 - 3000.0) / 1000.0, (5705.0 - 3000.0) / 1000.0
    Z0, Z1 = 2.850, 3.400
    ycoord = -d_face / 1000.0
    corners = np.array([[X0, ycoord, Z1], [X1, ycoord, Z1], [X1, ycoord, Z0], [X0, ycoord, Z0]])
    cx, cy, _ = project_np(cp, corners)
    # homography from the base-colour map (5410 x 550) to the image: bilinear on the 4 corners is exact for a plane under pinhole only with the perspective division; use the
    # homography solved from the 4 correspondences
    src_pts = np.array([[0, 0], [5410, 0], [5410, 550], [0, 550]], float)
    dst_pts = np.stack([cx, cy], axis=1)
    Aeq, b = [], []
    for (sx, sy), (dx, dy) in zip(src_pts, dst_pts):
        Aeq.append([sx, sy, 1, 0, 0, 0, -dx * sx, -dx * sy])
        b.append(dx)
        Aeq.append([0, 0, 0, sx, sy, 1, -dy * sx, -dy * sy])
        b.append(dy)
    h = np.linalg.solve(np.array(Aeq), np.array(b))
    H = np.array([[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1.0]])
    Hi = np.linalg.inv(H)
    x0, x1 = int(max(0, cx.min())), int(min(res[0] - 1, cx.max()))
    y0, y1 = int(max(0, cy.min())), int(min(res[1] - 1, cy.max()))
    xs, ys = np.meshgrid(np.arange(x0, x1 + 1), np.arange(y0, y1 + 1))
    P = np.stack([xs.ravel() + 0.5, ys.ravel() + 0.5, np.ones(xs.size)], axis=0)
    Q = Hi @ P
    tu, tv = Q[0] / Q[2], Q[1] / Q[2]
    base = np.asarray(Image.open(os.path.join(work, "fascia_export", "%s_basecolour_worn.png" % ctx().id)).convert("RGB")).astype(np.float32)
    inside = (tu >= 0) & (tu < 5410) & (tv >= 0) & (tv < 550)
    tl = luma(base)
    # letters: the gilt of the name block (centre third of the board, texture luma well above the ground's), ground: the maroon (texture luma near the median)
    ti = np.clip(tu.astype(int), 0, 5409)
    tj = np.clip(tv.astype(int), 0, 549)
    tluma = tl[tj, ti]
    med = float(np.median(tl))
    rita_ = ctx().id == "ritas"
    if rita_:
        sel_letters = inside & (tluma > med * 1.8) & (tu > 1500) & (tu < 3900)
        sel_ground = inside & (np.abs(tluma - med) < med * 0.25) & (tu > 400) & (tu < 5000)
    else:
        # 13 Oct, batch A: the lettering is whatever stands away from the ground's luma by more than 0.6 of it in either direction (light letters on a dark board, or dark on light), over the whole board
        sel_letters = inside & (np.abs(tluma - med) > med * 0.6) & (tu > 400) & (tu < 5000)
        sel_ground = inside & (np.abs(tluma - med) < med * 0.25) & (tu > 400) & (tu < 5000)
    if not rita_ and not sel_letters.any():
        rows.na("FAS-01c", "the board reads by day", "the board's picture carries no lettering (an empty unit's bare timber; Mickey's letters are applied in 3D and are measured by FAS-04)")
        return
    rl = luma(im.reshape(-1, 3).reshape(im.shape))[ys.ravel(), xs.ravel()]
    ground = float(rl[sel_ground].mean()) if sel_ground.any() else 0.0
    light_letters = bool(sel_letters.any() and float(tluma[sel_letters].mean()) > med)
    if rita_ or light_letters:
        letters = float(np.percentile(rl[sel_letters], 75)) if sel_letters.any() else 0.0
        cl = letters / ground if ground else 0.0
    else:
        letters = float(np.percentile(rl[sel_letters], 25)) if sel_letters.any() else 0.0
        cl = ground / max(letters, 1.0)
    # the stallriser's panel (front face; Rita's: d 135, u 2400..5550, z 0.10 to 0.45): its mean luma over the panel's middle band
    if rita_:
        su0, su1, sd, sz0, sz1 = 2400.0, 5550.0, 0.135, 0.10, 0.45
    else:
        sp_ = members["sta_panel"]
        wu = ctx().window_u
        su0, su1, sd, sz0, sz1 = wu[0] + 100.0, wu[1] - 100.0, sp_["d"][1] / 1000.0, max(0.10, sp_["z"][0] / 1000.0 + 0.10), min(0.45, sp_["z"][1] / 1000.0 - 0.05)
    st = np.array([[(su0 - 3000) / 1000.0, -sd, sz1], [(su1 - 3000) / 1000.0, -sd, sz1], [(su1 - 3000) / 1000.0, -sd, sz0], [(su0 - 3000) / 1000.0, -sd, sz0]])
    sx_, sy_, _ = project_np(cp, st)
    mk = Image.new("L", res, 0)
    ImageDraw.Draw(mk).polygon(list(zip(sx_, sy_)), fill=255)
    smask = np.asarray(mk) > 0
    stall = float(luma(im)[smask].mean())
    ratio = ground / stall if stall else 0.0
    if rita_:
        rows.add("FAS-01c", "the board reads by day", abs(ground - stall) / stall <= 0.15 and cl >= 2.0,
                 "STREET_SQUARE by day: the board's ground luma %.1f against the stallriser's %.1f (%.0f per cent; within 15 per cent), the gilt letters (75th percentile of the lettering's pixels) %.1f: letters to ground %.2f (at least 2.0; try 1: 34.2 against 55.6 and 1.39)" % (ground, stall, 100.0 * ratio, letters, cl))
    else:
        rows.add("FAS-01c", "the board reads by day", cl >= 2.0 and ground >= 12.0,
                 "STREET_SQUARE by day: the board's ground luma %.1f (not black: at least 12), the %s letters (%s of the lettering's pixels) %.1f: letters to ground %.2f (at least 2.0). The stallriser's luma %.1f is written beside it (%.0f per cent of the ground's); for Rita's the two had to agree within 15 per cent because both were one paint, which is not asked of a shop whose stallriser is another material" % (
                     ground, "light" if light_letters else "dark", "75th percentile" if light_letters else "25th percentile", letters, cl, stall, 100.0 * ratio))


def glass_rows_check(R, work, assets, rows, members):
    """GLS-02: no ink pixel of a glass row lies behind a bar, mullion or bead at STREET_SQUARE and STREET_30 (a ray from the eye to each ink pixel meets nothing opaque first)."""
    bvh, owner = front_bvh(front_glb(assets))
    fasc = os.path.join(work, "fascias")
    man = json.load(open(os.path.join(fasc, "manifest.json")))
    out, ok = [], True
    for cam in ("STREET_SQUARE", "STREET_30"):
        cp = cam_params(R, cam)
        for g in man["glass_lettering"]:
            if g["shop"] != ctx().id or (ctx().id == "ritas" and g["row"] not in (7, 8, 9)):
                continue
            keys = [k for k in members if k.startswith("glass_row_%d_" % g["row"])]
            if not keys:
                continue
            mem = members[keys[0]]
            a = np.asarray(Image.open(os.path.join(fasc, g["files"]["rgba"]["file"])).convert("RGBA"))[..., 3]
            jj, ii = np.nonzero(a[::2, ::2] > 128)
            jj, ii = jj * 2, ii * 2
            u = mem["u_mm"][0] + ii + 0.5
            z = mem["z_mm"][1] - jj - 0.5
            pts = np.stack([(u - 3000.0) / 1000.0, np.full(len(u), -mem["d_mm"] / 1000.0), z / 1000.0], axis=1)
            blocked = 0
            by = {}
            for p in pts:
                d = p - cp["eye"]
                dist = float(np.linalg.norm(d))
                hit = bvh.ray_cast(tuple(cp["eye"]), tuple(d / dist))
                if hit[0] is not None and hit[3] < dist - 1e-3:
                    blocked += 1
                    nm = owner[hit[2]]
                    by[nm] = by.get(nm, 0) + 1
            ok &= blocked == 0
            out.append("%s %s: %d of %d ink points behind %s" % (cam, g["string"], blocked, len(pts), by or "nothing"))
    rows.add("GLS-02", "no glass row lies behind a bar, mullion or bead", ok, "a ray from the camera's eye to each ink point of %s (the row's alpha, every 2 mm) must meet no opaque part of the front first: " % ("WATCHES, JEWELLERY and LOANS" if ctx().id == "ritas" else "the shop's glass rows") + "; ".join(out))


def hall_check(R, work, assets, rows, members):
    """FRN-09: through the side door's fanlight from STREET_SQUARE every ray meets the hall (or the door frame), none gets through to the room's card."""
    bvh, owner = front_bvh(front_glb(assets))
    cp = cam_params(R, "STREET_SQUARE")
    if ctx().id == "ritas":
        us = np.linspace(450.0, 1200.0, 40)
        zs = np.linspace(2130.0, 2380.0, 14)
    else:
        fg = members["glass_fanlight"]          # the side door's fanlight (the F1 family's `glass_fanlight`): rays through its middle, 15 mm in from its edges
        us = np.linspace(fg["u"][0] + 15, fg["u"][1] - 15, 40)
        zs = np.linspace(fg["z"][0] + 15, fg["z"][1] - 15, 14)
    miss, hall, other = 0, 0, {}
    tot = 0
    for u in us:
        for z in zs:
            p = np.array([(u - 3000.0) / 1000.0, -0.081, z / 1000.0])
            d = p - cp["eye"]
            d /= np.linalg.norm(d)
            # start just behind the fanlight's glass (d 82), so the glass and the front of the frame are not what is asked
            hit = bvh.ray_cast(tuple(p + d * 0.002), tuple(d))
            tot += 1
            if hit[0] is None:
                miss += 1
            else:
                nm = owner[hit[2]]
                if nm.startswith("hall_"):
                    hall += 1
                else:
                    other[nm] = other.get(nm, 0) + 1
    rows.add("FRN-09", "the hall behind the side door", miss == 0 and hall >= 0.5 * tot,
             "%d rays from STREET_SQUARE's eye through the side door's fanlight (u 450 to 1200, z 2130 to 2380): %d meet the hall's own walls, floor or ceiling, %d the door and its frame (%s), %d get through to the card: none may (try 1: the room's wall clock and pegboard showed)" % (tot, hall, sum(other.values()), ", ".join("%s %d" % kv for kv in sorted(other.items())[:5]), miss))


def uv_rows(assets, rows):
    """FAS-03: every textured primitive carries TEXCOORD_0 and every texCoord is 0 or more, in the three glbs."""
    det, ok = [], True
    for nm in glbs_of(assets):
        g, _, _ = glb_json(os.path.join(assets, nm))
        bad_prims, bad_tc = 0, 0
        for m in g["materials"]:
            def walk(o):
                nonlocal bad_tc
                if isinstance(o, dict):
                    if "texCoord" in o and o["texCoord"] < 0:
                        bad_tc += 1
                    for v in o.values():
                        walk(v)
            walk(m)
        for me in g["meshes"]:
            for pr in me["primitives"]:
                mat = g["materials"][pr["material"]] if "material" in pr else None
                if mat is None:
                    continue
                pb = mat.get("pbrMetallicRoughness", {})
                tex = any(k in pb for k in ("baseColorTexture", "metallicRoughnessTexture")) or any(k in mat for k in ("normalTexture", "emissiveTexture", "occlusionTexture"))
                if tex and "TEXCOORD_0" not in pr["attributes"]:
                    bad_prims += 1
        ok &= bad_prims == 0 and bad_tc == 0
        det.append("%s: %d textured primitives without TEXCOORD_0, %d negative texCoord" % (nm, bad_prims, bad_tc))
    rows.add("FAS-03", "textured primitives carry UVs", ok, "; ".join(det) + " (try 1: the three balls had none and pointed their maps at texCoord -1)")


def frn07_rows(R, work, rows):
    from scipy import ndimage as ndi
    mask = np.asarray(Image.open(os.path.join(work, "front_elevation_mask.png"))) > 0
    parts = np.asarray(Image.open(os.path.join(work, "front_elevation_mask_parts.png"))) > 0
    mask = ndi.binary_dilation(mask, iterations=1)
    e = ~mask
    lab, nc = ndi.label(e)
    big, wh = 0, (0, 0)
    for s in ndi.find_objects(lab):
        hh, ww = s[0].stop - s[0].start, s[1].stop - s[1].start
        if hh * ww > big:
            big, wh = hh * ww, (ww, hh)
    ep = ndi.label(~ndi.binary_dilation(parts, iterations=1))[0]
    outer = int(((~ndi.binary_dilation(parts, iterations=1))[:, :350].sum() + (~ndi.binary_dilation(parts, iterations=1))[:, 5650:].sum()))
    ok7 = wh[0] <= 5 and wh[1] <= 5
    return ok7, wh, int(e.sum()), e.size, outer


def silhouette_hull(sil):
    from scipy.spatial import ConvexHull
    ys, xs = np.nonzero(sil)
    if len(xs) < 10:
        return np.zeros_like(sil)
    pts = np.stack([xs, ys], axis=1)
    hull = ConvexHull(pts[::7] if len(pts) > 20000 else pts)
    poly = [tuple(pts[::7][i] if len(pts) > 20000 else pts[i]) for i in hull.vertices]
    m = Image.new("L", (sil.shape[1], sil.shape[0]), 0)
    ImageDraw.Draw(m).polygon(poly, fill=255)
    return np.asarray(m) > 0


def backdrop_rows(R, assets, work, rows):
    """FRN-08: the front alone (its glass made opaque, no hanging sign) against a white emissive backdrop, from each review camera: no backdrop pixel may show inside the front's outline
    (the silhouette with its enclosed holes filled)."""
    import bpy
    import mathutils
    res = CHECK_RES
    out, ok = [], True
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        objs = load_glb_objects(front_glb(assets))
        solid = bpy.data.materials.new("solid")
        solid.use_nodes = True
        solid.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.2, 0.2, 0.2, 1)
        for o in list(objs):
            if o.type != "MESH":
                continue
            if o.name.startswith(("sign_", "glass_row", "door_sign")):
                bpy.data.objects.remove(o, do_unlink=True)
                continue
            for sl in o.material_slots:
                if sl.material and sl.material.name.lower().startswith("glass"):
                    sl.material = solid
        me = bpy.data.meshes.new("bd")
        me.from_pydata([(-30, 3.0, -8), (30, 3.0, -8), (30, 3.0, 30), (-30, 3.0, 30)], [], [(0, 1, 2, 3)])
        bd = bpy.data.objects.new("bd", me)
        sc.collection.objects.link(bd)
        m = bpy.data.materials.new("white")
        m.use_nodes = True
        nt = m.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        e = nt.nodes.new("ShaderNodeEmission")
        o2 = nt.nodes.new("ShaderNodeOutputMaterial")
        nt.links.new(e.outputs[0], o2.inputs[0])
        bd.data.materials.append(m)
        cd = R["cameras"][cam]
        eye = to_model(cd["eye_street_m"])
        aim = to_model(cd["aim_street_m"])
        cam_d = bpy.data.cameras.new("cam")
        cam_d.sensor_fit = "VERTICAL"
        cam_d.angle_y = math.radians(G.VFOV[cam])
        cam_d.clip_start = 0.05
        co = bpy.data.objects.new("cam", cam_d)
        sc.collection.objects.link(co)
        co.location = mathutils.Vector(eye)
        co.rotation_euler = (mathutils.Vector(aim) - mathutils.Vector(eye)).to_track_quat("-Z", "Y").to_euler()
        sc.camera = co
        w = bpy.data.worlds.new("w")
        sc.world = w
        w.use_nodes = True
        w.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
        w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 1
        sc.cycles.use_denoising = False
        sc.cycles.use_adaptive_sampling = False
        sc.cycles.filter_width = 0.01
        sc.view_settings.view_transform = "Standard"
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        path = os.path.join(work, "gate", "check_%s_front_backdrop.png" % cam)
        sc.render.filepath = path
        sc.render.image_settings.file_format = "PNG"
        bpy.ops.render.render(write_still=True)
        a = np.asarray(Image.open(path).convert("L"))
        white = a > 128
        front = ~white
        holes = ndimage.binary_fill_holes(front) & white              # backdrop pixels the front's outline encloses
        lab, nl = ndimage.label(holes)
        sizes = np.bincount(lab.ravel())[1:] if nl else np.array([0])
        n_holes = int(sizes[sizes >= 4].sum())                         # specks of 1 to 3 px are aliasing at a seam
        big = int(sizes.max())
        if cam in ("CLOSE_35", "CLOSE_35_B"):
            ok &= n_holes == 0
        out.append("%s %d px (largest %d)%s" % (cam, n_holes, big, "" if cam in ("CLOSE_35", "CLOSE_35_B") else (" [the bay's outer sliver beside the right pilaster, which the gate's pier closes: N2]" if n_holes else "")))
    rows.add("FRN-08", "no backdrop through the front", ok, "the front alone (glass opaque, no hanging sign) against a white emissive backdrop, 1280 x 720, from each review camera: backdrop pixels the front's outline encloses (specks under 4 px not counted): " + "; ".join(out) + " (none allowed from CLOSE_35 and CLOSE_35_B, the review's cameras; the street cameras show only the bay's outer sliver, N2)")
    return ok


# ------------------------------------------------------------------------------------------------------------------------- the display
def tri_inset(V, T, N, d):
    return V - N * d


def display_rows(R, work, assets, rows):
    """DSP-03 and DSP-04."""
    import bpy
    from mathutils.bvhtree import BVHTree
    di = json.load(open(os.path.join(work, "display_work", "display_items.json")))
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = load_glb_objects(display_glb(assets))
    deps = bpy.context.evaluated_depsgraph_get()
    meshes = {}
    for ob in objs:
        if ob.type == "MESH":
            meshes[ob.name] = ob
    group_of = {}
    for gi, g in enumerate(di["groups"]):
        for nm in g["objs"]:
            group_of[nm] = gi
    data = {}
    for nm, ob in meshes.items():
        V, T, N = mesh_world(ob, deps)
        if len(V) == 0 or len(T) == 0:
            continue
        lo, hi = V.min(axis=0), V.max(axis=0)
        inset = min(0.001, 0.2 * float((hi - lo).min()) / 2.0)
        Ne = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
        Ve = V - Ne * inset
        data[nm] = {"lo": lo, "hi": hi, "bvh": BVHTree.FromPolygons(Ve.tolist(), T.tolist(), epsilon=0.0)}
    names = sorted(data)
    pairs, bad = 0, []
    tol = 0.002
    for i in range(len(names)):
        a = data[names[i]]
        for j in range(i + 1, len(names)):
            b = data[names[j]]
            if np.any(a["hi"] < b["lo"] + tol) or np.any(b["hi"] < a["lo"] + tol):
                continue
            ga, gb = group_of.get(names[i]), group_of.get(names[j])
            if ga is not None and ga == gb:
                continue
            pairs += 1
            ov = a["bvh"].overlap(b["bvh"])
            if ov:
                bad.append((names[i], names[j], len(ov)))
    # which group (piece) each object belongs to, for the report
    def label(nm):
        gi = group_of.get(nm)
        if gi is None:
            return nm
        g = di["groups"][gi]
        return "%s(%s)" % (g["model"], nm)
    bad_l = [(label(a), label(b), n) for a, b, n in bad]
    # the silhouette visibility: object-index pass from STREET_SQUARE and CLOSE_35
    per_cam = visibility(R, work, assets, di, group_of)
    areas = per_cam.pop("areas")
    _LAST["vis"] = (per_cam, areas, di)          # for the trade's-goods row (check_shop.py TRD-01)
    vis = np.maximum(per_cam["STREET_SQUARE"], per_cam["CLOSE_35"])
    sq = per_cam["STREET_SQUARE"]
    # 13 Oct, from the try 2 reviews (street 3): the front row (the bed's pieces and the scripted trays, pads and chains) must show half its silhouette from STREET_SQUARE ITSELF, because the
    # old rule (the better of CLOSE_35 and STREET_SQUARE) let a front row that the far pavement could not see pass; every other piece keeps the old rule
    front_row = [i for i, g in enumerate(di["groups"]) if (g["kind"] == "piece" and g.get("tier") == "bed") or g["kind"] == "scripted"]
    other = [i for i, g in enumerate(di["groups"]) if g["kind"] == "piece" and i not in front_row]
    # a front-row piece whose whole silhouette is under 20 px at STREET_SQUARE (a chain: 0.14 m long and 4 mm wide, a line under one pixel at 8.76 m) cannot be shown from the far pavement by any
    # arrangement: it is judged from the better of the two close cameras (a glazing bar stands over a 4 mm chain from one of them), and named
    tiny = [i for i in front_row if areas["STREET_SQUARE"][i] <= 20]
    low_front = [(di["groups"][i]["model"], round(float(sq[i]), 2)) for i in front_row if i not in tiny and sq[i] < 0.5] + [(di["groups"][i]["model"] + " (from the close cameras)", round(float(max(per_cam["CLOSE_35"][i], per_cam["CLOSE_35_B"][i])), 2)) for i in tiny if max(per_cam["CLOSE_35"][i], per_cam["CLOSE_35_B"][i]) < 0.5]
    low = [(di["groups"][i]["model"], round(float(vis[i]), 2)) for i in other if vis[i] < 0.5]
    rows.add("DSP-03", "no display mesh intersects another; every piece shows", not bad and not low and not low_front,
             "%d display meshes, %d pairs with overlapping boxes tested (each mesh inset 1 mm, so a 2 mm contact is tolerated): %d pairs intersect%s; the share of each piece's silhouette seen (an object-index pass, the frame's bars and the other pieces in front): the %d pieces of the front row (the bed's pieces and the scripted trays, pads and chains) from STREET_SQUARE itself: lowest %.2f among the %d large enough to be seen there (%d are under 20 px: %s, judged from the better of CLOSE_35 and CLOSE_35_B, lowest %.2f), %d under 0.5%s; the other %d pieces from CLOSE_35 or STREET_SQUARE: lowest %.2f, %d under 0.5%s"
             % (len(names), pairs, len(bad), (" (" + "; ".join("%s x %s" % (a, b) for a, b, _ in bad_l[:8]) + ")") if bad else "", len(front_row), min([float(sq[i]) for i in front_row if i not in tiny] or [0]), len(front_row) - len(tiny), len(tiny), ", ".join(sorted({di["groups"][i]["model"] for i in tiny})) or "none", min([float(max(per_cam["CLOSE_35"][i], per_cam["CLOSE_35_B"][i])) for i in tiny] or [0]), len(low_front),
                (": " + ", ".join("%s %.2f" % kv for kv in low_front[:8])) if low_front else "", len(other), min([float(vis[i]) for i in other] or [0]), len(low), (": " + ", ".join("%s %.2f" % kv for kv in low[:8])) if low else ""))
    # DSP-04
    L = di["length_m"]
    out, ok = [], True
    if ctx().id == "ritas":
        tier_spans = (("bed", (-L / 2 + 0.14, -L / 2 + 3.20)), ("step", tuple(di["tiers"]["step"]["u"])), ("middle", tuple(di["tiers"]["middle"]["u"])), ("top", tuple(di["tiers"]["top"]["u"])))
    else:
        # batch A: the bed along the whole window zone less 0.10 at each end (the return walls' corners), and any tier the shop's display records
        tier_spans = (("bed", (-L / 2 + 0.10, L / 2 - 0.10)),) + tuple((k, tuple(v["u"])) for k, v in di["tiers"].items() if k != "bed")
    for tier, span in tier_spans:
        iv = []
        for it in di["items"]:
            if it["tier"] == tier and not (tier == "bed" and it["ext"][5] > 0.011 and False):
                iv.append((it["ext"][0], it["ext"][1]))
        if tier == "bed":
            for sc_ in di["scripted"]:
                iv.append((sc_["u"][0] - L / 2, sc_["u"][1] - L / 2))
        iv.sort()
        cur = span[0]
        worst = 0.0
        for (a, b) in iv:
            if a > cur:
                worst = max(worst, a - cur)
            cur = max(cur, b)
        if cur < span[1]:
            worst = max(worst, span[1] - cur)
        ok &= worst <= 0.20 + 1e-9
        out.append("%s %.3f m (%d pieces)" % (tier, worst, len(iv)))
    rows.add("DSP-04", "no free run along a tier over 0.20 m", ok, ("the longest stretch of the bed's front strip (u 0.14 to 3.20), the step and each tier with nothing on it: " if ctx().id == "ritas" else "the longest stretch of the bed (the window's length less 0.10 at each end) and of each tier with nothing on it (the crates and trays count as what stands there): ") + "; ".join(out) + " (limit 0.20)")


def visibility(R, work, assets, di, group_of):
    """Per camera (STREET_SQUARE, CLOSE_35, CLOSE_35_B), per group, the share of its silhouette that an object-index render shows (and, under "areas", the silhouette in pixels)."""
    import bpy
    import mathutils
    res = (1920, 1080)                    # thin pieces (the spectacles' rims) are under a pixel wide at 1280
    per_cam = {}
    areas = {}
    for cam in ("STREET_SQUARE", "CLOSE_35", "CLOSE_35_B"):
        best = np.zeros(len(di["groups"]))
        per_cam[cam] = best
        areas[cam] = np.zeros(len(di["groups"]))
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        disp = load_glb_objects(display_glb(assets))
        front = load_glb_objects(front_glb(assets))
        for o in disp:
            if o.type == "MESH":
                o.location += mathutils.Vector((ctx().window_cx_m, -0.025, 0.600)) if o.parent is None else mathutils.Vector()
        deps0 = bpy.context.evaluated_depsgraph_get()

        def flat(c):
            m = bpy.data.materials.new("flat")
            m.use_nodes = True
            t = m.node_tree
            for n in list(t.nodes):
                t.nodes.remove(n)
            e = t.nodes.new("ShaderNodeEmission")
            e.inputs["Color"].default_value = (*c, 1.0)
            o2 = t.nodes.new("ShaderNodeOutputMaterial")
            t.links.new(e.outputs[0], o2.inputs[0])
            return m
        cols = {}
        for gi in range(len(di["groups"])):
            cols[gi] = ((gi + 1) % 17 / 17.0 + 0.03, ((gi + 1) // 17) % 17 / 17.0 + 0.03, ((gi + 1) // 289) % 17 / 17.0 + 0.03)
        mats = {gi: flat(c) for gi, c in cols.items()}
        black = flat((0, 0, 0))
        sil_tris = {gi: [] for gi in range(len(di["groups"]))}
        for o in disp:
            if o.type != "MESH":
                continue
            gi = group_of.get(o.name)
            o.data = o.data.copy()          # two copies of one model share a mesh in the glb: each needs its own to take its own colour
            o.data.materials.clear()
            o.data.materials.append(mats[gi] if gi is not None else black)
        for o in list(front):
            if o.type != "MESH":
                continue
            low = o.name.lower()
            if "glass" in low or o.name.startswith(("glass_row", "door_sign", "sign_")):
                bpy.data.objects.remove(o, do_unlink=True)
                continue
            o.data.materials.clear()
            o.data.materials.append(black)
        cd = R["cameras"][cam]
        eye = to_model(cd["eye_street_m"])
        aim = to_model(cd["aim_street_m"])
        cam_d = bpy.data.cameras.new("cam")
        cam_d.sensor_fit = "VERTICAL"
        cam_d.angle_y = math.radians(G.VFOV[cam])
        cam_d.clip_start = 0.05
        co = bpy.data.objects.new("cam", cam_d)
        sc.collection.objects.link(co)
        co.location = mathutils.Vector(eye)
        co.rotation_euler = (mathutils.Vector(aim) - mathutils.Vector(eye)).to_track_quat("-Z", "Y").to_euler()
        sc.camera = co
        w = bpy.data.worlds.new("w")
        sc.world = w
        w.use_nodes = True
        w.node_tree.nodes["Background"].inputs["Color"].default_value = (0, 0, 0, 1)
        w.node_tree.nodes["Background"].inputs["Strength"].default_value = 0.0
        sc.render.engine = "CYCLES"
        sc.cycles.device = "CPU"
        sc.cycles.samples = 1
        sc.cycles.use_denoising = False
        sc.cycles.use_adaptive_sampling = False
        sc.cycles.filter_width = 0.01
        sc.view_settings.view_transform = "Raw"
        sc.view_settings.look = "None"
        sc.render.resolution_x, sc.render.resolution_y = res
        sc.render.resolution_percentage = 100
        bpy.context.view_layer.update()
        path = os.path.join(work, "gate", "check_%s_object_index.png" % cam)
        sc.render.filepath = path
        sc.render.image_settings.file_format = "PNG"
        sc.render.image_settings.color_mode = "RGB"
        sc.render.image_settings.color_depth = "8"
        bpy.ops.render.render(write_still=True)
        img = np.asarray(Image.open(path).convert("RGB")).astype(np.float32) / 255.0
        # each piece's whole silhouette: the same render with only that piece drawn (white), so that the visible share and the silhouette are counted by the same rasteriser
        white = flat((1, 1, 1))
        all_disp = [o for o in disp if o.type == "MESH"]
        for gi, g in enumerate(di["groups"]):
            if g["kind"] not in ("piece", "scripted"):          # (13 Oct: the front row's trays, pads and chains are tested too: street review 3)
                continue
            names = set(g["objs"])
            for o in bpy.data.objects:
                if o.type == "MESH":
                    o.hide_render = o.name not in names
            for nm in names:
                ob = bpy.data.objects.get(nm)
                if ob is not None:
                    ob.data.materials.clear()
                    ob.data.materials.append(white)
            sp = os.path.join(work, "gate", "check_silhouette_tmp.png")
            sc.render.filepath = sp
            bpy.ops.render.render(write_still=True)
            sil = np.asarray(Image.open(sp).convert("L")) > 128
            area = int(sil.sum())
            for nm in names:
                ob = bpy.data.objects.get(nm)
                if ob is not None:
                    ob.data.materials.clear()
                    ob.data.materials.append(mats[gi])
            c = np.array(cols[gi])
            vis = int((np.abs(img - c[None, None, :]).max(axis=2) < 0.02).sum())
            areas[cam][gi] = area
            if area > 20:
                best[gi] = max(best[gi], min(1.0, vis / float(area)))
        for o in bpy.data.objects:
            if o.type == "MESH":
                o.hide_render = False
    per_cam["areas"] = areas
    return per_cam


def gate_frame_rows(R, work, rows):
    """PIC-05g (close fault 4): the gate's rendered review frames, at most 1 per cent of the pixels at 250 or above."""
    gate = os.path.join(work, "gate")
    det, ok = [], True
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        for st in ("day", "night_lit"):
            p = os.path.join(gate, "%s_%s.png" % (cam, st))
            if not os.path.exists(p):
                continue
            a = np.asarray(Image.open(p).convert("RGB"))
            share = float((a.max(axis=2) >= 250).mean())
            ok &= share <= 0.01
            det.append("%s %s %.4f" % (cam, st, share))
    rows.add("PIC-05g", "nothing burnt in the gate's frames", ok, "share of pixels with a channel at 250 or above in the eight rendered frames (limit 0.01; try 1: night frames 0.033 and 0.031): " + ", ".join(det))


def glass_zone_mask(R, cam, state, work, res=CHECK_RES, which="mask"):
    p = os.path.join(work, "gate", "check_%s_%s_%s.png" % (cam, state, which))
    return np.asarray(Image.open(p).convert("L")) > 128


def lit02b_rows(R, work, rows):
    """LIT-02b (close review fault 3c; try 2 narrow points: street 6, close 8): the rendered frames with the glass's reflection off, window-glass pixels under luma 12 where the glass shows the
    ROOM (the card, the reveals, the display's return walls). A black slab is one big patch (try 1's was about a third of the window); the room's own shade under the shelves, seen through the day
    card's 0.15, is a scatter of small ones (STREET_30 by day: 1.13 per cent of the glass in all, the largest patch 0.63). So at the two STREET cameras the limit is on the LARGEST CONNECTED
    patch (the dark room pixels dilated by 2 px, as the row measured it): at most 1 per cent of the glass. At CLOSE_35_B, the camera of the slab the row was written for, both limits hold: the
    share of the glass at most 1 per cent AND the largest patch at most 1 per cent. CLOSE_35 is reported. The display's own dark things (black plastic, velvet at night, the shade under a tier)
    are not a void; the share over ALL the window-glass pixels is written beside it."""
    det, ok = [], True
    for cam in ("CLOSE_35_B", "STREET_30", "STREET_SQUARE", "CLOSE_35"):
        for st in ("day", "night_lit"):
            pb = os.path.join(work, "gate", "check_%s_%s_norefl.png" % (cam, st))
            pm = os.path.join(work, "gate", "check_%s_%s_mask.png" % (cam, st))
            pr = os.path.join(work, "gate", "check_%s_%s_room.png" % (cam, st))
            if not (os.path.exists(pb) and os.path.exists(pm) and os.path.exists(pr)):
                continue
            im = np.asarray(Image.open(pb).convert("RGB")).astype(np.float32)
            mk = np.asarray(Image.open(pm).convert("L")) > 128
            rm = np.asarray(Image.open(pr).convert("RGB")).astype(np.float32)
            room = (rm[..., 0] > 128) & (rm[..., 2] < 128) & mk
            n = int(mk.sum())
            lum = luma(im)
            dark = lum < 12
            share_room = float((dark & room).sum()) / max(n, 1)
            share_all = float((dark & mk).sum()) / max(n, 1)
            # the largest connected patch of those dark room pixels (a slab is one patch; the brown dado seen at the day card's 0.15 is a scatter of small ones)
            from scipy import ndimage as _nd
            lab, nl = _nd.label(_nd.binary_dilation(dark & room, iterations=2))
            big = float(max(_nd.sum(dark & room, lab, range(1, nl + 1)))) / max(n, 1) if nl else 0.0
            good_share, good_slab = share_room <= 0.01, big <= 0.01
            if cam == "CLOSE_35_B":
                ok &= good_share and good_slab
                tested = "share and patch"
            elif cam in ("STREET_30", "STREET_SQUARE"):
                ok &= good_slab
                tested = "patch"
            else:
                tested = "reported"
            det.append("%s %s: room share %.4f (of %d glass px, the room shows in %.0f per cent of them), largest patch %.4f, all glass %.4f [%s%s]" % (
                cam, st, share_room, n, 100.0 * float(room.sum()) / max(n, 1), big, share_all, tested, "" if (good_slab and (good_share or cam != "CLOSE_35_B")) else ": OVER 1 per cent"))
    rows.add("LIT-02b", "no black void in the rendered frames", ok, "window-glass pixels (the glass mask: no frame, mullion, bead or lattice) under luma 12, in frames rendered with the glass's reflection off, where the glass shows the room: " + "; ".join(det) + " (limits: 0.01 on the largest patch at STREET_SQUARE and STREET_30, 0.01 on both the share and the patch at CLOSE_35_B; try 1's black slab at CLOSE_35_B's far light was about a third of the window)")


def night_rows(R, work, rows, spill_w):
    """LIT-05 on the glass only, and LIT-07 (the review's three conditions)."""
    gate = os.path.join(work, "gate")
    c_ = ctx()
    win_x = ((c_.window_u[0] - 3000.0) / 1000.0, (c_.window_u[1] - 3000.0) / 1000.0)       # Rita's (-0.70, 2.65)
    mem = json.load(open(os.path.join(work, "front_members.json")))["members"]
    mull_us = [(3386.7, 3456.7), (4493.3, 4563.3)] if c_.id == "ritas" else [(v["u"][0], v["u"][1]) for k, v in sorted(mem.items()) if k.startswith("win_mullion_")]
    mull_d = 0.092 if c_.id == "ritas" else max([v["d"][1] for k, v in mem.items() if k.startswith("win_mullion_")] or [92.0]) / 1000.0
    head_z0 = 2.25 if c_.id == "ritas" else (mem["win_transom"]["z"][0] / 1000.0 - 0.15 if "win_transom" in mem else 2.25)
    res = (2560, 1440)
    out05 = {}
    res_cond = {}
    for cam in ("STREET_SQUARE", "STREET_30"):
        p = os.path.join(gate, "%s_night_lit.png" % cam)
        if not os.path.exists(p):
            continue
        im = np.asarray(Image.open(p).convert("RGB")).astype(np.float32)
        res = (im.shape[1], im.shape[0])
        lum = luma(im)
        cp = cam_params(R, cam, res)
        # the display zone: z 0.60 to 1.45 above the footway across the window zone, at the glass (d 33)
        zone = np.array([[win_x[0], -0.033, 0.60], [win_x[1], -0.033, 0.60], [win_x[1], -0.033, 1.45], [win_x[0], -0.033, 1.45]])
        zx, zy, _ = project_np(cp, zone)
        zm = Image.new("L", res, 0)
        ImageDraw.Draw(zm).polygon(list(zip(zx, zy)), fill=255)
        zone_m = np.asarray(zm) > 0
        # the glass masks (render at 1280 x 720, scaled up): with the lattice (it is in front of the glass at night: the masked frame leaves it out) and without
        gm = np.asarray(Image.open(os.path.join(gate, "check_%s_night_lit_mask.png" % cam)).convert("L").resize(res, Image.NEAREST)) > 128
        gm_open = None
        po = os.path.join(gate, "check_%s_night_lit_maskopen.png" % cam)
        if os.path.exists(po):
            gm_open = np.asarray(Image.open(po).convert("L").resize(res, Image.NEAREST)) > 128
        glass_only = float(lum[zone_m & gm].mean()) if (zone_m & gm).any() else 0.0
        glass_with_lattice = float(lum[zone_m & gm_open].mean()) if gm_open is not None and (zone_m & gm_open).any() else None
        out05[cam] = (glass_only, glass_with_lattice, int((zone_m & gm).sum()))
        # the head band: z 2.25 to 2.39 across the window zone
        hb = np.array([[win_x[0], -0.033, head_z0], [win_x[1], -0.033, head_z0], [win_x[1], -0.033, head_z0 + 0.14], [win_x[0], -0.033, head_z0 + 0.14]])
        hx, hy, _ = project_np(cp, hb)
        hm = Image.new("L", res, 0)
        ImageDraw.Draw(hm).polygon(list(zip(hx, hy)), fill=255)
        head = np.asarray(hm) > 0
        head_burnt = float((im.max(axis=2)[head] >= 250).mean())
        # the mullion fronts (u 3386.7 to 3456.7 and 4493.3 to 4563.3, front face d 92, z 700 to 1400)
        mull_vals = []
        for (ua, ub) in mull_us:
            q = np.array([[(ua - 3000) / 1000.0, -mull_d, 0.70], [(ub - 3000) / 1000.0, -mull_d, 0.70], [(ub - 3000) / 1000.0, -mull_d, 1.40], [(ua - 3000) / 1000.0, -mull_d, 1.40]])
            qx, qy, _ = project_np(cp, q)
            qm = Image.new("L", res, 0)
            ImageDraw.Draw(qm).polygon(list(zip(qx, qy)), fill=255)
            mull_vals.append(np.asarray(qm) > 0)
        if mull_vals:
            mm = mull_vals[0]
            for _m in mull_vals[1:]:
                mm = mm | _m
            mull = float(lum[mm].mean())
            mull_p95 = float(np.percentile(lum[mm], 95))
        else:
            mull, mull_p95 = 0.0, 0.0           # a window without a mullion: nothing to read
        # the pavement pool in front of the window: the review's box (x 860 to 1760, y 1075 to 1145 at STREET_SQUARE; the same ground patch at STREET_30)
        pav = np.array([[win_x[0], -0.60, 0.0], [win_x[1], -0.60, 0.0], [win_x[1], -1.20, 0.0], [win_x[0], -1.20, 0.0]])
        px_, py_, _ = project_np(cp, pav)
        pm_ = Image.new("L", res, 0)
        ImageDraw.Draw(pm_).polygon(list(zip(px_, py_)), fill=255)
        pool = float(lum[np.asarray(pm_) > 0].mean())
        res_cond[cam] = {"head_burnt": head_burnt, "mullion": mull, "mullion_p95": mull_p95, "glass": glass_only, "pool": pool}
    if "STREET_SQUARE" in out05:
        a, b, n = out05["STREET_SQUARE"]
        ok05 = a >= 45          # "on the glass only": the frame, mullions, beads AND the lattice's bars are not glass and stay out of the zone; the reading with the bars in is written beside it
        if ctx().has_grille:
            lat_txt = "With the lattice's bars in the zone, as the street sees the window all night, it reads %s: the bars are black and cover about 30 per cent of it (a known shortfall: the room behind is lit as the approved night shot is)." % (("%.1f" % b) if b is not None else "?")
        else:
            lat_txt = "The shop has no night grille: the glass is what the street sees."
        rows.add("LIT-05", "the display is lit at night", ok05,
                 "STREET_SQUARE at night, on the GLASS ONLY as the review words it (the mullions, the frame and the beads are not glass and are masked out): the display zone (z 0.60 to 1.45 above the footway across the window zone, %d glass px) mean luma %.1f (at least 45; Rita's try 1 measured 45.4 with the glowing mullions inside its zone). %s The spill is the gate's stand-in (a rect light 0.10 behind the wall face at z 2.30, %s Blender watts, invisible to the camera, on the display's channel and the gate's footway): Lumen's own light on the display is owed on the PC (PC-02)"
                 % (n, a, lat_txt, spill_w))
    det, ok = [], True
    for cam, c in res_cond.items():
        c1 = c["head_burnt"] < 0.01
        c2 = c["mullion"] < c["glass"]
        ok &= c1 and c2
        det.append("%s: head band at 250 or above %.4f (under 0.01) %s; mullion fronts %.1f (p95 %.1f) against the glass %.1f %s; the pavement pool in front of the window %.1f (written, not a condition: see below)" % (
            cam, c["head_burnt"], "ok" if c1 else "FAIL", c["mullion"], c["mullion_p95"], c["glass"], "ok" if c2 else "FAIL", c["pool"]))
    rows.add("LIT-07", "the night spill stays behind the glass", ok and bool(res_cond), "; ".join(det) + " (try 1: head band 0.32 and 0.35, mullion fronts p95 228, pavement 113 against the glass 66.8). The third condition (the pavement pool no brighter than the lit glass) is STRUCK (13 Oct, from the try 2 street review, 5: it compared a pale pavement with a window whose glass shows dark velvet and black plastic and could not be met by any spill that lights the bed through the glass); the gate's footway is on the spill's channel again, so the pool is the gate's stand-in and the game's own is owed (PC-02)")


def board_rows(R, work, rows):
    placed = json.load(open(os.path.join(work, "rooms", "placed.json")))
    fixtures = json.load(open(os.path.join(work, "rooms", "fixtures.json")))
    scales = []
    sized = {g["model"] for g in R["room"]["goods"] if g.get("size_m")}
    bad = []
    for p in placed:
        if p["fixture"] in ("R-back-stock", "R-back-tv-tiers") and p["model"] != "television_02":
            s = p["scale"]
            if p["model"] in sized:
                continue
            scales.append(s)
            if not (0.9 - 1e-3 <= s <= 1.1 + 1e-3):
                bad.append((p["model"], s))
    tv = [p["scale"] for p in placed if p["model"] == "television_02"]
    rows.add("SO-06", "the stock wall's scales", not bad and all(abs(t - 1.0) < 1e-3 for t in tv),
             "%d stock pieces (the boxes and the clock carry their own sizes from the target: %s) at scales %.3f to %.3f (limit 0.9 to 1.1; try 1: 0.45 to 1.45); the %d television sets at %s%s"
             % (len(scales), ", ".join(sorted(sized)), min(scales or [0]), max(scales or [0]), len(tv), sorted(set(tv)), ("; OVER: %s" % bad[:5]) if bad else ""))

    def cover(fixture, y_rng, z_rng):
        area = (y_rng[1] - y_rng[0]) * (z_rng[1] - z_rng[0])
        tot = 0.0
        for it in placed + fixtures:
            if it.get("fixture") != fixture:
                continue
            if "boxes_yz" in it:
                boxes = it["boxes_yz"]
            elif "box_yz" in it:
                boxes = [it["box_yz"][:2] + it["box_yz"][2:]]
                boxes = [[it["box_yz"][0], it["box_yz"][1], it["box_yz"][2], it["box_yz"][3]]]
            elif "model" in it:
                e = it["ext"]
                boxes = [[e[2], e[3], e[4], e[5]]]
            else:
                continue
            for (a, b, c, d) in boxes:
                a, b = max(a, y_rng[0]), min(b, y_rng[1])
                c, d = max(c, z_rng[0]), min(d, z_rng[1])
                if b > a and d > c:
                    tot += (b - a) * (d - c)
        return tot / area, tot
    cl, tl = cover("R-left-board", (0.3, 4.2), (0.45, 2.15))
    cr, tr = cover("R-right-board", (1.3, 4.2), (0.45, 2.15))
    rows.add("ROOM-01", "the left board is covered", cl >= 0.60, "the left board (y 0.3 to 4.2, z 0.45 to 2.15, 6.63 m2): goods at real size cover %.0f per cent by bounding box (%.2f m2; at least 60 per cent)" % (100 * cl, tl))
    # ROOM-02 (13 Oct, from the try 2 close review, 6): an area share by bounding box does not measure slim tools, so each ROW is measured: the tools of a row (placed with the row's tag) as intervals along
    # the board (y), each widened by 0.03 (the rows' gaps are 0.04 to 0.06, so a gap of 0.06 or less counts as filled), their union at least 80 per cent of the board's 2.9 m
    out, ok2, ntools = [], True, 0
    for tag_, band in (("R1", "saws z 1.85 to 2.10"), ("R2", "hammers and pipe wrenches 1.40 to 1.80"), ("R3", "pliers and adjustable wrenches 0.95 to 1.35"), ("R4", "combination wrenches and planes 0.50 to 0.90")):
        iv = sorted((max(q["ext"][2] - 0.03, 1.3), min(q["ext"][3] + 0.03, 4.2)) for q in placed if q.get("tag") == tag_ and q["fixture"] == "R-right-board")
        cur, tot = 1.3, 0.0
        for a, b in iv:
            a = max(a, cur)
            if b > a:
                tot += b - a
                cur = b
        sc_ = [q["scale"] for q in placed if q.get("tag") == tag_]
        gaps = [iv[k + 1][0] + 0.03 - (iv[k][1] - 0.03) for k in range(len(iv) - 1)]
        frac = tot / 2.9
        ntools += len(iv)
        ok2 &= frac >= 0.80 and bool(iv) and (not sc_ or min(sc_) >= 0.9 - 1e-3) and (not gaps or (min(gaps) >= 0.04 - 1e-3 and max(gaps) <= 0.06 + 1e-3))
        out.append("%s (%s): %d tools, %.0f per cent of the width, gaps %.3f to %.3f, scales %.2f to %.2f" % (tag_, band, len(iv), 100 * frac, min(gaps or [0]), max(gaps or [0]), min(sc_ or [0]), max(sc_ or [0])))
    rows.add("ROOM-02", "the right board is covered", ok2, "by rows, each tool's interval along the board widened by 0.03, the union against the board's 2.9 m (at least 80 per cent), gaps 0.04 to 0.06, scales 0.9 to 1.0: " + "; ".join(out) + "; %d tools (the review: about 60); the area share by bounding box, for the record: %.0f per cent (try 2: 18)" % (ntools, 100 * cr))
    # ROOM-03: the risers and the boxes on the sets
    rs = [f for f in fixtures if f.get("name", "").startswith("riser_")]
    det3, tot_len, tot_fill, ok3 = [], 0.0, 0.0, bool(rs)
    for f in rs:
        e = f["ext"]
        zt = e[5]
        ln = e[1] - e[0]
        ws = [(q["ext"][0], q["ext"][1]) for q in placed if q["fixture"] == "R-back-stock" and abs(q["ext"][4] - zt) < 1e-3 and q["ext"][0] >= e[0] - 0.01 and q["ext"][1] <= e[1] + 0.01 and q["model"] != "cardboard_box_01"]
        w = sum(b - a for a, b in ws)
        tot_len += ln
        tot_fill += w
        sc_ = [q["scale"] for q in placed if q["fixture"] == "R-back-stock" and abs(q["ext"][4] - zt) < 1e-3 and q["ext"][0] >= e[0] - 0.01 and q["ext"][1] <= e[1] + 0.01]
        dims_ok = abs((e[3] - e[2]) - 0.195) < 0.006 and abs(zt - (e[5] - 0.0)) < 1e-6
        det3.append("z %.2f x %.2f to %.2f: %d pieces, %.0f per cent" % (zt - RISER_H, e[0], e[1], len(ws), 100 * w / ln if ln else 0))
        ok3 &= (w / ln >= 0.70 if ln else False) and dims_ok and (not sc_ or min(sc_) >= 0.9 - 1e-3)
    boxes_on_tv = [q for q in placed if q["model"] == "cardboard_box_01" and q["fixture"] == "R-back-stock" and q["ext"][4] > 2.15]
    ok3 &= (tot_fill / tot_len >= 0.80 if tot_len else False) and len(boxes_on_tv) == 2
    rows.add("ROOM-03", "the risers and the boxes on the sets", ok3, "%d riser shelves (0.20 above their television board, 0.195 deep): %s; overall %.0f per cent of %.2f m (at least 80, each at least 70); %d cardboard boxes on top of the upper sets (2 wanted), the stock wall's pieces at scale 0.9 to 1.0; the review: 'about 14 more pieces': %d stock pieces now against 33 in try 2" % (
        len(rs), "; ".join(det3), 100 * tot_fill / tot_len if tot_len else 0, tot_len, len(boxes_on_tv), sum(1 for q in placed if q["fixture"] in ("R-back-stock", "R-back-tv-tiers") and q["model"] != "television_02")))
    # ROOM-04: the left board's clocks
    ck = [q for q in placed if q["model"] == "wall_clock" and q["fixture"] == "R-left-board"]
    zs = sorted(q["ext"][4] / 2 + q["ext"][5] / 2 for q in ck)
    rowA = [z for z in zs if z < 1.72]
    rowB = [z for z in zs if z >= 1.72]
    times = [tuple(q["clock"]) if q.get("clock") else None for q in ck]
    ys = sorted((q["ext"][2] + q["ext"][3]) / 2 for q in ck)
    # never more than three in a line: no three at one z within 0.05 beyond rows of three; neighbours in different rows clear each other
    ok4 = (len(ck) == 6 and len(rowA) == 3 and len(rowB) == 3 and all(1.55 - 0.001 <= z <= 1.60 + 0.001 for z in rowA) and all(1.83 - 0.001 <= z <= 1.88 + 0.001 for z in rowB)
           and len({(t_[0], t_[1]) for t_ in times if t_}) == 6 and all(0.9 - 1e-3 <= q["scale"] <= 1.0 + 1e-3 for q in ck))
    rows.add("ROOM-04", "the left board's six clocks", ok4, "%d wall clocks on the left board: z of the centres %s (two rows: z 1.55 to 1.60 and 1.83 to 1.88, three in each); y %s; the times shown %s (all different); scale 1.0" % (
        len(ck), [round(z, 3) for z in zs], [round(y, 2) for y in ys], ["%d:%02d" % (t_[0], t_[1]) for t_ in times if t_]))


# ------------------------------------------------------------------------------------------------------------------------- 13 Oct, from the try 2 reviews
RISER_H = 0.20


def so07_rows(work, rows, tol=0.002):
    """SO-07 (close review 5): no mesh of the room intersects another, 2 mm tolerance (each mesh inset 1 mm along its normals, or less on a thin one, then a BVH overlap, as DSP-03 does for the display).
    The room is rebuilt here from the same script and target (seconds); a piece's own meshes (its hands, its lens) do not count against each other."""
    import bpy
    from mathutils.bvhtree import BVHTree
    if ctx().id == "ritas":
        import sw_room as S
        r = S.build_scene(os.path.join(work, "rooms_check"))
    else:
        import sw_room_gen as RG
        r = RG.build_scene(os.path.join(work, "rooms_check"), ctx())
    deps = bpy.context.evaluated_depsgraph_get()
    group_of = {}
    for gi, q in enumerate(r.placed):
        for nm in q["objs"]:
            group_of[nm] = gi
    data = {}
    for ob in bpy.data.objects:
        if ob.type != "MESH" or r.coll_t in ob.users_collection or ob.hide_render:
            continue
        V, T, N = mesh_world(ob, deps)
        if len(V) == 0 or len(T) == 0:
            continue
        lo, hi = V.min(axis=0), V.max(axis=0)
        inset = min(0.001, 0.2 * float((hi - lo).min()) / 2.0)
        Ne = N / np.maximum(np.linalg.norm(N, axis=1, keepdims=True), 1e-9)
        data[ob.name] = {"lo": lo, "hi": hi, "bvh": BVHTree.FromPolygons((V - Ne * inset).tolist(), T.tolist(), epsilon=0.0)}
    names = sorted(data)
    bad, pairs = [], 0
    for i in range(len(names)):
        a = data[names[i]]
        for j in range(i + 1, len(names)):
            b = data[names[j]]
            if np.any(a["hi"] < b["lo"] + tol) or np.any(b["hi"] < a["lo"] + tol):
                continue
            ga, gb = group_of.get(names[i]), group_of.get(names[j])
            if ga is not None and ga == gb:
                continue
            pairs += 1
            if a["bvh"].overlap(b["bvh"]):
                bad.append((names[i], names[j]))

    def lab(n):
        g = group_of.get(n)
        return "%s(%s)" % (r.placed[g]["model"], n) if g is not None else n
    rows.add("SO-07", "no room mesh intersects another", not bad, "%d room meshes (fixtures, %d placed goods, tickets, notices), %d pairs with overlapping boxes tested (each mesh inset 1 mm, so a 2 mm contact is tolerated): %d pairs intersect%s (try 2: the till ran 0.12 m up through the z 1.35 board and the box on it)" % (
        len(names), len(r.placed), pairs, len(bad), (" (" + "; ".join("%s x %s" % (lab(a), lab(b)) for a, b in bad[:40]) + ")") if bad else ""))
    return r


def coplanar_front(glb, R, members, tol=0.5, min_area=1.0, ang=2.0):
    """The visible coplanar overlaps of the front's parts. Returns [(partA, partB, direction, plane mm, area mm2, viewpoints that see it)]."""
    import bpy
    from mathutils.bvhtree import BVHTree
    from shapely.geometry import Polygon
    from shapely.ops import unary_union
    from collections import defaultdict
    bpy.ops.wm.read_factory_settings(use_empty=True)
    objs = load_glb_objects(glb)
    deps = bpy.context.evaluated_depsgraph_get()
    dirs = {(0, 1): "+x", (0, -1): "-x", (1, 1): "+y", (1, -1): "-y (street)", (2, 1): "+z", (2, -1): "-z"}
    per = {k: [] for k in dirs}
    cosang = math.cos(math.radians(ang))
    verts, polys, owner = [], [], []
    off = 0
    f1 = {k for k, v in members.items() if v.get("group") == "side_door_F1"}
    for ob in objs:
        if ob.type != "MESH":
            continue
        V, T_, _ = mesh_world(ob, deps)
        V = V * 1000.0
        if len(T_) == 0:
            continue
        low = ob.name.lower()
        if not (low.startswith(("sign_", "glass_row", "door_sign", "grille_lattice")) or "glass" in low):
            verts.extend(V.tolist())
            polys.extend((T_ + off).tolist())
            owner.extend([ob.name] * len(T_))
            off += len(V)
        a, b, c = V[T_[:, 0]], V[T_[:, 1]], V[T_[:, 2]]
        n = np.cross(b - a, c - a)
        ln = np.linalg.norm(n, axis=1)
        okf = ln > 1e-9
        n = n / np.where(okf, ln, 1.0)[:, None]
        for ax in range(3):
            for sg in (1, -1):
                sel = okf & (n[:, ax] * sg >= cosang)
                other = [i for i in range(3) if i != ax]
                for ti in np.nonzero(sel)[0]:
                    pts = V[T_[ti]]
                    per[(ax, sg)].append((float(pts[:, ax].mean()), ob.name, pts[:, other]))
    bvh = BVHTree.FromPolygons(verts, polys, epsilon=1e-6)
    eyes = [np.array(to_model(R["cameras"][c]["eye_street_m"])) * 1000.0 for c in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B")]
    for xs in (-6, -3, 0, 3, 6):
        for ys in (-1.5, -4.0, -8.0):
            eyes.append(np.array([xs, ys, 1.5]) * 1000.0)       # model frame: y negative toward the street
    res = []
    for key, items in per.items():
        ax, sg = key
        other = [i for i in range(3) if i != ax]
        bk = defaultdict(list)
        for c, nm, p in items:
            bk[int(round(c / tol))].append((c, nm, p))
        seen = set()
        for b in sorted(bk):
            cand = bk[b] + bk.get(b + 1, [])
            by = defaultdict(list)
            for c, nm, p in cand:
                by[nm].append((c, p))
            if len(by) < 2:
                continue
            polysd = {}
            for nm in by:
                ps = [q for q in (Polygon(p) for c, p in by[nm]) if q.area > 1e-6]
                if ps:
                    polysd[nm] = (unary_union(ps), float(np.mean([c for c, p in by[nm]])))
            ns = sorted(polysd)
            for i in range(len(ns)):
                for j in range(i + 1, len(ns)):
                    if ns[i] in f1 and ns[j] in f1:
                        continue                              # the door family's own parts (F1 is kept as it was built and checked)
                    A_, B_ = polysd[ns[i]], polysd[ns[j]]
                    if abs(A_[1] - B_[1]) > tol or not A_[0].intersects(B_[0]):
                        continue
                    ov = A_[0].intersection(B_[0])
                    if ov.area <= min_area or (ns[i], ns[j], key) in seen:
                        continue
                    seen.add((ns[i], ns[j], key))
                    geoms = [g for g in (ov.geoms if hasattr(ov, "geoms") else [ov]) if g.area > 0.2]
                    samp = []
                    for g in geoms:
                        samp.append(g.representative_point())
                        c0 = g.centroid
                        if g.contains(c0):
                            samp.append(c0)
                    vis = 0
                    for sp in samp[:6]:
                        p = np.zeros(3)
                        p[other[0]] = sp.x
                        p[other[1]] = sp.y
                        p[ax] = A_[1] + sg * 0.3
                        for e in eyes:
                            d = e - p
                            if np.dot(d, np.eye(3)[ax] * sg) <= 0:
                                continue
                            dist = np.linalg.norm(d)
                            h = bvh.ray_cast(tuple(p), tuple(d / dist))
                            if h[0] is None or h[3] >= dist - 0.5:
                                vis += 1
                                break
                    res.append((ns[i], ns[j], dirs[key], round(A_[1], 2), round(ov.area, 1), vis))
    return res


def frn10_rows(R, work, assets, rows, members):
    """FRN-10 (street review 1, close review 2): (a) no two parts of the front share a face plane where a camera can see it; (b) in the day gate frames no pixel of the front is under luma 8."""
    glb = front_glb(assets)
    cop = coplanar_front(glb, R, members)
    vis = [c for c in cop if c[5]]
    det_a = "%d coplanar same-facing overlaps of more than 1 mm2 among the front's parts (hidden ones, behind the doors or inside the joinery: not a fault), %d of them where a camera can see them%s" % (
        len(cop), len(vis), (": " + "; ".join("%s x %s at %s %s (%s mm2)" % (a, b, d, pl, ar) for a, b, d, pl, ar, v in vis[:6])) if vis else "")
    gate = os.path.join(work, "gate")
    res = (2560, 1440)
    dark_tot, det_b, miss = 0, [], False
    from scipy import ndimage as _nd
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        pf = os.path.join(gate, "%s_day.png" % cam)
        pm = os.path.join(gate, "check_%s_day_frontmask.png" % cam)
        if not (os.path.exists(pf) and os.path.exists(pm)):
            miss = True
            continue
        im = np.asarray(Image.open(pf).convert("RGB")).astype(np.float32)
        mk = np.asarray(Image.open(pm).convert("L")) > 128
        if mk.shape != im.shape[:2]:
            mk = np.asarray(Image.open(pm).convert("L").resize((im.shape[1], im.shape[0]), Image.NEAREST)) > 128
        mk = _nd.binary_erosion(mk, iterations=2)               # an edge pixel is half something else
        lum = luma(im)
        dk = mk & (lum < 8)
        n_raw = int(dk.sum())
        # a black AREA is the fault (the strips beside the side door were 53 mm wide and 2.8 m high); a line of shade under the cornice or the sill (about 25 mm at STREET_SQUARE) is light and
        # shadow, not a missing face. Only dark patches that survive an opening by a square of 35 mm on the front count: k px at this camera (its focal length in px over its distance to the wall)
        cpar = cam_params(R, cam, (im.shape[1], im.shape[0]))
        k_px = max(5, int(round(0.035 * cpar["f"] / max(abs(float(cpar["eye"][1])), 0.5))))
        n = int(_nd.binary_opening(dk, structure=np.ones((k_px, k_px), bool)).sum())
        dark_tot += n
        det_b.append("%s %d of %d front pixels under luma 8, %d of them in patches %d px (35 mm) or wider (the darkest pixel %.1f)" % (cam, n_raw, int(mk.sum()), n, k_px, float(lum[mk].min()) if mk.any() else -1))
    rows.add("FRN-10", "no two parts of the front share a visible face plane; nothing on the front is black", not vis and dark_tot == 0 and not miss,
             det_a + ". By day, in the four gate frames at 2560 x 1440, over the front's own pixels (a mask render: the glass, the two fanlights, the shop door's glass, the hall, the lettering rows and the OPEN sign are not the front; the mask eroded by 2 px; a dark patch counts when it is 35 mm wide on the front or more, a thin line of shade under the cornice or the sill does not): " + "; ".join(det_b) +
             " (try 2: the two strips beside the side door were luma 0 to 3, about 12,000 pixels at STREET_SQUARE: F1's frame jambs, the added side jambs and the fillers stood in one plane, d 100)")


def glass_night_rows(R, work, rows):
    """GLS-03 (street review 2, close review 3): at night p95 of |frame - the render with the glass's reflection off| over the window's glass, at most 15 levels at every camera. The frame
    (2560 x 1440) is reduced to the check render's 1280 x 720 by averaging 2 x 2; luma; the glass mask is the check's own."""
    gate = os.path.join(work, "gate")
    det, ok, n = [], True, 0
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        pf = os.path.join(gate, "%s_night_lit.png" % cam)
        pn_full = os.path.join(gate, "check_%s_night_lit_norefl_full.png" % cam)
        pn = pn_full if os.path.exists(pn_full) else os.path.join(gate, "check_%s_night_lit_norefl.png" % cam)
        pm = os.path.join(gate, "check_%s_night_lit_mask.png" % cam)
        if not (os.path.exists(pf) and os.path.exists(pn) and os.path.exists(pm)):
            ok = False
            continue
        fr = np.asarray(Image.open(pf).convert("RGB")).astype(np.float32)
        nr = np.asarray(Image.open(pn).convert("RGB")).astype(np.float32)
        mk = np.asarray(Image.open(pm).convert("L")) > 128
        if nr.shape[:2] == fr.shape[:2]:
            # the same size and samples as the frame (check_*_norefl_full.png): compared pixel for pixel; the 1280 mask is taken up to the frame's size
            mk = np.asarray(Image.open(pm).convert("L").resize((fr.shape[1], fr.shape[0]), Image.NEAREST)) > 128
        else:
            # the 1280 x 720 render of the earlier checks: the frame is reduced by averaging 2 x 2
            h2, w2 = fr.shape[0] // 2, fr.shape[1] // 2
            fr = fr[:h2 * 2, :w2 * 2].reshape(h2, 2, w2, 2, 3).mean(axis=(1, 3))
            if nr.shape[:2] != fr.shape[:2]:
                nr = np.asarray(Image.open(pn).convert("RGB").resize((w2, h2), Image.BILINEAR)).astype(np.float32)
                mk = np.asarray(Image.open(pm).convert("L").resize((w2, h2), Image.NEAREST)) > 128
        from scipy import ndimage as _nd
        mk = _nd.binary_erosion(mk, iterations=4 if pn == pn_full else 2)               # the mask's edge pixels (the lattice's bars, the frame) are antialiased differently in a 2560 frame reduced by 2 and a native 1280 render
        d = np.abs(luma(fr) - luma(nr))
        p95 = float(np.percentile(d[mk], 95)) if mk.any() else -1.0
        mean_d = float(d[mk].mean()) if mk.any() else -1.0
        ok &= 0 <= p95 <= 15.0
        n += 1
        det.append("%s p95 %.1f (mean %.1f, %d glass px)" % (cam, p95, mean_d, int(mk.sum())))
    rows.add("GLS-03", "the night glass does not double what is behind it", ok and n == 4, "at night, p95 of |gate frame minus the render with the glass's reflection off| (luma, levels), the frame against a render of the same size, samples and seed with the glass's reflection off, over the glass mask eroded by 2 px at 1280 (4 at 2560): " + "; ".join(det) +
             " (limit 15; try 2: 32.9 at STREET_30 and 17.2 at STREET_SQUARE: the stand-in glass mixed a Transparent and a Glass BSDF, which bent each ray at one face of the closed 6 mm slab and not the other, so everything behind it came two or three times; now a Glossy BSDF, GGX 0.02, weighted 0.2 x Fresnel at IOR 1.5, nothing refracted)")


def lit08_rows(R, work, rows):
    """LIT-08 (close review 1): at night_lit from CLOSE_35 and CLOSE_35_B, each display piece's mean luma over the lattice's gaps at least 0.6 of the room's mean luma seen round it. A piece's pixels
    are those an object-index render (the lattice drawn, the glass left out) shows as the piece; 'round it' is the ring of room pixels (the card, the reveals, the return walls) within 24 px of it."""
    from scipy import ndimage as _nd
    di = json.load(open(os.path.join(work, "display_work", "display_items.json")))
    gate = os.path.join(work, "gate")
    det, ok, worst_all = [], True, []
    for cam in ("CLOSE_35", "CLOSE_35_B"):
        pf = os.path.join(gate, "%s_night_lit.png" % cam)
        pp = os.path.join(gate, "check_%s_night_lit_pieces.png" % cam)
        if not (os.path.exists(pf) and os.path.exists(pp)):
            ok = False
            continue
        lum = luma(np.asarray(Image.open(pf).convert("RGB")).astype(np.float32))
        idx = np.asarray(Image.open(pp).convert("RGB")).astype(np.float32) / 255.0
        if idx.shape[:2] != lum.shape:
            idx = np.asarray(Image.open(pp).convert("RGB").resize((lum.shape[1], lum.shape[0]), Image.NEAREST)).astype(np.float32) / 255.0
        room = (idx.min(axis=2) > 0.985)
        res_ = []
        for gi, g in enumerate(di["groups"]):
            if g["kind"] not in ("piece", "scripted"):
                continue
            c = np.array(((gi + 1) % 17 / 17.0 + 0.03, ((gi + 1) // 17) % 17 / 17.0 + 0.03, ((gi + 1) // 289) % 17 / 17.0 + 0.03))
            m = np.abs(idx - c[None, None, :]).max(axis=2) < 0.012
            n = int(m.sum())
            if n < 60:
                continue
            ring = _nd.binary_dilation(m, iterations=24) & ~m & room
            if int(ring.sum()) < 150:
                continue
            res_.append((float(lum[m].mean()) / max(float(lum[ring].mean()), 1e-6), g["model"], float(lum[m].mean()), float(lum[ring].mean()), n))
        res_.sort()
        low = [r_ for r_ in res_ if r_[0] < 0.6]
        ok &= not low and bool(res_)
        worst_all += [(r_[0], cam, r_[1]) for r_ in res_[:3]]
        det.append("%s: %d pieces seen against the room, lowest ratio %s, %d under 0.6%s; median ratio %.2f" % (cam, len(res_), ", ".join("%s %.2f (%.0f against %.0f)" % (r_[1], r_[0], r_[2], r_[3]) for r_ in res_[:3]), len(low),
                                                                                                    (" (" + ", ".join("%s %.2f" % (r_[1], r_[0]) for r_ in low[:8]) + ")") if low else "", float(np.median([r_[0] for r_ in res_])) if res_ else 0.0))
    rows.add("LIT-08", "the display's goods are lit at night", ok, "at night_lit, each display piece's mean luma over the lattice's gaps against the room's mean luma in a 24 px ring round it: " + "; ".join(det) +
             " (limit 0.6; try 2, CLOSE_35_B: the alarm clock's dial 33 against a room of 95, the cassette player 26, the mantel clock 25; the two strip lights under the tier boards are the fix; PIC-05g stays at 0.01 or under)")


def manifest(HERE_, assets, work, out_path):
    files = []
    for nm in glbs_of(assets):
        files.append(os.path.join(assets, nm))
    if ctx().has_room:
        for st in ("day", "night_lit", "night_dark"):
            files.append(picture(work, st))
    out = {"made": __import__("time").strftime("%Y-%m-%d %H:%M:%S"), "what": "the files of the narrow-points build (13 Oct, from the try 2 reviews; v3); the three glbs and the three 4096 pictures are out of git (rebuilt by build_ritas.py) so this names the versions",
           "files": {}}
    for p in files:
        if os.path.exists(p):
            h = hashlib.sha256()
            with open(p, "rb") as f:
                for chunk in iter(lambda: f.read(1 << 20), b""):
                    h.update(chunk)
            out["files"][os.path.basename(p)] = {"bytes": os.path.getsize(p), "sha256": h.hexdigest()}
    json.dump(out, open(out_path, "w"), indent=1)
    return out
