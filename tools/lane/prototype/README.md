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
