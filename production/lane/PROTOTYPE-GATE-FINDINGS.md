# The loop prototype's publish gate: first run (19 Nov 2026)

Lane, task 4o part b. The gate is in tools/lane/gate/ (README there). Run on the prototype as published
(page version 1795032844-05a0, rebuilt here byte for byte), a fresh new game for every scenario, 19 Nov
06:41 to 06:48. A fresh reviewer (Opus, high effort) checked the gate and both gates' results against the
game's source: production/lane/GATE-REVIEW-2026-11-19.md. Every failure below was confirmed by it as a
real fault in the game, not in the gate.

## What fails today (for the first round after his yes; nothing is fixed by the gate itself)

1. A crash is never told in words. The cab takes damage (each of up to 4 points takes 5% off its top speed),
   but the screen only shakes and a sound plays; words come later as a "Noted in the Ledger" line. 4 of 4
   damaging crashes, at 10 to 30 mph. (drive.js, the hit branch.)
2. Keyboard steering snaps: the turn goes from nothing to 90% of full in the first frame the key is down and back
   to nothing the frame it comes up. This is the prototype's version of his "jerky keyboard steering".
3. A person knocked down by the cab is not told on screen at the time, and no choice is offered: the only prompt
   is "Get out". His ruling of 18 Nov (stop and help, or drive off into a hit-and-run) is not built yet.
   The person was hurt (0.82 of 1) and not killed, at one speed tried.
4. A pad moves neither Tom nor the cab; by design it works only the Ledger. "Every input device usable" fails.
5. Indoors, the camera can hide Tom behind the room's near wall (Regent House, walking into the wall nearest
   the camera; seen in 3 of 4 runs that reached that room).

What passes: never stuck on foot (8 wall pushes, 10 corners, 36 indoor pushes in 9 rooms), never stuck in the
cab after any of 12 hits (it cannot strand: damage only slows it), out of the cab always onto open ground,
pause and resume, save and load, back to play after 300 random keys, no pause that nothing holds, no page
errors.

## Limits the review found, still open in the gate (its must-fix list, short)

- Done in this run: a new game per scenario; a rule never reached in a full run now fails; steering judged on
  release too; the gate does not pass without the hands-on write-up.
- Still to do: read the game's own message list from the hit frame instead of the words on screen (the
  "told" checks are provisional); aim at named props (poles, bollards, parked cars, traffic) and compare what is
  drawn with what is solid (the lamp posts are drawn but not solid in the loop prototype, so the cab drives
  through them and the gate never aims at one); a minimum ramp time and an A-to-D switch for steering.
- Neither gate measures real-time smoothness (frame pacing, camera jerk while driving).
- The driving gate (4o-a): its pass on keyboard steering looked only at the first move from straight, so it
  would miss his complaint; its pedestrian rule cannot fail; it repairs and moves the car itself before testing
  Backspace, so part of the "Backspace leaves it dead" result may be its own doing. Worth re-checking before the
  round 4 prompt relies on that line (production/lane/DRIVING-ROUND4-FINDINGS.md).

## For the main session

- Nothing to merge into the game; the gate is lane tooling. The hands-on part has a helper send key presses to a
  headless browser in the cloud; CLAUDE.md's "Helpers never send clicks or keys" comes from rulings about
  computer use on his PC (29 and 30 Oct), which this is not, but the line's owner may want to say so.
