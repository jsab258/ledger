# Faces beyond the preset blends, and 1990 hair (28 September 2026)

The problem: Sheila (53, pale, lined, white English, thin mouth, grey-blue eyes, "greying brown, a short shampoo-and-set perm") and Darren (25, thin, narrow, pale; "a grown-out perm with bleached tips") failed twice as blends of Epic's MetaHuman presets: only three shipped female presets read white European, all of Sheila's candidates looked alike and leaned East Asian from the front, and the wardrobe's haircuts gave a modern crop and a straight bob with a white dip-dye. Researched by a separate helper; checked 28 September 2026.

## Faces

- The UE 5.8 MetaHuman Python API (examples in Engine/Plugins/MetaHuman/MetaHumanCharacter/Content/Python/examples) conforms from DNA, template, vertices, an Identity, or a custom mesh with a portrait; sculpts by `translate_face_landmarks`; and gets and sets the face's PCA coefficients. No preset or region blend is exposed. Doc: https://dev.epicgames.com/documentation/metahuman/metahuman-creator-python-scripting-in-unreal-engine . MetaHuman 5.8 released 17 June 2026; Mesh to MetaHuman takes any topology: https://forums.unrealengine.com/t/metahuman-5-8-released/2729288
- Cheap, inside MetaHuman (inferred): the difference between the European presets' face coefficients and the rest is a direction; push a face along it, then sculpt landmarks (nose bridge, lips).
- Free, bigger: MPFB2 (MakeHuman for Blender; code GPLv3, output CC0, allowed for sale): a head with ethnicity fully Caucasian and the character's age, sex and build, rendered front-on, then `track_face_landmarks_from_image` and `conform_to_target_meshes`, then sculpt. https://static.makehumancommunity.org/mpfb/faq/is_it_really_free.html ; https://www.cgchannel.com/2025/03/check-out-open-source-blender-character-generation-plugin-mpfb-2/ (March 2025). CC0 is on the licence allowlist.
- Fab editable presets (.mhpkg): paid CHF 4-15, a few free; need Jafar signed in; avoid ones named after real people.

## Hair

- No curl or wave parameter exists on a MetaHuman groom (5.8 source): scriptable parameters are colour only; curl is geometry, so it takes a different groom.
- Fab: "Curly Short 01" and "02" (AnnaLev), CHF 8.95 Personal, 17.02 Professional, with .mhpkg, Alembic source and a wardrobe item; "02" looks like a 1990 man's perm; nothing on Fab looks like a 1990 set. The listings say "Allows usage with AI: No". https://www.fab.com/listings/1797432c-a0bb-49c7-8439-416ad2bb9180 ; https://www.fab.com/listings/eddf64e5-09cf-4f0f-a3d7-a39e56c0fb74 . Money and a licence condition: his decision.
- Blender: hair curves shaped with Blender's Curl, Frizz and Clump node groups, exported as Alembic; the UE import and `GroomBlueprintLibrary.create_new_groom_binding_asset` are scriptable; a groom binding in a monitored folder becomes a MetaHuman wardrobe item: https://dev.epicgames.com/documentation/metahuman/hair-and-clothing-tools . Free and unattended; the risk is whether scripted curls look right.
- Ombre colours every strand along its length (Shift: where, Contrast: how hard, 0 soft; Intensity; OmbreMelanin, OmbreRedness). A hard white band means high contrast or intensity or white; for bleached tips try Contrast 0, Intensity about 0.5, low melanin with slight redness. Highlights colour some strands by a per-groom mask: streaks, not tips.

## Documented or inferred

Documented: the API calls, the wardrobe's colour-only parameters, the Fab listings and prices, MPFB2's licence. Inferred: that a European MPFB2 head or a coefficient push removes the East Asian lean, and how Ombre's Shift runs.
