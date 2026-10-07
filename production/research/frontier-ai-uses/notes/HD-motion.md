> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand D: character motion, July to October 2026

Helper report, 7 October 2026, about 30 minutes of searching. Covers motion from video, text-to-motion, in-betweening and transitions, retargeting and foot contact, motion matching, physics controllers, and faces from audio. LEDGER problem 4: natural sitting, standing, turning and idling for MetaHumans, using no NoAI asset.

Marks: [SHOWN] means I read the evidence myself (a GitHub README, LICENSE or CHANGELOG, a merged pull request, Epic's docs). [ABS] means I read only the arXiv abstract, which is the authors' own claim. [SS] means a search summary only: a lead, not evidence. UNREACHED means the page could not be opened. [I] means my own inference.

UNREACHED this session: fab.com (every Fab listing, so no NoAI flag could be checked), forums.unrealengine.com, research.nvidia.com and nvlabs.github.io (project pages and docs), www.nvidia.com (the licence texts themselves), huggingface.co (model cards and dataset terms), cgchannel.com, digitalproduction.com, rokoko.com.

---

## Bottom line

1. **The most direct route for LEDGER is Epic's own MetaHuman Animator Markerless Motion Capture plugin.** It is free, came with UE 5.8 (June 2026), is still Experimental and runs on Windows only. It solves body animation from one ordinary camera (a phone works) straight onto the MetaHuman skeleton, offline, on the local PC. Jafar or a friend could film "sit down on a chair", "stand up", "turn round", "idle while listening", and the clips would come from his own footage, with no dataset in between. Two questions stay open, and both must be checked on the PC:
   - whether its Fab listing is marked NoAI (UNREACHED here);
   - whether the body solve runs on an RX 6700. Epic recommends at least an RX 6800 XT with 8 GB and a DirectX 12 card. Nobody has reported results on AMD that I could find.
2. **The cleanest text-to-motion model for a sold game is NVIDIA's Kimodo, in its SOMA "RP" versions** (released March 2026, v1.1 in April; background, before the window). It was trained on 700 hours of licensed studio mocap (Bones Rigplay 1), not on AMASS or SMPL data. The code is Apache-2.0 and the weights are under the NVIDIA Open Model License, which by the README and search summaries allows commercial use and claims no ownership of outputs. It writes BVH files. It is officially tested only on NVIDIA cards, but nothing in its install list ties it to CUDA, and it can put its large text encoder on the CPU. Whether it runs on this PC (CPU or a community ROCm build) is unproven. **Do not use the Kimodo SMPL-X version (non-commercial), and do not use "drunk" prompts (LEDGER's no-alcohol rule).**
3. **NVIDIA's ARDY (10 July 2026, SIGGRAPH 2026)** is the real-time, streaming sibling of Kimodo, under the same licence and trained on the same data. It is interesting as a live locomotion and idle controller, but it is not practical on a 10 GB AMD card that is shared with the game and the voice.
4. **Excluded for a sold game:**
   - Tencent HY-Motion 1.0 and anything distilled from it (its licence does not apply in the EU, the UK or South Korea, and bans using its output outside its territory, so a game sold in the UK is outside it);
   - FlowHMR, GVHMR, PromptHMR and NVIDIA GEM-SMPL/GENMO (all licensed non-commercial);
   - the Kimodo SMPL-X version;
   - any model trained on AMASS or HumanML3D unless its own terms say otherwise.
5. **Mixamo is still online and free, though unmaintained** [SS]. It stays as the allowed baseline. Cascadeur's AI in-betweening costs money (Indie about $19 a month [SS]), so it is Jafar's decision.

---

## A. Motion from video

### A1. Epic: MetaHuman Animator Markerless Motion Capture plugin (UE 5.8)
- **Who and when:** Epic Games. It is "an experimental feature introduced in Unreal Engine 5.8" [SHOWN, Epic docs]. UE 5.8 was released on 23 June 2026 [SS], and press coverage dates from 18 to 23 June 2026 [SS]. That is just before the window but current.
- **Shown (Epic's docs, read):**
  - The plugin "integrates single-camera body-animations into the MetaHuman Animator to create body-only, or face and body animation for a single actor from one camera."
  - "Animation is processed offline."
  - It is installed from Fab, runs on Windows only, and needs UE 5.8 or later, Live Link Hub and Capture Manager.
  - It outputs "standard animation sequences".
  - The UE 5.8 release notes list "MetaHuman Animator – Body Capture, Experimental: body capture for single actor from single camera". Body features are Windows-only; facial capture now also runs on Linux and macOS.
  - MetaHuman hardware page: at least an NVIDIA RTX 3070, AMD RX 6800 XT or Apple M2 Ultra with 8 GB of video memory, at least 16 cores and 32 GB of RAM, and DirectX 12 as the default.
  - URLs: https://dev.epicgames.com/documentation/metahuman/metahuman-animation-from-mono-video-capture-in-unreal-engine ; https://dev.epicgames.com/documentation/metahuman/metahuman-hardware-requirements-in-unreal-engine ; https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes
- **Claimed:**
  - Free; takes video from a phone, webcam or studio camera; processed locally; hands included; can retarget to other characters [SS, press].
  - Uses about 3 GB of extra video memory while processing [SS].
  - A forum thread reports that "Stage 4 causes GPU reset and black screens on RTX 5070" in UE 5.8.2 [SS, title only; the forum was UNREACHED].
  - I found no report either way on AMD cards.
- **LEDGER angle:**
  - Problem 4, directly. The input is Jafar's own footage, so no dataset taint [I].
  - The output is already on the MetaHuman skeleton, with no BVH conversion and no retarget chain. It can then be cleaned in Sequencer.
  - **This PC:** the RX 6700 (10 GB) is below Epic's recommended RX 6800 XT but is a DirectX 12 card. Whether the body solve runs on AMD is unknown [I]; it is a one-evening test.
  - **Cost:** free.
  - **Licence:** an Epic tool, but distributed through Fab. Its "Allows usage with AI" flag must be read on the PC before use (UNREACHED), since Epic's own garment packs and the Game Animation Sample are NoAI.
  - It is Experimental, so it may change or vanish.

### A2. NVIDIA GEM-X: video to the SOMA 77-joint skeleton (background, March 2026)
- **Who and when:** NVIDIA. First commit "Initial release" on 16 March 2026, latest commit 27 April 2026 [SHOWN, GitHub commit list]. The README's news lines say "2025-05/06", which conflicts with the commit history and looks like a typo.
- **Shown (README, DEMO and INSTALL read):**
  - Monocular video in, whole-body 77-joint motion out (body, hands, face) on NVIDIA's SOMA body model, with world-space trajectories from moving cameras.
  - Code is Apache-2.0; weights are under the NVIDIA Open Model License. The README says "commercially usable, trained on NVIDIA-owned data only".
  - The pipeline uses SAM 3D Body (Meta's SAM License) internally.
  - The install expects CUDA 12.6+. An ONNX Runtime version exists, and it runs on Apple Silicon via CoreML.
  - Outputs are PyTorch `.pt` pose files; BVH is written only for the G1 robot retarget.
  - URL: https://github.com/NVlabs/GEM-X
- **LEDGER angle:**
  - Problem 4. A commercially clean open alternative to A1 if Epic's plugin fails on AMD.
  - **This PC:** officially CUDA only. Because an ONNX path exists, ONNX Runtime with DirectML on the RX 6700 is plausible, but not shown [I].
  - Turning its SOMA output into a BVH for Unreal needs a conversion step, perhaps Kimodo's `kimodo_convert`, which reads and writes SOMA BVH [I, not tested].
  - **Cost:** free.

### A3. SAM 3D Body built into ComfyUI (23 August 2026)
- **Who and when:** ComfyUI pull request #14370 by kijai, merged 23 August 2026 [SHOWN, PR page].
- **Shown:**
  - Adds SAM 3D Body nodes with "temporal smoothing for video detection", "BVH animation export (tested with Blender import)", GLB export, and multi-person video tracks through SAM 3.1.
  - The PR discussion notes that "body sliding" occurs in video.
  - Meta's SAM 3D Body (single-image model, checkpoints from 19 November 2025) is under the SAM License: worldwide, royalty-free, commercial use not barred. The only restrictions I saw are on military, weapons and trade-sanction uses [SHOWN LICENSE].
  - Its body model MHR is Apache-2.0 [SHOWN].
  - URLs: https://github.com/Comfy-Org/ComfyUI/pull/14370 ; https://github.com/facebookresearch/sam-3d-body
- **LEDGER angle:**
  - Problem 4. A second clean video-to-BVH path.
  - It estimates poses frame by frame and then smooths them, so expect foot sliding and jitter needing cleanup [I, consistent with the PR's own note].
  - **This PC:** ComfyUI's official AMD ROCm support on Windows covers the RX 7000 and 9000 series. The RX 6700 (gfx1031) is not in AMD's official Windows PyTorch wheels [SS]. A community build for gfx1031 was reported in August 2026 [SS], and DirectML or the CPU are fallbacks [SS].
  - **Cost:** free.

### A4. Video models excluded on licence
| Item | Date | Licence (read) | Verdict |
|---|---|---|---|
| FlowHMR (motion capture from video, scored on how well a physics controller can follow it) | arXiv 2 Oct 2026 [ABS]; code at github.com/flowhmr/flowhmr | "educational, research and non-profit purposes only … prohibited for commercial use" [SHOWN]; also needs SMPL-family files | Excluded |
| GVHMR (Zhejiang) | background | research and non-profit only [SHOWN] | Excluded |
| PromptHMR (Meshcapade) | background | "Non-Commercial Scientific Research Use Only" [SHOWN] | Excluded |
| GEM-SMPL / GENMO (NVIDIA) | Mar 2026 release | NVIDIA OneWay Noncommercial [SHOWN] | Excluded |

FlowHMR's abstract claims an 82.47% physics-tracking success rate against 62.82% for GVHMR [ABS]. That is a useful signal of where quality is going, but the model cannot be used.

### A5. Other video items (research only)
- **MoCapAnything V2** (SIGGRAPH Asia 2026): video straight to joint rotations on any skeleton; rotation error about 10° [ABS, arXiv 2604.28130]. Code and licence not checked.
- **TopoCap** (June 2026): video to animation for any skeleton topology [ABS, 2606.12153]. Licence not checked.
- **XmoPipe** (June 2026) builds motion datasets from online videos [ABS]. Models trained that way carry copyright doubt for a sold game [I].

### A6. Commercial video mocap services
- **Rokoko Vision** has a free "Starter" tier: single-camera AI mocap, FBX export, commercial use allowed [SS; rokoko.com UNREACHED]. Footage is processed in their cloud [I]. No dated July to October 2026 news found.
- **Move AI, DeepMotion, QuickMagic:** no dated news found for the window [SS]. They are subscriptions, so money, so Jafar's decision.

---

## B. Text-to-motion and motion generation

### B1. NVIDIA Kimodo (background: 16 March 2026; v1.1 on 10 April; CPU text-encoder option on 24 April)
- **Shown (README, CHANGELOG, pyproject and limitations page read):**
  - **Model:** a kinematic motion diffusion model "trained on a large-scale (700 hours) commercially-friendly optical motion capture dataset", Bones Rigplay 1.
  - **Controls:** text prompts plus full-body keyframes, hand and foot positions and rotations, 2D waypoints and paths.
  - **Licences:** code Apache-2.0. Kimodo-SOMA-RP v1/v1.1, SOMA-SEED and G1 weights under the NVIDIA Open Model License. **Kimodo-SMPLX-RP under the "NVIDIA R&D Model" licence, so non-commercial.**
  - **Body model:** SOMA-X, Apache-2.0. SMPL was used only to build a topology correspondence; SMPL files are optional and user-supplied.
  - **Text encoder:** LLM2Vec (MIT) on the gated Meta-Llama-3-8B-Instruct.
  - **Outputs:** NPZ (joint rotations plus foot-contact labels), BVH on the 77-joint SOMA skeleton (with a "standard T-pose" option, 13 April), MuJoCo CSV, and AMASS npz (SMPL-X only).
  - **Hardware:** about 17 GB of video memory on the GPU, or under 3 GB with `TEXT_ENCODER_DEVICE=cpu`. Tested on RTX 3090, 4090 and A100. "Developed on Linux, though Windows should work especially if using Docker."
  - **Dependencies:** pure PyTorch and transformers, with no CUDA-only package.
  - **Stated limits:**
    - at most 10 seconds per prompt;
    - fewer than 20 constrained frames per constraint type;
    - "the model by itself can generate foot skating", which post-processing reduces;
    - prompts should start with "A person…";
    - training covers locomotion, gestures, everyday activities, common object interactions, and styles including tired, old, sad and "drunk".
  - URLs: https://github.com/nv-tlabs/kimodo ; https://github.com/NVlabs/SOMA-X
- **Claimed:** NVIDIA Open Model License: "commercially useable"; NVIDIA "does not claim ownership to any outputs" [SS; the licence page on nvidia.com was UNREACHED]. Bones' own BONES-SEED subset (288 hours) is gated, with "licensing inquiries" sent to Bones [SS].
- **Unreal tools around it** [SS, Fab UNREACHED]:
  - "Kimodo Importer" on Fab: imports Kimodo SOMA BVH and retargets it to the UE5 skeleton.
  - "MotionSmith AI" on Fab: wraps Kimodo inside UE 5.8 but needs an NVIDIA CUDA GPU and Llama 3 access.
  - A ComfyUI-Kimodo node exists.
- **LEDGER angle:**
  - Problem 4: generate "a person sits down on a chair", "stands up from a chair", "turns 180 degrees to the left", "stands idle, shifting weight, arms folded", "listens and nods". Then retarget the SOMA BVH to MetaHuman: BVH into Blender, FBX into Unreal, then the IK Retargeter [I].
  - Kimodo cannot see a chair. Seat height has to come from full-body keyframes or the pelvis path, and Motion Warping in Unreal aligns it to the real chair [I].
  - **Licence:** the SOMA-RP weights look clean for a sold game. Its training data is licensed mocap, not AMASS [SHOWN README; the conclusion is I]. Llama 3 8B is used only as a text encoder on the PC. Its community licence allows commercial use below 700 million monthly users and, to my knowledge, has no territory exclusion for this model [I, not re-read today].
  - **Content rule:** never use "drunk" prompts (no alcohol), and avoid the "childlike" style (no children).
  - **This PC:** not shown on AMD. Feasible in principle on the CPU: the text encoder in bf16 needs roughly 16 GB of RAM [I], so close Unreal first. The alternative is a community ROCm build for gfx1031 [SS]. It is offline authoring, so slowness is acceptable.
  - The model would need registering in production/retention.json under LEDGER's rules.
  - **Cost:** free.

### B2. NVIDIA ARDY (released 10 July 2026, ACM TOG / SIGGRAPH 2026)
- **Shown (README and abstract):**
  - Streaming autoregressive diffusion: text prompts can change on the fly, plus waypoints, keyframes and keyboard or mouse locomotion, in real time.
  - Weights ARDY-Core-RP (20 fps) and G1-RP, released 10 July 2026, NVIDIA Open Model License, trained on Bones Rigplay 1. Code Apache-2.0. A SOMA-skeleton version is "coming soon".
  - Tested on Ubuntu with an RTX 4090. TensorRT is optional; the text encoder needs about 14 GB on the GPU or can run on the CPU.
  - Outputs NPZ with joint positions, rotations and foot contacts. The README mentions no BVH.
  - URLs: https://github.com/nv-tlabs/ardy ; arXiv 2607.08741
- **LEDGER angle:**
  - Problem 4, plus a new idea: a live, steerable idle and locomotion brain for passers-by.
  - Not realistic on the RX 6700, which is shared with the game and the voice; at best an offline authoring source [I].
  - Its "Core" skeleton would need a retarget map [I].
  - **Licence:** the same as Kimodo.

### B3. Faster versions of the big models
- **TACD** (2 October 2026) [ABS]: distils HY-Motion and Kimodo into 8-step students, 7.7 to 11.9 times faster with 3.8 to 6.7 times less peak memory. Whether weights are released is not checked.
  - A Kimodo student would count as an NVIDIA model derivative, which the licence permits [I].
  - An HY-Motion student inherits HY-Motion's territory exclusion [SHOWN licence clause defining distillation as a Model Derivative].
- **MixiMotion** (19 September 2026) [ABS]: one-step generation in 9.3 ms against 829.6 ms for its teacher, HY-Motion-1.0-Lite. As a distillation of HY-Motion it inherits the exclusion. **Excluded.**

### B4. Tencent HY-Motion 1.0 (background, 30 December 2025)
- **Shown (LICENSE read):** "This license agreement does not apply in the European Union, United Kingdom and South Korea." Clause 5(c): you "must not use … Output … outside the Territory". Output may not be used to improve other AI models. It needs 24 to 26 GB of video memory and uses the SMPL-H skeleton.
- **LEDGER angle:** **Excluded.** A game set in Britain and sold there would use the output outside the licence's territory. URL: https://github.com/Tencent-Hunyuan/HY-Motion-1.0

### B5. Research to watch (no LEDGER use yet)
- **TimelineControl** (Gül Varol and others, 2 October 2026): streaming, overlapping actions on separate body parts ("answer a phone while walking"). Code "will become publicly available" [ABS]. Training data is likely derived from HumanML3D or AMASS, so probably non-commercial [I].
- **World2Motion** (29 September 2026): turns the Cosmos 3 video world model into a scene-aware motion generator from one image and text, for example interacting with objects in the scene [ABS].
- **Parasitic Co-Denoising** (2 October 2026): reads 3D motion out of a frozen Wan2.1 video model [ABS]. Heavy, research only.
- **FlexMoGen** (Pacific Graphics 2026): text plus a style clip [ABS].
- **RoMo** (CVPR'26): an in-the-wild dataset [ABS]. Internet-video origin means copyright doubt [I].

---

## C. In-betweening, transitions, retargeting, foot contact, motion matching

- **Cascadeur:**
  - 2026.1 (9 April 2026) added AI in-betweening between key poses, with existing animation usable as a style reference.
  - 2026.2 (6 August 2026) updated AI in-betweening and motion generation and added animation layers [SS; cgchannel UNREACHED].
  - Indie licence: $19 a month or $96 a year below $100k revenue, becoming a perpetual licence after a year [SS].
  - **LEDGER:** good for hand-keyed sit and stand transitions. It costs money, so it is Jafar's decision. Its training-data provenance was not checked.
- **Kimodo's keyframe constraints act as in-betweening:** give the standing pose and the seated pose, and the model fills the motion between them [SHOWN README; applying it to sit and stand is I].
- **NVIDIA MotionBricks** (SIGGRAPH 2026; news 15 June 2026): real-time in-betweening at very high throughput. Released checkpoints appear to be for the Unitree G1 robot only [SS; project page UNREACHED]. Not usable on people now.
- **UE 5.8 engine features** [SHOWN release notes]:
  - IK Retargeter: foot plane and toes definition for target characters, and better pelvis motion control (Production); Retarget Override Sets (Production).
  - Pose Search / Motion Matching improvements, including experimental "warped montage trajectories" (Production).
  - Motion Warping gets an extra rotation offset per animation (Production).
  - Control Rig Physics (Beta): layers physics over an existing animation with a keyframable weight, for subtle sway and settling.
  - Animation Mixing in Sequencer (Experimental).
  - **LEDGER:** motion matching and choosers can run on a database built from LEDGER's own clips (own video, Kimodo, Mixamo). The engine features are not Fab content, but the Game Animation Sample's data stays excluded [I]. Motion Warping is the standard way to land a sit-down on a particular bench or chair [I].
- **Retargeting research** (SIGGRAPH Asia 2026 journal track) [ABS], research only:
  - artifact-driven fixes for self-penetration, arXiv 2609.06517;
  - ReCHOIR, object-contact retargeting, 2609.10982;
  - learnable-flattening transformer retargeting, 2609.38578.
- **Foot contact:** Kimodo and ARDY output per-frame foot-contact labels and have a post-process for foot skating [SHOWN]. The UE 5.8 foot-plane retarget settings handle the rest [SHOWN feature; fit is I].

---

## D. Physics-based or learned controllers

- **Tired Actor** (4 August 2026): physics character control shaped by fatigue [ABS].
- **LYRIC** (17 September 2026): language-driven physics control for whole-body object interaction [ABS].
- **GPC** (June 2026): large-scale pretraining for motor control [ABS].

All are research on simulation stacks, typically NVIDIA Isaac or CUDA [I]. **No LEDGER use now.** For a physical feel inside Unreal, UE 5.8 Control Rig Physics (Beta) is the practical route.

---

## E. Faces and listening (surprises worth knowing)

- **MetaHuman audio-driven animation** (UE 5.6+) [SHOWN docs]:
  - Real time or offline, through a MetaHuman Audio Live Link source.
  - Mood overrides (neutral, happy, sad, fear, disgust, anger, surprise), generated head movement and blinks.
  - The docs do not say whether it runs inside a packaged game, and list no NVIDIA-only requirement.
  - **LEDGER:** relevant to live talk, problem 1, and to making a listener look alive. Whether the real-time solver ships in a packaged build has to be tested on the PC [I].
- **Third-party runtime lip-sync plugins on Fab** ("Runtime MetaHuman Lip Sync" and others) claim to work in packaged builds on any platform [SS; Fab UNREACHED, NoAI unchecked].
- **Listener motion research:**
  - real-time listener nodding with timing and amplitude (ICMI '26, 14 July 2026) [ABS];
  - REALM reactive listening faces (27 September) [ABS];
  - AVTR-1, an open real-time dyadic avatar stack (19 September) [ABS].
- **GENEA Challenge 2026** (11 August 2026) [ABS]: the best speech-driven gesture system scored 32% on speech alignment, against a 62% motion-capture ceiling, and the rest were near 0%. The study was large: more than 23,000 votes.
  - **LEDGER [I]:** generated co-speech gestures are not yet good enough. For people talking to Tom, pick idle, listening and gesture clips from captured or authored motion rather than generating gestures live.
- **TokTalk** (29 May 2026, background) [ABS]: facial animation straight from audio-LLM tokens in real time.

---

## F. Running any of this on THIS PC (RX 6700 10 GB, Windows)

- AMD's official PyTorch wheels for Windows cover the RX 7000 and 9000 series; the RX 6700 (gfx1031) is not officially supported [SS]. A community ROCm 7.x build for gfx1031 on Windows was reported working on an RX 6750 XT in August 2026 [SS]. DirectML (ONNX Runtime) and the CPU are the other routes.
- **What fits best:** Epic's plugin, if it runs on AMD (it is a DirectX 12 Unreal tool, untested on AMD). Then Kimodo on the CPU or a community ROCm build, offline. Then GEM-X or SAM 3D Body through ONNX or ComfyUI.
- **Nothing in this strand needs the cloud or money,** except the commercial services (Rokoko cloud, Move AI, DeepMotion) and Cascadeur.

## G. Suggested order for LEDGER (my inference)

1. On the PC, read the Fab NoAI flag of the MetaHuman Animator Markerless Motion Capture plugin.
   - If clear, film four short phone takes against a plain wall (sit down onto a chair, stand up, turn 180 degrees, idle while listening).
   - Solve them offline and judge the clips on a MetaHuman through the game camera.
2. If the plugin fails on AMD or is NoAI: install Kimodo-SOMA-RP with its text encoder on the CPU.
   - Generate the same four motions with keyframe constraints.
   - Take the BVH through Blender to FBX, retarget to MetaHuman in UE 5.8, and fix foot contact with the UE 5.8 foot-plane settings.
   - Land sit-downs with Motion Warping.
3. Use Mixamo clips as the fallback and filler.
4. Use Cascadeur only on Jafar's yes, since it costs money.
5. Never use HY-Motion, MixiMotion, FlowHMR, GVHMR, PromptHMR, GEM-SMPL, Kimodo-SMPLX, or any AMASS/HumanML3D-trained model.
