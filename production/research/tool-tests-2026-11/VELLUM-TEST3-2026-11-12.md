Method researched: production/research/tool-tests-2026-11/VELLUM-METHOD-2026-11-12.md (SideFX Vellum Drape and garment docs, read 2026-11-12)

# Houdini Vellum test 3: Tom's jumper, the third and last try (12 Nov 2026, 10:24 to about 10:55 Swiss)

This is a tool test only. Nothing made here enters the game. He said yes to this third try at 09:11 today.

**Verdict: the third try falls short of Marvelous on all four pass checks and comes out worse than try 2 (body through cloth 281 points against Marvelous's 46; cloth inside the body beyond 3 mm 277 against 54; edges over 1.2x outside seams 1,988 against 544; the neckline sits 50 to 60 mm high and the right cuff 54 mm high). Vellum, set up this way headless, does not match Marvelous on this jumper, and the jacket was not started.**

## What was done

- Houdini 22.0.466 Apprentice, run through hython only, with no window and no clicks. Everything was written under `F:/LedgerTools/tool-tests-2026-11/houdini-vellum-test3/` (19 MB).
- Same input as try 2: Marvelous drape j3 (the nine pieces and Tom's body in the drape pose), the same flat pattern taken from the UVs, the same 680 seam pairs read from the drape, and the same cylinder placement. Test 2's setup code is reused unchanged; the try-3 code starts at the "TRY 3" line of `vellum_job3.py`.
- **Fabric.** Knit body and rib bands got separate Vellum cloth constraints, with values taken from Marvelous's own fabric files (mapping below).
- **Stitches closed the Drape way, in three stages:**
  1. **Stage 1, the pre-roll (60 frames).** Gravity off. Each seam pair got a soft zero-length attraction spring at stiffness 1000, which is Vellum Drape's default attraction stiffness. 5 substeps and 100 iterations.
  2. **Stage 2, weld and gravity (120 frames).** Every seam point was welded onto one root point with Vellum's Weld Points constraint, Add Bend across Welds on, so the 669 bend constraints across the seams rest at the pre-rolled shape. Gravity was then switched on. 5 substeps; 150 iterations, which is about the garment's diameter in edges; 10 collision passes; 3 post-collision passes (layers plus 2).
  3. **Stage 3, a finer settle (36 frames).** Chained on from stage 2's last frame, the way Freeze at Frame chains Drapes: 10 substeps, 300 iterations, 20 collision passes.
- **Not used.** Inflate Collisions was not used, because no cloth starts inside the body (placement is 15 to 25 mm out). Marvelous's coarse-to-fine particle steps (20, then 10, then 6 mm on the bands) cannot be copied, because Vellum runs on the one fixed mesh. The rising substeps and iterations stand in for them.
- **One false start in the same try.** Run 4 was stopped after stage 1. With seams still open up to 146 mm, Vellum's closest-point weld picked the wrong root for 323 points. Run 5 snaps each welded point onto its own root at the weld, which is what the Drape weld stage does in effect. All 680 welds then landed correctly (0 wrong). The table below is run 5.

## Fabric mapping (Marvelous to Vellum)

The values were read from the two library fabrics job_j3 assigned. They are binary .zfab files, decoded read-only in memory.

| | Marvelous knit (LowGaugeKnit_1) | Marvelous rib (Rib_1) | Vellum knit | Vellum rib |
|---|---|---|---|---|
| stretch weft / warp / shear | 14,236 / 17,368 / 5,987 | 18,794 / 15,373 / 8,546 | 1e5 | 1.08e5 |
| bend weft / warp (v2 fields) | 937 / 4,949 | 197 / 3,227 | 0.1 | 0.058 |
| density | 0.000268 g/mm² | 0.000140 g/mm² | 0.268 kg/m² | 0.140 kg/m² |
| friction / thickness | 0.03 / 0.5 | 0.03 / 0.5 | friction scale 1 | friction scale 2 (grip) |

- **Density** is the same physical quantity in both tools, so it was copied directly.
- **Stretch: calibrated by a strip test** (`strip_cal.py`, `strip_cal.json`). A 60 x 595 mm strip of the knit (body length, 10 mm spacing, the knit's density) hung from its top edge. Strain under its own weight, by stiffness: 1e10 gave 0.99 %, 1e5 gave 1.87 %, 1e4 gave 4.3 %. 3e3, 1e3 and 3e2 gave 53 %, 7.9 % and 241 %; those strips were still swinging at frame 72, so those rows are not reliable. The knit was set to 1e5, because its 1.9 % is nearest Marvelous's front stretch median of 1.7 %. The result fits: try 3's front median is 1.015 against Marvelous's 1.017. The rib was set to the knit times 1.08, Marvelous's rib-to-knit ratio (weft plus warp).
- **Bend: only the ratio is matched.** The rib was set to 0.58 times the knit, Marvelous's ratio. The knit stays at Vellum's cloth default of 0.1. The absolute bend level was not calibrated, because there was no Marvelous-side bend measurement to match without running Marvelous.
- **Warp/weft anisotropy** (about 20 % in Marvelous) was not set. Each fabric uses the average of the two.
- The **friction attribute** was set (rib doubled). Its effect was not measured separately.

## Results (all measured with the validated numpy check from test 2)

| Check | Marvelous j3 | Vellum try 2 (run 2) | Vellum try 3 (run 5) |
|---|---|---|---|
| **body through cloth >1 mm (points)** | **46** | 230 | **281** |
| body through, deepest mm | 22.6 | 24.9 | 25.0 |
| cloth inside body >1 mm | 74 | 276 | 333 |
| **cloth inside body >3 mm (the mark: 0)** | **54** | 229 | **277** |
| cloth inside, deepest mm | 19.6 | 40.1 | 39.1 |
| **edges >1.2x outside seams (the mark: 0)** | **544** | 1503 | **1988** |
| inner edges >1.2x (all) | 1416 | 3539 | 3985 |
| worst inner stretch | 9.843 (cuffL) | 8.062 (front) | 8.986 (neckband) |
| stretch median, front / back | 1.017 / 1.008 | 1.009 / 1.002 | 1.015 / 1.006 |
| stretch median, sleeveR / sleeveL | 1.046 / 1.03 | 1.042 / 1.047 | 1.014 / 1.068 |
| neckband top mm | 1640.5 | 1685.6 | 1698.1 |
| front top / back top mm | 1625.0 / 1624.4 | 1687.5 / 1694.1 | 1690.3 / 1676.7 |
| weltFront / weltBack lowest mm (hem) | 1026.8 / 1001.2 | 1038.0 / 1018.1 | 1033.0 / 1006.7 |
| weltFront / weltBack open edge median mm | 1089.0 / 1047.7 | 1097.3 / 1090.2 | 1081.4 / 1072.4 |
| cuffR / cuffL lowest mm | 1051.7 / 1047.9 | 1069.7 / 1085.2 | 1106.2 / 1039.0 |
| cuffR / cuffL open edge median mm | 1085.5 / 1078.9 | 1098.8 / 1123.9 | 1165.6 / 1073.0 |
| sleeveR / sleeveL lowest mm | 1081.8 / 1076.6 | 1115.3 / 1092.9 | 1160.9 / 1083.3 |
| neckband open edge median mm | 1619.4 | 1645.9 | 1655.2 |

**Pass check by pass check:**

- Body through cloth: fails (281 against 46).
- Cloth inside the body beyond 3 mm: fails (277 against 54).
- Edges over 1.2x outside seams: fails (1,988 against 544).
- Hang heights within about 10 mm: fail at the neck and the right arm.
  - Neckband open edge: 36 mm high. Front top: 65 mm high.
  - Right cuff open edge: 80 mm high. Right sleeve: 79 mm high.
  - These rows came within 10 mm: hems (6 and 5 mm), front welt edge (8 mm lower), left cuff (6 mm lower), left sleeve (7 mm).
  - Back welt edge: 25 mm high.
  - Left cuff's lowest point: 9 mm lower than Marvelous.

**Where the faults sit.** By edges over 1.2x outside seams, per piece:

| Piece | Try 3 | Try 2 | Marvelous |
|---|---|---|---|
| sleeveL | 894 | 342 | 123 |
| front | 517 | 608 | 40 |
| back | 466 | 221 | 0 |
| sleeveR | 96 | 268 | 143 |
| cuffs | 3 each | 28 and 30 | 103 and 135 |

The cuffs and welts are now cleaner than Marvelous's. Most cloth inside the body beyond 3 mm is in the neckband (78), sleeveR (63), sleeveL (56) and back (46).

## Settling

| Stage | Median move, last five frames | Worst point | 99th percentile |
|---|---|---|---|
| Stage 1 end (gravity off) | 0.38 mm | 34.8 mm | 21.8 mm |
| Stage 2 end | 0.23 mm | 44.2 mm | 24.6 mm |
| Stage 3 end, the result | **0.23 mm** | **22.9 mm** | 18.5 mm |

Most of the garment is still, but a small number of points keep moving up to 23 mm, where cloth is caught. Try 2 had 0.69 mm median and 15.6 mm worst.

## What failed and why

- **The attraction pre-roll did not close the seams.** After 40 frames the gaps were 8.1 mm median, 94 mm at the 95th percentile and 146 mm worst. After 60 frames they were 8.5, 94 and 146 mm: no further closing. So the soft springs stalled. The weld then had to close gaps of up to 146 mm at once, which is the sudden pull the SideFX page warns can push fabric through the body.
- **The likely reason (not tested further):** the cylinder placement wraps the sleeves about 250° and the neckband about 230° round their parts. Their seam halves sit on opposite sides of an arm or the neck, so the body collider stands between them and the springs cannot pull them through. SideFX's own advice is to make panels larger, or place them so seams meet without crossing the body. That would need a different placement (Marvelous-style arrangement points with the seams facing outward, or pieces starting from Marvelous's own draped shape), which is a new method, not a fix inside this try.
- **The fabric match did what it could measure:** front and back stretch medians now sit within 0.002 to 0.003 of Marvelous's, and the cuffs and welts are clean. It did not touch the collision tangles at the neck, the shoulders and the left sleeve, which are what decide the four checks.
- **Not done:** warp/weft anisotropy; an absolute bend calibration against Marvelous; a repeat run (try 2 already showed Vellum on this CPU repeats exactly). The jacket was not started, by the brief.
- This was the third and last try under the two-tries rule plus his yes. No fourth is proposed here.

## Cost

| Item | Time |
|---|---|
| Work (10:24 to about 10:55 Swiss) | about 30 minutes |
| Stage 1 | 2.5 s per frame (150 s) |
| Stage 2 | 2.1 s per frame (254 s) |
| Stage 3 | 7.4 s per frame (267 s) |
| Run 5 in total | 681 s |
| Run 4 (stopped after stage 1) | about 1.5 min |
| Strip calibration and probes | about 4 min |

Disk: 19 MB. Nothing is left running.

## Files (F:/LedgerTools/tool-tests-2026-11/houdini-vellum-test3/)

- `vellum_job3.py`: the job. Run as `hython vellum_job3.py RUN 0 S1 S2 S3`; run 5 was `run5 0 60 120 36`.
- `strip_cal.py` and `strip_cal.json`: the stretch calibration.
- `drape_check_np.py`: test 2's validated check, unchanged.
- `compare.py`: the table. Its run-agreement step needs both runs in this folder, so it errors after the table for run 2; that does not change the table.
- `check_marvelous_posed.json`, `check_run2.json` (copied from test 2) and `check_run5.json`.
- `run5/`: the last frame `jumper_vellum_last.obj`, `log.json` (fabric, stages, welds, settling), `pairs.json`, the stage-1 and stage-2 frames (`*_mm.npy`), and the rest and body geometry.
- Logs: `run5.log`, `run4-stopped.log`.
- Probes: `probe3.py`, `probe4.py`, `probe5.py` (node parameters, weld and bend behaviour).
