#!/usr/bin/env python3
"""EACH BRICK OF A BRICK SCAN FOUND AND NAMED, SO THE MATERIAL CAN GIVE EVERY COPY OF THE TILE ITS OWN BRICKS' TONES.

    python tools/brick_ids.py [ASSET ...] [--out-root F:/LedgerTools/game-inputs] [--preview DIR]
    python tools/brick_ids.py --selftest

WHY, 3 November 2026 (the corner's step 6, production/art/corner/CORNER-PLAN-2026-11-02.md: brick that does not
repeat): the street's brick rows wear a Poly Haven scan tiled every 1.05 m (production/specs/ps5-corner.json,
"scanned", always on since 4 October), and on the hook frame's big end wall its darkest bricks come back as the same
rows a metre apart, up and along. The per-house offset and tint (terrace-front.py, step 2.4) move and colour a whole
house, not the copies of the tile inside one wall. The brick research ranks a brick-ID channel second
(production/research/aaa-street/BRICK-2026-10-04.md, method 2, after O. Swierad's per-brick random values): the tile
stores a value per brick and the shader picks each brick's tone from it and from which copy of the tile it is in, so
no two copies agree and nothing moves (no seam, the bond and the scan's relief untouched).

WHAT IT WRITES, per scan (ps5-corner.json's "scanned" entries whose base is brick_*): <asset>_ids.png, RGBA, the
scan's own size and layout, read linear (not sRGB):
  R  the brick's random value, the same for every pixel of one brick, 0 on the mortar
  G  the brick's mean luminance over the median brick's, halved (1.0 is 0.5), 0 on the mortar
  B  which copy of the tile the brick's centre lies in, along u: 0 the one before, 0.5 this one, 1 the one after
  A  the same along v
B and A make a brick that crosses the tile's edge one brick: both its parts name the same copy, so they take one
tone. And <asset>_ids.json: the brick count, the share of mortar, and the bricks' tones at 5, 50 and 95% (the
material's range, so the re-toned wall keeps the scan's own spread). --preview writes a 3 by 3 copy of the tile
before and after, and prints how alike neighbouring copies are (1.0 before, by construction).

Mortar is told from brick by colour (the scans' brick is red, their mortar grey: red minus green, Otsu's threshold),
opened by 3 px so bricks that touch through a thin joint part; a brick is a connected region of 400 px or more
found on a 3 by 3 mosaic of the tile, so one that crosses an edge is found whole.
"""
import json
import os
import sys
import zlib

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(REPO, "production", "specs", "ps5-corner.json")
OUT_ROOT = "F:/LedgerTools/game-inputs"
MIN_BRICK_PX = 400
OPEN_PX = 3
#: HOW FAR ONE BRICK MAY BE MOVED (3 November, the grey scan's first preview: its near-black burnt bricks lifted to the
#: median came out an unnatural blue-grey): at most half again lighter or a third darker, so a burnt brick stays a dark
#: one and a pale one a pale one, only in other places; the material's own clamp (make_base_material.py) is the same
FACTOR_MIN, FACTOR_MAX = 0.67, 1.5


def _otsu(v):
    import numpy as np
    hist, edges = np.histogram(v, bins=256)
    mids = (edges[:-1] + edges[1:]) / 2.0
    w0 = np.cumsum(hist)
    w1 = w0[-1] - w0
    m0 = np.cumsum(hist * mids) / np.maximum(w0, 1)
    m1 = (np.sum(hist * mids) - np.cumsum(hist * mids)) / np.maximum(w1, 1)
    return float(mids[int(np.argmax(w0 * w1 * (m0 - m1) ** 2))])


#: HOW EACH SCAN'S MORTAR IS TOLD FROM ITS BRICK, read off the scans themselves (3 November): brick_4's mortar is pale
#: and grey, proud of the brick, so its shading map outlines the bricks and does not fill them, and colour does it;
#: brick_wall_001's mortar is a mid grey-brown, darker than its pale cracked faces, but recessed, so its shading map is
#: dark in every joint and colour is not (by colour it found 2 bricks).
MASK_BY = {"brick_4": "colour", "brick_wall_001": "ao"}


def ao_file(diff_rel):
    return diff_rel.replace("_diffuse_2k", "_ao_2k").replace("_diff_2k", "_ao_2k")


def brick_ids(rgb, ao=None):
    """rgb: H x W x 3 floats 0..1, a seamless tile; ao, its shading map (H x W), when the joints are to be told by it.
    Returns (ids H x W x 4 floats, info)."""
    import numpy as np
    from scipy import ndimage
    h, w = rgb.shape[:2]
    lum = rgb @ np.array([0.2126, 0.7152, 0.0722])
    if ao is not None:
        t = _otsu(ao)
        brick = ao > t
    else:
        chroma = rgb[..., 0] - rgb[..., 1]
        t = _otsu(chroma)
        # THE GREY BRICKS ARE BRICK TOO (the first map, 3 November: by colour alone the dark grey and blue-black
        # bricks, the very ones that repeat, read as mortar and were never re-toned): of the grey pixels, the dark are
        # brick and only the pale are mortar
        grey = chroma <= t
        t_lum = _otsu(lum[grey]) if grey.sum() > 100 else 0.0
        brick = (chroma > t) | (lum < t_lum)
    big = np.tile(brick, (3, 3))
    big = ndimage.binary_opening(big, structure=np.ones((OPEN_PX, OPEN_PX)))
    lab, n = ndimage.label(big)
    lum_big = np.tile(lum, (3, 3))
    idx = np.arange(1, n + 1)
    size = ndimage.sum(np.ones_like(lum_big), lab, idx)
    mean = ndimage.mean(lum_big, lab, idx)
    cy, cx = np.array(ndimage.center_of_mass(np.ones_like(lum_big), lab, idx)).T
    centre = lab[h:2 * h, w:2 * w]
    ok = np.zeros(n + 1, bool)
    ok[1:] = size >= MIN_BRICK_PX
    keep = ok[centre]
    k = centre - 1
    real = np.flatnonzero(ok[1:])
    # the median brick, counted once per brick: each whole brick has exactly one copy whose centre lies in the middle tile
    once = real[(cx[real] >= w) & (cx[real] < 2 * w) & (cy[real] >= h) & (cy[real] < 2 * h)]
    med = float(np.median(mean[once])) if len(once) else 1.0
    ratio = np.clip(mean / max(med, 1e-6), 0.25, 2.0)
    # one random value per physical brick: hashed from its centre's place in the tile, so both parts of an edge brick agree
    rnd = np.array([(zlib.crc32(("%d,%d" % (int(round(cx[i])) % w, int(round(cy[i])) % h)).encode()) % 65521) / 65520.0
                    for i in range(n)])
    out = np.zeros((h, w, 4))
    out[..., 2] = 0.5
    out[..., 3] = 0.5
    kk = k[keep]
    out[..., 0][keep] = np.maximum(rnd[kk], 1.0 / 255.0)
    out[..., 1][keep] = ratio[kk] / 2.0
    out[..., 2][keep] = (np.floor(cx[kk] / w) - 1 + 1) / 2.0
    out[..., 3][keep] = (np.floor(cy[kk] / h) - 1 + 1) / 2.0
    q = np.percentile(ratio[once], [5, 50, 95]) if len(once) else [1.0, 1.0, 1.0]
    # THE COMMON BRICK'S HUE: the mean colour of the middle half of the bricks by tone, over its own luminance
    rgb_big = np.tile(rgb, (3, 3, 1))
    mid = once[(ratio[once] >= np.percentile(ratio[once], 25)) & (ratio[once] <= np.percentile(ratio[once], 75))] if len(once) else once
    sel = np.isin(lab, mid + 1)
    mrgb = rgb_big[sel].mean(axis=0) if sel.any() else np.array([1.0, 1.0, 1.0])
    hue = mrgb / max(float(mrgb @ np.array([0.2126, 0.7152, 0.0722])), 1e-6)
    info = {"bricks": int(len(once)), "mortar_share": round(float(1.0 - keep.mean()), 3), "threshold": round(t, 4),
            "tone_q05_q50_q95": [round(float(v), 3) for v in q], "brick_hue": [round(float(v), 4) for v in hue]}
    return out, info


def retone(rgb, ids, cells_u, cells_v, q, amount=1.0, seed=0, hue=None):
    """What the material will do, in numpy: a cells_v x cells_u wall of copies of the tile, each brick's tone
    taken from the bricks' own spread by its random value and its copy's hash (amount 0: the plain tiling)."""
    import numpy as np
    h, w = rgb.shape[:2]
    rows = []
    for j in range(cells_v):
        row = []
        for i in range(cells_u):
            r, g = ids[..., 0], ids[..., 1]
            du = np.round(ids[..., 2] * 2 - 1)
            dv = np.round(ids[..., 3] * 2 - 1)
            cu, cv = i + du, j + dv
            hsh = np.modf(np.sin(cu * 12.9898 + cv * 78.233 + seed) * 43758.5453)[0] % 1.0
            rr = np.modf(r + hsh)[0] % 1.0
            tgt = np.where(rr < 0.5, q[0] + (q[1] - q[0]) * rr * 2, q[1] + (q[2] - q[1]) * (rr - 0.5) * 2)
            brick = np.clip(g * 20.0, 0, 1)
            f = 1.0 + (np.clip(tgt / np.maximum(g * 2.0, 1e-3), FACTOR_MIN, FACTOR_MAX) - 1.0) * amount * brick
            col = rgb * f[..., None]
            if hue is not None:
                # A LIFTED BRICK TAKES THE COMMON BRICK'S HUE as it is lifted (the grey scan's second preview: its
                # burnt bricks, lifted, showed the blue under the black): the share lifted, toward the median brick
                k = np.clip((f - 1.0) / (FACTOR_MAX - 1.0), 0, 1)[..., None]
                lum = (col @ np.array([0.2126, 0.7152, 0.0722]))[..., None]
                col = col + (lum * np.asarray(hue) - col) * k
            row.append(np.clip(col, 0, 1))
        rows.append(np.concatenate(row, axis=1))
    return np.concatenate(rows, axis=0)


def neighbour_alike(wall, h, w):
    """The mean correlation of luminance between each copy of the tile and the one to its right and the one above."""
    import numpy as np
    lum = wall @ np.array([0.2126, 0.7152, 0.0722])
    cv, cu = lum.shape[0] // h, lum.shape[1] // w
    cs = []
    for j in range(cv):
        for i in range(cu):
            a = lum[j * h:(j + 1) * h, i * w:(i + 1) * w].ravel()
            for (jj, ii) in ((j, i + 1), (j + 1, i)):
                if jj < cv and ii < cu:
                    b = lum[jj * h:(jj + 1) * h, ii * w:(ii + 1) * w].ravel()
                    cs.append(float(np.corrcoef(a, b)[0, 1]))
    return round(sum(cs) / len(cs), 3)


def scans(spec_path=SPEC):
    with open(spec_path, encoding="utf-8") as fh:
        return [s for s in json.load(fh).get("scanned", []) if str(s.get("base", "")).startswith("brick_")]


def run(assets, out_root, preview):
    import numpy as np
    from PIL import Image
    done = 0
    seen = set()
    for s in scans():
        # brick_4 is worn by two rows (brick_red and the rubbed arches): one map serves both
        if (assets and s["asset"] not in assets) or s["asset"] in seen:
            continue
        seen.add(s["asset"])
        diff = os.path.join(REPO, s["files"][0])
        rgb = np.asarray(Image.open(diff).convert("RGB"), dtype=float) / 255.0
        by = MASK_BY.get(s["asset"], "colour")
        ao = (np.asarray(Image.open(os.path.join(REPO, ao_file(s["files"][0]))).convert("L"), dtype=float) / 255.0
              if by == "ao" else None)
        ids, info = brick_ids(rgb, ao)
        info["mortar_by"] = by
        rel_dir = os.path.dirname(s["files"][0])
        dest = os.path.join(out_root, rel_dir)
        os.makedirs(dest, exist_ok=True)
        png = os.path.join(dest, s["asset"] + "_ids.png")
        Image.fromarray((np.clip(ids, 0, 1) * 255 + 0.5).astype(np.uint8), "RGBA").save(png)
        info.update({"asset": s["asset"], "base": s["base"], "from": s["files"][0], "covers_m": s.get("covers_m"),
                     "made_by": "tools/brick_ids.py", "channels": "R random, G tone over the median brick halved, "
                     "B and A the copy of the tile the brick's centre lies in (0, 0.5, 1), linear"})
        if preview:
            os.makedirs(preview, exist_ok=True)
            small = rgb[::4, ::4]
            ids_s = ids[::4, ::4]
            h, w = small.shape[:2]
            q = info["tone_q05_q50_q95"]
            before = retone(small, ids_s, 3, 3, q, amount=0.0)
            after = retone(small, ids_s, 3, 3, q, amount=1.0, hue=info["brick_hue"])
            info["neighbours_alike_before"] = neighbour_alike(before, h, w)
            info["neighbours_alike_after"] = neighbour_alike(after, h, w)
            for name, img in (("before", before), ("after", after)):
                Image.fromarray((img * 255 + 0.5).astype(np.uint8)).save(os.path.join(preview, "%s-%s.jpg" % (s["asset"], name)),
                                                                          quality=88)
        with open(os.path.join(dest, s["asset"] + "_ids.json"), "w", encoding="utf-8") as fh:
            json.dump(info, fh, indent=1)
        print("brickIds asset=%s bricks=%d mortar=%.3f tones=%s alike=%s->%s out=%s" % (
            s["asset"], info["bricks"], info["mortar_share"], info["tone_q05_q50_q95"],
            info.get("neighbours_alike_before"), info.get("neighbours_alike_after"), png))
        done += 1
    return 0 if done else 1


def selftest():
    """A seamless tile of four red bricks in grey mortar, one crossing the right edge into the left."""
    import numpy as np
    ok = []
    h, w = 64, 128
    rgb = np.full((h, w, 3), 0.55)
    bricks = {(0, 0): (4, 28, 4, 60, 0.30), (0, 1): (4, 28, 68, 124, 0.45),
              (1, 0): (36, 60, 36, 92, 0.60), (1, 1): (36, 60, 100, 156, 0.40)}   # the last crosses the right edge
    for (y0, y1, x0, x1, t) in bricks.values():
        for x in range(x0, x1):
            rgb[y0:y1, x % w] = (t, t * 0.4, t * 0.35)
    global MIN_BRICK_PX
    keep_min, MIN_BRICK_PX = MIN_BRICK_PX, 100
    try:
        ids, info = brick_ids(rgb)
    finally:
        MIN_BRICK_PX = keep_min
    ok.append(("four bricks found, the edge one once", info["bricks"] == 4))
    ok.append(("the mortar is zero in R and G", ids[1, 1, 0] == 0 and ids[1, 1, 1] == 0))
    a, b = ids[40, 120], ids[40, 10]    # both parts of the edge brick
    ok.append(("both parts of an edge brick share its random value", abs(a[0] - b[0]) < 1e-9 and a[0] > 0))
    ok.append(("its parts name copies one apart along u", abs((a[2] - b[2]) * 2 - 1) < 1e-9 or abs((b[2] - a[2]) * 2 - 1) < 1e-9))
    ok.append(("a brick inside the tile names this copy", ids[10, 30, 2] == 0.5 and ids[10, 30, 3] == 0.5))
    ok.append(("tones are relative to the median brick", abs(ids[10, 30, 1] * 2 - 0.30 / np.median([0.30, 0.45, 0.60, 0.40])) < 0.05))
    q = info["tone_q05_q50_q95"]
    plain = retone(rgb, ids, 2, 2, q, amount=0.0)
    ok.append(("amount 0 is the plain tiling", np.allclose(plain[:h, :w], rgb)))
    wall = retone(rgb, ids, 3, 1, q, amount=1.0)
    # the edge brick's left part at the end of copy 1 and its right part at the start of copy 2 are one brick
    left, right = wall[40, w + 120], wall[40, 2 * w + 10]
    ok.append(("an edge brick takes one tone across the copies' seam", np.allclose(left, right, atol=1e-6)))
    ok.append(("the mortar is never re-toned", np.allclose(wall[1, w + 1], rgb[1, 1])))
    ok.append(("the spec's brick rows wear two scans", sorted({s["asset"] for s in scans()}) == ["brick_4", "brick_wall_001"]))
    for name, good in ok:
        print("  %s %s" % ("ok  " if good else "FAIL", name))
    passed = sum(1 for _, g in ok if g)
    print("brick_ids selftest: passed=%d/%d failed=%d" % (passed, len(ok), len(ok) - passed))
    return 0 if passed == len(ok) else 1


if __name__ == "__main__":
    argv = sys.argv[1:]
    if "--selftest" in argv:
        sys.exit(selftest())
    out_root, preview, assets = OUT_ROOT, None, []
    i = 0
    while i < len(argv):
        if argv[i] == "--out-root":
            out_root = argv[i + 1]
            i += 2
        elif argv[i] == "--preview":
            preview = argv[i + 1]
            i += 2
        else:
            assets.append(argv[i])
            i += 1
    sys.exit(run(assets, out_root, preview))
