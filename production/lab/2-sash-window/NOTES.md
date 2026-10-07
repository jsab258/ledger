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
- Sources (7 Oct, about 22:27): SOURCES.md, by a helper over 88 minutes: George Ellis, *Modern Practical Joinery* (1902) pp.121-128 as the anchor (Fig. 400's frame section and Fig. 399's vertical section fully dimensioned), Hasluck (1907), Rivington (1875, 1889), Riley (1905), Allen, Mitchell and Burrell (text only); nine Commons photographs (CC BY-SA), only four of them original timber sashes and none a dated 1880-1900 terrace with original windows. Checked on return: Ellis Figs. 399-404 and 415-416 read on the page images (the numbers in target.json agree); one photo licence re-read on Commons (Cemetery Road, CC BY-SA 4.0, Acabashi).
- Finding for the builder: no source supports the game's 0.85 by 1.50 m opening height; every period example is 5 ft 6 in (1.676 m) high, and Rivington's rule is two to two and a half times the width.
- target.json (about 22:30): every value tied to its page; the opening is Ellis's worked example, 2 ft 8 in by 5 ft 6 in. A fourth drawing added: the vertical section through the stiles, which shows Ellis's horn ("bracket", Fig. 416: an ogee on its inner face, 3 in long; the step and curve scaled off the figure, not printed).
- v1 (about 22:33), first sourced attempt: FAIL. Elevation passed (overlap 0.993). The sections failed (vertical overlap 0.75, worst point 37 mm). What the overlays showed, and who was wrong:
  - the model's oak sill ran on behind the inside lining; Ellis's sill stops at the staff bead's face (frame depth 5 1/8 in): **model wrong**;
  - the inside lining sat behind the staff bead in both drawings; Ellis's Fig. 400 has the staff bead planted on it, sharing its depth: **target and model wrong** (the same misreading made twice, by one author: an exact target does not catch an error both sides share);
  - the target had no frame head; Ellis's Fig. 399 draws it (H, 1 1/4 in): **target wrong**;
  - the target drew sash members as plain rectangles; Ellis gives the glass rebate (1/4 in) and the stuck moulding: **target wrong**;
  - the horn length and the opening were measured off the wrong parts: **checker wrong**; and a 1.6 mm clearance closed at 1 mm a pixel in one drawing and not the other: **checker resolution**, sections now drawn at 0.5 mm.
- v2 (about 22:37): **PASS**: elevation 0.993 overlap, worst 1.4 mm; vertical section 0.998, worst 0.5 mm; horizontal section 0.9998, worst 0.5 mm; section through the stiles 0.994, worst 0.5 mm; all ten dimensions exact (checks/check_v2.json). Rendered for the reviewer (Workbench only): F:/LedgerTools/lab/sash/build/render_v2.
- Fresh review 1 (about 22:48, REVIEW.md, a reviewer who saw only the brief, the renders and the photographs): **FAIL**. The layout right (two over two, upper sash outside, horns, deep bottom rail, the proportion), but it read as a slim modern window. Three of its points were real errors the automatic check could not catch, because the target and the model shared my misreading:
  - the **horn**: Ellis's Fig. 416 is a face view; the ogee narrows the horn across its width (as photographs 7 and 8 show), not through its depth as I had drawn it in both;
  - the **glazing bars**: given the stiles' 3/8 in rebate each side, a 5/8 in bar has no outer face left, so it rendered as a hairline; Ellis says 3/16 in for bars;
  - **putty** missing (the rebates read as dark gaps), and no side play (the stiles touched the pulley stiles: flicker).
  - The rest was a disagreement between sources: broader visible linings and heavier stiles in photographs 1 and 6 (other window types, of unknown date and region) against Ellis's London box hidden behind the brick; and the brick head and the cill, which are not part of the window and were not in the target.
- v3 (about 22:51): the corrections, and a fifth drawing (the upper sash seen from the face, to check the horn's outline): FAIL on the two face views (overlap 0.95, 5 mm): the putty on the bars lay outside the rebate, over the glass, in **both** target and model (the section drawing agreed with itself; the face drawing, which only the model had putty in, showed it).
- v4 (about 22:53): **PASS** on all five drawings (face 0.989 / 0.998 overlap, worst 1.4 mm; sections worst 0.7 mm) and all ten dimensions. Rendered with a context head (a flat gauged arch one standard 9 in brick deep, not sourced for this window) and a weathered, throated stone cill. Second fresh review (new reviewer) running.
- Fresh review 2 (about 23:03, REVIEW-2.md, a new reviewer told which source the window follows): **PASS ON NARROW POINTS**. Right as a type (box sash behind a half-brick reveal, upper sash outside, ogee horns placed right, proportion, planes, nothing floating). Narrow points: (a) the painted border round the glass is about half the photographs' (7% of the width each side against 12-17% in photographs 1 and 6): even the London original shows 2 1/2 to 3 in of outside lining against Ellis's 3/4 in, so Ellis's drawing looks like the slimmest case, not the typical one; and the meeting rail reads thin and flat beside photograph 6's moulded one; (b) small square stubs where rails meet stiles; (c) a gap in the brick round the cill's ends (render context). The pane pattern (two over two) is a choice of source: none of the four original windows photographed is two over two.
- By the gate's rule (a step passes when its reviewer fails it only on narrow points), the window passes. Left for the builder: (a) is a choice between the manual and the photographs, of taste and region, not of accuracy; the lab did not make it. (b) and (c) are small.
