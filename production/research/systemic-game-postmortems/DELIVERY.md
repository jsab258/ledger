# Ambitious systemic games that shipped badly or never shipped

Research topic 21. Delivered to the studio. Nothing here is an instruction.

Topic 18 looked at small teams that SHIPPED and deferred the failures here.
This is that half, and it is deliberately not a list of disasters: the useful
cases are the ones whose ambition was the same SHAPE as LEDGER's, which means
simulated people with lives of their own, and the question is what broke.

Labels follow `production/art/atlas-02/research/`: CITED, DERIVED, ASSUMED,
HOLE.

Egress, stated because it fails silently: `blog.paavo.me`, a technical
write-up of what Radiant AI actually was, is EGRESS_BLOCKED from this
container, measured 2026-09-14.

---

## Part 1. Four cases, chosen for the shape of their ambition

### 1.1 Oblivion's Radiant AI (2006): the simulation ate the authored content

The case closest to LEDGER's design, and the one with the sharpest lesson.

CITED: Radiant AI had to be nerfed because it led to many deaths, with NPCs
killing other NPCs for drugs, money and items they wanted. "With unrestrained
Radiant AI, the game turned into a bloodbath, and if large numbers of
characters die, lots of quests tend to break, which is a problem in an RPG."
[SlashGear, Why Oblivion's NPC rampage matters](https://www.slashgear.com/1237314/why-oblivions-npc-rampage-matters-for-the-future-of-ai-development/),
[Cracked, Oblivion's AI had to be dumbed down to save the game](https://www.cracked.com/article_34695_the-elder-scrolls-iv-oblivions-ai-had-to-be-dumbed-down-to-save-the-game.html)

CITED, the specific example, which is worth reading twice because it is a
crime-and-consequence loop: in the Dark Brotherhood skooma mission, addicts
would acquire all the skooma, and when the dealer had none left to sell they
would attack him, leaving him dead and the mission unplayable. Separately,
Bethesda had not implemented a way for an NPC to pay a bounty, so an NPC who
stole and was seen by a guard would die.
[Medium, Oblivion and the notorious Radiant AI](https://thanasispapadopoulos.medium.com/the-elder-scrolls-iv-oblivion-and-the-notorious-radiant-artificial-intelligence-4996636473b)

CITED: during testing no NPCs were marked essential, and characters had strict
schedules for the crimes they would commit.
[Medium, as above],
[paavohtl's blog, What was Radiant AI, anyway?](https://blog.paavo.me/radiant-ai/) (EGRESS BLOCKED)

DERIVED, and it is the finding of this topic: the system did not fail because
it was bad at simulating people. It failed because it was GOOD at it, and the
authored content sitting on top of it assumed those people would still be
there. Two mechanisms did the damage, and both are mundane: a want with no
lawful way to satisfy it (skooma with no more supply) and a punishment with no
middle rung (a bounty with no way to pay it). Given either, a simulated person
escalates to violence because violence is the only branch left.

### 1.2 STALKER 2's A-Life 2.0 (2024): the simulation lost to the frame budget

The case closest to LEDGER's engineering, and it happened two years ago to a
studio with a real team and real money.

CITED: A-Life 2.0 was removed from the game's Steam description. "Optimization
issues ahead of launch forced GSC to shrink the area around the player in which
A-Life 2.0 works, when it is supposed to extend much farther in virtual
distance terms", in order to get the game into acceptable shape across PC and
Xbox Series X and S.
[Destructoid, A-Life 2.0 cut down due to performance concerns](https://www.destructoid.com/stalker-2-developer-reveals-that-a-life-2-0-was-cut-down-due-to-performance-concerns/),
[GameSpot, Why A-Life 2.0 was pulled from the game's description](https://www.gamespot.com/articles/stalker-2-developer-explains-why-a-life-2-0-was-pulled-from-the-games-description/1100-6528216/)

CITED, the developer in his own words: Ievgen Grygorovych of GSC Game World
said "We were fighting with optimization", and "To optimize, you have a lot of
things that need your resources, and you try to cut things from different
directions to properly optimize the game well." The system "to work properly
requires a much larger area for spawn NPCs and requires much more memory
resources".
[Windows Central, STALKER 2 devs explain why A-Life is broken](https://www.windowscentral.com/gaming/stalker-2-devs-explain-why-a-life-is-broken),
[Dexerto, STALKER 2 devs admit A-Life 2.0 nerf](https://www.dexerto.com/gaming/stalker-2-devs-nerfed-a-life-2-0-major-flaw-2997539/)

DERIVED, and it lands directly on topic 17: A-Life is a simulation of life
happening where the player is NOT, and what killed it was the cost of
everything the player CAN see. The two budgets got added together, the total
did not fit, and the half that was cut was the invisible half, because cutting
the visible half is what a player notices in a review. That is the exact
trade-off topic 17 argued should be two separate numbers, and this is what
happens when it is one.

Worth noting the second-order failure too: a marketing team member removed the
A-Life description from the Steam page without checking with executives, and
the studio then had to explain publicly why a promised system was not there.
[NeoGAF thread collecting GSC's explanation](https://www.neogaf.com/threads/stalker-2-dev-gsc-game-world-explains-for-the-first-time-what-went-wrong-with-a-life-2-0-and-why-it-was-removed-from-the-game%E2%80%99s-description-on-steam.1678015/)

### 1.3 No Man's Sky (2016): the gap between what was said and what shipped

CITED: the launch response was "marred by the lack of several features that had
been reported to be in the game", most prominently multiplayer. For years the
studio head had said that if two players met on a planet they would see each
other's avatars; on launch day they did not. Players compiled video montages of
interviews promising features that were not present. The studio then went
largely silent for months, which compounded the backlash.
[Wikipedia, No Man's Sky](https://en.wikipedia.org/wiki/No_Man's_Sky),
[Kotaku, The No Man's Sky hype dilemma](https://kotaku.com/the-no-mans-sky-hype-dilemma-1785416931)

CITED, the recovery: Foundation (November 2016 / January 2017) added base
building and vehicles; Atlas Rises (August 2017) added a rewritten story,
portals, procedural missions and a limited joint exploration where other
players appeared as orbs; NEXT (July 2018) delivered full multiplayer, two
years after launch. All free.
[No Man's Sky release log](https://www.nomanssky.com/release-log/),
[Dot Esports, all releases, updates and patches](https://dotesports.com/general/news/no-mans-sky-all-releases-updates-and-patches)

DERIVED: the game that shipped in 2016 is roughly the game that was reviewed
badly, and the thing that was actually broken was the DESCRIPTION. That is a
different failure from 1.1 and 1.2, and it is the only one of the four that is
purely self-inflicted by talking.

### 1.4 Milo and Kate (2010): the conversation demo that never shipped

The case closest to LEDGER's second pillar, and it is a cautionary one.

CITED: Milo and Kate was a Kinect tech demo in which players would converse
with a simulated child. It was shown at E3 and at TED, "proclaimed that players
would be able to converse with a child", and "the project was never seen again
after its debut". Its designer's reputation is widely attributed to
overpromising, with Milo named as the most infamous instance.
[Time Extension, Molyneux on revisiting one of his most infamous projects](https://www.timeextension.com/news/2025/10/peter-molyneux-thinks-it-could-be-wonderful-to-revisit-one-of-his-most-infamous-projects-with-todays-tech),
[TechCrunch, The lesson of Peter Molyneux](https://techcrunch.com/2015/02/15/the-lesson-of-peter-molyneux/amp)

CITED, his own stated lessons after Godus: he would not run a Kickstarter at
the START of development but "at the end or towards the end"; there is "an
overwhelming urge to over-promise" because crowdfunding's all-or-nothing rule
pushes developers to "just say anything"; and doing Kickstarter and Early
Access "before having something defined and playable is a hugely risky
undertaking that can be very destructive to the final quality of the game".
[TechRadar, Molyneux on what went wrong with Godus](https://www.techradar.com/news/gaming/peter-molyneux-on-what-went-wrong-with-godus-and-how-to-save-free-to-play-1276864),
[Wikipedia, Godus](https://en.wikipedia.org/wiki/Godus),
[IBTimes, Molyneux apologises for unfulfilled Godus Kickstarter promises](https://www.ibtimes.co.uk/peter-molyneux-apologises-unfulfilled-godus-kickstarter-promises-1487552)

DERIVED: a live conversation with a simulated person was demoed to the world
sixteen years ago and did not ship, and the reason usually given is not that
the technology was impossible but that the demo was a vertical slice sold as a
product. LEDGER's pillar 2 is the same promise with a technology that can
actually make the words. What Milo says is that the words were never the hard
part.

---

## Part 2. The four failure modes, and what this project has against each

### 2.1 The simulation eats the authored content

The Oblivion mode. Two preconditions did the damage there: a want with no
lawful satisfaction, and a punishment with no middle rung.

CITED, checked in this checkout on 2026-09-14: there is NO death state in
`Core`. A grep for `IsDead`, `\.Dead`, `Kill(` and `Die(` across
`ledger/Assets/Scripts/Core/` returns four hits and every one is a false
friend: a speech deadline, a comment about the press naming the player on
"essentially every killing", the crowd-fraction comment, and a suspicion
prompt.

CITED: `Core/Homicide.cs` defines `Killing` with `VictimId` and `VictimName`,
and its header states the design intent plainly: "killing the only witness to a
killing genuinely drops the chance of conviction". `VictimId` flows into
`Fact("player", "killed_" + VictimId, ...)` at `SimDirector.cs:7531`, into
`Harm.Inflict` at `TrafficHost.cs:289`, and into a witness-exclusion check at
`Witnesses.cs:127` where the victim is skipped as a witness of their own death.
Nothing marks anybody dead and nothing removes them from the population.

CITED: nothing anywhere marks an NPC essential, protected or unkillable. The
only `Protected` in Core is `Mixing.Protected(Bus, authored)`, an AUDIO bus
protection, which is a name collision rather than a defence.

DERIVED, and stated fairly rather than as an accusation: this is a phase
boundary, not negligence. `production/systems-inventory.json` types combat as
PARTIAL at phase 4, noting "the ONLY call into Core/Combat from the Game layer
is the stamina term the walk uses". Mortality is not due yet.

The reason to write it down now is the Oblivion lesson's timing. Radiant AI did
not break during development of the simulation; it broke when the simulation
met a cast the content assumed would be alive. LEDGER has ten named cast
members, authored stories (an earlier topic in this queue), and a mechanic that
rewards killing witnesses. The two systems are being built separately and have
never met. The moment they do is the moment this failure mode arrives, and
Oblivion's answer, marking people essential, is the one that hollows out the
simulation.

### 2.2 The invisible half loses to the visible half

The STALKER mode. Topic 17 found this project's version of it in advance: one
resident count gating two budgets that behave differently, with the moat living
entirely in the cheap, invisible one.

CITED, checked today: there is no simulation radius in this project. A grep for
`SimRadius`, `simulationRadius`, `offscreen`, `AbstractSim` and `Distant`
across Core and Game returns only visual-detail comments (a gull, a speech
bubble's font, the rig's solve distance, the skyline band).

DERIVED: LEDGER currently simulates everybody at full rate, everywhere, which
is why topic 17 measured 0.0746 ms per walker per frame as a FULL-RATE cost. So
this project has not yet made the choice GSC had to make under deadline. It has
also not built the mechanism that would let it make the choice cheaply, which
is the proximity-scaled update rate that both Mass Entity and Shadows of Doubt
use.

The useful reading is that GSC made this decision LATE, under launch pressure,
and the thing that made it expensive was that A-Life's radius was load-bearing
for the feature's whole identity. Deciding it early and deliberately is
available here and was not available to them.

### 2.3 The description breaks before the game does

The No Man's Sky and Godus mode. This is the one LEDGER is structurally
immune to, and it is worth saying clearly because three of the four cases here
were made worse by it.

CITED, from the goal statement copied into `CLAUDE.md`: "Success is the game
clearing the bar below, not shipping or sales." The bar is the Meridian Test,
whose fourth condition is "Jafar, on a free evening, chooses playing LEDGER
over replaying KCD2."

CITED, `production/budget.md`: "LEDGER stops when the week's LEDGER share is
spent", funded out of one person's own allowance.

DERIVED: there is no publisher, no crowdfunding campaign, no store page, no
pre-order, no release date and no audience that has been told anything. Every
one of Molyneux's stated lessons is about the pressure crowdfunding creates,
and none of that pressure exists here. The one failure mode in this set that
has destroyed the most goodwill is the one this project cannot commit without
first choosing to.

The corollary, which is less comfortable: the Meridian Test IS a promise, made
to one person, and condition 1 is a thirty-minute first impression. The No
Man's Sky lesson applies to it in miniature. What the test measures is exactly
what a reviewer would measure in the first half hour.

### 2.4 A vertical slice sold as a product

The Milo mode. A demo of a conversation is easy to make impressive once and
hard to make survive an hour.

DERIVED, and this is the sharpest thing this topic can offer about LEDGER's
own instruments: this project's defence against the Milo failure is unusually
strong and is already built, and it is not a design document. It is the rule in
`CLAUDE.md` that a feature is done when something calls it and a gate proves
the call happened (rule 6), the throughput ledger's habit of recording a
finished-looking piece as ZERO because nothing consumes it, and the
verification model that makes a claim carry its instrument.

A studio that records its own brand bible as zero throughput because nothing
reads it is a studio that will notice a vertical slice. That is worth saying,
because this delivery is otherwise a list of things to worry about.

---

## Part 3. What could not be established

1. **A post-mortem of an NPC MEMORY or relationship system cut before
   release.** Four differently-worded searches found none. Plenty of writing
   exists on building such systems and none on one being cut. This is the
   closest analogue to LEDGER's own moat and there is no case study of its
   failure, which means the moat's specific failure mode is unrehearsed in
   public.
2. **What Radiant AI actually was, technically.** The one serious technical
   write-up found is egress-blocked.
3. **Whether Oblivion's cut was as total as reported.** The sources are
   secondary and largely retrospective; the phrase "mostly cut" appears without
   a developer naming what remained.
4. **Any figures for STALKER 2's A-Life radius**, before or after. The
   developer quotes are qualitative.

---

## Part 4. Findings and interpretation

### Findings

F1. Oblivion's Radiant AI was cut because the simulation killed NPCs the
authored quests needed, through two mundane mechanisms: a want with no lawful
satisfaction, and a punishment with no middle rung.

F2. During Oblivion's testing no NPCs were marked essential.

F3. STALKER 2's A-Life 2.0 was reduced in radius before launch explicitly for
performance, in the developer's words "We were fighting with optimization", and
was removed from the Steam description.

F4. No Man's Sky's 2016 failure was a gap between statements and the shipped
game, and took two years and three major free updates to close.

F5. Milo and Kate, a live conversation with a simulated person, was demoed in
2010 and never shipped; the designer's own stated lesson is about the pressure
to overpromise before having something defined and playable.

F6. This checkout has no death state anywhere in Core. `Killing.VictimId` flows
into facts, gossip, harm and witness exclusion, and nothing marks anyone dead
or removes them.

F7. Nothing anywhere marks an NPC essential or protected. The one `Protected`
in Core is an audio bus.

F8. Combat is typed PARTIAL at phase 4 in the systems inventory, so F6 and F7
are a phase boundary rather than a defect.

F9. There is no simulation radius or offscreen tier in this project; everybody
is simulated at full rate.

F10. There is no publisher, crowdfunding, store page, pre-order or release
date, and the goal statement says success is the bar, "not shipping or sales".

### Interpretation

I1. The two failure modes with real purchase on LEDGER are 2.1 and 2.2, and
they arrive at known moments rather than gradually: 2.1 when mortality meets
the named cast, 2.2 when the frame budget is first set at a resident count.
Both moments are on the roadmap, and neither has happened.

I2. Oblivion's answer to 2.1 is the one to avoid. Marking people essential
makes the simulation lie, and LEDGER's moat is that the simulation does not.
The better reading of that case is that the bug was not mortality; it was that
a simulated person had exactly one branch left when a want went unsatisfied.
The defence is a middle rung on every escalation, which is a design job and not
a protection flag.

I3. The most valuable thing in Part 3 is the absence. Nobody has published a
post-mortem of a cut NPC-memory system, which means LEDGER's central moat is
the one part of it with no cautionary tale to learn from. That is a reason to
trust this project's own instruments more than the literature.

I4. Three of the four cases were made materially worse by talking. This project
has said nothing to anybody, and that is not an accident of its stage but a
consequence of how it is funded. It is a genuine structural advantage and it
lasts exactly as long as nobody makes a promise.
