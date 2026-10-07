> **Helper evidence note** for the frontier AI research of 7 October 2026, kept as written by a read-only helper given the problem (METHOD-BRIEF.md). Corrections found on checking are in ../SOURCES.md; where they differ, the numbered sections govern.

# Strand C: generated worlds, 3D assets and garments (July to October 2026)

Research helper report, 7 October 2026. About 30 minutes. Sources: the arXiv API (titles, abstracts, and for ten garment papers the full PDF text fetched from export.arxiv.org and searched), GitHub README and LICENCE files read directly, the Unreal Engine 5.8 release notes on dev.epicgames.com (read through the fetch tool's summariser, which quotes lines), Wikipedia, and web-search summaries.

Marks: [SHOWN] evidence I read (code, weights page, licence text, or a paper's own reported experiment, which is still the authors' report); [CLAIMED] announced only; [ABS] arXiv abstract read (authors' claim); [SS] search summary only, a lead and not evidence; UNREACHED; [I] my inference.

UNREACHED this session: every github.io project page I tried (PatternGSL, TailorCoPilot, Stitched Embeddings, OmniFabric, Procedura, WorldClaw), docs.worldlabs.ai, app.cinevva.com, Hugging Face, and vendor sites (Meshy, Tripo, Runway, Style3D, CLO). Nothing is concluded from them; where a claim rests only on a search summary it is marked [SS].

---

## Bottom line

1. **Clothing (problem 3): nothing found from July to October 2026 has shown a tailored jacket with a notched lapel, by any AI tool, research or commercial.** The research generators sit on GarmentCode's design space. I read its configuration file: it has a "SimpleLapel" collar part but no front opening or closure. The newest papers either never mention jackets or lapels, or name open-front garments as future work. [SHOWN] No AI shortcut exists to wait for.
2. **World models (problem 2) cannot supply the street.** The interactive ones (Genie 3, Runway GWM Worlds 2, ByteDance's reported model) output video, not geometry. The ones that output splats and meshes are barred for LEDGER. HY-World 2.x (Tencent) excludes the UK and EU by licence. Lyra 2.0 (NVIDIA) weights are research-only. Marble and Atlas (World Labs) are paid cloud services with unread terms. Their geometry and baked light are far below the Hook sheet. [SHOWN for the licences; I for quality]
3. **Image-to-3D for props** is better than a year ago, but nothing usable runs on this PC, and every candidate has a problem for LEDGER. Open models need NVIDIA and 24 GB or more, depend on a non-commercial renderer (nvdiffrast), and are trained on Objaverse-XL's Sketchfab subset, which contains items whose authors later set NoAI. The hosted services (Meshy 7, Tripo P2.0) cost money and do not disclose their training data.
4. **The one family that fits LEDGER today is language models writing procedural code:** Blender programs for hard-surface props (Nova3D, Procedura) and material programs (MatLoom, Material Apprentice). It needs no new model or GPU and adds no new licence, and its output is text. These are still the authors' reports on their own benchmarks, and none shows photoreal results at the KCD2 bar.
5. **For the way of working (problem 5)**, two benchmarks bear on how the agents work. CraftBench-UE: agents finish Unreal tasks far more often in C++ than in Blueprint. WorldAuditBench: frontier agents found 6.6 to 42.3% of planted faults in 3D worlds, against 83.4% for humans, which bears directly on the "fresh reviewer finds visible faults" gate. UE 5.8 ships an experimental MCP plugin.

---

## 1. World models and generated 3D scenes

### 1a. Interactive video world models (no geometry)

| Item | Who / date | What | Mark |
|---|---|---|---|
| Genie 3 / Project Genie | Google DeepMind. Project Genie released 29 Jan 2026 for AI Ultra; Street View-based street simulation reported 19 May 2026; global AI Ultra on 27 May 2026 (background, before July) | Website access to Genie 3; sessions capped at 60 s | [SHOWN] dates from Wikipedia; no Genie 4 found |
| Runway GWM Worlds 2 | Runway, 3 Sep 2026 | Real-time 720p/24 fps video with 48 kHz audio, text actions ("WorldPrompt"), multiplayer demo; research preview behind a contact form; no 3D export mentioned | [SS] (runway.com UNREACHED) |
| ByteDance real-time world model | Reported by Bloomberg, relayed 8 Sep 2026; launch "as early as October" | Built on Seedance, cloud-rendered for Pico headsets, about 50 ms latency | [SS], anonymous sourcing |
| DreamX-World 1.0 | AMAP/DreamX team, arXiv 15 Jun 2026 (background) | Interactive text/image-to-video world model; up to 16 FPS on **eight RTX 5090s** | [ABS] |

LEDGER angle: none. These produce pixels in the cloud, with nothing that becomes Unreal content. They cannot run on an RX 6700. The game must stay a game rendered by Unreal. Possibly worth watching as a future way to show friends a "concept walk" [I], but it would not meet the Meridian Test.

### 1b. Generators that output splats or meshes

**HY-World 2.0 / 2.1 (Tencent Hunyuan).**
- Report and first code on 16 Apr 2026. World-generation code and WorldStereo 2.0 weights on 18 May. The README notes "[July, 2026] Update HY World 2.1", pointing to the hosted product. [SHOWN] README.
- Input is text, an image, multi-view images or video. Output is 3DGS, mesh or point cloud. The README claims "directly importable into Unity / Unreal Engine / Isaac". [SHOWN, as the authors' claim]
- Size: HY-Pano 2.0 is about 80B parameters and WorldStereo 2.0 about 17B; CUDA 12.8; multi-GPU scripts. [SHOWN via the page summariser]
- **Licence: the "Tencent HY-WORLD 2.0 Community License" "DOES NOT APPLY IN THE EUROPEAN UNION, UNITED KINGDOM AND SOUTH KOREA".** Clause: "You must not use, reproduce, modify, distribute, or display the Tencent HY-WORLD 2.0 Works, **Output or results** ... outside the Territory." [SHOWN] licence text.
- LEDGER: a game set in Britain and sold there (and in the EU) cannot use its output. Excluded. It also cannot run on this PC.

**NVIDIA Lyra 2.0.**
- Released 15 Apr 2026; GUI and training code on 20 Jul 2026. [SHOWN] README.
- It generates a camera walkthrough video (built on Wan 2.1), then reconstructs it into Gaussian splats and meshes. Runtime on one H100 80 GB is about 9 min per 80 frames (about 35 s with DMD). [SHOWN]
- **Licence: the code is Apache 2.0, but "Lyra 2.0 models are released under the NVIDIA Internal Scientific Research and Development Model License"**, which is research-only. [SHOWN] Web summaries saying "Apache 2.0 code + weights for commercial use" are wrong.
- LEDGER: excluded (licence and hardware).

**World Labs Marble and Atlas.**
- Marble 1.1 / 1.1 Plus came in April 2026. [SS]
- Reported exports: splats (.spz/.ply, about 2M or 500k), a collider mesh of about 100 to 200k triangles, and a "visual mesh" of about 600k textured triangles. [SS]
- Atlas, an "omni" model outputting images, video, point clouds and 3D Gaussian splats, was announced 1 Sep 2026 in partner early access. [SS]
- AMD agreed to buy World Labs for $8.2bn in stock, with closing expected by the end of 2026. [SS] Several outlets, about 1 Oct 2026.
- docs.worldlabs.ai was UNREACHED, so the terms of use and output ownership are unread.
- LEDGER: a paid cloud service, so money is Jafar's call. Baked lighting in splats conflicts with "lighting judged through the game's own camera", with night and with wet [I]. A 600k-triangle whole-world mesh is a blockout, not a KCD2-grade street [I]. The training data is undisclosed.

**Research, July to October 2026 (all [ABS], none runnable here):**
- **WorldClaw** (Tencent, 5 Aug 2026). Agents plan regions, terrain, assets and materials, then build editable textured meshes on a height field. Its GitHub repo holds only the paper link, with no code or weights. [SHOWN repo README]
- **HoloWorld** (6 Aug). Unified indoor/outdoor urban world generation.
- **OctWorld** (3 Sep, ECCV 2026). Long-range consistent video with an octree TSDF memory.
- **SpatialCrafter** (27 Aug). Image-to-scene via a 3D proxy.
- **StreetDiff** (9 Sep). Multi-view urban street panoramas, with a Street360 HDR dataset.
- **Splat-to-mesh conversion:** AnyGS2Mesh (3 Sep, feed-forward, code "upon acceptance"), MEGA (1 Oct), Manifold-GS (31 Jul), TopoSurfel (21 Aug).

**Gaussian splats in Unreal 5.8.** The 5.8 release notes, as read, have no native splat support. Third-party plugins exist: WallGS, MLSLabsRenderer-Lite, and Yandex's open-source YaGS for 5.5 to 5.7. [SS]

---

## 2. Image-to-3D and text-to-3D (props, buildings, characters)

| Item | Date | Shown / claimed | Runs on RX 6700 10 GB, Windows? | Licence for a sold game |
|---|---|---|---|---|
| **TRELLIS.2** (Microsoft), background | Dec 2025 | 4B image-to-3D with PBR, GLB out. [SHOWN] README | **No**: "An NVIDIA GPU with at least 24GB"; CUDA-only mesh tools | MIT, but **nvdiffrast is used for rendering, and its licence says "may be used ... non-commercially" only** [SHOWN]. Trained on ObjaverseXL Sketchfab [SHOWN training config] |
| **Pixal3D** (TencentARC / Tsinghua, SIGGRAPH 2026) | Paper May 2026; multi-view inference code Sep 2026 | Pixel-aligned image-to-3D with PBR; TRELLIS.2 backbone [SHOWN via page summariser; ABS] | No (CUDA, NATTEN; "low-VRAM mode", no number given) | MIT; third-party parts keep their own licences (TRELLIS.2, Direct3D-S2, nvdiffrast); trained on ObjaverseXL Sketchfab |
| **Hunyuan3D-2.1** (Tencent), background | Jun 2025 (last open weights) | Shape plus PBR texture [SHOWN] | No: "10 GB VRAM for shape ..., 21GB for texture ..., 29GB ... in total"; CUDA | **Territory excludes EU, UK, South Korea** [SHOWN] |
| Hunyuan3D 3.x | Hosted only; 3.1 on 28 Jan 2026 | [SS] | Cloud | Tencent platform terms, unread |
| **Hunyuan3D-Buffalo 1.0** | arXiv 3 Aug 2026 | Unified 3D understanding, text-to-3D, editing and part generation; trained on an 87M-sample corpus [ABS] | Paper only; the repo has no code or weights [SHOWN] | n/a |
| FILIGREE3D | 28 Sep | Image-to-3D geometry at up to 2048³ voxels, about 1 min [ABS] | Unknown, likely CUDA [I] | Unknown |
| Flow3D-Pro (DHO RL) | 1 Oct | RL fine-tuning of 3D flow matching; better geometry [ABS] | — | — |
| BTC3D | 30 Sep | Training-free detail boost for any image-to-3D pipeline [ABS] | — | — |
| ProxyBuild | 20 Sep | Text to structured, editable buildings via "mesh-anchored procedural proxies" with LLM-parsed styles [ABS] | — | — |
| Fysiverse-3D-Vision | 22 Sep | Single image to an "executable" 3D scene layout [ABS] | — | — |
| **Cyc3D** (benchmark) | 28 Aug | Across five image-to-3D systems, "closed-source feed-forward models consistently outperform open-source"; "even the strongest methods achieve cycle-stability scores below 48" [ABS] | — | — |
| **Meshy 7 / 7.1** (hosted) | 10–12 Aug and 10 Sep 2026 | Image-alignment-focused model; 7.1 adds "Ultra 4K" [SS] | Cloud | Free plan reportedly CC BY 4.0, paid plans private [SS]; training data undisclosed |
| **Tripo P2.0** (hosted) | 21 Sep 2026 (preview in Aug) | "First" native quad-mesh generation; up to 50k triangles / 25k quads; mesh edit [SS] | Cloud | Terms unread; training data undisclosed |
| Rodin Gen-2.5 (hosted), background | 26 May 2026 | 10M-polygon raw output [SS] | Cloud | Unread |
| SAM 3D Objects (Meta), background | Nov 2025; encoder weights 1 Jun 2026 | Single-image object reconstruction | CUDA [I] | SAM License (19 Nov 2025): commercial use not barred; trade-control and military exclusions; no territory exclusion found [SHOWN] |

LEDGER angle (problem 2, props):
- **Hardware.** Nothing here runs on an RX 6700 under Windows. Official AMD PyTorch wheels for Windows support RDNA3/4 only. The RX 6700 (gfx1031) needs unofficial overrides. [SS] The 3D repos also depend on CUDA-only extensions such as nvdiffrast, flash-attn, NATTEN and custom mesh kernels. [SHOWN for TRELLIS.2 and Pixal3D; I for the rest]
- **NoAI taint (decision for Jafar).** Objaverse redistributed Sketchfab models. Sketchfab added a NoAI tag in February 2023, and its CEO said Objaverse scraped "before us implementing the noai tag". [SS] So models trained on Objaverse(-XL)'s Sketchfab subset (TRELLIS.2, Pixal3D and most open models) were trained on items some of whose authors now mark NoAI. The 3 October ruling bars NoAI items "as a reference or input for making anything else". Whether a model trained on them counts is Jafar's call. [I] My reading of the ruling's spirit is that it does.
- **Money.** Meshy and Tripo are subscriptions, so they need his yes. Their training data is undisclosed, so the NoAI check cannot be done.
- **Quality against the bar.** The output is dense triangle meshes with baked or approximate PBR. Even Tripo's quads are capped at 25k. Cyc3D's own numbers say geometry is still unstable. [I] Generated props would need retopology and hand texturing to pass a gate judged against KCD2. They do not remove the hand work.

---

## 3. AI texturing and PBR materials

- **UltraTex** (19 Sep 2026; authors include Yan-Pei Cao). 2K multi-view diffusion texturing, 22 to 75 times faster inference than its baseline; G-buffer TexVerse dataset of 268k assets. Code and data said to be at its project page (UNREACHED). [ABS]
- **Tex-Zero** (28 Sep; authors include Tencent's Chunchao Guo). A native 3D texture generator **trained only on 2D images, with no 3D assets**. [ABS] Relevant to the taint question: if its image data were clean, a texturer could avoid Objaverse. [I] The image sources were not stated in the abstract.
- **OmniFabric** (24 Sep; SIGGRAPH Asia 2026). Garment texture synthesised directly in sewing-pattern UV space from one photo, removing baked lighting. [ABS] Research; code unknown.
- **MatLoom** (30 Sep). A pretrained LLM, with no fine-tuning, writes compact layered material programs (PBR channels from shared spatial expressions), then repairs and critiques them. In a blind test (30 people, 20 prompts), its renders got 59.2% of choices against 19.3% for the best diffusion baseline. [ABS]
- **Material Apprentice / "Reflecting Process Expertise in Procedural Material Generation"** (14 Jul; ECCV 2026). An LLM turns process traces mined from tutorial videos into executable **Blender material node graphs**. Five Blender artists judged that they needed fewer edits. Code is promised. [ABS]
- **GS-PI** (17 Sep). PBR Gaussian assets (title and abstract only).
- **Substance 3D Sampler**. Text-to-texture and image-to-texture in beta, powered by Firefly; Sampler 6.0 adopts OpenPBR; about $59.99 a month. [SS] Money.

LEDGER angle:
- Program-based materials run on this PC today with Claude as the model. They produce text that can live in git. They fit CLAUDE.md's "generated textures" route for anything with no free scan.
- Unproven for photoreal wet British brick and render. [I] Procedural materials usually need a scanned (Poly Haven or ambientCG) base to reach photoreal; use them for variation and wear, judged by the gate.

---

## 4. Garments (problem 3): what each tool has shown on tailored menswear

Summary first: **no tool or paper in July to October 2026 shows a tailored men's jacket or coat with a notched or rolled lapel.** Details:

| Item | Date / who | What it demonstrates on jackets, coats and lapels | Release / licence | Mark |
|---|---|---|---|---|
| **GarmentCode** (base of most of the field) | 2023–24, ETH (background) | Design space: meta, waistband, shirt, collar, sleeve, skirt, pants. The collar "component" can be Turtle, **SimpleLapel**, Hood2Panels or none, with a `lapel_standing` flag. **No front-opening or closure parameter, no facings, pockets, vents or shoulder pads** | MIT | [SHOWN] `assets/design_params/default.yaml` |
| GarmentCodeData | 2024 (background) | 115k garments: "tops, shirts, dresses, jumpsuits, skirts, pants" | — | [ABS] |
| **PatternGSL** | 23 Jun 2026 (v5), ACM TOG | Template-free pattern language; 2 to 37 panels; 99.2% draping success. Dataset generated from GarmentCodeData specs. Limitations section: "The current simulator also focuses on closed garments ... Future work includes ... **extending to open-boundary garments**" | Code promised | [SHOWN] paper text |
| **SewFusion** | 20 Sep 2026 | Autoregressive topology plus flow-matched panel geometry; +6.36% panel accuracy and +11.30% stitch accuracy on SewFactory and GCD-MM. No mention of jacket, lapel or coat in the full text | Project page (UNREACHED) | [SHOWN] text search |
| **GarmentWeaver** | 31 Aug 2026 | Schema-aware VLM pattern generation from sketch or text. No jacket, lapel or coat in the text | Unknown | [SHOWN] text search |
| **Stitched Embeddings** | 1 Jul 2026 (Pons-Moll group) | Simulation-free shared latent for 3D garment and 2D pattern; **pattern recovery from meshes**. No jacket or lapel | Project page (UNREACHED) | [SHOWN] text search |
| **Learning-based seam correspondence** | 23 Jul 2026 (Huamin Wang et al.) | Infers which edges sew to which; tested on 90 out-of-distribution garments "including coats and jackets". Stitching inference only, not design | Unknown | [SHOWN] paper text |
| **TailorCoPilot** | 26 Aug 2026, UIST 2026, Style3D Research | Agentic pattern-making on a version-controlled pattern state. Worked example: a shirt **placket** and a **single-piece collar**; tasks include a dress. Fine-tuned Qwen3-VL-8B; Gemini used for data. No jacket or lapel | Built on Style3D (commercial); no release seen | [SHOWN] paper text |
| **EASE** | 28 Jun 2026, SMI 2026 | Explicit local ease; **transfer to new body shapes without re-simulation**. "A jacket is made by cutting the front of the shirt": a centre-front cut, no lapel | "will publicly release"; built on **SMPL** (non-commercial body model unless licensed) | [SHOWN] paper text |
| NGL | Feb 2026 (background), MPI | Training-free: a large VLM describes the garment in a small language (including `open_front: yes/no`), then it is mapped to GarmentCode. Shows a multi-layer outfit with an open "jacket" layer, but on the GarmentCode bodice, so no lapel construction | "released for research use" | [SHOWN] paper text |
| EasyFashion | 16 Sep 2026 | Co-creation system from reference images, text and body photos to sewing patterns; one real production case. No jacket or lapel | Unknown | [SHOWN] text search |
| Garment Particles | 25 May 2026 (background) | 5D point-cloud pattern/3D representation. No jacket or lapel | — | [SHOWN] text search |
| OmniFabric | 24 Sep 2026 | Textures only (see §3) | — | [ABS] |
| DiT-Garment | 16 Sep 2026 | Learned garment dynamics for any pose; generalises to artist-made garments | "available for research purposes" (non-commercial) | [ABS] |
| Fashion-3DLR; DiffGI | 25 Jul and 15 Jul 2026 | Thin-shell / non-watertight garment mesh generation from sketches or text | Research | [ABS] |
| **CLO 2026.0** | 2026 | "Pattern Drafter with Auto POM & Grading" (draft from measurements); AI auto-grading; sketch on avatar | Paid | [SS] |
| **Marvelous Designer 2026.0 / 2026.1** | 2026; 2026.1 on 24 Aug 2026 | 3D Pencil, template-based rigging, fold painting, seam ripping. **No AI pattern generation in the summaries** | Paid | [SS] |
| Style3D AI | Press release 31 Aug 2026 | Vendor claims of image-to-pattern, auto-stitching and simulation; GarmageNet (SIGGRAPH Asia 2025) reports 91.41% simulation-initialisation success on 150 complex patterns | Paid | [SS] |
| **Unreal 5.8 Chaos Cloth** | Jun 2026 | "Enabled non-destructive updates and round-trip editing with CLO/Marvelous Designer"; USD cloth attributes; "procedural interactions between layers (skin, muscle, garment)" | Engine | [SHOWN] via the release-notes page summariser |
| FreeSewing **Jaeger** / Carlton | (existing) | "A FreeSewing pattern for a sport coat style jacket" (Jaeger); Carlton is a coat | MIT | [SHOWN] README |

LEDGER angle (problem 3):
- **The AI field does not cover this garment yet.** The learned generators inherit GarmentCode's closed-front bodice. A jacket's defining structure (open front, facing, undercollar, roll line, notched lapel, canvas or interfacing, shoulder pad) is outside every dataset I could check. [SHOWN for GarmentCode and PatternGSL; I for the rest of the field]
- **The pattern itself is not the missing piece.** An MIT-licensed sport-coat pattern with a lapel already exists (FreeSewing Jaeger), and LEDGER has tried FreeSewing patterns. [I] The failure is more likely in construction and simulation: lapel roll, stiffness of fused panels, the undercollar, and pressing and shaping. Or the method is wrong: game studios typically take a tailored jacket from MD/CLO into sculpting, retopology and baking, with the lapel modelled and skinned, not simulated. CLAUDE.md requires checking that method with dated sources before another try ("research the method before the symptom"). This is outside my strand and is flagged, not concluded.
- **Fitting to Ron, Darren, Sheila and the three builds.** EASE shows ease-preserving transfer to new body shapes without re-simulation (research code to come; SMPL-based, so it would need porting to the MetaHuman body). Unreal 5.8's CLO/MD round-trip helps the existing Chaos cloth route. Nothing found fits garments to MetaHumans automatically. [SHOWN / I]
- **Money.** CLO, Marvelous Designer and Style3D are paid, and CLAUDE.md says no purchases for clothes.
- **Hardware.** None of the research code runs on this PC: CUDA, plus NVIDIA Warp in OmniFabric and EasyFashion. [SHOWN references; I]

---

## 4b. Other surprising things: language models and agents building assets and worlds

- **Nova3D** (22 Jul 2026). Generates assets as **executable Blender source code**. 54/54 items valid; 51/52 numeric and count constraints met (best baseline 11/52); 59 joints at 98.3% validity. On shape quality it is "second only to the strongest mesh-native model", "while conceding texture realism to baked-PBR systems". [ABS]
- **Procedura** (26 Aug). An LLM agent writes an object as a parametric assembly with typed "mates", checked by compile, mate and connectivity tests, then a vision critic. It reports the sharpest edges and wins on hard-surface benchmarks. [ABS]
- **3DHarnessBench** (6 Sep). Frontier VLMs recovering geometry as Blender Python, including through Blender MCP. Results "improve significantly with richer function call access", and are "strongly model-dependent". [ABS]
- **Thinking in Blender / SEIG** (1 Jun, background). A VLM rebuilds a photo as a staged Blender program (geometry, then materials, composition and light). [ABS]
- **Code2Games** (4 Oct). Builds a Blender world, then adapts it to UE5 using compile, runtime and gameplay-test feedback. [ABS] Its README uses a Qwen3-VL-plus API and Hunyuan3D-2.1 (territory-excluded), and **the repo has no LICENSE file (404), so no licence is granted**. [SHOWN]
- **EnvDreamer** (3 Oct; Torralba, MIT CSAIL). LLMs and VLMs generate validated UE5 environments; it releases EnvDreamer-20k. Aimed at robot training. [ABS]
- **CraftBench-UE** (19 Sep). 70 Unreal tasks for agents. **C++ completion beat Blueprint by 30.0 and 42.9 percentage points**. Of Blueprint submissions that passed asset checks, 42.2% and 50.0% failed runtime assertions. [ABS]
- **WorldAuditBench** (30 Sep). 213 planted faults (floating objects, walk-through walls and the like) in UE5 and Three.js worlds. Five frontier models found **6.6 to 42.3%**; humans found 83.4%. [ABS]
- **Unreal 5.8.** "a new experimental MCP (Model Context Protocol) plugin for the Unreal Editor", plus "an assistant toolset for animation features". [SHOWN] Release notes, via the summariser.
- **Blender MCP.** Community MCP servers for Blender exist; I saw no official Blender Foundation server. [SS]

LEDGER angle:
- **Problem 2, props and kits.** LLM-as-procedural-modeller is the only generation method found that runs on this PC with what LEDGER already has: Claude, Blender and the Unreal 5.8 MCP. It adds no model licence and no dataset taint beyond Claude itself. It turns "made by its plan, from dimensions" into code that can be reviewed and versioned as text. [I] It suits hard-surface street furniture (bollards, railings, lamp posts, bins, shopfront frames, sash windows). The papers concede texture realism, so materials should come from scans or the gate. Nothing shows KCD2-grade results.
- **Problem 5.**
  - CraftBench-UE supports having agents write gameplay in C++ rather than Blueprint where there is a choice. [I]
  - WorldAuditBench says an AI reviewer alone misses most visible faults. [I] The "fresh reviewer checks every frame" gate should get fixed checklists, planted-fault tests, and close-up captures of known risk spots, not open-ended looking. That is a suggestion, not a ruling.

---

## 5. Can it run on this PC? (AMD RX 6700 10 GB, Windows, no CUDA)

| Family | Verdict |
|---|---|
| Video world models (Genie 3, GWM Worlds 2, DreamX) | Cloud only; DreamX needs eight RTX 5090s [ABS] |
| HY-World 2.x | No: CUDA 12.8; 80B and 17B models; multi-GPU [SHOWN] |
| Lyra 2.0 | No: H100 80 GB timings [SHOWN] |
| TRELLIS.2, Pixal3D, Hunyuan3D-2.1 | No: NVIDIA ≥24 GB (TRELLIS.2); 29 GB for full Hunyuan3D-2.1; CUDA-only extensions [SHOWN] |
| Garment research code | No: CUDA and NVIDIA Warp [I, from cited dependencies] |
| LLM-written Blender or Unreal code (Nova3D-style, MatLoom-style) | **Yes**: the model is Claude via the subscription; Blender and Unreal run locally |
| AMD route generally | Official AMD PyTorch wheels for Windows are RDNA3/4 only; the RX 6700 (gfx1031) needs unofficial overrides [SS] |

## 6. Licence summary for a sold game (Jafar in Switzerland, game set in and sold to Britain)

| Item | Commercial? | Territory | Dataset / other |
|---|---|---|---|
| HY-World 2.0 | Yes, inside the Territory only | **Excludes EU, UK, South Korea, including use of Output** | Over 1M MAU needs a Tencent licence |
| Hunyuan3D-2.1 | Same pattern | **Excludes EU, UK, South Korea** | — |
| Lyra 2.0 weights | **No** (research-only model licence) | — | Built on Wan 2.1 |
| TRELLIS.2 | MIT | — | nvdiffrast is **non-commercial**; Objaverse-XL Sketchfab training data (NoAI question) |
| Pixal3D | MIT | — | Same dependencies and data as TRELLIS.2 |
| SAM 3D Objects | SAM License: commercial not barred | Trade controls | Training data not checked |
| GarmentCode, FreeSewing | MIT | — | — |
| NGL, DiT-Garment code | **Research use only** | — | — |
| EASE | Unreleased | — | **SMPL** body model (non-commercial without a licence) |
| Code2Games | **No licence file** | — | Uses territory-excluded Hunyuan3D-2.1 |
| Meshy, Tripo, Rodin, Marble, Atlas, Runway | Per paid terms (UNREACHED) | Unread | Training data undisclosed, so the NoAI check is impossible |

## 7. Unverified names

- "GPT-6 Astra" appears in one search result: a 3D-tool vendor's blog (blog.neural4d.com) claiming release on 3 Sep 2026. I could not verify it from any primary source (openai.com is unreachable). Treat it as unverified.
- "GPT-6.1 Sol": not encountered in this strand.

## 8. What I would put to the builder (nothing here is decided)

1. Do not pursue world models or splat scenes for Quay Street. They are excluded by licence (HY-World, Lyra), by money and unread terms (Marble, Atlas), by hardware, and by the bar. [I]
2. **A decision for Jafar (licence):** do models trained on Objaverse / Objaverse-XL Sketchfab data, which includes items now tagged NoAI, fall under the 3 October NoAI ruling? Recommendation: treat them as excluded. It is consistent with "not as a reference or input", and nothing they make would pass the bar without hand work anyway. [I]
3. Trial LLM-written procedural assets in Blender for one hard-surface street prop, and LLM-written material programs as variation layers over scanned bases, judged by the existing gate. It needs no new spend or licence. [I]
4. Clothing: stop waiting for AI tailoring. It has not been shown, and the research field's data cannot express a lapel. Run the "method before symptom" research on how professional game pipelines build a tailored jacket (MD/CLO, sculpt, retopology, bake; lapel modelled, not simulated) before any further attempt, as the rules require. [I]
