#!/usr/bin/env python
"""Camera height of each panorama, measured independently (see calibration_data.py for the two methods and the raw rows).

    /home/user/.bpyenv/bin/python calibrate.py [PANO_DIR]

Without PANO_DIR: recomputes every anchor's height from the raw numbers stored in calibration_data.py (pitch in tan units, foot row, tyre rows) and prints
each panorama's mean at its measurement ground against the stated height.
With PANO_DIR (a folder holding tm_<id>.jpg, the 8k tone-mapped copies from https://api.polyhaven.com/files/<id>): also RE-FITS each brick anchor's course pitch
from the picture (the Fourier fold of the bollards' calibrate.py: the profile of the column band is resampled to uniform tan(angle) and folded at trial pitches within
+-15 % of the by-eye guess) and prints how far the re-fit is from the stored pitch.
The height at the ground of a measurement is  h(anchor) + the step of the anchor's ground above it.  (The brick method is the bollards' writer's; credit
production/cloud-week/targets/bollards/calibrate.py.)
"""
import math, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import calibration_data as CD  # noqa: E402

H_IMAGE = 4096  # rows of the 8k tone-mapped panoramas (8192 x 4096)


def h_brick_mm(a):
    """camera height above the wall's foot (mm) from the stored pitch and foot row"""
    tf = math.tan((a['foot_row'] - H_IMAGE / 2.0) * math.pi / H_IMAGE)
    return a['gauge_mm'] * tf / a['pitch_tan']


def h_wheel_m(w):
    ab = (w['bottom_row'] - H_IMAGE / 2.0) * math.pi / H_IMAGE
    at = (w['top_row'] - H_IMAGE / 2.0) * math.pi / H_IMAGE
    tb, tt = math.tan(ab), math.tan(at)
    return w['D_m'] * tb / (tb - tt)


def anchors_for(pano):
    """list of (id, kind, height at the measurement ground in m) for one panorama"""
    out = []
    for a in CD.BRICKS:
        if a['pano'] == pano:
            out.append((a['id'], 'bricks', h_brick_mm(a) / 1000.0 + a['ground_step_m']))
    for w in CD.WHEELS:
        if w['pano'] == pano:
            out.append((w['id'], 'wheel', h_wheel_m(w)))
    return out


def refit_pitch(path, a):
    """re-fit the course pitch of one brick anchor from the panorama file (needs numpy and PIL)"""
    import numpy as np
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    im = Image.open(path).convert('L')
    H = im.size[1]
    x0, x1 = a['cols']
    y0, y1 = a['rows']
    arr = np.asarray(im.crop((x0, y0, x1, y1)), float)
    prof = arr.mean(1)
    rows = np.arange(y0, y1) + 0.5
    t = np.tan((rows - H / 2) * math.pi / H)
    tu = np.linspace(t[0], t[-1], 4 * len(t))
    pu = np.interp(tu, t, prof)
    pu = pu - np.convolve(pu, np.ones(61) / 61, mode='same')
    pu = pu[40:-40]
    tu = tu[40:-40]
    guess = a['px_pitch_by_eye'] * math.pi / H
    ps = np.linspace(0.85 * guess, 1.15 * guess, 1200)
    nb = 24

    def folded(q):
        ph = ((tu - tu[0]) / q) % 1.0
        idx = np.minimum((ph * nb).astype(int), nb - 1)
        m = np.array([pu[idx == k].mean() if (idx == k).any() else 0.0 for k in range(nb)])
        return m.var()
    cs = np.array([folded(q) for q in ps])
    return float(ps[int(np.argmax(cs))])


def summary():
    rows = []
    for pano, hd in CD.HEIGHTS.items():
        an = anchors_for(pano)
        vals = [v for _, _, v in an]
        mean = sum(vals) / len(vals)
        rows.append((pano, hd['h_m'], hd['err_m'], mean, an))
    return rows


if __name__ == '__main__':
    pano_dir = sys.argv[1] if len(sys.argv) > 1 else None
    for pano, hs, err, mean, an in summary():
        print(f'{pano}: stated {hs:.3f} +-{err:.3f} m; mean of its anchors {mean:.3f} m ({len(an)} anchors; first draft assumed {CD.ASSUMED_FIRST_DRAFT_M})')
        for id_, kind, v in an:
            print(f'    {id_:26s} {kind:6s} {v:.3f} m at the measurement ground')
    if pano_dir:
        print('re-fit of the brick pitches from', pano_dir)
        for a in CD.BRICKS:
            p = os.path.join(pano_dir, f"tm_{a['pano']}.jpg")
            if not os.path.exists(p):
                print('   missing', p)
                continue
            q = refit_pitch(p, a)
            print(f"    {a['id']:22s} stored {a['pitch_tan']:.5f} re-fit {q:.5f} ({100 * (q / a['pitch_tan'] - 1):+.1f} %)")
