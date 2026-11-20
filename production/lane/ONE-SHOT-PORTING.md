# The one-shot: rules ready to port

20 November 2026. Money, debts, jobs, fights and talk are not in the game's town code. Each is written here as a separate rule piece with its own test cases, so Unreal can port the proven rule and pass the same cases. This list was written by the pieces builder at 09:45 from its own branch and from what the other builders had pushed by then; the manager completes it after the merge.

## What a piece is

- A file under tools/lane/prototype/project/src/game/pieces/. It exports PIECE = { name, fns }. Every function is plain data in and plain data out: no clock, no screen, no game state, and chance only from a seed handed in.
- Its cases are tools/lane/prototype/project/test/cases/<name>.json: each case names its rule, the function, the inputs and the expected result.
- `node test/pieces.mjs` (in the project folder) runs every piece against its cases with no browser, in about two seconds. A port passes when the same inputs give the same results.
- The numbers a piece uses come from the one tuning table (rules.js and game/tune/). Each function takes the table as its last argument, so a port hands in its own copy.
- For the five pieces below, the cases are written by tools/pieces_cases.mjs. A case there states what the rule must give, by hand, and the writer refuses to write the file if the piece disagrees. One case (the same seed gives the same fight) records the piece's own answer.

## The five pieces of step 4(f)

| Piece | What rule it holds | Functions | Cases | Rules it proves | Does the game call it? |
|---|---|---|---|---|---|
| money | The pocket and the tin; paying (night money first, unless it must be clean); the wash (the book hides ten pounds, 80% of fares driven since the last wash, a quarter of the firm's own fares, and what fronts add); Sheila's warning; the week's running costs, wages and rent; the alibi fare; how the inspector reads the book; money in words | sumInWords, pay, earn, washCap, washWarning, wash, weekCosts, firmWeek, scriptedWeek, alibiFare, bookReads, moneyInWords | 42 | ER-MONEY-01, 02, 03 (both scripted weeks), 04 | Yes: money.js pays, earns and washes through it; the econ system runs the week by it |
| flows | No money from nowhere: every movement has two sides and a reason; the pots must equal the sum of flows | sound, open, add, balance, check, totals | 21 | ER-MONEY-01; part 2.7.7 | Yes: every earn, pay and wash is written into it, and the game checks it each game minute |
| debts | Mickey's five debts; a debtor pays what the purse holds and the rest stays on the book; paying in goods or in news; striking out; what each outcome tells the street | book, total, paysWhenAsked, collect, strike, tells, lesson, lines | 29 | parts 2.8.1, 2.8.2 | Partly: offered as G.hooks.debtCollect and debtForgive. The story's own collect in scenes.js still takes the whole debt at once (see Needs, below) |
| fights | The eight rungs and what each shows the street; nerve with face, corners and backing; the odds; the five endings; condition without bars; weapon tiers and breakage; the fall rule; a whole fight from a seed | rung, rungs, pressure, nerve, answer, odds, handsOff, weapon, condition, fall, deathBreaksRuling, ending, maySwing, bands, simulate, simulateMany, holds | 58 | ER-FIGHT-01 (17 of the melee sheet's bands), 02, 04, 05 (10,000 fights, no death breaks his ruling), 07 (patient 99.9%, masher 21%) | No: the game's fight (fight.js) still runs its own code. The piece states the same rules from the same numbers (rules.js, ladder) |
| talk | What typed words mean (a sum spoken is not money offered); only a plain yes is taken; what cannot be undone asks twice; Leave always offered; the claim check; the memory of lines; slow replies; reports | intent, plainYes, plainNo, decisionStart, decisionStep, decisionSound, claimCheck, lineAllowed, lineSaid, nextLine, replyRule, sceneTooLong, report, padCanAct | 100 | ER-TALK-01, 02, 03 (also 170 lines in test/game/talkrules.mjs), 04, 06, 07; ER-SPEAK-01 | Partly: talk.js reads intent, the plain yes and the claim check from it, and reports go through it. The memory of lines still runs in talk_lines.js (round 5's own code, the same rule). The slow-reply times are not applied: see Known differences |

## Pieces the other builders had pushed by 09:45 (the manager confirms after the merge)

| Piece | Builder | What rule it holds | Cases |
|---|---|---|---|
| job_template | jobs | A job as a small graph of saved states: four job states, five step states, windows, routes, variety | 31 |
| crime_rules | jobs | The verbs of jobs with the hands: getting in, searching, lifts and the hot mark, fencing, tails, casing, the torch, pocket lifts, damage, yard dogs | 104 |
| car_rules | cars | The car in the town: damage by speed, a hit and the choice, fares lost after a drive-off, stops, chases, the horn, tails, taking a parked car, the ambulance | 68 |
| fare_rules | cars | Fares: what one pays, which comes next, the way in words | 22 |
| witness_mind | bridge | What a witness keeps of him from the rung the real rule gives | 31 |
| giveaways | bridge | What gives him away, each catching more than the same act without it | 20 |
| cooling | bridge | Talk cools by kind; memory does not | 13 |
| law_statement | law | Who goes to the police; stopping a witness; the walk | 26 |
| law_custody | law | What an arrest costs, in hours | 16 |
| law_stages | law | The four stages of police interest and their signs | 21 |
| law_town | law | A street on edge, finding an unseen deed, the missing, bought men | 25 |
| police_beat | law | The constable's challenge, search and chase | 18 |
| calendar_days, life_crowd, life_happen, life_rules, life_coat, paper_lines, shop_rules, way_rules | life | The calendar, who is out, happenings, small rules of the town's days, the wardrobe, the paper, shops and haggling, finding the way | 165 in all |
| crew_rules, dial_rules, firm_rules, holdup_rules, rise_rungs, rival_ladder | rise | Crew and orders, the escalation dial, the firm's growth and fronts, hold-ups, the rise's rungs, the rivals' ladders | 165 in all |
| act_beats, act_inspection, ending_state | spine | Act II's beats on states, the inspection week, the endings as states | 51 in all |

Whether the game calls each of these is the manager's to fill in after the merge.

## Known differences between a piece and the game today

- Fights: the game does not call the piece (above). The piece's simulated fight is a model of the rules for the counts ER-FIGHT-05 and 07 ask for, not the game's frame-by-frame fight. Three rules in it are the piece's own first values, in game/tune/econ.js: a man just hit keeps his guard up a moment; a jab does not stop a blow already on its way; an ordinary player reads one blow in five.
- Talk, slow replies: ER-TALK-01 says two seconds to begin and eight to finish. The piece holds that. The game still waits up to fourteen seconds for a live reply, as before, because the cloud cannot reach the live voices to measure them and live talk must keep working as it does today.
- Talk, the clock: a turn of talk still moves the game clock by a minute and a half (rules.js, talk). It never runs on while he types (gate6 holds that).
- Money: the firm's week is new (running costs of nine pounds fifty on Thursday, the drivers' takings and wages, Saturday's count). The first values make ER-MONEY-03 hold: doing nothing leaves fourteen pounds on Friday against a rent of eighteen.
