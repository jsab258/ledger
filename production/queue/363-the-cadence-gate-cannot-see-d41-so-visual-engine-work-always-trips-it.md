line: instruments (ledger/verify.py's director_cadence, DIRECTOR_WORK and the
  D45 scope constants)
spec: D41 says VISUAL WORK IS UNGATED: the grade, the sky, lighting, post,
  materials, decals, props and camera get no director, no written predictions
  and no ruling records. `director_cadence` implements D45's path split
  (`d45Gated=scripts/ledger/ueprobe/content`) AND NOTHING OF D41's. A path
  cannot tell a grade constant from a schema change, so EVERY visual change
  that lives in the engine trips a gate D41 says should not apply to it.

  THREE INSTANCES IN ONE DAY, 2026-09-16, and the count is the finding:
    the lamp drive          GATED, and it WAS structural (a schema field). Right.
    the sky dome            GATED, and it WAS structural (a field, two tools,
                            a workflow change). Right.
    the sky luminance       GATED, and it is NOT: no schema change, no new
                            tool, no workflow change, one renamed constant and
                            a drive built on two existing precedents. A wrong
                            value is undone by the next render, which is
                            Jafar's own boundary for visual, word for word.

  So the gate was right twice and wrong once, and it cannot tell the cases
  apart because the only thing it reads is the path.
acceptance: either the gate can distinguish the two (and whatever distinguishes
  them is a thing the tree can READ rather than a judgement a commit message
  asserts), or the gate says plainly in its own printed line that it gates by
  PATH and not by D41's boundary, so a reader stops expecting it to
  max_sessions: 1
status: READY 2026-09-16, filed and NOT started, under Jafar's standing rule:
  a finding is filed and the standing order resumes.

  THE OBVIOUS FIX IS PROBABLY WRONG AND IS NAMED SO NOBODY REACHES FOR IT. A
  marker in the commit message, or a flag the resident sets, makes the gate
  satisfiable by assertion, which is the spawn-row hole this project already
  closed once: `organization.md` records that `director_cadence` used to be
  cleared by a SPAWN rather than a completed review, and the fix was to require
  an artifact. A "this is visual" flag would reopen exactly that, one layer up.

  WHAT MIGHT ACTUALLY READ. The tree knows some of it already: a change that
  touches no `.h` in the tested headers, adds no condition field, and changes
  no file under `production/specs/` or `.github/` is a strong candidate for
  visual. That is a hypothesis with three parts and no series behind it, which
  is why this is an item rather than a patch.

  THE HONEST INTERIM, and it costs a director spawn each time: keep gating and
  let the director rule quickly that a visual change lands. That is what
  happened today on the third instance, and the ruling record says in one line
  that no ruling was needed. A cheap wrong answer beats an expensive right one
  only until somebody starts skipping the spawn.
