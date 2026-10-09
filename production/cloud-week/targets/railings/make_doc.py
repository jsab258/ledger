#!/usr/bin/env python
"""Writes TARGET.md of the railings family from target.json (its numbers) and the prose below.
    /home/user/.bpyenv/bin/python make_doc.py
Run self_check.py after it: the self-check reads TARGET.md (group E) and the doc quotes the last self-check result from target.json."""
import json, os
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


w('# Quay Street\'s railings: the guard rail, the quay railing and chain, and the boundary railings the street does not have: the target (cloud week 42, 9 October 2026)')
w()
w('**Quay Street\'s one pedestrian guard rail is a 2.0 m panel, 1.0 m high, on two 48.3 mm steel posts (a 42.4 top rail flush with flat caps, a 33.7 rail at 200, seventeen 12 mm bars in 97.1 mm gaps, welded, black, post axes 0.375 m from the kerb face at x 10.0 to 12.0, leaving 1.576 m of footway); the quay kit has no railing, so a 3.0 m-bay tube railing on 76.1 mm posts (two rails, or a rail and a plain 13 mm chain sagging 200) is proposed for the jetty\'s basin edge and tip only (14 posts, 13 bays); the street has no area railing, chapel railing or yard gate; no photograph of a guard rail or a tube railing was reachable, so both are Judgement, backed by three photographed bar railings (bars every 78.5, 94.5 and 114) and one photographed chain bay.**')
w()
w('The target for the family "railings on Quay Street and its quay", written from Poly Haven\'s CC0 London photographs (all 2019) and the repository\'s own numbers. Everything is millimetres unless a line says otherwise (placements are metres in the street\'s or the south-quay kit\'s frame); the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, sections, plans, a sample of each reserve railing, the two placement plans) from target.json alone; `self_check.py` tests them against their own sources (last result: **' + SC + '**). `make_target.py`, `measure.py`, `calibrate.py`, `make_previews.py`, `make_doc.py`, `frames.py` and `rail_lib.py` re-make the files from the hand-read numbers and the panoramas.')
w()
w('**What is photographed and what is not, in one breath.** Photographed (Photo, +-6 % in size): R3B, a tall cast-iron park railing on a brick plinth (bars every 78.5, rails at 445, 1045 and 2000, spire heads to 2300, a hinge post to 2375); R3A, an area railing on a two-stage dwarf wall (bars every 114, rails at 840, 1435 and 1645); R3D, a low dark-green railing on a garden wall (bars every 94.5, rails at 680 and 1085); and LHB, one bay of the marina chain posts, whose lug heights (800 and 405) and chain sag (215 to 240) test the bollards target. **Not photographed, Judgement:** the guard rail A1 and the quay tube railing Q2, every number except the scene\'s own and the bollards target\'s chain. This is the target\'s first version.')
w()

# ---------------------------------------------------------------------------------------------------------------- 1
w('## 1. What the street has, what it needs, and where there is nothing to draw')
w()
w('The scene (SCENE-SLOTS.md, read 9 October; vignette-scene.json E8) places one guard rail: **a 2.0 m panel, 1.0 high, posts 0.05, rails 0.04, five infill bars of 0.025, east side, x 10.0 to 12.0, 0.25 m back from the kerb**, beside the gully at x 12.0. It was three panels (to x 16.0) until 29 September, when the AI tester found the east footway walled: the crates of the fish market left 0.65 m between rail and frontage, less than a walking person\'s 0.68. The held `trunk_protection_railing` is a tree-pit guard and is not this object (the bill of materials says so). The vignette-feet file puts both posts at z 3.375 and the pieces list shows the stand-in\'s lower rail 0.45 above its foot.')
w()
w('The asset plan names two linear kits for this family: "2 m guard-rail panel (posts, rails, infill)" and "two-rail tube railing with chain", one kit each ("Guard railing; quay railing with chain; fences": 1 kit; 1 kit), 1 to 3 panels on the street and a quay railing "along the quay".')
w()
w('**(a) The kerbside guard rail** is kind A1 below. **(b) The quay.** The south-quay kit (tools/art-recipes/south-quay, read 9 October, built live by the self-check) has a granite cope along every quay edge, ten cast-iron bell bollards, a ladder, a stone parapet on the jetty\'s seaward side and walled yards with boarded gates; it has **no railing on any quay edge**, and a search of its pieces for "rail" finds none. The bollards target (K5) adds four chain posts and two plain chains about the north quay\'s ladder (x -69.5, y -40.5 to -31.5). An earlier session read a 1989 photograph of the River Hull (the atlas\'s R08, Flickr, unreachable here) that shows a "chain-edged quay": chain at a working quay\'s edge is period-attested, a tube railing is not. So the working north and east quays stay as they are, and **kind Q2, a tube railing with 3.0 m bays, goes only where the public walks out: the jetty\'s basin edge and its tip before the harbour light** (section 7). This is Judgement and new to the kit; the integrator may refuse it and nothing else in this target depends on it.')
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
w('**What the search summaries gave (leads only, no number taken as a measurement).** BS 3049:1976 "Pedestrian guard rails (metal)" existed in 1990 (it was withdrawn on 15 November 1995 and BS 7818 replaced it); present-day catalogue panels use 12 mm bars at 110 to 112 centres (a 100 mm sphere may not pass), posts 50 x 30 mm and a height of 1100; Kent dates pedestrian guardrail from the 1930s; a 1983 London study and a 1988 article say the conventional rail hid the road and that a see-through type did better; working fish-quay berths in a present-day harbour audit are left unfenced; at Bideford the quay has cast-iron posts with tubular bars and chains from 1899 to 1905. These lead the Judgement numbers below and are named where they do.')
w()

# ---------------------------------------------------------------------------------------------------------------- 3
w('## 3. No guard rail was photographed: what the target rests on instead')
w()
w('Fifteen of Poly Haven\'s British panoramas (every one in Greater London and Cambridge; the two Epping Forest ones and St Fagans\' interior were not opened) were looked at in six to eight rectilinear views each. **None shows a kerbside pedestrian guard rail, a tube railing on a quay or a bar railing of the 1976 pattern.** What they show is cast and wrought bar railing (Bethnal Green, Urban Street 01), a steel palisade (Urban Street 02, 2000s, left out), stainless dock-edge balustrades (Canary Wharf, Adams Place Bridge, 2000s, a modern-only form, left out), a hoop-top railing and bolted chain posts with chain (Bethnal Green, Limehouse). Wikimedia Commons, Geograph, Flickr and the Historic England Archive, which hold 1980s photographs of exactly this object, refused the cloud.')
w()
w('So A1 and Q2 are built in three layers, each marked where it is used:')
w()
w('1. **Read**: the scene\'s numbers (2.0 m panel, 1.0 m high, post 0.05, rail 0.04, x 10.0 and 12.0, z 3.375), the frontage and kerb numbers, the bollards target\'s chain and 3.0 m bays.')
w('2. **Photo, by analogy**: all three photographed bar railings have their bars at 78.5, 94.5 or 114 centres (clear gaps 61 to 100): none has the scene\'s 333 mm gaps (five bars in 2.0 m). They are black (22 to 24 grey levels) except one council green. Their feet end in a ball or sit on a rail, their bars are round and plain. These set the bar rhythm and the paint.')
w('3. **Judgement**: tube sizes (the nearest standard tubes to the scene\'s 50 and 40: 48.3, 42.4 and 33.7; 76.1 for the quay posts), the lower rail\'s height, the cap, the welds, the ground detail, the wear, and the places on the jetty. Each is flagged in the part tables.')
w()
w('Where the photographs and the scene differ the photographs win, element by element (section 9). The scene\'s five 25 mm bars are replaced by seventeen 12 mm bars, because a bar railing with 308 mm gaps is not seen in any reached photograph.')
w()

# ---------------------------------------------------------------------------------------------------------------- 4
w('## 4. How the photographs were measured, and why the camera height is not 1.6 m')
w()
w('Each panorama (8192 x 4096) is re-projected with numpy to a flat elevation of one vertical plane through the foot line of the object (`rail_lib.py`: a ground point from the foot\'s pixel and the camera height, a plane through two of them, 1 mm to 4 mm a pixel; the native resolution is 3 to 5 mm at 5 to 7 m, so every picture is soft). **Every length then scales with the camera height at the ground the object stands on**, which the panoramas do not give. Each height is measured by the horizon method of the bollards and kerbs targets (`calibrate.py`: in a levelled panorama the horizon is the middle row; brick courses of a wall are evenly spaced in tan(angle below it), so the camera height above the wall\'s foot = 75 mm x tan(angle of the foot) / (course pitch in tan units)), on brick walls and piers that stand on the same ground as the railings.')
w()
rows = []
for a in CAL['horizon_anchors']:
    import math
    H = a['image_rows']
    h = a['gauge_mm'] * math.tan((a['foot_row'] - H / 2) * math.pi / H) / a['pitch_tan'] / 1000 + a['step_m']
    rows.append([a['pano'], a['id'], a['what'], 'cols %d-%d, rows %d-%d, foot row %d, pitch %.5f' % (a['cols'][0], a['cols'][1], a['rows'][0], a['rows'][1], a['foot_row'], a['pitch_tan']), '%.3f' % h])
tab(['panorama', 'anchor', 'what', 'raw rows', 'camera height above the foot (m)'], rows)
rows = []
for pano, P in CAL['panoramas'].items():
    rows.append([pano, '%.2f +-%.2f' % (P['h_cam'], P['err']), P['why']])
tab(['panorama', 'stated height at the objects\' ground', 'why'], rows)
w('Results: **no panorama was taken at 1.6 m**; the heights are 0.97 (Bethnal Green) and 1.12 m (Urban Street 01 and Limehouse) above the ground of each object. **Every number below is +-6 % in absolute size**; counts, pitches\' ratios and the proportions are exact to the pixel. `self_check.py` recomputes every anchor from its stored rows and fails if the mean at the objects\' ground is farther from the stated height than the stated error (group B). Where the three families overlap they agree: Bethnal Green 0.97 against the bollards target\'s 1.02 +-0.07, Limehouse 1.12 against its 1.17 +-0.06; the K5 post reads 1086 here and 1135 there, the same 4.3 % as the camera heights.')
w()
w('The photographed bar pitch is a second, independent hint of the scale: R3B\'s 78.5 is 3 % over three inches (76.2), and a Victorian railing is likely to have been made to three inches; this is not used to adjust anything.')
w()
w('**Tell the kerbs-and-covers and bollards writers** (already said in their targets): the panoramas are 0.97 to 1.12 m above their ground; sizes taken at 1.6 m are 30 to 65 % too large.')
w()
w('Other methods: `measure.py` finds the bars of R3B as the dark minima of the column profile of a 1 mm elevation at z 700 to 900 and fits their pitch (26 bars, 78.54 mm, rms residual 4.0 mm); its rails as dark rows between the bars; heads, posts, wall tops and rails of the other three were read by eye on gridded 1 mm and 2 mm elevations (`photo_measurements.json`, each with its error and how). The self-check\'s group C re-detects bars, rails, wall tops and tips on the 3 mm previews and compares them with the drawing (a scale fitted on one dimension, the bar pitch).')
w()

# ---------------------------------------------------------------------------------------------------------------- 5 frames
w('## 5. Frame, pivot, glb')
w()
w('* **A1**: local x along the panel (0 at its middle), y across (0 on the rail line, + toward the carriageway), z up from the flag top at the posts. **Pivot: the middle of the panel on the ground.** In the street recipe\'s frame the axis is z 3.375 and the posts stand at x 10.0 and 12.0 (placements, section 7).')
w('* **Q2**: local x along the run (0 at the middle of a bay), y across (+ toward the water), z up from the apron at the post foot; pivot at the middle of the bay on the ground. Placed in the south-quay kit\'s frame (x along Quay Street, y across, east +; the apron and copes at +0.05).')
w('* **glb**: metres, z up, scale 1; one mesh per piece kind and material (posts, rails, bars, caps, welds, base plates and nuts, chain links and eyes as separate meshes of the same piece); **no text, no decal with lettering, no number, no crest, no maker\'s mark** on any mesh or texture.')
w('* The elevation pictures of the photographs are rectified to the plane 110 mm behind the front face of a wall (where a railing stands on a wall), so a feature at the wall\'s front edge is 13 mm (R3B) lower than its true height; the notes say where this matters.')
w()

# ---------------------------------------------------------------------------------------------------------------- 5 A1
w('## 6. The target, kind by kind')
w()
w('Every number carries its kind: **Read** (printed in the repository), **Photo** (measured on a photograph: method in section 4, +-6 % in size), **Derived**, **Judgement** (a trade or period guess, said so).')
w()
w('### 6.1 A1: the kerbside pedestrian guard rail (`guard_rail_panel`, the scene\'s E8). Judgement, with Read numbers from the scene')
w()
P_ = A
tab(['part', 'dimensions (mm)', 'position', 'kind and basis'], [
    ['post (two)', 'round steel tube OD %s, wall %s, 1000 high above the flag; below ground 400, not modelled' % (P_['post']['od'], P_['post']['wall']), 'axes at x -1000 and +1000, y 0', 'Judgement: the nearest standard tube to the scene\'s 50 (a 1.5 inch nominal-bore tube is 48.3); height Read (the scene\'s 1.0)'],
    ['post cap (two)', 'flat pressed-steel plug, OD %s, %s thick, rim R2, 2 mm weld bead round it' % (P_['cap']['od'], P_['cap']['thickness']), 'z 992 to 1000: its top is the panel\'s top', 'Judgement'],
    ['top rail', 'round tube OD %s, wall %s; saddle-cut ends welded to the posts; length %.2f between the post faces' % (P_['top_rail']['od'], P_['top_rail']['wall'], 2 * P_['top_rail']['x'][1]), 'axis z %.1f, so its top is z 1000, flush with the caps' % P_['top_rail']['axis_z'], 'Judgement: 1.25 inch nominal bore; the scene\'s 40'],
    ['bottom rail', 'round tube OD %s, wall %s; same length and welds' % (P_['bottom_rail']['od'], P_['bottom_rail']['wall']), 'axis z 200 (underside 183): a hand\'s width over the flags', 'Judgement: the stand-in\'s lower rail at 450 had no photograph; R3D\'s bottom rail is 60 over its wall'],
    ['infill (17 bars)', 'solid mild-steel round bar Ø12, vertical, from the bottom rail\'s axis to the top rail\'s axis (the ends hide in the rails); a 2 mm weld at each end', 'x = %s ... %s, pitch %.2f, clear gap %.2f between bars and between a bar and a post' % (P_['infill']['x'][0], P_['infill']['x'][-1], P_['infill']['pitch'], P_['infill']['clear_gap']), 'Judgement: the gap rule (at most 100) from the search-summary lead; the pitch is inside the photographed 78.5 to 114'],
    ['weld beads', '3 mm fillet ring where each rail end meets a post; 2 mm at each bar end; not ground off', 'at the 4 rail ends and the 34 bar ends', 'Judgement'],
])
w('* **Overall**: 2052.0 x 52.0 x 1000.0 (the caps at x +-1000 are 52 across). **Panel length**: 2000 between post axes (Read). **How panels join**: a second panel (none on this street) would share the post, its rails butting the same tube; the bars are not offset. **How it ends**: at its posts: an end post is the same post with the same cap; no return, no end rail, no stay; the one panel ends at x 12.0 beside the gully.')
w('* **How it meets the ground**: the posts are concreted into the footway and the flags are cut round them; a **20 mm dark bitumen or tarmac joint ring** (sRGB (40, 38, 36), rough) lies flush round each post; no collar plate, no base plate, no fixing visible. The posts stand on the flag top; the builder reads the ground under them (the scene\'s foot level is y 0.05625; the kerbs target\'s flag level gives y 0.040).')
w('* **Edges**: nothing sharp: tube ends saddle-cut and welded, the cap\'s rim R2, bar ends hidden in welds. **Seams**: the post tubes show a faint longitudinal seam (0.3 mm ridge) on the footway side (Judgement). **Fixings**: none visible (a welded panel on welded posts). **Marks**: none: no plate, number, stencil, crest or maker\'s name.')
w('* **Paint**: **black gloss paint over galvanising, sRGB (24, 24, 26), semi-gloss, roughness 0.42, metal 0**: the same black as the bollards target\'s cast posts and the blacks measured on two panoramas (R3A (22, 21, 21) and the K5 post (23, 24, 28); R3B\'s raw median (36, 43, 30) is polluted by the foliage behind its bars). Variants below.')
w('* **Wear and damage** (Judgement, patterned on what the photographs show of black ironwork: flaking at the collars, rust at the bar feet and the foot of the post, dirt on the plinth): ' + '; '.join(A1['wear']) + '.')
w()
w('**Seeds per instance**: lean 0 to 1 degree toward the carriageway; bent bars 0 to 2 (5 to 15 mm out at z 300 to 600); rust at the feet 0 to 1; dirt height 300 to 600; bright-rubbed patches on the top rail 0 to 3; sticker remnants 0 to 2; chips 0 to 10.')
w()

w('### 6.2 Q2: the quay tube railing, two models (`quay_tube_railing`). Judgement; the chain is the bollards target\'s and Photo for its sag')
w()
P_ = Q2
tab(['part', 'dimensions (mm)', 'position', 'kind and basis'], [
    ['post', 'round steel tube OD %s, wall %s, %s above the apron; a pressed domed cap OD 80, rise 14, welded; a 5 mm fillet weld at the foot' % (P_['post']['od'], P_['post']['wall'], P_['post']['height']), 'bay ends at x +-1500', 'Judgement: 3 inch nominal bore; a quay post is heavier than the street\'s'],
    ['base plate', '200 x 200 x 12, four Ø18 holes on a 150 square (25 from each edge), four M16 studs with hex nuts 24 across flats and 13 high, the studs 10 proud of the nuts; 25 mm grout bed and a 20 mm fillet round the plate', 'z 0 to 12', 'Judgement'],
    ['top rail', 'tube OD 48.3, wall 3.2, saddle-welded; length %.2f' % (2 * P_['top_rail']['x'][1]), 'axis z 1000 (top 1024.2)', 'Judgement'],
    ['low rail (Q2a)', 'tube OD 42.4, wall 2.6, same length', 'axis z 500', 'Judgement'],
    ['chain (Q2b, in place of the low rail)', 'plain short link, bar 13, inner 39 x 18, outer 65 x 44, pitch 39, **no spikes**; 74 links between two eyes; alternate links edge-on', 'a catenary from eye to eye, z 500 at the eyes, **sag 200** (lowest z 300); arc %s' % Q2['chain']['arc_length'], 'Read: the bollards target\'s chain; sag Photo (LHB 215 to 240 for the marina\'s) and not the bollards target\'s 150'],
    ['eye ears (Q2b)', 'flat-bar ears 40 wide x 70 high x 8 thick, a Ø24 hole centred 45 from the post surface; one each side of every post', 'z 500, on the rail line facing the bay', 'Judgement (the bollards target\'s D-lug is 55 x 40 x 18 with the same Ø24 hole)'],
])
w('* **Bay**: 3000 post axis to post axis (Read: the bollards target\'s spacing). **Ends**: a run ends at a post of the same kind; at a corner two runs share one post with the rails mitred to it. **Edges**: saddle cuts, fillet welds, cap rim R3, plate edges R2. **Marks**: none.')
w('* **Paint**: black satin over galvanising, sRGB (24, 24, 26), roughness 0.55, metal 0: the K5 post\'s and the K6 bollards\'. Nuts and studs bright steel (150, 150, 152) with dull rust at the threads; the chain black, rubbed bright where the links touch.')
w('* **Wear**: ' + '; '.join(Q2['wear']) + '.')
w()
w('**The chain against the photograph (LHB).** One bay of the marina\'s chain posts, rectified to the plane through two post axes (span 2840, the bollards target\'s 3.06 read between two posts): the lugs are at z 800 and 405 (the bollards target: 420 and 840, 4 to 5 % higher at its 1.17 m camera), the upper swag hangs to z 585 (sag 215), the lower to 165 (sag 240), the post is 1086 high (1135 there). The target\'s sag of 200 is between the bollards target\'s 150 and the photograph\'s 227; **the bollards writer should raise K5\'s to 200**. The photographed chain is the marina\'s ornamental one with spikes on every second link; only its sag and the lugs\' heights are used.')
w()

w('### 6.3 The reserve kinds, photographed and not placed (R3B, R3A, R3D)')
w()
w('These stand for the railings a chapel, a yard or a front garden might carry. Each is Photo, +-6 % (R3A +-8 %). **R3B** (the main photograph, 1 mm elevation at 0.97 m):')
w()
B_ = K['R3B']
tab(['element', 'value (mm)', 'how'], [
    ['plinth', 'brick, four courses at 75 under a stone coping about 50 thick that overhangs 25; the top at z %s (+-20); a pier 550 wide under the hinge post with a pyramidal cap' % B_['plinth']['coping_top_z']['v'], 'Photo; the lip height corrected 13 for the plane\'s offset'],
    ['rails', 'three flat bars about 20 x 10: bottom at z %s, middle %s, top %s' % (B_['rails']['bottom_axis_z']['v'], B_['rails']['mid_axis_z']['v'], B_['rails']['top_axis_z']['v']), 'Photo: dark rows between the bars'],
    ['bars', 'round Ø17 (+-3; FWHM 20 with blur), **pitch %.2f** (26 bars, rms residual %.1f), a small ball end under the bottom rail; **every second bar** rises to a spire with a ring at 2040, a vase swelling to 60 across at 2128, a bead at 2190 and a spire to **z 2300**; the others stop at the middle rail with a small spear tip at **z 1225**' % (R3B['bar_pitch_mm'], R3B['bar_pitch_resid_rms_mm']), 'Photo'],
    ['hinge post', 'cast, round, shaft about 100 wide, a collar 155 across at z 2000 to 2035, a vase 135 across at 2180, a spire to **2375**; a boss and a strap hinge near the bottom rail; the gate leaf beyond it is swung open and is not measured', 'Photo'],
    ['paint, wear', 'black, semi-gloss, chalky at the lower bars; paint flaking at the post collars, rust spots at the bar feet, moss and lichen on the plinth and a green-black stain under the coping', 'Photo'],
])
w('**R3A** (an area railing on a two-stage wall; oblique view, +-8 %): the wall is 780 high (four lower courses of blue-black engineering brick to a blue bullnose string at z 300, five red stretcher courses at 75 to z 705, a blue bullnose coping); three rails at z 840, 1435 and 1645; bars every 114 (the thick tall bars every 228 with fleur-de-lis heads to z 1880, thin short bars between them to the middle rail with a small lily plaque); posts with a vase and ball to z 2150 and scroll knees to the top rail; black. **R3D** (a front-garden railing, 1.12 m camera): a dark brick wall 620 high (eight courses at 75 and a coping), a bottom flat-bar rail at z 680 (60 over the wall) and a top rail at 1085, round bars Ø13 every 94.5 with small spear points to z 1130, a gate leaf about 1040 wide with two C-scrolls hung from a brick pier; **paint dark green, sRGB (38, 56, 36)** (medians in shade (32, 47, 28) and in light (51, 69, 45)), satin. A hoop-top (bow-top) railing and a boarded double gate between brick piers (Urban Street 03) were seen and not measured.')
w()

# ---------------------------------------------------------------------------------------------------------------- 7 placements
w('## 7. Where each stands')
w()
P0 = T['placements']['street'][0]
w('**The street (A1).** East footway, posts at **x 10.0 and 12.0, axis z 3.375** (Read: vignette-feet.json): 0.375 from the kerb face (z 3.0) = the scene\'s 0.125 kerb + its 0.25 set-back; **0.205 behind the kerbs target\'s granite kerb back edge (z 3.170)**, so a gap of 0.181 between the kerb and the post\'s face remains. The road face is the -z face. The panel ends beside the gully (x 12.0, in the channel, the grate 440 x 290 in the kerbs target).')
w()
w('**Footway left to walk (the check the brief asks for).** The panel\'s rear face is z 3.399 (axis + 24.15); the nearest fixed projection on the frontage is the stallriser face at z 5.125 - 0.15 = 4.975 (the pilasters\' 5.025 are farther back at the shop doors): **1.576 m clear, against a walking person\'s 0.68** (the scene\'s note says 1.57). It is the fixtures that decide: **nothing deeper than 0.896 m (1.576 - 0.68) may stand between the rail and the frontage in x 9.5 to 12.5**; the fish market\'s 0.92 m crates would leave 0.656, which is the failure of 29 September, so they may not stand there. A1_walking_clear (a minimum of 0.68) and A1_no_deep_obstacle are in the checks.')
w()
w('**The quay (Q2), in the south-quay kit\'s frame (x along Quay Street, y across).** The jetty strip is x -130 to -110, y -100 to -15 (the atlas\'s north 220 to 240, east 300 to 385); its cope nose is x -110 on the basin edge and y -15 at the tip; its stone parapet (1.1 high, x -129.4 to -128.6) runs on the seaward side to y -23; the harbour light stands at (-120, -19.5) on a plinth 2.8 square; the bollards target puts K6 bollards at (-110.75, -80) and (-110.75, -45) and K7 cleats at x -110.25, y -64, -58, -52. The railing:')
w()
tab(['run', 'model', 'line', 'posts (x, y)', 'bays'], [
    ['basin edge', 'Q2a, two rails', 'x -110.4, 0.4 behind the nose', ', '.join('(%.1f, %.1f)' % tuple(p) for p in T['placements']['quay'][0]['posts_xy_m']), '7 of 3.0'],
    ['tip, before the harbour light', 'Q2b, rail and chain', 'y -15.4, 0.4 behind the nose; shares the corner post (-110.4, -15.4)', ', '.join('(%.1f, %.1f)' % tuple(p) for p in T['placements']['quay'][1]['posts_xy_m']), '6 of 3.0'],
])
w('**14 posts, 13 bays, 39 m.** The nearest post to a bollard or a cleat is 8.6 m (y -36.4 against -45), to the light\'s plinth face 2.7 m, to the parapet 7.5 m (the parapet ends at y -23.0 and the tip rail is at y -15.4; the tip\'s west post at x -128.4 has its plate edge 0.1 m from the line of the parapet\'s inner face, -128.6). The seaward corner between the tip and the parapet\'s end (y -15.4 to -23.0) is left open: it is the boats\' end. **Not railed: the north quay and the east quay** (boats alongside, ladder, ten bollards, fish boxes; the bollards target\'s K5 chain posts about the ladder are the only edge protection); the cope\'s nose stays bare. A person on the jetty has the whole 20 m strip: the 0.68 check is trivially met (Q2_walking_clear).')
w()
w('**Absent, with the reasons:** ' + ' '.join('%s: %s.' % (k.replace('_', ' '), v.rstrip('.')) for k, v in T['placements']['absent'].items()))
w()

# ---------------------------------------------------------------------------------------------------------------- 8 materials
w('## 8. Materials and colours')
w()
tab(['id', 'sRGB', 'roughness (words, 0 to 1)', 'metal', 'use'], [[m['id'], tuple(m['srgb']), '%s, %s' % (m['roughness_words'], m['roughness']), m['metal'], m['use']] for m in T['materials']])
w('The black is the one paint the three families share (bollards K1, K2, K5, K6: (24, 24, 26)); the photographed blacks measure (22, 21, 21) to (24, 24, 28) before tone-mapping differences. **The only coloured ironwork reached is R3D\'s green**; red, white, yellow and banded paints are not used (no photograph shows one, and the research says reflective bands are wrong for 1990). No white or yellow band, no sleeve, no reflective strip on any post.')
w()

# ---------------------------------------------------------------------------------------------------------------- 9 wear summary
w('## 9. Wear and damage, summarised; the photographs-win disagreements')
w()
w('Painted iron wears at its feet first (flaking, rust spots, dirt banked up), at the collars and at the rails where hands rest (rubbed bright), and takes dirt from the ground up; the photographed ironwork shows no dents, no graffiti and no stickers except notices wired on. A guard rail beside a kerb takes more: tyre spray on the road face, bumps that bend a bar, scrapes on the lower rail. Quay iron takes salt bloom and rust at its nuts and welds.')
w()
tab(['element', 'book, scene or the earlier targets', 'photograph', 'chosen'], [[d['element'], d['book'], d['photograph'], d['chosen']] for d in T['photographs_win']])

# ---------------------------------------------------------------------------------------------------------------- 10 variants
w('## 10. Variants the street needs')
w()
w('One panel on the street: **A1 one model** (the asset plan\'s "1 kit"), three conditions chosen once for the one panel (the others stay for other streets): ' + '; '.join('%s (%.0f %%): %s' % (c['id'], 100 * c['share'], c['note']) for c in T['variants']['A1_conditions']) + '. **Q2 two models** (Q2a two rails, Q2b rail and chain), one run each. The reserve kinds have one model each. Models per kind at most four (asset plan).')
w()

# ---------------------------------------------------------------------------------------------------------------- 11 checks
w('## 11. The checks unit 3.3\'s automatic check must pass')
w()
w('`target.json` `checks` lists %d: each a name, what to measure, the expected value and the tolerance (a "maximum" or a "minimum" where it is a limit).' % len(CK))
w()
tab(['name', 'what to measure', 'expected', 'tolerance', 'unit', 'basis'], [[c['name'], c['what'], c['expected'], ('max' if c.get('max') else ('min %s' % c['minimum'] if 'minimum' in c else '+-%s' % c['tol'])), c['unit'], c['basis']] for c in CK])
w()

# ---------------------------------------------------------------------------------------------------------------- 12 could not settle
w('## 12. What the target could not settle')
w()
for s in T['could_not_settle']:
    w('* ' + s)
w()

# ---------------------------------------------------------------------------------------------------------------- 13 read
w('## 13. What I would read once the network opens')
w()
for s in T['to_read_when_the_network_opens']:
    w('* ' + s)
w()

# ---------------------------------------------------------------------------------------------------------------- 14 previews
w('## 14. The previews (production/previews/cloud-week/refs/railings/), credited')
w()
w('All crops are of the object only: the railing\'s own elevation, cut to the objects; a notice board with a telephone number, a boat\'s name board and a distant figure are painted flat grey; nothing else that the brief bars (no car, person, readable lettering, litter, bottle or sign) is in any picture. Photographs: Poly Haven, CC0, Andreas Mischok (S1 to S3); the drawings are this target\'s. Elevations are rectified at the stated camera heights; the red outline is the drawing laid on the photograph, the cyan ticks z every 100.')
w()
tab(['file', 'what'], [
    ['`ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S1: R3B, the main photograph (3 mm a pixel, s 700 to 3870, z -50 to 2450); the drawing laid on it (bars of the fixed panel, rails, plinth, heads, hinge post)'],
    ['`...-r3b-park-railing-head-close.jpg`, `...-foot-close.jpg`', 'S1: 1 mm closes of the spires and the post\'s finial, and of the plinth, pier and the bars\' ball feet'],
    ['`ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S1: R3A (3 mm, oblique), and the drawing on it'],
    ['`ph-urban_street_01-r3d-garden-railing-elevation.jpg`, `...-target-on-photo.jpg`', 'S2: R3D and the drawing on it'],
    ['`ph-limehouse-lhb-chain-bay-elevation.jpg`, `...-target-on-photo.jpg`', 'S3: the chain bay (4 mm), the target\'s catenary (sag 200, red) at the photographed lug heights; yellow ticks the photographed lowest points'],
    ['`target-drawing-sheet.jpg`', 'the drawings of A1, Q2a and Q2b (elevations)'],
    ['`target-a1-beside-photographed-bars.jpg`', 'R3B (78.5), R3D (94.5) and A1 (109.1) at one scale: the evidence for the infill'],
    ['`target-plan-street.jpg`, `target-plan-jetty.jpg`', 'the east footway at the panel (x 8 to 14) with the 0.68 m walking strip; the jetty with the two runs'],
])
w('Fitted on the photographs by `self_check.py` group C: R3B\'s bar centres (22 of the fixed panel\'s bars, median residual under 4 mm, pitch scale fitted on that one dimension within 1 +-0.02), its three rails, its coping edge, its tall tip and its post top; R3D\'s wall top, rails and bars; R3A\'s rails, wall edges and tall bars; the chain\'s lowest points at LHB.')
w()

# ---------------------------------------------------------------------------------------------------------------- 15 files
w('## 15. Files, and what to hand on')
w()
w('`TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`; the makers `make_target.py` (the numbers), `measure.py`, `calibrate.py` (both need the panoramas), `make_previews.py`, `make_doc.py`, `frames.py`, `rail_lib.py`; `anchors.json` (the horizon anchors\' raw rows) and `photo_measurements.json` (the automated and hand-read measurements with their errors).')
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
