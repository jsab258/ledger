# Camera in walls, night walk of 8 Nov 2026: diagnosis

Build fa46ab0 (wip d092848), runs 2026-11-08-0151 and -0159. Read-only. Written 8 Nov 2026, 02:45. Log times UTC; picture files local (UTC+1).

## The measure

The pictures are the game's own view; the fault is real. But through the Z waits (D0 23:43 to D2 08:48) Tom stayed at (7.65, 6.99); every save line in that span gives the same place. "Wait a while" in the pictures is only the on-screen hint. The listed steps fall in the later town stages, while the tester walks him.

## 1. Where Tom and the camera are

The tester's path (F:/LedgerTools/nightly/2026-11-08/route/verdict.json) and the save lines agree: from D2 12:06 to past D3 07:13, Tom moves back and forth between (8.92, 5.42) and (9.30, 5.58), the office's front-east corner. The tester first aimed him at (8.57, 5.14), its stand-off point for Ron, who was outside. That point lies on the window board's box (x 5.14-8.62, z 5.12-5.62). Later it aimed him at the door. Every leg failed.

The drawn room's east wall stands at x 8.65-8.77 (LedgerProbe.log line 1040: "wall_left stands 865..877"). Tom's centre was therefore 15-53 cm past it, in the gap before the next building. The camera's place was not logged (-OfficeCamLog off); the pictures put it in the same gap or at the shop front.

## 2. Why

The camera arm's own settings are not the cause:

- The engine defaults stand: collision test on, Camera channel, 12 cm probe (UE 5.8.2 SpringArmComponent.cpp:27, 34-35). SliceCharacter.cpp:92-96 builds the arm and nothing changes those settings.
- Standing restores the capsule (SliceCharacter.cpp:2686) and logged "touched the room 0 times", minutes before the bad frames.

The cause is what the sweep can meet:

- **The drawn room has no collision.** Since 28 Oct (commit 1b7cb81) its meshes carry none (VignetteShot.cpp:7784-7799). The log shows "collision 0" for floor, walls and fittings, the blind included (lines 1038-1043). The office's walls "for the body and the camera's arm" are meant to be the spec's hidden boxes (CrimeProbe.cpp:4626-4650).
- **The spec has no east wall.** None of the 37 boxes in production/specs/mickeys-office.json is one. Between the shop front and the staff wall (z 5.12-9.40) that side has only the bench, the notices (1.2-1.9 m up) and the counter. The boxes there sit on x 9.00, 23-35 cm east of the drawn wall.

So Tom walks into the gap, and the camera following him passes through the wall.

Two things make it worse:

- Window glass ignores the camera channel by design (VignetteShot.cpp:2133-2137), so near the front the camera reaches the frame and pavement side.
- Past x 9.00, OfficeCameraTick counts Tom as outside (CrimeProbe.cpp:5371). It eases the arm out to the street's 3.10 m (lines 5431-5439), which carries the camera further from the room.

Confidence: high.

## 3. Black frames

The code has no fade (grep finds no StartCameraFade or SetManualCameraFade).

Nor is the room's exposure: by day the street fixes exposure at 4.0 (VignetteShot.cpp:10593-10598) and the office adds none (log line 1928), yet the room by day reads normally (0151 step-067, mean brightness 81 of 255).

The black frames are 0151 steps 068-070 (mean 1-2, about five seconds). Tom was walking from the counter at (7.51, 6.66) to the door, with the camera behind him to the east. A 2 m arm with its 0.45 m side offset reaches about x 9.5, past the drawn wall. Run 0159 has equally dark stretches (steps 060, 075-085, 113-130) while Tom stood in the gap.

Most likely cause: the camera sits in the unlit space behind the drawn wall. Confidence: medium; unverified, because the camera's place was not logged.

## 4. New or older

The fault dates from 28 Oct, when the rooms lost their collision. It reached the night walk on 8 Nov through two changes on 7 Nov: the office went on by default (cdb1ded04, CrimeProbe.cpp:4542-4544), and the tester now goes inside to sit and to greet Sheila. The 7 Nov review's "the camera can cut him off" (FINDINGS.md) may be the same cause; unverified.

## 5. Smallest mend

**The change (data only).** Add one hidden wall box to production/specs/mickeys-office.json, on the drawn east wall: about x 8.65-9.15, 0.1-3.0 m up, z 5.12-9.40. Measure its line against wall_left before setting it. It blocks Tom and the camera alike.

**Checks before committing:**

- PerceptionGolden and the regression, since the box also blocks sight traces.
- An editor walk to (8.9, 5.4) with -OfficeCamLog (CrimeProbe.cpp:5440-5458). It should log "meets east wall" where it now logs "clear".

**A separate tester fault.** In tools/route_walk.py, approach (lines 140-142) with OFFICE_BOX (line 71) sends Tom onto the window board to talk to someone outside: its z 5.12 edge counts that point as indoors, so the route never uses the door.

**How a packaged run would show it fixed.** In the next night walk's continued run:

- No save line inside the office east of x 8.31 (the wall less Tom's 0.34 m radius).
- No frame darker than mean 5 except the title.
- town-Ron reached.
- The office steps judged by eye against 0159 steps 147-249.

## Not checked

- The camera's exact place in any frame.
- What stops Tom at x 9.30.
- Whether the back room (z 9.55-13.0) or the front above the window board has the same gap.
