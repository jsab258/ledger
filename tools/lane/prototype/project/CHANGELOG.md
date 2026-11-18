# LEDGER loop prototype: changelog

## 18 November 2026. Readable source, known faults, test hook, Ledger screen test

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
