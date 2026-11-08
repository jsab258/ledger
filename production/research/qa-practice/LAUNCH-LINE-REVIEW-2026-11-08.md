# Launch line (QA step 2), fresh review, 8 Nov 2026, commit 2cad25a44

Verdict: PASS WITH FIXES (one narrow fix, not blocking).

Checked, all as the spec says:
- launch_line_check.py: last_command_line() and describe() match the spec. Self-test 16/16 (10 cases + 1 + 5 new). nightly_walk.py self-test 18/18.
- Real logs through describe(last_command_line(path)): the 4 Nov office log reads "a test launch: -mickeysinside" (the exact fault); the 7 Nov backup log reads "PLAYER+WATCH (talk is the stand-in: the run says nothing about talk)". Both as planned.
- from_log: only callers are launch_line_check.py:148 (self-test) and :167 (its CLI). Function untouched; still returns the first line.
- Old verdicts: nightly_walk.py launch_sentence() returns "not recorded (a walk from before 8 Nov)" when the key is absent, "no walk" when there is no verdict. A stored None reads "launch line not found". The paragraph line appears whenever a sentence exists.
- Never fails the walk: route_walk.py:331-336 wraps import and read in try/except Exception, and last_command_line() itself returns None on OSError. launch_sentence() sits outside any try in nightly_walk, but it only calls describe() on a string or None; judge() on odd text is the only unguarded step (not seen to raise).
- Log path: self.saved is PACKAGED_SAVED (F:/LedgerTools/played-game/Windows/LedgerProbe/Saved) or the editor's, set at route_walk.py:525 and passed to Route(). Same file the class already reads at :179 and :242. UE rotates the previous run to LedgerProbe-backup-*.log at start, so the live file is the latest launch, the Continue.

Fault (narrow):
1. tools/route_walk.py:334 and :526-530. walk() deletes route-checks.jsonl and route-where.txt before starting but never the log. If the first launch fails and walk() returns early through write() (lines 538/542), Logs/LedgerProbe.log is the previous run's, and its launch line is reported as this walk's. Failing case: the packaged game does not start tonight, last night's log has "-RouteWalk" only, and the report says "The walk ran on: PLAYER+WATCH". Fix: compare the log's modified time with the walk's start and store None (or "stale") when older.

Not changed: no repository file edited.
