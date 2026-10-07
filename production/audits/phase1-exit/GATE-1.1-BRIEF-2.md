# Item 1.1's gate, second review: what a fresh reviewer is given

For a reviewer who has not seen the work. It names the requirement, the bar, what the first review failed and where the outputs are; it carries no verdict of the maker's.

## The requirement (PLAN.md, phase 1)

"First proof, Mickey's front office: the room Tom walks into, from the room kit, researched first; real glass reflecting the street; a 1990 cab office's wear and clutter, radio set, ashtrays, kettle, telephone, scuffed counter; no glitches. With it one frontage of correct geometry, material and wear, its window of verified CC0 goods, and three fixed street views."

## The bar (CLAUDE.md, "the gate")

Visuals against the Hook sheet (production/reference/hook-sheet.png) and the two KCD2 frames (F:/LedgerTools/reference-other-games/production/reference/kcd2-town-fountain.jpg and kcd2-town-arcades.jpg; never in the repository); no visible fault or placeholder; a yes only for work that would pass in a 2026 game. A step passes when it fails only on narrow points later steps deal with. Judge the pictures themselves at full size; a report's words (the AI tester's included) are not evidence of what a picture shows.

## What the first review failed (GATE-1.1-REVIEW-1.md)

1. The world's edge past the street's south end from Mickey's pavement; the reverse view ending in blockout boxes under outsized trees.
2. Window glass by day with almost no street reflection, torn shapes where any; the gilt number from inside a thick black slab with a sawtooth edge; no reflection at night.
3. The packaged walk-in with the shop door missing; Tom walking through an open, lit doorway into an office "locked since Mickey died".
4. No visible wear on Rita's front or in the office.
5. No ashtray that reads; no district map; the window reveal in a black pitted scan material.
6. Kiosk, pillar box and the hill's houses and trees (argued as phase 2's, PLAN.md phase 2).
7. Narrow points.

## What was done, so the reviewer knows where to look (not a verdict)

- Glass: the street captured per shop window and shown in the pane at the Fresnel angle (unreal-look.json glass_cube_*).
- The south end: a scripted quay to the adopted atlas (production/art/south-quay/README.md); the sky photograph turned and held above its own land (sky_dome_yaw_deg, sky_horizon_clamp_deg).
- The door: shut, the office dark, until Tom comes with the key; the leaf then stands open and the lights come on as he enters.
- Wear: decals by rule (production/specs/street-wear.json), Rita's front and the office counter.
- The ashtray, the map, the reveal's lining, the lettering flat on the glass. The "black pitted reveal" was the lamp column outside Mickey's under a scanned metal map; dark steel is flat paint now.
- His order of 7 October, before this review: Mickey's top pane's ragged white strip (the room's bare ceiling tube seen through it, burnt out) and the rough black post (the lamp column close in front of the office's camera). The tubes are under opal diffusers now (tools/art-recipes/shop-room.py); the office's camera stands at x 6.9 m, off the lamp column (production/specs/vignette-scene.json).

## The outputs

- Mickey's office through its window, by day and at night: ue-probe/ue-vign_mickeys_day.png, ue-vign_mickeys_night.png (2560 x 1440).
- The three fixed street views: ue-probe/ue-vign_hook_day.png, ue-vign_reverse_day.png, ue-vign_hook_night.png.
- In the packaged game (the build machine's copy of the commit named in BUNDLE.md): the AI tester's walk-in, its step pictures and filmed frames (folder named in BUNDLE.md); the game's own shop photographs, Saved/PageShots of the packaged copy (Rita's and Mickey's fronts by day and night).
- How each was made: production/art/mickeys-props/README.md, production/art/shopfront-kit/README.md, production/art/south-quay/README.md, production/research/south-quay/METHOD-2026-10-06.md, production/research/shop-glass-reflections/NOTE.md.

## What the reviewer returns

PASS, or FAIL with every fault worst first, each tied to the picture it is seen in; which of the first review's seven points are answered and which are not.

## This round's outputs (7 October, 14:45)

- The commit and package: 67c51f5, packaged by the build machine (its own result commit after it); the played copy F:/LedgerTools/played-game is that package.
- The office through its window, by day and at night, and the three street views: ue-probe/ue-vign_mickeys_day.png, ue-vign_mickeys_night.png, ue-vign_hook_day.png, ue-vign_reverse_day.png, ue-vign_hook_night.png (2560 x 1440, filmed 14:21 in the editor's game mode from the same source; the office camera at x 6.9).
- The walk-in in the packaged game (-MickeysInside), played by the AI tester: production/playtest/ai-tester/2026-10-07-1444 (24 step pictures and report.md) and its filmed walk, F:/LedgerTools/tmp/ai-tester/film/2026-10-07-1444/walk.gif (44 frames).
- The game's own shop photographs from the package: F:/LedgerTools/played-game/Windows/LedgerProbe/Saved/PageShots (Rita's and Mickey's fronts, by day and at night, the newest files).
- Faults the maker knows of and names (not a verdict): the street caught in Mickey's glass by day draws the roofline across the road as large stair steps (three tries failed, set aside: production/research/shop-glass-reflections/CAPTURE-STEPS-2026-10-07.md); the office is built only when the game is started with -MickeysInside, and without it stands lit behind a shut door.

