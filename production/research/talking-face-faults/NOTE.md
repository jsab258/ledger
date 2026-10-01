# Sheila's face breaking as she talks (research, 1 October 2026)

Asked: Jafar's verdict on the speaking films was "Sheila's face breaks when she talks, her mouth twisting sideways with a seam showing across her cheek." This note covers how professionals drive a MetaHuman (FACS) face for speech at run time, then a diagnosis from the evidence and code, the checks to run in order, and a fix for each cause. I did not run Unreal or use the graphics card. Evidence: production/approvals/2026-10-01/answer-{sheila,darren,ron}.jpg, ue-probe/Source/LedgerProbe/Private/PersonAnim.cpp, Public/PersonAnim.h, and CrimeProbe.cpp (DressBody, MouthApply, HeardLevel).

## The answer in short

The most likely cause is the face idle's own mouth, not the loudness mouth. Each face plays Epic's captured face idle, mhc_mh001_fmn_f_idle (CrimeProbe.cpp, kLiveIdles), and our speaking mouth overrides only 11 of its roughly 150 mouth-area controls. Every other mouth, jaw and lip control in the idle passes through at full strength while the jaw opens: one-sided ones (mouthLeft/Right, jawLeft/Right, corner pull, press or depress on one side, lip shifts) and paired ones held at unequal values. When the idle reaches a moment where its captured mouth is pushed to one side, opening the jaw on top of it makes a twisted, one-sided mouth. Professionals avoid this with a mouth mask: while a character speaks, the speech layer owns every mouth and jaw control, and the idle keeps only the eyes, brows and blinks.

The "seam" looks like Sheila's own skin line. A thin marionette crease runs from her left mouth corner (viewer's right), and it is faintly there at rest (frames 0 and 1). The twist stretches it into a long dark diagonal down to the jaw. It should go back to its resting faintness once the twist is gone. Only if it does not go back do the face's wrinkle maps (animated maps) or the head turn need looking at.

The loudness code cannot make the asymmetry by itself. All its values are equal left and right, and all are inside 0 to 1: jaw 0.04 to 0.40, lips together up to 0.6, funnel up to 0.25, stretch up to 0.18, applied with ModifyCurve's Blend (a lerp, not additive).

## What the evidence shows

- **Sheila, frames 10 to 21** (the second sentence): her mouth is moved toward her own right, and the philtrum and chin skew with it. The open part of the mouth sits to one side. Her left cheek line is stretched from the mouth corner to the jawline. In frames 0 to 9 the mouth opens symmetrically and the same line is short and faint. In 10 to 21 her head is also turned to her right and down.
- **Darren, frames 0 to 11**: the same twist, in the same direction (toward his own right). It shows even in the quiet frames (0 and 6), where the lips are pressed and pushed to one side, so the one-sided mouth is there before the jaw opens. In frames 13 to 21 he faces front and his mouth is symmetric.
- **Ron**: symmetric throughout, facing front.
- **What fits**: all three play the same face idle, started 2.3 s apart in the loop. A one-sided stretch of that capture would show on whoever is speaking when their loop reaches it, always twisting the same way. That matches Sheila and Darren both twisting to their right. In both cases the twist coincides with the head turned to the right and down. That is either the same captured moment in the body idle (the actor glancing aside and shifting the mouth together) or our regard Look At. Check 3 separates the two.
- **The made-line path** (SaidTick) has the same gap. It copies only the mouth curves present in the made face, so any mouth curve the made face lacks still comes from the idle.

## Part 1: the method. How shipped games and Epic drive a speaking face

**Speech owns the mouth; the idle and emotion own the rest.** Everyone in the sources splits the face by region:

- Epic's audio-driven solve has a Process Mask: "full face animation or just curves relevant to the mouth region", explicitly for layering (S1).
- Hogwarts Legacy put Speech Graphics' lip-sync over English capture "by isolating the mouth muscles" (S8).
- JALI (Cyberpunk 2077) drives the jaw and lips from speech, and moves the neck, brows and eyes separately (S9).
- Because a MetaHuman face is driven by curves, layering is done per curve, not per bone. Epic forum advice is to remove the eye curves from one animation and all but the eye curves from the other (S5). An answer on another thread fades the idle out while the character talks (S6).
- NVIDIA warns that the default Face_AnimBP's own MouthClose-driven animation "interfere[s]" with Audio2Face lip movement and must be bypassed (S11). This is the same class of fault as ours: another layer still writing mouth controls under the lip-sync.
- One trap: a third-party guide's "Use Max Value" curve blend (S12) keeps the idle's one-sided mouth controls. That is exactly the wrong choice for this fault.

**Which controls a speech mouth uses.** MetaHuman's raw controls (S2) include:

- **Symmetric shapes:** jawOpen, and the quadrant lip controls (funnel, purse, towards, together, press, push and pull, in UL/UR/DL/DR quarters).
- **One-sided L/R pairs:** mouthStretch, mouthCornerPull, mouthCornerDepress, mouthUpperLipRaise, mouthLowerLipDepress and mouthDimple.
- **Lateral controls:** mouthLeft/Right, jawLeft/Right, and the upper and lower lip shifts.
- **The nasolabial fold's own control:** noseNasolabialDeepenL/R.

Speech solvers produce symmetric output by design:

- Audio2Face-3D's solver constrains every weight to [0,1], adds a symmetry term ("balanced activation" of left and right) and makes opposing poses mutually exclusive (S10).
- Meta's OVR Lipsync uses 15 symmetric visemes (sil, PP, FF, TH, DD, kk, CH, SS, nn, RR, aa, E, ih, oh, ou); it is end-of-life (S13).

Asymmetry is reserved for deliberate expression, and our loudness mouth correctly uses only symmetric pairs. The fault is what we let through underneath it.

**How the face is kept whole.**

- RigLogic turns the raw controls into joints, corrective blend shapes and animated-map (wrinkle) weights. Correctives fire on combinations of controls (S3, S4).
- The wrinkle maps are three animated normal and colour delta maps blended by region masks. They are 1K and 512 deltas and are switched off from LOD2 and at Medium or Low material quality (S7, S14).
- The face copies the body's bone pose in its post-process AnimBP (Copy Pose From Mesh), so head and neck come from one place (S15).
- So a symmetric, in-range set of mouth controls gives a whole face. A one-sided mouth control under an open jaw gives a corrective and wrinkle response on one side only, which is what the films show.

**Run-time options (unchanged from production/research/lip-sync/NOTE-2026-09-30.md).** Epic 5.8's real-time audio model adds procedural blinks and emotion detection (S16). Its documented Live Link audio route is GPU-heavy (S17). The streaming solver already planned is the professional route. It should be applied with the mouth-only mask below, or it will meet the same pass-through.

## Part 2: what to check first, in order

1. **Dump the idle's mouth curves over its loop.** This is cheap and needs no graphics card: an editor Python run with -nullrhi that reads each CTRL_expressions_mouth*, jaw*, teeth* and tongue* key of mhc_mh001_fmn_f_idle.
   - List the moments where any L/R pair differs by more than 0.1, or where mouthLeft/Right, jawLeft/Right or a lip shift goes above 0.1.
   - **How it shows:** one or more stretches of the loop with strong one-sided values, lasting about the length of a sentence.
2. **Log what the face actually receives during a film.** For each MouthFilm frame, log the Face component's evaluated curves (every CTRL_expressions_ value that differs left to right, plus the lateral ones), the idle's play time, SpeakWeight and LookAlpha.
   - **How it shows:** in Sheila's frames 10 to 21 the asymmetric curves are present, and they are not among our 11. The idle time falls in a stretch found in check 1.
3. **A/B film, same line, same idle start.** This uses the existing -MouthFilm and -FaceAB setup.
   - **(a)** As now.
   - **(b)** With all mouth and jaw curves masked while speaking (fix A).
   - **(c)** With the look off.
   - **How it shows:** if (b) removes the twist, the idle's curves are the cause. If only (c) removes it, the head turn is involved: go to check 6.
4. **The seam at rest.** Film or still the same idle moment without speech, using the portrait tool's -PortraitFaceAt and Scan shot of the face idle.
   - **How it shows:** if the line is long and dark there too, the idle's own one-sided mouth is stretching the skin, and fix A also fixes it. If it is faint at rest and long only when speaking, the speaking twist stretches it, and fix A also fixes it. If it stays after fix A, go to check 5.
5. **Wrinkle maps and textures, only if the line survives fix A.**
   - Re-film at the same moment with animated maps off, as a test only: Medium material quality, which Epic's scalability uses to switch them off (S7), or forced LOD2.
   - Log the RigLogic animated-map weights (the face's wrinkle-mask curves) for that region.
   - **How it shows:** the line vanishes with animated maps off, and one mask weight is high on that side.
   - Also confirm the face is at LOD0 at 60 cm (MouthApply already logs the LOD) and that the face textures are streamed at full mip. The line exists at rest, so compression is unlikely.
6. **The head turn, only if check 3(c) implicates it.**
   - Confirm the face's post-process AnimBP copies the body's pose (tools/ue/face_rig_check.py lists it; Epic's setup copies it, S15). Without that copy, the face runs its own idle, calm and Look At, and its neck can part from the body's.
   - Also note that our Look At turns the head bone alone (clamp 60°) while the neck is held 70% toward rest, so a glance is carried by one joint.
   - **How it shows:** a mismatch at the neck, or the lower face stretching only while LookAlpha is high.

## Part 3: fixes, by cause

- **A. Idle mouth curves pass through (most likely).** While speaking, mask the whole mouth. Put every mouth, jaw, lip, teeth and tongue control into the Mouth node's map (from the face's curve list, by the same name test SaidTick uses):
  - the loudness values for our 11;
  - 0 for all the others, or at most a small symmetric remainder: the mean of each L/R pair, scaled down, and the lateral controls zeroed;
  - all of it blended in by SpeakWeight as now.

  Do the same in SaidTick, so that mouth curves missing from a made face are zeroed rather than left to the idle. Eyes, brows and blinks stay the idle's. This is Epic's own mouth-only cut (S1, S5). It changes nothing in the face asset. Cost: a longer curve map; trivial.
- **B. The idle itself.** If check 1 shows one-sided mouth moments even when nobody is speaking that read badly, also damp the idle's lateral mouth and jaw controls at all times, or pick a calmer Epic idle. This is animation, not the face.
- **C. Head turn (only if check 6 implicates it).** Make sure the face copies the body. Spread the turn across neck_01, neck_02 and the head rather than the head alone, and keep the glance smaller while speaking. This is animation, not the face.
- **D. The cheek line (only if it survives A).** Find the control whose wrinkle region lights up, and keep our curves under it. For example, lower or drop mouthStretch, which carries a wrinkle region. Our code is the thing to change, not her maps.

## Flags: what would change the approved face (MH_LenaS4)

None of fixes A to C touches the face asset. The following would, so each needs Jafar's yes before anyone does it:

- editing her DNA or its expression poses;
- changing her skin texture or Face Texture Index (the marionette line is part of her approved skin);
- switching off or editing animated maps in her material (this changes how her face looks in every expression);
- changing her LOD settings.

## Sources

- S1: Epic, "Audio Driven Animation" (MetaHuman docs; Process Mask, head movement, real-time solver option), undated, read 1 Oct 2026. https://dev.epicgames.com/documentation/en-us/metahuman/audio-driven-animation
- S2: Epic, "Control Curves Driven by MetaHuman Animator" (raw control list), undated, read 1 Oct 2026. https://dev.epicgames.com/documentation/metahuman/mh-standards-docs/mha_index?lang=en-US
- S3: Epic/3Lateral, "Rig Logic: Runtime Evaluation of MetaHuman Face Rigs" whitepaper v2 (controls, correctives, animated maps, LODs), c. 2022, reported 10 May 2022 by 80.lv. https://cdn2.unrealengine.com/rig-logic-whitepaper-v2-5c9f23f7e210.pdf ; https://80.lv/articles/epic-revealed-the-tech-side-of-metahuman-creator-face-rigs
- S4: Epic, MetaHuman DNA Calibration docs (behaviour layer: GUI to raw, correctives, joints, blend shapes, animated maps), read 1 Oct 2026. https://github.com/EpicGames/MetaHuman-DNA-Calibration/blob/main/docs/dna.md
- S5: Epic forum, "How to blend MetaHuman's facial animation", 22 to 24 Jan 2023 (layer by curve, not by bone). https://forums.unrealengine.com/t/how-to-blend-metahumans-facial-animation/754799
- S6: Epic forum, "Metahuman idle animation stops when talking animation starts", answer 8 Oct 2023 (fade the idle while talking). https://forums.unrealengine.com/t/metahuman-idle-animation-stops-when-talking-animation-starts/786288
- S7: Epic, "MetaHuman Materials and Textures" (animated delta maps 1K/512; off at LOD2 and Medium/Low quality), undated, read 1 Oct 2026. https://dev.epicgames.com/documentation/metahuman/metahuman-materials-and-textures
- S8: Speech Graphics, "Audio Driven Facial Animation for Hogwarts Legacy", dated 23 Nov (year not shown; game 2023), read 1 Oct 2026. https://www.speech-graphics.com/client-projects/hogwarts-legacy
- S9: Edwards et al., "JALI-Driven Expressive Facial Animation and Multilingual Speech in Cyberpunk 2077", SIGGRAPH 2020 Talks, Aug 2020. https://dl.acm.org/doi/10.1145/3388767.3407339
- S10: NVIDIA, "Audio2Face-3D: Audio-driven Realistic Facial Animation for Digital Avatars", arXiv 2508.16401, 22 Aug 2025. https://arxiv.org/html/2508.16401v1
- S11: NVIDIA ACE Unreal Plugin 2.5, "Character Animation", last updated 31 Jul 2025 (MouthClose block interferes; bypass it). https://archive.docs.nvidia.com/ace/ace-unreal-plugin/2.5/ace-unreal-plugin-animation.html
- S12: Georgy Dev, "Runtime MetaHuman Lip Sync: Plugin Configuration" (paid plugin; method only), undated, read 1 Oct 2026. https://docs.georgy.dev/runtime-metahuman-lip-sync/plugin-configuration/
- S13: Meta, "Oculus Lipsync Viseme Reference" (end-of-life), read 1 Oct 2026. https://developers.meta.com/horizon/documentation/unreal/audio-ovrlipsync-viseme-reference/
- S14: Joe Raasch, "Metahuman Wrinkle Maps" (three wrinkle normal maps, masks), undated (c. 2023), read 1 Oct 2026. https://www.joeraasch.com/projects/metahuman-wrinkle-maps
- S15: Epic, "Play a Custom Animation" (the face copies the body in its post-process AnimBP; face curves overwrite body curves), undated, read 1 Oct 2026. https://dev.epicgames.com/documentation/metahuman/play-a-custom-animation?lang=en-US
- S16: Epic forum, "MetaHuman 5.8 Released!", 17 Jun 2026 (real-time audio model: procedural blinks, emotion detection). https://forums.unrealengine.com/t/metahuman-5-8-released/2729288
- S17: Epic, "Real-Time Animation for MetaHumans in Unreal Engine" (audio and video Live Link sources use the GPU), undated, read 1 Oct 2026. https://dev.epicgames.com/documentation/metahuman/realtime-animation-for-metahumans-in-unreal-engine
- Also seen: Epic forum, "[Solved] Black outline artifact only at LOD 0 on MetaHuman eyes (Use Animated Maps)", 9 Jul 2026. This shows the animated colour delta can draw dark lines from a shader offset, though only around the eyes. https://forums.unrealengine.com/t/solved-black-outline-artifact-only-at-lod-0-on-metahuman-eyes-use-animated-maps/2734633
