# In 1990 forensics could confirm a suspect. It could not find one.

Research topic 29. You asked for a short period-specific list of what a scene of
crime officer could collect. The list is short, and why it is short is the
useful part.

## Two dates decide everything

- The **UK National DNA Database** was established on **10 April 1995**.
- The **national automated fingerprint system** was established in **1999**.

Meridian's window closes in 1992.

So in our game there is **nothing to search a sample against.** A stain or a
print can be compared to a person the police have already got. It cannot be run
against a country to produce a person they have not. There are no cold hits in
1990.

The one partial exception is local and it proves the rule: a fingerprint can be
compared by hand against that force's own collection, so it identifies somebody
who already has form with that force, and nobody else.

## DNA is four years old and it is fragile

It exists. It debuted in a criminal investigation in October 1986 and the first
conviction came with Colin Pitchfork's sentencing on 23 January 1988, the year
our window opens. Courts accepted it by 1988. It is news, not routine.

And the method of the period needed:

- roughly **a stain the size of a coin**, not a trace
- **undegraded** DNA, destroyed by "heat, moisture, or time"
- **several days** to process

That last set of constraints is a gift. Canon's visual target is "photoreal,
wet, overcast, grimy Britain", and weather and grime are the stated strategy.
**The rain that defines how Meridian looks is the same rain that ruins the only
new forensic technique in it.** A bloodstain left out on a wet night in a port
town is not a DNA sample by the time anyone lifts it.

## The list

Everything a SOCO could collect in 1990: fingerprints, footwear marks, blood
(grouping, and DNA if the sample is generous), hairs, fibres, glass, paint, tool
marks, photographs.

Read down it and one thing is true of all of them: **every technique is
comparative.** Each answers "is this the same as that". Not one answers "who".

One period detail worth having: **in 1990 the scene examiner and the fingerprint
expert were the same person.** The two roles were split later. So the person who
lifts the mark is the person who compares it: one named character, not a
pipeline.

## Why this is good news for us

We model **no forensics at all.** I grepped for fingerprint, forensic, DNA,
SOCO, scene of crime and swab: six hits, all substring false friends.

What we model instead is `Traces.cs`, and it is the right thing. A stain has a
strength that dries toward a floor, washes off in 25 minutes given water and
privacy, counts as a mark above 0.3, is **noticeable at a distance in a light
level**, and carries a **social cost scaled by how well someone knows you**. An
item carries an origin and a history that is never cleared.

That is a **social** trace model. A stain in this game is seen by a person and
costs you standing. It is never swabbed.

Which lands exactly where Part 1 of the research lands. In 1990 forensics cannot
turn a crime into a name, so something else has to. In Meridian that something
is people: perception, memory, gossip, informing. `Informing.cs` already says the
same thing in its own words: "a true accusation nobody will corroborate is
ignored. A false one three people will swear to lands."

**The period does not constrain the premise. It enforces it.**

## The one thing to guard against

When forensics does eventually get built, the temptation will be to make it
satisfying, and satisfying forensics is modern forensics. A lab that names a
stranger from a smear on a door handle would quietly remove the reason witnesses
matter.

A 1990-accurate layer would: produce comparisons and never names; confirm or
refuse somebody already suspected; take days for anything involving DNA; be
destroyed by weather the game already simulates; and be run by one person who is
also the fingerprint expert.

And even its best result against an unknown offender is a local fingerprint hit,
which is to say it works on people who already have form, which is to say on
people the town already knows something about.

Even the forensics of 1990 routes back through what is already known about
somebody.

## What I could not find

Nothing here is a primary source; the journals and the College of Policing pages
are unreachable. And the detail I most wanted is missing: what a **provincial**
force could actually get in 1990, as against what existed in the country. How
long the queue at a regional laboratory was, and what it cost, is exactly what a
game would want, and no source I could reach says.

---

EGRESS NOTE, standing in every delivery: one route out of this container reads a
page in full, and it reaches source repositories and package registries only.
Everything cited in this topic is a search engine's summary and is labelled so.
