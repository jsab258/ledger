# THE BUILD MACHINE, MOVED TO THE NEW REPOSITORY (5 October 2026, phase 0 item 0.7).
#
# The history was cleaned into a new public repository, jsab258/ledger; the old one is now the
# private jsab258/ledger-archive-2026-10, where this PC's runner is still registered. This moves
# the runner to the new repository, keeping its name, its label (ledger-pc, which the Unreal
# workflow asks for), its work folder and its service under Jafar's own account.
#
# Run it yourself, in PowerShell opened as administrator (the service is reinstalled):
#   powershell -NoProfile -ExecutionPolicy Bypass -File C:\Users\Jafar\ledger-local\tools\runner\reconnect.ps1
# It asks for two things at its own prompts, which only you type: the registration token from
# GitHub's new-runner page, and your Windows password for the service's account. Nothing else.
#
# Where the token is: github.com/jsab258/ledger, Settings, Actions, Runners, "New self-hosted
# runner", Windows; under "Configure", the line beginning "./config.cmd --url ... --token": the
# long code after --token. It works for an hour.
#Requires -RunAsAdministrator
$ErrorActionPreference = "Stop"
$dir = "C:\actions-runner-ledger"
$svc = "actions.runner.jsab258-ledger.JAFAR-DESKTOP"
Set-Location $dir

Write-Host "1. Stopping the old runner service, if it runs."
Stop-Service $svc -ErrorAction SilentlyContinue

Write-Host "2. Forgetting the old registration on this PC only (the archive keeps an offline entry, harmless)."
& .\config.cmd remove --local
if (Get-Service $svc -ErrorAction SilentlyContinue) { & sc.exe delete $svc | Out-Null }

Write-Host "3. Registering with the new repository. Paste the token when asked; answer the other questions with Enter,"
Write-Host "   and give your Windows password when it asks for the service account's password."
& .\config.cmd --url https://github.com/jsab258/ledger --name JAFAR-DESKTOP --labels ledger-pc --work _work `
    --runasservice --windowslogonaccount ".\Jafar" --replace
if ($LASTEXITCODE -ne 0) { Write-Host "Registration did not finish (exit $LASTEXITCODE). Nothing else was changed."; exit $LASTEXITCODE }

Write-Host "4. Checking the new service runs."
$s = Get-Service "actions.runner.jsab258-ledger.JAFAR-DESKTOP" -ErrorAction SilentlyContinue
if ($s -and $s.Status -eq "Running") { Write-Host "The build machine is connected and running. Tell Claude: done." }
else { Write-Host "The service is not running yet: tell Claude what the window says." }
