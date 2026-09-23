# Nano on the card with the game running: four runs, one at a time.
#   A  the slice at 1280x720, no voice
#   B  the slice at 3440x1440 drawn at half and upscaled, no voice
#   C  B with Nano speaking the ten lines twice on the same card
#   D  Nano alone
# The game's frame times come from its own CSV profiler; GPU memory per process
# from Windows' GPU Process Memory counters, sampled every two seconds.
param([string]$Only = "ABCD")
$ErrorActionPreference = "Continue"
$repo = "C:\Users\Jafar\ledger-local"
$exe = "$repo\ue-probe\Packaged\Windows\LedgerProbe\Binaries\Win64\LedgerProbe.exe"
$csvDir = "$repo\ue-probe\Packaged\Windows\LedgerProbe\Saved\Profiling\CSV"
$out = "C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-local\7ec707fe-fd41-4a40-ac4f-b7fc4cc91e3b\scratchpad\nano-test\card"
New-Item -ItemType Directory -Force $out | Out-Null
$py = "C:\LedgerTools\chatterbox-nano\env-dml\Scripts\python.exe"
$env:NANO_PKG = "C:\LedgerTools\chatterbox-nano\src-master\src"
$env:NANO_WEIGHTS = "C:\LedgerTools\chatterbox-nano\weights"
$nanoPy = "C:\Users\Jafar\AppData\Local\Temp\claude\C--Users-Jafar-ledger-local\7ec707fe-fd41-4a40-ac4f-b7fc4cc91e3b\scratchpad\nano-test\nano_card_timing.py"

function Sample-Gpu($procIds, $file, $seconds) {
  $end = (Get-Date).AddSeconds($seconds)
  while ((Get-Date) -lt $end) {
    try {
      $c = Get-Counter "\GPU Process Memory(*)\Dedicated Usage" -ErrorAction Stop
      foreach ($s in $c.CounterSamples) {
        foreach ($p in $procIds) {
          if ($s.InstanceName -match "pid_$($p)_") { "{0:HH:mm:ss} pid={1} dedicatedMB={2:N0}" -f (Get-Date), $p, ($s.CookedValue / 1MB) | Add-Content $file }
        }
      }
    } catch { "counter-failed $_" | Add-Content $file }
    Start-Sleep -Seconds 2
  }
}

function Run-Game($label, $resX, $resY, $sp, $frames, $extraPids) {
  Remove-Item "$csvDir\*" -Force -ErrorAction SilentlyContinue
  # -ForceRes: a 3440x1440 WINDOW does not fit a 3440x1440 desktop once it has
  # borders, and the engine quietly shrank the first try to 888x500.
  $args = @("-LedgerSlice", "-RenderOffScreen", "-ResX=$resX", "-ResY=$resY", "-windowed", "-ForceRes", "-nosplash",
            "-dpcvars=r.ScreenPercentage=$sp,t.MaxFPS=0,r.VSync=0",
            "-ExecCmds=`"csvprofile frames=$frames`"")
  $g = Start-Process -FilePath $exe -ArgumentList $args -PassThru -RedirectStandardOutput "$out\$label-game.log" -RedirectStandardError "$out\$label-game.err"
  Start-Sleep -Seconds 20
  Sample-Gpu (@($g.Id) + $extraPids) "$out\$label-gpu.txt" 30
  $t = 0; while (-not (Get-ChildItem $csvDir -Filter *.csv -ErrorAction SilentlyContinue) -and $t -lt 180) { Start-Sleep 2; $t += 2 }
  Start-Sleep 3
  Stop-Process -Id $g.Id -Force -ErrorAction SilentlyContinue
  Get-ChildItem $csvDir -Filter *.csv -ErrorAction SilentlyContinue | Select-Object -First 1 | ForEach-Object { Copy-Item $_.FullName "$out\$label-frames.csv" -Force }
  "$label done csv=" + (Test-Path "$out\$label-frames.csv")
}

function Start-Nano($label, $rounds) {
  Start-Process -FilePath $py -ArgumentList @("`"$nanoPy`"", "`"$repo`"", "`"$out\$label-nano.json`"", $label, "$rounds") -PassThru `
    -RedirectStandardOutput "$out\$label-nano.log" -RedirectStandardError "$out\$label-nano.err" -NoNewWindow
}

if ($Only -match "D") {
  $n = Start-Nano "D-alone" 2
  Sample-Gpu @($n.Id) "$out\D-alone-gpu.txt" 40
  $n.WaitForExit(900000) | Out-Null
  "D done"
}
if ($Only -match "A") { Run-Game "A-720p" 1280 720 100 2400 @() }
if ($Only -match "B") { Run-Game "B-uw-half" 3440 1440 50 2400 @() }
if ($Only -match "C") {
  # The voice first, so the game's frames are captured while it is speaking.
  $n = Start-Nano "C-with-game" 8
  $t = 0; while (-not (Select-String -Path "$out\C-with-game-nano.log" -Pattern "nanoCard label=" -Quiet -ErrorAction SilentlyContinue) -and $t -lt 240) { Start-Sleep 2; $t += 2 }
  Run-Game "C-uw-half-nano" 3440 1440 50 2400 @($n.Id)
  Stop-Process -Id $n.Id -Force -ErrorAction SilentlyContinue
  "C done"
}
