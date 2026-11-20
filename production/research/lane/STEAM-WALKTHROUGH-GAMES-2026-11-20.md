# What players say about the walkthrough games: Steam reviews (20 November 2026)

Advisor 273 (his words, 18:08, 20 Nov: "Run the other steam studies now so we don't wait on monday, then they're all done"). The same method as the GTA V and RDR2 pull of the same day (PLAYERS-KCD2-GTAV-RDR2-2026-11-20.md on lane-2026-11), run on every other game the walkthrough studies use. Each game is coded twice: the players study's theme list, and what reviewers say about the mechanic the game is studied for.

## The games

Twelve were named; GTA V is done, and GTA IV and Sleeping Dogs are on both lists, so nine different games. Mafia: Definitive Edition was left out by his ruling (14:30, 20 Nov, advisor 269 and 274: no Mafia game is a reference for LEDGER), so it is neither pulled nor coded nor compared. The Getaway and Driver: San Francisco could not be pulled from Steam. Six games remain.

| Game | Studied for | Steam app | Steam release used | State |
|---|---|---|---|---|
| Sleeping Dogs: Definitive Edition | driving, fists, on foot, chases | 307690 | 8 Oct 2014 | coded, checked |
| GTA IV (The Complete Edition) | driving, fists, on foot, chases | 12210 | 2 Dec 2008 | coded, checked |
| L.A. Noire | chases, driving | 110800 | 8 Nov 2011 | coded, checked |
| Hitman: World of Assassination | being seen | 1659040 | 20 Jan 2022 | queued |
| Mafia: Definitive Edition | - | 1030840 | - | left out by his ruling |
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

## Remaining steps (the session's working list, 20 Nov 20:50; removed when done)

Advisors 273 then 276 (his asks tonight, ahead of the rest): (a) restart the pulls in the background: sh F:/LedgerTools/steam-reviews/pull-walkthrough.sh (skips games already pulled; left: Hitman WoA, Watch Dogs: Legion, FH4), then sh F:/LedgerTools/steam-reviews/pull-kcd2-after.sh (KCD2 1771300, never on this PC); then delete the Mafia placeholder. (b) Each pulled game: steam_review_mech.py <reviews.jsonl> walkthrough/<key>-mech.json --mech <its list> (lists in steam_walkthrough_tables.py); 'sample <key> <jsonl> check-<key> 80 <seed> --mech ...'; a research-reader (Sonnet) with HAND-CHECK-BRIEF-WALKTHROUGH.md; 'score check-<key> --mech ...' appended to walkthrough/checks.md. (c) All six coded: tables into the study, each game's mechanic findings beside its walkthrough study (feel-2026-11-20/*-raw.md, refmech on lane-2026-11), one fresh Opus final-reviewer, fix once, commit; rows say games done of six. (d) Story (advisor 276) for KCD2, GTA V, RDR2, SD, GTA IV, L.A. Noire, Hitman, WDL: steam_story_coder.py <jsonl> walkthrough/<key>-story.json; 'sample <key> <jsonl> story-<key> 50 <seed>'; a Sonnet reader per game with HAND-CHECK-BRIEF-STORY.md; 'score story-<key>'; write production/research/lane/STORY-PATTERNS-STEAM-2026-11-20.md on lane-2026-11 (pull --rebase; never wip or main) per the advisor's outline (per game shares among story-speaking reviews with quotes; patterns named in 5+ of 8, ranked; one- or two-game traits); push at once; row starting 'Story patterns done'. The cloud story session waits for it. RECIPE.md is at 5,996 of 6,000 words: make room before this unit's lines.
