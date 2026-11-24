#!/usr/bin/env python3
"""Draw paper-map.svg (blueprint data file 15) from map.json: Tom's paper map of the Hook.

Written 24 Nov 2026. Part 6.3: a drawn map, not a list; streets and water always drawn, as on a
folded street plan; every place mark is its own group, hidden until Tom has been there or been told
of it (the game sets the group's visibility; the file starts with only Mickey's shown, "the letter
said"). No "you are here" (Q20, recommended no). No minimap. Same seed as the street scatter, so the
pen wobble never changes between builds. Plain standard library.
"""
import json, math, os, random
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, '..', 'map.json')))
try:
    PL = {p['id']: p for p in json.load(open(os.path.join(HERE, '..', 'places.json'))).get('places', [])}
except Exception:
    PL = {}
OUT = os.path.join(HERE, '..', 'paper-map.svg')
rng = random.Random(19900214)

S = 1.6
X0, X1, Y0, Y1 = -95, 610, -30, 410
W, H = (X1 - X0) * S + 60, (Y1 - Y0) * S + 90
f = lambda x, y: (30 + (x - X0) * S, 60 + (Y1 - y) * S)

def wobble(pts, amp=0.9, step=12.0):
    out = []
    for i in range(len(pts) - 1):
        (ax, ay), (bx, by) = pts[i], pts[i + 1]
        L = math.hypot(bx - ax, by - ay)
        n = max(1, int(L / step))
        nx, ny = -(by - ay) / L, (bx - ax) / L
        for k in range(n):
            t = k / n
            j = (rng.random() - 0.5) * 2 * amp if 0 < k else 0
            out.append((ax + (bx - ax) * t + nx * j, ay + (by - ay) * t + ny * j))
    out.append(pts[-1])
    return out

def path(pts):
    q = [f(*p) for p in pts]
    return 'M' + ' L'.join('%.1f %.1f' % p for p in q)

def offset(pts, off):
    res = []
    for i, (x, y) in enumerate(pts):
        a = pts[max(0, i - 1)]
        b = pts[min(len(pts) - 1, i + 1)]
        dx, dy = b[0] - a[0], b[1] - a[1]
        L = math.hypot(dx, dy) or 1
        res.append((x - dy / L * off, y + dx / L * off))
    return res

INK, PENCIL, PAPER = '#2a2620', '#5a5148', '#f1e8d2'
o = ['<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d" data-file="paper-map.svg" data-version="%s">' % (W, H, W, H, M['version']),
     '<title>The Hook, on paper</title>',
     '<desc>Tom\'s paper map, drawn from map.json. Chosen: the named streets and the water are printed, as on a bought street plan, and always shown; every place mark (plotted places and spots alike) and every back way (the ginnel, the yards\' lane, the cuts, the gap) is hidden until Tom has been there or been told of it (part 6.3). No position marker (Q20).</desc>',
     '<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(35)"><line x1="0" y1="0" x2="0" y2="6" stroke="#7d8a92" stroke-width="0.7"/></pattern></defs>',
     '<rect width="100%%" height="100%%" fill="%s"/>' % PAPER,
     '<path d="M %.0f 0 V %.0f M 0 %.0f H %.0f" stroke="#d8ccb0" stroke-width="1.2"/>' % (W / 2, H, H / 2, W),  # the fold lines
     '<text x="30" y="34" font-family="Georgia, serif" font-size="20" fill="%s">The Hook</text>' % INK,
     '<text x="140" y="34" font-family="Georgia, serif" font-size="11" fill="%s">and the docks. Quay to the south.</text>' % PENCIL]
o.append('<g id="water">')
for w in M['water']:
    pts = w['poly'] + [w['poly'][0]]
    o.append('<path d="%s Z" fill="url(#hatch)" stroke="%s" stroke-width="0.8"/>' % (path(wobble(pts, 0.6, 20)), PENCIL))
o.append('</g><g id="streets">')
for r in M['roads']:
    half = r['carriageway_m'] / 2.0 + (0 if r['foot_only'] else 2.0)
    if r['foot_only']:
        # back ways are pencilled in only once Tom has walked them or been told (the game shows the group)
        o.append('<g class="way" data-way="%s" visibility="hidden"><path d="%s" fill="none" stroke="%s" stroke-width="1" stroke-dasharray="4 3"/></g>' % (r['id'], path(wobble(r['pts'], 0.5)), PENCIL))
    else:
        for side in (half, -half):
            o.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.2" stroke-linecap="round"/>' % (path(wobble(offset(r['pts'], side), 0.7)), INK))
o.append('</g><g id="street-names" font-family="Georgia, serif" font-style="italic" font-size="9" fill="%s">' % INK)
for r in M['roads']:
    if r['foot_only']:
        continue   # back ways carry no printed name
    pts = r['pts']
    i = max(range(len(pts) - 1), key=lambda k: math.hypot(pts[k + 1][0] - pts[k][0], pts[k + 1][1] - pts[k][1]))
    (ax, ay), (bx, by) = pts[i], pts[i + 1]
    mx, my = (ax + bx) / 2, (ay + by) / 2
    ang = -math.degrees(math.atan2(by - ay, bx - ax))
    if ang > 90: ang -= 180
    if ang < -90: ang += 180
    X, Y = f(mx, my)
    o.append('<text x="%.1f" y="%.1f" text-anchor="middle" transform="rotate(%.1f %.1f %.1f)" dy="-%d">%s</text>' % (X, Y, ang, X, Y, 6 if not r['foot_only'] else 3, escape(r['name'])))
o.append('</g><g id="places" font-family="Georgia, serif" font-size="8.5" fill="%s">' % PENCIL)
start_known = {'mickeys'}
seen = set()
for p in M['plots']:
    pid = p.get('place')
    if not pid or pid in seen:
        continue
    seen.add(pid)
    xs = [a for a, b in p['outline']]
    ys = [b for a, b in p['outline']]
    cx, cy = sum(xs) / len(xs), sum(ys) / len(ys)
    X, Y = f(cx, cy)
    name = PL.get(pid, {}).get('name', p['name'])
    vis = 'visible' if pid in start_known else 'hidden'
    o.append('<g class="place" data-place="%s" visibility="%s"><path d="M%.1f %.1f l5 5 M%.1f %.1f l-5 5" stroke="%s" stroke-width="1.3"/><text x="%.1f" y="%.1f">%s</text></g>'
             % (pid, vis, X - 2.5, Y - 2.5, X + 2.5, Y - 2.5, INK, X + 5, Y + 3, escape(name)))
# places without a plot (phone boxes, ranks, the bus stop, posts, fishing spots, the bonfire ground): hidden marks at their spot
for pid, p in sorted(PL.items()):
    if pid in seen or p.get('plot') or pid.startswith('edge_'):
        continue
    x, y = p.get('x'), p.get('y')
    if x is None or y is None:
        continue
    seen.add(pid)
    X, Y = f(x, y)
    o.append('<g class="place" data-place="%s" visibility="hidden"><circle cx="%.1f" cy="%.1f" r="2.2" fill="none" stroke="%s" stroke-width="1"/><text x="%.1f" y="%.1f">%s</text></g>'
             % (pid, X, Y, INK, X + 4, Y + 3, escape(p.get('name', pid))))
for e in M['soft_edges']:
    X, Y = f(e['x'], e['y'])
    txt = 'to ' + ', '.join(d.replace('_', ' ').title().replace('The ', 'the ') for d in e['districts'])
    o.append('<g class="place" data-place="%s" visibility="visible"><text x="%.1f" y="%.1f" font-style="italic">%s</text></g>' % (e['id'], X - 20, Y - 8 if e['id'] == 'edge_north' else Y - 14, escape(txt)))
o.append('</g>')
o.append('<text x="%.0f" y="%.0f" font-family="Georgia, serif" font-size="9" fill="%s">Places he has been or been told of are marked in pencil. No "you are here".</text>' % (30, H - 14, PENCIL))
o.append('</svg>')
open(OUT, 'w').write('\n'.join(o))
print('wrote', OUT, len(seen), 'place marks')
