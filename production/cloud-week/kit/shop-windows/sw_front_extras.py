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
