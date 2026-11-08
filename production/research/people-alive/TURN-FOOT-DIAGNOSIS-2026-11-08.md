# Tom's left foot in the turn into the run: diagnosis, 8 November 2026

Diagnosis only. Nothing was changed, built or run.

## The measure first: is the fault real?

Yes. Frames 675-700 of gate/new/side-walk-2026-11-08 were read with PIL; the camera stays fixed from 661 to 721.
- 676-682: the rear (left) shoe is still, toe at x 447.
- 683-689 (24.75-24.95 s): the toe creeps to x 474, 27 px. That is about 5 cm, taking the shoe as 28 cm long (assumed).
- Its drawn length stays 138-142 px, so its heading turns 15 degrees at most while the hips drive right.
- 690: it lifts and turns in the air. It never pivots on its ball.

The walk's own measure cannot see this. It reads only where the ball moves while down, never its heading (SliceCharacter.cpp, MeasureFeet).

## 1. What plays him

- Epic's Game Animation Sample (the GASP) moves an unseen mannequin. Tom's MetaHuman copies it through RTG_UEFN_to_Metahuman_nrw (walk.log lines 1725, 1746).
- The route turns the input to "run, the other way" in one frame from standing (SliceCharacter.cpp 943, 1192). A player can do the same.
- The run starts come from the database PSD_Dense_Stand_Run_Starts (gasp exports, chooser_Dense.t3d:92). The likely clip is M_Neutral_Run_Start_B_Rfoot or BR_Rfoot, since the right foot lifts first; not confirmed.
- The graph (SandboxCharacter_CMC_ABP.t3d) applies, in order:
  - orientation warping and steering in each clip;
  - Offset Root Bone, rotation half-life 0.1 s;
  - Foot Placement (always on; pivot around the ball; plant speed 50);
  - Leg IK.
- No turn-in-place: the mover is moving by 24.62 s.

## 2. Most likely cause

The foot keeps its old heading because Epic's 180° start clip, as matched and blended, does. Neither the foot lock nor the copy onto Tom does it.
- **The lock cannot hold a heading.** "Pivot around ball" pins only the ball's place and takes the foot's turn from the incoming pose (AnimNode_FootPlacement.cpp:1716-1720, 738-750, UE 5.8.2).
- **The body's own turn would turn the foot too.** Offset Root Bone comes before the lock. A foot that keeps its heading therefore means the clip turns the body over an unturned foot.
- **The 60° let-go cannot help.** It tests the ground-alignment twist, not the body's heading (:632-635).
- **The mannequin did the same on 24 Oct.** Its left ball stayed put (to 0.1 cm, contact 0) from 24.75 to 24.88 s, moved 7 cm, then lifted at 25.0 s (runs/tom-walk-fixedtraceall.txt).
- **The same pattern was seen before.** The 24 Oct review saw it in the walking pivot: "planted pointing the old way ... lifts and turns in the air".

Confidence: moderate, about 60%.

## 3. Is it old?

Yes; confidence high.
- The 24 Oct review saw this moment: "24.60-24.95, left forefoot scrubbed toward the run".
- The 5 and 8 Nov result lines are identical to every decimal.
- No commit since 26 Oct changes a GASP setting. The commits touch sitting, stops, head-up (idle while walking) and hair.

## 4. Cheapest candidates (none made)

1. **Confirm.** One packaged run with `-GaspShowMannequin -TomWalkProofTraceAt=24.5-25.1` added. If the mannequin shows the same flat backward foot, the fault is Epic's data; if not, it is the copy. Naming the clip needs the editor's Rewind Debugger.
2. **List it as a known shortfall:** narrow, old and in Epic's clip. Costs nothing.
3. **A pivot on Tom's copied pose** (MotionMatchAnim.cpp). While a foot is down and more than about 60° off the pelvis heading, turn it about its ball towards that heading. Check: in the same frames the shoe's drawn length should shrink, and the joins should not change.
4. **Keep motion matching off the B starts.** This is an Epic asset edited in the editor, and it changes every start. Check: frames 676-692 and every start's join.
5. **`-GaspPlantSpeed=1`.** It shortens the hold by 1-2 frames at most. Not recommended: his passed walk used 50.

## Not checked

The clip's name, the pelvis heading, the shoe's real length, whether the 13.68 cm worst stop is this contact, whether the warping and steering are switched on, and Epic's own sample at this turn.
