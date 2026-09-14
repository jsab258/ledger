# Coverage audit 3 of 5: Red Dead Redemption 2

STATUS: SPEC (research delivery). Branch `research/coverage-audit-rdr2`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. It is a mapping and a set of
recommendations. No tile is proposed, no queue item filed, the inventory is not
touched, and the decision is Jafar's.

## 0. How to read this file

Columns, claim labels and the word collision on "absent" are defined in
`production/research/coverage-audit-kcd2/DELIVERY.md` section 0.

SOURCING LIMIT, unchanged and re-confirmed by the blocks hit in games 1 and 2:
every external citation below is the search channel's summary of a named page,
not a page read in full. Repository claims name their file and line and were
produced by a command run this session.

D24 still does not exist in this checkout; the brief's formulation is used as
the test. Quotations from repository files predating the formatting law have had
em-dashes replaced by commas and italics dropped.

## 1. Counts

**36 systems** enumerated, mapped against the 91 tiles.

| Column | Count |
|---|---|
| COVERED | 6 |
| PARTIAL | 8 |
| ABSENT | 20 |
| RULED OUT | 2 |
| **Total** | **36** |

Of the 20 absent: **5 IN, 14 OUT, 1 ASK.** Three of those five are riders on
recommendations already made in games 1 and 2 rather than new work.

THREE FURTHER INs SIT IN THE PARTIAL COLUMN and the arithmetic above does not
hide them: A3, D2 and D7 each have a tile whose scope covers part of the thing,
and in each case the uncovered part is worth building. So the count of distinct
new work recommended by this game is five, and those five are the summary's.

The OUT rate is back to where game 1 was, and the reason is structural. RDR2 is
a very large world doing a moderate amount per square mile. Its excellence is in
authored density and animation, which is the axis pillar 6 says to expand
conservatively and the axis the project has already named itself worse at.

## 2. The finding this game contributes

Games 1 and 2 each found a built system with no tile. This game found none, and
instead confirmed something the other two only suggested.

**THE SAME GAP APPEARS IN ALL THREE GAMES: what the player is wearing is an
identity, and the town remembers it.** KCD2 averages charisma over visible
garments and penalises dirt and blood. Hitman's whole design is that an outfit
is who you are. RDR2 is the most specific of the three: CITED (search summary of
Shacknews, "How the Wanted and Bounty systems work"), "if the townsfolk have
seen the player commit crimes in the current clothing previously, they may
recognize him regardless of his mask", and separately (search summary of
GameSpot, "NPCs Will Judge You For Being Too Dirty (Or Too Clean)") townsfolk
avoid a muddy player and shops may refuse service.

That is not three games having the same idea. It is three games discovering that
in a world where people look at you, clothing is the cheapest identity there is.
`Core/Perception.cs:158` already says so in our own rung-1 example text, "a man,
big, long coat", and nothing supplies it. Three independent confirmations is
what a cross-cutting finding looks like and it will carry to CROSS-CUTTING.md.

## 3. A correction to game 2

The Hitman delivery raised an ASK about whether the player should see, live, who
can see through them and how close they are to being noticed. That framing was
too wide, and this game's A1 is what showed it.

`Core/Observation.cs` has already ruled half of it, in the `Awareness` enum:
`NeitherKnows` is documented as "You have a witness and no idea. THE QUIET
HORROR CASE, and the design deliberately gives the player nothing here, no
ghost, no warning. The first you hear of it is a rumour three days later."

So the live WITNESS popup RDR2 puts on screen is not an open question here. It
is already decided against, in code, with a reason. The ASK that remains is
narrower and better: in the cases where Tom IS aware (`YouKnow` and `Standoff`
are two of the four states), and for knowledge Tom would legitimately hold about
who in the room knows him, how much is surfaced. Game 2's ASK should be read
with that correction attached.

## 4. The mapping

### A. Crime, witnesses and the law (9)

**A1. A WITNESS prompt appears on screen naming the crime that was seen.**
CITED (search summary of Shacknews). **ABSENT.** **OUT**, per section 3: our own
code has already decided against it and given the better reason.

**A2. An eye icon marks the witness, white if they cannot identify you, red if
they can.** CITED (search summary of Dexerto, "How to never get a bounty").
**ABSENT.** **OUT**, same reason. Worth recording that this is a two-rung
identification ladder with a readout, and ours has five rungs and no readout.

**A3. A witness must physically travel to a lawman before the crime becomes a
bounty, and can be chased, bribed, intimidated or killed on the way.** CITED
(search summaries of Shacknews and RDR2.org, "Wanted System").
**PARTIAL**, and the uncovered half is the recommendation.
WHAT IS COVERED: propagation to other PEOPLE. `Core/Homicide.cs:225 FileWith`
posts a killing into the `GossipMill` as an indelible rumour per witness, and
the mill carries it through schedule intersections, which is a better model of a
report spreading than RDR2's beeline to a sheriff.
WHAT IS NOT: propagation to THE LAW. `HomicideBook.Pressure` (line 321) computes
police pressure from `LiveWitnesses`, and a witness counts the moment they are
alive and hold the rumour at or above `TestimonyGrade`. There is no travel term,
no station, no arrival. Read the two together and the consequence is exact: the
police know the instant somebody believes it, so THE MINUTE BETWEEN THE ACT AND
THE REPORT IS NOT PLAYABLE.
**IN.** That minute is the most valuable minute in a crime game and it is the
one RDR2 gets right. It is also where three of the game's existing verbs would
suddenly have a place to happen: `Gossip.Bribe`, `Gossip.Intimidate`, and the
arithmetic `Core/Homicide.cs` already carries for what killing a witness buys
and costs. Against the D24 test it is perception, memory and consequence in the
same object, and the model to change is one term in one function.

**A4. A witness can be stopped by intimidation, bribery or violence.** CITED
(search summary of Shacknews). **COVERED**: tile "bribes and intimidation"
(partial), and `Core/Homicide.cs`'s own arithmetic for what killing a witness
does to the inquiry. Ours is the better-reasoned version; it just has nowhere to
be used until A3 exists.

**A5. A bandana or mask hides your identity from eyewitnesses.** CITED (search
summary of Shacknews). **PARTIAL**: Disguise v0 is built
(`Game/GameController.cs:189`) and no tile names it; see game 1, section 2.3.

**A6. Townsfolk who have seen you commit crimes in that clothing may recognise
you through a mask.** CITED (search summary of Shacknews).
**ABSENT.** **IN, and it is the sharpest statement of the cross-game finding.**
This is not "clothes affect your reputation", it is "the coat IS the identity
the town holds", which is exactly our rung 1. It also gives the disguise verb
its failure mode for free: a new coat works until the new coat is the one they
remember, and then you need another. That is remediation as behaviour, which is
canon's own word for what replaces a reset.

**A7. Lawmen recognise you through any disguise.** CITED (search summary of
Shacknews): "lawmen appear to have super powers in Red Dead Redemption 2, as
even if you are wearing a mask, they will immediately recognize you as Arthur
Morgan through any disguise."
**ABSENT.** **OUT, and it is the clearest negative example in three games.**
This is the psychic guard D11 names by that phrase, shipped in a game that cost
hundreds of millions, and the source reporting it is a guide written to help
players work around it. Whatever the identification rules are, they have to
apply to the police too, or the player learns that the system is decoration with
an exception where it matters most.

**A8. Bounties accumulate per county, so crimes in a new county open a separate
debt.** CITED (search summary of Shacknews).
**ABSENT.** **ASK**, and it is the third appearance of one question. KCD2 has
reputation per settlement and per social group; RDR2 has bounty per county;
LEDGER has per-NPC memory and a ruling (D11) against any global number. Meridian
has seven districts and three organisations. The question for Jafar is in game
1's summary and does not change here, except that a third game arriving at the
same structure is evidence that the structure is doing something, not that
everyone copied Rockstar.

**A9. A wanted level with a search area you can leave.** CITED (search summary
of GamesRadar). **PARTIAL**: "suspicion and heat" (partial) and "the
what-they-know HUD for wanted states" (typed absent), which D12 scoped down to
exactly this case.

### B. Standing and social interaction (4)

**B1. Honor: one global meter moved by almost every act.** CITED (search summary
of the Red Dead Fandom wiki, "Honor"). **RULED OUT** by D11: "Never a stored
global credibility number. There is no reputation: 47 anywhere."

**B2. Greet and antagonize, as verbs available on every NPC in the world.**
CITED (search summary of the Red Dead Fandom wiki, "Greeting"): Arthur can
target any passing NPC and choose from options including greet, antagonize and
rob.
**ABSENT.** **IN, and it is the cheapest thing in this audit.** Our tile "the
cast" (partial) records the real problem in one sentence: the town needs 30 to
50 residents at phase 2 and "the population generator supplies names, not
people, so most of the town is a body with a schedule". A body with a schedule
that you can nod at or needle is a person. Two verbs, no dialogue tree, no
authored lines beyond a bark bank that already exists, and every use is a
perceivable act that the person remembers, which is the moat working on the
smallest possible input. It is also the honest answer to how a town of fifty
feels inhabited without authoring fifty conversations.

**B3. Honor changes dialogue, prices, cutscenes and the ending.** CITED (same).
**RULED OUT** with B1.

**B4. NPCs comment on your appearance and smell, and shops may refuse
service.** CITED (search summary of GameSpot). **PARTIAL**, tile "doors and who
gets in" (exists), which already refuses on standing and clothes: "In the last
sim notoriety at 0.87 shut the laundry and left the repair yard open."

### C. Appearance and upkeep (5)

**C1. Bathing at a price, in tiers.** CITED (search summary of the Red Dead
Fandom wiki, "Bathing"). **ABSENT.** **IN as a rider** on the recommendation
already made in game 1 (A6 there), where `Traces.Wash` at 25 minutes already
exists. Nothing new is asked for here; the second sighting is the evidence.

**C2. Beard and hair grow over weeks and are styled at a mirror.** CITED (search
summary of RDR2.org, "Hygiene and Shaving").
**ABSENT.** **OUT as a growth simulation, IN as a discrete choice folded into
the appearance work.** Shaving or not shaving is a one-bit change to a rung-2
distinguishing mark and costs nothing. Modelling two weeks of growth to get
there is a simulation whose only output is that same one bit.

**C3. Clothing warmth against ambient temperature, with a health penalty for
the wrong choice.** CITED (search summary of the Red Dead Fandom wiki, "Weather
in Redemption 2"). **ABSENT.** **OUT.** One town, one climate, no mountains: the
system has nothing to be about. The part of it that survives is that being
soaked is VISIBLE, which rides on appearance rather than on a warmth meter.

**C4. Dirt and mud accumulate visibly on the character.** CITED (search summary
of GameSpot). **ABSENT.** **IN as a rider** on game 1's appearance
recommendation. Third sighting.

**C5. Health, stamina and dead-eye cores, fed by eating and sleeping.** CITED
(general). **ABSENT.** **OUT**, on the argument already made at KCD2's A7:
nobody in Meridian can perceive them.

### D. The living world (10)

**D1. NPCs run daily schedules with real times.** CITED (search summary of
RockstarINTEL, "A day in the life of a Red Dead Redemption 2 NPC"): one
documented NPC leaves his room at 8:00, works a livestock yard from 10:00 to
21:15, drinks, and turns in at 00:05. **COVERED**, tile "daily routines"
(exists).

**D2. Personal habits layered on top of the schedule: a stable worker who
smokes and plays the harmonica.** CITED (same).
**PARTIAL**, tile "ambient street life beyond the crowd" (typed absent), whose
scope is the street working (deliveries, sweeping, washing on a line) rather
than a habit belonging to a person.
**IN for the uncovered half, and it is not decoration.** A habit attached to a
person is what makes that person PREDICTABLE, and a predictable person is both
the thing that makes a town feel alive (Meridian Test condition 3) and the thing
a player plans around: the man who steps out for a smoke at the same time every
evening is a witness you can schedule around or a witness you can rely on. It
costs one field on a routine that already exists.

**D3. Ambient work: moving hay, building, shopkeeping.** CITED (search summary
of LaughingSquid). **COVERED**, tile "ambient street life beyond the crowd"
(typed absent), whose note already makes the argument.

**D4. Random encounters seeded across the map.** CITED (general).
**ABSENT.** **OUT.** A random encounter is what a large empty world uses instead
of a schedule. In one town the same beat is a person with a reason to be there,
which we already have, and a person with a reason is worth more than an
encounter because the player can meet them twice.

**D5. NPCs despawn when the player leaves and do not persist.** CITED (search
summaries of Steam community discussions on despawning, and Gamerant's piece on
a companion despawn): killed NPCs are replaced by others, and open-world event
participants despawn if the player goes 100 metres and returns.
**ABSENT.** **OUT, definitionally, and record it as a scoreboard entry.** The
brief asked what NPCs do when unobserved. In the most celebrated living world
ever built, the answer is: they stop existing. KCD2's answer (game 1, E3) is
that they carry on. Ours is already KCD2's: the headless sim ran seventeen days
and logged 346 looks and 508 sounds with nobody watching. This is the one axis
where the project is ahead of a 100-million-dollar world, and it should be said
out loud in those terms rather than assumed.

**D6. Corpses persist and decompose in place, and NPCs near towns clear them.**
CITED (search summary of Steam community discussion).
**ABSENT.** **IN as a rider** on the body-discovery recommendation made in game
2 (B2 there). Second sighting. The half RDR2 adds is that the WORLD tidies
itself: somebody removes a body near a town, which is another person who now
knows something.

**D7. Dynamic weather, including thunderstorms with dynamic lighting that can
strike near the player.** CITED (search summary of the Red Dead Fandom wiki,
"Weather in Redemption 2").
**PARTIAL**, tile "weather and wet streets" (partial), whose scope is rain
changing what people can see and hear and wetting 13755 surfaces.
**IN for the uncovered half: weather as an EVENT rather than a condition.** A
downpour that empties the street changes who could have seen you, which makes
rain a tactical resource rather than a look. The perception side is already
built and measured; what is missing is that the schedules bend to it. Cheap,
because both halves exist and neither currently talks to the other, and the
payoff is the most characteristic thing about the setting: pillar 5 is wet,
overcast Britain, and right now the weather is scenery.

**D8. Over 200 species of animal, birds and fish, with unscripted inter-species
behaviour.** CITED (search summary of RDR2.org, "Wildlife", and the Red Dead
Fandom wiki: 38 species and 178 subspecies).
**ABSENT.** **OUT as an ecosystem.** The three animals a British port town
actually needs, gulls, dogs and rats, are ambient dressing and belong under the
ambient street life tile at dressing cost, not as an AI system. A gull is worth
having because it is free atmosphere; a deer ecosystem is worth having in a game
about wilderness.

**D9. Hunting: tracking, wind direction, blood trails, pelt quality.** CITED
(search summary of the Red Dead Fandom wiki, "Hunting"). **ABSENT.** **OUT.**

**D10. Horses with bonding, care, saddlebags, and permanent death.** CITED
(general). **ABSENT.** **OUT.** The nearest tile is "traffic and vehicles"
(exists) and D4 already sequences driving behind combat.

### E. Surfaces and structure (8)

**E1. Camp: chores, donations, morale, companion activities.** CITED (general).
**PARTIAL**: "factions and the empire" (exists) plus `Core/Companionship.cs`.
Mickey's is the premise's camp and the structure is already there.

**E2. Shops with real inventories, printed catalogues, and mail order.** CITED
(general). **PARTIAL**, tile "economy and trading" (partial), whose note records
that no prices, no trade surface and no shop exist in the scripts walked.

**E3. Newspapers.** CITED (general). **COVERED** by two tiles, both typed
absent: "letters and newspapers the player can read" and "the local paper and
the news reacting to you", the second of which the inventory correctly calls
"Meridian Test condition 2 arriving through a channel that is not a person's
mouth".

**E4. Letters and mail.** CITED (general). **COVERED**, same tile, and canon
makes paper the information channel.

**E5. Trains, stagecoaches and fast travel.** CITED (general). **ABSENT.**
**OUT.** One town.

**E6. Fishing.** CITED (general). **ABSENT.** **OUT.**

**E7. Cinematic camera and auto-ride along roads.** CITED (general).
**ABSENT.** **OUT.** It exists to make a twenty-minute ride bearable. Nothing in
Meridian is twenty minutes away, and if it were, that would be the bug.

**E8. Photo mode.** CITED (general). **COVERED**, tile "photo mode" (typed
absent).

## 5. What could not be established

1. **No primary Rockstar source was reachable.** Everything here is community
   documentation relayed through the search channel. For a game this large that
   is a real limit: RDR2's systems are undocumented by its developer and
   described by players, so a claim like "lawmen see through any disguise" is a
   player's reliable observation rather than a specification. I have labelled
   them CITED because the observation is what matters for an audit, but they are
   not specifications.
2. **Whether A3's report-travel is modelled anywhere other than in the bounty
   path.** I established RDR2 has it and that LEDGER's `Pressure` has no travel
   term. I did NOT establish that no other LEDGER file inserts a delay between a
   sighting and the law's stage; I read `Homicide.cs` and `Informing.cs` and
   traced `Pressure` and `LiveWitnesses`, and that is the extent of the check.
   A reach-auditor pass would settle it and this file does not claim to have
   done one.
3. **Honor's exact inputs and weights** are not established; the sources
   describe behaviour and farming strategies.
4. **Not enumerated.** The story missions and their structure, Dead Eye, the
   combat and gunplay, the duel system, Red Dead Online entirely, the
   accessibility options, and the animation system, which is the thing RDR2 is
   most admired for and which the project has already named on its "worse at,
   and at peace with it" list. Queue topic 8 covers animation and this audit
   deliberately left it alone.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Shacknews, "How the Wanted and Bounty systems work in Red Dead Redemption 2", https://www.shacknews.com/article/108138/how-the-wanted-and-bounty-systems-work-in-red-dead-redemption-2
- RDR2.org, "Wanted System", https://www.rdr2.org/wiki/wanted-system/
- RDR2.org, "Bounty System", https://www.rdr2.org/wiki/bounty-system/
- RDR2.org, "Wildlife", https://www.rdr2.org/wiki/wildlife/
- RDR2.org, "Hygiene and Shaving", https://www.rdr2.org/guides/shaving-hygiene-guide/
- Red Dead Fandom wiki, "Eyewitness", https://reddead.fandom.com/wiki/Eyewitness
- Red Dead Fandom wiki, "Law Enforcement in Red Dead Redemption 2", https://reddead.fandom.com/wiki/Law_Enforcement_in_Red_Dead_Redemption_2
- Red Dead Fandom wiki, "Honor", https://reddead.fandom.com/wiki/Honor
- Red Dead Fandom wiki, "Greeting", https://reddead.fandom.com/wiki/Greeting
- Red Dead Fandom wiki, "Bathing", https://reddead.fandom.com/wiki/Bathing
- Red Dead Fandom wiki, "Weather in Redemption 2", https://reddead.fandom.com/wiki/Weather_in_Redemption_2
- Red Dead Fandom wiki, "Hunting", https://reddead.fandom.com/wiki/Hunting
- Red Dead Fandom wiki, "Animals/Redemption 2 species", https://reddead.fandom.com/wiki/Animals/Redemption_2_species
- GamesRadar, "Bounty and Wanted Level: How they work, and how to escape from the Law", https://www.gamesradar.com/red-dead-redemption-2-bounty-and-wanted-level/
- Dexerto, "How to never get a bounty in Red Dead Redemption 2", https://www.dexerto.com/red-dead-redemption/how-to-never-get-a-bounty-in-red-dead-redemption-2-wanted-system-explained-218399/
- Dexerto, "What happens when you follow a Red Dead Redemption 2 NPC for an entire day?", https://www.dexerto.com/red-dead-redemption/what-happens-when-you-follow-a-red-dead-redemption-2-npc-for-an-entire-day-215958/
- RockstarINTEL, "A day in the life of a Red Dead Redemption 2 NPC", https://rockstarintel.com/a-day-in-the-life-of-a-red-dead-redemption-2-npc/
- LaughingSquid, "Non-Player Characters Hard at Work Earning a Living in Red Dead Redemption 2", https://laughingsquid.com/non-player-characters-working-dead-redemption-2/
- GameSpot, "Red Dead Redemption 2 NPCs Will Judge You For Being Too Dirty (Or Too Clean)", https://www.gamespot.com/articles/red-dead-redemption-2-npcs-will-judge-you-for-bein/1100-6462202/
- GameWith, "Hygiene and Appearance Guide", https://gamewith.net/red-dead-redemption2/article/show/1165
- Gamerant, "Red Dead Redemption 2 Clip Shows That Even NPC Despawns Can Look Cool", https://gamerant.com/red-dead-redemption-2-npc-charles-despawn-video/
- Steam community, despawning discussions, https://steamcommunity.com/app/1174180/discussions/0/4347743556799309580/
- Rockstar Games, "Wildlife" feature page, https://www.rockstargames.com/reddeadredemption2/features/wildlife

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`, `canon.md`,
`ledger-v2/respec/decision-register/D11-player-progression.md` and
`D12-information-surfaces.md`, `ledger/Assets/Scripts/Core/Homicide.cs`,
`Core/Informing.cs`, `Core/Observation.cs`, `Core/Perception.cs`,
`Game/GameController.cs`.
