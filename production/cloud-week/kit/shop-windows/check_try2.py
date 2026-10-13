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

CHECK_RES = (1280, 720)


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
    eye = np.array(G.to_model(cd["eye_street_m"]))
    aim = np.array(G.to_model(cd["aim_street_m"]))
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
    glb = os.path.join(assets, "ritas_front.glb")
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
    base = np.asarray(Image.open(os.path.join(work, "fascia_export", "ritas_basecolour_worn.png")).convert("RGB")).astype(np.float32)
    inside = (tu >= 0) & (tu < 5410) & (tv >= 0) & (tv < 550)
    tl = luma(base)
    # letters: the gilt of the name block (centre third of the board, texture luma well above the ground's), ground: the maroon (texture luma near the median)
    ti = np.clip(tu.astype(int), 0, 5409)
    tj = np.clip(tv.astype(int), 0, 549)
    tluma = tl[tj, ti]
    med = float(np.median(tl))
    sel_letters = inside & (tluma > med * 1.8) & (tu > 1500) & (tu < 3900)
    sel_ground = inside & (np.abs(tluma - med) < med * 0.25) & (tu > 400) & (tu < 5000)
    rl = luma(im.reshape(-1, 3).reshape(im.shape))[ys.ravel(), xs.ravel()]
    ground = float(rl[sel_ground].mean()) if sel_ground.any() else 0.0
    letters = float(np.percentile(rl[sel_letters], 75)) if sel_letters.any() else 0.0
    # the stallriser's panel (front face at d 135, u 2300..5650, z 0..525): its mean luma over the panel's middle band
    st = np.array([[(2400 - 3000) / 1000.0, -0.135, 0.45], [(5550 - 3000) / 1000.0, -0.135, 0.45], [(5550 - 3000) / 1000.0, -0.135, 0.10], [(2400 - 3000) / 1000.0, -0.135, 0.10]])
    sx_, sy_, _ = project_np(cp, st)
    mk = Image.new("L", res, 0)
    ImageDraw.Draw(mk).polygon(list(zip(sx_, sy_)), fill=255)
    smask = np.asarray(mk) > 0
    stall = float(luma(im)[smask].mean())
    ratio = ground / stall if stall else 0.0
    cl = letters / ground if ground else 0.0
    rows.add("FAS-01c", "the board reads by day", abs(ground - stall) / stall <= 0.15 and cl >= 2.0,
             "STREET_SQUARE by day: the board's ground luma %.1f against the stallriser's %.1f (%.0f per cent; within 15 per cent), the gilt letters (75th percentile of the lettering's pixels) %.1f: letters to ground %.2f (at least 2.0; try 1: 34.2 against 55.6 and 1.39)" % (ground, stall, 100.0 * ratio, letters, cl))


def glass_rows_check(R, work, assets, rows, members):
    """GLS-02: no ink pixel of a glass row lies behind a bar, mullion or bead at STREET_SQUARE and STREET_30 (a ray from the eye to each ink pixel meets nothing opaque first)."""
    bvh, owner = front_bvh(os.path.join(assets, "ritas_front.glb"))
    fasc = os.path.join(work, "fascias")
    man = json.load(open(os.path.join(fasc, "manifest.json")))
    out, ok = [], True
    for cam in ("STREET_SQUARE", "STREET_30"):
        cp = cam_params(R, cam)
        for g in man["glass_lettering"]:
            if g["shop"] != "ritas" or g["row"] not in (7, 8, 9):
                continue
            key = [k for k in members if k.startswith("glass_row_%d_" % g["row"])][0]
            mem = members[key]
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
    rows.add("GLS-02", "no glass row lies behind a bar, mullion or bead", ok, "a ray from the camera's eye to each ink point of WATCHES, JEWELLERY and LOANS (the row's alpha, every 2 mm) must meet no opaque part of the front first: " + "; ".join(out))


def hall_check(R, work, assets, rows, members):
    """FRN-09: through the side door's fanlight from STREET_SQUARE every ray meets the hall (or the door frame), none gets through to the room's card."""
    bvh, owner = front_bvh(os.path.join(assets, "ritas_front.glb"))
    cp = cam_params(R, "STREET_SQUARE")
    fl = R["door"]["fanlight"]
    us = np.linspace(fl["u_mm"][0] + 15, fl["u_mm"][1] - 15, 40) if False else np.linspace(450.0, 1200.0, 40)
    zs = np.linspace(2130.0, 2380.0, 14)
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
    for nm in ("ritas_front.glb", "ritas_grille_night.glb", "ritas_display.glb"):
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
    (the convex hull of its silhouette, eroded 3 px)."""
    import bpy
    import mathutils
    res = CHECK_RES
    out, ok = [], True
    for cam in ("STREET_SQUARE", "STREET_30", "CLOSE_35", "CLOSE_35_B"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        objs = load_glb_objects(os.path.join(assets, "ritas_front.glb"))
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
        eye = G.to_model(cd["eye_street_m"])
        aim = G.to_model(cd["aim_street_m"])
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
        hull = silhouette_hull(front)
        hull = ndimage.binary_erosion(hull, iterations=3)
        holes = white & hull
        n_holes = int(holes.sum())
        lab, nl = ndimage.label(holes)
        big = int(np.bincount(lab.ravel())[1:].max()) if nl else 0
        ok &= n_holes == 0
        out.append("%s %d px (largest %d)" % (cam, n_holes, big))
    rows.add("FRN-08", "no backdrop through the front", ok, "the front alone (glass opaque, no hanging sign) against a white emissive backdrop, 1280 x 720, from each review camera: backdrop pixels inside the front's outline (the convex hull of its silhouette, eroded 3 px): " + "; ".join(out) + " (none allowed)")
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
    objs = load_glb_objects(os.path.join(assets, "ritas_display.glb"))
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
    vis = visibility(R, work, assets, di, group_of)
    low = [(g["model"], round(v, 2)) for g, v in zip(di["groups"], vis) if g["kind"] == "piece" and v < 0.5]
    rows.add("DSP-03", "no display mesh intersects another; every piece shows", not bad and not low,
             "%d display meshes, %d pairs with overlapping boxes tested (each mesh inset 1 mm, so a 2 mm contact is tolerated): %d pairs intersect%s; the share of each piece's silhouette seen from CLOSE_35 or STREET_SQUARE (an object-index pass, the frame's bars and the other pieces in front): %d pieces, lowest %.2f, %d under 0.5%s"
             % (len(names), pairs, len(bad), (" (" + "; ".join("%s x %s" % (a, b) for a, b, _ in bad_l[:8]) + ")") if bad else "", sum(1 for g in di["groups"] if g["kind"] == "piece"),
                min([v for g, v in zip(di["groups"], vis) if g["kind"] == "piece"] or [0]), len(low), (": " + ", ".join("%s %.2f" % kv for kv in low[:8])) if low else ""))
    # DSP-04
    L = di["length_m"]
    out, ok = [], True
    for tier, span in (("bed", (-L / 2 + 0.14, -L / 2 + 3.20)), ("step", tuple(di["tiers"]["step"]["u"])), ("middle", tuple(di["tiers"]["middle"]["u"])), ("top", tuple(di["tiers"]["top"]["u"]))):
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
    rows.add("DSP-04", "no free run along a tier over 0.20 m", ok, "the longest stretch of the bed's front strip (u 0.14 to 3.20), the step and each tier with nothing on it: " + "; ".join(out) + " (limit 0.20)")


def visibility(R, work, assets, di, group_of):
    """Per group, the best share over STREET_SQUARE and CLOSE_35 of its silhouette that an object-index render shows."""
    import bpy
    import mathutils
    res = CHECK_RES
    best = np.zeros(len(di["groups"]))
    for cam in ("STREET_SQUARE", "CLOSE_35"):
        bpy.ops.wm.read_factory_settings(use_empty=True)
        sc = bpy.context.scene
        disp = load_glb_objects(os.path.join(assets, "ritas_display.glb"))
        front = load_glb_objects(os.path.join(assets, "ritas_front.glb"))
        for o in disp:
            if o.type == "MESH":
                o.location += mathutils.Vector((0.975, -0.025, 0.600)) if o.parent is None else mathutils.Vector()
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
        eye = G.to_model(cd["eye_street_m"])
        aim = G.to_model(cd["aim_street_m"])
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
        cp = cam_params(R, cam, res)
        deps = bpy.context.evaluated_depsgraph_get()
        for gi, g in enumerate(di["groups"]):
            if g["kind"] != "piece":
                continue
            # silhouette area: every triangle of the group's meshes projected and filled
            m = Image.new("L", res, 0)
            dr = ImageDraw.Draw(m)
            for nm in g["objs"]:
                ob = bpy.data.objects.get(nm)
                if ob is None:
                    continue
                V, T, _ = mesh_world(ob, deps)
                x, y, z = project_np(cp, V)
                for t in T:
                    if (z[t] > 0.05).all():
                        dr.polygon([(x[t[0]], y[t[0]]), (x[t[1]], y[t[1]]), (x[t[2]], y[t[2]])], fill=255)
            area = int((np.asarray(m) > 0).sum())
            c = np.array(cols[gi])
            vis = int((np.abs(img - c[None, None, :]).max(axis=2) < 0.02).sum())
            if area > 20:
                best[gi] = max(best[gi], min(1.0, vis / float(area)))
    return best


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
    """LIT-02b: the rendered frames with the glass's reflection off: at most 1 per cent of the window-glass pixels under luma 12 (on the review's two cameras, CLOSE_35_B and STREET_30, both
    states; the other two are reported)."""
    det, ok = [], True
    for cam in ("CLOSE_35_B", "STREET_30", "STREET_SQUARE", "CLOSE_35"):
        for st in ("day", "night_lit"):
            pb = os.path.join(work, "gate", "check_%s_%s_norefl.png" % (cam, st))
            pm = os.path.join(work, "gate", "check_%s_%s_mask.png" % (cam, st))
            if not (os.path.exists(pb) and os.path.exists(pm)):
                continue
            im = np.asarray(Image.open(pb).convert("RGB")).astype(np.float32)
            mk = np.asarray(Image.open(pm).convert("L")) > 128
            n = int(mk.sum())
            share = float((luma(im)[mk] < 12).mean()) if n else 1.0
            good = share <= 0.01
            if cam in ("CLOSE_35_B", "STREET_30"):
                ok &= good
            det.append("%s %s %.4f of %d px%s" % (cam, st, share, n, "" if good else " (over 1 per cent)"))
    rows.add("LIT-02b", "no black void in the rendered frames", ok, "window-glass pixels (the glass mask render: no frame, mullion, bead or lattice) under luma 12 in the frames rendered with the glass's reflection off: " + "; ".join(det) + " (limit 0.01 on CLOSE_35_B and STREET_30; try 1's black slab at CLOSE_35_B's far light was about a third of the window)")


def night_rows(R, work, rows, spill_w):
    """LIT-05 on the glass only, and LIT-07 (the review's three conditions)."""
    gate = os.path.join(work, "gate")
    win_x = (-0.70, 2.65)
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
        hb = np.array([[win_x[0], -0.033, 2.25], [win_x[1], -0.033, 2.25], [win_x[1], -0.033, 2.39], [win_x[0], -0.033, 2.39]])
        hx, hy, _ = project_np(cp, hb)
        hm = Image.new("L", res, 0)
        ImageDraw.Draw(hm).polygon(list(zip(hx, hy)), fill=255)
        head = np.asarray(hm) > 0
        head_burnt = float((im.max(axis=2)[head] >= 250).mean())
        # the mullion fronts (u 3386.7 to 3456.7 and 4493.3 to 4563.3, front face d 92, z 700 to 1400)
        mull_vals = []
        for (ua, ub) in ((3386.7, 3456.7), (4493.3, 4563.3)):
            q = np.array([[(ua - 3000) / 1000.0, -0.092, 0.70], [(ub - 3000) / 1000.0, -0.092, 0.70], [(ub - 3000) / 1000.0, -0.092, 1.40], [(ua - 3000) / 1000.0, -0.092, 1.40]])
            qx, qy, _ = project_np(cp, q)
            qm = Image.new("L", res, 0)
            ImageDraw.Draw(qm).polygon(list(zip(qx, qy)), fill=255)
            mull_vals.append(np.asarray(qm) > 0)
        mm = mull_vals[0] | mull_vals[1]
        mull = float(lum[mm].mean())
        mull_p95 = float(np.percentile(lum[mm], 95))
        # the pavement pool in front of the window: the review's box (x 860 to 1760, y 1075 to 1145 at STREET_SQUARE; the same ground patch at STREET_30)
        pav = np.array([[win_x[0], -0.60, 0.0], [win_x[1], -0.60, 0.0], [win_x[1], -1.20, 0.0], [win_x[0], -1.20, 0.0]])
        px_, py_, _ = project_np(cp, pav)
        pm_ = Image.new("L", res, 0)
        ImageDraw.Draw(pm_).polygon(list(zip(px_, py_)), fill=255)
        pool = float(lum[np.asarray(pm_) > 0].mean())
        res_cond[cam] = {"head_burnt": head_burnt, "mullion": mull, "mullion_p95": mull_p95, "glass": glass_only, "pool": pool}
    if "STREET_SQUARE" in out05:
        a, b, n = out05["STREET_SQUARE"]
        ok05 = a >= 45 and (b is None or b >= 45)
        rows.add("LIT-05", "the display is lit at night", ok05,
                 "STREET_SQUARE at night, on the GLASS ONLY (the glass mask render leaves out the mullions, the frame, the beads and the lattice's bars): the display zone (z 0.60 to 1.45 above the footway across the window zone, %d glass px) mean luma %.1f%s (at least 45; try 1 measured 45.4 with the glowing mullions inside its zone). The spill is the gate's stand-in (a rect light 0.10 behind the wall face at z 2.30, %s Blender watts, invisible to the camera): Lumen's own light on the display is owed on the PC (PC-02)"
                 % (n, a, (", and %.1f with the lattice's gaps as the glass" % b) if b is not None else "", spill_w))
    det, ok = [], True
    for cam, c in res_cond.items():
        c1 = c["head_burnt"] < 0.01
        c2 = c["mullion"] < c["glass"]
        c3 = c["pool"] <= c["glass"]
        ok &= c1 and c2 and c3
        det.append("%s: head band at 250 or above %.4f (under 0.01) %s; mullion fronts %.1f (p95 %.1f) against the glass %.1f %s; pavement pool %.1f against the lit glass %.1f %s" % (
            cam, c["head_burnt"], "ok" if c1 else "FAIL", c["mullion"], c["mullion_p95"], c["glass"], "ok" if c2 else "FAIL", c["pool"], c["glass"], "ok" if c3 else "FAIL"))
    rows.add("LIT-07", "the night spill stays behind the glass", ok and bool(res_cond), "; ".join(det) + " (try 1: head band 0.32 and 0.35, mullion fronts p95 228, pavement 113 against the glass 66.8)")


def board_rows(R, work, rows):
    placed = json.load(open(os.path.join(work, "rooms", "placed.json")))
    fixtures = json.load(open(os.path.join(work, "rooms", "fixtures.json")))
    scales = []
    sized = {g["model"] for g in R["room"]["goods"] if g.get("size_m")}
    bad = []
    for p in placed:
        if p["fixture"] == "R-back-stock":
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
    rows.add("ROOM-02", "the right board is covered", cr >= 0.60, "the right board (y 1.3 to 4.2, z 0.45 to 2.15, 4.93 m2): the tools at real size with every count doubled, as the review words the fix, cover %.0f per cent by bounding box (%.2f m2; the review asks for 60 per cent: doubled counts of these tools cannot reach it)" % (100 * cr, tr))


def manifest(HERE_, assets, work, out_path):
    files = []
    for nm in ("ritas_front.glb", "ritas_grille_night.glb", "ritas_display.glb"):
        files.append(os.path.join(assets, nm))
    for st in ("day", "night_lit", "night_dark"):
        files.append(os.path.join(work, "rooms", "pawnbroker_%s.png" % st))
    out = {"made": __import__("time").strftime("%Y-%m-%d %H:%M:%S"), "what": "the files the try 2 reviews are to look at; the three glbs and the three 4096 pictures are out of git (rebuilt by build_ritas.py) so this names the versions",
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
