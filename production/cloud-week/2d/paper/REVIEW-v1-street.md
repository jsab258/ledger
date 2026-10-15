FAIL

# Paper, cards, boards and plates (units 4.2 to 4.4): review v1, STREET view

12 October 2026, fresh reviewer, first try. What I looked at: the contact sheets and the SB1 preview; the full pictures reduced to street distance (0.6 to 2 px/mm), flat and lit from their height maps (my own raking light); each class-B picture against its class-A clean picture; the four Geograph photographs; and placed_decals.json, for what the default street shows.

**Verdict: FAIL.** The set reads as one town's 1990 paper. But four things would be seen from the pavement: how the paper is lost in classes B to D, a window bill with no fixing, the plastic OPEN sign's folded corner, and the newsagent's board in one hand.

## What passes

- **Words and dates.** No wrong word on any placed item, and nothing breaks the content rule ("BET" and "ALE" occur only inside BETWEEN and SALE). Every date falls on the right 1990 weekday, and the prices are believable.
- **Stocks and colours** follow section 4. The poll-tax bills read as one campaign, the notices as council, police, harbour and chapel paper. The boards and plates are in proportion with the Muswell Hill and Southwark photographs.
- **Fixings and orientation.** Nothing is mirrored or turned. Every hand card has one cue at the top-left and nothing on its right half. The sheets in windows (J01, D01, C01a, P04) carry four tabs, and the sleeves show their clear band.
- **Not counted:** the shortfalls NOTES.md already names (flat art slots, T02's tag zone that reads as a glow, F02 with no words, K02's B under the sucker, no overposting, no brick relief).

## Findings, worst first

1. **Torn paper in classes C and D is drawn as icicles (fault).** WHAT: the loss hangs as dozens of vertical spikes, 5 to 15 mm wide and 20 to 60 mm long, cutting through the lettering. WHERE: M01_C (placed on the empty unit's glass, SF2), lower half; also G02_C, B01_C, G01_C and T01s_C. WHOSE: the maker (bill_pasted loss). FIX:
   - Build the loss from 2 to 5 tear patches with outlines of wavelength 30 to 120 mm and amplitude 10 to 40 mm.
   - Open both the paper mask and the loss mask with a 15 mm disc, so that no tongue narrower than 15 mm is longer than 10 mm (test: count 0).
   - Then add the fibre fringe (0.5 to 1.5 mm) and keep the pale rim.
   - On glass, leave a paste ghost over the lost area: (214,205,185) at alpha 0.3.

2. **The printer's imprint survives as a straight-edged island (fault).** WHAT: the class-B loss stops exactly on the imprint's reader window, leaving a crisp rectangle of paper (68 x 13 mm on M01, 130 x 13 mm on P02 and P03) below a torn edge. WHERE: P02_B and P03_B (placed on SF2) and M01_B (placed on the west pier), bottom centre; also F01_B, G02_B and T03_B. WHOSE: the maker (the reader-window rule). FIX:
   - Imprints are illegible by design and not read (§14), so take the imprint out of the protected windows.
   - End the loss at least 4 mm from any other window, on a torn contour.
   - Test: no straight run of the paper outline longer than 8 mm, except the sheet's uncut edges.

3. **The poll-tax bill in the cottage window has no fixing (fault).** WHAT: at SF9, P02 is scaled 0.585 and "taped inside the glass", but it uses the pasted class-A picture: no tabs, so it floats in the window. WHERE: P02_A's corners are plain stock (255,124,56); the SF9 placement. WHOSE: the maker. FIX: a class-A glass_bill picture of P02 with no loss and four corner tabs of 65 x 27 mm on the 508 mm sheet (38 x 16 mm after scaling), rgb (196,164,84) at opacity 0.85.

4. **The plastic OPEN/CLOSED sign is dog-eared like card (fault).** WHAT: a white folded triangle of about 12 mm at the bottom-left corner, plus a grey smudge. K03a hangs on eight shop doors, so the same fold repeats down the street. WHERE: K03a_B and K03b_A/B/C, bottom-left corner. WHOSE: the target (it gives K03 the card_felt wear) and the maker. FIX:
   - A plastic_print wear: no dog-ear, curl, bleach or smudge; 6 to 20 scratches, 0.2 to 0.5 mm wide and 5 to 40 mm long; grime at most 5 per cent.
   - Keep the 8 mm corner radius.
   - Use at least three seeds across the eight doors.

5. **The newsagent's board reads as one template, not fifteen advertisers (fault).** WHAT: fourteen cards share one face (Patrick Hand) and one layout: heading cap 7 mm at 8 mm from the left, body cap 4.4 mm at a 9 mm pitch, lower half blank. They carry the same tab and sit in a tidy four-row grid with 60 per cent of the board bare glass. A real window holds many hands, crowded and overlapping. WHERE: SB1_B and SA01 to SA14; the target's §5.7 card lines and card_board table. WHOSE: the target. FIX:
   - (a) Add Kalam and Gochi Hand (OFL, on asset-plan note 4's own table) with OFL.txt and a catalogue line; no two neighbouring cards share a face.
   - (b) Vary each card: heading cap 6 to 11 mm, body cap 3.5 to 6 mm, line pitch 1.7 to 2.3 times the cap. Centre four cards, write two entirely in felt-pen capitals, and fill 50 to 85 per cent of the card's height.
   - (c) Overlap at least six pairs by 5 to 25 mm, and cut the bare glass to at most 35 per cent.

6. **Every class-B bill loses its bottom edge the same way (fault).** WHAT: on 7 of the 9 class-B bills (P02, P03, M01, T03, G02, F01, G01) the loss is a ragged band across the full width, the same edge every time, whereas the target says the lower corners go first. WHERE: the lower 10 to 40 mm of each _B picture. WHOSE: the maker. FIX: at least 70 per cent of the lost area within 120 mm of the lower corners, and at least half the bottom edge untouched.

7. **Letting boards: the grime is pencil lines and the foot a brown crust (fault).** WHAT: the streaks from the top edge are 2 to 4 mm wide, crisp, of even width and evenly spaced, so they read as scratches. The foot is a continuous brown noise band, 4 to 10 mm high. WHERE: L02_C, L03n_C and L04_C (all placed): the top third and the bottom edge. WHOSE: the maker. FIX:
   - Streaks 15 to 60 mm wide at the top, tapering to 5 to 20 mm, 80 to 250 mm long, 4 to 10 per cent darker, feathered by at least 5 mm, 2 to 5 to the metre, unevenly spaced, strongest under the top screws.
   - The foot: 2 to 4 separate peeled bites, 20 to 80 mm long and 3 to 15 mm deep, showing grey plywood (150,145,135), with the rest of the edge painted.

8. **Finger smudges are grey blobs (minor fault).** WHAT: soft neutral-grey discs 10 to 15 mm across, 9 to 16 per cent darker than the card, in mid-card. WHERE: K05_B at 146, 111 mm from the top-left corner; K06a_B at 86, 25 mm; K07a_B and K07d_B beside the tab; K01. WHOSE: the maker. FIX: an oval of 12 x 18 mm, 3 to 5 per cent darker and warm (multiply by 0.97, 0.96, 0.94), within 15 mm of the bottom edge or of the tab.

9. **Edge tears are clean V-notches (minor fault).** WHAT: each tear is a triangle cut out with straight sides. WHERE: P03_B, right edge at the ASSEMBLE line; F01_B and F01_C, right edge; F02, top and left; T01_B, left. WHOSE: the maker. FIX: a slit 20 to 140 mm long at 30 to 70 degrees to the edge. Either fold its flap back (the sheet's back plus a shadow, as the lifted corners already do) or lose it as a ragged bite; no straight segment longer than 5 mm.

**Narrow points (each passes):**

10. **S01n_D (placed).** The lost paint is round, evenly spread blots on every letter edge, a pattern rather than flaking, though the name still reads at 2.5 m. Angular flakes of 2 to 12 mm, twice as dense on the upper half of each letter, would read better. Maker.
11. **Tabs on card faces inside the glass.** Tape on the room side would show only beyond the card, but this is the target's chosen cue (§14). On weeks-old cards its amber reads as masking tape. Target.
12. **Class-B bills show little weather from the street.** Apart from an even tint they look clean, because the two rain runs per bill vanish below 1 px/mm. This is within the target's numbers, and the cockle in the height map carries the age. Using the target's top values (1.5 mm wide, opacity 0.4, at least 40 mm long) would help.
13. **Empty space in layouts.** M01 (140 mm), B01 (150 mm) and H01 (not placed; a 120 mm empty field) leave space that a jobbing printer would have filled, so they read slightly as retro pastiche. Target.
14. **Small lines and boards.** On L03n and L04, TO LET runs to 15 mm from the hairline, as full as the Muswell Hill board, and both carry the held agent's number. P05 and P06 show the campaign name at the small size the target allows.

## What I cannot judge from the files

- the maps under the game's light
- fluorescence and the wet look
- reflections on the glass
- the decals at true size and distance on the built walls
- the string, chain and sucker in 3D
- the art pictures still to be made
