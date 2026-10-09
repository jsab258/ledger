#!/usr/bin/env python
"""Draws the litter-bins target FROM target.json ALONE: elevations, plans and sections as filled polygons in millimetres (a JSON file) and as
pictures at 1 mm a pixel (a folder). Nothing here reads litter_data.py.

    /home/user/.bpyenv/bin/python -I target_drawing.py [--target target.json] [--json drawing.json] [--out DIR]

Views (y is up in an elevation or section, along the street in a plan): K1_front (from the building side: the letters), K1_side, K1_plan, K1_section;
K2_front (from the aperture), K2_plan, K2_section; D1_side, D1_front, D1_plan, D1_section; street_plan (20 mm a pixel); scale_sheet.
Section and elevation polygons are shapely-valid; self_check.py re-runs this module and measures the polygons."""
import argparse, json, math, os, sys
import numpy as np
from shapely.geometry import Polygon, LineString, box, Point, MultiPolygon
from shapely.ops import unary_union
from shapely import affinity

HERE = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------------------------------------------------------------------ geometry helpers
def silhouette(profile, x0=0.0, top_index=None):
    """filled outline of a lathe profile seen from the side: right = profile, left = its mirror; the axis offset x0; top_index closes an open top"""
    P = [tuple(p) for p in profile]
    if top_index is not None:
        P = P[:top_index + 1]
        if P[-1][0] > 0:
            P.append((0.0, P[-1][1]))
    if P[0][0] > 0:
        P = [(0.0, P[0][1])] + P
    if P[-1][0] > 0:
        P.append((0.0, P[-1][1]))
    right = [(x0 + r, z) for r, z in P]
    left = [(x0 - r, z) for r, z in reversed(P)]
    poly = Polygon(right + left)
    if not poly.is_valid:
        poly = poly.buffer(0)
    return poly


def r_of_z(profile, z, side='outer'):
    """outer radius of the silhouette at height z (the largest r whose segment spans z)"""
    best = 0.0
    P = profile
    for (r0, z0), (r1, z1) in zip(P[:-1], P[1:]):
        if min(z0, z1) <= z <= max(z0, z1) and z0 != z1:
            t = (z - z0) / (z1 - z0)
            best = max(best, r0 + t * (r1 - r0))
    return best


def sheet_band(profile, t, inward_of=None, mirror_x0=0.0, top_index=None):
    """the sheet of a lathe: a band of thickness t along the outline path, kept inside the silhouette (so t lies INWARD of the outer surface)"""
    path = LineString(profile if top_index is None else profile[:top_index + 1])
    band = path.buffer(t, cap_style=2, join_style=2)
    if inward_of is not None:
        band = band.intersection(inward_of)
    return band


def mirror_half(poly_right, x0=0.0):
    """a polygon drawn in (r, z) with r >= 0 -> the right half at x0 + r and the left at x0 - r (two polygons)"""
    return [affinity.translate(poly_right, xoff=x0), affinity.translate(affinity.scale(poly_right, xfact=-1, yfact=1, origin=(0, 0)), xoff=x0)]


def rounded_rect(cx, cy, w, h, r, n=8):
    pts = []
    for (ox, oy, a0) in [(w / 2 - r, h / 2 - r, 0), (-(w / 2 - r), h / 2 - r, 90), (-(w / 2 - r), -(h / 2 - r), 180), (w / 2 - r, -(h / 2 - r), 270)]:
        for k in range(n + 1):
            a = math.radians(a0 + 90 * k / n)
            pts.append((cx + ox + r * math.cos(a), cy + oy + r * math.sin(a)))
    return Polygon(pts)


def circle(cx, cy, r, n=96):
    return Point(cx, cy).buffer(r, quad_segs=n // 4)


def ring(cx, cy, r_in, r_out, n=96):
    return circle(cx, cy, r_out, n).difference(circle(cx, cy, r_in, n))


def loop_handle_side(r_body, proud, z0, z1, strap_t, w):
    """a D strap handle seen in profile (y horizontal): an outline frame from the wall out to proud and back"""
    outer = box(r_body - 1.0, z0, r_body + proud, z1)
    inner = box(r_body - 1.0, z0 + strap_t, r_body + proud - strap_t, z1 - strap_t)
    return outer.difference(inner)


def poly_pts(p):
    if p.is_empty:
        return []
    if isinstance(p, (MultiPolygon,)) or p.geom_type in ('MultiPolygon', 'GeometryCollection'):
        out = []
        for g in p.geoms:
            if g.geom_type == 'Polygon':
                out.append([[round(x, 3), round(y, 3)] for x, y in g.exterior.coords])
        return out
    return [[[round(x, 3), round(y, 3)] for x, y in p.exterior.coords]]


class View:
    def __init__(self, title, axes, scale_mm_per_px=1.0, note=''):
        self.title = title; self.axes = axes; self.polys = []; self.scale = scale_mm_per_px; self.note = note; self.lines = []; self.labels = []

    def add(self, name, part, material, geom, hole=False, edge=True):
        if geom is None or geom.is_empty:
            return
        self.polys.append(dict(name=name, part=part, material=material, geom=geom, edge=edge))

    def to_json(self):
        pj = []
        for p in self.polys:
            for pts in poly_pts(p['geom']):
                pj.append(dict(name=p['name'], part=p['part'], material=p['material'], points=pts))
        return dict(title=self.title, axes=self.axes, mm_per_px=self.scale, note=self.note, polygons=pj,
                    lines=[dict(name=n, points=[[round(a, 2), round(b, 2)] for a, b in pts]) for n, pts in self.lines], labels=self.labels)

    def bounds(self):
        g = unary_union([p['geom'] for p in self.polys])
        return g.bounds


# ------------------------------------------------------------------------------------------------------------------------------ the views
def k1_views(T):
    K = T['kinds']['K1']; post = K['post']; bn = K['bin']; br = K['bracket']
    x0 = bn['axis_offset_x']; prof = bn['outer_profile_rz']
    top = 8                                  # the rim bead's crown index in outer_profile_rz (checked by self_check)
    rp = post['od'] / 2
    # --- front from the building side (looking along -y): x to the right = from the post toward the bin
    v = View('K1 pole-mounted open bin, from the footway side (the letters face you)', ['x (mm) from the post axis', 'z (mm) above the flag top'])
    post_sil = silhouette(post['profile_rz'])
    v.add('post', 'post', 'paint_green_worn', post_sil)
    bin_sil = silhouette(prof, x0, top_index=top)
    v.add('bin', 'bin', 'paint_green_worn', bin_sil)
    s = br['back_strap']
    v.add('back_strap', 'bracket', 'paint_green_worn', box(s['x_from'], s['z0'], s['x_to'] + 0.0, s['z1']))
    for i, c in enumerate(br['clamps']):
        v.add(f'clamp_{i + 1}', 'bracket', 'paint_green_worn', box(-(rp + c['ring_t']), c['z0'], rp + c['ring_t'], c['z1']))
        v.add(f'clamp_ear_{i + 1}', 'bracket', 'paint_green_worn', box(-(rp + c['ring_t']) - 12, (c['z0'] + c['z1']) / 2 - 8, -(rp + c['ring_t']), (c['z0'] + c['z1']) / 2 + 8))
        v.add(f'bolt_head_{i + 1}', 'fixing', 'zinc_new', box(-(rp + c['ring_t']) - 20, (c['z0'] + c['z1']) / 2 - 6.5, -(rp + c['ring_t']) - 12, (c['z0'] + c['z1']) / 2 + 6.5))
    L = K['lettering']
    r_at = r_of_z(prof, L['z_centre'])
    chord = 2 * r_at * math.sin(math.radians(L['arc_deg'] / 2))
    v.add('lettering_LITTER', 'lettering', 'letters_cream', box(x0 - chord / 2, L['z_centre'] - L['cap_height'] / 2, x0 + chord / 2, L['z_centre'] + L['cap_height'] / 2), edge=False)
    stn = K['asset_stencil']
    v.add('asset_stencil', 'lettering', 'letters_cream_worn', box(-18, stn['z'] - stn['cap_height'] / 2, 18, stn['z'] + stn['cap_height'] / 2), edge=False)
    out = {'K1_front': v}
    # --- side (looking along x from the bin toward the post): y horizontal
    v = View('K1 from the end (looking along x)', ['y (mm) across', 'z (mm)'])
    v.add('post', 'post', 'paint_green_worn', silhouette(post['profile_rz']))
    v.add('bin', 'bin', 'paint_green_worn', silhouette(prof, 0.0, top_index=top))
    for i, c in enumerate(br['clamps']):
        v.add(f'clamp_{i + 1}', 'bracket', 'paint_green_worn', box(-(rp + c['ring_t']), c['z0'], rp + c['ring_t'], c['z1']))
    out['K1_side'] = v
    # --- plan
    v = View('K1 plan (x right, y up the page)', ['x (mm)', 'y (mm)'])
    v.add('bin_outer', 'bin', 'paint_green_worn', circle(x0, 0, bn['rim_bead']['centre_r'] + bn['rim_bead']['diameter'] / 2))
    v.add('bin_inner_mouth', 'bin', 'bin_sack_black', circle(x0, 0, bn['r_top'] - bn['wall'] - 1.0))
    v.add('post', 'post', 'paint_green_worn', circle(0, 0, rp))
    for i, c in enumerate(br['clamps'][:1]):
        v.add('clamp_ring', 'bracket', 'paint_green_worn', ring(0, 0, rp, rp + c['ring_t']))
    v.add('back_strap', 'bracket', 'paint_green_worn', box(rp, -s['width'] / 2, rp + s['thickness'], s['width'] / 2))
    dh = bn['base_plate']['drain_holes']
    for k in range(dh['count']):
        a = math.radians(dh['first_azimuth'] + 360.0 / dh['count'] * k)
        v.add(f'drain_hole_{k + 1}', 'bin', 'bin_sack_black', circle(x0 + dh['on_radius'] * math.cos(a), dh['on_radius'] * math.sin(a), dh['diameter'] / 2, 16))
    out['K1_plan'] = v
    # --- section through the post and bin axes (x, z)
    v = View('K1 section on the plane of the post and bin axes', ['x (mm)', 'z (mm)'])
    wall = Polygon(bn['wall_section_rz']).buffer(0)
    for g in mirror_half(wall, x0):
        v.add('bin_wall_and_floor', 'bin', 'paint_green_worn', g)
    tube = box(-rp, 0, rp, 1230).difference(box(-rp + post['wall'], -1, rp - post['wall'], 1231))
    v.add('post_tube', 'post', 'paint_green_worn', tube)
    cap = Polygon([(-r, z) for r, z in reversed(post['profile_rz'][4:])] + [(r, z) for r, z in post['profile_rz'][4:]])
    v.add('post_cap', 'post', 'paint_green_worn', cap.buffer(0))
    v.add('back_strap', 'bracket', 'paint_green_worn', box(s['x_from'], s['z0'], s['x_to'], s['z1']))
    for i, c in enumerate(br['clamps']):
        v.add(f'clamp_{i + 1}_left', 'bracket', 'paint_green_worn', box(-(rp + c['ring_t']), c['z0'], -rp, c['z1']))
        v.add(f'clamp_{i + 1}_right', 'bracket', 'paint_green_worn', box(rp, c['z0'], rp + c['ring_t'], c['z1']))
    out['K1_section'] = v
    return out


def k2_views(T):
    K = T['kinds']['K2']; prof = K['outer_profile_rz']; ap = K['aperture']; t = K['shell']
    v = View('K2 hooded drum bin, from the aperture (looking along -x)', ['y (mm) across', 'z (mm)'])
    sil = silhouette(prof)
    v.add('body_and_hood', 'shell', 'gel_green_chalk', sil)
    hole = rounded_rect(0, (ap['sill_z'] + ap['top_z']) / 2, ap['width'], ap['height'], ap['corner_r'])
    v.add('aperture_void', 'aperture', 'bin_sack_black', hole)
    liner_rim = box(-ap['width'] / 2 + ap['corner_r'], K['parts']['liner']['rim_z'][0], ap['width'] / 2 - ap['corner_r'], K['parts']['liner']['rim_z'][1])
    v.add('liner_rim_seen', 'liner', 'zinc_weathered', liner_rim.intersection(hole))
    L = K['lettering']
    r_at = r_of_z(prof, L['z_centre'])
    chord = 2 * r_at * math.sin(math.radians(L['arc_deg'] / 2))
    v.add('lettering_LITTER', 'lettering', 'letters_cream', box(-chord / 2, L['z_centre'] - L['cap_height'] / 2, chord / 2, L['z_centre'] + L['cap_height'] / 2), edge=False)
    v.add('join_groove', 'moulding', 'bin_sack_black', box(-r_of_z(prof, 582.0), K['parts']['join_groove']['z'][0] + 2, r_of_z(prof, 582.0), K['parts']['join_groove']['z'][1] - 4), edge=False)
    out = {'K2_front': v}
    # plan
    v = View('K2 plan (x right toward the aperture)', ['x (mm)', 'y (mm)'])
    v.add('hood', 'shell', 'gel_green_chalk', circle(0, 0, 250.0))
    v.add('body_max', 'shell', 'gel_green_fresh', ring(0, 0, 236.0, 237.0))
    v.add('foot', 'shell', 'gel_green_fresh', ring(0, 0, 210.0, 211.0))
    v.add('liner', 'liner', 'zinc_weathered', ring(0, 0, 186.0, 194.0))
    v.add('aperture', 'aperture', 'bin_sack_black', box(236, -ap['width'] / 2, 252, ap['width'] / 2))
    v.add('lock', 'fixing', 'zinc_new', circle(-250.0, 0, K['parts']['lock']['escutcheon_d'] / 2, 24))
    out['K2_plan'] = v
    # section through the axis (x toward the aperture)
    v = View('K2 section through the axis and the aperture centre', ['x (mm) toward the aperture', 'z (mm)'])
    S = silhouette(prof)
    right_half = S.intersection(box(0, -1, 300, 1000))
    path_r = [p for p in prof]
    band_r = LineString(path_r).buffer(t, cap_style=2, join_style=2).intersection(right_half)
    shell_r = band_r
    # the aperture cut through the hood wall on +x
    cut = box(200, ap['sill_z'], 300, ap['top_z'])
    shell_r = shell_r.difference(cut)
    shell_l = affinity.scale(band_r, xfact=-1, yfact=1, origin=(0, 0))
    v.add('shell_right_cut_at_aperture', 'shell', 'gel_green_chalk', shell_r)
    v.add('shell_left', 'shell', 'gel_green_chalk', shell_l)
    # return flanges on the sill and under the dome
    rs = r_of_z(prof, ap['sill_z']); rt = r_of_z(prof, ap['top_z'])
    fd = ap['return_flange_depth']; ft = ap['return_flange_t']
    v.add('aperture_sill_flange', 'aperture', 'gel_green_chalk', box(rs - t - fd, ap['sill_z'], rs - t, ap['sill_z'] + ft))
    v.add('aperture_top_flange', 'aperture', 'gel_green_chalk', box(rt - t - fd, ap['top_z'] - ft, rt - t, ap['top_z']))
    lp = K['parts']['liner']['profile_rz']
    liner = LineString(lp).buffer(0.8, cap_style=2, join_style=2)
    v.add('liner_right', 'liner', 'zinc_weathered', liner)
    v.add('liner_left', 'liner', 'zinc_weathered', affinity.scale(liner, xfact=-1, yfact=1, origin=(0, 0)))
    v.add('ballast', 'ballast', 'concrete_precast', box(-196, 8, 196, 52).intersection(S), edge=False)
    out['K2_section'] = v
    return out


def d1_views(T):
    K = T['kinds']['D1']; prof = K['outer_profile_rz']; lid = K['lid']['profile_rz']; sh = K['side_handles']; lh = K['lid']['handle']; t = K['sheet']['thickness']
    top = [i for i, p in enumerate(prof) if p[1] == K['body_top']][0]
    body_sil = silhouette(prof, 0.0, top_index=top)
    lid_sil = silhouette([(0.0, lid[0][1])] + lid + [(0.0, lid[-1][1])][:0], 0.0)
    lid_poly = Polygon([(r, z) for r, z in lid] + [(-r, z) for r, z in reversed(lid)]).buffer(0)
    rhz = lambda z: r_of_z(prof, z)
    # side view along x: the handles in profile at y = +-(r + proud)
    v = View('D1 galvanised dustbin, side (looking along x; the two handles in profile)', ['y (mm)', 'z (mm)'])
    v.add('body', 'body', 'zinc_weathered', body_sil)
    v.add('lid', 'lid', 'zinc_weathered', lid_poly)
    hh = box(-lh['length'] / 2, lid[-1][1], lh['length'] / 2, lh['top_z'])
    v.add('lid_handle', 'lid', 'zinc_weathered', hh)
    r_h = rhz(sh['z'])
    for sgn in (1, -1):
        g = loop_handle_side(r_h, sh['proud'], sh['z'] - sh['height'] / 2, sh['z'] + sh['height'] / 2, sh['strap_t'], sh['strap_w'])
        v.add('side_handle_%s' % ('plus' if sgn > 0 else 'minus'), 'handle', 'zinc_weathered', g if sgn > 0 else affinity.scale(g, xfact=-1, yfact=1, origin=(0, 0)))
    out = {'D1_side': v}
    # front view along y: one handle face-on
    v = View('D1 front (looking along y; one handle face-on)', ['x (mm)', 'z (mm)'])
    v.add('body', 'body', 'zinc_weathered', body_sil)
    v.add('lid', 'lid', 'zinc_weathered', lid_poly)
    v.add('lid_handle', 'lid', 'zinc_weathered', box(-lh['length'] / 2, lid[-1][1], lh['length'] / 2, lh['top_z']))
    face = box(-sh['strap_w'] * 2.4, sh['z'] - sh['height'] / 2, sh['strap_w'] * 2.4, sh['z'] + sh['height'] / 2)
    inner = box(-sh['strap_w'] * 2.4 + sh['strap_t'] * 2, sh['z'] - sh['height'] / 2 + sh['strap_t'], sh['strap_w'] * 2.4 - sh['strap_t'] * 2, sh['z'] + sh['height'] / 2 - sh['strap_t'])
    v.add('side_handle_face', 'handle', 'zinc_weathered', face.difference(inner))
    out['D1_front'] = v
    # plan
    v = View('D1 plan', ['x (mm)', 'y (mm)'])
    v.add('lid', 'lid', 'zinc_weathered', circle(0, 0, 251.0))
    v.add('rim_bead', 'body', 'zinc_weathered', ring(0, 0, 220.0, K['rim']['bead_r_max']))
    v.add('foot_ring', 'body', 'zinc_dark_grime', ring(0, 0, 200.0, K['foot_ring']['r_max']))
    v.add('lid_handle', 'lid', 'zinc_weathered', box(-lh['length'] / 2, -lh['strap_w'] / 2, lh['length'] / 2, lh['strap_w'] / 2))
    for sgn in (1, -1):
        v.add('side_handle_%s' % ('plus' if sgn > 0 else 'minus'), 'handle', 'zinc_weathered', box(-sh['strap_w'] * 1.2, sgn * r_h, sh['strap_w'] * 1.2, sgn * (r_h + sh['proud'])) if sgn > 0 else box(-sh['strap_w'] * 1.2, -(r_h + sh['proud']), sh['strap_w'] * 1.2, -r_h))
    for zc in K['rib_z']:
        v.lines.append(('rib_r_%d' % zc, [(rhz(zc) + K['rib']['proud'] * math.cos(a), (rhz(zc) + K['rib']['proud']) * math.sin(a)) for a in np.linspace(0, 2 * math.pi, 120)]))
    out['D1_plan'] = v
    # section: sheet bands
    v = View('D1 section through the axis, lid on', ['x (mm)', 'z (mm)'])
    S = silhouette(prof, 0.0, top_index=top)
    right = S.intersection(box(0, -1, 400, 800))
    band = LineString(prof[:top + 1]).buffer(t, cap_style=2, join_style=2).intersection(right)
    v.add('body_right', 'body', 'zinc_weathered', band)
    v.add('body_left', 'body', 'zinc_weathered', affinity.scale(band, xfact=-1, yfact=1, origin=(0, 0)))
    lid_band = LineString(lid).buffer(t, cap_style=2, join_style=2)
    v.add('lid_right', 'lid', 'zinc_weathered', lid_band)
    v.add('lid_left', 'lid', 'zinc_weathered', affinity.scale(lid_band, xfact=-1, yfact=1, origin=(0, 0)))
    v.add('lid_handle', 'lid', 'zinc_weathered', box(-lh['length'] / 2, lid[-1][1], lh['length'] / 2, lh['top_z']).difference(box(-lh['length'] / 2 + lh['strap_t'], lid[-1][1], lh['length'] / 2 - lh['strap_t'], lh['top_z'] - lh['strap_t'])))
    out['D1_section'] = v
    return out


def street_plan(T):
    P = T['placements']; ref = T['street_reference']
    v = View('Quay Street, plan of the litter bins and what they stand beside (20 mm a pixel; x along, z across, east +)', ['x (m x1000 mm)', 'z (m x1000 mm)'], 20.0)
    L = ref['street_length_m'] * 1000
    v.add('carriageway', 'ground', 'asphalt', box(0, -3000, L, 3000), edge=False)
    v.add('footway_east', 'ground', 'flags', box(0, ref['kerb_back_m'] * 1000, L, ref['building_line_m'] * 1000), edge=False)
    v.add('footway_west', 'ground', 'flags', box(0, -ref['building_line_m'] * 1000, L, -ref['kerb_back_m'] * 1000), edge=False)
    v.add('kerb_east', 'kerb', 'kerb', box(0, 3000, L, ref['kerb_back_m'] * 1000))
    v.add('kerb_west', 'kerb', 'kerb', box(0, -ref['kerb_back_m'] * 1000, L, -3000))
    for s in ref['shops']:
        z0, z1 = (ref['building_line_m'] * 1000, ref['building_line_m'] * 1000 + 800) if s['side'] == 'east' else (-ref['building_line_m'] * 1000 - 800, -ref['building_line_m'] * 1000)
        v.add('shop_' + s['id'], 'building', 'brick', box(s['x0'] * 1000, z0, s['x1'] * 1000, z1))
        zz = ref['building_line_m'] * 1000 * (1 if s['side'] == 'east' else -1)
        for key, w in (('shop_door', 900), ('side_door', 838)):
            if s.get(key) is not None:
                v.add(f"{s['id']}_{key}", 'door', 'door', box(s[key] * 1000 - w / 2, zz - 60 if s['side'] == 'east' else zz - 40, s[key] * 1000 + w / 2, zz + 60 if s['side'] == 'east' else zz + 60))
    for o in ref['obstacles']:
        g = circle(o['x'] * 1000, o['z'] * 1000, o['r'] * 1000, 32) if o['shape'] == 'circle' else box((o['x'] - o['w'] / 2) * 1000, (o['z'] - o['d'] / 2) * 1000, (o['x'] + o['w'] / 2) * 1000, (o['z'] + o['d'] / 2) * 1000)
        v.add(o['id'], 'obstacle', 'obstacle', g)
    for b in P['bins']:
        if b['kind'] == 'K1':
            v.add(b['id'] + '_post', 'bin', 'paint_green_worn', circle(b['post_x_m'] * 1000, b['post_z_m'] * 1000, 38.05, 24))
            v.add(b['id'] + '_bin', 'bin', 'paint_green_worn', circle(b['bin_axis_x_m'] * 1000, b['bin_axis_z_m'] * 1000, 186.5, 40))
        else:
            v.add(b['id'] + '_bin', 'bin', 'gel_green_chalk', circle(b['axis_x_m'] * 1000, b['axis_z_m'] * 1000, 250.0, 48))
    for d in P['dustbins']:
        v.add(d['id'], 'bin', 'zinc_weathered', circle(d['axis_x_m'] * 1000, d['axis_z_m'] * 1000, 250.0, 40))
    return {'street_plan': v}


def scale_sheet(T):
    v = View('K1, K2 and D1 side by side at one scale, with the 950 mm iron bollard of urban_street_02 (K2b) and a 1.75 m figure', ['mm', 'mm'])
    ref = T['reference_objects']
    x = 0.0
    K1p = T['kinds']['K1']
    k1 = K1p['bin']; rp = K1p['post']['od'] / 2
    items = []
    post = silhouette(K1p['post']['profile_rz'], x + 60)
    b = silhouette(k1['outer_profile_rz'], x + 60 + k1['axis_offset_x'], top_index=8)
    v.add('K1_post', 'K1', 'paint_green_worn', post); v.add('K1_bin', 'K1', 'paint_green_worn', b)
    x += 520
    v.add('K2', 'K2', 'gel_green_chalk', silhouette(T['kinds']['K2']['outer_profile_rz'], x + 100))
    x += 400
    D = T['kinds']['D1']
    top = [i for i, p in enumerate(D['outer_profile_rz']) if p[1] == D['body_top']][0]
    v.add('D1_body', 'D1', 'zinc_weathered', silhouette(D['outer_profile_rz'], x + 110, top_index=top))
    lp = D['lid']['profile_rz']
    v.add('D1_lid', 'D1', 'zinc_weathered', Polygon([(x + 110 + r, z) for r, z in lp] + [(x + 110 - r, z) for r, z in reversed(lp)]).buffer(0))
    v.add('D1_lid_handle', 'D1', 'zinc_weathered', box(x + 110 - 50, lp[-1][1], x + 110 + 50, D['lid']['handle']['top_z']))
    x += 400
    v.add('bollard_K2b', 'ref', 'iron_black', silhouette(ref['bollard_K2b_profile_rz'], x + 100))
    x += 360
    h = ref['person_height_mm']
    v.add('figure_1750', 'ref', 'figure', Polygon([(x + 100 - 120, 0), (x + 100 - 120, 780), (x + 100 - 200, 800), (x + 100 - 215, 1420), (x + 100 - 170, 1480), (x + 100 - 85, 1500), (x + 100 - 85, 1560), (x + 100 - 95, h - 25), (x + 100 - 30, h), (x + 100 + 30, h), (x + 100 + 95, h - 25), (x + 100 + 85, 1560), (x + 100 + 85, 1500), (x + 100 + 170, 1480), (x + 100 + 215, 1420), (x + 100 + 200, 800), (x + 100 + 120, 780), (x + 100 + 120, 0)]).buffer(0))
    return {'scale_sheet': v}


def build_all(T):
    views = {}
    for fn in (k1_views, k2_views, d1_views, street_plan, scale_sheet):
        views.update(fn(T))
    return views


# ------------------------------------------------------------------------------------------------------------------------------ pictures
PAL = {'paint_green_worn': (62, 76, 51), 'paint_green_chalk': (88, 100, 82), 'gel_green_chalk': (92, 112, 96), 'gel_green_fresh': (40, 78, 58), 'letters_cream': (226, 222, 205),
       'letters_cream_worn': (196, 190, 170), 'zinc_new': (168, 177, 174), 'zinc_weathered': (120, 130, 130), 'zinc_dark_grime': (89, 88, 82), 'bin_sack_black': (22, 22, 24),
       'concrete_precast': (153, 137, 118), 'asphalt': (70, 70, 74), 'flags': (150, 146, 140), 'kerb': (125, 125, 128), 'brick': (130, 82, 66), 'door': (60, 74, 88), 'obstacle': (200, 120, 60),
       'iron_black': (35, 35, 36), 'figure': (170, 140, 120)}


def draw(view, path, pad=40):
    from PIL import Image, ImageDraw
    sc = view.scale
    minx, miny, maxx, maxy = view.bounds()
    W = int((maxx - minx) / sc) + 2 * pad; H = int((maxy - miny) / sc) + 2 * pad + 22
    im = Image.new('RGB', (W, H), (246, 246, 242)); d = ImageDraw.Draw(im)
    X = lambda x: pad + (x - minx) / sc
    Y = lambda y: H - pad - (y - miny) / sc
    # grid ticks every 100 mm
    gx = math.ceil(minx / 100) * 100
    while gx <= maxx:
        d.line([(X(gx), Y(miny) + 4), (X(gx), Y(miny) + 10)], fill=(150, 150, 150)); gx += 100 * (5 if sc > 5 else 1)
    for p in view.polys:
        gs = [p['geom']] if p['geom'].geom_type == 'Polygon' else list(p['geom'].geoms)
        col = PAL.get(p['material'], (160, 160, 160))
        for g in gs:
            if g.geom_type != 'Polygon':
                continue
            pts = [(X(x), Y(y)) for x, y in g.exterior.coords]
            d.polygon(pts, fill=col, outline=(15, 15, 15) if p['edge'] else None)
            for hole in g.interiors:
                d.polygon([(X(x), Y(y)) for x, y in hole.coords], fill=(246, 246, 242), outline=(15, 15, 15))
    for n, pts in view.lines:
        d.line([(X(a), Y(b)) for a, b in pts], fill=(200, 50, 50), width=1)
    d.text((6, 4), view.title[:140], fill=(0, 0, 0))
    d.text((6, H - 16), f'{sc:g} mm a pixel; axes {view.axes[0]} / {view.axes[1]}', fill=(60, 60, 60))
    im.save(path)
    return im.size


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--target', default=os.path.join(HERE, 'target.json'))
    ap.add_argument('--json', default=os.path.join(HERE, 'drawing.json'))
    ap.add_argument('--out', default=None, help='folder for the pictures (never inside git outside production/previews)')
    a = ap.parse_args()
    T = json.load(open(a.target))
    views = build_all(T)
    doc = dict(schema='litter-bins drawing, 1', units='mm', source=os.path.basename(a.target), views={k: v.to_json() for k, v in views.items()})
    json.dump(doc, open(a.json, 'w'))
    print('wrote', a.json, {k: len(v.polys) for k, v in views.items()})
    if a.out:
        os.makedirs(a.out, exist_ok=True)
        for k, v in views.items():
            print(k, draw(v, os.path.join(a.out, k + '.png')))


if __name__ == '__main__':
    main()
