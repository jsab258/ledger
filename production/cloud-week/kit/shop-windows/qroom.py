#!/usr/bin/env python3
"""A quick look at a shop's room (batch B, 14 October 2026): the scene built from the shop's layout, rendered from the card's camera at a small size and a few samples with the light strengths of a previous
calibration if there is one (SCRATCH/shop-windows/<shop>/rooms/light_params.json) or rough ones; a picture to look at in seconds before the hour's render. Not a deliverable.

    python3 qroom.py --shop steam_laundry [--state day] [--res 1280x580] [--samples 16] [--crop x0,y0,x1,y1]
"""
import argparse
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("LEDGER_BPY", "/home/user/.bpyenv/bin/python")
VIEW = os.environ.get("LEDGER_SW_VIEW", "/tmp/claude-0/-home-user-ledger/6ce8dcad-c1af-55c1-8a8d-c9e781414d13/scratchpad/view")


def inner(a):
    sys.path.insert(0, HERE)
    import sw_assets as A
    import sw_ctx
    import sw_room as S
    import sw_room_gen as RG
    ctx = sw_ctx.Ctx(a.shop)
    A.set_shop(a.shop)
    A.WORK = ctx.work
    work = os.path.join(ctx.work, "rooms_quick")
    os.makedirs(work, exist_ok=True)
    r = RG.build_scene(work, ctx)
    pj = os.path.join(ctx.rooms, "light_params.json")
    P = json.load(open(pj)) if os.path.exists(pj) else dict(S.DEFAULT_P)
    if not os.path.exists(pj):
        P["tube"], P["day"], P["sodium_ratio"] = 60.0, 900.0, 0.12
    res = tuple(int(v) for v in a.res.split("x"))
    os.makedirs(VIEW, exist_ok=True)
    out = os.path.join(VIEW, "qroom_%s_%s.png" % (a.shop, a.state))
    r.set_state(a.state, P)
    r.render(out, a.samples, res)
    if a.crop:
        from PIL import Image
        x0, y0, x1, y1 = [int(v) for v in a.crop.split(",")]
        Image.open(out).crop((x0, y0, x1, y1)).save(out.replace(".png", "_crop.png"))
    print(out)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", required=True)
    ap.add_argument("--state", default="day")
    ap.add_argument("--res", default="1280x580")
    ap.add_argument("--samples", type=int, default=16)
    ap.add_argument("--crop", default=None)
    ap.add_argument("--inner", action="store_true")
    a = ap.parse_args()
    if a.inner:
        inner(a)
    else:
        sys.exit(subprocess.run([PY, os.path.abspath(__file__), "--inner"] + sys.argv[1:]).returncode)
