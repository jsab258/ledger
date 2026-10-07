# For Jafar

The overview first; then the day's summary, under 200 words. Earlier summaries are in git and in
production/archive/FOR-JAFAR-to-2026-10-04.md (and FOR-JAFAR-to-2026-09-24.md before that).

## Overview (Thursday 8 October, written Wednesday at 19:00 so a closed session cannot cost the 07:30 update; brought up to date in the morning)

<!-- morning pictures: written by tools/morning_pictures.py -->

**Morning, Wednesday 7 October. Phase 1, prove the bottlenecks. On: 1.1 Mickey's front office, frontage, three views: production/research/pre-production/3-PROOFS.md. Next: 1.2 Tom and a speaker: production/casting/CASTING.md.**

Filmed by the morning task at 05:20 (at 5bd17b52); it then ran past its 30 minutes and stopped, so the block was written late by hand.

| | Today, 07 Oct | Yesterday, 06 Oct |
|---|---|---|
| The hook camera by day | ![The hook camera by day, 2026-10-07](production/previews/morning-hook-day-2026-10-07.jpg) | ![The hook camera by day, 2026-10-06](production/previews/morning-hook-day-2026-10-06.jpg) |
| The reverse view | ![The reverse view, 2026-10-07](production/previews/morning-reverse-day-2026-10-07.jpg) | ![The reverse view, 2026-10-06](production/previews/morning-reverse-day-2026-10-06.jpg) |
| The street at night | ![The street at night, 2026-10-07](production/previews/morning-night-2026-10-07.jpg) | ![The street at night, 2026-10-06](production/previews/morning-night-2026-10-06.jpg) |

The Hook sheet, the bar they are held to: ![The Hook sheet](production/previews/hook-sheet-2026-10-05.jpg)

No decision asked: these are for watching the street change.

<!-- /morning pictures -->

Disk (10-07 19:00): C: 96.3 GB free, F: 39.7 GB free (the NoAI folders gone, as you approved).

**Phase 1: on 1.1 (Mickey's office and Rita's front); next its third fresh review.** The second failed yesterday at 15:15 (production/audits/phase1-exit/GATE-1.1-REVIEW-2.md). Fixed since: the glass (the capture was unlit and coarse: now lit by Lumen, sharp at the two camera windows, people left out, one window at a time so the card does not fill); Mickey's office dark until Tom has the key; the black block in the hook view (the houses past the bend had no sides, so a room box and a roof's underside showed: brick sides and gables now, in tonight's build). Still open from it: the cast in the face plugin's white base layer (clothes a failed capability for now, Needs you 3), the other shops' opaque windows, faint wear, the indoor camera. **1.2:** Tom's face blocked (Needs you 1); the speaker's clothes (Needs you 3). **1.3, speech:** failed, a blocked capability, your answer. **1.4, P1:** complete: 79 fps by day, at night and walking with the voice speaking, about 3 ms to spare; the card's peak while the windows are caught is being brought down.

**The night's eyes never saw a picture (your fault report, 16:00):** the nightly report looked for .png and the tester saves .jpg, so every morning from 4 to 7 October said there was nothing to look at. Fixed with a test that failed first; tonight's walk is looked at. **The tester's walk (7 October, 02:30): did not run.** Three game windows left open by the cut-off measurement held the played copy's files, so the 02:52 build was copied inside the old copy and the launcher your shortcut starts was gone: the walk had nothing to start. Your played copy was broken from 02:52 to 10:10, when it was put right by hand (last night's build, a32eeeb). The night jobs and the build's copy step now close any game window first, and the copy step no longer nests.

**Risks, Monday's review (production/research/pre-production/6-RISKS.md).**
- R3, the street missing the bar: up, 25. The audit finds the visual method unproved: five proof-view steps were set aside, and Mickey's room failed three reviews. Phase 1's binding stop answers it.
- R1, empty or unchecked talk: level, 25. The bench's 23 to 25 empty answers have not been re-run; in play, 0 of 8 were empty (P4).
- R2, slow replies: up, 25. Measured on the real path 7 October: first sound 4.6 s median, none within two seconds; a blocked capability by your answer.
- R10 and R7, the friends' evening: down, 9 and 10. It runs on your account with its $5 cap and no second account. The Shipping launch and the limits surviving a restart are proved in 0.6.
- R9, the way of working: level, 12. Orders now come weekly and there is one session, but that holds only if shown.

### Needs you

(Your lighting answer, 13:25: day and night now, four or five lighting states with transitions later; in RULINGS.md. Your voice page read back at 13:00: speech reported failed as a blocked core capability, no third attempt at the voice, the faster first sentence off; in RULINGS.md. Every other page's answers read back at 08:40: 145, none new. Your three answers of this morning are in RULINGS.md and gone from here: the voice's route, the NoAI folders, and the sitting clips, which were already in last month's Mixamo harvest with their travel.)

1. **Tom's face is blocked** (14:40): the one more try could not set his brows' colour, the cause the research found: the face plugin offers no colour settings to a script before, during or after a build. Recommended: one more day's research on the other route (the finished face's own brow settings, as his hair's are set), then a page with the result; or you pick the closest existing take for now. Research, or pick?
2. **The check study you asked for** (added 13:00; [the proposal](production/research/invented-claims/CHECK-FLOOR-PROPOSAL-2026-10-07.md)): one day and at most $1, three ways to clear the first sentence sooner, measured on the bench. The limit: with today's voice kept, even an instant check leaves the voice's own 1.6 to 4.4 s, so it cannot bring speech under two seconds in the game. Recommended: park it until a faster voice is on the table. Yes to run it now, or park?
3. **Plain clothes for the cast: a failed capability for now** (21:00). Both routes your rulings allow have failed: the outfit made in Blender failed three fresh reviews on shape ([the third](production/audits/clothing/RON-OUTFIT-REVIEW-3.md)); tonight's one try with two free ready-made pieces (MakeHuman's fisherman's jumper and wool trousers, CC0) failed its own measured checks, skin showing through the jumper among them. The cast stays in the white base layer. What is left needs you: a garment tool or bought clothes (your rulings say no), or a later look when the tools improve. Recommended: keep the base layer through phase 1 and report clothes as failed. Keep it, or open one of those?

### Road to worth playing (PLAN.md)

- **0. Recover control** (0.20W): done 6 October, passed by a fresh review with narrow points.
- **1. Prove the bottlenecks** (1.00W): Mickey's front office first, then a complete Tom and one speaker, the voice under two seconds, and P1 packaged. If a sample fails within its ceiling, I report the failed capability.
- **2. Quay Street from proved families** (2.00W): the brick, the facades, the wet street's seam and the hill return here.
- **3. Thirty minutes that hold** (0.75W): N3 ported, the weather proof, P4's gaps.
- **4. The friends' candidate** (0.50W): on your own account, $5 an evening.
- **5. The first town:** after the pilot.
- **Friends:** eight to twelve weeks, if phase 1 passes; low confidence.

## Builder, Wednesday 7 October

**Failed:** speech: 4.6 s median, 4.0 with a faster first sentence; a blocked capability, your answer. Item 1.1's second review: the glass worst, then the office lit, the cast's base layer, a black block, faint wear. Tom's face: blocked. Plain clothes: the made outfit failed its third review and the ready-made CC0 pieces their checks; failed for now (Needs you 3).

**Fixed:** the frame: 59 and 51 fps to 80 with the voice speaking, card peak 5.9 GB. The glass lit and reflecting the street. Mickey's office dark until the key; the black post and white strip. Since the review: the black block (houses without sides), the west shops' rooms, the roofs' seams, Sheila and Ron out of the office camera, Enter showing a line's end; in tonight's build. The glass still steps; the shopfront wear never showed; now the grime is in the paint itself. Your two faults done.

**Two-tries rule broken:** the glass, twice: past three tries before a measurement found the cause; tonight a third anti-aliasing try without fresh research. Kept: the wear stopped at two.

**Act on:** Tom's face: research the other route, or pick a take?

## Builder, Tuesday 6 October

**Done:** phase 0 passed its recheck. 1.1's review faults fixed and walked in the packaged game: reflections, a harbour at the street's end, the locked office lighting up as Tom enters, wear, ashtray, map. Walking carries real travel. Your build ruling is in.

**Failed:** 1.1's first review; P2, the voice; the walk-in three times (a door bar, an engine warning, a leftover picture in the doorway; fixed); last night's measurement and walk, lost when my session closed at 00:30 (I had ended my turn to wait for the night's jobs to wake me; the program closed while idle, nothing in Windows' logs says why).

**Two-tries rule broken twice:** Tom's face, ten passes before it was set aside; the sky's band, five tries in one evening before the photograph was measured.

**Your question, builds:** 8 yesterday, 17 to 36 minutes (median 31; 3.2 hours): 15 cooking and packaging, 6 a second cook kept only as a measurement (removed), 9 tests and pictures. While one runs the graphics card stays free: code, records, research, reviewers; editor work waits.

**Act on:** nothing; the voice's numbers come on one screen.

## Builder, Monday 5 October

**Done:** your plan adopted with its ten edits; phase 0's items 0.1 to 0.6; the history cleaned into the new repository (30.8 GB to 3.2 GB), with guards before every push here and on GitHub, nine workflows retired, the tests green on GitHub. Every page's answers read back: 144, none new.

**Failed, then fixed:** phase 0's fresh reviewer failed it on eleven old jobs waiting on GitHub to run on this PC (one installs a scheduled task); the reconnect now refuses while any wait. A retired job put a 16 MB picture on main: taken off. The finished game carried a jacket made in Marvelous Designer's evaluation-only trial: now never built in, and a check traces every file the package ships to its source (6,585 of 6,585).

**Evidence:** checks 62/62 here; the core tests green on GitHub; the Shipping package rebuilt twice; the friends' evening re-run across a restart from the real shortcut (6.7 cents of calls).

**C:** 57.2 GB free, **F:** 22.5 GB.

**For you:** cancel the eleven old jobs (or leave them to lapse about 13:20), then reconnect the build machine.

## Builder, Sunday 4 October

**No page today:** nothing passed the gate. [The proof view, one frame a step](https://claude.ai/artifact/CaQ73RAcLMk1zqvqaNYt3r).

**Done:** your six answers applied; P5 on your own account; the history plan written (Needs you 1). Mickey's office furnished behind its window; every shop's board lettered by us; poll-tax bills; the image model's 41 worded pictures retired (kept on F:); cornices, brackets, panelled doors; the cottage doors' "pale slab" fixed; the brand bible put right. The atlas kept off main, as you ordered.

**Failed:** the facades and Mickey's room, each after three fresh reviews (Needs you 3 and 4). Found: the street is lit by a sky 41% as bright as the one seen.

**Evidence:** checks 47/47; core tests 5,077; engine checks 693/693; both game targets built today; previews of every try in production/previews. Committed here, not pushed: none of it has passed its gate yet.

**C:** 72 GB free, **F:** 23 GB. Backup with this commit.

**For you:** your four answers are recorded; I act on them Monday, starting with the five set-aside steps judged again by your narrow-points rule.
