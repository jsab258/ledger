# Office camera in the 9 Nov night walk: diagnosis

Build 03470931b, runs 0131 and 0138, 9 Nov 2026. Log times UTC. Not checked: Mafia's and KCD2's close-camera method.

## The measure

The night's reviewer saw 12 of 278 pictures, every 23rd, from both runs (tools/nightly_walk.py:218-223), and named steps without the run. Step-070 is from 0131 (D0 about 12:39). Steps 060 and 083 are from 0138 (D2 about 11:20 and 12:40).

## Did the fix ship?

Yes, unchanged: the spec is the same in 3b3454e and 03470931b. Both logs say "boxes=38" (37 before), and the game's own lines name the east wall box. The save lines put Tom at x 8.35, the 8 Nov test's stop. No picture is black, and the camera is never behind the wall.

## Steps 060 and 083: the tester's route

From D2 10:00, Ron stood on the pavement at (9.05, 4.15), just outside the window. The route aimed Tom 1.1 m from him, at (8.57, 5.14). That spot is inside the window board's box, 8 cm from the east wall. Its z of 5.14 is past the office's 5.12 edge, so the route counts it as indoors and never uses the door (route_walk.py:71, 136-142). Tom walked 14 legs into the corner (D2 10:41 to 12:58) and ended 1.9 m short.

The pictures show him at the blind and the wall, his shadow on the wall. The camera is clear and the blind whole. It is the same place and framing as 8 Nov step-084, which passed. The 8 Nov diagnosis named this route fault (section 5); it is still unfixed.

## Step-070: the fix working, close framing

Tom had overshot to about (8.04, 7.05), by the counter and the east wall. The tester turned the view toward the window, so he faces the camera. The arm reaches back into the corner. Its 0.45 m side offset (SliceCharacter.cpp:95) aims it at the new wall box. The engine's sweep stops at the first hit (UE 5.8.2 SpringArmComponent.cpp:130, 187, 197-201). From his place, that stop is about 0.6 m from the pivot. His head's size in the frame also gives about 0.6 m. His body hides only inside 55 cm (SliceCharacter.h:145, SliceCharacter.cpp:162-177), so his face fills the frame's bottom. Before the fix, this camera would have gone into the wall.

## Cause and confidence

- The fix shipped and holds. Confidence: high.
- Steps 060 and 083 are the known route fault; the reviewer called a framing that passed on 8 Nov "pressed into". Confidence: high (times, save lines and path agree).
- Step-070 is the arm stopping at the wall. Confidence: medium. The camera's place was not logged (-OfficeCamLog off).

## New or known

No new game fault. Step-070 is a known shortfall, close framing in a small room (FINDINGS line 25). Steps 060 and 083 are a tester fault. Neither uses the office camera's second try.

## Not settled

Tom's centre at z 5.57 lies within the board box's depth (to 5.62). On 8 Nov he stood at (8.35, 6.51), over the bench. The low boxes may not fully hold his body. Unverified; a logged walk along the board would settle it.

## Smallest fixes (not applied)

1. Route (tools only): for a person outside, approach() measures the stand-off toward the door's outside point, not toward Tom.
2. Close framing (a later item): hide or fade Tom within about 0.8 m of his head, or narrow the side offset while the arm is cut short. Check it with -OfficeCamLog in this corner.
