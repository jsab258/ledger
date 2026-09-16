line: instruments (FrameStats.h LampPatchLit and LampGlowSegment, landed
  d9af9a3d; first real readings in run 49, e1b4de77)
spec: `LampPatchLit` is `CoreMaxLuma > RingMaxLuma && CoreMaxWarm > RingMaxWarm`.
  NO CONSTANT ANYWHERE, which was deliberate and correct at the time: it made
  the verdict reachable without anybody choosing a threshold nobody had
  measured (rule 2). RUN 49 IS THE SERIES THAT SHOWS WHAT THAT COSTS. A day
  row, every lantern off, read one lantern LIT:

      cond=overcast_day
        lantern1  YES  coreLuma=217 ringLuma=215  coreWarm=1  ringWarm=0

  It cleared "strictly greater on both" by TWO luma and ONE warm byte. For
  contrast, the same instrument on a night row where the lamp is genuinely
  burning:

        lantern0  yes  coreLuma=193 ringLuma=39   coreWarm=240 ringWarm=-30

  154 and 270. So the test cannot tell 2 from 154, and one byte of noise reads
  exactly like a sodium lamp.

  THE DENOMINATOR, so this is a rate and not an anecdote. Over the 49 shot
  lines run 49 wrote: night conditions (pin_setter_night n=4, wet_night n=8)
  read 1 to 3 lit; DAY AND GRID conditions read 1 lit on 11 of them, where the
  correct answer is 0 every time. The acceptance sentence this item's parent
  stated in advance, yes at night and no at day in ONE run, IS THEREFORE NOT
  MET, and it is not met for a measurement reason rather than a lighting one:
  the lamps really are lit at night, which the frames and the before-and-after
  picture show.
acceptance: the margin is PRINTED as its own pair on every lantern token
  (core minus ring on luma and on warm, named as what it is a statistic of),
  and a bound is then set FROM THE PRINTED SERIES and not from argument;
  a planted two-byte fixture reads not-lit and a planted night-margin fixture
  reads lit, accepting case first
max_sessions: 1
status: READY 2026-09-16, filed and NOT started, under Jafar's standing rule:
  an audit finding is filed and the standing order resumes.

  THE SERIES ALREADY EXISTS AND NOBODY HAS TO RUN ANYTHING TO GET IT. Every
  lantern token in run 49 already carries coreMaxLuma, ringMaxLuma,
  coreMaxWarm and ringMaxWarm, so the margins are derivable from the committed
  verdict for all 49 shot lines. Read those before choosing a number. That is
  the whole of rule 2 and it is already paid for.

  DO NOT "FIX" THIS BY RAISING A BOUND UNTIL THE SERIES IS READ, and do not
  fix it by removing the day rows from the denominator. The day row is the
  half that refutes; it is the reason the parent ruling moved the segment off
  probed shots onto every decoded frame, and an instrument that only reports
  where it expects to succeed is the one this project keeps rebuilding.

  ONE THING THIS ITEM DOES NOT CLAIM. It does not say the lamp is unlit or
  that the constant is wrong. kLampEmissiveUnitless at 1.00 produced a lamp
  measured at R-B=189 and luma=204 against a Hook sheet reference globe of
  maxWarm 140 and maxLuma 242, on a frame where the same bound read ZERO
  pixels the run before. The lighting works. The TEST that reports on it
  cannot yet distinguish it from noise, which is a different fault and a
  smaller one.

  RELATED AND SEPARATE: `of=3` never reaches `examined=4` on any row, because
  one lantern's eight-corner projection refuses. That is the projection
  working as designed on a lantern outside the frustum, not a fault, and it is
  why a night row reading 3/of=3 IS all readable lanterns lit. If a future
  reader wants that stated on the line rather than inferred, it is one token.
