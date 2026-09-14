line: instruments (Unreal)
spec: the phase 1 gate in ledger-v2/respec/roadmap-v2.md reads "sim holds
  frame budget at target resident count" and NAMES NEITHER NUMBER. There is
  no frame budget in ms and no target resident count anywhere in the row, so
  the gate cannot be read even in principle: it is a gate with no bound,
  which is CLAUDE.md rule 2 in a roadmap row.
  CORRECTING THE RESEARCH THAT RAISED THIS, because the reason matters for
  what gets built: the claim reaching Jafar was "nothing in the Unreal build
  measures a frame, the frame instrument is in Unity which D16 retired, and
  the file called FrameStats measures screenshot brightness". THE FIRST HALF
  IS FALSE. Unreal measures frame time today:
  VignetteSpec.h:1947 and :1964 emit frameMedianMs, "the MEDIAN of Timed
  game-thread frame deltas", 24 deltas after 8 discarded warm-up, per shot,
  and run 622bc39 read frameMedianMs=5.11/of=24warm8 on the hook shot. The
  claim about FrameStats.h is true and irrelevant: that file measures pixel
  luma and never claimed otherwise.
  WHAT IS ACTUALLY MISSING is the OTHER half of the gate. frameMedianMs is
  measured on a static vignette street with NO RESIDENTS IN IT. There is no
  Unreal scene with a population, so "at target resident count" has nothing
  to measure on, and the number that exists answers a different question from
  the one the gate asks.
acceptance: the gate's two numbers named from a printed series and not typed:
  a frame-time series over a rising resident count in Unreal, read at the
  count the roadmap intends, with the budget set from that series afterwards
  in that order. A run that measured no residents prints the words "nothing
  measured" rather than carrying the static-street number forward under the
  gate's name, which is the specific way this would go wrong quietly.
max_sessions: 1
status: READY 2026-09-14, ordered by Jafar. Phase 1 cannot have a gate until
  this lands, and that is his conclusion and it stands: a row naming a bound
  nobody can read is not a gate. Blocks the phase 1 close-out, blocks nothing
  in the visual slice.
