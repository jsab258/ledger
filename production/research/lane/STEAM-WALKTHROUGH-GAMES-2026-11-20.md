# What players say about the walkthrough games: Steam reviews (20 November 2026)

Advisor 273 (his words, 18:08, 20 Nov: "Run the other steam studies now so we don't wait on monday, then they're all done"). The same method as the GTA V and RDR2 pull of the same day (PLAYERS-KCD2-GTAV-RDR2-2026-11-20.md on lane-2026-11), run on every other game the walkthrough studies use. Each game is coded twice: the players study's theme list, and what reviewers say about the mechanic the game is studied for.

## The games

Twelve were named; GTA V is done, and GTA IV and Sleeping Dogs are on both lists, so nine different games. Mafia: Definitive Edition was left out by his ruling (14:30, 20 Nov, advisor 269 and 274: no Mafia game is a reference for LEDGER), so it is neither pulled nor coded nor compared. The Getaway and Driver: San Francisco could not be pulled from Steam. Six games remain.

| Game | Studied for | Steam app | Steam release used | State |
|---|---|---|---|---|
| Sleeping Dogs: Definitive Edition | driving, fists, on foot, chases | 307690 | 8 Oct 2014 | coded, checked |
| GTA IV (The Complete Edition) | driving, fists, on foot, chases | 12210 | 2 Dec 2008 | coded, checked |
| L.A. Noire | chases, driving | 110800 | 8 Nov 2011 | coded, checked |
| Hitman: World of Assassination | being seen | 1659040 | 20 Jan 2022 | coded, checked |
| Mafia: Definitive Edition | - | 1030840 | - | left out by his ruling |
| Watch Dogs: Legion | driving, chases | 2239550 | 26 Jan 2023 | coded, checked |
| Forza Horizon 4 | driving | 1293830 | 9 Mar 2021 | coded, checked |
| The Getaway | driving | none | never on PC | not reached |
| Driver: San Francisco | driving | none answers | delisted | not reached |

App ids and release dates read from Steam's store details on 20 Nov 2026, 18:15 (store.steampowered.com/api/appdetails). Driver: San Francisco's former app id gave no store page and no review count [UNREACHED].

## Method

- Pull: tools/steam_reviews.py through Valve's IUserReviewsService/GetAppReviews (the old appreviews address was retired 22 Oct 2026), English, Steam purchases, one request at a time with a 3 to 8 second pause; the five kinds of pull of PLAYERS.md (most helpful each way, most recent, most helpful in the last year, the first five weeks by week, and a monthly fill of 20 a vote); overlaps removed by review id. Steam's default filter leaves review-bomb periods out. Raw text on F:/LedgerTools/steam-reviews, never in git.
- General themes: tools/steam_review_coder.py, frozen 20 Nov 17:30 (logic hash 758ebc14), logic unchanged; its set-aside words widened at run time for these games' services (Games for Windows Live, Ubisoft Connect, always-online, the Xbox app, publisher and delisting talk) by tools/steam_review_mech.py.
- Mechanics: tools/steam_review_mech.py; a sentence naming the mechanic, its side from the same praise and complaint words, sub-points by their own words; short quotes kept.
- Check: a fresh sample of 80 per game (79 scored for Sleeping Dogs), half drawn at random from reviews of 8 or more words, half from the mechanic coder's broad net, read by hand (a Sonnet reader, brief F:/LedgerTools/steam-reviews/HAND-CHECK-BRIEF-WALKTHROUGH.md), scored for the general themes and per mechanic. The mechanic coder is the one committed in 68820ebcf (20 Nov 18:27, unchanged since); checks.md's heading names it "f84b50a1", a hash that could not be reproduced from the file [UNVERIFIED].
- One fresh Opus reviewer; fixed once.

## Results

All six games pulled and coded (20 Nov, 18:17 to 21:50). Full tables, sub-points and the script's sample quotes: F:/LedgerTools/steam-reviews/walkthrough/tables.md (built by tools/steam_walkthrough_tables.py); hand checks: F:/LedgerTools/steam-reviews/walkthrough/checks.md. The script's quotes are not used or relied on here: the hand checks show many are on the wrong side or off the mechanic.

| Game | Kept reviews (pulled) | Steam English count, up | Top praised themes | Top punished themes |
|---|---|---|---|---|
| Sleeping Dogs: DE | 4,932 (5,011) | 35,854, 34,327 up | story 44.8%, world 28.2%, looks 18.0% | story 10.2%, controls 8.6%, missions 7.0% |
| GTA IV | 6,328 (8,087) | 85,778, 69,935 up | story 35.0%, world 19.8%, looks 12.6% | port 25.9%, bugs 12.7%, missions 10.7% |
| L.A. Noire | 5,715 (6,676) | 19,304, 16,180 up | story 39.1%, world 21.1%, looks 15.2% | port 13.6%, story 9.8%, boring 7.1% |
| Hitman: WoA | 3,270 (3,818) | 37,156, 32,612 up | story 13.6%, world 12.8%, looks 9.5% | missions 9.0%, port 7.2%, story 4.8% |
| Watch Dogs: Legion | 2,427 (2,665) | 5,128, 2,959 up | story 25.1%, world 15.4%, looks 11.0% | story 19.6%, port 11.5%, missions 9.1% |
| Forza Horizon 4 | 3,732 (4,300) | 58,272, 52,092 up | driving 23.2%, looks 23.1%, world 12.5% | port 22.0%, bugs 4.9%, controls 3.5% |

General themes are the frozen coder's shares; its hand-checked precision here is 41 to 60 and recall 51 to 60, so they rank themes, they do not measure them.

### Mechanics: how often reviewers speak of each, and how far the count holds

"Script" is the share of kept reviews whose sentences the script ties to the mechanic (praised, punished). P and R are its precision and recall against the hand reader (a model reader; 80 reviews a game, half random, half from the script's broad net, so reviews outside the net are present but under-weighted and recall leans high). "Hand cases" are review-sides (a review praising and faulting counts twice). "Rough share" is script × P ÷ R, which equals the sample's ratio of hand cases to script cases applied to the script's share. Its sampling error is large (roughly ±18% of the value with about 30 hand cases, ±60% with a handful), larger than the lean from the net; the hand sample also leaves out reviews under 8 words, which the script's share counts. So the rough share is an order of size [UNVERIFIED beyond the sample]; with five or fewer hand cases it is shown only as "a few %" or "about 1%". Rows marked "weak" have five or fewer hand cases or precision under 35.

| Game | Mechanic | Script mention (praise, punish) | P, R (hand cases) | Rough share | Walkthrough study |
|---|---|---|---|---|---|
| Sleeping Dogs | fists | 46.4% (38.8, 11.1) | 80, 87 (38) | about 43% | feel-2026-11-20/FISTS-raw.md |
| Sleeping Dogs | driving | 22.6% (16.8, 7.8) | 59, 56 (18) | about 24% | the driving study |
| Sleeping Dogs | chases | 10.4% (8.5, 2.2) | 38, 100 (3) weak | a few % | feel-2026-11-20/CHASES-raw.md |
| Sleeping Dogs | on foot | 6.1% (4.4, 1.9) | 0, 0 (1) | not usable | feel-2026-11-20/ONFOOT-raw.md |
| GTA IV | driving | 14.8% (10.5, 5.5) | 73, 65 (17) | about 17% | the driving study |
| GTA IV | chases | 6.1% (4.1, 2.3) | 38, 75 (4) weak | a few % | CHASES-raw.md |
| GTA IV | fists | 4.1% (2.9, 1.3) | 25, 100 (1) weak | about 1% | FISTS-raw.md |
| GTA IV | on foot | 3.8% (1.6, 2.2) | 0, 0 (1) | not usable | ONFOOT-raw.md |
| L.A. Noire | driving | 11.7% (7.7, 4.7) | 31, 42 (12) weak | about 9% | the driving study |
| L.A. Noire | chases | 11.6% (8.8, 3.4) | 20, 40 (5) weak | a few % | CHASES-raw.md |
| Hitman: WoA | being seen | 17.7% (13.4, 5.9) | 55, 76 (29) | about 13% | feel-2026-11-20/SEEN-raw.md |
| Watch Dogs: Legion | driving | 7.7% (3.9, 4.2) | 65, 72 (18) | about 7% | the driving study |
| Watch Dogs: Legion | chases | 4.8% (2.8, 2.1) | 22, 100 (2) weak | about 1% | CHASES-raw.md |
| Forza Horizon 4 | driving | 36.9% (29.0, 13.2) | 33, 79 (14) weak | about 15% | the driving study |

The walkthrough studies are on lane-2026-11 under production/research/lane/feel-2026-11-20/ (Sleeping Dogs' also refmech-2026-11-20/SLEEPING-DOGS.md); they are not changed by this study.

### What it says, game by game (only where the count held)

Sides (praise or complaint) are taken from the hand reader where the script and the hand disagree; "hand" counts are review-sides in the 80-review sample, which is half from the net and so not weighted like the whole pull. Sub-point words (handling, combos, ai, camera) are the script's counts only, never hand-checked.

- **Sleeping Dogs:** the fighting is the mechanic most spoken of in this study: about four in ten reviews, mostly praise (hand: 33 praise, 5 complaint), the script's sub-points naming combos and impact most in praise, counters, combos and difficulty almost level in complaint (87, 81, 82). Driving is spoken of by about a quarter; the script puts praise ahead, but the hand sample has complaint ahead (12 against 6).
- **GTA IV:** driving is named by about one in six, praise ahead in both counts (hand 13 against 4); in the script's sub-points handling and the cars' weight lead on both sides. The PC port dominates complaint (25.9%), not any mechanic. Fists, chases and moving on foot are rarely raised.
- **L.A. Noire:** neither driving nor chases is a strong theme once corrected (under one in ten); the script overcounts both (precision 31 and 20).
- **Hitman: WoA:** being seen is raised by about one in eight, mostly in praise (hand 24 against 5); in the script's sub-points disguise and freedom are mostly praised, detection is named about evenly on both sides, and the guards' behaviour (ai) is named most.
- **Watch Dogs: Legion:** the one game here where driving is faulted more than praised: the script has it about level (3.9 against 4.2), the hand sample has only complaint (18 of 18). The script's complaint sub-points: handling 21, weight 10, camera 8.
- **Forza Horizon 4:** driving leads its praise, but the script overcounts it about 2.4 to one (33 script cases, 14 by hand; precision 33): about one in seven reviews speak of the driving itself rather than racing or cars in general. The hand reader found no driving complaint, against the script's 13.2% punished.

In the script's sub-points, handling is the most named on both sides in all five driving games. Moving on foot could not be measured: all eight of the script's on-foot hits in the two hand samples were wrong, and the hand reader found two cases in 159 reviews. Its rough share is "rare", not a number.

### What could not be reached or is weak

- The Getaway and Driver: San Francisco: not on Steam [UNREACHED].
- Moving on foot: no usable count (above).
- Five or fewer hand cases, order of size only: chases in Sleeping Dogs (3), GTA IV (4), L.A. Noire (5) and Watch Dogs: Legion (2); fists in GTA IV (1).
- Low precision (under 35): L.A. Noire driving 31 and chases 20, Forza Horizon 4 driving 33, Watch Dogs: Legion chases 22, GTA IV fists 25. These rows carry "weak" in the table.
- The hand reader is a model, not a person.
- Sub-point counts (handling, combos, ai) are the script's words only; no hand check of sub-points was made.
