# What a busy street costs, and the number nobody can set yet

Research topic 17. Topic 2 asked what fits on the graphics card. This one asks
what runs smoothly. Memory is a wall; speed is a negotiation, and this is the
negotiation.

## The headline, and it is not a number

**The roadmap says phase 1 is finished when the game "holds frame budget at
target resident count". Neither of those two numbers exists anywhere in the
project, and they cannot be set, because nothing in the Unreal build measures a
frame.**

We do have a frame-rate readout. It is careful, it is well argued, and it is in
Unity, which you retired on 10 September. The Unreal side has one file whose
name is FrameStats, and it turns out to measure the brightness of screenshots.

That is the finding. Not a missing target, a missing ruler.

## The uncomfortable arithmetic

Unreal's two headline features are Lumen, the lighting, and Nanite, the
geometry. Epic publish what they cost, on a PlayStation 5, at 1080p:

- At 60 frames per second: about 8.5 milliseconds of a 16.7 millisecond frame.
  Half the frame, gone, before we draw anything of our own.
- At 30 frames per second: about 12.5 milliseconds of a 33.3 millisecond frame.
  A third, and there is real room left.

And Epic's own demonstration city, the Matrix one with crowds and traffic, runs
at 25 frames per second at 1080p on a graphics card faster than yours.

## The good news, which is the same fact read the other way

That demo is a whole streaming city. Our street is 42 metres long.

The small footprint in the goal statement is not a compromise we are making on
the visuals. It is the thing that pays for the visuals. Every argument in this
topic that ends well ends there.

## The idea I would most like you to take from this

**"How many people" is two questions and we have been asking it as one.**

People the game is quietly simulating, who remember you and gossip about you,
cost us a measured 0.07 milliseconds each, per frame. Sixty-five of them is
about a third of a fast frame, which sounds bad until you notice that we
currently update every one of them sixty times a second. Nobody's memory of
you changes sixty times a second. Update the distant ones once a second instead
and the same crowd costs almost nothing, which is precisely how the two games
that do this well (the Matrix city demo, and Shadows of Doubt) get their
numbers.

People actually drawn on screen, with a body and a walk and a shadow, cost
somewhere between one and a half and four times that each, and that cost cannot
be avoided the same way, because a body drawn at half speed looks like a body
drawn at half speed. In Unreal every walking person also forces the shadow
system to redo work every single frame, which a standing building does not.

Our moat lives entirely in the one that can be slowed down. Your memory, your
gossip, your consequences: none of it needs to happen at frame rate. Only the
bodies in shot do.

So the phase 1 gate wants two numbers, not one, and the expensive one is the
one that has nothing to do with what makes this game different.

## The question only you can answer

**Is LEDGER a 30 frames per second game or a 60 frames per second game at
1080p?**

I am not asking rhetorically and I do not think 60 is obviously right. Three
things point at 30:

- The published baseline for Unreal 5 games is a Ryzen 5 5600 with an RX 6700.
  That is your machine, part for part. Our development machine is the industry's
  minimum spec machine.
- Kingdom Come 2, the game the whole bar is set against, is a 60 frames per
  second game on a card like yours at MEDIUM settings, and about a 25 frames per
  second game at maximum. Even the comparator trades one for the other. And it
  gets its look out of an older, leaner engine than ours, without Lumen or
  Nanite at all.
- At 30 there is room for the photoreal lighting. At 60 there is not much.

60 could be an option in the menu that turns things off. But which one we aim
at changes what we build, so it is worth deciding rather than drifting.

## One thing that might be free, and is worth checking first

Three separate files in the project say "the CI runner has no GPU, so any speed
we measure is meaningless". They were written on 26 July and 3 August. You moved
the builds onto your own PC on 22 August. Nobody has re-read those sentences
since.

If they are stale, then for three weeks this project has been measuring real
frame times on real target hardware and telling itself in three places that it
has not. The last run reported a 29 millisecond frame, which would be a
perfectly sensible number for your machine and a suspiciously good one for
software.

I could not settle it, because nothing in the report prints which graphics card
did the work. That is one line of code.

## What I would measure next, cheapest first

1. **Print the graphics card name in the run report.** One line. It tells us
   whether we already have three weeks of real measurements or none.
2. **Put a frame timer in the Unreal probe.** Three numbers: game, draw, GPU.
   Unreal gives them away for free; we just never wrote them down.
3. **Render one person walking on the Unreal street.** It has never happened.
   Until it does, every crowd number we have is about a simulation nobody can
   see.
4. **Then, and only then, set the two resident counts**, from a printed series
   rather than from a guess.

## What this is, and is not

It is an honest account of what the published figures cost and what we have
measured, which is a lot on the simulation side and literally nothing on the
Unreal rendering side.

It is not a budget. I could have invented one and it would have looked useful
for about a month. The thing that is actually blocking phase 1 is a missing
instrument, and instruments here are small and cheap.
