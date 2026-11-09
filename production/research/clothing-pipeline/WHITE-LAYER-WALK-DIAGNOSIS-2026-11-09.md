# Why Ron wore the white layer in the 9 November walk

Diagnosis, 9 November 2026. Read-only. Nothing was run in Unreal and no project file was changed.

## Was the measure wrong? Yes

The walk was meant to test the clothes' release (commit 0b2621d00, 8 Nov 15:50). It did not test it. The build machine did not make tonight's build, so the walk played the copy built at midday on 8 November (5ed8f38, 12:37). That was three hours before the release. The garment code and the rows on wip are correct. The game that was walked was older than them.

## What the walk shows

- Ron is in the white T-shirt and shorts but wears his boots. See 0138 step-106 (right edge), step-129 ("Talk to Ron" over him), step-150 (his line captioned "RON"), and 0131 step-093 (outside the window, boots on).
- Darren was seen, and he was not dressed. In 0138 step-152 and step-153 he is in the white layer with his line captioned "DARREN". The tester's "woman by the telephone box" (0138 step-106, and beside Ron at the bin in step-129) is very likely Darren. Short brown-blond hair, bare feet (his boots were held too), and he stands beside Ron as he does in 150 to 153. Medium confidence on that reading.
- Sheila is in the white layer with her handbag: 0131 step-093 behind the counter, and the far barefoot figure with the bag in 0138 step-001. This is expected.
- In 0131 step-037 the figure is Tom, not Ron.

## The cause, with evidence

1. **Tonight's build stopped at the disk check.** The nightly task log (F:/LedgerTools/nightly/task.log, lines 195-197) has `nightlyPackage=ASKED commit=03470931 built=5ed8f38 head=36446086` at 01:30:08, then `walk` at 01:31:38. On earlier nights the walk started 20 to 25 minutes after the request. The build machine's own log (C:/actions-runner-ledger/_diag/Worker_20261109-003014-utc.log, lines 5118-5135) shows a step failing with "exit code 3" at 00:30:28 UTC. That is the workflow's "Check free space on C and F" step (exit 3, .github/workflows/ledger-probe-unreal.yml). F:/LedgerTools/retention/space-checks.log, last line, 01:30:28: "the build machine's run stopped: ... F: 19.8 GB (needs 20.0) ... VERDICT STOP".
2. **The walk did not notice.** tools/nightly_walk.py lines 339-351 only wait while Runner.Worker.exe is running. The job ended within a minute, so the walk went ahead. Nothing checks that the played copy was replaced, and the night report's "The walk ran on" line names the launch mode, not the build.
3. **The played copy still holds the old rows.** F:/LedgerTools/played-game/Windows/LedgerProbe/Content/LedgerData/build-commit.txt reads 5ed8f38 (dated 8 Nov 12:44). Its staged garments.json (8 Nov 12:37) still has "hold" on RonJeans, RonJumper, DarrenJeans, DarrenJumper and DarrenBoots. The walk's command line has no -LedgerRepo (LedgerProbe.log line 333). So LedgerGarments.h lines 35-49 find only the staged copy, and lines 284-294 skip any row with "hold".
4. **The game's own log of the walk confirms it.** In LedgerProbe-backup-2026.11.09-00.36.35.log, lines 2154-2157 and 2217-2223, and again in LedgerProbe.log lines 1923-1926 and 1968-1974:
   `LedgerGarments: Rocco's RonJeans held back: 7 November: until a packaged walk and his page; worn with -WearHeld=RonJeans`
   `LedgerGarments: Rocco wears RonBoots`
   `LedgerGarments: Rocco is undressed (the base layer shows)`
   Darren ("Sam" in code) has the same three held-back lines for his jeans, jumper and boots. Ron is "Rocco" in the code (CrimeProbe.cpp line 1034).

These were ruled out:
- **The stage list.** garments.json is on it (tools/ue/stage_game_data.py line 39), and the copy has it.
- **The meshes.** They are in this copy. Its dress-test.log (8 Nov, the same copy, run with -WearHeld) shows Ron and Darren wearing jeans, jumper and boots.
- **The import.** RonJumper's assets are in C:/LedgerTools/mh-assemble, dated 8 Nov 12:32, before that build.
- **wip.** 36446086 contains the release, with five "released" rows and no "hold" on them.

## How sure

High (about 95%). The logs, file dates and pictures agree at every step. Not checked: what took F: from 20.3 GB (22:23) to 19.8 GB (01:30), and whether a build from 36446086 cooks and wears everything once it runs. Both rows were worn in that copy only with -WearHeld.

## Smallest fix (not applied)

1. Free about 1 GB or more on F: under the retention rules (F: shows about 19 GB free now). Then ask for one packaged build of current wip (tools/nightly_package.py) and walk it. No code or row change is needed for Ron or Darren to be dressed.
2. A guard so this cannot pass silently again. After the wait in tools/nightly_walk.py, compare the played copy's build-commit.txt with the head that was requested. If they differ, the report should say "walked an old copy (5ed8f38); tonight's build failed" instead of reading as a test of tonight's work.
