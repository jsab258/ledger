"""Review pictures of the kerbs and covers: review_scene.glb, the kit's own pieces placed as a player meets them (a run of granite kerb with its setts channel, a gully grate and a round
cover in the road, a stud cover in the footway, a stretch of concrete kerb and channel, and the dropped crossover at x 8 to 12.8 m); two views (Jafar, 11 October).

    /home/user/.bpyenv/bin/python render_kerbs.py [--out DIR] [--only street,close] [--samples 64] [--threads 2] [--glb PATH] [--previews DIR] [--version 1] [--date 2026-10-12]

street = the run from the carriageway's far side (3.5 m out, eye height 1.6 m, looking along and across the kerb), close = the crossover from 2.2 m, a little above the road (the lip row, the
ramp, the flank strips and the end blocks). 1600 x 1200, Cycles on the CPU, LEDGER_REVIEW_HDRI the overcast Bethnal Green entrance; review_supplies the pavement at z 0 (the channel's top);
the road and the footway are not modelled (they are the street's), so the kerb stands on a plain ground.
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
GLB = os.path.join(REPO, "production", "assets", "cloud-week", "kerbs-covers", "review_scene.glb")
PREVIEW_DIR = os.path.join(REPO, "production", "previews", "cloud-week", "kerbs-covers")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-kerbs-covers/render"


def views():
    """Metres, the model's frame: x along the kerb, y across (0 the kerb face, + toward the carriageway), z up from the channel's top."""
    return [
        {"name": "street", "loc": [-0.8, 2.9, 1.6], "target": [0.6, 0.0, 0.05], "lens": 30},
        {"name": "close", "loc": [10.4, 2.4, 1.1], "target": [10.4, -0.5, 0.05], "lens": 30},
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
    sys.argv = ["review_render.py", a.glb, a.out, "--views", vj, "--context", "none", "--samples", str(a.samples), "--width", "1600", "--height", "1200",
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
        dst = os.path.join(a.previews, "kerbs-covers-%s-v%d-%s.jpg" % (n, a.version, a.date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        print("preview", dst, os.path.getsize(dst))


if __name__ == "__main__":
    main()
