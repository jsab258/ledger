line: engine and art, jointly
spec: three fog rungs (0.020, 0.050, 0.080 at sky 1.00) and three sky
  rungs (0.35, 0.50, 0.70 at fog 0.100), cam_hook, sun 3.0, pin 0.300,
  everything else identical to the four A4 rows. Read on
  band.skyCentre.meanLuma and band.ground.p05 ONLY: shotMeanLuma and any
  near-black count are contaminated below about 0.25 by the world edge at
  the end of the street (the black band in ue-vign_fog_maxop0000.png).
acceptance: one committed run with the seven fog rows and the three
  cross rows, (a) and (b) above, and per-row asked beside read once 287
  has landed, the two statistics
  printed as a series over each axis, and overcast_day's value re-set
  BY RULING from that series and Jafar's eye, with the note field naming
  run, commit and rung.
  (a) AND (b) ARE SECTION 6 of
  game-design/decision-2026-09-14-ruling-the-null-series-follows-the-judged-row.md,
  which restated this line on 2026-09-14 because the words it replaces
  were never answerable: fogMaxOpacityRead occurs ONCE in the verdict,
  on the run-level sky line, and on 0 of the 37 shot lines.
  (a) the sky line's fogMaxOpacityRead reads the cap of the LAST
  condition applied, one per run, last-wins, and a value from the wrong
  row means the field did not reach the component on the last row or
  the shot order changed, named as one of those two.
  (b) THE FRAME ANSWERS PER ROW: the seven fog rows'
  band.skyCentre.meanLuma printed as a series in cap order and strictly
  decreasing with the cap, the four rendered rungs beside their 32bae70
  values 0.9268 / 0.8822 / 0.7979 / 0.6222 with residuals stated and NO
  bound, and the three new rungs between 0.7979 and 0.6222. A 0.100 row
  whose sky band sits at the 0.450 level is a cap that did not take.
max_sessions: 1
status: READY 2026-09-14. The judged row moves to 0.100 in the same
  dispatch under the ruling; this item is the series after it.
  THE SERIES IS RENDERED, run 622bc39, and (a) and (b) are both answered.
  (a) the run-level sky line reads fogMaxOpacityRead=0.100, which is the cap
  of the last condition applied (grid_null_repeat, moved to 0.100 by the
  18:23Z ruling), so the field reached the component on the last row.
  (b) band.skyCentre.meanLuma in cap order, strictly decreasing as required:

    fog    0.450   0.250   0.100   0.080   0.050   0.020   0.000
    mean  0.9268  0.8822  0.7979  0.7771  0.7370  0.6791  0.6222

  THE FOUR RUNGS RENDERED ON 32bae70 REPRODUCE EXACTLY, 0.9268 / 0.8822 /
  0.7979 / 0.6222 to four decimals, residual 0.0000 on all four, across two
  runs on different commits. Worth naming: rigDeterminism reads DIFFERS on
  both runs, and these band statistics did not move at all. That is evidence
  the sub-pixel grain does not reach a band statistic, and it is a stronger
  statement than the null floor because it spans runs rather than shots.

  THE TWO STATISTICS WANT DIFFERENT CAPS. On band.skyCentre.p50 and
  band.ground.p05, like for like against the sheet's 0.808 and 0.1935:

    fog    0.450   0.250   0.100   0.080   0.050   0.020   0.000
    p50   0.9331  0.8869  0.8035  0.7821  0.7410  0.6832  0.6285
    grnd  0.4617  0.3623  0.2536  0.2368  0.2100  0.1818  0.0862

  The sheet's sky sits between the 0.250 and 0.100 rungs, closest at 0.100
  (0.0045 under). The sheet's ground sits between the 0.050 and 0.020 rungs,
  around 0.030. FOG ALONE CANNOT SATISFY BOTH, which is what this item
  suspected and has now measured.

  AND THE CROSS ANSWERS IT. At fog 0.100, sky_intensity IS A GROUND-ONLY
  LEVER. At 0.35, 0.50, 0.70 and 1.00 the sky band's p50 reads 0.8035 at ALL
  FOUR, and so do its p05 (0.7883), p95 (0.8153) and spread (0.0270). The
  band is NOT clipped (band.skyCentre.clipHiAny=0/23040), so this is
  insensitivity and not saturation; only meanLuma drifts, 0.7979 to 0.7973
  across a near-threefold sky change, 0.0006 against a null floor of 0.0002.
  Meanwhile band.ground.p05 moves 0.2536, 0.2003, 0.1625, 0.1291. The sky
  band at this cap is FOG and not sky, consistent with
  skyModel=...the-far-field-is-the-height-fog.

  SO BOTH CAN BE MET AT ONCE. The candidate is fog 0.100 with sky_intensity
  0.70: sky p50 0.8035 (0.0045 under the sheet) and ground p05 0.2003 (0.0068
  over it). Against the shipped row's ground gap of 0.0601, that is the gap
  cut by about nine tenths for one value, with the sky untouched.

  NO CONSTANT IS SET FROM THIS AND NONE MAY BE. Section 2.2 item 3 of the
  16:25Z ruling reserves the re-set to a ruling made from the printed series
  and Jafar's eye, never to anyone reading residuals. This paragraph is the
  series, printed. The frame at sky 0.70 exists for whoever writes that
  ruling: production/d1-probe/ue-vign_fog010_sky070.png.
  UNANSWERED HERE: whether dropping the sky lever costs anything the two band
  statistics cannot see. Both frames were opened and the difference reads as
  deeper shadow rather than a changed light, but that is an eye and not a
  measurement.

  RULED 2026-09-14 20:01Z
  (decision-2026-09-14-ruling-the-reference-cell-is-the-grid-cell-at-the-judged-sky.md):
  Jafar took sky 0.70 at fog 0.100 off this series ('Sky 0.70 at fog 0.100 is
  taken. Apply it as the value and continue'). The last clause of this item's
  acceptance is met when the dispatch carrying sky 0.70 lands and the note on
  overcast_day names run, commit and rung; this item moves to done/ on that
  landing, and its rows leave under 293.
