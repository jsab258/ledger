#!/usr/bin/env python
"""Camera height of each panorama at the ground its railing stands on, by the HORIZON method (the method of the bollards and the kerbs targets;
the function pitch_and_h is theirs, kept unchanged so that the three families calibrate alike).

In a levelled equirectangular panorama the horizon is the middle row. On a vertical brick wall the courses are evenly spaced in tan(angle below the
horizon); camera height above the wall's foot = gauge * tan(angle of the foot) / (course pitch in tan units). The pitch is found by folding the
column-band profile resampled to uniform tan; the foot row is read by eye on a gridded crop.

Usage: calibrate.py PANO_DIR   (PANO_DIR holds <pano>.jpg, the 8192 x 4096 tone-mapped JPGs of Poly Haven)  -> prints each anchor, writes anchors.json
"""
import sys, os, json, math
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

# pano, id, columns x0 x1, rows y0 y1 (the courses' rows), foot row, gauge mm, step (m) from that foot to the ground the railing's plinth or the post stands on,
# what, pitch by eye in px (the fold searches +-15 % round it)
ANCHORS = [
    # Bethnal Green: every object here stands on, or beside a wall that stands on, the same block paving
    ('bethnal_green_entrance', 'bge_planter_wall', 5840, 5940, 2100, 2258, 2262, 75.0, 0.0, 'planter wall on the block paving (the bollards target)', 15.3),
    ('bethnal_green_entrance', 'bge_gate_pier', 2090, 2170, 1715, 2160, 2305, 75.0, 0.0, 'brick gate pier of the park entrance, red courses above its blue-brick base, on the paving', 20.3),
    ('bethnal_green_entrance', 'bge_dwarf_wall', 7535, 7550, 2100, 2175, 2243, 75.0, 0.0, 'red courses of the dwarf wall under the area railing R3a (five courses between the two blue bullnose strings)', 14.5),
    # Limehouse: the quay edge's chain posts stand on resin-bound gravel level with the clay paviors at the foot of this wall
    ('limehouse', 'lh_building_wall_a', 6890, 6910, 2165, 2392, 2397, 75.0, 0.0, 'the dock building beside the quay walk: red and blue engineering brick courses above the paving (left band)', 25.0),
    ('limehouse', 'lh_building_wall_b', 7030, 7050, 2165, 2335, 2342, 75.0, 0.0, 'the same wall, a second column band', 24.0),
    # Urban Street 01 (Hackney-side estate street): the dwarf wall under the low railing R3d and its gate pier, on the footway
    ('urban_street_01', 'us01_garden_wall', 4250, 4275, 2170, 2280, 2287, 75.0, 0.0, 'dark brick garden wall on the footway, under the low railing R3d (the bollards target measured it with a 0.07 step to its bollard bed; here the railing stands on the footway itself)', 15.3),
    ('urban_street_01', 'us01_gate_pier', 3800, 3820, 2045, 2175, 2225, 75.0, 0.0, 'brick gate pier on the same footway (joints at rows 2049, 2061 ... 2170, a steady 12.1 px)', 12.1),
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
    k = int(np.argmax(cs))
    p = float(ps[k])
    edge = k <= 2 or k >= len(ps) - 3
    tf = math.tan((foot - H / 2) * math.pi / H)
    return p, tf, gauge * tf / p, H, edge, (float(ps[0]), float(ps[-1]))


def run(pano_dir, anchors=ANCHORS, out=None):
    res = []
    for pano, name, x0, x1, y0, y1, foot, gauge, step, what, pxp in anchors:
        p, tf, h, H, edge, rng = pitch_and_h(os.path.join(pano_dir, f'{pano}.jpg'), x0, x1, y0, y1, foot, gauge, pxp)
        print(('FAILED (fit on the edge of its range) ' if edge else '') + f'{name}: pitch_tan {p:.5f}, tan(foot) {tf:.4f}, h above the foot {h:.0f} mm (+ {step} step -> {h / 1000 + step:.3f} m)')
        res.append(dict(pano=pano, id=name, cols=[x0, x1], rows=[y0, y1], foot_row=foot, image_rows=H, pitch_tan=round(p, 5), gauge_mm=gauge, step_m=step,
                        what=what, px_pitch_by_eye=pxp, search_range_tan=[round(rng[0], 5), round(rng[1], 5)], fit_on_edge=bool(edge)))
    if out:
        json.dump(res, open(out, 'w'), indent=1)
    return res


if __name__ == '__main__':
    d = sys.argv[1]
    run(d, out=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'anchors.json'))
