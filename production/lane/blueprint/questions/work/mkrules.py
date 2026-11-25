import json,collections
rows=json.load(open('rows2.json'))
exec(open('rulemap.py').read()); exec(open('ruletext.py').read())
fail=[r for r in rows if r['verdict'] in('partly','missing','contradictory')]
by=collections.defaultdict(list)
for r in fail: by[r['rule']].append(r)
subs=collections.defaultdict(collections.Counter)
for r in fail:
    if r['rulename']: subs[r['rule']][r['rulename']]+=1
order=sorted(G,key=lambda g:-len(by[g]))
L=["# Proposed general rules (25 Nov 2026)","",
"Each rule answers many player questions at once. Rules are ordered by how many failing questions they answer. Class: build means it changes how the game is built (data structures and systems), so it closes before the one-shot; content means animation, numbers, lines or props for the loops. Animation: none means talk and state only; clips means reuse of the small shared set; one or two bodies means new animation. The question ids are rows in QUESTIONS.csv. Working values are not set here; each rule is a direction for Monday's system pass, to be checked against canon, his rulings and the references there.","","Words used: the one-shot is the first full build from the blueprint; the loops are the rounds of content work after it; a slot is one thing a person holds about someone (a face, a coat, a deed); dials are each person's temper settings (nerve, greed, grudge, law); the claim check stops live talk saying what a person does not hold; the soft edge is the ring of places just off the walkable map; the fold rule is how a squeezed or threatened person gives way; a rung is a step on Frank's ladder of standing; can-you is how far a question goes beyond what KCD2, RDR2 and GTA V allow.","",
"| Rule | Questions | Build / content | Can-you (high / medium / low) | New animation (clips) | Monday pass |","|---|---|---|---|---|---|"]
summ=[]
for g in order:
    rs=by[g]; cc=collections.Counter(r['cls'] for r in rs); cy=collections.Counter(r['canyou'].split(':')[0].strip() for r in rs)
    an=collections.Counter(('two bodies' if r['anim'].startswith('two') else 'one body' if r['anim'].startswith('one') else 'clips' if r['anim'].startswith('clips') else 'none') for r in rs)
    pas=collections.Counter(r['pas'] for r in rs).most_common(1)[0][0]
    L.append(f"| {g} {G[g][0]} | {len(rs)} | {cc['build']} / {cc['content']} | {cy['high']} / {cy['medium']} / {cy['low']} | {an['one body']+an['two bodies']} ({an['clips']}) | {pas} |")
    summ.append((g,len(rs),cc,cy,an,pas))
L+=["",f"Total failing questions grouped: {len(fail)} (every one sits under a rule).",""]
for g,n,cc,cy,an,pas in summ:
    rs=by[g]
    cls='build, before the one-shot' if cc['build']>=cc['content'] else 'content, the loops'
    L+=[f"## {g}. {G[g][0]}","",T[g],"",
        f"- Answers: {n} questions ({sum(1 for r in rs if r['verdict']=='missing')} missing, {sum(1 for r in rs if r['verdict']=='partly')} partly, {sum(1 for r in rs if r['verdict']=='contradictory')} contradictory).",
        f"- Class: {cls} ({cc['build']} build, {cc['content']} content).",
        f"- Can-you: {cy['high']} high, {cy['medium']} medium, {cy['low']} low.",
        f"- Animation: {an['none']} none, {an['clips']} from the shared clips, {an['one body']} one body, {an['two bodies']} two bodies.",
        f"- Monday pass: {pas}.",
        "- Folds in the answerers' narrower rules: "+'; '.join(f"{k} ({v})" for k,v in subs[g].most_common())+'.',
        "- Questions: "+', '.join(r['id'] for r in rs)+'.',""]
open('/home/claude/lane/production/lane/blueprint/questions/RULES.md','w').write('\n'.join(L))
print('\n'.join(L[4:32]))
