# Quay Street's kerbs, channel, gully grates and covers: the target (cloud week 42, 9 October 2026)

**Quay Street's kerb is dressed grey half-battered granite (125 mm upstand, about 190 mm top, 255 mm deep, blocks 0.8 to 1.2 m with 9 mm joints) on most of its length and pale concrete on three stretches, the channel two courses of granite setts (225 mm; 255 mm for the concrete channel block), the dropped crossover a 3.0 m in-situ concrete ramp between granite flank strips with a row of setts as its 15 mm lip, the gully grate a rust-brown 485 x 325 cast-iron rectangle with eight slots (not a 400 mm square), and the covers four cast patterns plus a tarmac-filled recess, all blank, none with a maker's mark; no tactile paving in 1990.**

The target for the family "kerbs and drain covers on Quay Street", written from Poly Haven's CC0 London photographs (all 2019) and the repository's own numbers. Everything is millimetres unless a line says otherwise; the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (plans, sections, an elevation); `self_check.py` tests them against their sources (last result: SELF-CHECK PASS: 191 of 191 tests pass (A printed numbers 34/34, B photograph measurements 67/67, C drawing on the photographs 30/30, D internal consistency 55/55, E text 5/5)).

## 1. What the street's present kerb gets right, and what this target changes

Today's street (SCENE-SLOTS.md, read 9 October): kerb upstand 125, width 125, depth 255, blocks 915 long, channel course 255 wide, a dropped crossover on the west side at x 22.5 (3.0 wide, 6 mm upstand, one taper block), a gully grate 400 square (recess 50, dish 30) on the east side at x 12.0, crown 75 mm above the channel. These are trade guesses, not photographs.

| | the present street | this target | why |
|---|---|---|---|
| upstand | 125 (Read) | granite 125 kept; concrete 110 | Photo: 113 and 118 to the middle of the arris (125 to the top, PM01, PM02), so the 125 is right; a re-surfaced concrete kerb reads 96 to the arris middle (PM03) |
| kerb top width | 125 | granite 190, concrete 160 | Photo: 181, 185, 189 on granite (PM01, PM02, PM25), 166 on concrete (PM03): the street's 125 is a precast catalogue width, the photographed kerbs are wider |
| face | not stated (vertical) | granite half-battered (25 mm back by z = 100); concrete bullnosed R 60 | Photo PM26: the middle of the arris stands 29 +-9 mm behind the foot line |
| depth | 255 (Read) | 255 kept | unseen; Read |
| block length | 915 for all | granite random 800 to 1200 (mean 1000); concrete 915 | Photo PM04: whole granite blocks 0.84, 1.01, 1.14 m |
| channel | 255, "in the kerb's own concrete" | granite sett channel 225 (two courses) beside granite; concrete block 255 beside concrete | Photo PM06: 226 +-15, setts not concrete; their brightness (1.35 to 1.7 times the road, wear target M24) is unchanged |
| crossover | 3.0 m, 6 mm upstand, one taper block | 3.0 m kept; lip of setts 15 mm; in-situ concrete ramp 1 in 7.4; granite flank strips; the taper block kept as a variant | Photo PM09 to PM12: the photographed crossing has no taper block |
| gully grate | 400 square, recess 50, dish 30 | 485 x 325 rectangle, 8 slots 29 x 285 with 28 bars (about 0.42 open), dish 15 | Photo PM13, PM14, PM28, PM30 |
| corner | none | mitred (133 degrees) and radius (6500) | Photo PM27 (urban_street_01), PM16 (urban_street_04) |
| tactile paving | none | none | period: see 4.9 |

What the present street gets right: the 125 upstand, the 255 depth, the channel course of about a quarter of a metre, a 3.0 m crossing, a gully in the channel on the east side, the crown. What it gets wrong or lacks is in the table above and in section 6.

## 2. Sources

All photographs are Poly Haven's, CC0 (read at https://polyhaven.com/license on 9 October 2026), used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused Wikimedia, Geograph, Flickr, archive.org, gov.uk, BSI and most of the web (list below), so **no photograph from 1975 to 2000 was reached: every photograph is from 2019**, and for each object the table says why it would look the same in 1990 or what differs.

| id | URL | date read | author | licence | date taken (lat, lon) | what it shows | used | period object or replacement | why the same in 1990 (or what differs) |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://polyhaven.com/a/urban_street_03 ; files via https://api.polyhaven.com/files/urban_street_03 (8k tone-mapped JPG) | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-09-07 07:46 UTC (published 2019-09-26) (51.481339, 0.006877) | An overcast Victorian terrace street in south-east London (south-east London, near the Greenwich meridian): granite kerbs with a granite-sett channel, a vehicle crossing with a concrete ramp, granite flank strips and a row of setts as the lip, rust-brown cast-iron gully grates, a large recessed utility cover in the footway, patched flags. THE MAIN PHOTOGRAPH. | yes (main) | Mixed. The granite kerbs, setts and cast-iron grates are period-type objects (Victorian to 1970s, laid long before 1990); the concrete ramp looks 1970s-80s (weathered exposed aggregate); the yellow lines and the car are 2019. | Granite kerbs and sett channels were laid in the 19th and early 20th century and kept; cast-iron gratings to BS 497 (1976) were the 1990 norm; vehicle crossings with a concrete ramp and granite or concrete flanks were common in the 1970s-80s. Differences in 1990: the stone would be sootier and the channel dirtier; no 2000s dropper-block crossing with tactile blisters; no ductile-iron hinged grates. |
| S2 | https://polyhaven.com/a/urban_street_01 ; files via api.polyhaven.com | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-08-18 07:09 UTC (51.528295, -0.053879) | A resurfaced Bethnal Green street with a new granite build-out: granite kerb blocks, a mitred corner (about 133 degrees), a planter kerb. | yes (corner) | REPLACEMENT: the kerbs are new (2010s sawn-top granite, cleaner than 1990); the form (mitred corner, joint width, block length) is period. | Granite kerb corners were mitred or cut to radius in the same way for a century; in 1990 they would be older, chipped and dirtier. |
| S3 | https://polyhaven.com/a/urban_street_02 | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-08-18 06:45 UTC (51.526655, -0.056465) | An estate road: a square cover filled with tarmac (hairline outline, grass at the corners). | yes (tarmac-filled recessed cover) | Period-type object, old tarmac. | Recessed covers re-surfaced with tarmac are 1970s-1990s practice; it looks the same. |
| S4 | https://polyhaven.com/a/urban_street_04 | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-09-14 12:58 UTC (sunlit) (51.511786, -0.201884) | A Notting Hill / Bayswater street: a large-radius granite kerb corner, a long two-leaf studded cover in the carriageway, a small recessed footway cover. | yes (corner radius, road cover, small cover) | Granite kerb is Victorian; the road cover is utility ironwork of unknown age (a reinstatement patch around it). | Studded steel or iron utility covers in a pale mortar surround are 1960s-90s; a London-smart street, so the wear is cleaner than a port town's. |
| S5 | https://polyhaven.com/a/bethnal_green_entrance | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-08-18 07:01 UTC (51.526915, -0.054044) | A block-paved estate entrance with a double-triangular square stud-pattern cover (two leaves split on a diagonal, 10 x 10 studs; the cover is 0.9 m from the nadir, so its size is +-8 %). | yes (stud cover) | The block paving is 1990s-2000s; the cover is older ironwork re-set in it. | Cast square-stud treads are 1960s-80s; same. |
| S6 | https://polyhaven.com/a/birbeck_street_underpass | 2026-10-09 | Andreas Mischok | CC0 1.0 (Poly Haven) | 2019-08-18 06:53 UTC (51.525806, -0.056277) | A tarmac street under a railway arch: a pale concrete bullnosed kerb with a worn aggregate top, kerb-face yellow marks, a cast-iron gully grate with oval-trimmed slots. | yes (concrete kerb, second grate) | Concrete kerb probably 1970s-90s; grate probably 1980s or later (rust-brown cast iron). | Concrete bullnosed kerbs were laid from the 1960s; the grate type is BS 497 (1976) style; same in 1990, newer-looking. |
| S7 | https://polyhaven.com/a/metal_grate_rusty ; https://api.polyhaven.com/files/metal_grate_rusty (2k diffuse) | 2026-10-09 | Photography Dimitrios Savva, processing Rob Tuytel | CC0 1.0 (Poly Haven) | published 2022-07-07 (taken date not given) | A 500 mm tile of a rusty cast tread plate (raised alternate horizontal and vertical lugs). | yes (lug pattern, measured by autocorrelation) | A scan of real ironwork of unknown age. | Lug treads of this type are 20th-century iron. |
| S8 | https://polyhaven.com/a/water_manhole_cover ; https://api.polyhaven.com/files/water_manhole_cover (glTF 1k and .bin) | 2026-10-09 | Raunox | CC0 1.0 (Poly Haven) | published 2023-11-08 (a modelled asset, not a photograph) | A weathered round cast-iron manhole cover model: 690.76 x 690.76 x 67.62 mm, lid radius about 294 mm. Its texture atlas is not used. | yes (frame and lid sizes only) | Modelled asset. | A 600 class round cover with a 690 frame is 20th-century standard. |
| S9 | repository: production/cloud-week/targets/SCENE-SLOTS.md; production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md; production/research/street-clutter-1990/SUMMARY-2026-09-29.md; production/research/street-wear/WET-ROAD-2026-10-08.md; production/cloud-week/targets/wear/TARGET.md and target.json | 2026-10-09 | the project | the project's own | 2026-09-29 to 2026-10-08 | the street's present kerb, channel, gully and crossover; the asset plan's kerb and cover rows; the wear target's channel and grate numbers | yes (Read numbers) | n/a | n/a |
| S10 | WebSearch result summaries (9 October 2026): BS 7263 Part 1 (1990) kerb types HB2, BN2, BN3 and dropper kerbs; BS 497 Part 1 (1976) manhole covers, road gully gratings and frames, superseded 1994 by BS EN 124; tactile blister paving first laid in Parliament Square in 1983, the Department's guidance dated 1998 | 2026-10-09 | search summaries of third-party pages (NBS Source, a kerb supplier, Southwark and Edinburgh councils, BSI shop pages, CIHT and Euroblind articles, trid.trb.org) | n/a (leads only) | n/a | leads | NO numbers taken except where a line says "lead"; none changed a photograph-based number | n/a | n/a |
| S11 | https://polyhaven.com/a/docklands_01 and docklands_02 ; limehouse | 2026-10-09 | Savva Zakharov (docklands); Andreas Mischok (limehouse) | CC0 1.0 (Poly Haven) | 2025-03-11 and 2025-03-20 (docklands); 2019-05-19 (limehouse) (53.346038, -6.237996) | Docklands: granite setts and recessed covers on a quay; the coordinates 53.346, -6.238 are DUBLIN, not Britain. Limehouse: block paving, cast bollards, chain. | NO. Looked at and left out: Dublin is not a British street (its covers and setts carry Irish ironwork); Limehouse is a clean 1980s-90s development. | n/a | n/a |

**Unreached** (a page that refused is not evidence; nothing was taken from any of these):

| what | result | used |
|---|---|---|
| Wikimedia Commons, Geograph, Flickr, archive.org, Historic England, Hathitrust, National Archives | refused (connection 403/000) from this cloud on 9 October 2026 | nothing |
| gov.uk and assets.publishing.service.gov.uk (the Department's tactile paving guidance of 1998, Inclusive Mobility) | refused; only search summaries seen | nothing (a lead for "no tactile paving in 1990") |
| BSI knowledge and shop pages (BS 7263, BS 340, BS 435, BS 497) | refused; only search summaries seen | nothing (leads) |
| ambientCG manhole-cover and grate scans (ManholeCover001 to 011, Grate001, Grate002; CC0) | the catalogue API answered but every download (ambientcg.com/get?file=...) was refused with 403 | nothing |
| Sketchfab, Pexels, Unsplash | refused | nothing |

**Method.** Each panorama is the 8k tone-mapped JPG. A rectilinear view or a flat ground picture is re-projected from it with numpy (`make_previews.py`), camera height 1.6 m, proved by the 75 mm yellow line (PM22: 72 mm read, within 4 %). Heights are found from angles (`measure.py`: a vertical face at ground distance d = 1.6 m / tan(foot angle) has its top at 1.6 m - d tan(top angle)). On a ground picture, anything above the plane is smeared outward by 1600 / (1600 - z); the kerb-top picture (camera 1.475 m) is true for things 125 mm up. The photographed crossing (urban_street_03) has two main pictures, the ground plane and the kerb-top plane, at 3 mm a pixel; `self_check.py` looks for the drawn edges on them.

## 3. The frame, the levels, the pivots

* Plan frame: x along the kerb; y across, 0 at the kerb face line (the foot of the face, at the channel), + toward the carriageway, - toward the footway; z up from the top of the channel setts at the kerb foot. [Judgement]
* Levels: kerb top z = +125 (granite); footway flags +120 (5 below the kerb top; Photo: a visible joint, little step; Judgement for the 5); the road at the channel edge +6 and rising 1 in 40, +75 at 3 m (Read: scene). The asphalt edge stands 6 mm up on the setts and is ragged. [Photo, Judgement]
* Pivots: kerb block at the block centre on the face line at channel level; the crossing assembly at the centre of the gap between the two end blocks, y = 0, z = 0; grates and covers at the centre of the lid at its top surface; the corner at the corner point on the face line.
* Units in the glb: metres (divide by 1000), z up, scale 1; one mesh per piece kind, variants as material slots or separate meshes.

## 4. The target, part by part

Every number carries its kind: **Read** (printed in the repository), **Scaled** (measured off a drawing: none here), **Photo** (measured on a photograph: method and error in section 5), **Derived** (computed from the others), **Judgement** (a trade or period guess, said so).

### 4.1 Granite kerb block (`kerb_granite`; about 85 % of the run)

Section in the plan frame (points in `target.json` `pieces.kerb_granite.section_yz`, y then z):

`[[0, -130], [0, 45], [-25, 100], [-25.48, 104.88], [-26.9, 109.57], [-29.21, 113.89], [-32.32, 117.68], [-36.11, 120.79], [-40.43, 123.1], [-45.12, 124.52], [-50.0, 125.0], [-190, 125], [-190, -130]]`

* Upstand 125 (the street's 125 Read; Photo-consistent: PM01 and PM02 read 118 and 113 to the arris middle, which stands 7 below the top). **Upstand and batter are one measurement, not two:** PM01, PM02 and PM26 all read the same ray, from the camera to the middle of the arris, against the same foot; upstand and set-back trade about 0.39 mm of height per mm of set-back and the three readings disagree by about 15 mm. Read with a vertical face the ray puts the arris middle at about 129 mm (PM26) or 113 to 118 (PM01, PM02), and a review at two places read 129 and 133 with a vertical face and 119 to 123 with the 25 mm batter, so 125 with the batter stands [Photo-consistent with PM26 and the upstand together, not separately measured; Judgement for the split]. Top width 190, face line to the rear joint (Photo PM01 181, PM02 185, PM25 189; error +-10). Depth 255, the lower 130 buried (Read: the street's 255).
* Face HALF-BATTERED: vertical from the foot to z = 45, then sloping back 25 mm by z = 100 (about 25 degrees from vertical), then the top arris rounded R 25 (centre y = -50, z = 100) into a flat top 140 wide (Photo-consistent with PM26: the arris middle stands 29 +-9 behind the foot line, the model's is 32; Judgement for the split with the upstand, see above). The rear face vertical. The end arris R 10. [Photo; Judgement for 45 and R 25]
* Length: random in 800 to 1200, mean 1000, never two neighbours within 20 (Photo PM04: 0.84, 1.01, 1.14 m, +-30). Joint 9 +-3, open and silt-dark, no mortar fillet on the face (Photo PM05). Laying scatter: face line +-4 between neighbours, top level +-3, tilt up to 1.5 degrees; one joint in twelve opens to 15. [Photo, Judgement]
* Surface: top fine-picked granite, grain 1 to 3 mm, polished at the front half by tyres and feet; face self-faced, rougher and darker with grime; end faces dressed with chipped edges. [Photo]
* Pieces needed: straight block (random length), end block (square end, arris R 10), the crossing's two end blocks, the corner blocks (4.6).

### 4.2 Concrete kerb block (`kerb_concrete`; three runs of 4 to 8 blocks per side, about 20 m of the 96 m of kerb)

Section (y, z): `[[0, -145], [0, 50], [-0.74, 59.39], [-2.94, 68.54], [-6.54, 77.24], [-11.46, 85.27], [-17.57, 92.43], [-24.73, 98.54], [-32.76, 103.46], [-41.46, 107.06], [-50.61, 109.26], [-60.0, 110.0], [-160, 110], [-160, -145]]`

* Bullnosed: upstand 110, top width 160, front arris a full rounding R 60 over the top 60, flat top 100, depth 255 (145 buried). Length 915 (Read: the street's block), joint 8 pointed flush, cracked in places. [Photo PM03: upstand 96.5 to the arris middle, width 166 at the measured upstand, a re-surfaced street; Judgement for R 60]
* Surface: weathered concrete with fine aggregate showing and sparkling, paint blips allowed (the lines family places them). [Photo]
* The standard it comes from (a search lead, not read): BS 7263 Part 1 (1990), types HB2 and BN2 (125 x 255 x 915). The photographed kerbs are wider than 125 (above).

### 4.3 Channel

* **Granite sett channel** (beside the granite kerb): two courses, long side along the kerb. Course A (kerb side) y 0 to 115, B 115 to 225; total 225 [Photo PM06: 226 +-15; Read: the scene's 255 is kept for the concrete channel]. Sett along the kerb 130 to 230, mean 180 [Photo]; joints 12 with dark mortar recessed about 8, one joint in four open to 20 [Photo]. Top z = 0, domed 4 mm, level scatter 3, course B up to 5 lower where worn [Judgement]. The asphalt edge at y = 225, 6 mm proud, ragged by 10 to 50; over about a third of a run the asphalt laps 30 to 50 onto course B (so the visible channel is 180 to 195 there; in front of the crossing course B shows to 225), and the setts stay modelled to 225 underneath [Photo, review]. Long fall 1 in 80 toward the gully, cross-section flat [Judgement].
* Profile (y, z): the channel top is flat at z = 0 from y 0 to 225; the asphalt edge rises to 6 at y 225 and 7.0 at y 260; the road is z = 6 + (y - 225) / 40 up to 75.4 at 3000 (the crown 75 mm above the channel: Read, scene). Point lists: `pieces.channel_setts.profile_yz`.
* **Concrete channel block** (beside the concrete kerb): 255 across, 125 deep, 915 long, joint 8 [Read: the scene's 255 and "the kerb's own concrete"; Judgement: BS 7263 channel 255 x 125, a lead].
* Colour of the setts: `colour_share` sett_pale_worn 0.35, sett_dull 0.50, granite_blue_grey 0.15 (the three materials of section 7). The clean mix averages about 1.78 times the road in linear light; after the wear family's channel body (x 0.85) about 1.51, and about 1.45 with the dark joints, inside the 1.35 to 1.7 of [Read: wear target M24] and of check `channel_over_road_brightness`.

### 4.4 The dropped crossover (`crossover`; one on the street, west side, x 22.5)

As photographed in urban_street_03 (a house crossing, 2.15 m between the kerb ends; the street's yard entrance takes the same form at 3.0 m [Read: scene]). From the footway to the road, in the plan frame:

| part | numbers (mm) | kind |
|---|---|---|
| end blocks | two granite kerb blocks, square vertical end faces, arris R 10, gap between their faces 3000 (the photograph 2145 +-30) | Read; Photo PM10 |
| flank strips | granite, 155 wide (stone between joints: left 171, right 140), y -917 to -202 (715 long), top z 120; right strip's inner face on the block end, the left strip's inner face splayed, a dark band 45 wide; joint to the ramp and to the kerb 12 | Photo PM12; Judgement (the one-of-each choice) |
| ramp | x from -1488 to +1488, y -917 to -137, in-situ concrete, z 15 at the front rising to 120 at the back (105 over 780, 1 in 7.4), brushed with exposed fine aggregate, one hairline crack across, a 10 to 20 bitumen or mortar joint to the flags at the back | Photo PM11 (917 against 924 +-40); Derived |
| lip row | y -125 to 0, setts 170 along (+10 joint, 17 setts, pitch 176.5), 125 across, top z 15 above the channel, blue-grey, pale grey and one pink-grey in 8 | Photo PM07 (171), PM08 (125), PM09 (12 +-8) |
| joints | 12 mm bitumen between ramp, lip and flank strips | Judgement; Photo (dark lines) |
| footway beyond | flags at z 120 | Judgement |

The scene's 6 mm upstand is the modern flush figure; the photographed lip stands 12 to 20 above the channel setts. The scene's "one taper block" is kept as a **variant** (`taper_variant`): a precast concrete dropper 915 long, 160 wide, top from z 110 falling to 5 (1 in 8.7), one per side, to be used only if the builder wants a precast crossing [Judgement: a search lead names BS 7263 HB2-to-BN3 droppers at 1:9; no photograph of one was reached].

### 4.5 Corners

* **Mitred corner** (`kerb_corner_mitre`): two granite arms of 900 mitred at the bisector, interior angle 133 +-5 degrees (Photo PM27: the kerb's road edges run at 57 and 11 degrees and the yellow lines at 61 and 13 to 16 on the 3.5 mm ortho, giving 134 and 133.5; 90 allowed for a street corner), joint 9, arris rounding carried round the mitre, a small chip at the corner [Photo urban_street_01: a build-out; its kerb is new, so cleaner than 1990].
* **Radius corner** (`kerb_corner_radius`): face radius 6500 (Photo PM16: the yellow line fits 6.8 m, 0.2 m off the kerb, +-0.6 m); granite blocks cut to the curve, 1200 along the arc (Photo: about 1.3 m), joints radial 9; the two sett courses follow the curve with wedge-shaped setts. [Photo urban_street_04; Judgement for the block length]
* Neither is in today's street; place them at a build-out or at a cross-street if the town gets one.

### 4.6 Gully grate A (`gully_grate_A`: the street's grate, east side x 12.0 [Read])

| number | value | kind |
|---|---|---|
| overall along the kerb x across | 485 x 325 | Photo PM13: 489 x 324 +-9 |
| slots | 8, each 29 wide x 285 long, pitch 57, slot field 428 (7 x 57 + 29) | Photo PM14 (field 289 px = 433, corrected after the review), PM28 (slots 25.5 to 34.5, median 28.5), PM30 (pitch 56.97, centre fitted to 1 mm) |
| end walls | 28.5 along the kerb, 20.0 across | Derived |
| bars | 28 wide (24 to 28.5 on the photograph), 45 deep (z), tops chamfered 2, slot 29 at the top narrowing to 25 (casting draught) | Photo PM28; Judgement (45, 2, 25) |
| open area | slot area over plan area, 8 x 29 x 285 / (485 x 325) = 0.42 +-0.04 (the photograph's black fraction is about 0.41); the grate reads about half iron, not two-thirds | Derived; Photo PM28 |
| slot direction | across the channel, perpendicular to the kerb | Photo |
| position | kerb-side edge y 100, far edge y 425: 100 mm from the kerb foot, 200 of it beyond the 225 channel in the carriageway | Photo (102 to 426) |
| set in | top flush with the setts (z 0 +-3); the asphalt dished 15 mm toward the grate over 150 on the carriageway side; the yellow line kinks around it (the lines family) | Photo; Judgement for 15 |
| pot | black void 300 deep below the slots, silt at the bottom, so the slots read black | Judgement |

The scene's 400 square, recess 50 and dish 30 are replaced (section 6). **Grate B** (`gully_grate_B`, optional second design): 7 slots 28 wide at pitch 58 (bars 30) whose lengths 125, 250, 350, 395, 350, 250, 125 trim the field to an oval, in a frame 490 x 445, with two round lifting holes 25 across on the long axis about 55 beyond the centres of the two end slots; raised marks cast on its centre bar stay blank [Photo, rough: a perspective view at 3.5 m, +-15 %].

### 4.7 Covers (four cast patterns, as the asset plan wants, plus small lids)

* **P1 double-triangular square-stud cover** (`cover_stud_square`): outer 960 square (Photo PM18: about 980 x 920, +-70; the cover is 0.9 m from the nadir), frame rim 20, lid 920 square, **two triangular leaves** split on one diagonal joint 5 mm wide, 10 x 10 raised square studs 45 across at pitch 95 (margin 10), 4 high with 15 degree draught and 1 mm worn arrises; the studs the joint crosses are cut into right-angled half-studs on both leaves (at least five visible along it); one round keyhole 20 across per leaf near the middle of the leaf; a small raised blank oblong boss 80 x 40 x 3 near the joint's lower end, where a maker's mark would go (it stays blank); no lifting pockets; gap to the surround 10, block paving or flags cut to it. [Photo PM17: lattice 97.7 and 91.1 at right angles; PM18; the review of bethnal_green_entrance for the split, count, keyhole and boss; Judgement for the second keyhole and 4 mm.] Two on the street, footway or carriageway.
* **P2 round 600 cover** (`cover_round_600`): frame outer diameter 690, lid 590, frame depth 68, ring 50, a centred lug lattice, lugs 36 x 10.5 x 2.5 high, each 71.4 x 83.5 cell holding 2 horizontal lugs at (0, 0) and (35.7, 41.75) and 2 vertical lugs at (35.7, 6) and (0, 47.75) (centres in mm; rows 41.75 apart, a horizontal and a vertical lug alternating every 35.7 along a row, each row shifted 35.7; `pattern.lugs_in_cell`, which `target_drawing.py` reads), a plain 25 band at the rim. [Read from the CC0 Poly Haven model: 690.76 overall, 67.62 deep, lid radius 294.1 (PM24); the lug lattice is read off the displacement map of a CC0 scan of a real tread plate (PM23, the review's reading); Judgement for the 600 class.] No lettering. Two in the carriageway.
* **P3 recessed infill cover**: *footway* `cover_recessed_footway`, telecom-style and blank: outer 1180 x 660, a cast frame whose top is cast with raised oblong lugs (36 x 10.5 x 2.5, rows 41.75 apart: two staggered rows along each long side, three columns across the wider left end and two across the right) in two bands, an outer 45 wide level with the flags and an inner 65 wide stepped 12 down [Photo for the pattern, a 7 m telephoto that cannot measure the lug; Judgement for the size and counts], infill 960 x 440 (a pale flag or concrete tray lid, 25 chamfer, top 8 below the flags). [Photo PM19: 1182 x 669 outer (+-50 along, +-100 across, seen at 7 m), infill 960 x 420, rim 126 on the left]. *Carriageway* `cover_recessed_road`: 1000 x 1050 filled with tarmac, only a 15 dark hairline in the surface, a darker square, grass and moss at the corners, a crack running out of one corner [Photo PM20: 1020 x 1065 +-40].
* **P4 two-leaf road cover** (`cover_road_double_leaf`): 1820 x 620, two leaves with a 15 gap across the middle, fine stud tread (studs 18 on a 45 degree lattice at pitch 33, 3 high, margin 30), a 150 band of pale mortar and lighter tarmac round it. [Photo PM21: 1824 x 600 +-150 at 7 m: shape and pattern only. The leaf split is **Judgement, not Photo**: on a 4 mm ortho the studded field is divided by more than one seam, at least one oblique to the long axis, and no single cross-joint at the middle was seen; its period is unproven (it sits in a fresh reinstatement), so one on the street.]
* **Small lids** (`service_small`), 3 stopcock, 2 gas, 1 telecom: stopcock round lid 135 in a 175 frame with a 30 x 8 slot [Judgement]; gas 240 x 130 lid in a 290 x 180 frame with a 25 x 8 slot at each end [Judgement]; telecom blank 360 x 160 recessed lid with flag infill in a 410 x 210 frame with a 30 pale mortar surround [Photo urban_street_04, +-30 %].
* **Lettering**: none on anything. If a letter is ever wanted: "SV", "WATER" or "GAS", 20 high, cast, no maker, no company; only once a photograph shows it. No maker's name, council name, crest, crown or cypher on any cover or grate. [Brief; canon owes the council's name]
* Every cover and grate top is flush with the surface it is set in (+-3), except the footway infill (8 below the flags, +-3).

### 4.8 Pieces and counts for the street (Judgement)

Covers 10 to 14: P1 x 2, P2 x 2, P3 footway x 2 and road x 1, P4 x 1, small lids x 6 (3 stopcock, 2 gas, 1 telecom blank). Grates 1 (the scene's, east x 12) to 3. Kerb 96 m (both sides of 48 m), crossing 1 (west x 22.5), corners 0 to 2.

### 4.9 Tactile paving: what the period did

None on Quay Street in 1990. The search summaries (leads, not read: the Department's guidance sits on gov.uk, which refused) say the blister surface was first laid at a crossing in Parliament Square in 1983 as a trial of research for the Department of Transport, and that the Department's guidance on tactile paving dates from 1998; a minor street's dropped kerb in 1990 has plain flags or concrete. No blister, no corduroy, no yellow or red surface at the crossing. (The asset plan reached the same view: "leave the cone off".) [Judgement, with leads]

## 5. Photograph measurements (raw readings recomputed by `self_check.py`)

| id | what | photograph | method | raw reading | result (mm unless named) | error | kind |
|---|---|---|---|---|---|---|---|
| PM01 | granite kerb section, block at the crossing's right end | urban_street_03 | pano_depression | rows read on a gridded view (ph-urban_street_03-kerb-end-flank-view.jpg); foot = bottom of the dark face, arris_mid = middle of the light-to-dark rounding, rear = the dark joint behind the top | foot_distance_mm 3880, upstand_to_arris_mid_mm 118.4, top_width_given_assumed_upstand_mm 162.7, assumed_upstand_mm 125, top_width_given_measured_upstand_mm 180.9 | rows +-8 (about +-0.08 degree): upstand +-12 mm, top width +-20 mm | Photo |
| PM02 | granite kerb section, straight run | urban_street_03 | pano_depression | luminance profile over columns 850 to 1050: top 125 to 145 grey levels, drop to 54 at rows 396 to 410, face 47 to 57, rear joint 90 at rows 316 to 322 | foot_distance_mm 3893, upstand_to_arris_mid_mm 113.3, top_width_given_assumed_upstand_mm 153.2, assumed_upstand_mm 125, top_width_given_measured_upstand_mm 185.4 | foot row +-15 (the shaded foot is soft): upstand +-15 mm | Photo |
| PM03 | concrete bullnosed kerb section (Birbeck Street) | birbeck_street_underpass | pano_depression | rounded top, no sharp arris; foot lost in a dark band | foot_distance_mm 3353, upstand_to_arris_mid_mm 96.5, top_width_given_assumed_upstand_mm 134.8, assumed_upstand_mm 110, top_width_given_measured_upstand_mm 166.5 | upstand +-15 mm, width +-25 mm (a worn, re-surfaced kerb) | Photo |
| PM04 | granite block lengths along the straight run (three whole blocks) | urban_street_03 | ortho_px_list | joint to joint along the kerb top | values_mm [1011.0, 837.0, 1143.0], mean_mm 997.0, min_mm 837.0, max_mm 1143.0 | +-30 mm each | Photo |
| PM05 | kerb joint width | urban_street_03 | angular_width | dark open joint in the kerb top, view yaw 100 pitch -22 fov 18 | width_mm 9.2 | +-3 mm | Photo |
| PM06 | channel width, kerb foot to asphalt edge (granite sett channel) | urban_street_03 | rows_height_corrected | foot row 403 (the base of the lip row; the soft shadow under the kerb starts to rise there); asphalt edge row 474 = the steepest brightness change, over columns 330 to 1100; the asphalt edge stands about 6 mm up so it is smeared outward 1600/1594 | width_mm 226.4 | +-15 mm; the asphalt overlay may have narrowed the channel | Photo |
| PM07 | lip setts along the kerb (seven whole setts) | urban_street_03 | ortho_px_list | joint to joint, blue-grey and pale setts | values_mm [195.0, 165.0, 165.0, 195.0, 195.0, 150.0, 135.0], mean_mm 171.4, min_mm 135.0, max_mm 195.0 | +-9 mm each | Photo |
| PM08 | lip row depth across the kerb (front top edge to the back joint centre) | urban_street_03 | ortho_px_list | rows 351 (dark joint centre) to 393 (front top edge) on the main frame: 42 px | values_mm [124.8], mean_mm 124.8, min_mm 124.8, max_mm 124.8 | +-9 mm | Photo |
| PM09 | lip upstand from the dark band under it | urban_street_03 | smear_height | a vertical face of height h at distance d smears d*h/(1.6 m - h) outward in the ground ortho; the dark band under the lip row is 10 px = 30 mm | height_mm 12.2 | +-8 mm | Photo |
| PM10 | crossing: gap between the two kerb block ends | urban_street_03 | ortho_two_edges | end faces at columns 185 and 900 of the top frame | length_mm 2145.0 | +-30 mm | Photo |
| PM11 | crossing: ramp back edge, distance behind the kerb foot | urban_street_03 | ortho_rows_to_distance | distance from camera = 5000 - 3 * row (mm); the difference is the ramp back edge behind the foot line | distances_mm [3791, 4715], difference_mm 924 | +-40 mm | Photo |
| PM12 | flank strip width and length (left and right) | urban_street_03 | ortho_px_list | stone widths between the joints on the top frame: left 57 px (171 mm: cols 78 to 135), right 47 px (140 mm: cols 900 to 947); lengths 250 and 235 px (left, right) | values_mm [171.0, 141.0, 750.0, 705.0], mean_mm 441.8, min_mm 141.0, max_mm 750.0 | +-12 mm | Photo |
| PM13 | gully grate A overall (along the kerb, across) | urban_street_03 | ortho_px_list | columns 205 to 368, rows 437 to 545 of the main ground frame | values_mm [489.0, 324.0], mean_mm 406.5, min_mm 324.0, max_mm 489.0 | +-9 mm | Photo |
| PM14 | gully grate A slot field and slot pitch | urban_street_03 | ortho_px_list | CORRECTED after the review: slot field 289 px on the 1.5 mm preview (columns 170 to 459, first slot left edge to last slot right edge: 433 mm; the first reading, 278 px, took the first slot's left edge 6 px too far in), slot length 190 px, mean slot pitch 38 px (slot centres at 182, 218, 258, 297, [335 hidden under a leaf], 372, 410, 448); 8 slots. Slot widths at half level 25.5 to 34.5 (median 28.5) and bars 24 to 28.5 (PM28) | values_mm [433.5, 285.0, 57.0], mean_mm 258.5, min_mm 57.0, max_mm 433.5 | +-3 mm on pitch; +-8 on lengths | Photo |
| PM15 | grate B slot pitch (Birbeck Street) from the perspective view | birbeck_street_underpass | angular_width | seven slots at columns 330, 430, 530, 650, 760, 880, 990 of a 1400 px wide, 12 degree view (yaw 0.96, pitch -23; the preview is the same view reduced to 1200 px); pitch about 108 px; the slots stand about square to the view, so no foreshortening is applied | width_mm 57.4 | +-6 mm | Photo |
| PM16 | corner radius, circle fit to the yellow line of the corner | urban_street_04 | circle_fit_px | yellow line centre line found per column by colour, circle fitted by least squares; the line stands about 0.2 m off the kerb | radius_to_line_mm 6816, radius_face_mm 6616, centre_px [660, -208] | +-0.6 m | Photo |
| PM17 | stud cover: lattice pitch | bethnal_green_entrance | lattice_vectors_px | neighbouring studs on the rectified ortho (1.5 mm a pixel); the two vectors are at right angles (a square lattice) | pitch_a_mm 97.7, pitch_b_mm 91.1, dot_cos 0.011 | +-8 mm | Photo |
| PM18 | stud cover: outer edges | bethnal_green_entrance | edge_lengths_px | top edge and right edge of the cover on the 1.5 mm ortho, 0.9 m from the nadir; CORRECTED after the review: the top edge runs about 650 px along (the first reading, 515, was short), giving about 980 x 920 mm | lengths_mm [980.8, 890.1] | +-70 mm | Photo |
| PM19 | recessed utility cover in the footway: outer and infill | urban_street_03 | ortho_px_list | outer 394 x 223 px, infill 320 x 140 px, left rim 42 px; 7 m from the camera, so across-the-kerb sizes are +-100 mm | values_mm [1182.0, 669.0, 960.0, 420.0, 126.0], mean_mm 671.4, min_mm 126.0, max_mm 1182.0 | +-50 mm along, +-100 mm across | Photo |
| PM20 | tarmac-filled recessed cover | urban_street_02 | ortho_px_list | hairline outline columns 300 to 640, rows 440 to 795 | values_mm [1020.0, 1065.0], mean_mm 1042.5, min_mm 1020.0, max_mm 1065.0 | +-40 mm | Photo |
| PM21 | two-leaf studded road cover | urban_street_04 | ortho_px_list | long axis and width on a 4 mm ortho 7 m away | values_mm [1824.0, 600.0], mean_mm 1212.0, min_mm 600.0, max_mm 1824.0 | +-150 mm | Photo |
| PM22 | yellow line width (scale proof for camera height 1.6 m) | urban_street_03 | ortho_px_list | rows 548 to 572 at column 900; the line is 75 mm, so the scale is within 4 % | values_mm [72.0], mean_mm 72.0, min_mm 72.0, max_mm 72.0 | +-5 mm | Photo |
| PM23 | tread pattern cell (Poly Haven metal_grate_rusty, 500 mm tile) | metal_grate_rusty | listed | FFT autocorrelation peaks at 292 px (71.3 mm) and 342 px (83.5 mm) took only the axis peaks and missed the centred lattice; the lug centres on the displacement map give 2 horizontal and 2 vertical lugs per 71.4 x 83.5 cell | period_x_mm 71.4, period_y_mm 83.5, row_spacing_mm 41.75, row_shift_mm 35.7, lug_mm [36, 10.5] | +-2 mm | Photo (a texture scan of real ironwork) |
| PM24 | round cover model: outer diameter, depth, lid radius | water_manhole_cover | listed | vertex rings at radius 294.1, 313.4, 345.4 mm | outer_diameter_mm 690.76, depth_mm 67.62, lid_radius_mm 294.1, ring_inner_radius_mm 313.4 | exact (a model) | Read (a model's geometry, not a photograph) |
| PM25 | granite kerb, face line to the rear joint, on the kerb-top plane | urban_street_03 | ortho_px_list | top frame, right block: the dark fall of the arris is centred at row 400 and the face line is row 403; the rear joint's front edge is row 340: 63 px; the light top alone is rows 340 to 397 (171 mm) | values_mm [189.0], mean_mm 189.0, min_mm 189.0, max_mm 189.0 | +-9 mm | Photo |
| PM26 | granite kerb: how far the middle of the arris stands behind the foot line (a battered face) | urban_street_03 | setback_from_rows | top frame: the middle of the light-to-dark fall over the right block is row 399.5 (rows 394 to 406 over columns 959 to 1109); on the kerb-top plane a point 7 mm lower is drawn 0.5 % nearer, which is corrected; foot row 403 on the ground frame | set_back_mm 29.3 | +-9 mm | Photo |
| PM27 | mitred granite corner: interior angle (urban_street_01) | urban_street_01 | corner_angle | interior angle = 180 minus the difference of the two runs' directions: 134 from the kerb edges, 133.5 from the yellow lines | interior_edges_deg 134.0, interior_lines_deg 133.5, mean_deg 133.8 | +-5 degrees | Photo |
| PM28 | grate A: slot and bar widths on the 1.5 mm preview (the review) | urban_street_03 | listed | the slots are about as wide as the bars, not two-thirds iron | slot_width_median_mm 28.5, slot_width_min_mm 25.5, slot_width_max_mm 34.5, bar_width_min_mm 24.0, bar_width_max_mm 28.5, black_fraction 0.41 | +-3 mm | Photo |
| PM29 | grate B (Birbeck Street): slot width, bars, lifting holes (the review, rough) | birbeck_street_underpass | listed | rough: perspective view | slot_width_mm 28.0, bar_width_mm 30.0, lifting_hole_diameter_mm 25.0 | +-15 % | Photo |
| PM30 | grate A: centre and pitch of the slot field (centroids of the seven visible slots on the main ground frame) | urban_street_03 | listed | the slot field is centred at x -751 in the crossing's plan frame; the pitch is 57.0; the slots are 28.6 wide at half level | x_centre_mm -751.3, pitch_mm 56.97, residual_std_mm 1.0, slot_width_half_level_mm_mean 28.6 | +-2 mm on the centre and pitch; +-3 on widths | Photo |

## 6. Where the photographs win over the scene and the books

| item | scene or book | photograph | chosen | why |
|---|---|---|---|---|
| kerb top width | 125 (Read: scene; BS 7263 HB2/BN2 125 x 255, a lead) | 181 and 185 on two granite blocks at the measured upstand and 189 on the kerb-top ortho (face line to the rear joint); 166 on the concrete kerb at its measured upstand | granite 190, concrete 160 | three readings of granite agree within 8 mm; the 125 is a catalogue width for a precast kerb; the visible top runs from the face line to the dark joint under the flag |
| kerb face profile | no profile stated in the scene; a search lead names BS 7263 HB2 half-battered and BN2 bullnosed | the middle of the arris stands 29 +-9 mm behind the foot line on the granite kerb (a battered upper face); the concrete kerb is fully rounded | granite half-battered (vertical to 45, back 25 by 100, arris R 25); concrete bullnosed (R 60) | photographs win |
| kerb upstand | 125 (Read) | 113 to 118 to the middle of the arris rounding on granite (so about 125 to the top); 96 on a resurfaced concrete kerb | granite 125 (kept), concrete 110 | inside the error; a re-surfaced road eats 15 mm |
| kerb block length | 915 uniform (Read; BS block 3 ft) | whole granite blocks 0.84, 1.01, 1.14 m | granite random 800 to 1200 (mean 1000); concrete 915 | old granite kerb came in random lengths; the 915 block is the concrete one |
| channel material | concrete ("the kerb's own concrete"; wear target channel_concrete) | two courses of granite setts, 10 to 12 mm mortar joints, pale and worn | granite setts beside granite kerb; concrete channel block only beside the concrete kerb | the photograph shows setts; their brightness (1.35 to 1.7 times the road, Read from the wear target) is unchanged |
| channel width | 255 (Read; also the width of a BS concrete channel block) | 226 +-15 (two courses of setts, foot to asphalt edge) | 225 for the granite sett channel (two courses of 4.5 inch setts; the photograph gives 226 +-15); 255 kept for the concrete channel block | photographs win; the scene's 255 is the width of a BS concrete channel block |
| gully grate | 400 mm square, recess 50, dish 30 (Read) | 489 x 324 rectangle, 8 slots 29 wide (25.5 to 34.5) x 285 at pitch 57, bars 28 (24 to 28.5), slots across the channel, black fraction about 0.41, dish about 15 mm, kink in the yellow line | 485 x 325, 8 slots 29 x 285, bars 28; dish 15; recess and dish of the scene dropped | photographs win; the 400 square is a trade guess |
| dropped crossover upstand and taper block | 6 mm upstand, one taper block (Read) | a row of granite setts stands 12 to 20 mm proud as the lip; a ramp 0.9 m deep at 1 in 7.4; granite flank strips; no taper block | lip 15 mm, ramp and flank strips; the taper block kept as a precast variant (Judgement, a lead) | the photographed crossing is the period form; 6 mm is the modern flush figure |
| corner | asset plan: "kerb blocks ... drop kerb, corner" (no figures) | a mitred corner of about 133 degrees (build-out; PM27) and a radius corner of about 6.5 m (granite blocks cut to the curve) | both, as two pieces | both seen |
| tactile paving | asset plan: "leave the cone off" | no tactile surface on any dropped kerb in the photographs (the crossing in urban_street_03 is plain concrete); they are 2019 and say nothing about 1990 | none | leads: first trial 1983, guidance 1998; a minor street in 1990 has none |
| grate slot and bar widths | none printed (the first draft of this target: slot 18, bar 39) | slots 25.5 to 34.5 (median 28.5), bars 24 to 28.5; the black fraction is about 0.41 (PM28; PM14 corrected to a 289 px field) | slot 29, bar 28, slot span 428, end walls 28.5, open fraction 0.42 | the review re-measured the grate; the first draft read the slot field 11 px short |
| stud cover construction | none printed (the first draft: one lid, 8 x 8 studs, 860) | two triangular leaves on one diagonal joint with half-studs along it, 10 x 10 studs, outer about 980 x 920, a round keyhole about 20, a blank raised oblong boss about 80 x 40; no oblong lifting pockets | two triangular leaves, 10 x 10 studs, outer 960, keyholes and a blank boss | photographs win (the review re-read the Bethnal Green cover) |
| round cover tread lattice | none printed (the first draft: one horizontal and one vertical lug per 71.3 x 83.5 cell) | a centred lattice: 2 horizontal and 2 vertical lugs per 71.4 x 83.5 cell, rows 41.75 apart, 36 x 10.5 lugs (PM23) | lugs_in_cell with four lug centres | the autocorrelation had taken only the axis peaks |
| footway cover frame top | none printed (the first draft: a flat outer flange) | the cast frame carries rows of small raised oblong lugs over its whole top (a 7 m telephoto: pattern yes, lug size no) | a lugged frame (P2 lug 36 x 10.5 x 2.5, rows 41.75 apart) | photographs win; the lug size is Judgement |
| channel setts colour shares | wear target M24: the channel reads 1.35 to 1.7 times the road | pale and dull setts mixed with some blue-grey (the lip row and channel boxes of PM sample set) | sett_pale_worn 0.35, sett_dull 0.50, granite_blue_grey 0.15 | without shares the clean setts could not land the channel inside 1.35 to 1.7; at these shares about 1.51 after the grime |
| asphalt laps the outer sett course | channel course 255 (Read) | beyond the crossing's right end block the asphalt covers the outer 30 to 50 mm of course B, so the visible channel is 180 to 195; in front of the crossing course B shows to 225 | 225 modelled underneath; the asphalt laps 30 to 50 over about a third of a run | photographs win |
| cover and grate lettering | the brief: blank or generic words if photographed | no lettering legible on any cover or grate in the photographs | none | nothing photographed; "SV" "WATER" "GAS" allowed only if a photograph shows them |

## 7. Materials and colours (sRGB, clean surfaces; the grime, shade and wet are the wear family's)

All albedos are on the wear target's road scale (asphalt_dry 89/86/80 [Read]): each photograph colour is divided by the road beside it in linear light and multiplied by 89/86/80. **Gully-grate iron has ONE base colour, the wear target's iron_grate 58/54/52 [Read]; the rust comes from the wear target's grate_wear (mark 100/72/56). The 92/74/66 of the first draft is now only the EXPECTED composite on the bars (the photograph reads 88/75/76 to 125/109/103), kept to check the result, so the rust is not put on twice.** Metal is 1 for bare iron; the rust skin is dielectric, so use metal 0.3 where rust covers more than half a surface. Wet: roughness falls and albedo darkens by the wear target's wet rows (grate_wear 0.85, roughness -0.3; gutter_grime 0.8, roughness -0.55): nothing is darkened twice.

| key | plain name | sRGB (clean) | roughness 0-1 | metal | source and kind |
|---|---|---|---|---|---|
| granite_grey | dressed grey granite, fine speckle, worn smooth on top | 131/127/115 | 0.55 (matt, polished a little by feet on the top (0.40) and rougher on the face (0.70)) | 0 | Photo (kerb tops 138/135/138 and 153/152/161 against road 97/95/101), anchored to wear target kerb_granite 128/126/122 |
| granite_blue_grey | darker blue-grey granite (about 1 block in 5) | 103/105/101 | 0.55 (see name) | 0 | Photo (lip setts 109/114/129) |
| granite_pink_grey | grey granite with a pink cast (about 1 block in 20) | 139/125/111 | 0.55 (see name) | 0 | Photo (one pinkish sett 150/132/130 in the lip row), Judgement for its share |
| sett_pale_worn | channel setts, pale and worn, mortar lines dark | 141/133/119 | 0.6 (see name) | 0 | Photo (channel setts 153/147/149 near the grate, 115/108/109 farther along) |
| sett_dull | channel setts, dull and silted | 106/98/87 | 0.7 (see name) | 0 | Photo |
| concrete_kerb | pale warm-grey concrete kerb, fine aggregate showing, worn | 140/134/126 | 0.75 (see name) | 0 | Judgement; Photo (Birbeck Street kerb reads pale grey-brown with sparkling aggregate) |
| concrete_ramp | in-situ concrete, brushed, exposed fine aggregate, speckled pale and dark | 149/139/119 | 0.8 (see name) | 0 | Photo (161/153/148, speckle std about 14 grey levels on the photograph) |
| flag_pale | old concrete flag, pale | 124/117/102 | 0.75 (see name) | 0 | Photo; the footway family owns the flags |
| cast_iron_grate | cast iron gully grating, bare grey-black iron: the BASE is the wear target's iron_grate; the rust-brown bars come from its grate_wear (mark 100/72/56) | 58/54/52 | 0.7 (rough, rust matt; bar tops polished by wheels (0.45)) | 1 | Read: the base is the wear target's surfaces.iron_grate 58/54/52 (one base colour, so the rust is not put on twice); 92/74/66 is the EXPECTED RESULT on the bars after grate_wear, for checking it (Photo: bars 88/75/76 to 125/109/103 on a view where the road is 97/95/101) |
| cast_iron_cover | cast iron or steel cover, dark grey-brown, leaf-stained | 78/66/58 | 0.65 (see name) | 1 | Photo (Bethnal Green cover plate 112/95/85 under litter; 04 cover pale in sun); Judgement |
| mortar_pale | pale grey pointing and bedding mortar | 150/146/138 | 0.9 (see name) | 0 | Judgement |
| bitumen_joint | black bitumen joint filler | 30/28/28 | 0.6 (see name) | 0 | Photo (dark gap between ramp and flank strips) |
| tarmac_infill | tarmac in a recessed cover, the road's own colour | 89/86/80 | 0.85 (see name) | 0 | Photo; = wear asphalt_dry |

Colours as seen on the photographs (tone-mapped, not albedo): kerb tops 138/135/138 and 153/152/161, the kerb face in shade 38/38/35, the road 97/95/101, the ramp 161/153/148, lip setts 109/114/129 (blue-grey) and 157/156/160 (pale), channel setts 153/147/149 and 115/108/109, grate bars 88/75/76 and the slots 35/31/37, Bethnal Green's cover plate 112/95/85 under leaf litter.

## 8. Variants

* **kerb_granite**: count: 3; what: three colour variants (grey 75 %, blue-grey 20 %, pink-grey 5 %) x random length x laying scatter; wear states: clean top / chipped arris / tyre-polished front / weed at the foot
* **kerb_concrete**: count: 1; what: one section; 3 wear states (pointing cracked, arris spalled, paint blip); three runs of 4 to 8 blocks on the street, about 20 m of the 96 m of kerb, away from the crossing and the gully
* **crossover**: count: 2; what: A the photographed form (ramp + flank strips + sett lip) at 3.0 m on the west side at x 22.5; B the precast dropper variant (not used unless the builder wants a second crossing)
* **channel**: count: 2; what: granite setts (2 courses) beside granite; concrete channel block beside concrete
* **corner**: count: 2; what: mitred (angle 133 +-5, 90 allowed) and radius 6500; neither is in today's street: place at a build-out or at the cross-street end if the town adds one
* **gully_grate**: count: 2; what: A (8 slots 29 x 285, 485 x 325, on the street at x 12, east) and B (7 slots 28 wide oval-trimmed, 490 x 445, two lifting holes, optional second at the quay end); 3 wear states each; mirror along the kerb allowed
* **covers**: count: 4; what: four cast patterns (asset plan): P1 double-triangular square-stud cover (960 square, two leaves, 10 x 10 studs), P2 round 600 class with lug tread, P3 recessed infill cover (footway telecom-style 1180 x 660; carriageway tarmac-filled 1000 x 1050), P4 two-leaf fine-stud road cover 1820 x 620; plus small service lids (stopcock, gas, telecom blank)
* **street_counts_judgement**: covers 10 to 14: P1 x2, P2 x2, P3 footway x2 and road x1, P4 x1, small lids x6 (3 stopcock, 2 gas, 1 telecom blank); grates 1 (the scene) to 3

## 9. Wear and damage as the photographs show it

* **note**: what the photographs show; the numbers and masks belong to the wear family (gutter_grime, grate_wear, iron_wear, footway_infill): this lists the SHAPE-level wear the models carry.
* **kerb_granite**
  * top polished lighter at the front half (tyres, feet)
  * face dark with traffic film; the foot has a darker tide line
  * 1 block in 6 has an arris chip 20 to 60 mm long, 5 to 15 mm deep, or a chipped end
  * joints open and dark, 3 to 15 mm; a weed clump (100 to 150 mm) in a joint or at the foot about every 3 to 6 m of kerb (Photo: two in 4 m); leaf litter caught at the foot
  * blocks tilt up to 1.5 degrees and step 3 mm between neighbours
* **kerb_concrete**
  * pointing cracked and lost
  * arris spalled 10 to 30 mm, aggregate showing
  * paint blips across the top (lines family)
* **channel_setts**
  * mortar lost in 1 joint in 4, to 20 mm
  * setts polished pale on top, silt and leaf mulch in the joints, a sett missing or loose about 1 in 40
  * grit and mulch pile where the channel meets the grate (wear: gully piles)
  * a weed or two in the joints
* **crossover**
  * ramp: exposed aggregate, speckled, a hairline crack across it, bitumen joint black and cracked, dried needles and leaf mould in the joint at the left flank (a brown stain 150 wide)
  * flank strips: polished top, one chipped end, one splayed inner face dark
  * lip setts: blue-grey and pale setts with dark mortar, 1 in 8 pinkish
* **gully_grate**
  * bars rust-brown, tops polished by wheels, slots full of black silt
  * a leaf or two across the slots; litter caught; the asphalt around dished and cracked
  * the yellow line kinks around it (lines family)
* **covers**
  * stud and lug tops lighter where worn, sides and crevices rust-brown and black
  * leaf litter and grit in pockets and gaps
  * recessed infill cracked or chipped at the corner; a gap of 10 to 15 mm to the surround, grass or moss at the corners of the tarmac-filled one
  * pale mortar surround patched
* **what_is_not_here**
  * no gum, no cigarette ends, no oil: the wear family places them
  * no bright orange rust

## 10. Why each object is the same in 1990, or what differs

* **Granite kerbs and setts** (urban_street_03, 01, 04): dressed granite kerbs and sett channels were laid from the 19th century to the 1970s and kept; the same in 1990, but dirtier and sootier, and older kerbs are more often chipped and tilted. What differs: the 2010s build-out in urban_street_01 is new sawn granite (cleaner); the 2019 streets have been swept by machine more often than a 1990 channel.
* **Concrete kerb** (Birbeck Street): bullnosed concrete kerbs were laid from the 1960s; the same. BS 7263 Part 1 (1990, a lead) is the year's standard for the precast sections.
* **Crossover** (urban_street_03): ramp-and-flank crossings with a sett lip are 1970s-80s practice; the same. What differs from 2019 practice: no precast dropper blocks, no tactile blisters at the crossing, a steep ramp (1 in 7.4), a lip you can feel (15 mm, not 6).
* **Gully grate**: cast-iron gratings to BS 497 (1976, superseded 1994 by BS EN 124: a lead) were the 1990 norm; the photographed rust-brown cast grates look old and are the same. What differs: no hinged ductile-iron or galvanised "safe" grates, no anti-theft or cycle-slot patterns of the 2000s.
* **Covers**: cast or steel square-stud and tread covers and recessed infill covers are 1960s-90s; the same. What differs: no composite or plastic covers (2000s), no polymer-concrete lids, no coloured plastic stopcock caps, no operator logos.
* **Tactile paving**: absent in 1990 (4.9).
* **Poly Haven round-cover model and tread scan**: not photographs of a street; their age is unknown; the 600 class and the lug tread are 20th-century standard.

## 11. Checks the builder's automatic check must pass (unit 3.7)

The full list is in `target.json` under `checks` (41 checks). Each is a name, what to measure, the expected value and the tolerance:

| check | applies to | measure | expected | tolerance | kind |
|---|---|---|---|---|---|
| kerb_upstand_granite | kerb_granite | height of the top above the channel top (z of the flat top minus z = 0) | 125 | 8 | Read 125; Photo 113 to 118 to the arris middle |
| kerb_top_width_granite | kerb_granite | y extent of the flat top plus arris, face line to back | 190 | 15 | Photo PM01, PM02 (181, 185 at the measured upstand) and PM25 (189) |
| kerb_depth | kerb_granite, kerb_concrete | z from the top to the underside | 255 | 4 | Read |
| kerb_arris_radius_granite | kerb_granite | radius of a circle fitted to the top-front edge in section | 25 | 8 | Judgement; Photo (a worn rounding of about 25 mm) |
| kerb_face_batter | kerb_granite | face vertical from z = 0 to 45, then set back 25 mm by z = 100 (measured at the arris middle: 29 +-9) | {"vertical_to_z": 45, "set_back": 25} | {"vertical_to_z": 15, "set_back": 8} | Photo PM26 |
| kerb_block_length_granite | a run of 10 or more granite blocks | every length between 800 and 1200, mean 1000, no two neighbours within 20 mm | {"min": 800, "max": 1200, "mean": 1000} | 100 | Photo PM04 (0.84, 1.01, 1.14) |
| kerb_joint_width | kerb_granite | gap between neighbouring blocks at the top | 9 | 3 | Photo PM05 |
| kerb_concrete_section | kerb_concrete | upstand, top width, arris radius | {"upstand": 110, "top_width": 160, "arris_radius": 60} | {"upstand": 8, "top_width": 15, "arris_radius": 10} | Photo PM03; Judgement for the radius |
| kerb_concrete_length | kerb_concrete | block length | 915 | 5 | Read |
| channel_width | channel_setts | face line to the asphalt edge | 225 | 12 | Photo PM06 (226 +-15) |
| channel_width_concrete | channel_concrete | face line to the far edge of the block | 255 | 5 | Read |
| channel_courses | channel_setts | number of courses; across-widths A and B | {"courses": 2, "A": 115, "B": 110} | {"courses": 0, "A": 10, "B": 10} | Photo, Judgement |
| sett_length | channel_setts | sett length along the kerb, all | {"min": 130, "max": 230} | 15 | Photo |
| sett_top_level | channel_setts, lip_row | z of every channel sett top | {"min": -5, "max": 4} | 1 | Judgement; Photo |
| channel_over_road_brightness | channel_setts material after the wear family | luminance of the channel over the road beside it | {"min": 1.35, "max": 1.7} | 0.0 | Read: wear target M24 (Photo 1.35 to 1.7) |
| crossover_width | crossover | gap between the two end-block faces | 3000 | 20 | Read: SCENE-SLOTS 3.0 m |
| crossover_lip | crossover | z of the lip setts top; count of setts | {"z": 15, "count": 17} | {"z": 6, "count": 1} | Photo PM09 (12 +-8); Derived |
| crossover_ramp | crossover | ramp rise and run from the lip back edge to the back edge; back edge y | {"rise": 105, "run": 780, "back_y": -917} | {"rise": 8, "run": 40, "back_y": 40} | Photo PM11 (924 +-40) |
| crossover_flank | crossover | flank strip width, length, top z | {"width": 155, "length": 715, "top_z": 120} | {"width": 20, "length": 30, "top_z": 8} | Photo PM12 |
| crossover_watertight | crossover | largest gap between ramp, lip, flank strips and end blocks | 15 | 0 | Judgement (bitumen joint 12 mm) |
| gully_grate_overall | gully_grate_A | overall size along the kerb x across | [485, 325] | [10, 10] | Photo PM13 |
| gully_grate_slots | gully_grate_A | slot count; slot width x length; bar width; slot span; end wall along; pitch; slots perpendicular to the kerb | {"count": 8, "width": 29, "length": 285, "bar": 28, "span": 428, "end_wall_along": 28.5, "pitch": 57} | {"count": 0, "width": 4, "length": 8, "bar": 4, "span": 6, "end_wall_along": 4, "pitch": 2} | Photo PM14 (field 289 px = 433), PM28 (slots 25.5 to 34.5, bars 24 to 28.5) |
| gully_grate_open_fraction | gully_grate_A | slot area over the grate's plan area, 8 x 29 x 285 / (485 x 325) | 0.42 | 0.04 | Derived; Photo (the photograph's black fraction is about 0.41) |
| gully_grate_B | gully_grate_B | slot count, slot width, bar width, pitch; lifting holes (count, diameter, on the long axis about 55 beyond the end slot centres); raised marks on the centre bar blank | {"slots": 7, "width": 28, "bar": 30, "pitch": 58, "holes": 2, "hole_diameter": 25, "beyond_end_slot_mm": 55} | {"slots": 0, "width": 5, "bar": 5, "pitch": 4, "holes": 0, "hole_diameter": 4, "beyond_end_slot_mm": 15} | Photo, rough (PM29) |
| cast_iron_grate_base_colour | materials.cast_iron_grate | the base colour of the grate iron is the wear target's iron_grate; the rust comes from grate_wear (expected composite on the bars 92/74/66) | [58, 54, 52] | 0 | Read: wear target surfaces.iron_grate |
| gully_grate_place | gully_grate_A | y of the kerb-side edge | 100 | 15 | Photo (102) |
| gully_flush | gully_grate_A, covers | z of the top surface against the surface it is set in | 0 | 3 | Judgement (cover infill in the footway stands 8 below the flags, +-3) |
| cover_stud_square | cover_stud_square | outer; frame rim; lid; studs per row and column; pitch; stud size; stud height; leaves (2, triangular, one diagonal joint 5 mm with the studs on it cut to half-studs); keyhole per leaf; blank raised boss | {"outer": 960, "rim": 20, "lid": 920, "studs": 10, "pitch": 95, "stud": 45, "height": 4, "leaves": 2, "joint": 5, "keyhole": 20, "boss": [80, 40, 3]} | {"outer": 60, "rim": 5, "lid": 20, "studs": 0, "pitch": 4, "stud": 4, "height": 1, "leaves": 0, "joint": 2, "keyhole": 4, "boss": [10, 8, 1]} | Photo PM17, PM18 (980 x 920 +-70) and the review of bethnal_green_entrance |
| cover_round | cover_round_600 | frame diameter; lid diameter; depth | {"frame": 690, "lid": 590, "depth": 68} | {"frame": 5, "lid": 5, "depth": 3} | Read from a Poly Haven model (PM24) |
| cover_round_tread | cover_round_600 | lug lattice: cell; lugs per cell (2 horizontal, 2 vertical) at (0,0) and (35.7,41.75) horizontal, (35.7,6) and (0,47.75) vertical; lug size and height | {"cell": [71.4, 83.5], "lugs": 4, "lug": [36, 10.5], "height": 2.5} | {"cell": [1, 1], "lugs": 0, "lug": [3, 2], "height": 1} | Photo PM23 (the review: the centred lattice) |
| cover_recessed_footway_frame_lugs | cover_recessed_footway | raised oblong lugs 36 x 10.5 x 2.5 on the whole frame top, two staggered rows along the long sides, more across the wider left end (3 columns against 2) | {"lug": [36, 10.5], "height": 2.5, "row_pitch": 41.75} | {"lug": [4, 3], "height": 1, "row_pitch": 4} | Photo for the pattern; Judgement for the size |
| cover_recessed_footway | cover_recessed_footway | outer; infill | {"outer": [1180, 660], "infill": [960, 440]} | {"outer": [40, 60], "infill": [30, 40]} | Photo PM19 |
| cover_recessed_road | cover_recessed_road | outer square | [1000, 1050] | [50, 50] | Photo PM20 |
| cover_road_double_leaf | cover_road_double_leaf | outer; the leaf split is Judgement, not Photo | [1820, 620] | [100, 80] | Photo PM21 (rough); the split: Judgement |
| kerb_corner | kerb_corner_mitre, kerb_corner_radius | mitre interior angle (or 90); radius corner radius on the face | {"mitre_deg": 133, "or_deg": 90, "radius": 6500} | {"mitre_deg": 5, "or_deg": 2, "radius": 600} | Photo PM27 (133 +-5); PM16 (6.6 m +-0.6) |
| channel_setts_colour_share | channel_setts | colour shares of sett_pale_worn, sett_dull, granite_blue_grey; their linear mean over asphalt_dry after the channel body x 0.85 | {"shares": [0.35, 0.5, 0.15], "after_grime_over_road": [1.35, 1.7]} | {"shares": 0.0, "after_grime_over_road": 0.0} | the review (point 6); Read: wear target M24 |
| no_lettering | every cover and grate, mesh and textures | glyphs, crests, maker marks, council names, crowns | 0 | 0 | Brief |
| no_tactile_paving | the crossing and the street | blister or corduroy meshes or textures | 0 | 0 | Judgement; leads |
| pivot_and_units | every exported piece | pivot as in frame.pivot; metres; z up; scale 1 | "as stated" | 5 | Brief |
| colour_of_granite_top | kerb_granite material (clean albedo) | mean sRGB of the top texture | [131, 127, 115] | 10 | Photo (see materials.granite_grey.srgb) |
| drawing_match | each piece | silhouette of the built piece in plan and section at 1 mm a pixel against target_drawing.py polygons | 0.9 | 0.0 | min intersection over union; 0.95 for the kerb sections |

The edges `self_check.py` looked for on the main photographs (the drawing laid on the ground picture and on the kerb-top picture; scale fitted on one dimension only):

| edge | image | type | predicted (plan mm, height mm) | tolerance mm | what |
|---|---|---|---|---|---|
| foot_line_right_block | ground | step_low | y 0, z 0 | 15 | kerb face foot (the anchor of y = 0): the dark face, then the shadow ramp up to the setts, clear of the weed |
| lip_front_top_edge | ground | step | y 0, z 15 | 12 | light lip setts above, the dark band of their front face below |
| lip_back_joint | ground | line | y -131, z 15 | 12 | the dark joint between the lip row and the ramp (centre) |
| channel_asphalt_edge | ground | step | y 225, z 6 | 15 | pale setts above, asphalt below |
| grate_left_edge | ground | half_level | x -993.5, z 0 | 20 | setts left of the grate against its left end wall (the end walls are soft: +-20; the right edge is not visible against the setts, both 100 to 120 grey levels, so it has no probe; the slot edges below carry the grate's width) |
| grate_slot_tops | ground | step | y 122, z 0 | 12 | the upper ends of the black slots (frame 102 + end wall 20) |
| grate_slot_bottoms | ground | step | y 406, z 0 | 15 | the lower ends of the black slots (frame 426 - end wall 20) |
| slot1_left_edge | ground | half_level | x -965.0, z 0 | 6 | first slot, left side edge (slot 29 wide: centre -199.5 from the grate centre, edge at -14.5) |
| slot1_right_edge | ground | half_level | x -936.0, z 0 | 6 | first slot, right side edge |
| slot4_left_edge | ground | half_level | x -794.0, z 0 | 6 | fourth slot, left side edge |
| slot4_right_edge | ground | half_level | x -765.0, z 0 | 6 | fourth slot, right side edge |
| slot8_left_edge | ground | half_level | x -566.0, z 0 | 6 | eighth slot, left side edge |
| slot8_right_edge | ground | half_level | x -537.0, z 0 | 6 | eighth slot, right side edge |
| kerb_front_arris_right_block | top | step | y -32.3, z 117.7 | 15 | light top to dark face (the middle of the arris rounding) |
| kerb_top_rear_joint_right_block | top | line | y -196, z 125 | 15 | dark joint between the kerb top and the flag behind it (centre) |
| ramp_back_edge | top | step | y -917, z 120 | 18 | concrete ramp against the flags |
| flank_right_inner_joint | top | line | x 1069, z 120 | 15 | dark joint between the ramp and the right flank strip |
| flank_right_outer_joint | top | line | x 1221, z 120 | 15 | dark joint between the right flank strip and the dark flag |
| flank_left_outer_joint | top | line | x -1409, z 120 | 15 | dark joint between the pale flag and the left flank strip |

## 12. What the target could not settle

* The kerb top width (190 granite, 160 concrete), upstand (125, 110), face batter (25 mm back by z 100, PM26: 29 +-9) and arris radius (25, 60) rest on three views at 3.5 to 4 m with errors of 9 to 25 mm; the batter and the arris radius are read off one block each. A close photograph of a kerb end (Geograph, once reachable) would settle the profile.
* Whether Quay Street's old kerb is granite is Judgement: a port town's old quarter had granite kerbs and sett channels (the photographs show them in a Victorian street), but no photograph of a 1990 port-town street was reached.
* The channel width: 226 +-15 in one street (the street's granite 225); a second street with setts would show whether 225 or a wider sett course (up to 255) was usual.
* The round 600 cover's own pattern was not photographed: the lug tread comes from a CC0 scan of a real tread plate and the frame size from a CC0 model. A photographed British round cover is still owed.
* The stopcock and gas lids are Judgement (no photograph); BS 5834 (surface boxes) and the water and gas companies' drawings should be read once the network opens.
* Grate B (Birbeck Street) is measured only from a perspective view at 3.5 m: its slot lengths and frame are +-15 %.
* Gully grate dishing (15 mm) and the pot depth are Judgement.
* Whether a taper (dropper) block was used for house crossings in a 1990 port town: the photographed crossing used a concrete ramp with flank strips; the precast dropper (BS 7263, search lead) is kept as a variant.
* Tactile paving: leads say the first blister trial was 1983 and the guidance 1998; no 1985 to 1995 photograph of a minor-street dropped kerb was reached.
* Colours are ratios against the road on tone-mapped copies, not calibrated albedo; the wet-street look is the wear family's.
* No photograph from 1975 to 2000 was reached (Wikimedia, Geograph, Flickr, archive.org all refused): every photograph is 2019 and its 1990 sameness is argued, not shown.

## 13. What to read once the network opens

* BS 7263 Part 1 (1990) Precast concrete flags, kerbs, channels, edgings and quadrants: kerb sections (HB2, BN2, BN3), droppers, channels; and BS 340 (1979) it replaced.
* BS 435 (1975) Dressed natural stone kerbs, channels, quadrants and setts: the granite kerb and sett sizes (title and year from memory, to be checked).
* BS 497 Part 1 (1976) Manhole covers, road gully gratings and frames for drainage purposes (superseded 1994 by BS EN 124): grating sizes and slot patterns.
* BS 5834 (surface boxes for underground stop valves) and the gas and telecom operators' cover drawings, for the small lids.
* TRRL reports on road gully capacity (the search lead: "The drainage capacity of BS road gullies and a procedure for estimating their spacing"): grate sizes in use.
* The Department of Transport and DETR guidance on tactile paving (1998), the 1983 Parliament Square trial (Cranfield, Department of Transport research), and any 1985-92 local trial at a minor-street crossing.
* Highway authorities' standard details for vehicle crossings (1970s and 1980s drawings: ramp gradient, flank strips, dropper kerbs).
* Dated photographs 1975 to 2000: Geograph (CC BY-SA) searches for "dropped kerb", "granite sett channel", "gully grating", "stop tap cover"; Wikimedia Commons categories for cast-iron covers and gratings in England; Historic England Archive and a port town's local archive (Hull, Grimsby, Whitby, North Shields) for street scenes of the 1980s.
* IHT "Roads and Traffic in Urban Areas" (1987) and the Department's "Design Bulletin 32" for urban kerb and drainage details.

## 14. Narrow points applied after the review

The fresh review (TARGET-REVIEW.md: PASS, 0 faults, 11 narrow points) is applied in full; `self_check.py` now enforces the new values.

1. **Grate A slots and bars**: slot 29 (taper 29 to 25), bar 28, slot span 428, end walls 28.5, open fraction 0.42 +-0.04; PM14 corrected to a 289 px field, PM28 added; check `gully_grate_slots` now 29 +-4 and `gully_grate_open_fraction` added; six slot-edge probes (first, fourth and eighth slots, centre +-14.5, tolerance 6) and a slot-width test from their pairs, with the slot field's centre fitted to the photograph (PM30, x -751, 1 mm).
2. **Cover P1 is a double-triangular two-leaf cover**: outer 960, rim 20, lid 920, 10 x 10 studs (pitch 95, stud 45, margin 10), two triangular leaves on one 5 mm diagonal joint with half-studs along it, a 20 keyhole per leaf, a blank 80 x 40 x 3 boss, no lifting pockets; `cover_stud_square` check now 960 +-60, studs 10, leaves 2; the drawing clips the studs to the leaves.
3. **Cover P2 lugs**: cell 71.4 x 83.5 with `lugs_in_cell` (horizontal (0, 0) and (35.7, 41.75), vertical (35.7, 6) and (0, 47.75)), lug 36 x 10.5; `target_drawing.py` reads them; check `cover_round_tread`.
4. **Cover P3 footway frame** carries raised oblong lugs (P2's 36 x 10.5 x 2.5, rows 41.75 apart, two staggered rows on the long sides, more across the wider left end); `frame_steps` rewritten; the drawing shows them.
5. **Mitred corner about 133 degrees** (PM27 added, 133 +-5, 90 allowed); check `kerb_corner` added (mitre 133 +-5 or 90 +-2, radius 6500 +-600).
6. **Channel setts colour shares** 0.35 / 0.50 / 0.15, landing the channel at about 1.5 times the road after the wear family's grime; a test computes it.
7. **Handover** (`handover` in target.json): the wear target's gutter_grime band is 0.225 on granite stretches and 0.255 beside the concrete kerb, the grate is 0.485 x 0.325, and the grate iron has one base colour, the wear target's iron_grate 58/54/52 (92/74/66 is the expected composite). The line for NOW.md: Kerbs and covers target (unit 3.7): granite kerb 125 x 190 half-battered, setts channel 225 (concrete 255), crossover 3.0 m with ramp, flank strips and a 15 mm lip, gully grate 485 x 325 (8 slots 29 x 285), four cast covers; wear target: channel band 0.225 granite / 0.255 concrete, grate 0.485 x 0.325, iron base 58/54/52.
8. **Upstand and batter** reworded as one measurement (4.1 and `face_batter.kind`): Photo-consistent with PM26 and the upstand together, Judgement for the split; checks unchanged.
9. **Asphalt laps course B**: `meets_asphalt` now 10 to 50 wander, the asphalt lapping 30 to 50 onto course B over about a third of a run, the setts modelled to 225 beneath.
10. **Grate B**: slot 28, bar 30, two 25 lifting holes on the long axis about 55 beyond the end slots, raised centre-bar marks blank; check `gully_grate_B`; kind stays rough.
11. **Cover P4 leaf split** marked Judgement, not Photo; one on the street.

## 15. Files and credit

* This folder: `TARGET.md`, `target.json`, `target_drawing.py`, `self_check.py`, and the scripts that made them (`make_target.py`, `target_data.py`, `measure.py`, `make_doc.py`, `make_previews.py`). Run order: `make_target.py`, `make_doc.py`, `target_drawing.py OUT_DIR --overlay PREVIEW_DIR`, `self_check.py`. Pictures at 1 mm a pixel go to OUT_DIR (not into git); the reduced previews are in `production/previews/cloud-week/refs/kerbs-and-covers/`.
* **Self-check result** (last run): SELF-CHECK PASS: 191 of 191 tests pass (A printed numbers 34/34, B photograph measurements 67/67, C drawing on the photographs 30/30, D internal consistency 55/55, E text 5/5) (details in `target.json` under `self_check`).
* Previews, all crops of the object only (no people, no shop names, no number plates; a litter wrapper is masked with tarmac in the Birbeck grate view), JPEG at most 1200 px and under 300 KB. Each is derived from a CC0 Poly Haven panorama or texture and credited to its author: **Andreas Mischok** (urban_street_01, 02, 03, 04, bethnal_green_entrance, birbeck_street_underpass; CC0 1.0), **Dimitrios Savva (photography) and Rob Tuytel (processing)** (metal_grate_rusty; CC0 1.0).

| preview | source | what it shows |
|---|---|---|
| ph-urban_street_03-crossover-gully-ortho.jpg | urban_street_03, ground plane, 3 mm a pixel | THE MAIN PHOTOGRAPH: the crossing, lip, channel setts, gully grate |
| ph-urban_street_03-crossover-top-ortho.jpg | urban_street_03, kerb-top plane | the same crossing at kerb-top level: flank strips, ramp, kerb tops |
| ph-urban_street_03-target-on-photo.jpg | the drawing on the ground picture | orange lip setts, green channel setts, magenta grate, cyan slots, white foot line, yellow asphalt edge |
| ph-urban_street_03-target-on-top-photo.jpg | the drawing on the kerb-top picture | green kerb blocks and flank strips, yellow ramp back edge |
| ph-urban_street_03-granite-kerb-run-view.jpg | urban_street_03, yaw 100, pitch -22 | a straight granite kerb run with sett channel and grate |
| ph-urban_street_03-kerb-end-flank-view.jpg | urban_street_03, yaw 281, pitch -21 | the kerb end, the flank strip and the ramp edge, battered face |
| ph-urban_street_03-gully-grate-ortho.jpg | urban_street_03, 1.5 mm a pixel | grate A: 8 slots, bars, end walls |
| ph-urban_street_03-footway-cover-ortho.jpg | urban_street_03, footway plane | recessed telecom-style footway cover |
| ph-urban_street_02-tarmac-infill-cover-ortho.jpg | urban_street_02 | tarmac-filled recessed cover |
| ph-urban_street_04-road-cover-view.jpg | urban_street_04 | two-leaf studded road cover |
| ph-urban_street_04-kerb-corner-radius-ortho.jpg | urban_street_04, 10 mm a pixel | radius corner of granite kerb |
| ph-urban_street_01-kerb-mitred-corner-ortho.jpg | urban_street_01 | mitred granite corner |
| ph-bethnal_green_entrance-stud-cover-ortho.jpg | bethnal_green_entrance, 1.5 mm a pixel | square-stud cover |
| ph-birbeck_street_underpass-concrete-kerb-view.jpg | birbeck_street_underpass | concrete bullnosed kerb |
| ph-birbeck_street_underpass-gully-grate-view.jpg | birbeck_street_underpass | grate B, oval slot field |
| ph-metal_grate_rusty-tread-pattern.jpg | metal_grate_rusty (2k diffuse) | basket-weave lug tread |
| target-drawing-sheet.jpg | target_drawing.py | the drawings: sections, crossing plan, grate, covers, corner |
