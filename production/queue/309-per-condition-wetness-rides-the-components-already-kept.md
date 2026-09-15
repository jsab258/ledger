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
  line's wetnessModel token no longer says static, one run shows
  midWetSetGot at 0.9000 on a night shot and 0.0000 on wet_000, the null
  group at cam_hook drops the three wet_ rows and says why, and the guard's
  writes-per-tick prints with its denominator. Both suites green with a
  planted rejecting case for the guard (an unchanged wetness writes
  nothing). Taken AFTER the first wet frame is read under section 9 of the
  07:55Z ruling, not before: it changes none of the judged shots.
max_sessions: 2
status: READY 2026-09-15, filed by the ruling of 07:55Z
  (decision-2026-09-15-ruling-wetness-lands-static-and-the-widening-is-
  not-an-instrument.md). Ordered behind the first wet frame's reading.
  The dusk frame, Jafar's third item, is photographed at the static 0.6
  until this lands; if its row is to carry another wetness, this item is
  its dependency and the dusk item names it.
