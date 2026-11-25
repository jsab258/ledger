# Census C: combat, confrontation and stealth

Read only, from the repository as it stood on 25 November 2026. Branches: lane-2026-11 (lane) and origin/wip (wip).

Short names used in the "where" column:

- CD = game-design/combat-design.md (wip; Jafar's "Combat: Final State", 12 Oct, with the 2 Nov additions)
- WS = game-design/weapons-spec.md (wip; "Perception, weapons and violence", v5, approved 29 Jul, amended 18 Nov)
- FTM = production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md (both branches; bands C1 to C15, drills M1 to M10)
- S14 = production/research/aaa-reference/studies/14-combat.md (wip); S17 = studies/17-yakuza-shenmue.md; COMBAT.md = production/research/aaa-reference/COMBAT.md (wip)
- BP01, BP02, BP03, BP05, BP07, BP11 = production/lane/blueprint/BLUEPRINT-0x-*.md (lane); the number after is the part id
- LH = what-if/LONG-HEAT.md; PP = what-if/PROPOSED-PARTS.md; Q = what-if/QUESTIONS.csv; FIFTY = fifty/FIFTY.md; SM = hype/SIGNATURE-MOMENTS.md; RC = reality-check/SUMMARY.md (all under production/lane/blueprint/)
- DC = production/research/lane/details-catalogue/CATALOGUE.md (wip and lane); AAA = production/research/lane/aaa-studies/
- The player is Tom in the older wip documents (CD, WS, FTM, S14) and Frank in the blueprint (renamed 24 Nov).

State key: designed (written down with a rule or a number), partly (some of it written, or only proposed, or only in the July spec), gap (named as missing or never specified), ruled out (Jafar or canon says no).

## Table

| id | feature | what it does, or what the project says | where | state |
|---|---|---|---|---|
| C001 | Eight-rung ladder | Combat is eight rungs (stare, square up, threaten, shove or grab, strike, weapon out, weapon used, kill); each rung is an act with the seven perceivable slots, so memory and gossip treat it like any deed | CD The ladder; BP01 1.3.4 | designed |
| C002 | Most confrontations end on rungs 1 to 4 | Menace is the everyday form of combat; blows are the escalation and each rung costs more than the one below | CD The ladder; BP01 1.3.4 | designed |
| C003 | Stare / hard look | A held look is rung 1, put on the M key; a tension others notice, nothing to report. How long a stare lasts is open (the 3 s was the July spec's) | CD The ladder; BP01 1.3.4, 1.4.7; COMBAT.md Left open | partly |
| C004 | Square up | A visible change of stance (rung 2); witnesses pay attention before a blow lands. Clips A01 to A03 only drafted | CD The ladder; COMBAT.md 5.2; S14 clip table | partly |
| C005 | Threaten (rung 3) | Said in talk or shown; can stop a report to the police, never the street's talk | CD The ladder; BP01 1.3.4; BP02 2.5.2 | designed |
| C006 | Shove | Rung 4 on the M key; shove into a wall; recovery and reactions D01, D02 drafted | CD The ladder; BP01 1.3.4; COMBAT.md 5.2 | designed |
| C007 | Grab and pin | Takes a man by the collar, pins him to a wall, holds about 2 s; how a hold ends (release, break, strike from the hold, throw) is open | BP01 1.3.4; COMBAT.md Left open | partly |
| C008 | Strike (rung 5) | A committed blow; a fight; most who see it report it; injuries begin | CD The ladder | designed |
| C009 | Weapon out (rung 6) | Shows a knife, bat or gun; the street scatters; a gun out is news across town | CD The ladder; BP01 1.3.6 | designed |
| C010 | Weapon used and kill (rungs 7, 8) | Police interest, hospital, a traceable weapon; a body is a fact no rumour can soften | CD The ladder, The aftermath | designed |
| C011 | Blow response time | Any blow starts moving within 0.1 s of the button (C1); a press 100 ms early still counts | FTM (c) C1; BP01 1.1.1, 1.3.1 | designed |
| C012 | Jab | Lands 0.25 to 0.40 s after it starts; contact window 0.03 to 0.10 s; recovery 0.20 to 0.40 s | FTM (c) C2; BP01 1.3.1 | designed |
| C013 | Hook | Lands 0.45 to 0.75 s in FTM; the blueprint names only jab and heavy blow and says no combos | FTM (c) C2; BP01 1.3.1 | partly |
| C014 | Committed heavy blow | 0.63 to 0.85 s to contact, cannot be cancelled (which makes it readable); miss recovery 0.70 to 0.90 s | FTM (c) C2; BP01 1.3.1; S14 For LEDGER 1, 2 | designed |
| C015 | Hit-stop by blow kind | Freeze on contact: jab 0.025 to 0.05 s, hook 0.04 to 0.08, heavy 0.06 to 0.12, swing 0.07 to 0.13; method is by eye per animation, then frozen as data | FTM (c) C3, (d); BP01 1.3.1 | designed |
| C016 | Contact camera close-in and shake | Brief close-in held about 0.8 s inside the wider fight view, shake 0.3 to 1.5 degrees settling in 0.3 s, obeys Reduce motion | FTM (c) C10; CD Since 12 Oct, The fight camera; BP01 1.3.1 | designed |
| C017 | Four sound layers, no combat music | Whoosh, impact (within 0.034 s of contact), pain cry (0.05 to 0.30 s after), enemy shout (at least 0.40 s before his blow) | FTM C13; BP05 5.5.6; CD How a fight feels | designed |
| C018 | Hit reactions by side | A struck man reels to the side he was hit: light 0.5 to 0.7 s, heavy 0.9 to 1.3 s; physics blended over authored clips | FTM C4; S14 For LEDGER 3; CD The animation question | designed |
| C019 | Readable wind-ups | Every incoming blow readable 0.45 to 0.80 s ahead in shoulders, feet and breath, never an icon | FTM C5; BP01 1.3.2; CD How a fight feels | designed |
| C020 | Guard (block) | A held key; a blocked fist does little, a blocked heavy blow staggers a little, a swung weapon breaks through. CD says "a guard that drops" but COMBAT.md says defence is not a rung and is open | BP01 1.3.2; CD How a fight feels; COMBAT.md Left open | partly |
| C021 | Dodge or slip | A tap with a direction slips a blow (about 0.3 s, whole dodge 0.50 to 0.80 s, blows cannot land for 0.20 to 0.35 s) | FTM C6; BP01 1.3.2 | designed |
| C022 | Counter | A blow just after a slip or block counts as a counter, a heavy blow at a jab's speed. No on-screen counter flash | BP01 1.3.2; FTM (a) Sleeping Dogs, Arkham rows | partly |
| C023 | No combos | Jafar's ruling of 24 Nov: combos out. FTM still has a three-blow combination band (C14) and drill M2 | BP01 1.3.1, LH-14c; FTM C14, (f) M2 | ruled out |
| C024 | Stamina and mashing | Mashing empties stamina in 6 to 10 jabs or 3 to 4 heavy blows; refill 4 to 8 s; mashing tires you out and loses | FTM C11; CD How a fight feels; BP01 1.3.2 | designed |
| C025 | No lock-on, motion warp to close in | The man the stick points at is hit; Tom slides to about 1 m in the wind-up, closing in 0.40 to 0.55 s from at most 2.0 m; nobody hit through a wall | FTM C9; BP01 1.3.3; S14 For LEDGER 5 | designed |
| C026 | At most two swing at once | Two men may swing, at least 0.4 s apart, longest wait 2.5 s; attack tickets and a priority by distance and camera view | FTM C8, (d); BP01 1.3.2 | designed |
| C027 | Spacing round Tom | Enemies wait on slots round the player, shaped by walls (TLOU2's 16 radial lines) | FTM (d) | partly |
| C028 | Blows as data with timeline marks | TLOU2 method: attack data with hit frames, tracking and invulnerable spells; behaviours above it | FTM (d) | designed |
| C029 | Slower-fights assist | Wind-ups 25% longer with one swinger (BP) against 1.25 to 1.5 times (FTM); same fight at another tempo, not an easier one | BP01 1.3.2; FTM C5; BP11 C-114; CD How a fight feels | designed |
| C030 | Auto-resolve option | CD promises an auto-resolve option for fights; no later document specifies it | CD How a fight feels | gap |
| C031 | No health bar; condition in the body | Posture, breath, a guard that drops, blood and a limp; a player asked "who was winning?" can say (4 of 5 testers) | CD How a fight feels; BP01 1.3.7, RT-11 | designed |
| C032 | Minimal HUD switch | CD says a minimal HUD exists as a settings switch so values are data from day one; the blueprint says no bar and no number on screen | CD How a fight feels; BP07 (no number on screen) | partly |
| C033 | Frank's three states | Fresh, hurt (guard slower to rise, shorter breath, a stagger) and beaten (down), shown only in the body; no armour, no healing items | BP01 1.3.7, RT-11 | designed |
| C034 | Hidden capacity by fighter type | A big man most, a knife man least; a jab takes little, a heavy blow about three jabs, a weapon more (bat more than cosh); no numbers beyond that | BP01 RT-11; BP11 gap list 1.3.6 | partly |
| C035 | Five kinds of fighter | Boxer who guards, brawler who rushes, big man slow to drop, knife man who keeps distance, wiry one who slips and runs; no two fights in a row the same mix | BP01 1.3.12, FIT-P17 | designed |
| C036 | Fair one-on-one roughly even | Skill tips it; a patient fighter wins most, a masher under 3 in 10 | CD Tom, the crew and the odds; BP01 1.3.8 | designed |
| C037 | Two against one deadly, three a beating | Skilled player wins a fair two against one about 1 in 4 (15 to 35% in bots), masher under 10%; the street's places count double | CD Tom, the crew and the odds; BP01 FIT-P18 | designed |
| C038 | Nerve in a fight | A watched or cornered man stands longer; alone he gives way sooner; blood on Frank lowers his nerve; watchers keep about 3 m and scatter when a weapon is out. Nerve has no numbers | BP01 1.3.8; BP11 gap list 1.3.8 | partly |
| C039 | No random street fights | A crossing never starts a fight Frank or a rival's state did not cause; not Yakuza's frequent fights | AAA DENSE-DISTRICT-REVIEWS DENSE-05; S17 For LEDGER 7; CD Since 12 Oct | ruled out |
| C040 | Fist knock-out | Fists knock a man out for 10 to 30 s and never kill on their own (ruling of 30 Oct) | CD Knock-outs; FTM C7; BP01 1.3.7 | designed |
| C041 | The rare fatal fall | A fall against a kerb, wall or step after a heavy or weapon blow can kill, rarely, and the town treats it as a killing; deterministic; 1 in 50 to 1 in 20 knockdowns at the three edges; never to Frank | CD Knock-outs; BP01 RT2-12, 1.3.7 | designed |
| C042 | The quiet blow from behind | Cosh or fist on an unaware man knocks out 10 to 30 s and is seen as a strike; the nearest thing to a takedown | BP01 1.3.6, 1.3.7; Q001 | designed |
| C043 | Stealth takedown and finisher moves | No finishers, no scripted takedown clips (Mafia's 19 takedown designs and Yakuza finishers are ignored) | S14 For LEDGER 13; CD Since 12 Oct Street as a weapon; BP11 C-017 | ruled out |
| C044 | Choke, garrote, ligature | July spec has wire/garrote and cord/belt (silent, from behind, cannot be aborted); the 12 Oct design's four tiers and the blueprint do not carry them | WS 5.2 Family 4; CD Weapons; BP01 1.3.6 | gap |
| C045 | Finishing a downed man | A decision in the quiet afterwards: stand over him, hold strike 2 s, "Finish him?" asked twice; with fists a serious beating, never a death; with a weapon a killing | CD The ladder; BP01 RT2-11 | designed |
| C046 | Kick on a downed man | No standing kick; on a downed man strike becomes a kick, counted as fists, never kills, read one step heavier by the town | LH-14c; Q007; BP11 C-341 | partly |
| C047 | Blows on a pleading or downed man shown | Fully animated, no cut-away, PEGI 18 within canon (blood and light gore, no cruelty as spectacle) | BP01 RT2-11, 1.3.5; BP05 5.2.2; BP11 C-273, C-274, C-302 | designed |
| C048 | Back off | Backing off is a real option, an input at every moment of a fight | CD How fights end; BP01 1.3.9 | designed |
| C049 | Surrender or yielding by the other man | KCD2 morale: man backs off, runs or yields at 0.2, moved by events; for others' endings. Handing himself in is a separate proposal for Frank | S14 For LEDGER 7; COMBAT.md 2.6; LH-11 | partly |
| C050 | Run from a fight | A foot chase the runner can escape through alleys and yards; recognition decides what follows | CD How fights end; BP01 1.3.9, 1.5.1 | designed |
| C051 | Police arrive mid-fight | A beat officer first, then more; running from them is a new offence; arrival time is judgement only | CD How fights end; S14 Open blind spots | partly |
| C052 | People step in | Friends pull their man away, bystanders shout, a shopkeeper comes out; a person with nerve may step in unarmed; "people step in" has no build slot in CD | CD How fights end; BP02 2.5.3; COMBAT.md Left open | partly |
| C053 | Break up a fight between two other men | CD says townspeople's feuds can turn into fights the player may watch, join or break up; no separate verb exists | CD Tom, the crew and the odds; Q201 | gap |
| C054 | Frank cannot die | Beaten, he comes round on the pavement, in Grace Rinaldi's kitchen or in hospital; control back within 60 real seconds with the cost said | CD How fights end; BP01 1.3.9; FIFTY 45 | designed |
| C055 | Robbed when beaten | Only by men who rob for a living; takes paper money and what he holds, never the Ledger, coat or keys; the takers are named and findable | BP01 RT2-13; S14 For LEDGER 12 | designed |
| C056 | Hospital and the retired doctor | Hospital costs days, not money, and plants a witness; a doctor by the quay stitches for £20 and remembers; a hospital visit is a soft-edge scene | BP01 1.3.9, 1.3.11; PP P11 | designed |
| C057 | Marks that last | Bruises and cut lip three game days, limp one day, a knife wound bleeds until stitched; others see and say so | CD The aftermath; BP01 1.3.11 | designed |
| C058 | Lasting injury (arm in plaster) | Story needs a lasting arm injury that changes driving and the quay's fists; part gives only days | BP01 1.3.7, 1.3.11; BP11 C-338 | gap |
| C059 | Repeated beatings | A third beating in a game week brings Ron to fetch him; robbers take only what he carries | PP P15; Q184 | partly |
| C060 | Blood on clothes | Appears for edged, struck-with and struggle fights, not guns, cosh or accidents (WS); stays until washed with water and privacy; a rung-2 mark; noticed by light and proximity | WS 15.4; BP01 1.4.4; AAA IMMERSION-FEATURES IM-04, IM-05 | designed |
| C061 | Seven places for paired moves | Walls, doorways, railings, car bonnets, steps, kerbs and the quay edge, each a paired move fitted by height; a man in railings is out 4 s | BP01 1.3.5; CD The street is a weapon; S14 For LEDGER 9 | designed |
| C062 | Things to hand | Brick, chair, dustbin lid, wheel brace break after about 2, 3, 4 blows and never, then are left behind; CD adds snooker cue, cargo hook, ashtray, pipe, bins, crates, signs, bicycles | BP01 1.3.6; FTM C12; CD The street is a weapon, Since 12 Oct | designed |
| C063 | Paired animation count | About 14 designs, 28 with facings, against Mafia's 19 and 36; fit by height | S14 For LEDGER 9 | partly |
| C064 | Quay edge | A man put over the quay edge climbs out at the nearest ladder within a minute; whether it counts as one of the killing edges is open | BP01 1.3.5; CD Since 12 Oct Knock-outs | partly |
| C065 | Accidents as violence with no crime | Stairs, window, dock, road, fire, machinery; seen doing it is the worst observation; a coroner still comes; July spec only | WS 5.2 Family 6, 14 D | partly |
| C066 | Finishers off bridges, through windows | Not taken as moves; only their surfaces become paired moves | CD Since 12 Oct Street as a weapon | ruled out |
| C067 | Four weapon tiers | Fists; improvised; carried (cosh, knuckleduster, utility knife, flick knife, bat); firearms, rare | CD Weapons | designed |
| C068 | Carried weapons | Seen on him, found in a search, have a history; two things under the coat and one in hand; the rest in the drawer or shed | BP01 1.3.6; Q133; WS 7.1 | designed |
| C069 | Weapon draw | Held input (semicolon) chosen from the two things under the coat; slow enough to be a decision; cannot be undrawn unseen | BP01 1.3.6; WS 6.3 | designed |
| C070 | Brandish as a verb | July outcome table: comply, freeze, flee screaming, call the bluff, escalate; reversible only towards escalation | WS 5.1 | partly |
| C071 | Draw a weapon inside talk | Weapon input works in talk, camera stays at talk distance, rung 6, answered by the other man's temper; typed words never draw | LH-14b; Q006, Q161, Q208 | partly |
| C072 | Where weapons come from | Bought from a person, stolen, taken, or found once at Mickey's; no random loot; one deckhand seller | WS 7.3; BP01 RT2-14 | designed |
| C073 | Provenance and disposal | Every weapon remembers its history; drain or dock; found by next passer; prints, witness or seller link it | WS 7.4; LH-14d; Q008, Q134 | partly |
| C074 | Frisk | Who may, on what trigger; refusing is an answer; concealment belongs to object and coat; found is worse than used | WS 7.2, 15.5 | partly |
| C075 | Weapon animation list | About 70 clips for four carried weapons, 25 for things to hand, plus guns: draw, blows, block, put away, drop, hand over, disarmed | LH-14e | gap |
| C076 | Knife in a fight | A knife wounds (hospital 5 days, blood, 8 hours if arrested) and kills only by the finishing choice or the fall; open option: a committed thrust into a spent man | BP01 RT2-11; LH-14a; Q005 | partly |
| C077 | Knuckleduster, cosh effects | Carried and seen, but only "bat more than cosh" is ordered; knuckleduster has no stated effect | BP11 gap list 1.3.6; Q130 | gap |
| C078 | Throwing a knife or brick | Not written; only a thrown stone for noise | Q131 | gap |
| C079 | Picking up a dropped weapon | Guns from a man or body are covered; melee weapons not | Q132; LH-14e | gap |
| C080 | Firearms: two guns, rare and late | Service revolver (six) and sawn-off (two); none at the start; escalation dial Fists, Shown, Fired, War; before War a hit wounds, never kills | BP01 1.3.10, RT-10, RT2-14; CD Weapons | designed |
| C081 | Gun feel | No crosshair, no ammunition count, one fixed shoulder, empty click, no gyro, scope, explosions or ammunition types; recoil, rate of fire not yet written | BP01 1.3.10, RT-10 | partly |
| C082 | A shot is a town event | Heard to about 177 m by day; armed police only when a gun is involved; walls dulling it unwritten | WS 16.2; CD Weapons; BP01 1.3.10; Q143 | partly |
| C083 | Suppressed .22 | Dropped 18 Nov; every row naming it is void | WS banner, 5.2, 5.4, 16.2 | ruled out |
| C084 | July weapon families not carried | Ice pick, straight razor, kitchen knife, .22, .38 snub, .45 automatic, brass and casing clues | WS 5.2, 5.3 | gap |
| C085 | Bottles as weapons | July spec lists a bottle and a bottle of "something" in kit; content rule bars drink | WS 5.2 Families 2, 7; CD The street is a weapon; FTM (a) | ruled out |
| C086 | Women, over-sixties and the priest | Frank's line against striking them dropped 24 Nov; the town reads such a blow one step heavier | BP01 RT-09; LH-13 | ruled out |
| C087 | Strike own people | Cost and a way back for first blow on Ron, Sheila, Pauline, a driver; third final | PP P01; Q088, Q092, Q096 | partly |
| C088 | No stealth meter; the frame breathes | Vignette and temperature track light value exactly; no icon | FIFTY 7; BP01 1.4.2; WS 6.2 | designed |
| C089 | Light scale | Day 1.0, lamp 0.7, unlit street 0.25, doorway 0.12; dark readable, never blind (5 m always visible) | BP01 1.1.5, 1.4.2; WS 16.1 | designed |
| C090 | Hiding | Still figure in a doorway counts at 0.12 and only as a shape beyond 8 m; back to a watcher hides the face; among 3 or more within 2 m a glance takes 0.7 s; behind a van or corner nothing is caught | BP01 1.1.5 | designed |
| C091 | Crouch | In by ruling 24 Nov (Q19), but no input, speed or effect on being caught is written | BP01 1.1.1, 1.1.5; BP11 C-270 | gap |
| C092 | Slow walk | Z held halves the reach of footsteps | BP01 1.1.1; BP01 1.4.3 | designed |
| C093 | Sound reach with masking | Radius from loudness minus the listener's ambient floor; rain, crowd, jukebox and traffic mask; a footstep carries 3.6 m at 3 am and nothing at noon | WS 3.2, 16.2; BP01 1.4.3 | designed |
| C094 | Noise ring | One ring on the ground at the true audible radius at the moment of a sound; July spec only | WS 6.2 | partly |
| C095 | Walls and doors dull sound; sleepers wake | A shut door or wall halves reach; sleepers wake over a fixed loudness; proposed | PP P09; BP11 gap list; Q198 | partly |
| C096 | Reading watchers | Head turns, longer look, pause in walk, two heads together, a figure at a lit window; at least 0.8 s warning | BP01 1.4.1 | designed |
| C097 | The street goes quiet | Talk near him stops when noticed; resuming tells him it is over | BP01 1.4.3; WS 6.2 channel 1 | designed |
| C098 | Attention channels (barks, behaviour break, one music stem) | Four redundant channels, any two enough; the music stem sits uneasily with "no combat music" | WS 6.2; CD How a fight feels | partly |
| C099 | Seeing assist | Optional outline of people facing him, off by default; never shows what anyone knows | BP01 1.4.6 | designed |
| C100 | Symmetry rule | If you can tell he is facing you and you are in light, he can see you; silhouette gate at 8, 18, 35 m; survey verb as fallback | WS 15.1, 14 B | partly |
| C101 | Mutual awareness and the standoff | Four states; the standoff gets a 0.4 s audio duck, once per event; not in the blueprint | WS 4.4, 6.2 | partly |
| C102 | Ghost of a witness's belief | Shown only when awareness was mutual; coat with no face, you, or the wrong man | WS 6.2, 14 A | partly |
| C103 | Forgiveness window | One optional slow moment when first noticed, off by default | WS 6.3 | partly |
| C104 | Tailing and being tailed | Target looks back every 20 to 40 s; a mark is a doubt shown first; no hidden distance fail; ends in a Ledger line | BP01 1.1.6; Q024, Q110 | designed |
| C105 | Being stared at, followed, crowded | Neighbour notices loitering and says so, then a complaint or report | DC rank 4; BP01 1.1.7 | partly |
| C106 | Stopping and blending in | Bench, wall, doorway, cigarette; a belonging stopped man draws no second look; a loiterer does | BP01 1.1.7 | designed |
| C107 | Drawing a watcher away | Thrown stone (O) or rattled bin; beat constable leaves his round and rejoins; a yard dog barks, food quiets it | BP01 1.4.8 | designed |
| C108 | Wrong place noticed faster | Places labelled public, by hours, private, forbidden; owner warns, warns again, then calls | BP02 2.2.6; WS 10 Phase 1 gate | designed |
| C109 | Coat change and shedding a slot | Change coat, second car, cap and scarf; sheds a slot only against witnesses who have not told; people who know him see through it | BP01 1.4.4; BP02 GV-02; Q056 | designed |
| C110 | Foot flight | No timer; lost after 7 s unseen or a gap over 70 m unseen; ginnels, yards, six vault places; Frank 5.5 m/s, constable 5.2 | BP01 1.5.1, 1.1.8, FIT-G4 | designed |
| C111 | Pursuing on foot | Runner at Frank's speed less 5%; collar from within 1 m; let go, talk or lower rungs | BP01 1.5.2 | designed |
| C112 | Pursuer rules | Constable announces himself 3 s before challenging, never sees through walls, searches 30 to 120 s after a lost chase, same chase resumes if seen inside | BP01 1.5.4, DP5-C03 | designed |
| C113 | Caught by a constable | Hand on collar then search; weapon or goods mean arrest; running is not a crime but the next challenge is on cause | BP01 RT2-22 | designed |
| C114 | Hiding indoors in a chase | Pursuer follows through a door he saw; an unseen shut door is not searched; shops are full of witnesses | PP P10; Q055 | partly |
| C115 | Arrest, no chase | July spec refuses any chase and works by identification; blueprint and CD have chases | WS 15.2 | ruled out (superseded) |
| C116 | Resisting arrest | Allowed and the worst outcome; the game does not warn | WS 15.2 | partly |
| C117 | Chasing a thief; stopping a thief | Owners and witnesses chase; a bag snatch Tom may stop or ignore, remembered either way | DC rank 15; NOTES-C items 9, 17 | partly |
| C118 | Chase length | Chases 1 to 3 minutes (ruling 24 Nov); bots' band median 30 to 90 s foot, 60 to 120 s car | BP01 DP5-C01, C02; BP11 C-276 | designed |
| C119 | Seven slots per act | Precursor, draw, act, victim, actor, flight, aftermath, each caught separately | WS 4.1; BP02 2.2.1 | designed |
| C120 | Identification ladder | Someone, a shape, a mark, a face, recognition; recognition needs knowing him, not distance; the dangerous witness is the one who knows you | WS 4.2; BP02 2.2.2, RT2-03 | designed |
| C121 | Walk to tell | A witness walks to a phone box or friend, visible, at least 30 real seconds; "Oi!" stops her 2 s | BP01 1.4.5; SM-01; FIFTY 3 | designed |
| C122 | Stopping a witness | Talk her round, pay, threaten, help or let go; threat stops a report, never the sister hearing; paid witness remembers being paid | BP02 2.5.2; FIFTY 4, 5 | designed |
| C123 | Willingness differs from certainty | Whether she will say it depends on what she was doing there; the answer is usually a secret, not a knife | WS 4.3 | designed |
| C124 | Wrong witnesses | Partial slots plus familiarity produce false accusation; false belief may stand | WS 4.6; BP02 2.3.2 | designed |
| C125 | Memory hardens | Accuracy falls while confidence rises (rung +1 per about 4 retellings); never confers indelibility | WS 15.6 | partly |
| C126 | The victim is a witness | The man struck perceives; being attacked guarantees rung 3; the survivor is the worst witness | WS 15.3; BP01 1.3.11 | partly |
| C127 | Witness after she signs | Can take it back if talked round or paid; threat adds to the case; no retraction existed before the proposal | PP P07; Q107, Q108 | partly |
| C128 | Police know only what was perceived | No arrest or statement without a person who saw or a search that found | AAA FAILURE-AND-FRUSTRATION FF-05; DC rank 1 | designed |
| C129 | No heat bar | Only what they know, shown in the world | DC rank 1; BP07 | designed |
| C130 | Officer struck unseen | A blow from behind gives no identity; he calls up within 30 s; second constable in 2 to 4 min | LH-12; Q001, Q002 | partly |
| C131 | Killing a constable, the long heat | Squad week, door to door, remand road, committal | LH-01 to LH-11; Q013 | partly |
| C132 | Crowd reaction to a fight | Looks, one gathers, witnesses quieter for a game hour, bystanders who saw a weapon flee; KCD2 first values: flee within 3 m, 2 to 8 react, warning then arrest at 30 s | BP02 2.5.3; S14 For LEDGER 10 | designed |
| C133 | A street on edge | Three seen deeds in two days: doors locked earlier, a second constable on the beat | BP02 2.5.4; FIFTY 19 | designed |
| C134 | Unseen deeds found | Found by the first routine passing; "Nobody saw." then "Ada knows." | BP02 2.5.5; SM-03; FIFTY 10, 20 | designed |
| C135 | Bodies | Dragged at 0.9 m/s, boot in 4 s, dock in 3 s; a sunk body never found, the missing man becomes the town's question | BP01 RT2-11; BP02 2.5.5; Q015 | designed |
| C136 | Absence noticed | A man who vanishes is asked after by landlady, mates and Ellis | DC rank 13; SM-04 | designed |
| C137 | Women and over-sixties read heavier | A blow on them is read like a weapon, travels faster, costs standing | LH-13 | partly |
| C138 | Threat as the main use of a weapon | Most of what a weapon does happens before anyone is hurt | WS 5.1; CD The ladder | designed |
| C139 | Talk as an alternative to a fight | Intimidation is a speech check in KCD2; a threat at a sit-down; typed threats never act by themselves | S14 Before the blows; Q081; AAA TALK-AS-PLAY TALK-08 | partly |
| C140 | Talk during a fight | A fight or shout breaking in on talk (talk drops, the person reacts) and walking off mid-talk have no rule; no document describes speaking inside a fight | BP03 checklist note (line 375) | gap |
| C141 | Police de-escalation by talk | Talk a police scene down; his GTA VI video item 2, judged a candidate | NOTES-HIS-VIDEO item 2, table | gap |
| C142 | Orders in the field | Digit then target: with me, wait here, watch that, fetch him, take this there, drive, lean on him; crew never block a door | BP01 1.7.1 | designed |
| C143 | A man at his side | Follows at about 2 m, stands in a fight and takes the second man, so two against two is fair | BP01 1.7.4; CD Tom, the crew and the odds | designed |
| C144 | Sending, eight verbs | Hurt, plan, frame, lean on a witness, move or hide a body, dock or beat one of his own, hit a rival's property, vouch; done next night by nerve against nerve | BP01 1.7.2, RT-08; CD Tom, the crew and the odds | designed |
| C145 | Accomplice risk | The man sent knows; his own nerve and loyalty ceiling; he is the risk, not the alibi | CD Tom, the crew and the odds; BP01 1.7.2 | designed |
| C146 | Crew who watch remember | A permanent loyalty ceiling; the frightened one talks | CD The aftermath; BP02 | designed |
| C147 | Crew and guns | No verb hands a gun to a crewman; Ron refusing to ride with the gun is a story need | Q142; BP11 C-345 | gap |
| C148 | Town's memory of deeds | Nothing clears a memory; money, threats and friendship change only what a person does with it | AAA MEMORY-SYSTEMS MEM-09; MEM-02 | designed |
| C149 | Gossip carries how a deed was done | Three blows and walk away is told differently from kicking him on the floor; the worst telling is never undone | BP05 GV-06; FIFTY 16; SM-05 | partly |
| C150 | Gossip cooling | A scuffle a day or two, wounding about a week, officer struck 7 days, a killing never | BP02 2.4.2 | designed |
| C151 | Beaten man remembers | A man Frank beat shows a mark and mentions it first; meets him within three game days | AAA MEMORY-SYSTEMS MEM-04; PLAYERS-STORIES STORY-05 | designed |
| C152 | Shopkeepers remember trouble | The grocer remembers a robber; refuse after a robbery; refusal after a threat not stated | DC rank 2; Q102 | partly |
| C153 | Others fight too | A feud between townspeople can become a fight the player may watch, join or break up | CD Tom, the crew and the odds | partly |
| C154 | Boxing club | Frank cannot be robbed there; men can be recruited there | BP01 RT2-13; BP02 recruits | partly |
| C155 | Fight camera row | Wider row 3.5 to 5.0 m back, both men's feet in at least 90% of frames, watchers seen; no reference width exists | CD Since 12 Oct; BP05 5.2; FTM C10 | partly |
| C156 | Measuring drills | Ten scripted drills (M1 to M10) and a 31-test tool; browser tuned to the sheet, Unreal tuned to the browser | FTM (f); tools/lane/melee_drills.py | designed |
| C157 | Fight and chase share of play | Fights and chases about 8% of play | BP07 (activity table, line 108) | designed |
| C158 | Rise in position, never in numbers | Tom never gets better at fighting; his people, weapons and name change the odds | CD Since 12 Oct Tom's rise; BP07 | designed |
| C159 | Perception cost | Only the Near band perceives, 6 Hz staggered, 1.2 ms budget with a gate | WS 17.1 | designed |

## Core needs action games usually lack (also in the table)

| need | rows |
|---|---|
| Threats as the alternative to fighting | C002, C005, C070, C071, C122, C138, C139 |
| Talk mid-fight | C140 (gap), C139 |
| Witnesses and gossip carrying how a deed was done | C119 to C127, C134, C149, C150 |
| The crew acting on orders | C142 to C147 |
| The town's memory | C148, C151, C152, C136, C060 |

## Contradictions and holes

1. Crouch. Older text says "there is no crouch" (ONE-SHOT-PROMPT s6, DESIGN-ADDENDUM A1, SOUND-PLAN SND-06, BP11 C-270 note, redteam panels). Jafar ruled it in on 24 Nov (Q19). BP01 1.1.1 and 1.1.5 say its input and effect on being caught are "not yet written"; RC lists "crouch out (SND-06) against in (6.6)" as an unresolved clash; BP06 6.6 has no part for the key. File: BP01 1.1.1, 1.1.5; BP11 C-270, C-312; RC.
2. Combos. Jafar ruled combos out on 24 Nov, yet FTM still sets band C14 (three-blow combination, 1.5 to 2.4 s) and drill M2; BP01 1.3.1 and LH-14c say none, while 1.3.2 keeps a counter. Hooks are in FTM C2 but BP01 names only jab and heavy blow. File: FTM (c) C14, (f) M2; BP01 1.3.1, 1.3.2.
3. Fists never kill, and what that leaves open. CD says whether a shove into a kerb can kill is open, whether the quay edge counts is open, whether the fall applies to fights Tom is not in is open, how rare is "no reference found". BP01 RT2-12 settles the conditions (heavy blow, within 0.4 m of the edge, already spent) and says never to Frank, never by a car, but the "3 s after a blow" window in FTM is a session choice, not a ruling. File: CD Since 12 Oct Knock-outs; BP01 RT2-12; FTM (f) "Choices to know about".
4. Knife only when finishing. BP01 RT2-11 and Q005 say a knife kills only by the finishing choice or the fall. LH-14a proposes a committed thrust into a spent man and leaves it as Q-H1 for Jafar (A thrust, B never as now, C any stab). Open until he picks. File: BP01 RT2-11; LH-14a; what-if/SUMMARY.md.
5. Kicks. BP11 C-341: the story's worked example has Frank "put the boot in" to a taxman; the part has no kick input. LH-14c proposes a kick only on a downed man. GV-06 had used a kicked man as its example; it was reworded. File: BP11 C-341; LH-14c; BP05 GV-06.
6. Chase against "arrest, no chase". WS 15.2 (approved) refuses any foot chase and works by identification; CD How fights end, BP01 1.5 and Jafar's 24 Nov ruling (chases 1 to 3 minutes) have foot and car chases. The later rulings stand but WS is not marked as superseded on this point. File: WS 15.2; BP01 1.5.1; BP11 C-276.
7. Takedown and choke. WS has wire, cord and a silent kill from behind; CD's four tiers and BP01 have only the cosh or fist from behind (knock-out) and say no finishers. Nothing says whether a ligature exists. File: WS 5.2 Family 4; CD Weapons; S14 For LEDGER 13.
8. Weapon lists disagree. WS: fists, brass knuckles, cosh, bottle, bar, bat, switchblade, kitchen knife, ice pick, razor, wire, cord, five guns. CD: cosh, knuckleduster, utility knife, flick knife, bat; sawn-off and old revolver. BP01: cosh, knuckleduster, knife, bat; service revolver and sawn-off. The July list is the one named "approved" but not the later word. File: WS 5.2; CD Weapons; BP01 1.3.6, RT2-14.
9. Bottles and drink. WS lists a bottle as a weapon, "a bottle of something" as kit and "a bad drink" as an accident; FTM's reviewer has already barred drink; the content rule forbids it. WS is not edited for it. File: WS 5.2 Families 2, 6, 7; FTM (a), (e).
10. Name and setting drift. CD, WS, FTM and S14 say Tom and a man who runs a bar ("Tom Novak" in WS); canon on wip still says Tom Nowak; the blueprint says Frank Nowak and Mickey's minicab firm (renamed 24 Nov). CD's July-versus-now table covers the bar but not the name. File: CD What changed from July; WS 6.2; BP changelog run 5.
11. "Tom never gets better at fighting" against hand skills improving "at most a quarter better" (23 Nov ruling). The newer ruling wins; CD Tom's rise and FTM have not been reworded. File: CD Tom, the crew and the odds; BP11 C-263; BP07 line 165.
12. No health bar against a minimal HUD switch. CD says the HUD exists as a settings switch; BP says no number of standing, loyalty, fear, heat on screen and no bar. File: CD How a fight feels; BP07 line 440.
13. "Closes in a little" against a wider camera. CD How a fight feels says the camera closes in a little; Since 12 Oct says the wider fight row stands and only a 0.8 s close-in remains. No reference width exists (Mafia widens nothing); the first target of a 3 m ring is unverified. File: CD Since 12 Oct.
14. Sound-layer timing. DESIGN says four layers within a frame of the blow; FTM C13 says only the impact is within 0.034 s. FTM wins (BP11 C-115).
15. Wind-up assist length. 1.25 to 1.5 times (FTM C5) against 25% (BP). BP wins (BP11 C-114).
16. Coat memory. AAA MEM-02 first said a changed coat stops a mark-only link; canon's ladder says people who know him see through it. The ladder wins. File: AAA MEMORY-SYSTEMS MEM-02; BP01 1.4.4.
17. Struck officer. Old RT2-02 made every struck officer know Frank, which breaks the blow from behind; LH-12 replaces it but is only "proposed" (D2 in what-if/SUMMARY.md). The Core, police.json and carol_ellis.json still carry the dropped Ellis line. File: LH-12, LH-13; BP02 RT2-02.
18. Study 14 numbers are not evidence. FTM says every Study 14 number (KCD2 and Mafia files) predates the 17 Nov outside-only ruling and must be re-measured from footage; BP01 1.3.1 still quotes 0.75 s and 1.27 s as "prior research". Most melee bands are judgement, the footage plan (12 clips) is not yet done. File: FTM top note, (e); BP01 1.3.1; S14.
19. Gaps the documents name. How a grab or pin ends; how much a wall or bonnet adds to a blow; what "a beating" costs Tom's body; how the quiet decision to finish is prompted and who may be robbed; the stare's duration; the length of the "three is a beating" stagger; police arrival time in a fight; defence as a rung; the bill when Tom wakes. File: COMBAT.md Left open; S14 Open blind spots; BP11 gap list 1.3.5 to 1.3.9.
20. Mafia stealth and KCD2 unarmed finishing. COMBAT.md 3.4 describes Mafia's bare-hand choke, knife kill and body-stashing as references only; the blueprint has no body-stashing from view, no distraction other than the stone and the bin, and no stealth objective (no sequence where being unseen is required). Only light, sound and symmetry carry stealth. File: COMBAT.md 3.4; BP01 1.1.5, 1.4.8.
21. Accidents and the threat verb as dominant strategies. WS named both risks (11.4, 11.5) and said BalanceLab would prove them. The blueprint carries neither the accident family nor the brandish outcome table, so the balance question is untested. File: WS 11, 14 D, 5.2 Family 6; BP01 1.3.6.
22. No separate verb for breaking up a fight; no rule for a chase with no passenger; walls dulling a shot; hold-up of an officer (Q032); a week of repeat beatings is only proposed. File: Q201, BP11 gap list GV-03, Q143, Q032, PP P15.
23. Guns rare and late against Mickey's revolver found at rung 2 near the start of Act II. File: BP11 line 362; BP01 RT2-14.
