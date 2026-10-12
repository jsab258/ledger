"""Rita's models and textures: fetched (Poly Haven, CC0), looked at, and every maker's mark painted out of the maps by script.

Used by build_ritas.py. Nothing here needs Blender. Step 0 of the build (TARGET.md 11, INV-05, INV-06):
  fetch()        every Poly Haven id Rita's room and display place, at 1k, into SCRATCH/polyhaven/<id>/1k/ (never in the repository),
                 with the fetcher the project already has (tools/art-recipes/fetch_polyhaven.py, imported, not rewritten)
  sheets()       contact sheets of every base-colour map (12 to a sheet) into SCRATCH/sheets/, to be looked at before the build
  blank()        target.json's `blank` entries applied to the maps: each box takes the median of a 6 px ring just outside it,
                 then a same-size patch of the map's own grain is laid over it (no flat patch); <map>_clean.jpg is written beside
                 the map and <id>_clean.gltf points at it
  verify()       INV-06's script test on every final box: the largest difference from the ring colour at most 24 levels and fewer
                 than 2 per cent of the box's pixels with a gradient above 40; a whole-map replacement must differ from the original
"""
import hashlib
import importlib.util
import json
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
POLY = os.environ.get("LEDGER_POLYHAVEN", os.path.join(SCRATCH, "polyhaven"))
WORK = os.path.join(SCRATCH, "shop-windows")
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "shop-windows", "target.json")
TEXTURES = ["old_linoleum_flooring_01", "painted_plaster_wall"]
RES = "1k"


def load_target():
    return json.load(open(TARGET_JSON, encoding="utf-8"))


def ritas(T):
    return next(s for s in T["shops"] if s["id"] == "ritas")


def model_ids(T):
    """Every Poly Haven model Rita's room and display place (target.json), sorted."""
    r = ritas(T)
    ids = {g["model"] for g in r["room"]["goods"] if not g["model"].startswith("script:")}
    ids |= {i["model"] for i in r["display"]["items"]}
    return sorted(ids)


def _fetcher():
    path = os.path.join(REPO, "tools", "art-recipes", "fetch_polyhaven.py")
    spec = importlib.util.spec_from_file_location("fetch_polyhaven", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def fetch(ids=None, log=print):
    T = load_target()
    fp = _fetcher()
    ids = list(ids or (model_ids(T) + TEXTURES))
    os.makedirs(POLY, exist_ok=True)
    total = 0
    for a in ids:
        root = os.path.join(POLY, a, RES)
        if os.path.exists(os.path.join(root, "source.json")):
            continue
        for attempt in range(3):
            try:
                kind, n, size = fp.fetch(a, RES, POLY)
                total += size
                log("fetched %s (%s, %d files, %.1f MB)" % (a, kind, n, size / 1e6))
                break
            except Exception as e:  # network resets happen: try again, then say
                log("fetch %s try %d failed: %s" % (a, attempt + 1, e))
    return total


def gltf_path(asset, clean=True):
    folder = os.path.join(POLY, asset, RES)
    if clean:
        c = os.path.join(folder, asset + "_clean.gltf")
        if os.path.exists(c):
            return c
    return next((os.path.join(folder, f) for f in sorted(os.listdir(folder)) if f.endswith(".gltf") and not f.endswith("_clean.gltf")), None)


def base_maps(asset):
    """The base-colour image files a model's glTF names (paths relative to its folder, once each)."""
    g = json.load(open(gltf_path(asset, clean=False), encoding="utf-8"))
    out = []
    for m in g.get("materials", []):
        t = m.get("pbrMetallicRoughness", {}).get("baseColorTexture")
        if t is not None:
            img = g["textures"][t["index"]]["source"]
            if g["images"][img]["uri"] not in out:
                out.append(g["images"][img]["uri"])
    return out


def map_path(asset, name):
    """The relative path (as the glTF writes it) of the image whose file name is `name`."""
    g = json.load(open(gltf_path(asset, clean=False), encoding="utf-8"))
    for im in g["images"]:
        if os.path.basename(im["uri"]) == name:
            return im["uri"]
    raise KeyError("%s has no image %s" % (asset, name))


# ------------------------------------------------------------------ contact sheets (step 0)
def sheets(ids=None, per=12, tile=512, log=print):
    T = load_target()
    ids = ids or model_ids(T)
    os.makedirs(os.path.join(WORK, "sheets"), exist_ok=True)
    items = []
    for a in ids:
        for m in base_maps(a):
            items.append((a, m))
    font = ImageFont.load_default()
    n = 0
    for s in range(0, len(items), per):
        part = items[s:s + per]
        cols = 4
        rows = (len(part) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * tile, rows * (tile + 14)), (40, 40, 40))
        d = ImageDraw.Draw(sheet)
        for k, (a, m) in enumerate(part):
            im = Image.open(os.path.join(POLY, a, RES, m)).convert("RGB").resize((tile, tile), Image.LANCZOS)
            x, y = (k % cols) * tile, (k // cols) * (tile + 14)
            sheet.paste(im, (x, y + 14))
            d.text((x + 2, y + 1), (a + " | " + m)[:90], fill=(255, 255, 0), font=font)
        p = os.path.join(WORK, "sheets", "sheet_%02d.jpg" % (s // per))
        sheet.save(p, quality=88)
        n += 1
    log("contact sheets: %d (%d maps)" % (n, len(items)))
    return n


# ------------------------------------------------------------------ the blanking step
def _ring(arr, box, w=6):
    h, wd = arr.shape[:2]
    x0, y0, x1, y1 = box
    X0, Y0, X1, Y1 = max(0, x0 - w), max(0, y0 - w), min(wd, x1 + w), min(h, y1 + w)
    m = np.ones((Y1 - Y0, X1 - X0), bool)
    m[(y0 - Y0):(y1 - Y0), (x0 - X0):(x1 - X0)] = False
    patch = arr[Y0:Y1, X0:X1][m]
    return np.median(patch, axis=0)


def _clean_patch(arr, box, boxes, rng):
    """A same-size patch of the map's own grain from the nearest area that is clear of every listed box and close in colour to the ring."""
    h, wd = arr.shape[:2]
    x0, y0, x1, y1 = box
    bw, bh = x1 - x0, y1 - y0
    ring = _ring(arr, box)

    def clear(a, b, c, d):
        if a < 0 or b < 0 or c > wd or d > h:
            return False
        for (u0, v0, u1, v1) in boxes:
            if not (c <= u0 - 4 or a >= u1 + 4 or d <= v0 - 4 or b >= v1 + 4):
                return False
        return True
    best = None
    for r in range(1, 40):
        for dx, dy in ((0, -r), (0, r), (-r, 0), (r, 0), (-r, -r), (r, -r), (-r, r), (r, r)):
            a, b = x0 + dx * (bw + 6) // 2, y0 + dy * (bh + 6) // 2
            if clear(a, b, a + bw, b + bh):
                p = arr[b:b + bh, a:a + bw]
                dist = float(np.abs(np.median(p.reshape(-1, p.shape[-1]), axis=0) - ring).max())
                if dist < 40:
                    return a, b
                if best is None or dist < best[0]:
                    best = (dist, a, b)
        if best is not None and r > 6:
            break
    if best is None:
        return None
    return best[1], best[2]


def blank_map(src, dst, boxes, whole_map_print=None, seed=1):
    """Paint the boxes of one map to their ring colour plus the map's own grain. Returns the report rows."""
    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    out = arr.copy()
    rows = []
    rng = np.random.default_rng(seed)
    for box in boxes:
        x0, y0, x1, y1 = box
        ring = _ring(arr, box)
        pos = _clean_patch(arr, box, boxes, rng)
        fill = np.empty((y1 - y0, x1 - x0, 3), np.float32)
        fill[:] = ring
        if pos is not None:
            a, b = pos
            p = arr[b:b + (y1 - y0), a:a + (x1 - x0)]
            # the grain only: the patch minus its own broad level (a 9 px blur), so the box keeps the ring's colour
            pim = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
            grain = p - np.asarray(pim).astype(np.float32)
            fill = fill + np.clip(grain, -18, 18)
        out[y0:y1, x0:x1] = fill
        rows.append({"box": box, "ring": [round(float(c), 1) for c in ring], "patch_from": pos})
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, quality=95, subsampling=0)
    return rows


def invented_print(path, kind, size=1024, seed=1):
    """The project's own invented print for a picture frame (a made-up coastal view: sea, a headland, a sail, a sky), painted by script:
    no photograph, no real place, no person. Three kinds so the three frames differ."""
    rng = np.random.default_rng(seed)
    w = size
    y = np.linspace(0, 1, w)[:, None]
    x = np.linspace(0, 1, w)[None, :]
    sky_top = np.array([[0.42, 0.55, 0.70], [0.78, 0.62, 0.45], [0.55, 0.60, 0.62]][kind % 3])
    sky_low = np.array([[0.86, 0.84, 0.76], [0.95, 0.80, 0.55], [0.82, 0.82, 0.78]][kind % 3])
    sea = np.array([[0.16, 0.28, 0.36], [0.20, 0.25, 0.30], [0.18, 0.30, 0.34]][kind % 3])
    hor = 0.55 + 0.05 * (kind % 3)
    img = np.zeros((w, w, 3))
    t = np.clip(y / hor, 0, 1)
    for c in range(3):
        img[:, :, c] = np.where(y < hor, sky_top[c] * (1 - t) + sky_low[c] * t, sea[c] * (1 - 0.35 * ((y - hor) / (1 - hor))))
    # a headland and a sail, flat-painted
    hx = 0.15 + 0.2 * (kind % 3)
    land = (y > hor - 0.07 * np.exp(-((x - hx) / 0.18) ** 2)) & (y < hor + 0.004)
    img[land] = np.array([0.20, 0.24, 0.18])
    sx = 0.62 - 0.1 * (kind % 3)
    sail = (np.abs(x - sx) < 0.06 * (hor + 0.06 - y) / 0.16) & (y > hor - 0.16) & (y < hor + 0.01)
    img[sail] = np.array([0.90, 0.88, 0.80])
    hull = (np.abs(x - sx) < 0.07) & (y >= hor + 0.01) & (y < hor + 0.025)
    img[hull] = np.array([0.15, 0.10, 0.08])
    # a little paint grain and a brush wobble so it is not a flat vector
    img += rng.normal(0, 0.012, img.shape)
    wob = (np.sin(y * 90 + rng.random() * 6) * 0.01)[:, :, None]
    img += wob
    Image.fromarray((np.clip(img, 0, 1) * 255).astype(np.uint8)).save(path, quality=92)


def blank(ids=None, log=print):
    """Apply every blanking entry of target.json to the maps of the given models. Returns {asset: report}."""
    T = load_target()
    inv = T["inventory"]["polyhaven"]
    ids = ids or model_ids(T)
    report = {}
    for a in ids:
        e = inv[a]
        entries = e.get("blank") or []
        folder = os.path.join(POLY, a, RES)
        g = json.load(open(gltf_path(a, clean=False), encoding="utf-8"))
        rep = []
        if entries:
            by_map = {}
            for b in entries:
                by_map.setdefault(b["map"], []).append(b)
            for mp, bl in by_map.items():
                rel = map_path(a, mp)
                src = os.path.join(folder, rel)
                clean_name = os.path.splitext(mp)[0] + "_clean.jpg"
                dst = os.path.join(folder, os.path.dirname(rel), clean_name)
                boxes = [bx for b in bl for bx in b["boxes"]]
                if boxes == [[0, 0, 1024, 1024]]:
                    kind = {"hanging_picture_frame_02": 0, "standing_picture_frame_01": 1, "standing_picture_frame_02": 2}.get(a, 0)
                    invented_print(dst, kind)
                    rows = [{"box": boxes[0], "whole_map": True, "replaced_by": "invented_print(kind=%d)" % kind}]
                else:
                    rows = blank_map(src, dst, boxes, seed=int(hashlib.md5(a.encode()).hexdigest()[:6], 16))
                rep.append({"map": mp, "clean": clean_name, "rows": rows})
                for im in g["images"]:
                    if os.path.basename(im["uri"]) == mp:
                        im["uri"] = os.path.join(os.path.dirname(im["uri"]), clean_name).replace(os.sep, "/")
            json.dump(g, open(os.path.join(folder, a + "_clean.gltf"), "w"), indent=1)
            log("blanked %s: %s" % (a, ", ".join(r["map"] for r in rep)))
        report[a] = rep
    os.makedirs(WORK, exist_ok=True)
    json.dump(report, open(os.path.join(WORK, "blanking_report.json"), "w"), indent=1)
    return report


def verify(log=print):
    """INV-06's script test on each final box of every model with a blanking entry. Returns rows (id, ok, detail)."""
    T = load_target()
    inv = T["inventory"]["polyhaven"]
    rows = []
    for a in model_ids(T):
        for b in inv[a].get("blank") or []:
            folder = os.path.join(POLY, a, RES)
            rel = map_path(a, b["map"])
            orig = os.path.join(folder, rel)
            clean = os.path.join(folder, os.path.dirname(rel), os.path.splitext(b["map"])[0] + "_clean.jpg")
            if b["boxes"] == [[0, 0, 1024, 1024]]:
                h1 = hashlib.md5(open(orig, "rb").read()).hexdigest()
                h2 = hashlib.md5(open(clean, "rb").read()).hexdigest()
                g = json.load(open(gltf_path(a), encoding="utf-8"))
                points = any(os.path.basename(i["uri"]) == os.path.basename(clean) for i in g["images"])
                rows.append({"id": "INV-06 %s %s (whole map)" % (a, b["map"]), "ok": h1 != h2 and points, "detail": "hash differs: %s; glTF points at the print: %s" % (h1 != h2, points)})
                continue
            arr0 = np.asarray(Image.open(orig).convert("RGB")).astype(np.float32)
            arr1 = np.asarray(Image.open(clean).convert("RGB")).astype(np.float32)
            g = json.load(open(gltf_path(a), encoding="utf-8"))
            points = any(os.path.basename(i["uri"]) == os.path.basename(clean) for i in g["images"])
            for box in b["boxes"]:
                x0, y0, x1, y1 = box
                ring = _ring(arr0, box)
                patch = arr1[y0:y1, x0:x1]
                maxdiff = float(np.abs(patch - ring).max())
                gy, gx = np.gradient(patch.mean(axis=2))
                grad = np.hypot(gx, gy)
                share = float((grad > 40).mean())
                ok = maxdiff <= 24.0 and share < 0.02 and points
                rows.append({"id": "INV-06 %s %s %s" % (a, b["map"], box), "ok": bool(ok),
                             "detail": "largest difference from the ring %.1f (limit 24); gradient above 40 on %.2f%% (limit 2); glTF points at the clean map: %s" % (maxdiff, share * 100, points)})
    return rows


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "fetch"
    if cmd == "fetch":
        fetch()
    elif cmd == "sheets":
        sheets()
    elif cmd == "blank":
        blank()
    elif cmd == "verify":
        r = verify()
        print("%d of %d rows pass" % (sum(1 for x in r if x["ok"]), len(r)))
        for x in r:
            if not x["ok"]:
                print("FAIL", x["id"], x["detail"])
