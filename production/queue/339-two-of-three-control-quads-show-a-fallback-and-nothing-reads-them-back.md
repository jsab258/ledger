line: instrument (VignetteShot.cpp SpawnControlQuads and the quad line;
  the projected boxes on the shot line)
spec: The probe spawns three control quads in front of one camera, each meant
  to display a built-in-code 2x2 texture of red, green, blue and yellow. The
  verdict supplies its own reading key verbatim,
  quadReads=four-colours-means-a-texture-override-reaches-the-sampler/checker-means-it-does-not,
  and then calls its own quad rectangles
  PROJECTED-BOXES-NOT-MEASURED-COVERAGE. SO THE INSTRUMENT PRINTS WHERE TO
  LOOK, PRINTS WHAT THE ANSWER WOULD MEAN, AND NEVER LOOKS. The grading was
  left to a human opening the image, and for at least four runs nobody did.
acceptance: the quad line carries, per quad, the four quadrant means and a
  verdict of FOUR-COLOURS or FALLBACK read off the pixels, with the count of
  quads graded beside the count spawned; a fallback is a fault the run
  reports rather than a thing a reader might notice
max_sessions: 1
status: READY 2026-09-16, found by an artifact-reader and re-measured by the
  resident from ue-vign_camA_day.png before being written down.

  TWO OF THREE ARE A FALLBACK. Per quad, the mean RGB of each quadrant,
  sampled on a stride of 2 with a 3 pixel inset, n per quadrant beside it:

      worldY=350   TL (196.9,255.0,169.8)  TR (252.0,254.4,181.4)
                   BL (255.0,140.5,106.6)  BR (158.0,189.3,252.9)   n=812
                   channel spread 148.4    FOUR COLOURS

      worldY=250   TL (218.1,221.3,214.5)  TR (219.8,223.1,217.1)
                   BL (221.4,224.7,218.8)  BR (219.6,223.0,216.6)   n=812
                   channel spread  10.2    UNIFORM, pale

      worldY=150   TL (213.9,217.6,210.4)  TR (214.3,217.9,211.2)
                   BL (206.5,210.4,203.2)  BR (215.6,219.3,212.2)   n=840
                   channel spread  16.1    UNIFORM, pale

  The spread is the widest channel mean minus the narrowest across all four
  quadrants of one quad, so it is a within-quad statistic and the three are
  comparable. 148.4 against 10.2 and 16.1 is not a marginal call.

  BY THE VERDICT'S OWN KEY that is two texture overrides not reaching the
  sampler, in a build whose entire surface system is texture overrides
  reaching a sampler. Whether it touches the CityPack surfaces is NOT
  established here and must not be assumed: the quad texture is built in code,
  not one of the four re-picked materials.

  IT ALSO ANSWERS QUEUE 313, which found "a colour card and two floating
  swatches" in the night frame on run 46, ruled out the 10 spec pieces tagged
  surface card, and reported a FAILED localisation by eye. The three are the
  run's own diagnostic quads, present by construction on every cam_A shot:
  controlQuadVisibility is hidden-for-every-shot-whose-camera-is-not-the-one-they-were-placed-from,
  and shotWholeFrameIncludesControlQuads reads yes on exactly the two cam_A
  shot lines. 313's hand-read rectangle (487,298) to (613,423) matches the
  projected box x488..614 y298..422 to within two pixels.

  AND THE CARD SITS IN THE MIDDLE OF THE ONLY FRAME THAT READS AS NIGHT,
  which is a separate consequence worth one line: the dusk frame cannot be
  shot from cam_A while the quads are in it, and the 06:35Z ruling refuses
  that frame for exactly this reason.

  UNDER D45 a tool that measures the game: a test, no review.
