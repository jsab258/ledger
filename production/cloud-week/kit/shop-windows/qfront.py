#!/usr/bin/env python3
"""A quick look at a built front (batch B tool, 14 October 2026): the front glb alone in front of a flat mid-grey card, from one review camera, at a small size and a few samples, so that the geometry of a
new front can be looked at in seconds before any room is rendered. Not a gate frame and not a check: nothing here is a deliverable.

    python3 qfront.py --shop steam_laundry [--cam STREET_SQUARE] [--state day] [--res 1280x720] [--samples 12] [--display] [--out FILE]

With --display the shop's display glb is put in the window as well (after the display stage). Writes to the scratchpad's view folder unless --out is given.
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("LEDGER_BPY", "/home/user/.bpyenv/bin/python")
VIEW = os.environ.get("LEDGER_SW_VIEW", "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/view")


def inner(a):
    sys.path.insert(0, HERE)
    import numpy as np
    from PIL import Image
    import sw_ctx
    import sw_gate as G
    ctx = sw_ctx.Ctx(a.shop)
    os.makedirs(VIEW, exist_ok=True)
    card = os.path.join(VIEW, "grey_card.png")
    Image.fromarray(np.full((G.CARD_PX[1], G.CARD_PX[0], 3), (120, 112, 100), np.uint8)).save(card)
    out = a.out or os.path.join(VIEW, "q_%s_%s_%s.png" % (a.shop, a.cam, a.state))
    res = tuple(int(v) for v in a.res.split("x"))
    front = os.path.join(sw_ctx.ASSETS, ctx.front_glb)
    disp = os.path.join(sw_ctx.ASSETS, ctx.display_glb) if a.display else None
    grille = os.path.join(sw_ctx.ASSETS, ctx.grille_glb) if (ctx.has_grille and a.state != "day") else None
    G.render_view(a.cam, ctx.R["cameras"][a.cam], a.state, card, out, front, grille, disp, "/home/user/cache/hdri/bethnal_green_entrance_2k.hdr", samples=a.samples,
                  extra={"lamp_w": 50000, "spill_w": 150, "strip_w": 0.0}, res=res, ctx=ctx)
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", required=True)
    ap.add_argument("--cam", default="STREET_SQUARE")
    ap.add_argument("--state", default="day")
    ap.add_argument("--res", default="1280x720")
    ap.add_argument("--samples", type=int, default=12)
    ap.add_argument("--display", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--inner", action="store_true")
    a = ap.parse_args()
    if a.inner:
        inner(a)
    else:
        sys.exit(subprocess.run([PY, os.path.abspath(__file__), "--inner"] + sys.argv[1:]).returncode)
