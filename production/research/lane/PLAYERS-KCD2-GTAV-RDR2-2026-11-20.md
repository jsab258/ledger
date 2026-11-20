# PLAYERS, redone: what players praise and punish in KCD2, GTA V and RDR2

20 November 2026, the lane (players study, Opus). KCD2 means Kingdom Come: Deliverance II, GTA V means Grand Theft Auto V and RDR2 means Red Dead Redemption 2. This replaces the Mafia half of production/research/aaa-reference/PLAYERS.md (12 Oct 2026) after his words of 14:30 today: Mafia is no longer a reference game, so it is left out entirely. Marks: every count is a site's own figure (Metacritic, OpenCritic, the 12 Oct Steam study), a helper's coding count over the reviews read, the check coder's count, or my own arithmetic; where it is not plain from the sentence, it says which. Nothing from any game is in this file: no game text, picture or audio, and no raw review text; only counts and short quotes (under 15 words, at most two players per theme). No GTA VI story detail appears anywhere.

**Updated 20 Nov 2026, evening, on the production PC (advisor 271, his words 16:46):** GTA V and RDR2 now rest on about 10,000 English Steam reviews each, pulled and coded the 12 Oct way and checked by hand; the tables, the plain-words summary, the trust section and 'What this changes for LEDGER' are redone from them. The first pass (Metacritic, OpenCritic) is kept only where marked.

## In plain words

What players of these three games care about most, in order (Steam reviews for all three, from 20 Nov for GTA V and RDR2):

1. A story and characters worth caring about. First in all three games, and strongest in RDR2, where almost half of the reviews kept praise it.
2. A world that feels alive and lived in. Second overall, ahead of looks once GTA V and RDR2 are read on Steam.
3. How it looks. Third; RDR2 above all.
4. Then, far behind: plenty of game for the money, side stories, music and sound, a good PC version, driving and riding (GTA V). Freedom to play (sandbox, heists) is large in GTA V (15%) and RDR2 (9%); never coded for KCD2, it is not ranked, though under the rule used for KCD2-only themes it would be joint fourth (7.9%).

What they punish most, in the reviews read:

1. A bad PC version (stutter, crashes, long loads, heavy demands) and bugs that stop progress or break the illusion, level across the three games: the PC version leads as drafted (10.2% against 9.7%), bugs lead if the Rockstar games are counted over all their reviews as KCD2 is (8.4% against 7.6%). The PC version is first within GTA V and within RDR2 under any count, and worst in the launch months (RDR2's December 2019 Steam launch above all).
2. Boredom, and missions that waste time or fail you for doing it your way (both over-counted by the script on the check sets; rough).
3. KCD2's combat (a KCD2 complaint; not coded for the other two).
4. The same loop over and over.
5. Slow controls, menus and animations: eighth by the script's count across the three, second in the script's RDR2 count once the miscounted story row is set aside, and equal with the PC version in RDR2's hand check (10 and 10 of 68 reviews kept, too few to separate); the script under-reads it.

The script's "a thin story" row is not trusted: in RDR2's hand check the script gave it 11 times where the reading gave it once.

The biggest change from this afternoon's version: on Steam the PC version and bugs lead the complaints, and slow controls fall from first across the three games to close behind the PC version in RDR2. The recommendation on how quick Tom feels in the hands stands, and the PC-version lesson becomes the plainest one: a bad PC version is the complaint named most often in the Rockstar reviews, worst at launch.

How far to trust it: about 10,000 Steam reviews per game, coded by a word-list script rebuilt from the 12 Oct method (differences listed below) and checked against fresh hand readings of 100 per game. It is more precise than the 12 Oct script (61 against 53 of 100 tags right) but finds fewer of the hand tags (58 against 65). The praise order is solid (0.83); the punish order is rough as a whole: rank agreement 0.28 for RDR2 and none to speak of for GTA V (too few hand complaint tags; 0.48 pooled).

## What was read, and how far to trust the counts

- **Steam, reached from the production PC (20 Nov, 16:55 to 17:55).** Steam's old review address (store.steampowered.com/appreviews) was retired by Valve on 22 Oct 2026 and now redirects to the store front, which is what the cloud run met. Valve's replacement, IUserReviewsService/GetAppReviews on api.steampowered.com [ST-API], takes the same filters, needs no key, and answered from this PC. Pulls: one request at a time with a 3 to 8 second pause, English only, every purchase type (1,259 GTA V and 744 RDR2 reviews are by non-Steam buyers), Steam's default review-bomb filter left on; the five kinds of pull of PLAYERS.md: the most helpful of all time (600 a vote), the 500 most recent of each vote, the most helpful of the past 365 days (300 a vote), the most helpful per week for the first five weeks after the Steam release (100 a week a vote), and a monthly fill (GTA V 30 a month a vote over 139 months, RDR2 50 over 84, so each lands near 10,000 without one game dwarfing the other). Overlaps removed by review id. Raw text only in F:/LedgerTools/steam-reviews, outside the repository. Script: tools/steam_reviews.py on wip.
- **RDR2's Steam release is 5 Dec 2019**, a month after its PC release on Rockstar's own launcher (5 Nov 2019). The first four weekly pulls from 5 Nov found nothing; the fifth (3 to 9 Dec) found 100 a vote, kept in the sample; the five weeks were then pulled again from 5 Dec. So RDR2's weekly pulls fetched 600 a vote and its first Steam week is sampled twice.
- **Steam's totals (English, read 20 Nov):** GTA V 544,042 positive, 105,403 negative, 649,445 in all, Very Positive, 83.8% positive; RDR2 313,312 positive, 26,966 negative, 340,278, Very Positive, 92.1% positive [ST-API]. KCD2 (12 Oct): 92.9% positive.
- **How many.** GTA V: 10,334 different English reviews, 5,234 positive and 5,100 negative, written 13 Apr 2015 to 20 Nov 2026. RDR2: 10,154, 5,123 positive and 5,031 negative, written 5 Dec 2019 to 20 Nov 2026. KCD2 keeps its 12 Oct sample (5,701, 3,112 positive and 2,589 negative).
- **Set aside, on two grounds.** (a) Reviews whose only clauses are about GTA Online or Red Dead Online, anti-cheat, the launcher, accounts or bans: GTA V 1,479, RDR2 967. (b) Reviews the script found no theme in that also hold an online word or one off-topic word anywhere (the company, mods, keys, support, refund and the like): GTA V 2,337 (1,845 of them naming the game somewhere), RDR2 1,430 (988). In all GTA V 3,816 of 10,334 (37%), RDR2 2,397 of 10,154 (24%). So about 60% of set-asides are reviews the script could not tag, not reviews with nothing to say about the game; another 1,673 GTA V and 1,167 RDR2 untagged reviews stay in. Reviews that mix the online side with the story game are coded on their other clauses only: GTA V 2,727, RDR2 1,792. Kept: GTA V 6,518, RDR2 7,757. Shares for GTA V and RDR2 are of the reviews kept; KCD2's are of all 5,701 (no set-aside on 12 Oct). On the same check sets the hand reader set aside 58 of 100 GTA V and 32 of 100 RDR2, the script 43 and 26.
- **The sample is not random**, as on 12 Oct: about as many negative as positive reviews, although the real negative share is 16% (GTA V) and 8% (RDR2). Read what is said inside each side, and the order of themes. The three games' samples are built in the same five kinds of pull, with different fill sizes (KCD2's most-helpful pull got 600 positive and 192 negative, its monthly fill up to 100), so their sizes compare better than in this afternoon's version, not exactly.
- **Median hours played at review:** GTA V positive 108, negative 155; RDR2 positive 77, negative 20 (KCD2: 127 and 42).
- **How a count is made.** A word-list script rebuilt from the 12 Oct method, because the 12 Oct script lived only in the cloud (tools/steam_review_coder.py on wip): each review is split into sentences and then clauses (at but, however, although, though, while, whereas and semicolons); a clause takes a theme when its words match; praise or complaint comes from word lists with a flip for not, never, no; a clause naming a theme with no clear side takes the review's thumb, for the themes where that is usually right, and only in reviews with no online talk. KCD2-only themes (melee, period detail, challenge, combat) were not coded for GTA V and RDR2 and count as 0 there; the first pass found them near 0 for the two Rockstar games except combat (1.5% and 3.4%).
- **Where this differs from PLAYERS.md (12 Oct):** (1) clauses, not only sentences; (2) the thumb rule only in reviews with no online talk, not in all; (3) a set-aside, which 12 Oct did not have, so the KCD2 and Rockstar denominators differ; (4) a monthly fill of 30 or 50, not up to 100; (5) tuning on 60 GTA V reviews only, where 12 Oct tuned on two sets across both games; (6) a reader model (Sonnet) as hand coder, not the session; (7) the KCD2 column comes from the 12 Oct script, whose check differs (53 and 65 against 61 and 58), so each mean share mixes two scripts.
- **The check.** A reader (Sonnet) coded by hand, blind to the script, 60 GTA V reviews for tuning, then fresh sets of 100 GTA V and 100 RDR2 reviews, disjoint from the tuning set (reviews under eight words left out). The script was tuned three times on the 60 (its last save 17:30), frozen (file hash 758ebc14 recorded at the moment of scoring, and unchanged since in its logic: only its description was brought in line afterwards), and scored once on the fresh GTA V set, then once on the RDR2 set drawn and hand-read after the freeze: of every 100 tags the script gave, 61 matched the hand reading (GTA V 59, RDR2 62); of every 100 hand tags, the script found 58 (GTA V 58, RDR2 57); set-aside status agreed on 157 of 200. Rank correlation of theme order, script against hand: praise 0.83 (GTA V 0.88, RDR2 0.82), punish 0.48 pooled (GTA V -0.19 over only 10 hand complaint tags, RDR2 0.28). The 12 Oct check gave 53 and 65, order 0.84 and 0.91. So praise reads about as well as on 12 Oct; punishment reads worse, and the punish counts below the PC version are rough as a whole. Miscounts seen on the check sets:
  - **"A thin story" (punish) is over-counted:** RDR2 script 11, hand 1; GTA V 1 and 2. Reviews that praise the story and complain of something else in the same clause are scored against the story. Its row stays in the table, marked, and is left out of the reading.
  - **"Controls, menus, slow animations" (punish) is under-counted:** RDR2 script 7, hand 10; GTA V 0 and 1. Also under-counted in RDR2: linear (0 and 4), cutscenes (0 and 3), paid extras (0 and 3).
  - **Over-counted besides story:** RDR2 boring (6 and 3) and price (4 and 1); GTA V missions (3 and 0) and the same loop (3 and 0).
- **Ranking rule.** As in PLAYERS.md: themes are ranked by the mean of each game's share of its own reviews. KCD2-only themes are ranked with 0 for the Rockstar games; freedom, coded only for the Rockstar games, is not ranked (it would be joint fourth, 7.9%, under the same rule).
- **Critics.** Unchanged from this afternoon's version: GTA V PC 8 reviews, RDR2 PC 11; Metacritic as read today: GTA V Metascore 96 from 57 critics, user score 7.9 from 9,245 ratings; RDR2 93 from 44, user 6.8 from 5,614.

### The sample by kind of pull (reviews can sit in several rows)

| Kind | GTA V positive | GTA V negative | RDR2 positive | RDR2 negative |
|---|---|---|---|---|
| Most helpful of all time | 600 | 600 | 600 | 600 |
| 500 most recent | 500 | 500 | 500 | 500 |
| Most helpful, past 365 days | 300 | 300 | 300 | 300 |
| Most helpful, first five weeks on Steam (weekly) | 500 | 500 | 600 (week 1 twice) | 600 (week 1 twice) |
| Most helpful, monthly fill | 4,170 | 4,170 | 4,200 | 4,200 |
| Different reviews in all | 5,234 | 5,100 | 5,123 | 5,031 |

Reviews by year of writing, my count. GTA V: 2015 1,437, 2016 720, 2017 757, 2018 to 2023 720 each, 2024 727, 2025 720, 2026 1,653. RDR2: 2019 806, 2020 1,392, 2021 to 2023 1,200 each, 2024 1,205, 2025 1,205, 2026 1,946.

The first pass of this afternoon (Metacritic and OpenCritic, about 800 reviews a game, helper-coded) is replaced in the tables; its notes, quotes and critic counts are kept below where they still hold, marked "first pass".

## The twenty things players praised

Counts are reviews and their share of that game's kept reviews. KCD2: the 12 Oct Steam script counts. GTA V and RDR2: the 20 Nov Steam script counts (same method, rebuilt). 'not coded (0)': a KCD2-only theme the script did not look for.

| Rank | Theme | KCD2 (Steam, 5,701) | GTA V (Steam, 6,518 kept) | RDR2 (Steam, 7,757 kept) | Mean share |
|---|---|---|---|---|---|
| 1 | A story and characters worth caring about | 1,836 (32.2%) | 1,840 (28.2%) | 3,668 (47.3%) | 35.9% |
| 2 | A living, believable world that feels lived in | 1,398 (24.5%) | 1,154 (17.7%) | 2,356 (30.4%) | 24.2% |
| 3 | How it looks | 1,015 (17.8%) | 1,071 (16.4%) | 2,395 (30.9%) | 21.7% |
| 4 | A fair price and plenty of game for it | 403 (7.1%) | 541 (8.3%) | 644 (8.3%) | 7.9% |
| 5 | Side content that are whole stories, not errands | 781 (13.7%) | 140 (2.1%) | 316 (4.1%) | 6.6% |
| 6 | Music and sound (and the radio) | 270 (4.7%) | 313 (4.8%) | 654 (8.4%) | 6.0% |
| 7 | Skill-based melee that rewards learning it | 1,009 (17.7%) | not coded (0) | not coded (0) | 5.9% |
| 8 | It ran well, a good PC version | 444 (7.8%) | 320 (4.9%) | 255 (3.3%) | 5.3% |
| 9 | Driving and riding that feel good | 37 (0.6%) | 669 (10.3%) | 378 (4.9%) | 5.3% |
| 10 | Crafting, skills, getting better at things | 508 (8.9%) | 47 (0.7%) | 81 (1.0%) | 3.6% |
| 11 | Voice acting and performances | 219 (3.8%) | 124 (1.9%) | 352 (4.5%) | 3.4% |
| 12 | Choices and roleplay that change what happens | 403 (7.1%) | 81 (1.2%) | 133 (1.7%) | 3.3% |
| 13 | Period accuracy and detail | 568 (10.0%) | not coded (0) | not coded (0) | 3.3% |
| 14 | Humour, satire and a mix of tones | 269 (4.7%) | 192 (2.9%) | 70 (0.9%) | 2.9% |
| 15 | An ending that landed | 71 (1.2%) | 102 (1.6%) | 401 (5.2%) | 2.7% |
| 16 | The world reacts to you | 168 (2.9%) | 79 (1.2%) | 167 (2.2%) | 2.1% |
| 17 | Polish: few bugs | 258 (4.5%) | 38 (0.6%) | 81 (1.0%) | 2.1% |
| 18 | The slow burn and long cinematic scenes (liked) | 195 (3.4%) | 26 (0.4%) | 131 (1.7%) | 1.8% |
| 19 | Gunfights that feel weighty | 22 (0.4%) | 124 (1.9%) | 238 (3.1%) | 1.8% |
| 20 | Challenge as a reward | 235 (4.1%) | not coded (0) | not coded (0) | 1.4% |
| NEW | Freedom to play, lots to do (sandbox, heists, three leads); not ranked | not coded | 974 (14.9%) | 691 (8.9%) | |

### Notes on the praise, theme by theme (top ten and the new one)

First pass (Metacritic and OpenCritic, this afternoon): the notes, quotes and critic counts below come from it; shares quoted inside them are that pass's, not Steam's.

1. **Story and characters.** Named more than anything in all three. RDR2 players write about Arthur Morgan, his redemption, crying, the bond with the gang; GTA V players about the three leads and the heists. Critics: GTA V 3 of 8, RDR2 8 of 11. Quotes: "Arthur Morgan is an unforgettable protagonist" (an OpenCritic player, 11 Nov 2026, RDR2); "I just love Franklin, Michael and Trevor" (a Metacritic player, 16 Apr 2015, GTA V); "characters who you actually care about, a first for me in a Rockstar game" (bit-tech, 19 Nov 2019, RDR2).
2. **How it looks.** Higher for the Rockstar games: GTA V's PC version was praised as the best looking version, RDR2's land and light. Every critic of both PC releases praises the look (8 of 8, 11 of 11). Quotes: "great radio stations and next-gen graphics" (a Metacritic player, 15 May 2015, GTA V).
3. **A living world.** About a quarter of every game's reviews. Players name people going about their day and small things happening; critics name it almost always (GTA V 8 of 8, RDR2 9 of 11). Quotes: "AI pedestrians really make the place feel alive" (a Metacritic player, 23 Apr 2015, GTA V); "people living their daily lives" (a Metacritic player, 27 Oct 2026, RDR2); "Rockstar's world-building is among the best in the business" (The Guardian, date not shown, GTA V PC).
4. **Side stories.** A KCD2 strength (13.7%); the Rockstar players name it far less (about 4 to 5%).
5. **Music and sound.** GTA V's radio and RDR2's score; almost never a complaint. Quote: "That lovely western music just fills the background nicely" (Impulse Gamer, 19 Nov 2019, RDR2).
6. **A good PC version.** GTA V's April 2015 port was praised in its own right (32 of 126 reviews on PC-only pages, 25%); RDR2's was not (16 of 201, 8%, mostly after patches). PC-only pages here are Metacritic PC, GTA V Enhanced and Steam; OpenCritic covers every platform and is left out of these counts. Quote: "huge content and top notch optimization" (a Metacritic player, 24 Jun 2015, GTA V).
7. **Plenty of game for the money.** Steady at 5 to 7% in all three. Quote: "Worth your money and time" (a Metacritic player, 5 Jul 2023, RDR2).
8. **Melee.** KCD2 only; neither Rockstar game is praised for it.
9. **Voice acting.** Higher in RDR2. Quote: "the characters' voices will stay with me forever" (a Metacritic player, 18 Nov 2026, RDR2).
10. **Period detail.** KCD2's 15th century is praised; RDR2's 1899 is named by a few (11). For LEDGER's 1990 this is a KCD2 lesson more than a Rockstar one.
NEW. **Freedom to play.** GTA V players praise doing whatever they like, the heists with a choice of approach, and switching between three leads; critics name the heists and set pieces. Quotes: "This game is about liberty." (a Metacritic player, 3 Jul 2016, GTA V); "overall great freedom to do whatever you want" (a Metacritic player, 2 Oct 2026, GTA V).

Also worth naming: humour and satire is a GTA V strength (5.9%), and two GTA V critics say the satire wears thin or is heavy-handed. The slow burn is praised by RDR2 players who stayed: "It is a slow burner but once you get locked in" (an OpenCritic player, 13 Jun 2026, RDR2).

## The twenty things players punished

Same method. All three samples are now about half negative by design, so sizes compare across games, within the check's limits. Two rows are marked by the hand check; read RDR2's hand order beside the table: of 68 reviews kept, a bad PC version 10, controls and slow animations 10, bugs 6, the same loop 5, weak gunplay 4, linear 4, boring 3, missions 3, cutscenes 3, saves 3, paid extras 3, difficulty 3, a thin story 1, and survival, price and dated 1 each. Ten and ten of 68 are too few to separate the first two.

| Rank | Theme | KCD2 (Steam, 5,701) | GTA V (Steam, 6,518 kept) | RDR2 (Steam, 7,757 kept) | Mean share |
|---|---|---|---|---|---|
| 1 | Stutter, crashes, heavy hardware demands, a bad port | 260 (4.6%) | 736 (11.3%) | 1,139 (14.7%) | 10.2% |
| 2 | Bugs that stop progress or break the illusion | 888 (15.6%) | 347 (5.3%) | 647 (8.3%) | 9.7% |
| 3 | A story that felt predictable, cliched, rushed or thin (over-counted: RDR2 check script 11, hand 1) | 476 (8.3%) | 455 (7.0%) | 928 (12.0%) | 9.1% |
| 4 | Boring: nothing to do for minutes | 623 (10.9%) | 315 (4.8%) | 529 (6.8%) | 7.5% |
| 5 | Missions that waste time, give no direction or fail you for doing it your way | 409 (7.2%) | 436 (6.7%) | 644 (8.3%) | 7.4% |
| 6 | Combat that felt clunky or unfair | 1,182 (20.7%) | not coded (0) | not coded (0) | 6.9% |
| 7 | The same loop over and over | 385 (6.8%) | 395 (6.1%) | 398 (5.1%) | 6.0% |
| 8 | Menus, controls, camera and slow animations (under-counted: RDR2 check script 7, hand 10) | 318 (5.6%) | 167 (2.6%) | 698 (9.0%) | 5.7% |
| 9 | Too short, too expensive, not worth the price | 464 (8.1%) | 272 (4.2%) | 241 (3.1%) | 5.1% |
| 10 | Too many or too long cutscenes, a slow opening, too much talk | 612 (10.7%) | 13 (0.2%) | 63 (0.8%) | 3.9% |
| 11 | Difficulty that is wrong | 338 (5.9%) | 126 (1.9%) | 292 (3.8%) | 3.9% |
| 12 | A save system that costs time | 327 (5.7%) | 21 (0.3%) | 111 (1.4%) | 2.5% |
| 13 | Systems nobody explains | 286 (5.0%) | 12 (0.2%) | 25 (0.3%) | 1.8% |
| 14 | A world that is hollow, or whose rules change on a whim | 227 (4.0%) | 18 (0.3%) | 56 (0.7%) | 1.7% |
| 15 | Survival chores as friction | 217 (3.8%) | 16 (0.2%) | 47 (0.6%) | 1.6% |
| 16 | Paid extras, microtransactions, no story add-ons | 123 (2.2%) | 80 (1.2%) | 43 (0.6%) | 1.3% |
| 17 | Stealth that is thin or stupid | 197 (3.5%) | 7 (0.1%) | 7 (0.1%) | 1.2% |
| 18 | Linear, an empty map, an interactive movie | 115 (2.0%) | 0 (0.0%) | 24 (0.3%) | 0.8% |
| 19 | Gunplay that feels weak, or auto-aim | 28 (0.5%) | 33 (0.5%) | 100 (1.3%) | 0.8% |
| 20 | Looks poor or dated | 89 (1.6%) | 11 (0.2%) | 30 (0.4%) | 0.7% |

First pass, kept for its reading of the unhappy reviews: What unhappy players say, read inside each game (reviews scored 0 to 4, my count): GTA V, 98 reviews: too short or not worth the price 20 (mostly paying again for the 2014 console re-release), paid extras and no story add-ons 17, boring 14, thin story 12, crashes 10. RDR2, 99 reviews: boring 34, controls and slow animations 33, crashes and a bad port 32, long cutscenes and slow opening 12, bugs 10, linear 10.

### Notes on the punishments, theme by theme (top ten and survival chores)

First pass: notes, quotes and critic counts as this afternoon; their order follows the first pass, not the Steam table.

1. **Controls, menus, slow animations.** RDR2's signature complaint: forced slow walking in camp and in missions, a looting or skinning animation for every action, a horse that is hard to steer, a control scheme with many buttons. Critics agree: 9 of 11 RDR2 PC reviews fault it, and 4 of 8 GTA V. Quotes: "Every action felt painstakingly slow" (a Metacritic player, 19 Nov 2026, RDR2); "very clunky controls, movement and menus" (an OpenCritic player, 22 Oct 2026, GTA V); "Arthur is both the greatest sharpshooter and the worst horse rider" (Windows Central, RDR2 PC).
2. **Boring.** In RDR2, long rides and slow stretches; in GTA V, a sandbox that runs out. Quotes: "I stopped playing because it was sooo boring" (an OpenCritic player, 23 May 2026, RDR2); "open world full of nothing" (a Metacritic player, 6 Jun 2016, GTA V). No critic of either PC release calls either game boring.
3. **Combat.** A KCD2 complaint; in the Rockstar games the matching complaint is weak gunplay or auto-aim (RDR2 6.0%).
4. **A thin story, or leads nobody likes.** GTA V's story complaints are mostly about the three leads: hard to attach to, unlikeable, contradicting themselves. Seven more GTA V reviews say only that (coded as other), and 3 of 8 GTA V critics say it too. Quotes: "none of the three stories was interesting at all" (a Metacritic player, 27 Jan 2016, GTA V); "lacks the emotional depth and memorable moments" (a Metacritic player, 15 Sep 2026, GTA V); "I found the narrative difficult to care about." (PC Gamer, 20 Apr 2015, GTA V).
5. **Bugs.** A KCD2 complaint above all; RDR2's are mostly at the PC launch.
6. **Long cutscenes, slow opening.** RDR2: about one in ten reviews; the slow first chapter in the snow and the pace of missions. Quote: "slow and somewhat tedious pace" (a Metacritic player, 8 Oct 2026, RDR2).
7. **The same loop.** RDR2: riding back and forth between mission givers; GTA V: a sandbox that got old. Quotes: "Constantly riding back and forth everywhere gets exhausting" (a Metacritic player, 23 Oct 2026, RDR2); "fun sandbox that got old quick" (a Metacritic player, 14 Oct 2026, GTA V).
8. **Too short or too dear.** In GTA V, mostly about paying full price again for the console re-release and a story that ends; in RDR2 almost absent. Quote: "the Story is way to short" (a Metacritic player, 20 Oct 2015, GTA V).
9. **A bad port.** RDR2's PC version: 47 of 201 reviews on PC-only pages (23%), two thirds of them from November and December 2019; GTA V's PC launch drew almost none (3 of 126). Critics: 7 of 11 RDR2 PC reviews raise stability or demands, against 4 of 8 for GTA V. Quotes: "possibly one of the worst optimized games I've ever seen" (a Metacritic player, 6 Nov 2019, RDR2); "a monumental work straining against stubborn mission design and stability problems" (PC Gamer, 15 Nov 2019, RDR2).
10. **Missions that fail you for doing it your way.** RDR2 above all: a mission fails if the player strays from the script. PC Gamer and bit-tech say the same. Quote: "You can't complete a mission/quest unless you do it EXACTLY" (a Metacritic player, 5 Feb 2020, RDR2); "it really doesn't like you pushing at the boundaries" (bit-tech, 19 Nov 2019, RDR2).
11. **Survival chores.** RDR2 only (7.8%): eating, cleaning, horse care, slow looting. Quote: "Looting mechanics are tedious and inconvenient" (a Metacritic player, 1 Nov 2020, RDR2). One critic (WorthPlaying) liked the meters.

Also: RDR2 reviewers punish law that knows too much (the law identifying Arthur by magic, 4.5% punish a world whose rules seem arbitrary): "the lawmen still magically identify you as Arthur" (a Metacritic player, 26 Sep 2026, RDR2). GTA V reviewers punish the end of story add-ons after Online took over (3.3%; 17 of the 98 unhappy reviews): "no single player dlcs or updates since 2015" (a Metacritic player, 28 Feb 2026, GTA V).

## Where critics and players differ

From my reading of the critics' coding and the players' counts. First pass: the player figures in this section are this afternoon's Metacritic and OpenCritic ones; on Steam boredom is fourth, not second, and the PC version is first (see the tables).

- **Critics praise the world and the look in almost every review; players put the story first.** GTA V critics: world 8 of 8, look 8 of 8, story 3 of 8. RDR2 critics: look 11 of 11, world 9 of 11, story 8 of 11. Players: story first in both games.
- **Critics barely mention boredom; it is the second complaint of players.** No critic of either PC release calls the game boring or slow to the point of fault, while RDR2's unhappy players name boredom more than anything (34 of 99).
- **They agree on controls.** 9 of 11 RDR2 critics and 4 of 8 GTA V critics fault controls or interface, in line with the players.
- **They agree on GTA V's leads.** 3 of 8 GTA V critics fault the characters or the story's tone; players do too.
- **The port.** Critics reviewed RDR2's PC version a week or more after launch and many say the crashes were mended by then; players at launch punished it far harder (47 of 201 reviews on PC-only pages, 23%). Critics were also kinder in score: Metascores 96 and 93 against user scores of 7.9 and 6.8.
- **Same as 12 Oct.** Critics name the world reacting to you (GTA V 2 of 8, RDR2 3 of 11) far more than players do (under 1% of player reviews in both). Players notice the reaction only when it fails or seems to cheat.

## What this changes for LEDGER

Read against canon, RULINGS.md (read today) and the twenty basics. The release is a 15 to 20 hour game with one main story and two or three endings (RULINGS 28 Oct), Tom on foot in a small dense town, no stats (D11), no waypoints and few short skippable cutscenes (23 Sep).

### The story

1. **Characters worth caring about come first, and one lead beats three.** Story is the top praise in all three games on Steam and highest in RDR2, where the praise is for one man and his gang. GTA V's three leads earn praise for variety but most of its story complaints are that nobody can be attached to them (first pass; GTA V's Steam hand check holds only 2 story complaints). LEDGER has one lead, Tom, and a firm of regulars: the lesson is to spend the writing on Tom and the few people around him (Sheila, Ron, the crew) until a player would miss them.
2. **The scene a player retells.** In RDR2 it is Arthur's turn and the ending ("ending made me cry", a Metacritic player, 2 Oct 2026); in GTA V it is a heist, planned and done the player's way. LEDGER's first thirty minutes still need one scene a friend would retell (R6, P4, as on 12 Oct), and the rise needs at least one planned job that can be done more than one way.
3. **Predictable or thin.** GTA V's story is punished for tone and unlikeable people more than for its plot (first pass; the Steam script over-counts this theme and cannot say). RDR2's most loved arc is a redemption, which LEDGER rules out (D58: no redemption); LEDGER's endings have to land through cost instead, which RULINGS 28 Sep already ties to what Tom saw and heard. Players punish an ending they could not see coming from their own play (12 Oct); none of the three games is punished much for its ending (first pass; no ending complaint is coded on Steam).
4. **Cutscenes and the slow opening.** RDR2's slow first chapter and long scenes drew one review in ten in the first pass; on Steam the script under-reads this theme (RDR2 check: script 0, hand 3 of 68, about 4%), so its size is uncertain, not gone. The few-short-skippable rule (23 Sep) and a reason to go out within two minutes (the friends' plan) are right and should stay hard.

### The living world

5. **A living world is second by mean share on Steam (24%), and in the top three of every game.** It needs to read as people with their own day, which is what the Meridian Test and D25 already ask. As on 12 Oct, players rarely name the town reacting to them, critics do, and players punish law that knows too much (RDR2's law that names Arthur by magic; first pass 4.5%, but the Steam count does not show it: 0.7% by the script, 0 in the hand check). The claim check and the rule that a witness is only as sure as what they saw (30 Sep) are the answer; keep them over adding more reaction types.
6. **Missions that fail you for doing it your way are punished.** RDR2 is the warning. LEDGER's jobs (no waypoints) should accept any way of getting the result the job names, and fail only on what the town would notice.
7. **Freedom to play is GTA V's own praise** (Steam: 15% of GTA V's kept reviews, 9% of RDR2's; never coded for KCD2). LEDGER has no jump, no sandbox chaos as such, and a small map; its version is the crime layer's verbs (D56) giving the player more than one way through a job, and the town remembering.

### Feel in the hands (new)

8. **Controls and slow animations: eighth by the Steam script's mean share, joint first in RDR2's hand check.** Script: KCD2 5.6%, GTA V 2.6%, RDR2 9.0%; the script under-reads it (RDR2 check script 7, hand 10 of 68 kept, 15%), and the first pass read 23.5% on Metacritic. So it is not the largest complaint across the three games, but in RDR2, the slow, on-foot game nearest LEDGER's pace, it is close behind the PC version: equal in the hand check (10 and 10 of 68, too few to separate) and second in the script's RDR2 count once the miscounted story row is set aside; 9 of 11 RDR2 critics fault it (first pass). In the first pass about a quarter of RDR2's reviews complained of forced slow walking, an animation for every looting or skinning, and heavy controls, and 9 of its 11 critics say so. LEDGER is mostly on foot, in a small town, with object interaction as a floor (23 Sep). Nothing in RULINGS sets how fast Tom answers the keys or how long an everyday action may take. Recommended: put two numbers into the feel-targets sheet (RULINGS 17 Nov, measured from footage): the time from a key press to Tom moving, and the longest a common action (a door, a pocket, a pickup, a till) may hold control, with RDR2 as the slow end to stay inside, not past. Never force a slow walk.
9. **Survival chores.** RDR2's eating, cleaning and horse care drew 7.8% in the first pass; the Steam script finds 0.6% (hand check 1 of 68), so this is a smaller complaint than it looked. LEDGER has no meters (no stats, D11, D33, D34); keep it that way, and keep coat, pockets and storage (23 Sep) quick.
10. **Travel.** RDR2's long rides are a large part of its boredom and repetition complaints. LEDGER's town is small, and by RULINGS 23 Sep others drive the firm's cars; whatever moves Tom across the town later (the arcade car once the map grows, 17 Nov), the way between two things worth doing must carry talk, a story or a choice, never dead minutes. PLAN's phase 3 exit (at most five empty minutes in thirty) covers it; count travel time in it.

### Looks

11. **Looks matter more in RDR2 than in the other two.** Every critic of both PC releases praises the look; on Steam players name it third (RDR2 31%, KCD2 18%, GTA V 16%). Nothing changes in LEDGER's bar (the Hook sheet, 2026-grade only, judged through the game's own camera); the data only says it is worth what it costs.

### Length and price

12. **Length and price are rarely the story in these games.** Plenty of game for the money is praised by 7 to 8% in all three on Steam (fourth by mean share); complaints of too short or too dear run 3 to 8%; the GTA V complaints about price are about buying the same game again and about paid extras in Online, and RDR2 is almost never called short or dear. LEDGER's 15 to 20 hours (28 Oct) is shorter than all three; price is still not set. The 12 Oct candidate risk (price and length on the Monday risk list) stands; nothing here makes it more urgent.
13. **Updates after release.** GTA V players still punish the end of story add-ons. LEDGER plans more districts in updates after release (28 Oct); if they are announced, they must come, or be cut before anyone is told.

### The PC version (now the biggest change)

14. **A bad PC version is the complaint named most often in the Rockstar reviews read.** First within GTA V (11.3%) and RDR2 (14.7%) under any count; across the three games level with bugs (10.2% against 9.7% as counted here, bugs ahead if the Rockstar games are counted over all their reviews as KCD2 is). In RDR2's hand check 10 of 68, equal first, where the script reads it about right. It is worst at launch: of RDR2's kept reviews from its first two months on Steam (5 Dec 2019 to January 2020, 898 reviews), 42.5% punish crashes, stutter or demands, against 11.0% later; GTA V's first two months (to mid-June 2015, 717) 27.1%, against 9.3% later. The first pass's "GTA V's port drew almost no complaint" does not hold on Steam: both launches were punished, RDR2's harder; GTA V's launch was also praised more than RDR2's: 16.3% of its first-two-month reviews praise the PC version, against 11.2% for RDR2's (and 3.5% for GTA V later). (Launch months are over-sampled by the weekly pulls, so read these as inside-the-window shares.) The 60 fps line (23 Sep) and done meaning the packaged release build walked by the AI tester are the right defences; add a first-week crash and settings-reset check on a second PC before any public release.

### Things LEDGER has no answer for yet

- **A first-week check of the PC version** (point 14): with bugs, the complaint named most often across the three games on Steam, and first in both Rockstar games; no check beyond the 60 fps line and the tester's walk exists yet.
- **How fast Tom feels** (point 8): no target exists yet.
- **Music.** Music and sound is sixth in praise on Steam, and GTA V's radio is part of its identity. LEDGER has CC0 sound only (D26) and music deferred (PLAN, P18); a 1990 town with radios in its cab office, shops and cars will be judged on it. No ruling yet on what music plays.
- **Dead travel time** (point 10): no rule yet beyond PLAN's empty-minutes count.
- **Price**: still unset (as on 12 Oct).

## Not reached

- First pass only: Steam's old review address, refused by the cloud's network (403); it was also retired by Valve on 22 Oct 2026 and redirects to the store front from any network. The 20 Nov evening update reached Valve's replacement interface from the production PC; nothing in the Steam pulls was refused.
- Metacritic's current pages: every filter (negative, neutral, by score, page number) was ignored and the same recent list came back.
- GameFAQs player reviews of RDR2 on PC: the site refused the fetch.
- Metacritic's older KCD2 PC player page: no reviews in the text returned.
- RDR2's later console pages (PlayStation 4 pages 10, 19, 30, 40, 46, 54; Xbox One pages 2, 5, 7, 9, 11) and further PC pages were found by search but not read, to keep within time.
- No new KCD2 Steam pull; KCD2's numbers are those of 12 Oct.

## Unverified

- Every Steam theme count is the script's, with the accuracy given above (61 and 58 of 100 against the hand reading); none is a poll of players. The praise order is solid; the punish order is rough as a whole (RDR2 0.28, GTA V none to speak of, 0.48 pooled); two rows are marked as miscounted and four more over-counted on the check sets.
- The hand reader is one model (Sonnet), not a person; the 12 Oct check was read by the session itself. On the same check sets the hand reader set aside more reviews than the script (58 against 43 of 100 GTA V, 32 against 26 RDR2).
- Steam's review-bomb filter was left at its default (off-topic reviews left out); how many it removed is not reported by Steam.
- The first-pass notes below (helper coding of Metacritic and OpenCritic):
- The console pages were coded by the fetch tool over the whole page; two helpers reported loose coding on some lines of two RDR2 pages (PlayStation 4 page 45, Xbox One first page) and a few fields that came back out of place. Codes were read from wherever they sat in a line.
- The KCD2 shares come from a word-list script over Steam reviews; the GTA V and RDR2 shares from reading. The calibration (40 reviews) hints that the script's shares run higher; it is too small to correct by.
- Metacritic does not say how its older page order is chosen; the pages are whatever search returned.
- Critic scores marked none were not printed in the page text read; Impulse Gamer prints 5 without a scale. GameSpot's GTA V page is its console review with a PC section; it is counted as a PC review. The Guardian's GTA V review was read through inkl.
- Quotes from players are taken from the helpers' readings of the page text; a few may differ from the page by a word.

## Sources

All read 20 November 2026 (session clock, Swiss time) unless a page's own date is given. Kinds: aggregate (Metacritic, OpenCritic), official (Steam), press (critic), own count.

Steam (official; the reviews are their writers'; read 20 Nov 2026, 16:55 to 17:55 from the production PC):

- [ST-API] Valve, IUserReviewsService documentation (read in full): https://partner.steamgames.com/doc/webapi/IUserReviewsService ; the interface itself: https://api.steampowered.com/IUserReviewsService/GetAppReviews/v1/ with appid 271590 (GTA V) and 1174180 (RDR2). Raw pulls in F:/LedgerTools/steam-reviews (outside the repository); scripts tools/steam_reviews.py, tools/steam_review_coder.py, tools/steam_review_check.py, tools/steam_review_tables.py on wip.

Players (aggregate pages; the reviews are their writers'):

- [MC-G-PC] Metacritic, GTA V PC players: https://legacy.prod.metacritic.com/game/pc/grand-theft-auto-v/user-reviews and https://legacy.prod.metacritic.com/game/pc/grand-theft-auto-v/user-reviews?page=7 and the current list https://www.metacritic.com/game/grand-theft-auto-v/user-reviews/?platform=pc&dist=negative&page=1
- [MC-G-ENH] Metacritic, GTA V Enhanced players: https://www.metacritic.com/game/grand-theft-auto-v-enhanced/user-reviews/
- [MC-G-CON] Metacritic, GTA V console players: https://legacy.prod.metacritic.com/game/playstation-4/grand-theft-auto-v/user-reviews (and ?page=5, ?page=7, ?page=9), https://legacy.prod.metacritic.com/game/xbox-one/grand-theft-auto-v/user-reviews, https://legacy.prod.metacritic.com/game/xbox-360/grand-theft-auto-v/user-reviews?page=7, https://legacy.prod.metacritic.com/game/playstation-3/grand-theft-auto-v/user-reviews?page=6, https://legacy.prod.metacritic.com/game/playstation-5/grand-theft-auto-v/user-reviews
- [OC-G] OpenCritic, GTA V players: https://opencritic.com/game/163/-/user-reviews
- [ST-G] Steam, one GTA V review: https://steamcommunity.com/id/nipcon/recommended/271590
- [MC-R-PC] Metacritic, RDR2 PC players: https://legacy.prod.metacritic.com/game/pc/red-dead-redemption-2/user-reviews?page=3, ?page=16, ?page=18, and the current list https://www.metacritic.com/game/pc/red-dead-redemption-2/user-reviews?dist=negative
- [MC-R-CON] Metacritic, RDR2 console players: https://legacy.prod.metacritic.com/game/playstation-4/red-dead-redemption-2/user-reviews (and ?page=3, ?page=12, ?page=26, ?page=45), https://legacy.prod.metacritic.com/game/xbox-one/red-dead-redemption-2/user-reviews and ?page=6
- [OC-R] OpenCritic, RDR2 players: https://opencritic.com/game/3717/red-dead-redemption-2/user-reviews and ?page=2
- [ST-R] Steam, four RDR2 reviews: https://steamcommunity.com/id/bonkusdonkus/recommended/1174180/, https://steamcommunity.com/id/mjozerov/recommended/1174180, https://steamcommunity.com/id/xMakezx/recommended/1174180, https://steamcommunity.com/id/divittiwari/recommended/1174180
- [OC-K] OpenCritic, KCD2 players (calibration): https://opencritic.com/game/17486/kingdom-come-deliverance-ii/user-reviews and ?page=2

Critics (press) and aggregates:

- [MC-G-CR] Metacritic, GTA V PC critics: https://legacy.prod.metacritic.com/game/pc/grand-theft-auto-v/critic-reviews
- PCGamesN, GTA V PC, 10/10, 20 Apr 2015: https://www.pcgamesn.com/grand-theft-auto-v/grand-theft-auto-v-pc-review
- PC Gamer, GTA V PC, 92, 20 Apr 2015: https://pcgamer.com/gta-5-review
- WorthPlaying, GTA V PC, 9.2/10, 28 Apr 2015: https://worthplaying.com/article/2015/4/28/reviews/95699-pc-review-grand-theft-auto-v/
- The AU Review, GTA V PC, 8.5/10, 22 Apr 2015: https://www.theaureview.com/games/games-review-grand-theft-auto-v-pc-2015/
- Hardcore Gamer, GTA V PC, 18 Apr 2015: https://hardcoregamer.com/reviews/review-grand-theft-auto-v-pc/144928/
- Impulse Gamer, GTA V PC, 11 May 2015: https://www.impulsegamer.com/gta-v-pc-review/
- The Guardian, GTA V PC, read through inkl: https://www.inkl.com/news/grand-theft-auto-v-on-pc-review-rockstar-outdoes-itself-in-world-building
- GameSpot, GTA V (PC update 15 Apr 2015): https://www.gamespot.com/reviews/grand-theft-auto-5-review/1900-6415959/
- [MC-R-CR] Metacritic, RDR2 PC critics: https://legacy.prod.metacritic.com/game/pc/red-dead-redemption-2/critic-reviews
- PC Gamer, RDR2 PC, 88, 15 Nov 2019: https://www.pcgamer.com/uk/red-dead-redemption-2-review
- Windows Central, RDR2 PC: https://www.windowscentral.com/red-dead-redemption-2-pc-review
- bit-tech, RDR2 PC, 19 Nov 2019: https://bit-tech.net/reviews/gaming/pc/red-dead-redemption-2-review-pc/1/
- WorthPlaying, RDR2 PC, 8.0/10, 12 Nov 2019: https://worthplaying.com/article/2019/11/12/reviews/116894-pc-review-red-dead-redemption-2/
- GamingBolt, RDR2 PC, 8/10, 28 Nov 2019: https://gamingbolt.com/red-dead-redemption-2-pc-review-the-last-enemy-that-shall-be-destroyed
- Gamereactor, RDR2 PC, 9/10, 14 Nov 2019: https://www.gamereactor.eu/red-dead-redemption-2-on-pc/
- GameZone, RDR2 PC: https://gamezone.com/reviews/review-red-dead-redemption-2-on-pc
- GameSkinny, RDR2 PC: https://www.gameskinny.com/reviews/red-dead-redemption-2-pc-review-how-the-west-was-truly-won/
- God Is a Geek, RDR2 PC, 25 Nov 2019: https://www.godisageek.com/reviews/red-dead-redemption-2-pc-review
- Impulse Gamer, RDR2 PC, 19 Nov 2019: https://impulsegamer.com/red-dead-redemption-2-pc-game-review
- FutureFive NZ, RDR2 PC, 10/10, 18 Nov 2019: https://futurefive.co.nz/story/game-review-red-dead-redemption-2-pc

Within the project: production/research/aaa-reference/PLAYERS.md (method, theme list, KCD2 counts and critics), production/lane/synthesis/pack/05-players-basics.md, RULINGS.md, CLAUDE.md (all read 20 Nov 2026). The coded rows and the scripts that count them stay outside the repository, with the session.
