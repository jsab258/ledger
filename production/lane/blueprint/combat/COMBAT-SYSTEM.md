# COMBAT-SYSTEM: one general system for fights, menace and stealth

25 Nov 2026, the combat and stealth pass (his Go, 07:47); revision 1 the same day (his answers 10:52 to 11:31: chance pick A, D1 to D3 yes; REVISION-1.md lists every change). Status of the whole: ready for review. It replaces the combat and stealth parts of the blueprint listed at the end (for the keeper). Canon and RULINGS on wip outrank it; his "LEDGER Combat: Final State" (12 Oct) is its starting point, and where this text differs from a ruling it says so and the point is in RULINGS-TO-REVISIT.md, never changed silently.

Numbers here are the simulator's (SIM/combat_sim.py, revision 1, seed 1990, 2,000 runs a scenario), so text and code agree. Every number is a tuning value the loops retune; the rules are the design.

## The chance rule (his pick A, 25 Nov, advisor 382)

Readable rules decide outcomes. A player who did it right gets the result he worked for; failure comes only from things he could notice. In plain terms:
- No hidden roll overrules a correct play. A blow lands, is blocked or is slipped by what the struck man is doing at that moment (guard up and facing the blow, mid-swing and open, looking away); a takedown on a man reached unseen works; a disarm follows the grip and the moment. Whether a man gets his guard up follows his reaction time (fixed per man by his skill, slower when hurt, none when emptied) against the blow's wind-up: a quick boxer covers a heavy he sees coming, nobody covers a jab already on its way, and a man mid-swing cannot cover at all. What a man chooses (press, hold, run) is his temper, and it shows before it happens.
- Blows land on the attacker's line (high is the head, low the body, a guarded blow on the arms, a low kick on the legs), not by a dice table of zones.
- Knock-downs and knock-outs follow force and the man's visible state (wobbling from head blows, gasping) by thresholds.
- Injury: the low end is safe and certain (a punch or two, a shove: a bruise, a cut lip, a man on his backside); danger grows with what Frank chooses (kicking on, a weapon to the head, a knife, the kerb, a gun) and the body shows it (stops moving, blood, the breathing changes); a small real chance only at that violent end: how deep a knife goes, how a spent man falls at a kerb, how a critical wound turns out, where a shotgun's pellets go, a choke held on, boots on a head.
- Every such chance is fixed to the save: drawn from the save and the act itself, so a reload replays the same outcome for the same act (the simulator's reload check: the same 200 stabs replayed from one save under two different random streams give the same wounds and outcomes; a different save gives different ones). A different act (a blow to the body instead of the head, stopping at the cue) is a different draw.
- The people's own variety (one man's nerve, another's reach for a brick) is their temper, seeded the same way; the player reads it in faces and stances, never a hidden number on a correct play.

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
  - Aim: high, low, or at the weapon arm, by the stick or mouse held up, down or towards his weapon side as the blow starts (head, body, the arm that holds the weapon); legs by a low kick or a low thrust (the stick held down with a blade). A guarded blow lands on the forearms. Nothing is hit by chance. No five-zone rose, no zone switching, no feints (combos and their kin are out by his ruling).
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
  - Zones: head (face), neck, torso, arms, legs. Every blow lands on its line: the attacker's high or low (head or body), a slash high, a thrust to the body, a low kick to the legs, a guarded blow on the forearms, a man struck from behind where the blow was aimed. No zone dice table. What each zone does is CS-31.
  - Force: the action's force (jab 1.0, heavy 2.6, kick 1.7, boot on a downed man 1.3, shove into a surface 2.0 whatever is in his hand, since the wall is the weapon) times the weapon (fists 1.0, knuckleduster 1.35, chair 1.7, cosh 1.9, brick 2.0, bat 2.3) times wind, half again on a man who did not see it coming, half again for a counter.
  - Blunt harm adds up by zone (the head counts a quarter more): bruise, hurt from 3, serious from 9.5 (a broken nose, cheek, ribs: hospital), critical from 15 on the head or 22.5 on the body.
  - Edges and points (a knife, a broken chair leg) do not add up; each landed cut or stab has a depth, the knife's one chance, fixed to the save. A thrust to the body: minor 40%, serious 44%, critical 16%; to the face 30%, 45%, 25%; to the neck 10%, 40%, 50%; to an arm 70%, 27%, 3%; to a leg 62%, 32%, 6% (the femoral artery). A slash is mostly minor (a body slash 72%, 25%, 3%; a slash to the neck 35%, 40%, 25%). A slash on a guarding forearm always cuts it. A serious stab to the body or neck drops him (he goes down holding it). So a knife is usable from the first second of a fight, what a stab does depends on where it lands (his ruling, advisor 374), and a knife is the violent end of the scale.
  - Critical means dying: a man with a critical injury dies unless helped in time. Left alone, he dies about 55 times in 100; helped (a passer-by, Frank, the ambulance) about 20. Head harm, a bleed or a drowning all run through this.
  - Knocked down and knocked out: a blow knocks a man down when its force passes how steady he is (a head blow from force 3.4, a body blow from 5; head harm already taken and an empty wind make him less steady, and both show: he wobbles, his hands drop). A head knock-down puts him out once his head harm reaches 8, or at once from a weapon on a man who did not see it coming: 10 to 60 s from fists, 30 s to 5 minutes from a weapon (boxing counts under a minute as an ordinary knock-out; over a minute is a hospital case). Out is never shown as dead: an unconscious man breathes, groans, twitches; a dead man does not, and the player can always tell them apart.
  - His fists line (30 Oct): fists alone, and a shove into a surface, never take a man past serious (whether a shove can kill is still open in his design, so this pass keeps it at serious). The fall can (CS-07). A knuckleduster is a carried weapon, not fists: its force is a third more and it is not capped, though it seldom reaches critical. Boots on a downed man are not fists: they can reach critical (his decision D2, yes, 25 Nov). It is readable as it gets worse: at serious head harm he stops covering his head and goes still, Frank's breath changes, the second ask names it; a player who stops there kills nobody (the simulator: 0 deaths in 2,000 kerbside fights finished with boots by a player who stops at the cue; 31 in 1,000 by one who kicks on all three times). One blow on a downed man raises his harm one level at most, so each step shows before the next.
  - Burns, scalds and sprays are not in the body rule: hot fat, boiling water or anything thrown in a face to burn is out (cruelty as spectacle, canon). Fire (CS-22) harms by smoke and flame as an event, not as a hand weapon.
- Standard: deaths from fist fights alone at most 1 in 1,000; a knife fight kills in roughly 1 in 10 (revision 1 gives about 1 in 17, inside the research band below, since blades now land on their line) (England and Wales hospital data 2000 to 2005: 7.2% of stabbed patients died in hospital; a recent UK major trauma centre: 0.9%; an Icelandic national series: 17% died before reaching hospital); a beating to submission leaves most men hurt, about a fifth seriously.
- Test: B: the simulator, revision 1; seed 1990, 2,000 fights a scenario: one-on-one fist fights 0 deaths in 2,000 on the open street and at the kerb (the fall still happens: one critical, survived, in 2,000 open-street fights); a knife used by Frank 57.5 deaths per 1,000 fights (was 94: blades now land on their line, most thrusts to the body, and a guarded thrust goes into the forearm); of all opponents in one-on-one fist fights 65% end hurt, 24% serious. Rare-event rates rest on one to a few events and are leads, not measurements. The reload check passes: 200 stabs replayed from the same save under two different random streams give the same wounds and outcomes; a different save gives different ones.
- Source: RESEARCH.md (stab lethality, knock-out bands, cold water); rev1-work/RESEARCH-WOUNDS.md (gunshot series, partial); his rulings 30 Oct, 24 and 25 Nov (advisors 374, 382); KCD2's knock-out flags (census).
- Status: designed; the edge table is judgement within the research bands (no region-by-region source reached).

## CS-06 Weapons as data

- How it works: A weapon is a row of data, never a special case: kind (blunt, edge, firearm), force, wind-up, reach, wind cost, how many blows before it breaks, whether it hides under the coat, the menace it carries when shown, its noise, what evidence it leaves (prints on smooth handles, blood, a dent, fibres). Carried: knuckleduster, cosh, bat, utility knife, flick knife (his 12 Oct tiers; every make fictional). Things to hand break: chair after 2 blows, brick 3, dustbin lid 4, wheel brace never; anything graspable within 1.5 m that the props list marks can be picked up and swung or thrown (a brick, a chair, a crate lid, a length of pipe, a cargo hook, a snooker cue, an ashtray, a stall pole). Never a bottle, a glass or anything to do with drink (canon); no dog is ever harmed. A man losing looks round for something to hand (CS-09). Guns are CS-23.
- Standard: every weapon a data row; each has its answer (a grab on the weapon arm, a chair, numbers, running). A knife against one unarmed man nearly always wins, as in life (the simulator: 99% of decided fights); its price is the body count and what follows, and against two men it wins about 3 in 4. Carrying: two things under the coat at most (more shows); the cab's boot and the office are stashes, searchable by the police with cause. A thrown thing hits by its force at half the wind-up, aimed like a blow, and is left where it falls; a carried knife can be thrown but is then gone.
- Test: B: the simulator's weapon table; S: the props list carries the graspable flag; content check: no drink item flagged.
- Source: his design 12 Oct (four tiers, things at hand); blueprint 1.3.6; weapons spec (the bottle struck by canon); census rows on weapon pickup and breakage (Sleeping Dogs, Yakuza, GTA).
- Status: designed.

## CS-07 The street as a weapon

- How it works: Surfaces are force, not finishers. A shove or throw into a hard surface (wall, shop shutter, railings, car bonnet or door, kerb, step, phone box, quay bollard) hits at force 2.0 on the body or head and the man is out of the fight about 4 s; glass (a shop window, a car window, the phone box panes) adds a cut by the edge rule. The fall: a man knocked down near a kerb, step or wall foot who was already spent (three heavy blows or one weapon blow taken, as RT2-12; he shows it, slow and swaying) has his head strike it: serious about 1 in 10, critical 1 in 50, a chance fixed to the save; a man not yet spent falls safely; since a critical man dies only about half the time, deaths run below RT2-12's 1 in 50 to 1 in 20 (listed in RULINGS-TO-REVISIT R17). The fall applies to everyone's fights, not only Frank's (R18). So a fight by the kerb carries a small, real risk, and the cost comes after. The quay edge: a man thrown or falling in climbs out at the nearest ladder within a minute if conscious; if unconscious with his face in the water he is dying (critical) and dead in about two minutes unless pulled out (Tipton: cardio-respiratory arrest about 130 s after submersion). This settles the open question in his design (does the quay edge count): it counts through drowning, not through the fall; listed in RULINGS-TO-REVISIT R5 so he can overturn it. Frank never swims (his ruling) and can pull a man out from the steps or a ladder. Car doors can be slammed on a man (force 2.0 to an arm or the head). Doors: slam, hold shut, kick open (a locked door takes several kicks and is heard). Wet cobbles: a heavy blow or a run on wet stone slips 1 time in 20 (a stumble). Light can be changed: a bulb broken, a switch flicked, which changes CS-12 at once.
- Standard: seven places first, fitted by height (blueprint 1.3.5); every surface move fully animated with no cut-away, gore light (his ruling 24 Nov, canon).
- Test: B: kerbside scenario in the simulator (1 death in 2,000 fist fights at seed 1990, too few to measure the rate); S: each place triggers its paired move.
- Source: blueprint 1.3.5, RT2-12; his 30 Oct fall ruling; Study 17 (Yakuza's places, not its finishers); RESEARCH.md (cold water).
- Status: designed.

## CS-08 Grabs, holds, chokes and the ground

- How it works: A grab works unless the man slips it (his defence). From a grab: shove, shove into a surface, throw down (he goes down), pin to a wall (holds about 2 s each press and opens talk: a pinned man can be spoken to live, CS-10), take the weapon arm (disarm, by readable things, never a coin: the weapon comes free if his grip is loose (his wind under 0.4, hurt past 40% of what he can take, his weapon arm hurt) or he is caught in the 0.3 s after a swing; otherwise he holds on, it is a struggle for the arm that costs both men wind, and Frank can shove or let go; a gun is taken by the same rule once the man is grabbed close; the weapon drops to the ground, where anyone may take it; in the simulator a disarmed weapon leaves the fight, the pick-up is a build test). A man may grab Frank from behind while another hits him; Frank breaks free by pressing grab with his wind (a fresh Frank in about 1 s, an emptied one in 3). A grab works unless he is guarding and facing Frank (then he slips it). A choke in a fight works only from behind on a man busy with someone else (one of Frank's men, say) and takes half as long again as on an unaware man; from the front it is a grab. On the ground: a downed man can be kicked or struck (CS-14), helped up, or left; he gets up in 2 to 5 s unless beaten or out; a man on the ground can grab an ankle. No wrestling minigame: ground fighting is the downed state and the blows on it.
- Standard: every hold has a way out; a disarmed weapon is a real object on the ground.
- Test: B: the simulator counts disarms both ways; S: a dropped knife can be picked up by the other man.
- Source: KCD2 clinch, Sleeping Dogs grapples (census M021 to M030); his design (shove, grab, pin).
- Status: designed.

## CS-09 The temper in a fight

- How it works: Every half second each man not acting chooses: press, hold (hands up, circle), back off, look for something to hand, call for help, yield, beg, or run. The choice comes from his will to fight: his nerve, plus his friends still standing, minus the fear of what he faces (the menace of the weapon shown: knuckleduster 0.35, cosh 0.45, bat 0.55, knife 0.75, gun 1.0), minus how hurt he is, minus being outnumbered, minus Frank's menace (what the town has seen him do); grudge adds. Low will: he runs if he can, else yields; beaten and still facing it, he begs. Watched by his own people, a man stands longer; some call a bluff whatever their nerve. A man with high law shouts for the police; a man with a tie to the victim steps in (the temper model's rule). A provoked man starts trouble only with cause: a bump, a stare held, a grudge, a job; never at random (not Yakuza's street encounters). A man who walks away from a fight and comes back finds it where the tempers left it: men remember, and a fight half-won is resumed or settled by talk. Frank's crew decide by the same rule plus regard and loyalty: a frightened one runs; an angry one may go too far (a crewman with high grudge may keep hitting a downed man unless told to stop).
- Standard: every person in a confrontation can fight, freeze, back off, yield, beg, run or call for help, and the choice reads from the temper the player can see (stance, distance, voice).
- Test: B: the simulator, revision 1: in one-on-one fist fights against a careful Frank about 1 in 4 men yield and 1 in 8 run; against a knife half run; S: the temper model's golden rows.
- Source: the temper model (24 Nov, nerve, greed, mouth, law, grudge); Philpot et al. 2020; KCD2 and RDR2 surrender and flee (census).
- Status: designed.

## CS-10 Talk in a confrontation

- How it works: Menace is the main weapon (W2). Before or during a fight Frank can speak, a 1 to 2 s act he can be hit during: threaten (a word, or with a weapon shown), demand (leave, pay, tell me, hand it over), offer (money, a truce, a way out), bluff (claim men or a gun he has not got), name himself ("Mickey's nephew", later his own name), call his men, yield. The rules decide, the AI only voices: a threat folds a man if his nerve, plus pride (about 0.15 for each of his own watching, and a little of his own), is under the threat (a word 0.5, a weapon shown 0.8) times 0.8 plus 0.4 of Frank's menace. A bluff counts as a word, and a man who later learns it was a bluff lowers Frank's menace with him. An offer moves him by greed; a name moves him by what he has heard of Frank. Others speak too: beg, offer, threaten back, call Frank's bluff, shout for help. A pinned or yielded man can be talked to live (the claim check and the hard rule apply; the line he says is from what the Core decided). A threat stops a report to the police, never the street's talk (his ruling of 3 Oct). The threat's weight is general: 0.5 for a word plus 0.4 times the menace of what is shown (a cosh 0.68, a knife 0.8, a gun 0.9). A standoff is two sides each with a weapon shown: every beat each side's temper chooses hold, talk, back off or strike, and the first to move commits the street to rung 7. A cover story ("I'm here for a fare") is a claim: believed when the slots fit (right clothes, a reason for the place and hour, the cab outside) and the listener does not already know better; a bad fit makes him uneasy (CS-12). Owning up to a lesser deed is a claim too, weighed the same way. Frank can offer the police money only if the officer is bent (CS-19). Spoken threats to the live talk count as deeds (the live-play checker reads deed lines for threats, RULINGS 3 Oct).
- Standard: most confrontations end on rungs 1 to 4 (his design); a threat is not a sure win.
- Test: B: the simulator's threat table: at the start (Frank's menace 0.3) a bare word folds 12% of lone men, a cosh shown 29%, a knife shown 47%, a revolver 68%; two men together 0%, 2%, 6%, 12%. At menace 0.8 (a feared man): 19%, 53%, 82%, 96%; two men 1%, 6%, 25%, 53%. S (build test, not simulated): every man who folds to a shown weapon is a witness to rung 6.
- Source: his design 12 Oct and ruling 3 Oct; the temper model; census (RDR2 intimidation, GTA aiming at people, Hitman's lack of talk; LEDGER-only rows for talk mid-fight).
- Status: designed.

## CS-11 Several men, crews and tactics

- How it works: At most two swing at one man at once (a token), the rest circle, cut off the way out, grab from behind, or pick up something. Crowds are bodies: they block a run and a swing, and a wild blow can land on a bystander (then he is in it). A brawl spreads by ties: friends of either man join by their temper. Each outfit has its way: the dockside syndicate's men come in numbers and grab; Cammack's crew are quick to draw a knife and quick to run; Agar's men avoid fists and send for help or the police. When the man who leads them goes down, or half are beaten, the rest's will drops. Frank's men act on orders (stay back, take that one, hold him, stop, get him out) and otherwise by temper; a blow can land on a friend in a crowd (friendly blows are possible, about 1 in 30 swings in a close press). A beaten crewman is off the roster for his hospital days. Two against one is deadly and three is a beating; Ron at Frank's shoulder turns two against one into a fight he usually wins.
- Standard: the blueprint's FIT-P18: a skilled player wins a fair two against one about one time in four, a masher under one in ten.
- Test: B: the simulator: a careful Frank wins 2 v 1 29% (39% lost, 32% stopped by a bystander or the police), a masher 0%; 3 v 1 1% (79% lost); with Ron (2 v 2) 73%.
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
- How he turns (revision 1): only for a cause the player can notice: his routine glance over the shoulder (a rhythm the player can watch, every 6 to 20 s for 1 to 2 s), a footstep inside his hearing (he turns 0.8 s after it; the player hears his own step at the same strength), or other eyes (a watcher where he can see Frank). Nothing turns him "at the last moment" without a cause. A still figure in shadow during a glance is picked out only within about 1.5 m in a dark doorway, 2.3 m in an unlit street; under a lamp a still man is seen at about 9 m, 12 m with no shadow near (in the simulator crouch shrinks a shape at every distance in the dark, where every reach is about 4.5 m or under; the 4 m line above stays for the build).
- Test: B: the simulator, revision 1, approach from 12 m behind an unaware man, scenes drawn at random (his routine, rain, his build, shadow), three ways to play: walk straight in; crouch but ignore his glances; careful (crouch, slow on loud ground, freeze while he glances, and close in only when the gap before his next glance is long enough). Doorway dark, wet cobbles: careful 99.6% out (0.4% held back because the gap never came), crouch-and-go 24% out; unlit street, wet cobbles: careful 86% out, 14% held back; walking straight in 0% (63% heard, 37% seen); under a lamp: careful 19% out, 54% held back, 27% seen; by day careful 7% out; on a metal deck in the dark careful 25% out, 57% heard (the deck rings under him: the player hears it). Careful in the dark, any surface: 62% out, 30% heard (gravel and metal decks), 8% held back. Was (the first pass): dark doorway crouched 58% out with 23% broken free and 7% turned for no cause.
- Source: canon (perception ladder); blueprint 1.1.5, 1.4.1 to 1.4.3, 1.4.8; census (KCD2 noise and visibility, Hitman suspicion, RDR2 witnesses); RESEARCH.md (no published detection timings found: these are judgement).
- Status: designed; the numbers are judgement until the KCD2 and RDR2 seeing study (1.4.1's deciding row) is done.

## CS-13 Takedowns from behind

- How it works: An unaware man reached within 1 m from behind can be taken by any action; nothing is instant or certain.
  - Choke (grab from behind, held): a carotid hold puts him out in about 7.5 s (a small man 6.5, a big one 10; forensic sources say 5 to 10). He cannot break it, except a big, fresh man against a Frank who is winded or hurt (both readable before Frank tries: the man's size, Frank's own breathing); the struggle is heard about 6 m and other eyes may see it. Released at once when he goes limp, he is out 10 to 60 s and wakes with a sore throat and a grudge. Held on past that, deliberately (Frank keeps holding; the body shows it plainly: the man goes limp, then still, the face colour changes, the struggle sound stops), he is in danger: no risk for the first 40 s more (about 50 s of hold in all), then the chance of death rises by 1 in 100 a second: 20% at a minute past, 50% at 90 s, 80% at two minutes, near certain at 135 s, fixed to the save. Judgement: the only timing series found (breathing stopped at 62 to 157 s) is from a teaching sheet citing filmed hangings, not chokes (from memory, unchecked); the curve starts after its earliest time. His decision D1: yes (25 Nov).
  - Cosh to the head from behind: he is out, every time (a weapon on a man who did not see it coming), with a hurt head; no death from one blow. Each further blow on the man out raises his harm one level at most: a second to serious, a third to critical (the violent end, readable at each step: blood, then he stops moving).
  - Fist from behind: a heavy punch to the back of the head floors him, every time, but does not put him out; he is up in a few seconds, startled and angry. To put a man out quietly takes a choke or a cosh.
  - Knife from behind: a thrust to the body, by the edge rule (the depth fixed to the save); once reached it drops him seriously hurt about 4 in 10, kills about 1 in 12, otherwise wounds.
  - Failure, only from what the player could notice: the man heard a step inside his hearing (more on loud ground, walking not crouched, not slowed), glanced round on his routine while Frank was in sight, or someone else saw. Then he turns: a fight with Frank close and the man startled. An officer struck unseen does not know it was Frank (his ruling of 24 Nov). A constable or anyone knocked out remembers being struck, and his own last sight before.
- Standard: no instant kill, no guaranteed knock-out; failure believable and readable.
- Test: B: the simulator, revision 1, from approach to result (unlit street, wet cobbles): played carefully, choke out 87% and held back 13%; cosh out 87%; fist knocked down 86%; knife dropped 40%, wounded 36%, dead 7%; crouching in without watching him, choke out 21% (46% heard, 33% seen). A choke held 60 s past the knock-out, drawn from the save: 20% dead; 90 s: 49%. A big man choked by a fresh Frank: out; by a winded Frank: breaks free. The held choke by the curve above. Was (first pass): choke out 40%, broke free 17%, spotted 38%, with chance at every step.
- Source: RESEARCH.md (carotid hold timings; knock-out bands); his rulings 24 Nov; census (Hitman subdue, RDR2 and KCD2 stealth takedowns, GTA VI unconfirmed).
- Status: designed; D1 yes.

## CS-14 How a confrontation ends, and the quiet after

- How it works: Ends: someone backs off, runs, yields or begs, goes down, is knocked out, a bystander steps in (the more people watching the likelier: odds rise about a tenth for each, Philpot et al.), the police arrive (a beat constable first, then more), or Frank's men or the other man's friends pull him away. A man who steps in is answered by each fighter's temper: most stop; a high-grudge man shoves him off and he is in it. Frank's own yield (hands up) is answered by the other side's temper and purpose: a man defending himself leaves; a robber robs (RT2-13); a rival's men may take him to their boss; a man with a grudge may land a few more, the street reading that as worse. Provocation counts: if the other man struck first, or she swung first, the reading of Frank's answer is lower (times 0.7) as long as he stopped when it stopped. After it, with the other man down or yielded, Frank may: leave; help him up; rob him (paper money, a weapon, goods; the town calls it robbery); take him (hold someone overnight, his ruling: one night, nothing tied shown, a story the man tells after); speak to him live; or finish it. Finishing is never a move in the flow of the fight: with nobody else standing, Frank stands over him and holds strike or kick for 2 s, asked twice (blueprint RT2-11). The blow on a downed man, and beating a man who pleads, are fully animated with no cut-away (his ruling 24 Nov), gore light (canon). What the blows do is the body rule: fists stay at serious; boots can reach critical (D2); a weapon can kill. Watchers read it as worse (CS-17). A man yielded and spared remembers it (regard up a little, grudge down).
- Standard: a way out at every moment (ER-FIGHT-03); every ending leads on.
- Test: B: the simulator: in public one-on-one fist fights about 19% are ended by a bystander and 3.5% by the police; Frank finishing a downed man with three blows: with boots 31 deaths per 1,000 fights if he kicks on regardless, 0 if he stops when the man goes still; with a cosh to the head 56.5 per 1,000 regardless, 1 if he stops at the cue (was 15.5 and 42 by chance alone, revision 1 makes it follow the head harm the body shows). A cue before a blow that could kill: the downed man stops moving his arms to cover his head, and Frank's breath changes; the second ask names it ("He's not moving. Again?").
- Source: his design (how fights end, the quiet decision); blueprint 1.3.9, RT2-11, RT2-13; his rulings 24 Nov (holding overnight).
- Status: designed.

## CS-15 Frank losing

- How it works: Frank cannot die (12 Oct). When the body rule would make him dying, he is out instead. Beaten or out, he comes round on the pavement, in a neighbour's kitchen or in hospital (hospital costs days and the bill his 12 Oct design names, and plants a witness; the blueprint's "never money" is listed in RULINGS-TO-REVISIT R6, his design standing meanwhile). Where he wakes follows from where he fell and who found him: a quiet yard, the pavement; a neighbour with regard, her kitchen; anyone with law, or a serious injury, the hospital, in control within 60 real seconds with the cost said. What it costs comes from who beat him and why: robbed by men who rob (RT2-13, kept), taken to their boss for a talk and a demand (a rival's men), cautioned and cuffed (a constable), left (a man defending himself). He carries marks for days (CS-18), people see them and say so, and the town knows he lost (his standing, not a number). Always a way back: the men who did it have names and routines; he can front them, send men, pay, talk, or let it go. A run of losses costs more than money: a crewman who sees Frank lose again may leave (regard), a street he cannot hold goes to a rival; each has a way back by the same rules. Nothing ends or ruins the playthrough (the standing principle).
- Standard: ER-FIGHT-04 (in control within 60 real s); no dead end.
- Test: B: the simulator ends a lost fight with Frank beaten or out and never dead (5% of careful one-on-ones, 39% of 2 v 1); the come-round itself is a test for the build (S: every lost-fight route reaches a come-round within 60 real s), not run in this simulator.
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
- Test: S: injury records last their days; the simulator totals hospital days (seed 1990, revision 1: about 107,000 man-days over 50,000 fights).
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

- How it works: Guns are rare and late (his ruling, end state A). A gun is a weapon row with the highest menace; a shot is heard about 177 m by day and kept by whoever hears it. Being shot at: men without guns run or take cover behind anything solid (a van, a wall, a stall), which blocks a shot; men with guns shoot from where they stand and run when outmatched (blueprint RT-10). Hold-ups: a threat at menace 1.0 through CS-10. A hit follows the body rule (his decision D3, yes, 25 Nov: a gunshot can kill at any stage of the dial), with what each zone does in CS-31 and worse than a knife: a revolver body hit puts a man down and is serious or critical about half and half; a sawn-off under 5 m is one mass of shot (a body hit critical 9 in 10), from 5 to 15 m the pellets spread over the body and arms (a body hit serious 6 in 10, critical a third), beyond 15 m scattered pellets (mostly minor, a face or eye the danger), and the spread can hit a man standing beside or behind the one aimed at. A gunshot critical wound kills about 3 in 4 left alone and a third helped (a knife's: about half and a fifth). An aimed shot to the arm makes him drop what that hand holds, one to the leg stops a runner (Y1.5); where the shot goes is where the barrel points, which sways with range, Frank moving and his wind, the sway shown in Frank's arms and the gun (no reticle, his rulings), never a hidden roll; a shot that misses its small target may go into the body. The dial (Fists, Shown, Fired, War) moves only on a gun seen or heard: shown moves the town to Shown, fired to Fired, a gun killing to War, and War brings armed officers from outside and searches on cause. Carrying a gun is a charge in itself (Firearms Act, years), threatening with one a worse one. A wall stops a shot; a shut door or a building's walls muffle the sound to about a quarter of its reach. A search of the office that finds a gun is a charge and a mark on the firm's name. This replaces blueprint RT-10's "before War a hit wounds and never kills" (D3 yes). Carrying a gun in 1990: a revolver is a section 1 firearm needing a certificate (handguns were banned only in 1997; from a summary source, to confirm from the PC); shortening a shotgun below 24 inches is an offence in itself (Firearms Act 1968 s.4); a loaded gun in a public place is s.19; using one to resist arrest (s.17) or with intent to endanger life (s.16) carries life (rev1-work/RESEARCH-LAW.md; the 1990 maximum terms for ss.1, 4 and 19 on indictment are unverified).
- Standard: AAA when used, feel numbers to be measured (blueprint RT-10).
- Test: B: the simulator's gun table (revision 1, aimed and steady): revolver at 3 m aimed at the arm hits it 63% (54% drop the weapon), strays into the body 37%, kills 10%; at 8 m aimed at the legs hits them 47% (42% cannot run), the body 44%, misses 9%, kills 15%; at 8 m aimed at the body hits 79%, kills 21%; sawn-off at the body: 3 m kills 50%, 10 m 18%, 20 m 1% (mostly minor pellet wounds). The feel numbers wait for the footage measuring.
- Source: blueprint 1.3.10, RT-10, RT2-14; his rulings.
- Status: designed for zones and lethality (D3 yes); feel pending (late by his ruling).

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
  - Where weapons come from: CS-32.
  - Standoffs with several: the standoff rule (CS-10) holds for any number; each man watched weighs the threat on himself, and a man not watched may act.
  - Talk with the police: a cover story or an apology to a constable is a claim (CS-10); running from an arrest is a new offence and a chase (blueprint 1.5); talking out of an arrest works only on what he did not see.
  - Taunts and barks: written ahead in period speech and the local accent, checked once (RULINGS 24 Sep); slurs never.
  - Sight is symmetric too: what a watcher could see, the camera shows (blueprint 1.4.1, 1.4.2); no watcher sees through what blocks the player's view of him.
  - A witness's belief is only as sure as what he caught (RULINGS 30 Sep); a doubtful belief fades in strength as it is retold, the memory itself never wiped.
  - Dirt and smell: dirt on a man is a give-away to anyone near (blueprint 1.4.4), not camouflage; smell plays no part, except a body after days (CS-16).
  - Disguise: any coat, cap or uniform Frank has (bought, borrowed, taken) is a give-away changed (1.4.4); none is a key to a place.
  - Wrong places: a yard, a back room or a closed shop after hours is a wrong place; a man found there is suspicious to anyone who sees him (the 1.6 jobs parts set which places).
  - Overheard talk is the talk parts' (people speak within earshot, and Frank hears what anyone standing there would).
  - Pickpocketing is not a verb (theft in LEDGER is break-ins, robbery (his ruling, advisor 378: anyone, anywhere, from the start) and taking from a man down, CS-33).
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

## CS-31 What each part of the body does (revision 1)

- How it works: Where a blow, stab or shot lands decides what it does, by readable effects, for everyone. Levels are CS-05's; the effects come with the level and show in the body. Arms and legs take blunt harm on their own count: 6 on one limb breaks it (a bat's full heavy blow landing on a forearm, two if it is turned on the guard; a boot to a knee); fists alone never get there.

| Zone | Blunt (fist, cosh, bat, brick) | Blade (knife) | Gun (revolver, sawn-off) |
|---|---|---|---|
| Arm | bruised, then broken: drops what that hand holds, no heavy blow or carrying with it until treated; plaster for weeks | a cut or a stab through the forearm: drops what that hand holds if serious; a slash on a guarding arm always cuts; an artery about 1 in 30 | drops what that hand holds, the arm out until treated; seldom kills (about 1 in 20 hits reach critical) |
| Leg | bruised, then a broken knee or shin: limps, cannot run, a chase ends; can crawl | limps if serious, cannot run; the femoral artery about 6 thrusts in 100: he can bleed to death | cannot run, can crawl; about 1 in 10 critical (an artery) |
| Torso and chest | winded, then broken ribs; a man can take the most here | a serious stab drops him (he goes down holding it); critical about 1 in 6 thrusts | puts him down; serious or critical about half and half (revolver), nearly always critical from a sawn-off under 5 m |
| Head and face | knock-down, knock-out (CS-05), then a broken nose, cheek or teeth: marks for weeks; critical only by weapon or the fall | a face slash leaves a scar; a thrust to the face is critical about 1 in 4 | dying more often than not; a graze to the face leaves a mark |
| Neck | struck as the head | the most dangerous: a thrust is critical about half the time, a slash a quarter | the most dangerous: critical about 9 in 10 |

  - Marks: a face wound (a slash, a broken nose, a shot graze, teeth out) leaves a mark or scar the man carries: anyone who saw the deed ties the mark to it, and the town names him by it ("the one with the scar"); a stranger who sees it knows only that he was hurt. The same goes for Frank: a scar on Frank is a give-away for good (blueprint 1.4.4), black eyes and stitches for their days (CS-18).
  - The arm out: a man who dropped his weapon with an arm hurt cannot pick it up with that hand; with the other hand his blows are weaker (six tenths) and he cannot grab properly. He feels it: his will to fight drops.
  - The leg out: he cannot run, so a man who would have run yields or crawls away; Frank can walk alongside and talk.
  - Shot spread: a sawn-off's pellets are one mass under 5 m; from 5 to 15 m they spread over a man's body and arms and can hit a man within about a metre of the line, beside or behind him; beyond 15 m they scatter, minor wounds unless in the face or eyes (the spread widths are judgement: no pattern source was reached from the cloud).
  - Restored from the old blueprint (Y1.5): an aimed shot to the arm disarms and one to the leg stops a runner, inside this table, and a shot that misses its small target can go into the body (the simulator: at 3 m an arm shot hits the arm about 2 in 3, at 8 m a leg shot hits the leg about half the time).
- Standard: the same zone gives the same kind of effect to everyone; every effect shows in the body; deaths only at the violent end (a knife, a gun, a weapon to the head, boots kept on, the kerb).
- Test: B: the simulator counts arms out, legs out, dropped weapons and face marks per fight, and has the knife and gun tables by zone (results.json: knife_by_zone, guns). Against a knife man, an unarmed careful Frank cannot break the knife arm with fists; he takes it by the grab (disarms 0.19 a fight) and wins 48%, and his own forearm is cut out of use in 28% and his face marked in 44%. With a bat aimed at the knife arm he breaks it in 24% of fights and wins 77%. When Frank holds the knife, the other man's face is marked in 35% of fights.
- Source: his question of 10:52 ("what happens if I stab or shoot someone in the arm vs face or chest?"); RESEARCH.md (stab lethality bands); rev1-work/RESEARCH-WOUNDS.md (Swedish and Stockholm gunshot series: head and chest wounds carry most deaths, limbs few; per-region percentages and shotgun range classes not reached from the cloud, to read from the PC); RT-10 and Y1.5.
- Status: designed; the gun and arm and leg figures are judgement inside the research's direction.

## CS-32 Where weapons come from, and the law of 1990 (revision 1)

- How it works: Every weapon in the Hook has a place it came from, a person who saw it change hands, and a law it meets. Every make fictional.
  - From homes: a kitchen knife from any kitchen (Frank's flat above the office, a house he breaks into, the tea room's back); a hammer or a poker. Free, and missed by the owner, who may say so.
  - The ironmonger (west_north, canon): kitchen and utility knives, hammers, a wheel brace, lengths of pipe, a crowbar, rope. No age limit for a grown man in 1990 (the under-16 rule came on 1 Jan 1997). He sells openly; he remembers a buyer by the witness rules (the seller remembers, his ruling of advisor 378), and a knife bought the day before a stabbing is evidence when the police ask round.
  - The ship's chandler (east_chandler, canon): rigging knives, a marlinspike, cargo hooks, line; the same remembering.
  - The pawn's back room (Rita's, with Wayne her back-room hand handling goods that come in off the books): knuckledusters and flick knives, which the law forbade anyone to sell in 1990 (flick knives by the Restriction of Offensive Weapons Act 1959; knuckledusters, butterfly knives, swordsticks and the rest by the Criminal Justice Act 1988 s.141 and its Order, in force 18 Jan 1989); so under the counter, only to a man Rita trusts (rung 2 and up), dearer, and Rita or Wayne knows. Frank can sell weapons there too, the same way.
  - Off a man: disarming him in a fight (CS-08), or searching him when he is down (CS-33).
  - Off a body: the same search; the weapon then carries the dead man's story (who saw it on him).
  - A rival's lock-up, on a raid (the jobs parts).
  - Things to hand: everywhere (CS-06).
  - Guns: RT2-14 as written (Mickey's revolver in the desk once Sheila trusts him; the deckhand at the fish dock on Tuesdays and Fridays after midnight through Rita or Darren's tip; taken from a man or a body; a rival's lock-up). A gun taken from a man who drew one early is a real gun from then on: nothing vanishes; the dial moves when it is seen or heard (CS-23).
  - Carrying, by the law of 1990 (rev1-work/RESEARCH-LAW.md): a blade or point in a public place is an offence (CJA 1988 s.139, in force 29 Sep 1988 by Hansard of 7 Dec 1989; the commencement order not confirmed) unless he has good reason (his work: a docker's or a fisherman's knife on the way to the shift) or it is a folding pocketknife with a cutting edge under 3 inches; in 1990 it carried a fine only (prison came in 1996). Carrying an offensive weapon in public without lawful authority or reasonable excuse is an offence (Prevention of Crime Act 1953: up to 6 months, or 2 years on indictment); that a cosh, knuckleduster or flick knife counts as one in itself (made for injury) is unverified, from memory of the Act's definition and case law, to check from the PC. Owning one at home was not an offence. A constable can stop and search a man he suspects of carrying an offensive weapon or blade (PACE 1984 s.1, extended to blades by CJA 1988 s.140, confirmed) and acts on what he sees (CS-19: a bulge, a hand kept near a pocket, blood, running).
  - Stashing: a weapon under a minicab seat or in its boot is off Frank's body, so a street search of Frank finds nothing; a search of the car (with cause) finds it, and the driver who uses that car may find it first and knows (a crewman who knows is a risk, CS-21).
  - Inventories: what each person owns and carries, and what is in each house, is Monday's people pass (hand-over, below); this part sets only where weapons come from and what the law said.
- Standard: every weapon traceable to a source and a witness; the law of 1990 as researched, unverified points marked.
- Test: S: each source a golden row (bought, the seller remembers; under the counter only at the trust rung; a stashed blade not found on a body search, found on a car search).
- Source: canon (the ironmonger, the chandler, the pawnbroker); RT2-14; his rulings (advisors 376, 378); rev1-work/RESEARCH-LAW.md (legislation.gov.uk enacted and point-in-time texts, Hansard 7 Dec 1989, read 25 Nov 2026).
- Status: designed; the hand-over below.

## CS-33 Searching anyone who is down (revision 1)

- How it works: His ruling (advisor 376): anyone down, out or dead, can be searched, and carries what fits his role. Searching is a combat action like any other:
  - Doing it: kneel and go through his coat and pockets (about 4 s; a constable's belt kit about 6 s). Frank's hands are full and his back is to the street; it makes little noise. Each thing found can be taken or left.
  - What a man carries: by role, from the people pass (wages on a Friday, keys, a knife, a lighter and cigarettes). A beat constable in 1990: a wooden truncheon in its trouser pocket (about 14 inches; longer batons authorised from 1994: from a general summary and a museum entry only, unverified), handcuffs, a whistle, his personal radio and his pocketbook (the 1990 kit for cuffs, whistle, radio and pocketbook unverified, to check from the PC, as his ruling names them); his warrant card.
  - What things do: a truncheon is a cosh's weapon row; the radio lets Frank hear police traffic while he holds it (where cars are sent, a description going out), until the station notices it has gone quiet; the pocketbook holds the day's names, descriptions and times (what the police know, maybe of Frank); keys open the door or car they belong to; a wallet holds money and a name.
  - Consequences: taking anything from a man down is theft, or robbery if Frank put him down; from a constable it is read grave and raises the police response (his ruling); stolen police kit found on Frank later is evidence. A man who wakes with his pockets emptied knows he was robbed and, if he saw Frank's face before he went down, names him. A dead man's things turning up on Frank (his watch, his car, his keys) are recognised by anyone who knew him (his ties remember his things as they remember him).
  - Seen doing it: a man kneeling over another going through his coat is a deed seen in its own right: a witness tells what he saw (robbing a man down); whether the listener hears "he robbed a dead man" or "he killed him and robbed him" is the retelling's blur by distance (CS-17), and the police take whoever was seen as their first name.
  - Using what he took: a stolen warrant card shown to a stranger is a claim (CS-10), weighed by the slots (no uniform, the wrong face, the wrong manner) and mostly fails; impersonating an officer is a charge. Cuffing a man with stolen cuffs is out (no tied people shown, canon and his holding-overnight ruling).
- Standard: everything a man carries is findable; every taking leaves a trace someone can find.
- Test: S: golden rows: a constable searched, his radio carries traffic until the station misses him; a pocketbook's descriptions; a watcher's report of a search.
- Source: his rulings (advisors 376, 378); RESEARCH-LAW.md (police kit, partly unverified); CS-16, CS-17, CS-19.
- Status: designed; carried and owned inventories are Monday's people pass.

## CS-34 What this revision adds that the big three do not (his principle, advisor 377)

Each line: the can-you; checked for fun and for fit with Britain 1990; the animation it needs (a shared set means clips reused across many people and acts). "Beyond" is on paper, from the census and general knowledge of KCD2, RDR2 and GTA V, not a measured comparison.

| Can you | Fun | Fit | Animation |
|---|---|---|---|
| Break a knife man's arm with a bat so he drops it and fights one-handed, in plaster for weeks after (the big three disarm, nobody carries a broken arm for weeks) | yes: a clear, earned win | yes | arm hit and drop (one body, shared set); one-armed guard and walk (one body, reused for anyone in plaster) |
| Cut a face and have the town name the man by his scar, or have Frank named by his | yes: the town's memory made visible | yes | none (a face mark on the head model) |
| Hold a choke as long as you choose, the body telling you when to let go | yes: tension, a choice that matters | yes (D1) | one paired choke loop with release and still variants (two bodies, three clips) |
| Kick a downed man and see it get worse, so stopping at the cue kills nobody | yes: violence that reads | yes (D2, PEGI 18 within canon) | downed man covering, then going still (one body, shared set) |
| Reload and get the same result for the same act (no fishing for luck) | yes for a fair world; some players will grumble | yes | none |
| Take a constable's radio and listen to the police hunt, read his pocketbook for what they know | yes: a new kind of information | yes by his ruling (the 1990 kit to confirm from the PC) | kneel and search (one body over a downed body, one shared set for every search) |
| Open a dead man's flat or car with his own keys | yes | yes | reused door and car clips |
| Buy a knife at the ironmonger and have him remember you when the body is found | yes: consequence with a face | yes (1990: sold openly) | counter hand-over (reused shop clip) |
| Stash a blade under a cab seat to beat a street search | yes | yes (the minicab firm) | reused sit and reach clips |
| Hit the man behind with the sawn-off's spread | yes, grimly | yes, late and rare | reused hit reactions |
| Shoot a runner in the leg and walk alongside him as he crawls, talking | yes | yes, late and rare | crawl cycle (one body, reused for any leg wound) |
| Grab a winded man's knife arm the moment after his swing | yes: timing rewarded | yes | paired disarm (two bodies, two clips: kept and lost grip) |

Checked out: cuffing a man with stolen cuffs (tied people, canon); shooting weapons out of hands at range as a trick (the arm table already covers it, no trick shots).

## CS-35 Lines the 30 outside questions asked for (revision 1)

- How it works, one line each; decided within canon and the rules above, he can overturn any:
  - Thrown things: force by weight, aimed like a blow: light (a bag of shopping, an ashtray) 0.5, middling (a dustbin lid, a chair) 1.2, heavy (a brick, a length of pipe) 1.8; the zone counts as for any blow (the face a quarter more, and it can knock a man down).
  - Falls from height: pushed down a flight of stairs, a man takes force 2.5 to the head or body as he lands (serious about 1 in 5, critical 1 in 30, fixed to the save); off the sea wall onto stone, serious every time and critical about 1 in 4; into water, CS-07. Frank alone is out, never dying (his ruling).
  - A car door opened into a passer-by: the door slam of CS-07 at 1.5 from the seat, 2.0 standing; an assault when meant, and a claim of accident is a cover story weighed against what witnesses saw.
  - A collar grab in a calm talk: a deed at rung 4; the talk goes on with him held (his temper answers: talks, struggles or strikes); a fight starts only when someone strikes.
  - Losing: watchers' menace for Frank falls a little when he loses, less when he stood and took it; losing on purpose looks the same to them unless he plainly pulls his blows; whether a rival then tries the drivers is that rival's temper on Frank's menace.
  - Two people Frank wronged who do not know each other act alone, each on his own grudge; if they meet and both name Frank, the shared grudge counts as a tie and they may join.
  - A man who follows Frank uses the tailing rules both ways (blueprint 1.1.6) and learns where he lives only by seeing him go in.
  - Suspicion adds up: a man who catches the same coat or face behind him twice within the hour turns uneasy; a third time he challenges or tells someone.
  - A remembered noise: a second noise within a minute of the first makes him alert, not uneasy. A car door slam carries about 20 m at night; an alarm bell about 150 m.
  - Through windows: a figure in a lit room shows to the street at night; from a dark room a watcher sees the street at its own light; net curtains halve sight both ways and hide a face; height gives a view over walls, nothing more.
  - A searching man in a crowd looks at faces one at a time, about one a second within 10 m, and finds Frank only if he knows his face and looks at him.
  - A bribed witness later beaten: the bribe binds only while his report rule holds; the beating raises his grudge and drops his regard, so he may now tell, and telling of the bribe costs him too, which his law weighs.
  - The sawn-off at the legs: under 5 m the shot stays in the man aimed at (the leg is wrecked: cannot run, critical about 4 in 10); 5 to 15 m the spread takes both legs and can hit a man within a metre beside or behind; beyond 15 m scattered pellets.
- Standard: each line a golden row.
- Test: S: golden rows.
- Source: rev1-work/RESULTS-30.md (the fresh tester's what-to-add list).
- Status: designed.

## Hand-over to Monday's people pass

- Carried and owned inventories by role (what each person, house, shop, lock-up and car holds), including the constable's kit above, the dockers' Friday wages and who carries a knife for work (s.139's good reason).
- Owners' memory of their things (a recognised watch, car or keys) as a slot on the thing.
- Rita's and Wayne's under-the-counter stock and the trust rung for it; the ironmonger's and chandler's stock lists and prices.

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
- New: CS-08, CS-13, CS-16, CS-17, CS-19, CS-20, CS-21, CS-22, CS-24, CS-25; revision 1 adds the chance rule, CS-31 to CS-34 and the hand-over.
- Changed by revision 1: RT-10 (its "before War a hit wounds and never kills" replaced by CS-23 and CS-31, D3 yes; its arm and leg shots kept, Y1.5); RT2-14 kept and referenced by CS-32.
- Stale text to mark replaced, not edit: the weapons spec's bottle, "bad drink", wire and cord, and "arrest, no chase"; FEEL-TARGETS-MELEE C14 and drill M2.
