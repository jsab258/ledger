# Tom's shoes: the plan (30 October 2026)

His order C9: the jumper, jeans and shoes after the cuffs. His casting sheet: leather shoes (SPEC.md). Reference first: Mafia's shoes, a median 6,718 triangles over 18 at full detail (1,780 to 9,964), textures 512 (Study 6); LEDGER's target about 6,000 triangles, 512 to 1024, rigid (SPEC.md). How Mafia builds a shoe was not read (none found).

## What failed before

Three procedural tries each for Darren's trainers and Sheila's lace-ups (30 September; production/art/clothing/footwear/README.md): lofted from the body's own foot, they read as slippers to a blind reviewer (the toe, the lacing). Ron's boots passed from the first version of the same script. Epic's own free garments, tried on 22 October (DECISIONS), hold only yellow modern trainers.

## How it is done professionally (a read-only helper, every page read 30 October 2026)

- Artists' breakdowns agree on one chain: a blockout from photographs (subdivision modelling, once Marvelous for the upper), a sculpt of wrinkles and stitches, retopology, a bake, painted textures (80 Level, 9 February 2026, https://80.lv/articles/how-to-model-texture-a-pair-of-dr-martens-boots-using-blender; 18 June 2025, https://80.lv/articles/creating-realistic-tactical-boots-with-zbrush-substance-3d; Games Artist 2021, https://gamesartist.co.uk/rick-o-connel-character-breakdown-johannes-magnusson/). No studio talk found; none mentions a shoe last.
- A scanned boot sold on Fab: scan, sculpt, 2,774 triangles, 4K (https://forums.unrealengine.com/t/finkals-leather-mid-calf-boot-3d-scan-highpoly-lowpoly/2696640). Range seen: about 2,800 to 21,000 triangles, 2K to 4K textures.
- Epic: a MetaHuman outfit's foot is hidden by the Body Hidden Face Map (https://dev.epicgames.com/documentation/metahuman/testing-and-configuring-your-parametric-outfit-asset); no shoe-specific page.

## Free scanned shoes

- **CC0:** none suitable. Poly Haven has only rubber boots; Sketchfab's CC0 filter has no men's 1990 lace-up (searched shoe, oxford, brogue, derby, dress shoe and others); the Smithsonian site was not reached.
- **CC BY 4.0, the one candidate:** "Old Oxford Shoe" by inciprocal, a photo scan of an old brown leather oxford, one shoe, 19,982 triangles, 9,993 vertices, 4K PBR, downloadable, published 9 June 2021 (https://sketchfab.com/3d-models/old-oxford-shoe-29a5ed053eab46a7af308215600985a2; its licence read from Sketchfab's own data 30 October: "CC Attribution", http://creativecommons.org/licenses/by/4.0/, "Author must be credited. Commercial use is allowed."; no NoAI mark in its data). Its description names the maker's brand (TJTJ); whether any mark shows on the shoe is not checked (unverified).

## The routes

1. **The scan (recommended, on his word):** downloaded by him (Sketchfab needs a sign-in, which is his), mirrored for the left foot, retopologised to about 6,000 triangles a pair with the scan baked into 1024 maps, fitted to his foot (ease 4 to 5 mm, a flat sole: FOOTWEAR-2026-09-30.md), skinned to foot and ball, his feet hidden, credited in THIRD-PARTY.md. About 4 to 6 hours. The licence allowlist names CC0 libraries for 3D and not CC BY; his ruling of 3 October lets people wear garments from "unmarked CC-BY with credit", so this is his call.
2. **Our own:** the professional chain by hand in Blender (blockout from dated photographs, multires sculpt, retopology, bake). About 15 to 25 hours, with three failed procedural tries behind it.

Waiting on: his word (Needs you).

## The scan fitted (30 October, 09:58 to 10:46, a helper; F:/LedgerTools/garments/tom/shoes/out/summary.json)

- **Correction: the scan is not an oxford.** Its title says "Old Oxford Shoe", but the model is a square-toe slip-on with an apron toe and elastic side gores (seen in the helper's renders, bake/look/). This plan called it an oxford from the title without looking at the model. Whether a square toe suits 1990 is his call (canon): secondary sources disagree (LoveToKnow: square toes "trendy with some men in the late 1980s and early 1990s", https://shoes.maint.lovetoknow.com/Mens_Square_Toe_Dress_Shoes; Mel Magazine: their apex in the 1990s, Friends and later, https://melmagazine.com/en-us/story/square-toe-shoes-men; search snippets only, unverified).
- **Placed:** a right shoe, mirrored for the left; scaled 1.139 along, 1.253 across, 1.118 up (349 mm long on his 305 mm foot, width capped at 10% over the scan's own proportions); the collar and throat eased out locally (up to 19 mm) so the ankle clears. Toe gap 22.7 and 23.3 mm, heel 13.2 and 14.1 mm, ease in the opening 3.0 to 3.6 mm (under the 4 to 5 mm target); sole tilt 0.3 degrees. The soles stand 16.6 mm under his floor: the body is raised 17 mm (garments.json raise_mm, as Ron's boots).
- **Foot through the shoe:** 47 and 45 points beyond 1 mm (worst 11.5 mm, heel back, instep, ball sides). The game cannot hide the body's feet (MetaHuman removes hidden faces only when a character is built), so these would show: the shoe is to be eased out locally where the foot comes through, as Ron's boots were made by offsetting the body's own foot.
- **Game mesh:** 3,004 triangles a shoe (6,008 a pair; Mafia's median 6,718), levels 1,502, 750 and 304; silhouette within 0.6 mm of the scan; UVs 18 islands, no overlap. **Bake (1024):** hits 99.999%, normals over 60 degrees off 0.042%; the copyright corner nowhere on the surface (tested with a magenta corner: 0 texels). A faint, illegible trace of the moulded brand remains in the outsole's waist under a strong contrast stretch (listed). **Skin:** rigid on foot, the toe box on ball over a 20 mm slanted blend (the footwear research says 30 to 40 mm: to widen), at most 2 influences; through by more than 3 mm: walking 2 points (3.7 mm), stairs 3 and 3 (6.1 mm).
- **Waiting on:** his word on the square toe; then the foot's ease and the ball's blend, the import, the editor walk and a fresh reviewer.

## His decision (30 October, about 11:55)

No to the scan: its square toe is a late-1990s fashion, wrong for 1990, and his foot came through it. Tom wears the lace-up boots Ron wears in the game, black with dark laces and sole, under his jeans; the scan's files stay on F:, out of the game, its credit line out. Ron's boots are this project's own (tools/meshgen/blender/model_footwear.py's first version on Ron's foot, passed a blind review on 30 September; F:/LedgerTools/garments/ron_boots), not Epic's: Epic's lace-up boots left the project with the 3 October ruling and would need his Fab sign-in. They are carried onto Tom's feet by the MetaHuman bodies' shared layout (a helper, F:/LedgerTools/garments/tom/boots).

**Why reuse-first missed them:** the search for shoes looked outward (scans, Epic's packs) and read Ron's boots, in this plan's own first section, as the method that failed twice on the others' shoes, not as a finished pair already worn in the game; garments.json, where they are listed, was never searched as a source.
