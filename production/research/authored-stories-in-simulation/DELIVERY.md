# Topic 15: authored stories that survive emergence

STATUS: SPEC (research delivery). Branch
`research/authored-stories-in-simulation`, from commit `074f85b`. Written
2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written, and no narrative is proposed. The brief says this
topic feeds a writing lane Jafar intends to open later, so it is written as
PREPARATION FOR A WRITER rather than as a survey: what the constraints are, what
the project already guarantees, and what a writer would need before they could
start.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged.
Repository claims name their file and line.

## 1. The problem, stated precisely for this game

CITED (search summaries of the ResearchGate entry for "Authoring emergent
narrative-based games" and the UC Santa Cruz paper "Open Design Challenges for
Interactive Emergent Narrative"): emergent narrative "requires the simulation to
contain a large number of consistent and interacting subsystems, resulting in a
combinatorial explosion of possible game states", and the named design challenges
are "modular content, compositional representational strategies, story
recognition, and story support".

DERIVED, translating those into our own terms: two of those four are legibility
problems and topic 7 already covers them under a plainer name. "Story
recognition" is whether the player notices a story happened. "Story support" is
whether the game helps them follow it.

The other two are the writer's problem, and they are the subject here:
**modularity** (a beat that can appear in many world-states) and
**composition** (beats that combine without contradicting).

## 2. What our architecture already guarantees a writer, which is more than most

This is the useful part and I do not think it has been collected anywhere.

**2.1 The language model cannot contradict the writer.** Pillar 3: "Every outcome
the player feels is decided in C#-style deterministic Core (whatever the engine).
LLMs classify, never adjudicate." Pillar 2: conversation outputs are
"classifications and closed-set choices that deterministic Core executes."

DERIVED: in most AI-NPC projects the generative layer is the thing that breaks
the story, because a model can say anything. Here it structurally cannot. A
writer working on LEDGER is writing against a deterministic simulation, not
against a text generator. That is a much older and better-understood problem.

**2.2 Nothing in the world can be un-happened.** `canon.md`: "Nothing is ever
wiped." So a writer never has to handle the case where an event the story depends
on gets retconned by a reload or a reset. Whatever happened, happened.

**2.3 The simulation's contradictions are enumerable.** From reading the Core
this session, the sim can contradict a writer on: who is alive
(`Core/Homicide.cs`), who knows what (`Core/Gossip.cs`), who is where
(`Core/DayJob.cs`, `Core/Occupancy.cs`), who will talk to the player
(`Core/Access.cs`, the doors tile), and how the law stands
(`Core/Homicide.Inquiry`). It cannot contradict canon, the existence of the acts,
or anything `Core/ContentRule.cs` screens.

**That list is short, and handing it to a writer on day one is worth more than
any technique in section 3.** A writer who knows the five things the world can
take away from them can write around all five.

## 3. The techniques, and we already have the best worked example

### 3.1 Write a beat as a WINDOW and a COST, not as an event

`Core/Beat.cs` is the thing to show a new writer first. Its header, read this
session:

> An authored social obligation: someone from the day life asks for the player's
> evening, deliberately overlapping the outfit's drop window, so the two lives
> compete for the same hours [...] Not a hard timer: attending is presence during
> the window, the windows overlap enough that a determined player can thread
> both, and skipping costs standing with a person, never the game.

DERIVED: that is the whole technique in one paragraph. The beat asserts almost
nothing about the world. It does not require a place to be safe, a person to be
alive at a particular minute, or an earlier beat to have gone a particular way.
It asserts a WINDOW and attaches a SOCIAL COST, and its failure mode is "somebody
remembers being stood up" rather than a broken quest.

**Nothing in the emergent-narrative literature I read states the principle as
cleanly as our own file does.** It should be the writing lane's first reading.

### 3.2 Predicate the beats on state, not on sequence

DERIVED from 2.3 and from the literature's "modular content": a beat gated on
"after act two, scene four" breaks when the player does things out of order. A
beat gated on "when at least two of the dockside crew believe the player was at
the warehouse" cannot break, because it is a question the simulation can always
answer.

Our simulation is unusually rich in such predicates: `GossipMill` can be asked who
holds what at what confidence, `HomicideBook.Stage` gives an inquiry level,
`Access` answers who gets in. A writer with those as the gating vocabulary is
writing something the world cannot invalidate.

HOLE: I did not establish how `Core/Campaign.cs`, `ActTwo.cs` and `ActThree.cs`
currently gate their beats, so I cannot say whether the existing act drafts are
written this way or the other way. **That is the first thing a writing lane should
check and I could not.**

### 3.3 Script the on-ramp and nothing else

CITED (search summary of the Shadows of Doubt devblog series via ModDB and
itch.io, particularly devblog 18, "Scripted Missions in a Procedural World", and
devblog 28, "Building the World Through Writing"): the game has "an initial
starting case that is more scripted than the rest of the game to teach you the
fundamentals", and the team built "a custom-made dialogue editor with access to a
wide number of procedural fields and variables, which also allows inserting
written content directly into the game for testing".

DERIVED: the pattern is that the most-authored content sits at the FRONT, where
the world is most predictable because the player has not yet changed it, and the
simulation takes over afterwards. KCD2 does the same and so does Hitman's
tutorial level. It also lands on the tile "first hour and tutorial" (partial) and
on the Meridian Test's thirty-minute condition.

The second half of that citation is a production finding rather than a writing
one, and it belongs with the cross-cutting note from the coverage audit: **a tool
for writing against a simulation's variables is a thing a team building this
shape has to build**, and Articy froze on Disco Elysium's script (coverage audit
game 4).

### 3.4 Avoid the automatic fail

CITED (search summaries of the immersive-sim overviews, contrasting Dishonored
with "games that punish the player for getting spotted by an enemy with a game
over screen, an automatic fail state, as seen in games like Splinter Cell
Blacklist"): Dishonored's missions need not be done in a set order and the series
avoids automatic failure.

DERIVED, and it agrees with topic 14 and with `Beat.cs`'s "never the game": a
beat whose failure ends the run forces the writer to guarantee its
preconditions, which is exactly what a simulation cannot promise. A beat whose
failure costs standing does not.

## 4. What a writing lane would need before it could start

Findings, in the order a writer would hit them.

1. **The contradiction list** (2.3): the five things the world can take away.
2. **`Core/Beat.cs` as the exemplar** (3.1), and a ruling on whether every
   authored beat must follow its shape.
3. **The gating vocabulary** (3.2): which simulation predicates a writer may
   condition on, published as a list.
4. **An answer to canon's OPEN 2.** `canon.md` still records it as open:
   "Narrative survival. Whether Tom Novak, Acts I to III and the empire roster
   survive as baseline is decided in Phase 1 planning, along with the
   cast-sketch-versus-built-cards mismatch (Sam and Ada, written at one-street
   scale)." **A writing lane cannot open before that closes**, because it decides
   whether they are writing or rewriting.
5. **A tool** (3.3), and the knowledge that the industry-standard one broke under
   a comparable load.
6. **The content rule as a working constraint, not a review gate.** D18 is
   permanent and voids decisions already taken; `tools/content-gate.py` checks
   part of it; and topic 5 established that the live conversation path has no D18
   enforcement on it at all. A writer needs to know which clauses are enforced by
   a machine and which are on them.

## 5. The specific risk for this project, stated once

The tile "the three acts" (partial): "Three act drafts, their beats and their
endings run in the sim, including the Fall and the audit with a date. Narrative
v2 is phase 3 and unwritten, and **no record committed here says any of it has
been read by somebody playing.**"

DERIVED: there is authored narrative in the simulation that nobody has
experienced. The literature's "story recognition" problem is normally about
whether a player notices an emergent story. Ours is currently the stronger
version: whether anybody notices the AUTHORED one. That is the same finding topic
7 reached from the legibility side and it arrives here from the writing side.

## 6. What could not be established

1. **How the existing acts gate their beats** (3.2). `Core/Campaign.cs`,
   `ActTwo.cs` and `ActThree.cs` were listed and not read. This is the most
   important thing a writing lane would need and it is one session's work to
   answer.
2. **The Shadows of Doubt devblogs themselves**, which are the best practical
   source on this exact problem and are on `colepowered.com`, EGRESS_BLOCKED,
   as recorded in coverage-audit game 5.
3. **Any shipped game that combines a live language model with an authored act
   structure.** I looked. Topic 5's survey found the AI-NPC projects, and none of
   them has an act structure to protect. So the specific combination LEDGER is
   attempting has no precedent I could find, which is either the opportunity or
   the warning.
4. **Whether the academic work is usable.** The UC Santa Cruz and tension-space
   papers name the problems well and I could not read them, so I do not know
   whether they offer techniques or only a vocabulary.
5. **Not covered:** The Sims' wants and fears system, Crusader Kings' event
   chains, and Left 4 Dead's AI Director, all of which are authored pacing over
   emergence and any of which could be the fourth case study a writing lane
   wants.

## 7. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- ResearchGate, "Authoring emergent narrative-based games", https://www.researchgate.net/publication/228361928_Authoring_emergent_narrative-based_games
- UC Santa Cruz EIS, "Open Design Challenges for Interactive Emergent Narrative", https://eis.ucsc.edu/papers/ryanEtAl_OpenDesignChallengesForInteractiveEmergentNarrative.pdf
- arXiv 2004.10808, "Tension Space Analysis for Emergent Narrative", https://arxiv.org/pdf/2004.10808 (EGRESS BLOCKED)
- arXiv 1401.3841, "Narrative Planning: Balancing Plot and Character", https://arxiv.org/pdf/1401.3841 (EGRESS BLOCKED)
- Game Developer, "Emergent Meaning and Narrative in the Digital Space", https://www.gamedeveloper.com/design/emergent-meaning-and-narrative-in-the-digital-space-addressing-tensions-in-games-and-game-like-media (EGRESS BLOCKED)
- TV Tropes, "Emergent Narrative", https://tvtropes.org/pmwiki/pmwiki.php/Main/EmergentNarrative
- Dawnosaur, "The Power of Emergent Stories in Video Games", https://dawnosaur.substack.com/p/the-power-of-emergent-stories-in
- ColePowered Games, "DevBlog 18: Scripted Missions in a Procedural World", http://colepowered.com/shadows-of-doubt-devblog-18-scripted-missions-in-a-procedural-world/ (EGRESS BLOCKED)
- ColePowered itch.io mirror of the same, https://colepowered.itch.io/shadows/devlog/111292/shadows-of-doubt-devblog-18-scripted-missions-in-a-procedural-world
- ModDB, "Shadows of Doubt DevBlog #28: Building the World Through Writing", https://www.moddb.com/games/shadows-of-doubt/news/shadows-of-doubt-devblog-28-building-the-world-through-writing
- PC Gamer, "The uncertain future of games like Deus Ex and Dishonored", https://www.pcgamer.com/the-uncertain-future-of-games-like-deus-ex-and-dishonored/
- TV Tropes, "Immersive Sim", https://tvtropes.org/pmwiki/pmwiki.php/Main/ImmersiveSim

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Core/Beat.cs`, `Core/Homicide.cs`, `Core/Gossip.cs`,
`Core/ContentRule.cs`, the Core file listing (`Campaign.cs`, `ActTwo.cs`,
`ActThree.cs`, listed and not read), `canon.md` (the content rule and OPEN 2),
`ledger-v2/respec/vision-pillars-v2.md`, `production/systems-inventory.json`.
