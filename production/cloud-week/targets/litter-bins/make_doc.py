"""Writes TARGET.md from target.json (every number on the page is read from the file; nothing is typed twice).

    /home/user/.bpyenv/bin/python -I make_doc.py
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
T = json.load(open(os.path.join(HERE, 'target.json'), encoding='utf-8'))
OUT = []


def w(s=''):
    OUT.append(s)


def fmt(v):
    if isinstance(v, float):
        return ('%g' % round(v, 3))
    if isinstance(v, list) and v and all(isinstance(x, (int, float)) for x in v):
        return '[' + ', '.join(fmt(x) for x in v) + ']'
    if isinstance(v, list) and v and all(isinstance(x, list) and all(isinstance(y, (int, float)) for y in x) for x in v):
        return '[' + ' '.join('(' + ', '.join(fmt(y) for y in x) + ')' for x in v) + ']'
    return str(v)


def render(v, depth=0, key=None):
    pad = '  ' * depth
    if isinstance(v, dict):
        for k, x in v.items():
            if isinstance(x, (dict, list)) and not (isinstance(x, list) and x and all(isinstance(y, (int, float)) for y in x)) and not (
                    isinstance(x, list) and x and all(isinstance(y, list) and all(isinstance(z, (int, float)) for z in y) for y in x)):
                w('%s- **%s**:' % (pad, k))
                render(x, depth + 1, k)
            else:
                w('%s- **%s**: %s' % (pad, k, fmt(x)))
    elif isinstance(v, list):
        if v and all(isinstance(x, dict) for x in v) and len({tuple(x.keys()) for x in v}) == 1 and all(not isinstance(y, (dict, list)) for x in v for y in x.values()):
            ks = list(v[0].keys())
            w(pad + '| ' + ' | '.join(ks) + ' |')
            w(pad + '|' + '---|' * len(ks))
            for x in v:
                w(pad + '| ' + ' | '.join(str(x[k]).replace('|', '/') for k in ks) + ' |')
        else:
            for x in v:
                if isinstance(x, (dict, list)):
                    w('%s-' % pad)
                    render(x, depth + 1)
                else:
                    w('%s- %s' % (pad, x))
    else:
        w('%s%s' % (pad, v))


w('# Quay Street\'s litter bins and the household dustbin: the exact target')
w()
w('**%s**' % T['summary_line'])
w()
w('Cloud week 42. Written 9 October 2026; **K2 revised 12 October 2026** after one Geograph photograph (S12). `%s`' % T['self_check']['line'])
w()
w('## Files in this folder')
w()
w('- `target.json`: the whole target (units: %s).' % T['units'])
w('- `litter_data.py`, `litter_lib.py`, `make_target.py`, `measure.py`: the author tools (the data, the shared geometry, the writer, the photograph and texture measurements from the cached panoramas).')
w('- `target_drawing.py`: draws every kind\'s elevations, plans and sections, the street plan and a scale sheet from `target.json` alone (`drawing.json` holds the polygons; pictures with `--out DIR`).')
w('- `self_check.py`: %d checks in seven groups (the numbers read from other files, the target\'s own checks computed from its profiles, K2 against its photograph, internal consistency, the drawing, the content rule, the preview files); it writes its result into `target.json`.' % T['self_check']['checks'])
w('- `make_previews.py`, `make_doc.py`: the preview crop and its overlay; this page.')
w('- `TARGET-REVIEW.md`: the one review round (12 October).\n- Previews, in `production/previews/cloud-week/refs/litter-bins/`: `geo974902-southampton-hooded-bin-2008.jpg` (Jim Champion, Geograph 974902, 2008-09-21, CC BY-SA 2.0; cropped to the bin, the council crest sticker painted out) and its `-target-on-photo` overlay (K2\'s profile laid on it at one fitted dimension).')
w()
w('## What changed on 12 October (K2, after one photograph)')
w()
w('The network opened on 11 October. Geograph was searched for litter bins of every year 1975 to 1996 with a dozen terms and for bins on posts and hooded bins without a year: **no 1975 to 1995 photograph of a street litter bin was reached** (forty-nine photographs of any year came back for the year-filtered searches, none of a litter bin); Commons refused every request; archive.org was not searched. One 2008 photograph, S12, shows a hooded glass-fibre bin of a type made since 1984 beside a George V pillar box, which gives its scale; K2 was redrawn from it. **K2 is now a stepped drum**, widest at the base (r 247), a collar (r 230), a plain body (r 210), a groove at z 640 to 664 and a hood skirt (r 218) under a flat shallow dome, the aperture a lipped slot (about 230 x 105, sill 680); the first try\'s generic drum was widest at the middle with the hood the widest part and a narrow foot, the opposite. K1 (the pole-mounted open steel bin) has no photograph: it stays research and judgement.')
w()
w('## The review of 12 October (TARGET-REVIEW.md: PASS, fourteen narrow points, all applied, not re-reviewed)')
w()
w('The one review round Jafar allowed passed the target with fourteen narrow points; each is applied as the reviewer wrote it. **K1:** the bin hangs 232 from the post (216 put the rim bead 8.5 into the post) and the back strap is a tapered spacer bar 21 thick at z 640 and 10 at z 980. **D1:** the three mid-body ribs (a US can\'s) are two rolled rings under the rim at z 530 and 556, the body is plain with 64 vertical flutes 4 deep as a normal map, the side handles are horizontal 12 mm round-bar grips 170 long standing 38 proud on two lugs with two rivets each, the lid has 20 radial ribs (a normal map, one photograph). **K2:** the collar is r 220 (the photograph gives 217), the hood\'s lip at z 640 to 650 (groove 630 to 650), a ragged flush cement patch round the foot (r 290 to 330), the sticker defined as blank or illegible, the height 900 marked Judgement (the photograph gives proportions only: the pillar box beside the bin is of an unestablished type). **Self-check:** the clearance of the K1 bin against its post and spacer is tested; the scale line is reported, not passed. **Wording:** S12\'s period (form assumed unchanged), the stale sill (0.68), the product name out of a data key (`s12_974902`), B3\'s "chandler\'s queue" dropped.')
w()
w('## Sources')
w()
for s_ in T['sources']:
    w('- **%s** %s | read %s | %s | licence %s | taken %s' % (s_['id'], s_['url'], s_['read'], s_['author'], s_['licence'], s_['taken']))
    w('  - what: %s' % s_['what'])
    w('  - used: %s' % s_['used'])
    if s_.get('period'):
        w('  - period: %s' % s_['period'])
w()
w('**Unreached:**')
for u in T['unreached']:
    w('- %s' % u)
w()
w('## The frame')
w()
render(T['frame'])
w()
for k in ('K1', 'K2', 'D1', 'K3'):
    K = T['kinds'][k]
    w('## %s: %s' % (k, K.get('title') or K.get('name')))
    w()
    render({a: b for a, b in K.items() if a != 'title'})
    w()
w('## Placements')
w()
render(T['placements'])
w()
w('## Variants')
w()
render(T['variants'])
w()
w('## Materials')
w()
render(T['materials'])
w()
w('## Wear')
w()
render(T['wear'])
w()
w('## Dressing (overflowing litter: a separate set, never baked into a bin)')
w()
render(T['dressing'])
w()
w('## Photographs, books and the asset plan disagree')
w()
render(T['photographs_win'])
w()
w('## Photograph measurements')
w()
render(T['photo_measurements'])
w()
w('## Calibration')
w()
render(T['calibration'])
w()
w('## Panoramas looked at')
w()
render(T['panoramas_looked_at'])
w()
w('## Leads (search summaries: never numbers)')
w()
render(T['leads'])
w()
w('## What the target could not settle')
w()
for c in T['could_not_settle']:
    w('- %s' % c)
w()
w('## To read when more of the network answers')
w()
for c in T['to_read_when_the_network_opens']:
    w('- %s' % c)
w()
w('## The numbers the street already has (read from other files)')
w()
render(T['scene_numbers'] + T['other_target_numbers'] + T['hook_cast_numbers'])
w()
w('## The checks the builder\'s automatic check must pass')
w()
render(T['checks'])
w()
w('## Hand-over')
w()
render(T['handover'])
w()
w('## Self-check')
w()
sc = T['self_check']
w('%s' % sc['line'])
w()
for r in sc['reported']:
    w('- reported: %s' % r)
open(os.path.join(HERE, 'TARGET.md'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('TARGET.md', len('\n'.join(OUT).split()), 'words')
