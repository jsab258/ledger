"""The game mesh's texture layout: its pattern pieces packed into one square, the zip's two tapes joined at their
shared edge and drawn larger.

    blender -b --factory-startup -P tools/meshgen/blender/uv_pack_low.py -- LOW.blend PLAN.json IMPORT.json
        [--tape-scale 2.0] [--tex 2048] [--margin 0.008]

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
# 0.008, not 0.004 (28 October 2026, drape 19: at 0.004 the zip's island lay 6 px from its nearest neighbour at 2048,
# under the 8 px its bake margin and mipmaps need; 0.008 gives 10 px for 1.55 px/mm of cloth instead of 1.58)
MARGIN = opt("--margin", 0.008)
plan = json.load(open(PLAN, encoding="utf-8"))
imp = json.load(open(IMPORT, encoding="utf-8"))
NAMES = [p["key"] for p in plan["pieces"]]
# a garment with no zip (30 October 2026, Tom's jeans and jumper) has no tapes to join
HAS_TAPES = "tapeL" in plan.get("corners", {})
TAPE_W = max(x for n, x, y in plan["corners"]["tapeL"]) / 1000.0 if HAS_TAPES else 0.0    # the left tape's inner edge
TAPE_L = max(y for n, x, y in plan["corners"]["tapeL"]) / 1000.0 if HAS_TAPES else 0.0    # the tapes' length

bpy.ops.wm.open_mainfile(filepath=LOW)
low = bpy.data.objects["Low"]
me = low.data
bm = bmesh.new()
bm.from_mesh(me)
pat = bm.loops.layers.uv["pattern"]
uvm = bm.loops.layers.uv.get("UVMap") or bm.loops.layers.uv.new("UVMap")
pl = bm.faces.layers.int["piece"]
# A PIECE THE DRAPE STRETCHED DRAWN AT ITS DRAPED SIZE (28 October 2026, drape 19: its cuffs, gripped and caught on the
# wrist, cover 13 to 18% more cloth than their pattern, so drawn at pattern size they took 1.46 and 1.49 px/mm against
# the cloth's 1.5): each piece but the tapes enlarged by the root of its draped area over its pattern area, where that is
# over 1; pieces the drape did not stretch are drawn as before. The rib's ridges are drawn from "pattern", not from here.
a3_, ap_ = {}, {}
for f in bm.faces:
    n_ = NAMES[f[pl]]
    a3_[n_] = a3_.get(n_, 0.0) + f.calc_area()
    ps_ = [lp[pat].uv for lp in f.loops]
    ap_[n_] = ap_.get(n_, 0.0) + sum(abs((ps_[j] - ps_[0]).cross(ps_[j + 1] - ps_[0])) / 2 for j in range(1, len(ps_) - 1))
DRAPED = {n_: (1.0 if n_.startswith("tape") else max(1.0, math.sqrt(a3_[n_] / ap_[n_]))) for n_ in a3_}
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
            x, y = x * DRAPED[name], y * DRAPED[name]
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
# A BORDER ROUND THE SQUARE (drape 6's fresh review: the zip's island touched the texture's left edge, and its detail
# wrapped round to the far right, where the other maps say cloth): everything drawn in by --border pixels
BORDER = opt("--border", 8, int) / TEX
for d in me.uv_layers["UVMap"].data:
    d.uv = (BORDER + d.uv.x * (1 - 2 * BORDER), BORDER + d.uv.y * (1 - 2 * BORDER))

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
groups = [[n] for n in NAMES if not n.startswith("tape")] + ([[n for n in NAMES if n.startswith("tape")]] if HAS_TAPES else [])
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
res = {"low": LOW, "tex": TEX, "tapeScale": TAPE, "margin": MARGIN, "pxPerMm": ppm,
       "drapedScale": {n_: round(s_, 3) for n_, s_ in DRAPED.items() if s_ > 1.0}, "cover": round(float((cover > 0).sum()) / R / R, 3),
       "overlapShare": round(overlap, 5), "uvsOutsideSquare": out_of_square}
# THE PADDING, MEASURED AT THE MAP'S OWN SIZE (30 October 2026, the skill's 8 px; the margin is a share of the square,
# so at 1024 the jacket's 0.008 gives half the pixels it gives at 2048): each piece rasterised at --tex (the joined
# tapes one), then the nearest pixel of another piece searched ring by ring (square rings, so the distance read is
# never more than the true one), up to 24 px; and the nearest island pixel to the square's edge
lab = np.full((TEX, TEX), -1, dtype=np.int16)
gid = {n: k for k, grp in enumerate(groups) for n in grp}
for f in bm.faces:
    us = [lp[uvm].uv for lp in f.loops]
    xs = [u.x * TEX for u in us]
    ys = [u.y * TEX for u in us]
    x0, x1 = max(0, int(min(xs))), min(TEX - 1, int(max(xs)) + 1)
    y0, y1 = max(0, int(min(ys))), min(TEX - 1, int(max(ys)) + 1)
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
    lab[y0:y1 + 1, x0:x1 + 1][inside] = gid[NAMES[f[pl]]]
gap = None
for r_ in range(1, 25):
    offs_ = [(dx_, r_) for dx_ in range(-r_, r_ + 1)] + [(r_, dy_) for dy_ in range(-r_ + 1, r_)]
    for dx_, dy_ in offs_:
        A_ = lab[max(0, dy_):TEX + min(0, dy_), max(0, dx_):TEX + min(0, dx_)]
        B_ = lab[max(0, -dy_):TEX + min(0, -dy_), max(0, -dx_):TEX + min(0, -dx_)]
        if ((A_ >= 0) & (B_ >= 0) & (A_ != B_)).any():
            gap = r_
            break
    if gap is not None:
        break
ys_, xs_ = np.nonzero(lab >= 0)
res["islandGapPx"] = gap if gap is not None else ">24"
res["borderPx"] = int(min(xs_.min(), ys_.min(), TEX - 1 - xs_.max(), TEX - 1 - ys_.max())) if len(xs_) else None
bm.free()
bpy.ops.wm.save_as_mainfile(filepath=LOW)
json.dump(res, open(os.path.join(os.path.dirname(LOW), "uvpack.json"), "w", encoding="utf-8"), indent=1)
print("UVPACK", json.dumps(res))
