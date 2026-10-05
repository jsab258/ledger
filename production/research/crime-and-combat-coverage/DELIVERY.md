# Crime and combat coverage audit: the full grid

STATUS: SPEC (research delivery). Branch `research/crime-and-combat-coverage`.
Written 2026-09-21. Audited against [BRIEF.md](./BRIEF.md), written first.

NOTHING HERE IS AN INSTRUCTION. No queue item, no decision record, no code.

## 0. Method and sourcing

The brief's warning was the right one and it changed the answer. **Core is much
more built than the commission assumes.** Everything below marked BUILT was read
out of the source this session, not recalled.

Read: 103 files in `ledger/Assets/Scripts/Core/`, of which the public surface of
`Empire.cs` (1,200 lines), `Operation.cs`, `Combat.cs`, `Harm.cs`,
`Homicide.cs`, `Arsenal.cs`, `LooseEnds.cs`, `Informing.cs`, `Debts.cs`,
`Negotiation.cs`, `Press.cs`, `Summons.cs`, `Suspicion.cs`, `Traces.cs`,
`ContentRule.cs`, `IntentRouter.cs` and `ActThree.cs` was extracted in full
(enums and public methods), plus targeted reads of bodies. Wiring was checked
against the 89 files in `Game/`.

Reference games: four web searches. The search channel returned listicles for
the console crime games and substantive mechanics only for Crusader Kings 3 and
Godfather II, so those two carry most of section 6 and the rest is labelled.

TWO INSTRUMENT FAULTS OF MINE, recorded because the rules require it. My first
wiring check used `\bHomicide\b` and `\bOperation\b` and returned zero Game-layer
references for both, which would have been a false and consequential finding.
The real symbols are `game.Homicides`, `HomicideBook`, `OperationTarget` and
`OperationPlan`: 46 and 20 hits. Both systems are wired. Corrected before it
reached the grid.

LINK NOTE: the links in this file to other deliveries will not resolve until the
corpus is consolidated onto one branch, which had not happened when this was
written (`production/research/` on `origin/main`: 0 files).

## 1. The headline

**The crime half is not thin. It is one verb short, and that verb is the one
Jafar asked about.**

Measured: no delegation verb exists anywhere in Core. A search across all Core
files for `Order|Command|Dispatch|SendCrew|TellCrew|Instruct|Hit|Contract` as
call sites returns only LINQ `OrderBy`. And `OperationTarget` is a place, not a
person: its fields are `Id, Name, PlaceId, Difficulty, Payout, Exposure, Done,
DoneDay`.

So the player can fight a man himself (`Combat`), can plan a job on a building
with crew (`Operation.Bringing`), can recruit, pay and cut in a crew
(`Empire.RecruitByNeed`, `SetCut`), can buy, squeeze or blackmail a business
(`BuyClean`, `BuyDebt`, `Squeeze`, `AcquireViaHook`), and can pledge to or break
with a rival arm. **There is no verb between deciding a man should be hurt and
`Homicide.Record` recording that he was.**

## 2. The grid: stages down, actors across

Marks: **B** built in Core and reached from `Game/`; **C** built in Core, thin or
unreached; **M** missing. Evidence is the file that proves it.

### 2.1 Planning

| actor | mark | evidence and what exists |
|---|---|---|
| Player | **B** | `Operation.cs`: `Approach {Quiet, Forced, Social}`, `Read(plan,target,state) -> PlanRead`, `HourDensity(hour)`, `RiskWord(risk)`. `Game/PlanUI.cs`, `Game/OperationSetup.cs` |
| Crew | **B** | `Operation.Bringing(ids)`, `CompetenceOf`, `LoyaltyOf`; the weakest link is computed (`plan.Crew.OrderBy(state.CompetenceOf)`) |
| Rivals | **C** | `Empire.RivalArm`, `Summons.Due/TermsFor`. Rivals summon you; you cannot plan against them |
| Police | **M** | nothing lets the player plan around a known police pattern |
| Public | **B** | `Operation.HourDensity`, `OperationTarget.Exposure` |
| Press | **M** | no planning surface |

**The hole: a plan whose target is a person, and a plan the player does not
attend.** Both are single missing fields plus a resolver, not new subsystems.

### 2.2 Doing

| actor | mark | evidence |
|---|---|---|
| Player | **B** | `Combat.cs`: `Blow {SquareUp, Strike, Shove, Guard, BackOff, Finish}`, `Footing {Steady, Reeling, Down}`, stamina model, `Available`, `Resolve`, `Breathe` |
| Weapons | **B** | `Arsenal.cs`: `Family {Hands, Blunt, Edged, Ligature, Firearm, Environment, Kit}`, `Concealment {Innocent, Concealable, Damning, Impossible}`, `FriskCost`, `Fits` (carry limits), `AccidentAvailable` |
| Victim | **B** | `Arsenal.Threat {Comply, Freeze, FleeScreaming, CallTheBluff, Escalate}`; `Harm.Inflict`, `InjuryKind {Bruised, Cut, Broken, Bad}` |
| Crew | **M** | crew are brought on a job; nothing models a crew member fighting |
| Police | **M** | no response to a fight in progress |
| Public | **C** | `Combat.Saw(nearby, streetNoise)` resolves witnesses, but during-fight bystander behaviour is not modelled |

### 2.3 Being seen, recognised, remembered, talked about

| stage | mark | evidence |
|---|---|---|
| Seen | **B** | `Observation.cs` (521 lines), `Combat.Confidence(metres, occluded, streetNoise)`, `KillingConfidence`, `Acoustics.cs` |
| Recognised | **B** | five-rung identification (pillar 1), `Acquaintance.cs`, `Coat.cs` and `Wardrobe.cs` for changing what you look like, `Harm.LooksLike(personId, day)` so an injury is itself an identifying mark |
| Remembered | **B** | `MemoryStore.cs`, `MemoryRetrieval.cs`, `PlayerKnowledge.cs`; D18 makes a killing permanent |
| Talked about | **B** | `Gossip.cs` (976 lines), `Confab.ShouldHush` (NPCs go quiet within 4.5m when talking about you, scaled by nerve), `Press.Print(day, loudness, law, ...)` |

This block is the moat and it is the best-built part of the game. Nothing here
is missing.

### 2.4 Being acted on

| actor | mark | evidence |
|---|---|---|
| Police | **B** | `Homicide.Inquiry {None, Procedure, Investigation, Manhunt}`, `Pressure`, `PressureWhy`, `Stage`, `SummonsEllis`, `AsksAboutYou`, `BarsQuietExit`, `SuspicionFloor`, `RumorHalfLifeHours`; `Game/LawHost.cs` calls `Homicides.PointAt` |
| Rivals | **B** | `Summons.Answered {Took, Missed, Refused}`, `StandingChange`, `AttentionChange`, `Apply`; `Empire.PledgeTo`, `BreakWith`, `NotePoach`, `ResolveTable` |
| Crew | **B** | `Homicide.LoyaltyCeiling(nerve)`, `WouldTalkToPolice(g)`, `LooseEnds.SawCrew(loyalty, floor)`, `Harm.Feud`, `WillWorkTogether(a,b)` |
| Public | **B** | `Reaction.cs`, `Notice.cs` (`HushFraction(attending, present)`), `Suspicion.SuspicionLevel {Trusting, Uneasy, Suspicious, Confronting}` |
| Press | **C** | `Press.Print` and `Press.Notoriety` exist and are driven by loudness and inquiry stage. The player has no verb that touches the paper |

### 2.5 Living with it

| thing | mark | evidence |
|---|---|---|
| Physical traces | **B** | `Traces.cs`: `Stain` with `Noticeable(metres, lightLevel)`, `Age(minutes)`, `Wash(minutesSpent, hasWaterAndPrivacy)`, `SocialCost(familiarity)` |
| The weapon | **B** | `Traces.Origin {Bought, Stolen, Taken, Inherited, Ordinary}`, `Used(item, what, onWhom)`, `Traceability`, `Dispose(where, seen)`, `ResidualRisk` |
| The body | **M** | `Homicide.Record` takes a `where` and there is no verb to move, hide or delay the finding of a body |
| Injury | **B** | `Harm.Capability(person, day)`, `Treat(injury, wallet, day)`, `ScarsOf`, healing over days |
| Obligations | **B** | `LooseEnds.Kind {Law, Crew, Owed, Promise, Rumour, Standing}`, `Debts.Collect/Forgive/NightBorrowing` |
| The ending | **B** | `ActThree.cs`, section 7 |

## 3. The verified holes

Each was searched for before being called missing, as the brief required.

1. **Ordering violence.** No delegation verb in Core (section 1).
2. **A person as a target of a plan.** `OperationTarget` has `PlaceId` and
   `Payout` and nothing else.
3. **The body.** No `HideBody`, `MoveBody`, `ConcealBody` or discovery-delay
   anywhere in `Core/` or `Game/`.
4. **Leaning on a witness.** No `Recant`, `Retract`, `LeanOn`, `BuySilence`.
   NOTE, because it nearly became a false finding: `Gossip.Bribe(npcId,
   topicKey, offer)` and `BribePrice` DO exist and are wired into
   `Game/DialogueUI.cs`. That is paying somebody **to tell you** something. It
   is not paying them to stay quiet. And `hush` throughout Core is the town
   going quiet near you (`Confab.ShouldHush`), not the player hushing anyone.
5. **Crew sanction.** No `Expel`, `Demote`, `Discipline`, `Sanction`. You can
   set a man's cut and recruit him; you cannot punish him.
6. **Press manipulation.** No `PlantStory`, `KillStory`, `Leak`.
7. **Being outnumbered.** `Combat.Resolve(blow, self, target, metres)` is one
   against one. `Notoriety(witnessCount, killed)` counts watchers, not
   opponents.
8. **Police during a fight.** Nothing responds to violence in progress; the law
   engages through the homicide book afterwards.

## 4. Combat as its own layer

Against the brief's list: **fists** BUILT (`Blow`), **improvised and scarce
weapons** BUILT (`Arsenal.Family` including `Environment`, with `Concealment`
and `FriskCost` making carrying a choice), **injury** BUILT (`Harm`, with
capability loss and visible marks), **fighting dirty** PARTIAL (`Shove`,
`Finish`, `AccidentAvailable`), **being outnumbered** MISSING, **running**
PARTIAL (`BackOff` is a blow, not flight, and stamina already costs movement via
`StaminaAfterMoving`), **police response** MISSING, **what witnesses do**
SPLIT: after a fight BUILT (`Combat.Saw`, `Notoriety`), during a fight MISSING.

`Arsenal.FailureMode {LoseInPublic, HeStaysUp, HeGetsAHandOnIt, ItBreaks,
InterruptedMidway, MissAndTheStreetComes, HeSurvivesIt}` deserves naming on its
own: seven ways an attack goes wrong, of which at least three are social rather
than physical. That is already the right instinct for this game, and it is the
model the delegation verb should copy.

[D4](../../../ledger-v2/respec/decision-register/D4-combat-before-driving.md)
puts melee first and firearms scarce, which the `Arsenal.Family` ordering
matches.

## 5. Content rules, and where a verb is out

[D18](../../../ledger-v2/respec/decision-register/D18-content-rule.md) is
permanent and enforced in code by `Core/ContentRule.cs` (`IsShowableAge`,
`IsUnderageModel`, `IsShowableTrade`, `Screen(trades)`).

- **Drugs**: OUT as a verb, by name. Any "run the gear" verb is refused. The
  off-screen economy may be a rumour topic and a reason a rival has money.
- **Alcohol and gambling**: OUT as shown content. A pub may be a place and a
  business to squeeze; drinking and betting are not verbs and not depicted.
- **Children**: OUT everywhere, which removes a whole family of leverage verbs
  common to the reference games (threatening a man's family is available only as
  an adult relation, and see below).
- **Torture and cruelty as spectacle**: OUT. This constrains the delegation
  verb: ordering a beating is in scope, depicting one at length is not.
- **Police corruptible as individuals, never as a thesis**: so a bribe to one
  officer is admissible and a systemically bought force is not.

## 6. The reference games, mapped

CITED-SUMMARY unless stated. The search channel returned mechanics for two of
the six and listicles for the rest, so this section is honest about which.

**Crusader Kings 3** is the closest match to what LEDGER lacks, and it is not a
crime game. Its murder scheme has "a power, every target has a resistance, both
made up of their own skills plus their Spymasters", progresses over time, and
"the job might also be botched". Agents are recruited into the scheme, and
unwilling agents are coerced: secrets become hooks, where "a Criminal Secret
will give you a Strong Hook", weak hooks are single-use and strong hooks are
repeatable and "prevent the target from taking hostile actions against the
holder".

DERIVED, and it is the most useful mapping in this audit: **LEDGER already has
every part of that except the scheme itself.** `Empire.AcquireViaHook(business,
secret, owner, now)` is a hook used on a business. `Negotiation.Lever {Money,
Need, Secret, Threat, Respect}` is the coercion ladder. `Operation` is the
scheme with a target that happens to be a building. Nothing needs inventing; one
resolver needs writing.

**Godfather II** supplies the interface: from the "Don's View" strategy map you
"select a business that they want to bomb or attack, then select any crew member
and click ok", and crew can be "commanded directly in battle" or "sent to do a
job in another part of the world". Crew have specialised skills.

DERIVED: the two halves LEDGER has are the direct-command half and the empire
book. The missing half is send-a-man-elsewhere, and `Empire.CrewMember` already
carries competence and loyalty to resolve it with.

**Mafia, Sleeping Dogs, Yakuza, GTA**: the search channel returned comparison
listicles rather than mechanics. ASSUMED from general knowledge and marked as
such rather than cited: Sleeping Dogs is melee-led with environmental finishers
and a dual-reputation system; Yakuza separates street brawling from a business
management layer; Mafia is mission-authored rather than systemic; GTA supplies a
wanted-level model that this project's [Hitman
audit](../coverage-audit-hitman/SUMMARY.md) already argued against, since a
star meter is the opposite of a town that must be asked what it knows. HOLE:
none of this paragraph is sourced well enough to design from.

## 7. The ending, which is not undecided

The brief says "how the game ends is undecided". **Measured, it is decided and
built.** `Core/ActThree.cs` (642 lines, 161 references across `Game/`, with its
own `Game/ActThreeHost.cs`) defines:

`Ending {None, Both, Kingdom, StraightLife, BurnBoth, Quiet}`

with `Eligible(LedgerState) -> List<Ending>` and
`Resolve(s) => live.Count == 0 ? Ending.BurnBoth : live[0]`.

The comments in `Eligible` are where the red team's finding actually lives:

- **Quiet** requires `s.HandedOver && s.HasReadySuccessor && !s.Hunted`, and the
  file says why: "Signing the licence over settles who owns a pub; it does not
  settle a body, and the one thing a successor cannot inherit is a homicide.
  This is the only place the lethality answer takes an ending off the table
  outright, and it takes the quietest one."
- **Both** requires life loyalty above a trust threshold, an undissolved empire,
  and a managed information landscape (`DayCircleRacketHeat` below a fact
  threshold and `EllisCaseAnswerable`).
- **BurnBoth** is the default. The file: "This is what doing nothing produces,
  which is correct: it comes due whether or not you answer it."

DERIVED, and this is the honest form of "no route back": there are routes back,
and none of them is recovery. Once the town has turned, Quiet is barred by
`Hunted` and Both is barred by the landscape, which leaves Kingdom (keep
everything, nobody left who knew you before) and StraightLife (give up the
business to keep the people). Both are surrender of one half to save the other.
**The system does not lack an exit. It lacks an exit that costs less than
everything.** Whether that is a fault or the game is section 8's question.

## 8. What could not be established

1. **Whether Kingdom and StraightLife are actually reachable from a hunted
   state.** I read `Eligible`'s first gate and its comments, not its full body.
   This is the question the red team's finding turns on and it is answerable by
   reading one method.
2. **Mechanics for four of the six reference games** (section 6).
3. **Whether any of this is reachable in live play.** Wiring was checked by
   reference count, not by running the game. Rule 6 says built is not running
   and reference counts are a weaker instrument than a call trace.
4. **What `IntentRouter` actually exposes to the player.** It routes text to
   verbs with `IntentKind {Narrative, Mechanical, Novel}`, and I did not
   enumerate the verb table itself, which is the true player-facing list.
5. **Any judgement about how the combat feels.** Nothing was played.
