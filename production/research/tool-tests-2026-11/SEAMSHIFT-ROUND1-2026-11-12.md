# Seamshift, round 1 (12 November 2026)

His ask (advisor 119 and 120, 20:15 and 20:20): test his own MetaTailor replacement first. It's his own tool, so no licence, virus or contents check. Work folder: F:/LedgerTools/tool-tests-2026-11/seamshift-r1. That holds copies of the jobs pointing their output there, plus outputs, logs and our measurements. His folder was not changed. Picture: production/previews/seamshift-round1-2026-11-12.jpg. On top: Tom's jumper on Sheila S4 (front, three-quarter, back, neck). Below: blouse under cardigan on Sheila S4 (the identity run) and on Lena C1.

Method researched: METATAILOR-METHOD-2026-11-12.md and the Sheila refit (SHEILA-CARDIGAN-S4-2026-11-11.md). The professional method is the same: carry the garment through the skeleton and the body shape, solve collisions with a clearance, transfer skin weights from the target body, check in test poses. Same body files, same garment, same measuring script (measure_fit.py) as MetaTailor's test this morning, so the numbers sit side by side.

## Verdict: on Tom's jumper onto Sheila it is the best refit we have had. It is clean on every check, and it takes 0.8 s instead of MetaTailor's failure or the Blender chain's 3.2 h. On a layered, hand-made garment (her cardigan over her blouse) it fails three of four bodies. The cuffs shrink by a third on smaller bodies, and body-through counts double. The blouse passes everywhere. Keep for round 2 on the cardigan faults; it can already do a plain pullover's refit.

## The test
- Seamshift's release build (target/release/seamshift.exe) was run headless from job files: `run jobs/<job>.json`, with no clicks and no window.
- Jobs: its own tom-jumper-to-sheila, tom-jumper-to-cast (Sheila, Ron, Darren) and ron-shirt-and-jacket-layers, copied with outputs moved. Plus one of ours, sheila-layers-to-cast. That one fits her final blouse (blouse-under-cardigan) inside her final cardigan (chain3n), from S4 onto S4 itself (identity), Lena C1, Build Heavy and Sam C5.
- Our own measuring was measure_fit.py in Blender 5.2 headless, on its skinned FBX files.

## Numbers: Tom's jumper onto Sheila S4 (rest pose, our script)
| Check | Seamshift | MetaTailor (12 Nov) | Blender carry, step 1 (11 Nov) |
|---|---|---|---|
| Cloth inside body over 1 / 3 mm | 0 / 0 | 6 / 6 | 56 / 44 |
| Body through cloth over 3 mm | 41 (trunk 36, right arm 5; deepest 17.8 mm) | 3,022 | 299 |
| Cuffs L / R (Tom's own 74.6 / 75.0) | 72.7 / 74.0 | 40.6 / 39.2 | 67.3 / 67.6 |
| Welt F / B (Tom's own 76.9 / 74.6) | 76.6 / 75.6 | 64.7 / 90.0 | 72.5 / 66.7 |
| Crew band (Tom's own 29.2) | 28.0 | 25.2 | 30.7 |
| Neck hole | 161 x 104 mm, clear 5.0 to 26.5 mm, none inside | 177 x 99 | 138 x 44 |
| Gap median chest / waist / hip | 7.2 / 29.3 / 29.3 mm | 27.9 / 32.0 / 8.3 | 11.6 / 30.9 / 28.1 |
| Skin | 8 bones max (cap), mean 4.3, none unweighted, rest deform 0.0 mm | up to 21 per point | not skinned |
| Mesh | 9,860 points, 19,480 tris, both materials, both UV sets kept | UV set lost, points split | unchanged |
| Time | 0.8 s per garment per body | about 11 min in the app plus 22 preparing | 3.2 h whole chain |
- Its own numbers match ours exactly (41 / 0, the same band heights). Its claims in MECHANICS.md hold.
- The same bytes came out on two runs (skinned FBX, static FBX, result).
- Its test poses: walk, sit and arms up all pass. By eye, in the sit pose the hem balloons across the thighs at the back. With arms up the body of the jumper stays put, which is normal for skinning alone.
- Its other jobs all pass at 0.4 to 1.6 s each: the cast (Sheila 60/0, Ron 120/18, Darren 114/0 by its own check) and Ron's shirt under his double-walled suit jacket, on Tom and on Sheila.

## Numbers: Sheila's blouse under her cardigan (its own check; our script on C1)
| Body | Blouse | Cardigan: through over 3 mm / bands (ratios to source) / test poses |
|---|---|---|
| S4 (identity, should change nothing) | pass, 0 / 0 | FAIL: 503 (the source alone: 259); bands 1.08, 1.00, 0.97, 1.01, 1.07; walk 475 through |
| Lena C1 | pass, 0 / 0 | FAIL: 509; cuffs 0.64 / 0.68; walk 467, sit 468 |
| Build Heavy | pass | FAIL on bands only: one cuff 0.68, crew band 1.58; walk 480 through |
| Sam C5 | pass, 2 / 0 | FAIL: 510; cuffs 0.69 / 0.71 |
- Our script agrees on C1. Cuffs went from 80.6 / 85.2 mm to 56.1 / 55.0, and body through from 230 to 500, mostly trunk (405), at the open front.
- By eye it does better than our own source on layering: the blouse that poked through the cardigan at the shoulders and the waist is pushed under on every body. What it does worse: a ragged edge along the shoulder line, and a patch of bare belly under the lowest button, where the trimmed blouse ends.

## What works
- Driven entirely from job files, with exit codes, a log, a result file with pass/fail per check, and pictures (torso, neck, three poses, source). Same result twice. Under 2 s a job.
- Pose and proportion matching through the skeleton, with an exact point-to-point shape carry between MetaHuman bodies. The sleeves stay on the arms, which is where MetaTailor failed.
- Bands keep their height on a pullover. Skin weights come out capped at 8. Mesh, materials and both UV sets are kept.
- Layers listed inside first; double-walled garments recognised.

## What fails and why (as far as seen)
1. Cardigan cuffs shrink to about two-thirds on Lena C1, Sam C5 and one Heavy cuff, while the jumper's cuffs hold on every body. Unverified cause: the cardigan's Rib also covers the button band, so the band-height rule may be finding the wrong axis or the wrong island.
2. The identity fit is not a no-op. S4 onto S4 doubles body-through (259 to 503) and moves two bands by 7 to 8%. A refit onto the same body should hand back the garment unchanged.
3. Body-through counts body points under an open front, even where the blouse covers them. Lower layers don't count as cover, so open garments fail the bar whatever the fit.
4. The "no lower layer through this one" check passes with 12 to 24 lower-cloth points through. That contradicts its own rule 6.
5. One source body per job, so a blouse made on Lena C1 and a jumper made on Tom can't be layered in one job (we used both already on S4).
6. The Heavy crew band grew to 1.58x its source height.
7. Not yet checked in Unreal: the import, skeleton match and the 90-degree turn its notes report for Darren. That's round 2.
8. Small: the README's first line says the build contains "the original game's own files", which doesn't describe this tool.

## Improvements, most useful first
1. Make a fit onto the source body itself return the garment unchanged. A self-test on every job would catch drift.
2. Band detection that tells cuffs from button bands, e.g. by the opening each band edges, or band names per island in the job.
3. Count body points covered by any lower layer as covered, in body-through and in the test poses.
4. Make rule 6 fail at its stated bar, or state the bar.
5. Allow a per-garment `source_body`.
6. A smoothing pass along the shoulder line of an outer layer, where the collision leaves a ragged edge.
7. An Unreal import self-check (bone names, bind pose), or a written note of which import settings it expects.

## For level 3 (overlap)
Its body and skeleton loader (FBX any axis, MetaHuman exact match), its check suite (the same checks as measure_fit.py), its pictures and its job and result format all overlap with Drape Studio. They are candidates for the shared core.

## Unreached or untested
Unreal import; the packaged game; Pose Match in MetaTailor (still untried, so the comparison is against its defaults); Seamshift's viewer (it needs clicks, so it wasn't used).

## Round 2, 13 November 2026 (05:25 to 05:50): the Unreal import
- Method: tools/ue/seamshift_scratch_import.py in the MetaHuman project (full editor, unattended), the same import settings as the game's garments (import_garments.py), onto each wearer's own body skeleton, into a scratch folder deleted afterwards. A garment and its body each spawned at the origin; every bone's reference-pose position compared; bounds compared. Result file: C:/LedgerTools/mh-assemble/seamshift-scratch.txt; log Saved/Logs/seamshift-scratch.log.
- All three of tom-jumper-to-cast (Sheila S4, Ron P2, Darren S6) import onto the body's own skeleton, 342 of 342 bones shared, bind pose identical (worst 0.001 cm). No turn: each jumper is centred on the body (x -0.1 cm), wider than deep like the body, at chest height (centre 115 to 132 cm). The 90-degree turn its notes report for Darren does not appear in Unreal.
- Small faults: Darren's file carries one extra bone at its root named after his old body (MH_SamC5_Body); Unreal accepts it, but it is a stale name from the source FBX. Every file lacks smoothing groups (Unreal warns; it rebuilds normals itself).
- His updates: none since round 1 (his folder unchanged since 12 Nov 19:37).
- Still unreached: the packaged game (a held scratch garment is not worn in the game), and the cardigan faults, which wait for an update from him.
- Cost: about 0.4 h, no helpers. Time log: "tool test: Seamshift round 2 Unreal import".
