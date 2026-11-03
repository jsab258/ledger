# Handover: where the production session stands

The one file a fresh session starts from (his rulings of 3 November: a fresh session every day, never two at once). Rewritten, not appended, at each stop. Rules are CLAUDE.md's and RULINGS.md's; the phase's items are NOW.md's; this file holds only what is in flight.

**Started:** 2026-10-29 10:27 (the session "LEDGER Builder", running since then)
**Stopped:** not yet
(Never two at once: the day's session sets Stopped from Get-Date as its last act; the next fresh session, started by the scheduled task "LEDGER: the day's fresh session" at 05:15 (about 05:21 with the app's jitter), begins only when Stopped is later than Started and no other session in the checkout has been active for 15 minutes, then sets Started.)

**As of:** Tuesday 3 November 2026, 21:15 (Swiss time).

**The goal:** his order of 2 November (production/orders/2026-11-02.md), item by item, until 13:00 Monday 9 November or until he says stop; the scheduled task's prompt carries it in full.

## First, in this order (Wednesday 4 November)

1. Restore the three material files the editor rebuilt last night before any pull: `git checkout -- ue-probe/Content/Ledger/M_LedgerSurface.uasset ue-probe/Content/Ledger/T_LedgerDefaultNormal.uasset ue-probe/Content/Ledger/T_LedgerDefaultRough.uasset` (kept so the 04:15 morning pictures showed the brick tones; the build machine commits its own copies), then `git pull --rebase` (no autostash of uassets; the office prints and FOR-JAFAR.md stay modified on purpose).
2. Read his page's answers (https://claude.ai/artifact/1VZHkCBAHdw8HBdNHrByL8, collection verdicts): one item open, fresh-session-mode-2026-11-03 (set the daily task's permission mode to Auto). If he chose "not now", this session's arrangement is his to restate; if the task still has no Auto mode, every run stops at its first write until he approves.
3. Read the night walk (production/playtest/nightly/2026-11-04.md; the packaged-walk skill, step 9): it is the first packaged look at tonight's pushed work below. Compare the played copy's build-commit with wip's last push (856c0f1d4 or later).
4. The day's summary by 07:00 and the overview by 07:30 in FOR-JAFAR.md (the his-page skill, steps 8 and 9). The overview's first lines: `python tools/token_audit.py --shares 2026-11-03` (his ruling: the history's, Opus's and reviewing's shares; 2 Nov was 45%, 98%, 22%). Yesterday's summary is already written ("Builder, Tuesday 3 November (evening)"): add the evening's later lines below (decisions 19:18 to the wall tone) and keep it under 200 words. Its commit is the notes-only one that runs the backup. Computer use yesterday: Marvelous closed 07:17 by File, Quit.
5. Then the order: speech run F (packaged, shipped talk, `-AskSet=C:/Users/Jafar/ledger-local/production/research/invented-claims/bench/firsts-held.txt -AskNear`, no -AskAfterDeed, cap 0.80, raw to F:/LedgerTools/latency/askreal-2026-11-04f; the speech-bench skill); the corner's midweek page (below); the AT-RISK list (production/audits/phase1-exit/AT-RISK-2026-11-02.md, updated last night) with the walk and run F, one fresh review, told to him today (Wednesday is its deadline); the faster-builds measurement.

## Pushed last night (wip, ci 92 of 92), each passed in the editor, packaged first in the 01:30 walk

- Corner step 12, the reaction at Rita's window (DECISIONS 19:18): each witness who files gets Reaction::Decide from its card's temperament (production/specs/hook-cast.json); Investigate walks toward the glass after the head turn and stops short of the player (the walk waits for him). The walk-off's foot log now names plants made off camera ("NOT DRAWN"): off camera the bones are not refreshed, so its 8 m "slide" was the measure's.
- The packaged game's missing brick scans (DECISIONS 19:41): staging had never carried ps5-corner.json or its scans, so since 4 October the played copy wore the drawn brick while every editor picture showed the scan. Both staged now; stage_game_data's selftest (now in ci-checks) fails when the C++ names a spec file the list leaves out. Every packaged street picture before 4 November shows the other brick.
- Corner step 6, its first part, the bricks' own tones (DECISIONS 20:31, RECIPE.md): tools/brick_ids.py maps each brick of the two scans (on F:/LedgerTools/game-inputs and, ignored, in the checkout), M_LedgerSurface's custom node (off by default), set on the 29 brick-scan rows from ps5-corner.json; four fresh reviewers, no new fault. Watch in packaged pictures: a faint copper sheen on a few lifted chimney bricks at 3x zoom (the reverse view's reviewer).

## In flight

- Corner step 6, its second part, the wall's tone over metres: M_LedgerSurface MacroAmount/MacroScale (make_base_material.py, 103 wires), VignetteShot.cpp sets it from ps5-corner.json's "macro" 0.08 and "macro_scale" 0.0025 on the brick rows (-NoWallMacro off). Editor pictures in F:/LedgerTools/tmp/brick-pages/{day,night}-macro against day-on2 and night-on; one fresh Sonnet reviewer, all views in one batch (his small-piece rule): F:/LedgerTools/gate/new/wall-macro/review.json: no new fault, natural, visible only on the near gable side by side; pushed last night with the rest (DECISIONS 21:14), packaged first in the 01:30 walk.
- The corner's midweek page (today): the played copy with the street's switches and `-PageShots=day` (then `night`), `-RenderOffScreen -ResX=2560 -ResY=1440`, cam_hook, cam_A, cam_B, cam_mickeys, cam_reverse to Saved/PageShots/<camera>-<day|night>.png; one fresh final reviewer per frame beside F:/LedgerTools/gate/last-good/corner (cam_hook-day, cam_hook-night, cam_reverse-day are last night's editor pictures); shortfalls first: the Hook sheet's near wall is Flemish bond with many burnt headers (about 8% of its pixels against our 0.8%) and our scans are not, the walls even top to bottom, the lamp-lit wall clipping to pure red at night (step 13), the white base layer; step 13's night reading and step 11's wall reading (production/art/corner/BASELINE-2026-11-02.md) as information; the gilt as a choice.
- The fresh-session test (scheduled task ledger-fresh-session-test-2026-11-03, session "LEDGER: the day's fresh session, test (once)"): started 20:46 on its own, Opus 5.5 at medium, then stopped at its first file write waiting for his approval (no Auto mode on the task). If he allowed it, its result is F:/LedgerTools/scratch/fresh-start-test-2026-11-03.txt (it also tries the project agents).
- The helpers: seven project agents in .claude/agents (extractor, research-reader, importer, small-reviewer on Sonnet; final-reviewer, research-synthesis on Opus; diagnoser on Opus at high). Use them by name (subagent_type); a fresh session loads them. Reviews sized to the piece (RULINGS 3 Nov).

## Kept as they are

- Uncommitted on purpose: the office prints (calendar, fares, licence, drivers_board) changed in the checkout; git refuses pictures outside previews, their lasting copies are on F:/LedgerTools/game-inputs, as are message_pad and clock_face.
- Waiting list added 3 Nov: n02-9-hair-skill, n02-9-hair-cards-vs-strands, n02-9-dispatcher-voice, n02-9-study-a-files. Worth adding at the next order: Flemish bond with burnt headers for the corner's brick (the Hook sheet's near wall; BRICK-2026-10-04.md's bond verdict).
- Tries used: the reaction walk's delay 1 (the fault was the measure's); Tom's crown 4 (his yeses), a known fault; Sheila's hip 1 of 2; Ron's moustache 1 of 2; speech 2 of 2; the office's damp stain outline would be a third try (his yes first).
- His page last read: 21:05 (nothing new; one item open, added 21:00).

**Do not:** start local Unreal 01:15 to 04:30; run two Unreal jobs at once; run more than two helpers at once; tail Saved/route-checks.jsonl; print or copy any key; click anything outside Marvelous; run a tool with --help to read its usage; work while another LEDGER session works.
