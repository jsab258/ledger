# Tom's walk by Epic's MetaHuman route: the second go, 24 October 2026

His order of 24 October: "start the walk's next go now ... by Epic's MetaHuman route: the sample's own character as the mover, Tom's MetaHuman body worn over it, with the 3 cm foot-slide bar."

**Result: built and running; not passed. The slide is set aside after two genuine tries (his rule).**
- Epic's route runs in the game with `-LedgerGaspMover`, off by default:
  - the Game Animation Sample's own character (SandboxCharacter_CMC, unchanged) moves, unseen;
  - Tom's MetaHuman (L1) is worn in its slot.
- **The typical step is near the bar:** median slide 1.2 to 4.3 cm by kind.
- **The worst steps fail it:**
  - starts 15 cm;
  - stops 35 cm (the stop's low scuff, below);
  - turns 11 cm;
  - one steady-walk step 21 cm.
- His own clips, measured the same way, give starts 51, turns 50 and steady walk 52 at worst. Their medians are 3 to 23.
- The hidden mannequin's feet slide as much as Tom's. The copying adds little; the slide comes from the sample's own walk as driven here.
- **By eye** (research after the set-aside, pictures judged by a fresh reviewer): ordinary planted steps hold within 1.5 cm. A weight-bearing foot visibly slides 10 to 15 cm at about five moments of the route:
  - a stop's flat glide of 13 cm, the one a player may notice;
  - a pivot;
  - two turns from standing;
  - a landing.
  The measure's other large figures are swinging feet passing low.

This text was corrected after a fresh review (`metahuman-route-2026-10-24/REVIEW.md`), which found:
- the medians wrongly taken;
- a fault in the measure (fixed, below);
- three claims stated as fact without proof (each now checked or withdrawn).

## Questions and where they were answered

The questions are in `metahuman-route-2026-10-24/QUESTIONS.md`.

- **Epic's own pages** (`EPIC-SOURCES.md`, 24 sources read 24 October):
  - They describe the 5.4/5.5 sample only. Nothing documents SandboxCharacter_CMC, AC_VisualOverrideManager or the "ovw" retargeter.
  - Epic's one rule for a hidden mover: its mesh must "always tick pose and refresh bones" and tick before the worn body.
  - Epic documents Speed Planting for stored animations; whether it works live is not said.
- **The engine's source** (`ENGINE-SOURCE.md`, file and line cited):
  - The sample's retargeters set Blend to Source = 1 on both legs, so Tom's foot goal is placed on the mannequin's foot. ENGINE-SOURCE lists six exceptions: reach, a stale or late pose, frames, pelvis offset, later nodes, and toe swing.
  - The retarget node walks up the attachment chain to find its source mesh.
- **The sample's own files** (exported to text and read; `F:/LedgerTools/game-inputs/gasp/exports/`):
  - Its character carries a child-actor slot tagged `VisualOverride`.
  - AC_VisualOverrideManager sets a body class there and hides the mannequin (SetVisibility false; the mesh ticks pose and bones always).
  - BP_Kellan's body is tagged `RTG_UEFN_to_Metahuman_nrw`.
  - ABP_GenericRetarget looks that tag up in its IKRetargeter_Map and copies from the parent mesh.
  - Its character reads its gait from its own `CharacterInputState` (WantsToWalk, WantsToSprint, WantsToStrafe, WantsToAim, WantsToCrouch).
- **Read in the game's editor** (`plant_check`, 24 October 10:20):
  - The foot placement's plant settings in force are the graph's own variables.
  - **PlantSettings_Default:** UnplantRadius 20 cm, UnplantAngle 60°, lock pivoting around the ball.
  - **PlantSettings_Stops:** UnplantRadius 40 cm, replant ratio 0.75.
  - 57 of the first 60 walk and run clips carry the `contact_l` and `contact_r` curves its foot placement plants by. It does plant.

## What was built (ue-probe/Source/LedgerProbe/Private/SliceCharacter.cpp, StartGaspMover and GaspTick)

- **Into the game:**
  - The sample's 847 missing assets (about 1 GB, mostly its animations), copied at their own paths. Not in git; attributed in tools/attribution-check.py.
  - Its plugins.
  - Its settings: data-driven variables, gameplay tags, trace channels and pose search buffer.
  - The Sequencer mixer plugin is left out. It asserted on the game's own animation instances at the first frame.
  - The packaged build with these passed on the build machine: frames 15.2 ms median and 23.4 worst; card 5.5 GB.
- **The mover:**
  - It has a controller of its own, never the player's. Tom's capsule rides on it.
  - The keys', the pad's and the measure's input are handed to it each frame.
  - His pace goes as its own input state: walk unless running. Strafe and aim are off, because he turns to where he goes.
  - It moves at the sample's own speeds (walk 200 cm/s, run 500), not the game's (160 and 420).
- **The worn body**, as the sample dresses Kellan:
  - Tom's MetaHuman in the slot. Its Body is tagged for Epic's retargeter and runs ABP_GenericRetarget.
  - The mannequin is hidden. The worn body touches nothing and always works out its pose.

## The measure, and five faults found in the harness

The set route of 22 October (`-TomWalkProof`) is unchanged. A planted foot is a ball within 2.5 cm of its standing height and no higher than the other foot. The slide is its drift while planted.

Five faults were in the harness, not the walk, and each was fixed:
1. **The mover was made where Tom loaded, and the game then placed him at his start.** The mover now follows wherever the game puts him.
2. **The sample's character strafes toward its controller's view by default.** Strafe is now off.
3. **A MetaHuman's parts work out their pose only when drawn.** The worn body now always does.
4. **Heights were read from the capsule's foot.** A kerb read a foot as planted for metres. Each ball's height is now read from the ground traced under it.
5. **"No higher than the other foot" compared raw heights.** Tom's two balls stand a few millimetres apart, so a swinging foot passing low read as planted. This one was found by the fresh review. Each foot is now compared against its own standing height.

This last fix also lets the stop's scuff count. In it, the trailing foot slides forward about 45 cm, 1 to 3 cm off the ground, to meet the other. By the rule it is a planted foot sliding. Whether a player sees it as one is open (direction C).

## Results (two runs each, the same start and heading; `metahuman-route-2026-10-24/runs/`)

Median / worst slide in cm, with steps over 3 cm (itemised contacts):

| Kind | Epic's route, Tom's MetaHuman (gasp12a, b) | the sample's mannequin under him | his own clips (default2, one run) |
|---|---|---|---|
| starts | 3.3 / 14.9, 5 of 8 | 4.0 / 15.3, 7 of 8 | 5.4 / 50.6, 5 of 7 |
| stops | 4.3 / 34.9, 9 of 12 | 3.8 / 16.9, 12 of 14 | 16.2 / 18.7, 2 of 3 |
| turns | 3.7 / 11.1, 13 of 22 | 5.2 / 13.2, 17 of 18 | 23.3 / 50.4, 11 of 14 |
| steady walk | 1.4 / 21.0, 16 of 48 | 2.7 / 22.9, 17 of 40 | 3.2 / 51.6, 21 of 30 |
| run | 1.2 / 6.2, 3 of 16 | 1.9 / 3.3, 1 of 16 | not read* |

\* His clip run lowers his body 21 cm (RunDropCm). Calibrated standing, the measure reads both feet as planted; his stops after the run carry the same fault.

A contact's kind is set when the foot lands. A slide that starts in a stop and goes on into the next start counts as a stop.

## The two tries at the slide, each shown to have taken

Each run's result line now reports the settings in force at the route's end.

1. **The sample's own alternatives:**
   - Its sparse animation sets (`DDCvar.MMDatabaseLOD 1`) took and were worse: stops 71 cm.
   - Its control-rig feet (`DDCvar.FootPlacementMode 2`) were no test. The console setting took, but nothing in its character's graph reads it. Setting the graph's own `FootPlacementMode` variable (to 0 or 1, read back at the route's end) leaves every number identical to the decimal, because its Foot Placement node is always on: its enable is fixed true, in the main chain.
2. **The sample's foot lock held through each contact.** This is the node that runs; its plant settings are bound to the variables changed here. Its let-go distance and angle were raised from 20 cm and 60° to 100 cm and 180° on its own graph at run time (`-GaspUnplantCm=100 -GaspUnplantDeg=180`; took). Nothing changed: Tom's stops 35, turns 20, steady walk 24. So the slide does not come from the lock letting go.

Not a try: the sample's attribute-based root motion. Set from startup, the setting read 1, but the character never used root motion (`rootMotionUsed=0`, run t2rmv).

## Why it stops short of 3 cm: what is known, and what is not

- **Known:** the mannequin under him slides as much as he does. With Blend to Source = 1 he copies its feet, so the slide is in the sample's own walk as driven here.
- **Known:** its foot lock letting go at a distance is not the cause (try 2).
- **Known:** the body does not lag its capsule. The sample's root offset is 0 cm at every frame of the worst stop, because its own default `DDCvar.OffsetRootBone.TranslationRadius` is 0. So the stop glide is not the body catching up.
- **Known (traces, 11:35 to 11:49):** while a clip marks a foot as planted, the lock holds it within 0.5 cm, with foot placement on or off. Every real slide happens while the clip marks the foot as moving, so the lock lets it follow the clip, and the clip moves it along the floor. The stop's 13 cm glide is the clip `M_Neutral_Walk_Stop_F_Lfoot` (its name traced each frame). So the slide is in the sample's animation data as matched, not in the lock and not in the dressing.

## Research after the set-aside: does the measure count what a player sees? (24 October, 10:40 to 11:35)

The walk itself is unchanged. These are readings and pictures.

- **How the field measures foot skate** (`metahuman-route-2026-10-24/FOOT-SKATE-MEASURES.md`, 28 sources):
  - A foot is planted when it is both low and slow, heel and toe apart (Epic's Foot Placement: ball under 60 cm/s and within 10 cm).
  - Skate is reported as an average or a share of frames, never the worst single contact. Real motion capture scores above zero.
  - No studio or paper publishes a pass mark; studios judge by eye.
  - About 2 to 3 cm is roughly what people notice. A 2011 study (abstract only) puts viewers' detection at under about 2 cm; walking-slip research puts a felt slip at about 3 cm.
- **The worst steps pictured and judged by a fresh reviewer** (`metahuman-route-2026-10-24/VISUAL-REVIEW.md`):
  - All ten spans were pictured on a fixed time step, with a still side camera.
  - Ordinary planted steps hold within 1.5 cm.
  - A weight-bearing foot visibly moves more than 3 cm in about five places:
    - a stop where the front foot glides back flat about 13 cm after the body has stopped. This is the one a player is most likely to see: possibly from behind, obviously from the side.
    - a pivot's forefoot slide of about 15 cm;
    - two standing turns of 10 to 12 cm each;
    - an unclear landing of 7 to 12 cm.
  - The height reading's other big figures are swinging feet passing 1 to 2.5 cm over the floor, or separate contacts merged across a stop.
- **A second reading, planted by the animation's own contact marks:**
  - It is reported beside the height reading in each result line.
  - It gives worst 2.7 to 2.8 cm (a pass) but misses all the real slides above, because the animation marks those feet as moving.
  - **It is not adopted.** It would pass a walk that visibly slides.
- **What this means for the bar's measure:** the height reading over-counts (swings, merged contacts), and the contact-mark reading under-counts (drags marked as moving). Neither is the field's own; the field judges by eye. The walk fails the bar by eye too, by about 10 to 15 cm at five moments.

## Next directions (for the next go; the slide stays set aside under his rule)

- **D, now first: measure the clips themselves.** Read the foot travel while low and marked moving in the stop clip `M_Neutral_Walk_Stop_F_Lfoot` and in the pivot and turn clips the trace names, offline from the assets. Find which clips carry the slides. Then choose among:
  - a lock that holds a foot while it is low and slow, not only while marked planted (the field's contact test; the leg takes up the difference);
  - leaving the sliding clips out of the motion-matching sets;
  - a world-space lock on Tom's body (A).
- **A: a world-space foot lock on Tom's own body after the retarget,** releasing only when the foot lifts clear (engine route: ENGINE-SOURCE.md, point 5). Expect the leg to take up the drift instead (a stretched or bent knee). Holden: "almost always better to let feet slide than to break the pose".
- **C, the measure:** pictured judgement as the gate for the worst steps, as the field does. The height reading keeps flagging where to look.
- **To make it the default, whichever passes:** its assets reach the build machine; it is walked packaged.

## Cost

About 3.5 hours, 08:00 to 11:35, including the research helpers, the fresh review of the findings and the reviewer of the pictures.

## Evidence

- `metahuman-route-2026-10-24/`: QUESTIONS.md, EPIC-SOURCES.md, ENGINE-SOURCE.md, REVIEW.md, FOOT-SKATE-MEASURES.md, VISUAL-REVIEW.md.
- `metahuman-route-2026-10-24/runs/`, every run cited above (and fpoff, fp1a/b, roottrace and cliptrace for the foot placement and clip traces):
  - gasp12a and gasp12b: Epic's route, final measure;
  - t1fp2v and t2locka/b: the tries;
  - t2rmv: root motion, not taken;
  - default2: his clips;
  - gasp11a/b and t1*: under the earlier measure;
  - trace1: a stop frame by frame.
- The sample's exports: `F:/LedgerTools/game-inputs/gasp/exports/`.
