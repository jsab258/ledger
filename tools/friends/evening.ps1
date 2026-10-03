# HIS FRIENDS' EVENING (P5; Jafar, 3 October: "start the friends' build in a fresh Windows
# account, voice and talk included. For the evening, a copy of my key is placed in that account
# and removed afterwards"; "my friends may talk on my key during the friends' evenings, capped at
# five dollars an evening").
#
#   Before the evening, from his own account, in PowerShell run as administrator:
#     powershell -NoProfile -ExecutionPolicy Bypass -File tools\friends\evening.ps1 -Start
#   After it, the same way:
#     powershell -NoProfile -ExecutionPolicy Bypass -File tools\friends\evening.ps1 -End
#
# -Start puts into the friends' account (default "Friends"; -Account names another):
#   - a copy of his key, beside where the game reads it (AppData\Local\LEDGER\live-talk-key.txt);
#   - the evening's file beside it (friends-evening.json: five dollars, nothing spent), which the
#     talk program reads, starts from and keeps up to date, so a restarted game never gets a fresh
#     five dollars (ledger/TalkHelper, EveningCap); an evening already under way is left as it is;
#   - "Quay Street" on that account's desktop, starting the played copy on F:.
# -End reads what the evening spent, writes it to F:\LedgerTools\friends-evenings\evenings.jsonl,
# and removes the key and the evening's file, then checks they are gone.
#
# Administrator, because only an administrator may write into another account's folder. It
# never touches anything else of either account. The friends' account must have been signed in
# to once, so that Windows has made its folder.
param(
    [switch]$Start,
    [switch]$End,
    [string]$Account = "Friends",
    [double]$CapUsd = 5.0
)
$ErrorActionPreference = "Stop"
if ($Start -eq $End) { Write-Host "Say -Start or -End."; exit 2 }

$admin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
if (-not $admin) { Write-Host "Run PowerShell as administrator (right-click, Run as administrator), then this again."; exit 2 }

$prof = Get-CimInstance Win32_UserProfile | Where-Object { (Split-Path $_.LocalPath -Leaf) -ieq $Account } | Select-Object -First 1
if (-not $prof) { Write-Host "No folder for the account '$Account' yet: sign in to it once, sign out, then run this again."; exit 2 }
$userDir = $prof.LocalPath
$ledger = Join-Path $userDir "AppData\Local\LEDGER"
$key = Join-Path $ledger "live-talk-key.txt"
$evening = Join-Path $ledger "friends-evening.json"
$game = "F:\LedgerTools\played-game\Windows\LedgerProbe.exe"
$log = "F:\LedgerTools\friends-evenings\evenings.jsonl"

if ($Start) {
    $mine = Join-Path ([Environment]::GetFolderPath("LocalApplicationData")) "LEDGER\live-talk-key.txt"
    if (-not (Test-Path $mine)) { Write-Host "Your key is not where the game keeps it ($mine); nothing done."; exit 2 }
    if (-not (Test-Path $game)) { Write-Host "The played copy is not at $game; nothing done."; exit 2 }
    New-Item -ItemType Directory -Force -Path $ledger | Out-Null
    Copy-Item $mine $key -Force
    if (Test-Path $evening) {
        Write-Host "An evening is already under way in '$Account'; its spend so far is kept."
    } else {
        ('{"capUsd":' + $CapUsd.ToString([Globalization.CultureInfo]::InvariantCulture) + ',"spentUsd":0}') | Set-Content -Path $evening -Encoding ascii -NoNewline
    }
    $desk = Join-Path $userDir "Desktop"
    New-Item -ItemType Directory -Force -Path $desk | Out-Null
    $sh = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desk "Quay Street.lnk"))
    $sh.TargetPath = $game
    $sh.WorkingDirectory = Split-Path $game
    $sh.Save()
    Write-Host "Ready: the key and a five-dollar evening are in '$Account', and Quay Street is on its desktop. Sign in there and double-click it."
    exit 0
}

# -End
$spent = $null
if (Test-Path $evening) {
    try { $spent = (Get-Content $evening -Raw | ConvertFrom-Json).spentUsd } catch { $spent = $null }
}
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
$row = @{ date = (Get-Date -Format "yyyy-MM-dd HH:mm"); account = $Account; capUsd = $CapUsd; spentUsd = $spent } | ConvertTo-Json -Compress
Add-Content -Path $log -Value $row
Remove-Item $key, $evening, "$evening.tmp" -Force -ErrorAction SilentlyContinue
if ((Test-Path $key) -or (Test-Path $evening)) { Write-Host "The key or the evening's file is STILL in '$Account': remove $ledger by hand."; exit 1 }
Write-Host ("Done: the key and the evening are gone from '$Account'. The evening spent " + $(if ($spent -ne $null) { "US$" + ([double]$spent).ToString("0.00", [Globalization.CultureInfo]::InvariantCulture) } else { "an unknown amount (no evening file)" }) + ".")
exit 0
