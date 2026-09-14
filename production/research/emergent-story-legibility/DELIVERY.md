# Topic 7: how emergent-story games make their stories legible

STATUS: SPEC (research delivery). Branch `research/emergent-story-legibility`,
from commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged: no
external page was read in full, and the two GDC talks that are this topic's
primary sources are behind the vault as they were for topic 3. Repository claims
name their file and line.

WHY THIS TOPIC IS HIGHER PRIORITY THAN ITS QUEUE POSITION. Two earlier
deliveries reached it independently. The coverage audit refused Hitman's Mission
Stories, which IO built because their own user research found their densest level
incomprehensible, and flagged that refusing their answer means inheriting their
problem. Topic 3 hit the same wall from the level-design side. This is the third
arrival and the delivery treats it as a live problem rather than a survey.

## 1. The three mechanisms, and we have a version of none of them

### 1.1 Show the working: the itemised reason

CITED (search summaries of the RimWorld Wiki's Mood and Thoughts pages): mood is
a bar in the Needs tab, and beneath it "a representation of all the positive and
negative thoughts held by a colonist", each individual thought listed with its
contribution, summing to the number. "Pawn mood is related to the sum of all the
thoughts a pawn has, so minor penalties can quickly add up", and the interface
makes that visible.

**THIS IS THE THIRD INDEPENDENT ARRIVAL AT THE SAME MECHANISM IN THIS RESEARCH
LANE.** Disco Elysium itemises every modifier with its source before you commit
(coverage audit game 4, A2). Shadow of Mordor catalogues your interactions and
has the orc quote them back (1.2 below). RimWorld lists every thought with its
number. Three games in three different genres, solving legibility the same way,
and the way is: **do not summarise, enumerate.**

Our position, measured in topic 4 of this lane and restated: a grep for a public
`Why(` method across `ledger/Assets/Scripts/Core/*.cs` returns exactly two,
`Core/Homicide.cs:351 PressureWhy` and `Core/YardDepth.cs:330 ProbeWhy`, and both
are instruments that print which term of a number moved, for a verdict file. D12
asks for exactly that pointed at the player and it is not built.

### 1.2 The character quotes the history back at you

CITED (search summaries of the GDC 2018 talk listing "Helping Players Hate (or
Love) Their Nemesis" by Monolith's lead systems designer Chris Hoge, Game
Developer's write-up, and 80.lv's coverage): each orc captain "has a unique name,
title, personality, voice and set of skills"; enemies you kill "can cheat death
and return later with scars and injuries, reflecting your actions"; and **"the
game catalogues your interactions, and orcs reference this to choose dialogue in
future encounters."** The stated design intention was "to create Orcs that you
loved to hate and Orcs you hated to love", by "making Orcs more memorable,
designing exceptional moments, and keeping the player-Orc relationships going".

**This is our measured gap, exactly.** The inventory's tile "recognition and
confrontation" records: "In the shipped build every recognition beat measured sat
below the rung at which anybody comments, 1944 of 1944, so nobody says a word to
you. Typed down: the code runs and the street is silent."

DERIVED, and it is the sharpest comparison available to this project: Shadow of
Mordor's entire reputation rests on one thing our system does and one thing it
does not. It remembers, and so do we. **It says so, and we do not.** A memory
nobody voices is indistinguishable from no memory, and 1944 out of 1944 is that
statement with a denominator.

The three components Mordor pairs with the callback are worth separating,
because we have them in different states:

| Mordor | Ours |
|---|---|
| unique name | `Core/PlayerIdentity.cs` has the reverse, an address ladder for what the town calls YOU: "the new owner", Novak, Tom, Toma. The town's own people are named by a generator the inventory says "supplies names, not people" |
| unique voice | 19 cast voices, and the tile records that no committed file says anybody has heard one in a build |
| visible scars from your actions | the appearance finding from the coverage audit, recommended four times over and not built |
| catalogued interactions quoted back | the 1944 of 1944 |

### 1.3 The legible artefact: a thing the player can look at afterwards

CITED (search summaries of the Dwarf Fortress Wiki's Legends and Utilities pages,
and the LegendsViewer and LegendsViewer-Next repositories): Legends Viewer "loads
legends exported from Dwarf Fortress in a much more usable format than the
Legends mode of the game itself"; to "make something intelligible from the
exported data, players need a third party tool"; and the alternatives offer
"graphs, filtering, sorting, and hyperlinks", with a newer tool built for the
Steam release.

**DWARF FORTRESS IS THIS TOPIC'S CAUTIONARY CASE AND IT IS A SEVERE ONE.** It has
the deepest simulated history any game has ever generated. Its players cannot
read it. The community wrote, and keeps rewriting, external software to make the
game's own history legible, and the wiki recommends doing so.

DERIVED: a simulation that GENERATES history and a game that TELLS you about it
are different products, and the first does not imply the second. LEDGER's moat
is social memory, consequence persistence and information, scored 93, 95 and 90
against a best-in-class of 60, 85 and 65. Dwarf Fortress would score higher than
any of those on generation and would fail the Meridian Test's third condition,
because nobody describes a thing as alive that they cannot follow.

## 2. The tension nobody in this repository has written down

RimWorld's designer chose simple graphics ON PURPOSE, for narrative reasons.

CITED (search summaries of "The Story Generator: A Game Design Analysis of
RimWorld" and the Medium piece on its AI storytellers): "Tynan Sylvester
considers simple graphics an asset for the narrative purpose of the game,
justifying it with the idea of Apophenia, a human tendency to see and perceive
connections and meaning between unrelated things. The minimal game
representation is suitable for players to make up events and stories in their
head."

DERIVED, and I think it is the most useful thing in this file: **photorealism
costs apophenia, and D8 buys photorealism.**

A drawn square with a name invites the player to imagine a face, a history and a
motive, and the player's imagination does the authoring for free. A photoreal
face does not invite that, because it has already specified the face. The
player's projection has less room to work, and everything the projection would
have supplied has to be supplied by the game instead.

This is not an argument against D8 and I am not making one. D8 is approved,
reasoned and instrumented, and the visual bar is the entry condition for the
Meridian Test's first clause. It IS a constraint that follows from D8 and has not
been stated anywhere:

**A photoreal game cannot rely on the player to make the story. It has to say
more than a stylised game would, not less.**

Which lands on 1.2. Mordor is the proof that this is achievable, and it is not a
coincidence that Mordor is the photoreal one of the three.

## 3. What follows for LEDGER, as findings

Not proposals. Each one is a thing the three games do that our own measurements
say we do not.

1. **Enumerate, do not summarise.** Three games, three genres, one mechanism,
   and D12 already asks for it. The audit already recommended it once from Disco
   Elysium. This is the second recommendation and the third source.
2. **The callback is the whole of Mordor.** Our 1944 of 1944 is the same system
   with the last step missing, and the last step is the one players talk about.
3. **A memory needs an artefact you can read afterwards, and building it is a
   separate job from building the memory.** Dwarf Fortress proves the memory does
   not imply the artefact. D12 already specifies ours (the Ledger, tagged
   witnessed, heard or deduced) and queue 037 is the unbuilt spec row. This is
   the third of my deliveries to land on queue 037.
4. **Photorealism raises the legibility bar rather than lowering it** (section
   2), which is a cost of a decision already taken and should be known rather
   than discovered.

## 4. What could not be established

1. **Both GDC talks in full.** "Helping Players Hate (or Love) Their Nemesis" is
   behind the GDC Vault, as the Hitman talks were in topic 3. Everything about
   Mordor's design principles is the search channel's summary of a page
   describing the talk. The specific techniques for "designing exceptional
   moments" are what I most want and did not get.
2. **Whether Mordor's callbacks are authored templates or generated**, which
   matters a great deal for what they would cost us. Not established.
3. **How many distinct orc lines exist**, the volume question. Not established.
4. **RimWorld's storyteller internals.** The sources describe pacing by
   personality and I have no mechanism.
5. **Whether any Dwarf Fortress player actually reads Legends in-game.** The
   evidence is the existence and maintenance of external tools, which is strong
   circumstantial evidence and not a measurement of use.
6. **Not covered:** Crusader Kings, which is the obvious fourth case and where
   the event-log-as-narrative is most developed; Caves of Qud; and the whole
   question of how a game SUMMARISES a session, which is adjacent and different.

## 5. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- GDC Vault listing, "Helping Players Hate (or Love) Their Nemesis", https://www.gdcvault.com/play/1025150/Helping-Players-Hate-(or-Love)
- GDC, "Attend GDC 2018 for a behind-the-scenes look at Shadow of War's Nemesis system!", https://gdconf.com/article/attend-gdc-2018-for-a-behind-the-scenes-look-at-shadow-of-war-s-nemesis-system/
- Game Developer, "Video: How the nemesis system in Shadow of War was designed", https://www.gamedeveloper.com/design/video-how-the-nemesis-system-in-i-shadow-of-war-i-was-designed (EGRESS BLOCKED)
- 80.lv, "GDC: Helping Players Hate or Love Their Nemesis", https://80.lv/articles/gdc-helping-players-hate-or-love-their-nemesis (EGRESS BLOCKED)
- Medium (Niklas Eckstein), "How the Nemesis System Creates Stories", https://medium.com/@niklaseckstein/how-the-nemesis-system-creates-stories-d26754b30d2e
- RimWorld Wiki, "Mood", https://rimworldwiki.com/wiki/Mood
- RimWorld Wiki, "Thoughts", https://rimworldwiki.com/wiki/Thoughts
- RimWorld Wiki, "Mental break", https://rimworldwiki.com/wiki/Mental_break
- Substack (Zayd Qazi), "The Story Generator: A Game Design Analysis of RimWorld", https://zaydqazi.substack.com/p/the-story-generator-a-game-design
- Medium (C-N), "Algorithmic Authors: RimWorld's AI Storytellers as Agents of Literary Genre", https://medium.com/@coyega1328/algorithmic-authors-rimworlds-ai-storytellers-as-agents-of-literary-genre-eff70ea4560c
- Game Developer, "Rimworld, Dwarf Fortress, and procedurally generated story telling", https://www.gamedeveloper.com/design/rimworld-dwarf-fortress-and-procedurally-generated-story-telling (EGRESS BLOCKED)
- Dwarf Fortress Wiki, "DF2014:Legends", https://dwarffortresswiki.org/index.php/DF2014:Legends
- Dwarf Fortress Wiki, "DF2014:Utilities", https://www.dwarffortresswiki.org/index.php/DF2014:Utilities
- Dwarf Fortress Wiki, "Utility:Legends viewer", https://dwarffortresswiki.org/index.php/Utility:Legends_viewer
- GitHub, "Kromtec/LegendsViewer", https://github.com/Kromtec/LegendsViewer
- GitHub, "Kromtec/LegendsViewer-Next", https://github.com/Kromtec/LegendsViewer-Next

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`, `ledger/Assets/Scripts/Core/PlayerIdentity.cs`,
`Core/Homicide.cs`, `Core/YardDepth.cs`,
`ledger-v2/respec/decision-register/D8-visual-bar.md` and
`D12-information-surfaces.md`, `ledger-v2/respec/vision-pillars-v2.md`,
and this lane's own `production/research/coverage-audit-disco-elysium/` and
`coverage-audit-hitman/` on their branches.
