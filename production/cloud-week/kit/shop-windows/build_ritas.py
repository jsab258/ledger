#!/usr/bin/env python3
"""Rita's shop (the pawnbroker, east_parade bay 2): the whole thing, rebuilt exactly by one command.

    python3 build_ritas.py                 # every stage, in order
    python3 build_ritas.py front display   # some stages
    python3 build_ritas.py --list

Stages (each runs in its own Python so Blender's state never leaks from one to the next; needs bpy 5.2.2 as a module: /home/user/.bpyenv/bin/python has it, and this
script runs itself under that Python if the one it was started with has none):
  assets    fetch the 45 Poly Haven models and 2 textures into SCRATCH/polyhaven (1k), contact sheets, paint every maker's mark out of the maps (sw_assets.py)
  paper     the 4.1 fascia boards, signs and glass rows (production/cloud-week/2d/fascias/make_fascias.py) and the OPEN / CLOSED sign (2d/paper/make_paper.py) into SCRATCH
  front     the whole front from the 3.2 kit's parts, the doors, the band, the fascia, the signs and the grille (sw_front.py)
  display   the near metre as real meshes (sw_display.py)
  room      the room (target 4.4): light strengths calibrated to the approved pictures' means, then the three 4096 x 1855 pictures and their JSON (sw_room.py)
  gate      per review camera, the card baked through the game's `trace`, the front + display + glass rendered at 2560 x 1440 (sw_gate.py), the review set to previews
  checks    every check of the target that applies, one row each: checks/check_ritas_v1.json, printing "N of M rows pass" (check_ritas.py)

Where things go: models in production/assets/cloud-week/shop-windows/ (the front, the display and the lattice are over 1 MB: out of git, listed in .git/info/exclude, rebuilt here);
heavy outputs (pictures, bakes, renders, Poly Haven files) in SCRATCH (default /home/user/ledger-scratch; F:/LedgerTools on the PC); previews in production/previews/cloud-week/shop-windows/.
"""
import json
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
WORK = os.path.join(SCRATCH, "shop-windows")
ASSETS = os.path.join(REPO, "production", "assets", "cloud-week", "shop-windows")
PREVIEWS = os.path.join(REPO, "production", "previews", "cloud-week", "shop-windows")
PY = os.environ.get("LEDGER_BPY", "/home/user/.bpyenv/bin/python")
STAGES = ["assets", "paper", "front", "display", "room", "gate", "checks"]
ROOM_SAMPLES = int(os.environ.get("LEDGER_ROOM_SAMPLES", "64"))
GATE_SAMPLES = int(os.environ.get("LEDGER_GATE_SAMPLES", "48"))


def run_inner(stage):
    sys.path.insert(0, HERE)
    t0 = time.time()
    if stage == "assets":
        import sw_assets as A
        A.fetch()
        A.sheets()
        A.blank()
        rows = A.verify()
        print("assets: INV-06 script rows %d of %d pass" % (sum(1 for r in rows if r["ok"]), len(rows)))
    elif stage == "paper":
        os.makedirs(WORK, exist_ok=True)
        fasc = os.path.join(WORK, "fascias")
        paper = os.path.join(WORK, "paper")
        for cmd in ([PY, os.path.join(REPO, "production", "cloud-week", "2d", "fascias", "make_fascias.py"), fasc, "--only", "ritas,signs,glass,panels", "--seed-base", "1", "--jobs", "3"],
                    [PY, os.path.join(REPO, "production", "cloud-week", "2d", "paper", "make_paper.py"), paper, "--only", "K03a,K03b", "--seed-base", "1", "--jobs", "2"]):
            subprocess.run(cmd, check=True)
    elif stage == "front":
        import sw_front as F
        F.build_front(ASSETS, WORK, os.path.join(WORK, "fascias"), os.path.join(WORK, "paper"))
    elif stage == "display":
        import sw_display as Dp
        Dp.build_display(os.path.join(WORK, "display_work"), ASSETS)
    elif stage == "room":
        import sw_room as S
        rooms = os.path.join(WORK, "rooms")
        os.makedirs(rooms, exist_ok=True)
        r = S.build_scene(rooms)
        pj = os.path.join(rooms, "light_params.json")
        if os.environ.get("LEDGER_REUSE_CAL") and os.path.exists(pj):
            P = json.load(open(pj))          # the light strengths calibrated on the same scene (skips about four minutes)
        else:
            P = S.calibrate(r, rooms)
        times = S.render_states(r, rooms, P, rooms, samples=ROOM_SAMPLES)
        json.dump({"times_s": times, "samples": ROOM_SAMPLES, "params": P}, open(os.path.join(rooms, "render_times.json"), "w"), indent=1)
        json.dump(r.placed, open(os.path.join(rooms, "placed.json"), "w"), indent=0)
        json.dump(r.fixtures, open(os.path.join(rooms, "fixtures.json"), "w"), indent=0)
    elif stage == "gate":
        import sw_gate_run as G
        G.run(WORK, ASSETS, PREVIEWS, GATE_SAMPLES)
    elif stage == "checks":
        import check_ritas as C
        C.run(WORK, ASSETS, PREVIEWS, os.path.join(HERE, "checks", "check_ritas_v1.json"))
    print("stage %s: %.0f s" % (stage, time.time() - t0), flush=True)


def main(argv):
    if "--list" in argv:
        print("\n".join(STAGES))
        return 0
    if "--inner" in argv:
        run_inner(argv[argv.index("--inner") + 1])
        return 0
    stages = [a for a in argv if a in STAGES] or STAGES
    for st in stages:
        r = subprocess.run([PY, os.path.abspath(__file__), "--inner", st])
        if r.returncode != 0:
            print("stage %s failed (exit %d)" % (st, r.returncode))
            return r.returncode
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
