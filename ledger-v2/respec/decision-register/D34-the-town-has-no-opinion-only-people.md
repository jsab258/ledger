# D34: the town has no opinion, only people

STATUS: DECIDED 2026-09-14 by Jafar, dictated and recorded by the resident.

## The rule, as given

**D11 stands: no global or group reputation number is ever stored.**

**Research topic 30 found this is already built and working.**
`Gossip.DayCircleHeat` walks every person live, stores nothing, takes each
person's strongest rumour per topic, and `StreetWord` renders quiet,
murmuring, uneasy or hostile.

**Record it as ruled.**

## Verified at source, per rule 1

`Core/Gossip.cs:525` defines `DayCircleHeat()` on class `GossipMill` (the
file is `Gossip.cs`; the method sits on `GossipMill` inside it, which his
own shorthand is exact about for the file and the method and informal about
for the class). It runs fresh on every call over `_agents.Values` and writes
no field: nothing is stored. For each agent it builds `bestPerTopic`, the
strongest confidence per `TopicKey`, then combines topics by noisy-or into
one 0..1 reading. `StreetWord` is `Game/GameController.cs:285` to 286:
`heat < 0.2 ? "quiet" : heat < 0.45 ? "murmuring" : heat < 0.7 ? "uneasy" :
"hostile"`, called from `CurrentHeat`, which reads
`_gossip.Mill.DayCircleHeat()` directly. Both exist and both match his
description exactly.

## The tile this needs, named so it is not lost

No entry in `production/systems-inventory.json` (91 entries, machine-checked
by `tools/systems-inventory-check.py`) carries this evidence today. The two
nearest by name, "gossip propagation" and "suspicion and heat", cite
`Gossip.cs#HopDecay` and `Suspicion.cs#SuspicionTracker`, neither of which is
this function. A tile is owed, carrying `Core/Gossip.cs#GossipMill.DayCircleHeat`
and `Game/GameController.cs#StreetWord` as its evidence, typed exists.
Adding it to the file is implementation, and is not done by this record.

## A claim checked, so it is named rather than guessed

Three research topics reported that D24, D28 and D34 do not exist in this
checkout. Checked 2026-09-14: `D24-what-ledger-is-not.md` and
`D28-presentation-is-built-early.md` are both present in the register and
unchanged. D34 was the one genuinely missing, and this file is what closes
that gap. The claim was wrong on two of three, and it is recorded here
rather than silently corrected, the same way D12 already carries the record
of a prior claim that D10 did not exist, which was also false.

## Why it matters that this was already built

Three of the five research audits asked some version of "does the town have
an opinion, or only people" as an open question for him to answer. The
answer was already sitting in the code, unread by the inventory that exists
to track it.
