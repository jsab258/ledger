# LEDGER pre-mortem, 21 November 2026

December 2027: LEDGER is not a high-quality AAA game, or never shipped. Three independent passes found 74 ways that happened. 35 have no guard, 34 a partial one that would not catch it in time, 5 are guarded.

## The top 15 and their guards

1. **The looks were never won.** Clothes, hair, people, crowd and frame rate sit outside the gate; look work is paused with no restart date. Guard: one look on 1 Feb, too late. Cheapest: one small look job a week with a dated check. His (question 1).
2. **"Measured" mostly meant "decided".** 195 rows MEASURED, about 24 on real figures. Guard: partial (the split is reported; the gate counts all 195). Cheapest: the gate counts only real-figure rows. Advisor.
3. **The red-team gate never closes, or is bent.** 19, then 22 new gaps; two clean rounds needed. Guard: none. Cheapest: "material" defined now, at most four rounds, the rest to him as scope. Advisor.
4. **The giant prompt is written before the gate.** Its task fires Sun 29 Nov; red team 4 is 30 Nov at the earliest. Guard: partial (RULINGS forbids it; only the launch is checked). Cheapest: the task writes only once the gate is met. Advisor, now.
5. **The one-shot cannot fit its week.** 6 of 41 checks in about 7.5 hours on the giant prompt last time; about 45 Fable-builder hours in the one-shot's week. Guard: the two-day go or no-go. Cheapest: the throughput needed worked out before launch. Advisor.
6. **Measuring costs more than a week.** About 106 PC hours at about 1 weekly point an hour, beside the cloud runs. Guard: partial (cost per hour reported; nothing sets 106 hours against the week). Cheapest: a budget table per session before each order. Advisor.
7. **The rulers were never checked against anything real.** Both footage measurers are the same model; the method was never tried where the truth is known; the panel was never compared with him (its record is empty). Guard: none. Cheapest: measure our own recorded prototype for each number's error; the panel on every build he plays. Builder, lane.
8. **The story deadlocks the build.** The checked reader puts the story 6th to 7th of nine (perhaps from memory of the games), and his approval gates the one-shot. Guard: the 28 Nov deadline. His (question 2).
9. **Tests pass while the game is thin.** The builder wrote its own tests; checkers found staged scenes. Guard: hidden and staging checks, planned, not built. Cheapest: the idle lane builds them now, proven on the first one-shot's known thin spots.
10. **The reminder chains die silently.** Seven self-rescheduling chains (and seven one-off reminders) live in one session tied to his desktop. Guard: none. Cheapest: a daily cloud task that reports any chain with no next run. Advisor, now.
11. **Scheduled tasks carry stale facts.** Today's 09:30 report treats a stopped one-shot as the play note; Monday's recipe task reads a report never written; the lane waits on a dead one-shot to 21 Dec. Guard: none. Cheapest: fixed today, audited each Sunday. Advisor.
12. **The browser game did not port.** Car, camera and feel are browser code. Guard: rule pieces only. Cheapest: port the cab to Unreal under the same checks first. Builder.
13. **Live talk never worked.** 5.4 s to first sound, 7% invented details (autumn figures), canned in the prototype, no release cost figure. Guard: partial (a bake-off not running; a talk bench from 7 Dec). Cheapest: latency and cost per played hour as gate rows this week. Builder.
14. **The rulebooks disagree.** Three copies of CLAUDE.md differ (cloud sessions clone main's); RULINGS forbids a file CLAUDE.md requires; the lane's RULINGS has merge markers and a red check nobody watches; the handover leads with a withdrawn goal. Guard: a size check only. Cheapest: one CLAUDE.md everywhere; a check failing on conflict markers. Builder, lane.
15. **The watchdog watches the wrong rows.** Any row not starting "Lane row" counts as the builder's, so story and design rows hide a silent builder; its model rule stayed silent on a Fable row; its pace logic is last week's. Guard: none. Cheapest: a fixed session field on builder rows, tested with planted rows. Advisor, now.

## Three questions for him (scope)

1. Unreal looks while the browser game is proved: (a) fully paused; (b) one small look job a week, about 5% of the allowance (recommended); (c) resume in full.
2. If on 28 Nov the story is still below RDR2: (a) hold the one-shot; (b) build on the best version and judge it in play (recommended); (c) lower the bar.
3. Real players before Unreal: (a) only his verdict; (b) a friends' playtest of the browser evening once the loops reach it (recommended).

## How this was done (the method)

Gary Klein's pre-mortem (Klein, "Performing a Project Premortem", Harvard Business Review, September 2007; his own summary, "The Pre-Mortem Method", Psychology Today, January 2021: https://www.psychologytoday.com/ie/blog/seeing-what-others-dont/202101/the-pre-mortem-method ; both found 21 Nov 2026 by search). The steps: tell the team the project has already failed; each person writes every reason, alone; the reasons are pooled one at a time until none is left; the list is ranked and each reason gets a change to the plan. It rests on "prospective hindsight" (Mitchell, Russo and Pennington, 1989): people find more reasons when told the failure has happened than when asked what might go wrong.

Applied here: three passes wrote their lists alone from the same files (this session, and two fresh Opus helpers given only the files and the failure framing, never each other's lists or the advisor's view); the lists were merged into distinct ways, grouped by gap type, and each was given its guard today, the cheapest new guard and an owner. A fresh Opus helper then checked every guard claim against the files: 89 checked, 16 wrong or misdescribed (mostly guards that exist in part and had been marked none), all fixed once here. The limit: all three passes are the same model family, so a blind spot all Claude models share stays hidden (way 5 below is the same limit in the red teams).

What each pass found: this session 30 of the 74 ways (5 found by no other pass); helper A 52 (13 alone); helper B 54 (14 alone). Ways found by all three: 20.

## Gap types

- T1 The proxy taken for the thing: a status, a mapping or a passing test stands in for the real quality.
- T2 A judge never checked against anything real: an AI reader, panel, labeller or measuring method whose error nobody knows.
- T3 A gate that cannot close, or closes by being bent.
- T4 Capacity never worked out: hours, allowance or session size set against the plan.
- T5 Stale copies of a fact: a number, date or rule copied into a prompt or file and left behind when it changed.
- T6 Out of the proof: the hardest AAA work kept outside every gate and every date.
- T7 A single point of failure.
- T8 Parts that do not fit each other or canon.
- T9 What he sees: buried, stale, too long, or asking him what his rulings settle.
- T10 A monitor watching the wrong thing.
- T11 Nobody's job.

## The full table

Columns: the way it failed; type; found by (M this session, A and B the helpers); likelihood and harm (1 to 5); guard today and whether it would catch it in time; the cheapest guard and how we would know it works; owner (Adv the advisor, Bld the builder, Cld a cloud session, His his decision).

### The design and its proof

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 1 | Looks never won: clothes, hair, people, crowd paused with no restart date (Kiln 0 of 6, no hair passed) | T6 | MAB | 4/5 | Partial: look note and one look at the 1 Feb check (too late to change course) | One bounded look job a week with a dated check; works if a look frame improves on his page each fortnight | His (Q1) |
| 2 | Unreal looks, engine, performance and shipping are OUTSIDE the gate (57 rows) | T6 | MAB | 4/5 | None | An "Unreal reachability" list beside the gate, each row dated; works if every OUTSIDE row has a date and owner | Cld (design proof) |
| 3 | MEASURED counts decisions (195 measured, about 24 on real figures) | T1 | MAB | 5/5 | Partial: the split is reported (COVERAGE, DESIGN-COMPLETE, REPORT), but gate condition 1 counts all 195 as passing | The gate counts only real-figure rows; both counts on his page; works when the gate's own table shows the real-figure count | Adv (relaunch prompt) |
| 4 | Red teams never clean (19, 22 gaps), or the triage is loosened until they are | T3 | MAB | 4/5 | None | "Material" defined in writing before red team 3; at most four rounds, the residue to him as one scope list | Adv |
| 5 | Catch rate shows finding deleted text, not missing ideas; brief tuned between rounds; every red-teamer is a Claude model | T2 | MAB | 3/4 | Partial: new planted parts each round | Plant parts that were never in any file (taken from the reference mechanics list and withheld); works if the catch rate on these is reported separately | Cld |
| 6 | Giant prompt written Sun 29 Nov from an open design (gate 30 Nov to 1 Dec) | T3 | AB | 4/4 | Partial: RULINGS (20 Nov) forbids writing it before the gate, but the 29 Nov task writes it anyway; only the launch is checked | The task writes only after DESIGN-COMPLETE says met | Adv, now |
| 17 | "Higher bar wins" pushes GTA VI's numbers (driving share, scale) against canon's "not a driving game, one port" | T8 | B | 3/4 | Partial: canon outranks, no check applies it | Each "higher wins" number checked against canon's not-list before adoption | Cld |
| 18 | The map too small for chases (his own question) | T8 | AB | 4/4 | Guarded: the fit check runs now and advisor 286 measures car chases | (in hand) | Cld, Bld |
| 19 | The day's length (18 real minutes against 48 to 144) left open while routines are tuned | T8 | MAB | 3/3 | Partial: open decision C11, expected 23 to 28 Nov, not tied to red team 3 | C11 settled before red team 3 | Adv |
| 26 | The core design marked down by checked readers: a silent lead who types his lines | T8 | A | 4/4 | None | One prototype test of typed talk against suggested lines, judged by the checked reader and the panel | Cld (story, lane) |
| 36 | "All 242 themes on parts with a test" is a mapping; nobody checked the tests measure the themes | T1 | A | 3/3 | None | A fresh reviewer samples 20 theme-test pairs; works if under 2 of 20 fail | Cld |
| 69 | Waiting share stuck at about 42 to 47% over many rounds against "hands always busy" | T8 | B | 4/4 | Partial: gate row 1.6.5 exists (waiting under 10%), unmeasured until the teardown; no loop moved it | Close 1.6.5 in the teardown and hold the loops to it | Cld |
| 71 | The memory-and-gossip pillar conflicts with an older canon line; the question is still open | T8 | A | 3/3 | None | Put it in the next order's canon line | Adv |

### Measuring

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 12 | The "two measurers" are two runs of the same model reading the same kind of screenshot | T2 | MAB | 4/3 | None | The second reading by a blind helper on other moments, plus way 13 | Bld |
| 13 | The footage method never tried on footage whose true numbers are known | T2 | MA | 4/4 | None | Record our own prototype (truth in its code), measure it by the method, give every number an error bar | Bld, Cld |
| 14 | GTA VI at 30 frames a second carries twice the timing error, then wins as "the higher bar" | T2 | AB | 4/3 | Partial: the method notes the error | A higher number wins only if it is higher by more than its error | Bld |
| 15 | Activity shares from edited, action-picked uploads overstate how busy the games are | T2 | B | 4/4 | None | Shares only from long unedited play, the cut count recorded | Bld |
| 16 | GTA VI's column filled from first-week footage | T2 | A | 3/3 | None | Marked provisional; re-measured at the 19 Dec reception study | Cld |
| 20 | Sound levels "by ear" taken by sessions that cannot listen | T2 | B | 4/3 | None | Loudness read from the footage's audio, or the rows marked his | Bld |
| 58 | Mafia still listed in the teardown brief, driving method, order item 30, the lane's CLAUDE.md and the lane handover | T5 | A | 3/2 | Partial: order_ledger.py refuses new order items citing Mafia; method files are unchecked | A check that fails a method file naming Mafia as a reference | Bld |

### The story

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 21 | The 14-item ruler sat at its ceiling (80 of 80) | T1 | AB | 5/3 | Guarded: demoted to a floor check | (in hand) | Cld |
| 22 | The checked reader recognised every shipped game, so its fit may be memory | T2 | MAB | 4/4 | Partial: the report says so; nothing fixes it | Calibrate on less-known games with Steam story scores; works if the fit holds there | Cld |
| 23 | The players' story ranking rests on 18 to 43 story reviews a game and a weak tagging script | T2 | AB | 3/3 | Partial: a hand check | A larger hand-read sample for the top four games | Bld |
| 24 | His approval of the story gates the one-shot, but the story can only be proved in play: deadlock | T3 | MAB | 4/5 | Partial: the 28 Nov deadline | His answer to Q2 | His |
| 25 | The story loop relaunches on Fable whenever it is below the best, with no cap | T4 | A | 4/3 | Partial: the 28 Nov deadline in the reminder | A cap of rounds and Fable points in the 10:30 reminder | Adv, now |
| 27 | Story contradictions (proposed changes would have Ron drive in the best ending, against "he cannot drive") and three endings plus the hunted man against "two or three" | T8 | A | 3/2 | None | A consistency check of STORY-FINAL against RULINGS and itself | Cld |
| 28 | The story reaches him as a 25-minute read with nine changes, against his one-screen rule | T9 | AB | 4/3 | None | One screen, three decisions, the read linked | Adv |

### The build, the one-shot and the loops

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 7 | The one-shot cannot fit its week (6 of 41 in about 7.5 h on the giant prompt; about 45 Fable-builder hours in its week) | T4 | MAB | 4/5 | Partial: the two-day go or no-go | Required throughput worked out before launch; the no-go set from it | Adv |
| 8 | The giant prompt (170 KB now, more with the definitions and story) exceeds what one session holds | T4 | MB | 4/4 | None | A size cap with details by file; a fresh session asked 20 random rules from it must answer 18 | Adv, Cld |
| 9 | Hour estimates on file (prototype 270 to 500 h, driving, traffic) set against capacity once on the old plan (18 Nov), never against the new one | T4 | B | 4/5 | Partial: the re-forecast of 7 Dec, after the giant prompt | A capacity line in the giant prompt task: hours needed against hours a week | Adv |
| 29 | Tests pass while the game is thin: the builder writes its tests and rewrites its play stories; the staging check exists only on paper | T1 | MAB | 5/4 | Partial: hidden checks and a staging check planned (advisor 280), not built | The idle lane builds both now and proves them on one-shot 1's build, where checkers already found the thin spots | Cld (lane) |
| 31 | Tests read game values, not the screen (a turned head; a black camera in a wall passed) | T1 | MB | 4/3 | Partial: the driving study's flat-colour picture check reads the screen, but not on the game's page | Screen-based checks for the experience rules | Cld (lane) |
| 32 | Baselines re-taken on the build under test | T1 | B | 3/3 | None | Frozen baselines, changed only with a reviewer's line | Cld (lane) |
| 33 | Feel tuned in a headless browser running at a third of real speed | T2 | B | 3/3 | None | Timing confirmed in real time on the PC once per loop | Bld |
| 39 | The browser game did not port; the Unreal one-shot is unresearched | T6 | MAB | 4/5 | Partial: 12 port pieces with tests (rules only) | One verb (the cab) ported to Unreal under the same checks before the giant prompt | Bld |
| 43 | The lane wakes hourly to a dead one-shot rule until 21 Dec; loops locked behind checks 1 to 24 | T5 | MAB | 5/2 | None | Lane prompt rewritten to the new plan (it builds ways 29, 31, 32) | Adv, now |
| 68 | Several Fable builders at once (about 16 points in 20 minutes once) | T4 | B | 3/3 | Partial: the one-builder rule, but on one side of a merge conflict on the lane | Way 54's fix | Bld |

### Testing and the judges

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 34 | The AI panel never checked against him; its bar written three ways (7, 5 or "most" of 8); taken from humans with about 100 hours | T2 | MAB | 5/4 | Partial: PANEL-VS-JAFAR.md (panel_vs_him.py) exists; "No entries yet"; the bar is also written as 6 and 4 of 8 elsewhere | One bar in one file; the panel run on every build he plays, agreement recorded | Cld, Adv |
| 35 | The typed-talk set "98% agreement" is a second model, not people | T2 | A | 3/3 | None | Reported as AI-checked; a human sample at the first friends' play | Cld |
| 75 | No real players before release: the only real judge is him | T11 | M | 4/5 | Partial: RULINGS keeps a friends' build each phase from phase 4, in Unreal, undated under the new plan, nothing before Unreal | His answer to Q3 | His |

### Unreal, talk, sound and performance

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 37 | Live talk, the moat: 5.4 s to first sound, 7% invented details, canned in the prototype, no release cost plan | T6 | MAB | 4/5 | Partial: the bake-off (n16-6), open, not running; a monthly talk bench from 7 Dec; a spending stop per copy by ruling | Latency and cost per played hour as gate rows, measured this week | Bld |
| 38 | Voices from VCTK speakers without consent | T6 | B | 3/4 | Guarded: his ruling, risk his | (his) | His |
| 40 | Memory and frame budget cannot hold GTA VI's crowds | T6 | AB | 4/4 | Partial: the 60 fps ruling, no budget row | A budget row in the reachability list (way 2) | Bld |
| 41 | The 1 Feb scope check has nothing to judge (no pieces made) | T6 | A | 4/4 | None | Name now what data the check needs and who makes it | Adv |
| 42 | Marvelous lapses 26 Nov before the export (waits on his box, try 2 of 2) | T7 | AB | 3/4 | Partial: his box with the deadline | A reminder to him on 24 Nov through the advisor | Adv |
| 78 | Shipping (store page, rating, AI disclosure, legal) outside the gate with no dates | T6 | M | 3/4 | Partial: a rating note (G4), the drafted Steam AI disclosure, the privacy check | A dated shipping list in the reachability list | Cld |

### The allowance, time and money

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 10 | The measuring block (about 106 h at about 1 point an hour) costs more than a week | T4 | AB | 5/4 | Partial: the cost per hour is in every row (advisor 285) and the 95% stop halts work; nothing sets 106 h against the week | A budget table per session before each order | Adv |
| 11 | Another project on the account runs every 3 hours round the clock; the plans' hour budgets ignore it | T4 | MAB | 4/3 | Partial: the meter readings include it; the plans' hour budgets (45 Fable hours, 106 PC hours) do not | Plans budget from the meter's real weekly rise, not LEDGER's own estimates | Adv |
| 47 | A lapsed 75% stop copied into many places left sessions idle overnight | T5 | AB | 4/3 | Partial: week-shape.json is the source, prompts still copy numbers | Prompts read the stop from week-shape.json, never state it | Adv |
| 60 | Many sessions on one branch; allowance readings up to 90 minutes old | T4 | A | 4/3 | Partial: the lane's lock row | Every session reads the meter itself where it can, or says the reading's age | Adv |
| 73 | Everything rests on one subscription and on Fable being available | T7 | M | 2/5 | None | A one-page fallback: what runs on Opus only, and at what pace | Adv |

### The schedule

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 44 | Scheduled prompts carry stale facts (09:30 one-shot report today; recipe rewrite Mon 12:40 says "Saturday" and reads a report never written) | T5 | MAB | 5/3 | None | Fixed today; a prompt audit each Sunday before the order | Adv, now |
| 46 | Monday 12:40 to 13:30: recipe, audit file, calibration, relaunch, audit fire on each other's unfinished inputs | T5 | A | 3/2 | None | Stagger by dependency | Adv |
| 62 | Two plans: the release date stands on the old phase plan; the progress page shows its forecast until 7 Dec | T5 | MB | 4/4 | None | The forecast marked "old plan, not current" until re-forecast | Adv |

### Tools and his PC

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 45 | Seven self-rescheduling reminder chains (and seven one-offs) in one persistent session tied to his desktop; one missed firing ends a chain unseen | T7 | MAB | 4/4 | None | A daily cloud task listing the tasks and reporting any chain with no next run | Adv, now |
| 66 | One PC; 45 GB of lasting work outside the backup; C: at its floor | T7 | AB | 3/5 | Partial: retention floors; the backup gap waits on his hands (order item 26) | Keep it on his page until done | Adv |
| 67 | The cloud cannot reach Microsoft's sites; each fresh run rebuilds its tools | T7 | B | 3/3 | None | The browser build of the simulation done on the PC | Bld |
| 74 | The repository is public: the unreleased game and story readable by anyone | T7 | M | 3/3 | Partial: no keys or large files committed (guards) | His decision on making it private (accounts are his) | His |

### Records, rulings and handovers

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 52 | Three copies of CLAUDE.md differ (main, wip, lane); cloud sessions clone main and read the three-session version | T5 | MA | 4/3 | None | One CLAUDE.md on every branch; a check that fails on two copies | Bld |
| 53 | CLAUDE.md and RULINGS disagree (FOR-JAFAR, a third try; main's copy caps RULINGS at 2,500 words, RULINGS says 4,900) | T5 | MAB | 4/2 | Partial: the handover tells sessions to correct helpers | CLAUDE.md edited in a session he starts | Bld |
| 54 | RULINGS at its cap; the lane's copy carries merge markers in the models line | T5 | AB | 4/3 | Partial: the caps check runs on the lane too and is red now (RULINGS 5,014 of 4,900 words), but checks size only and its red goes unwatched | A check that fails on conflict markers, and someone owning the lane's red | Cld (lane) |
| 55 | The handover leads with a withdrawn goal (Kiln v1) and NOW's state line still counts it | T5 | AB | 5/3 | None: the history check forces rewrites by size, nothing checks the goal line (the 07:52 rewrite kept it) | Rewritten the day a ruling withdraws a goal | Bld |
| 56 | The lane handover describes a retired local lane ending 23 Nov | T5 | B | 4/3 | None | Rewritten with the lane prompt (way 43) | Cld (lane) |
| 57 | The risk register is from October and guards the old friends' build | T5 | MAB | 5/3 | None | This file replaces it; refreshed monthly with the re-forecast | Adv |
| 59 | Swiss time and UTC mixed in page reads | T5 | AB | 3/3 | None | All "at" fields in Swiss time | Bld |

### Reporting to him

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 61 | Every row opens with a dead goal ("v1: 0 of 6") | T9 | A | 5/2 | None | Row headline from the current order | Bld |
| 63 | Two owners of one progress page | T9 | B | 3/2 | Guarded: advisor 275's rule | (in hand) | Adv |
| 64 | Licence items on his page against "licences are never his question" | T9 | AB | 3/2 | None | His one paste of the licence rule (advisor 263's item), then the page check refuses licence items | Bld |
| 65 | His time is the bottleneck: hourly, 07:30, 18:30, 21:30 messages and phone alerts on top of story and page asks | T9 | B | 4/3 | None | Messages only when something he would act on changed; counted weekly | Adv |

### Monitors

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 48 | week-shape.json still the 16 Nov double week; the watchdog's logic too | T5 | AB | 4/2 | Partial: the Sunday order build sets it inactive | Watchdog line read from the file only | Adv |
| 49 | The watchdog (by its own prompt) counts any row not starting "Lane row" as the builder's life sign; its model rule raised nothing on a Fable story row at 22:47 | T10 | M | 4/3 | None | Builder rows carry a fixed session field the watchdog reads; tested with planted rows | Adv, now |
| 50 | The efficiency review tapers itself off before the expensive weeks | T10 | B | 3/2 | Guarded: by design, the Monday audit carries on | (in hand) | Adv |
| 51 | The daily model switch voids every calibration; rows show the configured model, not the one serving | T10 | AB | 3/3 | None | After any switch, the calibration sets rerun before a judge counts | Adv |

### Other

| # | Way it failed | Type | By | L/H | Guard today | Cheapest guard; proof it works | Owner |
|---|---|---|---|---|---|---|---|
| 72 | An unspecified flask in the newest bible and pubs in earlier ones, near the content rule; the canon check does not read the lane's story files | T11 | A | 2/2 | None | The canon check's scope widened to production/lane/story | Bld |

## Guards the advisor can set now

Ways 3, 4, 6, 7, 25, 43, 44, 45, 49 (prompt and task edits), then 10, 11, 28, 41, 47, 57, 62, 65 at the next order.

## Guards for the builder or a cloud session

Builder: 12 to 15, 20, 37, 39, 52, 53, 55, 59. Cloud: 2, 5, 22, 29, 31, 32, 36, 54 (the idle lane can take 29, 31, 32 and 54 at once).

## His to decide

Questions 1 to 3 above (scope), and way 74 (the repository's privacy, an account matter) when there is a quiet moment.
