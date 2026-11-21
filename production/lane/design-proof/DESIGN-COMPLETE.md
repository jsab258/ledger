# The gate: when the design counts as complete

The design counts as complete, and the next one-shot prompt may be written from it, only when all four hold:

1. Every row of the coverage map (coverage.json) is MEASURED, DECIDED or OUT with his ruling. No row is PENDING, UNMEASURED or UNDEFINED. OUTSIDE rows (Unreal-only looks, engine, performance, and shipping business) are not judged here.
2. Every review theme of every game (Steam players and critics; KCD2, GTA V, RDR2 and the six walkthrough games; the eight-game story patterns) maps to a part with a test (themes.json).
3. Two red teams in a row, each of two fresh helpers given only the game description with ten parts silently removed, find no material gap that is not in the map.
4. In both of those rounds each helper catches at least 9 of the 10 planted gaps.

## Process guards (from the pre-mortem of 21 Nov, ways 3, 4 and 19; written by run 4, 21 Nov)

**G-A. MEASURED means a real figure.** A row counts as MEASURED for the gate only when its standard rests on one of: a reference game's measured number; a dated real-world figure or a dated published standard (law, regulator guidance, accessibility guidelines); or a pass-or-fail rule of his (his ruling, canon or his numbered decisions). Each MEASURED row says which in its field real_basis. A standard the design sessions chose is a design decision: status DECIDED, listed below for him to overturn. DECIDED rows pass condition 1 as decisions, never as measurements, and the gate's report always gives three numbers side by side: rows MEASURED, rows resting on a reference game's number or a dated real-world figure, and rows DECIDED. Applied to the map on 21 Nov by scripts/run4_guard.py (a first pass by rule and by hand; a later run may move a row with a stated reason): the 195 rows called MEASURED became 101 MEASURED (66 on his rulings or canon, 20 on reference-game numbers, 15 on dated real-world figures or published standards) and 94 DECIDED.

**G-B. What a material gap is.** Defined on 21 Nov, before red team 3, and not to be changed until the gate is met or round 4 is done. A gap a red team raises is material when it is a part missing or undefined in the design, and at least one of these holds:
1. a player would meet it in the first game week (Act I and the first week of Act II, or any hour of the 41 playthrough checks' first week);
2. it is a system edge that can end a session stuck (no way on without reloading or quitting);
3. it is a system edge that would break one of his rulings or canon (content rule, Tom cannot die, a car hurts and never kills, no game over, the map ruling, the length ruling, and the rest of RULINGS.md);
4. it would block one of the playthrough checks from being run or passed.
Anything else (taste, polish, more of something that exists, Unreal-only looks, a different design the helper would prefer) is not material: it is logged in that round's triage file as a note and goes on no list. Triage applies these four tests by name, line by line, and each material line names the test it meets.

**G-C. At most four red-team rounds.** Rounds 1 and 2 are done (19 and 22 gaps). Round 3 is on Sun 29 Nov and round 4 on Mon 30 Nov. There is no round 5: after round 4, whatever is still open goes to him once as a scope list, each item with what it would take and a recommendation (define it now, defer it after the one-shot, or cut it), and the gate is judged on his answers. If round 3 and round 4 are both clean, conditions 3 and 4 are met.

**G-D. The clock before red team 3.** His open C11 is settled before red team 3 (pre-mortem way 19). Its rows are PENDING his answer; both versions are written in DEFINITIONS-2026-11-21.md (design pass 3, the clock) so either answer drops in the same day.

## Where it stands, 21 November 2026, after run 3

| Condition | State |
|---|---|
| 1. Rows | Not met. 363 rows: 195 MEASURED, 29 PENDING, 46 UNMEASURED, 22 UNDEFINED (red team 2's gaps, new today), 14 OUT, 57 OUTSIDE. Of the 195, about 24 rest on reference-game or period figures (15 before, plus the panel bar, rent, custody, the fence, cooling, display options and replay branches today); the rest are his rulings, canon, guidelines, design decisions he may overturn, or pass-or-fail guards. |
| 2. Themes | Met as a mapping (all 242 themes on parts with a test); they close with condition 1. |
| 3. Red teams | Not met. Round 1 found 19 material gaps, round 2 found 22 (RT2-01 to RT2-22, edges of existing systems rather than missing systems). Clean rounds so far: 0. |
| 4. Catch rate | Round 1: 10 and 9 of 10. Round 2a: 10 and 8 (brief improved once); round 2b: 9 and 10 of 10. |

## What stands between the design and the gate, with dates

| What | Rows | Closed by | When |
|---|---|---|---|
| Red team 2's 22 gaps: the cold-store contract loop, attacking the police, knowing Tom, how the ending is chosen, killing needed people, the firm failing, rivals' ladder and men, turf, crowd witnesses, finishing a downed man, the fatal fall, robbed when beaten, guns reaching Tom, the successor, police memory, a gun at a War stop, the licence hearing, the phone, the clock in moving talk, after the ending, a caught foot chase | 22 UNDEFINED | design pass 3 in the cloud, in the design's own words, with a fresh reviewer | Sun 22 Nov |
| GTA VI's footage pass, first (his ruling, the full pass) | GTA VI's column on the PENDING feel rows; GD-02; 1.2.10, 2.6.10 | PC measuring, block 1 (about 24.5 PC hours) | Mon 23 to Tue 24 Nov |
| Feel numbers for KCD2, GTA V and RDR2 | 16 PENDING, 3 UNMEASURED | PC measuring, block 2 | Tue 24 to Thu 26 Nov |
| The teardown and the hour split | 7.5 PENDING; 23 UNMEASURED | PC measuring, block 3 | Wed 25 to Fri 27 Nov |
| Extra rows on the feel sheets | 6 UNMEASURED; GD-01, GD-02, GD-07, GD-08, RT-10, RT-11, RT-19, 2.7.3 PENDING | PC measuring, block 4 (about 14.5 PC hours) | Thu 26 to Sat 28 Nov |
| The listening pass | 8 UNMEASURED | PC measuring, block 5 (about 2 PC hours) | Fri 27 to Sat 28 Nov |
| Who is out on a port street by hour (no 1990 figure found on 21 Nov) | 2.1.2 UNMEASURED | ONS time in and out of home tables, scaled back; PC reads the MTUS 1987 file if they give no hours | cloud by Thu 26 Nov |
| The day's length: the references run 48 to 144 real minutes a day against LEDGER's 18 (45 s an hour) | 7.13 PENDING | his open feel decision C11 and the PC's timing of a reference evening (A5) | 23 to 28 Nov |
| Story content, Act III's shape, the jobs after week one, humour per act | 5 UNMEASURED; GD-05, RT-01, RT-02, RT-03 PENDING | the story measure | by Sat 28 Nov 12:00 |
| Red team 3: a fresh copy with design pass 3 folded in, ten new planted parts, the improved briefs | conditions 3 and 4 | cloud, two fresh Opus helpers | Sun 29 Nov |
| Red team 4, needed because the gate wants two clean rounds in a row and none has been clean yet | conditions 3 and 4 | cloud | Mon 30 Nov at the earliest |
| One point for his ruling: a field-of-view setting (AX-03) | not blocking | the advisor puts it to him | when he answers |

Done on 21 Nov (run 3): the panel bar (7.2, 7.3), the 1990 figures (2.7.4, 2.6.4, 2.7.6), the published figures (2.4.2, 8.3.1, GD-04), the privacy check (8.2.1, 10.11), the typed-talk set (RT-14), red team 2.

Earliest the gate can be met: Mon 30 Nov to Tue 1 Dec, one day later than run 2 said, because the gate needs two clean red teams in a row and round 2 was not clean: red team 3 on Sun 29 Nov and red team 4 on Mon 30 Nov must both find nothing material, after design pass 3 closes the 22 gaps on Sun 22 Nov, the PC measuring (23 to 28 Nov) and the story measure (by 28 Nov). If red team 3 finds gaps again, each further round costs about a day.

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
