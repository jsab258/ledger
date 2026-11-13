# Handover: where the production session stands

The one file a fresh session starts from. Rewritten, not appended, at each stop; capped at 1,800 words (tools/doc-caps.py, 8 Nov). Rules are CLAUDE.md's and RULINGS.md's; the items are NOW.md's and the order's; this file holds what is in flight, what failed and why, the next steps in order and the tries used. Older lessons: TRIED-ARCHIVE.md.

**Started:** 2026-11-13 14:51 (Jafar's typed session: the start gate, advisor 134, and HumanMotionCraft, advisors 132 and 135, his chat 13 Nov; the builder's run of 13:53 stopped at 14:50)
**Stopped:** 2026-11-13 14:50 (run from 13:53: Seamshift round 4, Loomwright round on his update, Kiln's design note settled and its judge built, HumanMotionCraft's headless half, his folders snapshotted; Drape Studio's final round running on the machine since 14:48; pace +9.7; rows 1410, 1449; verdicts read to 13:13Z, advisor to 14:47).
(The hourly task runs `python tools/fresh_gate.py` first; at each item's end `python tools/history_check.py`: OVER means rewrite this file, set Stopped, stop.)

**The goal:** his order of 9 November (production/orders/2026-11-09.md, adopted 8 Nov 17:17; runs to 13:00 Monday 16 November). **Until Monday 16 Nov 07:00 Kiln has priority over the order's game work, clothing first (advisor 144, his pick 14:36)**; game items run only where Kiln waits (Unreal or the card idle). The weekly line still governs total usage.

## Standing ways of working (carry across every rewrite)
- **The night (advisor 42 and 44, 9 Nov):** round the clock; during the night's build and walk only work touching Unreal and heavy local jobs pause; never stop for the night. Space checked before the night build by 23:30.
- The hourly start round the clock, nothing touching Unreal 01:15 to 04:30, stopping before 01:40.
- A short row to 'reports' at least once an hour while working, ending 'Allowance: N% at HH:MM, pace X; my spend US$Y since HH:MM' (get_usage Weekly all models; `python tools/pace_line.py <percent>`; `python tools/token_measures.py --spend HH:MM`). Write it with ArtifactData and see its version. "at" is +01:00.
- **Every time stamp from Get-Date at the moment of writing** (this run guessed 14:40 for records written at 14:26 and had to correct them).
- Pace rules: RULINGS 7, 10 Nov and 13 Nov (idle fine while on track; the 16 Nov reset week runs a doubled line from his adoption tap, six helpers, no busywork; rows in that week name any hour with no session, advisor 140/143).
- Never end a turn while work remains (advisors 64, 68); the Stopped line is the last thing written (advisor 104).
- **The lean start's page reads, filtered (advisor 97):** advisor-acks ordered by "at" desc, limit 1, then advisor where "at" after it (Swiss +01:00); verdicts where "at" after the last read, in UTC; open items by filter on items.json state "open" (the field is "state", not "status"). Never list collections whole.
- Advisor 113: of two tools, prefer the one driven without clicks. Advisor 117: every garment's work its own time-log window. Advisor 111: check the paid-tools sweep before any second try. Launcher ruling (RULINGS 11 Nov) as written.
- **Kiln (RULINGS 13 Nov 14:19, advisor 142):** serves LEDGER, never itself; every module and fix names the game item it unblocks and hours saved; 15% of a week's usage (suspended until Mon 07:00 by advisor 144); park rule: M3 by about 22 Nov or keep-or-drop. Time log "tool loop: <tool> round n". Caps: clothing about 20 h, hair about 8 h.
- **He no longer develops any of his tools (advisor 146, 14:45):** the copies under F:/LedgerTools/tool-dev are their only line of development; no more rebasing on his folders.

## Run on 13 Nov, from 13:53 (this session)
- Seamshift round 4 (advisor 137): counted faults fixed, numbers match its notes; Heavy sitting 328 to 10 through but still balloons by eye (the picture decides, not the count, advisor 143); pullover over blouse keeps bands; new coverage check fails Ron's jacket vent honestly; front shoulder still rippled; no regression. Report 'Round 4' in SEAMSHIFT-ROUND1; preview seamshift-round4.
- Loomwright on his update (136 step 0): only cloth changed (hair and street byte-identical). Cloth round 2: on its mannequin no tears, layers apart, binary FBX, skinning; on Tom's real body (glTF made from MH_TomL1_FullBody) shirt and jumper fine and skinned to his 341 bones, jacket lost 2 to 2.7 m below the floor. Report 'Round 2' in LOOMWRIGHT-CLOTH-ROUND1; preview loomwright-cloth-round2. Loomwright's cloth cluster is dropped (139).
- Page: his taps 14:12 (HumanMotionCraft yes; start gate A) closed. Gate A cannot be built: the gate cannot read the page; advisor 143 says no further change for now.
- HumanMotionCraft (132): v0.3.0 official release, checksum matched, F:/LedgerTools/humanmotioncraft; headless half by one helper: fully drivable (167 commands, a move in 2 to 3 s); sit and lean right, smoking draw wrong (hand covers face; 2 tries, left); its foot-slide figure contradicts the planted bones; no fixtures in the release. Report HUMANMOTIONCRAFT-ROUND1-2026-11-13.md.
- Kiln: design note TOOLCHAIN-CORE-DESIGN-2026-11-13.md, reviewed (pass with fixes, all applied; review beside it). Copies under git in F:/LedgerTools/tool-dev: kiln (from Seamshift), loomwright, drapestudio, motionsmith, all tagged his-final-2026-11-13; ClothCraft cloned (MIT, commit 16761c55) in vendor/. Judge kit F:/LedgerTools/tool-dev/judge (bars.json M1 to M4, run_round.py, HASHES.txt, git): `python run_round.py <round> C:/LedgerTools/cargo-target/kiln/release/seamshift.exe`; M1 met by the unchanged copy (runs/m1-baseline, timings aside). Builds: CARGO_TARGET_DIR=C:/LedgerTools/cargo-target/kiln (F: about 21 GB, floor 20). Loop notes: F:/LedgerTools/tool-dev/LOOP.md (round 1 brief draft inside).
- RULINGS: advisors 140, 142, 145 in; three old lines tightened; at its 4,900 cap exactly.
- Pushed to wip at 14:44 (failed=none); later commits (Kiln name, notebook) not yet pushed.

## In flight
- **Drape Studio's final round** (advisors 145, 146), detached on the machine since 14:48: F:/LedgerTools/drapestudio-test-2026-11-13-final/run_all.ps1 built his final source (C:/LedgerTools/cargo-target/drapestudio, 14:49) and runs job_run1 (jumper j3), job_jacket (cuff grip), job_jeans, job_import (FreeSewing SVG), job_layer (jacket over jumper; 68 min on 11 Nov) one after another; progress in run_all.log, a DONE file at the end. Nothing else heavy beside it until DONE (fair times).

## Next, in order
1. FIRST: pace; verdicts after 2026-11-13T13:13Z, advisor after 14:47 Swiss (latest ack 1447-146). Push wip after ci-checks (gate the push on failed=none).
2. Drape Studio's final round: when DONE exists, judge it exactly as DRAPESTUDIO-TEST-2026-11-11.md did (drape_check_any.py on each job's plan, bounds.py hang heights, its own checks, pictures; numbers beside Marvelous j3 / v19 / n7 and 11 Nov; the layer by eye), write DRAPESTUDIO-TEST-2026-11-13-FINAL.md (Method line starting with a file name), a preview, a row, push. Then Kiln's front end comes from tool-dev/drapestudio/python (interface only; never its engine or presets; its licence is his question before any garment made through it is adopted).
3. The ClothCraft brief: the docs connector failed four times; advisor asked (ack 143) to send its text through the channel. Put it in F:/LedgerTools/tool-dev/kiln/BRIEFS.md.
4. Kiln round 1 (one fresh fixer helper, Opus, brief from LOOP.md plus the design note, its review, bars.json, the ClothCraft brief): the serve command for job_j3 over ClothCraft's pattern mesher, VBD and OGC on the CPU; first measure CPU time against M2's 186 s. Then judge: run_round.py (M1), job_j3 through kiln/python/run_job_script.py, drape_check_any.py against bars M2, pictures to a fresh reviewer, a round section in a KILN report, a row. Alternate with the Loomwright hair loop (first cluster: cards outside the scalp with a camera coverage check; F:/LedgerTools/tool-dev/loomwright).
5. By Monday 07:00 (advisor 144): for his evaluation, milestones passed, numbers against Marvelous, hours spent, cost of the next milestones.
6. HumanMotionCraft: done and set aside by his typed session (15:25; report's 'Round 1, the Unreal half'; acks 132, 134, 135 written). Its retarget's open fault (standing knees 22-33 deg, feet up to 4.8 cm) has 0 tries; only if it is ever wanted. The start gate's pace hold now ends at most 30 min after a clean stop (his typed approval; DECISIONS 14:53). Advisor 147 (15:18, Kiln's sequence for RULINGS) is unread by you and unacknowledged.
7. Loomwright hair in Unreal: before any new picture, research how MetaHuman grooms draw strands or cards in a scene capture; prove a change of subject changes the picture first.
8. Motionsmith next (when a game need asks): a real solve that stands.
9. Sunday 15 Nov: own leftovers (grep first), after Saturday's walk. On his adoption tap: week-shape.json active true, the doubled line.
10. Nothing touching Unreal 01:15 to 04:30. Tonight's walk: no game piece changed today.
11. Leftovers of mine (keep while rounds continue): C:/LedgerTools/mocap-solve (about 1 GB); F:/LedgerTools/tool-tests-2026-11/* (motionsmith-r2 keep rise430s_Body.fbx, r3, loomwright-r2, loomwright-cloth-r2, seamshift-r3, seamshift-r4), F:/LedgerTools/drapestudio-test-2026-11-13 and -final, F:/LedgerTools/humanmotioncraft (release and test-r1), C:/LedgerTools/cargo-target (kiln, drapestudio).

## Tried and failed, and why (newest; older in TRIED-ARCHIVE.md)
- A count passed a bad shape (Seamshift's sitting hem) and a lost layer passed every picture (Loomwright's jacket): judge every count beside a picture and check every layer is present.
- A folder-date check that skipped subfolders missed his Loomwright update for three hours: date the source files.
- Vellum on Tom's jumper 3 of 3, set aside. Cascadeur test 4, 2 of 2, set aside.

## Kept as they are
- Uncommitted on purpose: the office prints (copies on F:/LedgerTools/game-inputs); untracked shop-room files are not this session's; stash@{0} kept.
- Waiting list for the next order: as in git show 55179b917:production/handover/HANDOVER.md ('Kept as they are'), plus about 25 Nov Cascadeur's trial end (uninstall or keep, one line with a recommendation), the talk bake-off with the router key.
- Tries used: as in git show 570374d9a:production/handover/HANDOVER.md ('Tries used'), plus HumanMotionCraft's smoking key 2 of 2 (left).; HumanMotionCraft's retarget pelvis 2 of 2 (fixed: source retarget pose raised, root-motion step off). Ours: F:/LedgerTools/bodies' Build Average, Heavy and Slim are one body (identical measurements); use a cast body for a second build.
- API spend: US$1.15 (8 Nov); none since.
**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run heavy jobs beside the Drape Studio round before DONE; run more helpers than RULINGS allows; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help; let a helper stop a process; work while another LEDGER session works; write a time without Get-Date; write judge/ from a fixer; write into his folders under C:/Game Dev Tools.
