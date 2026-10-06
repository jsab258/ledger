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

## The outputs

- Mickey's office through its window, by day and at night: ue-probe/ue-vign_mickeys_day.png, ue-vign_mickeys_night.png (2560 x 1440).
- The three fixed street views: ue-probe/ue-vign_hook_day.png, ue-vign_reverse_day.png, ue-vign_hook_night.png.
- In the packaged game (the build machine's copy of the commit named in BUNDLE.md): the AI tester's walk-in, its step pictures and filmed frames (folder named in BUNDLE.md); the game's own shop photographs, Saved/PageShots of the packaged copy (Rita's and Mickey's fronts by day and night).
- How each was made: production/art/mickeys-props/README.md, production/art/shopfront-kit/README.md, production/art/south-quay/README.md, production/research/south-quay/METHOD-2026-10-06.md, production/research/shop-glass-reflections/NOTE.md.

## What the reviewer returns

PASS, or FAIL with every fault worst first, each tied to the picture it is seen in; which of the first review's seven points are answered and which are not.
