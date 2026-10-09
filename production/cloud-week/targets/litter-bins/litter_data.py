"""The litter-bins family's numbers, in one place (cloud week 42, 9 October 2026). Millimetres unless a name ends _m (metres).
make_target.py turns this into target.json; every other file reads target.json only.

Kinds of number: Read (printed in the repository or on a page reached), Photo (measured on a reached picture or model), Derived, Judgement, Lead (a search
summary or a catalogue snippet: it steers, it is never a number we rely on)."""
import math

# ---------------------------------------------------------------------------------------------------------------------------------------
# K1: pole-mounted open-top steel bin on its own post. Frame: pivot = the post axis on the flag top, z up, +x from the post toward the bin's centre.
# ---------------------------------------------------------------------------------------------------------------------------------------
K1_POST_R = 38.05            # 76.1 mm tube, 3.2 wall (Judgement: the trade's 3-inch tube; the recipe's existing post is 76 mm)
K1_POST_TOP = 1255.0
K1_BIN_OFFSET = 216.0        # post axis to bin axis: post radius + 5 strap + the bin's mid-height wall radius 173
K1_BIN_Z0 = 550.0            # underside of the base plate
K1_RIM_TOP = 1050.0
K1_WALL = 1.5
K1_R_BASE = 165.0            # outer radius of the wall at its foot (dia 330)
K1_R_TOP = 180.5             # outer radius of the wall under the rim bead (dia 361)


def k1_post_profile():
    return [(0.0, 0.0), (K1_POST_R, 0.0), (K1_POST_R, 1230.0), (40.0, 1231.0), (40.0, 1246.0), (37.0, 1252.0), (25.0, 1254.5), (0.0, K1_POST_TOP)]


def k1_bin_outer():
    """lathe about the bin's own axis: base plate underside, wall, rolled bead; (r, z)"""
    return [(0.0, K1_BIN_Z0), (160.0, K1_BIN_Z0), (165.0, 553.0), (K1_R_BASE, 560.0), (K1_R_TOP, 1038.0), (183.0, 1041.0), (186.5, 1046.0),
            (184.0, 1050.0), (180.0, 1050.5), (177.5, 1048.0), (176.8, 1045.0)]


def k1_wall_section():
    """closed outline of the right-hand half of the bin wall, base plate and rim bead in (r, z): outer up, bead, inner down, floor back to the axis"""
    outer = k1_bin_outer()
    up = outer[1:]                       # from the base corner round the bead
    inner_top_r = K1_R_TOP - K1_WALL
    inner = [(176.8 - 1.5, 1045.0), (inner_top_r, 1040.0), (K1_R_BASE - K1_WALL, 556.0)]
    floor = [(K1_R_BASE - K1_WALL, 553.0), (0.0, 553.0)]
    return [(0.0, K1_BIN_Z0)] + up + inner + floor


# K1 variants: conditions A, B, C (the model is one)
K1_CONDITIONS = {
    'A': dict(name='tired but sound', paint='paint_green_worn', fade=0.25, dents=[dict(z=640, az=200, d=55, depth=4), dict(z=700, az=250, d=40, depth=3)],
              rim_dent=None, post_lean_deg=0.4, bin_tilt_deg=0.0, rust_share=0.04, liner_sack=False, stickers=1, gum=2, scorch=3, overflow='O1_low'),
    'B': dict(name='faded and rusting', paint='paint_green_chalk', fade=0.55, dents=[dict(z=620, az=165, d=90, depth=8), dict(z=760, az=215, d=60, depth=5), dict(z=900, az=120, d=45, depth=3)],
              rim_dent=dict(az=240, length=70, depth=8), post_lean_deg=1.2, bin_tilt_deg=0.8, rust_share=0.08, liner_sack=True, stickers=2, gum=3, scorch=5, overflow='O1_full'),
    'C': dict(name='damaged', paint='paint_green_worn', fade=0.4, dents=[dict(z=600, az=185, d=110, depth=12), dict(z=690, az=140, d=70, depth=7), dict(z=830, az=230, d=50, depth=4)],
              rim_dent=dict(az=200, length=120, depth=18), post_lean_deg=1.5, bin_tilt_deg=2.5, rust_share=0.08, liner_sack=False, stickers=2, gum=4, scorch=7, overflow='O1_low'),
}

# ---------------------------------------------------------------------------------------------------------------------------------------
# K2: free-standing hooded drum bin (generic; not the form of any maker's bin). Frame: pivot = the base centre on the flag top; +x is the aperture's side.
# ---------------------------------------------------------------------------------------------------------------------------------------
K2_HEIGHT = 900.0
K2_OUTER = [(0.0, 0.0), (190.0, 0.0), (200.0, 2.0), (209.0, 8.0), (211.0, 40.0), (206.0, 48.0), (198.0, 52.0),                 # foot ring and its recess
            (205.0, 58.0), (214.0, 90.0), (224.0, 200.0), (233.0, 330.0), (237.0, 430.0), (236.0, 520.0), (232.0, 572.0),        # body
            (226.0, 576.0), (226.0, 588.0),                                                                                      # the join groove
            (244.0, 590.0), (250.0, 598.0), (250.0, 640.0),                                                                       # the hood's skirt
            (249.0, 700.0), (244.0, 760.0), (233.0, 812.0), (212.0, 850.0), (176.0, 878.0), (124.0, 893.0), (60.0, 899.0), (0.0, K2_HEIGHT)]
K2_SHELL = 5.0
K2_APERTURE = dict(width=300.0, height=150.0, sill_z=650.0, top_z=800.0, corner_r=30.0, azimuth_deg=0.0, return_flange_depth=15.0, return_flange_t=6.0,
                   note='cut through the hood wall; the lower edge is a flat sill with a 15 mm return flange turned inward; the upper edge is the dome overhanging it')
K2_LINER = [(0.0, 60.0), (185.0, 60.0), (190.0, 66.0), (190.0, 694.0), (194.0, 700.0), (194.0, 706.0), (190.0, 706.0)]   # galvanised, 0.8 sheet; rolled rim at z 700 to 706
K2_CONDITIONS = {
    'a': dict(name='council-fresh', gel='gel_green_fresh', chalk=0.15, scuff=0.25, burn=None, overflow='O2_low', stickers=0, gum=2, cracks=0, hood_dent=None),
    'b': dict(name='sun-chalked and scuffed', gel='gel_green_chalk', chalk=0.55, scuff=0.55, burn=None, overflow='O2_full', stickers=2, gum=4, cracks=3, hood_dent=dict(az=-35, d=80, depth=5)),
    'c': dict(name='burnt hood', gel='gel_green_chalk', chalk=0.45, scuff=0.45, burn=dict(az=-28, z=770, w=115, h=85, charred=60, plume=420), overflow='O2_full', stickers=1, gum=4, cracks=2, hood_dent=None),
}

# ---------------------------------------------------------------------------------------------------------------------------------------
# D1: galvanised household dustbin (the scene's two). Frame: pivot = base centre on the flag top; handles on +-y.
# ---------------------------------------------------------------------------------------------------------------------------------------
D1_BODY_TOP = 610.0         # Read: scene 0.61
D1_RIB_Z = (150.0, 290.0, 430.0)


def d1_body_r(z):
    return 199.0 + 25.0 * (z - 28.0) / (582.0 - 28.0)


def d1_outer():
    p = [(0.0, 6.0), (190.0, 6.0), (194.0, 0.0), (205.0, 0.0), (207.0, 8.0), (207.0, 20.0), (203.0, 26.0), (d1_body_r(28.0), 28.0)]
    for zc in D1_RIB_Z:
        r = d1_body_r(zc)
        p += [(d1_body_r(zc - 12.0), zc - 12.0), (r + 6.0, zc - 6.0), (r + 6.0, zc + 6.0), (d1_body_r(zc + 12.0), zc + 12.0)]
    p += [(d1_body_r(582.0), 582.0), (229.0, 585.0), (231.5, 595.0), (230.0, 606.0), (226.0, D1_BODY_TOP), (222.0, 609.0)]
    return p


D1_LID = [(240.0, 588.0), (250.5, 590.0), (251.0, 610.0), (247.0, 617.0), (240.0, 621.0), (210.0, 630.0), (150.0, 637.0), (80.0, 640.0), (0.0, 641.0)]
D1_LID_HANDLE = dict(length=100.0, strap_w=25.0, strap_t=3.0, rise=19.0, top_z=660.0, rivets=2)
D1_SIDE_HANDLE = dict(z=470.0, height=100.0, proud=45.0, strap_w=25.0, strap_t=3.0, rivets_per_end=2, rivet_d=8.0)
D1_CONDITIONS = {
    'a': dict(name='lid on, ordinary', lid='on', lid_tilt_deg=2.0, dents=5, rust_foot=0.35, white_rust=0.30, soot=0.2, sacks=0, overflow=None, number_stencil=True),
    'b': dict(name='lid off, over-full', lid='off_leaning', lid_tilt_deg=0.0, dents=7, rust_foot=0.5, white_rust=0.35, soot=0.35, sacks=2, overflow='O3_sacks', number_stencil=True),
    'c': dict(name='old and rusty', lid='on', lid_tilt_deg=0.0, dents=9, rust_foot=0.8, white_rust=0.45, soot=0.45, sacks=0, overflow=None, number_stencil=False),
}

# ---------------------------------------------------------------------------------------------------------------------------------------
# K3: precast concrete drum bin: WRITTEN, NOT PLACED (Judgement + Lead; no photograph)
# ---------------------------------------------------------------------------------------------------------------------------------------
K3 = dict(name='concrete_drum', placed=False, height=900.0, outer_d=550.0, wall=60.0, liner_d=410.0, liner_rim_below_top=40.0,
          finish='exposed pebble aggregate, grey-buff', source='street-clutter-1990 (c): a hollow cylinder 55 cm across and 90 cm tall, rough pebbled surface, a liner showing at the top; Lead: a 1960 design competition praised an open concrete bin and current precast bins are 500 to 550 across')

# ---------------------------------------------------------------------------------------------------------------------------------------
# materials: sRGB, roughness 0-1, metal 0-1, with the kind of the number and its source (texture ids are Poly Haven CC0 scans measured in photo_measurements.json)
# ---------------------------------------------------------------------------------------------------------------------------------------
MATERIALS = {
    'paint_green_fresh':  dict(srgb=[38, 64, 46], rough=0.45, metal=0.0, kind='Judgement', note='the council livery on a bin put up within two years; the street recipe\'s own council-green is (30, 62, 40) and reads too dark and saturated in overcast'),
    'paint_green_worn':   dict(srgb=None, rough=0.60, metal=0.0, kind='Photo', tex='green_metal_rust', note='worn dark-green paint on steel: the median of the scanned albedo of Poly Haven\'s green_metal_rust (Rob Tuytel, CC0)'),
    'paint_green_chalk':  dict(srgb=[88, 100, 82], rough=0.72, metal=0.0, kind='Judgement', note='the same green chalked and faded by twenty years of weather on its sun side (about 0.55 of the way to a pale grey-green)'),
    'gel_green_fresh':    dict(srgb=[40, 78, 58], rough=0.30, metal=0.0, kind='Judgement', note='glass-fibre gelcoat, the same livery, glossier than paint'),
    'gel_green_chalk':    dict(srgb=[92, 112, 96], rough=0.62, metal=0.0, kind='Judgement', note='gelcoat chalked by UV; the hood\'s top is the palest'),
    'letters_cream':      dict(srgb=[226, 222, 205], rough=0.5, metal=0.0, kind='Judgement', note='self-adhesive or stencilled letters; the same value as the street recipe\'s letters-white (235, 235, 228) lowered a little for age'),
    'letters_cream_worn': dict(srgb=[196, 190, 170], rough=0.65, metal=0.0, kind='Judgement', note='the same, grimed'),
    'zinc_new':           dict(srgb=None, rough=0.40, metal=1.0, kind='Photo', tex='corrugated_iron', note='new hot-dip zinc: scanned albedo of Poly Haven\'s corrugated_iron (Jenelle van Heerden / Dimitrios Savva, CC0)'),
    'zinc_weathered':     dict(srgb=None, rough=0.55, metal=0.8, kind='Photo', tex='corrugated_iron_03', note='weathered galvanising, dull and cool: scanned albedo of corrugated_iron_03 (Charlotte Baglioni, CC0)'),
    'zinc_worn_dirty':    dict(srgb=None, rough=0.65, metal=0.4, kind='Photo', tex='worn_corrugated_iron', note='old galvanising with grime, paint and rust specks: scanned albedo of worn_corrugated_iron (CC0)'),
    'zinc_dark_grime':    dict(srgb=None, rough=0.75, metal=0.2, kind='Photo', tex='corrugated_iron_02', note='galvanising under soot and street film: scanned albedo of corrugated_iron_02 (CC0)'),
    'white_rust':         dict(srgb=[205, 208, 204], rough=0.85, metal=0.0, kind='Judgement', note='zinc oxide and carbonate bloom, a chalky white-grey powder on damp galvanising (the container photograph shows its faint trace as the pale rub streaks: +3 to +9 in G and B over the face)'),
    'rust':               dict(srgb=None, rough=0.85, metal=0.0, kind='Photo', tex='rust_coarse_01', note='bare-steel rust: scanned albedo of rust_coarse_01 (CC0)'),
    'rust_painted':       dict(srgb=None, rough=0.85, metal=0.0, kind='Photo', tex='rusty_painted_metal', note='rust under and through paint: scanned albedo of rusty_painted_metal (CC0)'),
    'primer_ochre':       dict(srgb=[152, 110, 78], rough=0.8, metal=0.0, kind='Read', note='the wear target\'s pale ochre where paint has gone to primer or first rust (dry 152, 110, 78; wet 141, 102, 72)'),
    'soot':               dict(srgb=[36, 33, 30], rough=0.9, metal=0.0, kind='Judgement', note='cigarette scorch and smoke film'),
    'splash_band':        dict(srgb=[62, 56, 48], rough=0.9, metal=0.0, kind='Judgement', note='road-splash grime, dark warm grey-brown, heaviest below 0.3 m (the wear target\'s foot rule)'),
    'char':               dict(srgb=[22, 20, 18], rough=0.8, metal=0.0, kind='Judgement', note='burnt glass-fibre and scorched paint'),
    'melted_edge':        dict(srgb=[58, 64, 52], rough=0.25, metal=0.0, kind='Judgement', note='re-set resin at the rim of a burn hole, glossy'),
    'paper_remnant':      dict(srgb=[215, 210, 195], rough=0.8, metal=0.0, kind='Judgement', note='torn fly-poster paper, rain-softened'),
    'bin_sack_black':     dict(srgb=[22, 22, 24], rough=0.25, metal=0.0, kind='Judgement', note='black polythene sack (Poly Haven trashbag reads "shiny black")'),
    'concrete_precast':   dict(srgb=None, rough=0.9, metal=0.0, kind='Photo', tex='precast_concrete_wall', note='K3 only: scanned albedo of precast_concrete_wall (CC0)'),
}

# ---------------------------------------------------------------------------------------------------------------------------------------
# placements (street frame: x along the street from the south/quay end, z across from the crown, east +; metres)
# ---------------------------------------------------------------------------------------------------------------------------------------
KERB_FACE = 3.0           # |z| of the kerb face (Read: scene half carriageway)
KERB_BACK = 3.17          # |z| of the granite kerb's back edge (the kerbs target: top 170); the scene's 3.125 is the earlier reading
STALLRISER_FACE = 4.975   # |z| of the shopfront's stallriser face (building line 5.125 less 0.15 proud)
PLACEMENTS = [
    dict(id='B1', kind='K1', condition='A', side='east', post_x=6.6, post_setback_from_kerb_face=0.62, bin_dir=-1, yaw_note='the bin is hung on the quay side of its post (toward x = 0)', serves='Mickey\'s doors (shop door 4.797, side door 3.822) and the cab rank'),
    dict(id='B2', kind='K1', condition='B', side='east', post_x=35.2, post_setback_from_kerb_face=0.62, bin_dir=+1, yaw_note='hung on the uphill side (toward x = 48)', serves='the grocer\'s door (38.147) and the launderette\'s side door (32.178)'),
    dict(id='B3', kind='K2', condition='c', side='west', axis_x=44.0, axis_setback_from_kerb_face=0.80, yaw_note='the aperture faces the shops\' side of the footway (the building line)', serves='the newsagent\'s side door (41.178), the bus stop (46.0) and the chandler\'s queue'),
]
DUSTBINS = [dict(id='D1-1', condition='a', side='east', x=21.4, setback_from_kerb=1.6), dict(id='D1-2', condition='b', side='east', x=22.0, setback_from_kerb=1.6)]
WALKING_PERSON_M = 0.68
