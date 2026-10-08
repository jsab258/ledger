# The windows' second try: three views, one fresh reviewer each (8 October)

The second try (GATE-HOOK-1.md, its end): the rest of the street with Mickey's row; each house its own kind; the piece's glass out and a net card in each sash's pane; the houses' ground floors too.

| View | Against the last good (the sky's second try) | New faults from the change |
|---|---|---|
| Hook, day | Mickey's row (the right row) closer to the photographs and the Hook sheet: tall, low sills, set back, a kind per house, something different behind each | the near-left terrace's ground-floor sashes: lower sashes as flat white boards, the next house's windows white slits; a hard ochre stripe down the end house's upper blind; a pale blotch on one blind |
| Reverse, day | mixed, further on balance: proportions closer, but most panes white slabs and the left row's far windows vanished into their reveals | the far windows read as empty or bricked-up openings at this low angle; glass not reading as glass (white panels); the cottage roof darker with a soft band (cause not found) |
| Hook, night | the same: pools, darkness and the number of lit windows unchanged, the windows sitting better in the walls | windows lit in one sash only (each pane's card lit on its own) |

## The step

**Mickey's row: kept. The rest of the street: not passed in two tries, back to its box sashes.** His order: Mickey's row first, the rest of the street only if Mickey's row passes. Mickey's row passed its fresh review against the photographs on narrow points (REVIEW-PHOTOGRAPHS.md) and reads closer in both day views; the rest of the street's windows, deep-set at the street's low angles, read as boards, slabs and slits, a new fault in each day view. Kept with Mickey's row: its kinds, its panes' net cards, lit by the window not the pane (the night's fault), and the glazing bar the photographs measured (22.2 mm, the second amendment by a fresh helper; checks/check_v2.json, passing).

Seen in the earlier pictures too, added to the known list: the nets a square grid, not lace; the nets' horizontal ribs read as venetian blinds; the cream house's panes the wall's colour.

## After: why the deep sashes read as boards and slits (research, 10:45)

production/research/aaa-street/WINDOWS-GRAZING-2026-10-08.md: the reverse view's left row is Mickey's row (vignette-scene.json:822), so its far windows' slits and bricked-up look stay in the state kept. The geometry is right: below about 10° from the wall only the box's lining and track show, below about 8° only the brick return, as photograph 9 shows at 17° and below. What the photographs have and ours lacks is shade inside the box (lining about 220-250, inside corner 105-125, track 150-180 in photograph 9; ours a flat 153-180): no baked occlusion in the kit and no ambient occlusion input in M_LedgerSurface. Narrow and explained, on the known list; the next direction, about a day: occlusion baked into the kit's vertex colour and wired to the material's ambient occlusion, which Lumen applies to sky and bounce light.
