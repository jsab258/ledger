# Image-to-3D: the 14 open points checked, and the DINOv3 pick (17 Nov 2026)

For the image-to-3D target and its review. Web pages read 17 Nov 2026; nothing downloaded or run. Marks: confirmed, corrected, partly, needs the PC (with what to measure), open.

Reviewed 17 Nov 2026: PASS WITH FIXES, applied (reviews/REVIEW-IMAGE-TO-3D-CHECKS-2026-11-17.md).

## The 14 points

| # | Point | Result | What the sources say, or what to measure |
|---|---|---|---|
| 1 | trellis.cpp on the RX 6700 through Vulkan, Windows | Needs the PC | The trellis.cpp wiki lists prebuilt Windows binaries for Vulkan, ROCm and CUDA. Its only AMD card is a Radeon 8060S (gfx1151); no RDNA2 run is shown. Measure: one res-512 run on the bollard completes, GLB opens in Blender. |
| 2 | Card memory at res 512, q8 or q4, on 10 GB | Not found in the wiki; needs the PC | The wiki gives no memory table (README and getting-started not re-read this pass): only "the 1024 cascade runs on a 16 GB card" and a 5.6 GB peak (system RAM, not card memory) for res 512 on an Apple M5. The 24 Sep "about 6 GB" stays unsourced. Measure: peak dedicated GPU memory (Task Manager or GPU-Z log) for res 512 at q8, then q4, with nothing else on the card. |
| 3 | A Windows Vulkan command-line build in v0.8.1 | Partly | The wiki says prebuilt Windows x64 binaries cover Vulkan and gives a PowerShell installer. The v0.8.1 file list was unreached. Measure: the release's asset list shows a Windows Vulkan archive; if not, the build from source is a new hour. |
| 4 | trellis.cpp code derived from nvdiffrast or other non-MIT code | Partly | A GitHub code search for "nvdiffrast" in the repository found 7 files, all documents (ROADMAP.md and six files under docs/spec/), no source file. A lead, not proof. Measure on the PC: search the source for nvdiffrast and NVIDIA licence headers. |
| 5 | Time per run on this card | Needs the PC | Wiki, res 1024 with model load: Strix Halo Vulkan 6:09 to 12:39; RTX 5060 Ti 3:16 to 7:23; Apple M5 at res 512: 9:21. No RX 6700 figure. Measure: wall time per res-512 run, three seeds. |
| 6 | Whether output reaches the bar on worn period props | Needs the PC | No source speaks to it. The judge measures it. |
| 7 | Light baked into the base colour | Needs the PC | ComfyUI's TRELLIS.2 page lists the maps; nothing on baked lighting. Measure: pass bar item 2 (two-light test). |
| 8 | TripoSR on AMD Windows; image encoder licence; training data | Partly corrected | Paper: "The image encoder is initialized with a pre-trained vision transformer model, DINOv1" (fits ViT-B/16; checkpoint not named). facebook/dino-vitb16 is "apache-2.0". Training: "a carefully curated subset of the Objaverse" dataset "available under the CC-BY license". AMD under Windows still unverified: needs the PC (does it run on DirectML or CPU, and how long). |
| 9 | Which angle (86 or 64 degrees) is horizontal on the built camera | Needs the PC | Read the street camera's field of view and the project's aspect-ratio axis setting in the 5.8.2 editor. |
| 10 | 1990 British fish boxes, bollards, dustbins | Open | Not researched this pass (photographs, not tools). |
| 11 | Input-photograph licences | Open | None chosen yet; unchanged. |
| 12 | Megascans Wooden Storage Box fit | Open | Not re-checked. By the NoAI rule it is never fed to the generator; as a comparator it is fine. |
| 13 | blender-game-skills raw LICENSE | Open | The search did not return the repository; not fetched (web rule). |
| 14 | Every hour figure | Partly | Machine time known only from other cards (point 5). Stage 2 should add one hour if no Windows Vulkan archive exists (point 3). Attended hours remain estimates. |

Two further corrections to the target, found on the way:

- DINOv3 licence date: Meta's page is dated August 14, 2025, not 19 Aug 2025. Compare the F: copy.
- Outputs, confirmed: at res 512 the default is about 150K faces and a 1024 atlas; at res 1024 to 1536 about 300K faces and a 2048 atlas (wiki). Textures in the GLB are lossy WebP by default, PNG only in a build with TRELLIS_WEBP off. Lossy maps carry their compression into the bake. TRELLIS.2's encoder is DINOv3 (ComfyUI: TRELLIS.2 and Pixal3D "both use the same DINOv3 image encoder"); DINOv2 is not used.

## The DINOv3 pick

What the licence says (Meta's page, read at source today):
- Grant: "non-exclusive, worldwide, non-transferable and royalty-free limited license". No commercial bar is stated; the grant sets no limit by purpose beyond 1b.v.
- Outputs: named only in the "as is" disclaimer (section 3) and the litigation clause (section 5b). No obligation is placed on outputs as such.
- Derivative works: owned by the maker (5a). If the DINO Materials or "any derivative works thereof" are given to anyone, they go under this licence, with a copy, and a prominent "Built with DINOv3" notice (1b.i). Whether a mesh made with it is a derivative work is undefined; the plain reading is that a mesh is an output.
- Bars and duties: trade-control uses, including military or warfare (1b.v); credit in published research (1b.ii); obey the law (1b.iii); no reverse engineering (1b.iv).
- Burdens on him: he indemnifies Meta against third-party claims (5b); Meta may change the terms, continued use counting as agreement (8); Meta may end it on breach (6).

So: the tool is affected, the shipped meshes are not, on the plain reading. Nothing of DINOv3 ships. It stays off the allowlist until he says yes, and the training-data question (Objaverse-XL's Sketchfab subset, 3 Oct ruling) stays a separate block before any run whichever way this goes.

Alternatives checked:
- TRELLIS (version 1), TRELLIS-image-large: weights "license: mit", already on the allowlist ("TRELLIS/TRELLIS 2"); its paper: "For image conditions, we adopt visual features from DINOv2" (DINOv2 ViT-L/14 weights "apache-2.0" on the timm card). Fully permissive. But its README requires "An NVIDIA GPU with at least 16GB of memory", tested on Linux, and no port running the whole version-1 pipeline on Vulkan was found (LocalAI's TRELLIS-image-large GGUF is one decoder reused by TRELLIS.2). Not runnable here as found; same training-data question.
- TripoSR: code and weights MIT, encoder DINOv1 (Apache 2.0 checkpoint), trained on a CC-BY Objaverse subset. All licences permissive, but the same training-data question (its Objaverse subset is also from Sketchfab; per-object marks unread), off the allowlist (needs a decision record and his yes), older and coarser, and unproven on AMD under Windows.
- Stable Fast 3D: free only below US$1M annual revenue. Out.
- SAM 3D Objects: Meta's "SAM License", gated, terms not read. Out for now.
- Hunyuan3D: never ship (territory). Meshy, Tripo: paid, closed by the 16 Sep ruling; only by changing that ruling.

The one line for his page:

Let Meta's DINOv3 picture reader run on his PC as a part of TRELLIS.2, never shipped, its meshes used? A: yes, as a tool only, with "Built with DINOv3" and its licence added to the credits at no cost (recommended). B: no; the test runs the hand-made Blender arm only and reports "generator not run". C: no to DINOv3, try TripoSR instead (all licences permissive, older, coarser, unproven on this card; same training-data question, its Objaverse subset also from Sketchfab, per-object marks unread).

This alone does not start the generator: the training-data question (Objaverse-XL's Sketchfab subset, 3 Oct ruling) goes on the same page as a second one-line decision.

Reason for A: none stated on outputs, royalty-free, and TRELLIS.2's weights are the only allowlisted generator with a possible route to this card (trellis.cpp on Vulkan, unproven here; trellis.cpp and BiRefNet need a decision record). If a mesh were ever held to be a derivative work, the duty would be a copy of the DINOv3 licence plus the notice shipped with the game; option A adds both to the credits and THIRD-PARTY.md at no cost, which covers that reading. Risks: the indemnity and Meta's right to change terms, small for a tool kept out of the game. The 22 Sep ruling holds: this is the measurement, nothing is adopted on it alone.

## Sources (read 17 Nov 2026)

- trellis.cpp wiki: https://github.com/pwilkin/trellis.cpp/wiki
- DINOv3 License, Meta: https://ai.meta.com/resources/models-and-libraries/dinov3-license
- ComfyUI TRELLIS.2 tutorial: https://docs.comfy.org/tutorials/3d/trellis2
- TRELLIS paper (arXiv 2412.01506 v2): https://arxiv.org/html/2412.01506v2
- TRELLIS-image-large model card: https://huggingface.co/JeffreyXiang/TRELLIS-image-large/blob/main/README.md
- TRELLIS (version 1) README mirror: https://github.com/pb-coding/microsoft-trellis
- DINOv2 ViT-L/14 card (timm): https://huggingface.co/timm/vit_large_patch14_reg4_dinov2.lvd142m/blame/main/README.md
- LocalAI TRELLIS-image-large GGUF: https://huggingface.co/LocalAI-io/TRELLIS-image-large-GGUF
- TripoSR paper (arXiv 2403.02151): https://arxiv.org/html/2403.02151v1
- DINO ViT-B/16 card: https://huggingface.co/facebook/dino-vitb16
- SAM 3D Objects card: https://huggingface.co/facebook/sam-3d-objects
- Stable Fast 3D card: https://huggingface.co/stabilityai/stable-fast-3d
- GitHub code search, "nvdiffrast repo:pwilkin/trellis.cpp" (7 document files, no source)
- Local: the target and review, the allowlist, PROPS-LICENCE-AND-PLAN (NoAI rule), RULINGS.md.

## Unreached (never evidence)

- trellis.cpp releases and v0.8.1 file list: GitHub API refused; URL not in search results.
- trellis.cpp README and getting-started page: not in search results; the target's quotes from them not re-checked.
- LocalAI's 3D page: metadata only.
- blender-game-skills repository and LICENSE: not in search results.
- SAM 3D Objects licence text and Stable Fast 3D's full licence: not opened.
- Pixal3D's README: not opened.
