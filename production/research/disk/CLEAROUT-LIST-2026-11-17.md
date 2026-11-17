# Clear-out list, F:/LedgerTools (17 Nov 2026) - LIST ONLY, nothing deleted

- May go from gate: about 7.7 GB (7930 MB), 32 lines.
- Stays: about 5.9 GB.
- GameAnimationSample (5.6 GB): nothing reads it at build, cook, game or script level. It is cited only in research notes (see part 2). May go, with one caution: it is a Fab download that needs Jafar signed in to get back.

## Method
Names checked by grep (path text) in DECISIONS.md, HANDOVER.md, FINDINGS.md, NOW.md, production/approvals, production/specs, production/handover, tools and .github, plus open items in needs-you/items.json (none open names gate; all 38 items are done). retention.json protects gate wholesale, so the delete needs his yes (the clear-out yes of 17 Nov). 'Unreferenced' means no path text found; a picture shown inside an answered page was not traced pixel by pixel (the answers store holds its own copies under production/approvals). Approvals tool: 21 current, 5 lapsed, none names a gate folder. Sizes from du, MB, 17 Nov 08:30.

## Part 1: may go (full paths under F:/LedgerTools/gate/)
- new/dress-cast-2026-11-07 - 3002 MB - 7 Nov dress-cast review frames; no approval, decision, handover, tool or open item names it. Holds dress_film.ps1 and import logs (scripts there are regenerable from tools/; check before delete)
- new/knit-2026-11-08 - 1616 MB - 8 Nov knit review; unreferenced anywhere
- new/dress-cast-2026-11-08 - 789 MB - 8 Nov dress-cast review; unreferenced
- new/hair-test-2026-11-08 - 543 MB - cited only in the answered morning batch of 9 Nov (cards vs strands, decided); superseded by hair rounds
- new/brick-tones - 170 MB - unreferenced brick tone tests; brick since redone by n16-4 method
- new/corner-9d-2026-11-05 - 209 MB - corner review 5 Nov; unreferenced; superseded by later corner frames
- new/side-walk-2026-11-08 - 170 MB - unreferenced
- new/hair-near-2026-11-07 - 158 MB - unreferenced hair closeups, superseded by 8 Nov and later hair rounds
- new/hill-third-2026-11-05 - 140 MB - unreferenced hill review
- new/hill-2026-11-04 - 135 MB - unreferenced hill review
- new/corner-packaged-2026-11-06 - 111 MB - unreferenced
- new/hair-cards-vs-strands-2026-11-06 - 106 MB - decided (strands kept); frames unreferenced by path
- new/front-edge-wear-2026-11-07 - 82 MB - unreferenced
- new/corner-end-2026-11-06 - 70 MB - unreferenced; 7 Nov end frames are kept as answered
- new/corner-9b-2026-11-05 - 61 MB - unreferenced
- new/sky-2026-11-05 - 54 MB - unreferenced
- new/sky-2026-11-04 - 51 MB - unreferenced
- new/window-break-2026-11-06 - 50 MB - unreferenced
- new/timber-tcwear-2026-11-11 - 49 MB - unreferenced (tool comment may cite wear; none by path)
- new/corner-packaged-2026-11-08 - 45 MB - unreferenced
- new/corner-packaged-2026-11-05 - 44 MB - unreferenced
- new/wall-macro - 36 MB - unreferenced
- new/corner-gilt-2026-11-05 - 30 MB - unreferenced
- new/woodbox-2026-11-12 - 28 MB - unreferenced
- new/corner-people-2026-11-05 - 27 MB - unreferenced
- new/iron-cover-2026-11-08 - 27 MB - unreferenced
- new/tom-walk-film-2026-11-05 - 27 MB - unreferenced; later tom films exist
- new/corner-9a - 26 MB - unreferenced (with corner-9a-day-run.txt, -night-run.txt, 0 MB)
- new/sit-packaged-2026-11-06 - 10 MB - unreferenced
- new/(small, under 2 MB each: card-memory-2026-11-07, sit-drop-2026-11-05, tester-round-2026-11-07, quay-end-stop-2026-11-07, speaker-sit-2026-11-08, office-wall-2026-11-08, hair-colour-2026-11-07, speech-run-e-review.json, study-17-review.json, faster-builds-review.json) - 2 MB - unreferenced
- page-frames-2026-10-22 - 37 MB - 22 Oct page frames; unreferenced
- quay-street-before-hill.glb - 25 MB - unreferenced single file

## Part 1: stays
- new/launderette-n16-5-2026-11-17 - 83 MB - made today; DECISIONS cites
- new/grocer-, ironmonger-, newsagent-, chandler-, s1-street-level- n16-5-2026-11-17 and n16-5-fronts-2026-11-17 - 171 MB - made today
- new/brick-flemish-2026-11-11 - 503 MB - handover, DECISIONS and tools/flemish_tile.py cite its review
- new/brick-flemish-n16-4, brick-photo-n16-4, crate-test-2026-11-12, leak-scan-2026-11-12 - 141 MB - DECISIONS / ps5-corner.json cite; 16 Nov
- new/tom-films-2026-11-11, -b, tom-outfit, tom-surfaces-2026-11-11, tom-whole-2026-11-09, office-exit-2026-11-09 - 960 MB - DECISIONS cite; tom-outfit also named by md-bridge tools
- new/chandler-joinery, chandler-wear, street-level-2026-11-05 - 1013 MB - read by tools/chandler_joinery_check.py, street_wear.py and shop-front spec
- new/office - 1074 MB - handover, FINDINGS and approvals cite; may be thinned later by hand
- new/look - 608 MB - 57 approval files cite
- new/corner, corner-end-2026-11-07, corner-midweek-2026-11-04, night-2026-11-04, pale-line, sit, jacket, camera, calibration, tom-jacket, office-sit-default-2026-11-07 (and the review/run text files) - 540 MB - answers items, approvals, NOW/FINDINGS or specs cite
- last-good - 620 MB - standing rule: whole set stays
- before, prev, work - 312 MB - handover/DECISIONS/approvals/retention cite
- page-check-2026-10-22 - 64 MB - cited by production/approvals/2026-10-22-ritas/CHECK.md

## Part 2: GameAnimationSample (F:/LedgerTools/GameAnimationSample, 5,592 MB, last touched 24 Oct)
- Game project (ue-probe/LedgerProbe.uproject), Config, Content: no mention. Only a texture named T_GameAnimationSample_Logo appears in memory notes (a template asset that came from an old level, 18 MB, 'free to take' per COOKING-PLAN).
- tools/, .github/, production/specs, F:/LedgerTools *.py *.ps1 *.json *.ini, stage_game_data.py, packaging workflow: no mention.
- Mentioned in: production/research/sit-and-turn/TOM-MOTION-MATCHING-2026-10-22.md and SPOTS-2026-10-28.md (read from it as a study source: Epic's animation blueprint exported to text, allowed by his 13 Oct ruling), disk/F-USAGE-2026-11-16.md, frame-headroom notes. Study findings are recorded in those notes; the sample is only needed to look again.
- Not protected in retention.json. Losing it costs a re-download from Fab (his sign-in).

## Uncertain
- Folders marked 'unreferenced' were searched by path only. hair-test-2026-11-08 and hair-cards-vs-strands-2026-11-06 fed an answered page; dress-cast-2026-11-07 holds scripts/logs (dress_film.ps1, import logs).
- The gate rule says pictures behind current approvals stay: none found, but approvals store their own copies, not gate paths.
- The 'may go' sums are the safe set; the Part 1 'stays' list is the cautious reading and could be thinned later.
