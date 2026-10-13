"""The pane-to-frame measurements on the photographs (Photo kind). Each window: an outline box (jamb to jamb, head to sill top), the pane boxes (the glass or net
inside the sash), its state, and the proportion w/h its true window would have (0.50 for the period sash; 0.33 for P9's tall arched ones). Luma is sRGB-coded
0.2126 R + 0.7152 G + 0.0722 B (1a's measure).

MEASURED THE WAY THE GATE MEASURES (TARGET-REVIEW of 13 October, fault 2; TARGET.md section 9): P = the pane boxes' median; L = the 90th percentile of the OUTLINE
MINUS THE PANE BOXES (the joinery: the stile, rail and lining pixels, no brick, no stone); D = the outline's 5th percentile (joinery and pane together, no brick);
spread = the pane's 95th minus 5th percentile. The first version of this file took L over the whole outline and drew P1's outlines to include the white-painted stone head and
sill and a column of brick at the jamb: that made L 233 to 245 (the stone's paint, 248 to 254) and D/L 0.47 to 0.50 (the brick's own 119 over the stone), neither of which
the gate can read off a render. P1_a, P1_b and P1_e are now boxed without the stone and the brick; the other outlines are as they were and a few still include the dark reveal
or a little stone at their edge, so for them D is a floor (and L, now taken from the joinery alone, is a little nearer the frame's own luma).
The angle from the wall is estimated from the window's apparent proportion: sin(angle) = (w_app / h_app) / a_true; its error is +-5 degrees (the true proportion varies
0.40 to 0.62 between windows). The outline boxes are by eye on the photographs' own pixels (hw_photos.PHOTOS ids).
P1_c's frame is dark brown and its outline still includes the white stone head and sill: its L is the stone's paint, so its row reads a bare dark room against white, as the
bare band wants (fault 1's amendment makes every street frame white or cream: the bands apply to white and cream frames only)."""
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
    "P1_a": ("P1", "net_full", (435, 396, 451, 447), [(437, 399, 449, 444)], 0.50, "upstairs, white frame, white voile both sashes; boxed without the stone head and sill and without the brick column (the review's box)"),
    "P1_b": ("P1", "net_full", (405, 402, 418, 452), [(406, 405, 417, 449)], 0.50, "upstairs, white frame, white voile; boxed without the stone and the brick (the review's box)"),
    "P1_c": ("P1", "bare_dark", (391, 400, 401, 453), [(394, 406, 398, 446)], 0.50, "upstairs, dark-brown frame, bare glass, dark room (the outline still includes the white stone: see the note at the top)"),
    "P1_e": ("P1", "net_full", (435, 489, 451, 540), [(437, 492, 449, 537)], 0.50, "ground, white frame, voile on the lower sash and the upper sash clear and dark; boxed the same way as P1_a: from 5 rows under the stone head's end (y 484) to the stone sill's start (y 540), jamb to jamb (x 435 to 450)"),
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
# the review's second box for P1_a: the top three rows (the head's shadow, y 396 to 398) taken out as well: outline, pane
ALT_BOXES = {"P1_a": ("top_rows_out", (435, 399, 451, 447), [(437, 402, 449, 444)])}
# P8 measured the gate's way: all four panes of the two windows together (the review's reproduction: P/L 0.57, blue over red 46)
P8_PANES = [(309, 298, 340, 358), (309, 368, 340, 424), (573, 321, 602, 382), (573, 388, 602, 425)]


def luma(a):
    a = a.astype(float)
    return 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]


def to_lin(v):
    return (v / 255.0) ** 2.2


def _one(Y, ol, panes, rgb=None):
    """P (pane median), L (joinery p90: the outline minus the pane boxes), D (outline p5), spread, over one window."""
    x0, y0, x1, y1 = ol
    sash = Y[y0:y1, x0:x1]
    join = np.ones(sash.shape, bool)
    for b in panes:
        join[b[1] - y0:b[3] - y0, b[0] - x0:b[2] - x0] = False
    pv = np.concatenate([Y[b[1]:b[3], b[0]:b[2]].ravel() for b in panes])
    L = float(np.percentile(sash[join], 90))
    D = float(np.percentile(sash, 5))
    Pm = float(np.median(pv))
    sp = float(np.percentile(pv, 95) - np.percentile(pv, 5))
    out = {"L": L, "D": D, "P": Pm, "spread": sp, "pane_px": int(pv.size), "joinery_px": int(join.sum())}
    if rgb is not None:
        pr = np.concatenate([rgb[b[1]:b[3], b[0]:b[2]].reshape(-1, 3) for b in panes])
        med = np.median(pr, axis=0)
        out["rgb"] = [round(float(v), 1) for v in med]
        out["blue_minus_red"] = round(float(med[2] - med[0]), 1)
    return out


def measure_all(photo_dir):
    imgs = {}
    rgbs = {}
    out = {}
    for k, (pid, state, ol, panes, at, note) in WINDOWS.items():
        if pid not in imgs:
            rgbs[pid] = np.asarray(Image.open(P.fetch(photo_dir, pid)).convert("RGB"))
            imgs[pid] = luma(rgbs[pid])
        Y = imgs[pid]
        x0, y0, x1, y1 = ol
        m = _one(Y, ol, panes, rgbs[pid] if state == "glass_dark_room" else None)
        L, D, Pm = m["L"], m["D"], m["P"]
        asp = (x1 - x0) / float(y1 - y0)
        ang = math.degrees(math.asin(min(1.0, asp / at)))
        out[k] = {"photo": pid, "state": state, "aspect": round(asp, 3), "angle_deg": round(ang, 1), "L90": round(L, 1), "P50": round(Pm, 1), "D5": round(D, 1),
                  "P_over_L": round(Pm / L, 3), "D_over_L": round(D / L, 3), "pane_spread_5_95": round(m["spread"], 1),
                  "pane_px": m["pane_px"], "joinery_px": m["joinery_px"], "L_is": "p90 of the outline minus the pane boxes (the gate's joinery)", "note": note}
        if "rgb" in m:
            out[k]["pane_rgb_median"] = m["rgb"]
            out[k]["blue_minus_red"] = m["blue_minus_red"]
        if k in ALT_BOXES:
            nm, ol2, pn2 = ALT_BOXES[k]
            m2 = _one(Y, ol2, pn2)
            out[k]["alt_" + nm] = {"outline": list(ol2), "panes": [list(b) for b in pn2], "L90": round(m2["L"], 1), "P50": round(m2["P"], 1), "D5": round(m2["D"], 1),
                                   "P_over_L": round(m2["P"] / m2["L"], 3), "D_over_L": round(m2["D"] / m2["L"], 3), "pane_spread_5_95": round(m2["spread"], 1)}
    br = {}
    for pid, b in BRICK.items():
        if pid not in imgs:
            rgbs[pid] = np.asarray(Image.open(P.fetch(photo_dir, pid)).convert("RGB"))
            imgs[pid] = luma(rgbs[pid])
        br[pid] = round(float(np.median(imgs[pid][b[1]:b[3], b[0]:b[2]])), 1)
    return out, br


def measure_extra(photo_dir):
    """P8 as the gate sees it for WB-03: both windows' four panes together over the joinery of both outlines (the review's reproduction: P/L 0.57, blue over red 46)."""
    R8 = np.asarray(Image.open(P.fetch(photo_dir, "P8")).convert("RGB"))
    Y8 = luma(R8)
    pv = np.concatenate([Y8[b[1]:b[3], b[0]:b[2]].ravel() for b in P8_PANES])
    joins = []
    for k in ("P8_L", "P8_R"):
        ol, panes = WINDOWS[k][2], WINDOWS[k][3]
        x0, y0, x1, y1 = ol
        sash = Y8[y0:y1, x0:x1]
        jm = np.ones(sash.shape, bool)
        for b in panes:
            jm[b[1] - y0:b[3] - y0, b[0] - x0:b[2] - x0] = False
        joins.append(sash[jm])
    L8 = float(np.percentile(np.concatenate(joins), 90))
    pr = np.concatenate([R8[b[1]:b[3], b[0]:b[2]].reshape(-1, 3) for b in P8_PANES])
    med = np.median(pr, axis=0)
    return {"P8_four_panes": {"P50": round(float(np.median(pv)), 1), "L90": round(L8, 1), "P_over_L": round(float(np.median(pv)) / L8, 3), "pane_rgb_median": [round(float(v), 1) for v in med],
                              "blue_minus_red": round(float(med[2] - med[0]), 1), "note": "both windows' four panes together over the joinery of both outlines: the gate's own way for WB-03"}}


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
    print(measure_extra(d))
    print(br)
    for k, v in summarise(rows).items():
        print(k, v)
