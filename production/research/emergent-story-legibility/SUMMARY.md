# Making an emergent story followable

Research topic 7. Our gossip means nothing if a player cannot follow it. This is
the third time my own work has arrived at this problem from a different
direction, so I have written it as a live issue rather than a survey.

## Three games, three genres, one answer

**Do not summarise. Enumerate.**

RimWorld shows you, for every colonist, a list of every individual thought they
are having and the number each one contributes, adding up to their mood. Disco
Elysium shows you every modifier and where it came from before you commit to
anything. Shadow of Mordor catalogues what you did to an orc and then has the orc
say it back to your face.

Three completely different games, and all three make a simulation legible the
same way: by showing the working rather than showing the result.

We already know how to do this and have only ever done it for ourselves. There
are exactly two functions in our codebase whose job is to print which part of a
number moved and why, and both were written to debug our own instruments. Your
own ruling on information already asks for exactly this pointed at the player,
and it is not built.

That is now the second time I have recommended it and the third source.

## The one comparison that should sting a little

Shadow of Mordor's entire reputation rests on two things. It remembers what you
did to an orc. And the orc tells you about it next time.

We do the first. Our own measurements say we do not do the second: every
recognition moment measured in the shipped build landed below the level where
anybody comments, 1944 times out of 1944, so nobody says a word to you. Our notes
put it better than I can: "the code runs and the street is silent."

A memory nobody voices is indistinguishable from no memory. We have the harder
half already built and the famous half missing.

Mordor pairs the callback with three other things, and it is worth seeing where
we stand on each: orcs have a unique name, a unique voice, and visible scars from
what you did to them. We have nineteen cast voices that no record says anyone has
heard in a build, a population generator our own notes say "supplies names, not
people", and the appearance idea I have now recommended four times.

## The cautionary tale

Dwarf Fortress has the deepest simulated history any game has ever generated.
Its players cannot read it. The community wrote external software to make the
game's own history legible, keeps rewriting it, and the wiki recommends using it.

A simulation that generates history and a game that tells you about it are two
different products, and the first does not give you the second. If we score 93
on social memory and nobody can follow it, we have built Dwarf Fortress with
better lighting.

## The thing nobody here has written down

RimWorld's designer keeps the graphics simple on purpose, and the reason is
narrative. He cites apophenia, the human habit of seeing connections between
unrelated things, and argues that a minimal representation leaves room for
players to build the story in their heads.

Which means **photorealism costs us something, and it is not only money.**

A drawn square with a name invites you to imagine a face and a history, and your
imagination does that authoring for free. A photoreal face has already specified
the face. There is less room to project, and everything the projection would have
supplied has to come from the game instead.

I am not arguing against the visual bar. It is decided, reasoned, and it is the
entry condition for the first part of the Meridian Test. But it has a consequence
that I do not think has been stated anywhere: **a photoreal game cannot rely on
the player to make the story. It has to say more than a stylised game would, not
less.**

And Mordor is the proof that this is doable. It is not a coincidence that Mordor
is the photoreal one of the three.

## What follows

1. Enumerate rather than summarise. Second recommendation, third source.
2. The callback is the whole of Mordor, and our 1944 out of 1944 is that system
   with the last step missing.
3. A memory needs something you can read afterwards, and building that is a
   separate job from building the memory. Dwarf Fortress proves it. Your
   information ruling already specifies ours and the spec row is unbuilt. This is
   the third of my deliveries to land on that same unbuilt row.
4. Photorealism raises the legibility bar rather than lowering it. That is a cost
   of a decision already taken, and better known than discovered.

## What I could not get

The Nemesis talk is behind the conference paywall, as the Hitman talks were. So I
have the philosophy and not the techniques, and the part I most wanted, how they
designed what they call "exceptional moments", is exactly the part I could not
read. I also could not establish whether the orcs' callback lines are written
templates or generated, which matters enormously for what the same thing would
cost us.
