#!/usr/bin/env python
"""Builds target.json from litter_data.py and photo_measurements.json (run measure.py first).

    /home/user/.bpyenv/bin/python -I make_target.py
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from shapely.geometry import Polygon
import litter_data as D

HERE = os.path.dirname(os.path.abspath(__file__))
PM = json.load(open(os.path.join(HERE, 'photo_measurements.json')))
TEX = PM['textures']


def tex_srgb(tid):
    return TEX[tid]['median']


def revolve_volume(profile_rz, z0=None, z1=None):
    """volume (mm3) of the solid of revolution of an (r, z) outline closed on the axis"""
    P = np.array(profile_rz, float)
    poly = Polygon(list(map(tuple, P)) + [(0, P[-1][1]), (0, P[0][1])]) if P[0][0] == 0 else Polygon(P)
    return 2 * math.pi * poly.centroid.x * poly.area


def lathe_extent(profile_rz):
    P = np.array(profile_rz, float)
    return dict(r_max=float(P[:, 0].max()), z_min=float(P[:, 1].min()), z_max=float(P[:, 1].max()))


def build():
    T = {}
    T['family'] = 'litter-bins'
    T['title'] = 'Quay Street litter bins and the household dustbin: the target (cloud week 42, 9 October 2026)'
    T['written'] = '2026-10-09'
    T['units'] = 'millimetres unless a key ends _m (metres); angles in degrees; the .glb is metres, z up, scale 1'
    T['summary_line'] = ('Quay Street had three council bins in 1990, not eleven: two steel pole-mounted open bins (K1, 45 litres, rim at 1.05 m, hung on their own 76 mm posts, at x 6.6 and x 35.2 east) '
                         'and one free-standing hooded glass-fibre drum (K2, 900 high, at x 44.0 west by the newsagent and the bus stop), all council green and marked only LITTER, plus the scene\'s two galvanised '
                         'dustbins (D1, 0.46 across, 0.61 high, lid 0.50 x 0.05, at x 21.4 and 22.0 east); no photograph of a period bin was reached, so every bin shape is research and judgement, and the '
                         'only photographs measured are one galvanised steel container and the material scans.')
    T['frame'] = dict(
        profile='(r, z): r the radius from the part\'s own axis, z up from the flag top at the piece\'s pivot; each lathe outline runs round the part and closes on the axis; elevation polygons mirror it about the axis',
        pivot='K1: the post axis on the footway flag top; K2 and D1: the base centre on the flag top. The flag top is the kerbs target\'s +110 above the channel top. z up, +x as each kind says',
        axes=dict(K1='+x from the post axis toward the bin\'s axis (216 away); the lettering faces +y (the building side); the buried part of the post (0.3 m, not modelled) is below z = 0',
                  K2='+x is the aperture\'s side (azimuth 0); the lock is at azimuth 180',
                  D1='the two side handles stand at +y and -y; the lid\'s handle runs along x'),
        street='x along the street from the south (quay) end, z across from the crown, east +, metres; kerb face |z| 3.0, kerb back |z| 3.17 (kerbs target, granite; the scene\'s earlier 3.125), building line |z| 5.125, stallriser face |z| 4.975',
        glb='metres, z up, scale 1, forward -Z as production/specs/asset-interface.md says; one mesh per kind and condition; the liner, the lid, the sacks and every dressing piece are separate meshes of the same piece; NO text and no decal carries any word except LITTER (and the optional digits of the asset stencil)')
    # -------------------------------------------------------------------------------------------------------------------------- numbers (Read ones are re-read by self_check.py)
    T['scene_numbers'] = [
        dict(id='street_length_m', value=48.0, file='production/specs/vignette-scene.json', path='street.length_m'),
        dict(id='kerb_face_z_m', value=3.0, file='production/specs/vignette-scene.json', path='street.carriageway.half_width_m'),
        dict(id='footway_width_m', value=2.0, file='production/specs/vignette-scene.json', path='street.footway.width_m'),
        dict(id='dustbin_x_m', value=21.4, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].x_m'),
        dict(id='dustbin_count', value=2, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].count'),
        dict(id='dustbin_spacing_m', value=0.6, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].spacing_m'),
        dict(id='dustbin_setback_m', value=1.6, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].setback_from_kerb_m'),
        dict(id='dustbin_body_d_m', value=0.46, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].body_diameter_m'),
        dict(id='dustbin_body_h_m', value=0.61, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].body_height_m'),
        dict(id='dustbin_lid_d_m', value=0.5, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].lid_diameter_m'),
        dict(id='dustbin_lid_h_m', value=0.05, file='production/specs/vignette-scene.json', path='furniture[bom=E13_household_dustbin].lid_height_m'),
        dict(id='kiosk_x_m', value=16.5, file='production/specs/vignette-scene.json', path='furniture[bom=E3_telephone_kiosk].x_m'),
        dict(id='kiosk_setback_m', value=0.55, file='production/specs/vignette-scene.json', path='furniture[bom=E3_telephone_kiosk].setback_from_kerb_m'),
        dict(id='kiosk_plan_m', value=0.914, file='production/specs/vignette-scene.json', path='furniture[bom=E3_telephone_kiosk].plan_m'),
        dict(id='pillar_box_x_m', value=27.0, file='production/specs/vignette-scene.json', path='furniture[bom=E4_pillar_box].x_m'),
        dict(id='pillar_box_setback_m', value=0.6, file='production/specs/vignette-scene.json', path='furniture[bom=E4_pillar_box].setback_from_kerb_m'),
        dict(id='pillar_box_cap_d_m', value=0.66, file='production/specs/vignette-scene.json', path='furniture[bom=E4_pillar_box].cap_diameter_m'),
        dict(id='railing_x_m', value=10.0, file='production/specs/vignette-scene.json', path='furniture[bom=E8_guard_railing].x_m'),
        dict(id='railing_panel_m', value=2.0, file='production/specs/vignette-scene.json', path='furniture[bom=E8_guard_railing].panel_length_m'),
        dict(id='railing_setback_m', value=0.25, file='production/specs/vignette-scene.json', path='furniture[bom=E8_guard_railing].setback_from_kerb_m'),
    ]
    T['other_target_numbers'] = [
        dict(id='lamp_LC1_x_m', value=8.0, file='production/cloud-week/targets/lamp-posts/target.json', path='placement.columns[id=LC 1].x_m'),
        dict(id='lamp_LC1_z_m', value=3.77, file='production/cloud-week/targets/lamp-posts/target.json', path='placement.columns[id=LC 1].corrected_z_m'),
        dict(id='lamp_LC2_x_m', value=18.0, file='production/cloud-week/targets/lamp-posts/target.json', path='placement.columns[id=LC 2].x_m'),
        dict(id='lamp_LC3_x_m', value=28.0, file='production/cloud-week/targets/lamp-posts/target.json', path='placement.columns[id=LC 3].x_m'),
        dict(id='lamp_LC4_x_m', value=38.0, file='production/cloud-week/targets/lamp-posts/target.json', path='placement.columns[id=LC 4].x_m'),
        dict(id='door_mickeys_shop_x_m', value=4.797, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=mickeys].centres_street_x_m.shop_door'),
        dict(id='door_mickeys_side_x_m', value=3.822, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=mickeys].centres_street_x_m.side_door'),
        dict(id='door_fish_shop_x_m', value=10.797, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=fish_market].centres_street_x_m.shop_door'),
        dict(id='door_ritas_shop_x_m', value=19.203, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=ritas].centres_street_x_m.shop_door'),
        dict(id='door_empty_side_x_m', value=21.822, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=empty_unit].centres_street_x_m.side_door'),
        dict(id='door_empty_shop_x_m', value=22.797, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=empty_unit].centres_street_x_m.shop_door'),
        dict(id='door_laundry_side_x_m', value=32.178, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=steam_laundry].centres_street_x_m.side_door'),
        dict(id='door_laundry_shop_x_m', value=31.203, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=steam_laundry].centres_street_x_m.shop_door'),
        dict(id='door_grocer_shop_x_m', value=38.147, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=grocer].centres_street_x_m.shop_door'),
        dict(id='door_chandler_shop_x_m', value=44.203, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=chandler].centres_street_x_m.shop_door'),
        dict(id='door_tea_shop_x_m', value=25.797, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=tea_rooms].centres_street_x_m.shop_door'),
        dict(id='door_iron_shop_x_m', value=34.203, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=ironmonger].centres_street_x_m.shop_door'),
        dict(id='door_news_shop_x_m', value=40.203, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=newsagent].centres_street_x_m.shop_door'),
        dict(id='door_news_side_x_m', value=41.178, file='production/cloud-week/targets/shopfronts/target.json', path='shops[id=newsagent].centres_street_x_m.side_door'),
        dict(id='bollard_east_K3_x1_m', value=38.8, file='production/cloud-week/targets/bollards/target.json', path='placements.street_proper[id=side_passage].x_m[0]'),
        dict(id='bollard_east_K4_x1_m', value=42.5, file='production/cloud-week/targets/bollards/target.json', path='placements.street_proper[id=chandler_front].x_m[0]'),
        dict(id='bollard_east_K4_x2_m', value=44.0, file='production/cloud-week/targets/bollards/target.json', path='placements.street_proper[id=chandler_front].x_m[1]'),
        dict(id='bollard_west_yard_x1_m', value=20.7, file='production/cloud-week/targets/bollards/target.json', path='placements.street_proper[id=yard_mouth].x_m[0]'),
        dict(id='bollard_west_yard_x2_m', value=24.3, file='production/cloud-week/targets/bollards/target.json', path='placements.street_proper[id=yard_mouth].x_m[1]'),
        dict(id='kerb_top_width_mm', value=170, file='production/cloud-week/targets/kerbs-and-covers/target.json', path='pieces.granite_kerb.top_width', optional=True),
    ]
    T['hook_cast_numbers'] = [dict(id='bus_stop_x_m', value=46.0, file='production/specs/hook-cast.json', path='bus_stop.x_m'), dict(id='bus_stop_z_m', value=-4.3, file='production/specs/hook-cast.json', path='bus_stop.z_m')]
    # -------------------------------------------------------------------------------------------------------------------------- photographs and models
    T['calibration'] = dict(
        method='the horizon (brick-course) method of this week\'s bollards writer, re-run here on its two urban_street_02 anchors: in a levelled equirectangular panorama the horizon is the middle row; the courses of a 75 mm-gauge brick wall are evenly spaced in tan(angle below the horizon); camera height above the wall foot = 75 mm x tan(foot angle) / (course pitch in tan units)',
        horizon_anchors=PM['horizon_anchors'], camera_height=PM['camera_height'],
        note='no panorama is at 1.6 m: urban_street_02 is at 0.92 m above its footway and 1.04 m above the road where the container stands. Every length read on it is +-5 % at best. NO bin of the target is measured on a photograph, so no length of any bin rests on this height; it serves only the scale overlay of section 6 and the container\'s colour')
    T['photo_measurements'] = dict(container=PM['container'], textures=TEX, models=PM['models'], held_bins=PM['held_bins'])
    # -------------------------------------------------------------------------------------------------------------------------- materials
    mats = {}
    for k, v in D.MATERIALS.items():
        m = dict(v)
        if m.get('srgb') is None:
            m['srgb'] = tex_srgb(m['tex']); m['p10'] = TEX[m['tex']]['p10']; m['p90'] = TEX[m['tex']]['p90']
        mats[k] = m
    T['materials'] = mats
    # -------------------------------------------------------------------------------------------------------------------------- kinds
    k1_bin = D.k1_bin_outer()

    # capacity: inner frustum from the floor (z 553) to the rim underside (z 1040): r_in = r_out - wall
    r0 = D.K1_R_BASE - D.K1_WALL; r1 = D.K1_R_TOP - D.K1_WALL; h = 1040.0 - 553.0
    cap_l = math.pi * h / 3 * (r0 * r0 + r0 * r1 + r1 * r1) / 1e6
    K1 = dict(
        name='pole_open_steel', title='Pole-mounted open-top steel litter bin on its own 76 mm post (the street-clutter research\'s (a))',
        basis='JUDGEMENT AND LEADS: no photograph of a period pole bin was reached. The type is the asset plan\'s "pole-mounted open bin" and the clutter research\'s first candidate; its size is a 50-litre-class bin (Lead: a council review found pole bins to hold about 50 litres), the repository\'s own script bin (round, 0.40 across, rim 0.95) corrected by the leads; every number is Judgement unless marked',
        pivot='the post axis on the flag top', placed=True,
        post=dict(type='tube', od=2 * D.K1_POST_R, wall=3.2, height=D.K1_POST_TOP, profile_rz=D.k1_post_profile(),
                  cap='a pressed steel cap 80 across, 25 high, its top domed 4 mm, fitted with a dab of bitumen, painted with the post',
                  root='set in 0.3 m of concrete; the flag is cut round it with a 10 to 15 mm dark bitumen-and-grit joint; no flange, no collar',
                  kind='Judgement (the trade\'s 3-inch tube, 76.1 x 3.2; the repository\'s script post is also 76 mm)'),
        bin=dict(axis_offset_x=D.K1_BIN_OFFSET, z_base=D.K1_BIN_Z0, z_rim_top=D.K1_RIM_TOP, wall=D.K1_WALL, outer_profile_rz=k1_bin, wall_section_rz=D.k1_wall_section(),
                 r_base=D.K1_R_BASE, r_top=D.K1_R_TOP, rim_bead=dict(diameter=9.0, centre_r=182.0, centre_z=1046.0, note='the sheet rolled outward over a 4 mm wire; no sharp edge'),
                 base_plate=dict(thickness=3.0, turned_up_edge=6.0, drain_holes=dict(count=4, diameter=8.0, on_radius=100.0, first_azimuth=45.0)),
                 seam='one vertical lap seam 12 wide on the post side (azimuth 180), spot-welded every 40; not seen from the footway',
                 capacity_litres=round(cap_l, 1), capacity_kind='Derived from the inner frustum; Lead: pole bins about 50 litres'),
        bracket=dict(back_strap=dict(width=40.0, thickness=5.0, z0=590.0, z1=1030.0, x_from=D.K1_POST_R, x_to=D.K1_POST_R + 5.0, note='a flat bar welded up the back of the bin, touching the post along a line'),
                     clamps=[dict(z0=620.0, z1=660.0, ring_r_in=D.K1_POST_R, ring_t=5.0), dict(z0=960.0, z1=1000.0, ring_r_in=D.K1_POST_R, ring_t=5.0)],
                     clamp_note='each clamp is a 40 x 5 flat ring round the post, welded to the back strap on the bin side and closed at the far side of the post by ONE M8 bolt through two 12 mm ears (hex head 13 across, domed nut 13 across, 8 high)',
                     bolts=dict(count=2, size='M8', head_af=13.0, nut='domed, 13 across, 8 high', finish='galvanised, painted over once with the bin (a worn edge shows grey)')),
        lettering=dict(text='LITTER', cap_height=45.0, stroke=6.0, z_centre=800.0, azimuth_deg=90.0, arc_deg=70.0, material='letters_cream',
                       face='sans-serif capitals, upright, no serifs, set in an OFL face the builder picks (no maker\'s lettering, no council name); one line; a flat decal on the bin wall, bent to its radius',
                       words_allowed=['LITTER'], safe_because='LITTER is a plain English common noun: no maker, council, organisation, crest or product is named, and the asset plan says such words carry no brand'),
        asset_stencil=dict(optional=True, text='LB n', n=[1, 2], cap_height=22.0, z=1130.0, on='the post, away from the carriageway', material='letters_cream_worn', note='the same idea as the lamp columns\' LC n plates: generic, a letter pair and a digit'),
        extent=dict(x=[-D.K1_POST_R, D.K1_BIN_OFFSET + D.K1_R_TOP + 6.0], z=[0.0, D.K1_POST_TOP], bin_dia_rim_bead=373.0),
        edges='every edge rounded or rolled; the post\'s cap has a 3 mm radius; the bin\'s base corner is a 5 mm radius with a visible turned-up lap; the straps\' edges are square and slightly burred (a worn grey line where the paint has gone)',
        fixings='4 M8 bolts in two clamps (the bin hangs by its clamps alone); 8 to 10 spot-welds up the strap and 4 at the base plate seen as 6 mm dimples; no screws; no plate',
        conditions=D.K1_CONDITIONS, tri_budget=3500)
    k2_ext = lathe_extent(D.K2_OUTER)
    K2 = dict(
        name='hooded_drum', title='Free-standing hooded glass-fibre drum bin with a galvanised liner (generic; not the form of any maker\'s bin)',
        basis='JUDGEMENT AND LEADS: no photograph of a hooded bin of the period was reached. Leads (search summaries, unreached pages): hooded glass-fibre council bins existed by 1959 (Elton Civic Supplies, MoDiP records), Glasdon\'s own pages date its original Topsy to 1984 and a museum record dates a Glasdon bin with a removable red plastic hood and a metal liner to 1984 to 1990. The asset plan\'s "since about 1959" came from a retail page; the form below is a generic drum with a hood, built from the asset plan\'s "generic hooded bin, not the Topsy\'s exact form"',
        pivot='the base centre on the flag top', placed=True,
        outer_profile_rz=D.K2_OUTER, shell=D.K2_SHELL, height=D.K2_HEIGHT, extent=k2_ext, aperture=D.K2_APERTURE,
        parts=dict(foot_ring=dict(z=[0.0, 52.0], r_max=211.0, note='a moulded foot ring, 6 mm chamfer at the ground; the base below it is filled with concrete ballast to z 50 (not modelled)'),
                   body=dict(z=[52.0, 572.0], r_max=237.0, note='a gently bellied drum: r 205 at z 58, 237 at z 430, 232 at z 572; one moulded seam line down each side at azimuth +-90, 0.5 high, 3 wide'),
                   join_groove=dict(z=[576.0, 588.0], depth=6.0, note='the shadow line between body and hood'),
                   hood=dict(z=[588.0, k2_ext['z_max']], r_max=250.0, note='a lift-off glass-fibre hood: a skirt 50 high overhanging the body by 18, a shoulder, a shallow dome; the aperture is cut in its front'),
                   liner=dict(profile_rz=D.K2_LINER, rim_z=[700.0, 706.0], od=388.0, material='zinc_weathered', note='a galvanised steel liner 0.8 sheet, 640 high, a rolled rim whose upper edge is seen through the aperture; two wire bail handles (not modelled); capacity about 70 litres'),
                   lock=dict(azimuth_deg=180.0, z=582.0, d=22.0, escutcheon_d=40.0, note='a barrel lock at the back of the join; not seen from the front')),
        lettering=dict(text='LITTER', cap_height=55.0, stroke=8.0, z_centre=330.0, azimuth_deg=0.0, arc_deg=68.0, material='letters_cream', face='as K1', words_allowed=['LITTER'],
                       safe_because='as K1'),
        fixings='free-standing on its ballasted foot ring (mass about 28 kg); hood located by four moulded lugs and the lock; nothing is bolted to the footway; no visible screws or rivets on the front',
        edges='every moulding rounded: the aperture\'s lip R6, the hood skirt\'s edge R5, the foot ring\'s top R10; moulded seam lines only; no maker\'s name, logo, product number or moulded lettering of any kind',
        conditions=D.K2_CONDITIONS, tri_budget=6000)
    d1_out = D.d1_outer()
    D1 = dict(
        name='galvanised_dustbin_18in', title='Galvanised steel household dustbin (the scene\'s E13), to the shape of BS 792 as the research and leads give it',
        basis='READ for the sizes the scene prints (0.46 across, 0.61 high, lid 0.50 x 0.05); LEADS for the rest (a galvanised bin of 18 in top diameter, 15 in base, 22 to 24 in high; four sizes in BS 792:1973; a body, rims, base hoop, lid, body handles, lid handle); JUDGEMENT for the profile points; PHOTO for the metal\'s colour and weathering (the galvanised container of urban_street_02 and the zinc scans)',
        pivot='the base centre on the flag top', placed=True,
        outer_profile_rz=d1_out, body_top=D.D1_BODY_TOP, rib_z=list(D.D1_RIB_Z), rib=dict(height=24.0, proud=6.0, note='three swaged ribs, rounded, every 140; the first at 150'),
        foot_ring=dict(z=[0.0, 26.0], r_max=207.0, note='a rolled bottom hoop 207 across its fullest, its lower edge 6 above the ground at the centre (the base is dished)'),
        rim=dict(bead_r_max=231.5, z=[582.0, D.D1_BODY_TOP], note='a rolled top bead over a stiffening wire: 463 across (the scene\'s 0.46), its crown at 610 (the scene\'s 0.61)'),
        lid=dict(profile_rz=D.D1_LID, skirt_r_outer=251.0, skirt_z=[588.0, 617.0], dome_top_z=641.0, handle=D.D1_LID_HANDLE, note='a shallow pressed dome, 502 across (the scene\'s 0.50), its skirt overlapping the rim by 22 and standing 8 clear all round; a flat strap handle on its crown; lid height over the body top 50 (the scene\'s 0.05)'),
        side_handles=dict(count=2, azimuths_deg=[90.0, 270.0], **D.D1_SIDE_HANDLE, note='a loop of 25 x 3 flat strip, 100 tall, standing 45 proud, riveted at each end with two 8 mm dome-head rivets'),
        sheet=dict(thickness=0.6, kind='Lead: retail galvanised bins are 0.5 to 0.6 mm'),
        stencil=dict(optional=True, text='house number, digits only (for example 14 and 16)', cap_height=60.0, z=330.0, azimuth_deg=0.0, material='letters_cream_worn', note='painted by the householder, a brushed or stencilled white number, flaking; digits only, no word'),
        extent=dict(r_max=251.0, z=[0.0, D.D1_LID_HANDLE['top_z']], with_handles_r=264.0),
        edges='rolled edges at the foot, the rim and the lid; the ribs rounded; nothing sharp but the cut ends of the handle straps',
        fixings='rivets: 4 on each side handle (2 per end), 2 on the lid handle; the body has one vertical lock seam on the back (azimuth 180)',
        conditions=D.D1_CONDITIONS, tri_budget=4500)
    K3 = dict(D.K3)
    T['kinds'] = dict(K1=K1, K2=K2, D1=D1, K3=K3)
    # -------------------------------------------------------------------------------------------------------------------------- wear
    T['wear'] = wear_block()
    T['dressing'] = dressing_block()
    T['placements'] = placement_block()
    T['variants'] = dict(
        rule='one model of each kind (a council fits one design to a street): K1 one shape in three conditions, K2 one shape in three conditions, D1 one shape in three conditions; the shape never varies, the age does (asset plan A3: "variety comes from age and condition, not from shape")',
        models=dict(K1=1, K2=1, D1=1, K3_not_placed=1), conditions_per_model=3,
        street_picks=dict(B1='K1 A', B2='K1 B', B3='K2 c (burnt hood)', D1_1='D1 a (lid on)', D1_2='D1 b (lid off, over-full)'),
        seeds=dict(post_lean_deg=[0.0, 1.5], bin_tilt_deg=[0.0, 2.5], yaw_deg='K1: the bin side is fixed by the placement; K2: the aperture faces the building line +-15; D1: free about the axis, handles stay on the side seen from the street +-20', dent_positions='from the condition tables'),
        swaps='K2 hood open or off (the hood lifted aside at 0.4 m, the liner showing) only for a street event, not placed')
    T['reference_objects'] = reference_block()
    T['street_reference'] = street_reference_block()
    T['today_in_game'] = today_block()
    T['photographs_win'] = disagreements_block()
    T['sources'] = sources_block()
    T['unreached'] = unreached_block()
    T['panoramas_looked_at'] = panoramas_block()
    T['leads'] = leads_block()
    T['could_not_settle'] = could_not_settle_block()
    T['to_read_when_the_network_opens'] = to_read_block()
    T['checks'] = checks_block(T)
    T['handover'] = handover_block()
    return T


def reference_block():
    bt = json.load(open(os.path.join(HERE, '..', 'bollards', 'target.json')))
    fr = bt['frames']['US02_a']
    ref = dict(
        bollard_K2b_profile_rz=bt['profiles_final']['US02_a'],
        bollard_K2b_frame=dict(pano='urban_street_02', psi_deg=fr['psi'], depr_deg=fr['depr'], R_mm=fr['R'], note='the bollards writer\'s frame of the K2b bollard in urban_street_02 (its target.json frames.US02_a, profiles_final.US02_a): used only to lay a known object on the photograph at the camera height measured here'),
        person_height_mm=1750.0, person_kind='Judgement: a simple standing figure, for scale only')
    return ref


def street_reference_block():
    shops = [
        dict(id='mickeys', side='east', x0=3.0, x1=9.0, shop_door=4.797, side_door=3.822),
        dict(id='fish_market', side='east', x0=9.0, x1=15.0, shop_door=10.797, side_door=9.822),
        dict(id='ritas', side='east', x0=15.0, x1=21.0, shop_door=19.203, side_door=20.178),
        dict(id='empty_unit', side='east', x0=21.0, x1=27.0, shop_door=22.797, side_door=21.822),
        dict(id='steam_laundry', side='east', x0=27.0, x1=33.0, shop_door=31.203, side_door=32.178),
        dict(id='grocer', side='east', x0=33.0, x1=39.0, shop_door=38.147, side_door=None),
        dict(id='chandler', side='east', x0=40.0, x1=46.0, shop_door=44.203, side_door=45.178),
        dict(id='tea_rooms', side='west', x0=24.0, x1=30.0, shop_door=25.797, side_door=24.822),
        dict(id='ironmonger', side='west', x0=30.0, x1=36.0, shop_door=34.203, side_door=35.178),
        dict(id='newsagent', side='west', x0=36.0, x1=42.0, shop_door=40.203, side_door=41.178)]
    obs = []
    for lid, x, side in (('LC1', 8.0, 1), ('LC2', 18.0, -1), ('LC3', 28.0, 1), ('LC4', 38.0, -1)):
        obs.append(dict(id='lamp_' + lid, shape='circle', x=x, z=3.77 * side, r=0.062, clear_axis_m=1.0, source='lamp-posts target: axis |z| 3.77, sleeve 124'))
    obs.append(dict(id='kiosk', shape='box', x=16.5, z=3.125 + 0.55, w=0.914, d=0.914, source='scene E3: 0.914 square, 0.55 from the kerb'))
    obs.append(dict(id='pillar_box', shape='circle', x=27.0, z=3.125 + 0.6, r=0.33, source='scene E4: cap 0.66, 0.6 from the kerb'))
    obs.append(dict(id='guard_rail', shape='box', x=11.0, z=3.125 + 0.25, w=2.0, d=0.06, source='scene E8: one 2.0 m panel x 10 to 12, 0.25 back'))
    for nm, x, z in (('K3_a', 38.8, 3.5), ('K3_b', 40.2, 3.5), ('K4_a', 42.5, 3.45), ('K4_b', 44.0, 3.45)):
        obs.append(dict(id='bollard_' + nm, shape='circle', x=x, z=z, r=0.1, source='bollards target (east, behind the kerb face)'))
    for nm, x in (('W_yard_a', 20.7), ('W_yard_b', 24.3)):
        obs.append(dict(id='bollard_' + nm, shape='circle', x=x, z=-3.5, r=0.1, source='bollards target (west, the yard mouth)'))
    obs.append(dict(id='crossover_west', shape='box', x=22.5, z=-3.2, w=3.0, d=0.35, source='scene: a dropped crossover west x 21.0 to 24.0'))
    obs.append(dict(id='grit_bin', shape='box', x=41.0, z=-3.55, w=0.96, d=0.68, source='tools/art-recipes/terrace-front.py CLUTTER_ADDED (41.0 west, 0.55 from the kerb); production/assets/street/clutter/grit-bin.glb 0.96 x 0.68'))
    obs.append(dict(id='fish_crates', shape='box', x=12.0, z=4.975 - 0.46, w=6.0, d=0.92, source='the railings target\'s reading of the fish market\'s crates: 0.92 deep from the stallriser, x 9 to 15 east'))
    obs.append(dict(id='bus_stop_point', shape='circle', x=46.0, z=-4.3, r=0.2, source='production/specs/hook-cast.json bus_stop (the cast\'s standing place; the pole is not yet placed)'))
    return dict(street_length_m=48.0, kerb_face_m=3.0, kerb_back_m=3.17, building_line_m=5.125, stallriser_face_m=4.975, shops=shops, obstacles=obs,
                note='every number is read from the scene or the neighbours\' targets (self_check.py re-reads the Read ones); the kiosk, pillar box and railing places are the scene\'s set-backs from the kerb\'s back edge (3.125) to the piece\'s axis')


def wear_block():
    wear = dict(
        rule='The wear is a layer on each bin\'s own UVs (a mask set per mesh, as the asset plan\'s "curvature and occlusion bake per asset: edge chips to primer, rust streaks down from fixings, grime from the ground up, rain streaks from the top"), seeded per instance, and it AGREES WITH the wear target (production/cloud-week/targets/wear/target.json): its iron_wear rule for painted ironwork, its cig_end and gum kinds for the litter and gum round the bins, its splash and foot rule. Nothing below is measured on a bin photograph (none was reached); the parts marked Photo are measured on the galvanised container and the scans.',
        agree_with_wear_target=dict(
            iron_wear='paint loss and rust over 4 to 8 % of the UNWRAPPED area (post: 239 wide, the circumference of 76.1), in patches of 20 to 110 mm (p50 45), 40 % of the lost paint in the lowest 0.3 m of the post (the shoe), 30 % within 80 mm of a clamp, strap, bead or weld, 30 % anywhere; patch colour primer_ochre; below 4 in 10 clamps and every drain hole one or two rust streaks, width p50 24, aspect 4 to 12, length 100 to 300',
            cig_end='5 to 8 ends within 0.5 m of a K1 or K2 foot and 6 to 10 per m2 at the apron under B1 (Mickey\'s step), in the wear target\'s tiers (doorway apron 4 to 10 per m2); 8 x 25 to 30 mm, white or tan filter',
            gum='3 to 6 trodden discs within 0.5 m of each bin (the wear target\'s "around bins", shop-apron tier 4 to 8 per m2); 11 to 35 mm',
            splash='the lowest 0.3 m darker: splash_band, a gradient over 0.3 m (the wear target\'s foot rule)'),
        K1=[
            dict(id='K1-w1', what='paint loss and rust (the iron_wear rule above) on post, strap, clamps, base plate and rim bead', share_of_area=[0.04, 0.08], patch_mm=[20, 110], material='primer_ochre', under='rust_painted', kind='Read (wear target) applied; Judgement for the split by part'),
            dict(id='K1-w2', what='dents in the bin wall: round shallow dishes with a faint crease, concentrated below z 800 on the street side (kicked)', count=[2, 3], diameter_mm=[40, 110], depth_mm=[3, 12], kind='Judgement', per_condition='see conditions'),
            dict(id='K1-w3', what='rim bead crushed or bent inward over a stretch (a bin kicked or struck by a van)', length_mm=[70, 120], depth_mm=[8, 18], kind='Judgement', per_condition='B and C only'),
            dict(id='K1-w4', what='cigarette scorch on the rim: 3 to 7 brown-black marks 8 to 12 across on the rim bead, a grey ash smear 30 long on the outside below each', material='soot', kind='Judgement (tobacco is allowed; the wear target has the ends)'),
            dict(id='K1-w5', what='splash and grime band on the post and bin foot, dark warm grey-brown, lowest 0.3 m of the post fully, fading by 0.6 m; the bin\'s underside near-black', material='splash_band', kind='Judgement (the wear target\'s foot rule)'),
            dict(id='K1-w6', what='rust streaks from the four drain holes down the underside edge and a rust ring where the base plate meets the wall (a hand\'s width of orange along 40 % of the circumference)', material='rust_painted', kind='Judgement'),
            dict(id='K1-w7', what='fly-poster remnants: torn blank paper 80 to 250 mm, two at most, stuck on the bin\'s road side or the post; rain-softened, curling 3; no readable word, name or brand; no alcohol or gambling or children in any print', material='paper_remnant', kind='Judgement (the posters target governs content)'),
            dict(id='K1-w8', what='gum: 2 to 4 discs on the rim bead and 1 on the post at 1.0 m', kind='Judgement'),
            dict(id='K1-w9', what='paint fade: chalking on the faces looking at the sky (rim top, bead, the bin\'s upper third) toward paint_green_chalk by the condition\'s fade fraction; the underside and post foot keep the darker paint', kind='Judgement'),
            dict(id='K1-w10', what='the lettering: cream paint worn 25 % in speckles, one letter chipped at its edge, grimed toward letters_cream_worn below', material='letters_cream_worn', kind='Judgement'),
            dict(id='K1-w11', what='a black sack as the liner (B only): tucked over the rim 120 on the outside, a tie, a split showing contents', material='bin_sack_black', kind='Judgement'),
        ],
        K2=[
            dict(id='K2-w1', what='kick scuffs on the lower body (z 52 to 330): pale rubbed streaks and black rubber marks 20 to 80 long, covering the scuff fraction of the condition', kind='Judgement'),
            dict(id='K2-w2', what='UV chalking: the hood\'s top and the sun side go toward gel_green_chalk by the chalk fraction; roughness rises 0.30 to 0.62', kind='Judgement'),
            dict(id='K2-w3', what='BURN (condition c): a hole melted and burnt through the hood\'s upper left (azimuth -28, z 770), irregular, about 115 wide x 85 high, its edge thickened and re-set (melted_edge), a charred fringe 60 wide round it (char), a soot plume running up the dome 420 and a brown stain down the body 300; the liner inside scorched blue-black; a 25 mm stretch of the hood skirt blistered', kind='Judgement (bin fires are why the 1984 hoods carried a fire-safety device: Lead)'),
            dict(id='K2-w4', what='crazing: 2 to 3 hairline stress cracks 40 to 100 long at the aperture\'s lower corners and one running from the lock', kind='Judgement'),
            dict(id='K2-w5', what='cigarette scorch and dark dots on the aperture\'s sill lip (a place to stub out): 6 to 10 marks 8 to 12 across; a black smear below', material='soot', kind='Judgement'),
            dict(id='K2-w6', what='grime: splash_band to 0.35 m; a drip-stain tongue below the aperture\'s sill (brown-grey, 60 wide, 200 long); the hood\'s join groove packed dark', material='splash_band', kind='Judgement'),
            dict(id='K2-w7', what='fly-poster remnants (as K1-w7): 1 to 2, on the body, blank or ghosted', material='paper_remnant', kind='Judgement'),
            dict(id='K2-w8', what='a shallow dent 80 across, 5 deep on the hood (b)', kind='Judgement'),
            dict(id='K2-w9', what='the liner seen through the aperture: a galvanised rim, a black sack\'s folded edge over it, and loose litter (the overflow set)', kind='Judgement'),
            dict(id='K2-w10', what='the lettering: as K1-w10, plus a corner lifted 6 mm', kind='Judgement'),
        ],
        D1=[
            dict(id='D1-w1', what='dents: 5 to 9 round or oval dishes 30 to 120 across, 3 to 12 deep, lower half and one on the lid; the ribs flattened across the two worst; a crease running from the worst dent', kind='Judgement'),
            dict(id='D1-w2', what='rust at the foot hoop (35 to 80 % of its circumference, orange-brown streaking up 40), at the rivet heads of the handles (orange rings 12 across) and under the rolled rim\'s lowest edge; nowhere on the clean zinc between', material='rust', kind='Judgement (the container photograph shows none at 8 m; a seen-in-the-yard bin always has it at the foot)'),
            dict(id='D1-w3', what='white rust: a chalky bloom on the lower body and the underside of the lid\'s skirt, vertical pale rub-and-run streaks 20 to 60 wide (Photo: the container\'s streaks read +3 to +9 in G and B over its face)', material='white_rust', kind='Photo (the streak look), Judgement (the share)'),
            dict(id='D1-w4', what='soot and street film: the zinc goes from zinc_weathered at the top to zinc_dark_grime at the foot; a darker tide-line round the body where a wet pavement splashed it (z 120 to 160)', material='zinc_dark_grime', kind='Photo (the two scans), Judgement'),
            dict(id='D1-w5', what='scratches: 20 to 40 fine bright zinc-grey lines 60 to 200 long, mostly horizontal, where the bins are dragged', kind='Judgement'),
            dict(id='D1-w6', what='the lid: dented, sitting 2 degrees off, its handle strap rusted at the rivets; (b) the lid off, stood on its edge against the wall 120 beyond the second bin', kind='Judgement'),
            dict(id='D1-w7', what='a stencilled house number (digits only) in worn cream paint on the body\'s front, flaking', material='letters_cream_worn', kind='Judgement'),
            dict(id='D1-w8', what='a wet tide mark and dark drip tongue below the lid skirt, the lid\'s skirt edge dark inside', kind='Judgement'),
        ],
        note='What the photographs of the galvanised container show (urban_street_02, 8 m, 2019): a plain mid-grey surface with no visible spangle at that distance, faint vertical pale rub-and-run streaks on the left of the face, a few shallow smooth dents, a blue paint dab, handles of formed bar, no rust at the visible edges, grime heaviest at the foot behind the castors. The D1 wear above is that look plus the foot rust and rivet rust every old galvanised bin has.')
    return wear


def dressing_block():
    items = dict(
        crisp_packet=dict(size=[130, 95, 6], colours=[[170, 172, 176], [150, 40, 35], [200, 170, 40]], note='crumpled foil bag, printed with abstract stripes only: no word, no maker, no mark'),
        chip_paper=dict(size=[190, 150, 20], colours=[[200, 195, 180]], note='a greasy newsprint ball or flat sheet, grease spots (170, 150, 110); the print is grey bands, no readable word'),
        newspaper=dict(size=[380, 280, 12], colours=[[190, 188, 180]], note='a folded broadsheet page, unreadable grey text bands; no masthead, no headline'),
        tray_foam=dict(size=[190, 140, 30], colours=[[225, 222, 215]], note='a polystyrene food tray, yellowed edges'),
        can_330=dict(size=[66, 66, 115], colours=[[170, 40, 35], [60, 120, 70], [60, 90, 150]], note='a 330 ml soft-drink can, an invented generic livery, no lettering; NEVER beer, lager or cider'),
        bottle_2l=dict(size=[105, 105, 335], colours=[[200, 205, 195]], note='a clear or pale-green 2-litre pop bottle, label blank; never alcohol'),
        cig_packet=dict(size=[55, 85, 22], colours=[[230, 228, 220], [170, 150, 60]], note='a blank-faced cigarette pack (tobacco is allowed); no brand, no health text'),
        paper_cup=dict(size=[75, 75, 95], colours=[[225, 222, 212], [150, 110, 70]], note='a plain paper cup, no logo'),
        sweet_wrapper=dict(size=[60, 35, 2], colours=[[190, 60, 60], [60, 90, 160]], note='twist wrapper, no print'),
        cig_end=dict(size=[8, 8, 28], note='the wear target\'s kind: 8 x 25 to 30, white or tan filter'),
        gum=dict(size=[20, 20, 2], note='the wear target\'s kind: 11 to 35 across, trodden flat'),
        bin_sack=dict(size=[450, 400, 550], colours=[[22, 22, 24]], note='a tied black polythene sack; Poly Haven\'s CC0 trashbag model is 528 x 463 x 575 (Read, polyhaven.com/a/trashbag) and may be scaled to 0.85 as the source, else our own cloth-simulated shape (the asset plan: bags are ours)'),
    )
    sets = dict(
        O1_low=dict(for_kind='K1', mouth=dict(pieces=[3, 5], rise_above_rim=[0, 60], mix=['crisp_packet', 'chip_paper', 'can_330', 'cig_packet']), base=dict(radius_m=0.5, pieces=[3, 6], mix=['crisp_packet', 'sweet_wrapper', 'chip_paper']), cig_end=[5, 8], gum=[2, 3]),
        O1_full=dict(for_kind='K1', mouth=dict(pieces=[8, 12], rise_above_rim=[90, 160], mix=['crisp_packet', 'chip_paper', 'can_330', 'paper_cup', 'tray_foam', 'newspaper']), base=dict(radius_m=0.5, pieces=[8, 14], mix=['crisp_packet', 'sweet_wrapper', 'chip_paper', 'paper_cup', 'can_330']), cig_end=[6, 10], gum=[3, 5], sack_tie=True),
        O2_low=dict(for_kind='K2', aperture=dict(pieces=[1, 3], jammed_out_mm=[0, 30], mix=['crisp_packet', 'paper_cup']), base=dict(radius_m=0.55, pieces=[4, 8], mix=['crisp_packet', 'sweet_wrapper', 'chip_paper']), cig_end=[4, 8], gum=[2, 4]),
        O2_full=dict(for_kind='K2', aperture=dict(pieces=[4, 7], jammed_out_mm=[60, 100], mix=['paper_cup', 'tray_foam', 'chip_paper', 'newspaper', 'can_330']), base=dict(radius_m=0.6, pieces=[10, 16], mix=['crisp_packet', 'sweet_wrapper', 'chip_paper', 'paper_cup', 'can_330', 'bottle_2l', 'newspaper']), cig_end=[8, 14], gum=[3, 6]),
        O3_sacks=dict(for_kind='D1b', mouth=dict(sacks=1, rise_above_rim=[120, 200], note='one black sack bulging out of the open bin, tied, its neck folded, a split showing newspaper and tray'), beside=dict(sack_slumped=dict(size=[450, 400, 420], count=1, position='at the second bin\'s foot on the pavement, toward the kerb side'), spill=dict(pieces=[8, 12], radius_m=0.6, mix=['chip_paper', 'newspaper', 'tray_foam', 'crisp_packet', 'can_330'])), lid=dict(pose='stood on its edge against the wall, 120 mm beyond the second bin, 12 degrees off vertical')),
    )
    return dict(rule='OVERFLOWING LITTER IS A SEPARATE DRESSING: instanced pieces placed by the scene seed round and in each bin, never baked into its mesh, so a bin can be emptied (a night\'s work for the street) and the pieces scatter from the same seed as the scene\'s 34 pieces of litter and 60 of gum (seed 19900214, vignette-scene.json scatter). No piece carries a word or a brand; no alcohol, gambling or child-related object exists in the set.',
                items=items, sets=sets, instances_by_street=dict(B1='O1_low', B2='O1_full', B3='O2_full', D1_1=None, D1_2='O3_sacks'),
                consistent_with_wear_target='cig_end and gum counts lie inside the wear target\'s doorway-apron tier (4 to 10 per m2 and 4 to 8 per m2) over each bin\'s 0.5 to 0.6 m radius')


def placement_block():
    kf = D.KERB_FACE
    bins = []
    for p in D.PLACEMENTS:
        if p['kind'] == 'K1':
            z_ax = kf + p['post_setback_from_kerb_face']
            bin_x = p['post_x'] + p['bin_dir'] * D.K1_BIN_OFFSET / 1000.0
            e = dict(id=p['id'], kind='K1', condition=p['condition'], side=p['side'], post_x_m=p['post_x'], post_z_m=round(z_ax if p['side'] == 'east' else -z_ax, 3),
                     bin_axis_x_m=round(bin_x, 3), bin_axis_z_m=round(z_ax if p['side'] == 'east' else -z_ax, 3), setback_from_kerb_face_m=p['post_setback_from_kerb_face'],
                     near_edge_from_kerb_face_m=round(p['post_setback_from_kerb_face'] - D.K1_R_TOP / 1000 - 0.006, 3), far_edge_from_kerb_face_m=round(p['post_setback_from_kerb_face'] + (D.K1_R_TOP + 6) / 1000, 3),
                     bin_dir=p['bin_dir'], yaw_note=p['yaw_note'], serves=p['serves'])
        else:
            z_ax = kf + p['axis_setback_from_kerb_face']
            e = dict(id=p['id'], kind='K2', condition=p['condition'], side=p['side'], axis_x_m=p['axis_x'], axis_z_m=round(z_ax if p['side'] == 'east' else -z_ax, 3),
                     setback_from_kerb_face_m=p['axis_setback_from_kerb_face'], near_edge_from_kerb_face_m=round(p['axis_setback_from_kerb_face'] - 0.25, 3), far_edge_from_kerb_face_m=round(p['axis_setback_from_kerb_face'] + 0.25, 3),
                     yaw_note=p['yaw_note'], serves=p['serves'])
        bins.append(e)
    dust = []
    for d in D.DUSTBINS:
        zc = 3.125 + d['setback_from_kerb']
        dust.append(dict(id=d['id'], kind='D1', condition=d['condition'], side='east', axis_x_m=d['x'], axis_z_m=round(zc, 3), setback_from_kerb_m=d['setback_from_kerb'],
                         lid_edge_z_m=round(zc + 0.25, 3), note='the scene\'s setback is read from the kerb\'s back edge (3.125, the scene\'s kerb width 0.125), the convention the pillar box and lamp columns use; with the kerbs target\'s granite kerb (back edge 3.17) the lids\' far edge is 4.97 to 5.02, against the stallriser line 4.975: kept as the scene has it'))
    return dict(
        frame='x along the street (0 at the south/quay end), z across from the crown, east +; metres; set-backs are to the piece\'s axis from the kerb FACE (z 3.0) for the new bins (the bollards\' convention) and from the kerb\'s back edge for the scene\'s dustbins (the scene\'s)',
        bins=bins, dustbins=dust,
        conditional=[dict(id='B4', kind='K1', condition='A', side='west', post_x=47.2, post_setback_from_kerb_face=0.62, bin_dir=+1, only_if='the bus-stop flag pole is placed at x 46.0 within 2 m of this slot AND the street adds a second shelter-less stop; with B3 at 44.0 (2.0 m from the pole) the stop is already served, so B4 is NOT placed', placed=False)],
        rule_asset_plan='a litter bin within 3 m of each shop door and at the bus stop (production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md, A3 example rules)',
        judgement=dict(
            doors=dict(shop_doors=10, side_doors=9, note='ten shopfronts (six east bays and the chandler, three west shops) and nine side doors: the rule would place 10 to 19 bins in 48 m, one every 2.5 to 5 m, and a bin at the bus stop on top'),
            reasoning=['Lead: a council review (Rossendale, modern) found about half of a district\'s bins were pole bins of about 50 litres, the rest floor bins of 100 to 120 litres: bins are bought by the hundred and fixed where litter is made, not at every door.',
                       'Lead: the 1958 Litter Act and the 1960 Council of Industrial Design competition made bins a council duty on the main streets of towns, not a shopkeeper\'s; Quay Street is a minor street of an old port quarter.',
                       'The scene file already judged "a British parade carries about one bin per shop group" (E6 note) and the asset plan\'s own count is 2 to 3 for the street.',
                       'Litter is made at: the tobacconist and newsagent (the most), the grocer, the taxi rank where drivers wait and smoke, and the bus stop. The fishmonger\'s trade is wet and kept off the pavement; Rita\'s pawnbroker, the empty unit, the launderette and the chandler make little street litter; the tea room and the ironmonger make none.',
                       'So: THREE bins, one per litter source group, each within 3 m of at least one door or the stop: B1 serves Mickey\'s two doors (2.6 and 1.6 m) and the rank; B2 serves the grocer (2.7 m); B3 serves the newsagent\'s side door (2.8 m) and the bus stop (2.0 m).'],
            doors_served=dict(B1=['door_mickeys_shop (1.59)', 'door_mickeys_side (2.56)'], B2=['door_grocer_shop (2.73)'], B3=['door_news_side (2.82)', 'bus stop (2.0)']),
            doors_not_served='fishmonger 10.797, Rita\'s 19.203, empty unit 22.797, launderette 31.203, chandler 44.203, tea room 25.797, ironmonger 34.203, newsagent\'s main door 40.203 (3.8 from B3): the nearest bin to each is 4 to 15 m away, which is what a 1990 minor street had'),
        walking_strip=dict(minimum_m=D.WALKING_PERSON_M, rule='after every bin, the clear width between the bin\'s building-side extreme and the nearest obstacle on that side (the stallriser face |z| 4.975, a fixture, another bin) is at least 0.68 m, and the bin leaves the kerb\'s back edge (|z| 3.17) at least 0.25 m clear',
                           note='the 0.68 m is the walking person of the railings\' target; B1 and B2 leave 1.17 m, B3 0.92 m, the dustbins 1.30 m on the kerb side'),
        clearances=dict(from_door_leaf_x_m=0.30, from_lamp_column_axis_m=1.0, from_other_furniture_edge_m=0.60, from_kerb_back_m=0.25, from_crossover_edge_m=0.5, note='distances in plan between the bin\'s footprint and the thing, the bollards\' writer\'s rules (from other furniture 0.6)'),
        obstacles=dict(note='the fixed things the strip and the clearances are tested against, read from the other targets and the scene (self_check re-reads them): lamp columns LC1 (8.0 east), LC2 (18.0 west), LC3 (28.0 east), LC4 (38.0 west) at |z| 3.77; the kiosk (16.5 east, 0.914 square at 0.55 set-back); the pillar box (27.0 east, cap 0.66, set-back 0.6); the guard railing (10 to 12 east, 0.25 back); the east bollards K3 (38.8 and 40.2, |z| 3.5), K4 (42.5 and 44.0, |z| 3.45); the west yard bollards (20.7 and 24.3, |z| 3.5), the crossover (west 21 to 24); the recipe\'s grit bin (41.0 west, 0.96 wide); the fish market\'s crates (x 9 to 15 east, 0.92 deep from the stallriser); the bus stop (46.0 west)'),
        dustbin_note='the two dustbins stand 0.6 m apart on the line x 21.4 and 22.0, in front of the empty unit\'s side door (x 21.40 to 22.24): suits an unlet unit and the household that never uses it; the door is not to be opened in the walk. Kept as the scene has it.')


def today_block():
    h = PM['held_bins']
    return dict(
        what='The street today (read 9 October 2026): the scene file places three public bins (E6: swing_bin east x 8.0, 0.65 from the kerb face; outdoor_bin east x 30.0, 0.75; swing_bin west x 33.0, 0.65) and two dustbins (E13); the street recipe (tools/art-recipes/terrace-front.py CLUTTER_FOR_HELD) swaps BOTH held bin meshes for the script-built council-green pole bin (production/assets/street/clutter/litter-bin.glb) and the dustbins for production/assets/street/clutter/dustbin.glb, and adds a grit bin at x 41 west.',
        faults=[
            dict(id='T1', thing='swing_bin.glb (The Base Mesh, CC0), scene E6 x 8.0 east and x 33.0 west', measured=dict(size_m=h['swing_bin']['size_m']), what_is_wrong='a kitchen swing-lid bin (a narrow tapered body 0.33 x 0.32 with a pivoting top, a pedal-less lid 0.13 high): an indoor domestic object 0.84 m tall; no council street ever fixed one; one grey DefaultMaterial, no texture; the recipe replaces it, so it never shows'),
            dict(id='T2', thing='outdoor_bin.glb (The Base Mesh, CC0), scene E6 x 30.0 east', measured=dict(size_m=h['outdoor_bin']['size_m']), what_is_wrong='a square-plan tapered bin 0.60 x 0.60 with four flared horns and a domed centre: a modern decorative bin whose symmetrical pagoda top has no 1990 council equivalent; 0.60 square is too big for a 2.0 m footway with a 0.68 m walking strip beside a pillar box; DefaultMaterial grey, metallic 0.2, roughness 0.8, no texture; the recipe replaces it'),
            dict(id='T3', thing='production/assets/street/clutter/litter-bin.glb (what the street shows today for all three)', measured=dict(size_m=h['litter-bin']['size_m'], materials=h['litter-bin']['materials']),
                 what_is_wrong='the right idea (a green pole bin marked LITTER, a research candidate) but built as a stand-in: the bin is a plain tube 0.40 across with 3 mm walls and NO taper, drain holes written in its notes but not modelled, a thick torus rim, the bracket two cubes 80 x 60, no clamp rings or bolts, the rim at 0.95 m against 1.05, the post cut off at 1.0 m with a flat plain top, LITTER in Blender\'s default face at 75 mm, one clean colour with metallic 0.3 (paint is not metal), identical at all three places (a council\'s bins are one design but not one condition), no lean, dent, rust, grime, scorch, poster or litter at all: the "built, not lived-in" look the brief warns about'),
            dict(id='T4', thing='production/assets/street/clutter/dustbin.glb (the two dustbins)', measured=dict(size_m=h['dustbin']['size_m'], materials=h['dustbin']['materials']),
                 what_is_wrong='close in form (three ribs, a rolled foot and rim, two loop handles, a domed lid with a ring handle) but 0.55 high to the rim against the scene\'s 0.61, the lid a dome of 50 with a ring handle where the target has a strap; the handles are torus rings not riveted straps; one uniform grey (150, 152, 150) metallic 0.85 roughness 0.55 with no dent, rust, white rust, soot, house number or the lid off; both bins identical'),
            dict(id='T5', thing='the scene\'s own E6 note', what_is_wrong='"a British parade carries about one bin per shop group": right in judgement, but it places two on the east side at x 8 and 30 (neither near a shop door but Mickey\'s) and one on the west at 33, and not at the newsagent or the bus stop; the new placements replace them'),
        ])


def disagreements_block():
    return [
        dict(id='P1', topic='when hooded bins began', book='the asset plan (3-FURNITURE-PROPS-FOOD.md A4) reads "Glasdon\'s Topsy 65 marks 65 years in 2024, which puts the hooded glass-fibre bin\'s design at about 1959" from a retail listing', other='a search summary of the maker\'s own FAQ dates the ORIGINAL Topsy to 1984 (a lift-off hood, a fire-safety device); a museum record dates a Glasdon bin with a red plastic hood and a metal liner to 1984 to 1990; the MoDiP records (leads) show Elton Civic Supplies\' hooded glass-fibre bins dated 1959 with a side door to a galvanised liner', chose='a hooded bin is plausible in 1990 either way (a six-year-old Topsy-type or a thirty-year-old Elton-type); K2 is a generic drum with a LIFT-OFF hood and a galvanised liner, which fits both; the "65 years" is the company\'s age, not the bin\'s, and the asset plan\'s 1959 is not relied on', kind='Lead against a retail page; no photograph either way'),
        dict(id='P2', topic='which types', book='the clutter research (7) recommends (a) an open-top bin on a pole or (c) a round precast concrete bin', other='the asset plan lists two kinds (a pole-mounted open bin and a free-standing hooded bin)', chose='K1 (a) and K2 (b) are placed; (c) is written as K3 and not placed: the leads (a 1960 competition\'s praise for an open concrete design; a current precast range) show concrete bins existed but nothing says Meridian\'s council bought them; a concrete drum 0.55 across would also take 0.55 m of a 2.0 m footway where the 0.68 strip has to be kept beside a pillar box and a kiosk; timber-slatted bins have no support in any source and are not written', kind='Judgement'),
        dict(id='P3', topic='how many bins', book='the asset plan\'s rule: a litter bin within 3 m of each shop door and at the bus stop', other='the same plan\'s count: 2 to 3 on the street; the scene: one per shop group', chose='THREE bins (section 7): the rule would give 10 to 19', kind='Judgement'),
        dict(id='P4', topic='dustbin height', book='the clutter research (10): 575 mm tall (a modern 90-litre listing), 450 across the top, 400 at the foot; the recipe\'s script builds 0.55', other='the scene (E13, Read): 0.46 across, 0.61 high ("18 in by 24 in"); leads: 22 in (559) to 610 mm retail', chose='the scene\'s 0.46 x 0.61 and lid 0.50 x 0.05 (the scene is the law and the leads span 559 to 610); the foot 398 across and the three ribs are Judgement', kind='Read over Lead'),
        dict(id='P5', topic='pole bin rim height', book='the recipe\'s script puts the rim at 0.95', other='no source; ergonomics (a bin is used with a straight arm: rim near the hip-to-elbow height of 1.0 to 1.1 m)', chose='rim at 1.05 m, post top at 1.255; the recipe\'s 0.95 and 0.40 floor are replaced', kind='Judgement'),
        dict(id='P6', topic='the set-back convention', book='the scene\'s dustbins: "1.6 m back from the kerb"', other='the bollards\' target: 0.5 m behind the kerb FACE', chose='the dustbins keep the scene\'s reading (from the kerb\'s back edge); the new bins state their set-back from the kerb face and also give their edge distances', kind='Read'),
        dict(id='P7', topic='wheeled bins', book='the brief: no wheelie bins unless shown otherwise', other='urban_street_02 (2019) shows a purple four-castor bulk bin and a galvanised 1,100-litre steel container on the road by a housing block', chose='neither is placed: the purple plastic bulk bin is a later type; the steel container is a yard or estate bin, not a street litter bin (the asset plan places "1,100-litre bin" in the yard, 1 to 2); it is the only photograph of galvanised steel in street wear that was reached and is used for that', kind='Photo'),
    ]


def sources_block():
    return [
        dict(id='S1', url='https://polyhaven.com/a/urban_street_02', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0 (polyhaven.com/license)', taken='2019-08-18 06:45 UTC (51.526655, -0.056465)', what='an estate road under a railway viaduct, Bethnal Green: a galvanised steel 1,100-litre container and a purple four-castor plastic bin on the road at the kerb, black plain tapered bollards, double yellow lines', used='YES: the container\'s colour and wear; the scale overlay; the camera height', period='2019: the steel container is the kind used in yards and estates from the 1970s on (Lead); the purple bin is a later plastic type; the bollard is of a pattern that stood in 1990'),
        dict(id='S2', url='https://polyhaven.com/a/bethnal_green_entrance', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-08-18 07:01 UTC', what='a park entrance: two black rectangular panelled hooded bins inside the railings, about 10 to 15 m from the camera, behind a wall', used='LOOKED AT, not measured (8 to 12 pixels across; its ground level behind the wall is unknown)', period='modern (panelled, 2000s): a later type than K2'),
        dict(id='S3', url='https://polyhaven.com/a/leadenhall_market', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-05-19', what='a covered market lane in the City: two small stainless-steel rectangular bins with a sticker on a pavement', used='LOOKED AT, not measured; the frame includes shop lettering and a bar\'s sign, so no crop of it is kept', period='modern (stainless): not period'),
        dict(id='S4', url='https://polyhaven.com/a/roof_garden', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-05-19', what='a roof garden: two stainless drum bins on short pedestals beside a path', used='LOOKED AT, not measured', period='modern (2010s stainless drum): not period'),
        dict(id='S5', url='https://polyhaven.com/a/limehouse', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-05-19 15:45 UTC', what='a marina: one small blue bin on a pontoon', used='LOOKED AT, not measured', period='modern'),
        dict(id='S6', url='https://polyhaven.com/a/birbeck_street_underpass', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-08-18 06:53 UTC', what='a street under a railway arch: a wheeled bin at a blue gate, two small recycling boxes at a gate pier, road barriers', used='LOOKED AT, not measured', period='wheeled and recycling bins: later than 1990'),
        dict(id='S7', url='https://polyhaven.com/a/metal_trash_can', read='2026-10-09', author='GurJas Studios', licence='CC0 1.0', taken='model published 2023-09-27', what='a ribbed galvanised-style trash can with two handles and a lid, 0.906 high and 0.55 across (a US-style can), clean and rusted variants', used='YES: a reference for the pressed rib, rolled bead and handle arrangement of a ribbed steel can; its size is NOT the British dustbin\'s', period='not British'),
        dict(id='S8', url='https://polyhaven.com/a/trashbag', read='2026-10-09', author='Benny Weimer', licence='CC0 1.0', taken='model published 2026', what='a black polythene sack 0.528 x 0.463 x 0.575', used='YES: the sack\'s size and look', period='timeless'),
        dict(id='S9', url='https://polyhaven.com/textures (api.polyhaven.com/files/<id>, diffuse 1k)', read='2026-10-09', author='Dimitrios Savva, Jenelle van Heerden, Charlotte Baglioni, Rob Tuytel, Amal Kumar, Sergej Majboroda', licence='CC0 1.0', taken='various', what='twelve scanned material albedos: corrugated_iron, corrugated_iron_02, _03, worn_corrugated_iron, green_metal_rust, rust_coarse_01, rusty_painted_metal, precast_concrete_wall, pebble_embedded_concrete, painted_metal_shutter, worn_shutter, container_side', used='YES: the median sRGB of the galvanised, painted-green, rust and concrete colours (each in photo_measurements.json)', period='n/a: a material\'s colour does not date'),
        dict(id='S10', url='the repository (production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md; production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/specs/vignette-scene.json; production/specs/hook-cast.json; production/cloud-week/targets/*; production/assets/street/clutter/*.glb; ledger/Assets/Props/base-mesh/{outdoor_bin,swing_bin}.glb; tools/art-recipes/terrace-front.py; tools/meshgen/blender/clutter/{litter_bin,dustbin}.py)', read='2026-10-09', author='the project', licence='the project\'s own, and CC0 for the Base Mesh files', taken='2026-09-09 to 2026-10-09', what='the scene\'s bins and dustbins, the street\'s frame, the neighbours\' targets, the held and built bin meshes', used='YES (Read numbers)', period='n/a'),
        dict(id='S11', url='WebSearch result summaries, 9 October 2026 (Glasdon FAQ and news pages; London Transport Museum record 2023-1775; MoDiP records BXL 0564 to 0570; the National Archives blog "Public bins: a design history"; V&A O1194407; BSI Knowledge BS 792; a UK tariff ruling; trade catalogues; a council bins review)', read='2026-10-09', author='third parties (reached only as summaries; every page refused or does not resolve here)', licence='n/a', taken='n/a', what='leads: dates and sizes in section 3', used='LEADS ONLY: steer a judgement, never a number the target relies on', period='n/a'),
    ]


def unreached_block():
    return ['Wikimedia Commons (every litter-bin and dustbin category), Geograph, Flickr, archive.org, HathiTrust, Wikipedia, Historic England (the "From Lamp Posts to Litter Bins" blog), Glasdon\'s own site, the London Transport Museum, MoDiP, the National Archives\' blog, the V&A, BSI Knowledge, the Design Council Archive, British Pathe, BBC, gov.uk, legislation.gov.uk, Gutenberg, Pexels, Sketchfab, the Beauty of Transport: all answer "CONNECT tunnel failed, response 403" or do not resolve from this cloud (WebFetch: "getaddrinfo ENOTFOUND"). Nothing was taken from any of them except what a WebSearch summary said, marked Lead.',
            'ambientCG answers its home page only; a galvanised-steel query to its API returned no material.']


def panoramas_block():
    rows = [
        ('adams_place_bridge', 'a glazed footbridge', 'no bin', 'n/a'),
        ('bethnal_green_entrance', 'two black panelled hooded bins inside park railings, 10 to 15 m away; a white sack caught on the railings', 'modern hooded bin (a later type than K2)', 'no: panelled 2000s type; the hooded idea yes'),
        ('birbeck_street_underpass', 'a wheeled bin at a blue gate; two small recycling boxes at a gate pier; blue road barriers', 'wheeled and recycling bins', 'no (wheelie bins after 1990 on most streets; recycling boxes later)'),
        ('cambridge', 'a college A-board; no bin', 'no bin', 'n/a'),
        ('canary_wharf', 'a ticket-machine wall, a concrete block, handrails; no bin', 'no bin', 'n/a'),
        ('epping_forest_01 / 02', 'woodland; no bin', 'no bin', 'n/a'),
        ('greenwich_park / _02 / _03', 'parkland, a bench; no bin', 'no bin', 'n/a'),
        ('leadenhall_market', 'two stainless rectangular bins at a shopfront (plus shop lettering and a bar\'s sign in other views: no crop kept)', 'modern stainless', 'no'),
        ('limehouse', 'one small blue bin on a pontoon', 'modern', 'no'),
        ('roof_garden', 'two stainless drum bins on short pedestals', 'modern stainless drum', 'no'),
        ('urban_street_01', 'no bin: bollards, planted bed, cars', 'no bin', 'n/a'),
        ('urban_street_02', 'a purple four-castor plastic bulk bin with a grey lid and a galvanised steel 1,100-litre container with castors, on the road at the kerb outside a housing block; black bollards', 'bulk containers (not street litter bins)', 'steel container: yes (1970s on, Lead); purple plastic bulk bin: later; neither is a litter bin'),
        ('urban_street_03', 'no bin on the street; a blue box in a front garden', 'no bin', 'n/a'),
        ('urban_street_04', 'no bin: stuccoed terrace, a cycle hoop, a railed garden', 'no bin', 'n/a'),
    ]
    return dict(note='all seventeen British panoramas on Poly Haven (the Dublin sets docklands_01 and _02 and the Irish interiors were not used) were looked at as 8 rectilinear views each at 75 degrees; none shows a street litter bin of a type used before 1990',
                rows=[dict(panorama=a, shows=b, type=c, in_use_before_1990=d) for a, b, c, d in rows])


def leads_block():
    return [
        dict(id='L1', what='Glasdon\'s FAQ (search summary): the original Topsy was launched in 1984 with a lift-off hood and a fire-safety device; earlier hooded models such as the Super Guppy opened level with the rim so a full liner had to be hoisted about three feet', url='https://www.glasdon.com/intl/faq/topsy-litter-bin', kind='Lead', use='K2\'s lift-off hood; the burn variant'),
        dict(id='L2', what='London Transport Museum collection record 2023-1775 (search summary): "Waste bin; freestanding litter bin, 1984 - 1990", Glasdon-made, a metal liner and a removable red plastic outer hood', url='https://www.ltmuseum.co.uk/collections/collections-online/infrastructure/item/2023-1775', kind='Lead', use='K2\'s liner and hood; the date window'),
        dict(id='L3', what='MoDiP (Museum of Design in Plastics) records BXL 0564 to 0570 (search summary): Elton Civic Supplies\' free-standing bins of fire-retardant glass-fibre polyester dated 1959 with a side door to a galvanised liner; post-type bins of reinforced polyester c. 1960 to 1969, supplied to councils free, "no rust stains on concrete lamp standards"', url='https://www.modip.ac.uk/artefact/bxl-0567', kind='Lead', use='glass-fibre bins in councils by 1959 to 1969; pole bins on lamp standards'),
        dict(id='L4', what='The National Archives blog "Public bins: a design history we should not discard too easily" (search summary): the 1958 Litter Act; the 1960 Council of Industrial Design competition and its Embankment Gardens exhibition; the 1961 "Town Number One" (a perforated-sheet cylinder on a black base, V&A O1194407) ; councils decided locally so stock varied regionally; an open concrete design praised', url='https://blog.nationalarchives.gov.uk/public-bins-design-history', kind='Lead', use='why councils had bins; why no single type; K3'),
        dict(id='L5', what='Rossendale Borough Council bins review (search summary, modern): of 388 bins 207 were pole bins; pole bins hold about 50 litres, floor bins 100 to 120', url='https://www.rossendale.gov.uk/download/meetings/id/1746/Item%2520D9%2520-%2520Appendix%25202', kind='Lead (modern)', use='K1 capacity; the mix'),
        dict(id='L6', what='trade catalogues (search summaries, modern): a 70-litre galvanised post bin of 2 mm sheet with an 8 mm base and a "LITTER" sticker supplied; a 40-litre round steel post bin 355 across and 480 high; a 56-litre square post bin 419 x 235 x 622', url='https://www.kingfisherdirect.co.uk/middlesbrough-post-mountable-steel-litter-bin-70-litre-capacity', kind='Lead (modern)', use='K1 size band; the word LITTER as the one marking'),
        dict(id='L7', what='BSI Knowledge, BS 792 (search summary): editions 1938, 1947 (published 1965) and 1973 (published October 1973, withdrawn August 2016): "four sizes of dustbins up to 0.092 m3"; clauses on the body, rims, base, bottom hoop, lid, body handles and lid handle', url='https://knowledge.bsigroup.com/products/specification-for-mild-steel-dustbins', kind='Lead', use='D1\'s parts list'),
        dict(id='L8', what='a UK tariff ruling and two retail listings (search summaries): a 90-litre galvanised bin of 18 in top, 15 in base, 22 in high; 457 across x 610 high excluding the lid; or 450 top, 400 base, 575 high; 0.5 to 0.6 mm sheet', url='https://www.tax.service.gov.uk/search-for-advance-tariff-rulings/ruling/600008935', kind='Lead', use='D1\'s taper and sheet'),
        dict(id='L9', what='a summary of Preston Central Bus Station (1969): glass-reinforced plastic litter bins, poster boards and signs', url='(summary only)', kind='Lead', use='GRP street furniture by 1969'),
        dict(id='L10', what='Ian Leith, "British Litter Bins 1950 to 66", Design Council Archive, University of Brighton (a pointer in a summary)', url='(not reached)', kind='Lead', use='first thing to read when the network opens'),
    ]


def could_not_settle_block():
    return [
        'NO PHOTOGRAPH OF A PERIOD STREET LITTER BIN WAS REACHED, so the shape of K1 and K2 is research and judgement, not measurement: their proportions (the taper, the bead, the clamp rings, the hood\'s skirt and the aperture\'s size and height) are ergonomic and trade guesses and a fresh reviewer has nothing to hold them against but the asset plan\'s kit names and the leads.',
        'Which council colour Meridian used (green is a judgement from the repository\'s own recipe and from green being common on 1980s municipal steel and glass-fibre; no source says); canon owes the council\'s name and no word of it appears on any bin.',
        'Whether Meridian\'s council had bought the Topsy-type (1984) or only older hooded or pole stock; K2 is built generic so either reads.',
        'The real height of rim and aperture: K1 rim 1.05 and K2 aperture sill 0.65 are ergonomic Judgement (the repository\'s script has 0.95 for the pole bin).',
        'The BS 792 dimension table (the 1973 or earlier edition): 0.46 x 0.61 is the scene\'s; the foot (398), the rib heights and the handle sizes are Judgement.',
        'Whether bins were fixed to the lamp columns on Quay Street: K1 stands on its own post; the lamp-post target\'s shaft at 1.0 m is 68 mm and the sleeve 124, neither a clean 76 mm host. A column-mounted variant would need the lamp target\'s sleeve and a different clamp: not written.',
        'The bus stop (hook-cast: x 46.0, z -4.3; not in the scene file) has no pole yet, so the 2.0 m between B3 and the stop is to the cast\'s point.',
        'The camera heights of every panorama but urban_street_02 were not re-measured; no bin\'s size depends on one.',
    ]


def to_read_block():
    return ['Wikimedia Commons: Category "Litter bins in the United Kingdom" and "Dustbins" (and the Geograph Britain and Ireland grid squares of any English port town photographed 1985 to 1992): the type, size and colour of every bin in a dated street photograph; check each file page for author, licence, date',
            'Geograph: searches for "litter bin" and "dustbin" limited to 1980 to 1995 uploads of scanned slides',
            'Historic England Archive: street-furniture photographs 1975 to 1995',
            'The Design Council Archive (University of Brighton): Ian Leith, "British Litter Bins 1950 to 66", and its several hundred bin photographs',
            'MoDiP records BXL 0564 to 0570 in full (dates, dimensions, colours of the Elton glass-fibre bins)',
            'The London Transport Museum records 2023-1775 and 1999-37177 (dimensions and colours of a 1984 to 1990 hooded bin and a 1950s to 60s grey bin)',
            'Glasdon\'s company history and its Topsy and Super Guppy data sheets (the shapes to AVOID copying, and the real 1984 dimensions)',
            'The National Archives blog and the V&A record O1194407 (Town Number One)',
            'BSI BS 792:1973 (the preview of its dimension table) and BS 3735 (lids)',
            'British Pathe and BFI film of a British high street, 1988 to 1991 (bins in use, colours, overflow)']


def checks_block(T):
    K = T['kinds']
    ch = []

    def add(name, applies, measure, expected, tol, kind):
        ch.append(dict(name=name, applies_to=applies, measure=measure, expected=expected, tolerance=tol, kind=kind))
    # K1
    add('K1_total_height', 'K1', 'z of the post cap\'s top above the pivot', D.K1_POST_TOP, 25, 'Judgement')
    add('K1_post_diameter', 'K1', 'outer diameter of the post tube', 76.1, 3, 'Judgement (3-inch tube)')
    add('K1_rim_height', 'K1', 'z of the rim bead\'s crown above the pivot', D.K1_RIM_TOP, 20, 'Judgement; the repository script\'s 950 is wrong by 100')
    add('K1_bin_height', 'K1', 'rim crown minus the base plate\'s underside', D.K1_RIM_TOP - D.K1_BIN_Z0, 15, 'Judgement')
    add('K1_bin_rim_diameter', 'K1', 'diameter over the rim bead', 373.0, 12, 'Judgement')
    add('K1_bin_foot_diameter', 'K1', 'outer diameter of the wall at its foot', 330.0, 10, 'Judgement')
    add('K1_bin_offset', 'K1', 'post axis to bin axis along x', D.K1_BIN_OFFSET, 10, 'Derived')
    add('K1_capacity_litres', 'K1', 'inner volume from the floor to the rim', K['K1']['bin']['capacity_litres'], 6, 'Derived; Lead 50 L class')
    add('K1_wall_thickness', 'K1', 'sheet thickness (inner offset of the wall section)', D.K1_WALL, 0.7, 'Judgement; the repository script\'s 3 mm is too thick')
    add('K1_clamp_count_and_z', 'K1', 'two clamp rings, centres at z 640 and 980', [640.0, 980.0], 25, 'Judgement')
    add('K1_drain_holes', 'K1', 'four holes of 8 in the base plate on radius 100', [4, 8.0, 100.0], [0, 2.0, 6.0], 'Judgement')
    add('K1_letter_height', 'K1', 'cap height of LITTER', 45.0, 6, 'Judgement; the repository script\'s 75 is too tall')
    add('K1_only_word', 'K1', 'every word on any mesh or texture', ['LITTER'], 0, 'rule')
    add('K1_bead_diameter', 'K1', 'rolled bead cross-section', 9.0, 2, 'Judgement')
    # K2
    add('K2_total_height', 'K2', 'z of the dome crown', D.K2_HEIGHT, 20, 'Judgement')
    add('K2_hood_max_diameter', 'K2', 'diameter of the hood skirt', 500.0, 15, 'Judgement')
    add('K2_body_max_diameter', 'K2', 'diameter of the body at z 430', 474.0, 15, 'Judgement')
    add('K2_foot_diameter', 'K2', 'diameter of the foot ring', 422.0, 12, 'Judgement')
    add('K2_aperture_width', 'K2', 'width of the aperture opening', D.K2_APERTURE['width'], 20, 'Judgement')
    add('K2_aperture_height', 'K2', 'height of the aperture opening', D.K2_APERTURE['height'], 15, 'Judgement')
    add('K2_aperture_sill_z', 'K2', 'z of the aperture\'s lower edge', D.K2_APERTURE['sill_z'], 20, 'Judgement')
    add('K2_liner_rim_z', 'K2', 'z of the liner\'s rolled rim (seen through the aperture)', 700.0, 15, 'Judgement')
    add('K2_join_groove_z', 'K2', 'z of the join groove', [576.0, 588.0], 10, 'Judgement')
    add('K2_letter_height', 'K2', 'cap height of LITTER', 55.0, 6, 'Judgement')
    add('K2_only_word', 'K2', 'every word on any mesh or texture', ['LITTER'], 0, 'rule')
    add('K2_no_maker_mark', 'K2', 'moulded or printed maker, council or product marks', 0, 0, 'rule')
    # D1
    add('D1_total_height', 'D1', 'lid handle top above the base (body 0.61 + lid 0.05)', 660.0, 8, 'Read (scene)')
    add('D1_body_height', 'D1', 'rim crown above the base', 610.0, 6, 'Read (scene 0.61)')
    add('D1_rim_diameter', 'D1', 'diameter over the rolled top bead', 463.0, 6, 'Read (scene 0.46)')
    add('D1_lid_diameter', 'D1', 'lid skirt diameter', 502.0, 6, 'Read (scene 0.50)')
    add('D1_lid_height', 'D1', 'lid crown + handle above the rim crown', 50.0, 5, 'Read (scene 0.05)')
    add('D1_foot_diameter', 'D1', 'bottom hoop diameter', 414.0, 10, 'Judgement; Lead 400 to 412')
    add('D1_rib_count_and_z', 'D1', 'three swaged ribs at z', list(D.D1_RIB_Z), 15, 'Judgement')
    add('D1_side_handles', 'D1', 'two strap loops at z 470, 45 proud', [2, 470.0, 45.0], [0, 25.0, 8.0], 'Judgement')
    add('D1_lid_clearance', 'D1', 'lid skirt inner radius minus rim bead radius', 8.5, 4, 'Derived')
    # placements
    add('street_bin_count', 'placements', 'public litter bins on the street', 3, 0, 'Judgement (section 7)')
    add('dustbin_count_and_x', 'placements', 'dustbins and their x', [2, 21.4, 22.0], [0, 0.03, 0.03], 'Read')
    add('dustbin_setback', 'placements', 'axis from the kerb\'s back edge', 1.6, 0.04, 'Read')
    add('B1_place', 'placements', 'K1 post x and |z|', [6.6, 3.62], [0.05, 0.03], 'Judgement')
    add('B2_place', 'placements', 'K1 post x and |z|', [35.2, 3.62], [0.05, 0.03], 'Judgement')
    add('B3_place', 'placements', 'K2 axis x and |z|', [44.0, 3.80], [0.05, 0.03], 'Judgement')
    add('walking_strip', 'placements', 'clear footway beside every bin', 0.68, 'at least', 'Read (railings target)')
    add('kerb_clear', 'placements', 'bin edge to the kerb back edge', 0.25, 'at least', 'Judgement')
    add('door_leaf_clear', 'placements', 'bin footprint to the nearest door leaf in x', 0.30, 'at least', 'Judgement')
    add('every_bin_within_3m_of_a_door_or_the_stop', 'placements', 'distance from each bin to the nearest shop door or the bus stop', 3.0, 'at most', 'the asset plan\'s rule as applied')
    # materials and wear
    add('wear_iron_share', 'K1', 'share of the post and bin surface with paint loss', [0.04, 0.08], 0.0, 'Read (wear target)')
    add('no_brand_text', 'all', 'council name, maker name, product name, crest, monogram on any mesh or texture', 0, 0, 'rule')
    add('no_alcohol_gambling_children', 'all', 'any alcohol, gambling or child image in any dressing or poster remnant', 0, 0, 'rule (canon)')
    add('dressing_separate', 'all', 'overflow litter in the bin\'s own mesh', 0, 0, 'rule (the brief)')
    add('tri_budget', 'all', 'triangles per kind', dict(K1=3500, K2=6000, D1=4500), 0.15, 'Judgement')
    return ch


def handover_block():
    return dict(
        glb='K1_pole_open_<A|B|C>.glb, K2_hooded_drum_<a|b|c>.glb, D1_dustbin_<a|b|c>.glb (metres, z up, scale 1, pivot as the frame says); the lid of D1 b is a separate mesh stood against the wall; the liner of K2 and the sack of K1 B are separate meshes; the overflow pieces are the dressing sets\' instanced meshes (one mesh per item, 150 to 600 triangles)',
        replaces='production/assets/street/clutter/litter-bin.glb and dustbin.glb, the recipe\'s CLUTTER_FOR_HELD (swing_bin and outdoor_bin to litter-bin) and the three E6 placements of the scene (public bins: x 8.0 east, x 30.0 east, x 33.0 west) with B1, B2 and B3; the dustbins keep the scene\'s E13 place',
        lettering='LITTER only; the font is the builder\'s pick from an OFL face (the asset plan: "lettering must be set in OFL fonts"); no other word; digits only for the asset stencil and the house number',
        materials='master materials per substance (painted steel, glass-fibre gelcoat, galvanised steel, rust, grime) with the per-asset masks of the asset plan; the sRGB values in materials are albedo, not render values',
        notes=['the bins carry no maker\'s name, no council name, no crest, no cypher',
               'K1\'s bin is hung along the street, not across it, so it takes no footway depth beyond its own 0.37 m; its letters face the building line',
               'tobacco is allowed (canon): scorch marks and cigarette ends stay; nothing else of the content rule is touched'])


if __name__ == '__main__':
    T = build()
    json.dump(T, open(os.path.join(HERE, 'target.json'), 'w'), indent=1)
    print('target.json written', os.path.getsize(os.path.join(HERE, 'target.json')) // 1024, 'KB', len(T['checks']), 'checks')
