# Review: NIGHT-GAPS-2026-10-29 (29 October 2026)

**Verdict: FAIL.** Sections 1 to 3 hold, with two corrections (faults 1 and 2). The recommendation does not. Its premise is false (4) and its prediction does not reproduce (5). It ignores a ruling and three fixes that had passed (6), and check 2 cannot be measured as written (7).

**Confirmed:**
- Every near-black share. The 84% and 62% frames are 1,280 × 720, not 2,560 × 1,440.
- The look and scene values; the lamps at x 8 east, 18 west, 28 east, 38 west, 2.97 m off the centre line.
- In the engine source: lumens converted on the outer cone (261 cd both ways), zero light at the outer cone, the window's 27% and 8%, extended range off by default and unset.
- Mafia's preset medians, Kingdom Come II's counts, Epic's six pages, the patent's angles.

**Geometry:**
- A 46° cone ends 4.92 m out, at 4.755 m above the footway.
- So 10.2 m (kerb edge) to 11.2 m (house side) of each footway is unlit; the lamp across the road is 6.1 m or more away.
- A 60/75° cone ends at 17.8 m and reaches the gap.

## Faults

1. **"Berlin's overcast sky … 1.4 and 0.43 mcd/m²."**
   - Kyba: those are the rural site, 32 km out; the urban site read 26 and 2.4.
   - Correction: about 0.08 lux from a town's overcast sky. The conclusion stands.

2. **"About 8 to 1"; "cut off by 75° (semi-cut-off)."**
   - The patent's nadir is at most 80% of the peak, so at most 6.4 to 1.
   - A semi-cut-off beam reaches 75° but may throw 75 cd/klm at 90°: not a cut-off.
   - The lantern peaks at 60 to 65°, where the spot gives 0.49.
   - Correction: the spot is not the period lantern's shape.

3. **Mafia's lamp, "(R; 39 lamps)."**
   - In Study 5's extract the full set is on 20 of 39 lamps.
   - The inner cone is blank (engine default 0°), so Mafia's pool fades from the axis.
   - Correction: the 60° inner cone has no source; mark it (I).

4. **"The pool beneath is unchanged."**
   - Only true within 22°. With the squared falloff, new light against old:

     | Angle | 30° | 35° | 40° | 44° |
     |---|---|---|---|---|
     | New ÷ old | ×1.8 | ×3.5 | ×10.6 | ×89 |

   - Mickey's flags, sill (37°) and fascia (44°) would get several times what the cut of 8 October removed.
   - Correction: predict the rise. Measure with pool_clip.py on the hook camera's night frame (its boxes fit that camera only); add the legs (8 to 10%) and the shopfronts (12%, 3 October).

5. **"Mid-gap about 1.8 lux against about 11 beneath, about 6 to 1."**
   - Recomputed (scratchpad gaps_review.py): beneath, 11.6 lux.
   - The footway gap at x 18: 2.7 lux, about **4.2 to 1**. The lamp across the road (1.9 lux) was omitted.
   - From the chart's 28 October place: 3.1 to 3.3 to 1, under 4.
   - The road's centre: 5.7 to 7.6 lux from x 8 to 38, **1.3 to 1**.
   - The house front behind each lamp, 3 to 3.5 m up: 0 → 25 to 35 lux.

6. **The ruling and the history: missing.**
   - RULINGS, 1 October: "pools of lamp light with darkness between … not one orange wash".
   - That day a 70° pool lit the fronts and left no dark, so it was narrowed to 42° "as Jafar asked". 75° (and the 70° fallback) return to it.
   - Correction: cite both, check the road and fronts, show his page first, and ask him before moving the ruling.

7. **Check 2, C4.**
   - The calibrator stands upright facing the camera (CrimeProbe.cpp), not on the pavement.
   - At x 18 it reads about 100 to 1 whatever the pavement; at x 13 about 1.5. "The next" could be either.
   - No tool gives linear values (measure_night_pools.py: "not scene light").
   - Correction: x 9.8 and x 18, a flat chart or the pavement, and the linear method named.

8. **Check 1, "≤ 50%."**
   - The near wall, a third of the frame, stays 100% near black (only the moon lit it).
   - So the rest must fall under 25%, and the moon's 39% is no like-for-like target.
   - Correction: measure what the lamps reach.

9. **No rule when both fail** (near black above 50% and the ratio under 4).
   - The two remedies pull opposite ways.
   - Correction: make try 2 the patent-shaped light profile (IES), named by Study 5's item 03, Mafia's StreetPole profile and the 21 October column note. The fog ignores profiles.

10. **Column glare, "lit in either cone."**
    - At 1 m under the lantern the column sits at 38°: ×6 the light, lit to 0.2 m below.
    - Correction: predict it, and check lamp post C's close view.

11. **Unverified list incomplete:** add faults 3 to 8 and the fog a 75° cone lights.

## Measured since (05:51)

- Try 1's exact frame (ed-night-cone6075.png; editor built after the switch).
- Near black **61.8%**: check 1 fails. The near wall is still 100%.
- Red at 250 or more in the bottom half: 0.00% → 1.75%, a hot spot on the near pavement.

## Cost and what was not reached

- **Cost:** plausible. The switch is already staged; add his page and the hook camera's frame.
- **Epic nits:** IES sets shape alone only with Use IES Brightness off; the 120 ms is RecaptureSky().
- **Not reached:** BS 5489-3, the White Rose paper, Mafia's Blueprint inner cone and multiplier, any real photograph.
