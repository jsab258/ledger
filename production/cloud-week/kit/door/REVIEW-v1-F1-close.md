PASS

Fresh review, cloud week 42, piece 3.1 front door, variant F1, view "close" (the lock rail and the ironmongery from about 1.2 m), build v1. Renders judged: door-build/v1/F1/close.png and close_plate.png (1600 x 1200). Photographs: P2 door-photo-02-tottenham-six-panel-black.jpg (675 x 1200) and P1 door-photo-01-teignmouth-four-panel-red.jpg (480 x 640), judged on these copies only, since their source pages cannot be reached from this cloud. Coordinates are pixels in those files. Scale on the render is about 1.65 px/mm at the leaf face (the stile and the 37 mm cylinder) and 1.70 px/mm at the frame face (the 22 mm keep). On P2 it is 2.317 mm a pixel, the target's figure.

Nothing a player would see as wrong at this distance. No holes, gaps, floating parts, overlapping faces or faceting were found. Below are narrow points, worst first, each to be fixed before the next build.

## Notes (narrow points, worst first)

1. **The cylinder's keyway is horizontal; P2's is vertical.** In close.png the slot is a horizontal dash across the plug at (963, 440). P2 shows the keyway as a dark vertical streak in the plug at x 488-489, rows 497-500 (values 100/98, 64/24, 15, 76 inside a bright ring). That is about 1-2 px by 4 px, roughly 3 x 9 mm upright, which is the usual way a British rim cylinder is fitted. **Target's fault:** target.json `ironmongery.cylinder_lock.keyway` says "horizontal slot", and the build follows it. T1's build already cuts the vertical 3 x 9 slot, so F1 should take the same.

2. **The keep on the jamb face has no basis in P2.** It is a black 22 x 73 box with an 8 x 50 slot on the right jamb at (1080-1118, 527-650), and it is prominent in this view. P2's right jamb at the keep's height (rows 515-547, x 508-530) is bare painted timber with only the bead line. The target's reason, "P2 has a grey service box on the jamb at this height", misreads P2: that box is at rows 293-370, which is 1.33-1.51 m up and not 0.93-1.0 m. The object is copied from P1, whose target already says it may be a bell push. A keep on the outside face of the stop cannot take the latch bolt of an inward-opening door. **Target's fault.** Drop it from F1, or specify it as a period bell push. It reads as a small dark fitting, not as an error.

3. **The leaf shows no rail, stile or muntin joints.** The muntin runs into the lock rail, and the lock rail into the stile, with no line at all:
   - column 400, rows 600-720, is flat at 45-46;
   - row 850, x 860-1035, is a smooth gradient.

   P2 shows these joints as thin lines between the moulding feet, at rows about 648 and 733 across the muntins (x 313-353). The build's header says it left the joints closed on purpose. The target asks for "paint-bridged hairlines 0.4 mm, dark in the 1990 wear mask", so this is within the target. **Build's, deferred to the engine:** the wear mask (or a normal-map line) must carry the lines. Without them, at arm's length the leaf reads as one seamless slab.

4. **The plugged keyhole's outline and tones.** In close.png at (982, 245-295) it is a light-bulb shape: the round head joins the slot by straight diagonal shoulders. Inside it is a dark blank with a brass dot in the head. P2 at (493, 447) shows a round head over a parallel slot, with the head dark and the slot holding a pale metal blank. **Build's** (the target says only "keyhole-shaped dark recess with a small metal blank"). The fix is a circle over a parallel slot, with the blank in the slot.

5. **The cylinder collar's knurl.** In close.png at (933-995, 417-478) the collar has 12 sharp V-notches with flat lands between them, which reads as a gear or a bottle cap. P2's ring (at 476-502, rows 483-508) shows fewer, rounder scallops, about eight, and a rounded rim that catches light on its upper left. At 16 px across this cannot be settled. **Target's** (12 serrations) and unsettled: rounding the notches into scallops would sit closer to the photograph.

6. **The letter plate's screws.** close_plate.png has four domed screws at the plate's corners (around 742/855, 440/862). P2's plate (x 293-376, rows 281-311) has no corner screws. It shows two round bosses at the ends of the flap, in its upper third: these are the flap's pivots. P1's plate shows no screws. **Target's** misreading of P2. The screws are seated and plausible, but they are not what P2 shows. P2's flap is also framed by a bold round-section rim, while the render follows P1: a near-flat rim face (rising 2 mm over 13.5) with a sharp aperture edge and the flap recessed behind it. Both are period forms.

7. **The knob's rose barely reads.** Dark steel round a dark knob, it shows only as a dark band on the knob's right at x 437-463 in row 850. In P2 the recess shows as a distinct ring with a lit rim around the knob (x 316-349, rows 675-712, 33 px = 76 mm). **Build's or the material's;** the geometry is present. Check it again once final materials are on.

8. **No groove between the frame and the pilaster.** Context only: the jamb strip runs straight into the render's return at x 1129. P2 has a dark groove of 5-7 mm there, which target section 7 lists. This belongs to the surround and the assembled scene, not to the piece.

## What is right

- **Placement matches P2 and the target to a millimetre or two:**
  - The cylinder centre is 77 px (about 47 mm) from the stop edge; the target says 46.3, and P2 gives 20 px = 46 mm.
  - The keyhole is 35 mm from the stop edge and 111 mm above the cylinder; P2 gives 48 px x 2.317 = 111 mm.
  - The cylinder sits at about v 1040, where P2 gives row 495, about v 1035.
  - The knob is on the leaf's centre line, at the middle of the lock rail's visible height (rows 677-1027, centre 852; knob 790-910), as P2's knob sits in the middle of its lock rail.
- **The knob** is a turned beehive with five V-cut rings and a small brass cap. The rings match P2's period (about 3.5 px, or 8 mm, giving five rings to the radius), and the knob is 69 mm inside a 76 mm rose, nearly filling it as in P2. The silhouette is smooth, the black-painted iron is the right kind, it is seated in its recess, and nothing floats.
- **The lock rail is plain:** no band, no weatherboard, as P2.
- **The bolection mouldings** at the lock rail are right:
  - the outer nose casts a crisp shadow line on the rail, from row 670 down to the darkest point at 676;
  - a convex bead (lit at rows 658-669) leads into a bold bevel that falls to a flat field;
  - the moulding is about 42 mm on the face (rows 610-677), against P2's 18.5 px = 43 mm;
  - the mitres are tight, as in P2.
- **The frame** is a flat, square-edged face, about 49 mm showing. It has the planted quarter-round bead at the stop edge (P2's light line) and no ovolo. The stop's side face shows as a narrow strip, consistent with the camera's offset.
- **The letter plate (close_plate)** has P1's proportions:
  - the aperture is 0.63 of the plate's width, and the margins are 21 mm at the top and 29 mm at the bottom (target 22/30);
  - it is vertical on the muntin;
  - the outer edge is chamfered and the flap recessed, with its lifting lip at the foot;
  - nickel or chrome in kind, as P2's plate.
- **The cylinder** has a knurled nickel collar 2 mm proud, set in a bored hole with a dark relief ring, and the plug sits behind the collar.
- **Edges and fixings:** the leaf's arrises are eased and the frame's are square. No visible screws on the cylinder, keep or mouldings, as the target says. No faceting on any round part (knob, rose, plug or screws).
