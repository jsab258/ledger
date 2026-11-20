# Story patterns from Steam reviews (advisor 276, 20 Nov 2026)

What players say about the STORY of eight story games, from their English Steam reviews pulled on Jafar's PC on 20 Nov 2026 through Valve's IUserReviewsService/GetAppReviews (no key; each game's reviews.jsonl under F:/LedgerTools/steam-reviews/<appid>/). Games: Kingdom Come: Deliverance II (1771300), GTA V (271590), Red Dead Redemption 2 (1174180), Sleeping Dogs DE (307690), GTA IV (12210), L.A. Noire (110800), Hitman World of Assassination (1659040), Watch Dogs: Legion (2239550). Forza Horizon 4 has no story and is left out; no Mafia game (his ruling, 20 Nov 14:30).

## Method

1. A story coding script (tools/steam_story_coder.py) was tuned once on 50 hand-read GTA V reviews and frozen in commit 56334908b (wip, 20 Nov; the logic hash "f9597545" named in that commit could not be reproduced from the file [UNVERIFIED]). It tags reviews that seem to speak about the story and the sub-themes they praise or fault.
2. For each game, 50 reviews the script tagged as story were drawn at random (seed 1120, fresh against the tuning set) and read in full by a Sonnet hand reader with one fixed brief (F:/LedgerTools/steam-reviews/HAND-CHECK-BRIEF-STORY.md), coding each against the advisor's sub-theme list, with any missing sub-theme as its own phrase. Two limits of this choice: the samples come only from reviews the script tagged as story, and the script finds only about 59 in 100 of the reviews a reader would call story talk, so story talk it misses is not represented; and each game's pull is split by month and thumb, so it is roughly half thumbs down (KCD2: 2,030 up, 1,909 down), and the thumbs-up counts below reflect the sampling, not the players' real split.
3. Agreement, script against the hand reading (F:/LedgerTools/steam-reviews/walkthrough/checks.md): over the first five games, of every 100 script tags 47 were confirmed and the hand tags found by the script were 59 of 100; Hitman 22 and 39; Watch Dogs: Legion 24 and 41; KCD2 36 and 51. Over the first five games (the per-code figures cover only those), the script holds only for characters (57 of 80 right), writing (17 of 26) and a lead who changes (9 of 12); it over-tags a weak story and never got missions-tell-the-story right. **So every share below comes from the hand reading, not the script.** The script's counts appear only as the size of each game's story talk.
4. Per-game shares are of the hand-read reviews that actually speak about the story (between 18 and 43 of each game's 50), so each is a small sample: a share of 20% on 25 reviews is 5 reviews. Read them as directions, not exact numbers.
5. Caveat: the list lacked "the story praised in general". The Hitman, Watch Dogs: Legion and KCD2 readers wrote it down as their own phrase (whether the last two were asked to is not in the brief file [UNVERIFIED]); the first five games' readers wrote none. So in those three games many more reviews speak about the story only in general (KCD2 15 of 43, Hitman 16 of 32, Watch Dogs: Legion 19 of 40, against 0 to 2 elsewhere), and their per-game shares sit on larger bases. The cross-game ranking is therefore pooled only over reviews that carry a coded sub-theme, so every game counts alike. The general row is counted for every review whose reader phrase says it, and kept out of the ranking.
6. Quotes are sentences of 5 to 14 words, each used once, picked by the sub-theme's words from reviews the reader coded for that sub-theme; the sentence itself was not confirmed by a reader, so a quote can miss its sub-theme.

## Across games (named in at least 5 of 8), ranked by how often players name them (pooled over the 171 hand-read reviews that carry a coded sub-theme)

| Rank | Sub-theme | Side | Games | Pooled share |
|---|---|---|---|---|
| 1 | characters worth caring about | praise | 8 of 8 | 46% (78) |
| 2 | a weak or forgettable story | complaint | 5 of 8 | 20% (34) |
| 3 | the writing and dialogue | praise | 7 of 8 | 18% (30) |
| 4 | moments that hit hard | praise | 6 of 8 | 9% (15) |
| 5 | missions on rails | complaint | 5 of 8 | 8% (13) |
| 6 | a rushed or weak ending | complaint | 5 of 8 | 6% (11) |
| 7 | humour | praise | 5 of 8 | 6% (11) |
| 8 | an ending that lands | praise | 5 of 8 | 5% (9) |
| 9 | a turn that surprised | praise | 6 of 8 | 5% (8) |

## Single mentions (named in only one or two games; one review each unless a count says otherwise)

- too short (complaint): Sleeping Dogs DE 1 of 21, Hitman World of Assassination 4 of 32.
- a clash of tone (complaint): L.A. Noire 1 of 20, Watch Dogs: Legion 1 of 40.
- side content better than the story (complaint): L.A. Noire 1 of 20, Watch Dogs: Legion 1 of 40.
- a thin villain (complaint): GTA IV 1 of 25.
- missions that tell the story (praise): Hitman World of Assassination 1 of 32.

## Per game

### Kingdom Come: Deliverance II

Hand-read: 43 of 50 story-tagged reviews speak about the story (26 of them thumbs up; the pull is about half thumbs down by design); 28 carry a coded sub-theme. Script, whole pull: 1,670 of 3,855 kept reviews tagged as story; on reading about 86% of its picks speak about the story. Names in praised character lines (script, unfiltered): Hans, Capon, Katherine, Godwin, Rosa, Musa.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| the story praised in general (readers' own phrase) | praise | 70% | 30 of 43 |  |
| characters worth caring about | praise | 23% | 10 of 43 | "Music, Story, Characters and Gameplay are some of the best ive ever seen." / "The characters of the game are another highlight and quickly win you over." |
| missions on rails | complaint | 12% | 5 of 43 |  |
| the writing and dialogue | praise | 12% | 5 of 43 | "Everythig is great here: writing, graphics, gameplay, technical aspects." / "The writing, the characters, the stakes, it all came together beautifully." |
| a weak or forgettable story | complaint | 9% | 4 of 43 | "The writing is basic and mostly competent while being laughably bad at times." / "Great visuals, mediocre story, ABYSMAL combat system." |
| side stories | praise | 7% | 3 of 43 | "The story is amazing, side quests are just as good." |
| too much talk or cutscenes | complaint | 7% | 3 of 43 | "Too much talking and redundant mini games." |
| plot holes | complaint | 5% | 2 of 43 |  |
| a turn that surprised | praise | 5% | 2 of 43 | "The story is great, full of twists and I was immersed throughout it." |
| predictable or cliched | complaint | 5% | 2 of 43 | "The story is predictable and full of tropes." |
| a rushed or weak ending | complaint | 2% | 1 of 43 |  |
| moments that hit hard | praise | 2% | 1 of 43 |  |
| humour | praise | 2% | 1 of 43 | "A good amount of comedy sprinkled in between." |

Other sub-themes the readers named: boring stiff talking cutscenes; characters act out of character for plot; ending depends on missed dialogue choice; forced diversity plotlines; forgettable characters; forgettable side quests; implausible lead premise; moral choices; no evil choices; no real choice in story; recycled voice actors; repetitive side quests; story pacing; unsatisfying ending; weak characters; worldbuilding.

### GTA V

Hand-read: 18 of 50 story-tagged reviews speak about the story (15 of them thumbs up; the pull is about half thumbs down by design); 17 carry a coded sub-theme. Script, whole pull: 2,458 of 6,454 kept reviews tagged as story; on reading about 36% of its picks speak about the story. Names in praised character lines (script, unfiltered): Trevor, Franklin, Michael, Philips, Clinton, Lamar.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 83% | 15 of 18 | "This game is probably the only game that will ever master 3 protagonists." / "1) There are three playable characters, and they all have very different personalities." |
| the writing and dialogue | praise | 22% | 4 of 18 | "Trevor is the best written character of the three." / "The voice acting is top-notch, with memorable performances that bring the characters to life." |
| humour | praise | 22% | 4 of 18 | "They’re flawed, funny, and chaotic, and switching between them keeps the story fresh." |
| a lead who changes | praise | 22% | 4 of 18 | "It's so immersive and the character development is just PERFECT!" |
| a turn that surprised | praise | 6% | 1 of 18 |  |
| missions on rails | complaint | 6% | 1 of 18 |  |

Other sub-themes the readers named: characters just shout about being washed up, shallow next to RDR2.

### Red Dead Redemption 2

Hand-read: 26 of 50 story-tagged reviews speak about the story (19 of them thumbs up; the pull is about half thumbs down by design); 26 carry a coded sub-theme. Script, whole pull: 4,302 of 7,742 kept reviews tagged as story; on reading about 52% of its picks speak about the story. Names in praised character lines (script, unfiltered): Morgan, Arthur, John, Linde, Dutch, Van.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 73% | 19 of 26 | "His character development is subtle, believable, and devastatingly human." / "I like the story and I like the characters and I like shooting people." |
| moments that hit hard | praise | 31% | 8 of 26 | "Few games manage to tell a story with such maturity and emotional weight." / "It's an unforgettable experience that sets a new standard for open-world games." |
| the writing and dialogue | praise | 31% | 8 of 26 | "Many players still consider Arthur one of the best-written characters in video game history." / "RDR2 has some of the best characters, writing, and acting." |
| a lead who changes | praise | 19% | 5 of 26 | "Visually, Red Dead Redemption 2 remains breathtaking even by modern standards." |
| missions on rails | complaint | 12% | 3 of 26 |  |
| an ending that lands | praise | 12% | 3 of 26 | "It was a great conclusion, and it honestly made me cry." |
| a rushed or weak ending | complaint | 8% | 2 of 26 |  |
| too much talk or cutscenes | complaint | 8% | 2 of 26 |  |
| plot holes | complaint | 8% | 2 of 26 |  |
| side stories | praise | 4% | 1 of 26 |  |
| a turn that surprised | praise | 4% | 1 of 26 | "[b]Gameplay & Mechanics:[/b] Surprise, surprise, it’s an open-world action-adventure game." |

### Sleeping Dogs DE

Hand-read: 21 of 50 story-tagged reviews speak about the story (14 of them thumbs up; the pull is about half thumbs down by design); 21 carry a coded sub-theme. Script, whole pull: 2,552 of 4,932 kept reviews tagged as story; on reading about 42% of its picks speak about the story. Names in praised character lines (script, unfiltered): Shen, Wei, Cantonese, Chinese, Jackie, Triad.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 57% | 12 of 21 | "The undercover cop theme, characters, and atmosphere of Hong Kong are done really well." / "-the protagonist is not an idiot" |
| a weak or forgettable story | complaint | 29% | 6 of 21 | "Story went to shits in the second half, but a good game nonetheless." / "It is not fit into the story." |
| the writing and dialogue | praise | 10% | 2 of 21 |  |
| predictable or cliched | complaint | 10% | 2 of 21 | "Characters are one-dimensional and forgettable, and dialogue often feels clichéd and uninspired." / "Predictable, but still good enough." |
| moments that hit hard | praise | 10% | 2 of 21 |  |
| a turn that surprised | praise | 10% | 2 of 21 |  |
| plot holes | complaint | 5% | 1 of 21 |  |
| humour | praise | 5% | 1 of 21 | "+ Funny Cantonese dialogues (and some weird accents)" |
| too short | complaint | 5% | 1 of 21 |  |
| a lead who changes | praise | 5% | 1 of 21 | "It has an amazing storyline with great voice acting and character development." |
| a rushed or weak ending | complaint | 5% | 1 of 21 |  |
| a slow or padded middle | complaint | 5% | 1 of 21 |  |
| a flat or unlikeable lead | complaint | 5% | 1 of 21 |  |

Other sub-themes the readers named: one-dimensional forgettable characters; second half of the story falls apart.

### GTA IV

Hand-read: 25 of 50 story-tagged reviews speak about the story (18 of them thumbs up; the pull is about half thumbs down by design); 23 carry a coded sub-theme. Script, whole pull: 2,715 of 6,328 kept reviews tagged as story; on reading about 50% of its picks speak about the story. Names in praised character lines (script, unfiltered): Niko, Bellic, Roman, Johnny, Jacob, Tony.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 72% | 18 of 25 | "Similarly the game's cast of characters is stereotypical but acceptable." / "He is almost an ideal GTA main character." |
| the writing and dialogue | praise | 24% | 6 of 25 |  |
| a slow or padded middle | complaint | 20% | 5 of 25 |  |
| humour | praise | 12% | 3 of 25 | "And don't miss out on the hilarious websites in the game's Internets!" / "It's one of the more hilarious interactions in the entire series, IMO." |
| missions on rails | complaint | 4% | 1 of 25 |  |
| moments that hit hard | praise | 4% | 1 of 25 |  |
| an ending that lands | praise | 4% | 1 of 25 |  |
| predictable or cliched | complaint | 4% | 1 of 25 |  |
| a thin villain | complaint | 4% | 1 of 25 |  |

Other sub-themes the readers named: repetitive missions and replayed dialogue after failing; story drops the early characters and feels incoherent; too bleak and gloomy a world; too many characters.

### L.A. Noire

Hand-read: 20 of 50 story-tagged reviews speak about the story (12 of them thumbs up; the pull is about half thumbs down by design); 19 carry a coded sub-theme. Script, whole pull: 2,709 of 5,715 kept reviews tagged as story; on reading about 40% of its picks speak about the story. Names in praised character lines (script, unfiltered): Phelps, Cole, Kelso, Vice, Jack, Earle.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| a rushed or weak ending | complaint | 25% | 5 of 20 |  |
| a weak or forgettable story | complaint | 25% | 5 of 20 | "The writing is awful and the gameplay is not interesting." |
| the writing and dialogue | praise | 20% | 4 of 20 | "Aside from its phenomenal voice acting, L.A." / "The voice acting is also absolutely top notch." |
| missions on rails | complaint | 15% | 3 of 20 | "Linear Structure: Despite its open-world setting, L.A." |
| a slow or padded middle | complaint | 15% | 3 of 20 |  |
| moments that hit hard | praise | 10% | 2 of 20 | "Noire's main storyline, I felt emotional." |
| an ending that lands | praise | 10% | 2 of 20 |  |
| characters worth caring about | praise | 10% | 2 of 20 |  |
| plot holes | complaint | 5% | 1 of 20 |  |
| a clash of tone | complaint | 5% | 1 of 20 |  |
| a turn that surprised | praise | 5% | 1 of 20 | "Surprising final part, don't liked too much the end though, everything can't be perfect." |
| a flat or unlikeable lead | complaint | 5% | 1 of 20 |  |
| too much talk or cutscenes | complaint | 5% | 1 of 20 |  |
| side content better than the story | complaint | 5% | 1 of 20 |  |

Other sub-themes the readers named: case finales underwhelming; case stories kept the reviewer playing; chemistry between the lead and his partners; cringe dialogue; standalone Black Dahlia cases are the best part; unexplained story choices.

### Hitman World of Assassination

Hand-read: 32 of 50 story-tagged reviews speak about the story (25 of them thumbs up; the pull is about half thumbs down by design); 16 carry a coded sub-theme. Script, whole pull: 624 of 3,270 kept reviews tagged as story; on reading about 64% of its picks speak about the story. Names in praised character lines (script, unfiltered): Agent, Royale, Casino, Bond, Mikkelsen, Chiffre.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| the story praised in general (readers' own phrase) | praise | 44% | 14 of 32 |  |
| too short | complaint | 12% | 4 of 32 |  |
| a weak or forgettable story | complaint | 9% | 3 of 32 | "The story doesn't matter that much." |
| humour | praise | 6% | 2 of 32 | "Some story missions are really hilarious and creative." |
| a rushed or weak ending | complaint | 6% | 2 of 32 |  |
| side stories | praise | 6% | 2 of 32 |  |
| an ending that lands | praise | 6% | 2 of 32 |  |
| the writing and dialogue | praise | 3% | 1 of 32 |  |
| missions that tell the story | praise | 3% | 1 of 32 |  |
| characters worth caring about | praise | 3% | 1 of 32 |  |

Other sub-themes the readers named: amazing story; engaging stories that are not too serious; engaging story; enjoyed the main story; enjoyed the story; favourite story of the three; good spy conspiracy thriller story; handler voice-over repeated and annoying; memorable cinematic story; narrative never gets old; real cutscenes are back; story decent; story good overall; too story driven; well-balanced story.

### Watch Dogs: Legion

Hand-read: 40 of 50 story-tagged reviews speak about the story (24 of them thumbs up; the pull is about half thumbs down by design); 21 carry a coded sub-theme. Script, whole pull: 982 of 2,427 kept reviews tagged as story; on reading about 80% of its picks speak about the story. Names in praised character lines (script, unfiltered): Aiden, London, Wrench, Pearce, Bagley, Albion.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| a weak or forgettable story | complaint | 40% | 16 of 40 | "The story sucks, and the gameplay quickly becomes shallow and repetitive." / "story 6/10 could been better" |
| the story praised in general (readers' own phrase) | praise | 35% | 14 of 40 |  |
| a flat or unlikeable lead | complaint | 5% | 2 of 40 | "Maybe if it didn't lack a protagonist, it would be better." |
| side stories | praise | 5% | 2 of 40 | "[i]Some[/i] of the story lines/side quests etc." |
| a clash of tone | complaint | 2% | 1 of 40 | "But the funniest part is story cutscenes, the tone of characters varies a lot." |
| characters worth caring about | praise | 2% | 1 of 40 |  |
| a turn that surprised | praise | 2% | 1 of 40 |  |
| moments that hit hard | praise | 2% | 1 of 40 |  |
| an ending that lands | praise | 2% | 1 of 40 |  |
| predictable or cliched | complaint | 2% | 1 of 40 |  |
| side content better than the story | complaint | 2% | 1 of 40 |  |

Other sub-themes the readers named: DLC characters well voiced; DLC story more fleshed out; NPCs lacking; after-story continues; choices make no difference; disjointed dialogue from interchangeable leads; dry recycled robotic dialogue; generic mediocre writing; generic quips from recruits; good intro; interchangeable characters hinder story; interesting political themes; lack of a natural story; lacking character development; no emotional anchor; no main character; no single protagonist; play as a side character; poor dialogue; recruited characters hard to care about; recruiting undermines the story; recruits hard to care about; story and gameplay do not affect each other; story interesting enough; unnatural conversations in cutscenes from many characters; weak cast of characters.
