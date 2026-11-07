# QA: a lean proposal (7 Nov 2026)

A proposal for Monday's order; nothing is decided. Web links were read 7 Nov through a digest tool; [the reading](QA-READING-2026-11-07.md) keeps their limits. Dollars are API-price equivalents, not a bill; costs are estimates. No source gives a money cost per game hour of screen-watching agents, so none is given.

## 1. A studio's practices, done here

| Practice | An agent's way here | Needs | Still his |
|---|---|---|---|
| Plans, cases | Route stages are the cases: each working or not, linked to its fault ([Warhorse's way](https://forum.kingdomcomerpg.com/t/warhorse-studios-weekly-torch/29593/36)) | verdict.json | Nothing |
| Playthroughs, regression | Already nightly: fixed script, then Claude's eyes on 12 pictures (their cost unmeasured) | Screen, real keys, game log | Leaving the PC alone |
| Exploratory | One [charter, one session](https://en.wikipedia.org/wiki/Session-based_testing). One front window, so one at a time. False alarms ([TITAN 30%](https://arxiv.org/html/2509.22170v1)) and misses ([best model 48.39%](https://arxiv.org/abs/2604.02648), abstract only) | play.py | A ruling, if a helper drives |
| Checklist, certification | Save and Continue walked. [Menu sweep](https://learn.microsoft.com/en-us/gaming/gdk/_content/gc/policies/xr/xr003), [five resolutions](https://learn.microsoft.com/gaming/gdk/docs/store/policies/console/console-topfailingtestcases): not done, no fault yet | Logs, keys | Security prompts |
| Bug reports | FINDINGS stays the one home; the tester's 5-to-1 scale; [steps, evidence](https://gamedeveloper.com/design/how-to-report-bugs) | Pictures, logs | Nothing |
| Triage, fix checks | The session reads the report; the stage is walked again. Helpers in parallel only read. No primary source | Files | Scope, third tries |
| Focus, feel | The eyes name stiff poses; feel is not measured. No source reached | Films | His hands, friends' |
| Staffing | Few. [One blogger](https://gamedeveloper.com/programming/how-much-people-time-and-money-should-qa-take-part1): about 10% of budget; testers idle when they outnumber fixers | Time log | His meter |

## 2. The lean proposal: six real faults

**Office and sitting only in a test launch** (DECISIONS 7 Nov 12:48).
- Check: a switch beyond an allowed list in a gate's command.txt marks it "test launch", not "passed packaged".
- Cost: seconds, no tokens. Reuses: command.txt.
- Saved: the office's pass of 4 Nov, undone on 7 Nov.
- Caught? Yes, where command.txt is written. Whether his own launch carried the flag was not found (Exit A).

**Firewall box** (DECISIONS 7 Nov 15:10).
- Check: the front window's program read at the session's end.
- Cost: seconds, no tokens. Reuses: play.py's NOT-IN-FRONT line.
- Saved: some warning at most.
- Caught? No better than now: the tester named it, and only he may answer it. Prevention is a habit (no packaged copy from a new folder).

**Speaker in the base layer** (FINDINGS 24; Exit B).
- Check: one report line counting the game's "is undressed" log lines.
- Cost: none. Reuses: LedgerGarments.h's line. Saved: little.
- Caught? Never missed: the eyes named it in at least 12 night reports from 23 Oct, and his 8 Oct ruling kept it through phase 1, reported failed. No check dresses anyone.

**Card memory at its peak** (FINDINGS 13; Exit D).
- Check: the report compares the perf step's gpuMemMB and runs.jsonl's peaks with 6,000.
- Cost: none. Reuses: both records.
- Saved: the rehearsal's surprise: peaks of 6,161 to 8,481 MB (Windows' counter) in all 32 captures.
- Caught? The peak yes, only after a capture, not nightly; the perf step stands still and speaks Nano, not Pocket. The morning summary had flagged the 6,089.

**Tom treading on the spot** (FINDINGS 25).
- Check: a flag when a walk's legs run out before arriving (verdict.json's path); then one small review of a film there.
- Cost: flag none; review US$0.59 to 1.66 (gate reviewer, measured, UNIT-COSTS), only when it fires.
- Saved: a fault on the 5 Nov film, unrecorded until 7 Nov.
- Caught? Partly: a path shows he stopped, not that his legs strode; the reviewer finds that. On 7 Nov's night path the flag fires: 14 legs towards (7.9, 4.6), never arriving, that stage passed; cause unread, false alarms unknown.

**The quay's end wall** ([diagnosis](F:/LedgerTools/gate/new/quay-end-stop-2026-11-07/diagnosis.md): about 95% sure, code read, no human walk; mend unjudged, FINDINGS 28).
- Check: the same flag, plus a startup log line per spot in hook-cast.json from the game's StandBlockedAt and WalkLineClear (not tried).
- Cost: flag none; the line about 0.5 h once, US$11 to 19 at the stand-in US$22 to 38 an hour (UNIT-COSTS, inferred).
- Saved: part of the tester's three tries (FINDINGS 30).
- Caught? The flag probably, naming the place, not the wall; the line yes, for listed spots. Neither finds walls off the route ([Division's bots'](https://www.gamedeveloper.com/design/the-secret-ai-testers-inside-tom-clancy-s-the-division) limit too).

## 3. The rules

- Tools and records reused first; nothing new while a line in an existing report will do.
- A check is added only after a real fault slipped past, dropped when it has caught nothing for a month; its report line says whether it fired.
- Testing's records count in the process share, under about 15% (this brief's figure; no home found). The audit has no testing row, so the time log needs a tag.
- Helpers never send clicks or keys (CLAUDE.md); part 2 needs no change. An agent steering free play as a helper or on a schedule would: his decision, spending capped first.

## 4. The first step

Four read-only lines in the night report (nightly_walk.py): launch switches, legs that never arrived, undressed count, memory against 6,000. No model, no game.

About 1 h of session, US$22 to 38, plus one small reviewer, US$0.59 to 1.66 (estimates). Method: Warhorse's objective marks; Mafia's QA unreached.

Done when, fed 7 Nov's verdict.json, it names the 14 legs, and the next night's report carries all four lines.

## Unverified, unreached

The reading's section E: focus and feel, test-plan and regression primaries, Mafia. Its search-listing points stay unverified. Warhorse's digest is undated; TITAN's counts are inconsistent. Not read here: the 5 Nov path, the night walk's end time, his launch line.
