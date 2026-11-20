# Review of 4t piece 5, the consequence checker (20 Nov 2026, 03:35 Swiss time)

Fresh reviewer: Opus at high effort, given the code, its tests and the game's source, not the lane's reasoning. It ran the checker on a 6-hour stretch.

Verdict: PASS WITH FIXES.

## Must, all fixed once
1. A rule with nothing to check was passed as "1 checked". Now each rule carries its real count; with none it is "not reached" (ok null), never a pass; the gate lists those in its note and never counts them as passed.
2. The game reuses one sighting event for two game hours, so a late listener was wrongly failed. Reused sighting events (the save's sightIdx) are now exempt from the hearing-time rule.
3. Talk, fares, scenes and a passer-by walking off move feelings without a memory by design, so "a reaction has a cause" gave false faults. It is now a warning list in the notes, passers-by left out.
4. The talk panel's whole text (hints, Tom's own suggested lines) counted as spoken lines. play.py now records, in the hidden row only, the other person's talk lines, the written scene's line, subtitles and bubbles within earshot; the log's "talk" lines (Tom's own) are no longer counted.

## Should
Fixed: a "was part of it" memory now fails when the event has a party list without that person; no start save means the reactions warning is skipped, not judged against nothing; the earliest log minute is noted and the speaker's name taken off "said it to his face" lines; a missing actions file fails as not reached instead of crashing; rows without the game minute are left out and counted (no mixing of real and game minutes); save errors are written beside the saves and named, with the save used; the gate keeps the checker's results even when the machine report is empty and no longer relabels their source; page errors other than the missing art now fail.
Not fixed, named: the reactions rule cannot be made strict until the game records the cause of each change of regard (a game change, only through a loop).

## After the fixes
Unit tests 6 of 6 (each rule catches its planted fault; a clean week passes; nothing to check is not a pass). A whole game day: 93 memories and 66 tellings traced, 0 faults; parties and sounds not reached in that stretch. A short real session through play.py checked from its hidden folder.
