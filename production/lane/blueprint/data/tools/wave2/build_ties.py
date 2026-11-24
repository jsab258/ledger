#!/usr/bin/env python3
"""Build ties.json: one list for the whole cast in the real town's form [a, b, strength, "place hh:mm days; ..."].
The ties are hook-cast.json's 81 (ids mapped to the new people ids) plus those the story frame and the rivals'
ladders need. The meeting string is computed from routines.json: every place and hour both are at the same place
for at least 30 game minutes, so no friendship is one that never meets. Written 24 Nov 2026 (wave 2)."""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, HERE)
from build_people import C, parse_rt, parse_days, mins, DAYS, point_of
import math
TALK_M = 20.0  # two places count as together within 20 m (hook-cast.json talk range, rounded)
_near = {}
def near(p1, p2):
    if p1 == p2:
        return True
    k = (p1, p2)
    if k not in _near:
        a, b = point_of(p1), point_of(p2)
        _near[k] = bool(a and b and math.dist(a, b) <= TALK_M)
    return _near[k]

HOOK = json.load(open(os.path.normpath(os.path.join(D, '..', '..', '..', 'specs', 'hook-cast.json'))))
cid2id = {p['cid']: p['id'] for p in C.P if p.get('cid')}
ids = {p['id'] for p in C.P}

TIES = []
for a, b, w, _ in HOOK['ties']:
    if a in cid2id and b in cid2id:
        TIES.append((cid2id[a], cid2id[b], w, 'hook-cast.json'))
FRAME = [
    ("ron_kirby", "pauline_kitching", 0.6), ("ron_kirby", "danny_cammack", 0.4), ("ron_kirby", "brendan_walsh", 0.5),
    ("ron_kirby", "kevin_needham", 0.5), ("ron_kirby", "lily_tang", 0.4), ("ron_kirby", "stathers", 0.3),
    ("danny_cammack", "craig_fewson", 0.7), ("danny_cammack", "shane_boddy", 0.5), ("danny_cammack", "wes_akers", 0.5),
    ("danny_cammack", "jason_pinder", 0.3), ("danny_cammack", "rita_welburn", 0.6), ("danny_cammack", "vince_lazenby", 0.4),
    ("craig_fewson", "shane_boddy", 0.5), ("shane_boddy", "wes_akers", 0.6), ("shane_boddy", "dennis_iveson", 0.3),
    ("maureen_jensen", "stathers", 0.8), ("maureen_jensen", "mark_billany", 0.5), ("maureen_jensen", "pat_brannigan", 0.6),
    ("maureen_jensen", "dougie_saltmarsh", 0.5), ("maureen_jensen", "kevin_needham", 0.4), ("maureen_jensen", "lee_drewery", 0.4),
    ("stathers", "mark_billany", 0.6), ("stathers", "lee_drewery", 0.4), ("dougie_saltmarsh", "eddie_birtwhistle", 0.5),
    ("mark_billany", "pat_brannigan", 0.5), ("lee_drewery", "colin_mastin", 0.4), ("bill_huxtable", "colin_mastin", 0.5),
    ("bill_huxtable", "jimmy_raw", 0.3), ("jimmy_raw", "ken_dobbin", 0.7),
    ("geoffrey_agar", "simon_ombler", 0.8), ("geoffrey_agar", "susan_coverdale", 0.5), ("geoffrey_agar", "leonard_askew", 0.6),
    ("geoffrey_agar", "anthony_raine", 0.5), ("geoffrey_agar", "barry_coult", 0.4), ("geoffrey_agar", "alan_sowerby", 0.4),
    ("simon_ombler", "leonard_askew", 0.6), ("simon_ombler", "barry_coult", 0.5), ("barry_coult", "ray_spink", 0.7),
    ("barry_coult", "kenny_varley", 0.6), ("leonard_askew", "dawn_pybus", 0.6),
    ("carol_ellis", "graham_wardell", 0.5), ("carol_ellis", "trevor_garton", 0.3), ("carol_ellis", "sgt_kitson", 0.4),
    ("carol_ellis", "alison_sedman", 0.3), ("pc_ibbotson", "pc_haigh", 0.5), ("pc_ibbotson", "grace_rinaldi", 0.3),
    ("pc_haigh", "maggie_firth", 0.4),
    ("keith_garbutt", "maureen_jensen", 0.3), ("keith_garbutt", "danny_cammack", 0.3), ("keith_garbutt", "geoffrey_agar", 0.3),
    ("keith_garbutt", "vince_lazenby", 0.4),
    ("dennis_iveson", "neil_screeton", 0.7), ("eric_tharratt", "malcolm_ruddock", 0.6), ("malcolm_ruddock", "dougie_saltmarsh", 0.3),
    ("peter_tang", "lily_tang", 0.9), ("karen_grummitt", "sylvia_rennison", 0.4), ("julie_kettlewell", "pat_stainton", 0.6),
    ("doreen_harland", "irene_lowther", 0.5), ("doreen_harland", "pat_stainton", 0.5), ("tracey_scarth", "beryl_wood", 0.4),
    ("rita_welburn", "stanley_hirst", 0.6), ("rita_welburn", "mandy_calvert", 0.5), ("rita_welburn", "leslie_cotterill", 0.4),
    ("ian_megginson", "leslie_cotterill", 0.5), ("ian_megginson", "gary_mawer", 0.5), ("albert_suggitt", "cyril_pashby", 0.3),
    ("albert_suggitt", "wilf_hardcastle", 0.3), ("len_garside", "george_cammidge", 0.5), ("nora_cronin", "edna_coulson", 0.5),
    ("tadeusz_nowicki", "brendan_walsh", 0.4), ("aidan_keogh", "brendan_walsh", 0.4), ("philip_danby", "janet_ruddle", 0.3),
    ("philip_danby", "alison_sedman", 0.3), ("june_suddaby", "sheila_dunn", 0.5), ("edith_stockill", "peart", 0.5),
    ("arthur_brigham", "ada_vane", 0.3), ("joyce_ellerby", "june_suddaby", 0.2), ("rodney_usher", "dougie_saltmarsh", 0.4),
    ("douglas_fenwick", "paddy_rourke", 0.4), ("susan_coverdale", "paddy_rourke", 0.5),
]
have = {(a, b) for a, b, _, _ in TIES} | {(b, a) for a, b, _, _ in TIES}
for a, b, w in FRAME:
    assert a in ids and b in ids, (a, b)
    if (a, b) not in have:
        TIES.append((a, b, w, 'wave 2: the story frame, the rivals\' ladders (2.10.2) and the regulars\' work'))
        have |= {(a, b), (b, a)}

def slots(p):
    """Per day, a list of (start, end, place) from the routine."""
    out = {}
    for days, rows in parse_rt(p['rt']):
        for d in parse_days(days):
            rr = [(mins(t), pl) for t, pl, _ in rows]
            out[d] = [(rr[i][0], rr[i + 1][0] if i + 1 < len(rr) else 1440, rr[i][1]) for i in range(len(rr))]
    return out

PS = {p['id']: p for p in C.P}
SL = {p['id']: slots(p) for p in C.P if p['rt'] != 'lead'}
HOMES = {p['home'] for p in C.P}

def meetings(a, b):
    found = {}
    for d in DAYS:
        for s1, e1, p1 in SL.get(a, {}).get(d, []):
            for s2, e2, p2 in SL.get(b, {}).get(d, []):
                if p1 in ('edge_north', 'edge_west') or p2 in ('edge_north', 'edge_west') or not near(p1, p2):
                    continue
                s, e = max(s1, s2), min(e1, e2)
                if e - s >= 30:
                    key = (p1, '%02d:%02d' % (s // 60, s % 60))
                    found.setdefault(key, []).append(d)
    parts = []
    for (pl, t), ds in sorted(found.items(), key=lambda kv: -len(kv[1]))[:3]:
        parts.append('%s %s %s' % (pl, t, ','.join(x.capitalize() for x in DAYS if x in ds)))
    return '; '.join(parts)

out, never = [], []
for a, b, w, src in TIES:
    m = meetings(a, b)
    if not m:
        never.append([a, b])
    out.append([a, b, w, m])
json.dump({"file": "ties.json", "version": "wave2-2026-11-24", "clock": {"realSecondsPerGameHour": 120},
           "sources": ["production/specs/hook-cast.json ties (81, ids mapped to people/ ids)",
                       "the story frame (STORY-FRAME-2026-11-26 sections 2 to 4), BLUEPRINT-02 2.10.2 (each rival a lieutenant and three named men), the regulars' work places",
                       "meetings computed from routines.json by tools/wave2/build_ties.py: same place, both there (or within 20 m of each other, hook-cast.json's talk range) 30 game minutes or more"],
           "format": "[a, b, strength 0..1, 'place hh:mm Days; ...'] with at most three meetings, the most frequent first; an empty string means the two never meet in a week (listed in never_meet)",
           "never_meet": never,
           "open_points": ["Pairs in never_meet keep their tie (a rumour can still pass by a third person) but the real town's talk-range check will show them as friends who never meet; the keeper decides whether to add a shared hour or drop the tie."],
           "ties": out}, open(os.path.join(D, 'ties.json'), 'w'), indent=1, ensure_ascii=False)
print('ties', len(out), 'never meet', len(never))
for n in never:
    print('  never', n)
