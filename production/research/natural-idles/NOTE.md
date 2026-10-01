# Natural idles: how people stand, talk and walk without looking stiff

Research, 1 October 2026, by a separate research helper (about thirty minutes), for NOW.md item 2b: "People in natural idle poses and movement from Epic's free animation sample (they stand stiffly, arms held out)." It builds on production/research/townspeople-animation (30 September), which covered the whole townspeople pipeline, retargeting in 5.8, foot sliding and cost; this note does not repeat that. Nothing was run in Unreal. Files on this PC were only read: the game's code, and the engine's own plugin folders and headers.

Each source is marked OPENED (page read) or SNIPPET (search summary only).

## 1. The method, start to finish, as studios do it

1. **A move list for each kind of person.** For standing people it holds: a base idle per stance, idle "breaks" (fidgets), weight shifts, breathing, looking about, gestures while talking, a listener's loop, and the moves into and out of walking. The Witcher 3 kept a pool of 35 idle variations for each skeleton type (male, female, dwarf), plus sitting variants. It had about 2,400 dialogue animations, reused across characters as additive gestures with bone masks (Game Anim, 2016).
2. **Layers at runtime**, from the bottom up:
   - a base idle loop of about 8 to 12 seconds that includes a weight shift;
   - breaks every 30 to 60 seconds (vendor guide, 2026);
   - an additive breathing layer of 1 to 2 cm, at about 15 to 20 breaths a minute;
   - an additive head and eye look-at, laid over the idle, never replacing it;
   - upper-body gestures through a slot and a per-bone blend, so they can play over a walk;
   - the face on its own layer.
3. **Talking.** The Witcher 3 placed its first pass of idles and gestures automatically from the voice recording's accents, then animators fixed what mattered (Game Anim, 2016). Larger budgets capture the whole body for every line: Baldur's Gate 3 did, with 248 actors (PC Gamer, SNIPPET). A speaker loop and a listener loop work as a matched pair (vendor guide, 2026).
4. **No two people in step.** Each person gets:
   - a random start point in the loop (we do this already);
   - a play rate between 0.9 and 1.1;
   - slightly different blend times;
   - a different base idle from the person beside them;
   - a mirrored copy of a clip, which counts as another variation.
5. **Walking: state machine or motion matching.** Motion matching searches a large captured database every few frames (The Last of Us Part II used it mainly for locomotion; GASP is Epic's example). It suits a player character who must respond at once. People walking set routes at set hours need only this:
   - start, loop and stop clips;
   - the body moved at the clip's own speed, so the feet do not slide;
   - a blend into idle.
   The house rule says take the cheaper of two fine ways, so that is the choice. GASP's own idle breaks come through a state machine and a Chooser table (CHT_AnimationsForStateMachine), not through motion matching (Epic forum, 2025).
6. **Judged in the game**, through the game's camera, against reference footage.

**How many variations a small street needs.** We have three cast members and a handful of townspeople, all seen close up. The rules of thumb are:
- at least 4 base idles for each sex, because fewer than 4 shows repetition (vendor guide: 5 to 8 per archetype, little gain above 12);
- 8 to 12 breaks shared between them;
- one breathing additive;
- 2 speaker loops and 2 listener loops;
- 6 to 10 additive talk gestures (a beat, an open palm, a point, a shrug, a nod).

That makes about 15 to 25 clips for each sex. No two neighbours share a base idle. The Witcher 3's 35 per type served hundreds of people, so it is the ceiling, not the target.

## 2. What Epic's free animation actually is in 2026

**Game Animation Sample Project ("GASP").**
- Fab listing (OPENED 1 Oct 2026): free, published 11 June 2024, last updated 17 August 2026, for Unreal 5.4 to 5.8. It arrives as a complete project. **"License terms: Standard License"**, and "Allows usage with AI: No".
- Contents: "500+" game-ready animations at launch.
  - The 5.7 update (Epic, 3 Dec 2025, OPENED) added a new locomotion dataset with "400 new animations", a Smart Object level, and "basic NPC setups" in which people sit on benches.
  - The 5.8 update (Epic, 12 Aug 2026, OPENED) added: multi-character motion matching (Pose Search Interaction assets); a ragdoll pawn; an Experimental additive Look-At solver in Control Rig, "nondestructive" over existing animation, with samples of look-at over locomotion and over "acting gestures"; and benches the player can use.
- A third party's repackaging gives these counts (OPENED; its counts, not Epic's): about 1,800 in all, including 45 idles, 446 walks, 33 poses (leans, head turns), 11 look-at clips, 42 head-only aim clips and 62 interaction clips.
- Skeleton: everything is authored on the UEFN (Fortnite) mannequin. The MetaHuman example uses Epic's runtime retarget Animation Blueprint, ABP_GenericRetarget, with a tag such as RTG_UEFN_to_Metahuman_nrw on the body. It can switch between all MetaHuman body types and between masculine and feminine meshes (Epic docs, OPENED).
- **Women's moves: unconfirmed.** No Epic page says GASP has a separately performed feminine set. Swapping to a feminine mesh does not make the movement feminine. Check this once it is downloaded.

**Already on this PC, with no download: the MetaHuman plugin's own animations** (read from the UE 5.8 install, engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Animation):
- *UEFNAnimPreset/Locomotion*:
  - one standing idle, AS_MH_Neutral_Stand_Idle_Loop;
  - walk loops forward, back and to each side;
  - walk starts and stops for each direction and foot;
  - the same set for running.

  These 31 assets are already on metahuman_base_skel, the skeleton our cast uses. They play without retargeting, and the starts and stops are what our walkers lack.
- *TemplateAnimations*:
  - one body idle and one face idle, under **Technical_Loops** (mhc_mh001_fmn_b_idle and mhc_mh001_fmn_f_idle);
  - two range-of-motion clips (BodyROM and FaceROM);
  - facial expression loops and facial poses.

  "fmn" appears to be the female, medium-height, normal-weight template body. Epic says these clips "can be retargeted to your assembled MetaHuman character", using RTG_MH_IKRig for bodies (Epic docs, OPENED).

**Licences, stated plainly:**
- **GASP**: the Fab listing names the Fab Standard License. Its summary allows commercial use, "usage is not limited to Unreal Engine", and no standalone resale. Its "NoAI" flag forbids using the content in datasets for, the making of, or the training of generative AI. Either way it is on the allowlist: SHIP-SAFE 2 (Fab purchases under the Fab Standard License, at no cost) and SHIP-SAFE 8 (Epic's Unreal-only animation, ruled 30 September). Keep to the stricter reading of 8: inside the game only. Our AI tester plays the game and trains nothing, so the NoAI flag does not touch it. Name GASP in THIRD-PARTY.md when it is downloaded.
- **The MetaHuman plugin's animations**: these ship with the engine and are used under Epic's engine and MetaHuman terms, inside Unreal. They are allowed under SHIP-SAFE 3 and 8.
- **Do not use the third-party "GASP retargeted to Manny" repackaging** (Kingboars, Fab). It redistributes Epic's animations and says it is "not affiliated" with Epic. Take GASP from Epic's own listing.
- **Paid Fab packs** (for example "MC Idles", 238 idles including smoking and weight shifts, from the 30 September note): Fab Standard License, so allowed, but buying one is a **money decision for Jafar**.
- **Mixamo**: allowed with Jafar's account and token (D46). It is a fallback for women's idles if GASP has none.

**Needs the owner to sign in.** Before anyone can download GASP, someone signed in as Jafar must press "Add to My Library" on its Fab page. He can do it from his phone, free. Claude must not sign in (memory note "Fab needs Jafar signed in"). The project is then created through the Epic Games Launcher on this PC, which must also be signed in as him. Create it on F:, since new scratch goes to F:. Its size was not found, so enter the folder in production/large-files.json. **The MetaHuman plugin's own animations need no sign-in.**

## 3. Why people stand "with their arms held out"

Common causes in Unreal, then the suspects in our own code.

1. **Nothing is animating the mesh, so it shows its reference pose.** A MetaHuman's reference pose is an A-pose, arms about 45 degrees from the body; a Mixamo body's is a T-pose. Causes:
   - a skeleton mismatch;
   - an animation that failed to load in the packaged game because it was never cooked;
   - an anim instance that was never initialised;
   - a part such as a garment that does not follow the body's pose;
   - animation ticking turned off when off screen or far away.
2. **A retarget from a T-pose source onto the A-pose MetaHuman without matched retarget poses.** The arms come out about 45 degrees too high or go through the body. The fix is the IK Retargeter's Auto Align of the retarget poses (forum and vendor, SNIPPET; Epic's docs on matched retarget poses, in the 30 September note).
3. **A clip made for one body played unretargeted on another.** Every MetaHuman shares the skeleton, so it plays, but the rotations are the template's. On a different build the hands float off the hips or sink into them. This is why Epic says to retarget the Creator's clips to each assembled character.
4. **A technical, range-of-motion or preview loop used as a gameplay idle.** These are made to show how the mesh bends, not how a person stands.
5. **An additive clip played as a full pose, or applied twice.**
6. **Nodes that pull bones back toward their rest rotation.** These stiffen whatever they touch.

**Suspects in LEDGER, most likely first. All are unverified, because no frame was rendered.**
- **(a)** The three cast members all play the **same** idle: Epic's *Technical_Loops* preview idle from the female template, unretargeted, on two men and a woman. Only the start point differs (CrimeProbe.cpp DressBody; MetaHumanPortrait.cpp). This alone explains "stiff" and identical behaviour, and possibly the arms through cause 3 or 4. Check one frame of Ron through the game camera.
- **(b)** The head and two neck bones are held 70% toward their bind rotation, replacing whatever the idle does (PersonAnim.h, CalmAlpha 0.7), before the look is applied. The upper body stays lively while the head and neck stay still, which reads as rigid. Epic's 5.8 answer is an additive look-at over the idle.
- **(c)** The remaining Mixamo stand-ins in street-people.json play single Mixamo clips with no breaks.
- **What to check:**
  - the log line "LedgerCast: X has N part(s) that can speak": zero means cause 1;
  - the clips' cook path: DefaultGame.ini already cooks the Technical_Loops/Idle folder and /Game/Ledger, and anything new must be cooked too;
  - which people Jafar meant. Ask the frame, not him.

## 4. Using them on MetaHumans in UE 5.8, driven from C++

**Retarget offline, not at runtime.**
- Run GASP's own RTG_UEFN_to_Metahuman_* retargeters, or a saved retargeter built on RTG_MH_IKRig, in a batch over the chosen clips. Do it once for each body: Ron (MH_RoccoP2), Darren (MH_SamC5), Sheila (MH_LenaS4), and later the slim, average and heavy builds.
- Write the results into /Game/Ledger/Anim/... so they are cooked.
- tools/ue/retarget_metahuman_idle.py already does this for one clip.
- Use 5.8's Foot Definition and speed planting on walks (30 September note).
- Runtime retargeting (FAnimNode_RetargetPoseFromMesh, in the IKRig plugin) would cost a second pose evaluation per person every frame.
- Retargeted clips are on metahuman_base_skel, so the existing skeleton check in DressBody passes.

**The graph, in the native ULedgerPersonAnim.** It already supplies its own nodes through GetCustomRootNode. Every node below exists in the 5.8 headers on this PC:
- **Idle set**: FAnimNode_RandomPlayer (AnimGraphRuntime). Fill its Entries from C++ before the proxy's Initialize. Each entry has a sequence, ChanceToPlay, a minimum and maximum loop count, a play-rate range and a BlendIn; bShuffleMode avoids repeats. Use a base idle with a high chance and two to six loops, and breaks with a low chance and one loop each. One set per person; neighbours get different sets.
- **Transitions**: FAnimNode_Inertialization or FAnimNode_DeadBlending (Engine). These give smooth idle-to-walk and break changes without long cross-fades.
- **Walking**:
  - play the start clip, then the loop, then a stop clip timed by its own travel distance;
  - move the actor at the clip's measured root speed, not a fixed 1.2 m/s (the slide the 30 September note found);
  - the plugin's AS_MH_Neutral_Walk_* clips cover this today.
  - FAnimNode_BlendListByInt picks the state.
  - FAnimNode_MotionMatching and FAnimNode_BlendStack exist (PoseSearch and BlendStack plugins) but need editor-made databases and cost more: not now.
- **Gestures and scripted moments**: FAnimNode_Slot plus FAnimNode_LayeredBoneBlend from the spine up, played as montages from C++. Use this for talk gestures, checking a watch or lighting a cigarette, and for reactions. Test early that montages run through a native custom root.
- **Additives**: FAnimNode_ApplyAdditive for breathing and for beat gestures. The game already measures loudness (SpeakTick), so trigger a beat gesture on loudness peaks, as The Witcher 3 placed its gestures on the voice's accents. The listener nods on the speaker's pauses.
- **Look-at**: drop CalmAlpha to about 0.2 to 0.3, or remove it, and spread the turn over the spine, neck and head. Better: port GASP 5.8's additive Look-At Control Rig through the ControlRig node.
- The face keeps its own idle and the made mouths; nothing changes there.

## 5. How to judge it against Kingdom Come: Deliverance II

KCD2 is a 2025 benchmark built on extensive motion capture. For the finale alone Warhorse recorded 303 takes for 201 characters (GamesRadar and Gamereactor, SNIPPET). Reviewers still call its in-engine dialogue "a little lifeless at times" (SNIPPET). The bar for us is "not obviously game-like", not cinematic.

Film two 20-second clips through our game camera at play distance: one of a person standing while the player walks past, one of a conversation. Set them beside KCD2 footage at the same distance and check:
1. Do any two people move in step?
2. Is there a weight shift within 10 seconds?
3. Do the arms hang, fold or sit in pockets, never in an A-pose?
4. Does the head follow the player smoothly, with the body still alive under it?
5. Is there a break within 30 to 60 seconds?
6. Do the hands move on stressed words, and does the listener react?
7. Do the feet slide at starts and stops?
8. Does anyone snap round when turning?

Items 1, 2, 5 and 7 the AI tester can measure: bone phases between people, a pelvis sway, the number of different clips played per minute, and foot speed while a foot is down. The gate's blind reviewer judges the rest. Under the house rule, one fully animated sample person is approved by Jafar in the assembled game before the set is copied to anyone else.

## 6. What to do, in order

1. Render one frame of each person through the game camera and read the log, to find which cause from section 3 it is. Then retarget the plugin's MetaHuman locomotion (idle, walk starts, loops and stops) to each cast body and wire starts and stops. This needs no download and no sign-in.
2. **Jafar: add GASP to his Fab library**, one free tap on his phone. Create the project on F:, then batch-retarget about 15 to 25 clips per sex (idles, breaks, look-around poses, talk gestures) onto each body.
3. Build the C++ graph from section 4 for one person (Ron): the idle set, breaks, breathing, the additive look-at, talk gestures on loudness peaks, and walking with starts and stops. Put that person through the gate, then on Jafar's page in the game.
4. Only then copy it to the others, with no two neighbours sharing a base idle.
5. If GASP has no women's idles, use Mixamo women's idles (allowed). A paid pack would be Jafar's decision.

## Sources

Epic and Fab:
- Game Animation Sample (Fab listing): Epic Games; published 11 Jun 2024, last updated 17 Aug 2026; https://www.fab.com/listings/880e319a-a59e-4ed2-b268-b32dac7fa016 (OPENED 1 Oct 2026)
- Fab Standard License summary and Fab EULA: Epic Games; last updated 1 Oct 2024; https://www.fab.com/eula (OPENED)
- Download the latest Game Animation Sample Project, now updated for UE 5.8: Epic tech blog; 12 Aug 2026; https://www.unrealengine.com/tech-blog/download-the-latest-game-animation-sample-project-now-updated-for-ue-5-8 (OPENED)
- Explore the updates to the Game Animation Sample Project in UE 5.7: Epic tech blog; 3 Dec 2025; https://www.unrealengine.com/tech-blog/explore-the-updates-to-the-game-animation-sample-project-in-ue-5-7 (OPENED)
- Game Animation Sample Project in Unreal Engine: Epic docs, 5.8; undated; https://dev.epicgames.com/documentation/unreal-engine/game-animation-sample-project-in-unreal-engine (OPENED)
- Adding a MetaHuman to the Game Animation Sample Project: Epic docs, 5.8; undated; https://dev.epicgames.com/documentation/en-us/unreal-engine/adding-a-metahuman-to-the-game-animation-sample-project-in-unreal-engine (OPENED)
- Retarget MetaHuman Creator Animation: Epic docs; undated; https://dev.epicgames.com/documentation/metahuman/retarget-metahuman-creator-animation?lang=en-US (OPENED)
- Where can I change GASP idle_break animations: Epic forum; 17 and 19 Apr 2025; https://forums.unrealengine.com/t/where-can-i-change-or-replace-gasp-experimental-state-mechine-idle-break-animations/2461321 (OPENED)
- Game Animation Sample Animations Retargeted to UE5 Mannequin (third party, Kingboars): published 18 Sep 2025, updated 16 Aug 2026; https://www.fab.com/listings/259f8545-f820-47b3-8fc1-e8ec5458214d (OPENED; counts only, do not use)

Engine files read on this PC (UE 5.8 install), 1 Oct 2026:
- Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Optional/Animation: 31 UEFNAnimPreset assets and 33 TemplateAnimations assets, with their skeleton paths read from the files
- The node headers: AnimNode_RandomPlayer.h, AnimNode_Slot.h, AnimNode_LayeredBoneBlend.h, AnimNode_ApplyAdditive.h, AnimNode_BlendListByInt.h (AnimGraphRuntime); AnimNode_Inertialization.h, AnimNode_DeadBlending.h (Engine); AnimNode_RetargetPoseFromMesh.h (IKRig); AnimNode_MotionMatching.h (PoseSearch); AnimNode_BlendStack.h (BlendStack)

Methods and other games:
- Random Sequence Player node reference: Aaron Kemner; undated; https://www.aaronkemner.com/animnode-reference/randomplayer/ (SNIPPET)
- Cinematic Dialogue in The Witcher 3: Game Anim; 23 Mar 2016; https://www.gameanim.com/2016/03/23/cinematic-dialogue-witcher-3/ (OPENED)
- Behind the Scenes of Cinematic Dialogues in The Witcher 3: Piotr Tomsinski, GDC; 2016; https://www.gdcvault.com/play/1022988/Behind-the-Scenes-of-Cinematic (SNIPPET)
- Motion Matching in The Last of Us Part II: Michal Mach and Maks Zhuravlov, GDC; July 2021; https://gdcvault.com/play/1027118/Motion-Matching-in-The-Last (SNIPPET)
- Learn about the character technology of The Last of Us Part II's NPCs: Game Developer; 20 Apr 2021; https://www.gamedeveloper.com/design/learn-about-the-character-technology-of-i-the-last-of-us-part-ii-s-i-npcs-at-gdc-2021 (OPENED)
- Baldur's Gate 3 used motion capture from 248 actors: PC Gamer; 2023; https://www.pcgamer.com/baldurs-gate-3-used-motion-capture-from-248-actors-to-bring-its-npcs-to-life-youre-not-only-hearing-the-actors-voices-but-youre-also-seeing-their-physical-performances/ (SNIPPET)
- Idle Animation for Games: Design Guide: MoCap Online (vendor), Kyle Jirik; 11 Apr 2026; https://mocaponline.com/blogs/mocap-news/idle-animation-game-dev-guide (OPENED; a vendor's rules of thumb)
- Crowd and NPC Animation Guide: MoCap Online (vendor); 17 Mar 2026; https://mocaponline.com/blogs/mocap-news/crowd-npc-animation-guide (OPENED; a vendor's rules of thumb)
- T-Pose Fix in UE5 and Unity: MoCap Online (vendor); undated; https://mocaponline.com/blogs/mocap-news/tpose-animation-retargeting-fix (SNIPPET)
- Matching a T-pose skeleton to UE5's A-pose when retargeting: Epic forum; 2022 onward; https://forums.unrealengine.com/t/is-there-a-quick-way-to-perfectly-match-t-pose-skeleton-to-ue5s-standard-a-pose-when-retargeting/569850 (SNIPPET)
- KCD2 developers used a real horse in motion capture: GamesRadar; 2025; https://www.gamesradar.com/games/rpg/if-you-liked-red-dead-redemption-2s-ultra-realistic-horses-kingdom-come-deliverance-2-devs-also-used-a-real-horse-in-the-motion-capture-studio/ (SNIPPET)
- Kingdom Come: Deliverance 2 review: GamesRadar; Feb 2025; https://www.gamesradar.com/games/rpg/kingdom-come-deliverance-2-review-even-if-some-friction-can-lead-to-frustration-its-realization-of-medieval-life-remains-utterly-absorbing/ (SNIPPET)
- KCD2's cinematic director on cutscenes: Gamereactor; 2025; https://www.gamereactor.eu/kingdom-come-deliverance-ii-cinematic-director-explains-how-to-make-cutscenes-unskippable-1649193/ (SNIPPET)

## Not verified

- What the Technical_Loops idle actually looks like on Ron and Darren: no frame was rendered.
- Whether GASP holds feminine idles.
- GASP's download size.
- Whether montages play through a native custom root node.
- KCD2's own animation counts: none published that I found.
