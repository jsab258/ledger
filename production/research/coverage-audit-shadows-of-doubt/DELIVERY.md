# Coverage audit 5 of 5: Shadows of Doubt

STATUS: SPEC (research delivery). Branch
`research/coverage-audit-shadows-of-doubt`, from commit `074f85b`. Written
2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No tile is proposed, no queue item
filed, the inventory is not touched, and the decision is Jafar's.

## 0. Why this game, argued

The brief left game 5 open: one crime or investigation game, argued for.

I considered L.A. Noire (period crime, interrogation as a resolved system),
Pathologic 2 (a small town, a clock you cannot stop, permanent death) and Return
of the Obra Dinn, and chose Shadows of Doubt (ColePowered Games, 2023) for one
reason that none of the others has:

**IT IS THE ONLY SHIPPED GAME THAT HAS ACTUALLY BUILT THE THING LEDGER IS
BUILDING.** A whole town where every inhabitant is an individual with a name, an
address, a job, a routine and a persistent record of what they have seen, played
as crime. Every other game in this audit approximates one part of that with
authored content. This one simulates it, and it shipped, and it was reviewed.

That makes it the only available EVIDENCE about what happens when you do this,
as opposed to argument. Its two best ideas are cheap and we do not have them.
Its architecture answers a question the project has open. And its failures are
our risk register, written by people who found them the expensive way.

The other four games told us what to take. This one tells us what it costs to be
right about the thing we have already decided.

## 1. How to read this file

Columns, claim labels and the word collision on "absent" are in
`production/research/coverage-audit-kcd2/DELIVERY.md` section 0. The BENCHMARK
value introduced in game 4 is used again here, for the same reason: two entries
are architectural facts to be held against rather than systems to adopt.

SOURCING LIMIT, and it bites harder on this game than on any other. The
developer wrote a long public devblog series which is the primary source for
everything in section A, and `colepowered.com` is EGRESS BLOCKED, measured this
session. One search returned `Web search error: unavailable` and answered from
the model's own memory; that answer was discarded and the search re-run. So
every claim below is the search channel's summary of a named page, and the
devblog claims are summaries of a developer's own writing rather than the
writing. Repository claims name their file and line.

D24 still does not exist in this checkout. Quotations from repository files
predating the formatting law have had em-dashes replaced by commas and italics
dropped.

## 2. Counts

**23 systems** enumerated, mapped against the 91 tiles.

| Column | Count |
|---|---|
| COVERED | 6 |
| PARTIAL | 1 |
| ABSENT | 16 |
| RULED OUT | 0 |
| **Total** | **23** |

Of the 16 absent: **7 IN, 5 OUT, 2 ASK, 2 BENCHMARK.**

Five of the seven INs are riders: four on one recommendation (B1), and one was
already made in game 2. **Two distinct new things are recommended.**

Zero ruled out by a decision record, which is itself a small finding: nothing in
this game touches alcohol, gambling, children, player progression or any other
clause the register has spoken on. It is the only game in the audit that
collides with none of our rules, which is another way of saying it is the
closest to us.

## 3. The finding, and it is a warning

This is the most important paragraph in the whole audit and it is not about a
system we should build.

**Shadows of Doubt is what happens when you simulate a town and let procedural
generation write its contents, and reviewers describe the result in terms that
match pillar 4's warning almost word for word.**

CITED (search summary of Gamecritics, "Shadows Of Doubt Review", and Metacritic
and OpenCritic aggregates): the procedurally generated cities and cases "instead
lead to very repetitive generated cities, cases, and conversations", and
specifically "Literally every office explored had an identically written email
about a gambling ring, and each apartment had the same letters to old friends
with indistinguishable text". And CITED (same): "Once you do a couple of cases,
you pretty much only need a couple of names and fingerprints and the case is
closed."

Pillar 4, verbatim: "Content is made the way a studio makes it: per piece, with
a spec, an author agent and a verifier. **No procedural filler without an
authoring pass and verification.** The planning unit is verified pieces per
week." D18 restates the same discipline for content. `Core/Occupancy.cs` states
it a third time, in its own words, about a lit window: "A random lit/unlit
pattern would look better and mean nothing, and this project has a name for
that, a system built, plausible, and saying nothing."

DERIVED: this project arrived at the right rule and has, until now, held it on
argument. Shadows of Doubt is the empirical case. A simulated town whose
contents are generated does not read as a town; it reads as a template, and it
reads that way to REVIEWERS and not only to the people who built it. The two
failures compound in a way that matters for us specifically: identical
documents make the world feel false, AND they collapse the investigation into a
rote procedure, because if every apartment holds the same letter then the only
information that ever matters is the small structured part (a name, a
fingerprint). LEDGER's moat is information. A moat made of interchangeable
information is a moat with a dominant strategy.

The recommendation that follows is not a system. It is that pillar 4 should be
treated as the load-bearing wall it is, and that the tile "the cast" (partial),
whose note reads "the population generator supplies names, not people, so most
of the town is a body with a schedule", is describing the first three feet of
the same road.

## 4. The mapping

### A. The simulated city (7)

**A1. Every citizen has a name, an apartment, a job, a daily routine,
preferences, and people they interact with.** CITED (search summary of the Steam
store page and TechRaptor's preview).
**COVERED**, tiles "daily routines" (exists), "the town layout" (exists) and
"the cast" (partial). This is the same design, reached independently.

**A2. Hundreds of citizens.** CITED (search summary of ModDB's mirror of DevBlog
8: "the task of simulating 100s of individual citizens, all going about their
daily routines").
**PARTIAL**, tile "the cast" (partial), which names 30 to 50 residents at phase
2, and "the crowd you see" (partial), which read 65 walkers.

**A3. The day is PRE-COMPUTED, not simulated live: 10 to 15 seconds of
calculation before each day begins, scaling with population.** CITED (search
summary of ModDB's mirror of DevBlog 8): "the game requires a brief period of
calculation time before the start of each day (typically no more than 10-15
seconds depending on the population count)", because "Simulating 100s of
citizens would be a hugely intensive task for a system to handle in real time,
which is why the developer chose not to handle it in real-time."
**ABSENT.** **BENCHMARK, and an open architectural question rather than a
recommendation.** LEDGER's headless sim runs live, and the last landed run
covered seventeen days. Nothing about that is wrong today. But the shipped
configuration this project is heading for puts a dense Unreal street, a local
LLM and a text-to-speech model on one machine at the same time, and queue topics
2 and 17 exist precisely because nobody has yet said what that costs. The only
comparable shipped game looked at the same problem and moved the simulation off
the frame budget entirely. That is worth knowing before those two topics are
written, and it is a studio question and not Jafar's.

**A4. The AI update rate scales with proximity to what is on screen, making the
cost of 95 percent of citizens insignificant.** CITED (same source).
**ABSENT.** **BENCHMARK**, with A3. Level-of-detail on AI rather than on meshes,
and the 95 percent figure is the developer's own.

**A5. Sightings are produced by a global check that loops over travelling
citizens and asks whether they can see one another.** CITED (search summary of
DevBlog 8 via ModDB).
**COVERED**, and ours is considerably finer. `Core/Observation.cs` fills seven
slots independently, `Core/Perception.cs` resolves five identification rungs
against metres, light, facing and familiarity. Their check answers whether; ours
answers what.

**A6. Citizens can see out of their own lit windows into the street and into
windows across it.** CITED (search summary of DevBlog 8 via ModDB): "Citizens
can also see into windows across the street adjacent to their own if the light
is on, this means in certain circumstances you may wish to question the
occupants of an apartment in an adjacent building."
**ABSENT.** **IN, and it is a system we already own in one direction only.**
`Core/Occupancy.cs` is titled "WHO IS IN, AT AN HOUR, and therefore which
windows are lit", and its comment argues the point in the project's own terms:
a lit window "is the information pillar rather than decoration". That is the
window carrying information TO the player. Nothing carries information the other
way: measured this session, `Core/Perception.cs` and `Core/Observation.cs` have
no hit for a window or an indoor observer, and the one `window` in
`Observation.cs:469` is a metaphor.
So the man in the lit window above the shop is currently a light. Making him a
witness costs a position and a facing on somebody the occupancy model has
already placed, and it buys the single most characteristic witness a British
terraced street has: the neighbour who was in, with the light on, and saw you
come back at two.

**A7. Citizens store memories of what and who they saw, so they can be
questioned later.** CITED (search summary of DevBlog 8 via ModDB): "Citizens
need to record what/who they've seen in case they are relevant to one of your
investigations and you decide to question them."
**COVERED**, tile "permanent memory" (partial). Ours is per-person, append-only
and indelible for a killing; theirs is a recording for questioning. Same idea,
and the tile's open conflict (pruning at 600 events against canon's "nothing is
ever wiped", queue 115) is unaffected by this game.

### B. The detective toolkit (7)

**B1. Fingerprints, unique per NPC, read with a scanner.** CITED (search
summaries of HackerNoon's investigation guide and Steam community discussion):
"Every NPC in the game has a unique fingerprint."
**ABSENT.** **IN, as one recommendation covering B1, B2, B3, B6 and B7: what you
leave at a scene, and what a scene leaves on you.**
The project already has the second half and not the first. `Core/Traces.cs`
carries blood ON THE PLAYER and provenance ON AN OBJECT, and its header names
the intended reader: the aftermath has to be "something people can SEE and
something Ellis can FOLLOW". Mara Ellis is canon's detective. What is missing is
the scene itself: the thing you touched, the print in the mud by the yard gate,
the object with your history on it left where it fell.
The period is unusually good for this and that is not decoration, it is the
design space. In Britain between 1988 and 1992, fingerprints are the mature
forensic technology and everything else is new or absent: no DNA database, no
ubiquitous CCTV, no mobile phone records, and `canon.md` already rules CCTV rare
with tape recycled weekly. So a scene in Meridian yields prints, a heel print, a
dropped object and people's memories, and nothing else. That is a smaller, more
legible evidence set than a modern detective game can have, and small and
legible is what pillar 6 asks for.
Against the D24 test: it feeds consequence directly (the case against you) and
it is the half of `Traces` that was always implied and never built.

**B2. Footprints giving shoe size and type.** CITED (search summary of
HackerNoon). **ABSENT.** **IN as a rider on B1.**

**B3. Blood and DNA at the scene.** CITED (same). **ABSENT.** **IN as a rider on
B1 for the blood; OUT for DNA**, which is period-wrong as a routine tool in 1990
and would need a decision of its own if anybody wanted it as a rare plot device.

**B4. Some evidence, notably fingerprints and blood, disappears after a few
in-game hours.** CITED (search summary of Steam community discussion, "What
evidence proves the killer was at the scene?").
**ABSENT.** **OUT, and we have already made this decision the other way, with a
better reason.** `Core/Traces.cs` sets `StainFloor = 0.45` and says why: "It
does not fade on its own in any useful way. That is the design: dealing with it
has to be a decision you make, not a timer you wait out." Shadows of Doubt's
decay makes waiting a strategy; ours makes washing a verb. Ours is the more
interesting choice and it is already taken.

**B5. CCTV, remotely accessible if your department has the equipment.** CITED
(search summary of HackerNoon).
**ABSENT.** **IN, already recommended in game 2** (Hitman B1, the camera and the
tape). Not counted again as new work. The remote-access layer is OUT: canon's
CCTV is two sites and a recycled tape, which is a place you go rather than a
system you hack.

**B6. Records: call histories, private messages, address books, wallets.**
CITED (search summaries of the Steam store page and HackerNoon).
**ABSENT.** **IN as a rider on B1**, translated into period. There are no emails
in 1990 and there are itemised phone bills, address books, wage slips, betting
slips, rent books and letters, and `canon.md` makes paper the information
channel by rule. The tile "letters and newspapers the player can read" (typed
absent) covers the reading; what B1 adds is that a document can NAME A PERSON
and therefore be evidence rather than flavour.

**B7. Handwriting on notes as identifying evidence.** CITED (search summary of
Steam community discussion). **ABSENT.** **IN as a rider on B1.**

### C. Holding the information (4)

**C1. A physical pinboard where evidence is pinned and connected with string.**
CITED (search summaries of Gamer Journalist, "How to Submit Evidence", and
HackerNoon): you "pin information that can relate to the case in some way or
form to the Detective Board".
**ABSENT.** **ASK, and it is the one question this game raises for Jafar.**
D12 specifies our surface as a JOURNAL: "The player's own memory is fully
surfaced in an in-game journal called the Ledger. Per-person and per-event
entries, tagged witnessed, heard or deduced." A journal is a list and it scales
to any amount of information. A pinboard is a space, and it does something a
list cannot: it makes the CONNECTIONS the player drew visible, and it makes the
player do the drawing, which is the difference between being told a deduction
and making one.
It also costs more, is harder to make legible on a controller, and can become
busywork. Shadows of Doubt's own reviews are mixed on it. This is not a
technical choice, it is what the game feels like to sit in front of on a
Thursday evening, so it is his. It links to queue topic 13, which covers how
investigation games hold information the player cannot write down.

**C2. Anything can be pinned: addresses, photographs, emails, shoe sizes,
wallets.** CITED (search summary of Gamer Journalist). **ABSENT.** **ASK**, with
C1. Note the design consequence if the answer is the board: every piece of
evidence then needs a representation that is legible as an object, which is an
art cost the journal does not carry.

**C3. A case form where you write the name of the person you accuse.** CITED
(search summary of Gamer Journalist).
**COVERED**, and ours is already the better version. `Core/Informing.cs` is
exactly this verb, and its header states a thesis Shadows of Doubt does not
have: "truth is not an input. A true accusation nobody will corroborate is
ignored. A false one three people will swear to lands." Our accusation is weighed
by the same machinery that weighs accusations against the player, which is
`LedgerState.CaseStandsAt` and `HomicideBook`'s corroboration shape.

**C4. Arrest as a physical act: handcuffs, from behind or after knocking them
down, then telling them.** CITED (search summary of GamesRadar, "How to arrest
people in Shadows of Doubt").
**ABSENT.** **OUT.** Tom Novak is not the police. Recorded because it points at
the tile "court and the cells" (typed absent) from the other end: what is missing
there is not the player arresting somebody, it is the player being arrested, and
the inventory already notes that `CoatHost.Arrested` has no caller outside Core.

### D. Approach and consequence (3)

**D1. Multiple approaches to any case: lockpicking, breaking doors, sabotaging
security, bribing citizens, or playing by the book.** CITED (search summary of
the Steam store page).
**COVERED**, across "bribes and intimidation" (partial), "doors and who gets in"
(exists), "burglary and lockpicking" (typed absent) and "pickpocketing" (typed
absent).

**D2. A wrongful arrest is possible.** CITED (search summary of Steam community
discussion, in which a player reports three).
**COVERED**, and by the stronger model: `Core/Informing.cs` makes a wrong
accusation a thing the world weighs rather than a thing the game scores.

**D3. New cases generate continuously over time.** CITED (search summary of the
Steam store page).
**ABSENT.** **OUT**, and section 3 is the argument. An endless supply of
generated cases is what produces the repetition reviewers complained about. Our
equivalent is authored, which is slower and is the choice the project has
already made twice in writing.

### E. What generation did to it (2)

**E1. The city, its cases and its conversations are procedurally generated.**
CITED (search summary of Gamecritics): this "instead lead to very repetitive
generated cities, cases, and conversations".
**ABSENT.** **OUT, and this is the load-bearing OUT of the entire five-game
audit.** See section 3.

**E2. Procedurally generated document text populates every location.** CITED
(same): "Literally every office explored had an identically written email about
a gambling ring, and each apartment had the same letters to old friends with
indistinguishable text."
**ABSENT.** **OUT**, with E1, and worth separating because it is the specific
mechanism. It is also the exact shape of the risk sitting in our own tile "the
cast": a population generator that "supplies names, not people". Names are the
structured part, which generates fine. Letters are the unstructured part, which
is where the sameness shows.

## 5. What could not be established

1. **The devblogs themselves.** `colepowered.com` is egress-blocked and
   `colepowered.itch.io` was not tried after the block. Everything in section A,
   including the 10 to 15 second figure and the 95 percent figure, is a
   summariser's rendering of a developer's own post. These are the most
   load-bearing numbers in this file for queue topics 2 and 17, and they should
   be read from the devblog before either topic uses them.
2. **The actual population figure.** "100s" is the developer's own imprecision
   as relayed; I could not establish a number per city.
3. **Whether the pre-computed day is a full simulation or a schedule
   resolution.** This matters a great deal for A3's usefulness and I could not
   establish it. A ten-second pass that decides where everyone will be is a
   different thing from a ten-second pass that runs a day.
4. **Reception is genuinely mixed and I have not weighted it.** I have quoted
   the negative reviews because they are the informative half for us, and the
   same aggregates carry reviewers calling it "one of the most well-crafted
   experiences that anyone, even detective game veterans, should play". Section
   3 rests on a specific, repeated, concrete complaint (identical documents),
   not on a verdict.
5. **How much of the repetition was fixed after launch.** The game has been
   updated; I did not establish whether the document-sameness complaint still
   stands in the current build, and that is a real limit on section 3.
6. **Not enumerated.** The first-person movement and stealth, the cyberpunk
   setting and its social credit systems, the side jobs, the apartment and
   business ownership, the modding support, and the console port.

## 6. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Steam, "Shadows of Doubt" store page, https://store.steampowered.com/app/986130/Shadows_of_Doubt/
- ModDB, "Shadows of Doubt DevBlog #8: Simulating a City", https://www.moddb.com/games/shadows-of-doubt/news/shadows-of-doubt-devblog-8-simulating-a-city
- ColePowered Games, "DevBlog 8: Simulating a City", https://colepowered.com/shadows-of-doubt-devblog-8-simulating-a-city/ (EGRESS BLOCKED; the primary source for section A)
- ColePowered Games, "DevBlog 10: Gameplay Loop", https://colepowered.com/shadows-of-doubt-devblog-10-gameplay-loop/
- ColePowered Games, "DevBlog 15: Moving in the Citizens", https://colepowered.com/shadows-of-doubt-devblog-15-moving-in-the-citizens/
- ColePowered itch.io, "DevBlog #19: Designing a Detective Toolkit", https://colepowered.itch.io/shadows/devlog/113594/shadows-of-doubt-devblog-19-designing-a-detective-toolkit
- ColePowered itch.io, "DevBlog #18: Scripted Missions in a Procedural World", https://colepowered.itch.io/shadows/devlog/111292/shadows-of-doubt-devblog-18-scripted-missions-in-a-procedural-world
- TechRaptor, "Shadows of Doubt Preview: A City at Your Fingertips", https://techraptor.net/gaming/previews/shadows-of-doubt-preview-city-at-your-fingertips
- TV Tropes, "Shadows of Doubt", https://tvtropes.org/pmwiki/pmwiki.php/VideoGame/ShadowsOfDoubt
- Gamecritics, "Shadows Of Doubt Review", https://gamecritics.com/ryan-nalley/shadows-of-doubt-review/
- Metacritic, "Shadows of Doubt Reviews", https://www.metacritic.com/game/shadows-of-doubt/
- OpenCritic, "Shadows of Doubt Critic Reviews", https://opencritic.com/game/14865/shadows-of-doubt/reviews
- HackerNoon, "A Guide to Investigating Crime Scenes and Solving Murder Cases", https://hackernoon.com/shadows-of-doubt-a-guide-to-investigating-crime-scenes-and-solving-murder-cases
- Gamer Journalist, "How to Submit Evidence in Shadows of Doubt", https://gamerjournalist.com/how-to-submit-evidence-in-shadows-of-doubt/
- GamesRadar, "How to arrest people in Shadows of Doubt", https://www.gamesradar.com/games/simulation/shadows-of-doubt-arrest/
- Shadows of Doubt Wiki, "Cases", https://shadows-of-doubt.fandom.com/wiki/Cases
- Steam community, "What evidence proves the killer was at the scene?", https://steamcommunity.com/app/986130/discussions/0/3829791550536679886/
- Steam community, "How do I actually arrest suspects", https://steamcommunity.com/app/986130/discussions/0/3829792183358760735/

Repository sources, read this session at commit `074f85b`:
`production/systems-inventory.json`, `canon.md`,
`ledger-v2/respec/vision-pillars-v2.md`,
`ledger-v2/respec/decision-register/D12-information-surfaces.md`,
`ledger/Assets/Scripts/Core/Traces.cs`, `Core/Occupancy.cs`,
`Core/Perception.cs`, `Core/Observation.cs`, `Core/Informing.cs`,
`Core/Homicide.cs`.
