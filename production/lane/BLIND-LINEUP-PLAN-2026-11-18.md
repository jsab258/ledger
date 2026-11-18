# Blind line-up plan (blind-spots recommendation 10, part 2), 18 Nov 2026

The question: put one LEDGER frame among six frames from released games of 2024 to 2026 and ask "which look unfinished?". If LEDGER's frame is picked, the street is not done, whatever the gate said.

## The six frames

Each is a public video found by search on 18 Nov 2026; nothing is downloaded. The moments are described scenes, not checked by eye from the cloud, so the main session picks the exact second at capture and writes it down (timestamps "unverified" until then). Spread: three big-budget (AAA), three mid-budget (AA, estimate from price and studio size).

1. Assassin's Creed Shadows (AAA). Released 20 March 2025 ([Ubisoft, 9 Jan 2025](https://www.ubisoft.com/en-gb/game/assassins-creed/news/5HGcPYPmUIQa3lVrOMJk4u/assassins-creed-shadows-now-releases-march-20-2025)). Video: Extended Gameplay Walkthrough, https://www.youtube.com/watch?v=np601BPXlac (listed by [Gematsu](https://www.gematsu.com/2024/06/assassins-creed-shadows-combat-and-stealth-evolved-gameplay-screenshots)). Moment: a street in the castle town of Fukuchiyama with townsfolk in frame, third-person, before any fight. Why: the top of the bar for a lived-in town at street level.
2. Resident Evil Requiem (AAA). Released 27 February 2026 ([Sortir à Paris](https://www.sortiraparis.com/en/what-to-do-in-paris/gaming/articles/329392-resident-evil-requiem-capcom-s-horror-game-now-available)). Video: main trailer, https://www.youtube.com/embed/ybD_igVwWSo (embedded on the same page). Moment: a ruined Raccoon City street at night, wet ground, a figure in frame. Why: night, rain-dark tarmac and lamplight, the closest match to LEDGER's night street.
3. 007 First Light (AAA). Released 27 May 2026 ([Gaming Trend launch release](https://gamingtrend.com/news/james-bond-is-now-next-gen-play-007-first-light-now/); first set for 27 March, see [IOI, 12 Feb 2026](https://ioi.dk/007firstlightgame/news/2026/007-first-light-story-trailer-reveal)). Video: launch trailer, https://www.youtube.com/embed/7wp3CkognPI (embedded on the Gaming Trend page). Moment: any third-person street or town shot with bystanders, British locations first if shown. Why: realistic people in public places, partly British.
4. Mafia: The Old Country (AA, sold at a lower price than full AAA, estimate). Released 8 August 2025 ([Game Developer press release](https://www.gamedeveloper.com/press-release/mafia-the-old-country-launching-august-8-2025-debuts-official-gameplay-trailer-and-developer-insights-video)). Video: Official Gameplay Trailer, https://www.youtube.com/watch?v=UOIg2lFVsJE (linked in the same press release; $49.99 standard edition there). Moment: a Sicilian town street or square with people, third-person, night if shown. Why: a period crime game in a small grimy town, the nearest genre cousin.
5. Like a Dragon: Infinite Wealth (AA to AAA, estimate). Released 26 January 2024 ([Gematsu](https://www.gematsu.com/2023/09/like-a-dragon-infinite-wealth-launches-january-26-2024)). Video: Gameplay Trailer (English, worldwide), https://www.youtube.com/embed/jeTFK18PjnM?feature=oembed. Moment: a city street at night with a crowd, third-person, no fight or menu on screen. Why: night streets dense with ordinary people, a crime story.
6. Silent Hill f (AA, made by an outside mid-size studio for Konami, estimate). Released 25 September 2025 ([Gematsu](https://www.gematsu.com/2025/06/silent-hill-f-launches-september-25)). Video: English release-date trailer, https://www.youtube.com/embed/Lpf9LoIWylA?feature=oembed. Moment: Hinako walking a fogged street of the 1960s town of Ebisugaoka, before any monster. Why: a small, old, period town street in weather, third-person.

Kingdom Come: Deliverance II is left out: the street is already tuned against it.

## How the frames are captured

- On Jafar's PC, by the main session: each video played in his browser at its highest quality, paused at the chosen moment, one screenshot. No download.
- The project's content rule holds for the frames too: no alcohol, gambling or children visible (bar or casino signs, drinks, a child in a crowd); if any shows, another second is chosen.
- All seven scaled to the same size (1920 by 1080, then the same crop), with logos, subtitles, HUD and on-screen text cropped or covered by a neutral bar, the LEDGER frame given the same treatment.
- File names randomised (for example frame-k3.png); the key, which name is which game and second, kept in a separate file the judges never see.
- Stored outside the repository in F:/LedgerTools/reference-other-games/, the shelf in production/retention.json and production/storage-map.json where the KCD2 frames already live (the 21 Sep ruling keeps other games' screenshots out of the repository). No previews of other games in production/previews/.

The one decision for Jafar (for the main session to batch on his page, tagged DECISION):

"Keep six still frames from public game trailers on the PC, outside the project's records, only for this blind test, shown to AI reviewers and on this page, never used to make anything? A) Yes, the same as the KCD2 frames (recommended). B) Yes, but delete them after each round. C) No, use words only." The 17 Nov ruling says only our own words and numbers are kept from other games, and the KCD2 frames are the precedent for kept pictures, so the pictures need his yes before the first round.

## Which LEDGER frame

The hook camera by day from the morning pictures (production/previews/morning-hook-day-(date).jpg, made by tools/morning_pictures.py), taken full size from F:/LedgerTools/renders/morning/. The street at night is the second round: two shots of LEDGER in one line-up would let judges spot the odd one out by matching.

## Judging protocol

1. At least three fresh reviewers (new subagents, no project files, not told any frame is from a game in development). Same prompt to each: "Here are seven frames from video games. Rank all seven from most unfinished-looking (1) to least (7). For the top three, one line each on what gives it away."
2. Each gets the frames in a different random order.
3. The main session reads the key and records LEDGER's position from each reviewer, plus their lines about it, as a finding.
4. Once a round, Jafar on his page (tagged REVIEW): the seven frames full size, unnamed, "Which of these look unfinished? Tick any." His pick is stored.

## Pass line

Passes only if Jafar does not tick the LEDGER frame, and no reviewer ranks it 1 or 2, and its middle position across reviewers is 4 to 7, the less unfinished half (estimate; tune after the first round). Anything else: "not done", with the reviewers' lines turned into list items, per CLAUDE.md's audit rule.

## Cost

About 2 session hours (estimate): moments 20 minutes, one capture sitting on the PC 30 (browser only, no clash with Unreal builds), crops and key 30, reviewers 20, record and page item 20. Disk: under 50 MB (estimate).

## When to repeat

At each phase exit, and after any street change Jafar calls big. Each round uses the newest LEDGER frame, alternates day and night, and swaps in at least two new game frames from newly released games so the judges never see the same set twice.
