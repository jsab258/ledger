#!/usr/bin/env python3
"""Build lines/ (blueprint data file 10): the line-bank structure, the existing shared street bank converted, the
landmark direction lines (GV-03), Frank's written suggested and fixed lines, and a TO WRITE record for every
person's own lines and every story-carrying bank, for the story lane. Every text is checked against
content-words.json. Written 24 Nov 2026 (data-build wave 2)."""
import json, os, re, sys
from collections import Counter, defaultdict
HERE = os.path.dirname(os.path.abspath(__file__))
D = os.path.normpath(os.path.join(HERE, '..', '..'))
R = os.path.normpath(os.path.join(D, '..', '..', '..', '..'))
sys.path.insert(0, HERE)
from build_people import C

OUT = os.path.join(D, 'lines')
os.makedirs(OUT, exist_ok=True)
CLOCK = {"realSecondsPerGameHour": 120}
BANK = json.load(open(os.path.join(R, 'production/cloud-week/lines/lines.json')))
SUG = json.load(open(os.path.join(R, 'production/specs/suggested-lines.json')))
CW = json.load(open(os.path.join(D, 'content-words.json')))
MAP = json.load(open(os.path.join(D, 'map.json')))
cid2id = {p['cid']: p['id'] for p in C.P if p.get('cid')}

# ---- content check (mechanical categories, plus the prototype's banned words)
PATS = []
for cat in CW['categories']:
    for p in cat.get('patterns', []):
        PATS.append((cat['id'], re.compile(p['pattern'].replace('(?<', '(?<'), 0 if p.get('cased') else re.I)))
BANNED = [re.compile(r'\b%s\b' % re.escape(w), re.I) for w in CW['prototype_banned']['words']]
def content_fail(text):
    for cid, rx in PATS:
        if rx.search(text):
            return cid
    for rx in BANNED:
        if rx.search(text):
            return 'prototype_banned:' + rx.pattern
    return None

def frank(text):
    t = re.sub(r'\bTommy\b', 'Frankie', text)
    t = re.sub(r'\bTom\b', 'Frank', t)
    return t

def words(t):
    return len(re.findall(r"[A-Za-z']+", t))

SIT_RENAME = {'greeting.tom': 'greeting.frank', 'greeting.tommy': 'greeting.frankie'}
RUNG_RENAME = {'tom': 'frank', 'tommy': 'frankie'}
OWN_KIND = {'ron': 'ron_kirby', 'darren': 'darren_milner', 'father_walsh': 'brendan_walsh', 'june': 'june_suddaby'}

def head(name, sources, note, opens=None):
    return {"file": "lines/" + name, "version": "wave2-2026-11-24", "clock": CLOCK, "sources": sources,
            "open_points": opens or [], "note": note}

fails = []
def rec(**k):
    k.setdefault('words', words(k['text']))
    if not k['text'].startswith('TO WRITE'):
        f = content_fail(k['text'])
        if f:
            fails.append((k['id'], f, k['text']))
    return k

# ================= 1. the shared street bank, converted
shared, own = [], defaultdict(list)
for x in BANK['lines']:
    text = frank(x['text'])
    sit = SIT_RENAME.get(x['situation'], x['situation'])
    kind = x['kind']
    cond = dict(x.get('conditions') or {})
    if 'standing' in cond:
        cond['standing'] = [RUNG_RENAME.get(s, s) for s in cond['standing']]
    base = dict(id=x['id'].replace('greet-tommy', 'greet-frankie').replace('greet-tom', 'greet-frank'),
                situation=sit, text=text, src='production/cloud-week/lines/lines.json ' + x['id'],
                tokens=[], bank=x.get('bank'), context=x.get('context'), rung=RUNG_RENAME.get(x.get('rung'), x.get('rung')),
                conditions=cond, weight=x.get('weight'), group=x.get('group'), delivery=x.get('delivery'))
    if kind in OWN_KIND:
        own[OWN_KIND[kind]].append(rec(who=OWN_KIND[kind], once='day', **base))
    else:
        shared.append(rec(who=kind, once='week', **base))
members = {k: [cid2id.get(m, m) for m in v.get('members', [])] for k, v in BANK['speakers'].items()}
json.dump(dict(head('shared-street.json', ['production/cloud-week/lines/lines.json (1,626 lines, 13 kinds, 14 situations; converted)', 'BLUEPRINT-03 3.6.3, 3.6.4; BLUEPRINT-02 2.12.4'],
    "Shared street lines by speaker kind (who is a kind). A shared line once a week per street; everyday street talk at most every 45 s (2.12.4). Situations renamed for the lead: greeting.tom is greeting.frank, greeting.tommy is greeting.frankie. Conditions, weights and cool-down groups are the bank's own and are kept.",
    ["Kinds' members are the bank's (mapped to people ids); people added in wave 2 take the kind of their trade (speaker_kinds below).",
     "asked_way lines name the bank's own 34 places (conditions.place); places.json ids are the home for positions; the keeper maps the bank's place list to places.json ids before the one-shot (most map one to one: quay, mickeys, fish_shop to laveracks, ritas, caff, chapel)."]),
    speaker_kinds={k: {"what": v.get('what'), "members": members[k]} for k, v in BANK['speakers'].items() if k not in OWN_KIND},
    situations=sorted({l['situation'] for l in shared}), lines=shared), open(os.path.join(OUT, 'shared-street.json'), 'w'), indent=1, ensure_ascii=False)

# ================= 2. own lines: the four with lines, and a TO WRITE quota for everyone else who needs them
MOST_SEEN = ['ron_kirby', 'pauline_kitching', 'darren_milner', 'kevin_needham', 'terry_hodgson', 'pc_ibbotson', 'grace_rinaldi',
             'brenda_laverack', 'wayne_harrison', 'rita_welburn', 'lee_drewery', 'brendan_walsh']   # FIT-L01's twelve, the constable and the caff owner named
SHARED_ONLY = {'sheila_dunn', 'alison_sedman', 'ada_vane'}   # 3.6.3: they keep the shared lines
OWN_SITUATIONS = ['greet', 'comment', 'weather', 'work', 'about_frank', 'about_the_street', 'close']
quota = {}
for p in C.P:
    pid = p['id']
    if pid == 'frank_nowak' or pid in SHARED_ONLY:
        continue
    if p['k'] in ('principal', 'firm', 'regular', 'rival_man') or pid in MOST_SEEN:
        n = 60 if pid in MOST_SEEN else 30
        have = own.get(pid, [])
        quota[pid] = (n, len(have))
        lines = list(have)
        need = max(0, n - len(have))
        if need:
            lines.append(rec(id=pid + '.own.to_write', who=pid, situation='own', once='day',
                             text='TO WRITE (story lane): %d own street lines, about 7 words each, in the voice of the card (people/%s.json), spread over %s; at least three closing lines.' % (need, pid, ', '.join(OWN_SITUATIONS)),
                             src='BLUEPRINT-03 3.2.3, 3.6.3; FIT-L01 (%d for %s)' % (n, 'the twelve most seen' if n == 60 else 'a regular')))
        json.dump(dict(head('own-%s.json' % pid, ['people/%s.json (card: who, speak)' % pid] + (['production/cloud-week/lines/lines.json (the bank\'s own lines for this person)'] if have else []),
            "%s's own street lines: once a day each (3.6.3). %d needed, %d written." % (p['n'], n, len(have))), lines=lines),
            open(os.path.join(OUT, 'own-%s.json' % pid), 'w'), indent=1, ensure_ascii=False)

# ================= 3. landmark direction lines (GV-03): one per 20 s of chase, each naming a real landmark
LM = MAP['landmarks']
FOOT_ONLY = [("the yards' lane", 'he cannot follow you down the yards\' lane in a car'), ("the ginnel", 'the ginnel, nothing on four wheels gets through there'),
             ("the gap", 'through the gap by the quay, a car will not fit')]
dirs = []
for lm in LM:
    n = lm['name']
    nm = n[0].upper() + n[1:]
    base = lm['id'].replace('lm_', '')
    for i, (txt, who) in enumerate([
        ("Coming up on %s. That's %s. Leaving %s." % (n, n, n), 'ron_kirby'),
        ("Left after %s." % n, 'passenger'), ("Right at %s." % n, 'passenger'), ("Straight on past %s." % n, 'passenger'),
        ("%s on your left. Keep going." % nm, 'passenger'), ("Next one after %s, sharp left." % n, 'passenger'),
        ("Down by %s. He'll lose you there." % n, 'passenger'), ("Turn here, before %s." % n, 'passenger'),
    ]):
        dirs.append(rec(id='way.%s.%02d' % (base, i + 1), who=who, situation='direction.chase' if i >= 5 else 'direction.way', text=txt, once='never',
                        tokens=[lm['id']], landmark=lm['id'], said_as=lm['said'],
                        src='GV-03; map.json landmarks %s (written here from the landmark\'s name; Ron\'s three-beat form is the frame\'s: "Coming up on the ice house...")' % lm['id']))
for i, (place, txt) in enumerate(FOOT_ONLY):
    dirs.append(rec(id='way.footonly.%02d' % (i + 1), who='passenger', situation='direction.chase', text=txt[0].upper() + txt[1:] + '.', once='never',
                    tokens=[], src='GV-03 (he cannot follow you through the yard); map.json foot-only ways'))
json.dump(dict(head('directions.json', ['map.json landmarks (16) and foot-only ways', 'BLUEPRINT-01 GV-03'],
    "Landmark direction lines: whoever rides with Frank says the way by landmark (no marker). 'passenger' means Ron, a crewman or a fare who knows the town; Ron's own form is the three-beat one. once never: these repeat by design and are chosen so the landmark named is on the route ahead. At least one a 20 s of chase (GV-03).",
    ["The chase picker that chooses the landmark on the route ahead is the one-shot's (the route is map.json's driving graph); these are the words only.",
     "Ron's three-beat lines are written once per landmark here; his own-line voice for the rest is TO WRITE in own-ron_kirby.json."]), lines=dirs),
    open(os.path.join(OUT, 'directions.json'), 'w'), indent=1, ensure_ascii=False)

# ================= 4. Frank: suggested lines (approved, ruling 1 Oct) and the fixed lines the frame gives
fl = []
for k in ('greet', 'leave', 'personal'):
    for i, t in enumerate(SUG[k]):
        fl.append(rec(id='frank.suggest.%s.%02d' % (k, i + 1), who='frank_nowak', situation='suggest.' + k, text=frank(t), once='never', src='production/specs/suggested-lines.json %s (approved 1 Oct)' % k))
for deal, opts in SUG['deals'].items():
    for opt, ts in opts.items():
        for i, t in enumerate(ts):
            fl.append(rec(id='frank.deal.%s.%s.%02d' % (deal, opt, i + 1), who='frank_nowak', situation='decision.' + deal, text=frank(t), once='never',
                          src='production/specs/suggested-lines.json deals.%s.%s (approved 1 Oct)' % (deal, opt)))
FIXED = [("frank.fixed.want", "Thirty years, and that's the firm? An old man walking an envelope down to the water? Not for me. Every fare after dark, every door on this street, every quay with a rope on it: it goes through this office or it doesn't go. By Christmas, Ron. Mickey's runs the Hook. And when they say Mickey's, they'll mean me.", "the want, night one (STORY-FRAME 1)"),
         ("frank.fixed.car_three", "It's on my rank, so it's on my board. Car three. Two pound forty to the quay. Sheila, put it in the book.", "car three (STORY-FRAME 3)"),
         ("frank.fixed.spelling", "Nowak. N, O, W, A, K.", "the spelling (STORY-FRAME 3)")]
for i, t, s in FIXED:
    fl.append(rec(id=i, who='frank_nowak', situation='fixed', text=t, once='game', src='STORY-FRAME-2026-11-26 ' + s + '; the lead renamed Frank (decision of 24 Nov); TO CHECK against the story lane\'s scenes'))
json.dump(dict(head('frank.json', ['production/specs/suggested-lines.json (approved 1 Oct)', 'STORY-FRAME-2026-11-26 sections 1 and 3'],
    "Frank's written lines: the suggested lines (about 4 words; hellos, goodbyes, decisions: 3.6.6) and the fixed lines at authored beats. The rest of his talk is the player's."), lines=fl),
    open(os.path.join(OUT, 'frank.json'), 'w'), indent=1, ensure_ascii=False)

# ================= 5. story-carrying banks: TO WRITE for the story lane (only words the frame already gives are filled)
story = []
GIVEN = [
    ("story.ron.icehouse", "ron_kirby", "voice", "Coming up on the ice house. That's the ice house. Leaving the ice house."),
    ("story.ron.not_you", "ron_kirby", "voice", "I've told her nowt that isn't so. I've just not told her you."),
    ("story.ron.envelope", "ron_kirby", "night_one", "Aye. Well. Envelope still wants carrying."),
    ("story.sheila.reference", "sheila_dunn", "voice", "The book will hide ten pounds and four fifths of what the cars really drove. Past that I'm not keeping accounts, love, I'm writing you a reference."),
    ("story.sheila.you_write", "sheila_dunn", "voice", "Thirty-one years I've written what I was told. You write this one."),
    ("story.sheila.the_line", "sheila_dunn", "the_line", "Every fare goes in the book. That was Mickey's rule, and it's mine now. So. What was last night?"),
    ("story.sheila.habit", "sheila_dunn", "the_habit", "Same as your first night?"),
    ("story.danny.motor", "danny_cammack", "voice", "He's moved my motor. Mickey would've asked nicely for a fortnight and then said sorry."),
    ("story.danny.book", "danny_cammack", "voice", "You've got the book, nephew. I am the book."),
    ("story.danny.park", "danny_cammack", "car_two", "That's how you park it."),
    ("story.widow.short", "maureen_jensen", "voice", "I never ask anybody for anything, Mr Nowak. I find out what they're short of."),
    ("story.widow.oven", "maureen_jensen", "voice", "Sit down. It's been in the oven twice."),
    ("story.ellis.twice", "carol_ellis", "voice", "I'm not asking you to remember everything. I'm asking you to remember it the same way twice."),
    ("story.ellis.sign", "carol_ellis", "voice", "Somebody always saw, Mr Nowak. My trouble is finding the one who'll sign."),
    ("story.ellis.again", "carol_ellis", "the_turn", "Write it again. Underneath. Same words."),
    ("story.ron.cells", "ron_kirby", "the_night_between", "That you, boss? Say nowt."),
    ("story.ron.saying", "ron_kirby", "the_night_between", "Saying's nowt, boss. You've a firm to stand in. I've a door."),
    ("story.ron.watch", "ron_kirby", "the_watch", "Tell him it's five minutes fast. Mickey liked to be early."),
    ("story.ron.visit", "ron_kirby", "the_visit", "You keep that rank going, boss. I've not sat in here for you to finish with nowt."),
    ("story.screeton.change", "neil_screeton", "the_yard", "Eighty pound, Mr Nowak. I've your change here."),
    ("story.billany.straight", "mark_billany", "the_landing", "That's us straight."),
]
for i, who, sit, t in GIVEN:
    story.append(rec(id=i, who=who, situation='story.' + sit, text=frank(t), once='game', src='STORY-FRAME-2026-11-26 (sample line, not final script: the story lane owns it)'))
TOWRITE = [
    ('story.name_said', 'any', 'Each named person\'s first saying of the next rung\'s name (the new owner, Nowak, Frank, Frankie), said to his face (7.7); the three who say Frankie: the Widow, Danny, Ron once.'),
    ('story.next_want', 'any', 'The Ledger\'s next named want in a person\'s own words, one per beat (STORY-FRAME 6, the next want).'),
    ('story.pauline_air', 'pauline_kitching', 'Pauline on the air, one set per rung and per week (STORY-FRAME 1 table), and the last day\'s calls.'),
    ('story.said_to_face', 'any', 'A named witness\'s remark returning each deed of weight within a game day (STORY-FRAME 7): one per kind of deed per witness kind.'),
    ('story.rival_rungs', 'maureen_jensen, geoffrey_agar, danny_cammack', 'Each rival\'s noticed, visit, pressure, threat and sit-down lines (2.10.1 to 2.10.3, RT-06).'),
    ('story.fares', 'fare people', 'Two rides\' lines for each of the 40 fare people (fares.json TO WRITE fields).'),
    ('story.side_stories', 'givers', 'Step lines for every side story (about 30 a story; side-stories/ TO WRITE fields).'),
    ('story.happenings', 'any', 'Lines for the happenings (happenings.json TO WRITE fields).'),
    ('story.endings', 'any', 'The close\'s voices per ending, up to about five lines (STORY-FRAME 8).'),
    ('story.decisions', 'any', 'Decision lines: a yes, a no and a line that keeps talking for every decision (3.6.5); the 170 not-a-plain-yes test lines.'),
]
for i, who, what in TOWRITE:
    story.append(rec(id=i + '.to_write', who=who, situation=i, text='TO WRITE (story lane): ' + what, once='game', src='STORY-FRAME-2026-11-26; BLUEPRINT-03'))
json.dump(dict(head('story.json', ['STORY-FRAME-2026-11-26 sample lines', 'production/lane/story/paper/ (being written in parallel)'],
    "Story-carrying lines. The words given are the frame's sample lines (not final script), kept so the one-shot has them; every bank the story needs is listed as TO WRITE for the story lane, whose scenes outrank these.",
    ["The story lane's paper (production/lane/story/paper/) had not landed when this file was made: every line here is replaced by its scenes when it does."]), lines=story),
    open(os.path.join(OUT, 'story.json'), 'w'), indent=1, ensure_ascii=False)

# ================= README (the structure, not a data file)
readme = """# lines/ (blueprint data file 10)

Made 24 Nov 2026 by the data-build wave 2 job. Every spoken or written line is a record (TECH-PLAN section 3): id, who (a people id or a speaker kind), situation, text, words, once (day, week, game or never), tokens, src. The record carries its own cool-down.

| File | What | Lines | Written | TO WRITE |
|---|---|---|---|---|
| shared-street.json | the street's shared lines by speaker kind (converted from the cloud week's bank) | %d | all | none |
| own-<person>.json | one file per person who keeps own lines: 60 for the twelve most seen, 30 for the rest (FIT-L01) | %d files | %d (Ron, Darren, Father Walsh, June) | %d lines over %d people |
| directions.json | landmark direction lines for the way and chases (GV-03) | %d | all | none |
| frank.json | Frank's approved suggested lines and the frame's fixed lines | %d | all | none |
| story.json | story-carrying lines: the frame's sample lines, and every story bank as TO WRITE | %d | %d samples | %d banks |

Rules kept: the lead is Frank (greeting.tom became greeting.frank, greeting.tommy became greeting.frankie; Tom in any text became Frank). Sheila, Alison and Ada keep the shared lines (3.6.3). Own lines once a day; shared once a week per street. Every written text passes content-words.json (checked by tools/wave2/build_lines.py).

Own lines are not mass-written here: their quality is the story lane's.
"""
own_written = sum(v[1] for v in quota.values())
own_need = sum(max(0, v[0] - v[1]) for v in quota.values())
open(os.path.join(OUT, 'README.md'), 'w').write(readme % (len(shared), len(quota), own_written, own_need, sum(1 for v in quota.values() if v[0] > v[1]),
                                                         len(dirs), len(fl), len(story), len(GIVEN), len(TOWRITE)))
print('shared', len(shared), 'own files', len(quota), 'own written', own_written, 'own to write', own_need, 'directions', len(dirs), 'frank', len(fl), 'story', len(story))
print('content fails', len(fails))
for f in fails[:30]:
    print('  ', f)
sys.exit(1 if fails else 0)
