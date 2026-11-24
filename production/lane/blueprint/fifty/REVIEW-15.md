# Review of 15 rows (BLIND-50 and FIFTY), 24 Nov 2026

Independent check against the blueprint (chapters 01 to 11, data/, temper/, what-if/) and the catalogue (CATALOGUE.md, NOTES-A, -B, -C, HIS-VIDEO). Read only.

| Row | Table status | My status | Agree | Table uniqueness | My uniqueness | Agree | Build/content agree | Evidence |
|---|---|---|---|---|---|---|---|---|
| B5 | missing (by design) | missing | yes (but not "by design") | LEDGER's own if built | LEDGER's own if built | yes | yes (BUILD) | 2.3.2 has no false details, yet no rule forbids them: its own prior-research line says "the entry omits weapon focus and contamination" and PRIOR-RESEARCH-INDEX says add both. No catalogue game shows it |
| B7 | partly | partly | yes | LEDGER's own | LEDGER's own (spread nearest KCD2, word passed person to person) | yes | yes (BUILD) | 2.4.1 "weaker with each telling"; 6.7 lies are acts the hearer remembers, but nothing says a claim Frank makes is passed on as talk |
| B10 | missing | partly | no | LEDGER's own if built | LEDGER's own if built | yes | yes (BUILD) | Same pieces as B7: 6.7 claims and lies remembered, 2.10.2 "each rival knows only what its own people saw or heard"; the missing piece (a told claim passing on) is the same, so missing here and partly at B7 is inconsistent |
| B13 | partly | designed | no | nearest GTA VI | nearest GTA VI (police record the outfit) | yes | no (table BUILD; nothing to build) | RT2-16: "one with only a description stops a man who matches two marks ... within 18 m in light 0.7"; data/police.json description_match_within_m 18, min_light 0.7, marks_needed 2; 2.6.2 nothing found gives "a name taken and a word" |
| B23 | missing (by design) | missing (by design) | yes | LEDGER's own if built | LEDGER's own if built | yes | yes (none unless wanted) | 2.15.3 "a business, never a fourth rival"; the other firm only takes and returns fares |
| B28 | partly | partly | yes | nearest Yakuza | nearest Yakuza (period shops and assets) | yes | yes (CONTENT) | 4.3.3 prices and letters-and-print price_boards exact; tills exist as places to rob (1.x hold-up) but no till sound or shop receipt |
| B37 | partly | partly | yes | also in Sleeping Dogs, Yakuza | also in Sleeping Dogs (snippet only), Yakuza | yes | yes (CONTENT) | RT2-19 "a box call costs 10p; 999 is free"; letters-and-print phone_box "LOCAL CALLS 10p"; no pips, no card boxes |
| B39 | partly | partly | yes | nearest GTA V | nearest Sleeping Dogs (radio DJ patter), GTA V (radio signal) | yes (both "nearest") | yes (CONTENT) | 5.7.1 "Named only; not designed beyond"; sounds.json has amb_radio_* loops only, no bulletins |
| B48 | missing | missing | yes | LEDGER's own if built | LEDGER's own if built | yes | yes (BUILD) | BLUEPRINT-11 gap: the returning-people pool (S24) "no part holds it yet"; temper grudge and STORY-05 are words only |
| B50 | missing | missing | yes | nearest KCD2 | nearest Sleeping Dogs (cups left after use), KCD2 (wear by use) | yes (both "nearest") | yes (CONTENT) | map.json places static litter; 5.3.2 wear is seeded, "placing it by use is not yet stated"; no sweeper anywhere |
| F1 | designed | designed | yes | also in GTA VI, RDR2, KCD2; cab rule LEDGER's own | also in GTA VI, RDR2, KCD2; the car is recorded in GTA VI too | yes (cab note too strong) | n/a | 1.4.4 and 2.2.5 "a deed from the car always names the car"; GV-02 coat shed for witnesses who have not told; NOTES-A GTA VI row 2 records "outfit, weapons, vehicle" |
| F6 | designed | designed | yes | LEDGER's own | nearest GTA VI | no | n/a | TEMPER-MODEL section 7: "Ada reports ... Darren keeps quiet, folds to a word, takes the money ... Grace reports and refuses everything"; NOTES-A GTA VI row 8 "personality traits (temperament, aggression)" make NPCs react differently |
| F18 | designed | designed | yes | nearest KCD2, GTA V | nearest KCD2, GTA V | yes | n/a | 2.4.3 ladder notice to confront, posture first, a told version never above a seen one; data/lines/ |
| F21 | designed | designed | yes | nearest GTA VI | nearest GTA VI (hollow or solid stars) | yes | n/a | 6.2.1 and 2.3.2 "sure", "thinks so", "guesses"; ledger-texts.json sure_level values |
| F23 | designed | designed | yes | LEDGER's own | nearest GTA V | no | n/a | 6.1.5 "no screen clock. N raises Frank's watch ... Harbour Board ... chapel bell"; NOTES-B GTA V "phone shows the time matching building clocks" and church bells ring near their buildings |

Agreement: status 13/15 (B10, B13 differ); uniqueness 13/15 (F6, F23 differ). Build/content: agree on all 10 rows the table marks not designed, except B13, where my status leaves nothing to build (9/10).

## Errors seen in passing

- B5 and the header's "by design, no" for it: no ruling rules out false details; the blueprint's own research note argues for adding contamination. It is an open gap, not a choice.
- B13 being designed changes the BLIND-50 counts (designed 15, partly 23) and removes 13 from the list of 18 BUILD items.
- B39's "world music designed" overstates 5.7.1, which says "Named only; not designed beyond".
- F6 says "three neighbours" at one beating; the source is a town-wide side-by-side test at "the same wounding", not three neighbours.
- F23 cites data/tune.json, which holds the clock rate, not the watch, clock faces or bell.
- data/police.json key sees_tom_when (and the catalogue) still use the old name Tom for Frank.
