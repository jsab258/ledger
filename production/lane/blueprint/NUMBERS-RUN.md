# NUMBERS-RUN: the design's numbers through a model

Blueprint preparation item (b), 23 Nov 2026, blueprint preparation session (Opus 5.5). The model is numbers_run.py beside this file (standard Python, `python numbers_run.py`); every figure below is its output of 23 Nov after the fresh reviewer's corrections. It is a small model of the design's written rules, not the game: tools/lane/one-sim/ holds the town (who knows what), not money or the ladder, so the money and ladder rules were coded from the design text. Death, cars and guns are not modelled; where this file speaks of them it was checked against the text only.

Sources: DEFINITIONS-2026-11-21.md (G7, G8, RT-16, RT-17, RT2-01, RT2-07, RT-06, RT-12, RT-13, RT2-14, 2.7.3, GD-07, L-01, G6, GD-02), ONE-SHOT-PROMPT.md (sections 1, 13, 16, 24 to 34, 37, 40), CLOUD-FIGURES-2026-11-21.md (fence 0.33, London fares 1990), FIT-CHECK-2026-11-21.md (F19, F20, F24), RULINGS.md on wip (clock 60 s a game hour, about 7 weeks; guns rare and late; a car hurts and never kills; Tom cannot die; length 15 to 20 hours), BLUEPRINT-07-shape.md (rung 2 on Sunday's answer; Act II about 5 game weeks; fail-safe four days before its end).

Calendar: his clock, 49 game days. Act I is week 1, Act II weeks 2 to 6 (days 8 to 42), Act III week 7. A "most nights" player plays 42 of the 49 nights.

## 1. Amounts the design does not give

Run as three bands, each marked ASSUMED in the script. The one-shot cannot be tuned until they have figures (the G8 price check is due Thu 26 Nov; the rest have no owner yet):

| Missing amount | Bands run (low, mid, high) | Why these |
|---|---|---|
| Pence a mile on a fare ("80p plus distance") | a fare worth 1.30, 3.00, 6.00 | 1.30 is FIT F24's London 1990 figure; the prototype paid 2.30 to 10.28 (CHECK-1) |
| Tom's cut of a landing run | 10, 25, 50 | "comes back", no amount |
| A collection round's day | 20, 40, 60 | only figure is the old pub-era build's 60 |
| A hold-up's take | 40, 120, 250 | "what the till holds that hour" |
| Retail of a lifted thing (fence pays 0.33) | 40, 120, 300 | none given |
| A front's share | 300, 600, 900 | none given; old build's pawnshop 900 |
| A front's extra wash a week | 20, 50, 100 | "a set amount a week" |
| The Widow's dock-gate tax, a rival's payment to hold a rung, repair costs, Fixer prices | not run | none given; they are sinks, so leaving them out flatters the player |

Also unsettled in the design copies: fence 0.4 (ONE-SHOT-PROMPT s16) against 0.33 (CLOUD-FIGURES B3), the model uses 0.33; fares offered 40 to 80 a playthrough (G7) against 55 to 110 (FIT F20), the model uses G7.

Modelling choices that shape the results (stated so they are not mistaken for the design): the wash limit is treated as a hard cap each week (2.7.3 lets Tom go over it after Sheila's warning; going over was not modelled); a rising player saves for the next thing on his list rather than buying past it, in this order: basics, decent jacket, third car, stitches, good overcoat, fourth and fifth car, a front's share, a brief, a bought officer, a revolver; night money in the tin may pay for a car or a front's share (RT-17); a car counts from the week after it is bought.

## 2. Money

Three players: "fares only" (drives fares, no night work, never wins a good rank, so his drivers earn the Act I rate all game), "steady" (takes 60% of the debts, two night runs a week, a round from week 3, one lift a week, pays two men's night cuts a week), "hard" (all debts, three runs, a round from week 2, a hold-up every other week from week 3, two lifts, four men's cuts). The firm starts with 2 cars; each car earns the book 85 to 95 a week in Act I and 110 to 140 on a good rank from rung 2, and its driver costs 90 (G8). Rent 18 every Friday.

Week one, fares alone (ER-MONEY-03: a week of fares pays the first rent):

| Fare worth | Fares needed for 18 | Fares the design offers in a week (G7) |
|---|---|---|
| 1.30 | 14 | about 6 |
| 3.00 | 6 | about 9 |
| 6.00 | 3 | about 11 |

Cars and what is still out of reach (week a car first runs; wants left at the end of week 7 with their cost in pounds):

| Player, band | Third car | Fourth car | Fifth car | Wants left at week 7 |
|---|---|---|---|---|
| fares only, low | never | never | never | 8 (186); book at minus 144 |
| fares only, mid | never | never | never | 2 (110) |
| fares only, high | never | never | never | none from week 3 |
| steady, low | week 7 | never | never | 6 (2,050) |
| steady, mid | week 5 | never | never | 5 (2,050) |
| steady, high | week 5 | week 7 | never | 4 (1,450) |
| hard, low | week 5 | never | never | 6 (2,050) |
| hard, mid | week 4 | week 7 | never | 4 (1,150) |
| hard, high | week 4 | week 5 | week 7 | none at week 7 |

The wash (2.7.3: the book hides 10 a day plus 80% of the fares really driven): dirty money as a share of the week's limit.

| Player, band | Weeks 1 to 7, % of the limit used |
|---|---|
| steady, low | 54, 9, 49, 49, 49, 49, 36 |
| steady, mid | 74, 23, 93, 93, 69, 69, 69 |
| steady, high | 107, 51, 141, 141, 106, 106, 84 |
| hard, low | 91, 53, 61, 61, 45, 45, 45 |
| hard, mid | 130, 105, 126, 93, 93, 93, 74 |
| hard, high | 198, 178, 218, 161, 127, 127, 106 |

Findings, each with its fix inside his rulings:

M1. Week one does not pay at a London fare. At 1.30 a fare, 14 fares pay the rent; the design offers about 6. ER-MONEY-03 holds only if a fare is worth about 3 or more. Fix (tuning): set the per-mile rate so a typical Hook fare (1 to 2 miles to the station or Copper Row) pays 2.50 to 3.50, to be confirmed by Thursday's price check, and put at least 7 of the playthrough's fares in week one (S07's day shift already has 6).

M2. The clean-only player sinks at low fares and stalls at mid. At the Act I firm rate (two drivers earning about what they cost) the book loses 21 a week at 1.30 fares, so rent goes unpaid and RT-16's ladder lets the flat by week 4, and wages go unpaid so the drivers leave (RT2-06). That breaks OSP s13's "a player who only drives fares can still pay the rent". At 3.00 the book gains only 8 a week; at 6.00 he has bought everything his path offers by week 3 and money stops mattering for him. Fix: M1's fare rate (which alone lifts him to plus 8 to plus 61 a week), and give the clean path its own wants so money keeps mattering: the third car on terms (M3), the flat's arrears and a better room, the decent jacket the licence hearing asks for (RT2-18). GD-07's test (a named thing out of reach at every act's end) should be run on this player as well as the greedy and lazy bots.

M3. The rise stalls on car prices. Rung 2 comes with Sheila's answer and brings a third car (OSP s32; BLUEPRINT-07), but no rule says who pays for it; rung 3 needs five cars and the cold-store contract needs four (OSP s32; RT2-01). At 600 to 1,200 a car, with night money allowed to pay, the third car runs in week 4 at best and week 7 at worst, and only the hard player at high amounts reaches five cars, in Act III's week. A car earns the book only 20 to 50 a week over its driver's wage, so it pays for itself in 12 to 60 weeks: cars are a pure sink. In a 5-week Act II, rung 3 is out of reach for almost everyone. Fix (a rule to record, inside his rulings): the firm buys cars on hire purchase, as a 1990 minicab firm would: a deposit of about a tenth and about 15 to 25 a week from the book; a missed payment is a letter, then the car goes back. Cars stay a sink, but a steady player can reach rung 3 by Act II's third or fourth week. Re-run once G8's prices stand.

M4. The wash barely bites for an ordinary player. A steady player uses 9% to 93% of the limit at low and mid amounts, so the daily count is rarely a choice; it binds for the hard player (over 100% in 3 of 7 weeks at mid amounts and all 7 at high) and for the steady player only at high amounts. Fix (a rule change to record, since 2.7.3 and OSP s26 count all fares at one rate): count the drivers' fares at 40% and Tom's own at 80%. The steady player at mid amounts then uses 109% to 143% of the limit in six of the seven weeks and has to choose between a smaller night and a riskier book (the script's variant table). The 80% is already PENDING (GD-07).

M5. Nothing in the money rules can end the game: a missed rent becomes words and a lost flat, never a lost office (RT-16). Good as designed; M2 shows it is reached too easily at low fares.

## 3. The rivals' ladder and cooling

The ladder as written (RT2-07): five rungs, never skipped; noticed on the first thing a rival's people see; a visit after two more sightings or Tom at rung 2; pressure on a refused visit, Tom at rung 3 or a deed; a threat on a defied or countered pressure or a second deed; the sit-down on a defied threat, Tom at rung 4 or a man killed; a deed lifts a rival one rung at once; paying holds two game weeks unless a deed; Act II ends at the first sit-down; the fail-safe lifts the highest rival one rung a day from day 38. First notice is staggered (ASSUMED): the Widow day 8, Cammack day 10, Agar day 13. Three players: "payer" (pays at every rung, no deeds, stays at rung 2), "steady" (pays each rival once at the visit then refuses; defies Cammack's pressure on day 18, counters the Widow's on day 27; deeds against Cammack day 16 and the Widow day 30; rung 3 day 22, rung 4 day 35), "hard" (deeds against Cammack on days 9 and 10 and the Widow on days 11 and 12; defies every pressure and threat).

| Player | As designed | Fix A: one rung a rival every 5 game days | Fix B: fix A, and a paid rival holds 7 days and takes at most 2 payments |
|---|---|---|---|
| payer | ends day 40 by the fail-safe; rung changes in Act II weeks 1 and 5 only | day 40; weeks 1, 2, 5 | day 38; weeks 1 to 5 |
| steady | ends day 30; weeks 1 to 4 | day 39; weeks 1 to 5 | day 35; weeks 1 to 4 |
| hard | ends day 12; week 1 only | day 28; weeks 1 to 3 | day 28; weeks 1 to 3 |

Findings:

R1. Escalation runs away for an aggressive player. The Widow is noticed on day 8, visited 9, pressed 10, threatened 11, sits down 12: Act II ends in its first week, about 2 hours into a 9 to 14 hour act, before the real book, the contract, the gun or the case can come. Nothing in RT2-07 spaces the rungs. Fix (changes a DECIDED definition, so it is a decision to record, his to overturn): a rival climbs at most one rung every 5 game days, except by the fail-safe. The hard player's Act II then ends on day 28, three fifths of the way through, with a rung change in each of its first three weeks. A wider spacing (6 days) pushes him to day 32 but leaves the payer a week with no change, so 5 is the run's pick.

R2. Escalation stalls for a payer. A two-week hold and no trigger that forces the next rung mean a player who pays every visit sees no rung change in Act II weeks 2 to 4, then three rungs in three days by the fail-safe. That breaks Act II's rule that every game week brings a rival rung (OSP s37). Fix B (a decision to record): a paid rival holds 7 days, not 14, and takes at most two payments, then moves to the next rung anyway. With fix A the payer then sees a rung change in every week of Act II and the sit-down on day 38. The price of a payment is still missing (section 1).

R3. The fail-safe works but is steep when it is the only thing moving; with fix B it is not needed for any of the three players before day 38. Keep it as written.

R4. Cooling was set for a longer Act II. The escalation dial and Ellis each fall one step after about two quiet game weeks (RT-12, RT-13), so in a 5-week Act II either can fall at most twice, and the dial never returns to fists once a gun is shown. Talk cools in 1 to 7 game days, memory never. One shooting in week 2 colours the rest of the act. That suits guns rare and late, but RT2-14's first ways to a gun (Mickey's revolver on Sheila's trust, or the deckhand through Rita at rung 3 or Darren's tip) can come in Act II's first week for a player Sheila trusts early. No rate change is proposed here; record that the cooling numbers were set for 7 weeks and should be re-read when the panel plays a 5-week Act II.

R5. Checked against the text, not the model: no rung lets anyone kill Tom (beaten or shot he comes round, OSP s10, s33), a car hurts and never kills (P04), and every gun comes through one of RT2-14's four ways. The ladder fixes above change none of these.

## 4. Repeats for a player who plays most nights

Arithmetic (the script's last table), 42 nights played, foot about 25% of play (OSP s40):

| Length | Hours on foot | Street remarks heard (40 to 80 an hour, FIT F19) | Happenings at one per 15 real minutes (G6) |
|---|---|---|---|
| 15 h | 3.8 | 150 to 300 | 60 |
| 17.5 h | 4.4 | 175 to 350 | 70 |
| 20 h | 5.0 | 200 to 400 | 80 |

P1. Happenings run out above 15 hours. G6 asks for at least 60 written, one every 15 real minutes, none twice in the game unless people changed. A 17.5 hour player needs 70 and a 20 hour player 80. Fix: write 80 (about 10 a kind over 8 kinds), the cheaper certain fix (INVENTORY.md).

P2. Own lines repeat for the 30-line people. The 12 most-seen (L-01, Pauline among them) have 60 own lines at most once a day, so none repeats in 49 days. Everyone else has 30 at once a day; a regular met most nights (the Quay Street shopkeepers, a driver outside the 12) repeats from night 31, about 12 repeats each by the end. Fix: for the 30-line people, an own line at most every second day they are met (30 lines then last 60 days). It costs nothing to make.

P3. Shared street lines need sizing by how often a situation comes up, above the design's floor of 6 per situation per speaker kind (OSP s5). If half of 175 to 350 remarks are everyday ones, a flat 6 lines for each of about 6 speaker kinds (36) means each is heard 2 to 5 times and repeats within an hour once remarks pass 36 an hour (GD-02 allows none twice in a real hour). Fix: keep the floor of 6 per speaker kind for every situation and add about 120 everyday lines; INVENTORY.md counts the result (about 500).

P4. Fares. 40 written fare people with two rides each make 80 rides (G7, F20); with 40 to 80 offered nobody repeats, but at FIT F20's 55 to 110 up to 30 would. Fix: cap the offered fares at 80; Kevin and Terry take the rest off screen, as OSP s13 already allows.

P5. Scenes and side stories. Act II has 8 beats, each once; Act III 5 mornings; about 25 side stories are found, not repeated. The risk is the opposite: a 5-week Act II with 8 beats is one beat every 4 game days or so. With R1 and R2 fixed, a rung change, a beat or a firm change lands every week.

P6. Jobs. "No set piece twice in thirty minutes" and "three keys to every lock" are stated; jobs per hour are not (GD-08 PENDING), so job repeats cannot be run yet. With 9 job kinds and about 1 to 2 jobs a game evening, a kind recurs every 3 to 5 evenings; the variety has to come from places and people (each Act II place at least 2 jobs, RT-03).

## 5. What to run again, and when

1. After Thursday's G8 prices: the money run with real prices, hire purchase and the over-the-limit wash (M1 to M4).
2. When the Widow's tax and the price of a held rung are set: the ladder with fix B priced (R2).
3. When the line table exists (FIT F19, due Thu 26 Nov): the shared lines by situation (P3).
4. In the one-shot: the same three players as bots in the built game; this run's numbers become their expected rows.

Nothing here needs Jafar. M1 and the line sizes are tuning values. M3, M4, R1 and R2 change DECIDED definitions: each is a decision for the blueprint keeper to record in DECISIONS.md and fold in, and stays his to overturn.
