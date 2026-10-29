#!/usr/bin/env python3
"""A STRETCH OF THE AI TESTER'S FILM AS ONE MOVING PICTURE FOR HIS PAGE.

    python tools/film_webp.py FILM_DIR FIRST LAST OUT.webp [--width 800] [--ms 125]
    python tools/film_webp.py FILM_DIR --marks production/playtest/route-walk/<run>/film-marks.json --name sit-down OUT.webp
    python tools/film_webp.py --selftest

WHY, 29 October 2026 (his orders D10 and the camera's rows: the sit and each camera row shown to him in the game). The
tester films about eight frames a second while a key is held (tools/ai-tester/play.py, f-00001.jpg on) and names each
filmed stretch's frames in film-marks.json (tools/route_walk.py); his page shows films as animated WebP, as the walk's
page of 26 October did (production/approvals/2026-10-26). This cuts one stretch, scales it to the page's width and
loops it at the frames' own pace. Only frames a fresh reviewer has checked go on a page (CLAUDE.md, the gate).
"""
import glob
import json
import os
import sys


def frames(film_dir, first, last):
    out = []
    for n in range(int(first), int(last) + 1):
        p = os.path.join(film_dir, "f-%05d.jpg" % n)
        if os.path.exists(p):
            out.append(p)
    return out


def make(paths, out, width=800, ms=125):
    from PIL import Image
    ims = []
    for p in paths:
        im = Image.open(p).convert("RGB")
        h = max(1, round(im.size[1] * width / float(im.size[0])))
        ims.append(im.resize((width, h), Image.LANCZOS))
    if not ims:
        raise ValueError("no frames")
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    ims[0].save(out, save_all=True, append_images=ims[1:], duration=ms, loop=0, quality=72, method=4)
    return len(ims), os.path.getsize(out)


def selftest():
    import tempfile
    from PIL import Image
    ok = []
    d = tempfile.mkdtemp()
    for n in range(1, 6):
        Image.new("RGB", (960, 540), (n * 40, 0, 0)).save(os.path.join(d, "f-%05d.jpg" % n))
    paths = frames(d, 2, 4)
    ok.append([os.path.basename(p) for p in paths] == ["f-00002.jpg", "f-00003.jpg", "f-00004.jpg"])
    n, size = make(paths, os.path.join(d, "clip.webp"), width=400)
    im = Image.open(os.path.join(d, "clip.webp"))
    ok.append(n == 3 and getattr(im, "n_frames", 1) == 3 and im.size == (400, 225) and size > 0)
    print("film_webp selftest: passed=%d/%d failed=%d" % (sum(ok), len(ok), len(ok) - sum(ok)))
    return 0 if all(ok) else 1


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--selftest" in a:
        sys.exit(selftest())
    width = int(a[a.index("--width") + 1]) if "--width" in a else 800
    ms = int(a[a.index("--ms") + 1]) if "--ms" in a else 125
    if "--marks" in a:
        marks = json.load(open(a[a.index("--marks") + 1], encoding="utf-8"))
        first, last = marks[a[a.index("--name") + 1]]
        out = [x for x in a[1:] if x.endswith(".webp")][0]
    else:
        first, last, out = a[1], a[2], a[3]
    n, size = make(frames(a[0], first, last), out, width, ms)
    print("filmWebp frames=%d bytes=%d out=%s" % (n, size, out))
