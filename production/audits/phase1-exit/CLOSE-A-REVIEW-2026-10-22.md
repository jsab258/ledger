# Phase 1's close, Exit A (Mickey's front office, a frontage, three street views): the fresh review, 22 October 2026

A fresh reviewer (Opus), given CLOSE-BRIEF-2026-10-22.md and the outputs, not the maker's verdict; read only. Its report, verbatim in substance:

**Gates relied on.** For the office, GATE-1.1-REVIEW-3 (8 Oct), with GATE-OFFICE and GATE-GLASS (8 Oct) for the glass and night lighting; GATE-OFFICE says "Item 1.1 itself does not pass on this." For the frontage, gate-ritas-front/GATE.md (21 Oct). For the street views, the 22 Oct pictures themselves (no gate judged them).

**Clause verdicts.**
- From the room kit: MET (tools/art-recipes/shop-room.py, mickeys; mickeys-office.json "real_room").
- Researched first: MET (cab-office notes 30 Sep, props 6 Oct; no real 1985 to 1995 cab-office interior photograph found).
- Real glass reflecting the street: MET by day with known flaws (stepped edges, a grey ghost over the blind); at night the right half is near-black; the door glass is a coarse tan picture (tester 2026-10-08-1655).
- Radio set, kettle, telephone: MET (packaged walk-in, steps 085 and 095).
- Ashtrays: NOT SHOWN (placed in the recipe, not picked out in any picture).
- Scuffed counter and wear: NOT MET. The counter reads clean; shop-room.py line 1603 removed the counter scuffs; line 1489 leaves the props' baked wear masks out of the game.
- No glitches: NOT MET. Open: the open door's rails and gilt bar overrun the post; the wet flags glare white; small steps in the glass; and the faults below.
- Frontage geometry: MET (r5/pawnbroker-front-shop.png).
- Frontage material: partly met. The balls read matte, not gilt; at night the window burns white and the red velvet clips (set aside); close up, JPEG blocks on glossy goods (set aside).
- Frontage wear: NOT MET (the page itself says so; his "yes" was to the option "not yet 2026-grade until the wear and the night light are done").
- Window of verified CC0 goods: MET (the cloud kit's table; 8 Poly Haven source.json files checked, CC0 1.0).
- Three fixed street views: produced daily, but not at the Hook sheet's bar. Flat white puddle shapes, a toy-like hill, no parked cars, a bare sky at the street's end, and at night the right third of the frame black.

**Faults the maker's files do not name.**
- The three views do not come from the packaged build: tools/morning_pictures.py (lines 43 to 44 and 96) runs the editor in -game mode. The close brief's "made from the packaged build" was wrong.
- The packaged game looks different: the 22 Oct tester's pictures (2026-10-22-0248, steps 004 to 012) show the cast in the white base layer, where the editor views show people dressed.
- In the reverse view (21 and 22 Oct), a woman at the Ironmonger's window has a raised knee and spread arms, pressed into the glass behind the bin: a broken pose or clipping.
- No current packaged walk of the office. The 22 Oct route stops at the door, and its picture check failed ("OAuth session expired"). The last packaged walk-in is 8 Oct (62be907), before the window lettering changed on 21 Oct.
- production/art/shop-rooms/pawnbroker-goods-sources.md (6 Oct) is out of date: it lacks the boombox, the 8 mm projector, the alarm clock, the cassette player and the pocket watches now in the window.
- Inside the office (step 095), Tom's hair shows grey smeared patches.

**Not reached.** The nightly walk's 12 judged pictures (the judgement failed); the KCD2 frames.

**Verdict.** Exit A does not pass phase 1's bar: the office's wear and scuffed counter, the frontage's wear and "no glitches" are not met, and nothing current shows the office in the packaged build.
