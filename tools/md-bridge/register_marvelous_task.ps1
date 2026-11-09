# Registers the Windows task "LEDGER Marvelous open" (his yes, 9 November 2026, marvelous-task-2026-11-09).
# Interactive token: it runs only in his signed-in desktop and needs no password. No trigger: a session runs it
# with  schtasks /run /tn "LEDGER Marvelous open". Delete it any time with
#   Unregister-ScheduledTask -TaskName "LEDGER Marvelous open" -Confirm:$false
$ErrorActionPreference = "Stop"
$script = Join-Path (Split-Path -Parent $MyInvocation.MyCommand.Path) "open_marvelous.ps1"
$user = "$env:USERDOMAIN\$env:USERNAME"
$action = New-ScheduledTaskAction -Execute "powershell.exe" -Argument "-NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File `"$script`""
$principal = New-ScheduledTaskPrincipal -UserId $user -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -ExecutionTimeLimit (New-TimeSpan -Minutes 15) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName "LEDGER Marvelous open" -Description "Opens Marvelous Designer on his desktop and starts LEDGER's bridge (his yes, 9 Nov 2026). Runs only while he is signed in." -Action $action -Principal $principal -Settings $settings -Force | Out-Null
Get-ScheduledTask -TaskName "LEDGER Marvelous open" | Select-Object TaskName, State, @{n='Logon';e={$_.Principal.LogonType}} | Format-List
