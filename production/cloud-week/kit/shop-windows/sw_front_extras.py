"""Parts that belong to one shop's alterations (batch A, 13 October 2026): the newsagent's roller-shutter hood, rails and lit box sign; the tea rooms' flat panel sign; the empty unit's boards, letting
board and whitewashed glass; Mickey's raised letters. Functions take the Front (sw_front.Front) as `self` and are bound to it at the end of sw_front.py (`extras_<id>`, built with the kit's parts) and
`late_<id>` (built after the fascia material exists, so that a sign's face can carry its 4.1 picture).

Frame (millimetres): u from the viewer's LEFT across the bay (the fascia board u 295 to 5705, z 2850 to 3400, its front face at d 120), d out from the wall face, z above the footway.
"""
import math

import bpy

import build_shopfront as bs


def _sf():
    import sw_front as SF
    return SF


def _strip_frame(self, prefix, outer, d0, d1, thick, mat):
    """Four strips (a frame's returns) round a rectangle `outer` = (u0, z0, u1, z1)."""
    SF = _sf()
    u0, z0, u1, z1 = outer
    self.add(prefix + "_top", SF.bx(u0, u1, d0, d1, z1 - thick, z1), mat, bev=None)
    self.add(prefix + "_bottom", SF.bx(u0, u1, d0, d1, z0, z0 + thick), mat, bev=None)
    self.add(prefix + "_left", SF.bx(u0, u0 + thick, d0, d1, z0 + thick, z1 - thick), mat, bev=None)
    self.add(prefix + "_right", SF.bx(u1 - thick, u1, d0, d1, z0 + thick, z1 - thick), mat, bev=None)


# ---------------------------------------------------------------------------------------------------------------------------------- the newsagent
def extras_newsagent(self):
    """The roller shutter of 2.2's alterations (up by day: the steel hood 300 high and 210 out, over the window and the shop door, under the fascia; its two guide rails and the middle one, 50 x 50, from the
    hood to the sill and the threshold) and the lit box sign's returns (4.1: `newsagent_box`, outer 95, 40 to 5315, 510 on the board, 0.14 out, powder black, eight pan-head screws): the face is made
    after the board's material exists (`late_newsagent`). The slats are in the hood by day: nothing hangs in the opening."""
    SF = _sf()
    self.mats["shutter"] = bs.make_material("shutter_steel", (150, 152, 150), 0.45, 0.5)
    u0, u1 = 350.0, 4706.0
    prof = [(95.0, 2550.0), (212.0, 2550.0), (212.0, 2770.0), (172.0, 2850.0), (95.0, 2850.0)]
    self.add("hood_shutter", bs.prism_dz(prof, u0, u1), "shutter", bev=2.0)
    for k, (ua, ub, zb) in enumerate(((350.0, 400.0, 600.0), (3680.0, 3730.0, 0.0), (4656.0, 4706.0, 0.0))):
        self.add("rail_shutter_%d" % k, SF.bx(ua, ub, 96.0, 146.0, zb + (4.0 if zb == 0.0 else 0.0), 2550.0), "shutter", bev=1.5)
    # the box sign's returns (the face: late_newsagent)
    outer = (295.0 + 95.0, 3400.0 - 510.0, 295.0 + 5315.0, 3400.0 - 40.0)
    _strip_frame(self, "box_sign", outer, 120.0, 260.0, 12.0, "black")
    for k, (uc, zc) in enumerate(((560.0, 2930.0), (560.0, 3320.0), (2700.0, 2930.0), (2700.0, 3320.0), (3300.0, 2930.0), (3300.0, 3320.0), (5440.0, 2930.0), (5440.0, 3320.0))):
        self.add("box_screw_%d" % k, SF.cyl_d(uc, zc, 260.0, 264.0, 6.0, 10), "steel", bev=None)


def late_newsagent(self, fm, members, extra_objs):
    """The sign's lit face: the fascia's own picture (the 4.1 board, the name block and the box's rules) on a plane 6 mm inside the returns' front edge."""
    SF = _sf()
    u0, z0, u1, z1 = 295.0 + 95.0 + 12.0, 3400.0 - 510.0 + 12.0, 295.0 + 5315.0 - 12.0, 3400.0 - 40.0 - 12.0
    face = SF.quad_obj("box_sign_face", u0, u1, z0, z1, 254.0)
    SF.set_fascia_uvs(face)
    face.data.materials.append(fm)
    members[face.name] = {"u": [u0, u1], "z": [z0, z1], "d": [254.0, 254.0], "group": "box_sign"}
    extra_objs.append(face)


# ---------------------------------------------------------------------------------------------------------------------------------- the tea rooms
def extras_tea_rooms(self):
    """The flat panel sign (4.1: `tea_rooms_panel`, outer 90, 40 to 5320, 510 on the board, 30 deep, white timber returns): the frame here, the face (the board's picture) in `late_tea_rooms`."""
    self.mats["white_timber"] = bs.make_material("paint_white_timber", (232, 228, 214), 0.5, 0.0)
    outer = (295.0 + 90.0, 3400.0 - 510.0, 295.0 + 5320.0, 3400.0 - 40.0)
    _strip_frame(self, "panel_sign", outer, 120.0, 150.0, 16.0, "white_timber")


def late_tea_rooms(self, fm, members, extra_objs):
    SF = _sf()
    u0, z0, u1, z1 = 295.0 + 90.0 + 16.0, 3400.0 - 510.0 + 16.0, 295.0 + 5320.0 - 16.0, 3400.0 - 40.0 - 16.0
    face = SF.quad_obj("panel_sign_face", u0, u1, z0, z1, 147.0)
    SF.set_fascia_uvs(face)
    face.data.materials.append(fm)
    members[face.name] = {"u": [u0, u1], "z": [z0, z1], "d": [147.0, 147.0], "group": "panel_sign"}
    extra_objs.append(face)


# ---------------------------------------------------------------------------------------------------------------------------------- the empty unit
def _rot_box(SF, u0, u1, d0, d1, z0, z1, deg):
    """A box turned `deg` degrees about its own d axis (in the u, z plane) round its centre: the letting board, askew."""
    V, F = SF.bx(u0, u1, d0, d1, z0, z1)
    uc, zc = (u0 + u1) / 2.0, (z0 + z1) / 2.0
    a = math.radians(deg)
    out = []
    for (u, d, z) in [tuple(v) for v in V]:
        du, dz = u - uc, z - zc
        out.append((uc + du * math.cos(a) - dz * math.sin(a), d, zc + du * math.sin(a) + dz * math.cos(a)))
    return out, F


def extras_empty_unit(self):
    """The letting board (4.1: `letting_board`, 900 x 450, screwed over the fascia, turned 2 degrees, centre at board u 2705, z 275 up from the board's foot: the unit's bare timber fascia carries it): its edges
    here (a 25 mm board standing 25 out from the fascia's face); the face, with its TO LET lettering and its four screws, in `late_empty_unit`."""
    SF = _sf()
    self.mats["board_timber"] = bs.make_material("letting_board_edge", (190, 184, 166), 0.7, 0.0)
    uc, zc = 295.0 + 2705.0, 2850.0 + 275.0
    V, F = _rot_box(SF, uc - 450.0, uc + 450.0, 120.0, 145.0, zc - 225.0, zc + 225.0, 2.0)
    self.add("letting_board_edge", (V, F), "board_timber", bev=None)


def late_empty_unit(self, fm, members, extra_objs):
    """The letting board's face and the whitewash on every pane (the 4.1 tile `window_whitewash`, 3250 x 1800 at a millimetre a pixel, anchored to the window glass: u 400 to 3650, z 600 to 2400, repeated beyond
    it over the toplights and the door's glass). The tile's alpha (a mean of 0.8: whiting laid on with a cloth) is composited over a pale ground (214, 212, 204) so that the pane is opaque: the empty unit has no room
    behind it, and an unlit pane that showed the street's sky would not be a whitewashed one."""
    import os
    import numpy as np
    from PIL import Image
    SF = _sf()
    ctx = self.ctx
    # the board's face
    d = os.path.join(ctx.fascias, "panels", "letting_board")
    uc, zc = 295.0 + 2705.0, 2850.0 + 275.0
    face = SF.quad_obj("letting_board_face", uc - 450.0 + 4.0, uc + 450.0 - 4.0, zc - 225.0 + 4.0, zc + 225.0 - 4.0, 145.5)
    # (turned with the edge: rotate its vertices 2 degrees about the board's centre)
    a = math.radians(2.0)
    for v in face.data.vertices:
        u = v.co.x * 1000.0 + 3000.0 - uc
        z = v.co.z * 1000.0 - zc
        v.co.x = (uc + u * math.cos(a) - z * math.sin(a) - 3000.0) / 1000.0
        v.co.z = (zc + u * math.sin(a) + z * math.cos(a)) / 1000.0
    face.data.update()
    face.data.materials.append(SF.image_material("letting_board", os.path.join(d, "letting_board_basecolour.png"), orm=os.path.join(d, "letting_board_orm.png")))
    members[face.name] = {"u": [uc - 446.0, uc + 446.0], "z": [zc - 221.0, zc + 221.0], "d": [145.5, 145.5], "group": "letting_board"}
    extra_objs.append(face)
    # the whitewash
    src = os.path.join(ctx.fascias, "glass", "empty_unit", "window_whitewash_rgba.png")
    im = np.asarray(Image.open(src).convert("RGBA")).astype(np.float32)
    a_ = im[..., 3:4] / 255.0
    ground = np.array([214.0, 212.0, 204.0], np.float32)
    comp = (im[..., :3] * a_ + ground * (1.0 - a_)).clip(0, 255).astype(np.uint8)
    out = os.path.join(self.scratch, "whitewash_composite.png")
    Image.fromarray(comp).resize((1625, 900), Image.LANCZOS).save(out)
    wm = SF.image_material("whitewash", out, rough=0.9)
    u_a, z_a, wu, wz = 400.0, 600.0, 3250.0, 1800.0
    n = 0
    for ob in bpy.data.objects:
        if ob.type != "MESH" or not ob.name.startswith(("win_glass_", "door_glass_", "fanlight_glass", "band_toplight_glass_", "glass_fanlight")):
            continue
        me = ob.data
        uv = me.uv_layers.active or me.uv_layers.new(name="UVMap")
        for loop in me.loops:
            co = me.vertices[loop.vertex_index].co
            uv.data[loop.index].uv = ((co.x * 1000.0 + 3000.0 - u_a) / wu, (co.z * 1000.0 - z_a) / wz)
        me.materials.clear()
        me.materials.append(wm)
        if ob.name in members:
            members[ob.name]["material"] = "whitewash"
        n += 1
    return n
