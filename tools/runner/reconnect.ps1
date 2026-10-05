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

# NOTHING OLD RUNS ON THIS PC WHEN IT CONNECTS (found 5 October by the phase 0 exit's reviewer):
# main's sixteen upload steps set off eleven September jobs (installing a scheduled task,
# restarting the old Telegram bot, setting up compilers) that wait for this PC's label; a
# connected runner would take them at once. So before anything is changed, every waiting run is
# read from GitHub (public, no sign-in), and the script stops if any is from a workflow no longer
# in the repository or for a commit that is no longer its branch's latest.
Write-Host "0. Checking that no old job waits on GitHub for this PC."
$api = "https://api.github.com/repos/jsab258/ledger"
$hdr = @{ "User-Agent" = "ledger-reconnect" }
$current = (Get-ChildItem "C:\Users\Jafar\ledger-local\.github\workflows\*.yml").Name
$heads = @{}
$stale = @()
foreach ($st in "queued", "pending", "waiting", "requested") {
    $runs = (Invoke-RestMethod -Headers $hdr "$api/actions/runs?status=$st&per_page=100").workflow_runs
    foreach ($r in $runs) {
        if (-not $heads.ContainsKey($r.head_branch)) {
            try { $heads[$r.head_branch] = (Invoke-RestMethod -Headers $hdr "$api/branches/$($r.head_branch)").commit.sha }
            catch { $heads[$r.head_branch] = "" }
        }
        $retired = $current -notcontains (Split-Path $r.path -Leaf)
        $old = $r.head_sha -ne $heads[$r.head_branch]
        if ($retired -or $old) { $stale += $r }
    }
}
if ($stale.Count -gt 0) {
    Write-Host ""
    Write-Host "STOPPED: $($stale.Count) old jobs wait on GitHub and would run on this PC the moment it connects."
    Write-Host "Cancel each (open the link, then 'Cancel workflow'), or wait until GitHub drops them 24 hours"
    Write-Host "after they were made, then run this again. Nothing has been changed."
    foreach ($r in $stale) { Write-Host ("  {0}  ({1}, made {2})  {3}" -f $r.name, $r.head_branch, $r.created_at, $r.html_url) }
    exit 2
}
Write-Host "   none waiting."

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
