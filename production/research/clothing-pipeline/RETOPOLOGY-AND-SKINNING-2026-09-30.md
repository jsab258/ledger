# Retopology and skinning of the donkey jacket (30 September 2026)

The problem: one game-ready donkey jacket for a heavy and a lean MetaHuman, made only with scripted Blender 4.5 and free tools, holding up walking, sitting and arms raised. We have the drape (about 260,000 vertices, with separate yoke, pocket, button and collar shells). About 30 minutes of web reading. Brackets are source numbers. D = documented, I = my inference.

## The route for us

1. The dense drape becomes the "high" mesh, used only for baking. The game gets a new, light mesh with loops at the joints (D 1, 4, 5, 6).
2. Build the light mesh on the flat pattern pieces, not the 3D drape: a script lays a quad grid on each flat panel, rows bunched at the elbow and armhole, with equal vertex counts along edges that are sewn together (D 4). It then lifts the grid into 3D by finding each point's place on the drape through the pattern's UVs (D 4, 5, 7, 8). The drape's UVs must be the flat pattern, with no overlaps (D 7). A four-sided patch per panel is I.
3. Fallback if the flat panels are lost: Instant Meshes by command line per shell, aligned to its open edges (D 9), then joint loops added by script (I). Not QuadriFlow (D 1, 2, 3).
4. One surface, not layers. The yoke is a material slot or texture mask on that surface (I, from D 10, 23). Pockets, seams, stitching, button faces and the yoke's raised edge go into the normal and AO maps (D 10). The collar is modelled doubled (D 5), and the hems are turned in about a centimetre (I). Aim for about 10,000 to 15,000 triangles at LOD0 (I, from D 6, 11, 12).
5. The flat pattern is the UV layout, with seams on the real sewn seams (D 4, 5, 14).
6. Bake normals and AO in Cycles on the CPU by script (D 15, 16).
7. Skin by transferring the body's weights with Epic's "inpainting" method, in Unreal (D 17) or Blender (D 18, 19; licence check). Up to 8 influences (D 17).
8. Second body: carry the finished jacket to the lean body by surface binding, push it out of the body, then transfer weights again from the lean body (D 21, 22, 24, 26; the order is I).
9. The skirt below the hips: Chaos Cloth in 5.8, with Max Distance 0 everywhere else (D 17, 27).

## 1. How professionals make the game mesh

- Blender's manual: automatic remeshers "generally don't result in topology that lends itself to deformation"; characters are retopologised by hand (1).
- The standard garment method: retopologise on the flat pattern, carry the UVs across, then project the new mesh onto the 3D drape through UV space; sewn edges need equal vertex counts (4). (5, 2018) keeps the pattern UVs; (6, 2025) retopologised on the pattern, then added loops at elbows and knees.
- Budgets: a Resident Evil 2 Remake jacket, about 7,300 triangles (11); a 2025 garment set, 25,000 including shoes (6); paid MetaHuman outfits, about 51,000 for a whole outfit, 4 LODs (12).
- Loops: at least three round an elbow or knee, one or two extra at the shoulder (13). No jacket-specific count found.
- Model the silhouette; pockets, creases, stitching and buttons go into normal or colour maps, and floating high-mesh details are a normal baking method (10).
- The yoke: no source addresses it. Two skinned layers millimetres apart bend differently, so the lower shows through: our "torn" edge. Professionals hide or delete covered inner surfaces (23). So (I): one surface, the yoke a colour and material region.

## 2. Automating it in Blender, headless

- QuadriFlow wants a manifold mesh (2); open edges are only "somewhat supported" (3). It drops UVs and other data (1), is advised against for anything that deforms (1), and gives no loop control (3).
- Instant Meshes: BSD-3, last changed 3 November 2019, Windows build. Batch options: -o output, -f face count, -b align to open edges, -c creases, -r 4 -p 4 pure quads (9). No loops at joints.
- Shrinkwrapping a clean base garment onto the drape suits smooth shapes, not deep folds (ArtStation guide, undated, search summary). A CC0 MakeHuman garment could be the base (22).
- Blender's "Sample UV Surface" node finds the point at a given UV coordinate and fails where UVs overlap (7). A paid add-on for Marvelous garments uses it (8, 2024), so the approach works; we can script our own.

## 3. Baking

- The light mesh is active; the high meshes (drape plus pocket, button and collar shells) are selected. Use a cage, or Max Ray Distance without one; tangent space; margin type "Adjacent Faces" (15).
- Common failures (16, June 2026): black bakes (image not Non-Color, rays missing, flipped normals); garbled seams (too little margin); bumps reading as dents in Unreal (Blender's green channel is the opposite of Unreal's, so flip it).
- On garments (I): rays reaching the far side of the thin sheet (keep ray distance to a few millimetres), and the body darkening the AO (hide it, unless contact shadow is wanted).

## 4. Skinning to a MetaHuman

- Epic's method (18, SIGGRAPH Asia 2023) copies weights only where confident (near the body, normals within 30°), then fills the rest smoothly. It was built for loose garments. Reference code: MIT, about 280 lines, uses libigl (MPL-2.0) (18, 20).
- Unreal 5.8 has it built in: the TransferSkinWeights node, method InpaintWeights; defaults 30°, 5% search radius, 8 influences, 10 smoothing passes; "LayeredMeshSupport" handles single-sided cloth (17).
- A Blender add-on exists under GPL-3.0 (last commit 27 March 2026; a Blender 5.2+ fork, 11 September 2026), needing scipy, libigl and robust-laplacian (MIT) (19, 20). If GPL is not on the allowlist, that is Jafar's call.
- Plain fallback: Blender's Data Transfer modifier, "Nearest Face Interpolated", after "Generate Data Layers" (21). It struggles where body parts are close, such as armpits and between the legs (search summary).
- Twist and corrective joints: nothing documented. My view (I): keep the twist weights the transfer gives (they stop sleeves twisting like a sweet wrapper); keep corrective weights only where the jacket hugs the body (shoulders); drop face joints (a search summary agrees on face joints).

## 5. The same jacket on a second body

- Blender's Surface Deform: the target must have no concave faces, doubled vertices or three-face edges; artefacts grow with distance from the target (21). Since the bodies share topology, make the lean body a shape key of the heavy one and bind to that (I).
- MakeHuman ties each garment vertex to a body triangle plus an offset; assets CC0 (22).
- Unreal's outfit resizing warps a garment from source body to target body (24), in the editor only (25). Epic's docs and users report that resizing, or making a wardrobe item, overwrites custom weights with a transfer from the body (24, 26).
- What goes wrong: the loose skirt distorts (21) and cloth passes into the new body (I). Hence push out, then weight again.

## 6. The skirt in Chaos Cloth, 5.8

- New in 5.8 (27, 17 June 2026): the Dataflow cloth editor is production-ready and the default; new nodes import vertex and texture maps; weight painting and the tapered capsule collision shape are updated.
- In the 5.8 node reference (17): VertexColorToAttribute (pick a channel, scale, name the attribute); SimulationMaxDistanceConfig (Max Distance 0 makes a vertex kinematic, and a selection can force it); TransferSkinWeights.
- A low simulation mesh without thickness drives the render mesh (28).
- Unresolved (29, April 2026): simulation did not carry into an assembled parametric MetaHuman outfit.

## Not found

- A professional source on a contrasting yoke specifically.
- Documented loop counts for a jacket.
- Epic guidance on twist and corrective joints in MetaHuman clothing.
- The full text of Epic's 5.8 cloth tutorials and parametric clothing pages, which did not load. What I have is from search summaries and the node reference.
- The paper's PDF, which did not render.

## Sources

1. Blender Manual, "Remeshing" (manual source file). Blender Foundation, current 5.2 manual, undated. Read in full.
2. QuadriFlow README. Huang and Zhou, 2018. Read.
3. Blender issue T70548 (QuadriFlow and non-manifold meshes), 2019, search summary only. Plus devtalk "QuadriFlow improvements", 23 November 2019, read.
4. gamedev.zone, "Character Pipeline #2: Clothing Retopo from Marvelous with Maya". Undated. Read in full.
5. Inu Games, "Marvelous Designer to Unreal 4 Tips", Anna, 15 January 2018. Read in full.
6. Emma Turner, "Retopology (again)", 2 April 2025. Read in full.
7. Blender Manual, "Sample UV Surface Node" (source file). Undated. Read in full.
8. 80.lv, "Get This Procedural Retopology Blender Tool For Garments", A. Rutherford, 14 June 2024. Read.
9. Instant Meshes, W. Jakob et al.: options in main.cpp, LICENSE (BSD-3, 2015), last commit 3 November 2019. github.com/wjakob/instant-meshes. Read.
10. Polycount threads "modelling clothing", "HELP - Baking Normals with Floating Geometry" and "How to approach baking clothes". Undated. Search summaries only.
11. Polycount, "Polycounts in next gen games thread". Undated. Search summary only.
12. Fab listings (Combat Hazmat Suit, Helios Astronaut Suit). Undated. Search summary only.
13. Polycount topology threads and CG Typhoon, "Elbow topology". Undated. Search summaries only.
14. Polycount and unwrap3d on UV seams. Undated. Search summaries only.
15. Blender Manual, "Render Baking" (source file). Undated. Read in full.
16. StraySpark, "Fix Black Normal Map Bakes in Blender", 18 June 2026. Read.
17. Unreal Engine 5.8 docs, Dataflow node reference (index, TransferSkinWeights, SimulationMaxDistanceConfig, VertexColorToAttribute). Undated. Read.
18. Abdrashitov, Raichstat, Monsen and Hill (Epic Games), "Robust Skin Weights Transfer via Weight Inpainting", SIGGRAPH Asia 2023 project page. Read. Code at github.com/rin-23/RobustSkinWeightsTransferCode (MIT, 2024): README, example and utils read.
19. sentfromspacevr/robust-weight-transfer (GPL-3.0), last commit 27 March 2026: README and requirements read. protoco-jp fork, 11 September 2026: metadata read.
20. libigl Python bindings (MPL-2.0), search summary. robust-laplacian 1.1.0 on PyPI (MIT, 25 March 2026), read.
21. Blender Manual, "Data Transfer Modifier" and "Surface Deform Modifier" (source files). Undated. Read in full.
22. MakeHuman Community, MakeClothes documentation and legal page (assets CC0 since September 2020). Search summary only.
23. Reallusion, "Automatically Hiding Inner Meshes". Undated. Search summary only.
24. Unreal Engine 5.8 docs, "Getting Started with Parametric Clothing". Undated. Search summary only; the page did not load.
25. Epic forum, "Chaos Cloth Outfit Asset Resizing Addendum", 19 August 2025 onwards. Read.
26. Epic forum, "Skin Weights In MetaHuman Wardrobe Item Is Not Same From Skeletal Mesh", 2 September 2025 to 15 September 2026. Read.
27. Epic forum, "Tutorial: Chaos Cloth - Updates 5.8", 17 June 2026. First post read; the tutorial itself did not load.
28. Style3D Simulator guide, "General Mesh Garment Imported into UE". Undated. Read.
29. Epic forum, "Parametric Metahuman Clothing with Simulation?", 24 April and 4 May 2026. Read.
