# The cloud session's share in each order (proposal, 18 Nov 2026)

Waiting item 17 of the order of 16 Nov, for the order of 23 Nov and after. [M] counted from LANE-LOG.md and LANE-QUEUE.md; [est.] estimated.

## What the lane did this week

- 16 runs, 17 Nov 17:28 to 18 Nov 00:31, about 4.5 hours of run time summed over the runs (two runs at 20:17 overlapped), Opus 5.5 with helpers [M].
- 29 items done, each with an evidence file; all but the first (parked cars) had a fresh review, all PASS WITH FIXES but one FAIL on a single claim (the lamp pool, withdrawn). One item was rightly left to the main session as in hand [M].
- Every item left a "for the main session" line: about 67 actions, about 2 per item, and about 15 picks meant for his page [est.].
- Dollars: in the "Lane row" reports, not read here.

## What qualifies

Work that finishes in the cloud with its proof there: research, plans and costings for later PC work, reviews of plans and specs, code whose tests run in the cloud (including the prototype), Kiln code reading.

Never: Unreal, the card, builds, renders, drapes, Kiln or judge runs, Blender, Marvelous, any game, the tester, deletes, clicks or keys, publishing, work already in hand, work that needs him first.

## How the order names lane items

A section of its own, "Lane (cloud)", after the week's items:

- One line per item: code (`l23-1`), what it is, the item it feeds, cloud hours, acceptance check.
- The check, always: evidence file; one fresh review passed, fixes applied; cloud tests pass where there is code; no main-owned file edited; at most three "for the merge" lines, at most one for his page.
- Total about 12 cloud hours: 10% of a normal week's about 120 hours (205 / 1.7) [est.]. A cloud hour is one hour of a lane run, helpers included. This 10% is a production share; it is not CLAUDE.md's 10% for independent review, which stays as it is.
- At most one standing filler (proposed: the prototype's wave 1 checks), used only when the listed items are done.

## How the 10% is measured

The meter is shared, so the split is read by dollars.

- The record is dollars: the lane's from `lane_gate.py --spend` in its hourly "Lane row" (each run's last row adds its total and item codes), the main session's from `token_measures.py --spend` for the same days.
- Lane share = lane dollars / all dollars, applied to the meter points used; one line in Monday's overview: share against 10%, items done, intake hours.
- Hours are derived: each run's Started and Stopped lines become a start and stop row in the time log, kind "lane", under the item code. They cost items and feed the B12 forecast; they never decide the share.
- Over 12% by Thursday: no new lane items until Monday. Under 6% by Friday: the next order lists more.
- Intake time: time log, kind "intake", under the lane item's code.

## How the main session takes results in

From the log: one merge (about 10 min) plus about 2 actions per item at about 10 min each is 20 to 30 min per item [est.]. At 29 items, 10 to 15 main-session hours: as much as the lane's whole share. So:

- One merge a day, at an item end.
- Lane lines go to the next order's waiting list or the item they feed, never into the running week. Picks for him wait for Monday's batched taps.
- PC follow-ups count against the item they feed, not as intake.
- Target: intake under 25% of the lane's hours (about 3 h). Two weeks over: the next order halves the lane's items.

## When the queue runs dry (the rule)

The lane works the order's one standing filler if named, then stops: its gate says LANE WAIT until the next order. It never refills itself from the running list, the recipe map or advisor rows (this week's G4 and G1 came that way).

## Risks

1. Duplicated work: two TRAFFIC-COST files now differ. Each lane item names the one file it feeds; corrections go under "For the merge", never a second copy.
2. Results nobody merges: whether this week's work reached wip is unknown here. The overview counts unmerged lane items; a week unmerged, archived with one line.
3. Scope creep: about 15 page picks in one evening, against one phone screen of three decisions. Picks wait for Monday.
4. Prompts on his phone: a task made from a phone loses its permission setting; a helper published by mistake. The task is made at the PC; briefs forbid publishing; a prompt reaching him is a fault.
5. The prototype: 270 to 500 cloud hours at 12 a week is 22 to 40 weeks. Wave 1 only, then his play decides.

## Decisions for Jafar

1. Keep the lane after 23 Nov? RULINGS ends it then, and CLAUDE.md's "one session, never unattended lanes" text would change to allow it. A: yes, four weeks, then judged by its numbers (recommended). B: stop. C: open-ended.
2. Where its 10% comes from? A: the 70% production share, 60 main and 10 lane (recommended). B: your 20%. C: on top of the week.

Review applied: production/lane/reviews/REVIEW-K2-SHARE-SYSTEMS-2026-11-18.md
