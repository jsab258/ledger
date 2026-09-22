# 260: an oversized message fails every sweep for ever, and nothing retires it

STATUS: READY
OPENED: 2026-09-11

## The fault, measured

`production/outbox/2026-09-10-the-archive-landed.answer.md` is 5346 characters.
Telegram caps a text message at 4096. The sweep on 2026-09-11 08:00Z said so
plainly and then did the wrong thing with it:

    outbox: NOT SENT ... (Telegram said no (HTTP 400: Bad Request: message is
    too long)). It stays unsent and the next pass tries again.
    outbox done: outboxFiles=18 sent=0 unsent=1 alreadySent=17 sendFailed=1

THE RETRY IS THE BUG. A message rejected for LENGTH will be rejected for length
on every future pass, for ever, because nothing about it changes between
attempts. So `sweepExitCode=1` on every run of a channel that is otherwise
working, and a permanent red hides the next real failure behind it.

It also predates the move: the file came in at `0db066b2`, written before the
repository changed, so this has been failing quietly on the old home too.

## What separates this from a retryable failure

A network timeout, a rate limit and a bot restart are all worth retrying. A 400
naming a property of the message itself is not: the input is wrong, not the
moment. THE SENDER CANNOT CURRENTLY TELL THOSE APART and that distinction is
the whole of this item.

## Done looks like

1. The sender classifies a Telegram 400 that names the message as PERMANENT and
   stops retrying it, recording a refusal beside the file the way a register
   refusal is recorded, so the file is visibly parked rather than silently
   looping.
2. A permanently refused message does not hold `sweepExitCode` red. The run
   reports it in its own key with a denominator, something like
   `sendRefusedPermanent=1/18`, and exits on whether the RETRYABLE work
   succeeded.
3. Tested both ways, accepting case first: an ordinary message still sends, and
   a planted oversized one is refused once and not retried on the next pass.
4. The existing 5346-character message is either split or shortened by the
   Producer, or retired with its reason written down. NOT by this item's
   builder: the words are the Producer's and the content decision is not a
   plumbing change.

## What this must not become

Do not add a length check that silently truncates. A message he receives with
the end missing is worse than one he never receives, because nothing tells him
it was cut.
