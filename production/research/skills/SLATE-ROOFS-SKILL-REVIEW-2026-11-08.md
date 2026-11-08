# Review: the slate-roofs skill (8 November 2026)

Fresh reviewer. Read: the skill, its source list, dressing_tiles.py, terrace-front.py (palette, roof, stack, pot, aerial lines), vignette-scene.json "roofline" and blocks, ps5-corner.json's slate row, SURFACE-BANDS §4 and §7, TERRACE-KIT-TABLE §2, MAFIA-KIT §2, STEP9-PLAN, BASELINE, r2/r3/r5 reviews, the 6 Nov packaged reviews, RULINGS.md, and the RECIPE and DECISIONS entries by grep. Most numbers match their files (cut rows, holds, roughness 0.35/0.56, flashing 0.19 to 0.215, ridge 0.18/0.03, strip 0.10/15 mm, cap 0.06/0.15, pots, aerial, costs, try counts, the packaged pass). The steps run in a usable order.

**Verdict: PASS WITH FIXES**

1. **Line 48, density.** 1,536 px over 3.9 m is 394 px a metre. C6's band is 410 to 614 (street-weathering line 42), so the tile falls outside it, not "within 20%". dressing_tiles.py's docstring says "512 px a metre by construction", but the slate's side_px override breaks that. No DECISIONS, RECIPE or ps5-corner entry records an exception. The reviews judged only by eye ("not stretched"; slate size "cannot be measured"). The scale is also uneven: about 1.3 across against 1.63 down (2.39 m of source rows over 3.9 m). **Fix:** say the tile is 23% under the C6 floor, with no recorded exception and uneven scaling, and that the next change must either record the exception in DECISIONS or bring the tile inside the band.

2. **Line 12, pitch's home.** Pitch is read from vignette-scene.json's blocks ("roof.pitch_deg", overridden by "drawn"; terrace-front.py line 1169), not from terrace-front.py. That spec's "roofline" also holds unused gutter (0.112) and aerial rows, alongside the code's GUTTER_* and AERIAL_* values. **Fix:** name the blocks as pitch's home, and say the code constants win over the unused roofline gutter and aerial rows.

3. **Line 10, sources.** Reference first is in CLAUDE.md ("his rule, 28 October"); RULINGS.md has no 28 Oct line for it. MAFIA-KIT §2 does not say "photographed". It says fixed strips at one scale, with a cooked median of about 575 px a metre. **Fix:** cite CLAUDE.md, and quote §2's own words and density.

4. **Line 60, review size.** "One fresh small reviewer per batch" goes against the gate skill's "one view per fresh reviewer, never a bundle". Batching is allowed only for small pieces (RULINGS 3 Nov, reviews sized to the piece), yet line 19 says a roof change reaches every roof in the street. **Fix:** cite RULINGS 3 Nov and say that only a small texture or setting fix is batched, and that the packaged final reviews go one view per reviewer, as on 6 Nov.

5. **Line 67, shortfalls incomplete.** The 6 Nov packaged reviews listed three items the skill leaves out: the strips and ridge capping read as hard, even, near-black lines (review-reverse.json); the quay-end strip reads pale, like a painted line; and an orange fringe shows where the slate meets the near left gutter (review-hook-day.json). **Fix:** add these three, citing the packaged reviews.

6. **Line 48, "a Welsh terrace's" slate size.** The 26 cm by 17 cm claim rests only on a code comment. TERRACE-KIT-TABLE gives no slate size, and SURFACE-BANDS found nothing on Welsh slate. **Fix:** mark the slate size as unverified, the same status as line 24's period numbers.

Not faults: every step the skill states as proven matches its records (both 5 Nov faults passed on their second try, and the packaged reverse and hook reviews name the slate, strips and capping as present). Nothing contradicts RULINGS.md.
