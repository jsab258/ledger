# PCG source answers, Unreal 5.8 (7 November 2026)

Research only; no synthesis. Read 7 November 2026 in C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/PCG/Source/PCG (called S below). Nothing run. Tags: R read, U unverified.

## 1. What a cooked game holds of a PCG result saved in the level

- The generated meshes are ordinary instanced mesh components made on the target actor and registered as instance components (S/Private/Helpers/PCGActorHelpers.cpp:240-245). Only previews and debug output get transient flags (lines 232-238). R.
- The decision to drop PCG itself sits on the graph: `ShouldCook`, a per-platform bool, default true (S/Public/PCGGraph.h:753-762). Header words: if off, the graph and its compiled data "will be stripped from cooked builds", and "any PCG components or graph instances that reference this graph will also be excluded from cooking". R.
- A graph counts as editor-only when the engine's own editor-only flag is set or no platform cooks it (S/Private/PCGGraph.cpp:759, 802; `AnyPlatformShouldCook` at 2698-2716). The old `bIsEditorOnly` is deprecated in 5.8 (PCGGraph.h:868-870) and converted to `ShouldCook = false` on load (PCGGraph.cpp:701-704). R.
- The component follows its graph: `UPCGComponent::IsEditorOnly` is true if the module's editor-only-generation mode is on, or the component itself or its graph instance is editor-only (S/Private/PCGComponent.cpp:2143-2153); `NeedsLoadForTargetPlatform` is false when the graph is not loaded for that platform (2155-2164). R.
- Nothing in the mesh-placing code reads those flags; so by the code the placed mesh components are not marked editor-only. This is a reading of the code, not a packaged run: U until one packaged count is made.
- Settings named: component `GenerationTrigger` (default GenerateOnLoad, PCGComponent.h:326-327), `bActivated` (317), graph `ShouldCook`. On Load only generates when nothing is saved (PCGComponent.cpp:1764-1771: skips when `bGenerated` and no procedural instances in use). R. Components generating through the GPU path use procedural instance components, which the earlier note (PCG-RESULT-HOME, corrections) says are editor-only; that line, PCGProceduralISMComponent.cpp:140, was not re-read here: U.

## 2. Partitioning a non-partitioned component

- Property: `bIsComponentPartitioned` (editor label "Is Partitioned", default false), PCGComponent.h:319-324. Header words: partitions "the component in a grid, dispatching the generation to multiple local components"; grid size comes from the PCG World Actor unless the graph has hierarchical generation. R.
- `IsPartitioned()` is the flag and `CanPartition()`; `CanPartition` is false only when the owner is a partition actor (PCGComponent.cpp:129-137). Nothing in the code tests for World Partition there. R.
- Toggling after generation cleans up the old result, sets the flag, re-registers with the subsystem (SetIsPartitioned, 139-170; the editor toggle handler 2383-2400 regenerates if it was generated and active). R.
- Version history: the code comment at PCGComponent.cpp:2005 says components marked partitioned in non-WP worlds "from BEFORE partitioning was supported in non-WP worlds can leak resources", fixed by clearing the flag on load when `bDisableIsComponentPartitionedOnLoad` is set (PCGComponent.h:657-658). So support for non-WP worlds came in some earlier release than 5.8. Which release: U (no release notes read; none searched for under the engine folder).

## 3. Seeds across machines

What enters the seed (R):
- Component: `Seed = 42` (PCGComponent.h:313-314), handed to nodes as the execution state's seed (S/Private/PCGComponentExecutionState.cpp:18-22). Actor position is not part of it.
- Node: `GetSeed` is the node's `Seed` combined with the component seed by `ComputeSeed`, or the fixed default if the node does not use a seed (S/Private/PCGSettings.cpp:723-725). The combine is integer arithmetic only (S/Private/Helpers/PCGHelpers.cpp:35-48).
- Random streams combine the given seed, the node seed and the component seed the same way (PCGHelpers.cpp:55-73).
- Position: `ComputeSeedFromPosition` casts X, Y, Z to int (PCGHelpers.cpp:50-53). The spline sampler seeds from world or local position, 2D or 3D, or from an external seed plus sample index (S/Private/Elements/PCGSplineSampler.cpp:154-184). So moving an actor shifts position-seeded results; local-position seeding does not shift.
- The Generate Seed node draws from a random stream; "for users that want deterministic seeds across multiple data" it has a reset-per-input option (S/Private/Elements/PCGGenerateSeedElement.cpp:89-93).

What the code says about breaking determinism:
- The surface sampler notes world-scaled cell indices make it "deterministic" (PCGSurfaceSampler.cpp:116). R.
- The compute-graph compiler says the compute graph index order "should be deterministic" (Graph/PCGGraphCompilerGPU.cpp:2018). R.
- The engine ships a Determinism window setting per node (PCGSettings.h:494-495) with native tests registered for only one node, Difference, and a "TODO: Add other native test functions" (S/Private/PCGModule.cpp:331-335). R.
- No source comment found that names a node or setting as breaking determinism across machines. Not confirmed: whether the same seeds give identical output on another machine (float maths, GPU nodes, landscape or world-query inputs, the editor-camera node). U; only a run on two machines would show it.

## Not reached

- Release notes under the engine folder: not searched. No web page read. PCGProceduralISMComponent.cpp not re-read. No packaged run.
