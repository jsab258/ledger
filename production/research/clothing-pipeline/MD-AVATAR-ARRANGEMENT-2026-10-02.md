# Arrangement points on our MetaHuman bodies in Marvelous Designer (2 October 2026)

The problem as given: in Marvelous Designer 2026.1 Personal, our MetaHuman bodies imported from FBX by script, with auto arrangement points switched on, always say "Arrangement Points were not fitted to the avatar. The avatar must be in a T-pose or A-pose", and the list of points comes back empty. We tried arms at 52.6, 45 and 35 degrees, with and without the skeleton. Every body was the body only, without the head.

D = documented, with its source number. I = my inference.

## The route for us

1. Get each body's MetaHuman DNA out of Unreal. In 5.8 a script can do it: `MetaHumanCharacterExportBlueprintLibrary.export_dna` writes a head .dna and a body .dna to a folder (D21). By hand, there is Export DNA on the MetaHuman DNA asset (D22), or MetaHuman Creator's DCC Export, a zip that holds both .dna files (D23). This is the builder's side.
2. In Marvelous, once per body, by hand: File ▶ Import ▶ DNA. Load the body and head files, set the unit to cm, and tick Auto Add Arrangement Points and Auto Create Fitting Suit (D1). This is the only MetaHuman route Marvelous documents. It cannot be run from Python: there is no DNA call in the API docs or in our 2026.1 module dump (D18, D19). No user report confirms that the points actually appear, so try one body first (I).
3. Save each one with File ▶ Save As ▶ Avatar. The .avt keeps the bounding volumes, the arrangement points and the fitting suit (D7).
4. From then on the script loads that .avt with `import_api.ImportAvatar(path, options)` instead of importing the FBX (D18). It places pieces with `GetArrangementList` and `SetArrangement`, then `SetArrangementPosition`, `SetArrangementOrientation` and `SetArrangementShapeStyle` (D18). Check once that ImportAvatar opens no dialog (I). Never use `ImportFile`: it always opens a dialog (D18).
5. Check in Blender that the DNA avatar's surface matches the game's body: the same rest pose, and within a few millimetres (I).

If step 2 fails, try these next, cheapest first:

- **A. The head on (I).** Import the whole MetaHuman, head and body, as FBX: Unreal's "Export Combined Skel Mesh" (D2, D24). Try it once at 45 degrees and once in a T-pose. Why: Marvelous's MetaHuman joint-mapping preset is named for the combined head-and-body mesh, its own route loads head and body together (D1), and its required IK joints include Head and Neck (D17). Every import we tried had no head.
- **B. Build the points by hand once (D5, D6, I).** In the Avatar Editor's Arrangement tab, open the stock Adult_V2 bounding volumes (.pan). Point each volume's two end joints at MetaHuman joints, for example upperarm_l to hand_l. Then open Adult_V2_Arrangement_Point.arr: the points hang on the volume names. Save the .pan and .arr. On each other body (same joint names), open both, press Fit to Avatar (All), and save the .avt. The stock .pan names Marvelous's own joints (Left_Arm, Left_Hand: I looked inside the file), so it will not attach to MetaHuman joints until each volume is re-pointed.
- **C. Skip points on our bodies (I).** Arrange the jacket on an avatar that has points: a .avt from step 3 or B, or one of Marvelous's 18 MetaHuman body types (D12). Save it as a .zprj. Then load only the garment onto our avatar with `ImportZprj` (bLoadGarment on, bLoadAvatar off; D18) and re-drape it with `ReDrape3DArrangement`, which is in our 2026.1 dump but not yet in the online docs (D19). That needs a fitting suit on our avatar (D9).

## 1. What Marvelous requires for automatic points

- **Pose:** only "a T-pose or A-pose" (D3, D4, D15). I found no documented arm-angle range, palm direction or leg spread.
- **Avatar rules** from CLO's avatar guide (D17): Y-up and outward-facing normals are required. Recommended: an A- or T-pose, at most 70,000 triangles, symmetric mesh and joints, and joint names that match CLO's or Marvelous's for IK.
- **Skeleton:** not needed for the option. OBJ files, which have no skeleton, offer it too (D3). Each bounding volume runs between two joints and follows them (D6, D7).
- **Head:** no page says a head is needed. Marvelous's own MetaHuman route always includes it (D1).
- **Units:** cm for MetaHumans (D25). Ours already came in at the right size.
- **Is it AI?** The pages do not say. The install holds a 139 MB "Auto_Arrangement_Model_2_2_0.eom" beside an AI runtime (onnxruntime.dll). So the fit is probably made by a trained model, and the "pose" message is a generic failure, not a measured angle check (I).
- **Hand route:** the Avatar Editor's Arrangement tab can add volumes (two joints, shape, size) and points (volume, X, Y, offset, wrap). It opens and saves .pan and .arr files. An .arr "can be used to apply Arrangement points to an *.OBJ avatar" (D5). A point is invisible without its volume (D6). There is an official how-to video from 18 December 2025 (D26). Auto Sewing works only with Marvelous's default volumes and points (D10).

## 2. The MetaHuman route, 2025.2 to 2026.1

- The DNA importer arrived in 2025.2, November 2025 (D14, D31). It takes body and head .dna files and gives one seamless avatar. Its options are unit, auto points and auto fitting suit (both "for humanoid avatars only") and axis. Joints can be posed and keyframed; .mtn motions are not supported (D1, D16).
- The .dna files come from Unreal: Creator's DCC Export, from 5.6 (D23); Export DNA on the DNA asset, in 5.8 (D22); or the 5.8 Python call (D21).
- The USD guide (D2) never names the avatar it drapes on. It exports the "Combined Skel Mesh" from the MetaHuman Editor only to transfer skin weights in Unreal. Its USD cloth works from Marvelous 2025.2 with Unreal 5.6 and later. The Library's 18 MetaHuman body types are locked .avte files meant for making outfits (D12).

## 3. Python

- No call adds, loads or fits arrangement points or bounding volumes (D18, D19).
- The import options do include `bAddArrangementPoints` and `bAutoCreateFittingSuit` (D18).
- Pieces cannot be moved freely in 3D. Two outside tool authors say placement goes only through arrangement points (D28, D29). `SetPatternPieceMove` moves pieces in the 2D window only (D18).
- Pattern JSON import and export exist, but I found no documentation of an "ArrangementPointDataMap" field.
- Auto Convert to Avatar ("Rigging Only" keeps the shape and adds joints; A-pose recommended) is a menu in the Avatar Editor, not an API call (D8, D14).

## Not found

- An arm-angle range, or any rule on palms, legs or the head.
- Any user report of the DNA import's points working or failing.
- Any API call to load .arr or .pan files, or to run Auto Convert.
- Whether ImportAvatar opens a dialog.
- Whether re-drape works on an FBX avatar. A 2023 CLO answer said only registered or converted avatars work (D27); 2025.0 Marvelous says avatars with a fitting suit do (D9).
- CLO's avatar-editor PDF: I could not extract its text.
- The CLO-SET troubleshooting post (D30) refused access.

## Sources

1. MetaHuman DNA Importer, Marvelous Designer support, 22 Oct 2025 (updated 4 Jun 2026), support.marvelousdesigner.com/hc/en-us/articles/51752244831897. Full.
2. Marvelous Designer to MetaHuman: USD Garment Integration Workflow, MD support, 24 Nov 2025 (upd. 10 Aug 2026), .../articles/52699135975705. Full.
3. 3D File (OBJ) Import/Export, MD support, upd. 22 Aug 2026, .../articles/47358223288601. Full.
4. 3D File (FBX) Import/Export, MD support, upd. 1 Sep 2026, .../articles/47358232885017. Full.
5. Avatar Editor (ver. 2025.0), MD support, upd. 6 Sep 2026, .../articles/47358128221337. Full.
6. Add Arrangement Point; Open/Save Arrangement Point; Add Bounding Volume; Open/Save and Reset Bounding Volume; Fit to Avatar, MD support, upd. 30–31 Oct 2025, .../articles/47358324263705, 47358280634905, 47358365447705, 47358328549913, 47358360672025. Full.
7. Marvelous Designer File Format; Avatar (*.avt) Open/Save, MD support, upd. 20 Jul 2026 and 30 Oct 2025, .../articles/47358169252633, 47358320191897. Full.
8. Auto Convert to Avatar (2024.0+), MD support, upd. 9 Feb 2026, .../articles/47358210639897. Full.
9. Auto Fitting (incl. Re-Drape 3D Arrangement), MD support, upd. 26 Sep 2026, .../articles/47358335130649. Full.
10. Auto Sewing (2025.0), MD support, upd. 6 Jul 2026, .../articles/47358149073305. Full.
11. Avatar IK Joint Mapping (2025.0), MD support, upd. 24 Mar 2026, .../articles/47358133151385. Full.
12. 18 Default MetaHuman Body Types, MD support, upd. 20 Aug 2026, .../articles/47358187017113. Full.
13. glTF 2.0 (2026.0), MD support, upd. 17 Sep 2026, .../articles/55686813557913. Full.
14. New Feature Lists 2025.x, 2026.0, 2026.1, MD support, upd. May–Sep 2026, .../articles/47358120307353, 55837641308313, 59743730927129. Full.
15. Automated Arrangement Point Creation, CLO support, 19 Jul 2018 (upd. 4 Jun 2026), support.clo3d.com/hc/en-us/articles/360001749467. Full.
16. CLO MetaHuman DNA Importer; Re-drape 3D Arrangement; Auto 3D Arrangement, CLO support, upd. Dec 2025–Oct 2026, .../articles/51821648831257, 360034333873, 13200837772185. Full.
17. Creating Avatar; Creating Avatar/Pose/Motion (IK Mapping), CLO-SET CONNECT support, upd. Feb 2026, support-connect.clo-set.com/hc/en-us/articles/45304313038233, 45304267742873. Full.
18. Marvelous Designer API docs (API List, ApiTypes, Changelog), CLO Virtual Fashion, covers MD 2024.2–2025.1, developer.marvelousdesigner.com. Import, arrangement and option sections read.
19. Our MD 2026.1 module dump, production/research/clothing-pipeline/md-api-2026.txt, undated. Searched.
20. The installed presets, Preset/Avatar (files dated 20 Aug 2026). File names and headers only.
21. MetaHuman Creator Python Scripting, Epic, undated (UE 5.8+), dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine. Summary.
22. Working with DNA on a Customized MetaHuman, Epic, undated, dev.epicgames.com/documentation/metahuman/working-with-dna-on-a-customized-metahuman-in-unreal-engine. Summary.
23. MetaHuman Creator Export Tool, Epic, undated, dev.epicgames.com/documentation/metahuman/metahuman-creator-export-tool-in-unreal-engine. Summary.
24. "Fully Combined Metahuman Option", Epic forums, 18 Jul 2025, forums.unrealengine.com/t/2610178. Summary.
25. How to export an avatar (body) for Marvelous Designer from Maya (MetaHuman), virtualfilmer.com, Jun 2024. Summary.
26. "Marvelous Designer 2025.2: Set up Arrangement Points for Custom Avatars", Marvelous Designer on YouTube, 18 Dec 2025, youtube.com/watch?v=ftml9Wqdv5s. Description only; no transcript.
27. CLO community posts (Oct 2023, Apr 2024, 2021–23), support.clo3d.com/hc/en-us/community/posts/23767085277465, 31841064098969, 900003193903. Full.
28. mcp-for-clo3d, place_pattern tool, glama.ai, 26 Sep 2026. Summary.
29. Laboon2501/MarvelousDesigner-MCP README, GitHub, 19 Sep 2026. Searched.
30. "Troubleshooting: Auto Fitting and Arrangement Points", CLO-SET community, undated, connect.clo-set.com/community/post/12dc15957be44852b7ec66959a774353. Search snippet only (403).
31. "Marvelous Designer 2025.2: MetaHumans, Pleats & Keyframes", Digital Production, 18 Nov 2025. Summary.
