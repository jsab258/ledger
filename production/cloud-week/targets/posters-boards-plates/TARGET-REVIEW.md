FAIL

# Posters, boards and plates: fresh target review (cloud week 42)

Reviewer: a fresh target reviewer, 9 October 2026. I did not write this target and will not build it. Read: REVIEW-BRIEF.md, BRIEF.md, SCENE-SLOTS.md, canon.md, RULINGS.md, TARGET.md, target.json (all 76 items and all 308 approved strings, word by word), the fascia target's target.json, the asset-plan note 4, PERIOD-PRINT-AND-FONTS, the street-clutter and street-lines notes, the brand bible, hook-cast.json, vignette-scene.json, atlas-01, the Hook sheet and the 4 and 8 October street frames. Ran self_check.py and target_drawing.py on a scratch copy (outputs in the session scratchpad, posters-review/, nothing in git). Self-check reproduces: 215 checks, 215 passed, 0 failed, 13 reported.

Network: this cloud reaches polyhaven.com and raw.githubusercontent.com only. Wikimedia, Geograph, Flickr, archive.org, Wikipedia, Picture Sheffield and Hackney all refused me (tested today). So, like the writer, I reached no period photograph of a plate, a letting board, a pasted wall or a notice; the photographs-win test cannot be run for this family, and every period judgement below is mine against the project's own notes. The one photograph the target used (Poly Haven Urban Street 01) I opened at its source: Andreas Mischok, CC0, taken 18 August 2019, London; it informs nothing that will be built (the target rightly refuses its proportions).

13 faults, worst first. Each ends with the exact amendment.

## Faults

**1. The checks cannot see a wrong word, date or price in the pixels.** The word, forbidden-word and date checks (`.words`, `G.words.approved`, `G.forbidden`, `G.dates`) read the builder's own manifest, so a renderer that draws something other than what it lists passes them. The only pixel check of the lettering is `.mask` (font re-rendered, dilated 1 mm in print, 2.5 mm for hand), and I rendered wrong items through the target's own reader (`self_check.read_score`, `pos_ok`, `block_min_f`). The changed block passed both `.mask` and `.pos` in every case below:
- P01 THURSDAY 25 to 26 OCTOBER, F 0.997 (needs 0.90);
- W01 FRIDAY 2 to 9 NOVEMBER, F 0.991;
- C01a FRIDAY 12 to 13 OCTOBER, F 1.00;
- F01 LAST CROSSING 11.00 to 11.30, F 0.994;
- T03 £2.80 to £3.80, F 0.993;
- D01 TEA to ALE AND SANDWICHES, F 0.962;
- J01 Teas to Beer and cakes, F 0.942;
- K01 CLOSED FOR LUNCH to CLOSED FOR BINGO, F 0.973 (0.949 with the target's own hand jitter);
- K07a TEA BAGS to GIN BAGS, F 1.00;
- SA11 "Apply within." to "Pub, Fridays.", F 1.00;
- K09a £2.70 to £7.20, F 0.982.

Only changes of length or shape were caught: SATURDAY to SUNDAY, QUAY STREET misspelt, BAR OPEN 7. A mirrored hand card passed too: K01 mirrored failed 0 of 2 blocks. The three art slots (G01, T01, T02) have no check at all, though an image model drawing a pier or a phone box will add people, lettering, a crown or AMUSEMENTS signs. There is a further trap the other way. The variants list "skew -1.2 to +1.2 degrees", and a TRUE render skewed 1.2 degrees fails 6 of P01's 10 blocks and 8 of J01's 10.

Amendment:
- (a) Every 2D render writes a glyph manifest: for each block, each character as drawn, with its font, size, origin, baseline offset, rotation and scale, the hand jitter included.
- (b) Add a check `ITEM.glyphs`, reads pixels. Each glyph is re-rendered from the manifest and must score F at least 0.85 at 0.5 mm dilation in its own box. It must also out-score every other glyph of its font in A-Z a-z 0-9 £ . , ' - & ·, and its own mirror image, by at least 0.05. The manifest's characters must equal the approved string.
- (c) Add `ART.eye`, reads eye: a fresh reviewer looks at each art picture at 1:1 and passes it only with no person, hand, face, lettering, numeral, crown, kiosk mark, bottle, glass or arcade sign.
- (d) State that every texture is square-on: skew and rotation live only in the placement's `rot_deg`.
- (e) Add `PLACE.built`: each placed decal's centre lies within 20 mm of the target's u and z, its rotation within 0.3 degrees, and it is read the right way round in a render of the placed street.

**2. Unminted placeholder names are the street's default dressing.** The 3 October ruling says placeholders are never on his page, and whole street frames go on his page. The placements use them anyway:
- L01 with ARMITAGE & STOBBS at 52 mm capitals on the empty unit's fascia (SF5);
- L03 on the first floor (SF6);
- the film titles, studio and credits of T01, T02 and T03;
- the four ring names (W01, on SF1 and pier W1.0) and THE DRILL HALL (W01, B01);
- THE SANDERLING TRIO (D01, on SF1 and pier W2.1);
- WHITEWELL (G01) and QUAYSIDE (G02);
- MERIDIAN AGAINST THE POLL TAX at 21 to 24 mm on every poll-tax bill.

From across the street these are readable: the agent's name projects to about 8 px a capital at 8 m. `G.proposed` only checks that the names stay on their own items. The imprints (2.4 mm) are illegible and can stay.

Amendment:
- Add `held_until_minted: true` to every placement whose item carries a proposed name in a block of cap 10 mm or more.
- Add `G.page.placeholders`: it fails while any such placement is built and its name has no DECISIONS.md minting line.
- Place L02 on SF5. Replace L03 on SF6 with a no-agent flat board (L03n: TO LET / SELF-CONTAINED FLAT / ENQUIRIES 960 335, the L04 layout at 600 x 400).
- The other named bills are built only after the town mints their names.

**3. The WEIGHHOUSE LANE plate names the yard entrance, against the adopted atlas and the scene.** S02d is placed on the x = 24.0 flank, the "side opening at x 21 to 24". vignette-scene.json (the west_north note) calls those 3.0 m "the YARD ENTRANCE", with the dropped kerb at x 22.5. Atlas-01, which is the town's map (ruling 5 October), records the same opening as `yard_gap_x [21, 24]`. It runs Weighhouse Lane from [240,590] through [485,600] to [760,635], meeting Quay Street at the route's inland end, about 200 m beyond the built 48 m (atlas north 350 to 398). Naming the gap is a map fact, and the town has already settled it.

Amendment:
- Delete the S02d placement and the "PROPOSED because canon does not name the opening" lines in sections 7 and 13. S02 stays a kit plate, like S03.
- C03 may keep DIVERSION VIA WEIGHHOUSE LANE: the atlas's Weighhouse Lane and Tannery Row do make the way round.

**4. The paste plan is far denser than the asset plan and covers the gable the Hook sheet shows bare.**
- The asset plan's A5 table, which binds this family by the 3 October ruling, gives Quay Street 8 fly-posters and 4 poll-tax bills. Its proof is "one wall in view ... three bills from three templates".
- The target places 23 pasted bills, 8 of them poll-tax bills, plus 7 stickers.
- In the hook camera (cam_hook: x -3.0, z -1.6, yaw 20.4, vertical field 46 degrees, 2560 x 1440), the quay gable shows from its front corner to about u 2.7 m, at screen x 2190 to 2560. That strip would carry about nine bills in three layers, plus the plate.
- The Hook sheet's gable, which governs composition, is bare old brick. It has a black downpipe about 0.2 to 0.4 m from the front corner (my reading off the sheet), a render patch high up and a dark damp foot. The target never mentions the downpipe, and its zone starts at u 0.15.
- The west terrace's six house fronts each get a bill. The 1990 look of the poll tax on a residential terrace was the window bill inside a front window, not paper pasted on the house front.

Amendment:
- SF1 gets one layer of three bills, the plan's proof: P01 at u 0.70, W01 at u 1.30 and T02 at u 1.90, all with bottoms at z 1.00. Add the downpipe to SF1 as a 75 mm round cast-iron pipe at u 0.30, full height, with paper kept 150 mm clear of it. Keep the plate at u 1.0. Nothing more on SF1 until he has approved the sample in the assembled game.
- SF2 gets one layer: M01, P03, P02 and J01 as in the 4 October proof, plus C02, with no duplicate P01.
- Keep only the scene's own slot on the piers (W1.0, x 11.4).
- Move P02 off pier W1.1 into the plain row's bay-1 window at x 12.3, as an A3 window bill: P02 scaled by 297/508, taped inside the glass, top at 1.90 m.
- Totals: 8 fly-posters and 4 poll-tax bills, as the plan says.

**5. Two cloud-week targets give two different letting boards, and C02 uses the wrong address.**
- The fascia target's `small_panels.letting_board` is 900 x 450, TO LET only, Libre Franklin 800, cap 130, vinyl red, with "no agent and no number". This target's L01 and L02 are 1200 x 450 in Jost, with an agent band and a number. Only the centre (2705, 275) agrees.
- The fascia target gives the empty unit `street_number 7`. C02 says "Change of use of the ground floor, 21 to 27 Quay Street": the street x in metres used as house numbers.

Amendment:
- L02 takes the fascia target's board exactly (900 x 450, TO LET, Libre Franklin 800 cap 130, vinyl red, the 960 335 line dropped or added to both targets).
- If the 1200 mm agent board is wanted, change the fascia target's entry in the same batch with one DECISIONS line, and make `G.letting.mount` compare size and font with the fascia target.
- C02 line 1 becomes "Change of use of the ground floor, 7 Quay Street,".

**6. Two proposed names collide with real ones.**
- TIGER JIM LARKIN carries the name of James "Big Jim" Larkin, the dock-labour union leader: a real person, and a pointed one in a dock town whose cast includes a docker.
- THE SEA WOLF is Jack London's novel and its films (1941). It is also within a letter of the British film The Sea Wolves (1980).

Amendment:
- Rename them, for the town to mint. I propose BIG TED HOLROYD and THE HARPOONER; I could not check these against lists, because the network is closed.
- Add LARKIN and SEA WOLF to `forbidden_patterns.real_marks`.

**7. Period wording and process that read as the wrong decade or the wrong country.** Canon: "Any 1950s or 1970s framing is wrong."
- D01 "NEW VOGUE" is the Australian name for sequence dancing; a British chapel hall in 1990 would say OLD TIME AND SEQUENCE DANCING. Replace the NEW VOGUE block with "SEQUENCE" (same font, size and place).
- W01 "ALL-IN" is the 1930s name; 1980s British bills read WRESTLING. Replace the block with "PROFESSIONAL" (Oswald 700, re-fitted to the 428 mm measure).
- T01 and T03 split the week Sunday to Wednesday and Thursday to Saturday, the 1950s provincial pattern. The brand bible says the Tivoli's programme is "changed on Thursdays". Change the dates: T01 runs from THURSDAY 18 OCTOBER and T02 from THURSDAY 25 OCTOBER. T03 reads: FROM THURSDAY 18 OCTOBER / THE FOURTH WITNESS / FROM THURSDAY 25 OCTOBER / A WEEK AT GULLWING. On SF1, T02 becomes the top layer (class A) and T01 goes under it (class B).
- T01 and T02 print the cinema's name and dates inside the four-colour litho. A distributor's quad carried no venue; the venue and dates came on a pasted strip. Make THE TIVOLI and FROM ... a separate strip, 1016 x 90 mm, letterpress black on white stock, with its own age class, set 2 to 6 mm off square on the quad's top band, and keep the litho's top band blank.
- J01 (jumble sale) and D01 (dance) are crown and double-crown letterpress fly-posters. Note 4 says a 1990 jumble-sale notice "is Letraset, photocopy or two-colour screen print". Make both photocopy_a3 window notices: J01 taped inside the newsagent's glass beside SB1, D01 inside the grocer's glass. Keep the words.
- H03 "NOTICE TO SHIPMASTERS": British harbour practice is NOTICE TO MARINERS.

**8. No street date, so the age classes contradict each other.**
- The calendar gives a window (1 October to 30 November), not a day, and no check ties a bill's age class to its event.
- T03, the programme for the week from 21 October, is placed at class D (over 120 days) under T01 at class A for the same week. That puts the street after 9 February 1991 and P01 before 1 November 1990 at the same time.
- D01 at class C on SF1 and pier W2.1 would mean posting a 17 November dance by late September.
- The only date every dated placement allows is 26 to 31 October: H03 is dated 26 October, T01 is class A, and P01's meeting is on the 25th.

Amendment:
- Add `calendar.street_date: "Monday 29 October 1990"`.
- Set T03 to class B, D01 to B (both places), and J01 on SF2 and W2.0 to B.
- Add `G.dates.age`: for every placed dated item, street_date minus its class's days must fall at or before its event (for notices, at or after their date) and no more than 42 days before it.

**9. The mirror guard of the 29 hand cards contradicts their own fixings.** The mask is blind to a mirrored hand card (fault 1), so the corner cue is the only guard, and it does not hold together:
- The card board's own note says the cards are "taped to the inside of the glass (pins are for a cork board)", yet its table pins SA01, SA02, SA03, SA07, SA11 and SA12.
- The cues contradict the table. SA15 is taped top-right but its cue is tape top-left. SA01, SA05, SA09 and SA13 are taped or pinned on a board, yet their cue is a string loop and rubber sucker. SA08 is taped top-left, but its cue is a pin hole top-right. K07b, K07c, K09c and K05 are taped or stuck, yet their cues are a sucker or a pin hole.
- Several cues mark both sides (a crease "from the top-right corner", a torn lower-left with a top-right pin hole), which defeats `G.mirror.cues`' left-against-right corner reading.

Amendment:
- Every SA card in the table becomes "tape", no pins.
- Each hand card has one cue matching its fixing and nothing on the opposite half. Taped or stuck cards (K05, K06c, K07a-d, K09a-f, SA01-SA15): one tab of yellowed tape across the top-LEFT corner only. String-hung cards (K01, K06a): the knot and sucker at top-LEFT only.
- Delete every crease, tear and pin-hole cue.
- `G.mirror.cues` compares the 25 mm top-left and top-right patches only. The glyph check in fault 1 also covers mirror.

**10. Placements contradict the brand bible and the items' own words.**
- HC1, the Harbour Board case, belongs "by the dock office" (brand bible; hook-cast's harbour_office is in the docks). It is placed at u 6.95 on the parade's gable, 7 m down Mickey's yard lane (atlas `yardlane` at x 1.5) and out of every camera.
- FC1: the brand bible gives "a timetable board at each ramp with the winter service pasted over the summer one". The target makes it a perspex case on the same gable, with F01 "held behind the perspex", while F01's own variants say pasted and pin-holed.
- C01a, the police appeal, is placed on the brick pier of a house (W0.0). Its own variants say "taped inside a window ... or in a polythene sleeve cable-tied to a lamp column", and PERIOD-PRINT says a window poster is the safer choice.
- K02 (BACK AT, "Hal's Monday break") is on the newsagent's glass. The newsagent never closes midday (hook-cast 6 to 17.30), and Hal's shop is not on the built street (the fascia target's note 3).
- K05 says "at 1.45 m" but is placed with its bottom at 1.12.

Amendment:
- Remove HC1 and FC1 from Quay Street until the dock office and the ramp are built. FC1 becomes a painted timber board, 600 x 800, with F01 pasted over F02 and no glazing.
- Move C01a inside the empty unit's glass (SF2, u 0.30, z 1.30, four tape tabs).
- Leave K02 unplaced.
- K05's bottom goes to z 1.38.

**11. Parts a script cannot make from target.json alone.**
- K04's "dog silhouette, our own drawing" and its bar: no polygon is given, and the L3 sheet shows a bare ring.
- G02's "white ring inside": no width.
- K02's ticks, hands and paper-fastener: no sizes.
- The plates' relief edges. The cast letters' draft and top radius are missing; "rolled edge" on S02 and S03 has no radius.
- The two cases' rail sections and glazing beads.

Amendment:
- K04: either a point list for the silhouette in the 70 mm roundel, or drop the silhouette and keep the ring (7 mm) with a 7 mm bar from the inside top-left to the inside bottom-right at 45 degrees.
- G02: white ring 16 mm wide at 0.70 of the disc's radius.
- K02: ticks 2 x 8 mm; hour hand 30 x 5 mm; minute hand 40 x 4 mm, buff card; fastener 6 mm brass.
- Plates: raised letters and border with 10 degrees draft each side and a 0.8 mm top radius; pressed aluminium rolled edge radius 3 mm; enamel rolled edge 6 mm (all Judgement).
- HC1 rails: 46 x 60 mm with a 4 mm chamfer on the outer arris; glass 4 mm in a 10 x 10 mm bead (if HC1 is kept anywhere).

**12. The ferry timetable strands its one boat.** Monday to Saturday, the last sailing from the Hook (11.00) leaves the single vessel (brand bible) on the far side overnight, but the first sailing is from the Hook at 6.30. `G.ferry.schedule` does not test where the boat sleeps.

Amendment:
- The far-side column ends "9.45 / 10.45 / LAST CROSSING 11.15", so the boat ends at the Hook at 11.30 and the street's "last crossing's at eleven" still holds from the Hook.
- `G.ferry.schedule` checks that each day ends where the next day's first sailing leaves.

**13. Name plates: judgements against the project's own note.**
- All three placements default to the district line (THE HOOK and so on). No source supports it, and the street-clutter note describes a plain name plate.
- The `p` variants (MR1) are what that note lists as wrong for 1990 ("postcodes"), and they can never be shown anyway.
- QUAY STREET is cast iron of the 1920s or 1930s carrying the ruled Kindersley stand-in, a letter recommended in 1952, by which time raised plates were cast aluminium.
- S0x n plates are 170 mm deep, against the note's 20 to 25 cm.

Amendment:
- The default and placed variant is `n` (name only); `d` stays as a variant until a dated photograph shows a district line.
- Delete S01p, S02p and S03p, and MR1 from the approved words.
- QUAY STREET becomes cast aluminium: letters and border raised 3 mm, painted white with black letters, the paint flaking at the raised edges.
- Minimum plate depth 200 mm.

## What is right

- **Words.** Every one of the 308 strings is ours and fits canon's world. There is no drink, betting, bingo, raffle, pub or child anywhere, and no slur. The poll tax is an invented local campaign with no party or person. The names canon owes (football club, paper, pirate radio, TV, telephone operator, postal cypher, council) are all absent. The brand bible's unminted proposals are rightly refused. There are no real towns, codes or brands, and nothing after 1992.
- **Calendar.** Every printed weekday is right for 1990; I computed all 23. Monday 1 October, the GMT note after 28 October and the 12 h 25 min tide step are right too.
- **Prices.** Plausible for 1990: cod by the ONS note; fares, admissions, cards, rents.
- **Sizes and type.** Paper sizes are correct: double crown 20 x 30 in, crown 15 x 20, quad 30 x 40 landscape, four-sheet 40 x 60. Every font is OFL and its licence was read. I re-measured the plate widths from the Marcellus SC file and they agree within 7 mm. Marcellus SC is used as ruled on 30 September, and the Q's 36 mm tail is allowed for.
- **The world's hours.** The market's days, LAST WASH an hour before the laundry closes, and the fishmonger's hours all match hook-cast.
- **Placements and legibility.** The letting board's centre matches the fascia target: board x 2705 is street x 24.0, z 2.90 to 3.35, 50 mm clear. No full bill is above 2.3 m, so everything is within a paster's reach. The plates sit at junction corners and the street's end at about 2.5 m, as 1990 practice and the earlier note put them. Headlines and the plate read across the street: the QUAY STREET plate on the gable is about 18 px a capital in the hook frame.
- **What the checks do catch.** Mirrored printed sheets and plates (S01d, S02d, L01, P01, SA06 all fail when mirrored), shifted blocks, wrong fonts, misspelt plates and changes of length.
- **Honesty.** The target is candid about what it rests on, and its ageing model is reasonable.

## Notes (narrow; not faults)

- CAN'T PAY - WON'T PAY is the common 1990 slogan (and Dario Fo's English title), not a party's mark. Keep it.
- H04's heights fall from 4.7 m on 1 November, but the full moon was 2 to 3 November 1990, so springs peak about 4 November. Re-run the heights to peak on Sunday 4 November: 4.4, 4.6, 4.7, 4.8, 4.7, 4.5, 4.2.
- SA01's 960 417 is one digit from Mickey's 960 418. Use 960 471.
- COCKLES 45p needs a unit (45p PINT). Smoked haddock at £2.40 sits under fresh haddock at £2.50; usually it is dearer.
- G01 is a national-style four-sheet advertisement pasted under fly-posters. Legal adverts lived in framed contractor panels. Low priority once SF1 is cut (fault 4).
- T01's art asks for "a telephone box lit". Add crowns, kiosk lettering and operator marks to its forbidden list.
- The P1 previews show a council crest, blurred, on the case header. Mask it as the windows were masked.
- The forbidden lists miss plurals and near terms: SCHOOLS, BABYSITTER, PLAYGROUP, SCOUTS, CUBS, BROWNIES, INN, TAVERN, DARTS, QUIZ NIGHT. They also miss real soap powders (PERSIL, DAZ, ARIEL, OMO, BOLD, SURF), cinema chains (ODEON, ABC, RANK), real campaigns (MILITANT, SOCIALIST WORKER) and real wrestlers. The approved-word whitelist covers today's manifest; these lists guard later edits.
- Fonts off the asset plan's table: Patrick Hand, Libre Franklin, Libre Baskerville, Josefin Sans. Record each in DECISIONS.md or use the plan's faces; Kalam or Caveat Brush read more like a felt marker than Patrick Hand. Section 4b is wrong that League Gothic is not on the plan's table: it is.
- target_drawing.py's docstring promises elevations of the west piers and the plates' places, but only SF1 and SF2 are drawn.
- Not checkable here (network): real firms named QUAY PRINT or ARMITAGE & STOBBS; a film called The Fourth Witness.

## How I tested

- self_check.py was run on a copy under the scratchpad with --no-write: 215 of 215.
- target_drawing.py drew 76 items and 2 cases into the scratchpad.
- My test script (posters-review/wrong_renders.py in the session scratchpad) renders one block changed in the pixels with the manifest unchanged, and scores it with the target's own reader. It also mirrors whole items, skews true renders, and applies the target's hand_styles jitter over 20 seeds: true jittered cards pass, 1 seed in 20 fails on SA06.
- A second probe (gate_probe.py) ran test words through the target's forbidden lists, the content gate, RealWorld.cs and imagegen's tokens.
- I projected the placements into cam_hook by vignette-scene.json's numbers.
- No file in the target was edited, and nothing was committed.
