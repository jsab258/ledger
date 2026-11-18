# LEDGER loop prototype: source project (stage 0)

Written by the cloud lane, 18 Nov 2026, for the order's waiting item 16 ("the loop prototype as a source project in the repository: build step, tests, published to the same page"). A draft home: the main session moves the folder where PLAN.md places the prototype (the scope draft suggests prototype/ at the root) when it adopts it.

## What is here

- src/index.html and src/bundle/part-01.js, part-02.js: the published page exactly as it stood in version 1794862482-9f9b (read 18 Nov with the Artifact tool). The game script is one 1.21 MB file, over git's 1 MB limit for non-code text, so it is kept in two parts cut at line ends; the build joins them back byte for byte.
- src/MANIFEST.json: the page, its version, and a checksum for every file. The 13 pictures and the people rig (people.txt, 1.5 MB) stay on the published page and are not copied into git; a publish copies them server side from the page itself.
- build.py: joins the parts, checks every byte against the published checksums, writes dist/ (git ignores it): the page and its script (two files, not the single file the scope draft imagined; the pictures sit beside them) and dist/publish-files.json, the files map for one Artifact publish to the same page, so his link never changes. Its paths are from the repository root. It names only the script, because an update keeps the pictures it does not name; it records the page version it was built on, so the publisher reads the live page first and merges any newer change, and compares checksums after publishing. With --assets it also copies a local set of pictures in, checked, for offline play and tests.
- tests/test_build.py: 6 checks, no browser needed (rebuild identical to the published page, every source file under 1 MB, the publish map, the page names its script and people rig, an edited source refused unless allowed, the test hook present).
- tests/smoke_test.py: plays the built page in headless Chromium through the game's own test hook (window.LEDGER): every file loads, title screen, a new week, the clock moves, people move, at least 10 people, the week ended with the silent choice and the end report saying so, no page errors. Needs the pictures in a folder named by LEDGER_PROTO_ASSETS; skipped otherwise. Passed here on 18 Nov (Swiss time) with software graphics, in about 55 seconds.

Run: python build.py, then python -m unittest discover -s tests -p "*test*.py".

## What it shows

The page's script is a bundle: three.js 0.187.0 (the page's own REVISION string says 187; npm lists 0.187.0 as MIT, published 30 Oct 2026, checked with npm view on 18 Nov) and the game's code, with the game's names shortened by the bundler. So the repository can rebuild and test the page today, but nobody can read or edit its rules yet. No readable source was found in the repository or on the page (whether Fable kept one in its chat is unverified).

The game exposes a test hook, window.LEDGER: G (the whole game state), step, simStep, startNew, passTime, enterRoom, leaveRoom, endWeek, reportText, saveNow, restore, talk, rig, benchmark, and the engine's own scene, camera, THREE, ui, cam and F. endWeek needs a choice (endWeek('silent') works; with none it fails inside the game). Per-system checks can use this before any split.

## Stages from here

1. Stage 0 (this folder): rebuild and smoke test the page as published. Done.
2. Stage 1, the readable source: ask Fable for its source files as written, before bundling (added as the last line of production/lane/FABLE-DRIVING-NEXT-ROUND.md; the same ask belongs in his next prototype round). With them, src/ becomes one file per system plus three.js pinned at 0.187.0 from npm, and the build bundles with esbuild (MIT). If Fable has no source, the fallback is to unbundle by hand: split three.js out, reformat, and rename the game's code system by system, a few hours per system, checked after each step by the smoke test and the system's checks.
3. Stage 2, per-system checks in Node through the hook, in the scope draft's order (production/lane/PROTOTYPE-SCOPE-DRAFT.md: seeing and naming, gossip, the Ledger, money, police, fighting, saving first); the golden rows from tools/lane/simwasm/ where the C# Core has them.
4. Stage 3, publishing from the build: one Artifact publish of dist/index.html with dist/publish-files.json's files map to the same page, by whoever owns the page (the lane never publishes it).

## Open points for the main session

- Licence lines: three.js (MIT) and esbuild (MIT) are not on the allowlist by name; the page also loads Google Fonts (mostly OFL 1.1, which is listed; Special Elite is Apache 2.0, unverified here). MIT is listed for other tools, so likely a one-line addition, but it is his list.
- The page uses claude.use("db"), ("user") and ("sample") (save, sign-in and live talk). Outside claude.ai these are absent, so tests run with saves in the browser only and live talk off; talk checks must use its fallback lines.
- The pictures and the people rig live only on the page (and in this run's scratch copy). Keep a checked copy in F:\LedgerTools (MANIFEST.json has the checksums) so the smoke test runs on the PC and a lost page can be rebuilt.

## Per-system checks (stage 2, first four)

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
