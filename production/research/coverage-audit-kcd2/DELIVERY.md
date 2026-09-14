# Coverage audit 1 of 5: Kingdom Come Deliverance 2

STATUS: SPEC (research delivery). Branch `research/coverage-audit-kcd2`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. It is a mapping and a set of
recommendations. If Jafar rules something IN, the studio turns that into tiles
and queue items then, not before. No tile is proposed here, no queue item is
filed here, and the inventory is not touched.

## 0. How to read this file

### 0.1 The four columns, and a word that collides

Every KCD2 system below is mapped against `production/systems-inventory.json`
(91 tiles, read at commit `074f85b`) into one of four columns:

- **COVERED**: a tile exists whose scope includes this thing.
- **PARTIAL**: a tile exists but its scope covers only part of it, and the
  uncovered part is named.
- **ABSENT**: no tile covers it. This is the blind spot the audit exists to find.
- **RULED OUT**: a decision record excludes it, and the record is named.

THE WORD COLLISION, because it will mislead a fast reader. The inventory's own
`status` field also uses the word absent, and it means something different: a
tile typed `absent` means the studio has SEEN the thing and has not built it.
That is coverage, not a blind spot. So "COVERED, tile typed absent" appears
below and is not a contradiction: it means the map has the territory marked and
empty, which is the map working. Only the ABSENT column is a finding.

### 0.2 Labels on every claim

Following the standard set by `production/art/atlas-02/research/`:

- **CITED**: the claim and its source.
- **DERIVED**: computed or inferred here from cited inputs, with the reasoning
  printed so a later reader can refute it.
- **ASSUMED**: a choice with no source. Nothing downstream should treat it as
  researched.
- **HOLE**: something looked for and not found, stated so it can be a research
  task rather than a smoothed-over invention.

### 0.3 The sourcing limit, stated once and true of every citation below

In this checkout outbound HTTPS to research hosts is refused by the
organization egress proxy. Measured this session, not remembered:
`en.wikipedia.org`, `kingdomcomedeliverance-archive.fandom.com` and
`www.gamepressure.com` were each fetched and each answered
`EGRESS_BLOCKED`. WebSearch works and returns the search channel's summary of
a page together with the page title and URL.

So every external citation below is THE SEARCH CHANNEL'S SUMMARY of a page,
with the page recorded, and NOT a page this session read in full. Two
consequences a reader must hold. A figure could be the summariser's error. And
where a primary source was needed and could not be retrieved, the failure is
recorded as a HOLE rather than filled from memory.

Claims about THIS REPOSITORY carry no such limit: every one was produced by a
command run this session, and the file and line are given.

ONE NOTE ON QUOTATIONS FROM REPOSITORY FILES, made once here rather than at
each site. Several of the files quoted below were written before the formatting
law of 31 August and contain em-dashes and italics. Quotations of them here have
had em-dashes replaced by commas and italics dropped, so that this file complies
with the law. The words are otherwise unchanged, and the file and symbol are
given every time so the original can be read.

### 0.4 D24 does not exist in this checkout

The brief asks that every recommendation be argued against D24, "which says
LEDGER is a small dense town where what people know about you is the mechanic,
and that anything not feeding perception, memory, gossip or consequence gets
the smallest budget that keeps it from looking wrong."

MEASURED THIS SESSION: there is no D24. The D-numbered spine in
`ledger-v2/respec/decision-register/rulings-log.md` runs D1 to D18 and stops.
A grep for `D24` across `ledger-v2/`, `production/`, `game-design/` and
`canon.md` returns zero hits, and a grep for the phrases "smallest budget",
"small dense town" and "what people know about you is the mechanic" across
every markdown file in the repository returns zero hits.

This is recorded as a HOLE and not filled. The principle is used below exactly
as the brief states it, cited as "the D24 test as given in the brief", because
the brief is the instruction that governs this work. If the record exists
outside this checkout it should be pointed at; if it has not been written, then
a principle this audit's seventy-one verdicts lean on is currently unwritten,
which is worth knowing on its own.

## 1. What was enumerated, and the denominator

**71 systems** enumerated from Kingdom Come Deliverance 2, in seven groups.
Mapped against 91 tiles. The distribution:

| Column | Count |
|---|---|
| COVERED | 18 |
| PARTIAL | 11 |
| ABSENT | 35 |
| RULED OUT | 7 |
| **Total** | **71** |

Of the 35 in the ABSENT column: **9 recommended IN**, **21 recommended OUT**,
**5 recommended ASK**. The ratio is the point. An audit that recommended most
things IN would have told us nothing.

A SIXTH ASK SITS OUTSIDE THAT 35, and the arithmetic above does not hide it:
the scarcity of saving (F1 to F3) is absent while the save surface is covered,
so it is counted in the COVERED column and argued as an ASK. Nine of the INs
are also not nine pieces of work: A6, A14 and F11 are recommended as riders on
other entries rather than as systems of their own, and E4 folds into E5, which
leaves five distinct things to build. Those five are what the summary carries.

WHAT THE 71 IS A COUNT OF, since a number without that is not a measurement:
distinct player-facing or world-facing systems I could establish KCD2 contains
from the sources in section 7. It is not a count of everything KCD2 contains.
It is bounded by what one session's search channel surfaced, and section 8
names what I know is missing from it.

## 2. The finding that changes how the inventory should be read

This is the most important result in this delivery and it is not in the
columns, because the brief's method cannot express it.

**Four systems the brief listed as known gaps are already built in this
repository, and no tile in the inventory names any of them.** The blind spot
runs in both directions: the inventory misses things that EXIST as well as
things that are missing.

Measured this session, every path checked by reading the file:

**2.1 Blood on the player, as a thing people can see.**
`ledger/Assets/Scripts/Core/Traces.cs` declares a `Stain` class with an age, a
strength, whose blood it is, and whether it is your own. `Traces.Noticeable`
resolves it against metres and light level through the same
`Perception.LightFactor` the rest of the perception model uses, so a stain that
would ruin you in the bar is invisible on the walk home. `Traces.Age` dulls it
to a floor of 0.45 over roughly half a day and then it stays, which the file
states is deliberate: "dealing with it has to be a decision you make, not a
timer you wait out". `Traces.CountsAsMark` feeds it into the identification
ladder as rung-2 evidence, a distinguishing mark, "exactly like the limp".
`Traces.SocialCost` scales the cost by familiarity, so blood noticed by a
stranger is a rumour and blood noticed by someone close to you is a scene.
`Traces.Wash` costs 25 minutes and requires water and privacy.

AND IT IS REACHED, which is the half that usually fails here.
`Game/ViolenceHost.cs:294` sets the stain when the weapon marks you and counts
`StainsTaken`; `Game/NpcWalker.cs:904` reads `bloodOnMe` from
`ViolenceHost.StainNoticeableAt`, so a walker in the crowd notices;
`Game/SimDirector.cs:1670` ages it every tick and `:7302` runs the wash, with
one path that fails in public and one that works at home.

**2.2 Objects with a history that can be traced back to you.**
`Core/Traces.cs` also declares `Traces.Item` (an instance id, a weapon id, an
`Origin`, who it came from, a `History` list that is never cleared, whether it
was disposed of, where, and whether the disposal was witnessed) and
`Traces.Origin` with five routes: Bought, Stolen, Taken, Inherited, Ordinary.
The file's own reasoning: "a pistol in a bin is a video game, a pistol you can
name the seller of is this game". `Game/EvidenceHost.cs` wraps it with
`Traceability`, `ResidualRisk` and `StrongestThread`, and `Game/SimDirector.cs`
drives five instances through it at lines 6849 to 6874.

**2.3 Disguise.** `Game/GameController.cs:189` carries "Disguise v0
(design-doc 6.4 cover): the runner's coat". `Core/Gossip.cs:259` passes a
disguised sighting through at less than 1.0 confidence.
`Game/GossipDirector.cs:678` holds the sharpest line in the system: "The
disguise buys doubt about the face; it buys none about the car".
`Game/SimDirector.cs:13797` computes `disguiseWorks` and `:15311` emits it as a
named gate in the sim verdict.

**2.4 The coat as a concealment constraint rather than a bag.**
`Core/Coat.cs` states it plainly: "NOT AN INVENTORY. There is no grid, no
weight and no bag: the constraint is concealment, and the whole decision is
what did I bring, made at the door, before you know what the night holds".

**WHAT THE INVENTORY SAYS ABOUT ALL OF THAT.** Token counts run this session
over the whole 70,491-byte inventory file: `Traces` 0, `Stain` 0, `blood` 0,
`stolen` 0, `disguise` 0, `appearance` 0, `clothing` 0, `wearing` 0, `fence` 0.
The single hit for `clothes` is inside the note on "doors and who gets in" ("a
door asks for an introduction, standing, a payment or the right clothes"); the
single hit for `dirt` is "dirty cash" under economy and trading; the single hit
for `washing` is "washing on a line" under ambient street life. All three are
false friends. `EvidenceHost.cs` appears exactly once in the whole file, in the
evidence list of the tile "crime jobs and takings", which is a tile about
planning a job and banking the takings.

DERIVED, and this is the recommendation that follows: the inventory is not
wrong about what exists, it is INCOMPLETE ABOUT WHAT IT HAS NAMED. A system
with no tile cannot be typed, cannot be ruled on, cannot be argued about and
cannot be found by the next session. Three of the brief's ten known-already
gaps were reported as gaps because the map has no square for them, not because
the work is missing. Whether that warrants new tiles is Jafar's call and is one
of the ASKs in the summary.

HOLE, and it bounds the claim above. I established that these systems exist and
are called. I did NOT establish that any of them has ever run in a build a
person played, or that any gate measures them. `StainsNoticed` and
`WorstStainCost` are counters on `ViolenceHost` and I did not find a verdict key
that emits them. Built is not running, and this section claims built.

## 3. The mapping

Format: `ID. The KCD2 system` then COLUMN, tile or record, and the verdict.
Entries in the ABSENT column carry the argument. Entries in the other three
carry one line, because the argument for them is that the studio has already
had this thought.

### A. Character state, upkeep and progression (15)

**A1. Four main stats: Strength, Agility, Vitality, Speech.** CITED (search
summary of Fextralife, "Skills", and Method.gg, "Best Perks"): stats rise by
doing activities related to them.
**RULED OUT** by D11: "The player character has no improvable stats or skills.
Nothing about the player gets numerically better at anything."

**A2. Around twenty skills, each rising by use.** CITED (same): Alchemy,
Craftsmanship, Drinking, Horsemanship, Houndmaster, Scholarship, Stealth,
Survival, Thievery, Warfare, Swords, Heavy Weapons, Polearms, Unarmed,
Marksmanship and more. **RULED OUT** by D11.

**A3. 275 perks, unlocked every two levels.** CITED (search summary of
Fextralife, "Perks"). **RULED OUT** by D11.

THE ARGUMENT IS D11'S OWN AND IT IS WORTH QUOTING HERE, because A1 to A3 are
KCD2's entire progression spine and deleting them is the largest single
divergence in this audit: "if the player improves, the interesting question
becomes what have I unlocked. If only the world's model of the player improves,
the interesting question stays what do they think of me, and who told them,
which is the game."

**A4. Charisma computed from visible worn equipment, averaged over visible
layers only.** CITED (search summary of Sportskeeda, "Charisma in Kingdom Come
Deliverance 2, explained"): "Your total charisma is the average of the charisma
value of the individual pieces of your clothing or armor that are visible.
Layers hidden under others don't count."
**ABSENT** from the inventory (no tile names appearance or clothing; see 2.4).
**IN, reduced.** The identification ladder's own rung-1 example text in
`Core/Perception.cs:158` is "a man, big, long coat", so clothing is already the
thing the design says a witness reports at the bottom rung, and nothing supplies
it. Against the D24 test this is not a cosmetic system: it is a perception
input, and it is the cheapest one we do not have. What it buys is the whole
remediation route canon already promises ("remediation is behavioral: leave,
change appearance, rebuild relationships") becoming something the player can
actually do.

**A5. Clothing condition: damage, dirt and blood all lower charisma, and being
dirty applies a Speech penalty on top.** CITED (search summary of Sportskeeda
and Gamer Guides, "Washing Clothes and Armor"): "damaged, stained, or bloodied
clothing has a lower charisma value"; "even if your Speech is high, being dirty
will give you a Speech and charisma debuff".
**ABSENT** from the inventory. **IN.** The blood half of this is already built
and reached (section 2.1), so the work is the general case rather than the
system. What it buys: one violent minute costs three in-game days, which is
`Core/Traces.cs`'s own stated purpose, and it does it through perception rather
than through a timer.

**A6. Washing and laundering at troughs, tailors and bathhouses, at different
depths of clean.** CITED (search summaries of Deltia's Gaming, "How to Launder
Clothes", and Fextralife, "Baths").
**ABSENT** from the inventory. **IN as a rider on A5, not as its own thing.**
`Traces.Wash` already exists at 25 minutes with water and privacy required, and
`SimDirector.cs:7302` already distinguishes failing in public from working at
home. The KCD2 finding worth taking is the LADDER (a trough is not a bathhouse),
because a cheap partial clean that leaves a describable mark is more interesting
than a binary.

**A7. Nourishment (hunger) with graded penalties below 50, affecting stamina,
combat and dialogue checks.** CITED (search summaries of Gamerant, "Energy and
Nourishment Consequences", and Gamepressure).
**ABSENT.** **OUT.** It feeds none of perception, memory, gossip or consequence:
nobody in Meridian will ever know or care that Tom has not eaten. Under the D24
test that is the definition of the smallest budget, and the smallest budget for
hunger is zero. KCD2 can afford it because its fantasy is being a person in 1403;
ours is being a person the town is forming an opinion about.

**A8. Energy (sleep debt) with graded penalties below 50.** CITED (same).
**ABSENT**, and adjacent to the tile "sleep and the day boundary" (typed absent),
which covers crossing a day but not a meter. **OUT for the meter, IN for the day
boundary** (see F4). A meter that punishes you for being awake is a different
design from a day that has to be crossed.

**A9. Food spoils in inventory, and drying extends it.** CITED (search summary
of Gamepressure). **ABSENT.** **OUT.** Same argument as A7, one rung smaller.

**A10. Wounds located on body parts, bleeding as a status, bandages applied
from the inventory, injured legs stop you running.** CITED (search summaries of
TheGamer, "How To Recover Health", and Gamerant, "How to Heal").
**COVERED**, tile "injury and healing" (typed partial): `Core/Harm.cs` declares
an `InjuryKind` enum and an `Injury` class.

**A11. Illness from rotten food, dirty wounds and poor hygiene.** CITED (search
summary of Sevenswords, "Survival Guide"). **ABSENT.** **OUT.** A fever is not a
social fact. The one thread worth keeping is that a visible injury is a
distinguishing mark, and the ladder already has a slot for that.

**A12. Potions and decoctions as timed buffs and healing.** CITED (search
summary of Gamerant). **ABSENT.** **OUT.** Consumable buffs are the progression
system D11 deleted, wearing a different hat.

**A13. Carry weight, encumbrance, and an overload state that stops you
sprinting, jumping, fast-travelling and eventually mounting.** CITED (search
summaries of GameSpot, "How To Increase Carry Weight And Manage Encumbrance",
and Deltia's Gaming, "Weight Guide"): base 70, plus 5 per Strength point.
**PARTIAL**, tile "inventory" (typed partial). The tile's scope is the Coat,
which is a concealment constraint, not a weight one.
**OUT for weight.** `Core/Coat.cs` already made this decision and made it
better: "A player who can carry everything has not decided anything", with the
decision made at the door rather than in a menu. Weight would turn one sharp
decision into continuous arithmetic, and the arithmetic is invisible to
everybody in Meridian. The half of KCD2's encumbrance that IS moat work is
whether what you are carrying is VISIBLE, which is B11, not how heavy it is.

**A14. Item durability, repair kits and sharpening.** CITED (search summary of
Gamer Guides and TheGamer). **ABSENT.** **OUT as a number, IN as a rider on
A5.** A torn and bloodied coat is a describable mark; a coat at 62 percent
condition is a number nobody can see. Take the appearance, leave the durability.

**A15. Drinking as a skill, with alcohol as a mechanic and its own perk
tree.** CITED (search summary of Fextralife, "Perks": Drinking Perks is a named
category). **RULED OUT** by D18, recorded in `canon.md`: "Alcohol and gambling
are out ENTIRELY: never shown, served, drunk or spoken of, in image or speech."

### B. Crime, law and evidence (17)

**B1. Crimes recorded per location, with a viewable list of your known felonies
when arrested.** CITED (search summary of Escorenews, "How to see list of your
crimes when arrested"). **COVERED**: "the law and the police" (partial),
"permanent memory" (partial).

**B2. Witnesses remember, and guards are still looking for you when you come
back.** CITED (search summary of Gamerant, "KCD2's Crime System Explained"):
"Witnesses will remember you and if you return to the scene of the crime,
there's a strong chance the guards will still be on the lookout for you".
**COVERED**: "witnesses and what they caught" (exists), "recognition and
confrontation" (partial). This is the thing LEDGER is built to beat.

**B3. A crime with no surviving witness may not be recorded at all.** CITED
(same): "Some crimes might not be included if there were no witnesses (or none
survived)." **COVERED**, and LEDGER's version is finer: `Core/Observation.cs`
fills seven slots independently rather than answering "did he see it", and the
file says why: "Every crime game asks did he see it, which is why witnesses feel
fake everywhere."

**B4. Talking your way out with a guard, using Speech, Charisma or Strength,
and it works better on lower-ranking guards.** CITED (search summary of
Gamerant, "Crime and Punishment"). **PARTIAL**, tile "bribes and intimidation"
(partial): `Core/Gossip.cs:706 Bribe` and `:738 Intimidate` both return a
`DcResult` and `Game/DialogueUI.cs:2214` calls one. The uncovered part is what
the check READS, which is C1 to C3.

**B5. A graded punishment ladder: fine, jail, the stocks, caning, branding,
execution, scaled by severity and by repetition.** CITED (search summaries of
The Escapist and Gamerant, "crime-punishment-branding-executions").
**COVERED**, tile "court and the cells" (typed absent), whose own note makes the
argument: "an arrest that leads nowhere is a consequence that stops." The SHAPE
of the ladder for 1988 to 1992 Britain is queue topic 6 and is not this file's
to decide.

**B6. Accepting your punishment deletes all your known felonies in that
location.** CITED (search summary of The Escapist): "Once you accept your
punishment, all your known felonies in the location will be deleted."
**ABSENT.** **OUT, and this one is a trap worth naming.** It is a reset, and
canon's moat clause forbids resets in the same breath it defines the pillar:
"Permanent per-NPC memory. Nothing is ever wiped; remediation is behavioral."
KCD2 needs the wipe because its reputation is a number that would otherwise
only fall. We do not need it because our record is per person, and a person who
saw you go to the cells has a MORE specific memory afterwards, not a blank one.
Taking B6 would delete the pillar to solve a problem we do not have.

**B7. Repeat offences escalate the punishment.** CITED (same). **PARTIAL**,
tile "suspicion and heat" (partial), which is the mechanism escalation would
read. No separate recommendation.

**B8. Stolen items carry a visible stolen tag that everyone can read, decaying
in one to two in-game weeks.** CITED (search summaries of the Kingdom Come
Deliverance Fandom wiki, "Stolen goods", and Deltia's Gaming, "How to Sell
Stolen Items"). **ABSENT** from the inventory, and see 2.2: `Traces.Origin.Stolen`
exists in the code with no tile naming it.
**IN.** This is the moat in object form and it needs no new pillar: an object
with a provenance is a memory that can be carried, dropped, sold or found, and
`Traces.Item.History` is already "never cleared". What it buys is that the
player's own possessions become perceivable acts, which is exactly what D12 asks
of every information verb.

**B9. Fences: merchants who take stolen goods, with limited funds that refresh
over time.** CITED (search summary of Deltia's Gaming and Gameranx).
**PARTIAL**: "crime jobs and takings" (exists, and the takings launder) and
"economy and trading" (partial, and the tile says trading is not wired:
`Core/Negotiation.cs` is reached only from `Core/Empire.cs`). The fence is a
person with a schedule and a memory, which the town already knows how to make.

**B10. Geographic laundering: sell the thing in another town and nobody
knows.** CITED (search summary of the Fandom wiki, "Stolen goods").
**ABSENT.** **OUT, and the reason is the premise.** Meridian is one town.
Pillar 6 is "small and dense"; there is no far away. That is not a limitation to
work around, it is the design: the reason a stolen thing is dangerous here is
precisely that everywhere you could take it is somewhere people know you. KCD2's
answer would dissolve our best pressure.

**B11. Wearing or equipping stolen goods gives you away, because everyone can
tell.** CITED (search summary of Deltia's Gaming): "Do not equip stolen items
until the tag has been removed, because everyone can tell."
**ABSENT.** **IN, and it is the same predicate as blood.**
`ViolenceHost.StainNoticeableAt(metres, lightLevel)` already exists; a
dead man's watch on your wrist is another thing noticed at conversational
distance under a light and not across a dark street. One rule, two payloads.
Against the D24 test it feeds perception, memory and consequence at once, for
the cost of a second caller.

**B12. Bribing officials.** CITED (search summary of Gamerant, "Crime System
Explained"). **COVERED**, tile "bribes and intimidation" (partial). The tile's
own note names the missing half correctly: "nothing measured here says the town
REMEMBERS having been bought".

**B13. Changing your clothes so people do not recognise you.** CITED (same):
"people may still recognize you unless you change your clothes or bribe
officials." **ABSENT** from the inventory, and see 2.3: Disguise v0 is built.
**IN, to finish rather than to start.** The existing implementation is a single
coat with a confidence multiplier; what A4 and A5 would give it is a general
rule, so that the thing you changed and the thing they remembered are the same
kind of fact. `GossipDirector.cs:678` already knows the interesting half ("the
disguise buys doubt about the face; it buys none about the car"), which is a
better idea than KCD2's and deserves the system underneath it.

**B14. Trespass as its own crime, including sleeping in a bed that is not
yours.** CITED (search summaries of TheGamer, "Where To Find Beds", and The
Escapist). **PARTIAL**, tile "doors and who gets in" (exists). The uncovered
part is being inside once the door is open, which waits on interiors (tile
"interiors you can enter", typed absent).

**B15. Lockpicking as a skill-gated minigame.** CITED (search summary of
TheGamer, "Every Minigame Ranked"). **COVERED**, tile "burglary and
lockpicking" (typed absent), named a phase 2 petty-crime verb.

**B16. Pickpocketing as a skill-gated minigame.** CITED (same). **COVERED**,
tile "pickpocketing" (typed absent).

**B17. A night curfew, and a law requiring you to carry a torch after dark.**
CITED (search summary of PC Gamer, "How to use a torch"): "it's illegal not to
carry a torch at nighttime in KCD2". HOLE: I could not retrieve the primary
source for the exact rule.
**ABSENT.** **OUT.** There is no curfew in a British town in 1990, so the rule
does not transfer. The PRINCIPLE does transfer and we already have it: being
somewhere at an hour nobody has a reason to be there is itself perceivable, and
that is `Core/Perception.cs` plus the daily routines tile, with no new law
needed.

### C. Dialogue, persuasion and coercion (5)

**C1. Six resolved check types in two families.** CITED (search summaries of
Gamerant, "How to Pass Speech Checks", and Fextralife, "Persuasion System"):
positive are Persuasion, Impression and Presence; negative are Coercion,
Domination and Intimidation. **PARTIAL**, tile "bribes and intimidation": the
verbs exist, the resolved system does not.

**C2. Checks are binary pass or fail, not a percentage roll.** CITED (search
summary of Escorenews and ScalaCube): "you either pass or fail. Your skill
and/or dialogue stat levels must meet or exceed that of the Speech check."
**PARTIAL**, same tile. `DcResult` is the type that would carry this.

**C3. Each of the six reads a different pair, and the pairs are deliberate.**
CITED (search summary of Gamerant): Persuasion and Coercion read Speech above
Charisma; Impression and Domination read Charisma above Speech; Presence and
Intimidation read gear quality against the physical stats.
**PARTIAL.** **IN for the resolution model, and it must be re-based.** LEDGER
cannot copy this: D11 forbids the Speech and Charisma stats it reads. What
LEDGER has instead is better and is already sitting there unused: this NPC's own
memory of you (promises kept, lies caught, alibis that checked out, per D11),
what you visibly are right now (A4, A5, B11), and who else is within earshot.
That makes the same lie cost different amounts to different people, which is
D11's stated reason for the whole shape, and it makes D12's legibility clause
answerable: the reason the check failed is a thing that actually happened.
What it buys: the single most-used verb in a social RPG stops being a dice roll.

**C4. Reputation with the person you are talking to modifies the check.**
CITED (search summary of Fextralife, "Persuasion System").
**ABSENT** as stated, because LEDGER has no reputation. **ASK**, folded into D1
and D2 below: this is the same question asked from the dialogue end.

**C5. Some dialogue choices run on a timer.** CITED (search summary of
Escorenews): "some dialogues may have a timer".
**ABSENT.** **OUT for now, and it is not a free OUT.** A timer on a written
menu is a pressure device; a timer on a LIVE SPOKEN conversation is a different
object entirely, and whether silence is a move the player can make is a real
question that belongs to queue topic 1 (live speech) and not to this audit.
Flagged there rather than decided here.

### D. Reputation (3)

**D1. Reputation tracked separately in every settlement.** CITED (search
summary of HowToPlayHub, "KCD2 Reputation Guide"): "KCD2 tracks Henry's standing
separately in every settlement he visits".
**ABSENT.** **ASK.** See the argument at D3.

**D2. Reputation broken down by social group within a settlement.** CITED
(same). **ABSENT.** **ASK.**

**D3. Reputation gates merchant prices, dialogue checks, quest availability and
guard suspicion.** CITED (same). **PARTIAL**, tile "doors and who gets in"
(exists), which already does this with standing: "In the last sim notoriety at
0.87 shut the laundry and left the repair yard open."

THE ARGUMENT, and it is why these are ASK rather than OUT. D11 forbids a global
credibility number in the strongest terms available: "Never a stored global
credibility number. There is no reputation: 47 anywhere", and it gives the
reason, which is that a global number "makes lying a resource-management problem
against one meter, readable at a glance, identical everywhere". That reasoning
is about a GLOBAL number. It does not obviously rule on whether the Hook can
have a different opinion of you from the Exchange, or whether the dockers can
have a different one from the police, and canon names seven districts and three
rival organisations, which is a lot of structure for a system that only ever
tracks individuals. There is a real design difference between a stored per-group
number (which D11's argument catches) and a per-group READOUT computed from the
individual memories that already exist (which it arguably does not, and which
would cost little because the memories are there). Which of those he wants, or
neither, is a judgement about what the game is, so it goes to him. This is the
single biggest question KCD2 raises for us.

### E. World and simulation (7)

**E1. NPCs run 24-hour schedules: eat with others, go to work, shop, spend the
evening out, sleep in their own beds.** CITED (search summary of Wccftech, "Dev
Talks About Dynamic NPC Routines"). **COVERED**, tile "daily routines" (exists),
whose note states the reason correctly: "a witness has to have a reason to be
there."

**E2. Around 2400 NPCs, with roughly half concentrated in one city.** CITED
(search summary of the GDC session listing, "Supporting Thousands of NPCs in
Kingdom Come: Deliverance and Kingdom Come: Deliverance II").
**PARTIAL**, tile "the cast" (partial), which names 30 to 50 residents at phase
2. Density is a content question, not a systems gap, and pillar 6 already
decided we go dense rather than large.

**E3. The simulation continues while the player is elsewhere.** CITED (same
source): "All NPCs are doing their daily routines and reacting to player actions
even when the player is long gone." **COVERED**: the headless sim is the
project's own instrument and area 2 of the inventory is defined by this question.

**E4. NPCs interrupt their routine for something they see, such as a street
brawl or meeting a friend.** CITED (search summary of Wccftech).
**ABSENT** as a behaviour. **IN, folded into E5.**

**E5. The region's behaviour changes after crime: NPCs stay home instead of
going out, carry a weapon, or call for more patrols.** CITED (search summary of
Wccftech): "They will alter their routine if there was violence or theft in the
region recently."
**ABSENT.** **IN, and it may be the highest-leverage item in this audit.**
Meridian Test condition 3 is that a player describes the town as alive WITHOUT
BEING PROMPTED, and condition 2 is that the world visibly knows them once in
thirty minutes. A changed routine satisfies both without a single line of
dialogue, which matters because the inventory's own note on "recognition and
confrontation" records that in the shipped build "every recognition beat
measured sat below the rung at which anybody comments, 1944 of 1944, so nobody
says a word to you". A town that goes quiet after what you did is a consequence
that does not depend on anybody finding the words. And the inputs already exist:
`Core/Suspicion.cs`, the heat model, and the daily routines that would bend.

**E6. Weather and a day and night cycle.** CITED (general). **COVERED**: tiles
"weather and wet streets" (partial) and "light and the time of day" (exists).

**E7. Horses, with their own inventory and carry capacity, and a saddle that
raises it.** CITED (search summary of GameSpot, "How To Equip Horse Items").
**ABSENT.** **OUT.** No analogue. The nearest tile is "traffic and vehicles"
(exists) and driving is already scheduled at phase 5 behind phases 3 and 4.

### F. Player-facing surfaces (16)

**F1. Manual saving gated on a consumable (Saviour Schnapps), owned beds and
quest checkpoints.** CITED (search summaries of TheGamer, "Saviour Schnapps Is
Still Needed", and Game-scout).
**COVERED** as a surface, tile "save and load" (exists), but the SCARCITY is
**ABSENT**. **ASK.** See the argument at F3.

**F2. A save-and-exit option, added after launch backlash on the first game and
present from the start in the second.** CITED (same). **COVERED**.

**F3. Autosaves after dialogue and fights.** CITED (same). **COVERED**, tile
"failure states and autosave policy" (partial).

THE ARGUMENT FOR THE ASK, because this one cuts both ways and I will not
pretend otherwise. FOR making saving cost something: a permanent-memory game has
a unique vulnerability that KCD2 does not have. If the player can reload the
moment they are seen, the moat is optional, and every hour of work on perception
and memory is defeated by a keypress. That is a real threat and it is worth
saying out loud. AGAINST: this is the most criticised system in both KCD games
(CITED, search summary of TheGamer and OpenCritic: the save system was "so
controversial a save and exit option was eventually patched in", and PS5
aggregate criticism concentrates on "exactly these two systems", combat and
saving), and Meridian Test condition 1 gives us thirty minutes before a player
bounces. Punishing saving in the first thirty minutes is a good way to lose them
in the first ten. THE THIRD OPTION, which neither game takes and which I think
is the interesting one: save freely, but write the save AT THE MOMENT OF BEING
SEEN, so reloading costs the player the whole approach rather than the sighting.
The moat survives, the friction lands on planning rather than on patience, and
nothing is taken away from the player. That is a judgement about feel, so it is
his.

**F4. Sleeping at a bed, choosing a wake time on a 24-hour wheel.** CITED
(search summaries of Deltia's Gaming and ScalaCube).
**COVERED**, tile "sleep and the day boundary" (typed absent), whose note is
exact: "The only hit is System.Threading.Thread.Sleep(50) at Game/Audio.cs:1291,
a thread call and not a verb. Nothing advances the clock by resting and nothing
ends a day."
**IN, and the argument is the moat's clock.** Pillar 1 propagates gossip through
schedule intersections, so a rumour has a travel time. If the player cannot
deliberately cross a day, that travel time is something that happens TO them
rather than something they play against, and the best move in the game (do the
thing, then get off the street before the mill turns) is unavailable. Sleep is
not an upkeep system here, it is the control the player uses to move through the
moat's own timeline. It is also what makes the morning after exist as a thing to
dread.

**F5. Bed ownership: your own bed, rented lodgings, campsites, and trespass if
you use somebody else's.** CITED (same). **ABSENT** as a system.
**OUT.** Tom owns Mickey's from the first minute; the premise hands him the bed
that KCD2 makes you earn. Making lodging a resource would be inventing a problem
the story already solved. The one thread worth keeping rides on B14: sleeping
somewhere that is not yours is a perceivable act.

**F6. A map with exploration fog, a compass, and quest markers.** CITED
(search summary of Fextralife, "Hardcore Mode", by contrast).
**COVERED**, tile "map and minimap" (typed absent), whose note records that D12
was the blocker, D12 was decided, "so nothing blocks this but the work".

**F7. Hardcore mode removes the player marker from the map, removes compass
bearings, removes fast travel, and requires at least three permanent negative
perks.** CITED (search summaries of Fextralife, "Hardcore Mode", PowerPyx, and
the official account: "No map markers. No fast travel. No compass.").
**ABSENT.** **ASK** (the negative perks half is **RULED OUT** by D11).

**F8. You can ask an NPC for directions, and they open the map and point at
where you are.** CITED (search summary of TheGamer, "The Map In Kingdom Come:
Deliverance 2's Hardcore Mode Is Genius"): "there is a dedicated interaction
with NPCs to ask for directions, which opens up the map and they'll pinpoint
where you are."
**ABSENT.** **ASK, bundled with F7, and it is the best single idea this game
gave the audit.** D12 already lists the diegetic verbs by which the player is
allowed to learn things: "asking around, buying gossip, pub talk, eavesdropping,
stealing tapes. There is no free omniscient read." Asking a person where
something is, is that same rule applied to geography, and it turns navigation
into an encounter with somebody who then remembers that you asked. In a one-town
game the player will learn by walking anyway. Whether Meridian has a map at all
is a feel call, which is why this is ASK and not IN.

**F9. Mandatory negative perks chosen at the start of a Hardcore run.** CITED
(search summary of PowerPyx). **RULED OUT** by D11.

**F10. Fast travel, with random encounters interrupting it.** CITED (search
summary of Fextralife and GameSpot). **ABSENT.** **OUT.** One walkable town.
Fast travel would remove the streets, and the streets are where the moat
happens: every walk past the same shopfront is a chance to be seen by somebody
with a schedule.

**F11. A codex that explains a system, unlocked on first contact with that
system.** CITED (search summary of TheGamer and community discussion): "many
explanations don't get unlocked until the accompanying feature is first
interacted with in-game".
**ABSENT.** **IN as a rider on the existing tile "first hour and tutorial", not
as its own system.** It is cheap, it is period-correct in a game where paper is
the information channel, and just-in-time is the right shape for a game whose
rules are social rather than mechanical. Small.

**F12. Teaching through play, deliberately sparse, with some systems never
explained at all.** CITED (search summary of TheGamer and Fextralife
beginner guides): "Some vitally important stuff is just left for players to
discover on their own entirely", and "the game's opening feels slow and
overwhelming, but this is intentional".
**COVERED**, tile "first hour and tutorial" (partial).
**OUT for KCD2'S DEGREE of it, and this is a case where copying the admired
thing would be a mistake.** KCD2 has a hundred hours to recover from a bad first
hour. Meridian Test condition 1 gives us thirty minutes, total, before a player
who loves KCD2 decides. Those are opposite requirements, and the fact that
KCD2's opacity is admired by the people who stayed tells us nothing about the
people who left. Our version should teach the moat fast and hide nothing that a
player needs in order to understand that they are being watched.

**F13. Reading as an activity, gated on a Scholarship skill that sets reading
speed, in a world where literacy is rare.** CITED (search summaries of
Fextralife, "Scholarship", and the Fandom wiki, "Reading"): "Literacy allows
you to read, a far from common skill for medieval man."
**COVERED** for the object (tile "letters and newspapers the player can read",
typed absent, whose note says "LATE-ANALOG: paper is the information channel, so
this is pillar work and not dressing"); **RULED OUT** for the skill (D11).
**The conceit does not transfer at all and that is worth stating plainly**:
KCD2's reading system is interesting because literacy is scarce in 1403.
Literacy in a British port town in 1990 is universal. What survives is that
reading takes TIME and can be WITNESSED, which is a rider on the existing tile:
a man reading somebody else's letter is a man doing something in front of
whoever walks in.

**F14. Skill books in graded volumes, each needing a higher skill to read.**
CITED (search summary of INARA, "Skill books"). **RULED OUT** by D11.

**F15. A carried torch, which lights a small radius and raises enemy detection
range at night.** CITED (search summary of bo3.gg and PC Gamer): community
analysis puts the increase at 19 percent. HOLE: that figure is a community
measurement relayed by a search summary and I could not reach the original;
treat it as a direction, not a number.
**ABSENT.** **OUT for now, with a named condition for reopening it.** Meridian
in 1990 has sodium street lighting, and a man walking through a town centre
holding a torch is not a period image, it is a medieval one. The PERCEPTION half
is already ours: `Core/Perception.cs` scales every identification rung by
`LightFactor(lightLevel)`, so darkness already lowers the rung at which you are
identified, which is the mechanic the torch exists to trade against. REOPEN IT
IF: burglary (a tile, typed absent) lands with dark interiors, where a carried
light becomes a real decision again.

**F16. A potion that acts as night vision.** CITED (search summary of bo3.gg).
**ABSENT.** **OUT.** Fantasy affordance, and A12's argument.

### G. Craft, services and minigames (8)

**G1. Alchemy at a bench, with recipes and ingredients.** CITED (search summary
of TheGamer, "Every Minigame Ranked"). **ABSENT.** **OUT.**
**G2. Blacksmithing at an anvil.** CITED (same). **ABSENT.** **OUT.**
**G3. Weapon sharpening at a wheel.** CITED (same). **ABSENT.** **OUT.**

The argument for G1 to G3 is one argument. Crafting is a private loop: the
player and a bench, with nobody watching and nothing remembered. Against the D24
test it feeds none of the four, and it is expensive in exactly the way the
project cannot afford, which is bespoke authored interaction. KCD2's crafting is
excellent and is excellent at being a different game's pillar.

**G4. Dice as a tavern minigame.** CITED (same). **RULED OUT** by D17 and D18:
gambling is out entirely.

**G5. Archery contests.** CITED (same). **ABSENT.** **OUT.** No analogue, and
the nearest one would be a competitive social event, which is content rather
than a system.

**G6. Haggling and trading with merchants.** CITED (search summary of
HowToPlayHub: reputation "unlocks better merchant prices"). **PARTIAL**, tile
"economy and trading" (partial), which records that no prices, no trade surface
and no shop exist in the scripts walked.

**G7. A dog companion.** DERIVED from CITED: the perk list includes a
"Houndmaster Perks" category (search summary of Fextralife, "Perks"), which is
evidence a dog system exists. HOLE: the searches I ran did not return a direct
description of it, so its scope here is inferred from a perk category and
nothing more.
**ABSENT.** **OUT.** A companion that follows you everywhere is a second
perceivable object attached to the player, which is interesting, and it is also
an animal AI, a leash system and an authored relationship. The budget rule says
no.

**G8. The bathhouse as a service location bundling health, cleaning, repair,
a bed and temporary buffs.** CITED (search summary of Fextralife, "Baths").
**ABSENT.** **OUT as a bundle; the cleaning half rides with A6.** Note for the
record that KCD2's bathhouses also sell services D18 forbids, so the location as
KCD2 builds it is not available to us in any case.

## 4. The ten items the brief already knew about

Answered directly, in the brief's own order, with the column each falls in.
Three of these had answers already in the repository that the first pass could
not have seen, which is section 2.

| # | Item | Column | Verdict |
|---|---|---|---|
| 1 | Character appearance and cleanliness as a perception input | ABSENT from the inventory, PART BUILT in code | **IN** (A4, A5, 2.1) |
| 2 | Sleep, rest and how a day is crossed | COVERED by a tile typed absent | **IN** (F4) |
| 3 | Stolen goods, fences and evidence on the person | ABSENT from the inventory, PART BUILT in code | **IN** (B8, B11, 2.2) |
| 4 | Persuasion, coercion and intimidation as a resolved system | PARTIAL | **IN, re-based off D11** (C1 to C3) |
| 5 | Reputation per faction and per district | ABSENT | **ASK** (D1 to D3) |
| 6 | Carrying and encumbrance | PARTIAL | **OUT** (A13) |
| 7 | Light sources at night | ABSENT (player-carried); the perception half is COVERED | **OUT, with a reopening condition** (F15) |
| 8 | Reading as an activity | COVERED for the object, RULED OUT for the skill | **Rider, not a system** (F13) |
| 9 | Saving as a scarce resource | COVERED as a surface, ABSENT as a constraint | **ASK** (F1 to F3) |
| 10 | Tutorial through play | COVERED | **OUT at KCD2's degree** (F12) |

## 5. What the recommendations would cost

Rule 7 applies: what dominates, or no number. I have given no week counts
because I have no measured series for this studio's throughput on systems work
and will not invent one. What follows names the dominating cost and the thing
that could blow it up.

- **A4, A5, B11 (appearance, condition, carried evidence as perception
  inputs).** DOMINATED BY: the art side, not the code side. The predicate is a
  second caller on an existing function; making a coat visibly bloodied, torn or
  different in a photoreal frame is material and asset work on a body pipeline
  whose tile ("bodies and faces") is typed partial and reads `bodySkinned=0`.
  COULD BLOW UP: if it needs distinct garment meshes rather than material
  states.
- **B8 (provenance a person can connect to you).** DOMINATED BY: the surface,
  not the model. `Traces` and `EvidenceHost` exist; what does not exist is any
  screen or line through which the player learns that the watch is traceable.
  That is the Ledger notebook (tile partial, queue 037), so this rides on work
  that is already specified.
- **F4 (sleep and the day boundary).** DOMINATED BY: what happens while you
  sleep. Advancing a clock is trivial; making the sim run a night correctly, and
  making the player wake into a town that moved, is the actual work, and the tile
  note says nothing currently ends a day.
- **C1 to C3 (resolved persuasion).** DOMINATED BY: the writing, not the maths.
  The check is arithmetic over memories that exist. What makes it land is that a
  failed check surfaces the reason (D12's legibility clause), and a reason a
  player believes is an authored line per case.
- **E5 (the town's behaviour changing after a crime).** DOMINATED BY: the
  schedule system's willingness to bend. Routines exist and heat exists; the cost
  is in making a bent routine still look deliberate rather than broken, which is
  the kind of thing only a frame can judge.

## 6. What could not be established

Named rather than smoothed over.

1. **D24.** Does not exist in this checkout. Section 0.4.
2. **Whether any of section 2's built systems has ever run in front of a
   person.** I established the code and the call sites. I did not establish a
   gate, a verdict key or a played build. Built is not running.
3. **KCD2 numbers.** Every quantity relayed here (base carry weight 70, five
   per Strength point, 275 perks, 2400 NPCs, the 19 percent torch figure, the one
   to two week stolen-tag decay) comes through a search summary. None was read
   from a primary source or from the game. They are directions, not measurements.
4. **The dog.** Inferred from a perk category (G7).
5. **KCD2's reputation internals.** Whether a settlement's reputation is a
   single stored number or a computed aggregate is exactly the distinction the
   ASK at D3 turns on, and I could not establish it: the sources describe the
   player-facing behaviour only. This is the most consequential hole in the
   file.
6. **The curfew rule** (B17), relayed from a guide and not from a primary
   source.
7. **Systems I know are missing from the 71.** KCD2 contains at least: combat
   depth (master strikes, clinches, directional attacks), archery, stealth
   takedowns, armour layering and its effect on noise, tournaments, the dog, the
   companion characters, quest branching and failure, the two-region map
   structure, and the DLC content. Combat was not enumerated because tile
   "combat" is partial and D4 already sequences it; the rest were out of the
   time this pass had. The count of 71 is what one session's search channel
   surfaced, not a census.

## 7. Sources

Every one is the search channel's summary of the page named, retrieved
2026-09-14. None was read in full; see 0.3.

- Fextralife, "Skills", https://kingdomcomedeliverance2.wiki.fextralife.com/Skills
- Fextralife, "Perks", https://kingdomcomedeliverance2.wiki.fextralife.com/Perks
- Fextralife, "Persuasion System", https://kingdomcomedeliverance2.wiki.fextralife.com/Persuasion_System
- Fextralife, "Hardcore Mode", https://kingdomcomedeliverance2.wiki.fextralife.com/Hardcore_Mode
- Fextralife, "Baths", https://kingdomcomedeliverance2.wiki.fextralife.com/Baths
- Fextralife, "Scholarship", https://kingdomcomedeliverance2.wiki.fextralife.com/Scholarship
- Fextralife, "Horses", https://kingdomcomedeliverance2.wiki.fextralife.com/Horses
- Method.gg, "Best Perks in Kingdom Come Deliverance 2", https://www.method.gg/kcd2/best-perks-in-kingdom-come-deliverance-2
- Gamerant, "How to Pass Speech Checks (Intimidation, Persuasion, Coercion)", https://gamerant.com/kingdom-come-deliverance-2-kcd2-how-pass-speech-checks-intimidation-persuasion-coercion-dialogue/
- Gamerant, "Kingdom Come: Deliverance 2's Crime System Explained", https://gamerant.com/kingdom-come-deliverance-2-crime-punishment-reputation-system/
- Gamerant, "How Does Crime and Punishment Work", https://gamerant.com/kingdom-come-deliverance-2-kcd2-crime-punishment-branding-executions/
- Gamerant, "Energy and Nourishment Consequences Explained", https://gamerant.com/kingdom-come-deliverance-2-kcd2-restore-energy-nourishment/
- Gamerant, "How to Heal", https://gamerant.com/kingdom-come-deliverance-2-how-heal/
- Escorenews, "How Speech, Charisma, and Persuasion stats work in KCD2", https://escorenews.com/en/article/66480-how-speech-charisma-and-persuasion-stats-work-in-kcd2-guide-to-dialogue-and-talking-in-kingdom-come-deliverance-2
- Escorenews, "How to see list of your crimes when arrested by guards", https://escorenews.com/en/article/66186-how-to-see-list-of-your-crimes-when-arrested-by-guards-in-kingdom-come-deliverance-2-how-to-understand-why-henry-is-arrested-in-kcd2
- The Escapist, "How Crime and Punishment Work", https://www.escapistmagazine.com/how-crime-and-punishment-work-in-kingdom-come-deliverance-2/
- HowToPlayHub, "KCD2 Reputation Guide", https://howtoplayhub.com/kingdom-come-deliverance-2/reputation-guide
- Kingdom Come Deliverance Fandom wiki, "Stolen goods", https://kingdom-come-deliverance.fandom.com/wiki/Stolen_goods
- Kingdom Come Deliverance archive wiki, "Crime and reputation", https://kingdomcomedeliverance-archive.fandom.com/wiki/Crime_and_reputation
- Deltia's Gaming, "How to Sell Stolen Items", https://deltiasgaming.com/how-to-sell-stolen-items-in-kingdom-come-deliverance-2-2/
- Deltia's Gaming, "How to Launder Clothes", https://deltiasgaming.com/how-to-launder-clothes-in-kingdom-come-deliverance-2/
- Deltia's Gaming, "Weight Guide", https://deltiasgaming.com/weight-guide-for-kingdom-come-deliverance-2/
- Deltia's Gaming, "How and Where To Sleep", https://deltiasgaming.com/how-and-where-to-sleep-in-kingdom-come-deliverance-2/
- GameSpot, "How To Increase Carry Weight And Manage Encumbrance", https://www.gamespot.com/gallery/kingdom-come-deliverance-2-carry-weight-encumbrance/2900-6188/
- GameSpot, "How To Equip Horse Items", https://www.gamespot.com/gallery/kingdom-come-deliverance-2-horse-items-saddle/2900-6198/
- Gamer Guides, "Washing Clothes and Armor", https://www.gamerguides.com/kingdom-come-deliverance-ii/guide/getting-started/gameplay/washing-clothes-and-armor
- Sportskeeda, "Charisma in Kingdom Come Deliverance 2, explained", https://sportskeeda.com/esports/charisma-kingdom-come-deliverance-2-explained
- Sevenswords, "Kingdom Come II Survival Guide", https://sevenswords.uk/kingdom-come-ii-survival-guide/
- Gamepressure, "How does starvation and exhaustion work", https://www.gamepressure.com/kingdom-come-deliverance-2/how-does-starvation-and-exhaustion-work/z31179a
- TheGamer, "Saviour Schnapps Is Still Needed To Manually Save", https://www.thegamer.com/kingdom-come-deliverance-2-saviour-schnapps-save-system-unchanged-loading-manual/
- TheGamer, "Restricting Your Saves Is Good, Actually", https://www.thegamer.com/kingdom-come-deliverance-2-save-system-schnapps-good-actually/
- TheGamer, "The Map In Hardcore Mode Is Genius", https://www.thegamer.com/kingdom-come-deliverance-2-kcd2-dlc-worth-playing-on-hardcore-map-navigation/
- TheGamer, "Every Minigame In Kingdom Come: Deliverance 2, Ranked", https://www.thegamer.com/kingdom-come-deliverance-2-every-minigame-ranked/
- TheGamer, "Where To Find Beds", https://www.thegamer.com/kingdom-come-deliverance-2-beds-where-to-find/
- TheGamer, "How To Recover Health", https://www.thegamer.com/kingdom-come-deliverance-2-how-to-heal-recover-health-bleeding-guide/
- OpenCritic, "Saviour Schnapps Is Still Needed To Manually Save", https://opencritic.com/news/11565/saviour-schnapps-is-still-needed-to-manually-save-in-kingdom-come-deliverance-2
- PC Gamer, "How to use a torch", https://www.pcgamer.com/games/rpg/kingdom-come-deliverance-2-torch-how-to-use/
- bo3.gg, "How to See in the Dark", https://bo3.gg/games/articles/how-to-see-in-the-dark-in-kingdom-come-deliverance-2
- PowerPyx, "Hardcore Mode Guide", https://www.powerpyx.com/kingdom-come-deliverance-2-hardcore-mode-guide/
- Wccftech, "Dev Talks About Dynamic NPC Routines and Emergent Storytelling", https://wccftech.com/kingdom-come-deliverance-2-dev-talks-about-dynamic-npc-routines-and-emergent-storytelling-for-side-quests/
- GDC session listing, "Supporting Thousands of NPCs in Kingdom Come: Deliverance and Kingdom Come: Deliverance II", https://schedule.gdconf.com/session/supporting-thousands-of-npcs-in-kingdom-come-deliverance-kingdom-come-deliverance-ii/915120
- AI and Games Conference, "Supporting thousands of simulated NPCs in the open world of KCD2", https://www.aiandgamesconference.com/schedule/supporting-thousands-of-simulated-npcs-in-the-open-world-of-kcd2/
- INARA, "Skill books", https://inara.cz/kingdom-come-2/skill-books/
- ScalaCube, "Crime and Punishment Explained", https://scalacube.com/blog/kingdom-come-deliverance-2/crime-and-punishment-explained-in-kingdom-come-deliverance-2
- Gameranx, "How To Sell Stolen Items", https://gameranx.com/features/id/528127/article/kingdom-come-deliverance-2-how-to-sell-stolen-items/

Repository sources, all read this session at commit `074f85b`:
`production/systems-inventory.json`, `canon.md`,
`ledger-v2/respec/vision-pillars-v2.md`,
`ledger-v2/respec/decision-register/D11-player-progression.md`,
`ledger-v2/respec/decision-register/D12-information-surfaces.md`,
`ledger-v2/respec/decision-register/rulings-log.md`,
`ledger/Assets/Scripts/Core/Traces.cs`, `Core/Coat.cs`, `Core/Observation.cs`,
`Core/Perception.cs`, `Core/PlayerIdentity.cs`, `Core/Wardrobe.cs`,
`Game/EvidenceHost.cs`, `Game/ViolenceHost.cs`, `Game/NpcWalker.cs`,
`Game/GameController.cs`, `Game/GossipDirector.cs`, `Game/SimDirector.cs`.
