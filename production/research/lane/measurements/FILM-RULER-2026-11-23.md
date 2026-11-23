# The tester's film as a ruler (23 Nov 2026, 20:08 to 20:20 Swiss)

Built on: INSTALLED-METHOD.md, FRAMETIME-METHOD-2026-11-17.md and advisor 333.

Method researched: INSTALLED-METHOD.md and its review (INSTALLED-METHOD-REVIEW-2026-11-23.md: one clock for input and film; a step finer than the thing measured; the 30 fps default of a recorder too coarse for a punch). Built on advisor 333 (a frame-timed grabber of our own, no downloaded program) and the advisor's efficiency review of 23 Nov 19:44 (no page item holds the critical path when a fallback exists).

## What was run
Our packaged build (F: played-game, built 23 Nov 02:13), past the title, a 4 s walk and a 4 s run, filmed by tools/ai-tester/play.py, twice. He had been away 20 minutes.

| run | grabber | frames a second | grab window (stamp error is half) | step between grabs |
|---|---|---|---|---|
| 1 (20:08) | --film, the old 0.12 s pause and a JPEG save each frame | 5.3 | median 26 ms, max 118 | median 162 ms, p90 172 |
| 2 (20:12) | --film --fast (new: grab only, frames kept in memory, saved after the key is let go; key down and up stamped on the same clock) | 48.4 and 48.9 | median 19.7 ms, max 65 | median 20.1 ms, p90 21.2, max 42 |

## What the numbers mean
- Grabs are not new pictures. In the walk, 85 of 194 grabs repeat the one before (difference under 0.6 of 255, the floor of still frames): the game drew about 27 new pictures a second in its window while being filmed. A change of picture is placed to within one step (about 20 ms) plus half the grab window (about 10 ms).
- Input and film share one clock: the first grab came 0 ms after the key went down; the key's up and down are in times.jsonl.
- The run hold stood still against Ron ahead of Tom (frames 196 to 391 near identical), so the run's speed could not be read this time.
- The walk-speed check against the true 160 cm/s was NOT done: the game writes no player position anywhere the tester can read (CrimeProbe's route lines carry stages, not places). It needs a known distance on screen (flagstones, lamp posts) or a position line; not built.

## Decision
Good enough for the drills' slow rows (walk and run speeds, distances, time to top speed, braking, turn times, anything over about 0.1 s). Not good enough for quick actions (a punch's wind-up, a reaction under 0.1 s): those still want a 60 fps recorder, so the recorder item stays on his page for them alone. The drills start with --fast in each installed game, each only after he has been away 10 minutes (the tester's own keys count as use for 2 minutes).

Evidence: F:/LedgerTools/tmp/ai-tester/film/2026-11-23-2008 and 2026-11-23-2012 (times.jsonl and frames); the runs' reports under production/playtest/ai-tester/.
