#!/usr/bin/env python
"""Draws the railings target from target.json ALONE, at 1 mm a pixel (large views are scaled to fit 4000 px).
    /home/user/.bpyenv/bin/python target_drawing.py OUTDIR
writes OUTDIR/drawing.json (every view as filled polygons in millimetres: {"views": {name: {"plane", "units", "polygons": [{"layer", "poly"}]}}})
and one PNG per view in OUTDIR (pictures never go into git outside production/previews/).
Views: the A1 elevation (rectangular hollow-section posts and rails, 17 bars, end plates, four M10 bolts with the nuts on the posts' outer faces, the reinstatement patches),
the A1 section across the rails at a bar-free gap, the A1 plan, the A1 bolt section (a plan cut along the top rail's bolt axis), the walking-strip section across the footway
(rail, stallriser, the fish market's awning); Q2a, Q2b and the short Q2b end bay (elevations), the plan of the base plate; the reserve railings R3B, R3A, R3D (a sample of each);
the street plan at the guard rail; the jetty plan with the three Q2 runs and the kit's mooring rings.  The functions are imported by self_check.py (groups C and D)."""
import json, math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'target.json')))

COL = {'iron': (28, 28, 30), 'iron_green': (38, 56, 36), 'cap': (50, 50, 54), 'weld': (60, 60, 64), 'bar': (28, 28, 30), 'chain': (40, 40, 44), 'ground': (150, 140, 130),
       'plate': (60, 60, 64), 'nut': (150, 150, 152), 'kerb': (170, 170, 168), 'flag': (200, 198, 190), 'wall': (150, 90, 70), 'bg': (236, 234, 228), 'string': (60, 70, 100), 'coping': (130, 130, 128),
       'frontage': (190, 160, 140), 'water': (150, 170, 180), 'cope': (150, 150, 146), 'jetty': (190, 190, 184), 'dim': (200, 40, 40), 'patch': (45, 43, 41), 'zinc': (118, 120, 122)}


def rect(x0, x1, z0, z1):
    return [(x0, z0), (x1, z0), (x1, z1), (x0, z1)]


def circle(cx, cz, r, n=40):
    return [(cx + r * math.cos(2 * math.pi * k / n), cz + r * math.sin(2 * math.pi * k / n)) for k in range(n)]


def stadium(cx, cz, length, width, ang, n=10):
    """an oval link: a rectangle with semicircular ends, length along the angle"""
    r = width / 2.0
    L = length - width
    pts = []
    for k in range(n + 1):
        a = -math.pi / 2 + math.pi * k / n
        pts.append((L / 2 + r * math.cos(a), r * math.sin(a)))
    for k in range(n + 1):
        a = math.pi / 2 + math.pi * k / n
        pts.append((-L / 2 + r * math.cos(a), r * math.sin(a)))
    c, s = math.cos(ang), math.sin(ang)
    return [(cx + x * c - y * s, cz + x * s + y * c) for x, y in pts]


def lathe_elev(profile, cx):
    """(r, z) profile -> an elevation polygon mirrored about x = cx"""
    left = [(cx - r, z) for r, z in profile]
    right = [(cx + r, z) for r, z in profile]
    return left + right[::-1]


def shift(pts, dx, dy):
    return [(x + dx, y + dy) for x, y in pts]


class View:
    def __init__(self, name, plane, bounds, what=''):
        self.name, self.plane, self.bounds, self.what, self.polys = name, plane, bounds, what, []

    def add(self, layer, poly):
        self.polys.append(dict(layer=layer, poly=[[round(float(x), 2), round(float(y), 2)] for x, y in poly]))

    def json(self):
        return dict(plane=self.plane, units='mm', bounds=self.bounds, what=self.what, polygons=self.polys)


# ------------------------------------------------------------------------------------------------------------ A1
def a1_parts(K=None):
    """the A1 panel's solids in the elevation plane (x, z): dict layer -> list of polygons; the numbers the self-check reads back.
    Layers: post, cap, rail (both rails), endplate, bar, weld (the 2 mm bar-end fillets), nut, thread (outside the nut), bolt_hidden (shank and head, inside the rail end and the post)"""
    Kk = K or T['kinds']['A1']
    A = Kk['panel']
    P = Kk['profiles']
    out = {'post': [], 'cap': [], 'rail': [], 'endplate': [], 'bar': [], 'weld': [], 'nut': [], 'thread': [], 'bolt_hidden': []}
    pw = A['post']['width'] / 2
    cz0, cz1 = A['cap']['z']
    for x in A['post']['x']:
        out['post'].append(rect(x - pw, x + pw, 0, cz0))
        out['cap'].append(rect(x - pw, x + pw, cz0, cz1))
    ep = A['end_plates']['thickness']
    for nm in ('top_rail', 'bottom_rail'):
        R = A[nm]
        zc, hh = R['axis_z'], R['height'] / 2
        out['rail'].append(rect(R['x'][0], R['x'][1], zc - hh, zc + hh))
        for xe, s in ((R['x'][0], 1), (R['x'][1], -1)):
            out['endplate'].append(rect(xe, xe + s * ep, zc - hh, zc + hh))
    bz0, bz1 = A['infill']['z']
    br = A['infill']['diameter'] / 2
    wf = A['weld']['bead']
    for x in A['infill']['x']:
        out['bar'].append(rect(x - br, x + br, bz0, bz1))
        for sx in (-1, 1):
            out['weld'].append([(x + sx * br, bz0), (x + sx * (br + wf), bz0), (x + sx * br, bz0 + wf)])
            out['weld'].append([(x + sx * br, bz1), (x + sx * (br + wf), bz1), (x + sx * br, bz1 - wf)])
    nut_half_z = max(v for u, v in P['bolt_nut_hex'])
    head_half_z = max(v for u, v in P['bolt_head_hex'])
    shank = P['bolt_shank_diameter'] / 2
    for b in A['bolts']['list']:
        z = b['z']
        n0, n1 = sorted(b['nut_x'])
        out['nut'].append(rect(n0, n1, z - nut_half_z, z + nut_half_z))
        te = b['thread_end_x']
        t0, t1 = (n1, te) if te > 0 else (te, n0)
        out['thread'].append(rect(min(t0, t1), max(t0, t1), z - shank, z + shank))
        h0, h1 = sorted(b['head_x'])
        out['bolt_hidden'].append(rect(h0, h1, z - head_half_z, z + head_half_z))
        a_, b_ = sorted((b['head_x'][1], b['nut_x'][0]))
        out['bolt_hidden'].append(rect(a_, b_, z - shank, z + shank))
    return out


def a1_patch_extent(K=None):
    pts = (K or T['kinds']['A1'])['ground']['patch']['outline_xy']
    xs = [p[0] for p in pts]
    return min(xs), max(xs)


def a1_views():
    Kk = T['kinds']['A1']
    A = Kk['panel']
    P = Kk['profiles']
    v = View('A1_elevation', 'x (along the panel), z (up); seen from the footway side (the nuts are on the posts\' outer faces)', [-1100, 1100, -60, 1060], 'the guard rail panel: RHS posts and rails, 17 bars, four bolts')
    PP = a1_parts()
    v.add('ground', rect(-1100, 1100, -60, 0))
    px0, px1 = a1_patch_extent()
    for x in A['post']['x']:
        v.add('patch', rect(x + px0, x + px1, -Kk['ground']['patch']['flush_with_flags'], 0))
    for L_ in ('bar', 'weld', 'rail', 'endplate', 'post', 'cap', 'nut', 'thread', 'bolt_hidden'):
        for p in PP[L_]:
            v.add(L_, p)
    # section across the rails at a bar-free gap (x = half a pitch from the middle bar)
    xg = A['infill']['pitch'] / 2.0
    s = View('A1_section_rails', 'y (across; + toward the carriageway), z (up): section at x = %.1f (between two bars)' % xg, [-80, 80, -20, 1060], 'the two rails cut at a bar-free gap; the post and the next bar beyond')
    s.add('post_beyond', rect(-A['post']['depth'] / 2, A['post']['depth'] / 2, 0, A['post']['height']))
    s.add('beyond', rect(-A['infill']['diameter'] / 2, A['infill']['diameter'] / 2, A['infill']['z'][0], A['infill']['z'][1]))
    for nm, key in (('top_rail', 'top_rail_section'), ('bottom_rail', 'bottom_rail_section')):
        zc = A[nm]['axis_z']
        s.add('rail', shift([(a, b) for a, b in P[key]['outer']], 0, zc))
        s.add('hole', shift([(a, b) for a, b in P[key]['inner']], 0, zc))
    pl = View('A1_plan', 'x (along), y (across; + toward the carriageway): seen from above', [-1100, 1100, -170, 170], 'plan: the RHS posts (50 x 30), the top rail laid flat (50 across), the bars, the nuts and the tarmac patches')
    for x in A['post']['x']:
        pl.add('patch', shift([(a, b) for a, b in Kk['ground']['patch']['outline_xy']], x, 0))
    for x in A['infill']['x']:
        pl.add('bar', circle(x, 0, A['infill']['diameter'] / 2, 16))
    R = A['top_rail']
    pl.add('rail', rect(R['x'][0], R['x'][1], -R['width'] / 2, R['width'] / 2))
    for x in A['post']['x']:
        pl.add('post', shift([(a, b) for a, b in P['post_section']['outer']], x, 0))
        pl.add('hole', shift([(a, b) for a, b in P['post_section']['inner']], x, 0))
        pl.add('cap', shift([(a, b) for a, b in P['cap_plate']['outline']], x, 0))
    nut_half_y = max(u for u, v_ in P['bolt_nut_hex'])
    for b in A['bolts']['list']:
        if b['z'] == A['top_rail']['axis_z']:
            n0, n1 = sorted(b['nut_x'])
            pl.add('nut', rect(n0, n1, -nut_half_y, nut_half_y))
            te = b['thread_end_x']
            pl.add('thread', rect(min(n1, te), max(n1, te), -5, 5) if te > 0 else rect(min(n0, te), max(n0, te), -5, 5))
    # the bolt section: a plan cut along the top rail's bolt axis (z 985), the right-hand post
    bs = View('A1_bolt_section', 'x (along), y (across): cut at z = %.0f through the top rail\'s bolt axis, the right-hand end' % A['top_rail']['axis_z'], [900, 1100, -40, 40], 'the rail end, the end plate, the post wall, the bolt and its nut, 2:1 in the preview')
    xp = A['post']['x'][1]
    R = A['top_rail']
    wall = R['wall']
    bs.add('rail', rect(R['x'][1] - 150, R['x'][1], -R['width'] / 2, R['width'] / 2))
    bs.add('hole', rect(R['x'][1] - 150, R['x'][1], -R['width'] / 2 + wall, R['width'] / 2 - wall))
    ep = A['end_plates']['thickness']
    bs.add('endplate', rect(R['x'][1] - ep, R['x'][1], -R['width'] / 2 + wall, R['width'] / 2 - wall))
    bs.add('post', rect(xp - A['post']['width'] / 2, xp + A['post']['width'] / 2, -A['post']['depth'] / 2, A['post']['depth'] / 2))
    bs.add('hole', rect(xp - A['post']['width'] / 2 + A['post']['wall'], xp + A['post']['width'] / 2 - A['post']['wall'], -A['post']['depth'] / 2 + A['post']['wall'], A['post']['depth'] / 2 - A['post']['wall']))
    bt = [b for b in A['bolts']['list'] if b['post_x'] > 0 and b['z'] == R['axis_z']][0]
    h0, h1 = sorted(bt['head_x'])
    n0, n1 = sorted(bt['nut_x'])
    hy = max(u for u, v_ in P['bolt_head_hex'])
    ny = max(u for u, v_ in P['bolt_nut_hex'])
    bs.add('nut', rect(h0, h1, -hy, hy))
    bs.add('bolt', rect(h1, bt['thread_end_x'], -P['bolt_shank_diameter'] / 2, P['bolt_shank_diameter'] / 2))
    bs.add('nut', rect(n0, n1, -ny, ny))
    # a walking-strip section across the footway
    ws = walking_section()
    return [v, s, pl, bs, ws]


def walking_section():
    """y (up from the footway, mm) against z (across the footway, mm, the street frame): the rail, the stallriser, the awning's valance and sloping underside, and the strip a person needs"""
    W = T['street_fixtures']['walking_strip']
    A = T['kinds']['A1']['panel']
    za = T['placements']['street'][0]['z_axis_m'] * 1000
    v = View('A1_walking_section', 'z (across the footway, mm, the street frame), y (up from the footway, mm): section at x 10.5 to 12.5 (the awning over it)', [3000, 5300, -60, 3100], 'rail, stallriser, awning and the 0.68 m strip a person needs, 0 to 2.0 m high')
    v.add('ground', rect(3000, 5300, -60, 0))
    # the rail seen in section: post 30 deep, top rail 50 across, bottom rail 40, one bar 12
    half = A['top_rail']['width'] / 2
    v.add('post', rect(za - A['post']['depth'] / 2, za + A['post']['depth'] / 2, 0, A['post']['height']))
    v.add('rail', rect(za - half, za + half, A['top_rail']['axis_z'] - 15, A['top_rail']['axis_z'] + 15))
    v.add('rail', rect(za - A['bottom_rail']['width'] / 2, za + A['bottom_rail']['width'] / 2, 190, 210))
    fz = W['stallriser_face_z_m'] * 1000
    v.add('frontage', rect(fz, 5300, 0, 3000))
    aw = W['awning']
    zf = aw['front_edge_z_m'] * 1000
    zb = aw['z_m'][1] * 1000
    y_front = aw['body_underside_above_footway_at_front_m'] * 1000
    y_wall = y_front + aw['body_slope'] * (zb - zf)
    v.add('awning', [(zf, y_front), (zb, y_wall), (zb, y_wall + 90), (zf, y_front + 90)])
    v.add('valance', rect(zf - 8, zf + 8, aw['valance_bottom_above_footway_m'] * 1000, y_front + 90))
    zr = W['rear_face_z_m'] * 1000
    v.add('person_strip', rect(zr, zr + 680, 0, 2000))
    v.add('clear', rect(zr, fz, 0, 1500))
    return v


# ------------------------------------------------------------------------------------------------------------ Q2
def catenary_pts(x0, x1, z_eye, sag, n=60):
    span = x1 - x0
    # exact catenary through the two eyes with the given sag: solve a from sag = a (cosh(span / 2a) - 1)
    lo, hi = 1.0, 1e8
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * (math.cosh(span / (2 * mid)) - 1) > sag:
            lo = mid
        else:
            hi = mid
    a = (lo + hi) / 2
    xm = (x0 + x1) / 2
    pts = [(x0 + span * k / n, z_eye - sag + a * (math.cosh((x0 + span * k / n - xm) / a) - 1)) for k in range(n + 1)]
    return pts, a


def chain_links(pts, link):
    """link centres every pitch along the polyline; alternate links in the plane (outline) and edge-on (a bar)"""
    pitch = link['pitch']
    out = []
    d_acc = 0.0
    x_prev, z_prev = pts[0]
    out.append((x_prev, z_prev, math.atan2(pts[1][1] - pts[0][1], pts[1][0] - pts[0][0])))
    want = pitch
    for i in range(1, len(pts)):
        x, z = pts[i]
        seg = math.hypot(x - x_prev, z - z_prev)
        while d_acc + seg >= want:
            f = (want - d_acc) / seg
            cx, cz = x_prev + (x - x_prev) * f, z_prev + (z - z_prev) * f
            out.append((cx, cz, math.atan2(z - z_prev, x - x_prev)))
            want += pitch
        d_acc += seg
        x_prev, z_prev = x, z
    return out


def q2_bay_view(tag, bay, chain, short=False):
    Q = T['kinds']['Q2']
    post = Q['post']
    R = post['od'] / 2
    v = View(tag + '_elevation', 'x (along the run), z (up)', [-bay / 2 - 120, bay / 2 + 120, -40, 1160],
             'one %.1f m bay of the quay railing seen from the land side' % (bay / 1000.0) + (' with the chain' if chain else ' with two rails'))
    v.add('ground', rect(-bay / 2 - 120, bay / 2 + 120, -40, 0))
    bp = post['base_plate']
    for sx in (-1, 1):
        xc = sx * bay / 2
        v.add('plate', rect(xc - bp['size'][0] / 2, xc + bp['size'][0] / 2, 0, bp['thickness']))
        for nx in (-bp['holes']['pitch'] / 2, bp['holes']['pitch'] / 2):
            v.add('nut', rect(xc + nx - 12, xc + nx + 12, bp['thickness'], bp['thickness'] + 13))
            v.add('nut', rect(xc + nx - 4, xc + nx + 4, bp['thickness'] + 13, bp['thickness'] + 23))
        v.add('post', rect(xc - R, xc + R, bp['thickness'], post['height'] - post['cap']['rise']))
        cr = post['cap']['od'] / 2
        cap = [(xc - cr, post['height'] - post['cap']['rise'])] + [(xc + cr * math.cos(math.pi - math.pi * k / 12), post['height'] - post['cap']['rise'] + post['cap']['rise'] * math.sin(math.pi * k / 12)) for k in range(0, 13)]
        v.add('cap', cap + [(xc + cr, post['height'] - post['cap']['rise'])])
    tr = Q['top_rail']
    xr = bay / 2 - R
    v.add('rail', rect(-xr, xr, tr['axis_z'] - tr['od'] / 2, tr['axis_z'] + tr['od'] / 2))
    if not chain:
        lr = Q['low_rail']
        v.add('rail', rect(-xr, xr, lr['axis_z'] - lr['od'] / 2, lr['axis_z'] + lr['od'] / 2))
    else:
        ch = Q['chain']
        sb = ch['short_bay'] if short else ch
        ear = ch['eyes']['ear']
        ex = bay / 2 - R - ear['hole_centre_from_post_surface']
        ear_len = max(p[0] for p in Q['profiles']['ear_outline']['outline'])
        for sx in (-1, 1):
            xs = sx * (bay / 2 - R)
            xe = xs - sx * ear_len
            v.add('ear', rect(min(xs, xe), max(xs, xe), ch['eyes']['z'] - ear['height'] / 2, ch['eyes']['z'] + ear['height'] / 2))
            v.add('hole', circle(sx * ex, ch['eyes']['z'], ear['hole_diameter'] / 2, 20))
        pts, a = catenary_pts(-ex, ex, ch['eyes']['z'], sb['sag'])
        for j, (cx, cz, ang) in enumerate(chain_links(pts, ch['link'])):
            if j % 2 == 0:
                v.add('chain', stadium(cx, cz, ch['link']['outer_length'], ch['link']['outer_width'], ang))
            else:
                v.add('chain', stadium(cx, cz, ch['link']['outer_length'], ch['link']['bar'], ang))
        v.add('chain_curve', [(x, z) for x, z in pts])
    return v


def q2_views():
    Q = T['kinds']['Q2']
    post = Q['post']
    R = post['od'] / 2
    views = [q2_bay_view('Q2a', Q['bay']['centre_to_centre'], False),
             q2_bay_view('Q2b', Q['bay']['centre_to_centre'], True),
             q2_bay_view('Q2b_short', Q['bay']['short_end_bay'], True, short=True)]
    pl = View('Q2_plate_plan', 'x, y (mm), the base plate and its four studs', [-130, 130, -130, 130], 'plan of a post foot')
    pl.add('plate', rect(-100, 100, -100, 100))
    pl.add('post', circle(0, 0, R))
    hp = post['base_plate']['holes']['pitch'] / 2
    for sx in (-1, 1):
        for sy in (-1, 1):
            pl.add('nut', circle(sx * hp, sy * hp, 13.9, 6))
    views.append(pl)
    return views


# ------------------------------------------------------------------------------------------------------------ reserve kinds (a sample of each)
def r3b_bar_positions(K=None, s0=700.0, s1=3600.0):
    """predicted bar centres s (mm) of the park railing's fixed panel, left of the hinge post, from its pitch and its first measured bar;
    (s, tall) with tall every second bar (the first measured bar is a short one).  The gate leaf right of the post is swung open: the plane magnifies it, so it is not drawn."""
    Kk = K or T['kinds']['R3B']
    B = Kk['bars']
    limit = Kk['post']['axis_s']['v'] - Kk['post']['shaft_width']['v'] / 2 - 5.0
    out = []
    first, p, lo, hi = B['first_s'], B['pitch'], s0, min(s1, limit)
    k = int(math.ceil((lo - first) / p))
    while first + k * p <= hi:
        out.append((first + k * p, (k % 2 == 1)))
        k += 1
    return out


def r3b_view(s0=None, s1=None, z0=None, z1=None):
    K = T['kinds']['R3B']
    pv = T['photo_frames']['R3B']['preview']
    s0, s1, z0, z1 = [pv[k] if x is None else x for k, x in (('s0', s0), ('s1', s1), ('z0', z0), ('z1', z1))]
    v = View('R3B_elevation', 's (along the railing), z (up from the ground)', [s0, s1, z0, z1], 'the tall park railing on its plinth, in the photograph\'s frame')
    ct = K['plinth']['coping_top_z']['v']
    v.add('plinth', rect(s0, s1, 0, ct))
    v.add('coping', rect(s0, s1, ct - 40, ct))
    rails = K['rails']
    for key in ('bottom_axis_z', 'mid_axis_z', 'top_axis_z'):
        z = rails[key]['v']
        v.add('rail', rect(s0, s1, z - 10, z + 10))
    bars = K['bars']
    br = bars['diameter'] / 2
    head = bars['head_rz']
    zb = rails['bottom_axis_z']['v']
    for s, tall in r3b_bar_positions(K, s0, s1):
        v.add('head', circle(s, zb - 12, 10, 16))
        if tall:
            v.add('bar', rect(s - br, s + br, zb, head[0][1]))
            v.add('head', lathe_elev([(r, z) for r, z in head], s))
        else:
            zm = rails['mid_axis_z']['v']
            zs = bars['short_tip_z']['v']
            v.add('bar', rect(s - br, s + br, zb, zm + 60))
            v.add('head', [(s - br, zm + 60), (s + br, zm + 60), (s + 4, zs - 40), (s, zs), (s - 4, zs - 40)])
    pst = K['post']
    ps = pst['axis_s']['v']
    prof = K['profiles']['hinge_post_rz']
    w = pst['shaft_width']['v'] / 2
    v.add('post', rect(ps - w, ps + w, ct, prof[0][1]))
    v.add('post', lathe_elev([(r, z) for r, z in prof], ps))
    return v


def r3d_view():
    K = T['kinds']['R3D']
    win = T['photo_frames']['R3D']['preview']
    s0, s1 = win['s0'], win['s1']
    v = View('R3D_elevation', 's, z', [s0, s1, win['z0'], win['z1']], 'the low green railing on its garden wall, in the photograph\'s frame')
    wt = K['wall']['top_z']['v']
    v.add('wall', rect(s0, s1, 0, wt))
    zb, zt = K['rails']['bottom_axis_z']['v'], K['rails']['top_axis_z']['v']
    v.add('rail', rect(s0, s1, zb - 8, zb + 8))
    v.add('rail', rect(s0, s1, zt - 8, zt + 8))
    br = K['bars']['width']['v'] / 2
    tip = K['bars']['tip_z']['v']
    s = K['bars']['first_s'] - K['bars']['pitch']['v'] * 15
    while s < s1:
        if s > s0:
            v.add('bar', rect(s - br, s + br, zb, tip - 15))
            v.add('head', [(s - br, tip - 15), (s + br, tip - 15), (s, tip)])
        s += K['bars']['pitch']['v']
    return v


def r3a_view():
    K = T['kinds']['R3A']
    win = T['photo_frames']['R3A']['preview']
    s0, s1 = win['s0'], K['bars']['left_run_max_s']['v']
    v = View('R3A_elevation', 's, z', [win['s0'], win['s1'], win['z0'], win['z1']], 'the area railing on its two-stage dwarf wall (oblique photograph; the LEFT run only, s below %.0f)' % s1)
    v.add('wall', rect(s0, s1, 0, K['wall']['top_z']['v']))
    v.add('string', rect(s0, s1, K['wall']['string_z']['v'] - 30, K['wall']['string_z']['v']))
    v.add('coping', rect(s0, s1, K['wall']['top_z']['v'] - 40, K['wall']['top_z']['v']))
    for key in ('bottom_axis_z', 'mid_axis_z', 'top_axis_z'):
        z = K['rails'][key]['v']
        v.add('rail', rect(s0, s1, z - 10, z + 10))
    p = K['bars']['pitch_all']['v']
    br = 9.0
    zb, zm, zt = K['rails']['bottom_axis_z']['v'], K['rails']['mid_axis_z']['v'], K['bars']['tall_tip_z']['v']
    st = K['bars']['tall_first_s']['v']
    k = -int(st // (2 * p)) - 1
    while True:
        s = st + 2 * p * k
        if s > s1:
            break
        if s > s0 + 20:
            v.add('bar', rect(s - br * 1.4, s + br * 1.4, zb, zt - 120))
            v.add('head', [(s - 30, zt - 120), (s + 30, zt - 120), (s + 12, zt - 40), (s, zt), (s - 12, zt - 40)])
        ss = s + p
        if s0 + 20 < ss <= s1:
            v.add('bar', rect(ss - br, ss + br, zb, zm + 90))
            v.add('head', [(ss - 22, zm + 90), (ss, zm + 90 + 55), (ss + 22, zm + 90), (ss, zm + 90 - 30)])
        k += 1
    return v


# ------------------------------------------------------------------------------------------------------------ plans
def street_plan():
    """x along, z across, metres converted to mm; x 8 to 14, z 2.8 to 5.3"""
    SF = T['street_frame']
    A = T['kinds']['A1']['panel']
    P = T['kinds']['A1']['profiles']
    W = T['street_fixtures']['walking_strip']
    v = View('street_plan', 'x (street, mm), z (across, mm): the east footway at the guard rail', [8000, 14000, 2800, 5300], 'plan: carriageway edge, kerb, footway, guard rail with its patches, gully, stallriser, awning and the walking strip')
    v.add('road', rect(8000, 14000, 2800, 3000))
    v.add('kerb', rect(8000, 14000, 3000, SF['kerb_back_kerbs_target_z_m'] * 1000))
    v.add('flag', rect(8000, 14000, SF['kerb_back_kerbs_target_z_m'] * 1000, SF['stallriser_face_z_m'] * 1000))
    v.add('frontage', rect(8000, 14000, SF['stallriser_face_z_m'] * 1000, 5300))
    v.add('gully', rect(11780, 12220, 2800, 3000))
    aw = W['awning']
    v.add('awning_plan', rect(aw['x_m'][0] * 1000, aw['x_m'][1] * 1000, aw['z_m'][0] * 1000, aw['z_m'][1] * 1000))
    pl = T['placements']['street'][0]
    z = pl['z_axis_m'] * 1000
    xs = [x * 1000 for x in pl['x_m']]
    v.add('walk', rect(W['x_range_m'][0] * 1000, W['x_range_m'][1] * 1000, W['rear_face_z_m'] * 1000, W['stallriser_face_z_m'] * 1000))
    for x in xs:
        # local y (+ toward the carriageway) is street -z
        v.add('patch', [(x + a, z - b) for a, b in T['kinds']['A1']['ground']['patch']['outline_xy']])
    R = A['top_rail']
    v.add('rail', rect(xs[0] + (R['x'][0] - A['post']['x'][0]), xs[1] + (R['x'][1] - A['post']['x'][1]), z - R['width'] / 2, z + R['width'] / 2))
    for x in xs:
        v.add('post', rect(x - A['post']['width'] / 2, x + A['post']['width'] / 2, z - A['post']['depth'] / 2, z + A['post']['depth'] / 2))
    for b in A['bolts']['list']:
        if b['z'] == A['top_rail']['axis_z']:
            xc = xs[0] if b['post_x'] < 0 else xs[1]
            n0, n1 = sorted(b['nut_x'])
            nh = max(u for u, v_ in P['bolt_nut_hex'])
            v.add('nut', rect(xc + (n0 - b['post_x']), xc + (n1 - b['post_x']), z - nh, z + nh))
    return v


def jetty_plan():
    P = T['placements']['quay']
    Q = T['kinds']['Q2']
    v = View('jetty_plan', 'x (along Quay Street, mm), y (across, mm): the jetty in the south-quay kit\'s frame', [-132000, -106000, -70000, -12000],
             'plan: the jetty strip, the parapet, the harbour light plinth, the K6 bollards and K7 cleats, the kit\'s two mooring rings, and the three Q2 runs (post and ring symbols enlarged)')
    v.add('jetty', rect(-130000, -110000, -70000, -15000))
    v.add('parapet', rect(-129400, -128600, -70000, -23000))
    v.add('light_plinth', rect(-121400, -118600, -20900, -18100))
    for (x, y) in T['street_fixtures']['kit_rings_jetty_m']:
        v.add('ring', circle(x * 1000, y * 1000, 220, 24))
    for y in (-45.0,):
        v.add('bollard', circle(-110.75 * 1000, y * 1000, 200, 20))
    for y in (-52.0, -58.0, -64.0):
        v.add('bollard', circle(-110.25 * 1000, y * 1000, 120, 16))
    rw = Q['top_rail']['od'] / 2
    for b in P_bays():
        (x0, y0), (x1, y1) = b['a'], b['b']
        X0, Y0, X1, Y1 = x0 * 1000, y0 * 1000, x1 * 1000, y1 * 1000
        L = math.hypot(X1 - X0, Y1 - Y0)
        nx, ny = -(Y1 - Y0) / L * rw, (X1 - X0) / L * rw
        v.add('rail' if b['model'] == 'Q2a' else 'rail_chain', [(X0 + nx, Y0 + ny), (X1 + nx, Y1 + ny), (X1 - nx, Y1 - ny), (X0 - nx, Y0 - ny)])
    done = set()
    for run in P[:3]:
        for (x, y) in run['posts_xy_m']:
            if (x, y) in done:
                continue
            done.add((x, y))
            model = run['kind'] if (x, y) not in [tuple(p) for p in P[0]['posts_xy_m']] else 'Q2a'
            v.add('plate', rect(x * 1000 - 100, x * 1000 + 100, y * 1000 - 100, y * 1000 + 100))
            v.add('post_' + model, circle(x * 1000, y * 1000, Q['post']['od'] / 2))
    return v


def P_bays():
    return T['placements']['bays_detail']


def all_views():
    return a1_views() + q2_views() + [r3b_view(), r3a_view(), r3d_view(), street_plan(), jetty_plan()]


def draw(view, path, scale=1.0, margin=30):
    x0, x1, y0, y1 = view.bounds
    W, H = int((x1 - x0) * scale) + 2 * margin, int((y1 - y0) * scale) + 2 * margin
    big = max(W, H)
    if big > 4000:
        scale *= 4000.0 / big
        W, H = int((x1 - x0) * scale) + 2 * margin, int((y1 - y0) * scale) + 2 * margin
    im = Image.new('RGB', (W, H), COL['bg'])
    d = ImageDraw.Draw(im)

    def px(p):
        return (margin + (p[0] - x0) * scale, margin + (y1 - p[1]) * scale)
    fills = {'ground': COL['ground'], 'patch': COL['patch'], 'post': COL['iron'], 'cap': COL['cap'], 'rail': COL['iron'], 'bar': COL['bar'], 'weld': COL['weld'], 'endplate': COL['plate'],
             'plate': COL['plate'], 'nut': COL['nut'], 'thread': COL['nut'], 'bolt': (110, 110, 112), 'hole': COL['bg'], 'beyond': (110, 110, 112),
             'ear': COL['iron'], 'chain': COL['chain'], 'plinth': COL['wall'], 'coping': COL['coping'], 'head': COL['iron'], 'wall': COL['wall'], 'string': COL['string'], 'road': (120, 120, 118),
             'kerb': COL['kerb'], 'flag': COL['flag'], 'frontage': COL['frontage'], 'gully': (80, 60, 50), 'walk': (150, 200, 150), 'jetty': COL['jetty'], 'parapet': COL['cope'],
             'light_plinth': (120, 120, 118), 'post_Q2a': COL['iron'], 'post_Q2b': (80, 40, 40), 'rail_chain': (80, 40, 40), 'awning': (190, 120, 90), 'valance': (170, 100, 80),
             'ring': (200, 120, 40), 'bollard': (60, 60, 64), 'clear': (200, 225, 200),
             'post_beyond': None, 'awning_plan': None, 'chain_curve': None, 'bolt_hidden': None, 'person_strip': None}
    order = {'clear': 0}
    for pg in sorted(view.polys, key=lambda p: order.get(p['layer'], 1)):
        pts = [px(p) for p in pg['poly']]
        f = fills.get(pg['layer'], (90, 90, 90))
        if f is None:
            d.line(pts + [pts[0]], fill=(200, 60, 60), width=1)
        else:
            d.polygon(pts, fill=f)
    im.save(path)
    return im.size


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('usage: target_drawing.py OUTDIR   (pictures never go into git outside production/previews/)')
        sys.exit(2)
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    js = {'views': {}}
    for v in all_views():
        js['views'][v.name] = v.json()
        size = draw(v, os.path.join(out, v.name + '.png'))
        print(v.name, size, len(v.polys), 'polygons')
    json.dump(js, open(os.path.join(out, 'drawing.json'), 'w'))
    print('wrote', os.path.join(out, 'drawing.json'))
