"""The wear layer's own pictures: soft puddle masks, made here (the proof frame, stage 1).

    python tools/make_wear_masks.py            # writes ledger/Assets/StreamingAssets/Decals/ours/puddle_0N/puddle_0N.png
    python tools/make_wear_masks.py --selftest

WHY, 1 October (the street research, production/research/aaa-street, item 3,
the wet street: "puddles from a soft mask"; and the wear layer of D53): a
puddle is where water stands in a dip, so its edge is soft and irregular, it
is darker and a near mirror inside, and it fades to merely wet at the rim.
The masks are white with the puddle in the alpha (the decal root's layout:
<id>/<leaf>.png), made from smoothed noise thresholded softly, seeded, so the
same files come out each run. Nothing downloaded: the free scans can replace
them later by changing a line in tools/street_wear.py.

AND THE STAINS' OWN PICTURES, 2 October. Every wear decal had been printing
ambientCG's PREVIEW render, the <id>.png beside each pack (a lit sphere on
black, Leaking005's on a checkerboard), so the stains were sphere-shaped
blobs. The packs' real masks are their Opacity maps. M_LedgerGrime reads a
stain as (1 - its brightness) x its alpha, so each picture here is a flat
dark grey with the mask in the alpha, stretched so its strongest twentieth
is full, and cropped or faded to the shape its decal takes: a leak's streaks
for sills and gables, splatter fading upward for the foot of a wall, mottled
grime for soot (fading down) and algae (fading up), and a soft blob, made
here like the puddles, for oil.
"""
import os
import sys

import numpy as np
from PIL import Image

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.join(REPO, "ledger", "Assets", "StreamingAssets", "Decals", "ours")
SIZE = 512
N = 3


def smooth_noise(rng, size, octaves=(8, 16, 32, 64)):
    """Value noise by summing upsampled random grids, smoothest octave strongest."""
    out = np.zeros((size, size))
    amp = 1.0
    for cells in octaves:
        g = rng.random((cells + 1, cells + 1))
        img = Image.fromarray((g * 255).astype(np.uint8)).resize((size, size), Image.BICUBIC)
        out += amp * (np.asarray(img).astype(float) / 255.0)
        amp *= 0.5
    return out / out.max()


def puddle(rng):
    yy, xx = np.mgrid[0:SIZE, 0:SIZE] / (SIZE - 1.0)
    # an oval falloff so the puddle never touches the decal's edge
    r = np.hypot((xx - 0.5) / 0.46, (yy - 0.5) / 0.40)
    base = np.clip(1.0 - r, 0.0, 1.0)
    n = smooth_noise(rng, SIZE)
    field = base * 1.35 + (n - 0.5) * 0.55
    # a soft threshold: water inside, a wet rim, dry outside
    # AN OPAQUE CORE AND A NARROW WET RIM (2 October, late; the puddle research): a decal
    # mixes its roughness and flat normal by its opacity, so a soft mask left most of each
    # puddle part road, and the mirror never formed. The rim is now a few centimetres.
    alpha = np.clip((field - 0.28) / 0.13, 0.0, 1.0)   # 3 October: at 0.06 the rims read as pasted-on edges (fresh review); an opaque core still
    return alpha


AMBIENTCG = os.path.join(REPO, "ledger", "Assets", "StreamingAssets", "Decals", "ambientcg")
STAIN_GREY = 64            # M_LedgerGrime: opacity is (1 - grey/255) x alpha x strength, the colour grey x the tint


def opacity_map(pack):
    """A pack's real mask, 0..1, its strongest twentieth stretched to full."""
    d = os.path.join(AMBIENTCG, pack)
    leaf = [f for f in os.listdir(d) if "_Opacity." in f][0]
    m = np.asarray(Image.open(os.path.join(d, leaf)).convert("L")).astype(float) / 255.0
    top = max(np.percentile(m, 95), 1e-3)
    return np.clip(m / top, 0.0, 1.0)


def strip(m, rows_per_col):
    """A band across the mask, as wide as the mask and 1/rows_per_col of its width tall."""
    h = max(8, int(m.shape[1] / rows_per_col))
    y0 = (m.shape[0] - h) // 2
    return m[y0:y0 + h, :]


def ramp(m, strong_at):
    """Fade a mask from full at one edge to a third at the other."""
    t = np.linspace(0.0, 1.0, m.shape[0])[:, None]
    g = 1.0 - 0.67 * (t if strong_at == "top" else 1.0 - t)
    return m * g


def soften(m, radius):
    """A mask blurred by radius pixels (PIL's Gaussian), 0..1."""
    from PIL import ImageFilter
    img = Image.fromarray((np.clip(m, 0, 1) * 255).astype(np.uint8), "L").filter(ImageFilter.GaussianBlur(radius))
    return np.asarray(img).astype(float) / 255.0


def stains(rng):
    """{leaf: mask} for every wear kind but water."""
    leak = opacity_map("Leaking005")
    grime = opacity_map("SurfaceImperfections003")
    splat = opacity_map("SurfaceImperfections012")
    out = {"wear_streak": leak[:, : leak.shape[1] // 3],            # narrow and tall, as under a sill
           "wear_wash": np.maximum(leak, ramp(np.asarray(Image.fromarray((grime * 255).astype(np.uint8)).resize(
               (leak.shape[1], leak.shape[0]))).astype(float) / 255.0, "top") * 0.8),
           # softened (3 October: the splatter read as polka dots on the stallrisers)
           "wear_splash": ramp(strip(soften(np.maximum(splat * 0.7, grime * 0.6), 6), 10.0), "bottom"),
           "wear_soot": ramp(strip(grime, 5.0), "top"),
           "wear_algae": ramp(strip(np.maximum(grime, splat), 4.0), "bottom"),
           # rising damp: mottled, strongest at the foot, a soft ragged top edge (2 October)
           "wear_damp": ramp(strip(grime, 6.0), "bottom") * np.clip(np.linspace(0.0, 1.6, max(8, int(grime.shape[1] / 6.0)))[:, None], 0.0, 1.0)}
    blob = puddle(rng) ** 0.7
    out["wear_oil"] = blob * np.clip(smooth_noise(rng, SIZE, (16, 32, 64, 128)) * 1.6 - 0.3, 0.0, 1.0)   # drips and smears, not a solid disc
    return out


def write_stains():
    for leaf, a in stains(np.random.default_rng(19901003)).items():
        img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
        if max(img.size) > 1024:
            k = 1024.0 / max(img.size)
            img = img.resize((max(8, int(img.size[0] * k)), max(8, int(img.size[1] * k))), Image.LANCZOS)
        rgba = Image.new("RGBA", img.size, (STAIN_GREY, STAIN_GREY, STAIN_GREY, 255))
        rgba.putalpha(img)
        d = os.path.join(ROOT, leaf)
        os.makedirs(d, exist_ok=True)
        rgba.save(os.path.join(d, leaf + ".png"))
        print("%s: %dx%d, mean mask %.2f" % (leaf, img.size[0], img.size[1], np.asarray(img).mean() / 255.0))


SCENE_STAINS = ("Leaking005", "AsphaltDamageSet001", "Sticker001", "Moss001")


def write_scene_stains():
    """The scene file's ten stains (VignetteShot SpawnStain) printed the same preview renders:
    each gets its pack's colour with its real mask in the alpha, as ours/stain_<pack>; Moss001
    has no mask of its own and takes the algae's."""
    for pack in SCENE_STAINS:
        d = os.path.join(AMBIENTCG, pack)
        colour = Image.open(os.path.join(d, [f for f in os.listdir(d) if "_Color." in f][0])).convert("RGB")
        if pack == "Moss001":
            mask = stains(np.random.default_rng(19901003))["wear_algae"]
        else:
            mask = np.asarray(Image.open(os.path.join(d, [f for f in os.listdir(d) if "_Opacity." in f][0])).convert("L")).astype(float) / 255.0
        a = Image.fromarray((np.clip(mask, 0, 1) * 255).astype(np.uint8), "L")
        w, h = a.size
        k = min(1.0, 1024.0 / max(w, h))
        a = a.resize((max(8, int(w * k)), max(8, int(h * k))), Image.LANCZOS)
        rgba = colour.resize(a.size, Image.LANCZOS).convert("RGBA")
        rgba.putalpha(a)
        leaf = "stain_" + pack
        os.makedirs(os.path.join(ROOT, leaf), exist_ok=True)
        rgba.save(os.path.join(ROOT, leaf, leaf + ".png"))
        print("%s: %dx%d" % (leaf, a.size[0], a.size[1]))


def write():
    rng = np.random.default_rng(19901002)
    for i in range(1, N + 1):
        a = puddle(rng)
        rgba = np.zeros((SIZE, SIZE, 4), dtype=np.uint8)
        rgba[..., :3] = 255
        rgba[..., 3] = (a * 255).astype(np.uint8)
        d = os.path.join(ROOT, "puddle_%02d" % i)
        os.makedirs(d, exist_ok=True)
        Image.fromarray(rgba, "RGBA").save(os.path.join(d, "puddle_%02d.png" % i))
        print("puddle_%02d: %.0f%% of the square is water or wet rim" % (i, 100.0 * (a > 0.05).mean()))
    write_stains()
    write_scene_stains()


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_wear_masks selftest FAIL " + what)
    rng = np.random.default_rng(19901002)
    a = puddle(rng)
    check("a puddle stays clear of the decal's edge", a[0, :].max() == 0 and a[-1, :].max() == 0 and a[:, 0].max() == 0 and a[:, -1].max() == 0)
    check("it has water inside and a soft rim", a.max() > 0.95 and ((a > 0.05) & (a < 0.95)).mean() > 0.02)
    check("it is a puddle, not the whole square", 0.1 < (a > 0.05).mean() < 0.8)
    b = puddle(np.random.default_rng(19901002))
    check("seeded: the same mask each run", np.array_equal(a, b))
    st = stains(np.random.default_rng(19901003))
    check("a stain picture for every wear kind but water", set(st) == {"wear_streak", "wear_wash", "wear_splash", "wear_soot", "wear_algae", "wear_oil", "wear_damp"})
    check("no stain is empty or solid", all(0.03 < v.mean() < 0.9 for v in st.values()))
    check("the splash band is strongest at its foot", st["wear_splash"][-len(st["wear_splash"]) // 4:].mean() > st["wear_splash"][: len(st["wear_splash"]) // 4].mean())
    check("an oil stain stays clear of its decal's edge", st["wear_oil"][0, :].max() == 0 and st["wear_oil"][:, 0].max() == 0)
    print("make_wear_masks selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    write()
