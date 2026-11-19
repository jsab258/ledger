# Review 05: art (faces, bodies, clothes, the asset plans)

Fresh reviewer, 19 Nov 2026, branch lane-2026-11, read only. Sources: CLOTHES.md, CATALOGUE.md, RULINGS.md, canon.md, NOW.md, FINDINGS.md, DECISIONS.md, production/art/clothing (LOG, garment list, Ron's Kiln plan, set-aside readmes), production/casting sheets, production/approvals (his stored answers), production/specs (garments.json, in-game.json), the Kiln and tool-test notes, the time log, the PC inventory and the morning previews (looked at, not only listed). DECISIONS-TRACE rows on art were tested; the ones used below held.

## Summary

In eight weeks (25 Sep to 19 Nov) no whole person has passed his look. What he has approved on people: four faces (Ron P2, Sheila S4, Darren S6, Tom L1, each after earlier takes were turned down) and two interim clothing yeses on 8 Nov (Ron's and Darren's jeans, jumpers and boots, "Interim"). What he turned down or stopped: the three principals as first put in the game (25 Sep, "face in game looks nothing like concept art, clothes obviously"), the donkey jacket, the flat cap, Darren's face twice, the ready-made suit, procedural tailoring, and Tom as a whole person (11 Nov). No hair has passed. The clothing route has changed about ten times (Blender modelling, CC0 refits, ready-made suit, Marvelous, Houdini Vellum, Cascadeur, MetaTailor, Seamshift, Drape Studio, Loomwright, Kiln), and the same hard faults (sitting, wrists, collar at the neck, layers) followed every route. Kiln, a home-built cloth tool he accepted on 13 Nov on condition it "never becomes its own project", is now the week's main goal at about 70% of effort, with 0 of its 6 v1 lines met (NOW.md:14). Meanwhile the hero frame he sees every morning still shows an out-of-period placeholder woman beside Mickey's, the frozen faces still fail their own casting sheets, Kiln's engine was found on 18 Nov to carry 58 values decompiled from Marvelous although its design note said the opposite, and nothing made in Marvelous has been exported though the paid month ends about 25 Nov. Missing for KCD2-grade people: about 46 of some 50 named and seen people have no face, body or clothes at all.

## Findings, ranked

### 1. People are not moving forward; the clothing tool became the project (high)

Impact: the game's people are the thing he judges whole frames by, and they have stood nearly still while effort moved into building a cloth simulator. For him: weeks of page items about tools and tries, and no complete person to look at.

Evidence:
- Approvals on people (production/approvals/answers/INDEX.md): yes to faces and to "dressed-men-look" with the note "Interim. Next: a real wool knit texture, different colours for the two, fix Darren's neckband" (verdicts/dressed-men-look-2026-11-08.json); "tom-whole-person: no ... Boots read as rubber slippers, the jacket has no cloth texture, the jeans no denim" (11 Nov). Advisor row of 8 Nov 07:39: "The tailor boss is not defeated ... interim pass on the floor only".
- Garments set aside before reaching him: Sheila's skirt (failed sitting "five ways before research and twice after", production/art/clothing/sheila/README.md), her cardigan (three blind FAILs), Darren's shell-suit jacket (three FAILs, darren-shellsuit/README.md), Ron's donkey jacket (three reviews, then "failed by both allowed routes", CLOTHES.md:10), Tom's collar (four tries), Tom's surfaces (three tries, DECISIONS.md:64, 66), Sheila's collar and blouse hem (DECISIONS.md:71, 85).
- The same causes every time: "what fails is the sitting pose and the wrists in the skinned test, as on every garment before it" (darren-shellsuit/README.md, 30 Sep); in November the collar and wrist are again Kiln's open gaps ("coat blocked at the collar stand", NOW.md:14; TRIED-ARCHIVE.md:96).
- Kiln's drift (advisor rows in work/dec-E-advisor.jsonl): 13 Nov 14:19 "serves LEDGER ... never becomes its own project", share cap 15%; 13 Nov 14:36 priority over game work until Monday; 16 Nov 21:16 about 50%; 17 Nov 10:00 about 70%; 18 Nov 10:35 his goal "finish v1 of kiln so it can replace MD". RULINGS.md:39 now plans props, vehicles, buildings and streets modules after its three proofs.
- State: "Kiln v1 0 of 6" (NOW.md:14). Four garments drape in Kiln, "none in the game" (production/lane/MARVELOUS-RENEWAL-OPTIONS-2026-11-18.md, section 2). Ron's outfit alone is estimated at 17 to 21 h against n16-2's 10 h (RON-KILN-OUTFIT-PLAN-2026-11-16.md, section 2).
- Time log (a floor, it misses much): clothing tasks 79.9 of 247.4 logged hours since 5 Oct; in the weeks of 9 and 16 Nov, 44.2 of 58.8 logged hours (about 75%).

Missed check: the park rule and share cap of 13 Nov existed but nothing measured them against a person in the game. He raised the direction himself on 16 Nov ("it must turn into game progress soon").

End: ruling for him (scope). "Until one whole person passes your look in the packaged game, should Kiln (A) work only on Ron's and Tom's outfits, with M7, other garment kinds and any props, vehicles or buildings modules waiting [recommended], or (B) carry on toward v1 and M7 as now?"

### 2. An out-of-period placeholder stands in the hero frame every morning (high)

Impact: the frame he looks at daily, and judges the street by, has a modern-looking woman (striped top, skinny jeans, red high heels) posed in front of Mickey's. It breaks 1990 at a glance and is exactly the kind of thing his 4 Nov order meant.

Evidence:
- production/previews/morning-hook-day-2026-10-21.jpg and morning-hook-day-2026-11-18.jpg: the same figure, same pose, same spot, four weeks apart; dark generic figures by the phone box and on the left pavement in both.
- FINDINGS.md:16: "the street's three remaining placeholder figures (Mixamo, 23 September: Martha, Kate and Leonard ...) stand in play and in his page's frames; out of period".
- His order of 4 Nov (verdicts corner-midweek-2026-11-04): "nobody in a white base layer in any frame I see: dress them in plain period clothes we already have or Epic's ... or keep them out of frame until they are dressed".
- CLAUDE.md, the gate: "no visible fault or placeholder"; the garment list notes the three "need a crowd face and body first" (HOOK-GARMENT-LIST-2026-11-03.md:44).

Missed check: the morning-pictures step has no check for placeholders; he had to raise the white base layer himself on 4 Nov, two months after it was first seen, and the spirit of that order has not reached these three figures.

End: list item (take Martha, Kate and Leonard out of the three morning views and his page's frames now, or dress them in Ron's and Darren's released garments as variants) and rule (tools/morning_pictures.py fails when any figure in the three views has no released garment row or is on the placeholder list).

### 3. Kiln's engine carried decompiled Marvelous values while its design note said it did not (high)

Impact: licence and trust. Anything Kiln makes is meant to ship in a sold game; CLO's terms forbid reverse engineering. The design document he was shown said the risky part was kept out.

Evidence:
- TOOLCHAIN-CORE-DESIGN-2026-11-13.md:23: "Drape Studio's Python job interface is copied, not its engine ... Nothing of Drape Studio's engine, presets or files is copied: its own log says it decompiled Marvelous and copied 59 of its preset values".
- DECISIONS.md:34 (10 Nov): Drape Studio built "decompiling it and taking 59 of 82 values from Marvelous's preset files; CLO's General Terms forbid reverse engineering".
- DECISIONS.md:358 (18 Nov 03:13): "Kiln's engine is the Drape Studio engine, while his licence item says only names are reused"; :359 his page item corrected; :364 "58 rows"; :402 "All 58 decompiled values replaced"; :423 leg start values "stay borrowed, labelled STILL NEEDS RE-SOURCING".
- His word of 10 Nov ("Drape Studio is its own tool ... don't ask about licenses") and his outside-only rule of 17 Nov both bear on this; RULINGS.md:83 keeps the licence judgement his.

Missed check: the 13 Nov design note had a fresh review (TOOLCHAIN-CORE-DESIGN-REVIEW) that did not compare its claim with the code; a lane found it five days later. The studio did catch it, not him, but only after Kiln had become the main item.

End: rule (any tool whose output may ship gets a lineage note, where each part's code and values came from, checked against the code by a fresh reviewer before its output is adopted; nothing Kiln makes enters garments.json while any value is marked borrowed).

### 4. Nothing made in Marvelous has been exported, and the month ends about 25 Nov (high)

Impact: Tom's outfit, the only full outfit the game has, was drafted and draped in Marvelous; its project files cannot be opened after the month lapses. This is the one certain loss.

Evidence: production/art/clothing/LOG.md:14-16, "Exports before a Marvelous month ends: None yet" (last edited 2 Nov); MARVELOUS-RENEWAL-OPTIONS-2026-11-18.md section 2: "This is the one loss that is certain if nothing is done", safe last day "Tuesday 24 November"; RULINGS.md:83 "Everything exported to F: before any month ends". Marvelous drapes exist for Tom's jeans, jumper and zip jacket (DECISIONS.md:428).

End: list item (export every Marvelous garment kept, with pattern, fabric and UV files, to F:\LedgerTools\garments by 23 Nov, listed in LOG.md's export section, independent of Thursday's Kiln result).

### 5. Two bars for clothes are in force at once, and KCD2 is now the bar (high)

Impact: the studio recommends a yes on the low bar and he rejects on the high one. Every look costs him a round.

Evidence:
- RULINGS.md:82: "Clothes are the one exception to the visual bar ... Their floor: plain, period-plausible ..." RULINGS.md:83: "the tailor boss falls only when a garment set passes the 2026 bar close up". CLOTHES.md:5 repeats only the floor.
- The 8 Nov page item recommended yes because "they meet the clothes' floor ... which your rulings set for clothes instead of the 2026 bar" (items/dressed-men-look-2026-11-08.json); he passed it as "Interim". On 11 Nov his no on Tom named surface quality (no cloth texture, no denim), which the floor does not mention.
- Reviewers had passed the boots "with shortfalls" after "slippers at distance, 30 Oct" (LOG.md:12); he then saw "rubber slippers".
- His 18 Nov direction: KCD2 is the bar for immersion (RULINGS.md:53). Garment targets still come from Mafia's own files (Study 6 triangle counts, RON-KILN-OUTFIT-PLAN line 5: "Kingdom Come II not consulted for this plan"); under his 17 Nov rule such numbers are leads, not evidence.

End: ruling for him (scope). "For the principals at talk distance, which bar should clothes be judged on: (A) the 2026 bar close up, KCD2 frames beside, now [recommended]; (B) the floor until Kiln ships, the 2026 bar later; (C) the floor for everyone?"

### 6. Frozen faces fail their own casting sheets, and one sheet was edited to fit the game (medium)

Impact: canon's people (canon.md:77-79) are meant to look like their sheets. Two of the three principals do not, and nobody has a plan to close it.

Evidence:
- RULINGS.md:73: "Faces are frozen: Ron P2, Sheila S4 with its hair, Darren S6 ...; 8 Oct: Tom L1".
- FINDINGS.md:13: "Sheila's and Darren's faces still fail their sheets (eyes green, Sheila's lean East Asian from the front, the haircuts); their rebuild follows research." No order since 25 Oct carries that rebuild (orders 2026-10-25.md:377 set it aside).
- CATALOGUE.md:31: Sheila's face "has short dark hair and no spectacles against her sheet's greying set and spectacles on a chain"; the 11 Nov film shows exactly that (previews/sheila-held-film-2026-11-11c.jpg). Her spectacles have been held since 30 Sep because they "sit 2 to 3 cm high" (garments.json, SheilaSpectacles).
- Tom L1: the fresh reviewer of 8 Oct said no take "could stand as Tom in a 2026-grade game today" (casting/tom-nowak/CLOSEST-2026-10-08.md, section 3); he then said "Face and hair good" on 11 Nov.
- Ron's sheet was changed to match what passed: "jeans. (Jumper and jeans as Jafar passed them in the game, 8 Nov ...; the sheet's first wording was ... dark grey work trousers.)" (casting/ron-kirby/SHEET.md:13), while order n16-2 asks for work trousers. The three principals' sheets have no approval file at all; approvals.py lists all three as "NO APPROVAL".

He raised the first mismatch himself on 25 Sep ("face in game looks nothing like concept art") and Darren's hair on 29 Sep ("woman's haircut"); the check that should have caught both is the gate's own first step, the face against the casting sheet, before his page.

End: list item (one page item: Sheila and Darren as whole people beside their sheets, with keep the face and amend the sheet, or rebuild, recommended per person) and rule (a casting sheet, being the home of the cast, is never edited to match what was made without his yes; tools/approvals.py fails rather than flags a principal with no current approval).

### 7. Tries past two, and the attention they cost him (medium)

Impact: repeated third, fourth and fifth tries on small faults ate hours and his taps, while the large faults stayed.

Evidence: page items asking him for extra tries between 1 and 9 Nov, all on art: pale-line-further-try, collar-fourth-try ("One try, about 2 hours; if it fails, leave it"), boots-sole-fourth-try, tom-crown-third-try, darren-fit-third-try, boots-fifth-try (answers/INDEX.md). LOG.md:11 on Tom's jeans: "a third without asking (his rule broken)". Tom's crown: "four tries failed" (FINDINGS.md:23). Houdini Vellum third try on his yes (DECISIONS.md:112). The rule of 7 and 9 Nov (RULINGS.md:27) now stops the asking, which is right; nothing counts tries per fault kind across methods, so the collar and wrist fault started again at try 1 in every new tool.

End: rule (one fault ledger per fault kind, sitting, wrist, collar at the neck, layer through layer, carried across methods; a new method is first shown on those cases before any other work).

### 8. The clothing records contradict each other and the game (medium)

Impact: sessions and helpers start from the wrong brief; he reads stale states.

Evidence:
- CLOTHES.md is the 7 Oct text (last commit 8f67c56c9, 7 Oct): "Blender only", Marvelous "retired", state "failed by both allowed routes"; NOW.md still points n16-2 at it ("Ron as one complete person (CLOTHES.md)").
- Order n16-1: "The breadth set's six patterns made in Marvelous before 26 Nov" (orders/2026-11-16.md), against his pick A of 16 Nov 12:24 (own pattern tools, KILN-EVALUATION, last section).
- RULINGS.md:84 "stopped: procedural tailoring ..." and CLOTHES.md:5 "Tailoring waits", while Kiln drafts FreeSewing patterns and drapes jackets as the week's main item (the trace's row on this holds).
- CATALOGUE.md:31 and FINDINGS.md:23 still say the cast wear the white base layer, while garments.json released Ron's and Darren's clothes on 8 Nov (only Sheila's are held).
- production/specs/in-game.json: the player, Tom, is not among the placed things (only a backup line); Ron's and Sheila's voices still named as July and Nano although both moved to Pocket on 26 Oct.
- Darren's garment body: CLOTHES.md:9 "MH_SamC5"; DECISIONS.md:172 "Darren's jacket on S6 (his garments' body), not C5".
- LOG.md, "one line per garment", stopped on 2 Nov; nothing from Sheila's refit, the breadth set or Kiln.

End: list item (rewrite CLOTHES.md as the live clothing brief, current state and bars; add Tom to in-game.json; correct n16-1's wording) and rule (an item's brief file is touched in the same commit as any change of its route; tools/doc-caps.py or catalogue.py fails when NOW.md names a brief older than its item).

### 9. What is missing for KCD2-grade people (medium)

Impact: KCD2's immersion rests on many distinct, period-dressed, believable people. LEDGER has four, none finished.

Evidence:
- Faces: only four cast MetaHumans exist in any file (MH_TomL1, MH_RoccoP2, MH_LenaS4, MH_SamS6; no other MH_ name in the repository). RULINGS.md:73: the other eleven sheets "approved as text; their faces cast in MetaHuman from them": none done in eight weeks.
- Residents: "38 of the simulation's 41 residents are never drawn" (CATALOGUE.md:32). The garment list needs about 30 named people dressed, 77 h estimated, records running "2 to 4 times estimates" (HOOK-GARMENT-LIST-2026-11-03.md:9, 55-56).
- Bodies: four; "Slim, Average and Heavy builds are set aside"; one crowd body per sex (aaa-s06-04) not done (HOOK-GARMENT-LIST:43, 51).
- Crowd look: the 21 Sep commission of character concept sheets (docker, market trader, clerk, copper, cab controller, young man) is lost (DECISIONS-TRACE.md:23; confirmed, nothing commissions them).
- Hair: nothing on production/art/hair-2026-09-29/PASS-LIST.md has passed.
- Surfaces: one garment material with tint, grime and wet (aaa-s06-03) is not built; his 11 Nov no was about surfaces.
- The professional baseline he chose on 13 Nov (Epic's Panel Cloth and Chaos resizing in Kiln's acceptance suite) is in no Kiln file (lost, as the trace says; KILN-PARITY-LIST and kiln_items.json name neither).

End: list item (a costed people plan for the Hook: faces, bodies, hair, wardrobe and surfaces per person, cheapest proven route first, to his page as one scope item once item 1 is answered).

### 10. The cost of a person is not known (low)

Impact: he cannot weigh routes or scope without it; the 1 February scope test (RULINGS.md:15) needs cost per piece.

Evidence: Ron's cost table ends "No grand total is given"; body, hair, boots, reviews, helpers' hours and his minutes "not recorded" (ron-whole-person/RON-COST-TABLE-DRAFT-2026-11-09.md, Totals). Tom's four garments 16.7 h by 1 Nov, called floors because "the log held only about half the running hours" (LOG.md:5-12). 43 automatic "n16-1 session startup (auto)" entries, about 9.5 h, are booked to Kiln in production/time-log.jsonl, so Kiln's own hours are overstated and others' understated. Disk: F:\LedgerTools\garments 6.74 GB, of which Tom 5.37 GB (pc-inventory.json). Money: Marvelous $39 a month (renewal options note).

End: rule (tools/timelog.py never books automatic startups or idle windows to an item; each person's page item carries hours per part from the log).

### 11. Dead weight (low)

Evidence and safety:
- production/art/compare: 260 MB of full-size street PNGs from 22 to 23 Sep in git (largest 6.4 MB each), before the git rule of 3 Oct; the inventory marks hook-street-2026-09-22 dead. Superseded by every later frame.
- On F: and named by nothing (INVENTORY.md, PC side): garments\md_suit_jacket and garments\suit_jacket_test (suits stopped 2 Oct, RULINGS.md:84), review-faces-2026-09-26, casting-candidates. All made by the studio, none used by the game. Ron's ron_cc0_outfit and ron_plain_outfit are kept: the garment list names them for checking.
- production/art/clothing/md-suit-jacket, suit-jacket, suit-jacket-ingame-2026-10-01: a stopped route.

End: deletion (the F: folders under RULINGS.md:124, one DECISIONS line each; the git PNGs moved to F: and replaced by reduced previews, history untouched).

## What he raised that the studio should have caught first

- 25 Sep: in-game faces "nothing like concept art, clothes obviously". Check: the gate's face-against-sheet step before his page.
- 29 Sep: Darren's "woman's haircut". Same check.
- 4 Nov: nobody in the white base layer in any frame. Check: the gate's "no placeholder" rule; FINDINGS had it set aside since 25 Oct. The Mixamo three remain (finding 2).
- 8 Nov: knit "smooth, one flat colour"; the page named it, but recommended yes on the floor.
- 11 Nov: boots as slippers, no cloth texture, no denim. Check: reviewers judging at close range against photographs; they passed the boots with shortfalls after seeing "slippers" on 30 Oct.
- 14 Nov: held-back jobs "should have been by design from the start". Check: the research-first rule on how solvers are tested.
- 16 Nov: the Marvelous bridge click, "Clicked that many times in the past". Check: two-tries on the bridge start (it failed 8 and 16 Nov).
- 18 Nov: KCD2, not Mafia, is the bar; the art plans still cite Mafia first (finding 5).
