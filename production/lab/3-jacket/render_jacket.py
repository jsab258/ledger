"""Workbench pictures of the draped jacket on Ron's body, for the outline check and the reviewer.

    blender -b --factory-startup --python render_jacket.py -- sewn.npz body.npz outdir [tag]

Workbench only (the light render mode). Front, side, three-quarter and a close
view of the lapels; orthographic front and side for outlines, perspective for
the reviewer. The body is a plain grey figure (no head, as exported); the jacket
a flat charcoal so its outline and folds read.
"""
import math
import os
import sys

import bpy
import numpy as np


def mesh(name, V, F, rgba):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], [], [tuple(f) for f in F])
    me.validate()
    for p in me.polygons:
        p.use_smooth = True
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new(name + "_m")
    m.diffuse_color = rgba
    m.roughness = 0.8
    me.materials.append(m)
    return ob


def cam(name, loc, look, lens=None, ortho=None):
    c = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, c)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = [look[i] - loc[i] for i in range(3)]
    ob.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    if ortho:
        c.type = "ORTHO"
        c.ortho_scale = ortho
    else:
        c.lens = lens or 50
    return ob


def main():
    a = sys.argv[sys.argv.index("--") + 1:]
    g, b = np.load(a[0]), np.load(a[1])
    out = a[2]
    tag = a[3] if len(a) > 3 else "j"
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    key = "LOD0" if "LOD0_V" in b.files else sorted(k[:-2] for k in b.files if k.endswith("_V"))[0]
    mesh("body", b[key + "_V"], b[key + "_F"], (0.55, 0.55, 0.56, 1))
    j = mesh("jacket", g["garment_V"], g["garment_F"], (0.16, 0.16, 0.18, 1))
    sol = j.modifiers.new("thick", "SOLIDIFY")
    sol.thickness = 0.002
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "MATERIAL"
    sh.show_shadows, sh.shadow_intensity = True, 0.5
    sh.show_cavity, sh.cavity_type = True, "BOTH"
    sc.display.light_direction = (0.35, -0.6, 0.72)
    sc.render.resolution_x, sc.render.resolution_y = 1200, 1600
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    zc = 1.25
    shots = {"front": cam("front", (0, -6, zc), (0, 0, zc), lens=85),
             "side": cam("side", (6, 0, zc), (0, 0, zc), lens=85),
             "three_quarter": cam("tq", (-3.2, -4.6, zc + 0.2), (0, 0, zc), lens=85),
             "lapels": cam("lap", (-0.35, -1.25, 1.45), (0, -0.1, 1.36), lens=50),
             "back": cam("back", (0, 6, zc), (0, 0, zc), lens=85)}
    for nm, c in shots.items():
        sc.camera = c
        sc.render.filepath = os.path.join(out, "%s_%s.jpg" % (tag, nm))
        bpy.ops.render.render(write_still=True)
        print("RENDERED", sc.render.filepath)


if __name__ == "__main__":
    main()
