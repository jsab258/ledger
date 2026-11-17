# Review: prototype source project (tools/lane/prototype/)

Fresh reviewer, 17 Nov 2026 (machine clock 23:2x; file named as ordered). Nothing in the folder was edited.

## Verdict: PASS WITH FIXES

The build is real and the bytes are right. The smoke test passes but is too weak, the README overstates two things, and the publish map has one path fault and one version risk.

## What was checked

1. Build and tests. `python3 build.py` prints "identical to the published version". The unit tests ran 7 (6 build checks plus the smoke test), OK, 1 skipped. The build does verify bytes: it joins the two parts, takes SHA-256 of the joined script and of index.html, and stops if either differs from MANIFEST.json. Independently, dist/ledger.js and dist/index.html are byte-identical (cmp) to the copy read from the page in the scratchpad. The edited-source refusal test works.
2. Size guard. git-size-guard's own verdict() was run on every file: all of src/, build.py, tests and README pass (part-01.js 880,166 bytes, part-02.js 329,897, both under 1 MB, .js counted as non-code). dist/ is ignored by the folder's .gitignore (git check-ignore confirms); the dist files would all be refused (pictures by kind, ledger.js and people.txt over 1 MB), so the ignore matters and works. __pycache__ is ignored too.
3. Smoke test with LEDGER_PROTO_ASSETS set: passes in 46 s (headless Chromium, software graphics). But it is weak: a missing picture (404) would still pass, since only uncaught page errors are caught; reportText() is only checked to be a string, which it is even on the title screen; no week is ended. Two strengthenings were tried in a scratch script and both pass:
   - Record every response of 400 or more and every failed request for the local server; assert none (the only failure seen was Google Fonts, which the sandbox cannot reach; exclude other hosts). All 402 textured materials had loaded images.
   - Call LEDGER.endWeek("silent"), wait 3 s, assert G.story.phase is "end" and reportText() contains "Choice: silent". Also cheap: after step(120), assert at least one person's x or z changed (4 of 38 were moving).
   Note: LEDGER.endWeek() with no argument throws a TypeError inside the game (reading 'sev'); the game's own call passes "silent".
4. README. True: sizes (1.21 MB, 1.5 MB people.txt), version 1794862482-9f9b, 13 pictures, three.js r187 in the bundle, the three claude.use calls, the fonts, the Fable ask on the last line of FABLE-DRIVING-NEXT-ROUND.md. Wrong or overstated: see fixes 1 to 3. Plainness: fine for the main session; too technical for Jafar himself (checksums, bundler, hook), which is acceptable for a lane note but it should not go to his page as is.
5. Publish map. See fixes 4 and 5.

## Fixes

1. Smoke test: add the two checks above (no failed local requests; endWeek("silent") reaches "end" with "Choice: silent" in the report), plus the people-move check. Until then the README's "the end report text" is overstated: the test never ends a week.
2. README hook list: the hook also has scene, camera, THREE, ui, cam and F; list them or say "among others". Add that endWeek needs a choice ("silent", "take" or "wind").
3. README other claims: the build-test list names 5 of the 6 checks (the page-files check is missing); "three.js 0.187.0 released 30 Oct 2026" is not shown by anything in the folder (the bundle says only r187): mark the date unverified. The dates "18 Nov" in README and MANIFEST ("read": "2026-11-18") do not match the machine clock (17 Nov) or the sibling notes; correct them or say which clock is used. Stage 0 "Done" should say the smoke test runs only where a checked copy of the pictures exists. The scope draft says the build makes "one HTML file"; this makes two (index.html and ledger.js): reconcile one of them.
4. publish-files.json paths: file_path "dist/index.html" and "dist/ledger.js" are relative to the prototype folder, but the Artifact tool reads relative paths from the working directory (normally the repository root), so the publish would not find them. Write repository-relative paths (tools/lane/prototype/dist/...) or add a "root" entry the publisher passes.
5. Copying from the same page: an update keeps files it does not name, so the 13 self-copies are redundant; worse, they copy the page's current files, not version 1794862482-9f9b, so if the page changed since, the new pictures arrive unchecked with old code, and a publish from dist would also overwrite any newer code on the page. Before publishing, read the live page and stop unless its version equals MANIFEST's; either drop the self-copies or pin them with "ver"; after publishing, read the files back and check their SHA-256 against MANIFEST.
6. Durability: the pictures and people.txt now live only on the page and in a scratchpad a reboot clears. Keep a checked copy in a named F:\LedgerTools folder (CLAUDE.md: lasting inputs there) and point LEDGER_PROTO_ASSETS at it.
7. Small: rename test_page_loads_only_listed_files (it checks three names only; the textures are built by joining strings) or make it match every asset; the server log silencing in smoke_test.py does not work (setting log_message on a partial has no effect; use a subclass); close the files the tests open (ResourceWarnings).
