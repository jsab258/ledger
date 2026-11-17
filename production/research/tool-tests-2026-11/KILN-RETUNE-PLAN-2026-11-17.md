Method researched: KILN-METHOD-REVIEW-2026-11-16 (step 4), FABRIC-NUMBERS-2026-11-17, Kiln's doc.rs, serve.rs and gate jobs, judge/bars.json, regression_gate.py, Tom's plans, RUBRIC.md, production/reference (read 17 Nov 2026)

# Kiln fabric re-tune after true stiffness: the plan (17 Nov 2026)

Plan only. Reference games: none found for a drape solver (method review); targets are Marvelous's drapes of the same jobs and measured fabric numbers. Bands marked "ours" are unverified.

## 1. Presets and jobs

| Preset | Jobs |
|---|---|
| Low-Gauge Knit | j3; layered (frozen j3) |
| Rib Knit (darren_rib a copy) | j3, jacket, layered, nylon_jacket |
| Cotton Twill (also the fallback) | jacket, layered |
| Stiff Interlining (darren_zip_tape a copy) | jacket, layered, nylon_jacket |
| Denim | jeans |
| ron_trouser_twill | work_trousers |
| ron_melton, ron_melton_collar | donkey_jacket (not made in the baseline) |
| sheila_skirt_flannel, sheila_skirt_band | pleated_skirt (known failing) |
| darren_nylon | nylon_jacket |
| Jersey Knit, Silk Charmeuse | none |

The fabric files say "ESTIMATES ... not measured". First, the two copies become table rows naming their preset: one home per value.

## 2. Targets

**Benches** (Kiln jobs, no person): a 1,000 x 200 mm strip hung by its top (strain under own weight); a cantilever strip (bending length; ASTM D1388 geometry, not read: unverified); a Cusick disc, 300 on 180 mm (not read: unverified). **Garments:** Marvelous's numbers on the same job.

| Preset | Target (source) | Band |
|---|---|---|
| Low-Gauge Knit | Front hang 1,068 / 1,625 mm; front edges over 1.2x at most 63, all 1,416 (bars.json M2, Marvelous j3, 11 Nov). Sleeve folds against drape-j3's export (same run as M2: unverified). Density 420 unsourced (knits 163-213 g/m², FABRIC-NUMBERS) | ±25 mm (M2), aimed ±12 (ours); ±1 fold (ours) |
| Rib Knit | Cuffs 74.6/75.0, welt 76.9/74.6, crew 29.2 mm high (Tom's passed jumper, kiln/MECHANICS.md); cuff edges over 1.2x 0, worst at most 1.518 (pre-slide-fix, method review); band girth at most the body's under it (JUMPER-PLAN) | ±10% (Seamshift's bar); grip ours |
| Cotton Twill | Back hang 1,031 / 1,628; edges at most 1,076; inside 100, through 103 (M3, v19). Density 278 g/m² (BDP fabric 17, read 17 Nov): keep 270. Strip strain under 0.5% | ±25 mm; strain ours (derived from F4's 3% at 490 N/m: about 0.01% if linear) |
| Stiff Interlining | Tape length change under 1%, no fold along it | ours |
| Denim | Right-front hang 64 / 1,085, waistband 1,066 / 1,120; edges 83; inside 101, through 28 (M3, n7). Bending length about 2.0 cm (computed from B 0.273 at 10.38 oz, snippet: unverified). Lower-leg folds against n7's export | ±25 mm; ±1 fold (ours) |
| ron_trouser_twill, sheila_skirt_flannel | Cusick 0.32-0.35; bending length 1.0-1.3 cm (wools F4/F5, PMC8584912, read 17 Nov; lengths computed here, unit unverified). Loose fit: F4/F5 weigh 162-179 g/m², these 280-340. By eye: creases behind the knee, a half break (work-trousers-and-flat-cap-1990.md) | ±0.03 (ours) |
| ron_melton (+collar) | Garment mass (area x density) about 0.98 kg (V&A T.561-1993); length 810-900 mm (Museum Wales); "stiff and boxy, creasing" (all via donkey-jacket-1990.md) | ±15% (ours) |
| darren_nylon | Density 90 within 70-135 (only RGBench's 135 verified); no drape numbers | gate bands |
| sheila_skirt_band | Check only until the fall has a cause | none |
| Jersey, Silk | Bench order only (silk lowest Cusick) | none |

## 3. Order and stops

1. **Benches, step 4's own check:** each bench at 20 and 10 mm particles (rib also 6) and at Normal and Fitting within 10% (ours). If not, step 4 has not landed: no tuning.
2. Denim on jeans (one fabric, one job).
3. Rib Knit: benches, a ring on a cylinder of known girth, then j3's bands.
4. Low-Gauge Knit on j3 (rib fixed).
5. Cotton Twill and Stiff Interlining on the jacket; layered checked.
6. Fabric files: trouser twill, nylon, melton pair (if made), skirt pair (check).
7. Jersey, Silk on benches.
8. Full gate, one new baseline, M2 to M4 re-judged.

**Stop per preset:** inside its bands on every job using it, at both qualities. Otherwise two sweeps of at most six runs, then stop: best values kept, the failed capability reported plainly, no third sweep without his yes.

## 4. Keeping it general

- Values only in fabric data; no job, person or garment named in engine code (src/ searched before each commit).
- After each preset regression_gate.py runs all eight jobs, so a value tuned on one job is judged on every job using it. One new baseline at the end, compared with the fixed old one (the review's drift risk).
- Aim at the band's centre: "a count tuned to a bar lands beside the bar" (method review).
- Sourced densities stay fixed; stiffness is tuned.
- Held-back jobs never opened by the tuner; judged once at the end (bars.json M4, M7).

## 5. Hours (estimates, unverified; machine time extra)

| Piece | Hours |
|---|---|
| Benches, fold-count measure (search tools/ first) | 2-3 |
| Denim | 1.5-2 |
| Rib Knit | 2-3 |
| Low-Gauge Knit | 2-2.5 |
| Cotton Twill, Stiff Interlining | 2-3 |
| Trouser twill, nylon, melton | 3 |
| Skirt pair, Jersey, Silk | 1-1.5 |
| Gate, baseline, M2-M4 | 1.5-2 |
| **Total** | **15-20** |

## Unreached and unverified

- Melton, drill, nylon, rib, jersey measurements: none read. Marvelous's fabrics are encrypted.
- Bench standards, every "ours" band, every hour; whether Kiln accepts a non-human collider (Cusick table).
