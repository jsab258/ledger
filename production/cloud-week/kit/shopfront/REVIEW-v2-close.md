FAIL

# Shopfront parts, Rita's front (unit 3.2), try 2: the CLOSE view (about 1.75 m)

Fresh reviewer, 11 October 2026. I judged the render `kit-shopfront/render2/close.png` (1600 x 1200; also `production/previews/cloud-week/shopfront/shopfront-close-v2-2026-10-11.jpg`) against the target's photographs (P1 previews in `production/previews/cloud-week/refs/shopfronts/`) and five Geograph photographs I reached today (listed at the end). I did not read REVIEW-v1-*.md. I read NOTES.md and departures.py, which name try 1's faults in their own words. I also read the builder's code and ray-cast the built cornice (`build/cornice.npz`) for one point. Pixel positions below are in the 1600 x 1200 render.

The verdict: the piece fails on one fault, the acanthus leaf. The console's form, the cornice's break, the capital and the shaft all agree with the photographs. The leaf is the focal ornament of this view, and at this distance its carving shows stair-stepped edges and bright slivers, which is a visible build fault (the brief's "faceting where it should be round"). The fix stays inside `_leaf` and touches no other part. If it is applied, I would pass this view on the narrow points below.

## Faults, worst first

### 1. The acanthus leaf's carving is stair-stepped and has slivers at its tips (the build's)

- **What and where.** The leaf on the console's front runs from its head on the upper roll (about x 680 to 760, y 370 to 470) down to its tip (about x 765, y 595). Every vein shows a regular sawtooth, which is clearest on the head's chevrons at 1:1. Along the lower lobes' left edges there are thin bright slivers and a jagged outline. At 1:1 the whole leaf reads as a jagged herringbone, like a fir cone or a stack of arrowheads, not as carved timber. The head's turned tip also makes a small spur that breaks the upper roll's silhouette (about x 652, y 410).
- **What the photographs show instead.** Carving on Victorian shopfront consoles is smooth and continuous, even under a century of paint:
  - Kennington Lane (2013): the acanthus on the console's side and the raised volute fillets have rounded lobes and clean edges, with no step anywhere.
  - Marygate, York (2013): the leaf at each console's foot has a smooth outline and a clean midrib.
  - Percy Park Road, Tynemouth (2021): the console's front relief is low and smooth-edged.

  None of them shows a stepped groove or a sliver.
- **Why it happens (`build_shopfront.py`, `_leaf`).** The leaf is a height-field sampled on a grid of 5 mm rows by 25 columns (about 5 mm apart at the head). The veins are 3 wide (their groove is about 4.4 wide), so each vein falls between samples and comes out as a zigzag of single-sample dips: the sawtooth. The tip term `L["tip_forward"] * exp(...) * ... * (1.0 if d_out < 6.0 else 0.0)` has a hard cut 6 mm inside the outline, which leaves a cliff up to 6 mm high at each tip. Those cliffs catch the light as slivers and make the spur on the roll.
- **The exact fix**, in `_leaf` only:
  1. **Make the mesh follow the veins.** Replace the row grid (`zs` every 5 mm by `nc = 25`) with a constrained triangulation of the leaf's outline.
     - Use as constraint lines: the outline (the right half mirrored, plus `head_extension`); each vein's centre line and its two edges offset ±1.5 mm; and the rib's two edges at u ±4. Densify every constraint line at 1.5 mm.
     - Add interior points on a 4 mm grid, kept at least 2 mm clear of every constraint line.
     - Triangulate with `mathutils.geometry.delaunay_2d_cdt(verts, edges, [], 2, 1e-4)`. Output type 2 is constrained and keeps the inside of the outline only. The builder already runs under bpy.
     - Set each vertex's depth as now: `-(F_of_z(z) + height(u, z, w) - 0.3)`. Keep the back plane at d 120 and the walls as they are, with the edge loop taken as the outline's vertices in order.

     Every vein edge then becomes a straight mesh edge. The vein's centre-line vertices sit on the groove floor (2 down) and its edge vertices on the lobe surface, so each groove is a clean V from notch to rib. Expect about 3,000 vertices (about 6,000 triangles front and back), about what the leaf has now. console.glb stays under 400 KB.
  2. **Fade the tip turn instead of cutting it.** In `height()`, change the tip term's `* (1.0 if d_out < 6.0 else 0.0)` to `* max(0.0, 1.0 - d_out / 6.0)`. The turned tip then fades to nothing 6 mm inside the outline, with no cliff, and the spur on the roll's silhouette goes too.
  3. **Accept when** the close render at 1600 x 1200 shows each vein as one straight groove with no step along it, no bright sliver at any lobe, and an unbroken silhouette on the upper roll. Every other number in D3 stays: the outline, rib 8 x 4, veins 3 x 2 at 35 degrees, lobes domed 12, tips 6 forward, head to z 471.

## Narrow points (these would not fail the view alone; each has an exact fix)

1. **An open slot in the top of each cornice break (the build's; it cannot be seen from the street).**
   - **What.** The break is the profile's front part (d 130 to 215) swept 85 forward, so its back wall stands at d 215. The main run's members behind it fall back to d 200 to 211 above the corona, and its wash runs back to d 150. Between the break's two returns this leaves a pocket open to the sky. I ray-cast `build/cornice.npz`: at u 150 to 210 (and the same at the right break), the top falls from z 3550 to 3453 to 3461 for d 208 to 214. The pocket is about 80 long, 10 wide at the cap and 65 wide at the top. It would hold water and shows from any upper window.
   - **Fix.** In `cornice()`, after the two break unions, union into `cor_cornice` one box per break:
     - left break: u 138 to 222, d 145 to 216, z 3400 to 3550;
     - right break: u 5779 to 5862, same d and z.

     Each box lies wholly inside the returns, the main run and the break, so no new face shows. The break's top becomes flat from the wall to its own wash, which is how a broken-forward cornice is built.
   - **Accept when** a vertical ray anywhere over a break, from d 0 to the break's wash, finds the top at z 3550.
2. **The board's bed mould stands 2 mm proud of the console's foot over the lowest 20 mm (the build's departure D1; the builder noted it).** At about x 700 to 830, y 655 to 690 it cannot be seen at this distance.
   - **Fix.** In `departures.py`, set `FOOT_D = 134.0`. The lower roll still leaves the foot, now at about z 22. The board's bed mould (132) then dies into the console's side. Re-run CON-09.
3. **The lower side spiral is partly hidden behind the board.** Its eye is at d 125 and the board's face is at d 120, so only the front half of the spiral shows: a small curl beside the board at about x 820 to 835, y 625 to 650. It reads as the end of a scroll housed against the board, which is how Marygate's consoles meet their fascia. **No change asked.**

## What is right

- **The console's profile now matches the photographs.** It is a tapering bracket: a big upper roll projecting at the head, a concave body narrowing to the waist, and a small lower roll at the foot. That is Kennington Lane's console seen side-on (big volute above, small below, the waist between) and Marygate's (deep at the head, tapering to a small foot on the pilaster). Its height matches the board's, so it frames the board's end as on Charles Street, Hull (1989).
- **The side spirals** are raised fillets winding into an eye boss on the upper roll, as on Kennington Lane. They are clean and well proportioned, and no faceting shows on the roll at 6 degree steps.
- **The cornice breaks forward over each console** with mitred returns of its own profile. A plain cap block sits under the break and the console's roll carries it, as at Marygate (the cornice broken forward over every console) and Kennington Lane (a block over the console's head). The break, its returns and the main run meet cleanly, with no gaps or overlapping faces seen.
- **The bed mould (cyma) under the corona** runs between the consoles and dies into the cap blocks.
- **The fascia board's end is housed against the console's side.** No board end or mould shows proud of the console's front at any height.
- **The capital reads as a pier cap of the kind P1 shows,** and its order is right: astragal, neck fillet, a die with a raised tablet (its eased edge reads as paint-softened timber), a hollow flare and the abacus. The console's foot stands on the abacus with no gap, and the abacus shows a small ledge in front of it. The panelled shaft is right too: stiles, the sunk field and the top rail under the astragal.
- **Construction:** I saw no floating parts, holes or z-fighting outside the leaf. The dark interior and the blank fascia are as the brief intends.

## Photographs used

| Photograph | Page | Taken | Licence | What I used it for |
|---|---|---|---|---|
| Detail of 332 Kennington Lane (Stephen Richards) | https://www.geograph.org.uk/photo/4782551 | 2013-04-20 (after 1995: the only close side view of a shopfront console reached) | CC BY-SA 2.0 | The console's S-profile (big upper volute, small lower one, concave waist); raised spiral fillets and eye bosses; smooth carved acanthus; the block over the console under the cornice |
| Detail of 64 Marygate, York (Stephen Richards) | https://www.geograph.org.uk/photo/4919236 | 2013-05-14 (after 1995; a northern town) | CC BY-SA 2.0 | Consoles tapering from a deep head to a small foot on the pilaster; the cornice broken forward over each console; a smooth-edged leaf at each console's foot |
| Ruby & Frank, 4 Percy Park Road, Tynemouth (Geoff Holland) | https://www.geograph.org.uk/photo/6767122 | 2021-03-02 (after 1995; a northern port, front built in the 1880s) | CC BY-SA 2.0 | A console's front with low, smooth relief carving; the head turning over into a scroll under the cornice |
| Charles Street, Kingston upon Hull (Bernard Sharp) | https://www.geograph.org.uk/photo/3801638 | 1989-02-09 (in the period; a northern port) | CC BY-SA 2.0 | A pair of scrolled consoles at a party wall between two shop bays, each the fascia's height under a projecting cornice. Too small for profiles; used for period presence and placement only |
| Detail of 12 Mercer Street (Stephen Richards) | https://www.geograph.org.uk/photo/5367348 | 2013-08-03 (after 1995) | CC BY-SA 2.0 | Seen, not relied on: the consoles shown are of another kind (scrolled pier heads) |
| P1, Leadenhall Market, the target's previews (Poly Haven, Andreas Mischok) | https://polyhaven.com/a/leadenhall_market | 2019-05-19 | CC0 | The capital's members (die, flare, abacus) and the pier-and-fascia order. It shows no console |

How I searched: Geograph's syndicator feed (`q=` with words such as "shopfront console", "console bracket detail", "shopfront detail"; `takenyear:1975` to `takenyear:1995` with "shop" and "shopfront"). That gave 441 photographs taken 1975 to 1995. Of the ten nearest to the subject that I downloaded, only Charles Street, Hull shows consoles at all; none shows one close up. Wikimedia Commons' API answered one search (200) with no close-up of a shopfront console. Downloads are in the scratch folder `sf-review-close2/dl/`, crops in `sf-review-close2/`.
