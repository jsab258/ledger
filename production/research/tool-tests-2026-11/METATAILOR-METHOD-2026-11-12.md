Method note for the MetaTailor free test (12 Nov 2026)

Questions: (1) MetaTailor's own fitting workflow, step by step; (2) what it takes in and gives out; (3) the free version's limits; (4) whether anything runs without clicks; (5) the licence of what it exports. Read 2026-11-12.

## 1. Workflow
- No official manual was found on the web (two searches, 12 Nov); the makers point to their YouTube channel and Discord (CG Channel, 2 Feb 2026, read in full: https://www.cgchannel.com/2026/02/metatailor-2-5-is-out-with-new-bridge-plugins-to-unity-and-ue5/). Neither was read: unverified.
- Steps as one secondary source gives them (Style3D blog, read in full, dates inconsistent on the page: https://www.style3d.com/blog/?p=14278): export a clean body from MetaHuman; in MetaTailor a new project, Import Avatar; Import, Cloth: one garment piece at a time, each given a category (top, bottom, jacket), placed and scaled, confirmed; the app fits and skin-weights "within seconds"; File, Export FBX. Auto weights "may require manual correction for extreme animations". Fit settings are not described.
- CG Channel: garments auto-fit to "any bipedal 3D character"; results refined with sculpt brushes.
- Reference (his 28 Oct rule): none found in Mafia or KCD2 for this tool (in-house pipelines); the method is the vendor's as read.

## 2. In and out
- In: "any 3D wearable" (CG Channel); FBX in the Style3D steps. The install holds Unity's FBX SDK and USD plug-ins (its own files, F:/LedgerTools/tool-tests-2026-11/metatailor/app/META-Tailor_Data/Plugins): FBX in and out confirmed by file presence only.
- Out: FBX (both sources). The Unreal bridge avoids FBX but is Pro only since 2.5 (CG Channel).

## 3. Free limits
- Free: base features, up to 5 FBX exports a month; Pro US$35 a month or US$336 a year, unlimited exports and the bridges (CG Channel). Rental only; Windows only. A January 2024 forum post said test animations are locked on Free (search result only, unread: unverified).

## 4. Without clicks
- No command line or batch mode is mentioned anywhere read. Its install lists start_exe_args null (app_data.json). It is a Unity program: every step is a click. His ruling of 12 Nov allows clicks in MetaTailor for this free test only, after 10 idle minutes, never while the build machine runs.

## 5. Export licence
- Not stated in anything read; whether exports stay usable after a rental ends is unverified (wardrobe-at-scale/3-METAHUMAN-AND-FAB.md). Test only: nothing exported enters the game.

## The test, from this method
- Body: Sheila's S4 body as FBX (the one her refit used); garment: Tom's jumper game mesh (garments/tom/jumper/chain-j3d/game/jumper_game.blend, as the cardigan refit started from), exported FBX by Blender headless.
- In MetaTailor: Import Avatar, Import Cloth (category top), fit, one FBX export (1 of 5).
- Checks: the same as the Blender refit (SHEILA-CARDIGAN-S4-2026-11-11.md: points pushed out and through the body over 1 and 3 mm, neckband hole, band heights), clicks counted, minutes against the refit's 3.2 h. Blouse under it only if the jumper alone fits.

## Unreached
- MetaTailor's YouTube tutorials and Discord; its terms of service; the 80.lv articles (search results only).
