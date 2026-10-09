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
    WS = T['street_fixtures']['walking_strip']
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
    rear = WS['rear_face_z_m']
    # the awning of the fish market (outline) over the strip
    aw = WS['awning']
    R(aw['x_m'][0], aw['x_m'][1], aw['z_m'][0], aw['z_m'][1], None, (190, 120, 90))
    # the walking strip of 0.68 behind the rail, and the free width to the stallriser
    R(WS['x_range_m'][0], WS['x_range_m'][1], rear, SF['stallriser_face_z_m'], (205, 232, 205))
    R(pl['x_m'][0], pl['x_m'][1], rear, rear + 0.68, (150, 205, 150))
    R(WS['x_range_m'][0], WS['x_range_m'][1], SF['stallriser_face_z_m'] - 0.92, SF['stallriser_face_z_m'], None, (200, 40, 40))
    d.text(p(9.55, SF['stallriser_face_z_m'] - 0.90), 'crates 0.92 deep: 0.655 left (fails)', fill=(200, 40, 40))
    # the reinstatement patches (ragged, local y + toward the carriageway = street -z)
    for x in pl['x_m']:
        d.polygon([p(x + a / 1000.0, zr - b / 1000.0) for a, b in T['kinds']['A1']['ground']['patch']['outline_xy']], fill=(45, 43, 41))
    # the rail: top rail 50 across (9.5 px here), posts 50 x 30, the nuts on the posts' outer faces
    R(pl['x_m'][0] + (A_['top_rail']['x'][0] - A_['post']['x'][0]) / 1000.0, pl['x_m'][1] + (A_['top_rail']['x'][1] - A_['post']['x'][1]) / 1000.0, zr - 0.025, zr + 0.025, (150, 150, 152))
    for x in pl['x_m']:
        R(x - 0.025, x + 0.025, zr - 0.015, zr + 0.015, (118, 120, 122), (24, 24, 26))
        sgn = -1 if x == pl['x_m'][0] else 1
        R(min(x + sgn * 0.025, x + sgn * 0.033), max(x + sgn * 0.025, x + sgn * 0.033), zr - 0.0085, zr + 0.0085, (60, 60, 60))
    labs = [(8.1, 2.83, 'carriageway'), (8.1, 3.05, 'kerb 3.000 to 3.170'), (8.1, 3.8, 'footway'), (8.1, 5.0, 'frontage: stallriser face z 4.975'),
            (10.22, zr - 0.15, 'guard rail: axis z 3.375, rear face 3.400'), (9.6, 4.35, 'walking strip, 0 to 2.0 m high: 1.575 m clear at the ground, 1.39 m under the awning at a 2.0 m head (green)'),
            (12.45, 4.45, 'fish market awning (outline)'), (11.5, 2.83, 'gully x 12.0'), (12.2, 3.3, 'dark tarmac patches')]
    for x, z, txt in labs:
        d.text(p(x, z), txt, fill=(30, 30, 30))
    for k in range(0, 7):
        d.text(p(8.0 + k, 5.22), 'x %d' % (8 + k), fill=(30, 30, 30))
    im.save(path)
    return im


def jetty_plan_picture(path):
    """the jetty and the three Q2 runs, 14 px a metre: y -84 to -12 across (east right), x -131 to -107 up (north up); the rings, bollards and posts enlarged"""
    sc = 14.0
    Y0, Y1, X0, X1 = -84.0, -12.0, -131.0, -107.0
    W, H = int((Y1 - Y0) * sc), int((X1 - X0) * sc)
    im = Image.new('RGB', (W, H), (150, 170, 180))
    d = ImageDraw.Draw(im)
    ink = (20, 20, 20)
    org = (180, 80, 0)

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
    d.text((760, 170), 'harbour light plinth', fill=ink)
    # K6 bollards and K7 cleats of the bollards target
    for x, y in ((-110.75, -45.0), (-110.75, -80.0)):
        cx, cy = p(x, y)
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(60, 60, 60))
        d.text((cx - 20, cy + 10), 'K6 bollard', fill=ink)
    for y in (-52.0, -58.0, -64.0):
        cx, cy = p(-110.25, y)
        d.rectangle([cx - 2, cy - 2, cx + 2, cy + 2], fill=(60, 60, 60))
    d.text((p(-110.25, -64.0)[0] + 8, 58), 'K7 cleats (y -64, -58, -52)', fill=ink)
    # the kit's two mooring rings on the basin face (orange rings), labelled over the water
    rings = T['street_fixtures']['kit_rings_jetty_m']
    for (x, y) in rings:
        cx, cy = p(x, y)
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], outline=(230, 120, 20), width=3)
        d.text((cx - 90, 22), 'kit mooring ring (-110, %d)' % y, fill=org)
    # the runs
    for b in T['placements']['bays_detail']:
        col = (24, 24, 26) if b['model'] == 'Q2a' else (120, 60, 40)
        d.line([p(*b['a']), p(*b['b'])], fill=col, width=3)
    seen = set()
    for run in T['placements']['quay'][:3]:
        for q in run['posts_xy_m']:
            if tuple(q) in seen: continue
            seen.add(tuple(q))
            cx, cy = p(*q)
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(24, 24, 26), outline=(255, 255, 255))
    # the clearance from the nearer ring to the first post of the basin run
    a_, b_ = p(*rings[1]), p(-110.4, -21.4)
    d.line([a_, b_], fill=(230, 120, 20), width=1)
    d.text((a_[0] + 150, 22), '10.6 m clear', fill=org)
    d.text((790, 56), 'Q2a basin run (2 bays)', fill=ink)
    d.text((780, 112), 'Q2b tip run: 6 bays', fill=ink)
    d.text((640, 268), 'Q2b return along x -128.4: 3 bays 3.0, 3.0, 1.4', fill=ink)
    d.text((330, 284), 'seaward parapet (dark) ends at y -23.0', fill=ink)
    d.text((20, 120), '12 posts, 11 bays, 31.4 m of railing: black = Q2a two rails, brown = Q2b rail and chain', fill=ink)
    d.text((20, 136), 'the berth (y -100 to -23) stays open: no post or rail within 4.0 m of a ring', fill=ink)
    d.text((20, 152), 'cope nose x -110 (basin edge) and y -15 (tip); the rail line is 0.4 behind it', fill=ink)
    d.text((20, 168), 'posts, rings and bollards are enlarged', fill=ink)
    im.save(path)
    return im


def annotate_drawing(view, path, notes, scale):
    """the drawing script's picture of one view at a scale, with notes in pixels from the top left"""
    D.draw(view, path, scale=scale, margin=20)
    im = Image.open(path).convert('RGB')
    d = ImageDraw.Draw(im)
    for (x, y, txt) in notes:
        d.text((x, y), txt, fill=(180, 30, 30))
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
    # 1 mm closes of the head and of the foot (the hinge post and its pier), at the frames' own windows
    for nm, key in (('head-close', 'head_close'), ('foot-close', 'foot_close')):
        win = F[key]
        c = elev_image(pano_dir, F, win, win['mm'], ())
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
    sc_ = F['h_cam'] / 1.12                                   # the first version's masks, in the first version's frame, scaled to this one and widened by 15 mm
    masks = [[s0 * sc_ - 15, s1 * sc_ + 15, z0 * sc_ - 15, z1 * sc_ + 15] for (s0, s1, z0, z1) in (list(F['mask']) + [[1400, 1800, 950, 1250]])]
    im = elev_image(pano_dir, F, pv, pv['mm'], masks)
    sizes['ph-limehouse-lhb-chain-bay-elevation.jpg'] = save_jpeg(im, os.path.join(OUT, 'ph-limehouse-lhb-chain-bay-elevation.jpg'))
    HRL = T['photo_measurements']['hand_reads']['LHB']
    span = HRL['span_mm']['v']
    sag = T['kinds']['Q2']['chain']['sag']

    def extra(d, px):
        # the target's chain: eyes at the measured lug heights, the target's sag 200 below the eyes
        for key, zlug, col in (('upper', HRL['upper_lug_z']['v'], (255, 40, 40)), ('lower', HRL['lower_lug_z']['v'], (255, 40, 40))):
            pts, a = D.catenary_pts(0.0, span, float(zlug), sag, 80)
            d.line([px(x, z) for x, z in pts], fill=col, width=1)
        for key, zlow, col in (('upper', HRL['upper_chain_lowest_z']['v'], (255, 220, 0)), ('lower', HRL['lower_chain_lowest_z']['v'], (255, 220, 0))):
            x, y = px(span / 2.0, zlow)
            d.line([(x - 14, y), (x + 14, y)], fill=col, width=1)
        for s in (0.0, span):
            x, y = px(s, HRL['post_top_z']['v'])
            d.line([(x - 20, y), (x + 20, y)], fill=(255, 40, 40), width=1)
    ov = overlay(im, pv, pv['mm'], D.View('none', '', [0, 0, 0, 0]), extra=extra)
    sizes['ph-limehouse-lhb-chain-bay-target-on-photo.jpg'] = save_jpeg(ov, os.path.join(OUT, 'ph-limehouse-lhb-chain-bay-target-on-photo.jpg'))
    # ---------------------------------------------------------------- the drawings
    import tempfile
    tmp = tempfile.mkdtemp(prefix='railings_draw_')
    pics = {}
    views = {v.name: v for v in D.all_views()}
    for v in views.values():
        D.draw(v, os.path.join(tmp, v.name + '.png'))
        pics[v.name] = Image.open(os.path.join(tmp, v.name + '.png')).convert('RGB')

    def fit(im, w):
        return im.resize((w, int(im.height * w / im.width)), Image.LANCZOS)
    rows = [fit(pics['A1_elevation'], 1100), fit(pics['Q2a_elevation'], 1100), fit(pics['Q2b_elevation'], 1100)]
    labs = ('A1 guard rail panel: RHS posts 50 x 30 to 1030, top rail 50 x 30 flat (top 1000), bottom rail 40 x 20, 17 bars of 12, four studs (each view fitted to the sheet\'s width, not one scale)',
            'Q2a two-rail bay (3000): post 76.1, top rail 60.3, low rail 42.4', 'Q2b rail and chain bay (3000, sag 200): ears on the sides facing this bay')
    H = sum(r.height for r in rows) + 10 * len(rows)
    sheet = Image.new('RGB', (1100, H), (255, 255, 255))
    y = 0
    dd = ImageDraw.Draw(sheet)
    for r, lab in zip(rows, labs):
        sheet.paste(r, (0, y))
        dd.text((8, y + 4), lab, fill=(180, 30, 30))
        y += r.height + 10
    sizes['target-drawing-sheet.jpg'] = save_jpeg(sheet, os.path.join(OUT, 'target-drawing-sheet.jpg'))
    # the bolt section at 5 px a mm and the walking strip section
    bs = annotate_drawing(views['A1_bolt_section'], os.path.join(tmp, 'bolt.png'), [], 5.0)
    d_ = ImageDraw.Draw(bs)
    d_.text((8, 4), 'A1: plan section along the top rail\'s stud axis (z 985), right-hand end, 5 px a mm', fill=(180, 30, 30))
    d_.text((8, 18), 'rail end (grey) with its 6 mm end plate; M10 stud 61 long welded to the plate\'s outer face (3 mm root fillet), through the post to x 1036; nut 17 x 8 on the post\'s OUTER face, 3 mm thread', fill=(180, 30, 30))
    d_.text((8, bs.height - 16), 'post 50 x 30 x 3 (hollow), face x 975 to 1025; nut x 1025 to 1033; thread to 1036', fill=(180, 30, 30))
    sizes['target-a1-bolt-section.jpg'] = save_jpeg(bs, os.path.join(OUT, 'target-a1-bolt-section.jpg'))
    ws = Image.open(os.path.join(tmp, 'A1_walking_section.png')).convert('RGB')
    ws = ws.resize((int(ws.width * 1100.0 / ws.height), 1100), Image.LANCZOS)
    d_ = ImageDraw.Draw(ws)
    d_.text((8, 4), 'A1: section across the footway at x 10.5 to 12.5 (z across, y up): the rail, the stallriser face z 4.975, the fish market\'s awning', fill=(180, 30, 30))
    d_.text((8, 18), 'strip behind the rail from the rear face z 3.400: 1.575 m clear at the ground, 1.39 m at a 2.0 m head under the awning body (outline: the 0.68 m a person needs)', fill=(180, 30, 30))
    sizes['target-a1-walking-section.jpg'] = save_jpeg(ws, os.path.join(OUT, 'target-a1-walking-section.jpg'))
    sizes['target-plan-street.jpg'] = save_jpeg(street_plan_picture(os.path.join(tmp, 'street_plan_sym.png')).convert('RGB'), os.path.join(OUT, 'target-plan-street.jpg'))
    sizes['target-plan-jetty.jpg'] = save_jpeg(jetty_plan_picture(os.path.join(tmp, 'jetty_plan_sym.png')).convert('RGB'), os.path.join(OUT, 'target-plan-jetty.jpg'))
    # A1 beside the photographed railings at one scale (0.5 px a mm): R3B (bars 76.6), R3D (95.3), A1 (109.1), each 1000 wide, 900 high from z 100
    panels = []
    for fid, s0, labtxt in (('R3B', 1000, 'R3B park railing: bar pitch 76.6'), ('R3D', 1300, 'R3D garden railing: bar pitch 95.3')):
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
