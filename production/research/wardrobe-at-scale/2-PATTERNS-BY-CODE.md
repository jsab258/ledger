# GarmentCode and other code-generated sewing patterns (research note, 1 October 2026)

A separate helper was given the problem, not a theory, and spent about thirty minutes, reading only. It read GarmentCode's code and licence files, not just its README. **D** = documented (source number). **I** = its inference. Saved by the cloud session; its own checks of the deciding licences are in SUMMARY.md.

## In brief

1. **GarmentCode cannot make any of LEDGER's tailored garments.** Its whole wardrobe is: tops (a shirt, or a fitted shirt with darts); sleeves with band or flared cuffs, and necklines; a turtleneck, a "simple lapel" and a hood; waistbands, basic trousers and seven skirt types [1, 4] (D). It has no front opening or overlap, no buttons, no pockets, no fold lines and no layers [1, 4, 5] (D): so no facings, under-collars or linings, and nothing sewn on top, such as a yoke patch. The authors list these limits themselves [4, 5] (D).
2. **Its draping simulator is non-commercial.** The pattern library is MIT [1] (D). The simulator is a modified copy of NVIDIA Warp under NVIDIA's Source Code License: use "non-commercially … for research or evaluation purposes only" [2] (D). Plain NVIDIA Warp has been Apache 2.0 since 1.6.2 (March 2025) [3] (D), but lacks the garment changes.
3. **It cannot use the AMD card.** Warp runs on the graphics card only through NVIDIA's CUDA; it also runs on the CPU under Windows, and GarmentCode falls back to the CPU without CUDA [1, 3] (D). The paper gives 30 seconds per garment on an RTX 3090 [5] (D); CPU speed not measured.
4. **Everything newer either reuses GarmentCode's garment types or is non-commercial** (section 2). No openly licensed tool that drafts a jacket with lapels was found.
5. **The pattern is not where LEDGER failed.** FreeSewing's Jaeger already drafts a real sport coat [16] (D, earlier note), more than GarmentCode can. What failed was the drape and the finishing (I). GarmentCode adds nothing for jackets and coats; at most it is a cheap source of simple, varied crowd garments (I).

## 1. GarmentCode (2023) and GarmentCodeData (2024)

**What it can make** (from the code [1]):

| Garment | Verdict |
|---|---|
| Jacket with collar and lapels | **No.** "SimpleLapel" is a flat triangle sewn to a closed neckline, not a facing turned back along a roll line (D, code). ChatGarment's fork adds an `openfront` switch that only leaves the centre seam unsewn: edges meet, no overlap, no buttons [8] (D, code compared). |
| Sleeves with cuffs | Partly: one-piece sleeve, single-layer cuffs [4] (D). No two-piece tailored sleeve (D, code). |
| Coat | Only as a long top: shirt length up to 3.5 times (D). No fastening, collar stand or pockets (D). |
| Trousers | Basic: length, width, flare, rise, darts and cuff only (D). No fly, pockets, belt loops, pleats or crease (D). |
| Donkey jacket, suit jacket, car coat | **No** (I, from the rows above). |
| Work trousers | A rough base; every detail added by hand (I). |

New garment types are written as Python programs, but holes in a piece, fold lines, layers and pieces sewn on top are limits of how the system is built [4] (D), not just missing examples.

**What it produces** [1] (D, code): the pattern as JSON (pieces, their 3D placement, seams); SVG, PNG and a printable PDF; a mesh of the flat pieces (OBJ) whose texture layout is the flat pattern; the draped mesh (OBJ) and optional USD frames. No DXF export, the usual format for importing elsewhere. A draped garment averages about 30,000 triangles [5] (D).

**Bodies.** A pattern needs about 26 body measurements in a YAML file [1] (D), which could be taken off the MetaHuman bodies (I). The SMPL body model is optional; the repository's readme says its SMPL bodies are CC BY 4.0 [1] (D, unverified). The measuring tool is GPL-3.0 [6] (D).

**Licences:** code (pygarment) MIT [1, 7] (D); simulator fork non-commercial [2] (D), and its licence covers derivative works (section 3.2), so porting its changes onto Apache-licensed Warp would carry the restriction over; only an own rewrite would be free of it (I); dataset CC BY 4.0 by an earlier LEDGER note, CC BY-SA 4.0 by a search summary: unresolved. Last commit June 2025 [1]; pygarment 2.0.2 released April 2025 [7] (D); the project looks dormant (I).

## 2. Newer work, to October 2026

| Work | What it makes | Licence (code / weights) | Usable commercially? |
|---|---|---|---|
| ChatGarment, CVPR 2025 [8] | Image or text to GarmentCode settings, draped with ContourCraft; LLaVA-7B, needs NVIDIA (I) | Code Apache 2.0; GarmentCodeRC MIT; ContourCraft MIT but uses SMPL/SMPL-X; weights on SharePoint with no licence stated (D) | Code yes; weights unknown |
| AIpparel, CVPR 2025 [9] | A 7B model outputting patterns of GarmentCodeData's types; CUDA 12.1 (D) | No LICENSE file (D); "CC BY 4.0" (search summary) | A CC BY decision |
| Design2GarmentCode, CVPR 2025 [10] | A language model writes GarmentCode programs: the same garment types (D). Calls GPT-4o by default; a fine-tuned Qwen2-VL-2B is the alternative (D) | Code MIT (D); fine-tune licence unstated | Code yes; the default API call breaks the no-API rule |
| GarmageNet and GarmageSet, 2025 [11] | Patterns learned from 14,801 professionally made garments, 2,293 outerwear (search summary) | CC BY-NC-ND 4.0 (D) | **No** |
| DressCode, 2024 [12] | Text to pattern | No LICENSE file; CC BY-NC-ND (search summary) | **No** |
| Garment3DGen; GarmentDreamer [13] | Meshes, not patterns | CC BY-NC 4.0, both (D) | **No** |
| NeuralTailor 2022; SewFormer 2023 [14] | Point cloud or image to pattern; older garment types | MIT (D); CC BY 4.0 (search summary) | NeuralTailor yes; SewFormer a CC BY decision |
| Dress-1-to-3, 2025 | Image to pattern, refined by simulation; hours per garment [15] (D) | Code not released (search summary) | n/a |
| 2026 papers: Image2Garment, PatternGSL, SwiftTailor, Garment Particles, NGL, DressWild, SewFusion, GarmentWeaver, EASE, InverseDraping [15] | Image or text to pattern, or pattern editing | Not checked; PatternGSL's code "will be released" (D) | Unknown |
| Bolt (NVIDIA), April 2025 [15] | Refits finished outfits to new bodies "for gaming" | Code release not found | Unknown |

All of these learn from computer-generated single-layer garments (D for SwiftTailor and SewFusion; I for the rest). None claims lapels, button stands or pockets (I). Bolt's job, refitting to many bodies, is already done by MetaHuman's outfit resizer [16] (D).

## 3. From pattern to game mesh

1. **Pattern:** GarmentCode's JSON, or FreeSewing as now.
2. **Drape:** (a) Blender cloth, sewn from the JSON seams: the current method, which would fail in the same place (I); (b) Marvelous Designer, importing a pattern converted by script (I, untested), exporting USD with a simulation mesh for Unreal's Chaos Cloth [16, 17] (D): paid, Jafar's decision; (c) GarmentCode's own simulator: ruled out by its licence.
3. **Clean light mesh:** the flat-piece mesh already has the flat pattern as its texture layout [1, 5] (D), so the grain lies right (I), but it is dense triangles; professionals draw clean quads over the flat pattern and carry them back onto the 3D shape [16] (D).
4. **Sculpt the folds, then bake them into normal maps** [16] (D).
5. **Skin and resize** through MetaHuman's Outfit Asset, which copies the weights again from the body [16] (D); simulate only the loose parts.

## 4. Honest assessment

- **GarmentCode is the wrong place to look for jackets.** It can say less about a jacket than FreeSewing's Jaeger (I); its authors list layers, sharp folds, fastenings and sewn-on pieces as unsupported [4, 5] (D), and lapels, collars, a donkey-jacket yoke and patch pockets are made of exactly those (I).
- **The tailored look comes from construction a drape does not model:** canvas and interfacing, shoulder pads, a pressed roll line, two-layer collars and hand shaping. Studios drape stiffened, layered pieces in Marvelous and then sculpt [16] (D). Draping a correct single-layer pattern still gives a soft, shirt-like shell (I), which matches what LEDGER's blind reviewers faulted: shape, collar and lapel, yoke edges (I).
- **Where code patterns could help:** quick variety in simple crowd garments (shirts, blouses, plain skirts and dresses, basic trousers) across many bodies, with the flat pattern as the texture layout (I); each still needs a clean mesh, skinning and an approved sample, and a drape that may ship (an own one, or one on Apache-licensed Warp).
- **Tailoring at KCD2's level means modelled, sculpted garments** (I), as in TAILORED-ROUTES [16].
- **Decisions for Jafar:** the MIT code with an own drape needs none; output from AIpparel or SewFormer would be a CC BY decision; the non-commercial tools are out.

## Sources

1. GarmentCode repository: README, docs, LICENSE (MIT), assets/garment_programs, design_params/default.yaml, assets/bodies/Readme.md, pygarment/meshgen. Korosteleva et al., last commit 29 June 2025. https://github.com/maria-korosteleva/GarmentCode (read in full)
2. NvidiaWarp-GarmentCode, README and LICENSE.md. Undated; a fork of Warp 1.0.0-beta.6. https://github.com/maria-korosteleva/NvidiaWarp-GarmentCode (read)
3. NVIDIA Warp: README, LICENSE.md and CHANGELOG (1.6.2, 7 March 2025; 1.17.0, 31 August 2026). https://github.com/NVIDIA/warp (read in part); PyPI warp-lang 1.17.0 (read)
4. Korosteleva and Sorkine-Hornung, "GarmentCode: Programming Parametric Sewing Patterns", ACM TOG 42(6), December 2023, arXiv 2306.03642 (sections 5.4 and 6 read)
5. Korosteleva et al., "GarmentCodeData", ECCV 2024, arXiv 2405.17609 v3, 5 September 2024 (method, timing and limitations read)
6. GarmentMeasurements, Botsch et al., GPL-3.0, undated. https://github.com/mbotsch/GarmentMeasurements (LICENSE and README read)
7. pygarment 2.0.2, PyPI, 18 April 2025, MIT (read)
8. ChatGarment (Apache 2.0), Bian et al., CVPR 2025, https://github.com/biansy000/ChatGarment (README and install guide read); GarmentCodeRC, MIT, 28 April 2025, https://github.com/biansy000/GarmentCodeRC (code compared with [1]); ContourCraft, MIT, https://github.com/Dolorousrtur/ContourCraft (LICENSE read)
9. AIpparel-Code, Nakayama et al., CVPR 2025, https://github.com/georgeNakayama/AIpparel-Code (README read; no LICENSE file; licence from search summary)
10. design2garmentcode-impl, Style3D, MIT, last commit 19 November 2025, https://github.com/Style3D/design2garmentcode-impl (README and file list read)
11. garmagenet-impl LICENSE, CC BY-NC-ND 4.0, Style3D (read); arXiv 2504.01483 v4, 14 October 2025 (abstract read); GarmageSet details (search summary)
12. DressCode, He et al., SIGGRAPH 2024, https://github.com/IHe-KaiI/DressCode (no LICENSE file; licence from search summary)
13. Garment3DGen LICENSE.md, https://github.com/nsarafianos/Garment3DGen; GarmentDreamer LICENSE, https://github.com/boqian-li/GarmentDreamer (both read)
14. Garment-Pattern-Estimation (NeuralTailor), MIT, https://github.com/maria-korosteleva/Garment-Pattern-Estimation (LICENSE read); SewFormer, https://github.com/sail-sg/sewformer (search summary only)
15. arXiv abstracts read through export.arxiv.org: Image2Garment 2601.09658 (19 March 2026); PatternGSL 2606.24564 (2 July 2026); SwiftTailor 2603.19053 (19 March 2026); Garment Particles 2605.26391 (May 2026); NGL 2602.20700; DressWild 2602.16502; SewFusion 2609.23548 (September 2026); GarmentWeaver 2608.30550; EASE 2606.29419; InverseDraping 2604.02764; Bolt 2504.17614 (24 April 2025). Dress-1-to-3, 2502.03449: search summary only.
16. Earlier LEDGER notes (read): clothing-pipeline/TAILORED-ROUTES-2026-09-30, game-clothing-pipeline/NOTE-2026-09-30, character-pipeline/RESEARCH-2026-09-25
17. "[Tips&Tricks] Discover Better Workflow with Marvelous Designer and Unreal Engine", Marvelous Designer support, undated (search summary only)

## What could not be verified

- The dataset's licence (CC BY 4.0 or CC BY-SA 4.0): ETH's pages were blocked.
- The licences of the trained AIpparel and ChatGarment models: Hugging Face was blocked.
- SewFormer's, DressCode's and SMPL's licences, beyond search summaries.
- GarmentCode's simulation speed on a CPU, and whether its simulator builds on Windows without CUDA in practice.
- Whether Marvelous imports a converted GarmentCode pattern cleanly.
- Whether Unreal's Chaos Cloth tools can sew flat pieces without Marvelous.
- Code release and licences for Bolt and the 2026 papers (the search budget ran out).
- Whether any 2026 work handles lapels or fastenings: abstracts only.
- KCD2's own clothing pipeline: inference only.
