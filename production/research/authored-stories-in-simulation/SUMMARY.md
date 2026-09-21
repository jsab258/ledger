# Writing a story the world can argue with

Research topic 15, and the last of batch 2. You said this one feeds a writing
lane you intend to open later, so I have written it as preparation for whoever
takes that job rather than as a survey.

## The good news, which nobody has collected in one place

A writer joining this project gets three guarantees most people in this position
do not.

**The language model cannot contradict them.** In most projects that mix AI
characters with a written story, the generative layer is exactly what breaks the
story, because a model can say anything. Here it structurally cannot: our rule is
that the model classifies and never decides, and the deterministic code executes.
A writer here is writing against a simulation, not against a text generator,
which is a much older and better understood problem.

**Nothing can be un-happened.** Because nothing is ever wiped, a writer never has
to handle the case where an event their story depends on gets erased by a reload.

**And the list of things the world CAN take away from them is short.** From
reading the code, the simulation can contradict a writer on exactly five things:
who is alive, who knows what, who is where, who will talk to the player, and how
the law stands. It cannot contradict canon, the existence of the acts, or
anything the content rule screens.

Handing a new writer those five things on day one is worth more than any
technique, because a writer who knows what can be taken away can write around all
of it.

## We already have the best worked example, in our own code

The technique this whole topic is about is written more clearly in one of our own
files than in anything I found published. `Beat.cs` describes an authored social
obligation and explains itself like this:

"Not a hard timer: attending is presence during the window, the windows overlap
enough that a determined player can thread both, and skipping costs standing with
a person, never the game."

That is the whole answer. The beat asserts almost nothing about the world. It does
not need a place to be safe or a person to be alive at a given minute or an
earlier scene to have gone a particular way. It asserts a window of time and
attaches a social cost, and when it fails, somebody remembers being stood up
rather than a quest breaking.

**That file should be the writing lane's first reading.**

The general version: gate beats on states rather than on sequence. "After act
two, scene four" breaks when a player does things out of order. "When at least two
of the dockside crew believe the player was at the warehouse" cannot break,
because it is a question the simulation can always answer.

## Two techniques from elsewhere worth having

**Script the beginning and nothing else.** Shadows of Doubt has one opening case
that is far more scripted than the rest of the game, to teach the fundamentals,
and then hands over to the simulation. Kingdom Come does it, Hitman does it. The
logic is that the most authored content belongs at the front, where the world is
most predictable because the player has not changed it yet. That lands directly
on our first-hour work and on the thirty-minute condition in your own test.

**Never let a beat fail the run.** The immersive sims are praised specifically
for avoiding the "spotted, game over" failure, and our own Beat file says the
same thing in three words: "never the game". A beat that can end the run forces
the writer to guarantee its preconditions, and guaranteeing preconditions is
exactly what a simulation cannot do.

## What the writing lane needs before it can start

1. The five-item contradiction list above.
2. `Beat.cs` as the exemplar, and a ruling on whether every authored beat has to
   follow its shape.
3. A published list of which simulation facts a writer is allowed to gate on.
4. **An answer to an open canon question.** Canon still records as open whether
   Tom Novak, the three acts and the empire roster survive as the baseline at
   all. A writing lane cannot open before that closes, because it decides whether
   they are writing or rewriting.
5. A tool, and the knowledge that the industry-standard one for this job froze
   under a script the size of Disco Elysium's.
6. Clarity on which parts of the content rule a machine enforces and which are
   on them. Right now the live conversation path has none of it enforced.

## The thing that worries me

Our own notes on the three acts say: the drafts exist, their beats and endings run
in the simulation, "and no record committed here says any of it has been read by
somebody playing."

The academic literature worries about whether players notice the stories a
simulation generates. We have the stronger version of that problem: whether
anybody notices the story we WROTE. That is the same conclusion I reached in the
legibility topic from the other direction, and arriving at it twice from opposite
ends makes me trust it.

## One thing I could not check, and a writing lane should first

I did not read how the existing act files gate their beats, so I cannot tell you
whether the drafts are already written in the robust style `Beat.cs` describes or
in the fragile one. That is a single session's work and it is the first thing
worth knowing.

I also could not find a single shipped game that combines a live language model
with an authored act structure. Nobody in the AI-character space has an act
structure to protect. So this particular combination has no precedent I could
find, which is either the opportunity or the warning.
