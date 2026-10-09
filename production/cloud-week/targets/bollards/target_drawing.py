#!/usr/bin/env python
"""Draws the bollards target from target.json ALONE, in millimetres.

/home/user/.bpyenv/bin/python target_drawing.py OUT_DIR [PREVIEWS_DIR [OVERLAY_DIR]]

Writes OUT_DIR/drawing.json: for each kind the elevation (a mirrored outline), plans (circles or outlines at named heights) and, for the chain post, its
bolts, chain link and eye; for the street, the bollards' places as small plan polygons. And pictures at 1 mm a pixel: one per kind (elevation and plan,
a 100 mm grid, a scale bar), a sheet of all kinds, a plan of Quay Street's bollards (25 mm a pixel).
If PREVIEWS_DIR is given (the folder of the reduced photographs) it also lays each kind's elevation on its photograph (*-target-on-photo.jpg, in OVERLAY_DIR if given, else OUT_DIR).
Pictures never go into git outside production/previews/."""
import sys, os, json, math
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bollard_lib as L

T = json.load(open(os.path.join(HERE, 'target.json')))
INK = (20, 20, 20)
FILL = {'K1': (70, 70, 74), 'K2': (110, 112, 116), 'K3': (176, 174, 168), 'K4': (150, 152, 156), 'K5': (60, 60, 66), 'K6': (50, 50, 54), 'K7': (50, 50, 54)}


def circle(r, n=72, cx=0.0, cy=0.0):
    return [[round(cx + r * math.cos(2 * math.pi * i / n), 2), round(cy + r * math.sin(2 * math.pi * i / n), 2)] for i in range(n)]


def polygons():
    P = {}
    for kid, K in T['kinds'].items():
        d = {}
        if 'profile_rz' in K:
            prof = K['profile_rz']
            d['elevation'] = [[round(a, 2), round(b, 2)] for a, b in L.elevation_polygon(prof)]
            rmax = max(r for r, z in prof)
            d['plan_outline'] = circle(rmax)
            d['plan_foot'] = circle(prof[1][0] if len(prof) > 1 else rmax)
            zmid = max(prof, key=lambda p: p[0])
            d['max_radius_at_z'] = zmid[1]
        if kid == 'K5':
            b = K['fixings']['bolts']
            d['bolts_plan'] = [circle(b['nut_across_flats'] / 2.0 / math.cos(math.radians(30)), 6, b['pitch_circle_r'] * math.cos(math.radians(a)),
                                      b['pitch_circle_r'] * math.sin(math.radians(a))) for a in b['angles_deg']]
            ln = K['chain']['link']
            d['chain_link_elevation'] = rounded_rect(ln['outer_length'], ln['outer_width'], ln['bar_diameter'])
            d['chain_eye_z'] = K['fixings']['chain_eyes']['z']
        if kid == 'K6' and 'variants' in K:
            for v in K['variants']:
                if 'profile_rz' in v:
                    d['elevation_K6b'] = [[round(a, 2), round(b, 2)] for a, b in L.elevation_polygon(v['profile_rz'])]
        if kid == 'K7':
            half = K['elevation_half_xz']
            d['elevation'] = [[-x, z] for x, z in reversed(half)] + [[x, z] for x, z in half[1:]]
            d['plan'] = [[-K['length'] / 2, -K['width'] / 2], [K['length'] / 2, -K['width'] / 2], [K['length'] / 2, K['width'] / 2], [-K['length'] / 2, K['width'] / 2]]
        P[kid] = d
    # the places: small plan polygons in metres of street frame (x along, z across), r from the kind's base radius
    pl = T['placements']
    marks = []
    for e in pl['street_proper']:
        xs = e['x_m']
        zs = e.get('z_m')
        zs = zs if isinstance(zs, list) else [zs] * len(xs)
        for x, z in zip(xs, zs):
            marks.append(dict(id=e['id'], kind=e['kind'], x_m=x, z_m=z))
    P['places'] = marks
    return P


def rounded_rect(L_, W, bar):
    # a chain link seen face on: a stadium outline of overall L_ x W
    pts = []
    r = W / 2.0
    for i in range(0, 19):
        a = math.pi / 2 + math.pi * i / 18
        pts.append([round(-L_ / 2 + r + r * math.cos(a), 2), round(r * math.sin(a), 2)])
    for i in range(0, 19):
        a = -math.pi / 2 + math.pi * i / 18
        pts.append([round(L_ / 2 - r + r * math.cos(a), 2), round(r * math.sin(a), 2)])
    return pts


def draw_kind(kid, outpath, poly, key='elevation', margin=40):
    el = poly[key]
    xs = [p[0] for p in el]; zs = [p[1] for p in el]
    x0, x1, z0, z1 = min(xs), max(xs), min(zs), max(zs)
    plan = poly.get('plan_outline')
    pw = 0
    if plan:
        pw = (max(p[0] for p in plan) - min(p[0] for p in plan)) + 2 * margin
    W = int((x1 - x0) + 2 * margin + pw + 40)
    H = int((z1 - z0) + 2 * margin + 60)
    im = Image.new('RGB', (W, H), (245, 245, 242))
    d = ImageDraw.Draw(im)
    ox = margin - x0
    oy = H - margin - 30 + z0
    pt = lambda x, z: (ox + x, oy - z)
    for z in range(0, int(z1) + 100, 100):
        d.line([pt(x0 - margin, z), pt(x1 + margin, z)], fill=(210, 210, 215))
        d.text((2, oy - z - 10), str(z), fill=(120, 120, 130))
    d.line([pt(0, z0 - 10), pt(0, z1 + 10)], fill=(200, 160, 160))
    d.polygon([pt(x, z) for x, z in el], fill=FILL.get(kid, (80, 80, 80)), outline=INK)
    if plan:
        cx = ox + x1 + margin + pw / 2.0
        cy = oy - z0 - (max(abs(p[1]) for p in plan))
        d.polygon([(cx + p[0], H - margin - 30 - max(abs(q[1]) for q in plan) + p[1]) for p in plan], fill=FILL.get(kid, (80, 80, 80)), outline=INK)
        if poly.get('bolts_plan'):
            for b in poly['bolts_plan']:
                d.polygon([(cx + p[0], H - margin - 30 - max(abs(q[1]) for q in plan) + p[1]) for p in b], fill=(190, 190, 195), outline=INK)
    d.line([(margin, H - 14), (margin + 100, H - 14)], fill=INK, width=2)
    d.text((margin + 104, H - 20), '100 mm', fill=INK)
    d.text((margin, 4), f'{kid}  H {z1:.0f}  r max {max(abs(x) for x in xs):.0f}', fill=INK)
    im.save(outpath)
    return im


def overlay(preview_dir, out_dir):
    done = []
    for fid, F in (T.get('photo_frames') or {}).items():
        pth = os.path.join(preview_dir, F['file'])
        if not os.path.exists(pth):
            continue
        im = Image.open(pth).convert('RGB')
        d = ImageDraw.Draw(im, 'RGBA')
        prof = T['profiles_final'][fid]
        mm = F['mm_per_px']
        left, right = L.silhouette(prof, F['axis_offset_mm'], F['lean_deg'])
        px = lambda t, z: ((t - F['t_left_mm']) / mm, (F['z_top_mm'] - z) / mm)
        for side in (left, right):
            d.line([px(t, z) for t, z in side], fill=(255, 40, 40, 255), width=1)
        a0, s = F['axis_offset_mm'], math.tan(math.radians(F['lean_deg']))
        H = max(z for r, z in prof)
        d.line([px(a0, 0), px(a0 + s * H, H)], fill=(255, 255, 0, 150), width=1)
        for z in range(0, int(H), 100):
            x = 0
            d.line([(0, px(0, z)[1]), (6, px(0, z)[1])], fill=(0, 255, 255, 255))
            d.text((8, px(0, z)[1] - 5), str(z), fill=(0, 255, 255, 255))
        out = os.path.join(out_dir, F['file'].replace('-elevation.jpg', '-target-on-photo.jpg'))
        im.save(out, quality=88)
        done.append(out)
    return done


def street_plan(outpath, poly):
    mm = 25.0
    x0, x1 = -4000, 52000
    zl, zr = -7500, 7500
    W = int((x1 - x0) / mm); H = int((zr - zl) / mm)
    im = Image.new('RGB', (W, H), (235, 235, 230))
    d = ImageDraw.Draw(im)
    P = lambda x, z: ((x * 1000 - x0) / mm, (z * 1000 - zl) / mm)
    d.rectangle([P(0, -3)[0], P(0, -3)[1], P(48, 3)[0], P(48, 3)[1]], fill=(160, 160, 165))
    for z0_, z1_ in ((3, 5), (-5, -3)):
        d.rectangle([P(0, z0_)[0], P(0, z0_)[1], P(48, z1_)[0], P(48, z1_)[1]], fill=(205, 205, 200))
    col = {'K1': (20, 20, 20), 'K2': (90, 90, 160), 'K3': (150, 100, 40), 'K4': (40, 140, 60), 'K5': (160, 40, 40), 'K6': (0, 0, 0), 'K7': (0, 0, 0)}
    for m in poly['places']:
        cx, cy = P(m['x_m'], m['z_m'])
        r = 100 / mm * 2
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=col.get(m['kind'], (0, 0, 0)))
        d.text((cx - 8, cy - 22), m['kind'], fill=(0, 0, 0))
    d.text((8, 6), 'Quay Street, x 0 to 48 m (south end left), z across; bollards by kind; 25 mm a pixel', fill=(0, 0, 0))
    im.save(outpath)


def main(out_dir, preview_dir=None, overlay_dir=None):
    os.makedirs(out_dir, exist_ok=True)
    poly = polygons()
    json.dump(dict(units='mm (elevation x lateral, z up; plan x, y); places in metres of the street frame', polygons=poly), open(os.path.join(out_dir, 'drawing.json'), 'w'))
    pics = []
    for kid in ('K1', 'K2', 'K3', 'K4', 'K5', 'K6', 'K7'):
        p = os.path.join(out_dir, f'{kid}-elevation-and-plan.png')
        draw_kind(kid, p, poly[kid])
        pics.append(p)
    if 'elevation_K6b' in poly['K6']:
        d = {'elevation': poly['K6']['elevation_K6b'], 'plan_outline': circle(190)}
        p = os.path.join(out_dir, 'K6b-elevation-and-plan.png')
        draw_kind('K6', p, d)
        pics.append(p)
    # sheet
    ims = [Image.open(p) for p in pics]
    Wt = sum(i.width for i in ims) + 10 * len(ims)
    Ht = max(i.height for i in ims)
    sheet = Image.new('RGB', (Wt, Ht), (245, 245, 242))
    x = 0
    for i in ims:
        sheet.paste(i, (x, Ht - i.height)); x += i.width + 10
    sheet.save(os.path.join(out_dir, 'target-drawing-sheet.png'))
    street_plan(os.path.join(out_dir, 'street-plan-bollards.png'), poly)
    if overlay_dir:
        os.makedirs(overlay_dir, exist_ok=True)
        # a reduced sheet for the previews folder: two rows (the street's kinds; the quay's), at most 1200 px wide, a JPEG under 300 KB
        rows = [ims[:4], ims[4:]]
        sc = 1200.0 / max(sum(i.width for i in r) + 10 * len(r) for r in rows)
        rimgs = []
        for r in rows:
            Wr = sum(i.width for i in r) + 10 * len(r); Hr = max(i.height for i in r)
            rs = Image.new('RGB', (Wr, Hr), (245, 245, 242)); xx = 0
            for i in r:
                rs.paste(i, (xx, Hr - i.height)); xx += i.width + 10
            rimgs.append(rs.resize((int(Wr * sc), int(Hr * sc)), Image.LANCZOS))
        Hs = sum(i.height for i in rimgs) + 8
        sheet2 = Image.new('RGB', (1200, Hs), (245, 245, 242)); yy = 0
        for i in rimgs:
            sheet2.paste(i, (0, yy)); yy += i.height + 8
        q = 88
        while True:
            sheet2.save(os.path.join(overlay_dir, 'target-drawing-sheet.jpg'), quality=q, optimize=True)
            if os.path.getsize(os.path.join(overlay_dir, 'target-drawing-sheet.jpg')) < 290000 or q <= 50:
                break
            q -= 6
    outs = overlay(preview_dir, overlay_dir or out_dir) if preview_dir else []
    print('drawing.json,', len(pics), 'kind pictures, a sheet, the street plan,', len(outs), 'overlays ->', out_dir)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(1)
    main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None, sys.argv[3] if len(sys.argv) > 3 else None)
