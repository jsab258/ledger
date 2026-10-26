"""The game mesh's texture layout: its pattern pieces packed into one square, the zip's two tapes joined at their
shared edge and drawn larger.

    blender -b --factory-startup -P tools/meshgen/blender/uv_pack_low.py -- LOW.blend PLAN.json IMPORT.json
        [--tape-scale 2.0] [--tex 2048] [--margin 0.004]

WHY, 27 October 2026 (Tom's zip jacket, the bake chain's step 5: production/art/clothing/tom-outfit/
BAKE-PLAN-2026-10-27.md). retopo_pieces.py keeps each piece's true-size "pattern" layer; the textures need every
piece in one 0-to-1 square ("UVMap"). The zip's teeth are baked along the line where the two tapes meet, so the two
tapes are laid edge to edge there (no seam in the texture across the zip), and drawn --tape-scale times larger than
the cloth so a tooth gets enough pixels (the route's review: 1.5 px/mm over the jacket would give a tooth 2 to 5).

Checks written to uvpack.json beside LOW.blend: each piece's pixels per millimetre at --tex, the tapes' too, and
the share of the square covered by two islands at once (overlap; must be 0).
"""
import json
import math
import os
import sys

import bmesh
import bpy
import numpy as np

argv = sys.argv[sys.argv.index("--") + 1:]
LOW, PLAN, IMPORT = argv[0], argv[1], argv[2]
opt = lambda n, d, f=float: f(argv[argv.index(n) + 1]) if n in argv else d  # noqa: E731
TAPE = opt("--tape-scale", 2.0)
TEX = opt("--tex", 2048, int)
MARGIN = opt("--margin", 0.004)
plan = json.load(open(PLAN, encoding="utf-8"))
imp = json.load(open(IMPORT, encoding="utf-8"))
NAMES = [p["key"] for p in plan["pieces"]]
TAPE_W = max(x for n, x, y in plan["corners"]["tapeL"]) / 1000.0     # the left tape's inner edge, plan metres
TAPE_L = max(y for n, x, y in plan["corners"]["tapeL"]) / 1000.0     # the tapes' length

bpy.ops.wm.open_mainfile(filepath=LOW)
low = bpy.data.objects["Low"]
me = low.data
bm = bmesh.new()
bm.from_mesh(me)
pat = bm.loops.layers.uv["pattern"]
uvm = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
pl = bm.faces.layers.int["piece"]
# each piece back to its own plan coordinates (metres), then the tapes joined and enlarged
for f in bm.faces:
    name = NAMES[f[pl]]
    off = imp["pieces"][name]["layoutOffsetM"]
    for lp in f.loops:
        x, y = lp[pat].uv.x - off, lp[pat].uv.y
        if name == "tapeL":
            x -= 2 * TAPE_W            # its inner edge (+W) onto the right tape's (-W)
        if name.startswith("tape"):
            # THE ZIP CUT ONCE, AT MID-FRONT (the first packs: the joined tapes at x2 are a strip 1.39 m long, and the
            # square had to hold it, which held the cloth at 2048 / 1386 = 1.48 px/mm): the upper half its own island
            upper = sum(l[pat].uv.y for l in f.loops) / len(f.loops) > TAPE_L / 2
            x, y = x * TAPE, y * TAPE + (5.0 if upper else 0.0)
        else:
            x += 10.0 * (f[pl] + 1)     # every other piece well apart before packing
        lp[uvm].uv = (x, y)
bm.to_mesh(me)
bm.free()
me.uv_layers.active = me.uv_layers["UVMap"]
me.uv_layers["UVMap"].active_render = True

bpy.context.view_layer.objects.active = low
for o in bpy.data.objects:
    o.select_set(o is low)
bpy.ops.object.mode_set(mode="EDIT")
bpy.ops.mesh.select_all(action="SELECT")
bpy.ops.uv.select_all(action="SELECT")
# packed by each island's exact outline, not its box (the first pack, by default, covered 65% of the square and left
# the cloth at 1.44 to 1.48 px/mm against the plan's 1.5)
bpy.ops.uv.pack_islands(rotate=True, margin=MARGIN, shape_method="CONCAVE")
bpy.ops.object.mode_set(mode="OBJECT")

# THE CHECKS: pixels per millimetre per piece; islands overlapping (each island rasterised at 512, counted)
bm = bmesh.new()
bm.from_mesh(me)
uvm = bm.loops.layers.uv["UVMap"]
pl = bm.faces.layers.int["piece"]
area3, areauv = {}, {}
for f in bm.faces:
    n = NAMES[f[pl]]
    area3[n] = area3.get(n, 0.0) + f.calc_area()
    us = [lp[uvm].uv for lp in f.loops]
    a = 0.0
    for j in range(1, len(us) - 1):
        a += abs((us[j] - us[0]).cross(us[j + 1] - us[0])) / 2
    areauv[n] = areauv.get(n, 0.0) + a
ppm = {n: round(math.sqrt(areauv[n] / area3[n]) * TEX / 1000.0, 3) for n in NAMES}
R = 512
cover = np.zeros((R, R), dtype=np.int32)
# the two tapes are one island (joined at their shared edge), so they are rasterised together
groups = [[n] for n in NAMES if not n.startswith("tape")] + [[n for n in NAMES if n.startswith("tape")]]
for grp in groups:
    mask = np.zeros((R, R), dtype=bool)
    for f in bm.faces:
        if NAMES[f[pl]] not in grp:
            continue
        us = [lp[uvm].uv for lp in f.loops]
        xs = [u.x * R for u in us]
        ys = [u.y * R for u in us]
        x0, x1 = max(0, int(min(xs))), min(R - 1, int(max(xs)) + 1)
        y0, y1 = max(0, int(min(ys))), min(R - 1, int(max(ys)) + 1)
        if x1 < x0 or y1 < y0:
            continue
        gx, gy = np.meshgrid(np.arange(x0, x1 + 1) + 0.5, np.arange(y0, y1 + 1) + 0.5)
        inside = np.zeros_like(gx, dtype=bool)
        for j in range(1, len(us) - 1):
            ax, ay, bx, by, cx, cy = xs[0], ys[0], xs[j], ys[j], xs[j + 1], ys[j + 1]
            d = (by - cy) * (ax - cx) + (cx - bx) * (ay - cy)
            if abs(d) < 1e-12:
                continue
            l1 = ((by - cy) * (gx - cx) + (cx - bx) * (gy - cy)) / d
            l2 = ((cy - ay) * (gx - cx) + (ax - cx) * (gy - cy)) / d
            inside |= (l1 >= 0) & (l2 >= 0) & (l1 + l2 <= 1)
        mask[y0:y1 + 1, x0:x1 + 1] |= inside
    cover += mask.astype(np.int32)
out_of_square = 0
for f in bm.faces:
    for lp in f.loops:
        u = lp[uvm].uv
        out_of_square += not (0.0 <= u.x <= 1.0 and 0.0 <= u.y <= 1.0)
overlap = float((cover > 1).sum()) / float((cover > 0).sum())
res = {"low": LOW, "tex": TEX, "tapeScale": TAPE, "pxPerMm": ppm, "cover": round(float((cover > 0).sum()) / R / R, 3),
       "overlapShare": round(overlap, 5), "uvsOutsideSquare": out_of_square}
bm.free()
bpy.ops.wm.save_as_mainfile(filepath=LOW)
json.dump(res, open(os.path.join(os.path.dirname(LOW), "uvpack.json"), "w", encoding="utf-8"), indent=1)
print("UVPACK", json.dumps(res))
