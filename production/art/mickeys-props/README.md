# Mickey's front office: hero props

Hero props for the room the player walks into and sees through the window
(production/specs/mickeys-office.json). Method: section 4 of
production/research/shop-window-interiors/MICKEYS-OTHER-DIRECTION-2026-10-04.md
(mid-poly in Blender, bevels with Harden Normals plus Weighted Normal, no
high-to-low bake, one UV map without overlaps, AO and edge masks baked to
colour attributes).

## Set 1, the desk and its things (6 October 2026)

Seven glb files from six scripts. Each prop is one mesh in metres at real
scale, with its origin at the centre of its base on z = 0 and its front toward
-Y in Blender (glb is Y-up, as Blender exports it).

| Prop | Real reference (read 6 October 2026) | Reference size | Model size | Triangles | glb |
|---|---|---|---|---|---|
| Radio base station with desk mic and coiled lead | Transceiver: Philips FM1000, 1989-1998, [radiomuseum.org](https://www.radiomuseum.org/r/philips_vhfuhf_mobile_transceiver_fm1000_fm1100.html). Form (a set clipped on a mains PSU housing with the speaker): [Pye Museum, fixed mobiles](https://www.pyemuseum.org/divisions/communications/pye_telecom/products/f_mobiles.php). Mic: Kenwood MC-60 desk microphone, [rigpix](https://www.rigpix.com/microphones/kenwood_mc60.htm) | Transceiver 180 x 60 x 210 mm; mic base 170 x 160 mm, mic 170 mm | Transceiver 180 x 61 x 210 mm (0%, +1.7%, 0%); mic base 170 x 160 mm, stalk and head 171 mm (+0.6%); whole prop 320 x 485 x 209 mm | 15,372 | 692 KB |
| Telephone, push-button, coiled cord | MoDiP AIBDC 005579, Viscount telephone, ABS, c.1981-1989, [modip.ac.uk](https://www.modip.ac.uk/artefact/aibdc-005579); fittings from the [Science Museum Group's Viscount](https://collection.sciencemuseumgroup.org.uk/objects/co8054884/viscount-telephone-1982-1995) | 146 x 241 x 114 mm | 146 x 241 x 113.3 mm without the cord (0%, 0%, -0.6%); 196 x 278 x 113 mm with it | 7,998 | 319 KB |
| Jug kettle, corded, unplugged | MoDiP AIBDC 001258, polypropylene jug kettle, c.1990-1999, [modip.ac.uk](https://www.modip.ac.uk/artefact/aibdc-001258); form also from the V&A's [Autoboil](https://collections.vam.ac.uk/item/O1298422/autoboil-electric-jug-kettle-redring-electric-ltd/) | 220 x 130 x 220 mm | 220 x 129.9 x 220 mm (0%, -0.1%, 0%) | 6,884 | 230 KB |
| Mug (off-white, tea line inside) | Science Museum Group Y1980.1.39, porcelain mug, Stoke-on-Trent, 1978, [collection](https://collection.sciencemuseumgroup.org.uk/objects/co8405537/flying-scotsman-commemotive-mug) | 114 (over handle) x 81 x 92 mm | 113.9 x 81 x 92 mm (-0.1%, 0%, 0%) | 4,824 | 154 KB |
| Mug, chipped (brown glaze, chip at the rim) | as above | as above | as above | 4,876 | 151 KB |
| Glass ashtray (smoked, four rests, ash and two filter ends) | Diameter: Ravenhead 4-slot heavy glass ashtray, England, 6 in, [listing](https://poshmark.com/listing/Vintage-Ravenhead-Glass-Co-4Slot-Ashtray-Heavy-Glass-England-6-Diameter-2-pcs-6834f1f9e48e860b88cbd467) (no height given). Height: V&A 44111 ashtray, 1963-1981, 150 x 40 mm, [V&A](https://collections.vam.ac.uk/item/O381809/44111-ashtray-robert-welch/) | 152 x 40 mm | 152 x 152 x 40 mm (0%) | 5,640 | 207 KB |
| Desk lamp, anglepoise-style | Anglepoise Model 90, Herbert Terry & Sons, from 1973, [vintageinfo.be](https://vintageinfo.be/anglepoise-model-90-task-light/) | Base 180 mm, shade 144 x 210 mm, posed 650 high x 450 across | Base 180 mm, shade 144 x 210 mm (by construction); posed 649 x 448 mm (-0.2%, -0.4%) | 13,044 | 516 KB |

Every model is generic: no maker's name, badge or logo, and no one maker's
details (canon: every product is fictional). The references give sizes and the
period's general arrangement only (for the telephone, the common slimline
arrangement of a handset lying lengthways beside the keypad).

### Materials and textures

No textures and no downloaded files are used. Each prop has at most three
plain PBR materials (base colour, roughness, metallic):

- Radio: painted metal (dark grey), black plastic, red acrylic (channel window, lamps, knob lines).
- Telephone: stone-grey ABS (body, handset, cord), grey keys, black (feet, slots, key well, hook).
- Kettle: cream polypropylene gone slightly yellow, grey plastic (switch, lid button, shroud, foot), smoked window.
- Mug: off-white glaze, unglazed biscuit (foot ring), tea line. Mug, chipped: brown glaze, biscuit (foot ring and the chip).
- Ashtray: smoked glass (transmission 1, IOR 1.52; glTF KHR_materials_transmission), ash, cork filter.
- Lamp: mushroom-grey enamel, chrome (springs, knuckles, turntable, switch), frosted bulb.

Texture sources: none. The contact sheet's labels use Windows' Segoe UI; that
font is in the preview image only, never in the game.

### Wear masks

Two masks are baked per prop in Cycles and travel in the glb's **COLOR_0**:
red = **ao** (1 open, 0 occluded; AO distance 2 to 5 cm by prop size),
green = **edges** (Cycles Pointiness mapped from 0.50 to 0.60, 0.62 for the
mugs: 0 flat or concave, 1 a sharp convex edge), blue 0, alpha 1. The .blend
keeps them as colour attributes named "ao" and "edges" (and the packed
"ao_edges"). Why packed: Blender 5.2's glTF exporter keeps only the active
colour set; its "export all" option writes a white COLOR_0 and drops "ao"
(tested 6 October). A plain glTF viewer multiplies base colour by COLOR_0, so
the props look tinted there; the master material should read it as masks.
Long parts get extra edge loops before the bake so vertex masks have samples
along them, not only at buried ends.

### Checks (all scripts run headless from a clean start, 4 to 6 s each)

- UV overlaps (Blender's Select Overlap): 0 faces on every prop.
- COLOR_0 read back from each glb: red and green medians match the "ao" and "edges" bakes.
- Every glb under 1 MB (largest 692 KB, the radio).
- Previews looked at: no faceting or shading faults seen. A faint sawtooth along the top of the radio's channel-window bezel in its Eevee preview is shadow aliasing on a 1 mm step; a close-up without shadows shows the mesh and normals clean.
- The radio is 15.4k triangles, a little over the 15k guide, from its coiled lead and cast fins.
- Each glb re-imported into Blender: one mesh, its UV map, custom normals and COLOR_0 present, base on z = 0.

### Not modelled (for dressing or a later pass)

- Key legends on the telephone and channel digits on the radio's red window: small decals.
- Mains leads (radio, lamp) and the phone's line cord: the dresser routes them to the room's sockets. The kettle stands unplugged.
- Reuse checked first: Poly Haven's desk_lamp_arm_01 on this PC is orange and carries a maker's mark in its texture; vintage_electric_kettle is a metal kettle, not a 1990 jug; vintage_radio_transceiver is military (research note of 4 October).

### Paths

- Scripts: `tools/art-recipes/mickeys-props/` (`radio-base-station.py`, `telephone.py`, `jug-kettle.py`, `mugs.py`, `ashtray.py`, `desk-lamp.py`; shared steps in `_desk_common.py`; contact sheet `desk-contact-sheet.py`, run with Python, which calls Blender).
- Run: `blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/<script>.py [-- --no-render]` (`ashtray.py -- --empty` makes an empty ashtray).
- glb: `F:\LedgerTools\game-inputs\production\assets\mickeys-props\<prop>.glb`
- blend: `F:\LedgerTools\mickeys-props\blend\<prop>.blend`
- Previews and per-prop check reports: `F:\LedgerTools\mickeys-props\previews\<prop>.png` and `<prop>.json`
- Contact sheet: `production/previews/mickeys-props-desk-2026-10-06.jpg`

## Set 2, furniture

6 October 2026. Six props from six scripts, built by a second helper. Each script stands alone: it carries the same
"set 2 kit" block (bevel with Harden Normals, Weighted Normal, Smart UV, the Cycles bakes,
export, preview), builds its prop from an empty scene, bakes, exports and saves. Metres at
real scale, front toward -Y in Blender (the glb is Y-up, as Blender exports it). Floor pieces have
their origin at the base's centre on z = 0; the heater and blind at the back face's bottom centre
(the wall plane, y = 0).

| Prop | Real reference (read 6 October 2026) | Reference size | Model size (measured) | Triangles | glb |
|---|---|---|---|---|---|
| Swivel chair: fabric seat and back, black five-star base on twin castors, loop arms | "Vintage Office Chairs, 1980s, Set of 2", earth-brown fabric, black plastic frame and arms, [Chairish](https://www.chairish.com/product/29209626/vintage-office-chairs-1980s-set-of-2) | H 80, W 68, D 53, seat 43 cm | H 0.800 (-0.1%), W 0.680 (+0.0%), D 0.542 overall (+2.2%; seat front to back rear 0.531, +0.1%), seat 0.423 (-1.7%) | 12,496 | 559 KB |
| Counter, timber top with aluminium edging, framed front, lift-up flap on bar hinges over a two-way gate, end post (3 objects) | Length and depth: the plan (mickeys-office.json); height: the brief; flap and gate 600 mm on "brass bar hinges" and "two way hinges", [Shopequip](https://www.shopequip.co.uk/motorised+checkouts+counters/double+action+hinged+gate+flap+on+bar+hinges-C62-I2553.html); flap hinge 102 x 38 x 3 mm, [Hardware Collective](https://www.hardwarecollective.co.uk/counter-flap-hinge) | 3.80 x 0.50 x 1.05 m; flap 0.60 | 3.800 x 0.5025 (+0.5%, the edging strip) x 1.050 to the top (1.0569 over the hinge knuckles); flap 0.60 | 14,056 | 620 KB |
| Fixed wall bench: three oxblood vinyl seats and back pads, black steel frame, timber boards | Length and depth: the plan; heights: Castelli waiting bench, 1970, seat 46 cm, height 77.5 cm, [1stDibs](https://www.1stdibs.com/furniture/seating/benches/vintage-bench-waiting-room-bench-1970s/id-f_45922882) | 1.60 x 0.50 m (plan); seat 0.46 (0.45 in the plan), top 0.775 | 1.600 x 0.499, seat 0.451 (-1.9%), top 0.780 (+0.6%) | 10,400 | 390 KB |
| Four-drawer foolscap filing cabinet, putty enamel, bar handles, label holders, lock | Vintage four-drawer listings, H 132 W 47 D 62 cm, [Gumtree](https://www.gumtree.com/for-sale/uk/srpsearch+vintage+filing+cabinet); [Storia Vintage](https://storiavintage.com/storage/vintage-polished-steel-4-drawer-filing-cabinet-2039/) 132 x 45 x 62; foolscap 470 x 622 mm, [Bisley](https://www.bisleydirect.co.uk/bs-filing-cabinet-foolscap-four-drawer/) | 1.32 x 0.47 x 0.62 m | 1.320 (+0.0%) x 0.470 (+0.0%) x 0.620 (+0.0%), handles included | 5,624 | 285 KB |
| Wall convector heater: cream enamel, brown moulded ends, top outlet grille, inlet louvre, knob and rockers | Science Museum Group, Tefal electric convector No 64-41, c.1975, 425 x 600 x 155 mm, [collection](https://collection.sciencemuseumgroup.org.uk/objects/co538648/tefal-electric-convector-heater-no-64-41); wall depth: Dimplex panel convectors 430 high x 108 deep, [manual](https://www.dimplex.co.uk/sites/g/files/emiian551/files/2024-03/PLXENC%20-%20Series%20A%20Short%20Instructions%20-%20Issue%204.pdf) | 0.600 x 0.425 x 0.155 m | 0.600 (+0.0%) x 0.4275 (+0.6%) x 0.155 (+0.0%, wall to knob) | 4,446 | 238 KB |
| Venetian blind: 25 mm pale aluminium slats, ladders, lift cords, pull cords and acorn, tilt wand | [Cottai](https://www.cottai.com.tw/en/products-detail/25mm-venetian-Components/) components: slat 25 x 0.21 mm, ladder 21.5 x 28 mm, head rail 24 x 25 mm, bottom rail 10 x 20 mm, 6 mm hex wand; [Veneta](https://venetablinds.com.au/pages/venetian-blinds-specifications) head rail 24 x 25 to 27 mm | as listed; width and drop set by arguments | slats 25 mm at 21.5 mm pitch, head rail 24 x 25, bottom rail 10 x 20 (by construction, 0%; slats 0.5 mm thick, see notes); default 1.20 x 1.50 m, 68 slats at 35 degrees | 8,894 | 388 KB |

The references give sizes and the period's general arrangement only. Every model is generic:
no maker's name, badge, handle shape or lettering. Content: nothing for drink, betting or
children.

### Materials and textures

No textures and no downloaded files are used. Each prop has three plain PBR materials (base
colour, roughness, metallic):

- Chair: brown fabric (the 1987 offices' "mustard-brown fabric seats"), black plastic, chrome (the gas-lift column).
- Counter: stained timber (the top, the flap, the post's cap), dark walnut-effect front and carcass, aluminium (edging strip, flap hinges, gate hinges).
- Bench: oxblood vinyl (DECISIONS 4 October), black steel frame, dark stained timber (seat board, back board).
- Filing cabinet: putty enamel, chrome (handles, label frames, lock), label card.
- Heater: cream enamel (body, knob, rockers, louvre bars), dark brown plastic (moulded ends, control panel), charcoal metal (outlet grille, inlet slot, brackets).
- Blind: pale aluminium paint (slats, rails), off-white nylon (ladders, lift and pull cords), beige plastic (end caps, acorn, tilt wand).

Texture sources: none. Wear in the base colour costs nothing: in the .blend each material darkens
where "ao" is low and shows a worn edge colour where "edges" is high, broken into patches by a
procedural noise; the export strips that back to the plain constants, so the glb's materials are
exactly the values listed in each script and the game's master material does its own wear from
the masks. The contact sheet's labels use Windows' Arial, in the preview image only.

### Wear masks

The same packing as set 1, so one master material reads both sets: the glb's **COLOR_0** is red =
**ao** (1 open, 0 occluded), green = **edges** (0 flat or hollow, 1 a convex edge), blue 0,
alpha 1. The .blend keeps "ao" and "edges" as colour attributes by those names, plus the packed
"ao_edges" that is exported. Both baked in Cycles (CPU) into point-domain attributes: AO
distance 4 cm (blind) to 25 cm (counter); Pointiness mapped from 0.54 to 0.58, calibrated on a
test of this kit's bevels (a 24-sided cylinder reads 0.538, a two-segment bevel 0.557, its corner
0.589). Two traps found and handled in the kit: Cycles welds vertices nearer than 0.35 mm before it
measures Pointiness, so parts touching face to face read as all edge; each connected part is
moved apart for the edge bake (and back). And a face with vertices only on its bevels reads as
all edge, so faces get a support ring just past the bevel and long parts a cut every 0.3 m.

### Checks

- Each script ran headless from a clean start (`--factory-startup`, an empty scene) and rebuilt its prop, glb and .blend: 3 to 25 s each with `--no-render`. Their arguments were tried into a test folder: the counter at 4.81 m (16,624 triangles, over the guide at that length; no UV overlap) and the blind at 0.6 x 2.2 m with the slats at 70 degrees (100 slats, 9,434 triangles, no UV overlap).
- Sizes measured from the built meshes, against the references: every listed dimension within 3% (table).
- Triangles 4,446 to 14,056 (table), inside the 2k to 15k guide.
- One UV map ("UVMap") per object, the counter's three objects packed together; all UVs inside 0 to 1; every UV triangle rasterised at 2048 x 2048: 0 overlapping pixels on every prop. (The kit re-cuts and repacks any face that folds in the projection; in the final runs none did.)
- Every .blend object carries the colour attributes "ao", "edges" and "ao_edges"; each glb's COLOR_0 read back: red (ao) mean 0.37 to 0.79, green (edges) 0.19 to 0.69 (vertex means, weighted to small detail), blue 0, alpha 1. Flat faces read 0 edges (checked on the counter's panels and gate).
- glb sizes 238 KB to 620 KB, all under 1 MB; no images inside. Each glb re-imported into Blender: its objects (the counter's flap and gate still parented), one UV map, one colour set, sizes as built, base on z = 0.
- Previews looked at (Eevee, and a Workbench studio-light shading check per prop): no faceting, seams or shading faults seen; wear reads as small edge chips (the cabinet's enamel), grime in crevices and scuffed plastic on the chair's base. The chair's fabric, with no texture, reads smooth: its weave is the master material's job.

### Notes and what is not done

- **Counter height:** built 1.05 m as the brief says; the plan's counter box tops out at y 1.05 over a floor whose top is y 0.10, so in the plan it stands 0.95 m. One of the two wants settling (`--height` builds either).
- **Counter flap:** left and right as seen from the window. By default on the right, the stair strip's end, where the plan leaves the staff passage (x 4.19 to 5.2), closing against an end post: the 3.8 m run is body 3.12 + flap 0.60 + post 0.08. Run on to the stair wall (`--length 4.81`) the flap and gate would close that passage. The glb holds three objects: `counter`, and its children `counter_flap` (origin on the hinge knuckles' axis, front to back, at the top's surface) and `counter_gate` (origin on its vertical hinge axis), so both can be opened in the engine.
- **Heater depth:** 0.155 is the museum record's; here it is the wall to the knob's face, the cabinet 0.128 off the wall on 12 mm brackets. No mains flex: the dresser runs it to the room's socket.
- **Blind:** the slats are 0.5 mm thick, not 0.21: no eye sees the difference and the edge bake cannot tell faces closer than 0.35 mm apart. The ladders' rungs under the slats are not modelled (unseen at any distance), the strings are straight tapes, and the lift cords pass through the slats without routing holes.
- **Not modelled:** print on the cabinet's label cards (blank cards; a decal later), tears and cigarette burns in the vinyl (decals, the research's wear step), screws and fixings.
- **Preview render discipline:** one heater preview (10:47) was rendered while an UnrealEditor was open: my check printed "busy" but did not stop the chain. It was one Eevee still of a few seconds; every final preview waited for the GPU (checked every minute).
- **Git:** the set 1 commit staged the whole `tools/art-recipes/mickeys-props/` folder while set 2 was in progress, so early versions of these scripts may be in it; the files on disk now are the finished ones.

### Paths

- Scripts: `tools/art-recipes/mickeys-props/` (`chair.py`, `counter.py`, `bench.py`, `filing_cabinet.py`, `heater.py`, `blind.py`).
- Run: `blender.exe -b --factory-startup -P tools/art-recipes/mickeys-props/<script>.py [-- --no-render]`. The counter takes `--length --depth --height --flap-side left|right|none --flap-width --name`; the blind `--width --drop --tilt --name`; the bench `--length`. `--out-dir <folder>` writes everything to a test folder instead.
- glb: `F:\LedgerTools\game-inputs\production\assets\mickeys-props\<prop>.glb`; blend and a measured report: `F:\LedgerTools\mickeys-props\blend\<prop>.blend` and `<prop>.report.json`.
- Previews (800 px, Eevee) `F:\LedgerTools\mickeys-props\previews\<prop>.png`, shading checks (Workbench) in its `checks` folder; contact sheet `production/previews/mickeys-props-furniture-2026-10-06.jpg`.
