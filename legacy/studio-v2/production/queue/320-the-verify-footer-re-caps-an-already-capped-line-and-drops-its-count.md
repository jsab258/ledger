line: infrastructure (the evidence channel)
spec: this file
acceptance: (1) ledger/verify.py's attribution() wrapper never slices the
  FAIL line it reads from tools/attribution-check.py below the point where
  the embedded count and file list would be visible, for a rejecting fixture
  (a stray list wider than the wrapper's own width) and an accepting one (a
  short stray list, no notice printed), accepting case run first per rule
  5b; (2) the same question asked of every one of the 24 FAIL-line
  extraction sites this item catalogues in ledger/verify.py, each checked
  against its OWN underlying tool's message shape rather than assumed from
  this item's 5-of-24 sample, with the count actually fixed and the count
  still open both printed in the closing status, so a partial fix cannot
  read as a complete one; (3) the fix holds for a tool whose own message has
  NO inner cap at all (tools/pc-watcher.py's shape: a raw ", ".join with no
  count), not only for one that already caps well (tools/shape-check.py's
  shape: capsay.cap with its own "(+N more of M)"), because today's sample
  contains both shapes and a fix aimed at only one would leave the other.
max_sessions: 2
status: READY 2026-09-15, filed while closing the attribution red build for
  the citypack shortlist row (THIRD-PARTY.md + tools/attribution-check.py,
  same day, same commit batch). See also queue 060, same symptom in the same
  footer line, marked CLOSED 2026-09-10 "BY COMMIT cd55a79c" with "No ruling
  named this closure; see production/queue/275" on its own status line.
  CHECKED, NOT ASSUMED: cd55a79c's diff to tools/attribution-check.py (git
  show cd55a79c -- tools/attribution-check.py) adds only the .svg suffix
  entry; production/queue/275 is a bulk archival-closure commit and does not
  mention "060" anywhere in its own text (grepped). The line in
  tools/attribution-check.py that makes ITS OWN cap() announce truncation
  ("(+N more not shown)") was added by commit d69b8d0c, dated 2026-09-02,
  the CLAUDE.md split, a day BEFORE queue 060 was even filed (2026-09-03) -
  so whatever queue 060's fix actually was, it was not that line, and I have
  not traced further than this. What follows is the finding, verified fresh
  today, independent of that history.

## The finding, measured today rather than inherited from queue 060

`python3 ledger/verify.py`, footer line, before today's fix:

    ATTRIBUTION: no asset files live outside a directory this file knows
    about (2860 asset file(s) of 5825 walked, ex...

Run directly, the same problem, on the same day, shows every filename:

    python3 tools/attribution-check.py
      FAIL no asset files live outside a directory this file knows about
      (2860 asset file(s) of 5825 walked, examined):
      tools/citypack/shortlist-2026-09-15-network-blocked-proof/contact-concrete.png,
      tools/citypack/shortlist-2026-09-15-network-blocked-proof/contact-kerb.png,
      tools/citypack/shortlist-2026-09-15-network-blocked-proof/contact-metal.png,
      tools/citypack/shortlist-2026-09-15-network-blocked-proof/contact-plaster.png

`tools/attribution-check.py`'s own `cap()` (line 380) is not the fault here:
4 items is under its `limit=5`, so it emits the full sentence, colon and all
four names, un-truncated. The fault is one layer up. `ledger/verify.py`'s
`attribution()` wrapper (`def attribution()` at line 2002) does this at line
2019-2021:

    bad = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
    return False, "ATTRIBUTION: " + _cap(bad, strip=5, width=100,
                                         tail="see attribution-check").strip()

`bad` holds ONE element here (one FAIL line, because only one of
attribution-check.py's checks failed), so `_cap`'s `keep=1` list-level
cutting drops nothing and never appends "(+N more)". The cut is
`capsay.cap`'s WIDTH cut instead: it takes the first 100 characters of that
one already-complete sentence and appends its own TRUNC marker ("..."). 100
characters lands inside the word "examined)" and never reaches the colon,
so the four filenames, the entire actionable content of the failure, are
gone. What is left ("...ex...") announces that SOMETHING was cut (the
ellipsis) but not WHAT or HOW MANY, which is `.claude/rules/instruments.md`'s
own rule stated exactly: "Any cap in a log-extraction step must announce
when it bites" - a bare ellipsis is not an announcement of a count.

## Why this is not the same fix queue 060 needed, even though the symptom is byte-identical

Queue 060's acceptance criterion 1 was about the TOOL's own cap
self-announcing, which it now does (confirmed above: attribution-check.py's
`cap()` prints "(+N more not shown)"). Today's fault survives that fix
completely intact, because it happens ONE LAYER UP, after the tool has
already produced a correct, complete sentence: `ledger/verify.py` re-caps
the WHOLE LINE (label plus count plus colon plus list) by raw character
width, with no awareness that the tail of that string is itself a
list-with-a-count that a reader needs. A tool-side fix can be perfect and
this still happens, because the second cut is not the first tool's fault.

## The sweep this item is asking for, with its own denominator

`grep -c '_cap(' ledger/verify.py` -> 93 total `_cap(` call sites in the
file. `grep -c 'startswith("FAIL")'` (three quoting variants) -> 24 of
those are downstream of the specific idiom this bug lives in: extract every
line starting with "FAIL" out of a subprocess's (or, at two sites, an
in-process fixture's) stdout, then hand the resulting list to `_cap` a
second time. Line numbers of all 24, read in context, with their `_cap`
call's `width`/`strip`:

    502 clip_audit               width=90   -> tools/clip-motion.py --selftest
    538 picker_selftest          strip=8  width=90   -> (mixamo picker) --selftest
    584 sheet_read               strip=5  width=93   -> (prop sheet reader) --selftest
    621 prop_dimensions          strip=5  width=93   -> tools/prop-dimensions.py --selftest
    697 _meshgen_suite           strip=5  width=91   -> (shared ue selftest helper)
    911 powershell_steps         strip=5  width=93   -> (pwsh step parser) --quiet
    1078 ue_material_selftest    keep=3 (width 90)    -> (ue material gen) --selftest
    1116 ue_prop_import_selftest keep=3 (width 90)    -> (ue prop importer) --selftest
    1142 voice_assets            width=110  -> tools/stage-voice-assets.py --selftest
    1161 voices_into_build       width=110  -> tools/put-voices-in-build.py --selftest
    1199 pc_watcher               width=110  -> tools/pc-watcher.py --selftest
    1222 card_writing            width=120  -> dotnet Tier2Gen --selftest (C#, different idiom)
    1642 docs_shape              strip=5  width=100  -> tools/docs-check.py
    1701 budget_ceiling_line     strip=5  width=100  -> (budget ceiling check)
    2019 attribution             strip=5  width=100  -> tools/attribution-check.py   [THE FILED BUG]
    2088 filename_as_type        width=110  -> tools/lint-filetype.py --selftest
    2365 workflow_branch_refs    strip=5  width=90   -> (workflow branch refs) --selftest
    2495 stranger_test           width=120  -> dotnet StrangerTest (C#, different idiom)
    2513 shape_files (x2: 2532, 2548)  width=90   -> tools/shape-check.py
    2669 voice_live (per-script) width=70   -> tools/voice-live/*.py --selftest
    2678 voice_live              width=90   -> tools/voice-live/*.py --selftest
    2704 voice_gen               width=90   -> tools/voice-gen/ledger_voice_gen.py
    7421 director_cadence        width=120  -> in-process fixture, no subprocess
    8238 footer_strings          width=120  -> in-process fixture, no subprocess

I READ ALL 24 IN THIS VERIFY.PY-SIDE CONTEXT (the table above). I additionally
opened the UNDERLYING TOOL's own message-construction code for 5 of the 24
(the ones named below); the remaining 19 were not opened at the source
level and this item must not be read as having cleared them:

  CONFIRMED THE SAME FAULT SHAPE, two different ways it can arise:
  - 2019 attribution: the inner tool's cap is CORRECT and announces itself;
    the outer re-cap can still slice before reaching it (this item's own bug).
  - 2513 shape_files (both its _cap calls, 2532 and 2548): `tools/shape-check.py`
    imports capsay itself and its own `check()` caps embedded lists at
    `width=200, keep=4` WITH its own "(+N more of M)" clause (confirmed by
    reading tools/shape-check.py lines 30-45). verify.py's outer cap here is
    `width=90`, narrower than the inner tool's own per-item width of 200, so
    the outer cut can land inside an already-correct inner message before its
    count clause. Same fault, arising through a well-behaved inner tool this
    time rather than a careless one.
  - 1199 pc_watcher: `tools/pc-watcher.py`'s `selftest()` (confirmed as the
    enclosing function for the relevant line, and confirmed `--selftest`
    calls it) builds at least three FAIL-eligible messages from a RAW,
    UNCAPPED `", ".join(...)` with no count of its own at all (lines 587,
    598, 1061 of that file: `f"...{', '.join(sorted(TABLE))}"`,
    `f"...{', '.join(gone)}."`, `", ".join(missing)`). Nobody ever
    announces a count here, inner or outer; the outer width=110 cut is the
    only thing that touches this text at all, and it is silent about how
    much it removed.

  EXAMINED, DIFFERENT CONCLUSION FOR EACH:
  - 1142 voice_assets: `tools/stage-voice-assets.py`'s own `check(ok, what,
    got="")` (its local definition, not capsay) prints `got` verbatim with
    no capping whatsoever, and one call site feeds it an unbounded
    `"; ".join(missing)`. Latently the same shape as pc_watcher's; not
    confirmed to have actually bitten today, because the `missing` list in
    practice is small (a couple of filenames at most in the current tree).
  - 1161 voices_into_build: checked and NOT at risk from the code read.
    `tools/put-voices-in-build.py` does have raw `', '.join(...)` calls
    (lines 170, 226), but they are arguments to `say(...)`, an informational
    print, not to any `check(...)` call, so they never produce a
    "FAIL "-prefixed line and never reach verify.py's `bad` list. Recorded
    here so nobody re-spends the time checking it again.

  NOT EXAMINED AT THE SOURCE LEVEL (19 of 24, listed above by line number):
  502, 538, 584, 621, 697, 911, 1078, 1116, 1222, 1642, 1701, 2088, 2365,
  2495, 2669, 2678, 2704, 7421, 8238. Some of these are a different idiom
  entirely (1222 and 2495 read a dotnet/C# test runner's own summary, not a
  Python check() call) and may not share this shape at all; that is a guess
  stated as a guess, not a finding, because rule 3b applies to a "clear"
  claim as much as to a "found" one and none of these 19 has been opened.

## Not in scope

Do not widen or remove the outer `width=` caps blindly; an unbounded footer
line is the opposite fault (`ledger/verify.py`'s whole footer is one
comma-joined line, and one entry ballooning crowds out the other 92). The
fix likely has to make the OUTER cap aware of the INNER structure it is
re-cutting (for instance: cap the FAIL line's own already-capped tail
separately from its head, or raise the outer width past the inner tool's
own worst case and only then fall back to a character cut), rather than
either leaving today's blind character cut in place or simply enlarging its
number, which only moves the same failure to a longer list.

Do not fix this by hand at each of the 24 sites without first deciding the
one mechanism: this is exactly the "one idea, two implementations, and the
one nobody looks at is the one missing a line" shape `tools/capsay.py`'s own
docstring names as the reason it is a module and not a copy-pasted helper.
