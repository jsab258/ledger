# COMBAT-SYSTEM: one general system for fights, menace and stealth

25 Nov 2026, the combat and stealth pass (his Go, 07:47). Status of the whole: ready for review. It replaces the combat and stealth parts of the blueprint listed at the end (for the keeper). Canon and RULINGS on wip outrank it; his "LEDGER Combat: Final State" (12 Oct) is its starting point, and where this text differs from a ruling it says so and the point is in RULINGS-TO-REVISIT.md, never changed silently.

Numbers here are the simulator's (SIM/combat_sim.py, seed 1990), so text and code agree. Every number is a tuning value the loops retune; the rules are the design.

## The player wishes

What a fight in LEDGER should feel like and mean, in plain words. Every rule below serves at least one.

- W1. Ugly, fast, over in seconds. A fight is a scramble of a dozen blows, not a duel; you feel each one land, and you can lose.
- W2. Most trouble ends before the first blow. A look, a word, a name, a blade shown: menace is the everyday weapon, and the man in front of you decides by his own nerve whether to fold.
- W3. Anything a man could try in a 1990 street, Frank can try. The game answers by rule (what force, where, on whom, who saw), not by "you can't".
- W4. Sneaking runs on real senses. Dark, noise underfoot, a turned back, other people's eyes; it works, it fails believably, and getting caught is tense, never a reload.
- W5. The street watches and retells. Who saw, what they saw, and how the story of it travels and changes: kicking a man who was down is a different story from a fair fight.
- W6. Every blow has a price later, and there is always a way back. Injuries, police, revenge and standing follow; nothing ends or ruins a playthrough halfway.
- W7. Frank's power is people. Alone he is one man and two is deadly; with Ron at his shoulder the odds change.

Not a fighting game: depth goes where it feeds the social core (menace, witnesses, consequences); feel is AAA; no combos, no skill trees, no shooting depth, no lock-on, no health bars (his rulings).

## How to read this

Each part has How it works, Standard, Test, Source and Status, as the blueprint does. Parts CS-01 to CS-30. "The body rule" (CS-05) and "the temper in a fight" (CS-09) are the two rules most answers come from.

---

## CS-01 One fight model for everyone

- How it works: There is no combat mode and no special fight code for Frank. Every person in the Hook, Frank, his crew, a docker, a constable, two strangers quarrelling, uses the same actions (CS-02), the same body (CS-05), the same wind (CS-04) and decides by the same temper rule (CS-09). A fight between townspeople that Frank only watches runs on it too, so he can watch, join, or break it up (CS-14), and what happens is what the rules give. Each action is an act with the seven perceivable slots, so perception, memory and gossip treat a blow exactly like any other deed. The eight rungs of his ladder (stare, square up, threaten, shove or grab, strike, weapon out, weapon used, kill) stay as the street's reading of how far a confrontation has gone; they are not separate systems.
- Standard: one rule set; a test that swaps Frank for a townsperson in any fight gives the same outcome distribution for the same choices.
- Test: S: the simulator shares the body, wind, counter, surface and fall rules for everyone; the player's choices (style, target, tempo) and the townspeople's temper choices are separate functions, since one is the player's hands and the other the town's minds; Frank's critical injury becomes out (CS-15). The swap test (Frank's settings on a townsperson, same choices, same spread of outcomes) is owed, not run.
- Source: his design 12 Oct (the ladder, "other people fight too"); the moat (seven slots); KCD2's one rule set for player and NPCs (census M001 to M020).
- Status: designed.

## CS-02 Actions

- How it works: The whole verb set, keyboard and pad, no combos (his ruling of 24 Nov):
  - Move: walk, slow walk (Z), run, crouch (C, toggle or hold in settings; see CS-12), back off (move away while facing).
  - Guard (held right mouse / LB): hands up; blunt blows to the arms do little, wind still drains.
  - Slip (guard plus a direction tap): a short step out of a blow, about 0.3 s.
  - Jab (left mouse / X): quick, light.
  - Heavy (hold left mouse / hold X): committed, readable, cannot be cancelled. From a grab or in the clinch the same heavy comes out as a knee, an elbow or a headbutt (animation by range, one force rule).
  - Aim: high or low, by the stick or mouse held up or down as the blow starts (head or body); arms and legs are hit by chance or by a low kick. No five-zone rose, no zone switching, no feints (combos and their kin are out by his ruling).
  - Pull a blow (hold guard while striking): a third of the force, no knock-out past a count; for a lesson, sparring or a man Frank only means to frighten.
  - Kick (F / B): a low kick standing; on a downed man it is the boot (CS-14).
  - Grab (E / Y): collar or arm. From a grab: shove away, shove into a surface (CS-07), throw down, pin to a wall (holds, and opens talk), go for the weapon arm (disarm, CS-08), or from behind a choke (CS-13).
  - Weapon: draw (held semicolon / hold RB, cannot be undrawn unseen), put away, swing or slash (as jab), thrust (as heavy), throw (a thing to hand), drop, pick up (anything graspable within 1.5 m, CS-08).
  - Speak (the talk key mid-fight, Tab / d-pad): threaten, demand, offer, yield, beg, name himself, call his men (CS-10).
  - Hands up (hold the talk key and back): Frank yields (CS-14).
  - Help up, drag, carry over the shoulder (an unconscious man), put in a boot, roll into the water (CS-16).
  - A blow thrown within 0.45 s of a successful guard or slip is a counter: 0.6 of the wind-up, half again the force, and hard to defend. A guard raised in the last 0.15 s before a blow lands costs no wind (the KCD2 perfect block, without its icon). That is timing, not a combo.
- Standard: every action answers within 0.1 s; all rebindable; every action available on pad and keyboard; hold or toggle for guard, crouch and run (accessibility).
- Test: S: input map complete on both devices; B: each action in the simulator's table.
- Source: blueprint 1.3.1 to 1.3.4; KCD2 and Sleeping Dogs actions (census M001 to M040); his rulings 24 Nov (combos out, crouch in).
- Status: designed.

## CS-03 Feel

- How it works: Kept from the blueprint, which the melee feel sheet sets: a blow starts within 0.1 s; a jab lands in 0.25 to 0.40 s, a heavy in 0.63 to 0.85 s; hit-stop 0.025 to 0.13 s by blow; a brief close-in of about 0.8 s inside the wider fight camera (his camera ruling of 28 Oct); a small shake; four layers of sound; a struck man reels to the side he was hit. Every incoming blow is readable 0.45 to 0.80 s before it lands in shoulders, feet and breath. At most two men swing at Frank at once, 0.4 s apart; the others circle, block a way out, pick something up or try to grab him from behind (CS-11). No lock-on: the man the stick or mouse points at is the man hit; Frank slides to about 1 m in the wind-up; nobody is hit through a wall. Between blows a careful fighter keeps his hands up; a man who just missed or was blocked is open for about 0.3 s. Walls and low ceilings shorten a long swing (a bat in a passage becomes a jab with the end). Space limits numbers: a man needs about a metre of front to swing, so in a doorway or a passage only one can reach Frank at a time. The fight camera keeps every man within 3 m in frame where it can and, when one is behind Frank, his wind-up is heard (a scuff, a breath) 0.4 s before it lands; in rooms and stairwells the camera rides in close rather than through a wall.
- Standard: ER-FIGHT-01, 02 and 06 as in the blueprint (melee sheet C1 to C13); C14 (combination) is struck since combos are out.
- Test: S: melee drills at 1/60 s; H: "did you see the blow coming?"; the simulator's wind-ups match the sheet.
- Source: blueprint 1.3.1 to 1.3.3; FEEL-TARGETS-MELEE; census rows on hit-stop and reading (KCD2, Sleeping Dogs, RDR2).
- Status: pending (fist timings a lead, as the DECIDES-CHECK of 24 Nov says).

## CS-04 Wind and states

- How it works: Everyone has wind (0 to 1) and condition (hurt taken against his capacity, by kind: a big man 21, a boxer 15, a brawler 14, a wiry or knife man 12, Frank 12, the simulator's values). Every action costs wind (jab 0.12, heavy 0.20, kick 0.10, grab 0.08); wind returns at 0.12 a second only while he is not mid-blow, twice that with hands up; hurt lowers the ceiling; running, slipping and blows share the one wind. Below 0.18 a man is emptied: hands drop and he gasps, 1.5 s at a time, until his wind comes back (in the simulator a median of about 10 s, longer than blueprint 1.3.2's 4 to 8 s: a tuning item, R19), open to anything. So mashing empties Frank in a handful of blows and loses (his 12 Oct design). Blows land weaker as wind falls (force times 0.5 plus half the wind). States, the same for all: fresh; hurt (from 40% of capacity: guard slower, breath short, a stagger); beaten (at capacity: can barely fight, will yield or run if he can); down (on the ground 2 to 5 s, then up unless beaten or out); out (unconscious, CS-05); dying (a critical injury, CS-05); dead. Frank alone never reaches dead (CS-15). All shown in the body, never a bar.
- Standard: a player asked "who was winning?" answers right 4 times in 5 from the body alone (blueprint RT-11's test).
- Test: S: simulator states; H: the five-friend question.
- Source: KCD2 stamina as the core resource (census M016, M017); blueprint 1.3.7, RT-11.
- Status: designed.

## CS-05 The body rule

- How it works: One rule decides every injury for every person: what struck, how hard, where, and the state of the man struck. Nothing is decided by a listed case.
  - Zones: head (and neck), torso, arms, legs. An aimed blow goes where aimed; an unaimed one lands head 45%, torso 40%, arms 10%, legs 5%; a blocked blow lands on the arms.
  - Force: the action's force (jab 1.0, heavy 2.6, kick 1.7, boot on a downed man 1.6, shove into a surface 2.0) times the weapon (fists 1.0, knuckleduster 1.35, chair 1.7, cosh 1.9, brick 2.0, bat 2.3) times wind, half again on a man who did not see it coming, half again for a counter.
  - Blunt harm adds up by zone (the head counts a quarter more): bruise, hurt from 3, serious from 9.5 (a broken nose, cheek, ribs: hospital), critical from 15 on the head or 22.5 on the body.
  - Edges and points (a knife, a broken chair leg, glass) do not add up; each landed cut or stab draws its wound by kind and zone. A thrust to the body: minor 40%, serious 44%, critical 16%; to the neck or face: 25%, 40%, 35%; to an arm: 70%, 27%, 3%; to a leg: 62%, 32%, 6% (an artery). A slash is mostly minor (a body slash 72%, 25%, 3%). So a knife is usable from the first second of a fight, and what a stab does depends on where it lands; a body stab can kill (his ruling of 25 Nov).
  - Critical means dying: a man with a critical injury dies unless helped in time. Left alone, he dies about 55 times in 100; helped (a passer-by, Frank, the ambulance) about 20. Head harm, a bleed or a drowning all run through this.
  - Knocked down and knocked out: each landed blow can knock a man down, more likely with more force, more head harm and less wind. A knock-down from a head blow can knock him out: 10 to 60 s from fists, 30 s to 5 minutes from a weapon (boxing counts under a minute as an ordinary knock-out; over a minute is a hospital case). Out is never shown as dead: an unconscious man breathes, groans, twitches; a dead man does not, and the player can always tell them apart.
  - His fists line (30 Oct): fists alone, and a shove into a surface, never take a man past serious (whether a shove can kill is still open in his design, so this pass keeps it at serious). The fall can (CS-07). A knuckleduster is a carried weapon, not fists: its force is a third more and it is not capped, though it seldom reaches critical. Boots on a downed man are not fists: under this rule they can reach critical, rarely (his decision D2, recommended yes).
  - Burns, scalds and sprays are not in the body rule: hot fat, boiling water or anything thrown in a face to burn is out (cruelty as spectacle, canon). Fire (CS-22) harms by smoke and flame as an event, not as a hand weapon.
- Standard: deaths from fist fights alone at most 1 in 1,000; a knife fight kills in roughly 1 in 10 (England and Wales hospital data 2000 to 2005: 7.2% of stabbed patients died in hospital; a recent UK major trauma centre: 0.9%; an Icelandic national series: 17% died before reaching hospital); a beating to submission leaves most men hurt, about a fifth seriously.
- Test: B: the simulator; seed 1990, 2,000 fights a scenario: one-on-one fist fights 1 death in 2,000, on open street and at the kerb alike, by the fall (1 in 50 of the knock-downs of a spent man at an edge); a knife used by Frank 94 deaths per 1,000 fights; of all opponents in one-on-one fist fights (beaten or not) 68% end hurt, 21% serious. Rare-event rates rest on one to a few events and are leads, not measurements.
- Source: RESEARCH.md (stab lethality, knock-out bands, cold water); his rulings 30 Oct, 24 and 25 Nov; KCD2's knock-out flags (census).
- Status: designed; the edge table is judgement within the research bands (no region-by-region source reached).

## CS-06 Weapons as data

- How it works: A weapon is a row of data, never a special case: kind (blunt, edge, firearm), force, wind-up, reach, wind cost, how many blows before it breaks, whether it hides under the coat, the menace it carries when shown, its noise, what evidence it leaves (prints on smooth handles, blood, a dent, fibres). Carried: knuckleduster, cosh, bat, utility knife, flick knife (his 12 Oct tiers; every make fictional). Things to hand break: chair after 2 blows, brick 3, dustbin lid 4, wheel brace never; anything graspable within 1.5 m that the props list marks can be picked up and swung or thrown (a brick, a chair, a crate lid, a length of pipe, a cargo hook, a snooker cue, an ashtray, a stall pole). Never a bottle, a glass or anything to do with drink (canon); no dog is ever harmed. A man losing looks round for something to hand (CS-09). Guns are CS-23.
- Standard: every weapon a data row; each has its answer (a grab on the weapon arm, a chair, numbers, running). A knife against one unarmed man nearly always wins, as in life (the simulator: 99% of decided fights); its price is the body count and what follows, and against two men it wins about 3 in 4. Carrying: two things under the coat at most (more shows); the cab's boot and the office are stashes, searchable by the police with cause. A thrown thing hits by its force at half the wind-up, aimed like a blow, and is left where it falls; a carried knife can be thrown but is then gone.
- Test: B: the simulator's weapon table; S: the props list carries the graspable flag; content check: no drink item flagged.
- Source: his design 12 Oct (four tiers, things at hand); blueprint 1.3.6; weapons spec (the bottle struck by canon); census rows on weapon pickup and breakage (Sleeping Dogs, Yakuza, GTA).
- Status: designed.

## CS-07 The street as a weapon

- How it works: Surfaces are force, not finishers. A shove or throw into a hard surface (wall, shop shutter, railings, car bonnet or door, kerb, step, phone box, quay bollard) hits at force 2.0 on the body or head and the man is out of the fight about 4 s; glass (a shop window, a car window, the phone box panes) adds a cut by the edge rule. The fall: a man knocked down near a kerb, step or wall foot who was already spent (three heavy blows or one weapon blow taken, as RT2-12) has his head strike it: serious about 1 in 10, critical 1 in 50; since a critical man dies only about half the time, deaths run below RT2-12's 1 in 50 to 1 in 20 (listed in RULINGS-TO-REVISIT R17). The fall applies to everyone's fights, not only Frank's (R18). So a fight by the kerb carries a small, real risk, and the cost comes after. The quay edge: a man thrown or falling in climbs out at the nearest ladder within a minute if conscious; if unconscious with his face in the water he is dying (critical) and dead in about two minutes unless pulled out (Tipton: cardio-respiratory arrest about 130 s after submersion). This settles the open question in his design (does the quay edge count): it counts through drowning, not through the fall; listed in RULINGS-TO-REVISIT R5 so he can overturn it. Frank never swims (his ruling) and can pull a man out from the steps or a ladder. Car doors can be slammed on a man (force 2.0 to an arm or the head). Doors: slam, hold shut, kick open (a locked door takes several kicks and is heard). Wet cobbles: a heavy blow or a run on wet stone slips 1 time in 20 (a stumble). Light can be changed: a bulb broken, a switch flicked, which changes CS-12 at once.
- Standard: seven places first, fitted by height (blueprint 1.3.5); every surface move fully animated with no cut-away, gore light (his ruling 24 Nov, canon).
- Test: B: kerbside scenario in the simulator (1 death in 2,000 fist fights at seed 1990, too few to measure the rate); S: each place triggers its paired move.
- Source: blueprint 1.3.5, RT2-12; his 30 Oct fall ruling; Study 17 (Yakuza's places, not its finishers); RESEARCH.md (cold water).
- Status: designed.

## CS-08 Grabs, holds, chokes and the ground

- How it works: A grab works unless the man slips it (his defence). From a grab: shove, shove into a surface, throw down (he goes down), pin to a wall (holds about 2 s each press and opens talk: a pinned man can be spoken to live, CS-10), take the weapon arm (disarm: 40 in 100 it comes free and drops to the ground, where anyone may take it; in the simulator a disarmed weapon simply leaves the fight, the pick-up is a build test). A man may grab Frank from behind while another hits him; Frank breaks free by pressing grab with his wind (a fresh Frank in about 1 s, an emptied one in 3). A choke in a fight works only from behind on a man busy with someone else (one of Frank's men, say) and takes half as long again as on an unaware man; from the front it is a grab. On the ground: a downed man can be kicked or struck (CS-14), helped up, or left; he gets up in 2 to 5 s unless beaten or out; a man on the ground can grab an ankle. No wrestling minigame: ground fighting is the downed state and the blows on it.
- Standard: every hold has a way out; a disarmed weapon is a real object on the ground.
- Test: B: the simulator counts disarms both ways; S: a dropped knife can be picked up by the other man.
- Source: KCD2 clinch, Sleeping Dogs grapples (census M021 to M030); his design (shove, grab, pin).
- Status: designed.

## CS-09 The temper in a fight

- How it works: Every half second each man not acting chooses: press, hold (hands up, circle), back off, look for something to hand, call for help, yield, beg, or run. The choice comes from his will to fight: his nerve, plus his friends still standing, minus the fear of what he faces (the menace of the weapon shown: knuckleduster 0.35, cosh 0.45, bat 0.55, knife 0.75, gun 1.0), minus how hurt he is, minus being outnumbered, minus Frank's menace (what the town has seen him do); grudge adds. Low will: he runs if he can, else yields; beaten and still facing it, he begs. Watched by his own people, a man stands longer; some call a bluff whatever their nerve. A man with high law shouts for the police; a man with a tie to the victim steps in (the temper model's rule). A provoked man starts trouble only with cause: a bump, a stare held, a grudge, a job; never at random (not Yakuza's street encounters). A man who walks away from a fight and comes back finds it where the tempers left it: men remember, and a fight half-won is resumed or settled by talk. Frank's crew decide by the same rule plus regard and loyalty: a frightened one runs; an angry one may go too far (a crewman with high grudge may keep hitting a downed man unless told to stop).
- Standard: every person in a confrontation can fight, freeze, back off, yield, beg, run or call for help, and the choice reads from the temper the player can see (stance, distance, voice).
- Test: B: the simulator: in one-on-one fist fights against a careful Frank about 2 in 5 men yield and 1 in 7 run; against a knife half run; S: the temper model's golden rows.
- Source: the temper model (24 Nov, nerve, greed, mouth, law, grudge); Philpot et al. 2020; KCD2 and RDR2 surrender and flee (census).
- Status: designed.

## CS-10 Talk in a confrontation

- How it works: Menace is the main weapon (W2). Before or during a fight Frank can speak, a 1 to 2 s act he can be hit during: threaten (a word, or with a weapon shown), demand (leave, pay, tell me, hand it over), offer (money, a truce, a way out), bluff (claim men or a gun he has not got), name himself ("Mickey's nephew", later his own name), call his men, yield. The rules decide, the AI only voices: a threat folds a man if his nerve, plus pride (about 0.15 for each of his own watching, and a little of his own), is under the threat (a word 0.5, a weapon shown 0.8) times 0.8 plus 0.4 of Frank's menace. A bluff counts as a word, and a man who later learns it was a bluff lowers Frank's menace with him. An offer moves him by greed; a name moves him by what he has heard of Frank. Others speak too: beg, offer, threaten back, call Frank's bluff, shout for help. A pinned or yielded man can be talked to live (the claim check and the hard rule apply; the line he says is from what the Core decided). A threat stops a report to the police, never the street's talk (his ruling of 3 Oct). The threat's weight is general: 0.5 for a word plus 0.4 times the menace of what is shown (a cosh 0.68, a knife 0.8, a gun 0.9). A standoff is two sides each with a weapon shown: every beat each side's temper chooses hold, talk, back off or strike, and the first to move commits the street to rung 7. A cover story ("I'm here for a fare") is a claim: believed when the slots fit (right clothes, a reason for the place and hour, the cab outside) and the listener does not already know better; a bad fit makes him uneasy (CS-12). Owning up to a lesser deed is a claim too, weighed the same way. Frank can offer the police money only if the officer is bent (CS-19). Spoken threats to the live talk count as deeds (the live-play checker reads deed lines for threats, RULINGS 3 Oct).
- Standard: most confrontations end on rungs 1 to 4 (his design); a threat is not a sure win.
- Test: B: the simulator's threat table: at the start (Frank's menace 0.3) a bare word folds 12% of lone men, a cosh shown 28%, a knife shown 47%; two men together 0%, 2% and 5%. At menace 0.8 (a feared man): 20%, 51%, 81%; two men 0%, 8%, 25%. S (build test, not simulated): every man who folds to a shown weapon is a witness to rung 6.
- Source: his design 12 Oct and ruling 3 Oct; the temper model; census (RDR2 intimidation, GTA aiming at people, Hitman's lack of talk; LEDGER-only rows for talk mid-fight).
- Status: designed.

## CS-11 Several men, crews and tactics

- How it works: At most two swing at one man at once (a token), the rest circle, cut off the way out, grab from behind, or pick up something. Crowds are bodies: they block a run and a swing, and a wild blow can land on a bystander (then he is in it). A brawl spreads by ties: friends of either man join by their temper. Each outfit has its way: the dockside syndicate's men come in numbers and grab; Cammack's crew are quick to draw a knife and quick to run; Agar's men avoid fists and send for help or the police. When the man who leads them goes down, or half are beaten, the rest's will drops. Frank's men act on orders (stay back, take that one, hold him, stop, get him out) and otherwise by temper; a blow can land on a friend in a crowd (friendly blows are possible, about 1 in 30 swings in a close press). A beaten crewman is off the roster for his hospital days. Two against one is deadly and three is a beating; Ron at Frank's shoulder turns two against one into a fight he usually wins.
- Standard: the blueprint's FIT-P18: a skilled player wins a fair two against one about one time in four, a masher under one in ten.
- Test: B: the simulator: a careful Frank wins 2 v 1 29% (43% lost, 28% stopped by a bystander or the police), a masher 0.1%; 3 v 1 1% (84% lost); with Ron (2 v 2) 78%.
- Source: blueprint 1.3.8, FIT-P18; his design (the crew changes the odds); census rows on group AI (GTA, Sleeping Dogs, Yakuza, KCD2).
- Status: designed.

## CS-12 Senses and stealth

- How it works: Stealth is the perception ladder canon already holds, with these settled:
  - Sight: a watcher sees only where he faces; how sure he is grows with light, nearness, movement and time in view. Light values as the blueprint: day 1, lamp 0.7, unlit street 0.25, doorway 0.12. A still figure in a doorway is at most a shape beyond 8 m.
  - Crouch (in, his ruling of 24 Nov; this settles the contradiction): crouch halves footstep reach and makes Frank's shape half as easy to pick out beyond 4 m in the dark, at the cost of speed (1.2 m/s against 1.6 walking). It does nothing in light within 4 m: a crouching man under a lamp is a man crouching, and crouching where nobody crouches is itself odd to anyone who sees it.
  - Noise: reach set by act, surface, hour and weather: a walking footstep at night about 3.6 m on dry flags, a quarter more on wet cobbles, 1.7 times on gravel, about twice on a metal deck, more on broken glass; rain halves it; the day's traffic drowns it. Every noise the rule hears, the player hears at the same strength (ER-SND-01).
  - Alertness: calm, uneasy (heard something: turns, looks, walks to look), alert (knows someone is there: searches the likely places, calls out), engaged. A calm man glances round now and then, more in daylight and busy places; an uneasy one far more. He settles back to calm after about a minute, and remembers there was a noise.
  - Other watchers: everyone sees everything their senses allow; a takedown seen is a deed seen (CS-17).
  - Light can be changed (CS-07); a torch shows its carrier; a lamp going out is noticed by anyone who sees it or who knows the street (a constable on his round, a neighbour at her window) and makes them uneasy. Fog halves sight beyond 10 m; rain halves noise reach.
  - Indoors: floors and stairs are surfaces (a bare stair creaks at about twice dry flags; carpet halves it); walls and shut doors cut a sound to a quarter, an open door to a half. Sleepers hear at a third of a waking man's reach and wake uneasy. A dropped thing, broken glass and a blow land as noises at their own reach (glass about 15 m at night, a blow about 8 m, a shout 40 m).
  - Frank's men on a quiet job are noise and light like anyone: a crewman with low nerve or high mouth chatters unless told to keep quiet (an order); a lit cigarette is a light point visible far in the dark and is seen even by a man who cannot see the smoker.
  - Clothes: a dark coat at night makes his shape a fifth harder to pick out; a mask or scarf hides the face slot but is itself a give-away (a masked man is read as up to something); disguise fools strangers, never those who know him (blueprint 1.4.4).
  - A man found unconscious: the finder acts by temper: helps, fetches help or the police (law), robs him (greed), or walks on (nerve low); a found man is a story that travels.
  - No meters: alertness reads in heads, posture and voice; the optional seeing assist outlines only people facing Frank (blueprint 1.4.6).
- Standard: stealth works and fails believably: in the dark, crouched, it mostly works; under a lamp or by day it mostly does not; a loud surface is felt.
- Test: B: the simulator, approach from 12 m behind an unaware man and a choke: doorway dark, crouched, wet cobbles: 58% put out, 13% spotted, 23% broke free, 7% turned at the last moment; unlit street walking 34% out, crouched 41%; under a lamp crouched 18% out, 73% spotted; by day walking 15% out, 77% spotted; gravel and metal decks cut success by a seventh to a quarter (crouched, unlit, against wet cobbles' 41%: gravel 35%, metal deck 31%).
- Source: canon (perception ladder); blueprint 1.1.5, 1.4.1 to 1.4.3, 1.4.8; census (KCD2 noise and visibility, Hitman suspicion, RDR2 witnesses); RESEARCH.md (no published detection timings found: these are judgement).
- Status: designed; the numbers are judgement until the KCD2 and RDR2 seeing study (1.4.1's deciding row) is done.

## CS-13 Takedowns from behind

- How it works: An unaware man reached within 1 m from behind can be taken by any action; nothing is instant or certain.
  - Choke (grab from behind, held): a carotid hold puts him out in about 7.5 s (4 to 11; forensic sources say 5 to 10). Each second he may break the hold (about 1 in 30 at the start, more for a big man and as Frank's wind goes); the struggle is heard about 6 m. Released at once when he goes limp, he is out 10 to 60 s and wakes with a sore throat and a grudge. Held on past that, deliberately (Frank keeps holding; the body shows it plainly, the man goes still), he is in danger: no risk for the first 20 s more, then the chance of death rises by 1 in 100 a second: 10% at 30 s, 40% at a minute, 70% at 90 s, near certain at two minutes (breathing stopped at 62 to 157 s in one forensic series; no firm threshold was found, so this curve is judgement). This is his decision D1 (recommended: in, as a choice the player must hold).
  - Cosh or any blunt blow: the body rule with force half again on a man who did not see it coming, aimed at the head. Once he is reached (the simulator): out about 6 in 10, knocked down but conscious about 3 in 10, staggered 1 in 10, death about 1 in 200.
  - Fist from behind: out about 1 in 8, knocked down 1 in 7, otherwise a staggered man who turns to fight.
  - Knife from behind: by the edge rule where it lands; once reached, a thrust kills about 1 in 8 (some later, in hospital).
  - Failure: the man hears the last step (more on loud ground, walking not crouched, if he was uneasy) and turns: a fight with Frank close and the man startled. An officer struck unseen does not know it was Frank (his ruling of 24 Nov). A constable or anyone knocked out remembers being struck, and his own last sight before.
- Standard: no instant kill, no guaranteed knock-out; failure believable and readable.
- Test: B: the simulator: from approach to result (unlit street, crouched, wet cobbles): choke out 40%, broke free 17%, spotted 38%; cosh out 35%, knocked down 15%, staggered 6%, dead 0.2%; fist out 7%, staggered 43%; knife dead 8%; the held choke by the curve above.
- Source: RESEARCH.md (carotid hold timings; knock-out bands); his rulings 24 Nov; census (Hitman subdue, RDR2 and KCD2 stealth takedowns, GTA VI unconfirmed).
- Status: designed; D1 for him.

## CS-14 How a confrontation ends, and the quiet after

- How it works: Ends: someone backs off, runs, yields or begs, goes down, is knocked out, a bystander steps in (the more people watching the likelier: odds rise about a tenth for each, Philpot et al.), the police arrive (a beat constable first, then more), or Frank's men or the other man's friends pull him away. A man who steps in is answered by each fighter's temper: most stop; a high-grudge man shoves him off and he is in it. Frank's own yield (hands up) is answered by the other side's temper and purpose: a man defending himself leaves; a robber robs (RT2-13); a rival's men may take him to their boss; a man with a grudge may land a few more, the street reading that as worse. Provocation counts: if the other man struck first, or she swung first, the reading of Frank's answer is lower (times 0.7) as long as he stopped when it stopped. After it, with the other man down or yielded, Frank may: leave; help him up; rob him (paper money, a weapon, goods; the town calls it robbery); take him (hold someone overnight, his ruling: one night, nothing tied shown, a story the man tells after); speak to him live; or finish it. Finishing is never a move in the flow of the fight: with nobody else standing, Frank stands over him and holds strike or kick for 2 s, asked twice (blueprint RT2-11). The blow on a downed man, and beating a man who pleads, are fully animated with no cut-away (his ruling 24 Nov), gore light (canon). What the blows do is the body rule: fists stay at serious; boots can reach critical (D2); a weapon can kill. Watchers read it as worse (CS-17). A man yielded and spared remembers it (regard up a little, grudge down).
- Standard: a way out at every moment (ER-FIGHT-03); every ending leads on.
- Test: B: the simulator: in public one-on-one fist fights about 15% are ended by a bystander and 2% by the police; Frank finishing a downed man with three blows: with boots 15.5 deaths per 1,000 fights (about 1 in 50 of the fights he won), with a cosh to the head 42 per 1,000 (about 1 in 22). A cue before a blow that could kill: the downed man stops moving his arms to cover his head, and Frank's breath changes; the second ask names it ("He's not moving. Again?").
- Source: his design (how fights end, the quiet decision); blueprint 1.3.9, RT2-11, RT2-13; his rulings 24 Nov (holding overnight).
- Status: designed.

## CS-15 Frank losing

- How it works: Frank cannot die (12 Oct). When the body rule would make him dying, he is out instead. Beaten or out, he comes round on the pavement, in a neighbour's kitchen or in hospital (hospital costs days and the bill his 12 Oct design names, and plants a witness; the blueprint's "never money" is listed in RULINGS-TO-REVISIT R6, his design standing meanwhile). Where he wakes follows from where he fell and who found him: a quiet yard, the pavement; a neighbour with regard, her kitchen; anyone with law, or a serious injury, the hospital, in control within 60 real seconds with the cost said. What it costs comes from who beat him and why: robbed by men who rob (RT2-13, kept), taken to their boss for a talk and a demand (a rival's men), cautioned and cuffed (a constable), left (a man defending himself). He carries marks for days (CS-18), people see them and say so, and the town knows he lost (his standing, not a number). Always a way back: the men who did it have names and routines; he can front them, send men, pay, talk, or let it go. A run of losses costs more than money: a crewman who sees Frank lose again may leave (regard), a street he cannot hold goes to a rival; each has a way back by the same rules. Nothing ends or ruins the playthrough (the standing principle).
- Standard: ER-FIGHT-04 (in control within 60 real s); no dead end.
- Test: B: the simulator ends a lost fight with Frank beaten or out and never dead (5% of careful one-on-ones, 43% of 2 v 1); the come-round itself is a test for the build (S: every lost-fight route reaches a come-round within 60 real s), not run in this simulator.
- Source: his rulings 12 Oct, 24 Nov; blueprint 1.3.9, RT2-13.
- Status: designed.

## CS-16 Bodies and evidence, 1990

- How it works: A body or an unconscious man can be dragged (0.9 m/s), carried over the shoulder (slower, both hands taken), put in a boot (4 s), rolled into the dock from the quay edge (3 s), or left. Bodies are found by people on their routines and by smell after days; a missing man is noticed by those who expect him. Evidence is what 1990 had: fingerprints on smooth surfaces (a knife handle, a car door, glass), compared by hand against records on the 16-point standard, slow (days); blood on clothes until washed in water and private; blood group, no DNA database (1995); a weapon with a history (where bought, who saw it); fibres and the coat; tyre and shoe marks in mud; witnesses above all. Getting rid of a weapon (down a drain, into the dock) is itself a deed someone may see. A car pushed off the quay with a body in it is a big, loud deed: the car is the firm's or someone's, the registration is traced when it is raised (divers come for a car seen going in, or one reported missing), and the boot is searched. Blood in a boot stays until scrubbed with water in private, and a car search finds it. A bloodied coat can be burnt (a fire in a yard or a grate, smelt and maybe seen) or washed. Carrying, dragging or dumping a body is read by anyone who sees it as a killing seen, at the grave band, whether or not they saw the blow.
- Standard: the police know only what someone perceived or a search found (FF-05).
- Test: S: golden rows: a print on a knife handle names Frank only if his prints are on file (after an arrest).
- Source: RESEARCH.md (16-point standard 1953 to 2001; NAFIS from 2001; DNA database 1995); blueprint RT2-11, 1.6.7; weapons spec.
- Status: designed.

## CS-17 How the street reads it

- How it works: Every confrontation is a deed with the seven slots plus how it was done (provocation included, CS-14): the weapon, from behind, on a man down, on a man who yielded or begged, the victim's sex and age, numbers. Witnesses catch what their senses allowed (a shape, a coat, a face) and remember the manner. The reading is severity (the worst injury) times manner: from behind 1.3, on a man down 1.5, on a man who yielded 1.6, with a weapon 1.4; on a woman or anyone over sixty 1.5 (the town's line, now his line is dropped, RT-09). Gossip carries the manner with the deed and blurs it with distance and retelling (a knife becomes "he cut him up", a fair fight becomes "he jumped him" in the mouth of the loser's friends). The reading moves the town's menace (people fold sooner), fear (some stop using the firm: fares refuse, a frightened driver quits), regard (a fair fight can earn it; kicking a man down costs it), and the local paper and pirate radio take the grave ones. Service is a temper decision after any deed a person knows: a shopkeeper refuses (regard low, nerve high) or serves frightened (nerve low); the retired doctor refuses after a killing he knows of if his law is high; a landlady Frank hurt puts him out. A repeated deed adds: the street's mood over the weeks follows how much violence it has seen and settles slowly when it stops; it is never wiped (canon).
- Standard: the same injury reads differently by manner; a player can hear the manner come back to him in talk.
- Test: B: the simulator's consequence counts by band (talked of, bad, grave); S: gossip golden rows carry the manner slot.
- Source: canon (moat, gossip); 30 Sep witness ruling; the fifty-things finding (how a deed was done is not kept with the story); his ruling 24 Nov (RT-09 dropped).
- Status: designed.

## CS-18 Injuries and their days

- How it works: Every injury is a record on the person with its days, by level: bruise a day or two; hurt (a cut lip, a black eye) three days, shown; serious (broken nose, ribs, a stab stitched) a hospital stay of 3 to 14 days and marks for weeks; a broken arm in plaster for weeks, changing what he can do (one-armed: no heavy blow with that arm, driving clumsy), which answers the story's need for a lasting injury (C-338). Hand injuries from punching (split knuckles) show and slow the grip a day. Head knocks blur sight briefly. A man fighting on while hurt worsens his injury and collapses sooner. Townspeople and crew heal on the same clock and are off their routines meanwhile; a hurt docker misses shifts and that is talked of. Frank's marks are give-aways (blueprint 1.4.4). No healing items (his ruling); a retired doctor stitches for money and remembers.
- Standard: condition shows in the body, never a bar (his design).
- Test: S: injury records last their days; the simulator totals hospital days (seed 1990: about 87,000 man-days over 44,000 fights).
- Source: blueprint 1.3.11, RT-11; his rulings 24 Nov (no armour, no healing items).
- Status: designed.

## CS-19 Police, charges and the heat

- How it works: The police act on what is reported and seen. The charge follows the injury and the manner, in 1990 terms: a bruise, common assault (up to 6 months); hurt, actual bodily harm (s.47, up to 5 years); serious, wounding or grievous bodily harm (s.20, up to 5 years); serious with a weapon, on a man down or yielded, or critical, GBH with intent (s.18, up to life); a death, manslaughter, or murder when the weapon or the finishing shows intent; assaulting a constable, Police Act 1964 s.51. A report needs a witness who tells or a victim with high law; a threat can stop that, never the talk. Arrests lead to custody, interview, charge, bail or remand and court as the 1990 police research describes. Killing a constable brings the long heat (his ruling of 24 Nov: always recoverable, bribery possible, an officer struck unseen does not know who; LONG-HEAT.md is the design). Bent officers can be bought (DS Ellis about £800 then £100 a week, a missed week ends it: his ruling). In a fight a beat constable is a person on the same rules with a truncheon (a weapon row like a cosh) and a radio: arriving, he shouts to stop, then tries to hold the man he takes to be at fault; if resisted he strikes and radios, and help comes in minutes (a panda car first). Threatening an officer is a deed and a charge (obstruction or assault, s.51). Holding a constable (a locked room, overnight) is a grave deed: he is missed at his next point, his station searches for him, and the long heat's rules apply if he is badly hurt. Taking his radio or notebook is theft from an officer, read grave. A constable challenges a man on what he sees (a weapon, blood, running, a known face at a wrong hour). The inquiry into a civilian's death or a body found is CS-27.
- Standard: no charge without what a witness or search gives; every route recoverable.
- Test: B: the simulator maps every injury to its charge (seed 1990: common assault, ABH, s.20, s.18, manslaughter and murder all present); whether a charge is laid, which needs a witness, is a build test (S), not simulated.
- Source: RESEARCH.md (OAPA 1861, CJA 1988 s.39, Police Act 1964 s.51); his rulings 3 Oct, 24 Nov.
- Status: designed.

## CS-20 Revenge and the man who comes back

- How it works: A beaten man's grudge times how badly he was hurt and shamed decides what he does: lets it go; tells (by his law dial); comes back alone (high nerve) or with friends (low nerve), at a time his routine and Frank's cross, usually within three game days (STORY-05); or sends word to whoever protects him (a rival outfit takes it up as an insult to them). A man whose friend was beaten may come instead. Revenge can be met by fighting, talking (an apology, a payment), or sending men first. Settling a grudge ends the feud but never the memory (canon). A man Frank beat can also be recruited if his regard turns (a fair fight, a spared yield, money).
- Standard: every man Frank beat crosses Frank's path again within three game days (STORY-05, a meeting, not always a fight); whether he takes revenge, and when (that day or weeks later, when a chance or friends come), is his temper's.
- Test: B: the simulator draws revenge and reports as rates from grudge, law and the injury: about 3 in 10 beaten men take revenge and about 1 in 12 report it; S (build): the routine-crossing rule.
- Source: the temper model (grudge); PLAYERS-STORIES STORY-05; fifty-things finding (returning people).
- Status: designed.

## CS-21 Sending men to do violence

- How it works: Frank orders a man hurt, frightened or taught a lesson through a crewman (D56's first crime verb). The crewman carries it out by the same rules, and his temper decides whether he does it as asked, less, or more (a high-grudge man goes too far). He is a second person who knows, with his own nerve and loyalty (his design: the accomplice is the risk, not the alibi). Frank striking or threatening one of his own men costs regard with him and with every crewman who sees or hears of it; a man with low regard and high nerve refuses an order or quits; with high grudge he may sell Frank to a rival. Rivals may go for Frank's men to get at him, and Frank hears of it through the town's talk or the man's absence. A crewman carries only the weapons Frank gives him, and a crewman with a gun follows the same dial as Frank (CS-23). A send to kill is possible within canon: rare, the crewman may refuse by regard and law, and he knows forever (raised in RULINGS-TO-REVISIT, not a decision for him: canon already allows killing).
- Standard: the result of a send is decided by the fight rules, not a dice roll on success.
- Test: B (owed): sends through the simulator with the crewman as the fighter; not run in this pass.
- Source: his design 12 Oct; D56.
- Status: designed.

## CS-22 Fire

- How it works: Fire can be set at any time and can kill (his ruling). A fire spreads by material and wind, is seen and smelt, draws a crowd and the fire brigade, and a man trapped inside follows the body rule (smoke critical in minutes). Arson is its own deed, read grave if anyone was inside.
- Standard: his ruling; the street reads it as grave.
- Test: S: golden rows for an empty and an occupied building.
- Source: his ruling of 24 and 25 Nov.
- Status: designed; the spread model (terraces, cars, the warehouses) is a gap for the place parts, named here so it is not lost.

## CS-23 Guns, when they come

- How it works: Guns are rare and late (his ruling, end state A). A gun is a weapon row with the highest menace; a shot is heard about 177 m by day and kept by whoever hears it. Being shot at: men without guns run or take cover behind anything solid (a van, a wall, a stall), which blocks a shot; men with guns shoot from where they stand and run when outmatched (blueprint RT-10). Hold-ups: a threat at menace 1.0 through CS-10. A hit follows the body rule with a point wound far worse than a knife's. The dial (Fists, Shown, Fired, War) moves only on a gun seen or heard: shown moves the town to Shown, fired to Fired, a gun killing to War, and War brings armed officers from outside and searches on cause. Carrying a gun is a charge in itself (Firearms Act, years), threatening with one a worse one. A wall stops a shot; a shut door or a building's walls muffle the sound to about a quarter of its reach. A search of the office that finds a gun is a charge and a mark on the firm's name. In the blueprint today, before War a hit "wounds and never kills"; this pass recommends the body rule for guns too (RULINGS-TO-REVISIT R3; his decision D3).
- Standard: AAA when used, feel numbers to be measured (blueprint RT-10).
- Test: B: guns enter the simulator as a weapon row once their feel is measured.
- Source: blueprint 1.3.10, RT-10, RT2-14; his rulings.
- Status: pending (late by his ruling).

## CS-24 Frank's growth

- How it works: His ruling of 23 Nov (A, C and a light B): Frank rises mainly in position (crew, name, weapons, the menace the town has seen); skills are taught by those who trust him and kept if lost (Ron teaches the slip and counter window, the pin and the choke; the boxing club teaches guard and wind); hand skills improve quietly with practice, at most a quarter better (a wider counter window, less wind per blow, a firmer grab). No numbers shown, no skill tree. Sparring at the boxing club or with Ron is practice without hospital (pulled blows: force at a third, no knock-outs past a count).
- Standard: at most a quarter better; no skill tree.
- Test: B (owed): the simulator with Frank's defence and wind costs at 1.25 times, to show the gain stays inside a quarter; not run in this pass.
- Source: RULINGS 23 Nov; his design (Frank's rise).
- Status: designed.

## CS-25 Difficulty, assists and accessibility

- How it works: No difficulty levels (D27, D30), only assists that change their own thing: longer wind-ups (25%), auto-resolve a fight (the same fight at a different tempo, decided by the same rules), the seeing assist, sound shown as words, hold or toggle for guard, crouch and run, full rebinding, subtitles with speaker names, danger cues readable without colour, reduce motion (the shake), a gore setting (blood and marks lighter), a simplified scheme (one button strikes, guard is automatic against the man in front, timing still counts), and the minimal HUD switch his design names (a small figure for Frank's state, off by default; it never shows anyone else's). Balance over the seven weeks: early on Frank is alone and fights are risky; his crew, name and weapons tip the odds later, while rivals send more men; nothing scales enemies to him.
- Standard: assists change only their own thing.
- Test: S: screen inventory with each assist; B: auto-resolve uses the simulator's rules.
- Source: his design (accessible); blueprint 1.4.6, 6.x.
- Status: designed.

## CS-26 Sound and animation

- How it works: Sound: blows differ by surface and body part; breath and grunts carry state; footsteps by surface; a shot by place (street, warehouse, over water). Animation: lab-tested before building (his ruling); motion matching for footwork, motion warping to line bodies up, physics hit reactions blended over authored ones (a cap on how far a body flops, so a fall reads as a man, not a doll), paired moves per surface fitted by height; faces show pain, fear and anger; clothes pull when grabbed. No clip shows drink, gambling, children, torture or cruelty as spectacle (the animation library's gate).
- Standard: the animation source passes the lab test (one wind-up, strike, hit reaction, shove into a wall) before any build.
- Test: the lab test; the content gate on clip names.
- Source: his design 12 Oct (the animation question); RULINGS 30 Oct.
- Status: pending (lab first).

## CS-27 The inquiry into a death that is not a constable's

- How it works: A body found, a man dead in hospital after a fight, or a man missing long enough to be reported starts an inquiry by the local CID (DS Ellis's office): the scene, the body, statements from whoever the record says saw or heard anything, the dead man's ties (who had a grudge, who owed). It needs what any charge needs (CS-19): a witness who tells, evidence that names (CS-16), or a confession; without them it stays open and the talk goes on. A bought Ellis slows it, steers it to another suspect if one fits, and stops short of covering a killing the town saw. A killing by someone else is investigated the same way, and Frank may be leaned on if the town's talk points at him. A constable killed by anyone is the long heat (LONG-HEAT.md), whoever did it; the squad learns of a bought constable's payments only if someone tells or a paper is found. What happens to the story when a principal dies is the story pass's (the spine re-routes; named as a gap for that pass, not this one).
- Standard: no charge without a witness, evidence or confession; always recoverable.
- Test: S: golden rows for a body found with no witness, with one witness, and with a print on file.
- Source: his ruling of 24 Nov (long heat; Ellis bribable); the 1990 police research; CS-16, CS-19.
- Status: designed.

## CS-28 Edges a player will try

- How it works: Saves keep everything: a chase, a manhunt or the long heat carries across a save and a load; reloading is never stopped, and the game says when something is permanent (a death) before it happens (D27, D30). No fighting on anything moving: buses, the ferry and boats are scenery, and Frank cannot climb on a moving car; a fight in a parked car or at its doors uses the car's surfaces (CS-07). No animal is ever harmed (dogs, pigeons in the loft, gulls); a guard dog barks and can be quieted with food (blueprint 1.4.8). The car against people is canon's: Frank's car can knock a person down and hurt them badly, never kill; a man knocked into the water by a car climbs out (a car never kills, so the drowning rule does not apply to it); a claim of accident is a cover story (CS-10) against what witnesses saw. Hiding in a car boot is a hiding place like a doorway: unseen, but a search of the car finds him. Fleeing into buildings and yards and the search that follows are the chase parts' (blueprint 1.5).
- Standard: no dead end, no harmed animal, no killing car.
- Test: S: each edge as a golden row.
- Source: canon (cars, the content rule); RULINGS 24 Nov; blueprint 1.4.8, 1.5.
- Status: designed.

## CS-29 Smaller rules the census and the questions asked for

- How it works, one line each:
  - Blows: the cross and the hook are the heavy blow's animations by angle; there is no third button. The man the next blow goes to shows it only in Frank's shoulders and head turning to him, no marker.
  - Cover: Frank takes cover as a man does, by moving behind something solid; no snap-to-cover key; a wall stops a shot (CS-23).
  - Where weapons come from: carried weapons are bought (the ironmonger sells a utility knife and a cosh-length of pipe; a flick knife comes through people), taken from a man, found (a yard, a skip, the office); guns as RT2-14.
  - Standoffs with several: the standoff rule (CS-10) holds for any number; each man watched weighs the threat on himself, and a man not watched may act.
  - Talk with the police: a cover story or an apology to a constable is a claim (CS-10); running from an arrest is a new offence and a chase (blueprint 1.5); talking out of an arrest works only on what he did not see.
  - Taunts and barks: written ahead in period speech and the local accent, checked once (RULINGS 24 Sep); slurs never.
  - Sight is symmetric too: what a watcher could see, the camera shows (blueprint 1.4.1, 1.4.2); no watcher sees through what blocks the player's view of him.
  - A witness's belief is only as sure as what he caught (RULINGS 30 Sep); a doubtful belief fades in strength as it is retold, the memory itself never wiped.
  - Dirt and smell: dirt on a man is a give-away to anyone near (blueprint 1.4.4), not camouflage; smell plays no part, except a body after days (CS-16).
  - Disguise: any coat, cap or uniform Frank has (bought, borrowed, taken) is a give-away changed (1.4.4); none is a key to a place.
  - Wrong places: a yard, a back room or a closed shop after hours is a wrong place; a man found there is suspicious to anyone who sees him (the 1.6 jobs parts set which places).
  - Overheard talk is the talk parts' (people speak within earshot, and Frank hears what anyone standing there would).
  - Pickpocketing is not a verb (theft in LEDGER is break-ins, robbery and taking from a man down).
  - A stranger appearing mid-fight to rob the loser, a taxi to skip a fight, bailing from a moving car, stacking bodies against doors, police quirks: out (no random spawns, the cab is Frank's own, no fighting on moving things, bodies are objects that can be dragged, not furniture).
  - Cameras: the bank's camera is the only one (his ruling of 24 Nov; canon leaves a second site his to name), tape recycled weekly; a deed in its view is caught as a coat, a shape and the hour, and the tape can be taken by police within the week; footage cannot be erased by Frank without a break-in.
  - Gossip cools by severity: talk of a grave deed travels for weeks, of a scuffle a day or two; the memory stays (canon).
  - Raids on a rival's premises are jobs (the jobs parts), fought by these rules.
  - Breaking a truce (Garbutt's) is a deed the broker and both outfits read as grave; the outfit wronged takes it up as revenge (CS-20) at outfit level, and the broker's regard falls.
  - Hidden bodies: in the dock, a body comes up in days to weeks unless weighted, and then perhaps never; buried at the allotments or a yard, or left in a lock-up, it is found only by a search, a dog or smell after days. This replaces 2.5.5's "never found".
  - Running from fights: a man seen running from every fight loses menace with those who see or hear of it; a man who stands earns it, win or lose.
  - Followed or blocked: anyone, a constable included, notices a man following him by the tailing rules (blueprint 1.1.6) and challenges or calls for help by temper; standing in a constable's way is obstruction (s.51).
  - Medics: the ambulance comes in about 10 to 15 minutes to a call; attacking medics is read grave (times 1.6, as a yielded man), and a hurt man left unreached follows the dying rule.
  - Ragdoll: physics bodies are capped in number and settle to an authored pose within seconds (performance, CS-26).
  - Perception cost: the senses run on the Core's budget (BLUEPRINT-08); this pass adds no new per-frame sense.
- Standard: each line a golden row or a part of another test.
- Test: S: golden rows.
- Source: census rows; RESULTS-2.md.
- Status: designed.

## CS-30 Rules the second blind check asked for

- How it works, one line each:
  - Input: a press up to 0.1 s early counts; one action is held, never a queue. Turning during a heavy is slow; stepping in, out and circling are movement in guard at walking pace, a little wind each.
  - The opening: Frank starts with nothing; things to hand from the first night; a carried weapon in the first days (bought or taken); guns late (RT2-14).
  - Dirty fighting: a groin kick is a low kick by the same force rule; grit thrown in the eyes blinds 2 s; the street reads both as dirty (times 1.2).
  - A thrown thing is aimed like a blow, at the man pointed at, no reticle.
  - Property: broken glass, stalls and the kiosk are deeds against their owner, who remembers and asks for money or tells, by temper.
  - Armed men: a weapon under a coat shows as a bulge or a hand that stays near a pocket; no icon.
  - Backing down: always there; the town remembers who backed down (menace with those who saw). Frank's men take their tone from his last order.
  - Threats against a man's family: a threat with his ties added (weight up 0.1), read worse by the street (times 1.3).
  - A held or questioned man lies, stalls or bargains by his temper; what he says is limited to what he knows (the claim check).
  - Speech mid-fight is written lines chosen by the rules, never a live reply; live talk opens with a man pinned, yielded, or after.
  - Alarms: a shop bell rings at its reach; wired alarms are rare in the Hook (the bank, the chandler's) and bring a constable in minutes.
  - Orders: a held key and a word (take him, stop, get him out), no wheel on screen.
  - Hospital: casualty asks how; a stab or gunshot wound is passed to the police by habit.
  - Blood on the ground stays until rain or a hose, a day at most in the wet; seen and read by passers-by.
  - Grief: a dead man's ties grieve; a funeral at the church within the week; the family's grudge; the street quieter.
  - An alibi is a claim by another person, weighed by his temper and what others saw; the fare book is evidence both ways.
  - Place weighs the deed: a fight in the church, the hospital or a tea room is read worse (times 1.3) than on the docks at night.
  - Stalking and repeat beating: waiting at a man's home is a deed his household sees; a man beaten again and again goes to the police, to friends or leaves town, by temper; nobody can be farmed.
- Standard: each line a golden row.
- Test: S: golden rows.
- Source: the second blind check (census rows M411 to M463).
- Status: designed.

---

## Out on purpose

- Combos and their kin (feints, five-zone roses, zone switching), skill trees, lock-on, health bars, armour, healing items, explosions, scopes, ammunition types, silenced guns, swimming, a jump key (his rulings).
- Meters and scores: noise rings, suspicion bars, stealth scores and ratings, slow motion on a disarm, a camera tool, wanted stars, bounties and bounty hunters, mission failure on being wanted (none fit his no-HUD, no-numbers rulings; jobs have no fail screen).
- Poisons and cash thrown as a lure (a decision within canon: no such items in a 1990 street game of hands; R20); burns or scalds as weapons (cruelty, canon).
- Bottles or glasses as weapons, and any drink item (canon).
- Harm to any animal; children anywhere (canon's content rule for children; the animal line is the blueprint's 1.4.8, extended here).
- Torture, cruelty as spectacle, tied people shown (canon; his holding-overnight ruling).
- Pulling drivers from cars, and driving to kill: a car hurts, never kills (canon); pulling drivers was recommended out in the hype test (Q1, his to settle).
- Hostage-taking as a shield: out for now. A man held by the collar with a knife shown is a threat at 0.8 (CS-10), not a shield the police respect; 1990 armed police in a town are rare and a shield move invites a scene canon does not want. Recorded as a decision within canon.
- Attacking during a scripted scene: there are few short cutscenes and none takes control mid-confrontation; story people are never protected by invulnerability, they follow the body rule, and the spine re-routes (the standing principle).

## Which blueprint parts this replaces (for the keeper)

- Replaced whole: 1.3.4 (into CS-01, CS-10), 1.3.6 (CS-06), 1.3.7 (CS-04, CS-05), 1.3.8 (CS-09, CS-11), 1.3.9 (CS-14, CS-15), 1.3.12 and FIT-P17 (CS-11's kinds, kept as data), RT-11 (CS-04, CS-05), RT2-11 (CS-14, CS-16; the 2 s hold and two asks kept), RT2-12 (CS-07; its numbers kept), FIT-P18 (CS-11).
- Changed: 1.3.1 to 1.3.3 (CS-02, CS-03: numbers kept, C14 struck, wind costs set); 1.3.5 (CS-07: glass, water, doors, car doors added); 1.1.1 and 1.1.5 (crouch settled by CS-12); 1.4.2, 1.4.3, 1.4.8 (CS-12: surfaces, alertness states, light changed); 1.3.10 and RT-10 (CS-23, pending D3).
- Kept and referenced (this pass does not restate them): 1.1.5 to 1.1.7 (hiding, tailing, stopping and blending in), 1.2.5 and 1.2.10 (cars and people; taking a parked car), 1.3.11 (inside CS-18), RT2-13 (inside CS-15), RT2-14 (where guns come from), 1.4.1, 1.4.4 to 1.4.7 (reading watchers, give-aways and disguise, the walk to tell, the seeing assist, street manners), 1.4.8 (drawing a watcher away, dogs), 1.5 (chases on foot and by car, the search after), 1.6 (jobs with the hands: getting in, lockpicking, searching, getting rid of things), the police parts and police.json in BLUEPRINT-02 (the 1990 force, patrols, custody, informants), the gossip and witness parts in BLUEPRINT-02 (chain reactions, certainty against willingness, the signed statement), LONG-HEAT.md.
- Replaced in LONG-HEAT.md: LH-14a (a knife kills only by finishing) and LH-14c (no standing kick; the boot never kills) by CS-05 and CS-02; LH-12's 10 to 30 s for a struck constable stays for fists (CS-05's fist band 10 to 60 s contains it), a weapon blow uses CS-05's longer band; LH-14e's clip list to follow CS-06's weapons and CS-13's knife from behind.
- New: CS-08, CS-13, CS-16, CS-17, CS-19, CS-20, CS-21, CS-22, CS-24, CS-25.
- Stale text to mark replaced, not edit: the weapons spec's bottle, "bad drink", wire and cord, and "arrest, no chase"; FEEL-TARGETS-MELEE C14 and drill M2.
