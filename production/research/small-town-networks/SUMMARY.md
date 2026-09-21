# Who knows whom in a small town

Research topic 11. You wanted this so schedule intersections are not uniform.
The short answer is that the non-uniformity is already in canon and nothing
reads it.

## The shape of a real network

People's relationships come in layers, not a spread. The well-known figures are
five, fifteen, fifty, a hundred and fifty, each about three times the last. And
the attention is wildly lopsided: people spend nearly 40 percent of their social
effort on the innermost five, and 60 percent on the innermost fifteen. The fifty
layer is described as the one that is "less about emotional support and closeness
and more about providing useful connections and information", which is exactly
the layer a gossip game lives in.

A uniform spread of tie strengths is not a simplification of that. It is a
different thing.

## Your seven districts are the network structure

Two forces build real networks: people befriend people like themselves, and
friends of friends become friends. Together they reliably produce, in the
literature's words, "densely-connected, homogeneous parts that are weakly
connected to each other".

That is a description of the Hook, Copper Row, the Exchange, the Parade,
Fairview, Ironside and Gullwing. The districts are not set dressing over a social
network, they ARE its shape, and so are the three rival outfits.

So the answer to "make intersections non-uniform" is not to invent a
distribution. It is that canon already specifies one and the gossip code does not
consult it. A tie that crosses from the Hook to the Exchange is not a weaker
version of a tie within the Hook; it is a different kind of thing, and it is the
only route between two communities.

## Which makes last week's finding worse

Last topic I reported that our gossip passes rumours best between close friends
and worst between acquaintances, which is backwards from the standard finding
that information crosses a network through weak ties.

Put that together with the districts. If each district is a dense cluster joined
to the others by a few weak ties, then those few ties are simultaneously the only
bridges out and, in our model, the worst carriers. **Talk would pool in the
district where it started and reach the Exchange, if at all, as a whisper.**

That might be exactly the town you want. A crime in the Hook that the Exchange
never hears about is interesting. But right now it is the accidental product of
two choices nobody examined, and it is the biggest structural consequence I have
found in the gossip system.

## A neat one: the cast should have no strangers in it

Our plan is thirty to fifty authored residents, with a crowd of walkers on top.

Thirty to fifty fits entirely inside one person's information layer. So among the
authored cast, nobody should be a stranger to anybody: everyone has at least heard
of everyone. And the crowd should be nothing but strangers.

That is a clean split, and it makes our own code's argument sharper. Our
acquaintance file already says a face in the crowd "cannot name you at any
distance, in any light, however long they stare, which is correct, and is what
makes a busy street safer than an empty one where your neighbour lives." The
consequence: the player's safety depends on WHICH crowd, and the authored cast is
never cover.

## Something I found on the way that you should know

Our acquaintance file opens by explaining that the top rung of recognition, the
one the whole design turns on, has never been reachable, because no caller has
ever supplied a familiarity value, so every witness scores zero and "every person
in the city is a stranger to a man they have known for three acts".

**That is no longer true, and the file still says it is.** Someone wrote the fix:
there is now a familiarity function on the game controller, assembled from whether
the person shares your home, walks with you, is in the social graph, or has heard
of you, and the simulation passes it into both call sites. A reader arriving at
that file today is told the top rung is dead when it is not.

What I could NOT establish, and it matters: our inventory still records that
recognition landed below the level where anyone comments, 1944 times out of 1944.
I cannot tell from here whether that measurement came before the fix or survived
it. So the honest statement is narrow: **that number can no longer be blamed on a
missing familiarity function, and what it should be blamed on is now unknown.** A
run would settle it and I cannot make one.

I also noticed one hardcoded number in passing: a walker file calls the
recognition check with familiarity written in as 0.5 rather than taken from the
function. That value sits above the recognition threshold, so on that path every
crowd walker is treated as somebody who can name the player. I have not traced
what it feeds, and I am reporting rather than interpreting it.

## What I could not get

The papers themselves, again, because the hosts are blocked. Worth knowing that
Dunbar's numbers are contested in a literature I only have in outline, and the
current argument seems to be about how much people vary around them.

And I found nothing at all on whether a British small town in 1990 has a
different network shape from the general case. Everything above is general
network science.
