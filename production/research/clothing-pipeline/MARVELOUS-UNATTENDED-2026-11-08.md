# Marvelous Designer without a person at the PC (research note, 8 November 2026)

Order item n09-6. Research only: nothing downloaded or run; no clicks, keys or computer use; no logins or cookies. Sources read 8 Nov 2026. **D** documented; **I** inference; **U** unverified.

## Home facts read
- Installed: Marvelous Designer Personal, C:\Program Files\Marvelous Designer Personal. Its ChangeLog_Marvelousdesigner.html is only a redirect stub to marvelousdesigner.com/move/5300, so the exact build is not in it (U). tools/md-bridge/start_bridge.ps1 (read 8 Nov) calls it "Marvelous 2026.1", a Qt 6 program.
- Bridge (F:\LedgerTools\md-bridge\md_bridge.py, read 8 Nov): a script run inside Marvelous as the plug-in "Plugins > Plug-in > LEDGER bridge"; polls an inbox folder for job .py files, heartbeat in alive.txt. Its docstring: Marvelous "has no command line and no way to run a script at start-up".
- start_bridge.ps1: UI Automation walks Plugins > Plug-in > LEDGER bridge and invokes it; no mouse or keys. It works only on a menu that can be reached, so a dialog in front, or a window not yet up, stops it. Authorised only for that one item (his ruling 30 Oct, memory uia-only-the-bridge-item).
- Earlier research: production/research/clothing-pipeline/MD-SCRIPTING-2026-09-29.md (29 Sep): no command line, no headless, no start-up script, a click after every launch.

## Q1. Start-up script, command line, headless, batch
- Plug-in Management, https://developer.marvelousdesigner.com/register.html (8 Nov): a .py file is registered in the Plug-in Manager and "can be launched directly from within Marvelous Designer". Nothing on auto-run, start-up or command-line arguments (D, by absence).
- Developer changelog, https://developer.marvelousdesigner.com/changelog.html (8 Nov): 2025.1.107 added ".py as a plugin via the plugin manager"; no entry on command line, start-up, auto-run or batch to 2026.1 (D, by absence).
- The same 2026.1 entry says `ImportMeasurement` was removed from the docs because "it works in headless mode only". So some headless code path exists internally, but no documented way to enter it for Personal (D for the quote; the reading is I). Worth one question to Marvelous support.
- Official team reply (CLO/Marvelous support, 2022-2023 threads): no headless session. Only seen through a search summary; the thread pages returned 403, so this is U in full.
- Linux edition (CG Channel, 1 Oct 2025, via search result; page not read in full): Python API aimed at Enterprise pipelines and batch work "directly inside the software". No headless claim confirmed (U). Not Personal.
- No "MD Batch" or automation tool for Personal found (U; absence of evidence).

## Q2. Start-up dialogs and the settings that suppress them
- Nothing found in any reachable official page about licence/login, update, news or crash-recovery dialogs or settings to suppress them. Searches returned only other programs' settings. **Unreached/unverified.** The installed folder holds Breakpad (crash reporter) and a HASP licence DLL (hasp_windows_x64), which suggests crash and licence prompts exist (I).
- Prior note: Personal needs internet and a sign-in; if the sign-in is not remembered, a login dialog appears (I, 29 Sep).
- Support pages "Python Script" (support.marvelousdesigner.com/hc/en-us/articles/47358277921177) and the two community threads returned HTTP 403; not read, not worked round.
- A direct way to learn the dialogs: the 8 Nov failure itself. What stood in front was never seen (a scheduled run has no computer use). A try would log window titles from the process (see route 1).

## Q3. Studios
- AYON's Marvelous Designer addon, https://help.ayon.app/articles/2112433-marvelous-designer-configuration (8 Nov): the Launcher starts Marvelous and prepares the Python/PySide setup in a "pre-launch phase". It describes no start-up script or auto-run for its own menu; its tools are artist-driven (D). Pipeline code at docs.ayon.dev was seen only in a search result (U).
- CLO user thread "Automating CLO Export" (via search summary, 403 on read): users report Python is limited, one file at a time, human intervention needed (U).
- No studio example of a start-to-finish unattended Marvelous run found (D, consistent with 29 Sep).

## Q4. Task Scheduler, interactive
- Microsoft, TASK_LOGON_TYPE, https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_logon_type (page dated 2024-02-22, read 8 Nov): `TASK_LOGON_INTERACTIVE_TOKEN`: "User must already be logged on. The task will be run only in an existing interactive session." `TASK_LOGON_S4U`: "the task will run in a non-interactive desktop". `TASK_LOGON_PASSWORD`: password supplied at registration.
- Microsoft, https://learn.microsoft.com/en-us/windows/win32/taskschd/security-contexts-for-running-tasks (updated 2025-05-12, read 8 Nov): a non-administrator may register for their own account with the S4U or interactive logon type without a password.
- So a task set to the interactive token runs in his logged-on session, where a GUI program can have a window (D). That "Run only when user is logged on" in the Task Scheduler window is this logon type is I (the settings page itself was not read). Whether Marvelous's window then shows, and gets past its dialogs, is U. The session must be unlocked; a locked screen is U.

## Routes, most likely first
1. **Interactive task starts Marvelous, then the existing UI Automation start.** Likelihood: best. Needs: a task with the interactive token running the exe, then start_bridge.ps1 as a second task or first step after a wait for the window; a log of top-level window titles and the foreground window at each step, so the blocker is named. Risks: a dialog still in front (Q2 unknown); a locked session (U). Fits his ruling of 30 Oct (same item, same script); only the launch is new.
2. **Run the bridge's start through the same interactive task, retry on stale heartbeat.** Same as 1, with a repeat each few minutes; cheap addition once 1 works.
3. **Ask Marvelous support whether a start-up or headless switch exists** (the 2026.1 "headless mode only" wording). Needs his account or a public question; slow; Personal may be excluded.
4. **Enterprise licence (Linux or Windows) for batch use.** Not Personal; US$199 a month or US$2,000 a year per 29 Sep note; headless still unconfirmed. Needs money: his decision.
5. **Non-interactive (S4U/password) run.** Unlikely: a non-interactive desktop has no usable window for a Qt GUI and UI Automation (I).

## Could not reach
Support pages (Python Script article, both forum threads, CLO "Automating CLO Export"): 403. The installed changelog (redirect only). CG Channel and Digital Production pages: seen only in search results. Any Marvelous page on start-up dialogs or settings.
