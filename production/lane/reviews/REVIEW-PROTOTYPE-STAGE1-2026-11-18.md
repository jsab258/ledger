# Review: prototype stage 1 (18 Nov 2026, second-round source)

Verdict: PASS WITH FIXES. The source, build, lock, shim and re-pointed rows are sound. The fixes are wording in the note and the README, plus some incomplete use checks. No browser was run for this review.

## Checks run

- rules_test.py -k static: 116 passed, 12 deselected.
- test_build.py: 9 passed, including the rebuild against the published checksums. Byte for byte is confirmed.

## Answers

1. Re-pointed rows: right. All 18 rows were checked against rules.js, and each code read was checked to point at the right section. STORY is RULES.story in scenes.js, LAD is RULES.ladder in seeing.js, TALKING is RULES.talk in talk.js, KN[id] is in kinds.js, PEOPLE.x and week('x') are in cast.js. 6.06 and 6.07 are right: rules.js has Ron at 18.5 and Sheila at 14.3, and CHANGELOG section 2 names both in the lengthened lunches and errands. One small point for the record: Sheila's stop grew by 72 minutes, a little over Fable's "6 to 70". Gaps are listed below.
2. Lock: right in use. run() holds the lock and calls build(locked=True), so there is no second flock on a new handle and no deadlock. The lock file sits beside the work folder, so clearing the folder keeps it. One gap: finding 5.
3. Shim: right. The harness already ignores console errors matching "fonts.g" and "ERR_". Before this change the page also ended up on system fonts, only after a hang. So refusing fonts at once only saves time. The 180 s screenshot wait changes no assertion. Layout explanation: plausible, not verified. In ui.js, --lift is set inside hud(), which runs from the frame loop. In harness.mjs, shot() turns rendering on for 700 ms, then the screenshot is taken. 1280x720 is the first size, so it carries the first software-graphics frames. A late frame there would hold --lift past the 600 ms wait.
4. Outside-rules note: mostly right. The 375 total and the six reason counts match the 22 files listed in RESULTS.md, and match CHANGELOG. 112 rows split 85 table and 27 search, and both lists of remaining rows are exact. One error: finding 1.
5. README: plain, but finding 2 and finding 7 apply. The versions given match package.json.
6. Static checks: both pass, as above.

## Findings

1. production/lane/PROTOTYPE-OUTSIDE-RULES-2026-11-18.md: under "Not counted at all", state.js and clock.js are listed as outside the 22 rule files. They are rule files: they are in RULE_FILES in tools/numbers.mjs, with 20 and 4 numbers counted in RESULTS.md. Fix: leave only main.js, saving.js, map.js, render, audio.js and the Ledger drawing in that bullet. Add a line saying that save version 4 is one of state.js's 20 counted numbers, kept under the record's reasons and not as a rule, and that the weather list is words, so the counter never sees it.
2. tools/lane/prototype/README.md: "13 files, 4.8 MB" is wrong. PUBLISHED.json totals 4,495,951 bytes. Also, "the 13 pictures' checksums" should be 12 pictures and the people rig. Fix: "13 files, 4.5 MB" and "the 12 pictures' and the people rig's checksums".
3. tests/rules_test.py line 161: the comment "The default nerve 0.5 ... is still written in seeing.js" is now false. Fix: delete it. The module docstring's "Changed by" list also leaves out the second round, so the note's "the rows ... say so" is only half true. Fix: add two lines to the docstring. "6.06 Ron back at the rank after Tang's: was 17.9, now 18.5 (second round's retiming)." "6.07 Sheila back from the caff: was 13.1, now 14.3."
4. tests/rules_test.py: some use checks cover only half a rule. Fix by adding these:
   - 4.03: U("scenes.js", "P.mind.fear > STORY.paysUpAboveFear ||")
   - 7.05: U("talk.js", "parts.length > TALKING.replySentencesAtMost")
   - 1.21 to 1.21c: U("kinds.js", "sev: KN[id].newsworthyZeroToOne,")
   - 6.08 to 6.08c: one U per person, for example U("cast.js", "nerve: PEOPLE.ron.nerveZeroToOne,")
   - 6.06 to 6.07b: U("cast.js", "sched: week('ron')") and the same for sheila and grace
5. tools/lane/prototype/build.py work_lock: the lock file is written before prepare_work's check that the work folder is outside the repository. So --work pointed inside the repository leaves a .lock file there. Fix: first line of work_lock after abspath: `if _inside_repo(work): raise SystemExit("the work folder must be outside the repository: " + work)`.
6. tests/rules_test.py: the helpers sched(), traits() and kind_row() are no longer called. Fix: remove them.
7. README licence line: prettier, eslint and puppeteer-core have no versions. Fix: prettier 3.3.3, eslint 8.57.0, puppeteer-core 25.17.0, as in package.json. Also add to the shim sentence: "set LEDGER_ALLOW_FONTS=1 when using the shim on the PC". Without it, layout is measured with fallback fonts there too.

## Unverified

The browser results: same_week digest, oldsave, arrivals alone, layout at 3 of 4 sizes, and eyes. A side note, outside the lane's scope: Fable's CHANGELOG says "59 of the 157 walks" and then "all 145 walks now fit". The lane's note does not repeat either number.

Fixes applied by the lane, 18 Nov 12:43: findings 1 to 7 all applied (note's state.js and clock.js bullet; README sizes, pictures, licence versions, LEDGER_ALLOW_FONTS; stale comment and second-round list in rules_test.py; code-read checks for 4.03, 7.05, 1.21, 6.08, 6.06, 6.07; lock refuses a work folder inside the repository before writing; unused helpers removed). Static 116 pass, test_build 9 pass; systems_test and rules_test with the browser 141 pass, 1 skipped.
