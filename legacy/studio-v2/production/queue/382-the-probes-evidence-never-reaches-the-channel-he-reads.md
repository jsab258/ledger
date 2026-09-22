line: instruments and reporting, jointly (CLAUDE.md rule 12)
spec: RAISED BY JAFAR 2026-09-17 WITHOUT KNOWING IT WAS STRUCTURAL. His words:
  "Run 53's verdict carries no figure keys, so find out whether it landed at
  all, and if it did not, re-dispatch."

  RUN 53 LANDED AND THE KEYS EXIST. `production/d1-probe/ue-vignette-verdict.txt`
  line 1 names `61e46c4`, the commit the probe measured, and the file carries
  50 mentions of `figure` including `figure=STANDING` and
  `figureMeshHeightCm=166.50`. The landing commit is `4696d113`, "UE machine
  probe from 61e46c4e". No re-dispatch was needed and none was made.

  HE IS RIGHT ABOUT WHAT HE CAN SEE. `grep -rl "figure=" game-design/sim-shots/`
  returns NOTHING. `STATUS.md` and `dashboard.html` carry six hits for the word
  "figure" and every one is incidental: a queue filename, and the word used to
  mean a number. So the figure verdict appears in NO channel he reads.

  AND IT IS NOT A BROKEN STEP, WHICH IS THE PART THAT MAKES THIS AN ITEM.
  `game-design/sim-shots/runs/` is written by `tools/sim-shots-commit.sh` and
  read by `tools/glance.py`: that is the UNITY SIM pipeline. The UE probe
  writes to `production/d1-probe/` and nothing has ever copied between them.
  `game-design/sim-shots/verdict.txt` still names `cb4767e` at an epoch about
  two weeks old, which is the sim's last word and not the probe's.

  SO CLAUDE.md RULE 12 IS HALF TRUE AND NOBODY NOTICED. It says the channel
  that works is a file committed by CI under `game-design/sim-shots/`. That is
  true of the sim and false of the probe, and the probe is where every visual
  result of the last fortnight lives. FIFTY THREE RUNS HAVE REACHED HIM ONLY
  BECAUSE A SESSION READ THE RAW FILE AND COMPOSED A PICTURE BY HAND. Remove
  the session and the channel is dark.
acceptance: a probe run's own verdict line reaches the glance or the dashboard
  without a session composing anything, with the accepting case (a run with
  figure keys shows them) proven first and the never-ran case printing the
  words rather than a stale run's keys; and CLAUDE.md rule 12's sentence names
  both channels or names the right one
max_sessions: 1
status: READY 2026-09-17, filed and NOT started. His standing order is that
  nothing filed starts before the reset, and this is filed.

  WHAT MUST NOT BE DONE: copying the probe verdict into `sim-shots/` so the
  grep succeeds. Two pipelines writing one directory is how a run carries
  another run's evidence under its own name, which `.claude/rules/ci.md`
  already forbids in as many words. The probe needs its own row in the place
  he looks, not a squatter in the sim's.
