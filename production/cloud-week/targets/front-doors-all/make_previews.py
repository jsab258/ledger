"""Makes the previews of the photographs this target measured (reduced crops of the doors only, at most 1200 px and 300 KB, with anything a preview must not
show masked flat grey by script) and the overlays of the target's drawing on three of them, into production/previews/cloud-week/refs/front-doors-all/.
  /home/user/.bpyenv/bin/python make_previews.py PHOTO_DIR
The masks are recorded in preview_masks.json (box in the preview's own pixels) and read back by self_check.py --previews.
Photographs are for measuring and for the reviewers only: never placed in the game, never traced into a texture, never fed to an image model."""
import json
import os
import sys

from PIL import Image, ImageDraw

import target_drawing as TD
from td_common import HERE, PREVIEWS, TARGET_JSON, load_json
from td_data import MEAS, PHOTOS

sys.dont_write_bytecode = True
GREY = (120, 120, 120)

# preview file -> (photograph id, crop box in the photograph's pixels, zoom, masks [(what, box in the photograph's pixels)])
SPECS = {
    "d1-durham-carrville-terrace-1975-two-doors.jpg": ("D1", (0, 430, 200, 700), 4.0, []),
    "d2-railway-street-1987-three-doors.jpg": ("D2", (350, 235, 800, 385), 2.4, [("a pole-mounted board", (424, 262, 484, 332)), ("an oval plaque on the white door", (765, 297, 792, 318))]),
    "d3-levenshulme-ratcliffe-street-1994-four-light-door.jpg": ("D3", (0, 360, 260, 650), 4.0, [("a small numeral over the left door", (74, 440, 92, 449))]),
    "d4-barnoldswick-frederick-street-1990-three-doors.jpg": ("D4", (330, 300, 600, 450), 4.0, []),
    "d5-aberdeen-hazlehead-1987-council-flush-door.jpg": ("D5", (430, 100, 830, 1010), 1.0, [("a small white label on the door", (588, 358, 640, 384))]),
    "d6-hull-rensburg-street-1982-blue-door.jpg": ("D6", (780, 270, 900, 498), 4.0, [("a painted numeral on the door", (855, 361, 869, 393))]),
    "d7-hull-abbey-street-1986-arched-doorways.jpg": ("D7", (600, 290, 780, 590), 3.0, []),
    "d8-hull-brazil-street-1986-painted-frames.jpg": ("D8", (440, 300, 820, 500), 3.0, [("a board on the fence", (455, 425, 495, 470))]),
    "d9-newburn-council-houses-1989-turquoise-door.jpg": ("D9", (340, 500, 460, 640), 6.0, []),
    "d10-poole-boot-scraper-2014.jpg": ("D10", (0, 0, 640, 427), 1.6, []),
}
OVERLAYS = {
    "d3-levenshulme-ratcliffe-street-1994-target-on-photo.jpg": ("T2", "D3", (0, 360, 260, 650), 4.0, "D3_leaf"),
    "d2-railway-street-1987-target-on-photo.jpg": ("F5", "D2", (520, 250, 640, 380), 7.0, "D2_F5_leaf"),
    "d5-aberdeen-hazlehead-1987-target-on-photo.jpg": ("F6", "D5", (430, 100, 830, 1010), 1.0, "D5_leaf"),
}


def open_photo(d, pid):
    ph = PHOTOS[pid]
    p = os.path.join(d, "%s.jpg" % ph["gid"]) if ph.get("gid") else os.path.join(d, "%s.png" % pid)
    return Image.open(p).convert("RGB")


def save_small(im, path):
    q = 88
    while True:
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) < 290 * 1024 or q <= 40:
            return
        q -= 8


def main():
    d = sys.argv[1]
    os.makedirs(PREVIEWS, exist_ok=True)
    T = load_json(TARGET_JSON)
    masks_out = {}
    for fname, (pid, box, zoom, masks) in SPECS.items():
        im = open_photo(d, pid)
        if pid == "D5":
            pass
        draw = ImageDraw.Draw(im)
        for what, mb in masks:
            draw.rectangle(mb, fill=GREY)
        c = im.crop(box)
        c = c.resize((int(round(c.width * zoom)), int(round(c.height * zoom))), Image.LANCZOS)
        if max(c.size) > 1200:
            f = 1200.0 / max(c.size)
            c = c.resize((int(c.width * f), int(c.height * f)), Image.LANCZOS)
            zoom = zoom * f
        save_small(c, os.path.join(PREVIEWS, fname))
        if masks:
            ml = []
            for what, mb in masks:
                x0 = max(0, int(round((mb[0] - box[0]) * zoom)))
                y0 = max(0, int(round((mb[1] - box[1]) * zoom)))
                x1 = min(c.width, int(round((mb[2] - box[0]) * zoom)))
                y1 = min(c.height, int(round((mb[3] - box[1]) * zoom)))
                # inset by 3 px so the JPEG's edge does not enter the test
                ml.append({"what": what, "box_in_preview": [x0 + 3, y0 + 3, max(x0 + 4, x1 - 3), max(y0 + 4, y1 - 3)]})
            masks_out[fname] = ml
        print(fname, c.size, os.path.getsize(os.path.join(PREVIEWS, fname)) // 1024, "KB")
    for fname, (kind, pid, box, zoom, mkey) in OVERLAYS.items():
        im = open_photo(d, pid)
        for spec_name, (spid, sbox_, sz, smasks) in SPECS.items():
            if spid == pid:
                dr = ImageDraw.Draw(im)
                for what, mb in smasks:
                    dr.rectangle(mb, fill=GREY)
        c = im.crop(box)
        c = c.resize((int(round(c.width * zoom)), int(round(c.height * zoom))), Image.LANCZOS)
        L = TD.draw_kind(T, kind)
        spec, fs = TD.frame_of(T, kind)
        lb = MEAS[mkey]["box"]
        vz0, vz1 = fs["visible_leaf_z"]
        vx0, vx1 = fs["visible_leaf_x"]
        s = (lb[3] - lb[1]) / (vz1 - vz0) * zoom            # the scale fitted on the visible HEIGHT only
        ox = (lb[0] - box[0]) * zoom
        oy = (lb[3] - box[1]) * zoom
        dr = ImageDraw.Draw(c)

        def px(x, z):
            return (ox + (x - vx0) * s, oy - (z - vz0) * s)

        def outline(g, col):
            for part in TD.poly_coords(g):
                pts = [px(x, z) for x, z in part["exterior"]]
                dr.line(pts + [pts[0]], fill=col, width=2)
        outline(L["visible"], (255, 255, 0))
        for g in L["openings"].values():
            outline(g, (255, 40, 40))
        outline(L["mouldings"], (255, 140, 0))
        for g in L["furniture"].values():
            outline(g, (40, 255, 40))
        dr.text((6, 6), "drawing of %s (scale fitted on the height only): yellow visible face, red openings, green fittings" % kind, fill=(255, 255, 255))
        save_small(c, os.path.join(PREVIEWS, fname))
        masks_out[fname] = [{"what": w, "box_in_preview": [int((mb[0] - box[0]) * zoom) + 3, int((mb[1] - box[1]) * zoom) + 3, int((mb[2] - box[0]) * zoom) - 3, int((mb[3] - box[1]) * zoom) - 3]}
                            for spec_name, (spid, sbox_, sz, smasks) in SPECS.items() if spid == pid for w, mb in smasks
                            if box[0] <= mb[0] and mb[2] <= box[2] and box[1] <= mb[1] and mb[3] <= box[3]]
        masks_out[fname] = [m for m in masks_out[fname] if m["box_in_preview"][2] > m["box_in_preview"][0] + 1]
        if not masks_out[fname]:
            del masks_out[fname]
        print(fname, c.size, os.path.getsize(os.path.join(PREVIEWS, fname)) // 1024, "KB")
    # the drawings
    import tempfile
    tmp = tempfile.mkdtemp()
    TD.picture_kinds(T, tmp)
    TD.picture_rows(T, tmp)
    for src, dst in (("kinds-elevations.png", "target-ten-door-kinds-elevations.jpg"), ("street-rows.png", "target-street-rows-east-and-west.jpg")):
        im = Image.open(os.path.join(tmp, src)).convert("RGB")
        if max(im.size) > 1200:
            f = 1200.0 / max(im.size)
            im = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
        save_small(im, os.path.join(PREVIEWS, dst))
        print(dst, im.size)
    with open(os.path.join(HERE, "preview_masks.json"), "w") as f:
        json.dump(masks_out, f, indent=1)


if __name__ == "__main__":
    main()
