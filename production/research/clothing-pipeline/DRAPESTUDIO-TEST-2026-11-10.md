# Drape Studio tested as a Marvelous replacement, 10 November 2026

His ask (advisor 77, steps 2 to 4; his note 11:30 and advisors 81 and 82: his own tool, no licence or contents check). Its files were not changed. Work folder: F:/LedgerTools/drapestudio-test (scripts, results, OBJs, pictures). Picture: production/previews/drapestudio-jumper-2026-11-10.jpg (left Marvelous j3, middle Drape Studio try 1, right try 2).

## Verdict: does not work instead of Marvelous yet; works for part (the job layer)

## The test
- The exact Marvelous job for Tom's jumper (garments/tom/jumper/job_j3.py, 9 pieces, 21 seams, 400 + 200 + 100 steps) run unchanged through Drape Studio's `run_job_script.py`, only the body path (the same MetaHuman FBX the .avt came from) and the output folder changed. Same body, same pattern, same check (garments/tom/jumper/checks/drape_check.py, test copy accepting the group name "Avatar").
- Try 1: default seam directions. Try 2: `DRAPE_SEAM_DIRECTIONS=auto` (its documented setting). Two tries, spent.
- Repeatability: its own example job (examples/tom_tank_test.json) run twice at once: the two OBJs are byte-identical.

## Numbers (same check, same body)
| | Marvelous j3 | Drape Studio try 1 | try 2 |
|---|---|---|---|
| time | 124 s (GPU off, CPU) | 363 s | 373 s |
| where the front panel hangs (height, mm) | 1,068 to 1,625 (chest to neck) | 745 to 1,210 (waist to thigh) | 1,027 to 1,241 (bunched at the waist) |
| cloth vertices more than 1 mm inside the body | 74 | 6,196 | 5,850 |
| deepest, mm | 19.6 | 58.8 | 59.2 |
| body through the cloth, vertices over 1 mm | 46 | 1,698 | 1,284 |
| front panel: edges over 1.2x their pattern length | 63 | 206 | 470 |

By eye: Marvelous gives a jumper; try 1 slid to the hips like a skirt with the sleeves stretched to the arms; try 2 crumpled into a ring round the waist. The body and the cloth line up exactly in both OBJs (the body's bounds match Marvelous's to the millimetre), so this is the drape, not a units or export fault.

## What works (step 2)
1. Runs with no window, on the processor, no account, no network; Python job scripts written for Marvelous run with the same call names (every call in our job was accepted, none unsupported).
2. Reads the MetaHuman FBX directly (1,900 mm, landmarks found); 109 arrangement points.
3. JSON jobs in and out, a file bridge with heartbeat, measures built in (stretch, penetration, seam gaps).
4. The same job gives byte-identical output.
5. OBJ export with welded seams and pattern-proportional UVs; its own project file.

## What is missing or broken (with evidence)
1. The drape does not hold on the shoulders: a sewn jumper slides down the body (both tries, table above). The blocker.
2. Cloth passes through the body by up to 59 mm on 5,850 to 6,196 vertices against Marvelous's 74.
3. About three times slower than Marvelous on the same job (363 s against 124 s); the solver is single-threaded by design.
4. Its own example fails its own checks (seams_closed false, stretch_ok false: seam gap 8.2 mm, stretch 1.64).
5. Marvelous's fabric files are not read; it falls back to a preset by file name without saying so (the result's notes stay empty, also when ExportZPrj writes a .drape instead).
6. No FBX export and no pattern import from DXF or SVG (points only, through the API or JSON); buttons, grading sizes and the pattern cut answer False through the Marvelous names.
7. The runner needs DRAPE_STUDIO_EXE set, otherwise "not found" (the first run failed in 0.04 s).

## What would suit unattended work (improvements)
1. Fix the shoulder hold and body collision first; a built-in check that fails the job when a garment's top edge drops more than a set distance from where it was placed.
2. Report the fabric actually used (file read, preset fallen back to) in the result.
3. Multi-threaded or GPU solving to reach Marvelous's time.
4. The runner finding its own program beside it, with no setting.
5. FBX export with UVs, DXF/SVG pattern import.
6. A picture per job (front and side) written beside the OBJ, so a reviewer sees each drape without Blender.
7. Its own penetration measure in the Python path's result, as the JSON path gives.

Cost: about 35 minutes of session time, no helpers, no API spend.
