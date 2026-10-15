#!/usr/bin/env python
"""Writes TARGET.md of the railings family from target.json (its numbers) and the prose below.
    /home/user/.bpyenv/bin/python make_doc.py
Run self_check.py after it: the self-check reads TARGET.md (group E) and the doc quotes the last self-check result from target.json."""
import json, math, os
HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'target.json')))
K = T['kinds']
A1 = K['A1']
A = A1['panel']
Q2 = K['Q2']
HR = T['photo_measurements']['hand_reads']
R3B = T['photo_measurements']['R3B_auto']
CK = T['checks']
CAL = T['calibration']
WS = T['street_fixtures']['walking_strip']
PQ = T['placements']['quay']
SC = T.get('self_check', {}).get('result', 'SELF-CHECK not yet run')
L = []


def w(s=''):
    L.append(s)


def row(*cells):
    w('| ' + ' | '.join(str(c) for c in cells) + ' |')


def tab(head, rows):
    row(*head)
    row(*['---'] * len(head))
    for r in rows:
        row(*r)
    w()


def pts(run):
    return ', '.join('(%.1f, %.1f)' % tuple(p) for p in run['posts_xy_m'])


w('# Quay Street\'s railings: the guard rail, the quay railing and chain, and the boundary railings the street does not have: the target (cloud week 42, 9 October 2026, second version)')
w()
w('**Quay Street\'s one pedestrian guard rail is a 2.0 m panel, 1.0 m high, of rectangular hollow section (posts 50 x 30 x 3 to 1030 under a welded cap plate; a top rail 50 x 30 laid flat with its top at 1000; a bottom rail 40 x 20 x 2.5 at 200; seventeen 12 mm bars with clear gaps of 97.09 and 96.24; four M10 studs welded to the end plates, each with its nut on the post\'s outer face; galvanised grey by default; bounding box 2072 x 50 x 1030), its post axes 0.375 m from the kerb face at x 10.0 to 12.0 leaving 1.575 m of footway (1.39 m under the fish market\'s awning at a 2.0 m head); the quay kit has no railing, so a tube railing on 76.1 mm posts (top rail 60.3 x 3.6, 3.0 m bays; two rails or a rail and a plain 13 mm chain sagging 200) is proposed for the jetty\'s public end only: two bays of the basin edge, the tip and a three-post return closing the corner against the parapet (12 posts, 11 bays, 31.4 m, every post at least 10.6 m from the kit\'s mooring rings); the street has no area railing, chapel railing or yard gate; no photograph of a guard rail or a tube railing was reachable, so both are Judgement (and both sides of A1\'s form are judgement), backed by three photographed bar railings (bars every 76.6, 95.3 and 120) and one photographed chain bay.**')
w()
w('The target for the family "railings on Quay Street and its quay", written from Poly Haven\'s CC0 London photographs (all 2019) and the repository\'s own numbers. Everything is millimetres unless a line says otherwise (placements are metres in the street\'s or the south-quay kit\'s frame); the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, sections, plans, the bolt section, the walking strip, a sample of each reserve railing, the two placement plans) from target.json alone; `self_check.py` tests them against their own sources (last result: **' + SC + '**). `make_target.py`, `measure.py`, `calibrate.py`, `make_previews.py`, `make_doc.py`, `frames.py`, `awning_lib.py` and `rail_lib.py` re-make the files from the hand-read numbers and the panoramas.')
w()
w('**What is photographed and what is not, in one breath.** Photographed (Photo, +-6 % in size, each at its own camera height): R3B, a tall cast-iron park railing on a brick plinth (bars every 76.6, rails at 434, 1018 and 1948, spire heads to 2211, a hinge post to 2314); R3A, an area railing on a two-stage dwarf wall (bars every 120, rails at 883, 1509 and 1730); R3D, a low dark-green railing on a garden wall (bars every 95.3, rails at 698 and 1114); and LHB, one bay of the marina chain posts, whose lug heights (807 and 409) and chain sag (217 to 242) test the bollards target. **Not photographed, Judgement:** the guard rail A1 and the quay tube railing Q2, every number except the scene\'s own and the bollards target\'s chain.')
w()

# ---------------------------------------------------------------------------------------------------------------- 0
w('## 0. What changed after the fresh review (the second and last try)')
w()
w('The first version failed its fresh review with 2 faults and 9 narrow points (TARGET-REVIEW.md, untouched). One line each; the sections that follow carry the numbers.')
w()
tab(['item', 'what was done', 'where'], [
    ['**Fault 1: the guard rail\'s form**', 'A1 is now the review\'s form and numbers: posts RHS 50 x 30 x 3.0 to z 1030 with a welded 3 mm cap plate; top rail RHS 50 x 30 laid flat, top 1000, axis 985; bottom rail RHS 40 x 20 x 2.5 at 200; the 17 bars unchanged (gaps 97.09 and 96.24); a 6 mm end plate at each of the four rail ends with an M10 stud welded to it (the first review\'s bolts, made studs after the re-review: see 0A), the nut (17 AF, 8 high, 3 mm of thread beyond) on the post\'s outer face at x +-1025; bounding box 2072 x 50 x 1030; walking-clear and bounding-box checks recomputed; new section checks (A1_post_section, A1_post_top, A1_top_rail_section, A1_bottom_rail_section, A1_bolts). **I could not show from any source that the review is wrong**: no photograph of a guard rail was reached on either side, so both forms are judgement; the review\'s form is also what the first search summary\'s lead ("posts 50 x 30 mm") describes, which the first version set aside without saying why. The round-tube form is kept only as a recorded alternative (target.json, `alternative_recorded`) because it can be the right one if the PC photographs show it. The review\'s line is in section 13, first item: two dated (1985 to 1995) photographs from the PC before the build is gated.', '6.1, 9, 11, 13'],
    ['**Fault 2: the jetty railing**', 'Q2 amended as the review wrote it: the basin run cut to two bays at the tip, the tip run kept, a three-post return along x -128.4 closing the corner against the parapet: 12 posts, 11 bays, 31.4 m. New checks Q2_clear_of_rings (every post and rail at least 4.0 m from the kit\'s mooring rings; the nearest post is 10.6 m), Q2_corner_closed, Q2_return_posts; Q2_basin_posts and Q2_tip_posts re-stated. The two rings (read live from the kit) are drawn on the jetty plan.', '7, 11, 14'],
    ['1. Camera heights', 'Stated at each object\'s own ground: R3B 0.945 +-0.02, R3A 1.02 +-0.03, R3D 1.15 +-0.02, LHB 1.13 +-0.03; section 4\'s table says which anchor is at whose ground; every length read at the first version\'s pooled height is multiplied by 0.974, 1.052, 1.027 and 1.009; every elevation was re-made at the new heights; the brick courses of R3D and R3A read 75 in them.', '4'],
    ['2. R3B\'s bar heads', 'The review\'s profile, scaled to 0.945: a turned knop about 90 across (89.6) at 2044 and a ring about 44 across above it, a spire to 2211 +-15 (was "a vase 60 across at 2128", tip 2300); the knop is one value, 2044 +-8, checked by the re-review\'s 16k reading (see 0A).', '6.3, 0A'],
    ['3. R3A, left run only', 'The numbers and the pattern text are the left run\'s (s below 1577 on the new preview = 1500 x 1.052); the run beyond the cast post is another pattern and is not measured; group C fits only s below that.', '6.3'],
    ['4. Ground detail', 'The 20 mm bitumen ring is replaced by a ragged dark tarmac reinstatement patch, about 250 x 250 round each post (sRGB (45, 43, 41), roughness 0.85, flush with the flags to +-3, one straight flag edge, a 5 to 15 mm grit joint), outline given as 24 points; A1_foot_ring becomes A1_foot_patch [250, 250] +-60.', '6.1'],
    ['5. Paint default', 'Agreed with the review: galvanised grey (118, 120, 122), roughness 0.55, metal 1, streaked, with dark run-marks below the bolts and white zinc bloom at the feet, is the default at 55 %; black scuffed 30 %; black chipped 15 %. Reason: panels of the 1976 pattern were galvanised steel, painting was the owner\'s option, and the only blacks I photographed are cast and wrought iron, not galvanised steel.', '6.1, 8, 10'],
    ['6. Q2 bay', 'Option one: 3.0 m bays kept (the bollards target\'s spacing and the review\'s post lists) with the top rail 60.3 x 3.6 (Q2_top_rail_od 60.3 +-3). The 2.0 m option would have changed every post list.', '6.2'],
    ['7. Walking strip', 'A1_walking_clear is now the least free width between the rail\'s rear face and any fixed projection for a body from 0 to 2.0 m high in x 9.5 to 12.5: awning_02.glb was read (a sloping body, not the review\'s straight line): 1.575 m at the ground, **1.39 m at a 2.0 m head** (the review estimated about 1.0; both pass 0.68); recomputed live by the self-check every 0.1 m.', '7'],
    ['8. Ears', 'Ears only on the sides that face a Q2b bay: 18 in all (two per chain bay, nine chain bays); one on the Q2a/Q2b corner post, none toward a Q2a bay, one on the return\'s end post, two on the tip/return corner post.', '6.2, 7'],
    ['9. Set-back', 'Left as the scene has it (0.25 m behind the kerb: the road face is 0.35 m from the kerb face); the remembered 1980s rule of about 0.45 m is added to section 13 next to LTN 2/09.', '7, 13'],
])

w('## 0A. Narrow points applied after the re-review')
w()
w('The second review passed the target (0 faults, 4 narrow points). All four are applied as written; one line each.')
w()
tab(['point', 'what was done'], [
    ['1. The bolt', '**Studs welded to the end plates replace the four bolts**: M10 studs welded to the outer face of each 6 mm end plate (x +-975, on the rail axis, a 3 mm fillet round the root), 61 long, through an 11 mm hole across the post to x +-1036, with the same nut (17 AF x 8, face at +-1025) and 3 mm of thread beyond; `head` and the `head_x` entries are deleted; A1_bolts reads "four M10 studs welded to the end plates, each nut on the post\'s outer face"; section 12 and 6.1 say studs. Everything visible, A1_bolt_heights, A1_bbox and the drawings\' outline are unchanged (the stud section is redrawn).'],
    ['2. A1_bbox and the patches', 'The tarmac patches are **exported as a separate mesh `A1_ground_patch` (z 0 +-3)** and excluded from the overall-size check: A1_bbox\'s text and kinds.A1.bbox.note say "excluding the two ground patches, exported as a separate mesh `A1_ground_patch` (z 0 +-3)"; A1_foot_patch checks that mesh; the patch data carry `mesh` and `in_bbox: false`.'],
    ['3. R3B\'s knop', '**One value: 2044 +-8.** The re-review\'s reading on the 16k HDR at 0.945 (12 tall bars, rows every 4 mm) centres the widest rows (82 to 86 across, z 2034 to 2058) on z 2046, and the ring above (45 to 49 across) at z 2082 to 2106: that is the check of the knop, stored in `knop.check_16k`. The sentence in section 12 that sent a build to the 1 mm head close is deleted (that close, made from the 8k image, reads the knop higher and is not used for z). **The head profile now ends at the stated tip**, (0, 2211.43), equal to tall_tip_z (the 5 mm gap came from the review\'s first list: its last point 2275 against a stated tip of 2270).'],
    ['4. Numbers quoted one way', '**R3D\'s bar pitch is 95.3 (+-3, the line fit of the ten read centres) everywhere**: the summary line, section 3 (layer 2), the photographs-win infill row, section 6.3 and the previews table, and the label of `target-a1-beside-photographed-bars.jpg` (redrawn); "97" survives only where the review\'s scaling is named (94.5 x 1.027 = 97.0, 1.7 higher, inside the +-3). **LHB\'s upper lug is 807 (and the lower 409) everywhere**: the handover said 806. Likewise the marina chain\'s sag is quoted 217 and 242 (mean 230 +-35, over a 2865 span) at 1.13 m throughout, in place of the first version\'s 215 and 240 over 2840.'],
])
w('**Note, no change** (the re-review): the return\'s end post leaves a clear slot of about 0.24 m to the parapet\'s corner, which is shut to the game\'s 0.68 m walker, so the corner counts as closed. An integrator who wants a tighter close would move the end post to (-128.5, -22.9): the slot becomes about 0.10 m and Q2_corner_closed would read [0.1, 0.1]. Not done.')
w()

# ---------------------------------------------------------------------------------------------------------------- 1
w('## 1. What the street has, what it needs, and where there is nothing to draw')
w()
w('The scene (SCENE-SLOTS.md, read 9 October; vignette-scene.json E8) places one guard rail: **a 2.0 m panel, 1.0 high, posts 0.05, rails 0.04, five infill bars of 0.025, east side, x 10.0 to 12.0, 0.25 m back from the kerb**, beside the gully at x 12.0. It was three panels (to x 16.0) until 29 September, when the AI tester found the east footway walled: the crates of the fish market left 0.65 m between rail and frontage, less than a walking person\'s 0.68. The held `trunk_protection_railing` is a tree-pit guard and is not this object (the bill of materials says so). The vignette-feet file puts both posts at z 3.375 and the pieces list shows the stand-in\'s lower rail 0.45 above its foot.')
w()
w('The asset plan names two linear kits for this family: "2 m guard-rail panel (posts, rails, infill)" and "two-rail tube railing with chain", one kit each ("Guard railing; quay railing with chain; fences": 1 kit; 1 kit), 1 to 3 panels on the street and a quay railing "along the quay".')
w()
w('**(a) The kerbside guard rail** is kind A1 below. **(b) The quay.** The south-quay kit (tools/art-recipes/south-quay, read 9 October, built live by the self-check) has a granite cope along every quay edge, ten cast-iron bell bollards, **mooring rings on the north quay\'s face and on the jetty\'s basin face (x -110.05, y -62 and -32)**, a ladder, a stone parapet on the jetty\'s seaward side and walled yards with boarded gates; it has **no railing on any quay edge**, and a search of its pieces for "rail" finds none. The bollards target (K5) adds four chain posts and two plain chains about the north quay\'s ladder (x -69.5, y -40.5 to -31.5). An earlier session read a 1989 photograph of the River Hull (the atlas\'s R08, Flickr, unreachable here) that shows a "chain-edged quay": chain at a working quay\'s edge is period-attested, a tube railing is not. So the working north and east quays and the jetty\'s berth stay as they are, and **kind Q2, a tube railing with 3.0 m bays, goes only where the public walks out: the last two bays of the jetty\'s basin edge, its tip before the harbour light, and a return that closes the seaward corner** (section 7). This is Judgement and new to the kit; the integrator may refuse it and nothing else in this target depends on it.')
w()
w('**(c) Area and boundary railings: the street has no such place, and none is drawn for it.** Checked in vignette-scene.json (blocks), vignette-pieces.json (641 pieces), terrace-fronts.md, terrace-front.py, the atlas and the hook-cast file:')
w()
tab(['place', 'what the data says', 'so'], [
    ['the east parade, six bays and the chandler\'s (x 3 to 46)', 'shopfronts on the building line: the frontage line is z 5.125 (3.0 kerb face + 0.125 + 2.0), the stallriser stands 0.15 and the pilasters 0.10 proud; no forecourt, area or dwarf wall; one doorstep stone', 'no railing'],
    ['the west blocks (x 3 to 21, 24 to 33)', 'plain terraces and shops on the same line (cottages in the drawn street); no front gardens in the data', 'no railing'],
    ['the yard mouth (x 21.0 to 24.0, west)', 'a 3.0 m gap in the data with a dropped kerb; the bollards target\'s two K1 posts guard its corners; the scene stands a held crowd-control barrier across it (E11, x 22.5, z -4.85); no gate is placed', 'no gate: whether the yard is ever gated is the town session\'s call'],
    ['the south-quay kit\'s walled yards (junction corners)', 'brick walls 1.40 high with piers every 4.5 m and boarded leaves (the kit\'s own)', 'no railing'],
    ['a church or chapel', 'Father Walsh\'s chapel is at x 100 in hook-cast.json, past the street\'s bend; Fairview Chapel is in another district', 'not on the street'],
    ['the north approach (x > 48)', 'knee-high garden-wall boxes in the backdrop (terrace-front.py), not game objects', 'not drawn'],
])
w('The asset plan\'s fences kit (chain-link and palisade, along the yard) is a different family\'s; Poly Haven\'s `modular_chainlink_fence` (CC0) exists and Urban Street 02\'s steel palisade is a 2000s form, both left to it. Because the brief asks for photographs to be used where they are reached, three photographed railings are kept in the target as **reserve kinds R3B, R3A and R3D (placed: false)**: if the town session gates the yard or the story gets a chapel, the numbers are here. They also serve as the only photographic evidence for the bar proportions of A1.')
w()

# ---------------------------------------------------------------------------------------------------------------- 2
w('## 2. Sources')
w()
w('All photographs are Poly Haven\'s, CC0 (licence read at https://polyhaven.com/license on 9 October 2026: "Our assets are all licensed as CC0"), author Andreas Mischok, used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud\'s network refused every other photograph site (list below). **No photograph from 1975 to 2000 was reached; every photograph is from 2019**, and for each the table says what it shows and whether it is the period object or a replacement.')
w()
tab(['id', 'URL', 'date read', 'author, licence', 'date taken', 'what it shows', 'used', 'period object or replacement'],
    [[s['id'], s['url'], s['read'], s['author'] + ', ' + s['licence'], s['taken'], s['shows'], s['used'], s['period']] for s in T['sources']])
w('**Looked at and left out:** ' + '; '.join(T['looked_at_and_left_out']) + '.')
w()
w('**Unreached** (refused with 403 or not resolvable on 9 October; a page that refused is not evidence and nothing was taken from any of them): ' + ', '.join(T['unreached']) + '.')
w()
w('**What the search summaries gave (leads only, no number taken as a measurement).** BS 3049:1976 "Pedestrian guard rails (metal)" existed in 1990 (it was withdrawn on 15 November 1995 and BS 7818 replaced it); present-day catalogue panels use 12 mm bars at 110 to 112 centres (a 100 mm sphere may not pass), **posts 50 x 30 mm** and a height of 1100; Kent dates pedestrian guardrail from the 1930s; a 1983 London study and a 1988 article say the conventional rail hid the road and that a see-through type did better; working fish-quay berths in a present-day harbour audit are left unfenced; at Bideford the quay has cast-iron posts with tubular bars and chains from 1899 to 1905. These lead the Judgement numbers below and are named where they do. The review\'s own knowledge of 1970s and 1980s street and dock ironwork is marked (Judgement, reviewer) in its file; it too was not read from a source and awaits the PC.')
w()

# ---------------------------------------------------------------------------------------------------------------- 3
w('## 3. No guard rail was photographed: what the target rests on instead')
w()
w('Fifteen of Poly Haven\'s British panoramas (every one in Greater London and Cambridge; the two Epping Forest ones and St Fagans\' interior were not opened) were looked at in six to eight rectilinear views each; the review scanned urban_street_03 and 04 again. **None shows a kerbside pedestrian guard rail, a tube railing on a quay or a bar railing of the 1976 pattern.** What they show is cast and wrought bar railing (Bethnal Green, Urban Street 01), a steel palisade (Urban Street 02, 2000s, left out), stainless dock-edge balustrades (Canary Wharf, Adams Place Bridge, 2000s, a modern-only form, left out), a hoop-top railing and bolted chain posts with chain (Bethnal Green, Limehouse). Wikimedia Commons, Geograph, Flickr and the Historic England Archive, which hold 1980s photographs of exactly this object, refused the cloud.')
w()
w('So A1 and Q2 are built in three layers, each marked where it is used:')
w()
w('1. **Read**: the scene\'s numbers (2.0 m panel, 1.0 m high, post 0.05, rail 0.04, x 10.0 and 12.0, z 3.375), the frontage and kerb numbers, the bollards target\'s chain and 3.0 m bays, the kit\'s rings and cope.')
w('2. **Photo, by analogy**: all three photographed bar railings have their bars at 76.6, 95.3 or 120 centres (clear gaps 60 to 105): none has the scene\'s 333 mm gaps (five bars in 2.0 m). They are black (22 to 24 grey levels) except one council green. Their feet end in a ball or sit on a rail, their bars are round and plain. These set the bar rhythm and the black.')
w('3. **Judgement**: **the form of A1 (RHS, bolted: the review\'s; the first version\'s round tube was equally judgement)**, tube sizes of Q2 (76.1 posts, 60.3 and 42.4 rails), the lower rail\'s height, the cap, the welds, the ground detail, the finish, the wear, and the places on the jetty. Each is flagged in the part tables.')
w()
w('**Both sides are judgement here, and I say so plainly.** The first version chose round tube because the scene\'s stand-in was cylinders; the review chose rectangular hollow section and bolted ends from its knowledge of 1970s British guard rails. Neither side holds a photograph or a standard, and the one lead in hand ("posts 50 x 30 mm") is the review\'s. The target takes the review\'s form; the round form stays in target.json as `alternative_recorded` and the PC photographs (section 13) decide.')
w()
w('Where the photographs and the scene differ the photographs win, element by element (section 9). The scene\'s five 25 mm bars are replaced by seventeen 12 mm bars, because a bar railing with 308 mm gaps is not seen in any reached photograph.')
w()

# ---------------------------------------------------------------------------------------------------------------- 4
w('## 4. How the photographs were measured, and why the camera height is not 1.6 m')
w()
w('Each panorama (8192 x 4096) is re-projected with numpy to a flat elevation of one vertical plane through the foot line of the object (`rail_lib.py`: a ground point from the foot\'s pixel and the camera height, a plane through two of them, 1 mm to 4 mm a pixel; the native resolution is 3 to 5 mm at 5 to 7 m, so every picture is soft). **Every length then scales with the camera height at the ground the object stands on**, which the panoramas do not give. Each height is measured by the horizon method of the bollards and kerbs targets (`calibrate.py`: in a levelled panorama the horizon is the middle row; brick courses of a wall are evenly spaced in tan(angle below it), so the camera height above the wall\'s foot = 75 mm x tan(angle of the foot) / (course pitch in tan units)), on brick walls and piers that stand on the same ground as the railings.')
w()
w('**Second version: one height per object, at that object\'s own ground.** The first version pooled one height for each panorama (0.97 for Bethnal Green, 1.12 for Urban Street 01 and for Limehouse); the review, re-measuring at 16k, showed that two of the three pooled heights mixed different grounds. The anchors, all recomputed from their stored rows by the self-check:')
w()
rows = []
for a in CAL['horizon_anchors']:
    H = a['image_rows']
    h = a['gauge_mm'] * math.tan((a['foot_row'] - H / 2) * math.pi / H) / a['pitch_tan'] / 1000 + a['step_m']
    rows.append([a['pano'], a['id'], a['what'], 'cols %d-%d, rows %d-%d, foot row %d, pitch %.5f' % (a['cols'][0], a['cols'][1], a['rows'][0], a['rows'][1], a['foot_row'], a['pitch_tan']), '%.3f' % h])
tab(['panorama', 'anchor', 'what', 'raw rows', 'camera height above the foot (m)'], rows)
w('**Which anchor is at whose ground**, and the factor every first-version length was multiplied by (new height / first version\'s):')
w()
rows = []
for k, O in CAL['objects'].items():
    used = ', '.join(O['anchors'] + [q['id'] for q in O.get('quoted', [])]) or '-'
    other = []
    for e in O['excluded']:
        other.append('set aside: %s (%s)' % (e['id'], e['why']))
    if O['corroboration']:
        other.append('corroboration only, a different ground: ' + ', '.join(O['corroboration']))
    rows.append([k, O['pano'], '**%.3f +-%.2f**' % (O['h_cam'], O['err']), O['ground'], used, '; '.join(other) or '-', '%.3f (first version %.2f, x %.4f)' % (O['h_cam'], O['first_version_h'], O['scale_from_first_version'])])
tab(['object', 'panorama', 'camera height (m)', 'its own ground', 'anchors at that ground', 'others', 'scale'], rows)
for k, O in CAL['objects'].items():
    w('* **%s**: %s.' % (k, O['why']))
w()
w('The review\'s 16k remeasurements agree: R3B 0.942 (gate pier, 22 courses) and 0.941 (rectified); R3A 1.017 (its own wall); R3D 1.148 (the garden wall, four column bands 1.13 to 1.16); LHB paving 1.12 to 1.15, the building wall\'s foot 1.09. **I checked the result on the new elevations**: the brick courses of R3D\'s garden wall read 75 mm apart in the 3 mm elevation at 1.15 (autocorrelation 0.75), those of R3A\'s dwarf wall 75 (weakly, an oblique face) at 1.02, and R3B\'s bars 76.57 (three inches 76.2: 0.5 %) at 0.945; at the first version\'s heights they would have read 71.4 (R3A) and 73 (R3D). `self_check.py` recomputes every anchor and fails if the mean at an object\'s ground is farther from its stated height than the stated error (group B).')
w()
w('Results: **no panorama was taken at 1.6 m**. **Every number below is +-6 % in absolute size** (R3A +-8 %); counts, pitches\' ratios and the proportions are exact to the pixel. Where the three families overlap they agree: R3A 1.02 equals the bollards target\'s Bethnal Green 1.02 +-0.07, R3B at its gate pier\'s ground is 0.075 under it (0.005 outside that band; the planter wall both targets use reads 0.963, inside it); Limehouse 1.13 against its 1.17 +-0.06; the K5 post reads 1096 here and 1135 there, the same 3.4 % as the camera heights (0.966). **Nothing placed moves**: A1 and Q2 are not measured from a photograph; the changes are inside the stated errors.')
w()
w('Other methods: `measure.py` finds the bars of R3B as the dark minima of the column profile of a 1 mm elevation between the rails and fits their pitch (26 bars, %.2f mm, rms residual %.1f mm); its rails as dark rows between the bars; heads, posts, wall tops and rails of the other three were read by eye on gridded 1 mm and 2 mm elevations at the first version\'s heights and multiplied by the factors above (`photo_measurements.json` keeps both sets, each with its error and how). The self-check\'s group C re-detects bars, rails, wall tops, tips, knops and brick courses on the new previews and compares them with the drawing (a scale fitted on one dimension, the bar pitch).' % (R3B['bar_pitch_mm'], R3B['bar_pitch_resid_rms_mm']))
w()
w('**Tell the kerbs-and-covers and bollards writers** (already said in their targets): the panoramas are 0.945 to 1.15 m above their ground; sizes taken at 1.6 m are 40 to 70 % too large.')
w()

# ---------------------------------------------------------------------------------------------------------------- 5 frames
w('## 5. Frame, pivot, glb')
w()
w('* **A1**: local x along the panel (0 at its middle), y across (0 on the rail line, + toward the carriageway), z up from the flag top at the posts. **Pivot: the middle of the panel on the ground.** In the street recipe\'s frame the axis is z 3.375 and the posts stand at x 10.0 and 12.0 (placements, section 7).')
w('* **Q2**: local x along the run (0 at the middle of a bay), y across (+ toward the water), z up from the apron at the post foot; pivot at the middle of the bay on the ground. Placed in the south-quay kit\'s frame (x along Quay Street, y across, east +; the apron and copes at +0.05).')
w('* **glb**: metres, z up, scale 1; one mesh per piece kind and material (posts, rails, bars, caps, welds, end plates, studs and nuts, base plates and nuts, chain links and eyes as separate meshes of the same piece); **no text, no decal with lettering, no number, no crest, no maker\'s mark** on any mesh or texture.')
w('* The elevation pictures of the photographs are rectified to the plane 110 mm behind the front face of a wall (where a railing stands on a wall), so a feature at the wall\'s front edge is 13 mm (R3B) lower than its true height; the notes say where this matters.')
w()

# ---------------------------------------------------------------------------------------------------------------- 6
w('## 6. The target, kind by kind')
w()
w('Every number carries its kind: **Read** (printed in the repository), **Photo** (measured on a photograph: method in section 4, +-6 % in size), **Derived**, **Judgement** (a trade or period guess, said so).')
w()
w('### 6.1 A1: the kerbside pedestrian guard rail (`guard_rail_panel`, the scene\'s E8). Judgement (the review\'s form), with Read numbers from the scene')
w()
P_ = A
b0 = P_['bolts']
tab(['part', 'dimensions (mm)', 'position', 'kind and basis'], [
    ['post (two)', '**RHS 50 x 30 x 3.0**, the 50 face along the run (x), the 30 across (y); outer corner radius 4.5, inner 1.5; top at **z 1030** (30 proud of the top rail); below ground 400, not modelled', 'axes at x -1000 and +1000, y 0; the faces toward the panel at x +-975', 'Judgement (the review; the lead "posts 50 x 30"); the scene\'s 0.05 is the 50; height Read'],
    ['post cap (two)', 'a welded **3 mm flat cap plate**, the post\'s own outline, flush with the four sides, edges broken R1; a 1 mm bead ground flush', 'z 1027 to 1030', 'Judgement'],
    ['top rail', '**RHS 50 x 30 x 3.0 laid flat**: 50 across (y), 30 high (z); outer R4.5; length 1950 between the post faces; a **6 mm end plate** (the rail\'s own outline) welded to each end', 'axis z 985, **top z 1000**, underside 970; x -975 to +975', 'Judgement (the review); top Read (the scene\'s 1.0)'],
    ['bottom rail', '**RHS 40 x 20 x 2.5 laid flat**: 40 across, 20 high; outer R3.75; same length and end plates', '**axis z 200** (190 to 210)', 'Judgement (the review); the stand-in\'s lower rail at 450 had no photograph'],
    ['infill (17 bars)', 'solid mild-steel round bar Ø12, vertical, **from z 210 (the bottom rail\'s top) to z 970 (the top rail\'s underside)**; a 2 mm fillet weld at each end (68 beads)', 'x = %s ... %s, **pitch %.2f**, clear gap **%.2f** between bars and **%.2f** from a bar to a post face; both at most 100' % (P_['infill']['x'][0], P_['infill']['x'][-1], P_['infill']['pitch'], P_['infill']['clear_gap_between_bars'], P_['infill']['clear_gap_bar_to_post_face']), 'Judgement: the gap rule (at most 100: a 100 mm sphere may not pass) from the search-summary lead; the pitch is inside the photographed 76.6 to 120'],
    ['studs (four)', '**M10 studs, 61 long**, welded to the outer face of each 6 mm end plate (x +-975) on the rail axis with a 3 mm fillet round the root, through an 11 mm hole across the post (both 3 mm walls) to x +-1036; **hex nut 17 AF x 8 on the post\'s outer face** and 3 mm of thread beyond it; the bright steel painted over (the black variants) and rust-streaked below the nut', 'at z 985 and z 200, y 0, on each post: stud x +-975 to +-1036, nut faces at x +-1025 to +-1033, thread end +-1036', 'Judgement (the review: a struck panel can be unbolted and replaced; the re-review: studs, since a bolt head could not be fitted inside the rail end)'],
])
w('* **Overall**: **2072 x 50 x 1030** (x +-1036 including the nuts and 3 mm of thread; y +-25 the top rail laid flat; z 0 to 1030; **excluding the two ground patches, exported as a separate mesh `A1_ground_patch` (z 0 +-3)**). **Panel length**: 2000 between post axes (Read). **How panels join**: a second panel (none on this street) would bolt to the same post\'s other face with its own studs and nuts; the bars are not offset. **How it ends**: at its posts: an end post is the same post with the same cap; no return, no end rail, no stay; the one panel ends at x 12.0 beside the gully (its end post stands 0.025 over that line).')
w('* **How it meets the ground**: the posts are concreted into the footway; the flag is cut for each and the cut made good with **a ragged dark tarmac reinstatement patch about 250 x 250** round the post (sRGB (45, 43, 41), roughness 0.85), its edges ragged +-20, flush with the flags to +-3, **one edge a straight cut flag edge** (the footway side), a 5 to 15 mm dark grit joint where it meets the flags; the outline is 24 points in target.json (`ground.patch.outline_xy`, local x, y). No collar plate, no base plate. The posts stand on the flag top; the builder reads the ground under them (the scene\'s foot level is y 0.05625; the kerbs target\'s flag level gives y 0.040).')
w('* **Edges**: post and rail corners rounded (R4.5 on the 3.0 wall, R3.75 on the 2.5 wall); the cap\'s edges broken R1; bar ends hidden in 2 mm welds. **Seams**: the RHS\'s longitudinal weld seam shows as a 0.4 mm ridge on the narrow face turned to the footway (Judgement). **Marks**: none: no plate, number, stencil, crest or maker\'s name.')
w('* **Finish: galvanised, weathered dull grey, streaked, sRGB (118, 120, 122), roughness 0.55, metal 1, is the default** (55 % of the conditions): dark run-marks (60, 56, 52) 40 to 150 long below the bolts, white zinc bloom (200, 200, 196) in patches to 150 high at the feet, a rust streak (110, 60, 32) from each nut, the road face grimed brown-grey by tyre spray to about 500. **Why I agree with the review**: panels of the 1976 pattern were galvanised steel and painting was the owner\'s option, so weathered zinc is at least as likely as black for a provincial highway authority in 1990; and the only blacks I photographed are cast and wrought iron, not galvanised steel, so the photographs do not argue for black. The black remains at 45 % (black over galvanising, sRGB (24, 24, 26), roughness 0.42, the same black as the bollards target\'s posts and the two blacks measured on the panoramas: R3A (22, 21, 21) and the K5 post (23, 24, 28)). No bands, no reflective sleeves, no stripes.')
w('* **Wear and damage** (Judgement, patterned on what the photographs show of ironwork: flaking at the collars, rust at the bar feet and the foot of the post, dirt on the plinth): ' + '; '.join(A1['wear']) + '.')
w()
w('**Seeds per instance**: lean 0 to 1 degree toward the carriageway; bent bars 0 to 2 (5 to 15 mm out at z 300 to 600); rust at the feet 0 to 1; dirt height 300 to 600; bright-rubbed patches on the top rail 0 to 3; sticker remnants 0 to 2; chips 0 to 10; patch edge +-20.')
w()
w('**The first version\'s round-tube form, recorded and not to be built**: ' + A1['alternative_recorded']['what'] + ' Why set aside: ' + A1['alternative_recorded']['why_set_aside'])
w()
w('**The studs.** The first version\'s four bolts had their 17 AF heads inside the hollow rail ends, which cannot be fitted (the head does not go inside the 35 x 15 hollow of the bottom rail, and a head inside a closed tube could not be held while the nut is tightened). The re-review replaced them by M10 studs welded to the outer face of each end plate, 61 long, with the same nut and thread on the post\'s outer face: everything visible is unchanged. A build models the end plate, the nut and the 3 mm of thread; the stud inside the post and the root fillet are hidden and may be modelled as one cylinder and a weld bead on the plate face (section 12). The drawings `A1_bolt_section` and `A1_elevation` show it.')
w()

w('### 6.2 Q2: the quay tube railing, two models (`quay_tube_railing`). Judgement; the chain is the bollards target\'s and Photo for its sag')
w()
P_ = Q2
tab(['part', 'dimensions (mm)', 'position', 'kind and basis'], [
    ['post', 'round steel tube OD %s, wall %s, %s above the apron; a pressed domed cap OD 80, rise 14, welded; a 5 mm fillet weld at the foot' % (P_['post']['od'], P_['post']['wall'], P_['post']['height']), 'bay ends at x +-1500', 'Judgement: 3 inch nominal bore; a quay post is heavier than the street\'s'],
    ['base plate', '200 x 200 x 12, four Ø18 holes on a 150 square (25 from each edge), four M16 studs with hex nuts 24 across flats and 13 high, the studs 10 proud of the nuts; 25 mm grout bed and a 20 mm fillet round the plate', 'z 0 to 12', 'Judgement'],
    ['top rail', '**tube OD 60.3, wall 3.6** (2 inch nominal bore), saddle-welded; length %.2f' % (2 * P_['top_rail']['x'][1]), 'axis z 1000 (top 1030.15)', 'Judgement: the review\'s option for 3.0 m bays (48.3 would be spindly); 2.0 m bays with a 48.3 rail was its other'],
    ['low rail (Q2a)', 'tube OD 42.4, wall 2.6, same length', 'axis z 500', 'Judgement'],
    ['chain (Q2b, in place of the low rail)', 'plain short link, bar 13, inner 39 x 18, outer 65 x 44, pitch 39, **no spikes**; 74 links between two eyes (32 on the 1.4 m end bay); alternate links edge-on', 'a catenary from eye to eye, z 500 at the eyes, **sag 200** (lowest z 300; 87 on the 1.4 m bay, the same 7 %%); arc %s' % Q2['chain']['arc_length'], 'Read: the bollards target\'s chain; sag Photo (LHB 217 to 242 for the marina\'s) and not the bollards target\'s 150'],
    ['eye ears (Q2b)', 'flat-bar ears 40 wide x 70 high x 8 thick, a Ø24 hole centred 45 from the post surface; **only on the sides that face a Q2b bay**', 'z 500, on the rail line facing the bay', 'Judgement (the bollards target\'s D-lug is 55 x 40 x 18 with the same Ø24 hole)'],
])
w('* **Bay**: 3000 post axis to post axis (Read: the bollards target\'s spacing); the return\'s end bay 1400. **Ends**: a run ends at a post of the same kind; at a corner two runs share one post with the rails mitred to it. **Ears** (the review\'s point 8): none on a post\'s side that faces a Q2a bay or no bay; one on the corner post (-110.4, -15.4) (it faces the Q2b bay of the tip only), two on the tip/return corner post (-128.4, -15.4), one on the return\'s end post (-128.4, -22.8); 18 ears in all, two for each of the nine chain bays. **Edges**: saddle cuts, fillet welds, cap rim R3, plate edges R2. **Marks**: none.')
w('* **Paint**: black satin over galvanising, sRGB (24, 24, 26), roughness 0.55, metal 0: the K5 post\'s and the K6 bollards\'. Nuts and studs bright steel (150, 150, 152) with dull rust at the threads; the chain black, rubbed bright where the links touch.')
w('* **Wear**: ' + '; '.join(Q2['wear']) + '.')
w()
w('**The chain against the photograph (LHB), at 1.13 m.** One bay of the marina\'s chain posts, rectified to the plane through two post axes (span 2865, the bollards target\'s 3.06 read between two posts): the lugs are at z 807 and 409 (the bollards target: 840 and 420, 4 % higher at its 1.17 m camera), the upper swag hangs to z 590 (sag 217), the lower to 166 (sag 242), the post is 1096 high (1135 there). The target\'s sag of 200 is between the bollards target\'s 150 and the photograph\'s 230 +-35; **the bollards writer should raise K5\'s to 200**. The photographed chain is the marina\'s ornamental one with spikes on every second link; only its sag and the lugs\' heights are used.')
w()

w('### 6.3 The reserve kinds, photographed and not placed (R3B, R3A, R3D)')
w()
w('These stand for the railings a chapel, a yard or a front garden might carry. Each is Photo, +-6 % (R3A +-8 %), at its own camera height. **R3B** (the main photograph, 1 mm elevation at 0.945 m):')
w()
B_ = K['R3B']
hd = B_['bars']['head_rz']
tab(['element', 'value (mm)', 'how'], [
    ['plinth', 'brick, four courses at 75 under a stone coping about 50 thick that overhangs 25; the top at z %s (+-20); a pier about %.0f wide under the hinge post with a pyramidal cap' % (B_['plinth']['coping_top_z']['v'], B_['plinth']['pier']['width']['v']), 'Photo; the lip height corrected 13 for the plane\'s offset'],
    ['rails', 'three flat bars about 20 x 10: bottom at z %s, middle %s, top %s' % (B_['rails']['bottom_axis_z']['v'], B_['rails']['mid_axis_z']['v'], B_['rails']['top_axis_z']['v']), 'Photo: dark rows between the bars (the review at 16k: 433, 1018, 1948)'],
    ['bars', 'round Ø%.1f (+-3; FWHM 20 with blur), **pitch %.2f** (26 bars, rms residual %.1f; three inches is 76.2), a small ball end under the bottom rail; **every second bar rises to a head: %s**, tips at **z %.0f** (+-15); the others stop at the middle rail with a small spear tip at **z %.0f**' % (B_['bars']['diameter'], R3B['bar_pitch_mm'], R3B['bar_pitch_resid_rms_mm'], B_['bars']['knop']['text'], B_['bars']['tall_tip_z']['v'], B_['bars']['short_tip_z']['v']), 'Photo; the head is the review\'s 16k profile scaled by 0.974 (17 points (r, z) in target.json: shaft Ø17.5 up to z 1973, a flare, a neck at r 14.6, the knop r 44.8 at z 2044, a ring r 21.4 at 2090 to 2099, a spire ending at the stated tip, (0, 2211))'],
    ['hinge post', 'cast, round, shaft about %.0f wide, a collar %.0f across at z 1948 to 1982, a vase %.0f across at about 2125, a spire to **%.0f**; a boss and a strap hinge near the bottom rail; the gate leaf beyond it is swung open and is not measured' % (B_['post']['shaft_width']['v'], B_['post']['collar_width']['v'], B_['post']['urn_width']['v'], B_['post']['top_z']['v']), 'Photo'],
    ['paint, wear', 'black, semi-gloss, chalky at the lower bars; paint flaking at the post collars, rust spots at the bar feet, moss and lichen on the plinth and a green-black stain under the coping', 'Photo'],
])
Ra = K['R3A']
Rd = K['R3D']
w('**R3A** (an area railing on a two-stage wall; oblique view, +-8 %%, at 1.02 m): the wall is about %.0f high (four lower courses of blue-black engineering brick to a blue bullnose string at z %.0f, five red stretcher courses to z 741, a blue bullnose coping); three rails at z %.0f, %.0f and %.0f; **the numbers are the left run\'s (preview s below %.0f)**: bars every %.0f (the thick tall bars every 240 with spear heads to z %.0f, thin short bars between them to the middle rail with a small lily plaque); posts with a vase and ball to z %.0f and scroll knees to the top rail; black. **Right of the cast post the photograph shows another pattern, fleur-de-lis heads about half a pitch out of step with the left run\'s: it is not measured and not drawn** (the review\'s point 3; group C fits only the left run). **R3D** (a front-garden railing, 1.15 m camera): a dark brick wall %.0f high (eight courses at 75 and a coping), a bottom flat-bar rail at z %.0f and a top rail at %.0f, round bars Ø%.0f every %.1f (the ten read centres; the first version\'s stated 94.5 x 1.027 = 97.0, the review\'s figure, is 1.7 higher: both inside the +-3) with small spear points to z %.0f, a gate leaf about %.0f wide with two C-scrolls hung from a brick pier; **paint dark green, sRGB (38, 56, 36)** (medians in shade (32, 47, 28) and in light (51, 69, 45)), satin. A hoop-top (bow-top) railing and a boarded double gate between brick piers (Urban Street 03) were seen and not measured.' % (
    Ra['wall']['top_z']['v'], Ra['wall']['string_z']['v'], Ra['rails']['bottom_axis_z']['v'], Ra['rails']['mid_axis_z']['v'], Ra['rails']['top_axis_z']['v'], Ra['bars']['left_run_max_s']['v'], Ra['bars']['pitch_all']['v'], Ra['bars']['tall_tip_z']['v'], Ra['post']['top_z']['v'],
    Rd['wall']['top_z']['v'], Rd['rails']['bottom_axis_z']['v'], Rd['rails']['top_axis_z']['v'], Rd['bars']['width']['v'], Rd['bars']['pitch']['v'], Rd['bars']['tip_z']['v'], Rd['gate']['width']['v']))
w()

# ---------------------------------------------------------------------------------------------------------------- 7 placements
w('## 7. Where each stands')
w()
w('**The street (A1).** East footway, posts at **x 10.0 and 12.0, axis z 3.375** (Read: vignette-feet.json): 0.375 from the kerb face (z 3.0) = the scene\'s 0.125 kerb + its 0.25 set-back; **0.205 behind the kerbs target\'s granite kerb back edge (z 3.170)**. The road face of the top rail is z 3.350 (0.35 from the kerb face); the nuts face the panel\'s ends (x 9.964 and 12.036). The panel ends beside the gully (x 12.0, in the channel, the grate 440 x 290 in the kerbs target). **Set-back** (the review\'s point 9, a note and not a change): the scene\'s 0.25 behind the kerb is kept; a 1980s rule of about 0.45 is remembered (by the writer and the review) and not read: it is in section 13.')
w()
w('**Footway left to walk, from 0 to 2.0 m high (the check the brief asks for, as the review amended it).** The panel\'s rear face is the top rail\'s, z 3.375 + 0.025 = **3.400**; the nearest fixed projections behind it in x 9.5 to 12.5 are the stallriser face at z 5.125 - 0.15 = **4.975** (the pilasters\' 5.025 are farther back at the shop doors) at every height, and above 1.9 m the sloping underside of the fish market\'s awning (awning_02, x 10.5 to 13.5, z 3.39 to 5.125). I read the awning\'s mesh (`ledger/Assets/Props/base-mesh/awning_02.glb`, live in the self-check): the body falls from the fascia\'s underside at the wall to a front edge 1.896 above the footway at z 3.39, **right over the rail line**, with a scalloped valance hanging to 1.57 at that same z (10 mm in front of the rail\'s rear face, so nobody walks into it from behind the rail); the review estimated the clear width at a 2.0 m head from a straight line from the valance\'s bottom (about 1.0).')
w()
tab(['height of the body (m)'] + list(WS['clear_at_heights_m'].keys()), [['free width, rear face to the nearest projection (m)'] + list(WS['clear_at_heights_m'].values())])
w('So the free width is **1.575 m at ground level** and **%.2f m at a 2.0 m head** (the least, A1_walking_clear), against a walking person\'s 0.68 (the scene says 1.57 for the ground). It is the fixtures that decide: **nothing deeper than 0.895 m (1.575 - 0.68) may stand between the rail and the frontage in x 9.5 to 12.5** (A1_no_deep_obstacle); the fish market\'s 0.92 m crates would leave 0.655, the failure of 29 September, so they may not stand there. The check is the least over 0 to 2.0 m, so a lowered awning would be caught. Drawn: `target-plan-street.jpg` and `target-a1-walking-section.jpg`.' % WS['min_clear_m'])
w()
w('**The quay (Q2), in the south-quay kit\'s frame (x along Quay Street, y across).** The jetty strip is x -130 to -110, y -100 to -15; its cope nose is x -110 on the basin edge and y -15 at the tip (the cope stands 0.05 proud of the wall face); its stone parapet (1.1 high, x -129.4 to -128.6) runs on the seaward side to y -23.0; the harbour light stands at (-120, -19.5) on a plinth 2.8 square; the bollards target puts K6 bollards at (-110.75, -80) and (-110.75, -45) and K7 cleats at x -110.25, y -64, -58, -52; **the kit hangs mooring rings on the basin face at (-110.05, -62) and (-110.05, -32)** (read live from the kit\'s `mooring_rings` piece by the self-check). The first version\'s basin run (posts y -36.4 to -15.4) stood 1.4 m from the ring at y -32 and left the seaward corner open; the review was right on both: a railing over a working berth\'s ring would stop the lines, and the corner by the light is where a visitor would walk off. The railing now:')
w()
tab(['run', 'model', 'line', 'posts (x, y)', 'bays'], [
    ['Q2_basin_edge', 'Q2a, two rails', 'x -110.4, 0.4 behind the nose; the last two bays before the light', pts(PQ[0]), '2 of 3.0'],
    ['Q2_tip, before the harbour light', 'Q2b, rail and chain', 'y -15.4, 0.4 behind the nose; shares the corner post (-110.4, -15.4)', pts(PQ[1]), '6 of 3.0'],
    ['Q2_seaward_return', 'Q2b, rail and chain', 'x -128.4, from the tip\'s corner post (-128.4, -15.4) back to the parapet\'s end; its end bay is 1.4', pts(PQ[2]), '3.0, 3.0, 1.4'],
])
w('**12 posts, 11 bays, 31.4 m** (two Q2a bays and nine Q2b bays: nine chains). **Clearances (Derived, checked live):** the nearest post to a bollard or a cleat is 23.6 m (K6 at y -45), so Q2_clear_of_mooring (at least 8.0) holds; **the nearest post to a mooring ring is 10.6 m** (the post (-110.4, -21.4) to the ring at y -32; the other ring is 40 m away) and no rail is nearer: **Q2_clear_of_rings, at least 4.0 m**; the nearest post to the light\'s plinth face is 2.7 m; the return closes the corner: its end post (-128.4, -22.8) stands 0.2 from the parapet\'s inner face (x -128.6) and 0.2 from its end (y -23.0), its plate 0.1 clear (**Q2_corner_closed**, within 0.25). **Not railed: the north quay, the east quay and the jetty\'s berth (y -100 to -23 on the basin face)**: boats alongside, rings, ladder, bollards, fish boxes; the bollards target\'s K5 chain posts about the ladder are the only edge protection there; the cope\'s nose stays bare. A person on the jetty has the whole 20 m strip: the 0.68 check is trivially met (Q2_walking_clear). `target-plan-jetty.jpg` draws the three runs and the two rings.')
w()
w('**Absent, with the reasons:** ' + ' '.join('%s: %s.' % (k.replace('_', ' '), v.rstrip('.')) for k, v in T['placements']['absent'].items()))
w()

# ---------------------------------------------------------------------------------------------------------------- 8 materials
w('## 8. Materials and colours')
w()
tab(['id', 'sRGB', 'roughness (words, 0 to 1)', 'metal', 'use'], [[m['id'], tuple(m['srgb']), '%s, %s' % (m['roughness_words'], m['roughness']), m['metal'], m['use']] for m in T['materials']])
w('The black is the one paint the three families share (bollards K1, K2, K5, K6: (24, 24, 26)); the photographed blacks measure (22, 21, 21) to (24, 24, 28) before tone-mapping differences. **The A1 default is the galvanised grey** (the review\'s point 5). **The only coloured ironwork reached is R3D\'s green**; red, white, yellow and banded paints are not used (no photograph shows one, and the research says reflective bands are wrong for 1990). No white or yellow band, no sleeve, no reflective strip on any post.')
w()

# ---------------------------------------------------------------------------------------------------------------- 9
w('## 9. Wear and damage, summarised; the photographs-win disagreements')
w()
w('Painted iron wears at its feet first (flaking, rust spots, dirt banked up), at the collars and at the rails where hands rest (rubbed bright), and takes dirt from the ground up; the photographed ironwork shows no dents, no graffiti and no stickers except notices wired on. A guard rail beside a kerb takes more: tyre spray on the road face, bumps that bend a bar, scrapes on the lower rail; galvanising goes dull grey with white bloom and dark run-marks below the fixings. Quay iron takes salt bloom and rust at its nuts and welds.')
w()
tab(['element', 'book, scene or the earlier targets', 'photograph', 'chosen'], [[d['element'], d['book'], d['photograph'], d['chosen']] for d in T['photographs_win']])

# ---------------------------------------------------------------------------------------------------------------- 10
w('## 10. Variants the street needs')
w()
w('One panel on the street: **A1 one model** (the asset plan\'s "1 kit"), three conditions chosen once for the one panel (the others stay for other streets): ' + '; '.join('%s (%.0f %%): %s' % (c['id'], 100 * c['share'], c['note']) for c in T['variants']['A1_conditions']) + '. **Q2 two models** (Q2a two rails, Q2b rail and chain), one run each (Q2a twice, Q2b nine times). The reserve kinds have one model each. Models per kind at most four (asset plan).')
w()

# ---------------------------------------------------------------------------------------------------------------- 11
w('## 11. The checks unit 3.3\'s automatic check must pass')
w()
w('`target.json` `checks` lists %d: each a name, what to measure, the expected value and the tolerance (a "maximum" or a "minimum" where it is a limit). The review\'s section checks (A1_post_section, A1_post_top, A1_top_rail_section, A1_bottom_rail_section, A1_bolts, A1_bbox) replace the round-section ones; A1_foot_ring became A1_foot_patch.' % len(CK))
w()
tab(['name', 'what to measure', 'expected', 'tolerance', 'unit', 'basis'], [[c['name'], c['what'], c['expected'], ('max' if c.get('max') else ('min %s' % c['minimum'] if 'minimum' in c else '+-%s' % c['tol'])), c['unit'], c['basis']] for c in CK])
w()

# ---------------------------------------------------------------------------------------------------------------- 12
w('## 12. What the target could not settle')
w()
for s in T['could_not_settle']:
    w('* ' + s)
w()

# ---------------------------------------------------------------------------------------------------------------- 13
w('## 13. What I would read once the network opens (from Jafar\'s PC first)')
w()
for s in T['to_read_when_the_network_opens']:
    w('* ' + s)
w()

# ---------------------------------------------------------------------------------------------------------------- 14
w('## 14. The previews (production/previews/cloud-week/refs/railings/), credited')
w()
w('All crops are of the object only: the railing\'s own elevation, cut to the objects; a boat\'s name board and a distant figure are painted flat grey; nothing else that the brief bars (no car, person, readable lettering, litter, bottle or sign) is in any picture. Photographs: Poly Haven, CC0, Andreas Mischok (S1 to S3); the drawings are this target\'s. Elevations are rectified at the stated per-object camera heights; the red outline is the drawing laid on the photograph, the cyan ticks z every 100.')
w()
tab(['file', 'what'], [
    ['`ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S1: R3B, the main photograph (3 mm a pixel, s 680 to 3770, z -50 to 2385, at 0.945 m); the drawing laid on it (bars of the fixed panel, rails, plinth, heads, hinge post)'],
    ['`...-r3b-park-railing-head-close.jpg`, `...-foot-close.jpg`', 'S1: 1 mm closes of the turned heads (the knop and the ring) and the post\'s finial, and of the plinth, pier and the bars\' ball feet'],
    ['`ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S1: R3A (3 mm, oblique, 1.02 m), and the drawing on it (left run only)'],
    ['`ph-urban_street_01-r3d-garden-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S2: R3D (1.15 m) and the drawing on it'],
    ['`ph-limehouse-lhb-chain-bay-elevation.jpg`, `...-target-on-photo.jpg`', 'S3: the chain bay (4 mm, 1.13 m), the target\'s catenary (sag 200, red) at the photographed lug heights; yellow ticks the photographed lowest points'],
    ['`target-drawing-sheet.jpg`', 'the drawings of A1 (RHS, studs at the rail ends), Q2a and Q2b (elevations)'],
    ['`target-a1-bolt-section.jpg`', 'a plan section along the top rail\'s stud axis: the rail end, its 6 mm end plate, the post wall, the M10 stud welded to the plate (61 long), the nut on the outer face and the thread'],
    ['`target-a1-beside-photographed-bars.jpg`', 'R3B (76.6), R3D (95.3) and A1 (109.1) at one scale: the evidence for the infill'],
    ['`target-plan-street.jpg`, `target-a1-walking-section.jpg`', 'the east footway at the panel (x 8 to 14) with the walking strip, the awning\'s outline and the tarmac patches; the section across the footway: rail, stallriser, awning and the 0.68 m strip'],
    ['`target-plan-jetty.jpg`', 'the jetty with the three Q2 runs, the harbour light, the K6 and K7 mooring furniture and the kit\'s two mooring rings; the 10.6 m clearance marked'],
])
w('Fitted on the photographs by `self_check.py` group C: R3B\'s bar centres (23 of the fixed panel\'s bars, median residual 3 mm, pitch scale fitted on that one dimension 1.0005), its three rails, its coping edge, its tall tip, its knops and its post top; the lean of its bars in the photograph (0.65 degrees); R3D\'s wall top, rails, bars and brick courses; R3A\'s rails, wall edges, tall bars of the left run and brick courses; the chain\'s lowest points at LHB.')
w()

# ---------------------------------------------------------------------------------------------------------------- 15
w('## 15. Files, and what to hand on')
w()
w('`TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`; the makers `make_target.py` (the numbers), `measure.py`, `calibrate.py` (both need the panoramas), `make_previews.py`, `make_doc.py`, `frames.py` (the per-object heights and windows), `awning_lib.py`, `rail_lib.py`; `anchors.json` (the horizon anchors\' raw rows) and `photo_measurements.json` (the automated and hand-read measurements, both sets, with their errors). `TARGET-REVIEW.md` is the review\'s and is not touched.')
w()
h = T['handover']
w('* **To the builder**: ' + h['to_builder'])
w('* **To the bollards writer**: ' + h['to_bollards_writer'])
w('* **To the kerbs writer**: ' + h['to_kerbs_writer'])
w('* **To the town session**: ' + h['to_town_session'])
w('* **For NOW.md**: ' + h['for_NOW_md'])
w()
open(os.path.join(HERE, 'TARGET.md'), 'w', encoding='utf-8').write('\n'.join(L))
print('wrote TARGET.md', os.path.getsize(os.path.join(HERE, 'TARGET.md')), 'bytes')
