# Marvelous bridge auto-start: the self-recovering fix (16 November 2026)

Method researched: BRIDGE-AUTOSTART-DIAGNOSIS-2026-11-16.md (sections 2, 5 and 6), with BRIDGE-START-TIMEOUT-2026-11-16.md.

Written under his pick A of 16 Nov (advisor 174, DECISIONS 12:39: the start recovers by itself). Code written and checked offline only. No click, key or UI Automation call was made, no window was sent a message, no process was started or stopped, and start_bridge.ps1 was not run in its acting mode.

## Files changed
- tools/md-bridge/start_bridge.ps1 (rewritten, 475 lines). Header 1-44 gives the reasons. Switches at 45: -DryRun, -SelfTest, -AllowRestart (off by default). Logging and Finish at 67-84: every outcome goes to starts.jsonl, including the two results the old script left out. The copy picker at 88-105: the copy the heartbeat names (field `pid`), else the copy recorded in marvelous.pid (process id and start time must both match), else the only copy running. If several copies run and none is named, nothing is done. The window classifier at 107-123: the main window is the visible window with no owner whose class ends in QWindowIcon. The Welcome window is owned by it, has a class ending in QWindowOwnDC, a "Marvelous Designer" title and a smaller size. If the main window is disabled under any other window, the start stops. The restart guard is at 125-133 and the self-test (17 cases) at 135-179. The read-only Win32 listing is at 183-223 and the dry run at 259-290. The lock (start.lock) is at 301-311. The restart path is at 326-350: only the task's own copy, in which no bridge or job ever ran and no window is open over it, at most once in two hours; it is asked to close (CloseMainWindow), then stopped after 60 s, and only that one process. The settle step and the Welcome close are at 352-378: WM_CLOSE, at most three rounds 5 s apart. UI Automation starts from the window handle (FromHandle), tries Invoke with the menus shut, and falls back to Expand (379-475).
- tools/md-bridge/open_marvelous.ps1, lines 39-54 and 61: launches with -PassThru, waits on its own copy, writes marvelous.pid, and sets LEDGER_MD_IN_TASK=1.
- tools/md-bridge/md_job.py, lines 27-29: START_TIMEOUT_S = 180, with the reason. Lines 46-58: TimeoutExpired is caught. Lines 104-109: two new self-test cases.

## Not written
- The keyboard-accelerator route. RULINGS 1 Nov rule 7 and his 29 and 30 Oct rulings exclude simulated keys, and the diagnosis marks that route excluded.
- RULINGS line 29 (30 Oct) still says "nothing else". Closing the Welcome window and the restart go beyond it, so the session should bring that line into agreement before the live test.
- A one-line change to ledger_md_bridge.py, `"pid": os.getpid()` in the heartbeat at lines 97-98 and 142. This file was outside the brief. Until it is made, the heartbeat cannot name its copy.

## Checks run
- `start_bridge.ps1 -SelfTest`: 17 of 17 pass. `md_job.py --selftest`: 6 of 6 pass.
- `start_bridge.ps1 -DryRun` at 14:22 (read-only; starts.jsonl was unchanged afterwards):
  - Four copies were running: 3988, 5736, 6292 and 23092.
  - Target: none. The heartbeat names no copy and marvelous.pid does not exist.
  - It would do nothing in any case, because the heartbeat was alive (4-5 s old).
  - In 6292 and 23092 it would close the Welcome windows 0x4112A and 0x11010 (owned, Qt6103QWindowOwnDC, 960x550).
  - Every main window was Qt6103QWindowIcon, 2079x1251, and enabled. So the Welcome window is not modal.

## Untested
- Whether Marvelous accepts WM_CLOSE on the Welcome window and the window stays closed.
- Whether the Invoke works with the menus shut in Qt 6.10.
- The menu-bar walk from the window handle.
- The lock, the restart path and the in-task launch.
- Whether a 60 s settle is enough.

## Live test (the session's)
Two conditions first: only one Marvelous copy open (his copies are his to close), and the bridge's heartbeat stale. Then:
`powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/md-bridge/start_bridge.ps1 -DryRun`
then `schtasks /run /tn "LEDGER Marvelous open"`. After that, read opens.jsonl and starts.jsonl.
