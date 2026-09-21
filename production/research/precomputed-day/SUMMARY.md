# We already do this, and I was wrong three times about it

Research topic 27. You asked whether the simulation should run live, and told me
to first establish what Shadows of Doubt's precomputed day actually is. Doing
that led somewhere I did not expect.

## First, the precondition you set

**Their precomputed day is a schedule resolution, not a simulation.**

Their devblog: the 10 to 15 seconds at the start of each day is when citizens'
"activities for the day are chosen and mapped out for them". It produces an
itinerary. It does not fast-forward a world and record what happened in it.
Deviations get calculated live, because "there will never be more than a handful
of citizens requiring deviations".

So it cannot tell you who saw what, who stole what, or who fell out with whom.
None of that happens during the precompute. What it gives you is: **where
everybody is, at every hour, as a known quantity rather than something you have
to run a body to find out.**

That is a smaller claim than it sounds, and it happens to be exactly the one
thing our gossip cannot work without.

## Why it matters for us specifically

Our entire gossip system turns on one function:

> `Together(a, b)`: get both positions, and return true if they are within six
> metres.

A rumour moves only between two people who are near each other and who both
have a position. So "can this rumour spread" reduces entirely to "where is
everyone", which is the question a precomputed day answers.

## And here is the part I got wrong

**In topics 17, 21 and 25 I said this project has no simulation radius.** I ran
a grep for `SimRadius`, `offscreen`, `AbstractSim` and three other words, got
nothing, and reported an absence.

The project calls it `Lod` and `Band`. It has had a three-band system all along:

| band | distance | what it costs |
|---|---|---|
| **Near** | to 70 m, max 28 | in the gossip network, and drawn |
| **Mid** | to 130 m, max 120 | in the gossip network, **no body** |
| **Far** | beyond | no position, so no gossip |

The Mid band works out where somebody is from **their schedule and the clock**,
snapped to the street network, with no character in the world at all. That is
the Shadows of Doubt architecture. We built it. The comment on the hook that
carries it says exactly why: "a person with no body has no position and Together
would always say no."

The only real difference is timing. They resolve a whole day at dawn; we resolve
one person when asked. Both replace a body with a schedule lookup.

I reported an absence from a search that did not cover your own vocabulary, and
then quoted that absence twice more. That is the failure your rule 1 exists to
stop and I should have caught it.

## The number I would actually put in front of you

From the last landed run: **near=22, mid=159, far=382.**

563 residents were being tracked. 181 of them could gossip. **382 of them, 68%,
could not**, because the Far band returns no position at all.

That is not a bug. It is a deliberate, capped, hysteresis-protected performance
boundary, and it is the same decision the STALKER 2 team had to make in a panic
before launch and made badly. You made it early, calmly, with the numbers
printed.

What it means is that **"the town remembers" has a measured radius, and it is
130 metres.** Whether that costs you anything depends on whether rumours travel
because people move or because the player moves, and nothing measures which.

## A second correction, to topic 17

While looking for the band system I found this sitting in the same verdict file
I had already read twice:

    frameCost=[all:26.3 / noShadow:19.6 / noPixLights:20.6 / noBodies:26.2 ...]

Subtract, and on the last landed run:

- shadows cost **6.7 ms**
- pixel lights cost **5.7 ms**
- **the entire drawn crowd costs 0.1 ms**

Topic 17 framed the frame budget as a crowd problem and did all its arithmetic
in bodies per millisecond. On your own landed measurement the crowd is 0.4% of
the frame and lighting is nearly half of it.

The numbers I quoted in topic 17 were read correctly, but one was the CPU cost
of simulating people and I wrote the topic as though the render cost of drawing
them were the constraint. It is not.

That is the exact fault I closed the last batch by naming: a number that exists
for one half of a question, quoted for both. I did it myself, in the same batch,
and the evidence was in a file I had already opened.

## So: should the simulation run live?

It already does not, for two thirds of the town. The architectural question in
your brief was settled in this codebase before I started auditing it.

What is genuinely still open is smaller and more answerable:

1. **Should the Far band be able to gossip at all?** Today it cannot. A
   schedule-only rumour pass would cost no bodies and no rendering, and would
   make that 382 count for something.
2. **Should seeing and telling share one radius?** Right now the band governs
   both. Perception already has five distinct rung distances because they are
   different physical processes; transmission probably deserves the same.
3. **What does the schedule lookup actually cost?** Never measured, and it
   decides whether batching a whole day like ColePowered would buy anything at
   all.

---

EGRESS NOTE, standing in every delivery: one route out of this container reads a
page in full, and it reaches source repositories and package registries only.
Everything cited here from devblogs or press is a search engine's summary and is
labelled as such; the ColePowered devblog host is blocked.
