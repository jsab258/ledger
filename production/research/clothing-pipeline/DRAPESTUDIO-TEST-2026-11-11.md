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

# Tom's zip jacket and jeans, layering and a pattern import (advisor 100, 11 November, 13:22 on)

His pick (12:45): Tom's other garments through the updated build, his own tool, no checks of it. Same method as the jumper: Marvelous's own jobs (zip_jacket.py drape v19, jeans.py drape n7) through run_job_script.py, only the output folder and the body file changed (Drape Studio reads FBX, not Marvelous's .avt: the jacket on MH_TomL1_straight.fbx, the jeans on the same proxy body Marvelous used, n6/body/MH_TomL1_straight_proxy.fbx). Default seam directions; DRAPE_STUDIO_EXE unset; runs one after another for fair times. Same check (drape_check_any.py, the job's own plan), same hang heights (bounds.py). Work folder F:/LedgerTools/drapestudio-test-2026-11-11 (jacket/, jeans/, layer/, import/, pics/). Pictures: production/previews/drapestudio-jacket-2026-11-11.jpg and drapestudio-jeans-2026-11-11.jpg (left Marvelous, right Drape Studio; the picture script frames hips up, so the jeans' hems are out of frame).

## Verdict: the jacket drapes as well as Marvelous on our checks but takes 5.8 times as long; the jeans come out usable but sit about 2 cm high with the waistband standing off at the sides, in 2.6 times the time. The pattern import is exact in size but drags in FreeSewing's marks as pieces and loses the names.

## Numbers (same check, same body; the jacket after its cuff grip, as Marvelous's shipped drape)
| | Jacket, Marvelous v19 | Jacket, Drape Studio | Jeans, Marvelous n7 | Jeans, Drape Studio |
|---|---|---|---|---|
| time | 102 s | 587 s | 86 s | 226 s |
| hang height (jacket: back; jeans: right front), mm | 1,031 to 1,628 | 1,025 to 1,629 | 64 to 1,085 | 73 to 1,106 |
| waistband (jeans), mm | | | 1,066 to 1,120 | 1,074 to 1,141 |
| cloth points over 1 mm inside the body | 100 | 26 | 101 | 36 |
| body through the cloth, points over 1 mm | 103 (back 44, cuffs 31) | 158 (sleeves 142) | 28 | 52 (backs) |
| edges over 1.2x their pattern length | 1,076 | 891 | 83 | 216 |
| worst edge | 13.1x (right cuff) | 6.05x (left sleeve) | 1.70x | 2.19x |
| its own check | none | ok (604 edges over; seam gap 12.3 mm; 26 points through) | none | ok (45 points through; seam gap 5.6 mm; worst piece drop 73 mm) |

By eye: the jacket is a jacket: collar standing, shoulders, sleeves and the rib hem sit as Marvelous's do, the zip line straight down the front; Marvelous's own drape shows more folds at the hem band. Body through the cloth moved from the back and cuffs (Marvelous) to the upper sleeves (Drape Studio): the arm pokes through the sleeve near the armpit. The jeans: the waistband rides about 2 cm higher than Marvelous's and its top edge stands off the body at the hips; the seat and crotch read as jeans; slightly more stretch at the back.

## Layering (the jacket over the jumper)
**Verdict: fails.** job_layer.py (the jumper's run1 drape opened, its 9 pieces frozen, the jacket made, sewn and draped over it, then the cuff grip) ran to the end with every call answered, in **4,082 s (68 min)** against 587 s for the jacket alone on the body (about 7 times as long); Marvelous was not timed on this layering job today (not measured). The machine was also building the game for part of the run, so the time is an upper bound.
- By eye (production/previews/drapestudio-layer-2026-11-11.jpg, Drape Studio's own front and side pictures, the jumper drawn green): the jumper comes through the jacket over both shoulders, the upper chest, both sleeves and in strips down the front; the jacket's hem band crumples at the sides.
- Numbers (drape_check_any.py, the result split by piece order into the jumper and the jacket, since both garments name pieces back, sleeveR, sleeveL, cuffR and cuffL): the frozen jumper keeps its own drape (45 body points through, the sleeves; worst edge 6.1x); the jacket against the body alone 95 points through (sleeves 84), 20 cloth points inside the body, worst edge 5.8x, 1,827 edges over 1.2x. Jacket against the jumper used as the body: 2,006 jumper points through the jacket and 3,015 jacket points under the jumper's surface; this count trusts the jumper's face direction, which a garment mesh does not guarantee, so it is supporting evidence only; the picture decides.
- Why (likely, not measured): cloth-on-cloth contact against frozen cloth is either off or too thin at this particle size, so the jacket settles to the body's depth and the jumper shows through; the time grows with the contact pairs.
- Improvement for its maker: cloth-to-frozen-cloth collision with its own thickness (Marvelous's layer and thickness settings), and a check of one garment against another as the third mark beside body-through and stretch.

## Pattern import (FreeSewing's Brian at Tom's measures as FreeSewing's own SVG, ImportSVG)
- 14 pieces came in, in 0.08 s. Three are the pattern (fs-1 back, fs-2 front, fs-3 sleeve); the other 11 are FreeSewing's mark symbols (buttons, notches, a logo, 2 to 24 mm) taken as closed outlines.
- Sizes exact: back 307.3 x 628.4 mm, perimeter 1,828.4 against FreeSewing's 1,828.8; front 1,814.2 against 1,814.4; sleeve 430.9 x 611.5 mm, 1,798.2 against 1,798.3.
- Corners: back 7 lines, front 6, sleeve 4, so seams can be sewn between them; the part names are lost (fs-1...), and FreeSewing draws back and front as halves on the fold, so a whole piece needs mirroring by hand.

## What works, what fails and why
- Works: unattended runs of two more Marvelous jobs, unchanged but for the folder and body file; every call our jobs use answered (no unsupported call); the jacket's cuff grip (freeze, shrink, re-settle) runs; pictures and pass/fail beside each drape; a sized pattern straight from FreeSewing.
- Fails: time (5.8x on the 1,700-step jacket, 2.6x on the jeans; the jumper was 2.0x): it grows with steps and particles; the jacket's upper sleeves let the arm through (its own check passes it on its share rule); the jeans' waistband sits high and flares (Marvelous's denim file is locked, so its Denim preset is stiffer or lighter than Marvelous's denim: likely, not measured); SVG marks imported as pieces.

## Improvement suggestions for unattended work
1. Speed on long jobs: the jacket's 1,000-step settle dominates; a stop when still (its JSON jobs have until_still) in the Python Simulate would cut it.
2. A per-piece worst-stretch and worst-penetration limit, not only shares, so the sleeves' arm-through and the jumper's cuffs fail the check.
3. SVG import: skip anything inside <defs> or <use> and anything under about 30 mm; keep FreeSewing's part ids (data-part or the group's id) as names; an option to mirror a piece on its fold line.
4. A denim fabric close to Marvelous's (a .drape-fabric.json from Marvelous's stated values) and a waistband elastic hint.
