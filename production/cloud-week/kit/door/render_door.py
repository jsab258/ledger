"""The door's review pictures: the .glb in front of its context wall, lit by the shared overcast sky, by review_render.py.

    /home/user/.bpyenv/bin/python render_door.py [--variant T1|F1|both] [--out DIR] [--samples 64] [--only front,street]
                                                 [--glb-dir DIR] [--previews DIR] [--version 1] [--date 2026-10-08]

Steps, per variant:
  1. a review scene: the door's .glb as built (production/assets/cloud-week/door/door_<V>.glb) plus the context wall from
     door_context.py (never in the .glb), the wall's brick, buff quoins, arch and plinth given procedural brick shaders
     (courses 77, joints 10 struck 2 back), saved as <DIR>/scene_<V>.blend;
  2. tools/review_render.py on that scene with views_<V>.json (front: orthographic elevation; street: three-quarter from the
     pavement edge at 1.6 m, about 4 m off; close: the lock rail and the ironmongery from about 1.2 m; low: along the street
     at 1.6 m, about 8 m off, about 20 degrees to the wall), 1600 x 1200, at least 64 samples, the overcast HDRI
     LEDGER_REVIEW_HDRI=/home/user/cache/hdri/bethnal_green_entrance_2k.hdr (the camera sees a plain grey sky; the sky only lights);
     review_render's own `--context street` gives the pavement; the wall is this script's, not its plain wall plane;
  3. reduced previews (JPEG, at most 1600 px, under 500 KB) to production/previews/cloud-week/door/door-<V>-<view>-v<N>-<date>.jpg.
"""
import argparse
import json
import math
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bpy  # noqa: E402

import build_door as bd  # noqa: E402
import door_context as dc  # noqa: E402

REVIEW_RENDER = os.path.join(HERE, "..", "tools", "review_render.py")
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
PREVIEW_DIR = os.path.join(bd.REPO, "production", "previews", "cloud-week", "door")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/door-build/v1"

# kinds -> (colour sRGB 0-255 as the target gives, roughness)
BRICK = {
    "red": dict(c1=(159, 113, 85), c2=(143, 98, 73), mortar=(190, 182, 168), width=0.225, rough=0.9),
    "plinth": dict(c1=(128, 90, 68), c2=(112, 76, 57), mortar=(150, 142, 130), width=0.225, rough=0.9),   # the damp, darker base (115, 76, 57 in the splay's shade)
    "quoin": dict(c1=(200, 186, 158), c2=(188, 174, 146), mortar=(190, 182, 168), width=0.225, rough=0.9),
}
PLAIN = {
    "arch": ((219, 209, 190), 0.9),
    "mortar": ((96, 84, 72), 0.95),          # the arch's dark, sooty, recessed joints
    "render": ((222, 225, 229), 0.9),        # the shop pilaster's painted render
    "paving": ((84, 84, 83), 0.7),           # F1's paving slab, as review_render's own dark damp slabs
    "dark": ((26, 24, 22), 0.97),            # the closing face behind the leaf's gaps and the dark hall behind the fanlight: matt, dark, never lit from within
}


def srgb_to_lin(c):
    return tuple(bd.lin(v) for v in c)


def brick_material(name, spec, z_shift, with_splay=False):
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Roughness"].default_value = spec["rough"]
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sep = nt.nodes.new("ShaderNodeSeparateXYZ")
    sub = nt.nodes.new("ShaderNodeMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = z_shift
    comb = nt.nodes.new("ShaderNodeCombineXYZ")
    nt.links.new(tc.outputs["Object"], sep.inputs[0])
    nt.links.new(sep.outputs["Z"], sub.inputs[0])
    nt.links.new(sep.outputs["X"], comb.inputs["X"])
    nt.links.new(sub.outputs[0], comb.inputs["Y"])

    def brick(width):
        b = nt.nodes.new("ShaderNodeTexBrick")
        b.offset = 0.5
        b.offset_frequency = 2
        b.squash = 1.0
        b.inputs["Color1"].default_value = (*srgb_to_lin(spec["c1"]), 1)
        b.inputs["Color2"].default_value = (*srgb_to_lin(spec["c2"]), 1)
        b.inputs["Mortar"].default_value = (*srgb_to_lin(spec["mortar"]), 1)
        b.inputs["Scale"].default_value = 1.0
        b.inputs["Mortar Size"].default_value = 0.005       # each side of a cell edge: 10 mm joints
        b.inputs["Mortar Smooth"].default_value = 0.12
        b.inputs["Bias"].default_value = 0.0
        b.inputs["Brick Width"].default_value = width
        b.inputs["Row Height"].default_value = 0.077
        nt.links.new(comb.outputs[0], b.inputs["Vector"])
        return b
    b1 = brick(spec["width"])
    colour, height = b1.outputs["Color"], b1.outputs["Fac"]
    if with_splay:
        # the splayed course is a single course of headers: 65 wide at a 75 pitch; chosen by the face's slope
        b2 = brick(0.075)
        b2.offset = 0.0
        geo = nt.nodes.new("ShaderNodeNewGeometry")
        sepn = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(geo.outputs["Normal"], sepn.inputs[0])
        gt = nt.nodes.new("ShaderNodeMath")
        gt.operation = "GREATER_THAN"
        gt.inputs[1].default_value = 0.3
        nt.links.new(sepn.outputs["Z"], gt.inputs[0])
        mixc = nt.nodes.new("ShaderNodeMix")
        mixc.data_type = "RGBA"
        nt.links.new(gt.outputs[0], mixc.inputs["Factor"])
        nt.links.new(b1.outputs["Color"], mixc.inputs["A"])
        nt.links.new(b2.outputs["Color"], mixc.inputs["B"])
        mixh = nt.nodes.new("ShaderNodeMix")
        mixh.data_type = "FLOAT"
        nt.links.new(gt.outputs[0], mixh.inputs["Factor"])
        nt.links.new(b1.outputs["Fac"], mixh.inputs["A"])
        nt.links.new(b2.outputs["Fac"], mixh.inputs["B"])
        colour, height = mixc.outputs["Result"], mixh.outputs["Result"]
    bump = nt.nodes.new("ShaderNodeBump")
    bump.inputs["Strength"].default_value = 0.8
    bump.inputs["Distance"].default_value = 0.002
    nt.links.new(height, bump.inputs["Height"])
    nt.links.new(colour, bsdf.inputs["Base Color"])
    nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def plain_material(name, srgb, rough):
    return bd.make_material(name, srgb, rough)


def build_scene(T, variant, glb, blend_path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    bpy.ops.import_scene.gltf(filepath=glb)
    pivot = T["glb_pivot"]["terrace_four_panel" if variant == "T1" else "flat_door_over_shop"]
    parts = dc.build(T, variant)
    obs = dc.make_objects(parts, variant, pivot)
    z_shift = 0.022 if variant == "T1" else 0.0           # the course lines of the target's wall: z 12 + 77 k above the threshold
    mats = {k: brick_material("ctx_" + k, v, z_shift, with_splay=(k == "plinth")) for k, v in BRICK.items()}
    for k, (c, r) in PLAIN.items():
        mats[k] = plain_material("ctx_" + k, c, r)
    for ob in obs:
        ob.data.materials.append(mats[ob["kind"]])
        ob.data.shade_flat()
    bpy.ops.wm.save_as_mainfile(filepath=blend_path, compress=True)
    return obs


def views(variant):
    """Views in the piece's frame: metres, the base centre at the origin, +y away from the street, z up."""
    t1 = variant == "T1"
    top = 2.9 if t1 else 2.6
    cz = 1.45 if t1 else 1.3
    v = [
        {"name": "front", "ortho": 4.0 if t1 else 3.6, "loc": [0.0, -10.0, cz], "target": [0.0, 0.0, cz]},
        {"name": "street", "loc": [-2.0, -3.5, 1.6], "target": [0.0, 0.0, 1.35 if t1 else 1.25], "lens": 32},
        {"name": "close", "loc": [0.33, -1.2, 1.45 if t1 else 1.0], "target": [0.25, 0.19, 1.40 if t1 else 1.0], "lens": 50},
        {"name": "low", "loc": [-7.0, -2.7, 1.6], "target": [0.0, 0.0, 1.2], "lens": 50},
        # extras for the reviewer, not asked for: the head and the foot square-on, and the letter plate close
        {"name": "front_head", "ortho": 1.9, "loc": [0.0, -10.0, 2.25 if t1 else 2.1], "target": [0.0, 0.0, 2.25 if t1 else 2.1]},
        {"name": "front_foot", "ortho": 1.9, "loc": [0.0, -10.0, 0.5], "target": [0.0, 0.0, 0.5]},
        {"name": "close_plate", "loc": [0.1, -1.0, 1.95 if t1 else 1.7], "target": [0.0, 0.19, 1.95 if t1 else 1.7], "lens": 50},
    ]
    return v


def previews(out_dir, variant, names, version, date, preview_dir):
    from PIL import Image
    os.makedirs(preview_dir, exist_ok=True)
    res = []
    for n in names:
        src = os.path.join(out_dir, variant, n + ".png")
        if not os.path.exists(src):
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((1600, 1600))
        dst = os.path.join(preview_dir, "door-%s-%s-v%d-%s.jpg" % (variant, n, version, date))
        for q in (90, 85, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        res.append((dst, os.path.getsize(dst)))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", default="both", choices=["T1", "F1", "both"])
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--glb-dir", default=bd.ASSET_DIR)
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--only")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--date", default="2026-10-08")
    ap.add_argument("--previews", default=PREVIEW_DIR)
    ap.add_argument("--scene-only", action="store_true")
    a = ap.parse_args()
    T = bd.load_target()
    for variant in (["T1", "F1"] if a.variant == "both" else [a.variant]):
        vdir = os.path.join(a.out, variant)
        os.makedirs(vdir, exist_ok=True)
        blend = os.path.join(a.out, "scene_%s.blend" % variant)
        glb = os.path.join(a.glb_dir, "door_%s.glb" % variant)
        build_scene(T, variant, glb, blend)
        vj = os.path.join(HERE, "views_%s.json" % variant)
        json.dump(views(variant), open(vj, "w"), indent=1)
        if a.scene_only:
            continue
        cmd = [sys.executable, REVIEW_RENDER, blend, vdir, "--views", vj, "--context", "street", "--samples", str(a.samples),
               "--width", "1600", "--height", "1200", "--hdri", HDRI]
        if a.only:
            cmd += ["--only", a.only]
        env = dict(os.environ, LEDGER_REVIEW_HDRI=HDRI)
        print(" ".join(cmd))
        subprocess.run(cmd, check=True, env=env)
        names = (a.only.split(",") if a.only else [v["name"] for v in views(variant)])
        for dst, size in previews(a.out, variant, names, a.version, a.date, a.previews):
            print("preview", dst, size)


if __name__ == "__main__":
    main()
