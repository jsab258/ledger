# Hatch class: three noses and three tails, drawn fresh (17 November 2026)

Review applied (17 Nov 2026): all 8 fixes from production/lane/reviews/REVIEW-SIGNS-NOSETAIL-RONTONIGHT-2026-11-17.md section 2 (T1 tailgate shut line, T2 upright wording, full parameter table, heights as offsets, lit-edge measures, N2 grille height, Schedules 11 and 4 to read before modelling, photo sheet before N1 and N3 with N1's look-alike risk stated).

Lane helper for n16-9. Machine-free: nothing modelled or rendered. Inputs read: P9-BLIND-BRIEF.md, P9-OUTLINE-ROUNDS-2026-11-17.md, research/lane/HATCH-CLASS-AND-PLATES-2026-11-17.md, research/lane/CAR-METHOD-LANDSCAPE-2026-11-17.md, tools/lane/car_loft.py (HatchParams, ROUND3_PROPOSAL) and tools/lane/car_kit.py (BUMPER_DEPTH 0.18, FRONT_BUMPER_RISE 0.22, REAR_BUMPER_RISE 0.25, the lamp and plate sockets). Worked example body: HatchParams(**ROUND3_PROPOSAL), so nose_top_z 0.72 m, tail_top_z 0.84 m, sill_z 0.30 m, belt 0.875 m (0.625 x 1.40), roof edge about 1.38 m, width 1.66 m (half 0.83), nose width about 1.43 m (nose_taper 0.86), tail width about 1.53 m (tail_taper 0.92). ROUND3_PROPOSAL has not yet been through a blind round, so every height below is given as an offset from a body number (nose_top_z, tail_top_z or sill_z), as car_kit does; the metre figure in brackets is only this example.

Every number not from a page read is marked est. Design picks (shapes, sizes of lamps and grilles) are the lane's, so they are est. by nature; only the legal limits below are sourced.

## 1. The 1990 rules the modules must meet

| Rule | Value | Source (read 17 Nov 2026) |
|---|---|---|
| Indicators, cars first used on or after 1 April 1986 | one front, one rear and one side repeater each side; amber | Road Vehicles Lighting Regulations 1989, Schedule 7, as made: https://www.legislation.gov.uk/uksi/1989/1796/schedule/7/made |
| Indicator height | at least 350 mm, at most 1,500 mm | same |
| Indicator from the side of the car | at most 400 mm | same |
| Indicators apart (left to right) | at least 500 mm (400 mm if the car is under 1,400 mm wide) | same |
| Side repeater | within 2,600 mm of the front | same |
| Gap front indicator to dipped headlamp | only for cars first used from 1 April 1991 (so a 1990 car may have the indicator touching the headlamp) | same |
| Rear plate lamp | white, enough to light the plate; number and place free | Schedule 15, as made: https://www.legislation.gov.uk/uksi/1989/1796/schedule/15/made |
| Plate sizes | 520 x 111 mm standard; rear also 533 x 152 or 285 x 203 | class research file, section 3 |
| Plate colours | white front, yellow rear, reflective | class research file, section 3 |
| Front plate vertical, or as near vertical as practicable | 2001 rule as quoted by carreg.co.uk: https://carreg.co.uk/carreg-news/how-where-number-plates-should-be-legally-displayed ; the 1990 wording UNVERIFIED | |
| Rear fog lamp: one, on the offside (right) or centre | UNVERIFIED. Read Schedule 11 of the same regulations before fog_rear_y is modelled, not after | |
| Headlamp height limits | UNVERIFIED. Read Schedule 4 before lamp_z is modelled, not after | |

How the indicator checks are measured here: the 400 mm is taken from the outer edge of the lit area to the car's widest point (half width 0.83 m), the 500 mm between the inner edges of the two lit areas, and the 350 mm to the lowest edge of the lit area. These are the usual readings of such rules; the definitions part of the regulations was not read (UNVERIFIED), and the margins below are wide enough that a stricter reading still passes.

Period habits used below (est., the lane's reading of the class, not sourced): bumpers of 1985 to 1990 hatches were mostly black or grey plastic, often with a rubbing strip; painted (body-colour) bumpers came on upper trims from about 1988; lamps were rectangular or near-rectangular, flush or near flush; front indicators sat in the bumper or wrapped round the corner beside the headlamp; the front plate sat on the bumper face, the rear plate on the tailgate between the lamps or in a recess in the rear bumper.

## 2. New loft parameters (all modules)

The loft has no nose or tail detail today. These go in a new dataclass, NoseTail, beside HatchParams (not inside it, so the P9 silhouette stays fixed); the Blender side cuts lamp and grille recesses from them into the panels named in each module. None of them changes the station topology. A module leaves a parameter at 0 or "none" when it does not use it.

| Parameter | Meaning | Unit |
|---|---|---|
| nose_face_rake_deg | lean of the front panel back from vertical | deg |
| lamp_w | one headlamp's width | m |
| lamp_h_inner, lamp_h_outer | headlamp height at its inner and outer ends (equal for a rectangle; N3's trapezium differs) | m |
| lamp_corner_r | corner radius of the headlamp | m |
| lamp_z_off | headlamp centre below nose_top_z (car_kit uses 0.10) | m |
| lamp_inner_y | half gap between the two headlamps' inner edges | m |
| grille_h, grille_slats | grille opening height; horizontal slats (0 = plain slot) | m, count |
| grille_material | paint, black_plastic | slot |
| bumper_material | black_plastic, paint, paint_with_strip | slot |
| bumper_proud | how far the bumper face stands out from the panel above | m |
| bumper_wrap | how far the bumper runs back along the side | m |
| strip_h | rubbing strip height on the bumper (0 = none) | m |
| ind_front_mode | corner (wrap beside lamp), bumper (in the bumper), below (under the lamp) | enum |
| ind_front_w, ind_front_h | front indicator size | m |
| ind_front_y | front indicator centre from the car's centreline | m |
| ind_front_z_off | front indicator centre above sill_z (corner mode: same as the lamp) | m |
| plate_front_z_off | front plate centre above sill_z | m |
| tailgate_cut_z_off | tailgate's lower shut line above sill_z (car_kit: REAR_BUMPER_RISE, 0.25) | m |
| tailgate_half_w_low | tailgate half width below the rear screen (the rear quarters fill the rest) | m |
| tail_lamp_mode | band (horizontal, beside the tailgate), corner_L (L up the rear quarter), panel (lamps joined by a black panel across the tailgate) | enum |
| tail_lamp_w, tail_lamp_h | one cluster's horizontal part | m |
| tail_lamp_z_off | cluster centre below tail_top_z | m |
| tail_lamp_wrap | how far the cluster wraps round the side | m |
| tail_lamp_panel | panel the cluster is cut into: rear_quarter or tailgate | enum |
| tail_upright_h, tail_upright_w | T2's upright part: rise above the horizontal part's top, and width | m |
| tail_panel_h, tail_panel_ribs | T3's joining panel: height, rib count | m, count |
| plate_rear_mount | tailgate or bumper | enum |
| plate_rear_z_off | rear plate centre: below tail_top_z (tailgate mount) or above sill_z (bumper mount) | m |
| plate_lamps, plate_lamp_place | rear plate lamps: count; above_plate or recess_top | count, enum |
| fog_rear_y | rear fog lamp position, negative = offside (car_kit's right is y negative) | m |

## 3. Noses

All three noses are cut into car_kit's front_panel (above the bumper) and front_bumper.

### N1, "Bar nose" (the default, the plainest)

Brief: two wide rectangular headlamps with small corner radii, joined by a body-colour bar with one narrow black slot under it; no chrome. The amber indicator wraps round each corner beside the lamp. A deep black plastic bumper with a grey rubbing strip; the front plate in the middle of the bumper face; a small air slot below the plate. The face leans back a little. It reads as the cheaper trim of a 1986 to 1989 hatch.

| Parameter | Value | Unit |
|---|---|---|
| nose_face_rake_deg | 8 est. | deg |
| lamp_w | 0.38 est. | m |
| lamp_h_inner, lamp_h_outer | 0.13, 0.13 est. | m |
| lamp_corner_r | 0.015 est. | m |
| lamp_z_off | 0.10 (car_kit; example 0.62) | m |
| lamp_inner_y | 0.17 est. | m |
| grille_h, grille_slats | 0.05, 0 (a slot under the bar) est. | m, count |
| grille_material | black_plastic | slot |
| bumper_material | black_plastic | slot |
| bumper_proud | 0.05 est. | m |
| bumper_wrap | 0.25 est. | m |
| strip_h | 0.04 est. | m |
| ind_front_mode | corner | enum |
| ind_front_w, ind_front_h | 0.09, 0.13 est. | m |
| ind_front_y | 0.595 (0.17 + 0.38 + 0.045) est. | m |
| plate_front_z_off | 0.11 (bumper middle, 0.22 / 2 as car_kit; example 0.41) | m |

Width check (est.): 2 x 0.09 indicator + 2 x 0.38 lamp + 0.34 bar = 1.28 m against a nose about 1.43 m wide. Indicator lit area runs from 0.55 to 0.64 m from the centre, and its wrap carries the outer edge round to about 0.71 m: outer edge 0.12 to 0.19 m from the side (under 0.40), inner edges 1.10 m apart (over 0.50), lowest edge about 0.555 m in the example (over 0.35): legal.

Must not resemble: Opel Kadett E / Vauxhall Astra Mk2 and Ford Escort Mk4. Stated plainly: N1 is the highest look-alike risk of the six modules and it is the first sample. Wide rectangular lamps, a body-colour bar with one slot and wrap-round corner indicators is close to what the reviewer remembers of the Kadett E / Astra Mk2 nose, and this brief's first draft described that nose as having a "slatted grille", which may be wrong. The intended escapes (solid bar, only 8 degrees of lean, no round lamps so not the VW Golf II, no slanted inner lamp edges so not the Peugeot 309) are from memory and unchecked. Before N1 is modelled, the photo sheet in section 6 is made and these lines are redone against it; if the sheet shows the Kadett E / Astra Mk2 nose matches N1, N1 changes before modelling (first candidate: the indicator moves into the bumper and the bar becomes a black panel), and the change is recorded.

P9 second run: a viewer should say "a plain European family hatch, mid to late 1980s, could be Vauxhall, Ford or Opel" with no name above 50. If a round names a Vauxhall or Opel first, change only the bar to a black panel with one slat.

### N2, "Square-lamp nose with a slatted grille" (older, 1984 to 1987 look)

Brief: two near-square headlamps (slightly wider than tall), each with a separate small amber indicator in the bumper below and a little outboard of it. Between the lamps a black plastic grille of four thin horizontal slats, the same height as the lamps (0.17 m est.). A slim black bumper close to the body with no strip; the plate on the bumper face. Face nearly upright. It reads as an older or base model still on the road in 1990.

| Parameter | Value | Unit |
|---|---|---|
| nose_face_rake_deg | 3 est. | deg |
| lamp_w | 0.24 est. | m |
| lamp_h_inner, lamp_h_outer | 0.17, 0.17 est. | m |
| lamp_corner_r | 0.01 est. | m |
| lamp_z_off | 0.10 (car_kit; example 0.62) | m |
| lamp_inner_y | 0.30 est. | m |
| grille_h, grille_slats | 0.17 (equal to the lamps), 4 est. | m, count |
| grille_material | black_plastic | slot |
| bumper_material | black_plastic | slot |
| bumper_proud | 0.03 est. | m |
| bumper_wrap | 0.15 est. | m |
| strip_h | 0 | m |
| ind_front_mode | bumper | enum |
| ind_front_w, ind_front_h | 0.12, 0.05 est. | m |
| ind_front_y | 0.50 est. | m |
| ind_front_z_off | 0.17 est. (example 0.47) | m |
| plate_front_z_off | 0.10 est. (example 0.40) | m |

Indicator lit area 0.44 to 0.56 m from the centre: outer edge 0.27 m from the side (under 0.40), inner edges 0.88 m apart (over 0.50), lowest edge 0.445 m in the example (over 0.35): legal.

Must not resemble: Austin Maestro (square lamps with slats running across lamps and grille as one band), Fiat Uno and Fiat Tipo (small lamps either side of a slim slotted grille), Nissan Sunny N13. Stays clear: the grille is a separate box with a body-colour gap of 0.04 m est. from each lamp, slats stop at the box, lamps taller than the Tipo's slim slots. Not the VW Golf II: square, not round, lamps. All from memory; checked on the photo sheet if N2 is built.

P9 second run: "a European hatch of the early to mid 1980s, maybe British Leyland, Fiat or Ford" with the years range starting about 1982; that still overlaps 1985 to 1991. If the range misses 1985 (for example "1978 to 1984"), the nose is too old: change only the lamps to N1's wide shape.

### N3, "Smooth nose" (newest, 1989 to 1991 look, upper trim)

Brief: lamps shaped as a low trapezium, taller at the outer end, tapering inward, with a thin step at the top edge. No grille above the bumper but one shallow black slot between the lamps, 0.03 m high; the air comes through a wide intake in the bumper. A painted (body-colour) bumper with a thin black strip, wrapping well round the sides; the indicator a thin amber strip below each lamp; the front plate set into a shallow flat on the bumper. The face leans back more. It reads as the newest car on the street.

| Parameter | Value | Unit |
|---|---|---|
| nose_face_rake_deg | 14 est. | deg |
| lamp_w | 0.40 est. | m |
| lamp_h_inner, lamp_h_outer | 0.11, 0.14 est. | m |
| lamp_corner_r | 0.02 est. | m |
| lamp_z_off | 0.09 est. (example 0.63) | m |
| lamp_inner_y | 0.20 est. | m |
| grille_h, grille_slats | 0.03, 0 est. | m, count |
| grille_material | black_plastic | slot |
| bumper_material | paint_with_strip | slot |
| bumper_proud | 0.04 est. | m |
| bumper_wrap | 0.35 est. | m |
| strip_h | 0.025 est. | m |
| ind_front_mode | below | enum |
| ind_front_w, ind_front_h | 0.30, 0.03 est. | m |
| ind_front_y | 0.53 est. | m |
| ind_front_z_off | 0.24 est. (example 0.54, just under the lamp) | m |
| plate_front_z_off | 0.14 est. (example 0.44) | m |

Indicator lit area 0.38 to 0.68 m from the centre: outer edge 0.15 m from the side (under 0.40), inner edges 0.76 m apart (over 0.50), lowest edge 0.525 m in the example (over 0.35): legal.

Must not resemble: Ford Sierra and Escort (this brief's claim that they had a grille-less "bottom breather" nose is from memory; true of the Sierra as the lane remembers it, unconfirmed for the Escort), Renault 19 (slim lamps with a thin slatted grille between), Rover 214 R8 (small chromed grille in the middle), Fiat Tipo. Stays clear: keeps one slim black slot so it is not blank, has no grille shape or chrome in the middle, and the trapezium lamps taper the other way from a Sierra's. Must also stay clear of any 1990s Japanese look: no rounded oval lamps. Like N1, these lines are redone against the photo sheet before N3 is modelled.

P9 second run: "a late-1980s European hatch, newer design, possibly Ford, Renault or Rover" with years about 1988 to 1994. If a round reads it as Japanese, or the range starts after 1991, change only the bumper back to black plastic.

## 4. Tails

The tailgate's lower shut line sits at the rear bumper top in all three tails (tailgate_cut_z_off 0.25 = car_kit's REAR_BUMPER_RISE; example 0.55 m), so there is no separate rear panel under the hatch. Below the rear screen the tailgate is narrower than the body (tailgate_half_w_low), and the rear quarters wrap round to fill the corners beside it. Each tail names the panel its parts are cut into.

### T1, "Low band" (the default)

Brief: two horizontal lamp clusters cut into the rear quarters' corners, beside the tailgate at plate height, each in three side-by-side parts: amber indicator outer, red tail and brake in the middle, white reverse inner. Smooth lenses with one thin horizontal bar. The rear plate on the tailgate between the clusters, lit by two small white lamps above it. A black plastic bumper with a strip; the rear fog lamp in the bumper on the offside.

| Parameter | Value | Unit |
|---|---|---|
| tailgate_cut_z_off | 0.25 (car_kit; example 0.55) | m |
| tailgate_half_w_low | 0.35 est. | m |
| tail_lamp_mode | band | enum |
| tail_lamp_panel | rear_quarter | enum |
| tail_lamp_w, tail_lamp_h | 0.40, 0.14 est. | m |
| tail_lamp_z_off | 0.12 (car_kit; example 0.72) | m |
| tail_lamp_wrap | 0.06 est. | m |
| plate_rear_mount | tailgate | enum |
| plate_rear_z_off | 0.12 below tail_top_z est. (example 0.72, between the clusters) | m |
| plate_lamps, plate_lamp_place | 2, above_plate est. | count, enum |
| bumper_material | black_plastic | slot |
| strip_h | 0.04 est. | m |
| fog_rear_y | -0.35 est. (offside; Schedule 11 first) | m |

Recheck with the shut line: the tailgate below the screen runs from 0.55 m (example) to tail_top_z, and the clusters (0.65 to 0.79 m in the example) sit beside it, from 0.36 to 0.76 m from the centre, just outside its 0.35 m half width; the 520 mm plate (half 0.26) on the tailgate leaves 0.09 m each side to the shut lines. car_kit puts plate_rear at tail_top_z minus 0.30 (0.54 m, on the bumper); this module moves it up to tail_top_z minus 0.12 so it sits on the tailgate. Indicator part 0.12 m est. wide at the outer end: lit area 0.64 to 0.76 m from the centre, wrap carrying it a little further, so the outer edge is about 0.07 m from the side (under 0.40), inner edges 1.28 m apart (over 0.50), lowest edge 0.65 m in the example (over 0.35): legal. The tailgate needs a lower part narrower than its glass; that is a panel split change in car_kit's panels() (rear_quarter and tailgate x and y bands), not a loft change.

Must not resemble: Ford Escort Mk3 and Mk4 (ribbed lenses either side of the plate), Vauxhall Astra Mk2 (clusters wrapping far round the corner), VW Golf II (smaller clusters, as the lane remembers them, at the body corners beside the tailgate). Stays clear: smooth lenses (no ribs), short wrap (0.06 m est.), and clusters wide (0.40 m) and long across the back with the plate tight between them. The clusters are now beside the tailgate as on many hatches, so the earlier "in the body, not the tailgate" escape from the Golf II no longer applies; the escape rests on size and lens alone, and it is checked on the photo sheet.

P9 second run: "a European hatch, 1984 to 1991, like an Escort or Astra or Kadett" spread across several candidates, none above 50.

### T2, "Corner L" (taller, more modern)

Brief: each cluster an L, cut into the rear quarter: a horizontal part beside the tailgate and a short upright part climbing the foot of the rear pillar, stopping well below the window's top. The upright rises above tail_top_z, so it must stay on the rear quarter, outboard of the rear screen's side edge, never on the glass or the tailgate. The rear plate in a recess in a deep painted or black bumper (both work), with the plate lamp in the recess top. The tailgate below the glass is a plain panel with a small black handle strip. Rear fog in the bumper, offside.

| Parameter | Value | Unit |
|---|---|---|
| tailgate_cut_z_off | 0.25 (car_kit; example 0.55) | m |
| tailgate_half_w_low | 0.40 est. | m |
| tail_lamp_mode | corner_L | enum |
| tail_lamp_panel | rear_quarter | enum |
| tail_lamp_w, tail_lamp_h | 0.30, 0.12 est. | m |
| tail_lamp_z_off | 0.14 (example 0.70, horizontal part's centre) | m |
| tail_upright_h, tail_upright_w | 0.18, 0.08 est. (top at tail_top_z + 0.10; example 0.94) | m |
| tail_lamp_wrap | 0.10 est. | m |
| plate_rear_mount | bumper | enum |
| plate_rear_z_off | 0.16 above sill_z est. (example 0.46) | m |
| plate_lamps, plate_lamp_place | 1, recess_top est. | count, enum |
| bumper_material | black_plastic or paint_with_strip | slot |
| strip_h | 0.03 est. | m |
| fog_rear_y | -0.40 est. (Schedule 11 first) | m |

Bumper height check: car_kit's rear bumper runs 0.30 to 0.55 m in the example (REAR_BUMPER_RISE 0.25 est.); a 111 mm plate centred at sill_z + 0.16 fits with 0.03 m above and 0.10 m below est. Indicator at the outer end of the horizontal part, lit area 0.66 to 0.76 m est.: outer edge about 0.07 m from the side, inner edges 1.32 m apart, lowest edge 0.64 m: legal.

Must not resemble: Fiat Tipo (very tall slim lamps up the full pillar), Peugeot 205 and 309, Renault 19 (wide wrapping clusters). Stays clear: the upright's top at tail_top_z + 0.10 (0.94 m in the example) is only about an eighth of the way from the belt (0.875 m) to the roof edge (about 1.38 m), far from the roof; the horizontal part is longer than the upright.

P9 second run: "a European hatch, late 1980s, maybe Fiat, Peugeot or Renault" under 50. If a round names the Tipo, change only tail_upright_h down to 0.08 est.

### T3, "Black panel" (upper trim, 1988 to 1991 look)

Brief: two compact clusters in the rear quarters, joined across the tailgate by a black ribbed plastic panel cut into the tailgate at the same height (not a red lens, so it does not light), the rear plate below it in the bumper recess. Painted bumper with a thin strip. It reads as the upmarket trim of the range.

| Parameter | Value | Unit |
|---|---|---|
| tailgate_cut_z_off | 0.25 (car_kit; example 0.55) | m |
| tailgate_half_w_low | 0.46 est. | m |
| tail_lamp_mode | panel | enum |
| tail_lamp_panel | rear_quarter (the joining panel: tailgate) | enum |
| tail_lamp_w, tail_lamp_h | 0.30, 0.13 est. | m |
| tail_lamp_z_off | 0.11 est. (example 0.73) | m |
| tail_lamp_wrap | 0.05 est. | m |
| tail_panel_h, tail_panel_ribs | 0.12, 5 est. (top 0.01 below the clusters' top) | m, count |
| plate_rear_mount | bumper | enum |
| plate_rear_z_off | 0.16 above sill_z est. (example 0.46) | m |
| plate_lamps, plate_lamp_place | 1, recess_top est. | count, enum |
| bumper_material | paint_with_strip | slot |
| strip_h | 0.025 est. | m |
| fog_rear_y | -0.40 est. (Schedule 11 first) | m |

Indicator at the cluster's outer end, lit area 0.65 to 0.76 m est.: outer edge about 0.07 m from the side, inner edges 1.30 m apart, lowest edge about 0.67 m: legal.

Must not resemble: Peugeot 309 GTI and 405 (black or red band joining the lamps across the boot), Audi 80 B3 (full-width red band, a saloon anyway), Rover 200 R8. Stays clear: the panel is matt black and ribbed, its top 0.01 m est. below the clusters' top, and the clusters stay separate parts; no red across the car.

P9 second run: "a European hatch of the late 1980s, sporty or upper trim, possibly French or German" under 50. If a Peugeot is named first, change only the panel to body colour.

## 5. Mix and match

Marks: ++ pairs well (same period and trim), + fine, x do not ship (period clash: a 1984 face on a 1990 back reads as wrong).

| | T1 Low band | T2 Corner L | T3 Black panel |
|---|---|---|---|
| N1 Bar nose | ++ base model, first sample | ++ mid trim | + |
| N2 Square-lamp nose | ++ older base model | + | x (old face, newest back) |
| N3 Smooth nose | + | ++ upper trim | ++ top trim |

So eight pairs ship; N2 with T3 is ruled out by period sense, not law. Bumper colour follows the pair's trim: black with N1 and N2, painted with N3 and T3; T2 takes either.

## 6. Order and testing

1. Before modelling: read Schedules 11 (rear fog) and 4 (headlamp heights) of the 1989 lighting regulations and fix fog_rear_y and lamp_z_off against them.
2. Before modelling N1 and N3: a photo sheet of the named cars (Opel Kadett E / Vauxhall Astra Mk2, Ford Escort Mk3 to Mk5, Ford Sierra, VW Golf II, Peugeot 309, Renault 19, Rover 214 R8, Fiat Tipo), front and rear, from a source the allowlist permits for reference, put beside this brief; redo every "must not resemble" and "stays clear" line against it, and change N1 first if it matches the Kadett E / Astra Mk2. The photos are reference only, never traced or measured into the body.
3. Nothing is multiplied before he approves one complete sample (CLAUDE.md): build N1 + T1 first, run P9 again on its renders (the brief's note: modules get their own run at the material pass), then one more pair per round.
4. Each pair's P9 run uses a fresh helper and the same brief word for word; after a fail change only the feature named in answer 5, as each module's line above says.
5. The bigger risk is the sum: a viewer may name a real car from a nose and tail that each pass alone. Run every pair that ships, not only each module once (est. 8 runs; two rounds at most each per RULINGS 3 Nov).

## Not reached

- Lighting Regulations Schedule 11 (rear fog lamp) and Schedule 4 (headlamp heights), and the regulations' definitions of how the indicator distances are measured: not read; to be read before modelling (section 6, step 1).
- The 1990 wording on front plate position (the page read quotes the 2001 regulations).
- No pictures of any real car were looked at in this run; the "must not resemble" lines rest on memory until the photo sheet (section 6, step 2), and P9 stays the final check.
