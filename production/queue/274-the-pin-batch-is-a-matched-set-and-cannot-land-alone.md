# 274: the exposure pin batch is a matched set, and a C++ invariant refuses it

STATUS: RULED 2026-09-14, position B, under
game-design/decision-2026-09-14-ruling-the-pin-belongs-to-the-rig-and-the-render-waits-for-it.md.
Lands as one commit per its section 8; closes when the first Unreal run on or
after it prints section 9's keys.
OPENED: 2026-09-14, established by reverting one file at a time.

## What was learned, by experiment rather than by reading the diff

The exposure builder's work is four files, and three of them are ONE CHANGE
wearing three names. Each state below was measured by reverting and re-running
`dotnet run -c Release --project ledger/CoreTests -- --selftest`:

    all three present, flagless regeneration   RED  regenerating-changes-nothing
    pieces at HEAD, scene+Program present      RED  regenerating-changes-nothing
    scene at HEAD, Program present             RED  every-sun-on-condition-carries-a-pin
    scene and Program at HEAD                  GREEN 0 FAILED
    all three present, --ahead-of-run cb4767e  GREEN 4355/4355, aheadKey preserved

THE LAST ROW IS THE ANSWER AND IT WAS ORDERED BY A DIRECTOR, not found by me.
I had concluded from the first four rows that the batch was blocked. It was
not: I had never run the generator with the flag the failing check printed.

## A SECOND WRONG CONCLUSION, MINE, CAUGHT BY THE GATE

I wrote above that the last row is the answer and the batch lands. IT DOES NOT.
`--ahead-of-run cb4767e` genuinely fixes the piece-list half, and CoreTests
genuinely reads 4355 of 4355. I then reported the batch as landing on the
strength of the C# suite ALONE, and the UE probe tests are a SEPARATE SUITE
that also gates. Measured after the claim:

    ue-probe/tests/vignette-spec-test   391/393   two failures
    ue-probe/tests/frame-stats-test     113/113   clean

The two failures, both caused by the builder's scene and neither by the flag:

    FAILED  nullSeriesSamples=9/of=37, where the test names SEVEN shots
    FAILED  "the only rows asking for a pin are the ladder rungs"

THE SECOND IS THE REAL ONE AND IT IS A DESIGN DISAGREEMENT, not a bug. An
existing invariant says only the ladder rungs may ask for a pin, with its
reason attached: "a row pinned by accident would be photographed at an exposure
nobody chose". The builder's scene pins 25 of 27 sun-on conditions. Both
positions are defensible and the code cannot hold both.

The first failure is downstream of the same change: pinning 25 conditions
changes which frames share an identical applied-input group, so the null series
grew from 7 samples to 9 and a test that names seven shots in shot order no
longer matches.

REVERTING TO THE RULED STATE RESTORES 393/393 and 113/113, measured.

## What this means for the director's ruling

The ruling "the leak lands alone" was RIGHT, and it was right for a reason
better than the one it gave. It reasoned from the risk of a half-fix looking
whole; the actual reason is that the other half does not pass. I reported the
batch as unblocked between the ruling and this measurement, and that report
was wrong.

## The decision that is now owed

Which conditions may ask for a pin: the ladder rungs only, as the invariant
says, or every sun-on condition, as the scene now says? That is a Core and
spec question, so it is a director's call and not a builder's, and 274 stays
blocked until it is made. Whichever way it goes, the two tests above move with
it and the null-series shot count is re-derived rather than re-typed.

## The atomicity claim STANDS

`ledger/CoreTests/Program.cs` replaces a frozen literal (`pinned == 4 &&
unpinned == 23`, HEAD line 19631) with an INVARIANT: every sun-on condition
carries a pin, every sun-off condition carries none, day conditions that are
not rungs share one value. That invariant is better than the literal and is not
satisfiable by HEAD's scene, which pins 4 of 27. So scene, Program.cs and
pieces are genuinely one change. What was wrong was the conclusion that the one
change could not be made, not the observation that it is one change.

0.300 is a MEASURED RUNG (verdict line 321), not an interpolation.

## The separable half, which landed first and should have

The C++ leak fix is independent and green on its own: VignetteShot.cpp,
VignetteSpec.h, FrameStats.h and their two test files, 393/393 (was 383) and
113/113 (was 108). It fixes the actual fault: the camera actor is spawned once
and moved, the two AutoExposure override flags were written only when a
condition asked for a pin, and so they LEAKED from the previous shot.

## What this item is kept for

The method, not the conclusion. Reverting one file at a time and reading each
result is how the atomicity was established, and it was right. Reading only the
states I could reach without the flag is how the wrong conclusion was drawn,
and the flag was printed in the failure I was reading at the time.
