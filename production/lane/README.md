# The lane (16 to 23 November 2026 only)

A second Claude session that does only machine-free work, beside the main production session (his picks of 17 Nov about 16:05, advisor 202; RULINGS "7, 10 Nov" and "3, 4, 11 Nov").

- Where: its own sparse worktree, C:\Users\Jafar\ledger-lane, branch lane (text folders only, about 95 MB; pushes refused by its own setting). On F: only F:\LedgerTools\lane-research. Both are on production/storage-map.json.
- Start: the scheduled task "LEDGER: the lane session", hourly; its prompt is SCHEDULED-TASK-PROMPT.md, its setup SETUP-STEPS.md.
- Gate: tools/lane_gate.py reads only the lane's handover and the lane's own session logs; the main gate never reads the lane. After 2026-11-23 07:00 it says LANE STOPPED.
- Handover: LANE-HANDOVER.md (Started, Stopped, the rules, the queue, lines for the merge).
- Merge: the main session merges branch lane into wip at its item ends and appends the handover's "For the merge" lines. After the end, the main session removes the worktree (git worktree remove; Claude made it) and records one line.
