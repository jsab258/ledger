# When a world remembers you, what players actually do is tell somebody

Research topic 25, the last one. I went looking for how players behave when a
game remembers them, and found something slightly awkward about how we plan to
measure it.

## What players demonstrably do

Three cases where a game really did remember, and in all three the observable
behaviour is the same: **players retell it.**

- **Shadow of Mordor's Nemesis System.** Orcs that beat you came back with the
  scar and remembered you. Its design director said the goal was that players
  could "create and share their own experiences" rather than that they would
  notice the memory.
- **Dwarf Fortress and RimWorld.** Called "story generators": thousands of
  player-written accounts online. Boatmurdered, one shared fortress, is credited
  with popularising both the game and the Let's Play format.

Nobody measured "players felt recognised". What is measurable, in volume and
unprompted and for years, is that people wrote it down and told other people.

A small thing I liked: our own code already models NPCs retelling what they saw,
with the comment "memory hardens as it decays". The success signal for the game
turns out to be the player doing the thing the characters already do.

## The awkward half

I searched four different ways for research on whether players **notice** a
memory or reputation system that is working properly. There isn't any.

What there is research on is the opposite: **players quickly notice when NPCs
forget.** Timeline errors, impossible claims, characters who do not remember a
previous conversation. That is a first-order requirement, and it is well
studied.

So the evidence is lopsided, and it is worth saying plainly:

> **A world that remembers mostly buys the absence of a failure. Forgetting is
> loud. Remembering is quiet.**

That is worth a great deal. It is also almost invisible while it is working, and
it will not turn up in a thirty-minute test on its own.

## But the two loud cases share one property

Nemesis was not quiet. It was the most talked-about feature in its game. The
difference was not the memory, it was that the orc **came back** and said
something about it.

Boatmurdered is not "the fortress remembered". It is that the remembering
produced an event somebody wanted to describe.

**If the world is going to visibly know you, something has to come back.**
Recognition that only tints a greeting is the quiet kind.

## The thing I would actually fix

The Meridian Test says:

> Within those **30 minutes** the world visibly knows them at least once.

The roadmap's phase 1 gate says:

> witnessed crime reaches a second and third NPC within **one in-game week**.

Those are the same claim on two clocks that do not convert. One is half an hour
of a stranger's first session. The other is a week of simulated time.

I could not find a play-mode clock rate anywhere in the project. The only figure
that exists is twenty game-minutes per real second, and that is the CI sim,
which has to cover eleven days in a few minutes.

**The gossip gate proves the rumour spreads. It does not prove it spreads fast
enough for anyone to see in a first session, and nothing measures that.**

Worth knowing: the exact file that carries that twenty-minutes figure also
records an incident where confusing game minutes with real seconds caused four
attempted fixes to fail in a row. We have already paid once for mixing these
units.

## The cheapest thing that would meet condition 2

Canon already has it: **"What the town calls you reads out your standing: the
new owner, then Novak, then Tom, then Toma."**

That is a recognition signal a stranger can hear in the first half hour. It does
not need a crime to have happened, or witnesses, or the rumour to survive seven
hops of decay before somebody will repeat it. It is a change in the word a
person uses when they speak to you.

For a first session it is probably worth more than the whole gossip mill, which
needs an event and time the player has not spent yet.

## One thing about the whole queue, since this is the last topic

Across twenty-five topics the thing that came up most was not a missing feature.
It was a **number that exists for one half of a question and gets quoted for
both**: a frame time measured without a device name, a cost target with no
denominator, a gossip gate that proves propagation and reads as though it proved
timeliness.

That is not a criticism of the project. It is a compliment to it, because the
only reason I could find those is that almost everything here is measured and
written down. You cannot catch a half-measured claim in a project that measures
nothing.
