#!/usr/bin/env python3
"""ONE WOOD TRIM SHEET FOR PAINTED JOINERY, BY SCRIPT FROM ONE CC0 BOARD (his order D11, the look; production/research/
street-wear/MAFIA-WEAR-2026-10-28.md, section 5, "One shop front: the chandler", S2 joinery).

    python tools/art-recipes/wood_trim.py              # writes the sheet's three maps and its check line
    python tools/art-recipes/wood_trim.py --selftest

WHY, 30 October 2026. Mafia paints its shutters, frames and doors with one master, M_General_1_Layer_Paint_Chipped
(48 instances), paint over wood from a trim sheet (27 of the 39 window-folder trim slots sit on its wood-elements sheet;
study section 2). Our joinery had no wood under its paint, so a chip could only show an undercoat colour baked into the
paint (tools/art-recipes/front_wear.py). This is the wood the chipped-paint layer shows (tools/ue/make_kit_materials.py
make_paint_wood_master), mapped by tools/art-recipes/front_joinery.py.

THE SOURCE: Poly Haven's "kitchen_wood" (https://polyhaven.com/a/kitchen_wood, CC0 1.0, polyhaven.com/license; a
planed pine board 0.60 by 0.60 m, read from its API's info on 30 October 2026), fetched by tools/art-recipes/
fetch_polyhaven.py --res 2k into F:/LedgerTools/polyhaven/kitchen_wood/2k: its colour, roughness and (OpenGL) normal.

THE SHEET: 2,048 px square, the board turned so its grain runs along the sheet's width and tiled 7 times across, so
the sheet is 4.2 m of wood a side at 487.6 px/m (the method's density check: 512 px/m within 20%, so 410 to 614).
It repeats seamlessly along its width (a strip may run past its end), in three strips:
  * BOARDS, the top three quarters (v 0 to 0.75, 3.15 m): wide faces (door leaves, pilasters, the cornice);
  * NARROW MEMBERS, the next eighth (v 0.75 to 0.875): the same board at another phase, mirrored, for small mouldings
    and beads, so they do not repeat the boards' figure;
  * END GRAIN, the last eighth (v 0.875 to 1): growth rings drawn by script (8 mm a ring, the late wood
    darker), for faces cut across the grain.
The masks map holds the bare wood's roughness (R; the board is varnished, so its roughness is remapped to a weathered
bare wood's 0.55 to 0.85), the chip noise (G; Mafia's "Paint Cracks Tiling" 3 is its tiling in the material) and a
broad dirt noise (B), both periodic over the sheet and spread evenly over 0 to 1, so a threshold of t keeps 1 - t.
"""
import json
import os
import shutil
import sys

import numpy as np

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SOURCE = "F:/LedgerTools/polyhaven/kitchen_wood/2k/textures"
SOURCE_M = 0.60                  # the board's own size, Poly Haven's info "dimensions" 600 by 600 mm
PX = 2048
TILES = 7
SHEET_M = SOURCE_M * TILES       # 4.2 m a side
DENSITY = PX / SHEET_M           # 487.6 px/m
#: the strips, as v ranges of the sheet (v down from its top, as glTF and Unreal read a picture)
BOARDS = (0.0, 0.75)
NARROW = (0.75, 0.875)
END = (0.875, 1.0)
REL = "production/assets/wood-trim"
GAME_INPUTS = "F:/LedgerTools/game-inputs"
NAMES = {"colour": "wood_trim_colour.png", "masks": "wood_trim_masks.png", "normal": "wood_trim_normal.png",
         "flat": "wood_trim_flatnormal.png"}


def srgb_to_linear(v):
    v = np.asarray(v, dtype=np.float64)
    return np.where(v <= 0.04045, v / 12.92, ((v + 0.055) / 1.055) ** 2.4)


def linear_to_srgb(v):
    v = np.clip(np.asarray(v, dtype=np.float64), 0.0, 1.0)
    return np.where(v <= 0.0031308, v * 12.92, 1.055 * v ** (1 / 2.4) - 0.055)


def periodic_resample(img, n):
    """An image that tiles, resampled to n by n by its Fourier series, so it still tiles exactly."""
    from scipy.signal import resample
    out = resample(img, n, axis=0)
    return resample(out, n, axis=1)


def mosaic(tile, tiles=TILES, px=PX):
    """The tile (seamless, grain along its width already) repeated tiles by tiles and brought to px square."""
    from PIL import Image
    side = -(-px // tiles)       # 293 px a tile, so the mosaic is 2,051 and comes down to 2,048
    chans = []
    for c in range(tile.shape[2]):
        t = np.asarray(Image.fromarray(tile[..., c].astype(np.float32), mode="F").resize((side, side), Image.LANCZOS))
        chans.append(periodic_resample(np.tile(t, (tiles, tiles)), px))
    return np.stack(chans, axis=2)


def band_noise(px, wavelength_px, seed, octaves=((1.0, 1.0), (0.35, 0.4))):
    """Periodic noise over px square: white noise filtered round a wavelength (and finer octaves), spread evenly over 0
    to 1 by rank, so it tiles and a threshold t keeps 1 - t of it."""
    rng = np.random.default_rng(seed)
    f = np.fft.fftfreq(px)
    fr = np.sqrt(f[:, None] ** 2 + f[None, :] ** 2)
    acc = np.zeros((px, px))
    for scale, weight in octaves:
        w = np.fft.fft2(rng.standard_normal((px, px)))
        f0 = 1.0 / (wavelength_px * scale)
        acc += weight * np.real(np.fft.ifft2(w * np.exp(-((fr - f0) / (0.6 * f0)) ** 2)))
    rank = np.argsort(np.argsort(acc.ravel()))
    return (rank / (rank.size - 1.0)).reshape(px, px)


def end_grain(rows, px, mean_lin, seed=7):
    """Growth rings across a board cut far from its pith: nearly straight arcs along the width, wavy, periodic in it;
    the late wood 0.7 of the early's brightness, the whole a shade darker than the side grain (end grain drinks dirt). At 487.6 px/m a pixel is 2 mm, so rings are drawn at 8 mm (a fast-grown deal's; finer would
    alias), soft. Returns linear colour (rows, px, 3), roughness and a height for the normal."""
    rng = np.random.default_rng(seed)
    u = np.arange(px) / px
    v = np.arange(rows)[:, None] / DENSITY                              # metres down the strip
    wave = sum(a * np.sin(2 * np.pi * (k * u + rng.random())) for k, a in ((1, 0.012), (2, 0.006), (5, 0.002)))
    r = v + wave[None, :]                                               # metres across the rings
    ring_m = 0.008
    phase = r / ring_m + 0.15 * band_noise(px, 160, seed + 1)[:rows, :]
    frac = phase - np.floor(phase)
    late = 0.5 - 0.5 * np.cos(2 * np.pi * np.clip((frac - 0.55) / 0.45, 0, 1))
    pores = band_noise(px, 6, seed + 2)[:rows, :]
    bright = (1.0 - 0.30 * late) * (0.94 + 0.12 * pores) * 0.85
    colour = np.asarray(mean_lin)[None, None, :] * bright[..., None]
    rough = 0.82 + 0.06 * late
    return colour, rough, late


def normal_from_height(h, strength):
    """A DirectX (Unreal) normal map from a height, periodic differences."""
    gx = (np.roll(h, -1, axis=1) - np.roll(h, 1, axis=1)) * strength
    gy = (np.roll(h, -1, axis=0) - np.roll(h, 1, axis=0)) * strength
    n = np.stack([-gx, gy, np.ones_like(h)], axis=2)
    return n / np.linalg.norm(n, axis=2, keepdims=True)


def build(source=SOURCE):
    from PIL import Image
    diff = np.asarray(Image.open(os.path.join(source, "kitchen_wood_diff_2k.jpg")).convert("RGB"), dtype=np.float64) / 255.0
    rough = np.asarray(Image.open(os.path.join(source, "kitchen_wood_rough_2k.jpg")).convert("L"), dtype=np.float64) / 255.0
    nor = np.asarray(Image.open(os.path.join(source, "kitchen_wood_nor_gl_2k.jpg")).convert("RGB"), dtype=np.float64) / 255.0
    # the grain runs down the source picture; turned a quarter so it runs along the sheet's width (u)
    diff, rough, nor = np.rot90(diff), np.rot90(rough), np.rot90(nor)
    # a quarter turn of a normal map turns its vectors too: (x, y) -> (-y, x) in the picture's axes; and OpenGL's green
    # (y up) becomes DirectX's (y down) after
    nx, ny = nor[..., 0] * 2 - 1, nor[..., 1] * 2 - 1
    nor = np.stack([(-ny + 1) / 2, (nx + 1) / 2, nor[..., 2]], axis=2)
    lin = srgb_to_linear(diff)
    big = mosaic(np.concatenate([lin, rough[..., None], nor], axis=2))
    col, rgh, nrm = big[..., 0:3], big[..., 3], big[..., 4:7] * 2 - 1
    nrm[..., 1] = -nrm[..., 1]                                          # OpenGL to DirectX
    # THE NARROW MEMBERS' STRIP: the same wood at another phase (a third of a tile down), mirrored along its width
    a, b = int(NARROW[0] * PX), int(NARROW[1] * PX)
    shift = int(PX / TILES / 3)
    for arr in (col, rgh, nrm):
        arr[a:b] = np.roll(arr, -shift, axis=0)[a:b][:, ::-1]
    nrm[a:b, :, 0] *= -1                                                # mirrored in u, so its x turns
    # THE END GRAIN
    c, d = int(END[0] * PX), PX
    mean = np.median(col[: int(BOARDS[1] * PX)].reshape(-1, 3), axis=0)
    ecol, erough, eh = end_grain(d - c, PX, mean)
    col[c:d], rgh[c:d] = ecol, erough
    nrm[c:d] = normal_from_height(eh, 0.6)
    # bare weathered wood, not varnish: the board's roughness 0.40 to 0.78 remapped to 0.55 to 0.85 (the end kept)
    rgh[:c] = np.clip(0.55 + (rgh[:c] - 0.40) * (0.30 / 0.38), 0.5, 0.9)
    nrm /= np.linalg.norm(nrm, axis=2, keepdims=True)
    # flakes about 2 to 3 cm across at the material's tiling of 3 (a 4.4 cm wavelength), their edges ragged by two finer octaves
    chip = band_noise(PX, 64, 11, octaves=((1.0, 1.0), (0.35, 0.35), (0.12, 0.15)))
    dirt = band_noise(PX, 420, 13, octaves=((1.0, 1.0), (0.4, 0.5)))
    return {"colour": np.clip(col, 0, 1), "rough": rgh, "normal": nrm, "chip": chip, "dirt": dirt}


def numbers(maps):
    """The sheet's own checks: its density and its albedo (C6: 0.03 to 0.88; wood's median 0.09 to 0.36), each strip."""
    lum = maps["colour"] @ np.array([0.2126, 0.7152, 0.0722])
    out = {"px": PX, "sheet_m": SHEET_M, "density_px_m": round(DENSITY, 1), "density_ok": bool(abs(DENSITY / 512.0 - 1) <= 0.2)}
    for name, (v0, v1) in (("boards", BOARDS), ("narrow", NARROW), ("end", END)):
        s = lum[int(v0 * PX):int(v1 * PX)]
        out[name] = {"lum_p2": round(float(np.percentile(s, 2)), 4), "lum_median": round(float(np.median(s)), 4),
                     "lum_p98": round(float(np.percentile(s, 98)), 4),
                     "rough_median": round(float(np.median(maps["rough"][int(v0 * PX):int(v1 * PX)])), 3)}
        out[name]["ok"] = bool(0.03 <= out[name]["lum_p2"] and out[name]["lum_p98"] <= 0.88 and 0.09 <= out[name]["lum_median"] <= 0.36)
    # the seam along the width: the last column against the first, as against its neighbour
    c = maps["colour"]
    out["seam_step"] = round(float(np.abs(c[:, -1] - c[:, 0]).mean()), 4)
    out["neighbour_step"] = round(float(np.abs(c[:, 1] - c[:, 0]).mean()), 4)
    out["ok"] = bool(out["density_ok"] and all(out[k]["ok"] for k in ("boards", "narrow", "end"))
                     and out["seam_step"] <= 2.0 * out["neighbour_step"] + 1e-3)
    return out


def write(maps, out_dirs):
    from PIL import Image
    col = (linear_to_srgb(maps["colour"]) * 255 + 0.5).astype(np.uint8)
    masks = (np.stack([maps["rough"], maps["chip"], maps["dirt"]], axis=2).clip(0, 1) * 255 + 0.5).astype(np.uint8)
    nrm = ((maps["normal"] * 0.5 + 0.5).clip(0, 1) * 255 + 0.5).astype(np.uint8)
    for d in out_dirs:
        os.makedirs(d, exist_ok=True)
        Image.fromarray(col).save(os.path.join(d, NAMES["colour"]))
        Image.fromarray(masks).save(os.path.join(d, NAMES["masks"]))
        Image.fromarray(nrm).save(os.path.join(d, NAMES["normal"]))
        # a flat normal, the paint over wood's default where a paint has no relief map of its own
        Image.fromarray(np.full((8, 8, 3), (128, 128, 255), dtype=np.uint8)).save(os.path.join(d, NAMES["flat"]))


def main():
    maps = build()
    n = numbers(maps)
    dirs = [os.path.join(REPO, REL), os.path.join(GAME_INPUTS, REL)]
    write(maps, dirs)
    n["source"] = {"asset": "kitchen_wood", "page": "https://polyhaven.com/a/kitchen_wood", "licence": "CC0 1.0",
                   "licenceUrl": "https://polyhaven.com/license", "files": SOURCE, "read": "2026-10-30"}
    for d in dirs:
        json.dump(n, open(os.path.join(d, "wood_trim.json"), "w", encoding="utf-8"), indent=1)
    print("woodTrim=%s px=%d sheet=%.2f m density=%.1f px/m (512 within 20%%) boards median %.3f (p2 %.3f, p98 %.3f) "
          "narrow %.3f end %.3f (wood 0.09 to 0.36) seam %.4f vs neighbour %.4f out=%s" % (
              "OK" if n["ok"] else "FAIL", PX, SHEET_M, DENSITY, n["boards"]["lum_median"], n["boards"]["lum_p2"],
              n["boards"]["lum_p98"], n["narrow"]["lum_median"], n["end"]["lum_median"], n["seam_step"],
              n["neighbour_step"], ",".join(dirs)))
    return 0 if n["ok"] else 1


def selftest():
    ok = []
    ok.append(abs(DENSITY - 487.62) < 0.1 and 410 <= DENSITY <= 614)
    ok.append(BOARDS[1] == NARROW[0] and NARROW[1] == END[0] and END[1] == 1.0)
    z = band_noise(64, 8, 1)
    ok.append(abs(float((z > 0.7).mean()) - 0.3) < 0.01)                          # a threshold t keeps 1 - t
    t = np.random.default_rng(0).random((10, 10, 1))
    m = mosaic(np.repeat(t, 3, axis=2), tiles=3, px=32)
    ok.append(m.shape == (32, 32, 3))
    n = normal_from_height(np.zeros((8, 8)), 1.0)
    ok.append(np.allclose(n[..., 2], 1.0))
    print("wood_trim selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    sys.exit(selftest() if "--selftest" in sys.argv else main())
