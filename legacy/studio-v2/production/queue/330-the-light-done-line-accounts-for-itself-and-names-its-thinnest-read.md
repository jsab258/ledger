line: instrument (FrameStats.h LightProbeDoneLine and LightDeltaLine,
  VignetteShot.cpp the probe walk)
spec: Four holes queue 326 left open by design, each named in the 22:25Z
  ruling's sections 3, 4 and 5 and routed here rather than folded into a
  batch that was already under review.

  ONE. THE DONE LINE DOES NOT ACCOUNT FOR ITSELF. Usable plus no-read plus
  no-control lights should equal lights probed, and nothing on the line says
  so. It holds by construction today, traced through the call paths, but that
  is an argument and not an instrument. Print lightsAccounted=U+N+K/P on the
  line with the word DISAGREE when the sum and P differ.

  TWO. A BRANCH NO KEY COUNTS. The NOT-COMPARABLE return is counted on no
  done-line key at all, so those lights vanish from every tally rather than
  appearing in one. Print lightProbesNotComparable=k.

  THREE. THE LAST SILENT PRE-CAP IN THE FILE. LightDeltaLine's Head[420]
  carries an unbounded light id and shot id through a fixed buffer with no
  Needed check, so an overlong id is cut BEFORE the Body[1400] announcer can
  see it. That is exactly the pattern 326's C5 removed from the done line,
  and a mutation test there proved that with the pre-cap in place the
  announcer CANNOT fire. Restructure as C5 did, or carry the ids as
  std::string.

  FOUR. THE WORST-FLOOR SELECTION PICKS BY A DIFFERENT STATISTIC THAN THE
  RULE DECIDES BY. It selects the worst shot by the control's MEAN while the
  rule decides reads by MOVED pixel counts. Two numbers, one name: either
  pick by MovedAtLeast at the lowest edge, or print both with each statistic
  named beside it.

  AND ONE PRINTER, NOT A BOUND: lightFloorThinnestRead naming the light, the
  shot, its pixel pair and the edge, over every YES in the run. Some of 326's
  surviving reads are one and two pixels over their floor, and a reader
  cannot see that from a count.
acceptance: every number above on the line with its denominator; the
  restructured delta line proven by a planted overlong id that ANNOUNCES
  rather than cuts, with the mutation shown both ways as 326's C5 was; and
  the thinnest-read printer emitting on a real run rather than only in a
  fixture. Under D45 a tool that measures the game: a test, no review, no
  ruling record.
max_sessions: 1
status: READY 2026-09-16, filed by the 22:25Z ruling's section 10 as item B.
  Behind 329 and the carrying run. Item THREE is the last instance in the
  file of a pattern already proven dangerous, so it should not wait long.
