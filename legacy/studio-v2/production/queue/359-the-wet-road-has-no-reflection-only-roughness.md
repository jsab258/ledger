line: content/visual (production/specs/vignette-scene.json lighting and the
  night conditions; tools/ue/make_base_material.py's wetness model; whatever
  reflection source the Unreal scene does or does not have)
spec: JUDGED AGAINST THE HOOK SHEET ON 2026-09-16, which is Jafar's standing
  instruction for the visual slice and D41's loop. The lamps now light. The
  ROAD does not reflect, and the gap is measurable rather than an impression.

  THE MEASURE, chosen because it survives the day-versus-dusk exposure
  difference that makes absolute brightness useless here: the ratio of mean
  VERTICAL neighbour difference to mean HORIZONTAL neighbour difference over a
  road region. A wet road mirrors its surroundings in vertical smears, so its
  vertical gradient exceeds its horizontal one. The ratio is computed INSIDE
  each image, so exposure, grade and time of day cancel.

      HOOK street road (day, the approved reference)   v/h = 1.63
      run 49 pinset_night_3   (night, wetness 0.9)     v/h = 1.01
      run 49 vign_camA_night  (night, wetness 0.9)     v/h = 1.05
      run 49 settle_night_3   (night, wetness 0.9)     v/h = 1.03

  Three of ours, one reference. Ours are isotropic: vertical and horizontal
  agree to within five per cent, which is speckle. The reference is
  structured. AND OUR ROAD IS NOT SHORT OF VARIATION: its coefficient of
  variation is HIGHER than the reference's (0.485 against 0.323). We have
  plenty of noise and none of it points anywhere.

  WHAT IS RULED OUT, checked rather than assumed. The wetness value is not
  missing: `wet_night` and `pin_setter_night` both carry `wetness: 0.9` in the
  scene spec, and the drive reports `wetnessRedriveSetGot=0.6000..0.6000`,
  write-on-change, `wetnessRedriveRefused=...noMid.0`, so the parameter lands
  on the instances. The material is not missing it either:
  `materialWetnessOnMaterial=yes`, `materialWetnessParam=Wetness`.

  SO THE MECHANISM IS THE SUSPECT, AND THIS IS WHERE THE ITEM STOPS ASSERTING.
  The material's whole wetness model is
  `roughness.Lerp(RoughnessMap.R, 0.0800, Wetness)`. It lowers ROUGHNESS and
  does nothing else. A low-roughness surface is only a mirror if something
  exists for it to reflect and a method exists to reflect it; roughness alone
  produces a darker, glossier road rather than a reflecting one, which is
  exactly what four frames show. WHETHER THIS SCENE HAS ANY REFLECTION SOURCE
  AT ALL (screen-space reflections, a reflection capture, Lumen) IS NOT
  ESTABLISHED HERE AND MUST NOT BE GUESSED: nothing in this container can read
  the Unreal project's render settings, and the verdict carries no key that
  names one.
acceptance: the probe prints, per night shot, what the road's vertical-to-
  horizontal gradient ratio IS, so the number stops being something a human
  computes off a PNG by hand; and the scene names its reflection source on the
  scene line, or prints that it has none. THEN, and only with that series in
  hand, the road is moved toward the reference's 1.63 and the change is judged
  on the same ratio
max_sessions: 2
status: READY 2026-09-16, produced by the judging Jafar asked for rather than
  by an audit. The lamps landing is what made this visible: until run 49 the
  night frames had no light in them worth reflecting, so a road that did not
  reflect looked like a road that was simply dark.

  THE FIRST THING TO DO IS NOT TO CHANGE THE ROAD. It is to make the number
  the probe's own rather than mine. Every figure above was computed by hand in
  the container off committed PNGs, which makes it a one-off reading nobody
  can regress against. That is the instruments.md pattern and it is the same
  shape as the lamp: ship the printer, read real runs, set the bound last.

  ONE LIMIT OF THIS MEASURE, named so a later reader does not over-trust it. A
  road receding to a vanishing point carries geometric structure of its own
  (tiling bands, kerb lines), and those bias the ratio independently of
  wetness. Both images here are street-level views down a road, which is why
  the comparison is fair enough to act on, but the ratio is EVIDENCE OF A GAP
  rather than a measurement of reflectivity, and a bound set from it needs the
  per-shot series first.

  DO NOT RAISE `wetness` TO CHASE THIS. It is already 0.9 of a possible 1.0 on
  both night conditions, and the item's whole point is that the remaining
  0.1 is not what is missing.
