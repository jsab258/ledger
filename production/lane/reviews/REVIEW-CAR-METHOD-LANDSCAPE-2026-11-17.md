# Review: CAR-METHOD-LANDSCAPE-2026-11-17.md (17 November 2026)

Fresh independent reviewer. File reviewed: production/research/lane/CAR-METHOD-LANDSCAPE-2026-11-17.md. Not edited.

## Verdict: PASS WITH FIXES

The facts I checked hold. The licence reasoning follows the allowlist and the rulings. The recommendation (keep the loft, add variety through data) follows from the evidence and does not lean on anything it could not reach. The fixes below are wording, two missing rulings in the table, and two points a professional would name before the Blender pass.

## Spot checks (six claims, each page fetched 17 Nov 2026)

- [B1] Car Primitives: $19.95 commercial, $119.95 unlimited, $11.95 non-commercial, GPL, Blender 3.5 minimum, 13 Geometry Nodes inputs as listed. Matches. One wording slip (finding 1).
- [B2] Vehicle Forge: $19, GPL, Blender 5.0 to 5.2, 32 types, cars about 2,500 to 3,500 triangles, no UVs, no textures, no interior, no LODs. Matches.
- [A2] GTPlanet: an izmo artist in Bangalore, built from Polyphony's scans rather than CAD, about three months against the usual six. Matches.
- [A3] Virtuos: "roughly 90% of the vehicles", modelling, UVs, texturing, engine integration. Matches.
- [B5] Houdini Indie: $299 a year, revenue under $100,000, Apprentice free and non-commercial, page dated 19 Aug 2026. Matches. The page also sets a funding cap under $1 million and says Indie files use their own format (not needed for the verdict).
- [B6] TRELLIS.2 ROCm port: MIT, tested on a 7900 XTX under Ubuntu 22.04, "8 GB+ workable", RDNA2 untested and may hit Triton kernel problems, Windows not covered. Matches.

Local checks: RULINGS.md line 61 holds the 22 Sep image-to-3D hold as quoted. "Never-ship item 5" is used the same way in N09-13. car_loft.py sets TRIANGLE_BUDGET = 40000 and has a triangle_estimate. The file openly says the GPL ruling was not found by that word in RULINGS.md. That is honest, and it is the right way to handle it.

Style: no em-dashes, no italics. Plain English throughout, apart from finding 6.

## Findings and fixes

1. The Car Primitives date is merged with the product's age. The page says the product was published "almost 4 years ago" and gives no date for version 1.1.4. Its update notes mention Blender 4.0, 4.3 and 4.4, so the last update is recent. Fix in Part B, Car Primitives: replace "last version 1.1.4, published about four years ago" with "first published almost four years ago; last version 1.1.4, undated; update notes mention Blender 4.0, 4.3 and 4.4".

2. Two table rows leave out the rulings that close them. In the "Licence vs allowlist" column, the TRELLIS.2 row says only "MIT, allowlisted" and the Meshy / Tripo row says "allowlisted paid tiers (purchase)". Fix: add "held by 22 Sep ruling (image-to-3D)" to both. Add "and 16 Sep (nothing bought for cars)" to the Meshy / Tripo row.

3. The cheapest route depends on materials that were not read today. "Epic's free automotive materials" rests on N09-13 and on a headline [S4] that names UE 5.7, not 5.8. Fix: after "the loft plus Epic's free automotive materials", add "(free and Epic's own per N09-13; their page was not read today, so check the Fab licence and tag and whether they load in UE 5.8 at download, and name them in THIRD-PARTY.md)".

4. The recommendation is missing a pro point: the level-of-detail and glass split before the Blender pass. Part A point 5 and N09-13 (line 54) both say each car needs checked LODs or a checked Nanite fallback, after the 1 Oct finding. Whether glass can be Nanite is marked unverified. A professional settles both before the first export, not after. Fix: add one sentence to the Recommendation: "The first Blender pass exports glass, wheels and body as separate meshes, and the export step checks the Nanite fallback or hand-made LODs at street distance; whether see-through glass can be Nanite in UE 5.8 is researched from Epic's 5.8 page before that export."

5. The recommendation is missing a pro point: how panel detail fits the budget, and variety by shape. [A1] already says the budget is shared out per part and livery goes on as decals. A professional would also name panel gaps, rubbing strips and badges-removed trim as a trim sheet or normal-map decals, not modelled cuts. They would also name a few fixed-topology shape keys per class (bumper style, ride height, a three- or five-door rear) as the cheap mesh-level variety, sitting under the material variety. Fix: add to the "Copy the professionals' variety method" sentence: "panel lines and trim as a trim sheet and decals, not modelled cuts; and a few fixed-topology shape keys per class (bumpers, ride height, door count) as the only mesh variety".

6. The recommendation uses an undefined term. "ROUND3_PROPOSAL" is a variable name, and the file does not say it has not been tried in a blind round. Fix: replace "with ROUND3_PROPOSAL" with "with the round-3 shape the two outline rounds pointed to (set in car_loft.py, not yet tried in a blind round)".

## Not findings

- The licence logic on Car Primitives' own base meshes (whether a body grown from them is "our output") is correctly raised as an open point for any decision record.
- City Sample Vehicles are correctly treated as needing a record. Allowlist item 8 names only Epic's animation content, and the 13 Oct exception covers only NoAI-tagged Epic content on Fab.
- Unreached sources ([S1] to [S4], the itch.io page, the Gumroad page, the GDC video) are labelled and not used as evidence. The single use of [A6] is limited to its abstract.
