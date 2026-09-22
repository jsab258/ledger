line: engine (the Unreal probe's verdict)
spec: the shot line gains shotFogMaxOpacityAsked,
  shotFogMaxOpacityRead and shotFogMaxOpacityResidual, read off the
  height fog component while THIS frame stood, at the read site and
  in the shape of shotSkyIntensityAsked/Read (VignetteShot.cpp, the
  per-sample read that feeds shotLightStat). The formatter lives in
  VignetteSpec.h, the tested layer; the fixture in
  vignette-spec-test.cpp plants one row reading 0.450 against 0.100
  asked (the 2026-09-14 fault shape) and one at residual 0.000000,
  accepting first. The run-level fogMaxOpacityRead keeps its name and
  its stat gains one-per-run/last-wins. VignetteShot.cpp 1547 to 1548
  and the four A4 notes say per run until this lands.
acceptance: a committed run whose 43 shot lines each carry the three
  keys, asked equal to the row's fog_max_opacity on 43 of 43 with
  residual 0.000000, the seven fog rows' asked values reading 0.450,
  0.250, 0.100, 0.080, 0.050, 0.020 and 0.000 on their own lines, and
  both fixture outcomes printed.
max_sessions: 1
status: READY 2026-09-14, filed by the ruling of 18:23Z. Read by that
  ruling as a widening of the existing shot line under the
  no-new-instrument rule; the landing director may read it otherwise
  and must then name a retirement. Does not block the fog dispatch.
