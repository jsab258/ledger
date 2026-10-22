# Lamp post C's staining, after two tries: research for the third direction (22 October 2026)

His ruling of 21 October asks for the concrete columns "weathered and a shade darker". His message of 22 October says, with item 7 blocked: "then the lamp's staining". Two tries on 21 October drew rain streaks in the kit's shared material, as a world-aligned map of runs. Both read as "a uniform full-height grain ... with no rain runs from the arm, joint, spigot or plate" (production/audits/gate-lamp-post-C/GATE.md). The research direction set then was runs placed from their sources: decals, or staining baked onto the column. This note takes the second.

D = read at the source; M = measured here; I = inference; U = unverified.

## Questions

1. What staining does the column's own design ask for, and where?
2. Why did the two tries fail?
3. Decals or a bake, for a square concrete shaft?
4. How does a baked stain reach the kit's shared material without changing other pieces?

## 1. The design's own wear rows (production/cloud-week/targets/lamp-posts/TARGET.md, read 22 October) (D)

- **lime_streaks:** from the top face and the arm, 6 to 10 vertical lime streaks, 30 to 400 mm long and 4 to 20 mm wide. They are pale (190, 188, 180), on every face, strongest under the arm.
- **arm_lime:** 2 to 4 lime streaks from the arm's underside and end face, 30 to 150 mm long, 4 to 12 mm wide.
- **rust_bleed:** two rust-brown streaks under the door plate's two screws, on the -y face, 60 to 200 mm long and 4 to 8 mm wide (bare_steel_rust 94, 58, 40).
- **spigot_rust:** one rust streak, 20 to 60 mm long, under the spigot at the arm's end.
- **algae:** green algae on the -y face (the shaded face) from the footway to 700 mm, patchy, strongest below 300 mm. A lighter film on the other three faces, to 350 mm.
- **arm_algae:** a patchy green film (86, 104, 70) on the arm's top face, strength 0.35.
- **Left out:** the chipped arris is for one column (LC 2) only. The game stands one mesh at all four lamp spots, so it is not drawn.

The rows are the design's judgement, not measured from photographs; it says so itself (U as to period evidence).

## 2. Why the two tries failed (M, from the gate record)

The runs were a tiling map, world-aligned and the same on every face and at every height. Nothing tied them to the arm, the spigot or the plate, so they read as grain. The design asks for a few named runs from named sources, pale lime and rust, not an even darker grain.

## 3. Decals or a bake (I, from the 7 October research and today's)

- **Projected decals** fade only along their throw (production/research/street-wear/PAINTED-FRONTS-2026-10-07.md, 1). On a 220 mm square shaft each face would need its own decal, and the arm's faces their own. The design's pictures (the wear masks, production/cloud-week/2d/wear) are drawn for walls.
- **A bake** places each run exactly where the design puts it, on every face, in one picture. That is the industry's way for a unique piece: masks from the model's own position and facing (Adobe, Substance 3D Painter, Dirt and Metal Edge Wear generators, read today for Rita's front; production/research/street-wear/FRONT-WEAR-BAKE-2026-10-22.md).
- The same method passed on Rita's front today, through eight views.

## 4. Into the shared material (D, tools/ue/make_kit_materials.py read 22 October)

- **The master gains one optional stain.** M_LedgerKit builds every kit slot's colour from parameters: detail, dirt, streaks and top growth, all world-aligned. The addition is a StainMap texture on the piece's first UV and a StainStrength, default 0. The colour becomes lerp(colour, stain RGB, stain A × StainStrength).
- **At strength 0 nothing changes.** Every other kit piece and slot stays as it was (I; checked by measuring the column's other slots).
- **The column's slot** (concrete_C) takes the stain map and strength 1, and its world-aligned streaks off.
- **The column's faces get their own unwrap on that first UV.** Nothing else on those faces reads it: the detail and the streaks are world-aligned (D, the graph).

## Method

A recipe (tools/art-recipes/kit_stain.py, with its spec production/specs/kit-wear/lamp_post_C.json):
1. **Unwrap** the slot's faces alone into the first UV of the piece's game copy.
2. **Bake** each texel's position and facing in the piece's own frame (Cycles emission into float pictures).
3. **Draw** the design's named features on them in numpy, each from its own source: a few streaks with seeded positions, widths and lengths, fading downward; the algae patches on the shaded face and the arm's top.
4. **Write** one RGBA picture: the colour, and its amount in alpha.

The numbers are the design's, kept in the spec.

## Acceptance

- **Nothing else moves.** The column's darker concrete and grimy foot (his ruling, passed) and the other slots are unchanged away from the features: measured on BEFORE and NEW.
- **The close view reads it.** From the road by day, lime runs hang from the arm and the top, and rust from the plate and the spigot. They are not an even grain: measured as a handful of distinct runs.
- **Then the gate.** The lamp's views each go to a fresh reviewer: hook by day, reverse by day, and the close views from the road and from under, by day and at night.

## Unreached

- No photograph of a 1960s precast concrete column's staining was read today. The design's rows are its own judgement.
