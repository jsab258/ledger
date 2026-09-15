line: engine (VignetteShot.cpp ApplyCondition, SurfaceBind.h, VignetteSpec.h)
spec: Wetness reaches the material once per run, chosen at bind time off
  the first shot's condition (queue 186's static half, landed 2026-09-15).
  Eight of the committed file's 43 shots carry another wetness (wet_night
  x2, pin_setter_night x4, wet_000, wet_100) and are photographed at 0.6.
  RULED 2026-09-15 07:55Z: NO NEW GLOBAL AND NO LIST. Each piece's
  component holds the MID BindSurfaces made (compMaterialIsMid=is-the-
  instance-we-made on every reached line of ce99814) and GByName holds
  every piece actor. ApplyCondition is the owner: walk GByName, take
  GetMaterial(0), cast to UMaterialInstanceDynamic, re-drive BOTH
  parameters, Wetness through WetBindFor and AlbedoGrade through
  WetGradeFor, per surface, so membership stays IsGroundSurface and no
  second list exists. A write-on-change guard keyed on the last applied
  wetness, because ApplyCondition is re-entered every settle tick and a
  naive re-drive is one write per piece per tick. When it lands wetness
  JOINS the fingerprint in AppliedFieldsUnreal, the wet_ rows leave the
  null series, and the nullSeriesExcludes value and its assertions in
  vignette-spec-test.cpp change in the same commit. Decision, counts and
  strings in SurfaceBind.h where g++ runs them; the .cpp supplies the walk
  and the live state only.
acceptance: the per-surface line prints wetSet per condition, the done
  line's wetnessModel token no longer says static, one
  run shows shotWetness and shotWetnessOnPieces at 0.9000 with
  shotWetnessAgrees=yes on a night row and at 0.0000 on wet_000, on the two
  rows' own lines (midWetSetGot is one surface's last-wins pair and cannot
  carry two values in one run, ruled 22:25Z), the null
  group at cam_hook drops the wet_ rows that ACTUALLY differ (see the
  correction below, it is two of three) and says why, and the guard's
  writes-per-tick prints with its denominator. Both suites green with a
  planted rejecting case for the guard (an unchanged wetness writes
  nothing). Taken AFTER the first wet frame is read under section 9 of the
  07:55Z ruling, not before: it changes none of the judged shots.
max_sessions: 2
status: LANDED 2026-09-15 under the 22:25Z ruling, UNRENDERED; the run that
  carries it is the first landed run whose commit contains the batch commit,
  read in that ruling's section 10 order.
  Filed 2026-09-15 by the ruling of 07:55Z
  (decision-2026-09-15-ruling-wetness-lands-static-and-the-widening-is-
  not-an-instrument.md). Ordered behind the first wet frame's reading.
  The dusk frame, Jafar's third item, is photographed at the static 0.6
  until this lands; if its row is to carry another wetness, this item is
  its dependency and the dusk item names it.

CORRECTED 2026-09-15 22:24Z UNDER D43, by the builder's measurement and not by
this item's author. THIS ITEM SAID "the three wet_ rows" LEAVE THE NULL GROUP
AND THAT IS WRONG; SO DID THE BRIEF THAT SENT THE BUILDER. Read off the
committed spec rather than predicted:

    condition          wetness  sun   lanterns  sky   fog     expPin
    overcast_day         0.6    True    False   0.7   0.012    0.3
    grid_null_repeat     0.6    True    False   0.7   0.012    0.3
    wet_000              0.0    True    False   0.7   0.012    0.3
    wet_060              0.6    True    False   0.7   0.012    0.3
    wet_100              1.0    True    False   0.7   0.012    0.3

  wet_060 IS AT THE REFERENCE CELL'S OWN WETNESS and matches it on every other
  field, so once wetness is per-condition it is a GENUINE NULL SAMPLE of the
  day group and it is right that it stays. TWO rows leave, not three: the group
  goes 9 to 7 and distinct groups 28 to 30. The suite counts this off the
  discovered ids rather than typing the number ("wet ladder rows still in the
  null group: 1 of 3 offered"), which is the only version of this that cannot
  decay the way the sentence above did.
