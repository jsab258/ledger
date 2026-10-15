#!/usr/bin/env python
"""Builds target.json of the bollards family from bollard_data.py (and frames.json, once make_previews.py has made it).
Run order: make_target.py, make_previews.py PANO_DIR OUT_DIR, make_target.py, self_check.py.
/home/user/.bpyenv/bin/python make_target.py"""
import os, sys, json, math
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import bollard_data as D
import bollard_lib as L

r1 = lambda x: round(float(x), 1)


def finalise(read, h_read, h_cam):
    k = h_cam / h_read
    return L.scale_profile(read, k)


def fit_variant(base_profile, stations_final, z_ratio):
    """radius factor kr (least squares) of a variant of base_profile with every z multiplied by z_ratio, against (z, half width) stations"""
    zs = np.array([s[0] for s in stations_final], float)
    hw = np.array([s[1] for s in stations_final], float)
    rb = L.r_of_z(base_profile, zs / z_ratio)
    m = ~np.isnan(rb)
    kr = float((rb[m] * hw[m]).sum() / (rb[m] ** 2).sum())
    resid = hw[m] - kr * rb[m]
    return kr, float(np.abs(resid).max()), float(np.sqrt((resid ** 2).mean()))


def scale_rz(profile, kr, kz):
    return [(round(r * kr, 2), round(z * kz, 2)) for r, z in profile]


def feature(profile, z0, z1):
    zs = np.arange(z0, z1 + 0.5, 0.5)
    r = L.r_of_z(profile, zs)
    r = r[~np.isnan(r)]
    return r1(r.min()), r1(r.max())


def kit_junction(setback=0.5):
    """the four junction bollards from the south-quay kit's own junction builder: the two tangent points of the 8 m return (inside Quay Street's turn west) and the two of the 6 m
    return (the Harbour Board approach), each moved `setback` m from the kerb face along the footway normal (away from the road). The 12 m outside return carries none."""
    sys.path.insert(0, os.path.join(HERE, '..', '..', '..', '..', 'tools', 'art-recipes', 'south-quay'))
    import south_quay_geom as G
    sc = G.read_street_constants(); at = G.read_atlas(); jn = G.Junction(sc, at)
    nN_left = G.left2(jn.dN)
    nN_right = (-nN_left[0], -nN_left[1]); nE1_right = (-jn.nE1_left[0], -jn.nE1_left[1])
    rows = [('nw_T1', 8.0, jn.nw_T[0], nN_left, 'Quay Street\'s west kerb'), ('nw_T2', 8.0, jn.nw_T[1], jn.nW_left, 'the west road\'s north kerb'),
            ('ne_T1', 6.0, jn.ne_T[0], nN_right, 'Quay Street\'s east kerb'), ('ne_T2', 6.0, jn.ne_T[1], nE1_right, 'the Harbour Board approach\'s north kerb')]
    out = []
    for name, rad, T_, n, on in rows:
        out.append(dict(id=name, return_radius_m=rad, tangent_x_m=round(T_[0], 3), tangent_y_m=round(T_[1], 3), x_m=round(T_[0] + setback * n[0], 2), y_m=round(T_[1] + setback * n[1], 2),
                        on=on, normal=[round(n[0], 4), round(n[1], 4)]))
    return out


def build():
    PAN = D.PANOS
    hc = {k: v['h_cam'] for k, v in PAN.items()}
    K1 = finalise(D.K1_READ, D.FRAMES['US01_b']['h_read'], hc['urban_street_01'])
    K2 = finalise(D.K2_READ, D.FRAMES['BB_b']['h_read'], hc['birbeck_street_underpass'])
    K5 = finalise(D.K5_READ, D.FRAMES['LH_b']['h_read'], hc['limehouse'])
    H1 = max(z for r, z in K1); H2 = max(z for r, z in K2); H5 = max(z for r, z in K5)

    # the second K1 photograph (BGE_a): a SECOND CASTING of the pattern, NOT a model: shorter, slimmer, a taller rolled plinth, its bead a little higher
    kbge = hc['bethnal_green_entrance'] / D.FRAMES['BGE_a']['h_read']
    bge_hw = [(z * kbge, hw * kbge) for z, hw in D.BGE_A_HALFWIDTH]
    bge_H = D.BGE_A_TOP_Z_READ * kbge
    kz_bge = bge_H / H1
    kr_bge, bge_max, bge_rms = fit_variant(K1, bge_hw, kz_bge)
    K1B = scale_rz(K1, kr_bge, kz_bge)           # the comparison outline of BGE_a (used to mask and fit its picture only)
    # K2b (US02_a): its own profile, read at its own calibrated height (0.92 m: every z and r x 0.80 of the reading)
    kus = hc['urban_street_02'] / D.FRAMES['US02_a']['h_read']
    us_hw = [(z * kus, hw * kus) for z, hw in D.US02_HALFWIDTH_READ]
    us_H = D.US02_TOP_Z_READ * kus
    kz_us = us_H / H2
    sel = [(z, hw) for z, hw in us_hw if 150 * kus <= z <= 1000 * kus and not (640 * kus <= z <= 740 * kus)]
    kr_us, us_max, us_rms = fit_variant(K2, sel, kz_us)
    top = [(round(r * kus, 2), round(z * kus, 2)) for r, z in D.K2B_TOP_READ]
    z_join = top[0][1]
    shaft = [(round(r * kr_us, 2), round(z * kz_us, 2)) for r, z in K2 if z * kz_us < z_join - 5]
    K2B = shaft + top

    prof_final = {'US01_b': K1, 'BGE_a': K1B, 'BB_b': K2, 'US02_a': K2B, 'LH_b': K5}

    # judgement kinds
    K3 = [(0, 0), (124, 0), (125, 3), (100, 805), (98.5, 815), (90, 832), (70, 842), (40, 847), (0, 850)]
    K4 = [(0, 0), (57.15, 0), (57.15, 982), (54, 989), (44, 995), (26, 999), (0, 1000)]
    K6A = [(0, 0)] + [(round(r * 1000, 1), round(z * 1000, 1)) for r, z in
                       ((0.25, 0.00), (0.25, 0.04), (0.19, 0.06), (0.17, 0.08), (0.15, 0.47), (0.13, 0.51), (0.13, 0.55),
                        (0.21, 0.59), (0.22, 0.63), (0.20, 0.67), (0.11, 0.71), (0.0, 0.72))]
    # the upturned cannon: a barrel with reinforcing rings, the muzzle swell (r 172) with a flat muzzle face at z 914, and a ball of radius 105 (centre z 877) standing 68 above it
    K6B = [(0, 0), (190, 0), (190, 30), (176, 60), (170, 600), (176, 604), (176, 640), (162, 646), (150, 700), (150, 760),
           (150, 840), (162, 856), (172, 880), (172, 905), (158, 914),
           (98.3, 914), (87.5, 935), (70.3, 955), (48.7, 970), (24.9, 979), (0, 982)]
    # a horn cleat: half of the elevation outline (x from the centre, z), mirrored by the drawing
    CLEAT_HALF = [(0, 0), (200, 0), (200, 22), (62, 22), (48, 70), (185, 98), (200, 120), (172, 126), (130, 108), (0, 92)]

    def parts_from_profile(profile, spec):
        out = []
        for name, z0, z1, what in spec:
            rmin, rmax = feature(profile, z0, z1)
            out.append(dict(name=name, z0=z0, z1=z1, r_min=rmin, r_max=rmax, what=what))
        return out

    f1 = hc['urban_street_01'] / 1.15
    f2 = hc['birbeck_street_underpass'] / 1.15
    z = lambda v: round(v * f1, 1)
    z2 = lambda v: round(v * f2, 1)
    R = lambda P, a, b: feature(P, a, b)
    k1_parts = parts_from_profile(K1, [
        ('plinth', 0, z(116), 'a plain cylinder r %.0f, a 3 mm chamfer at the foot, its top edge rounded about R6' % R(K1, 50, 60)[1]),
        ('shoulder', z(116), z(134), 'the plinth top sloping in to the shaft (a cove, 20 mm run)'),
        ('shaft_lower', z(134), z(493), 'one straight taper (about 1.6 degrees a side), r %.0f to %.0f' % (R(K1, z(134), z(134))[1], R(K1, z(493), z(493))[1])),
        ('bead', z(493), z(557), 'a half-round bead, %.0f high and %.0f proud, fuller below its middle; a thin fillet ring (about 4 high, 1 proud) on its top edge' % (z(557) - z(493), R(K1, z(493), z(557))[1] - R(K1, z(493), z(493))[1])),
        ('shaft_upper', z(557), z(900), 'the same taper carried on, r %.1f to %.1f' % (R(K1, z(557), z(557))[1], R(K1, z(900), z(900))[1])),
        ('neck', z(900), z(940), 'a slight cove, r %.1f to %.1f' % (R(K1, z(900), z(900))[1], R(K1, z(940), z(940))[1])),
        ('cap_collar', z(940), z(968), 'a fat rounded ring, %.0f high, %.0f proud of the neck, max r %.0f' % (z(968) - z(940), R(K1, z(940), z(968))[1] - R(K1, z(940), z(940))[1], R(K1, z(940), z(968))[1])),
        ('quirk_and_ring', z(968), z(987), 'a 4 mm groove, then a thin plain ring %.0f high at r %.0f' % (z(987) - z(972), R(K1, z(975), z(985))[1])),
        ('dome', z(987), z(1041), 'a flattened dome, r %.1f at its foot, %.0f high, a little less than a hemisphere' % (R(K1, z(990), z(990))[1], z(1041) - z(988))),
    ])
    k2_parts = parts_from_profile(K2, [
        ('foot_ring', 0, z2(46), 'a rolled foot ring: r %.0f at its fullest (z about 12), its top sloping in to the shaft' % R(K2, 0, 50)[1]),
        ('shaft_lower', z2(46), z2(635), 'one straight taper, r %.0f to %.0f' % (R(K2, z2(46), z2(46))[1], R(K2, z2(635), z2(635))[1])),
        ('collar_band', z2(635), z2(672), 'a thin rounded band, %.0f high, %.0f proud (r %.0f at its fullest), at 0.59 of the height' % (z2(672) - z2(635), R(K2, z2(635), z2(672))[1] - R(K2, z2(635), z2(635))[1], R(K2, z2(635), z2(672))[1])),
        ('shaft_upper', z2(672), z2(1088), 'a gentler taper, r %.0f to %.0f' % (R(K2, z2(672), z2(672))[1], R(K2, z2(1088), z2(1088))[1])),
        ('cap_plate', z2(1088), z2(1112.5), 'a flat plate (r %.0f) that overhangs the shaft by about %.0f and is slightly domed (5 mm)' % (R(K2, z2(1092), z2(1104))[1], R(K2, z2(1092), z2(1104))[1] - R(K2, z2(1088), z2(1088))[1])),
    ])
    k5_parts = parts_from_profile(K5, [
        ('flange', 0, 100, 'a round cast flange r 143, rim 36 high with a rounded top edge, its top sloping up to the shaft'),
        ('shaft_lower', 100, 278, 'a cylinder r 91'),
        ('lower_bead', 278, 398, 'a fat bead, r 105 at its fullest, 120 high, flared below and rounded above'),
        ('shaft_mid', 398, 868, 'a cylinder r 90 narrowing to 86'),
        ('upper_bead', 868, 926, 'a second, smaller bead, r 101 at its fullest, with a fillet ring on top'),
        ('neck', 926, 1000, 'a cylinder r 80'),
        ('cap_collar', 1000, 1075, 'a flaring collar to a rounded rim r 107 (at z 1042), then a quirk and a step to r 84'),
        ('dome', 1075, 1135, 'a step r 84 up to z 1090, then a dome r 62 at its foot, 40 high'),
    ])

    fr = {}
    p = os.path.join(HERE, 'frames.json')
    if os.path.exists(p):
        fr = json.load(open(p))

    T = {}
    T['family'] = 'bollards'
    T['title'] = 'Quay Street bollards and the quay\'s mooring ironwork: the target (cloud week 42, 9 October 2026)'
    T['written'] = '2026-10-09'
    T['units'] = 'millimetres unless a key says _m (metres); angles in degrees; the .glb is metres, z up, scale 1'
    T['summary_line'] = ('Quay Street\'s bollards are black cast-iron posts about 1.08 m high (a domed cap, one big collar bead at half height, a plinth foot 0.2 m across), '
                         'plain tapered iron posts about 1.05 m high (a collar band at 0.59 H, a rolled foot ring 0.25 m across), and (judgement, no reached photograph) '
                         'concrete and steel-tube posts, 6 on the street and 4 at the quay-end junction, with 10 mooring bollards, 4 chain posts and 3 cleats on the quay; '
                         'all unmarked, unbanded, 0.5 m behind the kerb face.')
    T['frame'] = dict(
        profile='(r, z): r the radius from the axis, z up from the ground at the foot; every lathe profile runs from (0,0) up the outline to the axis at the top',
        pivot='the centre of the base on the ground (the footway flag top, +120 mm above the channel; the quay apron, level with the kerb top)',
        axis='vertical; the seed lean is a rotation about the pivot of 0 to 2 degrees',
        elevation_polygon='mirrored about the axis: left (t = -r), right (t = +r)',
        glb='metres, z up, scale 1; one mesh per variant; bolts, chain eyes and chains as separate meshes of the same piece')
    anchors_json = os.path.join(HERE, 'anchors.json')
    horizon = json.load(open(anchors_json)) if os.path.exists(anchors_json) else []
    T['calibration'] = dict(
        method=('Poly Haven\'s 8k tone-mapped panoramas (CC0) are re-projected to a flat, square-on elevation of one bollard (a vertical plane through its axis, perpendicular to '
                'the line of sight, 1 mm a pixel). The camera height is NOT known and is NOT 1.6 m here. EACH CAMERA HEIGHT IS MEASURED AT THE BOLLARD\'S OWN GROUND LEVEL: '
                'where an anchor stands on another level (a wall on the footway above a planted bed, a line on the road below a footway) the step between them is measured and added. '
                'Two kinds of anchor: (1) walls by the HORIZON method, which needs no re-projection and no assumed height: in a levelled equirectangular panorama the horizon is the middle row, '
                'the courses of a 75 mm brick wall are evenly spaced in tan(angle) and the camera height above the wall\'s foot is 75 mm x tan(angle of the foot) / (course pitch in tan units); '
                '(2) a yellow line or a paver measured on a plane at an assumed 1.6 m, whose true height is 1.6 x true size / measured size. Every length then scales with the height (+-4 to +-7 %).'),
        panoramas={k: dict(v, coords=list(v['coords'])) for k, v in PAN.items()},
        horizon_anchors=horizon,
        anchors=D.CAL,
        kerbs_and_covers_note=('The kerbs-and-covers target takes 1.6 m for urban_street_01 and urban_street_02 (the Bethnal Green session of 18 August 2019). At the ROAD (where its kerbs and covers lie) '
                               'the heights are about 1.25 to 1.27 m in urban_street_01 (the bed stands about 0.055 m above the road, so the camera is about 1.25 m above the road) and about 1.03 m in urban_street_02 (0.92 on the footway plus the '
                               '0.125 kerb): 1.6 m is about 25 % high in urban_street_01 and about 55 % high in urban_street_02. Its numbers from those two panoramas (the mitred corner, the tarmac-filled cover) '
                               'should be re-checked.'))
    T['scene_numbers'] = D.PRINTED
    T['profiles_final'] = {k: [list(map(float, p)) for p in v] for k, v in prof_final.items()}
    T['variant_fits'] = dict(
        K1_second_casting_from_BGE_a=dict(z_factor=round(kz_bge, 4), r_factor=round(kr_bge, 4), max_resid_mm=round(bge_max, 1), rms_mm=round(bge_rms, 1),
                                          note='NOT a model: BGE_a read at its calibrated 1.02 m is %.0f %% shorter and %.0f %% slimmer than K1, with a taller rolled plinth (about 140, a convex roll on its top) and its bead centre at 0.53 H; its comparison outline only masks its picture' % ((1 - kz_bge) * 100, (1 - kr_bge) * 100)),
        K2b_from_US02_a=dict(z_factor=round(kz_us, 4), r_factor=round(kr_us, 4), max_resid_mm=round(us_max, 1), rms_mm=round(us_rms, 1),
                             note='US02_a read at its own calibrated 0.92 m (x 0.80 of the reading): a smaller casting of the same pattern (%.0f against %.0f high), the same collar height ratio (0.592 against 0.587), a low cone cap, black. K2b IS profiles_final.US02_a, whole.' % (us_H, H2)))
    T['readings'] = {k: [list(r) for r in v] for k, v in D.READINGS.items()}
    T['readings_r_correction'] = {'BB_b': D.K2_R_FACTOR, 'note': 'the first eyeball radii of BB_b were 3.5 % low: the overlay showed its left edge 8 mm and its right 1 mm out; the profile carries the factor'}
    T['bge_halfwidth_read'] = [list(p) for p in D.BGE_A_HALFWIDTH]
    T['us02_halfwidth_read'] = [list(p) for p in D.US02_HALFWIDTH_READ]
    T['frames'] = {k: dict(D.FRAMES[k], h_cam_m=hc[D.FRAMES[k]['pano']]) for k in D.FRAMES}
    T['photo_frames'] = fr
    T['setbacks_photo'] = [dict(s) for s in D.SETBACKS]

    T['kinds'] = {}
    T['kinds']['K1'] = dict(
        name='cast_iron_domed', title='Cast-iron street bollard, domed head, one collar bead (the cannon type\'s plain cousin)',
        basis='Photo (US01_b, measured at its bed level, +-6 %); BGE_a is a second, slimmer casting of the pattern and is NOT a model', height=H1, base_diameter=round(2 * max(r for r, zz in K1[:6]), 1),
        profile_rz=[list(map(float, p)) for p in K1], parts=k1_parts,
        mouldings=[
            dict(name='collar_bead', z=[z(493), z(557)], r_peak=feature(K1, z(493), z(557))[1], note='half-round, fuller below its middle; its underside is the drip; no beading or fluting on it'),
            dict(name='cap_collar', z=[z(940), z(968)], r_peak=feature(K1, z(940), z(968))[1], note='fat rounded ring with a flat underside at the neck'),
            dict(name='quirk', z=[z(968), z(972)], r=feature(K1, z(968), z(972))[0], note='a 4 mm groove between the collar and the thin ring'),
            dict(name='thin_ring', z=[z(972), z(987)], r=feature(K1, z(972), z(987))[1], note='plain, 15 high'),
            dict(name='plinth_edge', z=[z(116), z(134)], note='top edge R6, then a cove to the shaft')],
        edges='no sharp edges: every step is rounded (R4 to R8) or coved; the plinth foot has a 3 mm chamfer; no flats, no facets',
        seams='none visible at 5 mm a pixel; a faint casting parting line down each side may be added at 0.3 mm (Judgement)',
        fixings='none visible: rooted (cast in or set in a footing), nothing bolted',
        root=dict(on_flags='the plinth stands directly on the paving; the paving is cut round it or butts it; a 5 to 15 mm dark grit joint, no mortar fillet, no collar plate (Photo BGE_a)',
                  in_planting='in a bed it stands on the soil with bark chips and leaves banked 20 mm against the plinth (Photo US01_b)',
                  bed_level='US01_b\'s ground is the SOIL of a planted bed, 0.07 m below the footway kerb top (a 0.05 visible face, an edging stone, then 0.02 to the soil): its camera height is measured there. On a footway the pivot is the flag top.',
                  pivot='centre of the plinth at the ground'),
        paint=dict(colour='black', srgb=[24, 24, 26], srgb_measured='median 10 to 38 across the panoramas (tone-mapping differs); 24 chosen',
                   roughness_words='glossy, the sky shows in it', roughness=0.35, metal=0,
                   note='black gloss on cast iron; NO white or yellow band (none in any photograph); no reflective band; no sleeve'),
        wear=['paint lost in vertical flakes and scuffs at the foot: one pale 15 x 65 mm chip at z 70 to 135 on one side (Photo US01_b)',
              'WORN-FOOT CONDITION ONLY (Photo BGE_a): the lower 110 mm of the plinth bare grey-brown metal in a speckled pattern over 60 to 70 % of its area',
              'fine scratches and dull rub marks where bags and wheels touch it, below 0.5 m',
              'dust and tyre grime on the plinth and the lower shaft, cleaner above 0.7 m; the gloss keeps a bright sky reflection on the dome, the collars and the shoulder',
              'no rust streaks, no graffiti, no stickers, no dents (cast iron)'],
        second_casting=dict(note='BGE_a: %.0f %% shorter and %.0f %% slimmer, a plinth about 140 high with a convex roll on its top edge, the bead centre at 0.53 H; not modelled (one design to a street); its pictures stay as evidence' % ((1 - kz_bge) * 100, (1 - kr_bge) * 100),
                            z_factor=round(kz_bge, 4), r_factor=round(kr_bge, 4)),
        variants=[dict(id='K1', note='the US01_b profile: the one model; the yard mouth uses it twice with two condition seeds'),
                  dict(id='K1_condition', states=['glossy repaint, a few scuffs (US01_b)', 'worn foot: plinth paint 60 to 70 % gone to z 110 (BGE_a)', 'dull and chalky, grimy, a rust bloom at the foot (Judgement)'])])
    T['kinds']['K2'] = dict(
        name='cast_iron_plain', title='Plain tapered iron bollard, collar band at 0.59 H, rolled foot ring',
        basis='Photo (BB_b main, measured at its footway, 1.085 +-0.06 m; US02_a second, 0.92 +-0.04 m); scale +-6 %', height=H2,
        base_diameter=round(2 * max(r for r, zz in K2 if zz <= 50), 1),
        profile_rz=[list(map(float, p)) for p in K2], parts=k2_parts,
        mouldings=[dict(name='collar_band', z=[z2(635), z2(672)], r_peak=feature(K2, z2(635), z2(672))[1], note='a thin rounded band, no beads either side'),
                   dict(name='foot_ring', z=[0, z2(46)], r_peak=feature(K2, 0, z2(46))[1], note='rolled, 46 high; the top slopes in; a lighter rub mark round it')],
        edges='rounded or coved throughout; the cap plate edge R3',
        seams='none visible; a vertical dark scratch about 40 mm long at z 840 to 880 on BB_b is damage, not a seam',
        fixings='none visible',
        root=dict(on_flags='the foot ring sits on the paving or tarmac; a darker 20 mm ring of dirt round it; no collar plate (Photo BB_b, US02_a)', pivot='centre of the foot ring at the ground'),
        paint=dict(colour='black (the default: the 1990 norm, and US02_a\'s paint)', srgb=[24, 24, 26], srgb_grey_condition=[88, 89, 91],
                   srgb_measured='BB_b median (97, 77, 70) under the underpass\'s orange light, lightness 81 (the grey is a 2019 London underpass paint: ONE condition only); US02_a median (15, 16, 18)',
                   roughness_words='semi-gloss (black); satin (grey)', roughness=0.45, metal=0,
                   note='no band; the cap plate is the same paint (the orange rim in BB_b is the underpass light on the plate, not brass)'),
        wear=['a lighter, scuffed ring round the foot ring (Photo BB_b, US02_a)', 'a few chips and thin dark scratches on the upper shaft (Photo BB_b)',
              'dust and a tan dirt line at the foot', 'no rust, no dents'],
        variants=[dict(id='K2a', note='flat, slightly domed cap plate (BB_b: the target profile), black by default'),
                  dict(id='K2b', note='a smaller casting, low cone cap, black: K2b IS profiles_final.US02_a, whole (it was read at its own height, 0.92 m)', height=us_H,
                       profile_rz=[list(map(float, p)) for p in K2B], z_factor=round(kz_us, 4), r_factor=round(kr_us, 4),
                       cone=dict(rim_r=round(80 * kus, 1), rim_z=[round(1148 * kus, 1), round(1166 * kus, 1)], rise=round(22 * kus, 1))),
                  dict(id='K2_condition', states=['clean black semi-gloss (US02_a)', 'scuffed with chips (BB_b)', 'mid-dark grey satin (BB_b\'s paint: the one grey condition)'])])
    T['kinds']['K3'] = dict(
        name='concrete_round', title='Round precast concrete bollard (1960s to 80s)',
        basis='Judgement: no photograph of one was reached; leads only (an asset-plan row, a search summary of a 230 mm precast unit at 600 or 915 above ground, a 160 x 750 post)',
        height=850, base_diameter=250, profile_rz=[list(map(float, p)) for p in K3],
        parts=[dict(name='shaft', z0=0, z1=805, r_min=100, r_max=125, what='a tapered cylinder, r 125 to 100'),
               dict(name='top', z0=805, z1=850, r_min=0, r_max=100, what='a 20 mm chamfer into a shallow dome (rise 18)')],
        mouldings=[], edges='top arris chamfered 20, foot arris chipped', seams='two vertical mould lines 180 degrees apart, 1 mm, and a horizontal pour line at z 400 +-60',
        fixings='none', root=dict(on_flags='cast into a footing; the flags butt it; a 10 mm tarmac or mortar fillet', pivot='centre at the ground'),
        paint=dict(colour='bare concrete', srgb=[152, 150, 144], roughness_words='dry, rough', roughness=0.9, metal=0, note='never painted; no band'),
        wear=['a dark grime band to 150 mm, rain streaks below the chamfer, a darker top', 'chipped top arris with the aggregate showing', 'a rust-coloured stain 40 mm wide from a cut-off lifting eye (Judgement)'],
        variants=[dict(id='K3', note='one model; condition: clean-ish, grimy, chipped')])
    T['kinds']['K4'] = dict(
        name='steel_tube', title='Steel tube bollard with a welded cap',
        basis='Judgement: no photograph reached; a 114.3 mm tube (the asset plan\'s 60 to 114 mm), 1.0 m above ground (a search-summary lead for a round bollard 1000 high)',
        height=1000, base_diameter=114.3, profile_rz=[list(map(float, p)) for p in K4],
        parts=[dict(name='tube', z0=0, z1=982, r_min=57.15, r_max=57.15, what='a plain tube 114.3 OD'), dict(name='cap', z0=982, z1=1000, r_min=0, r_max=57.15, what='a welded dome cap, a bead of weld round its edge')],
        mouldings=[], edges='the cap is a shallow dome (rise 18) with a 2 mm weld bead', seams='a vertical weld seam up the tube (Judgement)',
        fixings='none', root=dict(on_flags='set in a concrete footing flush with the paving, a 15 mm tarmac fillet round the tube', pivot='centre at the ground'),
        paint=dict(colour='black gloss or dull galvanised', srgb_black=[24, 24, 26], srgb_galvanised=[120, 122, 124], roughness_words='gloss (black); dull sheen (galvanised)', roughness=0.4, metal=1,
                   note='black variant: metal 0 (paint); galvanised variant: metal 1; NO band, NO sleeve (reflective bands are later)'),
        wear=['scuffs and a rust bloom 100 mm high at the foot where the paint is gone', 'a dent and a scrape at 0.4 to 0.6 m', 'a lean of up to 2 degrees where a van has leant on it'],
        variants=[dict(id='K4', note='one model; black, galvanised, black with a rusted foot')])
    T['kinds']['K5'] = dict(
        name='chain_post', title='Bolted cast-iron chain post (the quay edge, ladder head and steps)',
        basis='Photo (LH_b only, a 2019 marina), the POST only: the photographed spiked chain is marina dress and is not used; scale +-6 %; period doubtful, see the sources', height=H5, base_diameter=286,
        profile_rz=[list(map(float, p)) for p in K5], parts=k5_parts,
        mouldings=[dict(name='lower_bead', z=[278, 398], r_peak=105), dict(name='upper_bead', z=[868, 926], r_peak=101), dict(name='cap_collar', z=[1000, 1075], r_peak=107)],
        edges='rounded or coved throughout', seams='none visible',
        fixings=dict(bolts=dict(count=4, pitch_circle_r=124, nut_across_flats=22, nut_height=14, stud_above_nut=14, angles_deg=[45, 135, 225, 315],
                                note='hex nuts on studs through the flange, at 45 degrees to the line of posts (Photo LH_b: two at the sides, one at the front, one hidden)'),
                     chain_eyes=dict(z=[420, 840], note='a cast D-lug on each side of the shaft at two heights, in the line of the posts; the chain\'s end link passes through it',
                                     lug=dict(height=55, proud=40, thickness=18, hole_diameter=24, hole_centre_from_shaft_face=22, error='+-30 %', basis='Photo LH_b'))),
        chain=dict(default='plain', post_spacing_m=3.0,
                   plain=dict(bar_diameter=13, link='short link', inner_length=39, inner_width=18, outer_length=65, outer_width=44, pitch=39, spikes='none',
                              note='an unrestored 1990 working quay: a plain short-link chain, a 13 mm bar (the photographed chain\'s bar reads 12, +-15 %); the link\'s inner length 3 x the bar and the outer sizes are Judgement',
                              sag_mm=150, sag_note='mid-span sag of the upper chain (Judgement: 0.15 m); two chains, at the eye heights, black, rubbed bright where the links touch'),
                   spiked_option=dict(bar_diameter=12, inner_length=55, inner_width=25, outer_length=79, outer_width=49, pitch=55, every_nth_link=2, per_link=2, spike_length=28, spike_base=8,
                                      note='the marina\'s ornamental chain as photographed (LH_b), +-15 %: an OPTION the street does not use'),
                   error='plain link sizes Judgement; photographed link sizes +-15 %'),
        root=dict(on_flags='the flange stands on resin-bound gravel (Photo) or the quay apron; the nuts stand proud', pivot='centre of the flange at the ground'),
        paint=dict(colour='black', srgb=[24, 24, 26], srgb_measured='median (17, 19, 27) with a blue sheen from the sky', roughness_words='matt to satin, chalky', roughness=0.55, metal=0,
                   note='the nuts and studs are bright steel (srgb 150, 150, 152, metal 1) with dull rust at the threads; chain black, rubbed bright where the links touch (Photo)'),
        wear=['dust on the flange, pale dry splash marks to 0.2 m', 'the chain rubbed to bright steel at the contact points of its links', 'no rust on the casting, no graffiti'],
        marks='an embossed mark about 45 mm long on the right of the shaft at z 80 to 110 (unreadable): LEAVE BLANK, no maker\'s mark',
        variants=[dict(id='K5', note='one model; with the plain chain or without; chain-eye heights 420 and 840 (+-30)')])
    T['kinds']['K6'] = dict(
        name='mooring_bollard', title='Quay mooring bollard (cast iron)',
        basis='Read for the bell pattern (the south-quay kit: 0.72 m, flange r 250, barrel r 150, head r 220); Judgement for the cannon pattern; no photograph of either was reached',
        height=720, base_diameter=500, profile_rz=[list(map(float, p)) for p in K6A],
        parts=[dict(name='flange', z0=0, z1=80, r_min=170, r_max=250, what='a round flange 40 thick then a cone to the barrel (kit)'),
               dict(name='barrel', z0=80, z1=550, r_min=130, r_max=170, what='a tapered barrel r 150 (kit)'),
               dict(name='head', z0=550, z1=720, r_min=0, r_max=220, what='a flared head r 220 that overhangs the barrel by 70, then a dome (kit); soften the kit\'s polyline corners into R10 or more')],
        mouldings=[], edges='rounded', seams='none', fixings='set in the quay masonry, 0.75 m behind the cope nose; no bolts shown',
        root=dict(on_flags='stands in a cut in the granite sett apron or the cope, a lead or mortar joint 10 mm', pivot='centre at the apron level'),
        paint=dict(colour='black, worn', srgb=[26, 26, 28], roughness_words='scuffed, dull', roughness=0.6, metal=0, note='the kit\'s iron_black'),
        wear=['rope wear: a bright groove polished into the barrel at z 480 to 520 (Judgement)', 'paint gone to rust-brown on the head\'s upper rim and the flange', 'dents and chips'],
        variants=[dict(id='K6a', note='bell bollard (the kit profile)'),
                  dict(id='K6b', note='upturned cannon barrel (Charlestown lead: a quay with one), Judgement: a barrel with reinforcing rings, a muzzle swell to r 172 with a flat muzzle face at z 914, and a ball of radius 105 (centre z 877) standing 68 above the face, 982 high',
                       profile_rz=[list(map(float, p)) for p in K6B], height=982, ball=dict(radius=105, centre_z=877, standing_above_face=68, muzzle_face_z=914, muzzle_r=172))])
    T['kinds']['K7'] = dict(
        name='cleat', title='Horn cleat (quay or jetty)', basis='Judgement: no photograph reached', length=400, width=110, height=126,
        elevation_half_xz=[list(map(float, p)) for p in CLEAT_HALF],
        plan=dict(base=dict(length=400, width=110, end_radius=55, thickness=22, note='a base plate 400 x 110 with its ends rounded R55, two 16 mm bolts 300 apart (nut across flats 24)'),
                  pedestal=dict(length=96, width=124, note='96 along x 124 across at its foot, with rounded ends, 48 high; its section narrows upward'),
                  horns=dict(section='round', diameter_at_pedestal=32, diameter_at_tips=22, tip_height=126, note='round-section horns tapering from 32 to 22, the tips curving up to 126 above the base')),
        parts=[dict(name='base', note='400 x 110 x 22, ends R55, two 16 mm bolts (nut across flats 24) 300 apart'), dict(name='pedestal', note='96 x 124 at its foot, rounded ends, 48 high'),
               dict(name='horns', note='round section, 32 at the pedestal to 22 at the tips, the tips curving up to 126 above the base')],
        paint=dict(colour='black or bare iron', srgb=[26, 26, 28], roughness=0.6, metal=0), wear=['rope polish on the underside of the horns, rust at the bolts'], variants=[dict(id='K7', note='one model')])

    for kk, KK in T['kinds'].items():
        KK.setdefault('marks', 'none: plain castings, no maker, no council, no crest, no monogram, no lettering, no band')
    T['placements'] = dict(
        rule=('Bollards stand 0.5 m behind the kerb face (axis), on the footway, where a vehicle could mount it: at the two corners of a yard mouth, either side of a side passage, at the '
              'chandler\'s front, at the junction\'s kerb returns, and along the quay edge. Never in front of a door, a lamp column, a drain or the crossover. The frame is the street recipe\'s '
              '(x along, 0 at the street\'s south end, + north; y or z across, east positive), in metres.'),
        why_four_kinds=('The asset plan\'s "one design to a street" holds for each owner, not for the street: K1 is the council\'s cast stock (the yard mouth), K3 older council precast stock (the side passage), '
                        'K4 the chandler\'s own private posts, K2 the Harbour Board\'s at its approach (the junction); a harbour street has several owners.'),
        street_proper=[
            dict(id='yard_mouth', kind='K1', count=2, side='west', x_m=[20.7, 24.3], axis_from_kerb_face_m=0.5, z_m=-3.5, guards='the two corners of the yard mouth (the 3.0 m crossover, x 21.0 to 24.0)',
                 basis='Read: the scene file already places them (vignette-pieces E5); Photo: US01_b shows the pattern at a corner, BGE_a at a path'),
            dict(id='side_passage', kind='K3', count=2, side='east', x_m=[38.8, 40.2], axis_from_kerb_face_m=0.5, z_m=3.5,
                 guards='either side of the mouth of the 1.0 m passage between the parade and the chandler (x 39 to 40), the path to the yard and steps behind, so a car cannot nose onto the footway there',
                 basis='Judgement: the plain precast posts the clutter research names at terrace corners; no photograph'),
            dict(id='chandler_front', kind='K4', count=2, side='east', x_m=[42.5, 44.0], axis_from_kerb_face_m=0.45, z_m=3.45, guards='anti-parking posts at the chandler\'s front (the chandler\'s own private posts); the first stands 2.30 m in plan from the chandler\'s door centre (x 44.203), so the east side\'s posts read as two groups (K3 at 38.8 and 40.2, K4 at 42.5 and 44.0)',
                 basis='Judgement: a shop front\'s own posts; no photograph')],
        junction=dict(id='junction_corners', kind='K2', count=4, axis_from_kerb_face_m=0.5, points=kit_junction(),
                      rule=('the two tangent points of the 8 m return (inside Quay Street\'s turn west) and the two of the 6 m return (the Harbour Board approach), each moved 0.5 m from the kerb face '
                            'along the footway normal; none on the 12 m outside return. The four (x, y) are what the south-quay kit\'s Junction builder computes (self_check.py recomputes them).'),
                      basis='Judgement for the places; Derived for the coordinates'),
        quay=[dict(id='quay_edge', kind='K6', count=10, basis='Read: the south-quay kit\'s BOLLARDS (recipe frame, metres); K6b (the cannon) at the three quay ends, Judgement',
                   places=[dict(x_m=-69.25, y_m=-88.0, model='K6b', where='north quay, west end'), dict(x_m=-69.25, y_m=-58.0, model='K6a', where='north quay'),
                           dict(x_m=-69.25, y_m=-28.0, model='K6a', where='north quay'), dict(x_m=-69.25, y_m=2.0, model='K6a', where='north quay'),
                           dict(x_m=-69.25, y_m=30.0, model='K6b', where='north quay, east end'),
                           dict(x_m=-110.75, y_m=-80.0, model='K6a', where='jetty, 0.75 m behind its cope'), dict(x_m=-110.75, y_m=-45.0, model='K6a', where='jetty'),
                           dict(x_m=-95.0, y_m=40.75, model='K6a', where='east quay'), dict(x_m=-115.0, y_m=40.75, model='K6a', where='east quay'),
                           dict(x_m=-140.0, y_m=40.75, model='K6b', where='east quay, far end')]),
              dict(id='ladder_head', kind='K5', count=4, x_m=-69.5, y_m=[-40.5, -37.5, -34.5, -31.5], behind_cope_nose_m=0.5, post_spacing_m=3.0,
                   chains=[[-40.5, -37.5], [-34.5, -31.5]], open_gap_m=[-37.5, -34.5],
                   basis='Judgement: four posts at the north quay\'s ladder (y -36), a plain chain between the outer pairs only, the 3.0 m over the ladder left open so a person can climb out'),
              dict(id='cleats', kind='K7', count=3, x_m=-110.25, y_m=[-64.0, -58.0, -52.0], axis='long axis along y', behind_cope_nose_m=0.25,
                   basis='Judgement: on the jetty\'s granite cope, 0.25 m behind its nose (x -110.0), beside the jetty boat\'s berth (y -63 to -53); the kit has no timber fender, a real fixing is the stone cope')],
        counts=dict(street_proper=6, junction=4, street_and_junction=10, quay_K6=10, quay_K5=4, quay_K7=3),
        by_kind=dict(K1=2, K2=4, K3=2, K4=2, K5=4, K6=10, K7=3),
        clearances=dict(from_door_centre_m=1.2, from_lamp_column_m=1.5, from_crossover_edge_m=0.25, from_other_furniture_m=0.6, footway_clear_min_m=1.2))
    T['variants'] = dict(
        rule='two to four models a kind at most; the town\'s council fits one design to a street, so repeats are true; variety is age and condition (the asset plan)',
        models=dict(K1=1, K2=2, K3=1, K4=1, K5=1, K6=2, K7=1), conditions_per_model=3,
        seeds=dict(lean_deg=[0, 2.0], lean_note='Photo: 0.2 to 1.0 degree in the viewing plane on five bollards, inside the panoramas\' own tilt error; the asset plan\'s 1 to 3 degrees is the rule; 2 is the cap here',
                   paint_fade=[0, 1], dirt_height_mm=[80, 600], rust=[0, 1], chips=[0, 12], foot_paint_loss_height_mm=[0, 120], dents=[0, 2]))
    T['materials'] = {
        'iron_black_gloss': dict(srgb=[24, 24, 26], roughness=0.35, metal=0, use='K1, K2 (the default paint, both caps)'),
        'iron_grey_satin': dict(srgb=[88, 89, 91], roughness=0.5, metal=0, use='K2: the one grey condition (BB_b\'s paint)'),
        'iron_black_matt': dict(srgb=[24, 24, 26], roughness=0.55, metal=0, use='K5, K6'),
        'bare_iron_foot': dict(srgb=[64, 58, 52], roughness=0.7, metal=0, use='paint loss at the foot of K1 (Photo BGE_a: median 4.5 times the painted body\'s lightness)'),
        'concrete_grey': dict(srgb=[152, 150, 144], roughness=0.9, metal=0, use='K3'),
        'galvanised': dict(srgb=[120, 122, 124], roughness=0.5, metal=1, use='K4 variant'),
        'rust': dict(srgb=[110, 60, 32], roughness=0.85, metal=0, use='rust blooms'),
        'bright_steel': dict(srgb=[150, 150, 152], roughness=0.4, metal=1, use='K5 nuts, studs')}
    T['kerb_frame'] = dict(
        kerb_face_line='y = 0 (the kerbs target\'s plan frame: the foot of the face at the channel); the axis stands at y = -500 mm toward the footway',
        pivot_z='footway flag top, +120 mm above the channel top; the kerb top is +125 (granite)',
        existing_stand_in='0.765 m high, r 108 (the street recipe\'s cannon-and-ball clutter bollard); the held decorative_bollard_02 is 1.008 m high, 0.201 across')
    T['could_not_settle'] = [
        'The camera heights (1.0 to 1.22 m, per panorama) rest on brick gauge, line width and paver size; every length is +-6 to +-10 % until a photograph with a measuring scale in the plane is reached.',
        'Whether any of these bollards stood in a 1990 British street: every photograph is from 2019 or later. K1\'s and K2\'s patterns (a plinth, taper, bead and domed or flat cap) are the long-lived cast pattern; the borough of K1 and K2 is not known.',
        'Concrete (K3), steel tube (K4), mooring bollards (K6), cleats (K7): no photograph reached; their numbers are the kit\'s, the asset plan\'s or judgement.',
        'Whether a chain post (K5) belongs on a 1990 quay: the LH_b post is on a marina built in the 1980s to 1990s.',
        'Casting marks: none is shown on K1 or K2; K5 has one unreadable embossed mark near the foot, left blank.']
    T['to_read_when_the_network_opens'] = [
        'Wikimedia Commons: Category Bollards in the United Kingdom, and its cannon, mooring and concrete subcategories (1975 to 2000 photographs with the author and date on the file page)',
        'Geograph: 1980s and 1990s squares of dock and harbour towns with cast bollards, cleats and concrete posts (CC BY-SA, the date taken on each page)',
        'Historic England list entries 1202530 (Bristol, Floating Harbour quay wall and bollards, 1893), 1272267 (Docks 1 to 6 quay walls and bollards) and the Kent and Derbyshire HER pages for cannon bollards',
        'The Bristol Industrial Archaeological Society\'s Journal 3, Grahame Farr\'s 1970 paper on the quay bollards (types with sizes)',
        'BS 7263 and the Traffic Signs Manual chapter 3 on bollards and their set-backs; a 1980s highways standard detail for a precast and a cast bollard',
        'The Hook sheet\'s own bollard, if it has one, at full size, and the street recipe\'s clutter bollard\'s reference photographs']
    T['checks'] = make_checks(T)
    return T


def make_checks(T):
    K = T['kinds']
    C = []
    def add(name, applies, measure, expected, tol, kind):
        C.append(dict(name=name, applies_to=applies, measure=measure, expected=expected, tolerance=tol, kind=kind))
    P1 = K['K1']['profile_rz']; P2 = K['K2']['profile_rz']; P5 = K['K5']['profile_rz']
    d1 = lambda z: round(2 * float(L.r_of_z(P1, [z])[0]), 1)
    d2 = lambda z: round(2 * float(L.r_of_z(P2, [z])[0]), 1)
    d5 = lambda z: round(2 * float(L.r_of_z(P5, [z])[0]), 1)
    f1 = T['calibration']['panoramas']['urban_street_01']['h_cam'] / 1.15
    f2 = T['calibration']['panoramas']['birbeck_street_underpass']['h_cam'] / 1.15
    zr = lambda P, a, b: round(float(max(((r, z) for r, z in P if a <= z <= b))[1]), 1)       # z of the largest r in a range
    kp = 'Photo (scale +-6 %)'
    H1 = K['K1']['height']; H2 = K['K2']['height']
    # K1
    add('K1_height', 'K1', 'z of the top of the dome above the foot', H1, 50, 'Photo US01_b %.0f at its bed level (1.195 +-0.07 m); BGE_a, a second casting, 1014' % H1)
    add('K1_base_diameter', 'K1', 'diameter of the plinth at z 60', d1(60), 14, kp)
    add('K1_plinth_top_z', 'K1', 'z where the plinth stops and the shoulder begins', round(116 * f1, 1), 20, 'Photo US01_b; BGE_a (second casting) about 140')
    add('K1_shaft_diameter_z300', 'K1', 'diameter at z 300', d1(300), 10, kp)
    add('K1_shaft_diameter_z800', 'K1', 'diameter at z 800', d1(800), 10, kp)
    add('K1_taper', 'K1', 'dr/dz of the shaft between z 140 and 490 (a straight taper)', -0.0279, 0.008, 'Photo US01_b; BGE_a -0.0258')
    add('K1_collar_max_diameter', 'K1', 'largest diameter of the bead', round(2 * feature(P1, 490 * f1, 565 * f1)[1], 1), 10, kp)
    add('K1_collar_centre_z', 'K1', 'z of the bead\'s fullest point', zr(P1, 493 * f1, 557 * f1), 30, 'Photo US01_b 0.506 H; BGE_a 0.53 H')
    add('K1_collar_height', 'K1', 'z extent of the bead', round(64 * f1, 1), 12, 'Photo US01_b')
    add('K1_neck_diameter', 'K1', 'diameter at z %.0f' % (935 * f1), d1(935 * f1), 8, kp)
    add('K1_cap_collar_max_diameter', 'K1', 'largest diameter of the cap collar', round(2 * feature(P1, 940 * f1, 970 * f1)[1], 1), 8, kp)
    add('K1_cap_collar_z', 'K1', 'z of the cap collar\'s fullest point', zr(P1, 940 * f1, 970 * f1), 15, kp)
    add('K1_dome_foot_diameter', 'K1', 'diameter of the dome at its foot (z %.0f)' % (1000 * f1), d1(1000 * f1), 8, kp)
    add('K1_dome_rise', 'K1', 'height of the dome above its foot', round(53 * f1, 1), 8, kp)
    add('K1_silhouette_deviation', 'K1', 'largest radial distance between the built outline and profile_rz at the same z', 0, 6, 'the whole elevation, 5 mm a pixel photographs')
    add('K1_lean_seed', 'K1 and all rooted kinds', 'rotation of an instance about its pivot', [0, 2.0], 0.1, 'Photo 0.2 to 1.0 degree in the viewing plane; asset plan 1 to 3; cap 2')
    add('K1_paint_albedo', 'K1', 'base colour of the painted metal, sRGB', [24, 24, 26], 10, 'Photo (median 10 to 38 across four tone-mapped panoramas)')
    add('K1_paint_roughness', 'K1', 'roughness of the paint', 0.35, 0.15, 'Photo (the sky shows in the dome and the bead)')
    add('K1_foot_paint_loss', 'K1 worn-foot condition ONLY (not every instance)', 'share of the plinth\'s lower 110 mm bare (exposed iron material), speckled', [0.6, 0.7], 0.1, 'Photo BGE_a')
    add('K1_no_band_no_mark', 'K1, K2, K3, K4, K5, K6, K7', 'no white, yellow or reflective band material, no lettering, no crest, no monogram, no maker\'s mark on any mesh or texture', 0, 0, 'canon, the brief; no photograph shows a band')
    # K2
    ring2 = feature(P2, 0, 50)[1]
    add('K2_height', 'K2a', 'z of the top of the cap', H2, 60, 'Photo BB_b %.0f at its footway (1.085 +-0.06 m)' % H2)
    add('K2_foot_ring_diameter', 'K2a', 'largest diameter of the rolled foot ring', round(2 * ring2, 1), 18, kp)
    add('K2_shaft_diameter_z300', 'K2a', 'diameter at z 300', d2(300), 12, kp)
    add('K2_shaft_diameter_z900', 'K2a', 'diameter at z 900', d2(900), 10, kp)
    add('K2_collar_z_over_height', 'K2a and K2b', 'z of the collar band\'s middle divided by the height', 0.59, 0.03, 'Photo BB_b 0.587; US02_a 0.592')
    add('K2_collar_proud', 'K2a', 'radial projection of the collar band beyond the taper', 7, 4, 'Photo (7 +-4; the profile has %.1f)' % (feature(P2, 635 * f2, 672 * f2)[1] - feature(P2, 635 * f2, 635 * f2)[1]))
    add('K2_cap_overhang', 'K2a', 'radial overhang of the cap plate beyond the shaft under it', 5, 4, 'Photo BB_b (5 +-4; the profile has %.1f)' % (feature(P2, 1092 * f2, 1104 * f2)[1] - feature(P2, 1088 * f2, 1088 * f2)[1]))
    add('K2_silhouette_deviation', 'K2a', 'largest radial distance between the built outline and profile_rz at the same z', 0, 7, 'photographs')
    add('K2_paint_albedo', 'K2', 'base colour, sRGB (black default / the grey condition)', [[24, 24, 26], [88, 89, 91]], 10, 'Photo (black: US02_a; grey is Judgement-neutralised from a warm-lit measurement)')
    v2b = [v for v in K['K2']['variants'] if v['id'] == 'K2b'][0]
    add('K2b_height', 'K2b', 'z of the apex of the cone cap', round(v2b['height'], 1), 50, 'Photo US02_a at its own footway (0.92 +-0.04 m): a smaller casting than K2a')
    add('K2b_cone_cap', 'K2b', 'cap rim radius and the rise of the low cone above the rim', [v2b['cone']['rim_r'], v2b['cone']['rise']], [6, 6], 'Photo US02_a (rim r 80 and rise 22 at the 1.15 reading, x 0.80)')
    add('K2b_foot_ring_diameter', 'K2b', 'largest diameter of the rolled foot ring', round(2 * max(r for r, z in v2b['profile_rz'] if z <= 50), 1), 18, 'Photo US02_a')
    # K5
    add('K5_height', 'K5', 'z of the top of the dome', K['K5']['height'], 40, 'Photo LH_b (scale +-6 %)')
    add('K5_flange_diameter', 'K5', 'diameter of the flange', 286, 16, kp)
    add('K5_flange_thickness', 'K5', 'height of the flange rim', 36, 8, kp)
    add('K5_shaft_diameter_z600', 'K5', 'diameter at z 600', d5(600), 10, kp)
    add('K5_lower_bead', 'K5', 'largest diameter of the lower bead and its z centre', [210, 330], [10, 30], kp)
    add('K5_upper_bead', 'K5', 'largest diameter of the upper bead and its z centre', [202, 892], [10, 30], kp)
    add('K5_cap_collar_max_diameter', 'K5', 'largest diameter of the cap collar', 214, 10, kp)
    add('K5_bolts', 'K5', 'number of bolts, pitch-circle radius, nut across flats', [4, 124, 22], [0, 8, 4], 'Photo LH_b')
    add('K5_chain_eyes_z', 'K5', 'z of the two chain eyes', [420, 840], 30, 'Photo LH_b')
    add('K5_chain_eye_lug', 'K5', 'the D-lug: height, proud of the shaft, thickness, hole diameter', [55, 40, 18, 24], [17, 12, 6, 7], 'Photo LH_b (+-30 %)')
    add('K5_chain_plain', 'K5 on the street\'s quay', 'chain bar diameter, link outer length (a plain short link), post spacing (m); NO spikes', [13, 65, 3.0], [3, 10, 0.3], 'Judgement (an unrestored working quay); the photographed marina chain is spiked and is not used')
    add('K5_blank', 'K5', 'the embossed mark near the foot is not copied: the shaft is smooth', 0, 0, 'the brief')
    # K6
    add('K6a_dimensions', 'K6a', 'height, flange diameter, barrel diameter, head diameter', [720, 500, 300, 440], [80, 40, 30, 40], 'Read (the south-quay kit); Judgement')
    add('K6a_head_overhang', 'K6a', 'radial overhang of the head beyond the barrel under it', 70, 15, 'Read (the kit: head r 220, barrel r 150)')
    v6b = [v for v in K['K6']['variants'] if v['id'] == 'K6b'][0]
    add('K6b_height', 'K6b', 'z of the top of the ball', v6b['height'], 40, 'Judgement (an upturned cannon, a Charlestown lead)')
    add('K6b_ball', 'K6b', 'ball radius and how far it stands above the muzzle face', [105, 68], [15, 15], 'Judgement')
    add('K6b_muzzle_swell', 'K6b', 'muzzle swell radius and the z of the flat muzzle face', [172, 914], [15, 15], 'Judgement')
    # placements
    pl = T['placements']
    add('street_bollards_by_kind', 'street x 0 to 48', 'count of K1, K3, K4 on the street proper', [2, 2, 2], 0, 'Read (K1: the scene file) and Judgement')
    add('street_total_with_junction', 'street and its junction', 'count of all bollards in x -36 to 48', 10, 0, 'asset plan: 6 to 10 on the street')
    add('axis_from_kerb_face_mm', 'street K1 to K4', 'distance from the kerb face to the axis', 500, 100, 'Read (the scene file 0.5 m); Photo 0.33, 0.93 and 0.91 m on kerb-side bollards')
    add('footway_clear_min_m', 'every street bollard', 'clear width between the base and the building line (footway 2.0 m)', 1.2, 0, 'Judgement (a wheelchair needs 1.0)')
    add('clear_of_crossover', 'K1 at the yard mouth', 'distance from the crossover edge (x 21.0 and 24.0)', 0.3, 0.1, 'Read')
    add('clear_of_doors_m', 'east and west bollards', 'distance in plan from the axis to any shop door or side door centre (taken on the building line, z +-5.0)', 1.2, 0, 'the shopfronts target door centres')
    add('junction_posts_xy', 'K2 at the junction', 'the four (x, y) of the posts (metres, the recipe frame)', [[p['x_m'], p['y_m']] for p in pl['junction']['points']], 0.05, 'Derived from the south-quay kit\'s Junction: tangent points of the 8 m and 6 m returns + 0.5 m along the footway normal')
    q = {e['id']: e for e in pl['quay']}
    add('quay_K6_xy', 'K6', 'the ten (x, y) of the bollards, five on the north quay, two on the jetty, three on the east quay; K6b at (-69.25,-88), (-69.25,30), (-140,40.75)', [[p['x_m'], p['y_m']] for p in q['quay_edge']['places']], 0.01, 'Read (the south-quay kit BOLLARDS)')
    add('quay_K5_xy', 'K5', 'posts at x -69.5, y -40.5, -37.5, -34.5, -31.5; chains only between (-40.5,-37.5) and (-34.5,-31.5); the 3.0 m over the ladder (y -36) open', [q['ladder_head']['x_m'], q['ladder_head']['y_m']], 0.01, 'Judgement on the kit\'s LADDER_Y')
    add('quay_K7_xy', 'K7', 'cleats at x -110.25, y -64, -58, -52, long axis along y, on the jetty\'s granite cope', [q['cleats']['x_m'], q['cleats']['y_m']], 0.01, 'Judgement on the kit\'s jetty (x -130 to -110) and its boat (y -63 to -53)')
    add('quay_set_back_m', 'K6 on the north quay', 'axis behind the cope nose', 0.75, 0.1, 'Read (the south-quay kit)')
    add('quay_counts', 'the quay', 'K6, K5, K7', [10, 4, 3], 0, 'Read (K6); Judgement')
    # judgement kinds
    add('K3_dimensions', 'K3', 'height, foot diameter, top diameter', [850, 250, 200], [100, 30, 30], 'Judgement (leads: 600 or 915 above ground, 230 mm; 160 x 750)')
    add('K4_dimensions', 'K4', 'height, tube diameter', [1000, 114.3], [100, 8], 'Judgement (the asset plan\'s 60 to 114 mm tube)')
    add('K7_dimensions', 'K7', 'length, width, height, base end radius', [400, 110, 126, 55], [60, 20, 20, 5], 'Judgement')
    add('material_paint_values', 'all', 'metal 0 for painted iron and concrete; metal 1 only for galvanised steel and bright nuts', 1, 0, 'target.json materials')
    return C


if __name__ == '__main__':
    T = build()
    old = os.path.join(HERE, 'target.json')
    if os.path.exists(old):
        try:
            prev = json.load(open(old))
            for k in ('checks', 'self_check'):
                if k in prev and k not in T:
                    T[k] = prev[k]
        except Exception:
            pass
    json.dump(T, open(old, 'w'), indent=1)
    print('target.json written;', {k: round(max(z for r, z in T['profiles_final'][k]), 1) for k in T['profiles_final']})
