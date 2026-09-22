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

[CUT HERE: part 1 of 2. The rest follows as its own message, because the wire refuses anything over 4096 characters and nothing splits it automatically.]
