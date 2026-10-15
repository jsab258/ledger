PASS

# Quay Street's pillar box, second build: the street view (fresh review, 12 October 2026)

What was judged: render2/street.png (1600 x 1200, 6 m out, eye 1.6 m), enlarged in parts, against eleven photographs of twelve boxes (listed at the end), the target, PHOTO-CHECK.md and its 12 October addendum. The builder's Try 2 notes were read only after this view was formed.

Verdict: at street distance the box has the right shape and proportions and no build faults. It falls short only on narrow points, each a small detail with an exact fix. By the ruling of 9 October that is a PASS, with the points below for the builder.

## First: the picture misstates the box (the render tool's fault, not the box's)

The street picture shows the box standing 150 mm too tall, with a black base 450 mm high. The cause is the render tool (kit/tools/review_render.py, `context`). It lays the pavement at the model's lowest point, `min(lo.z, 0)`, and that point is the bottom of the hidden skirt at z -150. So the buried skirt shows above the ground. In the picture the box looks 1650 tall, 4.2 times its width, and the black is 27 per cent of the height. In the game, standing at z 0, it is 1500 tall, 3.85 times its width, and the black is 20 per cent. The preview in production/previews (pillar-box-street-v2) shows the same error. I re-rendered the same camera with the pavement at z 0 (scratch: rev2street/g0/street.png; the box then spans rows 397 to about 800, against 397 to 852 in the given picture). Fix: set the pavement at z 0 for any piece with a buried skirt, and redo the street and close previews before Jafar sees them.

## Narrow points, worst first (none is a fault of shape or proportion)

1. **The cap's rim band is plain; every photograph shows a row of cast dentils on it.** Where: the red band at the top of the box, the brightest line in the view. The photographs show a band of small rectangular blocks with dark gaps between them, running right round the rim on its upright face, just above the lower bead. They read at street distance as a dotted dark line. See P1 and P2 (the cap), Rhayader, Chester and Ballymena. By my estimate from preview-sized photographs there are about 60 blocks round the rim, about 16 wide and 20 tall at a pitch of about 28, with gaps 4 to 6 deep. Whose: the target's, which has no dentils. The builder's notes defer them to a normal map "on the underside", but the photographs put them on the band's face. A normal map there is enough at this distance.
2. **The small "next collection" tablet above the slot is missing; every Elizabeth II and George VI box in the photographs has it (eleven boxes).** Where: between the collar ring and the slot's hood. The photographs show a small framed window, about 40 x 30 in a frame of about 55 x 45. It sits centred or a little to one side, under the collar (P1, P2, Chester, both Alresford boxes, Rhayader, Ballymena, Shanklin, Outwood Lane, Quayside, Presteigne). At this distance it reads as a small pale or brass square over the slot. Whose: the target's ("not modelled, the research: uncertain"). The photographs settle it: the tablet's frame is cast into the box, so it was there in 1990, whatever the tablet then showed. The builder says the 17 mm gap is too small. Set the tablet into the hood's upper face, or lower the hood's top lip to make room.
3. **The slot's surround is too thin to read as a raised frame.** Where: round the dark slot under the cap. The build has a 30 mm projecting lip over the slot, a frame round it only 10 wide and 3 proud, and a sill 8 proud. At 6 m the slot looks cut into the body with a ledge above it. On the shallow pattern (Chester; Alresford, the right-hand box), the slot sits in a raised frame about 300 x 110 overall. That frame's side and bottom borders are about 20 to 25 wide and stand about 12 to 20 proud, under a heavier top, so it reads as a raised oblong with clear shadow lines. P1, P2, Outwood Lane and Alresford's left-hand box have the deeper box hood with side cheeks, which the builder set aside as the older pattern. That choice is fair, because both patterns were in the street in 1990. Fix: widen the frame's borders to about 22 and raise the frame and sill to about 12 to 15 proud. Whose: the target's (a 30 mm hood and no frame), plus the earlier review's frame size, which the build followed faithfully.
4. **The lock hardly shows.** Where: the right-hand side of the door, a little above half-height, where only a faint oblong outline is visible. In the photographs the escutcheon is a distinct raised oblong with a keyhole and a knob or lever under it, readable from across a street (P2 most clearly; also Presteigne, Ballymena and Chester). Fix: stand the escutcheon about 8 to 10 proud (now 3) and give it a handle about 25 across and 15 to 20 proud (now a 24 x 6 lever, 7 proud). Whose: the target's sizes.

Noted, not a fault at this distance: the plate frame stands 9 proud, where the photographs' frames look a little deeper (P1). The plate's top is 45 under the slot, where the photographs show 10 to 25 (P1, P2, Chester). Neither would be seen from 6 m.

## What is right

- **Proportions**, with the pavement at z 0: 1500 tall on a 390 body (3.85; P1 and P2 measure 3.68 to 3.98, and the other photographs agree by eye). The cap is 535 across (1.37 times the body; the photographs show 1.31 to 1.43). The slot's middle is at 0.85 of the height, and the slot is 0.64 of the body's width. The black base is 300, or 0.20 of the height (the photographs show 0.17 to 0.27), and is the body's width with a small rolled top, with no splayed foot.
- **The cap's order** reads like the photographs: a collar ring just over the slot, a deep concave flare out to the rim, an upright rim band and a low dome. Its overhang and outline match Ballymena, Chester and P2 seen at about the same size.
- **The front:** an upright collection plate centred under the slot, a white panel in a red frame, and a flush door with a visible joint, hinged on the left with no hinge showing. The lock is on the viewer's right, where every photograph has it. The cypher and lettering areas are flush and blank, as instructed.
- **The kind of colour:** red paint above a black base, with a white enamel panel and nothing metallic. The final gloss and wear belong to the engine.
- **Construction:** no faceting on the cylinder, cap or base edges. No gaps, floating parts or doubled faces show when the cap, slot, lock and base are enlarged. The check file agrees: every object is closed and no faces overlap in one plane.

## The photographs

Given: P1, geograph.org.uk/photo/3094819, Plymouth, taken 15 Aug 2012, CC BY-SA 2.0. P2, geograph.org.uk/photo/1428625, Bridlington, taken 25 Jul 2009, CC BY-SA 2.0.

Found by this review through Geograph's search feed (all CC BY-SA 2.0; taken dates from the feed):
- geograph.org.uk/photo/6913118: George VI box, Castle Street, Ballymena, taken 27 Jul 2021.
- geograph.org.uk/photo/1482931: George VI box, Undercliff, Shanklin, taken 13 Jun 2009.
- geograph.org.uk/photo/6499607: Elizabeth II box, Outwood Lane, taken 2 Jun 2020.
- geograph.org.uk/photo/5410937: Elizabeth II box on a quayside (TF1018), taken 31 May 2017.
- geograph.org.uk/photo/4657913: George VI box, Broad Street, Presteigne, taken 2 Sep 2015.
- geograph.org.uk/photo/2337761: Eton High Street, taken 24 Aug 1986. This is the only photograph before 1995 that the feed gave for a pillar box. It is a Victorian hexagonal box, so it was not used for shape; it does confirm a black-painted base in 1986.

I also opened the three that PHOTO-CHECK's addendum names, to test the builder's "shallow lip" pattern: Rhayader (2401662, 2011), Alresford (3114422, 2012) and Chester (6307696, 2019), all CC BY-SA 2.0. They bear it out: the shallow raised-frame pattern is real.

No photograph of an Elizabeth II or George VI box dated 1975 to 1995 was reached. I tried nearly 40 searches on Geograph's feed, filtered to dates up to 1996. Wikimedia's API answered 429 (rate-limited), and archive.org's search had none. All the castings shown are of the patterns standing in 1990, but their paint is that of the year each photograph was taken.
