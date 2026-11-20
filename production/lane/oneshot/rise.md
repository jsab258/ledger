# One-shot builder "rise": stage C, the rise (crew, rivals, rise, firm, dial, hold-ups)

Status at 09:45 Swiss, 20 Nov. Stopped early on the budget rule: the main row of 09:31 read 72% against the one-shot's ceiling of about 72.0% (22 + 0.83 an hour since Thu 15:29, plus 35). The piece in hand was finished, committed and pushed; nothing after it was started.

Where things are: tools/lane/prototype/project/src/game/ (crew.js, rivals.js, rise.js, firm.js, dial.js, holdup.js, rise_util.js, their tune, kinds and cast files), six rule pieces in game/pieces/ with 165 cases in test/cases/ (node test/pieces.mjs: all pass), in-game tests test/game/rise.mjs and rise_common.mjs.

Honest limit: the game builds with every system in, but NO in-game test of these systems has run to its end. The shared machine was killing every browser for lack of memory (nine builders at once; "Memory cgroup out of memory" in the kernel log, also on the old ledger_rules test, which passed here before the load rose). So every part below is "built shallow": its rules pass their cases under Node, its in-game code is written and builds, and it has not been played. First thing for whoever continues: run `python tools/lane/prototype/oneshot_dev.py test game/rise` on a quiet machine and fix what it shows, then write test/game/crew.mjs, rivals.mjs, firm.mjs, dial.mjs and holdup.mjs the same way (every state has a test call, listed at the end).

## Parts

- 1.6.15 Hold-ups (new; addendum A41 written, in the checklist and the tree, check.py 0 faults): built shallow. Piece holdup_rules, 30 cases pass (ER-HOLDUP-01 to 05). In game: weapon out, then H in front of a man or a keeper; refusals said with their reason; the mark always holds it; the take from the purse or till into the tin; the street on edge, a cooler name, fares down, the report after 30 game minutes unless he is reached, DS Ellis asked for next morning (emits police:reported and ellis:due for the law builder). Thin: ER-HOLDUP-06's every-outcome script not written; the mark's walk is a plain send to the phone box.
- 2.13 The escalation dial: built shallow. Piece dial_rules, 29 cases pass (ER-FIGHT-08, 09, three seeded weeks at War). In game: moves only on what somebody saw or heard, falls a step after 14 quiet days, never to Fists; said in the street and the Ledger, never a number.
- 1.3.10 Firearms: built shallow. A revolver found once in Mickey's desk (rung 2, asks twice) or bought through Lee Drewery; 0 pressed twice draws, 0 fires; a shot heard to 177 m by day, kept for good; can kill only at War. Thin: no aiming, no feel numbers, rivals' carriers are a list only.
- 2.12.2 Rung table: built shallow. Piece rise_rungs, 20 cases pass. Rungs land from what he holds, one at a time, never back.
- 2.12.3 Access and soft keys: built shallow. Six doors opened by standing and dress, an introduction, or the Fixer's appointment (G.hooks.access(door)). Thin: no other builder's door asks it yet.
- 2.12.5 Property that reacts: built shallow. The office and the flat are states with a line when each lands; the back door opens at rung 2. Thin: nothing is drawn.
- 7.7 Rising in position, felt: built shallow. The name is said to his face within a game day of each rung (ER-RISE-02), crowd greetings change at rungs 3 and 4, ER-RISE-03's list is in the tune table.
- 2.11.1 Recruiting: built shallow. Six recruits (Julie, Megginson, Lee, Norman, Karen, Shaun), by a need or a hook, in talk. Megginson and Karen are new people in the cast file (canon names from DESIGN 12, looks and cards invented).
- 2.11.2 Nerve, loyalty and breaking: built shallow. Piece crew_rules, 32 cases pass; the sign always comes before the break (ER-CREW-03).
- 2.11.3 Crew fates: built shallow. Poached, frightened (talks to the police), left unpaid; killed and arrested are states with no scene yet.
- 2.11.4 Crew pay and the cut: built shallow. A tenner agreed in a line before a night job, due at six; paid short lowers loyalty and he asks first; flows recorded.
- 1.7.1 Orders in the field: built shallow. Face the man, digits 1 to 8 (9 marks the person an order is about); answered at once, a man who cannot says why.
- 1.7.2 Sending (the eight verbs): built shallow. In talk with a man once a person is marked, Act II on; what cannot be undone asks twice; settles after six game hours; the chain is kept; the man and the target both hold it.
- 1.7.3 The board: built shallow (in firm.js). T at the board in the office: the lines in words, one move, Pauline runs it if untouched.
- 1.7.4 Men at his side: built shallow. Follows at about 2 m, snaps back if left behind 10 s; odds through G.hooks.crewOdds. Thin: he does not fight; the fight builder has no call for it yet.
- 2.15.1 Fleet and drivers: built shallow. Piece firm_rules, 27 cases pass. A car bought off Dennis Iveson, a driver from the recruits or a stranger at the counter (Mal), wages on Friday, an unpaid driver leaves.
- 2.15.2 Ranks and accounts: built shallow. Ferry and station ranks won by days there; the cold store, the Harbour Board, a solicitor, each through its person; account fares go in the book daily.
- 2.17 Fronts and rounds: built shallow. Launderette, Rinaldi's, the empty unit, by money, favour or pressure, each with a man; rounds on the quay and the parade; Saturday's money through the man, short if he is. G.x.firm.washExtraPence and G.hooks.firmWashExtra() for the wash.
- 2.10.1 Rival ladders: built shallow. Piece rival_ladder, 27 cases pass (ER-RIV-01 to 03). Daily, from Act II (sooner if the run ended); each rung said by their man or eye, or shown on the street after a day.
- 2.10.3 Pressures and answers: built shallow. Pay, defy or counter, each with its cost carried by people; unanswered for three days counts as a no.
- 2.10.4 The Fixer: built shallow. Keith Garbutt at Rinaldi's of an afternoon from Act II: a true read (made from the rival's own state), a meeting, one truce.
- 3.5.5 Sit-downs: built shallow. Rung 5, with the head on the street or in the back of his cab; accept, defy or counter; emits sitdown for the story builder.

## Known faults

- Nothing in game has been run to the end of a test (see the honest limit above). Expect small faults.
- test/harness.mjs, as the manager committed it, did not parse (a comment swallowed the rest of its line); fixed here in one line. Every builder will have made the same fix; take any one.
- New people stand "off" until sent for; their schedules use existing spots only.
- Nobody of the rise is drawn differently and no door is drawn open or shut.

## Needs from others

- fight (foot builder): count G.hooks.sideMen() as men on Tom's side; emit fight:end; treat 'revolver' as a weapon that is never swung.
- law: listen for police:reported { E, by, crime: 'robbery', hours: 12 } and ellis:due; read G.hooks.streetOnEdge(zone) and the street:edge event; G.hooks.alibi(x, z) names a driver who saw him.
- cars and fares: multiply fares by G.hooks.holdupFaresTimes(), G.hooks.rivalFaresTimes() and G.hooks.dial().nightFaresTimes; a car in G.x.firm.cars with off: true is off the road.
- pieces (money): add G.hooks.firmWashExtra() to what the book can hide; earn and pay are called with a third word, the reason.
- spine: Act II's beats can read G.x.rise.rung, G.x.rivals.<id>.rung and .settled, G.x.dial.state, and the events rise:rung, rival:move, sitdown, crew:broke; set G.x.acts.act.
- life and shops: G.x.shops.outfit (0 to 2) is read as his dress; G.x.holdup.banned[keeperId] is a keeper who will not serve him.

## Test calls (LEDGER.game)

rise.set(rung), rise.check(), rise.holdings(), rise.access(door), rise.introduce(id); crew.recruit(id, road), crew.order(id, verb, target), crew.send(id, verb, target), crew.settleSent(), crew.look(id), crew.payCut(id, pence), crew.setMan(id, fields); rivals.advance(rival), rivals.answer(rival, how), rivals.sitDown(rival, how), rivals.fixer(what, rival), rivals.know(rival, fact); dial.set(state), dial.tell(type, witnesses), dial.giveGun(), dial.draw(), dial.fire(), dial.quietDays(n); firm.buy('car' | 'front:id' | 'round:id' | 'account:id', opts), firm.place(car, rank), firm.board(), firm.dayEnd(), firm.weekEnd(), firm.wagesDay(); holdup.stage(targetId, opts), holdup.chain(i), holdup.reached(id).
