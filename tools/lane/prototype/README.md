# LEDGER loop prototype: source project (stage 1)

Written by the cloud lane, 18 Nov 2026. Stage 0 (the published bundle, rebuilt and smoke-tested) is replaced by stage 1: Fable's readable source, built here byte for byte. A draft home: the main session moves the folder where PLAN.md places the prototype when it adopts it.

## What is here

- project/: Fable's source as published beside the page under source/ (his second round of 18 Nov, page version 1794997640-def7), with his BUILD.md, CHANGELOG.md, DESIGN_NOTES.md, NOT_DONE.md, README.md and RESULTS.md from the page's top level. From 18 Nov 16:15 (his decision of 15:23) the lane builds the prototype itself: round 1 (the eight fixes) is the lane's own edit, listed in project/CHANGELOG.md; pin_build.py records each new build in PUBLISHED.json for the byte-for-byte check.
- published/: the page's files.json, measures.json and results/ (Fable's check results), for reference.
- PUBLISHED.json: the page, its version, the checksums the build must reproduce (ledger.js 17830684..., index.html f0e85bbb...), the checksums of the 12 pictures and the people rig, and the first round's pin under "previous".
- build.py: runs Fable's own build (npm ci --ignore-scripts, then node tools/build.mjs: esbuild 0.28.2 bundling three.js 0.187.0) in a work folder outside the repository and checks ledger.js and index.html byte for byte against PUBLISHED.json. A lock beside the work folder keeps two builds, or a build and a test run, from sharing it (a parallel build lost a log on the first try). With --assets DIR it copies the pictures in, checked.
- run_proto_tests.py: Fable's own tests, unchanged, in his npm test order (numbers, walks, same week, week, publish set, arrivals, nights, town, ledger rules, layout, files, talk, eyes) plus oldsave when OLD names an older build. They run in the cloud's Playwright Chromium through shim/puppeteer-core, a stand-in for the calls the tests use. The shim refuses Google Fonts requests at once (the cloud cannot reach them; each page load had waited about 90 s) and gives screenshots Puppeteer's 180 s instead of Playwright's 30 s. On the PC, set LEDGER_ALLOW_FONTS=1 when using the shim, or layout is measured with fallback fonts there too.
- reviewers/: the simulated Steam panel (task 4m): eight player cards, the packet made from a playtest, the prompt, and the theme scorer.
- tests/: the lane's own checks (rules, systems, Ron stopping, smoke, build), reading the readable source and LEDGER.rules.

The pictures and the people rig (13 files, 4.5 MB; people.txt is 1.5 MB, over the size guard) are not in git. Fetch them from the page (Artifact tool: action read, the page url, paths = the asset names, out_dir outside the repository) and check them with python build.py --check-assets DIR.

Run: python build.py; python -m pytest tests (set LEDGER_PROTO_ASSETS for the live checks); python run_proto_tests.py --assets DIR.

## Results here, 18 Nov 12:20 to 12:50 (second round's source)

- Build: ledger.js and index.html byte for byte the published ones (a second machine, after Fable's own). The first round's source, from git, also rebuilds its own published ledger.js (73245b8e...).
- Fable's tests: numbers, walks, same week (the seeded week gives his recorded save, digest 6e859584cd20ea3d7ab0, 19 parts, so the seeded week is the same on this machine too), week, publish set, arrivals, nights, town, ledger rules, files, talk and oldsave (a first-round save loads in the second-round build) pass; eyes prints its findings with no error. layout passes at three of four sizes; at 1280 by 720 the subtitles had not yet moved up 600 ms after the slip unfolded, right after a slow software-graphics screenshot. Without the screenshot, or with 4 s to settle, it passes: a timing effect of the cloud's graphics, not a layout fault (a slow machine would show the overlap for a moment). arrivals' first run crashed the browser tab while a second browser ran beside it; alone it passes.
- The lane's checks: see the sections below; numbers in production/lane/LANE-LOG.md.

## Licences for the builder

three.js 0.187.0 (MIT), esbuild 0.28.2 (MIT), acorn 8.19.0 (MIT, Fable's numbers tool only), prettier 3.3.3 and eslint 8.57.0 (MIT, formatting only), puppeteer-core 25.17.0 (Apache 2.0, Fable's tests only; not used here) are not on the allowlist by name. MIT is listed for other tools; the lines are his list's to add. The page also loads Google Fonts (mostly OFL 1.1, listed; Special Elite is Apache 2.0, unverified here). The art: Quaternius figures and Poly Haven textures, both CC0 by Fable's BUILD.md.

## Open points for the main session

- The page uses claude.use("db"), ("user"), ("sample") and ("downloads"). Outside claude.ai these are absent, so tests run with saves in the browser only and live talk through Fable's stand-in.
- Keep a checked copy of the pictures in F:\LedgerTools (PUBLISHED.json has the checksums) so the checks run on the PC and a lost page can be rebuilt.
- Fable's NOT_DONE.md item 1 needs a decision if the real game takes the routines over: walks fit only with Tom away or at the rank.

## Per-system checks (stage 2, first four)

The sections below were written for the bundle and re-pointed at the readable source on 18 Nov; their counts are the first run's. Fable's first round fixed the two findings kept as expected failures (restore through the hook, Ron stopping by the rank); they are now ordinary passing tests.

tests/systems_test.py, added 18 Nov 2026. It plays one new week in headless Chromium through the game's test hook only, with the clock stopped between steps, in about 40 seconds. Needs LEDGER_PROTO_ASSETS like the smoke test; skipped otherwise.

Seeing and naming:
- Wearing the coat on the street by day makes one sighting event, with the people who saw it as witnesses; each has a memory of it, and Sheila, indoors, has none.
- One event per sighting kind per two-hour block, however many people see it.
- Without the coat, no new coat sighting.
- The three on the rank start calling him more than "the new owner" once they have seen his face, and link the stranger off the bus to him; Brenda, who saw nothing, does not; the street's own name climbs once most of it knows his face (a threshold check only: how well everyone knows his face is set by hand).

The Ledger:
- The report's Known, Ledger right and missed counts match a count made separately from the minds and the Ledger.
- The Ledger never says someone saw an act unless that person is a witness of it.
- The same counts hold for a case counted by hand: the three on the rank saw both the bus and the coat and Tom saw them looking, so at least 6 known and 6 right.
- Gossip told behind his back adds one to Known and one to missed, and the report lists the person under "told" but not under what he believes. The told memory is planted by hand, not spread by the game's own gossip.

Money and the tin:
- A fare goes in the pocket, never the tin (the cab and passenger are placed at the drop by hand, so only the payment is tested), and raises the fare count, clean earnings and what the book can hide; the report's pocket matches.
- The report shows the tin apart from the pocket.
- Mickey's book starts with the five debts; an open debt can be demanded, a paid one cannot.

Saving and restore:
- With no claude.use (outside claude.ai) saving falls back to the browser; the save matches the live state, and restoring it brings back time, money, debts, events, the Ledger, the log and memories.
- A save of another version is refused and changes nothing.

Could not be checked, and why:
- Dirty money: the tin fills only at a night job's drop door (a key prompt) or when a debt is collected in talk or a fight, and washing goes through Sheila's talk. Not reachable through the hook; marked skipped.
- Taking a fare, picking up and driving are key presses; the check lets the radio offer the fare, then places the cab and passenger at the drop by hand, so only the payment is tested. It finds the fare places in the built script by the shape of their data; if a rebuild changes that, the check fails saying so.
- Finding: restoring through the hook leaves every person holding their old memory, not the restored one (the game's own Continue rebuilds the people; the hook does not). Kept as an expected failure, so a fix will show.

## Per-system checks (stage 2, second round)

tests/systems2_test.py, added 18 Nov 2026. Same set-up as the first round (headless Chromium, the hook only, the clock stopped between steps, LEDGER_PROTO_ASSETS needed). 15 tests: 11 pass, 3 skipped, 1 expected failure, in about 38 seconds. Its header lists what the hook exposes for each system.

- Gossip: the bus arrival reaches new people within five game hours; nobody forgets; every told memory has a recorded telling from someone who knew the story; no "saw" memory without being a witness.
- Talk: suggested lines (three at most) name nobody Tom has not learned; before Mickey's book is read, no line to a debtor speaks of a debt. Each talk is closed with its own Leave button, because the clock stops while talk is open. Sheila is left out: talking to her opens her written first scene.
- Police: crimes planted by hand on Monday evening (Tom's acts are key presses), then the game's own police run at 04:00: the witness who saw it makes a statement and the police are sent; nobody for an unseen crime, a told-only one, an afraid witness or a paid one.
- Routines: at 02:00, 09:15 and 12:30 on Tuesday every named person not sent elsewhere by the story is headed for their schedule's place (the rule written again in the test from its meaning).
- Debts: the five debts open; Julie's debt is not in the Ledger before the book is read, which matches the design (the scope draft's Ledger check, "never shows a fact he could not know"; the prototype's own note that debts are listed "by the names in Mickey's book").
- Skipped, not reachable: paying or striking out a debt, Sheila's book scene, and jobs (all written scenes or talk decisions that wait on key presses).
- Finding, kept as an expected failure: Ron sets off home at 23:36 and stops about 3 metres from the rank, still marked as walking, until at least 03:00.
- Not a test, noted: on Tuesday night the game paused and did not resume within a minute (Monday night's forced bedtime at about 04:30 resumes after its fade). Cause not found; so only the first night is stepped through.

## Rule checks (catching a changed number)

tests/rules_test.py, added 18 Nov 2026, run with pytest (python -m pytest tests/rules_test.py; the unittest command above does not run it). It guards the rules in production/lane/PROTOTYPE-RULES-READ-2026-11-18.md, by that file's rule ids, so a Fable round that changes a rule's number names the rule that moved.

- Static, no browser: one table of 112 rows (rule id, plain name with its number, the piece of the bundle holding it, how often it occurs). A row fails when its piece is gone or occurs a different number of times. Rules with no number, absences (no wages, no hop limit) and rules read from the design notes only are left out, listed in the file.
- Most rows search by the bundler's shortened names and carry the bundle_names mark (tests/conftest.py names it). When Fable's readable source replaces the bundle, the table is to be re-pointed at it, same ids; until then a rebuild that renames things fails those rows without any rule changing. pytest -m "not bundle_names" runs only the rest.
- Live, through the hook (needs LEDGER_PROTO_ASSETS, skipped otherwise, also skipped if Chromium cannot start): the week starts Monday 15:36; 45 real seconds of step are one game hour; 23.50 clean to start; Mickey's five debts and amounts; Ron's schedule; Sheila's, Darren's and Ron's traits; the ten who never make a statement; save version 4 in the browser; heat on a planted memory fades by e^(-minutes/1700); the hook's arrest (assaulting an officer, so counted as running) holds him 7 hours and bills 40.00 from clean, the rest owed to Agar. The 4-hour, 25.00 arrest needs the constable's talk choice, a key press, so only the static row holds it.
- Two readings in the rules file were found wrong and corrected there (18 Nov): 28 named people, not 31 (the bundle's 30 schedules include the fare passenger and the yard lad), and 51 kinds of act, not 45; the tests assert the corrected numbers.
- After the correction: 126 tests (115 static, 11 live), all pass, about 37 seconds with the pictures; without them the 12 live checks skip and the static ones take under a second.
