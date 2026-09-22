line: engine (test hygiene, ue-probe/tests/vignette-spec-test.cpp)
spec: the check at 3463 to 3467 says "the spread, the one-pair drift
  and whether the group is monotone all print" and asserts
  nullSpreadMeanLuma=0.0015, the fixture's maximum possible spread
  (0.0005 times shot index mod 4), true only while the discovered
  group holds a shot at residue 0 and one at residue 3. It went red on
  2026-09-14 for that reason alone (residues 1, 2, 3 gave 0.0010) and
  will again on any row change that shifts the residues. Split it:
  one check that the three keys print; one that the printed spread
  equals the spread recomputed from the discovered group's own
  indices by the fixture's formula, so the expected number moves with
  the data the way the derived id list does.
acceptance: both checks on the live spec with the accepting case
  printed; a planted group at residues {1, 2} (expected 0.0005)
  passing the recomputed form and failing the literal form, printed.
max_sessions: 1
status: READY 2026-09-14, filed by the ruling of 18:23Z. Not blocking.
