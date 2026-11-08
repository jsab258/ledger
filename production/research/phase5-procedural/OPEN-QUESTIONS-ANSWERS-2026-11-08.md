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
