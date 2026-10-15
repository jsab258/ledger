#!/usr/bin/env python
"""make_previews.py: review previews of the wear masks (unit 4.5): JPEG, 1600 px at most, under 500 KB.

    /home/user/.bpyenv/bin/python make_previews.py OUTDIR PREVIEW_DIR [--tag v1] [--date 2026-10-12]

Contact sheets by group of kinds: each kind's variants 0 and 1 drawn in the target's own colour for the kind over a mid-grey wall or ground (alpha = the mask), at one scale per sheet, a seamless tile
shown twice over; and the composed brick foot and head under the target's order, floor and colour rule on the maker's own masks (self_check.compose_walls), in the sooted and the cleaned state.
"""
import argparse
import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import wear_common as wc          # noqa: E402
import make_wear as mw           # noqa: E402

MAXW = 1600
BG_WALL, BG_GROUND = (150, 142, 132), (128, 126, 122)
GROUPS = [
    ("walls-runs", "streaks, fingers, runs and stains on walls", ["streak_sill", "streak_coping", "rust_bleed", "algae_downpipe", "bird_dropping", "salt_bloom", "wall_foot_splash", "wall_foot_damp"]),
    ("walls-surface", "paint, render, posters and soot on walls", ["paint_flake", "paint_fade", "render_crack", "render_patch", "poster_remnant", "wall_soot", "wall_head_band", "sign_ghost", "graffiti_buff", "handle_wear", "stone_top_lichen"]),
    ("ground", "pavement and road marks", ["gum", "cig_end", "pavement_stain", "flag_patch_crack", "footway_infill", "gutter_grime", "road_oil", "road_blot", "tyre_scuff", "road_patch", "road_crack", "line_wear"]),
    ("iron", "iron, grates", ["iron_wear", "grate_wear"]),
]
GROUND = {"gum", "cig_end", "pavement_stain", "flag_patch_crack", "footway_infill", "gutter_grime", "road_oil", "road_blot", "tyre_scuff", "road_patch", "road_crack", "line_wear"}


def font(px):
    for p in (wc.ROOT / "production" / "fonts" / "archivo" / "Archivo-var.ttf",):
        if p.exists():
            return ImageFont.truetype(str(p), px)
    return ImageFont.load_default()


def save_jpeg(im, path, limit=500_000):
    q = 90
    while True:
        im.save(path, "JPEG", quality=q, optimize=True)
        if Path(path).stat().st_size <= limit or q <= 50:
            return
        q -= 5


def tile_img(out, tj, draw, row, variant, scale):
    """one mask as a colour picture at `scale` px/m (the picture is the mask file reduced)."""
    k = tj["kinds"][row["kind"]]
    f = row["files"][variant % len(row["files"])]
    a = np.asarray(Image.open(Path(out) / f["file"])).astype(np.float32) / 65535.0
    ppm = f["px_per_m"]
    w, h = max(2, int(round(a.shape[1] * scale / ppm))), max(2, int(round(a.shape[0] * scale / ppm)))
    m = np.asarray(Image.fromarray(a, mode="F").resize((w, h), Image.BOX))
    if wc.wrap_mode(k) == "xy":
        m = np.tile(m, (2, 2))
    elif wc.wrap_mode(k) == "x":
        m = np.tile(m, (1, 2))
    col = np.asarray(draw.PALETTE.get(row["kind"], (30, 30, 30)), np.float32)
    bg = np.asarray(BG_GROUND if row["kind"] in GROUND else BG_WALL, np.float32)
    rgb = bg[None, None, :] * (1 - m[..., None]) + col[None, None, :] * m[..., None]
    return Image.fromarray(np.clip(rgb, 0, 255).astype(np.uint8))


def sheet(out, tj, draw, rows, ids, scale, title):
    pad = 10
    f = font(13)
    cells = []
    for kid in ids:
        r = rows.get(kid)
        if not r:
            continue
        ims = [tile_img(out, tj, draw, r, v, scale) for v in (0, 1)]
        cells.append((kid, ims))
    x, y, rowh = pad, pad + 22, 0
    placed = []
    for kid, ims in cells:
        wcell = sum(i.width for i in ims) + 4
        if x + wcell + pad > MAXW and x > pad:
            x, y, rowh = pad, y + rowh + 20 + pad, 0
        placed.append((x, y, kid, ims))
        x += wcell + pad
        rowh = max(rowh, max(i.height for i in ims))
    width = min(MAXW, max(px + sum(i.width for i in ims) + 4 for px, py, kid, ims in placed) + pad)
    canvas = Image.new("RGB", (width, y + rowh + 20 + pad), (72, 70, 68))
    d = ImageDraw.Draw(canvas)
    d.text((pad, 4), "%s  (%g px/m)" % (title, scale), font=font(15), fill=(235, 235, 230))
    for px, py, kid, ims in placed:
        xx = px
        for im in ims:
            canvas.paste(im, (xx, py))
            xx += im.width + 4
        d.text((px, py + max(i.height for i in ims) + 3), kid, font=f, fill=(235, 235, 230))
    return canvas


def composed(out, tj, draw, scw, rows):
    ed = draw.edges_by_kind(tj)
    seed = 1990
    masks, mppm = {}, {}
    for kid in ("wall_soot", "wall_foot_damp", "wall_foot_splash", "salt_bloom", "algae_downpipe", "wall_head_band"):
        m, _, ppm = mw.make_mask(tj, draw, ed, kid, seed, 0)
        masks[kid], mppm[kid] = m, ppm
    ims = []
    for state in ("cleaned", "sooted"):
        r = scw.compose_walls(tj, draw, seed, state, 400, head=True, masks=masks, masks_ppm=mppm)          # 400 px/m: the review found 200 too small to judge the foot
        lin = r["final"]
        srgb = scw.lin_to_srgb8(lin) if hasattr(scw, "lin_to_srgb8") else np.clip(lin ** (1 / 2.2) * 255, 0, 255)
        ims.append(Image.fromarray(np.clip(srgb, 0, 255).astype(np.uint8)))
    w = sum(i.width for i in ims) + 10
    canvas = Image.new("RGB", (w, ims[0].height + 24), (72, 70, 68))
    d = ImageDraw.Draw(canvas)
    d.text((6, 4), "composed brick foot (a downpipe at x 1 m) and the head under a verge, on the maker's own masks: cleaned and sooted house, 400 px/m", font=font(13), fill=(235, 235, 230))
    x = 0
    for i in ims:
        canvas.paste(i, (x, 24))
        x += i.width + 10
    return canvas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("prev")
    ap.add_argument("--tag", default="v1")
    ap.add_argument("--date", default="2026-10-12")
    a = ap.parse_args()
    out, prev = Path(a.out), Path(a.prev)
    prev.mkdir(parents=True, exist_ok=True)
    tj, draw, scw = wc.load_target()
    man = json.loads((out / "manifest.json").read_text())
    rows = {r["kind"]: r for r in man["kinds"]}
    for name, title, ids in GROUPS:
        scale = 120 if name != "iron" else 220
        im = sheet(out, tj, draw, rows, ids, scale, title)
        if im.height > 1600:
            im.thumbnail((1600, 1600))
        p = prev / ("wear-%s-%s-%s.jpg" % (name, a.tag, a.date))
        save_jpeg(im, p)
        print(p.name, im.size, p.stat().st_size // 1024, "KB")
    im = composed(out, tj, draw, scw, rows)
    p = prev / ("wear-composed-foot-head-%s-%s.jpg" % (a.tag, a.date))
    save_jpeg(im, p)
    print(p.name, im.size, p.stat().st_size // 1024, "KB")
    return 0


if __name__ == "__main__":
    sys.exit(main())
