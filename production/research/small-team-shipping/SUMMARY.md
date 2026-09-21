# Seven people who did something like this, and what it cost them

Research topic 18. I looked at seven games made by one or two people that were
genuinely ambitious, and asked how they actually did it rather than whether it
can be done.

## The short version

| game | people | years |
|---|---|---|
| Return of the Obra Dinn | 1 | 4.5 |
| Stardew Valley | 1 | 4.5 |
| Manor Lords | 1 | about 7 |
| Animal Well | 1 | 7 |
| Shadows of Doubt | about 3 | about 8 |
| Kenshi | 1, then a few | 12 |
| Dwarf Fortress | 2 | 20 |

Median: about seven years. Every one of them was full time or harder for most
of that. Stardew Valley's author worked 70-hour weeks for years, nearly
cancelled it, and nearly lost the whole thing to a hard drive with no backup.

## The finding that matters most

**Not one of them bought both depth and looks.**

The three with simulation anywhere near what we are building gave the visuals
away completely. Dwarf Fortress is the deepest simulation in games and it was
ASCII text for twenty years. Kenshi looked dated on the day it shipped. Shadows
of Doubt, which is the closest thing that exists to LEDGER, is voxels.

And the two that look good, Manor Lords and Obra Dinn, have nothing like our
moat. Nobody in them remembers you.

There is no case in the middle. What you have decided to build is the first one.

## The sentence I would put on the wall

Shadows of Doubt's developer wrote a devblog in March 2020 called "How Voxels
Saved the Project". In it:

> realism was off the table due to workload

and the voxel decision was, in his words, the biggest single factor in making an
ambitious simulation doable with a small team and a small budget, because the
turnaround on art assets is tiny compared to anything else.

He also says a more realistic low-poly look would have suited the game's
atmosphere better. He picked the look he thought was worse, to protect the
simulation.

That is the exact trade we have decided not to make. It is survivable only if AI
generation really does collapse the cost of making art, which is the thing his
devblog identifies as the constraint that breaks small teams.

## The uncomfortable one

Animal Well was made on nights and weekends alongside a day job, which is the
only case in the seven that matches how you work. It ran that way for about
three and a half years, and then the author went full time to finish it.

I could not find a single ambitious game that shipped entirely on part-time
hours. That is not proof it cannot happen. It is the shape of every record I
could find.

## Why I do not think that settles anything

All seven of those projects were priced in one person's hours. You are not
spending those. You spend decision hours, and the studio spends sessions.

That means none of the seven can tell us whether this works. What they tell us
with real confidence is what happens if the method does not work: seven years,
full time, or the trade Shadows of Doubt made.

**The only instrument that can settle it is already built and it is ours.**
`production/throughput.md` counts verified pieces a week. It is honest to the
point of being uncomfortable: it recorded a completed brand bible as ZERO
because nothing read it, and it says outright that the cost per piece is
undefined rather than pretending it is zero.

What it has measured is that once a pipeline exists, importing another piece
costs no sessions and about twenty seconds of machine time. What it says it has
NOT measured, in its own words, is what it costs to MAKE a piece worth
importing.

**That one number is the whole question.** If making a piece is nearly free, we
break the seven-year pattern. If it is not, we are a small team with a fast
build server, and the pattern applies to us.

## The question for you

You retired the deadline on 2 September and I think that was right: deadlines on
a hobby project you love mostly produce guilt.

But the reason everyone recommends deadlines is not the date. It is that a
deadline forces you to CUT. We have three things that bound work and none of
them cuts: the weekly budget bounds how fast we go, the attempt budget bounds
how many tries one item gets, and phase gates say when a phase is done. Nothing
bounds how many things are on the list.

And the list moves. On 9 September the systems census had 69 entries with 7 of
them unbuilt. On 10 September your ruling added 22 more, 18 of them unbuilt.
Overnight the known-unbuilt column went from 7 to 25.

To be clear, I think that was the right call and the opposite of a mistake:
those systems existed whether or not anyone wrote them down, and writing them
down is what lets you argue about them. The dangerous requirement is the
uncounted one.

**So the question is not whether to count things. It is whether you want a
ceiling on the count.** Something like: this phase ships with N systems and
nothing else gets in without one coming out. You already have half of this rule
in force, the one where a gap in another game is not a gap in LEDGER until you
say it is. The other half would be a number.

That is your call and there is no right answer. I raise it because it is the one
defence against the failure mode that killed most of the projects in this
research, and we do not currently have it.

## What I would do next, cheap

1. **Measure what it costs to make one piece**, not import one. The throughput
   ledger names the twelve-package batch as the thing that would measure it. It
   is the most valuable unknown in the project.
2. **Keep the throughput ledger brutal.** Its habit of recording zeros is worth
   more than any research I can do.
3. **Read the two devblogs I could not reach.** Shadows of Doubt's DevBlog 21
   and the Unreal interview with the Manor Lords developer are both blocked from
   where I work and both are written by people who solved our exact problem.
