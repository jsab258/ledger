# Review of TERRACE-KIT-TABLE-2026-10-29.md (fresh reviewer, 29 October 2026)

**Verdict: PASS WITH FIXES.** The counts and the brick photograph (G1) reproduce. The stone photograph's (G2) scale does not hold where it was used. The table builds a window height against a standing ruling. Two "reused as built" claims are wrong.

**Method.** I measured the four previews with my own Python (brightness profiles; FFT of brick rows). Pixels were converted to the original photographs using each preview's crop box and zoom from the two make_previews scripts. The scale is FD's door-leaf box (10.07 and 21.66 mm per pixel). For G1, brick length gave a second scale.

**G1 agrees within 10%, mostly within 3%:**
- Course: 85 to 87 mm. Brick plus joint: 216 to 220 mm.
- Upper opening: 1.00 to 1.04 × 1.62 to 1.69 m.
- Sill 3.70 m above the threshold; eaves 5.66 to 5.71 m.
- Door: 0.86 to 0.89 m wide, head 2.60 m.
- Plot: 3.88 to 3.90 m.
- Downpipe: 75 to 95 mm (one pixel is 10 mm).

**Counts confirmed** from the module strings: 42 meshes; 14 fitted; fronts A 31/25, B 27/21, C 35/29. Widths and opening alignment check.

## Faults

**1. G2's scale does not carry to where it was used.**
- Words: window "1.14 × 1.54 to 1.61", "storey step 2.5", "eaves about 4.7", ±5%. Item 2: "both photographs read 1.61 to 1.65".
- Source: the scale door is at the right of p7. The figures come from the middle house, about 300 px to the left. At that scale, its own door leaf reads 1.68 m and its neighbour's 1.57 m: too short for front doors. The view is oblique or stepped.
- With a usual 1.93 m leaf, those figures are about 15% low: window about 1.8 m, eaves about 5.4 m.
- Correction: mark them unverified; drop G2 from item 2's evidence.

**2. The window height contradicts a standing ruling.**
- Words: "His rulings stand … until he answers", yet the table builds 1,650 and item 2 asks him.
- Source: RULINGS, 8 October: "1.68 m". G1 reads 1.62 to 1.69, within ±5% of 1.68; no photograph contradicts it. His page carries nothing his rulings settle.
- Correction: build 1,676.4, the built sash's height, so the sash re-run changes width only. Keep the head on the grid at 2,475. Record the 26 mm grid exception in DECISIONS and drop item 2.

**3. The held pots are not pots.**
- Words: #41 and #42 "held", "reused as built".
- Source: TF lines 2008 to 2014: they "measure 0.67 and 0.95 m across, which is a whole stack and not a pot". TF builds 600 mm pots instead. The files confirm it (weathertop 0.95 m, roll-top 0.7 m across).
- Correction: re-run TF's pot builder (`_pot_mesh`, `plan_pots`).

**4. The reuse and recipe counts are overstated.**
- Each of door_T1 to T3.glb is a whole door: jambs, head, transom, a 267 mm fanlight and a stone step. The leaves must be cut out; #17 and #30 duplicate parts already in them.
- No recipe makes #10 (TF's bands are flush panels), #21 (no fascia board) or #33 (no ridge piece).
- Correction: about 3 reused, 22 re-run, 17 new. Name build_door.py and build_windows.py.
- Re-run the sash only through LEDGER_SASH_TARGET with a new target file. Otherwise window_design.py reads the street's own target.json, the one route to touching Quay Street.

**5. Some sizes are off the grid, despite the claim.**
- #40: 4½ × 2½ bricks, oversail 56 mm.
- #21: fascia 200 mm (2⅔ courses).
- #36: hopper 250 × 200.
- #30: step 300 deep.
- #3: six × 1,350 makes 8,100 against the 7,875 depth. 5 × #3 + #2 + #1 makes 7,875 exactly.
- The end wall's top storey lacks the 150 mm course up to the gable.
- "CamberArch_…x300" against "ring 225, rise 1/50": about 245 tall.
- Correction: fix these, or list them as exceptions beside the pipes and the reused leaves.

**6. Sill and lintel overhangs depart from G1 without a flag.**
- Words: "112.5 past each jamb" for both. G1: "about 90" and "about 70" (I read 97 and 79).
- That is 16 to 60% over, against the 8 October rule.
- Correction: flag them as set by the grid, or use 56 for lintels.

**7. Party piers on mirrored houses.**
- #7 sits on one side of each house. Mirroring B gives one boundary two piers and two downpipes, and the next none.
- G1 shows one pier between handed pairs.
- Correction: one pier per boundary, with a check.

**8. G1's ground bay is not mentioned.**
- The one measured brick photograph has a ground bay; the family is flat-fronted.
- Correction: record the choice in DECISIONS.

**9. Small faults.**
- The d3 zoom is 4.0, not 4.06: course 86.9 mm, not 85.6.
- "P1" is Teignmouth 2012 in the door rows, Hull 1985 in section 6. The 1/50 camber rests on the 2012 door.
- For house C, #13's "1 per #4" belongs on #14.
- Lintels are named by their own length, arches by their opening. MAFIA-KIT 5.1 names by opening.

**10. Open items.**
- Item 1 is sound and stronger than written. Two independent scales give 85 to 88 mm courses. VS's 75 is arithmetic on today's 65 mm brick, not a period source.
- Item 3's gap is MAFIA-KIT's own: 30 to 45 meshes targeted, about 25 budgeted. After faults 3 and 4, 22 to 28 hours is likelier than 20 to 24, and cutting to 38 does not close the gap.
- Item 5 holds. Nothing edits Quay Street.
