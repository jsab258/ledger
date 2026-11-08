# The lean QA proposal's first steps that need no Unreal, ready to build (8 November 2026)

For n02-9-qa-lean and n02-9-phase1-skills-playbook (order of 2 November, section 9). Sources:
- QA-LEAN-PROPOSAL-2026-11-07.md, as fixed on 8 Nov;
- production/research/PROPOSALS-REVIEW-2026-11-08.md.

Every file named here was read on 8 November 2026. Nothing was built or run.

**Reference.** Warhorse's per-objective marks, through the proposal's reading. Mafia's QA was not reached (proposal, "Unverified, unreached"). Each step reuses an existing tool, as the proposal's rule 1 asks.

**Costs.** Session hours are estimates (E). Dollars are at the stand-in US$22 to 38 a logged hour (I, UNIT-COSTS-2026-11-02.md). Small reviewers cost US$0.59 to 1.66 each (M, 30 Oct, UNIT-COSTS).

**Which steps qualify.** A step needs no Unreal when its code and its acceptance cases run on files already on disk.

Left out:
- **The quay's StandBlockedAt log line.** It needs C++ and a build.
- **The firewall-box line.** The proposal: no better than now.
- **The undressed-count line.** Dropped by the review.

Step 3b changes the build machine's perf step. It is prepared without Unreal, but its first reading needs the night's build.

**The proposal's rule.** A check is kept only while it catches something. So each line below says whether it fired, and the night's JSON keeps that, which gives the month's count to drop it on.

---

## Step 1. Legs that never arrived (first to build)

**Fault it would have caught.**
- Tom treading on the spot at Mickey's front: the 5 Nov packaged film, recorded only on 7 Nov (FINDINGS, "Tom and a speaker as played").
- The tester's rounds stopping at the quay's end wall (FINDINGS, "The quay end"; DECISIONS 7 Nov 21:45).

It catches them only partly. The path shows that he never arrived, not whether his legs strode. One small review of a film decides that.

**Check definition.**
- **Run.** A run is a maximal sequence of consecutive entries in verdict.json's "path" with the same "to". route_walk.py appends one entry per leg in go_to, line 282: {"to", "at", "clock"}.
- **When it fires:**
  - the run has at least 6 entries (the smallest leg cap in route_walk.py is 6, line 389; the default is 14);
  - its last entry's "at" is more than 0.5 m from "to" (the largest tol go_to is given is 0.5).
- **Why the length rule.** Runs toward a moving target ("follow") change "to" every leg, so they are length 1 and never fire.
- **Each fire is reported with:** the target, the leg count, the first and last clock, the distance left, and the last two "at" points.

**Where it goes.**
- **tools/route_walk.py:** a pure function stuck_runs(path). Route.write() adds verdict["stuck"].
- **tools/nightly_walk.py:**
  - summarise() carries it as "legs_never_arrived" with "fired": true or false;
  - paragraph() gains one sentence, for example: "Legs that never arrived: 1 (14 legs toward 7.9, 4.6, D0 09:50 to 12:05, 2.1 m short)."

**Acceptance cases.**
- **Real file (counted 8 Nov):** F:/LedgerTools/nightly/2026-11-07/route/verdict.json has exactly 14 consecutive entries toward (7.9, 4.6).
  - They run from D0 09:50 at (8.03, 1.16) to D0 12:05 at (8.39, 2.55), about 2.1 m short.
  - The legs bounce between x 8.4 and 8.5, z 2.5 and 3.4.
  - The next entry's "to" is (8.47, 3.29), and talk-open passed at 12:19.
  - The check must name this run. Its cause has not been read.
- **Every kept night.** Run read-only over all 23 night files, F:/LedgerTools/nightly/2026-10-04 to 2026-11-08. All 23 carry a "path". Read each fire by eye and record the false alarms. The threshold stays only if they are few.
  - This follows the lesson "check tool fixes on real files" (MEMORY; RECIPE 8 Nov, blind replay).
  - Whether the 5 Nov night fires at Mickey's front has not been read.
- **Self-test cases:**
  - arrival on leg 3: no fire;
  - 14 legs never within 0.5 m: fire;
  - a follow run with "to" changing each leg: no fire;
  - 5 legs not arriving: no fire;
  - the last entry within 0.4 m: no fire;
  - an empty or missing path: says "no path", not "none";
  - the paragraph shows the count and "fired".

**On a fire.** One small Sonnet reviewer (RULINGS 3 Nov: small piece, one round) looks at the walk's step pictures nearest the run. How to map the run's clock to step-NNN.jpg has not been read (unverified). Until that is read, use file times.

**Cost.**
- About 0.4 h E: function, wiring, self-tests, and the 23-night read.
- That is US$9 to 15 (I), plus US$0.59 to 1.66 per fire for the reviewer.
- No tokens at night.

---

## Step 2. The launch line in the night report

**Fault it would have caught.** Mickey's office and sitting "passed packaged" for days while they existed only behind test switches. The office pictures of 4 Nov carried -MickeysInside (DECISIONS 7 Nov 12:48; Exit A; n02-9-pass-is-players-launch).

**Check definition.**
- **Reuse.** tools/launch_line_check.py's judge(line) (8 Nov 08:34) classifies the line as PLAYER, PLAYER+WATCH or TEST.
- **Missing piece.** The night folder keeps no game log: F:/LedgerTools/nightly/2026-11-07 holds only route/verdict.json, walk.log, bench, bench.log and state.json. walk.log has no command line.
- **So the work is:**
  - route_walk.py's write() reads the "LogInit: Command Line:" line from <saved>/Logs/LedgerProbe.log (the file it already reads at lines 179 and 242) and stores it as verdict["launch"];
  - nightly_walk.py judges it and reports, for example: "The walk ran on: PLAYER+WATCH (talk is the stand-in)", or "a test launch: -X".
- **It reports and never fails.** The night walk is evidence, not a gate.

**Acceptance cases (real logs, read 8 Nov).**
- **Must read TEST** naming -mickeysinside: F:/LedgerTools/gate/new/office/2026-11-04-packaged-day/LedgerProbe.log, line 333.
  - That line is: "-LedgerSlice -LedgerCrime -Encounter=live -LiveFresh -TalkFake -NoTitle -windowed -ForceRes -nosplash -unattended -OfficeLook -MickeysInside -ResX=1920 -ResY=1080".
  - This is the exact fault.
- **Expected PLAYER+WATCH**, with the stand-in note: F:/LedgerTools/gate/new/office-sit-default-2026-11-07/walk-day/logs/LedgerProbe-backup-2026.11.07-14.45.48.log, line 333.
  - That is a route walk: -TalkHelper=, -TalkFake, -EncounterSave=, -RouteWalk and play.py's window switches.
  - Expected, not yet run.
- **launch_line_check.py --selftest** still passes, 11 cases plus 1.
- **Self-test cases:**
  - no log: "launch line not found";
  - a log with two "Command Line:" lines (a relaunch for Continue): the last one is judged;
  - the paragraph carries the verdict and the noted switches.

**Cost.** About 0.3 h E, so US$7 to 11 (I). No tokens.

---

## Step 3. Card memory at its peak, at High

**Fault it would have caught.** The memory figures were medians read as peaks:
- slice-perf.py line 76 and perf-hook.py line 113 both take statistics.median of GPUMem/LocalUsedMB;
- slice-perf.py drops the first 300 frames (line 26);
- the build machine's perf step runs with no scalability switch (ledger-probe-unreal.yml lines 2111 to 2113), at Highest, not the played High.

As a result the exit rehearsal found peaks of 6,161 to 8,481 MB (Windows' counter) in all 32 captures (QA proposal; REHEARSAL-2026-11-07-D line 15). The night report had called 5,810 to 6,089 the figure (MEMORY-PLAN-2026-11-07.md, line 7).

**Line, shared with the memory plan.** The memory plan and the QA proposal use the same measure and line:
- the highest GPUMem/LocalUsedMB in any frame after the load row;
- at High;
- against 5,650 MB, the table's total ceiling, under Windows' budget of 5,771 (MEMORY-PLAN section 4, line 50; the review's "Across the three").
- It reports, never fails. Three runs are taken only when a reading crosses the line.

**3a. The reader (no Unreal).**
- **slice-perf.py's line() adds:**
  - gpuMemPeakMB, the maximum over all frames, the 300 dropped ones included, since the launch peak sits there;
  - gpuMemPeakSettledMB, the maximum after the drop;
  - memLine=5650;
  - memVerdict, UNDER or OVER-LINE.
- The existing gpuMemMB keeps its name and is called the median in the text.
- **perf-hook.py** adds gpuMemPeakMB the same way, so runs.jsonl carries it.
- **"After the load row".** The plan uses these words without defining the row. This step reads it as "every frame row after the header and EVENTS rows". If the session means a later row, it says which (unverified).
- **Acceptance (real CSV, kept on F:):** F:/LedgerTools/tmp/p1-packaged/packaged-day-walk--3b3454e-sun.csv must read OVER-LINE.
  - Its median after the drop is already 5,842.5 MB (runs.jsonl line 368, picture 2, High), so its peak cannot be under 5,650.
  - Read beside runs.jsonl line 369's cardGameMBPeak, 8,716 (Windows' counter). The plan leaves its conflict with the game's figure open (MEMORY-PLAN section 4).
- **Self-test cases:**
  - a series rising to 6,100 in its first 300 frames then settling at 5,500: peak 6,100, settled peak 5,500, OVER-LINE;
  - all frames 5,000: UNDER;
  - no memory column: "absent";
  - the existing 8 slice-perf cases still pass.
- **Cost.** About 0.3 h E, so US$7 to 11 (I).

**3b. The night's step at High (prepared now, read after the next build).**
- **The change.** In ledger-probe-unreal.yml's perf step, change -ExecCmds to carry "scalability 2" as well as the capture. Whether one -ExecCmds with two comma-separated commands works on 5.8 is unverified. The first night shows it in sliceperf-run.log.
- **The file is on the workflow's watched paths** (lines 50 to 57). Pushed alone, it starts the build machine. So it goes with the night's package request (tools/nightly_package.py), never in a separate push.
- **Known gaps** (QA proposal): the step stands still, so it says nothing about walking, and it speaks Nano, not Pocket.
- **How the line reaches the report.** nightly_walk.py could read production/d1-probe/ue-perf-verdict.txt. How that file reaches this PC before the walk's report is not read: the build machine pushes, and the session pulls (unverified). If it is late, the memory line goes in the morning overview from the pushed file.
- **Done when:** the next night's line shows peak, settled peak and verdict at High.
- **Cost.** About 0.1 h E plus the night's build, which runs anyway.

---

## Step 4. A testing tag in the time log (optional; a record, no fault)

The proposal's rule 3: testing counts in the process share, under about 15%, and the audit has no testing row.
- **The change:** timelog.py's KINDS gains "testing", and token_audit.py maps it.
- **Fault it would have caught:** none. It measures the share, so by the proposal's own rule it is not a check.
- **Self-test:** a "testing" start and stop sums in week().
- **Cost.** About 0.1 h E, US$2 to 4 (I).

---

## Order, total, done

1. **Order:** Step 1, then 2, then 3a; 3b rides the next night's build; Step 4 if wanted.
2. **Total:** about 1.1 h E, US$24 to 42 (I), plus one small reviewer at US$0.59 to 1.66. The proposal said about 1 h.
3. **Done when:**
   - fed 7 Nov's verdict.json, the report names the 14 legs;
   - the office's 4 Nov log reads TEST;
   - the 3b3454e day walk reads OVER-LINE;
   - the next night's report carries all three lines, each saying whether it fired.

**Before any of it counts:** one fresh reviewer checks the steps against these files (CLAUDE.md, research method).

## Unverified, unreached

- Not yet known:
  - the false-alarm rate of Step 1 across the 23 nights;
  - the clock-to-picture mapping;
  - two commands in one -ExecCmds on 5.8;
  - how ue-perf-verdict.txt reaches the night report;
  - what "the load row" means;
  - the expected PLAYER+WATCH verdict on the 7 Nov route-walk log (not run).
- The 7 Nov path was read only to line 300 of its file, so other runs in that file have not been seen.
- Mafia's QA was not reached.
