# HIS FRIENDS' EVENING, ON HIS OWN ACCOUNT (P5; Jafar, 4 October: "drop P5's fresh Windows account.
# My friends play on my own account, so no second account is needed. The friends' build runs from
# its shortcut on this account, on my key with its five-dollar cap for the evening"; replacing the
# fresh account of 3 October).
#
#   Before the evening, from his own account, in an ordinary PowerShell:
#     powershell -NoProfile -ExecutionPolicy Bypass -File tools\friends\evening.ps1 -Start
#   After it, the same way:
#     powershell -NoProfile -ExecutionPolicy Bypass -File tools\friends\evening.ps1 -End
#
# -Start puts beside his key (AppData\Local\LEDGER, where the game reads it; the key itself stays
# where it is and is never copied) the evening's file (friends-evening.json: five dollars, nothing
# spent), which the talk program reads, starts from and keeps up to date, so a restarted game never
# gets a fresh five dollars (ledger/TalkHelper, EveningCap); an evening already under way is left
# as it is. It puts "Quay Street (friends)" on his desktop, starting the played copy on F: with the
# friends' own saved game, apart from his.
# -End reads what the evening spent, writes it to F:\LedgerTools\friends-evenings\evenings.jsonl,
# and removes the evening's file, so his own play is back on his own daily allowance. His key stays.
#
# No administrator is needed: it writes only into his own folders. It never touches anything else.
param(
    [switch]$Start,
    [switch]$End,
    [double]$CapUsd = 5.0,
    # The builder's own test only: a stand-in folder for his, under F:\LedgerTools\tmp, with its
    # own log.
    [string]$TestFolder = ""
)
$ErrorActionPreference = "Stop"
if ($Start -eq $End) { Write-Host "Say -Start or -End."; exit 2 }

$log = "F:\LedgerTools\friends-evenings\evenings.jsonl"
if ($TestFolder) {
    if (-not $TestFolder.StartsWith("F:\LedgerTools\tmp\", [StringComparison]::OrdinalIgnoreCase)) { Write-Host "A test folder lives under F:\LedgerTools\tmp."; exit 2 }
    $userDir = $TestFolder
    $log = Join-Path $TestFolder "evenings.jsonl"
} else {
    $userDir = [Environment]::GetFolderPath("UserProfile")
}
$ledger = Join-Path $userDir "AppData\Local\LEDGER"
$key = Join-Path $ledger "live-talk-key.txt"
$evening = Join-Path $ledger "friends-evening.json"
$game = "F:\LedgerTools\played-game\Windows\LedgerProbe.exe"
$save = "F:\LedgerTools\friends-evenings\save"

if ($Start) {
    if (-not (Test-Path $key)) { Write-Host "Your key is not where the game keeps it ($key); nothing done."; exit 2 }
    if (-not (Test-Path $game)) { Write-Host "The played copy is not at $game; nothing done."; exit 2 }
    if (Test-Path $evening) {
        Write-Host "An evening is already under way; its spend so far is kept."
    } else {
        ('{"capUsd":' + $CapUsd.ToString([Globalization.CultureInfo]::InvariantCulture) + ',"spentUsd":0}') | Set-Content -Path $evening -Encoding ascii -NoNewline
    }
    New-Item -ItemType Directory -Force -Path $save | Out-Null
    $desk = Join-Path $userDir "Desktop"
    New-Item -ItemType Directory -Force -Path $desk | Out-Null
    $sh = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path $desk "Quay Street (friends).lnk"))
    $sh.TargetPath = $game
    # THE FRIENDS' OWN SAVED GAME, apart from his own play's
    $sh.Arguments = '-EncounterSave="' + $save + '"'
    $sh.WorkingDirectory = Split-Path $game
    $sh.Save()
    Write-Host "Ready: a five-dollar evening is on your key, and Quay Street (friends) is on your desktop."
    exit 0
}

# -End
$spent = $null
if (Test-Path $evening) {
    try { $spent = (Get-Content $evening -Raw | ConvertFrom-Json).spentUsd } catch { $spent = $null }
}
New-Item -ItemType Directory -Force -Path (Split-Path $log) | Out-Null
$row = @{ date = (Get-Date -Format "yyyy-MM-dd HH:mm"); account = "his own"; capUsd = $CapUsd; spentUsd = $spent } | ConvertTo-Json -Compress
Add-Content -Path $log -Value $row
Remove-Item $evening, "$evening.tmp" -Force -ErrorAction SilentlyContinue
if (Test-Path $evening) { Write-Host "The evening's file is STILL there: remove $evening by hand."; exit 1 }
Write-Host ("Done: the evening is closed and your key is untouched. The evening spent " + $(if ($spent -ne $null) { "US$" + ([double]$spent).ToString("0.00", [Globalization.CultureInfo]::InvariantCulture) } else { "an unknown amount (no evening file)" }) + ".")
exit 0
