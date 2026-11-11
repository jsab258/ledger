# Epic's resizable outfits: the Wednesday verdict (item n09-6, 11 November 2026)

Ask: "Epic's resizing clothing on Tom's garments by Wednesday"; done when "the resizing verdict with numbers" (order of 9 Nov); his 8 Nov yes made Epic's resizable outfits the clothing backbone, "decided by Wednesday's resizing test". Inputs: RESIZING-READING-2026-11-08.md, RESIZING-READING-2-2026-11-09.md, RESIZING-SCRIPT-CALLS-2026-11-11.md (engine source, a helper), and a read-only probe of the built cast (tools/ue/resize_probe.py, C:/LedgerTools/mh-assemble/resize-probe.json, run 11 Nov 11:50).

## Verdict: not the backbone now, recommended; his choice, because the test his 8 Nov yes named was not run. Tom's own garments were not resized: no end-to-end script route was found for making one into a resizable outfit (below; source reading, unverified at run time). What was measured shows the route bakes an ordinary skeletal mesh per character, like ours, with its cloth simulation stripped. Recommended: keep skinned garments carried from body to body; list the crowd test for phase 5, cheapest route first (below, 'What would change the verdict').

## What Epic's resizing already does in our game (measured)
The four built cast members probed all wear an Epic resizable outfit: the white base layer is WI_DefaultGarment (OA_DefaultGarment, six source garments CA_DG_bodyShapeA to F on six source bodies). At each character's build the pipeline picks the nearest source by measurements, warps it to the body (RBF interpolation, 1,500 sample points by default) and bakes it to a skeletal mesh in that character's folder.

| Built mesh | source shape chosen | on disk | detail levels | cloth simulation kept |
|---|---|---|---|---|
| MH_TomL1_Outfits | A | 5.34 MB | 4, read from its 8 material slots (two per level) | none (0 legacy clothing assets) |
| MH_LenaS4_Outfits (Sheila) | A | 5.33 MB | 4 | none |
| MH_RoccoP2_Outfits (Ron) | D | 4.90 MB | 4 | none |
| MH_Test_Outfits | E | 10.14 MB | 4 | none |
| our SKM_TomJumper (skinned, carried) | none | 4.39 MB | | none |
| our SKM_TomZipJacket | none | 4.28 MB | | none |
| our SKM_TomJeans | none | 2.23 MB | | none |

The probe read sizes, slots and legacy clothing assets; detail levels are inferred from the slots. Vertex counts did not read in a commandlet (two tries, none read), so they are not shown.

So: (1) the result is an ordinary baked skeletal mesh per character, the same kind and about the size of ours on disk (its run-time cost was not measured); (2) nothing resizes while playing (Epic staff: run-time resizing "not currently possible"); (3) the simulation is stripped on the way by Epic's own account (its 5 Aug 2026 forum reply; our probe shows no legacy clothing on the baked meshes, consistent with it), unless a Strip Sim false variant or Epic's Resizing Graph workaround is used (not tried here). None of our carried garments simulate either, so this is no point against Epic's route; the probe reads legacy clothing assets only and cannot show a Chaos cloth.

## Why Tom's garment was not run through it
From the engine source (RESIZING-SCRIPT-CALLS-2026-11-11.md, file and line for each):
- A resizable outfit needs each garment fitted on a source body given as a combined head-and-body mesh. The call that makes one for a character (CreateCombinedFaceAndBodyMesh) is C++ only (MetaHumanCharacterEditorSubsystem.h line 819, no UFUNCTION).
- New cloth and outfit assets get their graph from a template picker that opens a window; scripts get an empty asset. Our 1 Oct cloth work got round it for one cloth asset by duplicating Epic's template (tools/ue/make_cloth_jacket.py, DF_StaticMeshClothTemplate), which may also work for the outfit (unverified).
- Re-running a graph and setting its inputs (target body, strip sim) are scriptable. Adding a wardrobe item: the sources disagree. RESIZING-SCRIPT-CALLS s3 and s4 found no script call that adds an outfit to a character; yet tools/ue/dress_metahuman.py logged 'metahumanDress=DRESSED ... default-garment' on 24 Sep (collection.try_add_item_from_wardrobe_item, C:/LedgerTools/mh-assemble/ue-material.txt), on an earlier engine. Unverified on 5.8.2 until run.
- The route left: duplicate Epic's outfit, swap its six sources for Tom's jumper on Tom's combined body, wrap it as a wardrobe item, add it to Ron, build, and measure the fit against Ron's own carried jumper. That needs a small editor function in C++ for the combined body (Geometry Export already makes a combined body mesh by another route, 28 Sep note, which may serve instead). About 4 h, an uncosted estimate. It was not started. Other routes, not tried: Epic's free Techwear outfit through the pipeline (a Fab download needing his sign-in; licence field blank), the Creator's Hair & Clothing screens by hand (his hands; computer use is Marvelous only), and the partial script route's first steps (duplicating Epic's outfit, unverified).

## Against our own route
Our skinned garments are carried between bodies that share the MetaHuman layout by tools/meshgen/blender/carry_garment.py: today Sheila's blouse (carry 1 try, skinning 2 tries, about 0.4 h) and her skirt (carry 1 try, clearance 2 tries, about 0.3 h; SHEILA-*-S4-2026-11-11.md). The faults that remain (a skirt through the thigh, a band edge) are fit and motion faults; whether Epic's warp would have them too is untested.

## What would change the verdict
A crowd of many different bodies per garment (phase 5), where one outfit with a few sources could fit dozens of people at build time without a hand carry for each. That is the place to try it, cheapest route first: (a) the partial script route's steps 1 to 4 (duplicate Epic's outfit, set its graph inputs, regenerate; RESIZING-SCRIPT-CALLS), never tried; (b) Epic's free Techwear outfit through the same pipeline for a real baked-mesh vertex and frame-cost reading (his sign-in on Fab); (c) the Creator's Hair & Clothing screens by hand (his hands); (d) the C++ helper. Listed for phase 5's design.

Corrected 11 Nov after advisor 99 against the review's fixes (RESIZING-VERDICT-REVIEW-2026-11-11.md): run-time, script-route and simulation lines marked unmeasured, the wardrobe-item disagreement stated, the cheaper tests listed first.

Cost: about 1.2 h (one helper reading engine source, two commandlet probes); no API spend.
