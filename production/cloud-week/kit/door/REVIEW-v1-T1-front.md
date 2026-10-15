FAIL

# Door T1, v1, view "front" (with front_head and front_foot): fresh review, 9 October 2026

Judged on front.png, front_head.png and front_foot.png against photograph 1 (P1, Teignmouth, Robin Stott, CC BY-SA 2.0, Geograph 3157125), with photograph 2 (P2, Tottenham, Acabashi, CC BY-SA 4.0) as a cross-check. I could not open the source pages from this cloud, so I judged on the preview copies. I scaled the elevation to P1 with the target's own door-plane mapping (5.15 mm a pixel, opening centre at x 192.85 px, z 10 at row 530) and laid it on the photograph, then compared matched crops and brightness profiles down single columns. Because the render's paint is black gloss and P1's is red, I measured each moulding's brightness against the flat leaf face in its own picture, not against the other picture. My working files are in the scratchpad (review-door-T1-front/: overlay_edges.png, cmp_weather.png, cmp_band.png, step_ends.png, cmp_moulding_corner.png).

The brick wall, quoins, arch and plinth are context and are not judged here.

## Faults, worst first

1. **The weatherboard reads as a flat strip, not a weathered roll.** Where: the foot of the leaf (front, rows about 1015-1045; front_foot, rows about 680-745). In the render its main face is as dark as the flat leaf face, about 0.1 on a 0 to 1 scale, with only two hairline highlights near its top. In P1 (rows 514-530) the weatherboard is the boldest member at the foot of the door. Its main face (rows 520-527) is its brightest part, about three times the brightness of the flat leaf face above it, so that face slopes upward to shed water, under a lit top roll. P2 confirms how black gloss behaves: there, every upward-facing moulding member reads pale grey against the black, so a sloped face would read bright on this black door too. Whose fault: **the target's.** Its profile (target.json `mouldings.weatherboard.profile_zp_mm`) holds the "belly" almost vertical at 22-26 mm proud from z 6 to z 50, which turns P1's lit face into a vertical face. The build follows that profile.

2. **The step's nosing is cut off square at both ends.** Where: the two ends of the stone tread (front_foot x about 397-450 and 1150-1205, rows 878-1020; also visible in front at x about 610-625 and 975-990). The half-round nosing is extruded straight and then trimmed by a vertical r 40 plan corner. That leaves the nose's section exposed as a sharp "<" chevron at each end, makes the tread's corners square in elevation, and runs the base face flush to the end with no undercut. In P1 (tread ends at x 87-95 and 283-291, rows 562-600) the nose and its shadowed undercut roll round both ends. The ends look rounded and cushion-like in elevation, with the dark undercut continuing under them. Whose fault: **both.** The target gives the nosing "along its front" only, with "plan corners radius 40", and never says the nose and undercut return round the ends. Its edges entry also says radius 30 where the step section says 45. The build realised the corner as a vertical cut through the extrusion (build_step: keep_inside on a plan prism), and that cut is the visible artefact.

3. **The lock-rail band reads as three thin reeds, not one bold moulded band.** Where: mid-height (front, rows about 705-735; top of front_foot, rows 22-84). In the render, three narrow crests (z 851, 832 and 803 above the leaf bottom) are split by two coves that fall darker than the flat leaf face. Those coves face downward and are deep. In P1 (rows 363.5-377.5) the band is lit across its whole height. Its two creases (rows 367-369 and 372-373) only dip to about 0.7 of its brightest and stay at twice the flat leaf, so the band reads as one or two broad rolls over the crisp shadow below. Whose fault: **the target's.** Its profile has 7 mm deep coves between three narrow crests. The build follows it.

## What is right

- Proportions: laid on P1 at the door plane's scale, the leaf, stiles, muntin, rails, all four panel openings, lock-rail height, transom and fanlight all fall on the photograph's edges within about 1-2 px. That is a close fit.
- Frame: flat and square-edged, 55 mm showing each side as in P1, with the head cambered to follow the arch. No ovolo and no rounded tube edge.
- Transom: reads as P1's white bar, with a bright weathered slope, a face and a lip bead below. The fanlight is a single pane with its bead line.
- Panels: four bolection-moulded panels, tall above the band and short below it, with closed mitres and no faceting.
- Letter plate: vertical on the muntin, the right size and height, with a raised rim and a top-hinged flap.
- Lock and keep: the cylinder lock on the right stile and the dark keep on the right jamb sit where P1 has them.
- No hinges, knocker or chain show outside, matching P1.
- Threshold and riser: the threshold front and the recessed riser sit at P1's rows (534-547 and 548-561). The riser is shaded under the threshold's nose as in P1, and the tread is the right height and width for P1.
- No holes, floating parts, overlaps or faceting show on the leaf, frame, transom or furniture at this view.

## Notes (narrow at this distance; not reasons for the FAIL)

- A bright white line runs under the leaf, and a thin white outline surrounds the letter-plate flap. Both are the context's light-emitting interior box (render_door.py, ctx_dark, emission 0.8) showing through the leaf's 10 mm bottom gap and the flap's 1-2 mm clearances, seen dead level by the orthographic camera. P1 shows both as dark lines (rows 530-533 under the weatherboard). This is not the piece's fault. In the engine, though, whatever sits behind the door will show through these gaps. Consider a water bar on the threshold, or a dark closing face behind the leaf foot and the plate's slot.
- Bolection width: P1's mouldings (x 135-145 px on the upper left panel) read about 45-50 mm wide, with a second internal step (three concentric lines). The render's read about 31-36 mm, with one nose and one cove. The target took P1 as 34 +-8, but my reading is wider and richer. At this distance it is subtle.
- Threshold front: P1's brightness falls off gradually from row 538 to row 547. The front may be rounded over most of its 70 mm height, though staining could also explain the gradient. The render has a flat face under an 18 mm nose. Worth a look.
- Cylinder lock: at the front view's scale it reads as a plain brass disc. P1's reads as a ring with a dark plug. It reads correctly at front_head's scale.
- The house numerals are absent. The target makes them optional and leaves the number to the town.
