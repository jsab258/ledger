# 272: the stop rule needs the meter that is exhausted

STATUS: READY
OPENED: 2026-09-13, from a deadlock hit live at 04:16Z.

## IT HAPPENED THREE TIMES, 2026-09-13, and the dates are the argument

This item was filed at 04:20Z off one refusal. By 13:25Z there were three, the
same HTTP 429 and the same wording each time, and not one notice carried a
reset instant:

    04:16Z   first attempt, on the daily wake
    07:19Z   +3h03m
    13:21Z   +6h02m,  9h05m across the series

THE 2026-09-13 BRIEF WAS NEVER WRITTEN. Jafar's one message a day did not go
out, on a day when the first thing it owed him was that his own bot has a
budget question open on his phone and would answer it wrong in the direction
that stops work. That is what the deadlock below costs when it fires, and it
is no longer a thing that might happen.

## The fault, hit rather than predicted

`production/budget.md`'s first stop condition reads, verbatim:

    1. EITHER METER at or above 85 percent: STOP. Write the brief, push,
       and do nothing further until Jafar gives a new number.

At 2026-09-13T04:16Z the Producer turn died mid-read on an API refusal, quoted
in full because its wording is the evidence:

    You've reached your Fable limit. Switch to another model, or manage usage
    credits ... (error type rate_limit, HTTP 429, model sent to the API:
    claude-fable-5-1)

So the Fable meter is at its hard limit, which is at or above 85 by
definition, and rule 1 fires. Rule 1's required action is WRITE THE BRIEF. The
brief may be written by the Producer and by nothing else, ruled 2026-09-03:
"Reporting to Jafar is THE PRODUCER'S ALONE." And of the fifteen agent
definitions, exactly two are Fable, measured: `producer.md` and
`studio-director.md`.

    the stop rule's required action  write the brief
    who may perform it               the Producer, alone
    the Producer's model             fable
    the exhausted meter              fable

THE RULE REQUIRES THE EXHAUSTED METER TO PERFORM THE STOP. It is not a
shortage; it is a circular dependency, and it bites exactly when it matters,
because the ONLY time rule 1 fires is when that meter is spent.

The second half is the same shape. A director review is the gate on any batch
over the cadence threshold, and `studio-director.md` is the other Fable
definition. So at the ceiling the studio can still BUILD (tier 3 is Opus) and
cannot REVIEW, which means it can produce work it is forbidden to land.

## What this is not

Not a reason to switch the Producer to another model on the spot. The
four-tier routing table was ruled 2026-09-10 and is enforced rather than
advisory, and a resident substituting a model for a ruled role at the moment
the rule bites is how a ruled table becomes a suggestion. That judgment is
Jafar's or a director's, and the director is the other thing that is
unavailable, which is itself part of the finding.

## Done looks like

1. `production/budget.md`'s rule 1 says what happens when the meter that is
   spent is the one the required action needs. Whatever the answer is, it is
   WRITTEN rather than improvised at the moment it fires.
2. The options are laid out with their costs rather than one being assumed:
   a standing exception permitting a named lower tier to write a stop brief;
   or a short pre-written stop message that needs no model time; or the
   explicit ruling that no brief goes out at the ceiling and the silence is
   itself the signal, which is the honest option and must be named as one.
3. Whatever is ruled, `tools/producer-check.py` and the daily wake prompt
   agree with it, so the register does not refuse the very message the stop
   rule demands.
4. THE DIRECTOR HALF IS PART OF THIS ITEM, not a follow-up: at the ceiling,
   say whether a batch already built may land without review, or waits. Today
   it waits, which is correct and unwritten.

## What this does not cover

Whether the Fable limit and the Fable percentage Jafar reads are the same
number. They behave alike here and nothing in the container can read his usage
page, so this item treats the 429 as evidence the meter is spent and does not
claim to know the arithmetic behind it.
