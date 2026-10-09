#!/usr/bin/env python
"""Makes the previews of the railings family (production/previews/cloud-week/refs/railings/).
    /home/user/.bpyenv/bin/python make_previews.py PANO_DIR
Needs the Poly Haven panoramas.  Every crop is of the object only: the elevation window is cut to the railing, anything else that the brief bars (a notice board with a telephone number,
a boat's name, a distant figure) is painted flat grey; the rest of each picture is the plane's own elevation.  JPEG, at most 1200 px on the long side, under 300 KB.
Photographs: Poly Haven, CC0, Andreas Mischok; the drawings are this target's."""
import sys, os, json, math
import numpy as np
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rail_lib as L
import measure as M
import target_drawing as D
from frames import FRAMES

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
OUT = os.path.join(ROOT, 'production', 'previews', 'cloud-week', 'refs', 'railings')
os.makedirs(OUT, exist_ok=True)
T = D.T


def save_jpeg(im, path, limit=290 * 1024, maxside=1200):
    if max(im.size) > maxside:
        r = maxside / float(max(im.size))
        im = im.resize((int(im.width * r), int(im.height * r)), Image.LANCZOS)
    for q in (88, 84, 80, 76, 72, 68, 62, 56):
        im.save(path, quality=q, optimize=True)
        if os.path.getsize(path) <= limit:
            break
    return os.path.getsize(path), im.size


def elev_image(pano_dir, F, win, mm, masks=()):
    pl = M.plane_of(F)
    e = L.elevation(os.path.join(pano_dir, F['pano'] + '.jpg'), pl, win['s0'], win['s1'], win['z0'], win['z1'], mm, rgb=True)
    im = Image.fromarray(np.clip(e, 0, 255).astype(np.uint8))
    d = ImageDraw.Draw(im)
    for (s0, s1, z0, z1) in masks:
        x0, x1 = (s0 - win['s0']) / mm, (s1 - win['s0']) / mm
        y0, y1 = (win['z1'] - z1) / mm, (win['z1'] - z0) / mm
        d.rectangle([x0, y0, x1, y1], fill=(128, 128, 126))
    return im


def to_px(win, mm):
    return lambda s, z: ((s - win['s0']) / mm, (win['z1'] - z) / mm)


def overlay(im, win, mm, view, color=(255, 40, 40), width=1, extra=None):
    ov = im.copy()
    d = ImageDraw.Draw(ov)
    px = to_px(win, mm)
    for pg in view.polys:
        pts = [px(s, z) for s, z in pg['poly']]
        d.line(pts + [pts[0]], fill=color, width=width)
    # z ticks every 100 in cyan, s ticks every 200 at the top
    for z in range(0, int(win['z1']), 100):
        if z < win['z0']: continue
        x, y = px(win['s0'], z)
        d.line([(0, y), (8, y)], fill=(0, 220, 220))
        if z % 500 == 0: d.text((10, y - 5), str(z), fill=(0, 220, 220))
    if extra: extra(d, px)
    return ov


def street_plan_picture(path):
    """the east footway at the guard rail, 190 px a metre: x 8 to 14, z 2.8 to 5.3 (symbols enlarged where the object is under 10 px)"""
    SF = T['street_frame']
    A_ = T['kinds']['A1']['panel']
    sc = 190.0
    X0, Z0, X1, Z1 = 8.0, 2.8, 14.0, 5.3
    W, H = int((X1 - X0) * sc), int((Z1 - Z0) * sc)
    im = Image.new('RGB', (W + 2, H + 2), (236, 234, 228))
    d = ImageDraw.Draw(im)

    def p(x, z):
        return ((x - X0) * sc, (z - Z0) * sc)

    def R(x0, x1, z0, z1, fill, out=None):
        a, b = p(x0, z0), p(x1, z1)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=fill, outline=out)
    R(X0, X1, Z0, 3.0, (120, 120, 118))
    R(X0, X1, 3.0, SF['kerb_back_kerbs_target_z_m'], (170, 170, 168))
    R(X0, X1, SF['kerb_back_kerbs_target_z_m'], SF['stallriser_face_z_m'], (205, 202, 192))
    R(X0, X1, SF['stallriser_face_z_m'], Z1, (190, 160, 140))
    R(11.78, 12.22, Z0, 3.0, (80, 60, 50))
    pl = T['placements']['street'][0]
    zr = pl['z_axis_m']
    rear = zr + A_['post']['od'] / 2000
    # the walking strip of 0.68 behind the rail, the crates that would break it
    R(pl['x_m'][0], pl['x_m'][1], rear, rear + 0.68, (150, 205, 150))
    R(9.5, 12.5, SF['stallriser_face_z_m'] - 0.92, SF['stallriser_face_z_m'], None, (200, 40, 40))
    d.text(p(9.55, SF['stallriser_face_z_m'] - 0.90), 'crates 0.92 deep: 0.656 left (fails)', fill=(200, 40, 40))
    # the rail and its posts (enlarged: the rail is 42 mm, 8 px here)
    a, b = p(pl['x_m'][0], zr), p(pl['x_m'][1], zr)
    d.line([a, b], fill=(24, 24, 26), width=5)
    for x in pl['x_m']:
        cx, cy = p(x, zr)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(24, 24, 26))
    labs = [(8.1, 2.83, 'carriageway'), (8.1, 3.05, 'kerb 3.000 to 3.170'), (8.1, 3.55, 'footway'), (8.1, 5.0, 'frontage: stallriser face z 4.975'),
            (10.05, zr - 0.13, 'guard rail, axis z 3.375 (0.205 behind the kerb)'), (10.1, 3.62, 'walking strip 0.68 (green): 1.576 m clear behind the rail to z 4.975'), (11.5, 2.83, 'gully x 12.0')]
    for x, z, txt in labs:
        d.text(p(x, z), txt, fill=(30, 30, 30))
    for k in range(0, 7):
        d.text(p(8.0 + k, 5.22), 'x %d' % (8 + k), fill=(30, 30, 30))
    im.save(path)
    return im


def jetty_plan_picture(path):
    """the jetty and the Q2 runs, 28 px a metre: y -52 to -12 across (east right), x -131 to -107 up (north up)"""
    sc = 28.0
    Y0, Y1, X0, X1 = -52.0, -12.0, -131.0, -107.0
    W, H = int((Y1 - Y0) * sc), int((X1 - X0) * sc)
    im = Image.new('RGB', (W, H), (150, 170, 180))
    d = ImageDraw.Draw(im)

    def p(x, y):
        return ((y - Y0) * sc, (X1 - x) * sc)

    def R(x0, x1, y0, y1, fill):
        a, b = p(x1, y0), p(x0, y1)
        d.rectangle([a[0], a[1], b[0], b[1]], fill=fill)
    R(-130.0, -110.0, -100.0, -15.0, (190, 190, 184))
    R(-130.0, -129.4, -100.0, -15.0, (150, 150, 146))
    R(-110.6, -110.0, -100.0, -15.0, (150, 150, 146))
    R(-129.4, -128.6, -100.6, -23.0, (90, 90, 88))
    R(-121.4, -118.6, -20.9, -18.1, (120, 120, 118))
    d.text(p(-119.9, -22.5), 'harbour light (plinth)', fill=(20, 20, 20))
    # K6 bollards and K7 cleats of the bollards target
    for x, y in ((-110.75, -45.0),):
        cx, cy = p(x, y)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=(60, 60, 60))
        d.text((cx + 8, cy - 6), 'K6 bollard (-110.75, -45)', fill=(20, 20, 20))
    for y in (-52.0,):
        cx, cy = p(-110.25, y)
        d.rectangle([cx - 3, cy - 3, cx + 3, cy + 3], fill=(60, 60, 60))
        d.text((cx + 8, cy - 6), 'K7 cleat (-110.25, -52)', fill=(20, 20, 20))
    Pq = T['placements']['quay']
    pts = [tuple(q) for q in Pq[0]['posts_xy_m']] + [tuple(q) for q in Pq[1]['posts_xy_m']]
    for i in range(len(pts) - 1):
        col = (24, 24, 26) if i < 7 else (120, 60, 40)
        d.line([p(*pts[i]), p(*pts[i + 1])], fill=col, width=3)
    for q in pts:
        cx, cy = p(*q)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(24, 24, 26), outline=(255, 255, 255))
    d.text(p(-110.4, -37.0), '(-110.4, -36.4)', fill=(255, 255, 255))
    d.text(p(-114.4, -15.8), '(-128.4, -15.4) tip end', fill=(20, 20, 20))
    d.text((8, 4), 'Q2a two-rail run (black): basin edge x -110.4, 7 bays of 3.0', fill=(255, 255, 255))
    d.text((8, 18), 'Q2b rail-and-chain run (brown): tip y -15.4, 6 bays of 3.0', fill=(255, 255, 255))
    d.text((8, 32), 'cope nose x -110 (basin edge) and y -15 (tip); rail line 0.4 behind it', fill=(255, 255, 255))
    d.text((8, H - 16), 'seaward parapet (dark) ends at y -23.0; the corner beyond it stays open', fill=(20, 20, 20))
    im.save(path)
    return im


def main(pano_dir):
    sizes = {}
    # ---------------------------------------------------------------- R3B, the main photograph
    F = FRAMES['R3B']
    pv = F['preview']
    im = elev_image(pano_dir, F, pv, pv['mm'], F['mask'])
    sizes['ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg'] = save_jpeg(im, os.path.join(OUT, 'ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg'))
    view = D.r3b_view(pv['s0'], pv['s1'], pv['z0'], pv['z1'])
    ov = overlay(im, pv, pv['mm'], view)
    sizes['ph-bethnal_green_entrance-r3b-park-railing-target-on-photo.jpg'] = save_jpeg(ov, os.path.join(OUT, 'ph-bethnal_green_entrance-r3b-park-railing-target-on-photo.jpg'))
    # 1 mm closes of the head and of the foot (the hinge post and its pier)
    for nm, win in (('head-close', dict(s0=2300, s1=3100, z0=1700, z1=2450)), ('foot-close', dict(s0=2300, s1=3100, z0=-50, z1=800))):
        c = elev_image(pano_dir, F, win, 1, ())
        sizes['ph-bethnal_green_entrance-r3b-park-railing-%s.jpg' % nm] = save_jpeg(c, os.path.join(OUT, 'ph-bethnal_green_entrance-r3b-park-railing-%s.jpg' % nm))
    # ---------------------------------------------------------------- R3A
    F = FRAMES['R3A']
    pv = F['preview']
    im = elev_image(pano_dir, F, pv, pv['mm'], F['mask'])
    sizes['ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg'] = save_jpeg(im, os.path.join(OUT, 'ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg'))
    view = D.r3a_view()
    sizes['ph-bethnal_green_entrance-r3a-area-railing-target-on-photo.jpg'] = save_jpeg(overlay(im, pv, pv['mm'], view), os.path.join(OUT, 'ph-bethnal_green_entrance-r3a-area-railing-target-on-photo.jpg'))
    # ---------------------------------------------------------------- R3D
    F = FRAMES['R3D']
    pv = F['preview']
    im = elev_image(pano_dir, F, pv, pv['mm'], F['mask'])
    sizes['ph-urban_street_01-r3d-garden-railing-elevation.jpg'] = save_jpeg(im, os.path.join(OUT, 'ph-urban_street_01-r3d-garden-railing-elevation.jpg'))
    view = D.r3d_view()
    sizes['ph-urban_street_01-r3d-garden-railing-target-on-photo.jpg'] = save_jpeg(overlay(im, pv, pv['mm'], view), os.path.join(OUT, 'ph-urban_street_01-r3d-garden-railing-target-on-photo.jpg'))
    # ---------------------------------------------------------------- LHB, the chain bay
    F = FRAMES['LHB']
    pv = F['preview']
    masks = list(F['mask']) + [[1400, 1800, 950, 1250]]
    im = elev_image(pano_dir, F, pv, pv['mm'], masks)
    # the embossed mark on the left post's flange: blur it (the bollards target leaves it blank)
    d = ImageDraw.Draw(im)
    px = to_px(pv, pv['mm'])
    sizes['ph-limehouse-lhb-chain-bay-elevation.jpg'] = save_jpeg(im, os.path.join(OUT, 'ph-limehouse-lhb-chain-bay-elevation.jpg'))
    HRL = T['photo_measurements']['hand_reads']['LHB']
    span = HRL['span_mm']['v']
    sag = T['kinds']['Q2']['chain']['sag']

    def extra(d, px):
        # the target's chain: eyes at the measured lug heights 800 and 405, the target's sag 200 below the eyes
        for key, zlug, col in (('upper', HRL['upper_lug_z']['v'], (255, 40, 40)), ('lower', HRL['lower_lug_z']['v'], (255, 40, 40))):
            pts, a = D.catenary_pts(0.0, span, float(zlug), sag, 80)
            d.line([px(x, z) for x, z in pts], fill=col, width=1)
        for key, zlow, col in (('upper', HRL['upper_chain_lowest_z']['v'], (255, 220, 0)), ('lower', HRL['lower_chain_lowest_z']['v'], (255, 220, 0))):
            x, y = px(span / 2.0, zlow)
            d.line([(x - 14, y), (x + 14, y)], fill=col, width=1)
        # the post tops
        for s in (0.0, span):
            x, y = px(s, HRL['post_top_z']['v'])
            d.line([(x - 20, y), (x + 20, y)], fill=(255, 40, 40), width=1)
    ov = overlay(im, pv, pv['mm'], D.View('none', '', [0, 0, 0, 0]), extra=extra)
    sizes['ph-limehouse-lhb-chain-bay-target-on-photo.jpg'] = save_jpeg(ov, os.path.join(OUT, 'ph-limehouse-lhb-chain-bay-target-on-photo.jpg'))
    # ---------------------------------------------------------------- the drawings
    import tempfile
    tmp = tempfile.mkdtemp(prefix='railings_draw_')
    pics = {}
    for v in D.all_views():
        D.draw(v, os.path.join(tmp, v.name + '.png'))
        pics[v.name] = Image.open(os.path.join(tmp, v.name + '.png')).convert('RGB')

    def fit(im, w):
        return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    rows = [fit(pics['A1_elevation'], 1100), fit(pics['Q2a_elevation'], 1100), fit(pics['Q2b_elevation'], 1100)]
    H = sum(r.height for r in rows) + 10 * len(rows)
    sheet = Image.new('RGB', (1100, H), (255, 255, 255))
    y = 0
    dd = ImageDraw.Draw(sheet)
    for r, lab in zip(rows, ('A1 guard rail panel (2000 between posts, 1000 high; each view fitted to the sheet\'s width, not one scale)', 'Q2a two-rail bay (3000)', 'Q2b rail and chain bay (3000, sag 200)')):
        sheet.paste(r, (0, y))
        dd.text((8, y + 4), lab, fill=(180, 30, 30))
        y += r.height + 10
    sizes['target-drawing-sheet.jpg'] = save_jpeg(sheet, os.path.join(OUT, 'target-drawing-sheet.jpg'))
    sizes['target-plan-street.jpg'] = save_jpeg(street_plan_picture(os.path.join(tmp, 'street_plan_sym.png')).convert('RGB'), os.path.join(OUT, 'target-plan-street.jpg'))
    sizes['target-plan-jetty.jpg'] = save_jpeg(jetty_plan_picture(os.path.join(tmp, 'jetty_plan_sym.png')).convert('RGB'), os.path.join(OUT, 'target-plan-jetty.jpg'))
    # A1 beside the photographed railings at one scale (0.5 px a mm): R3B (bars 78.5), R3D (94.5), A1 (115.5), each 1000 wide, 900 high from z 100
    panels = []
    for fid, s0, labtxt in (('R3B', 1000, 'R3B park railing: bar pitch 78.5'), ('R3D', 1300, 'R3D garden railing: bar pitch 94.5')):
        F_ = FRAMES[fid]
        win = dict(s0=s0, s1=s0 + 1000, z0=100 if fid == 'R3B' else 560, z1=1000 if fid == 'R3B' else 1460)
        pim = elev_image(pano_dir, F_, win, 2, F_['mask'] if fid == 'R3B' else ())
        panels.append((pim, labtxt))
    a1v = D.a1_views()[0]
    a1v.bounds = [-500, 500, 100, 1000]
    D.draw(a1v, os.path.join(tmp, 'A1_crop.png'), scale=0.5, margin=0)
    panels.append((Image.open(os.path.join(tmp, 'A1_crop.png')).convert('RGB'), 'A1 guard rail: bar pitch 109.1'))
    Wp = sum(p.width for p, _ in panels) + 10 * (len(panels) - 1)
    Hp = max(p.height for p, _ in panels)
    comp = Image.new('RGB', (Wp, Hp + 16), (255, 255, 255))
    x = 0
    dd2 = ImageDraw.Draw(comp)
    for p, lab in panels:
        comp.paste(p, (x, 16))
        dd2.text((x + 4, 2), lab, fill=(180, 30, 30))
        x += p.width + 10
    sizes['target-a1-beside-photographed-bars.jpg'] = save_jpeg(comp, os.path.join(OUT, 'target-a1-beside-photographed-bars.jpg'))
    json.dump({k: dict(bytes=v[0], px=list(v[1])) for k, v in sizes.items()}, open(os.path.join(HERE, 'previews_made.json'), 'w'), indent=1)
    for k, v in sizes.items():
        print(k, v)


if __name__ == '__main__':
    main(sys.argv[1])
