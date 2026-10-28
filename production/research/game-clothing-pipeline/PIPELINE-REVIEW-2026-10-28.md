# Fresh review of PIPELINE-2026-10-28.md (28 October 2026)

Reviewer: fresh, independent, read only. Every web page below was opened on 28 October 2026 and its passage read in the built-in browser (Zendesk pages refuse plain fetching) or by a page fetch; nothing was downloaded or signed into; no fetch saved a file. Project files read only. Installed program confirmed: MarvelousDesigner_Personal.exe, file version 2026, 1, 237, 58920.

## Confirmed (no fault)

- **Properties table:** Elastic (CLO 115012380228: strength "default value is 10", "recommended"; ratio "between 0 and 200", "Smaller the percentage is, shorter the length"); Shrinkage default 100%, 3D only, "temporarily to draw the inner layer"; particle distance 20 mm / "under 5mm" / 0.8 to 700; Layer 0 = off, back to 0 "for more stable simulation"; collision thickness "1.5mm on each side" and the 2026.1 direction note; skin offset 0 to 100, default 3, lower with particle distance; fold angle 0 to 360, 180 flat, strength 0 to 20; seam Turned/Tension/Sublayer; pressure for padding; fabric stretch (lower = more elastic).
- **Python API (list.html, synced 2026.1):** every call in "Calls the skill will use" exists with the arguments and returns stated, including the docstrings quoted (AddSeamlinePairGroup "return name of sewing group"; AddSeamlinePairGroupPartial 0 = success, negative = error; FlipPatternNormal all-or-nothing, simulate after; SetMeshType "to get mesh count information"; SetSimulationQuality 0 Normal, 1 Animation, 2 Fitting (Accurate Fabric), 3 FAST(GPU); gravity default -9800; UVPacking padding, genetic search, fidelity 1 to 5; CombineZfab base = physics, target = image; Attach/SetPatternEdgeToAvatarMeasure run the solver, refuse height/linear measures, lengths in mm). CutPatternAlongInternalShapes is absent from the docs. No fold, seam-tension, Turned, Sublayer, remesh, retopology, EveryWear, strain, pressure, stretch, bending or density call exists in the docs. No call places a zipper. -1600 "Low gravity" is in the Simulation Physics scenario. The changelog says what the document says (139 added, JSON pattern calls always False, "declared but not implemented" removed).
- **Item 3, the Game-Ready Export scenario:** right. It sets 15 mm on every piece, Simulate(60), UVPacking(True, False, True, 0.005, 2, [0, 90]), thick, single object, unified UVs, 2048 unified diffuse and normal, scale 0.1, BakeUVTexture, ExportOBJ and ExportFBX; no retopology, LODs or skinning. "Triangle" is the program default (the scenario sets no mesh type; the mesh article advises triangles). Retopology tools, Remeshing to Retopology and EveryWear (polygon count, Auto Seal, weight transfer, brushes, Auto Fitting on a fitting suit, avatar with joints) are window-only: no API call. CLO's Unreal guide: "Unreal Engine supports a maximum of 8 joints, so we set it to 8."
- **Garment Inspection Report scenario:** name, area_mm2, width, height, fabric, particle distance, layer; CSV and JSON; largest piece tinted red; the four calls proposed to add all exist.
- **Licence:** MD Additional Terms updated 23 Oct 2026; 1.2 CLO Samples include "sample patterns and designs, modules for patterns and designs"; 3.1 grants "for the limited duration of the applicable License Term", including (b), the licence in a CLO Sample inside a Modification; 4.3c forbids distributing or modifying Restricted CLO Samples; AI terms (30 Mar 2026) quote right. Consistent with MD-LICENCE-2026-10-26.md.
- **Cuff arithmetic:** 188 + 2 pi x 5.5 = 222.6 mm; 0.90 to 0.95 of it = 200 to 212; 205 / 231 = 0.89; elastic strength 10 and shrinkage 100 are the defaults. Drape 19's 13 points (8 + 5, 7 to 22 mm), 69 edges past 15 mm, 57.5 mm longest, lump: as SLEEVE-END says.
- **Measured triangle constant:** drape 19's cloth is 47,403 triangles over 1.2175 m2 (re-measured); its 10 mm pieces give 0.0356 per mm2, the cuffs 2.2 per d2. The 19,100 / 10,700 / 43,000 figures follow.
- **Mafia:** 2K page quotes right (no author or date). Study 6 numbers in section 1 (19,131 / 8,509 / 4,781 / 1,505; median top 21,994; LOD 47/25/9 %; screen sizes; 2048 shipped; no crowd cloth) match the study and JACKET-2026-10-28.md.
- **Other sources:** DigixArt (zero gravity against T/A-pose creases; tailors and pattern sites; "thin and unweld single"; polygroups, weld, subdivide, thickness last; black-and-white masks, colour in Unreal); Supermassive (unwelded, no thickness, UV as pattern; newer tools "could now be used"; flat Couture retopology); CLO forum 360020807153 and 900003087483; MD forum 48272311635097 and 48272815935641; Gears Tactics (100K to 120k vertices; LOD1 75%); MetaHuman body 30,500 vertices; RUBRIC's 1280 / d and 4.4 m; RULINGS 2 Oct (count body points first) and 3 Oct (clothes not judged on the Hook sheet); 1.55 to 1.79 px/mm (BAKE-PLAN).

## Faults

**1. The grip's length in try 3 and drape 19 is double-counted (item 4).**
- Document: "the grip asked for about 168 x 0.85 = 143 mm, about 0.64 of the 223 mm floor."
- Source (tools/md-bridge/zip_jacket.py; job_v9 to v19 plans): `WRIST_MM, CUFF_OF_WRIST = 197.1, 1.0`; cuffs drawn 197.1 x 60; `GRIP = 85` applied by SetWidthShrinkagePercentage.
- Correction: the cuff was cut at 197.1 mm and its width shrunk to 85% in 3D: about **168 mm, 0.75 of the floor**, not 143 and 0.64. Only try 2 (drape 8) was cut at 167.5 mm, and it had no grip. The conclusion (asked below the floor) stands with 0.75.

**2. What the sleeve end was sewn to (item 4).**
- Document: "a 231 mm sleeve end was sewn to a 168 mm cuff (ratio 0.73)".
- Source (job_v19.py): cuff 197.1 mm wide; 400 steps open plus 1,000 sewn, then `SetWidthShrinkagePercentage(..., 85)` and 200 + 100 steps.
- Correction: sewn to a 197 mm cuff (0.85) for the drape; its 3D width was shrunk to about 168 (0.73) only in the grip.

**3. The recipe's placement numbers come from the wrong body and the wrong drape.**
- Document: "position Y 25 (measured at the wrist); offset 40".
- Source: zip_jacket.py "on the straight-elbowed body Y 0 and offset 30 put an unsewn cuff nearest the wrist" (cuff_arrange4.py); job_v19 `CUFF_POS = [50, 0, 30]`; job_v20 `[50, 0, 40]`, the worse drape (SLEEVE-END).
- Correction: Y 25 was measured on the bent reference body (round 3); offset 40 is the sleeve's. On the straight-elbow body use Y 0, offset 30 (drape 19), and say offset 40 failed in drape 20.

**4. The weld options are documented.**
- Document: "the live options carry weldType (default FULLY_UNWELDED) ... its other values are UNVERIFIED" (and again under Unverified).
- Source (developer.marvelousdesigner.com/optiontype.html, WELD_TYPE): "FULLY_UNWELDED = 0 ... DEFAULT_WELDED = 1 # deprecated ... FULLY_WELDED = 2 ... SELECTED_WELDED = 3".
- Correction: state the four values; FULLY_WELDED welds every seamline; never use 1. Remove it from Unverified.

**5. LEDGER's targets labelled as Mafia's numbers (item 5).**
- Document, section 6: "Mafia's numbers (Study 6): jacket 18,000 to 22,000 triangles ... levels of detail about 50, 25 and 10%".
- Source (Study 6): "All of this is our choice, not a measured target"; Mafia's levels keep "a median 47%, 25% and 9%".
- Correction: head them "LEDGER's target (Study 6)"; Mafia's are 19,131 for the jacket, a 21,994 median top, LODs 47/25/9 %.

**6. Two Mafia numbers missing from the checks (item 5).**
- Document, step 9: "8 influences at most"; step 7: "cloth at 1.5 px/mm or more at 2048"; section 6: "No studio publishes ... a character texel density".
- Source (JACKET-2026-10-28.md): "Up to 8 influences at the top two LODs, 4 below"; "even texel density of about 12 px/cm at 2048".
- Correction: step 9: 8 at LOD0 and LOD1, 4 at LOD2 and LOD3. Step 7: Mafia's jacket measures about 1.2 px/mm; 1.5 is the project's own choice above it.

**7. "All window-only" overstates (item 3).**
- Document, section 5: "all of it window-only, none in the API" (the Quad (Grid) and Quad (Optimized) styles first).
- Source: `SetMeshType(_patternIndex, _meshType)`: "Triangle", "Quad" (list.html); CLO's Unreal guide: "Marvelous Designer's Quad Optimize option can achieve auto retopology."
- Correction: Quad (Grid), Remeshing to Retopology, Topology and EveryWear have no call; a "Quad" mesh type can be set by SetMeshType, and whether that is Quad (Optimized) is untested. Also: Quad (Optimized) is in 47358367597081, not 47358347315481 (Remeshing, Quad (Grid)).

**8. The strain cap's source is the older page.**
- Document: "blue at 100% to red at 120% (Global; 47358286228505)".
- Source: 47358286228505 (Fit Maps): "Red indicates a 120% of distortion rate"; 56518392287513: Global runs to "the user-defined fixed standard (Maximum)".
- Correction: 120% is the Fit Maps article's colour scale; in 2026's Strain Map the Global maximum is user-set. The 1.2x mark is the project's choice anchored on that scale.

**9. The MetaHuman LOD figures are cited to the wrong page.**
- Document: "Epic's MetaHuman outfits remesh to 50, 30 and 10%" (S13, the LOD specifications).
- Source: S13 gives only "Body Vertices | 30500 | 7600 ..."; Epic's parametric-outfit tutorial: "For this tutorial ... LOD[1] ... 50 ... LOD[2] ... 30 ... LOD[3] ... 10".
- Correction: cite dev.epicgames.com/documentation/metahuman/building-a-metahuman-parametric-outfit-with-a-render-mesh and call them a tutorial's example values.

**10. The "T-pose" quote is a legacy COLLADA workflow, uncited.**
- Document: "Marvelous's manual drapes on 'a T-pose avatar which can be easily draped', then poses."
- Source: article 47358445646489, "Change Pose by Collada's Joint Information": "Export a T-pose avatar which can be easily draped and an avatar with the final pose in COLLADA files."
- Correction: cite 47358445646489 and say it is the COLLADA (DAZ/Poser) pose-change route, not a general rule.

**11. One gown made into a studio's practice.**
- Document: "Supermassive drapes in A-pose [H]."
- Source (S2): "I created the gown in A-pose in Marvelous Designer".
- Correction: "Supermassive's artist made one gown in A-pose."

**12. An uncited claim.**
- Document: "CLO's rigging guide rigs in the bind pose."
- Source: none in the document or HELPER-SOURCES. EveryWear's page (45304301912857) describes weight transfer and does not mention a bind pose.
- Correction: cite it, or mark it UNVERIFIED.

**13. A forum post says less than stated.**
- Document: "ribbing is cut 'slightly smaller' than the edge, with the fabric's weft stretch lowered (... 360000697127)".
- Source: "Since the ribbig stretches well, ajust Stretch physical properties."
- Correction: "with its Stretch properties adjusted". Weft-only stretch comes from 360020807153.

**14. Inside-out cuffs overstated.**
- Document: "Marvelous turned each cuff inside out at its seam."
- Source (zip_jacket.py): the right cuff, cut unmirrored, "had to turn inside out through itself to be sewn" (27 Oct, fixed by mirroring); a twisted seam "the right cuff met it once". RIB-CUFFS and SLEEVE-END describe flat doubled bands.
- Correction: "the right cuff once turned through itself at its seam; since then the cuffs closed as flat doubled bands."

**15. The live program has a pin-adding call.**
- Document: "No tack call exists; other pins can only be counted or removed."
- Source: MD-API-2026.1.237.json lists `AddPinsForFabricValidation` (absent from the docs; RIB-CUFFS's review: it "adds pins").
- Correction: add "the live program also has the undocumented AddPinsForFabricValidation (purpose untested)".

**16. The floor rests on an unstated reading of the thickness value.**
- Document: "188 + 2 pi x 5.5, about 223 mm", with 5.5 = 3 mm skin offset + 2.5 mm collision thickness.
- Source (47358430412441): "set 1.5mm on each side, for a total of 3mm"; the field's value is not said to be per side or total.
- Correction: mark it UNVERIFIED that the 2.5 mm read is a clearance per side. If it is a total, the floor is about 215 mm and 0.90 to 0.95 gives 194 to 204 mm.

**17. The licence point is already settled by law, not a page question.**
- Document: "Licence points found (for his page if they bite)"; "Zipper teeth, sliders and pullers are trims, so 'Restricted CLO Samples' (1.7)".
- Source: license-allowlist never-ship 5: "Marvelous Designer's own avatars, sample garments, patterns and trims". 1.7 names "trims and accessories (including ... buttons, shoes, headwear, socks, and gloves)", not zippers.
- Correction: cite the allowlist (no page needed). Mark "zipper parts are trims" as the project's reading of 1.7 (sound, but not CLO's words).

**Small:**
- "Drape 19: 2 of about 1,175 under the cuffs": the source says 2 per side ("2 points poke through on each side").
- The recipe's "body pieces at 10 mm, 400 steps": drape 19 ran 400 steps open plus 1,000 sewn. Say whether 400 is new.
- Pressure "By script? not checked": the docs have no pressure call, so the answer is "no".

## Verdict

**Pass with fixes.** About 140 claims checked: the Marvelous property names, units and values, the API calls, both scenarios, the window-only finding and the licence claims stand. The faults are in the project's own history and recipe (1 to 3), one missed documented type (4), Mafia's numbers (5, 6) and source attributions (7 to 17). Fixes 1 to 6 must land before this becomes the skill. 17 faults plus 3 small points.
