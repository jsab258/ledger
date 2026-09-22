line: governance (CLAUDE.md, canon.md, and the tools they credit)
spec: Jafar ruled 2026-09-16: "The same test applies to every other claim in
  CLAUDE.md about what is enforced: check them all in that pass and report how
  many were true." A claim-auditor did. THIRTEEN claims found; SIX are cleanly
  true and wired; THREE are true in a narrower scope than their own sentence
  says; ONE is spot-verified only; TWO ARE FALSE; ONE was out of scope. The
  two false ones credit tools that exist, are tested, and are called by
  nothing.
acceptance: each false claim is either wired so the sentence becomes true or
  deleted so the file stops asserting it, each partially true claim's sentence
  is narrowed to what is actually checked, and the count is re-run afterwards
  so the remedy is measured rather than assumed
max_sessions: 2
status: READY 2026-09-16, the count with its denominator, and the two false
  claims re-verified by the resident before filing.

  THE HEADLINE IS NOT goal-block-check. IT IS THE CANON GATE.
  CLAUDE.md:33-34 says of canon.md "violating it is a gate failure, not a
  style note", and canon.md:5 says the same of itself. `tools/canon-gate.py`
  is 13KB, self-described as "The mechanical canon gate", implements the
  MODERNITY dict and forbidden_brands, and HAS ZERO CALL SITES. Re-verified:
  a grep over every .py, .sh, .yml and .yaml returns exactly one reference
  outside the tool, a comment in tools/content-gate.py:828 drawing an analogy.
  Not in verify.py's check tuple, not in ci-checks.sh, not in any workflow.

  WHAT THAT LEAVES UNGUARDED IS THE THING THIS PROJECT DRIFTS ON MOST.
  CLAUDE.md section 0: "Any 1950s or 1970s framing is wrong and is corrected
  on sight. Both drifts have happened here, one of them four times in a single
  conversation over four sources that were all correct." The gate that would
  catch an era artifact or a real brand runs never. Two NARROWER gates are
  wired and are easy to mistake for it: content-gate.py covers the D17/D18
  content rule, and canon-register-check.py (landed today) covers canon's own
  citation and status consistency. NEITHER catches an era or brand violation.

  THE SECOND FALSE ONE, CLAUDE.md:227-228: goal-block-check.py "proves the
  goal block still matches vision-pillars-v2.md". Wired into nothing.

  THE THIRD, FLAGGED AS PART-UNVERIFIABLE: CLAUDE.md:159-161, "wc26-picks is
  the archive, never pushed". No repo-local enforcement; .git/hooks holds only
  stock samples. Whether GitHub branch protection covers it is outside what
  this repository can read and was NOT asserted either way.

  THE THREE THAT ARE TRUE IN A SMALLER SCOPE THAN THEY CLAIM:

  1. THE LICENCE ALLOWLIST, CLAUDE.md:40-42. The asset half is wired and walks
     the whole tree with a denominator. The governance half, "a new tool enters
     only through a decision record naming its weights licence", has NO
     mechanical check: nothing detects that a new external tool was added and
     looks for the record. Process only.
  2. THE FORMATTING LAW, CLAUDE.md:43-45, "no em-dashes and no italic text in
     anything written from 31 August on". Enforced ONLY on player-facing game
     text, via slopcheck.py scanning ledger/Assets/Scripts/**/*.cs, AND AS A
     RATCHET at SLOP_CEILING 88 rather than at zero; plus the glance page.
     NOTHING SCANS THE DOCUMENT CORPUS the sentence's own words address.
     Re-verified by the resident: slopcheck.py:153 globs *.cs under
     Assets/Scripts and nothing else. The resident has hand-grepped every
     commit today for a law no tool applies to documents.
  3. RULE 9's concurrency claim, spot-verified at 10 of 19 workflows carrying a
     named per-workflow group, which matches the sentence; whether every
     expensive job is opt-in was not checked within budget and is not claimed.

  AND ONE THAT IS NOT FALSE BY ITS OWN WORDING BUT IS WORTH THE SAME EYE.
  CLAUDE.md:205-206, "Asked at close through production/quality-ladder.md".
  That file has ZERO readers in any .py, .sh or .yml. The sentence says ASKED,
  not checked, so it is not a false mechanical claim; nothing prompts or
  confirms the question was ever put at any close.

  THE SIX THAT ARE CLEANLY TRUE, named because a report of only the failures
  is a zero without its denominator: rule 10's docs-check and the 400-line cap;
  rule 12's sim-shots CI channel; the verify footer written on green and
  deleted on red (and enforced HARDER than the sentence claims, by a PreToolUse
  hook that blocks git commit unless the footer is newer than every changed
  file); director_cadence and the RULING stamp; report-frame.py withholding a
  picture when the last build measured nothing; and verify.py printing
  CLAUDE.md's own word count.

  THE BEST EVIDENCE THAT THIS IS A RECURRING CLASS AND NOT A ONE-OFF sits in
  the tree already: docs_shape()'s own docstring reads "THE TOOL EXISTED AND
  NOTHING RAN IT ... it was never wired into this file ... Nobody did for long
  enough that queue.md reached 536 lines against its own 400-line cap." That
  is this exact fault, found and fixed once before, and the file says so.

  CLAUDE.md AND canon.md ARE BOTH DIRECTOR TERRITORY. Nothing here is applied
  by the resident.
