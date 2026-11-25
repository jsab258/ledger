# REVIEW-SYSTEM: fresh review of COMBAT-SYSTEM.md and its simulator

25 Nov 2026. Fresh reviewer. Files checked: production/lane/blueprint/combat/COMBAT-SYSTEM.md, SIM/combat_sim.py, SIM/results.json, SIM/results-print.txt. Sources: RULINGS.md, canon.md, combat-design.md (his "LEDGER Combat: Final State", 12 Oct, with the 2 Nov section), research/BANDS.md, and his rulings of 24 and 25 Nov as given in the brief. No repository file was edited.

What was run: `combat_sim.py --n 2000` (seed 1990) reproduces results.json and results-print.txt exactly, so the published numbers are the code's. `--n 300` was run to scratchpad/review.json. Two probe scripts (scratchpad/revw/probe.py, probe2.py) import the simulator unchanged and measure what results.json does not store (end states, causes of critical injuries, threat rates at other menace values, the cosh on a downed man, blows to empty a masher).

Totals: 7 must fix, 10 should fix, 7 notes.

---

## Must fix

### 1. A fight ends at the first knock-down, and a beaten Frank is not counted as a loss (biases every win rate)

- Evidence: the loop ends as soon as one side has nobody "fresh" or "hurt" (combat_sim.py line 427, `if len({m.side for m in self.men if m.active()}) < 2`). "down" is not active, so a man knocked down for 2 to 5 s ends the fight, although CS-04 says "down (on the ground 2 to 5 s, then up unless beaten or out)". Then line 551 counts Frank as up if `standing()`, which includes "beaten", so a beaten Frank facing active foes falls into `no_result`, which results.json never reports.
- Probe, seed 1990, 2,000 fights each:
  - 2 v 1 patient: Frank ends beaten 890 times (44.5%), down 293, out 166. The design (CS-11) says "patient Frank wins 2 v 1 19% (with 24% lost and the rest stopped by a bystander or the police)". results.json: stepped_in 11.4%, police 1.9%. So about 44% of "the rest" are fights Frank lost on his feet. His true loss rate is nearer 68%, not 24%.
  - 1 v 1 masher: Frank ends beaten 534 times (27%), uncounted; results.json shows lost 20.5%.
  - 1 v 1 patient: 314 of the 2,000 opponents (16%) end merely "down", i.e. a win scored on a 2 to 5 s knock-down; 121 of Frank's "losses" are likewise a knock-down he would have got up from.
- Fix: end a fight only when a side has nobody standing who will fight on (out, dying, dead, fled, yielded, or beaten and not getting up); let "down" men rise on their timer. Count Frank beaten as a loss. Report `no_result` and `ended_by_timeout` in results.json. Re-run every headline in CS-04, CS-09, CS-11, CS-14, CS-15.

### 2. Finishing with a weapon does nothing; the "cosh about 1 in 250" figure is unsupported

- Evidence: `finish()` (line 439) uses "heavy" when Frank holds a weapon, but `land()` returns at once for any action but "stamp" on a man who is not standing (line 232, `if not tgt.standing() and act not in ("stamp",): return`). Probe: fifty cosh heavies on an unconscious man leave damage `{}` and worst "none". In the "1v1 cosh, Frank finishes" run, the only finishing blows that landed were 223 stamps, from Franks who had been disarmed back to fists.
- Design, CS-14: "finishing with boots after a won fist fight kills about 1 in 90 (11 per 1,000), with a cosh about 1 in 250." results.json: "1v1 cosh, Frank finishes" deaths_per_1000 4.0 against "1v1 Frank cosh patient" 2.5. The difference is noise plus disarmed stamps. CS-14's "a weapon can kill" in the quiet after is untested.
- Also: 11 per 1,000 is per fight; per won fight (83.2%) it is about 1 in 76, not 1 in 90.
- Fix: let a weapon blow land on a downed man (zone weighted to the head as the stamp is, force doubled as on a man who cannot defend); re-run and restate both rates per won fight.

### 3. A shove into a wall can kill in a fist fight; the design says only the fall can, and the shove question is open

- Evidence: a grab with fists leads to "shove_surface" (lines 375 to 377). The fists cap applies only to jab, heavy and kick (line 291), so the shove follows the uncapped body rule and can reach critical. Probe causes of critical injuries: 1 v 1 patient `critical_blunt_shove_surface` 2; street 4 (with 2 deaths); runner 1. results.json: "1v1 fists street" deaths_per_1000 0.5 with fall_critical_per_1000 0.0; "1v1 fists runner" 0.5 with 0.0. Those deaths are shoves, not falls. "1v1 fists patient" foe_worst critical 3.
- Design, CS-05: "His fists line (30 Oct): fists alone never take a man past serious. The fall can (CS-07)." CS-05 Test: "one-on-one fist fights 0.0 deaths per 1,000 (a fall at a kerb adds 0.5 to 3)". That holds only for the patient style. CS-07 says "Surfaces are force, not finishers" but never says a shove can kill.
- Source: his ruling of 30 Oct names "a fall on a kerb, wall or step after a blow"; combat-design.md, 2 Nov: "whether a shove (rung 4) into a kerb can kill is open".
- Fix: either cap a shove into a surface at serious (as fists) and let only the fall reach critical, or state in CS-07 that a shove into a hard surface can kill, raise it in RULINGS-TO-REVISIT as his question, and report it separately from falls.

### 4. Takedowns from behind are listed cases, not the body rule

- Evidence: `approach()` returns fixed outcome tables: cosh `r < 0.02` dead, `< 0.15` serious, `< 0.75` out, else staggered (lines 627 to 635); fist `r < 0.33` out (line 638); choke break-free a flat 0.035 a second (line 616). `land()` has an `unaware` parameter that doubles force (line 252) but nothing ever passes it, so the "behind" manner (line 248) is never set in any fight either.
- Design, CS-05: "One rule decides every injury for every person ... Nothing is decided by a listed case." CS-13: "Cosh or any blunt blow to the head: force doubled on an unaware man: once he is reached, out about 6 in 10, staggered a quarter, a serious head injury about 1 in 8, death about 1 in 50." Those four numbers are the code's inputs, not results of the doubled force. The simulator's own header says "Nothing here is a listed case".
- Fix: resolve the last metre through `land()` with `unaware=True` (cosh, fist, knife) and the body rule's knock-down and knock-out; let the choke's break chance depend on the man's capacity and Frank's wind and hurt, as CS-13 says. Report what comes out; retune the force or thresholds if the band is wrong, not the outcome.

### 5. The simulator branches on "is Frank" in its rules, failing CS-01's own test

- Evidence: only Frank may use a surface (line 220, `if m.is_frank and self.place["surface"]`), so no opponent ever shoves Frank into a wall. Frank counters every time inside the window if his style's defence is over 0.5, an opponent only with chance equal to his defence (line 409). Target choice uses hurt only for Frank (line 205). Opponents' pauses are shorter (`npc_pause`). Pick-ups, the weapon-arm grab and the guard roll are opponent-only. `will()` and temper never apply to Frank.
- Design, CS-01: "any branch on 'is Frank' outside CS-15 (he cannot die) and CS-20 (his growth) fails the check." A bot's choices for the player are fair; mechanics that only one side can use are not.
- Effect: Frank's win rates are inflated by moves and counters his opponents cannot use (street style uses surfaces 2.05 times a fight; opponents never).
- Fix: put the player's styles in one choice function that any man can use, and give opponents the same surface and counter rules. Then add the swap test CS-01 promises: Frank's settings on a townsperson give the same outcome spread.

### 6. "Hospital costs days, never money" changes his design without saying so

- Evidence: CS-15: "hospital costs days, never money, and plants a witness".
- Source: combat-design.md (his text, 12 Oct): "He wakes in hospital or on the pavement with the injuries, the bill, and a street that knows he lost"; The aftermath: "Treatment costs money and plants a witness". No later ruling in RULINGS.md removes the cost. The design's header promises "where this text differs from a ruling it says so and the point is in RULINGS-TO-REVISIT.md, never changed silently".
- Fix: restore the cost ("hospital costs days and money"), or keep the change, mark it in CS-15 as differing from his 12 Oct design, and add it to RULINGS-TO-REVISIT.md.

### 7. Mashing neither empties Frank as stated nor loses, against his design

- Evidence: results.json "1v1 fists masher": win 48.3%, lost 20.5% (with 27% more beaten and uncounted, finding 1). Probe: a masher swinging at an unresisting man empties after a median of 17 blows (300 of 300 runs). In fights `gasp_frank` fired 238 times in 2,000 masher fights.
- Design, CS-04: "So mashing empties Frank in about six to ten blows (blueprint 1.3.2)." The code: wind regained over one masher cycle (about 1.6 s at 0.12 a second) roughly equals a blow's cost, so wind barely falls unless he is hit.
- Source: combat-design.md: "Mashing tires you out and loses."
- Fix: retune wind (a lower return while attacking, or higher costs) until an unopposed masher empties in six to ten blows; then check that a masher loses most fair one-on-ones once finding 1 is fixed. If the design means to keep a near-even masher, say so and raise it with him.

---

## Should fix

### 8. The quay settles an open question without saying so

- Evidence: CS-07: "a man thrown or falling in ... if unconscious with his face in the water he is dying (critical) and dead in about two minutes unless pulled out". A man knocked out by fists at the quay edge can therefore die.
- Source: combat-design.md, 2 Nov: "Open: ... whether the quay edge counts, since the ruling names a kerb, a wall or a step". His 30 Oct ruling names only those three.
- Fix: say in CS-07 that this extends the 30 Oct fall to the quay, and put the point in RULINGS-TO-REVISIT.md. (Rolling a man in on purpose is a killing canon already allows and needs no change.)

### 9. Numbers in the design that the results do not support as stated

- CS-10: "at the start of the game (Frank's menace 0.3): ... a word with a knife shown about half". results.json scenario "1v1 menace with knife shown" runs at `menace=0.5` (line 707) and gives ended_by_threat 59.0%. Probe at 0.3: 47.4%, so the claim is right but no simulator scenario shows it. "two men together almost never (1 in 20 with a knife)": no 2 v 1 knife-shown scenario exists; probe gives 5.4%. Fix: add both scenarios at 0.3 and cite them.
- CS-18: "about 78,000 man-days over 46,000 fights". results.json sums hospital_days to 78,398 over 22 scenarios of 2,000, i.e. 44,000 fights. Fix: 44,000.
- CS-05 Test: "of losers of a one-on-one fist fight 65% hurt, 19% serious, 0.2% critical". results.json "1v1 fists patient" foe_worst: hurt 1,307, serious 385, critical 3 of 2,000 (65.4%, 19.3%, 0.15%) counts every opponent, including the 17.5% Frank did not beat. Fix: say "of Frank's opponents", or count losers only.
- CS-05 and CS-07: "a fall at a kerb adds 0.5 to 3" and "kerbside scenario ... deaths 0 to 3 per 1,000 fist fights". results.json "1v1 kerbside patient": deaths_per_1000 0.0, fall_critical_per_1000 0.5 (one man, who survived). Nothing is added; a band starting at 0 cannot fail. Fix: run the kerbside case large enough to measure it (finding 12) and state the measured rate.
- CS-11: "the rest stopped by a bystander or the police" (finding 1).
- CS-11 Standard "wins a fair two against one about one time in four"; Test 19%, lower once finding 1 is fixed. The design does not say the standard is missed. Fix: say so and retune, or mark it a known shortfall.
- CS-12: "unlit street ... crouched 43%" (results 0.441); "doorway ... 7% turned" (0.062); "under a lamp crouched 21% out" (0.221); "by day walking ... 74% spotted" (0.75). CS-13 gives "choke out 45%" for the same conditions as CS-12's 43%, from a second run. Fix: quote one run, rounded correctly.
- CS-12: "gravel and metal decks cut success by a tenth to a fifth (crouched, unlit: 39% and 36% against 44%)". The 44% is wet cobbles, itself the louder surface; against dry flags (0.478) the cut is a fifth to a quarter (0.386, 0.362). "walking on a metal deck by half (23%)": against dry flags walking (0.404) that is about two fifths. Fix: compare with dry flags and restate.
- CS-05: "of the men stabbed about 1 in 9 die". results.json does not record how many men were stabbed. Probe: 1,696 stabbed, 203 dead (1 in 8.4) in a fresh stream; consistent, but unverifiable from the file. Fix: write `men_stabbed` to results.json.

### 10. Tests the design says the simulator runs, which it does not

- CS-15: "the simulator's lost fights ... all route to a come-round, never a game over". No come-round exists in the code; it only counts.
- CS-24: "the simulator with Frank's defence and wind costs at 1.25 times". No such scenario.
- CS-21: "sends run through the simulator with the crewman as the fighter". No such scenario.
- CS-08: "the simulator counts disarms both ways". Counted in the log, never written to results.json; and the disarmed weapon vanishes (`tgt.weapon = "fists"`, line 374) instead of dropping where "anyone may take it".
- CS-10: "every man who folds to a shown weapon is a witness to rung 6". Not modelled.
- CS-19 Standard "no charge without what a witness or search gives"; Test "the simulator's charges fire at every level". `consequences()` charges every touched man, witnessed or not (line 466), and no constable is ever in a fight, so s.51 never fires.
- CS-17: the "behind" manner never occurs in a fight (finding 4) and the woman or over-sixty factor is never exercised (`victim_sex_age` always "man").
- Rules in the design with no code, affecting headlines: CS-07's "out of the fight about 4 s" after a shove and glass cuts; CS-03's "0.4 s apart" for two attackers; CS-09's grudge, watched by his own, high law shouting, a tie stepping in; CS-13's break chance "more if Frank is winded or hurt, or the man big" and the struggle heard at 6 m; CS-12's crouch "in the dark" (the code halves sight beyond 4 m in any light, day included, line 578).
- Fix: either implement each and report it, or change each Test line to say "not yet in the simulator".

### 11. The held choke's 24% is set by an invented hold length

- Evidence: `extra = rng.uniform(20, 120)` (line 621): how long the player holds on is drawn at random, and `hazard = 0.0 if extra < 20` can never apply. CS-13 Test: "held choke dead 24% of all attempts (about half of those that reach the hold)". That figure depends only on the assumed spread of hold times.
- Fix: report death risk by seconds held past the knock-out (for example 10, 20, 40, 60, 90, 120 s), which is what D1 asks him to judge. Note that the research's 62 to 157 s is from the start of the hold, not from the knock-out.

### 12. Rare-event numbers rest on one to three events

- Evidence: deaths_per_1000 of 0.5 is one death in 2,000. The `--n 300` run gives "1v1 fists, Frank finishes" 0.0 deaths against 11.0 at 2,000, and "1v1 fists street" 3.3 against 0.5. The CS-05 standard "at most 1 in 1,000" cannot be tested at 2,000 fights. All scenarios share one random stream, so changing one shifts every later one.
- Fix: run death and fall scenarios at 50,000 or more, print a 95% interval beside each rate, and seed each scenario separately (seed plus scenario index).

### 13. The stab research is misquoted

- Evidence: CS-05 Standard: "UK hospital data: about 7% of stabbed patients die in hospital, and about one in six died before hospital in one national series".
- Source: BANDS.md: 7.2% is TARN England and Wales 2000 to 2005; the "one in six before hospital" is the Iceland series (88 people, 2000 to 2015), not UK; the recent UK knife-only figure, 0.9% (2014 to 2018), is left out.
- Fix: name Iceland, give the 0.9% to 8% in-hospital band, and say the 1 in 10 to 1 in 15 target is judgement within it.

### 14. The emptied gasp is 1.5 s; the code says the blueprint has 4 to 8 s

- Evidence: CS-04 "gasps for about 1.5 s"; code line 401 `busy_until = self.t + 1.5` with the comment at line 218 "(1.3.2: 4 to 8 s)". CS-04 cites blueprint 1.3.2 without saying it changes it.
- Fix: check blueprint 1.3.2; if it says 4 to 8 s, either use it or list the change under "Changed" with a reason.

### 15. Threshold cases where the general rule should decide

- Evidence: `threat = 0.8 if shown >= 0.4 else 0.5` (line 524): a knuckleduster shown (menace 0.35) counts as a bare word, though CS-10 says "a weapon shown 0.8". `blade = target.weapon == "knife" or menace >= 0.45` (line 210): a cosh is treated as a blade. Pick-up rates (0.02, 0.05) and the brick-or-chair draw are fixed numbers, not the temper.
- Fix: make the threat the shown weapon's own menace (scaled), and let the fear term in `will()` drive caution and pick-ups instead of a blade flag.

### 16. The fall is a listed case in the design itself

- Evidence: CS-07: "a man ... who was already spent (four heavy blows or one weapon blow taken) has his head strike it: serious 12 times in 100, critical 1 in 50"; code lines 341 to 347 use a flat 2% once a count is reached, and the serious roll shares the same draw, so a spent man's serious chance is 10%, not 12%.
- Fix: make the fall a blow to the head at a force set by the knock-down's force and the man's head harm, through the body rule, tuned so that the kerbside rate lands inside RT2-12's 1 in 50 to 1 in 20 per spent fall.

### 17. Step-ins are not calibrated to the research cited

- Evidence: `p = stepin_per_5s * 1.10 ** bystanders / 3` (line 421); the "/3" has no source; checks every 5 s only. CS-09 cites Philpot's 91% of conflicts with a step-in; the sim gives 6.5% of 1 v 1 fights. BANDS.md notes Philpot's conflicts average 3.27 minutes and include non-violent ones, and Liebst finds the opposite crowd effect for single bystanders.
- Fix: state the rate per second of violence that the design intends, derive it from the sources with that caveat, and drop the unexplained divisor.

---

## Notes

### 18. Frank's menace lowers his own allies' will

`will()` subtracts `0.08 * self.menace` for every man, Ron included (line 183). Apply it only to Frank's opponents.

### 19. A knock-out is ABH under the charging standard

BANDS.md (CPS): ABH includes "loss of consciousness". The sim charges by worst injury level only, so a man knocked out with light damage is "common assault". Raise a knock-out to ABH in CS-19 and the code.

### 20. CS-20 contradicts itself

Standard: "every man Frank beat meets him within three game days"; Test: "about 3 in 10 beaten men take revenge". (results.json supports the 3 in 10 and 1 in 14: 30.3% and 7.3% of 56,564 touched men.) Also revenge and law are uniform random draws, not the man's temper. Reword the standard to "every man who takes revenge".

### 21. Dogs are attributed to canon

CS-06 and "Out on purpose" give "no dog is ever harmed" with canon as a source; canon.md has no line on dogs. Cite the blueprint (1.4.8) only.

### 22. DS Ellis's terms are incomplete

CS-19 gives "about £800 then £100 a week"; RULINGS 24 Nov adds "a missed week ends it". Add it.

### 23. "Roughly even" against 82.5%

combat-design.md says both "A fair one-on-one is roughly even, and skill tips it" and "A skilled player wins most fair one-on-ones". The patient bot wins 82.5% against a mix that includes wiry men of nerve 0.2 to 0.5, who often flee. State which target the 1 v 1 tuning aims at and how "fair" is defined (an opponent of equal nerve and capacity).

### 24. Dead code

Lines 265 to 266 and 275 to 276 (`pass` branches), line 426 (`sides` unused), the `extra < 20` branch (line 622) and the double negative in `will()` (`(0.1 if m.wounds else 0) * -1`). Harmless, but they hide intent in a file reviewers must trust.

---

## Checked and found sound

Force, weapon, threshold, edge-wound, capacity, wind-cost, menace and knock-out values in CS-04 to CS-06 match TUNE exactly. Results reproduce at seed 1990. Supported as stated: 1 v 1 patient win 82.5%; masher 2 v 1 1%; 3 v 1 under 1%; 2 v 2 with Ron about 80%; knife used by Frank 91 deaths per 1,000; yields a third and runs an eighth in 1 v 1; half run from a knife; a word folds about 1 in 8 at menace 0.3; 7% bystander and 1% police endings; cosh, fist, knife and choke takedown shares; revenge 3 in 10 and reports 1 in 14; hospital days 78,398. No conflict found with canon on alcohol, gambling, children, cars (never kill), drugs or brands; the knife from the first second, rare late guns, no armour or healing items, the long heat, the unseen officer, fire, holding overnight and PEGI 18 within canon's limits are all carried as ruled. D1, D2 and D3 are flagged as his decisions, as the brief requires.
