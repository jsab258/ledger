# Coverage audit 4 of 5: Disco Elysium

STATUS: SPEC (research delivery). Branch `research/coverage-audit-disco-elysium`,
from commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No tile is proposed, no queue item
filed, the inventory is not touched, and the decision is Jafar's.

## 0. How to read this file

Columns, claim labels and the word collision on "absent" are defined in
`production/research/coverage-audit-kcd2/DELIVERY.md` section 0. This file adds
one value to the recommendation set, and it is not a fudge:

- **BENCHMARK.** A fact about Disco Elysium that is not a system we could adopt
  or refuse, but a measured number the project should be held against. Four
  entries carry it, all in section E, and none of them is a recommendation.

SOURCING LIMIT unchanged: every external citation is the search channel's
summary of a named page, not a page read in full. One search returned
`Web search error: unavailable` and answered from the model's own memory
instead; that answer was DISCARDED and the search re-run, and nothing in this
file rests on it. Repository claims name their file and line.

D24 still does not exist in this checkout. Quotations from repository files
predating the formatting law have had em-dashes replaced by commas and italics
dropped.

## 1. Counts, and why the IN column is short

**26 systems** enumerated, mapped against the 91 tiles.

| Column | Count |
|---|---|
| COVERED | 5 |
| PARTIAL | 1 |
| ABSENT | 15 |
| RULED OUT | 5 |
| **Total** | **26** |

Of the 15 absent: **2 IN, 7 OUT, 2 ASK, 4 BENCHMARK.**

TWO INs IS THE LOWEST OF THE FOUR GAMES SO FAR and it is the right answer rather
than a thin pass. Disco Elysium is a dialogue-menu role-playing game whose
machinery is almost entirely character progression: 24 skills, four attributes,
skill points, twelve thought slots, clothing that grants stat bonuses. D11 rules
all of that out in one sentence, and it rules it out for a reason this game
happens to illustrate perfectly: in Disco Elysium the interesting question
genuinely is "what have I unlocked", because the protagonist is the subject. In
LEDGER the subject is the town.

So five of the 26 are RULED OUT by a single record, which is the highest
ruled-out rate in the audit, and most of the rest is architecture that assumes a
menu rather than a spoken conversation.

The two INs are worth more than their count. Both are about LEGIBILITY, which is
the brief's stated reason for including this game, and one of them answers a
clause of D12 that is currently unanswerable.

## 2. The finding

**D12 asks for a surface this project already knows how to build and has only
ever pointed at itself.**

D12's legibility clause, quoting the record: "when a claim is believed or
doubted, the NPC's actual relevant memory surfaces as the reason", and D11 gives
the stakes: "A judgement the player cannot trace to something that actually
happened reads as the game deciding arbitrarily, which is the psychic-guard
failure in a new costume."

Disco Elysium's answer to that problem is the most copied thing about it, and it
is not the writing: BEFORE you commit to a check, the game shows you the whole
sum. The skill, every modifier with its source, the difficulty, and the
resulting odds. CITED (search summaries of gamepressure, "Skill checks", and
Gamers.Wiki, "How to Pass Skill Checks"): the result is skill level plus
modifiers plus a two-dice roll against a set difficulty, and modifiers come from
items, clothing, stimulants, thoughts and previous choices, each named.

MEASURED HERE THIS SESSION: the project already has that idiom and has never
pointed it at a player. `grep` for a public `Why(` method across
`ledger/Assets/Scripts/Core/*.cs` returns exactly two:
`Core/Homicide.cs:351 PressureWhy` and `Core/YardDepth.cs:330 ProbeWhy`. Both
are instruments. `PressureWhy`'s own comment says what it is for: "The
pressure's parts, one compact token per sample, for the daily series the
heat-fade question needs", written because "`homInquiry=Manhunt` at the killing
against `inquiry=Procedure` at the end says heat FELL; nothing recorded says
WHICH TERM fell". That is exactly the reasoning D12 applies to the player, and
the code applies it to the verdict file.

Everything needed is already there. `Core/Gossip.cs:957 DcResult` carries an
`Outcome` and a `Message` but no breakdown of terms. `Core/Gossip.cs:970 Lead`
already models the player-facing shape of the information layer: "who is
carrying talk about them, how sure they are, where it came from, and whether it
touches the hidden life."

DERIVED: the gap between `PressureWhy` and what D12 asks for is a caller and a
surface, not a model. Disco Elysium is the evidence that such a surface makes a
game more legible rather than less atmospheric, at a scale of information far
beyond ours.

## 3. The mapping

### A. The check system (7)

**A1. Skill level plus modifiers plus two six-sided dice against a set
difficulty.** CITED (search summary of gamepressure, "Skill checks").
**ABSENT.** **OUT.** Pillar 3 is that consequence is deterministic: "Every
outcome the player feels is decided in C#-style deterministic Core". A visible
random roll is a different contract with the player, and our version of the
uncertainty is better placed anyway: the uncertainty in LEDGER is what somebody
saw and what they believe, not whether a die came up six.

**A2. Every modifier is itemised, with its source, and shown before you
commit.** CITED (same, and Gamers.Wiki).
**ABSENT.** **IN, and section 2 is the whole argument.** What it buys: D12's
legibility clause becomes answerable, and the moat becomes something the player
can reason about rather than something that happens to them. What it costs: a
caller and a surface, because `PressureWhy` proves the idiom is already in the
project's hands.

**A3. White checks can be retried, but only after the relevant skill rises or a
thought is researched.** CITED (search summary of gamepressure).
**ABSENT.** **ASK**, with A4.

**A4. Red checks get one attempt, ever, and the game tells you which is
which.** CITED (same), together with the sources' own note that "It is not
always a bad thing to fail a red check".
**ABSENT.** **ASK, and it belongs with the save question from game 1.** The
transferable idea is not the colour, it is that the game says BEFORE you act
whether this is recoverable. That is directly relevant to the save-scumming
question raised in game 1 (F1 to F3 there), because a player who knows a moment
is permanent is being asked to accept it rather than tricked into it. In a game
whose pillar is that nothing is ever wiped, telling the player which acts are
about to become permanent knowledge is either the kindest thing in the design or
a cheat that drains the tension, and which of those it is, is a feel judgement.

**A5. Passive checks resolve with no roll and no prompt, at skill plus
modifiers plus six.** CITED (search summary of gamepressure).
**COVERED** in substance, and ours is the deeper version: our whole perception
layer is a passive check the player never sees resolve, and
`Core/Observation.cs` documents the deliberate silence of it in the `Awareness`
enum.

**A6. Double six always wins and double one always loses.** CITED (same).
**ABSENT.** **OUT**, with A1.

**A7. Failing is authored: a failed check often produces different content
rather than less.** CITED (search summary of gamepressure and the wiki: "It is
not always a bad thing to fail a red check").
**ABSENT.** **IN, and it is cheap in code and expensive in writing, which is the
right way round for this project.** Our tile "the player's claims and lies"
records the exact failure this fixes: "in 90 of 90 caught lies not one spoken
line differed", and "Truth and silence both end at suspicion 0.060, so honesty
pays nothing". A failed intimidation that produces a scene, and a memory of you
having tried, is worth more than a refusal, and it feeds memory and consequence
directly. Note that the cost lands on the dialogue banks rather than on Core,
which is the content pillar's own unit of work.

### B. Character and progression (5)

**B1. 24 skills, each an internal voice with a personality, which interrupt
conversations with their own view.** CITED (search summary of Gamers.Wiki, "All
24 Voices and Attributes"): "during dialogue, investigation, and key decisions,
individual skills interrupt with distinct perspectives, facts, instincts, or
arguments, changing what you notice and which responses become available."
**RULED OUT** by D11 for the skills half. For the VOICES half: **OUT**, and the
brief's own definition is the argument. This is Disco Elysium's identity, not a
component. A game with an inner chorus is a game about a man arguing with
himself; ours is about a town forming an opinion of a man, and the attention the
chorus would take is attention taken from the town. Taking it would be copying
rather than designing.

**B2. Four attributes grouping the skills.** CITED (same). **RULED OUT** by D11.

**B3. The Thought Cabinet: twelve slots, thoughts acquired by interacting with
the world, a research phase lasting from thirty minutes to over twenty hours of
in-game time with temporary penalties during it, permanent effects after.**
CITED (search summaries of the Disco Elysium wiki, "Thought Cabinet", and
Gamers.Wiki).
**RULED OUT** by D11. Recorded in full because it is the most admired mechanic
in the game and somebody will propose it: it is a progression system with a
timer, and D11's line holds against it exactly as written.

**B4. Skill points spent on raising skills.** CITED (same). **RULED OUT** by
D11.

**B5. Health and Morale as two separate damage tracks, either of which can end
the game, healable mid-conversation.** CITED (search summary of the Disco
Elysium wiki, "Skills", and Bonus Action).
**PARTIAL** for the first track, tile "injury and healing" (partial),
`Core/Harm.cs`. **OUT** for the second: a morale track is the protagonist's
interior modelled as a resource, which is the same subject-of-the-game argument
as B1.

### C. Clothing (2)

**C1. Clothes grant bonuses and penalties to specific skills.** CITED (search
summary of the Disco Elysium wiki, "Clothing").
**ABSENT.** **OUT, and it is the fourth confirmation of the cross-game finding
in the one form we cannot use.** Games 1, 2 and 3 all found clothing carrying
identity; this one has clothing carrying statistics, which D11 forbids. Worth
recording precisely because it shows the finding is about what clothes MEAN and
not about a bonus: in the three games where clothing worked as perception it was
about who people thought you were, and here, where it works as a number, it is
the one version with nothing for us.

**C2. You can leave a conversation, change into a better outfit for the coming
check, and come back.** CITED (same, and a Steam guide on optimising clothing).
**ABSENT.** **OUT, and the contrast is instructive.** Disco Elysium's own
players treat this as an optimisation, which it is, because nobody in the world
sees you change. In LEDGER changing your clothes is an observable act that
somebody may remember, which is games 1 to 3's finding again: the same verb
costs nothing there and something here, and that difference is the moat.

### D. Information and legibility (5)

**D1. The Journal: tasks and sub-tasks, updated by dialogue, as the thing that
holds the case together.** CITED (search summary of joybit, "Disco Elysium for
First-Timers").
**COVERED** by D12 and the tile "the Ledger notebook" (partial), whose note
records that D12's journal, "one tagged entry per person and per event,
witnessed, heard or deduced, is not in it" and that queue 037 is the unbuilt
spec row.
NOT A RECOMMENDATION, BUT THE STRONGEST EVIDENCE IN THIS AUDIT FOR THAT QUEUE
ITEM. The brief asked how a game holds hundreds of pieces of information
legibly, and Disco Elysium's real answer is not the journal: it is that THE
PLAYER IS NEVER ASKED TO RECALL ANYTHING. The relevant fact is spoken to them at
the moment it becomes relevant, by a skill, in context. D12 already specifies
our version of exactly that ("Conversations show the Ledger page for the person
you are talking to"), and it is not built. This game is the proof that the
approach scales to a million words.

**D2. Skills interrupting dialogue as the delivery mechanism for commentary.**
CITED (search summary of Gamers.Wiki). **ABSENT.** **OUT**, with B1.

**D3. World knowledge delivered by a skill volunteering it in context rather
than by an encyclopedia the player opens.** CITED (same).
**COVERED** in shape by the tile "the town's own voice" (exists), which builds
what you overhear around the rumour's own summary rather than picking a written
line, and reported 540 of 3240 lines pointing at something the player did.

**D4. Thoughts acquired by interacting with the world, representing concepts
the detective internalises.** CITED (search summary of the Disco Elysium wiki).
**RULED OUT** by D11.

**D5. Time advances through action and dialogue rather than on a clock.**
CITED (search summary of Gamers.Wiki on the Thought Cabinet: "The timer advances
while you play").
**ABSENT.** **OUT, and firmly.** Pillar 1 propagates gossip through schedule
intersections, which requires everybody to be somewhere at a time whether or not
the player is doing anything. An action-advanced clock deletes the schedule, and
the schedule is the mechanism the moat runs on. This is the one Disco Elysium
idea that would do structural damage.

### E. Production and scale (4), all BENCHMARKS and not recommendations

These four are the reason this game is worth auditing for a project whose second
pillar is spoken conversation. None is a recommendation.

**E1. A script of approximately one million words.** CITED (search summaries of
ClutchPoints and Notebookcheck).
**BENCHMARK.** Our tile "dialogue banks" (partial) reports two banks plus a bark
generator, and the no-repetition blind test is phase 3's gate. One million words
is the number the authored-content pillar is implicitly being compared against
by anybody who has played this game.

**E2. Full voice acting in The Final Cut took about 14 months, with three
full-time VO directors and dozens of actors.** CITED (search summaries of PSU,
"It Took ZA/UM 14 Months To Record Over A Million Words", and PC Gamer).
**BENCHMARK, and it is the vindication of pillar 2.** Fourteen months of
directed studio recording by a funded team is the cost of voicing a million
words the human way. It is not payable here by anybody, at any budget, ever.
That is the argument for a live voice pipeline stated as a measurement rather
than as a preference, and it belongs in queue topic 1 and topic 20.

**E3. One narrator, Lenval Brown, recorded 350,000 words over eight months,
about a third of the game.** CITED (search summary of PC Gamer, "we talk to
Disco Elysium's incredible narrator, who recorded 350,000 words of dialogue").
**BENCHMARK.** DISCREPANCY RECORDED RATHER THAN RESOLVED: the PC Gamer headline
says 350,000 WORDS and the PSU piece relays 350,000 LINES. Those differ by more
than an order of magnitude. I could not reach either page to check, so the
figure is reported as contested, and anybody using it should resolve it first.

**E4. Articy, the industry-standard tool for non-linear narrative, slowed
dramatically and then froze under the volume of the script.** CITED (search
summary of ixbt.games, "Disco Elysium Hit a Technical Limit Due to the Volume
of the Script", and the Articy showcase page).
**BENCHMARK, and the one with a risk attached to it.** A funded studio using the
professional tool for exactly this job lost editorial control of its own script:
the source's phrasing is that "there was so much text that control over the
material began to be lost, and editing turned into a constant struggle". This
project intends more authored dialogue than it currently has any tooling for.
Flagged to CROSS-CUTTING as a research topic that is not in the queue.

### F. The world (3)

**F1. Martinaise: one small, dense, hand-authored district, re-walked
constantly.** CITED (general). **COVERED** by pillar 6, as shape rather than
system. Worth recording that the most information-dense role-playing game ever
written takes place in an area a player crosses in under two minutes.

**F2. No combat outside scripted checks.** CITED (general).
**ABSENT.** **OUT** as a design choice to copy: D4 already sequences combat
before driving, and `Core/Combat.cs` exists. Noted because it is evidence that a
crime game can be almost entirely conversation, which is the shape pillar 2
points at.

**F3. Sleeping at the hostel ends the day.** CITED (general).
**COVERED**, tile "sleep and the day boundary" (typed absent). Second
confirmation of the recommendation made in game 1 (F4 there).

## 4. What could not be established

1. **The 350,000 figure** (E3), words against lines, is contested between two
   sources and unresolved.
2. **ZA/UM's team size** during development could not be established, which
   matters because E2's fourteen months is only meaningful beside a headcount.
3. **Whether `PressureWhy`'s output ever reaches a player-facing surface.** I
   established that `Game/GameController.cs:444` assigns it to
   `e.InquiryAbout` and that `Game/SimDirector.cs` writes it into verdict
   strings. I did NOT trace `InquiryAbout` to a screen, so section 2's claim is
   bounded to: the idiom exists, both Core uses are documented as instruments,
   and no itemised breakdown of a social judgement reaches the player that I
   found.
4. **The exact contents of the Journal UI** and how it groups hundreds of
   threads; the sources describe that it does, not how.
5. **Not enumerated.** The political alignment tracking, the Final Cut's added
   quests, the ending structure, the art pipeline (which is oil-painted and
   irrelevant to a photoreal target), the music, and the tribunal set piece.

## 5. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- gamepressure, "Disco Elysium: Skill checks", https://www.gamepressure.com/disco-elysium/skill-tests/zfe3e2
- gamepressure, "Disco Elysium: Thought Cabinet", https://guides.gamepressure.com/disco-elysium/guide.asp?ID=58339
- Disco Elysium Wiki (wiki.gg), "Skills", https://discoelysium.wiki.gg/wiki/Skills
- Disco Elysium Wiki (wiki.gg), "Clothing", https://discoelysium.wiki.gg/wiki/Clothing
- Disco Elysium Wiki (wiki.gg), "Thought Cabinet", https://discoelysium.wiki.gg/wiki/Thought_Cabinet
- Disco Elysium Wiki (Fandom), "Thought Cabinet", https://discoelysium.fandom.com/wiki/Thought_Cabinet
- Disco Elysium Wiki (Fandom), "Voice Actors", https://discoelysium.fandom.com/wiki/Voice_Actors
- Gamers.Wiki, "How to Pass Skill Checks in Disco Elysium: White, Red, and Dice Rolls", https://gamers.wiki/en/games/disco-elysium/guides/how-to-pass-skill-checks-in-disco-elysium-white-red-and-dice-rolls
- Gamers.Wiki, "Disco Elysium Skills Guide: All 24 Voices and Attributes", https://gamers.wiki/en/games/disco-elysium/guides/disco-elysium-skills-guide-all-24-voices-and-attributes
- Gamers.Wiki, "Thought Cabinet Guide: Slots, Thoughts and Effects", https://gamers.wiki/en/games/disco-elysium/guides/disco-elysium-thought-cabinet-guide-slots-thoughts-and-effects
- Bonus Action, "Disco Elysium Basics: How Archetypes, Skills, Thoughts, and Clothes Work", https://bonus-action.com/guides/disco-elysium-basics-archetypes-clothes-skills-thoughts/
- joybit, "Disco Elysium for First-Timers: Tips I Wish I Knew", https://joybit.co.uk/disco-elysium/
- ClutchPoints, "Disco Elysium Final Cut edition features one million words of spoken dialogue", https://clutchpoints.com/gaming/disco-elysium-final-cut-edition-features-one-million-words-of-spoken-dialogue
- PlayStation Universe, "It Took ZA/UM 14 Months To Record Over A Million Words Of Dialogue", https://www.psu.com/news/it-took-za-um-14-months-to-record-over-a-million-words-of-dialogue-for-disco-elysium-the-final-cut-on-ps5-and-ps4/
- PC Gamer, "We talk to Disco Elysium's incredible narrator, who recorded 350,000 words of dialogue and has never acted before", https://www.pcgamer.com/we-talk-to-disco-elysiums-incredible-narrator-who-recorded-350000-words-of-dialogue-and-has-never-acted-before/
- PC Gamer, "The voice acting in Disco Elysium: The Final Cut makes the best RPG on PC even better", https://www.pcgamer.com/the-voice-acting-in-disco-elysium-the-final-cut-makes-the-best-rpg-on-pc-even-better/
- ixbt.games, "Disco Elysium Hit a Technical Limit Due to the Volume of the Script", https://ixbt.games/en/news/2026/01/16/disco-elysium-uperlas-v-texniceskii-predel-iz-za-obieema-scenariia.html
- Articy showcase, "Disco Elysium", https://www.articy.com/en/showcase/disco-elysium/
- Notebookcheck, "1 million words of text voice acted", https://www.notebookcheck.net/1-million-words-of-text-voice-acted-massive-RPG-Disco-Elysium-gets-Director-s-Cut-with-full-voice-acting-on-March-30th.529930.0.html

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`,
`ledger-v2/respec/decision-register/D11-player-progression.md` and
`D12-information-surfaces.md`, `ledger-v2/respec/vision-pillars-v2.md`,
`ledger/Assets/Scripts/Core/Gossip.cs`, `Core/Homicide.cs`,
`Core/Observation.cs`, `Game/GameController.cs`, `Game/SimDirector.cs`.
