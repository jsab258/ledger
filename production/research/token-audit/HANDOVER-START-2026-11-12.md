Method researched: the scheduled-tasks tool's own documentation (list_scheduled_tasks: "waiting ... means that a run is due and has not started, and names what holds it"; read 2026-11-12 23:58) and the task's run list (list_task_runs, 25 runs, read 2026-11-12 23:58)

# A handover that starts the next session at once (advisor "eff", 12 Nov 2026, item 1)

## Questions
1. Why does a handover wait about 15 minutes when the start runs every 15 minutes and the gate needs only 3 quiet minutes after a written stop?
2. Which documented way starts the next session at once, and is it within the session's own tools (the gate, the task's launcher) or his?

## What was measured
- The task: "Every 15 minutes", cron */15, jitter 369 s; its runs start at :06:5x, :21:5x, :36:5x and :51:5x each hour (25 runs read).
- While a session of this task works, the task shows "waiting: per_task_limit": the run that falls due is held, not dropped.
- The held run starts as soon as the working session ends: 17:23:41 after the 17:06 session's last activity at 17:22:53 (48 s); 19:34:43 after the 19:21 session's at 19:34:12 (31 s).
- Both held runs ended in seconds: the gate read "a session wrote a turn under 3 minutes ago" and said WAIT. The next session began at the following quarter.
- Idle by cause, 11 Nov 19:00 to 12 Nov 19:00 (tools/idle_gaps.py): handover waits 336 day minutes in 7 gaps, of which 4 gaps (15, 14, 14, 18 min, 61 in all) were this wait, and 3 (127, 129, 33) the pace hold catching stops that had his priority items open (fixed the same night, advisor 126).

## Answer
1. The held run arrives 30 to 50 s after the stop, the gate's 3 minutes refuse it, and the next run comes about 15 minutes later.
2. The way already exists and is the session's own: the task's one-run-at-a-time hold starts the next run at once; only the gate's quiet time stood in the way. No setting of his is needed, no session starts another (his rulings of 3, 4 and 11 Nov hold), and the schedule is untouched.

## Change made (tools/fresh_gate.py)
- Quiet time after a written stop 3 minutes to 18 seconds; 15 minutes still when no Stopped line is written. The self-test's two cases moved with it (10 s: WAIT; 30 s: GO); 46 of 46 pass.
- Why 18 s is safe: the held run starts only after the old run has ended, so its start shows the old session is done; 18 s keeps out a closing turn still being written. Another session he resumes by hand still counts by its turns.

## Expected saving and how it is read
- About 14 minutes per handover: 4 to 6 handovers a day, so about 55 to 85 minutes a day now, more in the double week. Target under 10 minutes a day in the handover-wait column (tools/idle_gaps.py), read Monday and Thursday.
- First proof: this session's own stop (12 Nov, about 00:10): the held run should read GO within a minute.

## Not reached
- The scheduled-tasks documentation does not state the per-task hold's behaviour in words beyond "waiting"; the behaviour is measured from two runs only.
