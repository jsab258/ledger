"""Parts of the front that belong to the shops of batch B (14 October 2026): the recessed lobby (the launderette's 300 and the grocer's 600), the tile and slab stallrisers' pictures, the lobby floors, the lit box
sign on the fascia and the hanging box of the launderette, the fish market's stowed awning. Functions take the Front (sw_front.Front) as `self` and are bound to it at the end of sw_front.py
(`lobby_*`, `extras_<id>`, `late_<id>`). Every number comes from target.json, the 3.2 kit's target (production/cloud-week/targets/shopfronts) or the 4.1 manifest; what they leave open is a Judgement named here and in NOTES.md.

Frame (millimetres): u from the viewer's LEFT across the bay, d out from the wall face toward the street, z above the footway; the model's x = (u - 3000) / 1000, y = -d / 1000.
"""
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import bpy
from mathutils import Matrix

import build_shopfront as bs


def _sf():
    import sw_front as SF
    return SF


# ---------------------------------------------------------------------------------------------------------------------------------- pictures
def tile_picture(path, tile_rgb, skirt_rgb=(28, 28, 30), grout_rgb=(148, 148, 140), px_per_mm=2.0, seed=5, soil=0.10):
    """The square-tile stallriser's printed face (3.2 target parts.stallriser.variants.tile_square): 6 in (152.4) tiles, 3 mm joints, a black skirting 100 high, two full courses, a half course 76.2 and a
    bullnose cap 35 (100 + 2 x 155.4 + 79.2 + 35 = 525). One repeat across is four tiles (621.6 mm), the picture is the whole 525 mm of height, v 0 at the bottom of the stallriser. A glaze (a faint
    top-lit gradient in each tile), a per-tile shade of +-4 per cent and a soiling of `soil` at the foot. Returns the repeat width in mm."""
    rng = np.random.default_rng(seed)
    pitch = 155.4
    W_mm, H_mm = 4 * pitch, 525.0
    w, h = int(round(W_mm * px_per_mm)), int(round(H_mm * px_per_mm))
    im = np.zeros((h, w, 3), np.float32)
    im[:] = grout_rgb
    k = px_per_mm
    # rows from the foot: (z0, z1, is_skirt)
    rows = [(0.0, 100.0, "skirt")]
    z = 103.0
    for _ in range(2):
        rows.append((z, z + 152.4, "tile"))
        z += 155.4
    rows.append((z, z + 76.2, "tile"))
    z += 79.2
    rows.append((z, 525.0, "cap"))
    for (za, zb, kind) in rows:
        for c in range(4):
            xa, xb = c * pitch, c * pitch + 152.4
            if kind == "cap":
                xa, xb = c * pitch - 1.5, c * pitch + pitch - 1.5
            col = np.array(skirt_rgb if kind == "skirt" else tile_rgb, np.float32) * (1.0 + rng.uniform(-0.04, 0.04))
            ya, yb = int(round((H_mm - zb) * k)), int(round((H_mm - za) * k))
            xa_, xb_ = int(round(xa * k)), int(round(xb * k))
            block = np.empty((max(yb - ya, 1), max(xb_ - xa_, 1), 3), np.float32)
            gy = np.linspace(1.05, 0.95, block.shape[0])[:, None, None]
            block[:] = col * gy
            if kind == "cap":
                block *= np.linspace(1.08, 0.92, block.shape[0])[:, None, None]
            im[max(ya, 0):yb, max(xa_, 0):xb_] = np.clip(block[:min(yb, h) - max(ya, 0)], 0, 255)[:, : (min(xb_, w) - max(xa_, 0))]
    # soiling at the foot and a little grain
    foot = np.linspace(0.0, 1.0, h)[:, None, None]
    im *= (1.0 - soil * foot ** 4)
    im += rng.normal(0.0, 1.6, im.shape).astype(np.float32)
    Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(path)
    return W_mm


def floor_picture(path, kind, w_mm, d_mm, seed=7):
    """The lobby's floor, one picture over the whole floor (u across, d out: the picture's top is the street edge), 1 px a millimetre.
    quarry: red-brown quarry tile 150 square with 3 mm joints, each tile a little different, worn at the front edge (the launderette's);
    terrazzo: grey with white and dark chips, and a 150 mosaic border of 20 mm tiles in cream and bottle green round the edge (the grocer's)."""
    rng = np.random.default_rng(seed)
    w, h = int(w_mm), int(d_mm)
    if kind == "quarry":
        im = np.empty((h, w, 3), np.float32)
        im[:] = (150, 144, 134)
        pitch = 153.0
        for j in range(int(math.ceil(h / pitch)) + 1):
            for i in range(int(math.ceil(w / pitch)) + 1):
                col = np.array((138, 68, 48), np.float32) * (1.0 + rng.uniform(-0.12, 0.12)) + rng.uniform(-6, 6, 3)
                x0, y0 = int(i * pitch), int(j * pitch)
                x1, y1 = min(w, int(i * pitch + 150)), min(h, int(j * pitch + 150))
                if x1 > x0 and y1 > y0:
                    blk = np.empty((y1 - y0, x1 - x0, 3), np.float32)
                    blk[:] = col
                    blk += rng.normal(0, 3.0, blk.shape)
                    im[y0:y1, x0:x1] = blk
        wear = np.linspace(1.0, 0.0, h)[:, None, None] ** 3 * 0.10
        im = im * (1.0 - wear) + np.array((170, 120, 100), np.float32) * wear
        Image.fromarray(np.clip(im, 0, 255).astype(np.uint8)).save(path)
        return
    # terrazzo
    base = np.empty((h, w, 3), np.float32)
    base[:] = (150, 148, 142)
    img = Image.fromarray(base.astype(np.uint8))
    d = ImageDraw.Draw(img)
    for _ in range(int(w * h / 90)):
        x, y = rng.integers(0, w), rng.integers(0, h)
        r = int(rng.integers(2, 6))
        c = int(rng.integers(0, 10))
        col = (236, 234, 226) if c < 6 else ((98, 96, 92) if c < 9 else (176, 150, 120))
        d.polygon([(x - r, y), (x, y - r + 1), (x + r, y + 1), (x + 1, y + r)], fill=col)
    bw, tw = 150, 20
    cream, green = (226, 214, 184), (36, 61, 49)
    d.rectangle([0, 0, w - 1, h - 1], outline=(70, 66, 60))
    for j in range(0, h, tw):
        for i in range(0, w, tw):
            if i < bw or i >= w - bw or j < bw or j >= h - bw:
                c = cream if ((i // tw) + (j // tw)) % 2 == 0 else green
                d.rectangle([i + 1, j + 1, i + tw - 1, j + tw - 1], fill=c)
    # the inner edge of the border: a thin dark line
    d.rectangle([bw - 1, bw - 1, w - bw, h - bw], outline=(60, 58, 54))
    img = img.filter(ImageFilter.GaussianBlur(0.4))
    a = np.asarray(img).astype(np.float32)
    a += rng.normal(0, 2.0, a.shape)
    Image.fromarray(np.clip(a, 0, 255).astype(np.uint8)).save(path)


def planar_uv(ob, fn):
    """UVs on every loop of an object built in metres: fn(u_mm from the viewer's left, d_mm out, z_mm) -> (s, t)."""
    me = ob.data
    uv = me.uv_layers.active or me.uv_layers.new(name="UVMap")
    for loop in me.loops:
        co = me.vertices[loop.vertex_index].co
        uv.data[loop.index].uv = fn(co.x * 1000.0 + 3000.0, -co.y * 1000.0, co.z * 1000.0)


# ---------------------------------------------------------------------------------------------------------------------------------- the lobby (a recessed door)
def lobby_parts(self):
    """The recessed lobby of a front (3.2 target parts.lobby): the door frame, the leaf, the fanlight, the bell, the threshold and the slab behind the door stand `recess` back from the frame line (d 100): the
    launderette 300 (the frame's front at d -200), the grocer 600 (d -500). Every object whose name starts door_, bell_ or fanlight_ is moved back (the OPEN sign and the glass rows that stand on the door
    are moved when they are made). What the lobby is made of, from the kit's `lobby` and the shop's own `front.lobby`:
      floor    z 0 to 25 from the leaf's outside plane (d 70 - recess) to the frame line (d 100), across the slot; quarry tile 150 (the launderette) or grey terrazzo with a 150 mosaic border (the grocer);
               a 30 x 6 nosing across the front edge (aluminium channel / brass), standing on the floor
      soffit   a plate z 2372 to 2400 between the returns, from the door frame's front to the frame line, painted board / plaster (the shop's window-frame paint is not used: it is the pier's paint)
      returns  the WINDOW side: the window's end frame returned square (members 28 wide: top rail, bottom rail at 600, a front post at the frame line), a 6 mm pane between them from z 600 to 2400, and below 600
               a kick panel 20 thick in the stallriser's own material (the grocer's green glass, the launderette's white tile); the OTHER side (the pier's, or the side door's): a lining 20 thick painted
               in the pier's paint, with two raised panels on it for the grocer (the target: 'a panelled lining in the pier's paint, 2 panels')
    The floor, the nosing and the kick panels are given their pictures in the shop's late_ step."""
    SF = _sf()
    ctx, R = self.ctx, self.R
    rec = ctx.lobby_depth
    slot = R["front"]["zones_u_mm"]["shop_door"]
    u0, u1 = float(slot[0]), float(slot[1])
    for o in list(self.B.objs):
        if o.name.startswith(("door_", "bell_", "fanlight_")):
            o.data.transform(Matrix.Translation((0.0, rec, 0.0)))
            o.data.update()
    d_back = 100.0 - rec                        # the door frame's front face
    win_is_u1 = ctx.door_end == "L"             # doors at the viewer's left: the window lies to the right of the slot
    uw = u1 if win_is_u1 else u0                # the slot's edge that meets the window
    up = u0 if win_is_u1 else u1                # the slot's other edge (the pier's, or the side door's)
    sgn = -1.0 if win_is_u1 else 1.0            # from an edge into the slot
    t = 20.0
    band_w = 28.0
    L = R["front"]["lobby"]
    panelled = "panelled" in str(L.get("pier_side_return", ""))        # the grocer's lining carries two panels (3.2: pier_side 'a panelled lining in the pier's paint, 2 panels')
    self.mats.setdefault("lobby_floor_placeholder", bs.make_material("lobby_floor_placeholder", (120, 110, 100), 0.4, 0.0))
    # floor and nosing
    self.add("lobby_floor", SF.bx(u0, u1, 70.0 - rec, 100.0, 0.0, 25.0), "lobby_floor_placeholder", bev=None)
    self.add("lobby_nosing", SF.bx(u0, u1, 70.0, 100.0, 25.0, 31.0), "brass", bev=1.0)        # brass, 30 x 6, at the frame line (the shop's own lobby entry says brass for both lobbies)
    # soffit between the returns (the lining's 20 on the pier side, the window-side return's 28 on the other)
    s_a, s_b = sorted((up - sgn * t, uw + sgn * band_w))
    self.add("lobby_soffit", SF.bx(s_a, s_b, d_back, 100.0, 2372.0, 2400.0), "white", bev=None)
    # the window-side return: u from uw into the slot by t
    ua, ub = sorted((uw, uw + sgn * t))
    self.add("lobby_kick_w", SF.bx(ua, ub, d_back, 100.0, 25.0, 600.0), "oxblood", bev=None)
    fa, fb = sorted((uw, uw + sgn * band_w))
    self.add("lobby_rail_w_bottom", SF.bx(fa, fb, d_back, 100.0, 600.0, 600.0 + band_w), "white")
    self.add("lobby_rail_w_top", SF.bx(fa, fb, d_back, 100.0, 2400.0 - band_w, 2400.0), "white")
    self.add("lobby_post_w", SF.bx(fa, fb, 100.0 - band_w, 100.0, 600.0 + band_w, 2400.0 - band_w), "white")
    ga, gb = sorted((uw + sgn * 11.0, uw + sgn * 17.0))
    self.add("lobby_glass_w", SF.bx(ga, gb, d_back, 100.0 - band_w + 3.0, 600.0 + band_w - 3.0, 2400.0 - band_w + 3.0), "glass", bev=None)
    # the other side: a painted lining
    la, lb = sorted((up, up - sgn * t))
    self.add("lobby_lining", SF.bx(la, lb, d_back, 100.0, 25.0, 2400.0), "oxblood", bev=None)
    if panelled:
        inner = (up - sgn * t)
        pa, pb = sorted((inner, inner - sgn * 6.0))
        span = 100.0 - d_back
        for k in range(2):
            d0 = d_back + 40.0 + k * (span - 40.0) / 2.0
            d1 = d0 + (span - 40.0) / 2.0 - 40.0
            self.add("lobby_panel_%d" % k, SF.bx(pa, pb, d0, d1, 300.0, 2100.0), "oxblood", bev=1.0)
    return {"d_back": d_back, "window_edge_u": uw, "other_edge_u": up}


# ---------------------------------------------------------------------------------------------------------------------------------- the lit box sign on the fascia
def _box_geometry(self):
    man = json.load(open(os.path.join(self.ctx.fascias, "manifest.json")))
    b = next(x for x in man["geometry_for_the_blender_builder"]["boxes"] if x["board"] == self.ctx.id)
    x0, y0, x1, y1 = b["outer_mm"]
    return {"u0": 295.0 + x0, "u1": 295.0 + x1, "z0": 3400.0 - y1, "z1": 3400.0 - y0, "depth": b["depth_m"] * 1000.0, "returns": b["returns"], "id": b["id"]}


def _strip_frame(self, prefix, outer, d0, d1, thick, mat):
    SF = _sf()
    u0, z0, u1, z1 = outer
    self.add(prefix + "_top", SF.bx(u0, u1, d0, d1, z1 - thick, z1), mat, bev=None)
    self.add(prefix + "_bottom", SF.bx(u0, u1, d0, d1, z0, z0 + thick), mat, bev=None)
    self.add(prefix + "_left", SF.bx(u0, u0 + thick, d0, d1, z0 + thick, z1 - thick), mat, bev=None)
    self.add(prefix + "_right", SF.bx(u1 - thick, u1, d0, d1, z0 + thick, z1 - thick), mat, bev=None)


def extras_steam_laundry(self):
    """The launderette's lit box sign on the old cream board (4.1: `steam_laundry_box`, outer 105 to 5305 on the board, 35 to 515 down from its top, 0.15 deep, bronze anodised returns, eight pan-head screws):
    the returns here, the face (the board's own picture) in `late_steam_laundry`. Read from the 4.1 manifest (geometry_for_the_blender_builder.boxes), not typed."""
    SF = _sf()
    g = _box_geometry(self)
    self.mats["bronze_anod"] = bs.make_material("bronze_anodised", (84, 68, 53), 0.35, 0.8)
    self.box_geo = g
    d1 = 120.0 + g["depth"]
    _strip_frame(self, "box_sign", (g["u0"], g["z0"], g["u1"], g["z1"]), 120.0, d1, 12.0, "bronze_anod")
    w = g["u1"] - g["u0"]
    for k in range(4):
        u = g["u0"] + w * (k + 0.5) / 4.0
        for z in (g["z1"] - 6.0, g["z0"] + 6.0):
            self.add("box_screw_%d_%d" % (k, int(z)), SF.cyl_d(u, z, d1, d1 + 4.0, 4.0, 10), "steel", bev=None)


# ---------------------------------------------------------------------------------------------------------------------------------- the pictures on the lobby and the stallriser, after the fascia material exists
def _tile_and_floor(self, members, tile_rgb, floor_kind, lobby=True, slab=False):
    SF = _sf()
    ctx = self.ctx
    work = self.scratch
    os.makedirs(work, exist_ok=True)
    win0 = ctx.zones["window"][0]
    stall = bpy.data.objects.get("sta_panel")
    kick = bpy.data.objects.get("lobby_kick_w")
    fl = bpy.data.objects.get("lobby_floor")
    if slab:
        sm = bs.make_material("paint_stallriser_slab_green", ctx.R["front"]["paint_srgb"]["stallriser"], 0.08, 0.0)
        for nm in [o.name for o in bpy.data.objects if o.name.startswith(("sta_slab_", "sta_backing"))]:
            ob = bpy.data.objects[nm]
            ob.data.materials.clear()
            ob.data.materials.append(sm if nm.startswith("sta_slab_") else bs.make_material("mastic_black", (22, 22, 22), 0.4, 0.0))
            if nm in members:
                members[nm]["material"] = ob.data.materials[0].name
        cap = bpy.data.objects.get("sta_capping")
        if cap is not None:
            cap.data.materials.clear()
            cap.data.materials.append(self.mats.get("chrome") or bs.make_material("chrome", (170, 172, 174), 0.2, 1.0))
        for nm in [o.name for o in bpy.data.objects if o.name.startswith("sta_mastic_")]:
            ob = bpy.data.objects[nm]
            ob.data.materials.clear()
            ob.data.materials.append(bs.make_material("mastic_black", (22, 22, 22), 0.4, 0.0))
        if kick is not None:
            kick.data.materials.clear()
            kick.data.materials.append(sm)
            if kick.name in members:
                members[kick.name]["material"] = sm.name
    else:
        tp = os.path.join(work, "tile_%s.png" % ctx.id)
        rep = tile_picture(tp, tile_rgb)
        tm = SF.image_material("tile_" + ctx.id, tp, rough=0.22)
        for ob in (stall, kick):
            if ob is None:
                continue
            planar_uv(ob, lambda u, d, z: ((u - win0) / rep, min(z, 524.0) / 525.0))        # (the lobby's kick panel stands to 600: above the stallriser's 525 it takes the cap's row)
            ob.data.materials.clear()
            ob.data.materials.append(tm)
            if ob.name in members:
                members[ob.name]["material"] = tm.name
    if lobby and fl is not None:
        slot = ctx.zones["shop_door"]
        u0, u1 = float(slot[0]), float(slot[1])
        d0, d1 = 70.0 - ctx.lobby_depth, 100.0
        fp = os.path.join(work, "lobby_floor_%s.png" % ctx.id)
        floor_picture(fp, floor_kind, u1 - u0, d1 - d0)
        fm = SF.image_material("lobby_floor_" + ctx.id, fp, rough=0.35 if floor_kind == "quarry" else 0.28)
        planar_uv(fl, lambda u, d, z: ((u - u0) / (u1 - u0), (d - d0) / (d1 - d0)))
        fl.data.materials.clear()
        fl.data.materials.append(fm)
        if fl.name in members:
            members[fl.name]["material"] = fm.name


def late_steam_laundry(self, fm, members, extra_objs):
    """The launderette: the box sign's lit face (the fascia's own picture on a plane 6 mm inside the returns' front edge), the white glazed tile on the stallriser and the lobby's kick panel, and the quarry floor."""
    SF = _sf()
    g = self.box_geo
    d_face = 120.0 + g["depth"] - 6.0
    face = SF.quad_obj("box_sign_face", g["u0"] + 12.0, g["u1"] - 12.0, g["z0"] + 12.0, g["z1"] - 12.0, d_face)
    SF.set_fascia_uvs(face)
    face.data.materials.append(fm)
    members[face.name] = {"u": [g["u0"] + 12.0, g["u1"] - 12.0], "z": [g["z0"] + 12.0, g["z1"] - 12.0], "d": [d_face, d_face], "group": "box_sign"}
    extra_objs.append(face)
    _tile_and_floor(self, members, tuple(self.R["front"]["paint_srgb"]["stallriser"]), "quarry")


def late_grocer(self, fm, members, extra_objs):
    """The grocer: the green glass slabs and chrome capping on the stallriser (and the lobby's kick panel in the same green glass), the terrazzo floor with its mosaic border."""
    _tile_and_floor(self, members, None, "terrazzo", slab=True)


# ---------------------------------------------------------------------------------------------------------------------------------- the launderette's hanging box
def make_hanging_box(ctx, front, fasc_dir):
    """The launderette's projecting box sign (4.1 `steam_laundry_box`): a box 0.62 out from the wall, 0.45 high (z 3.60 to 4.05 above the footway) and 0.14 thick between its two faces, its back edge fixed to
    the brick above the cornice over the pier at the window end of the bay (street x 27.175, the viewer's RIGHT end), bronze extrusions 20 wide round each face, white acrylic faces, tubes inside (not modelled).
    Built: two small plates on the brick, the body (white acrylic, 132 across), on each side a frame of four bronze rails 14 deep in u and 20 wide, closed across the top, bottom, front and back by caps,
    and on each side a face (a one-sided quad inside the frame, 2.5 mm behind its outer surface) carrying the 4.1 face a or b: a on the side that looks toward the quay end (low street x), as the
    ironmonger's board has it. The lowest part stands at 3.60 (the cornice's top is 3.55). Returns (parts [(material key, object in mm)], textured faces already in metres)."""
    SF = _sf()
    hs = ctx.R["fascia"]["hanging_sign"]
    mt = hs["mount"]
    uc = ctx.u_of_x(mt["x_street_m"])
    man = json.load(open(os.path.join(fasc_dir, "manifest.json")))
    hsm = next(h for h in man["hanging_signs"] if h["id"] == hs["id"])
    bw, bh, bt = (v * 1000.0 for v in hsm["parts"]["box_m"])          # 620 out, 450 high, 140 thick
    z_top = mt["arm_height_m"] * 1000.0
    z_bot = z_top - bh
    d0, d1 = 8.0, 8.0 + bw
    rail, half = 20.0, bt / 2.0
    parts = []
    mats = front.mats
    mats.setdefault("bronze_anod", bs.make_material("bronze_anodised", (84, 68, 53), 0.35, 0.8))
    mats.setdefault("acrylic", bs.make_material("sign_acrylic", (232, 230, 224), 0.3, 0.0))
    for k, zc in enumerate((z_bot + 60.0, z_top - 60.0)):
        parts.append(("black_iron", bs.new_obj("sign_plate_%d" % k, *SF.bx(uc - 40.0, uc + 40.0, 0.0, 8.0, zc - 40.0, zc + 40.0))))
    for sgn in (-1, 1):
        ua, ub = sorted((uc + sgn * (half - 14.0), uc + sgn * half))
        tag = "p" if sgn > 0 else "m"
        parts.append(("bronze_anod", bs.new_obj("sign_rail_top_" + tag, *SF.bx(ua, ub, d0, d1, z_top - rail, z_top))))
        parts.append(("bronze_anod", bs.new_obj("sign_rail_bottom_" + tag, *SF.bx(ua, ub, d0, d1, z_bot, z_bot + rail))))
        parts.append(("bronze_anod", bs.new_obj("sign_rail_front_" + tag, *SF.bx(ua, ub, d1 - rail, d1, z_bot + rail, z_top - rail))))
        parts.append(("bronze_anod", bs.new_obj("sign_rail_back_" + tag, *SF.bx(ua, ub, d0, d0 + rail, z_bot + rail, z_top - rail))))
    ia, ib = uc - (half - 14.0), uc + (half - 14.0)
    parts.append(("bronze_anod", bs.new_obj("sign_cap_top", *SF.bx(ia, ib, d0, d1, z_top - rail, z_top))))
    parts.append(("bronze_anod", bs.new_obj("sign_cap_bottom", *SF.bx(ia, ib, d0, d1, z_bot, z_bot + rail))))
    parts.append(("bronze_anod", bs.new_obj("sign_cap_front", *SF.bx(ia, ib, d1 - rail, d1, z_bot + rail, z_top - rail))))
    parts.append(("bronze_anod", bs.new_obj("sign_cap_back", *SF.bx(ia, ib, d0, d0 + rail, z_bot + rail, z_top - rail))))
    parts.append(("acrylic", bs.new_obj("sign_body", *SF.bx(uc - (half - 4.0), uc + (half - 4.0), d0 + rail, d1 - rail, z_bot + rail, z_top - rail))))
    a_side = -1 if ctx.west else 1
    faces = []
    for fk, side in (("a", a_side), ("b", -a_side)):
        f = next(x for x in hsm["faces"] if x["id"].endswith("." + fk))
        base = os.path.join(fasc_dir, f["files"]["basecolour"]["file"])
        orm = os.path.join(fasc_dir, f["files"]["orm"]["file"])
        x = (uc - SF.BAY_MID + side * (half - 2.5)) / 1000.0
        za, zb = (z_bot + rail) / 1000.0, (z_top - rail) / 1000.0
        ya, yb = -(d1 - rail) / 1000.0, -(d0 + rail) / 1000.0        # the street end to the wall end
        if side > 0:
            V = [(x, ya, za), (x, yb, za), (x, yb, zb), (x, ya, zb)]
            uv = [(rail / bw, rail / bh), (1 - rail / bw, rail / bh), (1 - rail / bw, 1 - rail / bh), (rail / bw, 1 - rail / bh)]
        else:
            V = [(x, yb, za), (x, ya, za), (x, ya, zb), (x, yb, zb)]
            uv = [(rail / bw, rail / bh), (1 - rail / bw, rail / bh), (1 - rail / bw, 1 - rail / bh), (rail / bw, 1 - rail / bh)]
        me = bpy.data.meshes.new("sign_face_%s" % fk)
        me.from_pydata(V, [], [(0, 1, 2, 3)])
        me.update()
        uvl = me.uv_layers.new(name="UVMap")
        for loop, (a_, b_) in zip(me.loops, uv):
            uvl.data[loop.index].uv = (a_, b_)
        ob = bpy.data.objects.new("sign_face_%s" % fk, me)
        bpy.context.scene.collection.objects.link(ob)
        ob.data.materials.append(SF.image_material("sign_face_%s" % fk, base, orm=orm))
        faces.append(ob)
    return parts, faces


def late_chandler(self, fm, members, extra_objs):
    """The chandler: the pale green glazed tile on the stallriser (3.2: tile_square, 'chandler pale green')."""
    _tile_and_floor(self, members, tuple(self.R["front"]["paint_srgb"]["stallriser"]), None, lobby=False)


def late_fish_market(self, fm, members, extra_objs):
    """The fish market: the white glazed tile on the stallriser (3.2: tile_square, 'fish and laundry white')."""
    _tile_and_floor(self, members, tuple(self.R["front"]["paint_srgb"]["stallriser"]), None, lobby=False)


# ---------------------------------------------------------------------------------------------------------------------------------- the fish market's stowed awning
GLASS_OBSTACLES = {"fish_market": [(2060.0, 2100.0)]}         # horizontal parts standing in front of a shop's glass: (z from, z to) in mm above the footway; no glass row may cross one (sw_front.clear_rects)


def _cyl_u(u0, u1, d, z, r, n=16):
    """A cylinder along u (a rail), mm: ends at u0 and u1, centre at (d, z)."""
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    V = []
    for u in (u0, u1):
        for t in a:
            V.append((u, -(d + r * math.cos(t)), z + r * math.sin(t)))
    F = [tuple(range(n))[::-1], tuple(range(n, 2 * n))] + [(i, (i + 1) % n, n + (i + 1) % n, n + i) for i in range(n)]
    return np.array(V), F


def extras_fish_market(self):
    """The retractable awning of P1, canvas stowed (3.3 / target `blinds_grilles_shutters`: 'a retractable awning's arms and blind rail across the front at the transom, canvas stowed or absent (Photo, P1: two
    diagonal arms and a black rail at about z 2080, +-40; the arms and the 40 mm rail are Judgement)'): a black round rail 40 across along the whole window from jamb to jamb at z 2080, standing out at d 150
    (the sill's nose is 150), and a flat arm 30 x 8 at each end running up and back from the rail to a small bracket on the window head's face (d 95, z 2790), in front of the window frame's jambs
    so that no arm crosses a pane. The rail's z band is a GLASS_OBSTACLE: the glass rows are placed clear of it."""
    SF = _sf()
    self.mats.setdefault("awning_black", bs.make_material("powder_black_awning", (37, 35, 34), 0.45, 0.0))
    win = self.R["front"]["zones_u_mm"]["window"]
    u0, u1 = float(win[0]), float(win[1])
    z = 0.5 * sum(GLASS_OBSTACLES["fish_market"][0])
    d_rail = 150.0
    self.add("rail_awning", _cyl_u(u0 + 5.0, u1 - 5.0, d_rail, z, 20.0), "awning_black", bev=None)
    for nm, ua in (("l", u0 + 14.0), ("r", u1 - 14.0 - 30.0)):
        # the arm: from the rail (d 150, z 2080) to the bracket (d 104, z 2790): a flat strip in the d-z plane, 30 wide in u, 8 thick
        pts = [(d_rail - 20.0, z + 18.0), (104.0, 2790.0)]
        V = []
        t = 8.0
        for (d, zz) in pts:
            for du in (0.0, 30.0):
                for dd in (-t / 2.0, t / 2.0):
                    V.append((ua + du, -(d + dd), zz))
        V = np.array(V)
        F = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
        self.add("rail_awning_arm_" + nm, (V, F), "awning_black", bev=None)
        self.add("rail_awning_bracket_" + nm, SF.bx(ua - 5.0, ua + 35.0, 95.0, 104.0, 2760.0, 2800.0), "awning_black", bev=None)
