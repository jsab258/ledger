"""The office telephone: a late-1980s British push-button desk telephone of the
slim kind (handset lying lengthways on a low sloping base, keypad beside it),
stone-grey ABS with darker keys and a coiled handset cord. Generic, no maker's
name, badge or layout; the key legends are left for a decal.

    blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/telephone.py [-- --no-render]

SIZE (read 6 October 2026): MoDiP AIBDC 005579, Viscount telephone, ABS,
STC for British Telecom, c.1981-1989: width 146 mm, height 114 mm,
depth 241 mm, https://www.modip.ac.uk/artefact/aibdc-005579
(the Science Museum Group's Viscount, 1982-1995, object 2004-136, was read for
the period and fittings: twelve keys plus function keys, coiled cord,
https://collection.sciencemuseumgroup.org.uk/objects/co8054884/viscount-telephone-1982-1995).
The envelope is that class's; the shapes are this recipe's own.
Origin: centre of the feet, z = 0; front (keypad edge) toward -Y; handset on
the left, its cord coiled on the desk at the left.
"""
import math
import os
import sys

from mathutils import Vector

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _desk_common as C  # noqa: E402

W, D, H = 0.146, 0.241, 0.114
ZF, ZB = 0.048, 0.072              # body top at the front and back edges
SLOPE = math.atan((ZB - ZF) / D)


def top_z(y):
    return ZF + (y + D / 2) * (ZB - ZF) / D


def build():
    C.reset()
    body_m = C.material("telephone_abs_stone", (0.63, 0.60, 0.53), 0.45)
    key_m = C.material("telephone_keys_grey", (0.30, 0.30, 0.29), 0.38)
    black = C.material("telephone_black", (0.05, 0.05, 0.05), 0.5)

    # ---- base: a low wedge, rounded --------------------------------------
    prof = [(-D / 2, 0.004), (D / 2, 0.004), (D / 2, ZB), (-D / 2, ZF)]
    b = C.extrude_profile("base", prof, -W / 2, W / 2, body_m, plane="YZ")
    C.bevel_part(b, 0.007, 3, angle=25)
    # a shallow plinth line round the bottom, black rubber feet
    C.box_z("plinth", -W / 2 + 0.004, W / 2 - 0.004, -D / 2 + 0.004, D / 2 - 0.004, 0.002, 0.007,
            black, bevel=0.002, segs=2)
    for sx in (-1, 1):
        for sy in (-1, 1):
            C.cyl("foot", 0.006, 0.003, (sx * 0.055, sy * 0.095, 0.0015), mat=black, segs=16)

    def on_top(x, y, lift, size, mat, name, bevel=0.0015, segs=2):
        z = top_z(y) + lift
        return C.box(name, size, (x, y, z), mat, rot=(SLOPE, 0, 0), bevel=bevel, segs=segs)

    # ---- keypad on the right: 4 x 3 keys and a row of three function keys
    cols = (0.018, 0.038, 0.058)
    rows = (-0.100, -0.080, -0.060, -0.040)
    on_top(0.038, -0.064, -0.0010, (0.066, 0.090, 0.0060), black, "key_well", bevel=0.0015, segs=2)
    for y in rows:
        for x in cols:
            on_top(x, y, 0.0028, (0.0145, 0.0125, 0.0060), key_m, "key", bevel=0.0018, segs=2)
    for x in cols:
        on_top(x, -0.016, 0.0022, (0.0145, 0.0080, 0.0050), key_m, "fkey", bevel=0.0016, segs=2)
    # ringer grille: five slots at the back right
    for i in range(5):
        y = 0.040 + i * 0.012
        on_top(0.040, y, 0.0002, (0.050, 0.0045, 0.0016), black, "slot", bevel=0.0008, segs=1)

    # ---- cradle rests and the hook-switch plunger on the left ------------
    hx = -0.036
    for y in (-0.090, 0.082):
        on_top(hx, y, 0.0035, (0.050, 0.022, 0.010), body_m, "rest", bevel=0.003, segs=2)
    on_top(hx, 0.000, 0.0015, (0.010, 0.022, 0.006), black, "hook", bevel=0.002, segs=2)

    # ---- handset: grip bar between two pods, lying on the rests ------------
    zb = 0.0
    hp = [(-0.110, zb + 0.005), (-0.104, zb), (-0.068, zb), (-0.058, zb + 0.013),
          (0.053, zb + 0.013), (0.063, zb), (0.099, zb), (0.105, zb + 0.005),
          (0.105, zb + 0.029), (0.100, zb + 0.034), (-0.104, zb + 0.034), (-0.110, zb + 0.029)]
    hs = C.extrude_profile("handset", hp, -0.024, 0.024, body_m, plane="YZ")
    rest_top = top_z(-0.090) + 0.0035 + 0.005          # top of the front rest
    M = C.mat4((hx, -0.004, 0), (SLOPE, 0, 0))
    hs.data.transform(M)
    # lift so the pods sit on the rests
    lift = rest_top - min(v.co.z for v in hs.data.vertices if v.co.y < -0.06)
    hs.data.transform(C.mat4((0, 0, lift)))
    C.bevel_part(hs, 0.0045, 3, angle=25)
    # ear and mouth caps: black discs on the pods' undersides show at the ends
    front_end = Vector((hx, -0.116, rest_top + 0.006))

    # ---- coiled handset cord: from the mouthpiece end to the left side -----
    socket = Vector((-W / 2 - 0.002, -0.050, 0.022))
    s0 = Vector((hx, -0.113, front_end.z + 0.002))
    tail_a = [s0 + Vector((0, 0.006, 0.004)), s0, s0 + Vector((-0.002, -0.010, -0.010))]
    cpath = C.catmull([tail_a[-1], Vector((-0.046, -0.140, 0.024)), Vector((-0.072, -0.152, 0.006)),
                       Vector((-0.108, -0.132, 0.0055)), Vector((-0.118, -0.085, 0.0055)),
                       Vector((-0.100, -0.052, 0.008)), Vector((-0.086, -0.050, 0.016))], per_seg=10)
    pts = C.coil(cpath, coil_r=0.0040, pitch=0.0048, step=0.0048 / 8, floor_z=0.0015)
    C.tube("cord_coil", pts, 0.00135, sides=5, mat=body_m)
    C.tube("cord_tail_a", C.resample(C.catmull(tail_a, 4), 0.003)[0], 0.0020, sides=8, mat=body_m)
    tb = C.resample(C.catmull([Vector((-0.086, -0.050, 0.016)), Vector((-0.079, -0.050, 0.020)),
                               socket], 4), 0.002)[0]
    C.tube("cord_tail_b", tb, 0.0020, sides=8, mat=body_m)
    C.cyl("cord_boot", 0.0034, 0.010, (-W / 2 + 0.002, -0.050, 0.022), (0, math.pi / 2, 0), black,
          segs=16, r2=0.0026)
    for ob in C.PARTS:
        if ob.name.startswith("cord"):
            ob["no_wn"] = True
            ob["sharp_angle"] = 89.0

    # envelope without the cord (the reference is measured without it)
    lo = Vector((1, 1, 1))
    hi = Vector((-1, -1, -1))
    for o in C.PARTS:
        if o.name.startswith("cord"):
            continue
        for v in o.data.vertices:
            lo = Vector((min(lo.x, v.co.x), min(lo.y, v.co.y), min(lo.z, v.co.z)))
            hi = Vector((max(hi.x, v.co.x), max(hi.y, v.co.y), max(hi.z, v.co.z)))
    env = hi - lo

    o = C.cli()
    ob, info = C.finish_prop("telephone", "telephone", ao_distance=0.025, edge_span=0.10,
                             render=o["render"], preview_kw={"azimuth": -36, "elevation": 30})
    info["envelope_without_cord"] = {
        "model_m": {"x": round(env.x, 4), "y": round(env.y, 4), "z": round(env.z, 4)},
        "ref_m": {"x": W, "y": D, "z": H},
        "diff_pct": {k: round(100 * (a - b) / b, 2) for k, a, b in
                     (("x", env.x, W), ("y", env.y, D), ("z", env.z, H))}}
    C.report("telephone", info)


if __name__ == "__main__":
    build()
