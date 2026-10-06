# Tom's face: the method, and why ten steps stalled

Research, 6–7 October 2026, item 1.2. **O** opened and read (a web page, or a file Epic ships with UE 5.8 on this PC); **S** search summary only; **I** inference. Login-walled pages were not reached and count for nothing.

## 1. Casting to a brief

- Epic's order: preset, blend (up to three presets, whole head or region; "Both", "Feature" or "Proportions"), sculpt, skin, hair. Epic names no preset ages or builds. O: [Blend](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-blend-tool-in-unreal-engine), [Presets](https://dev.epicgames.com/documentation/metahuman/metahuman-presets-in-unreal-engine), undated.
- Studios casting to a brief sculpt from reference and fit the MetaHuman to the sculpt. O: [80.lv, 11 May 2026](https://80.lv/articles/creating-a-mesmerizing-and-cinematic-real-time-character-using-zbrush-and-unreal-engine-5); [fxguide, 9 June 2022](https://www.fxguide.com/fxfeatured/huge-update-for-metahuman-import-your-own-head/).
- Apparent age: the Face Texture Index "can help make your character look younger or older"; Accents set under-eye darkness. O: [Skin tools](https://dev.epicgames.com/documentation/metahuman/skin-material-tools?lang=en-US). Lean: body constraints "Neck" and "Neck Base" (circumference, cm) beside Fat. O: plugin source.
- Male presets from their previews (I): European men are Bruce (~45, heavy), Orlando (35–40), Victor (35, lean), Lorenzo (~50), Walter (~60). The 20-to-30 men (Bo, Mikel, Cameron, Mateo, Trey) are not European. No lean European near 30 exists; Tom is 70% Walter.
- Regional blending is C++ only, not in Python. O: MetaHumanCharacterEditorSubsystem.h; I.
- Reviewers' ages: B2 25–27, D2 29, H2–I2 35–40 (after darker under-eyes), J2 28–30, L1 30–33. Age now follows skin and lids more than shape (I).

## 2. Why the brows stay pale

- Each groom's colour lives in the character's instance parameters (Melanin, Redness, Roughness, Whiteness, Lightness, DyeColor); Melanin's default is **0.16**, pale. O: MetaHumanDefaultGroomPipeline.h.
- At build, the eyebrow item's Melanin, Redness and Whiteness are copied into the face skin (EyebrowsMelanin…) and a painted brow layer is baked into the face texture. O: MetaHumanDefaultGroomPipeline.cpp, MF_BakedGroomTextures; brows run "StrandsToCardsToTexture" (WI_Eyebrows_M_Dense). Tom's built face reads only that baked colour (O: MI_Face_Skin_Baked_LOD1).
- recolour_hair sets hairMelanin on the groom material after the build: strands change, the painted brow beneath keeps the build-time colour (I).
- Epic's documented, scriptable fix, before the build: preview collection, assemble_for_preview, get_instance_parameters(item), set "Melanin", on_edit_preview_collection. O: example_add_grooms.py and test_set_character_instance_params.py, shipped with 5.8. The script's comment that this "is not open to scripts" is out of date.
- Lashes: Short Sparse/Fine/Thin, Long Slight Curl/Curl/Thick Curl; strands or cards. O: [Teeth and Eyelashes](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-teeth-and-eyelashes-tool-in-unreal-engine). Faint lashes likely share the pale default (I).

## 3. Shave shadow

- The skin filter sorts the 153 face textures by wrinkles, stubble and marks (O: Skin tools; Epic's texture_attributes.json).
- **Texture 85 has stubble "None"** and marks "Medium": the missing shadow, and probably the red spots (I).
- Low wrinkles, low marks: stubble low 43, 66, 84, 131, 145, 150; stubble medium 23, 27, 30, 31, 32, 57, 79, 98, 134, 142, 148 (O: table).
- A darker chin accent (steps K–M) tints the chin evenly; it draws no beard shape (I).
- Other routes: Epic's Beard_S_Stubble groom (O; the sheet says clean-shaven); the skin's "Hair Mask Beard" multiply (O: M_skin_unified), live only in an unbaked build, which 5.8 allows on UE Cine alone (O: [5.8 notes](https://dev.epicgames.com/documentation/metahuman/metahuman-5-8-release-notes-in-unreal-engine), pipeline source); a painted Texture Override (O: Skin tools).

## 4. Period haircuts within the allowlist

- Epic's: S_Clean, S_Casual, S_BrushCut, S_SideSweptFringe, S_Messy, S_RecedeMessy, S_SlickBack, S_SweptUp, S_BuzzCut, M_SideSweptFringe (O). L1's S_Clean already read as a tapered short back and sides.
- Fab, five men's short grooms opened 6 October, all "Allows usage with AI: No", so out under the 3 October ruling; four paid, CHF 4–90 (O): [Male 11](https://www.fab.com/listings/eb7f2500-56d2-49ed-bbf4-ce48f639b373), [Side Part](https://www.fab.com/listings/51cfebdf-fe5e-4b6c-bbb9-98d9775655d5), [GroomLab](https://www.fab.com/listings/77ad5940-b9b1-40b9-9a22-75afab29a4c0), [Hair Short](https://www.fab.com/listings/d042865f-0d8d-4668-9061-5a663c9da4f3), [Wavy](https://www.fab.com/listings/b70a09bc-c1f8-4ed6-a4f6-9a7c14c4740f). No CC0 men's groom found (S).
- Matte: the Roughness instance parameter (default 0.25), set before the build (O).
- Flatter needs a new groom: Epic's groom tools need Houdini 21 (O: [Groom Tools](https://dev.epicgames.com/documentation/metahuman/groom-tools)); Indie $299 a year, Apprentice non-commercial (S); or Blender curves to Alembic (S). Darren's Blender curls were set aside after three tries.

## 5. If the sliders cannot reach him

- **Sculpt and conform:** export the head, reshape jaw and neck in Blender keeping topology, return it through From Template with "Match Vertices by UVs"; joints and weights regenerate, the head rig is remade by the cloud. O: [From Template](https://dev.epicgames.com/documentation/metahuman/metahuman-creator-from-template-tool-in-unreal-engine). No money; a session's time.
- **Scans:** 3D Scan Store's MetaHuman Identity, £29.99 personal, £329.98 one commercial project (O: [Male 20](https://www.3dscanstore.com/metahuman/metahuman_identity_male_20)); Digital Reality Lab free with credit (O: [samples](https://www.digitalrealitylab.com/sample-model/)). Neither is CC0 or Fab, and each is a real likeness, which the allowlist never ships: his call (licence, money).

## Next two experiments, cheapest first

**N1, colour and skin the documented way (one prepare-and-build, about an hour).**

- Build: L1's face, shape unchanged, on texture 85 (control), 84, 31 and 148. Before the build, set Hair, Eyebrows and Eyelashes instance parameters (Melanin 0.75, Redness 0.08, Roughness 0.55, ombre and highlights off); neck 37 cm; no chin accent.
- Measure: the built face's EyebrowsMelanin equals the value set; in the studio portrait, brow brightness against hair, and upper lip and chin against cheek.
- Pass (fresh blind reviewer): brows match the hair within 10%; a visible shave shadow, no spots; reads 29–34; no new fault.

**N2, lean jaw and neck by sculpt (a day), from N1's best.**

- Build: in Blender, narrow jaw angle, lower cheeks and neck, topology unchanged; From Template with "Match Vertices by UVs"; full rig rebuilt.
- Measure: jaw width at the angle against cheekbone width; neck against jaw, front and profile.
- Pass (fresh blind reviewer): lean, 30–34, no rig fault in talk or expressions. If the cut still reads modern, a Blender short back and sides comes third.
