<#
.SYNOPSIS
  Prove the LEDGER daemon fleet starts WITHOUT a console window and stays up.
  Registers nothing, enables nothing, starts no scheduled task.

.DESCRIPTION
  Moved out of ledger-install-supervisor-task.yml on 2026-09-11 and otherwise
  unchanged. The step that held it measured 27467 characters against a
  MEASURED dispatch ceiling of 23184 (tools/workflow-size.py): the commit
  would have been green and the 422 would have arrived the first time
  somebody dispatched the very job written to prove the fleet. Out here it is
  also parsed by PowerShell's own parser on every run, through
  tools/ps-check.py's SCRIPTS list, rather than only by hand.

  WHAT IT ANSWERS. Section 1 of
  game-design/decision-2026-09-11-ruling-the-windowless-fleet-and-four-
  smaller-calls.md, the re-enable condition: fixCommit, the ast check's
  noWindowSites and unflagged on THAT checkout, taskRegistered and taskEnabled
  read at proof start, survivedSec per process against the window, and
  windowlessSamples with handlesNonZero and a CUMULATIVE conhostChildren.

  IT READS THE TASK AND NEVER WRITES IT. Register-ScheduledTask,
  Enable-ScheduledTask and Start-ScheduledTask are named in this sentence and
  called nowhere: this paragraph is the only place those three words appear in
  this file, which is a claim a grep settles in one line. The
  fleet is started by hand through tools/runner/launch-supervisor.py from a
  DELIBERATELY CONSOLE-LESS parent (CreateProcess with DETACHED_PROCESS,
  never Start-Process, which would hand the fleet this session's console and
  manufacture a windowless verdict), and the task's LastRunTime is printed
  before and after as the evidence that nothing here started it.

  RUNNABLE BY HAND ON THE PC, which is worth having the first time this is
  debugged: everything it needs is a parameter, and it finds
  process-query.ps1 and install-scheduled-task.ps1 beside itself rather than
  through a workflow workspace.

.EXAMPLE
  pwsh -File tools\runner\prove-windowless.ps1 -WindowSeconds 300

.EXAMPLE
  The instrument's own rejecting fixture, which the ruling requires FIRST.
  Point it at a checkout of the pre-fix commit:
  pwsh -File tools\runner\prove-windowless.ps1 -ProofRepo C:\Users\Jafar\ledger-prefix -WindowSeconds 120
#>
[CmdletBinding()]
param(
    # Which checkout to start the fleet from. Empty means the one the
    # registered task holds, then the installer's stable path.
    [string]$ProofRepo = "",
    # Seconds to watch AFTER the fleet is up. A rejecting run is capped at
    # 120 and stops at the first sighting.
    [string]$WindowSeconds = "300",
    [string]$OutFile = "production/pc-ops/windowless-proof.txt",
    [string]$TaskName = "LEDGER supervisor",
    # The commit line 1 of the evidence file names.
    [string]$Sha = "$env:GITHUB_SHA"
)

$ErrorActionPreference = "Continue"
# THE EVIDENCE PATH IS RESOLVED ONCE, ABSOLUTELY. Run by hand from another
# directory, a relative path would put the file somewhere nobody looks.
$script:out = if ([System.IO.Path]::IsPathRooted($OutFile)) { $OutFile }
              else { [System.IO.Path]::GetFullPath((Join-Path (Get-Location) $OutFile)) }
New-Item -ItemType Directory -Force -Path (Split-Path -Parent $script:out) | Out-Null
$script:lines = New-Object System.Collections.Generic.List[string]
function Say([string]$t) {
  # FLUSHED EVERY LINE. A step killed by its own timeout still
  # leaves the series it had printed, which is the difference
  # between a partial reading and no reading at all.
  $script:lines.Add($t)
  Write-Host $t
  ($script:lines -join "`n") | Set-Content $script:out -Encoding utf8
}
$sha = $Sha
if ($sha) { $sha = $sha.Substring(0, [Math]::Min(7, $sha.Length)) } else { $sha = "SHA-UNKNOWN" }
$stamp = [DateTimeOffset]::UtcNow.ToUnixTimeSeconds()
Say "# LEDGER windowless fleet proof - $sha @$stamp"
Say "# Line 1 names the commit this was measured on."
Say "# THIS RUN DID NOT REGISTER, ENABLE OR START THE SCHEDULED TASK."
Say "# It starts the fleet by hand through tools/runner/launch-supervisor.py"
Say "# from a DELIBERATELY CONSOLE-LESS parent (CreateProcess with"
Say "# DETACHED_PROCESS), which is the scheduled task's condition and the"
Say "# condition a .bat double-click never reproduces: a console-subsystem"
Say "# child of a parent with no console allocates its own console window."
Say "# Two readings per sample, because either alone could miss it: the"
Say "# MainWindowHandle of every process in the tree, and every conhost.exe"
Say "# or OpenConsole.exe whose parent is in the tree. The conhost tally is"
Say "# CUMULATIVE over the window (distinct pids), never last-wins."
Say "# CADENCE=1s, SAID OUT LOUD: a git child can live under a second, so"
Say "# this sampler can miss one. That is why the ruling also requires the"
Say "# same step to have printed WINDOWS-SEEN on the pre-fix checkout."

function Check-DoneLine([string]$line) {
  # A KEY WITH AN EMPTY VALUE IS NOT A READING. PowerShell
  # interpolates an unset variable as the empty string, so
  # "verdict=" would ship looking like a line that ran. Found by
  # running this formatter on Linux with planted values, which is
  # the only half of this step that can be exercised off Windows.
  $empty = @([regex]::Matches($line, '([A-Za-z]+)=(?=\s|$)') |
             ForEach-Object { $_.Groups[1].Value })
  if ($empty.Count -gt 0) {
    Say "doneLineEmptyValues=$($empty -join ',')/$($empty.Count)"
  }
  Say $line
}
function Finish([string]$verdict, [string]$why) {
  Say ""
  Check-DoneLine ("windowless-proof: fixCommit=$script:fixCommit " +
       "noWindowSites=$script:noWindowSites unflagged=$script:unflagged " +
       "role=$script:role taskRegistered=$script:taskRegistered " +
       "taskEnabled=$script:taskEnabled windowSec=0 samplesTaken=0 " +
       "windowlessSamples=0/0 handlesNonZero=nothing-measured " +
       "conhostChildren=nothing-measured transientChildrenSeen=0 " +
       "processesWatched=0/0 survivedSec=nothing-measured/300 " +
       "restartsObserved=0 verdict=$verdict notMeasuredWhy=$why")
  exit 0
}
$script:fixCommit = "unknown"
$script:noWindowSites = "nothing-measured"
$script:unflagged = "nothing-measured"
$script:role = "unknown"
$script:taskRegistered = "unknown"
$script:taskEnabled = "unknown"

Say ""
# A VALUE THAT CAN BE EMPTY IS NAMED WHEN IT IS. Running this on Linux to
# exercise the refusal path printed `runnerAccount=\`, a lone separator, and
# a key with nothing after it reads as a measurement rather than as a gap.
$acct = "$env:COMPUTERNAME\$env:USERNAME"
if ($acct -eq "\") { $acct = "unreadable-no-COMPUTERNAME-or-USERNAME" }
Say "runnerAccount=$acct"
$mySession = (Get-Process -Id $PID).SessionId
Say "runnerSessionId=$mySession"
Say "# MainWindowHandle is readable for processes in this session; a fleet"
Say "# started here runs in THIS session, so compare runnerSessionId with"
Say "# the per-process session= below before reading a 0 as reassurance."

# ---- THE TASK, READ AND NEVER WRITTEN ------------------------
$task0 = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
$info0 = $null
if ($task0) { $info0 = Get-ScheduledTaskInfo -TaskName $TaskName -ErrorAction SilentlyContinue }
$script:taskRegistered = "$([bool]$task0)"
$script:taskEnabled = if ($task0) { "$($task0.Settings.Enabled)" } else { "no-task-registered" }
$taskState0 = if ($task0) { "$($task0.State)" } else { "none" }
$lastRun0 = if ($info0 -and $info0.LastRunTime) { $info0.LastRunTime.ToString("o") } else { "none" }
Say "taskRegistered=$script:taskRegistered taskEnabled=$script:taskEnabled taskState=$taskState0 taskLastRunBefore=$lastRun0"

# ---- WHICH CHECKOUT, AND WHICH INTERPRETER -------------------
# PRECEDENCE, NAMED: the input wins (that is how the pre-fix
# fixture is pointed at), then the WorkingDirectory the REGISTERED
# TASK holds, which is the strongest available answer to "the same
# interpreter the task would use" because it is read from the task
# itself rather than re-derived, then the installer's stable path.
$repoSource = "input"
$repo = "$ProofRepo".Trim()
if (-not $repo -and $task0) {
  $a0 = $task0.Actions | Select-Object -First 1
  if ($a0 -and $a0.WorkingDirectory) { $repo = $a0.WorkingDirectory; $repoSource = "registered-task" }
}
if (-not $repo) {
  $repo = "C:\Users\Jafar\ledger-migrate"
  $repoSource = "installer-stable-path-literal"
  # ONE IDEA, TWO FILES, SO THE COPY IS CHECKED. This literal also
  # lives in install-scheduled-task.ps1's Find-Repo. If that one
  # moves and this one does not, the proof measures a different
  # checkout from the one the task starts, and says so here rather
  # than quietly proving the wrong tree.
  $inst = Join-Path $PSScriptRoot "install-scheduled-task.ps1"
  $instText = if (Test-Path $inst) { Get-Content $inst -Raw } else { "" }
  if ($instText -notmatch [regex]::Escape('C:\Users\$TargetUser\ledger-migrate')) {
    Finish "NOT-MEASURED" "the-installers-stable-path-no-longer-matches-this-steps-literal"
  }
}
Say "proofRepo=$($repo -replace ' ','~') proofRepoSource=$repoSource"
if (-not (Test-Path (Join-Path $repo "CLAUDE.md"))) {
  Finish "NOT-MEASURED" "no-checkout-at-$($repo -replace ' ','~')"
}
$launcher = Join-Path $repo "tools\runner\launch-supervisor.py"
if (-not (Test-Path $launcher)) {
  Finish "NOT-MEASURED" "no-launch-supervisor-py-in-that-checkout"
}
$script:fixCommit = (& git -C $repo rev-parse HEAD 2>$null)
if (-not $script:fixCommit) { $script:fixCommit = "unreadable" }
$branchDesc = (& git -C $repo log -1 --format=%cI 2>$null)
Say "fixCommit=$script:fixCommit fixCommitDate=$branchDesc"

$pythonw = ""
if ($task0) {
  $a0 = $task0.Actions | Select-Object -First 1
  if ($a0 -and $a0.Execute -and (Test-Path $a0.Execute)) { $pythonw = $a0.Execute }
}
$interpreterSource = "registered-task"
if (-not $pythonw) {
  $interpreterSource = "derived-same-order-as-Find-Python"
  foreach ($c in @((Join-Path $repo "tools\voice-live\env-export\Scripts\pythonw.exe"),
                   (Join-Path $env:USERPROFILE "miniconda3\pythonw.exe"))) {
    if (Test-Path $c) { $pythonw = $c; break }
  }
  if (-not $pythonw) {
    $onPath = Get-Command pythonw.exe -ErrorAction SilentlyContinue
    if ($onPath) { $pythonw = $onPath.Source }
  }
}
if (-not $pythonw -or -not ($pythonw -match 'pythonw\.exe$')) {
  Finish "NOT-MEASURED" "no-windowless-interpreter-found-so-nothing-here-could-prove-a-windowless-start"
}
Say "pythonForProof=$($pythonw -replace ' ','~') interpreterSource=$interpreterSource windowless=True"
$pythonc = Join-Path (Split-Path -Parent $pythonw) "python.exe"
if (-not (Test-Path $pythonc)) {
  $cmd = Get-Command python.exe -ErrorAction SilentlyContinue
  $pythonc = if ($cmd) { $cmd.Source } else { "" }
}

# ---- THE ast CHECK ON THAT CHECKOUT, WHICH SETS THE ROLE ------
$lint = Join-Path $repo "tools\lint-no-window.py"
$lintLine = ""
if ((Test-Path $lint) -and $pythonc) {
  $lintOut = & $pythonc $lint 2>&1
  $lintLine = ($lintOut | Select-String -Pattern 'noWindowSites=' | Select-Object -Last 1)
  if ($lintLine) { $lintLine = "$lintLine" }
}
if ($lintLine -match 'noWindowSites=(\S+)\s+unflagged=(\d+)') {
  $script:noWindowSites = $Matches[1]
  $script:unflagged = $Matches[2]
} elseif (-not (Test-Path $lint)) {
  $script:noWindowSites = "no-ast-check-in-that-checkout"
  $script:unflagged = "unknown"
} else {
  $script:noWindowSites = "ast-check-would-not-run"
  $script:unflagged = "unknown"
}
Say "astCheck=$($script:noWindowSites) unflagged=$($script:unflagged)"
# FAIL CLOSED INTO THE REJECTING ROLE. Only a measured
# unflagged=0 buys the accepting role; "could not tell" is not
# "fixed", and the rejecting role's pass is WINDOWS-SEEN, so a
# wrong guess here cannot manufacture a green re-enable.
$script:role = if ($script:unflagged -eq "0") { "accepting" } else { "rejecting" }
Say "role=$script:role"

$windowSec = 300
if ("$WindowSeconds".Trim()) {
  $parsed = 0
  if ([int]::TryParse("$WindowSeconds".Trim(), [ref]$parsed) -and $parsed -gt 0) { $windowSec = $parsed }
}
if ($script:role -eq "rejecting" -and $windowSec -gt 120) { $windowSec = 120 }
$stopOnFirst = ($script:role -eq "rejecting")
Say "windowSec=$windowSec sampleIntervalSec=1 stopAtFirstSighting=$stopOnFirst warmupCapSec=60"

# ---- NOTHING MAY BE RUNNING ALREADY --------------------------
# THE THREE-WAY READ, ONE IMPLEMENTATION: dot-sourced from
# tools/runner/process-query.ps1 rather than written again here.
. (Join-Path $PSScriptRoot "process-query.ps1")
$pre = Get-MatchingProcesses -Pattern 'pc-watcher\.py|supervise\.py|launch-supervisor\.py|telegram-bot\.py|executor\.py'
if (-not $pre.Ok) {
  Finish "NOT-MEASURED" "the-process-query-failed-so-nothing-could-prove-the-machine-was-idle"
}
Say "fleetBefore=$($pre.Processes.Count)"
if ($pre.Processes.Count -gt 0) {
  foreach ($p in $pre.Processes) {
    Say "  fleetBeforePid=$($p.ProcessId) cmd=$($p.CommandLine -replace ' ','~')"
  }
  Finish "NOT-MEASURED" "a-fleet-is-already-running-so-this-would-have-measured-someone-elses-start"
}
$startupDir = [Environment]::GetFolderPath('Startup')
$hook = Join-Path $startupDir "LEDGER studio machine.bat"
Say "startupHookBefore=$(if (Test-Path $hook) { 'present' } else { 'absent' })"
Say "# SIDE EFFECT, MEASURED NOT PREVENTED: tools/supervise.py rewrites or"
Say "# removes that Startup hook on every start of its own (install_autostart,"
Say "# B4). This proof does not change that policy; it reads it before and"
Say "# after so the change is visible rather than discovered later."

# ---- LAUNCH, FROM A PARENT WITH NO CONSOLE -------------------
$tempDir = if ($env:RUNNER_TEMP) { $env:RUNNER_TEMP } else { [System.IO.Path]::GetTempPath() }
$shim = Join-Path $tempDir "ledger-windowless-launch.py"
@'
import subprocess
import sys

# DETACHED_PROCESS, WHICH IS THE WHOLE POINT OF THIS FILE. Start-Process and
# .NET Process.Start both hand the child the console this CI step has, and a
# console-subsystem grandchild would then inherit it silently and open no
# window - the proof would print WINDOWLESS about a condition the scheduled
# task never has. DETACHED_PROCESS gives the child NO console, which is
# exactly the task's condition, and lets its own descendants allocate one if
# they are going to.
#
# DEVNULL RATHER THAN INHERITED HANDLES, and it cannot hide the fault: the 11
# sites that opened windows all used pipes already (capture_output=True), so
# redirection is not what allocates or suppresses a console. It is here so a
# detached child cannot hold this step's stdout pipe open and hang the job.
DETACHED = getattr(subprocess, "DETACHED_PROCESS", 0x00000008)
pythonw, launcher, repo, who = sys.argv[1:5]
proc = subprocess.Popen([pythonw, launcher, who], cwd=repo,
                        stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL, creationflags=DETACHED,
                        close_fds=True)
sys.stdout.write("%d\n" % proc.pid)
'@ | Set-Content $shim -Encoding utf8
if (-not $pythonc) {
  Finish "NOT-MEASURED" "no-console-python-to-run-the-detached-launcher-shim"
}
$launchedAt = Get-Date
$rootPid = (& $pythonc $shim $pythonw $launcher $repo "windowless-proof" 2>&1 | Select-Object -Last 1)
$rootPidInt = 0
if (-not [int]::TryParse("$rootPid".Trim(), [ref]$rootPidInt) -or $rootPidInt -le 0) {
  Finish "NOT-MEASURED" "the-detached-launch-printed-no-pid-($($rootPid -replace ' ','~'))"
}
Say "launchedPid=$rootPidInt launchedAt=$($launchedAt.ToUniversalTime().ToString('o'))"

# ---- THE SERIES ---------------------------------------------
$DAEMONS = @{
  'launch-supervisor\.py' = 'launch-supervisor'
  'supervise\.py'         = 'supervise'
  'pc-watcher\.py'        = 'pc-watcher'
  'telegram-bot\.py'      = 'telegram-bot'
  'executor\.py'          = 'executor'
}
$handlePids = @{}
$conhostPids = @{}
$transientPids = @{}
$daemonPids = @{}
$roster = @{}
$samplesTaken = 0
$fleetSamples = 0
$cleanSamples = 0
$handleSightings = 0
$conhostSightings = 0
$queryFailures = 0
$handleUnreadable = 0
$warmupSec = 0
$rosterFixed = $false
$windowStarted = $null
$firstSightingAtSec = -1
$lastFleetSec = 0
$nextLineAt = 0
$nextDetailAt = 0

function Sample-Tree($rootId) {
  $all = $null
  try { $all = @(Get-CimInstance Win32_Process -ErrorAction Stop) } catch { return $null }
  $byParent = @{}
  foreach ($p in $all) {
    $k = [string]$p.ParentProcessId
    if (-not $byParent.ContainsKey($k)) { $byParent[$k] = New-Object System.Collections.ArrayList }
    [void]$byParent[$k].Add($p)
  }
  $tree = New-Object System.Collections.ArrayList
  $queue = New-Object System.Collections.Queue
  $queue.Enqueue([string]$rootId)
  $seen = @{}
  $rootProc = $all | Where-Object { $_.ProcessId -eq $rootId } | Select-Object -First 1
  if ($rootProc) { [void]$tree.Add($rootProc); $seen["$rootId"] = $true }
  while ($queue.Count -gt 0) {
    $cur = $queue.Dequeue()
    if ($byParent.ContainsKey($cur)) {
      foreach ($c in $byParent[$cur]) {
        $cid = [string]$c.ProcessId
        if ($seen.ContainsKey($cid)) { continue }
        $seen[$cid] = $true
        [void]$tree.Add($c)
        $queue.Enqueue($cid)
      }
    }
  }
  return [pscustomobject]@{ All = $all; Tree = $tree; Seen = $seen }
}

$deadline = $launchedAt.AddSeconds(60 + $windowSec + 5)
while ((Get-Date) -lt $deadline) {
  $tick = Get-Date
  $elapsed = [int]($tick - $launchedAt).TotalSeconds
  $snap = Sample-Tree $rootPidInt
  if ($null -eq $snap) {
    $queryFailures++
    Start-Sleep -Seconds 1
    continue
  }
  $samplesTaken++
  $gp = @{}
  foreach ($g in (Get-Process -ErrorAction SilentlyContinue)) { $gp["$($g.Id)"] = $g }

  $daemonsNow = New-Object System.Collections.ArrayList
  $transientNow = 0
  foreach ($p in $snap.Tree) {
    $kind = "child:$($p.Name)"
    foreach ($pat in $DAEMONS.Keys) {
      if ($p.CommandLine -and $p.CommandLine -match $pat) { $kind = $DAEMONS[$pat]; break }
    }
    if ($kind -like 'child:*') {
      # CONSOLE HOSTS ARE NOT COUNTED HERE. Every conhost whose
      # parent is in the tree is itself in the tree (the walk takes
      # all descendants), so counting it as a transient child too
      # would inflate the one number that says whether this run
      # exercised the git path at all. It is counted once, under
      # conhostChildren, where it means something.
      if ($p.Name -ne 'conhost.exe' -and $p.Name -ne 'OpenConsole.exe') {
        $transientNow++
        $transientPids["$($p.ProcessId)"] = $kind
      }
    } else {
      [void]$daemonsNow.Add([pscustomobject]@{ Proc = $p; Kind = $kind })
      $daemonPids["$($p.ProcessId)"] = $kind
    }
  }
  $conhostNow = @($snap.All | Where-Object {
    ($_.Name -eq 'conhost.exe' -or $_.Name -eq 'OpenConsole.exe') -and
    $snap.Seen.ContainsKey([string]$_.ParentProcessId) })
  foreach ($c in $conhostNow) {
    $conhostSightings++
    $conhostPids["$($c.ProcessId)"] = "$($c.Name)/parent=$($c.ParentProcessId)"
  }
  $handlesNow = 0
  # THE TREE ALONE, because $conhostNow is a SUBSET of it: the walk
  # already took every descendant, so adding it again read every
  # console host twice in the sighting count. Proved on Linux with a
  # planted process table (a conhost under pc-watcher came back
  # inside the tree), which is the only half of this loop that can
  # be run off Windows.
  foreach ($p in $snap.Tree) {
    $g = $gp["$($p.ProcessId)"]
    if ($null -eq $g) { $handleUnreadable++; continue }
    if ($g.MainWindowHandle -ne 0) {
      $handlesNow++
      $handleSightings++
      $handlePids["$($p.ProcessId)"] = "$($p.Name)/handle=$($g.MainWindowHandle)"
    }
  }
  $dirty = ($handlesNow -gt 0 -or $conhostNow.Count -gt 0)
  if ($dirty -and $firstSightingAtSec -lt 0) { $firstSightingAtSec = $elapsed }
  if ($daemonsNow.Count -gt 0) {
    $fleetSamples++
    $lastFleetSec = $elapsed
    if (-not $dirty) { $cleanSamples++ }
  }

  # THE ROSTER IS FIXED ONCE THE FLEET IS UP, AND THE WINDOW STARTS
  # THERE. Measuring survival from the launch instant would make
  # survivedSec=300/300 unreachable for a daemon that takes three
  # seconds to appear, and a denominator nothing can reach is not a
  # gate, it is decoration.
  if (-not $rosterFixed -and ($daemonsNow.Count -ge 4 -or $elapsed -ge 60)) {
    $rosterFixed = $true
    $warmupSec = $elapsed
    $windowStarted = $tick
    foreach ($d in $daemonsNow) {
      $roster["$($d.Proc.ProcessId)"] = [pscustomobject]@{
        Kind = $d.Kind; Pid = $d.Proc.ProcessId; MissedAt = -1; LastSec = 0
      }
    }
    Say "rosterFixed warmupSec=$warmupSec processesWatched=$($roster.Count)"
    foreach ($k in $roster.Keys) {
      Say "  watch pid=$($roster[$k].Pid) kind=$($roster[$k].Kind)"
    }
  }
  if ($rosterFixed) {
    $wsec = [int]($tick - $windowStarted).TotalSeconds
    foreach ($k in $roster.Keys) {
      $entry = $roster[$k]
      if ($snap.Seen.ContainsKey("$($entry.Pid)")) {
        if ($entry.MissedAt -lt 0) { $entry.LastSec = [Math]::Min($wsec, $windowSec) }
      } elseif ($entry.MissedAt -lt 0) {
        $entry.MissedAt = $wsec
      }
    }
    if ($wsec -ge $nextLineAt) {
      $nextLineAt = $wsec + 5
      Say ("sample=$samplesTaken tSec=$elapsed windowSec=$wsec " +
           "daemons=$($daemonsNow.Count) children=$transientNow " +
           "handlesNonZeroNow=$handlesNow conhostNow=$($conhostNow.Count)")
    }
    if ($wsec -ge $nextDetailAt) {
      $nextDetailAt = $wsec + 30
      foreach ($d in $daemonsNow) {
        $g = $gp["$($d.Proc.ProcessId)"]
        $h = if ($null -eq $g) { "unreadable" } else { "$($g.MainWindowHandle)" }
        $ses = if ($null -eq $g) { "unreadable" } else { "$($g.SessionId)" }
        Say ("  proc sample=$samplesTaken pid=$($d.Proc.ProcessId) kind=$($d.Kind) " +
             "session=$ses handle=$h parent=$($d.Proc.ParentProcessId)")
      }
      foreach ($c in $conhostNow) {
        Say "  CONHOST sample=$samplesTaken pid=$($c.ProcessId) parent=$($c.ParentProcessId) name=$($c.Name)"
      }
    }
    if ($stopOnFirst -and $dirty) {
      Say "stoppedEarly=first-sighting-at-windowSec=$wsec"
      break
    }
    if ($wsec -ge $windowSec) { break }
  }
  Start-Sleep -Seconds 1
}

# ---- STOP WHAT THIS STEP STARTED -----------------------------
# THE INSTRUMENT PUTS THE MACHINE BACK. It started a fleet nobody
# asked to keep; leaving it up would also refuse the next proof run
# on the lock. The kill is verified by asking again, never assumed.
$stopRc = "not-run"
try {
  $null = & taskkill /F /T /PID $rootPidInt 2>&1
  $stopRc = "$LASTEXITCODE"
} catch { $stopRc = "threw" }
Start-Sleep -Seconds 3
$post = Get-MatchingProcesses -Pattern 'pc-watcher\.py|supervise\.py|launch-supervisor\.py|telegram-bot\.py|executor\.py'
$leftRunning = if ($post.Ok) { "$($post.Processes.Count)" } else { "unknown-query-failed" }
Say "stopExitCode=$stopRc fleetLeftRunning=$leftRunning"
$lockPath = Join-Path $repo "game-design\pc-jobs\supervisor.lock"
$lockHolder = "none"
if (Test-Path $lockPath) {
  $lockText = (Get-Content $lockPath -Raw) -replace '\s+', ' '
  $lockHolder = $lockText.Trim() -replace ' ', '~'
}
Say "lockAfter=$lockHolder"
Say "startupHookAfter=$(if (Test-Path $hook) { 'present' } else { 'absent' })"
$task1 = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
$info1 = $null
if ($task1) { $info1 = Get-ScheduledTaskInfo -TaskName $TaskName -ErrorAction SilentlyContinue }
$lastRun1 = if ($info1 -and $info1.LastRunTime) { $info1.LastRunTime.ToString("o") } else { "none" }
Say ("taskRegisteredAfter=$([bool]$task1) " +
     "taskEnabledAfter=$(if ($task1) { $task1.Settings.Enabled } else { 'no-task-registered' }) " +
     "taskStateAfter=$(if ($task1) { $task1.State } else { 'none' }) " +
     "taskLastRunAfter=$lastRun1")
Say "# taskLastRun unchanged before and after is the proof that this step"
Say "# did not start the task. Compare the two lines above."

# ---- WHAT THE WHOLE RUN SAW ----------------------------------
Say ""
$survivedFull = 0
$worst = -1
foreach ($k in $roster.Keys) {
  $e = $roster[$k]
  $sv = if ($e.MissedAt -ge 0) { $e.MissedAt } else { [Math]::Min($e.LastSec, $windowSec) }
  if ($sv -ge $windowSec) { $survivedFull++ }
  if ($worst -lt 0 -or $sv -lt $worst) { $worst = $sv }
  Say "proc kind=$($e.Kind) pid=$($e.Pid) survivedSec=$sv/$windowSec"
}
if ($roster.Count -eq 0) { $worst = 0 }
foreach ($k in $handlePids.Keys) { Say "windowSeen pid=$k what=$($handlePids[$k])" }
foreach ($k in $conhostPids.Keys) { Say "conhostSeen pid=$k what=$($conhostPids[$k])" }
Say ("transientChildrenSeen=$($transientPids.Count) daemonPidsSeen=$($daemonPids.Count) " +
     "handleSightings=$handleSightings conhostSightings=$conhostSightings " +
     "queryFailures=$queryFailures handleUnreadableReads=$handleUnreadable")
Say "# transientChildrenSeen is the denominator that decides whether this run"
Say "# exercised the failing path at all: 0 means no git child was caught"
Say "# between samples, and a WINDOWLESS verdict then rests on the daemons"
Say "# alone. The daemons ARE console-subsystem python.exe spawned by the"
Say "# same windowless parent, so an unflagged fleet still shows there."

$restarts = [Math]::Max(0, $daemonPids.Count - $roster.Count)
$verdict = "WINDOWLESS"
if ($handlePids.Count -gt 0 -or $conhostPids.Count -gt 0) {
  $verdict = "WINDOWS-SEEN"
} elseif ($roster.Count -eq 0 -or $worst -lt $windowSec) {
  $verdict = "DIED"
}
Say ""
Check-DoneLine ("windowless-proof: fixCommit=$script:fixCommit " +
     "noWindowSites=$script:noWindowSites unflagged=$script:unflagged " +
     "role=$script:role taskRegistered=$script:taskRegistered " +
     "taskEnabled=$script:taskEnabled windowSec=$windowSec " +
     "samplesTaken=$samplesTaken windowlessSamples=$cleanSamples/$fleetSamples " +
     "handlesNonZero=$($handlePids.Count) conhostChildren=$($conhostPids.Count) " +
     "transientChildrenSeen=$($transientPids.Count) " +
     "processesWatched=$survivedFull/$($roster.Count) " +
     "survivedSec=$worst/$windowSec restartsObserved=$restarts " +
     "firstSightingAtSec=$firstSightingAtSec verdict=$verdict")
