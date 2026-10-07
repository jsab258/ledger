# Lab test 2: one sash window from measured numbers

Started 7 October 2026. The method on trial: write the target as numbers from real sources, build in Blender, compare the build's outlines and dimensions with the target automatically, repeat until it passes; only then a fresh reviewer compares it with photographs.

## The pieces

| Piece | File | What it is |
|---|---|---|
| Sources | [SOURCES.md](SOURCES.md) | every number and photograph with its source and licence (helper, checked on return) |
| Target | [target.json](target.json) | the numbers, each traced to SOURCES.md |
| Target drawing | [target_drawing.py](target_drawing.py) | the elevation, vertical section and horizontal section drawn in 2D from target.json, the way a joinery manual draws them; never reads the model |
| The attempt | [window_design.py](window_design.py) | the window assembled member by member as 3D joinery (box frame, moulded and rebated sashes, horns, bars, oak sill), built in Blender by [../tools/blender_parts.py](../tools/blender_parts.py) |
| The check | [check_window.py](check_window.py) | cuts the built model where the target is drawn and compares in millimetres; pass = every drawing overlap at least 0.97, outline 95th percentile within 2 mm, worst point within 6 mm, every dimension within 1 mm |
| Attempts | checks/check_*.json (git); models, overlays and drawings on F:edgertoolsabsashbuild | one line per attempt below |

## Attempts

- v0 (7 Oct, 21:20): pipeline debug on placeholder numbers only, before any source arrived; counts for nothing. It showed the check working: the outer linings behind the brick and the head lining were flagged until the elevation was clipped to the brick opening (the brick hides them, so the check now does too).
