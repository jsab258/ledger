PASS

# Kerbs and drain covers: target review (cloud week 42, 9 October 2026)

Fresh reviewer; I did not write this target and will not build it. The target holds up. Everything that shows most from the street matches my own measurements from the 8k panoramas: the granite kerb's section, top width and block lengths, the two-course sett channel, the crossover's form, and the gully grate's size, position, slot count and pitch. I found no fault that fails the target. I found eleven narrow points, each a small detail with an exact fix (Jafar's ruling of 9 October), listed worst first.

**Before unit 3.7 builds:** points 1 and 2 must go into target.json, together with its `checks` and the drawing that is made from it. As written, the checks `gully_grate_slots` (slot 18 +-2) and `cover_stud_square` (8 x 8 studs, outer 860) enforce the error, so they would reject a piece built correctly.

## How I checked

* Read: BRIEF.md, REVIEW-BRIEF.md, canon.md, RULINGS.md, SCENE-SLOTS.md (Kerb, Gully grate, Road rows), the wear target's surfaces, gutter_grime, grate_wear and places entries, and the asset plan's kerb and cover rows (3-FURNITURE-PROPS-FOOD.md, lines 113, 114, 182 and 183).
* Sources reached on 9 October 2026: api.polyhaven.com files and info for urban_street_01, 03 and 04, bethnal_green_entrance, birbeck_street_underpass and metal_grate_rusty; the 8k tone-mapped JPGs downloaded; polyhaven.com/license read (CC0). The authors and dates in the info records agree with TARGET.md (urban_street_03 taken 2019-09-07 07:46 UTC, bethnal_green_entrance 2019-08-18 07:01 UTC; metal_grate_rusty is "a rusty metal grate, with raised tread pattern", 500 x 500 mm).
* Refused from this cloud (I re-tried them, every one returned 000): Wikimedia Commons, Geograph, Flickr, archive.org, gov.uk and the BSI site. What this limits: I could not check the target against any 1975-2000 photograph, against BS 497 grating sizes or BS 435 and BS 7263 kerb sections, or against the Department's tactile-paving guidance. My review tests the target against the same 2019 London panoramas it used, nothing older.
* I re-projected the panoramas with my own code (scratch only) at 1.5 mm a pixel: the ground plane (camera 1.6 m) and the kerb-top plane (1.475 m) of the main crossing frame, telephoto views of the grate, the kerb ends and the footway cover, the Bethnal Green cover, the urban_street_04 cover, the Birbeck grate, the east-side kerb run and the urban_street_01 corner. I also measured on the writer's own previews.
* Scale proof: the yellow line reads 76 to 82 mm on my ortho, about 75 to 80 once its 1.8-degree slant is allowed for. So the 1.6 m camera height holds to about 5 %.
* I ran `target_drawing.py` and `self_check.py` on a scratch mirror of the repository: 16 views and two overlays drawn; SELF-CHECK PASS, 155 of 155. Nothing in the repository was edited by me except this file.

### Re-measured numbers (mine against the target)

| what | target | my reading | verdict |
|---|---|---|---|
| granite kerb top width, face foot to the rear joint (right end block, two column bands) | 190 +-15 | 193 and 201 | right |
| arris middle behind the foot (batter) | 25 (PM26: 29) | 28.5 | right (but see point 8) |
| arris-middle ray, read as a vertical face | (PM01, PM02: 113, 118) | 129 and 133 | the model's 125 with a 25 batter fits it |
| block lengths on the east-side run | 800 to 1200 (PM04: 837, 1011, 1143) | about 830, 1050, 1130 | right |
| channel courses across | A 115, B 110 | A 112 to 115, B 105 to 110 | right |
| channel width, foot to the far edge of course B | 225 | 225 in front of the crossing; 180 to 195 where the asphalt laps over course B | right (see point 9) |
| grate A slots, count and pitch | 8 at 57 | 8 (the fifth under a leaf) at 56.8 to 57.1 | right |
| grate A slot length / across | 285 / 325 | about 278 / about 336 (+-10, radial blur) | right |
| grate A along the kerb | 485 +-10 | 466 to 478 (end walls soft) | right, just |
| **grate A slot width / bar width** | **18 / 39** | **28.5 to 30 / 25.5 to 28.5** | **contradicted (point 1)** |
| **Bethnal Green stud cover: studs, outer, leaves** | **8 x 8, 860, one lid** | **10 x 10, about 980 x 920, two triangular leaves** | **contradicted (point 2)** |
| **mitred corner angle** | **112** | **132 to 136** | **contradicted (point 5)** |

## Faults

None: nothing that fails the target.

## Narrow points, worst first, each with its exact amendment

1. **Gully grate A: the slots are drawn too thin and the bars too fat** (urban_street_03, the grate in the main frame; the writer's own `ph-urban_street_03-gully-grate-ortho.jpg`). At half level on the writer's preview, the black slots are 25.5 to 34.5 mm wide (median 28.5) and the bars 24 to 28.5. On my 1.5 mm ortho of the 8k panorama they are 25.5 to 31.5 (median 30) and the bars 25.5 to 28.5. In the photograph the slots are about as wide as the bars; the target gives slot 18 and bar 39, so its grate reads two-thirds iron. The writer's own overlay (`ph-urban_street_03-target-on-photo.jpg`) shows the cyan slot boxes narrower than the black slots. The cause is PM14's slot field: it was read as 278 px (first slot's left edge 6 px from its centre), but on the writer's preview it is 289 px (columns 170 to 459), which is 433 mm. Amend `pieces.gully_grate_A` as follows:
   * `slot_width` 29 (`slot_taper`: 29 at the top, 25 at the bottom)
   * `bar_width` 28
   * `slot_span` 428 (7 x 57 + 29)
   * `end_wall_along` 28.5
   * `slot_centres_x` unchanged
   * PM14 raw readings corrected to field 289 px; slot widths 25.5 to 34.5; bars 24 to 28.5.

   Amend `checks.gully_grate_slots` width to 29 +-4. Add a check `gully_grate_open_fraction`: slot area over the grate's plan area, 8 x 29 x 285 / (485 x 325) = 0.42 +-0.04 (the photograph's black fraction is about 0.41). Add edge probes to self_check part C for the first, fourth and eighth slots' side edges (x = centre +-14.5, ground frame, tolerance 6); without them the overlay test cannot see this error. The same bias shows in grate B (point 10).

2. **Cover P1 (`cover_stud_square`) is a double-triangular two-leaf cover, not a one-piece lid** (bethnal_green_entrance; the writer's own `ph-bethnal_green_entrance-stud-cover-ortho.jpg`). Four things differ from the target:
   * **The split.** One diagonal joint runs corner to corner. The studs it crosses are cut into right-angled half-studs on both sides; at least five are visible along it.
   * **The studs.** There are 10 per row and 10 per column; the target has 8 x 8.
   * **The size.** The outer edges read about 980 x 920 on the writer's 1.5 mm ortho. PM18's top edge of 515 px should be about 650 px; its right edge (-165, 570) agrees with mine.
   * **The fittings.** A round keyhole about 20 mm across is visible in one leaf, and a small raised blank oblong boss about 80 x 40 sits near the joint's lower end. There are no oblong lifting pockets.

   Amend the piece:
   * `outer` 960 (Photo 980 x 920 +-70)
   * `frame_rim` 20; `lid_inner` 920
   * `pattern.count` [10, 10]; pitch 95 and stud 45 kept; `edge_margin_mm` 10
   * add `leaves`: 2, triangular, joint 5 mm along one diagonal, studs on the joint cut into half-triangles
   * `lifting_pockets` replaced by "one round keyhole 20 mm per leaf, near the middle of the leaf"
   * add "a raised oblong boss 80 x 40 x 3 near one end of the joint, blank (where a maker's mark would go)"

   Amend `checks.cover_stud_square` to outer 960 +-60, studs 10, and add leaves 2 with a diagonal split. This is a period-right British type, so the photograph is a good one; the target just did not write it down.

3. **Cover P2's lug tread has half the lugs it should, in the wrong arrangement** (metal_grate_rusty; I read lug centres off its 1k displacement map, where the raised lugs are the high values). The tread is a centred lattice:
   * Rows are 41.75 mm apart.
   * Along each row a horizontal and a vertical lug alternate every 35.7 mm, so the horizontal lugs repeat every 71.4.
   * Each row is shifted 35.7 from the last, so a vertical lug sits above and below each horizontal one.
   * Lugs are 36 x 10.5 (the target's 38 x 9 is fine).

   The autocorrelation took only the axis peaks and missed the centred one. So each 71.4 x 83.5 cell of the scan holds 2 horizontal and 2 vertical lugs, not one of each as the target says. The drawing's quarter-cell offsets are not in target.json at all. Amend `pieces.cover_round_600.pattern`: `cell_mm` [71.4, 83.5]; `lugs_in_cell` = horizontal at (0, 0) and (35.7, 41.75), vertical at (35.7, 6) and (0, 47.75) (centres in mm; the vertical lugs sit 6 mm below their row's line). Make target_drawing.py read these positions from target.json.

4. **Cover P3 footway: the frame's top is patterned, not flat** (urban_street_03, the recessed cover in the west footway; a telephoto of the 8k at yaw 283.5, pitch -15). The rust-brown cast frame carries rows of small raised oblong lugs over its whole top, not "an outer flat flange". At 7 m the lug size cannot be measured. Amend `cover_recessed_footway.frame_steps` to "frame top cast with raised oblong lugs, two staggered rows along the long sides, more across the wider left end; use the P2 tread lug (36 x 10.5 x 2.5, rows 41.75 apart) [Photo for the pattern, Judgement for the size]". The concrete tray lid with a pale chamfered edge is right as written.

5. **The mitred corner's angle is about 133 degrees, not 112** (urban_street_01; the writer's own `ph-urban_street_01-kerb-mitred-corner-ortho.jpg`, a true ground ortho). On it the kerb's road edges run at 57 and 11 degrees and the yellow lines at 61 and 13 to 16 degrees. That gives an interior angle of 132 to 136. No photo measurement in target.json backs the 112. Amend `kerb_corner_mitre.angle_deg` to 133 +-5 (Photo, a new PM; 90 allowed for a street corner). Add a check `kerb_corner`: mitre angle 133 +-5 (or 90 +-2); radius corner 6500 +-600 on the face. No corner check exists today.

6. **The channel setts' colour shares are missing, so the brightness check cannot be met by design.** `channel_setts.colour` lists sett_pale_worn, sett_dull and granite_blue_grey with no shares. In linear light against asphalt_dry, sett_pale_worn alone reads 2.54 x the road and sett_dull 1.33 x. After the wear family's channel body (x 0.85) that is 2.16 and 1.13, both outside `channel_over_road_brightness` (1.35 to 1.7, tolerance 0). Add `colour_share`: sett_pale_worn 0.35, sett_dull 0.50, granite_blue_grey 0.15. The mean is then 1.78 x the road, and 1.51 after the grime (about 1.45 with the dark joints), inside the range.

7. **Handover to the wear target is not written down.**
   * The wear target's gutter_grime still says the channel is "0.255 m wide, in the kerb's own concrete", and its places and grate_wear entries still say a 0.40 m grate. Add to `photographs_win` (and to NOW.md's handover line when this lands): the gutter_grime channel band is 0.225 on granite stretches and 0.255 beside the concrete kerb, and the gully grate is 0.485 x 0.325.
   * The two targets give the iron two different bases: the wear target's `iron_grate` is 58/54/52 grey-black with grate_wear rust 100/72/56 painted on, while this target's `cast_iron_grate` is 92/74/66 rust-brown "clean". If both apply, the rust is put on twice. Amend `materials.cast_iron_grate`: the base is the wear target's iron_grate 58/54/52 and the rust comes from grate_wear; 92/74/66 becomes the expected composite on the bars (88/75/76 to 125/109/103 on the photograph), for checking the result.

8. **The upstand and the batter are one measurement, not two.** PM01, PM02 and PM26 all read the same ray, from the camera to the middle of the arris, against the same foot. From this camera, upstand and set-back trade about 0.39 mm of height per mm of set-back, and the three readings disagree by about 15 mm. Read with a vertical face, PM26's ray puts the arris middle at about 129 mm; PM01 and PM02 put it at 113 to 118. My readings of the 8k at two places are 129 and 133 with a vertical face, 119 to 123 with the 25 mm batter. So 125 with the batter stands. Amend the text of 4.1 and `face_batter.kind` to say this: "Photo-consistent with PM26 and the upstand together, not separately measured; Judgement for the split". Keep the checks.

9. **The asphalt edge laps over course B.** On the run beyond the crossing's right end block, the asphalt covers the outer 30 to 50 mm of course B, so the visible channel is 180 to 195 there. In front of the crossing, course B shows to y 225. Amend `channel_setts.meets_asphalt` from "10 to 30 mm wander" to "10 to 50 mm wander; over about a third of a run the asphalt laps 30 to 50 onto course B". The setts stay modelled to 225 underneath.

10. **Grate B (optional, Birbeck Street).** It shows the same thin-slot bias: on the writer's preview the slots are about half the pitch, so about 28 wide with bars about 30, against the target's 20. It also has two round lifting holes, about 25 mm across, on the long axis beyond the two end slots. Raised marks are cast on its centre bar and must stay blank (they are covered by no_lettering). Amend `gully_grate_B`: `slot_width` 28; add `lifting_holes`: two of 25 diameter on the long axis, about 55 beyond the centres of the two end slots (Photo, rough). The kind stays "rough".

11. **Cover P4: the leaf split is not shown by the photograph.** On a 4 mm ortho of urban_street_04, the cover's studded field is divided by more than one seam, at least one of them oblique to the long axis. I saw no single cross-joint at the middle. Amend `cover_road_double_leaf.leaf_split` kind to Judgement (not Photo). Its period is unproven (it sits in a fresh reinstatement), so keep it to one on the street, as the target already does.

## What is right

* **The approach.** Photographs win, element by element. The scene's 125 width, 915 granite blocks, 255 concrete channel, 400 square grate, 6 mm lip and taper block are each replaced from a photograph and written in `photographs_win`.
* **The granite kerb.** The section is a point list that a script can extrude. Top width 190, upstand 125, half-batter, R 25 arris and R 10 end arris all fit my readings. Random block lengths of 800 to 1200 with 9 mm open joints, the laying scatter and the chips all match the photographs.
* **The concrete kerb.** The bullnosed section (110 upstand, R 60) fits the Birbeck Street kerb.
* **The channel.** Two courses of granite setts (115 and 110), laid long side along the kerb, with dark recessed joints; the concrete channel block kept beside the concrete kerb.
* **The crossover.** Square-ended end blocks with their end faces exposed above the ramp. Granite flank strips, the in-situ ramp at 1 in 7.4, and a row of setts 12 to 20 mm proud as the lip; every part has plan coordinates. I saw the same in the photograph.
* **Grate A.** Its size, position (y 100 to 425, partly in the carriageway), 8 slots at 57 across the channel, the dish and the yellow-line kink are all right; only the slot and bar widths need point 1.
* **Covers P3 (road) and the small lids.** The tarmac-filled road cover is right. The small lids are honestly marked Judgement.
* **No tactile paving.** None at a vehicle crossing in 1990 is right whatever the dates of the guidance.
* **Nothing real on any casting.** `no_lettering` is the rule, and no maker's, utility's or council's name or crest appears anywhere in the target. The photographs' only cast marks, P1's boss and grate B's centre bar, are to stay blank.
* **Licences and previews.** Every photograph is CC0 with its author and date credited. The previews are crops of the object (I saw no lettering, no people, nothing the content rule bars; the Birbeck wrapper is masked).
* **London 2019 as a stand-in for a 1990 port town.** A fair one, and argued as such. Granite kerbs, sett channels and cast-iron grates are period objects in an old quarter. The target names what is modern and must not be copied:
  * urban_street_01's sawn-granite build-out (its form only is used)
  * Bethnal Green's block paving
  * hinged ductile and plastic covers
  * operator logos
  * tactile surfaces

  It also says what a port town would add: sootier stone, dirtier channels, more chips and tilt.
* **Buildable from target.json alone, once points 1 to 6 are in.** Every piece has numbers or point lists, a pivot and a material. The checks cover what the street shows: kerb section, lengths, joints, channel, crossover, grate, covers and flushness. Point 5 adds the missing corner check, and points 1 and 2 fix the two checks that would enforce the error.
