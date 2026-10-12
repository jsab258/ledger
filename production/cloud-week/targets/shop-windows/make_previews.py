#!/usr/bin/env python
"""Rebuild the previews of the shop-windows target in production/previews/cloud-week/refs/shop-windows/.

    /home/user/.bpyenv/bin/python make_previews.py [--photos DIR] [--work DIR] [--previews DIR]

  P1..P6-<place>-<what>.jpg          the six Geograph photographs, cropped to the craft (shop fronts and windows only), anything with a person, a real
                                     firm's name, a number or a drink merchant's sign masked or cropped away; credits in TARGET.md
  P1-worcester-fish-front-target-on-photo.jpg   the target's door, stallriser, glass lines laid on P1 at the scale fitted on the leaf's height
  D1-ritas-front.jpg                 Rita's bay in millimetres from target.json
  D2-ten-fronts-sheet.jpg            the ten fronts
  D3-ritas-room-plan-picture.jpg     Rita's plan, back wall with stand-off classes, and where the box lands in the 4096 picture
  D4-standoff-and-cameras.jpg        the stand-off rules as a chart (slide in pixels against stand-off at the three cameras) and the camera plan
JPEG at most 1200 px on the long side and under 300 KB. Originals are downloaded from Geograph into --photos (never into the repository).
"""
import argparse
import json
import os
import sys
import time
import urllib.request

from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import sw_common as S  # noqa: E402
import target_drawing as TD  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0 LedgerShopWindowsTarget/1.0"
# id: (direct image url, crop box in the original's pixels, masks (grey rectangles) in the original's pixels, preview name)
PHOTOS = {
    "2192169": ("https://s0.geograph.org.uk/geophotos/02/19/21/2192169_36cb6ecc.jpg", (0, 108, 640, 480), [(383, 108, 436, 146), (557, 94, 611, 134)], "P1-worcester-fish-front-below-fascia"),
    "2184467": ("https://s0.geograph.org.uk/geophotos/02/18/44/2184467_941cf948.jpg", (30, 388, 192, 582), [], "P2-bath-grocer-window-stock"),
    "5945841": ("https://s1.geograph.org.uk/geophotos/05/94/58/5945841_dc1c2255_1024x1024.jpg", (300, 326, 690, 520), [], "P3-pinner-hardware-newsagent-windows"),
    "3378991": ("https://s3.geograph.org.uk/geophotos/03/37/89/3378991_95b1bbed_1024x1024.jpg", (225, 548, 600, 990), [(405, 655, 478, 748), (300, 580, 350, 645)], "P4-hull-chandler-front-mesh"),
    "1633924": ("https://s0.geograph.org.uk/geophotos/01/63/39/1633924_c4220c3e.jpg", (0, 262, 330, 425), [], "P5-launderette-front-type-2009"),
    "27024": ("https://s0.geograph.org.uk/photos/02/70/027024_2285cb8f.jpg", (0, 262, 417, 420), [], "P6-kames-unlet-shop-1995"),
}


def save_jpg(im, path, limit=295_000):
    if max(im.size) > 1200:
        s = 1200.0 / max(im.size)
        im = im.resize((int(im.width * s), int(im.height * s)), Image.LANCZOS)
    for q in (90, 86, 82, 78, 72, 66, 60):
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < limit:
            break
    print(path, im.size, os.path.getsize(path) // 1024, "KB")


def fetch(url, path):
    if os.path.exists(path):
        return
    data = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=60).read()
    open(path, "wb").write(data)
    time.sleep(0.6)


def label(im, text):
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, im.width, 14], fill=(30, 30, 30))
    d.text((4, 2), text, fill=(240, 240, 240))
    return im


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default="/tmp/shop_windows_photos")
    ap.add_argument("--previews", default=os.path.join(HERE, "..", "..", "..", "previews", "cloud-week", "refs", "shop-windows"))
    ap.add_argument("--work", default="/tmp/shop_windows_previews")
    a = ap.parse_args()
    os.makedirs(a.photos, exist_ok=True)
    os.makedirs(a.previews, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    t = json.load(open(os.path.join(HERE, "target.json")))
    crops = {}
    for gid, (url, box, masks, name) in PHOTOS.items():
        p = os.path.join(a.photos, gid + ".jpg")
        fetch(url, p)
        im = Image.open(p).convert("RGB")
        dr = ImageDraw.Draw(im)
        for m in masks:
            dr.rectangle(m, fill=(120, 120, 120))
        c = im.crop(box)
        crops[gid] = c
        save_jpg(c, os.path.join(a.previews, name + ".jpg"))
    # the overlay on P1
    rows = {r["what"]: r for r in t["photographs"]["rows"]}
    top = rows["door leaf top (underside of the transom's board)"]["y_px"] - 108
    bot = rows["door leaf bottom / threshold"]["y_px"] - 108
    cx = (rows["leaf left edge"]["x_px"] + rows["leaf right edge"]["x_px"]) / 2
    fish = next(s for s in t["shops"] if s["id"] == "ritas")   # a T1 (timber) door: the photograph shows a timber door
    tmp = os.path.join(a.work, "p1_overlay.jpg")
    lines, k = TD.overlay(os.path.join(a.previews, PHOTOS["2192169"][3] + ".jpg"), {"leaf_top_y": top, "leaf_bottom_y": bot, "leaf_centre_x": cx}, fish, tmp)
    save_jpg(Image.open(tmp), os.path.join(a.previews, "P1-worcester-fish-front-target-on-photo.jpg"))
    # drawings
    ritas = next(s for s in t["shops"] if s["id"] == "ritas")
    im = TD.draw_polys(TD.front_polys(ritas), (1500, 760), 0.24, (30, 30), "Rita's bay from target.json: millimetres, u from the viewer's left, z from the footway; card dashed, display amber")
    save_jpg(im, os.path.join(a.previews, "D1-ritas-front.jpg"))
    sheet = []
    for s in t["shops"]:
        sheet.append(TD.draw_polys(TD.front_polys(s), (1500, 760), 0.24, (30, 30), s["id"]))
    cols, cw, ch = 2, 600, 304
    sh = Image.new("RGB", (cols * cw, 5 * ch), (240, 240, 240))
    for n, i in enumerate(sheet):
        sh.paste(i.resize((cw, ch)), ((n % cols) * cw, (n // cols) * ch))
    save_jpg(sh, os.path.join(a.previews, "D2-ten-fronts-sheet.jpg"))
    plan, _ = TD.draw_plan(ritas, (1500, 900))
    room = TD.draw_room(ritas, (1500, 520))
    pic, _ = TD.draw_picture(ritas, (1500, 680))
    d3 = Image.new("RGB", (1500, 900 + 520 + 680), (240, 240, 240))
    d3.paste(plan, (0, 0))
    d3.paste(room, (0, 900))
    d3.paste(pic, (0, 1420))
    save_jpg(d3, os.path.join(a.previews, "D3-ritas-room-plan-picture.jpg"))
    # the chart
    import numpy as np
    W_, H_ = 1500, 760
    ch_ = Image.new("RGB", (W_, H_), (244, 244, 240))
    dr = ImageDraw.Draw(ch_)
    scene = S.load_scene()
    card = S.card_of(scene, "east_parade", 2)
    dr.text((10, 6), "slide of an object painted on a surface, in pixels of a 2560 x 1440 frame, against its stand-off (m): back wall (left), right wall mid depth (right)", fill=(20, 20, 20))
    cols_ = {"STREET_SQUARE": (60, 120, 200), "STREET_30": (40, 160, 90), "CLOSE_35": (200, 60, 60)}
    for panel, (pl, obj_fn, plane, xmax) in enumerate((("back", lambda s_: (2.65, 4.5 - s_, 1.2), ("back", 4.5), 1.0), ("right", lambda s_: (5.3 - s_, 2.2, 1.2), ("right", 5.3), 0.3))):
        x0, y0, w, h = 60 + panel * 740, 60, 640, 600
        dr.rectangle([x0, y0, x0 + w, y0 + h], outline=(60, 60, 60))
        ymax = 120.0
        for ytick in (20, 40, 80, 120):
            yy = y0 + h - ytick / ymax * h
            dr.line([x0, yy, x0 + w, yy], fill=(200, 200, 200))
            dr.text((x0 - 34, yy - 6), str(ytick), fill=(20, 20, 20))
        for cn, col in cols_.items():
            eye, _ = S.camera_pose(cn, card, 17.025)
            ep = S.eye_in_picture(eye, card)
            pts = []
            for i in range(0, 41):
                s_ = xmax * i / 40.0
                v = S.slide_px(ep, obj_fn(s_), plane, 4.5, S.CAMERAS[cn]["vfov_deg"])
                pts.append((x0 + s_ / xmax * w, y0 + h - min(v, ymax) / ymax * h))
            dr.line(pts, fill=col, width=3)
        dr.text((x0, y0 + h + 8), "stand-off 0 to %.1f m   (red CLOSE_35, green STREET_30, blue STREET_SQUARE; lines at 20 and 40 px are the budgets)" % xmax, fill=(20, 20, 20))
    save_jpg(ch_, os.path.join(a.previews, "D4-standoff-and-cameras.jpg"))


if __name__ == "__main__":
    main()
