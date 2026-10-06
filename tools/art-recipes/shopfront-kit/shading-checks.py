r"""Workbench shading checks of the kit's six pieces from their saved .blend files: the whole piece
and close views where faults would show (bevels, mouldings, mullions, fittings), in one Blender
process so the graphics card is used for seconds only. The card is checked before EVERY render;
a busy card (UnrealEditor or Runner.Worker running) stops that render and the rest (exit 3).
The piece scripts render the same check themselves when the card is free; this is for the
moments it is free only briefly.

    blender.exe -b --factory-startup -P tools/art-recipes/shopfront-kit/shading-checks.py

Writes F:\LedgerTools\shopfront-kit\previews\checks\<piece>_shading.png and <piece>_shading_close<n>.png.
"""
import math
import os
import subprocess
import sys

import bpy
from mathutils import Vector

BLEND = r"F:\LedgerTools\shopfront-kit\blend"
OUT = r"F:\LedgerTools\shopfront-kit\previews\checks"
PIECES = ["pilaster", "stallriser_panelled", "stallriser_tile", "window_frame", "shop_door", "side_door"]
# whole piece, then close views (target, distance) where faults would show
CLOSE = {"pilaster": [((0.0, -0.08, 0.62), 0.9), ((0.0, -0.08, 2.65), 0.9)],
         "stallriser_panelled": [((-1.2, -0.1, 0.35), 1.2)],
         "stallriser_tile": [((-1.2, -0.1, 0.35), 1.0)],
         "window_frame": [((-0.54, -0.05, 2.42), 0.9)],
         "shop_door": [((0.3, -0.08, 1.0), 0.8), ((0.0, -0.05, 2.3), 1.2)],
         "side_door": [((0.15, -0.06, 1.05), 1.3)]}


def busy():
    try:
        out = subprocess.run(["tasklist", "/FO", "CSV", "/NH"], capture_output=True, text=True, timeout=60).stdout.lower()
    except Exception as e:  # noqa: BLE001
        print("WB GPU CHECK FAILED", e)
        return True
    hits = [n for n in ("unrealeditor", "runner.worker") if n in out]
    if hits:
        print("WB GPU BUSY", hits)
    return bool(hits)


def shoot(path, ctr, dist, az=-30.0, el=12.0, lens=55.0):
    sc = bpy.context.scene
    cam = bpy.data.objects.new("_wbcam", bpy.data.cameras.new("_wbcam"))
    sc.collection.objects.link(cam)
    cam.data.lens = lens
    a, e = math.radians(az), math.radians(el)
    d = Vector((math.sin(a) * math.cos(e), -math.cos(a) * math.cos(e), math.sin(e)))
    cam.location = Vector(ctr) + d * dist
    cam.rotation_euler = (-d).to_track_quat("-Z", "Y").to_euler()
    sc.camera = cam
    if busy():
        sys.exit(3)
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
    print("WB SAVED", path)
    bpy.data.objects.remove(cam)


os.makedirs(OUT, exist_ok=True)
for p in PIECES:
    bpy.ops.wm.open_mainfile(filepath=os.path.join(BLEND, p + ".blend"))
    sc = bpy.context.scene
    objs = [o for o in sc.objects if o.type == "MESH" and not o.name.startswith("_")]
    for o in list(sc.objects):
        if o.type == "CAMERA":
            bpy.data.objects.remove(o)
    pts = [o.matrix_world @ Vector(c) for o in objs for c in o.bound_box]
    lo = Vector((min(q.x for q in pts), min(q.y for q in pts), min(q.z for q in pts)))
    hi = Vector((max(q.x for q in pts), max(q.y for q in pts), max(q.z for q in pts)))
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "SINGLE"
    sh.single_color = (0.6, 0.6, 0.6)
    sh.show_specular_highlight = True
    sc.render.resolution_x = sc.render.resolution_y = 800
    sc.render.resolution_percentage = 100
    sc.render.image_settings.file_format = "PNG"
    rad = (hi - lo).length / 2
    fov = 2 * math.atan(18 / 55)
    shoot(os.path.join(OUT, p + "_shading.png"), (lo + hi) / 2, rad / math.sin(fov / 2))
    for k, (ctr, dist) in enumerate(CLOSE[p]):
        shoot(os.path.join(OUT, "%s_shading_close%d.png" % (p, k)), ctr, dist, az=-35.0, el=15.0)
print("WB DONE")
