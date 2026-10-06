"""The office kettle: a corded plastic jug kettle of about 1990, cream
polypropylene gone a little yellow, grey switch, lid button and connector
shroud, a smoked water-level window. Generic, no maker's name or shape.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/jug-kettle.py [-- --no-render]

SIZE (read 6 October 2026): MoDiP AIBDC 001258, an electric jug kettle,
white injection-moulded polypropylene, circa 1990-1999: width 220 mm,
height 220 mm, depth 130 mm, https://www.modip.ac.uk/artefact/aibdc-001258
(and the V&A's Autoboil, the first plastic jug kettle, 1979-1985, beige,
240 x 140 x 240 mm, for the form,
https://collections.vam.ac.uk/item/O1298422/autoboil-electric-jug-kettle-redring-electric-ltd/).
Origin: centre of the body's foot, z = 0. Spout toward -X, handle toward +X,
the level window toward -Y (the front).
The kettle stands unplugged: the connector socket under the handle is empty.
"""
import math
import os
import sys

import bmesh
from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402

W, D, H = 0.220, 0.130, 0.220
XC = -0.012                     # body axis, so spout tip and handle back span W
NSEG = 64
EXP = 2.6                       # superellipse squareness of the body section


def section(a, b, ang):
    c, s = math.cos(ang), math.sin(ang)
    return (a * math.copysign(abs(c) ** (2 / EXP), c), b * math.copysign(abs(s) ** (2 / EXP), s))


def build():
    C.reset()
    cream = C.material("kettle_pp_cream", (0.86, 0.83, 0.74), 0.42)
    grey = C.material("kettle_grey", (0.42, 0.42, 0.41), 0.40)
    smoke = C.material("kettle_smoked_window", (0.16, 0.14, 0.12), 0.08)

    # ---- body: lofted superellipse rings, tapering up, spout lip at -X ------
    rings_z = [0.0, 0.0025, 0.008, 0.020, 0.050, 0.090, 0.130, 0.165, 0.185, 0.196, 0.201]
    def ab(z):
        t = z / 0.201
        return 0.0685 - 0.0095 * t ** 1.3, 0.0650 - 0.0090 * t ** 1.3
    bm = bmesh.new()
    rings = []
    for z in rings_z:
        a, b = ab(z)
        if z == 0.0:
            a, b = a - 0.003, b - 0.003
        ring = []
        for k in range(NSEG):
            ang = 2 * math.pi * k / NSEG
            x, y = section(a, b, ang)
            # pouring lip: pull the top of the -X side out and up
            w = max(0.0, -math.cos(ang)) ** 6
            lift = max(0.0, (z - 0.150) / 0.051) ** 2
            x -= 0.031 * w * lift
            zz = z + 0.007 * w * lift
            ring.append(bm.verts.new((XC + x, y, zz)))
        rings.append(ring)
    for i in range(len(rings) - 1):
        for k in range(NSEG):
            bm.faces.new([rings[i][k], rings[i][(k + 1) % NSEG],
                          rings[i + 1][(k + 1) % NSEG], rings[i + 1][k]])
    bm.faces.new(list(reversed(rings[0])))
    bm.faces.new(rings[-1])
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    body = C._link("body", bm, cream)
    body["no_wn"] = True
    body["sharp_angle"] = 60.0

    # foot ring, grey
    C.cyl("foot", 0.060, 0.004, (XC, 0, 0.002), mat=grey, segs=48, bevel=0.0012)
    C.PARTS[-1].data.transform(C.mat4((XC, 0, 0), (0, 0, 0), (1.0, 0.94, 1.0)) @
                               C.mat4((-XC, 0, 0)))

    # ---- lid with its release button --------------------------------------
    lid_prof = [(0.0, 0.2125), (0.030, 0.2115), (0.044, 0.2085), (0.050, 0.2040), (0.052, 0.1995),
                (0.050, 0.1985), (0.0, 0.1985)]
    lid = C.lathe("lid", lid_prof, segs=48, mat=cream)
    lid.data.transform(C.mat4((XC + 0.006, 0, 0), (0, 0, 0), (1.0, 0.92, 1.0)))
    lid["no_wn"] = True
    lid["sharp_angle"] = 50.0
    C.box("lid_button", (0.030, 0.018, 0.009), (XC + 0.040, 0, 0.2155), grey, bevel=0.003, segs=3)

    # ---- handle: a squared D from the shoulder down to the hip at +X -------
    xc, zc, a_, b_, ex = 0.046, 0.111, 0.0625, 0.081, 2.0 / 3.0
    xin = 0.038                                   # joints sink into the body
    a_end = math.pi - math.acos(min(1.0, ((xc - xin) / a_) ** (1 / ex)))
    path = []
    for k in range(81):
        ang = a_end - 2 * a_end * k / 80
        c_, s_ = math.cos(ang), math.sin(ang)
        path.append(Vector((xc + a_ * math.copysign(abs(c_) ** ex, c_), 0,
                            zc + b_ * math.copysign(abs(s_) ** ex, s_))))
    path, _ = C.resample(path, 0.003)
    sec = C.rounded_rect(0.028, 0.019, 0.0085, n=4)
    h = C.profile_sweep("handle", path, sec, mat=cream)
    h["no_wn"] = True
    h["sharp_angle"] = 70.0
    # rocker switch under the thumb at the top of the handle, and the
    # connector shroud below the handle (empty: the kettle is unplugged)
    C.box("switch", (0.020, 0.016, 0.010), (0.082, 0, 0.1945), grey, rot=(0, math.radians(-12), 0),
          bevel=0.003, segs=2)
    C.box_z("shroud", 0.046, 0.076, -0.017, 0.017, 0.010, 0.040, grey, bevel=0.003, segs=2)
    C.box_z("socket", 0.0755, 0.0770, -0.011, 0.011, 0.016, 0.034, smoke, bevel=0.0006, segs=1)

    # ---- the level window on the front face, near the handle --------------
    wx = 0.026
    z0, z1 = 0.040, 0.168
    zm = (z0 + z1) / 2

    def face_y(z):
        a, b = ab(z)
        return -b * (1 - abs((wx - XC) / a) ** EXP) ** (1 / EXP)
    tilt = math.atan((face_y(z1) - face_y(z0)) / (z1 - z0))   # follow the taper
    y = face_y(zm)
    C.box("window", (0.016, 0.004, z1 - z0), (wx, y + 0.0012, zm), smoke, rot=(-tilt, 0, 0),
          bevel=0.0018, segs=3)
    C.box("window_frame", (0.021, 0.004, z1 - z0 + 0.005), (wx, y + 0.0016, zm), cream,
          rot=(-tilt, 0, 0), bevel=0.0018, segs=3)

    o = C.cli()
    ob, info = C.finish_prop("jug-kettle", "jug_kettle", ao_distance=0.03, edge_span=0.10,
                             ref={"x": W, "y": D, "z": H}, render=o["render"],
                             preview_kw={"azimuth": -30, "elevation": 22})
    return info


if __name__ == "__main__":
    build()
