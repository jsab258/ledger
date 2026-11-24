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
import people_fix as PF

OUT = os.path.join(D, 'lines')
os.makedirs(OUT, exist_ok=True)
import glob as _g
for _f in _g.glob(os.path.join(OUT, '*.json')):
    os.remove(_f)
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

SIT_RENAME = {'greeting.tom': 'greeting.frank'}
RUNG_RENAME = {'tom': 'frank'}
BANK_PLACE = {'quay': 'fishing_quay_west', 'mickeys': 'mickeys', 'fish_shop': 'laveracks', 'ritas': 'ritas', 'phone_box': 'phone_parade', 'laundry': 'launderette', 'grocer': 'grocer', 'chandler': 'chandlery', 'cafe': 'caff', 'newsagent': 'newsagent', 'bus_stop': 'bus_stop_qs', 'docks': 'dock_gate', 'fish_dock': 'fish_dock', 'harbour_office': 'harbour_board', 'customs_shed': 'customs', 'ferry': 'ferry_landing', 'warehouse_row': 'dents_warehouses', 'walsh_chapel': 'chapel', 'open_market': 'market_stalls_quay', 'boarding_house': 'boarding_house', 'allotments': 'allotments', 'old_basin': 'fishing_basin_north', 'harbour_board': 'harbour_board', 'market_hall': 'edge_north', 'tivoli': 'edge_north', 'fairview_chapel': 'edge_north', 'records_court': 'edge_north', 'police_station': 'police_station', 'canteen': 'edge_north', 'retort_works': 'edge_north', 'winter_rooms': 'edge_north', 'short_pier': 'edge_west'}
WRONG_WAY = re.compile(r'(Tuesday, Friday, Saturday|Tuesdays?, Fridays?|across from Rita|on the hill|You.ll hear the bell)', re.I)
dropped = Counter()
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
    if x['situation'] == 'greeting.tommy':
        dropped['greeting.tommy (Frankie is for the Widow, Danny and Ron once: 7.7, decision of 24 Nov)'] += 1
        continue
    if 'standing' in cond and 'frank' in cond['standing']:
        cond['standing'] = sorted(set(cond['standing']) | {'portsman'})   # rung 4 (the port's man) keeps the Frank greetings
    if x['context'] == 'greeting':
        cond['regard'] = ['neutral'] if x.get('rung') == 'stranger' else ['likes']
    base['calls_police'] = bool(x.get('calls_police', False))
    base['dialect'] = x.get('dialect', 'plain')
    if x['situation'] == 'asked_way':
        dest = BANK_PLACE.get((x.get('conditions') or {}).get('place')) if isinstance((x.get('conditions') or {}).get('place'), str) else None
        if kind == 'ron':
            dropped['Ron asked_way (he knows every road: GV-03; replaced by TO WRITE)'] += 1
            continue
        if WRONG_WAY.search(text):
            dropped['asked_way that contradicts map.json or places.json'] += 1
            continue
        pl = (x.get('conditions') or {}).get('place')
        if pl in ('boatyard', 'flats'):
            dropped['asked_way to a place the map does not have (boatyard, flats)'] += 1
            continue
        base['destination'] = BANK_PLACE.get(pl) if pl else None
    if kind in OWN_KIND:
        own[OWN_KIND[kind]].append(rec(who=OWN_KIND[kind], once='day', **base))
    else:
        shared.append(rec(who='kind:' + kind, once='week', **base))
KINDS = [k for k in BANK['speakers'] if k not in OWN_KIND]
for k in KINDS:
    for rg in ('afraid', 'angry', 'appearance', 'neutral'):
        shared.append(rec(id='%s.greet-regard-%s.to_write' % (k, rg), who='kind:' + k, situation='greeting.regard.' + rg, once='week', text='TO WRITE (story lane): 6 greetings by regard %s for %s, rungs owner to portsman; nobody says Frankie or Tom (2.12.4, 3.6.4)' % (rg, k), src='BLUEPRINT-02 2.12.4; BLUEPRINT-03 3.6.4', conditions={'regard': [rg]}))
    for sit, what in [('neighbours', 'neighbours greeting each other'), ('at_work', 'talking to oneself at work'), ('man_down', 'a body or a man down'),
                      ('know.comment', "the knowing ladder's comment step ('you want to watch yourself, son')"), ('know.refuse', "the knowing ladder's refuse step"),
                      ('know.confront', "the knowing ladder's confront step"), ('talk_of_deeds', 'bystanders talking of his recent deeds second-hand'),
                      ('everyday', 'everyday remarks with no event (weather dry, the street, prices), so 14 situations are live in a quiet hour')]:
        shared.append(rec(id='%s.%s.to_write' % (k, sit), who='kind:' + k, situation=sit, once='week', text='TO WRITE (story lane): 6 lines, %s, for %s' % (what, k), src='BLUEPRINT-02 2.4.3; BLUEPRINT-03 3.6.4; FIT-F19'))
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
    if PF.has_own(p):
        n = 60 if pid in MOST_SEEN else 30
        have = own.get(pid, [])
        quota[pid] = (n, len(have))
        lines = list(have)
        need = max(0, n - len(have))
        if need or True:
            lines.append(rec(id=pid + '.own.to_write', who=pid, situation='own', once='day',
                             text='TO WRITE (story lane): %d own street lines, about 7 words each, in the voice of the card (people/%s.json). Situations from line-situations.json (greetings by rung and by regard, everyday remarks, the knowing ladder, farewells); at least three closing lines. Everyday remarks of his own are owed even where situational lines exist. Names him: the new owner (rung 1), Mr Nowak or Nowak (2), Frank (3), Frank or Mr Nowak (4, the port\'s man); Sheila withholds his name until she trusts him; Ron says boss; only the Widow, Danny and Ron once say Frankie; nobody says Tom.' % (need, pid),
                             src='BLUEPRINT-03 3.2.3, 3.6.3; FIT-L01 (%d for %s)' % (n, 'the twelve most seen' if n == 60 else 'a regular')))
        json.dump(dict(head('own-%s.json' % pid, ['people/%s.json (card: who, speak)' % pid] + (['production/cloud-week/lines/lines.json (the bank\'s own lines for this person)'] if have else []),
            "%s's own street lines: once a day each (3.6.3). %d needed, %d written." % (p['n'], n, len(have))), lines=lines),
            open(os.path.join(OUT, 'own-%s.json' % pid), 'w'), indent=1, ensure_ascii=False)

# ================= 3. landmark direction lines (GV-03): one per 20 s of chase, each naming a real landmark
LM = MAP['landmarks']
FOOT_ONLY = [("the yards' lane", 'he cannot follow you down the yards\' lane in a car'), ("the ginnel", 'the ginnel, nothing on four wheels gets through there'),
             ("the gap", 'through the gap by the quay, a car will not fit')]
dirs = []
FORMS = [("Coming up on {n}. That's {n}. Leaving {n}.", 'ron_kirby', 'voice.ron', None, None, False),
         ("Left after {n}.", 'passenger', 'direction', 'left', None, True), ("Right at {n}.", 'passenger', 'direction', 'right', None, True),
         ("Straight on past {n}.", 'passenger', 'direction', 'straight', None, True), ("{N} on your left. Keep going.", 'passenger', 'direction', 'straight', 'left', True),
         ("{N} on your right. Keep going.", 'passenger', 'direction', 'straight', 'right', True),
         ("Next one after {n}, sharp left.", 'passenger', 'direction', 'left', None, True), ("Next one after {n}, sharp right.", 'passenger', 'direction', 'right', None, True),
         ("Right before {n}. He'll lose you there.", 'passenger', 'direction', 'right', None, True), ("Left before {n}. He'll lose you there.", 'passenger', 'direction', 'left', None, True)]
for lm in LM:
    n = lm['name']; N = n[0].upper() + n[1:]
    base = lm['id'].replace('lm_', '')
    for i, (f, who, sit, turn, side, counts) in enumerate(FORMS):
        dirs.append(rec(id='way.%s.%02d' % (base, i + 1), who=('kind:passenger' if who == 'passenger' else who), situation=sit, text=f.format(n=n, N=N), once='never',
                        tokens=[lm['id']], landmark=lm['id'], said_as=lm['said'], turn=turn, side=side, mode='car_or_foot', counts_for_gv03=counts,
                        src='GV-03; map.json landmarks %s (written here from the landmark\'s name)%s' % (lm['id'], '; Ron\'s three-beat is his running joke (STORY-FRAME 2): a voice line that does not count toward the GV-03 rate' if not counts else '')))
FOOT = [("yards_lane", "Down the yards' lane. He can't get a car down there."), ("ginnel", "Through the ginnel. Nothing on four wheels gets through."), ("quay_gap", "Through the gap by the quay. A car won't fit.")]
for i, (way, txt) in enumerate(FOOT):
    dirs.append(rec(id='way.footonly.%02d' % (i + 1), who='kind:passenger', situation='direction', text=txt, once='never', tokens=[way], way=way, turn=None, side=None,
                    mode='foot', counts_for_gv03=True, src='GV-03 (he cannot follow you through the yard); map.json roads %s (foot only)' % way))
json.dump(dict(head('directions.json', ['map.json landmarks (16) and foot-only ways', 'BLUEPRINT-01 GV-03'],
    "Landmark direction lines: whoever rides with Frank says the way by landmark (no marker). kind:passenger is whoever rides with Frank: Ron, a crewman, or a fare who knows the town (people whose card says so). turn and side let the picker match a line to the road ahead on map.json's driving graph (mode foot lines only in foot chases). counts_for_gv03 false marks Ron's three-beat running joke, a voice line. At least one counting line a 20 s of chase (GV-03).",
    ["The chase picker that chooses the landmark on the route ahead is the one-shot's (the route is map.json's driving graph); these are the words only.",
     "Ron's three-beat lines are written once per landmark here; his own-line voice for the rest is TO WRITE in own-ron_kirby.json."]), lines=dirs),
    open(os.path.join(OUT, 'directions.json'), 'w'), indent=1, ensure_ascii=False)

# ================= 4. Frank: suggested lines (approved, ruling 1 Oct) and the fixed lines the frame gives
fl = []
for k in ('greet', 'leave', 'personal'):
    for i, t in enumerate(SUG[k]):
        r = rec(id='frank.suggest.%s.%02d' % (k, i + 1), who='frank_nowak', situation='suggest.' + k, text=frank(t), once='never', src='production/specs/suggested-lines.json %s (approved 1 Oct)' % k,
                not_twice_in_one_talk=True)
        if re.search(r"finding my feet|all new to me|many strangers", t):
            r['conditions'] = {'rung_at_most': 2}
        fl.append(r)
for deal, opts in SUG['deals'].items():
    for opt, ts in opts.items():
        for i, t in enumerate(ts):
            fl.append(rec(id='frank.deal.%s.%s.%02d' % (deal, opt, i + 1), who='frank_nowak', situation='decision.' + deal, text=frank(t), once='never', stance=opt, not_twice_in_one_talk=True,
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
    ('story.frankie', 'maureen_jensen', 'Frankie at the fourth rung: the Widow to own him, Danny to needle him, Ron once if ever (STORY-FRAME 1, renamed); one line each, in the scene that earns it.'),
    ('story.ron_way', 'ron_kirby', 'Ron giving the way by landmark when asked: he knows every road (GV-03); about 10 lines.'),
    ('story.name_said', 'any', 'Each named person\'s first saying of the next rung\'s name (the new owner, Nowak, Frank, Frankie), said to his face (7.7); the three who say Frankie: the Widow, Danny, Ron once.'),
    ('story.next_want', 'any', 'The Ledger\'s next named want in a person\'s own words, one per beat (STORY-FRAME 6, the next want).'),
    ('story.pauline_air', 'pauline_kitching', 'Pauline on the air, one set per rung and per week (STORY-FRAME 1 table), and the last day\'s calls.'),
    ('story.said_to_face', 'any', 'A named witness\'s remark returning each deed of weight within a game day (STORY-FRAME 7): one per kind of deed per witness kind.'),
    ('story.rival_rungs', 'kind:rival_head', 'Each rival\'s noticed, visit, pressure, threat and sit-down lines (2.10.1 to 2.10.3, RT-06).'),
    ('story.fares', 'kind:fare_person', 'Two rides\' lines for each of the 40 fare people (fares.json TO WRITE fields).'),
    ('story.side_stories', 'givers', 'Step lines for every side story (about 30 a story; side-stories/ TO WRITE fields).'),
    ('story.happenings', 'any', 'Lines for the happenings (happenings.json TO WRITE fields).'),
    ('story.endings', 'any', 'The close\'s voices per ending, up to about five lines (STORY-FRAME 8).'),
    ('story.decisions', 'any', 'Decision lines: a yes, a no and a line that keeps talking for every decision (3.6.5); the 170 not-a-plain-yes test lines.'),
]
for i, who, what in TOWRITE:
    story.append(rec(id=i + '.to_write', who=(who if who.startswith('kind:') or '_' in who else 'kind:' + {'any': 'anyone', 'givers': 'giver'}.get(who, who)), situation=i, text='TO WRITE (story lane): ' + what, once='game', src='STORY-FRAME-2026-11-26; BLUEPRINT-03'))
json.dump(dict(head('story.json', ['STORY-FRAME-2026-11-26 sample lines', 'production/lane/story/paper/ (being written in parallel)'],
    "Story-carrying lines. The words given are the frame's sample lines (not final script), kept so the one-shot has them; every bank the story needs is listed as TO WRITE for the story lane, whose scenes outrank these.",
    ["The story lane's paper (production/lane/story/paper/) had not landed when this file was made: every line here is replaced by its scenes when it does."]), lines=story),
    open(os.path.join(OUT, 'story.json'), 'w'), indent=1, ensure_ascii=False)

# ================= the line table (FIT F19): every situation, when it is live, who speaks it
allsits = Counter(l['situation'] for f in (shared, dirs, fl, story) for l in f)
for v in own.values():
    allsits.update(l['situation'] for l in v)
LIVE = {'greeting': 'Frank comes within 7 m of the speaker; rung by standing, regard by what the speaker holds of him', 'bumped': 'Frank walks into the speaker',
        'rain_starts': 'the weather turns to rain', 'in_rain': 'raining', 'crime_noise': 'a deed heard, not seen', 'crime_shape': 'a deed seen as a shape',
        'crime_face': 'a deed seen with a face known', 'after_deed': 'within a game day of a deed the speaker holds', 'asked_way': 'Frank asks the way',
        'farewell': 'a talk ends', 'neighbours': 'two speakers within 7 m who know each other', 'at_work': 'the speaker at a work row of his routine',
        'man_down': 'a body or a man down within sight', 'know': 'the knowing ladder (2.4.3): the step matches what the speaker holds', 'talk_of_deeds': 'bystanders within 7 m of each other, a deed of his in their memory',
        'everyday': 'any hour, no event (the floor that keeps 14 situations live)', 'direction': 'a passenger in Frank\'s car or at his side in a chase or a fare', 'voice': 'authored moments only',
        'suggest': 'the talk screen (3.6.6)', 'decision': 'the talk screen, a decision (3.6.5)', 'fixed': 'authored beats', 'story': 'authored scenes (the story lane)', 'own': 'once a day per person'}
table = []
for sit, n in sorted(allsits.items()):
    key = next((k for k in LIVE if sit.startswith(k)), 'story')
    table.append({"situation": sit, "lines": n, "live_when": LIVE[key]})
json.dump({"file": "line-situations.json", "version": "wave2-2026-11-24", "clock": CLOCK, "sources": ["lines/*.json", "BLUEPRINT FIT-F19, 3.6.3, 3.6.4, 2.4.3, 2.12.4"],
           "speaker_kinds": {k: {"what": v.get('what'), "members": members.get(k, [])} for k, v in BANK['speakers'].items() if k not in OWN_KIND},
           "extra_kinds": {"passenger": "whoever rides with Frank (Ron, a crewman, a fare who knows the town)", "rival_head": "Danny, the Widow, Agar (authored scenes)", "fare_person": "fares.json people", "giver": "a side story's giver", "anyone": "any speaker"},
           "regards": ["afraid", "angry", "likes", "appearance", "neutral"], "standings": ["stranger", "owner", "nowak", "frank", "portsman"],
           "standing_note": "stranger: knows nothing of him (shows nothing, 2.4.3); owner, nowak, frank, portsman: the four rungs (7.7). portsman is the fourth rung, where people still say Frank or Mr Nowak; Frankie is for three people only.",
           "situations": table}, open(os.path.join(D, 'line-situations.json'), 'w'), indent=1, ensure_ascii=False)

# ================= README (the structure, not a data file)
readme = """# lines/ (blueprint data file 10)

Made 24 Nov 2026 by the data-build wave 2 job. Every spoken or written line is a record (TECH-PLAN section 3): id, who (a people id or a speaker kind), situation, text, words, once (day, week, game or never), tokens, src. The record carries its own cool-down.

| File | What | Lines | Written | TO WRITE |
|---|---|---|---|---|
| shared-street.json | the street's shared lines by speaker kind (converted from the cloud week's bank), plus TO WRITE records for greetings by regard, everyday remarks, neighbours, at work, a man down, the knowing ladder and talk of his deeds | %d | the converted lines | one record per kind and bank |
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
print('dropped', dict(dropped))
print('content fails', len(fails))
for f in fails[:30]:
    print('  ', f)
sys.exit(1 if fails else 0)
