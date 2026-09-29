# THE TALK PROGRAM AS IT SHIPS (town list 6aa, 28 September): one Windows
# program that needs no .NET installed, with the cast's cards and the named
# cast's routines beside it, so it runs on a friend's PC with no project folder.
#
#   powershell -File tools/publish-talk-helper.ps1 [-Out F:\town-scratch\talk]
#
# The game copies the folder into its own and starts LedgerTalk.exe from there:
# through the relay for a friend's copy (--relay <address> --copy <code>), with
# LEDGER's own capped live-talk key for Jafar's own, which the game puts into
# its environment only while he plays (CrimeProbe.cpp TalkKeyForThisRun; 29
# September). The output goes to drive F by default, not C.
param([string]$Out = "F:\town-scratch\talk")
$ErrorActionPreference = "Stop"
$repo = Split-Path -Parent $PSScriptRoot
dotnet publish (Join-Path $repo "ledger\TalkHelper\TalkHelper.csproj") -c Release -r win-x64 --self-contained true `
  -p:PublishSingleFile=true -p:IncludeNativeLibrariesForSelfExtract=true -p:AssemblyName=LedgerTalk -o $Out
if ($LASTEXITCODE -ne 0) { throw "publish failed" }
$cards = Join-Path $Out "cards"
New-Item -ItemType Directory -Force $cards | Out-Null
Copy-Item (Join-Path $repo "production\cast\cards\*.md") $cards -Force
Copy-Item (Join-Path $repo "production\specs\hook-cast.json") (Join-Path $Out "hook-cast.json") -Force
Get-ChildItem $Out -Filter *.pdb | ForEach-Object { Remove-Item $_.FullName }
"published to $Out"
