"""An anglepoise-style (spring-balanced, jointed arm) desk lamp for the radio
desk: a round iron base, paired square rods, three chromed springs, a conical
aluminium shade, all in a worn mushroom-grey enamel. Generic, no maker's.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/desk-lamp.py [-- --no-render]

SIZE (read 6 October 2026): Anglepoise Model 90, Herbert Terry & Sons, from
1973: base 180 mm across, shade 144 x 210 mm, posed 650 mm high and 450 mm
across; mushroom-grey painted iron base, three chrome springs,
https://vintageinfo.be/anglepoise-model-90-task-light/
(the same lamp, "approx 85cm" at full stretch, 1970s:
https://www.afoldofchairs.com/products/model-90-anglepoise-desk-lamp-by-herbert-terry-and-son-uk-1970s).
This recipe poses its own lamp to that 650 x 450 mm envelope.
Origin: centre of the base, z = 0; the arm reaches toward -Y (the front).
No mains flex is modelled (the dresser routes one if the back is seen).
"""
import math
import os
import sys

from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402

BASE_D, SHADE_D, SHADE_L = 0.180, 0.144, 0.210
TARGET_H, TARGET_W = 0.650, 0.450
L1, L2 = 0.320, 0.320
P0 = Vector((0, 0.010, 0.070))         # shoulder pivot


def shade_profile():
    """Outside then inside of a spun conical shade, along its own +Z."""
    R = SHADE_D / 2
    return [(0.0, -0.006), (0.018, -0.005), (0.027, 0.000), (0.031, 0.010), (0.034, 0.035),
            (0.044, 0.080), (0.058, 0.140), (0.068, 0.188), (R - 0.0005, SHADE_L - 0.004),
            (R, SHADE_L - 0.0015), (R - 0.0012, SHADE_L), (R - 0.0025, SHADE_L - 0.0015),
            (0.066, 0.188), (0.056, 0.140), (0.042, 0.080), (0.032, 0.036), (0.028, 0.012),
            (0.0, 0.006)]


def pose(alpha, beta, gamma):
    """Elbow, wrist, shade axis for lower arm at alpha, upper arm at beta
    (degrees above horizontal, reaching -Y) and shade axis gamma below
    horizontal."""
    a, b, g = map(math.radians, (alpha, beta, gamma))
    p1 = P0 + Vector((0, -math.cos(a), math.sin(a))) * L1
    p2 = p1 + Vector((0, -math.cos(b), math.sin(b))) * L2
    axis = Vector((0, -math.cos(g), -math.sin(g)))
    return p1, p2, axis


def extents(alpha, beta, gamma):
    p1, p2, axis = pose(alpha, beta, gamma)
    side = Vector((0, axis.z, -axis.y))           # in the YZ plane, normal to axis
    zmax = max(p1.z + 0.014, p2.z + 0.012)
    ymin = min(p1.y, p2.y)
    start = p2 + axis * 0.012
    for (r, t) in ((0.031, 0.0), (0.034, 0.035), (SHADE_D / 2, SHADE_L)):
        for sgn in (-1, 1):
            q = start + axis * t + side * r * sgn
            zmax = max(zmax, q.z)
            ymin = min(ymin, q.y)
    return zmax, BASE_D / 2 - ymin


def build():
    C.reset()
    enamel = C.material("lamp_enamel_mushroom", (0.58, 0.54, 0.47), 0.38)
    chrome = C.material("lamp_chrome", (0.80, 0.80, 0.80), 0.16, metal=1.0)
    bulb_m = C.material("lamp_bulb_frosted", (0.93, 0.92, 0.88), 0.30)

    # pose to the reference envelope by a small search
    best = None
    for alpha in range(70, 91, 2):
        for beta in range(0, 61, 2):
            for gamma in range(30, 86, 5):
                h, w = extents(alpha, beta, gamma)
                err = abs(h - TARGET_H) + abs(w - TARGET_W)
                if best is None or err < best[0]:
                    best = (err, alpha, beta, gamma)
    _, alpha, beta, gamma = best
    p1, p2, axis = pose(alpha, beta, gamma)

    # ---- base and shoulder -------------------------------------------------
    R = BASE_D / 2
    base = C.lathe("base", [(0.0, 0.0), (R - 0.003, 0.0), (R, 0.003), (R, 0.011), (R - 0.004, 0.015),
                            (0.072, 0.022), (0.045, 0.029), (0.026, 0.032), (0.0, 0.033)],
                   segs=64, mat=enamel)
    base["no_wn"] = True
    base["sharp_angle"] = 40.0
    C.cyl("turntable", 0.020, 0.010, (0, 0.010, 0.037), mat=chrome, segs=40, bevel=0.0015)
    for sx in (-1, 1):
        C.box_z("yoke", sx * 0.0145 - 0.0025, sx * 0.0145 + 0.0025, -0.003, 0.023, 0.040, P0.z + 0.012,
                enamel, bevel=0.0012)
    C.cyl("shoulder_bolt", 0.0075, 0.040, P0[:], (0, math.pi / 2, 0), chrome, segs=24, bevel=0.0015)

    def rod(name, a, b, w, mat, xoff):
        d = b - a
        L = d.length
        ang = math.atan2(d.z, -d.y)                 # angle above horizontal, toward -Y
        mid = (a + b) / 2 + Vector((xoff, 0, 0))
        C.box(name, (w, L, w), mid[:], mat, rot=(-ang, 0, 0), bevel=0.0012, segs=2)

    # ---- arms: paired square rods, a link rod, knuckles --------------------
    for sx in (-1, 1):
        rod("lower_rod", P0, p1, 0.007, enamel, sx * 0.0105)
        rod("upper_rod", p1, p2, 0.0065, enamel, sx * 0.0085)
    n1 = Vector((0, math.sin(math.radians(alpha)), math.cos(math.radians(alpha))))  # normal to lower arm
    rod("link_rod", P0 + n1 * 0.026 + Vector((0, 0.0, 0)), p1 + n1 * 0.024, 0.005, chrome, 0.0)
    C.cyl("elbow", 0.013, 0.034, p1[:], (0, math.pi / 2, 0), chrome, segs=28, bevel=0.002)
    C.cyl("wrist", 0.010, 0.028, p2[:], (0, math.pi / 2, 0), chrome, segs=24, bevel=0.002)

    # ---- three springs alongside the lower arm, behind it -------------------
    ua = (p1 - P0).normalized()
    for k, sx in enumerate((-0.019, 0.0, 0.019)):
        a = P0 + n1 * (0.020 if sx == 0 else 0.012) + Vector((sx, 0, 0)) + ua * 0.030
        b = a + ua * 0.125
        line = C.resample([a, b], 0.002)[0]
        pts = C.coil(line, coil_r=0.0050, pitch=0.0030, step=0.0030 / 6)
        sp = C.tube("spring", pts, 0.0009, sides=4, mat=chrome)
        sp["no_wn"] = True
        sp["sharp_angle"] = 89.0
        # hooks: a short straight leg at each end into the arm and the yoke
        C.tube("spring_leg", [a - ua * 0.012, a], 0.0009, sides=6, mat=chrome)
        C.tube("spring_leg", [b, b + ua * 0.012], 0.0009, sides=6, mat=chrome)

    # ---- shade, bulb, switch ----------------------------------------------
    q = axis.to_track_quat("Z", "Y").to_matrix().to_4x4()
    start = p2 + axis * 0.012
    from mathutils import Matrix
    M = Matrix.Translation(start) @ q
    sh = C.lathe("shade", shade_profile(), segs=56, mat=enamel, matrix=M)
    sh["no_wn"] = True
    sh["sharp_angle"] = 45.0
    bulb = C.lathe("bulb", [(0.0, 0.040), (0.013, 0.041), (0.014, 0.060), (0.022, 0.075),
                            (0.029, 0.095), (0.030, 0.110), (0.026, 0.128), (0.015, 0.140),
                            (0.0, 0.143)], segs=40, mat=bulb_m, matrix=M)
    bulb["no_wn"] = True
    bulb["sharp_angle"] = 60.0
    C.lathe("holder", [(0.0, 0.004), (0.018, 0.005), (0.018, 0.046), (0.0, 0.047)], segs=32,
            mat=enamel, matrix=M)
    side = Vector((0, axis.z, -axis.y))
    if side.z < 0:
        side = -side
    C.cyl("switch", 0.0055, 0.012, (start + axis * 0.018 + side * 0.036)[:],
          side.to_track_quat("Z", "Y").to_euler()[:], chrome, segs=20, bevel=0.0015)

    o = C.cli()
    ob, info = C.finish_prop("desk-lamp", "desk_lamp", ao_distance=0.05, edge_span=0.10,
                             ref={"z": TARGET_H, "y": TARGET_W}, render=o["render"],
                             preview_kw={"azimuth": -58, "elevation": 16, "fill": 1.0})
    info["pose_deg"] = {"lower_arm": alpha, "upper_arm": beta, "shade_down": gamma}
    info["base_diameter_m"] = {"model": round(BASE_D, 4), "ref": BASE_D}
    info["shade_m"] = {"model_d": SHADE_D, "model_len": SHADE_L, "ref": [0.144, 0.210]}
    C.report("desk-lamp", info)


if __name__ == "__main__":
    build()
