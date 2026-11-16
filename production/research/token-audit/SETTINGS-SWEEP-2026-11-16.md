# Settings sweep outside the repository, 16 Nov 2026 (read 14:19 Swiss time)

Read-only. No key or token value was printed; keys are marked "set" or "not set". Items not read are marked unread.

## Commands used

- `cat` (secrets filtered) of C:\Users\Jafar\.claude\settings.json and settings.local.json, ledger-local\.claude\settings.json and settings.local.json; grep of ledger-local\.claude\agents\*.md for model and effort lines; `head` of the scheduled task's SKILL.md.
- PowerShell: `Get-ItemProperty HKLM:\SOFTWARE\Microsoft\WindowsUpdate\UX\Settings`; `Test-Path` on the RebootRequired key; `powercfg /getactivescheme`; `powercfg /q SCHEME_CURRENT SUB_SLEEP STANDBYIDLE`, `SUB_SLEEP HIBERNATEIDLE`, `SUB_VIDEO VIDEOIDLE`; `Get-ScheduledTask` filtered on ledger, with `Get-ScheduledTaskInfo`; `Get-PSDrive C,F`; `Get-ChildItem` of both Startup folders; shortcut target through WScript.Shell; `Get-Process Runner.Listener,Runner.Worker`; `Get-ChildItem Env:` filtered on ANTHROPIC, CLAUDE, LEDGER, MODEL (key and token names shown as "set" only).
- grep of tools/ for model check, JUMP, start check, fresh_gate, ANTHROPIC_MODEL; the docstring of tools/fresh_gate.py.

## Table

| Setting | Where it lives | Current value | How it can raise cost or stop work | Existing check | Proposed check |
|---|---|---|---|---|---|
| Session model (the production session) | The scheduled task's run; no "model" line in any settings.json. Not set by ANTHROPIC_MODEL (not set) | Not readable from settings; the gate expects claude-opus-5-5 | A session on a dearer or weaker model | tools/fresh_gate.py: SESSION_MODEL = "claude-opus-5-5", log_model(), run_model(), model_wrong() (the 14 Nov model check, reads the newest run's log) | Keep. DAILY: also read the model of the newest assistant turn in the log; wrong if not claude-opus-5-5 |
| Effort of the session | Env CLAUDE_EFFORT (this helper's session) | medium in this helper's environment; the production session's value unread | Higher effort costs more tokens; lower may fail work | None found in tools/ | Start: read CLAUDE_EFFORT or the log's first turn; wrong if it differs from what RULINGS names (the brief names none; unread) |
| Project agents' model and effort | ledger-local\.claude\agents\*.md (in repo) | diagnoser opus/high; extractor sonnet/medium; final-reviewer opus/medium; importer sonnet/medium; research-reader sonnet/medium; research-synthesis opus/medium; small-reviewer sonnet/medium | A line edited to a dearer model or higher effort | None found | DAILY: compare the 7 model and effort lines with these values; wrong if any differs |
| switchModelsOnFlag | C:\Users\Jafar\.claude\settings.json | false | true could switch model silently | None found | DAILY: wrong if not false |
| User permissions allow list | C:\Users\Jafar\.claude\settings.json | allow: mcp__scheduled-tasks__run_scheduled_task only; no defaultMode line; settings.local.json is empty (0 bytes) | A missing allow stops a scheduled run at its first write; a bypass line would remove prompts | None found | DAILY: wrong if a defaultMode of bypassPermissions appears or the allow list is lost |
| Project permissions and hooks | ledger-local\.claude\settings.json (in repo) | allow: git fetch/add/commit/push -u origin main*, dotnet run/build/test, dotnet --version, build-local.ps1, play.py close. Hooks: UserPromptSubmit gate_prompt_hook.py (30 s), PostToolUse page_read_hook.sh (10 s), Stop stop_hook.py (15 s). Plugin unreal-engine-skills true | A hook that fails or hangs blocks every prompt or stop; a missing allow stops unattended writes | tools/gate_prompt_hook.py, page_read_hook.py, stop_hook.py exist (hooks themselves) | DAILY: the three hook scripts exist and python runs |
| Project local settings | ledger-local\.claude\settings.local.json (in repo folder) | skillOverrides: 14 skills off; cowork-plugin-management false | A skill turned on adds context cost | None found | Low value; skip |
| Scheduled task ledger-daily-fresh-session | C:\Users\Jafar\.claude\scheduled-tasks\ledger-daily-fresh-session\SKILL.md (one file, 6,182 bytes, changed 11 Nov 17:49) | Runs every 15 min per its description; the file holds no schedule, mode or model field (those live in the app, unread) | Wrong schedule, or a mode that is not Auto, stops it at its first write (memory note) | fresh_gate.py (decides GO/WAIT), not the task's own settings | DAILY: file date later than 11 Nov 17:49 means it changed; read it; wrong if the first line is not the gate run |
| Other scheduled tasks present | C:\Users\Jafar\.claude\scheduled-tasks\ | ledger-fresh-session-handoff, ledger-fresh-session-test-2026-11-02, -11-03, ledger-morning-check-2026-10-06, ledger-page-answers-nightly | Any of them enabled would start a second session (unread: enabled state is in the app) | None found | Start: confirm only the daily task is enabled (needs the app's list, unread here) |
| Windows Update active hours | HKLM\...\WindowsUpdate\UX\Settings | ActiveHoursStart 12, ActiveHoursEnd 5 (active 12:00 to 05:00) | A restart outside these hours kills the session (7 Nov: restart at 00:14 killed the 23:22 session); 05:00 to 12:00 is open to restarts | None found for the setting (fresh_gate.py handles the aftermath) | DAILY: read both values; wrong if changed from 12 and 5 |
| Pending restart | HKLM\...\Auto Update\RebootRequired | not present (False) | A pending restart can happen at once | None found | Start and DAILY: wrong if the key exists; log it |
| Update pause | WindowsUpdate\UX\Settings PauseUpdatesExpiryTime | empty (no pause) | Updates install and restart | None found | Info only |
| Power plan | powercfg | Ultimate Performance (071e8fd2-530b-49c7-925c-3edb157c2910) | A switch to a saver plan sleeps the PC | None found | DAILY: wrong if the active GUID differs |
| Sleep after | powercfg STANDBYIDLE | On AC 0 (never); on battery 600 s | AC sleep would stop all work and the runner | None found | DAILY: wrong if AC value is not 0 |
| Hibernate after | powercfg HIBERNATEIDLE | AC 0, battery 0 (never) | Same | None found | DAILY: wrong if AC not 0 |
| Display off | powercfg VIDEOIDLE | AC 900 s, battery 180 s | Display off alone does not stop work; matters only to tester window checks | None found | Info only |
| LEDGER nightly walk | Task Scheduler | Ready; daily 01:30; last 16 Nov 01:30:01 | Disabled or moved stops the night walk | None found in tools/ | DAILY: state Ready, trigger 01:30 |
| LEDGER retention | Task Scheduler | Ready; daily 03:30; last 16 Nov 03:30:01 | Disabled stops disk upkeep, then floors fail | None found | DAILY: state Ready, last run under 26 h ago |
| LEDGER morning pictures | Task Scheduler | Ready; daily 04:15; last 16 Nov 04:15:01 | Same for the morning pictures | None found | DAILY: state Ready, last run under 26 h |
| LEDGER Marvelous open | Task Scheduler | Ready; no triggers; last 16 Nov 10:18:54 | Run on demand only | None found | Info only |
| LEDGER supervisor | Task Scheduler | Disabled; logon trigger; last 15 Sep | If enabled it could start work unattended | None found | DAILY: wrong if not Disabled |
| Drive C: free | Windows | 56.9 GB; floor 40 (production/retention.json "floors", RULINGS 2 Oct) | Under 40 GB: builds and renders stop | tools/retention.py space (before any build or job) | DAILY: wrong if under 40 GB; warn under 45 GB |
| Drive F: free | Windows | 20.9 GB; floor 20 | Under 20 GB: stop; only 0.9 GB above the floor | tools/retention.py space | DAILY: wrong if under 20 GB; warn under 22 GB (already inside it) |
| Runner startup shortcut | C:\Users\Jafar\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\LEDGER runner.lnk (dated 15 Sep 17:03) | Target C:\actions-runner-ledger\run.cmd, start in C:\actions-runner-ledger. Also in that folder: Emby Server.lnk (25 Oct). All-users Startup folder: empty | A missing shortcut leaves no build machine after a restart | None found | DAILY: shortcut exists and target is run.cmd |
| Runner.Listener | Process | Running, PID 7300, since 13 Nov 06:49. Runner.Worker not running | Not running: packaged builds and nightly packaging do not start | None found | Start and DAILY: process present; wrong if absent |
| Environment, model names | Process environment (this helper's) | ANTHROPIC_MODEL not set; LEDGER_TALK_CORE_MODEL not set (also not set at User level) | Would override the model | None found | DAILY: wrong if either becomes set without a ruling |
| Environment, API | Process environment | ANTHROPIC_BASE_URL = https://api.anthropic.com; ANTHROPIC_API_KEY not seen in the filtered list (the name did not appear; so not set here) | A different base URL could route and bill elsewhere; a set key bills the API instead of the plan | tools/api_batch.py uses its own key file (not read) | DAILY: wrong if base URL differs; report only "set" or "not set" for the key |
| Environment, Claude Code | Process environment | CLAUDE_CODE_ENTRYPOINT claude-desktop; CLAUDE_CODE_HOST_SCHEDULED_RUN 1 and CLAUDE_CODE_SESSION_ATTENDED 1 (this helper's run); CLAUDE_CODE_DISABLE_CRON empty; CLAUDE_CODE_SIMPLE 0; OAuth scopes and host auth refresh: set | Sign-in lost stops all sessions | None found | Info only |
| MSYSTEM | Environment | MINGW64 | MSYS path rewriting breaks Unreal launches (memory note) | None found | Info only |
| Hourly-run log access | C:\Users\Jafar\.claude\projects\... session logs | Read by fresh_gate.py (LOGS) | Unreadable log: gate cannot decide | tools/fresh_gate.py | Covered |

## Existing tools that read settings

- tools/fresh_gate.py: reads the session model (SESSION_MODEL, log_model, run_model, model_wrong), the handover, the logs' turn times, blocked runs and pending jobs. It reads no Windows, power, drive, runner or scheduled-task setting.
- tools/retention.py space: free space against the floors (not re-run here).
- tools/token_audit.py, handover_cost.py: read model names from logs for cost only.
- grep found no tool reading ANTHROPIC_MODEL, CLAUDE_EFFORT, active hours, powercfg, RebootRequired, the Startup shortcut or Runner.Listener.

## Unread

- Production session's actual effort and permission mode; enabled state of the scheduled tasks and the task's schedule and mode (held in the app).
- Whether ANTHROPIC_API_KEY exists at User or Machine level (only this process's environment was read).
- tools/page_read_hook.py / stop_hook.py bodies; api_batch.py's key file.

## Checks built (16 Nov)

tools/settings_check.py reads every row marked DAILY above except the session effort and the app-held scheduled-task settings (unreadable from a script): one line each, then wrong=N warn=N; selftest 6/6; first live reading 14:20 all OK (C: 71.3 GB, F: 22.4 GB). It runs in the DAILY file each evening; the session model stays with fresh_gate.py.
