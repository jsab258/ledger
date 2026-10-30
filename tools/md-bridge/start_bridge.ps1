# Starts LEDGER's bridge in Marvelous Designer by invoking its one menu item through Windows UI Automation.
#
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/md-bridge/start_bridge.ps1
#   (normally called by tools/md-bridge/md_job.py when the heartbeat is stale; prints one JSON line)
#
# WHY, 30 October 2026 (his ruling of that morning, RULINGS.md): the bridge must start without him. When
# Marvelous is running and the bridge's heartbeat is older than 30 s, a script invokes Plugins > LEDGER
# bridge through UI Automation: no mouse movement, no keystrokes, no screen takeover. This one menu item in
# Marvelous is the only thing any script may invoke this way; nothing else, in no other app.
#
# HOW. Marvelous 2026.1 is a Qt 6 program, and Qt 6 speaks UI Automation itself (qwindows.dll), so its menu
# bar's items carry the Expand and Invoke patterns. A closed menu's items are not in the tree, so the path is
# walked open: Plugins (expanded), Plug-in (expanded; the bridge's place in pluginSettings.json, "Plugins /
# Plug-in"), LEDGER bridge (invoked), each looked for only under the item before it. Each name is matched
# exactly (trimmed), inside Marvelous's own process only; a missing name stops the walk and closes what was
# opened. Nothing is clicked or typed.
#
# WHEN. Only when Marvelous is running, answering Windows (a job in the bridge keeps its thread busy, and the
# heartbeat waits for it), not running a job (busy.json, newer than this Marvelous), and the heartbeat is over
# 30 s old or says stopped. Every invoke is logged as one line in F:/LedgerTools/md-jobs/starts.jsonl, which
# the day's summary reads.
$ErrorActionPreference = "Stop"
$PATH = @("Plugins", "Plug-in", "LEDGER bridge")      # the only path this script may walk (his ruling)
$EXE = "MarvelousDesigner_Personal"
$ROOT = if ($env:LEDGER_MD_JOBS) { $env:LEDGER_MD_JOBS } else { "F:\LedgerTools\md-jobs" }
$STALE_S = 30

function Say($ok, $note, $extra, [switch]$log) {
  $o = [ordered]@{ ok = $ok; note = $note; at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss") }
  if ($extra) { foreach ($k in $extra.Keys) { $o[$k] = $extra[$k] } }
  $line = ($o | ConvertTo-Json -Compress)
  if ($log) { [System.IO.File]::AppendAllText((Join-Path $ROOT "starts.jsonl"), $line + "`n", (New-Object System.Text.UTF8Encoding($false))) }
  $line
}

$proc = Get-Process $EXE -ErrorAction SilentlyContinue | Select-Object -First 1
if (-not $proc) { Say $false "Marvelous is not running"; exit 1 }
$beat = Join-Path $ROOT "heartbeat.json"
if (Test-Path $beat) {
  $age = ((Get-Date) - (Get-Item $beat).LastWriteTime).TotalSeconds
  $said = Get-Content $beat -Raw | ConvertFrom-Json
  if ($age -le $STALE_S -and -not $said.stopped) { Say $true "already alive (heartbeat $([int]$age) s old)"; exit 0 }
}
$busy = Join-Path $ROOT "busy.json"
if ((Test-Path $busy) -and (Get-Item $busy).LastWriteTime -gt $proc.StartTime) { Say $false "the bridge is running a job"; exit 1 }
if (-not $proc.Responding) { Say $false "Marvelous is busy (not answering Windows)"; exit 1 }

Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$A = [System.Windows.Automation.AutomationElement]
$T = [System.Windows.Automation.TreeScope]
$CT = [System.Windows.Automation.ControlType]
$mine = New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $proc.Id)

function ItemIn($scopeEl, $scope, $name) {
  # one menu item of this exact name under scopeEl, in Marvelous's process only
  $c = New-Object System.Windows.Automation.AndCondition(
    (New-Object System.Windows.Automation.PropertyCondition($A::ControlTypeProperty, $CT::MenuItem)),
    (New-Object System.Windows.Automation.PropertyCondition($A::NameProperty, $name)), $mine)
  $scopeEl.FindFirst($scope, $c)
}

function FindOpen($parent, $name, $seconds) {
  # an item of the menu just opened under $parent (Qt hangs the open popup under its item); Marvelous pads a
  # plug-in's title with spaces ("     LEDGER bridge      ", first try, 30 Oct), so names match trimmed
  $isItem = New-Object System.Windows.Automation.AndCondition(
    (New-Object System.Windows.Automation.PropertyCondition($A::ControlTypeProperty, $CT::MenuItem)), $mine)
  $until = (Get-Date).AddSeconds($seconds)
  while ((Get-Date) -lt $until) {
    foreach ($it in $parent.FindAll($T::Descendants, $isItem)) {
      if ($it.Current.Name.Trim() -ceq $name) { return $it }
    }
    Start-Sleep -Milliseconds 150
  }
  $null
}

function Pattern($el, $p) {
  $o = $null
  if ($el.TryGetCurrentPattern($p, [ref]$o)) { return $o }
  $null
}

$EC = [System.Windows.Automation.ExpandCollapsePattern]::Pattern
$IN = [System.Windows.Automation.InvokePattern]::Pattern
$fore = Add-Type -PassThru -Name Fg -Namespace LedgerUia -MemberDefinition '[DllImport("user32.dll")] public static extern System.IntPtr GetForegroundWindow();'
$before = $fore::GetForegroundWindow()
$opened = @()
try {
  $mainWin = $A::RootElement.FindFirst($T::Children, $mine)
  if (-not $mainWin) { Say $false "Marvelous has no window yet"; exit 1 }
  $top = ItemIn $mainWin $T::Descendants $PATH[0]
  if (-not $top) { Say $false "no '$($PATH[0])' menu in Marvelous's menu bar"; exit 1 }
  (Pattern $top $EC).Expand(); $opened += $top
  $sub = FindOpen $top $PATH[1] 5
  if (-not $sub) { throw "no '$($PATH[1])' item under '$($PATH[0])'" }
  (Pattern $sub $EC).Expand(); $opened += $sub
  $item = FindOpen $sub $PATH[2] 5
  if (-not $item) { throw "no '$($PATH[2])' item under '$($PATH[1])'" }
  $inv = Pattern $item $IN
  if (-not $inv) { throw "'$($PATH[2])' cannot be invoked" }
  $inv.Invoke()
  $opened = @()                                        # invoking the item closes its menus
  $after = $fore::GetForegroundWindow()
  Say $true "invoked $($PATH -join ' > ')" @{ pid = $proc.Id; foregroundChanged = ($before -ne $after) } -log
  exit 0
} catch {
  [array]::Reverse($opened)
  foreach ($el in $opened) { try { (Pattern $el $EC).Collapse() } catch {} }
  Say $false ("stopped: " + $_.Exception.Message) @{ pid = $proc.Id } -log
  exit 1
}
