"""The sash window's own shade, baked: the piece for the game with ambient occlusion in its vertex colour.

Run inside Blender (headless):
    blender -b --factory-startup --python bake_ao.py -- parts.json target.json out.glb

WHY (8 October; production/research/aaa-street/WINDOWS-GRAZING-2026-10-08.md): from the street's low
angles a box sash shows mostly its own lining, track and beads, and in the photographs those step in
tone (lining 220-250, inside corner 105-125, track 150-180 in photograph 9); ours were one flat white,
so the sashes read as boards and slits. The window is built from its parts (blender_parts.py) inside
its brick reveal and stone sill (render_window.wall, the target's wall), Cycles bakes ambient occlusion
at every vertex of the window's own parts under a uniform white sky, and only the window is exported:
COLOR_0 R the occlusion (the street's export carries R as occlusion, tools/art-recipes/terrace-front.py
KIT_EXPOSURE), G 0, B 1, A 1. The glass is left without (the street leaves a house's glass out).
"""
import json
import os
import sys

import bpy

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import blender_parts  # noqa: E402

AO_DISTANCE_M = 0.06      # the box's own channels and corners (19-38 mm); the reveal's shade is Lumen's own
STEP_M = 0.08             # the longest edge left after cutting: enough for an embedded end's dark to stay at the end
SAMPLES = 128


def wall_parts(T):
    """The wall round the opening, from render_window.wall without importing its Workbench setup."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("render_window", os.path.join(HERE, "render_window.py"))
    rw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(rw)
    return rw.wall(T)


def main():
    argv = sys.argv[sys.argv.index("--") + 1:]
    spec = json.load(open(argv[0]))
    T = json.load(open(argv[1]))
    out = argv[2]
    bpy.ops.wm.read_factory_settings(use_empty=True)
    win = blender_parts.build(spec)
    # CUT INTO STEPS FIRST (the first bake, 10:55): a part is a prism with corners only at its two
    # ends, and a lining's or sill's ends sit inside the brick as a real one's do, so the shade baked
    # there (none: inside the wall) spread down the whole visible length. Every edge longer than
    # STEP_M is cut into STEP_M pieces; the shape does not change, only where shade can be kept.
    import bmesh
    for o in win:
        bm = bmesh.new()
        bm.from_mesh(o.data)
        for e in [e for e in bm.edges if e.calc_length() > STEP_M]:
            n = int(e.calc_length() / STEP_M)
            if n > 0 and e.is_valid:
                bmesh.ops.subdivide_edges(bm, edges=[e], cuts=n)
        bmesh.ops.triangulate(bm, faces=bm.faces[:])
        bm.to_mesh(o.data)
        bm.free()
        o.data.update()
    wall = blender_parts.build({"parts": wall_parts(T)})
    scene = bpy.context.scene
    scene.render.engine = "CYCLES"
    scene.cycles.device = "CPU"
    scene.cycles.samples = SAMPLES
    world = bpy.data.worlds.new("sky")
    scene.world = world
    world.use_nodes = True
    world.node_tree.nodes["Background"].inputs[0].default_value = (1.0, 1.0, 1.0, 1.0)
    world.light_settings.distance = AO_DISTANCE_M
    baked = 0
    for o in win:
        mat = o.data.materials[0].name if len(o.data.materials) else ""
        if mat == "glass":
            continue
        me = o.data
        ca = me.color_attributes.new("Col", "FLOAT_COLOR", "POINT")
        me.color_attributes.active_color = ca
        for other in bpy.context.view_layer.objects:
            other.select_set(False)
        o.select_set(True)
        bpy.context.view_layer.objects.active = o
        bpy.ops.object.bake(type="AO", target="VERTEX_COLORS")
        # the street's layout: R occlusion, G edges (none), B exposure (full), A 1
        for d in ca.data:
            ao = d.color[0]
            d.color = (ao, 0.0, 1.0, 1.0)
        baked += 1
    for o in wall:
        bpy.data.objects.remove(o, do_unlink=True)
    for o in win:
        mat = o.data.materials[0].name if len(o.data.materials) else "none"
        if mat == "paint":
            o.data.materials[0].name = mat = "paint_joinery"
        o.name = "%s__%s" % (mat, o.name)
    bpy.ops.export_scene.gltf(filepath=out, export_format="GLB", export_yup=True, export_normals=True,
                              export_texcoords=False, export_cameras=False, export_animations=False,
                              export_extras=False, export_vertex_color="ACTIVE")
    print("BAKED %d part(s) -> %s" % (baked, out))


if __name__ == "__main__":
    main()
