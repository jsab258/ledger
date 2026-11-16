# Fresh review: street budget and scale test method note (n16-3), 16 November 2026

Reviewer: a fresh helper, files only, read 16 Nov 2026. Nothing run.

**Verdict: pass with fixes.** Most cited numbers match their sources. As written, though, the method would read low on memory and night cost, and its walk never reaches the copies. Fixes 1 to 6 are needed before step 1.

**Confirmed against source:** RULINGS line 63; PLAN line 41 (0/5/10/20) and line 46 (16.7, p99 25, 2.5/1.4 ms); perf-hook.py line 24 (14.0) and lines 25-35; slice-perf.py lines 15-19 and 37 (5,650); EXIT-D line 25-26 (0.19 to 0.27 ms); studies/12 lines 9, 25-26, 40, 49, 54, 56, 81, 82; studies/04 lines 28, 30, 50, 57, target 5; MEMORY-PLAN sections 1-5; MEMORY-WHERE lines 116-127 and 160; PIECES-DRAFT lines 26, 28, 37; atlas line 2009; vignette-scene lines 788-827; CrimeProbe lines 5338, 5353, 5356, 5430; workflow line 2133 (50%). orders/2026-11-09.md line 49 gives d4a070b: 4,965 steady, 5,323 peak, about 95 MB over a budget of 4,861 to 4,879, 17.05/14.99 ms. ue-perf-verdict.txt gives 5,395/5,023/17.29/15.18. All of these columns are in the 9ffd652 CSV header.

## Findings and fixes

1. **The walk never reaches the copies.** The walk stops at 45 m (CrimeProbe line 5435) and starts at x -3 (cam_hook), so it stays inside the 48 m built street. The note says "the hill and walk views catch that", which is wrong. Fix: add `-PerfHookWalkM=<m>` and a route along the copies' road line, or start the walk at the first copy's join.

2. **The copies leave out lights, and the light count is taken once.** `-ScaleTest` copies only static meshes, so lamps and window lights are not copied. The night view and the shadow-light budget therefore stay flat as N grows. The light count is also logged once, at the start of capture (lines 5413-5430), not per frame. Fix: copy each piece's lights with it. Log the count again at the walk's end, and at N=10 on every view.

3. **Shared copies read low (risk (a)).** The largest holder is the run-time pictures, 1,952 MB (MEMORY-WHERE line 144). The copies would share them, and the "88% kit" add-on misuses studies/04 line 28: that figure is placements in a 100-building group, not a share of unique fronts. Cheap fix: each copy decodes its own shop-room pictures and gives its fronts the textures of a different built unit (k mod 8). Unique memory then grows per copy at no art cost. Count one-off fronts from the Hook's planned piece list (studies/04 target 4: shops and Mickey's are the one-offs), not 12%. Also build the copies the same way the rough street will be built (instanced or per actor), or measure both at N=4.

4. **No measure for the 3 ms people budget, and the label is wrong.** The CSV has `Exclusive/GameThread/Animation`, `Exclusive/GameThread/CharacterMovement` and `AnimationParallelEvaluation/TotalTaskTime`. Add them to section 2 and perf-hook.py. "The lower, for 60 fps" is Kingdom Come II's 2.5 ms (studies/12 line 54), not 3. Mafia's 3 ms covers animation only (line 49). Fix: either animation ≤ 3 ms and people update ≤ 2.5 ms, or one 3 ms line marked as this note's choice.

5. **The baseline already fails, so the pass rule cannot steer.** At N=1 the GPU is 13.79 ms at High (0.19 ms spare, EXIT-D line 25) and 14.99 to 15.18 ms on the build machine. The frame is 17.05 to 17.29 ms, and steady memory is about 95 MB over budget. So N=10 will almost surely fail, and "the 1-copy budget less the measured growth" can come out negative. Fix: make the main deliverable the cost per copy and per person (ms and MB, with slopes). Judge growth separately from absolute headroom, and name the levers for each gap: draw size, Mafia's 40-83% dynamic resolution (studies/12 line 17), and freezing people.

6. **Scatter.** Each point is one capture, but launch peaks spread 6,086 to 6,224 MB over eight launches (MEMORY-PLAN line 8). Fix: three launches at N=1 and N=10 on hook and walk (about 12 more captures), and fit the slope across the whole ladder.

7. **The steady line moves.** LocalBudgetMB has read 9,427, 7,128, 5,771 and about 4,870 (MEMORY-PLAN section 6), and an open Marvelous or Kiln lowers it. Fix: run steps 4-5 with no other program holding the card. Log the budget column, but judge against a fixed 4,870 MB line. State that this line is stricter than the ruling's 6 GB, and say where it comes from (n09-3, 12 Nov).

8. **Percentile.** perf-hook's "slowest 1%" is the mean of the worst 1%, not the p99 (EXIT-D line 29: 23.86 against 20.59). Fix: judge the 25 ms target on the true p99.

9. **Hours.** 22 h at the note's own 2-4x record factor (PIECES-DRAFT line 26) comes to 44-88 h, more than n16-3's 40 h. MEMORY-PLAN gives 2-4 days for the test alone. The card time is also low: each invocation waits up to 240 s for voice warm-up (p1-packaged lines 57-58) and up to 120 s for shaders (CrimeProbe line 5389), and every N needs its own invocation. Fix: about 4 h of card. State the rough street's hours left after the multiplier, or cap the test and say what is cut.

10. **How the extra views run.** p1-packaged's matrix has only day-stand, night-stand and day-walk (lines 86-91). Fix: state that the reverse, hill and office views run as `-Only day-stand -GameArgs -PerfHookCam=<id> -Tag <view>`.

11. **Owner-dump acceptance.** The dump gave 4,583 MB not transient plus 3,698 MB of heap bookkeeping, against a 6,152 MB peak, and about 1,064 MB sat in no column (MEMORY-WHERE lines 109, 140). "Within 10%" may fail by design. Fix: name which totals are summed, and accept a stated gap with its reason.

12. **Office camera.** camera.json line 44 is a follow arm, not a fixed camera. PerfHook reads only vignette-scene's `cameras` list (line 5333). Fix: add a fixed cam_office there. cam_mickeys (line 803) is outside the window and does not stand in for it.

13. **Authority.** PLAN line 56 stops "town multiplication, whole-street parameter sweeps" for the builder. Fix: the DECISIONS entry cites n16-3's adopted text (his tap) as the basis, as well as MEMORY-PLAN section 5.

14. **Small corrections.**
    - The column is `LevelStreaming/NumLevelsLoading`, and it means nothing without World Partition.
    - The draw-distance row cannot be measured in this test; mark it "not tested".
    - "Would pass the budget" should read "would carry the total past 5,771 MB (MEMORY-PLAN line 18)".
    - The build machine's level is Highest (nightly 2026-11-13.json line 132), not "no picture level".
    - Mafia's 8 m plot is studies/04 line 14.
    - State the stand-ins' hair type, and use strand-haired cast bodies for the 8.
    - PLAN line 46 asks for a wet night; say whether the night view is wet.
    - The road lengths stay unverified; the area was not recomputed here.
