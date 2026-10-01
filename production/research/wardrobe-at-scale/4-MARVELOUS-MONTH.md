# Marvelous Designer as a one-month sprint (research note, 1 October 2026)

A separate helper was given the problem, not a theory, and spent about thirty minutes, reading only. **D** documented (source); **I** inference. Vendor sites could not be opened directly and the helper's web-search budget ran out, so vendor claims are **search summaries (SS)**. Read in full: the GitHub sources measured against MD 2026.0, Epic's documentation, and one copy of the EULA. Saved by the cloud session; its own check of the EULA is in SUMMARY.md.

The answer that settles ownership needs the current MD Terms at marvelousdesigner.com/terms/agreement, which could not be opened: confirm with CLO in writing before paying.

## In short

- **Ownership: probably yes, permanently.** The Personal licence, as quoted in forums, lets the licensee "sell or distribute its original works and their derivatives in any file formats", and says CLO "has no right, title, or interest" in them [2] (D, SS). The EULA read in full makes expiry stop *use of the software* ("cease all use of the Licensed Materials... uninstall"), not use of the works [1] (D). The two risks: library content, and buying as a company. The governing Terms page was not read (I).
- **Scripting reaches most of a garment (I) but none of the retopology.** Scripts can make patterns from coordinates, sew, apply fabric from a file, simulate, pack UVs, and export FBX, OBJ, Alembic or USD with simulation data. Scripts cannot import DXF or SVG, remesh, retopologise, or place pieces reliably; someone must click once each time the program launches [8, 9] (D).
- **Throughput:** a skilled artist takes about 1 to 3 days per finished game garment (I, thin evidence [17]). A script-driven month gives about 6 to 12 base garments if the first jacket passes review in week one, under 5 if not (I).
- **No alternative beats MD here (I).**

## 1. Licence and ownership

- **Who may buy Personal:** "individuals, freelancers, hobbyists and sole proprietors"; studios and game companies need Enterprise [3] (D, SS). One quoted line says the buyer is "a natural person, not legal entity", for "personal, recreational and commercial use" [2] (D, SS). A purchase on a company card or company e-mail "may be considered as a purchase by a corporate customer" [3] (D, SS). Jafar buying privately for his own game fits; a company with staff would need Enterprise at $199 a month [19] (I; the price D).
- **Who owns the output:** the quoted "original works" clause has no time limit (I). CLO's sister terms say "You retain all rights and ownership of your Work Product", and give CLO a licence to analyse that work "to improve the Services and Software" [15] (D, SS). Whether MD's Personal terms carry that clause is unread.
- **What expiry does:** under the October 2023 EULA, unrenewed subscriptions "expire at the end of the applicable License Term", and the licensee then uninstalls the "Licensed Materials" and may be asked for proof [1] (D). "Licensed Materials" is defined in the Terms at marvelousdesigner.com/terms/agreement, which could not be read [1] (D).
- **Library risk:** CLO bars distributing or monetising its default avatars without consent and a royalty [15] (D, SS). No licence for MD's own library was found. So: build on MetaHuman bodies with own patterns and textures, and ship nothing taken from the library (I).
- **Monthly or yearly:** the same Personal licence: $39 a month, renewing automatically, or $280 a year, prepaid [3, 4] (D, SS). A month bought directly is not refunded; access runs to the end of the cycle [4] (D, SS). A 14-day full trial exists [19] (D); nothing found on commercial use of work made in it.
- **Ruled out:** the indie tier (January 2026) needs 2 or more employees [6] (D, SS); standalone Enterprise licences ended on 2 December 2025 [5] (D, SS); perpetual and Steam licences ended in 2020 [7] (D, SS). Personal needs internet and sign-in [3] (D, SS).
- **After the month:** CLO-SET's web viewer opens .zprj files and, since January 2026, shows the 2D patterns [14] (D, SS). Editing needs a new licence (I). Before the month ends, export the meshes, the pattern JSON (MD's own format, readable by script), the .zfab fabric files, textures and UV layouts (I).

## 2. What scripting drives (2026.x)

Sources: the published "API 0.1" list (588 calls) [9], and calls measured on 2026.0.315 on 19 September 2026 [8]. The published docs cover 2024.2 to 2025.1, so calls added in 2025.2 or later may be undocumented [8] (D).

| Step | By script? |
|---|---|
| Avatar | `ImportFBX` / `ImportOBJ` with options (no dialog), `ImportAvatar`, measurement CSV [9] (D). No call for 2025.2's MetaHuman DNA import [9, 11] (D, by absence). |
| Pattern in | `CreatePatternWithPoints` and shapes from coordinates; `ImportPatternJSON` [9] (D). **DXF cannot be reached**: its option types exist but no function takes them [8] (D, measured). No SVG call [9] (D). A GarmentCode or FreeSewing pattern would need an own converter (I). |
| Sewing | `AddSeamlinePairGroup` [9] (D). A degenerate seam opens a modal dialog that hangs the script [8] (D). |
| Arrangement | `SetArrangementPosition` measured to do nothing; arrangement points cannot be created [8] (D). |
| Fabric | `AddFabric(.zfab/.jfab)`; `AssignFabricToPattern` takes three integers, not two [8] (D). No setters for physical properties [9] (D). |
| Simulation | `Simulate(steps)`, quality presets, CPU or GPU, gravity, collisions [9] (D). It returns True even when the garment stays flat [8] (D). Runs on the CPU on this PC [19] (D). |
| Retopology | **None by script.** The interface has Remeshing, Quadrangulate and Remeshing-to-Retopology [12] (D, SS); the API has only `SetMeshType(piece, "Quad")` and particle distance [9] (D). Whether a coarse quad mesh is good enough for the game is untested (I). |
| UVs | `ResetUVTo2DArrangement`, `UVPacking`, `FitAllUV`, `BakeUVTexture` [9] (D). |
| Export | `ExportFBX`, `ExportAlembic`, `ExportOBJ` (pass its options or it hangs), and `ExportUSD(path, options, ExportUSDOption)` with `m_bExportSimulationData` [8, 9, 10] (D). |
| Run | From the Python editor or a plugin: a click each launch, no quit [8] (D). |

**MetaHuman route:** MD documents the steps: import USD, Cloth Asset, Dataflow, Outfit Asset, apply [11] (D, SS); 2025.2 added DNA import and USD simulation data for Unreal 5.6 and later [11] (D, SS). Epic's page says a USD from MD or CLO can carry the render and sim meshes (earlier note, game-clothing-pipeline/NOTE-2026-09-30.md, Path B), while the page this helper read says "a render mesh only" for one path [16] (D): the trial would settle it (I).

**Since August:** 2026.1 (24 August) added lacing, pinch brushes, Seamline Rip, blendshape recording and toolbar options [13] (D, SS); nothing for scripting, headless use or retopology. No 2026.2 found. A Linux edition with Python exists, Enterprise only, about $2,300 a year [6, 7] (D, SS); headless unknown.

## 3. Throughput and ready-made content

- **Evidence:** a senior character artist takes 2 to 3 weeks per full character, clothing included [17] (D, SS); one artist made 9 characters with swappable outfits in 3 months [17] (D, SS); one freelance offer: an MD garment with textures in 3 days for $200, $350 with retopology [18] (D, SS, thin). No studio figure for garments per week was found: about 1 to 3 days per base garment, 2 to 5 a week, for a skilled artist (I).
- **A script-driven month (I):** week 1 is the pipeline and one jacket (MetaHuman body, own pattern, drape on the CPU, USD/FBX export, Outfit Asset in Unreal, blind review); after that, variants of a passed pattern are cheap (lengths, lapels, double-breasted, an overcoat from the jacket); the bottlenecks are the review gate and finishing the game mesh in Blender; hence 6 to 12 base garments, or under 5 if the jacket stalls.
- **MD's own library:** free garments (T-shirt, trousers, jeans, cargo shorts, hoodie, padded jacket, dresses and skirts) [13] (D, SS); the Modular Configurator (jackets, polos, shirts, T-shirts and trench coats) and a Modular Library since 2025.0 [13] (D, SS). No tailored suit or blazer pattern was named.
- **CONNECT** (CLO's marketplace): about 50,000 assets, about 10,000 free; each creator sets Basic and Extended licence prices per item [14] (D, SS). No period workwear found.

## 4. Alternatives

- **CLO:** $50 a month or $450 a year for an individual's personal or commercial use; more than one employee needs Business [15] (D, SS). The work stays the user's [15] (D). Same engine as MD, with a matching MetaHuman USD guide [11] (D). Dearer, with no gain for games (I).
- **Style3D Atelier:** free tier non-commercial [19] (D); about $99 a month Basic, $180 Pro by its own blog [19] (D, SS, thin); output terms not read.
- **Browzwear VStitcher:** not checked (blocked); sold to fashion firms on quotation, so a one-month individual licence is unlikely (I).
- **Blender add-ons:** Garment Tool from $54 and Simply Cloth Studio $36 to $170, one-off purchases [19] (D); meshes are ours (I). Both use Blender's cloth solver, which already failed blind review for jackets: they improve the workflow, not the quality (I).

## Sources

1. CLO Virtual Fashion LLC, MD "End User License Agreement" (signed-licence form), PDF dated 6 Oct 2023: https://flashbackj-general-storage.s3.amazonaws.com/data/clo/marvelous_designer_eula_new.pdf. Read in full.
2. The Personal-licence clause as quoted on the Daz 3D forums (discussion/26714) and in Steam MD6 discussions, undated. SS.
3. MD support: "What is the difference between Personal and Enterprise License?", "License Plan", "What kind of licenses...", undated: https://support.marvelousdesigner.com/hc/en-us/articles/47358297616153. SS.
4. MD support: "Can I cancel my subscription?", "Refund Policy for Cancellations" (…/50937459914777), undated. SS.
5. MD: "Standalone License Transition", effective 2 Dec 2025 (…/51136941117849). SS.
6. Digital Production, "Marvelous Designer adds indie pricing, quietly", 12 Jan 2026. SS.
7. CG Channel, "Marvelous Designer goes subscription-only" (July 2020); "...now available for Linux" (Oct 2025). SS.
8. matty/marvelous-designer-plugins (GitHub), docs/md-conventions.md and src/md_mcp/notes.py, measured 19 Sep 2026 on 2026.0.315: https://github.com/matty/marvelous-designer-plugins. Read.
9. lupin4/MD_Tools (GitHub), API_List.txt (a copy of the official API list), undated: https://github.com/lupin4/MD_Tools. Read.
10. The same repository, README and md_batch_process.py. Read.
11. MD support: "Marvelous Designer to MetaHuman: USD Garment Integration Workflow" (…/52699135975705) and "MetaHuman DNA Importer"; CLO's matching guide; news on 2025.2 (Nov 2025). SS.
12. MD support: "Remeshing", "Remeshing to Retopology (Selected)", "Retopology (ver. 12 & Above)", undated. SS.
13. MD support: "Marvelous Designer 2026.1 New Feature List" (24 Aug 2026), "Does Marvelous Designer provide sample assets?", "Modular Library (Ver. 2025.0)"; virtualfilmer.com, "Free Garments Included with MD 12". SS.
14. The CONNECT guide (2026) and terms (connect.clo-set.com, legal.clo-set.com); CLO-SET support pages on the 3D Viewer and the 2D Pattern Viewer (Jan 2026). SS.
15. CLO support: "Individual vs Enterprise", "How much does CLO cost?"; CLO-SET General Terms of Use (https://legal.clo-set.com/modal-tou-general); the clo3d.com legal archive. Undated. SS.
16. Epic, "Getting Started for creating Parametric Clothing in MetaHuman", undated: https://dev.epicgames.com/documentation/metahuman/getting-started-for-creating-parametric-clothing-in-metahuman. Read.
17. Polycount, "How long does it take to create a character?" (discussion/193616); 80.lv, "The Punisher: Clothes Production, Retopology, Texturing". SS.
18. A freelance clothing offer (summary of a gig listing), undated. SS, thin.
19. LEDGER notes MD-SCRIPTING-2026-09-29, TAILORED-ROUTES-2026-09-30 and SLEEVES-RECIPE-2026-09-29; Style3D AI blog on pricing (2026), SS.

## What could not be verified

- The current MD Terms: the definition of "Licensed Materials", what survives expiry, any AI or data clause, and the licence on library assets. The site was blocked.
- Whether work made in the 14-day trial may be used commercially.
- Whether a free CLO-SET account opens .zprj files.
- Whether the interface's DXF import still exists in 2026.1.
- Whether 2025.2 or later added API calls (DNA import, remeshing), and whether a 2026.2 exists.
- Whether MD's USD export carries a simulation mesh into Unreal 5.8.
- Whether the Linux edition can run headless.
- Any studio figure for garments per week, and any period workwear on CONNECT.
- Browzwear's pricing, Style3D's terms for commercial output, and the Blender add-ons' current prices.
