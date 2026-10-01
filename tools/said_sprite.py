#!/usr/bin/env python3
"""A face filmed saying a line, as one picture for the day's page (item 4, 1 October).

    python tools/said_sprite.py FRAMES_DIR FIRST COUNT OUT.jpg [--fps 10]
    python tools/said_sprite.py FRAMES_DIR --line N OUT.jpg     # the Nth line filmed (0 the first)
    python tools/said_sprite.py --selftest

The game's -MouthFilm writes a frame a tenth of a second while someone
speaks (Saved/MouthFilm/<who>/f_NNN.png, 1280 by 720, the face from 60 cm).
This cuts COUNT frames from FIRST on to the face (a 4:3 window at the
centre, the page's speaking box) and lays them in rows of five on one JPEG,
which tools/day_page.py's "said" item plays in time with the line's sound.
Prints the item's sprite entry. Reads the frames only.
"""
import glob
import json
import os
import sys

COLS = 5
TILE = (640, 480)


def window(w, h):
    """The 4:3 window at the frame's centre, two thirds of its height."""
    ch = int(h * 2 / 3)
    cw = ch * 4 // 3
    return ((w - cw) // 2, (h - ch) // 2, (w + cw) // 2, (h + ch) // 2)


def lines(frames_dir, gap=0.3):
    """The frames grouped by line: a pause of more than `gap` seconds
    between two frames' writing starts a new line (the film runs only while
    someone speaks)."""
    files = sorted(glob.glob(os.path.join(frames_dir, "f_*.png")))
    groups, last = [], None
    for f in files:
        t = os.path.getmtime(f)
        if last is None or t - last > gap:
            groups.append([])
        groups[-1].append(f)
        last = t
    return groups


def make(frames_dir, first, count, out, fps=10):
    files = sorted(glob.glob(os.path.join(frames_dir, "f_*.png")))[first:first + count]
    if not files:
        raise SystemExit("no frames at %s from %d" % (frames_dir, first))
    return make_files(files, out, fps)


def make_files(files, out, fps=10):
    """The sprite from these frames, in this order."""
    from PIL import Image
    rows = (len(files) + COLS - 1) // COLS
    sheet = Image.new("RGB", (TILE[0] * COLS, TILE[1] * rows))
    for i, f in enumerate(files):
        im = Image.open(f).convert("RGB")
        tile = im.crop(window(*im.size)).resize(TILE)
        sheet.paste(tile, ((i % COLS) * TILE[0], (i // COLS) * TILE[1]))
    os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
    sheet.save(out, quality=85)
    return {"file": out.replace("\\", "/"), "frames": len(files), "cols": COLS, "rows": rows, "fps": fps}


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("said_sprite selftest FAIL " + name)
    x0, y0, x1, y1 = window(1280, 720)
    check("the window is 4:3", (x1 - x0) * 3 == (y1 - y0) * 4)
    check("the window is centred", x0 == 1280 - x1 and y0 == 720 - y1)
    print("said_sprite selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    fps = int(sys.argv[sys.argv.index("--fps") + 1]) if "--fps" in sys.argv else 10
    if "--line" in sys.argv:
        n = int(sys.argv[sys.argv.index("--line") + 1])
        d, out = sys.argv[1], sys.argv[-1]
        allf = sorted(glob.glob(os.path.join(d, "f_*.png")))
        g = lines(d)[n]
        print(json.dumps(make(d, allf.index(g[0]), len(g), out, fps)))
    else:
        a = [x for x in sys.argv[1:] if not x.startswith("--")]
        print(json.dumps(make(a[0], int(a[1]), int(a[2]), a[3], fps)))
