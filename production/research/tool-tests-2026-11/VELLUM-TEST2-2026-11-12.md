# Houdini Vellum test 2: Tom's jumper alone against Marvelous (12 Nov 2026, 02:36 to 03:05 Swiss)

Tool test only; nothing made here enters the game. Plan: PLAN-2026-11-11.md, "Tests and bars" item 2 (and test 3, no clicks, repeats).

**Verdict: falls short of Marvelous on every measured check (body through cloth 230 vs 46 points, cloth inside the body beyond 3 mm 229 vs 54, edges over 1.2x outside seams 1,503 vs 544; the garment hangs 11 to 70 mm higher). It repeats exactly, and runs headless with no clicks. Two tries used; a third needs his yes.**

## What was done

- Houdini 22.0.466 Apprentice, hython only, no window. Job script: `F:/LedgerTools/tool-tests-2026-11/houdini-vellum-test2/vellum_job.py` (`hython vellum_job.py RUN FRAMES`). Everything written goes under that folder (48 MB).
- Input: Marvelous's drape j3 (`F:/LedgerTools/garments/tom/jumper/drape-j3/jumper.obj`, job_j3, 30 Oct). It holds the nine pieces (23,596 cloth points) and the body it was draped on (MH_TomL1_FullBody_LOD0, 51,619 points, the straight-elbow drape pose). The plan comes from `job_j3.plan.json`.
- **The pattern was not read into Houdini from the plan.** I used the fallback the brief allows: Marvelous's own piece meshes, laid flat from their UVs at pattern size, by the same rule drape_check.py uses (tile = the outline's box over the UV box). Rebuilding the plan's curves and seam-edge rules in Houdini would not have fitted in 30 minutes. Vellum cloth constraints were built on the flat layout, so the rest lengths are the pattern's.
- **Seams:** 680 zero-length Vellum distance constraints (stitches), one per pair of open-edge points that lie within 3 mm of each other in Marvelous's drape, across pieces and within a piece (the sleeve underarm, the band rings). So the sewing was read from Marvelous's export, not from the plan's seam list. Unpaired open-edge points were found only at the real openings: welt bottoms (88 + 88), cuff ends (32 + 32) and the neck edge (83).
- **Placement:** each flat piece was wrapped, with lengths kept, onto a cylinder round its body part. The parts are the torso (front, back, welts), the neck (neckband) and each arm (sleeves and cuffs, with the arm axis found from the body's own points). Each piece's angle round its axis, its facing and its height were taken from Marvelous's drape, in effect its arrangement points. The radius is the body's largest radius over the piece's span plus 15 to 25 mm.
- **Solve:** vellumsolver with 5 substeps, 100 iterations, self collision on, the body as a static collider, cloth point radius 2.5 mm, Vellum's default cloth stiffness (stretch 1e10, bend 0.1; no knit or rib fabric values were matched to Marvelous's). Run 1 was 120 frames; runs 2 and 3 were 180 frames at 24 fps. The last frame was written as an OBJ with the drape OBJ's exact layout (same vertices, UVs, groups and body).
- **The check:** the project's check, `F:/LedgerTools/garments/tom/jumper/checks/drape_check.py`, runs only inside Blender, and Blender was not allowed. So I ported it line for line to numpy and scipy: `F:/LedgerTools/tool-tests-2026-11/houdini-vellum-test2/drape_check_np.py`. **It was validated** on the same file Blender checked, `drape-j3/jumper_unposed.obj`: every check total and every piece value equals Blender's `checks/j3/unposed-check.json`. That covers body through cloth 46 (deepest 22.6 mm), cloth inside the body 74 and 54, worst stretch 9.843 on cuffL, inner edges over 1.2x 1,797 and edges over 1.2x outside seams 918, with no piece differing. No project tool measures hang heights, so the port also records each piece's lowest and highest point and the median height of each band's open edge. These are measured the same way on both drapes.
- Marvelous's side of the table is its posed drape (`jumper.obj`), the same pose and body Vellum draped on. The j3 record's own check was run on the unposed drape. Marvelous's drape itself misses the step-3 marks at the sleeves and cuffs; it is the bar here, not a pass.

## Results (all measured; Marvelous j3 posed against Vellum try 2, runs 2 and 3)

| Check | Marvelous j3 | Vellum run 2 | Vellum run 3 |
|---|---|---|---|
| body through cloth >1 mm (points) | 46 | 230 | 230 |
| body through, deepest mm | 22.6 | 24.9 | 24.9 |
| cloth inside body >1 mm | 74 | 276 | 276 |
| cloth inside body >3 mm (the mark: 0) | 54 | 229 | 229 |
| cloth inside, deepest mm | 19.6 | 40.1 | 40.1 |
| edges >1.2x outside seams (the mark: 0) | 544 | 1503 | 1503 |
| inner edges >1.2x (all) | 1416 | 3539 | 3539 |
| worst inner stretch | 9.843 (cuffL) | 8.062 (front) | 8.062 (front) |
| stretch median, front / back | 1.017 / 1.008 | 1.009 / 1.002 | 1.009 / 1.002 |
| stretch median, sleeveR / sleeveL | 1.046 / 1.03 | 1.042 / 1.047 | 1.042 / 1.047 |
| neckband top mm | 1640.5 | 1685.6 | 1685.6 |
| front top / back top mm | 1625.0 / 1624.4 | 1687.5 / 1694.1 | same |
| weltFront / weltBack lowest mm (hem) | 1026.8 / 1001.2 | 1038.0 / 1018.1 | same |
| weltFront / weltBack open edge median mm | 1089.0 / 1047.7 | 1097.3 / 1090.2 | same |
| cuffR / cuffL lowest mm | 1051.7 / 1047.9 | 1069.7 / 1085.2 | same |
| cuffR / cuffL open edge median mm | 1085.5 / 1078.9 | 1098.8 / 1123.9 | same |
| sleeveR / sleeveL lowest mm | 1081.8 / 1076.6 | 1115.3 / 1092.9 | same |
| neckband open edge median mm | 1619.4 | 1645.9 | same |

Where Vellum's faults are: the front's top tenths (the neckline riding up the neck; body through to 24.9 mm at about 1670 mm high) and the sleeves' wrist ends (about 1120 mm high). The welts are near clean in both: 1 and 5 edges over 1.2x for Vellum, 0 for Marvelous, and no cloth inside the body in either. Medians of stretch are alike (within 0.02); the counts over 1.2x are not.

**Repeat (test 3):** runs 2 and 3, the same script and settings, gave identical last frames: all 23,596 points within 0.000 mm, and every check number identical. Vellum on the CPU here is deterministic. Marvelous is not (the game-garment skill, step 3).

**Settling:** over the last five frames the median point moved 0.69 mm and the worst 15.6 mm (run 1: 0.78 and 22.6 mm). The drape is near rest but not fully still at 180 frames.

## Tries, what failed and why

- **Try 1 (run 1, 120 frames):** each piece was centred where Marvelous's piece is centred. A flat piece is taller than the same piece draped, so the neck ends started at the jaw and caught there. Result: body through 209, cloth inside beyond 3 mm 273, edges over 1.2x outside seams 1,477, neckband top 1686.1 mm.
- **Try 2 (runs 2 and 3, 180 frames):** each piece's top end was placed at Marvelous's top end. Little changed (table above): the garment still settles high, with the neckline up the neck.
- Likely causes, **not tested**. (a) No fabric match: Vellum's default near-inextensible cloth against Marvelous's knit and rib, so the stitched shoulders and neckband cannot give the way Marvelous's knit does. (b) The cylinder placement and stiff 1e10 stitches pull the seams closed fast across gaps of up to 232 degrees (the neckband) and leave folds caught at the neck and wrists. (c) No staged settle such as Marvelous's (particle distance 20, then 10, then 5 to 6 mm on bands; Fitting quality last).
- Two tries used. A third (knit and rib values matched, softer stitches ramped over time, staged settle) needs his yes, under the two-tries rule.
- Not done: the jacket-over-jumper half of plan item 2. The jumper alone did not pass first.

## Cost

About 30 minutes of work (02:36 to 03:05 Swiss). Simulation time: 2.2 to 2.5 s per frame on the CPU, so 227 s for run 1 and 338 s and 330 s for runs 2 and 3. One check takes about 20 s. Disk: 48 MB.

## Files (F:/LedgerTools/tool-tests-2026-11/houdini-vellum-test2/)

`vellum_job.py` (the job), `drape_check_np.py` (the check, ported and validated), `compare.py` (the table and the run agreement), `validate_unposed.json` (the port's validation), `check_marvelous_posed.json`, `check_run1.json`, `check_run2.json` and `check_run3.json`, and `run1/`, `run2/`, `run3/`, each holding `jumper_vellum_last.obj` (the last frame), `log.json`, `pairs.json` and the rest and body geometry. The logs are run1.log, run2.log and run3.log.
