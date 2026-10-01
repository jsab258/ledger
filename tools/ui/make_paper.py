"""The interface's newsprint, drawn by script (production/design/ui/STYLE-GUIDE.md, Materials).

    python tools/ui/make_paper.py            # writes production/art/ui/newsprint.png and newsprint-edge.png
    python tools/ui/make_paper.py --selftest

WHY, 1 October (the interface as drawn). Every sheet in the evening paper is
newsprint, "a coarse fibre and yellowing towards the edges ... and a soft
shadow under them"; the finish with real scanned paper comes later, under
Jafar's answer (a). Until then the game draws the sheet in the guide's
Newsprint (#E8E3D6) from these:

- newsprint.png, 512 px square and tileable: the sheet's Newsprint with the
  fibre in it (darker and lighter flecks, short fibres in every direction),
  seeded so it is the same every time;
- newsprint-edge.png, 256 px square: a soft yellowing towards all four
  edges, alpha only, stretched over a whole sheet.

Nothing fetched: noise from a fixed seed, made with Pillow.
"""
import math
import os
import random
import sys

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUT = os.path.join(REPO, "production", "art", "ui")


def fibre(size=512, seed=1990):
    from PIL import Image, ImageDraw, ImageFilter
    rnd = random.Random(seed)
    base = Image.new("L", (size, size), 128)
    px = base.load()
    # the pulp: fine noise, tileable because each value comes from the pixel itself
    for y in range(size):
        for x in range(size):
            px[x, y] = 128 + int(rnd.gauss(0, 4))
    base = base.filter(ImageFilter.GaussianBlur(0.6))
    d = ImageDraw.Draw(base)
    # the fibres: short strokes, light and dark, wrapped at the edges so the tile repeats
    for _ in range(1100):
        x, y = rnd.uniform(0, size), rnd.uniform(0, size)
        a = rnd.uniform(0, math.pi)
        n = rnd.uniform(3, 14)
        v = 128 + int(rnd.choice((-1, 1)) * rnd.uniform(3, 7))
        for ox in (-size, 0, size):
            for oy in (-size, 0, size):
                d.line([(x + ox, y + oy), (x + ox + n * math.cos(a), y + oy + n * math.sin(a))], fill=v, width=1)
    # a few darker flecks of the wood
    for _ in range(50):
        x, y = rnd.uniform(0, size), rnd.uniform(0, size)
        r = rnd.uniform(0.6, 1.4)
        for ox in (-size, 0, size):
            for oy in (-size, 0, size):
                d.ellipse([x + ox - r, y + oy - r, x + ox + r, y + oy + r], fill=128 - int(rnd.uniform(8, 16)))
    return base.filter(ImageFilter.GaussianBlur(0.45))


def edge(size=256):
    from PIL import Image
    im = Image.new("LA", (size, size))
    px = im.load()
    for y in range(size):
        for x in range(size):
            dx = min(x, size - 1 - x) / (size / 2.0)
            dy = min(y, size - 1 - y) / (size / 2.0)
            t = min(dx, dy)
            a = max(0.0, 1.0 - t / 0.22) ** 2      # within the outer 11% of the sheet
            px[x, y] = (150, int(a * 70))
    return im


def coupon_dash(size=48, inset=5, dash=6, gap=4):
    """A reader's coupon's dashed edge: a 2 px ink rule, dash and gap, round a clear square;
    the game draws it as a border brush, so the edges repeat along any length."""
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    ink = (0x1E, 0x1E, 0x1D, 255)
    a, b = inset, size - inset - 2
    t = 0
    while t < size:
        for x0 in range(t, min(t + dash, size)):
            if a <= x0 <= b + 1:
                d.rectangle([x0, a, x0, a + 1], fill=ink)
                d.rectangle([x0, b, x0, b + 1], fill=ink)
                d.rectangle([a, x0, a + 1, x0], fill=ink)
                d.rectangle([b, x0, b + 1, x0], fill=ink)
        t += dash + gap
    return im


def selftest():
    ok = bad = 0

    def check(name, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_paper selftest FAIL " + name)
    f = fibre(64, seed=3)
    check("the fibre is a grey around mid-grey", 110 < sum(f.getdata()) / (64 * 64) < 146)
    check("the same seed makes the same paper", list(fibre(32, 7).getdata()) == list(fibre(32, 7).getdata()))
    e = edge(32)
    check("the edge is clear in the middle and yellowed at the rim", e.getpixel((16, 16))[1] == 0 and e.getpixel((0, 16))[1] > 40)
    print("make_paper selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    os.makedirs(OUT, exist_ok=True)
    # the sheet's own colour, Newsprint #E8E3D6, with the fibre multiplied into it
    from PIL import Image
    f = fibre()
    rgb = [Image.eval(f, lambda v, c=c: max(0, min(255, int(c * v / 128.0)))) for c in (0xE8, 0xE3, 0xD6)]
    Image.merge("RGB", rgb).save(os.path.join(OUT, "newsprint.png"))
    edge().save(os.path.join(OUT, "newsprint-edge.png"))
    coupon_dash().save(os.path.join(OUT, "coupon-dash.png"))
    print("make_paper: newsprint.png, newsprint-edge.png and coupon-dash.png in %s" % OUT)
