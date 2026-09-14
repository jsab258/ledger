# Topic 14: failure design, and what happens after arrest

STATUS: SPEC (research delivery). Branch `research/failure-after-arrest`, from
commit `074f85b`. Written 2026-09-14 by the research lane.

NOTHING IN THIS FILE IS AN INSTRUCTION. No queue item filed, no tile proposed,
no decision record written.

## 0. How to read this file

Claim labels are CITED, DERIVED, ASSUMED and HOLE. Sourcing limit unchanged.
Repository claims name their file and line.

## 1. Where we are, measured

`Game/CoatHost.cs:159` declares `Arrested(Reaction.Lawful outcome, out bool
publicly)`. `Core/Homicide.cs:61` says what has become of it: "`CoatHost.Arrested`
has no caller in the whole Game layer." A grep this session for `Arrested` across
`ledger/Assets/Scripts` returns exactly those two hits, the declaration and the
comment about it having no callers.

The inventory agrees from two directions. The tile "the law and the police"
(partial): "Arrest cannot happen in this checkout: `CoatHost.Arrested` has no
caller outside Core walked here, so the spine's terminal state is unreachable in
play." The tile "failure states and autosave policy" (partial): "Arrest is NOT a
live failure state". And the tile "court and the cells" (typed absent): "an
arrest that leads nowhere is a consequence that stops."

**So the topic's question is currently unanswerable by play: nothing happens
after arrest, because arrest does not happen.** Everything below is about what
should.

## 2. Most of this literature does not apply to us, and it is worth saying why

CITED (search summaries of Game Developer's several pieces on fail states and
"Debunking Losing is Fun", the Learning Guild's article, and joyplayx's piece on
death and retry loops): the field's vocabulary is retry loops. "Well-designed
death and retry loops involve fast retries, fair mechanics, clear feedback, and a
sense of progression"; "the right kind of failure feedback is a reward"; and the
useful distinction is between "in-loop" failures "intended by the designer" and
"out-of-loop" ones "such as misunderstanding game controls".

DERIVED: all of that assumes a reset. Celeste, Hades, Mario and the roguelikes
are games where failure returns you to a known state and the design problem is
making the return quick and instructive.

`canon.md` forbids us that: "Permanent per-NPC memory. Nothing is ever wiped;
remediation is behavioral (leave, change appearance, rebuild relationships),
never a reset."

**So our design problem is a different one, and I have not found it named in the
literature: failure design in a reset game is about making the RETRY
interesting, and failure design in a permanent game is about making the
CONTINUATION interesting.** Nobody gets sent back. They carry on from a worse
position, and the question is whether the worse position is playable.

## 3. The one part that does apply, and it is the dangerous part

CITED (search summary of Game Developer's "The Balance of Fail States in Game
Design"): "The danger of a strong fail state comes in when it creates a feedback
loop of failure", and "the amount of control the player has over their success is
a big factor when it comes to whether a game is frustrating".

DERIVED, and this is the finding: **a permanent-memory game builds that loop by
construction.** Get seen, the town knows, doors close, the police attend, which
makes the next act harder, which makes being seen more likely. Every mechanism in
our moat pushes the same direction and none pushes back.

And one of our files says so deliberately. `Core/Homicide.cs`: "Each body you add
to fix the last one leaves you worse off than before the first." That is a
designed death spiral, it is correct for killing, and the design intends it to
be terrifying.

The question this topic raises is whether the SAME spiral is intended for
everything else, because architecturally it is the same spiral.

### 3.1 What we have to push back with, measured

Four mechanisms exist in `Core/Gossip.cs` and `Core/Homicide.cs`:

| Verb | What it is | Number |
|---|---|---|
| `Discredit` (`:772`) | argue a story down | `DiscreditFactor = 0.65` (`:690`) |
| `Contain` | buy or lean a story quiet | `DcOutcome` includes `Contained` and `Backfired` |
| `Age` (`:887`) | let a story go cold | hop decay and time |
| `PointAt` / redirect | aim the police at somebody else | `RedirectRelief = 0.45`, `RedirectHolds = 4` (Homicide `:189`, `:190`) |

Plus canon's three behavioural remedies: leave, change appearance, rebuild
relationships. DERIVED against the rest of this research lane: **two of those
three are not built.** "Change appearance" is the recommendation the coverage
audit made four times and topic 12 gave an interface to. "Rebuild relationships"
has no verb I found, and the acquaintance model (topic 11) is a static function of
household, companion, cast membership and having-heard-of-you rather than
something the player can move.

So the spiral has four brakes, one of which backfires by design, and the two
remedies canon names most prominently are unimplemented.

HOLE: I did not establish whether the four brakes are sufficient, because that
needs a played run against a hostile town and there has not been one.

## 4. Three things worth taking

### 4.1 Kenshi: the failure state is a PLACE, not a screen

CITED (search summary of Gamerant's "6 Games That Send You To Prison For In-Game
Crimes"): in Kenshi "gameplay doesn't come to a screeching halt when imprisoned;
players will still be immersed in intriguing landscapes with the potential to
conduct a myriad of activities, even collecting disguises in attempts to break
out."

DERIVED: the useful principle is that a failure state with verbs in it is a
location, and a failure state without verbs is a loading screen with a story
attached. And topic 6 already handed us the verbs and the clock: twenty-four
hours from arrival, a review at six hours by an inspector not on the case,
further reviews at nine-hour intervals, a superintendent for twelve more, a
custody sergeant who is independent of the investigation, a custody record, and
the old caution under which **silence costs nothing in court**.

That is a scene, with a timer, with a person to talk to, and with a real decision
(say nothing, or explain). It is not a fade to black, and we would not have to
invent any of it.

### 4.2 Sunless Sea: make the inheritance a TRADE, not a discount

CITED (search summaries of the Sunless Sea wiki's Legacy page and Failbetter's
own "Sunless Sea vs Sunless Skies: Death, Legacies and Repetition"): on death you
choose a legacy, each passing a different fraction of the last captain's things.
And the detail worth having: "choosing to carry over your prior Captain's map
would lock your next captain out of the experience points gained from discovering
new areas on the map."

DERIVED: what makes that interesting is not the inheritance, it is that taking
one thing costs another. We have no death-and-heir structure and should not build
one. What transfers is the SHAPE: a remedy should cost something specific rather
than simply reduce a number. `Discredit` at 0.65 reduces a number. A remedy with
a price is a decision.

Also CITED, and worth recording as a caution: Failbetter concluded their own
death was too punishing and, in the sequel, "wanted to address this and make the
threat of death less of a setback and more of an opportunity." A studio that
built the most admired permanent-loss system of its decade decided it had gone
too far.

### 4.3 Skyrim: the failure nobody believed in

CITED (search summary of ScreenRant's "Skyrim's Prison System Doesn't Make Any
Sense"): the system "is built around letting criminals get away with their
crimes, with the Dragonborn being given an item designed to facilitate their
escape when placed in a cell", and jail costs character progress, and a fine
avoids it entirely.

DERIVED, as the negative example: a designer who puts an escape tool in the cell
has decided the failure state is not worth playing. The tell is not the escape,
it is that the escape is FREE. Our risk is the opposite one, and both are worth
seeing next to each other: Skyrim did not believe in its consequence, and our
design believes in consequence so hard that the spiral is the thing to watch.

## 5. Findings

1. **Arrest is unreachable and the question is therefore open** (1).
2. **The retry-loop literature is about a reset we do not have** (2), and the
   problem we do have, making the continuation interesting rather than the
   retry, I could not find named anywhere.
3. **A permanent-memory game builds a failure feedback loop by construction**
   (3), which our own homicide file intends for killing and which is
   architecturally the same for everything else.
4. **Four brakes exist, one backfires by design, and two of canon's three named
   remedies are unbuilt** (3.1).
5. **The failure state should be a place with verbs**, and topic 6 already
   supplied the verbs, the clock and the one decision that matters (4.1).
6. **A remedy should cost something specific rather than reduce a number**
   (4.2).
7. **Failbetter decided their own permanent loss was too punishing** (4.2),
   which is the most relevant cautionary data point available.

## 6. What could not be established

1. **Whether our four brakes are enough.** Needs a played run against a hostile
   town, and none exists. This is the question the whole topic turns on and I
   cannot answer it from here.
2. **Whether the spiral is intended outside killing.** `Homicide.cs` states the
   intent for bodies. Nothing I read states it or denies it for anything else.
3. **Any named treatment of failure design in permanent-consequence games**
   (2). I looked and found a literature entirely about retries. If it exists I did
   not find it, and I cannot distinguish that from its not existing.
4. **Pathologic 2**, which is the most obvious missing case: a game about a town,
   a clock you cannot stop, and permanent loss, and the game most likely to have
   solved the continuation problem. It was on my shortlist for coverage-audit
   game 5 and lost to Shadows of Doubt. **It is the single biggest gap in this
   topic.**
5. **What `Contain` actually costs**, and what `Backfired` does. I read the
   enum and not the implementation.
6. **Not covered:** the prison-escape genre proper; Dwarf Fortress's "losing is
   fun", which is a community slogan rather than a design document and which
   topic 7 already touched; and the question of whether LEDGER should have a
   game-over at all, which is a Jafar question I am not putting to him because it
   is not raised by the research.

## 7. Sources

Search channel summaries, retrieved 2026-09-14; none read in full.

- Game Developer, "The Balance of Fail States in Game Design", https://www.gamedeveloper.com/design/the-balance-of-fail-states-in-game-design (EGRESS BLOCKED)
- Game Developer, "Figuring out Failure in Game Design", https://www.gamedeveloper.com/design/figuring-out-failure-in-game-design (EGRESS BLOCKED)
- Game Developer, "Debunking Losing is Fun Game Design", https://www.gamedeveloper.com/design/debunking-quot-losing-is-fun-quot-game-design (EGRESS BLOCKED)
- Game Developer, "Failure by Design: Encouraging learning through failure with games", https://www.gamedeveloper.com/design/failure-by-design-encouraging-learning-through-failure-with-games- (EGRESS BLOCKED)
- Learning Guild, "Metafocus: Well-designed Failure in Serious Games", https://www.learningguild.com/articles/metafocus-well-designed-failure-in-serious-games
- joyplayx, "How to Handle Failure in Games: Designing Death and Retry Loops", https://www.joyplayx.com/article/how-to-handle-failure-in-games-designing-death-and-retry-loops
- ScienceDirect, "Fail, fail again, fail better: How players who enjoy challenging games persist after failure in Celeste", https://www.sciencedirect.com/science/article/pii/S1071581923002082
- Gamerant, "6 Games That Send You To Prison For In-Game Crimes", https://gamerant.com/games-send-you-prison-for-crimes/
- ScreenRant, "Skyrim's Prison System Doesn't Make Any Sense", https://screenrant.com/elder-scrolls-5-skyrim-prisons-mages-magicka-criminals/
- Elder Scrolls Fandom wiki, "Prison (Skyrim)", https://elderscrolls.fandom.com/wiki/Prison_(Skyrim)
- Sunless Sea Fandom wiki, "Legacy", https://sunlesssea.fandom.com/wiki/Legacy
- Failbetter Games, "Sunless Sea vs Sunless Skies: Death, Legacies and Repetition", https://www.failbettergames.com/news/sunless-sea-vs-sunless-skies-death-legacies-and-repetition
- Failbetter Games community forums, "Legacy Items", https://community.failbettergames.com/t/legacy-items/12857

Repository sources, read this session at commit `074f85b`:
`ledger/Assets/Scripts/Game/CoatHost.cs:159`, `Core/Homicide.cs` (lines 61, 189,
190), `Core/Gossip.cs` (lines 690, 772, 801, 887, 953), `canon.md`,
`production/systems-inventory.json`, and this lane's own
`production/research/british-policing-1988-1992/` on its branch.
