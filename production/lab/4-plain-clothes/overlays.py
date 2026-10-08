"""The check's outline overlays for one version side by side (green both, red model only, blue target only)."""
import sys
from PIL import Image
ver, out = sys.argv[1], sys.argv[2]
d = "F:/LedgerTools/lab/clothes/checks"
ims = [Image.open("%s/overlay_%s_%s_%s.png" % (d, ver, g, v)).convert("RGB") for g in ("jumper", "trousers") for v in ("front", "side")]
crop = [im.crop((0, 0, im.width, int(im.height * 0.55))) if i < 2 else im.crop((0, int(im.height * 0.35), im.width, im.height)) for i, im in enumerate(ims)]
W = sum(c.width for c in crop) + 30
H = max(c.height for c in crop)
s = Image.new("RGB", (W, H), (200, 200, 200))
x = 0
for c in crop:
    s.paste(c, (x, 0)); x += c.width + 10
s.save(out)
