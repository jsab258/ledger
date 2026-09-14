# D33: the player sees their own position, never other minds

STATUS: DECIDED 2026-09-14 by Jafar, dictated and recorded by the resident.

## The rule, as given

**D12 stands: what NPCs know is never displayed as ground truth.**

**Tom's own reading is shown, in two places.**

1. **In the moment**, when he would legitimately notice being watched.
2. **After the fact**, in the Ledger, itemised with its reasons, using the
   Why idiom that `Core/Homicide.cs` and `Core/YardDepth.cs` already carry.

## The case where neither party knows

**Stays exactly as `Core/Observation.cs` rules it: the player gets nothing,
no ghost, no warning.**

**This was the only gap present in all five games audited.**

## Verified at source, per rule 1

The Why idiom is real in both files named. `Core/Homicide.cs:351`,
`HomicideBook.PressureWhy`, pairs the `Pressure` value with a compact token
breaking down what fed it: witness count, best confidence, the redirect
relief, and the drop reasons. `Core/YardDepth.cs:330`, `ProbeWhy`, pairs an
absence (no depth read) with a tally of the named reason. Both exist to
debug the studio's own numbers today; this ruling is what turns the same
idiom outward, toward the player.

`Core/Observation.cs:46` defines `enum Awareness` in four states. Its
`NeitherKnows` value, lines 48 to 51, is commented in the source as exactly
what is dictated above: the player is given nothing there, no ghost, no
warning, and the first he hears of it is a rumour three days later. The
other three states, `YouKnow`, `TheyKnow` and `Standoff`, are where an
in-the-moment reading already has names to attach to; which of them this
ruling covers is left to the UI work below, not decided here.

## What this does not decide

Where in the Ledger's layout the itemised reading sits, its wording, or the
in-the-moment cue's presentation. UI work against the standard, per D12,
waiting for a frame like everything visual does.
