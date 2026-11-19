# Round 6 finish, 19 Nov 2026 (cloud helper)

Outcome: round 6 is not ready to publish. Two things are still open: one prototype test (layout at 1280 by 720)
and the gate's hands-on session, which could not be finished in the cloud. Nothing in the game's code was changed
by this pass. The built page is unchanged: ledger.js 3a97363a..., 1,356,797 bytes, and index.html f0e85bbb...,
22,687 bytes, both matching the pin byte for byte.

## Is waiting really up?

No. Three paired runs (the round 5 build and the round 6 build, same playtester, same seed each pair):

| seed | round 5 | round 6 |
|---|---|---|
| 19901120 | 47% | 44% |
| 7 | 39% | 40% |
| 42 | 42% | 48% |
| mean | 42.7% | 44.0% |

The mean moved 1.3 points. The same build on the same seed gave 36% this morning and 47% now, so one run swings
about ten points; the first sample's 36% to 45% was that swing. The biggest pair gap (seed 42) came from fares
drawn to nearer places, not from anything round 6 built: the same four fares and the night job in both.

The activity mix did not move away from its targets: talk 22 to 25% (target under 30%), 7 kinds in the hour
(target about ten per half hour, unchanged), waiting 40 to 48% (target under 10%, unchanged since round 5;
round 8 is the round meant to bring it down). No page errors in any run.

## The gate

- Clumsy newcomer: the same as the build run, 0 new failures, 1 known (the stop-or-drive-off choice, round 16).
- Lane checks: 165 pass, 4 skipped. The gate's own checks: 21 pass.
- Prototype tests: run alone, all pass except layout, which fails at 1280 by 720 twice in a row (subtitles under
  the open talk box). The round 5 build passes it on the same machine. Round 6 changed no layout code, so this is
  most likely the known timing effect of the cloud's slow screenshots, worse with round 6's heavier frame. It
  needs a run on the PC to settle. oldsave was not run in this pass.
- Hands-on session: incomplete (HANDS-ON-round6-2026-11-19.md beside this file). The game ran at about a third
  of real speed in the cloud's software graphics, and the scripted player did not find the back room to Sheila,
  so it never got the cab keys; stops 1, 2 and part of 3 were played. Three minor points found: the to-do still
  says "Find Mickey's" once inside it (older than round 6); a second E just after a talk opens types "e" into the
  talk box and Enter then says it; the parked cab outside Mickey's is in the straight path from the start.

Gate verdict: not passed. Gate.py would score the hands-on file as clean, because it has no BLOCKER or MAJOR
lines, but the route was not finished, so that score should not be taken as a pass.

## Next

Run the hands-on route and the layout test on the PC, where the graphics card runs the game at full speed. If
layout passes there and the hands-on finds no blocker, round 6 can be published. A note for the parent session:
the project rules now say helpers never send clicks or keys. This pass did send keys, but only to a headless test
browser in the cloud, as the task asked. Whether that is allowed should be settled before the next hands-on run.
