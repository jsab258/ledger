line: infrastructure (the measurement surface)
spec: external audit 2026-09-06, P1
acceptance: no document, gate, brief or public claim cites the soak as evidence for hundreds of residents; each citation either states the real denominator or is removed; and the soak's own output states plainly what it does and does not support, with the count of citations found and changed printed
max_sessions: 1
status: READY 2026-09-16, REOPENED BY JAFAR and folded into queue 351 (see the foot of this file). Was CLOSED 2026-09-10, not on the ladder, BY COMMIT cd55a79c (subject: D18 lands at five sites, 510 files are archived and nothing is deleted). No ruling named this closure; see production/queue/275. Reviewed 2026-09-14 against production/stages.md and UNDECIDED, the audit could not make this call for him; see production/queue/275.; filed as a finding rather than as ladder work1, ready 2026-09-06, after the P0 pair. Small, and mostly a grep and a sentence.

## The fault

The soak prints growth as REPORTED, NOT GATED, and it was RUN ON SEVEN AGENTS.
It is cited as evidence for a town of hundreds.

Seven to several hundred is not an extrapolation, it is a different question.
Memory growth, gossip fan-out and schedule contention do not scale linearly in
the ways that would make seven informative about three hundred, and the run
itself never claimed they did: it says NOT GATED, which is the instrument being
honest and the citations being careless.

## What it actually supports, and say it in those words

That the sim runs 500 days twice without falling over at SEVEN agents. That is
worth having and it is not nothing. It supports no claim about population
scale, memory volume at scale, or performance at target resident count.

## The work

Find every citation by grep, not by memory: the roadmap rows, the pillars, any
agent-facing doc, any brief. Print the count found and the count changed. A
zero here ships its denominator like any other.

Then make the soak's own done line carry the sentence, so the next reader gets
it from the instrument rather than from a document that may not travel with it.

## Both halves

Accepting: the soak runs and prints what it supports, naming seven.
Rejecting: a planted document citing it for hundreds is caught by whatever
check this lands, or if no check is practical, the item says so plainly rather
than pretending a grep once is a guard.

REOPENED 2026-09-16 BY JAFAR, BY NAME, AND FOLDED INTO QUEUE 351. His words:
"queue 116 is the fourth casualty of cd55a79c, and it is the scale evidence
for pillar 1. Reopen it as part of 351 rather than leaving the decision to
whoever picks that up."

  THE RESIDENT HAD LEFT THAT DECISION OPEN and he closed it. Queue 351 as
  filed said "whoever takes this should read 116 first and decide whether it
  reopens or is superseded; that call is not made here". Deferring a call to
  an unnamed later reader is the same shape as the archiving commit that
  closed this item in the first place, and he ruled it rather than letting it
  sit.

  WHY IT IS NOT SUPERSEDED. 116 asks that no document cite the seven-agent
  soak as evidence for hundreds of residents. 351 asks for the MEASUREMENT
  that would make such a citation honest. Neither does the other's work: if
  351 runs and the town holds at 200, this item's citations still need
  correcting to say 200 and not 500; if 351 shows it falls over at 50, this
  item's citations need removing entirely. THE CITATION FIX IS DOWNSTREAM OF
  THE NUMBER AND CANNOT BE WRITTEN BEFORE IT.

  WHAT IS ALREADY DONE OF ITS ACCEPTANCE, so the reopening is not from zero:
  the soak's own comment now states the limit plainly, ledger/Soak/Program.cs
  line 57 reading "Seven agents is not a town (queue 116), so the projection
  names its denominators and the HEADROOM is printed as a multiple of the
  measured rate". That is the half of the acceptance about the soak's own
  output. The half about OTHER documents and claims citing it is unmeasured:
  nobody has run the grep and printed the count of citations found and
  changed, which this item's acceptance requires in those words.

  STATUS IS NOW READY, NOT CLOSED, and it rides with 351.

  AND IT IS THE FOURTH ITEM FOUND CLOSED BY cd55a79c with no ruling naming
  the closure, after queue 275's 182, queue 111 and queue 138. Three of the
  four recoveries came from Jafar noticing rather than from the studio: 138
  and now 116 by name, and 111 through an external audit he relayed. That
  ratio is the finding, and it belongs to queue 275 rather than here.

