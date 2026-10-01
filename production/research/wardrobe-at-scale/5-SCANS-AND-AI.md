# Scanned clothing libraries, and where AI garments stand (research note, 1 October 2026)

A separate helper was given the problem, not a theory, and spent about thirty minutes, reading only. Only raw GitHub files would open; the network refused shop, vendor, Hugging Face and arXiv pages, so everything from those is a search-engine summary. **D** means documented, with the source number. **I** means its inference. Saved by the cloud session; one correction is marked.

## In short

1. **No scan library sells 1990 British workwear.** In scans of whole people the clothes are fused to the body (Renderpeople, ActorCore, AXYZ) [13][18][19]. The only separate, game-ready scanned garments found are 3D Scan Store's: modern cuts, about £236 each with a commercial licence [12] (D). For LEDGER, scans are mainly useful as fabric surfaces (Megascans, Texturing XYZ) [14][15] (D/I).
2. **AI 3D generators make one static mesh with the folds baked in; none weights it to MetaHuman's skeleton** (I; Meshy rigs to its own skeleton [22] D). The two closest: Rodin Gen-2 (separate parts, quad output, $30 a month) [26] (D); Tripo plus MetaTailor fitting, still a beta [23][24] (D).
3. **The AI sewing-pattern models are blocked by their licences or limited to what GarmentCode can describe.** GarmentCode has shirt-type uppers and no parameters for pockets, buttons or front fastenings [7] (D): skirts, trousers and simple tops, not a tailored jacket (I).
4. **Nothing available today makes a 1990 tailored jacket at KCD2's level** (I). AI serves props, loose garments and textures. No shipped game with realistic AI-made clothing was found; the documented cases are stylised accessories and player-made items [36][37][38] (D).

## 1. Scanned libraries

| Source | What | Price | Sold game? | Garment separate? | MetaHuman |
|---|---|---|---|---|---|
| 3D Scan Store | Modern scanned garments (leather and puffer jackets, gilet, sweater, jeans, trainers): retopologised game mesh, 8k PBR, ZBrush high-poly, fitted to their own mannequin [12] D | Jacket 01 £25.99 personal; Business Commercial Single Project licence +£209.99 per item; male pack +£1,379.99 [12] D | Yes, one project [12] D | Yes [12] D; rigging not stated | Refit and skin (I) |
| Renderpeople | Scanned people | Posed $39, rigged $79, 120 people $999 [13] D | Games allowed; machine-learning use excluded [13] D | No: one 10–15k quad mesh [13] D | Reference or distant crowd only (I) |
| ActorCore | Scanned and themed people | not found | Allowed per a summary of the EULA; Reallusion's own content needs an export licence and the title registered [18] D | Baked (I) | No |
| AXYZ Metropoly | People for architectural renders | €19–59 each; anima ALL €649 a year [19] D | Unverified | Baked (I) | No |
| Megascans (Fab) | No garments; fabric surfaces: cotton plain and twill, wool, leather, tarp [14] D | Paid on Fab since 2025; claimed in 2024 stay free [14] D | Fab Standard | n/a | Textures (I) |
| Texturing XYZ | Tiling close-up fabric maps: wool, canvas, denim, fleece [15] D | Paid, tiered | Commercial tiers yes; personal no [15] D | n/a | Fine detail maps (I) |
| Sketchfab | Scattered CC0 and CC-BY scans (a 2017 photogrammetry "Old Leather Jacket"; a CC0 clothing kit) [16] D | Free | Per model; the store has closed into Fab [16] D | Static scans (I) | Retopology and skinning (I) |
| Museums | Smithsonian 3D is CC0 (2,346 of 2,544 models in 2020) [17] D, including US fashion scans; museum garment sets found span the 1700s to the 1970s [16] D | Free | CC0 where marked | Static, on dress forms (I) | Reference only; no 1980s British workwear found (I) |
| TurboSquid / CGTrader | Mixed, some scanned jackets | Per item | Royalty-free licences allow PC games [20] D | Varies | Per item |
| Fab MetaHuman outfits | Resizable: techwear, lumberjack workwear, formal [21] D | About $5–20 [40] D | Fab Standard | Yes | Nearest ready-made route (I) |

Two tools fit any garment mesh onto a MetaHuman: **MetaTailor**, $35 a month or $336 a year, rental only, its Unreal bridge in beta from July 2025 [24] D; and **Clothy3D Studio**, a free public beta since September 2025, handling MetaHuman and Marvelous Designer garments [25] D. Epic's outfit graph re-copies the weights from the body anyway [40] D.

## 2. AI garment generation, October 2026

**Commercial**
- **Meshy 6:** text or image to one textured mesh; auto-rigs to its own humanoid skeleton. Free tier CC BY 4.0; Pro $20, Premium $40 (full commercial rights), Studio $60, Ultra $100 a month [22] D. Cloud only (I).
- **Tripo 3.x:** the same kind of output; paid plans $19.90–139.90 a month carry a commercial licence [23] D. A Tripo-to-MetaTailor link for "fitted, rigged wearables" was announced as a beta [23] D.
- **Rodin Gen-2/2.5 (Hyper3D):** a 10B-parameter model; "BANG" splits a model into separate parts; quad meshes at 4k to 50k; T-pose or A-pose; Creator $30 a month, Business $120; paid outputs may be used commercially [26] D. The closest thing to "a jacket as its own quad mesh" (I). Not on the allowlist: a ruling (I).
- **Others** [27][28] (D): Kaedim (AI plus human clean-up) $400 a month for 20 assets; CSM $20–111 a month; Sloyd $15–50 a month, props only; Luma Genie closed on 1 January 2026.
- **NVIDIA Edify 3D:** the preview ended in June 2025; now only through Shutterstock's and Getty's enterprise services [29] D.
- **Adobe Substance 3D:** text-to-texture in Sampler; text-to-3D only in the Viewer beta [30] D.
- **Marvelous Designer 2026.0:** an AI Pattern Drafter (beta) from measurements or flat sketches, plus AI texture and image generators; no text-to-garment [31] D.
- **CLO:** its AI drafter makes trouser and skirt patterns from an image or text [32] D.
- **Style3D AI:** about $99+ a month by its own blog [33] D; its research code, GarmageNet, is CC BY-NC-ND (non-commercial) [10] D.
- **Roblox Cube/CubePart:** open weights under a research-only licence [11] D: forbidden.

**Open**

| Model | Output | Licence | Hardware | Verdict |
|---|---|---|---|---|
| TRELLIS.2 (4B) | Image to PBR mesh; handles open surfaces "e.g. clothing" [1] D | MIT; the code loads Meta's DINOv3 and BiRefNet [1] D | Linux, NVIDIA 24 GB+ [1] D, so rented; a Windows Vulkan port, trellis.cpp, fits about 6 GB at 512 (clothing-pipeline/TRIED-2026-09-24.md) | Best open option for shape. *Correction by the cloud session:* the helper wrote that DINOv3 "is already stopped by a ruling"; the earlier note stopped it to wait for Jafar's ruling ("not on the allowlist, so stopped before any download"), and no ruling on it was found in DECISIONS.md. TRELLIS v1: MIT, NVIDIA 16 GB+ [2] D |
| Step1X-3D | Closed shell plus texture | Apache-2.0 code [3] D; weights' licence not read | 27 GB [3] D | Its texture step reuses Hunyuan3D 2.0 code [3] D: check before use (I) |
| TripoSG | Closed solid shape (SDF) | MIT [5] D | CUDA 8 GB+ [5] D | A jacket comes out solid (I) |
| SPAR3D | Object mesh | Stability Community licence: free under $1M revenue, registration, ends above that [4] D | 10.5 GB (7 GB low-VRAM); CUDA, Mac or CPU [4] D | Not an allowlist-type licence: a ruling |
| ChatGarment | GarmentCode pattern plus a simulated mesh | Apache-2.0 code; weights' licence not stated [6] D | LLaVA 7B (I) | Its text route calls GPT-4o [6] D, against the no-API rule |
| AIpparel | Sewing patterns | No licence file [8] D: all rights reserved (I) | CUDA [8] D | Out |
| Garment3DGen | Reshapes a base garment mesh towards a target | CC BY-NC 4.0 [9] D | CUDA [9] D | Out |
| GarmentCode | Parametric patterns | MIT [7] D | NVIDIA Warp simulator [7] D | Uppers are Shirt/FittedShirt; collars include SimpleLapel [7] D |

Hunyuan3D 2.x/3.x is banned (territory exclusion).

2025–26 research papers, abstracts only [34]: GarmentX and GarmentWeaver (both output GarmentCode), DressWild, EasyFashion, BAG, GarmentDiffusion (no licence file found), InverseDraping (recovers a pattern from a 3D garment surface), Fashion-3DLR.

Whichever route, the garment still needs retopology, fitting on the source body, a weight transfer (or MetaTailor/Clothy3D) and Epic's outfit graph (I).

## 3. Honest state of the art

- **A tailored 1990 jacket at KCD2's level: no** (I). Image-to-3D gives a fused shell with folds baked in and no lining, lapel roll or pocket depth; retopology, UVs and skinning remain. Pattern AI stays within GarmentCode-like shapes [7]. Tencent's own game pipeline advises against loose clothing on humanoid inputs [35] D.
- **Where AI helps now** (I): skirts, trousers and simple tops as patterns; caps, bags and props as meshes; fabric textures; rough starting shapes for hand finishing.
- **Cheapest test that would settle it** (I): one month of Rodin Creator ($30) on the donkey jacket, in parts mode at about 18k quads, then the gate.
- **Shipped games, 2025–26:** inZOI uses AI for clothing textures and image-to-3D accessories, trained on Krafton-owned art [37] D; Parallel's Colony generates player-described helmets and weapons (GDC 2026) [36] D; Meshy Labs' Black Box generates weapons [38] D; a vendor claims 37 Interactive halved its modelling time [38] D. None is realistic tailored clothing (I). Steam requires disclosure of AI-made 3D models (January 2026 update) [39] D.
- No source was found on how Warhorse made KCD2's clothing.

## Sources

Read in full (raw GitHub files):
1. TRELLIS.2 README, LICENSE, image_feature_extractor.py, rembg/BiRefNet.py. Microsoft, undated (paper 2025). github.com/microsoft/TRELLIS.2
2. TRELLIS README, LICENSE. Microsoft, undated. github.com/microsoft/TRELLIS
3. Step1X-3D README, LICENSE. StepFun, news to 26 June 2025. github.com/stepfun-ai/Step1X-3D
4. SPAR3D README, LICENSE.md. Stability AI, undated. github.com/Stability-AI/stable-point-aware-3d
5. TripoSG README, LICENSE. VAST, 2025. github.com/VAST-AI-Research/TripoSG
6. ChatGarment README, docs/Installation.md, LICENSE. Undated (CVPR 2025). github.com/biansy000/ChatGarment
7. GarmentCode LICENSE, docs/Installation.md, assets/design_params/default.yaml. Korosteleva, 2024. github.com/maria-korosteleva/GarmentCode
8. AIpparel-Code README; no LICENSE on main or master. Undated. github.com/georgeNakayama/AIpparel-Code
9. Garment3DGen README, LICENSE.md. Undated. github.com/nsarafianos/Garment3DGen
10. GarmageNet README licence section, LICENSE. Style3D, undated. github.com/Style3D/garmagenet-impl
11. Roblox Cube README (updates to May 2026), LICENSE, cubepart README. github.com/Roblox/cube

Search summary only:
12. 3D Scan Store clothing pages, undated. 3dscanstore.com/3d-clothing-models-1/clothing-models
13. Renderpeople product pages and General Terms; HumanDataset. Undated. renderpeople.com/general-terms-and-conditions/
14. Fab, "Quixel to Fab Transition FAQs"; Tim Sweeney on X, 22 Oct 2024; Quixel fabric listings. support.fab.com/s/article/Fab-Transition-FAQs
15. Texturing XYZ terms; Micro Fabrics. Undated. texturing.xyz/pages/terms-of-service
16. Sketchfab blog: "Sketchfab Update ... Fab's live", Oct 2024; "3D Scanning a Museum Fashion Collection", undated.
17. Creative Commons, Smithsonian CC0 release, 27 Feb 2020; 3d.si.edu/collections/girlhood
18. ActorCore EULA, Reallusion, undated. actorcore.reallusion.com/eula; reallusion.com/license/content.html
19. AXYZ anima ALL page; CG Channel, "Chaos ends perpetual licenses of anima", Aug 2024.
20. TurboSquid licensing, undated. turbosquid.com/licensing; CGTrader forum.
21. Fab MetaHuman channel listings, undated. fab.com/channels/metahuman
22. Meshy pricing docs, undated. docs.meshy.ai/en/webapp/pricing; Costbench, Aug 2026; meshy.ai/features/ai-auto-rigging
23. Costbench, Tripo pricing, Sep 2026; Tripo blog, "METATAILOR x TRIPO", undated.
24. Digital Production, 28 Jul 2025; CG Channel, Jul 2025 (MetaTailor).
25. CG Channel, Oct 2025; Digital Production, 25 Sep 2025 (Clothy3D).
26. MakerStack Rodin review, 2026; AWN interview, undated; docs.hyper3d.ai Gen-2.5 spec.
27. Capterra, Kaedim, 2026.
28. creati.ai (CSM); Toolworthy (Luma Genie), 2026; sloyd.ai blog.
29. NVIDIA blog; build.nvidia.com (Edify), undated.
30. Adobe blog, 18 Mar 2024.
31. CG Channel, Apr 2026; Digital Production, 15 Apr 2026; MD support "Pattern Drafter (Beta)".
32. CLO support "Pattern Drafter"; Stytrix comparison, 2026.
33. Style3D AI blog, pricing, 2026.
34. arXiv abstracts: 2602.16502 (DressWild, 18 Feb 2026); 2608.30550 (GarmentWeaver, 31 Aug 2026); 2609.18483 (EasyFashion, Sep 2026); 2504.20409 (GarmentX, 29 Apr 2025); 2504.21476 (GarmentDiffusion, 2025); 2501.16177 (BAG, Jan 2025); 2604.02764 (InverseDraping, Apr 2026); 2607.23189 (Fashion-3DLR, Jul 2026).
35. Hunyuan3D Studio, arXiv 2509.12815, Sep 2025; Tencent Hunyuan on X.
36. Parallel Colony on X, Mar 2026; BlockchainGamerBiz.
37. Game8, "Does inZOI use AI?", 2025.
38. Cinevva, 9 Mar 2026 (Meshy Labs); meshy.ai/use-cases.
39. TechPowerUp, Steam AI disclosure clarification, Jan 2026.

Read on this PC:
40. production/research/clothing-pipeline/TAILORED-ROUTES-2026-09-30.md, TRIED-2026-09-24.md; game-clothing-pipeline/NOTE-2026-09-30.md.

## What could not be verified

- Every vendor page at source: prices, licence wording, and whether outputs stay licensed after a one-month plan ends (Rodin, Meshy, Tripo, MetaTailor).
- The licences of the model weights on Hugging Face (Step1X-3D, ChatGarment, AIpparel), and which image and background-removal models TRELLIS.2's published setup uses.
- Whether 3D Scan Store's licence is perpetual and whether its garments come skinned.
- ActorCore's and AXYZ's game terms in full.
- Whether Renderpeople's machine-learning exclusion bars using its scans as input to AI tools.
- Any V&A, Science Museum or Europeana 3D garment under an open licence, and any scan of 1980s British workwear anywhere.
- ClothDreamer (repository not found), Spline and NVIDIA Picasso: not checked.
- No vendor or paper shows a generated tailored jacket judged against a game-quality bar.
- Chinese studios' in-house garment tools (NetEase, Tencent, miHoYo) and the GDC 2026 survey figures: not reached.
