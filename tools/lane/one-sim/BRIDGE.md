# The plain bridge between the prototype and the one town (step 3a)

Task 4s, run 2, 19 November 2026. Written and tested the same day. Nothing in the prototype's own source was changed: the swap is step 4, a later round through the publish gate.

Seen by a fresh reviewer the same day (production/lane/REVIEW-ONE-SIM-RUN2.md: pass with fixes). Run 3, also 19 November, closed the holes it found in the bridge's own checks, added the way in for a save from before the swap, and ran a breaker over the result. Run 3's work has not had a fresh reviewer.

## In five lines

1. The bridge is one JavaScript file, wasm/one-sim-bridge.mjs (41 KB, 14 KB compressed; 15 KB before run 3 added the refusals, the old-save reader and the table of the prototype's kinds), over the loader (wasm/one-sim.mjs). It holds no town rule.
2. The prototype hands it its clock every simulation step. The bridge turns the clock into the same calls, in the same order, that the packaged game makes to its town code.
3. It hands back what each new hour did (who found the damage, who went to the police, DS Ellis, an arrest, Ada's invitation, Ron's envelope), and on request where people are and who knows what.
4. The town travels in the prototype's save as one plain object. Loaded into a fresh copy of the simulation it plays on exactly as if it had never stopped (tested, 6 of 6 weeks, under Node and in a real page).
5. Money, debts, jobs, fares, fights and talk stay in the prototype's own code. So do its street, its walking, its light and lines of sight, its weather, its car and its screens.
6. (run 3) A call the town would take in silence and that would leave it wrong is refused by the bridge with its reason, and changes nothing: an act out of turn, a second deed, an area or a story name the town does not know, a save whose pieces do not fit. A save from before the swap keeps loading.

## What the prototype calls each tick

One call, in clock.js simStep, right after the clock has moved (`G.t += dm`):

    for (const hour of town.tick(G.t, area)) onTownHour(hour);

- `G.t` is the prototype's own clock: game minutes since Monday 00:00, fractions and all.
- `area` is where he stands, as the cast file names areas (mickeys, ritas, quay and so on). The town uses it for one thing: who sees it when a constable takes him at ten. The game falls back to "mickeys" when it cannot tell, and so does the bridge when no area is given. An area the cast file does not have is refused (run 3): the prototype's own street names, such as "Quay Street", are not areas. `town.areas()` lists the cast file's.
- Handle the whole list before moving the clock again. If the handling of an arrest hour starts a clock skip from inside the loop, the hours of that skip reach the page before the rest of this list. The breaker tried it: every hour still comes once, the later ones first.
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

Each takes the prototype's clock at that moment. The clock must have been ticked to that minute first, so that an hour that has begun has had its steps before he acts in it. The bridge refuses an act out of turn and says why. Since run 3 that holds for every call below, the tea's minutes and the week's end included (the review found three that skipped the check).

| Call | When | What comes back |
|---|---|---|
| `town.deed({ minute, area, thing, said, witnesses, fact, words, certainty })` | He damages something. `witnesses` is who saw it and how well: `[{ id, rung }]`. Whoever is in the area and did not see it done finds it at once, and others as they come by. | `{ taken, dropped }`: the witnesses the town took, by the cast's ids, and the ones it does not know, each with why. |
| `town.saw({ minute, who, rung, fact, area, words, certainty })` | Somebody saw him do something that is no damage. One call a witness. | true, or false when the witness is nobody of the cast. |
| `town.answerAsk(askDay, answer, minute)` | His answer to a night's ask: the envelope handed over, a no, no show. | true if the town took it. |
| `town.teaMinute(minute)` | A minute he spends at Ada's tea. | |
| `town.weekAsksNow(minute)`, `town.weekAsk(minute)`, `town.weekGive(answer, minute)` | Whether Sheila asks now, her question at the week's end, and his answer. | true or false. |

What the town does with them, and what it does not (run 3, after the review):

- The town follows one deed. The rules keep one deed's story and its witnesses (TownWeek.h Deed), and a second deed would replace the first, witnesses and all. Before run 3 a second, unseen deed made the first one's witness never go to the police. Now a second deed is refused with that reason, and `town.deedHeld()` says which deed the town holds. A further piece of damage can be told with `saw`, one call a witness: it becomes talk. The damage itself is then not there for passers-by to find.
- Only the deed reaches the police, and always as damage. A sighting goes into the talk and can bring DS Ellis, but it is never a statement and never an arrest. A blow, a weapon or a killing has no call that reports it. The raw front door has one (`policeReport`, `takeIn`), used by one scripted week of the tests; the bridge does not wrap it. Whether it should is decision 5 of DIFFERENCES.md.
- Every sighting is kept as about his hidden life. An open or decent act has no call (DIFFERENCES.md, section 10).
- Most of the prototype's people are not in the cast (19 of 28). A witness the cast does not have is left out and named in `dropped`, never taken in silence. A witness named twice counts once.
- In turn means: at the clock's minute or later, inside an hour that has had its steps. An act given a later minute of that hour is taken, and it moves the town's clock to that minute, so a tick at an earlier minute after it is refused as a clock gone back. The prototype's acts happen at its own clock, where the two are the same.
- Refused, with the reason, and nothing changed: an area the cast file does not have; a story name that is not letters, digits and underscores; a story name the town's own rules use for their own stories (the asks, an arrest, DS Ellis asking, the week's end, a threat, his name, his arrival); a rung outside 0 to 4 (or -1 for a thing known); a certainty outside just above 0 to 1; a thing damaged, words about the damage or a story's words that are empty (the town keeps no damage for a thing with no name, and would still have sent the witness to the police over it); a call with no arguments or the wrong kind.

Who saw him, and how well, is still the prototype's to work out: its own geometry (distance, light, line of sight) and, for now, its own way of turning that into "how well". The real rule for "how well" is in the town code and in the golden table, but has no call on the front door yet (see "Not done yet").

## How saves carry the town

    G.town = town.save();                                        // in saving.js serialize, with the other keys
    town = await openTown({ wasm, castJson, saved: G.town });    // in restore, before the people are rebuilt

- `save()` returns one plain object. Inside are the same texts the packaged game writes into its save folder (CrimeProbe.cpp SaveEncounterToDisk): the town's talk (the game's agents.json), each person's memory as text (memory-<id>.md), the week's pieces (town.json), and the few lines the game keeps beside them (the deed's story and time, who saw it, her first visit, his first arrest). Each is written and read by the town code's own save routines. The bridge adds its place in the week: the minute it has run to, and the next hour due.
- Size: the biggest save in the tested weeks is 16,826 characters. The prototype stores its save in pieces of 150,000.
- A town saved, loaded and saved again gives the same save, character for character.
- `openTown({ saved: G.town })` with nothing in `G.town` is refused (run 3). Before, it opened a new week at minute zero without a word, and the next tick would have played every hour since Monday over a week already lived.

What is checked before a save is taken (run 3 added most of these after the review; each is refused with its reason, and the town that is refused is dropped whole):

- It is a saved town, of a version this build reads, with a way of talking it knows.
- Every piece is there and is the piece it says it is: the talk and the week's pieces are JSON objects; the talk holds every person of the cast; the week's pieces say how far the talk has run; there is a memory for every person, it is text, and it is that person's memory; the lines beside the week read.
- The clock fits itself: a whole minute, and the next hour due is the one after it (or the minute's own hour, for a town saved on the stroke of an hour before that hour ran).
- The clock fits the town: the town's own record of how far its talk has run is not past the saved minute, and not short of the last hour said to have run. A clock moved back would play hours over a town that has lived them; a clock moved on would skip hours it never had.
- The town's own readers then refuse what they refuse: a talk that is no whole text, a week from a later version.

The cast file and the save (run 3, the review's finding 7). The save carries a mark of what it rests on in the cast file: who is in the town, and its areas with their places. It is no longer a mark of the file's text, which changed with a Windows checkout's line endings and would have refused every save.

- The file's byte-order mark, line endings and spacing, its notes, its routines, its ties and its coordinates may change, and the save still loads. The town then plays on by the new file, as the packaged game does: its save holds no cast at all.
- If people, areas or places are added, taken away or renamed, the save is refused with a plain message that names who is in the save and not in the cast, and the other way round. Loading such a save "with the people still present" is not built. The names decision (DIFFERENCES.md, decision 1) changes what people are called, not their ids, so it does not trip this.

A prototype save from before the swap (run 3, the review's finding 3):

    const { town, hours, fed, dropped, lost } = await openTownFromOldSave({ wasm, castJson, old, areaOf, wordsOf });

- It has no town in it. It opens a fresh town at the save's clock (`old.t`). `hours` is what the first tick ran, to be handled like any tick's.
- Each thing its people saw him do with their own eyes is told to the town at that minute, as a sighting, under the kind's name with the event's number (strike_e7). `fed` lists them.
- The rung is read from the old memory. This is the bridge's reading of the prototype's memory, not a town rule, and step 4 may hand in another (`rungOf`): "tom" or "owner" (they tie it to him): recognised. "coat" or "cab" (a thing of his): a mark. "man" with a face score above 0.2, the prototype's own line for placing him later: a face. Any other "man": a silhouette.
- Left out, each named in `dropped` with its reason: what somebody was only told, or only heard; what people who are not in the cast saw; the kinds the town makes itself, cannot be told, or never passes on (DIFFERENCES.md, section 10); a place with no area in the cast.
- `lost` says in plain lines what the player loses, counted from that very save: the tea if its hour has passed, the asks already past, and the rest.
- `areaOf(event)` must give the cast file's area for where an old event happened. That table is step 4's (below); the default is the game's own fallback, "mickeys".
- The save version of the prototype stays as it is.

## The people and the places

- Nine people are in both casts. The bridge takes either id for them: sheila is lena in the cast file, ron is rocco, darren is sam, alison is noor, walsh is emil; ada, june, rita and hal carry the same id on both sides. Six carry the same full name on both sides. June, Rita and Hal have a surname only in the prototype.
- The other 19 people of the prototype have no certain match, and 32 of the real cast's 41 have no prototype id. Which names stand is a canon question, not the bridge's (DIFFERENCES.md, section 1).
- DS Ellis and the constable are people who walk about in the prototype. In the real rules they are steps of the hour. The bridge reports the step (`ellis`, `taken`); the prototype may still show somebody walking.
- Places: the cast file has 30 places in 24 areas. A table from those to the prototype's spots and rooms is step 4's work. Some real places have no spot on the prototype's map yet (DIFFERENCES.md, section 2).

## Not done yet (for step 4, the swap)

Added in run 3, from the review:

- No call reports violence. Only the damage deed reaches the police (above; decision 5).
- The town follows one deed, and the prototype has no act that damages a thing (decision 6).
- No call for an open or decent act: ten of the prototype's kinds have no home (decision 7; a change to the front door, not to the rules).
- No golden row covers two deeds, and none covers a sighting that is no damage. The bridge's handling of both is held by its own checks only.

From run 2:

1. How well a witness sees him. The real rule (Perception, Observation, Sighting) is in the town code, and the golden table's rows for it pass in the browser build (T1). It has no call on the front door yet. Step 4 needs one that takes what the prototype knows (distance, light, in view or not, the coat, in the cab) and gives the rung.
2. The words. The hour gives "Ada asked him in" as yes or no, not her line; the arrest's words and his rights are in the town code too. Add when a screen needs them.
3. What the street calls him, and how much each person likes or fears him. The prototype's own today (gossip.js, events.js). The town code has its own (Suspicion, Reaction, StreetVoice), not behind the door.
4. The two tables: places, and the area he stands in.
5. Golden rows for the bridge's by-the-minute order (next section), and for the details of each Ledger fact. Both are the C# side's to write, so the main session's.
6. The tellings. The town code knows each time a story passes from one person to another; the front door hands out who holds what, not each telling. The prototype's "two people stop talking as he passes" needs them (DIFFERENCES.md, section 8).
7. Two places where the packaged game builds its town a little differently from the front door, which follows the golden table's weeks. The game gives each person the name the street calls them (CrimeProbe.cpp line 5992, the cast file's "called"); the front door names them by id, so a memory line would read "I heard from rocco that". Only words differ, and no screen shows them yet. And the game reads each person's temperament from the cast file for how a witness reacts on the spot (CrimeProbe.cpp, WitnessReacts); that reaction is not behind the door.

## How it is tested

All inside `one-sim.sh all`, under Node and inside a real page in headless Chromium 157. The run's time and result are in PROGRESS.md.

| Check | What it shows | Result |
|---|---|---|
| T8 the bridge, talk by the hour | The six scripted weeks of the C# Core's table, driven by a clock in odd steps (7.3 game minutes) through the bridge, with the prototype's own id for Darren. Each hour against the C# Core's row. | 225 of 225 hours agree, field for field. The bridge's "held" agrees with the hour's answer at all 225. |
| T9 the bridge, talk by the minute | The same weeks the packaged game's way, with the clock ticked every game minute, every 0.37 and every 7.3 (13,146, 35,736 and 2,060 ticks) | The same town to the last character in all three. |
| T10 a save in the middle | Each week saved after two fifths of its hours, at a minute inside an hour, written out as text, loaded into a fresh module, played on | 6 of 6 end exactly as the week played straight through. Held in the cells at the save, he is still held after the load, until the same minute. |
| T11 rough handling (run 3: the review's holes) | A week starting at 15:36, a jump over two hours, a sighting by nobody, the prototype's own ids, a thirty-day jump, a save loaded and saved again; a deed's witnesses taken and dropped by name; the first deed's witness still going to the police on Wednesday at nine, and the constable on Thursday at ten, after a second deed was refused; the cast file as Windows writes it and with its spacing taken out; and 42 things that must be refused | All as they should be. Of the 42, 17 are run 2's (one more save added) and 25 are new: the tea and the week's end out of turn, unknown areas, a story name of the town's own, a second deed, saves whose pieces do not fit or hold nothing, a saved town that is not there, a cast with other people. |
| T12 a save from before the swap (run 3) | An old save written by hand in the prototype's shape (Wednesday 14:00, eight minds) | 4 first-hand memories told at the rungs they support, 8 left out each with its reason, the old save untouched, the losses said in 7 lines. Two days on the blow is held by 23 people and has brought no statement and no arrest; DS Ellis came once, for the talk. The town then saves and loads like any other. |
| T4x | The same town in Node and in Chromium, the bridge's weeks included | The bridge's weeks give digest d678e26b179e7b68 in both: the same as before run 3, so the fixes changed no town. |
| selftest | One hour of the table spoiled on purpose | T8 sees exactly that hour. |
| breaker (run 3, wasm/breaker.mjs) | 191 tries to make the bridge misbehave: opening it (16), the clock out of order (23), bad calls (52), spoiled saves (59), spoiled old saves (11), and a sound save at 30 awkward moments. A refused call must also leave the town's save as it was; a sound save must load, save again the same and play on to the same town. | First pass: 137 of 150 held. Eleven real holes were closed and two wrong expectations of the breaker put right, and a later reading of the code found one more hole, a deed with nothing named (PROGRESS.md lists them all). Now 191 of 191 hold. |

Size, measured: with the save routines inside, the simulation file is 423,015 bytes, 142,080 with gzip, 108,526 with Brotli. Before the save it was 301,665 and 79,767. So the download is now 109 KB, not 80 KB: the save cost 29 KB.

What the module asks of the page grew from four small system calls to seven. The three new ones are the computer's list of settings, in two calls (answered: none), and "stop" (answered with an error, never reached in any test). The page still gives it no clock time, no random numbers and no files.

## Found on the way: the order of talk inside an hour

The golden table's scripted weeks and the packaged game do not run an hour in the same order.

- The table's weeks (ledger/PerceptionGolden/Program.cs, EmitTownWeek) run each hour's steps and then the talk since the hour before. So news found at five o'clock is passed on in rounds dated from six minutes past four.
- The packaged game runs the talk of the hour before first, then the hour's steps (CrimeProbe.cpp line 7956, "THE HOUR BEFORE'S TALK FIRST"), and lets the talk follow the minutes. News found at five travels from five.

The bridge can do both. "By the hour" is the table's way, and is how T8 holds the bridge to the C# rows. "By the minute" is the game's way and the default, because the prototype should play what the game plays.

Measured, the same six weeks both ways: 129 of 225 hours come out identical. The other 96 are all in the two weeks that hold a deed, from five in the afternoon of the deed's day on. What differs is the count of stories the town holds at 96 hours, and at one hour who finds the damage (in the tea-day week, one person more finds it at eight the next morning by the minute). Who went to the police, DS Ellis's first visit and the first arrest come out the same in all six weeks. Moving his acts a minute later leaves both counts as they are, 0 and 96 (tried once by hand in this run, not part of the script).

So the game's own order is held to the C# Core only indirectly: the same code, proved by the hour. A set of golden rows played the game's way would close that. It is a finding for the Core's owner, not a fault of the bridge.
