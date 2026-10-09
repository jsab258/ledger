#!/usr/bin/env python
"""Draws the kerbs-and-covers target from target.json alone: filled polygons in millimetres (plans, sections, elevations)
into <OUT>/drawing.json and as pictures at 1 mm a pixel into <OUT>.  Pictures never go into git outside production/previews/.

Usage:  /home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [--overlay PREVIEW_DIR]
        --overlay lays the photographed crossing's outlines on the two main photographs in PREVIEW_DIR
        (writes ph-urban_street_03-target-on-photo.jpg and ...-target-on-top-photo.jpg there).

Frames: plan views: x along the kerb, y across (0 = kerb face line, + toward the carriageway = DOWN the picture);
section views: y across (footway left, carriageway right), z up; elevations: x along, z up.
"""
import json, math, os, random, sys
from PIL import Image, ImageDraw

try:
    from shapely.geometry import LineString, Polygon, box as sbox
    from shapely.ops import unary_union
except Exception:  # shapely is optional: the two corner plans are skipped without it
    LineString = None

HERE = os.path.dirname(os.path.abspath(__file__))


def load_target():
    return json.load(open(os.path.join(HERE, 'target.json')))


# --------------------------------------------------------------------------- small helpers
def rect(x0, y0, x1, y1):
    return [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]


def circle(cx, cy, r, n=72):
    return [[cx + r * math.cos(2 * math.pi * i / n), cy + r * math.sin(2 * math.pi * i / n)] for i in range(n)]


def rot_pts(pts, deg, cx=0.0, cy=0.0):
    c, s = math.cos(math.radians(deg)), math.sin(math.radians(deg))
    return [[cx + (x - cx) * c - (y - cy) * s, cy + (x - cx) * s + (y - cy) * c] for x, y in pts]


class View:
    def __init__(self, name, kind, title, xr, yr, axes):
        self.name, self.kind, self.title, self.xr, self.yr, self.axes = name, kind, title, xr, yr, axes
        self.polys = []

    def add(self, name, material, pts, layer=0, line=None):
        self.polys.append({'name': name, 'material': material, 'layer': layer, 'points': [[round(float(x), 2), round(float(y), 2)] for x, y in pts]})
        if line:
            self.polys[-1]['line'] = line

    def to_json(self):
        return {'kind': self.kind, 'title': self.title, 'x_range': self.xr, 'y_range': self.yr, 'axes': self.axes, 'polygons': self.polys}


def lengths_for(rng, start, end, lo, hi, last=None):
    """consecutive lengths from start to end (end approximate; the last piece is cut to fit), no two equal within 20 mm"""
    out, x = [], start
    while x < end - 1:
        L = rng.uniform(lo, hi)
        while last is not None and abs(L - last) < 20:
            L = rng.uniform(lo, hi)
        if x + L > end:
            L = end - x
            if L < lo * 0.5 and out:
                out[-1] += L
                break
        out.append(L)
        last = L
        x += L
    return out


def srgb(t, key, default=(128, 128, 128)):
    m = t['materials'].get(key)
    return tuple(m['srgb']) if m and 'srgb' in m else default


GRANITE_KEYS = ['granite_grey', 'granite_blue_grey', 'granite_pink_grey']


def pick_granite(rng, t):
    sh = t['pieces']['kerb_granite']['variant_share']
    r = rng.random()
    acc = 0.0
    for k in GRANITE_KEYS:
        acc += sh[k]
        if r <= acc:
            return k
    return GRANITE_KEYS[0]


# --------------------------------------------------------------------------- views
def section_kerb(t, which):
    p = t['pieces']['kerb_granite' if which == 'granite' else 'kerb_concrete']
    v = View('section_kerb_' + which, 'section', f'Kerb section, {which}, with channel, footway and road (y across: footway left, carriageway right; z up)',
             [-700, 800], [-300, 330], {'x': 'y (mm, + toward the carriageway)', 'y': 'z (mm, up)'})
    up, W = p['upstand'], p['top_width']
    fz = up - 5          # the footway flags stand 5 below the kerb top
    v.add('footway_bedding', 'mortar_pale', rect(-700, fz - 100, -W, fz - 50), 0)
    v.add('footway_flag', 'flag_pale', rect(-700, fz - 50, -W, fz), 1)
    v.add('kerb_' + which, p['material'], [[a, b] for a, b in p['section_yz']], 2)
    if which == 'granite':
        ch = t['pieces']['channel_setts']
        A, B = ch['courses'][0]['across'], ch['courses'][1]['across']
        v.add('channel_course_A', 'sett_pale_worn', rect(0, -140, A, 0), 1)
        v.add('channel_course_B', 'sett_dull', rect(A, -140, A + B, 0), 1)
        road_start = A + B
    else:
        cc = t['pieces']['channel_concrete']
        v.add('channel_block', 'concrete_kerb', [[a, b] for a, b in cc['section_yz']], 1)
        road_start = cc['width']
    pts = [[road_start, 6]] + [[y, 6 + (y - road_start) / 40.0] for y in (400, 800)] + [[800, -150], [road_start, -150]]
    v.add('asphalt', 'tarmac_infill', pts, 0)
    return v


def section_crossover(t):
    c = t['pieces']['crossover']
    v = View('section_crossover', 'section', 'Crossing section at the middle: footway, ramp, lip row, channel, road (y across, z up)',
             [-1500, 700], [-300, 300], {'x': 'y (mm)', 'y': 'z (mm, up)'})
    r = c['ramp']
    lip = c['lip_row']
    yb, yf = r['plan_y']
    fz = r['z_at_back']
    v.add('footway_bedding', 'mortar_pale', rect(-1500, fz - 100, yb, fz - 50), 0)
    v.add('footway_flag', 'flag_pale', rect(-1500, fz - 50, yb, fz), 1)
    v.add('ramp', 'concrete_ramp', [[yb, fz], [yf, r['z_at_lip']], [yf, -85], [yb, -85]], 1)
    v.add('joint_ramp_lip', 'bitumen_joint', rect(yf, -85, lip['y0'], r['z_at_lip']), 1)
    v.add('lip_row', 'granite_blue_grey', rect(lip['y0'], -120, lip['y1'], lip['top_z']), 2)
    ch = t['pieces']['channel_setts']
    A, B = ch['courses'][0]['across'], ch['courses'][1]['across']
    v.add('channel_course_A', 'sett_pale_worn', rect(0, -140, A, 0), 1)
    v.add('channel_course_B', 'sett_dull', rect(A, -140, A + B, 0), 1)
    pts = [[A + B, 6], [700, 6 + (700 - A - B) / 40.0], [700, -150], [A + B, -150]]
    v.add('asphalt', 'tarmac_infill', pts, 0)
    return v


def kerb_run(t, rng, x0, x1, y_back, shade=True):
    """list of (x_start, length, material) blocks from x0 to x1 (x1 > x0)"""
    p = t['pieces']['kerb_granite']
    ls = lengths_for(rng, x0, x1, p['length_mm']['min'], p['length_mm']['max'])
    out, x = [], x0
    for L in ls:
        out.append((x, L, pick_granite(rng, t)))
        x += L
    return out


def channel_setts_plan(v, t, rng, x0, x1, width):
    """two courses of granite setts between x0 and x1 across 'width' (course A as in the piece, B takes the rest)"""
    p = t['pieces']['channel_setts']
    A = p['courses'][0]['across']
    shares = [(k, w) for k, w in p['colour_share'].items() if k != 'why']
    for (ya, yb, nm) in ((0, A, 'A'), (A, width, 'B')):
        x = x0
        while x < x1:
            L = min(rng.uniform(p['sett_along_mm']['min'], p['sett_along_mm']['max']), x1 - x)
            j = p['joint_mm']
            r, acc, mat = rng.random(), 0.0, shares[0][0]
            for k, w in shares:
                acc += w
                if r <= acc:
                    mat = k
                    break
            v.add(f'sett_{nm}', mat, rect(x + j / 2, ya + j / 2, x + L - j / 2, yb - j / 2), 1)
            x += L


def plan_crossover(t, instance='street'):
    c = t['pieces']['crossover']
    ref = t['reference_instance']
    street = instance == 'street'
    gap = c['width_between_kerb_ends'] if street else ref['gap_between_kerb_ends']
    channel_w = t['pieces']['channel_setts']['width_total'] if street else ref['channel_width']
    rng = random.Random(1990 if street else 2019)
    name = 'plan_crossover_street' if street else 'plan_crossover_photo03'
    half = gap / 2.0
    ext = 1700
    v = View(name, 'plan', ('Crossing at the street\'s 3.0 m' if street else 'The photographed crossing (urban_street_03), gap %d' % ref['gap_between_kerb_ends']) +
             ' (x along the kerb, y across, + toward the carriageway = down the picture)', [-half - ext, half + ext], [-1250, channel_w + 450],
             {'x': 'x (mm)', 'y': 'y (mm, + toward the carriageway: down the picture)'})
    kg = t['pieces']['kerb_granite']
    W = kg['top_width']
    jh = kg['joint_mm']['width'] / 2.0
    jt = c['ramp']['joint_to_lip_and_flanks_mm']
    r = c['ramp']
    fl = c['flank_strips']
    fy0, fy1 = fl['plan_y']
    v.add('footway_flags', 'flag_pale', rect(-half - ext, -1250, half + ext, fy0 - jt), 0)
    for (x, L, m) in kerb_run(t, rng, 0, ext, W):
        v.add('kerb_block_L', m, rect(-half - x - L + jh, -W, -half - x - jh, 0), 3)
    for (x, L, m) in kerb_run(t, rng, 0, ext, W):
        v.add('kerb_block_R', m, rect(half + x + jh, -W, half + x + L - jh, 0), 3)
    if street:
        fw = fl['width_mm']
        lx, rx_ = (-half - fw, -half), (half, half + fw)
    else:
        lx, rx_ = tuple(ref['flank']['left_x']), tuple(ref['flank']['right_x'])
    v.add('flank_L', 'granite_grey', rect(lx[0], fy0, lx[1], fy1), 3)
    v.add('flank_R', 'granite_grey', rect(rx_[0], fy0, rx_[1], fy1), 3)
    rx0, rx1 = (-half + jt, half - jt) if street else (-half + 15, half - jt)
    v.add('ramp', 'concrete_ramp', rect(rx0, r['plan_y'][0], rx1, r['plan_y'][1]), 2)
    lip = c['lip_row']
    v.add('joint_ramp_lip', 'bitumen_joint', rect(rx0, r['plan_y'][1], rx1, lip['y0']), 2)
    n = int(math.ceil(2 * half / (lip['sett_along_mm'] + lip['joint_mm'])))
    pitch = 2 * half / n
    for i in range(n):
        m = 'granite_blue_grey' if rng.random() < 0.45 else ('granite_pink_grey' if rng.random() < 0.12 else 'granite_grey')
        v.add('lip_sett', m, rect(-half + i * pitch + lip['joint_mm'] / 2, lip['y0'], -half + (i + 1) * pitch - lip['joint_mm'] / 2, lip['y1']), 3)
    channel_setts_plan(v, t, rng, -half - ext, half + ext, channel_w)
    if not street:
        g = ref['gully']
        ga = t['pieces']['gully_grate_A']
        gx0, gx1 = g['x_centre'] - g['along'] / 2.0, g['x_centre'] + g['along'] / 2.0
        v.add('gully_grate_A', 'cast_iron_grate', rect(gx0, g['y0'], gx1, g['y1']), 4)
        yc = (g['y0'] + g['y1']) / 2.0
        for xc in ga['slot_centres_x']:
            xs = g['x_centre'] + xc
            v.add('gully_slot', 'grate_slot', rect(xs - ga['slot_width'] / 2, yc - ga['slot_length'] / 2, xs + ga['slot_width'] / 2, yc + ga['slot_length'] / 2), 5)
    v.add('asphalt', 'tarmac_infill', rect(-half - ext, channel_w, half + ext, channel_w + 450), 0)
    return v


def elevation_crossing(t):
    c = t['pieces']['crossover']
    half = c['width_between_kerb_ends'] / 2.0
    rng = random.Random(7)
    v = View('elevation_crossing_face', 'elevation', 'Kerb face looking from the carriageway at the crossing (x along, z up)', [-half - 1700, half + 1700], [-160, 260],
             {'x': 'x (mm)', 'y': 'z (mm, up)'})
    kg = t['pieces']['kerb_granite']
    for side in (-1, 1):
        for (x, L, m) in kerb_run(t, rng, 0, 1700, kg['top_width']):
            xa = half + x
            xb = half + x + L
            if side < 0:
                xa, xb = -xb, -xa
            v.add('kerb_face', m, rect(xa + kg['joint_mm']['width'] / 2.0, 0, xb - kg['joint_mm']['width'] / 2.0, kg['upstand']), 2)
    lip = c['lip_row']
    n = int(math.ceil(2 * half / (lip['sett_along_mm'] + lip['joint_mm'])))
    pitch = 2 * half / n
    for i in range(n):
        v.add('lip_sett', 'granite_blue_grey', rect(-half + i * pitch + 5, 0, -half + (i + 1) * pitch - 5, lip['top_z']), 2)
    v.add('channel_level', 'sett_pale_worn', rect(-half - 1700, -140, half + 1700, 0), 0)
    return v


def plan_gully(t, which):
    p = t['pieces']['gully_grate_' + which]
    if which == 'A':
        W, H = p['overall_along_kerb'], p['overall_across']
        v = View('plan_gully_A', 'plan', 'Gully grate A: %d x %d, %d slots %d x %d at pitch %d, slots across the channel' % (W, H, p['slot_count'], p['slot_width'], p['slot_length'], p['slot_pitch']), [-W / 2 - 60, W / 2 + 60], [-H / 2 - 60, H / 2 + 60],
                 {'x': 'x along the kerb (mm)', 'y': 'y across (mm)'})
        v.add('grate', p['material'], rect(-W / 2, -H / 2, W / 2, H / 2), 0)
        for xc in p['slot_centres_x']:
            v.add('slot', 'grate_slot', rect(xc - p['slot_width'] / 2, -p['slot_length'] / 2, xc + p['slot_width'] / 2, p['slot_length'] / 2), 1)
    else:
        W, H = p['overall_along_kerb'], p['overall_across']
        v = View('plan_gully_B', 'plan', 'Gully grate B: %d x %d, 7 slots %d wide trimmed to an oval field, pitch %d, two lifting holes' % (W, H, p['slot_width'], p['slot_pitch']), [-W / 2 - 60, W / 2 + 60], [-H / 2 - 60, H / 2 + 60],
                 {'x': 'x along the kerb (mm)', 'y': 'y across (mm)'})
        v.add('grate', p['material'], rect(-W / 2, -H / 2, W / 2, H / 2), 0)
        n = p['slot_count']
        for i in range(n):
            xc = (i - (n - 1) / 2.0) * p['slot_pitch']
            L = p['slot_lengths'][i]
            v.add('slot', 'grate_slot', rect(xc - p['slot_width'] / 2, -L / 2, xc + p['slot_width'] / 2, L / 2), 1)
        lh = p['lifting_holes']
        xe = (n - 1) / 2.0 * p['slot_pitch'] + lh['beyond_end_slot_centres_mm']
        for sgn in (-1, 1):
            v.add('lifting_hole', 'grate_slot', circle(sgn * xe, 0, lh['diameter'] / 2.0, 24), 1)
    return v


def plan_cover_stud(t):
    p = t['pieces']['cover_stud_square']
    S = p['outer'][0]
    inner = p['lid_inner'][0]
    v = View('plan_cover_stud_square', 'plan', 'Cover P1: %d square, %d mm frame, two triangular leaves on one diagonal (%g mm joint), 10 x 10 studs %d sq at %d, half-studs on the joint' % (S, p['frame_rim'], p['leaves']['joint_mm'], p['pattern']['stud_mm'], p['pattern']['pitch_mm']),
             [-S / 2 - 40, S / 2 + 40], [-S / 2 - 40, S / 2 + 40], {'x': 'x (mm)', 'y': 'y (mm)'})
    v.add('frame', p['material'], rect(-S / 2, -S / 2, S / 2, S / 2), 0)
    h = inner / 2.0
    jw = float(p['leaves']['joint_mm'])
    n = p['pattern']['count'][0]
    st, pi = p['pattern']['stud_mm'], p['pattern']['pitch_mm']
    if LineString is None:
        v.add('lid', p['material'], rect(-h, -h, h, h), 1, line=[20, 16, 14])
        for i in range(n):
            for j in range(n):
                cx, cy = (i - (n - 1) / 2.0) * pi, (j - (n - 1) / 2.0) * pi
                v.add('stud', 'cast_iron_cover', rect(cx - st / 2, cy - st / 2, cx + st / 2, cy + st / 2), 2, line=[110, 100, 92])
        return v
    lid = sbox(-h, -h, h, h)
    # the joint runs from the lower-left corner (-h, +h) to the upper-right corner (+h, -h) of the picture (y is down)
    cut = LineString([(-h - 50, h + 50), (h + 50, -h - 50)]).buffer(jw / 2.0, cap_style=2)
    leaves = lid.difference(cut)
    geoms = sorted(list(leaves.geoms), key=lambda g: g.centroid.x)
    for k, g in enumerate(geoms):
        v.add(f'leaf_{k + 1}', p['material'], list(g.exterior.coords)[:-1], 1, line=[20, 16, 14])
        for i in range(n):
            for j in range(n):
                cx, cy = (i - (n - 1) / 2.0) * pi, (j - (n - 1) / 2.0) * pi
                sq = sbox(cx - st / 2, cy - st / 2, cx + st / 2, cy + st / 2).intersection(g)
                if sq.is_empty or sq.area < 4:
                    continue
                for gg in (list(sq.geoms) if hasattr(sq, 'geoms') else [sq]):
                    if gg.area >= 4:
                        v.add('stud_half' if gg.area < 0.9 * st * st else 'stud', 'cast_iron_cover', list(gg.exterior.coords)[:-1], 2, line=[110, 100, 92])
        # one round keyhole per leaf, near the middle of the leaf
        c = g.centroid
        v.add('keyhole', 'grate_slot', circle(c.x, c.y, p['keyhole_diameter_mm'] / 2.0, 20), 3)
    bs = p['boss']['size_mm']
    # the blank raised boss on the joint, 150 from the lower end, long axis along the joint
    d = math.sqrt(0.5)
    off = 0.16 * S
    bx, by = -h + off * d + 0.06 * S, h - off * d - 0.06 * S
    v.add('boss', p['material'], rot_pts(rect(bx - bs[0] / 2, by - bs[1] / 2, bx + bs[0] / 2, by + bs[1] / 2), -45, bx, by), 3, line=[110, 100, 92])
    return v


def plan_cover_round(t):
    p = t['pieces']['cover_round_600']
    R = p['frame_outer_diameter'] / 2.0
    v = View('plan_cover_round_600', 'plan', 'Cover P2: round 600 class, frame 690, lid 590, centred lug tread (4 lugs per 71.4 x 83.5 cell)', [-R - 40, R + 40], [-R - 40, R + 40], {'x': 'x (mm)', 'y': 'y (mm)'})
    v.add('frame', p['material'], circle(0, 0, R), 0)
    v.add('lid', p['material'], circle(0, 0, p['lid_diameter'] / 2.0), 1, line=[20, 16, 14])
    pt = p['pattern']
    cell, lug = pt['cell_mm'], pt['lug_mm']
    lim = p['lid_diameter'] / 2.0 - pt['rim_plain_mm']
    nx, ny = int(2 * lim / cell[0]) + 2, int(2 * lim / cell[1]) + 2
    for i in range(-nx // 2, nx // 2 + 1):
        for j in range(-ny // 2, ny // 2 + 1):
            for L in pt['lugs_in_cell']:
                x, y = i * cell[0] + L['centre_mm'][0], j * cell[1] + L['centre_mm'][1]
                w, h = (lug[0], lug[1]) if L['orientation'] == 'horizontal' else (lug[1], lug[0])
                if math.hypot(abs(x) + w / 2, abs(y) + h / 2) < lim:
                    v.add('lug', 'cast_iron_cover', rect(x - w / 2, y - h / 2, x + w / 2, y + h / 2), 2, line=[110, 100, 92])
    return v


def plan_cover_recessed_footway(t):
    p = t['pieces']['cover_recessed_footway']
    W, H = p['outer']
    inf = p['infill']
    v = View('plan_cover_recessed_footway', 'plan', 'Cover P3 (footway): %d x %d frame, two-step rim, %d x %d infill' % (W, H, inf[0], inf[1]), [-W / 2 - 40, W / 2 + 40], [-H / 2 - 40, H / 2 + 40], {'x': 'x (mm)', 'y': 'y (mm)'})
    v.add('flange', p['material'], rect(-W / 2, -H / 2, W / 2, H / 2), 0)
    fl_ = p['frame_flange_mm']
    ledge = (W - 2 * fl_, H - 2 * fl_)
    v.add('ledge', p['material'], rect(-ledge[0] / 2, -ledge[1] / 2, ledge[0] / 2, ledge[1] / 2), 1, line=[20, 16, 14])
    v.add('infill', 'flag_pale', rect(-inf[0] / 2, -inf[1] / 2, inf[0] / 2, inf[1] / 2), 2, line=[90, 86, 80])
    fl = p['frame_lugs']
    lw, lh = fl['lug_mm']
    rowp = fl['row_pitch_mm']
    # two staggered rows along each long side (centres 34 and 34 + 41.75 in from the outer edge), lugs horizontal, second row shifted 35.7
    for sy in (-1, 1):
        for r_, off in enumerate((34.0, 34.0 + rowp)):
            yc = sy * (H / 2 - off)
            x = -W / 2 + 125 + (35.7 if r_ else 0.0)
            while x < W / 2 - 125 - lw / 2:
                v.add('frame_lug', p['material'], rect(x - lw / 2, yc - lh / 2, x + lw / 2, yc + lh / 2), 2, line=[110, 100, 92])
                x += 71.4
    # the ends: three columns of vertical lugs at the left (wider) end, two at the right
    for sx, cols in ((-1, 3), (1, 2)):
        for k in range(cols):
            xc = sx * (W / 2 - 22 - k * 36)
            y = -(H / 2 - 90)
            while y < H / 2 - 90 + 1:
                v.add('frame_lug', p['material'], rect(xc - lh / 2, y - lw / 2, xc + lh / 2, y + lw / 2), 2, line=[110, 100, 92])
                y += 71.4
    c = p['infill_chamfer_mm']
    v.add('infill_chamfer', 'mortar_pale', [[-inf[0] / 2 + c, -inf[1] / 2 + c], [inf[0] / 2 - c, -inf[1] / 2 + c], [inf[0] / 2 - c, inf[1] / 2 - c], [-inf[0] / 2 + c, inf[1] / 2 - c]], 3)
    return v


def plan_cover_recessed_road(t):
    p = t['pieces']['cover_recessed_road']
    W, H = p['outer']
    v = View('plan_cover_recessed_road', 'plan', 'Cover P3 (road): tarmac-filled recess %d x %d, %g mm hairline' % (W, H, p['hairline_mm']), [-W / 2 - 60, W / 2 + 60], [-H / 2 - 60, H / 2 + 60], {'x': 'x (mm)', 'y': 'y (mm)'})
    v.add('road', 'tarmac_infill', rect(-W / 2 - 60, -H / 2 - 60, W / 2 + 60, H / 2 + 60), 0)
    v.add('hairline_outer', 'bitumen_joint', rect(-W / 2, -H / 2, W / 2, H / 2), 1)
    v.add('infill', 'tarmac_infill', rect(-W / 2 + p['hairline_mm'], -H / 2 + p['hairline_mm'], W / 2 - p['hairline_mm'], H / 2 - p['hairline_mm']), 2)
    return v


def plan_cover_double_leaf(t):
    p = t['pieces']['cover_road_double_leaf']
    W, H = p['outer']
    v = View('plan_cover_road_double_leaf', 'plan', 'Cover P4: two-leaf road cover %d x %d, fine stud tread on a 45 degree lattice' % (W, H), [-W / 2 - 160, W / 2 + 160], [-H / 2 - 160, H / 2 + 160], {'x': 'x (mm)', 'y': 'y (mm)'})
    v.add('mortar_surround', 'mortar_pale', rect(-W / 2 - p['surround_mm'], -H / 2 - p['surround_mm'], W / 2 + p['surround_mm'], H / 2 + p['surround_mm']), 0)
    for s in (-1, 1):
        x0, x1 = (-W / 2, -7.5) if s < 0 else (7.5, W / 2)
        v.add('leaf', p['material'], rect(x0, -H / 2, x1, H / 2), 1, line=[20, 16, 14])
    pt = p['pattern']
    st, pi, mg = pt['stud_mm'], pt['pitch_mm'], pt['edge_margin_mm']
    nx, ny = int((W - 2 * mg) / pi), int((H - 2 * mg) / pi)
    for i in range(nx):
        for j in range(ny):
            cx = (i - (nx - 1) / 2.0) * pi
            cy = (j - (ny - 1) / 2.0) * pi
            if abs(cx) < 20:
                continue
            v.add('stud', 'cast_iron_cover', rot_pts(rect(cx - st / 2, cy - st / 2, cx + st / 2, cy + st / 2), 45, cx, cy), 2)
    return v


def plan_service_small(t):
    p = t['pieces']['service_small']
    v = View('plan_service_small', 'plan', 'Small lids: stopcock, gas, telecom blank (left to right)', [-750, 800], [-180, 180], {'x': 'x (mm)', 'y': 'y (mm)'})
    # stopcock round
    v.add('stopcock_frame', p['material'], circle(-500, 0, p['water_stopcock']['frame'] / 2.0), 0)
    v.add('stopcock_lid', p['material'], circle(-500, 0, p['water_stopcock']['lid'][0] / 2.0), 1, line=[20, 16, 14])
    v.add('stopcock_slot', 'grate_slot', rect(-515, -4, -485, 4), 2)
    g = p['gas_box']
    v.add('gas_frame', p['material'], rect(-g['frame'][0] / 2, -g['frame'][1] / 2, g['frame'][0] / 2, g['frame'][1] / 2), 0)
    v.add('gas_lid', p['material'], rect(-g['lid'][0] / 2, -g['lid'][1] / 2, g['lid'][0] / 2, g['lid'][1] / 2), 1, line=[20, 16, 14])
    v.add('gas_slot_L', 'grate_slot', rect(-g['lid'][0] / 2 + 15, -4, -g['lid'][0] / 2 + 40, 4), 2)
    v.add('gas_slot_R', 'grate_slot', rect(g['lid'][0] / 2 - 40, -4, g['lid'][0] / 2 - 15, 4), 2)
    tc = p['telecom_blank']
    cx = 500
    v.add('telecom_surround', 'mortar_pale', rect(cx - tc['frame'][0] / 2 - 30, -tc['frame'][1] / 2 - 30, cx + tc['frame'][0] / 2 + 30, tc['frame'][1] / 2 + 30), 0)
    v.add('telecom_frame', p['material'], rect(cx - tc['frame'][0] / 2, -tc['frame'][1] / 2, cx + tc['frame'][0] / 2, tc['frame'][1] / 2), 1)
    v.add('telecom_lid', 'flag_pale', rect(cx - tc['lid'][0] / 2, -tc['lid'][1] / 2, cx + tc['lid'][0] / 2, tc['lid'][1] / 2), 2, line=[90, 86, 80])
    return v


def plan_corner_mitre(t):
    if LineString is None:
        return None
    p = t['pieces']['kerb_corner_mitre']
    W = t['pieces']['kerb_granite']['top_width']
    ang = p['angle_deg']
    L = p['blocks_each_arm_mm']
    v = View('plan_corner_mitre', 'plan', 'Mitred corner, interior angle 112 degrees, two 900 blocks (face line along the outside)', [-1300, 1300], [-1100, 400], {'x': 'x (mm)', 'y': 'y (mm)'})
    # arms leave the corner O=(0,0): the face line goes from P1 to O to P2; the kerb body lies on the inside of the angle
    a1 = math.radians(180 - (180 - ang) / 2.0)   # arm 1 direction
    a2 = math.radians((180 - ang) / 2.0)          # arm 2 direction
    # footway side is -y (up the picture); arms point left and right, a little upward
    u1 = (-math.cos(math.radians((180 - ang) / 2.0)), -math.sin(math.radians((180 - ang) / 2.0)))
    u2 = (math.cos(math.radians((180 - ang) / 2.0)), -math.sin(math.radians((180 - ang) / 2.0)))
    P1 = (u1[0] * L, u1[1] * L)
    P2 = (u2[0] * L, u2[1] * L)
    line = LineString([P1, (0, 0), P2])
    body = line.buffer(W, single_sided=True, join_style=2, mitre_limit=10)
    ys = [pt[1] for pt in body.exterior.coords]
    if max(ys) > 1:   # wrong side (towards +y): flip
        body = line.buffer(-W, single_sided=True, join_style=2, mitre_limit=10)
    bis = LineString([(0, 0), (0, -3 * W)])
    cut = bis.buffer(4.5, cap_style=2)
    parts = body.difference(cut)
    geoms = list(parts.geoms) if hasattr(parts, 'geoms') else [parts]
    for g in geoms:
        v.add('kerb_block', p['material'], list(g.exterior.coords)[:-1], 2)
    return v


def plan_corner_radius(t):
    p = t['pieces']['kerb_corner_radius']
    R = p['radius_face_mm']
    W = t['pieces']['kerb_granite']['top_width']
    chord = p['block_chord_mm']
    n = int(round(90.0 / math.degrees(chord / R)))
    step = 90.0 / n
    cw = t['pieces']['channel_setts']['width_total']
    v = View('plan_corner_radius', 'plan', 'Radius corner R 6500 to the face: granite blocks cut to the curve, channel setts outside (the footway is up and to the left)',
             [-1500, R + cw + 300], [-R - 300, cw + 300], {'x': 'x (mm)', 'y': 'y (mm)'})
    # the face line starts at the origin heading +x and turns toward the footway side (-y); centre of the curve C = (0, -R)

    def arcpts(r, a0, a1, k=6):
        return [[r * math.cos(math.radians(a0 + (a1 - a0) * i / k)), -R + r * math.sin(math.radians(a0 + (a1 - a0) * i / k))] for i in range(k + 1)]
    rng = random.Random(3)
    v.add('kerb_straight_in', p['material'], rect(-1500, -W, -4.5, 0), 2)
    for i in range(n):
        a0 = 90.0 - i * step
        a1 = a0 - step
        da = math.degrees(4.5 / R)
        v.add('kerb_block', p['material'], arcpts(R, a0 - da, a1 + da) + arcpts(R - W, a1 + da, a0 - da), 2)
    A = t['pieces']['channel_setts']['courses'][0]['across']
    for (r0, r1, nm, mat) in ((R, R + A, 'A', 'sett_pale_worn'), (R + A, R + cw, 'B', 'sett_dull')):
        a = 90.0
        while a > 0.1:
            da = math.degrees(rng.uniform(130, 230) / r0)
            a1 = max(a - da, 0.0)
            j = math.degrees(6 / r0)
            v.add('sett_' + nm, mat, arcpts(r1 - 6, a - j, a1 + j, 4) + arcpts(r0 + 6, a1 + j, a - j, 4), 1)
            a = a1
    return v


def all_views(t):
    vs = [section_kerb(t, 'granite'), section_kerb(t, 'concrete'), section_crossover(t), plan_crossover(t, 'street'), plan_crossover(t, 'photo03'),
          elevation_crossing(t), plan_gully(t, 'A'), plan_gully(t, 'B'), plan_cover_stud(t), plan_cover_round(t), plan_cover_recessed_footway(t),
          plan_cover_recessed_road(t), plan_cover_double_leaf(t), plan_service_small(t), plan_corner_radius(t)]
    m = plan_corner_mitre(t)
    if m is not None:
        vs.append(m)
    return vs


# --------------------------------------------------------------------------- pictures
def render(v, t, path, mm_per_px=1.0):
    x0, x1 = v.xr
    y0, y1 = v.yr
    W, H = int((x1 - x0) / mm_per_px) + 1, int((y1 - y0) / mm_per_px) + 1
    im = Image.new('RGB', (W, H), (236, 232, 224))
    d = ImageDraw.Draw(im)

    def px(pt):
        x, y = pt
        if v.kind == 'plan':
            return ((x - x0) / mm_per_px, (y - y0) / mm_per_px)
        return ((x - x0) / mm_per_px, (y1 - y) / mm_per_px)   # sections and elevations: z up

    for pl in sorted(v.polys, key=lambda q: q['layer']):
        col = srgb(t, pl['material'], (160, 160, 160)) if pl['material'] in t['materials'] else {'grate_slot': (22, 20, 20)}.get(pl['material'], (160, 160, 160))
        d.polygon([px(p) for p in pl['points']], fill=col, outline=tuple(pl.get('line', [40, 36, 34])))
    # scale bar: 500 mm
    bx, by = 30, H - 24
    d.line([(bx, by), (bx + 500 / mm_per_px, by)], fill=(0, 0, 0), width=3)
    d.text((bx, by - 14), '500 mm', fill=(0, 0, 0))
    d.text((10, 6), v.title, fill=(0, 0, 0))
    im.save(path)


# --------------------------------------------------------------------------- overlay on the main photographs
def plan_to_px(t, x_plan, y_plan, z=None, plane='ground'):
    """plan mm -> column, row on the MAIN ortho frame (drawn at the measured camera height of urban_street_03). A point at height z mm above the
    channel level that lies off the frame's plane (the channel, or the kerb-top plane) is smeared away from the camera by (camera - plane) / (camera - z)."""
    ref, fr = t['reference_instance'], t['photo_frames']['MAIN']
    x_local = x_plan + ref['gap_centre_local_x']
    dist = ref['foot_line_distance_from_camera'] - y_plan
    if z is not None:
        cam = fr['camera_height_ground_m'] * 1000.0
        zp = 0.0 if plane == 'ground' else fr['top_plane_z_mm']
        f = (cam - zp) / (cam - z)
        x_local *= f
        dist *= f
    return (x_local - fr['x0_mm']) / fr['mm_per_px'], (fr['z1_mm'] - dist) / fr['mm_per_px']


def overlay(t, preview_dir):
    ref = t['reference_instance']
    fr = t['photo_frames']['MAIN']
    v = plan_crossover(t, 'photo03')
    cw = ref['channel_width']
    out = []
    for which, fname in (('ground', fr['ground_image']), ('top', fr['top_image'])):
        im = Image.open(os.path.join(preview_dir, fname)).convert('RGB')
        lay = Image.new('RGBA', im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(lay)
        c_ = t['pieces']['crossover']
        zmap = ({'lip_sett': c_['lip_row']['top_z'], 'sett_A': 0, 'sett_B': 0, 'gully_grate_A': 0, 'gully_slot': 0} if which == 'ground'
                else {'kerb_block_L': t['pieces']['kerb_granite']['upstand'], 'kerb_block_R': t['pieces']['kerb_granite']['upstand'], 'flank_L': c_['flank_strips']['top_z'], 'flank_R': c_['flank_strips']['top_z']})
        colour = {'gully_slot': (0, 255, 255, 255), 'gully_grate_A': (255, 0, 255, 255), 'lip_sett': (255, 128, 0, 255)}
        for pl in v.polys:
            if pl['name'] not in zmap:
                continue
            pts = [plan_to_px(t, x, y, zmap[pl['name']], which) for x, y in pl['points']]
            d.line(pts + [pts[0]], fill=colour.get(pl['name'], (0, 255, 0, 255)), width=1)
        if which == 'ground':
            for (y, z, col) in ((0, 0, (255, 255, 255, 255)), (cw, 6, (255, 255, 0, 255))):
                d.line([plan_to_px(t, -1800, y, z, 'ground'), plan_to_px(t, 1800, y, z, 'ground')], fill=col, width=1)
        else:
            for (y, z) in ((ref['ramp_back_y'], t['pieces']['crossover']['ramp']['z_at_back']),):
                d.line([plan_to_px(t, -ref['gap_between_kerb_ends'] / 2, y, z, 'top'), plan_to_px(t, ref['gap_between_kerb_ends'] / 2, y, z, 'top')], fill=(255, 255, 0, 255), width=1)
        out_im = Image.alpha_composite(im.convert('RGBA'), lay).convert('RGB')
        name = {'ground': 'ph-urban_street_03-target-on-photo.jpg', 'top': 'ph-urban_street_03-target-on-top-photo.jpg'}[which]
        out_im.save(os.path.join(preview_dir, name), quality=88)
        out.append(name)
    return out


def sheet(t, out_dir, preview_dir):
    """one reduced contact sheet of the drawings (at most 1200 px, under 300 KB) for the reviewers"""
    names = ['section_kerb_granite', 'section_kerb_concrete', 'section_crossover', 'plan_crossover_street', 'plan_gully_A', 'plan_cover_stud_square',
             'plan_cover_round_600', 'plan_cover_recessed_footway', 'plan_cover_road_double_leaf', 'plan_corner_radius']
    tiles = []
    for n in names:
        im = Image.open(os.path.join(out_dir, n + '.png')).convert('RGB')
        im.thumbnail((590, 228))
        tiles.append(im)
    S = Image.new('RGB', (1200, 1180), (255, 255, 255))
    for i, im in enumerate(tiles):
        S.paste(im, ((i % 2) * 600 + 5, (i // 2) * 236 + 4))
    p = os.path.join(preview_dir, 'target-drawing-sheet.jpg')
    q = 85
    while True:
        S.save(p, quality=q, optimize=True)
        if os.path.getsize(p) < 290000 or q < 50:
            break
        q -= 8
    return p


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    out_dir = args[0]
    os.makedirs(out_dir, exist_ok=True)
    t = load_target()
    views = all_views(t)
    js = {'units': 'mm', 'views': {v.name: v.to_json() for v in views}}
    json.dump(js, open(os.path.join(out_dir, 'drawing.json'), 'w'))
    for v in views:
        render(v, t, os.path.join(out_dir, v.name + '.png'))
    print('drew', len(views), 'views into', out_dir)
    if '--overlay' in args:
        pd = args[args.index('--overlay') + 1]
        print('overlays:', overlay(t, pd))
        print('sheet:', sheet(t, out_dir, pd))


if __name__ == '__main__':
    main()
