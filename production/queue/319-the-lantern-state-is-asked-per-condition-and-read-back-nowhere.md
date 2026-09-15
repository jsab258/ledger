line: engine (VignetteShot.cpp ApplyCondition, the shot line's light keys)
spec: A condition asks for the street lamps and the window practicals, and
  NOTHING READS BACK WHETHER THE ASK REACHED THE LIGHTS. Measured on run 46's
  committed verdict, 2026-09-15:

    conditions in production/specs/vignette-pieces.json     33
    of those carrying a `lanterns` and `window_practicals`  33
    of those setting BOTH true                               2  wet_night,
                                                                pin_setter_night
    shots in the spec                                       43
    shot lines in run 46's verdict                          43
    shots naming a lanterns-true condition                   6  camA/camB_night,
                                                                pinset_night_1..4
    keys on the vign_camA_night shot line                  109
    of those matching lant|prac|window|lamp|light            0

  The only light emit in the whole verdict is ONE run-wide line at scene build
  (line 186): lanternsPlaced=4/4 windowsLit=3/3 flatsLit=0/0 nothing-to-light.
  That is a count of what was PLACED, not of what was SWITCHED ON when a
  shutter opened. So a condition asking lanterns off and a condition asking
  lanterns on produce IDENTICAL instrument output today, and the frame is the
  only witness.

  WHAT IS NOT CLAIMED. ue-vign_camA_night.png is dark and its lamp post and two
  street lights read unlit to the eye, but shotMeanLuma=0.1203 with
  band.ground.p50=0.0337 under shotExposurePin=AUTO (read range 0.0300/8.0000)
  and fog_max_opacity 0.45, and a lamp that is ON but dim, a lamp that is OFF,
  and a lamp crushed by auto exposure are three different worlds that this
  frame cannot tell apart. THE LIGHTS ARE NOT SAID TO BE BROKEN. What is said
  is that nothing measures them, which is CLAUDE.md rule 6 in the same shape
  queue 309 records for wetness: a field that reaches the bind and whose
  applied state is unrecorded. Same class, different field, and 309's landing
  does not fix this one.

  THE TEST THAT WOULD SETTLE IT, and it cannot be run off the files on disk.
  Two conditions differing ONLY in `lanterns`, photographed at one camera,
  compared against this run's own noise floor. The floor is measured: the two
  frames the run itself certifies as sharing every applied input
  (vign_hook_day and vign_grid_null_repeat, both in nullSeriesIds) differ by
  696624 of 921600 pixels (75.59 per cent) at maxChannelDelta 29/255 and mean
  1.487 over the differing pixels. A lantern difference smaller than that is
  not a reading. No such pair exists in run 46: every lanterns-true condition
  also differs in hdri, sun, sky_intensity, fog and exposure_pin, so this
  needs a run and not an argument.
acceptance: the per-shot line carries the APPLIED lantern and practical state,
  read back off the lights while THAT shot stood, in the asked-against-read
  shape the camera and exposure keys already use, with its denominator (how
  many of the placed lights were reached). One run photographs two conditions
  differing only in `lanterns` at one camera and the difference prints BESIDE
  the null floor rather than alone. The null series says in its own value
  whether the lantern rows are in or out and why, as nullSeriesExcludes
  already does for wetness. Both outcomes watched: a lanterns-false shot must
  be shown to read as unlit by the same instrument that calls the other lit.
max_sessions: 1
status: READY 2026-09-15, found while reading run 46's night still for queue
  313 and while checking whether Jafar's third item can be taken as asked. It
  is AHEAD OF THE DUSK FRAME in that order, because "lamps lit, wet road, a
  figure in silhouette, that is the picture I judge by" is the deliverable and
  today nothing could tell him whether the lamps in it are lit. Sibling of 309
  and cheaper; neither blocks the other.
