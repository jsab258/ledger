#!/usr/bin/env python3
"""PAINTED TIMBER, ONE SQUARE SEAMLESS TILE FOR THE STREET'S JOINERY ROWS (the corner's step 9a, 4 November 2026;
production/art/corner/STEP9-PLAN-2026-11-03.md, "9a"; production/research/street-wear/MAFIA-WEAR-2026-10-28.md section 1).

    python tools/art-recipes/paint_wood_tile.py              # writes the tile's three maps and its check line
    python tools/art-recipes/paint_wood_tile.py --selftest

WHY. The street's scan rows (production/specs/ps5-corner.json "scanned": a base material, three maps, covers_m and a
match_rgb grade) are how the game draws a photographed surface on a row's mesh, on the mesh's own first UV set, which is
metric (1.00 UV unit a metre). The joinery rows frame_painted and paint_fascia were given painted_concrete_02 on
4 October and put off again: it read as tarmac at 2 m and as render at 1 m. Mafia paints its joinery over wood from a
trim sheet (M_General_1_Layer_Paint_Chipped, Paint Roughness 0.32), so this tile is paint over wood: the grain a faint
ghost under a flat coat, a gloss paint's roughness, a broad dirt. The scan row has no field for detail contrast (the
binder in VignetteShot.cpp sets only the three maps, the tiling 1/covers_m and the grade vector, a multiply), so the
low contrast is made here, in the maps, not in the material.

SOURCE. tools/art-recipes/wood_trim.py's sheet: Poly Haven kitchen_wood (CC0 1.0, https://polyhaven.com/a/kitchen_wood),
the BOARDS strip (v 0 to 0.75) at 487.6 px/m. Its board mosaic (the same functions, before the sheet's lower strips
overwrite it) and its masks file (B, the broad dirt) are read; the boards strip of the saved sheet is compared with the
mosaic's as a check that the two are the same wood.

METHOD.
  1. The tile is the boards strip cut square: 1,536 px over 3.15 m (487.6 px a metre; the method's 512 within 20%,
     410 to 614), grain along u.
  2. SEAMLESS in both directions. The sheet is periodic only over its own 2,048 px (7 boards), not over 1,536 (5.25
     boards), so a plain cut shows a seam on both axes (measured and printed). The tile is made periodic by a cosine
     cross-blend of its first 384 px with the 384 px that follow its last (the sheet's own continuation, which the mosaic
     has in both axes), first across u, then across v: the tile's last column then continues into its first exactly. The
     blend zone has lower grain contrast than the rest (two unrelated woods averaged); with the grain this faint it does
     not read.
  3. COLOUR is paint over wood: a neutral grey at the mean given below, the wood's grain luminance kept at
     GRAIN_KEEP (0.20) of its own contrast, a broad dirt noise (the masks' B) at DIRT_AMOUNT (+-0.10), no wood hue.
     The row's match_rgb (palette colour over the tile's mean, linear, as the other rows) gives it the paint colour.
  4. NORMAL: the sheet's grain relief with its xy tilt turned down to NORMAL_KEEP (0.25), renormalised, DirectX (green
     down) as the other rows' nor_dx maps.
  5. ROUGHNESS (R, as the binder reads it): Mafia's Paint Roughness 0.32, the wood's own variation scaled to +-0.03 and
     the dirt adding up to +0.04 (dirty paint is a little duller); never the bare wood's 0.55 to 0.85.

CHECK (the run prints it; --selftest runs the same checks on a small tile without the sheet): density 410 to 614 px/m;
seam error (mean absolute step between the last and the first column or row, over the mean step between neighbours
inside the tile) at most 1.5 on both axes; contrast (std of luminance over its mean) 0.04 to 0.12, well under the bare
wood's; roughness mean 0.32 +-0.03; normal tilt mean under 0.05.

Files go to production/assets/scanned/polyhaven/paint_wood_01/ (the folder the attribution check already names as Poly
Haven's scans; the pictures are git-ignored, as the brick maps are) and under the same path in F:/LedgerTools/game-inputs.
"""
import json
import os
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import wood_trim as wt  # noqa: E402

ASSET = "paint_wood_01"
REL = "production/assets/scanned/polyhaven/" + ASSET
GAME_INPUTS = "F:/LedgerTools/game-inputs"
SHEET_DIR = os.path.join(REPO, wt.REL)
SIDE = 1536                       # px; 3.15 m at wt.DENSITY
COVERS_M = SIDE / wt.DENSITY      # 3.15 m
BLEND = 384                       # px of cross-blend on each axis
PALETTE = (0.0625, 0.0875, 0.119)  # frame_painted / fascia_slate_blue linear_rgb (quay-street.json), the rows' colour
GRAIN_KEEP = 0.20
DIRT_AMOUNT = 0.10
NORMAL_KEEP = 0.25
ROUGH_BASE = 0.32                 # Mafia's Paint Roughness
ROUGH_WOOD = 0.03
ROUGH_DIRT = 0.04
NAMES = {"colour": ASSET + "_diff.png", "normal": ASSET + "_nor_dx.png", "rough": ASSET + "_rough.png"}
LUMA = np.array([0.2126, 0.7152, 0.0722])


def boards_mosaic(source=wt.SOURCE):
    """The board mosaic exactly as wood_trim.build makes it before its strips are overwritten: linear colour, roughness,
    DirectX normal vectors, all 2,048 square and periodic in both axes."""
    from PIL import Image
    ld = lambda n, m: np.asarray(Image.open(os.path.join(source, n)).convert(m), dtype=np.float64) / 255.0
    diff = ld("kitchen_wood_diff_2k.jpg", "RGB")
    rough = ld("kitchen_wood_rough_2k.jpg", "L")
    nor = ld("kitchen_wood_nor_gl_2k.jpg", "RGB")
    diff, rough, nor = np.rot90(diff), np.rot90(rough), np.rot90(nor)
    nx, ny = nor[..., 0] * 2 - 1, nor[..., 1] * 2 - 1
    nor = np.stack([(-ny + 1) / 2, (nx + 1) / 2, nor[..., 2]], axis=2)
    big = wt.mosaic(np.concatenate([wt.srgb_to_linear(diff), rough[..., None], nor], axis=2))
    nrm = big[..., 4:7] * 2 - 1
    nrm[..., 1] = -nrm[..., 1]
    return big[..., 0:3], big[..., 3], nrm


def seamless(img, side, blend):
    """Cut img (n, n, c) to side by side and make it periodic by a cosine cross-blend of its first `blend` rows and
    columns with the `blend` that follow its last, along each axis in turn (needs side + blend <= n)."""
    out = img[: side + blend, : side + blend].astype(np.float64).copy()
    w = (0.5 - 0.5 * np.cos(np.pi * (np.arange(blend) + 0.5) / blend))     # 0 at the seam, 1 inside
    # u (axis 1): new[x] = w * src[x] + (1 - w) * src[side + x], so new[-1] (= src[side - 1]) runs on into new[0]
    wu = w[None, :, None]
    out[:, :blend] = wu * out[:, :blend] + (1 - wu) * out[:, side:side + blend]
    out = out[:, :side]
    wv = w[:, None, None]
    out[:blend] = wv * out[:blend] + (1 - wv) * out[side:side + blend]
    return out[:side]


def seam_error(img):
    """Mean step across the wrap (last to first column/row) over the mean step between neighbours, per axis."""
    def one(a):
        wrap = np.abs(a[:, 0] - a[:, -1]).mean()
        inside = np.abs(a[:, 1:] - a[:, :-1]).mean()
        return float(wrap / max(inside, 1e-9))
    return {"u": one(img), "v": one(np.swapaxes(img, 0, 1))}


def make(mosaic, dirt_full, side=SIDE, blend=BLEND, palette=PALETTE):
    """The tile's maps from the board mosaic (col lin, rough, normal) and the sheet's dirt noise, all square and
    periodic. Returns linear colour, roughness, normal vectors, and the raw cut (colour only) for the seam report."""
    col, rgh, nrm = mosaic
    n = col.shape[0]
    lum = col @ LUMA
    detail = lum / np.median(lum[:side, :side]) - 1.0
    stack = np.concatenate([detail[..., None], rgh[..., None], nrm, dirt_full[..., None]], axis=2)
    raw = stack[:side, :side, 0:1]
    t = seamless(stack, side, blend)
    d, r, nv, dirt = t[..., 0], t[..., 1], t[..., 2:5], t[..., 5]
    base = float(np.asarray(palette) @ LUMA)                     # a neutral grey of the paint's own luminance
    k = 1.0 + GRAIN_KEEP * d + DIRT_AMOUNT * 2.0 * (dirt - 0.5)
    lin = np.clip(base * k, 0, 1)[..., None] * np.ones(3)[None, None, :]
    lin *= base / lin.mean()                                      # mean exactly the base
    rr = r - np.median(r)
    rr = rr / max(np.abs(rr).max(), 1e-9)
    rough = np.clip(ROUGH_BASE + ROUGH_WOOD * rr + ROUGH_DIRT * dirt, 0.05, 0.95)
    nv = nv.copy()
    nv[..., 0:2] *= NORMAL_KEEP
    nv /= np.linalg.norm(nv, axis=2, keepdims=True)
    return lin, rough, nv, raw


def quantise(lin, rough, nv):
    col = (wt.linear_to_srgb(lin) * 255 + 0.5).astype(np.uint8)
    rg = (np.clip(rough, 0, 1) * 255 + 0.5).astype(np.uint8)
    nm = ((nv * 0.5 + 0.5).clip(0, 1) * 255 + 0.5).astype(np.uint8)
    return col, rg, nm


def numbers(col8, rg8, nm8, side, covers_m, palette=PALETTE):
    """The checks, on what is written (the 8-bit maps the game reads)."""
    lin = wt.srgb_to_linear(col8 / 255.0)
    lum = lin @ LUMA
    mean = lin.reshape(-1, 3).mean(0)
    nv = nm8 / 255.0 * 2 - 1
    tilt = float(np.sqrt(nv[..., 0] ** 2 + nv[..., 1] ** 2).mean())
    dens = side / covers_m
    n = {"px": side, "covers_m": round(covers_m, 4), "density_px_m": round(dens, 1),
         "density_ok": bool(410 <= dens <= 614),
         "mean_lin": [round(float(x), 5) for x in mean],
         "contrast": round(float(lum.std() / lum.mean()), 4),
         "rough_mean": round(float((rg8 / 255.0).mean()), 4), "rough_std": round(float((rg8 / 255.0).std()), 4),
         "normal_tilt_mean": round(tilt, 4),
         "seam_colour": {k: round(v, 3) for k, v in seam_error(lin).items()},
         "seam_normal": {k: round(v, 3) for k, v in seam_error(nv).items()},
         "match_rgb": [round(float(p / m), 4) for p, m in zip(palette, mean)]}
    n["ok"] = bool(n["density_ok"] and 0.04 <= n["contrast"] <= 0.12 and abs(n["rough_mean"] - ROUGH_BASE) <= 0.03
                   and n["normal_tilt_mean"] < 0.05 and max(n["seam_colour"].values()) <= 1.5
                   and max(n["seam_normal"].values()) <= 1.5)
    return n


def main():
    from PIL import Image
    mosaic = boards_mosaic()
    masks = np.asarray(Image.open(os.path.join(SHEET_DIR, wt.NAMES["masks"])), dtype=np.float64) / 255.0
    dirt_full = masks[..., 2]
    # the saved sheet's boards strip against the mosaic's: the same wood?
    sheet = wt.srgb_to_linear(np.asarray(Image.open(os.path.join(SHEET_DIR, wt.NAMES["colour"])).convert("RGB"), dtype=np.float64) / 255.0)
    rows = int(wt.BOARDS[1] * wt.PX)
    diff_sheet = float(np.abs(sheet[:rows] - mosaic[0][:rows]).mean())      # the sheet is 8-bit, so its max is a quantising step
    lin, rough, nv, raw = make(mosaic, dirt_full)
    col8, rg8, nm8 = quantise(lin, rough, nv)
    raw_seam = seam_error(wt.srgb_to_linear(np.asarray(Image.fromarray(
        (wt.linear_to_srgb(mosaic[0][:SIDE, :SIDE]) * 255 + 0.5).astype(np.uint8)))/ 255.0))
    n = numbers(col8.astype(np.float64), rg8.astype(np.float64), nm8.astype(np.float64), SIDE, COVERS_M)
    n["uncut_seam_colour"] = {k: round(v, 3) for k, v in raw_seam.items()}
    n["sheet_vs_mosaic_mean_diff"] = round(diff_sheet, 5)
    n["palette_lin"] = list(PALETTE)
    n["source"] = {"asset": "kitchen_wood", "page": "https://polyhaven.com/a/kitchen_wood", "licence": "CC0 1.0",
                   "via": "tools/art-recipes/wood_trim.py boards strip", "made": "2026-11-04"}
    dirs = [os.path.join(REPO, REL), os.path.join(GAME_INPUTS, REL)]
    for d in dirs:
        os.makedirs(d, exist_ok=True)
        Image.fromarray(col8).save(os.path.join(d, NAMES["colour"]))
        Image.fromarray(nm8).save(os.path.join(d, NAMES["normal"]))
        Image.fromarray(np.stack([rg8] * 3, axis=2)).save(os.path.join(d, NAMES["rough"]))
        json.dump(n, open(os.path.join(d, ASSET + ".json"), "w", encoding="utf-8"), indent=1)
    print("paintWoodTile=%s px=%d covers=%.2f m density=%.1f px/m (410 to 614) mean_lin=%s contrast=%.4f rough=%.3f tilt=%.4f "
          "seam colour u/v=%.3f/%.3f (uncut %.3f/%.3f) normal u/v=%.3f/%.3f sheet_diff_mean=%.5f match_rgb=%s out=%s" % (
              "OK" if n["ok"] and diff_sheet < 0.002 else "FAIL", SIDE, COVERS_M, n["density_px_m"], n["mean_lin"],
              n["contrast"], n["rough_mean"], n["normal_tilt_mean"], n["seam_colour"]["u"], n["seam_colour"]["v"],
              raw_seam["u"], raw_seam["v"], n["seam_normal"]["u"], n["seam_normal"]["v"], diff_sheet, n["match_rgb"],
              ",".join(dirs)))
    return 0 if n["ok"] and diff_sheet < 0.002 else 1


def selftest():
    """A small tile from a synthetic periodic 'wood' (no sheet needed): the same maths, the same checks."""
    ok = []
    n, side, blend = 128, 96, 24
    rng = np.random.default_rng(3)
    v = np.arange(n)[:, None] / n
    u = np.arange(n)[None, :] / n
    grain = 0.3 + 0.1 * np.sin(2 * np.pi * 7 * v) + 0.05 * np.sin(2 * np.pi * 3 * u + 4 * np.sin(2 * np.pi * v))
    col = np.clip(grain[..., None] * np.array([1.0, 0.7, 0.4]), 0, 1)
    rgh = 0.6 + 0.1 * np.sin(2 * np.pi * 5 * v) * np.ones((1, n))
    nrm = np.zeros((n, n, 3))
    nrm[..., 0] = 0.2 * np.sin(2 * np.pi * 7 * v)
    nrm[..., 1] = 0.1 * np.sin(2 * np.pi * 3 * u)
    nrm[..., 2] = np.sqrt(1 - nrm[..., 0] ** 2 - nrm[..., 1] ** 2)
    dirt = wt.band_noise(n, 40, 5)
    lin, rough, nv, raw = make((col, rgh, nrm), dirt, side=side, blend=blend)
    c8, r8, n8 = quantise(lin, rough, nv)
    num = numbers(c8.astype(np.float64), r8.astype(np.float64), n8.astype(np.float64), side, COVERS_M * side / SIDE)
    cut = seam_error(col[:side, :side])
    print("paint_wood_tile selftest: density=%.1f px/m mean_lin=%s contrast=%.4f rough=%.3f tilt=%.4f seam colour u/v=%.3f/%.3f "
          "(uncut %.3f/%.3f) match_rgb=%s" % (num["density_px_m"], num["mean_lin"], num["contrast"], num["rough_mean"],
                                              num["normal_tilt_mean"], num["seam_colour"]["u"], num["seam_colour"]["v"],
                                              cut["u"], cut["v"], num["match_rgb"]))
    ok.append(abs(num["density_px_m"] - wt.DENSITY) < 0.1 and num["density_ok"])
    ok.append(max(num["seam_colour"].values()) <= 1.5 and max(num["seam_normal"].values()) <= 1.5)
    ok.append(max(cut.values()) > max(num["seam_colour"].values()))              # the blend made the seam smaller
    ok.append(abs(num["rough_mean"] - ROUGH_BASE) <= 0.03)
    ok.append(num["normal_tilt_mean"] < 0.05)
    ok.append(0.0 < num["contrast"] < 0.2)
    ok.append(abs(sum(m * x for m, x in zip(num["match_rgb"], num["mean_lin"])) - sum(PALETTE)) < 0.002)
    print("paint_wood_tile selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
