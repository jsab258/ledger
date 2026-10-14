"""The Poly Haven models and textures of the thirteen rooms: fetched at 1k (CC0), every base colour looked at at 100 per cent, the marks painted out by script, the framed pictures' artwork
replaced by prints cropped from CC0 photographs (HDRIs).

Run by build_windows.py (stage `assets`). Needs bpy only for the print crops (Blender loads the .hdr).

  fetch()       the ids of target.json inventory.polyhaven_models `used_in_rooms` and the nine textures, at 1k, into SCRATCH/polyhaven (never in the repository)
  blank()       MARKS: each box takes the median of a 6 px ring just outside it plus the map's own grain (hw_assets.blank_map); the model's normal and roughness maps get the same boxes (engraved
                lettering lives in the relief); <map>_clean.jpg beside the map, <id>_clean.gltf pointing at it
  print_map()   a framed picture's artwork map: a crop of a CC0 HDRI (tone-mapped, saturation 0.7, a slight warm cast, paper grain, a 6 mm mount) laid where the model's UVs put the picture

What was looked at, and where, is in NOTES.md (14 October, every base colour map of every placed model at 100 per cent, the suspicious regions at 3 to 5 times).
"""
import glob
import hashlib
import json
import os
import sys

import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_t as T  # noqa: E402
import hw_assets as A  # noqa: E402

A.POLY = T.POLY
A.RES = "1k"

# the marks found at 100 per cent (14 October 2026), boxes in pixels of the 1k base-colour map [x0, y0, x1, y1]
MARKS = {
    "television_02": [{"map": "television_02_diff_1k.jpg", "boxes": [[270, 450, 300, 548]], "fill": "the bezel's dark grey",
                       "reads": "'PARAGON' and 'Viewing System' lettered vertically on the front bezel, left of the buttons (the review of 13 October found it; confirmed at 5 times here)"}],
    "wall_clock": [{"map": "wall_clock_diff_1k.jpg", "boxes": [[246, 610, 316, 664]], "fill": "the dial's white",
                    "reads": "'URBAN' and 'quartz' on the dial under the 12 (a maker's name)"}],
}
# the pictures: every framed picture's artwork map is replaced (hanging_picture_frame_01 reads 'Ray Homes', _02 is a painting of a palace signed 'Celine.F', _03 a Japanese castle)
# the UV box of the picture on the model's map (u0, v0, u1, v1 with v up) and the picture's size in metres (read from the glTF in Blender, 14 October)
FRAME_ART = {"hanging_picture_frame_01": {"uv": (0.165, 0.002, 0.835, 0.998), "size_m": (0.5132, 0.7616), "oval": False},
             "hanging_picture_frame_02": {"uv": (0.007, 0.199, 0.993, 0.777), "size_m": (0.6041, 0.3540), "oval": False},
             "hanging_picture_frame_03": {"uv": (0.144, 0.003, 0.857, 0.994), "size_m": (0.2552, 0.3546), "oval": True}}
# the library of crops (CC0 photographs: Poly Haven HDRIs): (file, yaw, pitch, horizontal field degrees, short name). Chosen by eye from a contact sheet of the HDRIs: seascapes, a coast, a field and trees;
# no person, no sign, no modern building in any crop (looked at, 14 October)
HDRIS = {"lake_pier": os.path.join(T.SHARED_HDRI, "lake_pier_2k.hdr"), "dalkey_view": os.path.join(T.SHARED_HDRI, "dalkey_view_2k.hdr"),
         "blouberg_sunrise_1": os.path.join(T.SHARED_HDRI, "blouberg_sunrise_1_2k.hdr"), "belfast_open_field": T.SKY_HDRI}
LIBRARY = [("lake_pier", 25, 3, 52), ("lake_pier", 100, 2, 54), ("dalkey_view", 40, 0, 52), ("dalkey_view", 268, 1, 40), ("dalkey_view", 200, 5, 50), ("belfast_open_field", 0, 1, 48),
           ("belfast_open_field", 120, 3, 46), ("belfast_open_field", 300, 4, 46), ("blouberg_sunrise_1", 20, 1, 50), ("blouberg_sunrise_1", 60, 0, 52), ("dalkey_view", 118, 4, 44),
           ("belfast_open_field", 60, 3, 48)]
USED_MODELS = ["Shelf_01", "Sofa_01", "wooden_bookshelf_worn", "painted_wooden_bench", "vintage_cabinet_01", "wall_clock", "painted_wooden_cabinet", "vintage_oil_lamp", "side_table_01",
               "potted_plant_01", "television_02", "ornate_mirror_01", "mantel_clock_01", "hanging_picture_frame_01", "hanging_picture_frame_02", "hanging_picture_frame_03"]
TEXTURES = ["ceiling_interior", "decrepit_wallpaper", "dirty_carpet", "floral_jacquard", "linoleum_brown", "old_wooden_floor_02", "painted_plaster_wall", "peeling_painted_wall", "plastered_wall_04"]
_ENV = {}


def fetch(log=print):
    fp = A._fetcher()
    os.makedirs(T.POLY, exist_ok=True)
    for a in USED_MODELS + TEXTURES:
        if os.path.exists(os.path.join(T.POLY, a, "1k", "source.json")):
            continue
        for k in range(3):
            try:
                kind, n, size = fp.fetch(a, "1k", T.POLY)
                log("fetched %s (%s, %.1f MB)" % (a, kind, size / 1e6))
                break
            except Exception as e:
                log("fetch %s try %d failed: %s" % (a, k + 1, e))


def blank(log=print):
    rep = {}
    for a, entries in MARKS.items():
        folder = os.path.join(T.POLY, a, "1k")
        g = json.load(open(A.gltf_path(a, clean=False), encoding="utf-8"))
        rows = []
        for e in entries:
            rel = A.map_path(a, e["map"])
            src = os.path.join(folder, rel)
            dst = os.path.join(folder, os.path.dirname(rel), os.path.splitext(e["map"])[0] + "_clean.jpg")
            seed = int(hashlib.md5(a.encode()).hexdigest()[:6], 16)
            rows += A.blank_map(src, dst, e["boxes"], seed=seed)
            for im in g["images"]:
                if os.path.basename(im["uri"]) == e["map"]:
                    im["uri"] = os.path.join(os.path.dirname(im["uri"]), os.path.basename(dst)).replace(os.sep, "/")
            for kind in ("nor_gl", "arm"):
                comp = e["map"].replace("_diff_", "_%s_" % kind)
                try:
                    crel = A.map_path(a, comp)
                except KeyError:
                    continue
                cdst = os.path.join(folder, os.path.dirname(crel), os.path.splitext(comp)[0] + "_clean.jpg")
                A.blank_map(os.path.join(folder, crel), cdst, e["boxes"], seed=seed + 1, grain_scale=0.5)
                for im in g["images"]:
                    if os.path.basename(im["uri"]) == comp:
                        im["uri"] = os.path.join(os.path.dirname(im["uri"]), os.path.basename(cdst)).replace(os.sep, "/")
        json.dump(g, open(os.path.join(folder, a + "_clean.gltf"), "w"), indent=1)
        rep[a] = rows
        log("blanked %s" % a)
    os.makedirs(T.KITWORK, exist_ok=True)
    json.dump(rep, open(os.path.join(T.KITWORK, "blanking_report.json"), "w"), indent=1)
    return rep


def _env(name):
    if name not in _ENV:
        _ENV[name] = A._load_hdri(HDRIS[name])
    return _ENV[name]


def print_map(frame, k, dst, seed=3):
    """The artwork map for one placement of a frame: library crop k, laid into the model's picture box (the rest of the map is mount card)."""
    fa = FRAME_ART[frame]
    u0, v0, u1, v1 = fa["uv"]
    n = 1024
    c0, c1 = int(round(u0 * n)), int(round(u1 * n))
    r0, r1 = int(round((1 - v1) * n)), int(round((1 - v0) * n))
    pw, ph = c1 - c0, r1 - r0
    name, yaw, pitch, hfov = LIBRARY[k % len(LIBRARY)]
    mount = max(2, int(round(0.006 / fa["size_m"][0] * pw))) if not fa["oval"] else 0
    iw, ih = pw - 2 * mount, ph - 2 * mount
    # the crop keeps the picture's own proportions (the field is the horizontal one; a tall picture takes a narrower, taller view)
    view = A._rect_view(_env(name), yaw, pitch, hfov * (iw / float(ih)) if ih > iw else hfov, iw, ih)
    lum = 0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2]
    view = view * (0.22 / max(float(np.median(lum)), 1e-4))
    view = view / (1.0 + view * 0.55)
    view = np.clip(view, 0, 1) ** (1 / 2.2)
    g = (0.2126 * view[..., 0] + 0.7152 * view[..., 1] + 0.0722 * view[..., 2])[..., None]
    view = g + (view - g) * 0.62
    view = view * np.array([1.05, 1.0, 0.90])
    rng = np.random.default_rng(seed + k)
    from scipy import ndimage
    view = view + ndimage.gaussian_filter(rng.normal(0, 0.02, view.shape), (0.6, 0.6, 0)) + rng.normal(0, 0.006, view.shape)
    canvas = np.full((n, n, 3), 0.90, np.float32)
    if mount:
        canvas[r0:r1, c0:c1] = 0.95
    canvas[r0 + mount:r1 - mount, c0 + mount:c1 - mount] = np.clip(view, 0, 1)
    Image.fromarray((np.clip(canvas, 0, 1) * 255 + 0.5).astype(np.uint8)).save(dst, quality=94, subsampling=0)
    return {"frame": frame, "crop": k % len(LIBRARY), "source": name, "yaw": yaw, "pitch": pitch, "hfov": hfov}


def prepare(log=print):
    fetch(log)
    return blank(log)


if __name__ == "__main__":
    prepare()
