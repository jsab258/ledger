line: gate (ledger/verify.py surface_tint_agreement and its footer fixture)
spec: tools/surface-tint-check.py prints two pass lines since queue 186,
  "N surface(s) compared, 0 disagreement(s), tintsOnly=..." and "M wetness
  constant(s) compared, 0 disagreement(s), wetCovers=...". verify.py 854
  to 861 reads only the first, with the regex (\d+) surface\(s\) compared,
  and prints "surface tints agree (2 surface(s) compared, tints only)".
  The exit code covers both lines, so a drifted 0.92 goes red today; the
  green string cannot show that six more constants were examined, which
  is rule 3b's denominator missing from the one channel everybody reads.
  The red label at 856 says THE TWO COPIES OF THE SURFACE TINTS DISAGREE
  for a wetness disagreement too, naming the wrong table.
acceptance: the footer carries both counts live ("2 surface(s), tints
  only; 6 wetness constant(s)" or equivalent); the red label names which
  comparison failed; _strings_selftest carries the two-line shape as its
  accepting fixture and the one-line shape (the tool before 186) printing
  nothing-measured for the second count rather than a zero.
max_sessions: 1
status: READY 2026-09-15, filed by the ruling of 07:55Z. verify.py is not
  in the wetness batch and a formatter change needs its fixture, so it is
  not a one-line hand-apply.
