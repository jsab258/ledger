# THE LOCAL UNREAL BUILD (Jafar, 30 September: Unreal's build command is allowed
# in this project's settings, and only this). Builds the two LedgerProbe
# targets, the editor's and the game's, in Development for Win64, one after the
# other; the game target catches editor-only calls that would break the build
# machine. It waits while the build machine's runner builds or plays (a local
# Build.bat or editor then breaks the runner's build), and stops at the first
# failure. Nothing else: no packaging, no cleaning, no other project.
#
#   powershell.exe -NoProfile -File tools/ue/build-local.ps1
$ErrorActionPreference = "Continue"
function Wait-Runner {
  while (Get-CimInstance Win32_Process | Where-Object {
      ($_.Name -like 'UnrealEditor*' -or $_.Name -like 'UnrealBuildTool*' -or
       ($_.Name -eq 'dotnet.exe' -and $_.CommandLine -match 'UnrealBuildTool|AutomationTool')) -and
      $_.CommandLine -match 'actions-runner-ledger' }) {
    "{0} the build machine is building; waiting" -f (Get-Date -Format HH:mm)
    Start-Sleep -Seconds 30
  }
}
$repo = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$bat = "C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat"
$proj = "-Project=$repo\ue-probe\LedgerProbe.uproject"
foreach ($t in @("LedgerProbeEditor", "LedgerProbe")) {
  Wait-Runner
  "{0} building {1}" -f (Get-Date -Format HH:mm), $t
  $log = & $bat $t Win64 Development $proj -WaitMutex -NoHotReload 2>&1
  $log | Select-String -Pattern "error|Result:" | Select-Object -Last 15
  if (-not ($log | Select-String -Pattern "Result: Succeeded" -Quiet)) { "BUILD FAILED: $t"; exit 1 }
}
"both targets built"
