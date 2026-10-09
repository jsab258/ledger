# Quay Street's pillar box: the target (cloud week 42, 9 October 2026, second try)

**Quay Street's pillar box is a cast-iron cylinder of the 1950s-60s standard "Type A" pattern, painted pillar-box red (sRGB 150/30/32) above a black base band 200 mm high: body 489 mm across, a 576 mm foot, a 560 mm cap with a shallow 80 mm dome, 1500 mm above the footway in all (the earlier research's working figure; the stand-in's 1612 is 0.11 m too tall), a 320 x 45 mm letter slot centred at 1278 mm under a 30 mm hood, a 300 x 888 mm door that is flush (1 mm proud, a joint groove round it, hinged on the left with no hinge showing; a keyhole escutcheon and one collection-plate frame) and, where the cypher and the operator's lettering belong, FLUSH reserved areas with no raised or cut geometry (canon owes them): no cypher, crown, operator lettering or maker's mark, the collection plate saying only COLLECTIONS, MON-FRI 5.30 PM, SAT 12 NOON, and the front facing the building line; no photograph of a pillar box was reached, so no number below is measured on a photograph: every size is the repository's earlier figures (Read), derived from them, or the writer's judgement, and the first dated photograph overrides them.**

Written 9 October 2026 for the family "pillar box on Quay Street" (scene line furniture E4, east side, x 27.0). **This is the second try**, after TARGET-REVIEW.md (FAIL on one fault, the height, and nine narrow points, all applied; section 0 below). Units are millimetres unless a line says otherwise; the .glb is metres, z up, scale 1, the pivot the box's axis at the footway surface. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, a section, plans); `self_check.py` tests them. Last result: SELF-CHECK PASS: 212 of 212 tests pass (A printed numbers 61/61, B photograph measurements 13/13 [none exist: it tests that none is claimed], C drawing 21/21 [no photograph: nothing laid on one], D internal consistency 66/66, E text and canon 51/51) (`/home/user/.bpyenv/bin/python -I self_check.py`; it runs the drawing, regenerates the profile from pb_numbers.py, proves that the silhouette check fails a plain-disc cap and a foot without its moulding, and was tried on deliberately broken copies of target.json: eleven in the first try, one of which it passed until a regeneration test was added, and eleven more after the amendments, all refused)

## 0. What the review changed

| point | what was wrong | what this target now says |
|---|---|---|
| F1, the height | the first draft read the stand-in's BODY height 1372 as the whole box and defended it with the 73 in listing's 1350 to 1470; the research's own Type A figures are higher | total 1500, kind Read (the research's working figure, "the top is at about 150 cm"); 1626 (5 ft 4 in, the research's untraced Type A line) is the upper alternative; 1350 to 1470 is a casting's length that a lead sells as a Type B's, not used; everything from the sill up moves +128 (slot centre 1278, cap soffit 1343, door 280 to 1168). I could not show the reviewer wrong: the research says "about 150 cm above ground" twice and gives 5 ft 4 in for the Type A; the only support for less is the 73 in casting |
| N1 | a plain disc for the cap, or a foot with no moulding, passed every check; two checks were worded so a correct build could fail | new check `profile_silhouette` (back half, every 2 mm of z, against the profile, 0 within 1.5); `cap_soffit_height` measured on the back half; the reserved-area checks measure relief radially above the curved face; the self-check proves the new check fails a plain-disc cap and a foot without its moulding and passes a correct one |
| N2 | the door stood 4 proud but the research says "a flush panel" | door 1 proud (outer radius 245.5); the 3 x 3 groove shows it; the plate frame's face stays at y = 254.5 (9 above the door at the axis); a row in section 5 |
| N3 | external barrel hinges were an invention | removed: the hinges are internal; "hinged on the left" is the side of the joint only; one check says nothing on the door's left edge stands more than 1.5 proud; the rust-bleed trickle that was under the left hinge is under the hood's left end |
| N4 | the hood (30 proud) stuck out past the cap rim (23.5 proud) | cap 560 across (rim 35.5 proud); the hood tucks 5.5 inside it |
| N5 | blank raised disc, blank pad and blank enamel plate read as placeholders | flush reserved areas (no geometry) for the cypher and the lettering; the enamel plate and its frame are deleted; the box carries one plate; variant `no_plate` is no plate and no frame |
| N6 | a road-facing slot leaves the poster on the kerb edge | the front faces the building line (the shops); the scene owner is told, the scene's road side recorded as a Read figure the target goes against |
| N7 | two placements were left to the drawing script | written in target.json: the door and both reserved areas "concentric", with their radii |
| N8 | a bright brass keyhole cover | the shutter is painted red 150/30/32, metal 0, with dark bare metal 60/52/46 on its 1 mm edge only |
| N9 | two slips in 2.2 | "265 without coordinates" (997 listed, 732 with) and "8192 px wide" (every JPG), both recorded as numbers and tested |

## 1. What the street's stand-in gets right, and what this target changes

Today's stand-in (SCENE-SLOTS.md and vignette-scene.json, read 9 October): a body cylinder 0.597 across and 1.372 high with a cap cylinder 0.66 across and 0.10 high and a dome 0.14 on top of it, so 1.612 m in all; a box slot 0.32 x 0.045 at 1.15 m; no cypher, no lettering. It is "a trade-standard guess, not a photograph".

| | the stand-in | this target | why |
|---|---|---|---|
| height above the footway | 1612 (body 1372 + cap 100 + dome 140) | 1500 in all | the research (Read): "about 150 cm above ground", "the top is at about 150 cm"; 1626 is its untraced Type A line (the upper alternative) |
| body | 597 across | 489 across (19 1/4 in) | the research: 49 cm and 19 in; the 597 is read as the FOOT's size (576 chosen) |
| foot | none | 576 across, 48 mm band, splay, cove to the body at 140 | every standard box stands on a wider moulded foot |
| cap | 660 across, 100 high | 560 across: cove, rim, bead, neck (z 1343 to 1420) | the research: the rim is "a few centimetres proud of the body"; it is the outermost line above the foot |
| dome | 140 | 80 (rise / diameter 0.14 on the 560 cap) | a shallow bowl, not a hemisphere; Judgement, no photograph |
| aperture | 320 x 45 at 1150 | 320 x 45 kept; centre 1278 (+128); hood 30 proud over it, sill lip below, flap behind | the research: "a horizontal slot with a small hood just under the cap" |
| door, lock, plate | none | a flush door 300 x 888, an escutcheon, one collection-plate frame | brief: the front door of 8 October failed on furniture its target never wrote down |
| cypher, lettering | none (a rule: "no cypher, no lettering") | two flush reserved areas, no geometry | canon owes the postal cypher; a blank raised disc reads as a placeholder |
| facing | the slot on the road side | the building line | review N6 (section 3) |
| colour | one "metal" | red 150/30/32, black band 35/35/36 to 200, white plate enamel, a red-painted keyhole shutter | wear target and research |

What the stand-in gets right: the place (east side, x 27.0, 0.6 m behind the kerb), the slot's size, and "NO CYPHER, NO LETTERING" as the rule for the postal marks.

## 2. Sources

**No photograph of a pillar box was reached today, for the writer or for the reviewer.** The cloud's network refuses Wikimedia, Geograph, Flickr, archive.org, Sketchfab and the rest (listed under Unreached); the one open host with photographs is Poly Haven (CC0), and none of its British panoramas, models or textures shows a pillar box (the search is in 2.2). So nothing below is Photo-measured and nothing is laid on a photograph (there is no main photograph, so the brief's "drawing laid on the main photograph" does not exist; `self_check.py` says "NOT RUN" for it and claims nothing). The earlier research (production/research/street-clutter-1990/SUMMARY-2026-09-29.md, section 1) also warned that "most links show surviving examples photographed after 2000" and that "photographs taken 1985 to 1995 in northern England were not found"; this target goes one step further down: there is no photograph at all, of any date. Where this file says "the reviewer", it means TARGET-REVIEW.md; its points marked judgement rest on the reviewer's own knowledge and are not evidence either.

### 2.1 What was read, and what for

| id | where | date read | author | licence | date taken | what it shows or gives | used |
|---|---|---|---|---|---|---|---|
| S1 | production/specs/vignette-scene.json, furniture E4_pillar_box and street, lighting, as read by StreetVignette.cs (PillarBox, Furniture, Columns) | 2026-10-09 | the project | the project's own | 2026-09-02 to 2026-10-08 | the stand-in's sizes, place, setback (the box's axis 0.60 m behind the kerb's back), the slot on the road side, the east lamp column at x 28.0, the lantern colour | yes: Read numbers |
| S2 | production/cloud-week/targets/SCENE-SLOTS.md, BRIEF.md | 2026-10-09 | the project | the project's own | 2026-10-08 | the pillar box row; the brief's rules | yes |
| S3 | production/research/street-clutter-1990/SUMMARY-2026-09-29.md section 1 (the project's earlier reading, done on the PC) | 2026-10-09 | a helper, saved by the builder | the project's own | 2026-09-29 | the type (EIIR Type A of the 1950s-60s; Type K from 31 July 1980), the working figures (about 150 cm above ground, 49 cm across; "the top is at about 150 cm"), the untraced Type A line (5 ft 4 in tall, 1 ft 7 1/4 in wide), the listing sizes (73 in, 15 to 20 in buried, 19 in, 15 in), "Red body, black base", base about 20 cm, "a flush panel with the cast cipher, a plate frame and a keyhole". Its photographs (Geograph 4378457 Tenby, 10 May 2008; Geograph 24094 Kirkby in Cleveland, 5 July 2005, Mick Garratt, CC BY-SA) are links only, and Geograph is unreached from this cloud, so they were NOT seen | yes: Read numbers, cited as the project's earlier reading, with its caution |
| S4 | production/research/asset-plan/3-FURNITURE-PROPS-FOOD.md | 2026-10-09 | the project | the project's own | 2026-10-03 | "Bodies: lathe and box primitives with caps, rims, slots, hinges, lettering panels"; mid-poly, a bevel on every edge; "canon owes ... the pillar box's cypher" | yes |
| S5 | game-design/research/art-direction.md R-B4; production/specs/vignette-bill-of-materials.md | 2026-10-09 | the project | the project's own | 2026-09 | the accent budget: red boxes are the street's whole high-chroma accent; the frame's saturation > 0.6 share non-zero and under 0.078 | yes (6.3) |
| S6 | production/cloud-week/targets/kerbs-and-covers/target.json and TARGET.md | 2026-10-09 | the kerbs writer | the project's own | 2026-10-09 | footway flags +110, kerb top +115 above the channel, granite kerb top 170 | yes |
| S7 | production/cloud-week/targets/wear/target.json and TARGET.md | 2026-10-09 | the wear writer | the project's own | 2026-10-09 | pillar_box_red 150/30/32; iron_wear tone row 124/104/92; the 0.214 m strip tiled round the girth; patch sizes; the foot-splash envelope; rust-bleed, poster and bird marks | yes |
| S8 | https://api.polyhaven.com/assets?type=hdris and https://api.polyhaven.com/files/&lt;id&gt; (tone-mapped JPG, every one 8192 px wide): adams_place_bridge, bethnal_green_entrance, birbeck_street_underpass, cambridge, canary_wharf, epping_forest_01, epping_forest_02, greenwich_park, greenwich_park_02, greenwich_park_03, leadenhall_market, limehouse, roof_garden, urban_street_01, urban_street_02, urban_street_03, urban_street_04 | 2026-10-09 | Andreas Mischok (all seventeen) | CC0 1.0 (Poly Haven) | 2019-02-09 to 2019-12-17 (2019-05-19 adams_place_bridge, canary_wharf, leadenhall_market, limehouse, roof_garden; 2019-08-18 bethnal_green_entrance, birbeck_street_underpass, urban_street_01, urban_street_02; 2019-08-31 epping_forest_01, _02; 2019-02-09 greenwich_park; 2019-09-07 greenwich_park_02, _03, urban_street_03; 2019-09-14 urban_street_04; 2019-12-17 cambridge) | every British panorama of the catalogue: streets, parks and a market in London and Cambridge | searched for a pillar box: NONE found; used for nothing else |
| S9 | https://polyhaven.com/a/rusty_painted_metal ; https://api.polyhaven.com/files/rusty_painted_metal (1k diffuse) | 2026-10-09 | Amal Kumar | CC0 1.0 (Poly Haven) | published 2025-03-18 (taken date not given) | a scan of a weathered red-painted steel surface (a container): faded red 119/64/47 with dark run streaks 44/28/23 over about 7 % of its area | looked at only for how rust runs over red paint; NOT a pillar box and used for no size or colour of the box (7.5) |
| S10 | Poly Haven's catalogues of 521 models and 867 textures; ambientCG's catalogue API (searches for postbox, mailbox, pillar box, cast iron, red paint) | 2026-10-09 | various | CC0 | n/a | no pillar box, post box or letter box in any | nothing |
| S11 | WebSearch result summaries (standard mode, 9 October 2026) | 2026-10-09 | search summaries of ukaa.com, lbsg.org, uknature.co.uk, oxfordhistory.org.uk, Historic Environment Scotland, a Jersey heritage report, hobbyist paint pages | n/a (leads only) | n/a | see 2.3 | LEADS: they corroborated a figure or named a thing to read; NO number was taken from them |
| S12 | TARGET-REVIEW.md (a fresh reviewer, 9 October) | 2026-10-09 | the reviewer | the project's own | 2026-10-09 | the fault F1, the nine narrow points N1 to N9, and a re-run of the panorama search that found no pillar box either | yes: every amendment above; its judgement points are marked as such |

All Poly Haven material is used for the search and for looking only: not placed in the game, not traced into a texture, not fed to an image model.

### 2.2 The search of the panoramas

Poly Haven's catalogue lists 997 HDRIs, 732 of them with coordinates and **265 without**; the ones with coordinates in Britain are the seventeen of S8 (the docklands pair and the other 2025 sets at 53.3 N 6.2 W are Dublin, where boxes are green and Irish: left out; st_fagans_interior is a Welsh interior; none of the 265 without coordinates is labelled British, and a pillar box abroad is not a British one). Each was downloaded as its tone-mapped JPG, **8192 px wide in every case** (`panorama_scan.json`, `source_px`), and searched twice (`scan_panoramas.py`): (1) saturated-red blob detection on a 4096 px reduction (hue within 30 degrees of red, saturation above 0.68, value above 0.30, at least 80 px), then every large blob looked at as a rectilinear crop; (2) eight rectilinear views of 72 degrees round each street panorama, looked at by eye. A pillar box would be 90 px tall at 10 m on that scale. **Every red blob was a tail light, a brick wall, a painted shopfront, a refuse bin, a sign or graffiti; no panorama shows a pillar box.** The reviewer re-ran a looser search (saturation above 0.45, value above 0.12, 40 px) on three of them and found none either. The brief's expected case ("if no reachable photograph shows a pillar box") is therefore the case.

### 2.3 Leads (search summaries: never numbers)

| lead | via | what it did |
|---|---|---|
| a salvage dealer's Carron EIIR box, 73 in tall, about 20 in in the ground, body 15 in wide (also sold as PB42/2, Type B, circa 1966) | WebSearch summary of ukaa.com | by this lead the 73 in casting is a Type B's: it is NOT used for the Type A's height (review F1) |
| the Letter Box Study Group's 1937 Type B: 64 in high, 48 in round (15.3 in across) | WebSearch summary citing lbsg.org and a Scottish heritage listing | the Type B is narrow, the Type A (19 1/4 in) wide |
| the Type K record: cast iron, 63 in high, 19 1/4 in wide, from 1980, five foundries | WebSearch summary of lbsg.org | the Type K variant has the same width as the Type A; its 63 in (1600) agrees with a total near 1.5 to 1.6 m |
| OSM wiki: the larger Type A about 60 in round (19.1 in across) | WebSearch summary | corroborates 489 |
| BS 381C 538 (to about 1968) and 539 (after), renamed Cherry and Currant about 1988 | WebSearch summary of hobbyist pages | a colour name for the review; no sRGB taken |
| red with a black base stipulated in 1874; a listed box of 1936 "red with black base" | WebSearch summaries of a Jersey heritage report and a listed-building record | supports the black band; a reclamation firm shows about 6 in (152) of black: the 200 stays |
| an aperture widening in 1957 (6 1/4 to 8 in) | WebSearch summary of an Oxford history page | none: unclear which dimension; the scene's 320 x 45 kept |
| the Type K has a recessed aperture and no separate domed top | WebSearch summary of uknature.co.uk | the variant's description only |

### 2.4 Unreached

| what | result | used |
|---|---|---|
| Wikipedia, Wikimedia Commons, Geograph, Flickr, archive.org, Sketchfab, lbsg.org (Letter Box Study Group), postboxmap.co.uk, the Postal Museum, Europeana, the National Archives, Historic England, British Pathe, the Library of Congress, Gutenberg, the British Library, Openverse | no connection or refused (status 000) from this cloud on 9 October 2026; the reviewer found the same for six of them | nothing |
| GitHub search | 403 (the API refuses searches outside the session's repositories) | nothing |
| ambientCG downloads | refused in earlier targets; the catalogue has no pillar box | nothing |

### 2.5 What to read once the network opens

1. Dated photographs, 1975 to 2000, of Type A and Type B boxes of the 1950s-60s on provincial British streets: front, side, three-quarter, with a person or the kerb (125 mm) in frame. Geograph, Wikimedia Commons categories of UK pillar boxes, Flickr's archive sets, local archives (Leodis, Picture Sheffield, Tyne and Wear, Hull History Centre). **The one photograph that settles most**: a dated, square-on front view of a 1950s-60s Type A, the whole box from the footway to the dome, camera about 1 m up and 4 to 6 m away, with the kerb's 125 mm upstand or a standing person in frame; licence and date read on the file page. It settles at once the height, the slot's width and height, the cap's overhang and the dome's rise, the door's size and whether any hinge shows, and the order and sizes of cypher, lettering and plate.
2. The Letter Box Study Group's type records for Type A, B and K (heights, widths, apertures by date, the 1957 aperture change).
3. Royal Mail's and the Postal Museum's archives: repaint and paint specifications of the 1980s (the black band's height, the red), drawings of the standard boxes.
4. Historic England and Cadw listings of Type A boxes (some give measured sizes).
5. A measured visit: a real Type A on a street near the PC, with a tape and a scale rod. The PC has the network the cloud lacks.
6. Dated photographs of a new Type K of the 1980s, to decide whether the variant needs writing.

## 3. The frame, the datum, the facing

* Origin: the box's vertical axis at the footway surface, z = 0. +y is the FRONT (door, slot, plate), +x is the viewer's right looking at the front, z up. The pivot of the .glb is that point; the hidden skirt runs to z = -150. [Judgement, the brief's pivot rule]
* Footway level: the scene's footway falls toward the road at 1 in 40, flags +110 above the channel at the kerb's back (kerbs target), so at the axis (0.60 m back) the footway is 110 + 15 = 125 above the channel; across the 576 foot it differs by 14 mm; the box stands vertical and a fillet takes up the difference. [Read + Derived]
* Setback: the scene's code puts the AXIS 0.60 m behind the back of the kerb (z = FootwayFrontZ + setback). The foot's nearest point is then 312 mm from the kerb's back, and the clear footway past the box is 2000 - 600 - 288 = 1112. If "0.6 m back from the kerb" was meant to the nearest edge the axis moves to 0.89 m and 824 mm remain (see 9.1). [Read]
* **Facing: the building line** (the east side's shops, away from the carriageway). The scene's stand-in has its slot on the road side (StreetVignette.cs PillarBox puts it at z - sgn x 0.48 x d: Read); this target goes against it, as a Judgement (the reviewer's, N6), for three reasons: the foot stands 312 mm from the kerb's back, so a road-facing slot would put anyone posting a letter on the kerb edge or in the channel; a kerbside box on a 2 m footway faces the footway or along it; and the player walks the footway and would see the box's plain back. The kit piece is therefore turned 180 degrees about the vertical against the stand-in, and the scene owner is told (9.2); if the scene owner keeps the road side, the reason is to be recorded. The road side is then the back, where the kerb-side scrape, the sticker and the foot's worst knocks go (7).
* The east lamp column of the scene stands at x = 28.0 on the same line, 1.0 m from the box (Derived from lighting.column: first at 8.0, one every 10 m on alternate sides). The foot clears its base by 612 mm. The lantern (5 m up, 0.5 m out) lights the cap from above, and at night the box is the nearest object in the street to a sodium lamp (6.5).

## 4. The target, part by part

Kinds: **Read** (printed in the repository), **Derived** (computed from others), **Judgement** (the writer's choice). There are no **Scaled** and no **Photo** numbers: none was measured on a drawing or a photograph. Where a Judgement rests on the writer's general knowledge of the type and on no source read in this session, it is marked *Memory*: the lowest weight, a guess for the first dated photograph to correct. `target.json` `numbers` carries every number's kind and source (91 of them: 46 Read, 11 Derived, 34 Judgement).

### 4.1 The type: one main model, one variant not built

**Main: Type A, cast iron, 1950s-60s, domed cap with a moulded rim, hooded aperture, a flush door.** Why:
1. The street is a Victorian port quarter in 1990: the stock is the older cast-iron standard boxes; the capless Type K was introduced on 31 July 1980 and is the newer replacement (the research, Read; it recommends "an EIIR Type A of the 1950s-60s").
2. The stand-in already has a cap and a dome, so the silhouette the street was blocked with is the Type A's.
3. The Type A gives the camera four things to read at 1.6 m (the cap, the hooded slot, the door with its plate, the foot); the capless box has fewer.
4. The postal cypher and the operator's lettering, which canon owes, have clear places to stay reserved and flush on a Type A (a band, a disc); on a capless box they are cast into the aperture plate.

**Variant: Type K, capless (`type_k_capless`), NOT built.** The evidence supports only that one stood in some 1990 streets (the research, Read) and that it has the same 19 1/4 in width (two search leads). A coarse profile is in `target.json` `decision_type.variant` (the same body and foot, a flush rounded crown, no cap, the aperture recessed) and flagged "lead only, unmeasured". The street needs one box; do not build it unless asked.

### 4.2 The lathe profile (body, foot, cap and dome)

Outer surface, (radius, z) in mm from the hidden skirt up the axis; `target.json` `profile.outer_rz` has the 69 points. Revolve about the axis. The ratio of height to body width is 1500 / 489 = 3.07.

| segment | z from to | radius | kind |
|---|---|---|---|
| hidden skirt | -150 to 0 | 288 | Judgement (the real casting goes some 15 to 20 in deeper, the research; only 150 is modelled) |
| foot band | 0 to 48 | 288 | Judgement, *Memory* |
| foot top round | 48 to 60 | quarter round R 12 from 288 to 276 | Judgement |
| splay | 60 to 72 | 276 to 262 | Judgement |
| cove | 72 to 140 | an ellipse quadrant from 262 (horizontal) to 244.5 (vertical) | Judgement |
| body | 140 to 1343 | 244.5 (a plain cylinder, no taper) | Derived (19 1/4 in = 489 across) |
| cap under-moulding (cove) | 1343 to 1356 | 244.5 out to 280 (horizontal at the lip) | Judgement, *Memory* |
| cap rim | 1356 to 1378 | 280 (vertical, a sharp lower drip edge) | Judgement |
| cap bead | 1378 to 1390 | quarter round R 12 from 280 to 268 | Judgement |
| shelf and neck | 1390 to 1420 | 268 in to 250 (a flat shelf), then vertical | Judgement |
| dome | 1420 to 1500 | a spherical cap, chord radius 250, rise 80, sphere radius 430.6, apex on the axis at 1500 | Judgement, *Memory* |

Bevels (`target.json` `bevels`): cap rim lips 1.5, foot band bottom 2.0, door perimeter 1.0, hood lip 2.0, plate bezel 1.5, slot lips 1.0. Surface: sand-cast, a 0.3 mm bump at about 4 mm wavelength (a normal map; Judgement), a 0.5 mm raised casting seam down the back (x = 0, y < 0), and a thick paint bead (0.3 to 0.6 mm) along every edge. No finial or boss on the dome: the research names none. **The silhouette is checked against this table** (`profile_silhouette`, 9.3): a cap that is a plain 560 disc, or a foot without its round, splay and cove, fails.

### 4.3 The foot and how it stands in the footway

* The foot (the plinth) is the 576 mm band with its splay and cove above. The scene's 597 is read as this widest part at the pavement (3.5 % over).
* The casting goes some 15 to 20 in into the ground (the research); the model carries 150 mm of it as a hidden skirt, so the paving can dip or the pavement be cut round it without a gap. (The first draft derived a 482 mm depth from the 73 in listing; that derivation is dropped.)
* The flags (the footway family's) are cut to a rough round 20 to 60 mm from the foot, with a gap of 5 to 12 mm that a **fillet** covers: dark bitumen and mortar, 56/53/50, roughness 0.9, 15 to 35 mm wide and about 10 mm high at the foot, feathered to nothing on the paving, wider on the uphill (building) side. [Judgement]
* Black base band: the foot and the lowest 200 mm of the box are black, 35/35/36 (the wear target's iron_black), roughness 0.5; the line to the red is a brush line that wavers +-3 mm, the red overlapping the black by 1 to 2 mm in places. The 200 is the research's "about 20 cm tall" [Read]; a reclamation firm's "about 6 in showing" (152) is a lead that did not move it. The band crosses the cove (z 140 to 200) and covers the foot and the lowest 60 mm of the body.

### 4.4 The aperture, its hood, sill and flap

| part | numbers | kind |
|---|---|---|
| slot | 320 wide x 45 high, z 1255.5 to 1300.5, centred on the front axis (centre 1278, the scene's 1150 + 128), corner radius 5, cut through the 12 mm wall into a black interior (8/8/8, roughness 0.9); half angle on the cylinder 40.9 degrees; its top is 42.5 under the cap's under-moulding ("just under the cap", the research) | size Read (the scene), centre Derived, corner Judgement |
| hood | a curved lip wrapped round the front above the slot: underside flat on the slot's top (z 1300.5), front face at radius 274.5 (30 proud, **5.5 inside the cap rim's 280**) to z 1323, top sloping back to the body at z 1333 (10 under the cap's under-moulding), half angle 48 degrees (a little wider than the slot), cheeks on radial planes | Judgement, *Memory* |
| sill | a lip below the slot: a chamfer from the body at z 1240 to 11.5 proud at z 1251.5, flat to z 1255.5 (the slot's bottom), half angle 44 degrees | Judgement |
| flap | a 300 x 30 x 2 plate hinged along the inside top of the slot, hanging tilted 15 degrees, dark iron 40/40/42, seen through the opening | Judgement, *Memory* |

### 4.5 The door and the lock

| part | numbers | kind |
|---|---|---|
| door | x -150 to 150 (300 wide as a chord, half angle 37.7 degrees), z 280 to 1168 (888 high), **1 proud**: a cylindrical panel concentric with the body, outer radius 245.5, corner radius 10; a joint groove 3 wide x 3 deep round it is what shows it; plain, sand-cast, painted red | Judgement; the research says "a flush panel" (Read) |
| hinges | **none showing**: the hinges are internal (a knocked-out pin must not open the box); "hinged on the left" is the side of the joint only; no part on the door's left edge stands more than 1.5 mm proud of the door face | Judgement (review N3) |
| lock | on the RIGHT: an escutcheon disc 36 across, 3 proud, centred x 112, z 818; a keyhole slot 4 x 12; a swivel shutter 22 x 10 x 2 **painted with the door (150/30/32, metal 0), worn to dark bare metal 60/52/46 on its 1 mm edge only**; no maker's mark | Judgement, *Memory* (review N8) |

### 4.6 The flush reserved areas and the one plate frame

| part | numbers | kind |
|---|---|---|
| reserved for lettering | a FLUSH band on the body's own face (radius 244.5), concentric with the body, x -150 to 150 (300 wide as a chord, half angle 37.8 degrees), z 1190 to 1230 (40 high, centre 1210); no raised or cut geometry at all, relief 0 | Judgement, *Memory* (the position) |
| reserved for cypher | a FLUSH disc on the door's own face (radius 245.5), concentric with the door's face and centred on the door's axis at z 1088, 110 across; no raised or cut geometry at all, relief 0 | Judgement, *Memory* |
| collection-plate frame | a flat-faced boss 210 x 125 centred at (0, 918): its face plane is y = 254.5 (9 above the door's face at the axis), its sides run back to the cylinder (so the boss stands 33 mm proud at its edges); a 12 bezel; the plate window 186 x 101 recessed 3 below the bezel face | Judgement, *Memory* |

A real box carries its cypher and lettering as raised letters directly on the iron: it has no blank disc and no blank tablet, and a blank plate on a wall "is a placeholder that looks like a bug" (the scene's own words about a name plate). So the two reserved areas are flat, and the box carries ONE plate (the enamel instruction plate and its frame are deleted). The minted cypher and the lettering are cast in the reserved areas once canon supplies them. The real order of cypher, lettering and plate on the front of a Type A is the first thing to read from a dated photograph: each may be 40 mm or more out. The stack is placed so that nothing overlaps (self-check D): the door's top (1168), the lettering area (1190 to 1230), the sill (1240); down the door the roundel (1033 to 1143), the collection frame (855.5 to 980.5), the lock (800 to 836), 19 mm or more between them. It is the first draft's stack moved up 128, each item the same distance under the door's top.

### 4.7 The words on the box, and why they are safe

Canon: the postal cypher (the pillar box's) and the telephone operator's mark are owed by the brand bible; "ER", a crown, "POST OFFICE", "ROYAL MAIL" and a real maker's casting mark are not allowed (brief). So:

* **The reserved areas, hood, sill, door, foot, cap: no letters, numerals, crown or relief device at all.** No maker's name or date.
* **The collection-times plate: exactly five strings, nothing else**, black (22/22/24) on white vitreous enamel (232/229/218) with a 2 mm black border line inset 4 mm:
  * `COLLECTIONS` (bold, cap height 11, centred, 14 from the top), under it a 1.5 mm black rule inset 14,
  * `MON-FRI` (left, cap height 8, baseline 52 from the top) and `5.30 PM` (right),
  * `SAT` (left, cap height 8, baseline 76) and `12 NOON` (right).
  Any plain grotesque from production/fonts will do at 8 mm (OFL); a period face is not needed.
* **Why they are safe:** they are the plain English words and times a collection plate needs, as a notice on any street names no company; none names an operator, brand, council, maker or reign, none is a cypher or a crown; "POST OFFICE", "ROYAL MAIL", "LETTERS" on the slot, "GPO", "ER", "GR" and any foundry name are NOT used; the days are standard abbreviations; the times are an invented, plausible 1990 pattern (a weekday last collection, a Saturday noon, nothing on Sunday). If the brand bible or Jafar wants no lettering at all, delete the text list and the frame with it: variant `no_plate`, a flush door (the self-check and the checks accept both).

### 4.8 Triangle budget and the build

Mid-poly with a bevel on every edge (the asset plan's method, Read): about 8,000 to 30,000 triangles at LOD0 (Judgement). One mesh for the box, the plate as its own material slot, one UV set (the girth in the U direction for the wear strip, section 7).

## 5. Photographs win: what was overturned

No photograph was reached, so no photograph overrides anything. The repository's own figures disagree with each other, and with the reviewer's judgement, in places; each choice is below and in `target.json` `photographs_win`.

| item | a | b | chosen |
|---|---|---|---|
| height | the first draft's 1372 (the scene's BODY figure read as the whole box, and the 73 in listing's 135 to 147 cm) | the research's working figure 150 cm ("the top is at about 150 cm"), its Type A line 5 ft 4 in (1626), the scene's own stand-in 1612 | **1500 (Read: the research's working figure)**; 1626 recorded as the upper alternative; 1350 to 1470 is a casting's length (a lead says a Type B's) and is not used; the stand-in is 0.11 m too tall |
| body width | the scene 597 (a trade guess) | the research 49 cm / 19 1/4 in (untraced) and 19 in (a c.1955 listing) | 489 for the body; the scene's 597 is read as the foot (576 chosen) |
| cap width | the scene 660 (1.35 x the body) | the research: the rim is "a few centimetres proud of the body" | 560 (35.5 proud), the outermost line above the foot; the hood tucks 5.5 inside it |
| dome rise | the scene 140 | none | 80 (rise / diameter 0.14 on the 560 cap) |
| door | the research: "a flush panel with the cast cipher, a plate frame and a keyhole" | the first draft: 4 proud with hinges | 1 proud (outer radius 245.5), a 3 x 3 joint groove showing the door; no hinge shows (internal hinges); the research is Read, the hinges were an invention |
| facing | the scene: the slot on the road side (StreetVignette.cs PillarBox, Read) | the review (Judgement): a kerbside box on a 2 m footway faces the footway; the poster must not stand on the kerb edge, and the player walks the footway | the building line (toward the shops); the scene owner is told and, if the road side is kept, records why |
| aperture | the scene 320 x 45 at 1150 | a search lead: widened in 1957 (6 1/4 to 8 in), unclear which dimension; the research: "just under the cap" | 320 x 45 kept (Read); the centre moves up with the cap to 1278 |
| red | the wear target 150/30/32 | BS 381C 538 or 539 (a search lead: 538 to about 1968, 539 after) | 150/30/32 kept: the lead gives a shade name, not an sRGB |
| black band height | the research about 200 | a lead: about 6 in (152) showing when a reclamation firm sets a box | 200 |
| iron_wear share | the wear target 4 to 8 % (a downpipe) | this target 3 to 6 % | 3 to 6 %, typical 4 % (the wear writer to confirm) |

**On the height, why the reviewer is right.** The first draft's argument was that the scene's 1.372 is a "body" figure and the 73 in listing gives 1350 to 1470. But the research's own working figure is "about 150 cm above ground", its breakdown ends "the top is at about 150 cm", its untraced Type A line is 5 ft 4 in (1626) and the scene's stand-in is 1612; the 73 in listing is a casting's length whose own lead sells it as the narrow Type B. I have no figure in the repository that shows the reviewer wrong, so 1500 stands, kind Read, and everything from the sill up moves +128.

## 6. Materials and colours

### 6.1 The table

| surface | sRGB | name | roughness (words, 0 to 1) | metal | kind |
|---|---|---|---|---|---|
| red paint | 150/30/32 | pillar-box red, a deep gloss red | semi-gloss 0.35 on the body (a gloss enamel five to eight years after its last repaint); 0.45 on the top of the dome and cap rim (chalked) | 0 | colour Read (the wear target), roughness Judgement |
| black base paint | 35/35/36 | black | 0.5, satin | 0 | Read (wear target iron_black) |
| plate enamel | 232/229/218 | white vitreous enamel | 0.12, glossy | 0 | Judgement |
| plate text and border | 22/22/24 | black | 0.3 | 0 | Judgement |
| keyhole shutter | 150/30/32, edge 60/52/46 (1 mm) | painted with the door, worn bare at its edge | 0.35 | 0 (edge: bare metal) | Judgement (review N8) |
| flap | 40/40/42 | dark iron | 0.6 | 1 | Judgement |
| slot interior | 8/8/8 | black | 0.9 | 0 | Judgement |
| bare iron and rust in a chip | 141/102/72 (rust), 118/112/106 (grey primer), 112/56/34 (rust halo on red) | see 7.1 | 0.65 | 0.3 on a rusty chip, 1 on the bright sill band | wear target (Read) / Judgement |
| footway fillet | 56/53/50 | bitumen and mortar | 0.9 | 0 | Judgement |

### 6.2 The red

150/30/32 is the wear target's pillar_box_red, kept ("the furniture family's own colour wins" said that target, and this family agrees). Linear (0.305, 0.013, 0.0144), relative luminance 0.075, L* 33, HSV saturation 0.80, value 0.59. Why this and not a lighter, more orange red: (a) art-direction R-B4 makes the red boxes the street's whole high-chroma accent, and the accent budget counts the frame's pixels above saturation 0.6; at 0.80 the red keeps well over that after dirt and a wet sky; (b) the box paint of a port town in 1990 is a deep crimson-leaning red (the lead names BS 381C 538 or 539, "Cherry" and "Currant"), not the bright modern brand red. It is a Read colour with a Judgement behind it; it has not been checked against a paint chip or a photograph.

### 6.3 The accent budget

The box's projected area is about 0.78 m2 (0.489 x 1.5 and the cap's and foot's overhangs). On a 2560 x 1440 frame at 46 degrees vertical it covers about 2.4 % of the frame at 5 m, 0.95 % at 8 m and 0.4 % at 12 m (Derived), far under the 0.078 ceiling on its own. A wet sky lowers the saturation of the cap's top and the brightest patches to about 0.6 to 0.7; the vertical faces stay at 0.75 to 0.8.

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

No photograph shows a pillar box's wear, so every number here is Judgement unless it says it is the wear target's. State: **tired**, five to eight years after its last repaint, one tidy-up of the plate and lock, the chips not touched up; a port town's old quarter in a wet climate (RULINGS: "grime is the strategy"). The road side is the back (180 degrees from the front).

### 7.1 Chips and the layers of paint

A chip shows the repaints: the top red (150/30/32), then an older red (112/26/30, in half the chips), then at the bottom grey primer (118/112/106; 45 %), bare rusty iron (141/102/72; 40 %) or old black (35/35/36; 15 %, only on the base band and the door). Hard-edged, with a thick paint bead round each (0.3 to 0.6 mm) and a rust halo (112/56/34) where iron shows. The wear target's mark for the pillar box (a replacing 124/104/92, the mean of primer and rust) is the average of these. The mask is the wear target's `iron_wear` as a strip tiled round the girth, mirrored on alternate repeats; the girth is 1536 mm and the 214 strip fits 7.2 times, which is not even (a mirrored strip needs an even count to close at the seam), so **use 8 repeats of 192 mm** (the strip 10 % narrower) with the seam at the back (x = 0, y < 0); the mask runs from z = 0 up the 1500 mm (the wear target's is 2.4 m; the lowest 0.3 m keeps its 40 % of the lost paint). Patches 20 / 45 / 110 mm (p10 / p50 / p90), edge 4 mm (the wear target's). **Share of the area lost: 0.03 to 0.06, typical 0.04** of the body and foot (door furniture and slot excluded), against the wear target's 0.04 to 0.08 which is the downpipe's: the box is touched up in service. The wear writer should accept or overrule.

### 7.2 At the base

* 14 to 22 chips in the lowest 400 mm, 3 / 9 / 25 mm equivalent diameter (p10 / p50 / p90), 70 % of them under 300 mm.
* The foot's top round (z 48 to 60) is worn to bare iron over 30 % of the circumference, a band 10 to 14 mm wide, 96/84/76, strongest on the road side, the back (wheels, bags).
* A scrape on the road side at z 380 to 520, 180 long and 20 to 40 high, 15 % bare.

### 7.3 At the aperture

* The hood's lower front edge: 40 % of its length chipped, chips 2 to 10 mm, each with a rust halo.
* The sill lip: a bare band 10 mm wide over 60 % of its length, dull dark iron 80/76/72 (letters scrape it; it is not shiny).
* The slot is black inside, with a faint pale line where the flap's lip catches light.
* 30 to 60 micro-chips of 2 to 8 mm along the door's perimeter, the hood and sill edges, the cap rim's lips, the foot's top edge and the keyhole shutter's edge.

### 7.4 Grime

* Ground up, the wear target's foot-splash envelope: full strength to z 240, 0.85 at 330, 0.5 at 450, 0.15 at 610, gone by 750; on the red the multiplier is 1 - 0.38 x strength (0.62 at the foot) in linear light, the black band 1 - 0.2 x strength.
* Soot under the cap, z 1318 to 1343: x 0.7.
* 5 to 9 rain streaks from the cap rim, 10 to 30 wide, 100 to 350 long, x 1.12 (a cleaner streak down a dirtier ground; the overhang protects what is under it).
* 1 to 3 bird droppings on the dome and rim, 30 to 120 mm, 226/224/214 (the wear target's), with up to one run 10 to 30 wide and 50 to 300 long; the box stands at x 27, so the quay-end weight is 0.4.
* Chalking: the top of the dome and the rim's upper face x 1.08 lighter and a little pink, roughness 0.45.
* 1 to 2 shallow dents, 30 to 60 mm across and 1 to 2 mm deep, at z 300 to 700.

### 7.5 Rust bleed

Sources: every chip below 400 mm, the cap's under-moulding joint (z 1343), the hood's underside (one trickle under its LEFT end) and the foot's top edge; there are no hinges to bleed. Each source: 1 to 2 trickles, 5 / 10 / 20 mm wide, 80 / 200 / 350 long, running straight down, colour on the red 84/40/26, a dark dot of 3 to 10 mm at the source and a 15 to 40 mm brown halo, edge 8 to 25 mm, 0 to 2 detached drops of 20 to 60 mm. The widths follow the wear target's rust_bleed (measured on a brick wall, not on iron). Looked at, not used for numbers: Poly Haven's rusty_painted_metal (a container) shows the run streaks reading about a third of the red's luminance (44/28/23 on 119/64/47) over about 7 % of its area: rust over red paint runs dark brown-black, not orange.

### 7.6 Flyposting traces

* 1 to 2 patches 150 to 260 wide and 120 to 300 high, centres at z 600 to 900, on the sides and back, 70 to 140 degrees round from the front, never on the door, the plate, the lock, the slot or the hood; 20 to 60 % of the paper left, torn on the diagonal (2 to 10 mm hard edge), the paper colour 196/186/168 (the wear target's), a paste ghost 10 to 30 mm wide round it; unreadable remnants: nothing that shows a word, a face, a drink or a wager.
* 0 to 3 stickers of 40 to 100 mm at z 300 to 1100, the same exclusions.
* The scene's G5 sticker decal (0.15 x 0.15 m on the street face at 0.15 m up) sits on the box's road side, which is now the back: keep it there, clear of the door.

### 7.7 First look at 1.6 m

A red cylinder as tall as a man's shoulder; a dark, grimy foot and black band; three or four orange-brown chip clusters low down; one dark rust trickle under the hood's left end; a torn paper remnant on the side; the bright white plate; the black slot under its hood.

## 8. Variants the street needs

One box: `main`. The listed variants (`target.json` `variants`): `main` (built); `no_black_band` (all red to the ground; not built); `type_k_capless` (not built); `no_plate` (no plate and no frame, a flush door, built if canon wants no lettering at all; the reserved areas are unchanged). Per-instance variation: the wear seeds (the girth strip's seed and mirroring) only.

## 9. What the target could not settle, and the handover

### 9.1 Could not settle

1. Whether a Type A of the 1950s-60s stands 1500 above the footway (the research's working figure, kept) or up to 1626 (5 ft 4 in, the research's untraced Type A line): a photograph settles it; read it FIRST.
2. The slot's width: 320 is 65 % of the body's width (Read, the scene's); the reviewer's judgement is that a 1950s-60s Type A's slot is nearer half the body's width; read it SECOND, after the height.
3. The real order and positions on the front of the cypher, the lettering, the plate and the lock; the reserved areas and the frame are placed from the writer's general knowledge (Memory) and each may be 40 mm or more out.
4. The cap's moulding, the dome's rise (80 against the scene's 140) and the 30 mm neck, whether a finial or boss exists, the hood's depth: not to be moved without a photograph.
5. Whether the front faces the building line (this target's choice, the reviewer's) or the carriageway (the scene's stand-in), and which side the door's joint is on.
6. Whether "0.6 m back from the kerb" is to the axis (the scene's code; kept) or to the nearest edge: it moves the box 0.29 m and the clear footway from 1112 to 824 mm.
7. The exact 1990 red (BS 381C 538 or 539, a lead): 150/30/32 is the wear target's guess, checked against the accent budget and not against a chip.
8. The base band's height (200 Read; 152 as a lead) and whether a 1990 repaint kept it.
9. The Type K as a second variant: only worth writing once a dated photograph shows one in a street like this.
10. A "next collection" number tablet or rotary dial: not modelled (the research: uncertain).
11. The reflectance of the red at 589 nm (6.5): a fitted edge gives 0.08, a bluer edge 0.12 to 0.20; a spectrum of the real paint would settle it.

### 9.2 Handover (one line each, for NOW.md and the neighbours)

* **Scene file, furniture E4:** replace body 0.597 / 1.372, cap 0.660 x 0.100 and dome 0.140 with the kit piece (total height 1.500, foot 0.576, body 0.489, cap 0.560); its pivot is the axis at the footway; the stand-in (1.612 in all) was 0.11 m too tall. **The front (door, slot, plate) faces the building line, 180 degrees from the stand-in, whose slot is on the road side (StreetVignette.cs PillarBox): tell the scene owner; if the road side is kept, record why.**
* **Kerbs and footway:** the footway stands at +125 above the channel at the axis (110 at the kerb's back plus 15 of fall); the flags are cut round the foot with a fillet (4.3).
* **Wear:** pillar_box_red keeps 150/30/32; the iron_wear strip is 8 repeats of 192 mm round the 1536 mm girth, not 7.2 of 214; the share 0.03 to 0.06 (typical 0.04); the mask runs from the footway to 1500; the foot-splash envelope applies from the footway; the road side is the back.
* **Lighting:** the east lamp column at x = 28.0 is 1.0 m from the box on the same line; by night under the 589 nm lantern the box reads dark olive-brown (a tenth to a quarter of white), not red (6.5).
* **NOW.md line:** Pillar box target (cloud week 42), second try: NO photograph of a pillar box was reached; Type A, 1500 above the footway (the research's working figure; 1626 the upper alternative), body 489, foot 576, cap 560, red 150/30/32 over a 200 black band, flush reserved areas for the cypher and the lettering, one collection plate with only COLLECTIONS / MON-FRI 5.30 PM / SAT 12 NOON, the front toward the shops; the first dated photograph overrides every size.

### 9.3 The checks (for unit 3.6's automatic check)

`target.json` `checks`: 47 checks, each with a name, what to measure, the expected value, a tolerance and its kind: the total height 1500 +-15, the dome apex 1500 +-10, **`profile_silhouette` (the back half, every 2 mm of z against the profile, 0 within 1.5)**, body 489 +-5, foot 576 +-6, cap rim 560 +-6 (measured in z 1356 to 1378), soffit 1343 +-8 (measured on the back half), slot 320 x 45 centred at 1278, the hood's 30 proud and 5.5 inside the rim, the door 300 x 888 from z 280 and 1 proud +-1, nothing on its left edge more than 1.5 proud, the lock at (112, 818) and its painted shutter, the two reserved areas (no geometry, relief 0 measured radially above the curved face), the collection frame, the black band at 200 +-10, the red albedo 150/30/32 +-6, roughness 0.35 +-0.08, no letters except the five allowed strings, no cypher, crown, operator or maker glyphs, nothing floating, the clearance from the kerb's back (312 +-20) and from the lamp column (612 +-40), the front toward the footway, the wear share, the 8 UV repeats, the triangle range, bevels of at least 1 mm.

### 9.4 Files

* `TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`
* `pb_numbers.py` (every number with its kind and source), `make_target.py` (builds target.json, including the colour block), `make_previews.py`, `scan_panoramas.py` with `panorama_scan.json` (the search of the panoramas)
* previews in production/previews/cloud-week/refs/pillar-box/, named `<ref>-<place>-<what>.jpg`: `target-quay-street-elevations.jpg`, `target-quay-street-plans.jpg`, `target-quay-street-axial-section.jpg`, `target-quay-street-red-dry-wet-sodium.jpg`. They are the DRAWING made from target.json and colour swatches computed in code (own work, no licence): there is no photograph to preview and no target-on-photo overlay. The panoramas of S8 are Andreas Mischok's, CC0, used for the search and not reproduced.
