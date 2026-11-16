# n16-3 step 2 design: -ScaleTest=N, -ScalePeople=M, the walk along the copies (16 Nov 2026)

Drafted by a read-only planning helper, saved by the session. Nothing built. Method: METHOD-NOTE-2026-11-16.md section 4 step 2 and section 7 (binding). Every claim carries its file:line as the helper read it; check each before code.

## Three findings that change the plan
1. quay-street.glb has 179 meshes, one per material (terrace-front.py:8767-8893, 8902-8921); only 117 lie wholly inside the street's box (x -2 to 50, |z| <= 14, under 16 m; about 59,500 faces). The other 62 (about 436,000 faces, mostly foliage) span the street and the backdrop town (street_brick_grey x -118 to 241; street_slate -160 to 251). A copy takes the 117; the straddling roofs, roads and pavements are stood in by the replaced scene pieces (ground, kerb, frontage blocks), logged as standIns.
2. The backdrop town surrounds the Hook's road lines, so copies cut through backdrop houses: accepted for a measuring switch that never reaches his page, logged; an optional -ScaleTestHideTown gives a second reading.
3. The glass bake stamps four files (tools/ue/import_glass_bake.py:38-43): quay-street.json, unreal-look.json, shop-interiors.json, vignette-scene.json. None is edited; all new data in new files.

## Where it hooks in
BuildInteractiveStreet (VignetteShot.cpp:10476) calls BuildScene (10489) then ApplyCondition (10501-10503): one new call ScaleTestBuild(World) between them, so the first ApplyCondition drives the copies too. Today's spawners: SpawnStreet 2065-2194 (one Movable actor per mesh); lamps 2986-3059 (GLanterns, GLanternPools); lit windows 3066-3082 (GWindows); PaintStreet 7474-7709 (GStreetMids; decal pictures decoded per row, 7553-7583); ApplyShopInteriors 8372-8701 and BindInteriorPicture 8704-8734; ReDriveShopInteriors 8737-8772; SpawnPeople 2338-2493 (only leonard-idle and kate-idle have walks); PerfHookTick CrimeProbe.cpp:5309-5448 (straight 1.4 m/s walk capped at 45 m, 5446-5447; shadowing lights logged once, 5429-5442).

## Layout: a new offline tool
tools/scale_test_layout.py writes production/specs/scale-test.json (precedent: street_wear.py): road segments of kind main or minor from atlas.json's routes (quay 555, coast 707, night 742, goods 831, harbourlink 1062), clipped to the Hook polygon (62-70), street-to-atlas transform east = 400 + z, north = 350 + x (2009); exclusions the built street and the approach (x 48 to 108.8, 2035-2053); straight 48 m slots, footprint 48 x 26.3 m, no corners, oriented-rectangle overlap test; a walk polyline through the slots ending at cam_hook. Selftest: no exclusion touched, slot centres within 0.5 m of a road line, capacity for N = 2, 4, 10, 15, a continuous walk. Hand estimate (unverified): about 9 slots inside the Hook, enough for N=10; N=15 spills outside and is logged so.

## -ScaleTest=N
N counts street-lengths, so N-1 copies (METHOD-NOTE line 22; decided, the log prints both). Copy set: the 117 in-box street actors, the visible scene pieces (lamp columns, lanterns, props), the stand-ins, interiors except Mickey's room, the wear decals; never people, vehicles, sounds, Mickey's office or the glass catch. Spawned with the original as template at the slot's transform, Movable, collision off unless -ScaleTestCollide, tagged LedgerScaleCopy, outside GStreetActors and GByName. Lights: each copy's lamps, pools, windows, spills and strips in new arrays driven beside ApplyCondition (3813-3831) and ReDriveShopInteriors (8745-8755), spills in GSpillShadowLods (15 m rule). Pictures: copy k shows shop (u + k) mod 7's pictures on each card, decoded per copy through BindInteriorPicture (BC1 first), decal rows a new instance and a fresh decode each, fronts and displays of the shifted unit; ReDriveStreetLook mirrors parameters; -ScaleTestPictures=all|shops|none steps the decodes; the cooked front maps and glass cubes do not grow and are added by arithmetic. Optional -ScaleTestPack=ism (the review's N=4 comparison).

## -ScalePeople=M and the walk
Walker i in street-length i mod N, on a footway at local z +-4.1, x 4 to 44, through a shared SpawnStandIn helper moved out of 2412-2468; optional -ScalePeopleCast=K MetaHumans. -PerfHookRoute=scale follows the walk polyline (turns at most 45 degrees a second, PersonAnim.cpp:527); -PerfHookWalkM replaces the fixed 45 m; about 350 m takes 250 s, 15,000 frames (p1-packaged.ps1 -Frames). The light count logged at the capture's start, the walk's end and the capture's end.

## The log line
LedgerScaleTest: streetLengths, copies, slots, inHook, outsideHook, dropped, pack, collide, rowsPerCopy=117, rowsTown=62, standIns, pieces, interiors, meshes, actors, components, instances, tris, lightsPerCopy, lightsAdded, shadowCasting, pictures, pictureMBPerCopy, people, walking, standing, cast, hideTown, buildS; plus one LedgerScaleTestSlot line per slot.

## Acceptance
Layout selftest; both targets built; one editor run at -ScaleTest=10 -ScalePeople=20 from a new top-down measuring camera cam_scale_top (in measure-cameras.json, about 300 m up) and from cam_hill: nine copies on the road lines, none over the street or the approach, the log lines with nonzero lights, picture MB and 20 people; a short walk run showing the three light lines. Staging: production/specs/scale-test.json added to stage_game_data.py's list.

## Risks
Memory: the baseline is already about 95 MB over 4,870 MB; at N=10 1 to 2 GB more is plausible, and paging would then be measured instead of drawing: ladder 1, 2, 4 first, pictures stepped, nothing else on the card. Under-count: no straddling meshes, shared cooked maps, Movable not Static. Over-count: copies through the town, hidden people still animate. Actor iterators will see copies (the tag lets them skip). No World Partition: the worst case, not the shipped district.

## Hours
Core about 14 h (the method note said 8): layout 2.5, copy pass 3, lights 1.5, pictures 2, people 1.5 (+1 cast), walk 1.5, staging 0.5, build and editor run 1.5. Optional: ism 2, hide-town 0.5, a core export of the street box as its own GLB about 5 (decide after the N=10 screen).

## The layout as built (16 Nov)
tools/scale_test_layout.py, selftest 476 of 476: 10 slots inside the Hook (harbourlink, quay, goods, coast, coldstore, night roads), 98 with --allow-outside; N=15 needs four outside. The walk through all slots is about 1.4 km (dead ends walked out and back), and through the cold-store entry leaves the Hook for 296 m; the measured walk is the three nearest slots, 422 m, none outside (--walk-slots 3). Quay Street inside the Hook holds one slot (the rest is the built street and the approach). scale-test.json written at --n 10 --walk-slots 3.
