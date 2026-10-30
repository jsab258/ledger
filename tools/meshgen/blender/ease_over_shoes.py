"""FAILED ITS ONE TRY, 30 October 2026, and set aside (kept for the record): on Tom's jeans over his boots the hems
no longer sank into the boots (0 to 6 points, from 28), but the boots' laced fronts tore jagged holes through the jeans'
fronts (about 200 boot points outside the cloth a leg): a coarse game mesh moved point by point cannot drape over a
laced instep. A cloth that rests on a solid is draped over it, or cut to fit it.

A skinned trouser's lower legs eased out over the wearer's footwear: every point of the cloth that lies inside the
shoes, or nearer their surface than a clearance, is set out to the clearance along the shoe's normal, and the move is
spread smoothly up the leg, so the hem rests on the shoe instead of sinking into it. Weights, UVs and maps are kept.

    blender -b TROUSERS_SKINNED.blend -P tools/meshgen/blender/ease_over_shoes.py -- SHOES.fbx OUT_DIR NAME
            [--clear 0.004] [--below 0.17] [--fade 0.30] [--reach 0.04] [--rounds 3]

WHY, 30 October 2026 (his order C9 and his ruling on Tom's shoes: the boots Ron wears, under the jeans): Tom's jeans
were draped over a bare foot, so with his boots on their hems sink into the boots all round (29 of 32 hem points a
leg). Draping again over the boots failed twice (drape n5: the 16.5 in hem caught on the laces in one pinched break and
stretched round the boot); widening the hem would change the jean's cut. So the drape that passed is kept and only its
lower legs are moved, the way the boots themselves were set out from his foot: the professional clean-up of a cloth
that rests on a solid, done once here instead of by simulation in the game.

WHAT IT DOES: points of NAME under BELOW metres (the shoes' top plus a centimetre: higher, the shoe's top edge would
pull the shin down onto it, the first run's 196 mm move) and within REACH of the shoes' surface are tested against
SHOES.fbx (in the same space: both made on the wearer's reference pose); a point inside, or within CLEAR of it, takes a fixed
move to the surface plus CLEAR along its normal; every other point under FADE metres takes the average move of its mesh
neighbours, repeated until it settles (a harmonic fill), points above FADE fixed; then the test again, ROUNDS times.
OUT_DIR gets NAME_skinned.fbx (skin_garment.py's export), NAME_skinned.blend and ease.json.
"""
import json
import os
import sys
from collections import defaultdict

import bpy
from mathutils import Vector
from mathutils.bvhtree import BVHTree

argv = sys.argv[sys.argv.index("--") + 1:]
SHOES, OUT, NAME = argv[:3]


def opt(name, default, kind=float):
    return kind(argv[argv.index(name) + 1]) if name in argv else default


CLEAR, BELOW, FADE, ROUNDS = opt("--clear", 0.004), opt("--below", 0.17), opt("--fade", 0.30), opt("--rounds", 3, int)
REACH = opt("--reach", 0.04)
os.makedirs(OUT, exist_ok=True)
g = bpy.data.objects[NAME]
arm = next(o for o in bpy.data.objects if o.type == "ARMATURE")
before = set(bpy.data.objects)
bpy.ops.import_scene.fbx(filepath=SHOES)
shoes = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
sv, st = [], []
for o in shoes:
    me = o.data
    me.calc_loop_triangles()
    base = len(sv)
    sv += [o.matrix_world @ v.co for v in me.vertices]
    st += [tuple(base + i for i in t.vertices) for t in me.loop_triangles]
tree = BVHTree.FromPolygons(sv, st)

gw, gwi = g.matrix_world, g.matrix_world.inverted()
rest = [gw @ v.co for v in g.data.vertices]
n = len(rest)
nbrs = defaultdict(set)
for e in g.data.edges:
    a, b = e.vertices
    nbrs[a].add(b)
    nbrs[b].add(a)
zero = Vector((0.0, 0.0, 0.0))
move = [zero.copy() for _ in range(n)]
fixed = {}
low = [i for i in range(n) if rest[i].z < FADE]
history = []
# EACH SHOE'S UPRIGHT LINE (the second run: a shoe is a solid with an inner lining, so a hem point inside the shoe, nearest
# its lining, read as outside): its points' mean across, per side of the body, so a point is tested by a ray from it
# straight out from its own shoe's line; the shoe's last face along that ray is its outer surface
sides = {s: [v for v in sv if (v.x < 0) == (s < 0)] for s in (-1, 1)}
axis = {s: Vector((sum(v.x for v in vs) / len(vs), sum(v.y for v in vs) / len(vs), 0.0)) for s, vs in sides.items() if vs}


def outer_hit(p):
    """The shoe's outermost face straight out from its line through p, within REACH, or None."""
    a = axis.get(-1 if p.x < 0 else 1)
    if a is None:
        return None
    d = Vector((p.x - a.x, p.y - a.y, 0.0))
    if d.length < 1e-6:
        return None
    d.normalize()
    last, start = None, p.copy()
    for _ in range(8):
        hit, _nrm, _fi, dist = tree.ray_cast(start, d, REACH)
        if hit is None:
            break
        last = hit
        start = hit + d * 1e-4
    return last, d


for rnd in range(ROUNDS):
    added = 0
    for i in low:
        p = rest[i] + move[i]
        if p.z > BELOW or i in fixed:
            continue
        out = outer_hit(p)
        if out is not None and out[0] is not None:
            fixed[i] = (out[0] + out[1] * CLEAR) - rest[i]          # under the shoe's outer surface: set out past it
            added += 1
            continue
        hit, nrm, _fi, dist = tree.find_nearest(p)
        if hit is None or dist > REACH:
            continue
        side = (p - hit).dot(nrm)
        if side < CLEAR:
            fixed[i] = (hit + nrm * CLEAR) - rest[i]
            added += 1
    for i, d in fixed.items():
        move[i] = d.copy()
    free = [i for i in low if i not in fixed]
    for _ in range(300):
        for i in free:
            ns = nbrs[i]
            if not ns:
                continue
            acc = zero.copy()
            for j in ns:
                acc += move[j] if rest[j].z < FADE else zero
            move[i] = acc / len(ns)
    history.append({"round": rnd + 1, "fixedNew": added, "fixedTotal": len(fixed)})
    if added == 0:
        break

for i in range(n):
    if move[i].length > 0:
        g.data.vertices[i].co = gwi @ (rest[i] + move[i])
g.data.update()
peak = max((m.length for m in move), default=0.0)
moved = sum(1 for m in move if m.length > 1e-4)
for o in shoes:
    bpy.data.objects.remove(o, do_unlink=True)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from uv_order import maps_layout_first  # noqa: E402

reordered = maps_layout_first(g)
bpy.ops.object.select_all(action="DESELECT")
arm.select_set(True)
g.select_set(True)
bpy.context.view_layer.objects.active = arm
for o in bpy.data.objects:
    if o.type == "MESH" and o is not g:
        o.select_set(False)
bpy.ops.export_scene.fbx(filepath=os.path.join(OUT, NAME + "_skinned.fbx"), use_selection=True,
                         object_types={"ARMATURE", "MESH"}, add_leaf_bones=False, mesh_smooth_type="OFF", use_tspace=True,
                         colors_type="LINEAR", bake_anim=False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, NAME + "_skinned.blend"))
rep = {"clear_m": CLEAR, "below_m": BELOW, "fade_m": FADE, "reach_m": REACH, "rounds": history, "points_moved": moved,
       "move_peak_mm": round(peak * 1000, 1), "uvReordered": reordered}
json.dump(rep, open(os.path.join(OUT, "ease.json"), "w"), indent=1)
print("EASE " + json.dumps(rep), flush=True)
