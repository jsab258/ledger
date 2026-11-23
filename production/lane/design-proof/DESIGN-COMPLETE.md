# The gate: when the design counts as complete

The design counts as complete, and the next one-shot prompt may be written from it, only when all four hold:

1. Every row of the coverage map (coverage.json) is MEASURED, DECIDED or OUT with his ruling. No row is PENDING, UNMEASURED or UNDEFINED. OUTSIDE rows (Unreal-only looks, engine, performance, and shipping business) are not judged here.
2. Every review theme of every game (Steam players and critics; KCD2, GTA V, RDR2 and the six walkthrough games; the eight-game story patterns) maps to a part with a test (themes.json).
3. Two red teams in a row, each of two fresh helpers given only the game description with ten parts silently removed, find no material gap that is not in the map.
4. In both of those rounds each helper catches at least 9 of the 10 planted gaps.

## Process guards (from the pre-mortem of 21 Nov, ways 3, 4 and 19; written by run 4, 21 Nov)

**G-A. MEASURED means a real figure.** A row counts as MEASURED for the gate only when its standard rests on one of: a reference game's measured number; a dated real-world figure or a dated published standard (law, regulator guidance, accessibility guidelines); or a pass-or-fail rule of his (his ruling, canon or his numbered decisions). Each MEASURED row says which in its field real_basis. A standard the design sessions chose is a design decision: status DECIDED, listed below for him to overturn. DECIDED rows pass condition 1 as decisions, never as measurements, and the gate's report always gives three numbers side by side: rows MEASURED, rows resting on a reference game's number or a dated real-world figure, and rows DECIDED. Applied to the map on 21 Nov by scripts/run4_guard.py (a first pass by rule and by hand; a later run may move a row with a stated reason): the 195 rows called MEASURED became 99 MEASURED and 96 DECIDED (two rows, 2.17 and 1.6.10, moved after the reviewer's sample check).

**G-B. What a material gap is.** Defined on 21 Nov, before red team 3, and not to be changed until the gate is met or round 4 is done. A gap a red team raises is material when it is a part missing or undefined in the design, and at least one of these holds:
1. a player would meet it in the first game week (Act I and the first week of Act II, or any hour of the 41 playthrough checks' first week);
2. it is a system edge that can end a session stuck (no way on without reloading or quitting);
3. it is a system edge that would break one of his rulings or canon (content rule, Tom cannot die, a car hurts and never kills, no game over, the map ruling, the length ruling, and the rest of RULINGS.md);
4. it would block one of the playthrough checks from being run or passed.
Anything else (taste, polish, more of something that exists, Unreal-only looks, a different design the helper would prefer) is not material: it is logged in that round's triage file as a note and goes on no list. Triage applies these four tests by name, line by line, and each material line names the test it meets.

**G-C. At most four red-team rounds.** Rounds 1 and 2 are done (19 and 22 gaps). Round 3 is on Sun 29 Nov and round 4 on Mon 30 Nov. There is no round 5: after round 4, whatever is still open goes to him once as a scope list, each item with what it would take and a recommendation (define it now, defer it after the one-shot, or cut it), and the gate is judged on his answers. If round 3 and round 4 are both clean, conditions 3 and 4 are met.

**G-D. The clock before red team 3.** His open C11 is settled before red team 3 (pre-mortem way 19). Its rows are PENDING his answer; both versions are written in DEFINITIONS-2026-11-21.md (design pass 3, the clock) so either answer drops in the same day.

## Where it stands, 23 November 2026, after run 5

| Condition | State |
|---|---|
| 1. Rows | Not met. 401 rows: 111 MEASURED, 132 DECIDED, 42 PENDING, 45 UNMEASURED, 0 UNDEFINED, 14 OUT, 57 OUTSIDE. Of the 111 MEASURED: 21 on reference-game numbers, 15 on dated real-world figures or published standards (together 36), 75 on his rulings or canon. Only two measuring-block numbers are solid by the five-sample rule so far (GTA VI's two-star wanted spell, a parked-car entry); the rest of the sheets are leads. |
| 2. Themes | Met as a mapping (all 242 themes on parts with a test); they close with condition 1. Not recomputed for the rows of runs 4 and 5, which hang on parts already mapped. |
| 3. Red teams | Not met. Round 1: 19 material gaps; round 2: 22; all defined. Clean rounds so far: 0. Rounds left: 3 and 4 (G-C). |
| 4. Catch rate | Round 1: 10 and 9 of 10. Round 2a: 10 and 8; round 2b after one brief fix: 9 and 10. |

Run 5 (23 Nov): his clock B written in (G-D met: the clock is settled before red team 3); design pass 4 took the chase off its 90 s timer (GTA VI's bar), reset the busiest-view crowd on the counted views, and measured car entry on GTA VI's five samples; a fresh reviewer's 14 points fixed once.

## What stands between the design and the gate, with dates

| What | Rows | Closed by | When |
|---|---|---|---|
| GTA VI's footage to solid, first: being seen with the search after sight is lost, G-rows (town crowd), driving, the split hour | GTA VI's column on the PENDING feel rows; DP5-C03; GD-02; FIT-G9; 2.6.10; 7.5 | PC, order n23-1, block 1 (about 15 h left) | Mon 23 to Tue 24 Nov |
| Car chases to solid in four games (GTA IV in Mafia's place): lost-chase and search lengths | DP5-C02, DP5-C03, FIT-F04 | PC, block 2 (about 6 h) | Tue 24 Nov |
| The feel block, KCD2 from the installed game first, with walk and run speeds and the teardown | the PENDING feel rows; 2 FEEL and 23 teardown UNMEASURED; FIT-G4, FIT-F21, FIT-F16 | PC, block 3 (about 78.7 h before the cheaper routes) | Tue 24 to Fri 27 Nov |
| The other footage studies to solid (street life, conversations, first hours, district, port towns' daytime counts) | GD-02's floor and ceiling, FIT-G9 and the study rows | PC, block 4 (about 15.5 h) | Wed 25 to Fri 27 Nov |
| Extra rows and the listening pass | 6 A and 8 listening UNMEASURED; GD-01, GD-07, GD-08, RT-10, RT-11, RT-19, 2.7.3 PENDING | PC, block 5 (about 16.5 h) | Thu 26 to Fri 27 Nov |
| 1990 prices (spending, guns) and who is out by hour | FIT-G8, RT2-14, FIT-G9, 2.1.2 | cloud: dated price sources; ONS time-use tables | by Thu 26 Nov |
| Cloud checks on the line table and the money run | FIT-F19, FIT-F24 | cloud, 0.5 h and 2 h | F19 by Thu 26 Nov; F24 by Sat 28 Nov |
| Checks on the next prototype build: the one-hit wreck's rate and something within 30 s | FIT-F05, FIT-F32 | cloud, 1.5 h on the build | by Sat 28 Nov; with no build they go to him with red team 4's list |
| Story content, Act III's shape, the ending rule, the successor | 5 UNMEASURED; GD-05, RT-01 to RT-03, RT2-04, RT2-15 PENDING | story v3 | by Sat 28 Nov 12:00 |
| The fit check and the players' questions again, on the defined design and the blueprint | before red team 3 | cloud | Sat 28 Nov |
| Red team 3: a fresh copy from the blueprint with design passes 2 to 4 folded in, ten new planted parts, the improved briefs, triage by G-B's four tests | conditions 3 and 4 | cloud, two fresh Opus helpers | Sun 29 Nov |
| Red team 4, the last round (G-C); anything still open goes to him once as scope with a recommendation | conditions 3 and 4 | cloud | Mon 30 Nov |
| The DECIDED list shown to him (132 rows, below), each his to overturn | condition 1 | the advisor | before the gate |

The measuring is the risk. STATUS.md prices about 134 PC hours to bring every number to five samples; the order gives n23-1 60. The gate holds its date only if the cheaper routes (code measurers, the cheap reader, installed games first, one stream for several studies) close that gap; Monday's reprice says whether they do. If not, the lean order in MEASUREMENTS-NEEDED.md runs first, and the rows left at Fri 27 Nov are listed here by name and move the gate by the days they take.

Earliest the gate can be met: Mon 30 Nov to Tue 1 Dec, if the measuring closes by Fri 27 Nov and red teams 3 and 4 are both clean. Otherwise no round 5: the open items go to him on Mon 30 Nov as scope and the gate is judged on his answers (about Tue 1 Dec), and any measuring still open pushes it later, inside the one-shot's plan date of Mon 7 Dec.

## DECIDED rows: design decisions for him to overturn

Each row below has a pass-or-fail standard the design sessions chose inside his rulings and canon. None rests on a reference figure or a rule of his. He may overturn any of them; until he does, they stand.

| Row | Part | Where its standard comes from |
|---|---|---|
| 1.2.9 | Repairs, plates and paint | DESIGN §5, §12, §18 |
| 1.2.10 | Taking a parked car | Q2 (open) |
| 1.3.3 | Targeting without lock-on | DESIGN §7 |
| 1.3.11 | Marks that last | DESIGN §2, §7 |
| 1.4.3 | Hearing his own noise | DESIGN §17 |
| 1.4.4 | Give-aways and the coat | DESIGN §2 |
| 1.4.6 | Seeing assist | DESIGN §2, §17 |
| 1.4.8 | Drawing a watcher away | DESIGN §2 |
| 1.5.4 | Pursuers | DESIGN §8 |
| 1.6.1 | Getting in | DESIGN §4 Break-ins |
| 1.6.7 | Getting rid of things | DESIGN §2, §7 |
| 1.6.8 | Using the world | DESIGN §17 |
| 1.6.10 | Tom's wardrobe | DESIGN §14; rulings 29 Sep, 3 Oct |
| 1.6.11 | Casing a place | DESIGN §4, §10 |
| 1.7.4 | Men at his side | DESIGN §7, §12 |
| 2.1.1 | Schedules of named people | DESIGN §2; aaa-s01-04 |
| 2.1.3 | Off-screen life | DESIGN §2 |
| 2.1.4 | Weather and hour change who is out | DESIGN §6 |
| 2.2.5 | Give-away rules | DESIGN §2 |
| 2.4.3 | Showing what people know | The description, section 5 (What a person catches; Who tells whom). |
| 2.6.1 | The beat constable | DESIGN §8 |
| 2.6.2 | Challenge and search | DESIGN §8 |
| 2.6.3 | Statements and the arrest rule | DESIGN §8 |
| 2.6.5 | DS Ellis and the four stages | DESIGN §8; ending signs 30 Sep |
| 2.6.6 | Armed response and the dial's police | The description, sections 21, 33; RT-12. |
| 2.6.7 | Traffic police and stops | DESIGN §5, §18 |
| 2.6.9 | Charges, bail and the office searched | DESIGN §8, §18 |
| 2.7.1 | Clean money and the fare book | The description, section 24; RT-17. |
| 2.7.2 | Night money and the tin | The description, sections 24, 26; RT-17. |
| 2.7.5 | Purses, tills and shops | DESIGN §9, §18 |
| 2.7.7 | Flows ledger | DESIGN §9 |
| 2.7.8 | Spending | DESIGN §9, §18 |
| 2.8.2 | Partial payment and the book | The description, section 25. |
| 2.9.2 | Keeping or ending the arrangement | The description, sections 36, 37; RT-04. |
| 2.10.1 | Rival ladders | DESIGN §13 |
| 2.10.2 | Rival eyes | DESIGN §13; Core rule |
| 2.10.3 | Pressures and answers | DESIGN §13 |
| 2.10.4 | The Fixer | The description, sections 29, 30; RT-06. |
| 2.11.1 | Recruiting | The description, section 27; RT-07. |
| 2.11.2 | Nerve, loyalty and breaking | DESIGN §12 |
| 2.11.3 | Crew fates | The description, section 27. |
| 2.12.2 | Rung table | The description, section 32; RT-04. |
| 2.12.3 | Access and soft keys | The description, section 32. |
| 2.14 | Each person's temper | QUESTIONS 3 (open since 29 Sep) |
| 2.15.2 | Ranks and accounts | The description, sections 28, 31. |
| 2.17 | Fronts and rackets held | DESIGN §14; canon |
| 3.1.3 | Act III, The Ledger Comes Due | DESIGN §16 |
| 3.1.5 | Ending signs and Tom's reading | DESIGN §16 |
| 3.5.5 | Sit-downs | The description, section 30; RT-06, RT-07. |
| 3.5.6 | Job template and step states | DESIGN §4; Studies 11, 16 |
| 3.5.7 | How jobs reach him | DESIGN §4 |
| 3.6.5 | Decision lines | DESIGN §11 |
| 4.1.3 | Landmarks and signs | DESIGN §4 |
| 4.1.4 | The soft edge | DESIGN §5; Study 2 |
| 4.11.1 | Yard dogs | DESIGN §2 |
| 6.1.1 | The prompt | DESIGN §17 |
| 6.1.3 | The belief line | DESIGN §10, §1 |
| 6.1.4 | Light and sound cues | DESIGN §2 |
| 6.2.1 | People | DESIGN §10 |
| 6.2.2 | Day book | DESIGN §10 |
| 6.2.3 | Open | DESIGN §10, §4 |
| 6.2.4 | Money in words | DESIGN §9 |
| 6.2.5 | Tom's reading | DESIGN §10, §16 |
| 6.4 | Menus | DESIGN §17; basics 1 to 5, 19 |
| 6.6 | Controls | DESIGN §17 |
| 6.7 | Talk screen | DESIGN §11 |
| 6.8 | Photo mode | Ruling 23 Sep (optional presentation allowed); the camera rule; GTA V and RDR2 photo modes |
| 6.10 | Letters and papers in hand | DESIGN §17 |
| 7.4 | Acts II and III pacing | DESIGN §16 |
| 7.7 | Rising in position, felt | DESIGN §14 |
| 7.9 | Failure without reload | DESIGN §1 |
| 7.11 | Waiting and time skips | DESIGN §4, §6 |
| 7.16 | Pastimes | Q3 (open); canon |
| 8.10 | Collision and physics | ER-CORE-01; ER-FIGHT-06; the description, sections 10, 11. |
| 10.7 | Platform account, cloud saves and achievements | The description, section 3 (no meters); VISION (no stats or counts); Steamworks Cloud as c |
| 10.9 | Player support and community | The description, section 34 (line report); sources/a11y-pc.json (PC expectations). |
| AX-07 | Save thumbnails, rotating autosaves and never losing the onl | The description, section 3 (saving); ER-SAVE-01; PC players' expectation from the players  |
| AX-10 | Pause and focus safety (pause on losing focus, alt-tab safe) | PC players' expectations (sources/a11y-pc.json, PC section); the description, section 3 (E |
| GD-03 | Jobs done out of order and sequence breaks | The description, sections 14 and 3 (no game over, never stuck); the review studies (missio |
| RT-04 | Act transitions and stall paths | The description, sections 29 (ladder never skips a rung), 30 (Act II ends at a sit-down),  |
| RT-05 | The two rivals not met at Act II's end | The description, sections 29, 37, 39. |
| RT-06 | Rival threat rung and counters | The description, sections 29, 30. |
| RT-07 | Hooks and knowledge as leverage | The description, sections 24 (Ledger certainty), 27, 29, 30. |
| RT-08 | Sending verbs in play | The description, section 27. |
| RT-09 | Tom's line against women, over-sixties and the priest | The description, section 10 (Tom's own line) and its conflicts note on hold-ups. |
| RT-12 | Escalation dial War trigger | The description, section 33. |
| RT-13 | Ellis's case model | The description, sections 20, 21. |
| RT-16 | Missed rent | The description, sections 24 (rent), 3 (no game over); the doing-nothing run of S23. |
| RT-17 | Money pots in practice | The description, sections 21 (what he finds he keeps), 24 (two pots; clean money spent any |
| RT-18 | Pause and clock | The description, sections 24 (the map stops Tom but pauses nothing), 27, 34. |
| GV-01 | The boot, seen | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| GV-02 | Shedding what a witness holds, slot by slot | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| GV-03 | The passenger who knows the way | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| GV-04 | Places stay open | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| GV-05 | Bugs at release | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| GV-06 | How a deed is told: restraint and cruelty | production/research/lane/gtavi/YARDSTICK.md and IDEAS-FOR-LEDGER.md |
| RT2-01 | The cold-store contract and rung 3 are circular | design pass 3, RT2-01 |
| RT2-02 | Attacking the police | design pass 3, RT2-02 |
| RT2-03 | What makes a person know Tom | design pass 3, RT2-03 |
| RT2-05 | Killing principals and needed people | design pass 3, RT2-05 |
| RT2-06 | The firm failing for good | design pass 3, RT2-06 |
| RT2-07 | What moves a rival up his ladder | design pass 3, RT2-07 |
| RT2-08 | Rivals as actors | design pass 3, RT2-08 |
| RT2-09 | Turf: posts held and lost | design pass 3, RT2-09 |
| RT2-10 | Crowd extras as witnesses | design pass 3, RT2-10 |
| RT2-11 | Finishing a downed man, kicks and bodies | design pass 3, RT2-11 |
| RT2-12 | The rare fatal fall | design pass 3, RT2-12 |
| RT2-13 | Robbed when beaten | design pass 3, RT2-13 |
| RT2-16 | Police memory and arrest hours for road deeds | design pass 3, RT2-16 |
| RT2-17 | A gun found in a stop at War | design pass 3, RT2-17 |
| RT2-18 | The licence hearing | design pass 3, RT2-18 |
| RT2-19 | The phone as a verb | design pass 3, RT2-19 |
| RT2-20 | The clock in moving talk | design pass 3, RT2-20 |
| RT2-21 | After the ending and past nine weeks | design pass 3, RT2-21 |
| RT2-22 | A foot chase caught by a constable | design pass 3, RT2-22 |
| FIT-G1 | The Hook's road plan in metres, the chase loop | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G2 | Car speeds and the stop band | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G3 | A chase at the soft edge | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G5 | The beat constable's round | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G6 | How many street happenings are written | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G7 | How many fare people are written | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-G10 | Opening hours, day and night | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-F03 | What the 70 m of a lost chase means | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-F20 | Which fares carry a wrinkle (every one after the first) | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P04 | The struck person's fall | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P17 | At least five kinds of fighter | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P18 | Two against one stays deadly | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P34 | At least 24 rooms open | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P45 | Birds and animals | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-P52 | What an ordinary drawer holds | design pass 3; FIT-CHECK-2026-11-21.md |
| FIT-L01 | 60 street lines for the 12 people seen most, 30 for the rest | design pass 3; FIT-CHECK-2026-11-21.md |
| DP5-C01 | A chase has no timer (car and foot) | design pass 4 (run 5): raised by GTA VI's bar over the description's 90 s |
