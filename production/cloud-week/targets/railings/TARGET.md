# Quay Street's railings: the guard rail, the quay railing and chain, and the boundary railings the street does not have: the target (cloud week 42, 9 October 2026)

**Quay Street's one pedestrian guard rail is a 2.0 m panel, 1.0 m high, on two 48.3 mm steel posts (a 42.4 top rail flush with flat caps, a 33.7 rail at 200, seventeen 12 mm bars in 97.1 mm gaps, welded, black, post axes 0.375 m from the kerb face at x 10.0 to 12.0, leaving 1.576 m of footway); the quay kit has no railing, so a 3.0 m-bay tube railing on 76.1 mm posts (two rails, or a rail and a plain 13 mm chain sagging 200) is proposed for the jetty's basin edge and tip only (14 posts, 13 bays); the street has no area railing, chapel railing or yard gate; no photograph of a guard rail or a tube railing was reachable, so both are Judgement, backed by three photographed bar railings (bars every 78.5, 94.5 and 114) and one photographed chain bay.**

The target for the family "railings on Quay Street and its quay", written from Poly Haven's CC0 London photographs (all 2019) and the repository's own numbers. Everything is millimetres unless a line says otherwise (placements are metres in the street's or the south-quay kit's frame); the .glb is metres, z up, scale 1. `target.json` holds the same numbers for a script; `target_drawing.py` draws them (elevations, sections, plans, a sample of each reserve railing, the two placement plans) from target.json alone; `self_check.py` tests them against their own sources (last result: **SELF-CHECK PASS: 190 of 190 tests pass (A printed numbers 61/61, B photograph measurements 39/39, C drawing on the photographs 25/25, D internal consistency 54/54, E text and files 11/11)**). `make_target.py`, `measure.py`, `calibrate.py`, `make_previews.py`, `make_doc.py`, `frames.py` and `rail_lib.py` re-make the files from the hand-read numbers and the panoramas.

**What is photographed and what is not, in one breath.** Photographed (Photo, +-6 % in size): R3B, a tall cast-iron park railing on a brick plinth (bars every 78.5, rails at 445, 1045 and 2000, spire heads to 2300, a hinge post to 2375); R3A, an area railing on a two-stage dwarf wall (bars every 114, rails at 840, 1435 and 1645); R3D, a low dark-green railing on a garden wall (bars every 94.5, rails at 680 and 1085); and LHB, one bay of the marina chain posts, whose lug heights (800 and 405) and chain sag (215 to 240) test the bollards target. **Not photographed, Judgement:** the guard rail A1 and the quay tube railing Q2, every number except the scene's own and the bollards target's chain. This is the target's first version.

## 1. What the street has, what it needs, and where there is nothing to draw

The scene (SCENE-SLOTS.md, read 9 October; vignette-scene.json E8) places one guard rail: **a 2.0 m panel, 1.0 high, posts 0.05, rails 0.04, five infill bars of 0.025, east side, x 10.0 to 12.0, 0.25 m back from the kerb**, beside the gully at x 12.0. It was three panels (to x 16.0) until 29 September, when the AI tester found the east footway walled: the crates of the fish market left 0.65 m between rail and frontage, less than a walking person's 0.68. The held `trunk_protection_railing` is a tree-pit guard and is not this object (the bill of materials says so). The vignette-feet file puts both posts at z 3.375 and the pieces list shows the stand-in's lower rail 0.45 above its foot.

The asset plan names two linear kits for this family: "2 m guard-rail panel (posts, rails, infill)" and "two-rail tube railing with chain", one kit each ("Guard railing; quay railing with chain; fences": 1 kit; 1 kit), 1 to 3 panels on the street and a quay railing "along the quay".

**(a) The kerbside guard rail** is kind A1 below. **(b) The quay.** The south-quay kit (tools/art-recipes/south-quay, read 9 October, built live by the self-check) has a granite cope along every quay edge, ten cast-iron bell bollards, a ladder, a stone parapet on the jetty's seaward side and walled yards with boarded gates; it has **no railing on any quay edge**, and a search of its pieces for "rail" finds none. The bollards target (K5) adds four chain posts and two plain chains about the north quay's ladder (x -69.5, y -40.5 to -31.5). An earlier session read a 1989 photograph of the River Hull (the atlas's R08, Flickr, unreachable here) that shows a "chain-edged quay": chain at a working quay's edge is period-attested, a tube railing is not. So the working north and east quays stay as they are, and **kind Q2, a tube railing with 3.0 m bays, goes only where the public walks out: the jetty's basin edge and its tip before the harbour light** (section 7). This is Judgement and new to the kit; the integrator may refuse it and nothing else in this target depends on it.

**(c) Area and boundary railings: the street has no such place, and none is drawn for it.** Checked in vignette-scene.json (blocks), vignette-pieces.json (641 pieces), terrace-fronts.md, terrace-front.py, the atlas and the hook-cast file:

| place | what the data says | so |
| --- | --- | --- |
| the east parade, six bays and the chandler's (x 3 to 46) | shopfronts on the building line: the frontage line is z 5.125 (3.0 kerb face + 0.125 + 2.0), the stallriser stands 0.15 and the pilasters 0.10 proud; no forecourt, area or dwarf wall; one doorstep stone | no railing |
| the west blocks (x 3 to 21, 24 to 33) | plain terraces and shops on the same line (cottages in the drawn street); no front gardens in the data | no railing |
| the yard mouth (x 21.0 to 24.0, west) | a 3.0 m gap in the data with a dropped kerb; the bollards target's two K1 posts guard its corners; the scene stands a held crowd-control barrier across it (E11, x 22.5, z -4.85); no gate is placed | no gate: whether the yard is ever gated is the town session's call |
| the south-quay kit's walled yards (junction corners) | brick walls 1.40 high with piers every 4.5 m and boarded leaves (the kit's own) | no railing |
| a church or chapel | Father Walsh's chapel is at x 100 in hook-cast.json, past the street's bend; Fairview Chapel is in another district | not on the street |
| the north approach (x > 48) | knee-high garden-wall boxes in the backdrop (terrace-front.py), not game objects | not drawn |

The asset plan's fences kit (chain-link and palisade, along the yard) is a different family's; Poly Haven's `modular_chainlink_fence` (CC0) exists and Urban Street 02's steel palisade is a 2000s form, both left to it. Because the brief asks for photographs to be used where they are reached, three photographed railings are kept in the target as **reserve kinds R3B, R3A and R3D (placed: false)**: if the town session gates the yard or the story gets a chapel, the numbers are here. They also serve as the only photographic evidence for the bar proportions of A1.

## 2. Sources

All photographs are Poly Haven's, CC0 (licence read at https://polyhaven.com/license on 9 October 2026: "Our assets are all licensed as CC0"), author Andreas Mischok, used for measuring only: not placed in the game, not traced into a texture, not fed to an image model. The cloud's network refused every other photograph site (list below). **No photograph from 1975 to 2000 was reached; every photograph is from 2019**, and for each the table says what it shows and whether it is the period object or a replacement.

| id | URL | date read | author, licence | date taken | what it shows | used | period object or replacement |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S1 | https://polyhaven.com/a/bethnal_green_entrance | 2026-10-09 | Andreas Mischok, CC0 1.0 (https://polyhaven.com/license, read 2026-10-09) | 2019-08-18 07:01 UTC (51.526915, -0.054044), api.polyhaven.com/info read 2026-10-09 | a park entrance in Bethnal Green: a tall cast-iron park railing on a brick plinth with a hinge post and brick piers (R3B); a housing block's railing on a two-stage dwarf wall (R3A); a hoop-top railing and gate leaf; bollards; block paving | YES: R3B main photograph, R3A; calibration anchors | the Victorian pattern is long-lived but the paint, the hoop-top gate and the signs are 2000s; whether any of it stood in 1990 is unknown (R3A may be a replica); the picture is for bar proportions, rails, finials and the black paint, not as a 1990 record |
| S2 | https://polyhaven.com/a/urban_street_01 | 2026-10-09 | Andreas Mischok, CC0 1.0 | 2019-08-18 07:09 UTC (51.528295, -0.053879) | an estate street: a low dark-green railing and gate on a dark brick garden wall (R3D); park railings with spear heads on a granite plinth; bollards | YES: R3D; calibration anchors | an estate of the 1960s to 80s with renewed paint; the railing form is plausible for 1990 (a council green), the exact paint date is unknown |
| S3 | https://polyhaven.com/a/limehouse | 2026-10-09 | Andreas Mischok, CC0 1.0 | 2019-05-19 15:45 UTC (51.510606, -0.036324) | a marina basin: bolted cast-iron chain posts with two swags of spiked chain, a timber-piled quay edge across the water, pontoons | YES: LHB (the chain's lug heights and sag; the K5 post cross-check) | a 1980s to 90s marina redevelopment; the chain is ornamental (spiked); only its sag and the post's lug heights are used |
| S4 | the repository | 2026-10-09 | the project, n/a | 2026-09-02 to 2026-10-09 | SCENE-SLOTS.md, vignette-scene.json, vignette-feet.json, vignette-pieces.json, terrace-fronts.md, the kerbs and bollards targets, the south-quay kit (south_quay_geom.py, README, METHOD), the asset plan, the street-clutter research, atlas CONTINUATION.md (R08) | YES: Read numbers | n/a |
| S5 | WebSearch result summaries, 2026-10-09 (three queries: BS 3049 and guard rail infill; the history of British pedestrian guardrail; harbour quay edge railings and chain) | 2026-10-09 | third-party pages reached only as summaries, n/a | n/a | leads: BS 3049:1976 was withdrawn on 15 November 1995 and replaced by BS 7818; present-day guard rails use 12 mm bars at 110 to 112 centres, 50 x 30 mm posts and a 1100 height; a 1983 London study and a 1988 article on guardrail visibility; Kent dates guardrail from the 1930s; Torbay's audit leaves working fish-quay berths unfenced; Bideford's quay has cast-iron posts with tubular bars and chains from 1899 to 1905 | LEADS ONLY: no number taken as a measurement; the 100 gap rule is marked Judgement | n/a |

**Looked at and left out:** greenwich_park_02 (one run of black multi-rail railing along a path edge: square posts, five slender round rails and a flat top rail on a brick edging; SEEN AND NOT MEASURED: no wall or other anchor in its view gives its camera height; it is the nearest photographed thing to a tube railing, and it says a park railing of rails without bars was common in 2019); urban_street_02 (a steel palisade along a railway arch and a security door: a 2000s fence, not a railing of the period); urban_street_03 and 04, cambridge, birbeck_street_underpass, leadenhall_market, greenwich_park x3, roof_garden (no railing that bears on this family; urban_street_04 has plastered balustrades of Kensington, not an ironwork form); canary_wharf and adams_place_bridge (stainless dock-edge balustrades of the 2000s: modern-only forms, not used); docklands_01 and 02 (Dublin, not Britain); Poly Haven models: modular_chainlink_fence and large_iron_gate exist (CC0) but are not period guard rails or the street's; nothing in the catalogue is a guard rail, a tube railing or a quay chain.

**Unreached** (refused with 403 or not resolvable on 9 October; a page that refused is not evidence and nothing was taken from any of them): Wikimedia Commons, Geograph, Flickr (including the Hull photograph R08), archive.org, HathiTrust, Historic England and the Historic England Archive, British Listed Buildings, BSI Knowledge, gov.uk (LTN 2/09), legislation.gov.uk, openverse.org, Wikipedia, Project Gutenberg, Sketchfab, europeana.eu, api.wellcomecollection.org, loc.gov, web.archive.org (all refused with 403 or not resolvable, tried 2026-10-09); only polyhaven.com and ambientcg.com answered.

**What the search summaries gave (leads only, no number taken as a measurement).** BS 3049:1976 "Pedestrian guard rails (metal)" existed in 1990 (it was withdrawn on 15 November 1995 and BS 7818 replaced it); present-day catalogue panels use 12 mm bars at 110 to 112 centres (a 100 mm sphere may not pass), posts 50 x 30 mm and a height of 1100; Kent dates pedestrian guardrail from the 1930s; a 1983 London study and a 1988 article say the conventional rail hid the road and that a see-through type did better; working fish-quay berths in a present-day harbour audit are left unfenced; at Bideford the quay has cast-iron posts with tubular bars and chains from 1899 to 1905. These lead the Judgement numbers below and are named where they do.

## 3. No guard rail was photographed: what the target rests on instead

Fifteen of Poly Haven's British panoramas (every one in Greater London and Cambridge; the two Epping Forest ones and St Fagans' interior were not opened) were looked at in six to eight rectilinear views each. **None shows a kerbside pedestrian guard rail, a tube railing on a quay or a bar railing of the 1976 pattern.** What they show is cast and wrought bar railing (Bethnal Green, Urban Street 01), a steel palisade (Urban Street 02, 2000s, left out), stainless dock-edge balustrades (Canary Wharf, Adams Place Bridge, 2000s, a modern-only form, left out), a hoop-top railing and bolted chain posts with chain (Bethnal Green, Limehouse). Wikimedia Commons, Geograph, Flickr and the Historic England Archive, which hold 1980s photographs of exactly this object, refused the cloud.

So A1 and Q2 are built in three layers, each marked where it is used:

1. **Read**: the scene's numbers (2.0 m panel, 1.0 m high, post 0.05, rail 0.04, x 10.0 and 12.0, z 3.375), the frontage and kerb numbers, the bollards target's chain and 3.0 m bays.
2. **Photo, by analogy**: all three photographed bar railings have their bars at 78.5, 94.5 or 114 centres (clear gaps 61 to 100): none has the scene's 333 mm gaps (five bars in 2.0 m). They are black (22 to 24 grey levels) except one council green. Their feet end in a ball or sit on a rail, their bars are round and plain. These set the bar rhythm and the paint.
3. **Judgement**: tube sizes (the nearest standard tubes to the scene's 50 and 40: 48.3, 42.4 and 33.7; 76.1 for the quay posts), the lower rail's height, the cap, the welds, the ground detail, the wear, and the places on the jetty. Each is flagged in the part tables.

Where the photographs and the scene differ the photographs win, element by element (section 9). The scene's five 25 mm bars are replaced by seventeen 12 mm bars, because a bar railing with 308 mm gaps is not seen in any reached photograph.

## 4. How the photographs were measured, and why the camera height is not 1.6 m

Each panorama (8192 x 4096) is re-projected with numpy to a flat elevation of one vertical plane through the foot line of the object (`rail_lib.py`: a ground point from the foot's pixel and the camera height, a plane through two of them, 1 mm to 4 mm a pixel; the native resolution is 3 to 5 mm at 5 to 7 m, so every picture is soft). **Every length then scales with the camera height at the ground the object stands on**, which the panoramas do not give. Each height is measured by the horizon method of the bollards and kerbs targets (`calibrate.py`: in a levelled panorama the horizon is the middle row; brick courses of a wall are evenly spaced in tan(angle below it), so the camera height above the wall's foot = 75 mm x tan(angle of the foot) / (course pitch in tan units)), on brick walls and piers that stand on the same ground as the railings.

| panorama | anchor | what | raw rows | camera height above the foot (m) |
| --- | --- | --- | --- | --- |
| bethnal_green_entrance | bge_planter_wall | planter wall on the block paving (the bollards target) | cols 5840-5940, rows 2100-2258, foot row 2262, pitch 0.01290 | 0.963 |
| bethnal_green_entrance | bge_gate_pier | brick gate pier of the park entrance, red courses above its blue-brick base, on the paving | cols 2090-2170, rows 1715-2160, foot row 2305, pitch 0.01616 | 0.927 |
| bethnal_green_entrance | bge_dwarf_wall | red courses of the dwarf wall under the area railing R3a (five courses between the two blue bullnose strings) | cols 7535-7550, rows 2100-2175, foot row 2243, pitch 0.01108 | 1.020 |
| limehouse | lh_building_wall_a | the dock building beside the quay walk: red and blue engineering brick courses above the paving (left band) | cols 6890-6910, rows 2165-2392, foot row 2397, pitch 0.01878 | 1.095 |
| limehouse | lh_building_wall_b | the same wall, a second column band | cols 7030-7050, rows 2165-2335, foot row 2342, pitch 0.01636 | 1.052 |
| urban_street_01 | us01_garden_wall | dark brick garden wall on the footway, under the low railing R3d (the bollards target measured it with a 0.07 step to its bollard bed; here the railing stands on the footway itself) | cols 4250-4275, rows 2170-2280, foot row 2287, pitch 0.01203 | 1.156 |
| urban_street_01 | us01_gate_pier | brick gate pier on the same footway (joints at rows 2049, 2061 ... 2170, a steady 12.1 px) | cols 3800-3820, rows 2045-2175, foot row 2225, pitch 0.00945 | 1.084 |

| panorama | stated height at the objects' ground | why |
| --- | --- | --- |
| bethnal_green_entrance | 0.97 +-0.06 | three brick walls and piers on the same block paving as the railings: 0.963, 0.927 and 1.020 m (mean 0.970); the bollards target states 1.02 +-0.07 for this panorama (inside) |
| urban_street_01 | 1.12 +-0.06 | the garden wall and the gate pier on the footway: 1.156 and 1.084 m (mean 1.120); the bollards target adds the 0.07 step to its bed (1.23 and 1.15 there) |
| limehouse | 1.12 +-0.07 | two column bands of the dock building beside the quay walk (1.095, 1.052 m) and the two quoted paver readings (1.15, 1.17): mean 1.117 |

Results: **no panorama was taken at 1.6 m**; the heights are 0.97 (Bethnal Green) and 1.12 m (Urban Street 01 and Limehouse) above the ground of each object. **Every number below is +-6 % in absolute size**; counts, pitches' ratios and the proportions are exact to the pixel. `self_check.py` recomputes every anchor from its stored rows and fails if the mean at the objects' ground is farther from the stated height than the stated error (group B). Where the three families overlap they agree: Bethnal Green 0.97 against the bollards target's 1.02 +-0.07, Limehouse 1.12 against its 1.17 +-0.06; the K5 post reads 1086 here and 1135 there, the same 4.3 % as the camera heights.

The photographed bar pitch is a second, independent hint of the scale: R3B's 78.5 is 3 % over three inches (76.2), and a Victorian railing is likely to have been made to three inches; this is not used to adjust anything.

**Tell the kerbs-and-covers and bollards writers** (already said in their targets): the panoramas are 0.97 to 1.12 m above their ground; sizes taken at 1.6 m are 30 to 65 % too large.

Other methods: `measure.py` finds the bars of R3B as the dark minima of the column profile of a 1 mm elevation at z 700 to 900 and fits their pitch (26 bars, 78.54 mm, rms residual 4.0 mm); its rails as dark rows between the bars; heads, posts, wall tops and rails of the other three were read by eye on gridded 1 mm and 2 mm elevations (`photo_measurements.json`, each with its error and how). The self-check's group C re-detects bars, rails, wall tops and tips on the 3 mm previews and compares them with the drawing (a scale fitted on one dimension, the bar pitch).

## 5. Frame, pivot, glb

* **A1**: local x along the panel (0 at its middle), y across (0 on the rail line, + toward the carriageway), z up from the flag top at the posts. **Pivot: the middle of the panel on the ground.** In the street recipe's frame the axis is z 3.375 and the posts stand at x 10.0 and 12.0 (placements, section 7).
* **Q2**: local x along the run (0 at the middle of a bay), y across (+ toward the water), z up from the apron at the post foot; pivot at the middle of the bay on the ground. Placed in the south-quay kit's frame (x along Quay Street, y across, east +; the apron and copes at +0.05).
* **glb**: metres, z up, scale 1; one mesh per piece kind and material (posts, rails, bars, caps, welds, base plates and nuts, chain links and eyes as separate meshes of the same piece); **no text, no decal with lettering, no number, no crest, no maker's mark** on any mesh or texture.
* The elevation pictures of the photographs are rectified to the plane 110 mm behind the front face of a wall (where a railing stands on a wall), so a feature at the wall's front edge is 13 mm (R3B) lower than its true height; the notes say where this matters.

## 6. The target, kind by kind

Every number carries its kind: **Read** (printed in the repository), **Photo** (measured on a photograph: method in section 4, +-6 % in size), **Derived**, **Judgement** (a trade or period guess, said so).

### 6.1 A1: the kerbside pedestrian guard rail (`guard_rail_panel`, the scene's E8). Judgement, with Read numbers from the scene

| part | dimensions (mm) | position | kind and basis |
| --- | --- | --- | --- |
| post (two) | round steel tube OD 48.3, wall 3.2, 1000 high above the flag; below ground 400, not modelled | axes at x -1000 and +1000, y 0 | Judgement: the nearest standard tube to the scene's 50 (a 1.5 inch nominal-bore tube is 48.3); height Read (the scene's 1.0) |
| post cap (two) | flat pressed-steel plug, OD 52.0, 8.0 thick, rim R2, 2 mm weld bead round it | z 992 to 1000: its top is the panel's top | Judgement |
| top rail | round tube OD 42.4, wall 2.6; saddle-cut ends welded to the posts; length 1951.70 between the post faces | axis z 978.8, so its top is z 1000, flush with the caps | Judgement: 1.25 inch nominal bore; the scene's 40 |
| bottom rail | round tube OD 33.7, wall 2.6; same length and welds | axis z 200 (underside 183): a hand's width over the flags | Judgement: the stand-in's lower rail at 450 had no photograph; R3D's bottom rail is 60 over its wall |
| infill (17 bars) | solid mild-steel round bar Ø12, vertical, from the bottom rail's axis to the top rail's axis (the ends hide in the rails); a 2 mm weld at each end | x = -872.76 ... 872.76, pitch 109.09, clear gap 97.09 between bars and between a bar and a post | Judgement: the gap rule (at most 100) from the search-summary lead; the pitch is inside the photographed 78.5 to 114 |
| weld beads | 3 mm fillet ring where each rail end meets a post; 2 mm at each bar end; not ground off | at the 4 rail ends and the 34 bar ends | Judgement |

* **Overall**: 2052.0 x 52.0 x 1000.0 (the caps at x +-1000 are 52 across). **Panel length**: 2000 between post axes (Read). **How panels join**: a second panel (none on this street) would share the post, its rails butting the same tube; the bars are not offset. **How it ends**: at its posts: an end post is the same post with the same cap; no return, no end rail, no stay; the one panel ends at x 12.0 beside the gully.
* **How it meets the ground**: the posts are concreted into the footway and the flags are cut round them; a **20 mm dark bitumen or tarmac joint ring** (sRGB (40, 38, 36), rough) lies flush round each post; no collar plate, no base plate, no fixing visible. The posts stand on the flag top; the builder reads the ground under them (the scene's foot level is y 0.05625; the kerbs target's flag level gives y 0.040).
* **Edges**: nothing sharp: tube ends saddle-cut and welded, the cap's rim R2, bar ends hidden in welds. **Seams**: the post tubes show a faint longitudinal seam (0.3 mm ridge) on the footway side (Judgement). **Fixings**: none visible (a welded panel on welded posts). **Marks**: none: no plate, number, stencil, crest or maker's name.
* **Paint**: **black gloss paint over galvanising, sRGB (24, 24, 26), semi-gloss, roughness 0.42, metal 0**: the same black as the bollards target's cast posts and the blacks measured on two panoramas (R3A (22, 21, 21) and the K5 post (23, 24, 28); R3B's raw median (36, 43, 30) is polluted by the foliage behind its bars). Variants below.
* **Wear and damage** (Judgement, patterned on what the photographs show of black ironwork: flaking at the collars, rust at the bar feet and the foot of the post, dirt on the plinth): the road face grimed brown-grey by tyre spray to about 500 mm, the footway face cleaner; a dirt line at the foot; top rail polished bright (steel, 150, 150, 152) along its upper surface where hands rest, in patches 150 to 300 long; paint chipped to grey galvanising or primer at the weld beads, at the lower rail's road side (kicked) and on the post caps; rust bloom (110, 60, 32) at the posts' feet and at the weld rings, 0 to 1; one or two bars bent out 5 to 15 mm at 300 to 600 high (a bumped panel), 0 to 2 per panel; a lean of the posts of 0 to 1 degree toward the carriageway; a sticker or poster remnant on the top rail 0 to 2 (pale paper scraps, no lettering); cigarette ends and a sweet wrapper lodged between the kerb and the post (the litter set's, not this kit's).

**Seeds per instance**: lean 0 to 1 degree toward the carriageway; bent bars 0 to 2 (5 to 15 mm out at z 300 to 600); rust at the feet 0 to 1; dirt height 300 to 600; bright-rubbed patches on the top rail 0 to 3; sticker remnants 0 to 2; chips 0 to 10.

### 6.2 Q2: the quay tube railing, two models (`quay_tube_railing`). Judgement; the chain is the bollards target's and Photo for its sag

| part | dimensions (mm) | position | kind and basis |
| --- | --- | --- | --- |
| post | round steel tube OD 76.1, wall 5.0, 1100.0 above the apron; a pressed domed cap OD 80, rise 14, welded; a 5 mm fillet weld at the foot | bay ends at x +-1500 | Judgement: 3 inch nominal bore; a quay post is heavier than the street's |
| base plate | 200 x 200 x 12, four Ø18 holes on a 150 square (25 from each edge), four M16 studs with hex nuts 24 across flats and 13 high, the studs 10 proud of the nuts; 25 mm grout bed and a 20 mm fillet round the plate | z 0 to 12 | Judgement |
| top rail | tube OD 48.3, wall 3.2, saddle-welded; length 2923.90 | axis z 1000 (top 1024.2) | Judgement |
| low rail (Q2a) | tube OD 42.4, wall 2.6, same length | axis z 500 | Judgement |
| chain (Q2b, in place of the low rail) | plain short link, bar 13, inner 39 x 18, outer 65 x 44, pitch 39, **no spikes**; 74 links between two eyes; alternate links edge-on | a catenary from eye to eye, z 500 at the eyes, **sag 200** (lowest z 300); arc 2871.5 | Read: the bollards target's chain; sag Photo (LHB 215 to 240 for the marina's) and not the bollards target's 150 |
| eye ears (Q2b) | flat-bar ears 40 wide x 70 high x 8 thick, a Ø24 hole centred 45 from the post surface; one each side of every post | z 500, on the rail line facing the bay | Judgement (the bollards target's D-lug is 55 x 40 x 18 with the same Ø24 hole) |

* **Bay**: 3000 post axis to post axis (Read: the bollards target's spacing). **Ends**: a run ends at a post of the same kind; at a corner two runs share one post with the rails mitred to it. **Edges**: saddle cuts, fillet welds, cap rim R3, plate edges R2. **Marks**: none.
* **Paint**: black satin over galvanising, sRGB (24, 24, 26), roughness 0.55, metal 0: the K5 post's and the K6 bollards'. Nuts and studs bright steel (150, 150, 152) with dull rust at the threads; the chain black, rubbed bright where the links touch.
* **Wear**: salt bloom (pale, dry) on the sea face of posts and rails to 1.0 m; rust at the base plate, the nuts and the weld rings, 0 to 1; paint rubbed bright on the upper face of the top rail at the walking places (150, 150, 152); the chain black, rubbed bright where the links touch (the bollards target); links slightly rusty at their crossings; a rope scuff on one post at 400 to 600 high, 0 to 1 per run; the apron around the plates stained dark by oil and rain.

**The chain against the photograph (LHB).** One bay of the marina's chain posts, rectified to the plane through two post axes (span 2840, the bollards target's 3.06 read between two posts): the lugs are at z 800 and 405 (the bollards target: 420 and 840, 4 to 5 % higher at its 1.17 m camera), the upper swag hangs to z 585 (sag 215), the lower to 165 (sag 240), the post is 1086 high (1135 there). The target's sag of 200 is between the bollards target's 150 and the photograph's 227; **the bollards writer should raise K5's to 200**. The photographed chain is the marina's ornamental one with spikes on every second link; only its sag and the lugs' heights are used.

### 6.3 The reserve kinds, photographed and not placed (R3B, R3A, R3D)

These stand for the railings a chapel, a yard or a front garden might carry. Each is Photo, +-6 % (R3A +-8 %). **R3B** (the main photograph, 1 mm elevation at 0.97 m):

| element | value (mm) | how |
| --- | --- | --- |
| plinth | brick, four courses at 75 under a stone coping about 50 thick that overhangs 25; the top at z 345 (+-20); a pier 550 wide under the hinge post with a pyramidal cap | Photo; the lip height corrected 13 for the plane's offset |
| rails | three flat bars about 20 x 10: bottom at z 445, middle 1045, top 2000 | Photo: dark rows between the bars |
| bars | round Ø17 (+-3; FWHM 20 with blur), **pitch 78.54** (26 bars, rms residual 4.0), a small ball end under the bottom rail; **every second bar** rises to a spire with a ring at 2040, a vase swelling to 60 across at 2128, a bead at 2190 and a spire to **z 2300**; the others stop at the middle rail with a small spear tip at **z 1225** | Photo |
| hinge post | cast, round, shaft about 100 wide, a collar 155 across at z 2000 to 2035, a vase 135 across at 2180, a spire to **2375**; a boss and a strap hinge near the bottom rail; the gate leaf beyond it is swung open and is not measured | Photo |
| paint, wear | black, semi-gloss, chalky at the lower bars; paint flaking at the post collars, rust spots at the bar feet, moss and lichen on the plinth and a green-black stain under the coping | Photo |

**R3A** (an area railing on a two-stage wall; oblique view, +-8 %): the wall is 780 high (four lower courses of blue-black engineering brick to a blue bullnose string at z 300, five red stretcher courses at 75 to z 705, a blue bullnose coping); three rails at z 840, 1435 and 1645; bars every 114 (the thick tall bars every 228 with fleur-de-lis heads to z 1880, thin short bars between them to the middle rail with a small lily plaque); posts with a vase and ball to z 2150 and scroll knees to the top rail; black. **R3D** (a front-garden railing, 1.12 m camera): a dark brick wall 620 high (eight courses at 75 and a coping), a bottom flat-bar rail at z 680 (60 over the wall) and a top rail at 1085, round bars Ø13 every 94.5 with small spear points to z 1130, a gate leaf about 1040 wide with two C-scrolls hung from a brick pier; **paint dark green, sRGB (38, 56, 36)** (medians in shade (32, 47, 28) and in light (51, 69, 45)), satin. A hoop-top (bow-top) railing and a boarded double gate between brick piers (Urban Street 03) were seen and not measured.

## 7. Where each stands

**The street (A1).** East footway, posts at **x 10.0 and 12.0, axis z 3.375** (Read: vignette-feet.json): 0.375 from the kerb face (z 3.0) = the scene's 0.125 kerb + its 0.25 set-back; **0.205 behind the kerbs target's granite kerb back edge (z 3.170)**, so a gap of 0.181 between the kerb and the post's face remains. The road face is the -z face. The panel ends beside the gully (x 12.0, in the channel, the grate 440 x 290 in the kerbs target).

**Footway left to walk (the check the brief asks for).** The panel's rear face is z 3.399 (axis + 24.15); the nearest fixed projection on the frontage is the stallriser face at z 5.125 - 0.15 = 4.975 (the pilasters' 5.025 are farther back at the shop doors): **1.576 m clear, against a walking person's 0.68** (the scene's note says 1.57). It is the fixtures that decide: **nothing deeper than 0.896 m (1.576 - 0.68) may stand between the rail and the frontage in x 9.5 to 12.5**; the fish market's 0.92 m crates would leave 0.656, which is the failure of 29 September, so they may not stand there. A1_walking_clear (a minimum of 0.68) and A1_no_deep_obstacle are in the checks.

**The quay (Q2), in the south-quay kit's frame (x along Quay Street, y across).** The jetty strip is x -130 to -110, y -100 to -15 (the atlas's north 220 to 240, east 300 to 385); its cope nose is x -110 on the basin edge and y -15 at the tip; its stone parapet (1.1 high, x -129.4 to -128.6) runs on the seaward side to y -23; the harbour light stands at (-120, -19.5) on a plinth 2.8 square; the bollards target puts K6 bollards at (-110.75, -80) and (-110.75, -45) and K7 cleats at x -110.25, y -64, -58, -52. The railing:

| run | model | line | posts (x, y) | bays |
| --- | --- | --- | --- | --- |
| basin edge | Q2a, two rails | x -110.4, 0.4 behind the nose | (-110.4, -36.4), (-110.4, -33.4), (-110.4, -30.4), (-110.4, -27.4), (-110.4, -24.4), (-110.4, -21.4), (-110.4, -18.4), (-110.4, -15.4) | 7 of 3.0 |
| tip, before the harbour light | Q2b, rail and chain | y -15.4, 0.4 behind the nose; shares the corner post (-110.4, -15.4) | (-113.4, -15.4), (-116.4, -15.4), (-119.4, -15.4), (-122.4, -15.4), (-125.4, -15.4), (-128.4, -15.4) | 6 of 3.0 |

**14 posts, 13 bays, 39 m.** The nearest post to a bollard or a cleat is 8.6 m (y -36.4 against -45), to the light's plinth face 2.7 m, to the parapet 7.5 m (the parapet ends at y -23.0 and the tip rail is at y -15.4; the tip's west post at x -128.4 has its plate edge 0.1 m from the line of the parapet's inner face, -128.6). The seaward corner between the tip and the parapet's end (y -15.4 to -23.0) is left open: it is the boats' end. **Not railed: the north quay and the east quay** (boats alongside, ladder, ten bollards, fish boxes; the bollards target's K5 chain posts about the ladder are the only edge protection); the cope's nose stays bare. A person on the jetty has the whole 20 m strip: the 0.68 check is trivially met (Q2_walking_clear).

**Absent, with the reasons:** area railings: none on Quay Street: every frontage stands on the building line (frontage_z 5.125, a doorstep only); the south-quay kit's walled yards have brick piers and boarded gates, no railings; no chapel or church stands on the street (the chapel is at x 100 in hook-cast.json, beyond the bend). yard gate: none: the yard mouth (x 21.0 to 24.0, west) is a 3.0 m gap with a dropped kerb, its two corners guarded by the bollards target's K1 posts, and the scene stands a held crowd-control barrier across it (E11, prop_crowd_control_barrier_0 at x 22.5, z -4.85); the town session decides whether it is ever gated. backdrop: the north approach's garden walls are knee-high stone boxes in the backdrop (terrace-front.py), not game objects.

## 8. Materials and colours

| id | sRGB | roughness (words, 0 to 1) | metal | use |
| --- | --- | --- | --- | --- |
| iron_black_semi | (24, 24, 26) | semi-gloss, dulled, 0.42 | 0 | A1 default; R3B, R3A |
| iron_black_satin | (24, 24, 26) | satin, chalky, 0.55 | 0 | Q2, and the K5 and K6 beside it |
| iron_green | (38, 56, 36) | satin, 0.5 | 0 | R3D |
| galvanised_grey | (118, 120, 122) | dull sheen, 0.5 | 1 | A1 variant: unpainted or chipped to the zinc |
| bright_steel_rub | (150, 150, 152) | polished by hands, 0.35 | 1 | top rails' upper face, nuts, studs, chain contacts |
| rust | (110, 60, 32) | dry, matt, 0.85 | 0 | blooms at feet, welds, nuts |
| bitumen_joint | (40, 38, 36) | dull, 0.8 | 0 | the ring round the A1 posts |

The black is the one paint the three families share (bollards K1, K2, K5, K6: (24, 24, 26)); the photographed blacks measure (22, 21, 21) to (24, 24, 28) before tone-mapping differences. **The only coloured ironwork reached is R3D's green**; red, white, yellow and banded paints are not used (no photograph shows one, and the research says reflective bands are wrong for 1990). No white or yellow band, no sleeve, no reflective strip on any post.

## 9. Wear and damage, summarised; the photographs-win disagreements

Painted iron wears at its feet first (flaking, rust spots, dirt banked up), at the collars and at the rails where hands rest (rubbed bright), and takes dirt from the ground up; the photographed ironwork shows no dents, no graffiti and no stickers except notices wired on. A guard rail beside a kerb takes more: tyre spray on the road face, bumps that bend a bar, scrapes on the lower rail. Quay iron takes salt bloom and rust at its nuts and welds.

| element | book, scene or the earlier targets | photograph | chosen |
| --- | --- | --- | --- |
| infill of the guard rail | the scene's stand-in: five 25 mm bars in 2.0 m (clear gaps of 308); the asset plan "posts, rails, infill" | every photographed bar railing has its bars at 78.5 (R3B), 94.5 (R3D) or 114 (R3A) centres, so clear gaps of 60 to 105; none has a gap over 105. No guard rail was photographed | seventeen 12 mm bars at 109.1 centres (clear gap 97.1): Judgement from the analogues and the search-summary lead; the five-bar stand-in is replaced |
| lower rail height | the stand-in has its lower rail at 0.45 (half height) | R3D's bottom rail is 60 above its wall; R3B's 445 above the ground with a 380 plinth below it; the bars of both run to the bottom rail | lower rail axis at 200: Judgement (no photograph) |
| tube sizes | post 50, rail 40 | none | 48.3 post and 42.4 top rail, 33.7 lower rail: the nearest standard tubes to the scene's 50 and 40 (Judgement; inside the scene numbers' round-off) |
| the post cap | none | none (R3B has cast finials, R3D plain spear points: neither applies to a steel guard rail) | a flat plug cap flush with the rail top, Judgement |
| paint colour | "metal" in the scene | all photographed ironwork is black (22 to 24) except R3D's green (38, 56, 36) | black (24, 24, 26) default, galvanised grey and chipped variants |
| camera height | 1.6 m (the street writer's default) | 0.97 (Bethnal Green), 1.12 (Urban Street 01, Limehouse) at each object's ground | the anchors in section 4; sizes +-6 % |
| chain sag | the bollards target 150 (Judgement) | Photo LHB: 227 +-35 over 2840 (two swags: 215 and 240) | 200 for Q2b; the bollards writer should raise K5's to 200 |
| K5 post height | the bollards target 1135 at 1.17 m | LHB 1086 at 1.12 m (4.3 % lower, the same ratio as the camera heights, 1.12 / 1.17 = 0.957) | no change: agrees inside the errors |

## 10. Variants the street needs

One panel on the street: **A1 one model** (the asset plan's "1 kit"), three conditions chosen once for the one panel (the others stay for other streets): A1_black_scuffed (60 %): default: black, scuffed, rust at the feet; A1_black_chipped (25 %): black with the chips down to grey zinc at the road side and the caps; A1_galvanised (15 %): unpainted dull zinc (a 1970s fitting left unpainted), rust at the welds. **Q2 two models** (Q2a two rails, Q2b rail and chain), one run each. The reserve kinds have one model each. Models per kind at most four (asset plan).

## 11. The checks unit 3.3's automatic check must pass

`target.json` `checks` lists 40: each a name, what to measure, the expected value and the tolerance (a "maximum" or a "minimum" where it is a limit).

| name | what to measure | expected | tolerance | unit | basis |
| --- | --- | --- | --- | --- | --- |
| A1_panel_length | distance between the two post axes | 2000 | +-5 | mm | Read: the scene (2.0 m) and vignette-feet (x 10 and 12) |
| A1_height_to_top | top of the top rail and of the post caps above the flag top at the post | 1000 | +-10 | mm | Read: the scene (1.0 high) |
| A1_post_od | post outside diameter | 48.3 | +-3.0 | mm | Judgement (the scene 50) |
| A1_top_rail_od | top rail outside diameter | 42.4 | +-3.0 | mm | Judgement (the scene 40) |
| A1_bottom_rail_od | bottom rail outside diameter | 33.7 | +-3.0 | mm | Judgement |
| A1_bottom_rail_axis | bottom rail axis above the flag | 200 | +-25 | mm | Judgement |
| A1_bar_count | infill bars between the posts | 17 | +-1 | count | Judgement |
| A1_bar_diameter | infill bar diameter | 12 | +-2 | mm | Judgement |
| A1_bar_gap_max | largest clear gap between bars, and bar to post | 100 | max | mm (maximum) | Judgement |
| A1_bar_gap | the clear gaps are equal | 97.1 | +-3.0 | mm | Judgement |
| A1_bars_touch_rails | each bar's two ends lie within 1 mm of a rail axis | 0 | +-1.0 | mm | Judgement |
| A1_cap_top | post cap top equals the rail top | 0 | +-2.0 | mm | Judgement |
| A1_street_position | post axes at x 10.0 and 12.0, z 3.375 | [10.0, 12.0, 3.375] | +-0.05 | m | Read: vignette-feet.json |
| A1_behind_kerb_back | axis behind the kerbs target's 170 kerb back edge (z 3.170) | 0.205 | +-0.05 | m | Derived |
| A1_walking_clear | clear footway between the panel's rear face (z 3.399) and the nearest fixed frontage projection (stallriser face z 4.975) | 1.576 | min 0.68 | m (at least 0.68) | Derived |
| A1_no_deep_obstacle | no object deeper than 0.896 m stands behind the panel (x 9.5 to 12.5) between the rail and the frontage, so that 0.68 m remains: the fish market's 0.92 m crates may not stand there | 0.896 | max | m (maximum depth) | Derived: 1.576 - 0.68 |
| A1_no_lettering | no lettering, number, crest, maker's mark or plate on any mesh or texture | none | +-0 | - | Read: canon, brief |
| A1_paint_albedo | base colour within 10 of the sRGB of the chosen condition | [24, 24, 26] | +-10 | sRGB | Judgement |
| A1_bbox | overall size of the built panel | [2052.0, 52.0, 1000.0] | +-8.0 | mm | Judgement |
| A1_outline_residual | largest distance between a built elevation outline and the target's at the same x | 0 | +-6 | mm | Judgement |
| A1_foot_ring | dark joint ring round each post at the flags | 20 | +-6 | mm (width) | Judgement |
| A1_lean | seed lean of a post | [0, 1] | +-0 | deg (range) | Judgement |
| Q2_bay | post axis to post axis | 3000 | +-30 | mm | Read: the bollards target (3.0 m) |
| Q2_post_od | post outside diameter | 76.1 | +-4.0 | mm | Judgement |
| Q2_post_height | post top above the apron | 1100 | +-20 | mm | Judgement |
| Q2_top_rail_axis | top rail axis above the apron | 1000 | +-15 | mm | Judgement |
| Q2_top_rail_od | top rail outside diameter | 48.3 | +-3.0 | mm | Judgement |
| Q2_low_rail_axis | low rail (Q2a) or chain eye (Q2b) above the apron | 500 | +-15 | mm | Judgement |
| Q2_base_plate | base plate 200 x 200 x 12 with four nuts on a 150 square | [200, 200, 12] | +-3 | mm | Judgement |
| Q2_chain_bar | chain bar diameter, agreeing with the bollards target | 13 | +-1 | mm | Read: bollards target |
| Q2_chain_sag | mid-span sag of the Q2b chain below its eyes | 200 | +-50 | mm | Photo (LHB 227 +-35) |
| Q2_chain_no_spikes | no spikes on any link | none | +-0 | - | Read: bollards target (plain chain) |
| Q2_basin_posts | eight posts on the line x -110.4, y -36.4 to -15.4 every 3.0 | [-110.4, -36.4, -15.4] | +-0.05 | m | Derived |
| Q2_tip_posts | six more posts on y -15.4, x -113.4 to -128.4 every 3.0 | [-113.4, -128.4, -15.4] | +-0.05 | m | Derived |
| Q2_behind_nose | rail line behind the cope nose (x -110 on the basin edge, y -15 at the tip) | 0.4 | +-0.05 | m | Derived |
| Q2_clear_of_mooring | no post within 8 m of a K6 bollard (-110.75, -45) or a K7 cleat (-110.25, -52 to -64); nearest post y -36.4 | 8.6 | min 8.0 | m (at least 8.0) | Derived |
| Q2_clear_of_light | tip rail at least 2.5 m from the harbour light's plinth face (y -18.1) | 2.7 | min 2.5 | m (at least 2.5) | Derived |
| Q2_walking_clear | a person on the jetty keeps at least 0.68 m between the rail and any fixed object (the jetty is 20 m across) | 19.6 | min 0.68 | m (at least 0.68) | Derived |
| Q2_paint_albedo | base colour within 10 of the sRGB | [24, 24, 26] | +-10 | sRGB | Judgement |
| Q2_no_lettering | no lettering, crest or maker's mark | none | +-0 | - | Judgement |


## 12. What the target could not settle

* No photograph of a British pedestrian guard rail of any date was reachable: the whole of A1 other than the scene's 2.0 m, 1.0 m and the post and rail sizes is Judgement. Eight other panoramas (urban_street_03 and 04, cambridge, birbeck, canary_wharf, adams_place_bridge, roof_garden, greenwich_park) show none.
* Whether Quay Street's rail in 1990 was black, galvanised grey, white-and-black banded or green: all the photographed ironwork is black except one council green; black is the default and the others are variants.
* The lower rail's height and the infill's kind (round bar, flat bar, or open with two rails only). The 1983 and 1988 accident studies (search summaries) say the conventional rail of the 1980s hid the road from short pedestrians and that a see-through type did better, which supports dense infill for the rail of 1990; no number.
* Q2: whether a harbour authority of the Hook would rail the jetty tip; the kit has no railing and the asset plan names one. The Hull 1989 photograph (an earlier session's note) supports chain at a working quay edge, not a tube railing.
* The camera heights rest on 75 mm brick courses (73 to 79 mm if Victorian): +-6 %. The wall and pier anchors agree to 5 %; Limehouse's two own anchors (1.095, 1.052) are 6 % under the bollards target's paver readings (1.15, 1.17), and 1.12 is the mean.
* R3A is oblique (32 degrees): widths there are blur-doubled; only its heights, rails and pitches are used.
* The paint on the photographed ironwork has been renewed since 1990 and the panoramas are 2019: none of R3A, R3B, R3D or the K5 post is known to be older than 1990; a Victorian pattern is plausible for R3B.
* Whether the park railing's bar section is round or square (the blur hides it): round is assumed.
* The one photographed multi-rail tube railing (greenwich_park_02, a path edge) was not measured for want of an anchor: Q2's two-rail form (top 1000, low 500) is not checked against it; a five-rail form would be an alternative for the jetty.

## 13. What I would read once the network opens

* BS 3049:1976 "Specification for pedestrian guard rails (metal)" (withdrawn 15 November 1995; BSI Knowledge or a standards retailer): post and rail sizes, infill, finish, classes; and BS 7818:1995, which replaced it
* Department for Transport Local Transport Note 2/09 "Pedestrian guardrailing" (assets.publishing.service.gov.uk), its history section; Kent County Council's pedestrian guardrail policy (democracy.kent.gov.uk), which dates guardrail from the 1930s
* Wikimedia Commons categories for pedestrian guard railings, railings in Britain and bollards and chains at quays, 1975 to 2000 photographs; Geograph squares of fishing towns (Whitby, Brixham, Grimsby, Hull, North Shields) 1980s to 1990s: the author, licence and date on each file page
* Peter Marshall's River Hull photograph of 1989 (Flickr 51040207776, the atlas's R08): the chain-edged quay, its posts and its chain, if the licence allows measuring
* Historic England: list entries for quay walls and railings (Truro, list entry 1201539, "quay walls and railings"; Bideford, 1282939, cast-iron fence posts with tubular bars and chains), the Historic England Archive's 1980s photographs of dock edges and street furniture
* The Health and Safety Executive's Docks Regulations 1988 and "Safety in Docks" approved code of practice (what edge protection a 1990 quay needed); Torbay and North Devon harbour edge-protection audits (summaries say working fish quay berths were left unfenced)
* Tyne and Wear HER and North Shields Fish Quay conservation area notes; 1980s street-furniture catalogues for guard-rail panels: sizes and finishes only, no makers' marks
* The Traffic Signs Manual and the 1980s DoT "Roads in Urban Areas" guidance on guardrail set-back from the kerb (the scene's 0.25 m behind the kerb is a trade guess; a rule of about 0.45 m from the kerb face is remembered, not read)
* The street recipe's own reference photographs of the Hook sheet, if it shows a railing

## 14. The previews (production/previews/cloud-week/refs/railings/), credited

All crops are of the object only: the railing's own elevation, cut to the objects; a notice board with a telephone number, a boat's name board and a distant figure are painted flat grey; nothing else that the brief bars (no car, person, readable lettering, litter, bottle or sign) is in any picture. Photographs: Poly Haven, CC0, Andreas Mischok (S1 to S3); the drawings are this target's. Elevations are rectified at the stated camera heights; the red outline is the drawing laid on the photograph, the cyan ticks z every 100.

| file | what |
| --- | --- |
| `ph-bethnal_green_entrance-r3b-park-railing-elevation.jpg`, `...-target-on-photo.jpg` | S1: R3B, the main photograph (3 mm a pixel, s 700 to 3870, z -50 to 2450); the drawing laid on it (bars of the fixed panel, rails, plinth, heads, hinge post) |
| `...-r3b-park-railing-head-close.jpg`, `...-foot-close.jpg` | S1: 1 mm closes of the spires and the post's finial, and of the plinth, pier and the bars' ball feet |
| `ph-bethnal_green_entrance-r3a-area-railing-elevation.jpg`, `...-target-on-photo.jpg` | S1: R3A (3 mm, oblique), and the drawing on it |
| `ph-urban_street_01-r3d-garden-railing-elevation.jpg`, `...-target-on-photo.jpg` | S2: R3D and the drawing on it |
| `ph-limehouse-lhb-chain-bay-elevation.jpg`, `...-target-on-photo.jpg` | S3: the chain bay (4 mm), the target's catenary (sag 200, red) at the photographed lug heights; yellow ticks the photographed lowest points |
| `target-drawing-sheet.jpg` | the drawings of A1, Q2a and Q2b (elevations) |
| `target-a1-beside-photographed-bars.jpg` | R3B (78.5), R3D (94.5) and A1 (109.1) at one scale: the evidence for the infill |
| `target-plan-street.jpg`, `target-plan-jetty.jpg` | the east footway at the panel (x 8 to 14) with the 0.68 m walking strip; the jetty with the two runs |

Fitted on the photographs by `self_check.py` group C: R3B's bar centres (22 of the fixed panel's bars, median residual under 4 mm, pitch scale fitted on that one dimension within 1 +-0.02), its three rails, its coping edge, its tall tip and its post top; R3D's wall top, rails and bars; R3A's rails, wall edges and tall bars; the chain's lowest points at LHB.

## 15. Files, and what to hand on

`TARGET.md` (this), `target.json`, `target_drawing.py`, `self_check.py`; the makers `make_target.py` (the numbers), `measure.py`, `calibrate.py` (both need the panoramas), `make_previews.py`, `make_doc.py`, `frames.py`, `rail_lib.py`; `anchors.json` (the horizon anchors' raw rows) and `photo_measurements.json` (the automated and hand-read measurements with their errors).

* **To the builder**: A1 replaces the scene's five-bar stand-in at the same x and z; the posts keep the scene's x 10.0 and 12.0, z 3.375. Q2 is new to the south-quay kit: it needs a recipe step (fourteen posts, thirteen bays, the chain) or a placement from this target; the kit has no railing today.
* **To the bollards writer**: the chain: sag 200, not 150 (Photo LHB, two swags 215 and 240, mean 227 +-35); lug heights 800 and 405 here against 840 and 420 there (inside the errors); K5 height 1086 at 1.12 m against 1135 at 1.17 m (the same 4.3 % as the camera heights)
* **To the kerbs writer**: the kerb stands 0.205 m in front of the guard rail's axis (granite top 170, back edge z 3.170); the flag level at the post is y 0.040 against the scene's 0.05625
* **To the town session**: the fish market's crates (0.92 m deep) must not stand in x 9.5 to 12.5 behind the rail: that leaves 0.656 m of footway, under a walking person's 0.68. Whether the yard mouth gets gates is the town's call; this target has no yard gate
* **For NOW.md**: Railings target (cloud week 42): guard rail A1 = 2.0 m panel, 1.0 m, posts 48.3, rails 42.4 and 33.7 at 1000 and 200, seventeen 12 mm bars (gap 97.1), black; quay tube railing Q2 on the jetty basin edge and tip (14 posts, 13 bays, chain on the tip); no area railings or yard gates on the street; no guard-rail photograph reached.
