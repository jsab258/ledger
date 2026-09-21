# What Disco Elysium has that we do not

Coverage audit, game 4 of 5. I listed 26 things it contains and checked each
against our 91 systems. This is the shortest yes list of the four, and that is
the right answer rather than a thin pass: almost everything Disco Elysium is
made of is character progression, and you ruled years ago that our player does
not get better at anything. Five of its twenty-six systems are struck by that
one ruling alone.

But the two things worth taking are worth more than their number, and one of
them closes a hole in a decision you already made.

## Two things to take

**1. Show the working.**
Before you attempt anything in Disco Elysium, it shows you the whole sum: the
skill, every single thing helping or hurting you and where each came from, and
the odds. You never feel cheated, because you can always see why.

You already asked for this. Your ruling on information says that when someone
believes or doubts the player, the actual memory that made them believe it has
to surface, because otherwise it reads as the game deciding arbitrarily. That
surface does not exist yet. What does exist, and this is the useful part, is
that we already write code in exactly that style: there is a function in the
game whose entire job is to print which part of the police pressure moved and
why. We built it for ourselves, to debug our own numbers, and never pointed it
at the player. Disco Elysium is the proof that pointing it at the player makes a
game clearer without making it less atmospheric, at a scale of information far
past anything we will have.
COST: small. The thinking is done and the habit is already in the codebase.
What is missing is a screen.

**2. Failing should give you something, not take something away.**
In Disco Elysium a failed check usually opens different content rather than less
content, and the game is famous for it. Our own measurements say we currently do
the opposite: across ninety caught lies, not one spoken line was different, and
telling the truth ends at exactly the same suspicion number as saying nothing,
so honesty currently pays nothing.
A failed attempt to lean on someone should produce a scene, and a memory of you
having tried. That is worth more than a refusal, and it is the kind of cost
that lands on writing rather than on code, which is the right way round for us.
COST: moderate, and nearly all of it is writing.

## Two questions only you can answer

**Does the game tell the player when a moment is permanent?**
Disco Elysium marks some choices as one attempt only and says so up front, and
the rest as retryable. Our whole premise is that nothing is ever wiped. So: do
we warn people when they are about to do something the town will remember
forever? Telling them is either the kindest thing in the design or the thing
that drains all the tension out of it, and I genuinely do not know which. It is
the same family of question as the save one from game 1 and they should be
answered together.

**Nothing else here is a question for you.** The rest of the game is either
ruled out already or belongs to a different kind of game.

## Two numbers you should have

Not recommendations. Measurements to hold us against.

**A million words, fourteen months, three directors.** Disco Elysium's script
is about a million words and The Final Cut voiced every one of them. It took a
funded studio fourteen months, with three full-time voice directors and dozens
of actors. One narrator alone spent eight months. That is what voicing a game
like this costs the human way, and it is not payable here by anyone at any
budget. Which is the argument for the live voice pipeline stated as a
measurement rather than a preference.

**The professional tool broke.** ZA/UM wrote that script in Articy, which is the
industry-standard tool for exactly this job, and it slowed and then froze under
the volume, to the point where they describe losing editorial control of their
own text. We intend more authored dialogue than we currently have any tool for.
I have flagged this as a research topic that is not in my queue.

## What I said no to

The famous parts, and deliberately. The twenty-four skills that argue with you
in your head is the single most admired mechanic in modern role-playing games,
and it is Disco Elysium's identity rather than a component: a game with an inner
chorus is a game about a man arguing with himself, and ours is about a town
forming an opinion of a man. Taking it would be copying rather than designing.
The Thought Cabinet, the skill points, the attributes and clothes that give you
statistics all fall to your no-player-progression ruling. The dice are out
because we decided consequences are worked out rather than rolled for.

And one of them would have done real damage: in Disco Elysium time only moves
when you act. Our entire gossip system runs on people being somewhere at a time
whether or not you are doing anything, so an action-driven clock would quietly
delete the mechanism the whole game is built on.

One small thing worth noting. Changing clothes to pass a check is something
Disco Elysium players do freely, because nobody in that world sees you do it. In
ours, changing your clothes is something people notice and remember. Same action,
free there, expensive here, and that difference is more or less the whole point
of what we are building.
