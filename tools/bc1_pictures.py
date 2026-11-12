"""Block-compress the shop rooms' run-time pictures (BC1) so the card holds 1/8 of their decoded size.

Item n09-3 step 4 (card memory), 12 Nov 2026: plan production/research/frame-headroom/STEP4-NEXT-PLAN-2026-11-12.md,
its review STEP4-PLAN-REVIEW-2026-11-12.md. No texture compressor runs in a packaged game, and none is on this PC,
so the blocks are made here, ahead of time, by the standard BC1 method (principal-axis endpoints, 5:6:5, four
colours, nearest index): no new tool, no licence. The PNG stays the source and the game's fallback.

Output, beside each picture under the game inputs (F:, same path as the repository): <name>.bc1 =
  b"LBC1", then four little-endian uint32 (block width, block height: the picture padded up to a multiple of 4
  by repeating its last row and column; then the picture's own width and height), then the blocks, row by row,
  8 bytes each (two 5:6:5 colours, colour0 > colour1, then 16 two-bit indices, texel i at bits 2i).
The game reads it in VignetteShot.cpp ImportBc1Texture (PF_DXT1, sRGB, one mip as today) and falls back to the
PNG when the .bc1 is missing, older than its PNG, or malformed; stage_game_data.py stages a .bc1 only when current.

Usage: python tools/bc1_pictures.py            make every day and lit-night shop picture's .bc1 that is missing or stale
       python tools/bc1_pictures.py --check    report error (PSNR) for each, write nothing
"""
import json
import os
import struct
import sys

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_INPUTS = os.environ.get("LEDGER_GAME_INPUTS", r"F:\LedgerTools\game-inputs")
STATES = ("day", "night_lit", "night_dark")
# the dark night pictures stay PNG: BC1's four colours a block showed a 4x4 checker and blotches on their dark
# surfaces (first small review, 12 Nov, the tea room's counter); day and lit night passed
COMPRESSED = ("day", "night_lit")
MAGIC = b"LBC1"


def shop_pictures():
    """The shop pictures the game reads, as repository-relative .png paths (shop-interiors.json)."""
    with open(os.path.join(REPO, "production/specs/shop-interiors.json"), encoding="utf-8") as fh:
        shops = json.load(fh).get("shops", []) or []
    return [sh["pictures"] + "_" + s + ".png" for sh in shops if sh.get("pictures") for s in COMPRESSED]


def source_of(rel):
    for root in (REPO, GAME_INPUTS):
        p = os.path.join(root, rel)
        if os.path.isfile(p):
            return p
    return None


def bc1_target(rel):
    return os.path.join(GAME_INPUTS, rel[:-4] + ".bc1")


def is_current(png, bc1):
    return os.path.isfile(bc1) and os.path.getmtime(bc1) >= os.path.getmtime(png)


def _to565(c):
    c = np.clip(np.rint(c), 0, 255).astype(np.uint32)
    return ((c[..., 0] * 31 + 127) // 255) << 11 | ((c[..., 1] * 63 + 127) // 255) << 5 | ((c[..., 2] * 31 + 127) // 255)


def _from565(v):
    v = v.astype(np.uint32)
    r = (v >> 11) & 31
    g = (v >> 5) & 63
    b = v & 31
    return np.stack([(r * 255 + 15) // 31, (g * 255 + 31) // 63, (b * 255 + 15) // 31], -1).astype(np.float32)


def _palette(c0, c1):
    """Four colours per block, colour0 > colour1 (four-colour mode)."""
    a, b = _from565(c0), _from565(c1)
    return np.stack([a, b, (2 * a + b) / 3.0, (a + 2 * b) / 3.0], 1)   # (n, 4, 3)


def encode(rgb):
    """rgb: (H, W, 3) uint8, H and W multiples of 4 -> bytes of BC1 blocks, row by row."""
    h, w, _ = rgb.shape
    bx, by = w // 4, h // 4
    px = rgb.reshape(by, 4, bx, 4, 3).transpose(0, 2, 1, 3, 4).reshape(-1, 16, 3).astype(np.float32)
    mean = px.mean(1, keepdims=True)
    d = px - mean
    cov = np.einsum("nki,nkj->nij", d, d)
    axis = np.ones((px.shape[0], 3), np.float32)
    for _ in range(8):   # power iteration for the principal axis
        axis = np.einsum("nij,nj->ni", cov, axis)
        axis /= np.maximum(np.linalg.norm(axis, axis=1, keepdims=True), 1e-6)
    t = np.einsum("nki,ni->nk", d, axis)
    lo, hi = t.min(1), t.max(1)
    inset = (hi - lo) / 16.0   # the usual inset of the extremes
    e0 = mean[:, 0] + axis * (hi - inset)[:, None]
    e1 = mean[:, 0] + axis * (lo + inset)[:, None]
    c0, c1 = _to565(e0), _to565(e1)
    swap = c0 < c1
    c0, c1 = np.where(swap, c1, c0), np.where(swap, c0, c1)
    pal = _palette(c0, c1)
    dist = ((px[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(-1)   # (n, 16, 4)
    idx = dist.argmin(2).astype(np.uint32)
    idx[c0 == c1] = 0   # a flat block: colour0 only (equal colours would mean three-colour mode)
    shifts = (np.arange(16, dtype=np.uint32) * 2)[None, :]
    bits = (idx << shifts).sum(1, dtype=np.uint64).astype(np.uint32)
    out = np.empty((px.shape[0], 2), np.uint32)
    out[:, 0] = c0 | (c1 << 16)
    out[:, 1] = bits
    return out.astype("<u4").tobytes()


def decode(blocks, w, h):
    v = np.frombuffer(blocks, "<u4").reshape(-1, 2)
    c0, c1 = v[:, 0] & 0xFFFF, v[:, 0] >> 16
    pal = _palette(c0, c1)
    a, b = _from565(c0), _from565(c1)
    three = c0 <= c1   # three-colour mode, never written here, decoded for completeness
    pal[three, 2] = (a[three] + b[three]) / 2.0
    pal[three, 3] = 0.0
    idx = (v[:, 1:2] >> (np.arange(16, dtype=np.uint32) * 2)[None, :]) & 3
    px = np.take_along_axis(pal, idx[:, :, None].astype(np.int64).repeat(3, 2), 1)
    return px.reshape(h // 4, w // 4, 4, 4, 3).transpose(0, 2, 1, 3, 4).reshape(h, w, 3)


def padded(rgb):
    h, w, _ = rgb.shape
    ph, pw = (-h) % 4, (-w) % 4
    return np.pad(rgb, ((0, ph), (0, pw), (0, 0)), mode="edge") if (ph or pw) else rgb


def psnr(a, b):
    mse = float(((a.astype(np.float32) - b.astype(np.float32)) ** 2).mean())
    return 99.0 if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def make(png, bc1):
    rgb = np.asarray(Image.open(png).convert("RGB"))
    h, w, _ = rgb.shape
    p = padded(rgb)
    blocks = encode(p)
    os.makedirs(os.path.dirname(bc1), exist_ok=True)
    tmp = bc1 + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(MAGIC + struct.pack("<4I", p.shape[1], p.shape[0], w, h) + blocks)
    os.replace(tmp, bc1)
    return psnr(p, decode(blocks, p.shape[1], p.shape[0])), w, h, len(blocks)


def main(argv):
    check = "--check" in argv
    rows = []
    for rel in shop_pictures():
        png = source_of(rel)
        if not png:
            rows.append((rel, "missing png"))
            continue
        bc1 = bc1_target(rel)
        if check:
            rgb = padded(np.asarray(Image.open(png).convert("RGB")))
            rows.append((rel, "psnr %.1f dB" % psnr(rgb, decode(encode(rgb), rgb.shape[1], rgb.shape[0]))))
            continue
        if is_current(png, bc1):
            rows.append((rel, "current"))
            continue
        q, w, h, n = make(png, bc1)
        rows.append((rel, "made %dx%d, %.1f MB (BGRA8 %.1f MB), psnr %.1f dB" % (w, h, n / 1e6, w * h * 4 / 1e6, q)))
    for r in rows:
        print("bc1_pictures: %s: %s" % r)
    bad = [r for r in rows if r[1] == "missing png"]
    print("bc1_pictures: %d pictures, %d missing" % (len(rows), len(bad)))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
