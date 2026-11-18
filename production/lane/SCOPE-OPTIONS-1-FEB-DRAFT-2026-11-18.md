# Scope options for the 1 February 2027 check (draft, 18 Nov 2026)

Blind-spots recommendation 5: a ready answer for his 5 and 6 Nov rulings (cost per piece not clearly fallen by 1 February: scope moves first, never quality). Nothing goes to him now. Lane helper draft, reviewed 18 Nov (production/lane/reviews/REVIEW-SCOPE-OPTIONS-1-FEB-2026-11-18.md).

## The basis

- Weeks per phase: production/progress-page/progress.json, stations 5 to 10, "fc_w" (advisor's estimate, 5 Nov, re-forecast monthly, next 7 Dec). The Hook 15 to 20 W; crime and combat 6 to 8; empire 4 to 5; docks 6 to 8; story 9 to 12; release 5 to 7.
- Hours per W: about 205 main-line hours in the double week at about 170% (production/orders/2026-11-16.md, line 5), so 205 / 1.7 = about 120 h a normal week (estimate). The hours below use progress.json's planned 99 production hours a week (its phase 2 note; 99 h is CLAUDE.md's 70% production share; whether the advisor's later weeks assume it is unverified); at 120 h every hour figure rises by about a fifth and the weeks do not change. The page shows weeks only. (Changed 18 Nov 09:40 from 120 h, review point 6.)
- Where the forecast lands: phases 1 to 10 sum to 52.5 to 71.2 W from 8 Nov 2026 (progress.json, summed as index.html's forecast() does): 11 Nov 2027 to 20 Mar 2028. The target, 30 Nov 2027, is 55.3 W away, so the slow end is about 16 W (about 1,600 h) over.
- tools/lane/forecast.py is not used: 95% of logged hours carry no item code, so its P50 and P80 are not yet honest (production/lane/B12-FORECASTING-METHOD-2026-11-17.md).
- No named person's cost is measured yet (progress.json, "person_hours": null), so every saving is an estimate.

## Lever 1: release length (now 15 to 20 h, RULINGS 28 Oct)

Method: the story phase (9 to 12 W) scales with play length, taken at the middle, 17.5 h. Empire and release testing would shrink too; not counted.

| Option | Saving | The player loses | Canon |
|---|---|---|---|
| 15 to 20 h | 0 | nothing | none |
| 10 to 12 h | keeps 11 / 17.5 = 0.63; saves 0.37 x 9 to 12 = 3.3 to 4.5 W, 330 to 450 h (est.) | fewer jobs and side stories; acts shorter, all three acts and rivals kept | none (his ruling changes) |
| 6 to 8 h | keeps 0.4; saves 0.6 x 9 to 12 = 5.4 to 7.2 W, 530 to 710 h (est.) | at that length a rival's squeeze or an ending path likely goes | TOUCHES CANON: OPEN 2 fixes the three acts and three rivals as baseline; needs his canon call |

## Lever 2: named people (now 44: 14 principals, about 30 regulars; progress.json, RULINGS 30 Sep)

Method: the Hook's 15 to 20 W also holds one block, the 50 to 100 residents and load tests. The named people's share is taken as one half to three quarters (estimate), split evenly: 0.5 x 15 / 44 = 0.17 W to 0.75 x 20 / 44 = 0.34 W, so about 17 to 34 h a person. Canon names exactly 14 (canon.md, Premise and cast, Tom counted), so every cut falls on regulars.

| Option | Saving | The player loses | Canon |
|---|---|---|---|
| 44 | 0 | nothing | none |
| 30 | 14 x 0.17 to 0.34 = 2.4 to 4.8 W, 240 to 480 h (est.) | about half the regulars: fewer faces who know Tom by name, thinner gossip | none (his 30 Sep "thirty regulars" changes) |
| 20 | 24 x 0.17 to 0.34 = 4.1 to 8.2 W, 410 to 810 h (est.) | all but about 6 regulars; the street feels thin; the empire has few people to recruit | MAY TOUCH CANON: OPEN 2 also fixes "the empire roster"; needs his canon call |

## Lever 3: guns after melee (now "rare guns", last, after melee works; RULINGS 28 Oct and 12 Oct)

Method: the forecast gives crime, melee and guns 6 to 8 W together, not split. Guns' share taken as one third to one half (estimate): 2 to 4 W, 200 to 400 h. The combat options file costs option A's guns at 6 to 10 agent weeks after melee (production/lane/COMBAT-END-STATE-OPTIONS.md, estimate): 590 to 990 h if an agent week is one W (unverified). So the forecast is likely short on guns and the real saving larger.

| Option | Saving by release | The player loses | Canon |
|---|---|---|---|
| In for release | 0 | nothing | none |
| After release | 2 to 4 W against the forecast (est.); up to 6 to 10 W by the combat file | the top rung: no drawn gun, no town-wide shot; fists and improvised weapons carry the game | none (D24 "not a shooter" holds) |
| Never | same by release | the same, for good; the approved July weapons spec's firearms phase dropped | none, but his 28 Oct ruling and the July spec change |

## Lever 4: the docks (RULINGS 28 Oct: cut first)

| Option | Saving | The player loses | Canon |
|---|---|---|---|
| In | 0 | nothing | none |
| Cut to the first update | 6 to 8 W, 590 to 790 h (progress.json, station 8) | the second district; the Widow's syndicate acts from off the map | none: the Widow and her syndicate stay; canon names no docks district |

Docks out alone brings the forecast to 46.5 to 63.2 W: 30 Sep 2027 to 24 Jan 2028, the middle on target (27 Nov 2027), the slow end about 8 W over.

## Recommended mix

Docks to the first update (settled by his ruling, told not asked), guns after release, 30 named people, length kept. Saving 6 + 2 + 2.4 = 10.4 W to 8 + 4 + 4.8 = 16.8 W (est.): the slow end lands between 54.4 and 60.8 W, late Nov 2027 to early Jan 2028. If the trigger number is 0.9 or worse (cost hardly fell; the 0.9 is an estimate), add the 10 to 12 hour length.

## The page (shown on 1 Feb only if the trigger fires)

**LEDGER: scope, 1 February.** Repeat people still cost more than half as much as the first, so by your rule scope moves, never quality. The docks move to the first update, as you ruled on 28 Oct.

Opening sentence if no second complete person is measured by 1 Feb (review point 7): "**LEDGER: scope, 1 February.** No second person is finished yet, so repeat cost cannot be shown falling; by your rule scope moves, never quality."

Docks line (review points 8 and 9): the docks sentence above stands only if the middle of the 1 Feb re-forecast lands more than about 4 weeks after 30 Nov 2027 (today about 6.5 weeks; this is not progress.json's behind_w, which measures phases against PLAN.md and reads -0.5 weeks, so both numbers have a job: cost per piece decides whether the page goes up, lateness decides whether the docks are told or asked). If the forecast is on time, the docks take the length line's place: "3. Docks: first update (RECOMMENDED; saves about 6 to 8 weeks) / in for release.", and length stays at 15 to 20 hours unasked (the recommendation, no change to his ruling), so the page keeps to three one-line decisions (CLAUDE.md, his page).

1. Guns: after release (RECOMMENDED; saves about 2 to 4 weeks, likely more) / in for release / never.
2. Named people: 30, cutting regulars only (RECOMMENDED; saves about 2 to 5 weeks) / keep 44 / 20 (touches canon).
3. Length: keep 15 to 20 hours (RECOMMENDED) / 10 to 12 hours (saves about 3 to 4 weeks) / 6 to 8 (touches canon).

All three recommended: release at the slow end about late November 2027 to early January 2028.

## Trigger line

The page goes up if, on 1 Feb 2027, the logged hours of the second complete named person (Darren or Sheila, packaged and passed, from "person" tags in production/time-log.jsonl) divided by Ron's are above 0.5 (borrowed from progress.json's proposed "half or less" target for The Second Suit, which measures a repeated garment, Sheila's clothes against Tom's first, not a whole person; estimate), or if no second complete person is measured by then. Before showing it, every saving above is re-worked from the latest monthly re-forecast and, once measured, from Ron's real hours.

## Open questions

- progress.json's 1 Feb check uses a different number: "more than about 4 weeks behind". Proposed (18 Nov 09:40): cost per piece is the page's trigger (his ruling's words); the 4-week lateness decides only whether the docks are told or asked (see the docks line under the page). The main session rewrites progress.json's check note to name the re-forecast against 30 Nov 2027, not behind_w, when it merges. The main session lines up progress.json's check note with this when it merges.
- The 0.5 threshold is proposed, not ruled.
- Guns are probably under-counted in phase 6's 6 to 8 W.
