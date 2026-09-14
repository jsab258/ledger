# What happens after arrest

Research topic 14. The honest starting point: **nothing happens after arrest,
because arrest does not happen.** The function exists, and our own homicide file
records that it "has no caller in the whole Game layer". Three separate tiles say
the same thing from different angles, and one of them puts it best: "an arrest
that leads nowhere is a consequence that stops."

So this is about what should happen.

## Most of the writing on this subject is about a problem we do not have

Nearly everything published on failure design is about retry loops: fast retries,
clear feedback, a sense of progress, the player believing they can do better next
time. Celeste, Hades, Mario, the roguelikes. All of it assumes the game sends you
back to a known state.

Canon forbids us that. Nothing is ever wiped, and remediation is behavioural
rather than a reset.

Which leaves us with a different problem, and I could not find it named anywhere:
**failure design in a game with resets is about making the retry interesting.
Failure design in a game without them is about making the CONTINUATION
interesting.** Nobody gets sent back. They carry on from a worse position, and
the question is whether the worse position is worth playing.

## The part that does apply, and it is the thing to watch

One warning comes up repeatedly: the danger of a strong failure state is when it
creates a feedback loop of failure, where being behind makes you more likely to
fall further behind.

**A game built on permanent memory creates that loop by construction.** Get seen,
the town knows, doors close, the police pay attention, the next job is harder,
you are more likely to be seen. Every part of our moat pushes the same way and
nothing pushes back.

And one of our own files says so on purpose. About killing: "Each body you add to
fix the last one leaves you worse off than before the first." That is a designed
death spiral, it is right for killing, and it is meant to be frightening.

The question this raises is whether the same spiral is intended for everything
else, because structurally it is the same spiral.

## What we have to push back with, and two of them are not built

Four things exist in code: arguing a story down, buying or leaning it quiet,
letting it go cold, and pointing the police at somebody else. One of those is
designed to backfire.

Canon names three behavioural remedies: leave, change appearance, rebuild
relationships. **Two of those three are not built.** Changing appearance is the
thing I have now recommended four times across this research. Rebuilding
relationships has no verb I could find at all: how well somebody knows you is
currently computed from whether they share your home, walk with you, are in the
cast, or have heard of you, and none of that is something the player can move.

So the spiral has four brakes, one of which is designed to fail, and the two
remedies canon puts first are missing.

Whether four brakes are enough is the question the whole topic turns on, and I
cannot answer it, because nobody has played a run against a town that hates them.

## Three things worth taking

**Make the failure state a place, not a screen.** Kenshi's prison does not stop
the game: you are still somewhere, with things to do, and you can collect
disguises and try to get out. The principle is that a failure state with verbs in
it is a location, and one without them is a loading screen with a story attached.

And we already have the verbs. The policing research handed us the structure
without anybody having to invent it: twenty-four hours, a review at six by an
inspector who is not on the case, further reviews every nine, a custody sergeant
who is independent, a custody record you can later obtain, and the period rule
that **saying nothing costs you nothing in court.** That is a scene with a clock,
a person to talk to, and one real decision.

**Make a remedy cost something specific.** Sunless Sea's best detail is not that
you inherit things from your dead captain, it is that inheriting the map locks
you out of the experience you would have got by exploring. Taking one thing costs
another. We should not build heirs, but that shape transfers: our remedies
currently reduce a number, and a remedy with a price is a decision instead.

**And the cautionary one.** Failbetter, who built the most admired
permanent-loss system of their decade, decided afterwards that their own death
was too punishing and deliberately softened it in the sequel. That is the most
relevant data point available to us, and it is not encouraging about erring
toward severity.

## The negative example, for contrast

Skyrim's prison, in a critic's words, "is built around letting criminals get away
with their crimes": the game puts an escape item in your cell, and a fine avoids
jail entirely. The tell is not that you can escape, it is that escaping is free.
That is a designer who did not believe the failure state was worth playing.

Our risk is the exact opposite, and the two are worth seeing side by side.

## The gap in this one

**Pathologic 2.** A game about a town, a clock you cannot stop, and permanent
loss, and the game most likely to have actually solved the continuation problem.
It was on my shortlist when I picked the fifth game for the coverage audit and
lost to Shadows of Doubt. It is the biggest hole in this topic and I would go
back for it.
