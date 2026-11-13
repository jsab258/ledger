"""Stills and drift for one clip of the motion experiment (9 Nov).
    python check_clip.py out/m2-81f-s2202.webm
Renders stills 1, 11, ... and the last through portable Blender's sequencer (blender_stills.py), writes
<clip>-frames/sheet.jpg, and prints the floor line's row per still (camera drift; the shot list allows 2 px)."""
import os, subprocess, sys
import numpy as np
from PIL import Image
HERE = os.path.dirname(os.path.abspath(__file__))
BLENDER = r"F:\LedgerTools\blender52\blender-5.2.2-windows-x64\blender.exe"
clip = os.path.abspath(os.path.join(HERE, sys.argv[1]))
out = clip.rsplit(".", 1)[0] + "-frames"
os.makedirs(out, exist_ok=True)
subprocess.run([BLENDER, "-b", "--factory-startup", "--python", os.path.join(HERE, "blender_stills.py"), "--", clip, out],
               check=True, capture_output=True)
fs = sorted(f for f in os.listdir(out) if f.startswith("f") and f.endswith(".png"))
ims = [Image.open(os.path.join(out, f)).convert("RGB") for f in fs]
w, h = ims[0].size
sheet = Image.new("RGB", (w // 2 * len(ims), h // 2))
for i, im in enumerate(ims):
    sheet.paste(im.resize((w // 2, h // 2)), (i * w // 2, 0))
sheet.save(os.path.join(out, "sheet.jpg"), quality=88)
for f, im in zip(fs, ims):
    a = np.asarray(im.convert("L"), dtype=float)
    col = a[:, 20:80].mean(1)
    g = np.abs(np.diff(col))[h // 2:h - 40]
    print(f, "floor/wall rows", sorted(int(x) + h // 2 for x in np.argsort(g)[-2:]))
print("sheet", os.path.join(out, "sheet.jpg"))
