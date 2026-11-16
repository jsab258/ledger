# Starts LEDGER's bridge in Marvelous Designer by invoking its one menu item through Windows UI Automation.
#
#   powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools/md-bridge/start_bridge.ps1
#   (normally called by tools/md-bridge/md_job.py when the heartbeat is stale; prints one JSON line)
#   ... start_bridge.ps1 -DryRun        read-only: lists Marvelous's copies and windows and says what it would do;
#                                       no message sent, no UI Automation, nothing written
#   ... start_bridge.ps1 -SelfTest      the window picker and restart guard on recorded window lists (no app touched)
#   ... start_bridge.ps1 -AllowRestart  also allows the restart path below (default off)
#
# WHY, 30 October 2026 (his ruling of that morning, RULINGS.md): the bridge must start without him. When
# Marvelous is running and the bridge's heartbeat is older than 30 s, a script invokes Plugins > LEDGER
# bridge through UI Automation: no mouse movement, no keystrokes, no screen takeover.
# 16 November 2026 (his pick A, advisor 174, DECISIONS 12:39): the start recovers by itself. The redesign follows
# production/research/tool-tests-2026-11/BRIDGE-AUTOSTART-DIAGNOSIS-2026-11-16.md (sections 2 and 5):
#  - ONE COPY. Several Marvelous copies can run. The target is the copy the heartbeat names (field "pid", once the
#    bridge writes it), else the copy the task "LEDGER Marvelous open" last opened (marvelous.pid beside
#    starts.jsonl, process id and start time both matching), else the only copy. Several copies and none named:
#    nothing is done (the old script took the lowest process id).
#  - THE MAIN WINDOW BY ITS HANDLE. The old search took "the first window of the process" from the desktop and on
#    16 Nov most likely held the Welcome window (same title, a web page in its own window). The main window is now
#    the process's visible top-level window with no owner whose class ends in QWindowIcon; UI Automation starts
#    from that handle (AutomationElement.FromHandle).
#  - THE WELCOME WINDOW CLOSED BY MESSAGE. A visible window owned by the main window, class ending QWindowOwnDC,
#    titled "Marvelous Designer...", smaller than the main window, is sent WM_CLOSE (what its close button sends;
#    no click, no key). It came back once by hand, so up to three rounds, 5 s apart. Any other window of Marvelous
#    over a disabled main window (a question such as "save changes?") stops the start: nothing is closed then.
#  - THE ITEM INVOKED WITH ITS MENUS SHUT FIRST. Plugins > Plug-in > LEDGER bridge is looked for among the menu
#    items' children without opening anything, and invoked (Invoke pattern). Only if that finds nothing are the
#    menus opened with the Expand pattern (the 30 Oct route). No keyboard route: simulated keys are excluded by
#    RULINGS 1 Nov rule 7 and his 29 and 30 Oct rulings.
#  - EVERY OUTCOME LOGGED in F:/LedgerTools/md-jobs/starts.jsonl (two results were left out before), with the
#    copy, why it was chosen, the window handle and class, the Welcome closes, the route, the front program and
#    the milliseconds taken. A lock (start.lock) keeps two UI Automation clients off one Marvelous.
#  - TIMING. No query before the copy is 60 s old (Qt answers the first UI Automation request itself, the
#    diagnosis section 3; the 120 s wait of 16 Nov rested on a misreading). The whole run stays under 150 s;
#    md_job.py waits 180 s for it.
#  - RESTART, written but off unless -AllowRestart: only a copy the task itself opened (marvelous.pid), in which
#    the bridge never beat and no job ran, with no window of its own over it, at most once in two hours. It is
#    asked to close (CloseMainWindow), and only that process is stopped if it is still there after 60 s. A new
#    copy is then opened in his signed-in session: directly when this runs inside the task (LEDGER_MD_IN_TASK=1,
#    set by open_marvelous.ps1), else by asking the task to run. A copy he opened is never closed or stopped.
#    md_job.py never passes -AllowRestart (a restart can outlast its 180 s); only the task would, once switched on.
#    Closing the Welcome window and the restart go beyond the 30 Oct ruling's "nothing else": his ruling line is
#    for the session to bring in line before the live test.
param([switch]$DryRun, [switch]$SelfTest, [switch]$AllowRestart)
$ErrorActionPreference = "Stop"
$PATH = @("Plugins", "Plug-in", "LEDGER bridge")      # the only path this script may walk (his ruling)
$EXE = "MarvelousDesigner_Personal"
$EXE_PATH = "C:\Program Files\Marvelous Designer Personal\MarvelousDesigner_Personal.exe"
$TASK = "LEDGER Marvelous open"
$ROOT = if ($env:LEDGER_MD_JOBS) { $env:LEDGER_MD_JOBS } else { "F:\LedgerTools\md-jobs" }
$STALE_S = 30
$MIN_AGE_S = 60          # no query before the copy is this old
$MAIN_WAIT_S = 90        # how long from this run's start a main window may take to appear
$BUDGET_S = 150          # the whole run; md_job.py's limit (180 s) is above it
$WELCOME_ROUNDS = 3
$WELCOME_GAP_S = 5
$LOCK_STALE_S = 300
$RESTART_GAP_H = 2
$T0 = Get-Date
$script:ctx = [ordered]@{}
$script:haveLock = $false

function Stamp($t) { if ($t) { $t.ToString("yyyy-MM-dd HH:mm:ss.fff") } else { $null } }
function Hex($h) { "0x{0:X}" -f [int64]$h }

function Say($ok, $note, $extra) {
  $o = [ordered]@{ ok = $ok; note = $note; at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss");
                   ms = [int]((Get-Date) - $T0).TotalMilliseconds }
  foreach ($k in $script:ctx.Keys) { $o[$k] = $script:ctx[$k] }
  if ($extra) { foreach ($k in $extra.Keys) { $o[$k] = $extra[$k] } }
  $line = ($o | ConvertTo-Json -Compress -Depth 5)
  if (-not $DryRun -and -not $SelfTest) {
    [System.IO.File]::AppendAllText((Join-Path $ROOT "starts.jsonl"), $line + "`n", (New-Object System.Text.UTF8Encoding($false)))
  }
  $line
}

function Finish($ok, $note, $extra, $code) {
  # every outcome ends here: one line printed and (outside dry runs) logged, the lock let go
  Write-Output (Say $ok $note $extra)
  if ($script:haveLock) { Remove-Item (Join-Path $ROOT "start.lock") -ErrorAction SilentlyContinue }
  exit $code
}

# ---------------------------------------------------------------- pure parts (the self-test runs these)

function Pick-Target($procs, $beatPid, $record) {
  # $procs: objects with pid and start (DateTime); $record: $null or an object with pid and started (DateTime)
  $running = @($procs)
  $own = { param($p) [bool]($record -and $p.pid -eq $record.pid -and [math]::Abs(($p.start - $record.started).TotalSeconds) -le 2) }
  if ($beatPid) {
    $p = @($running | Where-Object { $_.pid -eq $beatPid })
    if ($p.Count) { return [pscustomobject]@{ pid = $p[0].pid; start = $p[0].start; own = (& $own $p[0]); why = "the bridge's heartbeat names this copy" } }
  }
  if ($record) {
    $p = @($running | Where-Object { & $own $_ })
    if ($p.Count) { return [pscustomobject]@{ pid = $p[0].pid; start = $p[0].start; own = $true; why = "the task opened this copy (marvelous.pid)" } }
  }
  if ($running.Count -eq 1) {
    return [pscustomobject]@{ pid = $running[0].pid; start = $running[0].start; own = (& $own $running[0]); why = "the only copy running" }
  }
  [pscustomobject]@{ pid = $null; start = $null; own = $false;
    why = "$($running.Count) Marvelous copies running, none named by the heartbeat or the task's record; acting on none" }
}

function Classify-Windows($wins, $procId) {
  # verdicts: no-main | blocked (a window of its own over a disabled main window) | close-welcome | go
  $mine = @($wins | Where-Object { $_.Pid -eq $procId -and $_.Visible })
  $mains = @($mine | Where-Object { $_.Owner -eq 0 -and $_.Cls -like '*QWindowIcon' } |
             Sort-Object -Property @{ Expression = { [int64]$_.W * $_.H }; Descending = $true }, @{ Expression = { $_.Z }; Ascending = $true })
  if (-not $mains.Count) { return [pscustomobject]@{ verdict = "no-main"; main = $null; welcome = @(); others = $mine } }
  $main = $mains[0]
  $mainArea = [int64]$main.W * $main.H
  $welcome = @($mine | Where-Object { $_.Owner -eq $main.Hwnd -and $_.Cls -like '*QWindowOwnDC' -and
                                      $_.Title -like 'Marvelous Designer*' -and ([int64]$_.W * $_.H) -lt $mainArea })
  $wh = @($welcome | ForEach-Object { $_.Hwnd })
  $others = @($mine | Where-Object { $_.Hwnd -ne $main.Hwnd -and $wh -notcontains $_.Hwnd })
  $ownedOthers = @($others | Where-Object { $_.Owner -eq $main.Hwnd })
  $v = if (-not $main.Enabled) { if ($ownedOthers.Count -or -not $welcome.Count) { "blocked" } else { "close-welcome" } }
       elseif ($welcome.Count) { "close-welcome" } else { "go" }
  [pscustomobject]@{ verdict = $v; main = $main; welcome = $welcome; others = $others }
}

function Test-RestartAllowed($target, $beatTime, $busyTime, $lastRestart, $now, $verdict) {
  if (-not $target -or -not $target.pid) { return [pscustomobject]@{ ok = $false; why = "no target copy" } }
  if (-not $target.own) { return [pscustomobject]@{ ok = $false; why = "not a copy the task opened; never closed by a script" } }
  if ($verdict -eq "blocked") { return [pscustomobject]@{ ok = $false; why = "a window of its own is open over it (work may be unsaved)" } }
  if ($beatTime -and $beatTime -gt $target.start) { return [pscustomobject]@{ ok = $false; why = "the bridge has run in this copy (garment work may be open)" } }
  if ($busyTime -and $busyTime -gt $target.start) { return [pscustomobject]@{ ok = $false; why = "a job ran in this copy" } }
  if ($lastRestart -and ($now - $lastRestart).TotalHours -lt $RESTART_GAP_H) { return [pscustomobject]@{ ok = $false; why = "restarted less than $RESTART_GAP_H h ago" } }
  [pscustomobject]@{ ok = $true; why = "the task's own copy, no bridge or job ever in it" }
}

function Run-SelfTest {
  $t = Get-Date "2026-11-16 10:18:55"
  function W($h, $p, $cls, $owner, $w, $hh, $z, [bool]$en = $true, $title = "Marvelous Designer Personal") {
    [pscustomobject]@{ Hwnd = $h; Pid = $p; Cls = $cls; Title = $title; Visible = $true; Enabled = $en; Owner = $owner; W = $w; H = $hh; Z = $z }
  }
  $four = @(
    [pscustomobject]@{ pid = 5736; start = $t }, [pscustomobject]@{ pid = 23092; start = $t.AddHours(2.2) },
    [pscustomobject]@{ pid = 6292; start = $t.AddHours(2.21) }, [pscustomobject]@{ pid = 3988; start = $t.AddHours(2.4) })
  $rec = [pscustomobject]@{ pid = 5736; started = $t }
  $cases = @(
    @{ n = "four copies, nothing names one: refused"; v = { -not (Pick-Target $four $null $null).pid } },
    @{ n = "four copies, the task's record: its copy"; v = { $r = Pick-Target $four $null $rec; $r.pid -eq 5736 -and $r.own } },
    @{ n = "record with a reused pid (start differs): refused"; v = { -not (Pick-Target $four $null ([pscustomobject]@{ pid = 5736; started = $t.AddMinutes(-9) })).pid } },
    @{ n = "heartbeat pid outranks the record"; v = { $r = Pick-Target $four 3988 $rec; $r.pid -eq 3988 -and -not $r.own } },
    @{ n = "one copy, no record: that copy, not own"; v = { $r = Pick-Target @($four[1]) $null $null; $r.pid -eq 23092 -and -not $r.own } },
    @{ n = "record's copy gone, two others: refused"; v = { -not (Pick-Target @($four[1], $four[2]) $null $rec).pid } },
    @{ n = "Welcome window over the main window: close it only"; v = {
        $c = Classify-Windows @((W 0x200 6292 "Qt6103QWindowOwnDC" 0x100 960 550 0), (W 0x100 6292 "Qt6103QWindowIcon" 0 1920 1040 1)) 6292
        $c.verdict -eq "close-welcome" -and $c.main.Hwnd -eq 0x100 -and $c.welcome.Count -eq 1 -and $c.welcome[0].Hwnd -eq 0x200 } },
    @{ n = "no Welcome window: go"; v = { (Classify-Windows @((W 0x100 3988 "Qt6103QWindowIcon" 0 1920 1040 0)) 3988).verdict -eq "go" } },
    @{ n = "main disabled under the Welcome window only: close it"; v = {
        (Classify-Windows @((W 0x200 1 "Qt6103QWindowOwnDC" 0x100 960 550 0), (W 0x100 1 "Qt6103QWindowIcon" 0 1920 1040 1 $false)) 1).verdict -eq "close-welcome" } },
    @{ n = "main disabled under another window: stop, nothing closed"; v = {
        $c = Classify-Windows @((W 0x300 1 "Qt6103QWindowIcon" 0x100 400 200 0 $true "Save"), (W 0x200 1 "Qt6103QWindowOwnDC" 0x100 960 550 1), (W 0x100 1 "Qt6103QWindowIcon" 0 1920 1040 2 $false)) 1
        $c.verdict -eq "blocked" } },
    @{ n = "no main window yet"; v = { (Classify-Windows @((W 0x200 1 "Qt6103QWindowOwnDC" 0 960 550 0)) 1).verdict -eq "no-main" } },
    @{ n = "another program's or unowned GL window is never taken for Welcome"; v = {
        $c = Classify-Windows @((W 0x500 2 "Qt6103QWindowOwnDC" 0x100 960 550 0), (W 0x600 1 "Qt6103QWindowOwnDC" 0 960 550 1), (W 0x100 1 "Qt6103QWindowIcon" 0 1920 1040 2)) 1
        $c.verdict -eq "go" -and $c.welcome.Count -eq 0 } },
    @{ n = "restart: not the task's copy refused"; v = { -not (Test-RestartAllowed (Pick-Target @($four[1]) $null $null) $null $null $null $t "go").ok } },
    @{ n = "restart: bridge ran in it refused"; v = { -not (Test-RestartAllowed (Pick-Target $four $null $rec) $t.AddMinutes(5) $null $null $t.AddHours(1) "go").ok } },
    @{ n = "restart: within two hours refused"; v = { -not (Test-RestartAllowed (Pick-Target $four $null $rec) $null $null $t.AddMinutes(30) $t.AddHours(1) "go").ok } },
    @{ n = "restart: window over it refused"; v = { -not (Test-RestartAllowed (Pick-Target $four $null $rec) $null $null $null $t.AddHours(1) "blocked").ok } },
    @{ n = "restart: the task's clean copy allowed"; v = { (Test-RestartAllowed (Pick-Target $four $null $rec) $t.AddMinutes(-5) $null $t.AddHours(-3) $t.AddHours(1) "go").ok } }
  )
  $pass = 0
  foreach ($c in $cases) {
    $r = $false; try { $r = [bool](& $c.v) } catch { $r = $false }
    if ($r) { $pass++ } else { Write-Output "FAIL: $($c.n)" }
  }
  Write-Output ("start_bridge selftest: passed={0}/{1} failed={2}" -f $pass, $cases.Count, ($cases.Count - $pass))
  if ($pass -eq $cases.Count) { 0 } else { 1 }
}

if ($SelfTest) { $r = Run-SelfTest; $code = $r[-1]; $r[0..($r.Count - 2)] | Write-Output; exit $code }

# ---------------------------------------------------------------- reading Windows (no input, no UI Automation)

Add-Type @"
using System; using System.Text; using System.Collections.Generic; using System.Runtime.InteropServices;
namespace LedgerMd {
  public class Win { public long Hwnd; public int Pid; public string Cls; public string Title; public bool Visible;
    public bool Enabled; public long Owner; public int X; public int Y; public int W; public int H; public int Z; }
  public static class Native {
    delegate bool EnumProc(IntPtr h, IntPtr l);
    [StructLayout(LayoutKind.Sequential)] struct RECT { public int L, T, R, B; }
    [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc f, IntPtr l);
    [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll", CharSet=CharSet.Unicode)] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
    [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
    [DllImport("user32.dll")] static extern bool IsWindowEnabled(IntPtr h);
    [DllImport("user32.dll")] static extern IntPtr GetWindow(IntPtr h, uint cmd);
    [DllImport("user32.dll")] static extern bool GetWindowRect(IntPtr h, out RECT r);
    [DllImport("user32.dll")] static extern IntPtr GetForegroundWindow();
    [DllImport("user32.dll")] static extern bool PostMessage(IntPtr h, uint m, IntPtr w, IntPtr l);
    // top-level windows of the given processes only, in stacking order (Z 0 = top); other programs' titles are not read
    public static Win[] TopLevel(int[] pids) {
      var hs = new List<IntPtr>();
      EnumWindows(delegate(IntPtr h, IntPtr l) { hs.Add(h); return true; }, IntPtr.Zero);
      var res = new List<Win>();
      for (int i = 0; i < hs.Count; i++) {
        IntPtr h = hs[i]; uint pid; GetWindowThreadProcessId(h, out pid);
        if (Array.IndexOf(pids, (int)pid) < 0) continue;
        var w = new Win(); w.Hwnd = h.ToInt64(); w.Pid = (int)pid; w.Z = i;
        var sb = new StringBuilder(256); GetClassName(h, sb, 256); w.Cls = sb.ToString();
        var tb = new StringBuilder(512); GetWindowText(h, tb, 512); w.Title = tb.ToString();
        w.Visible = IsWindowVisible(h); w.Enabled = IsWindowEnabled(h); w.Owner = GetWindow(h, 4).ToInt64();
        RECT r; if (GetWindowRect(h, out r)) { w.X = r.L; w.Y = r.T; w.W = r.R - r.L; w.H = r.B - r.T; }
        res.Add(w);
      }
      return res.ToArray();
    }
    public static int ForegroundPid() { uint pid; GetWindowThreadProcessId(GetForegroundWindow(), out pid); return (int)pid; }
    // WM_CLOSE (0x0010): asks the window to close, as its own close button does; no click, no key
    public static bool PostClose(long h) { return PostMessage(new IntPtr(h), 0x0010, IntPtr.Zero, IntPtr.Zero); }
  }
}
"@

function Front {
  $fp = [LedgerMd.Native]::ForegroundPid()
  $n = (Get-Process -Id $fp -ErrorAction SilentlyContinue).ProcessName
  if ($n) { $n } else { "pid $fp" }
}
function Describe($w) {
  [ordered]@{ hwnd = (Hex $w.Hwnd); cls = $w.Cls; title = $w.Title; owner = (Hex $w.Owner); enabled = $w.Enabled; size = "$($w.W)x$($w.H)"; z = $w.Z }
}
function Read-Json($p) { try { Get-Content $p -Raw | ConvertFrom-Json } catch { $null } }

$procs = @(Get-Process $EXE -ErrorAction SilentlyContinue | ForEach-Object { [pscustomobject]@{ pid = $_.Id; start = $_.StartTime } })
$script:ctx.copies = @($procs | ForEach-Object { $_.pid })

$beatPath = Join-Path $ROOT "heartbeat.json"
$beatTime = $null; $beatAge = $null; $said = $null; $beatPid = $null
if (Test-Path $beatPath) {
  $beatTime = (Get-Item $beatPath).LastWriteTime
  $beatAge = ((Get-Date) - $beatTime).TotalSeconds
  $said = Read-Json $beatPath
  if ($said -and $said.PSObject.Properties["pid"]) { $beatPid = [int]$said.pid }
}
$alive = ($beatTime -and $beatAge -le $STALE_S -and $said -and -not $said.PSObject.Properties["stopped"])
$recPath = Join-Path $ROOT "marvelous.pid"
$record = $null
$rj = if (Test-Path $recPath) { Read-Json $recPath } else { $null }
if ($rj -and $rj.pid -and $rj.started) { $record = [pscustomobject]@{ pid = [int]$rj.pid; started = [datetime]::Parse($rj.started) } }
$busyPath = Join-Path $ROOT "busy.json"
$busyTime = if (Test-Path $busyPath) { (Get-Item $busyPath).LastWriteTime } else { $null }

$target = Pick-Target $procs $beatPid $record
$script:ctx.target = $target.pid
$script:ctx.why = $target.why

# ---------------------------------------------------------------- dry run: list, judge, do nothing
if ($DryRun) {
  $pids = [int[]]@($procs | ForEach-Object { $_.pid })
  $wins = if ($pids.Count) { [LedgerMd.Native]::TopLevel($pids) } else { @() }
  $copies = @(foreach ($p in $procs) {
    $c = Classify-Windows $wins $p.pid
    [ordered]@{ pid = $p.pid; started = (Stamp $p.start); verdict = $c.verdict;
      main = $(if ($c.main) { Hex $c.main.Hwnd } else { $null });
      welcomeToClose = @($c.welcome | ForEach-Object { Hex $_.Hwnd });
      visibleWindows = @($wins | Where-Object { $_.Pid -eq $p.pid -and $_.Visible } | ForEach-Object { Describe $_ }) }
  })
  $would = if (-not $procs.Count) { "nothing: Marvelous is not running" }
    elseif ($alive) { "nothing: the bridge is alive (heartbeat $([int]$beatAge) s old)" }
    elseif (-not $target.pid) { "nothing: $($target.why)" }
    else {
      $c = Classify-Windows $wins $target.pid
      switch ($c.verdict) {
        "no-main" { "wait up to $MAIN_WAIT_S s for pid $($target.pid)'s main window, then stop" }
        "blocked" { "stop: pid $($target.pid)'s main window is disabled under a window of its own; nothing closed" }
        "close-welcome" { "send WM_CLOSE to $((@($c.welcome | ForEach-Object { Hex $_.Hwnd })) -join ', ') (pid $($target.pid)), then invoke the menu item from main window $(Hex $c.main.Hwnd)" }
        default { "invoke the menu item from main window $(Hex $c.main.Hwnd) (pid $($target.pid))" }
      }
    }
  $restart = Test-RestartAllowed $target $beatTime $busyTime $null (Get-Date) "go"
  $o = [ordered]@{ dryRun = $true; at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss");
    heartbeat = [ordered]@{ age_s = $(if ($beatAge -ne $null) { [int]$beatAge } else { $null }); pid = $beatPid; alive = [bool]$alive; stopped = [bool]($said -and $said.PSObject.Properties["stopped"]) };
    record = $(if ($record) { [ordered]@{ pid = $record.pid; started = (Stamp $record.started) } } else { "none (marvelous.pid absent)" });
    target = $target.pid; why = $target.why; wouldDo = $would;
    restartIfAllowed = "$($restart.ok): $($restart.why) (switch $(if ($AllowRestart) { 'on' } else { 'off' }))";
    front = (Front); copies = $copies }
  $o | ConvertTo-Json -Depth 6
  exit 0
}

# ---------------------------------------------------------------- acting run
if (-not $procs.Count) { Finish $false "Marvelous is not running" $null 1 }
if ($alive) { Finish $true "already alive (heartbeat $([int]$beatAge) s old)" $null 0 }
if (-not $target.pid) { Finish $false $target.why $null 1 }
$proc = Get-Process -Id $target.pid -ErrorAction SilentlyContinue
if (-not $proc) { Finish $false "the chosen copy closed" $null 1 }
if ($busyTime -and $busyTime -gt $proc.StartTime) { Finish $false "the bridge is running a job" $null 1 }
if (-not $proc.Responding) { Finish $false "Marvelous is busy (not answering Windows)" $null 1 }

# one UI Automation client at a time (diagnosis 1: two overlapped on 16 Nov)
$lockPath = Join-Path $ROOT "start.lock"
if (Test-Path $lockPath) {
  $lk = Read-Json $lockPath
  $lkAge = ((Get-Date) - (Get-Item $lockPath).LastWriteTime).TotalSeconds
  if ($lkAge -lt $LOCK_STALE_S -and $lk -and (Get-Process -Id ([int]$lk.pid) -ErrorAction SilentlyContinue)) {
    Finish $false "another start is running (pid $($lk.pid), $([int]$lkAge) s)" $null 1
  }
}
[System.IO.File]::WriteAllText($lockPath, (@{ pid = $PID; at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss") } | ConvertTo-Json -Compress))
$script:haveLock = $true

function Last-Restart {
  $p = Join-Path $ROOT "restarts.jsonl"
  if (-not (Test-Path $p)) { return $null }
  $l = @(Get-Content $p | Where-Object { $_.Trim() })
  if (-not $l.Count) { return $null }
  try { [datetime]::Parse(($l[-1] | ConvertFrom-Json).at) } catch { $null }
}

function Write-Record($p, $by) {
  [System.IO.File]::WriteAllText($recPath, ([ordered]@{ pid = $p.Id; started = (Stamp $p.StartTime); by = $by;
    at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss") } | ConvertTo-Json -Compress))
}

function Fail($note, $verdict) {
  # the restart path (off unless -AllowRestart); then the failure is logged
  if (-not $AllowRestart) { Finish $false $note @{ restart = "switch off" } 1 }
  if ($script:restarting) { Finish $false $note @{ restart = "failed part-way" } 1 }   # never a second restart in one run
  $script:restarting = $true
  $chk = Test-RestartAllowed $target $beatTime $busyTime (Last-Restart) (Get-Date) $verdict
  if (-not $chk.ok) { Finish $false $note @{ restart = "no: $($chk.why)" } 1 }
  $old = Get-Process -Id $target.pid -ErrorAction SilentlyContinue
  $how = "already gone"
  if ($old) {
    $old.CloseMainWindow() | Out-Null
    if ($old.WaitForExit(60000)) { $how = "closed" }
    else { Stop-Process -Id $target.pid -Force; $how = "stopped after 60 s" }   # this one recorded process only
  }
  [System.IO.File]::AppendAllText((Join-Path $ROOT "restarts.jsonl"),
    ((@{ at = (Get-Date -Format "yyyy-MM-dd HH:mm:ss"); pid = $target.pid; how = $how; reason = $note } | ConvertTo-Json -Compress) + "`n"),
    (New-Object System.Text.UTF8Encoding($false)))
  if ($env:LEDGER_MD_IN_TASK -eq "1") {
    $new = Start-Process -FilePath $EXE_PATH -WorkingDirectory (Split-Path $EXE_PATH) -PassThru
    Write-Record $new "start_bridge.ps1 restart"
    Finish $false $note @{ restart = "pid $($target.pid) $how; opened pid $($new.Id), the task's next try starts the bridge" } 1
  }
  & schtasks.exe /run /tn $TASK | Out-Null
  Finish $false $note @{ restart = "pid $($target.pid) $how; asked the task '$TASK' (exit $LASTEXITCODE) to open a new copy" } 1
}

# settle: the copy at least MIN_AGE_S old and its main window up
$young = $MIN_AGE_S - ((Get-Date) - $proc.StartTime).TotalSeconds
if ($young -gt 0) { Start-Sleep -Seconds ([int][math]::Ceiling($young)) }
$c = $null
while ($true) {
  $c = Classify-Windows ([LedgerMd.Native]::TopLevel([int[]]@($target.pid))) $target.pid
  if ($c.verdict -ne "no-main" -or ((Get-Date) - $T0).TotalSeconds -gt $MAIN_WAIT_S) { break }
  Start-Sleep -Seconds 5
}
if ($c.verdict -eq "no-main") { Fail "Marvelous has no main window yet" "no-main" }

# the Welcome window (or its like) closed by message, up to three rounds
$closed = @()
for ($r = 0; $r -lt $WELCOME_ROUNDS -and $c.verdict -eq "close-welcome"; $r++) {
  foreach ($w in $c.welcome) { if ([LedgerMd.Native]::PostClose($w.Hwnd)) { $closed += (Hex $w.Hwnd) } }
  Start-Sleep -Seconds $WELCOME_GAP_S
  $c = Classify-Windows ([LedgerMd.Native]::TopLevel([int[]]@($target.pid))) $target.pid
}
$script:ctx.welcomeClosed = $closed
$script:ctx.windows = @($c.others | ForEach-Object { "$(Hex $_.Hwnd) $($_.Cls) $($_.W)x$($_.H)" })
if ($c.verdict -eq "no-main") { Fail "the main window went away" "no-main" }
if ($c.verdict -eq "blocked") { Fail "the main window is disabled under a window of its own; nothing closed" "blocked" }
if ($c.verdict -eq "close-welcome") { Fail "the Welcome window is still open after $WELCOME_ROUNDS closes" "close-welcome" }
$script:ctx.hwnd = Hex $c.main.Hwnd
$script:ctx.cls = $c.main.Cls
$script:ctx.front = Front

# ---------------------------------------------------------------- UI Automation: the one menu item
Add-Type -AssemblyName UIAutomationClient, UIAutomationTypes
$A = [System.Windows.Automation.AutomationElement]
$T = [System.Windows.Automation.TreeScope]
$CT = [System.Windows.Automation.ControlType]
$mine = New-Object System.Windows.Automation.PropertyCondition($A::ProcessIdProperty, $target.pid)
$isItem = New-Object System.Windows.Automation.AndCondition(
  (New-Object System.Windows.Automation.PropertyCondition($A::ControlTypeProperty, $CT::MenuItem)), $mine)
$isMenu = New-Object System.Windows.Automation.AndCondition(
  (New-Object System.Windows.Automation.PropertyCondition($A::ControlTypeProperty, $CT::Menu)), $mine)
$isBar = New-Object System.Windows.Automation.AndCondition(
  (New-Object System.Windows.Automation.PropertyCondition($A::ControlTypeProperty, $CT::MenuBar)), $mine)
$EC = [System.Windows.Automation.ExpandCollapsePattern]::Pattern
$IN = [System.Windows.Automation.InvokePattern]::Pattern
$script:ctx.steps = @()
$script:lap = Get-Date
function Step($name) {
  $script:ctx.steps += "$name $([int]((Get-Date) - $script:lap).TotalMilliseconds) ms"; $script:lap = Get-Date
  if (((Get-Date) - $T0).TotalSeconds -gt $BUDGET_S) { throw "out of time after '$name' ($BUDGET_S s)" }
}
function Pattern($el, $p) { $o = $null; if ($el.TryGetCurrentPattern($p, [ref]$o)) { return $o }; $null }
function NamedItem($el, $name) {
  # Marvelous pads a plug-in's title with spaces ("     LEDGER bridge      ", 30 Oct): names match trimmed
  foreach ($ch in $el.FindAll($T::Children, $isItem)) { if ($ch.Current.Name.Trim() -ceq $name) { return $ch } }
  $null
}
function ShutChild($el, $name) {
  # an item reached with its menu shut: a child of the item, or of a Menu element directly under it
  $hit = NamedItem $el $name; if ($hit) { return $hit }
  foreach ($m in $el.FindAll($T::Children, $isMenu)) { $hit = NamedItem $m $name; if ($hit) { return $hit } }
  $null
}
function FindOpen($parent, $name, $seconds) {
  # an item of the menu just opened under $parent (Qt hangs the open popup under its item)
  $until = (Get-Date).AddSeconds($seconds)
  while ((Get-Date) -lt $until) {
    foreach ($it in $parent.FindAll($T::Descendants, $isItem)) { if ($it.Current.Name.Trim() -ceq $name) { return $it } }
    Start-Sleep -Milliseconds 150
  }
  $null
}

$opened = @()
try {
  $mainEl = $A::FromHandle([IntPtr]$c.main.Hwnd)
  Step "window"
  # children only, never the whole window; the bar a level or a few down; other top-level windows skipped
  $bar = $null; $level = @($mainEl)
  for ($d = 0; $d -lt 4 -and -not $bar -and $level.Count -gt 0; $d++) {
    $next = @()
    foreach ($el in $level) {
      $bar = $el.FindFirst($T::Children, $isBar); if ($bar) { break }
      foreach ($ch in $el.FindAll($T::Children, $mine)) {
        $ct = $ch.Current.ControlType
        if ($ct -eq $CT::Window -and $ch.Current.NativeWindowHandle -ne 0 -and $ch.Current.NativeWindowHandle -ne $c.main.Hwnd) { continue }
        if ($ct -eq $CT::Pane -or $ct -eq $CT::Group -or $ct -eq $CT::Custom -or $ct -eq $CT::Window) { $next += $ch }
      }
    }
    $level = $next
  }
  Step "menu bar"
  if (-not $bar) { Fail "no menu bar among Marvelous's main window's children" "go" }
  $top = NamedItem $bar $PATH[0]
  Step "'$($PATH[0])'"
  if (-not $top) { Fail "no '$($PATH[0])' menu in Marvelous's menu bar" "go" }

  # route 1: menus shut
  $route = "menus shut"
  $sub = ShutChild $top $PATH[1]
  $item = if ($sub) { ShutChild $sub $PATH[2] } else { $null }
  $inv = if ($item) { Pattern $item $IN } else { $null }
  Step "shut walk"
  if (-not $inv) {
    # route 2: menus opened by the Expand pattern (the 30 Oct route)
    $route = "menus expanded (shut walk: " + $(if ($item) { "item had no Invoke" } elseif ($sub) { "no '$($PATH[2])'" } else { "no '$($PATH[1])'" }) + ")"
    $e = Pattern $top $EC; if (-not $e) { throw "'$($PATH[0])' cannot be expanded" }
    $e.Expand(); $opened += $top
    $sub = FindOpen $top $PATH[1] 5
    if (-not $sub) { throw "no '$($PATH[1])' item under '$($PATH[0])'" }
    $e = Pattern $sub $EC; if (-not $e) { throw "'$($PATH[1])' cannot be expanded" }
    $e.Expand(); $opened += $sub
    $item = FindOpen $sub $PATH[2] 5
    if (-not $item) { throw "no '$($PATH[2])' item under '$($PATH[1])'" }
    $inv = Pattern $item $IN
    if (-not $inv) { throw "'$($PATH[2])' cannot be invoked" }
    Step "expand walk"
  }
  $fgBefore = Front
  $inv.Invoke()
  $opened = @()                                        # invoking the item closes its menus
  Step "invoke"
  Finish $true "invoked $($PATH -join ' > ')" @{ route = $route; frontAfter = (Front); frontChanged = ($fgBefore -ne (Front)) } 0
} catch {
  [array]::Reverse($opened)
  foreach ($el in $opened) { try { (Pattern $el $EC).Collapse() } catch {} }
  Fail ("stopped: " + $_.Exception.Message) "go"
}
