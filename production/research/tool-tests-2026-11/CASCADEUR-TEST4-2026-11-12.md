Method researched: production/research/tool-tests-2026-11/CASCADEUR-METHOD-2026-11-12.md (Cascadeur help and Python API, read 2026-11-12)

**Not passed (try 2 of 2): from Python with no click, Cascadeur rigged the MetaHuman and its Fix Foot brought foot slide under 1 cm on both feet with the timing kept, but the knees stayed bent (left 11.5, right 29.3 degrees), the toes stayed pitched about 23 degrees down with the balls pushed 1 to 2 cm into the floor, Auto Physics changed nothing measurable, and the app crashed on the render-to-video call, before any film or FBX export.**

Licence found in Cascadeur's own log: a two-week Trial (flags export, profeatures, trial; ends 2026-11-25), not the Free licence. So the Free limits are still unmeasured. Try 1 is below as first written. Try 2 is at the end.

Test 4 of PLAN-2026-11-11 (head-turn solve m2s1101e_Body.fbx), 12 Nov 2026, 10:27 to 10:31 local, driven only through Cascadeur's local script server (POST /run). No clicks, no keys, no screenshots.

## Limits
- FBX import on this licence: met, no click. FbxLoader.import_scene from Python brought in 342 joints and the animation ("Import scene: scene imported"). The scene runs at 30 fps and the file is 24 fps; Cascadeur warned and resampled, so the clip became 100 frames at 30 fps (same length in seconds, last frames held).
- Export formats: not measured. The API reports app.is_export_available() = True and app.is_pro_features_available() = True, which contradicts the plans page (Free saves .casc only); the licence may be on a trial. No FBX or .casc export was tried before the crash.
- Rig from Python: blocked (crash). RiggingWindow.create_from_qrt_by_fileName with the shipped Metahuman.qrigcasc template raised "Rig mode several animationInfo" (its check wants exactly one AnimationInfo on a scene made by FBX import), then Cascadeur closed itself inside _flatten_qrt_twist_data. The process was gone and the server refused connections at 10:31:35.
- Physics and clean-up tools from Python: unmeasured. What the API exposes: AutoPhysicTool has only turn_off and turn_off_all_fulcrum_points (no "turn on" or solve call); FixFootTool's editor has no methods; AutoPosingTool has add/update/activate/deactivate on a session. The action ids (AutoPhysicsTool.*, View.FixFoot) would go through ActionManager.call_action(key); not tried, because all of them need a rigged character first.

## What was done
1. Read the method note, the script server README and AGENTS.md; checked /health (ok).
2. Introspected csc, csc.fbx, csc.tools, the tools manager (55 tools listed) and the rigging window through /run.
3. Imported the clip into the empty scene with FbxLoader.import_scene (no dialog).
4. Measured the raw clip in Cascadeur, Y up, centimetres, frames 0 to 99 (measure_lib.py).
5. Called the quick rigging tool with the MetaHuman template: Cascadeur crashed. Per the brief (do not restart it), the test stopped there. One try only; the second try was not possible without a restart.

## Before and after against the bars
"After" is empty: no tool ran.

| Bar | Before (measured in Cascadeur) | After |
|---|---|---|
| Foot slide 1 cm or less, each foot | left ankle 2.60 cm, left ball 2.22 cm; right ankle 0.54 cm, right ball 0.82 cm (max over frames, horizontal, from frame 0) | not reached |
| Standing knees within 5 degrees of straight | left median 28.5, worst 35.0; right median 28.2, worst 34.9 (degrees bend, thigh-calf-ankle) | not reached |
| Toes flat | left ball 1.8 to 2.9 cm above floor, foot pitched 23.2 deg toes-down (median, worst 26.8); right ball -0.1 to 0.1 cm, pitch 21.6 deg (worst 23.8). Floor = lowest foot joint, -0.1 cm | not reached |
| Timing kept | head yaw rises from 0 at frame 0 to its 51.6 deg peak at frame 23, holds about 44 to 51 deg, falls from about frame 78 to 11.4 deg at frame 98 (30 fps frames) | not reached |

Also measured: head drifts 5.4 cm horizontally from frame 0 (matches the known 5 cm back). Left ankle sits 8.3 to 9.4 cm up against the right's 5.9 to 6.6 cm.

## Needs clicks / Python reach (plan item 6)
- From Python, no click: starting the script server (already done at launch), FBX import, reading every joint's world position and matrix per frame, listing tools.
- Rig creation: the call exists in Python but crashed the app on an FBX-imported scene. Whether the same template works through the quick rigging window by hand: unmeasured.
- Auto Physics on, Fix Foot, auto posing: no direct Python call to switch Auto Physics on or run Fix Foot; only action ids through call_action, untried. Unmeasured.
- Film beside the original: RenderToFile.play_to_video_file(scene_view, params, file) exists in Python, so a film may need no click; not tried (no result to film).
- Save .casc: view Scene has save(); not tried before the crash. No .casc in the folder.

## What failed and why
- Cascadeur crashed on the quick rigging call. Its Python layer expects an AnimationInfo set-up that a bare FBX import does not give (Cascadeur's usual route: an imported character rigged in its rigging mode, or a scene made from its own template). The script layer raised, the native side carried on and fell over. Restarting Cascadeur was outside this brief.
- A possible next route, untested: create a new scene with SceneManager.create_application_scene, import the model first (import_model), rig with the template, then import_animation and unbake onto the rig. That would be a second try and needs Cascadeur started again.

## Cost
About 10 minutes of work (10:27 to 10:35 local) plus this write-up; about 15 minutes in all.

## Files
- F:/LedgerTools/tool-tests-2026-11/cascadeur-test4/ : run.py and runm.py (clients), measure_lib.py (the measurements), s01 to s10 scripts, before_raw.txt (the raw numbers). qrt_try1.txt was not written (the connection dropped).
- Cascadeur's log: %LOCALAPPDATA%/Nekki Limited/Cascadeur/logs/cascadeur_log.log, lines around 10:31:17 (the exception and backtrace).

## Try 2 (12 Nov, 10:33 to 10:38 local, Cascadeur restarted by the session)
### Cause of try 1's crash, and the documented order
- Backtrace at 10:31:17: the template call ran Cascadeur's own quick-rig Python. Its add_qrt_json wants exactly one AnimationInfo, and a scene made by FBX import has none. It raised, and the native side crashed afterwards in a session call. AnimationInfo is made by "rig mode on" (rig_mode/on.py).
- Documented order (help page "Quick Rigging Tool", read 2026-11-12; the shipped samples/casc_import_export.py and test/application_test_cases/rig_scenes_scenarios.py): rig mode on, quick rigging tool ("Add rig elements"), "Generate rig" (= rig mode off with generation), then animate. The Python API page for RiggingWindow returned 404 (not reached).

### What ran, all from Python through /run
1. New scene (SceneManager.create_application_scene), then FbxLoader.import_model only: 342 joints, 1 frame, no AnimationInfo.
2. rig_mode.on.run_raw(scene, colour): AnimationInfo 1.
3. RiggingWindow.create_from_qrt_by_fileName(Metahuman.qrigcasc), with auto posing set on: 63 rig elements, 44 proto points, 21 proto rigid bodies, 1 spline IK. No crash.
4. rig_mode.off.run(scene, True) (generate): 43 points, 69 boxes, 21 rigid bodies, 52 edges, centre of mass, RigInfo 1. Saved rigged_model.casc.
5. FbxLoader.import_animation: "animation pasted on frames from 0 to 99" (30 fps scene, 24 fps file, resampled as in try 1). On the rig, the numbers match the raw clip (table, column "On rig").
6. All 43 rig points selected and the whole range selected (pycsc select, select_frame_range), then call_action("View.FixFoot"): "Fulcrum motion cleaning completed from 0 to 99 frames". Saved after_fixfoot.casc.
7. call_action("AutoPhysicsTool.Switch Auto Physics"), then "Snap to Auto Physics": no error and no change in any number. Second try (rig points, boxes and rigid bodies selected, switch again, snap after 8 s): "No working Autophysics", so the second switch had turned it off. Two tries; set aside. Whether Auto Physics solved anything on the first switch is unmeasured; it moved no measured joint.
8. Auto posing (AutoPosingTool.*): not tried. It acts while a point is dragged, and there was nothing to drive without a click.
9. Saved after_fixfoot_autophysics.casc (the state after step 7, with Auto Physics off).
10. Film: RenderToFile.take_image returned, but no picture file appeared. play_to_video_file then crashed Cascadeur (10:37:45; the process is gone and the server refuses connections). Per the brief, the test stopped. No film.
11. FBX export: not tried (crash first). Export formats are still not measured. The licence is a Trial, which exports by its flags.

### Before and after against the bars (try 2, measured in Cascadeur, cm, frames 0 to 99)
| Bar | Raw clip (try 1) | On rig, before tools | After Fix Foot (+ Auto Physics, no change) | Bar met? |
|---|---|---|---|---|
| Foot slide 1 cm or less | L ankle 2.60, L ball 2.22; R ankle 0.54, R ball 0.82 | L 2.63 / 2.22; R 0.62 / 0.82 | L ankle 0.73, L ball 0.29; R ankle 0.60, R ball 0.33 | yes |
| Knees within 5 deg of straight (median / worst) | L 28.5 / 35.0; R 28.2 / 34.9 | L 28.2 / 34.8; R 28.3 / 34.9 | L 11.5 / 11.8; R 29.3 / 30.4 | no |
| Toes flat | L ball +1.8 to +2.9 cm, pitch 23.2 deg down; R ball -0.1 to +0.1, pitch 21.6 | L ball +1.8 to +2.8, pitch 23.6; R ball -0.2 to 0.0, pitch 22.2 | L ball -2.2 to -0.9 cm (into the floor), pitch 23.6 (worst 27.4); R ball -1.6 to -0.8, pitch 22.2 (worst 24.3) | no |
| Timing kept | yaw 0 to 51.6 deg peak at frame 23; return from about frame 78 to 11.4 deg at frame 98 | same to 0.03 deg | same to 0.03 deg every frame | yes |

Also measured: head drift 5.4 cm before, 5.15 cm after (not a bar). Pelvis dropped from 93.0 to 92.1 cm median.

### Reach from Python (plan item 6), after try 2
- From Python, no click: new scene, model import, animation import, rig mode on, quick rig from the MetaHuman template, rig generation, frame and object selection, Fix Foot, Auto Physics switch and snap (it runs, but no measured effect), .casc save, licence state (in the log).
- Crashes the app: render to video (play_to_video_file). take_image returned but wrote no file.
- Not tried: auto posing, FBX export, the side-by-side film.
- Film: "film needs a click" is unproven. The Python call exists but crashed the app; the film would need the render window by hand or another route.

### What failed and why (try 2)
- Knees and toes: Fix Foot pins the contact points and holds slide. It does not straighten the legs or level the feet. It pushed the balls of the feet 1 to 2 cm under the floor and straightened only the left knee, to 11.5 degrees. Auto Physics, switched on through its action, left every measured joint as it was.
- The render call crashed Cascadeur (second crash today), so no film and no FBX export. No third try (two tries means two).

### Cost (try 2)
About 25 minutes (10:33 to 10:38 work in Cascadeur, plus reading the backtrace, the help page and the shipped samples, and this write-up). Both tries: about 40 minutes.

### Files (try 2)
F:/LedgerTools/tool-tests-2026-11/cascadeur-test4/ : t2_01 to t2_11 scripts with t2_01.txt to t2_10.txt replies; rigged_model.casc (rigged, no animation), after_fixfoot.casc (the Fix Foot result), after_fixfoot_autophysics.casc (same, after the Auto Physics switches). Nothing enters the game.

## Correction (2026-11-12 11:46, the session)
The 'toes 22 to 24 deg down' rows measure the ankle-to-ball line, which slopes about 23 deg on a flat foot by anatomy (measured on the control solve, STOCK-CHAIR-RISE-2026-11-12.md). Toes are judged by ball height: before Fix Foot the left ball rode 1.8 to 2.8 cm up (lifted), after it 0.9 to 2.2 cm into the floor (a new fault). The verdict stands (knees not met; toes now into the floor).
