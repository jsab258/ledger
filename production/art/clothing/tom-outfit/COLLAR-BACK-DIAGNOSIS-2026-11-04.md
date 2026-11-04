# Tom's collar back through his neck in Sheila's talk (diagnosis, 4 November 2026)

Fault: ai-tester 0203 steps 75 to 77 and 0210 steps 27, 28; not Ron's talk (0210 steps 16 to 18).

## Is the measure wrong?

Partly. Sheila's talk takes the close shot (camera.json talk.close: 0.80 m back, level with the collar); Ron's the far one. Cropped, Ron's step 17 also shows a small dent back left: the fault is in both, Sheila's deeper and filmed closer.

## Cause, ranked

1. **The collar is fixed to the trunk while the skin above it moves with the neck. High confidence.**
   - The worn jacket (v30-reskinned, skin.json) is weighted up to spine_05 only: no neck_01, neck_02 or head.
   - The skin at the collar is the head mesh's (seam 1.50 to 1.59 m; collar top 1.673 to 1.682 m). At rest it sits only 1.6 mm inside the collar.
   - Offline turn test, 2 Nov (head-map-record.json): 45 degrees left, skin through 5.0 mm, rim up to 18 mm into visible skin; 45 right, 2.4 and 16 mm.
   - The jacket copies the body's bones by name (UE 5.8.2 SkinnedMeshComponent.cpp:2361-2370), so any neck turn or bend spine_05 does not share brings skin over the rim, jagged along the triangles.
2. **Bigger head angles in Sheila's talk. Low to medium confidence; estimated from the pictures.**
   - 0203 step 77, 0210 steps 27, 28: head 60 to 75 degrees left of the chest (past the 45 tested), notch back right.
   - 0203 steps 75, 76: 10 to 20 degrees right, but 1.5 times more neck showing than Ron's step 17: likely bent forward.
   - Ron: 15 to 25 degrees left.
   - Nothing aims Tom's head at Sheila, so her height plays no part:
     - his head is Epic's mover pose only (SliceCharacter.cpp:755-761; MotionMatchAnim.cpp:146-159), held only while he sits (SliceCharacter.cpp:2555);
     - FaceForTalk turns only the camera (SliceCharacter.cpp:296-310, 376-391);
     - Look At is on the cast only (CrimeProbe.cpp:1151-1161);
     - the sample's aim offset needs strafe (its Enable_AO), which GaspTick turns off (SliceCharacter.cpp:849-859).
   - Inferred: in both Sheila talks Tom is pressed against her blocking capsule (0203 step 74, 0210 step 26) as the talk camera turns; the sample's starts and turns lead with the head.
3. **The hidden-face body map is not involved.** It cuts body faces only; the skin seen is the head mesh's. A head shrink map cannot fix skin over the rim (that record's note).

## Measured and inferred

- Measured offline: the weights, the seam, the rest gap, the 45-degree crossings.
- Inferred: every in-game angle.
- Not reached:
  - the walk's game log (overwritten);
  - any head angle line outside sitting;
  - whether a head map is built in;
  - the clip playing.
- To confirm: log HeadAgainstChest (LedgerGarments.h:209-224) and the mover's clip every 0.1 s in a talk; rerun the offline test at those angles, noting where round the neck each crossing falls.

## Candidate fixes

1. **Weight the collar's top band to neck_01 (about 30 to 50% at the edge, fading to spine_05; back and sides first).**
   - Start from v33 or v34, measured offline at 60 to 75 degrees first.
   - Cost: about 2 hours plus one packaged walk; one of the two tries.
   - Risk: set aside for the chin fault; the front may crush looking down.
2. **Limit his head against his chest in FLedgerHeadUpNode (turn about 40 degrees, forward bend about 10).**
   - Cost: about 2 hours of C++, a game build and a walk.
   - Risk: stiffer turns; the passed walk and sit walked again; hides the cause.
