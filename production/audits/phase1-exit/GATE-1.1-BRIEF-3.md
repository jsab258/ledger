# Item 1.1's gate, third review: what a fresh reviewer is given

For a reviewer who has not seen the work. It names the requirement, the bar, what the second review failed and where the outputs are; it carries no verdict of the maker's.

## The requirement (PLAN.md, phase 1)

"First proof, Mickey's front office: the room Tom walks into, from the room kit, researched first; real glass reflecting the street; a 1990 cab office's wear and clutter, radio set, ashtrays, kettle, telephone, scuffed counter; no glitches. With it one frontage of correct geometry, material and wear, its window of verified CC0 goods, and three fixed street views."

## The bar (CLAUDE.md, "the gate")

Visuals against the Hook sheet (production/reference/hook-sheet.png) and the two KCD2 frames (F:/LedgerTools/reference-other-games/production/reference/kcd2-town-fountain.jpg and kcd2-town-arcades.jpg; never in the repository); no visible fault or placeholder; a yes only for work that would pass in a 2026 game. A step passes when it fails only on narrow points later steps deal with. Judge the pictures themselves at full size; a report's words (the AI tester's included) are not evidence of what a picture shows.

## What the second review failed (GATE-1.1-REVIEW-2.md), in its order

1. The street in the glass: stair-stepped cut-outs by day, a white sawtooth in Rita's glass, a stepped halo at night.
2. The office lit in the normal game behind its shut door.
3. The packaged crowd in white base layers, barefoot; a passer-by blocking Mickey's window.
4. A flat black block and a black gable behind the west row in the hook view; the hill's box houses.
5. The reverse view: the Tea Room's and Ironmonger's windows opaque mustard panes; dark seams down the slate roofs.
6. Wear barely showing on Rita's front and Mickey's counter.
7. Indoors the camera pinned against the side wall.
8. Narrow points (the gilt number on a passer-by's back, the floating prompt, cut subtitles, the back doorway, binders, rings at night, brass, Rita's hair, Tom's tracksuit).

## What was done, so the reviewer knows where to look (not a verdict)

- 1: the window captures lit by Lumen, people left out, one window at a time. Anti-aliasing inside the captures was tried and set aside (it darkened the caught street to a third: production/research/shop-glass-reflections/CLOSE-RANGE-ROUTES-2026-10-07.md); the maker knows the reflected roofline still steps at two metres.
- 2: the office dark until Tom has the key (shop-interiors.json lit_at_start).
- 3: Sheila (in the locked office by her day) waits beside Mickey's door, and whoever waits at the cab rank stands at the door, not in front of the window (hook-cast.json body_x_m). The base layer stays: plain clothes are a failed capability for now, reported to Jafar (production/audits/clothing/RON-OUTFIT-REVIEW-3.md; his ruling of 4 October keeps the base layer meanwhile).
- 4: the houses past the bend given sides and gables (tools/art-recipes/terrace-front.py _kit_house_sides). The hill is phase 2's (PLAN.md).
- 5: the west shops show their own rooms; each row's slates one piece.
- 6: the maker found the shopfront marks never showed (projected marks do not land on paint, a rule of 3 October against streaked "marble"); two tries tonight, set aside, research next. The maker knows the fronts read clean.
- 7: the office camera walked is P15, phase 2's exit (PLAN.md).
- 8, two narrow points: Enter now shows the rest of a long line before moving on; a person's talk prompt needs them in sight.

## The outputs

(Filled in when tonight's package exists: its commit, the package's shop photographs, the morning's three views, the AI tester's walk-in.)

## What the reviewer returns

PASS, or FAIL with every fault worst first, each tied to the picture it is seen in, each marked narrow or not; which of the second review's eight points are answered and which are not.
