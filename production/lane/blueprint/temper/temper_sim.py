"""Temper check: a week of the town over the 119 named people, under the old four dials and the new five.

Written 24 Nov 2026 (the temper job). Usage: python3 temper_sim.py > temper_sim_output.txt
Reads data/people/*.json (routines), temper/old_four_dials.json (the retired dials), data/ties.json, temper/tempers.json (the new dials).
Deterministic: no random numbers; who is where comes from each person's routine.

The OLD rules are the Core's as built (PoliceFile.WouldReport, Gossip.Bribe/Intimidate, Debts, Empire squeeze,
recruit and poach, Gossip.Tick), with what the Core can actually see: nerve from the data, loyalty and greed at
their 0.5 defaults (nothing loads the data's dutiful or venal), gossip with no trait at all.
'OLD as intended' feeds the data's dutiful as loyalty and venal as greed, the most the four dials could do.
The NEW rules are TEMPER-MODEL.md section 3.
"""
import json, glob, os, collections

B = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(B, 'data')
P = {}
for f in sorted(glob.glob(os.path.join(D, 'people', '*.json'))):
    p = json.load(open(f)); P[p['id']] = p
TEMP = json.load(open(os.path.join(B, 'temper', 'tempers.json')))['people']
OLD = json.load(open(os.path.join(B, 'temper', 'old_four_dials.json')))['people']   # the retired fields, for the comparison
TIES = {}
for a, b, s, *_ in json.load(open(os.path.join(D, 'ties.json')))['ties']:
    TIES[(a, b)] = TIES[(b, a)] = max(s, TIES.get((a, b), 0))
DAYS = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
PLAYER = 'frank_nowak'


def day_ok(spec, day):
    if spec in (None, '', 'daily'):
        return True
    for part in spec.split(','):
        if '-' in part:
            a, b = part.split('-'); i, j, k = DAYS.index(a), DAYS.index(b), DAYS.index(day)
            if (i <= k <= j) if i <= j else (k >= i or k <= j):
                return True
        elif part == day:
            return True
    return False


def where(pid, day, hour):
    """The place a person's routine has them at, on that day at that hour (last entry at or before it)."""
    best = None
    for e in P[pid]['sched']:
        h, place = e[0], e[1]
        days = e[3] if len(e) > 3 else None
        if day_ok(days, day) and h <= hour + 1e-9 and (best is None or h >= best[0]):
            best = (h, place)
    return best[1] if best else P[pid].get('home')


# Who can see a deed at a place: that place plus the places that overlook it (Ada's window looks on Quay Street).
OVERLOOK = {'ritas': ['adas', 'rank_mickeys', 'mickeys', 'laveracks', 'newsagent'],
            'caff': ['launderette', 'newsagent'], 'newsagent': ['caff', 'ritas', 'adas'],
            'ferry_landing': ['snooker_hall'], 'dock_gate': ['widow_base', 'fish_dock'],
            'mickeys': ['adas', 'rank_mickeys', 'ritas']}
SEV = {'damage': 0.3, 'assault': 0.5, 'wounding': 0.7, 'robbery': 0.7, 'killing': 1.0}


def present(place, day, hour):
    seen = [place] + OVERLOOK.get(place, [])
    return [pid for pid in P if pid != PLAYER and where(pid, day, hour) in seen]


# ---------------------------------------------------------------- the two rule sets
class Old:
    name = 'OLD (as built: loyalty and greed 0.5)'
    def __init__(self, intended=False):
        self.intended = intended
        if intended: self.name = 'OLD as intended (dutiful as loyalty, venal as greed)'
    def t(self, pid):
        p = OLD[pid]; n = p['temperament']['nerve']
        L = p['temperament']['dutiful'] if self.intended else 0.5
        G = p.get('venal', 0.5) if self.intended else 0.5
        own = p.get('keepsQuiet') is True and L >= 0.6   # the old boolean, read as Mickey's own only where loyal
        return n, L, G, own
    def reports(self, pid, kind, menace, victim=False):
        n, L, G, own = self.t(pid)
        if own: return False
        if victim:
            if kind == 'damage': return True
            settle, fear = (0.4, 0.5) if kind == 'assault' else (0.6, 0.3)
            return L < settle and n >= fear
        if kind == 'killing': return L <= 0.575
        if kind == 'assault': return False
        return n >= 0.4 and L <= 0.575
    def yields(self, pid, T, menace): return self.t(pid)[0] <= 0.6
    def takes_bribe(self, pid, price, sev): return self.t(pid)[2] >= 0.3
    def joins(self, pid): return self.t(pid)[1] + 0.25 >= 0.55
    def folds(self, pid, menace): n, L, *_ = self.t(pid); return n <= 0.6 or L >= 0.6
    def debt(self, pid, menace):
        n, L, *_ = self.t(pid)
        return 'pays' if L >= 0.5 else ('begs' if n <= 0.5 else 'refuses')
    def poached(self, pid): return self.t(pid)[1] < 0.4
    def regard0(self, pid): return self.t(pid)[1]
    def slight(self, pid, r): return r - 0.15
    def week_recover(self, pid, r, r0): return r
    def passes(self, pid, conf, tie, stranger): return (not stranger) and conf * tie * 0.8 >= 0.2


class New:
    name = 'NEW (five dials)'
    def t(self, pid): return TEMP[pid]
    def reports(self, pid, kind, menace, victim=False):
        t = TEMP[pid]
        if t['keepsQuiet'] == 'owner': return False          # Mickey's own never go to the police about one of theirs
        s = SEV[kind]
        R = (t['law'] + 0.05 + 0.6 * (s - 0.5) - 0.35 * menace * (1 - t['nerve'])
             - 1.0 * max(0.0, t['regard'] - 0.5) + (0.25 if victim else 0.0))
        return R >= 0.5
    def yields(self, pid, T, menace): return TEMP[pid]['nerve'] < T * (0.8 + 0.4 * menace)
    def takes_bribe(self, pid, price, sev):
        t = TEMP[pid]; return t['greed'] + 0.15 * min(price, 2.0) >= 0.55 + 0.2 * t['law'] * (0.5 + sev)
    def joins(self, pid):
        t = TEMP[pid]; return t['regard'] + 0.25 + 0.2 * t['greed'] - 0.4 * t['law'] >= 0.5
    def folds(self, pid, menace):
        t = TEMP[pid]; return t['nerve'] < 0.4 + 0.3 * menace - 0.1 * t['grudge'] or t['regard'] >= 0.6
    def debt(self, pid, menace):
        t = TEMP[pid]
        if t['regard'] >= 0.5: return 'pays'
        if t['nerve'] < 0.45 + 0.3 * menace: return 'pays'
        return 'begs' if t['grudge'] < 0.5 else 'refuses'
    def poached(self, pid):   # asked of him as a crewman: regard after joining (+0.25) against a rival's money
        t = TEMP[pid]; return t['regard'] + 0.25 < 0.35 + 0.3 * t['greed']
    def regard0(self, pid): return TEMP[pid]['regard']
    def slight(self, pid, r): return r - 0.15 * (0.6 + 0.8 * TEMP[pid]['grudge'])
    def week_recover(self, pid, r, r0): return min(r0, r + 0.05 * (1 - TEMP[pid]['grudge']))
    def passes(self, pid, conf, tie, stranger):
        m = TEMP[pid]['mouth']
        if stranger and m < 0.7: return False
        if tie < 0.5 and m <= 0.2: return False
        return conf * tie * (0.5 + 0.9 * m) >= 0.2


# ---------------------------------------------------------------- the week
DEEDS = [  # (day, hour, place, kind): Frank's seen deeds in the test week
    ('mon', 11.0, 'ritas', 'damage'),      # puts Rita's window in
    ('tue', 10.5, 'caff', 'assault'),      # a slap across the counter
    ('wed', 12.0, 'newsagent', 'robbery'), # takes the till
    ('thu', 9.0, 'mickeys', 'wounding'),   # a man cut on the rank
    ('sat', 5.5, 'dock_gate', 'killing'),   # a man killed at the dock gate at the morning call
]


def gossip_week(rules, day0, hour0, witnesses, body=False):
    """Hour by hour to the end of the week: people at the same place meet; a teller passes the story on."""
    conf = {w: 0.9 for w in witnesses}
    told = 0
    d0 = DAYS.index(day0)
    for d in range(d0, 7):
        for h in range(0, 24):
            if d == d0 and h <= hour0: continue
            at = collections.defaultdict(list)
            for pid in P:
                if pid != PLAYER: at[where(pid, DAYS[d], h + 0.5)].append(pid)
            for place, here in at.items():
                if len(here) < 2 or place in ('edge_north', None): continue
                tellers = [x for x in here if x in conf]
                for a in tellers:
                    for b in here:
                        if b in conf or b == a: continue
                        tie = TIES.get((a, b), 0.0); stranger = tie == 0.0
                        if stranger: tie = 0.15
                        if (body and not stranger) or rules.passes(a, conf[a], tie, stranger):   # a body always passes (Gossip.cs)
                            conf[b] = round(conf[a] * 0.8, 3); told += 1
    return len(conf), told


def run(rules):
    out = []
    menace = 0.3
    profile = collections.defaultdict(list)
    out.append('== ' + rules.name)
    for day, hour, place, kind in DEEDS:
        w = present(place, day, hour)
        rep = [x for x in w if rules.reports(x, kind, menace)]
        body = kind == 'killing'   # at a body a threat or a bribe is refused (Gossip.cs, kept)
        th = [] if body else [x for x in rep if rules.yields(x, 0.5, menace)]           # Frank warns each would-be reporter off
        br = [] if body else [x for x in rep if x not in th and rules.takes_bribe(x, 1.0, SEV[kind])]   # then offers a week's money
        br2 = [] if body else [x for x in rep if x not in th and x not in br and rules.takes_bribe(x, 2.0, SEV[kind])]   # then two weeks'
        known, told = gossip_week(rules, day, hour, w, body=(kind == 'killing'))
        out.append(f'{day} {hour:05.2f} {kind:8s} at {place:10s} witnesses {len(w):2d}  would report {len(rep):2d} '
                   f'({100*len(rep)/max(1,len(w)):3.0f}%)  silenced by a word {len(th):2d}  bought {len(br):2d}+{len(br2)}  '
                   f'knows by Sunday {known:3d} of {len(P)-1} ({100*known/(len(P)-1):3.0f}%)')
        if kind in ('assault', 'wounding', 'robbery', 'killing'):
            menace = min(0.8, menace + 0.1)
    # the battery: every person, the same seven asks, the outcome vector is how visibly different they are
    town = [x for x in P if x != PLAYER]
    rows = collections.Counter()
    vec = {}
    m = 0.5
    for x in town:
        r0 = rules.regard0(x)
        r = rules.week_recover(x, rules.slight(x, r0), r0)
        v = (rules.reports(x, 'wounding', m), rules.reports(x, 'damage', m), rules.reports(x, 'killing', m),
             rules.yields(x, 0.5, m), rules.takes_bribe(x, 1.0, 0.7), rules.joins(x), rules.folds(x, m),
             rules.debt(x, m), rules.poached(x), round(r0 - r, 2) >= 0.1)
        vec[x] = v
        for i, name in enumerate(['reports a wounding', 'reports damage', 'reports a killing', 'yields to a word',
                                  'takes a week\'s money', 'joins on a need', 'folds to a squeeze', None,
                                  'leaves for a rival', 'still sore a week after a slight']):
            if name and v[i]: rows[name] += 1
        rows['debt: ' + v[7]] += 1
    uniq = len(set(vec.values()))
    rows['reporters of a wounding who take a week\'s money'] = sum(1 for v in vec.values() if v[0] and v[4])
    out.append('battery over %d people (menace 0.5):' % len(town))
    for k in ['reports a wounding', 'reports damage', 'reports a killing', 'yields to a word', "takes a week's money",
              'joins on a need', 'folds to a squeeze', 'debt: pays', 'debt: begs', 'debt: refuses', 'leaves for a rival',
              'still sore a week after a slight', "reporters of a wounding who take a week's money"]:
        out.append(f'  {k:32s} {rows[k]:3d}  ({100*rows[k]/len(town):3.0f}%)')
    out.append(f'  distinct behaviour patterns: {uniq} among {len(town)} people')
    alone = sum(1 for x in town if list(vec.values()).count(vec[x]) == 1)
    out.append(f'  people whose pattern nobody else shares: {alone}')
    big = collections.Counter(vec.values()).most_common(1)[0][1]
    out.append(f'  largest group behaving identically: {big}')
    return out, vec


if __name__ == '__main__':
    print('Temper check, one test week, %d named people (Frank excluded from the town\'s side).' % (len(P) - 1))
    print('Deeds: ' + '; '.join(f'{k} at {pl} {d} {h:05.2f}' for d, h, pl, k in DEEDS))
    allv = {}
    for rules in (Old(), Old(intended=True), New()):
        lines, v = run(rules); allv[rules.name] = v
        print(); print('\n'.join(lines))
    # a few people side by side under the new rules: the "reactions to the same event" test
    print(); print('== side by side, NEW, menace 0.5 (wounding seen / threat / week\'s money / joins / squeeze / debt / poached)')
    nv = allv['NEW (five dials)']
    for x in ['ada_vane', 'brenda_laverack', 'darren_milner', 'grace_rinaldi', 'norman_dent', 'rita_welburn',
              'kevin_needham', 'julie_kettlewell', 'lee_drewery', 'hal_metcalfe', 'margaret_lofthouse', 'alan_sowerby']:
        v = nv[x]
        print(f'  {x:20s} report {"Y" if v[0] else "-"}  yields {"Y" if v[3] else "-"}  bought {"Y" if v[4] else "-"}  '
              f'joins {"Y" if v[5] else "-"}  folds {"Y" if v[6] else "-"}  debt {v[7]:7s}  poached {"Y" if v[8] else "-"}')
