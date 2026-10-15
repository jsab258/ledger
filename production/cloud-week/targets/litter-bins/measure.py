#!/usr/bin/env python
"""Re-makes photo_measurements.json: everything the litter-bins target measures on a reached picture, with raw rows.

    /home/user/.bpyenv/bin/python -I measure.py [--cache DIR]

Reached sources (all Poly Haven, CC0, read 9 October 2026): the urban_street_02 panorama (Andreas Mischok, taken 2019-08-18),
twelve CC0 material scans (diffuse 1k), the metal_trash_can model (GurJas Studios) and the trashbag model (Benny Weimer).
Measurement only: nothing is placed in the game, traced into a texture or fed to an image model."""
import argparse, json, os, sys, urllib.request
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import litter_lib as L

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))

# US02 camera-height anchors: the same two brick anchors the bollards writer used (its calibrate.py), re-run here on the same pixels.
# (pano, id, cols x0 x1, rows y0 y1, foot row, gauge mm, step to the object's ground (m), what, joint pitch by eye px)
US02_ANCHORS = [
    ('urban_street_02', 'us02_building_wall', 740, 840, 2045, 2192, 2194, 75.0, 0.0, 'building wall behind the K2b bollard, on its footway', 11.75),
    ('urban_street_02', 'us02_gate_pier', 7970, 8000, 2028, 2215, 2226, 75.0, 0.0, 'gate pier at the panorama seam, on the same footway', 14.77),
]
# the grey galvanised steel 1100-litre container on the road beside the kerb (urban_street_02): the view that frames it and the boxes sampled
CONT_VIEW = dict(pano='urban_street_02', yaw=110.0, pitch=-5.0, fov=14.0, w=1400, h=1000)
CONT_FACE_BOX = (640, 60, 1160, 520)        # the flat side face, handles and streaks included (the median is robust to them)
CONT_STREAK_BOX = (640, 100, 720, 480)      # the pale vertical rub streaks on the face's left
CONT_CLEAN_BOX = (880, 330, 1120, 500)      # a plainer patch low on the face
TEXTURES = ['corrugated_iron', 'corrugated_iron_02', 'corrugated_iron_03', 'worn_corrugated_iron', 'green_metal_rust', 'rust_coarse_01',
            'rusty_painted_metal', 'precast_concrete_wall', 'pebble_embedded_concrete', 'painted_metal_shutter', 'worn_shutter', 'container_side']


def fetch(url, dest):
    if not os.path.exists(dest):
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        with open(dest, 'wb') as f:
            f.write(L.http_get(url))
    return dest


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--cache', default=os.path.join(L.CACHE, 'ref')); a = ap.parse_args()
    out = {'date': '2026-10-09', 'note': 'raw rows; self_check.py recomputes each from the pixels / files named'}
    # 1. camera height
    rows = []
    for pano, id_, x0, x1, y0, y1, foot, g, step, what, pxp in US02_ANCHORS:
        p, h_mm, edge = L.horizon_height(pano, x0, x1, y0, y1, foot, g, pxp)
        rows.append(dict(pano=pano, id=id_, cols=[x0, x1], rows=[y0, y1], foot_row=foot, gauge_mm=g, step_m=step, what=what, px_pitch_by_eye=pxp,
                         pitch_tan=round(p, 5), h_above_wall_foot_mm=round(h_mm, 1), fit_on_edge=edge))
    out['horizon_anchors'] = rows
    out['camera_height'] = {'urban_street_02_footway_m': 0.92, 'error_m': 0.04, 'urban_street_02_road_m': 1.04, 'road_error_m': 0.05,
        'rule': 'the footway height is the bollards writer\'s 0.92 +-0.04 (their anchors re-run above give %s mm); the road is the footway height plus the kerb upstand 0.12 +-0.02 (a 125 mm kerb less the footway\'s fall)' % [r['h_above_wall_foot_mm'] for r in rows]}
    # 2. container colours
    cv = CONT_VIEW
    img = L.view(cv['pano'], cv['yaw'], cv['pitch'], cv['fov'], cv['w'], cv['h'])
    out['container'] = dict(view=cv, face_box=list(CONT_FACE_BOX), streak_box=list(CONT_STREAK_BOX), clean_box=list(CONT_CLEAN_BOX),
        face=L.region_colour(img, CONT_FACE_BOX), streak=L.region_colour(img, CONT_STREAK_BOX), clean=L.region_colour(img, CONT_CLEAN_BOX),
        what='urban_street_02: a hot-dip galvanised steel 1,100-litre container on four castors, a rolled top edge, a formed D handle on its end and a pressed bar handle on its long face, vertical pale rub streaks, small shallow dents, no rust visible at 8 m; photographed 18 Aug 2019 (the type is in use before 1990: steel bulk containers of this kind date from the 1970s on, a lead, not a number)')
    # 3. material scans
    tex = {}
    for t in TEXTURES:
        info = L.http_json(f'https://api.polyhaven.com/files/{t}')
        d = info.get('Diffuse') or info.get('diff')
        url = d['1k']['jpg']['url']
        p = fetch(url, os.path.join(a.cache, f'{t}_diff_1k.jpg'))
        arr = np.asarray(Image.open(p).convert('RGB'))
        h, w, _ = arr.shape
        tex[t] = dict(url=url, central_crop=[w // 8, h // 8, 7 * w // 8, 7 * h // 8], **L.region_colour(arr, (w // 8, h // 8, 7 * w // 8, 7 * h // 8)))
    out['textures'] = tex
    # 4. models
    mi = L.http_json('https://api.polyhaven.com/info/metal_trash_can')
    files = L.http_json('https://api.polyhaven.com/files/metal_trash_can')
    g = files['gltf']['1k']['gltf']
    base = os.path.join(a.cache, 'metal_trash_can')
    fetch(g['url'], os.path.join(base, 'metal_trash_can.gltf'))
    for p, v in g['include'].items():
        if p.endswith('.bin'): fetch(v['url'], os.path.join(base, p))
    js, parts = L.read_gltf(os.path.join(base, 'metal_trash_can.gltf'))
    rows = []
    for name, P, T in parts:
        rows.append(dict(node=name, translation=[round(x, 4) for x in T], size_m=[round(x, 4) for x in (P.max(0) - P.min(0))],
                         min_m=[round(x, 4) for x in P.min(0)], max_m=[round(x, 4) for x in P.max(0)], verts=len(P)))
    tb = L.http_json('https://api.polyhaven.com/info/trashbag')
    out['models'] = dict(metal_trash_can=dict(page='https://polyhaven.com/a/metal_trash_can', authors=mi['authors'], licence='CC0', info_dimensions_mm=mi['dimensions'], gltf_1k_parts=rows,
                         note='y up. node metal_trash_can (the clean variant) is the body: 0.906 high, a ribbed cylinder with its ribs in the normal map and a rolled bead; handles and lid separate; 0.55 across: a US-style can, not the British 18-inch dustbin'),
                         trashbag=dict(page='https://polyhaven.com/a/trashbag', authors=tb['authors'], licence='CC0', info_dimensions_mm=tb['dimensions']))
    # 5. the repository's own bins (what the game has today)
    held = {}
    for name, rel in [('litter-bin', 'production/assets/street/clutter/litter-bin.glb'), ('dustbin', 'production/assets/street/clutter/dustbin.glb'),
                      ('grit-bin', 'production/assets/street/clutter/grit-bin.glb'), ('outdoor_bin', 'ledger/Assets/Props/base-mesh/outdoor_bin.glb'),
                      ('swing_bin', 'ledger/Assets/Props/base-mesh/swing_bin.glb')]:
        js, parts = L.read_glb(os.path.join(REPO, rel))
        P = np.vstack([p for _, p, _ in parts])
        held[name] = dict(file=rel, size_m=[round(x, 4) for x in (P.max(0) - P.min(0))], min_m=[round(x, 4) for x in P.min(0)], max_m=[round(x, 4) for x in P.max(0)],
                          materials=[dict(name=m.get('name'), base=[round(c, 4) for c in m.get('pbrMetallicRoughness', {}).get('baseColorFactor', [])], metallic=m.get('pbrMetallicRoughness', {}).get('metallicFactor'), roughness=m.get('pbrMetallicRoughness', {}).get('roughnessFactor')) for _, _, m in parts])
    out['held_bins'] = held
    json.dump(out, open(os.path.join(HERE, 'photo_measurements.json'), 'w'), indent=1)
    print('wrote photo_measurements.json')
    for r in out['horizon_anchors']: print(r['id'], r['h_above_wall_foot_mm'], 'mm', 'FIT ON EDGE' if r['fit_on_edge'] else '')
    print('container face', out['container']['face']['median'], 'streak', out['container']['streak']['median'], 'clean', out['container']['clean']['median'])


if __name__ == '__main__':
    main()
