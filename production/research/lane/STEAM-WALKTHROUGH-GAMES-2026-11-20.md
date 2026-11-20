# What players say about the walkthrough games: Steam reviews (20 November 2026)

Advisor 273 (his words, 18:08, 20 Nov: "Run the other steam studies now so we don't wait on monday, then they're all done"). The same method as the GTA V and RDR2 pull of the same day (PLAYERS-KCD2-GTAV-RDR2-2026-11-20.md on lane-2026-11), run on every other game the walkthrough studies use. Each game is coded twice: the players study's theme list, and what reviewers say about the mechanic the game is studied for.

## The games

Twelve were named; GTA V is done, and GTA IV and Sleeping Dogs are on both lists, so nine different games.

| Game | Studied for | Steam app | Steam release used | State |
|---|---|---|---|---|
| Sleeping Dogs: Definitive Edition | driving, fists, on foot, chases | 307690 | 8 Oct 2014 | pulling |
| GTA IV (The Complete Edition) | driving, fists, on foot, chases | 12210 | 2 Dec 2008 | queued |
| L.A. Noire | chases, driving | 110800 | 8 Nov 2011 | queued |
| Hitman: World of Assassination | being seen | 1659040 | 20 Jan 2022 | queued |
| Mafia: Definitive Edition | driving, fists, on foot, chases | 1030840 | 24 Sep 2020 | queued |
| Watch Dogs: Legion | driving, chases | 2239550 | 26 Jan 2023 | queued |
| Forza Horizon 4 | driving | 1293830 | 9 Mar 2021 | queued |
| The Getaway | driving | none | never on PC | not reached |
| Driver: San Francisco | driving | none answers | delisted | not reached |

App ids and release dates read from Steam's store details on 20 Nov 2026, 18:15 (store.steampowered.com/api/appdetails). Driver: San Francisco's former app id gave no store page and no review count [UNREACHED].

## Method

- Pull: tools/steam_reviews.py through Valve's IUserReviewsService/GetAppReviews (the old appreviews address was retired 22 Oct 2026), English, Steam purchases, one request at a time with a 3 to 8 second pause; the five kinds of pull of PLAYERS.md (most helpful each way, most recent, most helpful in the last year, the first five weeks by week, and a monthly fill of 20 a vote); overlaps removed by review id. Steam's default filter leaves review-bomb periods out. Raw text on F:/LedgerTools/steam-reviews, never in git.
- General themes: tools/steam_review_coder.py, frozen 20 Nov 17:30 (logic hash 758ebc14), logic unchanged; its set-aside words widened at run time for these games' services (Games for Windows Live, Ubisoft Connect, always-online, the Xbox app, publisher and delisting talk) by tools/steam_review_mech.py.
- Mechanics: tools/steam_review_mech.py; a sentence naming the mechanic, its side from the same praise and complaint words, sub-points by their own words; short quotes kept.
- Check: a fresh random sample per game read by hand (a Sonnet reader, brief F:/LedgerTools/steam-reviews/HAND-CHECK-BRIEF-WALKTHROUGH.md), scored for the general themes and per mechanic.
- One fresh Opus reviewer; fixed once.

## Results

(Filled as each game is coded.)
