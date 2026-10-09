"""Photograph measurements of the kerbs-and-covers target, recomputed from the raw readings kept in target.json.

Two methods are used (both on Poly Haven's CC0 London panoramas, camera height 1.6 m, proved by the 75 mm yellow line):

 * 'pano_depression': a rectilinear view (yaw, pitch, fov, w, h) is cut from the equirectangular panorama; a row in the
   view gives the angle below the horizon, and a vertical face at ground distance d = cam_h / tan(foot angle) has its top edge
   at height cam_h - d * tan(top angle).  Rows were read by eye on a gridded view and on a luminance profile.
 * 'ortho': the panorama is re-projected to a plane (the ground, or the kerb top 125 mm up) at 3 mm a pixel; lengths on the
   plane are read in pixels.  Things above the plane are smeared outward, so each reading names its plane.
"""
import math

CAM_H = 1600.0


def depression(row, pitch, fov, w, h):
    f = (w / 2.0) / math.tan(math.radians(fov) / 2.0)
    return -pitch + math.degrees(math.atan((row - h / 2.0) / f))


def kerb_from_rows(raw, cam_h=CAM_H, assumed_upstand=125.0):
    v = raw['view']
    a_f = depression(raw['rows']['foot'], v['pitch'], v['fov'], v['w'], v['h'])
    a_m = depression(raw['rows']['arris_mid'], v['pitch'], v['fov'], v['w'], v['h'])
    a_r = depression(raw['rows']['rear'], v['pitch'], v['fov'], v['w'], v['h'])
    d_f = cam_h / math.tan(math.radians(a_f))
    upstand = cam_h - d_f * math.tan(math.radians(a_m))
    d_r_assumed = (cam_h - assumed_upstand) / math.tan(math.radians(a_r))
    d_r_measured = (cam_h - upstand) / math.tan(math.radians(a_r))
    return {'foot_distance_mm': round(d_f), 'upstand_to_arris_mid_mm': round(upstand, 1),
            'top_width_given_assumed_upstand_mm': round(d_r_assumed - d_f, 1), 'assumed_upstand_mm': assumed_upstand,
            'top_width_given_measured_upstand_mm': round(d_r_measured - d_f, 1)}


def ortho_len(px, mm_per_px, plane_factor=1.0):
    return px * mm_per_px * plane_factor


def circle_fit(points):
    """least-squares circle through points (x, y); returns centre and radius"""
    n = len(points)
    sx = sum(p[0] for p in points); sy = sum(p[1] for p in points)
    sxx = sum(p[0] ** 2 for p in points); syy = sum(p[1] ** 2 for p in points); sxy = sum(p[0] * p[1] for p in points)
    sxxx = sum(p[0] ** 3 for p in points); syyy = sum(p[1] ** 3 for p in points)
    sxxy = sum(p[0] ** 2 * p[1] for p in points); sxyy = sum(p[0] * p[1] ** 2 for p in points)
    c = n * sxx - sx * sx; d = n * sxy - sx * sy; e = n * (sxxx + sxyy) - (sxx + syy) * sx
    g = n * syy - sy * sy; h = n * (sxxy + syyy) - (sxx + syy) * sy
    den = c * g - d * d
    a = (h * d - e * g) / den; b = (d * e - c * h) / den
    cx = -a / 2.0; cy = -b / 2.0
    r = math.sqrt(max(0.0, (a * a + b * b) / 4.0 - (sxx + syy - cx * sx - cy * sy + 0.0) / n + 0.0))
    # use mean distance (robust for a small arc)
    r = sum(math.hypot(p[0] - cx, p[1] - cy) for p in points) / n
    return cx, cy, r


def compute(pm):
    """results of one photo measurement from its raw readings"""
    m = pm['method']
    raw = pm['raw']
    if m == 'pano_depression':
        r = kerb_from_rows(raw, assumed_upstand=raw.get('assumed_upstand_mm', 125.0))
        return r
    if m == 'ortho_px_list':
        mm = raw['mm_per_px']
        vals = [ortho_len(p, mm, raw.get('plane_factor', 1.0)) for p in raw['px']]
        return {'values_mm': [round(v, 1) for v in vals], 'mean_mm': round(sum(vals) / len(vals), 1),
                'min_mm': round(min(vals), 1), 'max_mm': round(max(vals), 1)}
    if m == 'ortho_two_edges':
        mm = raw['mm_per_px']
        return {'length_mm': round(abs(raw['px1'] - raw['px0']) * mm, 1)}
    if m == 'ortho_rows_to_distance':
        # rows in the MAIN frame -> distance from the camera in mm: 5000 - 3 * row
        return {'distances_mm': [5000 - 3 * r for r in raw['rows']],
                'difference_mm': (5000 - 3 * raw['rows'][1]) - (5000 - 3 * raw['rows'][0])}
    if m == 'rows_height_corrected':
        # rows of the 3 mm MAIN ground frame; an edge at height z above the channel level is smeared outward by 1600/(1600-z)
        d0 = 5000 - 3 * raw['foot_row']
        d1 = (5000 - 3 * raw['edge_row']) * (1600 - raw['edge_z_mm']) / 1600.0
        return {'width_mm': round(d0 - d1, 1)}
    if m == 'corner_angle':
        # interior angle between two straight runs from their directions on the ground picture (degrees from the picture's x axis)
        a = 180.0 - abs(raw['dirs_deg'][0] - raw['dirs_deg'][1])
        b = 180.0 - abs(raw['dirs2_deg'][0] - raw['dirs2_deg'][1])
        return {'interior_edges_deg': round(a, 1), 'interior_lines_deg': round(b, 1), 'mean_deg': round((a + b) / 2, 1)}
    if m == 'setback_from_rows':
        # foot row on the ground frame (z = 0); the arris row on the kerb-top frame (plane z = 125 mm, camera 1475 mm)
        d_foot = 5000 - 3 * raw['foot_row']
        d_edge = (5000 - 3 * raw['edge_row']) * (CAM_H - raw['edge_z_mm']) / (CAM_H - raw['plane_z_mm'])
        return {'set_back_mm': round(d_edge - d_foot, 1)}
    if m == 'angular_width':
        dpp = raw['fov_deg'] / raw['w_px']
        return {'width_mm': round(raw['px'] * math.radians(dpp) * raw['distance_mm'], 1)}
    if m == 'smear_height':
        s = raw['smear_mm']; d = raw['distance_mm']
        return {'height_mm': round(CAM_H * s / (d + s), 1)}
    if m == 'circle_fit_px':
        pts = raw['points_px']
        cx, cy, r = circle_fit(pts)
        R = r * raw['mm_per_px']
        return {'radius_to_line_mm': round(R), 'radius_face_mm': round(R - raw['line_offset_mm']), 'centre_px': [round(cx), round(cy)]}
    if m == 'lattice_vectors_px':
        mm = raw['mm_per_px']
        out = {'pitch_a_mm': round(math.hypot(*raw['a_px']) * mm, 1), 'pitch_b_mm': round(math.hypot(*raw['b_px']) * mm, 1)}
        out['dot_cos'] = round((raw['a_px'][0] * raw['b_px'][0] + raw['a_px'][1] * raw['b_px'][1]) /
                               (math.hypot(*raw['a_px']) * math.hypot(*raw['b_px'])), 3)
        return out
    if m == 'edge_lengths_px':
        mm = raw['mm_per_px']
        return {'lengths_mm': [round(math.hypot(*e) * mm, 1) for e in raw['edges_px']]}
    if m == 'listed':
        return dict(raw.get('results', {}))
    raise ValueError(m)
