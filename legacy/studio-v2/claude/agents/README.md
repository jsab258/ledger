# Agent roster (v2 mapping)

ledger-v2/studio-v2/organization.md defines the departments. Roles here are
minted when their department first has work (waste rule: nothing built ahead
of need). Current files:

- v2 roles: planner, integrator, dialogue-writer (Phase 0 pilot needs these)
- producer (tier 1, minted 2026-09-03): the ONLY role that addresses Jafar.
  Its register is ruled and `tools/producer-check.py` enforces the
  mechanical half; routing classes are `production/interrupt-classes.md`.
- v1 roles kept and still valid where their function survives: the tier 2
  verifiers (measurement-auditor, claim-auditor, artifact-reader,
  guard-tester, reach-auditor) map to Verification; the tier 3 builders
  (systems-builder, instrument-builder, engine-specialist, content-wrangler)
  map to Engineering and World; studio-director maps to Direction.
- Not yet minted (no work yet): casting, rigs, audio, brand-bible keeper,
  watchdogs, judges (judges wait on the D7 calibration sample).

Standing constraints live INSIDE each role file, never in task briefs
(waste lesson 2).

Every definition carries a `## Budget and lessons` section: the frontmatter
`maxTurns` restated in prose, so the agent and the dispatcher both see the
number at the moment of dispatch (a number only the YAML held was declared and
never read through eight turn-limit deaths on 2026-09-16), plus
`lessons=N/N/N` naming the waste lessons that bite that role. A role touched by
none writes `lessons=none-apply`: silence and none are different facts.

Each section also prints `Observed spend` from `.claude/agent-turns.tsv`
(n, median, peak) beside the declared ceiling, so a ceiling nobody has checked
against real runs cannot read as a measured one. TWO CAVEATS, both load
bearing. The log's unit is a TRANSCRIPT TURN counted by `tools/spawn-cost.py`,
and whether that equals one `maxTurns` unit is UNSETTLED here: 8 of the 15
roles show a peak above their own declared ceiling, which is impossible if the
two units match and the ceiling is enforced. Until `tools/spawn-cost.py`
settles the unit, read the pair as a comparison of the same role against
itself over time, not as proof a spawn was cut off. And a role with 0 rows
prints the words "nothing measured": its ceiling is a shape guess.
