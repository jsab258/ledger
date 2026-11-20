import json,re,collections,os
S='/tmp/claude-0/-home-claude/41875b20-e387-5bb1-bc1f-8279467ea7a5/scratchpad'
OUT='/home/claude/ledger/production/lane/design-proof'
rows=json.load(open(S+'/rows0.json'))
where=json.load(open(S+'/where.json'))
GUARD='1.2.9 1.2.10 1.3.3 1.3.11 1.4.3 1.4.4 1.4.6 1.4.8 1.6.1 1.6.7 1.6.8 1.6.11 1.7.4 1.5.4 2.1.1 2.1.3 2.1.4 2.2.5 2.6.1 2.6.2 2.6.3 2.6.9 2.7.5 2.7.7 2.7.8 2.10.1 2.10.2 2.10.3 2.11.2 3.1.3 3.5.6 3.5.7 3.6.5 4.1.3 4.1.4 4.11.1 6.1.1 6.1.3 6.1.4 6.2.1 6.2.2 6.2.3 6.2.4 6.2.5 6.4 6.6 6.7 6.10 7.4 7.7 7.9 7.11'.split()
FELT='1.2.3 1.2.7 1.3.6 1.3.8 1.6.3 1.6.4 1.6.6 1.7.1 1.7.3 2.2.4 2.2.6 2.4.2 2.7.3 2.9.1 2.12.4 2.12.5 2.15.1 2.18 3.1.2 3.4.1 3.4.2 3.5.1 3.6.4 5.8.3 6.5 7.2 7.3 7.6 7.12 7.14'.split()
POINTER='2.6.6 2.7.1 2.7.2 2.8.1 2.8.2 2.9.2 2.10.4 2.11.1 2.11.3 2.12.2 2.12.3 2.15.2 3.5.2 3.5.3 3.5.4 3.5.5 5.5.1 5.5.2 5.5.3 5.5.4 5.5.5 5.5.6 5.5.7'.split()
UNDEF='6.8 8.2.1 10.7 10.9 10.11 10.12'.split()
# which study closes what
STUDY={
 'F':'PC measuring 23 to 28 Nov (feel: on foot, driving, fists, being seen, chases)',
 'H':'PC measuring 23 to 28 Nov (hour split, ACTIVITY-SHARES)',
 'T':'PC measuring 23 to 28 Nov (teardown: an hour of each reference game, every event listed)',
 'S':'story measure (cloud, running 20 Nov) and STORY-PATTERNS-STEAM (due after midnight 20/21 Nov)',
 'W':'Steam walkthrough study (six games, due after midnight 20/21 Nov)',
 'M':'MEASUREMENTS-NEEDED.md (new, for the order of 23 Nov)',
}
close={}
for i in '1.1.8 1.1.1 1.1.2 1.3.1 1.3.2 1.4.1 1.4.2 2.2.3 1.5.1 1.5.2 1.5.3 1.1.5 1.2.3 1.3.6 1.3.8 2.2.4 1.2.1 1.2.2'.split(): close[i]='F'
for i in '7.5 1.6.5 7.2 7.3'.split(): close[i]='H'
for i in '1.2.7 1.6.3 1.6.4 1.6.6 1.7.1 1.7.3 2.2.6 2.9.1 3.4.1 3.4.2 3.5.1 5.8.3 6.5 7.6 7.12 7.14 2.18 2.12.4 2.12.5 2.15.1 3.6.4 2.4.2 1.1.7'.split(): close[i]='T'
for i in '3.1.2 3.5.2 3.5.3 3.5.4 3.5.5 2.9.2 2.10.4 2.11.1 2.11.3 2.8.1 2.8.2 2.12.2 2.12.3 2.15.2 2.6.6 2.4.3'.split(): close[i]='S'
for r in rows:
    i=r['id']
    if r['status']=='RULE' or i in GUARD+FELT+POINTER+UNDEF:
        if i in UNDEF: r['status']='UNDEFINED'; r['basis']='part named but its standard is "none" and the description does not define it'
        elif i in GUARD: r['status']='MEASURED'; r['basis']='pass/fail rule (a guard or correctness test; no reference figure needed)'
        elif i in FELT: r['status']='UNMEASURED'; r['basis']='a felt number chosen by judgement, no reference figure behind it'
        elif i in POINTER: r['status']='UNMEASURED'; r['basis']='standard is only a pointer to a design section, no number or test'
        elif r['status']=='RULE': r['status']='UNMEASURED'; r['basis']='design rule only (not reviewed)'
    r['defined_in']=('ONE-SHOT-PROMPT: '+'; '.join(sorted(set(where[i])))+' | ' if i in where else '')+r['defined_in']
    if r['status'] in('PENDING','UNMEASURED','UNDEFINED'):
        k=close.get(i,'M'); r['closed_by']=STUDY[k]
    else: r['closed_by']=''
    r['source']='parts tree'
# 2.7.1/2.7.2/2.7.4/2.7.6/2.6.4 money and custody figures: 1990 research
for r in rows:
    if r['id'] in ('2.7.1','2.7.2'): r['closed_by']=STUDY['M']
# new rows
new=[]
def add(i,name,group,status,basis,defined,standard,test,ref,closed,source,parent=''):
    new.append(dict(id=i,name=name,group=group,felt=True,defined_in=defined,standard=standard,test=test,standard_source=ref,research=[],status=status,basis=basis,closed_by=closed,source=source,parent=parent))
AXg=[
 ('AX-01','Text and interface size, contrast and font','6.1, 8.9','AX-012 013 014 028 031 041 077 078 079 080','Text at least 18 px at 1080p, scalable to 200 percent, contrast 4.5 to 1 (XAG 101, 102)'),
 ('AX-02','Subtitle options','6.1.2','AX-021 062 063 065 066 082','Subtitles on by default before any sound; size, background and speaker name options (GAG, XAG 104)'),
 ('AX-03','Motion and comfort settings (shake, bob, blur, field of view, background movement)','1.1.2, 5.8.1','AX-015 016 052 058 059 095','Each motion effect can be turned off; field of view adjustable (GAG, XAG 117)'),
 ('AX-04','Audio options (separate sliders, mono, speech clarity)','5.5.7','AX-020 060 067 083 125','Master, voice, effects, ambience and music sliders; mono toggle (GAG, XAG 105)'),
 ('AX-05','Input options beyond the rebinding and toggles already in the description (reset to defaults, separate mouse and pad sensitivity and invert, no mashing)','6.6','AX-002 003 006 030 033 035 037 085 101 102 103 104','Every input rebindable for keys and pad, reset to defaults; sensitivity X and Y; invert per device; every hold has a toggle; no repeated-press requirement (GAG, XAG 107)'),
 ('AX-06','Menu usability (large stationary targets, back goes one level, focus visible, settings before play and from pause, all remembered)','6.4','AX-004 024 038 090 091 092 093 106 107 108 131 132','Pass of XAG 112 to 115 checks on every menu'),
 ('AX-07','Save thumbnails, rotating autosaves and never losing the only save (slots and autosave are already in the description)','7.8','AX-042 071 072 121 122 123','Several manual slots with a picture, time and place; autosave rotates at least three; a quit or crash never loses more than the last deed'),
 ('AX-08','Accessibility features listed in game and on the store page','6.4, 10.2','AX-025 026 054 099','A page in the menus and the store text lists every option (GAG basic, XAG 121)'),
 ('AX-09','Screen narration of menus','6.4','AX-084','Menus read aloud on option (XAG 106)'),
 ('AX-10','Pause and focus safety (pause on losing focus, alt-tab safe)','6.4','AX-120 128','The game pauses when the window loses focus; alt-tab never crashes or loses input'),
 ('AX-11','Information never by colour alone; key objects distinct','6.1.4, 6.2.1','AX-017 051 087','A colour-blind check of every cue passes'),
]
for i,n,par,ax,std in AXg:
    add(i,n,'Accessibility and PC settings','UNDEFINED','needed (public standard), not defined in the design','not defined (closest part '+par+')',std,'checklist pass by a tester on every screen','Game Accessibility Guidelines; Xbox Accessibility Guidelines; PC checks ('+ax+'; sources/a11y-pc.json)',STUDY['M']+' (write the standard into the design from the guidelines; no game measuring needed)','accessibility and PC standards (source e)',par)
GDg=[
 ('GD-01','Travel time across the playable map','6.9, 7.12','Crossing the Hook on foot and by car in a set number of real minutes, set from the reference games\' town crossing times','GD-030; RN none'),
 ('GD-02','Density: something to meet every so many metres or seconds on a street','7.12, 3.7','A count of things to do or notice per street minute, set from the teardown town pieces','GD-028; review theme "nothing to do"'),
 ('GD-03','Jobs done out of order and sequence breaks','3.5.6, 2.19','Every job tolerates its steps met early, late or skipped by another route; a rule and a test','GD-043'),
 ('GD-04','A second playthrough: what differs','7.15, 3.1.4','Named differences a replay meets (rival met first, endings, branch jobs), a count','GD-073; red team B70'),
 ('GD-05','Humour and a mix of tones','3.6, 3.2.3','Canon tone (dry British wit, seaside-postcard smut sparingly); a share of lines or scenes with a laugh, set from the review themes','CR-023; P15 review theme; canon Tone'),
 ('GD-06','Mods and community content','10.6','A yes or no and, if yes, what is opened','ST mods theme (KCD2, 3.8 percent of reviews)'),
 ('GD-07','Economy over weeks: what money buys and how it rises across 15 to 20 hours','2.7, 2.12','A money curve by act with sinks, set from reference games\' money over a playthrough','red team B13; critics: money too plentiful late (RDR2, GTA V)'),
 ('GD-08','The catalogue of jobs and stories per act (count, kinds, givers)','3.3, 3.5','Jobs per hour of play and kinds per act, set from the teardown and reference games\' mission counts','red team A8, B10'),
]
for i,n,par,std,ref in GDg:
    st='UNDEFINED'
    add(i,n,'Game shape (categories from design documents and talks)',st,'needed, not defined',"not defined (closest part "+par+")",std,'tester count or rule check',ref,STUDY['T'] if i in('GD-01','GD-02','GD-08') else (STUDY['M'] if i in ('GD-07','GD-03','GD-04','GD-05') else 'his ruling (scope)'),'design documents and talks (source f)',par)
rt=[l[2:] for l in open(S+'/redteam/real-gaps-v1.md').read().splitlines() if l.startswith('- ')]
for k,l in enumerate(rt,1):
    name,rest=l.split(':',1)
    parts=re.search(r'parts: (.*)$',rest).group(1)
    add('RT-%02d'%k,name.strip(),'Red team 1 (real gaps)','UNDEFINED','needed; the design mentions it but leaves the specifics a builder needs open',
        'partly, in the parts named',rest.split('(A')[0].split('(B')[0].strip(),'to be written with the definition','red team 1 (A and B), triage-v1.json',
        STUDY['S'] if k in (1,2,3,4,5,6,19) else STUDY['M'],'red team 1',parts)
OUTS=[
 ('OUT-01','Several playable leads','canon: the player is Tom Nowak'),
 ('OUT-02','First-person view','canon (Jafar, 24 Sep): third-person, never first-person'),
 ('OUT-03','Online or multiplayer','ruling 23 Sep: no multiplayer'),
 ('OUT-04','Alcohol and gambling','canon content rule; project facts'),
 ('OUT-05','A bigger map than the Hook and the docks','ruling 28 Oct: the Hook plus the docks; more districts after release'),
 ('OUT-06','Stats, levels, skill trees and survival meters','ruling 30 Oct and D33, D34: position, never numbers'),
 ('OUT-07','Crafting','ruling 23 Sep: buying, selling, fencing, no crafting'),
 ('OUT-08','Jumping and climbing walls','ruling 23 Sep: no jump (vaulting at set places to the recommended answer of his question 1)'),
 ('OUT-09','Minimap, waypoints, markers','D12, D20, D37: no minimap; a paper map and street signs'),
 ('OUT-10','Other spoken languages and translation','ruling 23 Sep: English only, text out of code'),
 ('OUT-11','American-style satire','canon Tone: never GTA-style American satire'),
 ('OUT-12','Game-over screen','D35, D58; ruling 30 Oct: no game over'),
 ('OUT-13','Children','canon content rule'),
]
for i,n,why in OUTS:
    add(i,n,'Left out by his rulings','OUT',why,'canon or RULINGS','-','S38 to S40 guards where they apply',why,'','rulings',''); new[-1]['ruling']=why
allrows=rows+new
json.dump({'made':'2026-11-20','note':'One row per part a player meets (parts tree leaves, group 9 machinery left out), plus rows added from the sources. OUTSIDE = Unreal-only work (looks, engine, performance on his PC), outside this proof.','statuses':['MEASURED','PENDING','UNMEASURED','UNDEFINED','OUT','OUTSIDE'],'rows':allrows},open(OUT+'/coverage.json','w'),indent=1,ensure_ascii=False)
c=collections.Counter(r['status'] for r in allrows); print(c, len(allrows))
print(collections.Counter(r['closed_by'][:30] for r in allrows if r['status'] in('PENDING','UNMEASURED','UNDEFINED')))
# second pass corrections
refre=re.compile(r'REFERENCE-MECH|PLAYERS|FEEL|footage|KCD2|GTA|RDR2|Sleeping Dogs|map-players',re.I)
VIS='4.1.1 4.1.2 4.2.1 4.2.2 4.2.3 4.3.1 4.3.2 4.3.3 4.3.4 4.3.5 4.3.6 4.3.7 4.3.8'.split()
for r in allrows:
    if r['source']!='parts tree': continue
    if r['status']=='MEASURED' and not r['basis'].startswith('pass'):
        r['basis']='reference figure' if refre.search(r['standard']+r['standard_source']) else 'his ruling, canon or a pass/fail rule'
    if r['id'] in ('1.2.1','1.2.2','1.2.4'):
        r['status']='PENDING'; r['basis']='first targets from FEEL-TARGETS-DRIVING, to be replaced by the measured game band'; r['closed_by']=STUDY['F']
    if r['id'] in VIS:
        r['status']='OUTSIDE'; r['basis']='its standard is the look (Unreal); its play content sits in the job, happening and route rows'; r['closed_by']=''
    if r['id']=='7.13':
        r['status']='UNMEASURED'; r['basis']='two values in use (45 s and 30 s a game hour); the reference games publish their day lengths'; r['closed_by']=STUDY['M']
json.dump({'made':'2026-11-20','note':'One row per part a player meets (parts tree leaves, group 9 machinery left out), plus rows added from the sources. OUTSIDE = Unreal-only work (looks, engine, performance on his PC), outside this proof.','statuses':['MEASURED','PENDING','UNMEASURED','UNDEFINED','OUT','OUTSIDE'],'rows':allrows},open(OUT+'/coverage.json','w'),indent=1,ensure_ascii=False)
c=collections.Counter(r['status'] for r in allrows); print('final',c, len(allrows))
print(collections.Counter(r['basis'] for r in allrows if r['status']=='MEASURED'))
