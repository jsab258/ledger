# Measuring in installed games: the method (23 Nov 2026, advisor 328)

## Built on

INSTALLED-METHOD-NOTES-2026-11-23.md (questions in INSTALLED-METHOD-QUESTIONS.md); FRAMETIME-METHOD-2026-11-17.md (PresentMon, benchmark practice, section 6); GAME-TERMS-AND-STUDY-LAW-2026-11-17.md (observing a program while running it); the footage method and sampling rule in STATUS.md (a step finer than the thing measured; five samples a number). Reviewed by a fresh reviewer, INSTALLED-METHOD-REVIEW-2026-11-23.md; its points are taken in below. Method researched: INSTALLED-METHOD-NOTES-2026-11-23.md. Reference: no studio drill sheet was reached; the drills are ours, from the footage method (none found).

## Before any run

- Permission (his ruling 23 Nov 16:06-16:10, advisors 331-332, RULINGS 17/23 Nov): scripted keys from outside the game are allowed for measuring, offline and single-player only; drills still wait until he has been away 10 minutes and stop at his first touch.
- The copy: the games installed on his PC are used as they are (Sleeping Dogs, GTA V, GTA IV, KCD2; RDR2 once installed). We never change, add or remove game files, bypass protection or anti-cheat, or go online (never GTA Online). How his copies are installed is not written about. The installed list is read at the start of each day and new games folded into the measuring.
- Tools: PresentMon (allowlist item 12). A screen recorder: ffmpeg is not on the allowlist; its licence is recorded on the allowlist with a named build source before it is fetched (licences are the session's to decide, RULINGS 19 Nov), else Windows' own capture is used.

## What is measured where

| In the installed game (drills) | From uncut footage of real players |
|---|---|
| Walk and run speed over a known distance | Chases through traffic, fights against several |
| Car: standstill to top speed; braking and turning from the top speed reached (a set speed needs a speedometer; where the game shows none, top speed is the only repeatable one) | How players spend their time; the first hours |
| One punch: wind-up, hit, recovery, from the input's logged time | Police and crowd reactions; wanted escapes (police and traffic vary, so a blind script cannot repeat them) |
| Frame times at fixed views (PresentMon, separate runs without recording) | Anything needing skilled real-time play |

## A drill

1. Load the same save before every run (the game's own; never a downloaded save); one warm-up run discarded.
2. The script sends keys by scan code (SendInput with the scan-code flag), logs the performance counter just before and after each send (the log is the truth, not the schedule), busy-waits for short holds (the system tick is 15.6 ms), checks the game window is in front before each key, releases every key at the end, on any error and when he touches the mouse or keyboard, and stops if any other window takes the front (a Windows Security box would take the keys).
3. The recorder starts first and its start is logged on the same counter, so every frame time maps to the input log; recording at 60 fps or more with duplicated frames off.
4. Numbers read by code from the frames: the game's response delay is measured from the logged input to the first changed frame, not assumed zero; distance from lengths measured in that game first (a car length from its own model in view, lane marks counted over a stretch driven at a steady speed); HUD by fixed-slot templates made for that game's HUD (tools/star_slots.py's method; its templates fit GTA's HUD only); two sheets per drill checked by eye.
5. Five runs a number; median and range; more runs when the range exceeds a fifth of the median (FRAMETIME section 6's practice of adding passes on spread).

## When it runs

Only after he has been away from the PC 10 minutes, with no build, walk or Kiln gate running; never during the night's build and walk. Each run logged in the hourly row.

## Openings

Who plays them: a script plays blind, and reading frames to choose keys is computer use. So an opening is attempted only by fixed key scripts where it is linear; any part needing reactions stops after two tries and goes in the row; the advisor may ask him to play it once (advisor 328). RDR2's opening cost reported before it starts. No opening length was found in the sources (UNVERIFIED for all four games).

## Gaps (unverified or unreached)

- How studios or reviewers measure movement and vehicle feel from outside: no source reached (Swink, GDC, Digital Foundry).
- Whether these games accept scan-code input, and whether desktop duplication captures exclusive fullscreen: first-run tests (borderless window if not).
- How the recorder's frame times map to the performance counter: not read; the start-logging step above is our own.
- Known lengths in each game: measured in that game, not taken from any source.
- Built-in benchmarks: GTA V's from a secondary guide; GTA IV's and Sleeping Dogs' from search results only.
