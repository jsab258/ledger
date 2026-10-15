"""Searches Poly Haven's British CC0 panoramas for a pillar box (9 October 2026): red-blob detection.

    /home/user/.bpyenv/bin/python -I scan_panoramas.py --dir DIR_FOR_DOWNLOADS [--out panorama_scan.json]

For each British panorama on api.polyhaven.com/assets?type=hdris (coordinates in Britain) it downloads the tone-mapped JPG into DIR
(an empty directory of your own: the files are untrusted data), reduces it to 4096 px wide and finds saturated red blobs (hue within 30
degrees of red, saturation above 0.68, value above 0.30, at least 80 px after a 2-pixel opening). Each blob was then looked at as a
rectilinear crop and by eye (the `looked_at` notes below are the writer's reading). A pillar box is a 0.5 x 1.4 m solid red object; at 10 m
it would be about 8 degrees tall, 90 px on this scale: far above the blob threshold.
The photographs are used for this search only: not placed in the game, not traced, not fed to an image model (Poly Haven: CC0).
"""
import argparse, json, os, sys, urllib.request
import numpy as np
from PIL import Image
from scipy import ndimage as ndi
Image.MAX_IMAGE_PIXELS = None

BRITISH = ["adams_place_bridge", "bethnal_green_entrance", "birbeck_street_underpass", "cambridge", "canary_wharf", "epping_forest_01", "epping_forest_02",
           "greenwich_park", "greenwich_park_02", "greenwich_park_03", "leadenhall_market", "limehouse", "roof_garden",
           "urban_street_01", "urban_street_02", "urban_street_03", "urban_street_04"]
LOOKED_AT = {
    "adams_place_bridge": "no red blobs; a glazed covered walkway",
    "bethnal_green_entrance": "blobs are brick gate piers and red tags on them; no post box in the eight views",
    "birbeck_street_underpass": "blobs are graffiti and brick under a railway arch; no post box",
    "cambridge": "no red blobs; a college court, no post box",
    "canary_wharf": "blobs are a lit ticker sign on a glass tower; no post box",
    "epping_forest_01": "woodland; no red", "epping_forest_02": "woodland; no red",
    "greenwich_park": "parkland; no red", "greenwich_park_02": "parkland; a few leaf-litter specks", "greenwich_park_03": "parkland; no red",
    "leadenhall_market": "hundreds of blobs: painted shopfronts and awnings of a covered market; the street furniture is bins and bollards; no post box",
    "limehouse": "blobs are brick courses and a red brick corner; boats and bollards; no post box",
    "roof_garden": "one tiny blob; a rooftop garden",
    "urban_street_01": "blobs are the tail lights of parked cars and a red-brick building; blue notice boards, bollards; no post box",
    "urban_street_02": "blobs are a purple wheelie bin (hue near red), brick, orange barrier panels behind railings; no post box",
    "urban_street_03": "blobs are the tail lights of two parked estate cars and a garden wall; a terraced street with no post box in eight views",
    "urban_street_04": "no red blobs; a stucco terrace in Notting Hill with no post box in eight views"}


def get(url, path):
    with urllib.request.urlopen(url, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", required=True)
    ap.add_argument("--out", default=os.path.join(os.path.dirname(os.path.abspath(__file__)), "panorama_scan.json"))
    a = ap.parse_args()
    os.makedirs(a.dir, exist_ok=True)
    res = {"date": "2026-10-09", "source": "https://api.polyhaven.com/files/<id> (tonemapped) for the ids below; CC0", "rule": "hue within 30 degrees of red, saturation > 0.68, value > 0.30, area >= 80 px at 4096 px wide",
           "panoramas": {}, "pillar_box_found": False}
    for pid in BRITISH:
        path = os.path.join(a.dir, pid + ".jpg")
        if not os.path.exists(path):
            meta = json.load(urllib.request.urlopen(f"https://api.polyhaven.com/files/{pid}", timeout=60))
            get(meta["tonemapped"]["url"], path)
        im = Image.open(path).convert("RGB")
        W, H = im.size
        im = im.resize((4096, int(H * 4096 / W)), Image.BILINEAR)
        arr = np.asarray(im).astype(float) / 255
        mx = arr.max(2); mn = arr.min(2); d = mx - mn
        sat = d / np.maximum(mx, 1e-6)
        r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
        hue = np.zeros_like(r)
        m = (r == mx) & (d > 0)
        hue[m] = ((g - b)[m] / d[m]) % 6
        red = (r == mx) & (sat > 0.68) & (mx > 0.3) & ((hue < 0.5) | (hue > 5.5))
        red = ndi.binary_opening(red, iterations=2)
        lab, n = ndi.label(red)
        sizes = ndi.sum(red, lab, range(1, n + 1)); objs = ndi.find_objects(lab)
        blobs = []
        for sz, sl in zip(sizes, objs):
            if sz < 80:
                continue
            y0, y1 = sl[0].start, sl[0].stop; x0, x1 = sl[1].start, sl[1].stop
            blobs.append({"area_px": int(sz), "yaw_deg": round((x0 + x1) / 2 / 4096 * 360, 1), "pitch_deg": round(90 - (y0 + y1) / 2 / im.size[1] * 180, 1), "w_px": x1 - x0, "h_px": y1 - y0})
        blobs.sort(key=lambda x: -x["area_px"])
        res["panoramas"][pid] = {"source_px": [W, H], "blobs_ge_80px": len(blobs), "largest": blobs[:6], "looked_at": LOOKED_AT[pid], "pillar_box": False}
        print(pid, len(blobs))
    json.dump(res, open(a.out, "w"), indent=1)


if __name__ == "__main__":
    main()
