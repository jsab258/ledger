# Quay Street's pillar box: the target (cloud week 42, 9 October 2026)

**Quay Street's pillar box is a cast-iron cylinder of the 1950s-60s standard "Type A" pattern, painted pillar-box red (sRGB 150/30/32) above a black base band 200 mm high: body 489 mm across, a 576 mm foot, a 536 mm cap with a shallow 80 mm dome, 1372 mm above the footway in all (the stand-in's cap and dome go INSIDE that height, not on top of it), a 320 x 45 mm letter slot at 1150 mm under a 30 mm hood, a 300 x 760 mm hinged door (two barrel hinges, a keyhole escutcheon) carrying a blank cypher roundel, a blank lettering pad and two plate frames (the collection plate says only COLLECTIONS, MON-FRI 5.30 PM, SAT 12 NOON; the enamel plate is blank), and no cypher, crown, operator lettering or maker's mark; no photograph of a pillar box was reached, so no number below is measured on a photograph: every size is the repository's earlier figures (Read), derived from them, or the writer's judgement, and the first dated photograph overrides them.**

Written 9 October 2026 for the family "pillar box on Quay Street" (scene line furniture E4, east side, x 27.0). Units are millimetres unless a line says otherwise; the .glb is metres, z up, scale 1, the pivot the box's axis at the footway surface. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, a section, plans); `self_check.py` tests them. Last result: SELF-CHECK PASS: 175 of 175 tests pass (A printed numbers 57/57, B photograph measurements 10/10 [none exist: it tests that none is claimed], C drawing 18/18 [no photograph: nothing laid on one], D internal consistency 50/50, E text and canon 40/40) (`/home/user/.bpyenv/bin/python -I self_check.py`; it runs the drawing, regenerates the profile from pb_numbers.py and was itself tried on eleven deliberately broken copies of target.json, ten of which it refused at once and one (a hand-edited profile point) only after a regeneration test was added)

## 1. What the street's stand-in gets right, and what this target changes

Today's stand-in (SCENE-SLOTS.md and vignette-scene.json, read 9 October): a body cylinder 0.597 across and 1.372 high with a cap cylinder 0.66 across and 0.10 high and a dome 0.14 on top of it, so 1.612 m in all; a box slot 0.32 x 0.045 at 1.15 m; no cypher, no lettering. It is "a trade-standard guess, not a photograph".

| | the stand-in | this target | why |
|---|---|---|---|
| height above the footway | 1612 (body 1372 + cap 100 + dome 140) | 1372 in all | the earlier research's own range is 1350 to 1470 (73 in casting less 15 to 20 in buried); the scene's 1.372 is read as the whole box |
| body | 597 across | 489 across (19 1/4 in) | the research: 49 cm and 19 in; the 597 is read as the FOOT's size (576 chosen) |
| foot | none | 576 across, 48 mm band, splay, cove to the body at 140 | every standard box stands on a wider moulded foot |
| cap | 660 across, 100 high | 536 across: cove, rim, bead (z 1215 to 1292) | the research: the rim is "a few centimetres proud of the body" |
| dome | 140 | 80 (rise / diameter 0.16) | a shallow bowl, not a hemisphere; Judgement, no photograph |
| aperture | 320 x 45 at 1150 | kept; hood 30 proud over it, sill lip below, flap behind | the research: "a horizontal slot with a small hood just under the cap" |
| door, hinges, lock, plates, pads | none | all of them, the pads and the roundel blank | brief: the front door of 8 October failed on furniture its target never wrote down |
| colour | one "metal" | red 150/30/32, black band 35/35/36 to 200, white plate enamel, brass shutter | wear target and research |

What the stand-in gets right: the place (east side, x 27.0, 0.6 m behind the kerb), the facing (the aperture on the road side), the slot's size and height, and "NO CYPHER, NO LETTERING" as the rule for the postal marks.

## 2. Sources

**No photograph of a pillar box was reached today.** The cloud's network refuses Wikimedia, Geograph, Flickr, archive.org, Sketchfab and the rest (listed under Unreached); the one open host with photographs is Poly Haven (CC0), and none of its British panoramas, models or textures shows a pillar box (the search is in 2.2). So nothing below is Photo-measured and nothing is laid on a photograph (there is no main photograph, so the brief's "drawing laid on the main photograph" does not exist; `self_check.py` says "NOT RUN" for it and claims nothing). The earlier research (production/research/street-clutter-1990/SUMMARY-2026-09-29.md, section 1) also warned that "most links show surviving examples photographed after 2000" and that "photographs taken 1985 to 1995 in northern England were not found"; this target goes one step further down: there is no photograph at all, of any date.

### 2.1 What was read, and what for

| id | where | date read | author | licence | date taken | what it shows or gives | used |
|---|---|---|---|---|---|---|---|
| S1 | production/specs/vignette-scene.json, furniture E4_pillar_box and street, lighting, as read by StreetVignette.cs (PillarBox, Furniture, Columns) | 2026-10-09 | the project | the project's own | 2026-09-02 to 2026-10-08 | the stand-in's sizes, place, setback (the box's axis 0.60 m behind the kerb's back), the east lamp column at x 28.0, the lantern colour | yes: Read numbers |
| S2 | production/cloud-week/targets/SCENE-SLOTS.md, BRIEF.md | 2026-10-09 | the project | the project's own | 2026-10-08 | the pillar box row; the brief's rules | yes |
| S3 | production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 1 (the project's earlier reading, done on the PC) | 2026-10-09 | a helper, saved by the builder | the project's own | 2026-09-29 | the type (EIIR Type A of the 1950s-60s; Type K from 31 July 1980), the listing and untraced sizes (73 in, 15 to 20 in buried, 19 in, 15 in, 1 ft 7 1/4 in), "Red body, black base", base about 20 cm, the modelling breakdown. Its photographs (Geograph 4378457 Tenby, 10 May 2008; Geograph 24094 Kirkby in Cleveland, 5 July 2005, Mick Garratt, CC BY-SA) are links only, and Geograph is unreached from this cloud, so they were NOT seen | yes: Read numbers, cited as the project's earlier reading, with its caution |
| S4 | production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md | 2026-10-09 | the project | the project's own | 2026-10-03 | "Bodies: lathe and box primitives with caps, rims, slots, hinges, lettering panels"; mid-poly, a bevel on every edge; "canon owes ... the pillar box's cypher" | yes |
| S5 | game-design/research/art-direction.md R-B4; production/specs/vignette-bill-of-materials.md | 2026-10-09 | the project | the project's own | 2026-09 | the accent budget: red boxes are the street's whole high-chroma accent; the frame's saturation > 0.6 share non-zero and under 0.078 | yes (6.3) |
| S6 | production/cloud-week/targets/kerbs-and-covers/target.json and TARGET.md | 2026-10-09 | the kerbs writer | the project's own | 2026-10-09 | footway flags +110, kerb top +115 above the channel, granite kerb top 170 | yes |
| S7 | production/cloud-week/targets/wear/target.json and TARGET.md | 2026-10-09 | the wear writer | the project's own | 2026-10-09 | pillar_box_red 150/30/32; iron_wear tone row 124/104/92; the 0.214 m strip tiled round the girth; patch sizes; the foot-splash envelope; rust-bleed, poster and bird marks | yes |
| S8 | https://api.polyhaven.com/assets?type=hdris and https://api.polyhaven.com/files/&lt;id&gt; (tone-mapped JPG): adams_place_bridge, bethnal_green_entrance, birbeck_street_underpass, cambridge, canary_wharf, epping_forest_01, epping_forest_02, greenwich_park, greenwich_park_02, greenwich_park_03, leadenhall_market, limehouse, roof_garden, urban_street_01, urban_street_02, urban_street_03, urban_street_04 | 2026-10-09 | Andreas Mischok (all seventeen) | CC0 1.0 (Poly Haven) | 2019-02-09 to 2019-12-17 (each id's date is in the list: 2019-05-19 adams_place_bridge, canary_wharf, leadenhall_market, limehouse, roof_garden; 2019-08-18 bethnal_green_entrance, birbeck_street_underpass, urban_street_01, urban_street_02; 2019-08-31 epping_forest_01, _02; 2019-02-09 greenwich_park; 2019-09-07 greenwich_park_02, _03, urban_street_03; 2019-09-14 urban_street_04; 2019-12-17 cambridge) | every British panorama of the catalogue: streets, parks and a market in London and Cambridge | searched for a pillar box: NONE found; used for nothing else |
| S9 | https://polyhaven.com/a/rusty_painted_metal ; https://api.polyhaven.com/files/rusty_painted_metal (1k diffuse) | 2026-10-09 | Amal Kumar | CC0 1.0 (Poly Haven) | published 2025-03-18 (taken date not given) | a scan of a weathered red-painted steel surface (a container): faded red 119/64/47 with dark run streaks 44/28/23 over about 7 % of its area | looked at only for how rust runs over red paint; NOT a pillar box and used for no size or colour of the box (7.3) |
| S10 | Poly Haven's catalogues of 521 models and 867 textures; ambientCG's catalogue API (searches for postbox, mailbox, pillar box, cast iron, red paint) | 2026-10-09 | various | CC0 | n/a | no pillar box, post box or letter box in any | nothing |
| S11 | WebSearch result summaries (standard mode, 9 October 2026) | 2026-10-09 | search summaries of ukaa.com, lbsg.org, uknature.co.uk, oxfordhistory.org.uk, Historic Environment Scotland, a Jersey heritage report, hobbyist paint pages | n/a (leads only) | n/a | see 2.3 | LEADS: they corroborated a figure or named a thing to read; NO number was taken from them |

All Poly Haven material is used for the search and for looking only: not placed in the game, not traced into a texture, not fed to an image model.

### 2.2 The search of the panoramas

Poly Haven's catalogue lists 997 HDRIs; the ones with coordinates in Britain are the seventeen of S8 (the docklands pair and the other 2025 sets at 53.3 N 6.2 W are Dublin, where boxes are green and Irish: left out; st_fagans_interior is a Welsh interior; about 400 older panoramas have no coordinates and none is labelled British). Each was downloaded as its tone-mapped JPG (4096 to 20000 px wide) and searched twice (`scan_panoramas.py`, results in `panorama_scan.json`): (1) saturated-red blob detection (hue within 30 degrees of red, saturation above 0.68, value above 0.30, at least 80 px on a 4096 px panorama), then every large blob looked at as a rectilinear crop; (2) eight rectilinear views of 72 degrees round each street panorama, looked at by eye. A pillar box would be 90 px tall at 10 m on that scale. **Every red blob was a tail light, a brick wall, a painted shopfront, a refuse bin, a sign or graffiti; no panorama shows a pillar box.** The brief's expected case ("if no reachable photograph shows a pillar box") is therefore the case.

### 2.3 Leads (search summaries: never numbers)

| lead | via | what it did |
|---|---|---|
| a salvage dealer's Carron EIIR box, 73 in tall, about 20 in in the ground, body 15 in wide (also sold as PB42/2, Type B, circa 1966) | WebSearch summary of ukaa.com | corroborates the research's own 73 in and its narrow 15 in; tells the narrow Type B from the wide Type A |
| the Letter Box Study Group's 1937 Type B: 64 in high, 48 in round (15.3 in across) | WebSearch summary citing lbsg.org and a Scottish heritage listing | the same: the Type B is narrow, the Type A (19 1/4 in) wide |
| the Type K record: cast iron, 63 in high, 19 1/4 in wide, from 1980, five foundries | WebSearch summary of lbsg.org | the Type K variant has the same width as the Type A |
| OSM wiki: the larger Type A about 60 in round (19.1 in across) | WebSearch summary | corroborates 489 |
| BS 381C 538 (to about 1968) and 539 (after), renamed Cherry and Currant about 1988 | WebSearch summary of hobbyist pages | a colour name for the review; no sRGB taken |
| red with a black base stipulated in 1874; a listed box of 1936 "red with black base" | WebSearch summaries of a Jersey heritage report and a listed-building record | supports the black band; a reclamation firm shows about 6 in (152) of black: the 200 stays |
| an aperture widening in 1957 (6 1/4 to 8 in) | WebSearch summary of an Oxford history page | none: unclear which dimension; the scene's 320 x 45 kept |
| the Type K has a recessed aperture and no separate domed top | WebSearch summary of uknature.co.uk | the variant's description only |

### 2.4 Unreached

| what | result | used |
|---|---|---|
| Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, Sketchfab, lbsg.org (Letter Box Study Group), postboxmap.co.uk, the Postal Museum, Europeana, the National Archives, Historic England, British Pathe, the Library of Congress, Gutenberg, the British Library, Openverse | no connection or refused (status 000) from this cloud on 9 October 2026 | nothing |
| GitHub search | 403 (the API refuses searches outside the session's repositories) | nothing |
| ambientCG downloads | refused in earlier targets; the catalogue has no pillar box | nothing |

### 2.5 What to read once the network opens

1. Dated photographs, 1975 to 2000, of Type A and Type B boxes of the 1950s-60s on provincial British streets: front, side, three-quarter, with a person or the kerb (125 mm) in frame. Geograph, Wikimedia Commons categories of UK pillar boxes, Flickr's archive sets, local archives (Leodis, Picture Sheffield, Tyne and Wear, Hull History Centre). They settle the height (1372 or 1400 or 1470), the cap's moulding and rise, the order of cypher, lettering and plates, the hinge side and the door's size.
2. The Letter Box Study Group's type records for Type A, B and K (heights, widths, apertures by date, the 1957 aperture change).
3. Royal Mail's and the Postal Museum's archives: repaint and paint specifications of the 1980s (the black band's height, the red), drawings of the standard boxes.
4. Historic England and Cadw listings of Type A boxes (some give measured sizes).
5. A measured visit: a real Type A on a street near the PC, with a tape and a scale rod. The PC has the network the cloud lacks.
6. Dated photographs of a new Type K of the 1980s, to decide whether the variant needs writing.

## 3. The frame, the datum, the facing

* Origin: the box's vertical axis at the footway surface, z = 0 (Derived: the footway meets the foot's top-of-skirt there). +y is the FRONT (door and slot), +x is the viewer's right looking at the front, z up. The pivot of the .glb is that point; the buried skirt runs to z = -150 and is hidden. [Judgement, the brief's pivot rule]
* Footway level: the scene's footway falls toward the road at 1 in 40, flags +110 above the channel at the kerb's back (kerbs target), so at the axis (0.60 m back) the footway is 110 + 15 = 125 above the channel; across the 576 foot it differs by 14 mm; the box stands vertical and a fillet takes up the difference. [Read + Derived]
* Setback: the scene's code puts the AXIS 0.60 m behind the back of the kerb (z = FootwayFrontZ + setback). The foot's nearest point is then 312 mm from the kerb's back, and the clear footway past the box is 2000 - 600 - 288 = 1112. If "0.6 m back from the kerb" was meant to the nearest edge the axis moves to 0.89 m and 824 mm remain (see 9.1). [Read]
* Facing: the front (door, slot, plates) faces the carriageway, as the stand-in's aperture does (StreetVignette.cs PillarBox puts it at z - sgn x 0.48 x d). [Read; the alternative is in 9.1]
* The east lamp column of the scene stands at x = 28.0 on the same line, 1.0 m from the box (Derived from lighting.column: first at 8.0, one every 10 m on alternate sides). The foot clears its base by 612 mm. The lantern (5 m up, 0.5 m out) lights the cap from above, and at night the box is the nearest object in the street to a sodium lamp (6.4).

## 4. The target, part by part

Kinds: **Read** (printed in the repository), **Derived** (computed from others), **Judgement** (the writer's choice). There are no **Scaled** and no **Photo** numbers: none was measured on a drawing or a photograph. Where a Judgement rests on the writer's general knowledge of the type and on no source read in this session, it is marked *Memory*: the lowest weight, a guess for the first dated photograph to correct. `target.json` `numbers` carries every number's kind and source (91 of them: 45 Read, 7 Derived, 39 Judgement).

### 4.1 The type: one main model, one variant not built

**Main: Type A, cast iron, 1950s-60s, domed cap with a moulded rim, hooded aperture, hinged door.** Why:
1. The street is a Victorian port quarter in 1990: the stock is the older cast-iron standard boxes; the capless Type K was introduced on 31 July 1980 and is the newer replacement (the research, Read; it recommends "an EIIR Type A of the 1950s-60s").
2. The stand-in already has a cap and a dome, so the silhouette the street was blocked with is the Type A's.
3. The Type A gives the camera four things to read at 1.6 m (the cap, the hooded slot, the door with its plates, the foot); the capless box has fewer.
4. The postal cypher and the operator's lettering, which canon owes, have clear places to stay blank on a Type A (a pad, a roundel); on a capless box they are cast into the aperture plate.

**Variant: Type K, capless (`type_k_capless`), NOT built.** The evidence supports only that one stood in some 1990 streets (the research, Read) and that it has the same 19 1/4 in width (two search leads). A coarse profile is in `target.json` `decision_type.variant` (the same body and foot, a flush rounded crown, no cap, the aperture recessed) and flagged "lead only, unmeasured". The street needs one box; do not build it unless asked.

### 4.2 The lathe profile (body, foot, cap and dome)

Outer surface, (radius, z) in mm from the buried skirt up the axis; `target.json` `profile.outer_rz` has the 69 points. Revolve about the axis.

| segment | z from to | radius | kind |
|---|---|---|---|
| buried skirt (hidden) | -150 to 0 | 288 | Judgement (the real casting is 482 deep: Derived, 73 in less 1372 mm; only 150 modelled) |
| foot band | 0 to 48 | 288 | Judgement, *Memory* |
| foot top round | 48 to 60 | quarter round R 12 from 288 to 276 | Judgement |
| splay | 60 to 72 | 276 to 262 | Judgement |
| cove | 72 to 140 | an ellipse quadrant from 262 (horizontal) to 244.5 (vertical) | Judgement |
| body | 140 to 1215 | 244.5 (a plain cylinder, no taper) | Derived (19 1/4 in = 489 across) |
| cap under-moulding (cove) | 1215 to 1228 | 244.5 out to 268 (horizontal at the lip) | Judgement, *Memory* |
| cap rim | 1228 to 1250 | 268 (vertical, a sharp lower drip edge) | Judgement |
| cap bead | 1250 to 1262 | quarter round R 12 from 268 to 256 | Judgement |
| shoulder and neck | 1262 to 1292 | 256 in to 250, then vertical | Judgement |
| dome | 1292 to 1372 | a spherical cap, chord radius 250, rise 80, sphere radius 430.6, apex on the axis at 1372 | Judgement (rise / diameter 0.16), *Memory* |

Bevels (`target.json` `bevels`): cap rim lips 1.5, foot band bottom 2.0, door perimeter 2.0, hood lip 2.0, plate bezels 1.5, panel pads 1.0, slot lips 1.0. Surface: sand-cast, a 0.3 mm bump at about 4 mm wavelength (a normal map; Judgement), a 0.5 mm raised casting seam down the back (x = 0, y < 0), and a thick paint bead (0.3 to 0.6 mm) along every edge. No finial or boss on the dome: the research names none.

### 4.3 The foot and how it stands in the footway

* The foot (the plinth) is the 576 mm band with its splay and cove above. The scene's 597 is read as this widest part at the pavement (3.5 % over).
* The casting goes 482 mm into the ground (Derived); the model carries 150 of it as a hidden skirt, so the paving can dip or the pavement be cut round it without a gap.
* The flags (the footway family's) are cut to a rough round 20 to 60 mm from the foot, with a gap of 5 to 12 mm that a **fillet** covers: dark bitumen and mortar, 56/53/50, roughness 0.9, 15 to 35 mm wide and about 10 mm high at the foot, feathered to nothing on the paving, wider on the uphill (building) side. [Judgement]
* Black base band: the foot and the lowest 200 mm of the box are black, 35/35/36 (the wear target's iron_black), roughness 0.5; the line to the red is a brush line that wavers +-3 mm, the red overlapping the black by 1 to 2 mm in places. The 200 is the research's "about 20 cm tall" [Read]; a reclamation firm's "about 6 in showing" (152) is a lead that did not move it. The band crosses the cove (z 140 to 200).

### 4.4 The aperture, its hood, sill and flap

| part | numbers | kind |
|---|---|---|
| slot | 320 wide x 45 high, z 1127.5 to 1172.5, centred on the front axis, corner radius 5, cut through the 12 mm wall into a black interior (8/8/8, roughness 0.9); half angle on the cylinder 40.9 degrees | Read (the scene), corner Judgement |
| hood | a curved lip wrapped round the front: underside flat on the slot's top (z 1172.5), front face at radius 274.5 (30 proud) to z 1195, top sloping back to the body at z 1205 (10 under the cap's under-moulding), half angle 48 degrees (a little wider than the slot), cheeks on radial planes | Judgement, *Memory* |
| sill | a lip below the slot: a chamfer from the body at z 1112 to 11.5 proud at z 1123.5, flat to z 1127.5 (the slot's bottom), half angle 44 degrees | Judgement |
| flap | a 300 x 30 x 2 plate hinged along the inside top of the slot, hanging tilted 15 degrees, dark iron 40/40/42, seen through the opening | Judgement, *Memory* |

### 4.5 The door, its hinges and lock

| part | numbers | kind |
|---|---|---|
| door | x -150 to 150 (300 wide, half angle 37.1 degrees), z 280 to 1040 (760 high), proud 4 (outer radius 248.5), corner radius 10; a joint groove 3 wide x 3 deep round it; plain, sand-cast, painted red | Judgement, *Memory* |
| hinges | two barrel hinges on the LEFT edge as seen from the front: axes at x -150 (straddling the door's edge), z 420 and 900; knuckle diameter 26, length 96; pin head 18 across and 6 high on top of each; painted red, the pin heads bare dark iron 60/52/46 | Judgement, *Memory* |
| lock | on the RIGHT: an escutcheon disc 36 across, 3 proud, centred x 112, z 690; a keyhole slot 4 x 12; a brass swivel shutter 22 x 10 x 2 (150/125/70, roughness 0.4, metal 1) over it; no maker's mark | Judgement, *Memory* |

### 4.6 The blank pads and the two plate frames

| part | numbers | kind |
|---|---|---|
| lettering pad (BLANK) | x -150 to 150, z 1062 to 1102 (300 x 40), 3 proud, corner radius 4, on the body between the door's top (1040) and the sill (1112); plain: relief spread within it 0.5 mm at most | Judgement, *Memory* (the position) |
| cypher roundel (BLANK) | a disc 110 across centred at (0, 960) on the door, 3 proud; plain: relief spread 0.5 mm at most | Judgement, *Memory* |
| collection-plate frame | a flat-faced boss 210 x 125 centred at (0, 790): its face plane is tangent to the door at the axis plus 6, its sides run back to the cylinder (so the boss stands 29 mm proud at its edges); a 12 bezel; the plate window 186 x 101 recessed 3 below the bezel face | Judgement, *Memory* |
| enamel-plate frame | a flat-faced boss 160 x 100 centred at (0, 590), a 10 bezel, the window 140 x 80, recessed 3 | Judgement, *Memory* |

The real order of cypher, lettering and plates on the front of an EIIR Type A is the first thing to read from a dated photograph: each may be 40 mm or more out. The pads and frames are placed so that nothing overlaps (self-check D): the door's top (1040), the lettering pad (1062), the sill (1112), the slot (1127.5); the roundel (905 to 1015), the collection frame (727.5 to 852.5), the lock (672 to 708), the enamel frame (540 to 640) are stacked down the door with 19 mm or more between them.

### 4.7 The words on the box, and why they are safe

Canon: the postal cypher (the pillar box's) and the telephone operator's mark are owed by the brand bible; "ER", a crown, "POST OFFICE", "ROYAL MAIL" and a real maker's casting mark are not allowed (brief). So:

* **Cypher roundel, lettering pad, hood, sill, door, foot, cap: no letters, numerals, crown or relief device at all.** No maker's name or date.
* **The enamel instruction plate: blank**, a plain ivory plate in its frame (232/229/218, roughness 0.12), no border and no words.
* **The collection-times plate: exactly five strings, nothing else**, black (22/22/24) on white vitreous enamel (232/229/218) with a 2 mm black border line inset 4 mm:
  * `COLLECTIONS` (bold, cap height 11, centred, 14 from the top), under it a 1.5 mm black rule inset 14,
  * `MON-FRI` (left, cap height 8, baseline 52 from the top) and `5.30 PM` (right),
  * `SAT` (left, cap height 8, baseline 76) and `12 NOON` (right).
  Any plain grotesque from production/fonts will do at 8 mm (OFL); a period face is not needed.
* **Why they are safe:** they are the plain English words and times a collection plate needs, as a notice on any street names no company; none names an operator, brand, council, maker or reign, none is a cypher or a crown; "POST OFFICE", "ROYAL MAIL", "LETTERS" on the slot, "GPO", "ER", "GR" and any foundry name are NOT used; the days are standard abbreviations; the times are an invented, plausible 1990 pattern (a weekday last collection, a Saturday noon, nothing on Sunday). If the brand bible or Jafar wants no lettering at all, delete the text list: the plate stays a blank white frame (variant `plates_blank`; the self-check and the checks accept both).

### 4.8 Triangle budget and the build

Mid-poly with a bevel on every edge (the asset plan's method, Read): about 8,000 to 30,000 triangles at LOD0 (Judgement). One mesh for the box, the plates as their own material slots, one UV set (the girth in the U direction for the wear strip, section 7).

## 5. Photographs win: what was overturned

No photograph was reached, so no photograph overrides anything. The repository's own figures disagree with each other in places; each choice is below and in `target.json` `photographs_win`.

| item | a | b | chosen |
|---|---|---|---|
| body width | the scene 597 (a trade guess) | the research 49 cm / 19 1/4 in (untraced) and 19 in (a c.1955 listing) | 489 for the body; the 597 is read as the foot (576) |
| height | the scene 1372 + 100 + 140 = 1612 | the research's "working" 150 cm, and its own range 135 to 147 | 1372 in all |
| cap width | the scene 660 (1.35 x the body) | none; the research says "a few centimetres proud" | 536 |
| dome rise | the scene 140 | none | 80 |
| aperture | the scene 320 x 45 at 1150 | a lead: widened in 1957 (6 1/4 to 8 in), unclear which dimension | the scene's kept |
| red | the wear target 150/30/32 | a lead: BS 381C 538 or 539 | 150/30/32 kept: the lead is a shade name, not an sRGB |
| black band | the research about 200 | a lead: about 152 showing | 200 |
| share of paint lost | the wear target 4 to 8 % (a downpipe) | this target 3 to 6 % | 3 to 6 %, typical 4 % (the wear writer to confirm) |

## 6. Materials and colours

### 6.1 The table

| surface | sRGB | name | roughness (words, 0 to 1) | metal | kind |
|---|---|---|---|---|---|
| red paint | 150/30/32 | pillar-box red, a deep gloss red | semi-gloss 0.35 on the body (a gloss enamel five to eight years after its last repaint); 0.45 on the top of the dome and cap rim (chalked) | 0 | colour Read (the wear target), roughness Judgement |
| black base paint | 35/35/36 | black | 0.5, satin | 0 | Read (wear target iron_black) |
| plate enamel | 232/229/218 | white vitreous enamel | 0.12, glossy | 0 | Judgement |
| plate text and border | 22/22/24 | black | 0.3 | 0 | Judgement |
| brass shutter | 150/125/70 | dull brass | 0.4 | 1 | Judgement |
| hinge pin heads | 60/52/46 | bare dark iron | 0.6 | 0.6 | Judgement |
| flap | 40/40/42 | dark iron | 0.6 | 1 | Judgement |
| slot interior | 8/8/8 | black | 0.9 | 0 | Judgement |
| bare iron and rust in a chip | 141/102/72 (rust), 118/112/106 (grey primer), 112/56/34 (rust halo on red) | see 7.1 | 0.65 | 0.3 on a rusty chip, 1 on the bright sill band | wear target (Read) / Judgement |
| footway fillet | 56/53/50 | bitumen and mortar | 0.9 | 0 | Judgement |

### 6.2 The red

150/30/32 is the wear target's pillar_box_red, kept ("the furniture family's own colour wins" said that target, and this family agrees). Linear (0.305, 0.013, 0.0144), relative luminance 0.075, L* 33, HSV saturation 0.80, value 0.59. Why this and not a lighter, more orange red: (a) art-direction R-B4 makes the red boxes the street's whole high-chroma accent, and the accent budget counts the frame's pixels above saturation 0.6; at 0.80 the red keeps well over that after dirt and a wet sky; (b) the box paint of a port town in 1990 is a deep crimson-leaning red (the lead names BS 381C 538 or 539, "Cherry" and "Currant"), not the bright modern brand red. It is a Read colour with a Judgement behind it; it has not been checked against a paint chip or a photograph.

### 6.3 The accent budget

The box's projected area is about 0.71 m2 (0.489 x 1.372 and the cap's overhang). On a 2560 x 1440 frame at 46 degrees vertical it covers about 2.2 % of the frame at 5 m, 0.9 % at 8 m and 0.4 % at 12 m (Derived), far under the 0.078 ceiling on its own. A wet sky lowers the saturation of the cap's top and the brightest patches to about 0.6 to 0.7; the vertical faces stay at 0.75 to 0.8.

### 6.4 How it reads wet

Wet paint stays glossy: roughness drops by 0.18 (0.35 to 0.17 on the body, 0.45 to 0.27 on the dome), and the diffuse darkens by about 12 % in linear light: 141/28/30. The sky mirrors in the cap's top and in the upper body's vertical faces as a pale, soft band; the foot (the splash zone, 7.4) goes much darker and glossier; the black band takes the street's wet reflections; the plate stays bright and its enamel mirrors the sky; rust runs show darker and redder.

### 6.5 How it reads by night under the 589 nm lantern

The scene's lantern is monochromatic 589 nm, colour rendering index 0 (linear sRGB 1.0, 0.7055, 0.0). A surface can only return that wavelength, at a fraction of it equal to its reflectance at 589 nm, so every object takes the lamp's yellow-orange and differs only in how bright it is. A deep red paint's reflectance rises steeply between 590 and 640 nm, so at 589 it is low. Fitting a logistic reflectance edge to the red's daylight colour (three edge widths; the shape is assumed, so this is Judgement with a wide error; `make_target.py`) gives:

| | reflectance at 589 nm | brightness against a white surface (0.85) | lit colour at the lamp's full level (sRGB) |
|---|---|---|---|
| fitted edge (width 8 / 12 / 18 nm) | 0.081 / 0.080 / 0.076 | 0.089 to 0.095 | 80/67/0 (width 12) |
| the same pigment with the edge 12 nm bluer (upper estimate) | 0.123 to 0.196 | up to 0.23 | 110/93/0 (width 12) |
| a white surface (0.85) | 0.85 | 1 | 237/203/0 |
| what an RGB engine gives (albedo x lamp triple) | n/a | 0.117 | 150/24/0, still RED |

So by night the box is **a dark olive-brown, about a tenth to a quarter as bright as a white wall, and not red**; the white plate and the lit, wet edges of the cap and hood are the brightest things on it, and the black slot reads as a hole. An RGB engine keeps the red channel and will draw the box a dark red under the same lamp, which is wrong in hue but about right in brightness. The consequence for the street: at night the box does NOT carry the red accent; the lantern's own colour and the lit windows do. The lighting and grading people should know that the box is the one red object they cannot lean on at night, and it stands 1.0 m from a lamp column.

## 7. Wear and damage

No photograph shows a pillar box's wear, so every number here is Judgement unless it says it is the wear target's. State: **tired**, five to eight years after its last repaint, one tidy-up of the plate and lock, the chips not touched up; a port town's old quarter in a wet climate (RULINGS: "grime is the strategy").

### 7.1 Chips and the layers of paint

A chip shows the repaints: the top red (150/30/32), then an older red (112/26/30, in half the chips), then at the bottom grey primer (118/112/106; 45 %), bare rusty iron (141/102/72; 40 %) or old black (35/35/36; 15 %, only on the base band and the door). Hard-edged, with a thick paint bead round each (0.3 to 0.6 mm) and a rust halo (112/56/34) where iron shows. The wear target's mark for the pillar box (a replacing 124/104/92, the mean of primer and rust) is the average of these. The mask is the wear target's `iron_wear` as a strip tiled round the girth, mirrored on alternate repeats; the girth is 1536 mm and the 214 strip fits 7.2 times, which is not even (a mirrored strip needs an even count to close at the seam), so **use 8 repeats of 192 mm** (the strip 10 % narrower) with the seam at the back (x = 0, y < 0); the mask runs from z = 0 up the 1372 mm (the wear target's is 2.4 m; the lowest 0.3 m keeps its 40 % of the lost paint). Patches 20 / 45 / 110 mm (p10 / p50 / p90), edge 4 mm (the wear target's). **Share of the area lost: 0.03 to 0.06, typical 0.04** of the body and foot (door furniture and slot excluded), against the wear target's 0.04 to 0.08 which is the downpipe's: the box is touched up in service. The wear writer should accept or overrule.

### 7.2 At the base

* 14 to 22 chips in the lowest 400 mm, 3 / 9 / 25 mm equivalent diameter (p10 / p50 / p90), 70 % of them under 300 mm.
* The foot's top round (z 48 to 60) is worn to bare iron over 30 % of the circumference, a band 10 to 14 mm wide, 96/84/76, strongest on the road side (wheels, bags).
* A scrape on the road side at z 380 to 520, 180 long and 20 to 40 high, 15 % bare.

### 7.3 At the aperture

* The hood's lower front edge: 40 % of its length chipped, chips 2 to 10 mm, each with a rust halo.
* The sill lip: a bare band 10 mm wide over 60 % of its length, dull dark iron 80/76/72 (letters scrape it; it is not shiny).
* The slot is black inside, with a faint pale line where the flap's lip catches light.
* 30 to 60 micro-chips of 2 to 8 mm along the door's perimeter, the hood and sill edges, the cap rim's lips and the foot's top edge.

### 7.4 Grime

* Ground up, the wear target's foot-splash envelope: full strength to z 240, 0.85 at 330, 0.5 at 450, 0.15 at 610, gone by 750; on the red the multiplier is 1 - 0.38 x strength (0.62 at the foot) in linear light, the black band 1 - 0.2 x strength.
* Soot under the cap, z 1190 to 1215: x 0.7.
* 5 to 9 rain streaks from the cap rim, 10 to 30 wide, 100 to 350 long, x 1.12 (a cleaner streak down a dirtier ground; the overhang protects what is under it).
* 1 to 3 bird droppings on the dome and rim, 30 to 120 mm, 226/224/214 (the wear target's), with up to one run 10 to 30 wide and 50 to 300 long; the box stands at x 27, so the quay-end weight is 0.4.
* Chalking: the top of the dome and the rim's upper face x 1.08 lighter and a little pink, roughness 0.45.
* 1 to 2 shallow dents, 30 to 60 mm across and 1 to 2 mm deep, at z 300 to 700.

### 7.5 Rust bleed

Sources: every chip below 400 mm, the two hinge knuckles, the cap's under-moulding joint (z 1215), the hood's underside, the foot's top edge. Each source: 1 to 2 trickles, 5 / 10 / 20 mm wide, 80 / 200 / 350 long, running straight down, colour on the red 84/40/26, a dark dot of 3 to 10 mm at the source and a 15 to 40 mm brown halo, edge 8 to 25 mm, 0 to 2 detached drops of 20 to 60 mm. The widths follow the wear target's rust_bleed (measured on a brick wall, not on iron). Looked at, not used for numbers: Poly Haven's rusty_painted_metal (a container) shows the run streaks reading about a third of the red's luminance (44/28/23 on 119/64/47) over about 7 % of its area: rust over red paint runs dark brown-black, not orange.

### 7.6 Flyposting traces

* 1 to 2 patches 150 to 260 wide and 120 to 300 high, centres at z 600 to 900, on the sides and back, 70 to 140 degrees round from the front, never on the door, the plates, the lock, the aperture or the hood; 20 to 60 % of the paper left, torn on the diagonal (2 to 10 mm hard edge), the paper colour 196/186/168 (the wear target's), a paste ghost 10 to 30 mm wide round it; unreadable remnants: nothing that shows a word, a face, a drink or a wager.
* 0 to 3 stickers of 40 to 100 mm at z 300 to 1100, the same exclusions.
* The scene's G5 sticker decal (0.15 x 0.15 m on the street face at 0.15 m up) sits where the door is: move it 70 degrees off the front.

### 7.7 First look at 1.6 m

Red cylinder; a dark, grimy foot and black band; three or four orange-brown chip clusters low down; one dark rust trickle under the left hinge; a torn paper remnant on the side; the bright white plate; the black slot under its hood.

## 8. Variants the street needs

One box: `main`. The listed variants (`target.json` `variants`): `main` (built); `no_black_band` (all red to the ground; not built); `type_k_capless` (not built); `plates_blank` (built if canon wants no lettering). Per-instance variation: the wear seeds (the girth strip's seed and mirroring) only.

## 9. What the target could not settle, and the handover

### 9.1 Could not settle

1. Whether a Type A of the 1950s-60s stands 1372, 1400 or 1470 above the footway: a photograph beside the kerb (125) or a person settles it in a minute.
2. The real order and positions on the front of the cypher, the lettering, the collection plate, the enamel plate and the lock; the pads, roundel and frames are placed from the writer's general knowledge (Memory) and each may be 40 mm or more out.
3. The cap's moulding, the dome's rise (80 against the scene's 140), whether a finial or boss exists, the hood's depth.
4. Whether the front faces the carriageway (kept, as the scene) or runs along the footway, and which side the door hinges on.
5. Whether "0.6 m back from the kerb" is to the axis (the scene's code; kept) or to the nearest edge: it moves the box 0.29 m and the clear footway from 1112 to 824 mm.
6. The exact 1990 red (BS 381C 538 or 539, a lead): 150/30/32 is the wear target's guess, checked against the accent budget and not against a chip.
7. The base band's height (200 Read; 152 as a lead) and whether a 1990 repaint kept it.
8. The Type K as a second variant: only worth writing once a dated photograph shows one in a street like this.
9. A "next collection" number tablet or rotary dial: not modelled (the research: uncertain).
10. The reflectance of the red at 589 nm (6.5): a fitted edge gives 0.08, a bluer edge 0.12 to 0.20; a spectrum of the real paint would settle it.

### 9.2 Handover (one line each, for NOW.md and the neighbours)

* **Scene file, furniture E4:** replace body 0.597 / 1.372, cap 0.660 x 0.100 and dome 0.140 with the kit piece (total height 1.372, foot 0.576, body 0.489, cap 0.536); its pivot is the axis at the footway; the stand-in was 0.24 m too tall if 1.372 was meant as the whole.
* **Kerbs and footway:** the footway stands at +125 above the channel at the axis (110 at the kerb's back plus 15 of fall); the flags are cut round the foot with a fillet (4.3).
* **Wear:** pillar_box_red keeps 150/30/32; the iron_wear strip is 8 repeats of 192 mm round the 1536 mm girth, not 7.2 of 214; the share 0.03 to 0.06 (typical 0.04); the foot-splash envelope applies from the footway.
* **Lighting:** the east lamp column at x = 28.0 is 1.0 m from the box on the same line; by night under the 589 nm lantern the box reads dark olive-brown (a tenth to a quarter of white), not red (6.5).
* **NOW.md line:** Pillar box target (cloud week 42): NO photograph of a pillar box was reached; Type A, 1372 above the footway, body 489, foot 576, cap 536, red 150/30/32 over a 200 black band, blank cypher and lettering pads, collection plate words COLLECTIONS / MON-FRI 5.30 PM / SAT 12 NOON only; the first dated photograph overrides every size.

### 9.3 The checks (for unit 3.6's automatic check)

`target.json` `checks`: 46 checks, each with a name, what to measure, the expected value, a tolerance and its kind: the total height 1372 +-15, body 489 +-5, foot 576 +-6, cap rim 536 +-6, slot 320 x 45 at 1150, the hood's 30 proud, the door 300 x 760 from z 280, two hinges at x -150, z 420 and 900, the lock at (112, 690), the blank pad and roundel (relief spread 0.5 mm, no letters), the two frames, the black band at 200 +-10, the red albedo 150/30/32 +-6, roughness 0.35 +-0.08, no letters except the five allowed strings, no cypher, crown, operator or maker glyphs, nothing floating, the clearance from the kerb's back (312 +-20) and from the lamp column (612 +-40), the front toward the road, the wear share, the 8 UV repeats, the triangle range, bevels of at least 1 mm.

### 9.4 Files

* `TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`
* `pb_numbers.py` (every number with its kind and source), `make_target.py` (builds target.json, including the colour block), `make_previews.py`, `scan_panoramas.py` with `panorama_scan.json` (the search of the panoramas)
* previews in production/previews/cloud-week/refs/pillar-box/, named `<ref>-<place>-<what>.jpg`: `target-quay-street-elevations.jpg`, `target-quay-street-plans.jpg`, `target-quay-street-axial-section.jpg`, `target-quay-street-red-dry-wet-sodium.jpg`. They are the DRAWING made from target.json and colour swatches computed in code (own work, no licence): there is no photograph to preview and no target-on-photo overlay. The panoramas of S8 are Andreas Mischok's, CC0, used for the search and not reproduced.
