# REVIEW-FINAL: fresh review of the combat pass before push

25 Nov 2026. A fresh reviewer who wrote none of it. Checked: SUMMARY.md, COMBAT-SYSTEM.md, RULINGS-TO-REVISIT.md, TESTS.md, CENSUS-BLIND.md, SIM/README.md. Sources: SIM/results.json and results-print.txt (seed 1990), tests-work/ (RESULTS, RESULTS-2, CLEAN-RESULTS, REVIEW-1), census-work/COMPARE.md, COMPARE-2.md, A.md, B.md, CENSUS.md's counts, RESEARCH.md, RULINGS.md, canon.md, combat-design.md, and blueprint RT2-12 and 1.3.2 where the design cites them. No repository file was edited.

What was run: `combat_sim.py --seed 1990 --n 2000` on a copy reproduces results.json and results-print.txt exactly (took 18.5 s). `--n 300` written to scratchpad/final.json. One probe (scratchpad/fr/probe_mash.py) imports the simulator unchanged: a masher swinging at a man who only guards, 300 runs, counting blows to empty and the length of the gasp.

Totals: 6 must fix, 10 should fix, 9 notes.

REVIEW-1's must-fix items: 1, 2, 3, 6 and 7 are fixed (fights run on through a knock-down, a beaten Frank is a loss, no_result and timeout are reported; weapon finishing lands; the shove is under the fists cap; the hospital bill is restored and listed as R6; a masher now loses 66% and empties in a median of 7 blows). Item 4 is half fixed (finding 4 below) and item 5 is not fixed (finding 3).

---

## Must fix

### 1. The comparisons with GTA V, RDR2 and KCD2 claim more than the census holds

- SUMMARY (top section): "ahead of GTA, RDR2 and KCD2 on memory, retelling, menace as a verb, period police and lasting consequence; level with KCD2 on stealth senses". TESTS section 2: "Claims about the other games are general and come from the census rows (census-work/A.md, B.md)", followed by a table of "Ahead" verdicts.
- Evidence: census-work/B.md line 137: "Detail on GTA V melee, stealth mode and GTA IV Euphoria combat were not found in fetched sources, so those are absent." Yet TESTS fills GTA V cells for exactly those: "Stealth mode, a radar shows noise", "Choke him out: Instant takedown", "Cosh from behind: Not a feature". Other cells have no census row at all: GTA V "forgets once you leave", "They have forgotten", "Swims out", "Body vanishes"; KCD2 "remembers the face for a while", "Takedown can fail on skill", "Wake, robbed or jailed", "Rivers drown", "Brawls in taverns". GTA V "Knock out a constable unseen: Wanted level anyway" sits against B.md B098 ("Some crimes count only if seen or reported", GTA5). And every "Ahead" compares a paper design (nothing built, CS-03 and CS-26 pending) with shipped games; RESEARCH.md found no stealth numbers for KCD2, RDR2 or Hitman, so "level with KCD2 on stealth senses" has nothing measured behind it.
- Fix: in SUMMARY replace the "Against the bar" paragraph with: "On paper, against what the census found of GTA, RDR2 and KCD2 (nothing built or measured yet): LEDGER's rules cover more on memory, retelling, menace as a verb, 1990 police and lasting consequence; the stealth senses are of KCD2's kind; it leaves out GTA's physical comedy, RDR2's and GTA's gunplay and KCD2's sword skill on purpose." In TESTS, mark every cell with no census row "(not in the census)" or blank it, delete the three GTA V stealth and melee cells B.md says were not found, change the constable cell to agree with B098, and change the verdict column heading to "On paper".

### 2. Hospital days: both numbers in CS-18 are wrong

- CS-18 Test: "the simulator totals hospital days (seed 1990: about 78,000 man-days over 46,000 fights)".
- Source: results.json, the sum of consequences.hospital_days over the 22 scenarios = 86,542; 22 scenarios of 2,000 = 44,000 fights (SUMMARY says 44,000 too). REVIEW-1 (finding 9) already flagged the 46,000.
- Fix: "about 87,000 man-days over 44,000 fights".

### 3. CS-01's Test claims a single code path the simulator does not have (REVIEW-1 must-fix 5 still open)

- CS-01 Test: "the only branches on 'is Frank' are CS-15 (he cannot die) and the bot's choice of style".
- Code (combat_sim.py): townspeople alone decide by will() and so flee, yield or pick something up (lines 197 to 205); only they grab for the weapon arm, drop aggression against a blade and take the two-swinger token (213 to 223); Frank alone picks the most hurt target (212); pauses differ, TUNE "pause" (0.3, 1.4) for Frank against "npc_pause" (0.2, 0.9), with a masher's pause cut to 0.4 (426); the surface rate is the style's for Frank, fixed by kind for others (227). Several are choices a bot may make for the player, but the Test says there are none. Line 353 also skips the critical fall for Frank and gives him a serious one, where CS-15 says "When the body rule would make him dying, he is out instead". The swap test the Standard promises ("a test that swaps Frank for a townsperson ... gives the same outcome distribution") was not run.
- A sign it matters: a knife in Frank's hand wins 98.9% of decided one-on-ones ("1v1 Frank knife patient"); a knife in a townsman's hand against unarmed Frank wins 46.6% of decided ("1v1 vs knife man patient": Frank wins 53.4% of decided). See finding 10.
- Fix: rewrite the Test line: "S: the simulator shares the body, wind, counter and surface rules; the player's choices (style, target, tempo) and the townspeople's temper choices are separate functions; Frank's fall to critical becomes out (CS-15). The swap test is owed, not run." Change line 353 so a critical fall puts Frank out. Then either run the swap test (Frank's settings on a townsperson, same choices, same spread) or leave it marked owed in SUMMARY's shortfalls.

### 4. The choke is still a listed case (REVIEW-1 must-fix 4, half fixed)

- CS-13: "Each second he may break the hold (about 1 in 30, more if Frank is winded or hurt, or the man big); the struggle is heard about 6 m." SIM/README: "takedowns run through the body rule".
- Code: `if rng.random() < 0.035:  # he breaks the hold (strength, Frank's wind)` (line 648): a flat chance whatever Frank's wind or hurt or the man's kind; the struggle is never heard (only "struggle_seen" with watchers, never called with watchers). Cosh, fist and knife now run through land(); the choke does not.
- Fix: make the break chance a function of the man's capacity (or kind) and Frank's wind and hurt, as CS-13 says, re-run and quote the result; or change CS-13 to "about 1 in 30 a second in the simulator (flat; the dependence on wind, hurt and size is not yet in it)" and README to "cosh, fist and knife takedowns run through the body rule; the choke's break chance is still flat".

### 5. CS-05 says the unaware blow is doubled; the code and CS-13 say half again

- CS-05: "times wind, doubled on a man who did not see it coming". CS-13: "the body rule with force half again on a man who did not see it coming".
- Code: TUNE "unaware_mult": 1.5. The clean test's tester relied on CS-05 (CLEAN-RESULTS C09: "an unseen hit doubles").
- Fix: CS-05: "half again on a man who did not see it coming".

### 6. SUMMARY tells him a ruling is already replaced that is still his decision D3

- SUMMARY top section: "the case-by-case rules ('fists never kill', 'a knife kills only when finishing', 'before War a hit wounds only') are replaced by one body rule".
- Source: CS-23: "In the blueprint today, before War a hit 'wounds and never kills'; this pass recommends the body rule for guns too (RULINGS-TO-REVISIT R3; his decision D3)". "Fists never kill" also stays, as the same paragraph says two lines later.
- Fix: "the case-by-case rules ('a knife kills only when finishing' and the like) are replaced by one body rule ...; your fists rule stays as a cap, and whether a gunshot can kill before War is your decision D3."

---

## Should fix

### 7. SUMMARY misdescribes the blind check's measure

- SUMMARY: "A fresh designer's blind list still found 19% the census had not named specifically (6% missed outright)".
- Source: COMPARE-2.md: "Covered 135, partly 53, missed 12 ... miss rate (12 + 26.5) / 200 = 19.25%". 19% is missed plus half of partly. The share not named specifically is (12 + 53) / 200 = 32.5%.
- Fix: "A fresh designer's blind list scored a miss rate of 19% (6% missed outright, 26% named only in general, counted at half), against a 5% target: not met."

### 8. "Target met" rests on samples too small or not independent

- SUMMARY: "on a clean set of 20 ... none unanswered (target met)". TESTS: "Target (under 5% unanswered): met on the clean set (0 of 20) and on combat-only old questions (0 of 108 after CS-29)".
- Evidence: 0 of 20 cannot show a rate under 5% (with none seen in 20, the rate could still be about 15% at the usual 95% bound). The "0 of 108" is the designer's own count after writing CS-29 for the one gap, with the 8 story questions set aside; no fresh tester judged it. The old set is not independent either: the design was revised after RESULTS.md, which judged both sets (for example Q018, a held constable, is now answered by CS-19 text written for it), but TESTS marks only the fresh 30 as "Not independent".
- Fix: SUMMARY: "none unanswered of 20 (too few to prove the 5% target; 12 of 20 left a detail open)". TESTS: "Target: not shown. The clean set had 0 of 20 unanswered, too few to prove under 5%; the old set's 0 of 108 is the designer's count after CS-29, not re-judged; the old and the fresh sets both drove the revision." Add "Not independent" to the old set's revised row.

### 9. "Every one has an answer" was partly checked by the designer alone

- SUMMARY: "463 features ... every one has an answer (a rule, a named part, or out with a reason)".
- Source: CENSUS.md: "The last 28 were not re-checked by the mapper ... The 53 rows from the second blind check were mapped by the designer". Counts otherwise check out (463 rows: 344 rule, 35 kept, 84 out; M411 to M463: 45, 6, 2).
- Fix: add "(81 of the answers mapped by the designer and not re-checked)" in SUMMARY's top section or its shortfalls.

### 10. "A knife nearly always wins" is true only when Frank holds it

- R8: "A knife against one unarmed man wins 99% of decided fights in the simulator, as in life." CS-06 Standard says the same.
- results.json: "1v1 Frank knife patient" win of decided 98.9%; "1v1 vs knife man patient" (townsman's knife, unarmed careful Frank) Frank wins 49.9%, of decided 53.4%, so the knife wins 46.6% of decided; and frank_hospital_pct 34.2 (a third of those fights would have left Frank dying, out instead).
- Fix: R8 and CS-06: "With Frank holding it, a knife beats one unarmed man in 99% of decided fights; a townsman's knife against an unarmed careful Frank wins about half, and puts Frank in hospital in a third of fights. The gap comes from temper (townsmen run or hold back) and finding 3's branches; to check by the swap test." Add one line to SUMMARY's simulator paragraph: "against a man with a knife, unarmed Frank wins about half and lands in hospital in a third."

### 11. The fall: "its numbers kept" is not so, and a band is misread

- CS-07: "who was already spent (four heavy blows or one weapon blow taken) has his head strike it: serious 12 times in 100, critical 1 in 50 (inside RT2-12's 1 in 50 to 1 in 20)". The replaces list: "RT2-12 (CS-07; its numbers kept)".
- Sources: RT2-12 (BLUEPRINT-01 line 365, DEFINITIONS 21 Nov): "at least three heavy blows or one weapon blow", "a heavy or weapon blow knocks the man down", "a fall kills in 1 in 50 to 1 in 20 knockdowns". RT2-12's band is deaths; CS-07's 1 in 50 is criticals, of which CS-05 says 20 to 55 die, so about 1 in 90 to 1 in 250 knock-downs kill, below the band. Code (lines 351 to 357): `heavies_taken >= 4`, any knock-down, and serious shares the critical draw (`r < 0.02` critical, else `r < 0.12` serious), so a spent man's serious chance is 10%, not 12%.
- Fix: use three heavy blows (or list four as a change with a reason in RULINGS-TO-REVISIT and "Changed"); restrict to a heavy or weapon knock-down, or say why not; draw serious separately or write "serious 10 in 100"; and either raise fall_crit_spent so deaths land inside 1 in 50 to 1 in 20 or write "deaths about 1 in 90 to 1 in 250 knock-downs, below RT2-12's band (a change, listed)".

### 12. Open points settled without a line in RULINGS-TO-REVISIT

- (a) The fall in fights Frank is not in. combat-design.md (Since 12 October): "Whether the fall applies to fights Tom is not in ... is open". CS-01 runs townspeople's fights on the same rules, which settles it (yes). Fix: add "R17. The fall applies to fights between townspeople too (his design left it open); settled yes by CS-01."
- (b) Pulling drivers from cars. Out list: "pulling drivers was recommended out in the hype test (Q1, his to settle)". It is neither a D nor an R. Fix: add it as R18 (decided within canon, out, he can overturn) and drop "his to settle", or make it a fourth question on his page.
- (c) CS-21: "A send to kill is possible within canon ... (raised in RULINGS-TO-REVISIT, not a decision for him ...)". No R line covers it. Fix: add "R19. A send to kill: possible within canon, rare, the crewman may refuse by regard and law" or drop the bracket.
- (d) Out list: "Poisons, cash thrown as a lure, and burns or scalds as weapons (cruelty, canon)". Canon names neither poison nor a cash lure, and a cash lure is not cruelty. Fix: "Poisons (cruelty, canon) and cash thrown as a lure (out within canon: money in LEDGER is paper and earned; decided by this pass)" and add both to the R list's recorded items.
- (e) CS-29: "the bank's camera is the only one (canon, RULINGS 24 Nov)". canon.md: "CCTV rare: the bank, and a second site that is Jafar's to name"; RULINGS 24 Nov: "the bank the only CCTV". Fix: cite "RULINGS 24 Nov (later than canon's second site)".

### 13. The gasp lasts longer than CS-04 says

- CS-04: "wind returns at 0.12 a second only while he is not mid-blow ... gasps, 1.5 s at a time, until his wind comes back (4 to 8 s in all, blueprint 1.3.2)".
- Probe (300 unopposed masher runs): blows to empty median 7 (in 1.3.2's 6 to 10: good); gasp in all median 9.5 s, 10th percentile 3.2 s, 90th 20 s; 26% inside 4 to 8 s. Cause: line 394 returns wind only when the man is not busy, and a gasp sets him busy (line 413), so almost no wind comes back during a gasp, which also contradicts "until his wind comes back".
- Fix: let wind return during a gasp (at the guard rate, say) and retune until the gasp lands in 4 to 8 s; or write the measured "about 10 s (3 to 20)" and list it as a change from 1.3.2.

### 14. Tests that say "the simulator" for things it does not do (REVIEW-1 findings 9 and 10, partly unfixed)

- CS-08 Test: "the simulator counts disarms both ways": counted in the log, not written to results.json; and the weapon vanishes (`tgt.weapon = "fists"`, line 384), while CS-08 says it "drops to the ground, where anyone may take it".
- CS-10 Test: "Every man who folds to a shown weapon is a witness to rung 6": not modelled.
- CS-19 Standard "no charge without what a witness or search gives" against code that charges every touched man (consequences(), line 473 on), and s.51 never fires (no constable in any fight); the Test sentence is true but hides this.
- CS-21 Test: "sends run through the simulator with the crewman as the fighter": no such scenario.
- CS-05 Test: "about 1 in 9 of the men stabbed": results.json has no count of men stabbed, so it cannot be checked.
- CS-12: "makes Frank's shape half as easy to pick out beyond 4 m in the dark": the code halves it beyond 4 m in any light (sight_p, `0.5 if crouch and dist > 4`). The outcome still holds (crouched by day 12.9% out against walking 16.2%; under a lamp 21.2% both), but the rule as written is not the code's.
- Fix: add "(not yet in the simulator)" to the CS-10, CS-19 and CS-21 Test lines; write disarms and men_stabbed to results.json and drop the disarmed weapon as an object, or mark them owed; in CS-12 either gate the crouch's sight halving on light below 0.3 in the code or write "beyond 4 m (in any light; by day the slower walk outweighs it)".

### 15. SUMMARY's top section is not short or plain, and shortfalls are not first

- It runs to 556 words, uses "census", "blind list", "seed 1990", "the simulator (44,000 fights, seed 1990)", "button-masher", and puts the shortfalls in "What else". The page rule is one phone screen, shortfalls first.
- Fix: replace "For him, short" with about 180 words, for example:
  "What a fight should feel like: ugly, fast, over in seconds; most trouble ends with a look, a word or a blade shown; anything a man could try in a 1990 street, Frank can try; sneaking runs on dark, noise and who is looking; the street retells how it was done; every blow costs later, with a way back; alone two men beat Frank, with Ron he wins.
  What changed: one rule for injuries, one for nerve and one for the senses replace the special cases. Your fists rule stays.
  Shortfalls first: the feature list still misses about a fifth of what a fresh designer expects (target: a twentieth); 20 new questions left none unanswered but 12 with a detail open; the numbers come from trial runs of the rules on a computer, nothing is built, and other games are compared on paper only.
  From 44,000 trial fights: a careful player wins about 4 in 5 one-on-ones, a button-masher 1 in 5, two against one about 1 in 4, with Ron about 4 in 5. Fists killed nobody in 12,000 one-on-ones; a knife kills in about 9 fights in 100; unarmed against a knife Frank wins about half. Sneaking up in a dark doorway works about 6 times in 10; walking up by day about 1 in 6.
  Your decisions: D1, D2, D3 (as now)."

### 16. REVIEW-1 should-fix items still open in the code

- Finding 15: `blade = target.weapon == "knife" or TUNE["weapon"][target.weapon]["menace"] >= 0.45` (line 217) still treats a cosh as a blade for caution, pick-ups and weapon-arm grabs, a threshold case where CS-09's fear term should decide.
- Finding 12: all scenarios share one random stream, no interval is printed beside rare rates, and death and fall rates rest on 0 to 33 events at 2,000 fights (the n=300 run gives "1v1 cosh, Frank finishes" 70.0 deaths per 1,000 against 42.5).
- Fix: drive caution and pick-ups from will()'s fear term; seed each scenario by seed plus index; run the death and fall scenarios at 50,000 and print a 95% interval; or list both as known shortfalls in README's limits.

---

## Notes

17. SUMMARY: "by day about 1 in 6" is walking (16.2%); crouched by day it is 12.9% (about 1 in 8). Write "walking up by day". "Two against one ... about 1 in 4" is 28.3%; "a little over 1 in 4" is closer.
18. SUMMARY: "No deaths in 2,000 one-on-one fist fights" undersells the evidence: all six one-on-one fist scenarios (12,000 fights, no finishing) had none. Write "none in 12,000 one-on-one fist fights (without finishing a downed man)".
19. CS-20 Test: "about 3 in 10 beaten men take revenge ... about 1 in 12 report it". results.json gives 17,692 revenges and 4,652 reports over 57,855 men touched (any injury, bruises included): 30.6% and 8.0%. Write "men Frank hurt", not "beaten men". Revenge and reports are still uniform random draws, not the man's temper (REVIEW-1 note 20).
20. SIM/README: "It takes about 15 s": 18.5 s here. "takedowns run through the body rule": not the choke (finding 4).
21. CENSUS-BLIND: "at the rate of fall it would likely land near 10 to 12%": a line through two points. Write "a guess from two checks".
22. R3: "stab and gunshot data both show point wounds kill by where they land": RESEARCH.md says the TARN region table mixes stab and shot and its "column alignment [is] unclear, verify". Write "the mixed stab and gunshot table (alignment unverified) points that way".
23. Replaces list: "LH-12's 10 to 30 s for a struck constable stays for fists (CS-05's fist band 10 to 60 s contains it)": keeping a separate band for constables is a listed case under CS-01; say which band a struck constable uses (CS-05's, under one rule).
24. Dead code from REVIEW-1 note 24 remains (`pass` branches at lines 275 to 276 and 285 to 286).
25. Style: no em dashes, no italics and no American spellings found in the six files ("meter" here is the gauge, correct in British use). The one style fault is SUMMARY's top section (finding 15). CENSUS.md, outside the six, says "the seven games" and "CS-01 to CS-29" while its rows carry eight game labels and CS-30 exists.

## Checked and found sound

Every other number checked matches results.json or results-print.txt: one-on-one win rates (78.6, 18.8, 72.8, 77.6, 55.6), 2 v 1 (28.3, 43.8 lost, 27.8 stopped), 3 v 1 1.0 (84.2 lost), with Ron 77.8; durations 15.1 s and 30.3 s; knife 91.5 deaths per 1,000; 2 v 1 knife 77.7% of decided; boots finishing 16.5 per 1,000 (1 in 48 of wins) and cosh 42.5 (1 in 21.5); bystanders 15.2% and police 1.9%; yields 0.39 and flights 0.15 a fight, half flee a knife (0.51); CS-05's 68% hurt, 21% serious, none critical; the threat table (12, 27, 47; 0, 1, 6; 21, 51, 81; 0, 7, 23) and the threat weights (0.68, 0.8, 0.9); the stealth rows (61, 14, 19, 6; 36, 43; 21 and 71; 16 and 77; 37 and 35); the takedowns (choke 43, 14, 38; cosh 35, 16, 6, 0.3 and, of those reached, 62, 27, 10, 0.5; fist 1 in 8 and 1 in 7; knife 7.5% and 1 in 8 reached); the held-choke curve; R7's 79% and 94%, 19% and 22%; CS-15's 5% and 44%; the charges present at every level; the test tables' counts (42, 68, 6; 86, 21, 9; 6, 18, 6; 28, 2, 0; 8, 12, 0; 69 moved; thirteen additions); the blind checks (116, 60, 24, 27.0%; 135, 53, 12, 19.25%; 12% and 6%); CENSUS.md's 463 rows and its answer counts; the research figures (7.2%, 0.9%, Iceland 17%, 5 to 10 s, 62 to 157 s, Tipton 130 s, Philpot 90.9% and 1.10 a bystander, the boxing minute, 177 m from the weapons spec). D1 to D3 are flagged as his decisions; R1, R2, R4 to R16 match COMBAT-SYSTEM.md. No conflict found with canon on alcohol, gambling, children, cars, drugs, brands or Frank's death.
