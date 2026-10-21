"""Review pictures of Rita's assembled front: shopfront_ritas.glb under the shared overcast sky, by tools/review_render.py.

    /home/user/.bpyenv/bin/python render_shopfront.py [--out DIR] [--only street,close] [--samples 64] [--threads 2]
                                                      [--glb PATH] [--previews DIR] [--version 1] [--date 2026-10-11]

The two views for review (Jafar, 11 October): street = the whole front from the opposite footway (9 m out, eye height 1.6 m, a little
toward the window end so the mouldings show their depth); close = the left pilaster's capital, the console and the end of the fascia from
1.7 m. `front` (an orthographic elevation) is the builder's own aid, not for review. 1600 x 1200, Cycles on the CPU, at most --threads
threads (the machine is shared), LEDGER_REVIEW_HDRI the overcast Bethnal Green entrance. review_render supplies the pavement; this script
adds, in the scene only and never in the .glb, what stands behind the front: a dark matt interior in the opening (the glass and the plain
door openings read against it, not against the sky), and nothing else (no wall, no neighbours).
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "tools"))
import bpy  # noqa: E402

import review_render as rr  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
HDRI = "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr"
GLB = os.path.join(REPO, "production", "assets", "cloud-week", "shopfront", "shopfront_ritas.glb")
PREVIEW_DIR = os.path.join(REPO, "production", "previews", "cloud-week", "shopfront")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-shopfront/render"


def views():
    """Metres, the model's own frame: x = 0 at the bay's middle, the wall face at y = 0, the street toward -y, z up."""
    return [
        {"name": "street", "loc": [1.2, -9.0, 1.6], "target": [0.0, 0.0, 1.85], "lens": 38},
        {"name": "close", "loc": [-1.55, -1.75, 2.65], "target": [-2.8, -0.08, 3.0], "lens": 30},
        {"name": "front", "ortho": 7.0, "loc": [0.0, -12.0, 1.8], "target": [0.0, 0.0, 1.8]},
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--only", default="street,close")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--glb", default=GLB)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--date", default="2026-10-11")
    ap.add_argument("--previews", default=PREVIEW_DIR)
    ap.add_argument("--no-previews", action="store_true")
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    vj = os.path.join(a.out, "views.json")
    json.dump(views(), open(vj, "w"), indent=1)

    orig_reset, orig_context = rr.reset, rr.context

    def reset():
        s = orig_reset()
        s.render.threads_mode = "FIXED"
        s.render.threads = a.threads
        return s

    def context(kind, lo, hi):
        orig_context(kind, lo, hi)
        # a dark matt interior behind the opening (u 350 to 5650, z 0 to 3.5: it reaches the cornice, so no sky shows under the board, and nothing shows above the cornice), set well back so the glass is lit from the street
        bpy.ops.mesh.primitive_cube_add(size=1.0, location=(0.0, 0.7, 1.75))
        ob = bpy.context.object
        ob.name = "ctx_interior"
        ob.scale = (5.3, 1.3, 3.5)
        m = bpy.data.materials.new("ctx_dark")
        m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.012, 0.011, 0.010, 1)
        b.inputs["Roughness"].default_value = 0.97
        ob.data.materials.append(m)

    rr.reset, rr.context = reset, context
    sys.argv = ["review_render.py", a.glb, a.out, "--views", vj, "--context", "street", "--samples", str(a.samples), "--width", "1600", "--height", "1200",
                "--hdri", HDRI, "--only", a.only]
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
        dst = os.path.join(a.previews, "shopfront-%s-v%d-%s.jpg" % (n, a.version, a.date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        print("preview", dst, os.path.getsize(dst))


if __name__ == "__main__":
    main()
