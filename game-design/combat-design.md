<!-- Imported 21 October 2026 from Jafar's Claude doc "LEDGER Combat: Final State" (12 October 2026, revision 12), https://claude.ai/code/artifact/1320a41f-aa3b-44d2-9e74-4713a3716a15, as his order of 21 October asks. His text unchanged but for one word: "Stanley knife" in the carried-weapons tier reads "utility knife" here, because canon makes every make fictional (the cloud's note of 13 October). It replaces game-design/combat-spec.md, marked replaced at its top. -->

# LEDGER Combat: Final State

Oct 12, 2026 · @Jafar

Combat in LEDGER is a ladder of escalation the whole street watches: good to do, costly to have done. Tom's power comes from his people, the street is his weapon, and fights must look and feel AAA. Jafar ruled the five decisions behind it on 12 October 2026, and this replaces the July combat spec. Building starts after the walk passes, with the animation source tested first.

## The rulings it rests on

Every part of this design follows from Jafar's own rulings, newest first; the five of 12 October are new and still have to be recorded in the repository.

| Date | Ruling | Where it is recorded |
| --- | --- | --- |
| 12 Oct 2026 | Fighting is good to do and costly to have done. Tom's power is people, not his fists. Fighting must look and feel AAA, which changes D24's spend rule for fighting only. Guns are in the final game, rare, built after melee works. Tom cannot die. | This doc; to go into RULINGS.md, DECISIONS.md and canon.md |
| 3 Oct 2026 | A threat can stop a report to the police, never the street's talk. | RULINGS.md |
| 23 Sep 2026 | Fists and improvised weapons, firearms rare; the crew act on orders; no jump. | RULINGS.md |
| 21 Sep 2026 | Three combat gaps, in order: being outnumbered, running away as a way out, the police arriving during a fight. Ordering a named man hurt through a crew member leads the crime verbs. | D56, queue item 402 |
| 14 Sep 2026 | LEDGER is not a shooter; fighting may exist and must not look broken (now changed for fighting by 12 Oct). | canon.md, D24 |
| 10 Sep 2026 | Violence stays, with blood and light gore; no torture and no cruelty as spectacle; killing is possible, rare, permanent and remembered forever. | canon.md, content rule D18 |
| 31 Aug 2026 | Melee first (fists, bats, blades), then improvised weapons, then scarce firearms; one gunshot is a town-wide event. | D4 |
| 28 Jul 2026 | Violence is a legitimate tool; witnesses can be killed, and consequences and police follow. No health bar now, a minimal HUD later. | game-design/combat-spec.md, section 7 |

## The ladder

Combat is not a mode the player enters; it is eight rungs of escalation, and he can stop on any of them. Each rung is an act with the seven perceivable slots, so identification, memory and gossip treat it like any other deed.

| Rung | What the player does | What the street takes from it |
| --- | --- | --- |
| 1. Stare | Holds a man's eye too long | A tension others notice; nothing to report |
| 2. Square up | Changes stance, visible to everyone | Witnesses start paying attention before anything lands |
| 3. Threaten | Says or shows what will happen | Can stop a report to the police, never the street's talk |
| 4. Shove or grab | Pushes him away, takes his collar, pins him to a wall | A scuffle: talked about, rarely reported |
| 5. Strike | Lands a committed blow | A fight: most who see it report it; injuries begin |
| 6. Weapon out | Shows a knife, a bat or a gun | The street scatters; a gun out is news across town |
| 7. Weapon used | Cuts, clubs or shoots | Police interest, a hospital visit, a weapon that can be traced |
| 8. Kill | A man does not get up | A body: a fact no rumour can soften; the police from procedure upwards |

Most confrontations should end on rungs 1 to 4. Menace is the everyday form of combat; blows are the escalation, and each rung up costs more than the one below.

Finishing a man who is already down is never a move in the flow of a fight. It is a decision taken in the quiet afterwards, with the street watching.

## How a fight feels

A fight must look and feel as good as the best grounded melee in AAA games, and the player pays for it afterwards, not during.

- **Weight.** Every blow commits the body, and a miss leaves you open. Contact is sold by a few frames of hit-pause, a jolt of the camera and the sound, never by numbers on screen.
- **Readable.** Every incoming blow has a wind-up the player can read from the attacker's body.
- **Learnable.** A skilled player wins most fair one-on-ones. Mashing tires you out and loses.
- **No mode.** No lock-on, no combat music, no arena. The camera closes in a little and the street carries on around the fight.
- **No health bar.** Condition shows in posture, breathing, a guard that drops, blood and a limp. A minimal HUD exists as a settings switch, so the values are data from day one.
- **Accessible.** A longer wind-up window and an auto-resolve option: the same fight at a different tempo, not an easier one.

Study 14 sets the numbers this section still lacks, measured in KCD2 and Mafia: wind-up, strike and recovery times; hit-pause length; blows and stamina to put a man down; how many attackers swing at once.

## Tom, the crew and the odds

Tom does not get better at fighting; he gets stronger through the men who fight for him, the weapons he carries and the name he has.

- **A fair one-on-one is roughly even**, and skill tips it.
- **Two against one is deadly; three is a beating.** Being outnumbered is the first of the three gaps to build, because it is what makes a crew worth having.
- **The crew changes the odds:** a man at your shoulder, a man on the door, a man you send.
- **Ordering a named man hurt** makes the man you send a second person who knows, with his own nerve and loyalty ceiling. The accomplice is the risk, not the alibi.
- **Crew who watch you fight remember it**, as loyalty and as fear; both are already modelled.
- **Other people fight too.** A feud between two townspeople can turn into a fight the player can watch, join or break up.

## The street is a weapon

The surroundings do much of the work: two-person moves against walls, doorways and the quay are what make a street fight look AAA.

- **Places:** walls, doorways, shop windows, railings, car bonnets, stairs, and the quay edge into the harbour.
- **Things at hand:** a brick, a chair, a snooker cue, a wheel brace from a cab boot, a cargo hook, an ashtray, a length of pipe, a dustbin lid.
- **Within the content rule:** nothing to do with drink, so no bottles or glasses as weapons; no cruelty as spectacle; blood and light gore are allowed.
- **How it is built:** each move against a surface is a paired animation of two bodies, lined up to that surface. Study 14 sets how many of these a street needs.

## Weapons

Four tiers, each louder than the last; every make is fictional, and firearms are built last, only after melee works.

| Tier | Examples | Carried and seen | What the town makes of it |
| --- | --- | --- | --- |
| Fists | None | Nothing to carry | A fight |
| Improvised | Brick, chair, snooker cue, wheel brace, cargo hook | Picked up on the spot and left behind, where it can be found | A fight that went further |
| Carried | Cosh, knuckleduster, utility knife, flick knife, bat | Can be seen on you and found in a search; has a history and has to be got rid of | A man who came ready |
| Firearms, rare | Sawn-off shotgun, old revolver | Hard to get, noticed, searched for | One shot is a town-wide event; armed police come only when a gun is involved |

## How fights end

Every fight ends one of five ways, and none of them ends the game.

- **Someone backs off.** Backing off is a real option and often the best one.
- **Someone runs.** A foot chase the runner can escape through alleys, yards and doorways. Whether he was recognised decides what follows.
- **Someone goes down.** Then comes the quiet decision: leave him, rob him, or finish him.
- **The police arrive mid-fight.** A beat officer first, then more. Running from them is a new offence, and an arrest leads to custody and court as the 1990 police research describes.
- **People step in.** Friends pull their man away, bystanders shout, a shopkeeper comes out.

Tom can be beaten, stabbed or shot, but he cannot die. He wakes in hospital or on the pavement with the injuries, the bill, and a street that knows he lost. The hospital is already a witness.

## The aftermath

The consequences of violence were built before the violence, in the C# Core that the Unreal port is checked against, and they carry over unchanged.

- **Injuries** last, heal on a schedule, turn bad untreated, leave scars and show in the walk (Core/Harm.cs).
- **Treatment** costs money and plants a witness who can place you somewhere on a given day.
- **Blood** stays on clothes until washed, which needs water and privacy.
- **Weapons** have a history and a risk in getting rid of them.
- **Feuds** run between named people, who then refuse to work together.
- **A body** is a fact no rumour can soften. The police move from procedure to investigation to manhunt; killing the only witness takes a manhunt down to an investigation, never further (Core/Homicide.cs).
- **The crew who saw** get a permanent loyalty ceiling, and the frightened one is the one who talks.

New for Unreal: bruises and cuts on the MetaHuman faces, blood on the clothes, and the limp in the walk.

## The animation question

Combat will stand or fall on animation, as clothes did, so the source of the moves is tested in the lab before anything is built.

**Unreal tools that cut the number of moves needed**

- Motion matching, already planned for the walk, for footwork and stance.
- Motion warping, which lines two bodies up so blows and grabs connect.
- Physics-driven hit reactions, blended over a few authored ones.
- Paired animations for grabs, shoves and moves against walls.

**Sources to test, within Jafar's limits** (no filming himself, no paying hundreds, nothing marked NoAI)

- Mixamo, free and already in use.
- Free motion libraries whose licences allow games.
- AI-generated motion, including motion taken from video.
- Fixes keyed by the AI on top of any of these.

**The test:** one wind-up, one strike, one hit reaction and one shove into a wall, judged in the game camera beside Study 14's reference. Two routes are tried, then the test is set aside under the usual rule if neither passes.

## How it gets built

Research and the animation test come first; building starts only after the walk passes, because both depend on feet and bodies in contact.

1. **This week, cloud:** public research on KCD2's and Mafia's combat (COMBAT.md), set against this design.
2. **PC back, lab:** Study 14 in the games' files sets the exact numbers: timings, move counts, reactions.
3. **Lab:** the animation source test.
4. **After the walk passes:** the first combat test, two men, one shove and one strike with hit reactions, in the game camera, through the usual gate.
5. **The lower rungs:** stare, square up, threaten, shove and grab, tied into perception and gossip.
6. **The three gaps, in Jafar's order:** being outnumbered, running away, the police arriving; then ordering a man hurt and the other crew verbs.
7. **The street as a weapon,** with improvised and carried weapons.
8. **Firearms, last.**

The builder imports this doc as game-design/combat-design.md when the PC is back, and the July spec is marked as replaced; its record of what the Core built stays as reference.

## What changed from July

The July spec's consequences survive; its feel, its scope and its setting do not.

| July spec | Now |
| --- | --- |
| Tom runs a bar, is "not a fighter", and fights feel out of control | Tom runs Mickey's minicab firm; fights are good to do and cost afterwards |
| Even the best play won about a quarter of fair fights | A skilled player wins most fair one-on-ones; being outnumbered is deadly |
| Five verbs, fought one against one | An eight-rung ladder, crews, the street as a weapon |
| Guns out of scope | Guns in the final game, rare, built last |
| Fighting only had to not look broken (D24) | Fighting must look and feel AAA |
| Whether Tom can die was not settled | Tom cannot die |
| Unity and capsules | Unreal, MetaHumans and the game camera |
