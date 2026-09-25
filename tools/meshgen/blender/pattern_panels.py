"""Turn a FreeSewing pattern (tools/meshgen/freesewing_draft.mjs's JSON) into flat cloth panels in Blender.

    blender -b -P tools/meshgen/blender/pattern_panels.py -- PATTERN.json OUT_DIR

WHY, 25 September: Jafar's clothing ruling, FreeSewing's open patterns sewn
and draped in Blender; the first garment is the Florent flat cap. This is the
first step: each part's seam outline becomes a flat panel of evenly spaced
triangles (cloth needs an even mesh to simulate), mirrored across its fold
where the pattern says "cut on fold", in metres, laid out side by side, with a
picture of the layout (panels.png) and a report (panels.json: each panel's
area, edge length and vertex count). Sewing and draping come after.
"""
import json
import math
import os
import sys

import bpy
import bmesh
from mathutils import Vector

argv = sys.argv[sys.argv.index("--") + 1:]
SRC, OUT = argv[0], argv[1]
os.makedirs(OUT, exist_ok=True)
EDGE = 0.008          # target cloth triangle edge, metres
# FROM THE PATTERN'S OWN CUT LIST (florent/src/*.mjs store.cutlist): the side
# band is cut once on the fold; the crown ("top") is cut twice, a left and a
# right joined by a centre seam; each brim layer once.
ON_FOLD = {"florent.side"}
CUT_PAIR = {"florent.top"}

pattern = json.load(open(SRC, encoding="utf-8"))
bpy.ops.wm.read_factory_settings(use_empty=True)


def outline(part):
    """The closed seam outline in metres (y up), or None. A part whose seam
    is open (cut on fold) is closed by its fold line and mirrored across it."""
    seam = part["paths"].get("seam")
    if not seam:
        return None, False
    pts = [(x / 1000.0, -y / 1000.0) for x, y in seam["points"]]
    if pts[0] == pts[-1]:
        pts = pts[:-1]
    fold = False
    pp = part["points"]
    if part.get("name") in ON_FOLD and "foldTop" in pp and "foldBottom" in pp:
        # the fold runs foldTop -> foldBottom: mirror the outline across it
        a = Vector((pp["foldTop"][0] / 1000.0, -pp["foldTop"][1] / 1000.0))
        b = Vector((pp["foldBottom"][0] / 1000.0, -pp["foldBottom"][1] / 1000.0))
        d = (b - a).normalized()
        def mirror(p):
            v = Vector(p) - a
            return tuple(a + d * v.dot(d) * 2 - v)
        on_fold = lambda p: abs((Vector(p) - a).cross(d)) < 1e-4
        # keep the outline's points off the fold, then walk back mirrored
        body = [p for p in pts]
        pts = body + [mirror(p) for p in reversed(body) if not on_fold(p)]
        fold = True
    return pts, fold


report = {}
x_at = 0.0
jobs = []
for name, part in pattern["parts"].items():
    part["name"] = name
    jobs.append((name, part, False))
    if name in CUT_PAIR:
        jobs.append((name + ".mirror", part, True))
for name, part, flip in jobs:
    pts, fold = outline(part)
    if pts and flip:
        pts = [(-x, y) for x, y in reversed(pts)]
    if not pts or len(pts) < 3:
        continue
    bm = bmesh.new()
    verts = [bm.verts.new((x, y, 0.0)) for x, y in pts]
    face = bm.faces.new(verts)
    bmesh.ops.triangulate(bm, faces=[face])
    # an even triangle mesh: subdivide long edges until none is over EDGE
    for _ in range(8):
        long = [e for e in bm.edges if e.calc_length() > EDGE * 1.6]
        if not long:
            break
        bmesh.ops.subdivide_edges(bm, edges=long, cuts=1, use_grid_fill=False)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
    bmesh.ops.beautify_fill(bm, faces=bm.faces[:], edges=bm.edges[:])
    minx = min(v.co.x for v in bm.verts)
    for v in bm.verts:
        v.co.x += x_at - minx
    maxx = max(v.co.x for v in bm.verts)
    x_at = maxx + 0.05
    me = bpy.data.meshes.new(name)
    bm.to_mesh(me)
    area = sum(f.calc_area() for f in bm.faces)
    bm.free()
    ob = bpy.data.objects.new(name.replace("florent.", ""), me)
    bpy.context.collection.objects.link(ob)
    report[name] = {"cutOnFold": fold, "vertices": len(me.vertices), "areaCm2": round(area * 1e4, 1),
                    "outlineMm": round(sum(math.dist(pts[i], pts[i - 1]) for i in range(len(pts))) * 1000, 1)}

# a picture of the layout, from above
scn = bpy.context.scene
cam = bpy.data.objects.new("Cam", bpy.data.cameras.new("Cam"))
scn.collection.objects.link(cam)
cam.data.type = "ORTHO"
xs = [ob.location.x + v.co.x for ob in scn.objects if ob.type == "MESH" for v in ob.data.vertices]
ys = [v.co.y for ob in scn.objects if ob.type == "MESH" for v in ob.data.vertices]
cam.location = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2, 2.0)
cam.data.ortho_scale = max(max(xs) - min(xs), (max(ys) - min(ys)) * 2) * 1.1
scn.camera = cam
scn.render.engine = "BLENDER_WORKBENCH"
scn.display.shading.show_object_outline = True
scn.render.resolution_x, scn.render.resolution_y = 1600, 800
scn.render.filepath = os.path.join(OUT, "panels.png")
bpy.ops.render.render(write_still=True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT, "panels.blend"))
json.dump(report, open(os.path.join(OUT, "panels.json"), "w"), indent=1)
print("PANELS " + json.dumps(report))
