FAIL

# Bollards (unit 3.4), try 2: the close view (K5's foot, nuts, lower lugs, lower bead)

Fresh reviewer, 11 October 2026 (cloud week 42). Judged: `close.png` (v2, also `production/previews/cloud-week/bollards/bollards-close-v2-2026-10-11.jpg`), against the target (`production/cloud-week/targets/bollards/TARGET.md` section 5.5, `target.json` `kinds.K5`), the build (`build_bollards.py` `k5_profile`, `build_kind`) and the photographs listed at the end. The main one is LH_b at full size: the target's own source, the 16k Limehouse panorama, re-projected at 0.5 mm a pixel in the target's own frame (bearing -59.492 degrees, 1.7206 m, camera 1.17 m), so the foot, nuts, bead and lug can be seen at about twice the detail of the previews. Not judged: tone, the light, the pale ground, wear.

**Verdict: one fault a player would see at 1.3 m (the lower bead's profile, the target's), and five narrow points. Each has an exact fix below. The bead fix is about twenty points of profile and no new parts.**

## Faults (worst first)

### 1. The lower bead is a soft swelling, not a cast roll moulding (the target's fault; the build follows it)

- **What, and where in the view:** the bead in the middle of the frame, just under the lower lugs. In the render it is a long, gentle swelling 120 mm high (z 278 to 398) and only 14 proud (r 105 on a shaft of r 91). Its upper half is almost a straight cone, running out over 63 mm, so it fades into the shaft above and below with no edge. At 1.3 m it reads as a balloon-like bulge in a pipe. It is the most visible form in the view.
- **What the photograph shows instead:** LH_b at full size (re-projected; the right-hand silhouette measured row by row against the bright pontoon behind it; radius in mm at a camera height of 1.17 m, where the shaft reads r 93):

  | z | 276 | 294 | 300 | 306 | 312 | 318 | 324 | 330 | 336 | 342 | 348 | 354 | 360 | 366 | 372 | 378 | 396 |
  |---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
  | r | 94 | 94 | 94 | 99 | 104 | 108 | 110 | 111 | 112 | 111 | 110 | 107 | 105 | 100 | 97 | 93 | 93 |

  Scaled to the target's shaft (r 91, x 0.978), the real bead is a full, nearly elliptical roll about **78 high (z 290 to 368) and 18 proud (r 109 at z 330)**. It meets the shaft at a **definite re-entrant corner top and bottom**: the silhouette steps out 5 mm in the first 6 mm instead of running out tangentially. In front view there is a **quirk on its upper face**: a dark groove line just inside the top of the roll, with a narrow fillet ring above it stepping back to the shaft. The target's own previews are too soft at 1.1 mm a pixel to show this, which is probably how the 120 mm reading came about. The cast chain posts at Tong (Geograph 4938930) show the same kind of crisp-arrised ring mouldings with flat fillets and sharp corners to the shaft. No cast post in any photograph used has a bead that fades out.
- **Whose:** the target's (`target.json` `kinds.K5.profile_rz` and the `lower_bead` part: "278 to 398, r 105, 120 high"). The build lathes it faithfully.
- **Exact fix:** in `target.json` `kinds.K5.profile_rz`, replace the nine points `(91, 278), (95, 285), (101, 297), (105, 315), (105, 335), (103, 352), (98, 372), (92, 390), (90, 398)` with these (an elliptical roll, centre (88, 330), semi-axes 21 radial by 40 vertical, then a quirk and a fillet ring):
  `(91, 290.4), (95.2, 292.4), (100, 297.2), (104.1, 304.3), (107, 313.1), (108.7, 323.1), (109, 330), (108.7, 336.9), (107, 346.9), (104.1, 355.7), (100, 362.8), (98.5, 364.6), (96, 365.5), (96, 370), (94.5, 373.5), (92, 376), (90, 377.5)`
  (the next point stays `(87, 600)`). Then:
  - set the `lower_bead` part to z 290 to 378, r_max 109, with the text "a full roll 78 high and 18 proud, crisp corners to the shaft, a quirk and a fillet ring on its upper face"; set `mouldings.lower_bead` to z [290, 378] and r_peak 109;
  - in `TARGET.md` section 5.5, update the profile and the part row to match;
  - update any K5 bead check in `check_bollards.py` and `self_check.py` to the new numbers.

  If the target cannot be touched before the rebuild, apply the same points as a named departure in `k5_profile` (the way try 2 applied the flange seat). Do not fillet the two corners where the roll meets the shaft: at most R1.5. The lower lugs (eye at z 420, root from z 392.5) then stand on 15 mm of plain shaft above the bead, as in LH_b.

## Narrow points (each a small detail with an exact fix; none fails the piece alone)

1. **The nuts are painted black** (build's fault). Each nut is built in `mname` (`paint_black`). The target says nuts and studs are bright steel (150, 150, 152, metal 1). The full-size LH_b shows all three visible nuts and their washers as pale bare or zinc-grey steel against the black flange. In the render they read as black lumps with silver pins. **Fix:** in `build_kind`, `B.add("nut_%d" % i, ..., mname, ...)` becomes `B.add("nut_%d" % i, ..., "bare_steel", ...)`. The dull rust at the threads comes from the engine mask.
2. **The studs are too thin** (build's; the target gives no diameter). The studs are lofted at radius 5.0, a 10 mm pin in a 22 mm across-flats nut, which is an M14 size. LH_b's stud ends measure 12 to 14 mm, about half the nut's width, with threads and a chamfered end. **Fix:** stud radius 5.0 becomes 7.0 (M14), with a 1.5 mm 45-degree chamfer ring at the top. Add `"stud_diameter": 14` to `target.json` `kinds.K5.fixings.bolts`.
3. **No washers** (target's and build's). LH_b's left and right nuts each stand on a flat round washer, seen as a ring wider than the nut at its foot. **Fix:** add a plain washer under each nut, 28 outside diameter, 15 hole, 2.5 thick (an M14 plain washer), on the seat at z 42 to 44.5. Raise the nut to z 44.5 to 58.5 and the stud end to z 72.5 (the stud stays 14 above the nut). Material `bare_steel`. Add `"washer": {"od": 28, "thickness": 2.5}` to the target's `bolts`. The washer at r 124 + 14 = 138 stays inside the seat (r 108 to 139).
4. **The nuts are plain hex prisms** (build's). Only a 1 mm bevel, so the top reads as a sharp-cornered hexagon. A real hex nut has a 30-degree chamfer on its top face, which turns the top into a circle touching the flats. At 1.3 m this is what makes a nut look like a nut. **Fix:** chamfer each nut's six top corners at 30 degrees: a 2 mm cut at the corners, falling to nothing at the flats (intersect the prism with a cone of half-angle 60 degrees whose top circle has a diameter equal to the across-flats, 22). Bevel 0.5 on the bottom.
5. **The lugs are flat plates butted onto the shaft** (build's). Each D-lug is a prism with a 2 mm bevel, let 4 mm into the shaft with no fillet, so a hard crease runs round its root, and its flat faces and square edges read as cut plate. On LH_b the lug is a rounded boss that blends into the shaft. A cast lug is one piece with the post, as Tong's cast fixings show. **Fix:** keep 55 x 40 x 18, the 24 mm hole and the eye at 22 from the shaft face. Add an R6 fillet all round the lug's root where it meets the shaft (a lofted ring or a weld-style fillet mesh in the lug's material). Ease the lug's outer edges R4 instead of 2 mm, and chamfer the eye's two mouths 1.5 mm.

## What is right

- **The flange:** 286 across, a vertical rim about 40 high with a rounded top edge, then the flat seat (try 2's change) and a short cove into the shaft. This matches LH_b at full size, where the shaft runs straight to within about 40 mm of the flange and then meets it in a short cove. The flat seat the nuts stand on is right.
- **The four nuts:** on the 124 pitch circle on the flat seat, standing on it (let in 0.5 mm: no gap, no floating), at 22 across flats and 14 high. Their size against the flange matches LH_b (about 27 across the corners seen there). The stud length above the nut (14) is right.
- **How it meets the ground:** the flange sits flat on the ground with no gap, as on LH_b's resin-bound gravel. The quay apron will take it the same way.
- **The lower shaft:** a plain cylinder of r 91 (LH_b reads 93 to 95 at its camera height, within the target's +-6 per cent).
- **The lugs' layout:** a D-lug on each side in the line of the posts, the lower pair's eyes at z 420 (LH_b's lower link, corrected for its nearness to the camera, is at about 410 to 420), sitting just above the bead. The 24 mm eye is bored cleanly through, with no holes or overlaps in the mesh.
- **Build quality at this distance:** no faceting on the shaft, bead or flange (64 sides), and no seams, gaps, overlapping faces or floating parts. No marks or lettering anywhere: the embossed mark on the photograph is rightly left blank.
- The shaft above the bead (r 90 narrowing to 86) and the upper lugs at the top of the frame are consistent with LH_b.

## Photographs used

| photograph | page | taken | licence | used for |
|---|---|---|---|---|
| LH_b, Limehouse marina (the target's S5), full-size 16k tone-mapped panorama re-projected at 0.5 mm a pixel (scratch only, not published; the embossed mark blurred) | https://polyhaven.com/a/limehouse | 19 May 2019 | CC0 1.0 | everything: the bead's silhouette table, the nuts, washers and studs, the flange and cove, the lug |
| Cast-iron chain posts at a village green, Tong (SJ7907) | https://www.geograph.org.uk/photo/4938930 | 27 April 2016 | CC BY-SA 2.0 | how cast posts' ring mouldings are formed (crisp arrises, flat fillets, sharp corners to the shaft) and how cast fixings blend into the casting |
| Old flanged shipyard bollard, Fyfe Shore (NS3374) | https://www.geograph.org.uk/photo/4824651 | 25 January 2016 | CC BY-SA 2.0 | a bolted cast flange's edge: a square vertical rim with only slightly eased edges, as built |
| Two lines of black iron posts on a riverside walk, Tyne (NZ2664) | https://www.geograph.org.uk/photo/4429544 | 14 April 2015 | CC BY-SA 2.0 | context only (too far away for the foot): black posts standing straight on paving |

**The 1975 to 1995 window: no close photograph was reached.** Geograph's feed was searched year by year for 1975 to 1999 ("bollard" and "bollards" with takenyear). It returned 18 photographs, none a close view of a flanged post, a chain post or a quay bollard's fixings. Searches for chain posts, flanged and bolted bollards and quay bollards (any date) gave nothing earlier than 2006 that shows nuts on a flange. Wikimedia Commons answered 429 once and then returned only scanned books for "bollard chain cast iron". Every photograph above is dated, and all are 2015 to 2019. The judgement rests mainly on the target's own source, seen at full size.

Not opened: `REVIEW-v1-street.md`. The street render was not used: this verdict is on the close view only.
