# Monday's numbers, raw: Sheila against Tom per garment (12 November 2026)

Extraction only, no judgement. TL = production/time-log.jsonl, number = the line of the window's start event (a window runs to its next stop; minutes by tools sum of start and stop times, read 12 Nov). AS = production/api-spend.jsonl. HO = production/handover/HANDOVER.md. TA = production/handover/TRIED-ARCHIVE.md. SK = .claude/skills/game-garment/SKILL.md. Notes in production/research/clothing-pipeline/ are named in full once, then short. "Own" = the window's name is about that garment alone; "shared" = the window also names other work (a ceiling, not the garment's time). "Not found" = no figure in any source read. No estimate is made here.

## What the sources hold, and what they do not

- Time log (645 lines, 317 windows, 12,473.9 min in all): windows are per sitting, not per garment. No window is per garment except those marked own. Helpers' hours are not logged apart (a helper appears only as a window named "helper").
- Dollars: AS has 21 lines (1 Nov to 8 Nov); none names a garment, Tom, Sheila, Ron or Darren (grep count 0). Dollars for dress windows exist only in unit-costs/RON-MEASURES-2026-11-08.md (Ron and Darren, window dollars); no Tom or Sheila clothing dollar figure found. All dollar cells below: not found.
- Sheila's refit hours come from the notes' own "About N h" lines (not the time log; the log has only the three small windows below). They are stated by the builder, not measured by a log.
- Skill steps: SK has nine steps (1 Reference and pattern; 2 Avatar and pose; 3 Drape; 4 Rib cuffs, bands and hems; 5 Zipper and topstitch; 6 Detail in Blender; 7 Game mesh and UVs; 8 Bake, texture and wear; 9 Skinning, levels of detail, the game) plus "A refit to another body" (SK line 99) and "Dressing a man" (line 89). No note numbers its work by those steps. Sheila's notes number the refit plan's own steps 0 to 7 (SHEILA-REFIT-PLAN-2026-11-09.md section 3), and name the tools used. Where a note names the skill's "A refit to another body" route (carry_garment.py, skin_garment.py), it is shown as "refit route". Steps used from a skill for Tom: not found as a count in any note.
- Pre-October work (before 5 Oct, no log): hours not found (git-only; Ron's pre-October span is in ron-whole-person/RON-PRE-OCTOBER-2026-11-08.md, not Tom's or Sheila's).

## Tom

Time-log windows by garment (minutes; own and shared kept apart).

| Garment | Own windows (TL line, min, name) | Own hours | Shared windows, not added (TL line, min) | Tries / set-asides (source) | Steps used |
|---|---|---|---|---|---|
| Jumper (cuffs and sleeve ends) | 164, 29, "Tom's cuffs, the third try (four drapes; set aside)"; 198, 30, "Tom's sleeve ends ... and cuffs (set aside), measured" | 0.98 (59 min) | none | Cuffs: three tries, set aside (TL 164 name; SK step 4 "simulator elastic cuffs (three tries)"; RECIPE.md line 54) | SK step 3 and 4 (SK text); not numbered in the windows |
| Jumper (drape and chain) | 290, 24, "C9 jumper drape j1"; 637, 31, "Vellum third try on Tom's jumper (helper)" | 0.92 (55 min) | 247, 110, "C jumper cut; D11 wet-ground checks written"; 304, 92, "C9 jeans, jumper, boots: chain, import, review, boots fit, details, set-asides" | Drape Studio's jumper 2 of 2, spent (HO line 55); Houdini Vellum on the jumper: try 1 and 2 set aside (DECISIONS.md line 91), try 3 with his yes, set aside 12 Nov 10:50 (DECISIONS.md line 112); Marvelous stays the drape tool | Drape (SK 3); chain of carry, import, review (TL 304 name) |
| Jumper (Drape Studio retest) | not found as a window of its own | not found | none | DRAPESTUDIO-TEST-2026-11-10.md and -11.md: runs named, no hours in them (grep for hours and dollars: 0 lines) | SK 3 only |
| Jeans | 270, 7, "C9 jeans: Titan drafted, Marvelous job written; the night's push" | 0.12 (7 min) | 304, 92 (above); 454, 7, "n02-tom-jeans/boots ... packaged reviews"; 619, 77, "Tom's films and the jeans film (texturing test)" | Jeans masks 2 then the fair film, set aside as a garment method (HO line 55) | SK 1 and 3 (pattern drafted, Marvelous job, TL 270) |
| Jacket (drape, weights, packaged film) | 228, 24, "grain's diagnosis ... Tom's jacket into the garment path" (shared with the grain diagnosis, counted here as named); 230, 9, "the jacket imported ... a build asked"; 234, 15, "Tom in his jacket, first build"; 259, 38, "C9 jacket: per-pose check, weights and UV order mended, editor film passed"; 272, 25, "C9 jacket packaged sit film (13 of 13)" (also names the head's pitch research) | 1.85 (111 min) | 251, 80, "D11 wall marks ...; 1.3 jacket withdrawn; D10 Sheila's desk" | 9 Nov: jacket front set 7 mm clear of the head mesh, passed review packaged (NOTEBOOK.md line 2018) | SK 7 to 9 (names in TL 259: per-pose check, weights, UV order) |
| Jacket collar | 280, 27, "collar: first try (inner facing), filmed, failed"; 300, 33, "collar second try (re-weighted), set aside" | 1.00 (60 min) | 329, 95.8 (third try, shared with speech work); 331, 48 ("pale line's try", shared with sitting walk); 333, 52.5 (fourth try, shared with test close) = 196.3 min shared | Four tries, set aside (TA line 20; TA line 50 "the collar 4, set aside"); his one try of about 2 hours is inside TL 333's name; 282, 23 min (records and push, collar's second try next) not counted | SK 4 (collar rectangle, stiffer fabric) |
| Boots (Epic's boots on Tom; Ron's boots carried to him) | none of its own | not found | 335, 39, "Epic's boots on Tom (research, install, wear); n02-4 corner"; 304, 92; 308, 185, "C9 outfit: boots maps and reshape, reviews ..."; 454, 7; 617, 23 (boots v5 with records) | Boots: 5 tries (his yes), passed (HO line 55). One measured refit: Ron's boots carried to Tom 2.95 h (SHEILA-REFIT-PLAN-2026-11-09.md section 3, "Hook review, 3 Nov"). Boots v5 and jacket judged together: "about 0.4 h for the build, pictures and reviews" (NOTEBOOK.md line 2020) | Refit route (carry_footwear); SK 9 |
| Shoes ("C9 shoes", wearer not named in the windows) | 284, 0; 294, 10, "shoes: scan in, marks painted out, credits"; 302, 57, "shoes fitted (helper), records" | 1.12 (67 min), wearer not stated | none | not found | not found |
| Surfaces, chest skin, talk view | 609, 9.3 (talk view filmed); 615, 2 (chest skin try 1); 623, 12 (painted colour maps); 627, 37.6 (import and film) | 1.01 (60.9 min) | 619, 77 (shared, counted under jeans) | Surfaces by painted maps: 3 tries, set aside (HO line 55; DECISIONS.md line 66); chest skin 1 of 2, passed (HO line 55) | SK 8 (texturing, painted maps) |
| Outfit specification | 126, 35, "Tom's outfit specified, body exported and measured" | 0.58 (35 min) | none | not found | SK 1 and 2 |
| Hair crown (not clothing) | 364, 80; 368, 46 | 2.10 (126 min) | none | Crown 4 tries, listed (HO line 55) | none |

Tom totals:
- Own windows, clothing only (jumper cuffs 59 + jumper drape and Vellum 55 + jeans 7 + jacket 111 + jacket collar 60 + shoes 67 + surfaces, skin, film 60.9 + outfit specification 35) = 454.9 min = 7.58 h. The shoes' 67 min have no wearer in their names; without them 387.9 min = 6.47 h.
- Shared windows, a ceiling, not added to the above: 247 (110) + 304 (92) + 308 (185) + 335 (39) + 454 (7) + 617 (23) + 619 (77) + 251 (80) + 329 (95.8) + 331 (48) + 333 (52.5) = 809.3 min = 13.49 h.
- Hours for the whole of Tom's clothes: not found (only own and shared windows; the log has no per-garment split).
- Dollars: not found.
- Tries and set-asides named above: set aside = cuffs, jacket collar, Drape Studio jumper (spent), Vellum on the jumper, jeans as a garment method (texturing), surfaces = 6 entries counting the Vellum tries as one. Passed after tries: boots (5), jacket clearance, chest skin (1 of 2).

## Sheila

| Garment | Hours | Source of hours | Dollars | Tries | Set-asides and open faults | Steps used (as the note names them) |
|---|---|---|---|---|---|---|
| Body, step 0 (C1 against S4) | not found (plan estimate 1.0 h E, not a result) | SHEILA-REFIT-PLAN section 3 step 0; SHEILA-STEP0-2026-11-11.md states no hours | not found | not found | none stated | Plan step 0; Blender headless measure |
| Blouse (carried to S4, skinned) | about 0.4 | SHEILA-BLOUSE-S4-2026-11-11.md, line 3 | not found | Carry 1 of 2, passed; skin try 1 failed (triangle cap), try 2 passed; shoulders trim 1, passed (SHEILA-CARDIGAN-S4 note and HO line 55) | Head mesh: 52 collar points inside, "not cleared" in that note; blouse hem lump through the cardigan, two tries (cover step diverged twice), open fault | Plan step 1; refit route (carry_garment.py, skin_garment.py), trim2.py |
| Blouse trim | not found | SHEILA-BLOUSE-TRIM-2026-11-11.md holds no hours (grep) | not found | not found | not found | not found |
| Skirt (carried to S4, skinned) | about 0.3 | SHEILA-SKIRT-S4-2026-11-11.md, line 3 | not found | Carry 1, passed; clear over blouse try 1 failed, try 2 left 3 flips (2 of 2); skin 1, ran clean (same note); HO line 55: "Sheila's skirt band clear 2 of 2, set aside" | Set aside: band top front ragged (open fault). Seated back hangs through the chair: 4,022 points (20%), no route chosen (three routes costed 0 h, 6 to 10 h, 8 to 12 h, unverified); cloth route note about 7.5 h (SHEILA-SKIRT-CLOTH-ROUTE-2026-11-11.md line 18), not built | Plan step 2; refit route |
| Cardigan (from Tom's jumper) | about 3.2 | SHEILA-CARDIGAN-S4-2026-11-11.md, line 3 | not found | Carry 1; welt and cuffs passed; cut 1; clear over blouse try 1 failed, try 2 passed; skin 1; left band fix 1 (passed); collar fault (c) passed at try 2; collar fault (d) 2 of 2 (HO line 55) | Set aside: collar fault (d) dark strips at the shoulder line (334 collar points under the cardigan, up to 17.4 mm). Open: hem lump, 2 collar points in the head, seated cloth in the arm, welt UV density | Plan step 3; refit route; chain: carry, resize_bands, build_cardigan, clear_layers, follow_cloth, skin_garment |
| Cardigan band diagnosis | not found | SHEILA-CARDIGAN-BAND-DIAGNOSIS-2026-11-11.md holds no hours (grep) | not found | see above | see above | not found |
| Shoes (Ron's boots carried and cut) | about 1.5 | SHEILA-SHOES-S4-2026-11-11.md, line 3 | not found | Carry 1 (one try); collar line try 1 and 2 (both faults used their two tries) | Left plainly: heel 20 mm not 25; shape still Ron's work boot; no texture maps; nothing in Unreal | Plan step 4; refit route (carry_footwear.py); cut_derby.py |
| Shoes, second route (modelled) | not found | SHEILA-SHOES-S4-MODEL-2026-11-11.md: no hours (grep) | not found | not found | not found | unread beyond its first lines |
| Handbag, spectacles | not found | made earlier on C1; spectacles sit 2 to 3 cm high on S4 (SHEILA-REFIT-PLAN section 1) | not found | not found | spectacles held | not found |
| Colours (white layer) | not found | HO line 74: "Sheila's colours (11 Nov): ... comes in white; now a selftest" | not found | 1, fixed (HO line 55) | none | not found |

Sheila time-log windows (not added to the note hours; overlap with them unknown):
- 607, 5.0 min, "n09-6 helper: Sheila refit plan" (own).
- 629, 6.0 min, "n09-6" stop note "Sheila collar faults c/d try 2: cardigan neck cut, collar lift both islands, seen blouse body cut, import".
- 631, 5.0 min, "n09-6" stop note "Sheila collar try 2 filmed packaged: c pass, d set aside".
- Own total 16.0 min = 0.27 h.
- Windows naming Sheila but not about her clothes: 60 (43 min, tester's route fault), 251 (80, desk), 339 (24, hand into hip), 33/35 stop notes (spots).

Sheila totals:
- Hours stated in the notes: blouse 0.4 + skirt 0.3 + cardigan 3.2 + shoes 1.5 = 5.4 h (builder's own "About" figures, not log measures).
- Log windows named for her clothes: 0.27 h. The two figures are not summed (the 0.27 h may lie inside the 5.4 h, unverified).
- Plan estimate for the whole refit: about 15 h E (12.5 without steps 4 to 6), SHEILA-REFIT-PLAN section 3 end; an estimate, not a result. The item n09-6 total is stated there as 18 h.
- Dollars: not found.
- Set aside: skirt band clear, collar fault (d), blouse hem lump (open, two tries), seated back (no route chosen); pre-log, 29 Sep: skirt sitting after 7 tries, cardigan route after 3 blind reviews, shoes after 3 reviews (SHEILA-REFIT-PLAN section 1 table).
- Tries counted per fault (from the notes above): blouse 1 + 2 + 1, skirt 1 + 2 + 1, cardigan 1 + 1 + 2 + 1 + 1 + 2 + 2, shoes 1 + 2; summed count of tries is not stated in any source and is not added here.

## Ron and Darren (found)

- Ron: ron-whole-person/RON-COST-TABLE-DRAFT-2026-11-09.md (reviewed 12 Nov): windows touching Ron 9.24 h, a ceiling; indicative pre-October span 26.4 h; Ron-only hours and dollars not recorded; no grand total in that file. Jumper and jeans refit: Ron-named 0.63 + 0.30 h (TL 555 to 558) with shared dress windows 1.77 + 0.47 + 1.49 h; dollars six dress windows 30.59 to 40.25 shared with Darren (unverified there). Boots: Ron's own pair passed before 30 Oct; making hours not recorded. Donkey jacket: 5.4 h (25 to 30 Sep, git span) + 3.69 h (7 Oct windows TL 32 and 40, shared), set aside after three blind reviews.
- Darren: TL 549, 28 min, "n02-9-dress-the-cast: Darren on his own body; office and sit pictures"; TL 551, 89 min, "Darren's second fit, both hems; office board checked"; TL 464, 9 min (Tea Rooms man). Sum 126 min = 2.10 h (shared with office work). Carry of Tom's jeans and jumper to Ron and Darren: 0.32 h, window 15:21 (RON-MEASURES-2026-11-08.md line 31).

## First against latest, per garment kind made more than once

| Kind | First made (wearer, hours) | Latest made (wearer, hours) | Source of each | Other makes between | Gap |
|---|---|---|---|---|---|
| Knit top (jumper, then cardigan) | Tom's jumper: own windows 0.92 h (TL 290, 637) plus cuffs 0.98 h (TL 164, 198); shared windows 3.37 h (TL 247, 304); total for the jumper not found | Sheila's cardigan carried from Tom's jumper: about 3.2 h (note line 3) | TL lines as listed; SHEILA-CARDIGAN-S4 | Ron's and Darren's jumpers (refit): Ron-named 0.93 h plus shared windows (Ron table) | Tom's first-make hours not isolated; Sheila's number is a note, Tom's is a log |
| Boots and shoes | Ron's boots: making hours not recorded (Ron table, Boots row) | Sheila's shoes from Ron's boots: about 1.5 h (note line 3) | Ron table; SHEILA-SHOES-S4 | Tom's boots: refit 2.95 h (SHEILA-REFIT-PLAN section 3, from the Hook review); five tries for boots v5 | First make's hours not found |
| Jeans | Tom's jeans: own 0.12 h (TL 270), shared 304, 454, 619 | Ron's and Darren's jeans (refit): no row of their own in the Ron table, folded into the jumper row | Ron table, Jumper + jeans row | none | Neither wearer's jeans has a clean per-garment figure |
| Jacket | Ron's donkey jacket: 5.4 h (git span) + 3.69 h (shared windows), set aside | Tom's jacket: own 1.85 h + collar own 1.00 h = 2.85 h, plus shared 196.3 min on collar tries 3 and 4 | Ron table; Tom table above | none | The two are different jackets (donkey against zip); different spans (git against log) |
| Blouse, skirt, handbag, spectacles, belt, t-shirt, cap | made once in the sources read; no second make found | not applicable | | | not applicable |

Not read: DECISIONS.md and NOTEBOOK.md in full (searched by words only, as the brief requires); the notes' pictures; any Tom note in production/art/clothing/ (not named in the brief); RECIPE.md's per-garment cost lines beyond "a chain about 3 h; a fix 0.2 to 1.5 h" (RECIPE.md line 54, section 6).

## Hours per garment, reconstructed (advisor 117, 12 Nov 13:05)

Marked **reconstructed**, not measured. Method: every commit on any branch since 5 Oct (git log, 1,555 commits, read 12 Nov 13:00) ordered by time; each commit is given the time since the commit before it, capped at 90 minutes (a longer gap is taken as a break); a commit whose message names a garment gives that time to it, split evenly when it names several. Script: the session's scratchpad recon.py (patterns: Tom with jumper/jacket/collar/jeans/boots; blouse, skirt, cardigan, derby/Sheila's shoes). Uncertainty: large. Commits bundle several pieces of work under one message, so a garment's time hides inside commits named for other work (Sheila's cardigan: the note states about 3.2 h, the commits give 1.6 h); helpers' time is not in it; pre-October work is not in it. Treat each figure as a floor of the order of magnitude, within a factor of two.

| Garment | Reconstructed hours | Commits naming it | Span |
|---|---|---|---|
| Tom: jumper | 4.1 | 8 | 30 Oct to 12 Nov |
| Tom: jacket and collar | 10.5 | 29 | 26 Oct to 11 Nov |
| Tom: jeans | 3.0 | 8 | 30 Oct to 11 Nov |
| Tom: boots | 2.8 | 9 | 30 Oct to 9 Nov |
| Tom, in all | 20.4 | | |
| Sheila: blouse | 1.7 (note: 0.4) | 9 | 11 Nov |
| Sheila: skirt | 1.6 (note: 0.3) | 7 | 11 Nov |
| Sheila: cardigan | 1.6 (note: 3.2) | 8 | 11 Nov |
| Sheila: shoes | 0.2 (note: 1.5) | 2 | 11 Nov |
| Sheila, in all | 5.1 (notes: 5.4) | | |

Reading: Tom's clothes took about four times Sheila's, which reused Tom's and Ron's pieces through the refit route in one day. From 12 Nov every garment's work is logged in its own time-log window named "garment: <wearer> <garment> <step>", so the Second Suit has measured hours.
