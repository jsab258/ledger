# Story patterns from Steam reviews (advisor 276, 20 Nov 2026)

What players say about the STORY of eight story games, from their English Steam reviews pulled on Jafar's PC on 20 Nov 2026 through Valve's IUserReviewsService/GetAppReviews (no key; each game's reviews.jsonl under F:/LedgerTools/steam-reviews/<appid>/). Games: Kingdom Come: Deliverance II (1771300), GTA V (271590), Red Dead Redemption 2 (1174180), Sleeping Dogs DE (307690), GTA IV (12210), L.A. Noire (110800), Hitman World of Assassination (1659040), Watch Dogs: Legion (2239550). Forza Horizon 4 has no story and is left out; no Mafia game (his ruling, 20 Nov 14:30).

## Method

1. A story coding script (tools/steam_story_coder.py) was tuned once on 50 hand-read GTA V reviews and frozen (f9597545). It tags reviews that seem to speak about the story and the sub-themes they praise or fault.
2. For each game, 50 reviews the script tagged as story were drawn at random (seed 1120, fresh against the tuning set) and read in full by a Sonnet hand reader with one fixed brief (F:/LedgerTools/steam-reviews/HAND-CHECK-BRIEF-STORY.md), coding each against the advisor's sub-theme list, with any missing sub-theme as its own phrase.
3. Agreement, script against the hand reading (F:/LedgerTools/steam-reviews/walkthrough/checks.md): over the first five games, of every 100 script tags 47 were confirmed and the hand tags found by the script were 59 of 100; Hitman 22 and 39; Watch Dogs: Legion 24 and 41. The script holds only for characters (57 of 80 right), writing (17 of 26) and a lead who changes (9 of 12); it over-tags a weak story and never got missions-tell-the-story right. **So every share below comes from the hand reading, not the script.** The script's counts appear only as the size of each game's story talk.
4. Shares are of the hand-read reviews that actually speak about the story (between 18 and 40 of each game's 50), so each is a small sample: a share of 20% on 25 reviews is 5 reviews. Read them as directions, not exact numbers.
5. Caveat: the list lacked "the story praised in general". The Hitman reader wrote it down unasked; the Watch Dogs: Legion and KCD2 readers were asked to; the first five games' readers were not. That row is counted only for those three games and is left out of the cross-game ranking.
6. Quotes are short sentences picked from hand-coded reviews by the sub-theme's words; players' words, kept short.

## Across games (named in at least 5 of 8), ranked by how often players name them (pooled 225 story-speaking reviews)

| Rank | Sub-theme | Side | Games | Pooled share |
|---|---|---|---|---|
| 1 | characters worth caring about | praise | 8 of 8 | 35% (78) |
| 2 | a weak or forgettable story | complaint | 5 of 8 | 15% (34) |
| 3 | the writing and dialogue | praise | 7 of 8 | 13% (30) |
| 4 | moments that hit hard | praise | 6 of 8 | 7% (15) |
| 5 | missions on rails | complaint | 5 of 8 | 6% (13) |
| 6 | a rushed or weak ending | complaint | 5 of 8 | 5% (11) |
| 7 | humour | praise | 5 of 8 | 5% (11) |
| 8 | an ending that lands | praise | 5 of 8 | 4% (9) |
| 9 | a turn that surprised | praise | 6 of 8 | 4% (8) |

## True of only one or two games

- too short (complaint): Sleeping Dogs DE 1 of 21, Hitman World of Assassination 4 of 32.
- a clash of tone (complaint): L.A. Noire 1 of 20, Watch Dogs: Legion 1 of 40.
- side content better than the story (complaint): L.A. Noire 1 of 20, Watch Dogs: Legion 1 of 40.
- a thin villain (complaint): GTA IV 1 of 25.
- missions that tell the story (praise): Hitman World of Assassination 1 of 32.

## Per game

### Kingdom Come: Deliverance II

Hand-read: 43 of 50 story-tagged reviews speak about the story (26 of them thumbs up). Script, whole pull: 1,670 of 3,855 kept reviews tagged as story; on reading about 86% of its picks speak about the story. Names in praised character lines (script, unfiltered): Hans, Capon, Katherine, Godwin, Rosa, Musa.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| the story praised in general (readers' own phrase) | praise | 37% | 16 of 43 |  |
| characters worth caring about | praise | 23% | 10 of 43 | "The characters have depth and realism until it interferes with the writers job of pushing the story along." / "Music, Story, Characters and Gameplay are some of the best ive ever seen." |
| missions on rails | complaint | 12% | 5 of 43 |  |
| the writing and dialogue | praise | 12% | 5 of 43 | "Everythig is great here: writing, graphics, gameplay, technical aspects." / "The writing, the characters, the stakes, it all came together beautifully." |
| a weak or forgettable story | complaint | 9% | 4 of 43 | "The story is predictable and full of tropes." / "Great visuals, mediocre story, ABYSMAL combat system." |
| side stories | praise | 7% | 3 of 43 | "The story is amazing, side quests are just as good." / "Unlike typical fetch quests, the missions are interesting and not repeating even the side quests." |
| too much talk or cutscenes | complaint | 7% | 3 of 43 | "Too much talking and redundant mini games." |
| plot holes | complaint | 5% | 2 of 43 | "So many moments of characters doing nonsensical stuff so that the next thing can happen." |
| a turn that surprised | praise | 5% | 2 of 43 | "The story is great, full of twists and I was immersed throughout it." |
| predictable or cliched | complaint | 5% | 2 of 43 | "The story is predictable and full of tropes." / "So rather than evolve, the game opts for the idiotic cliche of throwing the ultimate hero off a cliff so he loses all his skills and needs to reclaim them." |
| a rushed or weak ending | complaint | 2% | 1 of 43 |  |
| moments that hit hard | praise | 2% | 1 of 43 |  |
| humour | praise | 2% | 1 of 43 | "A good amount of comedy sprinkled in between." |

Other sub-themes the readers named: boring stiff talking cutscenes; characters act out of character for plot; ending depends on missed dialogue choice; forced diversity plotlines; forgettable characters; forgettable side quests; implausible lead premise; moral choices; no evil choices; no real choice in story; recycled voice actors; repetitive side quests; story pacing; unsatisfying ending; weak characters; worldbuilding.

### GTA V

Hand-read: 18 of 50 story-tagged reviews speak about the story (15 of them thumbs up). Script, whole pull: 2,458 of 6,454 kept reviews tagged as story; on reading about 36% of its picks speak about the story. Names in praised character lines (script, unfiltered): Trevor, Franklin, Michael, Philips, Clinton, Lamar.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 83% | 15 of 18 | "This game is probably the only game that will ever master 3 protagonists." / "1) There are three playable characters, and they all have very different personalities." |
| the writing and dialogue | praise | 22% | 4 of 18 | "Trevor is the best written character of the three." / "The writing is sharp, and the dialogue is filled with humor and social commentary, creating a narrative that feels both entertaining and thought-provoking." |
| humour | praise | 22% | 4 of 18 | "Grand Theft Auto V is not only a preposterously enjoyable video game, but also an intelligent and sharp-tongued satire of contemporary America." / "The characters as well as funny, interesting and they're all ass holes, so standard GTA affair." |
| a lead who changes | praise | 22% | 4 of 18 | "It's so immersive and the character development is just PERFECT!" / "Character Development and Narrative (4.5/5):" |
| a turn that surprised | praise | 6% | 1 of 18 |  |
| missions on rails | complaint | 6% | 1 of 18 |  |

Other sub-themes the readers named: characters just shout about being washed up, shallow next to RDR2.

### Red Dead Redemption 2

Hand-read: 26 of 50 story-tagged reviews speak about the story (19 of them thumbs up). Script, whole pull: 4,302 of 7,742 kept reviews tagged as story; on reading about 52% of its picks speak about the story. Names in praised character lines (script, unfiltered): Morgan, Arthur, John, Linde, Dutch, Van.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 73% | 19 of 26 | "Literally one of the best games ever created with one of the best characters ever" / "As the story unfolds, he becomes one of the most complex and emotionally compelling protagonists ever written in gaming." |
| moments that hit hard | praise | 31% | 8 of 26 | "Animals hunt one another, NPCs follow daily routines, weather systems transform landscapes, and random encounters create unforgettable moments that feel unique to every player." / "You play as Arthur Morgan, a member of the Van der Linde gang, and his journey is deep, emotional, and unforgettable." |
| the writing and dialogue | praise | 31% | 8 of 26 | "As the story unfolds, he becomes one of the most complex and emotionally compelling protagonists ever written in gaming." / "RDR2 has some of the best characters, writing, and acting." |
| a lead who changes | praise | 19% | 5 of 26 | "There are great games, there are legendary games, and then there is Red Dead Redemption 2—a title that transcends entertainment and becomes an experience." / "Red Dead Redemption 2 is one of the purest examples of a video game being a masterpiece in art." |
| missions on rails | complaint | 12% | 3 of 26 | "The completely scripted main story and quite a bit of its "logic" (more like, decision stupidity) didn't convince me at all." |
| an ending that lands | praise | 12% | 3 of 26 | "I became so emotionally invested in Arthur Morgan and company, even the ending brought me to tears." / "By the time you reach the conclusion of the main portion of the game, the fates of these characters left me feeling both sad and happy." |
| a rushed or weak ending | complaint | 8% | 2 of 26 |  |
| too much talk or cutscenes | complaint | 8% | 2 of 26 |  |
| plot holes | complaint | 8% | 2 of 26 |  |
| side stories | praise | 4% | 1 of 26 | "Story was so amazing and there was so much more to explore even the side quest stories were good none dissappointed." |
| a turn that surprised | praise | 4% | 1 of 26 | "Chapter 5, in particular, was an unexpected and incredible shift that really made the world feel larger and more alive than I thought it was." |

### Sleeping Dogs DE

Hand-read: 21 of 50 story-tagged reviews speak about the story (14 of them thumbs up). Script, whole pull: 2,552 of 4,932 kept reviews tagged as story; on reading about 42% of its picks speak about the story. Names in praised character lines (script, unfiltered): Shen, Wei, Cantonese, Chinese, Jackie, Triad.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 57% | 12 of 21 | "Good characters and story." / "The undercover cop theme, characters, and atmosphere of Hong Kong are done really well." |
| a weak or forgettable story | complaint | 29% | 6 of 21 | "Story went to shits in the second half, but a good game nonetheless." / "If you are looking for a gripping story that is AAA quality then do not expect it here." |
| the writing and dialogue | praise | 10% | 2 of 21 | "Amazing storyline, diverse characters that are all unique and with great dialogue and voice acting, fun events, side missions, and DLC." / "The story is well written and ensures that the protagonist doesn't climb up in the ranks too fast in an unrealistic manner." |
| predictable or cliched | complaint | 10% | 2 of 21 | "Characters are one-dimensional and forgettable, and dialogue often feels clichéd and uninspired." / "Predictable, but still good enough." |
| moments that hit hard | praise | 10% | 2 of 21 |  |
| a turn that surprised | praise | 10% | 2 of 21 | "It is one of my favourite games due to the many different characters that you meet and the plot twists that happen as you progress through the game." |
| plot holes | complaint | 5% | 1 of 21 |  |
| humour | praise | 5% | 1 of 21 | "+ Funny Cantonese dialogues (and some weird accents)" |
| too short | complaint | 5% | 1 of 21 | "Downside is that it is too short, there are not enough missions and so the storyline progresses a bit too quickly." |
| a lead who changes | praise | 5% | 1 of 21 | "It has an amazing storyline with great voice acting and character development." |
| a rushed or weak ending | complaint | 5% | 1 of 21 |  |
| a slow or padded middle | complaint | 5% | 1 of 21 |  |
| a flat or unlikeable lead | complaint | 5% | 1 of 21 |  |

Other sub-themes the readers named: one-dimensional forgettable characters; second half of the story falls apart.

### GTA IV

Hand-read: 25 of 50 story-tagged reviews speak about the story (18 of them thumbs up). Script, whole pull: 2,715 of 6,328 kept reviews tagged as story; on reading about 50% of its picks speak about the story. Names in praised character lines (script, unfiltered): Niko, Bellic, Roman, Johnny, Jacob, Tony.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| characters worth caring about | praise | 72% | 18 of 25 | "Liberty City feels alive in every corner, and Niko Bellic is one of the best-written protagonists in gaming." / "Similarly the game's cast of characters is stereotypical but acceptable." |
| the writing and dialogue | praise | 24% | 6 of 25 | "The storyline is great, the characters are well written, the cheats are fun to mess around with and alot of small details give this game a unique feeling." / "The open-world formula just doesn’t do much for me anymore, even when the writing is solid." |
| a slow or padded middle | complaint | 20% | 5 of 25 |  |
| humour | praise | 12% | 3 of 25 | "And don't miss out on the hilarious websites in the game's Internets!" / "It's one of the more hilarious interactions in the entire series, IMO." |
| missions on rails | complaint | 4% | 1 of 25 |  |
| moments that hit hard | praise | 4% | 1 of 25 |  |
| an ending that lands | praise | 4% | 1 of 25 | "As for the ending." |
| predictable or cliched | complaint | 4% | 1 of 25 |  |
| a thin villain | complaint | 4% | 1 of 25 |  |

Other sub-themes the readers named: repetitive missions and replayed dialogue after failing; story drops the early characters and feels incoherent; too bleak and gloomy a world; too many characters.

### L.A. Noire

Hand-read: 20 of 50 story-tagged reviews speak about the story (12 of them thumbs up). Script, whole pull: 2,709 of 5,715 kept reviews tagged as story; on reading about 40% of its picks speak about the story. Names in praised character lines (script, unfiltered): Phelps, Cole, Kelso, Vice, Jack, Earle.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| a rushed or weak ending | complaint | 25% | 5 of 20 |  |
| a weak or forgettable story | complaint | 25% | 5 of 20 | "The writing is awful and the gameplay is not interesting." / "There is virtually no content at all in this game, and the game plays more like a movie with a plot that feels painstakingly difficult to invest any interest in." |
| the writing and dialogue | praise | 20% | 4 of 20 | "The story, which follows detective Cole Phelps as he solves a variety of cases, is compelling and well-written, providing a cinematic experience." / "Aside from its phenomenal voice acting, L.A." |
| missions on rails | complaint | 15% | 3 of 20 | "Linear Structure: Despite its open-world setting, L.A." / "Especially since they are linear and lack choice of how you want deal justice (such as arresting or killing a suspect)." |
| a slow or padded middle | complaint | 15% | 3 of 20 | "Everyone else is going to get bored with the pacing or frustrated with the vague interrogation systems." |
| moments that hit hard | praise | 10% | 2 of 20 | "Noire's main storyline, I felt emotional." |
| an ending that lands | praise | 10% | 2 of 20 | "Ending makes me cry." |
| characters worth caring about | praise | 10% | 2 of 20 | "The story is ORGASMIC, the gameplay is GTA mashed with CHRISTIAN VALUES, sounds and graphics are GOOD, people can RELATE to the characters + the characters are strong." / "Fantastic story, fun yet sparse shooting and action sections, engaging mysteries and dialogue, and well written and interesting characters." |
| plot holes | complaint | 5% | 1 of 20 |  |
| a clash of tone | complaint | 5% | 1 of 20 |  |
| a turn that surprised | praise | 5% | 1 of 20 | "Surprising final part, don't liked too much the end though, everything can't be perfect." |
| a flat or unlikeable lead | complaint | 5% | 1 of 20 |  |
| too much talk or cutscenes | complaint | 5% | 1 of 20 |  |
| side content better than the story | complaint | 5% | 1 of 20 |  |

Other sub-themes the readers named: case finales underwhelming; case stories kept the reviewer playing; chemistry between the lead and his partners; cringe dialogue; standalone Black Dahlia cases are the best part; unexplained story choices.

### Hitman World of Assassination

Hand-read: 32 of 50 story-tagged reviews speak about the story (25 of them thumbs up). Script, whole pull: 624 of 3,270 kept reviews tagged as story; on reading about 64% of its picks speak about the story. Names in praised character lines (script, unfiltered): Agent, Royale, Casino, Bond, Mikkelsen, Chiffre.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| the story praised in general (readers' own phrase) | praise | 41% | 13 of 32 |  |
| too short | complaint | 12% | 4 of 32 |  |
| a weak or forgettable story | complaint | 9% | 3 of 32 | "Story is really meh." / "maybe exhausted by the boring/meaningless story, just the thinnest justification to murder the super rich in a sandbox..." |
| humour | praise | 6% | 2 of 32 | "Don't forget the shockingly funny writing; I'm not usually hanging on every word of each errant NPC like I do when I play Hitman." / "Some story missions are really hilarious and creative." |
| a rushed or weak ending | complaint | 6% | 2 of 32 |  |
| side stories | praise | 6% | 2 of 32 | "Each of more than 20 missions gives you a huge sandbox filled with different assassination opportunities, side stories, and challenges." |
| an ending that lands | praise | 6% | 2 of 32 |  |
| the writing and dialogue | praise | 3% | 1 of 32 | "Don't forget the shockingly funny writing; I'm not usually hanging on every word of each errant NPC like I do when I play Hitman." |
| missions that tell the story | praise | 3% | 1 of 32 |  |
| characters worth caring about | praise | 3% | 1 of 32 |  |

Other sub-themes the readers named: amazing story; engaging stories that are not too serious; engaging story; enjoyed the main story; enjoyed the story; favourite story of the three; good spy conspiracy thriller story; handler voice-over repeated and annoying; memorable cinematic story; narrative never gets old; real cutscenes are back; story decent; story good overall; too story driven; well-balanced story.

### Watch Dogs: Legion

Hand-read: 40 of 50 story-tagged reviews speak about the story (24 of them thumbs up). Script, whole pull: 982 of 2,427 kept reviews tagged as story; on reading about 80% of its picks speak about the story. Names in praised character lines (script, unfiltered): Aiden, London, Wrench, Pearce, Bagley, Albion.

| Sub-theme | Side | Share | Reviews | Quotes |
|---|---|---|---|---|
| a weak or forgettable story | complaint | 40% | 16 of 40 | "The first game has a captivating story, but some details in the gameplay bothered me, such as the movement of the character or combat mechanics, for example." / "Story and characters, well they are just goons, like you literally just play as a side character." |
| the story praised in general (readers' own phrase) | praise | 30% | 12 of 40 |  |
| a flat or unlikeable lead | complaint | 5% | 2 of 40 | "Melee is now the main focus and it is just so weird: can't dodge away from grabs, guard breaks lead to counter from the enemy who is supposedly guard broken." / "Maybe if it didn't lack a protagonist, it would be better." |
| side stories | praise | 5% | 2 of 40 | "[i]Some[/i] of the story lines/side quests etc." / "The story was the highlight for me, especially after exploring the city and tackling some side quests." |
| a clash of tone | complaint | 2% | 1 of 40 | "But the funniest part is story cutscenes, the tone of characters varies a lot." |
| characters worth caring about | praise | 2% | 1 of 40 |  |
| a turn that surprised | praise | 2% | 1 of 40 |  |
| moments that hit hard | praise | 2% | 1 of 40 |  |
| an ending that lands | praise | 2% | 1 of 40 |  |
| predictable or cliched | complaint | 2% | 1 of 40 |  |
| side content better than the story | complaint | 2% | 1 of 40 |  |

Other sub-themes the readers named: DLC characters well voiced; DLC story more fleshed out; NPCs lacking; after-story continues; choices make no difference; disjointed dialogue from interchangeable leads; dry recycled robotic dialogue; generic mediocre writing; generic quips from recruits; good intro; interchangeable characters hinder story; interesting political themes; lack of a natural story; lacking character development; no emotional anchor; no main character; no single protagonist; play as a side character; poor dialogue; recruited characters hard to care about; recruiting undermines the story; recruits hard to care about; story and gameplay do not affect each other; story interesting enough; unnatural conversations in cutscenes from many characters; weak cast of characters.
