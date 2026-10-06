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

