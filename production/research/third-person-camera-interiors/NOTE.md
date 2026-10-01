# The third-person camera in tight interiors: the method

Research, 1 October 2026, by a separate research helper (about thirty minutes of searching and reading, no Unreal or graphics card used). It answers the builder's question about Mickey's office (doorways 0.9 to 1.1 m, rooms 2 to 4 m deep): (a) at the front door the arm collapses to Tom's head and he vanishes; (b) by a wall or in a corner his back fills half the screen; (c) between counter and wall a near wall fills a third of the frame; changing the arm length (1.6, 2.0, 2.4 m) made no difference.

It builds on ../interior-blockout/DELIVERY.md section (b) (Max Payne room proportions, Gears door widths, Nesky's talk, the spring arm basics) and does not repeat it. Source tags: OPENED means the page itself was read; SNIPPET means only a search summary was seen.

---

## 1. What the observations already tell us (read before fixing anything)

How Unreal's spring arm works [S1]: every frame it sweeps one sphere (radius ProbeSize, default 12 cm, channel ECC_Camera) from the arm's origin (the component's location plus TargetOffset) to the arm's end (arm length back along the view, plus SocketOffset in view space). If the sphere hits anything, the camera is put at the hit point. The default BlendLocations simply snaps to the hit ("returns bHitSomething ? TraceHitLocation : DesiredArmLocation"). So once anything is hit, the arm length no longer matters, which is exactly what the 1.6/2.0/2.4 m trial showed.

Our setup (PROJECT, read 1 October from ue-probe SliceCharacter.cpp, CrimeProbe.cpp OfficeCameraTick and production/specs/mickeys-office.json):
- the boom hangs from the capsule's centre, about 0.88 m above the floor (hip height), with no TargetOffset;
- SocketOffset is 45 cm to the side and 55 cm up; indoors the arm eases to 2.0 m and the lift adds 45 cm, so the camera's end sits about 1.9 m above the floor before any pitch, and about 2.4 m when the player looks 15 degrees down;
- default probe (12 cm, ECC_Camera), no camera lag, no ease-out;
- Tom's mesh is switched off outright when the camera comes within HideWithinCm of his body line.

What that predicts (hypotheses, to confirm with step 0 below):
- (a) The sweep starts at hip height and climbs steeply to a point 1.9 to 2.4 m up and 45 cm to the side. A door head at about 2 m, or the jamb on the shoulder side, cuts that line within a metre of Tom; the camera lands beside his body and the hide rule blinks him out. Raising the camera indoors makes this worse, not better: the higher the end point, the sooner the line crosses the lintel and the ceiling.
- (b) The arm only ever pulls straight in along that line; it has no way to slide sideways along a wall, so a wall behind Tom puts the lens on his back.
- (c) The 45 cm shoulder offset is applied whatever the space; in a 1 m passage it pushes the camera next to one wall.

The method question, asked first: the spring arm is the bottom rung of what shipped games do. Studios treat this as a level-design-and-camera problem together; Nesky's second mistake is "designing levels and camera behaviors that don't match" [S13]. The spring arm alone is not the professional method for small rooms.

## 2. How studios do it, start to finish

1. Set camera metrics first, then size the spaces around them.
   - Full Spectrum Warrior's camera did not give good views in confined areas, so tight spaces were avoided by design [S11].
   - Hallways at least twice the player's width "will feel a bit narrow"; Unreal's generic door is 110 x 220 cm [S21].
   - Third-person rooms run larger than life and doors 1.5 to 2 times real width (Max Payne, Gears of War; see ../interior-blockout).
2. Camera collision is its own data, separate from what is drawn.
   - Martel (Game AI Pro, 2013): flags on objects so the camera ignores small posts, and foliage occludes the view without blocking the camera; draw every failed camera test on screen (red cylinders), because collision shapes drift from the visible meshes [S12].
   - Full Spectrum Warrior: poles do not collide with the camera [S11].
3. Collision response: a sphere, from a safe pivot, snapping in and easing out.
   - Lyra (Epic's UE5 sample) sweeps from a "safe location" on the character's capsule (the closest point to the aim line, clamped to the capsule's height), not from the actor's centre [S3].
   - The main ray snaps in at once ("don't interpolate toward this one, snap to it"); other rays ease the camera in over 0.1 s; clearing eases out over 0.15 s; the camera keeps 2 cm off the hit [S3].
   - Cinemachine's third-person rig goes origin, then shoulder, then hand, then camera, and has separate "damping into collision" and "damping from collision" [S9].
4. Predict, with feelers.
   - Full Spectrum Warrior (GDC 2004) cast several weighted rays from the look-at point; rays nearest the camera count 100 per cent [S11].
   - Lyra: seven feelers (centre ray with a 14 cm sphere; plus or minus 16 and 32 degrees of yaw; plus or minus 20 degrees of pitch), with separate weights for world and pawn hits [S3].
   - A Hat in Time's "camera whiskers" [S14] and Daedalic's line-of-sight modifier (Unreal Fest Europe 2018) rotate around obstacles before they block the view [S16].
5. Pull in, or swing round: it depends on who is moving the camera.
   - When the player turns the camera into a wall, keep his angle and only shorten the distance [S12].
   - When the camera follows on its own and the player backs into a wall, swing the camera's yaw smoothly along the wall's normal, which also stops it oscillating in corners [S12].
   - Never push the camera against the player's own turn (Nesky, mistakes 6 and 33) [S13].
   - Cinemachine names the three strategies: pull forward, preserve height, preserve distance [S10].
6. Fade, don't blink.
   - The character: Lyra raises OnCameraPenetratingTarget, "useful if you want to hide the target actor" [S3]. Full Spectrum Warrior made obstructing characters translucent [S11]. The usual Unreal technique is a masked material with a DitherTemporalAA fade by camera distance, with a ShadowPassSwitch so the shadow stays [S19].
   - Whatever stands between camera and character: The Witcher 3 and A Hat in Time dither nearby geometry [S14]. Unreal's Gameplay Cameras has an Occlusion Material node [S7]. Cinemachine has "transparent layers" [S10].
7. Mind the near plane: never let it cut the avatar (Nesky 12) [S13]. Martel padded the camera with a collision size, and says in retrospect simply raising the near clip "would have been far simpler" [S12].
8. Per-place camera settings, blended.
   - Uncharted 3: several player cameras (follow, aim, melee, cover) that designers tune, with priority schemes and fades between them [S15].
   - Martel: activation rules plus priorities, and triggers that level designers place [S12].
   - Daedalic: camera modification volumes [S16].
   - The Witcher 3 brings the camera closer indoors [S17], and Red Dead Redemption 2's indoor camera differs from its outdoor one (player reports, ../interior-blockout S35).
   - Nesky warns against applying a hint just after the player has turned the camera, and against rapid FOV shifts (mistakes 34 and 41) [S13].
9. Field of view: Daedalic varies FOV and distance with pitch [S16]; Nesky lists too small a FOV as a mistake [S13]. No source found that widens the FOV for interiors as standard practice; treat it as a last, judged trial. MetaHuman faces would stretch at wide angles close up (my inference).
10. Tools first: a debug display of the camera's state and its collision tests, and a free debug camera to watch the gameplay camera from outside [S12].

## 3. What Unreal 5.8 offers, and what each costs in our C++ project

| Behaviour | Unreal feature | Since | Cost for us |
|---|---|---|---|
| Pivot height | USpringArmComponent TargetOffset (world space, start of arm); SocketOffset (end) [S1] | UE4 | Two numbers |
| Probe size, channel | ProbeSize, ProbeChannel (ECC_Camera) [S1] | UE4 | Two numbers |
| Snap in, ease out | Override the protected virtual BlendLocations in a USpringArmComponent subclass [S1]; IsCollisionFixApplied() and GetUnfixedCameraPosition() for fade logic [S1] | UE4 | ~40 lines of C++ |
| Shoulder that shrinks or swaps | No built-in; a second sweep from pivot to shoulder point inside the subclass (Cinemachine's origin-shoulder-hand chain is the model [S9]) | n/a | ~60 lines |
| Camera-only collision | Per-component response to ECC_Camera (Ignore for props, door leaves, chairs); simple blocking boxes that block only Camera [S25] | UE4 | Data, no code |
| Feelers, safe pivot, penetration callback | Lyra's ULyraCameraMode_ThirdPerson (PreventCameraPenetration, FLyraPenetrationAvoidanceFeeler, ILyraCameraAssistInterface) [S3] | Lyra for UE 5.0 on | Port ~300 lines, or write ours from the method; licence check, see 5 |
| Per-room settings | Our own OfficeCameraTick rectangle test extended per room; or APlayerCameraManager plus UCameraModifier; Daedalic's MIT sample shows volumes and modifiers [S16] | UE4 | Small; data in mickeys-office.json |
| Character fade | Masked material + DitherTemporalAA + ShadowPassSwitch [S19]; or an opacity swap like the community CameraAntiBlockComponent (UE 5.1.1) [S20] | UE4 | Moderate: MetaHumans carry many material slots (face, body, groom, clothes) and each needs the parameter |
| Occluder fade | Gameplay Cameras' Occlusion Material node [S7], or our own trace plus a material parameter | 5.5 plugin | Moderate |
| Whole camera system | Gameplay Cameras plugin: Camera Rig assets, Boom Arm, Collision Push ("pushes the camera towards a 'safe position'"), Occlusion Material, directors (Blueprint, Single, State Tree) [S5, S7, S8] | 5.5, Experimental | High, and risky: see 5 |
| Near plane | Project Settings, Near Clip Plane (default 10 cm; my memory, not checked this session) | UE4 | One number; affects the whole game |

Gameplay Cameras in detail:
- It was introduced as Experimental in 5.5, and Epic's 5.8 page still says Experimental [S5, S6].
- Its author and only developer was laid off from Epic in March 2026. He expects UE6 to keep the runtime but probably not the data-driven editors, and advises asking Epic before committing to it [S6].
- Users report that Collision Push must run after Boom Arm, and that the component must be activated for the player [S7].
- Not recommended for LEDGER now.

## 4. Recommended order of things to try

Each step is cheap and judged through the game's own camera at the three failing spots (the front door walking in and standing just inside; Tom backed into the office's tightest corner; the counter passage), plus one conversation spot. Stop at the first step that passes all four.

0. Find out what the probe hits (an hour).
   - Draw the sweep, and log the hit component and its distance, at each failing spot.
   - Pass: for (a), (b) and (c) we can name the surface: lintel, jamb, ceiling, counter or wall. If it is the ceiling or a lintel, step 1 is the fix.
1. Move the pivot up, and stop lifting indoors.
   - TargetOffset about +60 cm (sweep from upper chest or neck, about 1.5 m above the floor) with SocketOffset Z cut to match; indoor lift 0; probe 12 to 15 cm.
   - Pass: walking through the front door 10 times, Tom never hidden; the camera's end never above about 1.9 m in the office.
2. Make the shoulder offset collide first.
   - In a spring arm subclass: sweep pivot to shoulder point; shorten the 45 cm to whatever is free; then sweep from there back to the camera. Optionally swap to the freer side, never while the player is turning.
   - Pass: in the counter passage the nearest wall covers less than about a sixth of the frame; door (a) still passes.
3. Snap in, ease out.
   - Override BlendLocations: in at once, out over about 0.3 to 0.5 s. This is a starting value: Lyra uses 0.15 s; tune by eye.
   - Pass: no pop or flicker when Tom walks past the door frame and furniture; no wall seen through.
4. Clean the camera's collision.
   - Door leaves, chairs, coat stand, bins and small counter parts ignore ECC_Camera; walls and ceilings keep it.
   - Pass: in the debug log from step 0 the probe hits only walls, ceilings and the counter body.
5. Per-room settings in mickeys-office.json: arm, shoulder, pivot height and pitch limits for each room, blended over about 0.5 s on entry and held off while the player turns.
   - Pass: one frame per room at its tightest spot shows Tom whole and the person he faces.
6. Fade Tom instead of switching him off.
   - About 0.15 s of dither between roughly 60 and 30 cm, with his shadow kept.
   - Pass: no pop in (b). Cost: MetaHuman material work, so do this only if (b) still bites after steps 1 to 3.
7. Only if corners still fail: swing the yaw along the wall's normal when Tom backs into a wall and the player is not steering the camera [S12], or Lyra-style feelers [S3].
   - Pass: the corner test from (b) shows his head and shoulders, not just his back.
8. Last: one FOV trial (a few degrees wider indoors, blended slowly).
   - Pass: more of the room in frame at the tightest spots, while the approved faces in conversation frames do not look stretched.

Not recommended:
- adopting the Gameplay Cameras plugin (see 3);
- fixed security-camera-style shots for the office (a change of genre feel; scope).

## 5. Money, licences, scope (for Jafar only if acted on)

- Licence: Lyra's camera code. Forum answers say Lyra code may be used in any Unreal project under the UE EULA [S23, SNIPPET]; it is not confirmed here against our allowlist. Writing our own from the method above avoids the question.
- Licence: Daedalic's sample code is MIT; its content is under the UE EULA [S16]. Check MIT against the allowlist before copying any of it.
- Money: paid camera plugins on Fab (for example Aurora Devs' Ultimate Gameplay Camera) exist. They are not needed and are not recommended.
- Scope and look: if steps 1 to 5 are not enough, the shipped answer is wider doors (1.5 to 2 times real) and roomier rooms. That changes how a period minicab office looks against the photographs, so it goes to Jafar as a whole-frame look decision, not something to change quietly.

## Gaps

- Not reached: a primary source for Red Dead Redemption 2's or Hitman's interior camera rules; Naughty Dog's or Santa Monica's camera collision details beyond talk abstracts; the Unreal tech blog article "Six Ingredients" itself (403; known only through Daedalic's README and a search summary).
- The Gameplay Cameras node reference page did not render; node behaviour comes from a forum thread and a search summary.
- The near-clip default and the exact heights in our office (ceiling, door head) were not checked; step 0 settles what matters.

## Sources

1. [S1] "USpringArmComponent", Unreal Engine 5.8 C++ API, Epic Games, undated. https://dev.epicgames.com/documentation/unreal-engine/API/Runtime/Engine/USpringArmComponent. OPENED.
2. [S2] "Using Spring Arm Components", UE 4.27 docs, Epic Games, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/using-spring-arm-components?application_version=4.27. SNIPPET.
3. [S3] Lyra Starter Game source (Epic Games), LyraCameraMode_ThirdPerson.h/.cpp, LyraPenetrationAvoidanceFeeler.h, LyraCameraAssistInterface.h, read from a public GitHub mirror, undated. https://github.com/LeNidViolet/Lyra/tree/main/Source/LyraGame/Camera. OPENED. Official listing: https://www.fab.com/listings/93faede1-4434-47c0-85f1-bf27c0820ad0 (undated, SNIPPET).
4. [S5] "Gameplay Camera System Overview", UE 5.8 docs, Epic Games, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/gameplay-camera-system-overview. OPENED.
5. [S6] Ludovic Chabant, "UE5 Gameplay Cameras: Coda?", 30 March 2026. https://ludovic.chabant.com/blog/2026/03/30/ue5-gameplay-cameras-coda/. OPENED. Series index, 20 January 2025 to 30 March 2026: https://ludovic.chabant.com/blog/category/programming/game-development/unreal-engine/. OPENED.
6. [S7] "Collision Push node in Gameplay Camera System not working", Epic forums, posts of 5 and 28 January 2026. https://forums.unrealengine.com/t/collision-push-node-in-gameplay-camera-system-not-working/2689515. OPENED.
7. [S8] "Collision" nodes, GameplayCameras API, Epic Games, undated. https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Plugins/GameplayCameras/Nodes/Collision. SNIPPET (the page did not render).
8. [S9] "Third Person Follow", Unity Cinemachine 3.0 manual, 2023. https://docs.unity3d.com/Packages/com.unity.cinemachine@3.0/manual/CinemachineThirdPersonFollow.html. OPENED.
9. [S10] "Cinemachine Deoccluder", Unity Cinemachine 3.0 manual, 2023. https://docs.unity3d.com/Packages/com.unity.cinemachine@3.0/manual/CinemachineDeoccluder.html. OPENED.
10. [S11] John Giors, "The Full Spectrum Warrior Camera System", Game Developer (GDC 2004 paper), 25 March 2004. https://www.gamedeveloper.com/design/the-i-full-spectrum-warrior-i-camera-system ; slides https://media.gdcvault.com/gdc04/slides/full_spectrum_warrior.pdf. OPENED (article).
11. [S12] Eric Martel, "Tips and Tricks for a Robust Third-Person Camera System", Game AI Pro, chapter 47, CRC Press, 2013. https://www.gameaipro.com/GameAIPro/GameAIPro_Chapter47_Tips_and_Tricks_for_a_Robust_Third-Person_Camera_System.pdf. OPENED (full text).
12. [S13] John Nesky, "50 Game Camera Mistakes", GDC 2014. https://gdcvault.com/play/1020460/50-Camera ; list as notes, undated: https://shermanrose.uk/knowledge/programming/games/50-game-camera-mistakes/. OPENED (notes).
13. [S14] Andreas Buehler, "Third Person Camera View in Games: a record of the most common problems...", Game Developer, 11 November 2019 (cites Mashable, 2017, for A Hat in Time). https://www.gamedeveloper.com/design/third-person-camera-view-in-games-a-record-of-the-most-common-problems-in-modern-games-solutions-taken-from-new-and-retro-games. OPENED.
14. [S15] Travis McIntosh, "The Cameras of Uncharted 3", GDC 2012, session abstract. https://www.gdcvault.com/play/1015514/The-Cameras-of-Uncharted. SNIPPET.
15. [S16] Daedalic Entertainment, third-person-camera sample for "Six Ingredients for a Dynamic Third-Person Camera", Unreal Fest Europe 2018, GitHub README, undated. https://github.com/DaedalicEntertainment/third-person-camera. OPENED. Unreal tech blog article: https://www.unrealengine.com/en-US/tech-blog/six-ingredients-for-a-dynamic-third-person-camera (403, SNIPPET).
16. [S17] Francesco De Meo, "The Witcher 3 New Mod Improves Camera Inside Buildings", Wccftech, 16 August 2019. https://wccftech.com/the-witcher-3-mod-improves-camera/. OPENED.
17. [S19] Chris Murphy (@HighlySpammable), DitherTemporalAA near-camera fade tip, X, 10 April 2020. https://x.com/highlyspammable/status/1248572319343063041. SNIPPET.
18. [S20] Dimmak23, "UE5 CameraAntiBlockComponent" (UE 5.1.1), GitHub, undated. https://github.com/Dimmak23/UE5_CameraAntiBlockComponent. SNIPPET.
19. [S21] "Metrics", The Level Design Book, undated. https://book.leveldesignbook.com/process/blockout/metrics. OPENED.
20. [S23] "Lyra to use as a basis", Epic forums, undated. https://forums.unrealengine.com/t/lyra-to-use-as-a-basis/1312370. SNIPPET.
21. [S25] "Collision Response Reference", UE 4.26 docs, Epic Games, undated. https://docs.unrealengine.com/4.26/en-US/InteractiveExperiences/Physics/Collision/Reference. SNIPPET.
