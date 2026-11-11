# Drape Studio retested after its update, 11 November 2026

His ask (advisor 94, 10:26): the 10 November test repeated exactly on the updated build; his own tool, no licence or contents check. Its files were not changed. Work folder: F:/LedgerTools/drapestudio-test-2026-11-11 (job copies, results, OBJs, checks, pictures, FBX). Picture: production/previews/drapestudio-jumper-2026-11-11.jpg (left Marvelous j3, middle run 1, right run 2).

## Verdict: run 1 now drapes Tom's jumper as well as Marvelous on every measure we check except time (about 2x slower) and the cuffs, which bunch at the wrists. It can do the jumper's drape step. Default seam directions only; "auto" still breaks the waistband.

## The test
- The same job as yesterday (garments/tom/jumper/job_j3.py through F:/LedgerTools/drapestudio-test/job_j3_ds.py: 9 pieces, 21 seams, 400 + 200 + 100 steps), only the output folder changed. Same body (MH_TomL1_straight.fbx), same check (drape_check_any.py, run on the plan inside the job). Runs one after another so the times are fair. DRAPE_STUDIO_EXE was left unset on purpose.
- Run 1: default seam directions. Run 2: DRAPE_SEAM_DIRECTIONS=auto. Repeatability: its example job run twice, and run 1 run a second time (run 1b).
- The update's notes name no new recommended setting for sewn garments, so there was no extra run.

## Numbers (same check, same body)
| | Marvelous j3 | 10 Nov try 1 | 10 Nov try 2 | 11 Nov run 1 | 11 Nov run 2 (auto) |
|---|---|---|---|---|---|
| time | 124 s | 363 s | 373 s | 246 s (run 1b 241 s) | 250 s |
| where the front panel hangs (height, mm) | 1,068 to 1,625 | 745 to 1,210 | 1,027 to 1,241 | 1,082 to 1,626 | 1,186 to 1,656 |
| cloth points over 1 mm inside the body | 74 | 6,196* | 5,850* | 0 | 0 |
| body through the cloth, points over 1 mm | 46 | 1,698* | 1,284* | 45 | 0 |
| front panel: edges over 1.2x their pattern length | 63 | 206 | 470 | 50 | 1,354 |
| whole garment: edges over 1.2x | 1,416 | 1,258 | 2,463 | 279 | 4,596 |
| its own check | none | none | none | ok (326 of 43,741 edges over its limit; worst 6.06, in the sleeves) | failed (seam gap 29.6 mm; 5,136 edges over) |

*Yesterday's two body counts were partly our misreading: the old build wrote the body's faces with relative numbers, which our check read as wrong triangles (the update's notes; the hang heights came from the garment, which was written normally, and the slide was real by eye). Today's body is written with ordinary numbers.

By eye: run 1 is a jumper: shoulders, chest and sleeves sit like Marvelous's; its body hangs a little straighter and shorter, and both cuffs bunch into crumpled rings at the wrists (cuffs dropped 98 and 106 mm from where they were placed). Run 2 sits on the shoulders but the waistband folds up into a ragged ring at the waist and the neck stands tall.

## What changed in the new build (its own notes, AUTOMATION.md, Cargo version still 0.1.0, program dated 11 Nov 09:47)
Torso pieces placed on an ellipse round the body at the right height; the body written with ordinary face numbers; the runner finds its program; notes kept and fabric fallbacks named; checks (stretch, penetration, seam gap, drop of each piece's top) in every Python result; front and side pictures beside every OBJ; a body-distance command; checks judged on the share of edges affected; its example widened 15% for Tom; each piece solved on its own core; FBX export; DXF and SVG pattern import.

## Yesterday's seven faults
1. Slides down the body: **fixed** (front 1,082 to 1,626 against Marvelous 1,068 to 1,625).
2. Cloth through the body: **fixed** (0 against 74; body through 45 against 46). Part of yesterday's number was our check misreading its body file.
3. Three times slower: **partly** (246 s against 363 s; Marvelous 124 s, so 2.0x).
4. Its example failed its own checks: **fixed** (both repeat runs pass: stretch, seams, penetration). Its checks now pass while at most 1% of edges are past the limit, and the example was widened, so the bar moved as well as the result.
5. Marvelous fabric files not read, silently: **partly** (still not read, the format is locked; the result now names the preset used: Jersey Knit and Rib Knit).
6. No FBX export, no DXF/SVG import: **FBX fixed** (run 1's project exported in 0.3 s; Blender opens a Garment of 14,447 points with a UV layer and the body at 1,899 mm, lined up 1,003 to 1,644 mm). DXF/SVG import: in its notes, **not tested** here. Buttons and sizes still answer False through Marvelous's names, by design, with its own calls instead.
7. Needed DRAPE_STUDIO_EXE: **fixed** (all runs without it).

## Yesterday's seven improvements
1. Shoulder hold and a drop check: **done** (drop_ok in every result; run 2 marked checksFailed).
2. Fabric used reported: **done** (as note 5).
3. Multi-threaded or GPU solving: **partly** (pieces on their own cores; seams and collisions still in turn; 2x Marvelous).
4. Runner finds its program: **done**.
5. FBX export, DXF/SVG import: **done** (FBX checked; import untested).
6. A picture per job: **done** (front and side, 900 x 1200, beside each OBJ).
7. Penetration in the Python result: **done** (penetration_max_mm, penetration_over_1mm, ok).

## What is still missing or broken
1. Cuffs bunch at the wrists while its check says ok: a share-based limit lets a few sleeve edges at 6x pass. A worst-edge limit per piece would catch it.
2. Seam directions "auto" folds the waistband (run 2): leave it off.
3. About twice Marvelous's time.
4. Marvelous fabrics need a hand-written .drape-fabric.json per fabric.

## Repeatability
The example job twice: byte-identical OBJs. The jumper twice (run 1, run 1b): byte-identical OBJs, now with the solving spread over cores.

## For unattended work
It now runs the whole jumper job unattended with no setting, writes its own pictures and a pass/fail, and exports FBX. Next useful: a per-piece worst-stretch limit in the check, and the cuff fix. Whether it replaces Marvelous for other garments (jacket, jeans) is not tested; one garment passing is one sample.

Cost: about 25 minutes of session time and one small helper-free FBX check; no API spend.
