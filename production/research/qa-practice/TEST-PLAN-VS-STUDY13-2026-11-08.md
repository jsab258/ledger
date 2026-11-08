# Test plan against Study 13 (8 Nov 2026)

For n09-9; nothing decided. Read 8 Nov 2026: production/research/aaa-reference/studies/13-pipeline.md (S13), TEST-PLAN-PHASES-2-3-2026-11-08.md (PLAN), QA-LEAN-PROPOSAL-2026-11-07.md (QA). Rule used: a check is added only when a fault slipped past (PLAN line 3).

S13 is about folders, naming and tuning data. It holds no number on performance or memory budgets, no build gate and no test method; its "Open blind spots" (line 84) say Mafia's source-side checks do not ship. So only the points below touch testing.

| # | (a) What S13 found | (b) Plan covers? | (c) If missed: evidence of a fault class? |
|---|---|---|---|
| 1 | Naming slips in Mafia: 16 prefixes written two ways, one misspelt table row; "A check would catch both" (line 42; table line 19). Mafia's slips are few. | Misses. PLAN check 2 (asset checks) lists stale imports, placeholders, JPEG normals, triangle overruns; no names. | None in LEDGER. S13 measures 23% prefixed (lines 8, 18) but names no fault it caused. Mafia's slips are measured, not shown to have broken a build. |
| 2 | Adopt a naming rule with a CI check; "Rules alone have not held (CLAUDE.md)" (lines 69 to 73). | Misses. | Weak. The line is a general claim; no slipped fault is cited. |
| 3 | Adopt: a check fails the build when a spec's number is also a C++ constant (lines 64 to 67); about 220 C++ and 356 C# constants (line 25). | Misses. The duplicate-number check is not in PLAN section 1. | None. S13 gives counts, not a case of a spec and a constant disagreeing. |
| 4 | LEDGER specs are checked against their homes by homes_check.py and the spec tests (line 59). | Partly. PLAN check 1 names ci-checks and gates (CoreTests to StrangerTest, canon, reach-check) but not homes_check.py or the spec tests. Whether ci-checks runs them: unverified. | Not a miss if ci-checks runs them; the plan only fails to name them. |
| 5 | Kingdom Come II tables are schema-checked, 1,243 tables, 13 schemas (lines 6, 57); 8 tables do not parse (line 86). | Partly. Spec tests (line 59 above) are the nearest LEDGER match; the plan does not name them. | None. No LEDGER fault from an unparsed spec is cited. |
| 6 | Mafia's asset-registry tags such as asset status and validation hint at source-side checks (line 84, tag N, a name only). | Misses. | None. A name only; S13 does not read what they check. |
| 7 | Settings as data: 22 hard-coded lines (lines 23, 74). | Not a test point (a build item); PLAN section 4 has nothing to cover. | No. |
| 8 | Performance and memory budgets; what a build must pass before people see it. | Not in S13. PLAN checks 1 to 7 stand on their own sources (QA, STEPS, MEMORY-PLAN). | Not applicable. |

Also: PLAN line 58 lists S13 as "not reached"; it has now been read.

## Proposed changes to the test plan (at most three)

1. Correct PLAN section 5 (line 58): S13 is now read, and its testing points are rows 1 to 6 above (S13 lines 42, 59, 64 to 73, 84).
2. Under PLAN check 1, name homes_check.py and the spec tests as part of ci-checks, if the session confirms ci-checks runs them (S13 line 59; unverified).
3. Add to PLAN section 4 ("Dropped or not added"): the naming check and the spec-number-equals-constant check, both proposed by S13 (lines 64 to 67, 69 to 73), not added because no fault has slipped past; to be reconsidered if one does.
