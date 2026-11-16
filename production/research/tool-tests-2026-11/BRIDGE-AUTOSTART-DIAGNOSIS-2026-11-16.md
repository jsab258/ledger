# Marvelous bridge auto-start: diagnosis and a self-recovering design (16 November 2026)

Method researched: this note's own sources section (UI Automation on Qt menus, Python's site start-up hook; https://docs.python.org/3.11/library/site.html), read 16 Nov 2026.

Diagnosis only. No project file was changed apart from this report. Nothing was clicked or typed. No UI Automation pattern was invoked, no bridge script was run, and no process was started or stopped. Marks used: **D** documented or measured, **I** inference, **U** unverified. Every web source was read on 16 Nov 2026.

## Questions
1. Is the record of the failure itself right? (Was it really "UI Automation timed out twice"?)
2. What stood between the script and the menu item on 16 Nov, and why did 9 Nov work?
3. How does UI Automation reach a Qt 6 program's menus, and does a fresh Qt window really have no tree until it is switched on?
4. Which start routes need no clicks (a start-up script, a Python start hook, command-line options, the plug-in's own settings)?
5. What design keeps working unattended (dismiss a stray window, restart Marvelous in his signed-in session, retry, otherwise go on without the bridge)? How can it be tested with nobody at the PC?

## 1. Was the measure wrong? Yes, in four places

- **Only one of the task's three tries timed out.** F:/LedgerTools/md-jobs/opens.jsonl (16 Nov) shows: bridge-1 10:20:27 "FindFirst ... Operation timed out"; bridge-2 10:25:30 and bridge-3 10:30:26 "no 'Plugins' menu in Marvelous's menu bar". Those two runs searched the whole tree (each took about 4.5 minutes) and found **no** "Plugins" item. starts.jsonl leaves those runs out because start_bridge.ps1:115 (and :95) write their outcome without `-log`. The handover ("timed out", line 46) and DECISIONS 10:25 follow starts.jsonl, so they record the wrong failure (D).
- **The window log cannot see a second window.** open_marvelous.ps1:31 logs `Process.MainWindowTitle`, one title per process. DECISIONS 10:25 concluded "its only visible window is the main one, no dialog" from that log. Marvelous's Welcome window carries the **same title** ("Marvelous Designer Personal") and is a separate window owned by the main window (section 2). That log could never have named it. The file's own claim "a dialog in the way is named, not guessed" (open_marvelous.ps1:11-12) does not hold (D for the title; I for the .NET main-window rule, whose source was not reached, see the end).
- **The test runs overlapped.** The direct start_bridge.ps1 run ("hung past 6 minutes", DECISIONS 10:25) ran during the task's bridge-2 (10:20:57 to 10:25:30). The hand-run children-only walk at 10:27:59 (starts.jsonl) ran during the task's bridge-3 (10:26:00 to 10:30:26). So two UI Automation clients were working on one Marvelous at the same time. Those results are not clean evidence (D for the times; harm from the overlap U).
- **The current start_bridge.ps1 cannot finish inside its caller.** start_bridge.ps1:92-93 sleep until Marvelous is 120 s old. md_job.py:51 kills the call after `timeout=90`, and `subprocess.TimeoutExpired` is not caught (md_job.py:50-53). The first `md_job.py --start` after a fresh launch will therefore crash md_job (D, from the code; not run).

The premise "a fresh Qt window has no menu tree until accessibility is switched on" is also only half right. In Qt 6.10 the first UI Automation request both switches accessibility on and is answered in the same call (section 3) (D).

## 2. The cause

### Cause A (high confidence on the facts, medium on the exact path): the Welcome window was open on the fresh Marvelous

Evidence:
- The advisor saw it when starting the bridge by hand at 12:45 today: the Welcome window was open, and it came back once after being closed (coordinator's message, 16 Nov).
- A read-only window listing of the running processes, taken by this helper at about 13:02 (Win32 EnumWindows, GetClassName, IsWindowVisible, GetWindow owner; no UI Automation, no input). Four Marvelous processes are running: 5736 (the task's launch, 10:18:55), 23092 (12:30:26), 6292 (12:30:46) and 3988 (12:43:15). In both copies nobody has touched (23092, 6292), one visible window sits directly above the main window in the stacking order. It is owned by the main window, class `Qt6103QWindowOwnDC`, 960 x 550, titled "Marvelous Designer Personal", the same title as the main window. In 3988, the copy the bridge was started in by hand, that window is gone (D, measured).
- `OwnDC` in a Qt window class means an OpenGL surface (qtbase 6.10 qwindowscontext.cpp:540-543, 580-581). Marvelous keeps a QtWebEngine profile named `welcomeProfile` (C:/Users/Jafar/AppData/Roaming/CLO Virtual Fashion/Marvelous Designer Personal/QtWebEngine/welcomeProfile). Qt's UI Automation helper carries a special case for "WebEngineView not knowing its parent" (qwindowsuiautils.cpp:33-35). Together these point to a web page inside its own window (I).
- `Qt6103` in the class names is Qt 6.10.3 (qwindowscontext.cpp:511-516 builds the prefix from the major, minor and patch numbers) (D).

Why this breaks the script (I; the exact path is U because the run never logged which element it held):
- start_bridge.ps1:94 takes `RootElement.FindFirst(Children, ProcessId)`, "the first window of Marvelous's process", and calls it the main window. Two paths lead to failure, and both are removed by the same fix:
  1. If the desktop lists the Welcome window first (it is higher in the stacking order), the search ran inside the Welcome page. That fits all four 16 Nov results: no "Plugins" item (bridge-2, bridge-3), no menu bar among its children (10:27:59), and slow or timed-out searches. A web page's accessibility tree is built across processes once it is switched on (U for this Marvelous).
  2. If UI Automation lists the owned Welcome window under the main window, as FlaUI assumes when it looks for modal windows among a window's descendants (FlaUI Window.cs, `ModalWindows`, lines 49-57), the whole-tree search walked into the web page. That explains the timeout and the minutes-long walks, but not the 1-second "no menu bar" answer from the children walk.
- 9 Nov worked 21 s after launch (opens.jsonl). Whether the Welcome window was not shown that day, or appeared later than the search, is not logged (U).

### Cause B (medium): Windows' Start menu or Search held the front all morning

- Every 16 Nov line in opens.jsonl reads `"front":"Search"`, from 10:18:55 to 10:30:26. On 9 Nov the front became "Marvelous Designer Personal" at 09:04:41 (D). The advisor found a Start menu left open in front of Marvelous at 12:45 (coordinator's message).
- So Marvelous never came to the front. The script opens the menus with Expand (start_bridge.ps1:116, 119). Whether Qt keeps a popup menu open in a program that is not in front was not found in the Qt source read (qwindowscontext.cpp has no popup-closing rule for deactivation in the lines searched) (U). The advisor's mouse click on the menu item fell through to the pattern toolbar underneath, so the open menu was not taking input normally while the Start menu was up. The keyboard route worked (coordinator's message) (D for the report; how it applies to Expand and Invoke is U).

### Cause C (certain as a hazard, not a cause on 16 Nov morning): several copies of Marvelous

- Four copies run now, all with the same window size and position, stacked on top of each other (D, listing above). Only 5736 existed at 10:20 (its own temp folder is the only one from that morning) (D).
- start_bridge.ps1:36 takes `Select-Object -First 1`, which is the lowest process number, not the copy the task opened or the one that holds the bridge. The heartbeat names no process (ledger_md_bridge.py:97-98). Two bridges would both read one inbox with no lock (ledger_md_bridge.py:103-105) (D, code). Four copies also hold memory on the card; the CLAUDE notes say Marvelous takes about 6 GB.

### Smaller faults found
- register_marvelous_task.ps1:10 stops the task after 15 minutes. On 16 Nov open_marvelous.ps1 ran 11.5 minutes (10:18:55 to 10:30:26). With the new 120 s wait, three tries can pass the limit (D times; I outcome).
- open_marvelous.ps1:52 waits 20 s after the window appears, then start_bridge.ps1 waits up to 120 s more. The two waits overlap without either knowing about the other (D).

## 3. How UI Automation reaches Qt menus (research)

- Qt 6.10 answers UI Automation itself. On the first `WM_GETOBJECT` it calls `accessibility()->setActive(true)`, then returns a provider for the window's accessible root. It ignores requests only while the program is starting up or closing down. https://raw.githubusercontent.com/qt/qtbase/6.10/src/plugins/platforms/windows/uiautomation/qwindowsuiaaccessibility.cpp lines 38-56 (D). So no separate warm-up step is needed: the first request is answered. The 120 s settle wait added on 16 Nov rests on a misreading (I).
- Qt maps menu bars to `UIA_MenuBarControlTypeId`, menu items to `UIA_MenuItemControlTypeId`, plain widget containers (`Client`) to Group, and anything unlisted to Custom. https://raw.githubusercontent.com/qt/qtbase/6.10/src/plugins/platforms/windows/uiautomation/qwindowsuiautils.cpp lines 91-158 (D). The four-level walk at start_bridge.ps1:99-112 skips ToolBar, TitleBar and Tab containers. If Marvelous's bar sits under one of these, the walk misses it (I; the current tree was not inspected).
- Microsoft: the root of the tree is the desktop, its children are application windows, and the tree is built as a client asks for it. https://learn.microsoft.com/en-us/windows/win32/winauto/uiauto-treeoverview (D). The page does not say in which order the desktop's children come back (U). `AutomationElement.FromHandle(hwnd)` gets the element for one known window directly. https://learn.microsoft.com/en-us/dotnet/api/system.windows.automation.automationelement.fromhandle (D).
- Earlier research (BRIDGE-START-TIMEOUT-2026-11-16.md) covers the timeouts (connection 2 s, transaction 20 s), the cost of searching the whole tree, and slow Qt providers. Nothing here contradicts it. That note did not have the Welcome window and missed bridge-2 and bridge-3.

## 4. Routes that need no click

| Route | Finding | Status |
|---|---|---|
| Marvelous's documented start-up script or auto-run | The developer site's plug-in page describes registering a .py in the Plug-in Manager and launching it "directly from within Marvelous Designer". It says nothing about running on start. https://developer.marvelousdesigner.com/register.html (D, by absence). The 26 Oct, 8 Nov and 1 Oct notes found the same. | none documented |
| The plug-in's own "run on start" setting | pluginSettings.json (C:/Users/Public/Documents/MarvelousDesigner/Plugins/pluginSettings.json) holds title, file, menu path, position and source type, and no start flag (D). api_plugin_log.txt shows a plug-in loads only on "User clicked to run a plug-in action" (D). | none found |
| Python's own start-up hook inside Marvelous (a `.pth` line or `sitecustomize.py` in its site-packages) | Standard Python runs these when the `site` module runs at interpreter start. https://docs.python.org/3.11/library/site.html; an embedding program can switch this off (`PyConfig.site_import`), https://docs.python.org/3.11/c-api/init_config.html (D). In Marvelous's Python (C:/Users/Public/Documents/MarvelousDesigner/Configuration/python311) the existing `distutils-precedence.pth` would import `_distutils_hack` whenever `site` runs. That package has no compiled cache, while modules the bridge uses (ctypes) do (D). So `site` probably does not run there, or runs on another path (I). Also unknown: whether Python starts when Marvelous starts or at the first plug-in click, and on which thread (U). | probe first (section 5, step 0); writes outside the allowed folders, so it needs a decision |
| Undocumented start-up options (`-python`, the "headless" options, `RegisterPythonScript`) | Recorded on 26 Oct from text inside the program. That note advised digging no further without CLO's word, because of CLO's terms on extraction (MD-SCRIPTING-2026-10-26.md lines 37-48) (D). This helper repeated a read-only text search of the program for start-up hooks, found nothing new beyond folder-registration messages, and deleted the extract at once. | not recommended |
| Keyboard route | It worked by hand (advisor). Simulated keys are forbidden by RULINGS (1 Nov rule 7; his 29 and 30 Oct rulings). | excluded |

No route that avoids UI Automation is confirmed. The Python hook is the only one that could be, and one job on the running bridge can settle it.

## 5. Recommended fix

### Step 0 (no Marvelous restart, about 10 minutes): probe Python's start-up hook through the bridge running now
One job via `md_job.py` reports: `sys.flags.no_site`, `'site' in sys.modules`, `sys.prefix`, `sys.path`, `site.getsitepackages()` (if present), `threading.current_thread().name`, and the thread id compared with the GUI thread the bridge's timer runs on. If `site` runs and processes the site-packages folder Marvelous uses, test a one-line `.pth` that only appends a time stamp to a file on F: at the next launch. If that time stamp falls at launch, before any click, the bridge can start itself. The `.pth` line would `import` a tiny starter in F:/LedgerTools that waits for the main window and then calls the bridge's `start()` on the GUI thread (SetTimer from the GUI thread, as ledger_md_bridge.py:131-137 already does). If `site` is off, or Python starts only at the first click, drop this route. Placing a file in C:/Users/Public/Documents/MarvelousDesigner is outside the allowed write folders and changes his program's set-up, so it needs a DECISIONS line and, under the rules, his ruling if it goes beyond them.

### The fallback that does not wait on step 0: keep the one menu item, make the start robust
Changes to make (none made here):

1. **start_bridge.ps1: address the main window by its handle, not "first window".** Replace :94 with: list the process's top-level windows (EnumWindows, as in the listing above); take the visible window that has no owner and whose class ends in `QWindowIcon`; then `AutomationElement.FromHandle(hwnd)`. Log the handle, class and size of every visible window of the process.
2. **Dismiss the Welcome window by window message, not by input.** Before any search, find visible windows owned by that main window with class ending `OwnDC` (the Welcome window's signature today: owned, `Qt6103QWindowOwnDC`, 960 x 550). Send `PostMessage(hwnd, WM_CLOSE)`, which asks the window to close as its close button would; https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-close (D). Check again after 5 s and up to 3 times, because it came back once. Never close the main window, and never close any window while the main window is disabled (a modal question such as "save changes?"); log and stop in that case. This is a new automated action beyond his 30 Oct ruling (which covers only the menu item), so it needs a DECISIONS line and his ruling replacing the old line (CLAUDE: "if code must change a ruling, ask him first").
3. **Try Invoke without opening the menus.** Qt builds a menu item's children from the action's menu (qwindowsuiautils and Qt's accessible menu item; I, not read for 6.10). So "LEDGER bridge" may be reachable and invokable while its menus stay shut, which would not need Marvelous in front (cause B). Try that path first, searching Children of the menu bar, then Children of each item. Keep Expand as the second path. The 30 Oct note says closed menus showed no items, so this is U: the test decides.
4. **One copy of Marvelous.** open_marvelous.ps1 writes the process number it launched to F:/LedgerTools/md-jobs/marvelous.pid. start_bridge.ps1 targets that process. If it is gone and exactly one other copy runs, use that one. If several run, log "several Marvelous copies" and do nothing (no guessing at :36). ledger_md_bridge.py adds `"pid": os.getpid()` to the heartbeat (:97-98, :142) and refuses to start when a fresh heartbeat names another living process (one bridge per inbox).
5. **Every outcome logged.** Add `-log` to start_bridge.ps1:95 and :115. Log which call failed, its elapsed milliseconds, the chosen window's class and handle, and the front window. Replace open_marvelous.ps1:31's title list with the full list of Marvelous's visible windows (handle, owner, class, size, order).
6. **One UI Automation client at a time.** A lock file (F:/LedgerTools/md-jobs/start.lock, with a time stamp, taken over after 5 minutes) so a hand run cannot overlap the task's run.
7. **Timing.** Remove the 120 s sleep (section 3). Wait instead for the main window plus 20 s, as open_marvelous.ps1:52 already does. Make md_job.py:51's timeout longer than start_bridge's worst case and catch `TimeoutExpired`. Raise the task limit (register_marvelous_task.ps1:10) to 30 minutes, or bound open_marvelous's loop under 15.
8. **Restart, once, only a copy with no work in it.** If three starts fail on the copy named in marvelous.pid, and that copy never had a fresh heartbeat (so no garment work is open in it), then: `CloseMainWindow()`, wait 60 s, and stop only that recorded process if it is still there. Run `schtasks /run /tn "LEDGER Marvelous open"` (his signed-in session; the task has the interactive token, register_marvelous_task.ps1:9). At most one restart in any 2 hours. Never touch a copy he opened or one with a past heartbeat. Stopping Marvelous by script is new, so it needs the same ruling as item 2.
9. **Down means go on (his 12:24 decision).** After the restart's tries, write F:/LedgerTools/md-jobs/down.json (time, reason). md_job.py `--start` and `submit` then answer at once "bridge down" instead of waiting, and the work that uses Marvelous (comparison drapes only, DECISIONS 12:39) is skipped. The next hourly run tries again once. Nothing goes on his page.

## 6. Unattended test plan

Offline checks (no Marvelous):
- A window-picker self-test from recorded window lists: today's four-copy listing, a single copy with the Welcome window, a single copy without it, and a main window disabled under a modal window. Expected: the right main handle; the Welcome window listed for closing; "several copies" refused; disabled main window means stop.
- md_job.py self-test: a start call that outlasts its timeout returns False with a note and does not crash; with down.json present, `--start` returns at once.
- ledger_md_bridge heartbeat carries `pid`; a second start with a fresh heartbeat from another living process refuses.

Live, in his signed-in session, through the interactive task only, when no job runs and only one Marvelous copy is open (the four now open must first be reduced by whoever owns them; a script must not close his copies):
1. Fresh launch, Welcome window shown. Pass: starts.jsonl names the Welcome window closed, then "invoked"; heartbeat fresh within 3 minutes of launch; the heartbeat's `pid` equals marvelous.pid.
2. Welcome window reappears. Pass: a second close is logged and the start still succeeds.
3. Another window in front. The task can only record what is naturally in front, never cause it. Pass: the front window is logged, and the invoke-without-Expand path (change 3) succeeds or fails with its own note.
4. Bridge already alive. Pass: "already alive", no UI Automation call.
5. Job running (busy.json). Pass: no action.
6. Failure path: point the menu path at a name that does not exist, in a test copy of the script with a separate `LEDGER_MD_JOBS` folder. Pass: three logged failures, one restart of the recorded copy only, then down.json, and md_job answering "bridge down" at once.
7. Repeat case 1 on three separate launches across a day (one success proved 9 Nov and failed 16 Nov).

Each live case is one task run, logged in opens.jsonl and starts.jsonl. Two tries per fault still hold (CLAUDE.md); the redesign counts as a new method only once the ruling for items 2 and 8 is given.

## Could not be confirmed or reached
- Which element start_bridge.ps1 held on 16 Nov (the Welcome window or the main window), and whether the Welcome window was on screen at 10:20 in copy 5736. That copy shows no Welcome window now, and who closed it, if anyone, is unknown. Confirm with change 5's logging on the next run.
- The order in which UI Automation lists a process's windows under the desktop: not stated in the Microsoft page read. The FlaUI source only implies owned windows sit under their owner.
- Whether Qt 6.10 keeps a menu open, and lets an item be invoked, while another program (the Start menu) is in front; whether closed menus' items can be invoked.
- Whether Marvelous has a setting to stop showing the Welcome window at start. The registry holds only a Help > Welcome Page shortcut entry (`actionWelcome_Page`); no "show at start" value was found. The login keys were not read.
- Whether Marvelous's Python runs `site` and when Python starts (step 0 settles both).
- The .NET Framework source for `Process.MainWindowHandle` (referencesource URL returned 404). The claim that an owned window is skipped rests on the 16 Nov listing and general knowledge (U).
- Qt bug pages and Marvelous support pages were not retried (earlier refused: 403 or a login wall); none is used as evidence.
