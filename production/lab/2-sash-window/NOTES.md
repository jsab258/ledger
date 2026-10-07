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
| Attempts | checks/check_*.json (git); models, overlays and drawings on F:/LedgerTools/lab/sash/build | one line per attempt below |

## Attempts

- v0 (7 Oct, 21:20): pipeline debug on placeholder numbers only, before any source arrived; counts for nothing. It showed the check working: the outer linings behind the brick and the head lining were flagged until the elevation was clipped to the brick opening (the brick hides them, so the check now does too).
- Sources (7 Oct, 22:30): SOURCES.md, by a helper over 88 minutes: George Ellis, *Modern Practical Joinery* (1902) pp.121-128 as the anchor (Fig. 400's frame section and Fig. 399's vertical section fully dimensioned), Hasluck (1907), Rivington (1875, 1889), Riley (1905), Allen, Mitchell and Burrell (text only); nine Commons photographs (CC BY-SA), only four of them original timber sashes and none a dated 1880-1900 terrace with original windows. Checked on return: Ellis Figs. 399-404 and 415-416 read on the page images (the numbers in target.json agree); one photo licence re-read on Commons (Cemetery Road, CC BY-SA 4.0, Acabashi).
- Finding for the builder: no source supports the game's 0.85 by 1.50 m opening height; every period example is 5 ft 6 in (1.676 m) high, and Rivington's rule is two to two and a half times the width.
- target.json (22:35): every value tied to its page; the opening is Ellis's worked example, 2 ft 8 in by 5 ft 6 in. A fourth drawing added: the vertical section through the stiles, which shows Ellis's horn ("bracket", Fig. 416: an ogee on its inner face, 3 in long; the step and curve scaled off the figure, not printed).
- v1 (22:40), first sourced attempt: FAIL. Elevation passed (overlap 0.993). The sections failed (vertical overlap 0.75, worst point 37 mm). What the overlays showed, and who was wrong:
  - the model's oak sill ran on behind the inside lining; Ellis's sill stops at the staff bead's face (frame depth 5 1/8 in): **model wrong**;
  - the inside lining sat behind the staff bead in both drawings; Ellis's Fig. 400 has the staff bead planted on it, sharing its depth: **target and model wrong** (the same misreading made twice, by one author: an exact target does not catch an error both sides share);
  - the target had no frame head; Ellis's Fig. 399 draws it (H, 1 1/4 in): **target wrong**;
  - the target drew sash members as plain rectangles; Ellis gives the glass rebate (1/4 in) and the stuck moulding: **target wrong**;
  - the horn length and the opening were measured off the wrong parts: **checker wrong**; and a 1.6 mm clearance closed at 1 mm a pixel in one drawing and not the other: **checker resolution**, sections now drawn at 0.5 mm.
- v2 (22:50): **PASS**: elevation 0.993 overlap, worst 1.4 mm; vertical section 0.998, worst 0.5 mm; horizontal section 0.9998, worst 0.5 mm; section through the stiles 0.994, worst 0.5 mm; all ten dimensions exact (checks/check_v2.json). Rendered for the reviewer (Workbench only): F:/LedgerTools/lab/sash/build/render_v2.
