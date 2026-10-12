PASS

Street view, kit unit 3.5 (litter bins and dustbins), first review. Fresh reviewer, 12 October 2026. Judged on the composition render street.png (1600 x 1200, camera 6 m out, eye height 1.6 m, lens 32), with 4x to 7x crops. Before forming this view I did not read the target's review, any other bin review or the build notes. Seen from the street, all three kinds read as British bins, at the right size and in the right shapes. There is no wrong profile and no visible build fault in the bins themselves. The points below are narrow, and each has an exact fix. The first one must be fixed before K1 B is placed. One known shortfall stays open: no photograph from 1975 to 1995 of a pole-mounted bin was reached, by the target or by me, so K1's form is still judgement. It is plausible, but no photograph confirms it.

## Faults, worst first (all narrow; for the builder)

1. **K1 B: the refuse sack reads as a black rubber lid. Build's fault.** Where: the leftmost bin, on top of the rim. The `k1_sack` mesh is a smooth black dome, 150 mm thick. Measured in the .glb, it sits wholly inside the rim (y 0.989 to 1.139). It stands 89 mm above the rim, with an 18 to 31 mm gap all round to the bin wall and nothing below it. Nothing turns over the rim. At street distance it is the darkest shape on the left of the frame, and it looks like a lid or a hat. The target (K1-w11) asks for "a black sack as the liner: tucked over the rim 120 on the outside, a tie, a split showing contents". A sack-lined open bin is recognised by the black band of the turned-down mouth below its rim. Exact fix: replace `k1_sack` with a liner sack.
   - **The cuff:** the mouth turns down over the rim bead and hangs on the outside, from z 1,050 down to about z 930, 2 to 4 mm off the wall (r about 0.19 at the rim). Give it 4 to 6 bunched gathers where it is pulled tight, and leave a gap where it is tucked, round the strap side.
   - **The body:** the sack fills the bin down to the base, so no void is left under a floating cap. It bulges no more than 60 to 90 mm above the rim, with creases. Use the Poly Haven trashbag the target names, or a cloth simulation, scaled to fit.
   - **The rest:** keep the tie and the split as the target says.

2. **K2: the dome's lip over the aperture is missing. Target's fault; the build follows the profile.** Where: the second object, at the top of the hood.
   - **The photograph:** in S12 (Geograph 974902, 2008), the flat dome's lower edge is a rounded lip that stands slightly proud of the hood skirt. It meets the skirt at about z 780 (photo y about 185 to 190 in the target's 630 px crop, the bin's ground at y 940). It casts a shadow line right round the hood. The slot's top edge is that lip, so the dome hoods the opening.
   - **The render:** a plain band of skirt about 37 mm deep runs between the slot's top (z 785) and the start of the dome's shoulder (z 822). There is no edge and no shadow line. The hood reads as one smooth cap with a slot cut in it.
   - **Fault 1917089:** the later hooded drum at Fifehead Magdalen (2010) has the same arrangement: the slot sits directly under a projecting top rim.
   - **The target contradicts itself:** its own aperture note says "the upper edge is the dome overhanging it", but `outer_profile_rz` has no overhang.
   - **Exact fix in the target profile:** make the skirt r 218 from z 650 to 778. Add a lip from (218, 778) out to (224, 782), round it R4 to (224, 790), and start the dome from there: (222, 800), (214, 830), (200, 858), (175, 880), (130, 893), (60, 899), (0, 900). Keep the aperture at sill 680 and top 785, so the lip's underside is the slot's top edge.
   - **Then rebuild K2 a, b and c.** The burn hole on c stays where it is.

3. **K1 C: the rim dent shows as a sharp upward kink, like a pouring spout. Build's fault.** Where: the rightmost bin, at the back of the rim next to the post. In the .glb, the inward push is concentrated within about 30 degrees of arc (azimuth 140 to 180), with hard ends. The target asks for 120 mm of arc length, 18 deep. Seen from 1.6 m, the hard ends turn the rim's ellipse into a pinch. Exact fix: spread the dent over the full 120 mm of arc length, with a cosine falloff over its whole length (no flat-bottomed section). Make the rim's drop (now about 5 mm) the deepest at the dent's centre and taper it the same way.

4. **D1 b: the loose lid stands on its edge at 72 degrees, leaning on nothing. Placement point, not a model fault.** Where: right of the fourth object. The target stands it against the wall, but the composition has no wall, so here it would fall over. The notes say the engine may move it. In Quay Street it must lean against the wall or against the can (resting on the can's foot hoop and rim), never stand free.

5. **K1: the bolt heads, nuts and ears render bright bare zinc.** The target (K1 bracket bolts) says galvanised, painted over once with the bin, with only a worn edge showing grey. Material slot `zinc_galv`: give it the condition's paint, and leave the grey to the edge-wear mask.

6. **K2: the cement patch renders as a bright white plate** against this render's darker ground. This is a matter of the render's ground, not the model. In S12 the patch is pale grey-beige and only a little lighter than the flags. Check it beside the footway's own flags in the engine, using the target's sRGB 186, 184, 176.

## What is right

- **K1 (both conditions shown):**
  - **Size against the street:** the rim is at 1.05 m and the post at 1.255 m. The bin is 373 across the bead and stands 205 below the post's cap. That is about waist height for a 1.75 m person, the height at which a hand drops litter into an open bin. The bin tapers slightly, wider at the rim.
  - **The rim:** the rolled bead reads as a rounded edge, not a sheet edge.
  - **How it hangs:** two flat clamp rings round the post, with the ears and bolts on the far side of the post. The bin hangs close to the post on its spacer bar. The bar ends above the bin's base, and that small step shows correctly at the lower back corner. No part runs into the post or floats free.
  - **The lean:** the posts look as if they lean about 5 to 6 degrees outward. That is the camera: it is pitched down about 9.5 degrees, so verticals near the frame's edges lean outward, the left post one way and the right post the other. Measured in the .glb, the posts lean 1.26 degrees (B) and 1.6 degrees (C), as the target asks (1.2 and 1.5). That reads as an old post, not a fault.
  - **K1 C's mirrored hang** (bin on the left of its post) reads correctly. Its 2.5 degree tilt shows only slightly at this distance, which is right.
  - **Round surfaces:** the post, the bin and the rim are round in silhouette, with no visible faceting.
- **K2 (condition c shown):**
  - **The profile matches S12 closely:** the base drum is the widest part, then a shoulder up to the collar, the plain body, the hood's lip and groove, and the skirt under a flat shallow dome. The height-to-width ratio is 1.92 in the render and about 1.9 in the photograph. The body-to-base width ratio is 0.87 in the render and 0.86 in the photograph.
  - **The aperture** is a rounded slot of the right size and height, with its sill visible.
  - **The burn hole** reads as a ragged dark notch in the hood's left side. It is clearly damage, not a second slot.
  - **It stands on its patch** without a gap.
  - **Its form reads as a council hooded glass-fibre bin,** not a modern panelled bin.
- **D1 (conditions a and b shown):**
  - **Size and silhouette:** 0.46 across and 0.61 high, with the lid 0.05. It has a rolled foot hoop, a plain tapering body (its flutes come as a normal map), two rolled rings under a rolled top bead, a horizontal round-bar grip on two riveted lugs, and a lid with a skirt over the rim and a flat strap handle. That is the silhouette of a British galvanised dustbin, the same as in Cusop and Chawleigh.
  - **The lid** overhangs the rim by about 20 mm, as in the photographs.
  - **D1 b's open mouth** reads as an open can.
  - **Colour:** the zinc grey is the right kind of colour against the green of the council bins.
- **All three:** the colours are the right kinds (council green, paint on K1 against gelcoat on K2, galvanised zinc on D1). There are no gaps, no overlapping faces and no floating parts in the bins themselves (D1 b's loose lid is the placement point in fault 4). Nothing carries any lettering.

## Photographs judged against

The ones I found myself, through Geograph's feed, all CC BY-SA 2.0:

- **Geograph 1917089**, "Fifehead Magdalen: postbox № SP8 62 and phone", taken 2010-06-13. A blue moulded hooded drum litter bin. This is a later example of the same family (hooded drums were made from 1984 on, per the target's leads), not a 1990 photograph. I used it only for the arrangement of a slot sitting under a projecting top rim, with grooves round the drum (fault 2).
- **Geograph 3757342**, "4 dustbins in Cusop", taken 2012-06-10. Four galvanised dustbins: tapering bodies, a rolled top bead, a ribbed domed lid lying on the ground. Galvanised household dustbins of this pattern were made and used unchanged from long before 1990 until wheeled bins replaced them, so the form is the period form. (That is my reasoning, not a dated source.) The target also lists this photograph.
- **Geograph 1278296**, "Church dustbin, Chawleigh", taken 2009-04-29. A galvanised dustbin with vertical corrugations and rings under the rim, its lid on the ground. The same reasoning applies, and the target also lists it.
- **Geograph 974902** (the target's S12), "Litter bin and postbox, Wilton Road", taken 2008-09-21. Used for K2's profile and the dome lip (the target's crop and overlay in the refs folder, and the page's thumbnail).
- **Geograph 2877032**, "Street furniture and post box, West Heath", taken 2012-03-19. Two post-mounted bins, both modern rectangular types. They are not evidence for or against K1's period form.

Period street photographs I reached that show no litter bin at the 640 px Geograph serves. They are not evidence for or against:

- Geograph 5185374 (Duke Street and Butterwalk, Dartmouth, July 1990)
- Geograph 5186049 (Foss Street, Dartmouth, July 1990)
- Geograph 4113801 (Winchester High Street, 1990-04-01)
- Geograph 689978 (High Street, Croydon, 1990-04-18)
- Geograph 2059722 (Church Street, Whitby, titled 1990; the taken date was not read from its page)

Searches that found no 1975 to 1995 photograph of a litter bin: Geograph's feed for "litter bin" (1,001 results read, the earliest taken 2003), "litter bin 1980s", "old litter bin", "lamppost bin", "post mounted bin", "pole mounted bin", "hooded litter bin" and "galvanised dustbin", plus "bin", "bins", "litter" and "rubbish" filtered by takenyear 1989 to 1991. Commons and archive.org were not tried. So **K1 has no photograph:** its round open bin on its own post, on two clamp rings, is the target's judgement. It is plausible at street distance, but it is not confirmed.
