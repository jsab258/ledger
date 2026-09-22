line: instruments (the figure's silhouette reading)
spec: RUN 53 REPORTED `figureSil1=figure_michelle/yes` ON SIX settle_night
  SHOTS. The box was opened and there is NO FIGURE IN IT: a shopfront doorway,
  railings and crates. The instrument measured a dark doorway against a
  lighter surround and called it a person in silhouette.

  THE PROJECTION IS NOT THE FAULT, and that was checked before this item was
  written rather than assumed. cam_hook stands at x=4.0, z=-2.1, yaw 11, fov_v
  39; the figure is at x=17.5, z=4.0, which is 14.8 m away and 13.3 degrees
  right of the camera axis, putting it at x about 905 and subtending about 114
  px. The verdict reports box=x827..936 and projH=120.80. The instrument is
  looking exactly where it should be looking.

  SO THE FIGURE IS NOT VISIBLE WHERE IT IS STANDING, and the silhouette test
  cannot tell that from a silhouette. That is the whole finding. A core-versus-
  ring comparison answers "is this rectangle darker than its surround" and a
  dark doorway answers yes. IT HAS NO WAY TO ASK WHETHER A FIGURE IS THERE.

  MEASURED ON cam_A, WHERE THE FIGURE IS AT LEAST PARTLY VISIBLE, and the
  measurement is the item's other half: the same rectangle before (run 51,
  73c902b5) and after (run 53) differs in 461 of 5460 pixels by more than
  2/255, largest single-channel difference 168. Something rendered. The
  difference picture,
  `game-design/sim-shots/figure_run53_camA_before_after.png`, shows it is a
  NARROW VERTICAL SLIVER where run 51 had bright sky: the figure is almost
  entirely occluded and only the part of it that blocks a sky gap is visible.
  8.4% of its own bounding box changed.
acceptance: the figure line carries an OCCLUSION reading beside the silhouette
  one, so a figure nothing can see is distinguishable from a figure that is
  dark against its surround; and a planted frame with the figure fully hidden
  is refused as a silhouette, accepting case proven first
max_sessions: 1
status: READY 2026-09-16, filed at the budget ceiling, NOT started.

  THIS IS QUEUE 372's BIAS ARRIVING FROM THE OTHER DIRECTION. 372 warned the
  oversized ring would cause a FALSE NO at night. This is a FALSE YES, and the
  cause is not the ring size: it is that darkness is not evidence of a person.
  Read the two items together.

  WHAT MUST NOT BE DONE ABOUT IT: adding a margin so the doorway falls below
  it. The doorway is genuinely darker than its surround; a margin would hide
  this case and the real one together, and no series exists to set one from.
