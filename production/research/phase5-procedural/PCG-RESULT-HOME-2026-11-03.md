# Where PCG's result lives, and how it is checked: Unreal 5.8 (3 November 2026)

Research only, for phase 5. Builds on P5 (RESEARCH-2026-10-28.md), MK (MAFIA-KIT-2026-10-28.md), the terrace kit table and Study 4. Tags: **R** read, **I** inferred, **U** unverified. All read 3 November 2026; nothing run, downloaded or cooked.

## Questions

1. Generated in the editor and saved, or generated at runtime: what Epic says on load time, memory, determinism, cooking, later editing, Nanite and HLODs.
2. PCG with World Partition, for 3 to 10 streets.
3. Can 5.8's grammar give base, repeated middle and top, fixed openings and scaled infill? Nodes, version, limits.
4. Seeds, and variety of materials, decals and props.
5. Inspecting and testing output; counting it by script.

## 1. Saved, or generated at runtime

**What the engine does (R).**
- Triggers: Generate On Load (default), On Demand, At Runtime [E1]. On Load generates at play start **only if no saved result exists**; GPU-spawned instances "are never persisted" and always regenerate [E2].
- Editing Mode decides saving: Normal saves with the level, Preview saves nothing, Load as Preview saves then acts transient [E3][W1].
- Epic's forum answer (Epic-Pro-Support thread; staff badge not visible, U): generated components should not regenerate; mark graphs editor-only as a safety [W4]. In 5.8 that is the graph's per-platform **Should Cook**; an uncooked graph and its PCG components are stripped from the cook [E4]. That the spawned meshes still ship is I (separate components; not cooked here).
- **Clear PCG Link** moves the result to a plain actor, unlinked [E5]: a full bake.
- A **builder commandlet** (5.4; settings asset 5.5 [W5]) regenerates and saves by script; in 5.8 it accepts levels without World Partition, needs a GPU, and by default regenerates only Load-as-Preview components [E6].

**Point by point.**
- **Load time, memory:** no figures from Epic (U). Runtime work has a per-frame budget: 5 ms in play, 15 in the editor in the installed source (Epic's page: 16.667 and 50) [E7][W2]. Epic warns of "visual pops" when cells finish late, and of costly pool growth in play [W3]. Runtime partition actors are transient, pooled (100), 16 generating at once [E8].
- **Determinism:** a saved result is fixed data; runtime regenerates every load and rests on the graph (section 4).
- **Cooking:** saved instances cook as level content (I); runtime needs the graph and every input cooked, and for LEDGER every spec file staged.
- **Editing afterwards:** saved results regenerate, but hand edits orphan (P5); runtime has only inputs to edit.
- **Nanite:** the spawner swaps hierarchical for plain instancing on Nanite meshes [E9]; Epic: with Nanite plain instancing "is always the choice"; 64 bytes a card instance against 672 a primitive; one material per instance component, variety through custom data [W6].
- **HLODs:** saved output joins its source's Data Layer and HLOD layer [W7]; runtime components "do not support" either [E10].
- **Epic's city:** City Sample PCG regenerates in the editor, all actors loaded, in "a few minutes"; grid 128 m [W8]. No page read advises baking or runtime outright (U).

## 2. With World Partition

- "Is Partitioned" splits generation into cells, each a local component on a partition actor; cell from the PCG World Actor, default 256 m (minimum 4 m), unless hierarchical generation sets it per node [E1][E11][W2].
- Hierarchical: 4 to 2,048 m plus Unbounded; data flows only to smaller grids; mixed inputs take the smallest; duplicated points need Cull Points Outside Actor Bounds [E12][W2].
- Runtime: player controllers are sources by default; radius per grid and quality level, default twice the cell, cleanup 1.1 times; distance-and-direction scheduling with frustum culling; best with hierarchical generation [E13][W2].
- Partitioning now works without World Partition (since when: U) [E14]. Regenerating needs a graph's actors loaded [W8]; the builder can load by cell [E6].
- World Partition's default runtime cell is 256 m [E15]; Mafia's Palermo 128 m (Study 4).
- **For 3 to 10 streets (I):** ten streets of 50 to 150 m fit in about 500 m square: 4 to 16 cells at 128 m. Partitioning buys little; one component per street or block, as City Sample's non-partitioned default [W8], is simpler.

## 3. The grammar

- **Nodes:** Spline To Segment, Subdivide Segment, Subdivide Spline, Duplicate Cross-Sections, Select Grammar, Print Grammar; first in 5.5's notes (no status label read) [W5], core PCG 1.0 in 5.8 [E16]. Primitive Cross-Section is Experimental, in the Geometry Script interop (Beta) [W9][E17]; PCG Primitives' slot definitions are Experimental [E17].
- **Syntax:** `[A,B]`, `[A,B]3`, `*` as many as fit, `+` at least once, `{A:2,B:1}` weighted, `<A,B,C>` first that fits [E18].
- **It fits:** Duplicate Cross-Sections stacks `[Ground],[Upper]*,[Top]`; Subdivide Segment fills each floor with modules of symbol, size and "scalable" [E19]. Openings fixed, infill scalable.
- **Limits in the code [E20]:**
  1. Leftover length spreads over **all** scalable modules by one factor, only lengthening, uncapped: MK's "within 10% either way" must be a check.
  2. The mesh is scaled, so brick stretches unless the wall material is world-aligned (I).
  3. Repeats grow in turn, so a door between two `*` runs sits mid-front [W9]; choices are greedy, with no backtracking or symmetry.
  4. Floors subdivide separately: windows align only if floors share widths and seed (I).
  5. Partial fills fail unless Accept Incomplete Subdivision; handing by Flip Axis; on splines "tight corners might be underestimated" [W9].
  6. No wall is made between modules; infill is modules (MK).

## 4. Seeds and variation

- The component seed (default 42) combines with each node's seed [E21]. Samplers seed points from whole-centimetre position [E22], so moving a plot reshuffles it; subdivision takes a Seed Attribute [E19], where P5's per-plot seed belongs.
- The Determinism window's tests run each node twice, on copied inputs and on shuffled input order [E23][W1].
- Mesh selectors take material overrides from attributes; each mesh-and-material pair is its own instance component [E24][W6]. Per-instance custom data packs from attributes [E24], as Mafia's paint colour (MK).
- No decal node: Spawn Actor can place a decal actor per point with "No Merging" (I, [E25]). Props: mesh spawner with Self Pruning (P5).

## 5. Checking

- **Editor:** debug rendering, Inspect into the Attribute List, Debug Object tree, Determinism, Profiling (CPU per node), Log and Data Overrides; export from the list view [W1][W3][W5].
- **Runtime:** overlay, drawn cells, pcg.RuntimeGeneration.Refresh; Development builds only [W3].
- **Automated:** no ready layout validator found (U). Parts: Export Selected Attributes to JSON or binary, editor only [E26]; Get Generated Graph Output by script [E5]; the Python interop (Beta, editor only) [E27]; the builder for nightly runs [E6].
- **Counting (I, not run):** an editor Python script can read each instance component's mesh, count and transforms, independent of the export.

## For LEDGER

1. **Saved in the editor, static.** Generate by script into a new saved level, Should Cook off so no generator ships; static Nanite instances, unlike today's movable runtime-spawned street, which never uses the shadow cache (P5).
2. **No runtime generation:** pops, a frame budget, no HLODs, surprise regeneration; nothing at this size needs it (P5 step 5 agrees).
3. **No World Partition at first:** ten streets are a few cells, and PCG partitions without it. Streaming becomes a scope item once memory or load time is measured to need it (the game peaks 5.9 to 6.8 GB of the 10 GB card, P5).
4. **Two counts that must agree:** the JSON export (the placement spec) and a Python count in the saved level.
5. **Core grammar suffices;** stretch cap, window columns and whole-brick infill are our checks; walls world-aligned.
6. **Blender stays the module maker,** exporting one mesh per module, not per material for a whole street.

## Not reached

- GDC 2026 "Developing Large Procedural Systems with Low Friction and Fast Generation" (Epic): refused (403).
- Unreal Fest Bali 2025 "Leveraging PCG for Building and City Creation": video only [W10].
- Release notes 5.5 and 5.8 past 100,000 characters; the grammar page's prerequisites link (404); City Sample PCG's files.

## Unverified

That meshes ship from an uncooked graph; when non-partitioned partitioning arrived; load time, memory and pop-in at our size; the replier's staff status; the grammar's 5.5 label; every I.

## Sources (read 3 November 2026)

E = C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/PCG/Source/PCG.
- E1 Public/PCGComponent.h:77-82, 314-347. E2 Private/PCGComponent.cpp:1743-1772. E3 Public/PCGCommon.h:588-593. E4 Public/PCGGraph.h:753-762, 868-870; PCGComponent.cpp:2143-2163. E5 PCGComponent.h:266-272, 799-800. E6 ../PCGEditor/Private/WorldPartitionBuilder/PCGWorldPartitionBuilder.h.
- E7 Private/Graph/PCGGraphExecutor.cpp:82-84, 123-125. E8 Private/RuntimeGen/PCGRuntimeGenScheduler.cpp:67-90, 2353. E9 Private/Helpers/PCGActorHelpers.cpp:132-156. E10 Private/Grid/PCGPartitionActor.cpp:346; PCGComponent.cpp:204-205. E11 Public/PCGWorldActor.h:58-62. E12 PCGGraph.h:718-728; PCGCommon.h:520-534. E13 PCGCommon.h:595-660; PCGWorldActor.h:73-80.
- E14 PCGComponent.cpp:2005-2010. E15 Engine/Source/Runtime/Engine/Public/WorldPartition/RuntimeHashSet/RuntimePartitionLHGrid.h:57. E16 Plugins/PCG/PCG.uplugin. E17 Plugins/Experimental/PCGPrimitives/PCGPrimitives.uplugin; Plugins/PCGInterops/PCGGeometryScriptInterop. E18 Private/Grammar/PCGGrammarParser.cpp:24-33.
- E19 Public/Elements/Grammar/PCGSubdivisionBase.h:18-32, 112; PCGSubdivideSegment.h:43, 51. E20 PCGSubdivisionBase.h:189-440; Private/Elements/Grammar/PCGSubdivideSegment.cpp:119. E21 Private/PCGSettings.cpp:723-726. E22 Private/Helpers/PCGHelpers.cpp:50-53. E23 Private/Tests/Determinism/PCGDeterminismTestsCommon.cpp:288-380.
- E24 Public/MeshSelectors/PCGMeshSelectorByAttribute.h:34-38; Public/InstanceDataPackers. E25 Public/Elements/PCGSpawnActor.h:17-21. E26 Public/Elements/IO/PCGExportSelectedAttributes.h. E27 Plugins/PCGInterops/PCGPythonInterop.
- W1 dev.epicgames.com/documentation/en-us/unreal-engine/procedural-content-generation-overview-for-unreal-engine
- W2 …/using-pcg-generation-modes-in-unreal-engine
- W3 …/pcg-runtime-generation-debugging-in-unreal-engine
- W4 https://forums.unrealengine.com/t/pcg-generation-at-runtime-on-already-generated-volumes/2688878
- W5 …/unreal-engine-5-5-release-notes (first 100,000 characters)
- W6 …/instanced-static-mesh-component-in-unreal-engine
- W7 …/using-pcg-with-world-partition-in-unreal-engine
- W8 …/city-sample-pcg-for-unreal-engine
- W9 …/using-shape-grammar-with-pcg-in-unreal-engine
- W10 https://forums.unrealengine.com/t/talks-and-demos-leveraging-pcg-for-building-and-city-creation/2705278
- Epic pages are the 5.8 documentation set. LEDGER: P5, MK, TERRACE-KIT-TABLE-2026-10-29.md, studies/04-street-world.md.

## Corrections and additions after its fresh review (PCG-RESULT-HOME-REVIEW-2026-11-03.md, PASS WITH FIXES)

- **Meshes from an uncooked graph, settled from the source (not yet run):** CPU-spawned instanced meshes are ordinary components on the target actor and ship (PCGActorHelpers.cpp:232-245); only the PCG component (PCGComponent.cpp:2143-2163) and GPU procedural instances (bIsEditorOnly, PCGProceduralISMComponent.cpp:140) are dropped. So the town's graphs stay CPU-only; any GPU scatter (litter, leaves) needs its own cooked graph and frame budget. Confirm with one packaged count.
- **Epic's instancing line (W6)** reads "If your project only uses Nanite then ISM is always the choice": the condition matters. Its figures are 64 bytes a basic instance against 672 a primitive, both on the GPU; instances share their component's materials, which may be several slots.
- **Runtime debug tools (W3)** work in Editor and Development builds, and the drawn cells can be enabled for Shipping (UE_ENABLE_DEBUG_DRAWING).
- **Collision:** PCG's instanced meshes are Static and NoCollision by default (PCGISMDescriptor.cpp:15-17): walls need a collision profile, and the Python count checks it.
- **Trigger and builder:** On Demand, not On Load (a report of unexpected regeneration On Load, W4); the builder skips Normal-mode components unless given -GenerateComponentEditingModeNormal (E6); or Clear PCG Link.
- **For this PC:** runtime generation's 5 ms budget is 30% of a 60 fps frame, which more than the pops rules it out; the baked town's worst view of 10 streets at 3440x1440 must be measured before it is adopted (about 3 GB free beside the game's 6.8 GB).
- **A departure from P5:** P5 asked for a partitioned level streamed by cell; this recommends none at first (without World Partition there are no HLODs, so HLODs do not separate the options; WorldPartitionConvertCommandlet is the later path). Nothing is decided here: phase 5's design, written during phase 2, decides it with its own DECISIONS line.
- **Decals:** an Add Component step can put a decal component per point onto one actor (inference).
- **7 November, the packaged count (PCG-COUNT-2026-11-07.md):** meshes ship and the graph goes, measured; but one inert PCG component stayed, unlike the header's words.
