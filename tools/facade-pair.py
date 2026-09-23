#!/usr/bin/env python3
"""One bay of a facade in Unreal beside its dimensioned drawing, and every drawn edge measured on the frame.

    python tools/facade-pair.py --block east_parade --bay 0 --frame FRAME.png \
        --width-m 7.0 --centre-z-m 4.6 --out PAIR.png
    python tools/facade-pair.py --selftest

WHY IT EXISTS, 24 September. The measurement sitting accepts a facade on a
pair, and Jafar's acceptance rule for it is "every drawn dimension within 5 cm,
measured, not eyeballed". tools/hook-pair.py pairs a perspective frame with a
painted sheet, which has no scale; this pairs an ORTHOGRAPHIC frame, which has
one, with a drawing, which has one, so each can be read in metres.

THE FRAME'S SCALE IS STATED, NOT FOUND: the Unreal elevation shot is square to
the frontage with a known orthographic width (--width-m) centred on the bay at
a known height (--centre-z-m), so a metre is frame-width / width-m pixels and
the bay's centre is the frame's centre. Seen from the street, as the drawing is:
the east side runs right to left.

THE MEASURING. Each vertical edge of the bay's ground-floor chain, and each
level, is looked for on the frame within 20 cm of where the drawing puts it:
the strongest change of brightness across the edge, averaged along the part of
the edge the drawing says is there. The offset is reported in millimetres and
the edge passes at 50 mm or under. Edges the frame shows no change at are
reported as NOT-FOUND, never as passes.

WRITES the pair (drawing above, frame below with the drawn edges laid over it
in cyan, red where an edge failed) and prints one facadePair line.
"""
import importlib.util
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOLERANCE_MM = 50.0
SEARCH_M = 0.20


def _drawing_module():
    spec = importlib.util.spec_from_file_location("facade_drawing", os.path.join(ROOT, "tools", "facade-drawing.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def frame_px(d, bay, width_m, centre_z, fw, fh, x, z):
    """Block-local metres to pixels on the orthographic frame of one bay."""
    s = fw / width_m
    xc = (bay + 0.5) * d["bay_width_m"]
    sign = -1.0 if d["mirror"] else 1.0
    return (fw / 2.0 + sign * (x - xc) * s, fh / 2.0 - (z - centre_z) * s)


def bay_edges(fd, d, bay):
    """The bay's ground-floor x edges, each with the z span it runs over, and its levels."""
    ids = ("pilaster", "shop_door_leaf", "side_door_leaf", "display_glazing", "gf_pier", "front_door")
    xs = {}
    for p in d["parts"]:
        base = p["id"].rsplit("_bay", 1)[0]
        if not p["id"].endswith("_bay%d" % bay) or not base.startswith(ids):
            continue
        for x in p["x"]:
            lo, hi = xs.get(round(x, 3), (p["z"][0], p["z"][1]))
            xs[round(x, 3)] = (min(lo, p["z"][0]), max(hi, p["z"][1]))
    return sorted(xs.items()), d["z_levels"]


def measure(gray, d, bay, width_m, centre_z, x_edges, levels):
    """Offsets in mm between each drawn edge and the strongest edge the frame shows near it."""
    import numpy as np
    fh, fw = gray.shape
    s = fw / width_m
    win = int(round(SEARCH_M * s))
    gx = np.abs(np.diff(gray, axis=1))
    gz = np.abs(np.diff(gray, axis=0))
    out = []
    for x, (z0, z1) in x_edges:
        px, top = frame_px(d, bay, width_m, centre_z, fw, fh, x, z1)
        _, bot = frame_px(d, bay, width_m, centre_z, fw, fh, x, z0)
        r0, r1 = int(max(0, min(top, bot) + 2)), int(min(fh - 1, max(top, bot) - 2))
        c0, c1 = int(px) - win, int(px) + win
        if r1 - r0 < 4 or c0 < 0 or c1 >= fw - 1:
            out.append(("x", x, None)); continue
        prof = gx[r0:r1, c0:c1].mean(axis=0)
        if prof.max() < 4.0:
            out.append(("x", x, None)); continue
        k = int(prof.argmax())
        out.append(("x", x, abs((c0 + k + 0.5) - px) / s * 1000.0))
    for z in levels:
        _, pz = frame_px(d, bay, width_m, centre_z, fw, fh, 0.0, z)
        a, _ = frame_px(d, bay, width_m, centre_z, fw, fh, bay * d["bay_width_m"] + 0.2, z)
        b, _ = frame_px(d, bay, width_m, centre_z, fw, fh, (bay + 1) * d["bay_width_m"] - 0.2, z)
        c0, c1 = int(max(0, min(a, b))), int(min(fw - 1, max(a, b)))
        r0, r1 = int(pz) - win, int(pz) + win
        if r0 < 0 or r1 >= fh - 1 or c1 - c0 < 4:
            out.append(("z", z, None)); continue
        prof = gz[r0:r1, c0:c1].mean(axis=1)
        if prof.max() < 4.0:
            out.append(("z", z, None)); continue
        k = int(prof.argmax())
        out.append(("z", z, abs((r0 + k + 0.5) - pz) / s * 1000.0))
    return out


def pair(block, bay, frame_path, width_m, centre_z, out_png, plan_text=None, fd=None, scene=None):
    import numpy as np
    from PIL import Image, ImageDraw
    fd = fd or _drawing_module()
    scene = scene or json.load(open(fd.SCENE, encoding="utf-8"))
    d = fd.plan_drawing(block, plan_text if plan_text is not None else fd.run_plan(block), scene)
    frame = Image.open(frame_path).convert("RGB")
    fw, fh = frame.size
    x_edges, levels = bay_edges(fd, d, bay)
    res = measure(np.asarray(frame.convert("L")).astype(float), d, bay, width_m, centre_z, x_edges, levels)
    # The drawing, cut to the same window in metres and scaled to the frame.
    tmp = os.path.splitext(out_png)[0] + "-drawing-full.png"
    fd.render(d, tmp)
    dr = Image.open(tmp).convert("RGB")
    os.remove(tmp)
    k = fw / width_m / d["px_per_m"]
    corners = [fd.to_px(d, (bay + 0.5) * d["bay_width_m"] + sx * width_m / 2.0, centre_z + sz * fh / fw * width_m / 2.0)
               for sx in (-1, 1) for sz in (-1, 1)]
    box = (min(c[0] for c in corners), min(c[1] for c in corners), max(c[0] for c in corners), max(c[1] for c in corners))
    dr = dr.crop(tuple(int(round(v)) for v in box)).resize((fw, fh))
    over = frame.copy()
    g = ImageDraw.Draw(over)
    bad = {("x", r[1]) for r in res if r[2] is not None and r[2] > TOLERANCE_MM}
    for x, (z0, z1) in x_edges:
        p0 = frame_px(d, bay, width_m, centre_z, fw, fh, x, z0); p1 = frame_px(d, bay, width_m, centre_z, fw, fh, x, z1)
        g.line([p0, p1], fill=(255, 40, 40) if ("x", x) in bad else (0, 230, 255), width=1)
    for z in levels:
        a = frame_px(d, bay, width_m, centre_z, fw, fh, bay * d["bay_width_m"], z)
        b = frame_px(d, bay, width_m, centre_z, fw, fh, (bay + 1) * d["bay_width_m"], z)
        g.line([a, b], fill=(0, 230, 255), width=1)
    o = Image.new("RGB", (fw, fh * 2 + 8), (18, 18, 20))
    o.paste(dr, (0, 0)); o.paste(over, (0, fh + 8))
    o.save(out_png)
    found = [r for r in res if r[2] is not None]
    passed = [r for r in found if r[2] <= TOLERANCE_MM]
    worst = max([r[2] for r in found] or [0.0])
    print("facadePair block=%s bay=%d edges=%d found=%d within50mm=%d worstMm=%.0f notFound=%d out=%s"
          % (block, bay, len(res), len(found), len(passed), worst, len(res) - len(found), out_png))
    for kind, v, off in res:
        print("  edge %s=%.3f offsetMm=%s" % (kind, v, "NOT-FOUND" if off is None else "%.0f" % off))
    return res


def selftest():
    """Pairs a drawing with itself, drawn as a frame would be: every edge must be found within tolerance."""
    import tempfile
    from PIL import Image
    fd = _drawing_module()
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("facade-pair selftest FAIL " + name)
    plan = ("tfBay widthM=6.000 eavesM=6.200 ridgeM=6.200 groundFloorM=3.400\n"
            "tfPart id=pilaster_left_bay0 material=frame_painted kind=box xM=0.000..0.350 yM=-0.1000..0.0000 zM=0.000..3.400 note=x\n"
            "tfPart id=pilaster_right_bay0 material=frame_painted kind=box xM=5.650..6.000 yM=-0.1000..0.0000 zM=0.000..3.400 note=x\n"
            "tfPart id=side_door_leaf_bay0 material=paint_door kind=box xM=0.386..1.152 yM=0.1200..0.1600 zM=0.000..1.981 note=x\n"
            "tfPart id=fascia_band_bay0 material=paint_fascia kind=box xM=0.000..6.000 yM=-0.1200..0.0000 zM=2.850..3.400 note=x\n"
            "tfPart id=wall_bay0 material=brick_red kind=box xM=0.000..6.000 yM=0.0000..0.2150 zM=3.400..6.200 note=x\n")
    scene = {"blocks": [{"id": "t", "side": "west", "bays": 1, "bay_width_m": 6.0, "roof": {"kind": "parapet"}}]}
    with tempfile.TemporaryDirectory() as tmp:
        d = fd.plan_drawing("t", plan, scene)
        full = os.path.join(tmp, "full.png")
        fd.render(d, full)
        width_m, cz, fw, fh = 7.0, 3.1, 1280, 720
        im = Image.open(full)
        k = fw / width_m / d["px_per_m"]
        cx, cy = fd.to_px(d, 3.0, cz)
        big = im.resize((int(im.width * k), int(im.height * k)))
        frame = big.crop((int(cx * k - fw / 2), int(cy * k - fh / 2), int(cx * k + fw / 2), int(cy * k + fh / 2)))
        fp = os.path.join(tmp, "frame.png")
        frame.save(fp)
        res = pair("t", 0, fp, width_m, cz, os.path.join(tmp, "pair.png"), plan_text=plan, fd=fd, scene=scene)
        found = [r for r in res if r[2] is not None]
        check("edges found on a frame that is the drawing", len(found) >= 5)
        check("all found edges within 50 mm", all(r[2] <= TOLERANCE_MM for r in found))
        shifted = Image.new("RGB", frame.size, (250, 248, 242))
        shifted.paste(frame, (int(round(0.12 * fw / width_m)), 0))
        sp2 = os.path.join(tmp, "shifted.png")
        shifted.save(sp2)
        res2 = pair("t", 0, sp2, width_m, cz, os.path.join(tmp, "pair2.png"), plan_text=plan, fd=fd, scene=scene)
        xs = [r for r in res2 if r[0] == "x" and r[2] is not None]
        check("a 120 mm shift is caught as a failure", any(r[2] > TOLERANCE_MM for r in xs))
    print("facade-pair selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


def main(argv):
    if "--selftest" in argv:
        return selftest()

    def arg(name, default=None):
        return argv[argv.index(name) + 1] if name in argv else default
    return 0 if pair(arg("--block", "east_parade"), int(arg("--bay", "0")), arg("--frame"),
                     float(arg("--width-m", "7.0")), float(arg("--centre-z-m", "3.1")),
                     arg("--out", "facade-pair.png")) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
