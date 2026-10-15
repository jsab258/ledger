FAIL

# Front door 3.1, T1, view "close" (v1): fresh review, 9 October 2026

Judged: `close.png` (the lock rail and the ironmongery from about 1.2 m) with its companion `close_plate.png` (the letter plate), against P1 (Teignmouth, red four-panel, the model) and P2 (Tottenham, black six-panel, the cross-check). The previews were cropped and enlarged with PIL. The Geograph and Wikimedia source pages can't be reached from this cloud, so nothing here rests on them. Scale on P1 at the leaf's plane is 5.19 mm a pixel (the target's wall-plane 5.03, corrected for the leaf being 188 mm deeper; it gives the 772 between the stops as 150 px, which P1 shows). Scale on the close render at the leaf is 1.61 px a mm (from the 43.5 mm cylinder). The brick, quoins and reveal returns are context and are not judged.

## Faults, worst first

1. **The cylinder lock is a flat brass coin, not a cylinder.**
   - **In the view.** The brass disc on the lock stile, upper right of `close.png` at about (943, 333). It stands 1.5 mm proud with a 0.9 mm bevel. The tone is even across its face, the outline is a thin dark line and the plug is an engraved circle. At this distance it reads as a flush round escutcheon or a sticker. It does not read as the rim cylinder of a night latch, which is the view's main piece of ironmongery.
   - **What P1 shows.** At (258.75, 290.3) the cylinder has a bright crescent along its upper-left edge (rows 286-288, luminance 142-153 against the door's 110-118). Along its lower edge there is a dark crescent (row 293, luminance 62-92). This is the shading of a rounded collar standing proud of the door, lit on top and shadowed or reflecting the ground below. A flush disc would give an even ring all round.
   - **What P2 shows.** At (488, 495) the collar stands clearly proud of the leaf, with its side lit and a shadow to its lower right. That is F1's knurled variety, but it confirms the period type.
   - **Whose fault.** The target's. `ironmongery.cylinder_lock` gives "flush cylinder lock", `collar_proud_mm` 1.5, and says "Collar and keyway Judgement". The build follows it exactly (`build_cylinder`, T1 branch).
   - **Fix.** The target should give the collar a projection and a rounded or chamfered front edge, set from a measured source (P1 is too small to measure it; its crescents are about 1 px, 5 mm). The plug's face should sit with the collar's front. The build then follows.

No other fault rises to FAIL at this distance. The narrow points are under Notes.

## What is right

- **Lock position and size match P1.**
  - Centre 46.6 mm from the stop face: P1 is 9 px from the frame edge, which is 47 mm.
  - Centre about 377 mm above the band's top: P1 is 73 px, which is 380 mm.
  - Collar 43.5 mm across: P1 is 8.4 px, which is 43.6 mm.
- **The jamb plate matches P1's dark plate.** It is 22 x 72.6 mm, set just right of the jamb's centre and 88 mm lower than the lock. P1's plate is cols 273-277, rows 300.3-314.4, 86-88 mm below the lock. The render's plate stands about 92 mm below, which is the camera's perspective.
- **The lock-rail band reads as P1's.**
  - It has three rounded crests with dark coves between. P1 has three highlights at rows 365.5, 370.5 and 374.5, with creases at 367.5 and 373, under a rounded top.
  - Its square underside throws a crisp shadow line, as P1's rows 378-386 do.
  - It sits 35 mm below the upper panels' moulding. P1 shows 6.5 px, which is 34 mm.
  - It stops cleanly at the stops, as in P1.
- **Frame.** Flat, square-edged and white, with no ovolo and no bead, 55 mm showing as in P1. The leaf sits 74 mm back behind the stop, whose edge face shows as the thin 5 px strip that the geometry predicts.
- **Panel mouldings.**
  - The bolection mitres are closed and crisp at all four corners in view.
  - The profile reads as a raised nose over a falling S-curve to a flat, recessed panel. The bottom moulding's shading runs bright, dim, then bright, close to P1's rows 346-357.
  - The muntin's flat is about 106 mm (P1 20-21 px, 104-109 mm).
  - The lock stile's flat is 88 mm (P1 16-17 px, 83-88 mm).
- **Letter plate (`close_plate`).**
  - Vertical on the muntin and centred on it, 76 x 242 mm. The 3.2:1 proportion is P1's (14.65 x 46.9 px).
  - The aperture is 48 x 190 mm with margins of 23 mm above and 30 mm below. P1 shows about 21 mm and 25 mm.
  - It has a recessed sprung flap with a lifting lip at the foot.
- **Nothing outside that the photographs lack.** There are no hinges, knocker, bolts or screws on the outside.
- **No build faults at 3x to 8x enlargement.** There are no holes, gaps, overlapping faces or floating parts, and no faceting. The cylinder, band, moulding curves and the flap's dish are smooth.

## Notes (narrow points, not seen as wrong at this distance)

- **Moulding width (target's, possible).** P1's four bolection mouldings read 9-10 px between their outer and inner dark lines (cols 134-144, 173-182, 203-212, 241-251). That is 47-52 mm at the leaf, or about 41 ±7 mm once the occlusion lines are allowed for. P2's mouldings give 43 mm. The target's 36 (from Riley, and "P1 34 ±8") sits at the narrow end. The target should re-measure; 40-42 mm may be nearer both photographs.
- **Letter-plate rim (build's).** The target asks for a rim "chamfered 45 degrees from 6 mm at the aperture edge down to the backplate". The build instead gives a 2 x 1 chamfer at the outer edge, then a shallow rise of about 10 degrees from 4 mm to 6 mm at the aperture. At 1 m this barely shows. The plate reads as one flat slab rather than a bevelled frame, so a true 45 degree bevel would read closer to P1's lighter border.
- **Metals' kind.**
  - P1's cylinder face is a dull grey-olive (luminance about 110-130). That is darker and greyer than its pale-brass letter plate (about 200), which suggests a nickel or darkened finish, not the same brass as the plate.
  - P1's jamb plate is mid-dark grey (about 100 against the jamb's 245). The render's plate is near black.
  - These are for the engine's materials; the form is right.
- **Jamb plate's identity (target's open question).** P1 can't tell a box keep from a bell push. As drawn, a black plate with a recessed slot is plausible at this distance. A keep on the outside face of the frame serves no latch, though, so if the town wants a working object it should be a bell push.
- **Rail and stile joints (build's).** The target asks for 0.4 mm hairlines. The build closes them on purpose ("so the stile-rail joints stay closed"). At 1.2 m a 0.4 mm line is about 0.6 px and doesn't show. P2 shows a faint line across the muntin's foot, so it is worth a normal-map line in the engine.
- **Keyway.** The keyway is a plain 3 x 9 mm slot with a small step at the top. At 1.2 m it is about 14 px, so it reads as a slot. A profiled (wavy) keyway would hold up better if the player goes nearer.
- **House numerals.** These are optional in the target and absent here. P1's "69" sits on the muntin inside this view's frame, so if the town uses numbers they will be seen in this view.
