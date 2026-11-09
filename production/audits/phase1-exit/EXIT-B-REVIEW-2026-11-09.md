# Phase 1's exit re-checked, Exit B (one complete Tom and one speaker, walking, sitting and turning): fresh final review, 9 November 2026

A fresh reviewer (Opus), read-only. Read: CLOSE-BRIEF-2026-11-09.md (Exit B), CLOSE-BRIEF-2026-10-22.md, CLOSE-2026-10-22.md and CLOSE-B-REVIEW-2026-10-22.md. Not read: the REHEARSAL files and EXIT-A-REVIEW.

The build judged is 5ed8f38, built 8 Nov (build-commit.txt). The brief's line 15 names wip 3644608 for the 9 Nov walk; the logs name no build.

What was looked at:
- all 278 step pictures of the walks 2026-11-09-0131 and -0138, as contact sheets;
- full-size crops of 0138 steps 028, 030, 037, 066, 070, 126 and 148;
- side-walk-2026-11-08 frames 184 to 700;
- two logs: LedgerProbe-backup-2026.11.09-00.36.35.log (log 1) and LedgerProbe.log (log 2).

## The old faults

- **Tom the stand-in: gone.** Log 2: "Tom's parts: Body=SKM_MH_TomL1_BodyMesh ..." and "Tom wears 3 garment(s) over his MetaHuman".
- **Tom's walk sliding: gone by eye.**
  - In side-walk frames 184 to 186, 488 and 546 his planted shoes hold still.
  - His street walking reads as ordinary: 0138 steps 099 to 108, 0131 steps 038 to 059.
  - Caveat: that film was a test launch on build 3b3454e. The 9 Nov walk logs no foot measure for Tom.
- **Nobody sits in the game as played: gone for Tom.**
  - Log 2: "stage=sit ok=1 seated 19 cm from the seat"; "stage=stand ok=1 touched the room 0 times".
  - 0138 step-030 shows him seated, with the office on by default.
- **Proofs only in the editor; the tester blind: gone.**
- **Speaker turning not shown packaged: gone.**
  - Log 2: "ledgerTurn=PASS who=rocco yawWant=-124.2 yawWent=-123.3" and "ledgerTurn=PASS who=sam -115.6/-114.6".
  - 0138 steps 152 to 153 show Darren turning to Tom.
- **Speaker walk sliding: NOT gone.** The packaged log measures it on every walk:
  - Darren (sam): worst 35.1 cm (log 1), then 32.5 and 45.4 cm (log 2); his steady strides slide 10.6 to 17.3 cm each.
  - Ron (rocco): worst 15.2, 18.5 and 13.9 cm (log 2).
  - Two of these lines are marked as possibly the measure's drift ("NOT DRAWN while down").
  - There is no film of a speaker walking.
- **A speaker sits in the game: NOT shown.**
  - Ron is placed seated: "Body now loops A_bench_idle_MH" (log 2, line 1989; 0138 steps 026 to 045). He never sits down.
  - His sit-down failed packaged on 8 Nov ("never-seated", speaker-sit-2026-11-08/sit.log).
- **Clothes on their floor: NOT gone for the speakers.**
  - Log 2: "Rocco/Lena/Sam is undressed (the base layer shows)". Ron's and Darren's jeans and jumpers, Darren's boots and Sheila's glasses and chain are held.
  - 0138 step-126: Darren barefoot in white, Ron in white with boots.
- **No single speaker walks, sits and turns: narrowed, not closed.** Ron walks (sliding), turns (passes) and is shown seated, but never sits down.

## New faults (they block)

1. **Ron is held in the office for a game day and a half, then moved without walking.**
   - Log 2 has eight lines from D1 06:51 to D2 10:00: "rocco cannot walk from where they stand (8.42, 5.92) ... blocked at once, here by office_east wall".
   - Meanwhile he stays seated while the days pass (0138 steps 031 to 045, captions Tuesday and Wednesday).
   - Then "rocco stands off a thing ... at mickeys_rank ... at D2 10:12" (line 2645).
   - This arrived with the office on by default; it touches Exit A too.
2. **A "Talk to Ron" label shows with Ron out of sight** (0138 steps 064, 069 and 070). Small.

## Known shortfalls

- **Speaker walks slide 13.9 to 45.4 cm** (log lines above). Not narrow.
- **No speaker sits down** (sit.log of 8 Nov; the bench loop only). Not narrow.
- **The cast in the white base layer:** Darren barefoot, Sheila without her glasses (log "undressed" lines; 0138 step-126). Not narrow.
- **A hole at Tom's collar at the throat** whenever he faces the camera standing (0138 step-037, cropped). Not narrow.
- **Tom's face against the office's wall corner and blind** for about 30 steps (0138 steps 054 to 090; crop of 066). Already diagnosed (OFFICE-CAMERA-WALK-2026-11-09.md).
- **Ron's hair is dark at the sides** where his sheet asks for a short grey fringe (0138 step-148 crop; ron-kirby/SHEET.md line 12). Hair stands at the engine default and has not passed its gate. Narrow.
- **Ron's seated pose:** his hands hover off his lap (0138 step-028). Narrow.
- **Tom's left shoe stays flat, toe backward,** for about 0.25 s in the turn into the run (side-walk frames 683 to 690). Narrow and known.
- **Tom's boots read as low slip-ons** at knee height (side-walk strip). Narrow.
- **The walk-join check fails at 13.68 cm** (result.txt). Mostly the route and the reading.

Not reached:
- Tom L1's freeze approval file;
- a foot measure of Tom in the 9 Nov walk (none logged);
- any film of a speaker walking.

## Verdict

**NOT MET.**

Tom is complete and now walks, sits and stands, and turns in the packaged game. But no speaker is complete:
- none is dressed;
- their walks slide 13.9 to 45.4 cm by the game's own measure;
- none sits down in the game;
- Ron, the nearest, is held in the office for a game day and a half, then moved without walking.
