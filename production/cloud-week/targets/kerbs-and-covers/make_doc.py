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

Today's street (SCENE-SLOTS.md, read 9 October): kerb upstand 125, width 125, depth 255, blocks 915 long, channel course 255 wide, a dropped crossover on the west side at x 22.5 (3.0 wide, 6 mm upstand, one taper block), a gully grate 400 square (recess 50, dish 30) on the east side at x 12.0, crown 75 mm above the channel. These are trade guesses, not photographs.

| | the present street | this target | why |
|---|---|---|---|
| upstand | 125 (Read) | granite 125 kept; concrete 110 | Photo: 113 and 118 to the middle of the arris (125 to the top, PM01, PM02), so the 125 is right; a re-surfaced concrete kerb reads 96 to the arris middle (PM03) |
| kerb top width | 125 | granite 190, concrete 160 | Photo: 181, 185, 189 on granite (PM01, PM02, PM25), 166 on concrete (PM03): the street's 125 is a precast catalogue width, the photographed kerbs are wider |
| face | not stated (vertical) | granite half-battered (25 mm back by z = 100); concrete bullnosed R 60 | Photo PM26: the middle of the arris stands 29 +-9 mm behind the foot line |
| depth | 255 (Read) | 255 kept | unseen; Read |
| block length | 915 for all | granite random 800 to 1200 (mean 1000); concrete 915 | Photo PM04: whole granite blocks 0.84, 1.01, 1.14 m |
| channel | 255, "in the kerb's own concrete" | granite sett channel 225 (two courses) beside granite; concrete block 255 beside concrete | Photo PM06: 226 +-15, setts not concrete; their brightness (1.35 to 1.7 times the road, wear target M24) is unchanged |
| crossover | 3.0 m, 6 mm upstand, one taper block | 3.0 m kept; lip of setts 15 mm; in-situ concrete ramp 1 in 7.4; granite flank strips; the taper block kept as a variant | Photo PM09 to PM12: the photographed crossing has no taper block |
| gully grate | 400 square, recess 50, dish 30 | 485 x 325 rectangle, 8 slots, dish 15 | Photo PM13, PM14 |
| corner | none | mitred (112 degrees) and radius (6500) | Photo urban_street_01, urban_street_04 |
| tactile paving | none | none | period: see 4.9 |

What the present street gets right: the 125 upstand, the 255 depth, the channel course of about a quarter of a metre, a 3.0 m crossing, a gully in the channel on the east side, the crown. What it gets wrong or lacks is in the table above and in section 6.

## 2. Sources

All photographs are Poly Haven's, CC0 (read at https://polyhaven.com/license on 9 October 2026), used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused Wikimedia, Geograph, Flickr, archive.org, gov.uk, BSI and most of the web (list below), so **no photograph from 1975 to 2000 was reached: every photograph is from 2019**, and for each object the table says why it would look the same in 1990 or what differs.

{src_table()}

**Unreached** (a page that refused is not evidence; nothing was taken from any of these):

{table(['what', 'result', 'used'], [[u['what'], u['result'], u['used']] for u in T['unreached']])}

**Method.** Each panorama is the 8k tone-mapped JPG. A rectilinear view or a flat ground picture is re-projected from it with numpy (`make_previews.py`), camera height 1.6 m, proved by the 75 mm yellow line (PM22: 72 mm read, within 4 %). Heights are found from angles (`measure.py`: a vertical face at ground distance d = 1.6 m / tan(foot angle) has its top at 1.6 m - d tan(top angle)). On a ground picture, anything above the plane is smeared outward by 1600 / (1600 - z); the kerb-top picture (camera 1.475 m) is true for things 125 mm up. The photographed crossing (urban_street_03) has two main pictures, the ground plane and the kerb-top plane, at 3 mm a pixel; `self_check.py` looks for the drawn edges on them.

## 3. The frame, the levels, the pivots

* Plan frame: x along the kerb; y across, 0 at the kerb face line (the foot of the face, at the channel), + toward the carriageway, - toward the footway; z up from the top of the channel setts at the kerb foot. [Judgement]
* Levels: kerb top z = +125 (granite); footway flags +120 (5 below the kerb top; Photo: a visible joint, little step; Judgement for the 5); the road at the channel edge +6 and rising 1 in 40, +75 at 3 m (Read: scene). The asphalt edge stands 6 mm up on the setts and is ragged. [Photo, Judgement]
* Pivots: kerb block at the block centre on the face line at channel level; the crossing assembly at the centre of the gap between the two end blocks, y = 0, z = 0; grates and covers at the centre of the lid at its top surface; the corner at the corner point on the face line.
* Units in the glb: metres (divide by 1000), z up, scale 1; one mesh per piece kind, variants as material slots or separate meshes.

## 4. The target, part by part

Every number carries its kind: **Read** (printed in the repository), **Scaled** (measured off a drawing: none here), **Photo** (measured on a photograph: method and error in section 5), **Derived** (computed from the others), **Judgement** (a trade or period guess, said so).

### 4.1 Granite kerb block (`kerb_granite`; about 85 % of the run)

Section in the plan frame (points in `target.json` `pieces.kerb_granite.section_yz`, y then z):

`{json.dumps(P['kerb_granite']['section_yz'])}`

* Upstand 125 (Photo, PM01, PM02: 118 and 113 to the arris middle, which stands 7 below the top; the street's 125 Read). Top width 190, face line to the rear joint (Photo PM01 181, PM02 185, PM25 189; error +-10). Depth 255, the lower 130 buried (Read: the street's 255).
* Face HALF-BATTERED: vertical from the foot to z = 45, then sloping back 25 mm by z = 100 (about 25 degrees from vertical), then the top arris rounded R 25 (centre y = -50, z = 100) into a flat top 140 wide (Photo PM26: the arris middle stands 29 +-9 behind the foot line; the model's is 32). The rear face vertical. The end arris R 10. [Photo; Judgement for 45 and R 25]
* Length: random in 800 to 1200, mean 1000, never two neighbours within 20 (Photo PM04: 0.84, 1.01, 1.14 m, +-30). Joint 9 +-3, open and silt-dark, no mortar fillet on the face (Photo PM05). Laying scatter: face line +-4 between neighbours, top level +-3, tilt up to 1.5 degrees; one joint in twelve opens to 15. [Photo, Judgement]
* Surface: top fine-picked granite, grain 1 to 3 mm, polished at the front half by tyres and feet; face self-faced, rougher and darker with grime; end faces dressed with chipped edges. [Photo]
* Pieces needed: straight block (random length), end block (square end, arris R 10), the crossing's two end blocks, the corner blocks (4.6).

### 4.2 Concrete kerb block (`kerb_concrete`; three runs of 4 to 8 blocks per side, about 20 m of the 96 m of kerb)

Section (y, z): `{json.dumps(P['kerb_concrete']['section_yz'])}`

* Bullnosed: upstand 110, top width 160, front arris a full rounding R 60 over the top 60, flat top 100, depth 255 (145 buried). Length 915 (Read: the street's block), joint 8 pointed flush, cracked in places. [Photo PM03: upstand 96.5 to the arris middle, width 166 at the measured upstand, a re-surfaced street; Judgement for R 60]
* Surface: weathered concrete with fine aggregate showing and sparkling, paint blips allowed (the lines family places them). [Photo]
* The standard it comes from (a search lead, not read): BS 7263 Part 1 (1990), types HB2 and BN2 (125 x 255 x 915). The photographed kerbs are wider than 125 (above).

### 4.3 Channel

* **Granite sett channel** (beside the granite kerb): two courses, long side along the kerb. Course A (kerb side) y 0 to 115, B 115 to 225; total 225 [Photo PM06: 226 +-15; Read: the scene's 255 is kept for the concrete channel]. Sett along the kerb 130 to 230, mean 180 [Photo]; joints 12 with dark mortar recessed about 8, one joint in four open to 20 [Photo]. Top z = 0, domed 4 mm, level scatter 3, course B up to 5 lower where worn [Judgement]. The asphalt edge at y = 225, 6 mm proud, ragged by 10 to 30 [Photo]. Long fall 1 in 80 toward the gully, cross-section flat [Judgement].
* Profile (y, z): the channel top is flat at z = 0 from y 0 to 225; the asphalt edge rises to 6 at y 225 and 7.0 at y 260; the road is z = 6 + (y - 225) / 40 up to 75.4 at 3000 (the crown 75 mm above the channel: Read, scene). Point lists: `pieces.channel_setts.profile_yz`.
* **Concrete channel block** (beside the concrete kerb): 255 across, 125 deep, 915 long, joint 8 [Read: the scene's 255 and "the kerb's own concrete"; Judgement: BS 7263 channel 255 x 125, a lead].
* Brightness: after the wear family's grime the channel reads 1.35 to 1.7 times the road beside it [Read: wear target M24]. The clean setts' colours are in section 7.

### 4.4 The dropped crossover (`crossover`; one on the street, west side, x 22.5)

As photographed in urban_street_03 (a house crossing, 2.15 m between the kerb ends; the street's yard entrance takes the same form at 3.0 m [Read: scene]). From the footway to the road, in the plan frame:

| part | numbers (mm) | kind |
|---|---|---|
| end blocks | two granite kerb blocks, square vertical end faces, arris R 10, gap between their faces 3000 (the photograph 2145 +-30) | Read; Photo PM10 |
| flank strips | granite, 155 wide (stone between joints: left 171, right 140), y -917 to -202 (715 long), top z 120; right strip's inner face on the block end, the left strip's inner face splayed, a dark band 45 wide; joint to the ramp and to the kerb 12 | Photo PM12; Judgement (the one-of-each choice) |
| ramp | x from -1488 to +1488, y -917 to -137, in-situ concrete, z 15 at the front rising to 120 at the back (105 over 780, 1 in 7.4), brushed with exposed fine aggregate, one hairline crack across, a 10 to 20 bitumen or mortar joint to the flags at the back | Photo PM11 (917 against 924 +-40); Derived |
| lip row | y -125 to 0, setts 170 along (+10 joint, 17 setts, pitch 176.5), 125 across, top z 15 above the channel, blue-grey, pale grey and one pink-grey in 8 | Photo PM07 (171), PM08 (125), PM09 (12 +-8) |
| joints | 12 mm bitumen between ramp, lip and flank strips | Judgement; Photo (dark lines) |
| footway beyond | flags at z 120 | Judgement |

The scene's 6 mm upstand is the modern flush figure; the photographed lip stands 12 to 20 above the channel setts. The scene's "one taper block" is kept as a **variant** (`taper_variant`): a precast concrete dropper 915 long, 160 wide, top from z 110 falling to 5 (1 in 8.7), one per side, to be used only if the builder wants a precast crossing [Judgement: a search lead names BS 7263 HB2-to-BN3 droppers at 1:9; no photograph of one was reached].

### 4.5 Corners

* **Mitred corner** (`kerb_corner_mitre`): two granite arms of 900 mitred at the bisector, interior angle 112 degrees (90 allowed), joint 9, arris rounding carried round the mitre, a small chip at the corner [Photo urban_street_01: a build-out; its kerb is new, so cleaner than 1990].
* **Radius corner** (`kerb_corner_radius`): face radius 6500 (Photo PM16: the yellow line fits 6.8 m, 0.2 m off the kerb, +-0.6 m); granite blocks cut to the curve, 1200 along the arc (Photo: about 1.3 m), joints radial 9; the two sett courses follow the curve with wedge-shaped setts. [Photo urban_street_04; Judgement for the block length]
* Neither is in today's street; place them at a build-out or at a cross-street if the town gets one.

### 4.6 Gully grate A (`gully_grate_A`: the street's grate, east side x 12.0 [Read])

| number | value | kind |
|---|---|---|
| overall along the kerb x across | 485 x 325 | Photo PM13: 489 x 324 +-9 |
| slots | 8, each 18 wide x 285 long, pitch 57, slot field 417 | Photo PM14 (pitch 57 +-3, slot length 285 +-8) |
| end walls | 34.0 along the kerb, 20.0 across | Derived |
| bars | 39 wide, 45 deep (z), tops chamfered 2, slot 18 at the top narrowing to 14 (casting draught) | Photo (bars 39); Judgement (45, 2, 14) |
| slot direction | across the channel, perpendicular to the kerb | Photo |
| position | kerb-side edge y 100, far edge y 425: 100 mm from the kerb foot, 200 of it beyond the 225 channel in the carriageway | Photo (102 to 426) |
| set in | top flush with the setts (z 0 +-3); the asphalt dished 15 mm toward the grate over 150 on the carriageway side; the yellow line kinks around it (the lines family) | Photo; Judgement for 15 |
| pot | black void 300 deep below the slots, silt at the bottom, so the slots read black | Judgement |

The scene's 400 square, recess 50 and dish 30 are replaced (section 6). **Grate B** (`gully_grate_B`, optional second design): 7 slots 20 wide at pitch 58 whose lengths 125, 250, 350, 395, 350, 250, 125 trim the field to an oval, in a frame 490 x 445 [Photo, rough: a perspective view at 3.5 m, +-15 %].

### 4.7 Covers (four cast patterns, as the asset plan wants, plus small lids)

* **P1 square-stud cover** (`cover_stud_square`): outer 860 square, rim 45, lid 770 square, 8 x 8 raised square studs 45 across at pitch 95, 4 high with 15 degree draught and 1 mm worn arrises, margin 30; two oblong lifting pockets 50 x 20 near the middle of opposite edges, silted; gap to the surround 10, block paving or flags cut to it. [Photo PM17: lattice 97.7 and 91.1 at right angles; PM18: 816 and 890 (the cover is 0.9 m from the nadir, +-70); Judgement for the pockets and 4 mm.] Two on the street, footway or carriageway.
* **P2 round 600 cover** (`cover_round_600`): frame outer diameter 690, lid 590, frame depth 68, ring 50, basket-weave lugs 38 x 9 x 2.5 high, one horizontal and one vertical per cell of 71.3 x 83.5, a plain 25 band at the rim. [Read from the CC0 Poly Haven model: 690.76 overall, 67.62 deep, lid radius 294.1 (PM24); the lug cell is the autocorrelation of a CC0 scan of a real tread plate (PM23); Judgement for the 600 class.] No lettering. Two in the carriageway.
* **P3 recessed infill cover**: *footway* `cover_recessed_footway`, telecom-style and blank: outer 1180 x 660, a cast frame with an outer flat flange 45 wide level with the flags and an inner ledge 65 wide stepped 12 down, infill 960 x 440 (a pale flag or concrete tray lid, 25 chamfer, top 8 below the flags). [Photo PM19: 1182 x 669 outer (+-50 along, +-100 across, seen at 7 m), infill 960 x 420, rim 126 on the left]. *Carriageway* `cover_recessed_road`: 1000 x 1050 filled with tarmac, only a 15 dark hairline in the surface, a darker square, grass and moss at the corners, a crack running out of one corner [Photo PM20: 1020 x 1065 +-40].
* **P4 two-leaf road cover** (`cover_road_double_leaf`): 1820 x 620, two leaves with a 15 gap across the middle, fine stud tread (studs 18 on a 45 degree lattice at pitch 33, 3 high, margin 30), a 150 band of pale mortar and lighter tarmac round it. [Photo PM21: 1824 x 600 +-150 at 7 m: shape and pattern only.] One on the street.
* **Small lids** (`service_small`), 3 stopcock, 2 gas, 1 telecom: stopcock round lid 135 in a 175 frame with a 30 x 8 slot [Judgement]; gas 240 x 130 lid in a 290 x 180 frame with a 25 x 8 slot at each end [Judgement]; telecom blank 360 x 160 recessed lid with flag infill in a 410 x 210 frame with a 30 pale mortar surround [Photo urban_street_04, +-30 %].
* **Lettering**: none on anything. If a letter is ever wanted: "SV", "WATER" or "GAS", 20 high, cast, no maker, no company; only once a photograph shows it. No maker's name, council name, crest, crown or cypher on any cover or grate. [Brief; canon owes the council's name]
* Every cover and grate top is flush with the surface it is set in (+-3), except the footway infill (8 below the flags, +-3).

### 4.8 Pieces and counts for the street (Judgement)

Covers 10 to 14: P1 x 2, P2 x 2, P3 footway x 2 and road x 1, P4 x 1, small lids x 6 (3 stopcock, 2 gas, 1 telecom blank). Grates 1 (the scene's, east x 12) to 3. Kerb 96 m (both sides of 48 m), crossing 1 (west x 22.5), corners 0 to 2.

### 4.9 Tactile paving: what the period did

None on Quay Street in 1990. The search summaries (leads, not read: the Department's guidance sits on gov.uk, which refused) say the blister surface was first laid at a crossing in Parliament Square in 1983 as a trial of research for the Department of Transport, and that the Department's guidance on tactile paving dates from 1998; a minor street's dropped kerb in 1990 has plain flags or concrete. No blister, no corduroy, no yellow or red surface at the crossing. (The asset plan reached the same view: "leave the cone off".) [Judgement, with leads]

## 5. Photograph measurements (raw readings recomputed by `self_check.py`)

{pm_table()}

## 6. Where the photographs win over the scene and the books

{win_table()}

## 7. Materials and colours (sRGB, clean surfaces; the grime, shade and wet are the wear family's)

All albedos are on the wear target's road scale (asphalt_dry 89/86/80 [Read]): each photograph colour is divided by the road beside it in linear light and multiplied by 89/86/80. Metal is 1 for bare iron; the rust skin is dielectric, so use metal 0.3 where rust covers more than half a surface. Wet: roughness falls and albedo darkens by the wear target's wet rows (grate_wear 0.85, roughness -0.3; gutter_grime 0.8, roughness -0.55): nothing is darkened twice.

{mat_table()}

Colours as seen on the photographs (tone-mapped, not albedo): kerb tops 138/135/138 and 153/152/161, the kerb face in shade 38/38/35, the road 97/95/101, the ramp 161/153/148, lip setts 109/114/129 (blue-grey) and 157/156/160 (pale), channel setts 153/147/149 and 115/108/109, grate bars 88/75/76 and the slots 35/31/37, Bethnal Green's cover plate 112/95/85 under leaf litter.

## 8. Variants

{bullets(T['variants'])}

## 9. Wear and damage as the photographs show it

{bullets(T['wear'])}

## 10. Why each object is the same in 1990, or what differs

* **Granite kerbs and setts** (urban_street_03, 01, 04): dressed granite kerbs and sett channels were laid from the 19th century to the 1970s and kept; the same in 1990, but dirtier and sootier, and older kerbs are more often chipped and tilted. What differs: the 2010s build-out in urban_street_01 is new sawn granite (cleaner); the 2019 streets have been swept by machine more often than a 1990 channel.
* **Concrete kerb** (Birbeck Street): bullnosed concrete kerbs were laid from the 1960s; the same. BS 7263 Part 1 (1990, a lead) is the year's standard for the precast sections.
* **Crossover** (urban_street_03): ramp-and-flank crossings with a sett lip are 1970s-80s practice; the same. What differs from 2019 practice: no precast dropper blocks, no tactile blisters at the crossing, a steep ramp (1 in 7.4), a lip you can feel (15 mm, not 6).
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

## 14. Files and credit

* This folder: `TARGET.md`, `target.json`, `target_drawing.py`, `self_check.py`, and the scripts that made them (`make_target.py`, `target_data.py`, `measure.py`, `make_doc.py`, `make_previews.py`). Run order: `make_target.py`, `make_doc.py`, `target_drawing.py OUT_DIR --overlay PREVIEW_DIR`, `self_check.py`. Pictures at 1 mm a pixel go to OUT_DIR (not into git); the reduced previews are in `production/previews/cloud-week/refs/kerbs-and-covers/`.
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
