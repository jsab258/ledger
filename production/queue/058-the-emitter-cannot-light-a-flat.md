line: production (the Unreal emitter)
spec: this file, ordered by the 3 September ruling
acceptance: the emitter can light a flat as well as a shop bay, and the verdict distinguishes "no flats asked for" from "flats asked for and not lit"; today it prints flatsLit=0/0 nothing-to-light, which is correct now and becomes a lie the moment a flat is added
max_sessions: 1
status: CLOSED 2026-09-10, not on the ladder, BY COMMIT cd55a79c (subject: D18 lands at five sites, 510 files are archived and nothing is deleted). No ruling named this closure; see production/queue/275. Reviewed 2026-09-14 against production/stages.md and not reopened. and untouched for 7 days 2026-09-03. engine-specialist, small.

## The finding

`flatsLit=0/0 nothing-to-light` is exactly the right shape for a zero: it
carries its denominator and it says in words that nothing was measured rather
than reporting a clean result. The hole is behind it. The scene has no lit
flats to ask for, so the path has never run, and the first flat added will
exercise code nothing has executed.

Filed while the zero is still honest, which is the cheapest moment to file it.
