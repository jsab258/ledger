"""The reviewer test's pictures: ten bases cut from production/previews (no person in any), twenty
copies with one planted fault each, five clean copies, shuffled under neutral names.

    python plant_faults.py <repo> <out_dir>

Writes <out_dir>/bases/Bxx.jpg (the last good pictures), <out_dir>/frames/frame-NN.jpg (what the
reviewers see) and <out_dir>/key.json (which frame is which: never shown to a reviewer).
Deterministic: the same previews give the same pictures.
"""
import json
import os
import random
import sys

from PIL import Image, ImageChops, ImageDraw, ImageFilter, ImageFont

Q = 88  # every picture, clean or not, goes through the same JPEG encoding

# The ten bases: (preview, crop box or None, the view as the gate's brief would name it)
BASES = {
    "B01": ("mickeys-room-furniture-day-2026-10-06.jpg", None, "Mickey's office through its window, by day"),
    "B02": ("mickeys-room-furniture-night-2026-10-06.jpg", None, "Mickey's office through its window, at night"),
    "B03": ("morning-hook-day-2026-10-07.jpg", (0, 0, 1600, 512), "the hook camera by day, the upper part of the frame"),
    "B04": ("morning-reverse-day-2026-10-07.jpg", (1025, 0, 1600, 900), "the reverse view by day, its right-hand part (the Ironmonger)"),
    "B05": ("morning-night-2026-10-07.jpg", (0, 0, 1600, 512), "the street at night, the upper part of the frame"),
    "B06": ("proof-2.6-shop-signs-and-bills-2026-10-04.jpg", (0, 0, 885, 900), "the shop row square on from the road, its left part (launderette, the empty unit to let)"),
    "B07": ("rita-day-kit-2026-10-06.jpg", (490, 0, 1600, 900), "Rita's frontage (the pawnbroker) by day, from the road"),
    "B08": ("rita-night-kit-2026-10-06.jpg", (490, 0, 1600, 900), "Rita's frontage (the pawnbroker) at night, from the road"),
    "B09": ("proof-2.6-mickeys-try3-2026-10-04.jpg", (1092, 0, 1600, 900), "Mickey's frontage from the hook camera, its right-hand part (the door and the corner)"),
    "B10": ("proof-2.6-shop-signs-and-bills-2026-10-04.jpg", (975, 0, 1600, 900), "the shop row square on from the road, its right part (pawnbroker, kiosk, fishmonger)"),
}
CLEAN = ["B01", "B03", "B05", "B07", "B10"]


def lum(im):
    return im.convert("L")


def paste_masked(dst, src, mask, at):
    dst.paste(src, at, mask)


def mask_where(im, box, test):
    """A mask over `box` of `im` where test(r, g, b) holds."""
    crop = im.crop(box)
    m = Image.new("L", crop.size, 0)
    px, mp = crop.load(), m.load()
    for y in range(crop.height):
        for x in range(crop.width):
            if test(*px[x, y]):
                mp[x, y] = 255
    return crop, m


def close(m, n=1):
    for _ in range(n):
        m = m.filter(ImageFilter.MaxFilter(3))
    for _ in range(n):
        m = m.filter(ImageFilter.MinFilter(3))
    return m


def row_span(m):
    """Fill each row of a mask between its first and last set pixel (a solid silhouette)."""
    mp = m.load()
    out = Image.new("L", m.size, 0)
    op = out.load()
    for y in range(m.height):
        xs = [x for x in range(m.width) if mp[x, y]]
        if len(xs) >= 2:
            for x in range(xs[0], xs[-1] + 1):
                op[x, y] = 255
    return out


def font(size, bold=False):
    for f in (["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"] if bold else []) + [
            "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]:
        if os.path.exists(f):
            return ImageFont.truetype(f, size)
    return ImageFont.load_default()


# ---- the twenty faults, one per copy; each returns (picture, box of the fault, what it is) ----

def f_b01_floating(im):
    """The yellow box files on the sill, a copy hanging in mid-air in front of the blind."""
    im = im.copy()
    box = (1230, 800, 1392, 888)
    crop, m = mask_where(im, box, lambda r, g, b: r > 90 and g > 80 and b < g - 35)
    m = row_span(m)
    at = (690, 400)
    im.paste(crop, at, m)
    return im, (at[0], at[1], at[0] + crop.width, at[1] + crop.height), \
        "floating object: a copy of the yellow box files hangs in mid-air in front of the blind, nothing under it"

def f_b01_testcolour(im):
    """The cork notice board in flat magenta, its shading kept: a missing material."""
    im = im.copy()
    box = (1157, 505, 1249, 581)
    region = im.crop(box)
    L = lum(region).point(lambda v: min(255, int(v * 1.25)))
    mag = Image.merge("RGB", (L, Image.new("L", region.size, 0), L))
    im.paste(mag, box[:2])
    return im, box, "test-colour block: the notice board on the right wall is flat magenta (a missing material)"


def f_b02_whitestrip(im):
    """A ragged white strip across the top pane, like the day picture's burnt-out tube."""
    im = im.copy()
    d = ImageDraw.Draw(im)
    rnd = random.Random(2)
    x0, x1, top = 588, 918, 92
    pts = [(x0, top)]
    y = 118
    for x in range(x0, x1 + 1, 6):
        y = max(104, min(138, y + rnd.randint(-5, 5)))
        pts.append((x, y))
    pts.append((x1, top))
    d.polygon(pts, fill=(236, 236, 232))
    return im, (x0, top, x1, 138), "a ragged white strip across the top pane over the blind (the night picture had none)"


def f_b02_zfight(im):
    """Z-fighting on the counter's front: jagged stripes of a paler surface through the wood."""
    im = im.copy()
    box = (812, 660, 962, 795)
    region = im.crop(box)
    L = lum(region)
    other = Image.merge("RGB", (L.point(lambda v: min(255, int(v * 1.7 + 30))),
                                L.point(lambda v: min(255, int(v * 1.5 + 22))),
                                L.point(lambda v: min(255, int(v * 1.1 + 10)))))
    rnd = random.Random(3)
    m = Image.new("L", region.size, 0)
    mp = m.load()
    offs, off = [], 0
    for _ in range(region.height):
        off = max(-6, min(6, off + rnd.randint(-2, 2)))
        offs.append(off + rnd.randint(0, 3))
    for y in range(region.height):
        for x in range(region.width):
            if ((x + int(0.7 * y) + offs[y]) // 9) % 3 == 0:
                mp[x, y] = 255
    region.paste(other, (0, 0), m)
    im.paste(region, box[:2])
    return im, box, "z-fighting: jagged pale stripes flicker through one panel of the counter's front"

def f_b03_blacksquare(im):
    im = im.copy()
    box = (448, 392, 506, 446)
    ImageDraw.Draw(im).rectangle(box, fill=(7, 7, 8))
    return im, box, "black square: a flat black block over the houses at the street's far end"


def f_b03_stretched(im):
    """One face's brick smeared sideways: a UV stretch."""
    im = im.copy()
    box = (1330, 120, 1530, 290)
    strip = im.crop((box[0], box[1], box[0] + 2, box[3]))
    im.paste(strip.resize((box[2] - box[0], box[3] - box[1]), Image.BILINEAR), box[:2])
    return im, box, "stretched texture: the brick on the corner house's side smeared into horizontal streaks"


def f_b04_floating(im):
    """The litter bin and its post lifted 55 px: the post's foot hangs above the pavement."""
    im = im.copy()
    src = im.copy()
    m = Image.new("L", im.size, 0)
    d = ImageDraw.Draw(m)
    d.rectangle((256, 608, 277, 785), fill=255)   # the post
    d.rectangle((268, 612, 336, 720), fill=255)   # the bin
    # where it stood: the stallriser and pavement 80 px to the right, 14 px lower (the street's slope)
    mp, sp, ip = m.load(), src.load(), im.load()
    for y in range(600, 790):
        for x in range(250, 340):
            if mp[x, y]:
                ip[x, y] = sp[x + 80, min(im.height - 1, y + 14)]
    lift = 55
    obj = src.crop((250, 600, 340, 790))
    om = m.crop((250, 600, 340, 790))
    im.paste(obj, (250, 600 - lift), om)
    return im, (250, 600 - lift, 340, 790), \
        "floating object: the litter bin and its post sit 55 px too high, the post's foot hanging above the pavement"

def f_b04_seam(im):
    """A dark seam down the slates, ridge to eaves."""
    im = im.copy()
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    d.line([(352, 128), (318, 292)], fill=(14, 14, 16, 225), width=4)
    im = Image.alpha_composite(im.convert("RGBA"), over).convert("RGB")
    return im, (314, 124, 356, 296), "a dark seam stripe down the roof's slates from ridge to eaves"


def f_b05_light(im):
    """A warm light on a blank dark wall, no lamp to cast it."""
    im = im.copy().convert("RGBA")
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    cx, cy, r = 1440, 175, 80
    px = over.load()
    for y in range(cy - r, cy + r):
        for x in range(cx - r, cx + r):
            dd = ((x - cx) ** 2 + ((y - cy) * 1.15) ** 2) ** 0.5 / r
            if dd < 1:
                a = int(255 * (1 - dd) ** 2.2)
                px[x, y] = (255, 178, 92, a)
    im = Image.alpha_composite(im, over)
    ImageDraw.Draw(im).ellipse((cx - 5, cy - 4, cx + 5, cy + 4), fill=(255, 238, 205, 255))
    return im.convert("RGB"), (cx - r, cy - r, cx + r, cy + r), \
        "light where none belongs: a warm glow on the blank upper wall of the corner house, no lamp"


def f_b05_debug(im):
    im = im.copy()
    d = ImageDraw.Draw(im)
    f = font(15)
    d.text((10, 8), "LIGHTING NEEDS TO BE REBUILT (37 unbuilt object(s))", fill=(255, 0, 0), font=f)
    d.text((10, 27), "'DisableAllScreenMessages' to suppress", fill=(255, 0, 0), font=f)
    return im, (8, 6, 470, 46), "debug text: the engine's red LIGHTING NEEDS TO BE REBUILT message top left"


def f_b06_pane(im):
    """One pane of the first-floor sash gone: a black void where the glass and blind were."""
    im = im.copy()
    box = (428, 204, 455, 254)
    ImageDraw.Draw(im).rectangle(box, fill=(10, 9, 9))
    return im, box, "missing window pane: the lower right pane of the middle first-floor window is a black hole"


def f_b06_duplicate(im):
    """The pillar box twice, the copy standing half into the first."""
    im = im.copy()
    box = (152, 500, 232, 664)
    crop = im.crop(box)
    px = crop.load()
    m = Image.new("L", crop.size, 0)
    mp = m.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b = px[x, y]
            if (r > g + 40 and r > b + 40) or (y >= 128 and 6 <= x <= 66 and r + g + b < 160):
                mp[x, y] = 255
    m = row_span(m)
    at = (box[0] + 46, box[1])
    im.paste(crop, at, m)
    return im, (box[0], box[1], at[0] + crop.width, box[3]), \
        "duplicated object: a second pillar box stands into the first, half overlapping it"

def f_b07_mirror(im):
    """The kiosk's 'Telephone' lettering flipped: the letters alone, on their own black panel."""
    im = im.copy()
    box = (652, 226, 764, 302)
    crop = im.crop(box)
    px = crop.load()
    m = Image.new("L", crop.size, 0)
    mp = m.load()
    for y in range(crop.height):
        for x in range(crop.width):
            r, g, b = px[x, y]
            if r > 90 and g > 70 and b < 0.6 * r:
                mp[x, y] = 255
    m = m.filter(ImageFilter.MaxFilter(3))
    panel = Image.new("RGB", crop.size, (16, 16, 17))
    clean = crop.copy()
    clean.paste(panel, (0, 0), m)
    flipped, fm = crop.transpose(Image.FLIP_LEFT_RIGHT), m.transpose(Image.FLIP_LEFT_RIGHT)
    fm = ImageChops.multiply(fm, m.point(lambda v: 255).transpose(Image.FLIP_LEFT_RIGHT))
    clean.paste(flipped, (0, 0), fm)
    im.paste(clean, box[:2])
    return im, box, "mirrored text: the kiosk's 'Telephone' sign reads backwards"

def f_b07_scale(im):
    """The blue-and-white vase in the window three times its size."""
    im = im.copy()
    box = (228, 534, 256, 576)
    crop = im.crop(box)
    m = Image.new("L", crop.size, 0)
    ImageDraw.Draw(m).ellipse((0, 0, crop.width - 1, crop.height - 1), fill=255)
    k = 3
    big = crop.resize((crop.width * k, crop.height * k), Image.LANCZOS)
    bm = m.resize(big.size, Image.LANCZOS).filter(ImageFilter.GaussianBlur(1))
    at = (box[0] + crop.width // 2 - big.width // 2, box[3] - big.height)
    im.paste(big, at, bm)
    return im, (at[0], at[1], at[0] + big.width, at[1] + big.height), \
        "wrong scale: one vase in the window three times the size of the goods around it"

def f_b08_fireflies(im):
    im = im.copy()
    rnd = random.Random(8)
    d = ImageDraw.Draw(im)
    spots = []
    for _ in range(26):
        spots.append((rnd.randint(20, 1090), rnd.randint(10, 150)))
    for _ in range(26):
        spots.append((rnd.randint(820, 1100), rnd.randint(160, 880)))
    for x, y in spots:
        s = rnd.choice([1, 1, 2])
        d.ellipse((x - s, y - s, x + s, y + s), fill=(255, 252, 240))
    return im, (20, 10, 1100, 880), "fireflies: about fifty bright white specks over the dark fascia and the kiosk's side"


def f_b08_prompt(im):
    im = im.copy().convert("RGBA")
    over = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(over)
    f = font(20)
    text = "[E]  Talk to Rita"
    w = d.textlength(text, font=f)
    x, y = 300, 700
    d.rounded_rectangle((x - 12, y - 8, x + w + 12, y + 30), radius=6, fill=(0, 0, 0, 150))
    d.text((x, y), text, fill=(255, 255, 255, 255), font=f)
    im = Image.alpha_composite(im, over)
    return im.convert("RGB"), (x - 12, y - 8, int(x + w + 12), y + 30), \
        "a floating 'Talk to Rita' prompt over the pavement with nobody there"


def f_b09_hole(im):
    """A ragged hole through the corner wall, the sky showing through, the wall's thickness at its edge."""
    im = im.copy()
    pts = [(392, 566), (420, 558), (447, 571), (452, 597), (436, 618), (407, 621), (388, 603), (384, 583)]
    d = ImageDraw.Draw(im)
    d.polygon(pts, fill=(78, 46, 36))
    inner = [(x + (4 if x < 418 else 1), y + (4 if y < 590 else 1)) for x, y in pts]
    d.polygon(inner, fill=(214, 216, 218))
    return im, (382, 556, 454, 623), "hole in a wall: a ragged hole through the corner wall with sky behind it"

def f_b09_tiling(im):
    """The corner wall's lower part made of one small stained tile repeated in a grid."""
    im = im.copy()
    tile = im.crop((392, 560, 462, 630))
    box = (306, 330, 500, 750)
    for y in range(box[1], box[3], 70):
        for x in range(box[0], box[2], 70):
            t = tile.crop((0, 0, min(70, box[2] - x), min(70, box[3] - y)))
            im.paste(t, (x, y))
    return im, box, "texture tiling: the corner wall's lower part is one small stained tile repeated in a grid, seams showing"

def f_b10_lowres(im):
    """The fish shop's upper brick not streamed in: blocky and blurred."""
    im = im.copy()
    boxes = [(338, 108, 414, 326), (492, 108, 625, 326)]
    for box in boxes:
        r = im.crop(box)
        small = r.resize((max(1, r.width // 11), max(1, r.height // 11)), Image.BILINEAR)
        im.paste(small.resize(r.size, Image.NEAREST).filter(ImageFilter.GaussianBlur(1.2)), box[:2])
    return im, (338, 108, 625, 326), "low-resolution texture: the fish shop's upper brick is blocky and blurred either side of its window"


def f_b10_grey(im):
    im = im.copy()
    box = (420, 143, 482, 258)
    ImageDraw.Draw(im).rectangle(box, fill=(126, 126, 126))
    return im, box, "untextured placeholder: the fish shop's upper window is a flat grey panel"


FAULTS = {
    "B01": [f_b01_floating, f_b01_testcolour],
    "B02": [f_b02_whitestrip, f_b02_zfight],
    "B03": [f_b03_blacksquare, f_b03_stretched],
    "B04": [f_b04_floating, f_b04_seam],
    "B05": [f_b05_light, f_b05_debug],
    "B06": [f_b06_pane, f_b06_duplicate],
    "B07": [f_b07_mirror, f_b07_scale],
    "B08": [f_b08_fireflies, f_b08_prompt],
    "B09": [f_b09_hole, f_b09_tiling],
    "B10": [f_b10_lowres, f_b10_grey],
}
KIND = {  # the fault's kind, as the task names it
    "f_b01_floating": "floating object", "f_b01_testcolour": "test-colour block",
    "f_b02_whitestrip": "white strip in a pane", "f_b02_zfight": "z-fighting",
    "f_b03_blacksquare": "black square", "f_b03_stretched": "stretched texture",
    "f_b04_floating": "floating object", "f_b04_seam": "seam stripe",
    "f_b05_light": "light where none belongs", "f_b05_debug": "debug text",
    "f_b06_pane": "missing window pane", "f_b06_duplicate": "duplicated object",
    "f_b07_mirror": "mirrored text", "f_b07_scale": "wrong scale",
    "f_b08_fireflies": "fireflies", "f_b08_prompt": "stray interface prompt",
    "f_b09_hole": "hole in a wall", "f_b09_tiling": "texture tiling",
    "f_b10_lowres": "low-resolution texture", "f_b10_grey": "untextured placeholder",
}


def main():
    repo, out = sys.argv[1], sys.argv[2]
    for sub in ("bases", "frames"):
        os.makedirs(os.path.join(out, sub), exist_ok=True)
    items = []
    for b, (name, crop, view) in BASES.items():
        im = Image.open(os.path.join(repo, "production", "previews", name)).convert("RGB")
        if crop:
            im = im.crop(crop)
        im.save(os.path.join(out, "bases", b + ".jpg"), quality=Q)
        base = Image.open(os.path.join(out, "bases", b + ".jpg")).convert("RGB")
        for fn in FAULTS[b]:
            pic, box, what = fn(base)
            items.append({"base": b, "fault": fn.__name__, "kind": KIND[fn.__name__], "box": list(box),
                          "what": what, "pic": pic, "area_pct": round(100.0 * (box[2] - box[0]) * (box[3] - box[1]) / (base.width * base.height), 2)})
        if b in CLEAN:
            items.append({"base": b, "fault": None, "kind": "clean", "box": None, "what": "clean", "pic": base, "area_pct": 0})
    random.Random(1990).shuffle(items)
    key = []
    for i, it in enumerate(items, 1):
        fname = "frame-%02d.jpg" % i
        it["pic"].save(os.path.join(out, "frames", fname), quality=Q)
        name, crop, view = BASES[it["base"]]
        key.append({"frame": fname, "base": it["base"], "source": name, "crop": crop, "view": view,
                    "fault": it["fault"], "kind": it["kind"], "box": it["box"], "what": it["what"],
                    "area_pct": it["area_pct"]})
    with open(os.path.join(out, "key.json"), "w") as fh:
        json.dump(key, fh, indent=1)
    print("%d frames, %d faulty, %d clean" % (len(key), sum(1 for k in key if k["fault"]), sum(1 for k in key if not k["fault"])))


if __name__ == "__main__":
    main()
