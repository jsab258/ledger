# How players actually behave when a world remembers them

Research topic 25, the last in the queue. Delivered to the studio. Nothing here
is an instruction.

Scope split with two earlier topics, declared once: "emergent story legibility"
and "detection legibility" asked how to MAKE a thing readable. This one asks
what players have been OBSERVED to do when a game already does it, which is a
different question and has a different and smaller evidence base.

It ends up being about the Meridian Test's second condition, because that is
where the evidence lands hardest.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

---

## Part 1. The behaviour that is actually observable: they retell

### 1.1 The Nemesis System, which is the closest precedent that shipped

CITED: the Nemesis System let enemies grow in power after defeating the player,
carry the scars of previous fights, and remember the history between them and
the player, organised into a hierarchy with unique names, titles, personalities,
voices and skills.
[Game Developer, Designing Shadow of Mordor's Nemesis system](https://www.gamedeveloper.com/design/designing-i-shadow-of-mordor-i-s-nemesis-system),
[CBR, Why Shadow of Mordor's Nemesis System is genius](https://www.cbr.com/shadow-mordor-nemesis-system/)

CITED, the design framing, and it is not vague: design director Michael de
Plater worked from self-determination theory and its three needs, competence,
autonomy and relatedness, with "How can we make narrative out of the gameplay?"
as the question at the core. "The game's designers put aside their desire to
tell a grand story and instead focused on ways players could create and share
their own experiences."
[Game Developer, as above]

DERIVED: the design goal that produced the most celebrated
world-remembers-you system in games was not that the player would NOTICE the
memory. It was that the player would have something to SHARE. That is a
behaviour, it is observable from outside the game, and it is a different target
from recognition.

### 1.2 The story generators, where the behaviour is documented at scale

CITED: Dwarf Fortress and RimWorld are described as "story generators, a type
of game in which fun does not come from reaching specific objectives but rather
from seeing non-scripted stories play out from the actions of the player", with
"thousands of stories online about the fun misadventures players have had".
[Game Developer, RimWorld, Dwarf Fortress, and procedurally generated story telling](https://www.gamedeveloper.com/design/rimworld-dwarf-fortress-and-procedurally-generated-story-telling),
[Game Developer, How Dwarf Fortress and RimWorld tell radically different stories](https://www.gamedeveloper.com/design/dwarf-fortress-and-rimworld-tell-very-different-stories)

CITED, the canonical instance: Boatmurdered, a shared Dwarf Fortress succession
game, "has been praised as an example of Dwarf Fortress' potential for emergent
storytelling, and credited for introducing both Dwarf Fortress and the Let's
Play format to a broader audience".
[Wikipedia, Boatmurdered](https://en.wikipedia.org/wiki/Boatmurdered)

DERIVED: across the three best-documented cases the observable player behaviour
is the same one. They retell. Not "players reported feeling recognised", which
nobody measured, but players wrote it down and told other people, in volume,
unprompted, for years.

### 1.3 The uncomfortable symmetry with our own code

`Core/Observation.cs` implements `Retell`, with the comment "MEMORY HARDENS AS
IT DECAYS: accuracy falls, confidence rises", four retellings per rung and a
0.94 certainty ceiling. The game models NPCs retelling what they saw.

DERIVED, and offered as an observation rather than a finding: the success signal
for this game, on the evidence in 1.1 and 1.2, is the PLAYER doing the thing the
NPCs already do in code. The moat is modelled inside the fiction and the
measurable outcome of the moat is the same act performed outside it.

---

## Part 2. The asymmetry, which is the finding of the topic

### 2.1 Players reliably notice forgetting, not remembering

CITED: "players quickly notice inconsistencies (timeline errors, impossible item
claims, or NPCs forgetting prior interactions), so long-horizon coherence and
state grounding are first-order requirements."
[via search summary alongside arXiv 2512.07388, Breaking Players' expectations: the role of non-player characters' coherence and consistency](https://arxiv.org/abs/2512.07388)

CITED, from the same study: two experiments found that "breaking players'
expectations influence[s] their evaluation of NPCs, with coherent and consistent
design reinforcing expectations and incoherent design challenging them", using
questionnaires, behavioural and physiological measures.
[IEEE Xplore, Breaking Players' Expectations](https://ieeexplore.ieee.org/document/11083609/)

CITED, a related result on the gap between design and reading: "player
interpretations of NPCs can differ from design intent, leading to
misunderstanding of NPC roles and potentially damaging believability and
immersion."
[ResearchGate, The Non-Player Character: exploring the believability of NPC presentation and behavior](https://www.researchgate.net/publication/303496966_The_Non-Player_Character_Exploring_the_believability_of_NPC_presentation_and_behavior)

HOLE, and it is the central one: I searched four ways for research measuring
whether players NOTICE a reputation or memory system that is working correctly,
and found none. The literature on reputation systems is about building them.
The literature on player perception is about what breaks. The positive case is
unmeasured.

DERIVED, and this is what the topic is for: **the evidence is asymmetric in a
way that matters for how this game should be judged.** Forgetting is loud and
memory is quiet. A world that remembers buys the absence of a failure the player
would have noticed, and that absence is worth a great deal and is almost
invisible while it holds.

### 2.2 Why that is not a counsel of despair

Two things cut the other way and both are in Part 1.

The Nemesis System was not quiet. It was the most talked-about feature of its
game and its owner patented it. The difference between quiet memory and loud
memory in that case was not the memory: it was that an orc who had beaten you
CAME BACK, with a scar and a line about it. The system did not wait to be
noticed; it presented itself.

And the story generators are not quiet either. What makes Boatmurdered is not
that the fortress remembered, it is that the remembering produced an EVENT
somebody wanted to describe.

DERIVED: the observable behaviour in 1.2 is downstream of a design property, and
the property is that the memory eventually does something that interrupts the
player. Recognition that only colours a greeting is the quiet kind.

---

## Part 3. The two clocks, and they do not agree

This is the concrete finding, checked in this checkout on 2026-09-14.

CITED, `CLAUDE.md`, the Meridian Test's condition 2: "Within those 30 minutes
the world visibly knows them at least once: recognized, gossiped about, or
confronted with something they did earlier."

CITED, `ledger-v2/respec/roadmap-v2.md:26`, phase 1's gate: "Gossip instrument
green: witnessed crime reaches a second and third NPC within one in-game week".

DERIVED: those are the same claim measured on two incommensurable clocks. One is
thirty REAL minutes of a stranger's first session. The other is one IN-GAME
week of simulated propagation.

CITED, the only conversion figure found: `Game/SimDirector.cs:1409`, "The sim
runs at twenty game-minutes per real second", which is a CI figure for a
headless run that has to cover eleven days, and is accompanied by the lesson
that mixing the two units caused four failed fixes ("THE BUDGET IS IN REAL
SECONDS, and the previous one was in game minutes, which is why none of the four
earlier fixes worked").

HOLE: I could not find a play-mode clock rate anywhere in this checkout. A grep
across `ledger/Assets/Scripts/` for `MinutesPerSecond`, `clockRate`,
`ClockScale`, `DayMinutes` and `compression` returns only comments about image
compression and the sim figure above. So the conversion between phase 1's week
and the Meridian Test's half hour is not established anywhere, in either
direction.

DERIVED, and stated carefully because the numbers are not available: the gossip
gate proves the mechanism PROPAGATES. It does not prove it propagates fast
enough to be witnessed in a first session, and nothing currently measures the
second thing. Those are different facts about one system, and this project's own
rule 2 is about exactly that distinction.

The same file that carries the 20-minutes-per-second figure also carries the
incident where confusing game minutes with real seconds cost four attempted
fixes. That is the strongest argument available for stating the two clocks
explicitly before phase 2 sets a feel target.

---

## Part 4. What this project already has bearing on it

CITED: `Core/Acquaintance.cs` grades Stranger 0.0, HeardOfYou 0.20, Known 0.50,
Close 0.80, and `Game/GameController.cs:78` supplies `FamiliarityWithPlayer`.

CITED: `Core/Gossip.cs` carries `HopDecay = 0.8` (:141) and
`MinConfidenceToShare = 0.2` (:142), and passes a rumour as
`r.Confidence * tie * HopDecay` (:371).

DERIVED, as arithmetic on this project's own constants rather than a claim about
play: a rumour starting at full confidence crosses the 0.2 sharing floor after
about seven hops of pure decay, fewer once the tie strength multiplier is below
1. So the mechanism is built to fade, which is correct design and also means
that WHERE the player is standing relative to the chain matters as much as
whether the chain runs.

CITED: `canon.md` already states the readout: "What the town calls you reads out
your standing: the new owner, then Novak, then Tom, then Toma. The gate is
knowing, not liking."

DERIVED: that ladder is the cheapest available instance of Part 2.2's
"presenting itself". It is a change in the words a stranger uses, it requires no
new system, and it is the one recognition signal that can fire in a first
session without a crime having happened at all.

---

## Part 5. What could not be established

1. **Whether players notice a working memory system.** Four searches, nothing
   measuring the positive case.
2. **The play-mode clock rate.** Not in this checkout.
3. **Any figures from the coherence study.** arXiv blocked again; the IEEE page
   was not fetched.
4. **Whether thirty minutes is a reasonable window** for condition 2. This
   depends on 2 and on design decisions not yet taken.
5. **Any post-launch data on Shadows of Doubt players** specifically, which
   would be the closest genre evidence and was not found in a usable form.

---

## Part 6. Findings and interpretation

### Findings

F1. The Nemesis System's stated design goal was that players could "create and
share their own experiences", built on self-determination theory, not that
players would notice the memory.

F2. Dwarf Fortress and RimWorld are documented as story generators with
thousands of player-written accounts; Boatmurdered is credited with popularising
both the game and the Let's Play format.

F3. The observable behaviour across all three cases is retelling.

F4. Research finds players quickly notice NPCs forgetting prior interactions,
timeline errors and impossible claims, making long-horizon coherence a
first-order requirement.

F5. No research was found measuring whether players notice a memory or
reputation system that is working correctly.

F6. Meridian Test condition 2 is measured in thirty real minutes; phase 1's
gossip gate is measured in one in-game week; nothing converts between them.

F7. The only clock figure in the checkout is 20 game-minutes per real second, a
CI sim figure, in the same file that records four failed fixes caused by
confusing game minutes with real seconds.

F8. `Gossip.HopDecay = 0.8` against `MinConfidenceToShare = 0.2` means a
full-confidence rumour fades below the sharing floor after roughly seven hops
before any tie-strength penalty.

### Interpretation

I1. The moat's value is asymmetric and the project should probably know that
explicitly: a world that remembers mostly buys the ABSENCE of a failure players
reliably detect. That is worth a great deal, it is not nothing, and it will not
show up in a thirty-minute test unless something makes it show up.

I2. The two cases where memory was loud rather than quiet share one property:
the memory eventually interrupted the player rather than colouring a greeting.
An orc came back with a scar and mentioned it. If condition 2 is to be met
reliably, something has to come back.

I3. The clock mismatch in Part 3 is the cheapest thing on this page to fix and
the easiest to leave. Two gates describe the same capability in units that
cannot be compared, in a project whose own file records what that confusion
already cost once.

I4. The standing ladder in canon is the recognition signal that can fire
earliest and costs least, and it does not need a crime to have happened. For a
first session it is probably worth more than the gossip mill, which needs an
event, witnesses, hops and time.

I5. Closing note on the whole queue rather than this topic: across
twenty-five topics the pattern that recurred most was not a missing feature. It
was a measurement that exists for one half of a question and is quoted for
both. This topic is the same shape: propagation is measured, timeliness is not,
and the gate reads as though it covered both.
