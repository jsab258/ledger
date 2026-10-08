"""Where a version's outline is more than the tolerance off the target's: heights and sides, in metres."""
import json
import sys

import numpy as np
from PIL import Image, ImageDraw
from scipy import ndimage

sys.path.insert(0, "../tools")
from outline import Frame, boundary, silhouette  # noqa: E402

ver = sys.argv[1]
T = json.load(open("target/target.json"))
d = np.load("F:/LedgerTools/lab/clothes/clothes_%s.npz" % ver)
for g in ("jumper", "trousers"):
    for view in ("front", "side"):
        fr = Frame(**T["masks"]["side_frame" if view == "side" else "front_frame"])
        img = Image.new("1", (fr.shape[1], fr.shape[0]), 0)
        dr = ImageDraw.Draw(img)
        for poly in T["views"][g][view]:
            P2 = np.asarray(poly, float)
            Q = np.stack(fr.to_px(P2[:, 0], P2[:, 1]), 1)
            dr.polygon([tuple(q) for q in Q], fill=1, outline=1)
        tgt = np.array(img, bool)
        M = silhouette({g: (d[g + "_V"], d[g + "_F"])}, (1, 2) if view == "side" else (0, 2), fr)
        bm, bt = boundary(M), boundary(tgt)
        dm = ndimage.distance_transform_edt(~bt) * fr.mm_per_px
        dt = ndimage.distance_transform_edt(~bm) * fr.mm_per_px
        s = fr.mm_per_px / 1000
        for name, B, D in (("model edge far from target", bm, dm), ("target edge far from model", bt, dt)):
            r, c = np.nonzero(B & (D > 10))
            if len(r) == 0:
                continue
            u = fr.u0 + c * s
            v = fr.v0 + fr.height - r * s
            lab, n = ndimage.label(B & (D > 10), structure=np.ones((3, 3)))
            print("%s %s: %s, %d px" % (g, view, name, len(r)))
            for i in sorted(range(1, n + 1), key=lambda i: -D[lab == i].max())[:4]:
                rr, cc = np.nonzero(lab == i)
                print("   u %.3f..%.3f  z %.3f..%.3f  up to %.1f mm" % (fr.u0 + cc.min() * s, fr.u0 + cc.max() * s,
                      fr.v0 + fr.height - rr.max() * s, fr.v0 + fr.height - rr.min() * s, D[rr, cc].max()))
