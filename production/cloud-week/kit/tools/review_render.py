"""Review pictures of a kit piece, rendered headless with Cycles on the CPU (no graphics card).

    python review_render.py piece.glb outdir [--views views.json] [--context street|wall|none]
        [--samples 64] [--width 1600] [--height 1200] [--hdri overcast.hdr]

Run with a Python that has the bpy package (Blender 5.2.2 as a module: pip install bpy==5.2.2), or
inside Blender:  blender -b --factory-startup --python review_render.py -- piece.glb outdir ...

WHY ONE HARNESS. Every piece of cloud week 42 is judged by a fresh reviewer against photographs,
one view per reviewer. The views must be the same kind of picture for every piece: a grey overcast
light (the street's weather, never sunshine), a pavement under the piece, the camera at a person's
eye height (1.6 m) as the game's third-person camera sees a street, plus a square-on elevation
and a close view for detail. A picture made here is a judging aid only: the look is developed in
Unreal against the Hook sheet (ruling of 23 September), never here.

THE VIEWS (metres, the piece's base centre at the origin, +y away from the street, z up), unless
--views gives others as [{"name", "loc": [x,y,z], "target": [x,y,z], "lens": mm} or
{"name", "ortho": width_m, "loc", "target"}]:
  front   square-on elevation, orthographic, fitted to the piece
  street  three-quarter from the pavement edge, eye height 1.6 m, about 4 m off
  low     a low glancing view along the street, 1.6 m high, about 8 m off at 20 degrees
  close   the piece's upper half from 1.2 m, for profiles, fixings and edges

The light: an overcast sky, from --hdri or the environment's LEDGER_REVIEW_HDRI if given (the
intended one is Poly Haven's CC0 "Bethnal Green Entrance" by Andreas Mischok, overcast, low
contrast, 2k: https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/2k/bethnal_green_entrance_2k.hdr), else a uniform grey-blue sky of 1.0 strength plus a soft key from above at 0.6;
filmic-free standard view transform, so values read as they are.
"""
import argparse
import json
import math
import os
import sys

import bpy
from mathutils import Vector


def args():
    argv = sys.argv
    argv = argv[argv.index("--") + 1:] if "--" in argv else argv[1:]
    p = argparse.ArgumentParser()
    p.add_argument("model")
    p.add_argument("outdir")
    p.add_argument("--views")
    p.add_argument("--context", default="street", choices=["street", "wall", "none"])
    p.add_argument("--samples", type=int, default=64)
    p.add_argument("--width", type=int, default=1600)
    p.add_argument("--height", type=int, default=1200)
    p.add_argument("--hdri", default=os.environ.get("LEDGER_REVIEW_HDRI"))
    p.add_argument("--only", help="comma-separated view names")
    return p.parse_args(argv)


def reset():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    s = bpy.context.scene
    s.render.engine = "CYCLES"
    s.cycles.device = "CPU"
    s.cycles.use_denoising = True
    s.view_settings.view_transform = "Standard"
    s.view_settings.look = "None"
    return s


def load(path):
    before = set(bpy.data.objects)
    if path.lower().endswith((".glb", ".gltf")):
        bpy.ops.import_scene.gltf(filepath=path)
    elif path.lower().endswith(".blend"):
        with bpy.data.libraries.load(path) as (src, dst):
            dst.objects = list(src.objects)
        for o in dst.objects:
            bpy.context.scene.collection.objects.link(o)
    else:
        raise SystemExit("unknown model kind: " + path)
    obs = [o for o in bpy.data.objects if o not in before and o.type == "MESH"]
    lo = Vector((1e9, 1e9, 1e9))
    hi = Vector((-1e9, -1e9, -1e9))
    for o in obs:
        for c in o.bound_box:
            w = o.matrix_world @ Vector(c)
            lo = Vector(map(min, lo, w))
            hi = Vector(map(max, hi, w))
    return obs, lo, hi


def material(name, rgb, rough=0.8):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*rgb, 1)
    b.inputs["Roughness"].default_value = rough
    return m


def plane(name, size, loc, rot, mat):
    bpy.ops.mesh.primitive_plane_add(size=1, location=loc, rotation=rot)
    o = bpy.context.object
    o.name = name
    o.scale = (size[0], size[1], 1)
    o.data.materials.append(mat)
    return o


def context(kind, lo, hi):
    """A grey wet-ish pavement under the piece; for 'wall', a plain brick-coloured wall behind it."""
    if kind == "none":
        return
    paving = material("ctx_paving", (0.09, 0.09, 0.088), 0.7)   # dark damp slabs
    plane("ctx_pavement", (400, 400), (0, 0, min(lo.z, 0) - 0.0005), (0, 0, 0), paving)
    if kind == "wall":
        brick = material("ctx_wall", (0.30, 0.15, 0.10), 0.85)
        plane("ctx_wall", (40, 12), (0, hi.y + 0.002, 6), (math.radians(90), 0, 0), brick)


def light(hdri):
    w = bpy.data.worlds.new("sky")
    bpy.context.scene.world = w
    w.use_nodes = True
    nt = w.node_tree
    bg = nt.nodes["Background"]
    if hdri and os.path.exists(hdri):
        env = nt.nodes.new("ShaderNodeTexEnvironment")
        env.image = bpy.data.images.load(hdri)
        nt.links.new(env.outputs["Color"], bg.inputs["Color"])
        bg.inputs["Strength"].default_value = 1.0
        # the camera sees a plain grey sky, never the photograph's modern street; it only lights
        path = nt.nodes.new("ShaderNodeLightPath")
        flat = nt.nodes.new("ShaderNodeBackground")
        flat.inputs["Color"].default_value = (0.55, 0.57, 0.60, 1)
        mix = nt.nodes.new("ShaderNodeMixShader")
        out = nt.nodes["World Output"]
        nt.links.new(path.outputs["Is Camera Ray"], mix.inputs["Fac"])
        nt.links.new(bg.outputs["Background"], mix.inputs[1])
        nt.links.new(flat.outputs["Background"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    else:
        bg.inputs["Color"].default_value = (0.62, 0.66, 0.72, 1)
        bg.inputs["Strength"].default_value = 1.0
        sun = bpy.data.lights.new("soft_key", "SUN")
        sun.energy = 0.6
        sun.angle = math.radians(40)          # a broad, soft overcast key, never a hard sun
        o = bpy.data.objects.new("soft_key", sun)
        o.rotation_euler = (math.radians(35), 0, math.radians(30))
        bpy.context.scene.collection.objects.link(o)


def default_views(lo, hi):
    cx, cz = (lo.x + hi.x) / 2, (lo.z + hi.z) / 2
    size = max(hi.x - lo.x, hi.z - lo.z)
    fit = max(hi.x - lo.x, (hi.z - lo.z) * 4.0 / 3.0) * 1.15   # ortho_scale spans the frame's width (4:3)
    tgt = (cx, (lo.y + hi.y) / 2, cz)
    return [
        {"name": "front", "ortho": fit, "loc": (cx, lo.y - 10, cz), "target": (cx, lo.y, cz)},
        {"name": "street", "loc": (cx - 2.4, lo.y - 3.2, 1.6), "target": tgt, "lens": 35},
        {"name": "low", "loc": (cx - 7.5, lo.y - 2.7, 1.6), "target": tgt, "lens": 50},
        {"name": "close", "loc": (cx - 0.5, lo.y - 1.2, max(cz + size * 0.15, 1.0)),
         "target": (cx, lo.y, cz + (hi.z - lo.z) * 0.25), "lens": 50},
    ]


def camera(v):
    cam = bpy.data.cameras.new(v["name"])
    ob = bpy.data.objects.new("cam_" + v["name"], cam)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = v["loc"]
    d = Vector(v["target"]) - Vector(v["loc"])
    ob.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    if "ortho" in v:
        cam.type = "ORTHO"
        cam.ortho_scale = v["ortho"]
    else:
        cam.lens = v.get("lens", 35)
    cam.clip_end = 500
    return ob


def main():
    a = args()
    s = reset()
    obs, lo, hi = load(a.model)
    context(a.context, lo, hi)
    light(a.hdri)
    s.cycles.samples = a.samples
    s.render.resolution_x, s.render.resolution_y = a.width, a.height
    views = json.load(open(a.views)) if a.views else default_views(lo, hi)
    only = set(a.only.split(",")) if a.only else None
    os.makedirs(a.outdir, exist_ok=True)
    made = []
    for v in views:
        if only and v["name"] not in only:
            continue
        s.camera = camera(v)
        s.render.filepath = os.path.join(a.outdir, v["name"] + ".png")
        bpy.ops.render.render(write_still=True)
        made.append(s.render.filepath)
    print(json.dumps({"model": a.model, "bounds_m": [list(lo), list(hi)], "views": made}))


if __name__ == "__main__":
    main()
