#!/usr/bin/env python
"""Draws the railings target from target.json ALONE, at 1 mm a pixel.
    /home/user/.bpyenv/bin/python target_drawing.py OUTDIR
writes OUTDIR/drawing.json (every view as filled polygons in millimetres: {"views": {name: {"plane", "units", "polygons": [{"layer", "poly"}]}}})
and one PNG per view in OUTDIR (pictures never go into git outside production/previews/).
Views: A1 elevation, A1 post section and plan; Q2a and Q2b bay elevations, plan of the base plate; the reserve railings R3B, R3A, R3D (a sample of each);
the street plan at the guard rail; the jetty plan with the Q2 runs.  The functions are imported by self_check.py (group C and D)."""
import json, math, os, sys
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'target.json')))

COL = {'iron': (28, 28, 30), 'iron_green': (38, 56, 36), 'cap': (50, 50, 54), 'weld': (60, 60, 64), 'bar': (28, 28, 30), 'chain': (40, 40, 44), 'ground': (150, 140, 130),
       'plate': (60, 60, 64), 'nut': (150, 150, 152), 'kerb': (170, 170, 168), 'flag': (200, 198, 190), 'wall': (150, 90, 70), 'bg': (236, 234, 228), 'string': (60, 70, 100), 'coping': (130, 130, 128),
       'frontage': (190, 160, 140), 'water': (150, 170, 180), 'cope': (150, 150, 146), 'jetty': (190, 190, 184), 'dim': (200, 40, 40)}


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


class View:
    def __init__(self, name, plane, bounds, what=''):
        self.name, self.plane, self.bounds, self.what, self.polys = name, plane, bounds, what, []

    def add(self, layer, poly):
        self.polys.append(dict(layer=layer, poly=[[round(float(x), 2), round(float(y), 2)] for x, y in poly]))

    def json(self):
        return dict(plane=self.plane, units='mm', bounds=self.bounds, what=self.what, polygons=self.polys)


# ------------------------------------------------------------------------------------------------------------ A1
def a1_parts(K=None):
    """the A1 panel's solids in the elevation plane (x, z): dict layer -> list of polygons; also the numbers the self-check reads back"""
    A = (K or T['kinds']['A1'])['panel']
    pr = A['post']['od'] / 2
    out = {'post': [], 'cap': [], 'rail': [], 'bar': [], 'weld': []}
    for x in A['post']['x']:
        out['post'].append(rect(x - pr, x + pr, 0, A['post']['height'] - A['cap']['thickness']))
        cr = A['cap']['od'] / 2
        out['cap'].append(rect(x - cr, x + cr, A['post']['height'] - A['cap']['thickness'], A['post']['height']))
    for nm in ('top_rail', 'bottom_rail'):
        R = A[nm]
        out['rail'].append(rect(R['x'][0], R['x'][1], R['axis_z'] - R['od'] / 2, R['axis_z'] + R['od'] / 2))
    bz0, bz1 = A['infill']['z']
    br = A['infill']['diameter'] / 2
    for x in A['infill']['x']:
        out['bar'].append(rect(x - br, x + br, bz0, bz1))
    wb = A['weld']['bead']
    for nm in ('top_rail', 'bottom_rail'):
        R = A[nm]
        for xe in R['x']:
            out['weld'].append(rect(xe - wb, xe + wb, R['axis_z'] - R['od'] / 2 - wb, R['axis_z'] + R['od'] / 2 + wb))
    return out


def a1_views():
    A = T['kinds']['A1']['panel']
    v = View('A1_elevation', 'x (along the panel), z (up); the road side toward the viewer', [-1100, 1100, -60, 1060], 'the guard rail panel from the footway side')
    P = a1_parts()
    v.add('ground', rect(-1100, 1100, -60, 0))
    for L_ in ('bar', 'rail', 'post', 'cap', 'weld'):
        for p in P[L_]:
            v.add(L_, p)
    # the dark joint ring at the flags
    for x in A['post']['x']:
        v.add('ring', rect(x - A['post']['od'] / 2 - 20, x + A['post']['od'] / 2 + 20, -6, 0))
    s = View('A1_section_post', 'y (across; + toward the carriageway), z (up): section through a post and the rails at a bar-free gap', [-60, 60, -20, 1060], 'section at x = 0 (rails) and the post outline for scale')
    for nm in ('top_rail', 'bottom_rail'):
        R = A[nm]
        s.add('rail', circle(0, R['axis_z'], R['od'] / 2))
    s.add('post_outline', circle(0, 500, A['post']['od'] / 2))
    pl = View('A1_plan', 'x (along), y (across)', [-1100, 1100, -60, 60], 'plan: the posts are circles of 48.3, the rail line y = 0, bars 12 round')
    for x in A['post']['x']:
        pl.add('post', circle(x, 0, A['post']['od'] / 2))
    pl.add('rail', rect(A['top_rail']['x'][0], A['top_rail']['x'][1], -A['top_rail']['od'] / 2, A['top_rail']['od'] / 2))
    return [v, s, pl]


# ------------------------------------------------------------------------------------------------------------ Q2
def catenary_pts(x0, x1, z_eye, sag, n=60):
    span = x1 - x0
    a = span * span / (8.0 * sag)
    # exact catenary through the two eyes with the given sag: solve a from sag = a (cosh(span / 2a) - 1)
    lo, hi = 1.0, 1e7
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
    d_acc, k = 0.0, 0
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


def q2_views():
    Q = T['kinds']['Q2']
    post = Q['post']
    R = post['od'] / 2
    bay = Q['bay']['centre_to_centre']
    views = []
    for tag, chain in (('Q2a', False), ('Q2b', True)):
        v = View(tag + '_elevation', 'x (along the run), z (up)', [-bay / 2 - 120, bay / 2 + 120, -40, 1160], 'one bay of the quay railing seen from the land side' + (' with the chain' if chain else ''))
        v.add('ground', rect(-bay / 2 - 120, bay / 2 + 120, -40, 0))
        for sx in (-1, 1):
            xc = sx * bay / 2
            bp = post['base_plate']
            v.add('plate', rect(xc - bp['size'][0] / 2, xc + bp['size'][0] / 2, 0, bp['thickness']))
            for nx in (-bp['holes']['pitch'] / 2, bp['holes']['pitch'] / 2):
                v.add('nut', rect(xc + nx - 12, xc + nx + 12, bp['thickness'], bp['thickness'] + 13))
                v.add('nut', rect(xc + nx - 4, xc + nx + 4, bp['thickness'] + 13, bp['thickness'] + 23))
            v.add('post', rect(xc - R, xc + R, bp['thickness'], post['height'] - post['cap']['rise']))
            cap = [(xc - post['cap']['od'] / 2, post['height'] - post['cap']['rise'])] + [(xc + post['cap']['od'] / 2 * math.cos(math.pi - math.pi * k / 12), post['height'] - post['cap']['rise'] + post['cap']['rise'] * math.sin(math.pi * k / 12)) for k in range(0, 13)]
            v.add('cap', cap + [(xc + post['cap']['od'] / 2, post['height'] - post['cap']['rise'])])
        tr = Q['top_rail']
        v.add('rail', rect(tr['x'][0], tr['x'][1], tr['axis_z'] - tr['od'] / 2, tr['axis_z'] + tr['od'] / 2))
        if not chain:
            lr = Q['low_rail']
            v.add('rail', rect(lr['x'][0], lr['x'][1], lr['axis_z'] - lr['od'] / 2, lr['axis_z'] + lr['od'] / 2))
        else:
            ch = Q['chain']
            ex = ch['eyes']['x']
            for sx, xe in ((-1, ex[0]), (1, ex[1])):
                ear = ch['eyes']['ear']
                xs = sx * (bay / 2 - R)
                v.add('ear', rect(min(xs, xs + (-sx) * (ear['hole_centre_from_post_surface'] + 20)), max(xs, xs + (-sx) * (ear['hole_centre_from_post_surface'] + 20)), ch['eyes']['z'] - ear['height'] / 2, ch['eyes']['z'] + ear['height'] / 2))
            pts, a = catenary_pts(ex[0], ex[1], ch['eyes']['z'], ch['sag'])
            for j, (cx, cz, ang) in enumerate(chain_links(pts, ch['link'])):
                if j % 2 == 0:
                    v.add('chain', stadium(cx, cz, ch['link']['outer_length'], ch['link']['outer_width'], ang))
                else:
                    v.add('chain', stadium(cx, cz, ch['link']['outer_length'], ch['link']['bar'], ang))
            v.add('chain_curve', [(x, z) for x, z in pts])
        views.append(v)
    pl = View('Q2_plate_plan', 'x, y (mm), the base plate and its four studs', [-130, 130, -130, 130], 'plan of a post foot')
    bp = post['base_plate']
    pl.add('plate', rect(-100, 100, -100, 100))
    pl.add('post', circle(0, 0, R))
    for sx in (-1, 1):
        for sy in (-1, 1):
            pl.add('nut', circle(sx * 75, sy * 75, 13.9, 6))
    views.append(pl)
    return views


# ------------------------------------------------------------------------------------------------------------ reserve kinds (a sample of each)
def r3b_bar_positions(K=None, s0=700.0, s1=3600.0):
    """predicted bar centres s (mm) of the park railing's fixed panel, left of the hinge post (s < 2535), from its pitch and its first measured bar;
    (s, tall) with tall every second bar (the first measured bar is a short one).  The gate leaf right of the post is swung open: the plane magnifies it, so it is not drawn."""
    B = (K or T['kinds']['R3B'])['bars']
    out = []
    first, p, lo, hi = B['first_s'], B['pitch'], s0, min(s1, 2535.0)
    k = int(math.ceil((lo - first) / p))
    while first + k * p <= hi:
        out.append((first + k * p, (k % 2 == 1)))
        k += 1
    return out


def r3b_view(s0=700.0, s1=3600.0, z0=-50.0, z1=2450.0):
    K = T['kinds']['R3B']
    v = View('R3B_elevation', 's (along the railing), z (up from the ground)', [s0, s1, z0, z1], 'the tall park railing on its plinth, in the photograph\'s frame')
    v.add('plinth', rect(s0, s1, 0, K['plinth']['coping_top_z']['v']))
    v.add('coping', rect(s0, s1, K['plinth']['coping_top_z']['v'] - 40, K['plinth']['coping_top_z']['v']))
    rails = K['rails']
    for key in ('bottom_axis_z', 'mid_axis_z', 'top_axis_z'):
        z = rails[key]['v']
        v.add('rail', rect(s0, s1, z - 10, z + 10))
    bars = K['bars']
    br = bars['diameter'] / 2
    head = bars['head_rz']
    for s, tall in r3b_bar_positions(K, s0, s1):
        zb = rails['bottom_axis_z']['v']
        if tall:
            zt = head[0][1]
            v.add('bar', rect(s - br, s + br, zb, zt))
            v.add('head', lathe_elev([(r, z) for r, z in head], s))
        else:
            zm = rails['mid_axis_z']['v']
            v.add('bar', rect(s - br, s + br, zb, zm + 60))
            v.add('head', [(s - br, zm + 60), (s + br, zm + 60), (s + 4, bars['short_tip_z']['v'] - 40), (s, bars['short_tip_z']['v']), (s - 4, bars['short_tip_z']['v'] - 40)])
    pst = K['post']
    ps = 2590.0
    w = pst['shaft_width']['v'] / 2
    v.add('post', rect(ps - w, ps + w, K['plinth']['coping_top_z']['v'], 1990))
    cw, uw = pst['collar_width']['v'] / 2, pst['urn_width']['v'] / 2
    v.add('post', lathe_elev([(w, 1990), (cw, 2000), (cw, 2035), (w * 0.85, 2060), (w * 0.85, 2110), (uw, 2150), (uw, 2200), (30, 2250), (12, 2300), (5, 2350), (0, pst['top_z']['v'])], ps))
    return v


def r3d_view():
    K = T['kinds']['R3D']
    s0, s1 = 0.0, 2860.0
    v = View('R3D_elevation', 's, z', [s0, s1, -60, 1300], 'the low green railing on its garden wall, in the photograph\'s frame')
    wt = K['wall']['top_z']['v']
    v.add('wall', rect(s0, s1, 0, wt))
    v.add('rail', rect(s0, s1, K['rails']['bottom_axis_z']['v'] - 8, K['rails']['bottom_axis_z']['v'] + 8))
    v.add('rail', rect(s0, s1, K['rails']['top_axis_z']['v'] - 8, K['rails']['top_axis_z']['v'] + 8))
    br = K['bars']['width']['v'] / 2
    s = K['bars']['first_s'] - K['bars']['pitch']['v'] * 15
    while s < s1:
        if s > s0:
            v.add('bar', rect(s - br, s + br, K['rails']['bottom_axis_z']['v'], K['bars']['tip_z']['v'] - 15))
            v.add('head', [(s - br, K['bars']['tip_z']['v'] - 15), (s + br, K['bars']['tip_z']['v'] - 15), (s, K['bars']['tip_z']['v'])])
        s += K['bars']['pitch']['v']
    return v


def r3a_view():
    K = T['kinds']['R3A']
    s0, s1 = 0.0, 3200.0
    v = View('R3A_elevation', 's, z', [s0, s1, -50, 2300], 'the area railing on its two-stage dwarf wall (oblique photograph, sample)')
    v.add('wall', rect(s0, s1, 0, K['wall']['top_z']['v']))
    v.add('string', rect(s0, s1, K['wall']['string_z']['v'] - 30, K['wall']['string_z']['v']))
    v.add('coping', rect(s0, s1, K['wall']['top_z']['v'] - 40, K['wall']['top_z']['v']))
    for key in ('bottom_axis_z', 'mid_axis_z', 'top_axis_z'):
        z = K['rails'][key]['v']
        v.add('rail', rect(s0, s1, z - 10, z + 10))
    p = K['bars']['pitch_all']['v']
    br = 9.0
    k = 0
    s = K['bars']['tall_first_s']['v'] - 2 * p * 2
    while s < s1:
        if s > s0:
            if k % 2 == 0:
                v.add('bar', rect(s - br * 1.4, s + br * 1.4, K['rails']['bottom_axis_z']['v'], K['bars']['tall_tip_z']['v'] - 120))
                v.add('head', [(s - 30, K['bars']['tall_tip_z']['v'] - 120), (s + 30, K['bars']['tall_tip_z']['v'] - 120), (s + 12, K['bars']['tall_tip_z']['v'] - 40), (s, K['bars']['tall_tip_z']['v']), (s - 12, K['bars']['tall_tip_z']['v'] - 40)])
            else:
                v.add('bar', rect(s - br, s + br, K['rails']['bottom_axis_z']['v'], K['rails']['mid_axis_z']['v'] + 90))
        s += p
        k += 1
    return v


# ------------------------------------------------------------------------------------------------------------ plans
def street_plan():
    """x along, z across, metres converted to mm; x 8 to 14, z 2.8 to 5.3"""
    SF = T['street_frame']
    v = View('street_plan', 'x (street, mm), z (across, mm): the east footway at the guard rail', [8000, 14000, 2800, 5300], 'plan: carriageway edge, kerb, footway, guard rail, gully, stallriser')
    v.add('road', rect(8000, 14000, 2800, 3000))
    v.add('kerb', rect(8000, 14000, 3000, SF['kerb_back_kerbs_target_z_m'] * 1000))
    v.add('flag', rect(8000, 14000, SF['kerb_back_kerbs_target_z_m'] * 1000, SF['stallriser_face_z_m'] * 1000))
    v.add('frontage', rect(8000, 14000, SF['stallriser_face_z_m'] * 1000, 5300))
    v.add('gully', rect(11780, 12220, 2800, 3000))
    pl = T['placements']['street'][0]
    z = pl['z_axis_m'] * 1000
    for x in pl['x_m']:
        v.add('post', circle(x * 1000, z, T['kinds']['A1']['panel']['post']['od'] / 2))
    v.add('rail', rect(pl['x_m'][0] * 1000, pl['x_m'][1] * 1000, z - 21.2, z + 21.2))
    v.add('walk', rect(pl['x_m'][0] * 1000, pl['x_m'][1] * 1000, z + 24.15, z + 24.15 + 680))
    return v


def jetty_plan():
    v = View('jetty_plan', 'x (along Quay Street, mm), y (across, mm): the jetty in the south-quay kit\'s frame', [-132000, -108000, -40000, -12000], 'plan: the jetty strip, the parapet, the harbour light plinth, and the two Q2 runs')
    v.add('jetty', rect(-130000, -110000, -40000, -15000))
    v.add('parapet', rect(-129400, -128600, -40000, -23000))
    v.add('light_plinth', rect(-121400, -118600, -20900, -18100))
    P = T['placements']['quay']
    for run in P[:2]:
        for x, y in run['posts_xy_m']:
            v.add('post_' + run['kind'], circle(x * 1000, y * 1000, 38.05))
    pts = [(p[0] * 1000, p[1] * 1000) for p in P[0]['posts_xy_m']] + [(p[0] * 1000, p[1] * 1000) for p in P[1]['posts_xy_m']]
    for (x0, y0), (x1, y1) in zip(pts[:7], pts[1:8]):
        v.add('rail', [(x0 - 24, y0), (x1 - 24, y1), (x1 + 24, y1), (x0 + 24, y0)])
    for (x0, y0), (x1, y1) in zip(pts[7:13], pts[8:14]):
        v.add('rail_chain', [(x0, y0 - 24), (x1, y1 - 24), (x1, y1 + 24), (x0, y0 + 24)])
    return v


def all_views():
    vs = a1_views() + q2_views() + [r3b_view(), r3a_view(), r3d_view(), street_plan(), jetty_plan()]
    return vs


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
    fills = {'ground': COL['ground'], 'ring': (40, 38, 36), 'post': COL['iron'], 'cap': COL['cap'], 'rail': COL['iron'], 'bar': COL['bar'], 'weld': COL['weld'], 'plate': COL['plate'], 'nut': COL['nut'],
             'ear': COL['iron'], 'chain': COL['chain'], 'plinth': COL['wall'], 'coping': COL['coping'], 'head': COL['iron'], 'wall': COL['wall'], 'string': COL['string'], 'road': (120, 120, 118),
             'kerb': COL['kerb'], 'flag': COL['flag'], 'frontage': COL['frontage'], 'gully': (80, 60, 50), 'walk': (150, 200, 150), 'jetty': COL['jetty'], 'parapet': COL['cope'], 'light_plinth': (120, 120, 118),
             'post_Q2a': COL['iron'], 'post_Q2b': (80, 40, 40), 'rail_chain': (80, 40, 40), 'post_outline': None, 'chain_curve': None}
    for pg in view.polys:
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
