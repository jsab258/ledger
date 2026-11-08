# The street sweep: rule misfits against real faults (8 November 2026)

For Monday's order (n02-9-asset-check-gaps' second half). One fresh review (Sonnet, 8 Nov): PASS WITH FIXES, fixes applied (F:/LedgerTools/asset-checks/review-2026-11-08.md). Source: the first working sweep, 09:30 on 8 Nov, 1,849 assets, 3,340 errors (full report F:/LedgerTools/asset-checks/street-sweep.json; counts in production/asset-checks/street-sweep-summary.json). Counted by script; "unverified" marks what the data does not show.

## Misfits: the rule or spec is wrong for the piece (about 2,580 errors)

| Rule | Errors | Where | Why a misfit | Proposed fit |
|---|---|---|---|---|
| names | 1,838 | ShopDisplays 656, ShopFronts 618, ShopRooms 365, Street 179, Vehicles 20 | imports keep their source names (the spec's own exemption reason, study 13) | rule 10 only in Kit and Props; the scripted folders exempt |
| lods, placeholder | 179 + 179 | Street | the street block's parts are pieces of one level; each has one slot named "-1" drawing WorldGridMaterial. That the game sets their materials at run time (StreetMeshes) is unverified from this data | a `street_part` kind with one level, once the run-time material is confirmed in a packaged picture |
| texture_role | 382 (275 textures) | ShopDisplays 224, ShopRooms 83, ShopFronts 67, Kit 8 | the role is matched on case-exact suffixes: 125 normal maps (_nor_gl_1k, lowercase _normal), 143 ARM, ORM and roughness maps, 7 Kit masks are all read as colour; none is a colour map | match suffixes case-blind and add _nor_gl, _arm, _orm, _roughness |
| collision (hulls) | part of 373 | Street 179, ShopFronts 15 | the frontage kind needs simple collision but allows 0 hulls, a contradiction in the spec | allow a few hulls or boxes on frontages |
| see_through | 2 of 6 | display panes, a camera lens | "pane" and "lens" are not in glass_words (only "glass") | add them; decide suction_pvc (a suction cup, not glass) and lamp post C's bowl |

## Real faults, each its own item (about 700 errors)

- Triangles: shop displays 74,218 to 702,264 against 60,000; Mickey's fittings 478,750 against 100,000; lamp post C 10,848 against 5,000 (perhaps a large prop: a kind choice); street foliage 153,725, 2.5% over (a kind choice).
- Texture sizes: 219 findings on 120 textures not a power of two, mostly the shop fronts' sign pictures (e.g. 475x121); 50 over their kind's size cap. That they draw without mips and shimmer is unverified (the check does not read mips).
- Once roles are read right: 129 ARM and ORM maps on default compression and 13 on the editor-icon setting will fail "packed maps on mask compression", a real list.
- Placeholders: 19 props with empty material slots; 12 textures of one flat colour; lamp post C's bowl samples no texture; 37 non-street placeholder errors in all.
- Missing levels of detail: 64 meshes with one level (props, shop fronts, rooms, displays, vehicles).
- Collision: the 179 street meshes use complex collision as simple. Whether a walkable street keeps it is a reference question (Mafia's street collision, studies/12-tech-budgets.md).
- One stale part: the chandler's held-back joinery holds a sub-asset from an older source.

## Cost

Fitting the rules and spec and a known list for what stays: about half a day; then the sweep runs in the build after the material step (its line read like materialStatus) and fails on new errors only. The real faults are separate items, sized each (the displays' triangles and the packed maps' compression first).
