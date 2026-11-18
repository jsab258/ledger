# Review: car_plates.py and car_kit.py (17 November 2026)

Fresh independent reviewer, about 10 minutes, no web. Code not edited.

Reviewed: tools/lane/car_plates.py, tools/lane/test_car_plates.py, tools/lane/car_kit.py, tools/lane/test_car_kit.py (with tools/lane/car_loft.py read for its derived numbers). Sources: production/research/lane/HATCH-CLASS-AND-PLATES-2026-11-17.md section 3; production/research/lane/TRAFFIC-COST-2026-11-17.md section 5.

## Verdict: PASS WITH FIXES

The 29 tests pass (python3 -m unittest, 0.05 s). The V796 arithmetic is right, the forbidden letters are right, right-hand drive is right, and both modules are deterministic for a fixed seed or parameter set. The fixes below are a content-rule gap in the blocklist, an unbounded loop, a missing validation path, and two kit geometry faults that check() lets through.

## What was confirmed correct

- V796 Group 2: 79 high, 57 wide, stroke 14, gaps 11 and 33, margin 11 all match the note. "G888 ABC" = 7 x 57 + 5 x 11 + 33 = 487 mm, so the side margin is 16.5 mm on 520 and the vertical margin is 16 mm on 111. The layout is centred both ways, and the spacing test checks the 11/11/11/33/11/11 gaps.
- Year letters: only A to H. I, O, Q, U and Z are never the year letter (the note's correction adding Q is honoured). The serial letters leave out I, Q and Z. The format regex matches G123 ABC with 1 to 3 digits and no leading zero.
- Right-hand drive: driver_seat, driver_hands and camera_driver_head all sit at y = -0.36. With y + to the car's left, that puts the driver on the car's right. check() enforces the sign and a test asserts it.
- Determinism: random.Random(seed) for int and str seeds, and kit functions are pure. Same input, same output.
- Kit: four mirrored wheels with unique bones and hubs at (axle, +/- track/2, radius). There are 5 collision boxes (at most 6 allowed). The bonnet is hinged at the screen base, the tailgate at the roof back, and the doors at their front edge on z axes. All of this is plausible for a 1990 five-door hatch.
- A fuzz run of 400 random parameter sets (each value moved +/-30%) gave no crashes in derive() or check().

## Findings, each with its fix

1. **The blocklist misses slurs and drink words (content rule).** A 20,000-plate run (seed 42) produced these serials: WOG, FAG, PAK, WOP, POM (slurs); KEG, SOT, TOT (drink, which is against canon's no-alcohol rule); LSD, POT, DOP (drugs); UDA, UVF (Troubles paramilitaries, sharp in 1990 Britain); BNP, KGB, PRK, TWT, YOB. "BEER" is in the list but can never match, because serials are 3 letters.
   Fix: add at least WOG FAG FGT PAK WOP POM NIG KEG SOT TOT VAT LSD POT DOP UDA UVF IRA BNP KGB PRK TWT YOB to BLOCKLIST, and remove BEER. Also reject the prefix numbers 69 and 666 in is_valid_registration (E69 and B666 read as jokes). Add a test asserting that each of these new words is rejected.

2. **generate_registrations hangs when count is near or above what is possible.** The space is 8 x 999 x 23^3, about 97.2 million plates minus the blocklist. The attempt cap of count x 50 + 1000 never triggers in practice. count = 98,000,000 ran past a 100 s timeout. A count of 0 or less silently returns [].
   Fix: at the top, compute capacity = len(YEAR_WEIGHTS) x 999 x len(SERIAL_LETTERS)^3. Raise ValueError if count < 0 or count > capacity // 2, and add a test for it. Optionally reject seed=None, which is not deterministic.

3. **The output functions skip validation.** plate_data("G123 BUM") and plate_svg("G123 BUM") both succeed, bypassing the blocklist. "H1" and "G123  ABC" also lay out without error. plate_svg(reg, "side") raises KeyError, not ValueError.
   Fix: in layout() (or in plate_data and plate_svg), raise ValueError when is_valid_registration(reg) is false. Give plate_svg the same side check as plate_data. Add tests for both.

4. **The kit's tailgate panel ends before its own glass.** In the default car, the tailgate runs x 3.616 to 3.900 (L - BUMPER_DEPTH), but the rear screen, marked part_of tailgate, runs to hatch_base = 3.980. The rear bumper (3.90 to 4.08) also overlaps the lower tailgate. This happens because the hatch's back face is near vertical and x ranges alone cannot describe it. Whenever hatch_base_from_tail < BUMPER_DEPTH (default 0.10, round 3 0.14, both under 0.18), the panel chain is false.
   Fix: give every panel a z band as well as an x range. Set tailgate x to [roof_back, max(hatch_base, L - 0.02)] and z to [rear bumper top, top_z(roof_back)], with the rear bumper z running from sill_z to a bumper-top estimate. Add a check that each glass piece with part_of lies inside its panel's x and z, and a test with the default parameters.

5. **The driver seat and front door handle are not tied to the B-pillar.** Both use screen_base + 0.95. In the fuzz run, 10 parameter sets that pass check() put the front door handle on the rear door, and 4 put the hip point behind the B-pillar. Example: handle x 2.21 with b_line 2.13.
   Fix: derive the hip point as b_line - 0.10 and the handle as b_line - 0.12. Or keep the formulas and add checks: a_line < handle x < b_line, seat x < b_line, and |seat y| + 0.25 < width/2 - shoulder_in. Add a test with screen_base_x = 1.10 and wheelbase = 2.35.

6. **Some kit checks are tautological, so tests pass on wrong code.** Length coverage is always 100%, because nose, lower_body and tail chain end to end by construction. The mass check compares a constant against its own range. The centre-of-mass x is front_axle + 0.40 x wheelbase, so it is always forward of mid-wheelbase. Nothing tests the hub z (= wheel_radius), the spin axis, steers or driven on the front only, or the y and z lower bounds of the boxes.
   Fix: add assertions for hub z == radius, spin_axis == [0, 1, 0], steers == driven == (name starts with F), and box lower bounds of y >= -width/2 - margin and z >= keel_z - margin. Replace the coverage check with a volume or silhouette check (for example, the box union covers at least 85% of the loft's side area sampled at 20 stations).

7. **The kit checklist is not fully covered (TRAFFIC-COST section 5).** Items 10 and 11 are missing: there are no lamp-lens or other material slots (only glass has a material). Item 9 is partial: the rear doors of a five-door car have no handle sockets. Item 4 says "one box plus arch shapes", and the kit has five boxes and no arch shapes. That stays within the 6-shape cap, so it is acceptable as a recorded deviation.
   Fix: add a "materials" list (paint, glass, chrome, black_plastic, rubber, lens, plate, interior), give each lamp socket material "lens" and a glow value, add door_handle_rear_left and door_handle_rear_right when DOORS == 5, and note the box-only collision choice in DECISIONS.md.

8. **The plates miss part of a 1990 street (realism; list item, not a code bug).** Only prefix plates A to H are generated. In 1990 a large share of cars on the road were pre-August-1983 suffix plates (ABC 123X). H only began in August 1990 and canon fixes no month, so an early-1990 scene with H plates would be wrong.
   Fix: make the year letters a function of a game date argument (H only when the date is 1 August 1990 or later, marked unverified in the note). Put "suffix-era plates (ABC 123 + year letter)" on the lane list, with research first.

9. **Minor items.** The 25 mm narrow "1" is a guess, and the code says so. The yellow #f6c800 is a stand-in. The exhaust, horn and front plate heights are fixed numbers that do not scale. Either leave these as they are with their "est." notes, or derive the plate z from the bumper band once finding 4 lands.

## Could the code produce plates that look like real personalised plates?

Yes, in two ways. First, every output is a format-valid real British registration from a block DVLA really issued, so almost any plate here belonged to some real car. That is unavoidable for period-correct plates and is the normal practice in films and games. Because the area code is not modelled and nothing ties a plate to a person, I judge it **acceptable**.

Second, some outputs look like cherished or vanity plates, which makes it more likely that a real, identifiable owner exists or that a plate reads as a deliberate joke:

- low numbers: 428 of 20,000 (2.1%) were 1 to 20, e.g. F8 CYW and C3 KKU (DVLA commonly held low numbers back for sale; UNVERIFIED here);
- triple letters: 34 of 20,000, e.g. D678 HHH and G69 CCC;
- word-like serials (finding 1).

Fix: draw numbers from 21 to 999, weighted toward 3 digits. Reject serials with all three letters the same, and the word list from finding 1. With these in place, the remaining risk is acceptable.
