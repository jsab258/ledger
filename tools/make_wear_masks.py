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
    w3 = leak.shape[1] // 3
    # THREE STREAKS, strongest under the sill and fading down (4 October, the brick's second fresh
    # review: "one identical decal under every window ... darkest at the bottom"): the leak's three
    # thirds, each ramped from full at its top; tools/street_wear.py picks one a window by seed.
    out = {"wear_streak": ramp(leak[:, :w3], "top"),            # narrow and tall, as under a sill
           "wear_streak_b": ramp(leak[:, w3:2 * w3], "top"),
           "wear_streak_c": ramp(leak[:, 2 * w3:3 * w3], "top"),
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


def marks(rng):
    """{leaf: mask} for the marks of use, 6 October (item 1.1's gate: "the counter top clean: no
    scuffs, rings, burns"; "Rita's stallriser, pilaster feet, sills and door bottoms pristine"):
    tea rings where mugs stood, short burns where a cigarette rested on an edge, and paint chipped
    to the undercoat, densest at the foot."""
    n = SIZE
    yy, xx = np.mgrid[0:n, 0:n] / float(n - 1)
    out = {}
    ring = np.zeros((n, n))
    for cx, cy, r, w, k in ((0.30, 0.36, 0.13, 0.012, 1.0), (0.64, 0.58, 0.12, 0.010, 0.75),
                            (0.44, 0.74, 0.14, 0.014, 0.55)):
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        band = np.clip(1.0 - np.abs(d - r) / w, 0.0, 1.0)
        broken = np.clip(smooth_noise(rng, n, (8, 16)) * 1.8 - 0.35, 0.0, 1.0)
        ring = np.maximum(ring, band * broken * k)
    out["wear_rings"] = soften(ring, 1)
    burn = np.zeros((n, n))
    for cx, cy, ang, length in ((0.30, 0.50, 0.2, 0.20), (0.70, 0.42, -0.4, 0.14), (0.54, 0.26, 1.2, 0.11)):
        ux, uy = np.cos(ang), np.sin(ang)
        t = (xx - cx) * ux + (yy - cy) * uy
        q = -(xx - cx) * uy + (yy - cy) * ux
        along = np.clip(1.0 - np.abs(t) / (length / 2.0), 0.0, 1.0)
        burn = np.maximum(burn, np.clip(1.0 - np.abs(q) / (0.010 + 0.014 * along), 0.0, 1.0) * along)
    out["wear_burns"] = soften(burn, 1)
    flakes = (smooth_noise(rng, n, (32, 64, 128)) > 0.70).astype(float)
    out["wear_chips"] = ramp(soften(flakes, 1), "bottom")
    # WHERE HEADS AND HANDS REST, 26 October (item 5, Mickey's office: the heads behind the bench
    # printed the street's rising-damp strip, whose straight sides and top read as three stuck-on
    # rectangles): an oval smudge, darkest a little above its middle where the head rests, mottled,
    # and fading to nothing at every edge, so no side of the decal can show
    d = np.sqrt(((xx - 0.5) / 0.40) ** 2 + ((yy - 0.42) / 0.36) ** 2)
    oval = np.clip(1.0 - d, 0.0, 1.0) ** 1.4
    mottle = 0.55 + 0.45 * np.clip(smooth_noise(rng, n, (8, 16, 32)) * 1.4 - 0.2, 0.0, 1.0)
    out["wear_head"] = soften(oval * mottle, 6)
    # DAMP COME THROUGH FROM ABOVE, 26 October (the same pass: the corner's leak photograph, cropped,
    # read as a streaked rectangle under the ceiling): a pale stain with a darker tide line at its
    # ragged edge, as water dries back, clear of the decal's edges on every side
    r = np.hypot((xx - 0.5) / 0.44, (yy - 0.45) / 0.40)
    field = np.clip(1.0 - r, 0.0, 1.0) * 1.3 + (smooth_noise(rng, n, (8, 16, 32)) - 0.5) * 0.45
    # (the second try, the same afternoon: a fresh reviewer read the first, a flat fill with a faint tide
    # line, as a cut-out shape: now the fill is faint and fades to nothing toward the middle, and the
    # tide lines carry it, the outer one strongest, two fainter ones inside where it dried back)
    edge = 0.30                                                        # where the water stopped
    inside = np.clip((field - edge) / 0.30, 0.0, 1.0)
    fill = np.where(field > edge, 0.22 * (1.0 - inside) ** 1.5, 0.0)
    rings = np.zeros_like(field)
    for off, width, k in ((0.012, 0.022, 1.0), (0.09, 0.016, 0.45), (0.17, 0.014, 0.30)):
        rings = np.maximum(rings, k * np.clip(1.0 - np.abs(field - edge - off) / width, 0.0, 1.0))
    out["wear_damp_patch"] = soften(np.maximum(fill, rings), 2.5)
    # WHERE A NOTICE HUNG AND WAS TAKEN DOWN, 29 October (his order D11, the office's decals, O2: "pale patches
    # behind the calendar and notices"): the paint it covered stayed unfaded, so a pale oblong with a soft edge a
    # centimetre or two wide, a little uneven inside, and the four corners where tape held it a touch stronger;
    # clear of the decal's edges on every side (laid with M_LedgerStain's TintOnly, so it lightens)
    inset = 0.10
    ex = np.clip(np.minimum(xx - inset, 1.0 - inset - xx) / 0.035, 0.0, 1.0)
    ey = np.clip(np.minimum(yy - inset, 1.0 - inset - yy) / 0.035, 0.0, 1.0)
    oblong = ex * ey * (0.80 + 0.20 * np.clip(smooth_noise(rng, n, (8, 16, 32)) * 1.4 - 0.2, 0.0, 1.0))
    for cx, cy in ((inset + 0.04, inset + 0.04), (1 - inset - 0.04, inset + 0.04), (inset + 0.04, 1 - inset - 0.04), (1 - inset - 0.04, 1 - inset - 0.04)):
        oblong = np.maximum(oblong, 0.95 * np.clip(1.0 - np.hypot(xx - cx, yy - cy) / 0.035, 0.0, 1.0))
    out["wear_pale"] = soften(oblong, 2)
    # TOBACCO SMOKE UNDER THE CEILING, 29 October (his order D11, the office, O1; production/research/street-wear/
    # MAFIA-WEAR-2026-10-28.md: "full at the ceiling, none 1.2 m above the floor, yellow-brown ... the edge broken by
    # the plaster's own texture"): the decal spans a wall from 1.2 m up to the ceiling, so the picture's top row is
    # the ceiling's edge and its bottom row the line where the smoke gives out; full at the top, falling off softly,
    # the line it gives out at wandering a few centimetres with a broad noise, mottled a little inside; its two
    # sides fade over their outer 1.5% so the room's corners show no edge
    wander = (smooth_noise(rng, n, (4, 8)) - 0.5) * 0.16
    t = np.clip(yy + wander, 0.0, 1.0)
    fall = np.clip(1.0 - t, 0.0, 1.0) ** 1.6
    grain = 0.85 + 0.15 * np.clip(smooth_noise(rng, n, (16, 32, 64)) * 1.4 - 0.2, 0.0, 1.0)
    sides = np.clip(np.minimum(xx, 1.0 - xx) / 0.015, 0.0, 1.0)
    smoke = soften(fall * grain, 2) * sides                              # the sides after the blur, or it fills them
    # (29 October: the first prints hung upside down, as every wall mark had; the game's spawner now prints a wall
    # picture's first row at the mark's top, VignetteShot.cpp SpawnWear, so the smoke is drawn the right way up)
    smoke[-2:, :] = 0.0                                                  # nothing at the foot's own row
    out["wear_smoke"] = smoke
    return out


def write_marks():
    for leaf, a in marks(np.random.default_rng(19901006)).items():
        img = Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8), "L")
        rgba = Image.new("RGBA", img.size, (STAIN_GREY, STAIN_GREY, STAIN_GREY, 255))
        rgba.putalpha(img)
        d = os.path.join(ROOT, leaf)
        os.makedirs(d, exist_ok=True)
        rgba.save(os.path.join(d, leaf + ".png"))
        print("%s: %dx%d, mean mask %.3f" % (leaf, img.size[0], img.size[1], np.asarray(img).mean() / 255.0))


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


#: THE CHANDLER'S NEW MARKS' PICTURES (30 October 2026, his order D11; production/research/street-wear/
#: MAFIA-WEAR-2026-10-28.md, "One shop front: the chandler", S1): a rust leak under the gutter's end and the grime
#: trodden onto the footway at its two doors. Drawn here from two CC0 ambientCG maps already staged and credited
#: (Leaking005's opacity, SurfaceImperfections003's; THIRD-PARTY.md, "Grime and decal textures"), nothing fetched.
#: They live in production/assets/street-wear/<leaf>/<leaf>.png (the wear file names them by that path; VignetteShot.cpp
#: SpawnWear reads a "production/" picture from the repository's root, or the packaged copy's staged one).
STREET_WEAR_DIR = os.path.join(REPO, "production", "assets", "street-wear")
#: Mafia's rust leak, 2.1 m tall by 0.55 m (the study's sizes, M), at the leak map's own 1,024 rows for its length:
#: 488 px/m both ways, within 20% of the 512 px/m the method asks outside (C6)
RUST_SIZE_M = (0.55, 2.1)
#: the threshold's decal, 1.9 m along the front (both doors, x 43.70 to 45.60) by 0.9 m out from it: 1,024 by 512, 539
#: and 569 px/m
THRESHOLD_SIZE_M = (1.9, 0.9)
#: where each door's middle falls across the threshold picture, from its left column (a ground decal's columns run
#: toward higher street x and its rows toward the front: measured in the game's roughness view, 30 October): the cloud
#: front's shop door (x 43.76 to 44.63) and side door (44.73 to 45.55), read off its own pictures (shop-interiors.json:
#: the doors at the viewer's left, x 43.7 to 46; the piece list's doors at x 40.8 and 41.6 are the old refit's), the
#: decal's low edge at x 43.70
THRESHOLD_DOORS = ((0.263, 0.115, 1.0), (0.758, 0.108, 0.6))   # (centre, half its width over the decal's, weight)
#: rust as it stains brick: a dark iron brown at the run, a little more orange where it spreads (sRGB)
RUST_CORE, RUST_EDGE = (96, 46, 22), (128, 66, 32)


def rust_leak():
    """(alpha 0..1, rgb 0..255): a run from one point under the gutter's end, narrow at its head and spreading as it
    falls, strongest at the top and fading out by its foot, its edge and runs the leak map's own."""
    leak = opacity_map("Leaking005")
    h = leak.shape[0]
    w = int(round(h * RUST_SIZE_M[0] / RUST_SIZE_M[1]))
    # the strip of the leak with the most run in its top third, so the head is a leak and not a blank
    best, x0 = -1.0, 0
    for x in range(0, leak.shape[1] - w, 16):
        s = leak[: h // 3, x:x + w].mean()
        if s > best:
            best, x0 = s, x
    # its upper three fifths, where the map's runs are, drawn the leak's whole length (below them the map is nearly
    # empty, and the rust runs the whole 2.1 m)
    m = np.asarray(Image.fromarray((leak[: int(h * 0.6), x0:x0 + w] * 255).astype(np.uint8)).resize((w, h), Image.BICUBIC)).astype(float) / 255.0
    # each row's runs stretched to its own strongest tenth: the map's leaks thin out in its lower half, and the rust
    # runs the whole 2.1 m, its fading left to `along`
    m = np.clip(m / np.maximum(np.percentile(m, 90, axis=1, keepdims=True), 0.2), 0.0, 1.0)
    t = np.linspace(0.0, 1.0, h)[:, None]
    u = np.linspace(-0.5, 0.5, w)[None, :]
    sigma = 0.07 + 0.22 * t                          # narrow at the head, wider at the foot
    across = np.exp(-0.5 * (u / sigma) ** 2)
    along = np.clip(t / 0.03, 0.0, 1.0) * (1.0 - 0.8 * t)   # a soft start under the gutter, a third left at its foot
    core = np.exp(-0.5 * (u / (0.035 + 0.05 * t)) ** 2) * (1.0 - 0.7 * t)
    a = np.clip((m * 1.2 * across + 0.55 * core * (0.4 + 0.6 * m)) * along, 0.0, 1.0)
    a *= np.clip((1.0 - t) / 0.06, 0.0, 1.0)         # nothing at the foot's last rows
    a *= np.clip((0.5 - np.abs(u)) / 0.06, 0.0, 1.0)  # nor at its sides
    k = np.clip(core * 1.4, 0.0, 1.0)[..., None]
    rgb = np.array(RUST_EDGE, dtype=float) * (1.0 - k) + np.array(RUST_CORE, dtype=float) * k
    return a, rgb


def threshold():
    """alpha 0..1: dirt trodden out from two doors onto the footway, strongest at the doors (the picture's last rows),
    gone a stride out, the shop door's heavier than the side door's, mottled by SurfaceImperfections003."""
    W, H = 1024, 512
    g = np.asarray(Image.fromarray((opacity_map("SurfaceImperfections003") * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)).astype(float) / 255.0
    u = np.linspace(0.0, 1.0, W)[None, :]
    v = np.linspace(0.0, 1.0, H)[:, None]
    lobes = np.zeros((H, W))
    for c, half, weight in THRESHOLD_DOORS:
        spread = half * (0.7 + 0.8 * (1.0 - v))     # wider as it goes out from the door, soft-sided
        lobes = np.maximum(lobes, weight * np.exp(-0.5 * ((u - c) / spread) ** 2))
    # gone toward the road, full at the door, its outer edge broken by the mottle rather than a line
    out = np.clip(np.clip((v - 0.05) / 0.95, 0.0, 1.0) ** 1.4 + 0.3 * (g - 0.5), 0.0, 1.0)
    a = np.clip(lobes * out * (0.45 + 0.75 * g), 0.0, 1.0)
    a *= np.clip(np.minimum(u, 1.0 - u) / 0.05, 0.0, 1.0) * np.clip(v / 0.12, 0.0, 1.0)   # no edge toward the road
    return a


def street_wear_pictures():
    """{leaf: (alpha, rgb or None)} for the chandler's new marks."""
    a, rgb = rust_leak()
    return {"wear_rust": (a, rgb), "wear_threshold": (threshold(), None)}


def write_street_wear(out_dir=STREET_WEAR_DIR):
    for leaf, (a, rgb) in street_wear_pictures().items():
        h, w = a.shape
        px = np.zeros((h, w, 4), dtype=np.uint8)
        px[..., :3] = STAIN_GREY if rgb is None else np.clip(rgb, 0, 255).astype(np.uint8)
        px[..., 3] = (np.clip(a, 0, 1) * 255).astype(np.uint8)
        d = os.path.join(out_dir, leaf)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, leaf + ".png")
        Image.fromarray(px, "RGBA").save(p, optimize=True)
        print("%s: %dx%d, mean mask %.3f, %d KB" % (leaf, w, h, a.mean(), os.path.getsize(p) // 1024))


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
    write_marks()


def selftest():
    ok = bad = 0

    def check(what, cond):
        nonlocal ok, bad
        ok, bad = (ok + 1, bad) if cond else (ok, bad + 1)
        if not cond:
            print("make_wear_masks selftest FAIL " + what)
    hd = marks(np.random.default_rng(19901006))["wear_head"]
    check("a head's smudge fades to nothing at every edge", max(hd[0, :].max(), hd[-1, :].max(), hd[:, 0].max(), hd[:, -1].max()) < 0.02)
    check("and is dark enough inside to show", hd.max() > 0.5)
    dp = marks(np.random.default_rng(19901006))["wear_damp_patch"]
    check("a damp patch fades to nothing at every edge", max(dp[0, :].max(), dp[-1, :].max(), dp[:, 0].max(), dp[:, -1].max()) < 0.02)
    check("its tide line darker than its middle", dp.max() > 0.6 and dp[SIZE // 2, SIZE // 2] < dp.max() * 0.7)
    pl = marks(np.random.default_rng(19901006))["wear_pale"]
    check("a notice's pale patch fades to nothing at every edge", max(pl[0, :].max(), pl[-1, :].max(), pl[:, 0].max(), pl[:, -1].max()) < 0.02)
    check("and is a filled oblong, strong in its middle", pl[SIZE // 2, SIZE // 2] > 0.75 and (pl > 0.5).mean() > 0.45)
    sm = marks(np.random.default_rng(19901006))["wear_smoke"]
    check("smoke is full under the ceiling (the picture's first rows: the mark's top)", sm[4:20, SIZE // 4:3 * SIZE // 4].mean() > 0.7)
    check("and gives out at its foot", sm[-3:, :].max() < 0.05 and sm[3 * SIZE // 4, :].mean() < 0.25)
    check("its sides fade so the corners show no edge", max(sm[:, 0].max(), sm[:, -1].max()) < 0.1)
    rng = np.random.default_rng(19901002)
    a = puddle(rng)
    check("a puddle stays clear of the decal's edge", a[0, :].max() == 0 and a[-1, :].max() == 0 and a[:, 0].max() == 0 and a[:, -1].max() == 0)
    check("it has water inside and a soft rim", a.max() > 0.95 and ((a > 0.05) & (a < 0.95)).mean() > 0.02)
    check("it is a puddle, not the whole square", 0.1 < (a > 0.05).mean() < 0.8)
    b = puddle(np.random.default_rng(19901002))
    check("seeded: the same mask each run", np.array_equal(a, b))
    st = stains(np.random.default_rng(19901003))
    check("a stain picture for every wear kind but water", set(st) == {"wear_streak", "wear_streak_b", "wear_streak_c", "wear_wash", "wear_splash", "wear_soot", "wear_algae", "wear_oil", "wear_damp"})
    check("no stain is empty or solid", all(0.03 < v.mean() < 0.9 for v in st.values()))
    check("the splash band is strongest at its foot", st["wear_splash"][-len(st["wear_splash"]) // 4:].mean() > st["wear_splash"][: len(st["wear_splash"]) // 4].mean())
    check("an oil stain stays clear of its decal's edge", st["wear_oil"][0, :].max() == 0 and st["wear_oil"][:, 0].max() == 0)
    sw = street_wear_pictures()
    ra = sw["wear_rust"][0]
    rh, rw = ra.shape
    check("the rust leak keeps Mafia's 2.1 by 0.55 m and 512 px/m within 20% both ways",
          abs(rw / float(rh) - RUST_SIZE_M[0] / RUST_SIZE_M[1]) < 0.01 and all(410 <= n / m <= 615 for n, m in ((rh, RUST_SIZE_M[1]), (rw, RUST_SIZE_M[0]))))
    check("the rust runs from its head and is fainter at its foot, nothing at its sides or last rows",
          ra[: rh // 4].mean() > 2.0 * ra[3 * rh // 4:].mean() and ra[-2:, :].max() < 0.01 and max(ra[:, 0].max(), ra[:, -1].max()) < 0.01)
    check("narrower at its head than its foot", (ra[rh // 10] > 0.05).mean() < (ra[7 * rh // 10] > 0.05).mean())
    ta = sw["wear_threshold"][0]
    th, tw = ta.shape
    check("the threshold is strongest at the doors (its last rows) and gone toward the road", ta[-th // 5:].mean() > 4.0 * ta[: th // 5].mean() + 1e-6)
    shop, side = (ta[-th // 4:, int(c * tw) - 20:int(c * tw) + 20].mean() for c, _h, _w in THRESHOLD_DOORS)
    check("the shop door's threshold darker than the side door's", shop > side > 0.05)
    check("and nothing at its edges but the door's", max(ta[0, :].max(), ta[:, 0].max(), ta[:, -1].max()) < 0.01)
    check("seeded and drawn the same each run", np.array_equal(ra, street_wear_pictures()["wear_rust"][0]))
    print("make_wear_masks selftest: passed=%d/%d failed=%d" % (ok, ok + bad, bad))
    return 1 if bad else 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    # --street-wear (30 October): the chandler's two new pictures only, into production/assets/street-wear; the
    # decal root's own pictures are left as they are
    if "--street-wear" in sys.argv:
        write_street_wear()
        sys.exit(0)
    write()
