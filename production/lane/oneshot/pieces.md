# Builder "pieces": status

20 November 2026, 09:50 Swiss time. Stopped early by the budget rule: the main row of 09:31 read 72% against the one-shot's ceiling of about 72% (22 + 0.83 for each hour since Thursday 15:29, plus 35).

## Parts

- 2.7.1 Clean money and the fare book: built. Tests: pieces (money, flows), game/econ. Earning and paying go through the money piece.
- 2.7.2 Night money and the tin: built. Same tests. Night money is spent first unless a thing must be paid clean.
- 2.7.3 The wash: built. Sheila says what the book will hide before anything goes through; "all of it" asks twice; the week's row is kept for the inspection. Cases pass; the in-game test (game/econ) did not finish here (see Known faults).
- 2.7.4 Rent and running costs: built shallow. Running costs on Thursday, the drivers' takings each working day, wages on Friday, the count on Saturday; what cannot be paid is held and raised by Sheila. Rent itself is still the story's own (scenes.js). ER-MONEY-03 passes as cases; in the game not yet seen to pass.
- 2.7.7 Flows ledger: built. Every earn, pay and wash is a flow with a reason; the game checks the pots against the book each game minute and counts anything unexplained. Cases pass.
- 2.8.2 Partial payment (the piece only; the part is the jobs builder's): passes its cases; in the game only through G.hooks.debtCollect.
- 3.6.1 Live talk: built, unchanged in how it reaches the page's Claude. One change: the sum of money offered is the one the game's own rule read in his words.
- 3.6.2 Claim check: built. A live line that names a titled person who is not in the town, lays a deed on Tom the speaker holds no memory of, or uses a word the content rule or the year forbids is not shown; the written line plays. Cases pass (13); in-game test not finished.
- 3.6.5 Decision lines: passes its test (game/talkrules: 170 lines that are not a plain yes, 1,530 tries, none taken). In the game a typed yes is taken only if it is a plain yes.
- 3.6.6 Suggested lines: built (as round 6; not changed).
- 3.6.7 AI notice and line report: built shallow. F9 reports the last line said, in a talk or on the pause screen; reports are kept in the save. No button on screen yet, and no way by pad.
- 3.6.8 How the player speaks, and 6.7 Talk screen: built (as round 6). A whole decision by Tab, arrows and Enter is written as a test (game/talkx) and not yet seen to pass.
- 9.6 The tuning table: built. `node tools/numbers.mjs game` lists every number in src/game outside game/tune, game/kinds and game/cast; `left` holds this builder's files to it. Run at 09:40 on this branch: none outside the record.
- Step 4(f): five pieces, 250 cases, all passing (money 42, flows 21, debts 29, fights 58, talk 100). production/lane/ONE-SHOT-PORTING.md.

## Tests

- node test/pieces.mjs: PASS, 5 pieces, 250 cases.
- test/game/talkrules.mjs (no browser): PASS.
- numbers: PASS. talk, talk5, fixes1: PASS (run before the last two small edits to talk.js).
- test/game/econ.mjs: its first six checks passed; then the browser was killed for lack of memory each time (nine builders testing at once: the machine's log shows the kills). Not seen to pass.
- test/game/talkx.mjs: one full run before fixes showed two test faults (now mended: the stand-in offered 500 pounds, and a talk closes when a person's lines run out); after that the browser was killed each time. Not seen to pass.
- same_week: killed the same way twice. It will differ from round 5's record anyway (money now moves on Thursday, Friday and Saturday).

## Known faults

- The two in-game tests above are unproven. Run them alone on a quiet machine first: `python tools/lane/prototype/oneshot_dev.py test game/econ game/talkx`.
- The fights piece is not called by the game's fight.
- The week bot answers Sheila's new choice with its first answer ("Only what the book will hide"), so a seeded week washes less than round 5's did.
- Kevin and Terry are counted as the two drivers until the rise's fleet says otherwise (G.x.firm.drivers, a list or a count).

## Needs from others

- Manager: tools/lane/prototype/project/test/harness.mjs was broken at the first commit (the comment on the port line cut off the window's width and height, so no browser test could start). Mended on this branch; take this branch's line.
- Spine (scenes.js): collect() and forgive() should call G.hooks.debtCollect(P, 'asked' or 'squeezed') and G.hooks.debtForgive(P), so a debtor pays what his purse holds (2.8.2). Today the story takes the whole debt.
- Spine (ledger_screen.js): the smoke run's line "Pauline Kitching knows that you tried to put money in Pauline Kitching's hand" names her twice; the cause (a typed sum read as a bribe) is fixed in talk, the wording is the Ledger's.
- Spine (the pause screen and the Ledger's money page): say "F9 reports the last line said"; G.hooks.moneyWords() gives what he has and owes in words; G.hooks.bookReads() gives the book as the inspector will find it (hold, thin or off), from G.x.econ.weeks.
- Foot (fight.js): call pieces/fights.js for nerve, answer, weapon and fall, or leave it and keep the note in ONE-SHOT-PORTING.md.
- Everyone: pass a reason as the third argument of earn and pay ("a fare", "the Monday bag"); without one the flow is written as "earned" or "paid". Never change G.money directly: the check counts it as money from nowhere.
- Rise: G.x.firm.washExtraPence is added to what the book hides; G.x.firm.drivers (a list or a count) sets wages and takings. The event 'wages:short' { pence, week } is sent when the drivers are paid short.
