#!/usr/bin/env python
"""Camera height of each panorama from brick courses, by the HORIZON method (independent of any re-projection and of any assumed height).

In a levelled equirectangular panorama the horizon is the middle row (H/2). On a vertical wall at distance d a height z above the camera's own level
is z = -d tan(theta) (theta below the horizon positive), so the courses are evenly spaced in tan(theta). Then
    camera height above the wall's foot = gauge * tan(theta_foot) / pitch_tan.
The courses' pitch is found by a Fourier fit of the column-band profile resampled to uniform tan(theta); the foot row is read by eye.
Usage: calibrate.py PANO_DIR  -> prints each anchor and writes anchors.json (raw numbers: band, rows, pitch_tan, foot row)."""
import sys, os, json, math
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

# pano, name, columns x0 x1, rows y0 y1 (the courses' rows), foot row, gauge mm, level step (m) to add to reach the bollard's own ground, what, joint pitch by eye in px near the horizon
# (the joints counted on a 4x crop; the Fourier fit then refines it inside +-15 %: it can otherwise lock on a harmonic)
ANCHORS = [
    ('urban_street_01', 'us01_garden_wall', 4250, 4275, 2170, 2280, 2287, 75.0, 0.07, 'garden wall on the footway behind US01_b; the bollard stands in a bed 0.07 m below that footway', 15.3),
    ('urban_street_01', 'us01_gate_pier', 3760, 3830, 2170, 2222, 2225, 75.0, 0.07, 'brick gate pier on the same footway', 11.9),
    ('bethnal_green_entrance', 'bge_planter_wall', 5840, 5940, 2100, 2258, 2262, 75.0, 0.0, 'planter wall on the same block paving as BGE_a', 15.3),
    ('birbeck_street_underpass', 'bb_viaduct_wall', 3700, 3760, 1845, 2015, 2318, 75.0, 0.0, 'yellow-stock wall above the paint, on BB_b\'s own footway (to 79 mm if Victorian courses)', 19.7),
    ('urban_street_02', 'us02_building_wall', 740, 840, 2045, 2192, 2194, 75.0, 0.0, 'the building wall behind US02_a, on its footway', 11.75),
    ('urban_street_02', 'us02_gate_pier', 7970, 8000, 2028, 2215, 2226, 75.0, 0.0, 'gate pier at the panorama seam, on the same footway', 14.77),
]


def pitch_and_h(path, x0, x1, y0, y1, foot, gauge, px_pitch):
    im = Image.open(path).convert('L')
    H = im.size[1]
    a = np.asarray(im.crop((x0, y0, x1, y1)), float)
    prof = a.mean(1)
    rows = np.arange(y0, y1) + 0.5
    t = np.tan((rows - H / 2) * math.pi / H)
    tu = np.linspace(t[0], t[-1], 4 * len(t))
    pu = np.interp(tu, t, prof)
    pu = pu - np.convolve(pu, np.ones(61) / 61, mode='same')
    pu = pu[40:-40]; tu = tu[40:-40]
    guess = px_pitch * math.pi / H
    ps = np.linspace(0.85 * guess, 1.15 * guess, 1200)
    nb = 24

    def folded(q):
        ph = ((tu - tu[0]) / q) % 1.0
        idx = np.minimum((ph * nb).astype(int), nb - 1)
        m = np.array([pu[idx == k].mean() if (idx == k).any() else 0.0 for k in range(nb)])
        return m.var()
    cs = np.array([folded(q) for q in ps])
    p = float(ps[int(np.argmax(cs))])
    tf = math.tan((foot - H / 2) * math.pi / H)
    return p, tf, gauge * tf / p, H


if __name__ == '__main__':
    d = sys.argv[1]
    out = []
    for pano, name, x0, x1, y0, y1, foot, gauge, step, what, pxp in ANCHORS:
        p, tf, h, H = pitch_and_h(os.path.join(d, f'tm_{pano}.jpg'), x0, x1, y0, y1, foot, gauge, pxp)
        print(f'{name}: pitch_tan {p:.5f}, tan(foot) {tf:.4f}, {tf / p:.2f} courses to the horizon, h above the wall foot {h:.0f} mm (+ {step} step -> {h / 1000 + step:.3f} at the bollard\'s ground)')
        out.append(dict(pano=pano, id=name, cols=[x0, x1], rows=[y0, y1], foot_row=foot, image_rows=H, pitch_tan=round(p, 5), gauge_mm=gauge, step_m=step, what=what, px_pitch_by_eye=pxp))
    json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchors.json'), 'w'), indent=1)
