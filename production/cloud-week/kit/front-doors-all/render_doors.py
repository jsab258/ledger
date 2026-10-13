"""The review pictures of the front doors: a kind's .glb with its house's fittings placed by data, in front of the 3.1 door's review wall, lit by the shared overcast sky.

    nice -n 15 /home/user/.bpyenv/bin/python render_doors.py --house east_parade_bay0 [--views street,close] [--samples 64] [--out DIR] [--previews DIR] [--date 2026-10-13]
    nice -n 15 /home/user/.bpyenv/bin/python render_doors.py --kind F1 --views front --samples 16 --width 800 --height 600     (an aid: the kind in its first house)

Steps, for one house (or one of the hill's doors):
  1. a scene: door_<K>.glb as built (the kind's paint is replaced by the house's paint and roughness by its condition, the frame by the house's frame colour),
     each fitting's .glb placed at the house's mount point (houses.json; mirror_x scales x by -1), and the context wall of the 3.1 review (door_context.py: brick,
     quoins, arch and plinth for the T kinds, the painted pilaster for the F kinds; never in a .glb) with its dark closing face and dark hall behind the glass;
  2. the shared harness tools/review_render.py with the gate's cameras of that kind (target.json gate.views: front, street, close, low, front_head, front_foot,
     close_plate, close_foot), 1600 x 1200, 64 samples, Cycles on the CPU, LEDGER_REVIEW_HDRI=/home/user/cache/hdri/bethnal_green_entrance_2k.hdr;
  3. reduced previews (JPEG, at most 1600 px, under 500 KB) as <kind>-<view>-v<version>-<date>.jpg (the kind's first house) or <kind>-<view>-<house>-v<version>-<date>.jpg
     (--version 2 for the pictures of try 2; the v1 pictures stay as the record).
A render aid in the scene, never in a file: the glass lets shadow rays through, so a pale net card behind a pane is lit by the sky as it would be through a real pane
(Cycles otherwise treats the glass as opaque to light and the net reads black). The look itself is the engine's.
"""
import argparse
import json
import math
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "..", "door"))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bpy  # noqa: E402
from mathutils import Vector  # noqa: E402

import build_door as bd  # noqa: E402
import render_door as rd  # noqa: E402
import doors_kinds as K  # noqa: E402

ASSET_DIR = os.path.join(bd.REPO, "production", "assets", "cloud-week", "front-doors-all")
PREVIEW_DIR = os.path.join(bd.REPO, "production", "previews", "cloud-week", "front-doors-all")
SCRATCH = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/unit9/render"
REVIEW_RENDER = os.path.join(HERE, "..", "tools", "review_render.py")
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
FRAME_MATS = ("paint_white", "paint_white_grimy")


def set_paint(mat, srgb, rough):
    b = mat.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (bd.lin(srgb[0]), bd.lin(srgb[1]), bd.lin(srgb[2]), 1.0)
    b.inputs["Roughness"].default_value = rough


def glass_passes_shadow_rays():
    """The render aid: every transmissive material mixes in a Transparent BSDF for shadow rays (see the module note)."""
    for m in bpy.data.materials:
        if not m.use_nodes or "Principled BSDF" not in m.node_tree.nodes:
            continue
        b = m.node_tree.nodes["Principled BSDF"]
        if b.inputs["Transmission Weight"].default_value < 0.5:
            continue
        nt = m.node_tree
        out = [n for n in nt.nodes if n.type == "OUTPUT_MATERIAL"][0]
        lp = nt.nodes.new("ShaderNodeLightPath")
        tr = nt.nodes.new("ShaderNodeBsdfTransparent")
        mix = nt.nodes.new("ShaderNodeMixShader")
        nt.links.new(lp.outputs["Is Shadow Ray"], mix.inputs["Fac"])
        nt.links.new(b.outputs["BSDF"], mix.inputs[1])
        nt.links.new(tr.outputs["BSDF"], mix.inputs[2])
        nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])


def net_look():
    """A second render aid, only in the scene (never in a file): the T2 net cards (material net_voile, a plain white card in the file) get the look of a gathered net: vertical folds, three
    gathers of 48, 37.7 and 83 mm (the windows target's NET_COMMON: wavelength 40 to 55 mm, brightness modulation 0.22), so that they read as nets behind glass and not as white boards. The first
    build's nets were a flat grey card that read as slate (the street review's point 1). The PC builds the real folded translucent net from net_voile."""
    import math as _m
    for m in bpy.data.materials:
        if not m.name.startswith("net_voile") or not m.use_nodes:
            continue
        nt = m.node_tree
        b = nt.nodes["Principled BSDF"]
        base = tuple(b.inputs["Base Color"].default_value)
        tc = nt.nodes.new("ShaderNodeTexCoord")
        sep = nt.nodes.new("ShaderNodeSeparateXYZ")
        nt.links.new(tc.outputs["Object"], sep.inputs["Vector"])
        def math(op, a_=None, b_=None):
            n = nt.nodes.new("ShaderNodeMath")
            n.operation = op
            for i_, v_ in enumerate((a_, b_)):
                if v_ is None:
                    continue
                if isinstance(v_, (int, float)):
                    n.inputs[i_].default_value = v_
                else:
                    nt.links.new(v_, n.inputs[i_])
            return n.outputs[0]
        x = sep.outputs["X"]
        total = None
        for wl, ph, amp in ((0.048, 0.0, 0.07), (0.0377, 1.3, 0.05), (0.083, 2.4, 0.04)):      # three gathers: 48, 37.7 and 83 mm, so the folds are not a regular corrugation
            w = math("MULTIPLY", math("SINE", math("ADD", math("MULTIPLY", x, 2.0 * _m.pi / wl), ph)), amp)
            total = w if total is None else math("ADD", total, w)
        mad = math("ADD", total, 0.78)                         # the net's mean brightness against a white card: a voile passes light and shows the dark hall a little
        cc = nt.nodes.new("ShaderNodeCombineColor")
        for i in range(3):
            nt.links.new(mad, cc.inputs[i])
        mix = nt.nodes.new("ShaderNodeMix")
        mix.data_type = "RGBA"
        mix.blend_type = "MULTIPLY"
        mix.inputs[0].default_value = 1.0
        mix.inputs[6].default_value = base
        nt.links.new(cc.outputs[0], mix.inputs[7])
        nt.links.new(mix.outputs[2], b.inputs["Base Color"])


def place_furniture(H, fur, ASSET):
    """Import one fitting's .glb and put it at its mount point (metres, the kind's own frame)."""
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=os.path.join(ASSET, "furniture", fur["glb"] + ".glb"))
    new = [o for o in bpy.data.objects if o not in before]
    root = bpy.data.objects.new("fit_" + fur["slot"], None)
    bpy.context.scene.collection.objects.link(root)
    root.location = Vector(fur["mount_m"])
    if fur.get("mirror_x"):
        root.scale = (-1.0, 1.0, 1.0)
    for o in new:
        if o.parent is None:
            o.parent = root
    return root


def build_house_scene(T31, N, H, rec, blend_path, asset=ASSET_DIR, kind_glb=None):
    kind = rec["kind"]
    variant = "T1" if kind.startswith("T") else "F1"
    glb = kind_glb or os.path.join(asset, rec["door_glb"])
    rd.build_scene(T31, variant, glb, blend_path)
    P = {p["id"]: p for p in N["paints"]}
    cond = rec.get("condition", "kept")
    rough = N["conditions"][cond]["roughness"]
    fr = {f["id"]: f for f in N["frame_colours"]}
    for m in bpy.data.materials:
        if m.name.startswith("paint_") and m.use_nodes:
            base = m.name.split(".")[0]
            if base in FRAME_MATS:
                set_paint(m, fr[rec.get("frame_colour", "white")]["srgb"], 0.35)
            else:
                set_paint(m, rec["paint_srgb"], rough)
    for fur in rec.get("furniture", []):
        place_furniture(H, fur, asset)
    glass_passes_shadow_rays()
    net_look()
    bpy.ops.wm.save_as_mainfile(filepath=blend_path, compress=True)


def previews(out_dir, house_dir, kind, names, house, first, date, version, preview_dir):
    from PIL import Image
    os.makedirs(preview_dir, exist_ok=True)
    res = []
    for n in names:
        src = os.path.join(house_dir, n + ".png")
        if not os.path.exists(src):
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((1600, 1600))
        tag = "%s-%s" % (kind, n) if first else "%s-%s-%s" % (kind, n, house)
        dst = os.path.join(preview_dir, "%s-v%d-%s.jpg" % (tag, version, date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        res.append((dst, os.path.getsize(dst)))
    return res


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--house")
    ap.add_argument("--kind")
    ap.add_argument("--views", default="street,close")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=1200)
    ap.add_argument("--out", default=SCRATCH)
    ap.add_argument("--asset-dir", default=ASSET_DIR)
    ap.add_argument("--previews")
    ap.add_argument("--date", default="2026-10-13")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--scene-only", action="store_true")
    ap.add_argument("--camera", action="append", help="an extra aid view NAME=x,y,z;tx,ty,tz;lens (metres, the kind's frame), rendered as NAME (may be given several times)")
    a = ap.parse_args()
    T31 = bd.load_target()
    N = K.load_new_target()
    H = json.load(open(os.path.join(a.asset_dir, "houses.json")))
    if a.house:
        recs = [h for h in H["houses"] + H["hill"] if h.get("house", h.get("id")) == a.house]
    else:
        recs = [h for h in H["houses"] if h["kind"] == a.kind][:1]
    if not recs:
        raise SystemExit("no such house or kind")
    rec = recs[0]
    house = rec.get("house", rec.get("id"))
    kind = rec["kind"]
    first = [h["house"] for h in H["houses"] if h["kind"] == kind][0] == house
    hdir = os.path.join(a.out, house)
    os.makedirs(hdir, exist_ok=True)
    blend = os.path.join(hdir, "scene.blend")
    build_house_scene(T31, N, H, rec, blend, a.asset_dir)
    if a.scene_only:
        return
    views = {v["name"]: v for v in N["gate"]["views"][kind]}
    names = a.views.split(",") if a.views else []
    for cam_ in (a.camera or []):
        nm, rest = cam_.split("=")
        loc, tgt, lens = rest.split(";")
        views[nm] = {"name": nm, "loc": [float(x) for x in loc.split(",")], "target": [float(x) for x in tgt.split(",")], "lens": float(lens)}
        names.append(nm)
    vj = os.path.join(hdir, "views.json")
    json.dump([views[n] for n in names], open(vj, "w"), indent=1)
    cmd = [sys.executable, REVIEW_RENDER, blend, hdir, "--views", vj, "--context", "street", "--samples", str(a.samples), "--width", str(a.width), "--height", str(a.height), "--hdri", HDRI]
    t0 = time.time()
    subprocess.run(cmd, check=True, env=dict(os.environ, LEDGER_REVIEW_HDRI=HDRI), stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print("%s %s rendered in %.0f s" % (house, a.views, time.time() - t0), flush=True)
    if a.previews:
        for dst, size in previews(a.out, hdir, kind, names, house, first, a.date, a.version, a.previews):
            print("preview", dst, size)


if __name__ == "__main__":
    main()
