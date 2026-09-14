# 273: the ahead-of-run key can never be spent, because its anchor can never advance

STATUS: READY
OPENED: 2026-09-14. RETITLED AND REWRITTEN the same day after a director
refuted the first version. The original title claimed the generator drops a
declaration the test requires and called the guard pair a ratchet. THAT CLAIM
IS WITHDRAWN and the withdrawal is kept here rather than deleted, because the
mistake is the useful part.

## WHAT I GOT WRONG, and how

`ledger/CoreTests/Program.cs` accepts `--ahead-of-run <sha>` (lines 39 to 58,
implemented 20697 to 20770). The failing check PRINTED THAT EXACT REMEDY at
lines 21115 to 21117. I measured only the flagless command, watched the key
vanish, and concluded the generator was broken.

So it is an INVOCATION, not a ratchet. The flagless command spends the key BY
DESIGN; the flagged one carries it. The drift check even feeds the committed
key back before comparing (20875 to 20887), which is the thing I asserted could
not happen.

THE RULE I BROKE IS THE ONE THIS PROJECT WRITES DOWN MOST OFTEN: when something
is silent or refuses, RUN THE EXISTING ENTRY POINT AND READ ITS OUTPUT BEFORE
PROPOSING A MECHANISM. The output was not silent. It named the flag, and I
proposed a mechanism instead of reading three lines further down my own
terminal.

## WHAT SURVIVES, and it is real

The key's anchor is the newest LANDED UNITY RUN. D16 decided on 2026-09-10 that
the engine is Unreal. No Unity run will ever land again. So:

    the key is spent when a newer Unity run agrees with the file
    no newer Unity run can ever exist
    therefore the key can never be spent

`remove_with` names a command whose precondition is now unreachable, and the
declaration it guards is permanent rather than temporary. A temporary licence
that cannot expire is a different object from the one that was designed, and
the file should say so rather than leaving the next reader to derive D16's
consequence for themselves.

## What done looks like

The `ahead_of_unity_run` block states that its anchor is frozen by D16, so a
reader knows the declaration is permanent and not an outstanding debt. Either
rename the key to say what it now is, or keep the name and add the D16 clause
beside `remove_with`. Whichever is chosen, the cross-engine check keeps
working: that check is sound and has already caught one real case, and nothing
here is a reason to weaken it.

Print the decision rather than leaving it implicit: the generator says which
branch it took and which run it compared against.
