"""Makes the reviewers' previews of the pillar box target (JPEG, at most 1200 px, under 300 KB) in production/previews/cloud-week/refs/pillar-box/.

    /home/user/.bpyenv/bin/python make_previews.py

There is NO photograph of a pillar box to preview and so no target-on-photo overlay: the previews are the DRAWING made from target.json (own work, no licence),
and a swatch sheet of the red dry, wet and under the 589 nm lantern. Each picture says so in its caption.
"""
import json
import math
import os
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "production/previews/cloud-week/refs/pillar-box")
T = json.load(open(os.path.join(HERE, "target.json")))
tmp = tempfile.mkdtemp(prefix="pbprev_")
subprocess.run([sys.executable, "-I", os.path.join(HERE, "target_drawing.py"), "--target", os.path.join(HERE, "target.json"), "--json", os.path.join(tmp, "d.json"), "--pics", tmp], check=True)
os.makedirs(OUT, exist_ok=True)
font = ImageFont.load_default()
BG = (244, 241, 236)


def save(im, name, maxside=1200, q=88):
    s = maxside / max(im.size)
    if s < 1:
        im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    p = os.path.join(OUT, name)
    for qq in (q, 82, 76, 70, 62):
        im.convert("RGB").save(p, "JPEG", quality=qq, optimize=True)
        if os.path.getsize(p) < 290 * 1024:
            break
    print(name, im.size, os.path.getsize(p))


def caption(im, text):
    import textwrap
    lines = textwrap.wrap(text, max(20, im.width // 6 - 2))
    pad = 10 + 13 * len(lines)
    out = Image.new("RGB", (im.width, im.height + pad), BG)
    out.paste(im, (0, pad))
    d_ = ImageDraw.Draw(out)
    for i, ln in enumerate(lines):
        d_.text((6, 6 + 13 * i), ln, fill=(30, 30, 34), font=font)
    return out


fe = Image.open(os.path.join(tmp, "front_elevation.png"))
se = Image.open(os.path.join(tmp, "side_elevation.png"))
sec = Image.open(os.path.join(tmp, "axial_section.png"))
plans = Image.open(os.path.join(tmp, "plans.png"))

pair = Image.new("RGB", (fe.width + se.width + 10, fe.height), BG)
pair.paste(fe, (0, 0)); pair.paste(se, (fe.width + 10, 0))
sys.path.insert(0, HERE)
import target_drawing as TD  # noqa: E402
levels = TD.plan_levels(TD.Box(T))
save(caption(pair, "DRAWING from target.json (not a photograph): front and side elevation, 1 mm a pixel before reduction. 489 body, 576 foot, 560 cap, 1500 high, red 150/30/32, black band 200. The cypher and lettering areas are flush (tinted here only to show where)."), "target-quay-street-elevations.jpg")
save(caption(plans, "DRAWING from target.json (not a photograph): plans at " + ", ".join(f"z {z} ({n.replace('_', ' ')})" for n, z in levels) + ". Front up the page."), "target-quay-street-plans.jpg")
save(caption(sec, "DRAWING from target.json: section through the axis, front to the right"), "target-quay-street-axial-section.jpg")

# swatches
cr = T["paint"]["colour_reading"]
red = tuple(T["paint"]["red"]["srgb"])
wet = tuple(cr["wet"]["albedo_srgb"])
black = tuple(T["paint"]["black_base"]["srgb"])
enamel = tuple(T["paint"]["plate_enamel"]["srgb"])
lamp = cr["sodium"]["lamp_linear_srgb"]


def l2s(x):
    x = max(0.0, min(1.0, x))
    return round(255 * (12.92 * x if x <= 0.0031308 else 1.055 * x ** (1 / 2.4) - 0.055))


white_lamp = tuple(l2s(0.85 * c) for c in lamp)
sp = cr["sodium"]["spectral_reading"]["12.0"]["lit_srgb_at_lamp_x1"]
up_r = cr["sodium"]["fits"]["12.0"]["reflectance_589_edge_12nm_bluer"]
sp_up = tuple(l2s(up_r * c) for c in lamp)
naive = tuple(cr["sodium"]["naive_rgb_multiply"]["lit_srgb"])
cells = [("red, dry, overcast (albedo)", red), ("red, wet (x 0.88)", wet), ("black base band", black), ("plate enamel", enamel),
         ("WHITE surface under the 589 nm lamp", white_lamp), ("box under the lamp: spectral, fitted edge", tuple(sp)), ("box under the lamp: spectral, edge 12 nm bluer", sp_up),
         ("box under the lamp: RGB product (what an RGB engine gives)", naive)]
W, H = 1200, 520
im = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(im)
cw = W // 4
for i, (label, c) in enumerate(cells):
    x0 = (i % 4) * cw; y0 = (i // 4) * 250 + 20
    d.rectangle([x0 + 8, y0, x0 + cw - 8, y0 + 170], fill=tuple(c))
    d.text((x0 + 10, y0 + 176), label, fill=(30, 30, 34), font=font)
    d.text((x0 + 10, y0 + 192), f"sRGB {c[0]}/{c[1]}/{c[2]}", fill=(30, 30, 34), font=font)
d.text((8, 4), "SWATCHES computed in make_target.py (not photographs). Under a monochromatic 589 nm lamp a red box is a dark olive-brown, about 0.09 to 0.23 as bright as white; an RGB engine keeps it red.", fill=(30, 30, 34), font=font)
save(im, "target-quay-street-red-dry-wet-sodium.jpg")
