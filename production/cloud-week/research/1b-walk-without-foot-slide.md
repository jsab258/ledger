**Summary: our joins slide mainly because the feet stand 13 to 27 cm apart between the idle and the start and stop clips, and because walkers and Tom move at a speed their clip does not match; the cure is engine-standard (measure clip speed, foot-down markers, move the start clip so its stance foot lands on the idle's), proved by planted-foot drift per contact, passing at 3 cm or less.**

# A walk without foot slide where clips join (note 1b, 8 October 2026)

## What I could and could not reach

Epic's pages (dev.epicgames.com), GDC Vault, Holden's blog and every forum were refused by the cloud's network (403 at the proxy; not retried). So I read: the repository (code and notes), and two open-source files on raw.githubusercontent.com (Holden's motion-matching demo, the ALS-Refactored animation code). Everything else is a search summary.

Marks. **[SHOWN]**: I read it at its source today (repository code, or the raw GitHub file). **[CLAIMED]**: an earlier repository note says it; that note's author read or measured it on the PC, and I could not re-check. **[SS]**: search summary only; a lead, not evidence. **[I]**: my inference.

## 1. The question

Walk clips are cut or blended into each other (idle to start, start to loop, loop to stop, stop to idle, walk to run, the loop's wrap). At those joins the planted foot should stay still on the ground. Ours drift. What is the professional method, which part of it fits LEDGER, and how do we prove the fix with numbers?

## 2. The professional method, end to end (Unreal 5.4 to 5.8 era)

All of these are engine features. None needs a purchase or a new licence [I; Mixamo itself is already allowed: allowlist item 3, SHOWN]. Epic's Game Animation Sample (the NoAI one) is not used, not opened, and nothing below needs it.

| Method | What it does | What it needs | Fits us? |
|---|---|---|---|
| Speed matching | Body speed = the clip's own travel speed. Loops just scale the play rate; Epic's function assumes constant speed [SS: Epic API page "Set Playrate to Match Speed"] | A measured speed per clip | **Yes, first.** |
| Root motion vs in place | Root motion: the clip moves the body, feet match by construction. In place: the capsule moves the body, so its speed must match the clip. [SS, Epic docs; CLAIMED, METHOD note 6 Oct] | Root motion needs a root bone with travel | Both already in use |
| Distance matching | Picks the clip time from a distance curve, so starts, stops and pivots end where the body ends. Play rate clamp defaults to 0.75 to 1.25. It ignores the phase of the clip before it [SS: Epic API pages, Animation Locomotion Library; Beta in 5.8: CLAIMED, LOCOMOTION note] | Root motion, then a Distance Curve Modifier | Later, for Tom |
| Stride warping, orientation warping (Animation Warping plugin) | Stretches the legs' stride to fit capsule speed; turns the legs to the travel direction. Stride scale = locomotion speed / root-motion speed; 0.5 halves the stride, 2.0 doubles it; a minimum-root-motion-speed setting skips starts and stops [SS: Epic Pose Warping page and API pages] | Root-motion clips and IK foot bones. The cast skeleton has no ik_foot bones (CLAIMED, METHOD note; one forum post agrees, SS). Virtual bones as a stand-in: untested | Not yet |
| Sync groups and sync markers | Keeps two blended loops in step: one clip leads, the others follow between matching markers. Both clips should start on the same foot. Roles include CanBeLeader (heaviest blend leads) and Transition Leader/Follower. Marker sync turns on by itself when markers match, else length sync [SS: Epic docs page; 4.27 page] | A "foot down" marker on each clip, same names | **Yes, for Tom** |
| Inertialization, dead blending | After a cut, the old pose's offset decays instead of a cross-fade. Gears of War 4 (Bollo, GDC 2018) [SS]. Epic ships an Inertialization node and an experimental Dead Blending node (5.3) [SS]. A montage set to inertialization needs an inertialization node after its slot [SS; CLAIMED]. Holden's demo uses a 0.1 s half-life [SHOWN: controller.cpp] | The node in the graph | Yes, for the body, not the feet |
| Foot locking, leg IK | Holds a planted foot in the world. Holden's demo: lock at contact, unlock past a 0.2 m drift, 0.1 s half-life [SHOWN]. ALS-Refactored: a lock curve per foot, lock released at 5 per second once moving [SHOWN: AlsAnimationInstance.cpp]. Epic's Foot Placement node (AnimationWarping) is Experimental and has plant settings (lock around ball or ankle, release angle and radius) [SS; CLAIMED] | Two-bone IK (we have it) | Yes, already partly built |
| Motion matching (Pose Search) | Searches a mocap database for the pose that fits now and soon. Production-ready in 5.4 (Epic blog, 23 April 2024) [SS]. Clips need root motion [SS; CLAIMED] | A large database, editor assets, 30+ hours [CLAIMED] | **No** |
| Mixamo preparation | Mixamo rigs have no root bone, the hips are the top [CLAIMED; SS]. "In Place" is offered clip by clip, not for all [SS]. In-place loops are a treadmill: the planted foot slides back at the clip's speed, so that speed is the number to measure. Foot markers: a script can add them (Blueprint library function AddAnimationSyncMarker; the Python name is unconfirmed [SS]). A free modifier does it by finding where a foot bone crosses the pelvis-to-floor line [SHOWN: its README on raw GitHub] | Our own clip-motion tool and footfall script | Yes |

The honest limit of the first two inertialization-style fixes: they hide differences in pose. They do not remove ground slide. A locked foot hides centimetres, not a stance [CLAIMED, WALK-JOINS note; I agree, because Holden unlocks at 20 cm].

## 3. Why our joins slide: ranked

There are three walkers in the repository. Each has its own causes.

**A. Sheila, the MetaHuman speaker (root-motion clips cut through one slot).**

1. **Stance mismatch at idle, start and stop.** The start's feet are staggered 27 cm from the idle's; the stop's feet are 13 cm off the loop's at best; the cast idle (mh001) is 19.5 to 27.4 cm from the set's own. The set's own stand idle matches within 3.6 to 5.1 cm but was set aside on 3 October because it looks braced [CLAIMED: WALK-JOINS, DECISIONS 8 Oct]. Measured first step 13 to 20 cm, stop 18 to 27 cm, bar 3 cm [CLAIMED]. Our hold pins the stance foot at the idle's place, 27 cm from where the clip wants it, and nothing moves the body to close the gap [SHOWN: PersonAnim.h comment, CrimeProbe.cpp HoldFoot]. This is the largest cause.
2. **The stop blends out on planted feet.** The stop is cut in with 0.1 s and blended out over 0.3 s into the idle [SHOWN: CrimeProbe.cpp, `Cut(Stop, ..., 0.1f, 0.3f)`]. A cross-fade moves planted feet toward the idle's stance [I].
3. **The earlier warp try failed on reach.** The body slid 25.8 cm and the held left foot 42 cm. The note's own guess: the foot was pulled out of the leg's reach with stretching off [CLAIMED]. `bAllowStretching = false` is set [SHOWN].
4. **Smaller ones** [CLAIMED]: ankle held while the ball is measured; the stop's bake slips 3.9 cm.
5. **The baked loop speed (1.80 m/s) is above the expected 1.0 to 1.6** [CLAIMED, METHOD step 4]. If the changeover frames double-count, the body outruns the feet [I].

**B. The street walkers (Mixamo clip, actors, `ULedgerPersonAnim`).**

1. **Fixed speed against clip speed.** The walker moves at 1.2 m/s unless the street file says otherwise [SHOWN: StreetMeshes.h 524]. The clips travel: Walking 1.61 m/s, Female Walk 1.02 m/s [CLAIMED, from tools/clip-motion.py]. The planted foot then skates at 0.41 m/s backward, or 0.18 m/s forward [I, subtraction]. This is a steady slide, not only at joins. The 30 September note already called it "the first fix" [SHOWN].
2. **Start and stop are a straight cross-fade, with no phase.** The weight ramps at 2.0 per second (0.5 s), the body's speed is the walk speed times that weight, and the pose is a linear idle-to-walk blend [SHOWN: PersonAnim.cpp lines 452, 442; `FAnimNode_TwoWayBlend`]. The walk loop is never set to a foot phase when the walker sets off [SHOWN: no such call]. While the weight falls, the clip still steps at full pace under a slowing body [I].
3. **Turning at the ends** is a yaw at 180 degrees a second with no turn clip [SHOWN: PersonAnim.cpp 447]. Planted feet pivot [I].

**C. Tom (a Character; idle, walk and run players, `ULedgerLocomotionAnim`).**

1. **No sync.** The three loops free-run and two-way blends mix them by speed, with no sync group or marker [SHOWN: LocomotionAnim.cpp]. The run is played at 1.5 times [SHOWN]. Out-of-phase loops average to feet that hover and shuffle [I].
2. **The run clip covers about half the ground.** 2.28 m/s of foot travel against a 4.2 m/s capsule [CLAIMED, METHOD note]. Worth re-measuring.
3. **Blend follows raw capsule speed.** Alpha is speed over 160 cm/s, unsmoothed [SHOWN]. No acceleration, braking or friction line is set in SliceCharacter.cpp [SHOWN: grep], so engine defaults apply and the capsule stops and starts within roughly a tenth to a third of a second [I].
4. **The one thing right:** the walk clip's 1.61 m/s against a 1.6 m/s capsule [CLAIMED; SHOWN for the 160].
5. **Loop seam.** A Mixamo export often repeats frame 0 as its last frame, which holds the feet for one frame at each wrap [SS: forum reports]. Unchecked here.

## 4. The fix that fits LEDGER, in order

Hours are mine [I], on the repository's earlier estimates.

1. **Measure each clip once (0.5 h).** For every walk, run and start/stop clip: travel speed from the planted foot, cycle time, footfall times, first and last frame match. `tools/clip-motion.py`, `planted_travel` in `make_root_motion_clips.py` and `tools/ue/footfalls.py` already do most of it. Known now: Tom's walk footfalls at 0.193 s (left) and 0.676 s (right) in 0.967 s; run at 0.254 and 0.805 in 1.1 s [SHOWN: SliceCharacter.h 128 to 129].
2. **Match speed to clip (1 h; fixes B1, C2, C3 partly).** Body speed = clip speed. Keep play rate within 0.9 to 1.1 of 1.0 (Paragon's play-rate change was 15% [CLAIMED]; Epic's clamp default is 0.75 to 1.25 [SS]). If the street wants 1.2 m/s and the clip does 1.61, the rate would be 0.75: choose a slower clip or accept about 1.45 to 1.6 m/s. Give Tom's run a clip that covers its speed, or lower the run's speed to the clip's.
3. **Start the walk on a foot (1 to 2 h; fixes B2).** When a walker sets off, set the loop's time to just before a footfall (0.193 s for Tom's walk) and shorten the ramp from 0.5 s to 0.25 to 0.3 s (start value, to tune [I]). When it stops, let the body slow only after the next footfall.
4. **Markers and a sync group for Tom (2 to 3 h; fixes C1).** Markers `FootDown_L` and `FootDown_R` at the times above, one sync group on walk and run (not the idle), both able to lead. Smooth the blend alpha (0.15 to 0.25 s, start value [I]). In native code the sequence player has a group name, role and method [I: confirm on the PC, section 7].
5. **Move the clip, not the foot (1 to 2 h; fixes A1).** At the cut from idle to start, shift the start clip's root so its stance foot lands exactly on the idle's stance foot (up to 27 cm). The body then jumps; take the jump out of the pelvis, spine and arms with a decaying offset, half-life 0.1 s (so about 90% gone in 0.33 s; Holden's value [SHOWN]), while both feet stay pinned. One pinned foot with the pelvis moving between two reachable poses always stays within the leg's reach, because the reachable set around a foot is a ball [I, geometry]; this is what the earlier warp try lacked. Release the swing foot when the clip lifts it (the right lifts at frame 5 and is let go at 8; the left lifts at 16 and is let go at 19; each over 0.06 s: the existing numbers [SHOWN: CrimeProbe.cpp]). Test: the stance foot drifts 3 cm or less over the first step.
6. **End the stop on its own last pose (1 h; fixes A2).** No 0.3 s blend-out on planted feet. Hold both feet at the stop's last frame, ease the body to the idle over 0.3 s, and move the second foot with a short settle step (3 to 5 cm lift, 0.3 to 0.4 s). The stop already has a 5 cm shuffle [SHOWN: comment at CrimeProbe.cpp 8133].
7. **Inertialize the body at cuts (1 to 2 h).** An Inertialization node after the slot, montage blend mode Inertialization; keep the legs out of it if the node allows (it can exempt bones [SS]). Dead Blending is the experimental alternative.
8. **Only later:** distance matching for Tom's stops; stride warping once IK foot bones exist; the shape-difference step between stances for the stop. Do not build motion matching.

## 5. How to verify with numbers

The walk proof already measures a version of this [SHOWN: CrimeProbe.cpp 8081 to 8103]. Make it stricter:

- **Record every rendered frame**, not every tenth: world position of `ball_l` and `ball_r`, the floor height, the clip name and time, from an editor run and from the packaged game. Last night's crude test read 0 to 1 cm at 10 frames a second and 2.5 to 6.6 cm at 100 [CLAIMED, DECISIONS 8 Oct]. A number without its sample rate means nothing.
- **Contact** = the ball within 2.5 cm of the floor and the lower foot, or the clip's own footfall to lift-off times. **Slip** = the largest ground (x, y) drift from the first frame of that contact, in cm.
- **Report per join**, not one worst number: idle to start, the steady loop, walk to run, the loop's wrap, loop to stop, stop to idle, and a turn.
- **Pass:** every contact 3 cm or less (the existing bar); median planted-foot ground speed 5 cm/s or less; pelvis jump between clips 2 cm or less (both the repository's bars [CLAIMED, LOCOMOTION note]); body speed within 0.9 to 1.1 of the clip's.
- **Target:** 2 cm. Viewers in a 2011 study noticed slides under 21 mm in most conditions (Práček, Hoyet, O'Sullivan, SCA 2011 [SS]); at street distance 3 cm is the working bar, and a fresh reviewer's eye still decides.
- **No agreed standard exists** in the literature: one common measure counts frames where a foot slides over 2.5 cm while under 5 cm high; another counts a vertex moving over 0.66 cm a frame [SS]. Ours is the first, stated per contact.
- **Repeat** the route 10 times from random loop phases (a walker standing 1 s, setting off, 6 m, stopping) so a lucky phase cannot pass.

## 6. To check on the PC

- **Sequence players in sync groups.** `FAnimNode_SequencePlayer` (and `_Standalone`): its group name, group role and sync method members, and whether a native proxy with a custom root node actually ticks sync groups. This decides step 4.
- **`FAnimNode_TwoWayBlend`:** whether it still updates the walk player at alpha 0 (it decides where the walkers' clip time is when they set off).
- **Animation Warping plugin** (module AnimationWarping): the flags in its .uplugin, `FAnimNode_StrideWarping` foot definitions, whether a virtual bone can be the IK foot; `FAnimNode_FootPlacement` status.
- **Animation Locomotion Library** (`UAnimDistanceMatchingLibrary`, `UDistanceCurveModifier`) and **BlendSpaceMotionAnalysis**: callable from native code, or Blueprint references only.
- **Inertialization:** `FAnimNode_Inertialization`, `FAnimNode_DeadBlending`, and `EMontageBlendMode`; the bone-exemption setting.
- **`FAnimNode_TwoBoneIK` with stretching off:** what it does when the target is out of reach (clamp, or drift). It explains the 42 cm.
- **`UCharacterMovementComponent` defaults** (MaxAcceleration, BrakingDecelerationWalking, GroundFriction, BrakingFrictionFactor): measure Tom's real start and stop times.
- **Marker tools:** `AnimationBlueprintLibrary` sync-marker function name in Python (`dir()` it); the existing L and R markers on the plugin's loops and starts.
- **Tom's clips:** frame 0 against the last frame; the run's travel speed again.

## 7. Sources (all accessed 8 October 2026)

**Reached and read ([SHOWN]):**
- Repository: ue-probe/Source/LedgerProbe (PersonAnim.h/.cpp, LocomotionAnim.h/.cpp, SliceCharacter.h/.cpp, CrimeProbe.cpp 7889 to 8154, StreetMeshes.h, VignetteShot.cpp); tools/ue/make_root_motion_clips.py, tools/ue/footfalls.py, tools/art-recipes/person-export.py; DECISIONS.md (8 Oct lines); NOW.md; allowlist.
- Repository notes, read but not re-measured ([CLAIMED]): production/research/sit-and-turn/ (LOCOMOTION 6 Oct, METHOD 6 Oct, RETARGET-FAULT 7 Oct, WALK-JOINS 8 Oct); townspeople-animation/SUMMARY.md (30 Sep).
- https://raw.githubusercontent.com/orangeduck/Motion-Matching/main/controller.cpp (undated file): unlock radius 0.2, blend half-life 0.1. Read as method only; nothing copied.
- https://raw.githubusercontent.com/Sixze/ALS-Refactored/main/Source/ALS/Private/AlsAnimationInstance.cpp and README.md (undated): foot-lock curves. Its LICENSE file was not found at that path (404), so nothing is to be taken from it, method only.
- https://raw.githubusercontent.com/TheEmidee/UEAnimationModifiersExtras/master/README.md (undated): foot sync marker modifier. Not recommended for adoption.

**Search summary only, not reached ([SS]; leads, not evidence):**
- dev.epicgames.com/documentation/en-us/unreal-engine/: animation-sync-groups-in-unreal-engine; pose-warping-in-unreal-engine; distance-matching-in-unreal-engine; motion-matching-in-unreal-engine; fix-foot-sliding-with-ik-retargeter-in-unreal-engine; locomotion-in-unreal-engine; API pages for AnimDistanceMatchingLibrary, DistanceCurveModifier, AnimNode_StrideWarping, AnimNode_OrientationWarping, AnimNode_FootPlacement, AnimNode_DeadBlending, EAnimGroupRole.
- docs.unrealengine.com/4.27 SyncGroups (4.27, old).
- unrealengine.com/en-US/blog/unreal-engine-5-4-is-now-available (23 April 2024).
- theorangeduck.com/page/dead-blending (Holden, February 2023) and /page/dead-blending-node-unreal-engine (13 August 2023).
- gdcvault.com/play/1025165 (Bollo, GDC 2018); gdcvault.com/play/1022985 (Clavet, GDC 2016).
- diglib.eg.org/handle/10.2312/SCA.SCA11.287-294 (Práček, Hoyet, O'Sullivan, 2011); research.cs.wisc.edu/graphics/Gallery/kovar.vol/Cleanup (Kovar, Schreiner, Gleicher, 2002).
- issues.unrealengine.com/issue/UE-387801 (a marker-sync crash in 5.7.4; check before relying on markers in a looping blend).
- unamedia.com/ue5-mixamo and forums.unrealengine.com threads (Mixamo root motion, loop seams; forums and vendor, last resort).

**Refused by the cloud's network (403), so unreached:** dev.epicgames.com, docs.unrealengine.com, unrealengine.com, forums.unrealengine.com, theorangeduck.com, gdcvault.com, gamedeveloper.com, wikipedia, youtube, fab.com, helpx.adobe.com.

**To read from the PC or once the network opens (short list):** Epic's sync groups, Pose Warping, Distance Matching and "Fix foot sliding with IK Retargeter" pages for 5.8; Epic's 5.8 release notes (animation); Holden's two dead-blending posts; Bollo's inertialization slides (GDC 2018); the full text of Práček 2011; Epic's Lyra animation page (method only); the UE-387801 report.
