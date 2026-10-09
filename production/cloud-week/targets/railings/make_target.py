#!/usr/bin/env python
"""Writes target.json of the railings family from the hand-read numbers below, anchors.json, photo_measurements.json and frames.py.
    /home/user/.bpyenv/bin/python make_target.py
Everything is millimetres unless a key says _m (metres, the street's frame).  Each number carries its kind: Read (printed in the repository),
Photo (measured on a photograph, method and error given), Derived, Judgement (a trade or period guess, said so)."""
import json, math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from frames import FRAMES, CAMERAS

ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
anchors = json.load(open(os.path.join(HERE, 'anchors.json')))
PM = json.load(open(os.path.join(HERE, 'photo_measurements.json')))
HR = PM['hand_reads']
R3B = PM['R3B']

T = {}
T['family'] = 'railings'
T['title'] = "Quay Street's kerbside guard rail, its quay railing and chain, and the boundary railings the street does not have"
T['written'] = '2026-10-09'
T['units'] = 'millimetres unless a key ends in _m (metres, the street recipe\'s frame); the .glb is metres, z up, scale 1'

# ------------------------------------------------------------------------------------------------------------------ scene numbers (Read)
T['scene_numbers'] = [
    dict(id='guard_rail_line', file='production/cloud-week/targets/SCENE-SLOTS.md', find='1.0 high; posts 0.05; rails 0.04; five infill bars of 0.025 a panel', what='the scene\'s stand-in: 1.0 high, posts 0.05, rails 0.04, five infill bars of 0.025 a panel', value=dict(height_m=1.0, post_m=0.05, rail_m=0.04, bars=5, bar_m=0.025)),
    dict(id='guard_rail_place', file='production/cloud-week/targets/SCENE-SLOTS.md', find='east side, x 10.0 to 12.0 (one 2.0 m panel, beside the gully), 0.25 m back from the kerb', what='one 2.0 m panel, east side, x 10.0 to 12.0, 0.25 m back from the kerb', value=dict(x0_m=10.0, x1_m=12.0, setback_from_kerb_m=0.25)),
    dict(id='scene_panels', file='production/specs/vignette-scene.json', find='"panels": 1,', what='E8 has one panel', value=1),
    dict(id='scene_setback', file='production/specs/vignette-scene.json', find='"setback_from_kerb_m": 0.25', what='E8 set-back 0.25 m', value=0.25),
    dict(id='scene_infill', file='production/specs/vignette-scene.json', find='"infill_per_panel": 5', what='E8 five infill bars', value=5),
    dict(id='scene_post_d', file='production/specs/vignette-scene.json', find='"post_diameter_m": 0.050', what='E8 post 0.050', value=0.05),
    dict(id='scene_rail_d', file='production/specs/vignette-scene.json', find='"rail_diameter_m": 0.040', what='E8 rail 0.040', value=0.04),
    dict(id='scene_infill_d', file='production/specs/vignette-scene.json', find='"infill_diameter_m": 0.025', what='E8 infill 0.025', value=0.025),
    dict(id='feet_post0', file='production/specs/vignette-feet.json', find='"x_m":10,"z_m":3.375,"foot_y_m":0.05625', what='post 0 stands at x 10, z 3.375, its foot at y 0.05625 (the footway there)', value=dict(x_m=10.0, z_m=3.375, foot_y_m=0.05625)),
    dict(id='feet_post1', file='production/specs/vignette-feet.json', find='"name":"rail_post1","bom":"E8_guard_railing","edge":"east_footway","region":"x12_18","x_m":12,"z_m":3.375', what='post 1 stands at x 12, z 3.375', value=dict(x_m=12.0, z_m=3.375)),
    dict(id='pieces_lower_rail', file='production/specs/vignette-pieces.json', find='"name":"rail_bar0_45","shape":"cyl","surface":"metal","asset":null,"x_m":11,"y_m":0.50625,"z_m":3.375', what='the stand-in\'s lower rail is 0.45 above its foot (y 0.50625 over 0.05625)', value=dict(above_foot_m=0.45)),
    dict(id='stallriser', file='production/cloud-week/targets/SCENE-SLOTS.md', find='stallriser 0.60 high, 0.15 proud', what='stallriser 0.15 proud of the frontage line', value=dict(proud_m=0.15)),
    dict(id='pilaster', file='production/cloud-week/targets/SCENE-SLOTS.md', find='pilasters 0.35 wide, 0.10 proud', what='pilasters 0.10 proud', value=dict(proud_m=0.10)),
    dict(id='frontage_z', file='production/specs/terrace-fronts.md', find='`frontage_z_m` 5.125', what='the frontage line is z 5.125 (the kerb face z 3.0 + the kerb 0.125 + the footway 2.0)', value=5.125),
    dict(id='kerb_target_top', file='production/cloud-week/targets/kerbs-and-covers/TARGET.md', find='115 mm upstand, about 170 mm top', what='the kerbs target: granite kerb 115 upstand, 170 top', value=dict(upstand=115, top=170)),
    dict(id='kerb_target_flags', file='production/cloud-week/targets/kerbs-and-covers/TARGET.md', find='footway flags +110', what='the kerbs target: footway flags +110 over the channel', value=110),
    dict(id='bollard_chain_bar', file='production/cloud-week/targets/bollards/TARGET.md', find='plain short link, a 13 mm bar', what='the bollards target\'s plain chain: short link, 13 mm bar', value=13),
    dict(id='bollard_post_spacing', file='production/cloud-week/targets/bollards/TARGET.md', find='post spacing 3.0 m', what='the bollards target\'s chain posts 3.0 m apart', value=3000),
    dict(id='bollard_lugs', file='production/cloud-week/targets/bollards/TARGET.md', find='a cast **D-lug** on each side of the shaft at z **420 and 840**', what='K5 chain eyes at z 420 and 840', value=[420, 840]),
    dict(id='bollard_sag', file='production/cloud-week/targets/bollards/target.json', find='"sag_mm": 150', what='K5 chain sag 150 (Judgement there)', value=150),
    dict(id='kit_jetty_x', file='tools/art-recipes/south-quay/south_quay_geom.py', find='"jetty_x": (220.0 - 350.0, 240.0 - 350.0)', what='the jetty strip x -130 to -110', value=[-130.0, -110.0]),
    dict(id='kit_jetty_end', file='tools/art-recipes/south-quay/south_quay_geom.py', find='"jetty_end_y": 385.0 - 400.0', what='the jetty\'s end at y -15', value=-15.0),
    dict(id='kit_cope', file='tools/art-recipes/south-quay/south_quay_geom.py', find='COPING_W_M = 0.60', what='the cope 0.60 across', value=0.60),
    dict(id='kit_parapet', file='tools/art-recipes/south-quay/south_quay_geom.py', find='kit.box(par, x_a, x_a + 0.80, -100.0 - COPING_W_M, at["jetty_end_y"] - 8.0,', what='the jetty\'s stone parapet on the seaward side: x -129.4 to -128.6, ending at y -23.0', value=dict(x=[-129.4, -128.6], y_end=-23.0)),
    dict(id='kit_light', file='tools/art-recipes/south-quay/south_quay_geom.py', find='c = ((jx0 + jx1) / 2.0, at["jetty_end_y"] - 4.5)', what='the harbour light stands at x -120, y -19.5', value=dict(x=-120.0, y=-19.5, plinth_half=1.4)),
    dict(id='kit_no_railing', file='production/art/south-quay/README.md', find='Ladder | 0.45 m wide, rungs 0.30 m apart', what='the kit has a ladder and bollards and a stone parapet on the jetty; it has no railing on any quay edge', value='none'),
    dict(id='asset_plan_rows', file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='2 m guard-rail panel (posts, rails, infill); two-rail tube railing with chain', what='the asset plan\'s linear kit rows', value='2 m panel; two-rail tube railing with chain'),
    dict(id='asset_plan_counts', file='production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md', find='Guard railing; quay railing with chain; fences', what='guard railing 1 kit, 1 to 3 panels; quay railing with chain 1 kit, along the quay', value='1 kit; 1 kit'),
    dict(id='hull_chain_edge', file='production/research/atlas-01/CONTINUATION.md', find='chain-edged quay', what='R08, River Hull, 1989 (a photograph read by an earlier session, not reachable here): a chain-edged quay', value='chain-edged'),
    dict(id='e8_not_tree_guard', file='production/specs/vignette-bill-of-materials.md', find='**E8 is not the railing we hold.**', what='the held trunk_protection_railing is a tree-pit guard, not E8', value='not E8'),
    dict(id='yard_gap', file='production/specs/vignette-scene.json', find='The 3.0 m between west_south\'s end at x=21.0 and this block\'s start at x=24.0 is the YARD ENTRANCE', what='the yard entrance is a 3.0 m gap in the data, x 21.0 to 24.0, west side', value=[21.0, 24.0]),
]

# ------------------------------------------------------------------------------------------------------------------ street frame numbers
T['street_frame'] = dict(
    note='the street recipe\'s frame, metres: x along the street (0 at its south end, + north), z across (the crown 0, + east); the kerb face at z +-3.0; the kerb\'s top 0.125 wide in the scene (170 in the kerbs target); the footway 2.0 wide to the frontage line z 5.125',
    kerb_face_z_m=3.0, kerb_back_scene_z_m=3.125, kerb_back_kerbs_target_z_m=3.170, frontage_z_m=5.125, stallriser_face_z_m=5.125 - 0.15, pilaster_face_z_m=5.125 - 0.10,
    channel_above_crown_m=-0.075, flags_above_channel_mm_kerbs_target=110, footway_crossfall='1 in 40, rising away from the kerb',
    foot_y_scene_m=0.05625, foot_y_kerbs_target_m=round(-0.075 + 0.115, 5),
    quay_frame='the south-quay kit\'s frame: x along Quay Street (0 at its south end, + north, so the quay is at x -70), y across (east +), z up; the apron and the copes at +0.05 over the crown')

# ------------------------------------------------------------------------------------------------------------------ calibration
cal = dict(method='horizon method of the bollards and kerbs targets (calibrate.py): camera height above a brick wall\'s foot = 75 mm x tan(angle of the foot) / (course pitch in tan units); the pitch by a fold of the column-band profile', horizon_anchors=anchors, panoramas={})
for pano, C in CAMERAS.items():
    P = dict(h_cam=C['h_cam'], err=C['err'], anchors=C['anchors'], why=C['why'])
    if 'quoted' in C: P['quoted'] = C['quoted']
    cal['panoramas'][pano] = P
cal['camera_note'] = ('None of the three panoramas was taken at 1.6 m: 0.97 (Bethnal Green), 1.12 (Urban Street 01 and Limehouse) above the ground each object stands on. '
                      'Every length below is +-6 % in absolute size (the stated errors); counts, ratios and pitches are exact to the pixel.')
T['calibration'] = cal

# ------------------------------------------------------------------------------------------------------------------ photograph frames
T['photo_frames'] = {k: dict(F) for k, F in FRAMES.items()}

# ------------------------------------------------------------------------------------------------------------------ photograph measurements
T['photo_measurements'] = dict(R3B_auto=R3B, hand_reads=HR)


def _circle(r, n=32, cx=0.0, cy=0.0):
    return [[round(cx + r * math.cos(2 * math.pi * k / n), 3), round(cy + r * math.sin(2 * math.pi * k / n), 3)] for k in range(n)]


def _stadium(length, width, n=8):
    r = width / 2.0
    L = length - width
    pts = []
    for k in range(n + 1):
        a = -math.pi / 2 + math.pi * k / n
        pts.append([round(L / 2 + r * math.cos(a), 3), round(r * math.sin(a), 3)])
    for k in range(n + 1):
        a = math.pi / 2 + math.pi * k / n
        pts.append([round(-L / 2 + r * math.cos(a), 3), round(r * math.sin(a), 3)])
    return pts


def _tube(od, wall):
    return dict(outer=_circle(od / 2.0), inner=_circle(od / 2.0 - wall), od=od, wall=wall)


def _catenary(x0, x1, z_eye, sag, step=100.0):
    span = x1 - x0
    lo, hi = 1.0, 1e8
    for _ in range(200):
        mid = (lo + hi) / 2
        if mid * (math.cosh(span / (2 * mid)) - 1) > sag:
            lo = mid
        else:
            hi = mid
    a = (lo + hi) / 2
    xm = (x0 + x1) / 2
    n = int(round(span / step))
    return [[round(x0 + span * k / n, 2), round(z_eye - sag + a * (math.cosh((x0 + span * k / n - xm) / a) - 1), 2)] for k in range(n + 1)]


# ------------------------------------------------------------------------------------------------------------------ the kinds
kinds = {}

# ============================================================== A1: the kerbside pedestrian guard rail panel (E8)
H = 1000.0
post_od, post_wall = 48.3, 3.2
cap_od, cap_t = 52.0, 8.0
top_od, top_wall = 42.4, 2.6
bot_od, bot_wall = 33.7, 2.6
top_axis = H - top_od / 2.0
bot_axis = 200.0
c2c = 2000.0
xface = c2c / 2.0 - post_od / 2.0
n_bars, bar_d = 17, 12.0
gap = (2 * xface - n_bars * bar_d) / (n_bars + 1)
pitch = gap + bar_d
bar_x = [round(-xface + gap + bar_d / 2.0 + i * pitch, 2) for i in range(n_bars)]
A1 = dict(
    id='A1', name='guard_rail_panel', title='Kerbside pedestrian guard rail, one 2.0 m panel between two posts (the scene\'s E8)',
    basis='Judgement: no photograph of a guard rail was reachable (section 3 of TARGET.md). The scene\'s numbers (2.0 m panel, 1.0 high, post 0.05, rail 0.04) are kept where nothing contradicts them; the infill, the lower rail and every detail are Judgement supported by the photographed bar railings R3B, R3A and R3D (bar pitch 78 to 116) and by search-summary leads (12 mm bars at no more than 100 clear)',
    frame='local: x along the panel (0 at its middle), y across (0 on the rail line, + toward the carriageway), z up from the flag top at the posts; pivot at the middle of the panel on the ground',
    panel=dict(centre_to_centre=c2c, height=H, post=dict(od=post_od, wall=post_wall, height=H, section='round steel tube, 48.3 mm outside diameter (1.5 inch nominal bore)', x=[-c2c / 2, c2c / 2]),
               cap=dict(od=cap_od, thickness=cap_t, z=[H - cap_t, H], edge_radius=2.0, what='a flat pressed-steel plug cap, driven into the tube and welded all round, 2 mm bead; its top is the panel\'s top'),
               top_rail=dict(od=top_od, wall=top_wall, axis_z=round(top_axis, 2), top_z=H, x=[-xface, xface], section='round steel tube 42.4 mm (1.25 inch nominal bore); its top is flush with the post cap'),
               bottom_rail=dict(od=bot_od, wall=bot_wall, axis_z=bot_axis, underside_z=round(bot_axis - bot_od / 2, 2), x=[-xface, xface], section='round steel tube 33.7 mm (1 inch nominal bore)'),
               infill=dict(count=n_bars, diameter=bar_d, section='round solid mild-steel bar, vertical, welded to the rails', clear_gap=round(gap, 2), pitch=round(pitch, 2), x=bar_x, z=[bot_axis, round(top_axis, 2)],
                           gap_rule='the clear gap between bars and between a bar and a post is at most 100 (a 100 mm sphere may not pass, the present-day safety rule: the infill is 12 mm bars at 110 to 112 centres, gaps 98 to 100, a lead only; the photographed bar railings have gaps of 60 to 105)'),
               weld=dict(bead=3.0, what='a 3 mm fillet bead round each rail end where it butts the post (saddle cut), and 2 mm at each bar end; ground smooth is NOT done: the beads show under the paint as slightly ridged rings')),
    ground=dict(kind='the posts are concreted into the footway; the flags are cut round them', ring_gap=20.0, ring_fill='dark bitumen or tarmac joint, 20 mm wide, flush with the flags, no collar plate and no base plate', below_ground_not_modelled=400.0),
    bbox=dict(x=[-(c2c / 2 + cap_od / 2), c2c / 2 + cap_od / 2], y=[-cap_od / 2, cap_od / 2], z=[0, H]),
    ends='the panel ends at its posts: an end post is the same post with the same cap; no return, no end rail, no stay (the one panel stops at x 12.0 beside the gully)',
    joins='a second panel (not on this street) would share the post: the rails of both butt the same post; the bars are not offset',
    edges='no sharp edges: the tube ends are saddle-cut and welded; the cap\'s rim is rounded R2; bar ends are cut square and hidden in the rail welds',
    fixings='none visible: no bolts, no lugs, no plates (welded panel on welded posts, the standard form of the 1976 British Standard, Judgement)',
    marks='none: no maker\'s plate, no council number, no crest, no stencilled letters. A paint-over of a number is NOT drawn.',
    paint=dict(default='black gloss paint over galvanising', srgb=[24, 24, 26], roughness_words='semi-gloss, dulled by two winters', roughness=0.42, metal=0,
               note='the same black as the street\'s cast bollards (bollards target K1/K2: (24, 24, 26)); the black of the photographed ironwork measures (22, 21, 21) (R3A) and (23, 24, 28) (the K5 post, LHB) and is the one paint all of it shares'),
    wear=['the road face grimed brown-grey by tyre spray to about 500 mm, the footway face cleaner; a dirt line at the foot',
          'top rail polished bright (steel, 150, 150, 152) along its upper surface where hands rest, in patches 150 to 300 long',
          'paint chipped to grey galvanising or primer at the weld beads, at the lower rail\'s road side (kicked) and on the post caps; rust bloom (110, 60, 32) at the posts\' feet and at the weld rings, 0 to 1',
          'one or two bars bent out 5 to 15 mm at 300 to 600 high (a bumped panel), 0 to 2 per panel',
          'a lean of the posts of 0 to 1 degree toward the carriageway',
          'a sticker or poster remnant on the top rail 0 to 2 (pale paper scraps, no lettering)',
          'cigarette ends and a sweet wrapper lodged between the kerb and the post (the litter set\'s, not this kit\'s)'])
kinds['A1'] = A1
A1['profiles'] = dict(
    note='sections and profiles as point lists, millimetres: tubes as outer and inner circles of 32 points (x across, y along the rail), the cap as an (r, z) lathe profile from the axis up, the weld bead as a fillet triangle, the ground ring as an annulus',
    post_section=_tube(post_od, post_wall), top_rail_section=_tube(top_od, top_wall), bottom_rail_section=_tube(bot_od, bot_wall), bar_section=dict(outer=_circle(bar_d / 2.0), od=bar_d),
    cap_rz=[[0.0, H - cap_t], [cap_od / 2 - 2.0, H - cap_t], [cap_od / 2 - 0.6, H - cap_t + 0.6], [cap_od / 2, H - cap_t + 2.0], [cap_od / 2, H - 2.0], [cap_od / 2 - 0.6, H - 0.6], [cap_od / 2 - 2.0, H], [0.0, H]],
    weld_fillet=[[0.0, 0.0], [3.0, 0.0], [0.0, 3.0]],
    ground_ring=dict(outer=_circle(post_od / 2 + 20.0, 48), inner=_circle(post_od / 2, 48), width=20.0))

# ============================================================== Q2: the quay tube railing (two-rail, and rail with chain)
Q_bay = 3000.0
q_post_od, q_post_wall, q_post_h = 76.1, 5.0, 1100.0
q_top_od, q_low_od = 48.3, 42.4
q_top_axis, q_low_axis = 1000.0, 500.0
q_xface = Q_bay / 2 - q_post_od / 2
eye_hole_d, eye_from_post = 24.0, 45.0
q_eye_x = q_bay_eye = Q_bay / 2 - q_post_od / 2 - eye_from_post
chain_sag = 200.0
span_eye = 2 * q_eye_x
arc = span_eye + 8.0 * chain_sag ** 2 / (3.0 * span_eye)
Q2 = dict(
    id='Q2', name='quay_tube_railing', title='Quay tube railing: two tube rails on round steel posts (Q2a), or one tube rail and a swag of chain (Q2b)',
    basis='Judgement: no photograph of a tube railing on a quay was reachable. The chain is the bollards target\'s plain chain (Read there) and its sag is Photo on the marina chain (LHB, 200 to 235). The asset plan names the kit ("two-rail tube railing with chain"); the Hull photograph R08 of 1989 (read by an earlier session) shows a chain-edged quay',
    frame='local: x along the run (0 at the middle of a bay), y across (0 on the rail line, + toward the water), z up from the apron at the post foot; pivot at the middle of the bay on the ground',
    bay=dict(centre_to_centre=Q_bay, allowed=[3000.0], note='bays of 3.0 m (the bollards target\'s post spacing)'),
    post=dict(od=q_post_od, wall=q_post_wall, height=q_post_h, section='round steel tube, 76.1 mm (3 inch nominal bore)', cap=dict(kind='pressed domed cap, welded', od=80.0, rise=14.0, z=[q_post_h - 14.0, q_post_h]),
              base_plate=dict(size=[200.0, 200.0], thickness=12.0, holes=dict(diameter=18.0, pitch=150.0, count=4), fixing='four M16 studs in the cope with hex nuts, 24 across flats and 13 high, studs 10 proud of the nuts',
                              grout='25 mm cement grout bedding, a 20 mm fillet round the plate, stained dark'), weld='a 5 mm fillet all round the post foot on the plate'),
    top_rail=dict(od=q_top_od, wall=3.2, axis_z=q_top_axis, top_z=q_top_axis + q_top_od / 2, x=[-q_xface, q_xface], section='round steel tube 48.3 mm; saddle-welded to the posts'),
    low_rail=dict(od=q_low_od, wall=2.6, axis_z=q_low_axis, x=[-q_xface, q_xface], section='round steel tube 42.4 mm (Q2a only)'),
    chain=dict(replaces='the low rail (Q2b only)', eyes=dict(z=q_low_axis, x=[-q_eye_x, q_eye_x], ear=dict(width=40.0, height=70.0, thickness=8.0, hole_diameter=eye_hole_d, hole_centre_from_post_surface=eye_from_post, what='a flat-bar ear welded to the post on the rail line, facing the bay; one each side of every post')),
               link=dict(bar=13.0, kind='plain short link', inner_length=39.0, inner_width=18.0, outer_length=65.0, outer_width=44.0, pitch=39.0, note='the bollards target\'s plain chain, unchanged (agrees)'),
               sag=chain_sag, sag_basis='Photo LHB: the marina chain\'s two swags sag 215 (upper) and 240 (lower), mean 227 +-35, over a 2840 span (8 %); the bollards target\'s 150 is Judgement and is low; 200 (7 %) here',
               span_between_eyes=round(span_eye, 2), arc_length=round(arc, 1), links=int(round(arc / 39.0)), curve='a catenary hanging from the two eye holes: z(x) = z_eye - sag + a (cosh(x/a) - 1) with a = span^2 / (8 sag)'),
    bbox=dict(x=[-(Q_bay / 2 + q_post_od / 2), Q_bay / 2 + q_post_od / 2], y=[-100.0, 100.0], z=[0, q_post_h]),
    ends='a run ends at a post of the same kind; the last bay may be shorter only on a return (none on this quay). At a corner two runs share one post, rails mitred to it',
    edges='saddle cuts and fillet welds; the cap\'s rim R3; the base plate\'s edges R2',
    marks='none',
    paint=dict(default='black, satin over galvanising', srgb=[24, 24, 26], roughness_words='satin, chalky on the sea side', roughness=0.55, metal=0, note='the same black and roughness as the K5 chain post and the K6 mooring bollards beside it (bollards target); the nuts and studs bright steel (150, 150, 152), dull rust at the threads'),
    wear=['salt bloom (pale, dry) on the sea face of posts and rails to 1.0 m; rust at the base plate, the nuts and the weld rings, 0 to 1',
          'paint rubbed bright on the upper face of the top rail at the walking places (150, 150, 152)',
          'the chain black, rubbed bright where the links touch (the bollards target); links slightly rusty at their crossings',
          'a rope scuff on one post at 400 to 600 high, 0 to 1 per run',
          'the apron around the plates stained dark by oil and rain'])
kinds['Q2'] = Q2
_hex = [[round(13.856 * math.cos(math.pi / 6 + k * math.pi / 3), 3), round(13.856 * math.sin(math.pi / 6 + k * math.pi / 3), 3)] for k in range(6)]
Q2['profiles'] = dict(
    note='sections and profiles as point lists, millimetres',
    post_section=_tube(q_post_od, q_post_wall), top_rail_section=_tube(q_top_od, 3.2), low_rail_section=_tube(q_low_od, 2.6),
    cap_rz=[[0.0, q_post_h], [20.0, q_post_h - 3.0], [34.0, q_post_h - 8.0], [40.0, q_post_h - 12.0], [40.0, q_post_h - 14.0], [38.05, q_post_h - 14.0]],
    base_plate_outline=[[-100.0, -100.0], [100.0, -100.0], [100.0, 100.0], [-100.0, 100.0]], base_plate_holes=[[-75.0, -75.0], [75.0, -75.0], [75.0, 75.0], [-75.0, 75.0]], hole_diameter=18.0,
    nut_hex_outline=_hex, nut_across_flats=24.0, nut_height=13.0, stud_diameter=16.0, stud_above_nut=10.0,
    ear_outline=dict(outline=[[0.0, -35.0], [(eye_from_post + 20.0), -35.0], [(eye_from_post + 20.0), 35.0], [0.0, 35.0]], hole_centre=[eye_from_post, 0.0], hole_diameter=eye_hole_d, thickness=8.0),
    link_inplane=dict(outline=_stadium(65.0, 44.0), hole=_stadium(39.0, 18.0)), link_edge_on=[[-32.5, -6.5], [32.5, -6.5], [32.5, 6.5], [-32.5, 6.5]],
    catenary_xz=_catenary(-q_eye_x, q_eye_x, q_low_axis, chain_sag), catenary_note='z of the chain\'s centre line every 100 mm along x, eyes at z 500, lowest point z 300')

# ============================================================== reserve kinds, photographed, NOT placed on the street
R3B_k = dict(
    id='R3B', name='park_railing_tall', title='Tall cast-iron park railing on a brick plinth with a hinge post (RESERVE, not on Quay Street)', placed=False, frame_id='R3B',
    basis='Photo, Bethnal Green Entrance (2019), the main photograph: 1 mm a pixel elevation at 0.97 +-0.06 m; lengths +-6 %',
    plinth=dict(coping_top_z=HR['R3B']['coping_top_z'], stone_coping='a stone slab about 50 thick with a weathered top, overhanging the brick by about 25', brick='red-brown brick, four courses at 75 below the coping, moss and lichen on the north face',
                pier=dict(width=HR['R3B']['pier_width'], top='a stone pier cap with a low pyramidal weathering at the coping level')),
    rails=dict(bottom_axis_z=HR['R3B']['bottom_rail_axis_z'], mid_axis_z=HR['R3B']['mid_rail_axis_z'], top_axis_z=HR['R3B']['top_rail_axis_z'], section='flat bar about 20 high by 10 thick, bars passed through or riveted to them (not resolved)'),
    bars=dict(pitch=R3B['bar_pitch_mm'], count_measured=len(R3B['bar_centres_s_mm']), first_s=R3B['bar_fit_first_s_mm'], diameter=17.0, diameter_err=3.0, section='round', tall_every=2,
              short_tip_z=HR['R3B']['short_bar_tip_z'], tall_tip_z=HR['R3B']['tall_bar_tip_z'], head_rz=HR['R3B']['bar_head']['v'], foot='a small ball end (about 20 across) a few mm below the bottom rail',
              leaf_note='the gate leaf right of the hinge post is swung open toward the camera: the plane magnifies it (its bars read at 88.9) so it is not measured', note='all bars at 78.5 (three inches is 76.2, 3 % less, inside the 6 % scale error); every second bar rises 1075 above the middle rail to a spire; the others stop at the middle rail with a small spear (z 1225)'),
    post=dict(shaft_width=HR['R3B']['post_shaft_width'], collar_width=HR['R3B']['post_collar_width'], urn_width=HR['R3B']['urn_width'], top_z=HR['R3B']['post_top_z'], kind='cast iron, round, with a fluted collar at the top rail, a vase and a spire; a boss and a strap hinge at the bottom rail level (a gate stile)'),
    height_to_tip=HR['R3B']['tall_bar_tip_z']['v'], spacing_of_posts='not seen: one hinge post in 3.9 m of railing',
    paint=dict(srgb=[24, 24, 26], note='black, semi-gloss, chalky on the plinth side; measured medians of the dark pixels (36, 43, 30) are polluted by foliage; the R3A and LHB blacks are (22, 21, 21) and (23, 24, 28)'),
    wear=['paint flaking at the post collars; bright rust spots at the bar feet', 'moss and lichen on the plinth and a green-black stain under the coping', 'a notice board and a locked-site sign wired to the bars (not drawn)'])
R3A_k = dict(
    id='R3A', name='area_railing_on_dwarf_wall', title='Area railing on a two-stage dwarf wall in front of a housing block (RESERVE, not on Quay Street)', placed=False, frame_id='R3A',
    basis='Photo, Bethnal Green Entrance (2019): oblique view, 10 mm a pixel along the wall, lengths +-8 %; heritage replica or 1980s work: unknown',
    wall=dict(top_z=HR['R3A']['wall_top_z'], string_z=HR['R3A']['wall_string_z'], courses='lower stage 4 courses of blue-black engineering brick under a blue bullnose string, red wall five stretcher courses, a blue bullnose coping course; one brick thick (215, Judgement)'),
    rails=dict(bottom_axis_z=HR['R3A']['bottom_rail_axis_z'], mid_axis_z=HR['R3A']['mid_rail_axis_z'], top_axis_z=HR['R3A']['top_rail_axis_z']),
    bars=dict(pitch_all=HR['R3A']['bar_pitch_all'], tall_first_s=HR['R3A']['tall_first_s'], tall_tip_z=HR['R3A']['tall_tip_z'], thick_width=HR['R3A']['bar_thick_width'], pattern='thick tall bars with fleur-de-lis heads every 233, thin short bars with small lily plaques between them to the mid rail'),
    post=dict(top_z=HR['R3A']['post_top_z'], shaft_width=HR['R3A']['post_shaft_width'], kind='cast post with a vase and ball, scroll knees to the top rail'),
    paint=dict(srgb=[22, 21, 21], note='black'))
import numpy as _np
_r3d_fit = _np.polyfit(_np.arange(10), _np.array(HR['R3D']['bar_centres_s']['v'], float), 1)
R3D_k = dict(
    id='R3D', name='low_garden_railing_and_gate', title='Low green railing, wall and gate of a council-estate front garden (RESERVE, not on Quay Street)', placed=False, frame_id='R3D',
    basis='Photo, Urban Street 01 (2019): 1 mm a pixel elevation at 1.12 +-0.06 m; lengths +-6 %; a 1960s to 80s estate form',
    wall=dict(top_z=HR['R3D']['wall_top_z'], courses='eight courses of dark brick at 75 plus a header coping; no piers in the window'),
    rails=dict(bottom_axis_z=HR['R3D']['bottom_rail_axis_z'], top_axis_z=HR['R3D']['top_rail_axis_z'], section='flat bar'),
    bars=dict(pitch=dict(v=round(_r3d_fit[0], 2), err=3, how='line fit of the ten hand-read bar centres (hand_reads.R3D.bar_centres_s)'), first_s=round(_r3d_fit[1], 2), width=HR['R3D']['bar_width'], tip_z=HR['R3D']['bar_tip_z'], section='round, plain small spear points'),
    gate=dict(width=HR['R3D']['gate_width'], top_z=HR['R3D']['gate_top_z'], pattern='a leaf of plain bars with two C-scrolls at mid height and a scroll at the foot, hung from a brick pier'),
    paint=dict(srgb=HR['R3D']['paint_srgb']['v'], name='dark green', roughness=0.5, note='the only coloured ironwork reached; a council-estate green'))
kinds['R3B'] = R3B_k
R3B_k['profiles'] = dict(bar_head_rz=HR['R3B']['bar_head']['v'], bar_head_error=HR['R3B']['bar_head']['err'],
                         hinge_post_rz=[[HR['R3B']['post_shaft_width']['v'] / 2, 1990], [HR['R3B']['post_collar_width']['v'] / 2, 2000], [HR['R3B']['post_collar_width']['v'] / 2, 2035], [42.5, 2060], [42.5, 2110], [HR['R3B']['urn_width']['v'] / 2, 2150], [HR['R3B']['urn_width']['v'] / 2, 2200], [30, 2250], [12, 2300], [5, 2350], [0, HR['R3B']['post_top_z']['v']]],
                         note='(r, z) from the ground; read by eye on the 1 mm elevation, +-15 (blur 6 mm)')
kinds['R3A'] = R3A_k
kinds['R3D'] = R3D_k
T['kinds'] = kinds

# ------------------------------------------------------------------------------------------------------------------ placements
street_axis_z = 3.375
posts = [dict(id='E8_post0', x_m=10.0, z_m=street_axis_z), dict(id='E8_post1', x_m=12.0, z_m=street_axis_z)]
quay_run_basin = [[-110.4, round(-36.4 + 3.0 * k, 2)] for k in range(8)]
quay_run_tip = [[round(-110.4 - 3.0 * k, 2), -15.4] for k in range(1, 7)]
T['placements'] = dict(
    rule='frames: A1 in the street recipe\'s frame (x along, z across, metres); Q2 in the south-quay kit\'s frame (x along Quay Street, y across, metres)',
    street=[dict(id='E8', kind='A1', side='east', count=1, panels=1, x_m=[10.0, 12.0], z_axis_m=street_axis_z, from_kerb_face_m=round(street_axis_z - 3.0, 4), behind_scene_kerb_back_m=round(street_axis_z - 3.125, 4),
                 behind_kerbs_target_back_m=round(street_axis_z - 3.170, 4), axis_basis='Read: vignette-feet.json (rail_post0/1 at z 3.375); the scene\'s "0.25 m back from the kerb" is taken from the kerb\'s back edge (3.125); the kerbs target widens the kerb to 170, leaving 0.205',
                 foot_note='the post feet stand on the flag top; the scene\'s foot level is y 0.05625 and the kerbs target\'s flag level is y 0.040: the builder reads the ground under the posts',
                 facing='the road side is the -z face (toward the carriageway)', beside='the gully at x 12.0 in the channel (the grate 0.44 x 0.29 in the kerbs target) and the fish market\'s frontage behind')],
    quay=[dict(id='Q2_basin_edge', kind='Q2a', frame='south-quay kit', line_x_m=-110.4, behind_nose_m=0.4, posts_xy_m=quay_run_basin, bays=7, bay_m=3.0, why='the jetty\'s basin edge, from the root side of the harbour light to its tip: the public walks out to the light'),
          dict(id='Q2_tip', kind='Q2b', frame='south-quay kit', line_y_m=-15.4, behind_nose_m=0.4, posts_xy_m=quay_run_tip, bays=6, bay_m=3.0, shares_post_with='Q2_basin_edge at (-110.4, -15.4)', why='the jetty\'s end in front of the harbour light: the same posts with the chain in place of the low rail'),
          dict(id='quay_unrailed', kind=None, why='the north quay and the east quay stay unrailed except the bollards target\'s K5 chain posts about the ladder (x -69.5, y -40.5 to -31.5): working berths with boats alongside; a railing would stop the lines. The cope nose stays bare.')],
    counts=dict(street_posts=2, quay_posts=len(quay_run_basin) + len(quay_run_tip), quay_bays=13),
    absent=dict(area_railings='none on Quay Street: every frontage stands on the building line (frontage_z 5.125, a doorstep only); the south-quay kit\'s walled yards have brick piers and boarded gates, no railings; no chapel or church stands on the street (the chapel is at x 100 in hook-cast.json, beyond the bend)',
                yard_gate='none: the yard mouth (x 21.0 to 24.0, west) is a 3.0 m gap with a dropped kerb, its two corners guarded by the bollards target\'s K1 posts, and the scene stands a held crowd-control barrier across it (E11, prop_crowd_control_barrier_0 at x 22.5, z -4.85); the town session decides whether it is ever gated',
                backdrop='the north approach\'s garden walls are knee-high stone boxes in the backdrop (terrace-front.py), not game objects'))

# ------------------------------------------------------------------------------------------------------------------ materials
T['materials'] = [
    dict(id='iron_black_semi', srgb=[24, 24, 26], roughness=0.42, roughness_words='semi-gloss, dulled', metal=0, use='A1 default; R3B, R3A'),
    dict(id='iron_black_satin', srgb=[24, 24, 26], roughness=0.55, roughness_words='satin, chalky', metal=0, use='Q2, and the K5 and K6 beside it'),
    dict(id='iron_green', srgb=[38, 56, 36], roughness=0.50, roughness_words='satin', metal=0, use='R3D'),
    dict(id='galvanised_grey', srgb=[118, 120, 122], roughness=0.5, roughness_words='dull sheen', metal=1, use='A1 variant: unpainted or chipped to the zinc'),
    dict(id='bright_steel_rub', srgb=[150, 150, 152], roughness=0.35, roughness_words='polished by hands', metal=1, use='top rails\' upper face, nuts, studs, chain contacts'),
    dict(id='rust', srgb=[110, 60, 32], roughness=0.85, roughness_words='dry, matt', metal=0, use='blooms at feet, welds, nuts'),
    dict(id='bitumen_joint', srgb=[40, 38, 36], roughness=0.8, roughness_words='dull', metal=0, use='the ring round the A1 posts'),
]

# ------------------------------------------------------------------------------------------------------------------ variants
T['variants'] = dict(
    models=dict(A1=1, Q2=2, R3B=1, R3A=1, R3D=1),
    note='one panel on the street, so one A1; the asset plan\'s "1 kit" holds. Q2 has two models (a, b) on one run each.',
    A1_conditions=[dict(id='A1_black_scuffed', share=0.6, srgb=[24, 24, 26], note='default: black, scuffed, rust at the feet'),
                   dict(id='A1_black_chipped', share=0.25, note='black with the chips down to grey zinc at the road side and the caps'),
                   dict(id='A1_galvanised', share=0.15, srgb=[118, 120, 122], note='unpainted dull zinc (a 1970s fitting left unpainted), rust at the welds')],
    seeds=dict(lean_deg=[0.0, 1.0], bent_bars=[0, 2], bend_mm=[5, 15], bend_z_mm=[300, 600], rust_foot=[0.0, 1.0], dirt_height_mm=[300, 600], rub_bright_patches=[0, 3], sticker_remnants=[0, 2], chips=[0, 10]),
    Q2_conditions=['Q2a: two rails, salt bloom and rust at the plates', 'Q2b: rail and chain, links rusted at the crossings'])

# ------------------------------------------------------------------------------------------------------------------ photographs win / disagreements
T['photographs_win'] = [
    dict(element='infill of the guard rail', book='the scene\'s stand-in: five 25 mm bars in 2.0 m (clear gaps of 308); the asset plan "posts, rails, infill"',
         photograph='every photographed bar railing has its bars at 78.5 (R3B), 94.5 (R3D) or 114 (R3A) centres, so clear gaps of 60 to 105; none has a gap over 105. No guard rail was photographed',
         chosen='seventeen 12 mm bars at 109.1 centres (clear gap 97.1): Judgement from the analogues and the search-summary lead; the five-bar stand-in is replaced'),
    dict(element='lower rail height', book='the stand-in has its lower rail at 0.45 (half height)', photograph='R3D\'s bottom rail is 60 above its wall; R3B\'s 445 above the ground with a 380 plinth below it; the bars of both run to the bottom rail', chosen='lower rail axis at 200: Judgement (no photograph)'),
    dict(element='tube sizes', book='post 50, rail 40', photograph='none', chosen='48.3 post and 42.4 top rail, 33.7 lower rail: the nearest standard tubes to the scene\'s 50 and 40 (Judgement; inside the scene numbers\' round-off)'),
    dict(element='the post cap', book='none', photograph='none (R3B has cast finials, R3D plain spear points: neither applies to a steel guard rail)', chosen='a flat plug cap flush with the rail top, Judgement'),
    dict(element='paint colour', book='"metal" in the scene', photograph='all photographed ironwork is black (22 to 24) except R3D\'s green (38, 56, 36)', chosen='black (24, 24, 26) default, galvanised grey and chipped variants'),
    dict(element='camera height', book='1.6 m (the street writer\'s default)', photograph='0.97 (Bethnal Green), 1.12 (Urban Street 01, Limehouse) at each object\'s ground', chosen='the anchors in section 4; sizes +-6 %'),
    dict(element='chain sag', book='the bollards target 150 (Judgement)', photograph='Photo LHB: 227 +-35 over 2840 (two swags: 215 and 240)', chosen='200 for Q2b; the bollards writer should raise K5\'s to 200'),
    dict(element='K5 post height', book='the bollards target 1135 at 1.17 m', photograph='LHB 1086 at 1.12 m (4.3 % lower, the same ratio as the camera heights, 1.12 / 1.17 = 0.957)', chosen='no change: agrees inside the errors'),
]

# ------------------------------------------------------------------------------------------------------------------ checks
def chk(name, what, expected, tol, unit, kind, basis='Judgement', **kw):
    d = dict(name=name, what=what, expected=expected, tol=tol, unit=unit, kind=kind, basis=basis)
    d.update(kw)
    return d

C = []
# A1
C += [
    chk('A1_panel_length', 'distance between the two post axes', 2000, 5, 'mm', 'A1', 'Read: the scene (2.0 m) and vignette-feet (x 10 and 12)'),
    chk('A1_height_to_top', 'top of the top rail and of the post caps above the flag top at the post', 1000, 10, 'mm', 'A1', 'Read: the scene (1.0 high)'),
    chk('A1_post_od', 'post outside diameter', 48.3, 3.0, 'mm', 'A1', 'Judgement (the scene 50)'),
    chk('A1_top_rail_od', 'top rail outside diameter', 42.4, 3.0, 'mm', 'A1', 'Judgement (the scene 40)'),
    chk('A1_bottom_rail_od', 'bottom rail outside diameter', 33.7, 3.0, 'mm', 'A1'),
    chk('A1_bottom_rail_axis', 'bottom rail axis above the flag', 200, 25, 'mm', 'A1'),
    chk('A1_bar_count', 'infill bars between the posts', 17, 1, 'count', 'A1'),
    chk('A1_bar_diameter', 'infill bar diameter', 12, 2, 'mm', 'A1'),
    chk('A1_bar_gap_max', 'largest clear gap between bars, and bar to post', 100, 0, 'mm (maximum)', 'A1', max=True),
    chk('A1_bar_gap', 'the clear gaps are equal', 97.1, 3.0, 'mm', 'A1'),
    chk('A1_bars_touch_rails', 'each bar\'s two ends lie within 1 mm of a rail axis', 0, 1.0, 'mm', 'A1'),
    chk('A1_cap_top', 'post cap top equals the rail top', 0, 2.0, 'mm', 'A1'),
    chk('A1_street_position', 'post axes at x 10.0 and 12.0, z 3.375', [10.0, 12.0, 3.375], 0.05, 'm', 'A1', 'Read: vignette-feet.json'),
    chk('A1_behind_kerb_back', 'axis behind the kerbs target\'s 170 kerb back edge (z 3.170)', 0.205, 0.05, 'm', 'A1', 'Derived'),
    chk('A1_walking_clear', 'clear footway between the panel\'s rear face (z 3.399) and the nearest fixed frontage projection (stallriser face z 4.975)', 1.576, 0.0, 'm (at least 0.68)', 'A1', 'Derived', minimum=0.68),
    chk('A1_no_deep_obstacle', 'no object deeper than 0.896 m stands behind the panel (x 9.5 to 12.5) between the rail and the frontage, so that 0.68 m remains: the fish market\'s 0.92 m crates may not stand there', 0.896, 0.0, 'm (maximum depth)', 'A1', 'Derived: 1.576 - 0.68', max=True),
    chk('A1_no_lettering', 'no lettering, number, crest, maker\'s mark or plate on any mesh or texture', 'none', 0, '-', 'A1', 'Read: canon, brief'),
    chk('A1_paint_albedo', 'base colour within 10 of the sRGB of the chosen condition', [24, 24, 26], 10, 'sRGB', 'A1'),
    chk('A1_bbox', 'overall size of the built panel', [2052.0, 52.0, 1000.0], 8.0, 'mm', 'A1'),
    chk('A1_outline_residual', 'largest distance between a built elevation outline and the target\'s at the same x', 0, 6, 'mm', 'A1'),
    chk('A1_foot_ring', 'dark joint ring round each post at the flags', 20, 6, 'mm (width)', 'A1'),
    chk('A1_lean', 'seed lean of a post', [0, 1], 0, 'deg (range)', 'A1'),
]
# Q2
C += [
    chk('Q2_bay', 'post axis to post axis', 3000, 30, 'mm', 'Q2', 'Read: the bollards target (3.0 m)'),
    chk('Q2_post_od', 'post outside diameter', 76.1, 4.0, 'mm', 'Q2'),
    chk('Q2_post_height', 'post top above the apron', 1100, 20, 'mm', 'Q2'),
    chk('Q2_top_rail_axis', 'top rail axis above the apron', 1000, 15, 'mm', 'Q2'),
    chk('Q2_top_rail_od', 'top rail outside diameter', 48.3, 3.0, 'mm', 'Q2'),
    chk('Q2_low_rail_axis', 'low rail (Q2a) or chain eye (Q2b) above the apron', 500, 15, 'mm', 'Q2'),
    chk('Q2_base_plate', 'base plate 200 x 200 x 12 with four nuts on a 150 square', [200, 200, 12], 3, 'mm', 'Q2'),
    chk('Q2_chain_bar', 'chain bar diameter, agreeing with the bollards target', 13, 1, 'mm', 'Q2', 'Read: bollards target'),
    chk('Q2_chain_sag', 'mid-span sag of the Q2b chain below its eyes', 200, 50, 'mm', 'Q2b', 'Photo (LHB 227 +-35)'),
    chk('Q2_chain_no_spikes', 'no spikes on any link', 'none', 0, '-', 'Q2b', 'Read: bollards target (plain chain)'),
    chk('Q2_basin_posts', 'eight posts on the line x -110.4, y -36.4 to -15.4 every 3.0', [-110.4, -36.4, -15.4], 0.05, 'm', 'Q2', 'Derived'),
    chk('Q2_tip_posts', 'six more posts on y -15.4, x -113.4 to -128.4 every 3.0', [-113.4, -128.4, -15.4], 0.05, 'm', 'Q2', 'Derived'),
    chk('Q2_behind_nose', 'rail line behind the cope nose (x -110 on the basin edge, y -15 at the tip)', 0.4, 0.05, 'm', 'Q2', 'Derived'),
    chk('Q2_clear_of_mooring', 'no post within 8 m of a K6 bollard (-110.75, -45) or a K7 cleat (-110.25, -52 to -64); nearest post y -36.4', 8.6, 0.0, 'm (at least 8.0)', 'Q2', 'Derived', minimum=8.0),
    chk('Q2_clear_of_light', 'tip rail at least 2.5 m from the harbour light\'s plinth face (y -18.1)', 2.7, 0.0, 'm (at least 2.5)', 'Q2', 'Derived', minimum=2.5),
    chk('Q2_walking_clear', 'a person on the jetty keeps at least 0.68 m between the rail and any fixed object (the jetty is 20 m across)', 19.6, 0.0, 'm (at least 0.68)', 'Q2', 'Derived', minimum=0.68),
    chk('Q2_paint_albedo', 'base colour within 10 of the sRGB', [24, 24, 26], 10, 'sRGB', 'Q2'),
    chk('Q2_no_lettering', 'no lettering, crest or maker\'s mark', 'none', 0, '-', 'Q2'),
]
T['checks'] = C

# ------------------------------------------------------------------------------------------------------------------ could not settle / to read / handover
T['could_not_settle'] = [
    'No photograph of a British pedestrian guard rail of any date was reachable: the whole of A1 other than the scene\'s 2.0 m, 1.0 m and the post and rail sizes is Judgement. Eight other panoramas (urban_street_03 and 04, cambridge, birbeck, canary_wharf, adams_place_bridge, roof_garden, greenwich_park) show none.',
    'Whether Quay Street\'s rail in 1990 was black, galvanised grey, white-and-black banded or green: all the photographed ironwork is black except one council green; black is the default and the others are variants.',
    'The lower rail\'s height and the infill\'s kind (round bar, flat bar, or open with two rails only). The 1983 and 1988 accident studies (search summaries) say the conventional rail of the 1980s hid the road from short pedestrians and that a see-through type did better, which supports dense infill for the rail of 1990; no number.',
    'Q2: whether a harbour authority of the Hook would rail the jetty tip; the kit has no railing and the asset plan names one. The Hull 1989 photograph (an earlier session\'s note) supports chain at a working quay edge, not a tube railing.',
    'The camera heights rest on 75 mm brick courses (73 to 79 mm if Victorian): +-6 %. The wall and pier anchors agree to 5 %; Limehouse\'s two own anchors (1.095, 1.052) are 6 % under the bollards target\'s paver readings (1.15, 1.17), and 1.12 is the mean.',
    'R3A is oblique (32 degrees): widths there are blur-doubled; only its heights, rails and pitches are used.',
    'The paint on the photographed ironwork has been renewed since 1990 and the panoramas are 2019: none of R3A, R3B, R3D or the K5 post is known to be older than 1990; a Victorian pattern is plausible for R3B.',
    'Whether the park railing\'s bar section is round or square (the blur hides it): round is assumed.',
    'The one photographed multi-rail tube railing (greenwich_park_02, a path edge) was not measured for want of an anchor: Q2\'s two-rail form (top 1000, low 500) is not checked against it; a five-rail form would be an alternative for the jetty.']
T['to_read_when_the_network_opens'] = [
    'BS 3049:1976 "Specification for pedestrian guard rails (metal)" (withdrawn 15 November 1995; BSI Knowledge or a standards retailer): post and rail sizes, infill, finish, classes; and BS 7818:1995, which replaced it',
    'Department for Transport Local Transport Note 2/09 "Pedestrian guardrailing" (assets.publishing.service.gov.uk), its history section; Kent County Council\'s pedestrian guardrail policy (democracy.kent.gov.uk), which dates guardrail from the 1930s',
    'Wikimedia Commons categories for pedestrian guard railings, railings in Britain and bollards and chains at quays, 1975 to 2000 photographs; Geograph squares of fishing towns (Whitby, Brixham, Grimsby, Hull, North Shields) 1980s to 1990s: the author, licence and date on each file page',
    'Peter Marshall\'s River Hull photograph of 1989 (Flickr 51040207776, the atlas\'s R08): the chain-edged quay, its posts and its chain, if the licence allows measuring',
    'Historic England: list entries for quay walls and railings (Truro, list entry 1201539, "quay walls and railings"; Bideford, 1282939, cast-iron fence posts with tubular bars and chains), the Historic England Archive\'s 1980s photographs of dock edges and street furniture',
    'The Health and Safety Executive\'s Docks Regulations 1988 and "Safety in Docks" approved code of practice (what edge protection a 1990 quay needed); Torbay and North Devon harbour edge-protection audits (summaries say working fish quay berths were left unfenced)',
    'Tyne and Wear HER and North Shields Fish Quay conservation area notes; 1980s street-furniture catalogues for guard-rail panels: sizes and finishes only, no makers\' marks',
    'The Traffic Signs Manual and the 1980s DoT "Roads in Urban Areas" guidance on guardrail set-back from the kerb (the scene\'s 0.25 m behind the kerb is a trade guess; a rule of about 0.45 m from the kerb face is remembered, not read)',
    'The street recipe\'s own reference photographs of the Hook sheet, if it shows a railing']
T['handover'] = dict(
    to_builder='A1 replaces the scene\'s five-bar stand-in at the same x and z; the posts keep the scene\'s x 10.0 and 12.0, z 3.375. Q2 is new to the south-quay kit: it needs a recipe step (fourteen posts, thirteen bays, the chain) or a placement from this target; the kit has no railing today.',
    to_bollards_writer='the chain: sag 200, not 150 (Photo LHB, two swags 215 and 240, mean 227 +-35); lug heights 800 and 405 here against 840 and 420 there (inside the errors); K5 height 1086 at 1.12 m against 1135 at 1.17 m (the same 4.3 % as the camera heights)',
    to_kerbs_writer='the kerb stands 0.205 m in front of the guard rail\'s axis (granite top 170, back edge z 3.170); the flag level at the post is y 0.040 against the scene\'s 0.05625',
    to_town_session='the fish market\'s crates (0.92 m deep) must not stand in x 9.5 to 12.5 behind the rail: that leaves 0.656 m of footway, under a walking person\'s 0.68. Whether the yard mouth gets gates is the town\'s call; this target has no yard gate',
    for_NOW_md='Railings target (cloud week 42): guard rail A1 = 2.0 m panel, 1.0 m, posts 48.3, rails 42.4 and 33.7 at 1000 and 200, seventeen 12 mm bars (gap 97.1), black; quay tube railing Q2 on the jetty basin edge and tip (14 posts, 13 bays, chain on the tip); no area railings or yard gates on the street; no guard-rail photograph reached.')

# ------------------------------------------------------------------------------------------------------------------ sources
T['sources'] = [
    dict(id='S1', url='https://polyhaven.com/a/bethnal_green_entrance', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0 (https://polyhaven.com/license, read 2026-10-09)', taken='2019-08-18 07:01 UTC (51.526915, -0.054044), api.polyhaven.com/info read 2026-10-09',
         shows='a park entrance in Bethnal Green: a tall cast-iron park railing on a brick plinth with a hinge post and brick piers (R3B); a housing block\'s railing on a two-stage dwarf wall (R3A); a hoop-top railing and gate leaf; bollards; block paving', used='YES: R3B main photograph, R3A; calibration anchors',
         period='the Victorian pattern is long-lived but the paint, the hoop-top gate and the signs are 2000s; whether any of it stood in 1990 is unknown (R3A may be a replica); the picture is for bar proportions, rails, finials and the black paint, not as a 1990 record'),
    dict(id='S2', url='https://polyhaven.com/a/urban_street_01', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-08-18 07:09 UTC (51.528295, -0.053879)',
         shows='an estate street: a low dark-green railing and gate on a dark brick garden wall (R3D); park railings with spear heads on a granite plinth; bollards', used='YES: R3D; calibration anchors',
         period='an estate of the 1960s to 80s with renewed paint; the railing form is plausible for 1990 (a council green), the exact paint date is unknown'),
    dict(id='S3', url='https://polyhaven.com/a/limehouse', read='2026-10-09', author='Andreas Mischok', licence='CC0 1.0', taken='2019-05-19 15:45 UTC (51.510606, -0.036324)',
         shows='a marina basin: bolted cast-iron chain posts with two swags of spiked chain, a timber-piled quay edge across the water, pontoons', used='YES: LHB (the chain\'s lug heights and sag; the K5 post cross-check)',
         period='a 1980s to 90s marina redevelopment; the chain is ornamental (spiked); only its sag and the post\'s lug heights are used'),
    dict(id='S4', url='the repository', read='2026-10-09', author='the project', licence='n/a', taken='2026-09-02 to 2026-10-09',
         shows='SCENE-SLOTS.md, vignette-scene.json, vignette-feet.json, vignette-pieces.json, terrace-fronts.md, the kerbs and bollards targets, the south-quay kit (south_quay_geom.py, README, METHOD), the asset plan, the street-clutter research, atlas CONTINUATION.md (R08)', used='YES: Read numbers', period='n/a'),
    dict(id='S5', url='WebSearch result summaries, 2026-10-09 (three queries: BS 3049 and guard rail infill; the history of British pedestrian guardrail; harbour quay edge railings and chain)', read='2026-10-09', author='third-party pages reached only as summaries', licence='n/a', taken='n/a',
         shows='leads: BS 3049:1976 was withdrawn on 15 November 1995 and replaced by BS 7818; present-day guard rails use 12 mm bars at 110 to 112 centres, 50 x 30 mm posts and a 1100 height; a 1983 London study and a 1988 article on guardrail visibility; Kent dates guardrail from the 1930s; Torbay\'s audit leaves working fish-quay berths unfenced; Bideford\'s quay has cast-iron posts with tubular bars and chains from 1899 to 1905', used='LEADS ONLY: no number taken as a measurement; the 100 gap rule is marked Judgement', period='n/a')]
T['unreached'] = ['Wikimedia Commons', 'Geograph', 'Flickr (including the Hull photograph R08)', 'archive.org', 'HathiTrust', 'Historic England and the Historic England Archive', 'British Listed Buildings', 'BSI Knowledge', 'gov.uk (LTN 2/09)', 'legislation.gov.uk', 'openverse.org', 'Wikipedia', 'Project Gutenberg', 'Sketchfab', 'europeana.eu', 'api.wellcomecollection.org', 'loc.gov', 'web.archive.org (all refused with 403 or not resolvable, tried 2026-10-09); only polyhaven.com and ambientcg.com answered']
T['looked_at_and_left_out'] = ['greenwich_park_02 (one run of black multi-rail railing along a path edge: square posts, five slender round rails and a flat top rail on a brick edging; SEEN AND NOT MEASURED: no wall or other anchor in its view gives its camera height; it is the nearest photographed thing to a tube railing, and it says a park railing of rails without bars was common in 2019)', 'urban_street_02 (a steel palisade along a railway arch and a security door: a 2000s fence, not a railing of the period)', 'urban_street_03 and 04, cambridge, birbeck_street_underpass, leadenhall_market, greenwich_park x3, roof_garden (no railing that bears on this family; urban_street_04 has plastered balustrades of Kensington, not an ironwork form)',
                              'canary_wharf and adams_place_bridge (stainless dock-edge balustrades of the 2000s: modern-only forms, not used)', 'docklands_01 and 02 (Dublin, not Britain)', 'Poly Haven models: modular_chainlink_fence and large_iron_gate exist (CC0) but are not period guard rails or the street\'s; nothing in the catalogue is a guard rail, a tube railing or a quay chain']

json.dump(T, open(os.path.join(HERE, 'target.json'), 'w'), indent=1)
print('wrote target.json', os.path.getsize(os.path.join(HERE, 'target.json')), 'bytes')
