#!/usr/bin/env python
"""Writes TARGET.md from target.json (the tables) and the prose below.  /home/user/.bpyenv/bin/python make_doc.py
Run order: make_target.py, make_doc.py, target_drawing.py OUT --overlay PREVIEWS, self_check.py"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'target.json')))
P = T['pieces']
M = T['materials']
PM = {p['id']: p for p in T['photo_measurements']}


def esc(s):
    return str(s).replace('|', '/').replace('\n', ' ')


def table(head, rows):
    out = ['| ' + ' | '.join(head) + ' |', '|' + '|'.join('---' for _ in head) + '|']
    for r in rows:
        out.append('| ' + ' | '.join(esc(c) for c in r) + ' |')
    return '\n'.join(out)


def srgb(k):
    return '%d/%d/%d' % tuple(M[k]['srgb'])


def src_table():
    rows = []
    for s in T['sources']:
        rows.append([s['id'], s['url'], s['date_read'], s['author'], s['licence'], s['date_taken'] + (f" ({s['coords'][0]}, {s['coords'][1]})" if s.get('coords') else ''), s['shows'], s['used'], s['period_or_replacement'], s['same_in_1990']])
    return table(['id', 'URL', 'date read', 'author', 'licence', 'date taken (lat, lon)', 'what it shows', 'used', 'period object or replacement', 'why the same in 1990 (or what differs)'], rows)


def pm_table():
    rows = []
    for p in T['photo_measurements']:
        res = p['result']
        rs = ', '.join(f'{k} {v}' for k, v in res.items() if not isinstance(v, dict))
        rows.append([p['id'], p['what'], p['photo'], p['method'], p['reading'], rs, p['error'], p['kind']])
    return table(['id', 'what', 'photograph', 'method', 'raw reading', 'result (mm unless named)', 'error', 'kind'], rows)


def win_table():
    return table(['item', 'scene or book', 'photograph', 'chosen', 'why'], [[w['item'], w['scene_or_book'], w['photograph'], w['chose'], w['why']] for w in T['photographs_win']])


def mat_table():
    rows = []
    for k, v in M.items():
        if not isinstance(v, dict):
            continue
        rows.append([k, v['name'], '%d/%d/%d' % tuple(v['srgb']), f"{v['roughness']} ({v.get('roughness_words', 'see name')})", v['metal'], v['kind']])
    return table(['key', 'plain name', 'sRGB (clean)', 'roughness 0-1', 'metal', 'source and kind'], rows)


def check_table():
    return table(['check', 'applies to', 'measure', 'expected', 'tolerance', 'kind'], [[c['name'], c['applies_to'], c['measure'], json.dumps(c['expected']), json.dumps(c['tolerance']), c['kind']] for c in T['checks']])


def probe_table():
    return table(['edge', 'image', 'type', 'predicted (plan mm, height mm)', 'tolerance mm', 'what'], [[e['id'], e['image'], e['type'], f"{'y' if e['kind'] == 'h' else 'x'} {e['fixed']}, z {e['z_mm']}", e['tol_mm'], e['what']] for e in T['edge_probes']])


SC = T.get('self_check', {}).get('result_line', 'not yet run')
import sys
sys.path.insert(0, HERE)
from corrected_numbers import N, REF, R as RS
CAL = T['calibration']


def cal_table():
    rows = []
    for pano, v in CAL['panoramas'].items():
        rows.append([pano, f"{v['h_m']:.3f} +-{v['err_m']:.2f}", f"{v['scale_from_1_6']:.3f}", v['ground'], f"{v['anchor_mean_m']:.3f} from {len(v['anchor_heights'])} anchors: " + ', '.join(f"{a['id']} {a['h_m']:.2f}" for a in v['anchor_heights']), v['note']])
    return table(['panorama', 'camera height used (m)', 'x (h / 1.6)', 'at the ground of', 'anchors, recomputed (m)', 'how it was settled'], rows)


def corr_table():
    return table(['item', 'panorama', 'first draft (1.6 m)', 'corrected', 'rule'], [[c['item'], c['panorama'], c['first_draft'], c['corrected'], c['rule']] for c in T['camera_height_corrections']])



def bullets(d):
    out = []
    for k, v in d.items():
        if isinstance(v, list):
            out.append(f'* **{k}**')
            out += ['  * ' + str(x) for x in v]
        elif isinstance(v, dict):
            out.append(f'* **{k}**: ' + '; '.join(f'{a}: {b}' for a, b in v.items()))
        else:
            out.append(f'* **{k}**: {v}')
    return '\n'.join(out)


DOC = f"""# Quay Street's kerbs, channel, gully grates and covers: the target (cloud week 42, 9 October 2026)

**{T['summary_line']}**

The target for the family "kerbs and drain covers on Quay Street", written from Poly Haven's CC0 London photographs (all 2019) and the repository's own numbers. Everything is millimetres unless a line says otherwise; the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (plans, sections, an elevation); `self_check.py` tests them against their sources (last result: {SC}).

## 1. What the street's present kerb gets right, and what this target changes

Today's street (SCENE-SLOTS.md, read 9 October): kerb upstand 125, width 125, depth 255, blocks 915 long, channel course 255 wide, a dropped crossover on the west side at x 22.5 (3.0 wide, 6 mm upstand, one taper block), a gully grate 400 square (recess 50, dish 30) on the east side at x 12.0, crown 75 mm above the channel. These are trade guesses, not photographs. **Every size below was first read off the pictures at an assumed camera height of 1.6 m; none of the panoramas was taken there, so each is now corrected at its own measured height (section 14).**

| | the present street | this target | why |
|---|---|---|---|
| upstand | 125 (Read) | granite {N['U']}; concrete {N['CU']} | Photo (corrected height): the arris middle reads 107 and 102 (PM01, PM02), so the top is about {N['U']}; a re-surfaced concrete kerb reads 70 to the arris middle (PM03); the 125 is outside the error |
| kerb top width | 125 | granite {N['TOPW']}, concrete {N['CW']} | Photo: 163, 167, 170 on granite (PM01, PM02, PM25), 122 on concrete (PM03): the concrete kerb is the street's 125 section, the old granite wider |
| face | not stated (vertical) | granite half-battered ({N['BATTER']} mm back); concrete bullnosed R {N['CR']} | Photo-consistent with PM26: the middle of the arris stands 26 +-9 mm behind the foot line |
| depth | 255 (Read) | 255 kept | unseen; Read |
| block length | 915 for all | granite random {N['LEN_MIN']} to {N['LEN_MAX']} (mean {N['LEN_MEAN']}); concrete 915 | Photo PM04: whole granite blocks 0.75, 0.91, 1.03 m |
| channel | 255, "in the kerb's own concrete" | granite sett channel {N['CH_W']} (two courses) beside granite; concrete block 255 beside concrete | Photo PM06: 204 +-15, setts not concrete; their brightness (1.35 to 1.7 times the road, wear target M24) is unchanged |
| crossover | 3.0 m, 6 mm upstand, one taper block | 3.0 m kept; lip of setts {N['LIP_Z']} mm; in-situ concrete ramp 1 in {N['RAMP_RUN'] / N['RAMP_RISE']:.1f}; granite flank strips; the taper block kept as a variant | Photo PM09 to PM12: the photographed crossing has no taper block |
| gully grate | 400 square, recess 50, dish 30 | {N['GA_L']} x {N['GA_W']} rectangle, 8 slots {N['GA_SLOT_W']} x {N['GA_SLOT_L']} with {N['GA_BAR']} bars (about 0.42 open), dish 15 | Photo PM13, PM14, PM28, PM30 |
| corner | none | mitred (133 degrees) and radius ({N['CORNER_R']}) | Photo PM27 (urban_street_01), PM16 (urban_street_04) |
| tactile paving | none | none | period: see 4.9 |

What the present street gets right: the 255 depth, a 3.0 m crossing, a gully in the channel on the east side, the crown, and the 125 width (now the concrete kerb's). What it gets wrong or lacks is in the table above and in section 6; the 125 upstand falls to {N['U']} and the quarter-metre channel to {N['CH_W']} once the camera heights are measured.

## 2. Sources

All photographs are Poly Haven's, CC0 (read at https://polyhaven.com/license on 9 October 2026), used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused Wikimedia, Geograph, Flickr, archive.org, gov.uk, BSI and most of the web (list below), so **no photograph from 1975 to 2000 was reached: every photograph is from 2019**, and for each object the table says why it would look the same in 1990 or what differs.

{src_table()}

**Unreached** (a page that refused is not evidence; nothing was taken from any of these):

{table(['what', 'result', 'used'], [[u['what'], u['result'], u['used']] for u in T['unreached']])}

**Method.** Each panorama is the 8k tone-mapped JPG. A rectilinear view or a flat ground picture is re-projected from it with numpy (`make_previews.py`) **at that panorama's own measured camera height** (section 14; the first draft assumed 1.6 m for all and the 75 mm yellow line did not prove it: PM22). Heights are found from angles (`measure.py`: a vertical face at ground distance d = h / tan(foot angle) has its top at h - d tan(top angle)). On a ground picture, anything above the plane is smeared outward by (h - plane) / (h - z); the kerb-top picture (camera h - U) is true for things at the kerb-top level. The photographed crossing (urban_street_03) has two main pictures, the ground plane and the kerb-top plane, at 3 mm a pixel; `self_check.py` looks for the drawn edges on them. The raw readings of section 5 (rows, columns, pixels) were taken on the first-draft 1.6 m pictures; `measure.compute` rescales each to its panorama's stated height.

## 3. The frame, the levels, the pivots

* Plan frame: x along the kerb; y across, 0 at the kerb face line (the foot of the face, at the channel), + toward the carriageway, - toward the footway; z up from the top of the channel setts at the kerb foot. [Judgement]
* Levels: kerb top z = +{N['U']} (granite); footway flags +{N['FLAGS_Z']} (5 below the kerb top; Photo: a visible joint, little step; Judgement for the 5); the road at the channel edge +6 and rising 1 in 40, +75 at 3 m (Read: scene). The asphalt edge stands 6 mm up on the setts and is ragged. [Photo, Judgement]
* Pivots: kerb block at the block centre on the face line at channel level; the crossing assembly at the centre of the gap between the two end blocks, y = 0, z = 0; grates and covers at the centre of the lid at its top surface; the corner at the corner point on the face line.
* Units in the glb: metres (divide by 1000), z up, scale 1; one mesh per piece kind, variants as material slots or separate meshes.

## 4. The target, part by part

Every number carries its kind: **Read** (printed in the repository), **Scaled** (measured off a drawing: none here), **Photo** (measured on a photograph: method and error in section 5), **Derived** (computed from the others), **Judgement** (a trade or period guess, said so).

### 4.1 Granite kerb block (`kerb_granite`; about 85 % of the run)

Section in the plan frame (points in `target.json` `pieces.kerb_granite.section_yz`, y then z):

`{json.dumps(P['kerb_granite']['section_yz'])}`

* Upstand {N['U']} (Photo at the corrected height: PM01 and PM02 read 107 and 102 to the arris middle, which stands 8 below the top; the scene's 125 Read is outside the error, so the photographs win). **Upstand and batter are one measurement, not two:** PM01, PM02 and PM26 all read the same ray, from the camera to the middle of the arris, against the same foot; upstand and set-back trade about 0.39 mm of height per mm of set-back and the three readings disagree by about 12 mm. Read with a vertical face the ray puts the arris middle at about 104 to 116 mm, and the review at two places read 116 and 120 with a vertical face and 107 to 111 with a 25 mm batter (all at the corrected height), so {N['U']} with a {N['BATTER']} mm batter stands [Photo-consistent with PM26 and the upstand together, not separately measured; Judgement for the split]. Top width {N['TOPW']}, face line to the rear joint (Photo PM01 163, PM02 167, PM25 170; error +-10). Depth 255, the lower {N['DEPTH'] - N['U']} buried (Read: the street's 255).
* Face HALF-BATTERED: vertical from the foot to z = {N['VERT_Z']}, then sloping back {N['BATTER']} mm by z = {N['U'] - N['ARRIS_R']}, then the top arris rounded R {N['ARRIS_R']} (centre y = -{N['BATTER'] + N['ARRIS_R']}, z = {N['U'] - N['ARRIS_R']}) into a flat top {N['TOPW'] - N['BATTER'] - N['ARRIS_R']} wide (Photo-consistent with PM26: the arris middle stands 26 +-9 behind the foot line, the model's is 27; Judgement for the split with the upstand, see above). The rear face vertical. The end arris R {N['END_R']}. [Photo; Judgement for {N['VERT_Z']} and R {N['ARRIS_R']}]
* Length: random in {N['LEN_MIN']} to {N['LEN_MAX']}, mean {N['LEN_MEAN']}, never two neighbours within 20 (Photo PM04: 0.75, 0.91, 1.03 m, +-30). Joint {N['JOINT']} +-3, open and silt-dark, no mortar fillet on the face (Photo PM05). Laying scatter: face line +-4 between neighbours, top level +-3, tilt up to 1.5 degrees; one joint in twelve opens to 15. [Photo, Judgement]
* Surface: top fine-picked granite, grain 1 to 3 mm, polished at the front half by tyres and feet; face self-faced, rougher and darker with grime; end faces dressed with chipped edges. [Photo]
* Pieces needed: straight block (random length), end block (square end, arris R {N['END_R']}), the crossing's two end blocks, the corner blocks (4.5).

### 4.2 Concrete kerb block (`kerb_concrete`; three runs of 4 to 8 blocks per side, about 20 m of the 96 m of kerb)

Section (y, z): `{json.dumps(P['kerb_concrete']['section_yz'])}`

* Bullnosed: upstand {N['CU']}, top width {N['CW']}, front arris a full rounding R {N['CR']} over the top {N['CR']}, flat top {N['CW'] - N['CR']}, depth 255 ({N['DEPTH'] - N['CU']} buried). Length 915 (Read: the street's block), joint 8 pointed flush, cracked in places. [Photo PM03 at the corrected height 1.165 m: upstand 70 to the arris middle (the top about 85 to 88), width 122 at the measured upstand, a re-surfaced street; the bollards' writer measured the footway 0.105 above the road here: {N['CU']} between them; Judgement for R {N['CR']}]
* Surface: weathered concrete with fine aggregate showing and sparkling, paint blips allowed (the lines family places them). [Photo]
* The standard it comes from (a search lead, not read): BS 7263 Part 1 (1990), types HB2 and BN2 (125 x 255 x 915): the corrected width is the same 125.

### 4.3 Channel

* **Granite sett channel** (beside the granite kerb): two courses, long side along the kerb. Course A (kerb side) y 0 to {N['CH_A']}, B {N['CH_A']} to {N['CH_W']}; total {N['CH_W']} [Photo PM06: 226 at 1.6 m x 0.90 = 204 +-15; Read: the scene's 255 is kept for the concrete channel]. Sett along the kerb {N['SETT_MIN']} to {N['SETT_MAX']}, mean {N['SETT_MEAN']} [Photo]; joints {N['SETT_JOINT']} with dark mortar recessed about 8, one joint in four open to 20 [Photo]. Top z = 0, domed 4 mm, level scatter 3, course B up to 5 lower where worn [Judgement]. The asphalt edge at y = {N['CH_W']}, 6 mm proud, ragged by 10 to 50; over about a third of a run the asphalt laps 30 to 50 onto course B (so the visible channel is then about 150 to 175; in front of the crossing course B shows to {N['CH_W']}), and the setts stay modelled to {N['CH_W']} underneath [Photo, review]. Long fall 1 in 80 toward the gully, cross-section flat [Judgement].
* Profile (y, z): the channel top is flat at z = 0 from y 0 to {N['CH_W']}; the asphalt edge rises to 6 at y {N['CH_W']} and 6.9 at y {N['CH_W'] + 35}; the road is z = 6 + (y - {N['CH_W']}) / 40 up to 76 at 3000 (the crown 75 mm above the channel: Read, scene). Point lists: `pieces.channel_setts.profile_yz`.
* **Concrete channel block** (beside the concrete kerb): 255 across, 125 deep, 915 long, joint 8 [Read: the scene's 255 and "the kerb's own concrete"; Judgement: BS 7263 channel 255 x 125, a lead].
* Colour of the setts: `colour_share` sett_pale_worn 0.35, sett_dull 0.50, granite_blue_grey 0.15 (the three materials of section 7). The clean mix averages about 1.78 times the road in linear light; after the wear family's channel body (x 0.85) about 1.51, and about 1.45 with the dark joints, inside the 1.35 to 1.7 of [Read: wear target M24] and of check `channel_over_road_brightness`.

### 4.4 The dropped crossover (`crossover`; one on the street, west side, x 22.5)

As photographed in urban_street_03 (a house crossing, {REF['gap'] / 1000:.2f} m between the kerb ends at the corrected height; the street's yard entrance takes the same form at 3.0 m [Read: scene]). From the footway to the road, in the plan frame:

| part | numbers (mm) | kind |
|---|---|---|
| end blocks | two granite kerb blocks, square vertical end faces, arris R {N['END_R']}, gap between their faces 3000 (the photograph {REF['gap']} +-30) | Read; Photo PM10 |
| flank strips | granite, {N['FLANK_W']} wide (stone between joints: left 154, right 127), y -{N['RAMP_BACK']} to -{N['FLANK_Y1']} ({N['RAMP_BACK'] - N['FLANK_Y1']} long), top z {N['FLAGS_Z']}; right strip's inner face on the block end, the left strip's inner face splayed, a dark band about 40 wide; joint to the ramp and to the kerb 12 | Photo PM12; Judgement (the one-of-each choice) |
| ramp | x from -1488 to +1488, y -{N['RAMP_BACK']} to -{N['RAMP_FRONT']}, in-situ concrete, z {N['LIP_Z']} at the front rising to {N['FLAGS_Z']} at the back ({N['RAMP_RISE']} over {N['RAMP_RUN']}, 1 in {N['RAMP_RUN'] / N['RAMP_RISE']:.1f}), brushed with exposed fine aggregate, one hairline crack across, a 10 to 20 bitumen or mortar joint to the flags at the back | Photo PM11 ({N['RAMP_BACK']} against 846 +-40); Derived |
| lip row | y -{N['LIP_W']} to 0, setts {N['LIP_SETT']} along (+{N['LIP_JOINT']} joint, {N['LIP_N']} setts, pitch {3000 / N['LIP_N']:.1f}), {N['LIP_W']} across, top z {N['LIP_Z']} above the channel, blue-grey, pale grey and one pink-grey in 8 | Photo PM07 (154), PM08 (112), PM09 (11 +-8) |
| joints | 12 mm bitumen between ramp, lip and flank strips | Judgement; Photo (dark lines) |
| footway beyond | flags at z {N['FLAGS_Z']} | Judgement |

The scene's 6 mm upstand is the modern flush figure; the photographed lip stands about {N['LIP_Z']} above the channel setts. The scene's "one taper block" is kept as a **variant** (`taper_variant`): a precast concrete dropper 915 long, {N['TAPER_W']} wide, top from z {N['CU']} falling to 5 (1 in {915 / (N['CU'] - 5):.1f}), one per side, to be used only if the builder wants a precast crossing [Judgement: a search lead names BS 7263 HB2-to-BN3 droppers at 1:9; no photograph of one was reached].

### 4.5 Corners

* **Mitred corner** (`kerb_corner_mitre`): two granite arms of 900 mitred at the bisector, interior angle 133 +-5 degrees (Photo PM27: the kerb's road edges run at 57 and 11 degrees and the yellow lines at 61 and 13 to 16 on the ortho, giving 134 and 133.5; an angle, so the camera height does not change it; 90 allowed for a street corner), joint 9, arris rounding carried round the mitre, a small chip at the corner [Photo urban_street_01: a build-out; its kerb is new, so cleaner than 1990].
* **Radius corner** (`kerb_corner_radius`): face radius {N['CORNER_R']} (Photo PM16: the yellow line fits 6.8 m at 1.6 m, 6.4 m at the corrected 1.50 m, 0.2 m off the kerb, +-0.6 m); granite blocks cut to the curve, {N['CORNER_CHORD']} along the arc (Judgement from the photograph's 1.2 to 1.3 m), joints radial 9; the two sett courses follow the curve with wedge-shaped setts. [Photo urban_street_04]
* Neither is in today's street; place them at a build-out or at a cross-street if the town gets one.

### 4.6 Gully grate A (`gully_grate_A`: the street's grate, east side x 12.0 [Read])

| number | value | kind |
|---|---|---|
| overall along the kerb x across | {N['GA_L']} x {N['GA_W']} | Photo PM13: 489 x 324 at 1.6 m x 0.90 = 440 x 292 +-9 |
| slots | 8, each {N['GA_SLOT_W']} wide x {N['GA_SLOT_L']} long, pitch {N['GA_PITCH']}, slot field {N['GA_SPAN']} (7 x {N['GA_PITCH']} + {N['GA_SLOT_W']}) | Photo PM14 (field 289 px = 390 at the corrected height), PM28 (slots 23 to 31, median 26), PM30 (pitch 51.3, centre fitted to 1 mm) |
| end walls | {N['GA_END_ALONG']} along the kerb, {N['GA_END_ACROSS']} across | Derived |
| bars | {N['GA_BAR']} wide (22 to 26 on the photograph), 45 deep (z), tops chamfered 2, slot {N['GA_SLOT_W']} at the top narrowing to {N['GA_SLOT_W'] - 4} (casting draught) | Photo PM28; Judgement (45, 2, 4) |
| open area | slot area over plan area, 8 x {N['GA_SLOT_W']} x {N['GA_SLOT_L']} / ({N['GA_L']} x {N['GA_W']}) = {N['GA_OPEN']} +-0.04 (the photograph's black fraction is about 0.41; a ratio, so the camera height does not change it); the grate reads about half iron, not two-thirds | Derived; Photo PM28 |
| slot direction | across the channel, perpendicular to the kerb | Photo |
| position | kerb-side edge y {N['GA_Y0']}, far edge y {N['GA_Y1']}: {N['GA_Y0']} mm from the kerb foot, {N['GA_Y1'] - N['CH_W']} of it beyond the {N['CH_W']} channel in the carriageway | Photo (92 to 383) |
| set in | top flush with the setts (z 0 +-3); the asphalt dished 15 mm toward the grate over 150 on the carriageway side; the yellow line kinks around it (the lines family) | Photo; Judgement for 15 |
| pot | black void 300 deep below the slots, silt at the bottom, so the slots read black | Judgement |

The scene's 400 square, recess 50 and dish 30 are replaced (section 6). **Grate B** (`gully_grate_B`, optional second design): 7 slots {N['GB_SLOT_W']} wide at pitch {N['GB_PITCH']} (bars {N['GB_BAR']}) whose lengths {', '.join(str(x) for x in N['GB_LENGTHS'])} trim the field to an oval, in a frame {N['GB_L']} x {N['GB_W']}, with two round lifting holes {N['GB_HOLE']} across on the long axis about {N['GB_HOLE_OFF']} beyond the centres of the two end slots; raised marks cast on its centre bar stay blank [Photo, rough: a perspective view at 3.5 m, +-15 %, at the corrected 1.165 m].

### 4.7 Covers (four cast patterns, as the asset plan wants, plus small lids)

* **P1 double-triangular square-stud cover** (`cover_stud_square`): outer {N['STUD_OUT']} square (Photo PM18: about 980 x 920 at 1.6 m, 612 x 575 at the corrected 1.00 m, +-45; the cover is 0.9 m from the nadir), frame rim {N['STUD_RIM']}, lid {N['STUD_OUT'] - 2 * N['STUD_RIM']} square, **two triangular leaves** split on one diagonal joint {N['STUD_JOINT']} mm wide, 10 x 10 raised square studs {N['STUD']} across at pitch {N['STUD_PITCH']} (margin {N['STUD_MARGIN']}), {N['STUD_H']} high with 15 degree draught and 1 mm worn arrises; the studs the joint crosses are cut into right-angled half-studs on both leaves (at least five visible along it); one round keyhole {N['STUD_KEYHOLE']} across per leaf near the middle of the leaf; a small raised blank oblong boss {N['STUD_BOSS'][0]} x {N['STUD_BOSS'][1]} x {N['STUD_BOSS'][2]} near the joint's lower end, where a maker's mark would go (it stays blank); no lifting pockets; gap to the surround 10, block paving or flags cut to it. [Photo PM17: lattice 61 and 57 at right angles; PM18; the review of bethnal_green_entrance for the split, count, keyhole and boss; Judgement for the second keyhole and the heights.] Two on the street, footway or carriageway.
* **P2 round 600 cover** (`cover_round_600`): frame outer diameter 690, lid 590, frame depth 68, ring 50, a centred lug lattice, lugs 36 x 10.5 x 2.5 high, each 71.4 x 83.5 cell holding 2 horizontal lugs at (0, 0) and (35.7, 41.75) and 2 vertical lugs at (35.7, 6) and (0, 47.75) (centres in mm; rows 41.75 apart, a horizontal and a vertical lug alternating every 35.7 along a row, each row shifted 35.7; `pattern.lugs_in_cell`, which `target_drawing.py` reads), a plain 25 band at the rim. [Read from the CC0 Poly Haven model: 690.76 overall, 67.62 deep, lid radius 294.1 (PM24); the lug lattice is read off the displacement map of a CC0 scan of a real tread plate (PM23, the review's reading); neither involves a camera height; Judgement for the 600 class.] No lettering. Two in the carriageway.
* **P3 recessed infill cover**: *footway* `cover_recessed_footway`, telecom-style and blank: outer {N['FW_OUT'][0]} x {N['FW_OUT'][1]}, a cast frame whose top is cast with raised oblong lugs (36 x 10.5 x 2.5, rows 41.75 apart: two staggered rows along each long side, three columns across the wider left end and two across the right) in two bands, an outer {N['FW_FLANGE']} wide level with the flags and an inner {N['FW_LEDGE']} wide stepped {N['FW_STEP']} down [Photo for the pattern, a 7 m telephoto that cannot measure the lug; Judgement for the size and counts], infill {N['FW_IN'][0]} x {N['FW_IN'][1]} (a pale flag or concrete tray lid, {N['FW_CHAMFER']} chamfer, top 8 below the flags). [Photo PM19 at the corrected 1.44 m: 1064 x 602 outer (+-45 along, +-90 across, seen at 7 m), infill 864 x 378, rim 113 on the left]. *Carriageway* `cover_recessed_road`: {N['RD_OUT'][0]} x {N['RD_OUT'][1]} filled with tarmac, only a {N['RD_HAIR']} dark hairline in the surface, a darker square, grass and moss at the corners, a crack running out of one corner [Photo PM20 at the corrected 1.01 m: 666 x 695 +-40].
* **P4 two-leaf road cover** (`cover_road_double_leaf`): {N['DL_OUT'][0]} x {N['DL_OUT'][1]}, two leaves with a 15 gap across the middle, fine stud tread (studs {N['DL_STUD']} on a 45 degree lattice at pitch {N['DL_PITCH']}, 3 high, margin {N['DL_MARGIN']}), a {N['DL_SURR']} band of pale mortar and lighter tarmac round it. [Photo PM21 at the corrected 1.50 m: 1710 x 563 +-140 at 7 m: shape and pattern only. The leaf split is **Judgement, not Photo**: on a 4 mm ortho the studded field is divided by more than one seam, at least one oblique to the long axis, and no single cross-joint at the middle was seen; its period is unproven (it sits in a fresh reinstatement), so one on the street.]
* **Small lids** (`service_small`), 3 stopcock, 2 gas, 1 telecom: stopcock round lid 135 in a 175 frame with a 30 x 8 slot [Judgement]; gas 240 x 130 lid in a 290 x 180 frame with a 25 x 8 slot at each end [Judgement]; telecom blank {N['TC_LID'][0]} x {N['TC_LID'][1]} recessed lid with flag infill in a {N['TC_FRAME'][0]} x {N['TC_FRAME'][1]} frame with a {N['TC_SURR']} pale mortar surround [Photo urban_street_04 at the corrected 1.50 m, +-30 %].
* **Lettering**: none on anything. If a letter is ever wanted: "SV", "WATER" or "GAS", 20 high, cast, no maker, no company; only once a photograph shows it. No maker's name, council name, crest, crown or cypher on any cover or grate. [Brief; canon owes the council's name]
* Every cover and grate top is flush with the surface it is set in (+-3), except the footway infill (8 below the flags, +-3).

### 4.8 Pieces and counts for the street (Judgement)

Covers 10 to 14: P1 x 2, P2 x 2, P3 footway x 2 and road x 1, P4 x 1, small lids x 6 (3 stopcock, 2 gas, 1 telecom blank). Grates 1 (the scene's, east x 12) to 3. Kerb 96 m (both sides of 48 m), crossing 1 (west x 22.5), corners 0 to 2.

### 4.9 Tactile paving: what the period did

None on Quay Street in 1990. The search summaries (leads, not read: the Department's guidance sits on gov.uk, which refused) say the blister surface was first laid at a crossing in Parliament Square in 1983 as a trial of research for the Department of Transport, and that the Department's guidance on tactile paving dates from 1998; a minor street's dropped kerb in 1990 has plain flags or concrete. No blister, no corduroy, no yellow or red surface at the crossing. (The asset plan reached the same view: "leave the cone off".) [Judgement, with leads]

## 5. Photograph measurements (raw readings recomputed by `self_check.py`)

The raw readings (rows, columns, pixels) were taken on the first-draft pictures drawn at an assumed 1.6 m; **the results below are rescaled to each panorama's measured camera height** (section 14: the `camera_height_m` stored with each measurement), by `measure.compute`. Their errors are the reading's own (stated) plus the camera height's (4 to 7 %).

{pm_table()}

## 6. Where the photographs win over the scene and the books

{win_table()}

## 7. Materials and colours (sRGB, clean surfaces; the grime, shade and wet are the wear family's)

All albedos are on the wear target's road scale (asphalt_dry 89/86/80 [Read]): each photograph colour is divided by the road beside it in linear light and multiplied by 89/86/80. **Gully-grate iron has ONE base colour, the wear target's iron_grate 58/54/52 [Read]; the rust comes from the wear target's grate_wear (mark 100/72/56). The 92/74/66 of the first draft is now only the EXPECTED composite on the bars (the photograph reads 88/75/76 to 125/109/103), kept to check the result, so the rust is not put on twice.** Metal is 1 for bare iron; the rust skin is dielectric, so use metal 0.3 where rust covers more than half a surface. Wet: roughness falls and albedo darkens by the wear target's wet rows (grate_wear 0.85, roughness -0.3; gutter_grime 0.8, roughness -0.55): nothing is darkened twice.

{mat_table()}

Colours as seen on the photographs (tone-mapped, not albedo): kerb tops 138/135/138 and 153/152/161, the kerb face in shade 38/38/35, the road 97/95/101, the ramp 161/153/148, lip setts 109/114/129 (blue-grey) and 157/156/160 (pale), channel setts 153/147/149 and 115/108/109, grate bars 88/75/76 and the slots 35/31/37, Bethnal Green's cover plate 112/95/85 under leaf litter.

## 8. Variants

{bullets(T['variants'])}

## 9. Wear and damage as the photographs show it

{bullets(T['wear'])}

## 10. Why each object is the same in 1990, or what differs

* **Granite kerbs and setts** (urban_street_03, 01, 04): dressed granite kerbs and sett channels were laid from the 19th century to the 1970s and kept; the same in 1990, but dirtier and sootier, and older kerbs are more often chipped and tilted. What differs: the 2010s build-out in urban_street_01 is new sawn granite (cleaner); the 2019 streets have been swept by machine more often than a 1990 channel.
* **Concrete kerb** (Birbeck Street): bullnosed concrete kerbs were laid from the 1960s; the same. BS 7263 Part 1 (1990, a lead) is the year's standard for the precast sections.
* **Crossover** (urban_street_03): ramp-and-flank crossings with a sett lip are 1970s-80s practice; the same. What differs from 2019 practice: no precast dropper blocks, no tactile blisters at the crossing, a steep ramp (1 in {N['RAMP_RUN'] / N['RAMP_RISE']:.1f}), a lip you can feel ({N['LIP_Z']} mm, not 6).
* **Gully grate**: cast-iron gratings to BS 497 (1976, superseded 1994 by BS EN 124: a lead) were the 1990 norm; the photographed rust-brown cast grates look old and are the same. What differs: no hinged ductile-iron or galvanised "safe" grates, no anti-theft or cycle-slot patterns of the 2000s.
* **Covers**: cast or steel square-stud and tread covers and recessed infill covers are 1960s-90s; the same. What differs: no composite or plastic covers (2000s), no polymer-concrete lids, no coloured plastic stopcock caps, no operator logos.
* **Tactile paving**: absent in 1990 (4.9).
* **Poly Haven round-cover model and tread scan**: not photographs of a street; their age is unknown; the 600 class and the lug tread are 20th-century standard.

## 11. Checks the builder's automatic check must pass (unit 3.7)

The full list is in `target.json` under `checks` ({len(T['checks'])} checks). Each is a name, what to measure, the expected value and the tolerance:

{check_table()}

The edges `self_check.py` looked for on the main photographs (the drawing laid on the ground picture and on the kerb-top picture; scale fitted on one dimension only):

{probe_table()}

## 12. What the target could not settle

""" + '\n'.join('* ' + s for s in T['could_not_settle']) + f"""

## 13. What to read once the network opens

""" + '\n'.join('* ' + s for s in T['to_read_when_the_network_opens']) + f"""

## 14. Camera heights corrected, 9 October

The bollards' writer and reviewer (production/cloud-week/targets/bollards/: TARGET.md section 3, calibrate.py, anchors.json, TARGET-REVIEW.md) showed that none of Poly Haven's London panoramas was taken at 1.6 m: all sit 0.9 to 1.5 m above their own ground. This target had assumed 1.6 m for every panorama, so **every size it read off a picture was too large** (a length on a flat plane read at an assumed 1.6 m is the true length times 1.6 / h). Each panorama's height was therefore measured again on its own, at the ground its measurements sit on, and every photograph-derived number corrected; angles, counts, ratios, Read numbers and the two asset-based numbers (the Poly Haven round-cover model and tread texture, which carry their own metric size) do not change.

**Methods** (`calibration_data.py`, `calibrate.py`; raw rows in `target.json` `calibration`): (1) **brick courses by the horizon method**, the bollards' writer's method, re-run on their anchors for urban_street_01, 02, bethnal_green_entrance and birbeck_street_underpass (their rows reproduce to 0.0 %), and applied to five new walls on urban_street_03: in a levelled equirectangular panorama the horizon is the middle row, the courses of a vertical wall are evenly spaced in tan(angle), so the camera height above the wall's foot is 75 mm x tan(foot angle) / (course pitch in tan units); the pitch is a Fourier fold of the column band's profile, the foot row read by eye, plus the step of the wall's ground above the ground the measurement sits on. (2) **car wheels**: a tyre of known outer diameter D between a top row and a bottom row gives h = D tan(a_b) / (tan(a_b) - tan(a_t)); used where no brick wall stands on the ground (urban_street_04), and checked on urban_street_03, where it gives 1.46 m against the bricks' 1.43.

{cal_table()}

**The yellow line is not a calibration.** The first draft scaled the panoramas by the 75 mm yellow line (PM22). On urban_street_03 it reads 64 mm (area over length), 72 mm (one cut) or 76 to 82 mm (the review, edges by eye) at an assumed 1.6 m, i.e. 1.46 to 1.87 m if the line is 75 mm: a ragged painted line cannot fix a height, and the bricks and the tyre decide it (1.44 m, which makes the line 58 to 74 mm).

**Every corrected number** (first draft, at an assumed 1.6 m, against the corrected one):

{corr_table()}

`self_check.py` part H recomputes every panorama's height from its own anchors, refuses a stated height that its anchors do not support or that is the first draft's 1.6 m, re-fits the brick pitches from the pictures when the panoramas are at hand, and tests that the scaled corrections equal the first draft x h / 1.6; the previews of the orthos were re-drawn at the corrected heights.

## 15. Narrow points applied after the review

The fresh review (TARGET-REVIEW.md: PASS, 0 faults, 11 narrow points) is applied in full; `self_check.py` enforces the values. **The numbers in this list are the review's, at the assumed 1.6 m; section 14 gives each one at its corrected height (the structure of every point stands).**

1. **Grate A slots and bars**: slot 29 (taper 29 to 25), bar 28, slot span 428, end walls 28.5, open fraction 0.42 +-0.04; PM14 corrected to a 289 px field, PM28 added; check `gully_grate_slots` now 29 +-4 and `gully_grate_open_fraction` added; six slot-edge probes (first, fourth and eighth slots, centre +-14.5, tolerance 6) and a slot-width test from their pairs, with the slot field's centre fitted to the photograph (PM30, x -751, 1 mm).
2. **Cover P1 is a double-triangular two-leaf cover**: outer 960, rim 20, lid 920, 10 x 10 studs (pitch 95, stud 45, margin 10), two triangular leaves on one 5 mm diagonal joint with half-studs along it, a 20 keyhole per leaf, a blank 80 x 40 x 3 boss, no lifting pockets; `cover_stud_square` check now 960 +-60, studs 10, leaves 2; the drawing clips the studs to the leaves.
3. **Cover P2 lugs**: cell 71.4 x 83.5 with `lugs_in_cell` (horizontal (0, 0) and (35.7, 41.75), vertical (35.7, 6) and (0, 47.75)), lug 36 x 10.5; `target_drawing.py` reads them; check `cover_round_tread`.
4. **Cover P3 footway frame** carries raised oblong lugs (P2's 36 x 10.5 x 2.5, rows 41.75 apart, two staggered rows on the long sides, more across the wider left end); `frame_steps` rewritten; the drawing shows them.
5. **Mitred corner about 133 degrees** (PM27 added, 133 +-5, 90 allowed); check `kerb_corner` added (mitre 133 +-5 or 90 +-2, radius 6500 at 1.6 m, 6200 corrected, +-600).
6. **Channel setts colour shares** 0.35 / 0.50 / 0.15, landing the channel at about 1.5 times the road after the wear family's grime; a test computes it.
7. **Handover** (`handover` in target.json): the wear target's gutter_grime band is 0.204 on granite stretches (0.225 at 1.6 m) and 0.255 beside the concrete kerb, the grate is 0.440 x 0.290 (0.485 x 0.325 at 1.6 m), and the grate iron has one base colour, the wear target's iron_grate 58/54/52 (92/74/66 is the expected composite). The line for NOW.md: {T['handover']['for_NOW_md']}
8. **Upstand and batter** reworded as one measurement (4.1 and `face_batter.kind`): Photo-consistent with PM26 and the upstand together, Judgement for the split; checks unchanged.
9. **Asphalt laps course B**: `meets_asphalt` now 10 to 50 wander, the asphalt lapping 30 to 50 onto course B over about a third of a run, the setts modelled to the full channel width beneath (225 at 1.6 m, 204 corrected).
10. **Grate B**: slot 28, bar 30, two 25 lifting holes on the long axis about 55 beyond the end slots, raised centre-bar marks blank; check `gully_grate_B`; kind stays rough.
11. **Cover P4 leaf split** marked Judgement, not Photo; one on the street.

## 16. Files and credit

* This folder: `TARGET.md`, `target.json`, `target_drawing.py`, `self_check.py`, and the scripts that made them (`make_target.py`, `target_data.py`, `measure.py`, `calibration_data.py`, `calibrate.py`, `corrected_numbers.py`, `make_doc.py`, `make_previews.py`). Run order: `make_target.py`, `make_doc.py`, `target_drawing.py OUT_DIR --overlay PREVIEW_DIR`, `self_check.py`. Pictures at 1 mm a pixel go to OUT_DIR (not into git); the reduced previews are in `production/previews/cloud-week/refs/kerbs-and-covers/`.
* **Self-check result** (last run): {SC} (details in `target.json` under `self_check`).
* Previews, all crops of the object only (no people, no shop names, no number plates; a litter wrapper is masked with tarmac in the Birbeck grate view), JPEG at most 1200 px and under 300 KB. Each is derived from a CC0 Poly Haven panorama or texture and credited to its author: **Andreas Mischok** (urban_street_01, 02, 03, 04, bethnal_green_entrance, birbeck_street_underpass; CC0 1.0), **Dimitrios Savva (photography) and Rob Tuytel (processing)** (metal_grate_rusty; CC0 1.0).

{table(['preview', 'source', 'what it shows'], [
    ['ph-urban_street_03-crossover-gully-ortho.jpg', 'urban_street_03, ground plane, 3 mm a pixel', 'THE MAIN PHOTOGRAPH: the crossing, lip, channel setts, gully grate'],
    ['ph-urban_street_03-crossover-top-ortho.jpg', 'urban_street_03, kerb-top plane', 'the same crossing at kerb-top level: flank strips, ramp, kerb tops'],
    ['ph-urban_street_03-target-on-photo.jpg', 'the drawing on the ground picture', 'orange lip setts, green channel setts, magenta grate, cyan slots, white foot line, yellow asphalt edge'],
    ['ph-urban_street_03-target-on-top-photo.jpg', 'the drawing on the kerb-top picture', 'green kerb blocks and flank strips, yellow ramp back edge'],
    ['ph-urban_street_03-granite-kerb-run-view.jpg', 'urban_street_03, yaw 100, pitch -22', 'a straight granite kerb run with sett channel and grate'],
    ['ph-urban_street_03-kerb-end-flank-view.jpg', 'urban_street_03, yaw 281, pitch -21', 'the kerb end, the flank strip and the ramp edge, battered face'],
    ['ph-urban_street_03-gully-grate-ortho.jpg', 'urban_street_03, 1.5 mm a pixel', 'grate A: 8 slots, bars, end walls'],
    ['ph-urban_street_03-footway-cover-ortho.jpg', 'urban_street_03, footway plane', 'recessed telecom-style footway cover'],
    ['ph-urban_street_02-tarmac-infill-cover-ortho.jpg', 'urban_street_02', 'tarmac-filled recessed cover'],
    ['ph-urban_street_04-road-cover-view.jpg', 'urban_street_04', 'two-leaf studded road cover'],
    ['ph-urban_street_04-kerb-corner-radius-ortho.jpg', 'urban_street_04, 10 mm a pixel', 'radius corner of granite kerb'],
    ['ph-urban_street_01-kerb-mitred-corner-ortho.jpg', 'urban_street_01', 'mitred granite corner'],
    ['ph-bethnal_green_entrance-stud-cover-ortho.jpg', 'bethnal_green_entrance, 1.5 mm a pixel', 'square-stud cover'],
    ['ph-birbeck_street_underpass-concrete-kerb-view.jpg', 'birbeck_street_underpass', 'concrete bullnosed kerb'],
    ['ph-birbeck_street_underpass-gully-grate-view.jpg', 'birbeck_street_underpass', 'grate B, oval slot field'],
    ['ph-metal_grate_rusty-tread-pattern.jpg', 'metal_grate_rusty (2k diffuse)', 'basket-weave lug tread'],
    ['target-drawing-sheet.jpg', 'target_drawing.py', 'the drawings: sections, crossing plan, grate, covers, corner'],
])}
"""

open(os.path.join(HERE, 'TARGET.md'), 'w').write(DOC)
print('wrote TARGET.md', len(DOC))
