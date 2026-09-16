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

CORRECTED 2026-09-16 02:50Z. THE CENTRAL CLAIM ABOVE IS FALSE AND THE ITEM IS
NARROWED. The builder sent to do it refused and was right. The original text
stays above UNEDITED, because an item rewritten after the fact is an item
nobody can audit.

WHAT WAS WRONG. "occurrences of any light key in the whole vignette verdict 1"
and everything drawn from it. The true reading:

    light LINES in run 47's verdict                                48
    shots they cover      exactly the 6 lanterns-true shots (camA, camB,
                          pinset_night_1 through _4)
    done line             lightProbeStatus=ALL lightsProbed=42/42
                          lightsReachedFrame=30/42 shotsProbed=6/43

  Queue 059's LIGHT PROBE has shipped this for six runs. It keeps the shot's
  own frame, turns ONE light off, re-renders at the same camera and condition,
  diffs in the g++-tested header, restores and reads the restore back
  (lightRestoreMismatch=0/42), and renders a control that toggles nothing.

  HOW I GOT IT WRONG, because the shape of the mistake is the lesson. I
  grepped KEY NAMES, `lant[A-Za-z]*=` and `prac[A-Za-z]*=`, and the probe
  emits a LINE TYPE: `light lantern0 kind=lantern ...`, carrying the lantern
  in a VALUE. So the count of 1 was true of key names and false of the
  verdict. CLAUDE.md rule 1 says grep for the SENTENCE and not the site; this
  is the same fault one level down, grepping for the shape I expected instead
  of reading what the file emits. Third time tonight in this seat: the same
  error found materialConnections absent when it was in ue-build.txt, and made
  an ancestry check pass against my own push.

WHAT SURVIVES, and it is one clause of four. THE PER-SHOT APPLIED STATE IS
STILL MISSING: 0 of 115 keys on run 47's vign_camA_night shot line name a
lantern or a practical, and the probe only looks at the 6 shots whose
condition has lights on. So `lightsSkippedAlreadyOff=0` over four runs is a
zero with a DENOMINATOR OF ZERO: the rejecting path exists and has never
fired, which is rule 5b's shape exactly. A per-shot asked-against-read pair
fixes that for free and prints the rejecting outcome on all 37 lanterns-false
shots.

WHAT DOES NOT SURVIVE, and must not be built:
  - the two-conditions-differing-only-in-lanterns experiment. It EXISTS and
    the existing one is tighter: one light at a time inside one condition at
    one camera, with its own floor on an identically formatted line. Building
    the proposed pair would add a 34th condition and a 44th shot, move the 43
    that several counts key on, and answer a weaker question.
  - the null-series clause. Already met: AppliedFieldsUnreal has carried
    lant.%s/prac.%s in the fingerprint since before this item, and run 47
    prints nullSeriesApplied=...lant.off/prac.off...
acceptance, REPLACED: the shot line carries shotLanternsAsked and
  shotLanternsRead=N/4, shotPracticalsAsked and shotPracticalsRead=N/3, and an
  agree key, the counts taken by walking the same populations lanternsPlaced
  and windowsLit report, the formatter and the agree decision in the
  g++-compiled header per queue 309's shape. It costs no render time and needs
  no spec change. Both outcomes watched, and the rejecting one is free: 37 of
  43 shots are lanterns-false and must read so.
