"""Review pictures of Quay Street's litter bins: a composition of the built models under the shared overcast sky, by tools/review_render.py (two views: street and close).

    /home/user/.bpyenv/bin/python render_bins.py [--out DIR] [--only street,close] [--samples 64] [--threads 2] [--version 1] [--date 2026-10-12]

The composition (made here from the .glb files, never committed, a judging aid only): along the street, left to right, K1 B (the open steel bin on its post, the sack in it), K2 c
(the hooded drum with its burnt hood, the aperture turned to the camera), D1 a (the dustbin, lid on), D1 b (lid off, leaning beside it) and K1 C (damaged, hung the other way).
street = all five from 6 m, eye height 1.6 m; close = K1 B's bin and clamps and K2 c's aperture and burn from 1.9 m. 1600 x 1200, Cycles on the CPU, at most --threads threads.
"""
import argparse
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bpy  # noqa: E402

import review_render as rr  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
ASSETS = os.path.join(REPO, "production", "assets", "cloud-week", "bins")
PREVIEW_DIR = os.path.join(REPO, "production", "previews", "cloud-week", "bins")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-bins/render"

# (file, x, y, yaw degrees about z)
SCENE = [("K1_pole_open_B", -1.0, 0.0, 0.0), ("K2_hooded_drum_c", 0.35, 0.0, -90.0), ("D1_dustbin_a", 1.3, 0.0, 0.0), ("D1_dustbin_b", 2.15, 0.0, 0.0), ("K1_pole_open_C", 3.6, 0.0, 180.0)]


def views():
    return [
        {"name": "street", "loc": [1.3, -6.0, 1.6], "target": [1.3, 0.0, 0.55], "lens": 32},
        {"name": "close", "loc": [-0.2, -1.9, 1.3], "target": [-0.15, 0.0, 0.8], "lens": 30},
    ]


def compose(path):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    for name, x, y, yaw in SCENE:
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=os.path.join(ASSETS, name + ".glb"))
        new = [o for o in bpy.data.objects if o not in before]
        for o in new:
            if o.parent is None:
                o.rotation_mode = "XYZ"
                o.rotation_euler = (0.0, 0.0, math.radians(yaw))
                o.location = (x, y, 0.0)
    bpy.ops.export_scene.gltf(filepath=path, export_format="GLB", export_apply=True, export_materials="EXPORT", export_cameras=False, export_lights=False, export_yup=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--only", default="street,close")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--date", default="2026-10-12")
    ap.add_argument("--previews", default=PREVIEW_DIR)
    ap.add_argument("--no-previews", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    scene = os.path.join(a.out, "review_scene.glb")
    compose(scene)
    vj = os.path.join(a.out, "views.json")
    json.dump(views(), open(vj, "w"), indent=1)
    orig_reset = rr.reset

    def reset():
        s = orig_reset()
        s.render.threads_mode = "FIXED"
        s.render.threads = a.threads
        return s

    rr.reset = reset
    sys.argv = ["review_render.py", scene, a.out, "--views", vj, "--context", "street", "--samples", str(a.samples), "--width", "1600", "--height", "1200", "--hdri", HDRI, "--only", a.only]
    rr.main()
    if a.no_previews:
        return
    from PIL import Image
    os.makedirs(a.previews, exist_ok=True)
    for n in a.only.split(","):
        src = os.path.join(a.out, n + ".png")
        if not os.path.exists(src):
            continue
        im = Image.open(src).convert("RGB")
        im.thumbnail((1600, 1600))
        dst = os.path.join(a.previews, "bins-%s-v%d-%s.jpg" % (n, a.version, a.date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        print("preview", dst, os.path.getsize(dst))


if __name__ == "__main__":
    main()
