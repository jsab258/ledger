# You already built this, and the number it uses is the wrong kind of number

Research topic 30, the last of the five. I expected to design an aggregation and
found one already working. The useful finding is about which statistic it uses.

## First, a flag

**D34 does not exist in this checkout.** Your decision register runs D1 to D18,
and no D20-to-D39 token appears anywhere in the repository. This is the third
time in thirty topics (D24 and D28 were the others), so I have done what I did
then: taken your own wording as the rule and worked against that rather than
inventing a record.

> a district's feeling is what its residents individually remember, never a
> number.

## What is already built

`Gossip.DayCircleHeat()` does exactly what that sentence asks for:

1. Walk every person in the mill, live, on every call. **Nothing is stored.**
2. Keep only those in the circle. **The group is a filter, not an object.**
3. Per person, take their strongest rumour per topic, so retellings of the same
   story never stack.
4. Combine that person's distinct stories so three half-believed sightings add
   up where one would not.
5. Take the result across the group.

Then `StreetWord` turns it into one of four words: **quiet, murmuring, uneasy,
hostile.** The player never sees a number.

That is your constraint, implemented, and it was implemented before the brief
was written. It should probably be written down as the house pattern: computed
on read, group as a filter, language as the output.

## The problem, in one table

Step 5 takes the **maximum**. Its own comment says so: "how convinced the
most-convinced day-circle NPC is."

So imagine forty people on the day circle:

| | one furious person | a town that has turned |
|---|---|---|
| the angriest person | 0.75 | 0.75 |
| everyone else | 0.05 | 0.70 |
| what the game computes | 0.75 | 0.75 |
| what it tells the player | **"The street is hostile"** | **"The street is hostile"** |

Those two towns are as different as a social simulation can make them. **Telling
them apart is what the moat is for.** The readout cannot.

It fails the other way too: thirty-nine people at 0.69 and nobody higher reads as
"uneasy", which is calmer than a single convinced witness at 0.71.

## Why this is your own rule, not my opinion

CLAUDE.md rule 2: "A peak answers 'did it ever', a median answers 'is this
normal', and neither answers the other. Before a new number enters a conclusion,
say which of peak, median, last-wins or at-worst it is."

`DayCircleHeat` is a peak. `StreetWord` renders it as a description of a
collective. The street's word does not say which it is, and it is a peak.

## And the aggregator is probably not the thing to change

I think the max is **right** for what it was originally built to drive: danger.
One person convinced enough to act is a threat whatever the other thirty-nine
think, and the comment's own framing, that carelessness is lethal and damage control
is meaningful, is a threat model.

The fault is that **one number is doing two jobs**: a danger reading and a mood
description. That is the same shape I flagged at the end of the last batch, then
committed myself in topic 17, and this is its third appearance.

## The better pattern is four hundred lines away in your own code

The day summary already does it properly:

> No open liabilities you know of. / **Somebody** is carrying something on you. /
> **A few people** are carrying things on you. / **Too many people** are carrying
> things on you.

That is a **count of people**, banded into language. "A few people" is a
statement about a population. "Hostile" is a statement about a mood that a
maximum cannot support.

The same loop that computes the max already visits every agent, so it could
return a count above the sharing floor and a median at no extra cost.

## About districts specifically

There is nothing there to critique, because there is nothing there.

Every resident has a `District` field. `DistrictPulse` exists and is correctly
built, but it runs the **other way**: it takes district facts (businesses you
own, prosperity) and seeds a new resident's starting suspicion. Its comment is
honest about its scope: "this seeds STARTING posture, it does not play the game
for anybody."

**Nothing reads a district's feeling out of its residents.** The only group
readout in the game is the day circle, which is a time-of-day social circle, not
a place.

All the ingredients exist and no function joins them. Worth knowing before
anyone designs a district reputation feature, because the obvious way to build
one is the stored score your own rule forbids.

---

EGRESS NOTE, standing in every delivery: one route out of this container reads a
page in full, and it reaches source repositories and package registries only.
This topic is almost entirely a read of your own code; the aggregation question
is a statistics question, and your rule 2 answers it better than anything I
found by searching.
