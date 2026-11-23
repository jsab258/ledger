# LEDGER: the blueprint

The whole game as one design. Version 1, 23 November 2026, by the blueprint keeper (claude-opus-5-5). This is the one document the design flows into; the giant one-shot prompt is written from it alone, and the one-shot starts only when it is complete (his ruling of 20 and 21 November; plan date the reset of Monday 7 December). Canon outranks it and his rulings decide what is in and out. Nothing here is new: the keeper consolidates what the design sources already say, settles their clashes by date and ruling, and lists what is missing.

## The game in one page

Britain, Monday 15 October 1990, a grey afternoon. Tom Nowak, 32, walks off the ferry in Meridian, a fictional British port town, with one suitcase and a letter. His uncle Mickey has died and left him Mickey's, a minicab office on Quay Street in the Hook: two tired cars, a radio, Sheila the bookkeeper who will not use his name, Ron the old docker who minds the door and the rank, a book of debts nobody can collect, and an envelope expected at the ferry landing after ten. Fifteen to twenty hours later the port does not move without him.

The minicab firm is the criminal machine: cover, eyes, alibi and risk. The player mostly acts with his hands (jobs, break-ins, fights, driving, working the street) while a living town watches, remembers and talks; talk is where the consequences surface, never the main thing he does. Tom rises in position (what people call him: the new owner, Nowak, Tom, Tommy; who works for him; what he owns, wears and can enter), never in numbers. Three acts: The Inheritance (a week with nothing and nobody), The Rise and the Squeeze (cars, crew, fronts and rackets while three rivals squeeze him), The Ledger Comes Due (the books are opened and the ending is what the town and the books hold); two or three endings.

The bar: Kingdom Come: Deliverance II for immersion and finish; GTA for why people play for hours; GTA VI measured as state of the art, the higher bar wins. The measure: a panel of eight kinds of player recommending it after a whole evening and a whole week.

## What binds every part (canon and his rulings)

- Third person, PC only on Windows; Britain 1990 (window 1988 to 1992); late analogue: phone boxes, cash, paper; CCTV rare.
- Content rule: no alcohol or gambling, shown or spoken of; tobacco stays; no children anywhere (the school stands closed); violence with blood and light gore, no torture or cruelty as spectacle; killing possible, rare, permanent, remembered forever; drugs only off screen; no sexual content; no slurs; every brand fictional.
- A car can hurt a person badly and never kills; only the player's car can strike anyone. Fists knock a man out and never kill alone; a fall after a blow can, rarely. Guns rare, late and after melee, through an escalation dial. Reloading is never stopped. From the approved design (canon OPEN 3) rather than a ruling: Tom cannot die and there is no game over.
- Clock: 60 real seconds a game hour; Act II about 5 game weeks, about 7 weeks in all (21 Nov). Length 15 to 20 hours with side stories inside.
- Map: the Hook plus its docks (the docks cut first if time runs short). Camera at the Between height, 3.1 m back, field of view a setting of 75 to 100, default 86.
- No minimap, waypoints or markers; a paper map and street signs. No stats, levels or skill trees; difficulty only as assists. No jump, no crafting, no multiplayer, no mods at release, English only.
- The moat: every act exposes seven perceivable slots; a five-rung identification ladder, its top rung gated by relationship; permanent per-person memory; gossip through schedule crossings; live talk with memory and local voice; the deterministic Core decides every outcome, language models classify and never adjudicate.

## How to read it

Every part has a short entry: how it works; its standard (a number or a pass-or-fail test) and test; the source of that standard (a reference game's measured figure, a dated real-world figure, his ruling or canon, or DECIDED by the design proof for him to overturn); its status; and its coverage.json row id. Statuses:
- measured: the standard rests on a real figure (his ruling or canon, a reference game, a dated real-world figure or published standard);
- decided: a design decision with a pass-or-fail standard, his to overturn;
- pending: defined, a number waits on a named, dated study (most on the PC measuring of 23 to 28 November);
- unmeasured: defined, no reference figure behind its number yet;
- out: left out by his ruling or canon (kept so nobody builds it);
- outside: Unreal-only work (looks, engine, performance), judged in Unreal against the Hook sheet and KCD2 frames;
- machinery: how the game is made, not met by the player (group 9; no coverage row).

Sources, newest first; on a clash the newer wins unless canon or a ruling says otherwise: canon and RULINGS (on wip); DEFINITIONS-2026-11-21 (its design pass 4 of 23 Nov newest), GTAVI-MAP, FIT-CHECK, CLOUD-FIGURES, PANEL-BAR and PRIVACY-CHECK of 21 Nov; the description copy of 21 Nov (redteam2/GAME-DESCRIPTION-COPY-2); DESIGN-ADDENDUM of 20 Nov; the description inside ONE-SHOT-PROMPT of 20 Nov; VISION of 19 Nov (approved); DESIGN and BUILD-ORDER of 18 Nov; the parts tree.

## The chapters

| File | Group | Parts | measured (on real figures) | decided | pending | unmeasured | out | outside | machinery |
|---|---|---|---|---|---|---|---|---|---|
| BLUEPRINT-01-hands.md | What the player does with his hands | 86 | 17 (7) | 32 | 22 | 15 | 0 | 0 | 0 |
| BLUEPRINT-02-town.md | The town under the hood | 94 | 25 (10) | 53 | 6 | 10 | 0 | 0 | 0 |
| BLUEPRINT-03-story.md | Story and people | 45 | 18 (3) | 10 | 8 | 8 | 0 | 1 | 0 |
| BLUEPRINT-04-place.md | The place | 33 | 6 (0) | 8 | 1 | 0 | 0 | 18 | 0 |
| BLUEPRINT-05-looks-sound.md | How it looks and sounds | 39 | 5 (0) | 1 | 0 | 8 | 0 | 25 | 0 |
| BLUEPRINT-06-interface.md | The interface and the Ledger | 19 | 5 (1) | 13 | 0 | 1 | 0 | 0 | 0 |
| BLUEPRINT-07-shape.md | The game's shape | 48 | 17 (3) | 10 | 5 | 3 | 13 | 0 | 0 |
| BLUEPRINT-08-technical.md | Technical | 25 | 16 (11) | 4 | 0 | 0 | 0 | 5 | 0 |
| BLUEPRINT-09-machinery.md | The machinery | 22 | 0 (0) | 0 | 0 | 0 | 0 | 0 | 22 |
| BLUEPRINT-10-shipping.md | Shipping | 13 | 2 (1) | 2 | 0 | 0 | 1 | 8 | 0 |
| all | | 424 | 111 (36) | 133 | 42 | 45 | 14 | 57 | 22 |

All 401 coverage.json rows are in, each once (284 parts-tree leaves and 117 rows added by the reviews, red teams, fit check, clock and rulings, each filed under the parts-tree part it belongs to), plus the 22 machinery parts and one ruled part with no coverage row yet (1.6.15 hold-ups, his ruling of 20 Nov, designed in DESIGN-ADDENDUM A41). The nine clock rows are measured on his ruling of 21 Nov (design pass 4 took clock B on 23 Nov). Design pass 4 of 23 Nov is folded in (no chase timer, the crowd per frame, car entry, three new chase rows DP5-C01 to C03).

BLUEPRINT-11-conflicts-and-gaps.md holds the 194 conflicts settled or corrected settled (what won and why), the 303 gaps for the design proof and the source traces not found.

## The story chapter

Pending. Story v3 (production/lane/story/v3/) is being written and is not picked; its phase 1 ranked twenty premises on 21 Nov. The latest full draft, STORY-FINAL.md (The Passenger, 20 Nov), was never approved. His rulings want his yes on the measured story before the one-shot. Until v3 is picked, chapter 03 carries the story's machinery (acts, beats firing on states, endings chosen by the town and the books, side stories, fares, street happenings) but no plot. When v3 is picked, this section names it and chapter 03 points to its bible.

## Questions that are his (canon, scope, money)

Each with the recommendation. Until he answers, each part is built to the recommendation and marked so; his answer replaces it.

- Q1 (1.1.8, OUT-08): Vaulting low walls and fences, next to the no-jump ruling (scope). Recommended: Keep vaulting at set places only.
- Q2 (1.2.10): Taking a parked car by force (scope, rating). Recommended: Yes, parked cars only, about 6 s by force; never a driver pulled out.
- Q3 (RT-09, 4.3.6): Tom's own line: he will not strike women, over-sixties or the priest. Sparing the priest brushes canon's "religion is never a mechanic" (canon). Recommended: Keep it as Tom's character, never framed as a religious rule.
- Q4 (RT2-11): Holding strike for 2 s over a downed man: is that a "finisher" under his combat design ruling of 12 Oct? (his ruling) Recommended: Keep as written: no animation, asked twice, camera turns away.
- Q5 (2.6.8): Can DS Ellis herself be bought? (canon: police corruptible as individuals, never as a thesis) Recommended: No, as the description says; two named officers can be.
- Q6 (2.14): Does every named person get his or her own temper? (scope, open since 29 Sep) Recommended: Yes, measured before it lands.
- Q7 (3.1.6, 2.12.1): Sheila's trust: what opens the book and her use of his name (his open point C12, canon). Built meanwhile to "a clean week in which he never asked her to put the books off". Recommended: A state the town can see, not a day count.
- Q8 (3.2.1, 5.6.1): Uncast voices: Danny, June, Father Walsh and six more (canon: no voice cast without his yes). Recommended: One listening page for all nine; he picks the best fit for each.
- Q9 (3.3, 3.2.3, FIT-L01): Advisor decisions on scope: about 25 side stories inside the ruled hours; 60 street lines for the 12 most seen, 30 for the rest. Recommended: Keep both; he may cut lines to about 50 to save writing.
- Q10 (4.9, 2.2.5): A second CCTV site, which canon leaves to him (canon). Recommended: None: the bank alone.
- Q11 (5.7.1, FIT-P09): A short made-for-the-game score under the few cut scenes and act ends (money; music is otherwise only where it plays in the world, and canon already rules out real bands and lyrics). Recommended: Yes, short and made for the game; none is built until he says.
- Q12 (7.1): Restaging his approved first hour of 29 Sep (arrival by ferry, a fare at 2:30, the debt book at 4:30), his question 4. Recommended: Yes, as DESIGN section 15 stages it.
- Q13 (7.16): Pastimes: is the boxing club the only one? (scope, his question 3) Recommended: The club alone.
- Q14 (8.6.1): The live-talk allowance per copy and the monthly ceiling (money). Recommended: Fix only after the talk bench measures a playthrough's cost, as his 24 Sep ruling says.
- Q15 (10.2, 10.12): The store fee, the price, a paid age-rating review, a demo (money). Recommended: PEGI 16 as the design target; pay only when 2026-grade frames exist; a demo of the first evening; price after the prototype.
- Q16 (10.6, 10.7): District updates free or paid; achievements at release (scope, money). Recommended: Decide free or paid with the release price, say nothing now; no achievements at release.
- Q17 (10.8, 10.10): The first store capsule (a whole street frame) and a name search for LEDGER (his accounts and money). Recommended: Show him the capsule from a packaged frame; he runs the name search before the Coming Soon page.
- Q18 (1.5.3, DP5-C02, FIT-G1, OUT-05): Design pass 4's R1: his map (the Hook plus the docks) holds car chases of 1 to 3 minutes without repeating roads; reference chases ran 2 to 8 (leads) (scope). Recommended: Keep the map; chases rich in lanes, yards, the switch to foot and the search, not length; check again when the five-sample lengths land.
- Q19 (7.13, CLK-06): Design pass 4's R2: his clock (60 s a game hour, a 24-minute day) is the shortest of the references (48 to 144 minutes), and its running time is 13 to 20 hours against his 15 to 20 (scope). Recommended: Keep 60 s; three bot playthroughs check the hours, and a short median is fixed by fewer nights skipped, never a longer calendar.
- Q20 (3.1, BLUEPRINT.md story section): His yes on the measured story, which the one-shot waits on (story, canon). Story v3 is mid-way (phase 1 ranked twenty premises; phase 2 writes three bibles from 23 Nov); STORY-FINAL (The Passenger, 20 Nov) was never approved. Recommended: Wait for v3's measured pick (its phase 2 and measure this week) and give the yes on that; not on STORY-FINAL.

## Keeping it

Every keeper run reads KEEPER-LOG.md first, then folds in what has landed since: the PC measuring sheets, the aaa-studies files (production/research/lane/aaa-studies/), the blueprint preparation files (tech plan, numbers run, inventory, sound plan, here in production/lane/blueprint/), the checkers' findings (production/lane/checkers/), the story pick and each design proof run. Each change is one line in BLUEPRINT-CHANGELOG.md with its source; BLUEPRINT-STATUS.json holds the counts per group for the progress page. From 23 Nov the design proof checks this blueprint, and red teams 3 and 4 are given it, not the old description.

