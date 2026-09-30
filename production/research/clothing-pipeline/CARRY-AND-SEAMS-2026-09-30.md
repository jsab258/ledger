# Carrying the jacket to a lean body, and the torn armhole (30 September 2026)

Asked: why the lean man's donkey jacket shows his chest and six-pack, why the sleeve-to-yoke seam looks torn, and how the PVC yoke should be textured. About 30 minutes of web reading. D = documented (source number); I = my inference.

## The route for us

1. Stop reading the change in body shape off the real skin. Make smoothed "cage" copies of both bodies (same point order), with the pectorals, abdominals and navel smoothed away but the overall girth kept, and carry the jacket from one cage to the other. D [2, 3]; how much to smooth is I.
2. Carry with a wide, even neighbourhood of body points. Drop the "narrower close to the skin" rule: that rule is what copies his muscles into the melton. D [4, 5] (more neighbours means smoother; fewer sample points means less body detail). Blaming the narrow rule is I.
3. Follow Pixar's refit instead of a plain move: bind each jacket point to its nearest cage point plus an offset and rebuild it on the lean cage; then "relax", solving for the shape that keeps each point's neighbourhood as it was on the heavy man, pulled towards the carried position only by a per-point "tightness" (high at collar, shoulders and cuffs; low over chest, belly and back). Seam points share neighbourhoods so seams move together. Repeat relax and rebind (Pixar: up to 25 rounds). D [1]; the numpy solver is I. Blender's Laplacian Deform, anchored at collar, shoulders and cuffs, is a cruder stand-in. D [10], I.
4. Push the jacket out of the smoothed lean cage (or a hull around it) plus an offset, never out of the real skin: Shrinkwrap in "Outside" mode against that proxy. D [3, 10]; I for the combination.
5. Then hang it straight as now. Then add a Smooth Corrective pass bound to the heavy man's drape, limited to chest, belly and back, to lift out any body print that remains. D [10] for what it does; I for this use.
6. Optional: a few frames of cloth simulation with high bending stiffness as a final settle, which is what Pixar does last. D [1].
7. Every step that moves points one at a time (carry, push-out, hanging, relaxing, weight copy) must move each seam's shared points as one group. Weld by distance at the end as a safety net. D [14, 1, 16].
8. Before lifting, give both sides of every seam the same number of points, spaced by matching lengths. The sleeve head is 3 to 4 cm longer than the armhole, the extra sitting in the upper, outer curve and none at the underarm; spread it there. D [17, 15]; I for our grid.
9. At the armhole, lift the whole jacket in one pass and project smoothly (Blender's "Target Normal Project"), not to the nearest point, which can jump between the sleeve and body layers in the armpit fold. D [10]; the armpit jump is search summary only [22].
10. Where sleeve and yoke must move by different amounts, fade the difference over 3 to 5 grid rows either side of the seam, never a hard step. I, supported by D [11].
11. Give each seam point one set of skin weights (one side's, or the average) and smooth the weights over a band either side, so the seam cannot open when the arms go up. D [18] (twin points move together only if their weights match); the band is I.
12. Yoke: take the drape's broad bulges out of its normal map; keep only the edge stitching, the small step where the yoke sits on the melton, a few shallow creases at the shoulder fold and very faint grain. Let the gloss and its roughness variation do the rest. D [19, 20]; mostly I.

## A. Carrying a garment to another body shape

Pixar's Soul tool [1] handles our exact case of two bodies sharing one mesh. A plain carry costs "mesh distortion"; relaxing restores the garment's own layout, tightness values choose where it hugs the body, panel edges are held together, and a short cloth simulation finishes. Research papers [12, 13] agree that a purely geometric carry loses the design (abstracts only). Wrap's Lattice node [4] does what we do now; its one control is how many body points are used, and more points give a smoother result. MetaHuman resizing [5] samples a set number of body points, and more points follow the body more closely (search summary only). MakeHuman [7] ties each clothing point to three body points plus an offset. Roblox [2] fits to a body cage "without all the fine details". Marvelous Designer [8] morphs the avatar over several frames while the garment simulates (search summary only). Blender's Surface Deform and Mesh Deform [10] are only as smooth as their target: bind them to the cage. All of steps 1 to 6 runs in Blender 4.5 with its bundled tools; scipy (BSD licence) would speed up the solver if the allowlist takes it (I).

## B. Stiff cloth bridging hollows

Two free sources [3, 2] work the same way: fit against a proxy that fills hollows. The Elastic Clothing Fit add-on uses a "convex-hull proxy of the body [that] fills concave regions", then elastic passes to restore the garment's silhouette and light Laplacian smoothing. Roblox's outer cage must "follow the clothing mesh closely, but always be outside" it. A hull per horizontal slice matches our hanging step (I).

## C. Torn seams

A report dated 29 September 2026 [14] matches our fault: a smoothing pass run after welding moved the two halves of each seam differently and reopened 78 of 94 seams. Its proposed fix is to treat each welded group as one point in every pass. A commercial Blender tool [15] evens out point spacing across seams, forces seam edges together and projects the whole mesh at once. Marvelous Designer merges seam points on export [16]. Shards likely come from points bunching where the two sides of a seam differ in length (ease [17]) and from nearest-point jumps in folds (I).

## D. The PVC yoke

Guidance for glossy leather [19]: keep normal strength low; "a smooth leather base with a noisy normal map feels wrong"; carry wear in roughness. A puffed, quilted look is what cloth programs make on purpose with inflation "Pressure" [20]. Our bake likely picked up the drape's bulges between seams, and gloss shows every such curve (I). Real donkey-jacket panels are flat PVC or leather across the shoulders and shoulder blades [21].

## Not found

Epic's own text on how outfit resizing interpolates. Wrap's full cloth-transfer settings. Any studio write-up of a PVC-yoke workwear jacket in a game. The Brouet paper in full. The Marvelous Designer and Polycount pages refused access.

## Sources

1. "Garment Refitting for Digital Characters", de Goes, Fong, O'Malley (Pixar), 17 Aug 2020, https://research.pixar.com/docs/2020.SiggraphTalks.GFO.pdf (read in full).
2. "Layered clothing example", Roblox Creator Hub, undated, https://github.com/Roblox/creator-docs/blob/main/content/en-us/resources/beyond-the-dark/layered-clothing.md (read).
3. "Elastic Clothing Fit" README, VRC-Staples, GPL-3.0, undated, https://github.com/VRC-Staples/Elastic-Clothing-Fit (read).
4. "Lattice" node, Faceform/R3DS Wrap docs, undated, https://docs.faceform.com/Wrap/Nodes/Lattice/Lattice.html (read in full).
5. "Building an Outfit Asset in Unreal Engine", Epic, UE 5.8 docs, undated, https://dev.epicgames.com/documentation/en-us/unreal-engine/building-an-outfit-asset-in-unreal-engine (search summary only).
6. "Tailoring Your Own Wardrobe Items", Epic MetaHuman docs, undated, https://dev.epicgames.com/documentation/metahuman/tailoring-your-own-wardrobe-items (read; nothing on the method).
7. "Technical notes on MakeHuman" and "Controlling the result with vertex groups", MakeHuman Community, undated, https://static.makehumancommunity.org/oldsite/uncategorized/technical_notes_on_makehuman.html (read).
8. "Auto Fitting" and "Morph Target with AVT Files", Marvelous Designer support, undated, https://support.marvelousdesigner.com/hc/en-us/articles/47358335130649-Auto-Fitting (search summary only).
9. "CC Garment Creation Guide", Reallusion wiki, undated, http://wiki.reallusion.com/Content_Dev:CC_Garment_Creation_Guide (read; advice only to leave a gap).
10. Blender Manual: Surface Deform, Mesh Deform, Laplacian Deform, Smooth Corrective, Shrinkwrap, current (5.2 LTS) source, undated, https://projects.blender.org/blender/blender-manual (read in full).
11. "Proximity Wrap deformer", Autodesk Maya 2024 Help, 2023, https://help.autodesk.com/cloudhelp/2024/ENU/Maya-CharacterAnimation/files/GUID-0D7E6B72-6021-4C66-9262-089D10246C3F.htm (partly read; "smooth influences" from search summary).
12. "Design Preserving Garment Transfer", Brouet, Sheffer, Boissieux, Cani, July 2012, https://dl.acm.org/doi/10.1145/2185520.2185532 (abstract and summary only).
13. "Dress Anyone", Chen et al., arXiv, May 2024, https://arxiv.org/html/2405.19148v1 (related work read).
14. Issue #31, DayOnly/CBBEtoUBE-exe, 29 Sep 2026, https://github.com/DayOnly/CBBEtoUBE-exe/issues/31 (read in full).
15. "UVRetopo", GRS Studio, v1.92, undated, https://www.grsstudio.ru/uvretopo.html (read).
16. "Merge Vertex by Proximity at Export", Marvelous Designer support, undated (search summary only).
17. "How to Draft a Tailored Sleeve Pattern", The London Pattern Cutter, undated, https://thelondonpatterncutter.co.uk/drafting-tailored-sleeve/ (read).
18. "BakeMesh() shows split vertices at UV seams", Unity Discussions, 20 Jul 2023, https://discussions.unity.com/t/skinnedmeshrenderer-bakemesh-shows-split-vertices-at-uv-seams-different-from-the-mesh-asset/923984 (read).
19. "Leather Texture Roughness and Normal Map Workflow", AITextured, undated, https://aitextured.com/articles/guides/leather-texture-roughness-and-normal-map-workflow/ (read).
20. "How to Create a Puffer Jacket with the Pressure Function", CLO3D community, undated (search summary only).
21. "Donkey jacket", Wikipedia, last edited 13 Sep 2026, https://en.wikipedia.org/wiki/Donkey_jacket (read).
22. Search results on Shrinkwrap modes for retopology in folds (Blender Artists and CG Cookie threads), undated (search summary only).
