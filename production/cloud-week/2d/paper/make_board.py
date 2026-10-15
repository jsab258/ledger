#!/usr/bin/env python
"""make_board.py: the newsagent's window board SB1 (unit 4.2): fifteen cards taped inside the glass, composed from the delivered card pictures.

    /home/user/.bpyenv/bin/python make_board.py OUTDIR [--ppm 6] [--class B]

Reads OUTDIR/manifest.json and the class-B pictures of the fifteen cards the target's card_board lists (SA01 to SA15), places each at the target's x, y (the card's lower left corner
before it is turned, millimetres from the board's lower left) and turns it by rot_deg (counter-clockwise, the target's placement sense) about its centre. The board is the glass:
the picture is RGBA, transparent where there is no card. Writes OUTDIR/SB1/SB1_<class>_{basecolour,height,orm}.png, SB1/SB1.cards.json (each card's id, corners and centre, in
board millimetres) and adds a row to manifest.json under "boards".
"""
import argparse
import hashlib
import json
import math
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import paper_common as pc          # noqa: E402


def pix_hash(arr):
    a = np.ascontiguousarray(arr)
    return hashlib.sha256(str(a.shape).encode() + str(a.dtype).encode() + a.tobytes()).hexdigest()


def corners_mm(c):
    """The four corners of a card after its turn, board millimetres (y up)."""
    cx, cy = c["x_mm"] + c["w_mm"] / 2, c["y_mm"] + c["h_mm"] / 2
    a = math.radians(c["rot_deg"])
    out = []
    for sx, sy in ((-1, -1), (1, -1), (1, 1), (-1, 1)):
        x, y = sx * c["w_mm"] / 2, sy * c["h_mm"] / 2
        out.append((cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)))
    return out


def build(out, ppm=6.0, cls="B"):
    sc, gl = pc.load_reader(out)
    cb = sc.T["card_board"]
    man = json.loads((Path(out) / "manifest.json").read_text())
    rows = {r["item"]: r for r in man["items"]}
    W, H = cb["area_mm"]
    w, h = int(round(W * ppm)), int(round(H * ppm))
    canvas = np.zeros((h, w, 4), np.float32)            # premultiplied
    hmap = np.zeros((h, w), np.float32)
    orm_r = np.zeros((h, w), np.float32)
    cards = []
    for c in cb["cards"]:
        r = rows[c["item"]]
        f = Path(out) / r["classes"][cls]["basecolour"]["file"]
        im = Image.open(f).convert("RGBA")
        k = r["px_per_mm"] / ppm
        # area-average down to the board's scale first (the cards are drawn at 12 px/mm, the board at 6), then turn with bicubic resampling
        sw, sh = int(round(c["w_mm"] * ppm)), int(round(c["h_mm"] * ppm))
        a = np.asarray(im).astype(np.float32)
        a[..., :3] *= (a[..., 3:4] / 255.0)
        chans = [Image.fromarray(a[..., i]).resize((sw, sh), Image.BOX) for i in range(4)]
        small = np.stack([np.asarray(ch) for ch in chans], -1)
        pad = int(max(sw, sh) * 0.2) + 4
        big = np.zeros((sh + 2 * pad, sw + 2 * pad, 4), np.float32)
        big[pad:pad + sh, pad:pad + sw] = small
        rot = [np.asarray(Image.fromarray(big[..., i]).rotate(c["rot_deg"], resample=Image.BICUBIC, center=(big.shape[1] / 2, big.shape[0] / 2))) for i in range(4)]
        rot = np.stack(rot, -1)
        cx, cy = (c["x_mm"] + c["w_mm"] / 2) * ppm, (H - (c["y_mm"] + c["h_mm"] / 2)) * ppm
        x0, y0 = int(round(cx - big.shape[1] / 2)), int(round(cy - big.shape[0] / 2))
        sx0, sy0 = max(0, -x0), max(0, -y0)
        sx1, sy1 = min(big.shape[1], w - x0), min(big.shape[0], h - y0)
        if sx1 <= sx0 or sy1 <= sy0:
            continue
        sub = rot[sy0:sy1, sx0:sx1]
        al = np.clip(sub[..., 3:4] / 255.0, 0, 1)
        dst = canvas[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1]
        dst[:] = sub * 1.0 + dst * (1 - al)
        # a card is 0.3 mm proud of the glass; the tape a little more
        hmap[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1] = np.maximum(hmap[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1], al[..., 0] * 0.3)
        orm_r[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1] = np.maximum(orm_r[y0 + sy0:y0 + sy1, x0 + sx0:x0 + sx1], al[..., 0] * 0.8)
        cards.append(dict(item=c["item"], corners_mm=[list(map(lambda v: round(v, 2), p)) for p in corners_mm(c)], centre_mm=[round(c["x_mm"] + c["w_mm"] / 2, 2), round(c["y_mm"] + c["h_mm"] / 2, 2)], rot_deg=c["rot_deg"]))
    a = np.clip(canvas[..., 3], 0, 255)
    rgb = np.where(a[..., None] > 0.5, canvas[..., :3] / np.maximum(a[..., None] / 255.0, 1e-3), 0)
    rgba = np.dstack([np.clip(np.round(rgb), 0, 255), np.clip(np.round(a), 0, 255)]).astype(np.uint8)
    d = Path(out) / "SB1"
    d.mkdir(parents=True, exist_ok=True)
    Image.fromarray(rgba, "RGBA").save(d / ("SB1_%s_basecolour.png" % cls), compress_level=6)
    h16 = np.clip(np.round(32768 + hmap * 25600), 0, 65535).astype(np.uint16)
    Image.fromarray(h16).save(d / ("SB1_%s_height.png" % cls), compress_level=6)
    orm = np.zeros((h, w, 3), np.uint8)
    orm[..., 0] = 255
    orm[..., 1] = np.where(a > 128, np.clip(orm_r / np.maximum(a / 255.0, 1e-3) * 255, 0, 255), 255 * 0.5).astype(np.uint8)
    Image.fromarray(orm, "RGB").save(d / ("SB1_%s_orm.png" % cls), compress_level=6)
    (d / "SB1.cards.json").write_text(json.dumps(dict(board=cb["id"], area_mm=cb["area_mm"], px_per_mm=ppm, size_px=[w, h], cards=cards)), encoding="utf-8")
    row = dict(item="SB1", title=cb["title"], area_mm=cb["area_mm"], px_per_mm=ppm, size_px=[w, h], class_=cls, cards=len(cards), glass_u_m=cb["glass_u_m"], z_bottom_m=cb["z_bottom_m"],
               basecolour=dict(file="SB1/SB1_%s_basecolour.png" % cls, mode="RGBA", sha256_pixels=pix_hash(rgba)), height=dict(file="SB1/SB1_%s_height.png" % cls, units_per_mm=25600.0, zero=32768, sha256_pixels=pix_hash(h16)),
               orm=dict(file="SB1/SB1_%s_orm.png" % cls, sha256_pixels=pix_hash(orm)), cards_json="SB1/SB1.cards.json")
    man["boards"] = [b for b in man.get("boards", []) if b["item"] != "SB1"] + [row]
    (Path(out) / "manifest.json").write_text(json.dumps(man, indent=1), encoding="utf-8")
    print("SB1: %d cards on %dx%d px (%g px/mm)" % (len(cards), w, h, ppm))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--ppm", type=float, default=6.0)
    ap.add_argument("--class", dest="cls", default="B")
    a = ap.parse_args()
    build(a.out, a.ppm, a.cls)
