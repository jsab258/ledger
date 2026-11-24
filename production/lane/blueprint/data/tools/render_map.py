#!/usr/bin/env python3
"""Draw map-topdown.svg from map.json (never by hand). Usage: python3 render_map.py [map.json] [out.svg] [--source paper]
Written 24 Nov 2026. Plain standard library. Scale 2 px a metre for the whole map, plus a Quay Street inset at 8 px a metre."""
import json, math, os, sys
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
src = sys.argv[1] if len(sys.argv) > 1 and not sys.argv[1].startswith('--') else os.path.join(HERE, '..', 'map.json')
out = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('--') else os.path.join(HERE, '..', 'map-topdown.svg')
M = json.load(open(src))

S = 2.0
X0, X1, Y0, Y1 = -100, 565, -75, 410
MARGIN = 30
INSET = dict(x0=95, x1=160, y0=-8, y1=62, s=8.0)
W = (X1 - X0) * S + 2 * MARGIN
H_MAIN = (Y1 - Y0) * S + 2 * MARGIN
IW = (INSET['x1'] - INSET['x0']) * INSET['s']
IH = (INSET['y1'] - INSET['y0']) * INSET['s']
H = H_MAIN + IH + 120

COL = dict(bg='#e9e4d8', water='#9fb6c3', road='#5d5d5d', pave='#bdb6a6', quay='#a99f8a', foot='#8a7b62', bldg='#6f5a4a', yard='#cfc6b0',
           place='#8c3b2a', door='#f2c14e', text='#222', lamp='#e8a33a', ladder='#1f4a66', vault='#c0392b', edge='#2c6e49', rank='#5b2c83')

def tx(x, ox=X0, s=S, mx=MARGIN):
    return mx + (x - ox) * s

def ty(y, oy=Y1, s=S, my=MARGIN):
    return my + (oy - y) * s

def poly(pts, f):
    return ' '.join('%.2f,%.2f' % f(x, y) for x, y in pts)

def offset_line(pts, off):
    """Offset a polyline to the left by off (metres)."""
    res = []
    for i, (x, y) in enumerate(pts):
        if i == 0:
            dx, dy = pts[1][0] - x, pts[1][1] - y
        elif i == len(pts) - 1:
            dx, dy = x - pts[i - 1][0], y - pts[i - 1][1]
        else:
            ax, ay = x - pts[i - 1][0], y - pts[i - 1][1]
            bx, by = pts[i + 1][0] - x, pts[i + 1][1] - y
            la, lb = math.hypot(ax, ay), math.hypot(bx, by)
            dx, dy = ax / la + bx / lb, ay / la + by / lb
        L = math.hypot(dx, dy)
        res.append((x - dy / L * off, y + dx / L * off))
    return res

def draw(view, f, s, scale_text=1.0, labels=True, detail=False):
    o = []
    fs = lambda n: '%.1f' % (n * scale_text)
    for w in M['water']:
        o.append('<polygon points="%s" fill="%s"/>' % (poly(w['poly'], f), COL['water']))
    # pavement and apron bands, then carriageways
    for r in M['roads']:
        if r['foot_only']:
            continue
        cw = r['carriageway_m'] / 2.0
        for side, sign in (('left', 1), ('right', -1)):
            sd = r[side]
            if sd.get('kind') in ('pavement', 'quay', 'bridge'):
                w = sd['width_m'] + 0.125
                a = offset_line(r['pts'], sign * cw)
                b = offset_line(r['pts'], sign * (cw + w))
                o.append('<polygon points="%s" fill="%s"/>' % (poly(a + b[::-1], f), COL['quay'] if sd['kind'] == 'quay' else COL['pave']))
    for r in M['roads']:
        if r['foot_only']:
            continue
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-linejoin="round"/>' % (poly(r['pts'], f), COL['road'], r['carriageway_m'] * s))
    for r in M['roads']:
        if not r['foot_only']:
            continue
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="%.2f" stroke-dasharray="%.1f,%.1f" stroke-linejoin="round"/>'
                 % (poly(r['pts'], f), COL['foot'], max(1.2, r['carriageway_m'] * s), 3 * s, 1.2 * s))
    # quay edges
    for e in M['quay_edges']:
        o.append('<polyline points="%s" fill="none" stroke="#3d3a33" stroke-width="%.2f"/>' % (poly(e['pts'], f), max(0.8, 0.6 * s)))
    # plots
    for p in M['plots']:
        if p.get('building'):
            fill = COL['place'] if p.get('place') else COL['bldg']
            if p['use'] in ('home',):
                fill = '#7d6a58'
            o.append('<polygon points="%s" fill="%s" stroke="#2b221b" stroke-width="0.5" opacity="0.92"/>' % (poly(p['outline'], f), fill))
        else:
            o.append('<polygon points="%s" fill="%s" stroke="#8d846f" stroke-width="0.5"/>' % (poly(p['outline'], f), COL['yard']))
    # doors
    for d in M['doors']:
        x, y = f(d['x'], d['y'])
        r = max(1.3, 0.45 * s)
        o.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s" stroke="#222" stroke-width="0.4"/>' % (x, y, r, COL['door'] if not d['locked'] else '#c9c3b5'))
    for l in M['lamp_columns']:
        x, y = f(l['x'], l['y'])
        o.append('<circle cx="%.2f" cy="%.2f" r="%.2f" fill="%s"/>' % (x, y, max(1.0, 0.35 * s), COL['lamp']))
    for l in M['quay_ladders']:
        x, y = f(l['x'], l['y'])
        o.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s"/>' % (x - 1.2, y - 1.2, 2.4, 2.4, COL['ladder']))
    for v in M['vault_places']:
        x, y = f(v['x'], v['y'])
        o.append('<path d="M%.2f %.2f l4 -4 l4 4" fill="none" stroke="%s" stroke-width="1.6"/>' % (x - 4, y + 2, COL['vault']))
    for pbx in M['phone_boxes']:
        x, y = f(pbx['x'], pbx['y'])
        o.append('<rect x="%.2f" y="%.2f" width="4" height="4" fill="#c0392b" stroke="#000" stroke-width="0.4"/>' % (x - 2, y - 2))
    for rk in M['cab_ranks']:
        o.append('<polyline points="%s" fill="none" stroke="%s" stroke-width="2.5"/>' % (poly(rk['pts'], f), COL['rank']))
    if detail:
        for pr in M['props']['items']:
            x, y = f(pr['x'], pr['y'])
            o.append('<circle cx="%.2f" cy="%.2f" r="0.9" fill="#4a4a4a"/>' % (x, y))
        for b in M['bollards']:
            x, y = f(b['x'], b['y'])
            o.append('<circle cx="%.2f" cy="%.2f" r="0.8" fill="#111"/>' % (x, y))
    if not labels:
        return o
    # labels: streets at mid-length, places at their centroid
    for r in M['roads']:
        pts = r['pts']
        L = sum(math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]) for i in range(len(pts) - 1))
        acc, target = 0, L * 0.5
        for i in range(len(pts) - 1):
            l = math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1])
            if acc + l >= target:
                t = (target - acc) / l
                x = pts[i][0] + t * (pts[i + 1][0] - pts[i][0])
                y = pts[i][1] + t * (pts[i + 1][1] - pts[i][1])
                ang = -math.degrees(math.atan2(pts[i + 1][1] - pts[i][1], pts[i + 1][0] - pts[i][0]))
                if ang > 90:
                    ang -= 180
                if ang < -90:
                    ang += 180
                X, Y = f(x, y)
                o.append('<text x="%.1f" y="%.1f" font-size="%s" fill="#fff" text-anchor="middle" dominant-baseline="middle" transform="rotate(%.1f %.1f %.1f)" font-family="sans-serif" font-weight="bold">%s</text>'
                         % (X, Y, fs(7 if not r['foot_only'] else 6), ang, X, Y, escape(r['name'])) if not r['foot_only'] else
                         '<text x="%.1f" y="%.1f" font-size="%s" fill="#4a3b22" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)" font-family="sans-serif" font-style="normal">%s</text>'
                         % (X, Y - 4, fs(6), ang, X, Y, escape(r['name'])))
                break
            acc += l
    for p in M['plots']:
        if not p.get('place'):
            continue
        xs = [a for a, b in p['outline']]
        ys = [b for a, b in p['outline']]
        X, Y = f(sum(xs) / len(xs), sum(ys) / len(ys))
        o.append('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" text-anchor="middle" font-family="sans-serif" stroke="#e9e4d8" stroke-width="2.2" paint-order="stroke">%s</text>'
                 % (X, Y, fs(6.5), COL['text'], escape(p['name'])))
    for e in M['soft_edges']:
        X, Y = f(e['x'], e['y'])
        o.append('<text x="%.1f" y="%.1f" font-size="%s" fill="%s" font-family="sans-serif" font-weight="bold" text-anchor="middle">soft edge: %s</text>'
                 % (X, Y - 6, fs(7), COL['edge'], escape(', '.join(d.replace('_', ' ') for d in e['districts']))))
    return o

parts = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">' % (W, H, W, H),
         '<rect width="100%%" height="100%%" fill="%s"/>' % COL['bg'],
         '<text x="%d" y="20" font-size="14" font-family="sans-serif" font-weight="bold" fill="#222">The Hook and its docks: map.json drawn top-down (metres from the ferry landing, x east, y north). Built from the file by render_map.py, %s.</text>'
         % (MARGIN, escape(M.get('version', '')))]
parts += draw('main', lambda x, y: (tx(x), ty(y)), S)
# grid ticks every 50 m
for gx in range(-100, 566, 50):
    parts.append('<text x="%.1f" y="%.1f" font-size="8" fill="#555" font-family="sans-serif" text-anchor="middle">%d</text>' % (tx(gx), ty(Y0) + 12, gx))
for gy in range(-50, 411, 50):
    if gy < Y0:
        continue
    parts.append('<text x="%.1f" y="%.1f" font-size="8" fill="#555" font-family="sans-serif">%d</text>' % (6, ty(gy) + 3, gy))
# scale bar and legend
sx, sy = tx(380), ty(-62)
parts.append('<rect x="%.1f" y="%.1f" width="%.1f" height="4" fill="#222"/><text x="%.1f" y="%.1f" font-size="9" font-family="sans-serif">100 m</text>' % (sx, sy, 100 * S, sx, sy - 3))
legend = [('door (open by hours / locked)', COL['door']), ('lamp column', COL['lamp']), ('quay ladder', COL['ladder']), ('vault place', COL['vault']),
          ('phone box', '#c0392b'), ('cab rank', COL['rank']), ('named place', COL['place']), ('foot-only way (dashed)', COL['foot'])]
lx, ly = tx(-95), ty(-50)
for i, (t, c) in enumerate(legend):
    parts.append('<rect x="%.1f" y="%.1f" width="8" height="8" fill="%s"/><text x="%.1f" y="%.1f" font-size="9" font-family="sans-serif">%s</text>'
                 % (lx + (i % 4) * 150, ly + (i // 4) * 13, c, lx + (i % 4) * 150 + 11, ly + (i // 4) * 13 + 8, escape(t)))
# the inset
oy = H_MAIN + 40
ox = MARGIN
parts.append('<text x="%d" y="%d" font-size="12" font-family="sans-serif" font-weight="bold">Inset: Quay Street as built (8 px a metre), Mickey\'s yard, the yards\' lane and the ginnel\'s foot</text>' % (ox, oy - 8))
parts.append('<svg x="%d" y="%d" width="%d" height="%d" viewBox="0 0 %d %d"><rect width="100%%" height="100%%" fill="%s" stroke="#333"/>' % (ox, oy, IW, IH, IW, IH, COL['bg']))
fi = lambda x, y: (tx(x, INSET['x0'], INSET['s'], 0), ty(y, INSET['y1'], INSET['s'], 0))
parts += draw('inset', fi, INSET['s'], scale_text=1.4, labels=True, detail=True)
for p in M['plots']:
    if p.get('street') == 'quay_street' and p.get('building') and p.get('number'):
        xs = [a for a, b in p['outline']]
        ys = [b for a, b in p['outline']]
        X, Y = fi(sum(xs) / len(xs), sum(ys) / len(ys))
        parts.append('<text x="%.1f" y="%.1f" font-size="11" fill="#fff" text-anchor="middle" font-family="sans-serif">%d</text>' % (X, Y + 14, p['number']))
parts.append('</svg>')
parts.append('</svg>')
open(out, 'w').write('\n'.join(parts))
print('wrote', out, int(W), 'x', int(H))
