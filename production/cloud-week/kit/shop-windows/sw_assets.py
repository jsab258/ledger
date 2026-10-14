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
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
SCRATCH = os.environ.get("LEDGER_SW_SCRATCH", "/home/user/ledger-scratch")
POLY = os.environ.get("LEDGER_POLYHAVEN", os.path.join(SCRATCH, "polyhaven"))
WORK = os.path.join(SCRATCH, "shop-windows")
TARGET_JSON = os.path.join(REPO, "production", "cloud-week", "targets", "shop-windows", "target.json")
TEXTURES = ["old_linoleum_flooring_01", "painted_plaster_wall"]       # Rita's room (the other shops' are TEXTURES_OF)
RES = "1k"
CURRENT = "ritas"             # the shop this process builds (build_shop.py sets it): model_ids, fetch, blank and verify work on that shop's room and display
# the Poly Haven textures each shop's room lays (the target's room.floor names them: Rita's lino and the tea room's chequer share a map)
TEXTURES_OF = {"ritas": ["old_linoleum_flooring_01", "painted_plaster_wall"], "ironmonger": ["old_wooden_floor_03", "painted_plaster_wall"],
               "newsagent": ["rubber_tiles", "painted_plaster_wall"], "tea_rooms": ["old_linoleum_flooring_01", "painted_plaster_wall"],
               # batch B (14 October): the launderette's grey vinyl and white tile dado, the grocer's brown lino, the chandler's oiled boards, the fish market's quarry floor and white tiled walls (and the marble slab)
               "steam_laundry": ["rubber_tiles", "painted_plaster_wall", "long_white_tiles"], "grocer": ["linoleum_brown", "painted_plaster_wall"],
               "chandler": ["old_wooden_floor_02", "painted_plaster_wall"], "fish_market": ["terracotta_floor_tiles", "long_white_tiles", "marble_01"]}


def set_shop(shop_id):
    global CURRENT
    CURRENT = shop_id


# Marks the builder found at 1k that the target's list does not have (step 0, looked at every map): applied the same way, reported in NOTES.md
# for the target's owner to add to inventory.texture_marks. Boxes in pixels of the 1k base-colour map, [x0, y0, x1, y1].
EXTRA_BLANK = {
    "cardboard_box_01": [{"map": "cardboard_box_01_diff_1k.jpg", "boxes": [[185, 190, 395, 350], [395, 255, 505, 365], [250, 360, 375, 465]],
                          "fill": "the cardboard's own tan", "reads": "'no sharp instruments to open', 'Keep Out of Reach of Children' (the children rule), the two handling pictograms and 'Recommended storage below 30 C'"}],
    "pliers": [{"map": "pliers_diff_1k.jpg", "boxes": [[146, 530, 196, 778]],
                "fill": "the handle's red", "reads": "'160 mm', the VDE and GS approval marks and '1000 V' (German certification marks, a modern insulated tool)"}],
    "seadogs_compass": [{"map": "seadogs_compass_diff_1k.jpg", "boxes": [[560, 230, 615, 335], [650, 225, 735, 350]],
                         "fill": "the brass ring's brown", "reads": "'LONDON 1965' and the maker's name 'RADOLIER' stamped on the bezel ring"}],
    # found on the second pass, every map of the 45 models at 1:1 to 2:1 in halves (the first pass was contact sheets at 512 px, which a 10 px word does not show on)
    "metal_toolbox": [{"map": "metal_toolbox_diff_1k.jpg", "boxes": [[209, 59, 237, 82]],
                       "fill": "the badge's own grey", "reads": "a word stamped round the toolbox's badge in red ('STEELIN...' and a number): a maker's badge"}],
    "filmstrip_projector_8mm": [{"map": "filmstrip_projector_8mm_diff_1k.jpg", "boxes": [[444, 560, 472, 632], [440, 672, 476, 726]],
                                 "fill": "the control plate's dark brown", "reads": "'PROJECTOMAT GPP' (the model name, gilt, upright) and the control legends under it"}],
    "vintage_video_camera": [{"map": "vintage_video_camera_diff_1k.jpg", "boxes": [[614, 251, 648, 263], [775, 633, 788, 661], [766, 975, 776, 1008]],
                              "fill": "the strip's grey", "reads": "'PH-JNL' three times on the lens strips (the maker the target already lists for this model as 'PH JNL 7' and 'PH.JNL - OPTICAL CO., LTD')"}],
    "portable_cassette_player": [{"map": "portable_cassette_player_diff_1k.jpg", "boxes": [[555, 965, 586, 1022], [954, 618, 970, 666]],
                                  "fill": "the case's grey-green", "reads": "a name plate ('NORT-o-ORUM' in bold, three lines of serial small print) and a model number 'ST7242 MI NA'"}],
    "Camera_01": [{"map": "Camera_01_strap_diff_1k.jpg", "boxes": [[632, 840, 712, 874]],
                   "fill": "the strap leather's brown", "reads": "'INGRID' handwritten in red on the strap (a person's name)"},
                  {"map": "Camera_01_body_diff_1k.jpg", "boxes": [[792, 626, 830, 652]],
                   "fill": "the body's black", "reads": "'DEP' (the German registered-design mark), printed mirrored below the first plate; the target's box for 'DEP' is 8 px above it"}],
    "hand_plane_no4": [{"map": "hand_plane_no4_diff_1k.jpg", "boxes": [[804, 272, 847, 292]],
                        "fill": "the casting's brown", "reads": "a small stamped plate, five letters, mirrored, 5 px high (a maker's or pattern stamp)"}],
    # batch A (13 Oct, 2026): found at 1k on the ironmonger's models, every map at 1:1 (the target's list lacks them)
    "wooden_hammer_01": [{"map": "wooden_hammer_01_diff_1k.jpg", "boxes": [[340, 232, 392, 292]],
                          "fill": "the head's grey", "reads": "a maker's logo stamped on the head (a letter P in a rounded frame with a registered-mark sign)"}],
    "trowel_01": [{"map": "trowel_01_diff_1k.jpg", "boxes": [[672, 585, 752, 625]],
                   "fill": "the blade's grey-pink", "reads": "a stamped word on the blade, mirrored ('Yokis' or 'Yoks': a maker's name)"}],
    "ratchet_wrench": [{"map": "ratchet_wrench_diff_1k.jpg", "boxes": [[210, 548, 440, 578]],
                        "fill": "the steel's pale grey", "reads": "an engraved line of three words and a year (a maker's inscription and '2016': after 1992)"}],
    "small_oil_can_01": [{"map": "small_oil_can_01_diff_1k.jpg", "boxes": [[538, 150, 630, 245]],
                          "fill": "the can's red", "reads": "a flame hazard diamond in the EU's modern (CLP) form: after 1992"}],
    "stationery_supplies": [{"map": "stationery_supplies_diff_1k.jpg", "boxes": [[244, 142, 344, 166], [200, 364, 312, 388], [524, 314, 652, 338]],
                             "fill": "each band's own colour (the stripes' yellow, the pencil's yellow, the red)", "reads": "'Haven Penworks' and the grade (2H, BUDGET, 6B) printed on three pencils (a maker's name)"}],
    # batch B (14 Oct, 2026): the chandler's rubber boots carry the two MICKY badges on the DIRTY variant's map as well (the target's boxes are for the clean map only)
    "rubber_boots": [{"map": "rubber_boots_dirty_diff_1k.jpg", "boxes": [[446, 48, 506, 74], [648, 398, 706, 424]],
                      "fill": "the boot's dark green", "reads": "MICKY (two badges) on the dirty variant's map, at 8 x: a rounded frame round the word"}],
    "sledgehammer_01": [{"map": "sledgehammer_01_diff_1k.jpg", "boxes": [[14, 400, 104, 596]],
                         "fill": "the handle's yellow", "reads": "a warning label: a column of small print and 'WARN...' (modern safety text)"}],
}


# Target boxes tightened where the target's box is wider than the print and straddles two surfaces (the fill would then be a median of two
# colours): {(model, map): {target box: tighter box that still holds every glyph}}. Looked at 100 per cent beside the original.
BOX_FIX = {("vintage_pocket_watch", "vintage_pocket_watch_diff_1k.jpg"): {(620, 630, 765, 790): [640, 664, 694, 762]},
           # batch B: the lifebuoy's second box ('PH . SA . 20', rotated) overlaps the third (the white band) by 6 rows, so the strip took the band's grey and failed INV-06's ring test; it starts below the
           # overlap and runs 23 rows lower to take the last letters ('GIT' at 3 x), which stood past its foot
           ("lifebuoy", "lifebuoy_diff_1k.jpg"): {(630, 690, 782, 902): [630, 697, 782, 925]},
           # batch A (13 Oct): the target's one box [0, 20, 840, 420] over the stationery map's four coloured pencil bands cannot pass its own script test (the four bands' colours differ by up to 40 from one ring
           # colour); the four lettered places are boxed one each (this one, and three in EXTRA_BLANK), each inside one band
           ("stationery_supplies", "stationery_supplies_diff_1k.jpg"): {(0, 20, 840, 420): [398, 100, 500, 124]}}


# Where the ring just outside a box is mostly another surface than the print's own, the target's stated sampled fill is used instead of the ring's median:
# {(model, box): (r, g, b)}. The box's own test in verify() then compares with that fill.
FILL_OVERRIDE = {("vintage_pocket_watch", (640, 664, 694, 762)): (180, 182, 184),
                 # the video camera's lens strips are light grey bands 12 to 14 px wide between dark rows: the ring would take the dark rows' median
                 ("vintage_video_camera", (614, 251, 648, 263)): (138, 142, 142),
                 ("vintage_video_camera", (775, 633, 788, 661)): (138, 140, 139)}


def entries(T, a):
    out = []
    for e in T["inventory"]["polyhaven"][a].get("blank") or []:
        e = dict(e)
        fix = BOX_FIX.get((a, e["map"]), {})
        e["boxes"] = [fix.get(tuple(b), b) for b in e["boxes"]]
        out.append(e)
    return out + list(EXTRA_BLANK.get(a, []))


def load_target():
    return json.load(open(TARGET_JSON, encoding="utf-8"))


def ritas(T):
    """The record of the shop this process builds (the name is the kit's old one; it is Rita's unless set_shop() said otherwise)."""
    return next(s for s in T["shops"] if s["id"] == CURRENT)


def model_ids(T):
    """Every Poly Haven model the current shop's room and display place (target.json), sorted."""
    r = ritas(T)
    ids = {g["model"] for g in (r.get("room") or {}).get("goods", []) if not g["model"].startswith("script:")}
    ids |= {i["model"] for i in (r.get("display") or {}).get("items", []) if not i["model"].startswith("script:")}
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
    ids = list(ids or (model_ids(T) + TEXTURES_OF.get(CURRENT, [])))
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


def fetch_all(log=print):
    fetch(log=log)
    fetch_print_sources(log=log)


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


def _grain(p):
    """A patch's grain: the patch minus its own broad level (a 4 px blur)."""
    pim = Image.fromarray(np.clip(p, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(4))
    return p - np.asarray(pim).astype(np.float32)


def _edge_share(p):
    gy, gx = np.gradient(p.mean(axis=2))
    return float((np.hypot(gx, gy) > 14).mean())


def _clean_patch(arr, box, boxes, rng):
    """A same-size patch of the map's own grain from the nearest area that is clear of every listed box, close in colour to the ring, and
    itself free of print and edges (a patch that carries numerals or a scale would only move the lettering). None when the map has no such
    area near: the caller then draws grain of the ring's own strength."""
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
    for r in range(1, 60):
        for dx, dy in ((0, -r), (0, r), (-r, 0), (r, 0), (-r, -r), (r, -r), (-r, r), (r, r)):
            a, b = x0 + dx * (bw + 6) // 2, y0 + dy * (bh + 6) // 2
            if not clear(a, b, a + bw, b + bh):
                continue
            p = arr[b:b + bh, a:a + bw]
            dist = float(np.abs(np.median(p.reshape(-1, p.shape[-1]), axis=0) - ring).max())
            if dist < 30 and _edge_share(p) < 0.0015:
                return a, b
    return None


def blank_map(src, dst, boxes, whole_map_print=None, seed=1, fills=None, grain_scale=1.0):
    """Paint the boxes of one map to their ring colour plus the map's own grain. Returns the report rows."""
    img = Image.open(src).convert("RGB")
    arr = np.asarray(img).astype(np.float32)
    out = arr.copy()
    rows = []
    rng = np.random.default_rng(seed)
    for box in boxes:
        x0, y0, x1, y1 = box
        ring = _ring(arr, box)
        if fills and tuple(box) in fills:
            ring = np.array(fills[tuple(box)], np.float32)
        pos = _clean_patch(arr, box, boxes, rng)
        fill = np.empty((y1 - y0, x1 - x0, 3), np.float32)
        fill[:] = ring
        if pos is not None:
            a, b = pos
            grain = _grain(arr[b:b + (y1 - y0), a:a + (x1 - x0)])
            how = "the map's own grain from the patch at %s" % (pos,)
        else:
            # no clean area near: grain of the ring's own strength (the ring is the print-free pixels just outside the box)
            h, wd = arr.shape[:2]
            X0, Y0, X1, Y1 = max(0, x0 - 8), max(0, y0 - 8), min(wd, x1 + 8), min(h, y1 + 8)
            rp = _grain(arr[Y0:Y1, X0:X1])
            m = np.ones(rp.shape[:2], bool)
            m[(y0 - Y0):(y1 - Y0), (x0 - X0):(x1 - X0)] = False
            sd = np.clip(np.median(np.abs(rp[m]), axis=0) * 1.4826, 1.0, 9.0)
            grain = rng.normal(0.0, 1.0, (y1 - y0, x1 - x0, 3)).astype(np.float32) * sd
            grain = np.asarray(Image.fromarray(np.clip(grain + 128, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.8))).astype(np.float32) - 128
            how = "grain drawn at the ring's strength (%s)" % ", ".join("%.1f" % v for v in sd)
        fill = fill + np.clip(grain * grain_scale, -13, 13)
        out[y0:y1, x0:x1] = fill
        rows.append({"box": box, "ring": [round(float(c), 1) for c in ring], "patch_from": pos, "grain": how})
    Image.fromarray(np.clip(out + 0.5, 0, 255).astype(np.uint8)).save(dst, quality=98, subsampling=0)
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


# ---------------------------------------------------------------------------------------------------------------------------------- the frames' prints (13 Oct, try 2)
# Close review narrow 7: the invented prints read as flat clip-art. Each frame's print is now a crop of a CC0 Poly Haven HDRI of a harbour (Lake Pier, polyhaven.com/a/lake_pier,
# Alexander Scholten, CC0), looked at in a rectilinear view, tone-mapped, saturation 0.7, a slight warm cast, paper grain and a 6 mm white mount; no person is in the crops (looked at
# at 100 per cent). The catalogue line (CATALOGUE.md is outside this unit's folders): "lake_pier HDRI, CC0, Poly Haven: frame prints of Rita's shop (kit/shop-windows)".
HDRI_ID = "lake_pier"
PRINT_HDRI = os.path.join(POLY, "_hdri", "lake_pier_2k.hdr")
FABRIC_ID = "Fabric034"
FABRIC_DIR = os.path.join(POLY, "_acg", "Fabric034")
# per model: the print's box in the 1024 px artwork map (u0, v0, u1, v1 in 0..1, v up, read from the model's UVs) and the quad's size in metres (to size the 6 mm mount)
PRINT_MAP = {"standing_picture_frame_01": ((0.165, 0.002, 0.835, 0.998), (0.132, 0.186)),
             "standing_picture_frame_02": ((0.143, 0.005, 0.861, 0.995), (0.135, 0.185)),
             "hanging_picture_frame_02": ((0.007, 0.223, 0.993, 0.801), (0.605, 0.354))}
# the views (yaw degrees from the HDRI's centre, pitch, horizontal field): the hanging frame has five (the five frames on the pledge board differ), the standing ones one each
PRINT_VIEWS = {"hanging_picture_frame_02": [(-30, -3, 62), (22, -2, 56), (150, -2, 56), (4, 8, 66), (-160, -1, 56)],
               "standing_picture_frame_01": [(-12, -2, 38)], "standing_picture_frame_02": [(30, -1, 36)]}


def fetch_print_sources(log=print):
    """The HDRI of the frames' prints (Poly Haven, CC0) and the fabric normal map of the display's velvet (ambientCG Fabric034, CC0), into SCRATCH/polyhaven."""
    import subprocess
    os.makedirs(os.path.dirname(PRINT_HDRI), exist_ok=True)
    if not os.path.exists(PRINT_HDRI):
        meta = json.loads(subprocess.check_output(["curl", "-sS", "-m", "60", "https://api.polyhaven.com/files/%s" % HDRI_ID]))
        url = meta["hdri"]["2k"]["hdr"]["url"]
        subprocess.check_call(["curl", "-sS", "-m", "180", "-o", PRINT_HDRI, url])
        log("fetched HDRI %s (%d bytes)" % (HDRI_ID, os.path.getsize(PRINT_HDRI)))
    nrm = os.path.join(FABRIC_DIR, "Fabric034_1K-JPG_NormalGL.jpg")
    if not os.path.exists(nrm):
        os.makedirs(FABRIC_DIR, exist_ok=True)
        zp = os.path.join(FABRIC_DIR, "f.zip")
        subprocess.check_call(["curl", "-sS", "-L", "-m", "180", "-o", zp, "https://ambientcg.com/get?file=Fabric034_1K-JPG.zip"])
        import zipfile
        with zipfile.ZipFile(zp) as z:
            z.extract("Fabric034_1K-JPG_NormalGL.jpg", FABRIC_DIR)
        os.remove(zp)
        log("fetched ambientCG Fabric034 normal map")


def _load_hdri(path):
    import bpy
    im = bpy.data.images.load(path, check_existing=True)
    w, h = im.size
    px = np.empty(w * h * 4, np.float32)
    im.pixels.foreach_get(px)
    return px.reshape(h, w, 4)[::-1, :, :3].copy()             # row 0 at the top


def _rect_view(env, yaw_deg, pitch_deg, hfov_deg, out_w, out_h):
    """A rectilinear (pinhole) view of an equirectangular image: yaw, pitch and horizontal field in degrees; bilinear."""
    h, w = env.shape[:2]
    f = (out_w / 2.0) / np.tan(np.radians(hfov_deg) / 2.0)
    xs = (np.arange(out_w) + 0.5 - out_w / 2.0)
    ys = (np.arange(out_h) + 0.5 - out_h / 2.0)
    X, Y = np.meshgrid(xs, ys)
    d = np.stack([X / f, -Y / f, np.ones_like(X)], axis=-1)                # camera: +z forward, +y up
    d /= np.linalg.norm(d, axis=-1, keepdims=True)
    p, yv = np.radians(pitch_deg), np.radians(yaw_deg)
    Rp = np.array([[1, 0, 0], [0, np.cos(p), -np.sin(p)], [0, np.sin(p), np.cos(p)]])
    Ry = np.array([[np.cos(yv), 0, np.sin(yv)], [0, 1, 0], [-np.sin(yv), 0, np.cos(yv)]])
    d = d @ Rp.T @ Ry.T
    lon = np.arctan2(d[..., 0], d[..., 2])
    lat = np.arcsin(np.clip(d[..., 1], -1, 1))
    u = (lon / (2 * np.pi) + 0.5) * w - 0.5
    v = (0.5 - lat / np.pi) * h - 0.5
    out = np.stack([ndimage.map_coordinates(env[..., c], [v, u], order=1, mode="wrap") for c in range(3)], axis=-1)
    return out


def harbour_print(dst, asset, variant=0, seed=1):
    """The frame's print: a harbour view cropped from the HDRI to the print's own shape, tone-mapped, desaturated to 0.7, warmed a little, with paper grain and a 6 mm white mount,
    laid into the 1024 px artwork map where the model's UVs put the print (the rest of the map is white card). Falls back to the painted print if the HDRI is not there."""
    if not os.path.exists(PRINT_HDRI):
        return False
    box, quad = PRINT_MAP[asset]
    yaw, pitch, hfov = PRINT_VIEWS[asset][variant % len(PRINT_VIEWS[asset])]
    n = 1024
    c0, r0 = int(round(box[0] * n)), int(round((1 - box[3]) * n))
    c1, r1 = int(round(box[2] * n)), int(round((1 - box[1]) * n))
    pw, ph = c1 - c0, r1 - r0
    mount_px = max(2, int(round(0.006 / quad[0] * pw)))
    iw, ih = pw - 2 * mount_px, ph - 2 * mount_px
    env = _load_hdri(PRINT_HDRI)
    view = _rect_view(env, yaw, pitch, hfov, iw, ih)
    lum = 0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2]
    view = view * (0.22 / max(float(np.median(lum)), 1e-4))               # middle grey from the median
    view = view / (1.0 + view * 0.55)                                      # a soft shoulder
    view = np.clip(view, 0, 1) ** (1 / 2.2)
    g = (0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2])[..., None]
    view = g + (view - g) * 0.7                                            # saturation 0.7
    view = view * np.array([1.045, 1.0, 0.93])                             # a slight warm cast
    rng = np.random.default_rng(seed + variant)
    view = view + ndimage.gaussian_filter(rng.normal(0, 0.020, view.shape), (0.6, 0.6, 0)) + rng.normal(0, 0.006, view.shape)
    canvas = np.full((n, n, 3), 0.93, np.float32)
    canvas[r0:r1, c0:c1] = 0.96                                            # the mount
    canvas[r0 + mount_px:r1 - mount_px, c0 + mount_px:c1 - mount_px] = np.clip(view, 0, 1)
    # a hairline of shade where the mount's bevel meets the print
    canvas[r0 + mount_px - 1, c0 + mount_px:c1 - mount_px] *= 0.82
    canvas[r0 + mount_px:r1 - mount_px, c0 + mount_px - 1] *= 0.86
    Image.fromarray((np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8)).save(dst, quality=94, subsampling=0)
    return True


def blank(ids=None, log=print):
    """Apply every blanking entry of target.json to the maps of the given models. Returns {asset: report}."""
    T = load_target()
    inv = T["inventory"]["polyhaven"]
    ids = ids or model_ids(T)
    report = {}
    for a in ids:
        entries = globals()["entries"](T, a)
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
                    if a in PRINT_MAP and harbour_print(dst, a, 0):
                        rows = [{"box": boxes[0], "whole_map": True, "replaced_by": "harbour_print: a crop of the CC0 Poly Haven HDRI %s (yaw %d, pitch %d, field %d)" % ((HDRI_ID,) + PRINT_VIEWS[a][0])}]
                        for k in range(1, len(PRINT_VIEWS[a])):          # the hanging frame's other four prints (the five frames on the pledge board differ)
                            harbour_print(os.path.splitext(dst)[0] + "_v%d.jpg" % k, a, k)
                    else:
                        invented_print(dst, kind)
                        rows = [{"box": boxes[0], "whole_map": True, "replaced_by": "invented_print(kind=%d)" % kind}]
                else:
                    fills = {k[1]: v for k, v in FILL_OVERRIDE.items() if k[0] == a}
                    rows = blank_map(src, dst, boxes, seed=int(hashlib.md5(a.encode()).hexdigest()[:6], 16), fills=fills)
                rep.append({"map": mp, "clean": clean_name, "rows": rows})
                for im in g["images"]:
                    if os.path.basename(im["uri"]) == mp:
                        im["uri"] = os.path.join(os.path.dirname(im["uri"]), clean_name).replace(os.sep, "/")
                # the same boxes on the model's normal and roughness maps: engraved and embossed lettering (the till's plates, the boombox's legends) lives in the relief, which the
                # target says a print does not have; found at 100 per cent in the first render (13 October), so the relief inside each box goes flat too
                if "_diff_" in mp and boxes != [[0, 0, 1024, 1024]]:
                    for kind in ("nor_gl", "arm"):
                        comp = mp.replace("_diff_", "_%s_" % kind)
                        try:
                            crel = map_path(a, comp)
                        except KeyError:
                            continue
                        cdst_name = os.path.splitext(comp)[0] + "_clean.jpg"
                        blank_map(os.path.join(folder, crel), os.path.join(folder, os.path.dirname(crel), cdst_name), boxes, seed=int(hashlib.md5((a + kind).encode()).hexdigest()[:6], 16), grain_scale=0.5)
                        rep.append({"map": comp, "clean": cdst_name, "rows": [{"box": b_, "companion_of": mp} for b_ in boxes]})
                        for im in g["images"]:
                            if os.path.basename(im["uri"]) == comp:
                                im["uri"] = os.path.join(os.path.dirname(im["uri"]), cdst_name).replace(os.sep, "/")
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
        for b in entries(T, a):
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
                ring = np.array(FILL_OVERRIDE.get((a, tuple(box)), _ring(arr0, box)), np.float32)
                patch = arr1[y0:y1, x0:x1]
                maxdiff = float(np.abs(patch - ring).max())
                gy, gx = np.gradient(patch.mean(axis=2))
                grad = np.hypot(gx, gy)
                share = float((grad > 40).mean())
                ok = maxdiff <= 24.0 and share < 0.02 and points
                rows.append({"id": "INV-06 %s %s %s" % (a, b["map"], box), "ok": bool(ok),
                             "detail": "largest difference from the ring %.1f (limit 24); gradient above 40 on %.2f%% (limit 2); glTF points at the clean map: %s" % (maxdiff, share * 100, points)})
    # the companion maps (normal, roughness): the same boxes, the same test
    for a in model_ids(T):
        for b in entries(T, a):
            if "_diff_" not in b["map"] or b["boxes"] == [[0, 0, 1024, 1024]]:
                continue
            folder = os.path.join(POLY, a, RES)
            for kind in ("nor_gl", "arm"):
                comp = b["map"].replace("_diff_", "_%s_" % kind)
                try:
                    rel = map_path(a, comp)
                except KeyError:
                    continue
                orig = os.path.join(folder, rel)
                clean = os.path.join(folder, os.path.dirname(rel), os.path.splitext(comp)[0] + "_clean.jpg")
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
                    share = float((np.hypot(gx, gy) > 40).mean())
                    ok = maxdiff <= 24.0 and share < 0.02 and points
                    rows.append({"id": "INV-06 %s %s %s (relief)" % (a, comp, box), "ok": bool(ok), "detail": "largest difference from the ring %.1f; gradient above 40 on %.2f%%; glTF points at it: %s" % (maxdiff, share * 100, points)})
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


def models_table(placed_json, display_json):
    """A markdown table of every model placed (room and display), with its Poly Haven page, licence read from its source.json and what was blanked (verify_display_sources.py's method:
    each asset's own source.json must be present, CC0, and from polyhaven.com)."""
    T = load_target()
    placed = json.load(open(placed_json))
    disp = json.load(open(display_json))
    room_n, disp_n = {}, {}
    for p in placed:
        room_n[p["model"]] = room_n.get(p["model"], 0) + 1
    for i in disp["items"]:
        disp_n[i["model"]] = disp_n.get(i["model"], 0) + 1
    rows = ["| model | Poly Haven page | licence | in the room | in the display | maker's marks painted out |", "|---|---|---|---|---|---|"]
    bad = []
    for a in sorted(set(room_n) | set(disp_n)):
        p = os.path.join(POLY, a, RES, "source.json")
        src = json.load(open(p)) if os.path.exists(p) else None
        lic = (src or {}).get("licence", "?")
        page = (src or {}).get("page", "?")
        if not src or "CC0" not in lic or "polyhaven.com" not in page:
            bad.append(a)
        ent = entries(T, a)
        marks = ("; ".join(dict.fromkeys(e["reads"].replace("|", "/") for e in ent))[:300]) if ent else "none found"
        rows.append("| %s | %s | %s | %d | %d | %s |" % (a, page, lic, room_n.get(a, 0), disp_n.get(a, 0), marks))
    return "\n".join(rows), bad
