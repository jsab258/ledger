# Quay Street's telephone box: the exact target

**The phone box is the 1985-to-1991 stainless kind: 890 x 890 mm in plan and 2192 mm high, a folded stainless lid with a 100 mm skirt, four stainless corner posts 40 mm square, a 270 mm black header carrying only the word Telephone, glazed on three sides above and below a 145 mm band (the door's is a yellow moulded handle panel with a rectangular pull, the sides' black), a stainless back sheet with the payphone on it and a 163 mm open gap under the bottom rail; no operator's mark, no crown, no card advertisement; one box, standing where the scene has it (east x 16.5, centre z 3.675, the door to the shops, the back to the road: the first version's move to x 23.5 rested on a wrong number and is withdrawn); it replaces the 29 September script's kiosk, whose numbers disagree with the photograph in six places; no period KX100 photograph was reached, so the geometry is measured on a 2017 photograph of a unit of the same kind.**

Cloud week 42, unit 13, family 1. Written 13 October 2026, not yet reviewed. `SELF-CHECK phone-box: 113 checks, 113 passed, 0 failed; negative controls 0 of 0 caught (offline)`

## Files in this folder

- `target.json`: the whole target (millimetres; z up; the door faces -y; pivot at the base's centre on the ground). Parts, numbers, photograph features, checks, owed lines.
- `make_target.py` (data and this page), `measure.py` (the pixel measurements on photograph P1), `photo_measurements.json` (their output), `target_drawing.py` (draws target.json alone), `self_check.py` (the checks and their negative controls), `make_previews.py` (the preview crops and the overlay).
- Previews in `production/previews/cloud-week/refs/street-dressing/phone-box/`: p1 (S1 cropped and masked), p1 target-on-photo, p2 (S2 detail).
- Shared tools one level up: `../sd_lib.py`, `../sd_check.py`, `../sd_doc.py`.

## The rulings that bind, and how this target meets each

| ruling | what it says | this target |
|---|---|---|
| RULINGS 2 Oct | the KX100 phone box stays | it is the KX100 kind (S4, S5, S6); one box on the street |
| canon (brands) | every brand fictional; the operator's mark and lettering are owed by the brand bible; no crown | no logo, no operator's name; the plain word Telephone only; the logo zone stays empty (text.logo_zone) |
| RULINGS 3 Oct (sources order) | free assets first, else our own in Blender from real photographs | no CC0 British kiosk exists (S7: 521 Poly Haven models, one non-British payphone); so own work by script (S9's route) |
| content rule (canon D18) | what the rule forbids is out of image and text | no cards or stickers, no drink container, no one in any preview; the data scan finds none |
| NoAI, licences | nothing marked NoAI; photographs free licences, measuring only, never placed or traced | S1 to S3 are CC BY-SA 2.0 Geograph photographs used only to measure; no NoAI source; nothing is placed in the game |
| RULINGS 1 Oct and 3 Oct (the look) | the Hook sheet and KCD2 frames; wet, dark, glistening street; accent budget (art-direction R-B4: red boxes carry the colour) | stainless, black and glass are neutral; the yellow handle panel is the one saturated patch and stays small (145 x 686 mm); the red accent stays with the pillar box |
| RULINGS 1 Oct (night) | pools of lamp light, not one orange wash | the lantern colour (1.0, 0.25, 0.0) linear only; the kiosk's own lamp is off in the sample (owed line O1 covers the lettering; a lit kiosk is a taste item for later) |
| RULINGS 8 Oct | photographs win over books, element by element | section 'Where the photographs win' below; W1 to W8 |
| RULINGS 13 Oct (RECIPE) | a notebook entry per unit | RECIPE.md carries unit 13's entry |
| RULINGS 16 Sep, 29 Sep (money, live talk) | nothing bought without his yes; live talk names no real make, brand or shop and nothing after 1992 | nothing bought (the photographs and the model records are free to read); every name on a part or a card is invented; nothing in the target is dated after 1992 |
| the rest of RULINGS.md | read in full on 13 October for this unit (faces, voices, clothes, people, talk, story, combat, disk and git) | none of them touches this object; the weather ruling (a grey range, never sunshine) governs how the game lights it, not the target |

## Sources

| id | url | read | author | licence | taken | what it shows | used | not used for | period |
|---|---|---|---|---|---|---|---|---|---|
| S1 | https://www.geograph.org.uk/photo/5269043 | 2026-10-13 | David Hillas | CC BY-SA 2.0 (creativecommons.org/licenses/by-sa/2.0, read on the page) | 2017-01-04 | a door-type KX100 in a village verge, head on, whole height, clear glass, the middle band black with a separate pink pull standing beyond the left edge at band height (post-1991), a pink 'Coins' header with a handset pictogram; roof, header, band, lower pane and the four posts all show; the grass hides the foot | YES | the livery (post-1991: the pink pull, the header's lettering and handset pictogram, the operator's printed logo and the notices, all painted out flat in the preview), the interior (painted out), the ground, the handle panel's form (P1's band is black: the form is S2's) | 2017 photograph of a unit built 1985 to 1996; the structure is the same in 1990, the livery differs (1991 revamp), so it is used for geometry only |
| S2 | https://www.geograph.org.uk/photo/5558709 | 2026-10-13 | David Hillas | CC BY-SA 2.0 (read on the page) | 2017-07-19 | a door-type KX100, nearer and looking down: the lid's rolled lip, the black channel frame, the stainless post with one round fixing, the moulded handle panel with its rectangular pull and finger recess, mud on the lower pane, plants at the foot | YES | measuring (the camera looks down about 25 degrees, the sides converge); the sticker on the lid, the etched figure and the notices (not period, real marks) | 2017; unit of the same kind as 1990's apart from the 1991 livery |
| S3 | https://www.geograph.org.uk/photo/5314484 | 2026-10-13 | David Hillas | CC BY-SA 2.0 (read on the page) | 2017-02-17 | the doorless KX100: the back panel, a payphone body with its keypad and handset, a notice frame, the stainless coin-vault housing above a low step, the two side panels seen from inside | YES | any number (oblique, the camera looks down); the notices' text and logos | 2017; the same housing as 1990's |
| S4 | https://www.britishtelephones.com/kxkiosk.htm | 2026-10-13 | the site's author (a hobbyist reference) | read for facts only (nothing copied); facts are not licensed | n/a (undated page) | KX100 dimensions Height 2192, Width 890, Depth 890 (mm), weight 266 kg; sides slightly raised above the ground against litter; the Mk2 'biscuit tin lid'; smoked glass at launch, clear later; the first handle panels yellow, 1991 pink | YES | any photograph or text copied | describes the 1985 to 1996 kiosk |
| S5 | https://www.the-telephone-box.co.uk/kiosks/kx100/ | 2026-10-13 | the site's author (a hobbyist reference) | read for facts only | n/a (undated page) | Height 7 ft 1 in, Width 2 ft 11 in; aluminium frame clad in stainless panels with anodised edging; black plastic modesty panel and trim; the first panels yellow, the phonecard kind green | YES | any number beyond the two dimensions (it gives 2159 x 889, which is 33 mm lower than S4; both are kept, S4 is chosen) | describes the 1985 to 1996 kiosk |
| S6 | https://en.wikipedia.org/wiki/KX_telephone_boxes | 2026-10-13 (raw wikitext through en.wikipedia.org) | Wikipedia contributors | CC BY-SA 4.0 (the page's own) | n/a (a text) | production 1985 to 1996, 3,000 a month in 1987 to 1989; the first deliveries had cylindrical levelling legs, a flat-sheet roof with upturned edges and a multi-panel back, the Mk2 followed with a single back sheet and the biscuit-tin lid; door panel and handle yellow (coin) or green (card) until the 1991 revamp; a windswept gap at the foot | YES | any picture | history of the 1985 to 1996 kiosk |
| S7 | https://api.polyhaven.com/assets?t=models | 2026-10-13 | Poly Haven artists | CC0 1.0 | n/a (the list of 521 models) | no British telephone box of any kind; the only phone is korean_public_payphone_01 (a post-mounted payphone, 401 x 301 x 740 mm) | no | everything: no CC0 model fits, so the kiosk is made by script | n/a |
| S8 | https://api.geograph.org.uk/syndicator.php (the feed; terms phone box, telephone box, telephone kiosk, KX100, phone kiosk, each with takenyear 1975 to 1996) | 2026-10-13 | Geograph contributors | CC BY-SA 2.0 (each page) | 1975 to 1996 searched | about 120 photographs of 1975 to 1996 with a telephone box in them, all of the older red boxes, one white box of a different municipal kind (1989) and one open-sided box named in a caption (1987); not one KX100 photograph before 2009 in about 400 results for the KX100 terms | no | measuring: no period KX100 photograph was reached | n/a |
| S9 | production/assets/street/clutter/kx100-kiosk.glb and tools/meshgen/blender/clutter/kx100_kiosk.py (this repository) | 2026-10-13 | this project | own work | made 29 September 2026 | an earlier scripted kiosk: 0.89 square, 2.18 high, a 50 mm roof slab, header 200 high, band 1.00 to 1.12 m, panes 0.11 to 1.00 and 1.12 to 1.93, a 120 mm gap, the word Telephone in yellow | YES | its numbers (they disagree with P1 in six places, see the reuse table) | n/a |

What was searched: Geograph's feed for `phone box`, `telephone box`, `telephone kiosk`, `KX100`, `phone kiosk` with each year 1975 to 1996 and without a year (about 400 results for the KX100 terms alone). Wikimedia Commons was not asked (the feed answered). archive.org was not searched (no book of kiosk dimensions was expected there). Not reached: the second hobby site (redphonebox) refused the proxy (502), the C20 Society article was not opened (a lead only).

## What already exists, and what is done with it

| existing thing | what it is | verdict | why |
|---|---|---|---|
| tools/meshgen/blender/clutter/kx100_kiosk.py and production/assets/street/clutter/kx100-kiosk.glb (29 Sep) | a scripted 0.89 x 0.89 x 2.18 kiosk with a 50 mm roof slab, header 200, band 1.00 to 1.12, panes 0.11 to 1.00 and 1.12 to 1.93 | REPLACED (rebuilt from this target; its helper functions are reused) | its numbers disagree with P1 in six places (W2 to W5 and the floor plate, section W); it also letters the header in yellow and has no payphone |
| production/specs/vignette-scene.json, furniture E3 | a 0.914 square, 2.515 high kiosk with plinth and cap, east x 16.5 | REPLACED in size, parts and livery; its slot is KEPT | K6 proportions (W1); the slot (east x 16.5, centre z 3.675, door to +z) is right: the set-back 0.55 m is to the kiosk's centre and leaves 0.843 m behind it |
| production/research/street-clutter-1990, asset-plan 3 (A3 assemblies row) | the KX100's frame, panes, band, door, handle panel, payphone, roof slab | KEPT as the list of parts | every named part is in the target |
| Poly Haven models | korean_public_payphone_01 and 520 others | REJECTED | no British kiosk; the payphone is post-mounted and Korean |
| git branches (git log --all for phone box, kiosk, KX100) | no other kiosk work | none to reuse | only the 29 September commit |

## The target

Axes: x across the front (right is +x seen from the front), y from the door (-y) to the back (+y), z up from the ground. Every part is a box or a cylinder; its extents come from target.json and the self-check measures them back from the parts.

### Assembly in words

- **Four stainless posts** (40 x 40 box section, brushed, vertical edges r 3) stand on the ground at the corners and reach the lid's plate. They show 40 mm of stainless on each face.
- **The lid** is a folded stainless lid: a 3 mm plate over four 3 mm skirts 100 mm deep, its lower edge turned in 8 mm; it overhangs the posts by 10 mm each side (P1: 17 mm wider than the posts' 870).
- **The front (the door)** is a leaf hung on three stainless pivot hinges on the right post: black header 270 high and 30 deep; two black stiles 52 wide; a bottom rail 68 high; the yellow handle panel 145 high between the stiles, 10 proud, corners r 8, with a rectangular pull 50 x 66 standing 28 proud at the left (lock) end; two panes of 4 mm toughened glass, upper 1051 to 1822 and lower 231 to 906 (each 4 mm into the frame all round).
- **The two sides** are fixed frames like the front with a plain black band (flush with the posts) in place of the yellow panel and a black fascia the header's height above.
- **The back** is one stainless sheet, 6 mm with its backing, from the ground to the lid. The payphone body (140 wide), keypad, handset on the left and a notice frame hang on its inner face above a stainless coin-vault housing.
- **The foot** is open: only the posts and the back sheet reach the ground; the front and sides stop 163 mm up so litter blows through.
- **Fixings**: round pan-head fixings 4 mm across on the posts beside the handle panel (S2 shows one) and on the lid's skirt corners; no bolts on the glazing (gasketed). Joints: the lid's skirts meet at mitred corners; the header butts the posts; the frames are channels with a gasket line (a 1 mm dark line round each pane).

### Parts, sample variant KX1 (millimetres)

| part | kind | material | x (mm) | y (mm) | z (mm) | edges | note |
|---|---|---|---|---|---|---|---|
| lid_top | box | stainless | -445 to 445 | -445 to 445 | 2189 to 2192 | folded edge r 4 | lid plate, 3 mm sheet |
| lid_skirt_front | box | stainless | -445 to 445 | -445 to -442 | 2092 to 2190 | lower edge turned in 8 mm | skirt 100 deep |
| lid_skirt_back | box | stainless | -445 to 445 | 442 to 445 | 2092 to 2190 | lower edge turned in 8 mm |  |
| lid_skirt_left | box | stainless | -445 to -442 | -442 to 442 | 2092 to 2190 |  |  |
| lid_skirt_right | box | stainless | 442 to 445 | -442 to 442 | 2092 to 2190 |  |  |
| lid_lip_front | box | stainless | -442 to 442 | -442 to -434 | 2092 to 2095 |  | turned-in lower edge, 8 mm |
| lid_lip_back | box | stainless | -442 to 442 | 434 to 442 | 2092 to 2095 |  |  |
| lid_lip_left | box | stainless | -442 to -434 | -434 to 434 | 2092 to 2095 |  |  |
| lid_lip_right | box | stainless | 434 to 442 | -434 to 434 | 2092 to 2095 |  |  |
| p_fl | box | stainless | -435 to -395 | -435 to -395 | 0 to 2189 | vertical edges r 3 | brushed box section 40 x 40 |
| p_fr | box | stainless | 395 to 435 | -435 to -395 | 0 to 2189 | vertical edges r 3 | brushed box section 40 x 40 |
| p_bl | box | stainless | -435 to -395 | 395 to 435 | 0 to 2189 | vertical edges r 3 | brushed box section 40 x 40 |
| p_br | box | stainless | 395 to 435 | 395 to 435 | 0 to 2189 | vertical edges r 3 | brushed box section 40 x 40 |
| f_header | box | black_plastic | -395 to 395 | -435 to -405 | 1822 to 2092 | corners r 6 | black header panel, 30 deep, carries the word |
| f_stile_l | box | black_plastic | -395 to -343 | -435 to -415 | 231 to 1822 | outer edge r 2 | door stile 52 wide, 20 deep |
| f_stile_r | box | black_plastic | 343 to 395 | -435 to -415 | 231 to 1822 | outer edge r 2 |  |
| f_rail_bottom | box | black_plastic | -395 to 395 | -435 to -415 | 163 to 231 | lower edge r 2 | bottom rail 68 high |
| f_band | box | handle_yellow | -343 to 343 | -445 to -415 | 906 to 1051 | corners r 8 | moulded handle panel, 10 proud of the frame |
| f_pull | box | handle_yellow | -343 to -293 | -473 to -445 | 918 to 984 | r 6 | rectangular pull with a finger recess, at the lock end |
| f_glass_up | box | glass | -347 to 347 | -428 to -424 | 1047 to 1826 | arrised 1 mm | upper pane, 4 mm toughened (transparent) |
| f_glass_lo | box | glass | -347 to 347 | -428 to -424 | 227 to 910 | arrised 1 mm | lower pane, 4 mm toughened (transparent) |
| f_hinge1 | cyl | stainless | 385 to 399 | -432 to -418 | 300 to 370 |  | pivot hinge, hinge side right |
| f_hinge2 | cyl | stainless | 385 to 399 | -432 to -418 | 1000 to 1070 |  | pivot hinge, hinge side right |
| f_hinge3 | cyl | stainless | 385 to 399 | -432 to -418 | 1700 to 1770 |  | pivot hinge, hinge side right |
| sl_header | box | black_plastic | -435 to -405 | -395 to 395 | 1822 to 2092 |  | black fascia round the side, same height as the header |
| sl_stile_f | box | black_plastic | -435 to -415 | -395 to -343 | 231 to 1822 |  |  |
| sl_stile_b | box | black_plastic | -435 to -415 | 343 to 395 | 231 to 1822 |  |  |
| sl_rail_bottom | box | black_plastic | -435 to -415 | -395 to 395 | 163 to 231 |  |  |
| sl_band | box | black_plastic | -435 to -415 | -343 to 343 | 906 to 1051 |  | plain black band, flush with the posts |
| sl_glass_up | box | glass | -428 to -424 | -347 to 347 | 1047 to 1826 |  |  (transparent) |
| sl_glass_lo | box | glass | -428 to -424 | -347 to 347 | 227 to 910 |  |  (transparent) |
| sr_header | box | black_plastic | 405 to 435 | -395 to 395 | 1822 to 2092 |  | black fascia round the side, same height as the header |
| sr_stile_f | box | black_plastic | 415 to 435 | -395 to -343 | 231 to 1822 |  |  |
| sr_stile_b | box | black_plastic | 415 to 435 | 343 to 395 | 231 to 1822 |  |  |
| sr_rail_bottom | box | black_plastic | 415 to 435 | -395 to 395 | 163 to 231 |  |  |
| sr_band | box | black_plastic | 415 to 435 | -343 to 343 | 906 to 1051 |  | plain black band, flush with the posts |
| sr_glass_up | box | glass | 424 to 428 | -347 to 347 | 1047 to 1826 |  |  (transparent) |
| sr_glass_lo | box | glass | 424 to 428 | -347 to 347 | 227 to 910 |  |  (transparent) |
| back_panel | box | stainless | -435 to 435 | 429 to 435 | 0 to 2092 |  | single sheet back (Mk2), 6 mm with its backing |
| lower_enclosure | box | stainless | -190 to 260 | 300 to 429 | 120 to 480 |  | coin-vault housing, brushed steel (Judgement) |
| pp_body | box | phone_grey | -170 to -30 | 350 to 429 | 1000 to 1340 |  | payphone body, 140 x 79 x 340 |
| pp_keypad | box | stainless | -150 to -50 | 338 to 350 | 1100 to 1200 |  |  |
| pp_handset | box | black_plastic | -192 to -164 | 340 to 390 | 1120 to 1300 |  | handset on its cradle at the left of the body |
| notice_frame | box | black_plastic | 40 to 210 | 415 to 429 | 1050 to 1350 |  | notice and charges frame |

### The numbers, with their sources and kinds (the self-check measures each back off the parts)

| id | what | value | kind | source and method | tolerance |
|---|---|---|---|---|---|
| N1 | overall height, ground to lid top | 2192 mm | Read | britishtelephones.com KX kiosk page (read 13 Oct): Height 2192; the other site's 7 ft 1 in = 2159 is 33 mm (1.5 percent) lower and is kept as the alternative | +-1.5 |
| N2 | overall width | 890 mm | Read | same page: Width 890; the other site gives 2 ft 11 in = 889 | +-1.5 |
| N3 | overall depth | 890 mm | Read | same page: Depth 890 | +-1.5 |
| N4 | lid skirt depth | 100 mm | Photo | P1 rows roof_top 67.1 to cap_bottom 96.3 (29.2 px) at 3.40 mm per px; error 12 mm | +-12 |
| N5 | header height | 270 mm | Photo | P1 rows cap_bottom 96.3 to header_bottom 176.0 (79.7 px) at 3.40 mm per px; error 15 mm | +-15 |
| N6 | handle band height | 145 mm | Photo | P1 rows band_top 402.6 to band_bottom 445.3 (42.7 px); error 12 mm. P1's middle band is BLACK (post-1991 livery), so only its height comes from P1; the panel's form (the full-width moulded panel with a pull) comes from S2 | +-12 |
| N7 | band centre above the ground | 978.5 mm | Photo | P1 band centre row 424.0, scale from the lid top (67.1) to the bottom rail's lower edge (661.2); error 20 mm | +-20 |
| N8 | gap between the bottom rail and the ground | 163 mm | Photo | P1: post feet row about 709 (+-9) against rail_bottom 661.15: 48 px at 3.41 mm per px = 163 mm, error 35 mm (the first version kept 172 with no source; the review of 13 October asked for P1's 163 or a named source, and 163 is used) | +-35 |
| N9 | clear glazing width | 686 mm | Photo | P1 columns glass_l 437.2 to glass_r 638.2 (201 px) at 3.40 mm per px; error 14 mm | +-14 |
| N10 | post face width (stainless strip seen from the front) | 40 mm | Photo | P1 columns post_l_outer 410.3 to frame_l_outer 421.9 (11.6 px) = 39 mm; error 6 mm | +-6 |
| N11 | door stile face width | 52 mm | Photo | P1 columns frame_l_outer 421.9 to glass_l 437.2 (15.3 px) = 52 mm; error 8 mm | +-8 |
| N12 | lid overhang each side beyond the posts | 10 mm | Photo | P1: lid 17 mm wider than the posts' 870 in total (the lid is 890); error 6 mm | +-6 |

### Photograph measurements (P1, S1)

each edge is the strongest grey-level step inside the recorded window, averaged over the recorded band on the kiosk's own face; the scale is fitted on the height from the lid's top edge to the bottom rail's lower edge only; the photograph leans about 1.8 degrees (the lid edge runs 4 px lower at the right) and the camera looks slightly down, so the tolerance is the measured spread plus 2 px, at least 4 px (14 mm).

| photo | feature | axis | measured px | recorded box (x0 y0 x1 y1) | error px | drawn edge |
|---|---|---|---|---|---|---|
| P1 | roof_top | y | 67.1 | [525, 60, 555, 76] | 4.0 | hi of lid_top |
| P1 | cap_bottom | y | 96.3 | [525, 88, 555, 104] | 4.0 | lo of lid_skirt_front |
| P1 | header_bottom | y | 176.0 | [560, 168, 600, 190] | 4.0 | lo of f_header |
| P1 | band_top | y | 402.6 | [470, 392, 500, 410] | 4.0 | hi of f_band |
| P1 | band_bottom | y | 445.3 | [470, 436, 500, 452] | 4.0 | lo of f_band |
| P1 | rail_top | y | 641.2 | [470, 628, 500, 644] | 4.2 | hi of f_rail_bottom |
| P1 | rail_bottom | y | 661.1 | [470, 650, 500, 664] | 5.1 | lo of f_rail_bottom |
| P1 | post_l_outer | x | 410.3 | [404, 250, 416, 330] | 4.1 | lo of p_fl |
| P1 | frame_l_outer | x | 421.9 | [416, 250, 428, 330] | 4.0 | hi of p_fl |
| P1 | glass_l | x | 437.2 | [430, 250, 444, 330] | 4.0 | hi of f_stile_l |
| P1 | glass_r | x | 638.2 | [630, 250, 645, 330] | 4.0 | lo of f_stile_r |
| P1 | frame_r_outer | x | 654.8 | [646, 250, 660, 330] | 4.0 | lo of p_fr |
| P1 | post_r_outer | x | 665.8 | [660, 250, 672, 330] | 4.2 | hi of p_fr |

### Materials and colours

| id | plain name | sRGB | roughness | metal | note |
|---|---|---|---|---|---|
| stainless | brushed stainless steel | 196, 198, 200 | 0.38 (satin, brushed) | metal | water-stained, never mirror bright |
| black_plastic | black moulded plastic, faded | 26, 26, 27 | 0.55 (semi-matt) | not metal | UV-faded to a very dark grey-brown at the top edges |
| handle_yellow | handle yellow, dulled | 232, 188, 22 | 0.45 (semi-gloss) | not metal | the 1985 to 1991 colour; dulled, scuffed at the pull |
| glass | clear toughened glass, slight grey cast | 205, 212, 214 | 0.05 (smooth) | not metal | transmission 0.84 (Judgement); smoked glass belongs to the first deliveries only |
| phone_grey | payphone body, cream-grey plastic | 168, 164, 150 | 0.50 (semi-matt) | not metal | stained brown by smoke (tobacco is allowed) |

### Wear

- tide mark: dust and splash grime on both lower panes from the bottom rail up to about 350 mm, darkest in the lowest 100 mm, a clean line above (S2)
- streaks of rain-carried grime down the glass from the lid's skirt, three or four, 1 to 3 mm wide as a mask
- scratched patches and fine scratches on the lower pane at hand height and on the yellow handle panel (scuffed at the pull, paint dulled to 232, 188, 22)
- the stainless is water-stained near the foot and the lid's lower lip, never mirror bright
- the black frame faded to dark grey-brown on the sun side, dust in its channels, a few small round fixings visible on the posts (S2 shows one on the left post beside the handle panel)
- litter caught in the gap under the lower rail: two crisp-packet shapes and a few cigarette ends (tobacco is allowed), none inside the kiosk
- NOT shown: any card or sticker advertisement (the content rule), any person, any drink container, any real logo

### Variants the street needs

- KX1 (the sample): the door kiosk. It stands in the street.
- KX2: the doorless open kiosk (S3): the same lid, header, posts, back and payphone with no front leaf, glass, stiles or band; one more place for the town if it wants a second box (none in the scene today).
- conditions (materials, not shapes): C0 sound, C1 grimy (the sample's wear), C2 one lower pane cracked in a star from a point 1 m above the ground (a mask on the glass, not a mesh).
- glass: G0 clear (the sample), G1 smoked (transmission 0.55): the first deliveries of 1985 to 1986 and a few after; at most one in ten on the street.

### Where it stands on Quay Street

**Slot:** east side, where the scene has it: centre x 16.5 m, centre z 3.675 m (the scene's 0.55 m set-back is to the kiosk's CENTRE from the kerb's back edge at z 3.125), the door facing the shopfront (+z, as the scene's kiosk_door at z 4.132 does) and the back sheet to the road; the box's faces at z 3.230 and 4.120 (890 deep), 105 mm from the kerb's back edge in front and 855 mm from the stallriser line (z 4.975) behind the door.

- the slot is the scene's own and is kept: x 16.5, centre z 3.675. The first version moved the box to x 23.5 on two reasons that do not hold. (1) It read the scene's 0.55 m set-back as the distance to the kiosk's front face and so counted 2.0 - 0.55 - 0.89 = 0.56 m of footway; the 0.55 m is to the centre (vignette-pieces.json kiosk_plinth stands at z 3.675 with a 0.914 plan: faces at 3.218 and 4.132), so the strip between the kiosk and the stallriser face (4.975) is 0.843 m with the scene's box and 0.855 m with this target's 890 box, both over the 0.68 m a walker needs; there was no walking-width reason to move it. (2) It argued that a kiosk must not stand before Rita's window: that is an inference, not a ruling; the box stood there on 2 October when Jafar ruled both 'the KX100 phone box stays' and 'Rita's window is the model', so no ruling is read to forbid it
- the move to x 23.5 also failed the street's own pieces: the box (x 23.055 to 23.945, height 2192 on a footway 0.07 to 0.09 above the crown) lay under the empty unit's awning (awning_02 at x 24.0, x 22.5 to 25.5, its sheet 2.35 m above the crown over the box's front edge, its valance hanging to 1.63 m between z 3.39 and 3.40), left 0.45 to 0.6 m of walkable strip at head height in front of it, and stood across the empty unit's shop-door slot (x 22.294 to 23.300); the town's place for the kiosk (hook-cast.json places.kiosk, x 16.5, z 4.3, 'beside kiosk_plinth') and the meetings that use it (kiosk/ritas_step, kiosk/fish_counter) would have been 5.5 m from Rita's step. All of that is why the slot stays, and the shared placement rows (sd_place.py) now test the pose against every piece of vignette-pieces.json and the shopfronts target's door zones
- the town's place for the kiosk, hook-cast.json places.kiosk (x 16.5, z 4.3), lies 0.18 m beyond the door's face (4.120) and 0.15 m beyond the pull (4.148), inside the 855 mm strip: the people who meet there stand at the door, exactly as before; DECISIONS 30 September records that Marta steps onto Rita's step (x 18.0) so that her friendship with Alison at the kiosk still meets, 1.5 m away as before
- the door faces the shops, as the scene's own kiosk_door does (z 4.132); the back sheet, with the payphone's back, faces the road: from the hook camera (x -3, looking up the street) the player sees the stainless back and the lid, not the livery; the clear glazing of the sides shows the interior
- clear of the lamp column at x 28 east (11.5 m), the pillar box at x 27 (10.5 m), the fish market's board (x 14.45 after the A-board target, 1.6 m), the railing (x 10 to 12) and the awnings (x 10.5 to 13.5 and 22.5 to 25.5): the shared placement rows read each of them from the scene

The scene's E3 line is not edited by this unit (it belongs to the scene's owner) and needs no change of place: the target replaces its size, parts and livery only. No move is asked of Jafar.

### Lettering

the word is the plain English word, set in one line, upright, 100 mm tall letters in the middle of the header, in an OFL grotesque such as Liberation Sans (SIL OFL 1.1); no logo, no operator's name, no crown; colour a pale yellow-white (240, 224, 150); the mark the brand bible still owes is a placeholder: the upper pane's logo zone (centred, 300 x 300, from z 1250) stays empty

### Where the photographs win over the books

| id | what | the book or script | the photograph | chosen |
|---|---|---|---|---|
| W1 | size and proportion | the scene file (E3) draws 0.914 square and 2.515 high, a plinth 0.15, a cornice, post 0.1 and a cap 0.7 x 0.2: the proportions of the older red kiosk | P1: height to width 2.51 measured over lid and posts (with the camera leaning), the printed KX100 gives 2192 / 890 = 2.46, the older kiosk 2.75; the lid, header, band and posts match the KX100 | 890 x 890 x 2192; the scene's numbers are replaced |
| W2 | roof | the 29 September script and the research note: a flat stainless slab 50 mm thick, slightly proud | P1 and S2: a folded lid with a skirt about 100 mm deep all round and a rolled lip | lid plate 3 mm on four 3 mm skirts 100 deep |
| W3 | header height | the script: 200 mm (1.93 to 2.13 m) | P1: header from the lid's lower edge to the glazing, 270 mm | 270 mm |
| W4 | the handle band's height above the ground | the script: 1.00 to 1.12 m (a chest-high band 120 mm) | P1: band 906 to 1051 mm, 145 mm high | 906 to 1051 |
| W5 | the foot | the script: panes begin 110 mm up and a floor plate stands inside | P1: the bottom rail's lower edge 163 mm up (48 px), the posts alone reach the ground, no floor plate | 163 mm gap, no floor plate |
| W6 | the lower enclosure | none | S3 shows a stainless housing over a step; kept as a Judgement box | lower_enclosure box, flagged Judgement |
| W7 | the scene's set-back | the scene file: setback_from_kerb_m 0.55 and plan 0.914, read in the first version as 'the kiosk's front is 0.55 m from the kerb' (0.56 m of footway left) | not a photograph: the scene's own kiosk_plinth stands at z 3.675 = 3.125 + 0.55 with a 0.914 plan, so 0.55 is to the CENTRE; the faces are at 3.218 and 4.132 and 0.843 m remains behind it | the slot is kept (x 16.5, z 3.675); with the target's 890 box the strip behind is 0.855 m |
| W8 | P1's middle band | the first version's S1 row: a post-1991 red-pink handle panel | P1's band is black; the only colour is a separate pink pull standing beyond the left edge at band height (about x 388 to 405, y 405 to 435 on the 1024 copy); S2's door has the full-width coloured panel | the band's height comes from P1, the panel's form from S2 |

### Checks for the builder (target.json `checks`)

| check | what to measure | expected | tolerance |
|---|---|---|---|
| N1: overall height, ground to lid top | measure it on the built mesh in millimetres (bbox) | 2192.0 mm | +-1.5 mm |
| N2: overall width | measure it on the built mesh in millimetres (bbox) | 890.0 mm | +-1.5 mm |
| N3: overall depth | measure it on the built mesh in millimetres (bbox) | 890.0 mm | +-1.5 mm |
| N4: lid skirt depth | measure it on the built mesh in millimetres (extent) | 100.0 mm | +-12.0 mm |
| N5: header height | measure it on the built mesh in millimetres (extent) | 270.0 mm | +-15.0 mm |
| N6: handle band height | measure it on the built mesh in millimetres (extent) | 145.0 mm | +-12.0 mm |
| N7: band centre above the ground | measure it on the built mesh in millimetres (centre) | 978.5 mm | +-20.0 mm |
| N8: gap between the bottom rail and the ground | measure it on the built mesh in millimetres (edge) | 163.0 mm | +-35.0 mm |
| N9: clear glazing width | measure it on the built mesh in millimetres (gap) | 686.0 mm | +-14.0 mm |
| N10: post face width (stainless strip seen from the front) | measure it on the built mesh in millimetres (extent) | 40.0 mm | +-6.0 mm |
| N11: door stile face width | measure it on the built mesh in millimetres (extent) | 52.0 mm | +-8.0 mm |
| N12: lid overhang each side beyond the posts | measure it on the built mesh in millimetres (gap) | 10.0 mm | +-6.0 mm |
| C1: three glazed faces and a solid back | count the glazed faces (front, left, right) and the back sheet | 3 glazed, 1 solid | exact |
| C2: three hinges on the right of the door | count pivot hinges on the front's right post | 3 | exact |
| C3: the handle panel is proud of the frame | the panel's front face minus the stile's front face | 10 mm | +-3 mm |
| C4: the pull stands out of the panel | the pull's front face minus the panel's front face | 28 mm | +-6 mm |
| C5: no part floats and every join meets | the contact graph of the meshes (touching within 2 mm) | all parts reach the ground | 0 floating |
| C6: the back, lid and header are closed from the front, back and side at 0, 30 and 45 degrees | rays at the stated faces | 0 get through | exact |
| C7: the header word | the text on the header | Telephone | exact |
| C9: the place | the built kiosk's centre in the street's frame and the way its door faces | x 16.5, centre z 3.675, door to +z | +-0.05 m each, exact direction |
| C8: no real mark | any text or logo on the model | none but the header word | exact |

### For the builder

- build by script from the parts; every part is a box or cylinder with the edges stated in its row; weld the stainless into one shape per post; glass is a separate mesh with a glass material and 4 mm thickness
- replace production/assets/street/clutter/kx100-kiosk.glb with the new kiosk at the slot; the old asset stays in git
- UVs: stainless 1 m tiling brushed (horizontal grain on the lid and back, vertical on the posts); header and handle panel one texture each
- keep the foot gap open and the posts' feet 40 x 40 on the ground

## Owed to Jafar's page (one line each, with a recommendation)

1. May the phone box's header carry the plain word Telephone, with no logo, until the town mints the Meridian operator's mark? (recommended: Yes, the plain word)

## What the target could not settle

- the 1990 header's lettering colour (the research note says yellow on black; no 1985 to 1991 photograph was reached; chosen pale yellow-white, Judgement)
- the side fascia's height (S3 shows the header across the front; the side fascia is Judgement at the same height)
- the interior (payphone, enclosure and notice frame positions are Judgement within about 30 mm: S3 is oblique)
- whether Quay Street's box has a door (the sample has one; KX2 is the alternative)
- smoked or clear glass for the single box (clear chosen: from 1988 on most were clear)
- the exact lid lip profile (S2 shows a rolled lip; modelled as a 3 mm skirt with an 8 mm turned-in edge)

## How the self-check is built

`python self_check.py` (offline) rebuilds the parts' geometry and tests: the overall box against the printed numbers; every printed and photographed number measured back off the parts; no floating part, every part meeting a neighbour, every declared join, no part sinking into another beyond its allowance; each closed face (back, roof, header, handle band, side header) shot with rays square on and leaning 30 and 45 degrees, fine across one direction and coarse along the other; the photograph's features predicted from the drawing with the scale fitted on the height only and compared with the pixels' measured edges; the text scanned for real makers and for what the content rule forbids; the lines for his page for em dashes and italics; this page regenerated and compared. `--live` re-reads the Geograph pages and re-measures the photographs' edges from the pixels; `--previews` checks the preview files. Each of about 20 negative controls is a deliberately wrong copy that must make the named row fail.
