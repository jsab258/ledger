# 07: Game design digest

Digest of the design documents in game-design/, made 18 November 2026 for the synthesis pack. Every item names its source as path plus section. Extracted only; nothing here is new design. Numbers are copied as written. Where a document marks itself LOG or NOT CURRENT, that status is given first.

## Contents

1. agency-model.md
2. open-city-spec.md
3. streets-and-cars-spec.md
4. street-spec.md
5. combat-design.md
6. combat-spec.md
7. weapons-spec.md
8. game-feel-spec.md
9. first-hour-2026-09-29.md
10. first-hour-on-paper-2026-09-29.md
11. first-moments-2026-09-29.md
12. ending-signs-2026-09-30.md
13. balance-findings-endings.md
14. balance-findings-economy.md
15. balance-findings-open.md
16. empire-roster.md
17. how-to-play.md
18. story-outline-2026-09-28.md
19. the-four-structural-defences.md
20. the-gap.md
21. side-stories-2026-11-08.md
22. authored-breadth-2026-11-13.md
23. police-asking-2026-09-29.md
24. rumour-reach-2026-09-23.md
25. The rest of game-design/, by title only
26. Contradictions between these documents

---

## 1. agency-model.md

Date: direction set 26 July 2026; benchmark re-scored 31 July; re-targeted 1 August; two sections added 2 November 2026. Status: SPEC. Where it differs from rulings, RULINGS.md wins (header note).

Purpose: what the game gives the player and how deep, benchmarked outside-in against shipped games (The framing).

Rules (The framing):
- Every non-social system exists to give the social system stakes.
- The grind test: a system asking for a decision occasionally is depth; one asking for maintenance on a timer is a chore. Every system needs a lazy path and an invested path; nothing may punish ignoring it.
- Conversation is never mandatory; a full loop must be playable with a few chip taps.

Benchmark (Benchmark section; LEDGER now, then target):
- Held, not raised: Social 93 (hold), Consequence persistence 95 (hold), Information 90 (hold); best-in-class 60, 85, 65.
- Time and opportunity cost 85 to 90; Economy 80 to 85; Faction politics 45 to 60 (lowered from 75); Operation planning 65 to 75; Law as a tool 40 to 70; Legacy and succession 40 to 45 (lowered from 70); Violence 45 to 70; Traversal and place 55 to 65; Class and access 60 to 65; Multiple solutions 65 to 80; Companionship 15 to 55; Public notoriety 40 to 60; Communication at distance 65 (target 60, past target); Constraint 45 to 55; Home that reacts 10 to 50; Family 15 to 50; Character competence 10 to 55 (raised from 40); Vice 5 to 40; Self-presentation 25 to 50 (raised from 35); Visible odds 0 to 50; Interiority 0 to 30; Vehicles 35 (40, late, superseded); Body needs 0 to 0; Crafting 0 to 0.
- Four rows added 1 August: Believable characters 10 to 75; Dialogue as writing 78 to 85 (judged 3 August against forty exchanges); Sense of place 50 to 70; Input feel 25 to 70.
- Competitor scores are authored judgement; the LEDGER column is measured.

The seven decisions (The seven decisions this encodes):
1. Deepest social simulation ever shipped.
2. Economy simulated end to end at district scale; every economic number legible as somebody's circumstance; squeeze, never micromanage.
3. Violence staged: consequence layer first, melee next, firearms last.
4. Traversal grows by breadth of place; cheap modes (Ferko's cab as fast travel, the ferry, a courier bicycle); "No drivable-vehicle physics, ever."
5. Operation planning a first-class loop: approach, people, hour, gear.
6. Access as soft keys: standing, notoriety, dress, introductions, an appointment brokered by Hal.
7. Phones exist (decided 26 July); gossip needs a phone channel; wiretaps become counterplay.

Outside-in additions approved 26 July (all eight): operation planning (75), multiple solutions (80, a project law: three or four keys per locked problem), companionship (55), home that reacts (50), character competence (40; options unlocked, never numbers), access as soft keys (65), visible odds (50; qualitative read, never percentages), interiority (30; pressure, not personality; intrusive lines, never stats).
- Competence decided: tracked per domain (collections, conversations, night work), unlocking approaches.
- Setting era decided: late-analog (landlines, payphones, answering machines).
- Vehicles superseded and built (26 July): a kinematic arcade car, no tyre model, damage, fuel or pursuit.
- Explicitly refused: lockpicking, alchemy, crafting minigames, gear treadmills, body-needs maintenance.
- Built 26 July night: Economy 65 to 80; Multiple solutions 35 to 60; Social 90 to 93; living city 36 people to 3,000. A missing row named: Interface, target 100.

Tom's rise (added 2 November; his ruling of 30 October):
- Tom rises in position, never in numbers.
- What the town calls him: the new owner, then Nowak, then Tom, then Tommy; the gate is knowing, not liking; Sheila the one exception.
- His power grows through crew, weapons and reputation; he does not get better at fighting.
- He sees his own position, never other minds; no reputation numbers; no stats; difficulty only as assists (D33, D34, D11).
- Ruled out (inferred there): experience points, levels, skill or perk trees, stat bars, reputation meters.

Study 17 design inputs (added 2 November), items as his: 1, the Hook plus the docks can carry 15 to 20 hours; 2, an hour budget by activity; 3, about 25 to 40 side stories found on foot, no markers; 4, far more named residents than the 30 regulars, each with a routine and one secret, routines with occupancy limits; 5, never force waiting, appointments with a window; 6, a legitimate docks job as an early daily loop with a small daily competition (no stake, inferred); 8, empire as a management game on the street (within D24); 9, density up and back, not out.

Open: items 6 and 8 against July's refused minigames and grind test; July's end-to-end economy against canon D24 (not an economy simulation); whether per-domain character competence survives the 30 October ruling (Tom's rise).

## 2. open-city-spec.md

Date: drafted 26 July 2026; approved with amendments 26 July. Status: SPEC.

Purpose: put the open game in one place: the week as on-ramp, Empire v1, the generation pipeline, the roadmap position (header).

Rules:
- Week mode, days 1 to 7: win or lose verdict, outfit patience, survival framing; the tutorial arc (section 1).
- Open mode, day 8 on: no verdict screen, no win state; exposure fuse and heat remain; two ledgers, empire standing and life standing, no ceiling (section 1).
- Act II and later fire on world state, not days; no timers (section 1).
- Empire v1, four firsts in the Hook (section 2): first business (buy clean, buy the debt, or lean on a secret; first candidate the pawnbroker); first recruit (supply the need: slow, sticky; spend a hook: fast, brittle; crew fields loyalty, fear, competence, breaking point); first racket (the drop inverted; a collection route; no countdowns); one reacting rival, the Dockside syndicate's street operation, driven only by what its people observe; ladder warning visit, prices raised, recruit poached, a violence threat; flat structure (Nemesis patent note).
- Generation (section 3): district template to place graph; every business a card; art skins, generation decides; scale path one street, then the Hook (about 8 to 12 blocks, 60 to 100 Tier-2), then Copper Row, then the seven districts.
- Roadmap (section 4): M6 becomes The Open City; a day-8 teaser in the slice where Lena lays out what the street could be.

Decisions, 26 July (section 5): 1, Empire v1 broader than the four firsts (multiple businesses and racket types; protection and fencing next); still excluded: districts beyond the Hook, the other two rival organisations, combat, vehicles. 2, day-8 teaser yes. 3, district generation with Empire v1. 4, open-mode fail state survivable but scarring: prison time, empire decay, reputation ruin; no game-over screen.

## 3. streets-and-cars-spec.md

Date: player decision 26 July 2026. Status: SPEC (M12).

Purpose: a real street grid and traffic, because "city can't feel real or immersive without cars and real streets" (header quote).

Rules and numbers (The design):
- Diagnosis: two roads, the founding cross at x=0 and z=0; twenty-two locations in open ground (What is actually wrong today).
- Grid: N-S avenues at x = -30, -16, 0, 16, 30; E-W at z = -18, -8, 0, 10, 18; twenty-five junctions, sixteen blocks; each of 24 places joined to its avenue by a lane.
- Road classes: avenue 8 m, street 6 m, lane 4 m.
- StreetMap is data in Core; hard tested property: every place reachable from every other.
- Cars arcade: traffic on avenues stopping for the player; a driveable car (get in, drive, get out; no gears, damage or handbrake); a car is a thing witnesses describe; the coat does not hide a vehicle.
- Out of scope: pedestrian collision, running people over, ownership, chases, police pursuit, damage, fuel, parking.
- Build order: StreetMap, road geometry, walkers on the network, traffic, the car, witnesses describe the car; cut from the bottom up.
- Melee deferred until the art pass (Melee).

## 4. street-spec.md

Date: drafted 16 August 2026, unbuilt. Status: SPEC.

Purpose: derive street dimensions from building typology before the topology re-plan; the current map measured at about 110 parcels citywide (header).

Numbers:
- Typology (section 1): terrace house frontage 4.5 to 7 m, depth 4.5 to 6 m; shop with flats 5.5 to 9 by 7 to 9 m; pub or corner premises 8 to 11 by 8 to 10 m; warehouse 12 to 30 by 10 to 16 m; villa 8 to 11 by 8 to 10 m (Fairview only); yard between rows 4 to 6 m.
- Blocks (section 2): rectangles; depth 16 to 19 m buildable, about 21 to 24 m face to face; length 5 to 10 parcels, 35 to 70 m; Copper Row 35 to 45 m; Fairview and Gullwing 55 to 70 m; Ironside plots 30 to 40 by 25 to 30 m.
- Streets (section 3): high street 9 to 10 m carriageway, 3 m pavements; terrace street 6.5 to 7.5 m, 2 m pavements; service lane 3 to 4 m, no pavements; esplanade 7 m plus 6 m promenade. Pitch about 45 to 80 m along, 28 to 34 m across; 2 to 4 times today's on the long axis.
- Junctions (section 4): lights only where avenue crosses avenue near a core; give-way elsewhere; zebras and belisha beacons placed by footfall rule; corner radii 1 to 2 m on terrace streets; no one-ways in v1.
- Parking (section 5): single yellows on core commercial edges; half-on-kerb under 7 m; never across a zebra, junction mouth or doorway.
- Migration (section 6): each of 61 places keeps street name and relative position; founding Hook node ids kept; the bar does not move.
- Gates (section 7): predicted terraceParcels at least 400; an unbroken terrace run of at least 8 frontages in one view; sim green two consecutive runs.

## 5. combat-design.md

Date: Jafar's doc "LEDGER Combat: Final State", 12 October 2026 (revision 12), imported 21 October; "Since 12 October" added 2 November. Replaces combat-spec.md.

Purpose: combat as a ladder of escalation the street watches: "good to do, costly to have done" (opening).

Rulings it rests on (The rulings it rests on): 12 Oct: good to do and costly; power is people; AAA feel (changes D24 for fighting only); guns in the final game, rare, after melee; Tom cannot die. 3 Oct: a threat can stop a police report, never the street's talk. 23 Sep: fists and improvised weapons, firearms rare, crew act on orders, no jump. 21 Sep: three gaps in order: outnumbered, running away, police arriving mid-fight. 14 Sep: not a shooter. 10 Sep: blood and light gore; no torture, no cruelty as spectacle; killing possible, rare, permanent. 31 Aug: melee, then improvised, then scarce firearms; one gunshot a town-wide event. 28 Jul: violence a legitimate tool; no health bar now.

The ladder (eight rungs): 1 Stare; 2 Square up; 3 Threaten (can stop a police report, never talk); 4 Shove or grab (talked about, rarely reported); 5 Strike (most who see it report it); 6 Weapon out (a gun out is news across town); 7 Weapon used (police interest, hospital, traceable weapon); 8 Kill (police from procedure upwards).
- Most confrontations end on rungs 1 to 4. Finishing a downed man is a decision in the quiet afterwards, never in the flow.

How a fight feels: weight (hit-pause, camera jolt, sound, no numbers); every blow has a readable wind-up; a skilled player wins most fair one-on-ones; mashing tires and loses; no lock-on, combat music or arena; no health bar (minimal HUD as a settings switch); accessibility: longer wind-up window and auto-resolve. Study 14 to set timings.

Odds: a fair one-on-one roughly even; two against one deadly; three a beating; the crew changes the odds; ordering a named man hurt makes the sent man a second person who knows; crew who watch remember (loyalty and fear); townspeople fight each other too.

The street as a weapon: walls, doorways, shop windows, railings, car bonnets, stairs, the quay edge; brick, chair, snooker cue, wheel brace, cargo hook, ashtray, pipe, dustbin lid; no bottles or glasses; moves against surfaces are paired animations.

Weapons, four tiers: fists; improvised (left behind, can be found); carried (cosh, knuckleduster, utility knife, flick knife, bat; can be found in a search, has a history); firearms, rare (sawn-off shotgun, old revolver; armed police only when a gun is involved). Every make fictional.

How fights end: someone backs off; someone runs (a foot chase through alleys, yards, doorways); someone goes down (leave, rob or finish); police arrive mid-fight (running from them a new offence; custody and court); people step in. Tom cannot die: he wakes in hospital or on the pavement.

Aftermath (carried from Core): injuries last and scar (Core/Harm.cs); treatment costs and plants a witness; blood stays until washed; weapons have a history; feuds; a body moves police from procedure to investigation to manhunt; killing the only witness takes a manhunt to an investigation, never further (Core/Homicide.cs); watching crew get a permanent loyalty ceiling.

Build order (How it gets built): research; Study 14 numbers; animation source test (one wind-up, strike, hit reaction, shove into a wall; two routes then set aside); first test after the walk passes; lower rungs; the three gaps; street as weapon; firearms last.

Since 12 October (added 2 November):
- Fists knock out and never kill on their own; a fall against a kerb, wall or step after a blow can kill, rarely, and the town treats it as a killing (ruling of 30 October). KCD2's quest knock-out lasts 10 s, taken only once checked to fit.
- Fight camera widens so the other man's feet and watchers are seen (camera pick of 28 October); first target, inferred: both men's feet and a ring of about 3 m; contact close-in of about 0.8 s.
- Not Yakuza's frequent random fights; kerbs added to places; bins, crates, signs, bicycles to things at hand; Yakuza finishers not taken.
- Open: whether the fall applies to fights Tom is not in; whether a shove can kill; how rare; whether the quay edge counts; whether a downed man can be finished with fists.

## 6. combat-spec.md

Date: phases 1, 2 and 3b built 28 July 2026. Status: REPLACED by combat-design.md (12 October); kept as the record of what the Core built.

Purpose: combat as the last missing verb to a consequence system already built (section 0).

Rules as written in July:
- Not a win condition; not empowering ("Tom Novak runs a bar. He is not a fighter"); not frequent (a handful of fights in a playthrough); not free; not a separate mode (section 2).
- Verbs (section 3): square up, strike, shove, guard, back off; finishing separate; guns out of scope.
- UI (section 4): no health bar, damage numbers or hit markers; condition on the body; telegraph not tell; sound carries it; accessibility: longer telegraph and auto-resolve.
- HomicideBook.Pressure (section 6, phase 3b): bodies 0.4 each; strongest naming witness up to 0.6; each further witness 0.25. One body unseen 0.40 Procedure; one witness through a wall 0.76 Investigation; one watching witness 1.00 Manhunt; two bodies no witness 0.80 Investigation; three bodies 1.20 Manhunt.
- Rumor.Indelible: Age, Discredit, Bribe, Intimidate, leash and suppression all step over a body; Manhunt removes the Quiet ending; Investigation forces Act III open; 39 checks, 16 breaks confirmed red.
- Violence lab (phase 4): leave-it lead 0.28; bribe 0.18 at $414; intimidate 0.23; kill-one 0.91 Manhunt, quiet 13%; kill-all 1.00, quiet 0%. Below 0.50 a case is answerable.
- Exchange retune: first run mash won 76% (a clean strike did 0.86 against a floor of 1.0). Retuned floor 1.0 to 2.8, strike cost 0.22 to 0.34, recovery 0.18 to 0.09, guard absorption 0.35 to 0.22. Then: mash 15% win, 67% down, 100% gassed; guard-then-hit 0% win; patient 26% win, 46% down, hurt 2.39; shove-and-go and back-off take nothing.
- Decisions 28 July (section 7): diegetic readout, maybe minimal HUD later; both may swing first; lethality yes, rarely, permanently; guns out of scope; auto-resolve yes.
- Risk (section 8): combat the easiest way to ruin the game.

## 7. weapons-spec.md

Date: v1 to v3 29 July 2026; v4 audit 29 July; v5 corrections; header of 18 November 2026. Status: SPEC v5, APPROVED, BUILDING (M16).

Purpose: perception, weapons and violence; "LEDGER is a crime game in a city that perceives, reacts and remembers" (section 1), replacing "the antagonist is gossip".

18 November decisions (header, advisor 226): combat's end state is option A: fists and improvised weapons every day, guns rare and heavily consequential, AAA in feel, melee first. An escalation dial once guns exist: if the player arms his crew or buys from the docks, guns spread, rivals arm, police bring armed cars, the town remembers who brought them. The suppressed .22 is dropped; every line naming it is void.

Perception (section 3): vision by cone, range, occlusion, light, motion, time in cone; output a confidence of being seen and separately of identification. Hearing by sound events; radius from loudness minus ambient at the listener; occluded by walls; scales with alert state; gives direction and distance, not identity. Before any weapon: people notice loitering, running at night, a lamp versus a doorway; quiet and loud hours.

Observation (section 4):
- Seven slots: precursor, draw, act, victim, actor, flight, aftermath. Six named observations emerge: full, act no actor, actor no act, sound only, aftermath, flight.
- Identification rungs: 0 someone; 1 silhouette; 2 a distinguishing mark (limp, scar, coat); 3 a face, a stranger; 4 recognition. Not monotonic: a stranger tops out at 3; an acquaintance reaches 4 directly. "The dangerous witness is not the closest one, it is the one who knows you."
- Certainty and willingness separate; willingness from nerve, loyalty, debts, fear, and what the witness was doing there.
- Mutual awareness, four states; the standoff is the bottom-right cell.
- Delivery window: the witness picks a destination, walks it, then the fact enters the mill; the player can follow, talk, pay, threaten, help or kill.
- Witnesses can be wrong: wrongly accused, let a false belief stand, plant an impression.
- Five testable claims (4.7), including interception before delivery leaving no trace.

Weapons (section 5):
- Brandish is a verb: comply, freeze, flee screaming, call the bluff, escalate; one-way: you can never un-draw.
- Seven families, about sixteen carried objects: Hands (fists, brass knuckles); Blunt (cosh, bottle, bar or tyre iron or pipe, baseball bat); Edged (switchblade, kitchen knife, ice pick, straight razor); Ligature (wire, cord or belt or scarf); Firearms, Phase 5 (.22 target pistol, .38 snub revolver that leaves no casing, .45 automatic that throws brass, suppressed .22 dropped, sawn-off shotgun); Environment (stairs, railings, a window, the dock, a road and a moving car, fire, water, machinery, "a bad drink and a long walk home"); Kit (gloves, a second coat, a bag, a car, a torch, "a bottle of something", keys).
- Accidents: "the only violence in this game that produces no crime"; three constraints: need position and privacy; being seen doing it is the worst observation; a suspicious death still gets a coroner (an inquest); two accidents round one man is a pattern.
- Thirteen axes per object (noise, masking, reach 0.8 m to 20 m and more, time to ready, abort, victim cries out, against a ready man, leaves a body, scene trace, trace on you, carrying, provenance, how it fails). Ready times: cosh about 1 s; ice pick about 1 s; wire about 2 s, both hands, cannot abort; .38 and .45 about 1.5 s.
- What stays out: damage numbers, health bars, durability, crafting, upgrades; no rifles, no automatic weapons; tops out at a sawn-off.

Legibility (section 6): three questions: am I visible, how far did that carry, who noticed. Recommended hybrid: the frame breathes (vignette opens and cools when lit); one noise ring at the true radius; attention by four redundant channels led by audio (the street goes quiet, barks, behaviour break, one music stem); an optional accessibility eye, off by default. Test: sound off and picture off passes. The ghost restricted (v4): shown only when awareness was mutual. The standoff: audio ducks about 0.4 s and the vignette tightens, once per event. Feel: the draw is the most important animation; one optional forgiveness slow, off by default.

Carry and acquisition (section 7): concealment not weight: two objects, three if one is small; chosen at the door; one screen, the coat. Four routes, all social: bought from a person, stolen (owner notices), taken, found exactly once (Mickey's, authored). No random world loot. Provenance permanent; disposal witnessable.

Reaction (section 8): notice, investigate, alarm, flee, deliver, fetch the law, intervene; bodies found by whoever passes next.

Phasing (section 10) and cost (section 18): 1 perception with non-crime reactions, about 3 days (behaviour gate: loitering under a lamp thirty seconds draws a look and a remark; running at night turns heads; a 3 am door slam brings someone to a window); 1b legibility about 1.5 days; 2 observation and reaction about 3.5; 3 melee, carry, blood, frisk about 3.5; 4 murder weapon, acquisition, accidents about 3; 5 firearms about 1.5; about 16 days in all.

Rules added in v4 and v5 (section 15):
- Symmetry: "if you can tell he is facing you, and you are in light, he can see you"; silhouette gate at 8, 18 and 35 m; if front and back are not distinguishable at 18 m the rule fails; fallback the survey verb.
- Arrest, no chase: a constable with a full or actor observation closes and takes you; running works only through the systems (not identified, busy street); resisting allowed and the worst outcome, no warning.
- The victim perceives: being attacked guarantees rung 3, usually 4; the survivor is the worst witness.
- Blood: on the actor for edged, ligature with struggle and improvised; never for firearms, cosh or accident; rung-2 evidence; persists until washed or the coat changed. "One violent minute should cost three in-game days."
- The frisk: constable, doorman, the outfits, Ellis as conversation; never at random; refusing is an answer; found is worse than used.
- Memory hardens: accuracy falls, confidence rises; hardening never confers indelibility.

Calibration (section 16):
- Vision: cone 120 degrees; acuity band inner 60; detection 40 m in daylight; rung 1 at most 35 m; rung 2 18 m; rung 3 8 m; rung 4 25 m; light multiplier day 1.0, lamp 0.7, unlit street 0.25, doorway 0.12; notice 0.35 s; identification 1.2 s; motion running 2.0, walking 1.0, still 0.5.
- Hearing: r = 1.5 m times 2 to the power (L minus A) over 8, capped at 250 m; inaudible when L is at or below A. Ambient: residential 3 am 15; daytime street 45; market at noon 58; the bar busy 68; heavy rain plus 12. Loudness: walking footstep 25; running 38; door slam 55; shout 65; bottle smashing 70; .38 snub 100. Worked: footstep at 3 am 3.6 m; footstep by day nothing; .38 by day 177 m; shout in the market 2.2 m. Alert lowers the floor by up to 8.
- Time: delivery walk 2 to 9 minutes; unsure witness waits 20 to 90 minutes; body in an alley at 3 am hours, in the market under a minute; memory hardening rung plus 1 per about 4 retellings, confidence plus 0.1 per retelling.
- Performance (17.1): only the Near band perceives; vision at about 6 Hz staggered; hearing event-driven; budget 1.2 ms per frame at 60 fps with a gate. Persistence (17.2): observation records, in-flight deliveries, awareness pairs, carried objects, provenance, blood, alert states.

Lab (section 18): RunPerceptionLab asks the slot-set distribution (if 80% are full, too generous), how often accidents and brandishing end it, a week after one killing by weapon, whether the survivor dominates.

Open: the F1 frame-rate number and the voice listening pass asked of Jafar (section 13); perception computed only for events the player is party to (assumption 1).

## 8. game-feel-spec.md

Date: 28 July 2026; camera section added 2 November. Status: SPEC.

Purpose: a full taxonomy of game feel benchmarked against KCD2 and GTA5 (header).

Rules and numbers:
- Input (section 1): a key pressed 100 ms early still registers; prompts stay valid a beat out of range; a locked 60 over an unlocked 90.
- Locomotion (section 2): momentum, turn radius, gait states including injured, tired, carrying; decided 28 July: code-driven movement, not root motion; head bob off by default.
- Camera (section 3): spring arm, speed FOV, look-ahead, collision, focus pulls. By situation (ruling of 28 October): street camera at the Between height, an 86-degree lens, pulled back to 3.1 m; closer for talk and low rooms; wider for fights; rows in production/specs/camera.json (street, talk, run, room); fights next.
- Audio (section 4): footsteps by surface times gait times 4 to 6 variants; occlusion for speech only (general occlusion outstanding); distance filtering on speech.
- World (section 5): doors with mass; objects react; puddles splash, not every step; NPCs react to bumps.
- Interaction grammar (section 6): anticipation, action, consequence, recovery.
- Feedback (section 9): every action gets a response within 100 ms; never two channels for one event.
- Menus (build order item 5): in 120 ms, out 200 ms.
- Feel.cs covered by 44 checks; eight deliberate regressions caught (section 0).
- Expectation: this reaches competent indie, not KCD2.

## 9. first-hour-2026-09-29.md

Date: 29 September 2026; approved by Jafar on the 29 September town page as the plan for the first session (approval file beside it).

Purpose: the first hour on paper, under two pages (opening).

Four steps (What the first hour has to do): he moves; he is seen; it is written down; it comes back, said to his face by somebody who was not there. The Meridian Test: the world visibly knows him at least once in the first thirty minutes.
- Measured: among forty named people a plainly seen night reaches a second person in about six real minutes (slowest tenth nineteen); in the coat, reaches anyone within a week about six times in ten. With the five he meets (Sheila, Ron, Darren, Ada, June) one says it to his face by minute thirty in 13 of 13 cases, 7 only at minute thirty; in the coat 6 of 13.

Clock (The clock): the new game has not set its clock; times assume two game minutes a real second and a nine o'clock start.

The hour, minute by minute (The hour):
- Minutes 0 to 7, day 1: Tom arrives with one suitcase and the letter after the funeral he missed. Sheila Dunn meets him at Mickey's, shows him round, stops at the one door she does not open. The game says once that the town answers in words written by an AI model and a line can be reported. Ron Kirby at the rank calls him boss; Darren Milner friendly and owing; Ada at her window; June, Mickey's daughter, wants nothing from the office. Strangers call him the new owner; people he has met use his name.
- Minutes 7 to 11, night one: the outfit's first ask, a small job and a coat that makes him harder to recognise. Refusing ends Mickey's arrangement and does not fail the game.
- Minutes 12 to 24, day 2, it comes back: the night is a story either way. If seen, it reaches a second person within minutes ("Funny hours you keep"); if unseen or refused, the outfit's talk comes back ("Heard you told them no"). His Ledger shows what he believes the street knows.
- Minutes 24 to 36, day 3: Ada's tea on the evening of the outfit's second ask, the week's first test of which life he keeps; Alison Sedman asks about the warehouse fire.
- Minutes 36 to 60, days 4 and 5: if the street is loud, DS Carol Ellis on Quay Street.
- The week ends on day 7, a little under half an hour later: Sheila, over the real book, "So which is it going to be?"

Teaching: every hint fires the first time it can mean something, never on the clock. Not in the first hour: the three rivals beyond a name, Act II, any ending, money beyond takings and the first envelope; the old day-5 scene with Ron (breaks the content rule).

Open for Jafar: whether the Ledger's belief is built from what Tom has seen and heard; whether Sheila keeping him at "new management" is the exception to names following knowing.

## 10. first-hour-on-paper-2026-09-29.md

Date: 29 September 2026.

Purpose: the approved hour run through the simulation for each of Tom's choices (TownReach --first-hour); two game minutes a real second, nine on day 1 to minute sixty.

Findings (the table):
- Asks every other night from night one while the arrangement stands.
- In every row the night is first said to his face at minute 13, by Darren: "Heard you did Mickey's run", "Heard you told them no", or "Heard they waited on you at the landing."
- Takes it every night: arrangement stands, three nights done; Ellis on day 5, minute 48. Takes it once: stands, patience low; no Ellis. Tells Ron no: ended the first night; no Ellis. Stays away: ended after three nights away; no Ellis.
- Ada warmer if he sits with her, cooler if he stands her up; Ada's tea decides how she thinks of him, not whether she talks.
- What brings Ellis is Ada's window: her telling puts it round ten people by day 5. The outfit's own talk never gets past Darren.
- Left out: passing each of the five once an hour; no other sight on the way to the landing; Alison's question; the clock.

## 11. first-moments-2026-09-29.md

Date: 29 September 2026, for Jafar's approval.

Purpose: the hints, each the first time it matters (checklist A04.07). The old game's four hints came at 1, 5, 30 and 90 seconds.

The six moments:
1. Not moved after four seconds: "{Move} walks, {Run} runs. People on this street notice who's about."
2. Free to talk, after the AI notice: Sheila, "That's Ron on the rank. Go and say hello..."; plain, "Walk up to anyone and press {Talk}. What you tell them, they remember." Plain line alone until Sheila's take passes the accent gate.
3. Ron hands over the coat and envelope: "If you go tonight, boss, wear that. In the dark nobody looks twice at a coat."; plain line on {Coat}.
4. Somebody saw: "Somebody saw that. What they make of it can go round."
5. A remark overheard: "That was about you. {Ledger} shows what you believe the street knows."
6. The Ledger opened: "What you believe the street now knows about you."

Rules: each once a game, saved; walking first; never two within twelve real seconds; hints 4 and 5 dropped after fifteen seconds waiting; the talk hint waits up to forty-five; the Core decides moments, the game shows them.

## 12. ending-signs-2026-09-30.md

Date: 30 September 2026. Code waits on Jafar's scope call.

Purpose: make every cost that decides the ending readable before it decides, as Tom's own reading, never a number or another mind (D58, D33).

Where it stands: endings decided in the Core (ActThree.Eligible, order Quiet, Both, StraightLife, Kingdom, else BurnBoth); the Unreal game has no endings yet; the evening's books word and the status bar's "The street:" are meters and not to be ported.

The seven factors:
1. Books as inspection sees them: decides Kingdom and Both; line 0.62; sign the inspector's manner ("I'll want the other book, Mr Nowak").
2. Books as they are: decides Both; line 0.62; sign Sheila, once each way, whatever her loyalty (today her bands fall at 0.45 and 0.7).
3. Keeping Mickey's business: decides Kingdom, Both, StraightLife; his own act.
4. A friend who would stand by him: decides Both and StraightLife; known from 0.45 (calls him Tom), warm, would stand by him at 0.55; sign an act asked of nobody; today's warning at 0.6 moves to 0.55.
5. The street's talk: decides Both; line 0.5; sign an overheard telling said as fact, a remark that stops as he passes.
6. Ellis's case: decides Both, bears on Kingdom; line 0.5 or deflected; she asks while answerable, tells once not ("We both know where you were").
7. The police: decides Quiet; nothing, asking round, investigating, manhunt; a killing with a sure witness passes through investigating for at least a day; today it jumps unseen (his call).
- Successor: ready, then not; says "I can't take it on now" if readiness lapses.
- Tom's reading says "quiet" only when every factor is quiet.

Checks: each sign and Eligible() call one state function; the lab sweep; the AI tester asked "how does this week end, and why?".

## 13. balance-findings-endings.md

Date: 27 July 2026. Status: LOG, NOT CURRENT.

Purpose: the first measurement of the ending distribution (400 worlds per row, 21-day campaigns).

Findings:
- StraightLife required EmpireDissolved; fixed to "no empire".
- Both fired 51 to 58%; fixed by also requiring the raw books to hold; now 13% (14.8% in the table), careful campaigns only.
- A hole: Kingdom no longer requires the life to be gone.
- Decision 10: cooperation relief halved, 0.09 to 0.045.

The matrix (Both, Kingdom, Straight, Burn, seen strain):
- Control, all four inspector treatments: 0, 0, 49.8, 50.3; strain 0.64 ignored, 0.50 answered, 0.84 stonewalled, 0.35 answered and deflected.
- Aggressive: ignored, answered, stonewalled all 100% Burn (strain 1.00, 0.77, 1.00); answered and deflected 100% Kingdom (0.54).
- Cautious: ignored 21.5 Kingdom, 78.5 Burn (0.79); answered 47.8 Kingdom, 52.3 Burn (0.61); stonewalled 3.3, 96.8 (0.94); answered and deflected 14.8 Both, 85.3 Kingdom (0.43).
- Quiet absent by construction.

Open: the inspector is inert for a player with no empire; options: let the audit reach the life, give the straight player something to protect, or say "there is nothing here to find"; recommendation: play it first.

## 14. balance-findings-economy.md

Date: 28 July 2026 (M13 section 27 July). Status: LOG, NOT CURRENT.

Purpose: the living economy measured (300 open-city campaigns per plan, 21 days).

Numbers:
- Control: end $2279, falls 0.07, street 0.48, prices 1.00. Aggressive: $2185, falls 0.62, street 0.22, prices 1.21. Cautious: $1866, 0.15, 0.39, 1.07. Broke 0% throughout; supplier lost 0%.
- Aggressive earns $1697 in rackets over three weeks and ends $94 behind control. Street 0.55 is ordinary; takings floor 0.35 never reached; zero bankruptcies in 900 campaigns.
- Neglect loses a supplier; paying on time buys 0.28 a week against the worst drift of 0.245 a week ("he asks $118 for it now").
- M13 purses (400 weeks): collector $1642, 60 collected; warm-collect $1762, 180 collected, 2 visits; with purses 3 visits and 1 part-payment, same money. Sam's loyalty 0.3; Rocco's $60; Sam pays $45 against a $120 marker.
- Not covered: a squeezed street's effect on purses.

## 15. balance-findings-open.md

Date: 26 July 2026. Status: LOG, NOT CURRENT.

Purpose: Monte Carlo of the open city (300 seeded 21-day campaigns per plan).

Numbers:
- Control: reached open 99.7%, end $2825, falls 0.06, rival stage 0.0. Aggressive (debt and squeeze, 2 crew, 2 rounds): $3138, falls 0.61, rival 3.7, racket $1708. Cautious (clean buy, 1 crew, 1 round): $2512, 0.12, rival 1.0, racket $469. Broke 0%; cut off 0%.
- Stage-2 rival tax $40 a day; aggression plus $313 (11%) for ten times the Falls.
- Knobs: racket income 60/80 to 80/100; stage-2 threshold 0.5 to 0.6.
- The $900 clean purchase not repaid by day 21 (plus $480).
- Decision: no tuning shipped.

## 16. empire-roster.md

Date: as built 26 July 2026. Status: SPEC.

Purpose: the Empire v1 roster, all data (EmpireSetup.cs and Tier2Batch).

Businesses:
- The pawnshop, Victor (nerve 0.4): clean $900, his marker $250 then squeeze, or his skim (weak hook); +$60 a day clean, washes $80.
- The market stall, Marla: clean $500 or her thumb on the scale (Sam knows); +$40 a day, washes $30.
- Round 2 to 3: Magda's teahouse $600, +$45, washes $40; Donna's bakery $550 or her $150 marker, +$45, washes $25.
- Next candidates: the teahouse (magda), steam laundry, corner bakery (danica), boarding house.

Rackets:
- Collection round $60 a day dirty, base risk 0.35. Protection round $80, risk 0.5. Fencing line $100, risk 0.4, needs the pawnshop.
- Rotten hook-crew (loyalty under 0.3) skim a quarter, visibly.
- The cut: fair; generous (minus $15 a day, plus loyalty); skim (plus $15, minus loyalty, remembered).

Recruitables: Sam $120 (cash, counted twice); Joey $100 (a Downtown reference for his daughter); Marla $150 (lean on her supplier); Victor $200 (a slice of his gambling marker cleared); any batch resident $120 default. Core cast (Lena, Ada, Rocco, Noor) not recruitable.

The rival: Dockside street arm, flat; attention only from observable moves; ladder slow beer (0.25), $40 a day street rent (0.5), poach the least loyal (0.75; loyal crew warn instead), the wordless threat (0.9).

Further rules:
- The break: skipping drops while rackets pay is declared independence (plus 0.25 rival attention).
- Ellis stands down 4 days after a Fall.
- The quit: a need-route crew member skimmed below loyalty 0.2 walks; hook-crew cannot leave.
- The day job: Meridian Parcel courier rounds, $40 clean a morning; Zlata dispatcher.
- Population: 22 walking, then about 36; 45 more cards ready.

Faction agency: Dockside syndicate, head Sera Kest (Joey, Ferko); the machine, Aldous Vane (Tibor); the New crew, Danny Ro (Rita). Poaching costs the arm 0.35 standing and adds 0.2 attention. PledgeTo needs standing at least 0.2; $50 a day tribute. BreakWith ends below zero standing.

Still unbuilt: arm against arm, absorbing a broken arm, the heads' Table scenes, Hal's brokerage verbs.

## 17. how-to-play.md

Date: verified 4 August 2026. Status: LIVE, player-facing for the prototype build.

Purpose: instructions for the prototype.

Premise as written: Tom inherited Mickey's pub on Hook Street and the criminal arrangement.

Controls: WASD and Shift move and run; E talk (type anything; chips optional); F car; L the ledger; J the plan; T the phone (costs distance in time, not secrecy); C the runner's coat; F1 debug brain; F2 API key; F5 save, autosave every morning; Esc.

Rules:
- Typed intent: words that match a possible action do it; unanticipated actions are weighed against money, standing, crew, hour and watchers.
- Streets: ten named streets, sixteen blocks; lights at four big crossings; you cannot run people over; a car is described whether or not the coat is on.
- The week: the bar earns clean money taxed by heat; at 22:00 the outfit posts a drop, found before 02:00 for dirty pay; the till washes $120 a day; two mornings in a row of a hostile street ends you, as does exhausting the outfit's patience; day 7, Lena asks what you intend; SPACE opens the city.
- Open city: nothing ends, things scar; exposed, three days inside, unexplained cash kept; Meridian Parcel board until noon, $40 clean, one round a day.
- Empire verbs: buy a front clean, buy the debt, or spend a secret; crew by need or by leverage; rackets with a cut; the Dockside arm (slow beer, rent, offers); the machine reads the deed registry; the New crew answers with noise; poaching noticed.
- Perception: the symmetry rule; light decides how far; how well somebody knows you decides naming; a 3 am footstep carries about three metres and at noon nothing; a ring shows how far.

## 18. story-outline-2026-09-28.md

Date: 28 September 2026; approved by Jafar 28 September with the spine as canon's baseline (approval file).

Purpose: the story in outline, under two pages.

Spine: "A stranger inherits a position, not a business." Tom Nowak arrives with a suitcase and a letter; Mickey dead three weeks; Mickey's is a cab office on Quay Street in the Hook, with a half-dead outfit and a book of debts. The name ladder: the new owner, Nowak, Tom, Tommy. Three questions: what did you inherit; how big can it get before your two lives touch; which life was real. Underneath, never explained: the dock labour scheme ended July 1989 and more than half the registered dockers' jobs went. Register: British noir, class not greed.

Arrival: after the missed funeral; June still in town; Sheila Dunn shows him round, promised Mickey to size him up; Ron Kirby calls him boss; Darren Milner owing; Ada at her window.

Act I, The Inheritance (first week, most scripted): five threads: the outfit's claim (first ask night one; refusing breaks the deal, not a quest); the warehouse fire (Alison Sedman, Ellis); Mickey's real book (Sheila shows it when she trusts him or under Ellis's pressure; a page ties the fire to the outfit); the street deciding who he is; someone worth being honest for (Alison, or Philip Danby still to write). Ada's tea the first test. Ends with Sheila: "So which is it going to be?" Wind it down, take it over, or refuse to say.

Act II, The Squeeze: opens when the business has grown. Maureen Jensen, the Widow, and the dockside syndicate go after his people (poaching Ron, taxing drivers); Geoffrey Agar and the old-money machine go after clean money with paper (the private-hire licence, a solicitor's letter, an inspection); Danny Cammack's new crew go after his cover (noise on Quay Street). The Fixer sells true reads, a meeting, one truce. DS Carol Ellis joins the crimes to the fire: one case. One guaranteed collision of his two lives. Ends at a sit-down with one head: accept, defy, or counter.

Act III, The Ledger Comes Due (an audit): a VAT inspection by Customs and Excise; the inspector brings one item each morning; Sheila may tell where the lie holds; Ellis offers a trade (give her a rival); a crew member may ask to take over; on the last day he can reach only a few people.

Endings (as built; stronger wins: Quiet, Both, Straight Life, Kingdom):
- Quiet: hands it to someone who can hold it (competence, loyalty, standing, no feud), never while hunted for a killing; three watch-only days.
- Both: business survives, one friendship holds, the street does not hold his rackets as fact, Ellis's case answerable, books hold and make sense; rare, not meant for a first playthrough.
- The Kingdom: business survives and books hold; people civil and no more unless one friend still counts him.
- The Straight Life: no business at the close (never built or sold up), one friendship holds.
- Burn Both: none of these; what doing nothing produces.
- D58: no redemption path; every cost visible as it approaches (D33).

Writing rules: beats fire on states; no single beat can fail the run; the simulation decides, the models only voice it; no drink, gambling or children.

Owed: Act III's Core text still reads as a pub; the laundering cap to be re-derived for a cab office under the 1983 VAT Act.

Open (canon's open question 2): does the spine stand with today's cast sheets (Ada the widow, Philip the teacher); recommended yes.

## 19. the-four-structural-defences.md

Date: written and verified 14 September 2026. Status: LIVE; an argument, not a plan.

Purpose: answer the criticism that AI NPC games are hollow (The criticism).

The four:
1. Outputs are classifications and closed-set choices executed by deterministic code; IntentKind is Narrative, Mechanical, Novel; a value outside VerbArg.Options invalidates the routing, never coerced.
2. Beliefs are rows in a memory store, not chat history; since 14 September nothing is removed from MemoryStore (the prune deleted over half a seven-agent soak street).
3. The model never decides an outcome; Adjudicator.Binds refuses effects on a requirement nobody could fail.
4. A character can only say what the simulation licenses.
- Fifth, for Jafar's judgement: the lexical fast path is the complete fallback with no model; the game is playable with no model present.
- Not claimed: that conversations are good, that the model is accurate, or that the four are measured.

## 20. the-gap.md

Date: 28 July 2026; updated 29 July. Status: LOG, NOT CURRENT.

Purpose: how far LEDGER is from KCD2 and GTA5 and how to close it.

Measurement (section 1, 0 to 10, LEDGER, KCD2, GTA5): social simulation 9, 4, 2; non-repeating dialogue 8, 5, 4; consequence 8, 6, 3; robustness 8; writing unproven, 8, 8; feel 5, 7, 9; audio 4, 8, 9; music and cinematics 3, 8, 9; content volume 3, 9, 10 (rescope); environment art 2, 9, 9; lighting 2, 9, 8 (cheapest big win); animation 1 to 4, 8, 9 (biggest gap).
- KCD2 about 250 people for five years; GTA5 about a thousand people and about a quarter of a billion dollars.
- Target: "unmistakably worse-looking than KCD2, unmistakably deeper than either" (section 2).
- Animation (3b): the mannequin of thirteen boxes and a sphere; Core/MotionMatch built; free datasets (AMASS, LAFAN1, 100STYLE) largely non-commercial; licensed libraries $100 to $1000.
- Audio (3c): a 3,000-line bark bank about five hours of GPU time.
- Scope call (section 4): cut from seven districts to two or three, dense.
- Budget (section 6): total $200 to $1550.
- Timeline (section 7): to about 3 months, competent indie; 3 to 9 months, motion matching, more districts; 9 to 12 months polish.
- Cannot do (section 8): make art, judge aesthetics, buy anything, playtest.

## 21. side-stories-2026-11-08.md

Date: draft, 8 November 2026, for his page (order of 2 November, n02-9-side-stories). Nothing built.

Purpose: thirty-two side stories found on foot.

Method: Yakuza 0 (found on foot, mostly light); KCD2 study 16 template (saved states, failure continues, patience 2 to 6 town hours, place named by landmark); canon D24 (every story ends in something the town knows; money-only stories cut).

Rules (The rules every story keeps): found on foot, never a marker; a Ledger line of about 22 words per step; offered on a state, window at least 2 town hours; two or three endings and a failure that continues; content rule throughout (adults only, no drink, no gambling of any kind, no children, nothing sexual, drugs never shown, no slur voiced, religion never mocked); Tom never drives; no real names; all micro, 3 to 5 steps (none 11 or more); tone light, grey or dark.

The stories (number, title, tone, act; offered when; waits):
- At the office: 1 The long way round, grey, I (Kevin Needham's short fares; until his pay day). 2 Two real minutes, light, I (Pauline's phone; about one minute). 3 The night lodger, light, I (Darren asleep in the spare car; until next night). 4 Mickey's Friday, light, I (Lily Tang's two of number nine; Fridays for four weeks). 5 A coat from the back room, grey, I to II (Tracey Scarth; Mickey's coat; until next market day). 6 The name on the board, light with weight, I to II (Shaun Hewson; 4 town hours). 7 A ride for the sergeant, grey, II (Ellis's car fails; 30 town minutes).
- On the parade: 8 Haddock's dear, light, I (Brenda Laverack; 3 dawns). 9 Twelve weeks' notice, grey, I to II (Julie Kettlewell; 6 hours). 10 The laundry's hampers, light, II (Doreen Harland; 2 days). 11 The window at the caff, grey, I to II (Grace Rinaldi; 2 days). 12 Closing time at the Tangs', grey, II (three closing times; racism never voiced or rewarded). 13 Off the back of a lorry, light, I (Darren's radios; 2 hours). 14 Posters on the glass, light, I to II (anti-poll-tax poster; a week).
- Quay and docks: 15 Half the berths empty, dark, II (Colin Mastin; next night). 16 The name board, light, I to II (Albert Suggitt; 3 days). 17 Mickey's mooring, grey, II (Gary Mawer; month end). 18 The ferry parcel, grey, I to II (letters to June; until June leaves). 19 The quiet quay, grey, II to III (Susan Coverdale, customs; three late turns). 20 All on the forms, grey, II (Christine Pickering; one telling).
- By the chapel: 21 Lilies, light, I (Winifred Duggleby; until Sunday). 22 Father Walsh's rounds, light, I to II (Nora Cronin; until cold weather ends). 23 Lead off the roof, grey, II (Dennis Iveson; 2 days). 24 Sign there, dear, light, I to II (Edith Stockill's will; 6 hours).
- Rows behind: 25 Looking costs nothing, grey, I (Rita Welburn, Mickey's watch, pawned by Ron; a month). 26 Monday at Hal's, light, any (Mondays 10 to 4). 27 Friday means Friday, grey, I to II (Sylvia Rennison; until Friday). 28 One way, light, I to II (Karen Grummitt; Thursday 5:00). 29 The rent on Ada's window, grey, I (Dawn Pybus; next rent day; only after Ada's tea). 30 The lamp outside Ada's, light, I to II (a week). 31 Nothing moves but me, dark, II (Norman Dent; 2 nights). 32 The camcorder, dark, any (only if a deed was filmed; a week; owner drafted as Hal).

Spread: 15 light, 14 grey, 3 dark; 21 open in Act I, 9 in Act II, 2 in any act; all micro; 24 of the thirty regulars give a story; Lee Drewery and Wayne Harrison have none.

Open: the sign's words (6); whether a story may lean on a principal's private life (4, 18, 29); the boat's name (16) and camcorder owner (32); Mickey's mooring invented; Yakuza 0's count of about 100 unverified; no state graphs, Ledger lines or tests yet.

## 22. authored-breadth-2026-11-13.md

Date: 13 November 2026, 23:02 (advisor's message 156). The ruling itself is RULINGS.md's first line.

Purpose: the notes beside his ruling on authored breadth.

Notes:
1. Writing is the biggest lever: every character gets a card, a history and relationships.
2. The crowd comes from authored rules (casting by role and district, period wardrobe lists, routines); no random faces or clothes.
3. Phase 5's kits and placement rules from the town plan are authored; sampled checks scale verification.
4. Kiln's tools carry out specs and the locked judge checks; image-to-3D and rule-built terraces are raw material until they pass; the 22 September image-to-3D ruling checked when props start.
5. Live talk only from authored facts; the fact check verifies.
6. Planning counts verified pieces per week by kind beside hours, from 16 November.
- Test for any piece: can we point to its spec and its check?

## 23. police-asking-2026-09-29.md

Date: 29 September 2026, for Jafar's page (checklist A15.06 and A15.09).

Purpose: people Ellis asks remember being asked and can say so.

Rules (What happens): on a visit about Tom she asks everybody of his day world who holds a story of his nights; a visit for a body asks nobody about him; each remembers being asked; the visit becomes news but never counts towards bringing her back; said to his face once each while news; changes nothing in how they stand to him.
- Six lines for those asked (for example "That detective stopped me about you.") and six for those who heard (for example "Word is Ellis was down the street after you.").
- Measured: taking the envelope every night, she comes day 5 at minute 48 and asks six of the street's ten; by minute 60 nine hold it (on the forty: asks thirteen, thirty-five hold it); Sheila says it at minute 49.

## 24. rumour-reach-2026-09-23.md

Date: 23 September 2026 (decision 2, ruled that day). No constant changed.

Purpose: why a realistic witness under-fills the circle, and whether the town visibly knows within thirty minutes.

Rules and numbers:
- Clock: 2 game minutes per real second; 30 real minutes is 60 game hours, 2.5 game days; one game day 12 real minutes; only pause stops it; the Fall skips 3 days.
- Share: passed = confidence times tie times 0.8 (HopDecay); refused under 0.2 (a body exempt); half-life 96 game hours, dropped under 0.03; copies compared by max, never added.
- Meeting: gossip round every 6 game minutes; talk range 6 m; 55 of 80 live ties never meet (29 of 80 with walking; 46 of 80 at 10 m); crowd ties meet in 0.14% of pair-hours; nothing links crowd residents to named characters.
- Graph: 40 people, 98 ties written, 80 live; mean live tie 0.44; 12 at 0.6 or more; 4 at 0.7 or more.
- Reach in the real street: Rocco 3 to 4 people; the average of 40 witnesses 0.5 to 1.5, most reach nobody; at 60 h figures equal 168 h figures.
- Stance: pressure = 0.55 times suspicion plus 0.45 times strongest rumour, minus 0.7 times (loyalty minus 0.5) for loyal NPCs, minus 0.12 with the coat. Rungs: Notices 0.12, Watches 0.26, Comments 0.42, Avoids 0.58, Refuses 0.72, Confronts 0.86.
- Suspicion: hearing adds 0.12 times passed; a contradicting rumour adds 0.35 times passed; Uneasy at 0.25. Naming needs familiarity 0.35; hearsay gives 0.20.
- Heat: status word quiet under 0.2, murmuring under 0.45, uneasy under 0.7; takings 220 times (1 minus 0.85 times heat).
- Conclusion: the number who know is not what is missing; how faintly they know is. The single biggest lever: the reaction ladder's 0.45 weight on rumour.

## 25. The rest of game-design/, by title only

PLAYTEST-RUNBOOK.md; arrest-2026-09-29.md; arrest-words-2026-09-29.md; art-collaboration.md; bark-names.json; barks.json; canon-proposal-graffiti-crews.md; cast-noor-draft.md; cast-tier1-batch2.md; clip-findings.txt; counterparty-purses-spec.md; day-one-2026-09-29.md; day-three-2026-09-29.md; ellis-2026-09-29.md; first-ask-2026-09-29.md; imagegen-batch-2.md; landing-2026-09-29.md; live-speech-latency.md; m0-plan.md; m15-the-world-speaks.md; playtest-notes-2026-07-29.md; playtest-notes-2026-07-30.md; playtest-plan.md; production-plan-audio-art.md; qa-matrix.md; research-mechanics.md; research-openworld-audit.md; roadmap-history.md; rumour-reach-quay-2026-09-23.md; setting-britain-2026-07-31.md; sheila-trust-2026-09-29.md; shopping-list.md; stranger-test-script.md; testing-system.md; threats-2026-09-29.md; tier2-batch-1.json; tier2-pipeline-spec.md; town-news-sample-2026-09-29.md; town-plan.md; town-traits-draft-2026-09-29.md; visual-bar-sources.md; voice-casting-history.md; voice-casting.md; voice-picks.json; voice-pipeline-plan-2026-07-31.md; waiting-2026-09-29.md; warehouse-fire-2026-09-29.md (with an approval file); week-end-2026-09-29.md; what-they-call-him-2026-09-29.md; writing-check-free.md; writing-judgement-2026-08-03.md; writing-samples-before-fixes.md; writing-samples.md. Folders: mickeys-office (BRIEF.md), picked-clips (voice clips), reference (README.md), research (GOVERNS.md, art-direction.md, content-sourcing.md, imagegen-licence-check.md, inhabited-street.md, performance-budget.md, procedural-density.md, water.md), sim-shots, voice-conds, voice-live.

## 26. Contradictions between these documents

Facts only; both sources named.

1. Tom's business and street. A minicab office, Mickey's, on Quay Street (story-outline, The spine; combat-design, What changed from July). A pub or bar on Hook Street (how-to-play, opening; combat-spec, section 2; weapons-spec, 4.2 rung 4 "Runs the bar on Hook Street", 7.1 "at home in the bar", 7.3 "something in the bar").
2. Tom's surname. Nowak (story-outline, The spine; ending-signs, factor 1; agency-model, Tom's rise). Novak (combat-spec, section 2; weapons-spec, Family 6 and 15.2).
3. Who asks the day-7 question. Sheila, over the real book (first-hour, The hour; story-outline, Act I). Lena, over the true books (how-to-play, The week; open-city-spec, section 4 item 2, day-8 teaser).
4. Ellis. DS Carol Ellis (story-outline, Act II; first-hour, minutes 36 to 60). Mara Ellis, "an inspector" (combat-spec, 7b).
5. The rivals' names. Sera Kest (Dockside), Aldous Vane (the machine), Danny Ro (the New crew) (empire-roster, Faction agency). Maureen Jensen the Widow, Geoffrey Agar, Danny Cammack (story-outline, Act II).
6. The core cast. Lena, Ada, Rocco, Noor as core; Sam, Joey, Marla, Victor recruitable (empire-roster, Recruitables); Rocco, Lena, Sam, Joey, Noor as the measured street (rumour-reach, section 2 and F). Sheila, Ron, Darren, Ada, June as the five met on day 1 (first-hour; first-hour-on-paper; story-outline, Arrival).
7. Drink and gambling. The story rules out drink and gambling (story-outline, Rules the writing keeps; side-stories, rules); combat-design bars bottles and glasses as weapons (The street is a weapon). Weapons-spec lists the bottle as a blunt weapon (Family 2), "a bad drink" (Family 6), "a bottle of something" (Family 7) and "bottle smashing" at loudness 70 (16.2). Empire-roster has the rival's first rung as "slow beer" and Victor's need as "a slice of his gambling marker cleared"; how-to-play repeats "a slow beer at your pub" and "buying the room a round".
8. Chases. "No chase", a refusal (weapons-spec, 15.2); chases and police pursuit out of scope (streets-and-cars-spec, section 5). "Someone runs. A foot chase the runner can escape through alleys, yards and doorways" (combat-design, How fights end).
9. Guns. Out of scope (combat-spec, sections 3 and 7). In the final game, rare, built last (combat-design, Weapons; weapons-spec, Family 5 and 18 November header). Combat-design's firearms are a sawn-off shotgun and an old revolver; weapons-spec lists a .22 target pistol, .38 snub, .45 automatic and sawn-off (suppressed .22 dropped). Weapons-spec 5.5 says "No rifles, no automatic weapons" while Family 5 lists a ".45 automatic".
10. How good Tom is in a fight. A skilled player wins most fair one-on-ones (combat-design, How a fight feels). "NOT empowering", even the best line wins about a quarter (combat-spec, sections 2 and 6); "Most of the roster says lose. Tom runs a bar" (weapons-spec, 5.3). Combat-spec targets a handful of fights per playthrough (section 2); combat-design says fighting is "good to do" (opening).
11. Death from a fall. A fall against a kerb, wall or step after a blow "the town treats it as a killing" (combat-design, Since 12 October). An accident such as a push down stairs "is the only violence in this game that produces no crime", and becomes an inquest (weapons-spec, Family 6).
12. Running people over. Weapons-spec lists "a road and a moving car" as an accident (Family 6). Pedestrian collision out of scope (streets-and-cars-spec, section 5); "you cannot run people over" (how-to-play, The streets).
13. Whether Tom drives. Tom has a car he drives (how-to-play, Controls and The streets; streets-and-cars-spec, section 4). "Tom never drives (others drive the firm's cars)" (side-stories, rules). "No drivable-vehicle physics, ever" (agency-model, decision 4), reconciled there as a kinematic car.
14. The police ladder after a witnessed killing. One body with one watching witness goes straight to Manhunt at pressure 1.00 (combat-spec, phase 3b table). It should pass through investigating for at least a day before a manhunt (ending-signs, factor 7, proposed and awaiting his call).
15. The fight camera. "The camera closes in a little" (combat-design, How a fight feels). The camera widens for fights (combat-design, Since 12 October; game-feel-spec, section 3).
16. Failing the week. Two hostile mornings in a row, or the outfit's patience exhausted, ends you (how-to-play, The week). Refusing the ask does not fail the game (first-hour, minutes 7 to 11); "No single beat can fail the run" (story-outline, Rules the writing keeps).
17. How often the outfit asks. A drop posted at 22:00 each night (how-to-play, The week). Asks every other night from night one (first-hour-on-paper, opening).
18. Number of districts. Seven districts (agency-model, benchmark evidence; open-city-spec, section 3 scale path). Cut to two or three (the-gap, section 4); the Hook plus the docks for 15 to 20 hours, more after release (agency-model, Study 17 item 1).
19. Rival organisations in Empire v1. The other two rival organisations excluded (open-city-spec, sections 2 and 5). Three arms built with heads and members (empire-roster, Faction agency; how-to-play, The open city).
20. Economy. Economy simulated end to end (agency-model, decision 2). Canon D24: not an economy simulation (agency-model, Tom's rise and Study 17 item 8, cited as open).
21. Character competence. Tracked per domain, unlocking approaches (agency-model, outside-in additions). Tom rises in position, never in numbers, and does not get better at fighting (agency-model, Tom's rise; combat-design, Tom, the crew and the odds); listed open in agency-model.
22. Who carries the inspection. Tobias Reese, inspecting for six mornings (balance-findings-endings, A new observation). A VAT inspection by Customs and Excise, unnamed inspector (story-outline, Act III).
