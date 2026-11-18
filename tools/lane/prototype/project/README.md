# LEDGER loop prototype

Meridian, a port town on the Humber, October 1990. Tom Nowak inherits Mickey's minicab office. He moves, is
seen, it is written down, it spreads, it comes back. The Ledger shows only what Tom believes.

One page, built with three.js 0.187.0. No server. The published page is `dist/index.html` and
`dist/ledger.js` with the art beside them.

    npm ci
    npm run build        # writes dist/
    npm test             # nights, layout, files, one full week (needs Chrome, see BUILD.md)

Read `BUILD.md` for the build, `CHANGELOG.md` for what changed and when, `NOT_DONE.md` for what is missing,
`DESIGN_NOTES.md` for every choice made without asking.

## The source, one file per part

All of it is under `src/`. Every rule's number is in `src/rules.js`, with the unit in its name.

| Part | Files |
| --- | --- |
| Seeing | `seeing.js` (who can see Tom, how well, what they make of it), `light.js` (one light field for picture and rules) |
| Gossip | `gossip.js` (passing on, fading, coming back, what the street calls him), `events.js` (events and memories), `kinds.js` (every kind of thing the town can know) |
| The Ledger | `ledger.js` (the book: entries, source events, striking through, the Open and Money parts), `ledger_screen.js` (the screen, the slip in talk), `measures.js` (the Ledger screen test) |
| Money and debts | `money.js` (pocket, tin, paying, washing through the fare book), `fares.js` (the cab fare), `jobs.js` (the night jobs and the drop doors) |
| Police | `police.js` (what reaches the station, the constable, custody, DS Ellis) |
| Routines | `routines.js` (people as agents, walking, trips), `cast.js` (the people and their week), `map.js` (the town and its named places), `clock.js` (one step of the simulation) |
| Talk | `talk.js` (live talk, suggested lines, decisions), `talk_lines.js` (written lines) |
| Saving | `saving.js` (save, restore, old saves), `state.js` (what a week holds, the pause book) |
| Scenes | `scenes.js` (the week's beats and written scenes), `work.js` (passing time, sleep, being beaten), `fight.js` (the confrontation ladder) |
| Rendering | `render/core.js`, `town.js`, `rooms.js`, `cars.js`, `figures.js`, `rig.js`, `tailor.js`, `actors.js`, `extras.js`, `effects.js`, `sync.js` |
| Rules | `rules.js` (the one table, exposed as `LEDGER.rules`) |
| Test hook | `hook.js` (`window.LEDGER`), `checks.js` (`LEDGER.check.arrivals()`, `LEDGER.check.nights()`) |
| The rest | `main.js` (boot, the loop, menus), `ui.js` (HUD, panels, the Noted line), `player.js` (keys, walking, camera), `drive.js`, `audio.js`, `util.js`, `end_screen.js`, `design_notes.js`, `design_notes_text.js`, `files_panel.js`, `index.html` (the page and its styles) |

## The test hook, in short

`window.LEDGER` in the page. Numbers have their units in their names: pence, game minutes, metres, real
seconds.

- `LEDGER.rules`: every rule's number, by name.
- `LEDGER.read()`, `LEDGER.person(id)`, `LEDGER.people()`, `LEDGER.places`, `LEDGER.insidePlaces`.
- `LEDGER.goTo(place)`, `goInside`, `goOutside`, `prompts()`, `press(key)`.
- `LEDGER.talk`: `open(id)`, `lines()`, `say(which, nth)`, `type(text)`, `answer('yes' | 'no' | 'keep')`, `leave()`.
- `LEDGER.written`: `read()`, `next()`, `choose(n)`.
- `LEDGER.job`: `read()`, `goToPickUp()`, `goToDrop()`; the drop door is `press('E')` at its prompt.
- `LEDGER.fare`: `places()`, `call()`, `accept()`, `pickUp()`, `dropOff()`. `LEDGER.cab`: `getIn()`, `driveTo(place)`, `getOut()`.
- `LEDGER.ledger`: `open(part)`, `close()`, `read()`, `rows()`, `pages()`, `key(code)`, `mark()`, `book()`, `openItems()`, `moneySums()`, `faults()`.
- `LEDGER.measures()`, `LEDGER.measuresJSON()`.
- `LEDGER.pauses()`, `LEDGER.pauseFaults()`, `LEDGER.check.arrivals(options)`, `LEDGER.check.nights(options)`.
- `LEDGER.saveText()`, `LEDGER.restore(text)`, `LEDGER.step(realSeconds)`, `LEDGER.wait(...)`.

## Tests

Headless Chrome through puppeteer-core. `test/harness.mjs` serves a folder and opens the page.

- `test/week.mjs`: one full week through the hook alone; writes `out/measures.json`.
- `test/nights.mjs`: everyone who sets off arrives or is accounted for; no pause without a resume.
- `test/layout.mjs`: the slip, the subtitles and the Ledger over a talk, at four window sizes.
- `test/files.mjs`: the files beside the page can be listed and read, the zip unpacks, the export falls back.
- `test/talk.mjs`: live talk with a stand-in for the page's Claude (working, switched off, refused, a broken rule).
- `test/oldsave.mjs`: a save written by an older build loads in this one, and its Ledger is rebuilt with a
  source event on every entry. `OLD=<folder with an older build> node test/oldsave.mjs`.
- `test/eyes.mjs`: the town's eyes setting, off and on.
