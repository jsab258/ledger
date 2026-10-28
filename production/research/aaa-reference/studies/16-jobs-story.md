# Study 16: Jobs and story (28 October 2026)

How Kingdom Come: Deliverance II (KCD2) and Mafia: The Old Country build, fail, guide and stage their jobs: from KCD2's quest graphs, level sequences and English text, Mafia's exported mission and cinematic files, Warhorse's public wiki and public pages read in full; no recordings. Our own words and numbers; Study 11's quest counts reused. Tags: **M** measured, **R** read, **I** inferred. Left unstudied under the content rule: one KCD2 side quest, two threads of a main quest, one Mafia step.

**The short answer.** KCD2 builds every job as a saved graph of states in data, wired to later jobs by named ports. Failure is rarely the end: a failed step gets its own journal entry, the world settles itself, and later quests can read "failed" as well as "done". It is not marker-free: 80% of objective starts point a marker, so its journal leaves "where" to the marker. Mafia is a straight line: 15 chapters, no choice kept, failure a restart, a quarter of it watched. LEDGER's lesson: KCD2's structure without its markers, so the words must carry "where".

## The numbers

| | KCD2 | Mafia |
|---|---|---|
| Jobs | 135 quests (Study 11): 32 main (untyped, I), 43 side, 45 micro, 15 activities | 15 chapters; 42 free-ride challenges (M; 2K says 24) |
| Size | files per quest median 72 (micro 26, side 106, main 196) (M) | 402 checkpoints, median 23 a chapter; 675 objective lines; 83 scripts (M) |
| Length in play | a main quest about 1.3 to 1.9 h (I: CENSUS's 40 to 60 h over 32) | a chapter about 40 to 60 min (I: CENSUS's 10 to 15 h over 15) |
| Branches | 199 objectives with two or more completed outcomes, in 78 quests (58%) (M) | none in data; route and kit picks in scripts (R, I) |
| Optional steps | 360 of 1,711 (21%) (M) | 3 of 675 (M) |
| Failure states | at least 698 cancelled-step entries, in 114 quests (84%) (M) | 5 fail reasons over 92 fail conditions (R, I); restarts (I) |
| Lateness | mostly patience on people, 2 to 6 world hours; a 10 s follow leash (R, three jobs) | 15 s out of bounds; companion 50 m and 10 s (R) |
| Guidance | a marker on 1,371 of 1,713 objective starts (80%) (M) | a marker with distance; can be switched off or shown on a key (R) |
| Journal | at least 4,464 step entries, median 22 words, p90 49; 84% use first-person words (M) | 74 beat entries and 15 chapter blurbs, median 35 words (M) |
| Cutscenes | about 164 story scenes in the levels, 304 min, median 97 s, longest 342 s (M; duplicates removed, I); 13 videos, 18.6 min (M) | 143 in-engine scenes, 185 min, median 62 s, longest 297 s (M) |
| Staging | median 16 camera cuts, median shot 6.3 s (M) | median 14 cuts, median shot 4.7 s (M) |
| Share watched | about 8 to 11% of the main story (I) | about 21 to 31% (I) |
| Memory | 1,202 out ports (468 yes/no, 734 triggers), 1,158 read elsewhere; permanent deaths in 76 quests (M) | no choice field in the save (R) |

## Structure

- **KCD2:** a quest is a node with in and out ports, sub-graphs and objectives, saved as XML (R; TALKS 3.1), with Study 11's states. Only states are saved; effects are rebuilt (R, wiki KM-A-30). The three jobs use no Lua (M). 74 quests keep their world steps in a part named for hibernation, awake only while the quest is active (M by name; R in two jobs). All 135 carry developer skip nodes, 2,364 in all (M; a debug shortcut, R, KM-A-55).
- **Mafia:** 15 missions in fixed order; each a list of checkpoints with objectives (eleven classes) and a five-reason fail map (R). Tables hold the order; Blueprint scripts stage it (M, R).

## Scale: three KCD2 jobs taken apart

| | Small: a stolen horse (micro) | Middle: a captured brother (side) | Large: scouting a fortress (main) |
|---|---|---|---|
| Files; objectives (optional) | 25; 5 (0) | 98; 11 (1) | 316; 27 (18) |
| Dialogues; spoken words | 4; 2,669 | 39; 6,280 | 158; 24,625 |
| Journal entries; words | 9; 309 | 36; 1,092 | 90; 2,650 (11 are findings) |
| Timers; branch steps | 2; 0 | 6; 1 (looters killed or let go) | 35; 5 (the report graded four ways) |
| Fail routes; failure entries | 1; 1 | 7; 12 | 9; 11 (no quest-level fail) |
| Out ports (yes/no); cutscenes | 0; a fader | 4; one of 113 s, 25 cuts | 19; 17, lengths not on disk |

(all M)

The small job fails only if its giver dies, and the horse is cleared away a day later. The middle one fails if the player leaves, loses, flees or the main story moves on; the enemy camp is then cleared off-screen. The large one cannot fail as a whole.

## Failure that continues

- **Late:** KCD2 mostly puts patience on people (2 and 6 world hours on the envoy), with one 5 h deadline on errands and a 10 s leash that fails the middle job (R). A guide lists two game-over timers (R, kcd2.org).
- **Caught:** crime nodes sit in 57 quests (M); in the large job a crime changes the next step (R). Patches 1.4 and 1.5 added fails for a crime or a killing (R).
- **Wrong man hurt:** 754 death watches in 119 quests; 76 make a death permanent (M). In two jobs a dead helper cancels only his steps, or fails the job if he gave it (R; as a rule, I).
- **Told, not hidden:** 36 quests have sub-graphs named for what follows a fail (M). An argument can end in banishment from the town (R, Shacknews, 17 Sep 2024); staying silent gets a group expelled, and the quest can still be finished (R, Destructoid, 19 Sep 2024).
- **Mafia** restarts the checkpoint, after 3 s or at once (R); no carry-on was found (I).

## No waypoints

- **KCD2 marks most steps** (80%, M); its journal names a way in only 3 of 12 and 11 of 44 entries in two jobs (I).
- **People guide first:** rumour-givers point at the giver; a leader on a leash; people who walk up to talk (84 nodes in 41 quests); guided tours (94 in 24); notes and quest items (310 in 72) (M).
- **The town gives directions:** 55 quests switch the townspeople's directions talk off during some steps (M), so it is on otherwise (I). Hardcore mode (patch 1.2.4, 15 Apr 2025) removes map position, compass and fast travel; the player asks the way (R, Deep Silver; VGC). Its effect on quest markers is unverified.
- **Mafia:** shown always, briefly, or on a key (R, settings text; CanIPlayThat, 29 Aug 2025); breadcrumb icons that move on as trigger volumes are passed (R fields, I meaning). Most direction is go-to (151 lines) and follow (64) (I).

## Cutscenes

- **KCD2:** of 194 sequences (328 min), 164 are story scenes once a master copy, a short duplicate, nine 10 s stubs and 19 town copies of punishment scenes are set aside: main 138 (258 min), side 26 (46 min) (M; the choice, I). With the videos, about 5.3 h (I); Warhorse's cinematic director's talk listing says five hours (R, Kino Art, 3 Oct 2025). A skip is implied, not confirmed (I, Gamereactor, 16 Dec 2025); story talk cuts the camera, lighter chat keeps it (R, Wccftech, 13 Sep 2024).
- **Mafia:** 33 of 141 triggers forbid skipping; the rest take an unexported default (R). Full performance capture, plus short body-only scenes (R, A Sound Effect, 19 Nov 2025).

## Memory

- **KCD2:** results leave a job as named ports, read in the region graphs over 2,258 wires (M); reputation goes to people in 34 quests, to factions in 30 (M). The large job's journal adds each finding as found, and the report is graded by them (R).
- **Mafia's save** keeps progress, loadout, money and collectibles, nothing chosen (R).

## For LEDGER

1. **Adopt: a job as a graph of saved states.** Study 11's four job and five step states; every change kept in the save data, effects rebuilt (SaveCodec does). Serves phase 3's "kept after restart", ROUTE.md section 3, D35.
2. **Adopt: failure that continues.** Every failure ends in a world state the town can talk about, never a game over; flags record "failed" as well as "done". The first ask already works so; make it every job's rule. Serves the outline's "no single beat can fail the run", D35, D58, RULINGS 12 Oct. **Ignore** Mafia's restart.
3. **Adapt: patience on people, not deadlines.** A window on the town's clock (KCD2 2 to 6 h; the ask's 22:00 to 01:00), then "stayed away"; a 10 s follow leash after which the leader waits, without KCD2's fail. Serves RULINGS 23 Sep (jobs).
4. **Adapt: the journal as the Ledger.** A line for every step state, failures included, and each finding; about 22 words, naming the person and the place by a landmark, which KCD2 leaves to its marker. Serves D12, phase 3's "useful office and ledger".
5. **Adapt: KCD2's guidance minus the marker.** The giver names place and landmark; anyone asked the way answers from authored facts (KCD2's directions talk); a leader may walk him; signs do the rest. Serves RULINGS 23 Sep, D20, D37, risk R6 (PLAYERS.md: players punish no direction).
6. **Adapt: sleeping steps and skip hooks.** Steps sleep while Tom is away and settle by the clock; each has a debug skip the AI tester can call. Serves RULINGS 3 Oct, phase 3.
7. **Adopt with numbers: few short cutscenes** (RULINGS 23 Sep). Proposed: each at most 60 s, skippable, a cut every 5 to 6 s; under 5% of the first hour watched (KCD2 a tenth, Mafia a quarter; Study 2's "well under 29%"). The producer decides.
8. **Ignore:** Mafia's fixed chapters and choiceless story (canon D24; the outline: beats fire on states); KCD2's markers (RULINGS 23 Sep) and faction numbers (D34).

**The job template (for the builder).**
- Job: id; giver (cast id); offered on a state, never the clock alone (the outline); state none, active, done or failed, with an outcome name (the ask's three).
- Each step: state (the five); the place, named with a landmark; who is there; a clock window and the person's patience; the act the town perceives (canon's seven slots); two or more outcomes where it decides; a Ledger line per state; two or more sources of direction (giver, a person asked, a sign, a note); a debug skip.
- Failure routes: late, caught, wrong man hurt, refused; each to a named outcome and a world state.
- Memory: flags the acts read; every state change kept in the save data; steps that sleep.
- Acceptance: every outcome reached in the Core's week like ROUTE.md section 4's rows; the AI tester reaches each from a fresh game with no marker.

**Targets for jobs without waypoints (proposed).** Every go-to step names its place by a landmark in the giver's line and the Ledger (KCD2's journal: about a quarter). Anyone who knows a destination says it when asked (RULINGS 25 Sep). The tester and P4's newcomers reach each place unaided within three minutes; misses are R6's evidence. No lateness fail inside a window of at least 2 h.

**Inputs for the three acts (proposed).**
- **Act I:** the ask, Ada's tea, Alison's question and Ellis's visit micro-sized (about 5 steps); the real book and the week's end side-sized (11 to 16). Act II reads their flags (ROUTE.md's table).
- **Act II:** each rival's attack a job whose failure continues; the sit-down one deciding step with three outcomes, like the large job's graded report.
- **Act III:** the inspection one step a morning, each with a day's window, graded by what the books hold. Scene candidates: the arrival and the books opening.

## Coverage map (rows to tick; REFERENCE.md's owner edits it)

Missions, jobs, story, and Cutscenes and staging: both games, 28 Oct (Study 16). Automated testing (KCD2's skip nodes, method only) and Interface (Mafia's marker settings): partly.

## Open blind spots

- **KCD2:** hardcore mode and quest markers; when the directions talk is on; the large job's 17 scene lengths; hibernation in code; job lengths in play.
- **Mafia:** objective instances sit in unexported level data (kinds, optional flags, timer seconds, stealth rules); the skip default; whether 30 video-flagged triggers play film.
- **Not reached:** TechRaptor, Deltia's Gaming, Escorenews, X, Fandom, Nexus, GameSpot, PCGamingWiki (refused; the first four on skipping, markers and an "almost six hours" figure); HowLongToBeat, Valnet sites, Polygon, Rock Paper Shotgun, Eurogamer (not tried, by their notices); any report of the 2025 Prague cinematics talk. Warhorse's KM-A-29 and 83 are empty.
- **LEDGER:** PLAN.md has phases 0 to 5, no phase 9; the acts come from game-design/story-outline-2026-09-28.md.

## Sources (read 28 October 2026)

- **KCD2's files:** quest graphs, English quest text, level sequences, the cinematics index, Study 2's video headers, Study 11's quest table. **Mafia's files:** Plotline, MissionSystem, Cinematics, settings text, save types, Study 2's lengths; the exports were removed from F: during the study (gone by 12:52), so its numbers rest on the derived tables in the session's raw notes.
- **Warhorse's wiki** (warhorse.youtrack.cloud): KM-A-30 (updated 30 Jul 2026), KM-A-55, KM-A-74 to 76.
- **Public, KCD2:** Deep Silver's hardcore article (https://www.deepsilver.com/games/kingdom-come-deliverance-ii/news/this-is-hardcore-adventuring-inside-a-brutal-new-bohemia) and patch notes 1.2.4 to 1.5 (.../news/patch-124, patch-13, patch-14, patch-15); VGC, 15 Apr 2025 (https://www.videogameschronicle.com/news/kingdom-come-deliverance-2s-gruelling-hardcore-mode-has-arrived/); Shacknews, 17 Sep 2024 (https://www.shacknews.com/article/141458/kingdom-come-deliverance-2-pax-west-2024-preview); Destructoid, 19 Sep 2024 (https://www.destructoid.com/hands-on-kingdom-come-deliverance-ii-is-a-game-where-every-choice-matters-even-when-you-stay-silent/); kcd2.org, updated 7 Sep 2026 (https://kcd2.org/en/post/kcd2-quests); Kino Art, 3 Oct 2025 (https://www.kinoart.cz/en/programme/absolute-cinema-cutscenes-in-kingdom-come-deliverance-2/2025/10/03/2000); Gamereactor, 16 Dec 2025 (https://www.gamereactor.eu/kingdom-come-deliverance-ii-cinematic-director-explains-how-to-make-cutscenes-unskippable-1649193/); Wccftech, 13 Sep 2024 (https://wccftech.com/kingdom-come-deliverance-2-qa-half-of-the-voiced-lines-arent-related-to-the-story-at-all/).
- **Public, Mafia:** 2K's patch notes, 7 Aug 2025 to Sep 2026 (https://mafia.2k.com/the-old-country/patch-notes/); CanIPlayThat, 29 Aug 2025 (https://caniplaythat.com/2025/08/29/mafia-the-old-country-accessibility-review/); A Sound Effect, 19 Nov 2025 (https://www.asoundeffect.com/mafia-the-old-country-game-audio/).
- **LEDGER:** canon.md, RULINGS.md, PLAN.md, the story outline, first-hour and first-ask designs, ROUTE.md, Studies 2 and 11, CENSUS.md, PLAYERS.md.

## Review

A fresh reviewer (Opus, 12:38 to 12:52) re-measured the KCD2 counts with its own scripts and checked the Mafia tables, the public pages and every LEDGER tie. Pass with fixes, all applied: ports split into flags and triggers; the jobs' journal counts; cutscenes de-duplicated (5.3 h, not 5.8); Warhorse's own figure; the preview claims split; skipping unconfirmed; lateness "mostly" on people; tags and floors. Cost, from the clock: 11:56 to about 13:00 (three helpers 12:01 to 12:30).
