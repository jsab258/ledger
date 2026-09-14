# The four structural defences

> **STATUS: LIVE**, written 2026-09-14, verified 2026-09-14 against the code it
> cites: IntentRouter.cs (IntentKind, VerbArg.Options, Adjudicator.Binds and the
> lexical fallback) and MemoryStore.cs (no prune, removed from both engines the
> same day) were each opened and read, not recalled. This is the
> answer to the strongest criticism this project will face, and the research
> found it had never been written down as the argument it is. It is an
> argument, not a plan: nothing here is work, and it changes when the
> architecture changes rather than on a schedule.

## The criticism

Every AI NPC demo of the last few years has been hollow in the same way, and a
reasonable person who has seen three of them will assume this is a fourth. The
hollowness is not a quality problem that a better model fixes. It is
structural: the model is the game. It decides what happened, it remembers by
re-reading its own transcript, and its output is prose that the world then has
to pretend was an action. Nothing is at stake because nothing is written down,
and the fiction dissolves the moment two characters are asked the same question.

LEDGER's claim is that it is not built that way. Four properties say why, and
each is checkable in the code rather than promised.

## 1. Outputs are classifications and closed-set choices, executed by
deterministic code

The model does not emit an action. It emits a label from a fixed set, and code
that was written by hand decides what that label does.

`Core/IntentRouter.cs` carries this literally. `IntentKind` is three values,
Narrative, Mechanical, Novel. A verb's arguments are `VerbArg.Options`, and its
own comment states the rule the whole defence rests on:

    Options is a CLOSED set, a value outside it invalidates the whole
    routing, it is never coerced into the nearest match.

That last clause is the defence. The usual failure is silent coercion: the
model says something almost valid, the system snaps it to the nearest legal
value, and the player is now playing a game whose rules bend toward whatever
the model felt like saying. Here an invalid value fails the routing outright.

## 2. Beliefs are rows in a memory store, not chat history

What a person knows is a record, written when they perceived it, readable by
anything, and outliving the conversation that produced it. It is not a
transcript the model re-reads.

`Core/MemoryStore.cs` holds these rows. As of 2026-09-14 NOTHING IS EVER
REMOVED FROM IT: the prune that had been dropping older events was found to be
deleting over half of a seven-agent soak street and was removed from both
engines, because permanent per-NPC memory is pillar 1. A test that asserted the
prune was asserting a canon violation and now asserts the opposite.

This is what makes the world consistent between two characters. They are not
each recalling a conversation; they are each reading their own rows about the
same event. Two people can disagree, and the disagreement is a fact about what
each of them saw, not an artifact of two model calls diverging.

## 3. The model never decides an outcome

Adjudication is code. `IntentRouter.cs` names the guard: `Adjudicator.Binds`
"will not let an effect that writes to the simulation travel on a requirement
nobody could fail". An effect that changes the world must be earned against a
condition that could have gone the other way.

So the model can be wrong, and being wrong costs a misread intent rather than a
corrupted world. Nothing it says writes to the simulation directly.

## 4. A character can only say what the simulation licenses

A person cannot mention what they do not have a row for. The speech path is fed
by what the simulation knows that character knows, so the ordinary chatbot
failure, confidently inventing a fact about the world, has no surface to happen
on. The character is not constrained by a filter after the fact; it is
constrained by having nothing else available.

## The fifth property, observed rather than dictated, for Jafar's judgement

The three-value classifier degrades rather than dies. `IntentRouter.cs` again:

    the lexical fast path resolves unambiguous phrasings for free and
    instantly, and is the complete fallback when there is no model
    available at all.

So the game is playable with NO MODEL PRESENT. That is a stronger statement
than any of the four above, because it proves the model is not load-bearing:
it is an improvement to a system that already works. This was not in the
dictation and is recorded here as an addition to rule on, not as settled.

## What this argument does not claim

It does not claim the conversations are good. It does not claim the model is
accurate. It claims that when the model is wrong the world stays consistent,
and that what the town remembers does not depend on what any model said. Those
are the properties the hollow demos lack, and they are the ones the moat is
built from.

It also does not claim these four are measured. Each names code that exists;
none names a verdict key that proves the property holds under load. That gap is
honest and is the natural next rung: an argument grounded in code is stronger
than one grounded in intent, and weaker than one grounded in a number.
