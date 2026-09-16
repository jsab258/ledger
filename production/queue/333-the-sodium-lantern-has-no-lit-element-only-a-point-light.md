line: content (production/specs/vignette-scene.json lighting.lantern and the
  four lantern pieces, the surface binder that would have to carry a lit
  surface kind)
spec: D28 step 2 and the Hook sheet both want dusk with the sodium lamps lit.
  The four lanterns in the spec are pieces of shape box and surface metal
  carrying emissive=true, and THE EMISSIVE FLAG DOES NOT MAKE THE FIXTURE
  GLOW. It spawns a point light 0.05 m below the piece centre and nothing
  else. The box itself renders through the ordinary metal surface, so the lamp
  head is a dark object with an invisible light under it. No globe, no lens,
  no lit element of any kind exists in the scene.
acceptance: the lamp head carries a surface that reads as the emitting part at
  night, and a night frame in which the fixture is measurably the brightest
  warm thing in its own neighbourhood rather than a silhouette against the sky
max_sessions: 2
status: READY 2026-09-16, filed from run 48's committed frames and the source.

  READ IN THE CODE, NOT INFERRED FROM THE PICTURE.
  VignetteShot.cpp:1310 to 1326 is the whole of what emissive does: "A POINT
  LIGHT UNDER EVERY EMISSIVE PIECE", then `if (!P.Emissive) { continue; }` and
  a SpawnPointLight. Grepping SurfaceBind.h and tools/ue/make_base_material.py
  for emissive, EmissiveColor and selfillum returns ZERO hits in either, so
  the surface binder never learns the piece is meant to emit. The four pieces
  are the only emissive ones in the file, 4 of 610, and each reads
  shape=box surface=metal asset=None bom=E2_sodium_lantern_head.

  SEEN IN THE FRAME. Magnified from ue-pinset_night_3.png, both lamp heads are
  dark rectangles on dark poles against a pale sky. Over the whole frame, 26
  pixels of 921600 have R minus B at or above 20, the brightest of them at
  luma 68, and the brightest pixel in the frame is the neutral sky at 181.
  There is no warm bright thing anywhere. The one warm source that DOES render
  in this street is a window practical in vign_camA_night: 23 pixels at
  (1045,170) to (1051,173), peak R minus B of 130 at rgb 131/108/1, with soft
  falloff around it. So the glow mechanism works in this scene and the lamp
  simply has nothing to glow with.

  THE ORDER THIS IMPLIES, and it is the opposite of the one the studio was
  about to take. Exposure was the standing suspect. It is not the cause: a
  tonemap is monotone, so no exposure makes a fixture darker than the sky
  behind it come out brighter than it. Exposure is still owed for a different
  reason (queue 332 and 334), but a lit lamp does not arrive with it.

  WHAT MUST NOT BE GUESSED ON THE WAY. lighting.lantern's own note says range
  18.0 and intensity 3.2 "are NOT derived and are the first values of a series
  that has never been printed: they are the numbers the night frame will be
  tuned from once one exists, and rule 2 forbids calling them anything better
  than that". That still stands. The colour IS derived and is not in question:
  589 nm low pressure sodium through the CIE 1931 functions, gamma 1.000 /
  0.857 / 0.000.

  THIS IS SPEC AND ENGINE WORK, NOT A TOOL. It touches production/specs and
  probably the surface vocabulary, so it is GATED and wants a director before
  it lands, unlike 329 and 332 beside it.
