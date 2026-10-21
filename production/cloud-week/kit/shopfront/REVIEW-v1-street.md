PASS

# Shopfront unit 3.2, Rita's front: review of v1, STREET view

Cloud week 42, 11 October 2026. A fresh reviewer: I did not write the target or build the piece, and I have not seen any other review. I judged the street render (about 9 m out, the whole front) against the target's photographs and drawing, the approved game front, and period photographs reached today. Jafar's ruling of 9 October applies: a piece that fails only on narrow points passes, with those points listed.

As the brief asks, I did not judge these: the empty door and side-door slot (the dark opening), the blank fascia, the missing wall and glass reflections, the render's light, its pale ground, and wear.

## Faults (things a player would see as wrong at this distance)

None. At 9 m the front reads as a real painted timber parade front of about 1900 to 1935, kept on into 1990. The parts, their order, their proportions and their relief match the photographs, and I found no visible build fault: no holes, gaps, overlapping faces, floating parts, or faceting where a surface should be round.

## Narrow points (exact fixes, worst first)

1. **The toplight bars do not line up with the mullions. Target's.**
   - Where: in the toplight row above each of the two mullions. Each mullion stops at the transom, and the nearest bars stand about 140 mm to either side of its line. In the render, the mullions are centred at x 878 and 1088 px, and the bars at 829 / 904 and 1060 / 1139 px.
   - In the target, `shops[ritas].glazing_layout` puts the mullion centres at 1121.7 and 2228.3 from the frame's left edge, but the toplight bars at 855.5, 1265.2, 2084.8 and 2494.5. That is 8 equal toplights over 3 lights, so no bar can fall on a mullion line.
   - What the reference shows: the approved game front (production/previews/rita-day-kit-2026-10-06.jpg) has a toplight bar directly over its mullion. None of the period photographs I reached shows toplights large enough to check, so this point rests on the approved model and on joinery practice, not on a period photograph.
   - Fix: carry each mullion's line up through the toplight row as a 70-wide bar on centres 1121.7 and 2228.3. Then split each light's toplight into three with two 28-wide bars (`toplight_bar_plan`). That gives bar centres at 390.9, 745.8, 1497.6, 1852.5, 2604.2 and 2959.1, and 9 equal toplights of 326.9 each (toplights 9, not 8). The transom, head, glass and beads are unchanged.

2. **The leaf on each console reads as a stack of horizontal ribs. Build's.**
   - Where: on the front face of both consoles, in the middle of the fascia's height. At this distance it looks like a ribbed, downward-pointing triangle (a fir-tree or radiator-fin shape), not a carved leaf.
   - Cause: the build cut "a groove 3 deep across each notch between the lobes" (NOTES, judgements). Those horizontal grooves catch the light more strongly than the 4 mm rib.
   - What the target says: an acanthus pendant with a rib 8 wide and 4 proud, and grooves 4 x 3 between the lobes. It does not ask for horizontal grooves.
   - What the photograph shows: the consoles in Colliergate, York (2013, below) read as vertical members, a scroll with a drop at the foot. Nothing on their faces runs across. No period photograph of a console was reached at a readable size.
   - Fix: keep the rib full length (z local 150 to 420) as the strongest relief. Cut each groove between lobes diagonally, from the rib outward and downward at about 45 degrees to its notch in `leaf_outline`, not straight across. Failing that, drop the cross grooves and let the lobed outline and the rib carry the leaf.

3. **The cornice's crown is at the light end of the photographs. Target's; no change asked of the builder.**
   - Where: the top band of the front. The crown is 150 high on a 550 board, 0.27 of the board, and it reads as a plain thin cornice.
   - What the photographs show: Hull in 1977 (below) has a plain front whose cornice is about 0.4 of its fascia's height. Colliergate (2013) has about 0.6, and there the cornice breaks forward over the console heads.
   - The target's own section 3 puts the true crown at 170 to 300. It keeps 150 because the fascia target fixes the cornice top at 3.55 m and the hanging signs' brackets at 3.60 m.
   - At 9 m the render's cornice still passes as the plain kind that Hull 1977 shows, so this is not a fault.
   - If a heavier crown is wanted later: lower the soffit to 3360 (crown 190, board 510, which is within P1's measured 505) and leave the top at 3550. That changes the fascia target's board, so it is Jafar's call, not the builder's.

4. **Things in the render scene, not in the piece. To check when the doors land.**
   - A pale sliver about 20 mm wide (4 px) runs down the left pier's inner side and under the fascia across the door slot. It is sky seen through the empty slot, because the scene's dark box does not fill it.
   - The sill and the stallriser end square and exposed at u 2300, beside the empty shop-door slot.
   - In the assembled game, the side door's frame (d 100) must close against the pier's backing core, and the shop door's jamb must cover the sill and stallriser ends. When the door family is added, check from this same camera that no daylight or bare end grain shows.

## What is right

- **The parts and their order** match the period photographs. A pier has a plinth, a panelled shaft and a capital. A console stands on each capital through the fascia's height. A plain board runs between the consoles, and a cornice runs over the whole width with both ends closed. Below, the window frame stands on a stout sill over a panelled stallriser.
  - Hull 1977 shows the same arrangement on a humbler front: piers with simple caps, a plain fascia, a thin projecting moulded cornice, and a sill over the stallriser.
  - Colliergate shows consoles over the piers through the fascia's height, and a panelled stallriser.
- **The proportions** read as a 1900 to 1935 parade front: fascia 550 in a 3.55 m front (0.155); sill and plinth tops at 600; a toplight row about 310 high over an 80 transom; three lower lights of about 1.04 m each. The bay matches the target's elevation (D1) and the approved game front.
- **The relief reads at street distance:**
  - the shaft stands clearly in front of the window jamb, with a visible shadow line;
  - the plinth stands in front of the shaft;
  - the sill's nose throws a line on the stallriser;
  - the consoles stand proud of the board at every height, with no board end or bed mould showing beside them. The second target review's console fault is fixed as seen from the street.
- **Rita's line holds**: on both piers the plinth's top is level with the sill.
- **The stallriser** has three raised-and-fielded panels over a skirting, with its muntins on the mullion lines (x 880 and 1090 px against the mullions at 878 and 1088).
- **The window**: the mullions have round noses that read as round (no facets), and the frame is a believable timber section, neither aluminium-thin nor arcade-heavy.
- **The cornice's mitred returns** close both ends as boxes. The cornice nose oversails the consoles by a small margin, and nothing floats.
- **The kind of colour**: deep oxblood gloss on the piers, consoles, board, cornice and stallriser, with white gloss on the frame and sill. That is a plausible 1990 repaint of a timber front, of the same kind as the green-painted timber front in York in 1990 (below).

## Photographs used

**Period photographs reached today (Geograph):**

1. **Hessle Road, Kingston upon Hull** (a disused small timber shopfront in a northern port).
   - Page: https://www.geograph.org.uk/photo/2880716
   - Taken 1977. CC BY-SA 2.0 (Chris Morgan).
   - Used for: the arrangement of the parts; a thin projecting cornice about 0.4 of the fascia; piers with simple caps; sill over stallriser.
2. **Russell's bicycle shop, Clifford Street, York.**
   - Page: https://www.geograph.org.uk/photo/1618041
   - Taken June 1990. CC BY-SA 2.0 (Michael Jagger).
   - A painted timber front with piers and fascia. At 640 px it is too small for detail, so it was used only for the kind of front and of paint in a northern city in 1990.

**Modern photograph, said as such:**

3. **Detail of 1-2 Colliergate, York** (a restored timber front).
   - Page: https://www.geograph.org.uk/photo/4893401
   - Taken 13 May 2013, not period. CC BY-SA 2.0 (Stephen Richards).
   - Used for: consoles on the piers through the fascia's height, how they read, and the cornice's weight.

**The target's own references:**

- the P1 Leadenhall previews (2019, CC0, Poly Haven) and the target drawing D1, both in production/previews/cloud-week/refs/shopfronts/;
- the approved game front, production/previews/rita-day-kit-2026-10-06.jpg.

**Seen and not used:**

- Geograph 775756 (Salisbury, 22 July 1992, CC BY-SA 2.0): a faience front, not timber.
- About thirty other pre-1995 Geograph results: street scenes with no readable shopfront.

**Wikimedia Commons**: one search returned no files, and the next request was refused (rate-limited). Nothing from Commons is used.

Downloads and crops are in the session scratchpad (sf-review-street/). Nothing was placed in the repository except this review.
