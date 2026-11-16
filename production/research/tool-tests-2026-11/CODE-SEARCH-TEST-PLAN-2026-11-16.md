# The code-search test for Kiln's fixers: plan (16 November 2026)

For n16-1 (order of 16 Nov; advisor 166, his pick A of 15 Nov 07:59): a code-search tool for fixers, licence first or one we have; two rounds with it and two without; kept only if cheaper at the same quality.

Reference: none found in the studies (a tooling question, not a game method).

Method researched: KILN-ROUND1-2026-11-13.md (rounds 7 to 9: fixers' time went on finding where a check or a solver step lives; round 9's fixer spent 20 minutes and made no drape run).

## The tool

- Chosen: **ast-grep** (structural search over syntax trees, a command-line tool, Rust supported). Licence read 16 Nov 2026 at https://raw.githubusercontent.com/ast-grep/ast-grep/main/LICENSE: MIT, "Copyright (c) 2022 Herrington Darkholme". A fixer calls it through its shell; nothing ships.
- What we already have: plain text search (the fixers' built-in search, ripgrep underneath). That is the "without" arm.
- Not chosen: Serena, a symbol-lookup server; its licence page (read 16 Nov 2026, https://raw.githubusercontent.com/oraios/serena/main/LICENSE) puts v2 and later under GPL-3.0-or-later, with only releases up to v1.7.0 under MIT. An old MIT release would be the second candidate only if ast-grep shows no gain.
- Install: into F:/LedgerTools (never C:), by pip (`ast-grep-cli`) or its release binary, when the first "with" round is due; licence recorded in Kiln's CREDITS.md as a tool used, not code reused.

## The test (runs inside Kiln's share after the 13:00 reset, not before)

1. Four fixer rounds on real Kiln work, alternating: without, with, without, with, so no arm gets all the easy rounds. Same agent (one fresh Opus fixer), same brief template; the "with" brief adds two lines on ast-grep and one example.
2. Measured per round, from the run itself: tokens and wall time to the first code change; tokens and time in all; number of files read whole; whether the fix met its acceptance case on the judge's run (quality).
3. Rule: kept only if the two "with" rounds cost at least 15% less in tokens than the two "without" at the same pass rate; anything less is noise at four rounds and the tool is dropped, one line in DECISIONS.
4. Its own time-log windows: "tool loop: kiln code-search round n".

Estimate (unmeasured): about 1 h of setup and reading spread over the four rounds, which run anyway as Kiln work.
