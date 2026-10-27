# Lumen coverage of the office's fittings (27 October 2026)

Why enclosed spots in Mickey's office crush to near-black at High, and whether the merged fittings mesh is the cause. Epic's UE 5.8 pages read in full, engine source and config read locally, all on 27 October 2026.

## Questions

1. How the surface cache covers a mesh; the card setting; Epic on merged meshes.
2. How to see coverage.
3. Distance field resolution and thin boards; modular against merged.
4. Settings Python can set, by exact name.
5. Why High against Epic changed nothing; cheaper fixes.

## Answers

**1.** Lumen captures each mesh's material from several directions; the captures are "Cards", made offline per mesh. Default 12, raised with **Max Lumen Mesh Cards** in Build Settings, "useful for more complex interiors or single meshes with irregular shapes" [T]. Uncovered areas "will not bounce light"; more cards may not solve all issues, the other fix being to break the mesh into less complex pieces [T]. And: "Importing an entire room, which includes furniture, in a single mesh is not expected to work with Lumen" [T]. Maximum: no Epic page says; the editor field runs 0 to 32 and the builder holds a constant of 32 [S1, S2]. The builder clusters cards from 10 cm cells, needs 15 cells per card, and coarsens cells for meshes over 6.4 m or over 10,000 cells [S2]. Inference: the office's whole furniture shares 12 cards, about two per facing direction, so small undersides lose out.

**2.** View Modes > Lumen > **Surface Cache**: uncovered areas pink, and black in reflections [T]. Console: `r.Lumen.Visualize 5` (Surface Cache Coverage; 1 Overview, 3 Lumen Scene), working without the editor's show flag [S3]; `r.Lumen.Visualize.CardPlacement 1` draws the cards [T]. Show > Visualize > Mesh DistanceFields / Global DistanceField [T]; as show flags `VisualizeMeshDistanceFields`, `VisualizeGlobalDistanceField`, absent from Shipping builds [S4].

**3.** Resolution follows imported size times **Distance Field Resolution Scale** (Build Settings) and the project's Distance Field Voxel Density [T, MP]. Engine defaults: a 5 cm voxel (0.2 per cm) and about 126 voxels a side at scale 1 or below [S5, S6]; Epic's page still says 128 cubed [M]. "Walls should be no thinner than 10 centimeters (cm) to avoid light leaking"; distance fields "cannot represent extremely thin features" [T]. Software tracing "requires that levels be composed of modular geometry"; large single meshes get a poor representation and self-occlusion [T]; quality is best with meshes of similar size [M]. This room is 5.3 by 4.15 m [C2], so the merged fittings keep 5 cm voxels, as a separate shelf would. The 3 cm board is thinner than one voxel either way; scale 2 gives 2.5 cm.

**4.** `unreal.MeshBuildSettings`: `max_lumen_mesh_cards` (default 12; 0 switches cards off), `distance_field_resolution_scale` (default 1), `generate_distance_field_as_if_two_sided` [A1]. After import: `StaticMeshEditorSubsystem.get_lod_build_settings(mesh, 0)` / `set_lod_build_settings(mesh, 0, settings)` [A2]. At import, `InterchangeGenericMeshPipeline` has the same three names [A3]. The project's import_street.py already sets the scale through the glTF pipeline override (the editor subsystem is absent in its commandlet); the card count can go the same way.

**5.** The project's config explains it: ue-probe/Config/DefaultScalability.ini (3 October) gives the project's GI level 2 Epic's values line for line, such as `r.Lumen.TraceMeshSDFs.Allow=1` and probe downsample 16 [C1]. High and Epic are the same GI here, so no change was right. The engine's own High differs (mesh tracing off, downsample 32) [B]. Epic's art knobs: post-process **Diffuse Color Boost** (below 2) and **Skylight Leaking**, "to keep indoor areas from going fully black", neither physically based [G]. Lumen Scene Detail and Max Trace Distance treat leaks, not darkness [T].

## What this means for the office

- The card half of the hypothesis is supported by Epic's words, not yet shown in this room.
- "Merged means a coarse distance field" is not supported: the room fits the cap. The 3 cm board breaks Epic's 10 cm guidance whatever the mesh.
- The quality-level result is expected; drop it as evidence.
- Screen traces off brightened it (37 to 41), so the darkness lies in Lumen's world trace: consistent, not proof.
- **Cheapest test:** two editor photographs of the shelf view, `-ExecCmds "r.Lumen.Visualize 5"` and `r.Lumen.Visualize.CardPlacement 1`. Pink under shelf, bench and walkway confirms it. Then re-import the fittings with `max_lumen_mesh_cards` 32 and measure the 37 again; if still pink, split shelf, bench and counter into their own meshes. For the board, the Mesh DistanceFields view; if missing or swollen, scale 2 on the fittings.

## Unverified / not reached

- Whether a value above 32 set from Python is honoured.
- Whether the fittings pass 10,000 cells (cards coarsen to about 16 cm).
- Whether `r.Lumen.Visualize` works in the build type the project packages.
- The Technical Details page calls both per-mesh tracing and Global Tracing the default; unresolved.
- Whether the fittings' field is weakened as an "open" mesh [A1].
- Forum and talk material not read (time). No page refused.

## Sources (all read 27 October 2026)

- [T] https://dev.epicgames.com/documentation/unreal-engine/lumen-technical-details-in-unreal-engine
- [G] https://dev.epicgames.com/documentation/unreal-engine/lumen-global-illumination-and-reflections-in-unreal-engine
- [P] https://dev.epicgames.com/documentation/unreal-engine/lumen-performance-guide-for-unreal-engine (levels "attempt to keep indirect lighting looking similar")
- [M] https://dev.epicgames.com/documentation/unreal-engine/mesh-distance-fields-in-unreal-engine
- [MP] https://dev.epicgames.com/documentation/unreal-engine/mesh-distance-fields-properties-in-unreal-engine
- [A1] https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/MeshBuildSettings
- [A2] https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/StaticMeshEditorSubsystem
- [A3] https://dev.epicgames.com/documentation/en-us/unreal-engine/python-api/class/InterchangeGenericMeshPipeline
- [S1] UE 5.8 Editor/StaticMeshEditor/Private/StaticMeshEditorTools.cpp 916-919
- [S2] Developer/MeshUtilities/Private/MeshCardRepresentationUtilities.cpp 28, 599-687, 713-746
- [S3] Runtime/Renderer/Private/Lumen/LumenVisualize.cpp 29-45, 293-296
- [S4] Runtime/Engine/Public/ShowFlagsValues.inl 353, 357
- [S5] Runtime/Engine/Private/DistanceFieldAtlas.cpp 69-80
- [S6] Developer/MeshUtilities/Private/MeshDistanceFieldUtilities.cpp 312
- [B] Engine/Config/BaseScalability.ini
- [C1] ue-probe/Config/DefaultScalability.ini
- [C2] production/specs/shop-interiors.json
