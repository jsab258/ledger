# The town's economy, 1990: design pass

Design pass of 24 Nov 2026 (due Thu 26 Nov 12:00), lane-2026-11, Opus 5.5. Prices and wages in PRICES-WAGES-1990.md beside this file; the money run in economy_run.py (run: `python economy_run.py --seeds 300`); the owner's open choices in section 9. Third person throughout.

## 0. What this rests on, and where it disagrees

Rests on (read 24 Nov): canon.md and RULINGS.md on wip; BLUEPRINT-02 sections 2.7 (money), 2.8 (debts), 2.9 (the arrangement), 2.10 (rivals), 2.11.4 (crew pay), 2.12.2 (the rung table), 2.15 (the firm), 2.17 (fronts and rounds), RT-07 (hooks), RT-16, RT-17, GD-07, FIT-G8, FIT-F24; BLUEPRINT-04 4.2.2, 4.2.3 (cold stores, dock gate, Harbour Board clerk, bonded store), 4.3 (trades, hours, the pawn, the station); NUMBERS-RUN.md and numbers_run.py (findings M1 to M5); PRIOR-RESEARCH-INDEX.md (no 1990 price study existed before this one; cab-office-1990 and CLOUD-FIGURES B1 and B3 are built on); the C# town simulation's Economy.cs (prosperity, a price level, suppliers who grow dear, squeeze raising prices) and its July balance log (game-design/balance-findings-economy.md: no death spiral, rackets paid for by the street); research/shop-hours-1990.

Binding facts: canon's D24, rewritten 19 Nov, says LEDGER is "NOT an economy simulation", and BLUEPRINT 2.7.5 says "no price tables, stock or supply chains". So this design is a money model under the crime, not a market: every pound is a flow from a person, a purse, a till, a wage or a bribe (2.7.7), shops have weekly takings and a margin, nobody trades stock, and prices move only on a shop's own board for a cause the town can name. The player never sees a table. Alcohol and gambling do not exist (no betting money, no drink trade, no fruit machines); tobacco does.

Disagreements and which wins:
- Clock. RULINGS of 21 Nov set 60 s a game hour; the decision of 24 Nov (in this job's brief) sets 2 real seconds a game minute, a 48-minute day. The newer decision wins here. The economy is weekly, so the money curve does not change, but a 7-week story at 48 minutes a day is about 39 real hours if no time is skipped, against a ruled length of 15 to 20 hours; with nights slept through it is still over 20. That is the keeper's and the owner's to square (KEEPER-LOG line), not this file's.
- Ellis. BLUEPRINT-04 4.3.7 says she cannot be bought; the decision of 24 Nov says she can, at a high price. The decision wins (section 5.7).
- The driver's pay. The design pays a flat £90 a week; the real trade paid by takings. Owner's choice 1; the run uses the split, which gives the book about the same in Act I.
- Rung 3. The run first let five cars and a front or a round lift Tom to rung 3. The rung table (2.12.2) asks for a front and a round. The table wins, and its consequence is stated in section 7: a firm that never runs a round stays at rung 2. Still looser than the table in the run: the recruit (rung 2), the night desk (rung 3) and the three posts (rung 4) are not modelled, and the contract's income is paid from rung 3 although RT2-01 notes the contract and rung 3 are circular.

## 1. Who has money, and when

- Working people: dockers and cold-store hands about £190 to £230 a week, paid Friday; shop staff about £120, paid Saturday; a lorry driver £245; women in manual work about £143. About one in eight men out of work, on benefit. Their week goes on rent (£23 council, £35 a private terrace, £25 rooms), food, tobacco, the launderette, the caff and the chip shop, bus and the occasional cab. A household has a few pounds left on Friday night and nearly nothing by Thursday. That rhythm is the town's: shops are busiest Friday evening and Saturday, quiet by Thursday (early closing, research/shop-hours-1990), and a debtor pays on Friday or not at all.
- Shopkeepers: nine trades in reach (fishmonger, grocer, newsagent and tobacconist, launderette, caff, chip shop, ironmonger, tea room, the pawn). Each takes £380 to £1,900 a week, pays stock, rent and staff, draws about a manual wage for himself and keeps a margin of about £45 to £175. The margin is the shop's purse: what a debtor, a protection man or a robber can get, and what pays for anything that goes wrong.
- The firm: two tired cars (rung 1), a car's week on a dead rank about £130 in takings, half to the driver and half to the book; fuel, cover and repairs about £46 a car come out of the book. Tom's own fares come whole to the book, less fuel.
- The rivals and the police: the Widow taxes cars at the dock gate (£5 a car a week) once Tom has five cars, until answered; two constables and, at a high price, DS Ellis can be bought.
- Tom: £23.50 in his pocket, the book at nothing, the tin empty, rent £18 every Friday, Mickey's debt book (£156, five debts, the design's).

## 2. Where money comes from and goes (Tom)

In (clean, to the book): the firm's half of the takings; Tom's fares; the count's wash of night money (2.7.3, with M4's 40% of drivers' fares and 80% of Tom's, plus £60 a week a front).
In (night, to the tin or the pocket): the debt book; the outfit's landing runs (£20 Tom's cut); a protection round; smuggled tobacco; loans; a hook spent for money; a hold-up; goods to a fence or the pawn.
Out (book): rent £18; office running £12; fuel, cover, repairs about £46 a car; terms on cars £22 a week each; anything bought in a shop.
Out (cash only, RT-17): men's night cuts (£10 to £40); men posted at rung 4 (£40 a week each); bribes; Ellis's retainer. Night outgoings are paid only from cash in hand; nothing turns the book into tin. Short pay is recorded and lowers that man's loyalty (2.11.4), never borrowed.

## 3. What the player sees

- Prices spoken by sellers and written where a 1990 shop wrote them: the caff's board (tea 30p, breakfast £1.80, dinner £2.50), cards in the newsagent's window, the chip shop's menu board, the pawn's tickets. A board changes only for a cause (section 5.1, 5.3) and the change is visible: a price chalked over.
- The fare book at the counter: every fare, by Tom and by the drivers, written by Sheila, readable; Friday's line is the rent.
- The tin: a cash tin in Mickey's inner office; Tom sees roughly what is in it ("about £40"), never a figure to the penny.
- Tom's own words, on asking (2.7.7): "£31 in your pocket. The tin has about £40 in it. Rent, £18, Friday. Darren still owes £12."
- The street's mood in words, built on Economy.cs's words: "comfortable", "getting by", "tight", "hurting"; prices "ordinary", "up", "steep". People say these, the paper prints them.

## 4. The firm

How it works: a car's takings are split half to the driver and half to the book (choice 1). A dead firm's rank gives £130 a week a car, a good rank from rung 2 £210, the cold-store contract (rung 3) £40 more. The book pays fuel (about 13 gallons a week at £2.00), cover and repairs. A driver whose half falls under £60 for two weeks, or who is frightened, leaves (2.15.1, RT2-06). More cars come on terms: about £90 down and £22 a week for a year; a missed week is a letter, two and the car goes back. The fare: 80p, then £1.10 a mile, a quarter more at night and on Sunday; a Hook fare is £1.90 to £3.55, typically £3.

| Week | Book from one car on a dead rank | On a good rank | With the contract |
|---|---|---|---|
| Takings, the firm's half | £65 | £105 | £125 |
| Less fuel, cover, repairs | £46 | £46 | £46 |
| Less terms (a car bought on terms) | £22 | £22 | £22 |
| Left to the book (owned car / on terms) | £19 / minus £3 | £59 / £37 | £79 / £57 |

Rung 2 brings the third car (OSP s32) on terms, the £90 deposit from the book. Under the flat wage (choice 1 (a)) a car leaves the book minus £6 on a dead rank and £74 on a good one, so Act I is harsher and Act II richer; the split is the steadier curve (section 7).

So a car is a slow earner and a sink until paid off; Mickey's two cars are the firm's profit in Act I. This keeps NUMBERS-RUN M3's finding (cars are a sink) and its fix (terms).

## 5. The crime levers

For each: what it pays, what it costs, and what it does to prices, mood and loyalty, gossip and the police. Pounds an hour are of the player's own hands, from economy_run.py's effort estimates (ASSUMED).

### 5.1 Protection (a round)
- Pays: £5 to £15 a shop a week, set by what the shop can bear (section 5 of the prices file); the man who walks it keeps a quarter. Eight shops at £10 is about £60 a week to the tin. About £180 an hour of Tom's hands (setting each shop up, then trouble on the round).
- Costs: a man of nerve on the round (2.17); trouble on it comes back to Tom through him; each shop signed is a person who may tell, by temper (0.3 of a case point each in the run).
- Prices: a shop pays out of up to 60% of its margin without passing it on. Asked more, half the excess goes on its board (prices up, chalked over) and half off its purse; customers thin. Four losing weeks and it shuts, and the town says why.
- Mood and loyalty: the shopkeeper is afraid, not loyal; fear is loyalty only until it breaks. A shop squeezed past what it can bear is a likely teller (a case point a week in the run), and after three such weeks he stops paying and tells (2 points, off the round for good).
- Gossip: a round is told as a told version within a game day (2.8.2); a shop shutting is told for weeks and is a lasting mark (2.19).
- Police: slow; a shopkeeper rarely goes to the police in 1990 (reporting of threats was low, research/threats-1990), but squeezing past bearing is how Ellis gets a witness.
- Run: at £10 a shop no shop shuts for protection (the racketeer's newsagent shuts from smuggled tobacco, section 5.2) and the dearest board moves 1%. At £40 a shop the round pays £660 an hour while it lasts, the dearest board rises 9%, shops refuse and tell, Tom is arrested three times, and he ends the story poorer than the fair round (£224 against £785 at week 7). After the story ends the greedy round does end richer (week 13: £1,667 against £1,207); see F4.

### 5.2 Smuggled tobacco
- Pays: a case of 200 packs bought off a boat at the dock gate or out of the bonded store's leak for about £100 (50p a pack), sold to stalls, the caff's back counter and men in the yards at 80p (£160): £60 a case, about £240 an hour of Tom's hands (meet, carry, place).
- Costs: the Widow's ground (the dock gate is hers); customs. Two cases a week pass unseen; more needs men at the gate (rung 4, four cases). Pushed past that, customs take a load (the whole week's cases lost) and Ellis hears.
- Prices: none on a board; the legal newsagent loses the packs it would have sold. Two cases a week, then four once Tom has men at the gate, shut the racketeer's newsagent in week 7. The newsagent says so first, at two losing weeks.
- Mood and loyalty: buyers like cheap cigarettes; the newsagent does not, and knows why.
- Gossip: low until a seizure, which is news.
- Police: customs first, then Ellis.

### 5.3 Loans (Tom lends)
- Pays: "a pound in five a week", until the principal comes back over four weeks; a quarter of what is still out goes bad each week after the fourth. The Hook's borrowers can carry about £200 at once (a dozen men at £10 to £30). About £40 to £80 an hour.
- Costs: money out of the tin first; bad debts; collection is fronting up (2.8.2) with its talk.
- Prices: none. Mood: the borrower's purse drained each Friday; he pays in money, in kind or in what he hears (as Darren does).
- Gossip and police: a squeeze or a let-off is told within a game day; a beaten debtor is a deed with witnesses.
- Mickey's debt book is the first five loans: £156, Darren in news, the other four in money or goods (the design).

### 5.4 Blackmail (a hook spent for money)
- Pays: £50 to £300, what the person's purse holds (run: £120). A hook is spent once (RT-07); the person now knows Tom knows, and remembers.
- Costs: a hook, which can only come from a perceived source (Darren, his own eyes, Mickey's real book); so it is rationed by the world, about one a fortnight at most.
- Mood and loyalty: hatred; that person never comes over to Tom, and is a teller waiting for a reason.
- Police: 0.6 of a case point; a likely witness the day Ellis asks.

### 5.5 Hold-ups and lifts
- Hold-ups pay what the till holds that hour (about £90, a small shop's day); rare and late (ruling 20 Nov), loud, witnessed, 2 case points. A held-up shop is afraid for weeks; its takings fall a tenth at first and recover as the fear fades.
- A lift pays a third of retail at a fence (about £40), a fifth less for each further piece the same week (2.7.6); Rita's back room opens at rung 2. The buy-back (decision of 24 Nov): what Tom sold, the shop or pawnbroker that bought it sells back within 7 game days at what it paid plus a quarter; a fence holds nothing. About £305 to £340 an hour, the best repeatable lever, limited by what is worth taking in a written town, the falling price and talk (a lift cools in a day or two, 2.4.2). Ten lifts a week bring in about £100 a week more than two, at the cost of three arrests, and are then no longer the best lever.

### 5.6 The outfit's runs
- £20 Tom's cut a run to the ferry landing, nights one, three, five, seven in Act I (2.9.1); about £200 an hour. A stop and search keeps the envelope.

### 5.7 Bribes, DS Ellis included
- A constable: £50 to look away once, £200 to lose a statement once (design).
- DS Ellis (decision of 24 Nov, she can be bought at a high price): about £800, two and a half weeks of her pay, buys her; she then takes £100 a week (choice 2). While bought her case cools twice as fast and she loses her best line once. A missed week and she is no longer bought, her case jumps (3 points in the run), and she remembers; she is never bought twice. Paid only from cash. In the run the racketeer, keeping £900 back in the tin for her, buys her in week 6, Act II's last week. At £1,000 he could not until week 8, after the story.

### 5.8 The firm's costs of a rising position
- Rung 4 posts men at the dock gate, the cold store and the landing: £40 a week each, from cash (an honest firm would pay yard men from the book).
- The Widow's tax: £5 a car a week from five cars until answered.

## 6. Rules the one-shot can check (blueprint format)

### EC-01 The fare
- How it works: 80p, then £1.10 a mile; a quarter more 22:00 to 06:00 and on Sunday. A Hook fare of 1 to 2.5 miles is £1.90 to £3.55. At least 7 fares are offered in week one.
- Standard: a week-one fares-only player pays Friday's £18 from fares alone (ER-MONEY-03).
- Test: B: the fares-only bot, week one, rent paid from fares; the fare for a 1.5-mile trip at 14:00 is £2.45, at 23:00 £3.06 (the 80p included in the quarter).
- Source: PRICES-WAGES-1990 section 2 (cab research S9, CLOUD-FIGURES B1); NUMBERS-RUN M1.

### EC-02 A car's takings and its split
- How it works: a car's week £130 on a dead rank, £210 on a good rank from rung 2, £40 more with the contract; half to the driver, half to the book; the book pays fuel, cover and repairs (about £46). A driver whose half is under £60 two weeks running leaves.
- Standard: the flows ledger balances (ER-MONEY-01); a car's book line equals half its takings less its costs.
- Test: B: a seeded week of two cars on each rank, audited.
- Source: PRICES-WAGES-1990 sections 2 and 4; cab research S12 to S14 (Hamiltax's 70/30 and the settle). Choice 1.

### EC-03 Cars on terms
- How it works: a car from the lot or a seller, £600 to £1,200, or on terms: about £90 down and £22 a week for a year from the book. A missed week is a letter said by Sheila; two and the car goes back. Mickey's car (car two) is never taken.
- Standard: a steady player reaches five cars inside Act II.
- Test: B: the mix bot has five cars inside Act II (run: week 6; racketeer week 4; honest week 7).
- Source: NUMBERS-RUN M3; PRICES-WAGES-1990 section 2.

### EC-04 Shops have a week
- How it works: each shop has weekly takings, costs, its owner's draw and a margin (prices file section 5); the margin is its purse. Takings fall when its board rises and while it is afraid. Four losing weeks in a row and it shuts; it says so at two.
- Standard: no shop shuts without a cause the town can name in the four weeks before (protection past bearing, a hold-up, smuggled tobacco on its trade, a rival). Takings move with Friday and Saturday wages and with early closing.
- Test: B: 300 noisy runs a style (takings within 15% either way), no causeless closure (run: 0 of 1,200); a slack month at the docks (every shop's takings down 15% for four weeks) shuts no shop.
- Source: this pass; Economy.cs (a poor street makes a supplier dearer, never a guaranteed loss).

### EC-05 Prices move only on a board, for a cause
- How it works: a shop on a round pays out of up to 60% of its margin; past that, half the excess goes on its board (prices chalked up), capped at a quarter over; the town says "prices are up" at 10% and "steep" at 25% (Economy.cs's words).
- Standard: with no squeeze, no robbery and no rival on it, a shop's board never moves.
- Test: B: honest, lazy and mix runs leave every board at its first price (run: 1.00); the racketeer at £10 moves the dearest board 1%, at £40 9%.
- Source: this pass; Economy.cs PriceWord.

### EC-06 Protection
- How it works: £5 to £15 a shop a week by what it can bear; the man on the round keeps a quarter; asking past what it can bear raises its board, thins its trade, may send the owner to the police by temper, and after three weeks he refuses and tells.
- Standard: the round never pays more than twice the middle repeatable lever an hour at the fair rate; squeezing the street never ends the story richer than the fair round.
- Test: B: the dominance check at £10 (run: £177 to £182 an hour against a middle of £182); the greed check at £40 (run: week 7 £224 against £785).
- Source: this pass.

### EC-07 Smuggled tobacco
- How it works: £100 a case off the boat, £160 sold on; two cases a week pass, four with men at the gate (rung 4); more and customs take the week's load, and Ellis hears. The legal newsagent loses the packs.
- Standard: tobacco never pays more than twice the middle lever an hour; pushing past the gate always ends in a seizure within three weeks.
- Test: B: the racketeer within the gate (£240 an hour) and the variant pushed past it (run: seizures and three arrests).
- Source: PRICES-WAGES-1990 sections 1 and 6 (Hansard 14 Feb 1990: tax 73% of a pack); BLUEPRINT-04 4.2.3.

### EC-08 Loans
- How it works: a pound in five a week; principal back over four weeks; a quarter of what is out goes bad each week after the fourth; collected by fronting up.
- Standard: lending never makes money from nothing (every pound lent leaves the tin first); a bad loan is a person with a grudge.
- Test: B: lend £100, follow it six weeks; the ledger balances.
- Source: this pass (rate INFERRED).

### EC-09 Blackmail is a hook spent
- How it works: a hook spent for money takes what the purse holds (£50 to £300) and is spent once (RT-07).
- Standard: no hook pays twice; blackmail is rationed by hooks, never by a timer.
- Test: S: spend a hook for money, try again: refused in words.
- Source: RT-07.

### EC-10 The buy-back
- How it works: within 7 game days a shop or the pawn sells back what it bought from Tom at what it paid plus a quarter; a fence holds nothing.
- Standard: as written.
- Test: S: sell a radio to the pawn for £12, buy it back on day 6 for £15, on day 8 it is gone.
- Source: decision of 24 Nov.

### EC-11 Ellis's price
- How it works: about £800 from cash buys her; £100 a week keeps her; a missed week ends it for good and her case jumps.
- Standard: she can be afforded only from Act II's later weeks by a player with a full night who saves for her; never twice.
- Test: B: the racketeer buys her in week 6 (run); a missed retainer week unbuys her (to add as a seeded case; the run's racketeer never misses).
- Source: decision of 24 Nov; PRICES-WAGES-1990 section 4 (sergeant's scale). Choice 2.

### EC-12 The money curve
- How it works: the numbers below.
- Standard: nobody is rich by week 3 (worth under what it costs to start everything his path still wants, cars at their deposit); nobody broke with no way back (book and pocket below nothing three Fridays running); the lazy player pays every Friday's rent (MP-04); a rising player's Act II last week brings in 3 to 10 times week one, counting income before outgoings and leaving out the inherited debt book and rationed one-offs (MP-02); no single take over the greater of £150 or 1.5 weeks' income (MP-02); a named want out of reach at week 7 (GD-07); squeezing the street never ends the story richer than the fair round. Every week the flows balance (opening plus in less out equals closing) and the tin never goes below nothing; the run stops if not.
- Test: B: python economy_run.py --seeds 300; breakages 0. In noisy runs MP-02 is judged on the mean curve (mean week 6 against mean week 1); single noisy weeks outside 3 to 10 are reported, not failed.
- Source: MONEY-AND-PROGRESSION MP-02; GD-07; this run.

## 7. The run (economy_run.py, 24 Nov; output in economy_run-output-2026-11-24.txt)

Four styles over 13 game weeks (7 story, 6 after): honest (fares, gentle debts, cars on terms, a front bought clean); racketeer (every lever, Ellis bought); mix (the firm plus two runs, a four-shop round, a case of tobacco, a little lending); lazy (GD-07's lazy bot: four or five fares a week, nothing else). Worth is book, tin and pocket; wants left are what his path still wants, with what it costs to start each.

| Week | Honest worth (wants left) | Racketeer | Mix | Lazy |
|---|---|---|---|---|
| 1 | 92 (11) | 199 (16) | 149 (11) | 45 (15) |
| 3 | 146 (7) | 459 (9) | 141 (6) | 133 (8) |
| 5 | 398 (6) | 693 (4) | 191 (5) | 262 (6) |
| 7 | 188 (4) | 785 (2) | 584 (2) | 109 (5) |
| 13 | 147 (1) | 1,207 (0) | 1,222 (0) | 742 (2) |

Over 300 noisy runs each (takings within 15% either way), worth at week 7 (10th to 90th): honest 126 to 292, racketeer 652 to 1,647, mix 468 to 852, lazy 115 to 586. Rich by week 3, broke with no way back, shops shut with no cause: none in 1,200 runs. The money ratio (MP-02) on the mean curve: honest 3.7, mix 7.0, racketeer 10.0 (the top of the band). Rung 3: racketeer week 5, mix week 7; rung 4: racketeer week 9; honest and lazy never past rung 2 (no round). Ellis: racketeer week 6. Pounds an hour of Tom's hands: lift 305 to 339, tobacco 240, landing 200, round 177 to 182, loans 41 to 82, fares 55; the best is under twice the middle. The flows balance every week in every run.

What broke and was tuned (each a change in the run):
1. Night outgoings were paid from an empty tin. Fixed: cash-only payments pay what the tin holds; short pay is recorded (RT-17, 2.11.4); an arrest's brief is paid from what cash there is and only a positive week is halved; a weekly flows audit now stops the run on any pound from nowhere.
2. The racketeer could never afford Ellis: the count washed every pound out of the tin. Fixed: a player keeps back what he means to spend in cash (the racketeer keeps £900); her price cut from £1,000 to £800, so she is affordable in Act II's last week and not only after the story.
3. Smuggled tobacco at 95p a pack was the best lever; cut to 80p (£160 a case). The run's seizure only fired for a player who ignores the gate; that variant now runs (seizures and three arrests).
4. The round's pounds an hour counted setting up only; trouble on the round (2 minutes a shop a week) added; the man's cut raised to a quarter. Greed (£25 to £40 a shop) won outright; now a shop squeezed past bearing adds a case point a week and refuses and tells after three, so greed ends the story poorer.
5. Lifts were a flat third every time; now a fifth less for each further piece the same week, and none before Rita opens at rung 2.
6. The money ratio failed when week one counted the inherited debt book and when single noisy weeks were compared; it now counts income before outgoings, leaves out the debt book and rationed one-offs, and is judged on the mean curve. The racketeer still sat at 10.2, so the Hook's borrowers were capped at £200 out at once and the good rank set at £210.
7. Rung 2 was free; it now brings the third car on terms (OSP s32). Rung 3 needs a front and a round; rung 4 two of each and a brief.
8. The "rich by week 3" check compared worth with a year of car terms and could not fail; it now uses what each want costs to start. A slack month at the docks was added to test causeless closures.

Findings that stay open:
- F1. A fare worth £1.30 (a London cab's rate per mile read as a fare) breaks the honest and the mix player: broke with no way back, and every driver's half under £60 every week. The fare must be about £3 (EC-01).
- F2. An honest firm stops at rung 2 for good, because rung 3 needs a round; the lazy firm too. That fits a crime game, but the clean player has little to rise into after week 7. Choice 3.
- F3. After the story (weeks 8 to 13) the racketeer and the mix have bought everything by weeks 10 to 12 and money stops mattering. Only matters if play goes on after the ending; then the after-game needs its own wants.
- F4. After the story the greedy round does end richer (week 13: £1,667 against £1,207), because the fewer shops left keep paying and nothing new hunts Tom. Inside the story it loses. If play goes on after the ending, Ellis's case should keep climbing with the street's tellers.
- F5. The clock (section 0): a 48-minute day over 7 weeks is longer than the ruled 15 to 20 hours.
- F6. The mix player reaches rung 3 only in the story's last week (week 7), though the design wants rung 3 inside Act II for a steady player. A front on terms, or the contract counting for the round (choice 3 (b)), would bring it to about week 5. Not tuned here; recorded for the keeper.
- F7. Not modelled, so not tested: a driver leaving after two weeks under £60 (the run only records such weeks: none on the recommended figures; every week at a £1.30 fare); the Widow's tax being answered (answered by a man posted at £40 a week, a cost the run leaves out); the Friday and Saturday wage rhythm inside a week (the run is weekly).

## 8. What changes in the blueprint (for the keeper)

- 2.7.1, 2.7.4, FIT-G8, FIT-F24: the fare (EC-01), the driver's pay (EC-02, if choice 1 goes the recommended way), diesel at 36p a litre in place of 45p; G8 and F24 move from pending to sourced or inferred as labelled in the prices file.
- 2.7.5 and 2.7.8: EC-04 and EC-05 (shops have a week; boards move only for a cause), which keep "no price tables, stock or supply chains".
- 2.6.8, 4.3.7: Ellis can be bought (EC-11).
- 2.15.1: cars on terms (EC-03).
- 2.17: protection (EC-06), with the newsagent and tobacco (EC-07).
- New rows: EC-07 to EC-10.
- NUMBERS-RUN M1 and M3 are settled by EC-01 and EC-03; M4 is used as written.

## 9. Choices for the owner (at most three)

1. How are the drivers paid? (a) a flat wage of £90 a week, as now; (b) RECOMMENDED: half of what each car takes, the firm paying fuel and cover, as real 1990 cab firms did; (c) each driver owns his car and pays the firm about £50 a week. The run: under (a) the book loses about £6 a car a week on a dead rank and gains £74 on a good one, so Act I is harsher and Act II richer, and the honest and mix curves break the money study's band; under (b) it is £19 and £59, a steadier curve, and a dead rank is felt by the drivers.
2. How is DS Ellis bought? (a) RECOMMENDED: about £800 once, then £100 a week, and a missed week ends it for good; (b) about £1,200 once and she stays bought; (c) cheaper, about £400, but only once Tom holds a hook on her as well. (a) keeps a weekly cost late in the story and a risk if the money runs short; (b) is simpler and lets a rich player forget her; (c) keeps your decision that she can be bought while making it a story turn rather than a purchase.
3. Can an honest firm rise past rung 2? (a) RECOMMENDED: no, rung 3 needs a round as the rung table says; the clean firm stays a respectable cab office and the empire is crime's, which is the game's pillar; (b) yes, winning the cold-store contract counts in place of a round: this keeps an honest road to rung 3 and also brings the steady player's rung 3 into Act II (F6), but it makes the contract the clean player's whole Act II; (c) yes, a second front counts in place of a round.
