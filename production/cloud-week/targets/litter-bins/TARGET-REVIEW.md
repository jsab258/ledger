PASS (on narrow points only: 14 points for the builder, none blocking; the first three must be applied before the build is judged)

# Litter bins and dustbins: fresh review of the target (cloud week 42, 12 October 2026)

Reviewed: TARGET.md, target.json, target_drawing.py, self_check.py, make_target.py, litter_data.py and the two previews, against REVIEW-BRIEF.md and BRIEF.md. This was the one review round allowed, so it fails only what would make the build look wrong or break a rule. Nothing does that, because every fault below has an exact fix. Jafar's ruling of 9 October makes that a PASS. The points are ordered worst first.

Re-run: self_check.py, run in a scratch copy with the files it reads, gives `SELF-CHECK litter-bins: 139 checks, 139 passed, 0 failed, 9 reported`, the same as the writer's result. The drawing runs inside it (group 5). The result is honest about what it covers, but three of its passes prove less than they say (point 9).

## Faults and narrow points, worst first

**1. K1's bin runs into its own post and bracket (an internal clash, so the builder cannot build it as written).**
Where: target.json `kinds.K1.bin.axis_offset_x` = 216, `kinds.K1.bracket.back_strap` (x 38.05 to 43.05, z 590 to 1030) and `clamps` (rings r 38.05 to 43.05).
What the numbers give: the bin's back wall stands at x = 216 - r(z). That is x 50.0 at z 590, which leaves a 7 mm gap behind the strap, so the strap touches nothing. It is x 43.2 at z 800, already at the strap. At z 980 it is x 37.4, inside the upper clamp and the post tube. The rim bead (r 186.5 at z 1046) reaches x 29.5, which is 8.5 mm into the 76.1 post. The tapered bin cannot touch a vertical post along a flat 5 mm strap. Self-check group 4 does not test this.
Fix: set `axis_offset_x` to **232** (bead r 186.5 + post r 38.05 + 7 clear). Make the back strap a **tapered spacer bar** 40 wide: its post face is flat on x 43.05, its bin face follows the bin wall (x = 232 - r(z)), so it is **21 thick at z 640 and 10 thick at z 980**, welded to the bin along its length. Change these to match: check `K1_bin_offset` to 232 +-10; `extent.x` to [-38.05, 418.5]; placements B1 `bin_axis_x_m` to 6.368 and B2 to 35.432. The z set-backs do not change, because the bin hangs along the street.

**2. D1's three horizontal swaged ribs are an American can's, not a British dustbin's.**
Where: target.json `kinds.D1.rib_z` [150, 290, 430], `rib`, and the matching bumps in `outer_profile_rz` (z 138 to 162, 278 to 302, 418 to 442). Its source is S7, Poly Haven's US-style can.
What the photographs show: none of the four British galvanised dustbins found (sources below) has mid-body horizontal ribs. Pentonville (2908276) and Chawleigh (1278296) have **vertical corrugations** over the body below a plain band. Chawleigh shows **two swaged rings just under the rolled rim**. Patterdale (5055396) has a **plain body** with one vertical seam and the foot hoop. Seen close up from the pavement, three evenly spaced horizontal ribs read as the American type.
Fix: delete the three ribs: profile straight from (199, 28) to (224, 582) with the taper kept. Add two rings under the rim, at z **530 and 556**, each 18 high and 4 proud and rounded. Then choose one of the photographed forms and write it down: (a) plain body (Patterdale), or (b) the recommended one, **vertical corrugations**: 64 flutes round the body (a pitch of about 21 mm at r 210), each 4 deep, rounded, from z 40 to z 515, fading out at both ends (Pentonville, Chawleigh). Change check `D1_rib_count_and_z` to `[530, 556]` +-10.

**3. D1's side handles are drawn as vertical loops; the photographs show horizontal grips.**
Where: target.json `kinds.D1.side_handles` ("a loop of 25 x 3 flat strip, 100 tall, standing 45 proud").
What the photographs show: Patterdale (5055396) shows a **horizontal round-bar grip** about 0.37 of the body's width long, on **two lugs, each held by two rivets one above the other**, at about two-thirds of the height. Chawleigh (1278296) shows the same horizontal grip on a lug, just under the rim rings.
Fix: `side_handles` = 2 at azimuth 90 and 270, centre **z 470**. Each is a **12 mm round bar, 170 long between lug centres**, its grip standing **38 proud** of the body, bent down at each end into a lug **25 wide x 55 tall x 3** with **two 8 mm dome rivets one above the other** (40 apart). Change check `D1_side_handles` to [2, 470, 38] +-[0, 25, 6]. The rivet count (four a side) does not change.

**4. K2's collar is drawn 11 mm too wide on the radius.**
Where: `kinds.K2.outer_profile_rz` points (231, 282) (230, 300) (230, 338) (224, 348) (214, 356); `parts.collar.r_max` 230; `photo_measurements.topsy_974902` collar row (x 62 to 210, 148 px); check `K2_collar_diameter` 460.
What the photograph shows (S12 original, 427 x 640, measured on 4x and 8x enlargements; brick module 51 x 17 px, so the pixels are square). At rows 436 to 452 the collar's silhouette runs from **x 70 to x 210.5**, which is 140.5 px, 434 mm, **r 217**. The writer's x 62 is the left edge at rows 457 to 465, which is already the shoulder flaring out to the base drum. The collar stands only about 9 mm proud of the body (r 208), not 20 mm. The overlay preview shows the gap: the cyan line sits outside the grey on the left side of the collar.
Fix: replace the points from (236, 262) to (210, 364) with **(238, 258) (228, 276) (221, 290) (220, 300) (220, 345) (216, 352) (211, 358) (210, 364)**. Set `collar.r_max` to 220. Set the photo row to x 70 to 210.5, 140.5 px, 434 mm, r 217. Set check `K2_collar_diameter` to **440** +-12. The order check in self-check group 3 still holds (247 > 220 > 218 > 210).

**5. K2's hood skirt is drawn ending about 15 mm too high.**
Where: `outer_profile_rz` (210, 640) (206, 648) (206, 658) (218, 664); `parts.join_groove.z` [640, 664]; check `K2_join_groove_z`.
What the photograph shows: the hood's lower lip is at rows 338 to 341 on both sides, which is **z 640 to 650** at 3.09 mm a pixel. The writer's own table has the groove at 630 to 650. In the photograph the skirt below the aperture is about 35 mm deep (sill to lip). The target leaves 16 mm (680 - 664).
Fix: **(210, 630) (206, 636) (206, 644) (218, 650)**; `join_groove.z` [630, 650]; `body.z` [364, 630]; `hood.z` [650, 900]. Change check `K2_join_groove_z` to [630, 650] +-10. The sill stays at 680, the lettering at 470, and the liner fits as before.

**6. K2 is missing how it meets the ground.**
Where: `kinds.K2.fixings` ("nothing is bolted to the footway").
What the photograph shows: the bin stands on a **ragged pale cement patch** set flush in the paving round its foot. The patch reaches about 40 to 90 mm beyond the base drum at the front, with a broken edge. This is where its ground fixing was set.
Fix: add `ground_patch`: an irregular flush disc, r 290 to 330 (seeded), 0 to 2 mm proud, sRGB (186, 184, 176), roughness 0.85. It is a separate mesh, or it goes in the footway decal set. Say the fixing is hidden, under the base.

**7. K2's "stickers" are not defined, and the target contradicts itself about them.**
Where: `kinds.K2.conditions.b.stickers` 2 and `c.stickers` 1, against the basis "No maker's mark, crest or sticker is modelled". K1 also has stickers 1 to 2.
Fix: define a sticker once, in `wear`. It is a weathered blank or illegible paper or vinyl rectangle, 60 to 120 mm across, with **no readable word, number, logo or crest**, and with no maker's or council sticker (S12's council crest is exactly what must not appear). Or set every count to 0.

**8. The photograph cannot settle K2's absolute size; the target should say so.**
Where: `photo_measurements.topsy_974902.method` ("the George V box ... at an assumed 1.5 m ... agree within 2 %"); self_check group 3's "pillar box reading (3.2) agrees within 4 per cent" uses a hard-coded 3.2.
What the photograph shows: the box beside the bin is 462 px tall and 101 px across its body, 4.6 to 1. The pillar-box target's Type A is 1500 by 489, 3.07 to 1. So the box in the photograph is not that type, and nothing establishes its height. The scale therefore rests on K2's own height of 900, which is a Judgement. The bin's proportions measure well (points 4 and 5 aside), but its absolute size is not measured.
Fix (words only): in `kinds.K2.basis` and `could_not_settle`, write "K2's height 900 is Judgement. S12 gives proportions only; the box beside it is of an unestablished type and height." In self-check group 3, mark the 3.2 line as "reported" instead of a pass.

**9. The self-check passes three things it does not test.**
Group 3 compares the profile with the writer's own pixel table, not with the photograph, so a misread (point 4) passes. Group 4 has no clearance test between K1's bin and its post, strap and clamps (point 1). The scale line is a hard-coded number (point 8).
Fix: add a group 4 test: for z 560 to 1050, `axis_offset_x - r_bin(z)` >= 43.05 under the strap and >= 38.05 + 3 everywhere, with the bead included. Add a group 3 note that the pixel table is the writer's reading and was checked by a reviewer on 12 October.

**10. A stale figure.** `could_not_settle` (TARGET.md line 1468) says "K2 aperture sill 0.65"; the data says 680. Fix: write 0.68.

**11. The period claim for S12 is stated more firmly than it is known.** `sources.S12.period` says "its form is read as unchanged". Nothing reached shows a 1984 to 1990 example: the leads give a date, not a form. The photographed bin may be a later generation of the type. Fix: write "assumed unchanged since the 1980s; no period photograph of the type was reached". This is already the sense of `could_not_settle`, so it is wording only.

**12. D1's lid: one photograph shows radial ribs.** Cusop (3757342) shows a lid lying on the ground with **pressed radial ribs**. Fix: add `lid.radial_ribs`: 20 ribs, 12 wide, 3 proud, from r 70 to r 225 on the dome, the strap handle across the crown kept. This comes from one low-resolution photograph, so mark it "Photo, one example".

**13. A product name in the builder's input.** The key `photo_measurements.topsy_974902` names a maker's product. Leads may name makers; a key the build script reads should not. Fix: rename it to `s12_974902`, in self_check.py too.

**14. Wording only.** B3 "serves ... the chandler's queue", but the chandler is on the east side (shopfronts target, x 40 to 46 east) and B3 is on the west. Fix: drop the phrase.

Colour, recorded and not a fault: S12's bin is charcoal grey gelcoat. K2's council green is Judgement, and the target says so. Keep it.

## What is right

- **K2's form is what the photograph shows**, except points 4 and 5. Re-measured on the original from Geograph, with the writer's scale (row 548 = z 0, 3.09 mm a pixel), against the target:

  | part | photograph | target |
  |---|---|---|
  | hood skirt | r 214 | r 218 |
  | body | r 208 | r 210 |
  | collar | r 217, z 287 to 355 | r 230, z 300 to 364 |
  | shoulder | z 250 to 287 | z 236 to 300 |
  | base drum | r 244, z 0 to 250 | r 247, z 0 to 236 |
  | aperture | about 90 to 100 high, sill about 680 to 690, rounded ends, on one side of the hood | 105 high, sill 680 |
  | dome shoulder | starts at z about 820 | starts at z 822 |

  The stepped drum is the right reading and the first try's form was wrong: the base drum is the widest part, there is a narrow collar, a plain body, a lipped hood with its slot, and a flat shallow dome. The overlay preview shows it, except the collar's left edge. The photograph's pixels are square: it is cropped from 2112 x 2816, not squeezed, and brick module 51 x 17 px = 3.0.
- **S12 checks out at its page:** Geograph 974902, "Litter bin and postbox, Wilton Road", Jim Champion, taken Sunday 21 September 2008, CC BY-SA 2.0, SU4014, Southampton. The caption says the slot on the left is for litter and the one on the right for mail. The crop cuts away the George V box with its GR cypher and POST OFFICE lettering and masks the council crest sticker. No shop name, child, alcohol or gambling is in either preview. Both previews are under 300 KB and 1200 px.
- **K1 and D1 are honest about being judgement.** K1's basis, every K1 number and the `could_not_settle` list say there is no photograph. D1's sizes are the scene's Read 0.46 x 0.61 and lid 0.50 x 0.05, the period's 18 x 24 in.
- **D1's proportions fit the photographs.** The four dustbins found have a body about 1.3 to 1.37 times as tall as it is wide; the target has 610 / 463 = 1.32. They also show the rolled rim, the foot hoop, the lid's central strap handle, the single vertical seam (Patterdale), and the painted house number (Pentonville shows a hand-painted "45", just as D1's optional stencil). Only the ribs, the handles and the lid ribs differ (points 2, 3 and 12).
- **K1's heights fit the one post bin found.** Maesteg's "old-style" post bin (4229090) hangs on a single post from about 0.45 to 0.5 m up to about 1.0 m, and carries LITTER as its only word. K1 hangs from 0.55 to 1.05 with LITTER only. That bin is a closed cylinder with a top and a front slot, not an open top. It is the only post-mounted bin of an older pattern found, and it does not show K1's form wrong. It does show that a closed post bin also existed. K1 stays Judgement, as it says.
- **The content rule and canon are kept.** LITTER and digits are the only words. There is no maker, council, crest or cypher on any part. The dressing excludes alcohol (soft-drink cans and pop bottles only, "never beer, lager or cider"), gambling and child-related objects. Tobacco is kept, which canon allows. Britain 1990, no wheeled bins, no 2000s street furniture placed (S2 to S6 were rejected as modern). The council's name is left to canon.
- **A builder can build K2 and D1 from target.json alone, and K1 once point 1 is applied.** The profiles are closed lathe outlines, and the shell, aperture, liner, lock, lettering, conditions, materials (sRGB, roughness, metal), wear (agreeing with the wear target), dressing sets, triangle budgets and hand-over names are all present.
- **The placements agree with the street's own files.** B1 at x 6.6 east: 1.4 m from LC1, clear of Mickey's door leaf by 0.95 m. B2 at x 35.2 east: 2.73 m from the grocer's door, with the grocer on the east side as the shopfronts target says. B3 at x 44.0 west: 2.82 m from the newsagent's side door (newsagent on the west, x 36 to 42) and 2.0 m from the cast's bus stop at (46.0, -4.3). Every bin leaves 0.92 to 1.17 m of walking strip and 0.25 m or more from the kerb back. The dustbins keep the scene's E13 line (21.4 and 22.0 east, set back 1.6 m) with their convention stated. Taking out the scene's three E6 bins (8.0 east, 30.0 east, 33.0 west) still gives the west shops a bin (B3), as the scene's 22 September line meant.

## Photographs and sources judged against

All were reached on 12 October 2026 through Geograph's syndicator feed, with each image and S12's page fetched with a user agent naming only the project. All are CC BY-SA 2.0. They were used for measuring and judging only. None was copied into the repository.

- **S12**, geograph.org.uk/photo/974902, "Litter bin and postbox, Wilton Road", Jim Champion, taken 2008-09-21. A hooded glass-fibre bin, the period type in a later example. The page was read for licence, date and caption, and the original 427 x 640 was measured.
- geograph.org.uk/photo/2908276, "Northdown Street, Pentonville", Stephen McKay, taken 2012-04-20. A galvanised dustbin with a vertically corrugated body, a lid with a central handle, a side handle near the top and a hand-painted house number.
- geograph.org.uk/photo/1278296, "Church dustbin, Chawleigh", Tom Jolliffe, taken 2009-04-29. A galvanised dustbin with vertical corrugations, two swaged rings under the rim and a horizontal side grip.
- geograph.org.uk/photo/5055396, "Mossy bin, Patterdale", Karl and Ali, taken 2016-07-29. A plain-bodied galvanised dustbin with a vertical seam, a horizontal bar grip on two double-riveted lugs, a foot hoop and a lid handle.
- geograph.org.uk/photo/3757342, "4 dustbins in Cusop", Jaggery, taken 2012-06-10. Four galvanised dustbins and a lid with radial ribs. The caption says dustbins "have been replaced by wheelie bins in many parts of the UK. These survivors ...".
- geograph.org.uk/photo/4229090, "Yellow litter bin on a river footbridge in Maesteg", Jaggery, taken 2014-10-30. The caption calls it "the old-style bin": a closed post-mounted cylinder with LITTER on a plate.
- geograph.org.uk/photo/4285959, "Jedburgh, High Street 1989", Ben Brooksbank, taken 1989-03-25. A dated 1989 street litter bin: free-standing, faceted, brown, about waist high, at the kerb by a lamp column. It is neither a pole bin nor a drum, which shows that period stock varied by council, as the target's leads say.
- Why the later photographs count for the dustbins: galvanised dustbins stopped being bought when wheeled bins came in (late 1980s to 2000s), so those still standing in 2009 to 2016 are period stock, as the Cusop caption says. The Maesteg bin is called old-style by its photographer, but its date is not known.
- Looked at and not used: 5022565, 3540953, 1162753, 602460, 4202743, 4261883, 1684746, 2877032, 5555558, 3684525, 3132365, 1569563 and 4941394 (modern or square bins, no pole bin of an older pattern), and twenty-two Geograph street photographs taken 1989 to 1991 (Winchester, Croydon, Lincoln, Purley, Staveley, Putney, Holborn, Northallerton, Dumfries, Holt, Johnstone, Hull, Manchester, Earlston and others), in which no bin was legible except Jedburgh's.
- Searches: Geograph's feed for "litter bin", "litter", "bin", "dustbin", "rubbish", "street furniture", "high street" and "shops" with takenyear 1989, 1990 and 1991, and with no year for "litter bin lamp post", "litter bin lamppost", "litter bin post", "post mounted litter bin", "pole mounted litter bin" (none returned), "hooded litter bin", "old litter bin", "metal dustbin", "galvanised dustbin" and "dustbin". **No photograph of a pole-mounted or lamp-column-mounted open steel bin was found, and none of a hooded drum from 1975 to 1995.** Wikimedia Commons answered one search with nothing relevant and was not pursued further.
- Repository files: production/specs/vignette-scene.json (E6, E13), production/specs/hook-cast.json (bus stop), and the shopfronts, lamp-posts, bollards, kerbs-and-covers and pillar-box target.json files.
