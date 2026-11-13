"""Contact sheet of the HumanMotionCraft body films (13 Nov 2026): one row per move and view, six moments each.

    python tools/tool-tests/hmc_sheet.py <film dir> <out.jpg> [width]

Rows: sit and stand (average body, side), sit and stand (Rocco, a heavier cast body, side), counter lean (average, side and front),
bus-stop smoke (average, front and side). Each row labelled; a JPEG under 500 KB at the given width (default 1600).
"""
import os
import sys

from PIL import Image, ImageDraw

film, out = sys.argv[1], sys.argv[2]
width = int(sys.argv[3]) if len(sys.argv) > 3 else 1600
ROWS = [("a_average", "side", "sit and stand, average body, side"),
        ("a_rocco", "side", "sit and stand, heavier cast body (Rocco), side"),
        ("b_average", "side", "counter lean, average body, side"),
        ("b_average", "front", "counter lean, average body, front"),
        ("c_average", "front", "bus-stop smoke, average body, front"),
        ("c_average", "side", "bus-stop smoke, average body, side")]
cell_w = width // 6
cell_h = int(cell_w * 800 / 600)
label_h = 22
sheet = Image.new("RGB", (cell_w * 6, (cell_h + label_h) * len(ROWS)), (235, 235, 235))
d = ImageDraw.Draw(sheet)
for r, (name, view, label) in enumerate(ROWS):
    y = r * (cell_h + label_h)
    d.text((6, y + 4), "HumanMotionCraft on MetaHuman (Unreal retarget): " + label, fill=(20, 20, 20))
    for k in range(6):
        p = os.path.join(film, "%s_%s_%d.png" % (name, view, k))
        if os.path.isfile(p):
            im = Image.open(p).convert("RGB").resize((cell_w, cell_h), Image.LANCZOS)
            sheet.paste(im, (k * cell_w, y + label_h))
q = 85
while True:
    sheet.save(out, "JPEG", quality=q, optimize=True)
    if os.path.getsize(out) < 500 * 1024 or q <= 40:
        break
    q -= 5
print("hmc_sheet:", out, sheet.size, os.path.getsize(out) // 1024, "KB, quality", q)
