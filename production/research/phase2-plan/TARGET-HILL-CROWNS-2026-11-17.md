Method researched: HILL-METHODS-2026-10-04.md

# Target: the hill's crowns (17 Nov 2026)

What the hill's trees must look like and cost; not the build. For waiting item 6, production/orders/2026-11-16.md section 3. Marks: **R** read in full, **I** inference, **U** unverified. Nothing measured on this card.

## 1. What the crowns look like (c. 1990, damp port town)

- **Species:** sycamore (in 89.7% of British hectads, more than any native tree; tolerant of wind, pollution and salt spray; planted on coasts; Wikipedia Acer pseudoplatanus, https://en.wikipedia.org/wiki/Acer_pseudoplatanus, first 100,000 of 109,285 characters read 17 Nov, **R**), ash, birch on waste ground, an odd lime, hawthorn and elder scrub, one churchyard yew (asset-plan/5-VEGETATION-AND-DISTANCE.md A3, 3 Oct; **I**, no photograph behind it).
- **Season:** October, mostly green and yellowing, wet (same, **I**). Real autumn colour and leaf-fall dates for the north-east or west coast: **U**.
- **Form:** the Hook sheet has a few trees between terrace rows; its "wooded valley side with loose villas" is the image model's invention, and the town bible wants contour terraces and retaining walls (production/reference/hook-sheet-audit.md lines 88-96, **R**). Bar: "lower, softer, varied, trees, mist" (RULINGS 3 Oct, **R**).
- **Photographs:** production/reference holds none of hill trees (photographs.md R06-R09 are streets, **R**). No dated 1988-92 hillside photograph has been seen: **U**.

## 2. How the two games do it

- **Mafia: The Old Country:** an edge hidden behind "a belt of generated foliage"; distant set pieces are 74 assets game-wide, 20 meshes with 8 distant versions (studies/04-street-world.md line 44, **R**). Quality levels thin foliage by 80, 60, 30% then none (meaning inferred); Nanite pool 300 MB; distant detail in two layers, instanced and merged (studies/12-tech-budgets.md, **R**). No tree count, crown size or switch distance was measured; Epic's Mafia interview returned 403 (field-scans/DISTANCE-DETAIL-2026-11-09.md, **U**).
- **Kingdom Come II (CryEngine):** vegetation ratio 70 / 110 / 250 at low / default / top; view ratio 50 / 100 / 180 (12-tech-budgets lines 19-24). Distant-detail nodes at depth 4 (5,063 of 6,920) are mostly vegetation, median radius 45 m (line 43). How Warhorse authors trees: not found.
- **Fit:** neither study gives a per-tree triangle count or switch distance at our 110 to 250 m, so no number can be copied; CryEngine's ratios do not fit Unreal.
- **Our distances:** hook camera about 64 degrees across 2,560 px, so a pixel is 4.8 cm at 110 m and 9 cm at 206 m; a 10 m tree is 165-220 px tall at 125 m (HILL-METHODS row 4, **I**). Rise tiers start at x 125, step 27 m, five tiers (terrace-front.py, read 17 Nov).

## 3. What we have, and the fault

- **Built:** `_leafy_tree` in tools/art-recipes/terrace-front.py: trunk, 11-15 boughs, about 1,300 opaque leaf triangles of 25-45 cm (800 in the far wood), dark hearts; ridge trees 10-16 m; two far-wood rows of 12 and 15 m behind the top tier (**R**).
- **Tried:** three tries, all spent (handover/TRIED-ARCHIVE.md lines 11-12). The 5 Nov review: specks, sky gaps and roof triangles reduced, but "the crowns now read as clean lumps", which it would block on. Opaque leaf triangles trade flecks for lumps; "a soft edge probably needs another method (cards or impostors)". The gaps were real holes (checked with fog off). Item closed 5 Nov: kept, listed, no further try without his yes (answers/.../hill-third-try-2026-11-04.json).
- **Listed shortfalls:** "the far hill's simple trees" (audits/gate-corner/GATE-MIDWEEK-2026-11-04.md line 20); "boxes and blobs" (PS5-GAP-LIST-2026-11-08). Haze and Lumen's 200 m limit are separate faults (HILL-METHODS findings 1-2).
- **Never built:** the planned sycamore and oak at three ages as impostors, about 30 on the hill (HILL-METHODS "What to try" 4).

## 4. Sources and cheapest method

Allowed: Poly Haven, ambientCG (CC0), Megascans and Megaplants by Epic (allowlist line 5; RULINGS 3 and 13 Oct: Epic's own content is usable even if tagged NoAI). Nothing from other sellers marked NoAI.

| Route | Evidence | Frame cost | Risk |
|---|---|---|---|
| A. Own trees: Sapling Tree Gen (GPL-3.0, Blender 4.4+) with ambientCG LeafSet027 (sycamore), 016 and 012 (oak), baked as octahedral impostors by Epic's Impostor Baker (experimental plugin, off by default; 8 triangles against a billboard's 72; three frames blended) | HILL-METHODS rows 3-4 (**R**) | under 0.2 ms for a few hundred (**I**); leaf cards 0.5 ms for 40 trees (**I**) | forum reports of foliage material faults (**U**); 5.8 state unchecked; Sapling untested on our Blender |
| B. Megaplants English Oak, European Beech, Silver Birch, Hornbeam: free, "Allows usage with AI: Yes", Nanite foliage with voxel far form | B-MEGASCANS-2026-11-10.md section 10 (**R**) | none found | Experimental, "we do not recommend shipping"; texture size and engine version not stated; voxel plus wind faults reported (**U**) |
| C. Leaf cards, nearest tier only | HILL-METHODS row 4 | as A | a 170 px frame suffices only past about 150 m (**I**) |

Poly Haven has no British broadleaf; avoid tree_small_02 and jacaranda (HILL-METHODS). Whole-hill tree budget about 0.5-1.2 ms of 2.5 (**I**). Phase 2's guess for the hill's crowns: 8 to 16 h (**I**).

**Cheapest route likely to pass (judgement, not a decision):** A, because it has no licence risk, costs least per frame and aims at the named fault, the soft broken edge. First a one-tree test: one species at three ages, baked, placed on the two near tiers, beside the hook frame. Open: Impostor Baker in 5.8; whether impostors reach Lumen (instanced foliage is in its surface cache only with Nanite). A fourth attempt needs his yes, asked once.

## 5. Checks and views

- **Views:** hook camera by day beside the last good picture, the Hook sheet's right half and the KCD2 frames; the reverse view; the street at night. At the played level (`scalability 2`), packaged, walked by the tester.
- **Reviewer asks:** crowns a broken, soft-edged mass, not clean lumps; no floating specks; no sky holes with fog off (`showflag.fog 0`); no stilt trunks above the crest; at least two species and three ages; lower than the old crest; mist softens upper rows, crowns stay legible.
- **Measures:** hook-camera frame time and peak card memory (High peak 6,103 MB against 5,771 MB, field-scans §2) before and after.
- **Fails if:** a clean lump, a lollipop or a stylised tree; the hill hazed, not built.

## Unreached

- Any 1988-92 hillside photograph (Geograph, Flickr, co-curate not retried).
- Mafia's interview (403); Epic's Nanite Foliage body; Impostor Baker in 5.8; Warhorse's tree authoring; any tree LOD distance or count from either game's files.
- Autumn colour and leaf-fall dates for the region; any cost figure measured on this card.
