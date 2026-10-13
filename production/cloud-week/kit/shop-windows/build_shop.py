#!/usr/bin/env python3
"""One shop's whole shop-window kit, rebuilt exactly by one command (13 October 2026, generalised from build_ritas.py).

    python3 build_shop.py --shop ritas                  # every stage, in order
    python3 build_shop.py --shop ironmonger front       # some stages
    python3 build_shop.py --list --shop newsagent       # the stages that shop has

Shops: ritas (the pawnbroker, east_parade bay 2: the worked example), ironmonger, newsagent, tea_rooms (west_north bays 1, 0, 2), and the two fronts without a new room: mickeys (its approved room already
exists) and empty_unit (to let: whitewashed glass, no room). Every number about a shop comes from production/cloud-week/targets/shop-windows/target.json (sw_ctx.Ctx); the code holds none.

Stages (each runs in its own Python so Blender's state never leaks from one to the next; needs bpy 5.2.2 as a module: /home/user/.bpyenv/bin/python has it, and this script runs itself under that Python
if the one it was started with has none):
  assets    fetch the shop's Poly Haven models and textures (1k) into SCRATCH/polyhaven, contact sheets, paint every maker's mark out of the maps (sw_assets.py)       [shops with a room]
  paper     the 4.1 fascia boards, signs and glass rows (production/cloud-week/2d/fascias/make_fascias.py) into the shop's folder, and the OPEN / CLOSED sign (2d/paper/make_paper.py, one for all shops)
  front     the whole front from the 3.2 kit's parts, the doors, the band, the fascia, the signs (sw_front.py + sw_variants.py)
  display   the near metre as real meshes (sw_display.py for Rita's, sw_display_gen.py for the others)                                                                      [shops with a room]
  room      the room (target 4.4): light strengths calibrated to the approved pictures' means, then the three 4096 x 1855 pictures and their JSON (sw_room.py / sw_room_gen.py)  [shops with a room]
  gate      per review camera, the card baked through the game's `trace`, the front + display + glass rendered at 2560 x 1440 (sw_gate.py), the review set to previews
  (scenecheck  not a stage of the run: `build_shop.py --shop X scenecheck` builds the room's scene and runs SO-01 to SO-07 on it in seconds, before the hour's render)
  checks    every check of the target that applies, one row each: checks/check_<shop>_<version>.json, printing "N of M rows pass" (check_shop.py; Rita's: check_ritas.py's v3 rows)

Where things go: models in production/assets/cloud-week/shop-windows/ (the ones over 1 MB are out of git, listed in .git/info/exclude, rebuilt here);
heavy outputs (pictures, bakes, renders, Poly Haven files) in SCRATCH (default /home/user/ledger-scratch; F:/LedgerTools on the PC); previews in production/previews/cloud-week/shop-windows/.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
ASSETS = os.path.join(REPO, "production", "assets", "cloud-week", "shop-windows")
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "shop-windows")
PY = os.environ.get("LEDGER_BPY", "/home/user/.bpyenv/bin/python")
ALL_STAGES = ["assets", "paper", "front", "display", "room", "gate", "checks"]
ROOM_SAMPLES = int(os.environ.get("LEDGER_ROOM_SAMPLES", "64"))
GATE_SAMPLES = int(os.environ.get("LEDGER_GATE_SAMPLES", "32"))
CHECK_VERSION = os.environ.get("LEDGER_CHECK_VERSION", "")        # "" -> v1 for the new shops, v3 for Rita's


def stages_of(shop):
    sys.path.insert(0, HERE)
    import sw_ctx
    ctx = sw_ctx.Ctx(shop)
    out = []
    for st in ALL_STAGES:
        if st in ("assets", "display", "room") and not ctx.has_room:
            continue
        out.append(st)
    return out


def run_inner(shop, stage):
    sys.path.insert(0, HERE)
    import sw_ctx
    ctx = sw_ctx.Ctx(shop)
    t0 = time.time()
    rita = shop == "ritas"
    if stage == "assets":
        import sw_assets as A
        A.set_shop(shop)
        A.WORK = ctx.work
        os.makedirs(ctx.work, exist_ok=True)
        A.fetch_all()
        A.sheets()
        A.blank()
        rows = A.verify()
        print("assets: INV-06 script rows %d of %d pass" % (sum(1 for r in rows if r["ok"]), len(rows)))
    elif stage == "paper":
        os.makedirs(ctx.work, exist_ok=True)
        only = "%s,signs,glass,panels" % shop
        cmds = [[PY, os.path.join(REPO, "production", "cloud-week", "2d", "fascias", "make_fascias.py"), ctx.fascias, "--only", only, "--seed-base", "1", "--jobs", "3"]]
        if not os.path.exists(os.path.join(ctx.paper, "K03b")) or rita:
            cmds.append([PY, os.path.join(REPO, "production", "cloud-week", "2d", "paper", "make_paper.py"), ctx.paper, "--only", "K03a,K03b", "--seed-base", "1", "--jobs", "2"])
        for cmd in cmds:
            subprocess.run(cmd, check=True)
    elif stage == "front":
        import sw_front as F
        F.build_front(ASSETS, ctx.work, ctx.fascias, ctx.paper, ctx=ctx)
    elif stage == "display":
        if rita:
            import sw_display as Dp
            Dp.build_display(ctx.display_work, ASSETS)
        else:
            import sw_assets as A
            import sw_display_gen as DG
            A.set_shop(shop)
            A.WORK = ctx.work
            DG.build_display(ctx.display_work, ASSETS, ctx)
    elif stage == "room":
        import sw_assets as A
        A.set_shop(shop)
        A.WORK = ctx.work
        rooms = ctx.rooms
        os.makedirs(rooms, exist_ok=True)
        if rita:
            import sw_room as S
            r = S.build_scene(rooms)
        else:
            import sw_room_gen as RG
            r = RG.build_scene(rooms, ctx)
        pj = os.path.join(rooms, "light_params.json")
        if os.environ.get("LEDGER_REUSE_CAL") and os.path.exists(pj):
            P = json.load(open(pj))          # the light strengths calibrated on the same scene (skips about four minutes)
        else:
            if rita:
                import sw_room as S
                P = S.calibrate(r, rooms)
            else:
                P = r.calibrate(rooms)
        only = [x for x in os.environ.get("LEDGER_ROOM_STATES", "").split(",") if x]       # a state rendered again, the others kept (e.g. night_dark)
        if rita:
            import sw_room as S
            times = S.render_states(r, rooms, P, rooms, samples=ROOM_SAMPLES)
        else:
            times = r.render_states(rooms, P, rooms, samples=ROOM_SAMPLES, **({"states": tuple(only)} if only else {}))
        tp = os.path.join(rooms, "render_times.json")
        if only and os.path.exists(tp):
            prev = json.load(open(tp))["times_s"]
            prev.update(times)
            times = prev
        json.dump({"times_s": times, "samples": ROOM_SAMPLES, "params": P}, open(tp, "w"), indent=1)
        json.dump(r.placed, open(os.path.join(rooms, "placed.json"), "w"), indent=0)
        json.dump(r.fixtures, open(os.path.join(rooms, "fixtures.json"), "w"), indent=0)
        if not rita:
            json.dump(getattr(r, "notes", []), open(os.path.join(rooms, "layout_notes.json"), "w"), indent=1)
            json.dump(getattr(r, "rows", {}), open(os.path.join(rooms, "rows.json"), "w"), indent=1)
            json.dump(getattr(r, "texts", []), open(os.path.join(rooms, "texts.json"), "w"), indent=1)
        # the masters' copies beside the glbs (out of git: .git/info/exclude lists the folder); on the PC the masters go to F:/LedgerTools/shop-rooms
        dst = os.path.join(ASSETS, "rooms")
        os.makedirs(dst, exist_ok=True)
        for st in ("day", "night_lit", "night_dark"):
            shutil.copyfile(os.path.join(rooms, "%s_%s.png" % (ctx.picture_name, st)), os.path.join(dst, "%s_%s.png" % (ctx.picture_name, st)))
        shutil.copyfile(os.path.join(rooms, "%s.json" % ctx.picture_name), os.path.join(dst, "%s.json" % ctx.picture_name))
    elif stage == "scenecheck":
        # the room's layout tested without the hour's render: the scene is built, its placement written to rooms_scene/ and the stand-off and intersection rows (SO-01 to SO-07) run on it
        import sw_assets as A
        import check_shop as CS
        import check_try2 as X
        import sw_room_gen as RG
        A.set_shop(shop)
        A.WORK = ctx.work
        X.use(ctx)
        sdir = os.path.join(ctx.work, "rooms_scene")
        os.makedirs(sdir, exist_ok=True)
        r = RG.build_scene(sdir, ctx)
        json.dump(r.placed, open(os.path.join(sdir, "placed.json"), "w"))
        json.dump(r.fixtures, open(os.path.join(sdir, "fixtures.json"), "w"))
        keep, ctx.rooms = ctx.rooms, sdir
        rows = CS.Rows()
        CS.room_rows(ctx, rows, ASSETS)
        ctx.rooms = keep
        X.so07_rows(ctx.work, rows)
        for rr in rows.rows:
            print(rr["status"].upper(), rr["id"], rr["detail"][:900])
        for n in getattr(r, "notes", []):
            print("NOTE", n)
    elif stage == "gate":
        import sw_gate_run as G
        vw = [tuple(v.split(":")) for v in os.environ.get("LEDGER_GATE_VIEWS", "").split(",") if v]       # e.g. STREET_SQUARE:night_lit: only those frames again, the check renders kept
        if vw:
            G.run(ctx.work, ASSETS, PREVIEWS, GATE_SAMPLES, views=vw, check_renders=False, ctx=ctx)
        else:
            G.run(ctx.work, ASSETS, PREVIEWS, GATE_SAMPLES, ctx=ctx)
    elif stage == "checks":
        if rita:
            import check_ritas as C
            C.run(ctx.work, ASSETS, PREVIEWS, os.path.join(HERE, "checks", "check_ritas_%s.json" % (CHECK_VERSION or "v3")))
        else:
            import check_shop as C
            C.run(ctx, ASSETS, PREVIEWS, os.path.join(HERE, "checks", "check_%s_%s.json" % (shop, CHECK_VERSION or "v1")))
    print("stage %s (%s): %.0f s" % (stage, shop, time.time() - t0), flush=True)


def main(argv):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--shop", default="ritas")
    ap.add_argument("--list", action="store_true")
    ap.add_argument("--inner", default=None)
    ap.add_argument("stages", nargs="*")
    a = ap.parse_args(argv)
    if a.list:
        print("\n".join(stages_of(a.shop)))
        return 0
    if a.inner:
        run_inner(a.shop, a.inner)
        return 0
    have = stages_of(a.shop)
    stages = [s for s in a.stages if s in ALL_STAGES or s == "scenecheck"] or have
    for st in stages:
        if st not in have and st != "scenecheck":
            print("stage %s: not for %s (no room), skipped" % (st, a.shop))
            continue
        r = subprocess.run([PY, os.path.abspath(__file__), "--shop", a.shop, "--inner", st])
        if r.returncode != 0:
            print("stage %s failed (exit %d)" % (st, r.returncode))
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
