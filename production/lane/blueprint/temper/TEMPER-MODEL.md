# The temper model

Written 24 Nov 2026 by the temper job, for blueprint part 2.14 (each person's temper) and its question Q6, which the owner has answered: every named person gets a temper of their own. Research behind each choice: RESEARCH.md. The check: temper_sim.py and temper_sim_output.txt. The values: tempers.json (the one home; data/people/ derives from it).

## 1. What a temper is for

A temper is the few fixed things about a person that make the same deed go differently with them there. The deterministic Core decides every outcome from it; language models only voice what the Core decided. Two rules from the research govern the size: every dial must drive decisions the player meets, and every dial must show on screen (Short, GDC 2017; the Nemesis cut-back; Dwarf Fortress's invisible facets; Watch Dogs: Legion's one-note people). A dial that drives nothing, or that nobody can see, is cut.

## 2. The decisions, and what drives them

From the 42 decisions in notes/DECISIONS-IN-THE-BLUEPRINT.md (rows numbered there), grouped by what drives them. "Regard" is goodwill to Frank (the Core's Loyalty), a state that moves in play, not a temper dial.

| Decisions | Driven by |
|---|---|
| Report a seen deed to the police; report as a victim; fetch the police at a body; sign a statement; testify; ring the night desk | law, seriousness, fear (nerve against Frank's menace), regard, own secret |
| Yield to a threat; face a drawn weapon; stand or fold in a fight; step in at a hold-up or beating; flee; come to look; pay a debt or resist; fold to a squeeze; hold a post; carry out a send; crack about a body | nerve, against menace and the odds; regard |
| Take a bribe; answer the money lever in talk; skim; leave for a rival's money; sell what they know; take a cut | greed, against the price and the deed's weight; law |
| Pass gossip on; to whom (ties only, or anyone met); how soon; volunteer things in talk; keep a thing quiet when asked | mouth, tie strength, the story's confidence; keepsQuiet |
| How far regard falls after a slight, a squeeze, a threat or a short payment; how fast it comes back; whether a threat backfires into telling; refusing again after being pushed; turning on Frank later | grudge |
| Join the crew; walk with Frank at night; take the firm; tell Frank a secret; warmth of greeting | regard, with nerve, greed and law as above |
| First reaction to a deed (Reaction.Decide: fetch the police, carry the news, flee, investigate) | law replaces dutiful (fetch the police at law over 0.55); mouth replaces willingness (carry the news at mouth over 0.4); nerve as now |
| How soon a witness sets off to tell, and where (Delivery.Begin) | nerve (runs under 0.35, as now); law picks the police station, mouth the nearest tie; the wait is 20 + 70 x (1 - mouth) game minutes |
| Pay protection or refuse; a driver leaving when frightened; the threat and respect levers in a favour; haggling over goods | nerve (refuse, stay, the threat lever's 0.2 + 0.7 x (1 - nerve) as in the Core); greed (what the shop or the buyer will bear); grudge (refusing after three squeezed weeks); respect stays on regard |

Not temper (set by knowledge, ties, the purse or authored scenes, and left as they are): going quiet when Frank walks up (tie), blackmail by a hook (the secret), borrowing after being emptied (the purse), stance and greeting rungs (suspicion and regard), what live talk says (memories and deed facts), naming and trusting him (knowing), officers' prices (authored).

## 3. The five dials

Each runs 0 to 1, authored in steps of 0.05. Rule for authoring: every person has at least one dial at 0.2 or under or 0.8 or over, because extremes are what the player can see; no two principals, firm or regulars share all five (the data check fails otherwise).

### nerve: how hard they are to frighten
- Grounded in: HEXACO Emotionality (fearfulness), its own factor, separate from honesty (Pletzer 2019); fear explains some silence, not most (Maynard 1994: 22% of unreported witness incidents).
- Low: folds to a word, runs from a weapon, pays at once, backs off. High: stands, calls a bluff, refuses, may step in.
- Decisions and shape: yields to a threat if nerve is under threat x (0.8 + 0.4 x menace), where a word is 0.5 and a shown weapon 0.8, and menace (0.3 at the start, up 0.1 for each seen violent deed of Frank's, at most 0.8) is what the town has seen him do. Folds to a squeeze if nerve is under 0.4 + 0.3 x menace - 0.1 x grudge, or regard is 0.6 or more. A debtor pays if regard is 0.5 or more or nerve is under 0.45 + 0.3 x menace; else begs or refuses (grudge decides). Fear lowers a report by 0.35 x menace x (1 - nerve). Already in the Core and kept: the weapon test (Arsenal: nerve against menace), coming to look (Notice: interest x (0.35 + 0.9 x nerve)), coming to look as now. Stepping in changes: the Core's nerve over 0.85 would let only 5 of 118 people ever step in, against the research (someone stepped in in 90.9% of 219 filmed public fights, more often with more people there; Philpot et al.), so a person steps in, unarmed, at a hold-up or a beating if nerve reaches 0.75 - 0.05 x (other bystanders, at most 4) and either law is 0.5 or more or they have a tie to the victim. At a body a threat is refused (the Core's rule, kept).
- On screen: stance and distance (backs to a wall, keeps three metres, or squares up), voice (the nervous line bank at nerve 0.35 or under, the steady one at 0.65 or over: the Core picks the nervous bank at nerve over 0.65 today, which the new meaning makes backwards, so it flips), and what they do: run, comply, freeze, refuse.
- Over the game: down 0.1 after seeing a killing (as the Core does now), down 0.05 each time they yield to Frank; back up 0.02 a game week towards where they started, never above it by more than 0.1.

### greed: how readily money moves them against what is right
- Grounded in: HEXACO Honesty-Humility, the strongest single trait predictor of wrongdoing (r = -0.48 with deviance; each standard deviation halves the odds of cheating); bribe-taking in the lab follows it, weakly.
- Low: cannot be paid, and an offer insults. High: names a price, takes the envelope, sells what he knows, skims.
- Decisions and shape: takes a bribe if greed + 0.15 x price (in weeks of their own money, at most 2) reaches 0.55 + 0.2 x law x (0.5 + the deed's weight); a refused bribe from someone with law 0.5 or more makes the report more likely, not less. The money lever in talk keeps its Core form, 0.25 + 0.55 x greed. A crewman leaves for a rival's money if his regard (in the check, his starting regard plus the 0.25 a need adds when he joins) is under 0.35 + 0.3 x greed. At a body a bribe is refused (the Core's rule, kept). A greedy crewman skims sooner (the Core's skim floor rises with greed).
- On screen: asks what is in it, looks at the envelope, haggles, the greedy line bank above 0.65; and the plain act of taking or refusing.
- Over the game: fixed. Canon's bought officers keep their authored prices (Ellis once at 800 then 100 a week, Wardell 200, Garton 50); greed decides only the bribe rule, never those scenes.

### mouth: how much and how widely they pass things on
- Grounded in: Extraversion predicts gossip, in every kind (Robbins and Karan); news spreads through a few well-connected talkers (Banerjee et al.).
- Low: tells only the people closest to them, if anyone. High: tells everyone met, strangers included, and tells it first.
- Decisions and shape: at a meeting a teller passes a story on if confidence x tie x (0.5 + 0.9 x mouth) reaches 0.2 (the Core's rule, with the trait added; at mouth 0.33 it equals today's 0.8); mouth 0.7 or more also tells people at the same place with no tie (tie counted 0.15); mouth 0.2 or under tells no tie under 0.5. A body always passes, whatever the mouth (as the Core does now). In live talk the band (close, ordinary, talker) goes to the voice so a talker volunteers and a close one waits to be asked.
- On screen: talkers stand in doorways and at counters with someone, start conversations, and their version of a deed reaches Frank first; close ones are seen alone and answer short.
- Over the game: fixed; after a seen deed everyone talks quieter for a game hour (the Core's rule).

### law: how readily they bring the police in
- Grounded in: the British reporting research (victims 70% against witnesses 29% on high-crime estates; seriousness and "the police could not do much" the main reasons; fear a small part), and the street's code against informing (Davey 2021; unverified for 1990). Duty and trust in the police are a working hypothesis here, not measured (no source read).
- Low: never the police; settles it, or tells the street only. High: walks to the phone box, signs a statement, rings the night desk.
- Decisions and shape: a witness reports if law + 0.05 + 0.6 x (seriousness - 0.5) - fear - 1.0 x (regard - 0.5, when above 0) reaches 0.5, with seriousness 0.3 for damage, 0.5 assault, 0.7 wounding or robbery, 1.0 a killing; a victim adds 0.25; keepsQuiet "owner" never reports Mickey's own. A person joins the crew on a need if regard + 0.25 + 0.2 x greed - 0.4 x law reaches 0.5 (the lawful refuse crime). The design's "never the police" people (rita_welburn, wayne_harrison, hal_metcalfe, the scrap dealer dennis_iveson, the customs officer douglas_fenwick, the old firm's man old_firm_man, the dock gun seller alf_garside) are law 0.15 or under, which replaces the old flag.
- On screen: looks to the phone box, mentions the police in a line, walks off towards the station; or spits the word, "I don't talk to them".
- Over the game: down 0.1 when their report came to nothing or they saw an officer bought; up 0.1 when Ellis acts on their word; never more than 0.2 from where they started.

### grudge: how long and how hard they hold a wrong
- Grounded in: Agreeableness as forgiveness against retaliation (Fehr et al. 2010, r = 0.22 with forgiveness; HEXACO's design), and the project's memory standards (MEM-09, TALK-05).
- Low: forgives, takes him back, a slight fades in days. High: forgets nobody, cites the old wrong, refuses again.
- Decisions and shape: every loss of regard is multiplied by 0.6 + 0.8 x grudge; regard comes back towards its start by 0.05 x (1 - grudge) a game week; a threat that fails backfires (tells the street "he threatened me") when grudge is 0.6 or more; a debtor who will not pay refuses rather than begs at grudge 0.5 or more; a crewman docked or beaten turns sooner.
- On screen: the greeting carries the old wrong ("You'll want paying for the window, will you"), refusals come with a reason, the cold shoulder lasts.
- Over the game: fixed; it is what governs how regard moves.

## 4. Beside the temper (state, not dials)

- regard: goodwill to Frank at the start (the Core's Loyalty, which nothing loaded until now): 0.3 for a stranger, higher for Mickey's people (Ron 0.7, Sheila 0.6, Pauline 0.6), 0.1 to 0.2 for rivals' men, 0.2 to 0.25 for officers. It moves in play; the temper decides how.
- keepsQuiet: whom they keep a thing quiet for when asked, the four words the Core reads: owner (Mickey's own: Ron, Sheila, the firm's Pauline, Kevin and Terry, the old firm's man; 2.5.2: they never go to the police about one of their own, though Kevin still tells the street and the Widow everything), friend (the default: only on first-name terms), anyone (keeps quiet for whoever asks, breakably: the trade that never talks), nobody (Brenda, Darren, Danny, the reporter, honest officers). The data's true/false is replaced.
- menace, own secret, sympathy for the victim: per deed or per pair, already in the Core's design; not temper.

## 5. The town's spread

From tempers.json (119 people, Frank included but never read by the Core for his own choices): the residents to come are drawn from the same spread by age and work, each with one dial at an extreme. Law sits low across the Hook (the docks' code), mouth high among shop counters, the laundry and the hairdresser, greed high among the fence's people, the porters and the bought, nerve high among the gate men (Stathers), the old dockers and the boxers (Sid Bulmer); the Widow's lesser men run from middling to low (Billany is mouthy until hit).

## 6. The four old dials: what survives

- nerve: survives, with one meaning (how hard to frighten); it was the only dial the Core read for the cast, and it now also governs folding and fear in reporting.
- dutiful: goes, split in two. Its meaning (duty to the law) becomes law; its other use in the data, as loyalty to Frank for 41 people, becomes regard, a state.
- willingness: goes. It was a per-deed answer (the Core's Willingness formula mixes nerve, regard, own secret, fear and sympathy), not a trait; its trait part splits into mouth (to the street) and law (to the police).
- keepsQuiet: goes as a dial; it is now the four-word stance the Core already expects.
- Also retired: venal (becomes greed, now read), talk (becomes mouth, now read), discretion (only ever 1 minus talk).
- New: grudge, because the design's memory and refusal rules (MEM-03, MEM-09, TALK-05) need a per-person size, and the cast's words ask for it (Grace "forgets nobody", Ron "carries things for years", Father Walsh forgives).

## 7. The check (temper_sim.py, a week of the town over the 118 townspeople)

Five deeds by Frank at real places and hours, witnesses taken from each person's routine, gossip hour by hour along ties.json; then the same seven asks put to everyone. Bands: from research where it gives one (marked R), else proposed here (P), since the design gives none.

| Measure | Band | Old, as the Core sees it | Old, as intended | New |
|---|---|---|---|---|
| Reports a seen wounding (everyone at menace 0.5) | 20 to 45% (P, anchored on R: witnesses 29%) | 75% | 58% | 41% (test week, all deeds: 15 of 63 witnesses, 24%) |
| Reports seen damage | 10 to 30% (R: vandalism 27%, mostly victims) | 75% | 58% | 14% |
| Reports a seen killing | 60 to 90% (P, from the project's withdrawn traits draft, 32 of 41) | 100% | 81% | 63% (test week: 1 of 5, the Widow's men at the dock gate) |
| Yields to a word | 15 to 45% (P, anchored on R: threats silenced about a quarter) | 86% | 86% | 42% (test week: 5 of 14 reporters asked, 36%) |
| Takes a week's money | 20 to 50% (P; lab dishonesty about 26%) | 100% | 89% | 37% |
| Joins the crew on a need | 20 to 50% (P) | 100% | 96% | 39% |
| A weekday deed known by Sunday | 30 to 70% of the town (P) | 38 to 45% | 38 to 45% | 35 to 41% |
| The Saturday dawn killing known by Sunday | (one day only; below the 30% floor) | 24% | 24% | 24% |
| Different behaviour patterns among 118 | as many as possible | 3 | 19 | 56 |
| Largest group behaving identically | small | 73 | 25 | 10 |

Two results sit outside their bands and are left so, named: the test-week killing (1 of 5 reported, because the witnesses at the dock gate at dawn were the Widow's men and the dock's code holds; the battery's 63% is the town as a whole), and the Saturday killing's spread (24% by Sunday, with one day to run; a body always passes, so it keeps spreading).

In the test week, under the new dials, the witnesses who would report a weekday deed were silenced by a word in 5 of 14 cases (a killing cannot be threatened or bought), and none could be bought even with two weeks' money; across the whole town 8 of the 48 who would report a wounding would take a week's money (Raine, Coult, Ackroyd, Agar, Askew, Rennison, Garton, Tasker), about 1 in 6. So honest reporters mostly cannot be paid, and Frank's other roads (regard, a favour, a secret, a tea with Ada) carry the weight, as MEM-11 asks. The old rules let one word silence almost everyone.

Side by side (the test the research names): at the same wounding, Ada reports, will not be frightened or paid and would never work for him; Darren keeps quiet, folds to a word, takes the money and joins; Grace reports and refuses everything; Rita keeps quiet, takes the money, joins and would leave for a rival's pay; Alan Sowerby reports but folds to a word.

## 8. What the Core must change (handover, for the builder; not done here)

1. Load each person's temper, regard and keepsQuiet from data/people/ into the Gossiper (nerve, greed and loyalty are read now; mouth, law and grudge are new fields).
2. PoliceFile.WouldReport: replace the fixed 0.4 and 0.575 with the law formula above; keep the killing and Mickey's-own rules.
3. Gossip.Bribe and Intimidate: the greed and nerve formulas above; a body still refuses both; a threat stops the report, never the street's talk (2.5.2; today Contain stops both).
4. Gossip.Tick: add mouth to the passing rule and the stranger rule.
5. Every regard change through one function that applies 0.6 + 0.8 x grudge, and a weekly recovery.
6. Debts, Empire squeeze, recruit and poach: the shapes above.
7. Reaction.Decide and Delivery.Begin: law in place of dutiful, mouth in place of willingness, as in section 2; then call them (nothing in the Core does today).
8. StreetVoice: the nervous line bank at nerve 0.35 or under (today over 0.65). Arsenal and Reaction: the stepping-in rule of section 3.
9. Port the simulation's rules as golden rows (PerceptionGolden) before any of it lands.

## 9. Open points

- The bands marked P are proposals; the owner may set others.
- Crew breaking still reads regard only; "past his nerve he talks" needs a pressure figure from 2.11.2.
- Rival men's regard for their own head is a tie, not temper, and has no data yet.
- The residents to come (200 to 300) take their tempers in the seeded pass; the rule is in cast.json.
- Facet-level evidence (dutifulness, greed avoidance) does not exist in the meta-analyses; the dials sit at factor level.
