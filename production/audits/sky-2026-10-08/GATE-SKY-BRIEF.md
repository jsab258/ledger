# The sky's gate, 8 October: one view per reviewer

Jafar's order of 8 October, step 2: the street lit by the sky it shows, the compensations made for the dark light removed, checked against the Hook sheet, then the gate (CLAUDE.md "The gate") on the hook, reverse and night views, one fresh reviewer per view, each beside its last good picture. Two tries; if still worse than the morning, back to the tag before-sky-2026-10-08.

## What changed (where to look, not a verdict)

- The sky light equals the dome seen (production/specs/unreal-look.json sky_light_gain 0.58 -> 1.4286, so its intensity is 1.0 at the day's sky 0.7); the lab read the engine's code: the street had been lit by 41% of the sky on screen.
- The compensations removed: the brick's gains 2.74/2.81/2.58 -> 1.0/1.03/0.94, the grey brick's 3.13 -> 1.14, the painted joinery's 1.2 -> 1.0; the pavement's 0.6 -> 0.42 (it rose with the light and was measured above the sheet).
- At night the sky light is as it was; the night camera one stop brighter (night_exposure_bias -1 -> 0), since the brick lost its boost under the lamps too.
- The pictures are the editor's, both sides, the same build; only the look file differs.

## Measured against the Hook sheet (scratchpad sky_regions.py; share of the sky's luminance)

| Region | Sheet | Before | After |
|---|---|---|---|
| Near lit brick | 6.2% | 9.7% | 11.0% |
| Far side's walls | 13.6% | 3.4% | 6.7% |
| Road | 40.7% | 22.2% | 43.4% |
| Near pavement | 9.8% | 4.4% | 9.4% |

## The views

| | View | New | Last good | Known shortfalls (item 1.1's third review) |
|---|---|---|---|---|
| S1 | Hook view, day | F:/LedgerTools/gate/new/sky/2026-10-08/hook-day.png | F:/LedgerTools/gate/last-good/sky/hook-day.png | the cast's white base layer; the doormat mid-pavement before Mickey's tiles; a low-poly satellite dish; a glittery kick plate; the hill's blobby trees and houses; the left terrace's narrow doors; no parked cars; the shop glass's stepped reflections |
| S2 | Reverse view, day | .../new/sky/2026-10-08/reverse-day.png | .../last-good/sky/reverse-day.png | the base layer; curved streaks across the slates; a bare white sky at the street's end |
| S3 | Hook view, night | .../new/sky/2026-10-08/hook-night.png | .../last-good/sky/hook-night.png | the base layer; the glass's steps; the bare sky at the street's end (no cloud, no town glow); the Fresh Fish window's stock; the hill's flat trees |

The bar: production/reference/hook-sheet.png; the KCD2 frames F:/LedgerTools/reference-other-games/production/reference/kcd2-town-fountain.jpg and kcd2-town-arcades.jpg (never in the repository).
