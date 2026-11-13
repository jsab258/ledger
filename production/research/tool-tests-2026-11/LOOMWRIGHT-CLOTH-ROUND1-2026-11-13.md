# Loomwright cloth, round 1 (13 November 2026)

His own replacement for Houdini (C:\Game Dev Tools\Loomwright), advisor 119 and 120: its cloth module, after its hair (LOOMWRIGHT-HAIR-ROUND1-2026-11-12.md, rounds 1 and 2). Work folder F:/LedgerTools/tool-tests-2026-11/loomwright-cloth; nothing written into his folder; nothing enters the game.

Method researched: production/research/tool-tests-2026-11/VELLUM-METHOD-2026-11-12.md, 12 Nov 2026 (the professional garment route, with the game-garment skill: pattern pieces sewn and draped on the real avatar, then skinned to the MetaHuman skeleton, only loose parts simulated; SideFX's paneling and drape pre-roll), and the tool's own MECHANICS.md (cloth.rs: XPBD, 1 substep, 100 iterations; SideFX's own page warns 1 substep per 100 iterations is very stretchy).

## Verdict

**Level 1 (is it good at the job): fails.** Its example job (Tom's shirt, jumper and jacket in three layers) passes all 17 of its own checks, but the picture shows the jacket's and the jumper's collar and shoulders crumpled into torn, jagged sheets, the jumper showing through the jacket at the chest and back, and every layer on a built-in mannequin (cylinders and an egg head), not Tom's body. Nothing here could be judged against the clothing floor, let alone the 2026 bar.

**Level 2 (can the builder use it): passes.** One job file, no clicks, 96 s for three layers and three crowd refits, the same bytes twice (its verify: fingerprint 12ba339b…, every file and number identical), a report with every check.

## The test

| Job | Result |
|---|---|
| cloth_tom_layers (its example: shirt cotton, jumper knit with ribs, jacket wool; body 1.78 m, chest 98, waist 86, hips 98 cm; three crowd bodies) | runs, rc 0, 96.1 s; 17 checks pass, one left to a person (Marvelous's numbers) |
| Same job again (verify) | identical output |
| On Tom's MetaHuman body | not possible: the job takes only height, chest, waist, hips and arm angle; there is no body file input |
| Skinned for Unreal | not possible: garments.fbx holds static meshes (ASCII FBX, metres, Y up), no skeleton or weights |

## Numbers

- Hems: shirt 0.98 m, jumper 1.05 m, jacket 0.95 m; sleeve ends 1.27, 1.19, 1.11 m (A-pose 45 degrees).
- Stretch: 95th percentile 1.0% on every layer; mean 0.43 to 0.65%.
- Cloth inside body: shirt 0, jumper 0.58%, jacket 0.28%; body through cloth: jacket 2 points; layer through layer: 0 counted.
- Ribs grip: shirt collar 16.7%, jumper 29.0%.
- Picture: production/previews/loomwright-cloth-round1-2026-11-13.jpg (front | back | without the jacket).

## What works

- Job files, exit codes, report.json, a job log and a stretch map; same result twice to the byte.
- The layer order and the checks are the right kind (inside body, body through cloth, stretch, hem drop, rib grip, layer through layer, a slot for Marvelous's fit-check numbers).
- Patterns from FreeSewing SVG or Marvelous/AAMA DXF are accepted (not run this round).
- Crowd refits run in the same job.

## What fails, and why

1. **The collar and shoulders crumple and tear** on the jumper and the jacket (seen front and back). Most likely: the built-in garments start overlapping the layer underneath (MECHANICS: friction between garments is relaxed for that reason), and with 1 substep the solver cannot settle them; the checks count points inside, not folds or self-crossing.
2. **Its checks pass a garment that is visibly wrong.** Layer through layer reads 0 while orange shows through the jacket; no self-collision or crumple measure; stretch capped at 1.0% reads as perfect because woven stretch is effectively inextensible.
3. **No real body.** Only four measurements; the game's garments are fitted to each MetaHuman's own body mesh.
4. **No skinning.** The output is static; the game needs skeletal meshes bound to the MetaHuman skeleton (our Blender chain does this).
5. ASCII FBX, which Blender refuses (round 1 found the same).

## Improvements, most useful first

1. A body file input (OBJ or FBX of the MetaHuman body in A-pose), as the hair module now takes a scalp.
2. A self-collision pass and a crumple check (largest fold angle, self-crossing faces), and layer-through-layer counted from the camera, not only at points.
3. More substeps (SideFX: 5 for clothing) and a sewing pre-roll (seams pulled together with gravity off) instead of starting garments overlapped.
4. Skin weights copied from the body to the garment (nearest-surface transfer, then smoothing), with the MetaHuman skeleton in the FBX.
5. Binary FBX.

## Against the others

Marvelous with our Blender chain makes Tom's jumper and jacket that passed in the packaged game; Vellum was set aside after three tries; Seamshift refits a finished garment cleanly. Loomwright's cloth, as it stands, is not a route for the game's garments.

Cost: about 0.2 h builder time, no helpers ("tool test: Loomwright cloth round 1").
