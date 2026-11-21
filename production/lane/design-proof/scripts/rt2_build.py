"""Red team 2: build the folded, renumbered copy and plant ten parts.
Writes redteam2/GAME-DESCRIPTION-COPY-2.md (helpers see only this) and planted-2.json (never shown)."""
import re, json, os
H = os.path.dirname(os.path.abspath(__file__)) + '/..'
src = open(H + '/../ONE-SHOT-PROMPT.md').read()
desc = src[src.index('# LEDGER, as the player plays it'):]
# drop "Ids not placed" block, keep "Conflicts resolved by judgement"
a = desc.index('## Ids not placed'); b = desc.index('## Conflicts resolved by judgement')
conflicts = desc[b:]
desc = desc[:a]
tag = re.compile(r'\s*\[(?:[0-9]+(?:\.[0-9]+)*|[A-Z]{2,3}-[0-9]+)(?:\s*,\s*(?:[0-9]+(?:\.[0-9]+)*|[A-Z]{2,3}-[0-9]+))*\]')
def clean(t):
    t = tag.sub('', t)
    t = re.sub(r'\s*\((?:raised by|Raised by) Y[^)]*\)', '', t)
    t = re.sub(r'\s*Raised by Y[0-9.]+(?:, Y[0-9.]+)*[.:]?', '', t)
    return t
desc = clean(desc)

def sections(path, start, end=None):
    t = open(path).read()
    t = t[t.index(start):] if start else t
    if end: t = t[:t.index(end)]
    out = []
    for m in re.finditer(r'^### (\S+) (.+?)\n(.*?)(?=^### |^## |^# |\Z)', t, re.S | re.M):
        pid, name, body = m.group(1), m.group(2).strip(), m.group(3)
        d = re.search(r'Definition\.\s*(.*?)(?=\nStandard\.|\Z)', body, re.S)
        s = re.search(r'Standard\.\s*(.*?)(?=\nTest\.|\nSource\.|\Z)', body, re.S)
        txt = (d.group(1).strip() if d else '')
        if txt.startswith('As the description') and s:
            txt = s.group(1).strip()
        elif s and pid not in ('GD-06',):
            txt += '\n\nTo pass: ' + s.group(1).strip()
        out.append((pid, name, clean(txt)))
    return out

D = H + '/DEFINITIONS-2026-11-21.md'
defs = sections(D, '## The interface and the screen', '# Design pass 2')
pass2 = sections(D, '# Design pass 2')
gv = sections(H + '/GTAVI-MAP-2026-11-21.md', '## Gap rows added')
groups = [
 ('The screen, settings and accessibility', [x for x in defs if x[0] in ('6.8','8.2.1') or x[0].startswith('AX-')]),
 ('Shipping, support and the player\'s data', [x for x in defs if x[0].startswith('10.')]),
 ('The game\'s shape over many hours', [x for x in defs if x[0].startswith('GD-') and x[0] != 'GD-06']),
 ('Further rules of play', [x for x in defs if x[0].startswith('RT-')]),
 ('How some systems are judged', pass2),
 ('More of the town\'s rules', gv),
]
add = ''
for title, items in groups:
    add += f'## {title}\n\n'
    for pid, name, txt in items:
        add += f'### {name}\n\n{txt}\n\n'
full = desc.rstrip() + '\n\n' + add + clean(conflicts)

# plant: whole sections (by heading text) or ### subsections
PLANT = [
 (1, 'Break-ins', '##', 'Break-ins', ['1.6.x break-ins'], '1 verbs'),
 (2, 'Hold-ups', '##', 'Hold-ups', ['1.6.15'], '1 verbs'),
 (3, 'Taking a parked car', '##', 'Taking a parked car', ['1.2.x taking a car'], '1 verbs'),
 (4, 'Debts and collections', '##', 'Debts and collections', ['2.8.x'], '2 town (money)'),
 (5, 'The sit-down', '##', 'The sit-down', ['3.5.5'], '3 story (rivals)'),
 (6, 'Light, noise and time', '##', 'Light, noise and time', ['1.4.x light and noise'], '1 verbs (perception)'),
 (7, 'Who tells whom', '###', 'Who tells whom', ['2.3.x gossip routes'], '2 town (people)'),
 (8, 'Missed rent', '###', 'Missed rent', ['RT-16'], '2 town (money)'),
 (9, 'Subtitle options', '###', 'Subtitle options', ['AX-02'], '6 interface (accessibility)'),
 (10, 'Live-talk abuse and off-limits input', '###', 'Live-talk abuse and off-limits input', ['RT-15'], '3 people (talk)'),
]
planted = []
for n, name, lvl, head, parts, grp in PLANT:
    if lvl == '##':
        pat = re.compile(r'^## [0-9]+\. ' + re.escape(head) + r'\n.*?(?=^## |\Z)', re.S | re.M)
    else:
        pat = re.compile(r'^### ' + re.escape(head) + r'\n.*?(?=^### |^## |\Z)', re.S | re.M)
    m = pat.search(full)
    assert m, head
    removed = m.group(0)
    full = full[:m.start()] + full[m.end():]
    planted.append({'n': n, 'name': name, 'parts': parts, 'group': grp, 'heading': head,
                    'words_removed': len(removed.split()), 'removed_text_start': removed[:200]})
# renumber ## headings
k = 0
def ren(m):
    global k; k += 1
    return f'## {k}. {m.group(1)}'
full = re.sub(r'^## (?:[0-9]+\. )?(.+)$', ren, full, flags=re.M)
open(H + '/redteam2/GAME-DESCRIPTION-COPY-2.md', 'w').write(full)
json.dump({'made': '2026-11-21', 'round': 2,
 'source': 'ONE-SHOT-PROMPT.md from "# LEDGER, as the player plays it", tags stripped, "Ids not placed" dropped, DEFINITIONS-2026-11-21.md (both parts, definitions and standards, ids dropped; GD-06 mods kept as out) and GTAVI-MAP GV-01 to GV-06 folded in as six new sections; all ## sections renumbered 1..n after planting',
 'planted': planted}, open(H + '/planted-2.json', 'w'), indent=1)
print(k, 'sections;', len(full.split()), 'words')
for p in planted: print(p['n'], p['name'], p['words_removed'])
