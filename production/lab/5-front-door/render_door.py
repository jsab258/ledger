"""Workbench pictures of the built door in its brick opening, for the fresh reviewer; and the .glb.

    blender -b --factory-startup --python render_door.py -- parts.json target.json outdir [door.glb]

Workbench only (the light render mode). The wall is plain brick with the opening, the 4 1/2 in
reveal, the frame's recess behind it and a flat brick arch over the head (target.json); the stone
sill is the target's. The leaf, its panels and mouldings are painted red, the frame white, as
the photograph the target follows (Teignmouth, Geograph 3157125). The .glb holds the door and its
frame only, no wall.
"""
import json
import math
import os
import sys

import bpy

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "tools"))
import blender_parts  # noqa: E402

COL = {"iron": (0.62, 0.48, 0.20, 1), "leaf": (0.55, 0.05, 0.04, 1), "panel": (0.55, 0.05, 0.04, 1), "moulding": (0.55, 0.05, 0.04, 1),
       "frame": (0.92, 0.91, 0.88, 1), "glass": (0.16, 0.19, 0.21, 1), "stone": (0.62, 0.60, 0.55, 1),
       "brick": (0.45, 0.22, 0.14, 1), "arch": (0.72, 0.62, 0.45, 1)}


def material(name):
    m = bpy.data.materials.get("m_" + name) or bpy.data.materials.new("m_" + name)
    m.diffuse_color = COL.get(name, (0.8, 0.8, 0.8, 1))
    m.roughness = 0.05 if name == "glass" else 0.45
    m.metallic = 0.3 if name == "glass" else 0.0
    return m


def wall(T):
    o, fr = T["opening"], T["frame"]
    W, H = o["brick_width_mm"] / 1000, o["brick_height_mm"] / 1000
    rv, wt = o["reveal_depth_mm"] / 1000, o["wall_thickness_mm"] / 1000
    jx0, jx1 = fr["jamb_x_mm"]["left"][0] / 1000, fr["jamb_x_mm"]["right"][1] / 1000
    head_top = (fr["head_section_mm"]["z0"] + fr["head_section_mm"]["height"]) / 1000
    span, top, low = 1.6, H + 0.9, -0.076
    P = []
    def slab(nm, x0, x1, y0, y1, z0, z1, mat="brick"):
        P.append({"name": "ctx_" + nm, "material": mat, "profile": [[x0, y0], [x1, y0], [x1, y1], [x0, y1]],
                  "axis": "z", "plane": ["x", "y"], "start": z0, "end": z1})
    slab("left", -span, 0.0, 0.0, wt, low, top)
    slab("right", W, W + span, 0.0, wt, low, top)
    slab("left_back", 0.0, jx0 if jx0 > 0 else 0.0001, rv, wt, low, top)       # nothing: the frame's recess starts at the reveal
    slab("over", 0.0, W, 0.0, rv, H + 0.2286, top)
    slab("arch", -0.115, W + 0.115, 0.0, rv, H, H + 0.2286, "arch")   # the arch runs into the brick each side
    slab("over_back", jx0, jx1, rv, wt, head_top, top)
    slab("below", -span, W + span, 0.0, wt, -0.6, low)
    return [p for p in P if p["name"] != "ctx_left_back"]


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
    T = json.load(open(argv[1], encoding="utf-8"))
    out = argv[2]
    glb = argv[3] if len(argv) > 3 else None
    os.makedirs(out, exist_ok=True)
    bpy.ops.wm.read_factory_settings(use_empty=True)
    door = blender_parts.build(spec)
    ctx = blender_parts.build({"parts": wall(T)})
    for ob in door + ctx:
        mname = ob.data.materials[0].name.split(".")[0] if ob.data.materials else "brick"
        ob.data.materials.clear()
        ob.data.materials.append(material(mname))
        # curved mouldings shaded smooth, their arrises kept sharp (by angle)
        ob.data.shade_smooth()
        ob.data.set_sharp_from_angle(angle=math.radians(40))
    if glb:
        bpy.ops.object.select_all(action="DESELECT")
        for ob in door:
            if not ob.name.startswith("stone"):
                ob.select_set(True)
        bpy.ops.export_scene.gltf(filepath=glb, export_format="GLB", use_selection=True, export_apply=True)
        print("GLB", glb, os.path.getsize(glb))
    sc = bpy.context.scene
    sc.render.engine = "BLENDER_WORKBENCH"
    sh = sc.display.shading
    sh.light, sh.color_type = "STUDIO", "MATERIAL"
    sh.show_shadows, sh.shadow_intensity = True, 0.6
    sh.show_cavity, sh.cavity_type = True, "BOTH"
    sh.show_specular_highlight = True
    sc.display.shadow_focus = 0.2
    sc.display.light_direction = (0.45, -0.55, 0.70)
    sc.render.resolution_x, sc.render.resolution_y = 1400, 1800
    sc.world = bpy.data.worlds.new("w")
    sc.render.image_settings.file_format = "JPEG"
    sc.render.image_settings.quality = 90
    W = T["opening"]["brick_width_mm"] / 1000
    H = T["opening"]["brick_height_mm"] / 1000
    cx = W / 2
    shots = {
        "front": camera("front", (cx, -7.0, H / 2), (cx, 0, H / 2), lens=85),
        "oblique": camera("oblique", (cx - 2.0, -3.6, 1.5), (cx, 0.15, H * 0.5), lens=55),
        "panel_close": camera("panel_close", (cx - 0.45, -0.9, 0.55), (cx - 0.15, 0.2, 0.45), lens=50),
        "lock_rail_close": camera("lock_rail_close", (cx + 0.5, -1.1, 1.05), (cx + 0.1, 0.2, 0.83), lens=50),
        "street": camera("street", (cx + 1.5, -9.0, 1.6), (cx, 0, H / 2), lens=70),
    }
    for nm, cam in shots.items():
        sc.camera = cam
        sc.render.filepath = os.path.join(out, nm + ".jpg")
        bpy.ops.render.render(write_still=True)
        print("RENDERED", sc.render.filepath)


if __name__ == "__main__":
    main()
