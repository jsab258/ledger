FAIL

# Railings target: fresh review (cloud week 42, 9 October 2026)

**2 faults, 9 narrow points.** The street's one guard rail A1 is drawn as a round-tube handrail, welded and capped flush. In my judgement a 1990 British kerbside guard rail has rectangular hollow-section rails and posts and bolted panel fixings, and the target's own lead says so. The jetty railing Q2 runs along the jetty's working berth, over the kit's own mooring ring, and leaves the open seaward corner by the light unrailed. Both faults have exact amendments below. Re-measured at full resolution, the photographed numbers hold within their stated errors, except R3B's bar heads (narrow point 2, an unplaced reserve kind). The camera heights hold within their errors, but two of the three are pooled across different grounds (narrow point 1).

How it was checked:

* I read the brief, the review brief, canon.md, RULINGS.md, TARGET.md, target.json, the scripts, the previews, the scene's E8 line and pieces, the bollards and kerbs targets, and the south-quay kit (south_quay_geom.py, README).
* I ran self_check.py and target_drawing.py on a scratch copy. The self-check gave **SELF-CHECK PASS 190/190**, and the drawing script wrote 11 views.
* I downloaded the three panoramas myself from Poly Haven. The 8k tone-mapped JPGs have the same md5 as the writer's. I also took the **16k HDRs** (api.polyhaven.com/files, decoded through bpy). The licence is CC0, the author Andreas Mischok, and the dates 2019-08-18 and 2019-05-19, all read from api.polyhaven.com/info.
* I re-measured on the 16k HDRs: the camera heights by course pitch and by rectified walls, the R3B pitch, rails, tips and heads, the LHB chain, and the Limehouse pavers.

**Network limits.** Wikimedia Commons, Geograph, Flickr, archive.org, gov.uk and assets.publishing.service.gov.uk refused through the proxy (CONNECT 403). So neither the writer nor I reached any photograph of a British pedestrian guard rail or quay railing of any date, nor BS 3049:1976 or LTN 2/09. I also scanned urban_street_03 and urban_street_04 again: no guard rail in either.

My A1 and Q2 judgements below come from my knowledge of 1970s to 1980s British street and dock ironwork and are marked **(Judgement, reviewer)**. They must be confirmed from Jafar's PC, which can reach Geograph and Commons.

## Faults, worst first

### Fault 1. A1, the street's one guard rail, has the wrong form: a welded round-tube handrail, not a 1976-pattern guard rail (Judgement, reviewer; no photograph on either side)

**Where.** TARGET.md 6.1, target.json kinds.A1.panel/profiles/fixings, the drawing A1_elevation. A1 stands in cam_A's near frame, so it is the most-seen piece of this family.

**What is wrong.** The target makes the posts round 48.3 tube and the rails round 42.4 and 33.7 tube, saddle-cut and welded to the posts. It caps the posts with flat plugs flush with the rail top and has "fixings: none visible".

* **Its only basis for "round" is the scene stand-in's primitive cylinders** ("post_diameter 0.05"). That is the same stand-in whose five-bar infill the target rightly throws out.
* **Its own lead contradicts it.** Its search summary gave "posts 50 x 30 mm" (S5, section 2), a rectangular hollow section, and the target never says why it set this aside.

In my judgement, the kerbside guard rail of a British town in 1990 (BS 3049:1976 stock, galvanised, often painted) is:

* a welded panel of rectangular hollow-section rails with a flat top face, and 12 to 16 mm round bars at about 110 centres;
* **bolted** to rectangular (or flat-bar) posts concreted into the footway, so that a struck panel can be unbolted and replaced;
* finished with the post top standing a little proud of the top rail.

A round-tube welded frame with plug caps reads as a tubular handrail or park barrier. That difference is visible from the pavement: a flat-topped rail against a round one, square post tops, and the clamp bolts at each rail end.

What A1 already gets right, and keeps:

* 2.0 m panel, 1.0 m to the top, x 10.0 to 12.0, axis z 3.375;
* vertical round-bar infill, 17 bars of 12 mm at 109.09, with gaps of at most 100;
* bottom rail at 200;
* black over galvanising as one condition;
* no marks.

**Amendment** (all Judgement, reviewer; millimetres in A1's local frame). Replace kinds.A1.panel post/cap/top_rail/bottom_rail/weld/fixings and their profiles with the following.

* **post**: RHS 50 x 30 x 3.0, the 50 face along the run, the 30 across (y). Outer corner radius 4.5. Top at **z 1030** (30 proud of the top rail), closed by a welded 3 mm flat cap plate flush with the four sides, edges broken R1. Axes at x ±1000, so the post faces toward the panel are at x ±975.
* **top rail**: RHS 50 x 30 x 3.0 laid flat (50 across y, 30 high), top **z 1000**, axis 985, from x −975 to +975.
* **bottom rail**: RHS 40 x 20 x 2.5 laid flat (40 across, 20 high), axis **z 200** (190 to 210), from x −975 to +975.
* **infill**: unchanged x list (−872.76 … +872.76, pitch 109.09), round Ø12. Each bar runs from z 210 to z 970, welded at both ends with a 2 mm fillet. Clear gaps are 97.09 between bars and 96.24 from a bar to a post face; both are ≤ 100 and pass.
* **fixings (new; replaces "none visible")**: at each of the four rail ends, a 6 mm end plate (the rail's own outline) is welded on and bolted to the post's inner face by one M10 bolt running along x through the post.
  * The hex head (17 across flats, 7 high) is on the panel side.
  * The hex nut (17 AF, 8 high) and 3 mm of thread are on the post's outer face (x ±1025).
  * The bright steel is painted over and rust-streaked at the nut.
* **joins**: a second panel would bolt to the same post's other face with the same bolt.
* **bbox** → [2072, 50, 1030] (x ±1036 including the nuts and thread, y ±25 from the top rail).
* **Walking strip, recomputed**: rear face z 3.375 + 0.025 = **3.400**. Clear to the stallriser face 4.975 = **1.575 m** (≥ 0.68). A1_no_deep_obstacle max depth becomes **0.895**.
* **checks**: replace the round-section checks with the following.

| check | expected | tolerance |
| --- | --- | --- |
| A1_post_section | [50, 30] | ±2 |
| A1_post_top | 1030 | ±10 |
| A1_top_rail_section | [50, 30] | ±2, top at 1000 ±10 |
| A1_bottom_rail_section | [40, 20] | ±2 |
| A1_bolts | 4 per panel, nut on the post's outer face | — |
| A1_bbox | [2072, 50, 1030] | ±8 |
| A1_walking_clear | ≥ 0.68 | (expected 1.575) |
| A1_no_deep_obstacle | ≤ 0.895 | — |

* **TARGET.md section 9**: add a photographs-win row: "post and rail sections: the scene's cylinders and the round tubes chosen in the first version → RHS, as the lead (posts 50 x 30) says; Judgement until a photograph is reached".
* **TARGET.md section 13, first item**: "From the PC: two dated (1985 to 1995) Geograph or Commons photographs of a British kerbside guard rail, to confirm the sections, the post top and the clamp before the build is gated."

### Fault 2. Q2 is on the wrong edge of the jetty: over the kit's mooring ring, and the seaward corner by the light is left open

**Where.** TARGET.md section 7 (the Q2 table and "the seaward corner … is left open: it is the boats' end"), target.json placements.quay, the preview target-plan-jetty.jpg.

**What is wrong.**

* The south-quay kit hangs **mooring rings on the jetty's basin face at (−110, −62) and (−110, −32)** (south_quay_geom.py, `_quay_furniture`: `for y in (-62.0, -32.0)`). It also moors its boat_jetty on that edge.
* The basin-edge run (posts y −36.4 to −15.4) **puts a railing directly over the ring at y −32**, 1.4 m from the post at −33.4. That contradicts the target's own rule for working edges ("a railing would stop the lines").
* Its check Q2_clear_of_mooring tests only the K6 bollards and K7 cleats, so it misses the ring. The jetty plan does not draw the rings.
* Meanwhile the jetty's **seaward** edge between the parapet's end (y −23.0) and the tip (y −15.0) is left open "for boats". Boats do not lie on the exposed seaward side of a parapeted jetty, and that corner is where a visitor to the light would walk off.

In my judgement (reviewer), a 1990 harbour authority would leave the basin side open for berthing and rail the light's end, closing the gap to the parapet. The target's principle (working edges unrailed, the jetty end railed) is right; only the runs are misplaced.

**Amendment** (south-quay kit frame, metres).

* **Q2_basin_edge (Q2a)**: cut to two bays at the tip, with posts at (−110.4, −21.4), (−110.4, −18.4) and corner (−110.4, −15.4). The ring at y −32 is then 10.6 m clear and the berth stays open.
* **Q2_tip (Q2b)**: unchanged, with posts every 3.0 m from (−110.4, −15.4) to the corner (−128.4, −15.4).
* **New Q2_seaward_return (Q2b)**: along x −128.4 from the tip corner back to the parapet's end. Posts at (−128.4, −18.4), (−128.4, −21.4) and an end post at (−128.4, −22.8), a 1.4 m end bay on a return as the target's own "ends" rule allows. The return closes off the open corner x −130 to −128.4, y −23 to −15.4. Its end post stands 0.2 m from the parapet's inner face (x −128.6) and its plate is 0.1 m clear of the parapet.
* **Totals**: 12 posts, 11 bays, 31.4 m.
* **Checks**:
  * add **Q2_clear_of_rings**: no post or rail within 4.0 m of the kit's rings (−110, −62) and (−110, −32), expected 10.6, min 4.0;
  * add **Q2_corner_closed**: the return's end post within 0.25 m of the parapet's inner face line and its end, y −23.0;
  * re-state Q2_basin_posts and Q2_tip_posts, and add Q2_return_posts, with the coordinates above;
  * Q2_clear_of_mooring stays.
* **Drawing**: draw the two rings on the jetty plan.
* **TARGET.md section 7**: replace "the seaward corner … is left open: it is the boats' end" with the return.

## Narrow points (each with its exact fix)

### 1. Camera heights, which holds where

Each figure below was measured at the object's own ground, at 16k, by me.

| panorama | where | result | what it means |
| --- | --- | --- | --- |
| bethnal_green_entrance | **at R3B's ground** (the gate pier beside it on the same paving; 22 courses, rms 1.4 % of a course; foot row 4618 of 8192, the writer read 4610) | **0.942** (75 mm gauge), 0.957 (76.2) | — |
| bethnal_green_entrance | rectified pier at h = 1 | course pitch 79.73 → **0.941** | — |
| bethnal_green_entrance | corroboration from R3B's own bars | pitch 76.4 at 0.94 | exactly three inches, a Victorian railing's likely pitch |
| bethnal_green_entrance | **at R3A's own two-stage wall** (red courses rectified at h = 1: 73.78) | **1.017** | — |
| bethnal_green_entrance | summary | — | The writer's pooled 0.97 is about 3 % high for R3B and 5 % low for R3A. The earlier 1.00 to 1.04 holds for R3A's wall, not for R3B. |
| urban_street_01 | **at R3D's own garden wall** (rectified on a 2.55 m foot line, 7 courses: 65.35 at h = 1) | **1.148** | — |
| urban_street_01 | the same wall in four column bands, foot read per column | 1.13 to 1.16 | — |
| urban_street_01 | the writer's own garden-wall anchor | 1.156 | agrees |
| urban_street_01 | the gate pier | 1.084 | the outlier (different bricks or foot), wrongly pooled in |
| urban_street_01 | summary | — | 1.12 is 2.6 % low for R3D. The earlier 1.23 holds for the planted bed or road (a kerb step below the footway), not for R3D. |
| limehouse | **the building wall's foot** (rectified, two gauges: courses 68.44 → 1.096, stretchers 207.6 → 1.084; ratio 3.03, metric bricks) | **1.09** | — |
| limehouse | **the paving the chain posts stand on** (clay pavers by the camera: course module 91.2 at h = 1) | **1.12** (102 module) **to 1.15** (105) | — |
| limehouse | summary | — | 1.12 holds at the posts' ground. The earlier 1.15 to 1.18 is the upper end and assumes 5 mm joints. |

**Fix**: state per object:

| object | camera height (m) | Photo sizes ×, and the error band |
| --- | --- | --- |
| R3B | 0.945 ±0.02 | × 0.974 (pitch 76.5, rails 433 / 1018 / 1948, tall tips about 2210, post top 2313) |
| R3A | 1.02 ±0.03 | × 1.052 |
| R3D | 1.15 ±0.02 | × 1.027 (pitch 97.0) |
| LHB | 1.12 to 1.14 | ±0.03 |

Section 4's table is to say which anchor is at whose ground. Every change is inside the target's ±6 % (R3A ±8 %), so nothing placed moves.

### 2. R3B heads contradict the photograph (reserve kind, not placed)

At 16k (h 0.97, the writer's plane):

* the knop of the tall bars is **87 to 100 across (median about 95) at z 2090 to 2110**, not "60 across at 2128";
* the tall tips are at **2255 to 2285**, not 2300;
* head_rz ends at z 2335, which contradicts its own tall_tip_z of 2300.

**Fix** (at 0.97, ±8 mm; × 0.974 if narrow point 1 is taken): head_rz =

(9,1990) (9,2025) (16,2030) (20,2040) (15,2050) (15,2068) (28,2080) (46,2098) (42,2110) (30,2125) (20,2135) (22,2145) (22,2155) (18,2165) (12,2200) (6,2240) (0,2275)

Set tall_tip_z to **2270 ±15** and change "a vase swelling to 60 across" in TARGET.md to "a turned knop about 95 across at 2100, a ring about 45 across at 2150".

### 3. R3A's drawing does not fit right of the post (reserve)

Right of the cast post, the photograph shows a second pattern: fleur-de-lis heads, offset by about half a pitch from the drawing (the overlay's tall bars there fall between the photographed ones). The left run, with spear heads and lily plaques on the short bars, fits.

**Fix**: in R3A.bars.pattern, say the numbers are the left run's (s < 1500 on the preview) and that the run beyond the post is another pattern, not measured. Group C should fit only s < 1500.

### 4. A1 ground detail (Judgement, reviewer)

A 20 mm bitumen ring is too neat for posts concreted into a 1970s flagged footway. The usual detail is a cut flag made good with a small patch.

**Fix**: replace profiles.ground_ring with a **reinstatement patch** of dark tarmac, sRGB (45, 43, 41), roughness 0.85, round each post:

* about 250 x 250, ragged edges ±20, flush with the flags to ±3;
* one flag edge cut along it;
* a 5 to 15 mm dark grit joint where it meets the flags.

Change the check A1_foot_ring to A1_foot_patch [250, 250] ±60.

### 5. A1 paint default (Judgement, reviewer)

For a highway-authority guard rail in a provincial port in 1990, unpainted galvanising weathered dull grey was at least as common as black.

**Fix**: make A1_galvanised the default at 55 %, sRGB (118, 120, 122) streaked, roughness 0.55, metal 1, with dark run-marks below the bolts and white zinc bloom at the feet. Set A1_black_scuffed to 30 % and A1_black_chipped to 15 %. Keep "no bands, no reflective sleeves". This is one condition for one panel, so it is a choice and not a fault.

### 6. Q2 bay length (Judgement, reviewer)

3.0 m comes from the bollards target's post-and-chain spacing. For a welded tube railing with a 48.3 top rail, 2.0 m is the usual maximum; 3 m bays look spindly and would not take a crowd load.

The commonest 1990 dock-edge form was galvanised ball-type stanchions, with 33.7 to 42.4 rails passing through forged balls at about 1.8 to 2.0 m.

**Fix**: either keep 3.0 m and make the top rail **60.3 x 3.6** (Q2_top_rail_od 60.3 ±3), or go to 2.0 m bays. In the second case, recompute fault 2's post lists every 2.0 from the same corners.

### 7. The walking-strip check is taken at ground level only

The fish market's awning_02 (x 10.5 to 13.5) has its front edge about 1.57 m above the footway at z 3.39, exactly over the rail line, rising to the fascia. At a 2.0 m head height the strip behind the rail is about 1.0 m clear today, which passes, but A1_walking_clear would not catch a lowered awning.

**Fix**: make A1_walking_clear the clear width between the panel's rear face and any fixed projection **from 0 to 2.0 m above the footway** in x 9.5 to 12.5, min 0.68 (expected about 1.0 with the awning).

### 8. Q2 corner and end-post ears

target.json says "one ear each side of every post", but end and corner posts have a bay on one side only.

**Fix**: put ears only on the sides that face a Q2b bay. At the two Q2a/Q2b corners, the ear faces the Q2b bay only.

### 9. Set-back (note, not a change)

The scene's 0.25 m behind the kerb leaves the rail's road face 0.35 m from the kerb face. A 1980s rule of about 0.45 m is remembered (by the writer and by me) and not read. Leave it as the scene has it, and add it to section 13's PC list next to LTN 2/09.

## What is right

* **The scene's numbers are read correctly.** E8 is one 2.0 m panel, 1.0 m high, at x 10.0 to 12.0, with posts at z 3.375. vignette-pieces.json was checked by me.
  * The stallriser face at z 4.975 is the nearest fixed frontage behind the panel. The doors at x 9.35 to 11.09 sit at z 5.065, and the downpipe shoe at x 9.0 is outside the window.
  * No crate or other object stands behind the panel today.
  * The 1.576 m clear, against 0.68, and the 0.896 obstacle rule are right, and they are the right response to the 29 September failure.
* **The infill change is right.** Seventeen 12 mm vertical bars at 109 centres, gaps ≤ 100, replace the five 25 mm stand-in bars. Plain vertical-bar infill fits 1990; the see-through "visibility" panels came after.
* **The absences are right.** There is no area, chapel or yard railing on the street, and the data checks bear this out:
  * the frontage line has no forecourts;
  * the chapel is at x 100;
  * the yard mouth is the town's to gate.
* **The quay principle is right for a 1990 working port.** Working quays are left unrailed, with granite cope and bollards. Chain stands only at the ladder (the bollards target's K5), and any railing belongs at the jetty's public end. Only Q2's runs are misplaced (fault 2).
* **The photographed measurements reproduce at 16k.**
  * R3B: bar pitch 78.9 at 0.97 (target 78.54), and rails at about 450, 1060 and 2006 (target 445, 1045, 2000). The post finial is at about 2375, and the hinge post, collar and ball feet are as described.
  * LHB: post top about 1076 (1086), lugs about 790 and 388 (800, 405), swag sags about 207 and 220 (215, 240).
  * Q2b's sag of 200 (7 %) is a sound choice. Raising the bollards target's K5 chain sag from 150 to 200 is right.
* **Sources and licences.** Every photograph used is Poly Haven CC0, by Andreas Mischok, 2019. The author and dates are verified on the API, and the target says honestly that none is from the period.
  * Unreached sources are listed, and leads are kept as leads.
  * No real maker's name, crest or council name appears anywhere. "council" occurs only as "council green" and "council number".
  * The previews are cropped and masked (the boat's name board, the notice, the figure, the flange mark), and none shows alcohol, gambling or children.
* **Build from target.json alone.** As written, unit 3.3 could build A1 and Q2 from target.json without other sources: sections as point lists, the cap and catenary profiles, the link and ear outlines, the base plate and nuts, post lists, materials, wear words and seeds. After the two amendments it still can, because every new part is given as numbers above.
* **The scripts.** self_check.py passes 190/190 on a clean copy, and target_drawing.py draws all 11 views from target.json alone.
