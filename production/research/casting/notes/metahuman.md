# Cast faces from an approved portrait: what MetaHuman (UE 5.6-5.8) can take in, and how close it gets

Research notes, 2026-09-24. Nothing downloaded or installed.
Labels: DOC = Epic/vendor documentation; MEASURED = a reported measurement or test; CLAIM = vendor or user assertion, not measured.
"opened" = page fetched and read; "snippet" = search-result text only, page not read.
Where a doc page shows no date it is marked "undated, current docs as read 2026-09-24".

---

## 0. The short answer

- **There is no official "image to MetaHuman" in 5.6, 5.7 or 5.8.** Epic's routes into a face are: presets + blend/sculpt, DNA import, template mesh (MetaHuman topology), custom mesh of any topology (Mesh to MetaHuman / "From Custom Mesh"), and Identity from **depth** footage (iPhone TrueDepth or a stereo head-mounted rig). Nothing takes a single still photo as the main input.
- The one image-related hook: the 5.8 Python API can add a **2D-landmark term from a portrait image** to a *mesh* conform, but the portrait must be a render with a camera you know exactly. It adds to a mesh fit; it does not replace one.
- So a generated portrait has to go through a **third-party image-to-head step** and then **From Custom Mesh**, or be matched by hand/script with the parametric face tools.
- Nothing in the MetaHuman pipeline is documented as NVIDIA- or CUDA-only. Our RX 6700 (10 GB) is **below Epic's recommended AMD card** (RX 6800 XT). Identity marker tracking needs **DirectX 12 on Windows**. Auto-rig and texture synthesis are **cloud** services.
- **No measured likeness numbers exist** in anything we found (no landmark error, no mm error for MetaHuman fits). The community reports are qualitative: "vaguely similar", losing ears, eyes, nose and mouth. All of those reports date from before 5.6.

---

## 1. What the current MetaHuman tools take as input

### 1a. MetaHuman Creator in-engine (since 5.6)
- **Creator moved into the editor in 5.6.** Its local authoring workflow "is enhanced by cloud services that deliver autorigging and texture synthesis". Face tools were extended to bodies, and a **parametric body system** was added. "Almost every Creator operation — sculpt, conform, wardrobe, rigging, texture synthesis — can now be batched via Python or Blueprints."
  Source: https://www.metahuman.com/news/metahuman-leaves-early-access-with-a-feature-packed-new-release, June 2025, snippet, DOC.
- **Creator import tools** take "custom meshes, template meshes, DNA files, or MetaHuman identity assets". The Head and Body tools "blend, sculpt, transform, and model".
  Source: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-in-unreal-engine?lang=en-US, undated, opened, DOC.
- **5.6 change:** Mesh to MetaHuman no longer creates a character in the web Creator. After making an Identity you use **Conform from Identity** in the MetaHuman Character asset editor.
  Source: https://dev.epicgames.com/documentation/en-us/metahuman/from-mesh, undated, opened (and snippet), DOC.

### 1b. Template conform (mesh already in MetaHuman topology)
- The mesh "must be the MetaHuman Template mesh in terms of topology … The semantic significance of the vertices needs to be preserved". Cardinal edge loops (eyelids, ear ridges, folds) cannot be approximated. Epic recommends "Conform from Template" in the Character asset editor.
  Source: https://dev.epicgames.com/documentation/metahuman/from-template-mesh, undated (5.6+), opened, DOC.
- **From Template tool / Mesh Fit:** "Match Vertices by UVs" handles meshes that have MetaHuman topology but a different vertex order, or were triangulated by FBX. Separate slots take eye and teeth meshes. Joints, RBFs and skin weights are generated automatically.
  Source: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-from-template-tool-in-unreal-engine, undated, opened, DOC.
- A forum/search snippet says a strictly MetaHuman-topology template gives "exactly that mesh rigged — not an approximation", and that a refine step projects template vertices to the closest point on the custom surface. **Not confirmed on the doc page we opened**, so treat it as a CLAIM.
  Source: https://forums.unrealengine.com/t/new-mesh-to-metahuman-workflow-for-custom-characters/1275923, 2023, snippet, CLAIM.
- 5.7 added "UV-space vertex correspondence between the conform template and model meshes", which allows FBX round-trips.
  Source: https://www.metahuman.com/news/metahuman-5-7-brings-major-improvements-to-body-conforming-with-more-to-come, late 2025, snippet, DOC.

### 1c. Mesh to MetaHuman / From Custom Mesh (any topology)
- **Identity route (5.6/5.7, still documented):** the input is an FBX or OBJ of any topology, ideally textured with skin albedo. The sclera must show ("Empty eye sockets are very likely to track poorly"), the eyes must be open, and the lighting flat and front-facing if the mesh is not albedo-textured. Use OBJ above 200k vertices. Steps: create an Identity → promote a neutral frame → track markers → Identity Solve → auto-rig.
  Source: https://dev.epicgames.com/documentation/en-us/metahuman/from-mesh, undated, opened, DOC.
- **5.8 "From Custom Mesh" tool:** does head and body conforming together in one step and "accepts head and/or body mesh of any topology as input". It is aimed at "scans, external GenAI/DCC tools". Auto Solve "frames the face, traces the facial features (creating a 2D View), and fits the MetaHuman mesh", then runs a refine pass. It works best on human-like meshes in an A-pose. Stylised or extreme meshes may not solve.
  - **It does not carry the source mesh's texture across.** Textures are only used to help trace features.
  - The doc does not mention the cloud for the solve itself.
  Sources: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-from-custom-mesh-tool-in-unreal-engine (undated, opened, DOC); https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine (5.8, released 17 June 2026, opened, DOC); https://forums.unrealengine.com/t/metahuman-5-8-released/2729288 (17 June 2026, opened, DOC).

### 1d. Identity from footage
- **Identity from video needs a compatible depth device**: an iPhone/iPad with TrueDepth (neutral, left, right and teeth frames), or a calibrated stereo pair (neutral and teeth), ingested through Capture Manager in Live Link Hub. Still images are not mentioned.
  Source: https://dev.epicgames.com/documentation/metahuman/from-video-footage, undated, opened, DOC.
- **Mono video or webcam is for performance (animation) only.** Identity creation needs depth. Devices: iPhone 12 or newer.
  Source: https://dev.epicgames.com/documentation/metahuman/metahuman-animator-capture-device-requirements, undated, opened, DOC.
- **For us: this route cannot take a generated portrait.** Not applicable.

### 1e. Single image or multiple images to MetaHuman
- **No Epic feature does this** in 5.6, 5.7 or 5.8 (checked the release notes and the Creator, From Mesh and From Footage docs). Only third-party tools do (section 3).
- **Python, 5.8:** a combined conform "from custom meshes with portrait images". You call `track_face_landmarks_from_image(pixels, width, height)`, and the 2D landmarks "drive the 2D landmark term of the solve". But: "The portrait must be pre-rendered, and the camera intrinsics and extrinsics supplied to the solver must match the camera that produced the image, because the 2D landmarks are back-projected into 3D."
  - This means a render of the custom mesh, not a free photo.
  - It is **untested whether an assumed camera for a generated portrait would help.** That is our inference, not Epic's.
  Source: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine, undated (5.8), opened, DOC.

### 1f. Skin texture: synthesis and "from photo"
- Skin is **parametric**: Skin Tone, Face Texture Index and Body Texture Index (these control wrinkles and apparent age). The texture source downloads at 2K, 4K or 8K. **Texture Override** accepts your own face and body maps. **No texture-from-photo feature is documented.**
  Source: https://dev.epicgames.com/documentation/metahuman/skin-material-tools?lang=en-US, undated, opened, DOC.
- Texture synthesis and high-resolution download run on Epic's servers (5.6 news, snippet, DOC; Python doc, opened, DOC).
- 5.8 adds "unbaked" texture and material authoring and export to DCC tools, plus custom lighting previews in Creator.
  Source: 5.8 release notes, opened, DOC.

### 1g. Body
- Parametric body (5.6). 5.7 removed the A-pose requirement and height limits, added FBX round-trip and "Estimate Joints from Mesh", and added hand and foot circumference parameters. 5.8 conforms body and head from any-topology meshes in one step.
  Sources: 5.7 news and 5.8 notes above, snippet/opened, DOC.

### 1h. Cloud auto-rig and texture service
- Auto-rig (joints-only, or joints + blendshapes) and texture download both call **MetaHuman Cloud**. "The editor must be signed in to an Epic account with MetaHuman Cloud access."
  Source: Python scripting doc, opened, DOC.
- **No published quota** was found for auto-rig or texture calls.
- **Known problem (thread dated 3 Aug 2026):** AutoRig and texture downloads fail on a hard-coded 300 s HTTP timeout ("Server Error"), mostly from non-US regions (reported from South Africa; one US repro). The engine's HTTP timeout settings do not change it. Workarounds that users reported: a US VPN, or Cloudflare WARP. The poster called it a regression from 5.5.
  Source: https://forums.unrealengine.com/t/metahuman-creator-in-editor-plugin-autorig-texture-download-fail-with-a-300s-http-timeout-server-error-from-non-us-regions-5-6-5-7-5-8-regression-from-5-5/2740392, 2026-08-03, opened, CLAIM (user reports).

### 1i. Python scripting
- Scriptable steps:
  - head conform from .dna, template mesh, vertex arrays or an Identity asset
  - body conform
  - face sculpt: landmarks, plus face-model (PCA) coefficients
  - body sculpt constraints
  - texture download (cloud)
  - auto-rig (cloud)
  - assembly (Cinematic, Optimized or UEFN)
  - export (DCC, DNA, meshes)
- Example scripts ship with the plugin under `Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Python/examples/`: `example_conform_head.py`, `example_conform_from_identity.py`, `example_sculpt_face.py`, `example_download_textures.py`, `example_auto_rig.py`, `example_assembly.py`, and others.
  Source: Python scripting doc, opened, DOC.
- 5.8 adds `GetFaceModelCoefficients` / `SetFaceModelCoefficients`, which gives "conform-to-PCA support".
  Source: 5.8 release notes, opened, DOC.
- **Why this matters for us:** a script can read and set the whole face-shape vector. That makes an automated "render → compare with portrait → adjust" loop possible without any mesh (our inference).
- 5.8 also open-sources RigLogic and DNA as **OpenRigLogic** (MIT).
  Source: 5.8 forum post, 17 June 2026, opened, DOC.

---

## 2. Hardware and OS

- **Recommended GPU** (for both Animator and Creator): "At least nVIDIA RTX 3070, AMD RX 6800 XT, or Apple M2 Ultra, with 8GB VRAM". Also recommended: 16 physical cores and 32 GB RAM. Assembly with large or virtual textures can go past 32 GB. Windows needs a DX12 card with DX12 as the default RHI.
  Source: https://dev.epicgames.com/documentation/metahuman/metahuman-hardware-requirements-in-unreal-engine, undated (URL suggests 5.7), opened, DOC.
  - **Our RX 6700 10 GB is below the recommended AMD card, though above the 8 GB VRAM line.** Nothing says it is unsupported.
- **Windows and DX12 only:** Identity marker tracking is limited to DX12, so on Mac/Linux, Identity and Performance creation and "Conform from Identity" are disabled.
  Source: hardware requirements page, snippet (same page family), DOC.
- **No CUDA or NVIDIA-only requirement** is documented for Creator, conform or Identity. Both AMD and NVIDIA are listed as supported. DOC.
- **Old AMD reports:**
  - RX 6600 XT crash on "Track Active Frame" in Mesh to MetaHuman: https://forums.unrealengine.com/t/mesh-to-metahuman-crashing-problem/747903, Jan 2023, snippet, CLAIM.
  - R7 card ran out of VRAM on Identity Solve: https://forums.unrealengine.com/t/metahuman-identity-solve-crashes-video-card-on/641706, Sep 2022, snippet, CLAIM.
  - Both predate 5.6.
  - The 5.8 known-issues page lists **no AMD, conform or auto-rig issues**: https://dev.epicgames.com/documentation/metahuman/metahuman-known-issues-5-8-in-unreal-engine, opened, DOC. The only related item: Identity assets from earlier plugin versions open empty in 5.8 and must be recreated.
- **Depth cameras** (iPhone TrueDepth, stereo HMC) are needed only for Identity from footage. They are not needed for mesh or template conform. DOC (section 1d).

---

## 3. Third-party routes from a portrait to a 3D head

| Tool | Input | Output / MetaHuman link | Runs on | Licence / cost | Source |
|---|---|---|---|---|---|
| **KeenTools FaceBuilder for Blender** | 1 image minimum; the MetaHuman page says **4–8 photos**; you place pins by hand | Head mesh, low/mid/high poly; "one-click texturing" blended from the views; exports an **"MH texture"** in MetaHuman UV layout; alignment goes through Mesh to MetaHuman | Blender 64-bit on Win/Linux/Mac; needs a GPU Blender supports (no CUDA stated) | Freelancer $19.99/mo or $15.99/mo billed yearly; Studio $699/yr; 15-day free trial; "all subscriptions can be used for commercial work"; Freelancer = one machine, one person | https://keentools.io/products/facebuilder-for-blender (opened, DOC/CLAIM); https://keentools.io/integrations/fbb-mh (undated, opened, DOC); https://keentools.io/buy (opened) |
| **MetahumanModeler** (Blender addon, liyouwang) | Single image; multi-view since v2.0 (Feb 2026); symmetry v2.2 (Apr 2026); texture fusion v2.3 (May 2026) | Head **directly in MetaHuman topology** via shape keys, plus a facial texture, so it can go straight to **template conform** | Windows only; Blender 3.3–3.6 and 4.1–4.5; GPU not stated | $59 (Gumroad); licence terms not read | https://blenderartists.org/t/generating-metahuman-based-on-a-single-image-blender-ue5-tutorial/1531052 (opened); price from snippet of https://liyouwang.gumroad.com/l/MetahumanModelerCompiled |
| **Reallusion Headshot 3 / 3.1** (in Character Creator 5) | Single front photo, optional side/full-body; tools to neutralise expression, balance light and remove stray hair | Rigged CC5 head and body, 4K texture; head generation **runs locally**; the optional AI image generator uses online credits. CC5 exports rigged to Unreal; its mesh could then go through From Custom Mesh (our inference) | Windows | Headshot 3.1 $199 perpetual **+ CC5 $299 perpetual** (or $29/mo, $99/yr) | https://www.cgchannel.com/2026/07/reallusion-releases-headshot-3-0/ (3.0 on 28 Apr 2026, 3.1 on 3 Jul 2026, opened); https://www.reallusion.com/character-creator/headshot/photo-to-3d-head.html (opened, CLAIM "Unmatched Precision") |
| **TRELLIS.2** (Microsoft, 4B) | Single image | Textured PBR mesh (general objects, not specialised for heads) | **CUDA-only** officially; community AMD/ROCm forks exist with reported problems | **MIT** | https://github.com/microsoft/TRELLIS.2 and issue #74 (snippet) |
| **Hunyuan3D 2.x / 3.x** (Tencent) | Single image | Mesh | CUDA | **Licence excludes the EU, UK and South Korea**, plus conditions above 100M MAU. **FLAG: do not use.** | https://github.com/Tencent-Hunyuan/Hunyuan3D-2.1/blob/main/LICENSE (snippet) |
| **FaceLift** (ICCV 2025) | Single image → multi-view diffusion → Gaussian splats | 3D head as Gaussians, not a mesh | CUDA | Code Apache-2.0, **weights: Adobe Research License (non-commercial)**. Not usable. | https://github.com/weijielyu/FaceLift (snippet) |
| **DECA / EMOCA / SMIRK** (FLAME fitting) | Single image | FLAME mesh (coarse) | PyTorch (CPU is possible, slow) | DECA: **non-commercial research only**. The FLAME 2023 Open model is CC-BY-4.0, but older FLAME and these fitters are research-only. Not usable. | https://github.com/yfeng95/DECA (snippet); https://flame.is.tue.mpg.de/ (opened) |
| **PanoHead** (CVPR 2023) | Single image, via GAN inversion | 360° head | CUDA | NVIDIA proprietary / NC. Not usable. | https://github.com/SizheAn/PanoHead (snippet) |
| **Hyper3D Rodin** | Image(s) | Textured mesh (cloud) | Cloud | Paid plans (Creator $30/mo, Business $120/mo) or about $0.4–1.5 per model; "full commercial rights" claimed | https://hyper3d.ai/pricing (snippet, CLAIM) |
| **Avaturn** | Selfies | Its own rigged avatar, not MetaHuman | Cloud | Pro $800/mo | https://avaturn.me/ (snippet) |

**Helper tool: Character DNA Addon (poly-hammer).** It imports MetaHuman DNA into Blender, lets you edit the head and body, and sends them back to Creator. Supports UE 5.6–5.8 and Blender 4.5/5.2. GPL-3.0, free base plus a paid pro tier. Useful for hand-fixing likeness after a fit.
Source: https://github.com/poly-hammer/meta-human-dna-addon, opened, DOC.

---

## 4. Measured closeness

- **No quantitative likeness measurement was found** for MetaHuman Identity, template or custom-mesh fits (no landmark error, no mm RMS, no recognition score) in Epic docs, forums or papers searched. The papers that do report ~1–2 mm registration errors are about generic template registration, not MetaHuman.
- **Qualitative reports (all before 5.6):**
  - The Identity solve keeps some resemblance. Applying skin in the (then web) Creator moves it further away: "vaguely similar"; one user showed the drift stage by stage (mesh → solve → Creator → skin).
    Source: https://forums.unrealengine.com/t/mesh-to-metahuman-not-similar/579555, June 2022 to April 2024, opened, CLAIM.
  - Stray in "ears, eyes, nose and mouth, areas that are vital in capturing a likeness". Cause: the mesh is contorted to the conformal template. Fix: edit in Blender (MetaReForge) and rewrite the DNA.
    Source: https://www.linkedin.com/pulse/unreal-engine-mesh-metahuman-likeness-improvement-blender-grizzle-q2uce, 10 Jan 2024, opened, CLAIM.
- MetahumanModeler's own author: "If you have very high accuracy or shape similarity in generating models, then this addon is not an optimal choice." Source: blenderartists thread, opened, CLAIM (a vendor admitting a limit).
- **Structural limits (DOC + inference):**
  - The face lives in MetaHuman's database/PCA space. 5.8 exposes the coefficients, which suggests the default conform can leave that space and conform-to-PCA pulls it back.
  - Eyes and teeth are separate meshes.
  - Hair, brows and lashes are grooms, not taken from the mesh.
  - Skin is parametric plus override: **age, wrinkles, blemishes and complexion do not come from the fit**; they come from the texture index/tone or a custom texture.
  - Clothed meshes fit to the garment silhouette.
  - Strong asymmetry and extreme proportions solve less well.

---

## 5. What our image lane could produce

**What stable-diffusion.cpp supports** (README, opened 2026-09-24, DOC):
- Z-Image, Qwen Image (including 2.1, Day-0 on 20 Sep 2026), FLUX.1/2
- **Edit models that take a reference image (`-r`)**: FLUX.1-Kontext-dev, the Qwen-Image-Edit series and others
- **PhotoMaker** (SDXL only; v2 needs `id_embeds` from a Python `face_detect.py`, i.e. InsightFace)
- **IP-Adapter** (SD1.5/SDXL, including Plus)
- ControlNet (SD1.5)
- Backends include Vulkan
- **No PuLID and no InstantID found in sd.cpp.**
Sources: https://github.com/leejet/stable-diffusion.cpp (opened); https://github.com/leejet/stable-diffusion.cpp/blob/master/docs/photo_maker.md (opened).

**Consistency options:**
- **Same seed + same prompt with the view changed.** Cheap, but the identity drifts across views. No source; general practice.
- **Reference-image editing from the approved front portrait.** Qwen-Image-Edit-2509/2511 is **Apache-2.0**. 2509 claims better person consistency. 2511 adds multi-angle views from one reference. A community "Multiple-angles" LoRA exists for 2509.
  Sources: https://huggingface.co/Qwen/Qwen-Image-Edit-2509, https://huggingface.co/Qwen/Qwen-Image-Edit-2511, https://huggingface.co/dx8152/Qwen-Edit-2509-Multiple-angles (all snippet, CLAIM).
  - **Best fit for us: it runs in sd.cpp on Vulkan.** Whether it fits in 10 GB depends on GGUF quantisation. Not checked.
  - FLUX.1-Kontext-dev: the licence is BFL's non-commercial dev licence. Check it against our allowlist before use (not re-read here).
- **PhotoMaker v2 / InstantID / PuLID** depend on **InsightFace models, which are non-commercial research only** (buffalo_l, antelopev2; commercial licence by request). Avoid.
  Source: https://github.com/deepinsight/insightface/blob/master/python-package/README.md (snippet).

**Inputs to prepare for FaceBuilder, MetahumanModeler or Headshot:**
- Front, left three-quarter, right three-quarter and profile
- Neutral expression, mouth closed, eyes open with sclera visible
- Flat, even, front-facing light
- Hair off the forehead, ears and face edges
- No glasses
- Same focal length feel across views (long lens, little perspective distortion)
- High resolution

This matches Epic's own input rules for meshes (sclera showing, flat symmetric light).

**Risk that a generated face resembles a real person:**
- Diffusion models reproduce identities that appear often in training data, especially celebrities. Researchers detect this with face-recognition (ArcFace) similarity against reference identities.
  Sources: https://arxiv.org/pdf/2606.20155 (NAMESAKES, 2026, snippet, MEASURED in the paper); https://stable-diffusion-art.com/realistic-people/ (snippet, CLAIM).
- Practical checks:
  - Never put a person's name or "looks like" in a prompt.
  - Avoid "beautiful/famous/actor" style tokens that pull toward prototypes.
  - Have a human run a reverse-image search (Google Lens / TinEye) on the approved portrait.
  - A face-embedding check against a celebrity set would need a face-recognition model; the common ones (InsightFace) are non-commercial, so that needs its own licence check.
  - Keep a record of prompt and seed per character.
- Licence: the MetaHuman licence allows use "in workflows that incorporate artificial intelligence technology", but not "to train or enhance the AI models themselves". **So do not fine-tune a LoRA on MetaHuman renders.** Using a render as a one-off conditioning image is a workflow use; that is our reading, confirm if in doubt.
  Source: https://www.cgchannel.com/2025/06/you-can-now-sell-metahumans-or-use-them-in-unity-or-godot/, 4 June 2025, opened, secondary reporting of the licence.

---

## 6. Routes ranked for us (Windows, RX 6700, no NVIDIA, no iPhone depth)

1. **Free, in-engine, scriptable, no new money.** Start from the nearest preset. Use the 5.8 Python face sculpt: landmarks + `Get/SetFaceModelCoefficients`. Iterate: render at the portrait's framing → compare with the portrait (side by side, or 2D landmarks) → adjust.
   - Stays inside the MetaHuman face space and needs no third-party licence.
   - Likeness is limited by how well we can judge or measure. Skin via tone/texture index.
2. **One subscription month (money → Jafar).** Image lane makes front + 3/4 + profile with Qwen-Image-Edit from the approved portrait → KeenTools FaceBuilder (pins, 4–8 views) → head OBJ plus MetaHuman-UV texture → **From Custom Mesh** (5.8) or Identity → cloud auto-rig → apply FaceBuilder's texture through Texture Override.
   - About $16–20 per month, commercial use allowed.
3. **$59 one-off (money → Jafar).** MetahumanModeler: single or multi-view portrait → MetaHuman-topology head → **template conform**, which avoids the any-topology re-fit.
   - The vendor admits accuracy limits.
   - Windows only; Blender 4.5 at most.
4. **$498 (money → Jafar).** CC5 + Headshot 3.1 → CC5 head → From Custom Mesh. The most capable single-photo tool found, but the most expensive and it adds a second character system.
- **Excluded:** Hunyuan3D (territory), FaceLift, DECA/EMOCA/SMIRK, PanoHead (non-commercial), InsightFace-based ID adapters (non-commercial), MetaHuman Identity from footage (needs depth hardware).
- **Watch:** the cloud auto-rig/texture 300 s timeout outside the US (Aug 2026 thread). Our existing scripted rig/texture calls may hit it.
