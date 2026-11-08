# People in motion: field scan (8 Nov 2026)

One-page scan before a method is chosen. Nothing decided. Every link read 8 Nov 2026 unless marked. Own notes cited, not repeated: [ALIVE-PROPOSAL](../people-alive/ALIVE-PROPOSAL-2026-11-07.md), [natural-idles](../natural-idles/NOTE.md), [markerless-mocap](../markerless-mocap/SUMMARY.md) and RECHECK.md, [townspeople-animation](../townspeople-animation/SUMMARY.md), [Study 07](../aaa-reference/studies/07-animation.md).

## 1. AAA practice
- Motion matching: Clavet, Ubisoft, GDC 2016, For Honor; the session summary says small markup on long mocap clips, frames picked at run time by current pose and wanted path ([GDC Vault](https://www.gdcvault.com/play/1022985/Motion-Matching-and-The-Road)). Naughty Dog, GDC 2021, "Motion Matching in The Last of Us Part II" (Mach, Zhuravlov): summary mentions "initial joy, later frustration and ultimate fear" ([GDC Vault](https://gdcvault.com/play/1027118/Motion-Matching-in-The-Last)).
- Both talks: only the summary was readable (members-only body). The talks themselves are unreached; claims on weight shift, look-at, foot placement and layered additives are not confirmed here beyond Study 07's notes (unverified from primary).
- Search hit, not read: Clavet's later ragdoll motion matching talk ([GDC Vault 1026712](https://gdcvault.com/play/1026712/contactUs)); unverified.

## 2. Epic, UE 5.8 docs (pages read in full)
- [Motion Matching](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-matching-in-unreal-engine): Pose Search schema and databases; channels incl. trajectory, pose, velocity, phase; brute force and PCA-KD-tree search; blend stack, inertial blend, notifies. Crashing Legs and Permutation Time channels experimental. The page gives no 5.6 or 5.7 change list.
- [Game Animation Sample](https://dev.epicgames.com/documentation/en-us/unreal-engine/game-animation-sample-project-in-unreal-engine): choosers filter databases; orientation warping, Leg IK, additive lean, simple aim offset; Offset Root Bone node experimental. Licence not on the page (Fab listing unread).
- [Mover](https://dev.epicgames.com/documentation/en-us/unreal-engine/mover-in-unreal-engine): experimental; CMC stays supported. [Motion Warping](https://dev.epicgames.com/documentation/en-us/unreal-engine/motion-warping-in-unreal-engine): montage warp windows to named targets; status unstated. [Control Rig](https://dev.epicgames.com/documentation/en-us/unreal-engine/control-rig-in-unreal-engine): full-body IK, splines, usable in Animation Blueprints.
- [5.8 release notes](https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-8-release-notes) (first 100,000 of 357,524 characters read): Control Rig Physics to Beta; Retargeter foot definition and override sets; ChaosMover adds trajectory prediction for motion matching; Animation Mixing in Sequencer experimental; Mover "moving out of Experimental" (wording; page still says experimental).
- [MetaHuman 5.8 notes](https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine?lang=en-US): single-camera body capture (experimental, Windows-only); MetaHuman Crowd plugin (experimental, Mass, instanced meshes by distance); root motion removed from locomotion animations; neck bone propagation and LookAt fix; NaN-joint packaged-build fix.
- [Mono video capture](https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine?lang=en-US): plugin from Fab, Live Link Hub import, solve in Performance editor, export an animation sequence; the page gives no EULA, limits or footage rules. [Digital Production, 23 Jun 2026](https://digitalproduction.com/2026/06/23/metahuman-gets-markerless-mocap/): free incl. commercial use per the Fab listing (Fab unread), Windows, DX12, recommended 16 cores, 32 GB RAM, 8 GB GPU; no accuracy, foot-slide or cleanup figures.
- [MetaHuman Crowds](https://dev.epicgames.com/documentation/metahuman/metahuman-crowds-in-unreal-engine): far characters skip the post-process Anim Blueprint; fewer LODs; card hair. Mass: [page](https://dev.epicgames.com/documentation/en-us/unreal-engine/mass-entity-in-unreal-engine) tagged experimental. Pose Search release-note coverage: none found.

## 3. AI-native tools and licences
- Our markerless notes (SUMMARY, RECHECK): MediaPipe and MMPose Apache 2.0; AMASS and HumanML3D-trained text-to-motion models carry non-commercial chains.
- [MDM](https://github.com/GuyTevet/motion-diffusion-model): code MIT, but depends on CLIP, SMPL, datasets with their own licences; text to 9.8 s motion; outputs npy joints and SMPL params, mesh .obj for Blender; no Unreal route stated; last news 12 Feb 2025.
- [SMPL licence](https://smpl.is.tue.mpg.de/modellicense.html): non-commercial research, education, artistic only; commercial use prohibited without Meshcapade licence; training commercial networks barred.
- [GVHMR](https://github.com/zju3dv/GVHMR) (video to world-grounded motion): its [LICENSE](https://raw.githubusercontent.com/zju3dv/GVHMR/main/LICENSE) is custom, "educational, research and non-profit purposes only"; commercial needs permission. [WHAM](https://github.com/yohanshin/WHAM): page says MIT but needs SMPL registration; its LICENSE file unread; Blender/Unreal export not stated.
- [HY-Motion 1.0](https://github.com/Tencent-Hunyuan/HY-Motion-1.0) (30 Dec 2025): text-to-motion, 1.0B needs 26 GB VRAM, Lite 24 GB; licence terms unreached (License.txt returned 404); weights licence and territory limits unverified.
- Generative in-betweening: nothing read; unverified.

## 4. Small developers
- Devs on [80.lv](https://80.lv/articles/creating-gameplay-animations-without-an-expensive-mocap-suit/): hand-keyed in Blender over filmed reference, Auto-Rig Pro retarget; no hours given. [Xbox Wire, 19 Feb 2026](https://news.xbox.com/en-us/2026/02/19/how-soulslingers-indie-team-brought-custom-mocap/): suit supplied by publisher; days of rehearsal; one to three takes. No devlog found combining free video pose estimation with NPC motion (search only). Vendor blogs ignored as evidence.

## 5. Fit and cost (estimates, unmeasured)
- Epic's single-camera body capture: cheapest licence path (free, commercial per a secondary source); experimental; quality unmeasured. Test: 3 to 6 hours for one phone take through retarget to Ron, judged for foot slide.
- Keep GASP motion matching; the open-source AI models stay barred by licence until cleared.

Unreached: GDC talk bodies; metahuman.com 5.8 post (login redirect, not followed); Fab listing; HY-Motion licence text; 5.8 notes beyond character 100,000; Epic Crowd sample guides.

Reading of the sources: Epic's single-camera MetaHuman body capture, trialled on one phone take beside the existing motion matching, is the option they favour for us (the reader's reading, to be checked by the session).
