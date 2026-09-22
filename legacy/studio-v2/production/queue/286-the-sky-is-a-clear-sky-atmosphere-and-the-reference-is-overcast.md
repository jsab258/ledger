line: engine and art, jointly
spec: at fog 0.000 the atmosphere alone renders the sky band at 0.6222
  with meanRGB 152.7/158.2/176.8, blue by 24 counts and 0.19 under the
  sheet's 0.808 (verdict 32bae70 line 209). The four constants at
  VignetteShot.cpp 183 to 186 are "a starting point" with no series. Print
  a series over Mie scattering scale (0.04, 0.08, 0.16, 0.32) at fog
  0.100 and the judged sky, 0.70 since 2026-09-14 20:01Z (a series at 1.00
  would be about the retired street), Rayleigh held, reading
  band.skyCentre.meanLuma and
  the B minus R gap per rung. No constant moves in that run.
acceptance: a committed run printing the Mie series; the rung where the
  sky band's B minus R gap closes to within the null spread named; and
  the overcast candidate frame from that rung sent beside the sunlit one
  so Jafar can say which way the gap runs (D23).
max_sessions: 1
status: READY 2026-09-14. The other route to an overcast, binding the
  HDRI the conditions have always named, sits under queue 186
  (LookForNamedHdri prints whether the file is reachable). Whichever
  series lands first decides the sky's lever.  SCOPED 2026-09-14, NOTHING BUILT, AND THE SHAPE IS NOT WHAT THE ITEM ASSUMES.

  MIE CANNOT VARY PER ROW AS BUILT. kSkyMieScale is a global constant declared
  at VignetteShot.cpp:184 and written at :1589 inside ApplyCondition(const
  Condition& C), in a block that takes C and IGNORES it for all four scattering
  values. Shots carry only id, camera and condition, and the binary takes one
  flag set and writes ONE verdict, so there are exactly two routes: a condition
  field, or four dispatches.
  FOUR DISPATCHES CANNOT MEET THIS ITEM'S ACCEPTANCE, which is the part that
  settles it. "Within the null spread" is a WITHIN-RUN statistic: NullSeriesLine
  takes the largest set of frames of ONE run sharing one fingerprint at one
  camera. Four runs carry four different null spreads and cannot be read against
  one. It would also move a constant four times, which this item forbids twice.
  So: the condition field, or nothing.

  THE CASCADE IS MEASURED, NOT ESTIMATED. The scoping agent replicated
  AppliedFieldsUnreal (VignetteSpec.h:2586) in python and reproduced run
  ce99814's verdict EXACTLY, nine samples over 28 distinct groups with the same
  nine ids, so the model below was checked against a landed run.
    field only, all 33 rows at the shipped 0.040: conds 33, shots 43, groups 28,
      largest 9. NOBODY joins or leaves; only nullSeriesApplied gains /mie0.0400,
      and the longest group key goes 137 to 147 chars against a Buf[384].
    field plus five rungs at the reference cell: conds 33 to 38, shots 43 to 48,
      groups 28 to 32, largest 9 to 10. vign_mie_004 JOINS (field-identical to
      the group); nobody leaves; the other four rungs are singletons.
  If Mie did NOT join the fingerprint the four rungs would fall INTO the null
  group and the run would publish a deliberate Mie spread as its own noise
  floor, which is the exposure-pin incident verbatim.
  The rest of the cascade: both readers need the key fail-closed on all 33 rows,
  StreetVignettePieces.cs must WRITE it or the C++ reader refuses the generated
  file, RefCellAgainstJudged goes stale on an unlisted field exactly as it did
  for fog_max_opacity, and CoreTests pins three counts that move (33 to 38, 43
  to 48, 26/38 to 31/43).

  B MINUS R NEEDS NO NEW KEY. band.skyCentre.meanRGB is already on every shot
  line and condition=<id> already labels the rung, so the whole series shape was
  derived off the committed verdict without adding anything. Jafar's
  no-new-instrument rule is satisfied by reading what exists.

  THE ITEM'S OWN HEADLINE NUMBERS BELONG TO A ROW THE SERIES IS NOT SHOT AT,
  and a reader will misread the result without this. "0.6222, blue by 24 counts,
  0.19 under the sheet" is vign_fog_maxop0000: fog 0.000 AND sky 1.00. The
  series is specified at fog 0.100 and sky 0.70, where the same band reads
  0.7975 luma, 0.010 under the sheet rather than 0.19, and B minus R +9.9 rather
  than +24. AT THE JUDGED CELL THE LUMA GAP IS ALREADY CLOSED and only a
  9.9-count colour gap is left. The series measures a gap four fifths smaller
  than line 2 of this item implies.

  AND THE ACCEPTANCE IS AT THE INSTRUMENT'S FLOOR AS LITERALLY WRITTEN. The
  nine-row null group's B minus R spread is 0.1 counts, and 0.1 is also the
  print resolution of meanRGB. So "closes to within the null spread" asks a Mie
  rung to make the sky band neutral to a tenth of a count, with the target
  sitting exactly at what the instrument can express. RESTATING IT IS A RULING
  AND NOT A BUILDER'S CALL, and Jafar's eye is already named in it (D23), so it
  goes to him or to a director: a direction and a magnitude ("which rung moves B
  minus R most, and does the frame read overcast") rather than a threshold.

  THE LEVER HAS NEVER BEEN SHOWN TO MOVE A PIXEL, and this is the finding that
  matters most. The atmosphere actor and all four constants landed in ONE
  commit, 884f049c on 2026-09-09, and nothing has moved them since. No key reads
  any of them back: grepped, and the only textual hit in the verdict is the word
  "inscattering" in a prose line. So if four rungs come back identical the run
  CANNOT TELL "Mie is not the lever" from "the setter never took".
  THE FIX IS A ROW AND NOT A KEY, which keeps the no-new-instrument rule intact:
  make the bottom rung Mie 0.000. Mie off against Mie at eighty times the engine
  default must change a sky if the setter works, so the series carries its own
  positive control (rule 5b) and its own null control (the 0.040 rung, which
  lands in the null group). That is why the recommendation is FIVE rungs and not
  the item's four.
  The false comment at VignetteShot.cpp:182 claiming "Every one is printed" is
  corrected in the same batch as this note.

  A NAMED COST: StreetVignetteHost.cs:166 renders EVERY shot in the plan and
  Unity has no SkyAtmosphere in this path, so five Mie rows are five extra
  Windows-build frames that differ in nothing Unity reads. Precedent exists
  (the wetness rows are null samples in Unreal for the mirror reason), so this
  is a cost to name rather than a blocker.

  AND ONE ODD THING NOBODY OWNS, flagged rather than chased: fog_max_opacity
  0.000 to 0.100 moves the sky band 0.6222 to 0.7979 at a HELD exposure. A ten
  per cent veil cannot do that by linear blending, so either SetFogMaxOpacity
  does not mean what the derivation at VignetteShot.cpp 205 to 221 assumes, or
  the tonemap is doing most of the work. It does not block this item and it was
  not measured.

<!--RULING spawn=2026-09-14T16:25:22Z-->

  JAFAR SETTLED THE FORK 2026-09-16T14:1xZ, AND HE SETTLED IT BY WIDENING IT.
  His words: "I approved the photograph, not a particular binding. If it needs
  a different asset type or a different setup to render as a sky, do that under
  D41 without asking; the ruling was the overcast photograph rather than the
  mechanism."

  SO THE LEVER IS THE PHOTOGRAPH AND NOT THE ATMOSPHERE. This item offered two
  routes and said whichever series landed first would decide; it is decided
  without a series, because the thing he approved was never a scattering
  constant. THE MIE SERIES IS NOT THE ROUTE and is not to be run to "compare
  fairly": running it now would spend a round trip settling a question he has
  answered.

  AND THE MECHANISM IS EXPLICITLY NOT HIS TO APPROVE, which is the part that
  unblocks the work. A different asset type or a different setup is the
  studio's call under D41, without asking. That removes the only thing that
  made this item wait.
