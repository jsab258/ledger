# Noticing and memory: Hitman WoA and Watch Dogs: Legion (outside view)
Read 23 Nov 2026. Outside sources only. British spelling. Evidence is thin on players: I read 1 individual Steam review and about 13 forum posters, no Reddit page reached.

## Sources
1. Game Developer, "The AI of Hitman (2016)", Tommy Thompson, 7 Aug 2019. https://gamedeveloper.com/design/the-ai-of-hitman-2016-
2. PC Gamer, "How IO made the Hitman trilogy", Andy Kelly, 27 Jan 2021. https://www.pcgamer.com/au/how-io-made-the-hitman-trilogy-its-stealth-masterpiece/
3. PC Gamer, Hitman Complete First Season review, Phil Savage, 23 Nov 2016. https://www.pcgamer.com/au/hitman-the-complete-first-season-review
4. Hitman wiki, List of gameplay concepts, undated, read 23 Nov 2026. https://hitman.fandom.com/wiki/List_of_gameplay_concepts (names only, no mechanics)
5. Steam review, Redstone, posted 16 May 2023. https://steamcommunity.com/id/redstone_wired/recommended/1659040/
6. Steam forum thread, Freelancer/Showdown, 26-28 Dec 2024. https://steamcommunity.com/app/1659040/discussions/0/598514132636974233
7. Steam forum thread, trespass and sight, 4-8 Feb 2023. https://steamcommunity.com/app/1659040/discussions/0/3770111248607201394
8. Steam forum thread, Showdown suspects, 18-19 Dec 2024. https://steamcommunity.com/app/1659040/discussions/0/598513360098596698
9. Game Developer, "How Watch Dogs: Legion's play-as-anyone simulation works", Tommy Thompson, 9 Dec 2020. https://gamedeveloper.com/design/how-watch-dogs-legion-s-play-as-anyone-simulation-works
10. PC Gamer, "All of my WD Legion recruits are massive disappointments", Fraser Brown, 5 Nov 2020. https://www.pcgamer.com/all-of-my-watch-dogs-legion-recruits-are-massive-disappointments
11. PC Gamer, WD Legion review, Christopher Livingston, 28 Oct 2020. https://www.pcgamer.com/au/watch-dogs-legion-review
12. Inverse, WD Legion review, Tomas Franzese, 28 Oct 2020 (updated 20 Feb 2024). https://www.inverse.com/gaming/watch-dogs-legion-review
13. Giant Bomb forum, review thread (posts undated). https://www.giantbomb.com/forums/watch-dogs-legion-774547/watch-dogs-legion-finally-gets-the-gameplay-mostly-1890958/

## (a) Hitman
Mechanisms (source 1 unless stated)
- Routines: NPCs run set routines (serving, guarding, cooking); the article says they must be predictable because stealth players rely on it. Player acts can interrupt at once or with a delay so the NPC notices later. Opportunities let the player lure targets off routine (3).
- Knowledge: each active AI has public knowledge plus private memory (last-known positions). Sight and hearing only, locally. Shared services refresh periodically, so information goes stale and can be exploited.
- Witnesses: civilians are passive, notice extreme acts, can confront or alert guards, cannot fight. Guards fight and react to bodies and open weapons. A Dead Body service tells nearby NPCs a body is recent. Dead VIP starts a timed guard search from last known spot.
- Crowd zones: a drawn gun gives three zones (prone, panic, alert). Designers tune per level. Crowds "never calm down" once upset.
- Disguise service: tells each NPC whether the costume looks suspicious; refreshed periodically, so a stale disguise can pass. Only certain NPC types recognise you, which the critic found clear and welcome, though odd that some guards spot colleagues and others do not (3).
- Hitman 2 added turning the face away to shake a look, and mirror sight.
- Scale: 300+ behaviour-tree characters per level; Hitman 2 crowds over 2,000.
- Not found: an indicator or instinct explanation. Source 1 does not describe on-screen indicators; the wiki (4) names Instinct, Opportunities (renamed Mission Stories in Hitman 2) with no detail. Gap.
Developer statements
- Engström: scripting sits "on top of the systems"; systems must recover when players disrupt (2). Same piece: oversized missions are exhausting to replay, fewer return to them.
- Swartout Large: AI changes need all stakeholders so players are not confused (2).
Critic (3): "each Hitman mission is designed to be replayed"; advises switching off UI hints on a first go. Complains of the same voices everywhere.

Hand-coded players (unit = one reader's post; mixed Steam review and forum posts)
| # | Source | Game | Up/down | Hours | Themes |
|---|---|---|---|---|---|
| H1 | 5 Redstone | WoA | up | 169.9 | Praises NPC revamp over older games (unpredictable, repeated); replay; notes update friction |
| H2 | 6 OP | WoA | n/a | n/a | Punishes: NPC spots you for a split second then fires; guards everywhere |
| H3 | 6 DrakeyC | WoA | n/a | n/a | Punishes: guards see through wall into crate; unfair penalty for killing wrong suspect |
| H4 | 6 Rocket | WoA | n/a | n/a | Showdown enforcers kill in one shot; loud acts in public draw notice (neutral, advice) |
| H5 | 7 Sin4profit | WoA | n/a | n/a | Punishes: trespass flags seem random; shot in crates |
| H6 | 7 majikthise | WoA | n/a | n/a | Explains alerted sight cones; guards see through walls (explains, no praise) |
| H7 | 7 TYPHOON | WoA | n/a | n/a | Punishes: spotted through walls or floor |
| H8 | 7 DyD&Marina | WoA | n/a | n/a | Punishes: suspects do one routine cycle then stop (bug) |
| H9 | 7 Excirial | WoA | n/a | n/a | Wants trespass rules consistent with outfit rules |
Counts (base 9): punishes noticing that feels unfair or unreadable (H2,H3,H5,H7,H9; H6 explains the cause) 5 of 9; punishes routine breakage 1 of 9 (plus one more poster in 7 reporting a suspect walking through a wall); praises NPC behaviour 1 of 9; Steam thumbs known for 1 only. Source 8 (suspects, enforcers) is advice-heavy, not coded. Players learn by replay and wiki-style tips; no sampling of Mission Stories sentiment reached.

## (b) Watch Dogs: Legion
Mechanisms (9)
- Each "uprezzed" citizen gets a full 24-hour routine (sleep, work, leisure), travels visibly (can be intercepted, uses Metro), repeats daily until something changes it. Shared activities bring two people together.
- Uprezzing a person also uprezzes involved family and friends; contacts are recast into later missions.
- Memory records player acts and gives each citizen a reason for their view of DedSec. Harm changes schedules (hospital) and ripples to friends and family. Opinions are personal: someone hurt may not recognise a different operative. Area mood comes from set missions, not a count of attacks. Some citizens hate DedSec so much they cannot be recruited; revenge missions are gated by counters and timers.
- Tiers: on-screen, fully uprezzed, and a stored layer of incidental meetings. Hundreds in the active pool; unengaged ones cycle out.
- Recruit lines written and recorded about 20 times each; England tested by generating 100+ lawyers for plausible variety.
- Walsh: "almost all of it... is real" (9). Livingston (11) says generated people stay "ordinary"; Inverse mentions up to 9 million generated (12).
Critics
- 10 (Brown): traits "drearily one-note"; swapping agents free of cost means "the magic evaporates"; voices do not fit.
- 11 (Livingston): early recruits ordinary; connections made London feel "populated with people"; the few he grew attached to mattered; beaten friend means "they'll know that too".
- 12 (Franzese, 7/10): world "feel[s] alive"; many duds; dialogue repeats word for word; permadeath adds weight; recruits "feel tertiary".

Hand-coded (unit = one reader or critic; no Steam reviews reached)
| # | Source | Voice | Verdict | Themes |
|---|---|---|---|---|
| W1 | 10 Brown | critic | down | interchangeable, one-note, swap without cost |
| W2 | 11 Livingston | critic | mixed | ordinary at first; web of ties makes people; memory felt |
| W3 | 12 Franzese | critic | mixed | alive at scale; duds; repeated dialogue; permadeath weight |
| W4 | 13 bigsocrates | forum | mixed/down | all play roughly the same; voices alike; 1-4 traits |
| W5 | 13 therealturk | forum | down | "no one ever feels special"; everyone can do everything |
| W6 | 13 bigsocrates reply | forum | down | differences mostly cosmetic |
Counts (base 6): punishes interchangeable people 5 of 6 (W1,W3,W4,W5,W6); praises scale or connections 3 of 6 (W2,W3, W1 no); permadeath praised for weight 1 of 6; punishes repeated or ill-fitting dialogue and voices 3 of 6 (W1,W3,W4). Critics and one forum thread only: thin.

## What made being noticed and remembered felt, and what fell flat
Felt
- Harm has a visible consequence in someone's life (hospital, changed schedule) and reaches friends: 9, 11.
- Only the person harmed remembers; a stranger-NPC does not: 9. Felt as personal.
- Memory the player can feel through a named tie, not a number: 11.
- Predictable routines the player can learn and then break: 1, 3, 5.
- Readable rules for who can see through you (same-type NPCs only): 3.
- Replay as the way noticing is learnt: 3, 2.
- Permadeath gave weight, where the person mattered: 12.
Fell flat
- Noticing that seems to ignore the rules: seeing through walls, random trespass flags, instant fire: 6, 7.
- Routines that stop or glitch: 7.
- Same voices or word-for-word repeated lines break the sense of a person: 3, 10, 12.
- People who differ only in looks and perks, freely swappable: 10, 13.
- Generated people not tied into the story stay "tertiary": 12.
- Oversized levels tire replay: 2.
Note for the studio (inference, mine): both sets of players punish a break between what a person visibly knows and what the game does.

## Not reached
- Individual Steam review pages for WD Legion (none returned); Reddit pages (none returned); Hitman Steam review listings beyond one.
- Any IO GDC talk or interview on enforcers, the instinct indicator or alarms; Hocking interview text (gamedeveloper.com search hits seen, Hocking-specific page not fetched).
- Mission Stories player sentiment; Hitman wiki pages on enforcers and suspicion.
- Source 9 and 1 are second-hand writing about the games, not developer transcripts.
