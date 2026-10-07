# P1 COMPLETED PACKAGED (phase 1, item 1.4; PLAN.md: "P1 completed packaged: day, night, walking,
# Windows memory, sustained speech"). P1 was profiled on 3 October in the editor's game mode
# (production/research/pre-production/P1-RESULTS-2026-10-03.md); this runs the same hook camera in
# the PACKAGED game, the played copy, with the cast's voice speaking without a break the whole time
# (tools/voice-live/voice_load.py, on the card, as the game has it), and reads Windows' own memory
# counters while it captures: the card's dedicated memory in use (all processes, and the game's and
# the voice's own), and each process's private memory and working set.
#
#   powershell -File tools/p1-packaged.ps1 [-Exe F:\LedgerTools\played-game\Windows\LedgerProbe.exe]
#
# Three captures of 1800 frames each: standing by day, standing at night, walking by day, at his
# screen size (3440x1440) and the game's own 55%. Each writes one JSON line (tools/perf-hook.py) and
# its memory line to production/research/pre-production/p1-packaged/runs.jsonl. It refuses to start
# while the build machine or an Unreal editor runs (their graphics work would be in the numbers).
param([string]$Exe = "F:\LedgerTools\played-game\Windows\LedgerProbe.exe", [int]$Frames = 1800, [int]$VoiceSeconds = 660)
# THE LAUNCHER AND THE GAME IT STARTS, 7 October: the copy's top-level LedgerProbe.exe is a launcher stub
# that starts LedgerProbe\Binaries\Win64\LedgerProbe.exe and lingers. The first run measured the stub
# (1 MB) and, stopping it, left the game itself running all night; started directly from a script the
# real binary would not find its own content. So the stub starts it, and the game is then found by its
# path and measured, waited for and, if need be, stopped itself.
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo
if (Get-Process Runner.Worker, UnrealEditor*, LedgerProbe* -ErrorAction SilentlyContinue) { "p1Packaged status=BUSY (the build machine, an editor or a game is running)"; exit 2 }
if (-not (Test-Path $Exe)) { "p1Packaged status=NO-GAME exe=$Exe"; exit 2 }
$outDir = Join-Path $repo "production\research\pre-production\p1-packaged"
New-Item -ItemType Directory -Force $outDir | Out-Null
$runs = Join-Path $outDir "runs.jsonl"
$gameDir = Join-Path (Split-Path $Exe -Parent) "LedgerProbe"
$csvDir = Join-Path $gameDir "Saved\Profiling\CSV"
$tmp = "F:\LedgerTools\tmp\p1-packaged"
New-Item -ItemType Directory -Force $tmp | Out-Null
$py = "python"

# THE VOICE, SPEAKING THROUGHOUT: started once, warmed, and left running for all three captures.
$voice = Start-Process -FilePath $py -ArgumentList @("tools/voice-live/voice_load.py", "--seconds", "$VoiceSeconds") -PassThru -NoNewWindow `
         -RedirectStandardOutput "$tmp\voice-load.log" -RedirectStandardError "$tmp\voice-load.err"
$w = 0
while (-not (Select-String -Path "$tmp\voice-load.log" -Pattern "voiceLoad ready" -Quiet -ErrorAction SilentlyContinue) -and $w -lt 240 -and -not $voice.HasExited) { Start-Sleep 2; $w += 2 }
$voiceReady = Select-String -Path "$tmp\voice-load.log" -Pattern "voiceLoad ready" -Quiet -ErrorAction SilentlyContinue
"p1Packaged voice=" + $(if ($voiceReady) { "speaking" } else { "NOT-READY" })

function Sample-Memory($gamePid, $voicePids) {
  # Windows' own counters: the card's dedicated memory per process and in all, and each process's memory.
  $s = @{ at = (Get-Date).ToString("s") }
  try {
    $all = (Get-Counter '\GPU Adapter Memory(*)\Dedicated Usage' -ErrorAction Stop).CounterSamples | Measure-Object CookedValue -Sum
    $s.cardAllMB = [math]::Round($all.Sum / 1MB)
    $per = (Get-Counter '\GPU Process Memory(*)\Dedicated Usage' -ErrorAction Stop).CounterSamples
    $s.cardGameMB = [math]::Round((($per | Where-Object { $_.InstanceName -like "pid_$($gamePid)_*" } | Measure-Object CookedValue -Sum).Sum) / 1MB)
    $s.cardVoiceMB = [math]::Round((($per | Where-Object { $ip = $_.InstanceName; $voicePids | Where-Object { $ip -like "pid_$($_)_*" } } | Measure-Object CookedValue -Sum).Sum) / 1MB)
  } catch { $s.cardError = "$_".Substring(0, [Math]::Min(80, "$_".Length)) }
  $g = Get-Process -Id $gamePid -ErrorAction SilentlyContinue
  if ($g) { $s.gamePrivateMB = [math]::Round($g.PrivateMemorySize64 / 1MB); $s.gameWorkingMB = [math]::Round($g.WorkingSet64 / 1MB) }
  $vp = $voicePids | ForEach-Object { Get-Process -Id $_ -ErrorAction SilentlyContinue }
  if ($vp) { $s.voicePrivateMB = [math]::Round((($vp | Measure-Object PrivateMemorySize64 -Sum).Sum) / 1MB) }
  $os = Get-CimInstance Win32_OperatingSystem
  $s.systemUsedMB = [math]::Round(($os.TotalVisibleMemorySize - $os.FreePhysicalMemory) / 1KB)
  return $s
}

$matrix = @(
  @{ label = "packaged-day-stand"; args = @("-PerfHook=stand") },
  @{ label = "packaged-night-stand"; args = @("-PerfHook=stand", "-PerfHookNight") },
  @{ label = "packaged-day-walk"; args = @("-PerfHook=walk") }
)
foreach ($m in $matrix) {
  Remove-Item "$csvDir\*" -Force -ErrorAction SilentlyContinue
  $a = @("-LedgerSlice", "-LedgerCrime", "-Encounter=live", "-LiveFresh", "-TalkFake", "-NoTitle") + $m.args + @(
         "-PerfHookFrames=$Frames", "-csvGpuStats", "-ExitAfterCsvProfiling", "-RenderOffScreen", "-ResX=3440", "-ResY=1440",
         "-windowed", "-ForceRes", "-nosplash", "-unattended", "-dpcvars=r.ScreenPercentage=55,t.MaxFPS=0,r.VSync=0")
  $t0 = Get-Date
  $stub = Start-Process -FilePath $Exe -ArgumentList $a -PassThru -NoNewWindow -RedirectStandardOutput "$tmp\$($m.label).log" -RedirectStandardError "$tmp\$($m.label).err"
  $voicePids = @(Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "voice-server.py|voice_load.py" } | ForEach-Object { $_.ProcessId })
  # the game the launcher starts, found by its path (up to a minute)
  $p = $null
  for ($k = 0; $k -lt 30 -and -not $p; $k++) {
    Start-Sleep 2
    $g = Get-CimInstance Win32_Process -Filter "Name='LedgerProbe.exe'" | Where-Object { $_.ExecutablePath -like "*\Binaries\Win64\LedgerProbe.exe" } | Select-Object -First 1
    if ($g) { $p = Get-Process -Id $g.ProcessId -ErrorAction SilentlyContinue }
  }
  if (-not $p) { "p1Packaged $($m.label) status=NO-GAME-PROCESS"; continue }
  $samples = @()
  while (-not $p.HasExited -and ((Get-Date) - $t0).TotalMinutes -lt 8) { Start-Sleep 2; $samples += ,(Sample-Memory $p.Id $voicePids) }
  if ($stub -and -not $stub.HasExited) { Stop-Process -Id $stub.Id -Force -ErrorAction SilentlyContinue }
  if (-not $p.HasExited) { Stop-Process -Id $p.Id -Force -ErrorAction SilentlyContinue }
  Get-Process LedgerProbe -ErrorAction SilentlyContinue | Stop-Process -Force -ErrorAction SilentlyContinue   # nothing of this capture outlives it
  Start-Sleep 2
  $csv = Get-ChildItem $csvDir -Filter *.csv -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
  $perf = if ($csv) { (& $py tools/perf-hook.py $csv.FullName --label $m.label) -join "" } else { "{`"label`": `"$($m.label)`", `"status`": `"NO-CSV`"}" }
  $mem = @{ label = $m.label; samples = $samples.Count }
  foreach ($k in "cardAllMB", "cardGameMB", "cardVoiceMB", "gamePrivateMB", "gameWorkingMB", "voicePrivateMB", "systemUsedMB") {
    $v = @($samples | ForEach-Object { $_[$k] } | Where-Object { $_ -ne $null } | Sort-Object)
    if ($v.Count) { $mem[$k + "Peak"] = $v[-1]; $mem[$k + "Median"] = $v[[int][math]::Floor($v.Count / 2)] }
  }
  $memLine = $mem | ConvertTo-Json -Compress
  Add-Content $runs $perf -Encoding utf8
  Add-Content $runs $memLine -Encoding utf8
  "p1Packaged $($m.label) minutes=$([math]::Round(((Get-Date) - $t0).TotalMinutes, 1))"
  $perf
  $memLine
}
# the voice ends on its own when its time is up, and only then prints its summary (sustained speech)
$w = 0
while ($voice -and -not $voice.HasExited -and $w -lt 900) { Start-Sleep 5; $w += 5 }
if ($voice -and -not $voice.HasExited) { Stop-Process -Id $voice.Id -Force -ErrorAction SilentlyContinue }
Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -match "voice-server.py" } | ForEach-Object { Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }
$sum = Select-String -Path "$tmp\voice-load.log" -Pattern "voiceLoadSummary" -ErrorAction SilentlyContinue | Select-Object -Last 1
"p1Packaged voice=" + $(if ($sum) { $sum.Line } else { "no-summary" })
