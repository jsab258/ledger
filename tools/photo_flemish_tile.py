#!/usr/bin/env python3
"""A FLEMISH-BOND TILE BUILT FROM PHOTOGRAPHED BRICKS: REAL BRICKS CUT FROM A CC0 SCAN INTO THE DRAWN BOND.

    python tools/photo_flemish_tile.py --donor F:/LedgerTools/game-inputs/polyhaven/brick_wall_006 \
        --out F:/LedgerTools/game-inputs/brick-flemish-photo-n16-4 [--seed 7] [--px 2048]
    python tools/photo_flemish_tile.py --selftest

WHY, 16 November 2026 (order item n16-4; brick, a genuinely different method, try 1 of it): the drawn tile
(tools/flemish_tile.py) passed its twelve measured checks and still read newly built near the camera: offline
measures cannot see a CG surface. The professional route found (N16-4-PHOTO-BRICK-READING-2026-11-16.md, Q2:
photographed or scanned bricks arranged as instances into a layout that tiles, mortar handled apart, colour
variation layered on) keeps real worn faces. No CC0 Flemish scan exists in the allowed libraries, so the bond comes
from flemish_tile.layout() (true sizes, 85 mm courses) and each brick's face, chips and relief come from a real
brick in the donor scan (Poly Haven brick_wall_006, CC0, 3 m wide, English-like bond with separable bricks; measured, its bricks read about 1.25 times true size at the stated 3 m, so the kinds are told by their sizes on that scale: headers 100-155 mm, stretchers 225-330 mm, courses 55-85 mm high).

METHOD. 1) Find the donor's bricks: mortar is lighter and greyer than brick, so a mask from a local-contrast
lightness and saturation test, opened and split into connected parts; each part's box, kept when its height is a
course's and its length a header's or a stretcher's. 2) For each brick of the bond, take a donor brick of the same
kind (header for header, stretcher for stretcher), never the same donor brick twice in a row, crop it with a
half-joint margin of its own mortar, resize to the cell (brick plus joint) and paste, in all three maps (diffuse,
normal, roughness), wrapping at the tile's edge. 3) Grade in linear light: each brick to its target colour from
flemish_tile's families and dark-header clusters, keeping half of its own tone difference from the donor's median
(the grade multiplies, so its stains and chips stay); the mortar to the target's warm grey. 4) The ids map is the
pasted donor masks, so flemish_tile.py --check measures the result unchanged.
"""
import argparse
import json
import os
import sys

import numpy as np
from PIL import Image
from scipy import ndimage

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import flemish_tile as ft  # noqa: E402

DONOR_W_MM = 3000.0


def load(p, lin=False):
    a = np.asarray(Image.open(p).convert("RGB"), dtype=np.float64) / 255
    return ft.srgb_to_lin(a) if lin else a


def find_bricks(diff_srgb, mm_px):
    """Donor bricks as boxes (r0, r1, c0, c1, mask) from a lightness and saturation test against the local mean."""
    l = ft.lum(diff_srgb)
    mx, mn = diff_srgb.max(-1), diff_srgb.min(-1)
    sat = (mx - mn) / np.maximum(mx, 1e-4)
    loc_l = ndimage.uniform_filter(l, int(120 / mm_px))
    loc_s = ndimage.uniform_filter(sat, int(120 / mm_px))
    mortar = (l > loc_l * 1.06) & (sat < loc_s * 0.92)
    mortar = ndimage.binary_closing(mortar, iterations=1)
    brick = ~mortar
    brick = ndimage.binary_fill_holes(ndimage.binary_opening(brick, iterations=2))
    lab, n = ndimage.label(brick)
    out = []
    for i, sl in enumerate(ndimage.find_objects(lab)):
        if sl is None:
            continue
        h, w = (sl[0].stop - sl[0].start) * mm_px, (sl[1].stop - sl[1].start) * mm_px
        m = lab[sl] == i + 1
        fill = m.mean()
        # a merged pair shows as a column of the box with little brick in it (a perpend)
        colfill = m.mean(0)
        mid = colfill[len(colfill) // 5: len(colfill) - len(colfill) // 5]
        if not (55 <= h <= 85) or fill < 0.8 or (mid.size and mid.min() < 0.55):
            continue
        kind = "H" if 100 <= w <= 155 else ("S" if 225 <= w <= 330 else None)
        if kind:
            out.append((sl[0].start, sl[0].stop, sl[1].start, sl[1].stop, kind, m))
    return out, mortar


def build(donor_dir, px=2048, seed=7):
    rng = np.random.default_rng(seed)
    name = os.path.basename(os.path.normpath(donor_dir))
    d_srgb = load(os.path.join(donor_dir, name + "_diff_2k.jpg"))
    d_lin = ft.srgb_to_lin(d_srgb)
    d_nor = load(os.path.join(donor_dir, name + "_nor_dx_2k.jpg"))
    d_rgh = load(os.path.join(donor_dir, name + "_rough_2k.jpg"))[..., 0]
    dmm = DONOR_W_MM / d_srgb.shape[1]
    donors, dmortar = find_bricks(d_srgb, dmm)
    pools = {k: [b for b in donors if b[4] == k] for k in "SH"}
    if min(len(pools["S"]), len(pools["H"])) < 12:
        raise SystemExit("photoFlemish too few donor bricks: S=%d H=%d" % (len(pools["S"]), len(pools["H"])))
    # targets per brick from the drawn tile's own colour and dark-header logic (same seed, same layout)
    ref = ft.draw(px, seed)
    bricks, kinds, dark, mm = ref["bricks"], ref["kinds"], ref["dark"], ref["mm"]
    n = len(bricks)
    tgt = np.stack([np.bincount(ref["ids"][ref["ids"] >= 0], ref["albedo"][..., k][ref["ids"] >= 0], minlength=n)
                    for k in range(3)], 1) / np.maximum(np.bincount(ref["ids"][ref["ids"] >= 0], minlength=n), 1)[:, None]
    dmed = np.median([ft.lum(d_lin[b[0]:b[1], b[2]:b[3]][b[5]].mean(0)) for b in donors])
    alb = np.zeros((px, px, 3))
    nor = np.zeros((px, px, 3))
    rgh = np.zeros((px, px))
    ids = np.full((px, px), -1, np.int32)
    jpx_d = ft.JOINT_MM / 2 / dmm
    last = {"S": -1, "H": -1}
    used = []
    for i, (x0, x1, y0, y1, k, c, j) in enumerate(bricks):
        pool = pools[k]
        pick = int(rng.integers(len(pool)))
        if pick == last[k]:
            pick = (pick + 1) % len(pool)
        last[k] = pick
        used.append((k, pick))
        r0, r1, c0, c1, _, m = pool[pick]
        # crop the brick with a half joint of its own mortar round it
        R0, R1 = int(max(r0 - jpx_d, 0)), int(min(r1 + jpx_d, d_srgb.shape[0]))
        C0, C1 = int(max(c0 - jpx_d, 0)), int(min(c1 + jpx_d, d_srgb.shape[1]))
        mask = np.zeros((R1 - R0, C1 - C0), bool)
        mask[r0 - R0:r1 - R0, c0 - C0:c1 - C0] = m
        # the cell in the tile: the brick plus a half joint each side
        a, b = int(round((x0 - ft.JOINT_MM / 2) / mm)), int(round((x1 + ft.JOINT_MM / 2) / mm))
        t0, t1 = int(round((y0 - ft.JOINT_MM / 2) / mm)), int(round((y1 + ft.JOINT_MM / 2) / mm))
        size = (b - a, t1 - t0)

        def rs(arr, resample=Image.BILINEAR):
            if arr.ndim == 2:
                return np.asarray(Image.fromarray(arr.astype(np.float32), "F").resize(size, resample), np.float64)
            return np.stack([rs(arr[..., q]) for q in range(arr.shape[2])], -1)

        cl = rs(d_lin[R0:R1, C0:C1])
        cn = rs(d_nor[R0:R1, C0:C1])
        cr = rs(d_rgh[R0:R1, C0:C1])
        cm = rs(mask.astype(np.float64), Image.NEAREST) > 0.5
        # grade the brick part to its target, keeping half its own tone difference from the donor median
        own = cl[cm].mean(0) if cm.any() else cl.reshape(-1, 3).mean(0)
        keep = (ft.lum(own) / dmed) ** 0.5
        gain = tgt[i] * keep / np.maximum(own, 1e-4)
        cl = np.where(cm[..., None], cl * gain, cl)
        rows = np.arange(t0, t1) % px
        cols = np.arange(a, b) % px
        alb[np.ix_(rows, cols)] = cl
        nor[np.ix_(rows, cols)] = cn
        rgh[np.ix_(rows, cols)] = cr
        sub = ids[np.ix_(rows, cols)]
        sub[cm] = i
        sub[~cm] = -1
        ids[np.ix_(rows, cols)] = sub
    # mortar to the target's warm grey, keeping its own variation (ratio to its mean)
    mm_mask = ids < 0
    mort = alb[mm_mask]
    mlin = ft.srgb_to_lin(ft.MORTAR_SRGB)
    alb[mm_mask] = mort / np.maximum(mort.mean(0), 1e-4) * mlin * 0.9
    return dict(albedo=np.clip(alb, 0, 1), normal=nor, rough=np.clip(rgh, 0, 1), ids=ids, bricks=bricks, dark=dark,
                kinds=kinds, mm=mm, donors=dict(S=len(pools["S"]), H=len(pools["H"])), used=used)


def write(out, d, seed, donor_dir):
    os.makedirs(out, exist_ok=True)
    Image.fromarray((ft.lin_to_srgb(d["albedo"]) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_diff.png"))
    Image.fromarray((np.clip(d["normal"], 0, 1) * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_nor_dx.png"))
    Image.fromarray((d["rough"] * 255 + 0.5).astype(np.uint8)).save(os.path.join(out, "flemish_rough.png"))
    hdr = np.zeros(d["ids"].shape, np.uint8)
    m = d["ids"] >= 0
    hdr[m] = np.where(d["kinds"][d["ids"][m]] == "H", 128, 64) + np.where(d["dark"][d["ids"][m]], 127, 0)
    Image.fromarray(hdr).save(os.path.join(out, "flemish_headers.png"))
    np.save(os.path.join(out, "flemish_ids.npy"), d["ids"])
    b = d["bricks"]
    meta = dict(seed=seed, px=int(d["ids"].shape[0]), covers_m=round(ft.TILE_MM / 1000, 4), pitch_mm=ft.PITCH_MM,
                joint_mm=ft.JOINT_MM, stretcher_unit_mm=round(ft.UNIT_MM, 2), header_mm=round(ft.HEADER_MM, 2),
                kinds=d["kinds"].tolist(), dark=d["dark"].astype(int).tolist(),
                centres_mm=[[round((x[0] + x[1]) / 2 % ft.TILE_MM, 1), round((x[2] + x[3]) / 2, 1)] for x in b],
                course=[x[5] for x in b], along=[x[6] for x in b], donor=donor_dir.replace("\\", "/"),
                donor_bricks=d["donors"], method="photographed bricks cut into the drawn bond (photo_flemish_tile.py)")
    json.dump(meta, open(os.path.join(out, "flemish_meta.json"), "w"))


def selftest():
    # find_bricks on a drawn wall of known bricks: grey joints, red bricks; must find most of them by kind
    rng = np.random.default_rng(1)
    mm_px = 1.5
    img = np.ones((600, 900, 3)) * np.array([0.62, 0.58, 0.52])
    truth = {"S": 0, "H": 0}
    for r in range(0, 600 - 60, 60):
        x = int(rng.integers(0, 20))
        while x < 900 - 200:
            w = 190 if rng.random() < 0.5 else 90
            img[r + 4:r + 56, x + 4:x + w - 4] = np.array([0.55, 0.22, 0.14]) * (0.9 + 0.2 * rng.random())
            truth["S" if w == 190 else "H"] += 1
            x += w
    found, _ = find_bricks(img, mm_px)
    got = {k: sum(1 for f in found if f[4] == k) for k in "SH"}
    ok = got["S"] >= 0.8 * truth["S"] and got["H"] >= 0.8 * truth["H"]
    print("photo_flemish_tile selftest: %s (found %s of %s)" % ("passed" if ok else "FAILED", got, truth))
    return 0 if ok else 1


def main(a):
    ap = argparse.ArgumentParser()
    ap.add_argument("--donor")
    ap.add_argument("--out")
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--px", type=int, default=2048)
    ap.add_argument("--selftest", action="store_true")
    o = ap.parse_args(a)
    if o.selftest:
        return selftest()
    if not (o.donor and o.out):
        ap.print_usage()
        return 2
    d = build(o.donor, o.px, o.seed)
    write(o.out, d, o.seed, o.donor)
    print("photoFlemish out=%s donors S=%d H=%d" % (o.out, d["donors"]["S"], d["donors"]["H"]))
    return ft.check(o.out)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
