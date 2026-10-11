"""Review pictures of the guard rail panel: guard_rail_A1.glb under the shared overcast sky, by tools/review_render.py (two views: street and close).

    /home/user/.bpyenv/bin/python render_railings.py [--out DIR] [--only street,close] [--version 1] [--date 2026-10-12]

The docstring below is the shopfront wrapper's:


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
GLB = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-bollards/bollards_row.glb"
PREVIEW_DIR = os.path.join(REPO, "production", "previews", "cloud-week", "bollards")
DEFAULT_OUT = "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/kit-bollards/render"


def views():
    """Metres: the row runs along x from -2.6 to 2.6 (K1, K2, K2b, K3, K4, K6, K6b, K5), the footway side is -y, z up."""
    return [
        {"name": "street", "loc": [0.0, -7.0, 1.6], "target": [0.0, 0.0, 0.5], "lens": 38},
        {"name": "close", "loc": [1.9, -1.0, 0.85], "target": [2.6, 0.0, 0.35], "lens": 32},
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
        dst = os.path.join(a.previews, "bollards-%s-v%d-%s.jpg" % (n, a.version, a.date))
        for q in (92, 88, 84, 80, 75, 70, 65, 60):
            im.save(dst, quality=q, optimize=True)
            if os.path.getsize(dst) < 480 * 1024:
                break
        print("preview", dst, os.path.getsize(dst))


if __name__ == "__main__":
    main()
