# Independent check 1 (20 Nov 2026) - LEDGER browser build in /home/claude/w3

Played by my own scripts (hc1.mjs, hc2.mjs, hc3.mjs in /home/claude/w3; logs hc1.log, hc2.log, hc3f.log here).
Stories played: S01 (New game, by hand to the office), S02 (from save S01), S03 front-up branch (from save S02).
The S03 strike branch was started but the headless page crashed when three browsers ran at once; not re-run for time.

## Verdicts

### S01 Off the ferry - THIN
- Met: control at 20.0 s, suitcase in hand. Standing still: one hint at 4.0 s ("W A S D to walk..."), none after.
  Heads turned (12 bodies flagged). Lines in passing with voice in LEDGER.mix (loud 0.6): Ada's window, Darren, Ron ("Afternoon, boss"), by 58 s.
  AI notice shown once in the first talk. Watch clock did not move in talk. Leave offered.
- Not met / weak: the first hint is a key list, not the way to Quay Street by its landmark (section 4).
  Two windows say almost the same line back to back ("...You've his walk." from Ada, then "a voice from the window above").
  June gave no line on my route up the east pavement.
  Typed talk is canned (offline: "written lines only"): "Who runs the fish dock" -> "So listen, you got a minute? No? Fair enough."; "Give me the twenty two quid you owe" -> "You get used to the quiet. You never get to like it." No sense of being heard.
  Sheila's walk-round did not start when I walked into the office: she stood at her desk ("A word, when you're ready"); after 50 s Pauline said "Talk to her [E]". Next to Sheila there was no prompt for her (only drawer/board).

### S02 The first fare - THIN
- Met: E at the driver's door, in within 1.8 s. Pauline gives the way by landmarks (Harbour Office clock, ferry landing, lamp over the door; then caff, green door, slippers on the step); R repeats it. Walsh talks from the back seat while moving (two lines). Paid "Two pounds thirty" (80p + distance), coin sound; Money page in words ("£25.80 in his pocket. £2.30 of fares..."). Chapel bell (bell:8) in the mix. Fare about 60 real s.
- Faked / failed: on accepting, Father Walsh is moved from his home (-7,-66) straight to the Infirmary (-116,53) by code (fares.js fareAccept sets P.x/P.z). The fare offer came at 3:15 of play, past "never later than 3 real minutes" (the S01 save is already at 3:10). The objective text says "[F] gets in" but the car is entered with E.

### S03 The debt book and Darren's £22 (front-up branch) - THIN, broken off the scripted path
- Met: Sheila said the fare-book line; Ledger Open/People/Day book/Money open with words. M offers nod, greeting, hard look, Oi, shove.
- Failed in my play: hard look got no answer; two shoves took no money. Darren's debt stayed £22 (state owed 2200, tin 0); no "every penny on me" line; no debt book page; Darren instead said "Saw you on Quay Street, the quay end gone midnight. Couldn't sleep either?" to his face at 11.30pm.
  Cause, in the code: game/book.js frontedUp() returns at once unless Sheila has finished all four stops and shown the debt book (x.shown); I had stood near her for about 30 s and walked out. A player who walks out early hits the same wall, and nothing tells him.
- Lies on the Ledger: Open listed "Lee Drewery owes the book £15.00 ... Closed Mon 15 Oct: Paid." and the same for Dennis, though nobody paid. Day book: "Laid hands on darren Milner. Laid hands on darren Milner." (doubled, small d).
  Money: fare book went from £2.30 to £10.28 and pocket from £25.80 to £33.78 with "Fares taken this week (1)": about £8 arrived with no fare driven and nothing said (perhaps the off-screen drivers, but shown as Tom's own one fare).
- One person within sight turned (ron, c2); belief line showed "Darren Milner knows that you gave Darren Milner a hard look."

## Code parts

1. First fare, src/fares.js + game/feel.js - THIN. Pay is a real formula (flag fall + metres). But the passenger is teleported to the pick-up on accept, and the fare's offer timing is a fixed cue from the tour flag, not a person on a routine.
2. Debt book and fronting up, src/game/book.js - THIN. Purse arithmetic is real (purse 1000p for Darren, rest stays). But it is all gated on x.shown with no feedback; any single shove pays (no nerve, no ladder: the hard look is not needed); Darren and Sheila are held in place by staging overrides; the "gather and drift back" is one scripted goToPoint.
3. Ron's ask, src/game/outfit.js - THIN. Branches (yes / no twice / away) are real state; the wait stops. Ron is placed inside the office at the mat by code when due, not walking in from the rank; staying away is a timer.
4. Hints, src/game/feel.js - REAL IN PLAY. Hints fire on standing still, once each, with a 12 s gap; nudges repeat the objective. Shortfall: the first hint is a key list, not the landmark way the design asks.
5. The story player, test/stories/play.mjs - THIN. Inputs are real key and mouse events and every frame is stepped. But walkTo plans paths with LEDGER.standable and the street graph; "heads turned" is read from internal Q.mind.look, not a rendered head; control is detected from LEDGER.G. The builder's S03 waits on Sheila by reading her position from LEDGER.G, so it never meets the early-walk-out wall I hit.

## Faults, most serious first
1. Fronting up Darren does nothing unless Sheila has finished the debt book first, and nothing says so. Repro: from save S02, Continue, walk out of the office within about 30 s, M > hard look, M > shove at Darren: no money, debt stays £22.
2. The Open page claims Lee's £15 and Dennis's £80 are "Closed: Paid" when nothing was paid. Repro: same run, L, Open.
3. Money appears without a fare (fares £2.30 -> £10.28, pocket +£7.98, "Fares taken (1)"). Repro: same run, Money page before and after the street scene.
4. Father Walsh is moved across the map on accepting the first fare. Repro: from save S01, read people.walsh before and after getting into car two.
5. The first fare comes after 3:15 of play (limit 3:00). Repro: S01 save played 190 s; offer at 194.95 s.
6. Sheila's walk-round does not start when he walks in; no prompt beside her. Repro: New game, walk to Mickey's door at (6.2,36), E, stand 50 s.
7. Typed talk answers off the point (offline written lines). Repro: talk to Darren, type "Give me the twenty two quid you owe".
8. Wrong key in the objective ("[F] gets in", it is E). Two window voices repeat "You've his walk". Doubled, small-d Day book line. Darren's "gone midnight" line at 11.30pm.
