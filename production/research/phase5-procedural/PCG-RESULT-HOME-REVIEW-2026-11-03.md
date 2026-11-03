# Review: where PCG's result lives (3 November 2026)

Fresh reviewer. Read in full: the note, W1-W4, W6-W9, W5 to 100,000 characters, every cited E line and five further engine files. Nothing run.

**Verdict: PASS WITH FIXES.** The recommendation follows; four omissions could break the packaged town.

## Claims checked (35)

These match their sources, as worded, for 5.8:
- Triggers, On Load skipping saved results, procedural instances never kept, editing modes (E1-E3).
- W4: no staff badge, posted Nov to Dec 2025.
- Should Cook per platform, stripping (E4); Clear PCG Link (E5); the builder (E6, W5).
- 5/15 ms in source, 16.667/50 on the page (E7, W2); pops, "expensive" pool doubling (W3); 100 pooled, 16 at once (E8); the HISM-to-ISM swap (E9).
- HLOD and Data Layers: joined when saved (W7), "do not support" at runtime (E10; PCGPartitionActor.cpp:346).
- City Sample: few minutes, all loaded, 128 m, unpartitioned (W8).
- All grid sizes, radii, sources and rules (E11-E14, W2). The 256 m World Partition cell (E15) is 5.8's default RuntimeHashSet (BaseEngine.ini); the old hash uses 128 m.
- Grammar nodes, labels, syntax and modules (W5, W9, E16-E19).
- **Shared factor:** ExtraScale is leftover ÷ total scalable length for every scalable module, never negative, uncapped (PCGSubdivisionBase.h:412-433), applied as point scale (PCGSubdivideSegment.cpp:119). Repeats grow in turn and priority is greedy (E20).
- Seeds, determinism, overrides, packers, No Merging, Python Beta (E21-E25, E27).

## Errors

1. **Meshes from an uncooked graph** (marked unverified): settled from the source, not run.
   - CPU-spawned ISMs are ordinary components on the target actor, with no editor-only flag (PCGActorHelpers.cpp:232-245), and nothing strips them at cook.
   - Only the PCG component (PCGComponent.cpp:2143-2163) and GPU procedural ISMs (`bIsEditorOnly = true`, PCGProceduralISMComponent.cpp:140) are dropped.
   - So CPU output ships and GPU output does not. Confirm with one packaged count.
2. **W6.**
   - The quote reads "If your project only uses Nanite then ISM is always the choice"; the note drops the condition.
   - It is 64 bytes for a basic instance against 672 for a primitive, both on the GPU.
   - Instances share the component's materials, which can be several slots.
3. **W3.** The overlay and the drawn cells work in Editor and Development builds; the drawn cells can be enabled for Shipping (UE_ENABLE_DEBUG_DRAWING). Refresh: no build stated.
4. The export runs "where the Editor can be used" (E26). Seed 42 lives in PCGComponent.h:314. Both minor.

## Missing

1. **GPU scatter conflicts with Should Cook off.** P5 keeps GPU litter and leaves. With the graph uncooked they vanish from the packaged game. Keep the town's graphs CPU-only; any GPU scatter needs its own cooked graph and frame budget.
2. **No collision by default.** PCG's ISMs are Static (good for the shadow cache) and NoCollision (PCGISMDescriptor.cpp:15-17). Set a profile for walls, and have the Python count check it.
3. **Trigger and builder.** Use On Demand: W4 reports unexpected regeneration On Load. The builder skips Normal-mode components unless given -GenerateComponentEditingModeNormal (E6). Or use Clear PCG Link.
4. **Departure from P5,** which asked for a partitioned level streamed by cell: it needs a DECISIONS line.
   - Without World Partition there are no HLODs either, so HLODs do not separate the two options here.
   - WorldPartitionConvertCommandlet is the later path.
5. **For this PC.**
   - 5 ms is 30% of a 60 fps frame; that, more than pops, rules out runtime generation.
   - Gate recommendation 3 on a measured worst view of 10 streets at 3440x1440 (about 3 GB is free after P5's 6.8 GB).
6. **Decals:** Add Component can put a decal component per point onto one actor (I).
