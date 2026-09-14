# D38: the audit's findings become tiles

STATUS: DECIDED 2026-09-14 by Jafar, dictated and recorded by the resident.
Process level: it governs how `production/systems-inventory.json` is typed
from here on, the same map D21 already requires a ruling to re-type in its
own batch.

## The rule, as given

**Five systems that exist in code get tiles immediately, because the
inventory is currently a map of what the studio has CONSIDERED rather than
what it HAS.**

| system, in his words | his citation | verified |
|---|---|---|
| blood on the player, with noticing, ageing and washing | `Core/Traces.cs` | yes: class `Stain`, `Traces.Noticeable`, `Traces.Age`, `Traces.Wash` (`WashMinutes` = 25) |
| object provenance across five origins | `Core/Traces.cs`, reached from EvidenceHost | yes: `enum Origin` carries exactly five values, `Bought`, `Stolen`, `Taken`, `Inherited`, `Ordinary`; `Game/EvidenceHost.cs` calls `Traces.Acquire`, `Traces.Used`, `Traces.Dispose`, `Traces.ResidualRisk` |
| disguise | `Core/Gossip.cs:259` | yes: line 259 is the exact line, the `Witness` method's confidence discount for a disguise, distance or darkness |
| the four-rung concealment model | `Core/Arsenal.cs`, reached from `Core/Coat.cs` | yes: `enum Concealment` carries exactly four values, `Innocent`, `Concealable`, `Damning`, `Impossible`; `Core/Coat.cs` calls `Arsenal.Get`, `Arsenal.Fits`, `Arsenal.FriskCost` |
| the lit window as an information carrier | `Core/Occupancy.cs` | yes: the file's own comment names the lit window the information pillar rather than decoration |

All five citations verified 2026-09-14: file exists, symbol exists, and the
behaviour matches his description.

**Each typed on its own evidence and marked built-not-measured where no
verdict key emits it.**

None of the five appears in the 91-entry inventory today under any name
checked. `Traces.cs` and `Arsenal.cs` are cited nowhere in
`production/systems-inventory.json`. `Gossip.cs` and `Occupancy.cs` are each
cited once, but by a different function than the one named here: the
"gossip propagation" tile cites `Gossip.cs#HopDecay`, not line 259, and the
"daily routines" tile cites `Occupancy.cs#HomeFraction`, the outward-facing
half, not the lit window looking back at the player that D39 orders as new
work.

## The three further typing rules

**Every recommendation ruled now or next (D39) gets a tile typed absent.**

**Everything ruled out (D39) gets a tile typed ruled-out, naming the record
that struck it**, so the map shows what was decided against rather than
leaving it to look like an oversight.

**Everything ruled later (D39) goes in the queue with a number and no tile
until its stage arrives.**

## What the map's first screen must say

**How many tiles carry his judgement rather than a builder's.**

## What this does not do

Edit `production/systems-inventory.json`. The current schema
(`tools/systems-inventory-check.py`, `STATUSES = ("exists", "partial",
"absent")`) has no fourth value; `absent` already covers "typed absent"
above with no change needed, but whether "ruled-out" lands as a new status
value or as `absent` plus a note naming the record is implementation's call,
not settled here. Landing this ruling in the file is a schema question plus
twenty tile writes (this record's five, D39's eleven now-or-next items typed
absent, and D39's four ruled-out items), not a side effect of recording it.
