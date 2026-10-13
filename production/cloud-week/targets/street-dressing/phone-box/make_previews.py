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
# P1: nothing of the operator's logo, the notices or the interior may read (the review of 13 October found the logo's blue and
# red shapes still showing as blobs through a blur). So the whole upper pane inside its frame is painted flat by script (the
# median of each row, smoothed down the pane, so no shape survives), the header's lettering and handset pictogram are painted
# flat pink, and the sticker on the lower pane is painted flat.
import numpy as np
from PIL import ImageFilter


def flat_rows(img, box, sigma=10.0):
    a = np.asarray(img.convert("RGB"), float)
    x0, y0, x1, y1 = box
    reg = a[y0:y1 + 1, x0:x1 + 1, :]
    rowmed = np.median(reg, axis=1)                      # one colour per row: no shape can survive
    k = int(sigma * 3)
    pad = np.pad(rowmed, ((k, k), (0, 0)), mode="edge")
    ker = np.exp(-0.5 * (np.arange(-k, k + 1) / sigma) ** 2)
    ker /= ker.sum()
    sm = np.stack([np.convolve(pad[:, c], ker, mode="valid") for c in range(3)], axis=1)
    out = a.copy()
    out[y0:y1 + 1, x0:x1 + 1, :] = sm[:, None, :]
    return Image.fromarray(np.clip(out, 0, 255).astype("uint8"))


PANE = (441, 181, 634, 399)          # the upper pane inside the black frame (glass_l 437, glass_r 638, header_bottom 176, band_top 402)
masked = flat_rows(im, PANE)
masked = P.fill_boxes(masked, [(441, 127, 636, 172)], colour=(240, 130, 174))   # header: the word and the handset pictogram
masked = P.fill_boxes(masked, [(528, 488, 572, 535)])                            # the sticker on the lower pane
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
