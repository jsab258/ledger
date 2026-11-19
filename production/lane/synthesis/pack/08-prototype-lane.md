# 08. The prototype lane: drafts, the loop prototype after round 5, measures, panels, driving study, risks

Digest for the synthesis pack, 18 November 2026. Extracted from local files only; nothing here is new design. Numbers are copied as written; where two files differ, both are shown.

## Source keys

Paths from the repository root. Each item names its key plus section.

- SCOPE: production/lane/PROTOTYPE-SCOPE-DRAFT.md
- VSD: production/lane/PROTOTYPE-VS-DESIGN-2026-11-18.md
- COMBAT: production/lane/COMBAT-END-STATE-OPTIONS.md
- RISK: production/lane/RISK-REGISTER-WHOLE-GAME-DRAFT-2026-11-18.md
- SKEL: production/lane/SKELETON-FIRST-OPTIONS-2026-11-18.md
- PT1: production/lane/PROTOTYPE-PLAYTEST-1-2026-11-18.md
- REV1 to REV5: production/lane/REVIEWS-round1.md to REVIEWS-round5.md
- NEW0: production/lane/playtest-1/newcomer.md; NEW0R: production/lane/playtest-1200-rerun/newcomer.md; NEW1 to NEW5: production/lane/playtest-round1/ to playtest-round5/newcomer.md; SWEEP5: production/lane/playtest-round5/sweep.md
- DN, ND, RES, CL, README: tools/lane/prototype/project/DESIGN_NOTES.md, NOT_DONE.md, RESULTS.md, CHANGELOG.md, README.md
- DRV3: production/lane/synthesis/pack/sources/driving-round3-CHANGELOG.md

## 1. The lane drafts

### 1.1 Prototype scope draft (SCOPE)

Draft of 17 Nov, not ruled, 15 review fixes applied. His decision of 17 Nov: the browser loop prototype becomes the whole game in rough, playable form and the spec of record; art quality, animation, performance, voices, clothes and faces stay out (SCOPE, header).

Plan, in four waves with rough cloud hours (SCOPE, section 3):
- Wave 1 (66 to 126 h): the C# Core in the browser (15 to 27 h); the warehouse fire as ruled, replacing the prototype's invented one (3 to 6 h); witnesses and perception; gossip and memory; the Ledger; talk; standing and names; routines; street life; weather and light; saving.
- Wave 2 (63 to 112 h): money and debts; crime verbs; police and suspicion; combat with fists and street weapons (20 to 35 h); the cab office; getting hurt.
- Wave 3 (111 to 190 h): July's five guns, after fists pass his playtest; jobs, crew and empire firsts; the three rivals and the Fixer; love interests; camcorder and CCTV; story beats and endings (35 to 60 h).
- Wave 4 (31 to 68 h): the Hook and the docks; traffic; shops; three to five side stories.
- Total about 270 to 500 cloud hours, rough, not measured.
- Out: art, animation, performance, voices aloud, clothes, faces, AAA driving, minigames, Tom's past, districts beyond the Hook and the docks.
- Build: a source project building one HTML file with Node tests per system, on the same page (SCOPE, section 4).
- One simulation: preferred the C# Core in WebAssembly (about 2 to 4 MB, not measured; browser step not proved); fallback JavaScript rules checked against the same 102,960 golden answers (proved for three perception rules, 30 of 30 rows) (SCOPE, section 4).
- Recipe: five proposed new lines (skeleton before production, feel studies, skeleton as spec of record, nightly browser walk, review gates), confidence low to medium (SCOPE, section 5).
- Flag: the prototype's invented rule that Tom will not hit a woman, anyone 60 or over, or the priest is in neither canon nor combat-design.md and must not reach the Unreal spec unruled (SCOPE, section 2).

Open decisions (SCOPE, section 6):
- 1. One simulation, Core numbers winning (clock, gossip fading), .NET licence line: recommended yes.
- 2. Endings: three (the Kingdom with Quiet and Both as ways it turns out, the Straight Life, Burn Both) against the ruled two or three and the built five: recommended yes.
- 3. Budget within the week's production share and current Fable rules until wave 1 is played: recommended.

### 1.2 Prototype against the real game's rules (VSD)

Rule of settlement: canon, then rulings, then "one simulation": what the C# Core already has comes from the Core; what it lacks (fares, jobs, rent, clock, week shape) comes from the prototype. The prototype side was a hand reading of a minified bundle (VSD, intro and Limits).

Eighteen rows (VSD, The table), one line each:
1. Clock: prototype 45 s a game hour vs Unreal 30 s; recommends 45 s; owner.
2. Clock stops in talk: already agree.
3. Talk distance and rounds: C# 6 m every 6 game minutes wins over 4.8/8 m every 4; builder.
4. Who passes stories: any two named people vs only along 81 friendship ties; owner.
5. Retold certainty: x0.8 no floor vs x friendship x0.8, nothing under 0.2; recommends C#; owner.
6. Fading: heat halves in about 20 game hours vs certainty halves every 96; owner.
7. Temperament: 28 people with own numbers vs everyone at 0.5; recommends own values, measured first; owner.
8. Who reports: C# (seeing is enough, his 1 Oct ruling) wins; builder.
9. Who never reports: one list in the cast file; builder.
10. Arrest: C# Custody.cs times and free duty solicitor win over 4 hours and Agar's bill; builder.
11. When Ellis walks: C# rule (three of his day world, not before day 4) wins; builder.
12. Seeing and naming: C# five rungs win (canon's moat); builder.
13. Debt roster: prototype's five debts win (Iveson 80.00, Harrison 30.00, Milner 22.00, Drewery 15.00, Kettlewell 9.00); builder.
14. How a debtor pays: C# purses and part payments win; builder.
15. Money: prototype's pence and 23.50 start win, keeping C#'s idea that talk cuts income; builder.
16. Washing: prototype's fare-book rule (10.00 plus 80 percent of fares) wins over a flat 120; builder.
17. Rent: code to match Friday 18:00; builder.
18. Week shape: prototype's Monday to Friday wins, recorded; builder.

Also found: the retired Unity build's "A drink for Mickey" breaks the content rule, and two CoreTests checks carry the title; for FINDINGS.md (VSD, after the table).

Open decisions (VSD, Three decisions): 1. game hour A 45 s (recommended) or B 30 s; 2. story travel A one retelling along friendships, fading over four days (recommended) or B several retellings, fading in about a day; 3. own temperament A yes (recommended) or B everyone ordinary. Decisions 1 and 2 pull against each other: the first-hour bar (7 of 13 runs landing only at minute 30) was measured at 30 s, so A on both needs a re-run.

### 1.3 Combat end state (COMBAT)

Options (COMBAT, The options):
- A (recommended): fists and improvised weapons daily, guns rare, consequential, AAA in feel; no canon change; about 6 to 10 agent weeks after melee.
- B: guns as menace only; short of the July spec; about 3 to 5 weeks.
- C: set-piece gunfights with cover; needs a ruling against D24 "not a shooter"; about 3 to 5 months.
- D: GTA style; breaks D24 and the memory moat; counterpoint only.

Under A (COMBAT, roster, routes, after a shot, feel studies): sawn-off shotgun, old .38 revolver, .22 target pistol, heavy self-loading pistol, silenced .22, plus a proposed replica, all fictional makes; four routes through people (bought, stolen, taken, found once at Mickey's); a shot heard about 177 m by day, up to 250 m; unarmed officer first, armed officers tens of minutes later (judgement); Tom cannot die; feel studies melee first, then G1 to G5 (draw, shotgun at a wall, a shot at a man, Tom shot, the next morning). Settled by the session: no armed car in Meridian in 1990 (COMBAT, Settled by the session).

Open decisions (COMBAT, Decisions for you): 1. option A, recommended yes; 2. silenced pistol, recommended keep as one rare story item, never bought.

Status as written: RISK says "his option pick is still open" (RISK, item 1); CL rounds 3 and 4 cite "his combat pick of 18 Nov (option A with an escalation dial ... melee first)" (CL, lane rounds 3 and 4).

### 1.4 Whole-game risk register (RISK)

Would replace 6-RISKS.md (friends' build only, last reviewed 5 Oct). Ten risks, each with one fallback (change method, spend, or cut); reviewed monthly from 7 Dec 2026; a risk closes only when its test passed (RISK, header and How it is reviewed). Top risks in section 6.

### 1.5 Skeleton first (SKEL)

Professionals call it the horizontal slice (Tim Cain) or connected-systems playable (Borut Pfeifer); the story half is already decided by his 17 Nov decision (SKEL, Summary).

Options for Unreal (SKEL, Options):
- A (recommended): a grey Hook end to end after the friends' evening, before people are multiplied, the AI tester walking arrival to an ending nightly; docks last or not at all; about 2 to 4 weekly allowances, low confidence.
- B: the same after the Hook's first block of people passes, 4 to 8 W later.
- C: keep street by street.

Open decision: A, B or C; A keeps the words of "deep before wide" but changes its order, so it is his call (SKEL, The one-line decision). Open point: BalanceLab (200 runs a plan) shows Burn Both commonest in 10 of 12 rows, a cautious player reaching Kingdom up to 82 percent and Both 5 to 13 percent, Quiet never by construction; for the town task (SKEL, Open points).

### 1.6 Prototype playtest 1 (PT1)

AI playtester on Fable's second-round page, seed 19901120 (PT1, header). Faults (PT1, Faults): 1 talk gives nothing back (stock lines; Sheila's line to five questions; Ada's ten times); 2 the prompt names someone other than the person in front (10 cases); 3 bubbles with nobody there; 4 lines out of time; 5 a name shown before learned; 6 a stale to-do note; 7 talks dead after a debt line; 8 paid help buys nothing; 9 to 11 design feel for the main session (waiting 39 percent and talking 37 percent; three fares an hour; strangers bark only). Faults 1 to 8 were then fixed by the lane in round 1 (CL, lane round 1).

## 2. The prototype after round 5

### 2.1 What exists

- One page in three.js 0.187.0, no server; source one file per part; npm build and test (README).
- Area: the Hook around Quay Street plus a slice of Copper Row; the Parade left out; interiors as small sets (DN, Scope; Interiors).
- Monday 15 to Friday 19 October 1990; 45 s a game hour; clock stops in talk and reading (DN, Calendar and clock).
- All rule numbers in LEDGER.rules: 1,313 in 32 sections (CL, second round).
- Art: Quaternius CC0 bodies and animations, Poly Haven textures; 5.5 MB; 11.5 ms a frame at the bus stop on an RX 6700 (DN, Art pass).

Systems (DN sections named):
- Seeing: sight 4 m plus 44 m by light; field about 120 degrees; noise walk 5 m, run 12, cab 30, fight 26 (Witness numbers).
- Naming: familiarity x closeness; named above 0.36, "the new owner" above 0.2 (Naming).
- Names: the new owner 0.2, Nowak 0.5, Tom 0.8, Tommy 1.05; Sheila says "new management" (What they call him).
- Gossip: certainty down 20 percent a telling; heat halves in about 20 hours; a forced Tuesday telling (Gossip).
- Ledger: only what Tom noticed or was told; People, Day book, Open, Money; never deleted, struck through (The Ledger; CL first round 4).
- Talk: two-call live talk, written fallback, three suggested lines, decisions only by the game's own lines (Live talk; Talk pass).
- Money: start 23.50; fares 80p plus distance; fare book hides 10 pounds plus 80 percent; rent 18 pounds Friday (Money).
- Police: nightly statements; 4 to 7 hours, 25 to 40 pounds; Ellis walks Thursday and Friday above loudness 2.2 (Police).
- Fighting: ladder stare, square up, threaten, shove, strike, weapon out; the invented "will not hit" rule (Fighting).
- Hurt: no health bar; beaten, he wakes in Grace's kitchen for 8 pounds and half the tin (Getting hurt).
- Night work, invented: Monday holdall 60 pounds; Tuesday parcel 40; Wednesday Iveson's 80, 100 for doing it, at Ada's tea hour (Night work). The fire is invented, not canon (The fire).

Added by the lane rounds (CL):
- Round 1: the eight playtest fixes (facing rule 30 degrees; no repeat within a talk; bubbles within 20 m and in sight; greeting by hour; no early names; notes expire; Leave always offered; paid help gives something).
- Round 2: the carry under watch: PC Ibbotson walks a beat; seen within 16 m he calls out; stand and the bag is taken, run and it is a chase (lost after 7 s or 70 m unseen).
- Round 3: fists with weight: hit-stop 0.04/0.09/0.10 s; jab 0.28 s, heavy 0.70 s; walls; at most two men swinging; onlookers; breath; each debtor refuses in his own words.
- Round 4: face (0.06 nerve per onlooker within 12 m, at most 0.24); corners (0.2); G grabs a thing to hand (chair breaks after 2 blows, brick 3, lid 4; brace and hook never).
- Round 5: lines remembered and saved (own lines once a day, shared lines once a week per street); small talk answers the question; Lee stands, backed by Cammack, and it comes to blows at the shove.

Controls named: Z to wait; E talk and act; Tab suggested lines, Up, Down, Enter; L the Ledger, Q and E change part, / and a letter jumps, Esc closes; F2 folds the slip; C the coat; G a thing to hand; a pad drives only the Ledger (DN, Talk, screen and Ledger pass; CL first round 4 and lane round 4; NEW5, log; ND, section 7).

Tests: same_week, week, arrivals, nights, town, ledger_rules, layout, files, talk, oldsave, eyes, plus fixes1, watch2, melee3, melee4, talk5 (RES, The tests; CL).

### 2.2 Key design-note rules

- Invented choices are marked and are not canon (DN, header).
- Nothing on screen Tom could not know; watchers show it with bodies, noise by sound; a testing switch restores the meters (DN, Talk, screen and Ledger pass).
- The game writes every line that decides; the AI writes only follow-ups, never sees cards or secrets, and lines are dropped if over twelve words, naming unknowns, breaking content or agreeing or paying (DN, Talk pass).
- Only a yes decides; walking away leaves a thing open or is the quiet answer (DN, Talk pass: decisions).
- Ledger sureness from how Tom learned it: to his face sure; seen looking or paid for "thinks so"; two heads together "guesses" (DN, Screen pass).
- "Nobody saw" written after two game minutes unseen, never removed (DN, Rules table and retiming).
- Every walk fits with a quarter to spare, Tom away and at the rank (DN, Second round).
- No alcohol, gambling, children, shown drugs or slurs; brands invented; traffic keeps left; no long dashes or italics (DN, Content rules; House style).
- Not built: voices aloud, guns, minimap, second car, interiors beyond Ada's, the Parade, Tom's past (DN, Not built).

### 2.3 What is not done

- A talk closed in the person's voice stays open with only Leave; bubbles not hidden behind walls in rooms; only Ada's prompt and note checked for those faults (ND, Lane round 1).
- Walks arrive only in the two checked cases; elsewhere fixing it needs a decision (ND, 1).
- The retiming went further than asked: 22 longer rows, some stops removed (ND, 2).
- 1,053 zeros, ones and twos unexamined (ND, 3).
- The same-week proof does not cover fight blows or crashing the cab (ND, 4); the gossip table is one week each (ND, 5); measures played by script, not a person (ND, 6).
- Tuesday night pause not reproduced; pad only for the Ledger; no zip (ND, 7).
- Not checked: a real AI follow-up line, a second machine, a person playing a retimed week (ND, 8).
- Faces cannot age, no shadow maps, window light does not affect seeing; frame time unmeasured in a crowd or night fight (DN, Art pass).
- Melee not yet: closing in (C9), camera close-in (C10), kerb fall (C7) (CL, lane round 3).
- The facing rule picks the nearest inside 30 degrees, not the closest to straight ahead (CL, lane round 1); round 5's sweep still shows one prompt fault and one text overlap (SWEEP5; RES, round 5).
- Live AI talk untested by the playtester (RES, round 5).

## 3. The measures, rounds 1 to 5

AI playtester's newcomer hour, seed 19901120, booked at estimated human pace (NEW5, header). Panel: eight simulated reviewers reading only the playtester's record.

| Build | Talk | Waiting | Longest empty stretch | Tense per 30 min | Kinds of activity | Fights | Thumbs up of 8 | Hours before stopping | Sources |
|---|---|---|---|---|---|---|---|---|---|
| 12:00 page, first run | 37% | 39% | 11.5 min | not booked | 5 | 0 | not run | not run | NEW0; PT1 |
| 12:00 page rerun (build A) | 36% | 36% | 10.7 min | 5.5 | not stated | 0 | 0 | 0.19 | NEW0R; RES r1; REV1 |
| Round 1 (build B) | 22% | 37% | 11.8 min | 6.0 | 4 | 0 | 0 | 0.36 | NEW1; RES r1, r2; REV1 |
| Round 2 | 23% | 40% | 11.4 min | 7.5 | 5 | 0 | 0 | 0.70 | NEW2; RES r2; REV2 |
| Round 3 | 24% | 46% (runs 48, 46) | 13.5 min (runs 10.5, 13.5) | 15.0 | 6 | 0 | 0 | 0.72 | NEW3; RES r3; REV3 |
| Round 4 | 24% | 39% | 7.9 min | 18.0 | 6 | 0 | 1 | 0.69 | NEW4; RES r4; REV4 |
| Round 5 | 25% | 41% | 10.8 min | 19.5 | 7 | 1 | 2 | 0.57 | NEW5; RES r5; REV5 |

Notes as written:
- Kinds: 12:00 "walk, talk, sit in the cab, drive, take a fare" (PT1); round 1 "walk, talk, drive, wait" (RES r1); round 3 added fronting up, round 5 fighting (RES r3, r5).
- New things, first / second half hour: 52/11, 52/11, round 1 59/3 in RES but 47/18 in NEW1, 70/5, 69/4, 71/6, 69/14 (NEW files; RES).
- Pursuits and escapes: 0 in every round (RES; NEW5).
- Round 5 tense moments: 39, of which 28 seen doing it, 7 choices under pressure, 3 risks of being seen, 1 fight; to round 1 all were sightings at night (NEW5; RES r1).
- Round 5 fight: with Lee at 21.1 min, 20 s; Tom landed 6, took 2, blocked 6; one man down; 2 watchers (NEW5, Fights).
- Lines heard more than once: 11 in round 4, 4 in round 5 (RES r5). Prompt faults in the sweep: 10, 3, 5, then 1 (RES r1, r2; SWEEP5).
- Run-to-run noise on the empty stretch about 3 min; three round 5 runs gave 9.1, 12.0, 10.8 (RES r5).
- Study 2's bars, not reached: about 10 distinct activities per 30 minutes; nothing new for at most about 5 minutes (PT1; RES r1, r2; REV5).

## 4. The reviewer panels

Eight cards grounded in PLAYERS.md; a signal for the next round, never a gate (REV1, intro). Calibration: the panel told build A from B by cited evidence and hours, not thumbs (both 0); the within-talk repeat was cited by 7 of 8 on A and none on B; the theme scorer could not see it (REV1, Calibration).

### 4.1 Recurring complaints, ranked by citations summed over rounds 1 to 5

1. Free talk repeats (shared lines, across talks and people, then the same sign-offs): 6, 6, 8, 6, 6 = 32 (REV1 c2; REV2 c1; REV3 c1; REV4 c1; REV5 c2), plus 7 on build A. In round 5 it is each person's closing line ("Right, boss. I'd best watch the rank." three times).
2. Nothing tense, nothing kicks off (every debtor gives way): 8, 4, 4, 2 = 18 (REV1 c1; REV2 c3; REV3 c2; REV4 c2); round 5 has "the debt ladder the same five times", 1 (REV5 c4).
3. Waiting and empty stretches: rounds 3, 4, 5 at 6, 3, 7 = 16 (REV3 c3; REV4 c3; REV5 c1); in round 1 part of complaint 1, all eight. Top in round 5.
4. Every debtor refuses with the same line: 3, 5 = 8 (REV1 c3; REV2 c2); fixed in round 3 (CL, lane round 3).
5. Arrests leading nowhere visible: 5, 2 = 7 (REV3 c4; REV4 c4).
6. Talk-heavy opening (first action at 4.1 min): 2, 2 = 4 (REV1 c4; REV5 c3). Theme "slow opening, too much talk": 88, 62, 100, 62, 100 percent of reviews, against KCD2 10.7 and Mafia 14.0 (theme tables).
7. Ladder unexplained: 1 in round 3, then logged as expected friction (REV3 c5; REV4, REV5).
8. Sightings with no visible cost: 1 (REV2 c4). Period slips: round 1 only (REV1 c5).

Expected friction, not to fix: no waypoint or minimap, the facing-rule prompts, no tutorial pop-ups, the required AI-talk disclosure (REV1 to REV5). Round 5 themes: punished slow opening 100, boring 100, too short 75, thin story 62 percent; praised living world 50, story and characters, voices and humour 38 each (REV5, themes).

### 4.2 Quit moments

- Build A: story-first and crime-drama fans at 24 and 18 min (REV1).
- Round 1: impatient 2.4 to 3 min (opening speeches); sandbox and AI sceptic 4 to 5; immersion 7; period stickler 11; systems 17; two did not quit (REV1).
- Round 2: AI sceptic 4 min (Ron's three replies again); impatient 17 (dead air, empty cab); immersion and sandbox about 41 (the 11.4 min stretch); story-first 49 (no scene after minute 24); three stayed (REV2).
- Round 3: AI sceptic 4 (Ron repeats); impatient 27.5 and sandbox 29.5 (nothing new after 24.5); immersion 40; four stayed (REV3).
- Round 4: AI sceptic 3.5 (Ron repeats); impatient 17.7 (nothing new, empty cab); KCD2 fan 22.9 (back on the street a minute after arrest); GTA 44 (no chase or fight); four stayed (REV4).
- Round 5: impatient 3 (Sheila's nine speeches); GTA 5 (talk and waiting); AI sceptic 10 (Ron's sign-off twice); story 30; KCD2 fan 43 (inside the 10.8 min stretch); three stayed (REV5).

### 4.3 Exciting moments

- Round 1: Sheila reading the debt book (five); the reporter tracing Sheila's answer, "a fare book learns a sentence" (three); the first fare (one) (REV1).
- Round 2: the night carry past the constable and Hal's "No coat. Somebody'll have seen your face" (6 of 8); the debt book; the fare book catching the laundered money (REV2).
- Round 3: the holdall and Hal (4); the constable with a statement, "Go with him" or "Run" (3, new); the debt book (1); nobody named the fight sample (REV3).
- Round 4: the holdall and Hal (5); the arrest with "Run"; the statement coming back; the debt book (REV4).
- Round 5: the fight with Lee and the arrest after it (5 of 8, new); the holdall and Hal (2); fronting up Darren (1); none (1) (REV5).

### 4.4 Each round's chosen next step

- After round 1: one non-talk activity with tension (REV1), built as the carry (CL r2). After round 2: the melee round (REV2), built (CL r3). After round 3: debtors who stand (REV3); round 4 built face, corners, things to hand (CL r4). After round 4: talk memory with a standing debtor folded in (REV4), built (CL r5).
- After round 5, recommended: a new non-talk activity for the empty middle hour (cab fares with pressure, a fare carrying something, a followed passenger, or a break-in), with varied closing lines folded in (REV5, Next round's candidates).

## 5. The driving study, round 3 (Quay Run)

A separate Fable study. Round 2 met all 28 "ordinary" targets; round 3 changed direction: LEDGER is not a driving sim, cars fun and easy first, 1990 character second; what carries over is measured behaviour, never physics settings (DRV3, intro).

### 5.1 What it built

Part A (DRV3, Part A):
- A "game" target set as default. Retune: about a third more power (0 to 60 about 11 s); grip sideways 0.92 to 0.98, lengthways 0.96 to 1.43; wet 0.72 of dry; yaw inertia 1250 to 720 kg m2; centre of mass 0.52 to 0.44 m; steering lock 38.5 degrees; anti-lock; a two-way handbrake. Automatic and mild aids by default.
- Two tyre faults fixed; chase camera keeps a margin from walls, cars and lamp posts; FOV widens with speed; page-made engine, tyre, road, wind and impact sound; two-gear kickdown; a controller copy of the page for Chrome or Edge.
- 28 of 28 game targets met with aids, 24 of 28 without; 0 of 40 random 3 percent nudges broke one; a 60 mph key lane change swings the tail 11 degrees dry and settles in about 0.9 s (DRV3, Game targets; Character).

Part B (DRV3, Part B):
- On foot, third person; one button in and out (in 1.57 s, out 1.45 s; slide across 1.72 s); hinged front doors.
- Reacting traffic: keeps left, one set of lights, stops for people, horns, swerves, pulls in for police, goes round a stopped car where there is room, gives up after 60 s unseen. 8 driving, 19 parked, 10 pedestrians, one police car; up to 5 on full physics.
- Damage stages by closing speed: 2.8 mph none, 9.9 dented, 21.8 crumpled, 39.7 will not drive on; will not drive on from about 35 mph in one hit or 8 points (dent 1, crumple 3); crumpled pulls 0.9 degrees; R repairs (DRV3, Damage stages).
- A fictional police car and chase: reckless driving in its sight starts it; caught stopped within 9 m for 3 s, held up 6 s, or on foot within 8 m for 3 s; escape after 20 s unseen; 54 demo chases 39 percent escaped, 39 percent caught (DRV3, Police chase).
- Cost 0.30 ms of a 16.7 ms frame; soaks found no police contact at 5 mph or more and no camera inside a wall in 40 minutes (DRV3, Cost; Left running).

### 5.2 Known issues as listed (DRV3, What does not feel right yet)

Nobody had driven it by hand or played part B; low yaw inertia "may feel darty on the keys at speed", the first thing to try by hand; a locked sideways slide stops sooner than straight braking; synthetic engine tone; box figure through the sill; chase all or nothing; "Caught" leads to nothing; hit traffic shows no dents; pedestrians cannot be hurt; lanes beside parked cars block until the player looks away; thin chase on foot; police over-patient in traffic; demo driver too close. Not in the round: interior, weapons from the car, several police cars, new models. Not possible: hand driving, a real controller, listening, real-PC frame rate (DRV3, What could not be done).

### 5.3 The owner's two faults

Per the pack brief, the owner played about three minutes and reported (1) a pole hit left the car unable to move and (2) keyboard steering was jerky. The round 3 notes do not record these reports. Related lines only: four light poles were added (DRV3, Cost); a car reaches "will not drive on" from about 35 mph in one hit or at 8 points, with R to repair (DRV3, Damage stages), and the notes do not say how a pole hit is staged; on steering, the notes warn the 720 kg m2 yaw inertia "may feel darty on the keys at speed" and record step steer at 0.182 s to 63 percent of yaw rate against 0.15 to 0.25 (DRV3, What does not feel right yet; Game targets, M5.yaw_63_s).

## 6. The risk register's top risks

From RISK, The ten, ranked (L likelihood, I impact; hours estimates):

1. Combat does not reach AAA: nothing thrown in Unreal. L high, I high. Test one Unreal room, Tom against one man, timed to the feel sheet, about 14 session and 4 PC hours, by 1 Feb 2027. Fallback: Epic's Game Animation Sample with physics hit reactions.
2. Scope outruns the date: 44 named people; phases 2 to 10 at 52 to 71 weeks against about 54 to 30 Nov 2027. L high, I high. Test: time Ron then Sheila, multiply by 44, by 1 Feb 2027. Fallback: cut the docks to the first update.
3. Live talk cost: $0.12 an hour at 15 replies (counter $0.327); about $1.80 to 2.40 a playthrough today; replies per hour unmeasured. L med, I high. Test the bake-off under $4 plus a replies count, by 7 Dec 2026. Fallback: cache the briefing, cheaper arm or local model.
4. Accents fail a native ear. L med, I high. Blind listening sheet with at least three native listeners, by 15 Jan 2027. Fallback: recast from allowlisted sets on his yes; no paid panel.
5. The recipe does not transfer (history re-reading 53, 40, 24 percent of spend). L med, I high. A fresh session rebuilds one unit, by 21 Dec 2026. Fallback: runnable step lists.
6. Clothing stalls on the cloth engine. L high, I med. By 14 Dec 2026. Fallback: reuse MetaHuman and CC BY garments.
7. Card memory runs out (6,005 MB on 8 Nov; binding line about 4.7 GB). L high, I high. By 14 Dec 2026. Fallback: voice off the card.
8. Hair never passes. L high, I med. By 1 Feb 2027. Fallback: Houdini Indie, about $299 a year (unverified).
9. Estimates run two to five times over. L high, I med. By 4 Jan 2027. Fallback: move scope at the 1 Feb check.
10. Process overhead (records 13 and 11 percent against 15). L med, I med. By 7 Dec 2026. Fallback: fewer record kinds.

Rated high on both: 1 combat, 2 scope, 7 card memory. Every L and I is the lane's judgement (RISK, Not verified).
