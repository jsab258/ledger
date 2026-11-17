Method researched: 04-street-world.md

# Target: props and dressing, Quay Street (17 Nov 2026)

What dressing the street needs and where it comes from; not the build. Waiting item 3 of the order. "Read 17 Nov" means read today. "Judgement" means no source sets the number. "Unverified" means no page read confirms it. Furniture already targeted (lamps, kiosk, pillar box, bollards, rails, plates) is in TARGET-STREET-FURNITURE-2026-11-17.md and is not repeated.

**Questions answered.**
1. Which props a wet 1990 high street with a quay end needs, by place, with counts from the studies.
2. For each: Megascans entry, own asset already held, or own make.
3. What is period-wrong.
4. The checks and the views that see them.

**Reference first.**
- **Mafia: The Old Country** (Study 4, 25 Oct): its 73 m Palermo street holds 4.9 true props per 10 m: plant pots 1.2, boxes and buckets 1.0, laundry 0.7, lamps 0.5, signs and post boxes 0.5, seating 0.4, ropes 0.4. Ground dressing (paving, kerbs, moss, debris) is another 91 pieces in 73 m, so 12.5 per 10 m (91 / 7.3, this note's arithmetic); with it 17.4 per 10 m. Its neighbouring streets run 2.2 and 0. Dressing sits where the mission walks.
- **Kingdom Come II:** loose props (barrels, crates, carts) could not be counted (Study 4). No density number exists; its frames are only the bar.
- Quay Street's scene file places 43 props and 10 decals in 48 m, about 9 per 10 m (Study 4, from vignette-scene.json, not counted in the build). Study 4's bar: at least 5 per 10 m, ground dressing counted apart.
- Neither study gives counts per place (doorstep, kerb, alley). Per-place numbers below are Mafia's category rates assigned to the nearest place; that assignment is Judgement.

**Megascans status (read 17 Nov).** Listings opened today read Free, "Allows usage with AI: Yes", seller Quixel Megascans. The allowlist (ledger-v2/research/license-allowlist.md line 5) already admits Megascans. The header of production/specs/fab-free-megascans.md ("NEVER TO BE USED", 3 Oct) is out of date: it predates the 13 Oct ruling and the 5 Nov change (texture-pipeline/B-MEGASCANS-2026-11-10.md). That list holds decals, ground materials, food and rope, and none of it was downloaded. Nothing needs a login except adding to Jafar's library (he signs in). The Fab EULA text and Quixel's updated terms were not reached (B-MEGASCANS).

## The target

Counts: Mafia's rates times 4.8 (48 m), rounded. "Held" means a file in ledger/Assets/Props/base-mesh (CC0, The Base Mesh) or a built piece.

| # | Place and prop | Count on 48 m | Megascans entry (read 17 Nov) | Held or own |
|---|---|---|---|---|
| **Doorstep** | | | | |
| 1 | Cardboard back-stock boxes | with 4 to 5 "boxes and buckets" | Cardboard Box, 0.12 x 0.23 x 0.03 m, [05238fcb](https://www.fab.com/listings/05238fcb-94ba-478d-8500-bf86e9e84465), tags store, used, torn; a second listing [67698f37](https://www.fab.com/listings/67698f37-2754-4847-ba1a-9d015f9aa759), 0.12 x 0.22 x 0.15 m per search text only | Poly Haven cardboard_box_01 held |
| 2 | Newsagent's A-board | 1 | none | pavement_sign.glb held; Poly Haven standing_chalkboard_01 held |
| 3 | Newspaper bundles | 1 to 2 | none (Paper Trash is a litter atlas, not a bundle) | own make |
| 4 | Milk bottles on a step | 1 to 2 | none | own make (canon question below) |
| **Kerb** | | | | |
| 5 | Litter bin | 3 | none | litter-bin.glb built |
| 6 | Cigarette ends, gum, wrappers | Ground dressing, counted apart; scene holds 34 litter and 60 gum | Paper Trash, scan 0.41 x 0.41 m, 9990 px/m, tags newspaper, trash, [e083354c](https://www.fab.com/listings/e083354c-3a8a-418f-9cc6-187bfbc16b5c) | atlas pieces own make |
| 7 | Oil stain, leakage decals | median 1 per wall, at most 6 in view (Mafia, Study 4 via furniture target) | Oil Stain and Leakage decals on fab-free-megascans.md; not opened today | decals held (A17) |
| 8 | Grit bin | 1 | none | grit-bin.glb built |
| 9 | Cones (road works) | 0 to 1 | none | traffic_cone_01 and _02 held |
| **Shopfront** | | | | |
| 10 | Fish boxes, stacked | 1 stack | none | own make |
| 11 | Fruit and veg trays and crates | 1 to 2 | Wooden Storage Box, 0.3 x 0.5 x 0.06 m, [53a6cf14](https://www.fab.com/listings/53a6cf14-0cf5-46d0-b90b-71134b7c490e), tags warehouse, tray | wooden_crate_01 and _02 held; Poly Haven wooden_crate_01 |
| 12 | Bin bags | 2 to 3 | none | own make (cloth baked) |
| 13 | Goods in windows (kippers, fruit, pies) | per shop | Smoked Fish [e0b85907](https://www.fab.com/listings/e0b85907-6447-4538-a4b7-6bd2a82d3e22), Pork Pie, apples, Tea Cake (GOODS-2026-10-03 table) | fish scans are Sketchfab CC0, tags unchecked |
| **Alley and yard** | | | | |
| 14 | Galvanised dustbin | 2 to 4 | none | scene dustbin (E13) |
| 15 | Pallet | 1 | Wooden Pallet, 1.18 x 1.24 x 0.14 m, [6622c5d8](https://www.fab.com/listings/6622c5d8-691b-4f1b-a29c-80c0e9d54af8), tags industrial, worn | pallet.glb, small_pallet, large_pallet held |
| 16 | Oil drum, jerrycan | 1 to 2 | none | oil_barrel.glb held; Poly Haven Barrel_01, metal_jerrycan |
| 17 | Metal crate | 0 to 1 | Industrial Junkyard Crate Metal, 0.89 x 1.23 x 0.76 m, [3e83258c](https://www.fab.com/listings/3e83258c-676f-48b0-860c-10f16e917684) | none |
| 18 | Paint tin, oil can | 1 to 2 | Dirty Paint Can, 0.18 x 0.19 x 0.20 m, [ff3b53a0](https://www.fab.com/listings/ff3b53a0-4260-46d0-8672-21ad5fecae06); Old Metal Oil Can, 0.22 x 0.22 x 0.34 m, [f0651f11](https://www.fab.com/listings/f0651f11-ed1c-4f22-9f5c-709457a3a9aa) | Poly Haven oil_tin held |
| 19 | Skip | 0 (ruled off the street until made real, 2 Oct, per asset-plan note 3) | none | skip.glb held |
| **Quay** | | | | |
| 20 | Rope coils | ropes 0.4 per 10 m, so about 2 | Rope Coil, 0.18 x 0.18 x 0.24 m, tags nautical, dock, [8ec7aab4](https://www.fab.com/listings/8ec7aab4-8be8-442e-95ab-840a8fa32932); Bundled Rope Coil [7d418d8c](https://www.fab.com/listings/7d418d8c-8daf-4dd0-8fb5-3af2b94bd135), not opened | none |
| 21 | Lifebuoy, buoys | 1 to 2 | none | Poly Haven lifebuoy, ocean_buoy held |
| 22 | Mooring bollards, cleats | along the edge | none | own make (Lydney Harbour and Gowanus scans are references, licence unseen) |
| 23 | Fishing net on a pile | 1 | none | own make (cloth baked) |
| 24 | Chain-link fence at the yard | 1 run | none | Poly Haven modular_chainlink_fence (listed, not read) |

**Totals.** 24 prop lines. Megascans offers a usable entry for 7 (1, 6, 11, 15, 17, 18, 20), counting 13 only as an existing food list; all are scans of used or industrial goods whose British or 1990 fit is unverified (B-MEGASCANS: no page states origin). 14 lines have a held file or built piece. Own make only: 3, 4, 10, 12, 22, 23 (6 lines).
**Density arithmetic (this note's).** The furniture target counts about 14 pieces on 48 m (2.9 per 10 m); the bar of 5 per 10 m is 24 pieces, so about 10 dressing pieces from the table must be placed to reach it, and the scene's own 9 per 10 m would be 43.

## Period-wrong, to avoid

| Claim | Status |
|---|---|
| Wheeled bins in the yard: use dustbins | Internal: asset-plan 1-BUILDINGS line 118 "Never a wheeled bin". Street-clutter note: wheeled bins "spreading from the mid-1980s", uncertain per town. No external source read. Unverified |
| Plastic milk crates | "plastic crates by 1990" is an inference (asset-plan 3 B4). Unverified |
| Plastic against wooden fish boxes | Both plausible; "let a photograph decide" (asset-plan 3 B4; search summaries only). Unverified |
| Tactile paving, reflective sleeves, QR codes, LED heads, Piper "BT" logo | Street-clutter note's lists (29 Sep, helper read Wikipedia and others; not re-read today). Unverified |
| Split recycling bins, heritage cast-iron bins | Same note, marked uncertain |
| Newspaper chip wrapping | "Largely ended in the 1980s", popular articles only (asset-plan 3 C4). Unverified |
| Megascans tags and look: Smoked Fish tagged "Medieval"; Bazaar pack tagged Arabia, Persia | Read 17 Nov on the listings. The Bazaar pack (94 assets, markets and textiles) reads foreign; not a source for British stalls. Look by eye before use |
| Pallet blocks may carry brand stamps | Period note, 1 Oct (check by eye) |

## Content (canon.md lines 109 to 123)

- No beer, bottle or wine crates, betting slips, pools coupons, scratchcards, fruit machines, toys, prams, school bags, children's washing. Tobacco stays.
- Open question for the synthesis: the street-clutter note excluded "milk crates"; asset-plan 3 says milk is not alcohol so milk bottles and crates are inside canon. Not decided here.
- "Plant pots" (Mafia 1.2 per 10 m) and "laundry" (0.7) are the two Mafia categories this street does not use (furniture target); laundry risks children's clothes.

## Checks a fresh reviewer uses, and the views

1. **Density.** Count both sides, per 10 m, from the fixed kinds list (bins, signs, boxes and crates, pots, seating, lamps and posts, bikes, litter heaps, post boxes, kiosks): at least 5 (Study 4 target 2, Mafia). Ground dressing counted apart. Dressing concentrated on the walked path, thinner beyond (Study 4 target 3). Views: the day's hook camera, the reverse view.
2. **Repetition.** Mafia reuses kit meshes about 15 times in its measured street (Study 4), so repeated meshes are not a fault alone. Fail on the same mesh and same dirt twice within a glance, and on a stack that reads as one copy (GOODS rule: three to six distinct pieces per pile). Source for the fail rule: asset-plan 1-BUILDINGS line 221 ("two neighbours alike at a glance"). Views: doorstep and shopfront at 1 to 3 m, wet, by day.
3. **Period giveaways.** Run the table above line by line; any wheeled bin, plastic bin, modern sign or brand mark fails. Views: the street at night (sodium light flattens colour, so shape must carry) and the reverse view.
4. **Grounding.** Each piece sits on the ground with a contact shadow, worn, none CG-clean (asset-plan 3 B4 bar; street-weathering skill). The quay end: the view ends on a building or a turn, never open ground (Study 4 target 6).
5. **Content.** A frame sweep for the canon list.

Compared with the Hook sheet and KCD2 frames for density and wear only; neither sets a number.

## Sources read 17 Nov 2026

Fab listings (fetch tool, text of page): Wooden Pallet, Industrial Junkyard Crate Metal, Wooden Storage Box, Rope Coil, Dirty Paint Can, Old Metal Oil Can, Paper Trash, Smoked Fish, Cardboard Box 05238fcb, Bazaar. Project files: fab-free-megascans.md and .json (first 80 lines of the json; the md lists the same items), B-MEGASCANS-2026-11-10, TARGET-STREET-FURNITURE and TARGET-FISHMONGER, NEXT-PIECES-REFERENCES, 04-street-world.md, street-clutter-1990 SUMMARY, asset-plan 3-FURNITURE-PROPS-FOOD and SUMMARY (lines 190 to 235), period-vehicles-and-props NOTE, GOODS-2026-10-03 (matches only), asset-coverage DELIVERY (A8, A17, A18), license-allowlist line 5, canon.md lines 105 to 130, base-mesh file list.

## Unreached or unverified

- Quixel's updated terms and the full Fab EULA (B-MEGASCANS).
- Cardboard Box 67698f37, Bundled Rope Coil, Oil Stain and Leakage decals: not opened today. No other Megascans listing for bins, buckets, barrels, bags, cigarette ends or nets was found; the search returned only the above (a search list, not evidence of absence).
- Every image (the tool reads text only); no dated 1988 to 1992 photograph of litter, bins, crates or milk was found in production/reference (photographs.md holds none on these; the grep found nothing).
- Kingdom Come II prop density. Per-place counts. Any British or 1990 fit of any Megascans item.
- Which Megascans items are in Jafar's Fab library: none downloaded or added.
