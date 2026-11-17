# Setting up the lane task (about two minutes, at the PC)

## Before he starts (the main session does this, not him)
1. Commit tools/lane_gate.py and production/lane/ on wip (with storage-map.json's two new lines).
2. In C:\Users\Jafar\ledger-lane run `git merge --ff-only wip`, so the lane's branch has the gate and the lane handover.
3. There, run `python tools/lane_gate.py`: it must print a line beginning "LANE GO no lane session has started yet".
4. Put the steps below on his page as one ACTION item, with this file's prompt text attached.

## His steps (at the PC itself: a task made from a phone loses its permission setting)
Labels marked "(label may differ)" could not be checked from here; the nearest matching button is the right one.

1. Open the Claude app on the PC.
2. Click "Scheduled" in the left sidebar (label may differ: "Scheduled tasks").
3. Click "New task" (label may differ: "New scheduled task" or a "+" button).
4. In the name box, type: LEDGER: the lane session
5. In the folder box, choose: C:\Users\Jafar\ledger-lane (label may differ: "Working folder" or "Project folder").
6. Set how often it repeats to: Hourly (label may differ: "Repeat" or "Frequency").
7. Set the model to: Opus 5.5.
8. Paste the prompt: the text between the two lines in SCHEDULED-TASK-PROMPT.md (the main session gives it to him on his page, ready to copy).
9. Set permissions to: automatically approve (label may differ: "Auto" or "Permission mode: Auto").
10. Click "Save" (label may differ: "Create").

## Afterwards (the main session)
- At the next hour: the task's first run should show under Scheduled, on the task's page, and production/lane/LANE-HANDOVER.md in C:\Users\Jafar\ledger-lane should carry a Started time. If it does not, say so in that hour's row.
- The main gate is unchanged: tools/fresh_gate.py reads only the main project's logs, so the lane never holds the main session.
- The task stops being useful at Monday 23 November 07:00 (the gate then says LANE STOPPED and each run ends at once). Turning the task off after that is his (one ACTION item that day).
