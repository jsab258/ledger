"""The pane-to-frame measurements on the photographs (Photo kind). Each window: an outline box (jamb to jamb, head to sill top), the pane boxes (the glass or net
inside the sash), its state, and the proportion w/h its true window would have (0.50 for the period sash; 0.33 for P9's tall arched ones). Luma is sRGB-coded
0.2126 R + 0.7152 G + 0.0722 B (1a's measure). L = the outline's 90th percentile, P = the pane median, D = the outline's 5th percentile.
The angle from the wall is estimated from the window's apparent proportion: sin(angle) = (w_app / h_app) / a_true; its error is +-5 degrees (the true proportion varies
0.40 to 0.62 between windows). The outline boxes are by eye on the photographs' own pixels (hw_photos.PHOTOS ids); a few include the dark reveal at their edge, so
D is a floor: the tight outlines (P1) are the ones to compare with a render's D/L."""
import math
import os
import sys

import numpy as np
from PIL import Image

sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import hw_photos as P

# id: (photo, state, outline (x0, y0, x1, y1), [pane boxes], a_true, note)
WINDOWS = {
    "P1_a": ("P1", "net_full", (433, 392, 451, 455), [(438, 398, 449, 446)], 0.50, "upstairs, white frame, white voile both sashes"),
    "P1_b": ("P1", "net_full", (403, 396, 419, 458), [(407, 402, 416, 448)], 0.50, "upstairs, white frame, white voile"),
    "P1_c": ("P1", "bare_dark", (391, 400, 401, 453), [(394, 406, 398, 446)], 0.50, "upstairs, dark-brown frame, bare glass, dark room"),
    "P1_e": ("P1", "net_full", (433, 485, 451, 545), [(438, 492, 449, 538)], 0.50, "ground, white frame, white voile"),
    "P4_C": ("P4", "net_full", (513, 130, 560, 231), [(523, 182, 557, 226)], 0.50, "upstairs, full white net (black and white print)"),
    "P4_G": ("P4", "bare_dark", (517, 289, 563, 417), [(529, 354, 560, 406)], 0.50, "ground, bare, the room black, a pot plant"),
    "P4_E": ("P4", "net_half", (393, 319, 420, 413), [(400, 363, 417, 401)], 0.50, "ground, a net over the lower half"),
    "P3_a": ("P3", "net_full", (855, 281, 907, 377), [(862, 333, 902, 370)], 0.50, "upstairs, cream frame, lower sash voile, near square"),
    "P3_b": ("P3", "net_full", (630, 292, 670, 383), [(636, 322, 666, 372)], 0.50, "upstairs, red-brown frame, voile"),
    "P3_c": ("P3", "net_full", (631, 450, 670, 550), [(637, 480, 667, 543)], 0.50, "ground, red-brown frame, voile"),
    "P3_d": ("P3", "bare_dark", (852, 463, 907, 570), [(862, 525, 902, 555)], 0.50, "ground, cream frame, bare lower sash, dark room, near square"),
    "P3_e": ("P3", "net_full", (460, 453, 498, 537), [(470, 470, 495, 530)], 0.50, "ground, white frame, voile"),
    "P3_f": ("P3", "net_full", (463, 303, 500, 387), [(470, 325, 497, 375)], 0.50, "upstairs, white frame, voile"),
    "P9_a": ("P9", "glass_bright", (376, 276, 398, 410), [(381, 285, 394, 402)], 0.33, "tall sash in shade, panes pale (sky), bars as dark lines"),
    "P9_b": ("P9", "glass_bright", (433, 250, 456, 395), [(438, 258, 452, 388)], 0.33, "tall sash in shade"),
    "P9_c": ("P9", "glass_bright", (322, 125, 345, 252), [(327, 135, 340, 245)], 0.33, "tall sash in sun, panes bright"),
    "P6_up": ("P6", "glass_sky_room", (284, 103, 388, 264), [(292, 112, 381, 152), (295, 165, 328, 250), (343, 165, 380, 250)], 0.50, "replacement window: sky in the top light, dark room and a net edge below"),
    "P8_L": ("P8", "glass_dark_room", (306, 295, 377, 429), [(309, 298, 340, 358), (309, 368, 340, 424)], 0.50, "original 2/2, near square from below, panes blue-grey over a dark room"),
    "P8_R": ("P8", "glass_dark_room", (569, 317, 639, 431), [(573, 321, 602, 382), (573, 388, 602, 425)], 0.50, "original 2/2, near square from below"),
}
BRICK = {"P1": (480, 395, 560, 470), "P8": (390, 330, 440, 420)}   # brick beside the windows, for the frame-to-wall ratio


def luma(a):
    a = a.astype(float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def to_lin(v):
    return (v / 255.0) ** 2.2


def measure_all(photo_dir):
    imgs = {}
    out = {}
    for k, (pid, state, ol, panes, at, note) in WINDOWS.items():
        if pid not in imgs:
            imgs[pid] = luma(np.asarray(Image.open(P.fetch(photo_dir, pid)).convert("RGB")))
        Y = imgs[pid]
        x0, y0, x1, y1 = ol
        sash = Y[y0:y1, x0:x1]
        pv = np.concatenate([Y[b[1]:b[3], b[0]:b[2]].ravel() for b in panes])
        L = float(np.percentile(sash, 90)); D = float(np.percentile(sash, 5)); Pm = float(np.median(pv))
        asp = (x1 - x0) / float(y1 - y0)
        ang = math.degrees(math.asin(min(1.0, asp / at)))
        out[k] = {"photo": pid, "state": state, "aspect": round(asp, 3), "angle_deg": round(ang, 1), "L90": round(L, 1), "P50": round(Pm, 1), "D5": round(D, 1),
                  "P_over_L": round(Pm / L, 3), "D_over_L": round(D / L, 3), "pane_spread_5_95": round(float(np.percentile(pv, 95) - np.percentile(pv, 5)), 1),
                  "pane_px": int(pv.size), "note": note}
    br = {}
    for pid, b in BRICK.items():
        if pid not in imgs:
            imgs[pid] = luma(np.asarray(Image.open(P.fetch(photo_dir, pid)).convert("RGB")))
        br[pid] = round(float(np.median(imgs[pid][b[1]:b[3], b[0]:b[2]])), 1)
    return out, br


def summarise(rows):
    """Bands by state, over the rows given (a dict of measure_all's rows)."""
    bands = {}
    for st in sorted({r["state"] for r in rows.values()}):
        v = [r for r in rows.values() if r["state"] == st]
        pl = [r["P_over_L"] for r in v]
        bands[st] = {"n": len(v), "P_over_L_min": min(pl), "P_over_L_max": max(pl), "P_over_L_median": float(np.median(pl)),
                     "D_over_L_median": float(np.median([r["D_over_L"] for r in v])), "angles_deg": sorted(r["angle_deg"] for r in v)}
    return bands


if __name__ == "__main__":
    d = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.environ.get("TMPDIR", "/tmp"), "hw_photos")
    rows, br = measure_all(d)
    for k, v in rows.items():
        print(k, v)
    print(br)
    for k, v in summarise(rows).items():
        print(k, v)
