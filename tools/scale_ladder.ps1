# n16-3 step 4, first part: the hook stand at N = 1, 2, 4, 10 street-lengths, no people, three launches at N=1 and N=10
# (METHOD-NOTE-2026-11-16.md step 4 and review fix 6). Each capture through tools/p1-packaged.ps1 (packaged copy, High, voice).
Set-Location C:\Users\Jafar\ledger-local
$plan = @(1, 1, 1, 2, 4, 10, 10, 10)
$i = 0
$qlog = "F:/LedgerTools/tool-dev/runs/kiln-gate-2026-11-17-lanes/queue.log"
if (-not (Test-Path $qlog)) { "scaleLadder stop: no queue log"; exit 2 }
# wait for the Kiln lane queue to finish (no perf capture beside drapes; a gap between jobs is not enough, 17 Nov)
while (-not (Select-String -Path $qlog -Pattern "queue finished|STOP before" -Quiet)) { Start-Sleep 60 }
"scaleLadder: Kiln queue finished at $(Get-Date -Format HH:mm)"
foreach ($n in $plan) {
  $i++
  while (Get-Process Runner.Worker, UnrealEditor*, LedgerProbe*, drape-studio* -ErrorAction SilentlyContinue) { Start-Sleep 30 }
  $space = python tools/retention.py space --job "scale ladder" --drives CF
  if (-not ($space -match '"verdict": "GO"')) { "scaleLadder stop: space $space"; break }
  "scaleLadder run $i of $($plan.Count): N=$n at $(Get-Date -Format HH:mm)"
  & powershell -NoProfile -Command "& tools/p1-packaged.ps1 -Only day-stand -Tag scale$n-r$i -GameArgs '-ScaleTest=$n'" | Select-Object -Last 3
}
"scaleLadder done $(Get-Date -Format HH:mm)"
