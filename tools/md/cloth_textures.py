"""Tileable cloth textures for the proof suit: the jacket's charcoal worsted twill, the shirt's pale blue cotton and
the tie's silk with a diagonal stripe; colour (sRGB) and normal (OpenGL: flip green for Unreal) maps, made from
numbers (no photograph, nothing to license).

    python tools/md/cloth_textures.py OUT_DIR [--size 1024]

OUT_DIR gets suit_jacket_basecolor.png, suit_jacket_normal.png, shirt_basecolor.png, shirt_normal.png,
tie_basecolor.png, tie_normal.png.

WHY, 2 October (the jacket proof): the jacket's UVMap runs one tile to 25 cm of cloth along the grain on every
piece (tools/md/finish_md_jacket.py), so one tileable twill covers it at one scale; a 1990 charcoal suit is a
worsted twill whose diagonal reads as a soft sheen at a few metres and as a weave close to, with a little heather
in the yarn. The tie's UVs run across and down its blade (tools/md/shirt_and_tie.py), so its stripe lies at 45
degrees as a regimental stripe does. Everything is periodic (sines on whole cycles, noise filtered in the frequency
domain) so the tiles meet without a seam.
"""
import os
import sys

import numpy as np
from PIL import Image

argv = sys.argv[1:]
OUT = argv[0]
N = int(argv[argv.index("--size") + 1]) if "--size" in argv else 1024
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(1990)
y, x = np.mgrid[0:N, 0:N] / N                      # 0..1 over the tile


def noise(scale_px, seed):
    """Tileable noise, its features about scale_px pixels, mean 0, deviation 1."""
    r = np.random.default_rng(seed).standard_normal((N, N))
    f = np.fft.fftfreq(N)
    fx, fy = np.meshgrid(f, f)
    k = np.sqrt(fx ** 2 + fy ** 2) * N
    filt = np.exp(-(k * scale_px / N * 4) ** 2)
    out = np.real(np.fft.ifft2(np.fft.fft2(r) * filt))
    return (out - out.mean()) / (out.std() + 1e-9)


def normal_from(h, strength):
    gx = (np.roll(h, -1, 1) - np.roll(h, 1, 1)) * 0.5 * strength
    gy = (np.roll(h, -1, 0) - np.roll(h, 1, 0)) * 0.5 * strength
    n = np.stack([-gx, gy, np.ones_like(h)], -1)          # OpenGL: green up
    n /= np.linalg.norm(n, axis=-1, keepdims=True)
    return ((n * 0.5 + 0.5) * 255).astype(np.uint8)


def save(name, rgb, nrm):
    Image.fromarray(np.clip(rgb * 255, 0, 255).astype(np.uint8)).save(os.path.join(OUT, name + "_basecolor.png"))
    Image.fromarray(nrm).save(os.path.join(OUT, name + "_normal.png"))


# THE JACKET: a 2/2 twill, its wale every 1.6 mm (160 cycles over a 25 cm tile), rising to the left as a right-hand
# twill does on the face; yarn by yarn variation and a faint heather
wales = 160
twill = np.sin(2 * np.pi * wales * (x + y)) * 0.5 + 0.5
yarn = noise(2, 1) * 0.25 + noise(10, 2) * 0.15
h = twill * 0.8 + yarn * 0.2
heather = noise(3, 3) * 0.035 + noise(40, 4) * 0.015
base = np.array([0.215, 0.218, 0.232])                   # charcoal, as stored (sRGB), about #373841
col = base[None, None, :] * (1 + heather[..., None] + (twill[..., None] - 0.5) * 0.08)
save("suit_jacket", col, normal_from(h, 6.0))

# THE SHIRT: pale blue oxford, a basket weave every 1 mm (250 cycles), white weft through blue warp
warp = np.sin(2 * np.pi * 250 * x) * 0.5 + 0.5
weft = np.sin(2 * np.pi * 250 * y) * 0.5 + 0.5
basket = (warp * weft + (1 - warp) * (1 - weft))
h = basket * 0.7 + noise(2, 5) * 0.15
blue = np.array([0.70, 0.78, 0.88])
white = np.array([0.93, 0.94, 0.95])
mix = (warp > 0.5)[..., None] * 0.45 + 0.35 + noise(3, 6)[..., None] * 0.03
col = blue * mix + white * (1 - mix)
save("shirt", col, normal_from(h, 3.0))

# THE TIE: burgundy silk with a navy and gold regimental stripe at 45 degrees, a fine twill in the silk
d = (x + y) % (1 / 6) * 6                                 # six stripe repeats across the tile, diagonal
ground = np.array([0.36, 0.07, 0.10])
navy = np.array([0.08, 0.10, 0.22])
gold = np.array([0.62, 0.48, 0.20])
col = np.broadcast_to(ground, (N, N, 3)).copy()
col[(d > 0.40) & (d < 0.58)] = navy
col[(d > 0.62) & (d < 0.66)] = gold
silk = np.sin(2 * np.pi * 400 * (x - y)) * 0.5 + 0.5
col *= (1 + (silk[..., None] - 0.5) * 0.06)
save("tie", col, normal_from(silk * 0.6 + noise(2, 7) * 0.1, 2.0))
print("TEXTURES", sorted(os.listdir(OUT)))
