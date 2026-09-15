line: engine (VignetteSpec.h ExposurePinSegment, vignette-spec-test.cpp)
spec: ExposurePinSegment formats into char Buf[760] with no truncation
  announcement. Measured 2026-09-15 by the resident on the two shapes the
  g++ run emits: 733 and 738 bytes, 22 of headroom at worst. Hand-counted
  by the director in the 07:55Z ruling: the directive's fixed text is
  about 672 bytes and the NOT-READ shape (Word NOT-READ, and Read, Resid
  and Over each nothing-measured/nothing-measured at 33 bytes) comes to
  about 794 to 796, over the buffer by about 35. That is the failure row,
  and what it loses is the tail of shotExposurePinStat, the last key,
  cut mid-word and silently; no numeric key is lost. The
  -Wformat-truncation warning on this directive (VignetteSpec.h 3081 at
  HEAD, 3095 after queue 186's comment lines; seen at -O1 with code
  generation on, invisible under -fsyntax-only which cannot emit it)
  predates queue 186 and is not new. The fix is the pattern the file
  already has at AppendChunk (848 to 856): a chunk that overran says so.
  The same printer covers the three buffers queue 186 added
  (WetnessDoneSegment 700, WetFields 420, the null-series 960), which were
  hand-counted and never printed.
acceptance: the suite prints each segment's length for every shape it can
  build, NOT-READ included, as the series the buffers are sized from; the
  NOT-READ shape is the planted rejecting case, shown truncating before
  the fix and announcing or fitting after it; the accepting case (a
  PINNED-HELD day row) is unchanged byte for byte. No verdict key added.
max_sessions: 1
status: READY 2026-09-15, filed by the ruling of 07:55Z. Not a condition
  of the wetness batch and not folded into it: its own accepting and
  rejecting case.
