# Phase 1's exit: the requirements and where the outputs are (for a fresh reviewer)

PLAN.md, phase 1, "Prove the bottlenecks": "Every exit bundle names the commit and package, raw logs, fixed-camera images, a walking recording and the failures. A fresh model gets the requirements and outputs, never the maker's verdict, and verifies the exit." This bundle names each requirement and its outputs as they stand; it carries no verdict of the maker's. Being filled as phase 1 runs (started 6 October).

| # | Requirement (PLAN.md, phase 1) | Outputs to check | State |
|---|---|---|---|
| 1 | Mickey's front office: the room Tom walks into, from the room kit, researched first; real glass reflecting the street; a 1990 cab office's wear and clutter, radio set, ashtrays, kettle, telephone, scuffed counter; no glitches | tools/art-recipes/shop-room.py (mickeys), production/specs/mickeys-office.json (real_room), production/art/mickeys-props/README.md (sets 1 and 2, sources and measurements), production/previews/mickeys-props-desk-2026-10-06.jpg, mickeys-props-furniture-2026-10-06.jpg, mickeys-room-furniture-day-2026-10-06.jpg, mickeys-room-furniture-night-2026-10-06.jpg; tools/street_wear.py room_wear; research: production/research/shop-window-interiors/MICKEYS-OTHER-DIRECTION-2026-10-04.md, cab-office-interior-1990 | furnished; walk-in test and recording to come |
| 2 | One frontage of correct geometry, material and wear, its window of verified CC0 goods | production/art/shop-rooms/pawnbroker-goods-sources.md (tools/art-recipes/verify_display_sources.py); the shopfront kit (to come) | goods verified; frontage to come |
| 3 | Three fixed street views | to come | |
| 4 | One complete Tom and one speaker walking, sitting and turning | tools/ue/make_cast_metahumans.py (Tom's takes A1 to A5); clips to come | candidates written |
| 5 | P2, the voice: two measured approaches at most, timed beside checked talk | production/research/voice-off-card/NOTE.md, RESULTS-2026-10-06.md; tools/voice-live/off_card.py, off_card_bench.py | FAILED on its delay line (3.36 s and 4.18 s against 1.0 s); the money ruling on his overview |
| 6 | P1 completed packaged: day, night, walking, Windows memory, sustained speech | to come | |
| 7 | Exit: the samples meet the bar; the render and voice pairing has measured headroom; median first meaningful speech two seconds or less (else state-grounded prepared opening beats are tested) | to come | |

## Failures, as they happen

- P2 (6 October): neither processor route brings the voice's share near 1.0 s, beside the game or off it; both pass the frame lines. Reported to him as P2's clause asks (FOR-JAFAR.md, Needs you).
