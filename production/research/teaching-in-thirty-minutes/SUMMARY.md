# Your whole tutorial happens in the first ninety seconds

Research topic 28. You asked how a game teaches a social system in thirty
minutes. Answering it needed one constant I had failed to find, and once I had
it the topic mostly became arithmetic.

## The constant, and the hole it closes

In topic 25 I said no play-clock rate existed in the project and left it as a
gap. It does exist. It is called `MinutesPerRealSecond` and it is `2`.

**One game day is twelve real minutes.**

Everything below follows from that:

| | |
|---|---|
| The Meridian Test's 30 minutes | **2.5 game days** |
| Phase 1's gossip gate, "one in-game week" | **84 real minutes** |
| The gate, against the entire first session | **2.8 times longer** |

So a build can pass phase 1's gossip gate and still fail condition 2 of the
Meridian Test, because the gate allows a rumour to take nearly three times the
length of the whole first session to reach its second listener. That was the
mismatch I flagged in topic 25 and could not size. Now it is sized.

## What the game teaches today, and when

You do have onboarding, and the inventory is honest about it: four diegetic
toast lines, typed partial, phase 3, with the note that no authored first hour
exists and nobody has played one.

The four lines are well written. They fire at 09:02, 09:10, 10:00 and 12:00 game
time. At two game-minutes per real second, from a nine o'clock start:

| line | real time |
|---|---|
| WASD walks, Shift runs | **1 second** |
| press Talk, they remember | **5 seconds** |
| press Ledger for what the street knows | **30 seconds** |
| the coat, and tonight's drop | **90 seconds** |

**The entire tutorial is over in ninety seconds.** The first toast lasts eight
seconds and the second fires at five, so two of the four overlap.

A player who has not yet worked out that WASD moves them is being told about the
ledger twenty-five seconds later and about a night job a minute after that.

This is not a writing problem. The triggers were clearly chosen as story beats
(mid-morning, noon) and a clock running at 120 times real speed turns beats into
a burst. Nobody would notice without doing the division.

Worth saying: the code already knows the right principle. Two other hints, about
money and the day close, fire on first occurrence instead of on the clock, with
a comment explaining that a hint about money not yet held teaches nothing. That
reasoning applies to all four of the timed ones too.

## The thing our first session actually has to do

The standard ladder for a first thirty minutes is movement, then a resource,
then a threat, then the reason the two connect. Ours is different and specific:

1. **You move.** Already first, correctly.
2. **You are seen.**
3. **It was written down.**
4. **It came back.**

Steps 2 and 4 are your condition 2 in halves; step 3 is the moat.

Today all three are **asserted in toast text** inside ninety seconds ("the
street watches whoever is moving", "they remember", "what you believe the street
knows") and **none of them is demonstrated.**

Topic 25 found the one property shared by both cases where a memory system
landed loudly rather than quietly: it interrupted the player rather than
colouring a greeting. An orc came back with the scar and mentioned it. Step 4 is
that, and it is the only one of the four a toast cannot fake.

## The negative example I would keep in mind

Dishonored's Chaos system runs invisibly through a mission and reports
afterwards, tallying your kills and detections at the end. The reported player
experience is that it felt like being **penalised**, not like understanding a
system.

That is exactly the shape a day-close summary of "what the town now knows" would
take, and it is the obvious thing to reach for.

## The cheapest thing that is not a toast

Canon already has it: "What the town calls you reads out your standing: the new
owner, then Novak, then Tom, then Toma."

A stranger calling you "the new owner", and somebody twenty minutes later
calling you "Novak", is the world showing you it kept track. In the game's own
register, with no hint box, no crime, no witnesses and no rumour hops.

Topic 25 reached that conclusion from watching how players behave. This topic
reached it from the clock. Two pieces of research arriving at the same answer
from opposite directions is the strongest agreement I can offer you.

## The one number I would measure next

**How long a rumour actually takes to make its first hop in play.**

Every input exists: the decay rate, the sharing floor, the six-metre talk
range, the band system, and now the clock. No run reports it. It is a
single number, it decides whether condition 2 is reachable at all, and nothing
in the verdict carries it.

## One ordering thing worth a look

Phase 2's gate is your feel check. The first hour is typed phase 3.

So the feel check is scheduled to happen before the thing that would make a
first session legible exists.

---

EGRESS NOTE, standing in every delivery: one route out of this container reads a
page in full, and it reaches source repositories and package registries only.
The design writing cited here is search-engine summary and labelled as such.
