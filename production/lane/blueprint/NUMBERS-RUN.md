# NUMBERS-RUN: the design's numbers through a model

Blueprint preparation item (b), 23 Nov 2026, blueprint preparation session (Opus 5.5). The model is numbers_run.py beside this file (standard Python, run with `python numbers_run.py`; every table below is its output of 23 Nov). It is a small model of the design's written rules, not the game: tools/lane/one-sim/ holds the town (who knows what), not money or the ladder, so the money and ladder rules were coded from the design text.

Sources: DEFINITIONS-2026-11-21.md (G7, G8, RT-16, RT-17, RT2-07, RT-12, 2.7.3, GD-07), ONE-SHOT-PROMPT.md (sections 1, 13, 16, 24 to 34, 40), CLOUD-FIGURES-2026-11-21.md (fence 0.33, London fares 1990), FIT-CHECK-2026-11-21.md (F19, F20, F24), RULINGS.md on wip (clock 60 s a game hour, about 7 weeks; guns rare and late; car hurts never kills; Tom cannot die; length 15 to 20 hours), BLUEPRINT-07-shape.md (Act II about 5 game weeks, fail-safe four days before its end).

Calendar used: his clock, 49 game days. Act I is week 1, Act II weeks 2 to 6 (days 8 to 42), Act III week 7. A "most nights" player plays 42 of the 49 nights.

## 1. Amounts the design does not give

These were run as three bands; each is marked ASSUMED in the script. The one-shot cannot be tuned until they have figures (the G8 price check is due Thu 26 Nov; the rest have no owner yet):

| Missing amount | Bands run (low, mid, high) | Why these |
|---|---|---|
| Pence a mile on a fare ("80p plus distance") | a fare worth 1.30, 3.00, 6.00 | 1.30 is FIT F24's London 1990 figure; the prototype paid 2.30 to 10.28 (CHECK-1) |
| Tom's cut of a landing run | 10, 25, 50 | "comes back", no amount |
| A collection round's day | 20, 40, 60 | only figure is the old pub-era build's 60 |
| A hold-up's take | 40, 120, 250 | "what the till holds that hour" |
| Retail of a lifted thing (fence pays 0.33) | 40, 120, 300 | none given |
| A front's share | 300, 600, 900 | none given; old build's pawnshop 900 |
| A front's extra wash a week | 20, 50, 100 | "a set amount a week" |
| The Widow's dock-gate tax, repair costs, Fixer prices | not run | none given; they are sinks, and leaving them out flatters the player |

Also unsettled in the design copies: fence 0.4 (ONE-SHOT-PROMPT s16) against 0.33 (CLOUD-FIGURES B3); the model uses 0.33. Fares offered: 40 to 80 a playthrough (G7) against 55 to 110 (FIT F20); the model uses G7.

## 2. Money

Three players: "fares only" (drives fares, no night work, never buys a car), "steady" (takes 60% of the debts, two night runs a week, a round from week 3, one lift a week, pays two men's night cuts a week, saves for the next thing on the list), "hard" (all debts, three runs, a round from week 2, a hold-up every other week from week 3, two lifts, four men's cuts). The wants list is DEFINITIONS G8's spending list in the order a rising player buys: basics, decent jacket, third car, stitches, good overcoat, fourth and fifth car, a front's share, a brief, a bought officer, a revolver. Cars come only when bought (the firm starts with 2, OSP s32); each car earns the book 85 to 95 a week in Act I and 110 to 140 from rung 2, and its driver costs 90 (G8). Rent 18 every Friday.

Week one, fares alone (ER-MONEY-03 says a week of fares pays the first rent):

| Fare worth | Fares needed for 18 | Fares the design offers in a week (G7) |
|---|---|---|
| 1.30 | 14 | about 6 |
| 3.00 | 6 | about 9 |
| 6.00 | 3 | about 11 |

When the third car arrives, and what is still out of reach at the end (pounds):

| Player, band | Third car | Fourth car | Fifth car | Wants left at week 7 (cost) |
|---|---|---|---|---|
| fares only, low | never | never | never | good overcoat (90) |
| fares only, mid | never | never | never | nothing from week 3 |
| fares only, high | never | never | never | nothing from week 2 |
| steady, low | week 6 | never | never | 6 items (2,050) |
| steady, mid | week 4 | week 5 | never | 5 items (2,050) |
| steady, high | week 4 | week 7 | never | 5 items (2,650) |
| hard, low | week 4 | never | never | 6 items (2,050) |
| hard, mid | week 4 | week 7 | never | 5 items (2,050) |
| hard, high | week 4 | week 7 | never | 5 items (2,650) |

The wash (DEFINITIONS 2.7.3: the book hides 10 a day plus 80% of the fares really driven): dirty money as a share of the week's limit.

| Player, band | Weeks 1 to 7, % of the limit used |
|---|---|
| steady, low | 54, 9, 49, 49, 49, 49, 36 |
| steady, mid | 74, 23, 93, 93, 69, 69, 69 |
| steady, high | 107, 51, 141, 141, 106, 106, 84 |
| hard, low | 91, 53, 61, 61, 45, 45, 45 |
| hard, mid | 130, 105, 126, 126, 93, 93, 74 |
| hard, high | 198, 178, 218, 218, 161, 161, 127 |

Findings, each with its fix inside his rulings:

M1. Week one does not pay at a London fare. At 1.30 a fare, 14 fares pay the rent; the design offers about 6. ER-MONEY-03 holds only if a fare is worth about 3 or more, or Tom is offered at least 6 a week in Act I and they average 3. Fix: set the per-mile rate so a typical Hook fare (crossing to the station or Copper Row, 1 to 2 miles) pays 2.50 to 3.50 (still inside 1990 provincial meters, to be confirmed by Thursday's price check), and put at least 7 of the playthrough's fares in week one (S07's day shift already has 6).

M2. Money stops mattering for the fares-only player in week 2 or 3. At mid and high fares he has bought everything his path offers by week 3, and the book then grows by 78 to 151 a week with nothing to spend it on. That is the players' fear named in FIT ("money that stops mattering after week one"). Fix: give the clean path its own wants: the third car on the book (see M3), the flat's arrears and a better room, the decent jacket needed for the licence hearing (RT2-18), and Pauline's and the drivers' wages rising when the firm grows. GD-07's own test (a named thing out of reach at every act's end) should be run on this player, not only the greedy and lazy bots.

M3. The rise stalls on car prices. Rung 2 needs a third car and rung 3 needs five (OSP s32), and the cold-store contract needs four (RT2-01). At 600 to 1,200 a car no player in any band reaches five cars in 7 weeks; the third car arrives in week 4 at best (week 6 for a steady player at low amounts). A car earns the book only 20 to 50 a week over its driver's wage, so it pays for itself in 12 to 60 weeks: cars are a pure sink. With Act II only 5 weeks long (his clock), rung 3 never happens. Fix: hire purchase, which a 1990 minicab firm would use: a car on the never-never for a deposit of about a tenth and a weekly payment of about 15 to 25 from the book; a missed payment is a letter, then the car goes back. Cars stay a sink that needs steady money, but rung 2 lands in Act II's first week and rung 3 by week 3 or 4 for a steady player. The money run should be repeated with this rule once G8's prices are fixed.

M4. The wash barely bites for an honest-ish player. A steady player uses 9% to 93% of the limit at low and mid amounts, so the daily count with Sheila is rarely a choice. It binds only for the hard player, and at high amounts he piles up 2,000 to 3,000 in the tin that cannot be explained, which is the intended pressure. Fix: count the drivers' fares at 40% instead of 80% (Tom's own fares stay at 80%): the steady player at mid amounts then uses 109% to 143% of the limit in five of the seven weeks and has to choose between a smaller night and a riskier book (script's variant table). The 80% figure is already PENDING (GD-07), so this is a tuning value, not a rule change.

M5. The fares-only player is safe from ruin: his book is never below minus 21 (a missed first Friday at the lowest fare, which RT-16's ladder turns into words, not a loss), and the office is never lost. Good as designed.

## 3. The rivals' ladder and cooling

The ladder as written (RT2-07): five rungs, never skipped, each lifted by its triggers; a deed against a rival lifts him one rung at once; paying holds a rival two game weeks unless Tom does a deed against him; Act II ends at the first sit-down; the fail-safe climbs the highest rival one rung a day from four days before Act II's end (day 38). Three players: "payer" (pays every visit, no deeds, rises no further than rung 2), "steady" (pays each rival once, rung 3 on day 22 and rung 4 on day 35, a deed against Cammack on day 16 and the Widow on day 30), "hard" (deeds against Cammack on days 9 to 11 and the Widow on day 12, defies every pressure).

| Player | Act II ends (as designed) | Weeks of Act II with a rung change |
|---|---|---|
| payer | day 40 (week 5), by the fail-safe: pressure 38, threat 39, sit-down 40 | 1 and 5 only |
| steady | day 30 (week 4) | 1, 2, 3, 4 |
| hard | day 12 (week 1) | 1 only |

Findings:

R1. Escalation runs away for an aggressive player. Noticed day 8, visit 9, pressure 10, threat 11, sit-down 12: Act II ends in its first week, about 2 hours into a 9 to 14 hour act, and the 8 Act II beats, the gun, the contract and the case never come. Nothing in the triggers spaces the rungs. Fix (inside the rulings; nothing on screen changes): a rival climbs at most one rung every 4 game days, and the sit-down that ends Act II waits until Act II's fourth week (day 29); before then a rival at threat goes on doing threat-rung harms (window, tyres, a hearing date, RT-06). With both, the hard player's Act II ends on day 29 with rung changes in weeks 1, 2 and 4 (script's third variant). The steady player is unchanged in shape (ends day 35).

R2. Escalation stalls for a payer. Paying holds a rival two weeks and no trigger forces the next rung, so a player who pays every visit sees no rung change from day 9 to day 38, then three rungs in three days. That breaks Act II's own rule ("every game week of Act II brings at least one rival rung") in weeks 2, 3 and 4, and the ending arrives as a lurch. Fix: a paid rival holds for one game week, not two, and asks more each time (the second payment double the first; a third refused by the rival, who moves to pressure). Then a payer climbs one rival a rung about every 10 days, which meets the weekly rule with three rivals in turn. Price of each payment: still missing (Widow's tax and the others are not given).

R3. The fail-safe works but is late and steep. It turns 4 days into three rungs. With R2's fix it rarely fires; keep it as written.

R4. Cooling fits the shorter Act II only just. The escalation dial and Ellis both fall one step after about two quiet game weeks (RT-12, RT-13), so in a 5-week Act II either can fall at most twice, and the dial never returns to fists once a gun is shown. Talk cools in 1 to 7 game days and memory never. Under the old 7-week Act II these cooling rates gave room to recover; under his clock they mean one serious shooting in week 2 colours the whole act. That suits "guns rare and late", but the first gun beat should not be offered before Act II's third week (it is tied to rung 3, which M3 currently puts out of reach; with hire purchase it lands in week 3 or 4). No change to rates proposed; record that the cooling numbers were set for a longer Act II and should be re-read when the panel plays it.

R5. Safety rules the model checked hold by construction: no rung lets anyone kill Tom (Tom cannot die; beaten or shot he comes round, OSP s10, s33), a car hurts and never kills (P04), and guns enter only through people from rung 3 (RT2-14). Nothing in the ladder can bypass them.

## 4. Repeats for a player who plays most nights

Arithmetic (the script's last table), 42 nights played, foot about 25% of play (OSP s40):

| Length | Hours on foot | Street remarks heard (40 to 80 an hour, FIT F19) | Happenings at one per 15 real minutes (G6) |
|---|---|---|---|
| 15 h | 3.8 | 150 to 300 | 60 |
| 17.5 h | 4.4 | 175 to 350 | 70 |
| 20 h | 5.0 | 200 to 400 | 80 |

Findings:

P1. Happenings run out above 15 hours. G6 asks for at least 60 written, one every 15 real minutes, none twice in the game unless people changed. A 17.5 hour player needs 70 and a 20 hour player 80. Fix: write 80 (about 10 a kind across 8 kinds), or space them one per 18 minutes after Act I. Writing 80 is the cheaper certain fix (see INVENTORY.md).

P2. Own lines repeat for the 30-line people. The 12 most-seen have 60 own lines at most once a day (L-01), so none repeats in 49 days. Everyone else has 30 at once a day; a regular met most nights (Quay Street's shopkeepers, Pauline's radio, the drivers if not in the 12) repeats from night 31, about 12 repeats each by the end. Fix: for the 30-line people, an own line at most every second day they are met (each lasts 60 days), or 45 lines for the next 12 most-seen. The first costs nothing to make.

P3. Shared street lines need sizing by how often a situation comes up, not a flat 6. The rules are: none heard twice in a real hour (GD-02), at most one remark every 45 s, 6 lines per situation per speaker kind (OSP s5). Everyday remarks (the weather, the street, the time of day) are most of what is heard: if half of 175 to 350 remarks are everyday ones, 6 lines times about 6 speaker kinds (36) means each is heard 2 to 5 times in the game and repeats within an hour once the rate passes 36 an hour. Fix: about 120 everyday lines (enough for the no-repeat-in-an-hour rule at 80 an hour with room), about 40 for weather, about 24 for each common deed situation, 6 for rare ones. Total about 400 (counted in INVENTORY.md).

P4. Fares. 40 written fare people with two rides each make 80 rides (G7, F20); with 40 to 80 offered nobody repeats, but at FIT F20's 55 to 110 up to 30 rides would repeat. Fix: cap the offered fares at 80 for the playthrough (Kevin and Terry take the rest off screen, as OSP s13 already allows).

P5. Scenes and side stories. Act II has 8 beats, each once; Act III 5 mornings; about 25 side stories of about 12 minutes are found, not repeated. No repeat risk; the risk is the opposite, that a 5-week Act II with 8 beats has weeks with no beat: one beat about every 4 game days. With R1 and R2 fixed, a rung change, a beat or a firm change lands every week.

P6. Jobs. "No set piece twice in thirty minutes" and "every job a small graph with three keys" are stated; jobs per hour are not (GD-08 PENDING), so job repeats cannot be run yet. With 9 job kinds and Act II at about 1 to 2 jobs a game evening, a kind recurs about every 3 to 5 evenings; the variety has to come from places and people (each Act II place at least 2 jobs, RT-03).

## 5. What to run again, and when

1. After Thursday's G8 prices: the money run with real prices and hire purchase (M1, M3).
2. When the Widow's tax, the payment for a held rung and the front's prices are set: the ladder with R2's priced holds.
3. When the line table exists (FIT F19, due Thu 26 Nov): the shared-line run by situation (P3).
4. In the one-shot: the same three players as bots in the built game; the script's numbers become the expected rows.

Nothing here needs Jafar: every fix is a tuning value or a rule inside his rulings, recorded for the blueprint keeper to fold in.
