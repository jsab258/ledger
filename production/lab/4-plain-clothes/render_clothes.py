"""Workbench pictures of Ron in the modelled jumper and trousers: front, side, back, three-quarter.

    blender -b --factory-startup --python render_clothes.py -- clothes.npz outdir tag

Workbench only. The body is a plain grey figure; the jumper an oatmeal wool colour, the
trousers charcoal; flat colours, so the outline and the fit read.
"""
import math
import os
import sys

import bpy
import numpy as np

COL = {"jumper": (0.74, 0.68, 0.56, 1), "sleeve": (0.74, 0.68, 0.56, 1), "trouser": (0.20, 0.20, 0.22, 1), "body": (0.62, 0.60, 0.58, 1)}


def mesh(name, V, F, rgba, smooth=True):
    me = bpy.data.meshes.new(name)
    me.from_pydata([tuple(v) for v in V], [], [tuple(int(i) for i in f) for f in F])
    me.validate()
    for p in me.polygons:
        p.use_smooth = smooth
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    m = bpy.data.materials.new(name + "_m")
    m.diffuse_color = rgba
    m.roughness = 0.9
    me.materials.append(m)
    return ob


def cam(name, loc, look, lens=85):
    c = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, c)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = [look[i] - loc[i] for i in range(3)]
    ob.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    c.lens = lens
    return ob


def main():
    a = sys.argv[sys.argv.index("--") + 1:]
    g = np.load(a[0])
    out, tag = a[1], a[2]
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    b = np.load(r"F:/LedgerTools/lab/jacket/ronfull_down.npz")
    mesh("body", b["LOD0_V"], b["LOD0_F"], COL["body"])
    names = sorted({k[:-2] for k in g.files if k.endswith("_V")})
    for n in names:
        key = "trouser" if n.startswith("trouser") else ("sleeve" if n.startswith("sleeve") else "jumper")
        mesh(n, g[n + "_V"], g[n + "_F"], COL[key])
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "MATERIAL"
    sh.show_shadows, sh.shadow_intensity = True, 0.45
    sh.show_cavity, sh.cavity_type = True, "BOTH"
    sc.display.light_direction = (0.35, -0.6, 0.72)
    sc.render.resolution_x, sc.render.resolution_y = 1000, 1600
    sc.world = bpy.data.worlds.new("w")
    sc.world.color = (0.80, 0.80, 0.80)
    sh.background_type = "WORLD"
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    zc = 0.95
    D = 5.6                                      # 85 mm lens: a 2.3 m tall frame round the figure
    shots = {"front": cam("front", (0, -D, zc), (0, 0, zc)), "side": cam("side", (D, 0, zc), (0, 0, zc)),
             "back": cam("back", (0, D, zc), (0, 0, zc)), "three_quarter": cam("tq", (-0.56 * D, -0.83 * D, zc + 0.2), (0, 0, zc))}
    for nm, c in shots.items():
        sc.camera = c
        sc.render.filepath = os.path.join(out, "%s_%s.jpg" % (tag, nm))
        bpy.ops.render.render(write_still=True)
        print("RENDERED", sc.render.filepath)


if __name__ == "__main__":
    main()
