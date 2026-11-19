# The plain bridge between the prototype and the one town (step 3a)

Task 4s, run 2, 19 November 2026. Written and tested the same day. Nothing in the prototype's own source was changed: the swap is step 4, a later round through the publish gate. Not yet seen by a fresh reviewer.

## In five lines

1. The bridge is one small JavaScript file, wasm/one-sim-bridge.mjs (14 KB, 5 KB compressed), over the loader (wasm/one-sim.mjs). It holds no town rule.
2. The prototype hands it its clock every simulation step. The bridge turns the clock into the same calls, in the same order, that the packaged game makes to its town code.
3. It hands back what each new hour did (who found the damage, who went to the police, DS Ellis, an arrest, Ada's invitation, Ron's envelope), and on request where people are and who knows what.
4. The town travels in the prototype's save as one plain object. Loaded into a fresh copy of the simulation it plays on exactly as if it had never stopped (tested, 6 of 6 weeks, under Node and in a real page).
5. Money, debts, jobs, fares, fights and talk stay in the prototype's own code. So do its street, its walking, its light and lines of sight, its weather, its car and its screens.

## What the prototype calls each tick

One call, in clock.js simStep, right after the clock has moved (`G.t += dm`):

    for (const hour of town.tick(G.t, area)) onTownHour(hour);

- `G.t` is the prototype's own clock: game minutes since Monday 00:00, fractions and all.
- `area` is where he stands, as the cast file names areas (mickeys, ritas, quay and so on). The town uses it for one thing: who sees it when a constable takes him at ten. The game falls back to "mickeys" when it cannot tell, and so does the bridge.
- Most calls do nothing and return an empty list. Once a game minute the bridge lets the town's talk run up to that minute. Once a game hour it runs the hour's scheduled steps and returns that hour.

What happens inside, which is the packaged game's own order (CrimeProbe.cpp, ClockHours and the clock's tick, lines 7946 to 7961 and 9108 to 9113):

1. For each whole hour the clock has crossed since the last call, oldest first: the town's talk of the hour before, up to its last minute; then the hour's steps in the game's order (TownWeek RunHour: six o'clock's passing, the damage found, nine's reports and DS Ellis, ten's constable and Ada's invitation, eight in the evening's envelope, eleven's tea closed, the week's end closed, the talk).
2. Then the town's talk up to now.

The same is true when the prototype skips time (sleep, the cells): its own skip already calls simStep in steps, so the town's hours run on meanwhile. A jump of thirty days in one call also works: 720 hours come back, in 0.25 to 0.4 s.

Cost, measured: 15 to 21 thousandths of a second of work for a whole game day when ticked every game minute. At the prototype's clock a game day lasts 18 real minutes.

## What it reads back

Every hour, from `tick`. One object an hour, with the thirteen answers the game's hour gives, named:

| Name | What it is | What the prototype would do with it (step 4) |
|---|---|---|
| found | who came by and found the damage, and the minute | they now know of it |
| went | who went to the police this morning | their statement is with the police |
| ellis | why DS Ellis came, or nothing | she is on the street asking; today the prototype decides this by its own loudness rule |
| taken | how his arrest will end (Cautioned, Charged, BailedToReturn), or nothing | the arrest scene, then the cells |
| held, heldUntil | he is in the cells this hour, and the minute he is let out | the prototype skips its clock to that minute |
| invite | Ada asked him in for tea | her line |
| ron | Ron brought the envelope | Ron at the door |
| tea | the tea's state, in the rules' own word | |
| asks | the next night he will be asked, the nights answered and how, and why the asks ended if they did | |
| outfit | what the outfit's man holds about him | |
| stories | how many stories the town holds, everyone's counted | |
| ellisFirst, takenFirst | "never" or "day N, for ...", "no" or "day N, ..." | the end screen |

"Held" is the one thing the bridge remembers by itself. In the packaged game the town only says that he is held; the game keeps "until when" (CrimeProbe.cpp ConstableHour, lines 7710 to 7720). The bridge does the same, from each hour's own answer, and offers it as `town.held()`.

On request, at any time:

- `town.placeOf(id, minute)`: where the town's routine puts a person at that minute, as a place of the cast file (mickeys_rank, fish_front, adas_step, off). The routine changes on the hour. The prototype's own walking takes them there.
- `town.knows()`: the Ledger's facts as the town holds them. One entry for each person and each story: who, the story, whether they saw it or were told, how many tellings from the one who saw it, who that was, how well that first witness saw him (0 someone, 1 a silhouette, 2 a mark, 3 a face, 4 recognised), whether the story names him, how sure, and the words.
- `town.state()`: the week's pieces (the asks, the police file, the tea, the damage, the arrests, the week's end).

## What it tells the town when he does something

Each takes the prototype's clock at that moment. The clock must have been ticked to that minute first, so that an hour that has begun has had its steps before he acts in it. The bridge refuses an act out of turn and says why.

| Call | When |
|---|---|
| `town.deed({ minute, area, thing, said, witnesses, fact, words, certainty })` | He damages something. `witnesses` is who saw it and how well: `[{ id, rung }]`. Whoever is in the area and did not see it done finds it at once, and others as they come by. |
| `town.saw({ minute, who, rung, fact, area, words, certainty })` | Somebody saw him do something that is no damage. One call a witness. |
| `town.answerAsk(askDay, answer, minute)` | His answer to a night's ask: the envelope handed over, a no, no show. |
| `town.teaMinute(minute)` | A minute he spends at Ada's tea. |
| `town.weekAsk(minute)`, `town.weekGive(answer, minute)` | Sheila's question at the week's end, and his answer. |

Who saw him, and how well, is still the prototype's to work out: its own geometry (distance, light, line of sight) and, for now, its own way of turning that into "how well". The real rule for "how well" is in the town code and in the golden table, but has no call on the front door yet (see "Not done yet").

## How saves carry the town

    G.town = town.save();                                        // in saving.js serialize, with the other keys
    town = await openTown({ wasm, castJson, saved: G.town });    // in restore, before the people are rebuilt

- `save()` returns one plain object. Inside are the same texts the packaged game writes into its save folder (CrimeProbe.cpp SaveEncounterToDisk): the town's talk (the game's agents.json), each person's memory as text (memory-<id>.md), the week's pieces (town.json), and the few lines the game keeps beside them (the deed's story and time, who saw it, her first visit, his first arrest). Each is written and read by the town code's own save routines. The bridge adds its place in the week: the minute it has run to, and the next hour due.
- Size: the biggest save in the tested weeks is 16,826 characters. The prototype stores its save in pieces of 150,000.
- Checked before anything is loaded, each refused with its reason: not a saved town, a later version, another cast file, a piece missing, the week's pieces from a later version, the talk cut short.
- A prototype save from before the swap has no town in it. Step 4 must choose: such a save starts a fresh town at its clock (people remember nothing of the old week), or is not offered. Recommended: not offered, since the prototype's save version changes with the swap anyway.

## The people and the places

- Nine people are in both casts. The bridge takes either id for them: sheila is lena in the cast file, ron is rocco, darren is sam, alison is noor, walsh is emil; ada, june, rita and hal carry the same id on both sides. Six carry the same full name on both sides. June, Rita and Hal have a surname only in the prototype.
- The other 19 people of the prototype have no certain match, and 32 of the real cast's 41 have no prototype id. Which names stand is a canon question, not the bridge's (DIFFERENCES.md, section 1).
- DS Ellis and the constable are people who walk about in the prototype. In the real rules they are steps of the hour. The bridge reports the step (`ellis`, `taken`); the prototype may still show somebody walking.
- Places: the cast file has 30 places in 24 areas. A table from those to the prototype's spots and rooms is step 4's work. Some real places have no spot on the prototype's map yet (DIFFERENCES.md, section 2).

## Not done yet (for step 4, the swap)

1. How well a witness sees him. The real rule (Perception, Observation, Sighting) is in the town code, and the golden table's rows for it pass in the browser build (T1). It has no call on the front door yet. Step 4 needs one that takes what the prototype knows (distance, light, in view or not, the coat, in the cab) and gives the rung.
2. The words. The hour gives "Ada asked him in" as yes or no, not her line; the arrest's words and his rights are in the town code too. Add when a screen needs them.
3. What the street calls him, and how much each person likes or fears him. The prototype's own today (gossip.js, events.js). The town code has its own (Suspicion, Reaction, StreetVoice), not behind the door.
4. The two tables: places, and the area he stands in.
5. Golden rows for the bridge's by-the-minute order (next section), and for the details of each Ledger fact. Both are the C# side's to write, so the main session's.

## How it is tested

All inside `one-sim.sh all`, under Node and inside a real page in headless Chromium 157. Last full run 17:01 to 17:05 UTC: exit 0 in 228 s, "one-sim: everything passed".

| Check | What it shows | Result |
|---|---|---|
| T8 the bridge, talk by the hour | The six scripted weeks of the C# Core's table, driven by a clock in odd steps (7.3 game minutes) through the bridge, with the prototype's own id for Darren. Each hour against the C# Core's row. | 225 of 225 hours agree, field for field. The bridge's "held" agrees with the hour's answer at all 225. |
| T9 the bridge, talk by the minute | The same weeks the packaged game's way, with the clock ticked every game minute, every 0.37 and every 7.3 (13,146, 35,736 and 2,060 ticks) | The same town to the last character in all three. |
| T10 a save in the middle | Each week saved after two fifths of its hours, at a minute inside an hour, written out as text, loaded into a fresh module, played on | 6 of 6 end exactly as the week played straight through. Held in the cells at the save, he is still held after the load, until the same minute. |
| T11 rough handling | A week starting at 15:36 (the prototype's start), a jump over two hours, a clock going back, a clock that is no number, acts out of turn, a sighting by nobody, the prototype's own ids, a thirty-day jump, eight saves and casts that must be refused | All as they should be. |
| T4x | The same town in Node and in Chromium, the bridge's weeks included | The bridge's weeks give digest d678e26b179e7b68 in both. |
| selftest | One hour of the table spoiled on purpose | T8 sees exactly that hour. |

Size, measured: with the save routines inside, the simulation file is 423,015 bytes, 142,080 with gzip, 108,526 with Brotli. Before the save it was 301,665 and 79,767. So the download is now 109 KB, not 80 KB: the save cost 29 KB.

What the module asks of the page grew from four small system calls to seven. The three new ones are the computer's list of settings, in two calls (answered: none), and "stop" (answered with an error, never reached in any test). The page still gives it no clock time, no random numbers and no files.

## Found on the way: the order of talk inside an hour

The golden table's scripted weeks and the packaged game do not run an hour in the same order.

- The table's weeks (ledger/PerceptionGolden/Program.cs, EmitTownWeek) run each hour's steps and then the talk since the hour before. So news found at five o'clock is passed on in rounds dated from six minutes past four.
- The packaged game runs the talk of the hour before first, then the hour's steps (CrimeProbe.cpp line 7956, "THE HOUR BEFORE'S TALK FIRST"), and lets the talk follow the minutes. News found at five travels from five.

The bridge can do both. "By the hour" is the table's way, and is how T8 holds the bridge to the C# rows. "By the minute" is the game's way and the default, because the prototype should play what the game plays.

Measured, the same six weeks both ways: 129 of 225 hours come out identical. The other 96 are all in the two weeks that hold a deed, from five in the afternoon of the deed's day on. What differs is the count of stories the town holds at 96 hours, and at one hour who finds the damage (in the tea-day week, one person more finds it at eight the next morning by the minute). Who went to the police, DS Ellis's first visit and the first arrest come out the same in all six weeks. Moving his acts a minute later leaves both counts as they are, 0 and 96 (tried once by hand in this run, not part of the script).

So the game's own order is held to the C# Core only indirectly: the same code, proved by the hour. A set of golden rows played the game's way would close that. It is a finding for the Core's owner, not a fault of the bridge.
