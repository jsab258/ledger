#!/usr/bin/env python
"""Rebuild the previews of the shop-windows target in production/previews/cloud-week/refs/shop-windows/.

    /home/user/.bpyenv/bin/python make_previews.py [--photos DIR] [--work DIR] [--previews DIR]

  P1..P6-<place>-<what>.jpg          the six Geograph photographs, cropped to the craft (shop fronts and windows only), anything with a person, a real
                                     firm's name, a number or a drink merchant's sign masked or cropped away; credits in TARGET.md.
                                     The crops and EVERY mask are the list extras.PREVIEW_PHOTOS (original pixels, flat grey 120): they are drawn on each
                                     rebuild and then READ BACK from the written JPEG (flat grey inside each mask, or the run stops); self_check.py
                                     reads the committed JPEGs against the same list (PRV-01 to PRV-03).
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
import extras as X  # noqa: E402

UA = "Mozilla/5.0 (X11; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0 LedgerShopWindowsTarget/1.0"
PHOTOS = {p["gid"]: p for p in X.PREVIEW_PHOTOS}
PHOTO_PREVIEW = {p["id"]: p for p in X.PREVIEW_PHOTOS}


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
    ap.add_argument("--only", choices=["photos", "all"], default="all", help="photos: only the six photograph previews (no drawings)")
    a = ap.parse_args()
    os.makedirs(a.photos, exist_ok=True)
    os.makedirs(a.previews, exist_ok=True)
    os.makedirs(a.work, exist_ok=True)
    t = json.load(open(os.path.join(HERE, "target.json")))
    crops = {}
    for gid, ph in PHOTOS.items():
        p = os.path.join(a.photos, gid + ".jpg")
        fetch(ph["url"], p)
        im = Image.open(p).convert("RGB")
        S.draw_masks(im, ph["masks"], X.MASK_GREY)          # the masks are drawn on every rebuild, on the ORIGINAL, before the crop
        c = im.crop(tuple(ph["crop"]))
        crops[gid] = c
        out = os.path.join(a.previews, ph["name"] + ".jpg")
        save_jpg(c, out)
        rep = S.preview_mask_report(out, ph, X.MASK_GREY)    # and read back from the JPEG that was written
        bad = [r for r in rep if not r["ok"]]
        print("  %s: %d masks, %d with pixels in the crop, flat grey: %s" % (ph["id"], len(rep), sum(1 for r in rep if r["pixels"]), "yes" if not bad else "NO " + str(bad)))
        if bad:
            raise SystemExit("mask not flat grey in " + out)
    if a.only == "photos":
        return
    # the overlay on P1
    rows = {r["what"]: r for r in t["photographs"]["rows"]}
    crop_top = PHOTO_PREVIEW["P1"]["crop"][1]
    top = rows["door leaf top (underside of the transom's board)"]["y_px"] - crop_top
    bot = rows["door leaf bottom / threshold"]["y_px"] - crop_top
    cx = (rows["leaf left edge"]["x_px"] + rows["leaf right edge"]["x_px"]) / 2
    fish = next(s for s in t["shops"] if s["id"] == "ritas")   # a T1 (timber) door: the photograph shows a timber door
    tmp = os.path.join(a.work, "p1_overlay.jpg")
    lines, k = TD.overlay(os.path.join(a.previews, PHOTO_PREVIEW["P1"]["name"] + ".jpg"), {"leaf_top_y": top, "leaf_bottom_y": bot, "leaf_centre_x": cx}, fish, tmp)
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
