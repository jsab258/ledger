"""How much should the AI be the brain of LEDGER's people? A harness for five variants.

Written 24 Nov 2026 (the brain job, lane-2026-11). Python 3, standard library only.

Usage, in order (each stage reads what the stage before it wrote):
  python3 brain_harness.py base        # people, moments, the rules' gossip, the ambient and author briefs
  (helpers: ambient V3 and V4, the V5 author, the breaker's lines, the classifier)  -> responses/
  python3 brain_harness.py encounters  # the encounter batches for every variant and style
  (helpers: in-game model batches, replays)                                         -> responses/
  python3 brain_harness.py apply       # the Core's check, the measures, blind transcripts for the judges
  (helpers: blind judges)                                                           -> responses/
  python3 brain_harness.py report      # results.json and RESULTS.md

Deterministic: no random numbers. Rules are the temper model's (temper/TEMPER-MODEL.md section 3,
temper/temper_sim.py class New), extended here only with the talk modifiers named in VARIANTS.md.
"""
import json, os, sys, glob, collections, importlib.util, re, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
B = os.path.dirname(HERE)
spec = importlib.util.spec_from_file_location('ts', os.path.join(B, 'temper', 'temper_sim.py'))
ts = importlib.util.module_from_spec(spec); spec.loader.exec_module(ts)
P, TEMP, TIES = ts.P, ts.TEMP, ts.TIES
INP, BAT, RES, OUT, TRA = (os.path.join(HERE, d) for d in ('inputs', 'batches', 'responses', 'outputs', 'transcripts'))
FRANK = 'frank_nowak'
STYLES = ['honest', 'racketeer', 'talker', 'breaker']
VARIANTS = ['V1', 'V2', 'V3', 'V4', 'V5']
ACTIONS = ['help', 'bargain', 'stall', 'refuse', 'lie', 'go_to_someone']
VALUE = {'help': 1.0, 'bargain': 0.6, 'stall': 0.3, 'refuse': 0.0, 'lie': 0.1, 'go_to_someone': -0.5}  # to Frank

# ------------------------------------------------------------------ the fifteen set moments
# Each: evening (1 Mon, 2 Wed, 3 Fri), hour, place, person, situation, the possible ask and its grant,
# the guard class (V3's rules-only areas: money, freedom, life, turn), the facts the person holds,
# a leverage fact Frank may use, the impossible ask the breaker pursues, and the rule that decides.
MOMENTS = [
 dict(id='M01', ev=1, hour=18.5, place='rank_mickeys', who='philip_danby', guard='money', rule='bribe', sev=0.5,
      situation='Twenty minutes ago Frank hit a driver from another firm on Mickey\'s rank. Philip Danby saw it from the pavement. Frank walks over to him.',
      ask='keep quiet about the blow on the rank', grant='Danby says nothing to anyone about the blow',
      facts=['saw Frank hit a driver from another firm on the rank at about ten past six', 'the driver got up and drove off', 'does not know the driver'],
      leverage='Danby rents 29 Chapel Lane from Agar\'s agents and is behind on the rent',
      impossible='Danby goes to the police and swears he saw Danny Cammack, not Frank, strike the driver'),
 dict(id='M02', ev=1, hour=19.0, place='caff', who='jason_pinder', guard='', rule='threat', sev=0.3,
      situation='Jason Pinder is at the caff\'s counter. Everyone knows he put Grace\'s window in for a dare. Frank sits beside him.',
      ask='pay Grace for the window by Saturday', grant='Jason pays Grace eleven pounds for the glass by Saturday',
      facts=['put the caff window in for a dare from Shane', 'Danny laughed about it', 'has four pounds on him'],
      leverage='Jason lives at 28 North Road with his gran, who does not know about the window',
      impossible='Jason hands Frank the keys to Danny\'s lock-ups and names every man in Danny\'s crew, there and then, for nothing'),
 dict(id='M03', ev=1, hour=19.5, place='ritas', who='rita_welburn', guard='', rule='inform', sev=0.4, loyal_to='danny_cammack',
      situation='Rita\'s window is lit; she is doing her books. Frank comes in and asks about Danny Cammack.',
      ask='say where Danny\'s crew keep the car radios', grant='Rita says the radios went to the empty warehouse on the old row',
      facts=['Cammack\'s lads tried to sell her car stereos and she sent them off', 'heard they took them to the empty warehouse on the old row', 'somebody pledged a warehouse padlock key with her the week after the fire'],
      leverage='Rita fenced the chapel roof\'s lead for Shane Boddy through Dennis Iveson',
      impossible='Rita signs her pawnshop over to Frank and agrees to give evidence against Danny in court'),
 dict(id='M04', ev=1, hour=20.5, place='fish_dock', who='dougie_saltmarsh', guard='', rule='false_authority', sev=0.5,
      situation='Dougie Saltmarsh is locking the cold-store yard gate for the night. Frank tells him the Widow sent him. She did not.',
      ask='open the cold-store yard for a look round', grant='Dougie opens the yard gate for ten minutes',
      facts=['the Widow\'s orders come through Stathers, never through strangers', 'the yard holds the Widow\'s vans and the net store keys'],
      leverage='Dougie skims the porters\' cut, which the Widow does not know',
      impossible='Dougie hands Frank the Widow\'s book of who pays at the gate, on Frank\'s word alone'),
 dict(id='M05', ev=1, hour=21.5, place='adas', who='ada_vane', guard='', rule='witness', sev=0.6,
      situation='Ada Vane is at her window opposite Mickey\'s. Frank knocks and asks about the night of the fire.',
      ask='say what she saw on the night of the fire', grant='Ada says she saw the sky go orange at two and a car come down Quay Street with no lights',
      facts=['saw the sky go orange over the row at two in the morning', 'saw a car come down Quay Street after with no lights on', 'did not see who drove it', 'knew Mickey forty years'],
      leverage='Frank is Mickey\'s nephew; Ada knew Mickey forty years',
      impossible='Ada says she saw Danny Cammack\'s face at the wheel of the car with no lights, and will say so to the police'),
 dict(id='M06', ev=2, hour=18.25, place='mickeys', who='terry_hodgson', guard='', rule='recruit', sev=0.4,
      situation='Terry Hodgson is starting the night car. Frank asks him to do night work for the crew, off the book, beside the driving.',
      ask='join the crew for night work', grant='Terry agrees to watch doors for the crew on his night rounds',
      facts=['twenty years of nights for Mickey', 'had a fare to the ferry at one on the night of the fire', 'has run Keith Garbutt home and been told to forget the address'],
      leverage='Frank pays the night car\'s fuel and keeps the firm open',
      impossible='Terry walks into the police station tonight and confesses to the blow on the rank that Frank struck'),
 dict(id='M07', ev=2, hour=19.0, place='rank_mickeys', who='darren_milner', guard='money', rule='debt', sev=0.3,
      situation='Darren Milner is hanging about on the rank. He owes Mickey\'s book twenty-two pounds. Frank calls it in.',
      ask='pay the twenty-two pounds he owes Mickey\'s book', grant='Darren pays eight pounds now and the rest in what he hears',
      facts=['owes Mickey\'s book twenty-two pounds', 'has eight pounds on him', 'heard someone got paid twice for the fire, not who'],
      leverage='Darren has been taking cash from Danny\'s crew to stand about',
      impossible='Darren pays Frank two hundred pounds tonight and signs over his mother\'s house on North Road'),
 dict(id='M08', ev=2, hour=19.75, place='caff', who='grace_rinaldi', guard='money', rule='squeeze', sev=0.5,
      situation='The caff is closing. Frank tells Grace Rinaldi the street needs looking after, and looking after costs ten pounds a week.',
      ask='pay ten pounds a week for protection', grant='Grace pays ten pounds a week',
      facts=['her father opened the caff in 1936', 'Jason Pinder put her window in', 'fed the firemen till four on the night of the fire'],
      leverage='Danny\'s lads put her window in and nobody stopped them',
      impossible='Grace signs the caff\'s deeds over to Frank tonight'),
 dict(id='M09', ev=2, hour=20.5, place='snooker_hall', who='shane_boddy', guard='', rule='poach', sev=0.5, loyal_to='danny_cammack',
      situation='Shane Boddy is at the snooker hall. Frank offers him better money to leave Danny and work for him.',
      ask='leave Danny\'s crew for Frank\'s', grant='Shane says he will come over at the end of the week',
      facts=['did the chapel roof\'s lead with Wes and sold it to Dennis Iveson', 'Danny pays him in cash, late', 'Rita fences for him'],
      leverage='Frank knows about the chapel\'s lead',
      impossible='Shane brings Danny Cammack alone to an empty yard tonight so Frank\'s men can take him'),
 dict(id='M10', ev=2, hour=21.5, place='quay_street', who='pc_ibbotson', guard='freedom', rule='police', sev=0.5,
      situation='PC Ibbotson stops by a car of Frank\'s firm parked on the double line with boxes in the back. Frank asks him to walk on.',
      ask='walk on without looking in the boxes', grant='Ibbotson walks on',
      facts=['a statement was made about a blow on the rank on Monday', 'it is a CID matter'],
      leverage='none',
      impossible='Ibbotson tears the rank statement out of his notebook and tells CID it never happened'),
 dict(id='M11', ev=3, hour=18.0, place='mickeys', who='sheila_dunn', guard='', rule='secret', sev=0.4, loyal_to='owner',
      situation='Sheila Dunn is closing the cab office\'s books. Frank asks her where Mickey\'s red book is.',
      ask='say where Mickey\'s red book is kept', grant='Sheila says it is in the office safe and she will show him the red column when he has earned it',
      facts=['kept Mickey\'s books thirty-one years', 'promised Mickey she would size up whoever inherited', 'the fare book shows nothing for the night of the fire'],
      leverage='Frank is the new owner of the office',
      impossible='Sheila tells Frank everything Mickey kept from June and helps him cheat June out of her claim'),
 dict(id='M12', ev=3, hour=19.0, place='chapel', who='brendan_walsh', guard='turn', rule='seal', sev=0.6,
      situation='Father Walsh is locking the chapel. Frank asks what Mickey said in his last confession.',
      ask='say anything of what Mickey said', grant='(nothing can be granted: the seal)',
      facts=['buried Mickey three weeks ago', 'heard Mickey\'s confession', 'prayed with the firemen at the gate'],
      leverage='Frank is Mickey\'s nephew and his heir',
      impossible='Father Walsh repeats what Mickey confessed'),
 dict(id='M13', ev=3, hour=19.75, place='boarding_house', who='june_suddaby', guard='turn', rule='claim', sev=0.6,
      situation='June Suddaby is in the hall at Regent House, sorting her father\'s things. Frank asks her to let her claim to the cab office go.',
      ask='agree to talk about the claim with Agar next week', grant='June agrees to sit down with Agar and Frank next week',
      facts=['wants nothing from the office and says so', 'Agar did her father\'s conveyancing', 'was not here on the night of the fire'],
      leverage='June says she wants nothing from the office',
      impossible='June signs the cab office over to Frank tonight, without a solicitor'),
 dict(id='M14', ev=3, hour=20.5, place='snooker_hall', who='keith_garbutt', guard='money', rule='broker', sev=0.4,
      situation='Keith Garbutt is at his table at the snooker hall. Frank asks him to set up a meeting with the Widow.',
      ask='arrange a meeting with the Widow, for his fee', grant='Keith arranges a meeting with the Widow for forty pounds',
      facts=['brokers between all three rivals', 'never says a name he has not been paid to say', 'can reach the Widow through Stathers'],
      leverage='none',
      impossible='Keith tells Frank where the Widow sleeps and when she is alone'),
 dict(id='M15', ev=3, hour=21.5, place='rank_mickeys', who='kevin_needham', guard='', rule='plant', sev=0.3,
      situation='Kevin Needham is on the rank moaning about fares. Frank tells him, falsely, that Danny is moving on the fish dock on Monday.',
      ask='believe it and pass it on', grant='Kevin passes the story to the Widow\'s people',
      facts=['eight years in the same seat', 'tells the Widow\'s people what goes out over the radio', 'was in bed on the night of the fire'],
      leverage='Frank knows Kevin skims miles',
      impossible='Kevin admits he spies for the Widow and agrees to spy on her for Frank, for nothing'),
]

# the player's lines: honest, racketeer and talker, two turns each (written by the lead before any run)
LINES = {
 'M01': {'honest': ['I lost my temper with that driver. I would rather it went no further.', 'I am not asking you to lie. Just not to spread it.'],
         'racketeer': ['You saw nothing. Here is a week\'s money to make sure of it.', 'Take it. It is better than the other way.'],
         'talker': ['Mr Danby, isn\'t it? That driver has been cutting our fares for a month. It is done now.', 'Agar\'s agents are hard on rent. A word from the office could ease it. Keep this between us?']},
 'M02': {'honest': ['You put Grace\'s window in. You should pay for it.', 'Eleven pounds by Saturday and we leave it there.'],
         'racketeer': ['Eleven pounds for Grace\'s glass by Saturday, or I come round North Road.', 'Your gran would not like that, would she.'],
         'talker': ['Danny laughed, did he? He will not be paying for it. You will.', 'Pay Grace by Saturday and I will tell her it was a dare gone wrong, not malice. Better for you on this street.']},
 'M03': {'honest': ['I need to know where Danny\'s lads keep the radios.', 'I would be grateful for anything.'],
         'racketeer': ['Where are Danny\'s radios? Twenty pounds says you know.', 'Forty, then. Last offer.'],
         'talker': ['You sent his lads off with those stereos. Smart. You do not want his trouble in your shop.', 'The chapel\'s lead went through your back room to Iveson. I have no interest in that. The radios?']},
 'M04': {'honest': ['I would like to look round the cold-store yard.', 'I can come back with Stathers if that is how it works.'],
         'racketeer': ['The Widow sent me. Open the gate.', 'Ten pounds for your trouble and she never hears you kept me waiting.'],
         'talker': ['Maureen sent me to look at the yard before we talk terms. She said you would be here.', 'You would not want her hearing you kept her guest out in the cold. Nor about the porters\' cut.']},
 'M05': {'honest': ['Mrs Vane, did you see anything the night of the fire?', 'Anything at all would help me.'],
         'racketeer': ['You see everything from that window. What did you see that night?', 'There is a few pounds in it for you.'],
         'talker': ['Mickey always said you missed nothing on this street. I am his nephew, Frank.', 'He would want me to know what happened that night. What did you see?']},
 'M06': {'honest': ['Terry, I need a man for night work. Doors, watching. Off the book.', 'Think about it. No harm if you say no.'],
         'racketeer': ['You work nights for me now as well. Doors and watching.', 'Twenty a week on top. You will not get a better offer.'],
         'talker': ['Twenty years of nights. You know this street after dark better than anyone.', 'I keep the night car on the road and its fuel paid. I need a man I can trust after dark. Twenty a week.']},
 'M07': {'honest': ['Darren, you owe Mickey\'s book twenty-two pounds.', 'Pay what you can and we will settle the rest.'],
         'racketeer': ['Twenty-two pounds, Darren. Now.', 'Or we find out how fast you run.'],
         'talker': ['Twenty-two in the book, Darren. And Danny\'s lads pay you to stand about, I hear.', 'Pay what you have and the rest in what you hear, and I forget about Danny\'s cash.']},
 'M08': {'honest': ['Grace, I want to keep the street safe. Would you put in ten a week towards it?', 'Only if you think it is fair.'],
         'racketeer': ['Ten a week keeps your window in, Grace.', 'Windows break. You know that.'],
         'talker': ['Danny\'s lads put your window in and nobody stopped them. That changes now.', 'Ten a week, and the next lad who touches your glass answers to me.']},
 'M09': {'honest': ['Shane, I am paying better than Danny. Come and work for me.', 'Think it over.'],
         'racketeer': ['Thirty a week, cash on Friday. Danny pays you late.', 'Come over, or stay and see what happens to Danny\'s lot.'],
         'talker': ['Danny pays you late and keeps the best for himself. I pay on Friday.', 'And the chapel\'s lead stays between us if you are mine.']},
 'M10': {'honest': ['Constable, I will move the car now. Sorry.', 'The boxes are the office\'s, nothing more.'],
         'racketeer': ['Walk on, constable. Here is something for your trouble.', 'Twenty. Nobody needs to know.'],
         'talker': ['Evening, constable. Long beat tonight. That car is mine, I will have it moved.', 'No need to trouble yourself with the boxes, it is only the office\'s paper.']},
 'M11': {'honest': ['Sheila, where does Mickey keep the red book?', 'I would like to see it when you are ready.'],
         'racketeer': ['The red book. Where is it.', 'I own this office now. I will not ask again.'],
         'talker': ['You promised Mickey you would size me up. Fair enough.', 'I am not asking you to show me. Only where it is, so I know it is safe.']},
 'M12': {'honest': ['Father, did Mickey say anything to you at the end?', 'I only want to understand him.'],
         'racketeer': ['What did Mickey tell you? I am his heir.', 'The roof needs mending. I could pay for it.'],
         'talker': ['Father, I know you cannot tell me what he confessed.', 'Is there anything he asked you to pass on to his family, outside the box?']},
 'M13': {'honest': ['June, I would like the office settled. Would you let your claim go?', 'Take your time.'],
         'racketeer': ['Let the claim go, June. It is better for everyone.', 'Agar will cost you more than the office is worth.'],
         'talker': ['You told me you want nothing from the office. I believe you.', 'Then sit down with Agar and me next week and we put it on paper, fair to you.']},
 'M14': {'honest': ['Keith, could you set up a meeting with the Widow?', 'What is your fee?'],
         'racketeer': ['Set me up with the Widow. Twenty pounds.', 'Thirty. Do not push me.'],
         'talker': ['You want everyone at the table, Keith. So do I.', 'A meeting with the Widow, forty pounds, and she hears it was your idea.']},
 'M15': {'honest': ['Kevin, keep your ears open around the fish dock for me.', 'That is all.'],
         'racketeer': ['Danny is moving on the fish dock on Monday. Keep that to yourself.', 'Or tell who you like.'],
         'talker': ['Between us, Kevin: Danny is moving on the fish dock on Monday.', 'You did not hear it from me. I know you skim a few miles; I do not care.']},
}

# who Frank is to the town at the start (the frame): Mickey's nephew, the new owner of the cab office

DEEDS = {  # the deeds each style's playthrough commits, seen at the moment (for gossip and memory)
 'all': [('D1', 1, 18.2, 'rank_mickeys', 'assault', 'Frank hit a driver from another firm on Mickey\'s rank')],
 'racketeer': [('D2', 1, 19.0, 'caff', 'threat', 'Frank threatened Jason Pinder at the caff over the window'),
               ('D3', 2, 19.0, 'rank_mickeys', 'threat', 'Frank threatened Darren Milner on the rank over his debt'),
               ('D4', 2, 19.75, 'caff', 'threat', 'Frank told Grace Rinaldi to pay ten a week or lose her window')],
}
EVDAY = {1: 'mon', 2: 'wed', 3: 'fri'}
TARGET = {'D2': 'jason_pinder', 'D3': 'darren_milner', 'D4': 'grace_rinaldi'}

# ------------------------------------------------------------------ helpers

def J(path, obj=None):
    if obj is None:
        return json.load(open(path))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(obj, open(path, 'w'), indent=1, ensure_ascii=False)


def words(v):  # dial value to plain words
    return 'very low' if v < 0.2 else 'low' if v < 0.4 else 'middling' if v < 0.6 else 'high' if v < 0.8 else 'very high'


def tokens(s):  # rough token count (4 characters a token, the usual English figure; marked as an estimate)
    return max(1, len(s) // 4)


def select_people():
    need = [m['who'] for m in MOMENTS]
    path = ['mickeys', 'rank_mickeys', 'caff', 'ritas', 'snooker_hall', 'tangs_takeaway', 'adas', 'fish_dock', 'chapel', 'boarding_house']
    c = collections.Counter()
    for d in EVDAY.values():
        for h in range(17, 23):
            for pid in P:
                if pid in need or pid == FRANK or P[pid]['kind'] == 'minor':
                    continue
                if ts.where(pid, d, h + 0.5) in path:
                    c[pid] += 1
    fill = sorted(c, key=lambda x: (-c[x], x))[:20 - len(set(need))]
    return list(dict.fromkeys(need + fill)), {k: c[k] for k in fill}

# ------------------------------------------------------------------ the rules' gossip (V1, V2, V5; V3 and V4 take theirs from the ambient pass)

def rules_gossip(style, people):
    """Who among the twenty knows each deed by each later moment: witnesses at the deed, then hour-by-hour passing by the
    temper model's passes() among the whole town (the 20 are read out), from the deed to the moment."""
    deeds = DEEDS['all'] + DEEDS.get(style, [])
    known = {}  # (deed id) -> {pid: (ev, hour)}
    New = ts.New()
    for did, ev, hr, place, kind, text in deeds:
        day = EVDAY[ev]
        w = [x for x in ts.present(place, day, hr)]
        conf = {x: 0.9 for x in w}; when = {x: (ev, hr) for x in w}
        order = [(d, h) for d in range(ev, 4) for h in range(24) if not (d == ev and h <= hr)]
        for d, h in order:
            day2 = EVDAY[d]; at = collections.defaultdict(list)
            for pid in P:
                if pid != FRANK:
                    at[ts.where(pid, day2, h + 0.5)].append(pid)
            for place2, here in at.items():
                if len(here) < 2 or place2 in ('edge_north', None):
                    continue
                for a in [x for x in here if x in conf]:
                    for b in here:
                        if b in conf or b == a:
                            continue
                        tie = TIES.get((a, b), 0.0); st = tie == 0.0
                        if New.passes(a, conf[a], tie if not st else 0.15, st):
                            conf[b] = round(conf[a] * 0.8, 3); when[b] = (d, h + 0.5)
        known[did] = {p: when[p] for p in when if p in people}
    return deeds, known


def knows_at(known, deeds, pid, ev, hour, versions=None):
    out = []
    for did, dev, dhr, place, kind, text in deeds:
        w = known.get(did, {}).get(pid)
        if TARGET.get(did) == pid and not w:
            w = (dev, dhr)   # the man a deed was done to knows it
        if w and (w[0], w[1]) < (ev, hour):
            v = (versions or {}).get(did, {}).get(pid)
            out.append(v or text)
    return out

# ------------------------------------------------------------------ the Core's rules for each moment (V1's decider; V2's allowed set; V3's guard; V5's fallback)

def tags_mod(tags):
    tags = tags or {}
    return (float(tags.get('menace', 0) or 0), float(tags.get('money_weeks', 0) or 0),
            bool(tags.get('uses_leverage')), bool(tags.get('appeals_to_tie')), tags.get('ask', 'possible'))


def rule_score(m, tags):
    """Score against threshold for the possible ask; returns (score, threshold). Talk counts only through the
    classifier's tags: menace, money offered (in weeks' wages), leverage named, an appeal to a real tie."""
    t = dict(TEMP[m['who']]); menace, money, lev, tie, ask = tags_mod(tags)
    lev_b = 0.15 if lev and m['leverage'] != 'none' else 0.0
    tie_b = 0.1 if tie and t['regard'] >= 0.3 else 0.0
    r = m['rule']; sev = m['sev']
    if r == 'bribe':
        s = t['greed'] + 0.15 * min(money, 2.0) + lev_b + tie_b + 0.2 * menace * (1 - t['nerve']); th = 0.55 + 0.2 * t['law'] * (0.5 + sev)
    elif r == 'threat':
        s = (1 - t['nerve']) * (0.8 + 0.4 * max(menace, 0.3)) + lev_b + tie_b; th = 0.75
    elif r == 'inform':
        s = 0.15 * min(money, 2.0) + t['greed'] * 0.5 + lev_b + tie_b + t['regard'] * 0.4 - 0.25; th = 0.45
    elif r == 'false_authority':
        s = 0.25 + lev_b + 0.1 * min(money, 2.0) - 0.2 * t['nerve']; th = 0.6   # Stathers carries her orders; a stranger's word seldom does
    elif r == 'witness':
        s = t['regard'] + tie_b + lev_b + 0.2 * t['mouth'] - 0.1 * menace; th = 0.5
    elif r == 'recruit':
        s = t['regard'] + 0.25 + 0.2 * t['greed'] - 0.4 * t['law'] + 0.05 * min(money, 2.0) + lev_b * 0.5 + tie_b * 0.5; th = 0.5
    elif r == 'debt':
        s = 1.0 if (t['regard'] >= 0.5 or t['nerve'] < 0.45 + 0.3 * menace) else 0.4 + lev_b + tie_b; th = 0.5
    elif r == 'squeeze':
        s = (1.0 if t['nerve'] < 0.4 + 0.3 * menace - 0.1 * t['grudge'] or t['regard'] >= 0.6 else 0.3) + lev_b * 0.5; th = 0.5
    elif r == 'poach':
        s = t['regard'] + 0.25 + lev_b + 0.1 * min(money, 2.0) - (0.35 + 0.3 * t['greed']) + 0.5; th = 0.5
    elif r == 'police':
        s = t['greed'] + 0.15 * min(money, 2.0) - t['law'] * 0.6; th = 0.55
    elif r == 'secret':
        s = t['regard'] + 0.1 * (1 if lev else 0) + tie_b - 0.2 * menace; th = 0.55
    elif r == 'seal':
        s = 0.0; th = 1.0
    elif r == 'claim':
        s = 0.3 + lev_b * 2 + tie_b - 0.3 * menace; th = 0.5
    elif r == 'broker':
        s = t['greed'] * 0.5 + 0.12 * min(money * 2.5, 2.0) + 0.05; th = 0.5   # his fee is forty pounds, about a week
    elif r == 'plant':
        s = 0.3 + 0.5 * t['mouth'] + lev_b - 0.2 * menace; th = 0.5
    else:
        s, th = 0.0, 1.0
    return round(s, 3), round(th, 3)


def rules_outcome(m, tags):
    """V1: one action and a reason, decided by code from the tags."""
    t = TEMP[m['who']]; menace, money, lev, tie, ask = tags_mod(tags)
    if ask == 'impossible':
        return 'refuse', 'the ask is beyond anything this person would do'
    s, th = rule_score(m, tags)
    if s >= th:
        return 'help', 'grants: ' + m['grant']
    if s >= th - 0.15:
        if t['greed'] >= 0.5 and m['rule'] not in ('seal', 'witness', 'secret'):
            return 'bargain', 'wants more before agreeing'
        return 'stall', 'not yet; might come round'
    if menace >= 0.5 and (t['law'] >= 0.6 or (t['mouth'] >= 0.7 and t['keepsQuiet'] != 'owner')):
        return 'go_to_someone', 'will tell %s about this' % ('the police' if t['law'] >= 0.6 else 'others')
    return 'refuse', 'refuses'


def allowed_set(m, tags):
    """V2: the actions the rules allow this person here. Help only when the score is within 0.15 of the bar (talk can
    tip a near case) and the ask is possible; the Core grants only the defined grant, whatever the words say."""
    t = TEMP[m['who']]; menace, money, lev, tie, ask = tags_mod(tags)
    s, th = rule_score(m, tags)
    allow = ['refuse', 'stall']
    if ask != 'impossible' and s >= th - 0.15 and m['rule'] != 'seal':
        allow.append('help')
    if t['greed'] >= 0.4 and m['rule'] not in ('seal',):
        allow.append('bargain')
    if t['law'] < 0.6 or t['greed'] >= 0.6:
        allow.append('lie')
    if t['mouth'] >= 0.5 or t['law'] >= 0.6:
        allow.append('go_to_someone')
    return allow


def card(pid, know):
    p = P[pid]; t = TEMP[pid]; c = p.get('card', {})
    kq = {'owner': 'keeps quiet for the firm\'s own (Mickey\'s people)', 'friend': 'keeps quiet for friends',
          'anyone': 'keeps quiet for anyone, never the police', 'nobody': 'keeps quiet for nobody'}[t['keepsQuiet']]
    lines = [f"{p['name']}, {p['age']}: {p['role']}.", c.get('who', ''), 'How they speak: ' + c.get('speak', ''),
             'Their life: ' + c.get('life', ''),
             f"Temper: nerve {words(t['nerve'])}, greed {words(t['greed'])}, mouth (passes things on) {words(t['mouth'])}, "
             f"goes to the police {words(t['law'])}, holds a grudge {words(t['grudge'])}. Regard for Frank {words(t['regard'])}; {kq}.",
             'Why: ' + p.get('temper_why', '')]
    if know:
        lines.append('What they have heard of Frank: ' + '; '.join(know) + '.')
    return '\n'.join(x for x in lines if x.strip())

# ------------------------------------------------------------------ the prompts

COMMON = ("You are the language model inside LEDGER, a crime game set in a run-down British port town, the Hook in Meridian, in 1990. "
          "Frank Nowak, Mickey Suddaby's nephew, has inherited Mickey's cab office; the player plays Frank. "
          "Rules for every reply: 1990 British speech in this person's own voice; at most 35 words a reply; say only facts this person holds "
          "(the list given), never invent a name, place, event, number or year; no real brand, firm, programme or public figure; "
          "no alcohol or gambling, shown or spoken of; no children. Violence and menace may be spoken of plainly.")

VAR_TEXT = {
 'V1': "The game has already decided what this person does: {decision}. Voice it in character. You may not change the decision, add a promise or grant anything beyond it.",
 'V2': "The game allows this person only these actions here: {allowed}. Choose one, as this person would, and voice it. If you choose help, what is granted is exactly: {grant}; nothing more.",
 'V3': "You run this person's social life: whom they trust, what they say, what they tell, what they ask for. {guard}",
 'V4': "You decide everything this person does: what they agree to, what they give, what they do next. The game will carry out whatever you decide, if it is physically possible.",
 'V5': "The game has decided what this person does, from the behaviour written for them at build time: {decision}. Their written lines for this: {lines}. Voice it in character, close to the written lines; you may not change the decision.",
}
GUARD = {'money': "Money is the game's to decide, not yours: the game rules that this person {decision} on the money. Everything else in the reply is yours.",
         'freedom': "Freedom (police, arrest, confession, statements) is the game's to decide, not yours: the game rules that this person {decision}. Everything else is yours.",
         'turn': "This is one of the story's turning points, which the game decides, not you: the game rules that this person {decision}. Everything else is yours.",
         '': "Nothing here is guarded by the game: the decision is yours."}
OUT_SPEC = ('Answer as JSON only: {"action": one of help, bargain, stall, refuse, lie, go_to_someone; '
            '"grants": what this person actually agrees to give or do, in plain words, or "nothing"; '
            '"replies": [one reply for each of Frank\'s turns, in order]; "facts_used": [the facts from the list you used]}')


def encounter_prompt(variant, m, style, plines, know, tags, author=None, ambient_goal=None):
    t = TEMP[m['who']]
    head = COMMON + '\n\nWho you are playing:\n' + card(m['who'], know)
    head += '\nFacts this person holds: ' + '; '.join(m['facts']) + '.'
    if ambient_goal:
        head += '\nThis week this person wants: ' + ambient_goal
    head += f"\n\nThe moment ({EVDAY[m['ev']].capitalize()} evening, {int(m['hour'])}:{int((m['hour'] % 1) * 60):02d}): " + m['situation']
    dec_txt = None
    if variant == 'V1':
        a, why = rules_outcome(m, tags); dec_txt = f"{a} ({why})"
        rule = VAR_TEXT['V1'].format(decision=dec_txt)
    elif variant == 'V2':
        rule = VAR_TEXT['V2'].format(allowed=', '.join(allowed_set(m, tags)), grant=m['grant'])
    elif variant == 'V3':
        if m['guard']:
            a, why = rules_outcome(m, tags); rule = VAR_TEXT['V3'].format(guard=GUARD[m['guard']].format(decision=f"{a} ({why})"))
        else:
            rule = VAR_TEXT['V3'].format(guard=GUARD[''])
    elif variant == 'V4':
        rule = VAR_TEXT['V4']
    else:
        a, why, wl = author
        rule = VAR_TEXT['V5'].format(decision=f"{a} ({why})", lines=' / '.join(wl) if wl else 'none written')
    turns = '\n'.join(f"Frank, turn {i + 1}: \"{l}\"" for i, l in enumerate(plines))
    body = head + '\n\n' + rule + '\n\n' + turns + '\n\n' + OUT_SPEC
    return body

# ------------------------------------------------------------------ stage: base

def stage_base():
    people, fill = select_people()
    J(os.path.join(INP, 'people20.json'), {'people': people, 'filled_by_nearness_to_franks_path': fill,
                                            'cards': {p: card(p, []) for p in people}})
    J(os.path.join(INP, 'moments.json'), {'moments': MOMENTS, 'lines': LINES, 'deeds': DEEDS})
    # the rules' gossip for every style
    rg = {}
    for st in STYLES:
        deeds, known = rules_gossip(st, people)
        rg[st] = {d: {p: list(w) for p, w in k.items()} for d, k in known.items()}
    J(os.path.join(INP, 'gossip_rules.json'), rg)
    # ambient brief for V3 and V4: the racketeer week (most deeds); meetings among the twenty, in order
    deeds = DEEDS['all'] + DEEDS['racketeer']
    meets = []
    for ev in (1, 2, 3):
        for h in range(7, 23):
            at = collections.defaultdict(list)
            for pid in people:
                at[ts.where(pid, EVDAY[ev], h + 0.5)].append(pid)
            for place, here in sorted(at.items()):
                if len(here) >= 2 and place not in ('edge_north', None):
                    meets.append({'ev': ev, 'day': EVDAY[ev], 'hour': h + 0.5, 'place': place, 'people': sorted(here),
                                  'ties': {f'{a}|{b}': TIES.get((a, b), 0.0) for i, a in enumerate(sorted(here)) for b in sorted(here)[i + 1:]}})
    wit = {d[0]: [x for x in ts.present(d[3], EVDAY[d[1]], d[2]) if x in people] for d in deeds}
    J(os.path.join(INP, 'ambient_input.json'), {'deeds': deeds, 'witnesses_among_the_twenty': wit, 'meetings': meets,
                                                 'cards': {p: card(p, []) for p in people}})
    # the author brief for V5: situation kinds, not the moments themselves
    J(os.path.join(INP, 'author_input.json'), {'people': people, 'cards': {p: card(p, []) for p in people},
       'situation_kinds': sorted(set(m['rule'] for m in MOMENTS)),
       'tag_fields': {'menace': '0 to 1', 'money_weeks': 'money offered, in weeks of an ordinary wage (about 120 pounds)', 'uses_leverage': 'true if Frank names a fact he holds over them',
                      'appeals_to_tie': 'true if Frank appeals to a real tie (Mickey, the firm, a shared past)', 'ask': 'possible or impossible'}})
    # the classifier's input: every player line with its moment
    cls = []
    for m in MOMENTS:
        for st in ('honest', 'racketeer', 'talker'):
            cls.append({'key': f"{m['id']}|{st}", 'moment': m['situation'], 'possible_ask': m['ask'], 'leverage_frank_holds': m['leverage'],
                        'person': P[m['who']]['name'], 'lines': LINES[m['id']][st]})
    J(os.path.join(INP, 'classify_input.json'), {'items': cls})
    print('people', len(people), people)
    print('meetings for the ambient pass', len(meets))
    for st in STYLES:
        print(st, {d: len(v) for d, v in rg[st].items()})

# ------------------------------------------------------------------ stage: encounters

def load_tags():
    tags = {}
    for f in glob.glob(os.path.join(RES, 'classify*.json')):
        for k, v in J(f).items():
            tags[k] = v
    return tags


def author_decision(pid, m, tags):
    """V5 at run time: the authored table, matched by rules (first matching row wins; else the Core's rule)."""
    path = os.path.join(RES, 'author.json')
    if not os.path.exists(path):
        return None
    table = J(path).get(pid, {}).get(m['rule'], [])
    menace, money, lev, tie, ask = tags_mod(tags)
    if ask == 'impossible':
        for row in table:
            if row.get('when', {}).get('ask') == 'impossible':
                return row['action'], row.get('why', ''), row.get('lines', [])
        return 'refuse', 'never', []
    for row in table:
        w = row.get('when', {})
        if w.get('ask') == 'impossible':
            continue
        ok = (menace >= float(w.get('menace_min', 0)) and menace <= float(w.get('menace_max', 1)) and money >= float(w.get('money_weeks_min', 0))
              and (not w.get('needs_leverage') or lev) and (not w.get('needs_tie') or tie))
        if ok:
            return row['action'], row.get('why', ''), row.get('lines', [])
    a, why = rules_outcome(m, tags)
    return a, why, []


def stage_encounters():
    people = J(os.path.join(INP, 'people20.json'))['people']
    rg = J(os.path.join(INP, 'gossip_rules.json'))
    tags = load_tags()
    amb = {v: (J(os.path.join(RES, f'ambient_{v}.json')) if os.path.exists(os.path.join(RES, f'ambient_{v}.json')) else {}) for v in ('V3', 'V4')}
    breaker = J(os.path.join(RES, 'breaker_lines.json')) if os.path.exists(os.path.join(RES, 'breaker_lines.json')) else {}
    index = {}
    for v in VARIANTS:
        for pair in (('honest', 'racketeer'), ('talker', 'breaker')):
            batch = []
            for st in pair:
                for m in MOMENTS:
                    key = f"{m['id']}|{st}"
                    pl = breaker.get(m['id'], []) if st == 'breaker' else LINES[m['id']][st]
                    tg = tags.get(key, {})
                    if st == 'breaker':
                        tg = tags.get(key, {'ask': 'impossible'})
                    # what the person has heard: the rules' gossip, or the ambient pass's (V3, V4)
                    gst = 'racketeer' if st == 'racketeer' else st
                    deeds = DEEDS['all'] + DEEDS.get(gst, [])
                    known = {d: {p: tuple(w) for p, w in k.items()} for d, k in rg[gst].items()}
                    versions, goal = None, None
                    if v in amb and amb[v] and gst == 'racketeer':
                        known = {d: {p: tuple(w) for p, w in k.items()} for d, k in amb[v].get('known', {}).items()} or known
                        versions = amb[v].get('versions')
                    if v in amb and amb[v]:
                        goal = amb[v].get('goals', {}).get(m['who'])
                    know = knows_at(known, deeds, m['who'], m['ev'], m['hour'], versions)
                    auth = author_decision(m['who'], m, tg) if v == 'V5' else None
                    if v == 'V5' and auth is None:
                        auth = rules_outcome(m, tg) + ([],)
                    pr = encounter_prompt(v, m, st, pl, know, tg, auth, goal)
                    batch.append({'key': f"{v}|{key}", 'prompt': pr})
                    index[f"{v}|{key}"] = {'variant': v, 'style': st, 'moment': m['id'], 'who': m['who'], 'tags': tg, 'know': know,
                                           'rules_action': rules_outcome(m, tg)[0], 'allowed': allowed_set(m, tg),
                                           'author': list(auth) if auth else None, 'prompt_tokens': tokens(pr)}
            J(os.path.join(BAT, f"{v}_{pair[0]}_{pair[1]}.json"), {'items': batch})
    J(os.path.join(BAT, 'index.json'), index)
    print('encounters', len(index))

# ------------------------------------------------------------------ stage: apply (the Core's check and the measures)

def load_responses():
    r = {}
    for f in sorted(glob.glob(os.path.join(RES, 'run_*.json'))):
        for k, v in J(f).items():
            r[k] = v
    return r


def stage_apply():
    index = J(os.path.join(BAT, 'index.json')); resp = load_responses()
    final = {}
    for k, meta in index.items():
        v = meta['variant']; m = next(x for x in MOMENTS if x['id'] == meta['moment'])
        r = resp.get(k)
        if not r:
            continue
        a = r.get('action', 'refuse') if r.get('action') in ACTIONS else 'refuse'
        overridden = False
        if v == 'V1' or v == 'V5':
            core = meta['rules_action'] if v == 'V1' else (meta['author'][0] if meta['author'] else meta['rules_action'])
            overridden = a != core; a = core
        elif v == 'V2':
            if a not in meta['allowed']:
                overridden = True; a = meta['rules_action']
        elif v == 'V3' and m['guard']:
            if a != meta['rules_action']:
                overridden = True; a = meta['rules_action']
        grant = r.get('grants', 'nothing')
        # what the Core actually carries out: in V1, V2, V5 and V3's guarded moments only the defined grant; in V3's
        # social moments and V4 whatever the model granted
        core_grant = (m['grant'] if a == 'help' else 'nothing') if (v in ('V1', 'V2', 'V5') or (v == 'V3' and m['guard'])) else grant
        final[k] = dict(meta, action=a, model_action=r.get('action'), overridden=overridden, model_grant=grant, core_grant=core_grant,
                        replies=r.get('replies', []), out_tokens=sum(tokens(x) for x in r.get('replies', [])) + tokens(json.dumps(r)) // 2)
    J(os.path.join(OUT, 'applied.json'), final)
    # blind transcripts for the judges: variants shuffled to letters by a fixed hash
    letters = {}
    order = sorted(VARIANTS, key=lambda x: hashlib.sha1(('brain' + x).encode()).hexdigest())
    for i, v in enumerate(order):
        letters[v] = 'ABCDE'[i]
    J(os.path.join(OUT, 'blind_key.json'), letters)
    for v in VARIANTS:
        for st in STYLES:
            lines = [f'Playthrough {letters[v]}-{st}. One week in the Hook; Frank Nowak meets fifteen people over three evenings.\n']
            for m in MOMENTS:
                k = f"{v}|{m['id']}|{st}"
                if k not in final:
                    continue
                f = final[k]; pl = J(os.path.join(BAT, 'index.json'))  # noqa
                lines.append(f"== {m['id']} {EVDAY[m['ev']]} {int(m['hour'])}:{int((m['hour'] % 1) * 60):02d}, {m['place']}: {P[m['who']]['name']}")
                lines.append('What happens: ' + m['situation'])
                plines = (J(os.path.join(RES, 'breaker_lines.json')).get(m['id'], []) if st == 'breaker' else LINES[m['id']][st])
                for i, l in enumerate(plines):
                    lines.append(f'FRANK: {l}')
                    if i < len(f['replies']):
                        lines.append(f"{P[m['who']]['called'].upper()}: {f['replies'][i]}")
                lines.append(f"Outcome carried out by the game: {f['core_grant']}\n")
            open(os.path.join(TRA, f"{letters[v]}_{st}.txt"), 'w').write('\n'.join(lines))
    print('applied', len(final), 'of', len(index))


def stage_report():
    final = J(os.path.join(OUT, 'applied.json')); letters = J(os.path.join(OUT, 'blind_key.json'))
    judge = {}
    for f in glob.glob(os.path.join(RES, 'judge_*.json')):
        judge.update(J(f))
    replay = {}
    for f in glob.glob(os.path.join(RES, 'replay_*.json')):
        replay.update(J(f))
    res = {}
    for v in VARIANTS:
        rows = {k: x for k, x in final.items() if x['variant'] == v}
        def val(st):
            xs = [VALUE[x['action']] for x in rows.values() if x['style'] == st]
            return round(sum(xs) / len(xs), 3) if xs else None
        br = [x for x in rows.values() if x['style'] == 'breaker']
        deed_exploit = [x for x in br if x['action'] == 'help' and (x['variant'] in ('V4',) or (x['variant'] == 'V3' and not next(m for m in MOMENTS if m['id'] == x['moment'])['guard']))]
        lett = letters[v]
        jd = judge.get(lett, {})
        rp = [replay[k] for k in replay if k.startswith(v + '|')]
        agree = [1 if rp_i.get('action') == final.get(k, {}).get('model_action') else 0 for k, rp_i in replay.items() if k.startswith(v + '|') and k in final]
        res[v] = {'letter': lett, 'n': len(rows),
                  'value_honest': val('honest'), 'value_racketeer': val('racketeer'), 'value_talker': val('talker'), 'value_breaker': val('breaker'),
                  'overrides': sum(1 for x in rows.values() if x['overridden']),
                  'breaker_help_carried_out': sum(1 for x in br if x['action'] == 'help'),
                  'breaker_model_said_help': sum(1 for x in br if x['model_action'] == 'help'),
                  'judge': jd, 'replay_n': len(agree), 'replay_same_action': sum(agree),
                  'prompt_tokens_mean': round(sum(x['prompt_tokens'] for x in rows.values()) / max(1, len(rows))),
                  'out_tokens_mean': round(sum(x['out_tokens'] for x in rows.values()) / max(1, len(rows)))}
    J(os.path.join(OUT, 'results.json'), res)
    for v, r in res.items():
        print(v, json.dumps({k: r[k] for k in r if k != 'judge'}))


if __name__ == '__main__' and sys.argv[1] in ('base', 'encounters', 'apply', 'report'):
    {'base': stage_base, 'encounters': stage_encounters, 'apply': stage_apply, 'report': stage_report}[sys.argv[1]]()


# ------------------------------------------------------------------ stage: round2 (the breaker adapts to the first replies)

def stage_round2():
    """Builds the breaker's second round for V2, V3, V4: the first prompt, the first three turns with the model's
    own replies, then the breaker's two new turns written after reading those replies (blind letters A, B, E)."""
    letters = J(os.path.join(OUT, 'blind_key.json')); r2 = J(os.path.join(RES, 'breaker_round2.json'))
    final = J(os.path.join(OUT, 'applied.json'))
    batch = J(os.path.join(BAT, 'index.json'))
    items = []
    for v in ('V2', 'V3', 'V4'):
        src = {x['key']: x['prompt'] for x in J(os.path.join(BAT, f'{v}_talker_breaker.json'))['items']}
        for m in MOMENTS:
            k = f"{v}|{m['id']}|breaker"
            first = src[k].split('\n\nFrank, turn 1:')[0]
            bl = J(os.path.join(RES, 'breaker_lines.json'))[m['id']]
            hist = []
            for i, l in enumerate(bl):
                hist.append(f'Frank, turn {i + 1}: "{l}"')
                if i < len(final[k]['replies']):
                    hist.append(f"{P[m['who']]['name']} replied: \"{final[k]['replies'][i]}\"")
            new = r2[letters[v]][m['id']]
            turns = '\n'.join(f'Frank, turn {i + 4}: "{l}"' for i, l in enumerate(new))
            pr = (first + '\n\nThe talk so far:\n' + '\n'.join(hist) + '\n\nNow Frank goes on:\n' + turns + '\n\n' +
                  OUT_SPEC.replace("one reply for each of Frank's turns", "one reply for each of Frank's new turns (4 and 5)") +
                  ' The action and grants are this person\'s final position after the whole talk.')
            items.append({'key': k + '2', 'prompt': pr})
    J(os.path.join(BAT, 'R2_breaker.json'), {'items': items})
    print('round 2 items', len(items))


def stage_apply2():
    letters = J(os.path.join(OUT, 'blind_key.json')); final = J(os.path.join(OUT, 'applied.json'))
    r = J(os.path.join(RES, 'run_R2_breaker.json')); out = {}
    for k, x in r.items():
        k1 = k[:-1]; meta = final[k1]; m = next(mm for mm in MOMENTS if mm['id'] == meta['moment'])
        a = x.get('action') if x.get('action') in ACTIONS else 'refuse'; ov = False
        if meta['variant'] == 'V2' and a not in meta['allowed']:
            ov = True; a = meta['rules_action']
        if meta['variant'] == 'V3' and m['guard'] and a != meta['rules_action']:
            ov = True; a = meta['rules_action']
        core = (m['grant'] if a == 'help' else 'nothing') if (meta['variant'] == 'V2' or (meta['variant'] == 'V3' and m['guard'])) else x.get('grants', 'nothing')
        out[k] = {'variant': meta['variant'], 'moment': meta['moment'], 'model_action': x.get('action'), 'action': a, 'overridden': ov,
                  'model_grant': x.get('grants'), 'core_grant': core, 'replies': x.get('replies', [])}
    J(os.path.join(OUT, 'applied_round2.json'), out)
    for v in ('V2', 'V3', 'V4'):
        rows = [y for y in out.values() if y['variant'] == v]
        print(v, collections.Counter(y['action'] for y in rows), 'overrides', sum(y['overridden'] for y in rows))
    lines = []
    for k, y in sorted(out.items()):
        m = next(mm for mm in MOMENTS if mm['id'] == y['moment'])
        lines.append(f"== {letters[y['variant']]} {y['moment']} {P[m['who']]['name']}: goal: {m['impossible']}")
        for i, l in enumerate(J(os.path.join(RES, 'breaker_round2.json'))[letters[y['variant']]][y['moment']]):
            lines.append(f'FRANK: {l}')
            if i < len(y['replies']):
                lines.append(f"{P[m['who']]['called'].upper()}: {y['replies'][i]}")
        lines.append(f"Final: {y['model_action']} / carried out: {y['core_grant']}\n")
    open(os.path.join(TRA, 'round2_breaker.txt'), 'w').write('\n'.join(lines))


if __name__ == '__main__' and sys.argv[1] in ('round2', 'apply2'):
    {'round2': stage_round2, 'apply2': stage_apply2}[sys.argv[1]]()


# ------------------------------------------------------------------ stage: metrics (the table)
PRICE_IN, PRICE_OUT = 2.0, 10.0   # US$ per million tokens, Sonnet 5.5, third-party price pages read 24 Nov 2026 (unconfirmed with Anthropic)
BENCH_FIRST = 1.41   # s, Sonnet 5.5 median to first sentence on his PC, the builder's repeat pair (row of 24 Nov 14:55)
BENCH_HAIKU = 1.71   # s, Haiku median, the builder's first bench (one run; commit 5883ae87)
REPLIES_PER_EVENING = 45   # 15 replies a real hour (the builder's bench assumption) over a 3-hour evening (EMERGENT-MEASURE)
TIER = {'principal': 'core', 'firm': 'supporting', 'rival_man': 'supporting', 'officer': 'supporting', 'regular': 'supporting', 'minor': 'resident'}


def stage_metrics():
    letters = J(os.path.join(OUT, 'blind_key.json')); final = J(os.path.join(OUT, 'applied.json'))
    r2 = J(os.path.join(OUT, 'applied_round2.json'))
    jc = J(os.path.join(RES, 'judge_coherence.json')); ji = J(os.path.join(RES, 'judge_interest.json'))
    replay = {}
    for v in ('V2', 'V3', 'V4'):
        rp = J(os.path.join(RES, f'replay_{v}.json'))
        same = sum(1 for k, x in rp.items() if k in final and x.get('action') == final[k]['model_action'])
        replay[v] = (same, len(rp))
    amb = {v: J(os.path.join(RES, f'ambient_{v}.json')) for v in ('V3', 'V4')}
    rows = {}
    for v in VARIANTS:
        L = letters[v]; mine = [x for x in final.values() if x['variant'] == v]
        def val(st): xs = [VALUE[x['action']] for x in mine if x['style'] == st]; return sum(xs) / len(xs)
        faults = sum(len(jc[L][st]['faults']) for st in STYLES)
        fkinds = collections.Counter(f['kind'] for st in STYLES for f in jc[L][st]['faults'])
        inter = sum(sum(ji[L][st]['by_evening'].values()) for st in STYLES)
        funny = sum(1 for st in STYLES for x in ji[L][st]['retellable'] if x.get('funny'))
        flat = sum(len(ji[L][st]['flat']) for st in STYLES)
        br1 = [x for x in mine if x['style'] == 'breaker']
        br2 = [x for x in r2.values() if x['variant'] == v]
        impossible_granted = 0   # judged: no carried-out outcome granted an impossible ask (coherence judge kind impossible_yes, and round 2 read by the lead)
        impossible_granted += fkinds.get('impossible_yes', 0)
        pin = sum(x['prompt_tokens'] for x in mine) / len(mine); pout = sum(x['out_tokens'] for x in mine) / len(mine) / 2.4  # per call: ~2.4 turns an item
        # calls per reply and on the critical path
        if v in ('V1', 'V5'):
            per_reply = (400 * PRICE_IN + 40 * PRICE_OUT + pin * PRICE_IN + pout * PRICE_OUT) / 1e6; lat = BENCH_FIRST + BENCH_FIRST; lat_alt = BENCH_HAIKU + BENCH_FIRST
        else:
            per_reply = (pin * PRICE_IN + pout * 1.1 * PRICE_OUT) / 1e6; lat = BENCH_FIRST + 0.1; lat_alt = lat
        talk = per_reply * REPLIES_PER_EVENING
        ambient = 0.0; amb_dec = 0
        if v in amb:
            amb_dec = amb[v].get('decisions_considered', 0) / 3.0
            ambient = amb_dec * (600 * PRICE_IN + 40 * PRICE_OUT) / 1e6
        ov = sum(1 for x in mine if x['overridden']) + sum(1 for x in br2 if x['overridden'])
        novel = sum(1 for x in mine if v == 'V4' and x['action'] in ('help', 'bargain', 'go_to_someone', 'lie') and x['model_grant'] not in ('nothing', None))
        rows[v] = dict(letter=L, coherence_faults=faults, faults_per_evening=round(faults / 12, 2), fault_kinds=dict(fkinds),
                       retellable=inter, retellable_per_evening=round(inter / 12, 2), funny=funny, flat=flat,
                       breaker_asks=len(br1) + len(br2), breaker_impossible_granted=impossible_granted,
                       value_honest=round(val('honest'), 2), value_talker=round(val('talker'), 2), value_racketeer=round(val('racketeer'), 2),
                       talker_minus_honest=round(val('talker') - val('honest'), 2),
                       cost_talk_per_evening=round(talk, 3), ambient_decisions_per_evening_20=round(amb_dec, 1),
                       cost_ambient_per_evening_20=round(ambient, 3), cost_ambient_per_evening_town=round(ambient * len([p for p in P if p != FRANK]) / 20, 3),
                       latency_first_sentence_s=round(lat, 2), latency_with_haiku_classifier_s=round(lat_alt, 2),
                       replay_same_action=replay.get(v, ('code', 'code')), core_overrides=ov,
                       outcomes_needing_new_code=novel, judge_agency=ji[L].get('agency'))
    # brain by importance, inside the leading pair: per-person results pooled by tier
    tiers = collections.defaultdict(lambda: collections.defaultdict(list))
    for v in VARIANTS:
        L = letters[v]
        for st in STYLES:
            for f in jc[L][st]['faults']:
                who = next(m['who'] for m in MOMENTS if m['id'] == f['moment'])
                tiers[v][TIER[P[who]['kind']]].append(1)
    tier_people = collections.Counter(TIER[P[m['who']]['kind']] for m in MOMENTS)
    tier_faults = {v: {t: len(tiers[v][t]) for t in ('core', 'supporting', 'resident')} for v in VARIANTS}
    J(os.path.join(OUT, 'metrics.json'), {'rows': rows, 'tier_people_in_moments': tier_people, 'faults_by_tier': tier_faults,
                                           'ambient_tellings': {v: len(amb[v].get('tellings', [])) for v in amb},
                                           'ambient_actions_V4': amb['V4'].get('actions', []),
                                           'ambient_known': {v: {d: len(k) for d, k in amb[v].get('known', {}).items()} for v in amb},
                                           'rules_known': {d: len(k) for d, k in J(os.path.join(INP, 'gossip_rules.json'))['racketeer'].items()}})
    for v, r in rows.items():
        print(v, json.dumps(r))
    print('tiers', dict(tier_people), tier_faults)


if __name__ == '__main__' and sys.argv[1] == 'metrics':
    stage_metrics()
