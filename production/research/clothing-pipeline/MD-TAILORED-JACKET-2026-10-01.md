# A 1990 suit jacket in Marvelous Designer: the method (research note, 1 October 2026)

The problem: one charcoal wool, single-breasted 1990 suit jacket, made in Marvelous Designer 2026 (MD) partly by Python, then sent to Unreal 5.8 as a MetaHuman Outfit Asset for a heavy and a lean man. Earlier attempts failed on the tailoring: shards where the lapel roll ends, a lapel that does not roll, a puffy breast pocket, the wrong decade. A separate helper, about thirty minutes, web only; nothing signed into. **D** = documented [source]; **I** = the helper's inference.

## The route for us

1. **Bodies.** Drape one size on the heavy build and one on the lean build, and give the Outfit Asset both. Epic says more source bodies give better resizing [22] (D). Realistic clothes warp badly between very different bodies (PIPELINE-2026-09-30) (D), and tailoring worst (I). Epic's Construction Presets [20] are a fallback.
2. **Load the body** with `ImportFBX`, setting `bAddArrangementPoints` and `bAutoCreateFittingSuit`, so no dialog appears [13] (D). This corrects the 29 September note: arrangement points can be made by script. MD's DNA import adds them too, but only by menu [9] (D).
3. **Pattern.** Draft FreeSewing Jaeger at each body's measurements (2 buttons, 1 vent, lower lapel start) [26] (D). Export each piece's points as JSON and build the pieces with `CreatePatternWithPoints` and `CreateInternalShapeWithPoints` [13] (D). Redraw the patch pockets as flap pockets (I).
4. **Build it the tailor's way.** Make a front shell plus a separate lapel facing, joined along the front edge by a **turned** seam, and an undercollar plus a top collar. Draw the roll line as an internal line on front and facing [16] (D-summary). Run it edge to edge, from the break point to the neckline: a roll line that stops inside a piece is the likeliest cause of the shards (I).
5. **Stiffen.** Put **Bond** (MD's fused interlining) on the fronts or on a chest-and-lapel area, and on the collar [7] (D). Seam-tape the edges with the "Fusible (lapel)" and "Reinforcement (Under Collar)" presets [6] (D).
6. **Fold.** Give the roll lines a fold angle and fold strength, and pre-fold them with Fold Arrangement. Strengthen for the first drape, then Unstrengthen [2, 3, 5] (D).
7. **Shoulder.** Add a rigid shoulder-pad object as a second avatar [8] (D); its shape stays in the drape (I).
8. **Stop the puffing.** Set fold strength 0 on the shell-to-facing and shell-to-lining seams [4] (D). Make the breast pocket a welt cut into the front and Bonded, not a layered piece (I).
9. **Simulate.** Work at a 20 mm particle distance and finish at 5 mm or less [12] (D), on the "Fitting" quality preset [13] (D). Lapel and collar at 2 to 3 mm (I).
10. **Buttons** are placed and fastened by hand [12] (D).
11. **Export** with `ExportUSD` and its simulation-data option, one file per body. Then follow MD's eight Unreal steps: Cloth Asset, Transfer Skin Weights, an Outfit Asset from the Resizable template, one size per body [1] (D). This needs MD 2025.2 or later for UE 5.6 and up [1] (D).
12. **Still by hand:** the click that starts the script, Bond, fold angles, tape presets and the buttons; there are no calls for these [13] (D). Do them once in a template project and reload it with `ImportZprj` (I).

## 1. How professionals make a tailored jacket in MD and CLO

- MD's own suit tutorial (MD 9.5, 2020) builds the jacket from Modular Configurator blocks, including a ready **Blazer** [10, 11] (D). Whether that block is still in the 2026 library is unknown. Open it as a check on pieces and sewing (I).
- **CLO** [16] (D-summary): trace the roll line as an internal line and fold it with the Fold Arrangement gizmo, then repeat on the lining. Keep shell and lining from overlapping. Sew them with **Turned** lines, not flat ones, or they collide and the simulation goes unstable.
- **Folds:** angle 0 to 360° (180 is flat), strength 0 to 20 [3] (D). Strengthen gives "clean folds where fold angles are applied" [5] (D).
- **Tailoring practice** (Jaeger's instructions): canvas on the fronts, and tape on the roll line cut about 0.5 cm short so the lapel rolls [26] (D).

## 2. Fabric settings

- MD 2025's presets include V2_Woven_Twill_1, V2_Woven_Flannel_1, V2_Woven_Tweed_1 and V2_Woven_Melton_Boiled_1. No "suiting" or "gabardine" preset was seen [18] (D). Start from **Twill**, since worsted suiting is a twill (I).
- **Weight:** British 290 to 310 g cloths sell as 9.5 to 10 oz [19] (D-summary). That is per running metre of 150 cm cloth, about 195 to 210 g/m² (I).
- **Buckling ratio:** low for wool, near 0% (MD manual, search summary) (D-summary).
- **Fused fronts:** CLO's "Fusible (Lapel)" is a 30 gsm wefted interfacing [17] (D-summary).

## 3. A 1990 British suit

- Licence to Kill (1989) [27] (D):
  - two buttons, a **low button stance** and a **low gorge**
  - medium notch lapels and flap pockets
  - padded, extended shoulders and a very full cut
- Dalton's 1987 off-the-peg English suits had double vents [28] (D).
- Early-1990s Armani dropped the padding for soft shoulders [29] (D-summary).
- Lapels of about 3 to 3.5 in (8 to 9 cm) [30] (D-summary).
- For a high-street suit (I):
  - roll the lapel to the top of two buttons, with the top button at or just below the waist
  - long enough to cover the seat
  - a centre vent and lightly padded shoulders

## 4. FreeSewing Jaeger

- **Pieces** [26] (D): fronts and facings, back, sides, two-piece sleeves, collar, collar stand and undercollar, welts, patch pockets, canvas and lining.
- **Options** [26] (D): buttons 1 to 3; vents 0 to 2 and their length; lapel start and reduction; front cutaway and hem radius; collar height, notch angle and depth, collar roll and roll-line height; pockets, eases, length and sleeve bend.
- Its sewing instructions are marked unfinished [26] (D). Licence MIT (pattern-jacket-2026-09-29) (D).
- **No converter to MD exists** (D, by absence). Read the paths from FreeSewing in Node rather than its SVG.
- `CreatePatternWithPoints` takes straight, spline and Bezier points, but the order of the Bezier handles is undocumented. Test it on one curved piece first (I).

## 5. Construction Presets and the Outfit route

- **The packs:** sets of 4 and of 2, free, Standard Licence, listed for UE 5.6 to 5.7 (3 June 2025, updated 12 November 2025). They hold the presets plus FBX files with body and head combined; the builds are not named [20] (D).
- **Our own bodies:** export them as a Full Body Skeletal Mesh to FBX, with a little clearance at the armpits and thighs [22] (D).
- **Reported broken:**
  - The presets' FBX files distort through the Interchange importer. The fix is `Interchange.FeatureFlags.Import.FBX 0` [21] (D).
  - In 5.8, cloth simulation is lost when an Outfit becomes a Wardrobe item [23] (D, 19 July 2026). That hardly matters if only the vent and hem simulate (I).
  - The Outfit Asset is Beta in 5.8 (PIPELINE-2026-09-30) (D).

## 6. Driving MD 2026 by Python

- **No start-up script, start-up folder or command-line flag was found** (D, by absence). A .py registered in the Plug-in Manager still needs a click [13] (D).
- One bridge lists itself at launch through `pluginSettings.json`, yet still needs a click after each restart. It was verified on 2026.0.315 [14, 15] (D).
- `ImportFile` opens dialogs. Use `ImportZprj`, `ImportFBX` or `ImportZpac` with options instead. There is no DXF import call [13] (D).
- **Calls that exist** [13] (D): `SetPatternLayer`, `SetParticleDistanceOfPattern(s)`, `SetAddlThicknessCollision`, `SetPatternPieceSeamtaping` (no preset choice), `SetSimulationQuality`, `ExportUSD` with `m_bExportSimulationData`, and pattern JSON and ZPRJ in and out. `SetPatternPieceElastic` at a 100% ratio neither stretches nor shrinks [12] (D), so it can stand in for tape (I).
- **Calls that do not exist** [13] (D, by absence): fold angle, fold strength, Fold Arrangement, Strengthen, Bond, shoulder pads, and placing buttons (only their colours can be set).

## Not found

- A dated professional breakdown of a tailored jacket in MD. Videos were found but have no transcripts; ArtStation and CLO pages were refused.
- Whether JSON or ZPRJ templates keep fold angles and Bond.
- The full 2026 preset list.
- Epic's 5.8 Outfit pages, which redirect.
- The builds of the Construction Presets.
- Measured photographs of 1990 high-street suits.

## Sources (all reached 1 October 2026)

1. "Marvelous Designer to MetaHuman: USD Garment Integration Workflow", MD Team, 9 Dec 2025, support.marvelousdesigner.com/hc/en-us/articles/52699135975705 (read in full)
2. "Fold Arrangement", MD manual, 29 May 2025, …/articles/47358260153881 (full)
3. "Fold Pattern", MD manual, 29 May 2025, …/articles/47358354961049 (full)
4. "Fold Seam Line", MD manual, 29 May 2025, …/articles/47358411649305 (full)
5. "Strengthen / Unstrengthen", MD manual, 29 May 2025, …/articles/47358253657497 (full)
6. "Seam Taping", MD manual, updated 7 Jan 2026, …/articles/47358218656921 (full)
7. "Bond", MD manual, 29 May 2025, …/articles/47358358998809 (full)
8. "Avatar (*.avt) Add", MD manual, 29 May 2025, …/articles/47358359735961 (full)
9. "MetaHuman DNA Importer", MD manual, 30 Oct 2025, …/articles/51752244831897 (full)
10. "Suit: Pants, Shirt, Jacket and Layering", MD, 29 May 2025, …/articles/47358198497305; video "9.5 Marvelous Designer Suit: Jacket", 11 May 2020, youtube.com/watch?v=GGlsBuQ2Biw (page and description; no captions)
11. "Marvelous Designer 9.5: Blazer Modular Configurator", MD, 12 May 2020, youtube.com/watch?v=5QPxLYqBWhk (description only)
12. "Creator's Field Guide, 2024 Edition", CLO Virtual Fashion, June 2024, s3.marvelousdesigner.com/newmdweb/case/20240626/MD+User+Guide+2024.pdf (relevant sections)
13. MD API: API List, ApiTypes, Plug-in Management, Changelog to 2025.1.201, undated, developer.marvelousdesigner.com (searched in full)
14. Laboon2501/MarvelousDesigner-MCP, GitHub README, undated (read)
15. dcc-mcp/dcc-mcp-marvelous-designer, GitHub README, undated (read)
16. "Constructing a Collar/Lapel", CLO support, undated, support.clo3d.com/hc/en-us/articles/115013191087 (search summary only; sign-in wall)
17. "Bond: How to Add Interlining / Fusible / Reinforcement", CLO support, undated (search summary only)
18. "Marvelous Designer 2025 Fabric Preset Reference Chart", Maryam Winartomo, ArtStation, about 17 Oct 2025, maryamwinartomo.artstation.com/projects/5Wxvlw (text and chart 3 of 3)
19. "Wool Weight Conversion", Ask Andy About Clothes forum, undated (search summary only)
20. "MetaHuman Clothing Construction Presets, Set of 4" and "Set of 2", Epic Games on Fab, 3 Jun 2025, updated 12 Nov 2025, fab.com/listings/3c0c4df1-ce96-44cf-8a30-c47d744d2a0c (read)
21. "MetaHuman Clothing Construction Presets, Set of 4" thread, Epic forums, Jun to Aug 2025, forums.unrealengine.com/t/…/2538920 (read via summary)
22. "Creating Your MetaHuman Characters", Epic, undated, dev.epicgames.com/documentation/metahuman/creating-your-metahuman-characters (read)
23. "Metahuman Parametric Wardrobe asset missing cloth simulation 5.8", Epic forums, 19 Jul 2026, forums.unrealengine.com/t/…/2736828 (read)
24. "Tailoring for MetaHumans: CLO and Marvelous Designer to Unreal Engine demo", Epic, 24 Apr 2026 (page read; webinar not watched)
25. "Marvelous Designer 2025.2: MetaHumans, Pleats & Keyframes", Digital Production, 18 Nov 2025 (read)
26. Jaeger: overview, options, instructions, FreeSewing, undated, freesewing.eu/docs/designs/jaeger/ (read)
27. "The Last 1980s Suit: Navy Pinhead Suit in Licence to Kill", Matt Spaiser, Bond Suits, 15 Aug 2013 (read)
28. "Tailoring for the Times: Timothy Dalton", Matt Spaiser, Bond Suits, 2 Aug 2012 (read)
29. "How relevant is 80s Armani?", Permanent Style, Jul 2021 (search summary only)
30. "Classic Style and the Suit's Ideal Proportions", Bond Suits, undated (search summary only)

Earlier notes relied on: MD-SCRIPTING-2026-09-29, PIPELINE-2026-09-30, TAILORED-ROUTES-2026-09-30, pattern-jacket-2026-09-29.
