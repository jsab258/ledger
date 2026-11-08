# The street sweep: rule misfits against real faults (8 November 2026)

For Monday's order (n02-9-asset-check-gaps' second half).  Not yet reviewed: a fresh reviewer checks it against the full report before it becomes the order's plan. Source: the first working sweep, 09:30 on 8 Nov, 1,849 assets, 3,340 errors (full report F:/LedgerTools/asset-checks/street-sweep.json; counts in production/asset-checks/street-sweep-summary.json). Counted by rule and folder by script; the "likely" calls below are read from names and messages, not yet opened in the editor (unverified where marked).

## Misfits: the rule is wrong for the piece (about 2,700 errors)

| Rule | Errors | Where | Why a misfit | Proposed fit |
|---|---|---|---|---|
| names | 1,838 | ShopDisplays 656, ShopFronts 618, ShopRooms 365, Street 179, Vehicles 20 | imports keep their source names (the spec's own exemption reason, study 13); the import scripts name these, not a person | rule 10 only in Kit and Props; the scripted folders exempt from names |
| lods, placeholder | 179 + 179 | Street | the street block's parts are one level's pieces whose materials the game sets at run time (StreetMeshes) | a `street_part` kind: one level allowed, empty slots allowed when the street spec names the material |
| see_through | 6 | display panes, a camera lens | "pane" and "lens" are glass but not in glass_words | add them |
| texture_role | 382 | ShopDisplays 224, ShopRooms 83, ShopFronts 67, Kit 8 | the role is guessed from the name; detail masks (T_KitDetail_*) and scan maps read as colour (unverified: open five) | read the role from the material's parameter, not the name |

## Real faults, each its own item (about 600 errors)

- Triangles: shop displays 74,000 to 702,000 against 60,000 (grocer 702,264); Mickey's fittings 478,750 against 100,000; street foliage 153,725; lamp post C 10,848 (perhaps a large prop: a kind choice). Frame and memory weight, relevant to exit D's card memory.
- Non-power-of-two textures: 269, mostly the shop fronts' sign pictures (e.g. 475x121): no mip chain, shimmer at distance.
- Missing levels of detail on props, shop fronts, rooms, displays, vehicles: 64 meshes with one level.
- Collision: 179 street meshes use complex collision as simple (each also has one hull: 358 errors). Whether a walkable street should keep it is a reference question (Mafia's street collision, studies/12-tech-budgets.md), not a rule fit.
- One stale part: the chandler's held-back joinery holds a sub-asset from an older source.

## Cost

Fitting the rules and a known list for what stays: about half a day, then the sweep can run in the build after the material step (its line read like materialStatus) and fail on new errors only. The real faults are separate items, sized each (the displays' triangles first).
