Method researched: TARGET-PROPS-DRESSING-2026-11-17.md

# Target: the image-to-3D lab test, as Kiln's props module (17 Nov 2026)

What the test makes, with what, judged how, and what it costs; not the build. For waiting item 11, production/orders/2026-11-16.md section 3. Marks: **R** read in full today (17 Nov), **I** inference, **U** unverified, **J** judgement (no source sets it). Nothing was downloaded, installed or run on this card. Revised the same day for review fixes F1 to F5 (reviews/TARGET-IMAGE-TO-3D-PROPS-REVIEW-2026-11-17.md).

**Questions answered.**
1. Which props the test uses, and why.
2. Which tools could make them: weights licence at source, allowlist status, memory against a 10 GB AMD card.
3. The judge first: references, camera views and distances, budgets, pass bar.
4. The professional method from generated mesh to game prop.
5. How Kingdom Come II and Mafia make such props.
6. Hours, and what is unverified.

**Rulings that bound it.** 22 Sep: image-to-3D waits until hand-made props are the bottleneck (RULINGS, the look and the street). This test is the measurement that answers that ruling, so nothing it makes is adopted for production on its own result (**J**). 13 Nov, authored breadth (RULINGS line 6): "Generation is welcome when it carries out a plan"; ruled out are "things that exist only because a generator could make them"; the test for any piece is "can we point to its spec and its check?" Each prop below therefore names its spec and its check, and nothing outside that list is generated. 13 and 14 Nov: Kiln serves LEDGER, at most 15% of weekly usage; each module's judge comes first (references, camera coverage, budgets), then props. 24 Sep: a new tool enters only by a record naming its weights licence. 16 Sep: nothing bought for the street, so Meshy and Tripo (allowlisted on paid tiers only) are closed without his ruling.

## 1. The props, and why

From TARGET-PROPS-DRESSING-2026-11-17.md (its line numbers).

Spec and check for every row: **spec** = the props target line named (place, count, the period table at its lines 60-71, the content rules at lines 73-77) plus the reference photographs and true size gathered in section 3; **check** = section 3's mechanical list and pass bar items 1-6, plus the props target's checks 2 (repetition), 3 (period) and 4 (grounding).

| # | Prop (spec) | Kind (budget) | Why it is in the test | Comparator (the "hand-made or Megascans" arm) |
|---|---|---|---|---|
| A | Cast-iron mooring bollard, quay edge (line 22: "along the edge", own make) | medium prop | Own make only; a curved casting, the shape hand modelling does worst and generation claims best (**I**). Already in the never-run batch tools/meshgen/specs/props-trellis-01.json as `prop_mooring_bollard` | Our own Blender-made bollard on the same budget (the hand arm, section 6 stage 5) |
| B | Wooden fish box, one of a stack of three to six distinct pieces (line 10: one stack at the shopfront, own make) | medium prop (stacks by instancing) | Own make only; worn wood with nailed slats; the stack rule (three to six distinct pieces) tests whether seeds give variety for free (**I**) | Megascans Wooden Storage Box, 0.3 x 0.5 x 0.06 m, https://www.fab.com/listings/53a6cf14-0cf5-46d0-b90b-71134b7c490e (props target, read 17 Nov there), and Poly Haven wooden_crate_01 (held, CC0) |
| C | Galvanised dustbin (line 14: 2 to 4 in the alley and yard; never a wheeled bin, period table) | medium prop | The control: a hand-made one already stands in the scene (E13), so generated and hand-made sit side by side at once | The scene's dustbin (E13) |

Left out: milk crates and bottle crates (canon question open, props target lines 75-76; the 9 Nov list's "bottle crate" is dropped for this reason, **J**); bin bags and the net (soft, made by cloth bake, not image-to-3D); newspaper bundles (paper thickness and our own print; small prop, a later round).

## 2. Candidate tools

| Tool | Weights licence (at source) | On the allowlist? | Runs on the RX 6700 10 GB, Windows? |
|---|---|---|---|
| **TRELLIS.2-4B** (Microsoft), image to textured GLB | "This model and code are released under the MIT License" (https://github.com/microsoft/TRELLIS.2, **R**; model card "License: mit", https://huggingface.co/microsoft/TRELLIS.2-4B, **R**). Training: Objaverse-XL's Sketchfab subset (README's training commands, **R**) | **Yes**, line 5 "TRELLIS/TRELLIS 2 (MIT)". But see its helpers below, and the training-data block | **Not as published:** "An NVIDIA GPU with at least 24GB of memory", "tested only on Linux" (README, **R**) |
| **trellis.cpp** (Piotr Wilkin), a C++/GGML port of TRELLIS.2 with Vulkan, ROCm and CUDA builds | Code: "MIT License", "Copyright (c) 2026 Piotr Wilkin" (https://raw.githubusercontent.com/pwilkin/trellis.cpp/main/LICENSE, **R**). Runs the TRELLIS.2 weights plus two helper models: **DINOv3 ViT-L/16** ("License: dinov3-license", https://huggingface.co/timm/vit_large_patch16_dinov3.lvd1689m, **R**) and **BiRefNet** ("License: mit", trained on DIS-TR, https://huggingface.co/ZhengPeng7/BiRefNet, **R**) | Code: no (tool code, needs the decision record, as FoldCraft got in line 10). BiRefNet: MIT, not named, needs the record. **DINOv3: no, and it needs his yes** (stopped there on 24 Sep, clothing-pipeline/TRIED-2026-09-24.md lines 90-94) | **Maybe, via Vulkan (U).** Its getting-started page: "AMD / Intel / everything else → Vulkan, which is self-contained"; ROCm opt-in (https://github.com/pwilkin/trellis.cpp/blob/main/docs/getting-started.md, **R**). AMD's HIP SDK 7.2.0 table marks the RX 6700 (gfx1031) "Unsupported" for Windows ROCm (https://rocm.docs.amd.com/projects/install-on-windows/en/latest/reference/system-requirements.html, page dated 2026-07-31, **R**), so ROCm is out and Vulkan is the only route. Memory: "The 1024 cascade runs on a 16 GB card" (README, **R**); no figure for res 512; an Apple M5 res-512 run peaked at 5.6 GB of shared memory (README, **R**, not card memory); quantised weights "q8 ~9.5 GB", "q4 ~6 GB" on disk (getting-started, **R**). So res 512 with q4 or q8 on 10 GB is plausible, unproven (**U**). **The 24 Sep note's "prebuilt Windows Vulkan, res 512 fits about 6 GB" (TRIED-2026-09-24 line 90) names no source and this pass could not reproduce it:** no memory figure for res 512 is published, and no Windows Vulkan archive is among the visible v0.8.1 files. It is not evidence. The full weights download is about 16.5 GB, its folder settable to another drive (`--models-dir`, **R**). Latest release v0.8.1, 25 Sep; its visible Windows files are cuda, cuda12, rocm and the Studio portable, with three files hidden, so a Windows Vulkan command-line archive is **U** (https://github.com/pwilkin/trellis.cpp/releases, **R**) |
| **Pixal3D** (TencentARC), a TRELLIS.2 fine-tune, runs in trellis.cpp v0.8.0+ | MIT, third-party parts keep their own licences (frontier-ai-uses/notes/HC-worlds-3d-garments.md line 76, 2026-10, not re-read today) | No | Same as trellis.cpp; same DINOv3 and training data |
| **TripoSR** (Stability and Tripo, 2024) | "released under the MIT license, which includes the source code, pretrained models" (https://github.com/VAST-AI-Research/TripoSR, **R**) | No (MIT kind; needs the record and, per the brief, his yes) | "about 6GB VRAM"; PyTorch; CUDA "if available" (README, **R**). On AMD under Windows only through DirectML or similar (**U**). Vertex colours, or a baked texture with `--bake-texture`. Older and coarser than TRELLIS.2 (**I**) |
| **Hunyuan3D 2.1** | Territory "excluding the territory of the European Union, United Kingdom and South Korea"; §5(c) bars use of Output outside it (https://raw.githubusercontent.com/Tencent-Hunyuan/Hunyuan3D-2.1/main/LICENSE, release 13 June 2025, **R**) | **NEVER SHIP** (allowlist never-ship 3) | Not considered |
| Meshy, Tripo (hosted) | Paid plans "Private & Customer owned" (Meshy; N09-13, 8 Nov) | Paid tiers only | Cloud; a purchase, closed by 16 Sep |
| Claude-written Blender (no generator): the blender-game-skills skill (MIT, read 11 Nov through a summariser, tool-tests-2026-11/BLENDER-GAME-SKILLS-2026-11-11.md) or our own art-recipes scripts | No model weights | Kind allowed; skill's raw LICENSE unread (**U**) | **Yes**: Blender 5.2 on F:, today |

**Licence notes the record must carry.**
- nvdiffrast's non-commercial licence (HC note) belongs to the Python TRELLIS.2; trellis.cpp states it is "all in native C++/GGML with no Python at runtime" (README, **R**). Whether any of its ported code derives from nvdiffrast was not checked in the code (**U**). FlexiCubes, which the shape decoder uses, is "made available under the Apache License 2.0" (https://github.com/nv-tlabs/FlexiCubes, **R**).
- DINOv3 License (last updated 19 Aug 2025, copy held at F:/LedgerTools/trellis/licences/dinov3-LICENSE.md, **R** today): worldwide royalty-free use; trade-control and military bars; an indemnity to Meta (§5b); Meta may change the terms "effective immediately" (§8). Nothing in it bars commercial use of outputs (**I**). It is a tool, never shipped; its outputs would be.
- **Training data: a block before any generator run.** Objaverse-XL's Sketchfab subset holds items whose authors later set NoAI (HC note line 93; frontier-ai-uses/3-LEGAL.md line 84). The 3 Oct ruling bars NoAI-marked content "even as a reference", with only Epic's own content excepted. Whether a model trained on such items counts is his call. The allowlist names TRELLIS 2 regardless, but **no generator runs (stage 2 onward) until he has answered this question**, alongside DINOv3. The same applies to Pixal3D, and to TripoSR whose training data is unread.
- Input pictures: every input image needs its own licence tag (allowlist PROCESS 1). **Only CC0 or public-domain photographs, or our own Blender renders.** No generated image is an input: an image model's output would feed a generator, and no image model is on the allowlist for this.

**Recommendation (J).** TRELLIS.2 weights through trellis.cpp's command line (never the Studio app, which needs clicks), Vulkan, res 512, q8 weights first, on F: only. It is the only allowlisted generator that might run here. It needs one item on his page with two answers, both required before stage 2: (1) DINOv3 as a tool whose outputs only are used; (2) whether a model trained on Objaverse-XL's Sketchfab subset is allowed under the 3 Oct ruling. If either is no or unanswered, the test runs only the Claude-written Blender arm against the comparators and reports "generator not run: licence".

## 3. The judge first (Kiln's props judge, shared with later modules)

Kept outside the tool, as clothing's judge is (TOOLCHAIN-CORE-DESIGN-2026-11-13.md line 30): a folder of references, cameras, bars and comparators the maker cannot change (**J**: proposed F:/LedgerTools/tool-dev/judge-props).

**References.** For each prop, at least two dated photographs, 1985-1995, British; production/reference holds none on bins, crates or quay fittings (props target, "unreached"). Leads: Picture Sheffield t13140 and t13138 for fish trade (FISHMONGER, 3 Oct); Lydney Harbour and Gowanus bollard scans as shape references only, licence unseen (props target line 53). Real sizes come from the photographs or a source, since TRELLIS output is "normalised into a unit cube" with no scale (props-trellis-01.json comment, 1 Sep).

**Camera views and distances.** The street camera sits 3.1 m behind Tom with an 86-degree lens (RULINGS 28 Oct); HILL-METHODS uses about 64 degrees across 2,560 px. Which one is horizontal on the built camera is **U**, so both are given. A 0.5 m prop at 2,560 px wide (this note's arithmetic):

| Distance | at 64 degrees | at 86 degrees | Where |
|---|---|---|---|
| 1.5 m | 683 px | 458 px | doorstep and shopfront close views (props target check 2: 1 to 3 m) |
| 3 m | 341 px | 229 px | Tom passing, hook camera |
| 10 m | 102 px | 69 px | across the street, reverse view |
| 30 m | 34 px | 23 px | the quay end from the hook camera |

The judge's captures: three fixed, named cameras per prop, **close (1.5 m, eye height)**, **street (3 m, from the street camera)** and **reverse (10 m)**, each wet by day and at night, at High ("scalability 2"), 2,560 x 1,440. Also a turntable of eight level views for silhouette and holes (clothing's judge uses eight level cameras, KILN-ROUND1 round 7). Two extra renders of the close camera serve item 2.

**Budgets** (production/specs/asset-budgets.json `prop_medium`, from pre-production/4-BUDGETS.md line 165, **R**): LOD0 at most 5,000 triangles; 3 LODs, each about half the last; at most 3 materials; textures at most 1024² or the shared trim; at most 4 MB per unique asset; simple collision, at most 10 hulls, most one box. Nanite off (budgets heading). Kit texel density is 512 px/m (4-BUDGETS line 150). A 0.5 m prop at 1.5 m shows about 900 to 1,370 px per metre on screen, so 1024² is soft only in the closest view (**I**).

**Pass bar** (each prop; generated and comparator judged the same way):
1. Mechanical, before any eye: manifold and watertight; non-overlapping UVs; separate base colour, roughness, metallic and normal maps; collision present; true scale within 3% of the reference size (**J**); triangles, LODs, materials and texture size within the budget above. The first four are the "production-ready" list of arXiv 2604.23629 (content-mass-and-judgement/SUMMARY.md lines 45-61, read in full 19 Sep).
2. No light baked into the base colour. Judged on the **close (1.5 m)** camera, rendered twice under a single directional light (sky and ambient off), both renders at 45 degrees elevation: once from the camera's left (azimuth -90 degrees) and once from its right (+90 degrees). It fails if any dark or bright patch on a face stays put between the two renders where the geometry gives no reason for it. A crevice may stay dark; a painted shadow on a flat face fails. The reviewer writes pass or fail and names any patch found (**J**).
3. Beside its comparator in the three named captures (close, street, reverse): one fresh Sonnet reviewer, one round (RULINGS 3 Nov, small piece). For **each view separately** the reviewer writes a verdict of "better", "equal" or "worse" for the generated prop, and lists any fault: melted edges, closed gaps, fused slats, wrong period shape, CG-clean. Pass needs "better" or "equal" written in all three views and no new fault in any. A missing view verdict counts as a fail.
4. Period: matches its photographs; no brand marks, no wheeled bin, no plastic where wood or iron is right (props target, period table).
5. **The bottleneck measure:** hands-on hours from input picture to an imported, judged prop, against the hand arm's hours on the same prop. The generated route is worth adopting only if it passes items 1-4 on at least two of the three props at no more than half the hand arm's hours (**J**, in the manner of clothing's "time at most 1.5 times Marvelous's", KILN-ROUND1 round 4). Machine time is logged apart.
6. Then the nightly packaged walk (CLAUDE.md).

Compared with the Hook sheet and KCD2 frames for wear only; neither sets a number.

## 4. The professional method, generated mesh to game prop

| Step | Method | Source |
|---|---|---|
| Generate | Background removal (BiRefNet), DINOv3 image features, three flow stages, FlexiCubes mesh, then weld, hole fill, remesh, quadric decimation to a face budget (default 150K at res 512), xatlas unwrap, PBR bake from the voxel field to a 1024² atlas at res 512 | trellis.cpp README, "Pipeline" and flags (**R**; the 24 Sep copy at F:/LedgerTools/trellis/README-trellis.cpp.md agrees) |
| Pick | Several seeds per input; the judge's turntable picks one per prop, or three to six distinct ones for the fish-box stack | **J** |
| Retopology | Hard props: decimate, not voxel or quad remesh. The manual: "Reducing the face count of a mesh that otherwise has no problems with its geometry. It's better to use Decimate"; voxel remesh is for "overly dense or messy geometry, such as from a sculpt or a 3D scan". Hand retopology only where a mesh deforms | Blender manual, Remeshing page (bundled copy F:/LedgerTools/blender_mcp/mcp/blmcp/data/manual/modeling/meshes/retopology.rst, **R**; the online 5.3 page returned navigation only) |
| UVs | Re-unwrap the game mesh (the generated atlas is for the dense mesh); margins round islands "to avoid discontinuities at UV seams, due to texture filtering and mip-mapping" | Blender manual, Render Baking, Margin (bundled baking.rst, **R**) |
| Bake | High (generated, dense) to low (game mesh) by "Selected to Active", rays cast "from the low-poly object inwards towards the high-poly object", with a cage or extrusion; tangent-space normals, "the right choice in most cases"; base colour and roughness baked from the generated maps | same, **R** |
| Wear and variation | Our kit master with the seeded grime layer (21 Sep ruling, D53); KCD2-style hue and blend-map variation per instance (section 5) | RULINGS; CLOSE-RANGE via asset-plan/3 line 53 |
| LODs | Unreal's automatic LODs: quadric simplification "until it reaches the requested target number of triangles"; LOD groups are "the preferred way"; the SmallProp preset "NumLODs=4,LODPercentTriangles=50,PixelError=10"; keep Auto Compute LOD Distances on | https://dev.epicgames.com/documentation/en-us/unreal-engine/static-mesh-automatic-lod-generation-in-unreal-engine (page titled 5.9, **R**) |
| Clean and measure | tools/meshgen's CLEAN stage already runs headless Blender to measure, normalise, build the LOD chain and export GLB. Its licence gate refuses any tool without a `TOOL-DECISION:` record | tools/meshgen/README.md (**R**). Reuse it; do not write a new cleaner (**J**) |

Industry: Hunyuan3D Studio (arXiv 2509.12815, 16 Sep 2025) automates "Part-level 3D Generation, Polygon Generation, Semantic UV" (abstract, **R**); its full text was read 19 Sep (content-mass SUMMARY). A paper from the same field says benchmarks "omit topology, UV, rigging, and engine import metrics" (arXiv 2604.23629, read 19 Sep), so a generator's quality claims are not evidence for this bar.

## 5. How the reference games make such props

- **Image-to-3D: none found** in either study.
- **Kingdom Come II:** barrels "all in one texture atlas using HSL and blendmap variation"; its turnip is a "modified scan" (asset-plan/3-FURNITURE-PROPS-FOOD.md line 53, CLOSE-RANGE, 3 Oct). Texture bytes in its archive: furniture median 0.7 MB, small props 0.35 MB (studies/05-visuals.md line 43, measured). The method to copy: treat the generated mesh as KCD2 treats a scan, cut down, baked to a shared atlas and varied per instance. Its numbers sit inside our 4 MB cap, so they add no further limit (**I**).
- **Mafia: The Old Country:** 35 trim sets in one library, mostly 2048² (phase5-procedural/MAFIA-KIT-2026-10-28.md line 90); kit meshes reused about 15 times in its measured street (studies/04-street-world.md, via the props target); props stop casting shadows at a quarter of their distance (studies/12-tech-budgets.md line 51). To copy: the shadow distance for props, and trims for the box and the bin where they fit.
- Neither study counted prop triangles (games-numbers/PUBLISHED-NUMBERS-2026-11-09.md line 18: "Not found"); n16-11's table may fill this.

## 6. Order and hours (all estimates, I)

| Stage | Hours |
|---|---|
| 0. Judge first: photographs, sizes, the three named cameras and turntable, bars file, comparators placed | 5 |
| 1. Decision record (trellis.cpp, BiRefNet, TRELLIS.2 weights) and his page item (DINOv3; Objaverse training data). **Stage 2 is blocked until both are answered yes** | 1 |
| 2. After both yeses: command-line build or archive and q8 weights onto F:, space check first; one res-512 run on the bollard. Two tries, then stop and report | 2 attended, plus machine time **U** |
| 3. Three props x four seeds; pick | 1 attended, 1-3 machine **U** |
| 4. Cleanup to budget (decimate, UV, bake, wear, LODs, collision, import): 3-5 per prop | 9-15 |
| 5. Hand arm on the bollard and fish box (the dustbin is held) | 6-10 |
| 6. Captures, one Sonnet review, walk, NOTEBOOK lines | 3 |
| **Total with the generator** | **27-37** |
| Without both yeses (stages 0, 1, 5, 6 and a report) | 15-19 |

Disk: the weights are 16.5 GB in full, about 9.5 GB at q8 (getting-started, **R**), on F: only. The default folder is under %LOCALAPPDATA%, so it must be set. GPU: never beside Unreal, a Kiln gate or the night jobs (memory notes). The hours count against Kiln's 15% (RULINGS 13 Nov).

## Sources read 17 Nov 2026

github.com/microsoft/TRELLIS.2 (README); huggingface.co/microsoft/TRELLIS.2-4B; github.com/pwilkin/trellis.cpp (README), its LICENSE, releases page and docs/getting-started.md; huggingface.co/timm/vit_large_patch16_dinov3.lvd1689m; huggingface.co/ZhengPeng7/BiRefNet; github.com/VAST-AI-Research/TripoSR; Hunyuan3D-2.1 LICENSE; github.com/nv-tlabs/FlexiCubes; AMD HIP SDK for Windows system requirements (7.2.0); Epic's automatic LOD page and Nanite page (5.9); arXiv 2509.12815 abstract. Local: DINOv3 licence copy and trellis.cpp README copy on F:/LedgerTools/trellis (24 Sep); Blender manual retopology.rst, remesh.rst, baking.rst (bundled); RULINGS.md (lines 6, 38, 50, 61); license-allowlist.md; orders 2026-11-09 and 2026-11-16; TARGET-PROPS-DRESSING and TARGET-HILL-CROWNS; TRIED-2026-09-24; HC-worlds-3d-garments; N09-13-CAR-COSTS; BLENDER-GAME-SKILLS; tools/meshgen README and props-trellis-01.json; 4-BUDGETS; asset-budgets.json; asset-plan/3; studies 04, 05, 12, 13; MAFIA-KIT; KILN-ROUND1; TOOLCHAIN-CORE-DESIGN; content-mass SUMMARY. CATALOGUE.md has no image-to-3D line.

## Unverified (14)

1. trellis.cpp running on the RX 6700 through Vulkan under Windows (no RDNA2 or gfx1031 run shown).
2. Card memory at res 512 with q8 or q4 weights on 10 GB. No figure is published; the M5's 5.6 GB is shared memory; the 24 Sep note's "about 6 GB" on a prebuilt Windows Vulkan build is unsourced and was not reproduced, so it is not evidence.
3. A Windows Vulkan command-line archive in v0.8.1 (three release files hidden; the Studio app needs clicks and is not used).
4. Whether any trellis.cpp code derives from nvdiffrast or another non-MIT source (code not read).
5. Generation time per run on this card.
6. Whether TRELLIS.2 output reaches this bar on worn period props (no evidence either way).
7. Light baked into TRELLIS.2's base colour.
8. TripoSR on AMD under Windows; its image encoder's licence; its training data.
9. Which camera angle (86 or 64 degrees) is the horizontal one on the built camera.
10. Period shapes: 1990 British fish boxes (wood or plastic), quay bollards, dustbins; no dated photograph in hand.
11. Input-photograph licences (none chosen yet).
12. British or 1990 fit of the Megascans Wooden Storage Box (props target).
13. blender-game-skills' raw LICENSE text.
14. Every hour figure above.

## Unreached

- wiki.polycount.com Texture_Baking: connection refused. Adobe Substance 3D Painter baking page: HTTP 403. Not used.
- docs.blender.org online retopology and baking pages: only navigation text came back, so the bundled manual copy was read instead (its exact version is not stated in the files).
- trellis.cpp v0.8.0 and v0.6.0 file lists: did not load.
- Not read this pass: Stable Fast 3D, SAM 3D Objects, Meshy and Tripo terms (Tripo's pages gave 403 on 8 Nov, N09-13).
