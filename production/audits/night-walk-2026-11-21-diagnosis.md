# Night walk 21 Nov 2026: diagnosis (read-only)

There are two separate faults. The talk stages did not fail because of the sign-in. The walk judged Sheila close enough to talk to, 2.3 m away, but she stood behind the grey steel kiosk. The game only lets Tom talk to someone in plain sight, so pressing T opened nothing and the typed line reached the game as ordinary key presses. The bench and the picture check failed because the Claude Code command-line program that the night task runs had lost its own sign-in. The desktop app does not keep that copy fresh. The fix needs Jafar's hands (sessions may not log in).

## (a) Talk: a measuring fault in the walk
- No network and no claude -p under -TalkFake. The game treats the run as unattended (ue-probe/Source/LedgerProbe/Private/CrimeProbe.cpp:3540) and starts TalkHelper with --fake (:3605), which answers from KnowledgeFake (ledger/TalkHelper/Program.cs:1546, 1552). TalkHelper does not compile in the Claude Code client (TalkHelper.csproj:11). The log says "LedgerTalk: the stand-in" (LedgerProbe-backup-2026.11.21-01.02.02.log line 1439). The relaunch's greetings got stand-in words in 0.02-0.18 s (walk.log lines 16-18).
- Sheila: "in_sight=no blocker=...street_cl_kx100_kiosk_stainless", tom_to_face_m=2.31 (log line 1928). T counts only people in sight (CrimeProbe.cpp:10655-10671), so it said "Nobody near enough... nearest is Ron, 14 metres away" (line 1932). The typed letters landed as game keys (lines 1936-1953).
- The walk's reach test is distance only (tools/route_walk.py:611). route-where.txt gives every shown person a 3.5 m reach with no sight test (CrimeProbe.cpp:4411-4417). Before that, 14 legs slid along z 2.5 toward an old spot from D0 13:47 to 17:21 (state.json, stuck.fires).
- Not new: talk passed on 13, 14, 15 and 18 Nov and failed on 16, 17 and 19 Nov ("not on the street"). It depends on where her day puts her.

## (b) Who runs the night's claude -p
Task "LEDGER nightly walk" (schtasks, read only) runs daily at 01:30 as Jafar, "Interactive only": `cmd.exe /c ...python.exe tools\nightly_walk.py`. It runs claude -p for the pictures (tools/nightly_walk.py:333-337) and for the bench through ClaimBench (:276-282; ledger/DevTools/ClaudeCodeClient.cs:51, 146). Both use the npm program, version 2.1.310 (%APPDATA%\npm\claude.cmd). Its sign-in file, %USERPROFILE%\.claude\.credentials.json, was rewritten at 02:09:43, during the bench. Only its date was read. The file sits outside %LOCALAPPDATA%, so MSIX privacy is not the cause. Desktop sessions sign in through the app (CLAUDE_CODE_SDK_HAS_HOST_AUTH_REFRESH is set) and never refresh this file. tools/nightly_package.py makes no claude call (line 106 is git commit-tree).

## (c) What changed
Played builds: 5eb76d5 (wip 5856d0ac) on 20 Nov and f8c9f4f (wip 3fad784e) on 21 Nov, per build-commit.txt, LEDGER-STABLE-COPY.txt and task.log. In between, code changed only for the menu fix (LedgerPaper.cpp/.h) and play.py's pointer parking. Neither touches talk, route_walk.py, TalkHelper or sign-in. The sign-in worked at 01:56-01:59 on 20 Nov (bench 60 answered) and failed at 02:09 on 21 Nov. The same failure happened on 21-22 Oct and cleared on 23 Oct.

## (d) Smallest fixes
1. Sign-in, needs Jafar: in a Command Prompt, run `claude`, type `/login`, finish in the browser, then `/exit`. A session then confirms with one short claude -p run or the next night.
2. Talk, a session can do it in the tester: press T alone, wait for talk-open, and approach again before typing. Or the game adds a sight flag per person to route-where.txt.

Not checked: the sign-in file's contents and the server's reason (not opened, by rule); whether a sign-out elsewhere caused it; whether `claude setup-token` lasts longer (unverified).
