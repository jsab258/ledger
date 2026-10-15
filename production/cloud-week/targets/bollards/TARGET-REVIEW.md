FAIL

# Bollards target: fresh review (cloud week 42, 9 October 2026)

Reviewer: a fresh target reviewer who neither wrote nor will build this. I read REVIEW-BRIEF.md, BRIEF.md, canon.md and RULINGS.md, and the target's TARGET.md, target.json, target_drawing.py, self_check.py and makers. I looked at all 21 previews, and re-read the five panoramas' licence, author and date at Poly Haven: api.polyhaven.com/info and /files, and polyhaven.com/license, all reached on 9 October 2026. All five are CC0, by Andreas Mischok, and the dates match. I downloaded the five 8k tone-mapped panoramas and re-measured the camera height in each one myself, using a different method from the writer's. Both scripts were run on a scratch copy, outside git. self_check printed **SELF-CHECK PASS: 260 of 260**. target_drawing.py made drawing.json, 8 kind pictures, the sheet, the street plan and 5 overlays without error. Nothing in the target folder was edited and nothing was committed.

**Verdict: FAIL, on 3 faults** (worst first below), plus 12 narrow points. Fault 1 is not narrow. It concerns the whole size of one kind, K2, and the method every height rests on. Faults 2 and 3 each have an exact fix. With all three amended as written here, the target would pass.

## The camera-height claim, tested (every height rests on it)

**My method.** In a levelled equirectangular panorama, row 2048 is the horizon. It cuts every vertical surface at the camera's height above that surface's foot, whatever the distance. On a brick wall I find the course pitch in tan(angle) units, which is constant up a vertical plane, and the foot row, both in the same columns. Then:

camera height above the foot = 75 mm × tan(θ_foot) / pitch.

The courses were counted from intensity profiles in 12 to 25 px column bands and checked by eye on 3x to 4x crops. **The key point is to use a wall standing on the same ground as the bollard.** Kerb steps between levels were measured with the same rule.

| panorama | writer's h at the bollard's foot | my h above the bollard's foot | how |
|---|---|---|---|
| urban_street_01 (US01_b, K1a) | 1.16 | **1.17 to 1.23** | Two walls on the footway behind give 1.16 (garden wall, cols 4250 to 4275: joints 2178 to 2270, 15.3 px; foot at row 2287) and 1.12 (gate pier, col 3760 to 3830: 11.9 px; foot 2225). But US01_b stands in a planted bed whose soil is **0.07 m below that footway**: the footway kerb top at row 2504, a 0.05 m visible face, an edging stone, then 0.02 m more to the soil (cols 4560 to 4740). Walls plus the step give 1.21 to 1.23. The writer's road-line anchor gives about 1.17 at the bed. A parked hatchback's roof stands above the horizon and its wheel gives at least 1.3 above the gutter, so the camera was not low. |
| bethnal_green_entrance (BGE_a, K1b) | 1.02 | **1.03 to 1.04** | Planter wall on the same block paving as BGE_a (cols 5840 to 5940): 15.3 px courses, foot row 2262, 13.9 courses to the horizon. **The writer's value holds.** |
| birbeck_street_underpass (BB_b, K2a) | 1.22 | **1.04 to 1.14** | The writer's only anchor, the double yellow line, lies **on the road**. BB_b stands **on the footway, 0.10 to 0.11 m higher**: kerb face rows 2553 to 2597 at col 3500 to 3700. The line's 1.24 above the road is therefore 1.14 above the footway. The viaduct wall on that footway (yellow stock above the paint, cols 3700 to 3760: joints 1852, 1872 … 2009, 19.7 px; foot row 2318) gives 1.04 at a 75 mm gauge, or up to 1.10 if these Victorian courses run 79 mm. |
| urban_street_02 (US02_a, K2b) | 1.15 ("pooled", no anchor of its own) | **0.91 to 0.93** | Two brick surfaces stand on US02_a's own footway. The building wall behind it (cols 740 to 840: joints 2052 to 2192, 11.75 px; foot 2194) gives 0.93. The gate pier at the panorama seam (col 7985: joints at 2032, 2047, 2061 … 2208, 2224, a steady 14.77 px; foot about 2226) gives 12 courses, 0.90 to 0.91. **The writer measured 0.84 to 0.9 here and set it aside** ("its bricks are not a 75 mm gauge"), with no evidence. For 1.15 to hold, the courses would have to be 95 mm, which no British brick gives. US02_a's cap sits about 5 px above the horizon, so its height ≈ h + 0.02. |
| limehouse (LH_b, K5) | 1.17 | **1.15 to 1.18** | Brick building on the same paving (blue-brick courses 25.2 px; foot about 2440). **The writer's value holds.** |

So the writer's headline is right: no panorama was taken at 1.6 m, and every one sits between 0.9 and 1.3 m above its own ground. But **the height was applied at the wrong ground level for two of the five bollards, and one anchor that contradicted the pooled value was discarded.** The "independent check" in TARGET.md §3 is circular: K2's two heights (1180 and 1188) agree only because US02_a was given the pooled height. All of self_check's group C fits are tautological for this question, because the previews were rectified at the writer's own heights. No automatic test in the target could catch this.

## Faults, worst first

### 1. K2 is 11 to 20 % oversize in every dimension, and K1a is probably 3 to 5 % small (camera heights taken at the wrong level)
*Photographs:* birbeck_street_underpass, BB_b, bearing −24.7° (pano col about 3534). urban_street_02, US02_a, bearing −148.8° (col about 710). Places and numbers are in the table above.
At the camera heights its own foot stands at, BB_b is **about 1,000 to 1,100 high, not 1,180**, and US02_a is **about 950, not 1,188**. As written, K2 would stand 130 mm taller than K1 at the quay-end junction. The photographs make it about K1's height or less, which is visible from the street beside a person or a K1.
**Amendment:**
- **K2a (BB_b):** use h = 1.085 (the footway mean of the two anchors), so every z and r of `kinds.K2.profile_rz`, `parts`, `mouldings` and `profiles_final.BB_b` is × 0.8897.
  - Height **1050**. Foot ring Ø **250**. Collar band z **599 to 634** (still 0.59 H), 7 proud. Cap plate r 75, overhang 5.
  - Checks: `K2_height` 1050 ± 60; `K2_foot_ring_diameter` 250 ± 18; `K2_shaft_diameter_z300` **193.4** ± 12; `K2_shaft_diameter_z900` **145.4** ± 10; `K2_collar_proud` 7 ± 4; `K2_cap_overhang` 5 ± 4.
- **K2b (US02_a):** use h = 0.92, so `profiles_final.US02_a` is × 0.80.
  - Height **950**, foot ring Ø 208. Against K2a: z_factor **0.905**, r_factor **0.831**.
  - Add a check `K2b_height` 950 ± 50.
- **Calibration:**
  - `calibration.panoramas.birbeck_street_underpass.h_cam`: 1.085 ± 0.06, "at the footway; the line anchor is at the road, 0.10 below".
  - `urban_street_02.h_cam`: 0.92 ± 0.03, with the two brick anchors added to `calibration.anchors`.
  - Delete the "independent check" sentence in §3 and the self_check B test "the two K2 photographs agree on the height".
- **K1a (narrow by itself, same cause):** US01_b's camera stands 1.17 to 1.23 above its bed, against 1.16 used. Scale K1a by **1.03**: height **1082**, plinth Ø 202. `K1_height` 1080 ± 50, `K1_base_diameter` 202 ± 14. Or keep 1050 and make the check +70 / −40, saying why.
- **Method, in TARGET.md §3:** "each camera height is measured at the bollard's own ground level; where the anchor is on another level, the step between them is measured and added".
- **Also tell the kerbs-and-covers writer** that their 1.6 m is about 25 % high in urban_street_01 at road level (about 1.27) and about 55 % high in urban_street_02 (about 1.03 at the road). The warning in this target says "30 %" for both.

### 2. The quay placements in target.json would put 21 of the 31 pieces in the wrong place, or nowhere
*Source:* tools/art-recipes/south-quay/south_quay_geom.py, `BOLLARDS` (line 1473), `LADDER_Y`, `at["jetty_x"]`; research/south-quay/METHOD §4 and §6.
- **K6:** `placements.quay.quay_edge` says 10, "x_m −69.25, spacing_m 30". A script reading that puts ten bollards in one 270 m line, past the end of the north quay. The kit has five on the north quay, two on the jetty and three on the east quay.
  **Amend** to the kit's coordinates (recipe frame, metres): (−69.25, −88.0), (−69.25, −58.0), (−69.25, −28.0), (−69.25, 2.0), (−69.25, 30.0), (−110.75, −80.0), (−110.75, −45.0), (−95.0, 40.75), (−115.0, 40.75), (−140.0, 40.75). Name which three are K6b. Proposed: (−69.25, −88.0), (−69.25, 30.0) and (−140.0, 40.75), the quay ends.
- **K7:** "on the jetty's timber fender" has no fender to stand on. The kit has no timber fender, and the jetty is stone with a granite cope.
  **Amend** to x **−110.25** (on the jetty's cope, 0.25 m behind its nose at x −110.0), y **−64.0, −58.0, −52.0**, long axis along y, beside the jetty boat's berth (y −63 to −53).
- **K5:** "two each side of the quay ladder (y −36), with the chain run across its head". A chain across a ladder head blocks the way out of the water.
  **Amend** to posts at x **−69.5**, y **−40.5, −37.5, −34.5, −31.5**, with chains between the outer pairs only (−40.5 to −37.5 and −34.5 to −31.5). The 3.0 m over the ladder stays open.
- **K2 junction:** "the four kerb-return tangent points" of a three-arm junction with three returns (8, 6 and 12 m), and no coordinates.
  **Amend** to the exact rule "the two tangent points of the 8 m return (inside Quay Street's turn west) and the two of the 6 m return (the Harbour Board approach), each moved 0.5 m from the kerb face along the footway normal; none on the 12 m outside return". Better still, give the four (x, y) the kit's junction builder computes.

### 3. K6b's profile is a stepped spire, not the cannon "with a ball top" its own words describe
*Source:* `kinds.K6.variants[K6b].profile_rz` and the drawing K6b-elevation-and-plan. Above z 790 the points (140, 796), (120, 840), (95, 880), (60, 905), (50, 915), (40, 940), (30, 955), (0, 965) draw a pointed beehive. An upturned cannon ends in a flared muzzle with a ball sitting in it. Three of these on the quay would read as lighthouses, not guns.
**Amend:** replace everything after (150, 760) with (150, 840), (162, 856), (172, 880), (172, 905), (158, 914), (98.3, 914), (87.5, 935), (70.3, 955), (48.7, 970), (24.9, 979), (0, 982). That is a muzzle swell to r 172, a flat muzzle face at z 914, and a ball of radius 105 (centre z 877) showing 68 mm. Height **982**. Add a check `K6b_ball` (ball radius 105 ± 15, standing 68 ± 15 above the muzzle face).

## Narrow points (a small detail with an exact fix each; for the writer and the builder)

1. **K1b does not reproduce BGE_a.** The overlay on bge_a shows the photographed plinth about 140 high with a convex roll on top (foot close-up). The drawn plinth is 113 with K1a's flat R6 edge, and the bead is about 15 mm high. *Fix:* drop K1b (models K1: 1; the yard mouth uses K1a twice with two condition seeds; one design per street). Or give K1b its own profile: plinth to z 140, a half-round roll R 14 on its top edge, bead centre at 0.53 H.
2. **`kinds.K2.base_diameter` is 271.6**, while the text and the `K2_foot_ring_diameter` check say 281. *Fix:* set it to 2 × max r of the foot ring (250 after fault 1).
3. **K2b recipe.** "profile K2 up to z 1088, then the cone given in profiles_final.US02_a" mixes two scales. *Fix:* "K2b = `profiles_final.US02_a` × 0.80, whole".
4. **K5 chain eye.** "a cast D-lug" has no size. *Fix (Photo LH_b, ±30 %):* a D-lug 55 high, 40 proud of the shaft, 18 thick, with a 24 mm hole whose centre is 22 from the shaft face.
5. **K5's spiked chain** is the photographed 1980s to 90s docklands-marina dress. For an unrestored 1990 working quay, set `chain.spikes` to none and use a plain short-link chain with a 13 mm bar. Keep the spiked chain only as an option the street does not use.
6. **K3 at x 47.2, both sides.** Nothing in the scene says what they guard: no corner, crossing or opening is placed there. *Fix:* name the corner or entry they guard, or move the pair to the yard-mouth pattern's other use (a side passage) or drop them; the street count stays within 6 to 10. Also say in §1 why one 48 m street carries four kinds, against the asset plan's "one design per street". For example: K4 is the chandler's own private posts, K3 the street-end pair is older council stock, and K1 and K2 belong to different owners.
7. **K2 grey (K2a's colour)** is a 2019 London underpass paint; black was the 1990 norm. *Fix:* make black the default K2 paint, with grey (88, 89, 91) as one condition only.
8. **K7's plan shape** is missing. *Fix:* base 400 × 110 with ends rounded R 55; pedestal 96 × 124 at its foot with rounded ends; horns of round section, Ø 32 at the pedestal tapering to Ø 22 at the tips.
9. **`K1_foot_paint_loss`** (60 to 70 % bare) is written as if every K1 had it. *Fix:* apply it to the worn-foot condition only.
10. **Checks missing** for K1b (if kept), K2b's cone cap (rim r 80 × 0.80, rise 22 × 0.80), K6a's head overhang (70 ± 15) and K6b (fault 3). Add each with its number.
11. **self_check.** Group C cannot test the scale. *Fix:* add one scale test per panorama that does not depend on the writer's heights: courses to the horizon on a wall at the bollard's own level, as in the table above.
12. **K4 "guarding the metal-refit window"** at 0.45 m from the kerb does not guard a window 1.5 m back. *Fix:* say "anti-parking posts at the chandler's front" (the placement is fine).

## Element by element (photographed kinds)

**K1 (US01_b, BGE_a).** The items below are in the target with a number or a profile, except where marked:
- overall form;
- plinth, with its 3 mm chamfer;
- shoulder and cove;
- the one straight taper;
- the bead with its fillet ring;
- the neck;
- the cap collar, quirk and ring;
- the flattened dome;
- the edges (R4 to R8);
- seams (none);
- fixings (none);
- marks (none);
- the root on paving, with a grit joint, and in a bed, with a 20 mm bark bank;
- paint (sRGB, roughness);
- wear (chip 15 × 65 at z 70 to 135; foot bare 60 to 70 %; dirt to 0.5 to 0.7 m);
- lean.

Contradicted:
- the absolute size (fault 1, about 3 %);
- K1b's plinth and roll (narrow 1).

**K2 (BB_b, US02_a).** The items below are in the target with a number or a profile:
- form;
- rolled foot ring;
- two tapers;
- collar band;
- flat cap plate (K2a) and low cone (K2b);
- edges;
- no seams, fixings or marks;
- root, with its dirt ring;
- paint;
- wear (scuffed foot ring, chips, a 40 mm scratch).

Contradicted: the absolute size (fault 1, 11 to 20 %).

**K5 (LH_b).** The items below are in the target with a number or a profile:
- flange;
- four nuts (size, pitch circle, angles);
- studs;
- two beads;
- neck;
- cap collar;
- dome;
- chain-eye heights;
- chain links and spikes;
- paint;
- wear;
- the mark (left blank).

In words only: the D-lug (narrow 4).

**Judgement kinds.** K3, K4, K6 and K7 are marked Judgement (K6a Read from the kit) in every place they appear, in TARGET.md and target.json alike. Their numbers are reasonable for the kind: an 850 concrete post 250 at the foot, a 114.3 tube 1000 high, a 720 bell bollard on a 500 flange, a 400 horn cleat. K6b's top is the exception (fault 3).

## Photographs win: checked

The 0.765 cannon-and-ball stand-in and the 1.008 held mesh are replaced by K1 as photographed, which is right. The research's "sometimes a white band" is rightly overruled: no band appears in any of the five photographs (I looked at all the bollards in each panorama). The 0.5 m set-back (scene, Read) is not contradicted, since the photographs range from 0.33 to 1.25 m. The lean of 0 to 2° agrees with the photographs' 0.2 to 1.0°. I found no element where the target follows a book against its photographs. The size error comes from calibration, not from a book.

## Rules: checked

- **Sources:** only Poly Haven was reached, and I reached the same pages. Search summaries are used as leads only, and are marked so.
- **Licences:** CC0, read on polyhaven.com/license and the API. The author and dates are confirmed. Nothing is NoAI.
- **No real names or marks:** no real maker's, council's or borough's name, crest or monogram is on any kind. Every kind says "no marks". K5's embossed mark is blurred in the previews and is to be left blank. The self_check banned-word scan passes. TARGET.md names places (Bethnal Green, Limehouse, Bristol, Charlestown), which is fine because none goes on a casting.
- **What the previews show:** they are cropped to the object. I saw no alcohol, gambling, children, cars, business names or legible lettering in any of the 21. The graffiti behind BB_b shows as unreadable colour at its 28 mm margin.
- **Period:** every photograph is from 2019, and the target says so for each.
  - K1's pattern (plinth, straight taper, half-height bead, collar and flattened dome) is a generic cast-iron form, in use long before 1990. It has no sleeve, band, stainless or reflective strip, so it is fair for a 1990 northern port street once grimed and dulled, which the condition variants provide. The US01 site itself (fresh paint, new granite-edged beds) is London-smart and must not be copied; the target copies only the casting.
  - K2's plain tapered post is fair as 1970s to 80s stock, painted black (narrow 7).
  - K5 is regeneration-era marina ironwork, flagged "period doubtful" by the writer. Its spiked chain should go (narrow 5).
  - None of the five is a 2000s replacement type, judged at this resolution. That is a judgement, not a proof; no 1975 to 2000 photograph was reachable.

## Buildability and the checks

From target.json alone, a script can build every kind's mesh: lathe profiles for K1, K2, K3, K4, K5, K6a and K6b; a half outline for K7; bolts and chain numbers; materials; variants; condition seeds. The gaps are the K5 lug and the K7 plan (narrow points 4 and 8) and the K2b recipe (narrow 3). The placements are not buildable as written for the quay and the junction (fault 2). The street proper is buildable. On it, the yard-mouth pair stands 0.3 m outside each crossover edge and clear of the cones and crates. Every street bollard leaves 1.40 m or more of footway behind it (2.0 − 0.5 − base r 0.1; K4 1.49), which is twice the 0.68 m a walking person needs. They stand 1.2 m or more from door centres and 1.5 m or more from lamp columns (I checked E1's columns at x 8, 18, 28 and 38 in vignette-pieces.json). The 53 checks catch what matters from the street for K1, K2 and K5: heights, diameters, bead and collar places, silhouette within 6 or 7 mm, no band or marks, set-back, clearances and counts. They inherit fault 1's numbers, and lack checks for K1b, K2b, K6a's head and K6b (narrow 10).

## What is right

- The finding that these panoramas were not taken at 1.6 m. My own measurements confirm it in all five (0.9 to 1.3 m), and the BGE and Limehouse heights hold exactly.
- K1's profile and parts are close, measured work. The overlay on US01_b fits with a median of 0.85 mm, and every moulding the photograph shows is written down with a number.
- K5 is complete down to the nut angles and chain links. Its mark is left blank.
- Judgement is marked everywhere it is used. The unreached sources are listed and nothing is taken from them.
- The street's ten bollards are believable in count and place on the street proper, and do not block the footway.
- The writer's own "could not settle" list is honest and specific.

## Where the network limited this review

Wikimedia Commons, Geograph, Flickr and archive.org all refused (proxy 403, 9 October 2026). So I could not test any of the following against a dated 1975 to 2000 British photograph or a period book:
- whether the K1 and K2 patterns stood in a 1990 northern town;
- the judgement kinds (K3, K4, K6, K7);
- the real form and size of a cannon or bell mooring bollard;
- the Historic England entries the target lists.

Every size above rests on brick gauges (75 mm modern, 73 to 79 mm Victorian) measured on Poly Haven's CC0 panoramas, reached at full resolution.

## Re-review (try 2)

PASS

**0 faults; 4 narrow notes.** I re-reviewed the amended target (TARGET.md §15, target.json, the new calibrate.py and anchors.json, self_check.py, target_drawing.py and the new previews) against my own measurements on the five full-resolution panoramas.

All scripts ran on a fresh scratch copy:
- self_check: **SELF-CHECK PASS: 308 of 308**;
- target_drawing.py: 8 kind pictures, the sheet, a street plan and a quay plan, and 4 overlays;
- calibrate.py: reproduces anchors.json exactly.

Nothing in the target was edited and nothing was committed.

### The three faults: each truly answered

**1. Camera heights and sizes.** I re-measured each bollard directly, without the writer's frames. For each I took the top and foot rows in the panorama at the bollard's column, put the axis one foot-radius behind the foot's front edge, and used H = h − d_axis × tan(angle to the top), with my own heights:

| bollard | h used | top row | foot row (front edge) | d_axis | H (mine) | target |
|---|---|---|---|---|---|---|
| US01_b (K1) | 1.195 | 2114 | about 2707 | 2.26 m | 1.08 m | 1082 |
| BB_b (K2a) | 1.085 | 2061 | 2465 | 3.40 m | 1.05 m | 1050 |
| US02_a (K2b) | 0.92 | 2041, 7 px above the horizon | 2265 | 5.58 m | 0.95 m | 950 |

US02_a's foot ring reads 0.21 m across at its distance, against 208 in the target.

The scaled profiles, parts, mouldings, base diameters and checks all agree. K2 is 1050 high, foot ring 250, shaft Ø 193.3 at z 300 and 145.4 at z 900, collar at z 599 to 634. K2b is profiles_final.US02_a whole: cone rim 64, rise 17.6, collar at 0.59 H. K1 is 1081.7 high with a 201.6 plinth. The circular "two K2s agree" test is gone. K2b is now honestly a smaller casting, and a test checks that K2a is not taller than K1.

**2. Quay and junction placements.** I checked these against tools/art-recipes/south-quay/south_quay_geom.py myself.
- **K6:** the ten places are the kit's `BOLLARDS` exactly. The three K6b cannons are at the quay ends. The three boats' lines all go to K6a bells (the kit's `BOATS`), so no rope runs to a cannon.
- **K5:** posts at x −69.5, y −40.5 to −31.5, with chains on the outer pairs only. The ladder's handholds (x −70.15 to −69.55, y −36 ± 0.23) sit 1.3 m from the nearest post. The fish-box stack at (−67.0, −41.5) is 2 m inshore of the chain line. Nothing collides.
- **K7:** the cleats at x −110.25 sit on the jetty's cope; the jetty strip runs x −130 to −110 and the jetty bollards stand at −110.75. They are beside the jetty boat's berth (y −63 to −53). The jetty rings hang under the cope face, not on top.
- **Junction:** I ran the kit's own `Junction`. Its 8 m and 6 m return tangent points are (−21.176, −3.0), (−28.986, −9.265), (−21.719, 3.0) and (−27.698, 8.502), as stated. All four posts sit **3.50 m from the nearest road centreline**, so 0.5 m behind the kerb face on the footway side, not in a carriageway. They stand on the kit's 2.0 m corner footways, leaving about 1.5 m clear to the yard walls.

**3. K6b.** The profile is now the muzzle swell to r 172, a flat face at z 914, and a ball of R 105 (centre z 877) standing 68 mm proud; height 982. My drawing run shows a cannon muzzle with a ball, not a spire. The checks K6b_height, K6b_ball and K6b_muzzle_swell are present.

### The twelve narrow points: all answered

1. K1b is dropped: K1 has one model.
2. K2 base_diameter is 250.
3. K2b is "profiles_final.US02_a, whole".
4. The D-lug is 55 / 40 / 18 with a 24 hole, centred 22 from the shaft face.
5. The chain is plain short link, 13 mm bar, no spikes; the spiked chain is an unused option.
6. K3 is moved to flank the scene's real 1.0 m passage at x 39 to 40. That passage is confirmed in vignette-scene.json's chandler note, and §1 now explains the four kinds by owner.
7. K2 is black by default, with grey as one condition.
8. K7's plan is given.
9. K1_foot_paint_loss is "worn-foot condition ONLY".
10. The new checks are in: 65 in all.
11. Group B now calibrates each panorama independently, and §3 says group C tests shape, not scale.
12. K4 is "anti-parking posts".

Every street post clears doors (1.56 m and more), lamp columns, the crossover and the other furniture, and leaves 1.38 to 1.49 m of footway against the 0.68 m a walking person needs.

### Narrow notes (each a small detail with an exact fix; no number the builder uses moves)

1. **The US01 gate pier in calibrate.py.** The fitted pitch_tan 0.01049 sits exactly on the +15 % edge of its search range (1.15 × the 11.9 px guess), which means the fit failed. That is where the reported 0.98 (1.05 at the bed) comes from. Listed directly at cols 3800 to 3820, the joints fall at rows 2049, 2061, 2072, 2084, 2096, 2108, 2121, 2133, 2146, 2158 and 2170, a steady 12.1 px. That gives 1.09 above the pier foot and 1.16 at the bed.
   *Fix:* set that anchor's pitch to 12.1 px (or its rows to 2045 to 2175), and make calibrate.py mark any fit that lands on its range edge as failed. The group B mean for urban_street_01 then becomes about 1.18 against the stated 1.195.
   The BGE planter wall is curved, so its pitch changes with the column (15.3 to 16.6 px). Its 0.96 to 1.04 spread is real, but it no longer carries any number.
2. **The quay-plan picture** from target_drawing.py draws only the north quay's land, so the jetty and east-quay posts appear over water. The coordinates are right.
   *Fix:* draw the jetty strip (x −130 to −110, y −100 to −15) and the east quay (y ≥ 40) as land.
3. **The east side reads as a cluster.** K3 at x 40.2 and K4 at x 41.5 stand 1.3 m apart in two materials, so four posts in 5.2 m read as a cluster from the street.
   *Fix (judgement):* move the first K4 to **x 42.5**. It is still 2.30 m in plan from the nearest door centre (the chandler's at x 44.203), and the two pairs then read as two groups 2.3 m apart.
4. **A muddled phrase in §3.** "the bed 1.195 plus the 0.055 to 0.07 it stands above or below the road" mixes two things.
   *Fix:* "the bed stands about 0.055 m above the road, so the camera is about 1.25 m above the road".
