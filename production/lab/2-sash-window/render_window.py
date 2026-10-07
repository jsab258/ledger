"""Workbench pictures of the built window in a plain brick opening, for the fresh reviewer.

    blender -b --factory-startup --python render_window.py -- parts.json target.json outdir

Workbench only (the light render mode; no Cycles, no EEVEE). The wall is a plain
slab with the brick opening, the reveal and a stone sill from target.json, so the
window is seen as on a terrace: from the front, from an oblique angle that shows
the reveal and the sashes' offset, and close up at the meeting rail and horns.
"""
import json
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import blender_parts  # noqa: E402

COL = {"paint": (0.97, 0.96, 0.92, 1), "glass": (0.16, 0.19, 0.21, 1), "arch": (0.50, 0.27, 0.19, 1),
       "brick": (0.42, 0.22, 0.15, 1), "stone": (0.62, 0.60, 0.55, 1)}


def material(name):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = COL.get(name, (0.8, 0.8, 0.8, 1))
    if name == "glass":
        m.roughness = 0.05
        m.metallic = 0.3
    return m


def wall(T):
    o, f = T["opening"], T["frame"]
    W, H = o["width_mm"] / 1000, o["height_mm"] / 1000
    depth = T.get("wall", {}).get("thickness_mm", 230) / 1000
    span = 2.2
    parts = []
    # four slabs round the opening, front face at y=0
    for nm, x0, x1, z0, z1 in (("wall_L", -span, -W / 2 - 0.05, -1.0, H + 1.0), ("wall_R", W / 2 + 0.05, span, -1.0, H + 1.0),
                               ("wall_Li", -W / 2 - 0.05, -W / 2, -1.0, H), ("wall_Ri", W / 2, W / 2 + 0.05, -1.0, H),
                               ("wall_top", -W / 2 - 0.05, W / 2 + 0.05, H + 0.2286, H + 1.0), ("wall_top_back", -W / 2, W / 2, H, H + 0.2286),
                               ("wall_bot", -W / 2, W / 2, -1.0, -0.127)):
        parts.append({"name": nm, "material": "brick", "profile": [[x0, 0], [x1, 0], [x1, depth], [x0, depth]],
                      "axis": "z", "plane": ["x", "y"], "start": z0, "end": z1})
    ss = T.get("stone_sill", {"projection_mm": 50, "height_mm": 75, "width_extra_mm": 100})
    p, h, e = ss["projection_mm"] / 1000, ss["height_mm"] / 1000, ss["width_extra_mm"] / 1000
    # context, not the window under test: a weathered stone cill, sloping to a nose and throated
    # underneath (Rivington Part I p.9: projecting at least 2 in, throated)
    parts.append({"name": "stone_sill", "material": "stone",
                  "profile": [[-p, -h], [-p + 0.020, -h], [-p + 0.020, -h + 0.010], [-p + 0.030, -h + 0.010],
                              [-p + 0.030, -h], [depth, -h], [depth, 0.0], [0.03, 0.0], [-p, -0.025]],
                  "axis": "x", "plane": ["y", "z"], "start": -W / 2 - e, "end": W / 2 + e})
    # context: a flat gauged brick arch over the opening, one standard 9 in brick deep (not sourced
    # for this window: the photographs show gauged and segmental heads), slightly lighter brick
    parts.append({"name": "gauged_arch", "material": "arch", "profile": [[-W / 2 - 0.05, 0], [W / 2 + 0.05, 0], [W / 2 + 0.05, 0.1143], [-W / 2 - 0.05, 0.1143]],
                  "axis": "z", "plane": ["x", "y"], "start": H, "end": H + 0.2286})
    return parts


def camera(name, loc, target, ortho=None, lens=50):
    cam = bpy.data.cameras.new(name)
    ob = bpy.data.objects.new(name, cam)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = loc
    d = [target[i] - loc[i] for i in range(3)]
    ob.rotation_euler = (math.atan2(math.hypot(d[0], d[1]), -d[2]), 0, math.atan2(d[1], d[0]) - math.pi / 2)
    if ortho:
        cam.type = "ORTHO"
        cam.ortho_scale = ortho
    else:
        cam.lens = lens
    return ob


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    spec = json.load(open(argv[0]))
    T = json.load(open(argv[1]))
    out = argv[2]
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    obs = blender_parts.build({"parts": spec["parts"] + wall(T)})
    for ob in obs:
        mname = ob.data.materials[0].name if ob.data.materials else "paint"
        ob.data.materials.clear()
        ob.data.materials.append(material(mname.split(".")[0]))
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light = "STUDIO"
    sh.color_type = "MATERIAL"
    sh.show_shadows = True
    sh.shadow_intensity = 0.6
    sh.show_cavity = True
    sh.cavity_type = "BOTH"
    sh.show_specular_highlight = True
    sc.display.shadow_focus = 0.2
    sc.display.light_direction = (0.45, -0.55, 0.70)
    sc.render.resolution_x, sc.render.resolution_y = 1600, 1600
    sc.render.film_transparent = False
    sc.world = bpy.data.worlds.new("w")
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    H = T["opening"]["height_mm"] / 1000
    shots = {
        "front": camera("front", (0, -6.0, H / 2), (0, 0, H / 2), lens=85),
        "oblique": camera("oblique", (-2.2, -3.4, H * 0.65), (0, 0.12, H * 0.55), lens=60),
        "meeting_rail": camera("meeting_rail", (-0.10, -0.55, H * 0.47), (0.36, 0.15, H * 0.50), lens=50),
        "street": camera("street", (1.2, -9.0, 1.6), (0, 0, H / 2), lens=70),
        "plan_section_low": camera("low", (0.0, -2.5, -0.6), (0, 0.1, 0.3), lens=60),
    }
    for nm, cam in shots.items():
        sc.camera = cam
        sc.render.filepath = os.path.join(out, nm + ".jpg")
        bpy.ops.render.render(write_still=True)
        print("RENDERED", sc.render.filepath)


if __name__ == "__main__":
    main()
