#!/usr/bin/env python3
"""The front's rows of one shop alone (batch B, 14 October 2026): `front_rows` on the built front glb and its members file, without the room, the display or the gate, so that a front's faults show in
seconds. The rows that need the gate's frames print as failing here (that is not a finding). Not a deliverable.

    python3 check_front_only.py --shop steam_laundry
"""
import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PY = os.environ.get("LEDGER_BPY", "/home/user/.bpyenv/bin/python")


def inner(a):
    sys.path.insert(0, HERE)
    import sw_ctx
    import sw_assets as A
    import check_shop as C
    import check_try2 as X
    ctx = sw_ctx.Ctx(a.shop)
    A.set_shop(a.shop)
    A.WORK = ctx.work
    X.use(ctx)
    rows = C.Rows()
    assets = os.path.join(sw_ctx.ASSETS)
    try:
        C.front_rows(ctx, rows, assets)
    except Exception as e:       # the row that stopped it is the first finding
        import traceback
        traceback.print_exc()
    for r in rows.rows:
        print(r["status"].upper(), r["id"], r["name"], "|", r["detail"][:int(a.width)])


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--shop", required=True)
    ap.add_argument("--width", default="500")
    ap.add_argument("--inner", action="store_true")
    a = ap.parse_args()
    if a.inner:
        inner(a)
    else:
        sys.exit(subprocess.run([PY, os.path.abspath(__file__), "--inner"] + sys.argv[1:]).returncode)
