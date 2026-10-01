"""The evening paper's photographs: the game's own frames screened into halftone dots (STYLE-GUIDE.md, Materials).

    python tools/ui/make_halftone.py            # writes production/art/ui/halftone-*.png
    python tools/ui/make_halftone.py --selftest

WHY, 1 October (the interface as drawn). The title's front page and the
loading page carry a photograph of the street, and the guide says how:
"photographs of the town are the game's own frames, screened into dots that
grow where the picture is dark, in ink on newsprint". So each picture is a
frame the game itself took (production/approvals/2026-10-01, Quay Street at
night from the hook camera), cropped to the shape the screen draws it at,
lifted in contrast the way a newspaper's block was, and screened: a grid of
round dots at 45 degrees, each dot's area the darkness of its cell, ink
(#1E1E1D) on newsprint (#E8E3D6). Drawn at twice the size the screen shows
it in the guide's units, so on a 1440 screen it is still sharp.
"""
import math
import os
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "art", "ui")
SOURCE = os.path.join(REPO, "production", "approvals", "2026-10-01", "street-hook-night.webp")
INK, PAPER = (0x1E, 0x1E, 0x1D), (0xE8, 0xE3, 0xD6)
#: name: (crop as fractions of the frame (x0, y0, x1, y1), size in the guide's units (w, h))
PICTURES = {
    "halftone-title": ((0.36, 0.14, 0.70, 0.99), (238, 395)),       # the front page's column: the lamp, the cars, Mickey's
    "halftone-loading": ((0.05, 0.18, 0.95, 0.88), (1072, 420)),   # the loading page's spread, a story saved after dark
    "halftone-loading-day": ((0.05, 0.18, 0.95, 0.88), (1072, 420)),   # and by day, a new story at 9 am
    "halftone-title-day": ((0.36, 0.14, 0.70, 0.99), (238, 395)),   # the front page by day, the street behind it lit the same
}
#: the frame each is screened from, when not the night one
DAY = os.path.join(REPO, "production", "approvals", "2026-10-01", "street-hook-day.webp")
SOURCES = {"halftone-loading-day": DAY, "halftone-title-day": DAY}
CELL = 7          # pixels between dots, at twice the guide's units


def screen(img, cell=CELL, angle=45.0):
    """A grey picture screened into round dots on a grid turned by angle."""
    from PIL import Image, ImageDraw
    w, h = img.size
    out = Image.new("RGB", (w, h), PAPER)
    d = ImageDraw.Draw(out)
    a = math.radians(angle)
    ca, sa = math.cos(a), math.sin(a)
    px = img.load()
    r = int(math.hypot(w, h) / cell) + 2
    for i in range(-r, r):
        for j in range(-r, r):
            # the cell centre on the turned grid
            gx, gy = i * cell, j * cell
            x = w / 2 + gx * ca - gy * sa
            y = h / 2 + gx * sa + gy * ca
            if x < -cell or y < -cell or x > w + cell or y > h + cell:
                continue
            v = px[min(w - 1, max(0, int(x))), min(h - 1, max(0, int(y)))] / 255.0
            dark = 1.0 - v
            if dark <= 0.02:
                continue
            # the dot's area is the cell's darkness (less half a pixel, which the
            # drawing adds round a small dot); past half the dots join
            rad = cell * math.sqrt(dark / math.pi) - 0.5
            if rad <= 0.3:
                continue
            d.ellipse([x - rad, y - rad, x + rad, y + rad], fill=INK)
    return out


def prepare(frame, crop, size):
    from PIL import Image, ImageOps, ImageEnhance
    w, h = frame.size
    box = (int(crop[0] * w), int(crop[1] * h), int(crop[2] * w), int(crop[3] * h))
    pic = frame.crop(box)
    target = (size[0] * 2, size[1] * 2)
    pic = ImageOps.fit(pic, target, Image.LANCZOS)
    g = ImageOps.grayscale(pic)
    g = ImageOps.autocontrast(g, cutoff=1)
    g = ImageEnhance.Contrast(g).enhance(1.25)
    return g


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_halftone selftest FAIL " + name)
    from PIL import Image
    black = screen(Image.new("L", (40, 40), 0))
    white = screen(Image.new("L", (40, 40), 255))
    check("black screens to ink", black.getpixel((20, 20)) == INK)
    check("white stays newsprint", white.getpixel((20, 20)) == PAPER)
    grey = screen(Image.new("L", (70, 70), 128))
    inked = sum(1 for p in grey.getdata() if p == INK) / (70.0 * 70.0)
    check("mid grey inks about half the paper", 0.35 < inked < 0.65)
    check("the source frame is there", os.path.isfile(SOURCE))
    print("make_halftone selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    from PIL import Image
    os.makedirs(OUT, exist_ok=True)
    for name, (crop, size) in PICTURES.items():
        frame = Image.open(SOURCES.get(name, SOURCE)).convert("RGB")
        screen(prepare(frame, crop, size)).save(os.path.join(OUT, name + ".png"))
        print("make_halftone: %s.png, %dx%d" % (name, size[0] * 2, size[1] * 2))
