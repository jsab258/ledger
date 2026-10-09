#!/usr/bin/env python
"""Photograph measurements of the railings family.  Needs the panoramas:  measure.py PANO_DIR  ->  photo_measurements.json
Automated: the park railing R3B (bar centres, pitch, bar width, rail rows, coping top, post width) on a 1 mm a pixel elevation.
Read by eye on gridded 1 mm and 2 mm a pixel elevations (the numbers below, each with its error): R3A, R3D, the Limehouse bay LHB, and the heads of R3B.
Every length is at the camera height of frames.CAMERAS (each at its own ground), so +-6 % in absolute size; ratios and counts are exact to the pixel."""
import sys, os, json, math
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.signal import find_peaks
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rail_lib as L
from frames import FRAMES, OBJECTS, SCALE, FIRST_H, H_CAM


def plane_of(F, W=8192, H=4096):
    h = F['h_cam']
    pts = []
    for col, row in F['feet_px']:
        g = L.ground_point(col, row, W, H, h)
        if F.get('flange_r_mm'):
            g = g + g / np.hypot(*g) * F['flange_r_mm'] / 1000.0
        pts.append(g)
    return L.Plane(pts[0], pts[1], h, off_mm=F['off_mm'])


def r3b(pano_dir):
    F = FRAMES['R3B']
    pl = plane_of(F)
    win = F['window']
    f = SCALE['R3B']
    e = L.elevation(os.path.join(pano_dir, F['pano'] + '.jpg'), pl, 0, win['s1'], win['z0'], 2400 * f, 1)
    z1 = 2400.0 * f
    z1 = float(round(z1))

    def zrow(z): return int(round(z1 - z))
    prof = e[zrow(900):zrow(700)].mean(0)
    d = gaussian_filter1d(gaussian_filter1d(prof, 25) - prof, 1.0)
    pk, _ = find_peaks(gaussian_filter1d(d, 1), height=15, distance=40)
    pk = pk[(pk > 600 * f) & (pk < 2600 * f)]
    fit = np.polyfit(np.arange(len(pk)), pk, 1)
    res = pk - np.polyval(fit, np.arange(len(pk)))
    ws = []
    for p in pk:
        seg = d[p - 30:p + 31]
        m = seg.max()
        if m < 20: continue
        idx = np.where(seg > m / 2)[0]
        ws.append(int(idx.max() - idx.min() + 1))
    # the bars of the gate leaf to the right of the hinge post (s 2700 to 3800): their own phase
    pk_all, _ = find_peaks(gaussian_filter1d(d, 1), height=15, distance=40)
    pk2 = pk_all[(pk_all > 2700 * f) & (pk_all < 3820 * f)]
    fit2 = np.polyfit(np.arange(len(pk2)), pk2, 1)
    mids = (pk[:-1] + pk[1:]) // 2
    cols = np.concatenate([np.arange(m - 6, m + 7) for m in mids])
    rp = e[:, cols].mean(1)
    rd = gaussian_filter1d(gaussian_filter1d(rp, 30) - rp, 1)
    rr, _ = find_peaks(gaussian_filter1d(rd, 1), height=14, distance=20)
    rails = [dict(z=float(z1 - r), depth=round(float(rd[r]), 1)) for r in rr]
    # the coping's top surface: the strongest brightness change in the band z 330..450 averaged over s 700..2400 (the stone is lighter than the shadow under the rail)
    sub = gaussian_filter1d(e[:, int(700 * f):int(2400 * f)].mean(1), 2)
    rows = range(zrow(450), zrow(290))
    gr = [(float(sub[r + 2] - sub[r - 2]), float(z1 - r)) for r in rows]
    top = max(gr)[1]
    # the hinge post: the widest dark run around s = 2590 at z 1700..1910
    pw = []
    for z in range(1700, 1920, 30):
        cx = int(round(2590 * f))
        row = e[zrow(z) - 2:zrow(z) + 3].mean(0)[cx - 140:cx + 160]
        thr = (np.percentile(row, 90) + row.min()) / 2
        dark = row < thr
        idx = np.where(dark)[0]
        k = idx[np.argmin(abs(idx - 140))]
        a = b = k
        while a > 0 and dark[a - 1]: a -= 1
        while b < len(dark) - 1 and dark[b + 1]: b += 1
        pw.append(int(b - a + 1))
    return dict(frame='R3B', bar_centres_s_mm=[int(x) for x in pk], bar_pitch_mm=round(float(fit[0]), 2), bar_fit_first_s_mm=round(float(fit[1]) + 0.5, 2), bar_pitch_resid_rms_mm=round(float(np.sqrt((res ** 2).mean())), 2),
                leaf_bar_centres_s_mm=[int(x) for x in pk2], leaf_bar_pitch_mm=round(float(fit2[0]), 2), bar_fwhm_mm_median=float(np.median(ws)), bar_fwhm_mm_all=ws, rails=rails, coping_top_z_mm=top, post_width_mm=pw,
                method='1 mm a pixel elevation (rail_lib.elevation) at the stated camera height; bars = dark minima of the column profile at z 700..900; rails = dark rows between bars; FWHM includes the blur of a 3 to 4 mm native pixel')


# read by eye on the gridded elevations (1 mm and 2 mm a pixel), each with its error; the method is in the text of TARGET.md section 4
HAND_READS = {
    'R3B': dict(
        bottom_rail_axis_z=dict(v=445, err=15, how='dark row between the bars at z 440 (rows 2000+: also detected by the column-between-bars profile, depth 19); a flat bar about 18 high'),
        mid_rail_axis_z=dict(v=1045, err=15, how='row profile peak 1036, picture read 1056'),
        top_rail_axis_z=dict(v=2000, err=10, how='row profile peak, depth 43, FWHM 26 (blur included): a flat bar about 20 high'),
        coping_top_z=dict(v=345, err=20, how='the stone slab\'s top at its front lip: the gradient search gives 331 on the plane 110 behind the face; the lip is nearer the camera, so its true height is about 13 higher (the ray falls 110 x (0.97 - 0.35) / 5.2 over that distance)'),
        short_bar_tip_z=dict(v=1225, err=20, how='spear tips of the short bars, which stop just above the middle rail'),
        tall_bar_tip_z=dict(v=2270, err=15, how='spear tips of the tall bars (every second bar), 255 to 285 over the 16k re-measurement of the fresh review, median 2270 (the first version read 2300); 270 above the top rail'),
        post_top_z=dict(v=2375, err=15, how='the finial of the hinge post'),
        post_shaft_width=dict(v=100, err=10, how='mean of eight rows z 1700 to 1910 (93 to 110), blur included'),
        post_collar_width=dict(v=155, err=15, how='the collar at z 1995 to 2035'),
        urn_width=dict(v=135, err=15, how='the vase under the hinge post\'s finial, z 2150 to 2210'),
        post_axis_s=dict(v=2590, err=15, how='the hinge post\'s axis along the plane'),
        pier_width=dict(v=550, err=40, how='the brick pier under the hinge post, s 2530 to 3080'),
        bar_foot=dict(v='each bar ends in a small ball (about 20 across) just under the bottom rail, 12 below its axis', err=None, how='1 mm elevation of the foot'),
        bar_head=dict(v=[[9, 1990], [9, 2025], [16, 2030], [20, 2040], [15, 2050], [15, 2068], [28, 2080], [46, 2098], [42, 2110], [30, 2125], [20, 2135], [22, 2145], [22, 2155], [18, 2165], [12, 2200], [6, 2240], [0, 2275]],
                      err=8, how='(r, z) of a tall bar\'s head, the fresh review\'s 16k profile (the first version\'s 60 across at 2128 was wrong): a ring 40 across at 2030, a turned knop about 92 across at 2098 to 2110, a ring about 44 across at 2145 to 2155, a spire to the tip at 2275; at the first version\'s height 0.97, +-8'),
    ),
    'R3A': dict(
        wall_top_z=dict(v=780, err=20, how='top of the blue bullnose coping, 1 mm and 3 mm elevations'),
        wall_string_z=dict(v=300, err=20, how='top of the lower blue bullnose string'),
        red_courses_between=dict(v=5, err=0, how='five red stretcher courses between z 330 and 705 at 75 mm: the scale check on the elevation'),
        bottom_rail_axis_z=dict(v=840, err=20, how='dark row; the picture read 825'),
        mid_rail_axis_z=dict(v=1435, err=15, how='dark row, profile 1435'),
        top_rail_axis_z=dict(v=1645, err=15, how='dark row, profile 1649'),
        bar_pitch_all=dict(v=114, err=5, how='the thick (tall) bars at s 204, 435, 660, 891, 1110 on the 3 mm preview: 226.5 apart; the thin ones the same, half a pitch between: all bars 113.3 (the first reading, from the far side of the post, gave 116)'),
        tall_first_s=dict(v=204, err=15, how='the first thick bar with a fleur-de-lis head in the preview window'),
        left_run_max_s=dict(v=1500, err=20, how='the numbers of R3A are the LEFT run\'s (preview s < 1500 at the first version\'s height, the spear heads and lily plaques); right of the cast post the photograph shows a second pattern (fleur-de-lis heads about half a pitch out of step) that is not measured'),
        tall_tip_z=dict(v=1880, err=25, how='fleur-de-lis heads of the tall bars'),
        post_top_z=dict(v=2150, err=40, how='the vase and ball on the post, in the oblique view'),
        post_shaft_width=dict(v=100, err=25, how='oblique view, blur doubled by the 32 degree angle'),
        bar_thick_width=dict(v=22, err=10, how='the tall bars read 40 to 55 at 1 mm in the oblique view (blur x 2): about 22 across'),
        resolution_mm_per_px_across=dict(v=10, err=None, how='5.4 mm native at 7 m, divided by sin 32 degrees along the wall'),
    ),
    'R3D': dict(
        wall_top_z=dict(v=620, err=15, how='the strongest brightness step at z 608 to 621 over s 100 to 1000, eight courses plus the coping'),
        bottom_rail_axis_z=dict(v=680, err=15, how='1 mm elevation s 1400 to 2400'),
        top_rail_axis_z=dict(v=1085, err=12, how='1 mm elevation: a flat bar'),
        bar_tip_z=dict(v=1130, err=20, how='the bars stand 45 above the top rail, with a small spear point'),
        bar_pitch=dict(v=94.5, err=3, how='ten bars read at s 1500, 1600, 1695, 1790, 1885, 1975, 2060, 2155, 2250, 2340 on the gridded 1 mm elevation; a line fit gives the pitch and the first bar (two automated searches found 4 bars at rms 12 mm and 65 to 70 mm pitches: the foliage behind the railing defeats them)'),
        bar_centres_s=dict(v=[1500, 1600, 1695, 1790, 1885, 1975, 2060, 2155, 2250, 2340], err=6, how='read by eye on the 1 mm elevation, +-6'),
        bar_width=dict(v=13, err=3, how='blur included: a round bar of 12 to 14'),
        gate_width=dict(v=1040, err=150, how='the leaf between the brick pier and its stile in the 38 degree view, at 5.5 m'),
        gate_top_z=dict(v=1100, err=40, how='the gate\'s top rail level with the railing\'s'),
        paint_srgb=dict(v=[38, 56, 36], err=10, how='median of the gate leaf in shade (32, 47, 28) and in light (51, 69, 45)'),
    ),
    'LHB': dict(
        span_mm=dict(v=2840, err=60, how='axis to axis of the two posts, from their flanges\' front edges moved back 143'),
        upper_lug_z=dict(v=800, err=30, how='the chain\'s end link at the post, 2 mm elevation'),
        lower_lug_z=dict(v=405, err=30, how='the same, lower'),
        upper_chain_lowest_z=dict(v=585, err=25, how='lowest dark band of the upper swag at mid-span'),
        lower_chain_lowest_z=dict(v=165, err=25, how='lowest dark band of the lower swag'),
        post_top_z=dict(v=1086, err=35, how='the dome\'s top; the bollards target states 1135 at its 1.17 m (4 % higher, inside both errors)'),
        flange_bolts=dict(v=4, err=0, how='four hex nuts on studs, two seen at the sides and one in front'),
    ),
}


NOSCALE = {'red_courses_between', 'flange_bolts', 'bar_foot', 'paint_srgb', 'resolution_mm_per_px_across'}


def _sc(v, f):
    if isinstance(v, (int, float)):
        return round(v * f, 2)
    if isinstance(v, list):
        return [_sc(x, f) for x in v]
    return v


def scaled_hand_reads(raw=None):
    """every length read at the first version's pooled height, multiplied by new / first for its object (narrow point 1 of the fresh review)"""
    raw = raw or HAND_READS
    out = {}
    for frame, d in raw.items():
        f = SCALE[frame]
        out[frame] = {}
        for k, e in d.items():
            e2 = dict(e)
            if k not in NOSCALE:
                e2['v'] = _sc(e['v'], f)
                if e.get('err'):
                    e2['err'] = round(e['err'] * f, 2)
            e2['read_at_h'] = FIRST_H[frame]
            e2['scaled_by'] = f if k not in NOSCALE else 1.0
            out[frame][k] = e2
    return out


if __name__ == '__main__':
    pano_dir = sys.argv[1]
    out = dict(R3B=r3b(pano_dir), hand_reads=scaled_hand_reads(), hand_reads_as_read_at_first_version=HAND_READS, scale=SCALE, camera_heights=H_CAM, first_version_heights=FIRST_H)
    json.dump(out, open(os.path.join(HERE, 'photo_measurements.json'), 'w'), indent=1)
    print(json.dumps(out['R3B'], indent=1)[:1800])
