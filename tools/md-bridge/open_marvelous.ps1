# Opens Marvelous Designer on his desktop and starts LEDGER's bridge in it, run by the Windows task
# "LEDGER Marvelous open" (registered by tools/md-bridge/register_marvelous_task.ps1).
#
#   schtasks /run /tn "LEDGER Marvelous open"      (how a session asks for it; the task has no trigger)
#
# WHY, 9 November 2026 (his yes on his page, marvelous-task-2026-11-09, 07:58): Marvelous has no command line
# or background mode, so a night session can only reach it in his own signed-in desktop. The task runs with the
# interactive token ("only while he is signed in"), the one route the plan found likely
# (production/research/clothing-pipeline/MARVELOUS-UNATTENDED-2026-11-08.md, route 1). It starts the program,
# waits for its main window, then calls start_bridge.ps1, the one UI Automation use his 30 October ruling allows.
# Nothing is clicked or typed. Each step's top-level window titles and the front window are logged as one JSON
# line in F:\LedgerTools\md-jobs\opens.jsonl, so a dialog in the way is named, not guessed.
$ErrorActionPreference = "Stop"
$EXE_PATH = "C:\Program Files\Marvelous Designer Personal\MarvelousDesigner_Personal.exe"
$EXE = "MarvelousDesigner_Personal"
$ROOT = if ($env:LEDGER_MD_JOBS) { $env:LEDGER_MD_JOBS } else { "F:\LedgerTools\md-jobs" }
$HERE = Split-Path -Parent $MyInvocation.MyCommand.Path
$WAIT_S = 240

Add-Type @"
using System; using System.Text; using System.Runtime.InteropServices;
public static class LedgerWin {
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll", CharSet=CharSet.Unicode)] public static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  public static string Title(IntPtr h) { var s = new StringBuilder(512); GetWindowText(h, s, 512); return s.ToString(); }
}
"@

function Log($step, $note) {
  $front = [LedgerWin]::Title([LedgerWin]::GetForegroundWindow())
  $wins = @(Get-Process | Where-Object { $_.MainWindowTitle } | ForEach-Object { "$($_.ProcessName): $($_.MainWindowTitle)" })
  $o = [ordered]@{ at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss"); step = $step; note = $note; front = $front; windows = $wins }
  if (-not (Test-Path $ROOT)) { New-Item -ItemType Directory -Force $ROOT | Out-Null }
  [System.IO.File]::AppendAllText((Join-Path $ROOT "opens.jsonl"), ($o | ConvertTo-Json -Compress) + "`n", (New-Object System.Text.UTF8Encoding($false)))
}

Log "begin" "task started"
$p = Get-Process $EXE -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $p) {
  Start-Process -FilePath $EXE_PATH -WorkingDirectory (Split-Path $EXE_PATH)
  Log "launched" "Marvelous started"
} else { Log "running" "Marvelous was already open; not started again" }

$t0 = Get-Date
while ($true) {
  $p = Get-Process $EXE -ErrorAction SilentlyContinue | Select-Object -First 1
  if ($p -and $p.MainWindowHandle -ne 0 -and $p.MainWindowTitle) { break }
  if (((Get-Date) - $t0).TotalSeconds -gt $WAIT_S) { Log "timeout" "no main window after $WAIT_S s"; exit 2 }
  Start-Sleep -Seconds 5
}
Log "window" "main window: $($p.MainWindowTitle)"
Start-Sleep -Seconds 20   # its plug-ins load after the window shows

for ($i = 1; $i -le 3; $i++) {
  $out = & powershell.exe -NoProfile -ExecutionPolicy Bypass -File (Join-Path $HERE "start_bridge.ps1") 2>&1 | Out-String
  Log "bridge-$i" $out.Trim()
  if ($out -match '"ok":\s*true') { exit 0 }
  Start-Sleep -Seconds 30
}
exit 3
