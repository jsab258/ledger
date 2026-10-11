"""Review pictures of Quay Street's pillar box: pillar_box.glb under the shared overcast sky, by tools/review_render.py (two views: street and close).

    /home/user/.bpyenv/bin/python render_pillarbox.py [--out DIR] [--only street,close] [--samples 64] [--threads 2]
                                                      [--glb PATH] [--previews DIR] [--version 1] [--date 2026-10-12]

The two views for review (Jafar, 11 October): street = the whole box from the opposite footway's distance (6 m out, eye height 1.6 m, a little to its right so the
hood and the cap show their depth); close = the cap, the hooded slot, the collection plate and the door's head from 1.45 m. 1600 x 1200, Cycles on the CPU, at most
--threads threads (the machine is shared), LEDGER_REVIEW_HDRI the overcast Bethnal Green entrance. review_render supplies the pavement; nothing else stands in the scene.
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
GLB = os.path.join(REPO, "production", "assets", "cloud-week", "pillar-box", "pillar_box.glb")
PREVIEW_DIR = os.path.join(REPO, "production", "previews", "cloud-week", "pillar-box")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-pillar-box/render"


def views():
    """Metres, the model's own frame: the axis at the origin, the front (door, slot, plate) toward +y, z up."""
    return [
        {"name": "street", "loc": [1.7, 6.0, 1.6], "target": [0.0, 0.0, 0.75], "lens": 38},
        {"name": "close", "loc": [0.6, 1.45, 1.3], "target": [0.0, 0.0, 1.12], "lens": 30},
    ]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    ap.add_argument("--only", default="street,close")
    ap.add_argument("--samples", type=int, default=64)
    ap.add_argument("--threads", type=int, default=2)
    ap.add_argument("--glb", default=GLB)
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--date", default="2026-10-12")
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
        dst = os.path.join(a.previews, "pillar-box-%s-v%d-%s.jpg" % (n, a.version, a.date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        print("preview", dst, os.path.getsize(dst))


if __name__ == "__main__":
    main()
