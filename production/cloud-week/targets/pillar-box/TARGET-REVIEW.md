FAIL

# Pillar box on Quay Street: target review (cloud week 42, 9 October 2026)

A fresh reviewer, who did not write the target and will not build it, wrote this review. It covers TARGET.md, target.json, target_drawing.py, self_check.py, pb_numbers.py, scan_panoramas.py with panorama_scan.json, and the four previews. The review checked them against the earlier research (production/research/street-clutter-1990/SUMMARY-2026-09-29.md, section 1), the scene's stand-in (production/specs/vignette-scene.json, E4), canon.md and RULINGS.md.

**The special condition holds.** No photograph of a pillar box was reachable for this review either. Wikimedia Commons, Geograph, Flickr, archive.org, postboxmap.co.uk and lbsg.org all returned status 000 from this cloud on 9 October. So the photographs-win test cannot be run. Every point below marked *judgement* rests on the reviewer's own knowledge of 1950s-60s cast-iron Type A boxes. It is not evidence, and the first dated photograph overrides it.

**What was run.** Both scripts were run on a scratch copy in a mirrored tree under the session scratchpad, with all outputs kept there:

* `self_check.py` gives SELF-CHECK PASS, 175 of 175. This reproduces the writer's result, and target.json came out byte-identical after the run.
* `target_drawing.py` writes 74 polygons and four pictures. They were looked at.

**The writer's panorama search was re-checked.**

* api.polyhaven.com lists 997 HDRIs, 732 of them with coordinates. The writer's seventeen are exactly the ones in Great Britain. The other entries near 53.3 N 6.2 W are in Dublin, st_fagans_interior is a Welsh interior, and there is nothing in Northern Ireland.
* urban_street_01, urban_street_03 and urban_street_04 were re-downloaded. Their MD5s match the catalogue.
* All three were re-scanned with a looser threshold than the writer's, so that a box in shade would also be caught (saturation above 0.45, value above 0.12, 40 px at 4096 wide). The candidate crops and the horizon band from +20 to -35 degrees were then looked at by eye.
* The red things found were tail lights, brick arches and courses, a red front door, road-works barriers, an A-board and a Give Way sign. **No pillar box. The writer's finding stands.**

---

## Faults (1)

### F1. The height (1372) contradicts the repository's own figures for a Type A, and the slot, hood, cap and door stack hang on it

**Where.** TARGET.md summary line, 1 (the table), 4.2, 5 (height row) and 9.1 item 1. In target.json: `overall.total_height`, `numbers.total_height`, `profile.outer_rz` above z 1215, `parts.aperture`, `parts.door`, `parts.panels`, `parts.plates`, the checks, and self-check test A "total height lies inside the research's visible range 1350 to 1470".

**What is wrong.** The target reads the stand-in's *body* height (1.372, with a 0.10 cap and a 0.14 dome on top of it in the scene) as the whole box. It then justifies 1372 with the research's range of 1350 to 1470, which is "73 in casting less 15 to 20 in buried". The repository does not support that:

1. **The research's own Type A figures are higher.** The research gives "Working figures: about 150 cm above ground". Its modelling breakdown agrees: "Base ... about 20 cm", "Body: a cylinder ... about 115 cm tall", "The top is at about 150 cm". The target's body ends at 1215, against the research's 1350.
2. **The target takes the width from a source and leaves out that source's height.** The research line is: "An untraced source gives a Type A as **5 ft 4 in tall** and 1 ft 7¼ in (49 cm) wide." The target's body (489 = 19¼ in) comes from that line. The line's 5 ft 4 in (1626) appears nowhere in the target's height discussion: not in 1, not in 5, not in 9.1 and not in `photographs_win`. Item 9.1 frames the question as "1372, 1400 or 1470".
3. **The 73 in casting is a Type B's, by the target's own lead.** Lead 2.3, row 1, reads: "a salvage dealer's Carron EIIR box, 73 in tall, about 20 in in the ground, body 15 in wide (also sold as PB42/2, Type B)". The only support for a box under 1.47 m is therefore the casting length of the narrow box, not the Type A.
4. **The other figures in the repository cluster at about 1.6 m.** The scene's stand-in is 1612 in all. The leads (search summaries, not numbers) give a Type K of the same 19¼ in width at 63 in (1600) and a Type B at 64 in (1626).
5. **Judgement, not evidence.** A Type A stands about shoulder height on an adult man, roughly 1.5 to 1.6 m, and is a little over three body-widths tall. Its slot sits about mid-chest. At 1372 the box is 2.8 widths tall. The drawn front elevation reads squat: a short column with the slot at elbow height. That is the first thing a British player would notice, from any distance.

**The exact amendment.** Total height 1500, kind **Read** (the research's working figure, "the top is at about 150 cm"). Record 1626 (5 ft 4 in, the untraced Type A; the scene's 1612 agrees) as the upper alternative and 1350 to 1470 as a Type B's casting. Keep the slot "just under the cap" (the research, Read) by moving everything from the sill up by **+128**:

| item | now | amended |
|---|---|---|
| total height, dome apex | 1372 | **1500** (sagitta 80 kept; dome base 1420) |
| body | 140 to 1215 | 140 to **1343** |
| cap: soffit / cove top / rim / bead top / neck top | 1215 / 1228 / 1228-1250 / 1262 / 1292 | **1343 / 1356 / 1356-1378 / 1390 / 1420** (add 128 to every `profile.outer_rz` point with z ≥ 1215) |
| slot | 1127.5 to 1172.5, centre 1150 | **1255.5 to 1300.5, centre 1278** (320 x 45 kept) |
| hood | 1172.5 / front top 1195 / top 1205 | **1300.5 / 1323 / 1333** (10 under the soffit, kept) |
| sill | 1112 to 1127.5 | **1240 to 1255.5** |
| lettering area | 1062 to 1102 | **1190 to 1230** (cz 1210) |
| door | 280 to 1040 (760 high) | **280 to 1168 (888 high)**, 300 wide kept |
| roundel / collection frame / lock / enamel frame (cz) | 960 / 790 / 690 / 590 | **1088 / 918 / 818 / 718** (each the same distance under the door's top as now) |
| hinges (if kept, see N3) | z 420, 900 | **z 420, 1028** (each 140 in from the door's ends) |
| buried depth | 482, Derived from 73 in | drop the 73 in derivation (it is a Type B's casting); the hidden skirt stays 150 |

**What follows from F1.**

* **Checks.** Change these: `total_height` 1500 ±15; `dome_apex` 1500 ±10; `cap_soffit_height` 1343 ±8; `cap_rim_diameter` measured in z 1356 to 1378; `aperture_centre_z` 1278 ±12; `door_size` 300 x 888; `hinge_count_and_place` z [420, 1028]; `lock_place` z 818; `lettering_pad_blank` cz 1210; `cypher_roundel_blank` cz 1088; `collection_frame` cz 918; `enamel_frame` cz 718; `body_straight` over z 140 to 1343.
* **Self-check.** Test A's "inside 1350 to 1470" becomes "total height = research_working_height". Drop the test "buried depth inside 15 to 20 in".
* **Wear.** The soot band under the cap moves to z 1318 to 1343. The wear mask runs to 1500.
* **Handover lines.** Change them to "total height 1.500; the stand-in was 0.11 m too tall".
* **Item 9.1.1.** Reword it to "1500 (kept) or up to 1626; a photograph settles it".

The ratio becomes 1500 / 489 = 3.07 widths.

---

## Narrow points (each a small detail with an exact fix; for the writer before the builder starts)

### N1. The checks would not catch a wrong moulding: the failure mode of 8 October

Today a plain 536 x 22 disc for the cap rim, with no cove, bead or neck, passes every check. So does a foot with no quarter-round, splay or cove. Two checks are also worded so that a correct build could fail them.

**Add** this check:

```
{"name": "profile_silhouette",
 "applies_to": "foot, body, cap, dome",
 "measure": "on the back half (y < 0, clear of the casting seam), the mesh's radius every 2 mm of z from 0 to the apex, against profile.outer_rz interpolated; largest absolute deviation, mm",
 "expected": 0,
 "tolerance": 1.5,
 "kind": "Derived (the profile); 3.0 allowed within 2 mm of a bevelled edge"}
```

**Reword** these:

* `cap_soffit_height` must be measured "on the back half (y < 0)". At the front the hood exceeds the body's radius from z 1172.5, which would trip the check 42 mm early.
* In `lettering_pad_blank` and `cypher_roundel_blank`, "relief spread above its own plane" must become "relief measured radially above the pad's own curved face". A 300-wide pad that follows the cylinder departs 51 mm from a plane, and the 110 roundel departs 6 mm. As written, the check pushes the builder toward a flat pad, which would float or cut into the body.

### N2. The door is 4 proud, but the research says "a flush panel" (Read), and the target does not record the disagreement

**Fix:**

* `door.proud` becomes **1** (outer radius 245.5). The 3 x 3 joint groove stays, and is what shows.
* Check `door_proud` becomes 1 ±1.
* The plate frames keep their face plane where it is now (y = 254.5), which makes `bezel_proud_at_axis` 9.
* Add a row to `photographs_win.disagreements`.

### N3. The external barrel hinges are likely wrong (judgement)

A Type A's door hangs on internal hinges, for security: a knocked-out pin would open the box. From outside only the door's joint line shows on the hinge side. Two 26 x 96 red knuckles with bare iron pin heads would be an invented feature, visible close up.

**Fix:**

* Remove the hinge knuckles and pin heads from the geometry. Keep "hinged on the left" as the side of the joint only.
* Replace checks `hinge_count_and_place` and `hinge_size` with: "no part on the door's left edge stands more than 1.5 mm proud of the door face".
* In 7.5, drop the "two hinge knuckles" rust-bleed sources. In 7.7, drop "one dark rust trickle under the left hinge" and put that trickle under the hood's left end instead.

### N4. The cap's overhang is less than the hood's projection

* The research (Read) says the rim is "a few centimetres proud of the body". The target's rim is 23.5 proud, while the hood under it stands 30 proud.
* So in the side elevation the hood sticks out past the cap's rim. Judgement: on a Type A the cap's rim is the outermost line above the foot, and the hood tucks inside it.

**Fix:**

* `cap_radius` becomes **280** (rim diameter 560, 35.5 proud). The cove keeps its height and runs from 244.5 out to 280.
* Check `cap_rim_diameter` becomes 560 ±6.
* The hood stays 30 proud, now 5.5 inside the rim.

### N5. The blank roundel, blank pad and blank enamel plate read as placeholders (judgement, plus the project's own rule)

* A real box carries its cypher and lettering as raised letters directly on the iron. It has no blank disc and no blank tablet.
* The scene file says of a street name plate: "a blank white plate on a wall is a placeholder that looks like a bug". The same holds for a blank ivory plate in a frame on the door.

**Fix:**

* Delete `plates.enamel_frame` and `plates.enamel_plate`, and their check. The box carries one plate.
* Make the roundel and the lettering pad **flush reserved areas** with no raised geometry: `reserved_for_cypher` (on the door, cz 1088 after F1, 110 across) and `reserved_for_lettering` (300 x 40, cz 1210 after F1). Their checks become "no geometry, relief 0 within the area".
* The minted cypher is cast there once canon supplies it.
* The `plates_blank` variant becomes "no plate and no frame" rather than an empty white plate.

### N6. Facing the road leaves the poster on the kerb edge (judgement)

* The foot stands 312 mm from the kerb's back. A road-facing aperture means anyone posting a letter stands on the kerb edge or in the channel.
* A kerbside box on a 2 m footway faces the footway (the building line) or along it.
* It also matters for the game: the player walks the footway, and would see the box's plain back.

**Fix:**

* `frame_numbers.scene.front_faces` becomes "the building line".
* Check `front_faces_road` becomes `front_faces_footway`, expected 0 ±10 degrees from the direction pointing at the buildings.
* Tell the scene owner, because StreetVignette.cs places the stand-in's slot on the road side. This is the scene's Read figure against judgement. If the scene owner keeps the road side, record why.

### N7. target.json leaves two placements to the drawing script

The drawing script fills these in, but target.json does not say them in words, and a builder from target.json alone would have to guess.

**Fix:**

* `panels.lettering_pad_BLANK` (or the reserved area of N5): add "curved, concentric with the body, outer radius 247.5".
* `hinges` (if any survive N3): add "knuckle axis on the door's outer face, r 248.5, at x -150".

### N8. The keyhole shutter (judgement, low confidence)

A box's keyhole cover is painted with the door and worn at its edge, not bright brass.

**Fix:** paint the shutter red 150/30/32, metal 0, with dark bare metal 60/52/46 on its edge only. If the writer keeps brass, record it as Memory.

### N9. Two small slips in 2.2

* "About 400 older panoramas have no coordinates": the catalogue has **265** (997 listed, 732 with coordinates).
* "4096 to 20000 px wide": every one of the seventeen tone-mapped JPGs is **8192** wide (panorama_scan.json `source_px`).

Correct both numbers.

### For the first photograph, not changed now

* **The slot's width.** 320 is 65 % of the body's width. Judgement, low confidence: a 1950s-60s Type A's slot is nearer half the body's width. The target's own lead says the aperture was widened to 8 in in 1957, without saying which dimension. Keep 320 (Read) until the photograph, and read it there second, after the height.
* **The dome's rise (80) and the 30 mm neck.** These read plausibly in the drawing. Do not move them without a photograph.

---

## What is right

**The kinds are honest.**

* No number is called Photo or Scaled. 91 numbers carry their kind: 45 Read, 7 Derived and 39 Judgement, with "Memory" flagged on every judgement from general knowledge.
* `total_height` is honestly marked Judgement (Memory/Read).
* The self-check's part B tests that nothing is claimed.
* The reviewer spot-checked the scene's E4 figures, the research's quoted strings, the kerbs target's +110 and +115, and the wear target's red and black. All of them trace.

**The sources are honest.**

* Unreached sources are listed and used for nothing. The reviewer confirmed them unreached.
* Leads are kept out of the number registry.
* The Poly Haven material is CC0, used only for the search, and not reproduced.
* The panorama search is complete and correct (verified above).

**The type is right.**

* An EIIR-era Type A of the 1950s-60s follows the research's recommendation, and is right for an old port quarter in 1990.
* The Type K is a variant that is not built. The Penfold is avoided.
* There is no finial on the dome, which is right for the type (judgement).

**These numbers agree with each other and with the research:**

* body 489, matching the research's 49 cm, 19 in and 19¼ in, and the leads;
* foot 576, read as the scene's 597;
* black band 200 (Read), covering the foot and the lowest 60 mm of the body;
* red 150/30/32, the same as the wear target;
* the slot "just under the cap", with a hood and a sill (as in the research);
* the front stacked in the right order (judgement): slot, lettering, door with the cypher at its top, the collection plate below it, and the lock at the side;
* the stack checked for overlaps, with 19 mm or more between items.

**The canon is safe.**

* There is no cypher, crown, "POST OFFICE", "ROYAL MAIL", "ER", "GR", maker's name or date anywhere.
* "COLLECTIONS", "MON-FRI", "5.30 PM", "SAT" and "12 NOON" name no company, operator, council, maker or reign. They are the generic words any collection notice needs, the times are invented and plausible for 1990, and they break no content rule.
* The checks `no_marks` and `plate_words` enforce this.

**It is buildable.**

* The lathe profile is a point list, every part has numbers and a place, and the materials carry sRGB, roughness and metal.
* The plate text has sizes and places, and the font comes from production/fonts (OFL).
* The scripts run, and the drawing comes from target.json alone.
* Apart from N7, unit 3.6 could build it from target.json alone.

**The wear and the lighting are thorough and usable.** This covers the chips and paint layers, the strip of 8 repeats of 192 mm round the girth, the base, the aperture, grime, rust bleed and flyposting, and the sodium-lamp note (by night the box reads dark olive-brown, not red), which the lighting people need.

**The writer's own "could not settle" list is the right list.** It needs only the corrections to item 1 above.

---

## (6) Fit to build without a photograph?

**Not as it stands, because of F1.** Once F1 is amended, with N1's silhouette check added and N2 to N5 applied, the target is fit to build **one sample** as the street's replacement for the stand-in. That sample is not multiplied, and not put to the gate or on Jafar's page.

The gate is a check against real references, and it cannot be run without a photograph. So the piece is "ready for review", not done, until a photograph comes, and the photograph overrides every Judgement and Memory number.

**The single photograph that would settle the most:**

* **What:** a dated, square-on front view of a 1950s-60s EIIR Type A on a provincial British street, the whole box from the footway to the dome.
* **How taken:** camera about 1 m up and 4 to 6 m away, with the kerb's 125 mm upstand or a standing person in the frame for scale.
* **Where from:** from this PC, since the cloud cannot reach it: Geograph or Wikimedia Commons, CC BY-SA or freer, licence and date read on the file page.
* **What it settles at once:**
  * the height;
  * the slot's width and height above the footway;
  * the cap's overhang and the dome's rise (both visible in silhouette);
  * the door's size, and whether any hinge shows;
  * the order and sizes of the cypher, lettering and plate.

---

## Re-review (try 2)

PASS

Re-reviewed 9 October 2026 by the same reviewer. This round looked at the amended TARGET.md, target.json (47 checks), self_check.py, target_drawing.py and the four new previews.

**What was run.** All on a fresh scratch copy (a mirrored tree under the session scratchpad; outputs kept there):

* `self_check.py` gives SELF-CHECK PASS, 212 of 212. This reproduces the writer's result, and target.json came out byte-identical after the run.
* `target_drawing.py` writes 67 polygons; the elevations, section and plans were looked at.
* The new `profile_silhouette` check was **tested on real meshes**. The script built lathe meshes with bpy (a bmesh spin, 64 segments round) from `profile.outer_rz` and from altered versions of it. It then applied the check exactly as worded: on the back half, the mesh's largest radius at every 2 mm of z from 0 to the apex, against the profile interpolated. The tolerance was 1.5, with 3.0 allowed within 2 mm of the rim's lips.

There are **no faults**. The one fault and all nine narrow points are truly answered (details below). There are five new narrow points, each with an exact fix; the first must be made before unit 3.6 runs its check.

### The fault and the nine points: answered?

| | answered? | how it was checked |
|---|---|---|
| F1, the height | **yes** | `total_height` 1500, kind Read (the research's working figure). 1626 is recorded as the upper alternative and 1350-1470 as a Type B's casting, not used. The `buried_depth` derivation is dropped. Every number from the sill up is +128, as written: soffit 1343, rim 1356-1378, bead to 1390, neck to 1420, apex 1500; slot 1255.5-1300.5 (centre 1278); hood 1300.5 / 1323 / 1333; sill 1240-1255.5; lettering area 1190-1230; door 280-1168; cypher area cz 1088, frame cz 918, lock z 818. The checks, the self-check's test, the soot band (1318-1343), the mask (to 1500), the accent area (0.78 m2) and the handover lines (0.11 m too tall) all follow. Height to body width is now 3.07. |
| N1, the checks | **yes, with one new flaw (R1 below)** | `profile_silhouette` exists. `cap_soffit_height` and `body_straight` are measured on the back half. Both reserved-area checks measure relief radially above the curved face. On real meshes the new check **fails a plain 560 disc cap** (35.3 mm off at z 1344) and **fails a foot without its round, splay and cove** (43.2 mm at z 50). It also fails subtler moulding errors: the foot's round as a 12 mm chamfer (4.9), the cap bead as a square corner (12.0), the cap cove as a 45 degree chamfer (14.5). It **passes a correct build** (0.00), a correct build with a 1.5 mm bevel on the rim's lower lip (1.24), and a cove built as a true ellipse in 4 segments (1.05). |
| N2, a flush door | yes | `door.proud` 1, outer radius 245.5, check 1 ±1. The frame's face stays at y 254.5 (9 above the door), and a row in section 5 records the disagreement. |
| N3, no hinges showing | yes | The knuckles and pins are gone from parts, drawing and plans (a self-check test covers this). `door_left_edge_flush` replaces the hinge checks. The rust trickle is now under the hood's left end (7.5, 7.7). |
| N4, cap over hood | yes | Cap 560 (35.5 proud). The hood at 274.5 sits 5.5 inside the rim: check `hood_inside_cap_rim`, and the side elevation shows it. |
| N5, no placeholders | yes | The cypher and lettering areas are flush with no geometry, the enamel plate and frame are deleted ("none"), and the `no_plate` variant is a flush door. |
| N6, facing | yes | The front faces the building line. `front_faces_footway` replaces `front_faces_road`. The scene owner is told in 9.2, which says to record why if the road side is kept. The road side is now the back in the wear (the scrape, the sticker). |
| N7, placements in words | yes | The door and both reserved areas are "concentric", with their radii (245.5, 244.5, 245.5). |
| N8, the keyhole shutter | yes | Painted 150/30/32, metal 0, with a 1 mm bare edge 60/52/46. Check `keyhole_shutter_paint`. |
| N9, two slips | yes | "265 without coordinates" and "8192 px wide" are corrected, recorded as numbers and tested. |

**Canon** still holds. The only words are COLLECTIONS, MON-FRI, 5.30 PM, SAT and 12 NOON. There is no cypher, crown, "POST OFFICE", "ROYAL MAIL", operator, reign or maker's mark, and `no_marks` and `plate_words` are intact.

**Number kinds** are still honest: 91 numbers (46 Read, 11 Derived, 34 Judgement), no Photo, no Scaled, and Memory flagged.

### New narrow points, each with an exact fix

These are for the writer, or for unit 3.6 to apply as written.

**R1. `profile_silhouette`, as worded, refuses correct builds that are off by an invisible fraction of a millimetre.**

The check reads the radius at a fixed z. Where the profile runs nearly horizontal, a tiny height error turns into a large radius error: the dome near its apex, the cove arriving at the rim's lip, and the top of the foot's round. On the real meshes, a correct build fails in three ways:

* placed **0.3 mm high**: 15.2 mm off at z 1500, and 7.2 at z 1356;
* placed **1 mm high**: 28.7 mm off. The datum check allows 3 mm, the height check 15 and the apex check 10, so the checks contradict each other;
* with the dome built as a **true sphere in 8 rings** instead of the profile's 20 points: 1.9 mm at z 1498.

The self-check's own proof missed this, because its "correct build" test moves the profile only in r, by 0.8 mm, never in z.

**Exact fix.** The measure becomes:

> "on the back half (y < 0, clear of the casting seam), the section's outline in the r-z plane against profile.outer_rz from z 0 to the apex: the largest nearest distance either way (every point of the outline to the profile, and every point of the profile to the outline, sampled every 0.5 mm along each), mm"

* expected 0, tolerance **1.5**;
* drop the 3.0 bevel allowance, which is no longer needed: a 1.5 mm bevel on the rim's lip gives 0.57 under this measure.

Tested on the same cases, this measure:

* **fails** the plain cap (13.0), the plain foot (28.9), the foot chamfer (3.5), the square bead (4.9), the cove chamfer (5.0) and a dome rise of 100 instead of 80 (20.0);
* **passes** the exact build (0.00), 1 mm high (1.00), 0.3 mm high (0.30), the true-sphere dome (0.38) and the bevelled lip (0.57).

Add those two kinds of case (a z shift and a different dome tessellation) to the self-check's proof.

**R2. `dome_sagitta` has an ambiguous reference height.** "the z of the dome's base circle (r 250)" matches every z from 1390 to 1420, because the 30 mm neck stands at r 250. Measured from 1390, a correct build reads 110 and fails the 80 ±6. This was already in the first draft and the first review missed it.

**Exact fix:** "apex z minus the highest z at which the profile radius is 250 (the top of the neck, 1420)".

**R3. Nothing says the reserved areas are painted like their surroundings.** The drawing tints them, and the preview's caption says "tinted here only to show where", but target.json does not.

**Exact fix:** add to both reserved areas "painted the surrounding red (body or door), with no tint, outline or mask in any texture: invisible on the built box". Add a check: "albedo within each reserved area equals the surrounding paint within 3 per channel".

**R4. A slip in `parts.door.placement`.** It says "half angle 37.0 degrees", while `half_angle_deg` and TARGET.md say 37.7 (asin(150/245.5) = 37.66).

**Exact fix:** change "37.0" to "37.7".

**R5. The bevels table names an edge that has no place at the footway.** It lists "foot band bottom 2.0", but the profile runs straight from the hidden skirt (z -150) through z 0 to 48 at r 288, so there is no edge at the footway. A builder could read it as a 2 mm groove at the ground line.

**Exact fix:** rename it "skirt bottom (z -150, hidden), 2.0", or delete it.

### Judged again, without a photograph (judgement, not evidence)

At 1500 high and 3.07 body-widths, with a 560 cap overhanging a hood that tucks under it, a slot at chest height (1278), a flush door with no hinges showing, one plate and a lock on the right, all facing the footway, the box no longer reads squat or invented.

What remains open are exactly the things the target already lists for the photograph: 1500 against 1626, the slot's width (320), the dome's rise and neck, and the order of the cypher, lettering and plate.

### (6) Fit to build without a photograph?

**Yes, for one sample, once R1's fix is applied** (without it the automatic check can refuse a correct build). R2 to R5 can be applied by the builder as written.

Build one box as the street's replacement for the stand-in. It is not multiplied, and not put to the gate or on Jafar's page. It stays "ready for review", not done, until one photograph comes, because the gate's check against real references cannot be run without one. The photograph overrides every Judgement and Memory number.

**The single photograph that would settle the most:**

* **What:** a dated, square-on front view of a 1950s-60s EIIR Type A on a provincial British street, the whole box from the footway to the dome.
* **How taken:** camera about 1 m up and 4 to 6 m away, with the kerb's 125 mm upstand or a standing person in the frame.
* **Where from:** from this PC: Geograph or Wikimedia Commons, CC BY-SA or freer, licence and date read on the file page.
* **What it settles at once:** 1500 against 1626, the slot's width and height, the cap's overhang and the dome's rise in silhouette, the door's size, and the order of the cypher, lettering and plate.
