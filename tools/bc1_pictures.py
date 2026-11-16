"""Block-compress the game's run-time pictures ahead of time, so the card holds 1/8 (BC1) or 1/4 (BC3, BC5) of their decoded size.

Item n09-3 step 4 (card memory), 12 Nov 2026: plan production/research/frame-headroom/STEP4-NEXT-PLAN-2026-11-12.md,
its review STEP4-PLAN-REVIEW-2026-11-12.md: the shop rooms' pictures, BC1. Widened 16 Nov 2026 (n16-3, the packing
plan's step 2, PACKING-PLAN-2026-11-16.md): every run-time picture family the game reads (street maps, scans, decals,
sky, scalp), BC5 for normal maps and BC3 for colour whose alpha matters. No texture compressor runs in a packaged game,
and none is on this PC, so the blocks are made here by the standard methods (BC1: principal-axis endpoints, 5:6:5,
four colours, nearest index; BC4, the half of BC3 and BC5: the block's own minimum and maximum, eight levels, nearest
index): no new tool, no licence. The PNG or JPEG stays the source and the game's fallback.

Output, under the game inputs (F:, the picture's repository path), beside each picture: <name>.bc1, .bc3 or .bc5 =
  a four-byte magic (b"LBC1", b"LBC3", b"LBC5"), then four little-endian uint32 (block width, block height: the
  picture made a multiple of 4; then the picture's own width and height), then the blocks, row by row:
  BC1  8 bytes a block: two 5:6:5 colours, colour0 > colour1, then 16 two-bit indices, texel i at bits 2i.
  BC3 16 bytes a block: a BC4 block of the alpha, then a BC1 colour block (always read in four-colour mode).
  BC5 16 bytes a block: a BC4 block of red, then one of green (a normal map's x and y; the material's normal sampler
      rebuilds z from them, Common.ush UnpackNormalMap).
  BC4: two bytes (value0 > value1: eight levels), then 16 three-bit indices, texel i at bits 3i.
A side not a multiple of 4 is padded by repeating its last row or column when that adds at most 0.5% of the side
(the shop rooms' 1855 to 1856), else the picture is resampled to the next multiple of 4, so its UVs still cover it.
The game reads any of them in VignetteShot.cpp ImportTexture (ImportBlockTexture), and falls back to the PNG when the
copy is missing, older than its picture, or malformed; stage_game_data.py stages a copy only while it is current.

Kept as PNG (named exceptions): brick ID maps (read nearest, exact values), cropped decals (the crop needs the decoded
picture), the shops' dark night pictures (BC1 showed a 4x4 checker on their dark surfaces, first small review 12 Nov),
the interface's pictures (LedgerPaper.cpp, Slate brushes), and the decal packs' unread source maps.

Usage: python tools/bc1_pictures.py            make every run-time picture's copy that is missing or stale
       python tools/bc1_pictures.py --check    report the error (PSNR) of each, write nothing
       python tools/bc1_pictures.py --shops    the shop rooms only (the 12 Nov scope)
       python tools/bc1_pictures.py --selftest the encoders against their own decoders on made pictures
"""
import json
import os
import re
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
MAGICS = {"bc1": b"LBC1", "bc3": b"LBC3", "bc5": b"LBC5"}
BLOCK_BYTES = {"bc1": 8, "bc3": 16, "bc5": 16}
FORMATS = tuple(MAGICS)
PICTURE_EXT = (".png", ".jpg", ".jpeg")
DECAL_ROOT = "ledger/Assets/StreamingAssets/Decals"
SHOP_ROOMS = "production/art/shop-rooms/"
PAD_LIMIT = 0.005   # padding by repetition only up to 0.5% of a side; more is resampled


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


def target(rel, fmt):
    return os.path.join(GAME_INPUTS, os.path.splitext(rel)[0] + "." + fmt)


def bc1_target(rel):
    return target(rel, "bc1")


def is_current(png, bc1):
    return os.path.isfile(bc1) and os.path.getmtime(bc1) >= os.path.getmtime(png)


# ---------------------------------------------------------------------------------------------------------------- BC1

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


def _blocks(img, ch):
    """(H, W, ch) -> (n, 16, ch), blocks row by row, texels row by row inside a block."""
    h, w = img.shape[:2]
    return img.reshape(h // 4, 4, w // 4, 4, ch).transpose(0, 2, 1, 3, 4).reshape(-1, 16, ch)


def _unblocks(px, w, h, ch):
    return px.reshape(h // 4, w // 4, 4, 4, ch).transpose(0, 2, 1, 3, 4).reshape(h, w, ch)


def encode(rgb):
    """rgb: (H, W, 3) uint8, H and W multiples of 4 -> bytes of BC1 blocks, row by row."""
    return _encode_bc1_words(_blocks(rgb, 3).astype(np.float32)).astype("<u4").tobytes()


def _encode_bc1_words(px):
    """px: (n, 16, 3) float -> (n, 2) uint32 BC1 blocks (four-colour mode; a flat block is colour0 only)."""
    out = np.empty((px.shape[0], 2), np.uint32)
    step = 65536   # in slices, so a 4096-wide picture's distances fit in memory
    for s in range(0, px.shape[0], step):
        p = px[s:s + step]
        mean = p.mean(1, keepdims=True)
        d = p - mean
        cov = np.einsum("nki,nkj->nij", d, d)
        axis = np.ones((p.shape[0], 3), np.float32)
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
        dist = ((p[:, :, None, :] - pal[:, None, :, :]) ** 2).sum(-1)   # (n, 16, 4)
        idx = dist.argmin(2).astype(np.uint32)
        idx[c0 == c1] = 0   # a flat block: colour0 only (equal colours would mean three-colour mode)
        shifts = (np.arange(16, dtype=np.uint32) * 2)[None, :]
        out[s:s + step, 0] = c0 | (c1 << 16)
        out[s:s + step, 1] = (idx << shifts).sum(1, dtype=np.uint64).astype(np.uint32)
    return out


def _decode_bc1_words(v, four_only=False):
    c0, c1 = v[:, 0] & 0xFFFF, v[:, 0] >> 16
    pal = _palette(c0, c1)
    a, b = _from565(c0), _from565(c1)
    if not four_only:
        three = c0 <= c1   # three-colour mode, never written here, decoded for completeness
        pal[three, 2] = (a[three] + b[three]) / 2.0
        pal[three, 3] = 0.0
    idx = (v[:, 1:2] >> (np.arange(16, dtype=np.uint32) * 2)[None, :]) & 3
    return np.take_along_axis(pal, idx[:, :, None].astype(np.int64).repeat(3, 2), 1)   # (n, 16, 3)


def decode(blocks, w, h):
    v = np.frombuffer(blocks, "<u4").reshape(-1, 2)
    return _unblocks(_decode_bc1_words(v), w, h, 3)


# ---------------------------------------------------------------------------------------------------------------- BC4

def _bc4_palette(r0, r1):
    """(n,) endpoints, r0 > r1 -> (n, 8) levels (eight-level mode; r0 == r1 is a flat block, index 0 only)."""
    a, b = r0.astype(np.float32), r1.astype(np.float32)
    lv = [a, b] + [((7 - i) * a + i * b) / 7.0 for i in range(1, 7)]
    pal = np.stack(lv, 1)
    six = r0 <= r1   # six-level mode, never written here but for a flat block, decoded for completeness
    if six.any():
        for i in range(1, 5):
            pal[six, 1 + i] = ((5 - i) * a[six] + i * b[six]) / 5.0
        pal[six, 6] = 0.0
        pal[six, 7] = 255.0
    return pal


def _encode_bc4(ch):
    """ch: (n, 16) float of one channel -> (n, 8) uint8 BC4 blocks."""
    hi = np.clip(np.rint(ch.max(1)), 0, 255).astype(np.uint32)
    lo = np.clip(np.rint(ch.min(1)), 0, 255).astype(np.uint32)
    pal = _bc4_palette(hi, lo)
    idx = np.abs(ch[:, :, None] - pal[:, None, :]).argmin(2).astype(np.uint64)   # (n, 16)
    idx[hi == lo] = 0
    bits = (idx << (np.arange(16, dtype=np.uint64) * 3)[None, :]).sum(1, dtype=np.uint64)
    out = np.empty((ch.shape[0], 8), np.uint8)
    out[:, 0] = hi
    out[:, 1] = lo
    for k in range(6):
        out[:, 2 + k] = ((bits >> np.uint64(8 * k)) & np.uint64(0xFF)).astype(np.uint8)
    return out


def _decode_bc4(b):
    """(n, 8) uint8 -> (n, 16) float."""
    pal = _bc4_palette(b[:, 0].astype(np.uint32), b[:, 1].astype(np.uint32))
    bits = np.zeros(b.shape[0], np.uint64)
    for k in range(6):
        bits |= b[:, 2 + k].astype(np.uint64) << np.uint64(8 * k)
    idx = (bits[:, None] >> (np.arange(16, dtype=np.uint64) * 3)[None, :]) & np.uint64(7)
    return np.take_along_axis(pal, idx.astype(np.int64), 1)


# ------------------------------------------------------------------------------------------------------- BC3 and BC5

def encode_bc3(rgba):
    px = _blocks(rgba, 4).astype(np.float32)
    a = _encode_bc4(px[:, :, 3])
    c = _encode_bc1_words(px[:, :, :3]).astype("<u4").view(np.uint8).reshape(-1, 8)
    return np.concatenate([a, c], 1).tobytes()


def decode_bc3(blocks, w, h):
    b = np.frombuffer(blocks, np.uint8).reshape(-1, 16)
    a = _decode_bc4(b[:, :8])
    c = _decode_bc1_words(np.ascontiguousarray(b[:, 8:]).view("<u4").reshape(-1, 2), four_only=True)
    return _unblocks(np.concatenate([c, a[:, :, None]], 2), w, h, 4)


def encode_bc5(rg):
    px = _blocks(rg, 2).astype(np.float32)
    return np.concatenate([_encode_bc4(px[:, :, 0]), _encode_bc4(px[:, :, 1])], 1).tobytes()


def decode_bc5(blocks, w, h):
    b = np.frombuffer(blocks, np.uint8).reshape(-1, 16)
    return _unblocks(np.stack([_decode_bc4(b[:, :8]), _decode_bc4(b[:, 8:])], 2), w, h, 2)


# ----------------------------------------------------------------------------------------------------------- pictures

def padded(rgb):
    h, w = rgb.shape[:2]
    ph, pw = (-h) % 4, (-w) % 4
    pad = ((0, ph), (0, pw)) + ((0, 0),) * (rgb.ndim - 2)
    return np.pad(rgb, pad, mode="edge") if (ph or pw) else rgb


def fitted(img):
    """A multiple of 4 on each side: repeated last rows or columns when they add at most 0.5%, else resampled."""
    h, w = img.shape[:2]
    ph, pw = (-h) % 4, (-w) % 4
    if not (ph or pw):
        return img, "exact"
    if ph <= PAD_LIMIT * h and pw <= PAD_LIMIT * w:
        return padded(img), "padded"
    size = (w + pw, h + ph)   # each channel resampled alone (Lanczos), so any channel count goes the same way
    chans = [np.asarray(Image.fromarray(np.ascontiguousarray(img[:, :, k])).resize(size, Image.LANCZOS))
             for k in range(img.shape[2])]
    return np.stack(chans, 2), "resampled"


def psnr(a, b):
    mse = float(((a.astype(np.float32) - b.astype(np.float32)) ** 2).mean())
    return 99.0 if mse == 0 else 10 * np.log10(255.0 ** 2 / mse)


def _load(rel):
    with open(os.path.join(REPO, rel), encoding="utf-8") as fh:
        return json.load(fh)


def id_maps():
    out = set()
    for spec in ("production/specs/vignette-pieces.json", "production/specs/ps5-corner.json"):
        for sc in _load(spec).get("scanned", []) or []:
            if isinstance(sc.get("ids"), str) and sc["ids"]:
                out.add(sc["ids"])
    return out


def cropped_decals():
    """Decal cards the scene asks for with a crop (an asset string 'id#u0,v0,u1,v1', SurfaceBind.h SplitDecalAsset)."""
    out = set()
    for rel in ("production/specs/vignette-pieces.json", "production/assets/street/quay-street.json"):
        try:
            text = open(os.path.join(REPO, rel), encoding="utf-8").read()
        except OSError:
            continue
        for m in re.finditer(r'"([A-Za-z0-9_./-]+)#[-0-9.]+,[-0-9.]+,[-0-9.]+,[-0-9.]+"', text):
            out.add(DECAL_ROOT + "/" + m.group(1) + ".png")
    return out


def is_normal(leaf):
    leaf = leaf.lower()
    return leaf.endswith("_n") or "_nor_dx" in leaf or "_nor_gl" in leaf or "_normal" in leaf


def is_rough(leaf):
    leaf = leaf.lower()
    return leaf.endswith("_r") or "_rough" in leaf


def runtime_pictures():
    """Every picture the game may decode at run time, as repository paths, from the files the game reads them from
    (stage_game_data.wanted(), which follows the street's sidecar, the scans, the wear layer, the shop rooms, the sky,
    the photographed surfaces, the decal root and the scalp the same way the game resolves them)."""
    sys.path.insert(0, os.path.join(REPO, "tools", "ue"))
    import stage_game_data
    return [f for f in stage_game_data.wanted() if f.lower().endswith(PICTURE_EXT)]


def plan(rel, shops, ids, crops):
    """(format or None, why) for one picture; the image itself decides only BC1 against BC3 (alpha that matters)."""
    leaf = os.path.splitext(os.path.basename(rel))[0]
    if rel in ids:
        return None, "brick ID map (read nearest, exact values)"
    if rel in crops:
        return None, "cropped decal (the crop needs the decoded picture)"
    if rel.startswith("production/art/ui/"):
        return None, "interface picture (LedgerPaper.cpp, a Slate brush)"
    if rel.startswith(DECAL_ROOT + "/") and re.search(r"_[0-9]K-(PNG|JPG)_", os.path.basename(rel)):
        return None, "decal pack source map (not read by the game)"
    if rel.startswith(SHOP_ROOMS):
        if rel.endswith("_night_dark.png"):
            return None, "dark night shop picture (BC1 checker, review 12 Nov)"
        if rel not in shops:
            # a shop picture the street's own rows wear (quay-street.json "decal"; 16 Nov: chandler_day and three more
            # were read by the game and decoded as PNG when this rule called them unread)
            return "colour", "shop picture worn by a street row"
        return "bc1", "shop room"
    if is_normal(leaf):
        return "bc5", "normal map"
    if is_rough(leaf):
        return "bc1", "roughness map"
    return "colour", "colour"


def read_picture(path):
    im = Image.open(path)
    if im.mode in ("I;16", "I;16B", "I", "F"):
        return None
    has_alpha = im.mode in ("RGBA", "LA", "PA") or (im.mode == "P" and "transparency" in im.info)
    rgba = np.asarray(im.convert("RGBA"))
    return rgba, has_alpha


def choose(fmt, rgba, has_alpha):
    if fmt == "colour":
        return "bc3" if has_alpha and int(rgba[:, :, 3].min()) < 255 else "bc1"
    return fmt


def compress(fmt, rgba):
    """-> (blocks, block w, block h, fit, psnr text, psnr worst)"""
    if fmt == "bc5":
        img, fit = fitted(np.ascontiguousarray(rgba[:, :, :2]))
        blocks = encode_bc5(img)
        q = psnr(img, decode_bc5(blocks, img.shape[1], img.shape[0]))
        return blocks, img.shape[1], img.shape[0], fit, "rg %.1f dB" % q, q
    if fmt == "bc3":
        img, fit = fitted(rgba)
        blocks = encode_bc3(img)
        dec = decode_bc3(blocks, img.shape[1], img.shape[0])
        qc, qa = psnr(img[:, :, :3], dec[:, :, :3]), psnr(img[:, :, 3], dec[:, :, 3])
        return blocks, img.shape[1], img.shape[0], fit, "rgb %.1f dB, alpha %.1f dB" % (qc, qa), min(qc, qa)
    img, fit = fitted(np.ascontiguousarray(rgba[:, :, :3]))
    blocks = encode(img)
    q = psnr(img, decode(blocks, img.shape[1], img.shape[0]))
    return blocks, img.shape[1], img.shape[0], fit, "rgb %.1f dB" % q, q


def write(path, fmt, bw, bh, w, h, blocks):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(MAGICS[fmt] + struct.pack("<4I", bw, bh, w, h) + blocks)
    os.replace(tmp, path)


def make(png, bc1):
    """The 12 Nov entry point: one BC1 copy, padded. Kept for callers of that day."""
    rgb = np.asarray(Image.open(png).convert("RGB"))
    h, w, _ = rgb.shape
    p = padded(rgb)
    blocks = encode(p)
    write(bc1, "bc1", p.shape[1], p.shape[0], w, h, blocks)
    return psnr(p, decode(blocks, p.shape[1], p.shape[0])), w, h, len(blocks)


def main(argv):
    if "--selftest" in argv:
        return selftest()
    check = "--check" in argv
    shops = set(shop_pictures())
    rels = sorted(shops) if "--shops" in argv else runtime_pictures()
    ids, crops = id_maps(), cropped_decals()
    rows, made, kept, worst = [], 0, 0, []
    before = after = 0.0
    for rel in rels:
        fmt, why = plan(rel, shops, ids, crops)
        src = source_of(rel)
        if not src:
            rows.append((rel, "missing picture"))
            continue
        if fmt is None:
            kept += 1
            rows.append((rel, "stays PNG: " + why))
            continue
        got = read_picture(src)
        if got is None:
            kept += 1
            rows.append((rel, "stays PNG: sixteen-bit or float picture"))
            continue
        rgba, has_alpha = got
        fmt = choose(fmt, rgba, has_alpha)
        out = target(rel, fmt)
        h, w = rgba.shape[:2]
        if not check and is_current(src, out):
            rows.append((rel, "current %s" % fmt.upper()))
            continue
        blocks, bw, bh, fit, qtext, q = compress(fmt, rgba)
        worst.append((q, rel, fmt, qtext))
        before += w * h * 4 / 2 ** 20
        after += len(blocks) / 2 ** 20
        if check:
            rows.append((rel, "%s %dx%d (%s), %s" % (fmt.upper(), w, h, fit, qtext)))
            continue
        write(out, fmt, bw, bh, w, h, blocks)
        # one copy a picture: another format's older copy would still be read before it
        for other in FORMATS:
            stale = target(rel, other)
            if other != fmt and os.path.isfile(stale):
                os.remove(stale)
        made += 1
        rows.append((rel, "made %s %dx%d (%s), %.2f MB (BGRA8 %.2f MB), %s" % (
            fmt.upper(), w, h, fit, len(blocks) / 2 ** 20, w * h * 4 / 2 ** 20, qtext)))
    for r in rows:
        print("bc1_pictures: %s: %s" % r)
    worst.sort()
    for q, rel, fmt, qtext in worst[:10]:
        print("bc1_pictures: worst: %s %s (%s)" % (fmt.upper(), rel, qtext))
    bad = [r for r in rows if r[1] == "missing picture"]
    print("bc1_pictures: %d pictures, %s %d, %d stay PNG, %d missing; encoded %.1f MB of BGRA8 as %.1f MB"
          % (len(rows), "checked" if check else "made", len(worst) if check else made, kept, len(bad), before, after))
    return 1 if bad else 0


def selftest():
    rng = np.random.default_rng(7)
    ok = bad = 0

    def t(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("bc1_pictures selftest FAIL " + name)
    grad = np.dstack([np.tile(np.linspace(0, 255, 64), (64, 1))] * 3).astype(np.uint8)
    t("BC1 of a smooth ramp above 35 dB", psnr(grad, decode(encode(grad), 64, 64)) > 35)
    flat = np.full((8, 8, 4), (90, 120, 30, 255), np.uint8)
    t("BC1 of a flat block is exact to 5:6:5", psnr(flat[:, :, :3], decode(encode(flat[:, :, :3]), 8, 8)) > 40)
    a = rng.integers(0, 256, (16, 16)).astype(np.uint8)
    rg = np.dstack([a, a[::-1]])
    t("BC5 of noise above 28 dB", psnr(rg, decode_bc5(encode_bc5(rg), 16, 16)) > 28)
    t("BC5 is 16 bytes a block", len(encode_bc5(rg)) == 16 * 16)
    ramp = np.tile(np.linspace(0, 255, 32), (32, 1)).astype(np.uint8)
    t("BC4 of a ramp above 40 dB", psnr(np.dstack([ramp, ramp]), decode_bc5(encode_bc5(np.dstack([ramp, ramp])), 32, 32)) > 40)
    rgba = np.dstack([grad, np.tile(np.linspace(255, 0, 64), (64, 1)).astype(np.uint8)])
    dec = decode_bc3(encode_bc3(rgba), 64, 64)
    t("BC3's alpha above 40 dB", psnr(rgba[:, :, 3], dec[:, :, 3]) > 40)
    t("BC3's colour above 35 dB", psnr(rgba[:, :, :3], dec[:, :, :3]) > 35)
    t("BC3 is 16 bytes a block", len(encode_bc3(rgba)) == 16 * 256)
    t("a 1855 side is padded", fitted(np.zeros((1855, 8, 3), np.uint8))[1] == "padded")
    t("a 102 side is resampled", fitted(np.zeros((102, 8, 3), np.uint8))[0].shape[0] == 104)
    t("normal maps by name", is_normal("brick_red_n") and is_normal("brick_4_nor_dx_2k") and not is_normal("kerbstone"))
    t("roughness by name", is_rough("paving_r") and is_rough("asphalt_01_rough_2k") and not is_rough("door"))
    shops = {SHOP_ROOMS + "x_day.png"}
    t("dark night shop stays PNG", plan(SHOP_ROOMS + "x_night_dark.png", shops, set(), set())[0] is None)
    t("a shop's day picture is BC1", plan(SHOP_ROOMS + "x_day.png", shops, set(), set())[0] == "bc1")
    t("a street row's shop picture is compressed too", plan(SHOP_ROOMS + "y_day.png", shops, set(), set())[0] == "colour")
    t("an ID map stays PNG", plan("a/b_ids.png", shops, {"a/b_ids.png"}, set())[0] is None)
    t("a pack source map stays PNG", plan(DECAL_ROOT + "/ambientcg/X/X_2K-PNG_Color.png", shops, set(), set())[0] is None)
    t("colour with alpha that matters is BC3", choose("colour", rgba, True) == "bc3")
    t("colour with opaque alpha is BC1", choose("colour", np.dstack([grad, np.full((64, 64), 255, np.uint8)]), True) == "bc1")
    # AN INDEPENDENT READER: Pillow's DDS decoder reads the same blocks within rounding (16 Nov, before the game did)
    import io
    for fourcc, blocks, mine, ch in ((b"DXT1", encode(grad), decode(encode(grad), 64, 64), 3),
                                     (b"DXT5", encode_bc3(rgba), dec, 4),
                                     (b"ATI2", encode_bc5(rgba[:, :, :2].copy()), decode_bc5(encode_bc5(rgba[:, :, :2].copy()), 64, 64), 2)):
        head = struct.pack("<4sIIIIIII11I", b"DDS ", 124, 0x81007, 64, 64, len(blocks), 0, 1, *([0] * 11))
        head += struct.pack("<II4s5I", 32, 4, fourcc, 0, 0, 0, 0, 0) + struct.pack("<5I", 0x1000, 0, 0, 0, 0)
        try:
            im = Image.open(io.BytesIO(head + blocks))
            im.load()
            theirs = np.asarray(im).astype(np.float32)[:, :, :ch]
            t("%s blocks read the same in Pillow's DDS reader" % fourcc.decode(), float(np.abs(theirs - mine[:, :, :ch]).max()) <= 2.0)
        except Exception as e:
            t("%s blocks open in Pillow's DDS reader (%s)" % (fourcc.decode(), e), False)
    print("bc1_pictures selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
