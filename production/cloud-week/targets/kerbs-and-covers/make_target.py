#!/usr/bin/env python
"""Writes target.json for the kerbs-and-covers family (cloud week 42, 9 October 2026).

All numbers are millimetres unless a key says otherwise. Plan frame: x along the kerb, y across
(0 = the kerb face line at the channel, + toward the carriageway, - toward the footway), z up from the top of the
channel setts at the kerb foot. Run:  /home/user/.bpyenv/bin/python make_target.py
It keeps an existing "self_check" block out (self_check.py rewrites it).
"""
import json, math, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))


def arc(cx, cz, r, a0, a1, n=8):
    """points on a circle (y,z) from angle a0 to a1 degrees, n segments"""
    return [[round(cx + r * math.cos(math.radians(a0 + (a1 - a0) * i / n)), 2),
             round(cz + r * math.sin(math.radians(a0 + (a1 - a0) * i / n)), 2)] for i in range(n + 1)]


def srgb_to_lin(c):
    c = c / 255.0
    return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4


def lin_to_srgb(v):
    v = max(0.0, min(1.0, v))
    return 255.0 * (12.92 * v if v <= 0.0031308 else 1.055 * v ** (1 / 2.4) - 0.055)


# ---------------------------------------------------------------- sampled colours (tone-mapped 8k copy, medians of boxes)
# urban_street_03, ortho of the crossing (3 mm a pixel); the road beside the kerb is the anchor
ROAD_PHOTO = [96.7, 95.4, 100.7]
WEAR_ASPHALT_DRY = [89, 86, 80]  # Read: wear target surfaces.asphalt_dry (cloud week 42)
PHOTO_SAMPLES = {
    'asphalt_road': ROAD_PHOTO,
    'kerb_top_right_block': [137.9, 135.4, 138.2],
    'kerb_top_left_block': [153.0, 152.4, 160.8],
    'kerb_face_in_shade': [38.0, 38.1, 35.4],
    'flank_strip_right': [127.6, 125.0, 127.9],
    'concrete_ramp': [161.2, 153.3, 147.9],
    'footway_flag_pale': [134.6, 129.1, 127.9],
    'footway_flag_dark': [92.4, 89.0, 89.2],
    'lip_sett_blue_grey': [109.0, 114.0, 129.3],
    'lip_sett_pale': [157.0, 156.3, 159.7],
    'channel_setts_pale': [152.7, 146.8, 148.8],
    'channel_setts_dull': [115.2, 108.1, 109.3],
    'grate_bar_rust': [88.0, 75.0, 76.0],
    'grate_slot': [35.0, 31.0, 37.0],
    'bg_cover_plate': [112.0, 95.0, 85.0],
}


def albedo_from(sample):
    """sample sRGB in the photograph -> albedo sRGB on the wear target's road scale (linear ratio to the road)."""
    out = []
    for c in range(3):
        r = srgb_to_lin(sample[c]) / srgb_to_lin(ROAD_PHOTO[c])
        out.append(round(lin_to_srgb(r * srgb_to_lin(WEAR_ASPHALT_DRY[c]))))
    return out


def build():
    t = {}
    t['family'] = 'kerbs-and-covers'
    t['title'] = "Quay Street's kerbs, channel, gully grates and covers"
    t['written'] = '2026-10-09'
    t['units'] = 'mm (the .glb is in metres: divide by 1000), z up, scale 1'
    t['summary_line'] = (
        "Quay Street's kerb is dressed grey half-battered granite (125 mm upstand, about 190 mm top, 255 mm deep, blocks 0.8 to 1.2 m with "
        "9 mm joints) on most of its length and pale concrete on three stretches, the channel two courses of granite setts "
        "(225 mm; 255 mm for the concrete channel block), the dropped crossover a 3.0 m in-situ concrete ramp between granite flank strips with a row of setts as its "
        "15 mm lip, the gully grate a rust-brown 485 x 325 cast-iron rectangle with eight slots (not a 400 mm square), and the "
        "covers four cast patterns plus a tarmac-filled recess, all blank, none with a maker's mark; no tactile paving in 1990.")
    t['frame'] = {
        'plan': 'x along the kerb, y across (0 = kerb face line at the channel; + toward the carriageway), mm',
        'z': 'up from the top of the channel setts at the kerb foot (z = 0); kerb top z = +125; footway flags +120; road at the channel edge +6, then 1 in 40 up to +75 at 3 m',
        'pivot': ('kerb block: x at the block centre, y = 0, z = 0 (channel level); crossing assembly: x at the centre of the '
                  'gap between the two end blocks, y = 0, z = 0; grate and covers: centre of the lid, z = 0 at the top surface '
                  'of the lid (the surface it is set flush in); corner: the corner point on the face line, z = 0'),
        'glb': 'metres, z up, scale 1; one mesh per piece kind, the variants as extra material slots or separate meshes',
    }

    # ------------------------------------------------------------------ scene numbers (Read from SCENE-SLOTS.md, 8 Oct 2026)
    t['scene_numbers'] = {
        'source': 'production/cloud-week/targets/SCENE-SLOTS.md (read 9 October 2026), rows Kerb, Gully grate, Road and footway',
        'kind': 'Read',
        'kerb_upstand': 125, 'kerb_width': 125, 'kerb_depth': 255, 'kerb_block_length': 915,
        'channel_course_width': 255, 'crossover_width': 3000, 'crossover_centre_x_m': 22.5, 'crossover_upstand': 6,
        'crossover_side': 'west',
        'gully_grate_square': 400, 'gully_recess': 50, 'gully_dish': 30, 'gully_x_m': 12.0, 'gully_side': 'east',
        'carriageway_width': 6000, 'crossfall': '1 in 40', 'crown_above_channel': 75, 'footway_width': 2000,
    }

    # ------------------------------------------------------------------ materials
    pm = PHOTO_SAMPLES
    mats = {
        'note': ('sRGB are CLEAN-surface albedos on the wear target\'s road scale (asphalt_dry 89/86/80): each is the photograph\'s '
                 'sampled colour divided by the road beside it in linear light, times the wear target\'s asphalt_dry. Grime, shade '
                 'and wet are the wear family\'s (gutter_grime, grate_wear), so the dark kerb face of the photographs is NOT baked in. '
                 'Roughness 0-1 is Judgement.'),
        'granite_grey': {'name': 'dressed grey granite, fine speckle, worn smooth on top', 'srgb': albedo_from([142, 140, 144]),
                         'kind': 'Photo (kerb tops 138/135/138 and 153/152/161 against road 97/95/101), anchored to wear target kerb_granite 128/126/122',
                         'roughness': 0.55, 'roughness_words': 'matt, polished a little by feet on the top (0.40) and rougher on the face (0.70)',
                         'metal': 0},
        'granite_blue_grey': {'name': 'darker blue-grey granite (about 1 block in 5)', 'srgb': albedo_from([112, 116, 126]),
                              'kind': 'Photo (lip setts 109/114/129)', 'roughness': 0.55, 'metal': 0},
        'granite_pink_grey': {'name': 'grey granite with a pink cast (about 1 block in 20)', 'srgb': albedo_from([150, 138, 138]),
                              'kind': 'Photo (one pinkish sett 150/132/130 in the lip row), Judgement for its share',
                              'roughness': 0.55, 'metal': 0},
        'sett_pale_worn': {'name': 'channel setts, pale and worn, mortar lines dark', 'srgb': albedo_from([152.7, 146.8, 148.8]),
                           'kind': 'Photo (channel setts 153/147/149 near the grate, 115/108/109 farther along)',
                           'roughness': 0.60, 'metal': 0},
        'sett_dull': {'name': 'channel setts, dull and silted', 'srgb': albedo_from([115.2, 108.1, 109.3]), 'kind': 'Photo',
                      'roughness': 0.70, 'metal': 0},
        'concrete_kerb': {'name': 'pale warm-grey concrete kerb, fine aggregate showing, worn', 'srgb': [140, 134, 126],
                          'kind': 'Judgement; Photo (Birbeck Street kerb reads pale grey-brown with sparkling aggregate)',
                          'roughness': 0.75, 'metal': 0},
        'concrete_ramp': {'name': 'in-situ concrete, brushed, exposed fine aggregate, speckled pale and dark', 'srgb': albedo_from(pm['concrete_ramp']),
                          'kind': 'Photo (161/153/148, speckle std about 14 grey levels on the photograph)',
                          'roughness': 0.80, 'metal': 0},
        'flag_pale': {'name': 'old concrete flag, pale', 'srgb': albedo_from(pm['footway_flag_pale']), 'kind': 'Photo; the footway family owns the flags', 'roughness': 0.75, 'metal': 0},
        'cast_iron_grate': {'name': 'cast iron gully grating, bare grey-black iron: the BASE is the wear target\'s iron_grate; the rust-brown bars come from its grate_wear (mark 100/72/56)', 'srgb': [58, 54, 52],
                            'expected_composite_srgb_on_bars': [92, 74, 66],
                            'kind': 'Read: the base is the wear target\'s surfaces.iron_grate 58/54/52 (one base colour, so the rust is not put on twice); 92/74/66 is the EXPECTED RESULT on the bars after grate_wear, for checking it (Photo: bars 88/75/76 to 125/109/103 on a view where the road is 97/95/101)',
                            'roughness': 0.70, 'roughness_words': 'rough, rust matt; bar tops polished by wheels (0.45)', 'metal': 1,
                            'metal_note': 'bare iron is metal 1; the rust skin is dielectric: use metal 0.3 where rust covers more than half'},
        'cast_iron_cover': {'name': 'cast iron or steel cover, dark grey-brown, leaf-stained', 'srgb': [78, 66, 58],
                            'kind': 'Photo (Bethnal Green cover plate 112/95/85 under litter; 04 cover pale in sun); Judgement',
                            'roughness': 0.65, 'metal': 1, 'metal_note': 'metal 0.4 on rusty edges and stud sides'},
        'mortar_pale': {'name': 'pale grey pointing and bedding mortar', 'srgb': [150, 146, 138], 'kind': 'Judgement', 'roughness': 0.9, 'metal': 0},
        'bitumen_joint': {'name': 'black bitumen joint filler', 'srgb': [30, 28, 28], 'kind': 'Photo (dark gap between ramp and flank strips)', 'roughness': 0.6, 'metal': 0},
        'tarmac_infill': {'name': 'tarmac in a recessed cover, the road\'s own colour', 'srgb': [89, 86, 80], 'kind': 'Photo; = wear asphalt_dry', 'roughness': 0.85, 'metal': 0},
    }
    t['materials'] = mats
    t['photo_samples'] = {'road_anchor': ROAD_PHOTO, 'wear_asphalt_dry': WEAR_ASPHALT_DRY, 'samples': PHOTO_SAMPLES,
                          'method': 'median of boxes on the 3 mm ortho of urban_street_03 (see make_previews.py frame MAIN); linear-light ratio to the road, rescaled to the wear target\'s asphalt_dry'}

    # ------------------------------------------------------------------ pieces
    K_UP, K_W, K_D = 125, 190, 255
    # half-battered face (Photo PM26): vertical to z = 45, then back 25 mm by z = 100, then a rounded arris R 25 to the flat top
    kg_section = ([[0, -(K_D - K_UP)], [0, 45], [-25, K_UP - 25]] + arc(-50, K_UP - 25, 25, 0, 90, 8)[1:] +
                  [[-K_W, K_UP], [-K_W, -(K_D - K_UP)]])
    KC_UP, KC_W, KC_R = 110, 160, 60
    kc_section = ([[0, -(K_D - KC_UP)], [0, KC_UP - KC_R]] + arc(-KC_R, KC_UP - KC_R, KC_R, 0, 90, 10)[1:] +
                  [[-KC_W, KC_UP], [-KC_W, -(K_D - KC_UP)]])

    pieces = {}
    pieces['kerb_granite'] = {
        'what': 'straight dressed granite kerb block (the old quarter\'s kerb; about 85 % of the run)',
        'section_yz': kg_section,
        'section_note': ('section in the plan frame: face at y = 0, back at y = -190; HALF-BATTERED face: vertical from the foot to z = 45, then sloping back 25 mm by z = 100 (about 25 degrees from vertical), then the top arris rounded R 25 (centre y -50, z 100) into a flat top 140 wide; back vertical; '
                         'buried to z = -130 so the block is 255 deep (the street\'s depth). The buried part is not seen: a plain box is enough.'),
        'upstand': K_UP, 'top_width': K_W, 'depth': K_D, 'top_arris_radius': 25, 'end_arris_radius': 10,
        'face_batter': {'vertical_to_z': 45, 'set_back_mm': 25, 'at_z': 100, 'kind': 'Photo-consistent with PM26 and the upstand together, not separately measured; Judgement for the split. PM01, PM02 and PM26 read one ray, from the camera to the middle of the arris, against one foot: read with a vertical face PM26 puts the arris middle at about 129 mm, PM01 and PM02 at 113 to 118, and a review at two places read 129 and 133 with a vertical face and 119 to 123 with the 25 mm batter, so upstand 125 with a 25 mm batter stands'},
        'length_mm': {'min': 800, 'max': 1200, 'mean': 1000, 'law': 'random in 800 to 1200, mean 1000, never two equal in a row'},
        'joint_mm': {'width': 9, 'tolerance': 3, 'fill': 'silt-dark open joint, no mortar fillet on the face; 3 mm dark line in the top'},
        'laying_tolerance': {'face_line_offset_between_blocks': 4, 'top_level_step_between_blocks': 3, 'tilt_deg_max': 1.5,
                             'note': 'blocks settle: a joint may open to 15 mm in 1 of 12'},
        'surface': {'top': 'fine-picked granite, grain 1 to 3 mm, polished at the front half', 'face': 'self-faced, rougher, darker with grime',
                    'end_faces': 'dressed, edges chipped'},
        'material': 'granite_grey', 'variants': ['granite_grey', 'granite_blue_grey', 'granite_pink_grey'],
        'variant_share': {'granite_grey': 0.75, 'granite_blue_grey': 0.20, 'granite_pink_grey': 0.05},
        'pivot': 'block centre on the face line at channel level',
    }
    pieces['kerb_concrete'] = {
        'what': 'straight precast concrete bullnosed kerb (replacement stretches; three runs of 4 to 8 blocks per side)',
        'section_yz': kc_section,
        'section_note': 'front arris a full rounding R 60 over the top 60 mm, flat top 100 mm, upstand 110 (worn street: 125 less overlay), 255 deep; section in the plan frame (face y = 0, back y = -160)',
        'upstand': KC_UP, 'top_width': KC_W, 'depth': K_D, 'top_arris_radius': KC_R,
        'length_mm': {'fixed': 915, 'note': 'the street\'s 3 ft block: Read from SCENE-SLOTS'},
        'joint_mm': {'width': 8, 'tolerance': 3, 'fill': 'grey pointing, flush, cracked in places'},
        'surface': {'top': 'weathered concrete with fine aggregate showing, sparkling', 'face': 'smooth, pitted, paint blips allowed (yellow loading marks belong to the lines family)'},
        'material': 'concrete_kerb', 'pivot': 'block centre on the face line at channel level',
    }
    # ---- channel
    pieces['channel_setts'] = {
        'what': 'granite sett channel beside the granite kerb: two courses, laid long side along the kerb',
        'width_total': 225,
        'width_note': 'Photo 226 +-15 (PM06, two courses of 4.5 inch setts); Read: the scene\'s 255 is kept for the concrete channel block beside the concrete kerb',
        'courses': [{'name': 'A (kerb side)', 'y0': 0, 'y1': 115, 'across': 115}, {'name': 'B', 'y0': 115, 'y1': 225, 'across': 110}],
        'sett_along_mm': {'min': 130, 'max': 230, 'mean': 180}, 'joint_mm': 12,
        'sett_top': {'z': 0, 'dome_mm': 4, 'level_scatter_mm': 3, 'note': 'course B sits up to 5 mm lower where worn'},
        'pointing': 'dark mortar recessed 8 mm, partly lost: 1 joint in 4 open to 20 mm',
        'meets_asphalt': 'asphalt edge at y = 225 stands 6 mm proud of the setts and runs out at 1 in 40; ragged edge, 10 to 50 mm wander; over about a third of a run the asphalt laps 30 to 50 mm onto course B (the visible channel is then 180 to 195); the setts stay modelled to 225 underneath',
        'colour': ['sett_pale_worn', 'sett_dull', 'granite_blue_grey'],
        'colour_share': {'sett_pale_worn': 0.35, 'sett_dull': 0.50, 'granite_blue_grey': 0.15,
                         'why': 'the clean setts at these shares average about 1.78 times the road in linear light; after the wear family\'s channel body (x 0.85) about 1.51, and about 1.45 with the dark joints: inside the 1.35 to 1.7 of check channel_over_road_brightness'},
        'long_fall': '1 in 80 along the kerb toward the gully (Judgement); cross-section flat',
        'section_yz_course_A': [[0, -140], [0, 0], [115, 0], [115, -140]], 'section_yz_course_B': [[115, -140], [115, 0], [225, 0], [225, -140]],
        'profile_yz': {'channel_top': [[0, 0], [225, 0]], 'asphalt_edge': [[225, 0], [225, 6], [260, 7.0]], 'road_surface': [[260, 7.0], [3000, 75.4]],
                       'note': 'z of the road = 6 + (y - 225) / 40 (crossfall 1 in 40, Read) up to the crown, 75 mm above the channel at 3.0 m (Read: scene); the asphalt edge stands 6 mm up on the setts'},
    }
    pieces['channel_concrete'] = {
        'what': 'concrete channel block beside the concrete kerb (the scene\'s 255 channel course)',
        'section_yz': [[0, -125], [0, 0], [255, 0], [255, -125]], 'width': 255, 'depth': 125, 'length_mm': 915, 'joint_mm': 8,
        'kind': 'Read: the scene says "in the kerb\'s own concrete"; Judgement: BS 7263 channel 255 x 125 x 915 (a search lead, not read)',
        'material': 'concrete_kerb',
    }
    # ---- crossover
    W_C = 3000
    pieces['crossover'] = {
        'what': 'dropped vehicle crossing as photographed (urban_street_03): two square-ended kerb blocks, two granite flank strips, an in-situ concrete ramp, a row of setts as the lip, 12 mm bitumen joints between them',
        'width_between_kerb_ends': W_C, 'width_note': 'Read: SCENE-SLOTS 3.0 m. The photographed crossing (a house gate) is 2150 between the kerb ends; the form, not the width, is taken.',
        'end_blocks': {'piece': 'kerb_granite', 'end_face': 'square, vertical, arris R 10, the front 30 mm of the top chipped on one of the two'},
        'lip_row': {'y0': -125, 'y1': 0, 'sett_along_mm': 170, 'joint_mm': 10, 'across_mm': 125, 'top_z': 15,
                    'top_z_note': 'Photo: the lip stands 12 to 20 mm above the channel courses (dark shadow band 30 mm in the ortho); the scene\'s 6 mm is flatter than the photograph',
                    'count': 'ceil(3000 / 180) = 17 setts, lengths 150 to 190, colours blue-grey, pale grey, one pink-grey in 8',
                    'material': ['granite_blue_grey', 'granite_grey', 'granite_pink_grey']},
        'ramp': {'plan_x': [-W_C / 2 + 12, W_C / 2 - 12], 'plan_y': [-917, -137], 'z_at_lip': 15, 'z_at_back': 120, 'gradient': '1 in 7.4 (105 over 780)',
                 'joint_to_lip_and_flanks_mm': 12, 'surface_yz': [[-137, 15], [-917, 120]], 'material': 'concrete_ramp',
                 'texture': 'brushed, exposed fine aggregate; one hairline crack across the ramp; a joint line 25 mm wide at the back edge',
                 'back_edge': 'meets the footway flags at y = -917 with a 10 to 20 mm bitumen/mortar joint'},
        'flank_strips': {'piece': 'granite strip', 'width_mm': 155, 'length_mm': 715, 'plan_y': [-917, -202], 'top_z': 120,
                         'inner_face_x_from_kerb_end': 0, 'inner_face_note': 'Photo: the right strip (140 wide) has its inner face on the kerb block end; the left strip (170 wide) has a splayed dark inner face about 45 mm wide; the street takes both at 155 with the inner faces on the block ends',
                         'joint_to_ramp': 'bitumen 12 mm', 'material': 'granite_grey'},
        'taper_variant': {'what': 'precast concrete dropper (taper block): one per side if the builder prefers a precast crossing',
                          'plan': [915, 160], 'top_z_start': 110, 'top_z_end': 5, 'gradient': '1 in 8.7 (105 over 915)',
                          'kind': 'Judgement: a search lead (BS 7263 HB2 to BN3 dropper, 125 x 255 to 125 x 150, 1:9) names it; no photograph of one reached',
                          'material': 'concrete_kerb'},
    }
    # ---- corners
    pieces['kerb_corner_mitre'] = {
        'what': 'external corner formed by two granite blocks mitred at the bisector (planter and build-out corners)',
        'angle_deg': 133, 'angle_tolerance_deg': 5, 'angle_note': 'Photo PM27 (urban_street_01, the review\'s reading of the kerb\'s road edges and the yellow lines): 133 +-5 degrees interior; 90 allowed for a street corner', 'joint_mm': 9,
        'blocks_each_arm_mm': 900, 'material': 'granite_grey',
        'top_at_corner': 'arris round continues round the mitre; a small chip at the corner',
    }
    pieces['kerb_corner_radius'] = {
        'what': 'street corner on a radius: granite blocks cut to the curve',
        'radius_face_mm': 6500, 'radius_note': 'Photo urban_street_04: least-squares circle through the yellow line of the corner, 6.8 m (PM16), line about 0.2 m off the kerb, +-0.6 m: face 6.5 m',
        'block_chord_mm': 1200, 'joint_mm': 9, 'joint_direction': 'radial', 'material': 'granite_grey',
        'channel': 'the two setts courses follow the curve; setts cut slightly wedge-shaped',
    }
    # ---- gully grates
    ga = {'overall_along_kerb': 485, 'overall_across': 325, 'slot_count': 8, 'slot_width': 29, 'slot_length': 285, 'slot_pitch': 57}
    ga['slot_span'] = (ga['slot_count'] - 1) * ga['slot_pitch'] + ga['slot_width']
    ga['end_wall_along'] = (ga['overall_along_kerb'] - ga['slot_span']) / 2
    ga['end_wall_across'] = (ga['overall_across'] - ga['slot_length']) / 2
    pieces['gully_grate_A'] = {
        'what': 'road gully grating, rectangular, slots across the channel (perpendicular to the kerb): the street\'s grate, east side x 12 m',
        **ga,
        'slot_centres_x': [round((i - (ga['slot_count'] - 1) / 2) * ga['slot_pitch'], 2) for i in range(ga['slot_count'])],
        'bar_width': ga['slot_pitch'] - ga['slot_width'], 'bar_depth_z': 45, 'slot_taper': 'slot 29 wide at the top, 25 at the bottom (casting draught)',
        'open_fraction': round(ga['slot_count'] * ga['slot_width'] * ga['slot_length'] / (ga['overall_along_kerb'] * ga['overall_across']), 3),
        'open_fraction_note': 'slot area over plan area, 8 x 29 x 285 / (485 x 325); the photograph\'s black fraction is about 0.41 (review)',
        'edge': 'bar top edges chamfered 2 mm; frame flush with the setts; the grate sits with its kerb-side edge 100 mm from the kerb foot and 200 mm of it lies beyond the 225 channel in the carriageway',
        'plan_position': {'y0': 100, 'y1': 425, 'note': 'Photo: y 102 to 426 from the kerb foot (foot = base of the lip row, row 403)'},
        'pot': 'black void below the slots 300 deep (gully pot), silt at the bottom: the slots read black',
        'dish': 'the asphalt is dished 15 mm toward the grate over 150 mm on the carriageway side (the yellow line kinks around it); the scene\'s dish 30 / recess 50 are replaced',
        'material': 'cast_iron_grate', 'pivot': 'centre of the grate at the top surface',
        'variants': 3, 'variant_note': 'wear states: rust and silt, bar tops polished, one slot half-blocked with a leaf; mirrored along the kerb allowed',
    }
    pieces['gully_grate_B'] = {
        'what': 'second grate design: 7 slots trimmed to an oval field (Birbeck Street); the quay end\'s grate if the builder wants variety',
        'slot_count': 7, 'slot_width': 28, 'slot_pitch': 58, 'slot_lengths': [125, 250, 350, 395, 350, 250, 125],
        'bar_width': 30, 'lifting_holes': {'count': 2, 'diameter': 25, 'on_long_axis': True, 'beyond_end_slot_centres_mm': 55, 'kind': 'Photo, rough (review): two round lifting holes about 25 across on the long axis beyond the two end slots'},
        'cast_marks': 'raised marks are cast on its centre bar: they stay BLANK (no_lettering)',
        'overall_along_kerb': 490, 'overall_across': 445, 'kind': 'Photo, rough (perspective view, +-15 %); Judgement for the frame; the slots are about half the pitch (28 wide, bars 30)',
        'material': 'cast_iron_grate', 'pivot': 'centre of the grate at the top surface',
    }
    # ---- covers
    pieces['cover_stud_square'] = {
        'what': 'square double-triangular cast cover: two triangular leaves split on a diagonal, a lattice of raised square studs (pattern 1)',
        'outer': [960, 960], 'outer_note': 'Photo 980 x 920 +-70 on the review\'s reading (Bethnal Green entrance, 0.9 m from the nadir of the panorama); PM18',
        'frame_rim': 20, 'lid_inner': [920, 920], 'lid_recess_below_frame_mm': 0,
        'leaves': {'count': 2, 'shape': 'right-angled triangles', 'split': 'one diagonal joint corner to corner, 5 mm wide',
                   'studs_on_the_joint': 'the studs the joint crosses are cut into right-angled half-studs (half-triangles) on both leaves; at least five are visible along it',
                   'kind': 'Photo (review, bethnal_green_entrance): one diagonal joint, half-studs along it'},
        'pattern': {'type': 'square_stud_lattice', 'stud_mm': 45, 'pitch_mm': 95, 'stud_height_mm': 4, 'edge_margin_mm': 10,
                    'count': [10, 10], 'stud_sides': '15 degree draught, top flat, arrises worn round 1 mm'},
        'keyhole_diameter_mm': 20,
        'keyholes': 'one round keyhole 20 mm across per leaf, near the middle of the leaf (Photo: one seen in one leaf; Judgement for the other)',
        'boss': {'size_mm': [80, 40], 'height_mm': 3, 'where': 'near one end of the joint (the lower one), on the joint line', 'blank': True,
                 'note': 'a small raised blank oblong boss, where a maker\'s mark would go: it stays blank (no_lettering)'},
        'lifting_pockets': 'none (replaces the earlier two oblong pockets): the lifting points are the round keyholes',
        'material': 'cast_iron_cover', 'gap_to_surround_mm': 10, 'surround': 'block paving or flags, edge blocks cut to it',
        'use': 'footway and carriageway, 2 on the street', 'pivot': 'centre of the lid at its top surface',
    }
    pieces['cover_round_600'] = {
        'what': 'round manhole cover in the carriageway, 600 class (pattern 2)',
        'frame_outer_diameter': 690, 'lid_diameter': 590, 'frame_depth': 68, 'frame_ring_width': 50,
        'kind': 'frame size Read from the CC0 Poly Haven model water_manhole_cover (690.76 mm overall, 67.6 mm deep, a modelled asset, not a photograph); 600 class Judgement',
        'pattern': {'type': 'basket_lug', 'lug_mm': [36, 10.5], 'cell_mm': [71.4, 83.5], 'lug_height_mm': 2.5, 'rim_plain_mm': 25,
                    'lugs_in_cell': [{'orientation': 'horizontal', 'centre_mm': [0, 0]}, {'orientation': 'horizontal', 'centre_mm': [35.7, 41.75]},
                                     {'orientation': 'vertical', 'centre_mm': [35.7, 6]}, {'orientation': 'vertical', 'centre_mm': [0, 47.75]}],
                    'note': ('a centred lattice (review, read off the 1k displacement map of the Poly Haven CC0 texture metal_grate_rusty, a scan of a real cast tread, 500 mm tile): rows 41.75 apart; along each row a horizontal and a vertical lug alternate every 35.7, so the horizontal lugs repeat every 71.4; each row is shifted 35.7 from the last so a vertical lug sits above and below each horizontal one; the vertical lugs sit 6 mm below their row\'s line. So each 71.4 x 83.5 cell holds 2 horizontal and 2 vertical lugs. Lug 36 x 10.5 x 2.5.')},
        'lettering': 'none (a generic WATER or GAS is allowed only once a photograph shows it)',
        'material': 'cast_iron_cover', 'use': '2 in the carriageway', 'pivot': 'centre of the lid at its top surface',
    }
    pieces['cover_recessed_footway'] = {
        'what': 'large recessed cover in the footway, telecom-style and blank (pattern 3, footway)',
        'outer': [1180, 660], 'outer_err': [50, 100], 'frame_rim_total': 110,
        'frame_steps': 'frame top cast with raised oblong lugs, two staggered rows along the long sides, more across the wider left end; use the P2 tread lug (36 x 10.5 x 2.5, rows 41.75 apart) [Photo for the pattern, Judgement for the size]. The rim is two bands, an outer 45 wide level with the flags and an inner 65 wide stepped 12 down, both lugged',
        'frame_lugs': {'lug_mm': [36, 10.5], 'height_mm': 2.5, 'row_pitch_mm': 41.75, 'long_sides': 'two staggered rows on each long side (second row shifted 35.7)', 'left_end': 'three columns of vertical lugs', 'right_end': 'two columns of vertical lugs', 'kind': 'Photo for the pattern (a telephoto of the 8k at 7 m cannot measure the lug), Judgement for the size and counts'},
        'infill': [960, 440], 'infill_material': 'flag or concrete tray lid, pale, 25 mm chamfer on its edge, top 8 mm below the flags',
        'material': 'cast_iron_cover', 'use': '1 or 2 on the street, west footway beside the yard', 'pivot': 'centre of the infill at the flag surface',
        'kind': 'Photo urban_street_03 (a view 7 m away, the near edge sharp, the far edge soft)',
    }
    pieces['cover_recessed_road'] = {
        'what': 'recessed cover filled with tarmac in the carriageway (pattern 3, road)',
        'outer': [1000, 1050], 'outer_err': 50, 'frame_rim': 40,
        'look': 'only a 15 mm dark hairline in the tarmac, a darker square, grass and moss at the corners, a crack running out of one corner',
        'material': 'tarmac_infill', 'use': '1 on the street', 'pivot': 'centre at the road surface',
        'kind': 'Photo urban_street_02 (an estate road, same tarmac look as a 1990 reinstatement)',
    }
    pieces['cover_road_double_leaf'] = {
        'what': 'long two-leaf cover with a fine stud tread in the carriageway (pattern 4, road)',
        'outer': [1820, 620], 'outer_err': 150, 'leaf_split': 'two equal leaves with a 15 mm gap across the middle', 'leaf_split_kind': 'Judgement, not Photo: on a 4 mm ortho of urban_street_04 the studded field is divided by more than one seam, at least one oblique to the long axis, and no single cross-joint at the middle was seen; its period is unproven (it sits in a fresh reinstatement), so one on the street',
        'pattern': {'type': 'square_stud_lattice', 'stud_mm': 18, 'pitch_mm': 33, 'stud_height_mm': 3, 'edge_margin_mm': 30, 'lattice_rotation_deg': 45},
        'surround': 'pale mortar and a patch of lighter tarmac, 150 wide', 'material': 'cast_iron_cover',
        'kind': 'Photo urban_street_04 (seen 7 m away: shape and pattern, not exact numbers)', 'use': '1 on the street', 'pivot': 'centre at the road surface',
    }
    pieces['service_small'] = {
        'what': 'small footway covers: stopcock, gas, telecom-style blank',
        'water_stopcock': {'lid': [135, 135], 'shape': 'round', 'frame': 175, 'pattern': 'plain with a slot 30 x 8', 'kind': 'Judgement (no photograph reached)'},
        'gas_box': {'lid': [240, 130], 'shape': 'rectangle', 'frame': [290, 180], 'pattern': 'plain, one 25 x 8 slot at each end', 'kind': 'Judgement (no photograph reached)'},
        'telecom_blank': {'lid': [360, 160], 'shape': 'rectangle recessed, flag infill', 'frame': [410, 210], 'surround': 'pale mortar 30 wide',
                          'kind': 'Photo urban_street_04 (a small recessed cover with a pale mortar surround, 7 m away, +-30 %)'},
        'lettering': 'none; if a letter is ever wanted: "SV" or "WATER" or "GAS" cast 20 mm high, no maker, no company',
        'material': 'cast_iron_cover', 'count': '3 stopcock, 2 gas, 1 telecom', 'pivot': 'centre at the flag surface',
    }
    pieces['tactile_paving'] = {
        'what': 'none on Quay Street in 1990',
        'why': ('A blister surface at crossings was first laid in Parliament Square in 1983 as a trial, and the Department\'s guidance on it '
                'dates from 1998 (search summaries, leads, not read). A minor street\'s dropped kerb in 1990 has plain flags or concrete: no blisters, no corduroy.'),
        'kind': 'Judgement, with leads',
    }
    t['pieces'] = pieces

    # ---------------------------------------------------------------- the photographed crossing instance (for the overlay)
    t['reference_instance'] = {
        'photo': 'urban_street_03, ortho frame MAIN (yaw 272.2, 3 mm a pixel), two planes: ground (camera height 1.6 m) and top (1.475 m = the kerb top, 125 mm up)',
        'gap_between_kerb_ends': 2150, 'foot_line_distance_from_camera': 3791, 'gap_centre_local_x': -672,
        'foot_line_note': 'foot = the base of the lip row and of the kerb face: the row where the dark face and its shadow start to rise toward the setts (row 403 of the 3 mm frame, +-5 px); the soft shadow under the kerb makes the middle of the rise (row 407) 12 mm lower',
        'channel_width': 225, 'lip': {'y0': -125, 'y1': 0}, 'ramp_back_y': -917, 'ramp_front_y': -137,
        'flank': {'width': 155, 'y0': -917, 'y1': -202, 'left_x': [-1403, -1232], 'right_x': [1075, 1215]},
        'kerb_top_rear_y': -190, 'gully': {'x_centre': -751, 'y0': 102, 'y1': 426, 'along': 489, 'across': 324},
        'note': 'the channel here is 226 wide by the gradient of its edge (PM06); the street\'s granite channel is 225, the concrete one 255 (Read); the grate position and size are as photographed (its x_centre -751 is the fitted centre of the slot field, PM30: seven slot centroids, std 1.0 mm)',
    }
    t['photo_frames'] = {
        'MAIN': {'pano': 'urban_street_03', 'yaw_deg': 272.2, 'x0_m': -2.3, 'x1_m': 1.1, 'z0_m': 3.15, 'z1_m': 5.0, 'mm_per_px': 3.0, 'size_px': [1134, 617],
                 'ground_image': 'ph-urban_street_03-crossover-gully-ortho.jpg', 'top_image': 'ph-urban_street_03-crossover-top-ortho.jpg',
                 'camera_height_ground_m': 1.6, 'camera_height_top_m': 1.475,
                 'row_to_distance': 'distance from the camera in mm = 5000 - 3 * row; local x in mm = -2300 + 3 * column'},
    }
    # ------------------------------------------------------------------ data blocks
    import target_data as D
    import measure as M
    t['sources'] = D.sources()
    t['unreached'] = D.unreached()
    pms = D.photo_measurements()
    for pm in pms:
        pm['result'] = M.compute(pm)
    t['photo_measurements'] = pms
    t['photographs_win'] = D.photographs_win()
    t['variants'] = D.variants()
    t['wear'] = D.wear()
    chk = D.checks()
    for c in chk:
        if c['name'] == 'colour_of_granite_top':
            c['expected'] = mats['granite_grey']['srgb']
    t['checks'] = chk
    t['could_not_settle'] = D.could_not_settle()
    t['to_read_when_the_network_opens'] = D.to_read_later()
    t['edge_probes'] = D.edge_probes()
    t['handover'] = D.handover()
    t['scale_fit'] = D.SCALE_FIT
    return t


if __name__ == '__main__':
    t = build()
    p = os.path.join(HERE, 'target.json')
    old = {}
    if os.path.exists(p):
        try:
            old = json.load(open(p))
        except Exception:
            old = {}
    # carry over blocks written by other scripts
    for k in ('photo_measurements', 'sources', 'decisions', 'variants', 'wear', 'checks', 'edge_probes', 'could_not_settle',
              'unreached', 'previews', 'photographs_win'):
        if k in old and k not in t:
            t[k] = old[k]
    json.dump(t, open(p, 'w'), indent=1)
    print('wrote', p, len(json.dumps(t)))
