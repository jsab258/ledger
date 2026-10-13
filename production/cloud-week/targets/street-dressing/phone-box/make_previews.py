"""phone-box: the preview crops (masked) and the target-on-photo overlay. Needs the photographs in the scratch folder
(measure.py downloads P1; this script downloads S2)."""
import json
import os
import sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import sd_lib as L
import sd_photo as P
from PIL import Image

SCRATCH = os.environ.get("SD_SCRATCH", "/home/user/ledger-scratch/street-dressing/phone-box")
OUT = os.path.join(L.PREVIEWS, "phone-box")
T = json.load(open(os.path.join(HERE, "target.json")))

pg1, p1 = L.sampled_photo("5269043", "P1", SCRATCH)
im = Image.open(p1).convert("RGB")
CROP = (380, 40, 700, 735)
# P1: the printed logo and notices behind the glass are blurred, the header's lettering painted out (its pink panel is flat)
masked = P.blur_boxes(im, [(440, 195, 645, 495)], radius=7)
masked = P.fill_boxes(masked, [(488, 126, 602, 172)])   # the word 'Coins' on the header panel
c1 = masked.crop(CROP)
sz1 = P.save_limited(c1, os.path.join(OUT, "p1-verge-kx100-front.jpg"))
# overlay on the same crop
ph = T["photos"][0]
ov = P.overlay(masked.copy(), T, ph).crop(CROP)
sz2 = P.save_limited(ov.resize((ov.width * 2, ov.height * 2), Image.LANCZOS) if False else ov, os.path.join(OUT, "p1-verge-kx100-target-on-photo.jpg"))
print("p1", sz1, "overlay", sz2)

pg2, p2 = L.sampled_photo("5558709", "P2", SCRATCH)
im2 = Image.open(p2).convert("RGB")
c2 = im2.crop((150, 520, 545, 870))
print("p2", P.save_limited(c2, os.path.join(OUT, "p2-handle-kx100-detail.jpg")))
