# The hardware floor: a number, at last

Research topic 2. This has been an open question since the respec and nothing
has ever specified it. Here is a number, how I got it, and the uncomfortable
part.

## The number

**Minimum: 12 GB of graphics memory, 16 GB of system memory, a 6-core processor,
an SSD, 1080p at 30 frames per second.**
**Recommended: 16 GB graphics, 32 GB system, 8 cores, 60 frames per second.**

Roughly 45% of people on Steam today have 12 GB or more. Roughly 32% have 16 GB
or more. For comparison, Kingdom Come 2's minimum is a 6 GB card and its
recommended is a high-end modern one.

Our floor is higher than theirs, and it is higher for one reason: they only have
to fit a game on the card. We have to fit a game, a conversation model and a
voice model on the same card at the same time. Almost no shipped game does that,
which is why no published guide answers the question and I had to build the
number out of three pieces.

## The uncomfortable part

**Your machine has 9.98 GB, and the three pieces do not fit in it.**

Adding them up with the most generous assumptions I can justify: about 6 GB for
a dense street, about 5 GB for the voice, about 2 GB for a small conversation
model. That is 13 GB on a 10 GB card. With less generous assumptions it is 19.

I want to be careful about what that does and does not mean. It does not mean
the machine cannot build the game: it can render the street, and it can speak,
and it can do either alongside the other. It means it probably cannot do all
three at once at the visual bar. And the fourth condition of the Meridian Test
is you, on a free evening, choosing to play this over Kingdom Come 2, which
means the machine has to run the whole thing eventually, or that test cannot
happen on it.

I am not recommending you buy anything. There is a much cheaper answer first.

## The thing that is actually too big is ours

The surprise in this topic was not the graphics card. It was the voice.

Our own export report, run on your machine in August, reads the files off disk:
the two speech graphs are about 3 GB each, and the audio graph another 2 GB. The
voice is the single largest thing on the card. It is bigger than a conversation
model. It is possibly bigger than the street.

And it is big for a fixable reason. The model's weights were published in a
half-size format and we exported them at full size, doubling everything. The
attempt to fix that in August failed, because the conversion broke the model's
ability to decide when to stop talking.

Topic 1 recommended evaluating Resemble AI's new smaller version of the same
engine, for speed. This topic wants the same evaluation for size, for entirely
separate reasons. Two topics arriving independently at the same next step is the
strongest signal I have produced so far, and it makes that evaluation the
highest-value cheap thing on the board.

If the voice comes down from 5 GB to around 1.5 GB, the floor drops toward 10 GB
and your machine is back inside it.

## One decision this exposes that nobody has made

**Nobody has ever said how big the conversation model is.** It is the difference
between 2 GB and 6 GB, which is the difference between fitting and not.

Worth knowing: your own pillar says the conversation model classifies and picks
from closed sets, and never decides outcomes, because the deterministic code
does that. That is a much smaller job than writing free-form prose, and small
jobs suit small models. There is academic work on exactly this, NPC dialogue
models under a gigabyte on consumer hardware, which I could not read because the
paper host is blocked from where I work. It should be read.

## What I would measure next, all cheap

1. **How much memory the Unreal street actually uses.** Never measured. The 6 GB
   above is my assumption and it is the shakiest number in the whole calculation.
2. **Whether the two speech graphs share their weights or load two copies.** One
   line of a probe answers it, and it is worth 3 GB either way.
3. **Whether a small conversation model is usable on your processor rather than
   your graphics card.** You have 32 GB of system memory and six cores. If it is
   fast enough there, the largest competitor comes off the card entirely and the
   arithmetic changes shape.

## What this number is, and is not

It is a **memory** budget: what fits. It says nothing about whether the game
runs smoothly on a 12 GB card, which is a separate question about frame time and
is the next performance topic in my queue. Memory is a wall and frame rate is a
negotiation, so I did the wall first.

One number in it is assumed rather than measured (the street), and it is the
most likely way this is wrong. If the street wants 8 GB rather than 6, the floor
becomes 16 GB, and that would be a different conversation.
