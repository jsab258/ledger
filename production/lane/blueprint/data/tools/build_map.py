#!/usr/bin/env python3
"""Build map.json for LEDGER's Hook and docks (blueprint data file 1).

Written 24 Nov 2026 by the data build (Opus 5.5). Source of truth for the plan:
BLUEPRINT-04 FIT-G1 and 4.1, DEFINITIONS-2026-11-21 G1 (the road table),
production/specs/vignette-scene.json (Quay Street as built, street-local
metres) and the built shop fronts (the grocer's fanlight reads 11, so the
east side of Quay Street is odd). The prototype's way.js is mined for names,
landmark wording and trades, never for positions (it is an older plan).

Frame: metres, origin at the ferry landing, x east, y north, z up (z is the
ground level at a point, metres above the quay's road). Bearings for doors
are compass degrees (0 north, 90 east) of the way the door FACES (out of the
building, toward the street).

Run:  python3 build_map.py            (writes ../map.json)
Then: python3 check_map.py            (tests it)
      python3 render_map.py           (draws ../map-topdown.svg from map.json)

Everything here is design data. Values not given by the blueprint, G1 or the
built street are listed in CHOSEN (and carry "chosen": true in the file).
"""
import json, math, random, os

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'map.json')

def r2(v):
    return round(v, 3)

def P(x, y):
    return [r2(x), r2(y)]

def seglen(a, b):
    return math.hypot(b[0] - a[0], b[1] - a[1])

def polylen(pts):
    return sum(seglen(pts[i], pts[i + 1]) for i in range(len(pts) - 1))

def basin_x(y):
    """Basin Road's centre line, straight from (250, 0) to (210, 350) as G1 gives it."""
    return 250.0 - 40.0 * y / 350.0

CHOSEN = []
OPEN = []

def chosen(what):
    CHOSEN.append(what)

KERB = 0.115          # granite kerb upstand, 4.1.1 prior research (atlas ADOPTED 2026-10-06; the scene file's 125 mm is wrong)
KERB_W = 0.125        # kerb width, vignette-scene.json street.kerb.width_m
PAV = 2.0             # footway width, vignette-scene.json and terrace-fronts.md
chosen('Pavements 2.0 m both sides on every drivable road (Quay Street measured 2.0; elsewhere the same figure chosen); G1 widths read as the carriageway, kerb to kerb')
chosen('Granite kerb, 115 mm upstand, on every drivable road (Quay Street measured; the rest chosen to match an old port)')

# ---------------------------------------------------------------- roads
# side features: 'left' and 'right' are relative to the direction of travel from the first point to the last.
# kinds of edge: 'pavement' (footway and kerb), 'quay' (quay apron, granite cope, water beyond, no kerb on the water side),
# 'bridge' (footway with parapet over water), 'none'.
ROADS = []

def road(id, name, pts, cw, left, right, g1_length=None, g1_width=None, foot_only=False, z=None, note='', src='FIT-G1', plates=True, **kw):
    r = dict(id=id, name=name, pts=[P(*p) for p in pts], carriageway_m=cw, left=left, right=right,
             foot_only=foot_only, drivable=not foot_only, two_way=not foot_only, kerb_upstand_m=(None if foot_only else KERB),
             length_m=r2(polylen(pts)), g1_length_m=g1_length, g1_width_m=g1_width, src=src, plates=plates)
    if z is not None:
        r['z'] = z
    if note:
        r['note'] = note
    r.update(kw)
    ROADS.append(r)
    return r

pav = lambda w=PAV: dict(kind='pavement', width_m=w)
quay = lambda w=3.0: dict(kind='quay', width_m=w)

# The quay road. South side is the sea quay (apron 3 m to the granite cope) except over the Old Basin's mouth (x 250 to 480),
# where the road crosses the fixed basin bridge with a 2 m footway and parapet on each side.
road('quay_road', 'The Quay', [(0, 0), (120, 0), (159, 0), (250, 0), (480, 0), (540, 0)], 9.0,
     left=pav(), right=quay(3.0), g1_length=540, g1_width=9,
     spans=[dict(from_x=250, to_x=480, kind='basin_bridge', left=dict(kind='bridge', width_m=2.0), right=dict(kind='bridge', width_m=2.0),
                 note='the fixed basin bridge across the Old Basin mouth, parapets 1.1 m, water both sides')],
     z=[0, 0, 0, 0, 0, 0], note='G1: landing and rank 0 to 30, Quay Street foot 120, chandler and boxing club hall 190 to 230 north side, basin mouth 250 to 480, fish dock 480 to 540')
chosen('The Quay is the quay road\'s street name (the prototype calls it "the quay")')

# Quay Street as built. Street-local x (vignette-scene.json, 0 at the south end) maps to world y = 4.5 + street x:
# the street begins at the quay road's north kerb line. World x = 120 + street z (z east positive).
QS_Y0 = 4.5
road('quay_street', 'Quay Street', [(120, 0), (120, QS_Y0), (120, QS_Y0 + 48.0), (120, 57.1)], 6.0, left=pav(), right=pav(),
     g1_length=48, g1_width=11, z=[0, 0, 3.0, 3.1],
     built=dict(length_m=48.0, front_to_front_m=10.25, carriageway_m=6.0, footway_m=2.0, kerb_upstand_m=0.115, bay_m=6.0,
                climb_m=3.0, climb_note='flat for the first 12 m, then 1 in 12 to the top (4.1.1 prior research: 1 in 12 at the north end)',
                street_local_to_world='world x = 120 + street z; world y = 4.5 + street x (vignette-scene.json frame)'),
     note='Built street: 48 m from the quay road\'s north kerb (world y 4.5) to its top (y 52.5); the centre line adds the 4.5 m of the quay road\'s junction mouth and 4.6 m at the top, where it turns into Back Parade at y 57.1 so that Back Parade\'s south pavement wraps the chandlery\'s north wall')
chosen('Quay Street\'s street-local x = 0 sits on the quay road\'s north kerb (world y 4.5); its 48 built metres run y 4.5 to 52.5')

BEND_A = (120, 57.1)                # the turn: Back Parade's south frontage passes just north of the chandlery (y 50.5)
BEND_B = (160, QS_Y0 + 48.0 + 14)  # (160, 66.5): G1's bend shifted north by the 4.5 m junction mouth, same 40 by 14 m shape
road('back_parade', 'Back Parade', [BEND_A, BEND_B], 9.0, left=pav(), right=pav(), g1_length=42, g1_width=9, z=[3.0, 3.6],
     note='the bend behind the parade: the parade\'s yards and the chandler\'s back on its south side')
chosen('Back Parade is the name of the bend behind the parade')
chosen('The turn from Quay Street into Back Parade is at y 57.1 (G1: 48 on its own frame), 4.6 m past the built street\'s top, so the bend clears the built chandlery; Back Parade 41.1 m')

road('north_road', 'North Road', [BEND_B, (160, 260), (160, 300), (160, 330), (160, 350), (160, 400)], 9.0, left=pav(), right=pav(),
     g1_length=338, g1_width=9, z=[3.6, 6.0, 6.4, 6.6, 6.8, 7.2], soft_edge_end=True,
     note='to the soft edge at y 400; G1 measures it from y 62, this plan from y 66.5 (the bend moved north with Quay Street\'s junction mouth), so 333.5 m')
chosen('North Road is the north road\'s name; ground rises gently to about 7 m at the edge')

road('chapel_lane', 'Chapel Lane', [(160, 260), (139, 260), (-80, 260)], 7.0, left=pav(), right=pav(), g1_length=240, g1_width=7,
     z=[6.0, 6.0, 6.5], soft_edge_end=True, src='FIT-G1; canon (Chapel Lane is not one of canon\'s three minted streets but is G1\'s name)',
     note='the west road; the chapel and the closed school x -20 to 60, the retired doctor\'s terrace; soft edge at x -80')

road('coldstore_road', 'Cold Store Road', [(160, 350), (210, 350), (340, 350), (480, 350), (540, 350)], 9.0, left=pav(), right=pav(),
     g1_length=380, g1_width=9, z=[6.8, 6.6, 6.0, 5.2, 5.0],
     note='Basin Road\'s top at x 210, the cold stores\' loading yard mouth at x 340, the warehouse row\'s top at x 480')
chosen('Cold Store Road is the cold-store road\'s name')

road('dock_road', 'Dock Road', [(540, 350), (540, 210), (540, 80), (540, 0)], 10.0, left=pav(), right=pav(), g1_length=350, g1_width=10,
     z=[5.0, 3.0, 0.8, 0], note='the dock gate and its yard mouth at y 210 (east side), customs and the Harbour Board at y 20 to 80 (west side)', src='FIT-G1; prototype address "Dock Road"')

road('basin_road', 'Basin Road', [(250, 0), (basin_x(150), 150), (basin_x(255), 255), (basin_x(300), 300), (210, 350)], 7.0,
     left=pav(), right=quay(2.0), g1_length=353, g1_width=7, z=[0, 1.0, 2.4, 3.8, 6.6],
     quay_side_note='the right (east) side is the Old Basin\'s west quay from y 10 to y 250; above y 259 it is Iveson\'s yard wall',
     note='the Old Basin\'s west quay (y 30 to 250), Iveson\'s yard (y 260 to 320, east side)')

road('basin_top', 'Basin Top', [(basin_x(255), 255), (300, 255), (360, 255), (480, 255)], 7.0, left=pav(), right=quay(2.0),
     g1_length=260, g1_width=7, z=[2.4, 2.4, 2.4, 2.4], note='the basin\'s north road: the burned warehouse x 300 to 360 on its north side; its south side is the basin\'s north quay')
chosen('Basin Top is the basin\'s north road\'s name')

road('warehouse_row', 'Warehouse Row', [(480, 0), (480, 255), (480, 350)], 7.0, left=quay(2.0), right=pav(), g1_length=350, g1_width=7,
     z=[0, 2.4, 5.2], quay_side_note='the left (west) side is the basin\'s east quay from y 10 to y 250',
     note='Norman Dent\'s warehouses on the east side; the basin\'s east quay (y 30 to 250) on the west')

# foot-only ways: bollarded at both ends, no car can follow
road('yards_lane', "the yards' lane", [(159, QS_Y0), (150, 8.0), (150, 64.15)], 2.5, left=dict(kind='none'), right=dict(kind='none'),
     g1_length=63, g1_width=2.5, foot_only=True, plates=False,
     note='leaves the quay road east of Mickey\'s, runs north behind the parade\'s yards to Back Parade; Mickey\'s back fence is its vault place')
chosen('The yards\' lane enters from the quay road at x 159 (G1 175) and runs at x 150, so it passes Mickey\'s back fence; 65.8 m')

GINNEL = [(60, QS_Y0), (80, 30.0), (139, 260), (160, 330)]
road('ginnel', "the terraces' ginnel", GINNEL, 1.5, left=dict(kind='none'), right=dict(kind='none'), g1_length=345, g1_width=1.5,
     foot_only=True, plates=False,
     note='from the quay road at x 60 (G1) diagonally through the yards behind Quay Street\'s west side (Ada\'s back gate at the end of her long cottage garden), across Chapel Lane at (139, 260), to North Road at (160, 330)')
chosen('The ginnel keeps G1\'s ends and crossing, with one bend at (80, 30) so it runs behind the west side\'s yards; 342.9 m. The west cottages and shops have long yards (about 25 to 40 m) back to it')

road('cut_150', 'the warehouse cut (south)', [(basin_x(150), 150), (160, 150)], 2.0, left=dict(kind='none'), right=dict(kind='none'),
     g1_length=50, g1_width=2, foot_only=True, plates=False, note='between the Basin Road warehouses to North Road')
road('cut_300', 'the warehouse cut (north)', [(basin_x(300), 300), (160, 300)], 2.0, left=dict(kind='none'), right=dict(kind='none'),
     g1_length=50, g1_width=2, foot_only=True, plates=False, note='past Cammack\'s lock-ups to North Road')
OPEN.append('G1 gives both warehouse cuts as 50 m, but G1\'s own Basin Road line lies 73 m (centre to centre) from North Road at y 150 and 56 m at y 300; the cuts are drawn at the true distances (72.9 m and 55.7 m). The keeper should mark G1\'s 50 m as approximate.')

road('quay_gap', 'the gap', [(120, 27.0), (77.647, 27.0)], 3.0, left=dict(kind='none'), right=dict(kind='none'), foot_only=True, plates=False,
     src='vignette-scene.json (the yard gap between the cottages and the shops, street x 21 to 24; atlas street_anchor yard_gap_x)',
     note='the passage between the west cottages and the west shops, from Quay Street to the ginnel')

# ---------------------------------------------------------------- water and land
QE = -7.5   # the sea quay's cope line: road edge -4.5, apron 3.0
WATER = [
    dict(id='sea', name='the harbour', poly=[P(-100, QE), P(250, QE), P(250, -4.5), P(480, -4.5), P(480, QE), P(560, QE), P(560, -45), P(-100, -45)],
         src='G1 (the water lies south of the quay road)', note='the stretch under the basin bridge (x 250 to 480) runs to the bridge\'s south parapet at y -4.5'),
]
# The Old Basin: bounded by Basin Road's quay (centre + 3.5 + 2.0), Basin Top's quay (y 255 - 5.5), Warehouse Row's quay (480 - 5.5)
# and the bridge's north parapet (y 4.5 + 2.0).
def basin_edge_x(y):
    return basin_x(y) + 5.7
BASIN = [P(basin_edge_x(6.625), 6.625), P(474.3, 6.625), P(474.3, 249.3), P(basin_edge_x(249.3), 249.3)]
WATER.append(dict(id='old_basin', name='the Old Basin', poly=BASIN, src='G1; 4.2.2', note='quay edges on all three land sides, the bridge on the fourth'))

FOOTPRINT = dict(x=[-80, 540], y=[0, 400], src='G1 (about 620 by 400 m, 0.25 km2)')

# ---------------------------------------------------------------- plots, buildings and doors
PLOTS, DOORS = [], []

def rect(x0, y0, x1, y1):
    return [P(x0, y0), P(x1, y0), P(x1, y1), P(x0, y1)]

def plot(id, name, poly, use, storeys=None, building=True, street=None, number=None, place=None, enterable=False, src='', note='', chosen_=False, **kw):
    p = dict(id=id, name=name, outline=poly, building=building, storeys=storeys, use=use, street=street, number=number,
             place=place, enterable=enterable, src=src)
    if note:
        p['note'] = note
    if chosen_:
        p['chosen'] = True
    p.update(kw)
    PLOTS.append(p)
    return p

def door(id, plot_id, x, y, facing, street=None, number=None, locked=True, kind='front', src='', note='', chosen_=False, **kw):
    d = dict(id=id, plot=plot_id, x=r2(x), y=r2(y), facing=facing, street=street, number=number, locked=locked, kind=kind, src=src)
    if note:
        d['note'] = note
    if chosen_:
        d['chosen'] = True
    d.update(kw)
    DOORS.append(d)
    return d

def ginnel_x(y):
    pts = GINNEL
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        if ay <= y <= by:
            return ax + (bx - ax) * (y - ay) / (by - ay)
    raise ValueError(y)

# --- Quay Street, as built (vignette-scene.json blocks; trades by the 3 Oct ruling; numbers from the built fascias)
QS_E = 125.125   # east frontage: 120 + 3.0 + 0.125 + 2.0
QS_W = 114.875
DEPTH = 8.0
def qy(sx):
    return QS_Y0 + sx

east = [  # (bay, number, id, name, use, place, storeys, enterable, door street x, note)
    (0, 1, 'mickeys', "Mickey's", 'cab_office', 'mickeys', 2, True, 4.65, 'the cab office (canon D19); the flat above by the inner stair; Mickey\'s inner office locked; the built door\'s middle at street x 4.65'),
    (1, 3, 'laveracks', "Laverack's", 'fishmonger', 'laveracks', 2, True, 9.4, 'bay 1, the fishmonger (ruling 3 Oct); Brenda Laverack'),
    (2, 5, 'ritas', "Rita's", 'pawnbroker', 'ritas', 2, True, 18.0, 'bay 2, Rita\'s pawn (hook-cast.json, the built fascia decal_02_fascia_ritas_pawn); window lit at night (ruling 1 Oct); back room fences from rung 2'),
    (3, 7, 'empty_unit', 'the empty unit', 'empty_shop', 'empty_unit', 2, False, 24.0, 'bay 3, the empty unit to let, whitewashed, a TO LET board, card and a fallen blind inside (ruling 3 Oct, 24 Nov)'),
    (4, 9, 'launderette', 'the Washeteria', 'launderette', 'launderette', 2, True, 30.0, 'bay 4, the launderette (ruling 3 Oct); the prototype\'s name'),
    (5, 11, 'grocer', 'Hook Stores', 'grocer', 'grocer', 2, True, 38.147, 'bay 5, the grocer (ruling 3 Oct); fanlight 11 (fascia_common.py); the prototype\'s name'),
]
for bay, num, pid, name, use, place, storeys, enter, dsx, note in east:
    sx0 = 3.0 + 6.0 * bay
    plot('qs_' + pid, name, rect(QS_E, qy(sx0), QS_E + DEPTH, qy(sx0 + 6.0)), use, storeys, street='quay_street', number=num, place=place,
         enterable=enter, src='vignette-scene.json east_parade bay %d; canon; RULINGS 3 Oct' % bay, note=note, bay='east_parade_bay%d' % bay,
         upstairs='flat' if bay else 'flat (Tom\'s, above the office)')
    door('d_qs_%d' % num, 'qs_' + pid, QS_E, qy(dsx), 270, 'quay_street', num, locked=(pid == 'empty_unit'), kind='front',
         src='vignette-scene.json; built fronts', hours_from='places.json')
    # every parade bay has a back door to its own yard and a yard gate on the yards' lane
    yard = 'qs_%s_yard' % pid
    plot(yard, "%s yard" % name, rect(QS_E + DEPTH, qy(sx0), 148.75, qy(sx0 + 6.0)), 'yard', None, building=False, street='quay_street',
         src='terrace practice (a back yard to the lane); chosen', chosen_=True)
    door('d_qs_%d_back' % num, 'qs_' + pid, QS_E + DEPTH, qy(sx0 + 3.0), 90, 'quay_street', num, locked=True, kind='back', chosen_=True)
    if bay > 0:
        door('d_qs_%d_yardgate' % num, yard, 148.75, qy(sx0 + 3.0), 90, None, None, locked=True, kind='yard_gate', chosen_=True,
             note="the yard gate on the yards' lane")
chosen('Each parade bay has a back yard to x 148.75 with a back door and a locked gate on the yards\' lane')
# Mickey's yard: two escapes, the quay gate and the back fence (the lane's vault place)
door('d_mickeys_yard_quay_gate', 'qs_mickeys_yard', 141.0, qy(3.0), 180, 'quay_road', None, locked=False, kind='yard_gate',
     src='canon (a yard with two escapes); 4.3.1', note="the yard's gate onto The Quay's pavement; bolted from inside, open by day")
plot('qs_chandler', 'the chandlery', rect(QS_E, qy(40.0), QS_E + DEPTH, qy(46.0)), 'ship_chandler', 2, street='quay_street', number=13, place='chandlery',
     enterable=True, src='vignette-scene.json east_chandler (street x 40 to 46); RULINGS 3 Oct', bay='east_chandler',
     note='the ship\'s chandler\'s shop; grey brick, end stack')
door('d_qs_13', 'qs_chandler', QS_E, qy(44.0), 270, 'quay_street', 13, locked=False, src='vignette-scene.json (doors on the right)', chosen_=True)
plot('qs_chandler_yard', "the chandlery's yard", rect(QS_E + DEPTH, qy(40.0), 148.75, qy(46.0)), 'yard', building=False, chosen_=True, src='chosen')

west = [  # (from street x, to street x, number, id, name, use, place, storeys, enterable)
    (3, 9, 2, 'ada', "Ada's", 'home', 'adas', 1, True, "Ada's cottage, across from Mickey's: her front room window looks on the street (4.3.4); back gate on the ginnel"),
    (9, 15, 4, 'cottage_4', '4 Quay Street', 'home', None, 1, False, 'a single-storey cottage (drawn street since 3 Oct)'),
    (15, 21, 6, 'cottage_6', '6 Quay Street', 'home', None, 1, False, 'a single-storey cottage; a break-in room for jobs'),
    (24, 30, 8, 'pearts', "Peart's", 'newsagent', 'newsagent', 1, True, 'the newsagent and tobacconist (ruling 3 Oct); prototype name'),
    (30, 36, 10, 'ironmonger', "the ironmonger's", 'ironmonger', 'ironmonger', 1, True, 'crowbar, torch, keys cut (4.3.3)'),
    (36, 42, 12, 'copper_kettle', 'the Copper Kettle', 'tea_room', 'tea_room', 1, True, 'the tea room (ruling 3 Oct); prototype name'),
]
for sx0, sx1, num, pid, name, use, place, storeys, enter, note in west:
    plot('qs_' + pid, name, rect(QS_W - DEPTH, qy(sx0), QS_W, qy(sx1)), use, storeys, street='quay_street', number=num, place=place,
         enterable=enter, src='vignette-scene.json west_south / west_north; RULINGS 3 Oct; canon (three sides)', note=note)
    door('d_qs_%d' % num, 'qs_' + pid, QS_W, qy((sx0 + sx1) / 2.0), 90, 'quay_street', num, locked=(use == 'home'), src='vignette-scene.json', chosen_=True)
    yard = 'qs_%s_yard' % pid
    ya, yb = qy(sx0), qy(sx1)
    west_edge = [P(ginnel_x(yb) + 1.0, yb)] + ([P(80.0 + 1.0, 30.0)] if ya < 30.0 < yb else []) + [P(ginnel_x(ya) + 1.0, ya)]
    plot(yard, '%s yard' % name, [P(QS_W - DEPTH, ya), P(QS_W - DEPTH, yb)] + west_edge, 'yard',
         building=False, street='quay_street', chosen_=True, src='chosen (the yards run back to the ginnel)')
    door('d_qs_%d_back' % num, 'qs_' + pid, QS_W - DEPTH, qy((sx0 + sx1) / 2.0), 270, 'quay_street', num, locked=True, kind='back', chosen_=True)
    ym = qy((sx0 + sx1) / 2.0)
    door('d_qs_%d_yardgate' % num, yard, (ginnel_x(ym) + 1.0) if not (ya < 30.0 < yb) else (81.0 + (ginnel_x(ym) + 1.0 - 81.0)), ym, 270, None, None, locked=(pid != 'ada'), kind='yard_gate', chosen_=True,
         note="the back gate on the ginnel" + (" (Ada's, unlatched by day)" if pid == 'ada' else ''))
plot('qs_corner_store', 'the builder\'s store', rect(QS_W - DEPTH, qy(42.5), QS_W, qy(48.0) + 3.0), 'store', 1, street='quay_street', number=14,
     src='chosen', chosen_=True, note='a locked store at the top of the west side, across from the bend')
door('d_qs_14', 'qs_corner_store', QS_W, qy(45.5), 90, 'quay_street', 14, locked=True, chosen_=True)
chosen('Quay Street numbers: east side odd (Mickey\'s 1 to the chandlery 13, the built grocer\'s fanlight reads 11), west side even (Ada 2 to the tea room 12, the store 14)')
OPEN.append('The prototype numbers Mickey\'s 2 Quay Street (east even); the built grocer\'s fanlight reads 11, so the east side is odd here (Mickey\'s 1). Letters, the paper and the prototype need the new numbers.')
OPEN.append('Bay 2 is Rita\'s pawn (hook-cast.json and the built fascia); the blueprint also names Wayne Harrison\'s pawn (4.3.3, 2.7). Both are kept: Rita\'s on Quay Street, Wayne\'s on North Road. The keeper should confirm two pawns are meant.')
OPEN.append('The chip shop is "on the parade" (G10) but the six parade bays are all taken (Mickey\'s and the five ruled or built trades); it stands at the top of the parade on Back Parade\'s north side.')
OPEN.append('RT2-19 puts a phone box "at the parade\'s north end"; the built KX100 kiosk stands at street x 16.5 by Rita\'s (RULINGS 2 Oct: the phone box stays). The built place is kept.')

# --- The Quay, north side (one-sided street, numbered from the landing eastward)
QN = 4.5 + KERB_W + PAV   # 6.625
quay_plots = [
    ('quay_smokehouse', "the smoke house", 2, 12, 16, 'smoke_house', 1, False, None, 'Laverack\'s smoke house, the tarred door that smells of kippers (prototype)'),
    ('quay_snooker', 'the snooker hall', 13, 33, 18, 'snooker_hall', 2, True, 'snooker_hall', 'upstairs over a shuttered ship\'s stores; frames for no money (24 Nov pastimes ruling)'),
    ('quay_regent', 'Regent House', 34, 44, 16, 'boarding_house', 3, True, 'boarding_house', 'the boarding house with the VACANCIES card (prototype); the ferry clerk lodges here'),
    ('quay_caff', "Rinaldi's", 45, 58.5, 16, 'caff', 2, True, 'caff', "Grace Rinaldi's caff by the ginnel's mouth, steam on the glass; the dock shift's breakfast"),
    ('quay_metcalfes', "Metcalfe's", 162, 172, 14, 'coin_shop', 2, True, 'metcalfes', "Hal's coin shop that sells no coins (prototype; Hal has a shop, 4.3.3)"),
    ('quay_secondhand', 'the second-hand shop', 174, 186, 14, 'second_hand_shop', 2, True, 'second_hand', 'takes radios and video recorders (1.6, 2.7); a buyer and a listener'),
    ('quay_chandler_store', "the chandler's store", 190, 208, 16, 'warehouse', 2, False, None, "G1's chandler's at 190 to 230: the chandler's warehouse; the shop is on Quay Street"),
    ('quay_ships_stores', 'the ship\'s stores', 232, 241, 12, 'shop_shuttered', 2, False, None, 'shuttered since 1989'),
    ('quay_net_store', 'the net store', 487, 512, 12.5, 'net_store', 2, False, 'widow_base', "the fish dock's net store, the Widow's dock office over it (RT2-08)"),
    ('quay_fish_merchants', 'the fish merchants\' office', 514, 531, 11.5, 'office', 2, False, None, 'the fish auction\'s office, open at dawn'),
]
n = 0
for pid, name, x0, x1, depth, use, storeys, enter, place, note in quay_plots:
    n += 1
    plot(pid, name, rect(x0, QN, x1, QN + depth), use, storeys, street='quay_road', number=n, place=place, enterable=enter,
         src='FIT-G1 (positions on the quay road where G1 names them); prototype way.js (names, landmarks); chosen', chosen_=True, note=note)
    door('d_quay_%d' % n, pid, (x0 + x1) / 2.0, QN, 180, 'quay_road', n, locked=not enter, chosen_=True)
# the boxing club's old hall stands behind its own forecourt, beside the chandler's store
n += 1
plot('quay_boxing', 'the boxing club', rect(210, QN + 3.4, 230, QN + 23.4), 'boxing_club', 1, street='quay_road', number=n, place='boxing_club',
     enterable=True, src='FIT-G1 (190 to 230 north side); 4.3.3 (the boxing club\'s old hall behind the chandler\'s)', note='the old hall, a bare bulb over the door; a forecourt in front')
door('d_quay_%d' % n, 'quay_boxing', 220, QN + 3.4, 180, 'quay_road', n, locked=False, chosen_=True, setback_m=3.4)
plot('quay_boxing_forecourt', "the boxing club's forecourt", rect(210, QN, 230, QN + 3.4), 'forecourt', building=False, chosen_=True, src='chosen')
# the Widow's office stair: an outside door at the net store's east end
door('d_widow_office', 'quay_net_store', 512, QN + 6.0, 90, 'quay_road', None, locked=True, kind='stair', chosen_=True,
     note="the outside stair to the Widow's dock office over the net store")
chosen('The Quay\'s north side, west to east: smoke house, snooker hall (over a shuttered stores), Regent House, Rinaldi\'s caff, then Metcalfe\'s, the second-hand shop, the chandler\'s store, the boxing club, a shuttered ship\'s stores; past the basin the net store (the Widow\'s office over it) and the fish merchants\' office')

# --- Dock Road, west side: customs and the Harbour Board (G1 y 20 to 80); east side: the dock gate at y 210
DW = 540 - 5.0 - KERB_W - PAV   # 532.875
plot('dock_customs', 'the customs house', rect(503, 22, DW, 48), 'customs', 2, street='dock_road', number=1, place='customs', enterable=False,
     src='FIT-G1; 4.2.3 (customs, an officer who never reports; the bonded store)', note='customs house with the bonded store behind (tobacco and boxed goods, never drink)')
door('d_dock_1', 'dock_customs', DW, 35, 90, 'dock_road', 1, locked=True, chosen_=True)
plot('dock_bonded', 'the bonded store', rect(487, 22, 501, 48), 'bonded_store', 1, street='dock_road', src='4.2.3', chosen_=True,
     note='a place of risk; tobacco and boxed goods, never drink')
door('d_bonded', 'dock_bonded', 494, 22, 180, None, None, locked=True, kind='loading', chosen_=True)
plot('dock_harbour_board', 'the Harbour Board', rect(503, 52, DW, 80), 'harbour_office', 2, street='dock_road', number=3, place='harbour_board', enterable=True,
     src='FIT-G1; 4.2.3; canon (Meridian Harbour Board)', note='the counter with an account and a clerk who sells shipment times; the clock over the door (prototype)')
door('d_dock_3', 'dock_harbour_board', DW, 66, 90, 'dock_road', 3, locked=False, chosen_=True)
DE = 540 + 5.0 + KERB_W + PAV   # 547.125
plot('dock_gate', 'the dock gate', rect(DE, 200, DE + 8, 220), 'dock_gate', 1, street='dock_road', place='dock_gate', enterable=False,
     src='FIT-G1 (the dock gate and its yard mouth at y 210); 4.2.3', note='the gate hut and the striped pole across the yard mouth; the docks beyond are off the map', chosen_=True)
door('d_dock_gate', 'dock_gate', DE, 210, 270, 'dock_road', None, locked=True, kind='gate', note='the pole across the yard mouth; past it is the working dock, off the map')

# --- Warehouse Row, east side: Norman Dent's warehouses
WE = 480 + 3.5 + KERB_W + PAV   # 485.625
n = 0
for (y0, y1) in [(90, 150), (160, 200), (230, 300), (306, 343.375)]:
    n += 1
    plot('dent_%d' % n, "Dent's warehouse %d" % n, rect(WE, y0, DW, y1), 'warehouse', 2, street='warehouse_row', number=n * 2 - 1,
         place=('dents_warehouses' if n == 1 else None), src='FIT-G1; 4.2.2 (Norman Dent\'s warehouses)', chosen_=True)
    door('d_wr_%d' % (n * 2 - 1), 'dent_%d' % n, WE, (y0 + y1) / 2.0, 270, 'warehouse_row', n * 2 - 1, locked=True, kind='loading', chosen_=True)
plot('dock_gate_sheds', "the dock gate's sheds", rect(503, 202, DW, 222), 'shed', 1, street='dock_road', src='G1 (sight breakers: the dock gate\'s sheds)', chosen_=True)
door('d_gate_sheds', 'dock_gate_sheds', DW, 212, 90, 'dock_road', None, locked=True, chosen_=True)

# --- Cold Store Road
CN = 350 + 4.5 + KERB_W + PAV    # 356.625
CS = 350 - 4.5 - KERB_W - PAV    # 343.375
cold = [P(300, CN), P(334, CN), P(334, 372), P(346, 372), P(346, CN), P(470, CN), P(470, 392), P(300, 392)]
plot('cold_stores', 'the Old Basin Cold Stores', cold, 'cold_store', 2, street='coldstore_road', number=1, place='cold_stores', enterable=False,
     src='4.2.2 (x 300 to 470, north side, a 170 m block, loading yard mouth at x 340)', note='the grey shed with the frosted pipes; the packing shift leaves at half past five',
     loading_yard=rect(334, CN, 346, 372))
door('d_cold_yard', 'cold_stores', 340, 372, 180, 'coldstore_road', 1, locked=False, kind='loading', note='the loading doors at the back of the loading yard, whose mouth is at x 340; open on the shift')
door('d_cold_office', 'cold_stores', 360, CN, 180, 'coldstore_road', 1, locked=True, kind='office', chosen_=True, note="the office door (the cold-store deputy's)")
plot('lot', 'the used-car lot', rect(166.625, 356.625, 202, 395), 'car_lot', None, building=False, street='north_road', place='car_lot',
     src='FIT-G1 (y 360 to 395); 2.15 (a car from the lot, 600 to 1,200 pounds)', note='bunting, cars with prices in the windscreens; the hut', chosen_=True)
door('d_lot_gate', 'lot', 166.625, 375, 270, 'north_road', None, locked=False, kind='gate', chosen_=True, note='the lot\'s open front on North Road')
plot('lot_hut', "the lot's hut", rect(192, 384, 200, 393), 'office', 1, street='north_road', src='chosen', chosen_=True)
door('d_lot_hut', 'lot_hut', 196, 384, 180, None, None, locked=False, chosen_=True)
plot('cs_garage', "Holt's garage", rect(476, CN, DW, 392), 'garage', 1, street='coldstore_road', number=3, place='garage', enterable=True,
     src='chosen (somewhere to respray or change plates: 2.3, GV-02)', chosen_=True, note='repairs and resprays; a pit and a compressor')
door('d_cs_3', 'cs_garage', 504, CN, 180, 'coldstore_road', 3, locked=False, kind='workshop', chosen_=True)
n = 4
for x0 in range(208, 296, 11):
    plot('cs_house_%d' % (n // 2), '%d Cold Store Road' % (n + 1), rect(x0, CN, x0 + 9, CN + 9), 'home', 2, street='coldstore_road', number=n + 1, src='chosen', chosen_=True)
    door('d_cs_%d' % (n + 1), 'cs_house_%d' % (n // 2), x0 + 4.5, CN, 180, 'coldstore_road', n + 1, chosen_=True)
    n += 2
plot('cs_agar', 'Agar\'s agents', rect(268, 325, 290, CS), 'estate_agent', 2, street='coldstore_road', number=2, place='agar_base', enterable=False,
     src='RT2-08 (Agar\'s base: an estate agent\'s office on the cold-store road holding his papers)', note='plate glass, a brass plate; his papers in the back room')
door('d_cs_2', 'cs_agar', 279, CS, 0, 'coldstore_road', 2, locked=True, chosen_=True)
for i, x0 in enumerate([296, 312]):
    plot('cs_workshop_%d' % (i + 1), 'the workshop', rect(x0, 322, x0 + 14, CS), 'workshop', 1, street='coldstore_road', number=4 + 2 * i, src='chosen', chosen_=True)
    door('d_cs_%d' % (4 + 2 * i), 'cs_workshop_%d' % (i + 1), x0 + 7, CS, 0, 'coldstore_road', 4 + 2 * i, chosen_=True)
# --- Basin Road (west side warehouses, east side Iveson's yard above the basin)
def along(pts_a, pts_b, s, off):
    """Point at distance s along segment a->b, offset 'off' to the left (positive) of the direction of travel."""
    dx, dy = pts_b[0] - pts_a[0], pts_b[1] - pts_a[1]
    L = math.hypot(dx, dy)
    ux, uy = dx / L, dy / L
    nx, ny = -uy, ux
    return (pts_a[0] + ux * s + nx * off, pts_a[1] + uy * s + ny * off)

def orect(a, b, s0, s1, off0, off1):
    return [P(*along(a, b, s0, off0)), P(*along(a, b, s1, off0)), P(*along(a, b, s1, off1)), P(*along(a, b, s0, off1))]

BA, BB = (250.0, 0.0), (210.0, 350.0)
bearing_left_basin = (math.degrees(math.atan2(-(BB[1] - BA[1]), -(BB[0] - BA[0]))) )  # unused helper
def compass(dx, dy):
    return round((math.degrees(math.atan2(dx, dy)) + 360) % 360, 1)
# Basin Road runs north-north-west; its left side is west. Frontage offset 3.5 + 0.125 + 2.0 = 5.625
FO = 3.5 + KERB_W + PAV
dirx, diry = (BB[0] - BA[0]), (BB[1] - BA[1])
L = math.hypot(dirx, diry)
face_west = compass(-diry / L, dirx / L)   # the left normal points out of the west-side buildings toward the road: reverse it
face_to_road_from_west = compass(diry / L, -dirx / L)
n = 0
for (s0, s1) in [(36, 76), (82, 122), (126, 147), (155, 196), (202, 246)]:
    n += 1
    pid = 'basin_wh_%d' % n
    plot(pid, 'Basin Road warehouse %d' % n, orect(BA, BB, s0, s1, FO, FO + 22), 'warehouse', 2, street='basin_road', number=2 * n - 1,
         src='G1 (the basin\'s warehouses as sight breakers); chosen', chosen_=True)
    dx_, dy_ = along(BA, BB, (s0 + s1) / 2.0, FO)
    door('d_br_%d' % (2 * n - 1), pid, dx_, dy_, face_to_road_from_west, 'basin_road', 2 * n - 1, kind='loading', chosen_=True)
# Iveson's yard (east side of Basin Road, y 260 to 320) with the hut inside
s_iv0, s_iv1 = 262.0 / diry * L, 320.0 / diry * L
iv = orect(BA, BB, s_iv0, s_iv1, -FO + 2.0 - 0.0 - 2.0, -FO - 36)
plot('iveson_yard', "Iveson's yard", iv, 'scrap_yard', None, building=False, street='basin_road', number=2, place='iveson_yard', enterable=True,
     src='4.3.5 (Basin Road, y 260 to 320); prototype (the scrap yard with the crane and the dog)', note='crane, weighbridge, the yard dog on a chain; the yard hand in his twenties')
gx, gy = along(BA, BB, (s_iv0 + s_iv1) / 2.0, -FO + 0.0)
door('d_br_2', 'iveson_yard', gx, gy, compass(-diry / L * -1, dirx / L * -1) if False else face_west, 'basin_road', 2, locked=False, kind='yard_gate',
     note='the yard gate, open 07:30 to 17:00', chosen_=True)
hx, hy = along(BA, BB, s_iv0 + 40, -FO - 20)
plot('iveson_hut', "Iveson's hut", rect(hx - 4, hy - 3, hx + 4, hy + 3), 'hut', 1, street='basin_road', place='iveson_hut', enterable=True,
     src='4.3.5 (one of the eight named enterable places; a break-in at night)', note='the tarred hut by the weighbridge (prototype)')
door('d_iveson_hut', 'iveson_hut', hx - 4, hy, 270, None, None, locked=True, kind='front', chosen_=True)

# --- Basin Top (north side)
BT = 255 + 3.5 + KERB_W + PAV   # 260.625
plot('burned_warehouse', 'the burned warehouse', rect(300, BT, 360, 300), 'ruin', 2, street='basin_top', number=5, place='burned_warehouse',
     src='FIT-G1 (x 300 to 360); 4.2.2; the warehouse fire', note='the black shell with the boarded doors (prototype)')
door('d_bt_5', 'burned_warehouse', 330, BT, 180, 'basin_top', 5, locked=True, note='boarded; a loose board at the east end', chosen_=True)
for i, (x0, x1) in enumerate([(266, 296), (366, 410), (416, 470)]):
    num = [3, 7, 9][i]
    plot('bt_wh_%d' % num, '%d Basin Top' % num, rect(x0, BT, x1, 300), 'warehouse', 2, street='basin_top', number=num,
         place=('net_loft' if num == 3 else None), src='chosen', chosen_=True, note=('the net loft' if num == 3 else 'a basin warehouse'))
    door('d_bt_%d' % num, 'bt_wh_%d' % num, (x0 + x1) / 2.0, BT, 180, 'basin_top', num, kind='loading', chosen_=True)

# --- North Road
NW = 160 - 4.5 - KERB_W - PAV   # 153.375
NE = 160 + 4.5 + KERB_W + PAV   # 166.625
def north_house_rows(side, y_ranges, start_num):
    num = start_num
    for (y0, y1) in y_ranges:
        y = y0
        while y + 6.0 <= y1 + 0.01:
            pid = 'nr_%d' % num
            if side == 'west':
                plot(pid, '%d North Road' % num, rect(NW - 9, y, NW, y + 6), 'home', 2, street='north_road', number=num, src='chosen', chosen_=True)
                door('d_nr_%d' % num, pid, NW, y + 3, 90, 'north_road', num, chosen_=True)
            else:
                plot(pid, '%d North Road' % num, rect(NE, y, NE + 9, y + 6), 'home', 2, street='north_road', number=num, src='chosen', chosen_=True)
                door('d_nr_%d' % num, pid, NE, y + 3, 270, 'north_road', num, chosen_=True)
            num += 2
            y += 6.0
    return num
# west side: even numbers from the foot; east side odd
wnext = north_house_rows('west', [(84, 126)], 2)
plot('nr_wayne', "Harrison's", rect(NW - 10, 128, NW, 140), 'pawnbroker', 2, street='north_road', number=wnext, place='waynes_pawn', enterable=True,
     src='4.3.3 (the pawn, Wayne Harrison, 10:00 to 17:00, back room by knock to 22:00)', note="Wayne Harrison's pawn; three brass balls", chosen_=True)
door('d_nr_%d' % wnext, 'nr_wayne', NW, 134, 90, 'north_road', wnext, locked=False, chosen_=True)
door('d_nr_wayne_back', 'nr_wayne', NW - 10, 134, 270, None, None, locked=True, kind='back', chosen_=True, note='the back room door, by knock to 22:00')
wnext = north_house_rows('west', [(142, 196)], wnext + 2)
plot('nr_corner_shop', 'the corner shop', rect(NW - 10, 198, NW, 210), 'corner_shop', 2, street='north_road', number=wnext, src='chosen', chosen_=True,
     note='a general shop with cards in the window')
door('d_nr_%d' % wnext, 'nr_corner_shop', NW, 204, 90, 'north_road', wnext, locked=False, chosen_=True)
wnext = north_house_rows('west', [(212, 248)], wnext + 2)
wnext = north_house_rows('west', [(338, 398)], wnext)
enext = north_house_rows('east', [(72, 102)], 1)
plot('nr_builders', "the builders' merchant", rect(NE, 104, NE + 16, 146), 'builders_yard', 1, street='north_road', number=enext, src='chosen', chosen_=True,
     note='timber and sand under a lean-to; the yard closed at night')
door('d_nr_%d' % enext, 'nr_builders', NE, 125, 270, 'north_road', enext, locked=False, kind='yard_gate', chosen_=True)
enext = north_house_rows('east', [(153, 201)], enext + 2)
plot('nr_old_pub', 'the Mariner (boarded)', rect(NE, 204, NE + 14, 222), 'pub_boarded', 2, street='north_road', number=enext, src='canon (other pubs remain as buildings, boarded); 4.10', chosen_=True,
     note='boarded since 1988; never entered for drink')
door('d_nr_%d' % enext, 'nr_old_pub', NE, 213, 270, 'north_road', enext, locked=True, chosen_=True)
enext = north_house_rows('east', [(226, 286)], enext + 2)
plot('cammack_lockups_s', "Cammack's lock-ups (south court)", rect(NE, 290, NE + 24, 299), 'lock_ups', 1, street='north_road', src='RT2-08; FIT-G1', chosen_=True,
     note='lock-up garages facing the north warehouse cut')
plot('cammack_lockups', "Cammack's lock-ups", rect(NE, 301, NE + 24, 320), 'lock_ups', 1, street='north_road', place='cammack_base', enterable=False,
     src='RT2-08; FIT-G1 (east side, y 290 to 320)', note="the north court of lock-ups on the cut; Danny Cammack's base (the end lock-up holds his things)", chosen_=True)
for i in range(5):
    if i < 2:
        door('d_lockup_%d' % (i + 1), 'cammack_lockups_s', NE + 6 + 8 * i, 299, 0, 'north_road', None, locked=True, kind='garage', chosen_=True, note="a lock-up's up-and-over door on the cut")
    else:
        door('d_lockup_%d' % (i + 1), 'cammack_lockups', NE + 4 + 8 * (i - 2), 301, 180, 'north_road', None, locked=True, kind='garage', chosen_=True, note="a lock-up's up-and-over door on the cut")
enext = north_house_rows('east', [(324, 342)], enext + 2)

# --- Back Parade (north side): the chip shop at the top of the parade and two houses
BPA, BPB = BEND_A, BEND_B
bp_face = compass(*(lambda dx, dy, L: (0.0 - (-dy / L), 0.0 - (dx / L)))(BPB[0] - BPA[0], BPB[1] - BPA[1], seglen(BPA, BPB)))
for i, (s0, s1, pid, name, use, place, enter, num) in enumerate([
        (6, 15, 'bp_chippy', "Dobson's", 'chip_shop', 'chip_shop', True, 1),
        (16, 23, 'bp_house_3', '3 Back Parade', 'home', None, False, 3),
        (24, 31, 'bp_house_5', '5 Back Parade', 'home', None, False, 5),
        ]):
    plot(pid, name, orect(BPA, BPB, s0, s1, 6.625, 6.625 + 9), use, 2, street='back_parade', number=num, place=place, enterable=enter,
         src=('G10 (the chip shop on the parade, 11:30 to 14:00 and 17:00 to 23:30)' if place else 'chosen'), chosen_=True,
         note=('the chip shop at the top of the parade' if place else ''))
    dx_, dy_ = along(BPA, BPB, (s0 + s1) / 2.0, 6.625)
    door('d_bp_%d' % num, pid, dx_, dy_, bp_face, 'back_parade', num, locked=not enter, chosen_=True)

# --- Chapel Lane
CLN = 260 + 3.5 + KERB_W + PAV   # 265.625
CLS = 260 - 3.5 - KERB_W - PAV   # 254.375
plot('chapel', 'the chapel', rect(-20, CLN + 3, 14, CLN + 27), 'chapel', 1, street='chapel_lane', place='chapel', enterable=True,
     src='4.3.6 (the chapel and the closed school, x -20 to 60); canon (religion part of life)', note='the chapel with the green door, a bench outside (prototype); three steps and railings', number=1)
door('d_cl_1', 'chapel', -3, CLN + 3, 180, 'chapel_lane', 1, locked=False, note='open 07:00 to 20:00 (places.json)', chosen_=True)
plot('chapel_forecourt', "the chapel's yard", rect(-20, CLN, 14, CLN + 3), 'forecourt', building=False, src='chosen', chosen_=True)
plot('chapel_hall', 'the chapel hall', rect(-20, CLN + 29, 14, CLN + 43), 'hall', 1, street='chapel_lane', place='chapel_hall', enterable=True,
     src='4.3.6 (the hall: tea and talk on Tuesday 19:00 to 21:30; one of the eight enterable places)', note='behind the chapel, reached by the path at its west side')
door('d_chapel_hall', 'chapel_hall', -3, CLN + 29, 180, 'chapel_lane', None, locked=False, kind='side', note='reached by the path past the chapel\'s west side', chosen_=True)
plot('priests_house', "the priest's house", rect(18, CLN, 28, CLN + 10), 'home', 2, street='chapel_lane', number=3, place='priests_house', enterable=True,
     src='4.3.6 (the priest\'s house by the chapel; the first fare goes there)', note='the house by the chapel gate with the slippers on the step (prototype)')
door('d_cl_3', 'priests_house', 23, CLN, 180, 'chapel_lane', 3, locked=True, chosen_=True)
plot('cl_barber', 'the barber', rect(32, CLN, 38, CLN + 9), 'barber', 2, street='chapel_lane', number=5, place='barber', enterable=True,
     src='prototype (the striped pole on Chapel Lane, 5 Chapel Lane); 2.4 (a barber for a week)', chosen_=True)
door('d_cl_5', 'cl_barber', 35, CLN, 180, 'chapel_lane', 5, locked=False, chosen_=True)
num = 7
for x0 in list(range(40, 68, 6)) + list(range(72, 132, 6)):
    pid = 'cl_%d' % num
    is_doc = (num == 23)
    plot(pid, ('the retired doctor\'s' if is_doc else '%d Chapel Lane' % num), rect(x0, CLN, x0 + 6, CLN + 9), 'home', 2, street='chapel_lane', number=num,
         place=('doctors' if is_doc else None), enterable=is_doc, src=('4.3.4 (the retired doctor\'s terrace stitches wounds, 20 pounds); G1' if is_doc else 'chosen'), chosen_=True,
         note=('the end of the terrace, the brass plate taken down' if is_doc else ''))
    door('d_cl_%d' % num, pid, x0 + 3, CLN, 180, 'chapel_lane', num, locked=True, chosen_=True)
    num += 2
plot('school', 'the school (closed)', rect(0, CLS - 30, 60, CLS - 6), 'school_closed', 2, street='chapel_lane', number=2, place='school',
     src='canon (THE SCHOOL STANDS CLOSED; nobody is in it); 4.3.6', note='boarded, padlocked gates; nobody inside, ever')
plot('school_yard', 'the school yard', rect(0, CLS - 6, 60, CLS), 'yard', building=False, src='chosen', chosen_=True, note='padlocked gates; empty')
door('d_cl_2', 'school_yard', 30, CLS, 0, 'chapel_lane', 2, locked=True, kind='gate', note='padlocked', chosen_=True)
door('d_school', 'school', 30, CLS - 6, 0, None, None, locked=True, kind='front', note='boarded; nobody inside, ever', chosen_=True)
num = 4
for x0 in range(64, 130, 6):
    pid = 'cl_%d' % num
    plot(pid, '%d Chapel Lane' % num, rect(x0, CLS - 9, x0 + 6, CLS), 'home', 2, street='chapel_lane', number=num, src='chosen', chosen_=True)
    door('d_cl_%d' % num, pid, x0 + 3, CLS, 0, 'chapel_lane', num, chosen_=True)
    num += 2
plot('allotments', 'the allotments', rect(-78, CLS - 60, -24, CLS), 'allotments', building=False, street='chapel_lane', place='allotments',
     src='24 Nov pastimes ruling (a pigeon loft on the allotments)', chosen_=True, note='plots, sheds, water butts; the pigeon loft at the back')
door('d_allot_gate', 'allotments', -51, CLS, 0, 'chapel_lane', None, locked=False, kind='gate', chosen_=True)
plot('pigeon_loft', 'the pigeon loft', rect(-60, CLS - 56, -48, CLS - 50), 'pigeon_loft', 1, street='chapel_lane', place='pigeon_loft', enterable=True,
     src='24 Nov pastimes ruling', chosen_=True)
door('d_pigeon_loft', 'pigeon_loft', -54, CLS - 50, 0, None, None, locked=False, chosen_=True)
for i, x0 in enumerate(range(-76, -26, 8)):
    pid = 'cl_w_%d' % i
    nm = 101 + 2 * i
    plot(pid, '%d Chapel Lane' % nm, rect(x0, CLN, x0 + 7, CLN + 9), 'home', 2, street='chapel_lane', number=nm, src='chosen', chosen_=True)
    door('d_cl_%d' % nm, pid, x0 + 3.5, CLN, 180, 'chapel_lane', nm, chosen_=True)

# --- The quay road's south side: the ferry landing, fish dock structures
plot('ferry_landing', 'the ferry landing', [P(4, QE), P(26, QE), P(26, -28), P(4, -28)], 'landing', building=False, street='quay_road', place='ferry_landing',
     src='4.2.1 (the plan\'s origin; the landing and its rank 0 to 30); canon (Meridian Ferry)', note='the gangway and pontoon; the shelter under the last lamp')
PLOTS[-1]['on_quay_apron'] = True
door('d_landing_gangway', 'ferry_landing', 15, QE, 0, 'quay_road', None, locked=False, kind='gate', chosen_=True, note='the head of the gangway')
plot('landing_shelter', 'the landing shelter', rect(1, -7.2, 5, -5.2), 'shelter', 1, street='quay_road', src='prototype (the shelter under the last lamp)', chosen_=True)
PLOTS[-1]['on_quay_apron'] = True
plot('ice_hut', 'the ice hut', rect(500, -7.0, 506, -4.8), 'hut', 1, street='quay_road', place='fish_dock', src='prototype (the stacked fish boxes and the ice hut)', chosen_=True)
PLOTS[-1]['on_quay_apron'] = True
door('d_ice_hut', 'ice_hut', 503, -4.8, 0, None, None, locked=True, chosen_=True)
plot('tea_stall', 'the tea stall', rect(548, 196, 551, 199), 'stall', None, building=False, street='dock_road', place='tea_stall',
     src='4.2.3 (a tea stall at the gate 22:00 to 06:00)', chosen_=True)
door('d_tea_stall', 'tea_stall', 548, 197.5, 270, 'dock_road', None, locked=False, kind='hatch', chosen_=True, note='the serving hatch')

# ---------------------------------------------------------------- named points
def pt(id, kind, x, y, **kw):
    d = dict(id=id, kind=kind, x=r2(x), y=r2(y))
    d.update(kw)
    return d

LAMPS = []
# Quay Street's four concrete columns, as built (4.1.1): street x 8 east, 18 west, 28 east, 38 west, setback 0.6 m from the kerb
for i, (sx, side) in enumerate([(8, 'east'), (18, 'west'), (28, 'east'), (38, 'west')]):
    x = 120 + (3.0 + KERB_W + 0.6) * (1 if side == 'east' else -1)
    LAMPS.append(pt('lamp_qs_%d' % (i + 1), 'lamp_column', x, qy(sx), road='quay_street', model='lamp_post_C', height_m=5.0, lamp='35 W low-pressure sodium',
                    src='4.1.1; 4.4; vignette-scene.json lighting'))
chosen('Lamp columns off Quay Street: concrete, the same model, every 30 m staggered on drivable roads (40 m on Dock Road, Warehouse Row, Basin Road and Basin Top), one at each end of the ginnel and the yards\' lane and one at the ginnel\'s Chapel Lane crossing')

def stagger_lamps(r, spacing):
    pts = r['pts']
    L = polylen(pts)
    s = spacing / 2.0
    k = 0
    off = r['carriageway_m'] / 2.0 + KERB_W + 0.6
    while s < L:
        # locate segment
        acc = 0
        for i in range(len(pts) - 1):
            l = seglen(pts[i], pts[i + 1])
            if acc + l >= s:
                side = 1 if k % 2 == 0 else -1
                if r['left']['kind'] == 'quay':
                    side = -1
                if r['right']['kind'] == 'quay':
                    side = 1
                x, y = along(pts[i], pts[i + 1], s - acc, off * side)
                LAMPS.append(pt('lamp_%s_%d' % (r['id'], k + 1), 'lamp_column', x, y, road=r['id'], model='lamp_post_C', height_m=5.0,
                                lamp='35 W low-pressure sodium', src='chosen (spacing)', chosen=True))
                break
            acc += l
        k += 1
        s += spacing
for r in ROADS:
    if r['id'] == 'quay_street':
        continue
    if r['foot_only']:
        continue
    stagger_lamps(r, 40.0 if r['id'] in ('dock_road', 'warehouse_row', 'basin_road', 'basin_top') else 30.0)
for rid, (x, y) in [('ginnel', GINNEL[0]), ('ginnel', (139.8, 262.5)), ('ginnel', GINNEL[-1]), ('yards_lane', (150.9, 62.0)), ('yards_lane', (159.6, 5.2))]:
    LAMPS.append(pt('lamp_%s_%d' % (rid, len([l for l in LAMPS if l['road'] == rid]) + 1), 'lamp_column', x, y, road=rid, model='lamp_post_C', height_m=5.0,
                    lamp='35 W low-pressure sodium', src='chosen', chosen=True))

VAULTS = [
    pt('vault_mickeys_fence', 'vault', 148.75, 11.0, way='yards_lane', across=[90, 270], height_m=1.1, what="Mickey's yard's back fence into the yards' lane",
       src='1.1.8; 4.3.1 (one vault place at the back fence, Tom 0.8 s, a constable 1.2 s)'),
    pt('vault_ginnel_backs', 'vault', 82.57, 40.0, way='ginnel', across=[0, 180], height_m=1.0, what='the low wall across the ginnel behind the shops',
       src='1.1.8 (three on the ginnel)', chosen=True),
    pt('vault_ginnel_bins', 'vault', 113.09, 159.0, way='ginnel', across=[11.2, 191.2], height_m=0.9, what='the bins chained across the ginnel',
       src='1.1.8; prototype (the bins across the west alley)', chosen=True),
    pt('vault_ginnel_fence', 'vault', 149.5, 295.0, way='ginnel', across=[16.7, 196.7], height_m=1.1, what='the broken fence across the ginnel\'s top',
       src='1.1.8', chosen=True),
    pt('vault_cut_150', 'vault', 196.43, 150.0, way='cut_150', across=[90, 270], height_m=1.0, what='the fence across the south warehouse cut',
       src='1.1.8 (one on each warehouse cut)', chosen=True),
    pt('vault_cut_300', 'vault', 187.86, 300.0, way='cut_300', across=[90, 270], height_m=1.1, what='the gate across the north cut by the lock-ups',
       src='1.1.8', chosen=True),
]
chosen('Vault place positions and heights (0.9 to 1.1 m): Mickey\'s back fence; on the ginnel a wall at (82.6, 40), bins at (113.1, 159), a fence at (149.5, 295); one mid-way along each cut')

# Quay edges, ladders and mooring bollards
QUAY_EDGES = [
    dict(id='edge_sea_west', name='the sea quay (west)', pts=[P(-80, QE), P(250, QE)], water='sea', cope_m=0.60, drop_to_water_m=3.2, src='4.2.1; research/south-quay (cope 0.60, water 3.20 m below at half tide)'),
    dict(id='edge_sea_east', name='the fish dock quay', pts=[P(480, QE), P(540, QE)], water='sea', cope_m=0.60, drop_to_water_m=3.2, src='4.2.2'),
    dict(id='edge_basin_west', name="the basin's west quay", pts=[P(basin_edge_x(10), 10), P(basin_edge_x(249.3), 249.3)], water='old_basin', cope_m=0.60, drop_to_water_m=3.2, src='G1 (west quay y 30 to 250)'),
    dict(id='edge_basin_north', name="the basin's north quay", pts=[P(basin_edge_x(249.3), 249.3), P(474.3, 249.3)], water='old_basin', cope_m=0.60, drop_to_water_m=3.2, src='G1'),
    dict(id='edge_basin_east', name="the basin's east quay", pts=[P(474.3, 249.3), P(474.3, 10)], water='old_basin', cope_m=0.60, drop_to_water_m=3.2, src='G1 (east quay y 30 to 250)'),
]
LADDERS, BOLLARDS = [], []
chosen('Quay ladders every 40 m along every quay edge (a man in the water is never more than 20 m from one), mooring bollards every 15 m; two bollards at each end of each foot-only way')
for e in QUAY_EDGES:
    a, b = e['pts'][0], e['pts'][-1]
    L = seglen(a, b)
    nlad = int(math.ceil(L / 40.0))
    sp = L / nlad
    s = sp / 2.0
    i = 0
    while s < L:
        x, y = along(a, b, s, 0)
        LADDERS.append(pt('ladder_%s_%d' % (e['id'][5:], i + 1), 'quay_ladder', x, y, edge=e['id'], src='4.2.4 (a man put in climbs out at the nearest ladder); chosen spacing', chosen=True))
        i += 1
        s += sp
    s = 7.5
    i = 0
    while s < L:
        x, y = along(a, b, s, 0.6 if e['water'] == 'sea' else 0.6)
        BOLLARDS.append(pt('bollard_%s_%d' % (e['id'][5:], i + 1), 'mooring_bollard', x, y, edge=e['id'], src='4.2.1; chosen spacing', chosen=True))
        i += 1
        s += 15.0
for r in ROADS:
    if not r['foot_only']:
        continue
    for end, (p0, p1) in (('a', (r['pts'][0], r['pts'][1])), ('b', (r['pts'][-1], r['pts'][-2]))):
        for k, off in enumerate((-0.6, 0.6)):
            x, y = along(p0, p1, 0.3, off * r['carriageway_m'] / 2.0)
            BOLLARDS.append(pt('bollard_%s_%s%d' % (r['id'], end, k + 1), 'lane_bollard', x, y, way=r['id'], src='G1 (foot-only lanes are bollarded or gated at both ends)'))

PHONE_BOXES = [
    pt('phone_landing', 'phone_box', 32.0, -5.6, model='KX100', src='RT2-19 (by the landing)', chosen=True),
    pt('phone_parade', 'phone_box', 120 + 3.0 + KERB_W + 0.55 + 0.457, qy(16.5), model='KX100', src='vignette-scene.json furniture E3 (street x 16.5, east, setback 0.55); RULINGS 2 Oct'),
    pt('phone_dock_gate', 'phone_box', 548.6, 224.0, model='KX100', src='RT2-19 (at the dock gate)', chosen=True),
]
RANKS = [
    dict(id='rank_mickeys', name="Mickey's rank", road='quay_street', pts=[P(122.8, qy(5.0)), P(122.8, qy(10.0))], cars=2, holder='firm',
         src='canon (a rank outside); hook-cast.json mickeys_rank (street x 7.5 to 8.7)'),
    dict(id='rank_ferry', name='the ferry rank', road='quay_road', pts=[P(4, -3.4), P(24, -3.4)], cars=4, holder=None,
         src='4.2.1 (the landing and its rank 0 to 30); 2.15.2 (won by being there)'),
    dict(id='rank_north', name='the north road rank', road='north_road', pts=[P(157.2, 378), P(157.2, 392)], cars=3, holder=None,
         src='2.15.2 (the ferry rank and a second); prototype (the north road rank)', chosen=True),
]
POSTS = [
    pt('post_dock_gate', 'turf_post', 547.6, 204.0, hours='06:00-22:00', src='RT2-09'),
    pt('post_cold_store', 'turf_post', 340.0, 355.6, hours='06:00-22:00', src='RT2-09; the loading yard mouth', chosen=True),
    pt('post_landing', 'turf_post', 14.0, -6.2, hours='22:00-02:00', src='RT2-09; 4.2.1 (the landing\'s window 22:00 to 01:00)', chosen=True),
]
RIVAL_BASES = [
    dict(id='base_widow', rival='widow', name="the Widow's dock office", plot='quay_net_store', door='d_widow_office', src='RT2-08'),
    dict(id='base_agar', rival='agar', name="Agar's agents", plot='cs_agar', door='d_cs_2', src='RT2-08'),
    dict(id='base_cammack', rival='cammack', name="Cammack's lock-ups", plot='cammack_lockups', door='d_lockup_3', src='RT2-08'),
]
POLICE_POINTS = [
    pt('beat_mickeys_door', 'beat_point', 123.6, qy(4.65), src='G5 (Mickey\'s door tried on the short round)'),
    pt('beat_yards_lane', 'beat_point', 150.0, 35.0, src='G5 (the yards\' lane)'),
    pt('beat_landing', 'beat_point', 15.0, -5.0, src='G5 (the landing looked over for 15 s)'),
    pt('patrol_wait_north_edge', 'edge_wait', 160.0, 396.0, src='G3 (the patrol waits on the road of the edge)'),
    pt('patrol_wait_west_edge', 'edge_wait', -76.0, 260.0, src='G3'),
    pt('stop_north_road', 'stop_point', 157.4, 230.0, src='G2 (the patrol stops a driver); chosen place', chosen=True),
    pt('stop_quay_road', 'stop_point', 60.0, -3.0, src='G2; chosen place', chosen=True),
    pt('stop_coldstore_road', 'stop_point', 420.0, 347.4, src='G2; chosen place', chosen=True),
    pt('stop_dock_road', 'stop_point', 537.4, 120.0, src='G2; chosen place', chosen=True),
]
WEAPON_PLACES = dict(
    note='1.3.5 The street as a weapon: seven kinds. Walls are every building outline face; doorways every door; kerbs every drivable road\'s kerb line; the quay edge every quay edge; car bonnets every car. Railings and steps are listed here.',
    railings=[
        dict(id='rail_qs_guard', pts=[P(123.6, qy(8.5)), P(123.6, qy(11.5))], height_m=1.0, src='vignette-scene.json furniture E8 (guard railing, street x 10, east)'),
        dict(id='rail_bridge_north', pts=[P(250, 6.5), P(480, 6.5)], height_m=1.1, src='the basin bridge parapet', chosen=True),
        dict(id='rail_bridge_south', pts=[P(250, -6.5), P(480, -6.5)], height_m=1.1, src='the basin bridge parapet', chosen=True),
        dict(id='rail_chapel', pts=[P(-20, CLN + 0.2), P(-8, CLN + 0.2)], height_m=1.0, src='chosen (railings at the chapel yard)', chosen=True),
        dict(id='rail_landing', pts=[P(4, QE - 0.2), P(26, QE - 0.2)], height_m=1.0, src='chosen (the landing\'s rail)', chosen=True),
    ],
    steps=[
        dict(id='steps_chapel', x=-3.0, y=CLN + 1.5, rise_m=0.5, src='chosen', chosen=True),
        dict(id='steps_regent', x=50.0, y=QN + 0.4, rise_m=0.3, src='chosen', chosen=True),
        dict(id='steps_harbour_board', x=DW - 0.6, y=66.0, rise_m=0.45, src='chosen', chosen=True),
    ],
)
LANDMARKS = [
    pt('lm_mickeys', 'landmark', 125.1, qy(6), name="Mickey's", said="the cab office at the bottom of Quay Street", src='prototype way.js; canon'),
    pt('lm_chapel', 'landmark', -3.0, CLN + 15, name='the chapel', said='the chapel on Chapel Lane, the green door', src='4.1.3 (past the chapel, second left); prototype'),
    pt('lm_caff', 'landmark', 66.0, QN + 8, name="Rinaldi's", said='the caff on the quay by the ginnel, steam on the glass', src='4.1.3 (try the caff)'),
    pt('lm_cold_stores', 'landmark', 385.0, 374.0, name='the cold stores', said='the big grey shed on Cold Store Road', src='4.2.2'),
    pt('lm_dock_gate', 'landmark', 549.0, 210.0, name='the dock gate', said='the gate with the hut and the striped pole', src='4.2.3; prototype'),
    pt('lm_ferry_landing', 'landmark', 15.0, -15.0, name='the ferry landing', said='the landing at the west end of the quay', src='4.2.1'),
    pt('lm_basin_bridge', 'landmark', 365.0, 0.0, name='the basin bridge', said='the bridge over the Old Basin', src='G1'),
    pt('lm_burned_warehouse', 'landmark', 330.0, 280.0, name='the burned warehouse', said='the black shell on Basin Top', src='4.2.2'),
    pt('lm_fish_dock', 'landmark', 510.0, -6.0, name='the fish dock', said='the fish boxes and the ice hut at the east end of the quay', src='4.2.2'),
    pt('lm_boxing_club', 'landmark', 220.0, QN + 13, name='the boxing club', said="the old hall behind the chandler's store, a bare bulb over the door", src='4.3.3'),
    pt('lm_car_lot', 'landmark', 184.0, 375.0, name='the car lot', said='the bunting at the top of North Road', src='G1'),
    pt('lm_harbour_board', 'landmark', 518.0, 66.0, name='the Harbour Board', said='the stone office with the clock over the door', src='prototype; canon'),
    pt('lm_snooker_hall', 'landmark', 30.0, QN + 9, name='the snooker hall', said='upstairs on the quay, by the landing', src='24 Nov ruling', chosen=True),
    pt('lm_school', 'landmark', 30.0, CLS - 18, name='the old school', said='the closed school on Chapel Lane, boarded', src='canon', chosen=True),
    pt('lm_old_pub', 'landmark', NE + 7, 213.0, name='the boarded pub', said='the boarded-up Mariner on North Road', src='canon', chosen=True),
    pt('lm_basin', 'landmark', 365.0, 128.0, name='the Old Basin', said='the old dock behind the quay', src='atlas-01 H2'),
]
EDGES = [
    dict(id='edge_north', road='north_road', x=160, y=400, districts=['copper_row', 'the_exchange', 'the_parade', 'gullwing'],
         landmarks={'copper_row': 'the market hall', 'the_exchange': 'the police station and the council offices', 'the_parade': 'the Tivoli', 'gullwing': 'the Winter Rooms on the front'},
         src='4.1.4; G3; canon (seven districts); atlas-01 landmarks', chosen=True),
    dict(id='edge_west', road='chapel_lane', x=-80, y=260, districts=['ironside', 'fairview'],
         landmarks={'ironside': 'the retort works', 'fairview': 'Fairview chapel up the hill'}, src='4.1.4; G3; atlas-01', chosen=True),
]
chosen('Which districts each soft edge offers: the north edge Copper Row, the Exchange (the police station, the licensing hearing), the Parade and Gullwing; the west edge Ironside and Fairview')
OFF_MAP = [
    dict(id='police_station', name='the police station', district='the_exchange', via='edge_north', src='atlas-01 E2 (the Exchange); 4.3.7 (custody is under 2 real minutes of play, not walked)'),
    dict(id='infirmary', name='the Infirmary', district='the_exchange', via='edge_north', src='prototype (out along the west road); 4.3.8', chosen=True),
    dict(id='licensing', name="the council's licensing committee", district='the_exchange', via='edge_north', src='RT2-18'),
]
OPEN.append('G3 puts the north soft edge at y 440; G1\'s table and footprint end North Road at y 400. The plan uses 400.')

# ---------------------------------------------------------------- props (Study 4: at least 5 per 10 m of street)
PROP_KINDS = ['dustbin', 'dustbin', 'sign', 'crates', 'bench', 'bicycle', 'litter', 'sign', 'crates', 'tub', 'dustbin', 'litter', 'grit_bin', 'fish_boxes']
FORBIDDEN_PROPS = ['skip', 'pallets', 'wheelie_bin', 'tactile_paving', 'satellite_dish_on_street']
chosen('Props: a seeded scatter (seed 19900214, the vignette\'s) on the pavements of every drivable road at 5 per 10 m (Quay Street 9 per 10 m, as its scene file), from a fixed kind list; no skips or pallets until real, no wheeled bins (1990)')
PROPS = []
rng = random.Random(19900214)
for r in ROADS:
    if r['foot_only']:
        per10 = 2.0
    else:
        per10 = 9.0 if r['id'] == 'quay_street' else 5.0
    L = r['length_m']
    count = int(math.ceil(L / 10.0 * per10))
    pts = r['pts']
    for k in range(count):
        s = (k + rng.random()) * L / count
        acc = 0
        for i in range(len(pts) - 1):
            l = seglen(pts[i], pts[i + 1])
            if acc + l >= s or i == len(pts) - 2:
                if r['foot_only']:
                    off = (rng.random() - 0.5) * r['carriageway_m'] * 0.6
                else:
                    sides = [sd for sd in ('left', 'right') if r[sd]['kind'] in ('pavement', 'quay', 'bridge')]
                    sd = rng.choice(sides)
                    w = r[sd]['width_m']
                    o = r['carriageway_m'] / 2.0 + KERB_W + 0.3 + rng.random() * (w - 0.6)
                    off = o if sd == 'left' else -o
                kind = rng.choice(PROP_KINDS)
                if kind == 'fish_boxes' and r['id'] not in ('quay_road', 'warehouse_row', 'dock_road', 'basin_road'):
                    kind = 'crates'
                x, y = along(pts[i], pts[i + 1], min(s - acc, l), off)
                PROPS.append(dict(id='prop_%s_%d' % (r['id'], k + 1), kind=kind, x=r2(x), y=r2(y), road=r['id']))
                break
            acc += l
# Quay Street's built furniture and the pillar box
STREET_FURNITURE = [
    pt('pillar_box_qs', 'pillar_box', 120 + 3.0 + KERB_W + 0.6 + 0.3, qy(27.0), src='vignette-scene.json furniture E4 (street x 27, east)'),
    pt('dustbin_qs_21', 'dustbin', 120 + 3.0 + KERB_W + 1.6, qy(21.4), src='vignette-scene.json furniture E13'),
    pt('bus_stop_qs', 'bus_stop', 116.4, qy(14.0), src='prototype (the shelter by the lamp, opposite the launderette); chosen place', chosen=True),
    pt('bench_triangle', 'bench', 92.0, 7.6, src='chosen (the triangle by the ginnel\'s mouth)', chosen=True),
    pt('pillar_box_north', 'pillar_box', NE - 0.9, 205.0, src='chosen', chosen=True),
    pt('fish_boxes_dock', 'fish_boxes', 520.0, -6.0, src='prototype (stacked fish boxes)', chosen=True),
]
FISHING = [
    pt('fishing_quay_east', 'fishing_spot', 200.0, QE + 0.6, src='24 Nov pastimes ruling (fishing off the quay)', chosen=True),
    pt('fishing_quay_west', 'fishing_spot', 160.0, QE + 0.6, src='24 Nov pastimes ruling', chosen=True),
    pt('fishing_basin_north', 'fishing_spot', 300.0, 249.3 + 0.6, src='24 Nov pastimes ruling', chosen=True),
]
NAME_PLATES = []
chosen('Name plates: one at each end of every named street, on the left-hand wall or railing 1.5 m in from the corner, white enamel, black Marcellus SC capitals')
for r in ROADS:
    if not r['plates']:
        continue
    pts = r['pts']
    a0, a1 = pts[0], pts[1]
    b0, b1 = pts[-1], pts[-2]
    off = r['carriageway_m'] / 2.0 + KERB_W + PAV - 0.1
    for end, (p0, p1) in (('a', (a0, a1)), ('b', (b0, b1))):
        x, y = along(p0, p1, (r['carriageway_m'] if end == 'a' else 0) / 2.0 + 6.0, off)
        NAME_PLATES.append(pt('plate_%s_%s' % (r['id'], end), 'name_plate', x, y, road=r['id'], text=r['name'].upper(), font='Marcellus SC',
                              src='4.1.3 (Marcellus SC, his ruling of 30 Sep)'))

# ---------------------------------------------------------------- walking and driving graphs
NODES = {}
EDGES_G = []

def node(id, x, y, kind, **kw):
    if id not in NODES:
        d = dict(id=id, x=r2(x), y=r2(y), kind=kind)
        d.update(kw)
        NODES[id] = d
    return id

JUNCTIONS = {
    (0.0, 0.0): 'j_landing', (120.0, 0.0): 'j_quay_street_foot', (159.0, 0.0): 'j_yards_lane_foot', (250.0, 0.0): 'j_basin_road_foot',
    (480.0, 0.0): 'j_warehouse_row_foot', (540.0, 0.0): 'j_fish_dock_corner', (120.0, 57.1): 'j_bend_top', (160.0, 66.5): 'j_north_road_foot',
    (160.0, 150.0): 'j_cut150_west', (160.0, 260.0): 'j_chapel_lane', (160.0, 300.0): 'j_cut300_west', (160.0, 330.0): 'j_ginnel_top',
    (160.0, 350.0): 'j_coldstore_west', (160.0, 400.0): 'j_north_edge', (139.0, 260.0): 'j_ginnel_chapel', (-80.0, 260.0): 'j_west_edge',
    (210.0, 350.0): 'j_basin_road_top', (340.0, 350.0): 'j_cold_yard_mouth', (480.0, 350.0): 'j_warehouse_row_top', (540.0, 350.0): 'j_coldstore_east',
    (540.0, 210.0): 'j_dock_gate', (540.0, 80.0): 'j_harbour_board', (r2(basin_x(150)), 150.0): 'j_cut150_east', (r2(basin_x(255)), 255.0): 'j_basin_top_west',
    (r2(basin_x(300)), 300.0): 'j_cut300_east', (480.0, 255.0): 'j_basin_top_east', (300.0, 255.0): 'j_burned_wh_w', (360.0, 255.0): 'j_burned_wh_e',
    (120.0, 4.5): 'j_quay_street_mouth', (150.0, 8.0): 'j_yards_lane_bend', (150.0, 64.15): 'j_yards_lane_top', (60.0, 4.5): 'j_ginnel_foot',
    (80.0, 30.0): 'j_ginnel_corner', (120.0, 27.0): 'j_gap_east', (77.65, 27.0): 'j_gap_west', (60.0, 0.0): 'j_ginnel_quay', (120.0, 52.5): 'j_quay_street_top',
    (159.0, 4.5): 'j_yards_lane_mouth',
}

def jid(p):
    k = (r2(p[0]), r2(p[1]))
    if k in JUNCTIONS:
        return node(JUNCTIONS[k], k[0], k[1], 'junction')
    nid = 'n_%s_%s' % (str(k[0]).replace('.', 'p').replace('-', 'm'), str(k[1]).replace('.', 'p').replace('-', 'm'))
    return node(nid, k[0], k[1], 'bend')

# Roads become chains of nodes; doors and other points are split into the nearest road edge.
def project(p, a, b):
    ax, ay = a; bx, by = b
    dx, dy = bx - ax, by - ay
    L2 = dx * dx + dy * dy
    t = max(0.0, min(1.0, ((p[0] - ax) * dx + (p[1] - ay) * dy) / L2))
    return (ax + t * dx, ay + t * dy), t

# Foot-only ways meet roads at their end points: add those points to the roads they touch (split points).
SPLITS = {r['id']: [] for r in ROADS}
def add_split(rid, p, nid):
    SPLITS[rid].append((p, nid))

# yards' lane mouth and ginnel foot sit on the quay road's north kerb (y 4.5); link them to the quay road centre line by a 4.5 m crossing
# (the pavement and half the road), so the graphs stay on centre lines.
LINKS = []
def link(a_id, b_id, length=None, foot_only=True, kind='link', **kw):
    a, b = NODES[a_id], NODES[b_id]
    L = length if length is not None else seglen((a['x'], a['y']), (b['x'], b['y']))
    LINKS.append(dict(a=a_id, b=b_id, length_m=r2(L), foot_only=foot_only, kind=kind, **kw))

# door anchoring: each door to the nearest point of its street's centre line (or, for a yard gate / back door, to the nearest foot way)
DOOR_ANCHOR = {}
for d in DOORS:
    best = None
    for r in ROADS:
        if d['street'] and d['kind'] in ('front', 'gate', 'yard_mouth', 'office', 'loading', 'workshop', 'stair', 'garage', 'side', 'yard_gate') and r['id'] != d['street'] and not (d['kind'] == 'yard_gate' and r['foot_only']):
            if d['kind'] != 'garage':
                continue
        if d['kind'] in ('back',):
            continue
        pts = r['pts']
        for i in range(len(pts) - 1):
            q, t = project((d['x'], d['y']), pts[i], pts[i + 1])
            dist = seglen(q, (d['x'], d['y']))
            if best is None or dist < best[0]:
                best = (dist, r['id'], i, q)
    if best is None:
        continue
    dist, rid, i, q = best
    rp = next(r for r in ROADS if r['id'] == rid)['pts']
    vert = [v for v in (rp[i], rp[i + 1]) if seglen(v, q) < 0.01]
    if vert:
        nid = jid(vert[0])
    else:
        nid = node('n_door_' + d['id'], q[0], q[1], 'door_anchor', door=d['id'])
        SPLITS[rid].append((q, nid))
    DOOR_ANCHOR[d['id']] = (nid, dist, rid)

# vaults split their ways
for v in VAULTS:
    r = next(r for r in ROADS if r['id'] == v['way'])
    best = None
    pts = r['pts']
    for i in range(len(pts) - 1):
        q, t = project((v['x'], v['y']), pts[i], pts[i + 1])
        dd = seglen(q, (v['x'], v['y']))
        if best is None or dd < best[0]:
            best = (dd, q)
    if v['id'] == 'vault_mickeys_fence':
        continue   # it lies between Mickey's yard and the lane, handled as a link below
    nid = node('n_' + v['id'], best[1][0], best[1][1], 'vault', vault=v['id'])
    SPLITS[r['id']].append((best[1], nid))

# the ginnel's foot is on the quay road's north kerb: split The Quay below it
SPLITS['quay_road'].append(((60.0, 0.0), jid((60.0, 0.0))))
# junction splits: where one road's end lies on another's line
for r in ROADS:
    for p in (r['pts'][0], r['pts'][-1]):
        for o in ROADS:
            if o is r:
                continue
            pts = o['pts']
            for i in range(len(pts) - 1):
                q, t = project(p, pts[i], pts[i + 1])
                if seglen(q, p) < 0.01 and 0.0 < t < 1.0:
                    SPLITS[o['id']].append((q, jid(q)))

for r in ROADS:
    pts = r['pts']
    chain = []
    for i in range(len(pts) - 1):
        a, b = pts[i], pts[i + 1]
        chain.append((0.0 if i == 0 else None, jid(a), a))
        L = seglen(a, b)
        mids = []
        for (q, nid) in SPLITS[r['id']]:
            qq, t = project(q, a, b)
            if seglen(qq, q) < 0.05 and 0.0 < t < 1.0:
                mids.append((t, nid, q))
        mids.sort()
        for t, nid, q in mids:
            chain.append((t, nid, q))
    chain.append((1.0, jid(pts[-1]), pts[-1]))
    # dedupe consecutive
    seq = []
    for _, nid, q in chain:
        if seq and seq[-1][0] == nid:
            continue
        seq.append((nid, q))
    for k in range(len(seq) - 1):
        (n1, q1), (n2, q2) = seq[k], seq[k + 1]
        EDGES_G.append(dict(a=n1, b=n2, road=r['id'], length_m=r2(seglen(q1, q2)), foot_only=r['foot_only'],
                            vault=(NODES[n1].get('vault') or NODES[n2].get('vault'))))

# doors join the graph by a short link from the door's own node
for d in DOORS:
    did = node('n_' + d['id'], d['x'], d['y'], 'door', door=d['id'])
    if d['id'] in DOOR_ANCHOR:
        nid, dist, rid = DOOR_ANCHOR[d['id']]
        link(did, nid, foot_only=True, kind='door_link')
# back doors join their own yard; a yard joins its gate (if any) or its building's front door through the building
for d in DOORS:
    if d['kind'] != 'back':
        continue
    front = next((f for f in DOORS if f['plot'] == d['plot'] and f['kind'] == 'front'), None)
    if front:
        link('n_' + d['id'], 'n_' + front['id'], foot_only=True, kind='through_building')
    yard = d['plot'] + '_yard'
    gate = next((g for g in DOORS if g['plot'] == yard), None)
    if gate:
        link('n_' + d['id'], 'n_' + gate['id'], foot_only=True, kind='across_yard')
# Mickey's yard: the back door to the quay gate, and over the back fence (vault) into the lane
link('n_d_qs_1_back', 'n_d_mickeys_yard_quay_gate', foot_only=True, kind='across_yard')
lane_node = node('n_vault_mickeys_fence_lane', 150.0, 11.0, 'vault', vault='vault_mickeys_fence')
SPLITS_LATE = (lane_node, (150.0, 11.0))
# split the lane edge containing y 11
for e in list(EDGES_G):
    if e['road'] == 'yards_lane':
        a, b = NODES[e['a']], NODES[e['b']]
        if abs(a['x'] - 150) < 0.01 and abs(b['x'] - 150) < 0.01 and min(a['y'], b['y']) < 11 < max(a['y'], b['y']):
            EDGES_G.remove(e)
            EDGES_G.append(dict(a=e['a'], b=lane_node, road='yards_lane', length_m=r2(abs(a['y'] - 11)), foot_only=True, vault=None))
            EDGES_G.append(dict(a=lane_node, b=e['b'], road='yards_lane', length_m=r2(abs(b['y'] - 11)), foot_only=True, vault=None))
            break
link('n_d_qs_1_back', lane_node, foot_only=True, kind='vault', vault='vault_mickeys_fence', note="across Mickey's yard and over the back fence")
# the two foot ways that start on The Quay's north kerb cross the pavement and half the road to its centre line
link('j_ginnel_foot', 'j_ginnel_quay', foot_only=True, kind='kerb_link')
link('j_yards_lane_mouth', 'j_yards_lane_foot', foot_only=True, kind='kerb_link')
# Iveson's hut sits inside his yard: from the yard gate across the yard
link('n_d_br_2', 'n_d_iveson_hut', foot_only=True, kind='across_yard')
# the chapel hall: by the path past the chapel's west side to Chapel Lane
link('n_d_chapel_hall', 'n_d_cl_1', length=40.0, foot_only=True, kind='path')
# the lot's hut: across the lot to North Road
lot_anchor = node('n_lot_entrance', 160.0, 375.0, 'door_anchor')
# split North Road at y 375
for e in list(EDGES_G):
    if e['road'] == 'north_road':
        a, b = NODES[e['a']], NODES[e['b']]
        if min(a['y'], b['y']) < 375 < max(a['y'], b['y']):
            EDGES_G.remove(e)
            lo, hi = (a, b) if a['y'] < b['y'] else (b, a)
            EDGES_G.append(dict(a=lo['id'], b=lot_anchor, road='north_road', length_m=r2(375 - lo['y']), foot_only=False, vault=None))
            EDGES_G.append(dict(a=lot_anchor, b=hi['id'], road='north_road', length_m=r2(hi['y'] - 375), foot_only=False, vault=None))
            break
link('n_d_lot_hut', lot_anchor, foot_only=False, kind='across_lot')
# the pigeon loft: across the allotments from their gate
link('n_d_pigeon_loft', 'n_d_allot_gate', foot_only=True, kind='path')
# the yards' lane mouth and the ginnel foot are on the quay road's north kerb: the graph already splits The Quay where the lane meets it

GRAPH = dict(
    note='Walking graph on centre lines: every road, lane and link. The driving graph is the same less every edge or link with foot_only true. Lengths in metres. A vault edge or node is passable on foot only by vaulting (Tom 0.8 s, a constable 1.2 s).',
    nodes=sorted(NODES.values(), key=lambda n: n['id']),
    edges=EDGES_G + LINKS,
)

LOOPS = dict(
    chase_loop=dict(roads=['quay_road (540 to 120)', 'quay_street', 'back_parade', 'north_road (to 350)', 'coldstore_road', 'dock_road'],
                    nodes=['j_fish_dock_corner', 'j_quay_street_foot', 'j_bend_top', 'j_north_road_foot', 'j_coldstore_west', 'j_coldstore_east', 'j_fish_dock_corner'],
                    g1_length_m=1528, src='FIT-G1; D-Q2'),
    basin_ring=dict(nodes=['j_basin_road_foot', 'j_basin_top_west', 'j_basin_top_east', 'j_warehouse_row_foot', 'j_basin_road_foot'], g1_length_m=1000,
                    src='FIT-G1 (about 1,000 m)'),
    parade_loop=dict(nodes=['j_north_road_foot', 'j_coldstore_west', 'j_basin_road_top', 'j_basin_road_foot', 'j_quay_street_foot', 'j_bend_top', 'j_north_road_foot'],
                     g1_length_m=910, src='FIT-G1 (about 910 m)'),
    crossing_by_road=dict(from_node='j_landing', to_node='j_north_edge', g1_length_m=548, mode='drive', src='FIT-G1; GD-01'),
    crossing_on_foot=dict(from_node='j_landing', to_node='j_north_edge', g1_length_m=475, mode='walk', src='FIT-G1; GD-01'),
)

MAP = dict(
    file='map.json', version='2026-11-24', frozen_ids=True,
    clock=dict(realSecondsPerGameHour=120),
    frame=dict(units='metres', origin='the ferry landing (0, 0)', x='east', y='north', z='ground level above the quay road', bearing='compass degrees, 0 north, 90 east; a door\'s facing is the way it faces out',
               src='FIT-G1; 4.2.1'),
    sources=['BLUEPRINT-04 FIT-G1, 4.1.1 to 4.1.5, 4.2.1 to 4.2.4, 4.3, 4.4', 'production/lane/design-proof/DEFINITIONS-2026-11-21.md G1, G3, G5, G10',
             'production/specs/vignette-scene.json and terrace-fronts.md (Quay Street as built)', 'production/cloud-week/2d/fascias (the grocer\'s fanlight 11)',
             'production/specs/hook-cast.json (Rita\'s in bay 2, the rank)', 'tools/lane/prototype/project/src/game/tune/way.js (names and landmark wording only)',
             'production/art/atlas-01/data/atlas.json (district landmarks off the map)', 'canon.md; RULINGS.md; the decisions of 24 Nov (pastimes)'],
    footprint=FOOTPRINT,
    roads=ROADS, water=WATER, quay_edges=QUAY_EDGES,
    plots=PLOTS, doors=DOORS,
    name_plates=NAME_PLATES, lamp_columns=LAMPS, vault_places=VAULTS, quay_ladders=LADDERS, bollards=BOLLARDS,
    phone_boxes=PHONE_BOXES, cab_ranks=RANKS, turf_posts=POSTS, rival_bases=RIVAL_BASES, police_points=POLICE_POINTS,
    weapon_places=WEAPON_PLACES, landmarks=LANDMARKS, soft_edges=EDGES, off_map=OFF_MAP,
    street_furniture=STREET_FURNITURE, fishing_spots=FISHING,
    props=dict(rule='at least 5 per 10 m of street (Study 4, 4.1.5); Quay Street 9 per 10 m; foot ways 2 per 10 m', kinds=sorted(set(PROP_KINDS)),
               forbidden=FORBIDDEN_PROPS, seed=19900214, items=PROPS),
    loops=LOOPS, graph=GRAPH,
    chosen_values=CHOSEN, open_points=OPEN,
)

if __name__ == '__main__':
    with open(OUT, 'w') as f:
        json.dump(MAP, f, indent=1)
    print('wrote', OUT, 'roads', len(ROADS), 'plots', len(PLOTS), 'doors', len(DOORS), 'props', len(PROPS), 'nodes', len(NODES), 'edges', len(GRAPH['edges']))
