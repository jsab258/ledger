# Review of RESIZING-VERDICT-2026-11-11.md (item n09-6, fresh reviewer, 11 Nov 2026)

Result: PASS WITH FIXES (sources read in full; one engine header spot-checked).

## Numbers
- Table sizes (5.34, 5.33, 4.90, 10.14, 4.39, 4.28, 2.23 MB) match resize-probe.json diskBytes. Shapes A/A/D/E come from material names, not a field: inference, fine.
- "4 detail levels" is not in the probe (lods null, lodRows empty). It is 8 material slots divided by two, plus Epic's "four body LODs" (READING 8 Nov). Say "inferred".
- "0 clothing assets" is mesh_clothing_assets (legacy clothing) only. It cannot show a Chaos cloth; "none" for simulation is stronger than the probe.
- 1,500 points, 5 Aug 2026 reply, "not currently possible": match the readings.
- Sheila carry times: blouse note says about 0.4 h, skirt 0.3 h; verdict says "about 0.3 h each". Blouse skinning took 2 tries; skirt clearance took 2 tries (band top still ragged). "In 1 try" holds for the carry step only.

## Claims stronger than source
- "The game pays the same at run time" (line 22): no vertex, draw or frame number exists (probe vertex reads failed; READING-2 s3: "would have to be measured"). Disk size is not run-time cost. Sizes also differ (Test 10.14 MB vs 4.39 MB).
- "Has no script route here": SCRIPT-CALLS says "none found end to end", every step "unverified at runtime", and lists a partial route (duplicate OA_, SetDataflowNodeProperty, RegenerateAssetFromDataflow). The verdict also says adding a wardrobe item is scriptable, but SCRIPT-CALLS s3 and s4 say "No script call adds an outfit to a character". Direct contradiction.
- "The simulation is stripped on the way": Epic says Creator's graph strips it, and a Strip Sim false variant exists. Not the same as "a baked mesh always loses cloth".
- "Faults Epic's warp would have too": no source; not tested.
- "Our 1 Oct cloth work got round it": no cited file. "About 4 h": an estimate, uncosted.
- "Every built cast member": the probe covers four.
- CreateCombinedFaceAndBodyMesh "C++ only": confirmed in MetaHumanCharacterEditorSubsystem.h:819 (plain C++ declaration) and the 28 Sep note, but missing from SCRIPT-CALLS. The same note shows Geometry Export already makes the combined body mesh by another route.

## Honesty against the order
Order n09-6 asked for Epic's resizing "on Tom's garments" and a verdict "with numbers". The verdict states plainly that Tom's garments were not resized. It does not say that his 8 Nov yes was "decided by Wednesday's resizing test", and that the test was not run. The title "not the backbone now" is a decision made without the test.

## Recommendation
Keeping carried garments is supported for now (Sheila blouse and skirt exist). The case that no cheaper real test exists is not made. Unlisted cheaper options: (a) Epic's free Techwear Outfit in the same pipeline, giving a real baked-mesh vertex and cost reading (READING-2 item d); (b) the Creator Hair & Clothing path from READING-2 s4, a hand route needing no script; (c) the partial script route's steps 1 to 4, which were never tried. The 4 h C++ helper is one option, not the only one.

## Fixes
Reword the run-time, script-route and simulation lines as unmeasured. Correct the contradiction on adding a wardrobe item. Give the blouse 0.4 h and 2 tries. State that the Wednesday test was not run and list (a) to (c).
