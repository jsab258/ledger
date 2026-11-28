# Blind replay of the claimed passes

28 November 2026. Helper job 7, part 3 of 3. The drafts' summary (DESIGN-DRAFTS-SUMMARY-2026-11-28.md) says 39 schemes that failed the paper chaos test now pass: economy G02, G04, G09, P14, R06; docks G03; crew and rivals K07, K08, S03, S08, T08, T09, T15, P03; property G05, G07, P12; courting P05, S07; justice K06, K11, K12, S06, T06; things H01, H02, H03, K01, K02, K09, R01, R02, R03, R04, R05, R10, R11, H07; Ledger P13. Counted: 39.

## How the 30 were drawn and traced

Drawn with Python's random module, seed 20261128, sampling 30 of the 39 in the order above: G02, G04, G09, P14, G03, K07, K08, S03, S08, T09, P03, G05, G07, P12, K06, K11, T06, K01, K02, K09, R01, R02, R03, R04, R05, R10, R11, H01, H03, H07. Left out: R06, T08, T15, P05, S07, K12, S06, H02, P13.

Each scheme was traced from its own steps in paper-chaos/PART-1 to PART-7, rule by rule, against the drafts and the blueprint, and only then compared with the drafts' re-trace tables. One disclosure: part 1's review needed each draft read in full, so I had seen those tables once before this part began; the traces below were made from the scheme steps and the rules, not from the tables. Marks and questions as in part 2 (H, H(rule), S, M, X; Q1 breaks, Q2 end to end by rules, Q3 fair and enjoyable).

## The result

21 of the 30 really pass (70%). 9 do not: K07, K08, P03, G05, P12, T06, K02, R05, H07.

| Area (claimed by) | Drawn | Pass | Fail |
|---|---|---|---|
| Economy | G02, G04, G09, P14 | 4 | 0 |
| Docks | G03 | 1 | 0 |
| Crew and rivals | K07, K08, S03, S08, T09, P03 | 3 | 3 (K07, K08, P03) |
| Property | G05, G07, P12 | 1 | 2 (G05, P12) |
| Justice | K06, K11, T06 | 2 | 1 (T06) |
| Things | K01, K02, K09, R01, R02, R03, R04, R05, R10, R11, H01, H03, H07 | 10 | 3 (K02, R05, H07) |
| All | 30 | 21 | 9 |

Read against all 39, the claim "105 of 105" is not supported: at this rate about 27 of the 39 mends hold, which would put the old test near 93 of 105, not 105. The rate on the nine not drawn is unknown; part 1 already doubts R06 (E-9: the new inspector comes a week after a one-week act), and part 2 found that P13's rule (L7) leaves a lucky bluff about a secret no way to work (BT10).

## The nine that fail, and why

| Scheme | Fails on | Why | Fix (law) |
|---|---|---|---|
| K07 Kill Ron | Q2 | R12 sends Sheila "to the police by his law dial or to a rival"; his ruling of 1 Oct: Mickey's people "never go to the police about one of their own; they handle it privately" | R12 keeps the ruled line: Mickey's people answer privately (leave, refuse, confront, tell a rival), never the police (law 3) |
| K08 The ordered killing | Q2 | R11's grave-ask rule cannot be computed as written (greed times pounds; nerve backwards; no law) | CR-2 (law 3) |
| P03 A man inside | Q2 | R15.2's weekly "contact" is no act | BF10 (law 8) |
| G05 The landlord | Q2, Q3 | The purchase costs about £27,000 for the unit and two flats against about £1,200 for the best player at week 13; no rule brings a tenant; the Hook's only agent is Agar's office | X-3, P-11, BF11 (law 4, law 3) |
| P12 The building bought early | Q2 | Starting a business has no rule; the wash a front adds has three figures; the agent is Agar's | BF19, X-2, BF11 (law 4) |
| T06 The impostor detective | Q2 | J5 sets the ring's deed "as theft of the same value"; theft has no seriousness anywhere (2.5.2's scale has damage, assault, wounding or robbery, a killing) | J-4: a theft row with value bands (law 3) |
| K02 The weighted body | Q2, Q3 | The chain comes from a boatyard that does not exist; the dredger's eight-week cycle outlasts the story; three disappearances bring a county squad, a new town-wide event | X-6, BF23, X-10 (law 2, law 1, law 3) |
| R05 Burn the book | Q2 | Sheila's "honest" rebuild of a book that hid washed money either repeats the wash or breaks the tin's flows | T-7 (law 2, law 7) |
| H07 The corner on cigarettes | Q2 | Selling packs to passers-by without a front is sent to E2.3, which governs fares | E-18: a rule for selling goods in the street, with BF03's buyer ceiling (law 4) |

## The traces

### G02 The fare war (economy)
1. Offers regulars half fare. H(rule): E2.2 (the board), G04 (a spoken promise is an obligation).
2. Passengers switch. H: E2.3.
3. The other firm cuts back or its drivers ask for work. H: E2.4, decision 21, 2.11.1.
4. Takes its rank. H: 2.15.2.
5. Flows balance at the lower fare; drivers refuse ranks that no longer pay. H: E2.6, 2.7.7.
- Q1 no. Q2 yes. Q3 yes: the war costs Frank's own book. Caution: the per-fare switching it rests on is the taxi-sim depth part 1 asks to cut (E-1); the pass survives the cut if demand moves at business level.
- Verdict: pass.

### G04 After the ending, the round pays for ever (economy)
1 to 3. The ending, the clock on, rivals frozen on their rungs. H: RT2-21, E8.1.
4. Raises the round to £40 a shop. H: EC-06, E8.1 (each rival keeps its weekly pressure; learners keep learning).
5. Shopkeepers refuse and tell after three squeezed weeks. H: 2.17.
6. Telling reaches the station; squeezed shops close after six weeks. H: E8.1, E8.2; arrests still run on a signed statement (2.6.3).
- Q1 no. Q2 yes. Q3 yes: the round shrinks unless it is fair.
- Verdict: pass. Correction to part 1: E-4 asked to drop E8.2 and let EC-04 carry it, but EC-06's own run shows the greedy round still ends richer after the story under EC-04 alone (£1,667 against £1,207 at week 13). Keep E8.2's closure and make it hold at any time, not only after the ending.

### G09 Cars for scrap (economy)
1, 2. Takes a parked car and drives off unseen. H: 1.2.10, 2.2.3.
3. Sells the whole car to the scrap yard. H: E4.2 (a fifth of its value; broken in two days; plate kept).
4. The owner reports. H: 1.2.10.
5. Plate or respray. H: 1.2.9, T8.
6. The yard man remembers. H: E4.2, 2.7.6.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### P14 The months after (economy)
1 to 4. The clock runs on; rivals freeze; ordinary weeks; something to do each day. H: RT2-21, 7.12.
5. Nothing changes after a month. H: E8.1 to E8.3 (pressure, learners, closures, the newcomer).
- Q1 no. Q2 yes. Q3 yes. Caution: RT2-21's test still stops at 14 game days; no draft lengthens it.
- Verdict: pass.

### G03 Tobacco at the gate, for ever (docks)
1. Meets the boat and buys a case. H: D2.
2. Carries and stores at the office. H: D1, T1.
3. Sells to stalls, the caff's back counter and men in the yards. H: D3.
4. Repeats at two cases a week. H: EC-07.
5. The newsagent shuts. H: EC-04.
6. Week 8 on. H: D5.3 (the gate officer watches the fixed day and the allowance falls a case each four weeks); D3.3 (buyers' rates fall a tenth a week).
- Q1 no. Q2 yes. Q3 yes as written: the scheme keeps one pattern, so the learners bite.
- Verdict: pass, thinly. A player who rotates drivers resets D5.3 and one who skips a week resets D3.3 (part 2, BP08); the mend holds only for a player who does not read the rule. BF22 makes it hold for everyone.

### K07 Kill Ron (crew)
1, 2. Asks Ron to the yard after dark; kills him in the shed. H: 3.6.1, RT2-11.
3. Ron's place passes on. H: RT2-05, decision 8.
4. Sheila or Kevin learns of it. H: 2.3.1, 2.4.1.
5. Will they tell the police? S: R12 weighs tie against loyalty and, grudge higher, sends the teller "to the police by his law dial or to a rival"; his ruling of 1 Oct (RULINGS, "The story and the first week") says Mickey's people never go to the police about one of their own and handle it privately.
- Q1 no. Q2 no (5). Q3 yes once settled.
- Verdict: fail Q2. Fix (law 3): R12 keeps the ruled line for Mickey's people: grudge higher, they act privately (leave, refuse him, confront him, tell a rival), never the police. A new finding for part 1 (CR-12).

### K08 The ordered killing (crew)
1. Gives the order. H: R10.
2. Danny decides. S: R11's line cannot be computed as written (CR-2): greed times pounds swamps every threshold, a hard man needs more to kill than a soft one, and law is not weighed.
3. The chain. H: 1.7.2.
4. Frank kills Danny. H: RT2-11, G19.
5. Danny's ties ask after him. H: J9, 2.5.5.
- Q1 no. Q2 no (2). Q3 unclear until 2 is fixed.
- Verdict: fail Q2. Fix: CR-2.

### S03 The false grass (crew)
1, 2. Tells two dock men; it spreads. H: G01, 2.4.1.
3. Lee is beaten or dropped. H: R13 (only fight roles or grudge ties answer with force; the ordinary town avoids him).
4. Lee learns who started it. H: G01.
5. Lee's grudge and the docks behind him. H: 3.5.2, G08.
- Q1 no. Q2 yes. Q3 yes. Caution: R13 names "crews" among fight roles; say criminal crews, since dockers work in gangs too.
- Verdict: pass.

### S08 The go-between round (crew)
1, 2. Hires Julie; sends her to the first shop. H: 2.11.1, decision 33.
3. The shopkeeper weighs Julie plus the man he believes is behind her. H: R14, 2.17.
4. Julie skims. H(rule): G10.
5. A shop refuses and tells after three weeks. H: 2.17.
6. Ellis asks who is behind her. H: LH-04, 2.6.5.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### T09 Talking to three at once (crew)
1. Starts talk with one. H: 3.6.1.
2. The others hear and answer. H: R16.
3. Each weighs the offer. H: WI-P06 (values for rival men's loyalty to their head still owed, CR-10).
4. One reports to the Widow. H: WI-P06, 2.10.2.
- Q1 no. Q2 yes. Q3 yes. Caution: several live speakers against the 2 s bar (CR-8).
- Verdict: pass.

### P03 A man inside the Widow's crew (crew)
1. Picks a man the Widow would take. H: 2.11.1.
2. He asks her side for work. H: R15.1.
3. He reports weekly. S: R15.2's "contact" is no act (CR-11).
4. His two loyalties pull. H: R15.2.
5. Found out. H: R7, WI-P06.
- Q1 no. Q2 no (3). Q3 yes once built.
- Verdict: fail Q2. Fix: BF10.

### G05 The landlord (property)
1. Finds who sells. S: the go-between is "the landlord's agent" (P2); the Hook's only estate agent is Agar's base (RT2-08), which the draft never weighs (BF11).
2. Agrees a price. S: rent times eight puts the unit at about £10,400 and each flat at about £8,320; EC-12's best player holds about £1,200 at week 13 (X-3). The price exists and can never be paid.
3. Lets the unit and collects rent. M: P7 rules tenants who exist; nothing brings one (P-11).
4. A tenant falls behind. H: E10, P7.2.
5. Which pot. H: P7.1.
6. A squeezed tenant tells. H: P7.3, G04, G26.
- Q1 no. Q2 no (1 to 3). Q3 no: the scheme's purchase is out of reach in every run.
- Verdict: fail Q2 and Q3. Fix: X-3, P-11, BF11.

### G07 The burnt caff (property)
1. Takes a share. H: P2, P2.4.
2. Sets the fire. H: CS-22, G18.
3. The brigade reads the seat. H(rule): G18; P6.2.
4. Insurers pay the owner; Frank's part comes through him. H: P6.3, P6.4.
5. The adjuster doubts. H: P6.2, P6.3.
6. The front is gone; takings stop. H: 2.17, EC-04.
- Q1 no. Q2 yes. Q3 yes: a gamble with a reader. Caution: nothing rebuilds the caff (part 2, BR02 and BF16).
- Verdict: pass.

### P12 The building bought early (property)
1. Finds who owns the empty unit. S: the rating list names occupiers (P1.2) and the unit has none; the agent's board leads to Agar's office (BF11).
2. Buys it. H: P2 offers a lease instead (the purchase is out of reach); the deposit (£325) is reachable around week 3 by estimate.
3. Opens a business. S: P3.1 lets a shop "open at once", but nothing says who serves, what stock is or what it takes (P-12).
4. It washes through its till. S: three figures for a front's wash (X-2).
- Q1 no. Q2 no (1, 3, 4). Q3 unclear.
- Verdict: fail Q2. Fix: BF11, BF19, X-2.

### K06 The fare who saw the envelope (justice)
1, 2. The fare off the radio sees the envelope. H: 3.4.3, GV-01.
3. Driven to the quay, he asks, protests and tries the door at a slow corner. H: J7.2.
4. Pulled out of the back seat. H: J7.1, J7.3.
5. Knocked down and drowned. H: 1.3.7, T6.3, decision 6.
6. The radio's log. H: G13, LH-04, J9.
- Q1 no. Q2 yes. Q3 yes: the dispatch book points straight at him.
- Verdict: pass.

### K11 The witness in hospital (justice)
1, 2. Learns he is there; visits in visiting hours. H: WI-P11.
3. Attacks him in the bed. H: J6 (strike allowed in a hospital visit, played as an act), J7.1 (a man in bed cannot get out).
4. Police called at once; a ward of witnesses. H: WI-P11, J6.2.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass. Correction to part 1: J-7 called J6 and WI-P11's "nothing in the hospital is walked" a contradiction. On replay it is not: an act played from a fixed scene needs no walked room. What remains is part 1's build point (J-9).

### T06 The impostor detective (justice)
1. Gets and wears the tunic. H: decision 13, CS-33.
2. Claims to be CID. H: G03, G11.
3. The pawnbroker hands over the ring. H(rule): G03, G04.
4. What deed has been done. S: J5 adds posing as police (a lesser charge, Ellis up one stage) and taking goods by a lie "as theft of the same value"; no theft row or value scale exists (2.5.2 has damage 0.3, assault 0.5, wounding or robbery 0.7, a killing 1.0; WI-P05 and 1.6.3 give lifts no seriousness), so the pawnbroker's report rule has nothing to read.
5. The pawnbroker learns the truth. H: J5.2.
6. Ellis hears. H: J5.1.
- Q1 no. Q2 no (4). Q3 yes once set.
- Verdict: fail Q2. Fix: J-4.

### K01 The witness on her walk (things)
1 to 5. Seen going; run down; knocked down; dragged and rolled in; drowns. H: 2.5.1, 1.5.2, 1.3.7, CS-16, decision 6.
6. The body comes up. H: T5.4 strikes 1.6.7's line; 2.5.5 and T5 (three to fourteen days).
7. The inquiry. H: CS-27, 2.6.10.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### K02 The weighted body (things)
1. Kills unseen. H: 1.3.6.
2. Takes a chain and weight. S: T5 sends him to "the boatyard", which is on no map (X-6, decision 19); the chandler on the quay road exists and would serve.
3. Sinks him off the fish dock. H: CS-16.
4. The body stays down. S: until the dredger works that berth, every eight weeks; the story runs about seven (T-6).
5. The missing man. H: J9.1.
6. The inquiry without a body. H: J9.2, CS-27.
7. He does it again. S: J9.3 brings a county squad at three, a new town-wide event against his ruling (X-10).
- Q1 no. Q2 no (2, 4, 7). Q3 no: inside the story a chained body never comes back.
- Verdict: fail Q2 and Q3. Fix: X-6, BF23 (divers search where the inquiry's facts point), X-10 (CID and Ellis, never the squad).

### K09 The allotment grave (things)
1 to 3. Lures, kills in the yards' lane, carries him to the allotments. H: G01, 1.3.6, CS-16.
4. Digs a grave. H: T5 (a spade from the yard shed or an allotment hut, 40 game minutes, heard at 20 m).
5. The rival notices his man gone. H: 2.5.5, 2.10.2.
6. The allotment holder or his dog. H: T5, 2.5.5.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### R01 The cab off the quay (things)
1 to 4. Drives at the edge; a body in the boot; tries to push it in; nothing to trace. H: 4.2.4, T6.1 (CS-16's line struck), CS-16.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### R02 Burn the fleet (things)
1. Sets the fire. H: CS-22, G18.
2. The cars burn. H: T3.2 (car two back within a day by the floor; the others bought on terms in a week); P6 (the firm's cover pays later, or not).
3 to 5. No car on the road; buys again; arson as a deed. H: 2.15, EC-03, CS-22.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### R03 Dark street (things)
1, 2. Breaks a lamp; sight falls. H: 1.3.5, 2.2.3.
3. The council mends it in three days, the next day after a second break. H: T4.2.
4. The constable walks there more; residents talk. H: T4.2, T4.3.
5. Breaking is a deed. H: T4.3, 2.2.1.
- Q1 no. Q2 yes. Q3 yes: no lasting dark.
- Verdict: pass.

### R04 No phones (things)
1. Smashes each kiosk. H: G19, RT2-19.
2. Witnesses walk instead. H: 2.5.1.
3. BT mends in five days, then the next day. H: T4.1, T4.2.
4. Criminal damage. H: T4.3, 2.5.5.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### R05 Burn the book (things)
1. Takes the fare book. H: 1.6.8, T7.1.
2. Burns it. H: T7.2 (what survives: Sheila's memory, the drivers' sheets, Pauline's log, the paying-in slips).
3. Act III's mornings. S: if Sheila is loyal she rebuilds "honestly, so it holds or is thin by what really happened" (T7.3). The burnt book hid washed money as fares. An honest rebuild either writes the wash in again (not honest) or shows only real fares (then the washed money has no book and 2.7.7's flows break). RT-01 cannot grade an item until that is said.
- Q1 no. Q2 no (3). Q3 unclear.
- Verdict: fail Q2. Fix: T-7 (law 2, law 7): say that Sheila rebuilds the book as it stood, wash included, from her memory and the sheets, and that the inspector grades the rebuilt weeks one step harsher for being written after the event.

### R10 The blocked door (things)
1. Frank stands in the door. H: T9.1.
2. Sheila asks twice, then comes back in an hour. H: T9.2.
3. The count is missed and reads as put off. H: T9.2, RT2-06.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### R11 The tin in the dock (things)
1. Carries the tin to the quay. H: 1.1.4.
2. Throws it in. H: T3.3, T6.2.
3. The night money is gone. H: 2.7.7, T3.3.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### H01 The radio hoard (things)
1, 2. Lifts and carries thirty radios. H: 1.6.3, WI-P05, 1.6.9.
3. The shed holds twenty-four; the rest go to a lock-up or a hiding place. H: T1, T2 (or G14's listed hiding places, if part 1's T-8 is taken).
4. Waits for the talk to cool. H: 2.4.2, 2.7.6.
5. Sells two a week. H: 2.7.6, E7 (buyers' rate falls a tenth a week for the same kind).
6. Owners never forget. H: 1.6.3.
7. Ellis searches the office once. H: 2.6.9, T2.3.
- Q1 no. Q2 yes. Q3 yes: storage now costs places and risk.
- Verdict: pass.

### H03 The painted cars (things)
1, 2. Takes three cars; Shaun resprays them. H: 1.2.10, 1.2.9.
3. Keeps them: the yard holds two more than the firm's; the third goes to a lock-up. H: T1.
4. An owner looks closely and knows his car. H: T8.
5. The police trace a car. H: G13, RT2-16.
- Q1 no. Q2 yes. Q3 yes.
- Verdict: pass.

### H07 The corner on cigarettes (things, with economy)
1. Buys the newsagent's stock. H: 2.7.5, economy draft edges (the owner sells what is on the shelf and remembers).
2. Stores the cartons. H: T1.
3. Sells packs to the parade at double. S: the economy draft's re-trace sends street selling without a front to "a talk act to passers-by whom E2.3 governs"; E2.3 governs fares switching firms. No rule says who buys goods from a man in the street, at what price or with what risk (E-18).
4. The shop restocks. H: 2.7.5, EC-04.
5. The newsagent tells. H: EC-04.
- Q1 no. Q2 no (3). Q3 unclear.
- Verdict: fail Q2. Fix (law 4): selling in the street is a sale to a named passer-by who weighs price against his purse and his other way (BF03), knows the shop's price, and holds who sold him what; stock carries its owner and any hot mark (E4.1).

## Corrections to parts 1 and 2 found here

- Part 1, E-4: reversed in part. E8.2's closure is needed; make it hold at any time rather than drop it (G04 above).
- Part 1, J-7: withdrawn as a contradiction; the build point stays as J-9 (K11 above).
- Part 1, new CR-12: R12 against his ruling of 1 Oct on Mickey's people and the police (K07 above).
- Part 1, new J-15: theft has no seriousness anywhere, which J5 relies on (T06 above; widens J-4).
- Part 2, BG04: a seam that was not one; BG04 passes and part 2 now reads 43 of 70 (61%). The corrected file accompanies this one.

## Re-check of 15 findings

Fifteen of the thirty verdicts were drawn by a fixed seed (Python random, seed 3011) and checked again at their sources as a strict reviewer would.

| Scheme | Checked again against | Result |
|---|---|---|
| G02 | E2.2 to E2.6; 2.15.2; canon OPEN 3 on taxi-sim parts | Kept pass, with the E-1 caution |
| G09 | E4.2; T8 | Kept pass |
| G03 | D5.3; D3.3; the scheme's own words ("never more") | Kept pass as written; the thinness note stands |
| K07 | RULINGS, 1 Oct ("never go to the police about one of their own"); R12 | Kept fail |
| S03 | R13.1's wording | Kept pass; the "crews" caution added on this check |
| S08 | R14; 2.17 | Kept pass |
| T09 | R16; WI-P06; 2.14's open list | Kept pass (the missing values are data, not a rule) |
| G07 | P6.2 to P6.4; P2.4 | Kept pass; the rebuild caution added on this check |
| T06 | J5; 2.5.2; WI-P05; 1.6.3; a search of the blueprint for any seriousness of theft (none) | Kept fail |
| K09 | T5; 4.3.3 (the allotments on Chapel Lane) | Kept pass |
| R01 | T6.1; 4.2.4 | Kept pass |
| R02 | T3.2; P6.3 | Kept pass (and the same reading corrected BG04 in part 2) |
| R03 | T4.1 to T4.3 | Kept pass |
| R10 | T9.2; RT2-06 | Kept pass |
| H03 | T1 (yard: the firm's cars and two more; a lock-up holds one car); T8 | Kept pass |

Fifteen kept; two cautions added (S03, G07); no verdict changed.
