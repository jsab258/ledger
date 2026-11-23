"""Build and score blind pairs for one LEDGER key scene against the shelf.

Build:  python ledger_pairs.py build CANDIDATE.md OUTDIR [--seed N]
        CANDIDATE.md holds one scene already rewritten to FORMAT.md (five headings, 330-370 words).
        Writes OUTDIR/judge_0.md .. judge_3.md (give each to a fresh Opus AND a fresh Sonnet judge
        with judge_prompt.txt; never both orders to one judge) and OUTDIR/meta.json.
Score:  python ledger_pairs.py score OUTDIR
        Reads OUTDIR/out_<k>_<model>.jsonl and prints the verdicts.

Pairs: the candidate against 4 clean admired and 4 clean forgettable shelf scenes, plus 4 shelf
control pairs (clean admired against clean forgettable) whose answer is known. Each pair in both
orders. A judge model that gets a control wrong in both orders is not counted for that run.
"""
import json, random, sys, os, glob

HERE = os.path.dirname(os.path.abspath(__file__))
SET = json.load(open(os.path.join(HERE, '..', 'set', 'scenes.json')))
BRIEF = open(os.path.join(HERE, '..', 'BRIEF-v1.md')).read().split('---', 1)[1].strip()


def build(cand_path, out, seed):
    rng = random.Random(seed)
    cand = open(cand_path).read().strip()
    n = len(cand.split())
    if not 320 <= n <= 380:
        sys.exit(f'candidate is {n} words; rewrite it to FORMAT.md (330-370) first')
    clean = [x for x in SET if not x['recognised']]
    adm = rng.sample([x for x in clean if x['label'] == 'admired'], 4)
    frg = rng.sample([x for x in clean if x['label'] == 'forgettable'], 4)
    ca = [x for x in clean if x['label'] == 'admired' and x not in adm]
    cf = [x for x in clean if x['label'] == 'forgettable' and x not in frg]
    controls = list(zip(rng.sample(ca, 4), rng.sample(cf, 4)))
    texts = {'LEDGER': cand}
    texts.update({x['id']: x['text'] for x in SET})
    pairs = [('L%02d' % i, 'LEDGER', x['id'], x['label']) for i, x in enumerate(adm + frg)]
    pairs += [('C%02d' % i, a['id'], f['id'], 'control') for i, (a, f) in enumerate(controls)]
    rng.shuffle(pairs)
    jx, jy = [], []
    for pid, one, two, kind in pairs:
        a, b = (one, two) if rng.random() < 0.5 else (two, one)
        jx.append((pid + 'x', a, b)); jy.append((pid + 'y', b, a))
    rng.shuffle(jx); rng.shuffle(jy)
    groups = [jx[:6], jx[6:], jy[:6], jy[6:]]
    os.makedirs(out, exist_ok=True)
    alias = {}
    for g, grp in enumerate(groups):
        txt = BRIEF + '\n\n'
        for pid, a, b in grp:
            shown = 'Q%03d' % rng.randrange(1000)
            while shown in alias:
                shown = 'Q%03d' % rng.randrange(1000)
            alias[shown] = (pid, a, b)
            txt += f'===== PAIR {shown}\n\n--- SCENE 1\n{texts[a]}\n\n--- SCENE 2\n{texts[b]}\n\n'
        open(os.path.join(out, f'judge_{g}.md'), 'w').write(txt)
    json.dump({'pairs': pairs, 'alias': alias}, open(os.path.join(out, 'meta.json'), 'w'), indent=1)
    print('built', len(pairs), 'pairs in both orders into', out)


def score(out):
    meta = json.load(open(os.path.join(out, 'meta.json')))
    alias = meta['alias']
    for model in ['opus', 'sonnet']:
        picks = {}
        for f in glob.glob(os.path.join(out, f'out_*_{model}.jsonl')):
            for line in open(f):
                if line.strip():
                    d = json.loads(line)
                    pid, a, b = alias[d['pair']]
                    picks[pid] = a if str(d['choice']).strip() == '1' else b
        if len(picks) < 2 * len(meta['pairs']):
            print(model, f'incomplete: {len(picks)} of {2 * len(meta["pairs"])} judgements; not scored')
            continue
        res = {'admired': [], 'forgettable': [], 'control': []}
        for pid, one, two, kind in meta['pairs']:
            x, y = picks.get(pid + 'x'), picks.get(pid + 'y')
            if kind == 'control':
                res['control'].append('right' if x == y == one else 'wrong' if x == y == two else 'tie')
            else:
                res[kind].append('LEDGER' if x == y == 'LEDGER' else 'shelf' if x == y == two else 'tie')
        ok = res['control'].count('wrong') == 0
        print(model, 'controls', res['control'], '(counted)' if ok else '(NOT counted: a control was wrong)')
        print('  against admired:', res['admired'])
        print('  against forgettable:', res['forgettable'])


if __name__ == '__main__':
    if sys.argv[1] == 'build':
        seed = int(sys.argv[sys.argv.index('--seed') + 1]) if '--seed' in sys.argv else 1
        build(sys.argv[2], sys.argv[3], seed)
    else:
        score(sys.argv[2])
