#!/usr/bin/env python3
"""A Kiln drape's OBJ rewritten in the layout the garment chain reads (Marvelous's export, as
tools/meshgen/blender/import_md_drape.py and tools/md/unpose_garment.py take it). Machine-free: plain Python, no
Blender, no Unreal; inputs are only read.

    python tools/kiln_to_game.py KILN.obj PLAN.json OUT_DIR [--name work_trousers] [--body-name KilnBody_LOD0]
        [--tol 0.05] [--scale-tol 0.005]
    python tools/kiln_to_game.py --selftest        # on real Kiln outputs (Ron's work trousers, Tom's jumper)

WHY, 17 November 2026 (n16-1, Kiln's parity list gap 1: no Kiln drape has reached the game; plan:
production/research/phase2-plan/KILN-TO-GAME-PLAN-2026-11-17.md). Read from both sides' code the same day:

- Kiln's OBJ (engines/drapestudio/src/export.rs write_obj; serve.rs "export_obj" and avatar_obj; reached from a job
  script's ExportOBJ through python/kiln_front/compat.py) is already millimetres, y up ("app" space), one "g" group
  per pattern named as the plan's key, seam partners welded (8 mm, mechanics.rs SEW_CLOSE_GAP), the body appended as
  one group "g Avatar" when the job exports the avatar. Its "vt" lines are each piece's own flat pattern points at
  true size in metres, v negated (uv.x / 1000, -uv.y / 1000), each piece where Kiln's pattern space puts it.
- import_md_drape.py fits each piece's UVs onto the plan's outline with a positive tile per axis (no flip) and fails
  the drape when a boundary vertex lands over --tol (0.05 mm) off that outline. Kiln's pattern space is the plan's
  with y turned over (frontR's first point: plan (-16.05, -30.32), .drape (0, 30.32)); the negated v undoes that, so
  Kiln's "vt" are the plan's own frame shifted along x by its layout (measured on both self-test garments: every
  piece fits at signs (1, 1) and y shift 0 to 0.011 mm). The import's fit would therefore accept them as they are
  (tile 1000); this tool still rewrites them onto the plan exactly, so the boundary check is made here, before any
  Blender run, and a turned-over or wrong-size piece is refused by name.
- The blocker: the import takes the drape's body only from a group whose name ends in "_LOD0" (its body-fit check,
  then removed). Kiln names it "Avatar", so bodyFitMm is missing (counted as 99, ok false) and the body stays in the
  .blend as a stray mesh beside the FBX's own. unpose_garment.py picks the body by "_LOD0" first, then by size.

WHAT IT DOES. For each plan piece: its boundary (edges used once in its UV faces), the sign of each axis and the
shift that put those boundary points on the plan's outline (box centres matched; the straight fit, signs (1, 1),
unless it misses by over --tol, then the best of the four sign pairs, reported as flipped), the scale checked to be
1 (true size), and the worst boundary distance written; the UVs then rewritten
as plan millimetres / 1000, so the import's fit is the identity. "g Avatar" becomes "g <--body-name>". Positions,
normals and faces are copied unchanged. OUT_DIR gets <name>.obj and kiln_to_game.json (inputs with their sha256,
per-piece sign, shift, scale and boundary error, the checks, ok). ok needs every plan piece present, no group
outside the plan but the body, no piece turned over, scale within --scale-tol, every boundary within --tol mm.
"""
import hashlib
import json
import math
import os
import sys

OUT_ROOT = "F:/LedgerTools/game-inputs/kiln-to-game"


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def read_obj(path):
    """Lines kept in order; per group the faces' (v, vt) index triples (1-based, absolute)."""
    lines = open(path, encoding="utf-8").read().splitlines()
    vts, groups, order, cur = [], {}, [], None
    for ln in lines:
        if ln.startswith("vt "):
            a = ln.split()
            vts.append((float(a[1]), float(a[2])))
        elif ln.startswith("g "):
            cur = ln[2:].strip()
            if cur not in groups:
                groups[cur] = []
                order.append(cur)
        elif ln.startswith("f "):
            corners = []
            for tok in ln.split()[1:]:
                p = tok.split("/")
                corners.append((int(p[0]), int(p[1]) if len(p) > 1 and p[1] else 0))
            groups.setdefault(cur, []).append(corners)
    return lines, vts, groups, order


def seg_dist(q, a, b):
    dx, dy = b[0] - a[0], b[1] - a[1]
    dd = dx * dx + dy * dy
    t = 0.0 if dd == 0 else max(0.0, min(1.0, ((q[0] - a[0]) * dx + (q[1] - a[1]) * dy) / dd))
    return math.hypot(q[0] - a[0] - t * dx, q[1] - a[1] - t * dy)


def poly_dist(q, pts):
    return min(seg_dist(q, pts[i], pts[(i + 1) % len(pts)]) for i in range(len(pts)))


def box(pts):
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return min(xs), max(xs), min(ys), max(ys)


def fit_piece(faces, vts, outline, tol=0.05):
    """Sign per axis, shift and scale putting the piece's UV boundary (in mm) onto the plan outline."""
    used = sorted({c[1] for f in faces for c in f})
    if not used or 0 in used:
        return None
    count = {}
    for f in faces:
        for i in range(len(f)):
            e = tuple(sorted((f[i][1], f[(i + 1) % len(f)][1])))
            count[e] = count.get(e, 0) + 1
    bnd = sorted({k for e, n in count.items() if n == 1 for k in e})
    mm = {k: (vts[k - 1][0] * 1000.0, vts[k - 1][1] * 1000.0) for k in used}
    ox0, ox1, oy0, oy1 = box(outline)
    ux0, ux1, uy0, uy1 = box(list(mm.values()))
    scale = ((ox1 - ox0) / max(ux1 - ux0, 1e-9), (oy1 - oy0) / max(uy1 - uy0, 1e-9))
    oc = ((ox0 + ox1) / 2, (oy0 + oy1) / 2)
    uc = ((ux0 + ux1) / 2, (uy0 + uy1) / 2)
    # Kiln's pattern space is the plan's shifted along x (measured on both self-test garments: every piece that is
    # not mirror-symmetric fits at sign (1, 1), y shift 0), so the straight fit is kept whenever it is within tol;
    # a turned-over fit is tried only when it is not, and reported ("flipped"), since on a symmetric piece (a
    # rectangle band, a jumper's back) a flip fits as well and would mirror the texture.
    def worst_of(sx, sy, ks):
        return max(poly_dist((sx * (mm[k][0] - uc[0]) + oc[0], sy * (mm[k][1] - uc[1]) + oc[1]), outline) for k in ks)
    sx, sy, flipped = 1, 1, False
    if worst_of(1, 1, bnd) > tol:
        probe = bnd[:: max(1, len(bnd) // 60)]
        _, sx, sy = min((worst_of(a, b, probe), a, b) for a in (1, -1) for b in (1, -1))
        flipped = (sx, sy) != (1, 1)
    mapped = {k: (sx * (p[0] - uc[0]) + oc[0], sy * (p[1] - uc[1]) + oc[1]) for k, p in mm.items()}
    worst = max(poly_dist(mapped[k], outline) for k in bnd) if bnd else float("inf")
    return {"sign": [sx, sy], "shiftMm": [round(oc[0] - sx * uc[0], 4), round(oc[1] - sy * uc[1], 4)],
            "scale": [round(scale[0], 6), round(scale[1], 6)], "boundaryPoints": len(bnd),
            "uvPoints": len(used), "faces": len(faces), "flipped": flipped, "boundaryWorstMm": round(worst, 4)}, mapped


def convert(obj_path, plan_path, out_dir, name=None, body_name="KilnBody_LOD0", tol=0.05, scale_tol=0.005):
    name = name or os.path.splitext(os.path.basename(obj_path))[0]
    out_abs = os.path.abspath(out_dir).replace("\\", "/")
    assert out_abs.lower().startswith(OUT_ROOT.lower()), "outputs only under %s" % OUT_ROOT
    for p in (obj_path, plan_path):
        assert os.path.abspath(p).replace("\\", "/").lower() != out_abs.lower(), "an input in the output folder"
    src_sha = {obj_path: sha256(obj_path), plan_path: sha256(plan_path)}
    plan = json.load(open(plan_path, encoding="utf-8"))
    outlines = {p["key"]: [(x, y) for x, y, *_ in p["points"]] for p in plan["pieces"]}
    lines, vts, groups, order = read_obj(obj_path)
    rep = {"source": {"obj": obj_path, "plan": plan_path, "sha256": src_sha}, "name": name, "pieces": {},
           "groups": order, "checks": {}}
    missing = [k for k in outlines if k not in groups]
    body_groups = [g for g in order if g not in outlines]
    rep["checks"]["missingPieces"] = missing
    rep["checks"]["extraGroups"] = [g for g in body_groups if g != "Avatar"]
    rep["checks"]["bodyGroup"] = "Avatar" in groups
    new_uv = {}
    for key, outline in outlines.items():
        if key not in groups:
            continue
        got = fit_piece(groups[key], vts, outline, tol)
        if got is None:
            rep["pieces"][key] = {"error": "faces without UVs"}
            continue
        info, mapped = got
        rep["pieces"][key] = info
        for k, q in mapped.items():
            assert k not in new_uv, "a UV point shared by two pieces (%s)" % key
            new_uv[k] = (q[0] / 1000.0, q[1] / 1000.0)
    worst = max((p.get("boundaryWorstMm", float("inf")) for p in rep["pieces"].values()), default=float("inf"))
    scale_off = max((abs(s - 1.0) for p in rep["pieces"].values() for s in p.get("scale", [9, 9])), default=9)
    rep["checks"]["boundaryWorstMm"] = worst
    rep["checks"]["scaleWorstOff"] = round(scale_off, 6)
    rep["checks"]["flippedPieces"] = [k for k, p in rep["pieces"].items() if p.get("flipped")]
    rep["checks"]["uvRewritten"] = len(new_uv)
    rep["checks"]["uvTotal"] = len(vts)
    rep["ok"] = (not missing and not rep["checks"]["extraGroups"] and worst <= tol and scale_off <= scale_tol
                 and not rep["checks"]["flippedPieces"] and all("error" not in p for p in rep["pieces"].values()))
    # the file: every line kept but the rewritten vt lines and the body's group name
    out, vt_i = [], 0
    for ln in lines:
        if ln.startswith("vt "):
            vt_i += 1
            if vt_i in new_uv:
                u, v = new_uv[vt_i]
                ln = "vt %.6f %.6f" % (u, v)
        elif ln.strip() == "g Avatar":
            ln = "g " + body_name
        out.append(ln)
    if out and out[0].startswith("#"):
        out.insert(1, "# kiln_to_game.py: UVs on the plan outline (mm / 1000), body group %s" % body_name)
    os.makedirs(out_abs, exist_ok=True)
    obj_out = os.path.join(out_abs, name + ".obj")
    with open(obj_out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")
    rep["out"] = obj_out.replace("\\", "/")
    rep["bodyName"] = body_name if rep["checks"]["bodyGroup"] else None
    rep["inputsUnchanged"] = all(sha256(p) == h for p, h in src_sha.items())
    rep["ok"] = rep["ok"] and rep["inputsUnchanged"]
    json.dump(rep, open(os.path.join(out_abs, "kiln_to_game.json"), "w", encoding="utf-8"), indent=1)
    return rep


SELFTEST = [
    # Ron's work trousers: a real Kiln export of the job (the 20 mm pass's first stage, unwelded, no body); the
    # passing run's final OBJ is no longer on disk (kiln-armline-2026-11-16 keeps its .drape and pictures only)
    ("trousers", "F:/LedgerTools/tool-dev/runs/kiln-patcheck-2026-11-16/work_trousers/stages/p20_000.obj",
     "F:/LedgerTools/garments/ron/kiln-outfit-2026-11-16/work_trousers_job.plan.json", False),
    # Tom's jumper j3: a real final Kiln export, welded, with the body appended ("g Avatar")
    ("jumper", "F:/LedgerTools/tool-dev/runs/kiln-bodystd-2026-11-16/j3/jumper.obj",
     "F:/LedgerTools/tool-dev/runs/kiln-bodystd-2026-11-16/j3_plan.json", True),
]


def selftest():
    fails = []
    for tag, obj, plan, has_body in SELFTEST:
        rep = convert(obj, plan, OUT_ROOT + "/selftest/" + tag, name=tag)
        c = rep["checks"]
        print("SELFTEST %s ok=%s boundaryWorstMm=%s scaleWorstOff=%s pieces=%d body=%s unchanged=%s" % (
            tag, rep["ok"], c["boundaryWorstMm"], c["scaleWorstOff"], len(rep["pieces"]), c["bodyGroup"],
            rep["inputsUnchanged"]))
        if not rep["ok"]:
            fails.append(tag + ": not ok")
        if c["bodyGroup"] != has_body:
            fails.append(tag + ": body group expected %s" % has_body)
        # the written file read back: the body renamed, the same counts, the UVs of each piece on its outline
        lines2, vts2, groups2, order2 = read_obj(rep["out"])
        lines1, vts1, groups1, order1 = read_obj(obj)
        if has_body and ("KilnBody_LOD0" not in groups2 or "Avatar" in groups2):
            fails.append(tag + ": body group not renamed")
        if len(vts2) != len(vts1) or sum(len(f) for f in groups2.values()) != sum(len(f) for f in groups1.values()):
            fails.append(tag + ": counts changed")
        if [l for l in lines1 if l.startswith(("v ", "vn ", "f "))] != [l for l in lines2 if l.startswith(("v ", "vn ", "f "))]:
            fails.append(tag + ": positions, normals or faces changed")
        plan_d = json.load(open(plan, encoding="utf-8"))
        for p in plan_d["pieces"]:
            again = fit_piece(groups2[p["key"]], vts2, [(x, y) for x, y, *_ in p["points"]])
            if again is None or again[0]["flipped"] or max(abs(s) for s in again[0]["shiftMm"]) > 0.01:
                fails.append("%s %s: rewritten UVs are not the plan's own frame" % (tag, p["key"]))
    # a broken input is refused: a plan naming a piece the OBJ lacks
    tag, obj, plan, _ = SELFTEST[0]
    bad_plan = os.path.join(OUT_ROOT, "selftest", "bad_plan.json")
    d = json.load(open(plan, encoding="utf-8"))
    d["pieces"].append(dict(d["pieces"][0], key="pocketX"))
    json.dump(d, open(bad_plan, "w", encoding="utf-8"))
    rep = convert(obj, bad_plan, OUT_ROOT + "/selftest/bad", name="bad")
    if rep["ok"] or rep["checks"]["missingPieces"] != ["pocketX"]:
        fails.append("a missing piece was not refused")
    # outputs refused outside the game-inputs folder
    try:
        convert(obj, plan, "C:/Users/Public/kiln_to_game_should_not_exist")
        fails.append("an output outside %s was allowed" % OUT_ROOT)
    except AssertionError:
        pass
    print("SELFTEST", "PASS" if not fails else "FAIL " + "; ".join(fails))
    return 0 if not fails else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[:1] == ["--selftest"]:
        sys.exit(selftest())
    if len(a) < 3:
        print(__doc__)
        sys.exit(2)
    opt = lambda n, d, f=str: f(a[a.index(n) + 1]) if n in a else d  # noqa: E731
    r = convert(a[0], a[1], a[2], name=opt("--name", None), body_name=opt("--body-name", "KilnBody_LOD0"),
                tol=opt("--tol", 0.05, float), scale_tol=opt("--scale-tol", 0.005, float))
    print("KILN_TO_GAME", json.dumps({"ok": r["ok"], **r["checks"], "out": r["out"]}))
    sys.exit(0 if r["ok"] else 1)
