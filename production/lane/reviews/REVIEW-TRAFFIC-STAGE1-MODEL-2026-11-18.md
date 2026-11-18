# Review: traffic stage 1 reference model (18 November 2026)

Fresh reviewer. Read the spec, the costing note and all of tools/lane/traffic/. Ran the 55 tests (all pass) and scratch probes.

## Verdict: PASS WITH FIXES

IDM, timetable, random numbers and pool are sound and portable. Two behaviours are wrong and baked into G7, and one spec claim fails after 10 minutes. Regenerate the goldens after fixes 1 to 4.

## Findings

1. traffic_model.py, lines 208 to 209 and 232 to 235: after an emergency stop the stand-off point is over 0.5 m behind the car, so the filter drops the person. The held car logs acceleration +1.0 every step, a new emergency_stop every 0.1 s (33 in G7), and never horns. Fix: for each person with c.x < bx <= c.x + detect_m, use bx - person_standoff_m if that exceeds c.x - 0.5, else bx - contact_m. Log emergency_stop only when the clamp stops a moving car. Test: one event, a_mps2 not positive while held, horn at 3 s.

2. traffic_model.py, line 233: the clamp can move a car backwards (a person 0.1 m ahead moves it from 10.0 to 9.8 m). Fix: c.x = max(x_before_step, person_x - contact_m).

3. traffic_model.py, line 217: a person beside the car body (between bumpers) is ignored; the car drives through. Fix: take people with bx > c.x - c.length into `ahead`; if bx <= c.x, hold the car, v = 0, log one emergency_stop. Add to spec rule 7.

4. traffic_model.py, lines 271 to 281, rates.json hour_horizon_s: each hour's stream stops at 600 s. Clock held at 12:00 for 1,800 s: last spawn at 537.8 s. Spec rule 1 says cars keep coming. Fix: draw each lane's next arrival lazily from its keyed stream, keeping its Rng state until the hour changes; drop hour_horizon_s. Test: spawns after 600 s on a held clock.

5. traffic_model.py, lines 168 to 172: above v0 the code adds the plain IDM interaction term to the IIDM free term. That hybrid is not the published IIDM (from memory, ch. 11.3: a_free + a(1 - z^2) when z >= 1, else a_free; unverified, book not reached). It brakes slightly harder, the safe side. Fix: call it a hybrid in the docstring and spec rule 4, or implement both IIDM cases. Plain IDM below v0 matches Zhou et al. eq. 1 and 2 (read today). City values match cars.json; Table 11.2 not reached: unverified.

6. Port ambiguity, lines 281, 303, 321 to 328, 239, 260: the spec pins only the acceleration order. Also pin: pending sorted by (due_ms, lane, hour, n); spawns before the step; events and despawns in car-list order; hour from integer ms (t_ms // 30000); delta as x*x*x*x; horn timer as an integer step count, not summed 0.1 with 1e-9 slack. Street.day never advances, so past 24 game hours day 1 replays. Fix: hour_of returns (day, hour); load_hour rekeys on day.

7. test_traffic_model.py, lines 159 to 162: "nothing stuck" is true by construction. Fix: assert no car stays under 0.3 m/s for 20 s without a person ahead.

8. test_traffic_model.py, line 61: test_traits_do_not_depend_on_rates never touches rates. Fix: alter the mean gaps in memory and assert traits for the same (hour, lane, n) are unchanged.

9. Coverage: over 200 seeded days no car is dropped, so deferral, the 10 s drop, the pool limit and deferral across an hour change are never exercised; the soak has no people. Fix: golden G8, a person blocking lane 0 for 60 s in a rush hour across an hour change (queue, full pool, defer, drop, horns in the log).

10. test_traffic_model.py, lines 103 to 108: never checks the promised emergency_stop event. Fix: assert exactly one.

## Spec claims against goldens

Speed cap 9.17 to 9.45 m/s (claim about 9.2: fair). Stop 1.78 m behind the stand-off (about 2 m: fair). Horns 2.9 and 9.9 s after first under 0.3 m/s (matches). 7.72 cars a day over 200 seeds against 7.67 expected (matches). 55 checks: correct. Held clock and emergency stop: wrong (findings 1, 4).
