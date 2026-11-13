# Drape Studio, his final version, tested 13 November 2026

Method researched: DRAPESTUDIO-TEST-2026-11-11.md (the same jobs, body files, check scripts and hang heights, repeated unchanged; his final source, tag his-final-2026-11-13, built fresh at 14:49). Asked by advisors 145 and 146. Work folder F:/LedgerTools/drapestudio-test-2026-11-13-final (run_all.ps1, jobs/, checks/, pictures). Jobs run one after another, nothing heavy beside them, so the times are fair. DRAPE_STUDIO_EXE set to the fresh build.

## Verdict
His final version reaches Marvelous's time on the jumper (125 s against 124 s) and is near it on the jacket (147 s against 102 s) and the jeans (173 s against 86 s), and beats Marvelous on cloth through the body on all three. The jumper's cuffs and the jeans' waistband, the two shape faults of 11 Nov, are fixed. The jacket over the jumper now holds the jumper under the jacket nearly everywhere by eye, but took 113 minutes. Still open: the jacket's gripped cuffs crumple at the wrist and its sleeves stretch to about 5.4 times their pattern length (its own check now fails it on that), and layering's time.
Picture: production/previews/drapestudio-final-2026-11-13.jpg (top: jumper, jacket after its cuff grip; bottom: jeans, jacket over jumper; front and side each, its own pictures).

## Times (same jobs, one after another)
| | Marvelous | 11 Nov | 13 Nov final |
|---|---|---|---|
| jumper (j3, 700 steps) | 124 s | 246 s | 125 s |
| jacket with cuff grip (v19, 1,700 steps) | 102 s | 587 s | 147 s |
| jeans (n7) | 86 s | 226 s | 173 s |
| jacket over jumper | not timed | 4,082 s (game build beside it) | 6,795 s (nothing beside it) |
| FreeSewing SVG import | | 0.08 s | under 1 s |

Why faster: a stop-when-still is now in the Python Simulate (the jumper skipped 576 of its steps, the jacket 1,399 of 1,700, the jeans 474), the improvement suggested on 11 Nov.

## Numbers (drape_check_any.py on the job's own plan, bounds.py hang heights)
| | jumper: Marvelous j3 / 11 Nov / 13 Nov | jacket after grip: Marvelous v19 / 11 Nov / 13 Nov | jeans: Marvelous n7 / 11 Nov / 13 Nov |
|---|---|---|---|
| hang height, mm (jumper front; jacket back; jeans right front) | 1,068-1,625 / 1,082-1,626 / 1,075-1,623 | 1,031-1,628 / 1,025-1,629 / 1,023-1,624 | 64-1,085 / 73-1,106 / 74-1,106 |
| jeans waistband, mm | | | 1,066-1,120 / 1,074-1,141 / 1,076-1,141 |
| cloth points over 1 mm inside the body | 74 / 0 / 0 | 100 / 26 / 0 | 101 / 36 / 3 |
| body through the cloth, points over 1 mm | 46 / 45 / 0 | 103 / 158 / 25 (sleeves) | 28 / 52 / 13 (backs) |
| edges over 1.2x their pattern length | 1,416 / 279 / 991 | 1,076 / 891 / 761 | 83 / 216 / 139 |
| worst edge | | 13.1x / 6.05x / 5.47x (left sleeve) | 1.70x / 2.19x / 2.02x |

One step back: the jumper's edges over 1.2x rose from 279 to 991 (Marvelous 1,416), likely the price of stopping when still (not measured). The jumper's check this time read the plan from inside the job (checks/job_run1_plan.json), the same pieces as 11 Nov's pattern file, which the check script could not read today. The jeans' hang and waistband numbers are unchanged from 11 Nov, yet by eye the waistband now lies on the hips: the 11 Nov flare was at its top edge, which the bounding heights do not show. Jacket over jumper: our check counts against the body only and both garments share piece names, so its numbers are not comparable; the picture decides (below).

## Its own check
- Jumper: ok; worst edge 1.88x (limit 3.0 per piece, new), 873 of 43,741 edges over its share limit; no penetration; seam gap 3.5 mm; cuffs dropped 5 and 1 mm from where placed (11 Nov: 98 and 106).
- Jacket: **fails itself** on the new per-piece worst edge: sleeveR 5.22x, sleeveL 5.46x (limit 3.0); seam gap 12.0 mm. On 11 Nov the same sleeves (6.05x) passed on the share rule; the check now catches what our check caught.
- Jeans: ok; worst edge 1.59x; 3 points through by up to 1.6 mm; seam gap 3.9 mm.
- Pattern import: 3 pieces (back, front, sleeve), FreeSewing's marks no longer taken as pieces; names still fs-1 to fs-3; sizes as 11 Nov.
- Fabrics: Marvelous's fabric files still cannot be read (locked format); each result names the preset used.

## By eye (its own front and side pictures)
- Jumper: a jumper, shoulders, chest and sleeves as Marvelous's; the cuffs now end cleanly at the wrists (11 Nov: crumpled rings).
- Jacket: collar, zip line, body and rib hem read as a jacket; the gripped cuffs crumple into a ragged grey lump at the wrist, and the sleeve ends look ragged from the front.
- Jeans: the waistband lies flat on the body (11 Nov: stood off at the hips); legs straight, hems at the shoe.
- Jacket over jumper (layer/grip, after the cuff grip): the jumper stays under the jacket from front and side except a sliver of green at the right armpit and at both cuffs, against shoulders, chest, sleeves and strips down the front on 11 Nov; the jumper's outline presses through the jacket at the chest as creases; the gripped cuff crumples as on the jacket alone. The back was not pictured by the tool.

## Against 11 Nov's list
1. Speed: done on single garments (stop when still); layering 6,795 s against 4,082 s on 11 Nov, slower, likely the cloth-on-cloth contact now working (not measured).
2. Per-piece worst-stretch limit: done (catches the jacket's sleeves).
3. SVG import: marks skipped; names and fold mirroring not done.
4. Denim close to Marvelous's: the waistband now sits; the denim file itself still a preset.
5. Layering: the jumper now stays under the jacket nearly everywhere by eye (fixed in the main); time 113 min.

## What this means for Kiln
Kiln's front end is taken from this version's python/ folder (interface only, never its engine or presets). Its numbers become the bar Kiln's drape engine must meet beside Marvelous: M2 (jumper) is now met by Drape Studio itself on time and on our check; M3 (jacket and jeans) is close but for the jacket's sleeve stretch and cuff crumple; M4 (layer) by eye, but at about 66 times Marvelous's jacket time. The engine work in Kiln therefore targets the layering time first and the jacket's sleeves, with Brief 1's OGC contact and start check. Whether a garment made through Drape Studio may be adopted is his licence question, before any such garment goes in. Cost: about 1 hour of session time; no helpers; no API spend.
