"""The painted face of the fish market's A-board (AB1): the fish list in hand-painted capitals, by script.

    python -I tools/meshgen/blender/clutter/a_board_paint.py --out F:/LedgerTools/tmp/clutter/a-board/a_board_paint.png

The texture step of a_board.py (Blender's own Python has no PIL, so this runs
on the system's). Everything it paints is read from the target
(production/cloud-week/targets/street-dressing/a-board/target.json): the
leaf's outline (f_main and the two feet's polygons), the ply's off-white
(materials.ply_paint), the lines of text with their cap heights, tops,
alignments, margin and gap (text), and the wear (wear: a grey splash band to
150 mm, the lower arris and feet worn to bare ply, the arch dirty to its
flared edges, rust-brown weeping at the top edge and the right arris).

THE CANVAS. One image serves both leaves (the target: "the back leaf's lines
identical"); a_board.py maps it unmirrored onto each outer face, so on either
face the viewer's right is the image's right. The canvas is the leaf's width
by twice that (600 x 1200 mm), a power of two on each side at the default
2048 x 4096 (3.41 px per mm, the target's "3 px per mm" rounded up to the
power of two the asset checks ask for): the top 990 mm is the face, feet
included; the 210 mm below holds three strips for the unpainted surfaces
(the inner face and top edge in bare ply, the long cut edges with the ply's
laminations and their dark lower 40 mm, and the dirty foot soles and arch
cuts). The layout is written beside the image as JSON and a_board.py reads
it, so the two scripts never disagree about where a strip is.

THE HAND. Each letter is set one by one from the project's OFL font Oswald
(a narrow upright sans, the nearest to a signwriter's block capital among the
project's fonts), with the target's 2 to 3 percent unevenness of height, a
wandering baseline, a small lean per letter and uneven spacing; then the
strokes are brushed: blurred, pushed about by a fine noise and cut again at a
noisy level, so the edges waver and the strokes thicken and thin as a brush
does, and the black is laid at a slightly uneven density. Prices are the
target's own words (text.lines: cod sourced, the others marked invented
there); nothing is added to them.
"""
import argparse
import json
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
TARGET = os.path.join(REPO, "production", "cloud-week", "targets", "street-dressing", "a-board", "target.json")
FONT = os.path.join(REPO, "production", "fonts", "oswald", "Oswald[wght].ttf")

ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
ap.add_argument("--out", required=True, help="the PNG to write; its layout goes beside it as .json")
ap.add_argument("--target", default=TARGET)
ap.add_argument("--width", type=int, default=2048, help="image width in px (a power of two); the height is twice it")
ap.add_argument("--seed", type=int, default=1990)
ap.add_argument("--preview", help="optional JPEG of the face, 1024 wide, for looking at")
args = ap.parse_args()

T = json.load(open(args.target, encoding="utf-8"))
AB1 = {p["id"]: p for p in T["variants"]["AB1"]["parts"]}
MAIN = AB1["f_main"]
LEAF_W = MAIN["s"][0]                                  # 600
LEAF_TOP = MAIN["c"][2] + MAIN["s"][2] / 2.0           # 990, the leaf's own z of its top edge
ARCH_TOP = MAIN["c"][2] - MAIN["s"][2] / 2.0           # 58
CANVAS_H_MM = 2.0 * LEAF_W                             # 1200: the face plus 210 mm of strips
Z_CANVAS_BOTTOM = LEAF_TOP - CANVAS_H_MM               # -210
W = args.width
H = 2 * W
PPM = W / LEAF_W                                       # px per mm
rng = np.random.default_rng(args.seed)
SRGB_GROUND = np.array(T["materials"]["ply_paint"]["srgb"], np.float32)
TEXT = T["text"]

# the strips below the face, in canvas z (mm; the face is z 0 to 990): each band painted whole,
# a_board.py's UVs sample only the inner "use" part so the neighbours never bleed in
STRIPS = {
    "inner": {"band": [-100.0, 0.0], "use": [-90.0, -10.0], "what": "inner face and top edge: bare weathered ply"},
    "edge": {"band": [-155.0, -100.0], "use": [-145.0, -110.0], "what": "the long cut edges: laminations, the outer face at the use band's top, dark lower 40 mm at its left"},
    "dirty": {"band": [-210.0, -155.0], "use": [-200.0, -165.0], "what": "foot soles and the arch's cut faces: dirty bare ply"},
}
EDGE_DARK_MM = 40.0          # the target's wear: the lower 40 mm of the bare edge is dark
U_MARGIN = 0.02              # the strips' u range is [U_MARGIN, 1 - U_MARGIN]


def col(x_mm):
    """image column of a leaf x (viewer's left is -LEAF_W/2)"""
    return (x_mm + LEAF_W / 2.0) * PPM


def row(z_mm):
    return (LEAF_TOP - z_mm) * PPM


def noise(shape, cell_mm, aniso=(1.0, 1.0), ppm=None):
    """smooth zero-mean unit noise; cell size in mm along (x, z), times aniso"""
    h, w = shape
    ppm = ppm or PPM
    gx = max(3, int(w / (cell_mm * aniso[0] * ppm)) + 3)
    gy = max(3, int(h / (cell_mm * aniso[1] * ppm)) + 3)
    g = rng.standard_normal((gy, gx)).astype(np.float32)
    a = np.asarray(Image.fromarray(g, mode="F").resize((w, h), Image.BICUBIC), np.float32)
    return (a - a.mean()) / (a.std() + 1e-6)


def smoothstep(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0.0, 1.0)
    return t * t * (3 - 2 * t)


def over(img, rgb, alpha):
    a = np.clip(np.asarray(alpha, np.float32), 0.0, 1.0)[..., None]
    img *= (1.0 - a)
    img += a * np.asarray(rgb, np.float32)


# ------------------------------------------------------------------ the ground: chalking off-white over ply
img = np.empty((H, W, 3), np.float32)
img[:] = SRGB_GROUND
shape = (H, W)
grain = noise(shape, 2.5, (1.0, 24.0))            # the ply's face grain telegraphing up the leaf
mottle = noise(shape, 55.0)                       # chalking, uneven
brush = noise(shape, 1.5, (30.0, 1.0))            # the ground coat's brush marks, across, barely
fine = noise(shape, 0.5)
lum = 1.8 * mottle + 0.8 * grain + 0.35 * brush + 0.6 * fine
img += lum[..., None]
img[..., 2] += 0.6 * noise(shape, 80.0)           # a faint cool/warm drift, never a colour

# the leaf's outline (face part of the canvas): the panel above the arch and the two feet
outline = Image.new("L", (W, H), 0)
d = ImageDraw.Draw(outline)
d.rectangle([col(-LEAF_W / 2), row(LEAF_TOP), col(LEAF_W / 2), row(ARCH_TOP)], fill=255)
for fid in ("f_foot_l", "f_foot_r"):
    d.polygon([(col(x), row(z)) for x, z in AB1[fid]["poly"]], fill=255)
inside = np.asarray(outline, np.float32) / 255.0
face_rows = int(round(row(0.0)))
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
z_mm = LEAF_TOP - (yy + 0.5) / PPM
x_mm = (xx + 0.5) / PPM - LEAF_W / 2.0

# distance (mm) from each face pixel to the leaf's outline
pad = np.pad(inside[:face_rows] > 0.5, 1, constant_values=False)
dist = np.full(shape, 1e3, np.float32)
dist[:face_rows] = ndimage.distance_transform_edt(pad)[1:-1, 1:-1] / PPM

# ------------------------------------------------------------------ the lettering, letter by letter
SS = 2                                           # supersampling for the brush pass
lines = TEXT["lines"]
z_hi = max(l["z_top"] for l in lines) + 25.0
z_lo = min(l["z_top"] - l["h"] for l in lines) - 25.0
BAND_TOP_ROW = int(row(z_hi))
bh = int((z_hi - z_lo) * PPM * SS)
band = np.zeros((bh, W * SS), np.float32)
PPMS = PPM * SS
fonts = {}


def font(px, wght):
    k = (int(round(px)), wght)
    if k not in fonts:
        f = ImageFont.truetype(FONT, k[0])
        f.set_variation_by_axes([wght])
        fonts[k] = f
    return fonts[k]


def cap_ratio(wght):
    f = font(1000, wght)
    l, t, r, b = f.getbbox("H", anchor="ls")
    return -t / 1000.0


def set_word(word, x0_mm, base_z_mm, h_mm, wght, slope, wobble):
    """paint one run of letters starting at x0 (mm) on a baseline; returns its ink extent in mm"""
    size = h_mm * PPMS / cap_ratio(wght)
    x = x0_mm
    ink = [1e9, -1e9]
    for ch in word:
        f0 = font(size, wght)
        adv = f0.getlength(ch) / PPMS
        if ch != " ":
            dh = float(np.clip(rng.normal(0, 0.011), -0.028, 0.028))          # height, 2 to 3 percent
            f = font(size * (1 + dh), wght)
            asc, desc = f.getmetrics()
            padp = int(0.4 * size)
            gw = int(f.getlength(ch)) + 2 * padp
            gh = asc + desc + 2 * padp
            g = Image.new("L", (gw, gh), 0)
            ImageDraw.Draw(g).text((padp, padp + asc), ch, font=f, fill=255, anchor="ls")
            ang = float(rng.normal(0, 0.75)) + math.degrees(slope)
            capp = cap_ratio(wght) * size * (1 + dh)
            g = g.rotate(ang, resample=Image.BICUBIC, center=(gw / 2.0, padp + asc - capp / 2))
            xc = x + adv / 2.0
            bz = base_z_mm + slope * (xc - x0_mm) + wobble(xc) + float(rng.normal(0, 0.010 * h_mm))
            px = int(round((x + LEAF_W / 2.0) * PPMS)) - padp
            py = int(round((z_hi - bz) * PPMS)) - (padp + asc)
            a = np.asarray(g, np.float32) / 255.0
            y0, x0 = max(py, 0), max(px, 0)
            y1, x1 = min(py + gh, bh), min(px + gw, W * SS)
            band[y0:y1, x0:x1] = np.maximum(band[y0:y1, x0:x1], a[y0 - py:y1 - py, x0 - px:x1 - px])
            cols = np.nonzero(a.max(0) > 0.5)[0]
            if cols.size:
                ink[0] = min(ink[0], (px + cols[0]) / PPMS - LEAF_W / 2.0)
                ink[1] = max(ink[1], (px + cols[-1]) / PPMS - LEAF_W / 2.0)
        x += adv * (1 + float(rng.normal(0, 0.03))) + float(rng.normal(0, 0.012 * h_mm))
    return ink


def width_of(word, h_mm, wght):
    size = h_mm * PPMS / cap_ratio(wght)
    return font(size, wght).getlength(word) / PPMS


margin = TEXT["margin_mm"]
placed = []
for ln in lines:
    h = ln["h"]
    wght = 620 if ln["id"] == "head" else 560
    base = ln["z_top"] - h
    slope = math.radians(float(rng.normal(0, 0.22)))
    ph, amp, per = rng.uniform(0, 2 * math.pi), rng.uniform(0.004, 0.009) * h, rng.uniform(250, 450)
    wobble = (lambda ph, amp, per: (lambda xm: amp * math.sin(2 * math.pi * xm / per + ph)))(ph, amp, per)
    rec = {"id": ln["id"], "text": ln["text"], "price": ln["price"], "h_mm": h, "z_top_mm": ln["z_top"], "align": ln["align"]}
    if ln["align"] == "centre":
        w = width_of(ln["text"], h, wght)
        x0 = -w / 2.0 + float(rng.normal(0, 2.5))                       # centred by eye
        ink = set_word(ln["text"], x0, base, h, wght, slope, wobble)
    else:
        x0 = -LEAF_W / 2.0 + margin + abs(float(rng.normal(0, 1.5)))      # by eye, never past the margin
        ink = set_word(ln["text"], x0, base, h, wght, slope, wobble)
        wp = width_of(ln["price"], h, wght)
        xp = LEAF_W / 2.0 - margin - wp - abs(float(rng.normal(0, 2.0)))
        ink2 = set_word(ln["price"], xp, base + slope * (xp - x0), h, wght, slope, wobble)
        rec["gap_mm"] = round(ink2[0] - ink[1], 1)
        ink = [ink[0], ink2[1]]
    rec["ink_x_mm"] = [round(ink[0], 1), round(ink[1], 1)]
    rec["ink_width_mm"] = round(ink[1] - ink[0], 1)
    n_chars = len((ln["text"] + (ln["price"] or "")).replace(" ", ""))
    rec["advance_over_height"] = round((width_of(ln["text"].replace(" ", ""), h, wght)
                                        + (width_of(ln["price"].replace(" ", ""), h, wght) if ln["price"] else 0)) / n_chars / h, 3)
    placed.append(rec)

# the brush: blur, push the edges about, cut again at a wandering level
sig = 0.42 * PPMS
m = ndimage.gaussian_filter(band, sig)
del band
bshape = m.shape
coords = np.indices(bshape, dtype=np.float32)
coords[0] += PPMS * (0.30 * noise(bshape, 5.0, ppm=PPMS) + 0.05 * noise(bshape, 1.4, ppm=PPMS))
coords[1] += PPMS * (0.30 * noise(bshape, 5.0, ppm=PPMS) + 0.05 * noise(bshape, 1.4, ppm=PPMS))
m = ndimage.map_coordinates(m, coords, order=1, mode="nearest")
del coords
lvl = 0.5 + 0.08 * np.clip(noise(bshape, 9.0, ppm=PPMS), -2, 2)
a = smoothstep(lvl - 0.07, lvl + 0.07, m)
del m, lvl
a = a.reshape(bh // SS, SS, W, SS).mean(axis=(1, 3)) if bh % SS == 0 else \
    a[:bh - bh % SS].reshape(bh // SS, SS, W, SS).mean(axis=(1, 3))
r0 = BAND_TOP_ROW
r1 = r0 + a.shape[0]
ashape = a.shape
dens = 0.962 + 0.012 * np.clip(noise(ashape, 2.0, (1.0, 4.0)), -2, 2)     # brush drag, a little thin in places
pin = smoothstep(3.0, 3.6, noise(ashape, 0.6))                             # the rare pinhole where the ground shows
ink_alpha = a * dens * (1.0 - 0.3 * pin)
INK = np.array([27, 27, 25], np.float32)
sub = img[r0:r1]
over(sub, INK, ink_alpha)

# ------------------------------------------------------------------ the wear, light
facem = inside > 0.5
# the grey splash band from the paving, to 150 mm, streaked upward
prof = np.clip(1.0 - z_mm / 150.0, 0.0, 1.0) ** 1.7
streak = np.clip(0.55 + 0.35 * noise(shape, 2.0, (1.0, 14.0)) + 0.15 * noise(shape, 12.0), 0, 1)
splash = 0.30 * prof * streak
dots = Image.new("L", (W, H), 0)
dd = ImageDraw.Draw(dots)
for _ in range(800):
    zx = float(rng.exponential(28.0))
    if zx > 160:
        continue
    xm = float(rng.uniform(-LEAF_W / 2, LEAF_W / 2))
    rr = float(rng.uniform(0.2, 0.9)) * PPM
    cx, cy = col(xm), row(zx)
    dd.ellipse([cx - rr * rng.uniform(0.5, 1.0), cy - rr * rng.uniform(1.0, 2.2), cx + rr, cy + rr],
               fill=int(rng.uniform(35, 95)))
dots = dots.filter(ImageFilter.GaussianBlur(0.25 * PPM))
splash = np.maximum(splash, np.asarray(dots, np.float32) / 255.0 * np.clip(1.0 - z_mm / 170.0, 0, 1))
over(img, (118, 117, 110), splash * facem)
over(img, (96, 94, 88), 0.22 * np.clip(1.0 - z_mm / 22.0, 0, 1) * facem)            # the foot line's grime

# the feet's arch dirty to its flared edges, and the lower arris and the feet's edges worn to bare ply
arch = (z_mm < ARCH_TOP + 25.0) & (np.abs(x_mm) < 200.0)
dirt = 0.30 * np.clip(1.0 - dist / 18.0, 0, 1) * np.clip(0.6 + 0.4 * noise(shape, 4.0), 0, 1)
over(img, (104, 97, 86), dirt * arch * facem)
lowedge = z_mm < ARCH_TOP + 12.0
wornw = 2.6 * (1.0 + 0.55 * noise(shape, 6.0))
over(img, (168, 146, 114), 0.85 * smoothstep(0.6, 0.0, dist - wornw) * lowedge * facem)
allw = 0.6 * (1.0 + 0.8 * noise(shape, 5.0))                                       # the arrises everywhere, barely
over(img, (176, 158, 128), 0.30 * smoothstep(0.5, 0.0, dist - allw) * facem)

# rust-brown weeping from the glue line: the top edge and the right arris (the viewer's right on each face)
RUST = (124, 74, 40)
weep = 0.30 * np.exp(-(LEAF_TOP - z_mm) / 2.2) * np.clip(0.55 + 0.45 * noise(shape, 3.0, (4.0, 1.0)), 0, 1)
weep += 0.26 * np.exp(-(LEAF_W / 2.0 - x_mm) / 2.6) * np.clip(0.5 + 0.5 * noise(shape, 2.0, (1.0, 12.0)), 0, 1)
runs = []
for _ in range(8):                                  # short runs down from the top edge, clear of the heading
    runs.append((float(rng.uniform(-280, 280)), LEAF_TOP, float(rng.uniform(12, 52)), float(rng.uniform(1.2, 4.0)),
                 float(rng.uniform(0.14, 0.30))))
for _ in range(5):                                  # and from the right arris, running down beside it
    runs.append((LEAF_W / 2.0 - float(rng.uniform(1.0, 6.0)), float(rng.uniform(250, 960)),
                 float(rng.uniform(30, 120)), float(rng.uniform(1.5, 4.5)), float(rng.uniform(0.10, 0.22))))
for (rx, rz, length, wid, a0) in runs:
    c0, c1 = int(max(col(rx - 3 * wid - 2), 0)), int(min(col(rx + 3 * wid + 2), W))
    q0, q1 = int(max(row(rz), 0)), int(min(row(rz - length), H))
    if c1 <= c0 or q1 <= q0:
        continue
    zz, xx2 = z_mm[q0:q1, c0:c1], x_mm[q0:q1, c0:c1]
    t = np.clip((rz - zz) / length, 0, 1)
    xc = rx + 0.6 * np.sin((rz - zz) / 9.0)
    a_run = a0 * (1 - t) ** 1.3 * np.exp(-((xx2 - xc) / wid) ** 2) * (zz <= rz)
    weep[q0:q1, c0:c1] = np.maximum(weep[q0:q1, c0:c1], a_run)
over(img, RUST, np.clip(weep, 0, 0.42) * facem)

# off the leaf (the arch's opening): the dirty colour, so the arch's edges never filter towards white
over(img, (112, 104, 92), (~facem) & (np.arange(H)[:, None] < face_rows))

# ------------------------------------------------------------------ the strips below the face
def band_rows(b):
    return int(round(row(b[1]))), int(round(row(b[0])))


ply = np.array([164, 146, 120], np.float32)
s0, s1 = band_rows(STRIPS["inner"]["band"])
img[s0:s1] = ply + (2.5 * mottle[s0:s1] + 2.0 * noise((s1 - s0, W), 1.4, (1.0, 25.0)))[..., None]
e0, e1 = band_rows(STRIPS["edge"]["band"])
u0, u1 = band_rows(STRIPS["edge"]["use"])
t = np.clip((np.arange(e0, e1) - u0) / float(u1 - u0), 0, 1)                    # 0 at the outer face, 1 inner
plies = 7
lam = np.where((t * plies) % 1.0 < 0.13, 0.0, 1.0)                              # thin dark glue lines
shade = np.where(np.floor(t * plies) % 2 == 0, 1.0, 0.93)
edge = ply[None, :] * (0.72 + 0.28 * lam[:, None]) * shade[:, None] * 1.08
img[e0:e1] = np.clip(edge, 0, 255)[:, None, :] + 1.5 * fine[e0:e1, :, None]
paintwrap = smoothstep(0.09, 0.03, t)                                           # the paint over the outer arris
over(img[e0:e1], SRGB_GROUND, np.broadcast_to(paintwrap[:, None], (e1 - e0, W)) * 0.8)
u = (np.arange(W) + 0.5) / W
s_edge = (u - U_MARGIN) / (1 - 2 * U_MARGIN) * LEAF_TOP                          # the edge's own z along u
darkl = smoothstep(EDGE_DARK_MM + 6.0, EDGE_DARK_MM - 6.0, s_edge)
over(img[e0:e1], (70, 64, 56), np.broadcast_to(0.75 * darkl[None, :], (e1 - e0, W)))
c0r, c1r = band_rows(STRIPS["dirty"]["band"])
img[c0r:c1r] = np.array([112, 104, 92], np.float32) + (4.0 * noise((c1r - c0r, W), 6.0) + 1.5 * fine[c0r:c1r])[..., None]

out = np.clip(img + 0.5, 0, 255).astype(np.uint8)
os.makedirs(os.path.dirname(os.path.abspath(args.out)), exist_ok=True)
Image.fromarray(out, "RGB").save(args.out, optimize=True)

# the ground's measured mean, away from letters and wear (z 150 to 250 mm and 420 to 480, the middle 400 mm)
probe = ((z_mm > 160) & (z_mm < 280) | (z_mm > 430) & (z_mm < 490)) & (np.abs(x_mm) < 200)
gmean = out[probe].reshape(-1, 3).mean(0)
layout = {
    "image": [W, H], "px_per_mm": round(PPM, 4), "seed": args.seed,
    "font": os.path.relpath(FONT, REPO).replace("\\", "/"), "font_weights": {"head": 620, "lines": 560},
    "canvas_mm": [LEAF_W, CANVAS_H_MM], "canvas_z_bottom_mm": Z_CANVAS_BOTTOM,
    "face": {"x_mm": [-LEAF_W / 2.0, LEAF_W / 2.0], "z_mm": [0.0, LEAF_TOP],
             "u": "(x . viewer_right + width/2) / width", "v": "(z - canvas_z_bottom) / canvas_height"},
    "strips": STRIPS, "strip_u": [U_MARGIN, 1 - U_MARGIN], "edge_dark_mm": EDGE_DARK_MM,
    "ground_srgb_target": SRGB_GROUND.tolist(), "ground_srgb_measured": [round(float(c), 1) for c in gmean],
    "lines": placed, "fit_mm": LEAF_W - 2 * margin,
}
json.dump(layout, open(os.path.splitext(args.out)[0] + ".json", "w"), indent=1)
print("a_board_paint: %s %dx%d %.2f px/mm ground %s" % (args.out, W, H, PPM, layout["ground_srgb_measured"]))
for rec in placed:
    print("  %-8s %-22s %-9s ink %6.1f mm (fit %.0f)%s" % (rec["id"], rec["text"], rec["price"] or "", rec["ink_width_mm"],
                                                         LEAF_W - 2 * margin,
                                                         ("  gap %.1f" % rec["gap_mm"]) if "gap_mm" in rec else ""))
if args.preview:
    Image.fromarray(out[:face_rows]).resize((1024, int(face_rows * 1024 / W)), Image.LANCZOS).save(args.preview, quality=90)
