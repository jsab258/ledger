# Coverage audit 2 of 5: Hitman (World of Assassination)

STATUS: SPEC (research delivery). Branch `research/coverage-audit-hitman`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. It is a mapping and a set of
recommendations. If Jafar rules something IN, the studio turns that into tiles
and queue items then, not before. No tile is proposed here, no queue item is
filed, and the inventory is not touched.

## 0. How to read this file

The four columns, the four claim labels (CITED, DERIVED, ASSUMED, HOLE) and the
note about the word collision on "absent" are all defined in
`production/research/coverage-audit-kcd2/DELIVERY.md` section 0, and are not
repeated here. Two things do need saying again.

THE SOURCING LIMIT, re-measured this session and not carried over on trust.
`www.gamedeveloper.com` was fetched for the AI of Hitman article and answered
`EGRESS_BLOCKED`, as `en.wikipedia.org` and two others did for game 1. WebSearch
works. So every external citation below is the search channel's summary of a
named page and not a page read in full. Claims about this repository carry no
such limit and name their file and line.

D24 STILL DOES NOT EXIST in this checkout (game 1, section 0.4). The brief's own
formulation of it is used as the test and cited as such.

QUOTATIONS from repository files written before the formatting law of 31 August
have had em-dashes replaced by commas and italics dropped. The words are
otherwise unchanged and the file and symbol are given.

## 1. Why this game, and what the numbers came out as

The brief's reason is right and the audit confirms it harder than expected.
Hitman is a game about being looked at in a small dense place, which is the same
sentence as pillar 1 and pillar 6. GTA is a game about a large place.

**32 systems** enumerated, in four groups, mapped against the 91 tiles.

| Column | Count |
|---|---|
| COVERED | 6 |
| PARTIAL | 5 |
| ABSENT | 20 |
| RULED OUT | 1 |
| **Total** | **32** |

Of the 20 absent: **10 IN, 8 OUT, 2 ASK.**

THAT RATIO IS HALF, AND THE BRIEF SAID TO EXPECT MOST THINGS OUT, so it needs
defending rather than presenting. Game 1 came out at 9 IN of 35 absent, which is
26 percent. This one is 50 percent, and the reason is not a loosening of the
bar: it is that Hitman's entire system list IS perception, disguise, evidence
and being challenged, which is the list D24's test says to fund. When a game
contains almost nothing but the thing we are building, a low IN rate would mean
the audit was not reading it.

The 10 is also not 10 pieces of work, and the accounting matters more than the
headline. Two are riders on other entries (A9 on A8, B3 on B2), one is naming
work rather than building work (A11, which already exists in code), and two are
smaller and conditional (C3, D5). Five distinct things are recommended, and
those five are what the summary carries.

## 2. The finding, continued from game 1

Game 1 found four built systems that no tile names. This game found a fifth, in
the same place and of the same kind.

**`Core/Arsenal.cs` already has a four-rung concealment model, and it is better
than Hitman's.** The enum is titled "How hard it is to explain if somebody finds
it on you" and reads: `Innocent` ("A bottle, a bar, a kitchen knife. Nobody
asks."), `Concealable` ("Fits under a coat and raises an eyebrow."), `Damning`
("Fits, and is damning."), `Impossible` ("Does not fit. A man with a bat has
already said something."). `Arsenal.Fits` enforces it with `CoatCapacity = 2`
and `CoatCapacityIfOneIsSmall = 3`, and refuses more than one Impossible item.
Hitman's version of the same idea is two states, concealed or conspicuous.

Token counts run over the whole inventory file this session: `conceal` 0,
`concealment` 0, `blend` 0, `cctv` 0, `tape` 0. The seven hits for `camera` are
all the player camera tile.

DERIVED, and it is the same conclusion game 1 reached by a different road: the
inventory is a good map of what the studio has THOUGHT ABOUT and an incomplete
map of what it HAS. The finding that follows is A10 below: a four-rung
concealment model is in the code and nothing in the game ever tests it, so the
rungs have never cost anybody anything.

## 3. The mapping

### A. Disguise, and being challenged (11)

**A1. A disguise changes where you may go and who stops you.** CITED (search
summary of the Hitman Fandom wiki and Steam community guides). **PARTIAL**, tile
"doors and who gets in" (exists), whose note reads "A door asks for an
introduction, standing, a payment or the right clothes". The uncovered part is
that the outfit works on the street and not only at a door.

**A2. Enforcers: specific named NPCs who see through a specific disguise,
because they would know a real one.** CITED (search summary of Steam community
discussion, "How do I understand if someone is noticing my disguise"):
"Enforcers are those who have the white dot above their head indicating that
they can detect you."
**ABSENT** as a named concept. **IN, and it is mostly already ours.**
`Core/Perception.cs` gates rung 4, recognition, on
`RecognitionFamiliarity = 0.35` and reaches 25 metres, with the comment "at
twenty metres in the rain a stranger is a shape and your neighbour is you".
That IS the enforcer rule, derived rather than authored: the people who defeat
your disguise are the people who know you. Hitman had to hand-place enforcers
because its NPCs have no relationships. We get them free from the acquaintance
graph, and against the D24 test this is perception and memory in one object.
What is missing is not the rule, it is that nothing anywhere names the rule as
a system, so nobody can design the disguise verb against it.

**A3. The white dot: the game tells you which people those are.** CITED (same).
**ABSENT.** **ASK**, and see A7, with which it is one question.

**A4. Lookouts: NPCs who detect you regardless of outfit or location.** CITED
(search summary of Steam community discussion): "a new species of NPCs that act
as Super Enforcers since they can detect you no matter what outfit you have or
where you are."
**ABSENT.** **OUT, and firmly.** A character who sees through everything by
authorial fiat is exactly the psychic guard D11 names as the failure mode to
avoid, in a costume. Every LEDGER identification has to come out of the ladder,
which is what makes it arguable and therefore fair.

**A5. Trespass zones: your outfit is wrong for this room, and everyone in it
becomes an enforcer.** CITED (search summary of Steam community discussion):
"If you are trespassing or doing something illegal like dragging a body then all
dots on the minimap will turn white because they are all enforcers."
**PARTIAL**: "doors and who gets in" (exists) plus "interiors you can enter"
(typed absent). The concept needs rooms, and the rooms are the blocker.

**A6. Vision cones: detection fills by angle and distance, and the rate varies
with what you carry, whether you are crouched, and how centred you are.** CITED
(search summary of Steam community discussion).
**COVERED**, and ours is at least as detailed: `Perception.IdRung` takes metres,
light level, familiarity, a distinguishing mark and `faceToward`, with
`DetectRangeMetres = 40`, silhouette at 35, mark at 18, face at 8 and
recognition at 25, all scaled by `LightFactor`.

**A7. A suspicion meter that fills before detection, visible to the player.**
CITED (search summary of the Hitman Fandom wiki, "Suspicion Meter").
**ABSENT** as a live readout. **ASK**, with A3. See the argument at the end of
this section.

**A8. Blend-in: performing an action consistent with what you appear to be
suppresses suspicion.** CITED (search summary of the Hitman Fandom wiki, "Blend
in"): "a feature that allows the player to evade detection by imitating an
innocent bystander consistent with whatever outfit he is wearing".
**ABSENT.** **IN, and it is the single most transferable idea in this game.**
LEDGER's perception answers whether you were SEEN. It has nothing that answers
whether what you were doing NEEDED EXPLAINING. Those are different facts, and
the second is the one that makes a dense street playable rather than a place
where you are simply always visible. A man standing at a bus stop at eight in
the morning is invisible; the same man in the same place at three is a fact
somebody will mention. The inputs already exist: the daily routines tile puts
everybody somewhere for a reason, so the game already knows what a reason looks
like.

**A9. Compromised: once someone has witnessed you doing something, you cannot
blend in around them until they are gone.** CITED (search summary of the Hitman
Fandom wiki, "Alert Levels").
**ABSENT.** **IN, as a rider on A8 rather than as its own work**, and ours is
already stronger by construction: Hitman clears the state at the end of the
mission, LEDGER's per-NPC memory never clears it, so "she has seen you do this
once and will not buy it again" falls out of the existing memory store rather
than needing a flag.

**A10. Frisking and metal detectors at thresholds.** CITED (search summaries of
the Hitman Fandom wiki, "Frisking" and "Metal Detector"): in the World of
Assassination trilogy the metal detector is replaced by pat-downs, and "failing
a frisk will either cause the guard to confiscate your weapons and allow you
access, or immediately turn hostile".
**ABSENT.** **IN, and section 2 is the argument.** The four-rung concealment
model is written, tested and never exercised: nothing in the game ever asks what
is under the coat, so the difference between Concealable and Damning has never
cost a player anything. A doorman who pats you down is period-correct for a
British club in 1990, the doorman already exists as a hook in the doors tile,
and it turns an existing model into a decision made at the door, which is the
Coat's own stated purpose.

**A11. Concealed versus conspicuous items, with a briefcase to smuggle one
past a check.** CITED (search summary of the Hitman Fandom wiki, "Frisking").
**ABSENT from the inventory, BUILT in the code** (section 2).
**IN, but the work is a tile and not a system.** The briefcase half is OUT: a
container that launders one illegal object through one checkpoint is a puzzle
piece for a level-replay game, and the four rungs already carry the same
decision with more texture.

THE ASK THAT A3 AND A7 ARE, stated once. Hitman shows you, live, who can see
through you and how close you are to being noticed. That readout is most of why
a Hitman level is playable rather than merely dense. D12 rules that "NPC minds
are never shown as ground truth" and that the player sees only their character's
model of what each NPC knows, assembled strictly from evidence they have, with
"no free omniscient read". The tension is real and it is not obviously a
contradiction: Tom Novak WOULD know, walking into his own pub, which of the
people in it know him well enough that a change of coat will not help, because
that is his own knowledge and D12 surfaces the player's own memory fully. So
there is a version of the white dot that is D12-compliant and a version that is
not, and the line between them is exactly where Jafar's judgement is needed. The
same question, one step earlier, is whether the player feels being looked at
while it is happening or only learns about it afterwards.

### B. Evidence, and the record the world keeps (6)

**B1. Security cameras record to a tape, and the tape can be found and
destroyed.** CITED (search summary of the Hitman Fandom wiki, "Silent
Assassin"): "Do not get caught on the camera. If caught, destroy the
recordings."
**ABSENT.** **IN, and canon has already done the design work.** `canon.md`
specifies CCTV as rare (the bank, and a second site that is Jafar's to name),
with "tape recycled weekly", plus "One camcorder in town, a rare witness type".
That is a witness that does not talk, does not forget, cannot be intimidated,
and has a one-week clock attached. It is the cheapest possible variation on the
gossip mill because it is the mill's opposite, and it makes a whole class of
play (get to the tape before Thursday) exist for the cost of an object with a
timer.

**B2. A body is found, and the finding is an event with a time and a finder.**
CITED (search summary of the Hitman Fandom wiki, "Alert Levels"): "Bodies always
alert bystanders if found, whether they are dead or unconscious".
**ABSENT.** **IN, and it is a genuine hole rather than a port.**
`Core/Homicide.cs` records a killing with a day, an hour and a place, tracks
`SawYouDoIt` and the people who know there is a body without being able to name
who made it, and derives police pressure from them. What it does not have is the
body as an object that sits somewhere until somebody walks past it.
`Core/Observation.cs` has an `Aftermath` slot ("Body, blood, a broken door, an
object left behind"), so a witness CAN catch the aftermath of an act they saw
the end of, but nothing models the yard being opened on Tuesday morning by the
man whose job it is. `Core/Traces.cs` states the purpose this would serve in its
own header: "One violent minute should cost three in-game days". The delay
between the act and the discovery is where those three days live.

**B3. Bodies can be hidden, and a container holds two.** CITED (same).
**ABSENT.** **IN as a rider on B2**, because a discovery clock with no way to
push it back is a timer rather than a decision. The two-per-container rule is a
level-design constraint and does not transfer; what transfers is that hiding
takes time, takes a place, and can be witnessed, which is the shape
`Traces.Dispose` already uses for objects (it records where, and whether the
disposal was seen).

**B4. Accidents: a death staged so that it reads as not-a-murder.** CITED
(search summary of the Hitman Fandom wiki, "Silent Assassin"): targets killed by
accident or poison may be found without voiding the rating.
**ABSENT.** **OUT.** Hitman needs accidents because you kill on every mission
and the killing needs variety. D18 makes killing here "possible, rare,
permanent, and the town remembers it forever", which is the opposite design
pressure: a rare permanent act does not want an optimisation surface. The one
idea worth keeping is already implied by the seven slots, which can produce a
sighting that contains an aftermath and no actor.

**B5. A witness voids the rating, and killing the witness does not restore
it.** CITED (same): "Killing a witness will not regain the SA rating".
**COVERED**, and ours is the better-argued version. `Core/Homicide.cs` states
the problem in its header ("killing a witness has to GENUINELY WORK. If it does
not stop the rumour, the choice is fake and the player notices inside one
attempt") and answers it with arithmetic instead of a rule: killing the only
witness drops the police from a manhunt to an investigation, "never back to
procedure, and never to nothing", and "each body you add to fix the last one
leaves you worse off than before the first."

**B6. An NPC whose outfit you took is later found unconscious and missing.**
CITED (DERIVED from the body rules above; I did not find a source describing
this as its own system, so it is recorded as a HOLE for how Hitman handles it).
**ABSENT.** **OUT.** Small, and it rides on B2 if B2 lands.

### C. The world, and how it stays legible while full of people (9)

**C1. NPCs run looping routines written to fit the fiction of the place.**
CITED (search summary of PlayStationTrophies coverage of IO Interactive's GDC
2012 crowds talk): "they're serving drinks, applying makeup, guarding entryways,
cooking dinner, whatever is needed to fit the fiction of the location."
**COVERED**, tile "daily routines" (exists).

**C2. Crowd density: over 1000 crowd NPCs active in a level and still
reactive.** CITED (same, about Absolution: "techniques and optimizations used to
achieve 1200 character crowds while running at 30fps on current-gen consoles").
**PARTIAL**, tile "the crowd you see" (partial), which reads 65 walkers in the
headless sim and no committed frame of anybody walking the Unreal street.
NOT A RECOMMENDATION, A BENCHMARK: 1200 at 30fps on 2012 console hardware is the
number the density pillar should eventually be argued against, and it belongs to
queue topic 17 rather than to this audit.

**C3. Distractions: a thrown coin, a running tap, a switched-off generator,
each pulling an NPC off their route to investigate.** CITED (search summaries of
the Hitman Fandom wiki, "Distractions" and "Alert Levels").
**ABSENT.** **IN, small, and conditional on A8 landing first.** The period
version is already standing on the street: `canon.md` makes phone boxes and
answering machines the late-analog spine, and the tile "phone boxes and
answering machines" (exists) reports twenty calls tried, nine reachable, eleven
rung out. Ringing the box on the corner to move a man off a doorway is a
distraction verb built from infrastructure that already works, and unlike a
thrown coin it is itself a perceivable act with a caller who can be traced.
Worth doing only once being-seen and being-explicable are both modelled,
because a distraction with nothing to hide from is a toy.

**C4. Alert escalation: unaware, searching, hunting, hostile.** CITED (search
summary of the Hitman Fandom wiki, "Alert Levels").
**PARTIAL**: "suspicion and heat" (partial) and "the law and the police"
(partial), whose note records that arrest is currently unreachable because
`CoatHost.Arrested` has no caller outside Core.

**C5. Mission Stories: authored, guided chains discovered by eavesdropping or
by examining something.** CITED (search summary of the Hitman Fandom wiki,
"Mission Stories"): "optional guided paths which help assist the player in the
completion of mission objectives".
**ABSENT.** **OUT, and the reason is the whole argument of the project.** A
mission story is a hand-authored route through a sandbox, added because IO's own
user research found the learning curve too steep (CITED, search summary of the
GDC talk listing, "Level Design in HITMAN: Guiding Players in a Non-Linear
Sandbox": "user research showed players had fun but the learning curve was too
steep"). Our equivalent of guidance has to come out of the simulation, or the
moat is decoration with a guided tour running past it. That said, the PROBLEM
Mission Stories solve is real and we will meet it: it is queue topic 7, how
emergent-story games make their stories legible, and this is the strongest
argument I have found for keeping that topic high in the queue.

**C6. Eavesdropping as the way information enters the player's hands.** CITED
(same): mission stories "typically reveal themselves either after eavesdropping
in on an NPC conversation".
**COVERED.** D12 lists eavesdropping among the diegetic verbs by name, and the
tile "the town's own voice" (exists) reports 540 of 3240 overheard lines
pointing at something the player did.

**C7. Instinct mode: see NPCs, items and routes through walls.** CITED (search
summary of the Hitman Fandom wiki, "Instinct Mode").
**ABSENT.** **OUT, and it is the clearest OUT in this audit.** It is the free
omniscient read D12 bans in the same words ("There is no free omniscient read"),
and D12 gives the reason: "if knowing is free, then asking around, buying gossip
and eavesdropping are decorations rather than verbs". Hitman can afford it
because its information has no cost; ours is the product.

**C8. A drawn weapon reads completely differently from a holstered one.**
CITED (search summary of Steam community discussion on detection).
**COVERED**, and named as its own perception slot: `Core/Observation.cs`
`Slot.Draw`, "The weapon appearing. Vision only, and loud socially even when the
weapon is silent."

**C9. One small footprint, many vertical layers, learned by repetition.**
CITED (search summary of the GDC talk listing and the noclip documentary
reference).
**COVERED** by pillar 6 ("Small and dense, built to expand") rather than by any
tile, because it is the shape and not a system.

### D. Structure, and what the game is for (6)

**D1. A planning phase: loadout, starting location, smuggled agency pickups,
all chosen before you know what will happen.** CITED (search summary of
StrategyWiki, "HITMAN/Gameplay").
**PARTIAL**, tile "inventory" (partial), and the convergence is worth recording:
`Core/Coat.cs` reached the same design independently, in the same words. "The
whole decision is what did I bring, made at the door, before you know what the
night holds, which is precisely what makes it a decision rather than a shopping
trip."

**D2. Replay as the core loop: the same place many times, until you know it.**
CITED (same). **ABSENT.** **OUT.** LEDGER is one continuous town with a memory
that never resets, so there is no second attempt at a night. The player learning
the place by walking it is D11's second progression axis and happens anyway.

**D3. Challenges and Mastery unlocks tied to level progression.** CITED (same).
**RULED OUT** by D11: nothing about the player gets numerically better.

**D4. Elusive Targets: one attempt, no saves, gone if you fail.** CITED
(search summary of the Hitman Fandom wiki).
**ABSENT.** **OUT as a mode**, but it is the same question as the save scarcity
ASK raised in game 1 (F1 to F3 there), and the two should be answered together
rather than separately.

**D5. Freelancer showdowns: identify the real target among many suspects from
described traits, such as what they are wearing or that they sneeze.** CITED
(search summary of the Hitman Fandom wiki, "Freelancer", and ScreenRant).
**ABSENT.** **IN, and it is the most interesting structural idea Hitman has for
us.** It is our own identification ladder run backwards. Rung 1 is "a man, big,
long coat" and rung 2 is "the one with the limp" (`Core/Perception.cs:157` to
`:159`), and those are exactly the terms in which a Freelancer suspect is
described. Today the ladder only ever runs from the town toward the player.
Making it run the other way, so that a rumour gives Tom a rung-2 description and
he has to find the man it fits, turns the information pillar into something the
player DOES rather than something that happens to them. Cheap in model terms
because the descriptions already exist; the work is a surface and an authored
reason to care.

**D6. Nothing carries between missions: the level resets, the NPCs forget.**
CITED (DERIVED from the mission structure and the per-mission Silent Assassin
rating; no source was needed for the absence of persistence, but it is DERIVED
rather than CITED and should be read as such).
**ABSENT.** **OUT, definitionally, and it is the sentence this whole audit turns
on.** Hitman is a closed system that forgets, and its brilliance depends on
that: the level is a clockwork box you may wind up and break as many times as
you like. LEDGER is an open system that does not forget. Everything Hitman does
well with observation, we can take. Everything Hitman does with structure
assumes the forgetting, and cannot be taken without it.

## 4. What could not be established

1. **The GDC talks are behind a paywall.** "Level Design in HITMAN: Guiding
   Players in a Non-Linear Sandbox" and "Crowds in Hitman: Absolution" are the
   two primary sources for sections C1, C2 and C5, and I have their titles,
   speakers and the search channel's summary of the listing pages, not their
   content. The 1200-crowd figure and the user-research claim both come through
   that channel. HOLE.
2. **The AI of Hitman (2016)** on gamedeveloper.com, which is the best single
   secondary source on the perception model, is egress-blocked. Everything in
   section A about vision cones and enforcers therefore rests on community
   descriptions rather than on a technical write-up. HOLE, and it is the one I
   would most want closed.
3. **Whether Hitman NPCs have any memory at all across a single mission**
   beyond the alert and compromised states. The sources describe states, not
   storage. D6 is DERIVED, not CITED.
4. **B6** (the missing NPC) could not be sourced as a system.
5. **Systems not enumerated.** Contracts mode, the sniper maps, the story, the
   escalation contracts, multiplayer Ghost Mode, the accessibility options, and
   the whole of Hitman Absolution's different design (Instinct as a resource,
   the notoriety system) are outside the 32. Absolution's notoriety in
   particular is a per-region reputation that persists across missions, and it
   is the nearest thing in this series to our moat. NOT ENUMERATED HERE and
   worth a pass of its own if the reputation ASK from game 1 goes anywhere.

## 5. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Hitman Fandom wiki, "Difficulty Level/Silent Assassin", https://hitman.fandom.com/wiki/Difficulty_Level/Silent_Assassin
- Hitman Fandom wiki, "Alert Levels", https://hitman.fandom.com/wiki/Alert_Levels
- Hitman Fandom wiki, "Suspicion Meter", https://hitman.fandom.com/wiki/Suspicion_Meter
- Hitman Fandom wiki, "Blend in", https://hitman.fandom.com/wiki/Blend_in
- Hitman Fandom wiki, "Distractions", https://hitman.fandom.com/wiki/Distractions
- Hitman Fandom wiki, "Instinct Mode", https://hitman.fandom.com/wiki/Instinct_Mode
- Hitman Fandom wiki, "Mission Stories", https://hitman.fandom.com/wiki/Mission_Stories
- Hitman Fandom wiki, "Frisking", https://hitman.fandom.com/wiki/Frisking
- Hitman Fandom wiki, "Metal Detector", https://hitman.fandom.com/wiki/Metal_Detector
- Hitman Fandom wiki, "Freelancer", https://hitman.fandom.com/wiki/Freelancer
- StrategyWiki, "HITMAN/Gameplay", https://strategywiki.org/wiki/HITMAN/Gameplay
- Steam community, "How do I understand if someone is noticing my disguise?", https://steamcommunity.com/app/1659040/discussions/0/4338735599617531740/
- Steam community, "Something I've always wondered", https://steamcommunity.com/app/1659040/discussions/0/4143942360096776899/
- Steam community, "NPC alert level details?", https://steamcommunity.com/app/236870/discussions/0/364042262877531023/
- GDC Vault listing, "Level Design in 'HITMAN': Guiding Players in a Non-Linear Sandbox", https://www.gdcvault.com/play/1023872/Level-Design-in-HITMAN-Guiding
- GDC Vault listing, "Crowds in Hitman: Absolution", https://www.gdcvault.com/play/1015526/Crowds-in-Hitman
- PlayStationTrophies, "GDC 2012: IO Interactive Focusing on Quality Rather Than Quantity When it Comes to Crowds", https://www.playstationtrophies.org/news/news-6081-gdc-2012-io-interactive-focusing-on-quality-rather-than-quantity-when-it-comes-to-crowds-in-hitman-absolution.html
- Game Developer, "The AI of Hitman (2016)", https://www.gamedeveloper.com/design/the-ai-of-hitman-2016- (EGRESS BLOCKED, listed because it is the source this file most needs)
- ScreenRant, "Hitman III: 10 Facts To Know About The Freelancer Game Mode", https://screenrant.com/hitman-freelancer-mode-important-facts/
- dbltap, "Hitman 3 Silent Assassin Requirements", https://www.dbltap.com/posts/hitman-3-silent-assassin-requirements-01exd43krjht

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`, `canon.md`,
`ledger-v2/respec/decision-register/D11-player-progression.md` and
`D12-information-surfaces.md`, `ledger/Assets/Scripts/Core/Arsenal.cs`,
`Core/Perception.cs`, `Core/Observation.cs`, `Core/Homicide.cs`, `Core/Coat.cs`,
`Core/Traces.cs`.
