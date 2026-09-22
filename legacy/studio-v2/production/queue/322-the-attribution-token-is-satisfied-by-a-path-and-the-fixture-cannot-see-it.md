line: gate (tools/attribution-check.py, its selftest)
spec: The row check is `token in text` over the whole of THIRD-PARTY.md
  (486 to 533 on 2026-09-15). A token that is a substring of a path,
  a filename or another row's prose passes with its own declaration
  deleted. Found by hand on 2026-09-15 for citypack-shortlist against
  the workflow filename and fixed by respelling; measured the same
  night by the 22:25Z ruling over all twelve tokens: CityPack is
  satisfied only by the path at THIRD-PARTY.md 184 inside a LOG
  paragraph headed NOTHING YET, and Kenney and ambientCG are satisfied
  by other rows' sections. The selftest cannot see any of this: its
  full_doc (692 to 696) is the tokens joined by spaces, so no
  rejecting fixture has ever contained a path or a sentence.
acceptance: a token counts only on a DECLARATION line (a `## ` heading
  carrying it, or a table row whose first cell is Source, Licence or
  Where), never in prose or a path; the rejecting fixture is built
  from the LIVE THIRD-PARTY.md by blanking one row's declaration lines
  and asserting that row alone goes red, run for every WATCHED row so
  the count of rows examined prints beside the count refused; the
  accepting fixture is the live document, which requires 323 first.
  Both counts on the done line. Under D45: a test, no review.
max_sessions: 1
status: READY 2026-09-15, filed by the 22:25Z ruling. Ordered after 323,
  because the accepting fixture is the live document and the live
  document is red under this rule until the pack has its row.
