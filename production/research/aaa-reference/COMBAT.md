# COMBAT: how Kingdom Come 2 and Mafia: The Old Country do melee, set beside the combat spec

Reviewed by a fresh reviewer on 13 October 2026 (REVIEW-7b.md); its listed fixes are applied and were not reviewed again. The section "Set against Jafar's rulings of 12 October and his design", the note above the table in section 4, the pointer in section 5 and section 5.6 (the list's adjustments) were added later and were NOT reviewed.

13 October 2026 (Jafar's local time). Cloud week 42, unit 7b, the combat part. Public pages only. Nothing from either game (files, text, pictures, sound) is in this file: only this file's own sentences, its own arithmetic and the developers' published numbers, each with its source key. The keys are listed with their links at the end.

## In plain words

1. Neither game publishes a timing test. The only hard numbers are Warhorse's own rules table for Kingdom Come 2 (stamina costs, about 2 seconds between a careful opponent's attacks). For Mafia's knife duels there are no numbers at all.
2. Both games make a blow readable with one clear signal (a green shield, a red glint). That backs the spec's "telegraph, not tell". Kingdom Come's stamina, witnesses and town unrest suit LEDGER; its stats, perks and lock-on do not.
3. Of 42 points taken from the spec: 12 ADOPT, 25 ADAPT, 5 IGNORE (section 4).
4. The draft for phase 3 lists 17 animations for two men with a shove and a strike (section 5). The strike winds up for about two thirds of a second (20 frames), by judgement: people need about 0.2 s just to press one key when a light comes on, before any choice.
5. Jafar needs to do nothing now. Combat waits for characters (PLAN.md), and section 5 is the brief for that day.
6. Added later, not reviewed: the next section sets all of this against Jafar's rulings of 12 October and his design "LEDGER Combat: Final State" (39 rows). Where they differ from the July spec, they win. Section 4 stays as the record. Section 5.6 adds 15 entries to the target list, 2 of them for the first test.

## Set against Jafar's rulings of 12 October and his design (replaces the July spec as the yardstick)

**Not reviewed.** This section, the note above the table in section 4 and the additions in section 5.6 were written on 13 October 2026, after the fresh review. No reviewer has read them. They use no new sources about the two games: every game finding below is one this file already holds, cited by section and key. Marks are as in section 1.

**Source.** The design is Jafar's document "LEDGER Combat: Final State" (Claude Docs, revision 12, dated 12 October 2026). This section was written from that document as read on 13 October 2026. The builder will import it as game-design/combat-design.md; if the imported text differs, this section is redone. Its five rulings are in RULINGS.md (the lines starting "12 Oct, combat"). Where the rulings and the design differ from game-design/combat-spec.md (the July spec, now marked replaced and kept as the record of what the Core built), they win. Section 4 was written against that spec and stays as the record too.

**Study 14.** The design names Study 14: the lab's study of the two games' own files on Jafar's PC (his route B). It is not part of this file, which holds public pages only. The design says Study 14 sets the numbers it still lacks: wind-up, strike and recovery times, hit-pause length, blows and stamina to put a man down, and how many attackers swing at once. This file's numbers on those four points are stand-ins, listed after the table.

**Verdicts.** As in section 4 (ADOPT: take it as it is; ADAPT: take the idea, change the form; IGNORE: leave it), plus NOT COVERED: no page read for this file says anything on the point. R01 to R05 are the five rulings of 12 October; the other rows follow the design in its own order. "Old row" means a row of the table in section 4. The design's own words are quoted in the second column (each under 15 words).

### The table

| Id | Ruling or design point | KCD2 | Mafia TOC | Verdict | Reason |
|---|---|---|---|---|---|
| R01 | Ruling: fighting is good to do and costly to have done (weighty, readable, learnable; the cost comes afterwards: injuries, witnesses, police, feuds) | One signal for the moment (green shield) and a price per swing, 26 stamina (2.2, 2.3, 2.4). Afterwards: health that does not heal itself, witnesses who report, reputation that spreads, a watchful area (2.4, 2.7). Players call the combat a loud complaint [K33] | One signal (red glint, sound) and a parry called generous [M1, M13]. Nothing afterwards published (3.5); fights "don't change much" [M19] | ADAPT | Take the one-signal read and the price per swing. The cost afterwards is KCD2's strongest finding for LEDGER (old rows 1, 5, 29, 34, 39) and moves up (list below). R16, R17 and R37 take the parts one by one |
| R02 | Ruling: Tom does not get better at fighting; his power grows through crew, weapons and reputation | Weak at the start [K27]; skills and perks grow with use, "unstoppable by halfway" says one player [K33] (old row 3) | Enzo is a "coiled spring" who scrapes for weapons [M7]; scarce ammunition [M8]. No growth published | ADAPT | Drop growth (D11, no stats). Growth through crew, weapons and reputation is NOT COVERED by either game: KCD2's reputation changes how people answer a crime (2.7), not a fighter's power. See R24. Old row 3 superseded in part |
| R03 | Ruling: fighting must look and feel AAA (D24 changed for fighting only; still not a shooter) | First person; a hit reaction slows the player; a too-long knock-back was fixed as a bug (2.3, old row 40). No hit-pause or frame figure published | Third person on Unreal Engine 5 (3.1); critics find the fights repetitive, "contractual" (3.6); PC Gamer 45 of 100 [M10]; hit-pause not published | ADAPT | Neither game publishes a timing test (In plain words, 1), so neither gives a feel yardstick. A large budget did not keep Mafia's fights from repeating (3.6). The measures of 5.4 stay this file's judgement until Study 14. Old rows 37 and 42 superseded in part |
| R04 | Ruling: guns are in the final game, rare, built only after melee works (tier four: sawn-off shotgun, old revolver; one shot is a town-wide event; armed police only when a gun is involved) | Crossbows and early firearms are slow and a firearm can explode in the hand; the sword is faster than reloading [K5, K7, K8] | Guns central, "every bullet counts"; scarce ammunition [M5, M8] | ADAPT | Old row 13 superseded. Its own note stands: KCD2's slow, fragile gun is the model for a rare gun, Mafia's gun-led game is not. A shot as a town-wide event, and armed police: NOT COVERED (nearest: reputation spreads by distance, 2.7). Firearms are a later note and last in the build order |
| R05 | Ruling: Tom cannot die; beaten, stabbed or shot, he wakes in hospital or on the pavement with the injuries, the bill and a street that knows he lost | Hanging is game over [K14]; fists knock out, a reading (2.6); a knock-out is an unconsciousness depth that fades, about 480 s before vitality counts (2.6, derived, unverified); injuries last (old row 39); reputation spreads (2.7) | Duels are to the death, scripted and not skippable [M7, M21]; what happens to a loser is not published | ADAPT | Take KCD2's knock-out as the shape of Tom's blackout (down, a timed way back, injuries stay, news spreads). Drop game over. The bill, the hospital and a street that knows he lost: NOT COVERED. Old row 31 superseded for Tom |
| R06 | The ladder: eight rungs, he can stop on any; each rung an act with the seven perceivable slots; most confrontations end on rungs 1 to 4 | A hare icon runs from suspicion through recognition and confrontation to hostile [K30]; drawing a weapon makes NPCs confront; anger above 0.67 arms everyone (2.7, old row 7) | A duel starts by script [M5]; fights are scripted (old row 30). No ladder published | ADAPT | KCD2's four icon states and anger scale are the nearest thing to a ladder, but they are drawn on a HUD for the player (old row 17); LEDGER's rungs show on bodies and fill the Core's seven slots (5.3). That most confrontations end early: NOT COVERED by either game. Old row 6 stands |
| R07 | Rung 1, stare: holds a man's eye too long; "a tension others notice; nothing to report" | The hare icon's white state is suspicion; 4 s to recognise an unremarkable person, 4 s before NPCs lose you (2.7) [K30, K1] | Enemies spot from far away and go to where they saw you (3.4) | ADAPT | Old row 17. A stare is an act on a body, not an icon. KCD2's 4 s recognition time sits beside the 3 s hold of A02 (5.3). Entry F01 (5.6) |
| R08 | Rung 2, square up: changes stance, visible to everyone; "witnesses start paying attention before anything lands" | No stance verb; drawing a weapon makes NPCs confront (old row 7) [K1, K9] | Enzo "boldly draws his knife to challenge foes" [M6]; the duel start is scripted [M5] | ADAPT | Old row 7 stands. Both games show a visible commitment; neither shows fists up. Already A01 and A02 (5.3) |
| R09 | Rung 3, threaten: says or shows what will happen; "can stop a report to the police, never the street's talk" | No page read describes the player threatening anyone. Nearest: a witness who asks money for silence [K25]; a would-be reporter killed before the alarm goes out [K30] (2.7) | Not published | NOT COVERED | Neither game says anything on a threat as a player's act. KCD2's two ways to stop a report are a payment and a killing. Entry F02, source judgement (5.6) |
| R10 | Rung 4, shove or grab: pushes him away, takes his collar, pins him to a wall; "a scuffle: talked about, rarely reported" | A clinch with "locks, grips and throws"; a clinch push out of a fighting pen was removed as a fault in patch 1.2; no shove verb read for KCD2 (2.2) [K5, K9] | A bare-hand grab from behind, held to choke (3.4) [M15]; no shove published | ADAPT | Old row 9. The shove stands as C01. KCD2's clinch is the only grab finding and it is a weapon lock; Mafia's is a stealth choke. The collar grab and the pin are LEDGER's own: F03 to F05 and G01 to G04 (judgement) |
| R11 | Rung 5, strike: lands a committed blow; "a fight: most who see it report it; injuries begin" | A four-direction swing, 26 stamina, chain, charge to 1.4 s, a spam delay added (2.2, 2.3); a guard who sees a crime reports it, and civilians can (2.7) [K26] | Slash, thrust, strike and a red-glint heavy strike [M1, M13] | ADAPT | Old row 8. Stands as B01 and B02. KCD2's guards and civilians who report what they see match the design's line; how many report is published nowhere |
| R12 | Rung 6, weapon out: shows a knife, a bat or a gun; "the street scatters; a gun out is news across town" | Drawing a weapon makes NPCs confront; watchers flee if the source of the violence moves too close (patch 1.2); NPCs arm everywhere above anger 0.67 (2.7) [K1, K9] | Enzo "boldly draws his knife to challenge foes" [M6]; one knife carried (3.2) | ADAPT | Both games treat a drawn weapon as an act others react to; the Core's draw slot is the same idea (5.3). KCD2's NPCs confront it, where the design's street scatters. Old row 7. Later than the lower rungs |
| R13 | Rung 7, weapon used: cuts, clubs or shoots; "police interest, a hospital visit, a weapon that can be traced" | Bleeding loses 1 HP per 6 s; health does not heal itself; gear wears (old rows 5, 39) [K1, K18]; crimes bring fines or worse (2.7) | A knife wears with use; duels to the death (3.2) [M3, M7]. No police published | ADAPT | Old rows 5 and 39: take lasting injury and the heal schedule. A hospital visit and a traceable weapon: NOT COVERED. Neither game gives a weapon timing (2.3, 3.2). Later (5.6) |
| R14 | Rung 8, kill: a man does not get up; "a fact no rumour can soften"; the police from procedure upwards | Armed fights can kill; killing innocents is a crime; the police ladder runs from fine to execution; a corpse is hidden after 300 s or 3,600 s (2.6, 2.7) | Quick-time kills in duels and one-hit knife kills; no bystander reaction published (3.2, 3.5) | ADAPT | For other men: Tom cannot die. Old rows 29, 33, 34 and 35 stand (police, one problem solved, who else saw, nobody the same). The corpse timer is not copied (old row 32). KCD2's wipe of the record after a punishment must not be copied (2.7) |
| R15 | Finishing a man who is already down: never a move in the flow of a fight; "a decision taken in the quiet afterwards" | A separate mercy kill on a weak foe, with its own animation; knock-out is the alternative (2.6) [K18, K9] | Quick-time kills inside the duel; one-hit knife kills mid-fight (3.2) [M14, M3] | ADAPT | Old row 12. Take KCD2's separate act. Drop the animation: in the design it is a decision, not a move, so no clip is built (5.5). R34 is what comes before it |
| R16 | How a fight feels, weight: every blow commits the body; contact is sold by hit-pause, a jolt of the camera and sound, "never by numbers on screen" | A hit reaction slows the player; a too-long knock-back was a bug; patches fix missing hit and attack sounds (2.3, old rows 20, 40) [K9]. No hit-pause length published | Hit-pause not published (old row 37); "listen for critical audio cues" [M1] | ADAPT | Already in 5.3: B01 has a 2-frame hit-pause, a camera nudge and a thud (judgement; Dustloop says hit-stop exists and its length differs by game [S1]). The lengths are Study 14's to replace |
| R17 | How a fight feels, readable and learnable: every incoming blow has a wind-up readable from the body; a skilled player wins most fair one-on-ones; mashing "tires you out and loses" | One signal per blow (green shield, weapon position); a stamina price; a spam delay added by patch (2.2, 2.3) [K27, K28, K9]. No win rate published | One signal (red glint, sound); button-mashing "won't get Enzo very far" [M1, M13] | ADAPT | Old rows 19 and 26. Take the one-signal tell and a price per swing. The wind-up (20 frames, 5.1) is judgement. The win rate is NOT COVERED by either game. Old row 27 superseded |
| R18 | No mode: no arena, no lock-on; "the camera closes in a little and the street carries on" | Lock-on with a key, cycling between foes, the camera locked in combat (2.8); a hare icon with crossed swords in direct combat (old row 6); lock-on keeps a crowd survivable (2.5, design reading) | A separate one-on-one mode with five actions [M7, M22]; third person (3.1) | IGNORE | Old rows 6 and 37. Leave lock-on and the arena. Without lock-on a crowd is more dangerous than in KCD2, which suits R23. The camera must show the man at the side (K35's tip: keep all in view, 2.5) |
| R19 | No combat music | Music and UI hint at combat (a patch fix mentions them) (old row 6) [K10] | Audio cues carry the timing [M1] | IGNORE | Old row 6: leave the music. Sound as the read stays (old row 20) |
| R20 | No health bar: condition shows in posture, breathing, a guard that drops, blood and a limp | Bars shown; Hardcore Mode hides health and stamina bars and cuts combat cues; low stamina weakens blows (2.4, 2.8) [K20, K6, K18] | A HUD scale option; combat bars not described (3.7) [M3] | ADAPT | Old rows 14, 15 and 16. Hardcore Mode shows it can ship. Its cut cues are not wanted: the body signals take their place (A02's breath, E02's sinking guard, D05, 5.3) |
| R21 | A minimal HUD as a settings switch, so the values are data from day one | Hardcore Mode and "UI only when relevant" are settings (2.8) [K6, K11] | An adjustable HUD [M1, M3] | ADOPT | Old row 23. Both games ship it as a setting |
| R22 | Accessible: a longer wind-up window and an auto-resolve option, "the same fight at a different tempo" | Windows widen with skill; fans built a mod to widen them within ten days of release [K22, K1, K38] (old row 22) | "Simplified Struggle" completes rapid presses; three difficulty levels (3.7) [M3] | ADAPT | Old row 22. Already the 1.5 times telegraph setting of 5.1 and item 8 of 5.4. Mafia's auto-complete is the model for auto-resolve; KCD2's skill growth is not (no stats) |
| R23 | Two against one is deadly; three is a beating; being outnumbered is the first of the three gaps | Outnumbered is deadly [K33]; an attack from behind is almost impossible to block or dodge [K35]; a gap rule thins a crowd, 3.6 s each for two (2.3, 2.5, derived from an unverified reading) | Not published | ADAPT | Take "outnumbered is deadly" and the players' tips (terrain so they come one at a time [K33], keep all in view [K35]). Do not copy the gap rule: it makes two men hit about as often as one (list below, 5.6) |
| R24 | The crew changes the odds (a man at your shoulder, on the door, one you send); crew who watch remember it, as loyalty and fear; ordering a named man hurt makes a second person who knows | One quest note stops friendly NPCs reporting [K11]; a person's opinion weighs 5, a faction's 3, a group's 1 (2.7, old row 35). No crew or follower finding | Not published | NOT COVERED | Neither game has a crew that fights for the player. Loyalty and fear are already in the Core (the design; old row 35). The nearest KCD2 findings are the witness who is paid or silenced (2.7) |
| R25 | Other people fight too: a feud between two townspeople can become a fight the player can watch, join or break up | The gap between attacks is halved (factor 0.5) when the target is another NPC (2.3) [K1]; watchers flee if violence moves close (2.7) | Not published | ADAPT | KCD2's table shows that NPC against NPC fights exist and run faster. Whether the player can break one up is in no page read. Not in the first stages |
| R26 | The street as a weapon, places: walls, doorways, shop windows, railings, car bonnets, stairs, the quay edge | No page read describes a place as a weapon. Nearest: players use terrain so foes come one at a time [K33]; NPCs see through an open door [K8] (2.5, 2.7) | Not published | NOT COVERED | Neither game says anything on it. A shove into a wall is built (G01, G02) and the pin (G03, G04); the other places wait for the street stage (5.6) |
| R27 | The street as a weapon, things at hand: a brick, a chair, a snooker cue, a wheel brace, a cargo hook; nothing to do with drink | Not published; the content rule of 2.9 stands | A thrown coin only distracts (3.4) | NOT COVERED | Neither game says anything on picked-up weapons. They wait for the street stage (5.6) |
| R28 | The street as a weapon, built: each move against a surface is a paired animation of two bodies; Study 14 sets how many a street needs | KCD2's "locks, grips and throws" are paired moves in kind; no page read says how they are built (2.2) [K5] | A takedown from behind pairs two bodies in kind; the build is not published (3.4) | NOT COVERED | Neither game says how its paired moves are made. The first stages use this list's own entries (5.2, 5.6). The number of pairs a street needs is Study 14's |
| R29 | Tier, fists: nothing to carry; the town's word is "a fight" | Hooks, jabs and "occasional kicks"; three unarmed combos; fists knock out, a reading (2.2, 2.6) [K22, K18, K27] | No fist system published; one critic says none (3.3) [M20] | ADAPT | Old rows 8 to 10 and 31. Fists are the tier of the first stages. KCD2 is the model; Mafia is not |
| R30 | Tier, improvised: a brick, a chair, a snooker cue, a wheel brace, a cargo hook; picked up on the spot and left where it can be found | No page read describes one | No page read describes one | NOT COVERED | Neither game says anything. Street stage |
| R31 | Tier, carried: cosh, knuckleduster, a utility knife, flick knife, bat; seen on you and found in a search; "a man who came ready" | Weapons wear and are carried openly (old row 5; 2.2); no search of the player is described | One knife carried, three types, durability spent by use (3.2) [M1, M3] | ADAPT | Both games have a carried weapon that wears. Being found in a search, and having a history: NOT COVERED. Street stage |
| R32 | Ending, someone backs off: "a real option and often the best one" | The developers' tip "consider a tactical retreat" [K8]; fleeing draws a chase (2.6) | No retreat inside a duel [M22] | ADOPT | Old row 11. Already A03; J01 adds the longer retreat (5.6) |
| R33 | Ending, someone runs: a foot chase the runner can escape through alleys, yards and doorways; whether he was recognised decides what follows | Running from guards leads to a chase and a "wanted" state; morale under 0.2 makes an NPC flee; an AI hunts a target for 15 to 60 s; recognition takes 4 s, and a guard later says "aren't you that guy" (2.3, 2.6, 2.7) [K18, K26, K1, K14] | Not published | ADAPT | Take the chase, the hunt time as a bracket for when a chaser gives up, and recognition as what decides the aftermath. Whether KCD2's chase can be escaped is in no page read: NOT COVERED in part. J02 and J03 (5.6) |
| R34 | Ending, someone goes down: then the quiet decision, leave him, rob him or finish him | A knocked-out man stays down while a depth value fades; the first game's surrender rule lets the winner let him go, refuse, or take money or gear as a price [K22]; surrender can be switched off [K6] (2.6, old row 41) | Not published for a loser; boss prompts (3.2) | ADAPT | Old row 41. Stands as D06, D07 and D08, now also Tom's (R05): D08 is needed (5.6). KCD2's surrender rule is close to "leave him or rob him". "Finish him" is R15 |
| R35 | Ending, the police arrive mid-fight: a beat officer first, then more; running from them is a new offence; an arrest leads to custody and court (the 1990 police research) | A guard who sees a crime reports it; guards call reinforcements; guards attack if the player runs when confronted; running leads to a "wanted" state (2.6, 2.7) [K26, K18] | Not published (3.5) | ADAPT | Take the reports, the reinforcements and run-means-offence. How fast an officer arrives mid-fight is in no page read: NOT COVERED. Custody and court come from the police research, not these games. Old row 29. No new clip: the fighters use A03, J01 or J02 (5.6) |
| R36 | Ending, people step in: friends pull their man away, bystanders shout, a shopkeeper comes out | The opposite is read: watchers flee if violence moves close (2.7) [K9]; an NPC about to raise the alarm [K30] | Not published (3.5) | NOT COVERED | No page read has bystanders step between fighters. J04, source judgement, to be checked first against the townspeople animation research (5.5; CLAUDE.md: reuse first) |
| R37 | The aftermath carries over unchanged: injuries last and heal on a schedule, treatment costs money and plants a witness, blood stays on clothes, weapons have a history, feuds, a body, the crew who saw | Health does not heal itself; bleeding; injury fades 1 percent per 20 s; witnesses, spread, unrest, the punishment ladder (2.4, 2.7, old rows 1, 5, 29, 33 to 35, 39). Treatment cost: not described | Not published (3.5) | ADOPT | KCD2 is the only model and its findings rise in weight (list below). Covered by neither game: the bill, blood on clothes, a weapon's history, a feud between named people |
| R38 | The lab test of the animation source: one wind-up, one strike, one hit reaction and one shove into a wall, judged in the game camera beside Study 14's reference; two routes tried, then set aside under the usual rule | Not published: no page read says how Warhorse made or tested its combat animation | Not published; two developer diaries on knife research and motion capture were opened and not used (end of section 6) | NOT COVERED | Neither game gives a method to copy. The lab test is a subset of the first test: B01 (wind-up and strike), D03 (hit reaction), C01 with G01 (shove into a wall). This file's checks can be its measures (5.4 items 1, 2 and 6) |
| R39 | The first combat test, after the walk passes: two men, one shove and one strike with hit reactions, in the game camera, through the usual gate | First person; a hit reaction slows the player (2.3, old row 40) | Third person; hit-pause not published (old row 37) | ADAPT | No game gives a test to copy. Section 5 is already this test; its entries and items 1 to 9 stand. 5.6 adds G01 and G02 to it (the shove into a wall, from the lab test) and drafts the later stages in the design's build order |

Rows: 39. ADOPT 3, ADAPT 26, IGNORE 2, NOT COVERED 8. The design lists five endings (R32 to R36), one row each.

**Animation sources.** The design's sources to test are Mixamo, free motion libraries whose licences allow games, AI-generated motion and fixes keyed by the AI, "within Jafar's limits", with "nothing marked NoAI". Jafar narrowed that on 13 October (RULINGS.md, the 3 Oct line): content Epic itself publishes on Fab, the Game Animation Sample among it, may be used inside the game; NoAI content from any other seller stays out. The walk is rebuilt on that sample with motion matching (RULINGS.md, the 3 Oct line on poses). The design's Unreal tools (motion warping, physics-driven hit reactions, paired animations) suggest that this list's D, F and G entries are the authored base those tools blend over and line up (judgement).

### Old rows of section 4 that the design supersedes

The design's own table "What changed from July" gives the list. Its lines map to the old table like this.

- "Tom runs a bar, is 'not a fighter'" becomes "fights are good to do and cost afterwards": old row 3 is superseded in part. Its "no growth" half stands (R02); its "not a fighter" half does not (R01).
- "Even the best play won about a quarter of fair fights" becomes "A skilled player wins most fair one-on-ones": old row 27 loses its "quarter of the time" (R17). Its "three to four swings" half stands.
- "Five verbs, fought one against one" becomes an eight-rung ladder: old rows 7 to 12 are mapped to R07 to R15. Old row 10 (Guard) has no rung; the design keeps "a guard that drops" (R20), so E01 to E03 stand.
- "Guns out of scope" becomes "Guns in the final game, rare, built last": old row 13 is superseded (R04).
- "Fighting only had to not look broken (D24)" becomes "Fighting must look and feel AAA": old rows 37 and 42 are superseded in part (R03). Row 42's advice to stop if combat distracts is replaced by a warning against repetition.
- "Whether Tom can die was not settled" becomes "Tom cannot die": old row 31 is superseded for Tom (R05). The design also quotes the 10 September rule that killing is rare, permanent and remembered forever (D18), so for other men old rows 31 and 36 stand.
- "Unity and capsules" becomes "Unreal, MetaHumans and the game camera": no old row; section 5 already names the game camera.
- Old row 4 (a handful of fights) is no longer a yardstick: the design gives no count, only that most confrontations end on rungs 1 to 4 (R06).
- Old rows 6, 14 and 23 (no mode, no health bar, a HUD toggle) are confirmed, not changed (R18 to R21).

### What the rulings change in this file's findings

- **Tom cannot die (R05).** The games' death, game-over and corpse findings now matter for other men only: the hanging that ends KCD2 (2.7), the corpse timers of 300 s and 3,600 s (2.7, old rows 2 and 32), Mafia's duels to the death (3.2). KCD2's knock-out (2.6) matters for Tom: a timed way back, injuries that stay, news that spreads. D08 (getting up) is now needed (5.6).
- **Guns rare and last (R04).** The firearm findings (K5, K7, K8, M5, M8, old row 13) become a note for the last stage of the build order. Nothing in the target list changes for them.
- **No lock-on, no health bar, no combat music (R18 to R20).** The lock-on findings (the patch note on attacks without lock-on in 2.2, the design reading in 2.5, 2.8) and KCD2's bars are ignored. The stat findings are ignored too, because Tom does not get better (R02): K2's skills, the perfect-block window that widens with skill (the reading in 2.3), accessibility by skill (old row 22). Tempo comes from a setting (R22).
- **The cost afterwards moves up (R01, R37).** The witness, guard, spread and unrest findings of 2.7, and the persistence of injuries (old row 39), are what make a fight costly to have done. They come from KCD2 alone: Mafia publishes nothing on bystanders (3.5). They cover crimes, not defeats, so a street that knows Tom lost has no game finding behind it.
- **Crowds (R23).** KCD2's gap rule thins a crowd (2.3, 2.5). Copied as it is, two men would hit about as often as one: a blow every 1.8 s from the pair (3.6 s / 2) against every 2.0 s from one man (derived from an unverified reading). Section 5.6 keeps each man's own 2.0 s instead.
- **Win rate (R17).** The four blows of 5.4 run 3 are a mechanics check for one unguarded man, not a balance. Old row 27's quarter is gone and no game publishes a win rate, so the figure comes later from the lab.
- **The warning against repetition replaces the advice to stop (R03).** Old row 42 said to stop if combat distracts. The design asks for AAA instead, so the findings on repeating fights (3.6: M19, M18) become the thing to watch. The ladder and the street are the answer, by judgement.
- **The shove (R10).** Old row 9's shove creates distance in the open. Against a wall it does not: the men end 1.4 m apart, inside strike reach (derived, G01 in 5.6).

### Numbers that Study 14 is meant to replace

Everything below comes from public pages or from this file's own judgement. The design says Study 14 sets these four things from the games' files.

- **Wind-up, strike and recovery times.** Every length and key frame in 5.2 and 5.3 (all judgement); the derived wind-up of 5.1 (0.64 s, 20 frames, range 0.50 to 0.80 s); the shove's 8 frames and its range (0.20 to 0.35 s); the 5-frame guard raise; the recoveries (0.60 s after contact for B01, 1.2 s for B02). Nothing in sections 2 and 3 measures these (2.3, 3.2).
- **Hit-pause length.** The 2 frames (0.067 s) in B01, and the camera nudges (1.5, 1, 2 and 0.5 degrees) in B01, C01, D02, D06 and E03 (judgement; [S1]).
- **Blows and stamina to put a man down.** KCD2's stamina rows (K1: 26, 20, 22 a second, 0.6, 0.75, 15 to 40, 0.7) and the times derived from them (1.18 s, 1.97 s, 0.91 s), exported before release, where "retail values may differ" (2.3, 2.4, unverified item 8); and the four-blow result of 5.4 run 3, which comes from LEDGER's own Combat.cs constants and is to be compared with the games.
- **How many attackers swing at once.** K1's gap rows (2 s, 0.8, 4 s, 0.5; 2.3, 2.5); the derived 3.6, 5.2 and 6.8 s and the 0.5 to 0.6 a second (an unverified reading); B01's 2.0 s mean gap with its 0.5 s spread.
- All numbers marked judgement or derived in 5.6 stand in for the same four things.

### Left open for the design document

- The design gives words for what the street takes from each rung ("rarely reported", "most who see it report it") and no numbers: how many report, how long attention lasts. Only the shove has one (4.0 s, Bumps.AttentionSeconds, in C01).
- Defence. "A guard that drops" is in the design, but no guard, dodge or block is a rung. E01 to E03 stand as drafted. Whether there is a dodge, a block, or a held guard that becomes a grab is open.
- How a grab, a pin and a held man end: release, a shove that breaks it, a strike from the hold, a throw. The design says "pins him to a wall" and no more.
- How much a wall, doorway, bonnet or quay edge adds to a shove or a blow. The design names the places and gives no number. G01 assumes a wall adds nothing to a steady man.
- What "three is a beating" means for Tom's body, and how far two or three men stagger their blows (5.6 is judgement).
- The foot chase: how a chaser catches a runner, and whether a dead end can. The design says the runner can escape and that recognition decides what follows.
- How the quiet decision is made (a prompt, a held key, a choice), and who may be robbed or finished.
- Where Tom wakes, hospital or pavement, what decides it, and the size of the bill.
- Whether the stare has a time. The 3 s hold of A02 was the July spec's.
- The design's build order has no place for "people step in" (J04). It is placed with the lower rungs, by judgement.
- The design's carried tier names a real trade name for the utility knife, while the same line says every make is fictional. The name is not repeated in this file.
- The design's rulings table says the five rulings of 12 October still have to be recorded. They are already in RULINGS.md and DECISIONS.md, and canon.md's D24 sentence is edited.

## 1. How to read this file

- **Marks.** official (the developer's own page or wiki), interview (a named developer's words, printed by someone else), wiki (a community wiki), player (a forum post or a named guide writer), press (a critic or a guide site), standard (a public convention), derived (arithmetic by this file, formula shown), judgement (this file's own), unverified (could not be confirmed, used in no total or ratio).
- **Date read.** Every source was read on 13 October 2026 (Jafar's local time; the machine clock showed 22:04 UTC on 12 October). No other date is given per source.
- **How much was read.** Every page was read to its end, with two kinds of exception named in the Sources list: the long patch-note pages and the official rules table were read through their combat, crime, takedown, tutorial and feature sections, and their quest-by-quest fix lists were searched by keyword, not read line by line.
- **Words used.** A frame is one picture of an animation. At 30 frames per second one frame is 0.033 s. The wind-up is the slow part before a blow lands. Hit-pause is a freeze of one or two frames at the moment of contact. Footing is the spec's word for steady, reeling or down.
- **Names.** Canon names are used: Tom Nowak and DS Carol Ellis. The spec still says Tom Novak, Mara Ellis, and that Tom "runs a bar". Canon (D19) says Mickey's is a minicab office. The spec's argument holds with a minicab office.
- **Game material.** Official parameter names are quoted only so a reviewer can find the row. Quotes are under 15 words.

## 2. Kingdom Come: Deliverance II (KCD2)

### 2.1 What it is, for this comparison

- First person, open world, set in 15th century Bohemia [K17, K39]. Melee uses a lock-on "combat rose" with spokes that show the swing direction [K23]. Warhorse's own words for it: "authentic first person combat" [K39].
- Warhorse says success comes from mastery of techniques, "rather than an unseen roll of the dice" [K5]. The official modding wiki shows that NPC choices are chance weighted (section 2.3).
- A developer says the combat is "on its basis, the same combat as in the first game", with new movement sets and more animations [K15, Tobias Stolz-Zwilling, Warhorse PR manager, 3 March 2025]. Another developer interview says there are "many iterative changes to the combat", some to make it easier, some to make it deeper [K16, Martin Ziegler, Warhorse lead scripter, 15 July 2024].

### 2.2 The moves

| Move | What it is | Source and mark |
|---|---|---|
| Directional strike | Four directions (up, down, left, right) for most weapons, three for polearms. The direction is chosen with the mouse and shown on the rose. Guides disagree on which weapon lacks which direction. | K18 wiki, K34 player, K31 press |
| Thrust | The arrow at the bottom of the rose is for stabs. One player says KCD2 has no point-stab; patch notes still speak of "slash or stab" damage for master strikes. Conflict, not resolved. | K18 wiki, K33 player, K9 official |
| Chain | Press attack again while the first swing is still going. | K18 wiki |
| Combo | A set order of directions; the last blow is a special one. Taught by trainers. Patch 1.4 cut every polearm combo to three moves. PCGamesN lists combos of three or four inputs, and three unarmed combos. After each swing the weapon moves by itself to a set next side, which is why some combos need no steering. | K27 press, K11 official, K34 player |
| Feint | Hold attack in one direction, change direction, then release. The foe has less chance to block. | K19 wiki |
| Block | Hold the block key. Costs stamina in proportion to the blow. Enemies can still land techniques on a plain block. | K18 wiki, K28 press |
| Perfect block (parry) | Press block when the green shield shows. Costs no stamina and breaks the foe's chain. | K18 wiki, K28 press |
| Riposte | A counter-blow right after a perfect block. A riposte can only be stopped by another perfect block. It costs stamina. | K18 wiki, K28 press |
| Master strike | A counter from the opposite side at the green shield. Taught by Master Tomcat after a duel. Sword only, say Gamerant and the players; one player says NPCs use it in a fist fight. | K24 press, K31 press, K32 player |
| Dodge | A sidestep that costs stamina (official cost 20, section 2.3). A perfect dodge is timed to the same shield. Beebom says it suits light swords and fists best. | K1 official, K28 press |
| Clinch, lock, grip, throw | Warhorse says "locks, grips and throws" were added so a man can be grappled into submission, and that an unarmed man can disarm an armed one. Patch 1.2 removed, as a fault, the ability to push an opponent out of a fighting pen with the clinch. A perk lets two unarmed men go from a clinch to an arm lock and a chokehold that knocks out. | K5 official, K9 official, K29 press |
| Shove or kick | The first game's codex has a kick that pushes a man away. For KCD2 no page read describes a kick or shove as its own verb; the nearest was a clinch push out of a fighting pen, which patch 1.2 removed as a fault. | K22 wiki (first game), K9 official |
| Fists | Hooks and jabs in the first game's codex. For KCD2, a wiki says a fistfight uses fists and "occasional kicks". | K22 wiki, K18 wiki |
| Tackle | A tackling attack exists (patch 1.2 mentions it). No timing published. | K9 official |

### 2.3 Timings: who measured, and what is official

**Nobody named has measured KCD2's wind-ups or parry windows.** No frame count or seconds figure for a swing, a perfect block or a master strike was found with a stated method. What exists is Warhorse's own rules table, below. It was exported on 14 January 2025, before release (4 February 2025) and before patches 1.2 to 1.5, whose notes record combat changes: multi-hit combo damage raised in 1.2, enemy difficulty rebalanced in 1.3, a polearm perk changed in 1.4 [K9, K10, K11]. Retail values may differ. All rows are from K1 (official), the wiki page "RPG Constants/Params".

| What it is | Official name | Value | Unit |
|---|---|---|---|
| Stamina cost of one attack | BaseAttackStaminaCost | 26 | stamina points |
| Stamina cost of one dodge | BaseDodgeStaminaCost | 20 | stamina points |
| Stamina regained at rest | StamRegenBase | 22 | per second |
| Regain while a block is held or the weapon is raised | StamRegenBlockMod | 0.6 | times the base |
| Regain while moving | StamRegenMoveMod | 0.75 | times the base |
| Stamina lost when a blow is stopped | MinStaminaDamage, MaxStaminaDamage | 15 and 40 | stamina points |
| Share of a swing's stamina taken when the strike begins (the rest while the weapon is raised) | StaminaDrainRatioStriking | 0.7 | share |
| Delay before a held attack starts to charge | AttackChargingBeginCooldown | 0.2 | seconds |
| Time to reach full charge | AttackChargingCooldown | 1.4 | seconds |
| Mean gap between attacks for a defensive AI fighter | CombatAutoMaxAttackDelay | 2 | seconds |
| How the gap grows for each attacker | CombatAutoAttackDelayIncreasePerAttacker | 0.8 | "how many times the period is increased" |
| Spread of that gap | CombatAutoAttackDelaySigma | 4 | seconds ("attack delay variation") |
| Gap shortened when the target is another NPC | CombatAutoNPCOpponentAtkDelayCoef | 0.5 | share |
| Smallest perfect-block slot at the lowest skill | MinPerfectBlockSlot01 | 0.3 | unit not stated |
| Perfect-block window, as a share of the lead time of the attack | MaxPerfectBlockSlotModifier | 0.85 | share |
| Fewest steps in an AI combo | ComboMinSteps | 3 | steps |
| Danger stays on after the last enemy stops being a threat | CombatDangerCooldown | 0.5 | seconds |
| Distance inside which the "active combat" icon is used | CombatActiveNPCRadius | 10 | metres |
| Time an AI hunts a target | CombatAutoMinHuntAttackDuration, CombatAutoMaxHuntAttackDuration | 15 and 60 | seconds |
| Morale needed so an NPC does not flee a fight | MoraleForCombat | 0.2 | scale 0 to 1 |
| Attack from behind counts from this angle, and adds | FromBehindAngle, CombatDmgRBonusFromBehind | 2.356 radians, 1.2 | angle, multiplier |

Derived from those rows (formula shown; none is an official figure):
- At rest one attack's stamina comes back in 26 / 22 = 1.18 s. With a block held it takes 26 / (22 x 0.6) = 1.97 s. A dodge takes 20 / 22 = 0.91 s. (derived)
- 2.356 radians is 135 degrees (2.35619 x 57.2958 = 135.0). (derived)
- If the gap rule is "the period grows by 0.8 of itself for each extra attacker" (a reading by this file, unverified), the gap is 2.0 s for one attacker, 3.6 s each for two, 5.2 s each for three, 6.8 s each for four. The crowd as a whole then swings at about 0.5 to 0.6 times a second whatever its size, before the official 4 s spread is applied (derived from an unverified reading).
- Reading of the perfect-block row: the window is at most 85 percent of the time between the slot opening and the hit, and it widens with the square root of relative skill (the official table gives the exponent 0.5). So a slower attack gives a longer window. This is a reading of a help text, unverified.
- The same table holds chance-weighted AI choices: block, perfect block, master strike and dodge each have a pair of probability values, and combos have step probabilities (names such as CombatPerfectBlockProb1 and ComboNextStepProbHit) [K1]. The AI is not deterministic even though the player's results are.

What the patches say about timing, without numbers [K9 patch 1.2 unless marked]:
- A short delay was added between melee attacks made without lock-on, so that spamming attacks works less well.
- A hit reaction now slows the player, so he cannot "easily back away from attacking enemies".
- Being hit no longer interrupts drawing a weapon.
- Patch 1.4: practice opponents "start practice fights in defense" [K11].

**Numbers from guides that could not be confirmed (unverified, used nowhere):**
- Expert Game Reviews gives a table with a perfect block of 12 to 18 frames (200 to 300 ms) and a master strike of 9 to 12 frames (150 to 200 ms) at 60 fps. It names no measurer and no method, and it says master strike unlocks at combat level 5 from Captain Bernard in Rattay, which contradicts the other guides, which name Master Tomcat [K36].
- LootLore gives a master strike window of about 0.4 s (24 frames at 60 fps), widening to 0.55 s with a perk, and says Warhorse confirmed a 30 percent reduction in a dev blog. No such post was found. It also says the skill unlocks at Defense 8 and works unarmed, which contradicts Gamerant, Seven Swords and the players [K37].
- Both contradict the official table, where the window is a share of each attack's lead time rather than a fixed length (reading above).

Official stat names tell what the system tracks, without values [K2]: the player has slots for perfect block, dodge and combo; a clinch advantage and clinch attack; knock-out and unconsciousness protection; a surrendering state; separate anger from violence and from material loss; reputation that spreads by distance, relation and ancestor. The table list [K3] shows combat data held as zones, guard stances, animation steps and combos.

### 2.4 Stamina

- Official: an attack costs 26, a dodge 20, sprinting 3.5 a second, and a stopped blow takes 15 to 40 [K1]. Wiki: attacking, blocking and sprinting spend stamina; low stamina weakens blows and leaves you open [K18, K21].
- Armour turns blows into stamina loss while stamina lasts, and into health loss when it is gone, so a fully armoured man has to be worn down first [K18 wiki, K22 wiki for the first game].
- Stamina returns "fairly quickly" if you stand still, slower in a fight [K21 wiki]. Official: x0.6 while blocking, x0.75 while moving (table above).
- A wiki states a maximum of 136 stamina. No method; unverified [K21].
- Warhorse's own tip: switching to the sword is faster than reloading a crossbow [K8].

### 2.5 How many enemies attack at once, and how the AI queues them

- **Official.** The rules table has a gap between an AI fighter's attacks (mean 2 s, defensive) and a factor that lengthens the gap for each attacker, with separate smaller factors if the victim is on a horse (0.1) or holds a ranged weapon (0.2) [K1]. A movement-activity value also drops by 0.5 for each additional attacker (the help text is terse) [K1]. That is a spacing rule, not a strict queue of one.
- **Talk.** The 2025 GDC talk by Warhorse's Matej Marko is about NPC behaviour made from goal-planning and modular behaviour trees: the desired state of an NPC is the goal, planning finds the actions [K13, abstract only]. The page does not mention melee. Its video was behind a login limit.
- **Patch.** Patch 1.2 added tutorials "providing hints about fighting multiple opponents" [K9].
- **Players disagree.** One says the others "just come close, gang up on you" while you are locked on to one [K33]. A guide writer says an attack from behind is almost impossible to block or dodge, and advises keeping all enemies in view and only single attacks [K35]. Another poster says to use terrain so they come one at a time [K33]. A search summary of a GameSpot review says enemies are less aggressive and can be taken one at a time; that page was not reached (403) and nothing from it is used.
- **Design reading (this file's, unverified).** With a gap that grows with the crowd, the official numbers look built so that three or four men do not hit three or four times as often. They stay dangerous because the player can lock on to only one.

### 2.6 How fights end

- **Death or knock-out.** Armed fights can kill. Official help text for the unarmed case says health "cannot reach" a knock-out level, value 0 [K1]; a reading by this file is that fists knock out and do not kill (unverified). Patches fixed how kills are counted in the statistics (soldiers count as enemies, not civilians) [K11, K12]. A knock-out is held as an unconsciousness "depth": 480 after a combat hit, used up at 1 per second plus a term for vitality [K1, official names CombatHitUnconsciousDepth, UnconsciousDepthFadeoutSpeedBase]. That is about 480 s before vitality counts (derived; whether game time or real time is not stated, so unverified).
- **Surrender and mercy.** Surrender goes both ways. Patch 1.2 fixed "sometimes missing the chat option to surrender" and the reaction of an NPC "being attacked, but missed, while they're surrendering to the player" [K9]. Patch 1.3 fixed "the combat opponent asking for mercy while performing a combo" and made Cumans met on the road stop surrendering [K10].
- **The first game's rule, which KCD2's patch notes echo in part (Cumans do not surrender).** A beaten man can surrender honourably; the winner may let him go, refuse, or take money or gear as a price. You cannot surrender to bandits or to a mortal enemy. After one surrender to someone you must wait before you can again. Surrender is only possible within a few metres [K22 wiki, first game's codex].
- **Hardcore Mode.** Warhorse's own description: "You won't get surrendering enemies, visual cues in combat" [K6]. So surrender is a switchable assist.
- **Mercy kill.** A separate execution is used on a weakened foe; a patch added the face animation for it [K9]. A wiki says a finisher is used when the enemy's health is low and needs no stealth [K18].
- **Flight and guards.** Running from guards leads to a chase and a "wanted" state; guards attack if you run when confronted [K18, K26]. An NPC with morale under 0.2 flees a fight [K1]. A patch fixed NPCs being "indecisive about bandaging themselves, fighting, or running away" [K9].
- **A fight in the story.** A fight can be a scripted bout (tourney, duel, fist fight) with its own crime rules; patch notes record many fixes where a crime during a bout broke it [K9, K10, K12].

### 2.7 Witnesses, guards, crime and reputation

This ties to KIT.md and coverage-audit-kcd2. The audit built its rows B2, B3, E4 and E5 from search summaries. The pages below were opened: they confirm B2 and E5 and add numbers, the "watchers flee" note touches E4, and B3 (no surviving witness, no record) was neither confirmed nor contradicted.

- **Who reports.** A guard who sees a crime reports it; civilians can report and set off an investigation [K26 press]. A witness can also ask money for silence, in the pre-release preview [K25 press, 16 August 2024]. An NPC about to raise the alarm can be killed before the alarm goes out [K30 press].
- **Where it lives.** KIT.md could not find where KCD2 records witnesses. The official crime page says the crime logic is "mainly in AI Behavioral trees" with a few values in tables [K4]. The rules table holds the perception numbers: a view radius from 2.5 m (an almost blind NPC) to 50 m, a penalty to visibility at night outdoors, 4 s of recognition time for an unremarkable person, and a 4 s decay before NPCs become unaware of you [K1].
- **Evidence.** Being seen near evidence such as a corpse still gets you accused, and evidence left behind puts the guards in that area on high alert, so a return to the scene means questions [K25]. A corpse is hidden from the world 300 s after it is discovered, or 3,600 s if undiscovered (game time) [K1]. Crime entries carry fields named expiration and isSpreadable that the official page does not explain; the example entry for assault shows importance 130 and the violent flag set [K4, shown as an example of the table format].
- **Spreading.** Reputation moves from a person to a faction after 10,800 s of world time (3 hours, derived) plus a random bias of up to 1,800 s, and to nearby factions up to 400 m away at a quarter strength [K1]. When opinions are combined, a person's counts 5, a faction's 3 and a larger group's 1 [K1]. A developer: if you commit a crime across town, the guards there do not know until time has passed; skip 24 hours and the same guard says "aren't you that guy" [K14, Tobias Stolz-Zwilling, 18 December 2024].
- **Unrest.** If a crime goes unsolved, the area gets more watchful and people carry and ready weapons [K14]. A wiki's words: people "become more vigilant, arm themselves", and guards call reinforcements [K18]. Officially, NPCs arm everywhere once anger passes 0.67 [K1].
- **During a fight.** Patch 1.2: NPCs watching a violent event "will now flee if the source of the violence moves too close"; NPCs reacting to violence got "boosted hearing"; the anger of a place from thefts and violence was rebalanced; NPCs seeing through obstacles or behind themselves was fixed [K9]. Distances: the "investigating" icon shows for NPCs up to 100 m away, the "active combat" icon inside 10 m [K1].
- **Punishment ladder.** Fine, talk your way out, run, or accept: pillory, caning, branding, execution (press) [K26]. Warhorse's interview says a hanging is game over [K14]. The audit already notes that accepting punishment wipes your record in that place, which LEDGER must not copy.
- **Developers' own tips.** NPCs can see through an open door and remember it was shut; a stranger in a house is remembered when something goes missing [K8].
- **Behaviour icon.** A hare icon runs from white (suspicion) through yellow (being recognised, with ears that rise) and orange (confronted, or an alarm raised) to red (hostile) [K30 press].

### 2.8 Camera and targeting

- First person [K17, K39].
- Lock-on to one foe with a key; cycle between foes; the camera is locked in combat and a held block frees it [K22 wiki for the first game, K35 player]. A fix made camera clipping with a shield and free-look limits [K9, K12].
- The attack zone is picked by the mouse; zones greyed out cannot be struck [K22 wiki].
- Hardcore Mode hides health and stamina bars and shows "far less visible" combat indicators [K20 wiki, K17]. Patch 1.4 added a setting that shows UI only when relevant [K11].

### 2.9 Where KCD2 touches the content rule

Taverns, drinking, dice games and betting on fist fights exist in KCD2 and its guides [K29, K14]. Nothing about them is used here. Children: not touched.

## 3. Mafia: The Old Country (Mafia TOC)

### 3.1 What it is

Third person, linear, set in Sicily in the early 1900s, Unreal Engine 5, released 8 August 2025 [M10]. Official: "not an open-world game" [M2], and "a focused, linear experience" [M4]. Hangar 13's own framing: "This isn't an era of advanced weaponry or easy brawls" [M2]. Combat has cover shooting, stealth, a knife used for takedowns, and one-on-one knife duels [M22, M10]. Official: even a payment collection "can lead to a standoff at gunpoint or a brutal knife duel", and the tools depend on the task [M9]. Metacritic 73 on all three platforms [M10]. KIT.md found no Hangar 13 talk; one exists (the PAX East 2025 panel), but it is a video that could not be read, so Popverse's report of it is used [M7].

### 3.2 Knife duels

- **What a duel is.** Hangar 13's president Nick Baynes at PAX East 2025: the knife is "more than just a one-shot kill"; a new knife-dueling mode puts you against a boss character, one on one, to the death (the report words this with a typo, so it is not quoted) [M7, press report of the panel]. The game director calls them lethal encounters that "unfold at pivotal moments in the story" [M5, official, 8 May 2025].
- **Inputs.** Five actions only: slash, thrust, strike, dodge, parry. No other action is possible during a duel [M22 press]. On PC: strike right mouse, thrust middle mouse, slash left mouse, parry left shift, dodge space, steer with WASD [M12 press].
- **Rhythm.** Official: "the timing windows for different inputs (dodge, parry, etc.) are unique", button-mashing "won't get Enzo very far", listen for audio cues and "watch for red glints indicating unparryable attacks that must be dodged" [M1]. Guides: a normal attack is parried; a heavy strike with a red glint cannot be, so you dodge and counter; your own strike breaks a guard, then you follow with slashes or thrusts [M13, M14]. Parry is called generous [M13]. A foe is open for a short time after its own dodge; slashes have a wider hit area than thrusts [M12]. Each opponent has its own timing for strong attacks [M12].
- **Shape of a boss duel.** Guides describe two phases: rapid slashes first, then unparryable strikes from about half health, and quick-time prompts at about 50 percent and 0 percent health; a late prompt lets the boss regain 25 percent [M14]. These are guide claims. A German press piece describes the duels as a matter of quick reflexes, dodging or striking at the right moment [M26].
- **Tutorial.** A sparring duel with a blunt blade; three parries are needed to advance [M14, M21].
- **Knives.** Three types: one throwable, one that allows one-hit kills in active combat, one with the best durability [M1]. Only one knife is carried; durability is spent by lockpicking, quick stealth kills, throws and one-hit kills; whetstones restore it; the plain melee attack always works and "isn't as quick or stealthy as a silent takedown" but is lethal [M3]. In duels the knife type does not change damage [M12].
- **Frames or seconds.** Not published. A search summary of a guide says "about a second" to parry; that page was not reached (403) and nothing from it is used.

### 3.3 Brawls and fists

- Hand-to-hand fighting as a system: not published. Hangar 13 shows "freeform melee attacks you can employ in any combat encounter" [M6, official, 22 July 2025], with no inputs or timings. One critic says "You won't be using your fists in the Sicilian underworld" [M20, press]. Hangar 13's own words are that this "isn't an era of ... easy brawls" [M2].
- A knife melee attack exists outside duels and is always available [M3].

### 3.4 Takedowns and stealth

- **Bare hands.** Approach crouched, in the target's blind spot, hold the grab and press the prompted button repeatedly to choke him out. The guide: "this takes time, and if another enemy appears nearby, he will spot you" [M15 press].
- **Knife.** A quick lethal stab from behind, faster than choking, at the cost of knife durability [M15, M3]. A throwing knife kills from range and has to be collected [M1].
- **Distraction.** Throw a coin or a bottle. The guides differ: one says the nearest enemy comes, not necessarily the one you meant [M15]; another says every guard close enough to hear investigates [M16].
- **Bodies.** Official tip: stash bodies, "which will prevent guards from being alerted by the sight of a corpse" [M1]. Drag a body out of a patrol route or into a crate [M15, M17].
- **Detection.** Enemies "spot you from a long distance" and move to where they saw you even if not fully alerted [M15]. Some sequences require staying undetected; most do not [M3].
- **Instinct.** A mode that shows enemies through walls [M1, M6].
- **Timings of takedowns:** not published.

### 3.5 What bystanders do

Not published. No page read describes civilians, witnesses or police reacting to a fight in the main story. The game is linear and its stealth is about guards. The 2K Free Ride update lists timed combat challenges against waves and assassinations, with no civilians mentioned [M25].

### 3.6 How it holds up over a whole game

GameScreed: the fights "don't change much throughout the game and get boring very quickly" [M19]. CrimeNet Gazette: another blade "starts feeling contractual" [M18]. Impulse Gamer calls the duels cinematic and a highlight that "didn't overstay their welcome" [M20]. GameIndustry: duels are story-based and not skippable, "one of the most challenging parts" [M21]. PC Gamer scored it 45 out of 100, Game Informer 6 of 10 (the Wikipedia table) [M10].

### 3.7 Accessibility

Official: "Simplified Struggle (automatically completes rapid-button-press inputs)", three difficulty levels, adjustable HUD scale, aim assist options [M3].

### 3.8 Where Mafia touches the content rule

Hangar 13's blog mentions the family's wine in a villa video [M6]. It is not used. No children, gambling or drink feature in the fighting pages read.

## 4. The comparison with game-design/combat-spec.md

The verdict says what LEDGER should do with the games' practice for that point, not whether the spec is right. ADOPT: take it as it is. ADAPT: take the idea, change the form. IGNORE: leave it. "Not published" means no page read says. The reason quotes the spec or Jafar's answers, or Combat.cs where marked.

**Note added 13 October (not reviewed):** Jafar's rulings of 12 October outrank the July spec where they differ; the rulings section near the top lists the rows they supersede (3, 4, 7 to 12, 13, 27, 31, 37 and 42, in whole or in part), and this table stays as the record.

| # | Spec point | KCD2 | Mafia TOC | Verdict | Reason |
|---|---|---|---|---|---|
| 1 | Filter: "Violence is seen" | Witnesses report or confront; reputation spreads at a stated delay; violence makes a region more watchful; watchers flee if it comes close [K14, K1, K9] | Not published for fights; a second enemy who comes near spots a choke, and a visible corpse alerts guards [M15, M1] | ADOPT | Spec section 1 makes witnesses the cost; KCD2 builds consequence from witnesses and LEDGER's seven slots go finer |
| 2 | Not a win condition: killing a witness works, the second problem is larger | Killing the would-be reporter stops the alarm [K30], but a corpse near you still gets you accused [K25] and fades after 300 or 3,600 s [K1] | Not published | ADAPT | Keep "works, evidence remains"; drop the corpse timer, since spec 7b says none of the containment tools "touch a corpse" |
| 3 | Not empowering: Tom is "not a fighter" | Weak at the start [K27], outnumbered is deadly [K33], but skills grow and one player says "unstoppable by halfway" [K33] | Enzo is a "coiled spring" who scrapes for weapons [M7]; scarce ammunition [M8] | ADAPT | Keep "not a superhero"; drop growth, since D11 forbids stats and spec says "if the player feels good at fighting, the fiction ... break" |
| 4 | Not frequent: "a handful of fights" | Fights, tourneys and bandit events recur; no count published | Duels come at the end of each chapter [M19]; critics call them repetitive [M19, M18], one disagrees [M20] | IGNORE | Spec target is a handful per playthrough; both games run far more and Mafia's critics are the warning |
| 5 | Not free: witnesses, lasting injury, treatment, feud | Health does not heal itself, bleeding loses 1 HP per 6 s, crimes bring fines or branding, gear wears [K18, K1, K26] | Health regenerates; knife durability; no social cost published [M25, M3] | ADOPT | Spec: "Every swing has a cost even when you win"; KCD2 charges body, gear and standing |
| 6 | Not a separate mode: no arena, no lock-on state, no sting | Lock-on rose, a hare icon with crossed swords in direct combat, music and UI hint at combat (a fix mentions them) [K18, K30, K10] | A separate one-on-one mode with five actions [M7, M22] | IGNORE | Spec: "No arena, no lock-on state you enter and exit, no music sting" |
| 7 | Verb: Square up (a stance everyone sees) | No stance verb; drawing a weapon makes NPCs confront; above anger 0.67 NPCs arm everywhere [K1, K9] | Enzo "boldly draws his knife to challenge foes" [M6]; duel start is scripted [M5] | ADAPT | Spec: "Witnesses start paying attention BEFORE anything lands"; both show a visible commitment, LEDGER's is a stance with fists |
| 8 | Verb: Strike (slow, telegraphed, heavy; a miss hurts you more) | Four-direction swing, chain, cost 26, spam delay, charge up to 1.4 s [K1, K18, K9] | Slash, thrust, red-glint heavy strike, audio cues [M1, M13] | ADAPT | Spec: "A small verb set ... beats a large one where the player mashes"; take one-cost swing and sight-and-sound tell, drop directions and combos |
| 9 | Verb: Shove (distance, non-injuring, de-escalation) | Clinch with "locks, grips and throws" [K5]; a clinch push out of a fighting pen was removed as a fault in patch 1.2 [K9]; kick in the first game [K22] | Not published | ADAPT | Spec: "Cheap, non-injuring"; KCD2's clinch is a weapon lock, LEDGER's is a two-hand push that makes space |
| 10 | Verb: Guard (absorb; cannot guard forever) | Block drains stamina with the blow, regain x0.6; perfect block free; armour turns hits into stamina loss [K18, K1, K28] | Parry and dodge; no held guard published; foes guard and can be guard-broken [M13] | ADAPT | Spec: "Absorb rather than avoid"; take stamina drain and slower regain, drop the perfect-block prize |
| 11 | Verb: Back off ("the game should say so") | Developers' tip: "consider a tactical retreat" [K8]; fleeing draws a chase [K26] | No retreat inside a duel [M22] | ADOPT | Spec: "explicitly viable"; Warhorse's own tips say the same |
| 12 | Finishing a downed man, as a decision afterwards | A separate mercy kill on a weak foe [K18, K9]; knock-out is the alternative | Quick-time kills inside the duel; one-hit knife kills mid-fight [M14, M3] | ADAPT | Spec: "never ... in the flow of a scuffle"; KCD2's separate act fits, Mafia's in-flow kills do not |
| 13 | Guns out of scope | Crossbows and early firearms are slow, and a firearm can explode in the hand [K5, K7, K8] | Guns central; "every bullet counts" [M5] | IGNORE | Spec: "Guns are out of scope"; RULINGS: firearms rare; KCD2's slow, fragile gun is the model if they return |
| 14 | No health bar, damage numbers or hit markers | Bars shown; Hardcore hides them and cuts cues; UI only when relevant [K20, K17, K11] | HUD scale option; combat bars not described [M3] | ADAPT | Spec: "No health bar"; Hardcore shows it can ship, LEDGER's is the default and keeps the data (spec 7c) |
| 15 | Your condition on your body | Low stamina weakens blows; controller feedback for low stamina [K18, K11] | Not published | ADAPT | Spec: "breathing that gets ragged, a guard that drops"; KCD2 uses haptics, LEDGER uses the body |
| 16 | Their condition on theirs | NPCs bandage, flee or fight by state; low-health behaviour from 40 percent [K9, K1] | Not published; bosses regain health after a missed prompt [M14] | ADOPT | Spec: "how they hold the injured side"; KCD2 shows hurt people acting hurt |
| 17 | Threat read from the world (three seconds of staring) | Hare icon: suspicion, detection, warning, threat [K30] | Instinct shows enemies through walls [M1] | ADAPT | Spec: "Somebody who is about to swing has been staring"; both use a HUD aid, LEDGER's must be gaze and stance |
| 18 | Contextual prompt: fading, forgiving, buffered | Green shield and riposte icon; UI only when relevant [K28, K11] | In-game tutorials and mid-fight feedback [M1] | ADAPT | Spec: prompt "appears the way the talk prompt does"; keep learn-by-doing |
| 19 | Telegraph, not tell | Weapon position shows direction, the shield tells the moment [K27, K28] | Red glint and sound; unique window per input [M1] | ADAPT | Spec: "Every incoming strike has a readable wind-up"; take glint and sound, drop icons |
| 20 | Sound carries most of it | Patches fix missing attack, hit, battle-cry and clinch sounds [K9] | "Listen for critical audio cues" [M1] | ADOPT | Spec: "Sound carries most of it" |
| 21 | The audience: cost shown in Mickey's book or a line | Arrest dialogue lists your crimes; a reputation tab, kept per town and faction [K9, K18, K26] | Not published | ADAPT | Spec: "not a toast"; KCD2's list is a menu, LEDGER's is diegetic |
| 22 | Accessibility: longer telegraph, auto-resolve | Windows widen with skill [K22, K1]; fans built a mod to widen them within ten days of release [K38] | "Simplified Struggle" completes rapid presses; three difficulties [M3] | ADAPT | Spec: "the same fight at a different tempo"; Mafia's auto-complete is the model, KCD2's skill growth is not (no stats) |
| 23 | Minimal HUD later as a toggle (7c) | Hardcore and "UI only when relevant" are options [K6, K11] | Adjustable HUD [M1, M3] | ADOPT | Spec 7c: "a settings toggle rather than a rewrite" |
| 24 | Resolve has no randomness | Mastery "rather than an unseen roll" [K5]; AI picks are chance weighted [K1]; stealth kills can fail [K9] | Not published | ADAPT | Combat.cs: "No randomness: a fight the player cannot read is a fight they cannot learn"; player outcomes fixed, AI variety seeded |
| 25 | Reach 1.6 m: no hit at range | Not published (only a from-behind angle of 135 degrees with x1.2) [K1] | Not published | IGNORE | Nothing to take; Combat.cs: a hit at four metres is "the fastest way to lose a player's trust" |
| 26 | Stamina must matter; mashing gasses out | Swing costs 26, regain 22 per second: 1.18 s per swing at rest (derived); a spam delay was added by patch [K1, K9] | Button-mashing "won't get Enzo very far" [M1] | ADAPT | Spec lab: mashing won 76 percent until retuned; KCD2 needed a patch for the same flaw; LEDGER's regains far slower (0.34 cost, 0.09 per second, 3.8 s per swing, derived) |
| 27 | A fight is three to four swings; winning costs | Armoured fights are long stamina contests, unarmoured men fall fast [K18] | Two-phase duels; length not published [M14] | ADAPT | Spec: "Even the best line wins a quarter of the time"; LEDGER's men in coats match KCD2's unarmoured case |
| 28 | Witness rules: from how far, through what; alley at night vs noon | Night lowers visibility (a penalty of 0.7 outdoors); hearing boosted for violence; seeing through walls fixed; investigators shown to 100 m [K1, K9] | Enemies spot from far and investigate; bodies stashed [M15, M1] | ADAPT | Spec phase 2: "Fighting in an alley at night is genuinely different"; LEDGER's Observation is finer |
| 29 | A killing brings police (a new pressure track) | Ladder from fine to execution; unrest makes guards call in help; area more watchful even without proof [K26, K18, K14] | Not published | ADOPT | Spec 7b: "It brings police"; the audit's E5 asked for the town to change its behaviour |
| 30 | Who swings first: both | NPC anger from violence and from being robbed exists; the player can strike anyone [K2, K4] | Scripted | ADOPT | Jafar: "violence is a part of our crime world and a legit tool" |
| 31 | Lethality: yes, rarely and permanently | Fists knock out (a reading); killing innocents is a crime; hanging ends the game [K1, K26, K14] | Duels are to the death, scripted [M7] | ADAPT | Jafar: "Yes, rarely and permanently"; fists as knock-out fits "finishing" being a separate act |
| 32 | A body is a fact that cannot be discredited | Corpse hidden after 300 or 3,600 s; crime memory expires [K1, K4] | A seen corpse alerts guards until hidden [M1] | IGNORE | Spec 7b: no discredit or decay "touch a corpse"; both games let evidence fade or be hidden |
| 33 | A killing solves the immediate problem completely | Kill the reporter and no alarm [K30] | Hide the body and nobody is alerted [M1] | ADOPT | Spec 7b: be "honest about this or the choice is fake" |
| 34 | Who else saw | A witness reports at once; civilians too [K26] | A nearby second enemy spots you [M15] | ADOPT | Spec 7b: killing one witness of three "is the mechanism by which this spirals" |
| 35 | The crew know; nobody who saw is the same | Per-person reputation weighs 5, faction 3, group 1 [K1]; one quest note stops friendly NPCs reporting [K11] | Not published | ADAPT | Spec 7b: "Nobody who saw it is ever quite the same about you"; LEDGER already holds loyalty |
| 36 | Rare and permanent; a playthrough without killing | The player can knock out instead of killing [K18] | Duels to the death cannot be skipped [M21] | ADAPT | Spec 7b: "possible to complete a whole playthrough having never done it"; Mafia's forced duels are the opposite |
| 37 | Camera rig and momentum: weight and readability | First person, lock-on, free look while blocking, hit reaction slows the player [K17, K35, K9] | Third person; hit-pause not published [M10] | ADAPT | Spec 5: "Weight and readability"; take the hit-reaction slow-down, keep LEDGER's third-person camera with no lock-on |
| 38 | An enemy AI that can telegraph and react | 2 s mean gap, longer per attacker; practice foes start in defence [K1, K11] | Boss phases; own strong-attack timing per boss [M14, M12] | ADOPT | Spec 5: "an enemy AI that can telegraph and react"; both give concrete rhythms |
| 39 | Injuries persist and heal on a schedule | Bleeding 1 HP per 6 s; injury fades 1 percent per 20 s; health does not heal itself [K1, K18] | Health regenerates; Classic difficulty makes it sparse [M25] | ADAPT | Spec 0: "Injuries persist and heal on a schedule"; KCD2's run in game seconds, LEDGER's in days |
| 40 | The stagger model (Bumps) | A hit reaction slows the player; a too-long knock-back was fixed as a bug [K9] | A parry staggers the foe [M14] | ADAPT | Spec 5 lists Bumps for "Contact classification and stagger"; cap distances as Bumps does (0.55 m) |
| 41 | Footing: Down, cannot act, can be finished | Knocked-out men stay unconscious while a depth value fades; unconscious men no longer idle [K1, K12] | Not published | ADAPT | Combat.cs: Down is "On the ground. Cannot act; can be finished"; KCD2's timed unconsciousness gives the way back up |
| 42 | The risk: combat ruins the game; stop if it distracts | Combat is a loud complaint among players [K33]; a critic finds it "overly reliant on parry & riposte" [K23]; Warhorse made it "more accessible" [K16, K15] | Critics: repetitive, "contractual" [M19, M18]; PC Gamer 45 of 100 [M10] | ADOPT | Spec 8: "the correct decision is to stop there and leave violence as something that happens TO you" |

Notes on the table:
- The rows cover every verb (six, with finishing), every "must not be" (five), the interface rules, the plan points from sections 5 and 6, Jafar's answers, the body rules of 7b and the risk of section 8.
- Not copied, because RULINGS, canon or the coverage audit rule them out: KCD2's stats, perks, skills that rise with use, jump, horses, hunger, alcohol, dice and betting; Mafia's driving, cover shooting and quick-time bouts. RULINGS "What the game is" lists no jump, fists and improvised weapons, firearms rare (23 September, genre) and no stats (D11). No health bar is the spec's own rule (combat-spec section 4), not a ruling.
- Ideas from the games that are not in the spec and could be raised later: a hit from behind that counts more (KCD2 official, x1.2 from 135 degrees); hiding a body to delay its finding (Mafia's stash points); NPCs that flee a fight when it moves close to them (KCD2 patch 1.2).

## 5. DRAFT TARGET LIST for combat-spec phase 3

**Adjusted 13 October, not reviewed.** The spec this list was written for is replaced by Jafar's design. The list's job is the same: it is the first test's brief. Entries A01 to E03 and items 1 to 9 stand. Section 5.6 adds 15 entries (2 for the first test), runs 5 to 10 and items 10 to 17, in the design's build order.

**Status: DRAFT.** Phase 3 in the spec is "Bodies and telegraphs. Animation, the read, hit reactions, the guard", blocked on characters. This list is what a first test needs. It names targets and timings, not clips. Where the clips come from (MetaHuman movement clips and Mixamo, per RULINGS 3 October; the project's own capture would need a new ruling and an allowlist record first) is not decided here. All names are the project's own and carry no drink, gambling or child words, so they should pass the clip-name walk of tools/content-gate.py (to be run when the clips exist).

### 5.1 How the numbers were made

- One frame is 1/30 s. Each timing is marked: game (from a published game number), standard (a public convention), judgement (this file's own), derived (arithmetic).
- Standard: fighting-game frame data splits a move into startup (to the first hitting frame), active frames and recovery [S1]. The same page says fighting games run at 60 fps, so one of their frames is 1/60 s; the frames in this list are 1/30 s.
- Standard: simple human reaction to a visual signal is about 190 ms for college-age people, and "on the order of 200 ms" generally [S2]. Choosing between three answers (guard, shove, back off) and pressing a key takes longer; that part is judgement.
- Game: KCD2's official numbers give a mean 2 s between a careful AI fighter's attacks and 0.2 s before a held attack starts to charge [K1]. They give no wind-up length for a plain swing. No Mafia number exists.
- The repository's own constants: reach 1.6 m and shove reach 1.9 m (Combat.cs); a stumble is at most 0.55 m (Bumps.Stagger in Interaction.cs); VerbBeat's default wind-up is 0.18 s (Interaction.cs). That default is below the 0.19 s reaction time in [S2], so a strike left at it could not be read.
- The wind-up, derived with judgement: 0.19 s simple reaction, seeing a signal and pressing one key (standard) + 0.35 s more to choose among three answers (judgement) + 0.10 s for the guard to come live (E01) = 0.64 s, rounded up to 20 frames (0.667 s; 0.64 s is 19.2 frames). Range 0.50 to 0.80 s. Contact comes 2 frames later, at 0.733 s, so a guard pressed at 0.54 s is live 0.09 s (between 2 and 3 frames) before the blow lands.
- Telegraph setting (spec section 4, "a longer telegraph window"): the wind-up is multiplied by 1.5 and nothing else changes. 20 frames become 30 and every later key frame moves by 10.

### 5.2 The list at a glance

| Id | Name | Length | Frames at 30 fps | Key frames | Timing source |
|---|---|---|---|---|---|
| A01 | square-up enter | 0.70 s | 21 | stance visible f6 | judgement |
| A02 | square-up hold (loop) | 2.0 s | 60 | loop seam f60 | judgement; spec says a swinger stares for 3 s |
| A03 | stand-down step | 0.90 s | 27 | hands down f6, step f14 | judgement |
| B01 | strike, lands | 1.33 s | 40 | wind-up end f20, contact f22, recovery starts f28 | judgement on a standard |
| B02 | strike, misses | 1.93 s | 58 | wind-up end f20, would-be contact f22, recovery starts f32 | judgement |
| C01 | shove | 0.80 s | 24 | wind-up end f8, contact f10, recovery starts f14 | judgement |
| D01 | shoved, steady | 0.83 s | 25 | 1.2 m reached f15 | judgement (the distance is derived from repository constants) |
| D02 | shoved while reeling, falls | 1.00 s | 30 | ground f14 | judgement |
| D03 | struck, steady | 0.60 s | 18 | head snap ends f4, step ends f10 | judgement |
| D04 | struck, reeling | 1.00 s | 30 | 0.55 m reached f15 | judgement (the distance is derived from repository constants) |
| D05 | reeling (loop) | 1.5 s | 45 | loop seam f45 | judgement |
| D06 | struck, knocked down | 1.50 s | 45 | ground f16 | judgement |
| D07 | down (loop) | 3.0 s | 90 | loop seam f90 | judgement |
| D08 | getting up | 3.0 s | 90 | hands and knees f30, kneeling f60 | judgement |
| E01 | guard raise | 0.17 s | 5 | guard live f3 | judgement |
| E02 | guard hold (loop) | 1.5 s | 45 | loop seam f45 | judgement |
| E03 | guard takes a blow | 0.50 s | 15 | impact f2 | judgement |

Seventeen entries. Both men use the same clips; only the camera differs for Tom Nowak.

### 5.3 The entries

Each entry: start pose, end pose, length and key frames with their source mark, blends, what it causes, sound, camera, what witnesses register and when. In every D entry, frame 0 is the frame after the contact frame of the clip that caused it. Blend lengths are in frames at 30 fps and are judgement. Sounds are the project's own recordings or CC0 (RULINGS D26), never from a game. "Seen" and "heard" use the repository's perception rules: seven slots (precursor, draw, act, victim, actor, flight, aftermath, from weapons-spec section 4.1) and the shout-range sound carry (Violence.SeenFrom is Acoustics.ShoutCarry).

**A01 square-up enter.** Start: standing or walking idle. End: feet a shoulder apart with the lead foot toward the other man, knees soft, hands up at chest height, chin tucked, weight forward. 21 frames (0.70 s), range 0.5 to 1.0 s, judgement. Stance visible at f6 (0.20 s), when the shoulders turn and the hands rise. Blends from walk or idle over 5 frames; to A02. Causes: nothing; it is not an attack. Sound: foot scuff at f4, cloth at f6, breath in at f8. Camera: none; no mode change (spec section 2). Witnesses: the precursor slot fills at f6 for anyone with sight of the stance; "witnesses start paying attention before anything lands" (spec section 3).

**A02 square-up hold (loop).** Start and end: the A01 end pose with a slow weight shift and chest breathing, rate tied to the body's breath rate (Rig.BreathRate in Rig.cs: 0.25 breaths a second at rest, 0.75 when spent, at most 0.93 when spent and hurt). 60 frames (2.0 s) loop, judgement. Blends from A01, B01, B02, C01, D01, D03, D05, E02; to B01, C01, E01, A03. Sound: breath. Camera: none. Witnesses: the precursor continues. An NPC swings only after at least 3 s of holding it (spec section 4: "has been staring for three seconds").

**A03 stand-down step.** Start: A02 pose. End: hands low, one step back, shoulders turned away. 27 frames (0.90 s), judgement. Hands down at f6 (0.20 s), step planted at f14. Displacement 0.8 m. Blends from A02 or E02 over 3 frames; to walk over 5 frames. Sound: step, breath out. Camera: none. Witnesses: at f6 the precursor ends ("he stood down"); this is the best option "and the game should say so" (spec section 3). No act is recorded.

**B01 strike, lands.** Start: A02 pose. Wind-up: weight to the back foot, right fist cocked behind the ear, torso twisted away, breath in. Contact: a heavy overhand at head height. End: follow-through, then a half-step and guard up. 40 frames (1.33 s). Wind-up end f20 (0.667 s), range 0.50 to 0.80 s (judgement on a standard, section 5.1). Contact f22 (0.733 s), with 3 active frames (f22 to f24, judgement; "first hitting frame" convention from [S1]). Recovery starts f28; free to act at f40, which is 0.60 s after contact (judgement). A strike by the same man is not started again for 2.0 s on average, spread plus or minus 0.5 s (game: KCD2 official mean gap. KCD2's own table gives a far wider spread, 4 s, CombatAutoAttackDelaySigma [K1]; LEDGER's narrow spread is judgement, chosen so the rhythm can be learned). Blends from A02 over 4 frames; to A02 over 5 frames. Causes: a hit reaction by the target's footing: steady, D03 (0.25 m stagger, 0.33 s); reeling, D04 (0.55 m, 0.5 s); would be floored, D06 (falls, ground at 0.53 s, ends 0.6 m from where he stood). Through a guard, E03. Sound: breath in at f3, cloth swish f18 to f22, thud at f22, grunt at f24. Camera: hit-pause of 2 frames (0.067 s) on both men at f22 (judgement; Dustloop confirms hit-stop exists as a concept, its length differs by game [S1]); for Tom's camera a 1.5 degree nudge toward the blow settling over 0.4 s (judgement; spec: "a camera that drifts and settles harder"). Witnesses: at f22 the act and victim slots fill for anyone in sight; the thud carries to shout range; the actor slot fills only if the identification ladder allows. Aftermath fills when the target is down (D06, D07). The act is recorded in the harm book.

**B02 strike, misses.** As B01 to f22; the fist meets nothing. Then overbalance: torso swings past, one stumbling step forward 0.4 m by f32, then recovery. 58 frames (1.93 s); recovery starts f32; free to act at f58, which is 1.2 s after the would-be contact, twice B01's 0.6 s (judgement; spec: "misses hurt you more than them"). Blends and sound as B01 without the thud; a breath out of effort at f26. Causes: none; the target's reaction is a flinch or a step back of its own. Camera: no hit-pause; Tom's camera lurches forward slightly (judgement). Witnesses: the act slot fills at f22 with no victim: "he swung at him".

**C01 shove.** Start: A02 pose or standing, facing. Wind-up: both hands drawn to the chest. Contact: palms drive into the target's chest, rear foot pushing, lean 10 to 15 degrees. End: arms out then lowered, balance regained. 24 frames (0.80 s). Wind-up end f8 (0.267 s), range 0.20 to 0.35 s; contact f10 (0.333 s); recovery starts f14; free at f24 (judgement). Faster than the strike on purpose: 0.267 s is barely above the 0.19 s simple reaction time (standard), so a shove can be seen but hardly answered. It is cheap, and it is not a duel move. Blends from A02 over 3 frames; to A02 over 4 frames. Causes: D01 if the target is steady, D02 if he is reeling (as Combat.cs floors a reeling man on a shove). No injury. Sound: palms on coat at f10, breath out. Camera: no hit-pause; a 1 degree push (judgement). Witnesses: at f10 the shove registers as a Bumps shove, which holds the watchers' attention for 4.0 s (Bumps.AttentionSeconds). Act slot only, a quiet act. A shove does not make a victim record in the harm book.

**D01 shoved, steady.** Start: any stance. End: back in A02 pose, hands up. 25 frames (0.83 s). Two quick backward steps; displacement 1.2 m reached at f15 (0.5 s), then 10 frames to find balance. Blends from A02, E02 or a strike's recovery over 2 frames; to A02 over 5. Derived: the men stand about 0.8 m apart at contact (judgement), so 0.8 + 1.2 = 2.0 m, past shove reach (1.9 m) and past strike reach (1.6 m), which is the spec's "create distance". It is more than twice the 0.55 m stumble cap on purpose, because a shove is meant to move a man. Causes: nothing further. Sound: two shoe scrapes (f4, f9), breath. Camera: none. Witnesses: the victim's stagger is the visible part of the act slot.

**D02 shoved while reeling, falls.** Start: D05 pose. End: on his back or seat. 30 frames (1.0 s). Pushed 1.4 m, feet go at f6, ground contact at f14 (0.47 s), then settles into D07. Judgement. Blends from D05 over 2 frames; to D07 over 4. Causes: footing becomes Down (Combat.cs). Sound: scrape, a dull body fall on the pavement at f14, breath knocked out at f15. Camera: a 2 degree drop and settle (judgement). Witnesses: aftermath begins at f14: "a man is down". Watchers may investigate or raise the alarm (weapons-spec section 8).

**D03 struck, steady.** Start: any stance. End: back in stance, a little lower. 18 frames (0.60 s). Head snaps for 4 frames, half-step of 0.25 m by f10, hand to the face, stance regained at f18. Judgement; stays under the 0.55 m stumble cap. Blends from any stance over 2 frames; to A02 over 5. Causes: footing stays steady. Sound: grunt, shoe scuff. Camera: none beyond B01's. Witnesses: nothing new.

**D04 struck, reeling.** Start: D03, D05 or stance. End: hunched, hand to the face, guard low (D05's pose). 30 frames (1.0 s). Two half-steps and a lurch, 0.55 m reached at f15 (0.5 s). Derived: equal to the Bumps stagger cap. Blends from D03, D05 or any stance over 3 frames; to D05 over 5. Causes: footing reeling; guard drops (Combat.cs: Reeling means "Guard is dropping"). Sound: a heavy grunt, a wet breath, shoes. Camera: none. Witnesses: the injured side shows (HarmBook.LooksLike has never been displayed).

**D05 reeling (loop).** Pose: swaying, one hand to the face, ragged breath, chin up. 45 frames (1.5 s) loop, judgement. Blends from D04 and D08; to D02, D04, D06, E02, A02. Footing reeling. Sound: breath at the ragged rate. Camera: none. Witnesses: his state reads as hurt.

**D06 struck, knocked down.** Start: D04 or D05 pose. End: on the ground on his side, one hand on his head. 45 frames (1.5 s). Knees go in 8 frames, falls sideways, ground at f16 (0.53 s), 0.6 m from where he stood, then settles. Judgement. Blends from D04 or D05 over 3 frames; to D07 over 5. Causes: footing down. Sound: a gasp, a body fall at f16, a scrape of a hand on stone. Camera: on Tom's camera a 2 degree settle (judgement). Witnesses: aftermath begins at f16; the victim and a body on the ground are the strongest cue the mill can read.

**D07 down (loop).** Pose: on his side, knees drawn, hand to the head, breathing. 90 frames (3.0 s) loop, judgement. Blends from D06 or D02; to D08. Footing down: cannot act; can be finished (Combat.cs). The finishing verb is not in this first test. Sound: breath. Camera: none. Witnesses: aftermath persists.

**D08 getting up.** Start: D07 pose. End: standing, hand on knee, reeling pose. 90 frames (3.0 s): hands and knees by f30, kneeling by f60, standing by f90. Judgement. Blends from D07 over 5 frames; to D05 over 5. Needed only if the test lets a downed man rise; the spec does not say. Sound: breath, a shoe on stone. Camera: none. Witnesses: a man standing up again is not a new event.

**E01 guard raise.** Start: A02 pose. End: forearms up over face and ribs, chin down. 5 frames (0.17 s), guard live at f3 (0.10 s). Judgement: the guard must be live well inside the wind-up. Blends from A02 over 2 frames; to E02. Causes: nothing. Sound: cloth. Camera: none. Witnesses: a defensive posture, no slot.

**E02 guard hold (loop).** Pose: arms up, shoulders hunched, forearms sinking slowly as stamina falls: up to 15 cm lower as stamina goes from 1.0 to 0.3 (judgement; spec: "a guard that drops as you tire"). 45 frames (1.5 s) loop. Blends from E01 and E03; to E03, A02 or A03. A held guard becomes a grab in the full spec; not in this test. Sound: breath. Camera: none. Witnesses: none.

**E03 guard takes a blow.** Start: E02 pose. End: E02 pose with the guard knocked slightly open. 15 frames (0.50 s). Impact at f2, slide back 0.2 m, then reset. Judgement. Blends from E02 over 2 frames; to E02 over 4. Causes: through a guard the blow does 0.22 of its force (Combat.cs), so the footing normally stays steady. Sound: a blow on forearms, grunt. Camera: a 0.5 degree nudge. Witnesses: the act slot fills as in B01.

### 5.4 The first test, and what it measures to pass

The scene: Tom Nowak and a second man, on the built Quay Street, packaged build, day and night. Four short runs, each with both men in shot.
- Run 1, the read. The second man squares up (A01) and holds for 3 s or more (A02), then strikes (B01). Tom guards (E01, E03) in one take and backs off (A03) in another.
- Run 2, the shove. Tom shoves a steady second man (C01, D01); the pair ends more than 1.9 m apart.
- Run 3, the strikes. Tom strikes the second man four times, 2.0 s apart (the KCD2 mean gap), standing still between blows. Derived from the Combat.cs constants and the order Combat.Resolve works in (the swing's cost of 0.34 is paid first, then the blow's power is 0.55 + 0.45 x the stamina left; stamina back 0.09 a second; floor 2.8, reeling from 55 percent of it, 1.54; an unguarded man at full capability): the running totals are 0.847, 1.622, 2.325 and 2.956 punishment, so the man is steady after blow 1 (D03), reeling after blow 2 (D04, then D05 between blows), still reeling after blow 3 (D04 again, 0.475 short of the floor), and down on blow 4 (D06, then D07). However far apart the swings, an unguarded man at full capability needs four blows: three fully rested blows add only 2.541. A shove on him while reeling puts him down at once (C01, D02). One run uses a miss (B02) because the second man stepped back.
- Nothing in the test kills anyone.

It passes when all of these hold. The thresholds are judgement unless marked.

1. **Timing.** Every key frame in 5.2 is within one frame (0.033 s) of the table in 10 of 10 runs, read from the clip's own markers and checked against a 30 fps recording.
2. **Readable.** A fresh reviewer (not the builder; CLAUDE.md's gate), shown the strike from the street camera at 3 m and at 8 m, says "he is about to hit" before the contact frame in at least 9 of 10 showings, and tells a shove from a punch in 10 of 10.
3. **Answerable.** A scripted player who presses guard 0.54 s after the wind-up starts (0.19 s standard plus 0.35 s judgement; the press lands on f17, 0.567 s, the first frame after it) has the guard live by f20 (0.667 s, E01's f3), at least 2 frames (0.067 s) before contact at f22 (0.733 s).
4. **Distances.** A shove ends with the two men more than 1.9 m apart in every run on level ground, from a start at least 0.8 m apart, with the shoved man moved 1.15 m to 1.35 m. A strike moves a steady man 0.25 m, a reeling man no more than 0.55 m, a floored man ends within 0.15 m of 0.6 m from where he stood.
5. **Footing and clip agree.** With Combat.Resolve, run 3 gives D03, D04, D04, D06 in that order (blows 1 to 4); a shove on a reeling man gives D02. No clip plays in the wrong footing, and the swinger is visibly short of breath by blow 4.
6. **Joins.** No foot slide over 5 cm and no pop at any blend (NOW.md records a walk that slides at its joins, so this is a real risk).
7. **What witnesses register.** Replayed in the headless simulation with two onlookers, one 6 m away in view and one behind a wall: the first records a precursor within 0.23 s of A01 starting, and act and victim at f22; the second records sound only, at f22. Neither records anything before A01. The shove records only the 4.0 s shove attention.
8. **Tempo.** With the longer-telegraph setting on, the wind-up is 30 frames, every later key frame is 10 frames later, and the outcomes are identical.
9. **Rules of the game.** No health bar, damage number or hit marker is drawn (a screenshot check). All 17 clip names pass the content gate. Frame time stays inside PLAN.md's performance exit (median 16.7 ms) with the two men on screen.

Done means walked in the packaged build by the AI tester; it stays "ready for review" until Jafar passes it (CLAUDE.md).

### 5.5 What this list leaves out

Changed 13 October (not reviewed): the grab, the retreat and an onlooker stepping in are now drafted in 5.6 (F03 to F05, G03, G04, J01, J04). Finishing, guns, improvised weapons and carried knives stay out, and the last list of 5.6 gives their order. Where the clips come from is the lab test's question (see the rulings section).

- Finishing a downed man: a decision for the quiet afterwards, and the most sensitive scene under the content rule (violence stays, no cruelty as spectacle). Not in a first test.
- Guns, improvised weapons, knives and the grab that a held guard becomes.
- The onlookers' own animations (turn, step back, flee). The townspeople animation research covers them; this list only says when they should notice.
- Sources of the clips themselves.

### 5.6 Entries, runs and measures added after Jafar's design (13 October 2026, not reviewed)

**What changed.** The design keeps the first test as ruled: two men, one shove and one strike with hit reactions, in the game camera, after the walk passes, through the usual gate. Its lab test of the animation source (one wind-up, one strike, one hit reaction, one shove into a wall) comes before any building. So entries A01 to E03, runs 1 to 4 and items 1 to 9 of 5.4 stand, and nothing is renumbered. This section adds 15 entries with new ids (F, G, H, J) and items 10 to 17, grouped in the design's own build order. Square up and the shove are already in the first test, because the test needs them to be read and answered. The stare, the threat and the grab come after it. All new numbers are judgement or derived (marked), so they stand in for what Study 14 is to measure. Blend lengths are frames at 30 fps and judgement, as in 5.3.

Three stages. **first**: joins the first test (and is the lab test's shove into a wall). **rungs**: the test after it, the lower rungs. **gaps**: the test after that, the three gaps. Either man plays F, G and J01 to J03; H01 is the joining man's; J04 is a third person's.

| Id | Name | Length | Frames at 30 fps | Key frames | Timing source | Stage |
|---|---|---|---|---|---|---|
| G01 | shoved into a wall | 0.67 s | 20 | wall contact f8, rock ends f12 | derived from D01's pace; judgement | first |
| G02 | rebound off the wall | 0.80 s | 24 | off the wall f6, half-step ends f12 | judgement | first |
| F01 | stare (loop) | 2.0 s | 60 | loop seam f60 | judgement | rungs |
| F02 | threaten | 1.0 s | 30 | step f4 to f12, point lands f14, hand down f30 | judgement | rungs |
| F03 | grab | 0.90 s | 27 | wind-up end f9, contact f11, pull ends f17 | judgement | rungs |
| F04 | grabbed | 0.80 s | 24 | hands on wrist f8, leaning back f14 | judgement | rungs |
| F05 | held (loop) | 1.5 s | 45 | loop seam f45 | judgement | rungs |
| G03 | pin | 0.80 s | 24 | forearm lands f8, full weight f14 | judgement | rungs |
| G04 | pinned (loop) | 1.5 s | 45 | loop seam f45 | judgement | rungs |
| J01 | back away | 1.67 s | 50 | hands open f6, steps f14, f26, f38, turn f40 to f50 | judgement; step length from A03 | rungs |
| J04 | steps in | 1.2 s | 36 | hands rise f12, between the men f24 | judgement | rungs |
| H01 | second man joins | 2.0 s | 60 | eyes lock f6, last step f38, hands rise f42, stance visible f48 | judgement | gaps |
| H02 | circle (loop) | 1.5 s | 45 | loop seam f45 | judgement | gaps |
| J02 | break and run | 1.0 s | 30 | turn done f6, first stride f8, run cycle reached f24 | judgement | gaps |
| J03 | gives up the chase | 1.5 s | 45 | slowed f12, stopped f15, hands on knees f24 | judgement | gaps |

Fifteen new entries: 2 first, 9 rungs, 4 gaps. With the 17 above that is 32, and the first test's own list is 19. The police arriving has no new entry (see the last list).

**Existing entries whose status changes.**
- D08 (getting up) was "needed only if the test lets a downed man rise". It is needed now: Tom can be beaten and cannot die (R05), so a downed Tom gets up or wakes. D06 and D07 serve Tom as they serve the second man.
- D07: the note that a downed man can be finished stays Combat.cs's. In the design finishing is a decision, never a move, so no clip is built for it.
- E02: the held guard that "becomes a grab" is F03, in the rungs stage. The design names no defensive move, so E01 to E03 stand.
- A03 is the first test's way of backing off. J01 is its longer sibling.
- A02: the 3 s hold before an NPC swings stays. F01 counts toward it when a man stares first (judgement; open, see the rulings section).

### The entries added

**First stage: the shove into a wall.**

**G01 shoved into a wall.** Start: any stance, a wall 0.6 m behind him (judgement). End: back flat to the wall, hands out. 20 frames (0.67 s). The back meets the wall at f8 (0.27 s), head and shoulders rock until f12, still by f20. Derived: D01 moves a man 1.2 m by f15, 0.08 m a frame, so 0.6 m takes 7.5 frames, rounded to f8. The other frames are judgement. Blends from A02, E02 or a strike's recovery over 2 frames; to G02 over 2 (to D06 over 3 for a reeling man; to G04 over 3 once the pin exists). Hit reaction: this is the reaction. A steady man stays steady (judgement: a wall is not a blow; how much a wall adds is open). A reeling man is floored, as a shove floors him in D02 (Combat.cs), and goes down along the wall, G01 into D06. Distance, derived: the men stand about 0.8 m apart at contact (D01, judgement), so 0.8 + 0.6 = 1.4 m, inside strike reach 1.6 m. A shove into a wall does not create distance. Witnesses: the shove registers as in C01 at its contact (a Bumps shove, 4.0 s of attention, act slot only: "a scuffle"). The back on the wall at f8 is a sound that carries to shout range like B01's thud (judgement).

**G02 rebound off the wall.** Start: G01's end pose. End: A02-like stance, a little lower. 24 frames (0.80 s). Peels off the wall by f6 (0.20 s), a half-step forward of 0.3 m by f12 (judgement, under the 0.55 m stumble cap), hand to the chest, stance by f24. Judgement. Derived: 1.4 m less 0.3 m = 1.1 m apart afterwards, still inside strike reach. Blends from G01 over 2 frames; to A02 over 5. Hit reaction: this is the reaction; footing stays steady. Witnesses: nothing new.

**Rungs stage: the lower rungs, tied into perception and gossip.**

**F01 stare (loop).** Start and end: head and eyes on the other man, shoulders square to him, hands loose at the sides, weight even, chin slightly down; the breath layer of A02. 60 frames (2.0 s) loop, seam f60, judgement. Eyes locked by f6 of the blend. Blends from walk or idle over 6 frames; to A01 or F02 over 4; to walk or idle over 8 when he looks away. Hit reaction: none; it is not contact. Witnesses: rung 1, "a tension others notice; nothing to report". The precursor slot fills once the stare has held 1.0 s (30 frames, judgement); a glance fills nothing.

**F02 threaten.** Start: F01 or A02 pose. A step in of 0.4 m (judgement), chin up, one hand rises to a pointed finger at chest height, a short flat word, the hand drops. 30 frames (1.0 s): step f4 to f12, point lands f14 (0.47 s), held to f24, hand down f30. Judgement. Blends from F01 or A02 over 4 frames; to A02, A03 or J01 over 4 (the other man's answer). Hit reaction: none; no contact. Witnesses: rung 3. The precursor slot at f14; a threatened witness can be kept from reporting, never the street's talk (RULINGS 3 Oct). The words belong to the dialogue, not to this list.

**F03 grab.** Start: A02 pose, facing, in reach. Wind-up: the lead hand opens and reaches for the collar, the rear foot gathers. Contact: the hand closes on the collar and pulls the man 0.3 m in (judgement). End: held at arm's length, free hand low; the hold is then a pose with A02's breath layer. 27 frames (0.90 s): wind-up end f9 (0.30 s), contact f11 (0.367 s), pull ends f17 (0.567 s). Judgement: a longer reach than the shove's, so 0.30 s against C01's 0.267 s, still above the 0.19 s reaction time (standard, [S2]), so a grab can be seen. Blends from A02 or F02 over 3 frames; to C01 over 2 (a shove from the hold); to A02 over 5 on release. Hit reaction: F04 on the target; no injury. Witnesses: rung 4, "a scuffle: talked about, rarely reported". The act slot at f11, quiet, as C01. Whether a grab holds attention for 4.0 s as a shove does is open. No victim record in the harm book.

**F04 grabbed.** Start: any stance. End: F05's first pose. 24 frames (0.80 s): pulled 0.3 m forward (as F03's pull), hands reach the holder's wrist by f8 (0.27 s), weight leans back by f14 (0.47 s). Judgement. Blends from any stance over 2 frames; to F05 over 4. Hit reaction: this is the reaction; footing steady; no injury. Witnesses: the pull is the visible part of the act slot, as D01.

**F05 held (loop).** Pose: leaning back against the hold, both hands on the holder's wrist, head turned slightly away, feet shuffling. 45 frames (1.5 s) loop, seam f45, judgement. Blends from F04; to A02 over 5 frames on release; to C01 over 3 (he shoves the hold off; the holder takes D01). Hit reaction: none while held. Witnesses: the scuffle continues; nothing new.

**G03 pin.** Start: A02 pose or F03's hold pose, the other man at the wall (G01's end pose). The holder steps in, forearm across the chest, the other hand on the collar, weight into him. 24 frames (0.80 s): step f2 to f8, forearm lands f8 (0.27 s), full weight f14 (0.47 s), then a pose with the breath layer. Judgement. Blends from A02, F03 or G02 over 3 frames; to A02 over 5 on release; to A03 over 4 (steps back). A strike from a pin needs its own wind-up and is later. Hit reaction: G04 on the target; no injury. Witnesses: rung 4, the act slot at f8, quiet; no victim record in the harm book. Whether a pin fills the victim slot is open.

**G04 pinned (loop).** Pose: back flat to the wall, head back, both hands on the holder's forearm, feet shuffling, breath at the spent rate (0.75 a second, A02). 45 frames (1.5 s) loop, seam f45, judgement. Blends from G01 or G03; to G02 over 3 frames on release; to C01 over 3 (he breaks the pin with a shove; the holder takes D01). Hit reaction: none while held. Witnesses: continues; nothing new.

**J01 back away.** Start: A02, E02, F01 or F02 pose. End: standing, hands open and low, then a turn. 50 frames (1.67 s): hands open f6 (0.20 s, as A03), steps planted f14, f26 and f38, turn f40 to f50. Displacement 2.4 m (derived: three steps of 0.8 m, the step length of A03). Judgement. Blends from A02, E02, F01 or F02 over 3 frames; to the walk over 5 after the turn. Hit reaction: none. Witnesses: at f6 the precursor ends ("he stood down", as A03); no act is recorded. "A real option and often the best one" (the design).

**J04 steps in.** Played by a third person: a friend, a bystander or a shopkeeper. Start: walking or standing within 3 m of the pair (judgement). He turns toward them, both hands out palms toward the two men, and steps between. 36 frames (1.2 s): turn f6, hands rise f12 (0.40 s), between the men by f24 (0.80 s), held to f36. Judgement. Blends from walk or idle over 5 frames; to idle over 6. Hit reaction: none; no blow may land on him in the test (judgement; a hit on an intervener is a later rule). Witnesses: he steps in only after his own perception shows a precursor (A01 at f6) or an act (B01 at f22). His arrival at f24 ends the exchange: both men take A03 within 15 frames (0.5 s, judgement). The townspeople animation research is to be checked for an existing clip first (5.5; CLAUDE.md: reuse first). This entry is a target, not a clip.

**Gaps stage: being outnumbered, then running away.**

**H01 second man joins.** Played by the joining man. Start: standing or walking, in sight, within 4 m (judgement). End: A01's pose, 1.5 m to the side of the first man and a half-step behind him (judgement). 60 frames (2.0 s): eyes lock f6, steps planted f14, f26 and f38, hands rise f42, stance visible f48 (6 frames later, as A01's f6), A02 pose to f60. Judgement. Blends from walk or idle over 6 frames; to A02 over 5. Hit reaction: none. Witnesses: rung 2 for the second man: the precursor slot at f48. He may not start a wind-up until 1.0 s (30 frames, judgement) after f48, so the player sees him first.

**H02 circle (loop).** Pose: sidestepping in the stance, feet never crossed, head on the target. 45 frames (1.5 s) loop, seam f45, judgement; 0.9 m of arc a loop. Blends from H01 or A02 over 4 frames; to A02 over 4 (B01 starts from the A02 pose, so a strike after a circle goes through A02). Hit reaction: none. Witnesses: the precursor continues; nothing new. Purpose, by judgement: one man holds the front and one works to the side, so the two do not stand as a pair.

**J02 break and run.** Start: any stance. 30 frames (1.0 s): turn away complete f6 (0.20 s), first stride f8, run cycle reached f24 (0.80 s). The run cycle is the walk's rebuild on Epic's Game Animation Sample (RULINGS 13 Oct), not in this list. Judgement. Blends from any stance over 3 frames; to the run cycle over 6. A chaser starts at f12 (derived: the runner's f6 plus the 0.19 s reaction time of [S2], 5.7 frames, rounded to 6). Hit reaction: none. Witnesses: the flight slot fills at f6, when the body has turned away (judgement). "Whether he was recognised decides what follows" (the design).

**J03 gives up the chase.** Start: the run cycle. End: standing, bent, hands on knees, breath at the spent rate (0.75 a second, A02). 45 frames (1.5 s): slowed by f12, stopped f15, hands on knees f24, head up looking after the runner f36. Judgement. Blends from the run cycle over 4 frames; to idle over 8. Hit reaction: none. Witnesses: nothing new; the runner's flight slot is not undone. The rule that ends a chase, by judgement: the chaser stops when the runner is out of sight and more than 10 m ahead (KCD2's active-combat radius, 2.3, adapted) or after 60 s of hunting (K1's longest hunt time, 2.3, adapted). The chaser's top speed is 0.9 of the runner's (judgement), so a runner can escape.

### The runs, as adjusted

**The first test.** The four runs of 5.4 stand. One run is added. Run 5, the wall: with a wall 0.6 m behind the second man, Tom shoves him (C01, G01, G02); the pair end 1.4 m apart, inside strike reach, and the second man is steady. With the second man reeling, the shove puts him down along the wall (C01, G01, D06). The lab test is a subset of this test: B01 (wind-up and strike), D03 (one hit reaction), C01 with G01 (the shove into a wall). Tom can be the man who goes down (D06, D07, D08): he gets up. Nothing in the test kills anyone.

**The test after it (the lower rungs).** Run 6: the second man stares (F01) and squares up (A01, A02), and Tom threatens (F02). One take ends with the second man backing away (J01) or Tom stepping back (A03); another with a grab (F03, F04, F05) and a release. Run 7, the pin: a shove into the wall (C01, G01), a pin (G03, G04), then a release (G02) or a break with a shove (C01 on the holder, D01). Run 8: a friend steps in (J04) as a strike is thrown (B01), and both men stand down (A03).

**The test after that (the three gaps).** Run 9, outnumbered: the first man holds (A02), the second joins (H01) and works round (H02), and the two strike in turn (B01). Tom guards (E01 to E03), takes one blow (D03) and, in the last take, goes down (D06, D07, D08). Run 10, running away: J02, then J03. The police arriving waits for the officer's own animations.

**How two attackers stagger.** Each man keeps B01's mean gap of 2.0 s and its spread of plus or minus 0.5 s (KCD2's official mean gap; the narrow spread is judgement). KCD2's rule for more attackers (2.3: each gap grows by 0.8 of itself; an unverified reading) is not copied. It would give 3.6 s each for two and one blow from the pair every 1.8 s (3.6 / 2, derived), hardly more often than one man's 2.0 s, which contradicts "two against one is deadly" (R23). Instead the second man is offset by half a gap: his wind-up starts 1.0 s after the first man's (judgement), so the pair's blows come about once a second (2 / 2.0 s, derived) and, with the spread, never within 0.5 s (15 frames, judgement) of each other: the later man waits. The second man's wind-up is B01's unchanged, 20 frames, so the answer time of 5.1 holds for each blow. With no lock-on, the man at the side stays readable by sound (B01's cloth swish, f18 to f22) and by his stance. If the one-man floor of four blows holds for two men (judgement), an unguarded Tom is down about 3.0 s after the first blow (three gaps of 1.0 s), against 6.0 s for one man (three gaps of 2.0 s), both derived.

### Measures added (they continue 5.4's numbering; items 1 to 9 do not change)

Thresholds are judgement unless marked, as in 5.4.

10. **The wall shove (first).** In 10 of 10 runs with a wall 0.6 m behind (judgement), the shoved man's back meets the wall at G01's f8 within one frame; the men end 1.4 m apart (derived, plus or minus 0.15 m as in item 4); and a strike by the shover can land at once, since 1.4 m is inside the 1.6 m reach. No clip passes through the wall, and the game camera keeps both men in view with no pop at the wall (judgement; a camera near a wall is the risk).
11. **A man who is down is left alone (first, and every stage after).** After D06 or D02, no blow, grab or pin starts on him in 10 of 10 runs; the other man takes A03 or leaves. When Tom is floored, no death clip, text or end screen plays: he gets up (D08) or the run cuts to the aftermath (ruling 5; in the design, finishing is "a decision", not a move).
12. **Timing and joins on every new clip (all stages).** Items 1 and 6 apply to every F, G, H and J entry: key frames within one frame in 10 of 10 runs, no foot slide over 5 cm, no pop at a blend.
13. **The lowest rungs read (rungs).** A fresh reviewer, shown F01 and then A01, from 3 m and from 8 m, tells a stare from a square-up in at least 9 of 10 showings (the bar of item 2). In the headless simulation the onlooker in view records a precursor no sooner than 1.0 s into F01 and nothing for a shorter glance. An onlooker threatened in F02 makes no police report and still talks (RULINGS 3 Oct).
14. **The grab and the pin (rungs).** The holder's hand is within 5 cm of the collar at F03's f11 (judgement, the 5 cm of item 6) and the target's pull is 0.3 m (judgement). A held man breaks free with C01 in 10 of 10 tries and the holder takes D01. Neither clip injures: no victim record in the harm book, as for the shove in item 7.
15. **The endings (rungs and gaps).** J01: no act or victim slot fills in 10 of 10 runs. J04: he arrives within 3.0 s (judgement) of the act slot filling, both men take A03 within 15 frames of f24, and no blow lands on him. J02 and J03: a runner with a lead of 3 m (judgement) is not caught in 10 of 10 runs, and a chase ends by the rule in J03, never later than 60 s.
16. **Outnumbered (gaps).** Over 20 blows from two attackers in the headless simulation: the mean spacing is 1.0 s, plus or minus 0.2 s (judgement); no two contact frames are closer than 15 frames (0.5 s); and each man's own mean gap is 2.0 s (B01). A fresh reviewer, shown the second man's strike from the side at 3 m in the game camera, says "he is about to hit" before contact in at least 9 of 10 showings (as item 2).
17. **Names (all stages).** All 15 new clip names pass the content gate. The first test's two (G01, G02) join item 9's 17, which makes 19; the other 13 pass when they are built, 32 in all.

### What stays for later, in the design's build order

1. **The lower rungs** (after the first test): stare, square up, threaten, shove and grab, tied into perception and gossip. Drafted above as the rungs stage (F01 to F05, G03, G04, J01, J04).
2. **The three gaps, in Jafar's order:** being outnumbered (H01, H02), running away (J02, J03), the police arriving. The last has no entry: an officer's own animations, and the arrest rules (a rule, not a clip). Then ordering a named man hurt and the other crew verbs (the crime verbs, not clips).
3. **The street as a weapon, with improvised and carried weapons:** doorways, shop windows, railings, car bonnets, stairs, the quay edge; a brick, a chair, a snooker cue, a wheel brace, a cargo hook; cosh, knuckleduster, a utility knife, flick knife, bat. This holds rungs 6 to 8 (weapon out, weapon used, kill) and a blow with a wall behind, which needs the design's number for what a wall adds. Study 14 sets how many paired moves a street needs.
4. **Firearms, last,** after melee works (R04).
5. **Never a clip:** finishing a man who is down. It stays a decision.

## 6. Not reached, unverified, sources

### Not reached

- YouTube videos, which asked for a sign-in and were not worked around: Warhorse's official live-action combat video, the Hangar 13 PAX East panel ("Family Takes Sacrifice"), the "Breaking Omertà" developer insights video, and the "Family Code" videos. Only the official pages that describe them were read.
- The GDC 2025 talk video (the Vault page showed a login limit; only its abstract was read) and the GDC 2026 session page "Supporting Thousands of NPCs" (403).
- Fandom wikis for both games (403). The Unreal Engine developer interview on Mafia (403; the WebFetch tool could not resolve the host either).
- GameSpot reviews of both games, Stevivor, GamesHub, Checkpoint, Keengamer (403), Deltias and Sportskeeda (405), Nexus Mods (403). Nothing from them is used. Search summaries that quoted them were treated as leads only.
- The Epic Games interview with Martin Ziegler: not opened; known only through the Insider Gaming page [K16].
- Business Wire's launch release: the transfer failed.
- Other Steam community pages were not opened, except the two guides named at the end of the Sources list.

### Unverified

1. Expert Game Reviews frame table for perfect block and master strike (no method; contradicts the official wiki on who teaches master strike) [K36].
2. LootLore's 0.4 s and 0.55 s windows, "30 percent" claim, Defense 8 unlock and "works unarmed" [K37].
3. A search summary of Keengamer saying "about a second" to parry in Mafia (page not reached).
4. Fextralife's maximum stamina of 136 [K21].
5. Player claims that master strikes are sword-only, and that NPCs use them in fist fights [K32].
6. Our reading of the perfect-block help text (window is a share of lead time, widens with the square root of skill).
7. Our reading of the attacker-gap rule and the rates built on it (derived rates in 2.3).
8. Whether retail values match the table exported on 14 January 2025.
9. Units not stated in the official table: MinPerfectBlockSlot01, the stealth slot and cooldown values (StealthKillMinSlot 0.05 and StealthKillMaxSlot 0.4, StealthCooldown 5). Not used in any total.
10. The Escapist's mapping of crimes to punishments (press; no official table read) [K26].
11. The official wiki's example crime entry values (assault, importance 130): shown as an example of the table format [K4].
12. Whether KCD2 has a kick or shove as a named verb; only the first game's codex and a patch note that removed a clinch push were read [K22, K9].
13. That fists knock out and do not kill in KCD2 (a reading of one help text with value 0) [K1].
14. Any fist or brawl system in Mafia: not published; one critic says none [M20].
15. Any bystander, civilian or police reaction to a fight in Mafia: not published.
16. Which weapons lack which direction in KCD2: guides conflict [K18, K34, K31].

### Sources

All read 13 October 2026. "Full" means read to the end. "Sections" means the named parts were read and the rest of the page was searched by keyword. The keys are not consecutive: M11, M23 and M24 were dropped when they proved not needed.

**Our own repository (read first):** game-design/combat-spec.md (full), game-design/agency-model.md (full), game-design/weapons-spec.md (sections 4, 6, 8, 10), RULINGS.md (full), canon.md (full), CHARTER.md, PLAN.md, NOW.md, TOWN.md, CATALOGUE.md (homes table), production/research/aaa-reference/KIT.md, production/research/coverage-audit-kcd2/SUMMARY.md and DELIVERY.md (sections B, E, F), ledger/Assets/Scripts/Core/Combat.cs and Interaction.cs.

**Added later, not reviewed:** Jafar's design "LEDGER Combat: Final State" (Claude Docs, revision 12, dated 12 October 2026), read in full on 13 October 2026; the RULINGS.md lines starting "12 Oct, combat" and its 3 Oct line on animation sources.

**Kingdom Come: Deliverance II**

- K1, official. Warhorse modding wiki, article KM-A-20 "RPG Constants/Params", values exported 14 January 2025, page updated 25 October 2025. Whole table read; the help texts were read for the combat, crime, perception, reputation and injury rows. https://warhorse.youtrack.cloud/articles/KM-A-20 (the page is a script shell; the text was read through the wiki's public interface https://warhorse.youtrack.cloud/api/articles/KM-A-20?fields=idReadable,summary,content,updated)
- K2, official. Same wiki, KM-A-21 "Stats and skills", updated 15 January 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-21
- K3, official. Same wiki, KM-A-12 "Database tables", updated 28 January 2025. Sections (the list of tables for combat, AI, RPG and crime). https://warhorse.youtrack.cloud/articles/KM-A-12
- K4, official. Same wiki, KM-A-27 "Crime", updated 31 March 2025. Full. https://warhorse.youtrack.cloud/articles/KM-A-27
- K5, official. Warhorse Steam announcement "Weapons and combat mechanics", 18 October 2024. Full. https://steamcommunity.com/games/1771300/announcements/detail/4521142560073672483
- K6, official. Warhorse Steam announcement "Hardcore Mode is live NOW in Patch 1.2.4", 15 April 2025. Full. Steam news feed https://api.steampowered.com/ISteamNews/GetNewsForApp/v2/?appid=1771300&count=300&maxlength=0&format=json (item 1796631172410040)
- K7, official. Deep Silver game page, Combat feature text. Sections (the Combat feature text). https://www.deepsilver.com/games/kingdom-come-deliverance-ii
- K8, official. Deep Silver "Insider tips from the developers of Kingdom Come: Deliverance 2" (before the 4 February 2025 launch). Full. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/insider-tips-from-the-developers-of-kingdom-come-deliverance-2
- K9, official. Patch 1.2 notes (Steam post of 13 March 2025 points to them). Sections plus keyword search of the quest lists. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-12
- K10, official. Patch 1.3 notes (Steam post 15 May 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-13
- K11, official. Patch 1.4 notes (Steam post 9 September 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-14
- K12, official. Patch 1.5 notes (page undated; hotfix 1.5.1 followed on 14 November 2025). Sections. https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/patch-15
- K13, official. GDC Vault page for "Combining GOAP and MBTs to Create NPCs' Behaviors for Kingdom Come: Deliverance II", Matej Marko, Warhorse, GDC 2025. Abstract only. https://www.gdcvault.com/play/1035576
- K14, interview. Tobias Stolz-Zwilling, Warhorse PR manager, with Stephen Farrelly, 3rd-Phase Boss, 18 December 2024. Full. https://3rd-phase-boss.com/blogs/gaming/kingdom-come-deliverance-2-developer-interview-hands-on
- K15, interview. Tobias Stolz-Zwilling, Tech4Gamers, 3 March 2025. Sections (the combat answer and its neighbours). https://tech4gamers.com/kingdom-come-deliverance-2-interview-warhorse/
- K16, interview via press. Martin Ziegler quoted by Insider Gaming, 15 July 2024. Full. https://insider-gaming.com/warhorse-kingdom-come-deliverance-2-immersive/
- K17, wiki. Wikipedia, Kingdom Come: Deliverance II. Sections (gameplay, plot, mode notes). https://en.wikipedia.org/wiki/Kingdom%20Come:%20Deliverance%20II
- K18, wiki. Fextralife KCD2 wiki, "Combat", edited 24 August 2026. Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Combat
- K19, wiki. Fextralife, "Feint". Full. https://kingdomcomedeliverance2.wiki.fextralife.com/Feint
- K20, wiki. Fextralife, "Hardcore Mode". Sections (the mode list and perks). https://kingdomcomedeliverance2.wiki.fextralife.com/Hardcore+Mode
- K21, wiki. Fextralife, "Stamina". Sections (the description and stats). https://kingdomcomedeliverance2.wiki.fextralife.com/Stamina
- K22, wiki. Kingdom Come: Deliverance Wiki on wiki.gg, "Combat" (codex entries of the first game). Full. https://kingdomcomedeliverance.wiki.gg/wiki/Combat
- K23, press. Shacknews review, 3 February 2025. Sections (the combat and save paragraphs, pros and cons). https://www.shacknews.com/article/142932/kingdom-come-deliverance-2-review-score
- K24, press. Gamerant, "Master Strike, Explained", 5 February 2025. Full. https://gamerant.com/kingdom-come-deliverance-2-kcd2-how-master-strikes-explained/
- K25, press. Gamerant, KCD2 crime and punishment preview, 16 August 2024. Full. https://gamerant.com/kingdom-come-deliverance-2-crime-punishment-reputation-system/
- K26, press. The Escapist, "How Crime and Punishment Work in KCD2", 21 February 2025. Full. https://www.escapistmagazine.com/how-crime-and-punishment-work-in-kingdom-come-deliverance-2/
- K27, press. PCGamesN combat and combos guide, updated 21 February 2025. Full. https://www.pcgamesn.com/kingdom-come-deliverance-2/combat-combos
- K28, press. Beebom, block, parry, dodge and riposte, 4 February 2025. Full. https://beebom.com/how-to-block-parry-dodge-riposte-in-kingdom-come-deliverance-2/
- K29, press. Gamer Guides, Unarmed leveling and perks, 4 February 2025. Sections. https://www.gamerguides.com/kingdom-come-deliverance-ii/guide/stats-and-skills/unarmed
- K30, press. Gamer Guides, "The Rabbit Icon", 5 February 2025. Read through the four hare icon states and the start of the sneaking advice. https://www.gamerguides.com/kingdom-come-deliverance-ii/guide/getting-started/gameplay/the-rabbit-icon-stealth-and-detection
- K31, press. Seven Swords combat guide (page dated 10 October 2026). Full except its question-and-answer list. https://sevenswords.uk/kingdom-come-deliverance-ii-combat-guide/
- K32, player. Steam discussion "Master strikes?", 6 February 2025. Full. https://steamcommunity.com/app/1771300/discussions/0/601895662819239243
- K33, player. Steam discussion "This combat system is utter trash", February 2025. First page of replies. https://steamcommunity.com/app/1771300/discussions/0/601895505111307429
- K34, player. Steam guide "Understanding how Combos work" by Kabirbd. Chapters 1 and 2. https://steamcommunity.com/sharedfiles/filedetails/?id=3442173547
- K35, player. Steam guide on fighting multiple enemies, by The Last Virgin. Full. https://steamcommunity.com/sharedfiles/filedetails/?id=3455238658
- K36, unverified. Expert Game Reviews, timing guide. Full. https://expertgamereviews.com/kingdom-come-deliverance-2-combat-timing-guide/
- K37, unverified. LootLore, master strike guide (dated 23 May 2026). Full. https://lootlore.online/en/kingdom-come-deliverance-2/mechanics/kcd2-master-strike-guide
- K38, press. Master of Warcraft, Easy Combat mod, 14 February 2025. Sections (the lines about timing windows). https://www.masterofwarcraft.net/2025/02/kingdom-come-2-easy-combat-mod-master.html
- K39, official. Warhorse Steam announcement "Catch-up on our Gameplay Showcase", 10 January 2025. Full. Steam news feed (item 1788311419052726), same link as K6.

**Mafia: The Old Country**

- M1, official. 2K, "Quick Tips". Full. https://mafia.2k.com/the-old-country/news/quick-tips/
- M2, official. 2K, "Community Q&A" (June 2025). Full. https://mafia.2k.com/the-old-country/news/community-q-and-a/
- M3, official. 2K, "Community Q&A #2" (early August 2025). Full. https://mafia.2k.com/the-old-country/news/community-q-and-a-2/
- M4, official. 2K newsroom, 8 May 2025. Full. https://newsroom.2k.com/news/mafia-the-old-country-launching-august-8-2025-debuts-official-gameplay-trailer-and-developer-insights-video
- M5, official. PlayStation Blog, Alex Cox, Hangar 13 game director, 8 May 2025. Full. https://blog.playstation.com/2025/05/08/mafia-the-old-country-uncovers-the-origins-of-organized-crime-on-august-8/
- M6, official. PlayStation Blog, Alex Cox, 22 July 2025. Full. https://blog.playstation.com/?p=407886
- M7, press report of a developer panel. Popverse, Nick Baynes at PAX East, 11 May 2025. Full. https://www.thepopverse.com/gaming-mafia-the-old-country-weapons-player-knife-duel-stealth-pax-east-2025
- M8, interview via press. GamingBolt, Joshua Zammit quoted, 8 May 2025. Full. https://gamingbolt.com/mafia-the-old-countrys-combat-has-a-life-or-death-vibe-encourages-more-tactical-play
- M9, official. 2K, "The Family Code" gameplay videos page. Full. https://mafia.2k.com/the-old-country/news/gameplay-deep-dive-videos-family-code/
- M10, wiki. Wikipedia, Mafia: The Old Country. Sections (gameplay, release, reception table). https://en.wikipedia.org/wiki/Mafia:%5FThe%5FOld%5FCountry
- M12, press. Game8, "Knife Fight Guide". Sections (the duel tips and the controls table). https://game8.co/games/Mafia-The-Old-Country/archives/542506
- M13, press. GamerBlurb, knife fight guide, 9 August 2025. Full. https://gamerblurb.com/articles/mafia-the-old-country-knife-fight-dueling-guide
- M14, press. DTGRE, Palio chapter knife guide, 7 August 2025, and its L'Ombra boss guide. Full. https://www.dtgre.com/2025/08/mafia-old-country-palio-knife-combat-guide.html and https://www.dtgre.com/2025/08/boss-fight-guide-defeating-lombra-mafia-the-old-country-palio.html
- M15, press. VGTimes, stealth guide, 13 August 2025. Full. https://vgtimes.com/guides/131564-mafia-the-old-country-stealth-guide-tips-for-silent-gameplay-and-sneaky-completion.html
- M16, press. Gameranx, ten quick tips, 8 August 2025. Sections (the knife, dodge, parry and distraction tips). https://gameranx.com/features/id/547457/article/mafia-the-old-country-10-quick-tips-to-become-a-made-man/
- M17, press. Game8, stealth guide. Sections. https://game8.co/games/Mafia-The-Old-Country/archives/542458
- M18, press. CrimeNet Gazette review. Sections (the lines on knives, stealth and duels). https://www.crimenetgazette.com/post/mafia-the-old-country-review-join-the-mafia-regret-the-knife-budget
- M19, press. GameScreed review, 8 August 2025. Sections (the lines on combat, stealth and duels). https://www.gamescreed.com/reviews/mafia-the-old-country-review
- M20, press. Impulse Gamer review, 7 August 2025. Sections (the lines on stealth, knives and duels). https://www.impulsegamer.com/mafia-the-old-country-review-pc/
- M21, press. GameIndustry review, 22 September 2025. Sections (the lines on duels and missions). https://www.gameindustry.com/reviews/game-review/mafia-the-old-country-is-a-crime-saga-told-with-cinematic-splendor/
- M22, press. MobileSyrup review, 18 August 2025. Sections (the lines on mechanics and duels). https://mobilesyrup.com/2025/08/18/mafia-the-old-country-breathes-new-life-into-the-classic-franchise/
- M25, official. 2K, "Free Ride update". Sections. https://mafia.2k.com/the-old-country/news/free-ride-update/
- M26, press (German). PC Games, new combat video, 31 July 2025. Full. https://www.pcgames.de/Mafia-The-Old-Country-Spiel-74877/News/Neues-Video-zum-Kampfsystem-1478658/

**Standards**

- S1, standard. Dustloop, "Using Frame Data". Full. https://dustloop.com/w/Using%5FFrame%5FData
- S2, standard. Wikipedia, "Reaction time" (mental chronometry). Sections on simple reaction time. https://en.wikipedia.org/wiki/Reaction%5Ftime

Opened and not used: 2K's developer diaries 1 and 3 for Mafia (knife research, motion capture stages), Wccftech's Mafia interview piece, Gamerant's second KCD2 crime article, PatchCrazy's crime guide, Gamer Guides' other pages, a Steam guide "How To Win Fights", and a Steam "How Not to Die" guide (a joke guide).
