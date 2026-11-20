# One-shot builder "life": the town's days, lines, shops, finding the way

Branch os/life (pushed as oneshot-life). Systems: way, life, shops, under tools/lane/prototype/project/src/game/. Stopped early at 09:45 because the weekly reading (72% at 09:30, main row) reached the one-shot's ceiling (about 72%). Kept current at each checkpoint.

Tests: `node test/pieces.mjs` (8 pieces of mine, 165 cases, all pass, no browser); test/game/way.mjs (passes: 18 checks); test/game/shops.mjs and test/game/life.mjs (written; see Known faults for how far they have run).

## Parts

- 6.9 Finding the way: passes its test (way_rules cases, game/way). 61 places, each with an address, a landmark and a ground label (ER-WAY-02); asking the way in a talk; the lost nudge once after 90 s and the offer after three minutes (ER-WAY-03). Thin: ER-WAY-01 (a newcomer reaches ten places) is a hands-on check, not run.
- 2.2.6 Ground rules (labels only, for the foot builder): built shallow. Every place has its label and hours; way_rules.ground says free, private or forbidden by the hour. The warnings are the foot builder's.
- 2.1.1 Schedules of named people: built (was built). Danby and Dr Calvert added with rows that fit (tools/walk_times.mjs passes, 149 walks).
- 2.1.2 The crowd's clock windows, 3.2.4 The crowd: built shallow. life_crowd piece holds the windows (the prototype's own first values, the 1990 hours research is still owed); nobody under eighteen (a check in game/life). Test: life_crowd cases.
- 2.1.4 Weather and hour change who is out: built shallow. The same hour dry, in drizzle and in rain gives 14, 10 and 6 walkers every time (ER-NIGHT-03, life_crowd cases); in play the life system thins the walkers out of his sight to that count.
- 2.1.5 Crowd movement and avoidance: not built (routines.js is another builder's; nothing of mine changes how walkers avoid).
- 2.1.6 The town's calendar: built. calendar_days piece (32 cases, ER-CAL-01): Monday 15 October 1990, market Thursday, the match Saturday (Meridian Town, invented), Sunday shut and the chapel busy, Bonfire Night on day 21, Remembrance Sunday on day 27; each hour the calendar sends churchgoers, market-goers, the match's followers and the street to their places. ER-CAL-02: the content check runs over every line.
- 3.2.3 The thirty regulars, 3.6.3 Written street lines: built shallow. 14 regulars who had no street lines of their own now have 8 each (thirty each is the target); Philip Danby added as a person.
- 3.6.4 Crowd lines by situation: built. Five situations (bumping, neighbours, at work, rain, greeting), four kinds of speaker, six lines each (120), a line never twice in a day from one person. Thin: the "neighbours" and "at work" lines are written and not yet triggered in play.
- 2.12.4 Greetings by regard: built. Afraid, angry, likes, his appearance, neutral, each said differently at the four rungs (reads G.x.rise.rung); life_rules cases.
- 2.7.5 Purses, tills and shops, 2.7.8 Spending: built. Ten shops, each selling only its list, by its hours, from its week's stock; weekly restock on Monday; no tick (ER-SPEND-01, shop_rules 25 cases). The haggle is three offers at most, from the buyer's purse, hot goods fetch less, a refusal is remembered (ER-HAGGLE-01).
- 1.6.10 Tom's wardrobe: built shallow. Second-hand coat, donkey jacket for nights, decent jacket, good overcoat, hat and scarf, the barber; a change at the mirror in Regent House or the office; a new coat leaves a witness of the old one with a shape (ER-COAT-01, life_coat 19 cases). Thin: nothing is drawn differently on Tom; other systems read G.hooks.dress().
- 2.4.5 The paper: built. Out Tuesday and Friday at three; prints only what Alison Sedman saw or was told, at the strength she had it (ER-PAPER-01, paper_lines cases); six readers a day hold it as told by the paper; reading it writes the Ledger.
- 6.10 Letters and papers in hand: built. Letters wait at the office, open as a page, go into the Ledger; G.hooks.letter(spec) and G.hooks.postLetter(spec) for other builders (mickey, solicitor, vat, rent are written).
- 3.7 Street happenings: built. Six (the shoplifter, the bread van, the row on the step, the lost man, the loose dog, the woman locked out), each placed by a named state and the hour, never dice (ER-HAPPEN-01, life_happen cases), none twice in 30 minutes or twice a week on a street; four of them can come back days later as a favour.
- 3.3 Side stories: built shallow. Six new ones of three or four steps (the bench plate, the man in the net store, the piano for the hall, the wreath, Shaun's ladder, the keys of No. 3), each ending in a town fact. The 32 drafts of 8 Nov were not in this working copy.
- 3.2.7 Calling on people: built. Alison at Rinaldi's, Danby at home, the tea room or the bench; only when the routine allows; no score; a second call inside a day is cooler (life_rules cases).
- 3.2.5 Someone worth being honest for: built shallow. Honest visits build it; two lies end it; G.x.life.friend = { who, holds, word } and G.hooks.friend() for the endings.
- 7.16 Pastimes: built shallow. The boxing club behind the chandler's, Tuesday to Saturday evenings: three written rounds with gloves (G.hooks.spar is used instead if the foot builder gives one), or watch; no money moves (ER-PASTIME-01).
- 2.19 Lasting marks on the town: built. A forced door a day, a broken window two, tape three; G.hooks.townMark(kind, placeId) for other builders; kept in the save.
- 7.12 Always something to do: built shallow. life.somethingToDo() and G.hooks.somethingToDo(): the nearest fare, debt, person with a word, happening or story within 30 s (life_rules cases); the 20-moment probe is in game/life.
- 6.5 Teaching the player: built shallow. G.hooks.hint(id, text): once each, never two within 12 s (ER-FIRST-03, life_rules cases); only two hints of my own use it yet.

## Known faults

- game/shops and game/life have not yet run to the end: from about 09:15 the shared machine ran out of memory and killed the browsers of every builder (dmesg: memory cgroup out of memory, about one kill every 15 s). The page itself is steady (81 MB heap, no faults, through a new week and 20 s of play). First thing to do next: run both and fix what they find.
- The places' hours (way_places.js) and the older RULES.shops hours differ by up to an hour for some shops; one home is owed.
- The hat, scarf and barber change what witnesses can tie to him only through G.hooks.dress(); seeing.js does not read it yet.
- test/harness.mjs: the manager's port-shift comment had swallowed the window size on the same line (a syntax error for every test); mended here by removing the comment.

## Needs from others

- seeing (bridge): read G.hooks.dress() (catchCap, drawsALook, coat) when a watcher catches him, and stamp an event with the coat worn.
- foot: G.hooks.spar({ rounds, gloves, noFall, noBlood }) for the boxing club; the warnings for private and forbidden ground from PLACES[id].label and way_rules.ground.
- jobs: G.hooks.goodsCarried() (a list of { id, name, kind, honestPence, hot }) and G.hooks.goodsSold(id, pence, shopId) so the shop counters can buy; G.hooks.keyToCopy() for the key cut; the things bought sit in G.tom.items (torch, crowbar, padlock, cigarettes, matches, 'cut key', 'keys: No. 3').
- law: G.hooks.hasBrief() says whether a solicitor is on call; G.hooks.townMark('tape', placeId) for tape.
- spine: draw the paper map from G.hooks.placeKnown(placeId) and LEDGER.game.way.places(); post the Act III letter with G.hooks.postLetter('vat').
- rise: G.hooks.favour('harbour' | 'lift' | 'shaun' | 'norman' | 'deckhand' | 'keys3' | 'nurse' | 'yardwatched') are soft keys and leads earned on the street; G.hooks.postLetter('solicitor') for Agar's letter.
- econ: money.js pay and earn are called with a third argument (why) for the flows ledger.
