# THE AI TESTER'S LAUNCHER, 23 September: Unreal's own test launcher starts the
# packaged game for the exploratory tester and supervises it.
#
#   pwsh tools/ai-tester/launch.ps1 -Build <folder holding the packaged Windows game> [-Minutes 20] [-Slice]
#
# WHY IT IS THIS AND NOT OURS: Jafar asked that what Unreal provides be found
# and used first (production/research/ai-tester/WHAT-UNREAL-PROVIDES.md).
# Gauntlet's RunUnreal with the built-in UnrealGame.DefaultTest starts the
# game on this PC in a fixed window, kills it at the time limit, and leaves
# the log, any crash and its verdict (normal exit, timeout, crash, failed
# start) in an artifact folder - no C#, no plugin, nothing inside the game.
#
# WHAT THE GAME IS GIVEN, all launch flags: a 1280x720 window it keeps; a log
# at a fixed path the tester reads while it plays; the sound kept when the
# window loses focus; and Slate.ForceRawInputSimulation so an absolute mouse
# move turns the camera, as it does over Remote Desktop. -Slice starts the
# slice's player instead of the probe's.
#
# WHAT IT DOES NOT DO: look at the screen or press keys. That is the tester,
# and who the tester is (a computer-use model, paid) waits on Jafar
# (FOR-JAFAR, 23 September). This starts the game, waits, and reports.
param(
    [Parameter(Mandatory = $true)][string]$Build,
    [int]$Minutes = 20,
    [switch]$Slice
)
$ErrorActionPreference = "Stop"
$repo = Split-Path (Split-Path $PSScriptRoot -Parent) -Parent
$ue = "C:\Program Files\Epic Games\UE_5.8"
$uat = Join-Path $ue "Engine\Build\BatchFiles\RunUAT.bat"
$project = Join-Path $repo "ue-probe\LedgerProbe.uproject"
$stamp = Get-Date -Format "yyyy-MM-dd-HHmm"
$out = Join-Path $repo "production\playtest\ai-tester\$stamp"
New-Item -ItemType Directory -Force -Path $out | Out-Null
$log = Join-Path $out "game.log"

# NO SPACES INSIDE THE CLIENT'S ARGUMENTS: they travel inside one quoted
# -ClientArgs, so the cvar goes as -dpcvars=name=value rather than a quoted
# -ExecCmds, and the log path is the repository's, which has none.
$client = @("-nosplash", "-abslog=$log", "-ini:Engine:[Audio]:UnfocusedVolumeMultiplier=1.0",
            "-dpcvars=Slate.ForceRawInputSimulation=1")
if ($Slice) { $client += "-LedgerSlice" }

$uatArgs = @("RunUnreal", "-test=UnrealGame.DefaultTest", "-project=`"$project`"", "-build=`"$Build`"",
          "-platform=Win64", "-configuration=Development", "-windowed", "-ResX=1280", "-ResY=720",
          "-MaxDuration=$($Minutes * 60)", "-LogDir=`"$out`"", "-ClientArgs=`"$($client -join ' ')`"")
Write-Host "aiTesterLaunch build=$Build minutes=$Minutes slice=$Slice out=$out"
$p = Start-Process -FilePath $uat -ArgumentList $uatArgs -PassThru -NoNewWindow `
     -RedirectStandardOutput (Join-Path $out "gauntlet.log") -RedirectStandardError (Join-Path $out "gauntlet.err")
$p.WaitForExit()
$verdict = Select-String -Path (Join-Path $out "gauntlet.log") -Pattern "Result:|ExitReason|Test.*(Passed|Failed)|exited with code" |
           Select-Object -Last 5 | ForEach-Object { $_.Line.Trim() }
"aiTesterLaunch exit=$($p.ExitCode)" | Set-Content (Join-Path $out "verdict.txt")
$verdict | Add-Content (Join-Path $out "verdict.txt")
Get-Content (Join-Path $out "verdict.txt")
exit $p.ExitCode
