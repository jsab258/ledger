#!/usr/bin/env python3
"""Pack the candidates' pictures for the approval page.

    python tools/ue/candidate_sheet.py F:/LedgerTools/tmp/cand production/casting/candidates-2026-09-25
    python tools/ue/candidate_sheet.py --selftest

From the portrait tool's -PortraitTakes run (MetaHumanPortrait.cpp): for each
candidate, the front and profile pictures as JPEGs, and the speaking frames
packed into ONE sheet of frames (a sprite), which the page steps through in
time with the line's audio. One file per clip, not ninety: the page has a
file limit, and this PC has no video encoder (ffmpeg would be a new download).

Writes <out>/<slug>/<take>-front.jpg, -profile.jpg, -speak.jpg and
<out>/index.json: per candidate, the sprite's columns, rows, frame count and
frames a second, which the page needs to play it.
"""
import glob
import json
import math
import os
import re
import sys

WHO = {"lena": "sheila-dunn", "rocco": "ron-kirby", "sam": "darren-milner"}
FPS = 15              # MetaHumanPortrait.cpp SpeakFps
STILL = (720, 540)    # front and profile, cut from the 1280x720 frame's centre
FRAME = (400, 300)    # each speaking frame in the sheet
# The speaking frames are cut round the face, not the frame's centre: at the
# portrait tool's speaking distance the head sits in the top half, and a
# centre cut left it sixty pixels wide, too small to read the lips.
SPEAK_BOX = (400, 40, 880, 400)
COLS = 10


def centre_crop(im, aspect):
    w, h = im.size
    tw = min(w, int(h * aspect))
    th = min(h, int(tw / aspect))
    x, y = (w - tw) // 2, (h - th) // 2
    return im.crop((x, y, x + tw, y + th))


def grid(n, cols=COLS):
    return cols, max(1, math.ceil(n / cols))


def pack(src, out):
    from PIL import Image
    index = {}
    for p in sorted(glob.glob(os.path.join(src, "ue-portrait-*-c*-front.png"))):
        m = re.match(r"ue-portrait-(\w+)-(c\d)-front\.png$", os.path.basename(p))
        if not m or m.group(1) not in WHO:
            continue
        who, take = m.group(1), m.group(2).upper()
        slug = WHO[who]
        os.makedirs(os.path.join(out, slug), exist_ok=True)
        entry = {"take": take}
        for shot in ("front", "profile"):
            f = os.path.join(src, "ue-portrait-%s-%s-%s.png" % (who, take.lower(), shot))
            if os.path.exists(f):
                im = centre_crop(Image.open(f).convert("RGB"), STILL[0] / STILL[1]).resize(STILL, Image.LANCZOS)
                rel = "%s/%s-%s.jpg" % (slug, take, shot)
                im.save(os.path.join(out, rel), quality=85)
                entry[shot] = rel
        frames = sorted(glob.glob(os.path.join(src, "ue-speak-%s-%s" % (who, take.lower()), "f*.png")))
        if frames:
            cols, rows = grid(len(frames))
            sheet = Image.new("RGB", (cols * FRAME[0], rows * FRAME[1]))
            for i, f in enumerate(frames):
                im = Image.open(f).convert("RGB").crop(SPEAK_BOX).resize(FRAME, Image.LANCZOS)
                sheet.paste(im, ((i % cols) * FRAME[0], (i // cols) * FRAME[1]))
            rel = "%s/%s-speak.jpg" % (slug, take)
            sheet.save(os.path.join(out, rel), quality=78)
            entry["speak"] = {"file": rel, "frames": len(frames), "cols": cols, "rows": rows, "fps": FPS}
        index.setdefault(slug, []).append(entry)
    for slug in index:
        index[slug].sort(key=lambda e: e["take"])
    with open(os.path.join(out, "index.json"), "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=1)
    n = sum(len(v) for v in index.values())
    size = sum(os.path.getsize(x) for x in glob.glob(os.path.join(out, "*", "*.jpg"))) / 1e6
    print("candidate_sheet: %d candidates, %.1f MB -> %s" % (n, size, out))
    return index


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        if cond:
            ok += 1
        else:
            bad += 1
            print("candidate_sheet selftest FAIL " + name)
    check("ninety frames make a ten by nine sheet", grid(90) == (10, 9))
    check("a single frame makes a sheet of one row", grid(1) == (10, 1))
    from PIL import Image
    im = centre_crop(Image.new("RGB", (1280, 720)), 4 / 3)
    check("the crop keeps the frame's height and centres the width", im.size == (960, 720))
    check("every asset name has its person", sorted(WHO.values()) == ["darren-milner", "ron-kirby", "sheila-dunn"])
    print("candidate_sheet selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    pack(sys.argv[1], sys.argv[2])
