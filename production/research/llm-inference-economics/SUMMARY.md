# What it costs every time somebody in Meridian opens their mouth

Research topic 19. Topic 2 asked what fits on your graphics card. Topic 17
asked what runs smoothly. This one asks who pays for the talking, and how much.

## What the game does today, which surprised me

**It phones Anthropic, and the player pays.** The conversation code in the
project is a cloud client. There is no local model anywhere, and no open model
has ever been named in this project. The how-to-play file says the player
presses F2 and enters their own API key.

That was a deliberate deferral, recorded in the roadmap: four options named,
decision postponed, and the code written so that changing later is not a
rewrite. That was the right call. This is the evidence coming back for it.

## The number

Every time a character says one line, the game sends them a briefing of about
**7,400 characters**, and it sends the whole thing again for the next line, and
again for the line after that. I measured that by running the project's own
probe rather than guessing: the character cards are 4,600 to 5,400 characters
and the rules block is another 2,900.

Using the project's own price list, and its own assumption of twenty
conversations an hour:

| | cost per hour of play |
|---|---|
| all cheap-tier characters | **$0.36** |
| a fifth of them on the good model | **$0.50** |
| all on the good model | **$1.08** |

We set ourselves a target of **$0.05 an hour**. We are between seven and twenty
times over it.

## The free win

**Nothing caches that 7,400-character briefing, and it is the one thing in the
world caching was invented for.**

Anthropic charge a tenth of the normal price for re-reading something they have
already seen. Turning that on is a header and one marker on a request the game
already sends. No model change, no redesign.

It takes about 60 percent off every row of that table. All-cheap goes from
$0.36 to $0.14.

## A fairer way to read the target

Turned round, our $0.05 budget buys:

- **42 short exchanges an hour** with caching on
- **17 an hour** as things stand today

So the target is not mad. It is a target for a game where you have seven or
eight proper conversations an hour. It is impossible for a game where you have
twenty. **Nobody has ever said which of those LEDGER is**, and that is the
question underneath the money.

## The local option, honestly

A model running on the player's own machine costs nothing per hour. It gets
paid for in three other ways, and here is where the published numbers land.

There is an academic paper this year on exactly our problem, one model per
character with swappable memory. Its measurements:

- A **small model, about a billion parameters**: 800 MB of graphics memory,
  answers in under two seconds. **Fits our budget.**
- A **seven billion parameter model**: 4.2 GB, answers in five and a half
  seconds. **Too slow** for us, and too big for your 10 GB card once the street
  and the voice are on it.

Our own latency budget, from the plan, is about four seconds to first spoken
word, and the speech half already claims 1.2 of those. So the talking model has
about 2.8 seconds. The small one fits. The big one does not.

The catch is not speed or size, it is **skill**. The job is two jobs. Picking
from a list of options is easy and a small model does it fine. But the same
prompt also demands period British dialogue while obeying about fifteen
simultaneous "never do this" rules, including never inventing a person who does
not exist. Holding many negative rules at once is exactly what small models are
worst at.

**Nobody has ever tested this.** We have a probe that talks to characters, and
the client is a one-method interface. Putting a small local model behind it and
seeing whether it can hold a character is an afternoon.

## The thing that could bite us late

**The licence allowlist has no entry for a language model at all.**

It covers voices, 3D, characters, faces, music and maps. It is the law of this
project, it is the reason nothing unlicensed has ever shipped here, and the
second pillar of the whole game is a live language model that it does not
mention.

That is fine while the model is a cloud service, because we ship nothing. The
moment we bundle one it becomes the first thing in the game whose licence that
document has never considered. Worth knowing: Llama's licence reportedly
excludes parts of the EU, which is the exact reason the allowlist already bans
one of the 3D tools outright.

## The question for you

**Who pays for the conversations?** The four shapes on the record are: the
player brings their own key (today), we run a server, we charge a subscription,
or we ship a model in the box.

I am not going to pick one and I do not think you need to yet. What the numbers
say is that it need not be all-or-nothing: the code already sorts characters
into a cheap tier and a good tier. The obvious shape is the crowd running
locally and free, and the ten people who matter running on a proper model where
the writing has to be good.

## What I would do next, cheapest first

1. **Turn on prompt caching.** 60 percent off, no design change, one afternoon.
2. **Print the cost per hour.** The tracker counts tokens and nothing ever
   divides by hours. We have been aiming at a target we have never once
   measured.
3. **Put a small local model behind the existing interface and see if it can
   hold a character.** That is the whole local question, answered by experiment
   rather than by me quoting benchmarks.
4. **Read the actual licence file of whichever models we test**, before anyone
   engineers against one.

One process note: the single most relevant paper here is on arXiv, which is
blocked from where I work. This is the second research topic in a row stopped by
that exact wall. Anything you can open on your own machine, I cannot.
