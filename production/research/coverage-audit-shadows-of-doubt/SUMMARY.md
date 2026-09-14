# What Shadows of Doubt has that we do not

Coverage audit, game 5 of 5. I got to pick this one. I chose Shadows of Doubt
(2023) because it is the only game that has ever actually built the thing we are
building: a whole town where every person has a name, an address, a job, a
routine and a memory of what they saw, played as crime. Everybody else fakes a
piece of it with hand-written content. This one simulated it, shipped it, and
got reviewed for it. So it is the only real evidence we have about what happens
when you do this, rather than more argument.

I listed 23 things it contains. Two are worth taking, one is a question for you,
and one is a warning I think matters more than either.

## The warning first

Shadows of Doubt generates its city, its cases and its documents. Reviewers
described the result almost exactly the way your own content rule predicts:
repetitive cities, repetitive cases, repetitive conversations, and specifically
that every office they entered had the identical email about a gambling ring and
every flat had the same letters to old friends. And then the second half, which
is the part that should worry us: once you have done two cases, you only ever
need a couple of names and a fingerprint, because everything else is
interchangeable.

That second sentence is our nightmare, not theirs. Our whole claim is
information. If every letter in Meridian reads the same, then the only
information that ever matters is the small structured bit, and the game has one
best strategy forever.

You already made the rule that prevents this: content gets made piece by piece,
with a spec and someone checking, and no procedural filler without an authoring
pass. This game is the proof that the rule is load-bearing rather than
fastidious. It is also worth noting that our own notes say the population
generator currently "supplies names, not people" and most of the town is a body
with a schedule. That is the first three feet of the same road.

## Two things to take

**1. The man in the lit window is a witness.**
Their citizens can see out of their own windows, and across the street into
other windows, when the light is on. We already have half of this and I do not
think anyone has noticed: our code works out who is in at each hour and lights
their window accordingly, and the comment on it calls a lit window "the
information pillar rather than decoration". But the light only carries
information TO the player. Nobody is looking back out. So right now the man
upstairs is a lamp.
Making him a witness costs almost nothing, because the system already knows he
is in, and it buys the most characteristic witness a British terraced street
has: the neighbour who was up, with the light on, and saw you come back at two.
COST: small.

**2. What you leave at a scene.**
We have blood on your coat, and we have objects that remember who sold them to
you and what you did with them. We do not have the place. Nothing models the
print on the glass, the heel mark by the yard gate, or the thing you dropped and
did not notice.
The period is unusually kind here. In Britain around 1990, fingerprints are the
one mature forensic tool and everything else is absent: no DNA database, no
cameras everywhere, no phone in anyone's pocket, and you have already ruled CCTV
down to two sites with the tape wiped weekly. So a scene in Meridian yields
prints, a footmark, a dropped object and what people remember, and nothing else.
That is a small, readable set of evidence, which is exactly the kind we want.
COST: moderate, and the model it extends already exists.

## One question only you can answer

**A notebook, or a corkboard with string?**
You ruled that the player's own memory is fully surfaced as a journal: an entry
per person and per event, tagged as witnessed, heard or worked out. Shadows of
Doubt uses the other thing instead: a physical board where you pin photographs,
addresses and scraps and run string between them.

A notebook is a list. It holds any amount and never gets confusing. A board is a
space, and it does one thing a list cannot: it shows the connections the player
drew, because the player drew them. That is the difference between being told a
deduction and making one.

The board costs more, is harder to read on a controller, can turn into
busywork, and their reviews are split on theirs. This is not a technical
question, it is what the game feels like to sit in front of on a Thursday
evening, so it is yours. If the answer is the board, be aware it also means
every piece of evidence needs to look like something, which the notebook does
not require.

## One thing for the studio, not for you

Their game does not simulate its town in real time. It works out each day in
advance, ten to fifteen seconds of calculation before the day starts, because
the developer decided doing it live was too expensive. Ours runs live. That is
fine today, but we have never said what a dense street, a local language model
and a voice model all want from one machine at once, and this is the only
comparable game that hit that question and answered it by moving the simulation
off the frame budget. I have noted it for the two performance topics in my
queue; it needs no decision from you.

## What I said no to

Less than usual, because this game collides with almost none of our rules. The
main refusals are their endless generated cases and their generated documents,
for the reason at the top. Their evidence also fades after a few hours, which we
already decided against in the other direction, with a better reason written in
our own code: dealing with blood on your coat should be a decision you make, not
a timer you wait out. And their player is a detective who handcuffs people,
which Tom is not, although it does point out that the missing piece on our side
is being arrested rather than arresting.
