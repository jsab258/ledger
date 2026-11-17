# Review of TRAFFIC-COST-2026-11-17.md (17 November 2026)

Verdict: PASS WITH FIXES

Checked: hours (1.5+2+6+5+2+3+3+2.5+4 = 29, matches). Confirmed in sources: carriageway 6.0 m and 48 m (vignette-scene.json), parked z 1.96 (street-vehicles.json), BusynessAt values, accel 2.6 / brake 5.5 / gap 1.6 / top speed 11.0 (Traffic.cs), 75 Traffic mentions in CoreTests, 2-VEHICLES.md lines 198-199, studies/05 (25 of 39), studies/12 line 76, H4b line 188, 4-BUDGETS 4.5 (7.5 vs 10.8, parked cars 0.5), SUMMARY.md (no ice-cream van, no brewery dray, GTA 25 colour sets). No real brands, alcohol, gambling or children. Dependency on one passed car matches RULINGS line 11.

Faults
1. Section 1 cites PLAN-PARKED-CARS-2026-11-17.md without a path; the file is in production/research/phase2-plan/. Write the full path.
2. Section 4 says Traffic.cs is "about 1,370 lines"; the file is 1,406. Write "about 1,400".
3. Section 3 gives the sound bed as -40/-45/-42 LUFS without a source; street-sounds.json has no such figures (they appear in studies/08-sound.md). Cite studies/08-sound.md.
4. S0 checks "a dated note" and S6 "in the mix's band" are weakly testable; S0 is not a walk check, so mark it as such. In S6 name the band's figure from studies/08.
5. S4 "within +-1 car per hour" is unmeasurable on a walk of minutes; state it as a logged spawn count over a scripted hour sweep.
6. Section 3 KCD2 claim "DELIVERY.md line 562" was not checked as to wording (line 562 reads "ABSENT... No analogue"); say "no analogue" rather than "no cars".
