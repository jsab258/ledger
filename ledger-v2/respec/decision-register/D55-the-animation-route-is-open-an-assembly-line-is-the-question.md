# D55. The animation route is open: an assembly line is the question, commissioned at stage 2 after the 3D line has produced something

CANON: none

Ruled by Jafar, 2026-09-21, first message, under "On bodies and movement, both
for stage 2", kept verbatim in
`game-design/decision-2026-09-21-the-week-after-the-reset-five-measurements-and-eleven-rulings.md`.
Written by the director the same day; the resident reviews and commits.

## The rule, as given

**"The animation route is not closed, and the earlier finding answered a
question I did not ask. The mocap topic was briefed on whether markerless
capture is viable, so it answered about licences and failure modes. My
question is whether an animation assembly line can exist the way the image
line does: a spec goes in, generation happens, an artifact comes out, it is
imported and verified, and nobody hand-animates anything. The pieces exist:
the image lane works, video models generate motion, MediaPipe and MMPose are
Apache 2.0 so our own or generated footage through an estimator is
unencumbered end to end, and Blender retargeting is scriptable and already on
the PC. The soft physics and sliding feet the research flagged in generated
video are a quality problem with known fixes, not a wall. The caveat is that
this would be a third generative line while the second is unproven. So the
route is recorded as open and commissioned at stage 2, after the 3D line has
produced something."**

## What is decided

- The route is OPEN. The earlier finding answered "is markerless capture
  viable" and is not a finding on "can an animation assembly line exist".
- The commission: at stage 2, after the MESH station has put one image through
  (queue 391 in the resident's log; "if it runs, the 3D line is complete for
  the first time"), an evaluation of an animation line in the image line's
  shape: spec in, generation, artifact out, imported, verified, nobody
  hand-animates. Its deliverable is one clip through the whole line with the
  verification printed, or the named break.
- His caveat is part of the ruling: "a third generative line while the second
  is unproven." The 3D line producing something is the gate, not a
  suggestion.

## The licence law comes before any footage goes through a model

CLAUDE.md: a new tool enters only through a decision record naming its weights
licence, and no tool checks this. "MediaPipe and MMPose are Apache 2.0" is his
statement from the research and is not verified here. THIS RECORD IS NOT THAT
DECISION RECORD: it commissions the evaluation. Before the first clip is
imported, each estimator and any video model used enters
`ledger-v2/research/license-allowlist.md` through a record naming its weights
licence. No video model is named here; none is on the allowlist by this record.

## What was checked, 2026-09-21

"markerless" occurs on main only in his message; "mocap" hits are v1
documents (`game-design/the-gap.md`, `production-plan-audio-art.md`,
`voice-casting-history.md`) and the KCD2 and RDR2 teardown. The finding he
overturns is in the research delivery on its branch; when the consolidation
lands it, its summary gets the mark under D43: "answered a question he did not
ask; D55 records the route as open". `production/stages.md` stage 2 says "The
register decides faces (D2) and nothing yet decides bodies": D46 decided the
bodies' source, and this record decides that the animation route is open and
evaluated, not what it is. `vision-pillars-v2.md` line 23, "Worse at ...
Animation parity with mocap studios", stands: an assembly line is not parity.

## What this does not decide

Which estimator. Which video model. The retargeting method. The order inside
stage 2 beyond his one constraint (after the 3D line has produced something):
D44 gives the rest to the studio.
