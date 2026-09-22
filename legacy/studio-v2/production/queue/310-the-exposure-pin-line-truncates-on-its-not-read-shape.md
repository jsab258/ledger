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
  HEAD, 3095 after queue 186's comment lines, 3111 after queue 309's; seen
  at -O1 with code generation on, invisible under -fsyntax-only which
  cannot emit it) predates queue 186 and is not new.
  AND THE COMPILER CARRIES ITS OWN FIGURE, WHICH IS THE ONE THAT MAKES THE
  CAP REACHABLE, added 2026-09-15 22:22Z by the resident after reading the
  warning rather than the hand count. g++ says: "output 685 or more bytes
  (assuming 883) into a destination of size 760". So there are now THREE
  numbers on this row and they are three different statistics of one
  directive, which is why none of them replaces another:
      733 and 738   MEASURED, the two shapes an actual run emits
      794 to 796    HAND-COUNTED, the NOT-READ shape nobody has emitted
      883           THE COMPILER'S STATIC WORST CASE over the format string
  883 is 123 bytes over the buffer and 87 over the hand count, so the hand
  count UNDERSTATED the exposure and a fix sized to 796 would still be
  short. The bound this item sets must be read off the printed series the
  acceptance asks for, never off any of these three, per CLAUDE.md rule 2.
  VERIFIED NOT WORSENED BY QUEUE 309: HEAD and the 309 tree were compiled
  side by side in a `git worktree` (never a stash, a builder was live in
  the tree) and both emit exactly 1 warning with IDENTICAL byte figures;
  only the line number moved. The fix is the pattern the file
  already has at AppendChunk (848 to 856): a chunk that overran says so.
  The same printer covers the three buffers queue 186 added
  (WetnessDoneSegment 700, WetFields 420, the null-series 960), which were
  hand-counted and never printed.
  QUEUE 309 ADDED TWO MORE, per the 22:25Z ruling: WetRedriveSegment 860,
  whose worst shape the suite already builds and asserts (test 15d, the
  pattern to copy), and WetShotFields 420, of which two shapes are printed
  and the worst (two sixteen-character condition ids) is not built.
acceptance: the suite prints each segment's length for every shape it can
  build, NOT-READ included, as the series the buffers are sized from; the
  NOT-READ shape is the planted rejecting case, shown truncating before
  the fix and announcing or fitting after it; the accepting case (a
  PINNED-HELD day row) is unchanged byte for byte. No verdict key added.
max_sessions: 1
status: READY 2026-09-15, filed by the ruling of 07:55Z. Not a condition
  of the wetness batch and not folded into it: its own accepting and
  rejecting case.
