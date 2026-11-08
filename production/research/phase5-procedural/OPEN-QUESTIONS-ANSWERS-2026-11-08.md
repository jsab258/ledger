# Phase 5 open questions: list and answers (8 November 2026)

Research only; no synthesis, no design decision. Nothing run. Read 8 Nov 2026. S = C:/Program Files/Epic Games/UE_5.8/Engine/Plugins/PCG/Source/PCG. Tags: R read, U unverified, X unreached.

## A. The list (from the five notes, in order)

From PCG-COUNT-2026-11-07.md (its "Not reached" and table):
1. Why the PCG component stays in the packaged game although the header says components of an uncooked graph are excluded (cause "unread").
2. Whether that leftover component could start generating with no graph.
3. Whether the placed instances were drawn (no picture).
4. Same transforms on two machines.
5. Nanite: plain against hierarchical instancing.
6. Partition, grammar, a real street's size, memory, frame time.

From PCG-SOURCE-ANSWERS-2026-11-07.md:
7. PCGProceduralISMComponent.cpp:140 editor-only line, not re-read.
8. Which release made partitioning work in non-World-Partition worlds.
9. Whether the same seeds give identical output on another machine (float maths, GPU nodes, landscape or world-query inputs, editor-camera node).
10. Release notes under the engine folder: not searched.

From RESEARCH-2026-10-28.md (Unverified, Not reached):
11. Horizon, Ghost Recon (10 min per 2x2 km tile, 20 degree roads) and Far Cry 5 figures: helper-read, too large to re-open.
12. City Sample's window rooms (fan analyses only).
13. What the engine's render-thread figure means (15.17 ms median).
14. 5.8 GPU scatter timings (release notes give none).
15. GDC Vault (maintenance), Spider-Man 2019 slides (403), video-only talks, Watch Dogs / AC Unity / Cyberpunk validation: not reached.

From MAFIA-KIT-2026-10-28.md:
16. How the Primitives code applies `[ ]` width groups; the cut volume's use.
17. Copying structure or assets from Epic's sample and Primitives content (not on the allowlist): his decision, not a research question.
18. Per-front counts landing on the wrong building; WEAR decal figures (source folder deleted); trim-sheet strip layout; Houdini rules; Palermo/San Celeste/Mafia master graphs: no engine source applies.

From TERRACE-KIT-TABLE-2026-10-29.md:
19. Brick course 75 or 86 mm, G1 scale, G2 sizes, northern bricks, port-town sample, Historic England, full-size originals: period-evidence questions, not engine questions; not attempted here.

## B. Answers

**Q1 (component stays).** The code says it should go. `UPCGComponent::NeedsLoadForTargetPlatform` returns false when the graph is loaded and the graph is not cooked for that platform (S/Private/PCGComponent.cpp:2155-2164); the graph instance repeats the test (S/Private/PCGGraph.cpp:2873-2881); the graph's test is `ShouldCookForPlatform` (PCGGraph.cpp:805-827, reads the per-platform `ShouldCook`). `IsEditorOnly` on the component follows the graph instance (PCGComponent.cpp:2143-2153). R. Why the packaged count still showed one component is not answered: those functions are queried by the cooker, whose code lies outside the PCG plugin and was not read; the spike's cause is U. One possible gap (U, not tested): the cook asks the component only if the cooker calls these functions for components inside a level's actors.

**Q2 (leftover component generating with no graph).** By code, no. `ShouldGenerate` returns false when `!bActivated || !GetGraph() || !GetSubsystem()` (PCGComponent.cpp:366-371); `GetGraph` returns null with no graph instance (232-235); `GenerateInternal` exits when `ShouldGenerate` fails (544-546); on load a component with no graph is set not-generated (1990-1995). The On Load path also needs a graph through the same gate (1769-1771). R, a reading, not a packaged run: U.

**Q7 (editor-only line).** Confirmed: `bIsEditorOnly = true;` at S/Private/Components/PCGProceduralISMComponent.cpp:140, in the constructor of `UPCGProceduralISMComponent` (the file is under Components/, not Compute/). R.

**Q9 / Q4 (cross-machine determinism).** Nothing new beyond the 7 Nov note. Added: partitioned generation can be forced to run local components one after another "for determinism" (S/Internal/PCGTrackingManager.h:207 and 256). The engine's per-node determinism tests are registered for one node only, Difference (S/Private/PCGModule.cpp:331-335, re-read through the grep of 8 Nov); the test levels are `EDeterminismLevel` (S/Public/Tests/Determinism/PCGDeterminismTestsCommon.h:23-31). No comment names a node that breaks determinism across machines. Whether outputs match on two machines: U.

**Q8 (release of non-WP partitioning).** Not found. A web search returned only forum threads and API pages, none stating it. The 5.6 and 5.7 release-note pages were fetched but returned only a table-of-contents heading, so nothing was read: X. Pages tried: https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-6-release-notes and .../unreal-engine-5-7-release-notes (8 Nov 2026). Release: U. A search of the engine folder for Markdown release notes under Plugins/PCG found none.

**Q16 (`[ ]`).** Only the parser's token table was read: `[` and `]` are `SequenceStart`/`SequenceEnd`, beside `,` delimiter, `:` weight delimiter and `<` priority start (S/Private/Grammar/PCGGrammarParser.cpp:24-28). How the Primitives plugin applies width groups: not read here, U.

**Q3, Q5, Q6.** Need an editor, a picture or a build; not attempted (brief forbids runs). Open.

**Q10.** Done for the engine folder: no release-notes file found by search of Plugins/PCG (Markdown only; other folders not searched).

**Q11-Q15, Q18-Q19.** Not attempted: web talks, fan analyses and period-evidence questions are outside the engine source; the briefed sources for them were already marked unreached or helper-read. Q13 and Q14 would need engine render-stat source or a measured run; not read.

## C. Counts

19 numbered questions (some grouped). Answered from source: Q2 (by reading), Q7, Q10 (partly), Q1 in part (code path read; cause still open). Newly confirmed detail: PCGTrackingManager.h:207, 256. Unverified: Q1 cause, Q2 (no run), Q4/Q9, Q8, Q16. Unreached: Q8 release notes (5.6, 5.7 pages returned no text), Q15 sources. Not attempted: Q3, Q5, Q6, Q11-Q14, Q17-Q19.

## Continued 8 Nov evening

Read 8 Nov 2026. E = C:/Program Files/Epic Games/UE_5.8/Engine. Research only; nothing run, no synthesis.

**Q1, the cook path outside the PCG plugin (R).**
- The save harvester asks the object, not the plugin: `GenerateMarksForObject` sets NotForClient when `NeedsLoadForClient()` is false and NotForServer likewise; both marks together mean editor-only (E/Source/Runtime/CoreUObject/Private/UObject/SavePackage/PackageHarvester.cpp:26-46, 80-87). `NeedsLoadForTargetPlatform` is asked only if the object is not already editor-only, or the target allows editor objects (PackageHarvester.cpp:47-64).
- For any component, `UActorComponent::NeedsLoadForClient/Server` return false whenever `IsEditorOnly()` is true (E/Source/Runtime/Engine/Private/Components/ActorComponent.cpp:1228-1242). `UPCGComponent::IsEditorOnly` is true when the graph instance's is (PCGComponent.cpp:2143-2153). `UPCGGraph::IsEditorOnly` is true when `!AnyPlatformShouldCook()` (PCGGraph.cpp:744-803); `AnyPlatformShouldCook` is true if `ShouldCook.Default` or any per-platform value is true (PCGGraph.cpp:2698-2712, tail beyond line 2712 not read).
- Conditions found under which an editor-only object is kept anyway: an object whose `HasNonEditorOnlyReferences()` is true overrides the NotForClient/NotForServer marks, but only in an editor save with no target platform (SaveContext.cpp:290-296, PackageHarvester.cpp:67-87, 129-131, 736-743); the only overrides found are `UBlueprint` (Blueprint.cpp:1945) and `UObjectRedirector` (ObjectRedirector.h:41); `UPCGComponent` is not among the hits of a grep of E/Source/Runtime (the PCG plugin folder was not searched for it).
- Spike note (PCG-COUNT-2026-11-07.md:13, 22, 33; tools/ue/pcg_count_spike.py:93): the script set `should_cook` to `PerPlatformBool(default=False)` on the graph; the packaged count came from `obj list class=` and gave "1 PCGComponent, 2.4 KB, on its volume". The note does not say whether the count was taken per level actor or over all loaded objects, and the project was deleted.
- Candidate found, not tested (U): `APCGVolume`'s constructor creates the component as a default subobject, "PCG Component" (S/Private/PCGVolume.cpp:15). A class-wide object count in a packaged game could therefore include the volume class's own default object (a CDO subobject), which the harvester never excludes ("CDOs must be included if their class are", PackageHarvester.cpp:32-36). Whether the counted object was that one or the placed volume's: U; the PCG note's own wording ("on its volume") says the second.

**Q16, how `[ ]` is applied (R).**
- Parser: `[` makes a child module of type Sequence under the current module, `]` closes it, a mismatch is an error (PCGGrammarParser.cpp:83-106, 59-79, 180-185). A token after a module sets its weight (after `:`) or its repetition (`*`, `+`, or an integer) (lines 124-171). Sequence is a plain container: `<>` (Priority) and `{}` (Stochastic) are the choosing types.
- Size: a Root or Sequence's unit size is the sum of its children's minimum sizes; Priority and Stochastic take the minimum (S/Private/Elements/Grammar/PCGSubdivisionBase.cpp:182-229). A module's minimum size is its unit size times its minimum repetitions (S/Public/Grammar/PCGGrammar.h:22).
- Expansion: Root and Sequence replace themselves with all their children in order, each repeated by its count; `*` and `+` become a repeat marker, later copied while the remaining length fits (S/Public/Elements/Grammar/PCGSubdivisionBase.h:178-236, 262-270, 361-394). Priority takes the first child that fits; Stochastic takes a weighted random pick (lines 271-349) from a stream seeded by the context seed (line 189).
- Leftover length: spread as an extra scale over modules marked scalable, in proportion to their unit size (lines 411-439). Whether any width remains if no module is scalable: the code returns the remaining length to the caller; its use there not read (U). The Primitives plugin's own graphs (E/Plugins/Experimental/PCGPrimitives/Content) are uassets, not read. The cut volume's use: not read.

**Q8, release notes (partly reached).**
- 5.5 page (https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5-5-release-notes) came back as 379,206 characters, read in four 100,000-character stretches through a summarising fetch tool, not as raw text: U. No statement on partitioning in non-World-Partition worlds was reported. Reported in the PCG part: a world-partition builder for PCG components existed from 5.4, and a new PCG Builder Settings asset (first stretch only).
- 5.6 page: returned only "Table of Contents": X. 5.7 URL: returned a page titled "Unreal Engine 5.8 Release Notes" with only a table of contents: X (title mismatch noted).
- A search (8 Nov) found no page stating the release. One forum thread, "Intermittent cook failures when a PCGWorldActor tries to register ALandscapeProxy components in non-world partition mode" (https://forums.unrealengine.com/t/intermittent-cook-failures-when-a-pcgworldactor-tries-to-register-alandscapeproxy-components-in-non-world-partition-mode/2706259), shows PCG used in non-WP worlds in 5.7; its text was not opened. Release that made it work: U.

Unreached this session: 5.6 and 5.7 release-note bodies; the forum thread above (not opened).
