# LEDGER loop prototype: changelog

## 18 November 2026, lane round 4. A debt that can come to blows (melee, part 2)

Built by the cloud lane. Design question: can a debt turn into a fight in the first hour, decided by where
and how Tom fronts a man up, and do things to hand make that fight a moment a player would retell? Serves the
panel's second complaint of round 3 (nothing kicks off: all five debtors gave way), his combat pick of 18 Nov
(fists and things to hand every day, guns rare) and the melee feel sheet's C12 (hits before breaking). KCD2 is
the measuring stick. The town's simulation (witnesses, gossip, memory, routines) is untouched.

1. Face: a man fronted up with folk within 12 m has more to lose by backing down: 0.06 nerve for each one,
   at most 0.24. The same debtor who gives way in a quiet yard may stand in the street, and then it comes to
   blows in front of witnesses. He says why ("Not in front of this lot, you don't.").
2. Corners: a man shoved back into a wall with nowhere to go gets 0.2 nerve and is likelier to come off it
   swinging ("You've got me against a wall. Big mistake.").
3. Tom's name is read once, when he starts to front a man up. Before, each stare, threat and shove of the
   same fronting-up went into the man's memory and was counted again on the next rung (0.24 by the shove),
   so nobody ever stood.
4. Things to hand mid-fight: [G] snatches up the nearest chair, brick, dustbin lid, wheel brace or cargo hook
   within reach. It takes half a second and a blow landing in that moment stops it; it comes out as a weapon,
   with what that costs Tom in the town.
5. Breakage (C12): a chair goes to pieces after 2 blows, a brick crumbles after 3, a dustbin lid buckles after
   4; a wheel brace or a cargo hook, like the sheet's pipe, does not break. A broken chair or lid stays broken;
   a skip or a scrap heap has more. The count stays with the thing, carried from one fight to the next.
6. Test: test/melee4.mjs (face, corner, grab, drill M7 for each thing, a lid carried across two fights).

## 18 November 2026, lane round 3. Fists with weight (melee, part 1)

Built by the cloud lane. Design question: when a debt turns into a fight, do the blows land with weight, can
a player read what is coming, and does the street react, so a fight is a moment a player would retell? Serves
his combat pick of 18 Nov (option A with an escalation dial: fists and things to hand every day, guns rare;
melee first) and the melee feel sheet (production/research/lane/FEEL-TARGETS-MELEE-2026-11-18.md, bands C1 to
C15, measured with its drills). KCD2 is the measuring stick. The town's simulation is untouched: onlookers
only show it on their faces; what they make of a fight stays the witness rules' own business.

1. Hit-stop: on contact both men are held for a moment, 0.04 s for a jab, 0.09 s for a heavy blow, 0.10 s
   for a swung weapon (C3), with a small camera shake on a heavy blow.
2. Timings in the sheet's bands: Tom's jab lands 0.28 s after it starts (C2 0.25 to 0.40), his heavy 0.70 s
   (0.63 to 0.85); a man struck reels 0.55 s from a jab and 1.05 s from a heavy (C4); Tom is busy 0.30 s after
   a jab lands and 0.46 s after a heavy (freeze not counted); a missed heavy costs 0.80 s.
3. Walls: a man knocked back with a wall close behind him hits it: more hurt, a heavy reaction (1.15 s) and a
   thud ("Into the wall."). A shove into a wall shows the same way.
4. Outnumbered: at most two men swing at Tom at the same moment, their swings at least 0.45 s apart, and no
   man waits more than about 2.2 s between swings (C8). A man winding up a heavy blow often shouts first, at
   least 0.45 s before it lands (C13).
5. Onlookers: people within 20 m who are standing about stop and look; the timid shrink back; some call it
   out ("Fight!", "Somebody fetch the police!"). Walking or seated people carry on.
6. Breath: Tom gets no breath back while still swinging, so 8 or 9 jabs tire him (C11 6 to 10) and he is back
   to full in about 6 s.
7. Each debtor refuses in his own words with his own reason (the panel's second complaint of round 2).
8. Tests: test/melee3.mjs runs the sheet's drills through the test hook at 1/60 s (jab, heavy, a man against
   a wall, three men, stamina) and writes the drills' record for tools/lane/melee_drills.py. The playtester's
   newcomer now fronts up a debtor who will not pay, as the game invites, and fights as a first-time player
   would. Old saves load (the fight's state is never saved).
9. After a fresh review (PASS WITH FIXES): Tom's blow stopped by a man's guard is recorded apart from Tom's own
   blocks; every attack begun is recorded as over whatever ends it; a man's wait between swings is capped;
   the missed heavy shortened into its band; onlookers who are walking or seated are left be, and the fight's
   end clears only the looks it gave; a shove into a wall no longer adds lasting fear.

Not yet (next melee rounds): picking up a chair, a brick or a pipe and breaking it (C12), closing in on a blow
(C9), the camera close-in (C10), the kerb fall rule (C7), and the playtester's fight sample at more debts.

## 18 November 2026, lane round 2. The carry under watch

Built by the cloud lane. Design question: does a night carry past a watching constable give the first half
hour a tense moment a player would retell? Serves the real game's night-job spec (a delivery under watch, the
risk of being seen by the town's own eyes) and Study 15's search rule (a search follows suspicion, never chance;
found goods are kept). Study 16: a failed job is not the end; the Ledger says "The bag was taken" and later
scenes read it. The town's simulation is untouched: with the constable left out, the seeded week is the same as
round 1's part for part; with him in, the week bot meets him, so the week's record was rewritten.

1. When Tom lifts the bag or the parcel, PC Ibbotson walks a beat between the pick-up and the drop, back and
   forth (`jobs.beatStartsAlongTheWayFraction` 0.35, `jobs.beatEndsShortOfTheDropFraction` 0.15, 1.1 m/s, at
   most 240 real seconds). He sees with the town's own eyes: lamps, line of sight and where he faces, so in the
   dark he sees about 4 m and under a lamp much further. Ron's advice now matters: keep out of the light.
2. Seen with the bag within 16 m (`jobs.challengesWithinMetres`), he calls out: "You. With the bag. Stop there
   a minute." Stand, and he searches: the bag is taken, the job is lost (the Ledger and Sheila's Friday read
   it), the street hears of it (a new act, `bag_taken`). Run, and it is a chase with the police's own chase
   numbers: out of his sight 7 s or 70 m away and he gives up; Tom keeps the bag and can still knock, but it
   is a run from the police the street can see and talk about (`ran_police`).
3. In the evening of the first day the to-do note says Ron is waiting at the cab rank: the playtester's
   newcomer never heard the first night's offer in an hour before; now it takes the job at 13.5 minutes.
4. Tests: test/watch2.mjs (the beat starts at the pick-up; unseen behind him in the dark; searched when
   standing; a chase lost round a corner keeps the bag and the drop still works); oldsave passes (saves
   without the watch load). The playtester carries the bag a step at a time and runs when called out to.
5. After a fresh review (PASS WITH FIXES, all applied): a taken bag leaves the to-do list; getting into the cab
   or a doorway is no instant escape (he looks for the cab or the door, as in an arrest; the 7 s unseen rule
   decides); a call-out lasts at most 12 real seconds (`jobs.challengeLastsAtMostRealSeconds`); he stays for his
   own search lines; only a constable's arrest (not DS Ellis's) stops the beat; the parcel no longer clinks.

## 18 November 2026, lane round 1. The eight fixes from the first playtest

Built by the cloud lane, not Fable. Design question: does the loop hold up for a first hour once the faults
that break a playtest are gone? Serves the real game's talk spec (written-line fallback, conditions on lines,
barks and subtitles), its interaction-targeting rule, the Ledger's knowledge rule, objective text and the
paid-information rule. No new systems, places, people or story; the town's simulation is untouched (the seeded
week's events, memories, stories, money, debts and Ledger are the same part for part; only the save's talk
log, stats and time stamps differ, so its record was rewritten).

1. Talk never gives the same answer twice in one talk. A person's own stock answers come first; the shared
   pool ("Same as ever. Less of it.", "He'd have liked the turnout") is used at most once a talk and each shared
   line by one person a day. With nothing fitting left, the person closes the talk in their own voice (one line
   each for the named people) and only a way to leave is offered.
2. The talk prompt, E and Q go to the person Tom faces: within about 30 degrees (`ladder.targetWithinFacingRadians`
   0.52, was 1.2) and a named or marked person preferred only when within 0.3 m of the nearest
   (`ladder.namedPreferredByMetres` 0.3, was 1.2; the extra metre for marked people is gone).
3. Speech bubbles only from someone within earshot (`talk.bubbleHeardWithinMetres` 20) and, on the street, in
   Tom's line of sight; no empty bubbles; the same line from a second person within 10 real seconds stays unsaid
   (`talk.sameBubbleQuietRealSeconds`).
4. Greetings follow the hour: Morning, Afternoon or Evening by the clock (`talk.morningUntilHour` 12,
   `talk.afternoonUntilHour` 18, `talk.eveningGreetingUntilHour` 4).
5. No name before Tom has learned it: Ada's window prompt says "the old woman at the window" until he knows her
   name, and shows only when he can see her there.
6. The to-do note never outlives its hour: when Ada's tea passes unattended, it says the tea was missed.
7. A street matter (a debt, an offer) never leaves the talk dead: Leave is always offered beside it, a no to
   the matter itself drops it and brings the ordinary lines back, and a matter with nothing left to say lapses.
8. Paying for help gives something or is not offered: Ron's fiver for the door and Darren's three pounds are
   offered only when they know something Tom does not; a pound pressed on them with nothing to tell buys only
   their goodwill (and silence with the police), never an invented "nobody saw a thing".

A fresh review then found three slips, fixed before this build: the missed-tea note now also replaces the
other "Ada at seven" notes; a street matter with only Leave left lapses so the ordinary lines return; a closed
talk always offers a way to leave. Still open: the facing rule picks the nearest person inside the 30 degrees,
not the one closest to the line straight ahead.

Tests: `test/fixes1.mjs`, one check a fix (in Node for 1 and 4, in the source for 3 and 8, on the page for 2,
5, 6 and 7), added to `npm test`. All earlier tests pass; an old save loads. The playtester's numbers before and
after are in RESULTS.md.

## 18 November 2026, second round. Every number in the rules table, routines retimed, three fixes

No new systems. Walking pace and the rules of seeing and pausing are as they were. Old saves still load.

### 1. Every rule's number in `LEDGER.rules`, changing nothing

- Moved into `src/rules.js`, each under a plain name with its unit: the confrontation ladder (129 names),
  the story's hours, distances and regard (107), talk (55), the routines and the anonymous crowd (59), the 52
  kinds of thing the town can know, each person's numbers (28 people), the 28 weekly schedules, Tom's own
  pace, shop hours, driving, traffic, and smaller groups in police, rest, naming, light, weather and time.
  `rules.js` now holds 1,313 numbers in 32 sections.
- A move cannot change a value: `tools/numbers.mjs` writes each number's own text into the table. The kinds
  and the cast were also compared whole, before and after: identical, key order included.
- Left where they are, 375 numbers in the 22 rule files, counted by reason so none can be added unnoticed
  (`npm run numbers`): 58 unit conversions, 69 indexes and plain arithmetic, 29 text and layout, 53 places on
  the map, 84 camera and controls, 82 how people and things look. The numbers 0, 1 and 2 (1,053 of them)
  were left in place without being looked at one by one.
- Proof that nothing changed: one full scripted week, played with a fixed seed on a clock the test owns,
  gives exactly the same save on the page published earlier today and on the build with the numbers moved.
  All 19 parts of the save are the same (events, every mind's memories, stories passed on, money, debts, the
  Ledger, the measures): whole digest `d45ae942a389fab4d9a4` both times, and the same again on a second and
  third run. This is now a test, `test/same_week.mjs`, with its record in `test/golden/`.

### 2. Routines retimed

- What the check found first: with Tom kept at the rank, 59 of the 157 walks in the schedules had too little
  time, not only the walks to the map's edge and the watchman's rounds. Within 90 metres of Tom people walk at
  their real pace, a game minute to the metre, and the rank is where the quay end's routines cross.
- The rule used: every row leaves room for its walk and a quarter again, with Tom away and with Tom at the
  rank. `tools/walk_times.mjs` works this out from the game's own paths: all 145 walks now fit.
- Twenty-two people have longer rows:
  - The drivers. Kevin makes one run away a day (10.12am to 1.12pm) instead of two. Terry makes two runs a
    night instead of three. Each walk to or from the map's edge has three hours.
  - The watchman. Norman makes three rounds a night instead of five, each leg with about an hour and three
    quarters, and comes in for his chips at 3.54pm.
  - Lunch and errands lengthened by 6 to 70 minutes: Sheila, Ron, Rita, Wayne, Hal, Shaun, Father Walsh,
    Mrs Rennison, Julie, Susan, Brenda, Darren.
  - Long walks through the quay end given three to four hours: Lee and Dennis (lunch at the caff), Nora (the
    fish queue), Alison (her round now runs 7am to 6.12pm), June (the ferry landing), Susan (in at 6am).
  - Stops that went, because the day could not hold them: Albert's breakfast at the caff, June's Monday
    evening walk to the ferry.
  - Ada goes to chapel at 6.12am on Wednesdays, not 8am, so she is back at her window to ask Tom to tea.
- `LEDGER.check.arrivals()` now keeps Tom at the place named for the whole of it. Before, the game put him to
  bed at 4.24am and the rest of the check ran with him indoors.
- Both checks over 26 game hours, from Mon 15 Oct 3.42pm (`test/arrivals.mjs`, results in `RESULTS.md`):

| Tom | Walks set off | Arrived | Given up for another place | Still on their way at the end | Stood still | Pause never ended |
| --- | --- | --- | --- | --- | --- | --- |
| Away, before | 163 | 142 | 16 (9 at the map's edge) | 5 | 0 | no |
| Away, after | 153 | 150 | 0 | 3 | 0 | no |
| At the rank, before (until 4.24am only) | 163 | 136 | 22 (9 at the map's edge) | 5 | 0 | no |
| At the rank, after (the whole 26 hours) | 153 | 142 | 0 | 11 | 0 | no |

- The gossip before and after. One scripted week with the same seed on each build; each cell is before then
  after. A sighting is one person seeing Tom do a thing (an act that goes on is counted each time it is seen
  again). A pair has met when two named people stood within talking distance. `LEDGER.gossip()` returns it.

| Day | Sightings | Stories passed on | Furthest story (tellings) | Pairs of named people who met |
| --- | --- | --- | --- | --- |
| Mon 15 Oct | 161 then 98 | 11 then 16 | 2 then 3 | 14 then 27 |
| Tue 16 Oct | 6 then 11 | 52 then 87 | 4 then 5 | 48 then 79 |
| Wed 17 Oct | 0 then 0 | 31 then 18 | 8 then 6 | 43 then 69 |
| Thu 18 Oct | 2 then 3 | 31 then 14 | 9 then 4 | 53 then 73 |
| Fri 19 Oct | 0 then 0 | 22 then 53 | 5 then 8 | 54 then 82 |
| Sat 20 Oct | 0 then 0 | 6 then 9 | 5 then 8 | 17 then 29 |
| The week | 169 then 112 | 153 then 197 | 9 then 8 | 62 then 95 |

Met in the week after, not before (43): ada + albert; ada + june; ada + nora; ada + walsh; albert + alison; albert + brenda; albert + nora; albert + walsh; alison + julie; alison + kevin; brenda + nora; brenda + susan; brenda + terry; darren + lee; darren + nora; darren + norman; dennis + grace; dennis + julie; dennis + rita; dennis + shaun; dennis + sheila; dennis + wayne; grace + kevin; grace + lee; julie + kevin; julie + lee; julie + nora; julie + sheila; june + lee; june + susan; kevin + norman; lily + norman; lily + terry; nora + ron; nora + sylvia; norman + peter; norman + ron; norman + susan; norman + terry; pauline + terry; peter + terry; rita + shaun; rita + sheila.

Met in the week before, not after (10): ada + darren; albert + kevin; albert + susan; alison + darren; alison + dennis; alison + june; alison + sylvia; darren + julie; june + kevin; lee + susan.

- In short: more people cross each other's paths (62 pairs then 95) because they are out on the street for
  longer, and more stories are passed on (153 then 197). The furthest story travelled 9 tellings, then 8.

### 3. Small fixes

- a) "Nobody saw" never disappears. An act waits two game minutes; if no watcher is known by then the line is
  written, and from then on it can only be struck through with the day and the reason. If a watcher is known
  before the wait is over, nothing is written. No entry is ever taken out of the book.
- b) In People, `/` and then a letter jumps to that letter: any letter, E, L and Q among them. It goes to the
  first page under the letter and says so when nobody is under it. Esc lets the jump go.
- c) The two first-round scripts are replaced by tests through the hook that pass or fail, and both are in
  `npm test`: `test/town.mjs` (what `logic.mjs` printed: being seen, the ladder and the priest, the police
  and custody, Ada's tea, the second ask, Iveson's yard, DS Ellis, the lads, saving and loading) and thirteen
  checks added to `test/week.mjs` (what `play.mjs` printed). `test/ledger_rules.mjs` checks a) and b).

### 4. Found on the way, and fixed

- A constable coming for Tom could walk back and forth in the lane east of Quay Street and never arrive: he
  planned his way afresh every second and a half, and there the way flipped between two ways round. He now
  keeps to his way while Tom stays where he was. The town test could not pass without this.

### 5. Test hook additions

- `LEDGER.gossip()`: the gossip table, day by day.
- `LEDGER.ledger.act(kind)`: an act at a moment of the test's choosing. `LEDGER.ledger.learn(eventId,
  personId)`: a watcher turns up. `LEDGER.ledger.waiting()`: acts still waiting to see whether anybody saw.
  `LEDGER.ledger.read().said`: the line the book says back.
- `LEDGER.check.arrivals()` reports `tomPutBackThereTimes`.
- The test harness has a seeded, stepped mode (`launch({ seed })`): the same seed gives the same week on any
  machine.

## 18 November 2026, first round. Readable source, known faults, test hook, Ledger screen test

No new systems. Rules, story, numbers and saves are as they were except where a fault below is fixed.
Old saves still load.

### 1. Readable source

- The source is one file per part and formatted (Prettier): `seeing.js`, `gossip.js`, `events.js` (events and
  memories), `ledger.js`, `ledger_screen.js`, `money.js`, `fares.js`, `jobs.js`, `police.js`, `routines.js`,
  `talk.js`, `talk_lines.js`, `saving.js`, `scenes.js`, and the picture under `render/`. See `README.md`.
- The first formatting pass produced a byte-for-byte identical build, so nothing changed by being reformatted.
- three.js is pinned at 0.187.0, esbuild at 0.28.2. The build is `npm run build` (see `BUILD.md`).
- The page (`index.html`) is now a source file, `src/index.html`, copied into the build.
- Leftover re-exports and 46 unused imports were removed.

### 2. Faults fixed

- a) `LEDGER.restore(text)` now loads a saved week exactly as Continue does: the people are rebuilt around
  their restored memories and each mind gets its index back. Continue and the hook share one function.
- b) Ron no longer stands three metres from the rank all night. A witness pauses in their walk once for one
  act, and not again for 20 real seconds: an act that goes on (being out in the small hours) is seen again and
  again and used to renew the pause before it ran out. New check: `LEDGER.check.arrivals()`.
- c) Every pause and resume is now logged with the game time and its reason (`LEDGER.pauses()`), and
  `LEDGER.check.nights()` steps through Tuesday and Wednesday night and reports any pause with no resume.
  What it found, and what was changed:
  - Fades and goodbyes were timed by the browser's timers. A browser holds its timers back, by up to a
    minute, in a tab that is not showing: the game stayed paused until the held timer fired. They are now
    timed by the game's own steps (with the browser timer behind them as a fallback), so a pause ends the
    same way in a showing tab, a hidden tab and a stepped test.
  - The blocks that pause the game while they work (sleep, custody, the beating, tea, the chapel, falling
    into bed) now always end their pause, even if something inside them throws.
  - A written line said outside a scene left its box open and the game paused; it now closes itself.
  - A watchdog resumes, and logs as a fault, any pause that nothing is holding for three real seconds.
- d) The slip in talk sits inside the talk box, beside the typing box. Subtitles ride above the talk box and
  the written-line box while either is open. Checked at four window sizes by `test/layout.mjs`.
- e) Rent is late from Friday 6pm game time, as Mrs Rennison's line says ("Friday, by six"). It was Saturday
  00:00.

### 3. Test hook (`window.LEDGER`)

- Suggested lines and decisions: `LEDGER.talk.open(id)`, `.lines()`, `.say(which)`, `.type(text)`,
  `.answer('yes'|'no'|'keep')`, `.key('Tab'|'F2')`, `.leave()`. `talk.open` goes up to the person and presses
  E, so a waiting written scene (a first meeting, a job offered) runs as in play.
- Written scenes: `LEDGER.written.read()`, `.next()`, `.choose(n)`.
- Prompts and keys: `LEDGER.prompts()`, `LEDGER.press('E')`. Named places: `LEDGER.places`,
  `LEDGER.insidePlaces`, `LEDGER.goTo(name)`, `LEDGER.goInside(name)`, `LEDGER.goOutside()`.
- The night job: `LEDGER.job.read()`, `.goToPickUp()`, `.goToDrop()`, then `LEDGER.press('E')` at the drop
  door. Washing: talk to Sheila and `LEDGER.talk.answer('yes')`.
- The fare: `LEDGER.cab.getIn()`, `LEDGER.fare.call()`, `.accept()`, `.pickUp()`, `.dropOff()`, with the
  places by name in `LEDGER.fare.read()` and `LEDGER.fare.places()`.
- Readable numbers: `LEDGER.read()` and `LEDGER.person(id)` use plain names with units (Pence, GameMinutes,
  Metres, RealSeconds, ZeroToOne). Every rule's number is in `LEDGER.rules` (`src/rules.js`).
- Checks: `LEDGER.check.arrivals(options)`, `LEDGER.check.nights(options)`. Pauses: `LEDGER.pauses()`.
- The Ledger and its measures: `LEDGER.ledger.open(part)`, `.rows()`, `.key(code)`, `.mark(row)`, `.book()`,
  `LEDGER.measures()`, `LEDGER.measuresJSON()`.
- Everything the hook had before is still there under the same names.

### 4. The Ledger screen test

- L opens it anywhere (in play, over a talk, over a written line) and L or Esc closes it. Tab never opens
  it. It pauses the game, or the talk under it, and gives that back when it closes.
- Four parts as tabs: People, Day book, Open, Money. Q and E change part. It opens on the part last used.
- People: a page per person met or noticed, newest first, with an A to Z index; a typed letter jumps there.
  A page is headed by the description until the name is learned, then by the name with the description
  struck through beneath it.
- Day book: a page per day, the week so far in five lines at most, then entries with time and place.
- Open: things waiting, with a day only where somebody said one. Closed lines are ruled off and stay.
- Money: pounds and pence, only sums Tom knows.
- Every entry: when, what (22 words at most), how Tom knows, sureness in words only when unsure, and its
  source event. A wrong belief is struck through with the day and the reason and is never deleted.
- Wording: clipped notebook entries without "I" or "me". Money "£18.00", "80p". Times "6.30pm". Dates
  "Fri 19 Oct".
- The Noted line: never while a subtitle shows, about 4 seconds, one in 10 seconds at most, extras counted
  ("Noted in the Ledger: 3 things").
- The slip in talk starts folded to its heading; F2 unfolds it; the choice is remembered.
- The end screen's truth view is labelled a playtest view and has a setting to switch it off.
- Measures are logged, shown on the Playtest measures screen (pause menu and end screen), exported as one
  JSON file and returned by `LEDGER.measures()`. Scripted find-the-fact asks come up on Tuesday 9.30am,
  Wednesday noon, Thursday 10am and Friday 9am; keyboard and pad are kept apart.
- A pad drives the Ledger (and only the Ledger): View opens and closes it, LB and RB change part, the D-pad
  moves, A marks, B closes.

### 5. Published beside the page

- The source files, the build command, this changelog, the design notes, the measures from one full week
  and the list of what could not be done are published as files beside `index.html`, and listed in
  `files.json`. In the game, "Source and files" (title screen and pause menu) lists them and shows any of
  them as text, with a Copy button. Where the host allows saving, one button saves all of it as one zip.
- The measures export and the file saves go through the host's save door (the `downloads` capability),
  because a page in this viewer may not start a download itself. Where there is no door, the JSON is shown
  to copy.
- The Open part writes "Fri, by 6pm" for the rent only after Mrs Rennison has said "by six", and "Today"
  for Sheila's question only once she has asked it. Before that the line has "Fri", or no day.
- The Design notes text moved to `src/design_notes_text.js`, so `DESIGN_NOTES.md` is written from the
  same text the game shows.
