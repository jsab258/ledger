#!/usr/bin/env python
"""placed_decals.py: the paste plan, joined to the pictures (unit 4.2 to 4.4): which picture goes where on Quay Street.

    /home/user/.bpyenv/bin/python placed_decals.py OUTDIR

Reads target.json's `placements` (the target's own: surface, position, height, turn, layer, class) and OUTDIR/manifest.json; writes OUTDIR/placed_decals.json:
    placed:  the 46 default placements, each with the picture file of its class (basecolour, height, orm), its size in metres and `rot_deg` (the only place a skew or a turn lives:
             every picture is square-on). The newsagent's fifteen cards are one decal, SB1 (make_board.py), and are listed once.
    held:    the 16 held placements (named twins, nameless stand-ins, the gable's proof wall): not on the default street, listed so that nothing is forgotten.
Every default placement's class must be one the maker delivered for that item; a missing one is reported and exits 1.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_common as pc          # noqa: E402


def main(out):
    T = json.loads((pc.TARGET_DIR / "target.json").read_text(encoding="utf-8"))
    man = json.loads((Path(out) / "manifest.json").read_text())
    rows = {r["item"]: r for r in man["items"]}
    boards = {b["item"]: b for b in man.get("boards", [])}
    placed, held, missing = [], [], []
    seen_sb1 = False
    uses = {}
    for p in T["placements"]:
        e = {k: p[k] for k in ("item", "surface", "u_m", "u_centre_m", "street_x_m", "z_bottom_m", "rot_deg", "layer", "age_class", "w_m", "h_m", "note") if k in p}
        if p.get("held"):
            e["held_why"] = p.get("held_why", "")[:200]
            held.append(e)
            continue
        iid, cls = p["item"], p["age_class"]
        if iid == "SB1":
            if seen_sb1:
                continue
            seen_sb1 = True
            b = boards.get("SB1")
            if not b:
                missing.append("SB1: run make_board.py")
                continue
            e["files"] = dict(basecolour=b["basecolour"]["file"], height=b["height"]["file"], orm=b["orm"]["file"])
            placed.append(e)
            continue
        r = rows.get(iid)
        if not r or cls not in r["classes"]:
            missing.append("%s class %s (%s)" % (iid, cls, p["surface"]))
            continue
        c = r["classes"][cls]
        vs = [c] + c.get("seed_variants", [])
        pick = vs[uses.get((iid, cls), 0) % len(vs)]          # an item hung more than once (K03a on eight doors) takes its seed variants in turn
        uses[(iid, cls)] = uses.get((iid, cls), 0) + 1
        e["files"] = dict(basecolour=pick["basecolour"]["file"], height=pick["height"]["file"], orm=pick["orm"]["file"], glyphs=r["glyphs_json"]["file"])
        e["height_units_per_mm"] = c["height"]["units_per_mm"]
        e["px_per_mm"] = r["px_per_mm"]
        placed.append(e)
    plan = dict(schema="ledger.cloud-week-42.placed-decals/1", street_date="1990-10-29", placed=placed, held=held, missing=missing,
                note="rot_deg is the placement's turn (counter-clockwise, degrees); every picture is square-on. u_m counts from the surface's viewer's-left edge; street_x_m is metres along Quay Street.")
    (Path(out) / "placed_decals.json").write_text(json.dumps(plan, indent=1), encoding="utf-8")
    print("placed %d, held %d, missing %d" % (len(placed), len(held), len(missing)))
    for m in missing:
        print("  MISSING", m)
    return 1 if missing else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
