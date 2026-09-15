line: instrument (the camera that takes the frame Jafar judges)
spec: The cam_hook note in production/specs/vignette-scene.json derives the
  horizon row and the near-ground distance in the same paragraph, and the two
  derivations use the pitch in OPPOSITE directions. The horizon one reproduces
  exactly. The near-ground one does not. Settle which is wrong, and say what it
  does to the choice of fov_vertical_deg 39.0, which was made because of the
  near-ground number.
acceptance: A reading, not a change. Whoever takes it prints the arithmetic for
  BOTH the built camera and the Hook sheet panel, says which of the two
  derivations is sound, and states whether 39.0 still follows from the panel. If
  39.0 does not follow, the new number is NOT applied here: it goes to Jafar,
  because the camera is the composition and D23 names his eye.
max_sessions: 1
status: READY 2026-09-15. Found while sanity-checking a projection built to
  measure the rendered kerb for queue 181, and found because the projection was
  checked against the note rather than trusted.

  THE PROJECTION AGREES WITH THE NOTE ON TWO THINGS OUT OF THREE, and the two
  it agrees on are the ones that pin the camera:

    fovH from fovV 39.0 at 1280x720   projection 64.4   verdict prints 64.4
    horizon row                       projection 406.6  note derives 0.5641
                                                        of 720 = 406.2

  THE THIRD DOES NOT AGREE AND THE GAP IS NOT SMALL. The note says "the bottom
  edge of this frame lands 4.06 m ahead against the panel's 4.15 m, which is
  what sets the feel of standing there". The projection puts the ground at
  4.06 m on row 828 of a 720-row frame, which is off the bottom of the picture,
  and puts row 720 at about 5.26 m at eye 1.5975 or 5.43 m at eye 1.65.

  WHERE 4.06 COMES FROM, and it reproduces exactly, which is what makes this a
  finding rather than a disagreement: 1.650 / tan(19.5 + 2.6 degrees) = 4.063.
  So the note took the angle from the horizon to the bottom edge as fovV/2 PLUS
  the pitch. With the camera pitched UP the bottom edge swings AWAY, so that
  angle is fovV/2 MINUS the pitch, 19.5 - 2.6 = 16.9 degrees, and
  1.650 / tan(16.9) = 5.43 m.

  THE SAME PARAGRAPH GETS THE SIGN RIGHT SIX LINES EARLIER. On the horizon it
  says "the panel's horizon sits at row 348 of 617, which is 0.564 of the frame
  height and 0.128 half-heights BELOW centre, so the camera is pitched up", and
  that derivation reproduces to 0.4 px. One paragraph, one pitch, two
  directions.

  WHY IT MATTERS RATHER THAN BEING A TYPO. The note states plainly that
  fov_vertical_deg is "THE ONLY NUMBER HERE THAT NEEDS AN ASSUMPTION", and it
  gives the near ground as the reason 39.0 was taken: "39.0 vertical is taken
  so that the NEAR GROUND matches". If the near ground at 39.0 is actually
  5.43 m and not 4.06 m, then 39.0 was chosen for a reason that does not hold.
  Solving the other way at eye 1.65 for a 4.15 m near ground gives fovV about
  48.6 degrees, which is not a rounding difference and would change the
  composition of the frame Jafar judges by.

  WHAT IS NOT CLAIMED, and it is the reason this is a reading and not a fix.
  The panel's own 4.15 m may have been derived by the SAME method, in which
  case two consistently wrong numbers were compared and the comparison may
  still land somewhere defensible. That cannot be settled from this side: it
  needs the panel derivation redone, and the panel is
  production/art/atlas-01/concepts/hook.png on origin/art/atlas-01, read with
  git show rather than by checking that branch out.

  NOTHING MEASURED FOR queue 181 DEPENDS ON THIS. The kerb reading there used
  the projection, and the projection is pinned by the two checks that DO agree:
  focal length and pitch are what decide where a piece at known world
  coordinates lands, and both reproduce the note exactly. The near-ground
  number is a separate claim about the frame's bottom edge and moves nothing
  that was measured.
