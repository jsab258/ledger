# Method and shares: raw research notes

Helper run, 20 Nov 2026. 20 searches used. Tags: "read 20 Nov 2026" means the page was fetched and read (the fetch tool summarises pages, so it is a summary, not the full text). "snippet only" means only the search result title/URL was seen. Every other source in the results was not opened and is not evidence.

Headline: the search tool returned titles and links only, no text, so many obvious sources (Swink, Wagar, Eurogamer method page, Naughty Dog and Ubisoft motion matching talks, Splinter Cell tests) were NOT reached. Nothing below about them is evidence. They are listed at the end as gaps to chase from the PC.

## Q1. Measuring game feel from video

### (a) Melee: startup, active, recovery, hit-stop, latency

- Dustloop forum thread "Counting move frames", Jul to Aug 2012. https://www.forums.dustloop.com/topic/5153-counting-move-frames/ (read 20 Nov 2026). Community practice, anecdotal, no settled method.
  - Capture at 60 fps (capture card or camera), step one frame at a time.
  - Startup: first frame after idle changes to the frame before the hit spark.
  - Active frames are hard to tell from recovery. One trick: meaty a move so only its last active frame connects.
  - Hit-stun counts must subtract hit-stop (example given: 39 frames minus 13 hit-stop = 26).
  - Pitfalls named: the game does not always run a true constant 60 fps so counts can be off by a few frames; active frames are inferred from repeated frames so easy to miscount; hit-stop distorts counts; programmable controllers can drop frames in long inputs; multi-hit moves are very hard.
  - Trust: low to medium. Forum posts, 14 years old, but the pitfalls match common sense.
- Sakurai, Famitsu column vol 490-491, translated by Source Gaming, 11 Nov 2015. https://sourcegaming.info/2015/11/11/thoughts-on-hitstop-sakurais-famitsu-column-vol-490-1/ (read 20 Nov 2026).
  - Hit-stop is a brief freeze of both fighters to stress impact. Scales with damage, tuned per attack, capped, and kept shorter than he would like in free-for-alls. The flinch transition during hit-stop takes four frames. Vibration is planned around the freeze length.
  - No total frame counts given. Trust: high for intent (the designer himself, via a translation); no numbers to copy.
- Kotaku (Luke Plunkett), 7 Sep 2009. https://kotaku.com/measuring-the-time-it-takes-between-a-button-press-and-5353769 (read 20 Nov 2026). Only says Digital Foundry measured controller-to-game lag, excluding TV lag, and points to a Eurogamer piece for the method. Method detail NOT obtained. The Eurogamer "Console Gaming: The Lag Factor" page appeared only as a search hint (via an n4g and neogaf mirror, snippet only), not opened.
- Regensburg "Yet another latency measuring device" (PDF) and OpenLDAT (J Soc Inf Display, 2022): appeared in search, snippet only. Useful pointers for hardware latency rigs, not read.
- Celia Wagar hit-stop articles: NOT found. Searches returned itch.io posts and a placeholder page (https://gamejuice.pages.dev/articles/hit-stop-frame-trick, read 20 Nov 2026: says "Coming Soon", no content, no sources, so worthless). Swink "Game Feel": not reached. Capcom talks on hit-stop: not reached.

### (b) Third-person locomotion and camera

- John Nesky, "50 Camera Mistakes", GDC 2014. https://gdcvault.com/play/1020460/50-Camera (read 20 Nov 2026, abstract page only). Lists failures such as impaired distance judgement and broken line of sight. No numbers on distance, lag or FOV on the free page; full video is members only. A second page, gamedeveloper.com "50 common game camera mistakes" (snippet only, listed as video, 17 Nov 2015) not opened. Nesky's Journey talk: not found.
- Epic, "Six ingredients for a dynamic third person camera". https://www.unrealengine.com/tech-blog/six-ingredients-for-a-dynamic-third-person-camera (read 20 Nov 2026, no date shown). Names the tunable parts: arm length (distance), camera lag and rotation lag (rubber band delay on start/stop), FOV, offset, pitch. Useful as the list of things to estimate from video. Gives no video-measurement method. Trust: fine as a parameter list.
- FOV from screenshots: Wikipedia "Field of view in video games" https://en.wikipedia.org/wiki/Field_of_view_in_video_games (read 20 Nov 2026). Confirms horizontal and vertical FOV relate through aspect ratio (the equations did not come through in the summary), and gives only broad figures: console about 60 degrees, PC 90 to 100. No image-based method there. Other hits not opened (snippet only): a Valve developer wiki FOV page, a computergraphics.stackexchange question, a SynthEyes "determining field of view" page (borisfx.com/documentation/syntheyes/GeoHTracking_files/determining_field_of/), a dev.to HFOV vs VFOV post. The camera-tracking route (vanishing points, known-size objects) is standard in match-moving software, but I did not read a source that applies it to game footage. Mark as unverified.
- Run speed from known object sizes, motion matching talks (Naughty Dog, Ubisoft): not reached.

### (c) Stealth perception

- Tommy Thompson, "The AI of Hitman 2016", Game Developer, 7 Aug 2019. https://gamedeveloper.com/design/the-ai-of-hitman-2016- (read 20 Nov 2026). Describes sensors, shared-knowledge services that update only periodically, and Hitman 2 changes (turn face away, mirrors, crowds). No ranges, angles or detection times. Trust: good on structure, silent on numbers.
- GameSkinny "Sciencing the s**t out of Hitman disguises" (Larry Everett, undated, over 8 years old). https://www.gameskinny.com/opinion/sciencing-the-shit-out-of-hitman-disguises/ (read 20 Nov 2026). Cites face-recognition studies; NO detection test, distances or sample counts. Do not cite as a measurement.
- Hitman forum bug threads and Steam threads appeared (snippet only). No community distance test was found or read. Splinter Cell detection analyses: not found.
- Honest summary: no published video-based detection time or range method was reached. The obvious practical method (repeat a fixed approach in a quiet spot, frame-step to the first alert cue, many trials) is general reasoning, not a source.

### (d) Chases

- Nothing found. No source reached on measuring chase pacing or gap closing from video.

### Cross-cutting notes on samples, repeatability, frame rate

- Only the Dustloop thread gave concrete pitfalls (variable frame rate, duplicated frames, hit-stop distortion, controller macro skips). No source stated a recommended sample size. Treat that as an open question.
- 30 fps games in 60 fps uploads, duplicated frames: not covered by any source reached. Reasoning only: a 30 fps game encoded at 60 fps shows each game frame twice, so counts must be halved and timing resolution is 33 ms, not 16.7 ms. Mark as unverified; check on a known-duration clip from this PC before use.

## Q2. Play time split by activity

Short answer: no published activity split (on foot / driving / cut scenes / menus / waiting) was found for any of the named games. Only whole-length figures, one cut-scene total, and telemetry papers that measure other things.

### Developer talks and telemetry papers

- Mahlmann, Drachen, Togelius, Canossa, Yannakakis, "Predicting Player Behavior in Tomb Raider: Underworld", IEEE CIG 2010. https://www.um.edu.mt/library/oar/bitstream/123456789/22926/1/cig10TRU.pdf (read 20 Nov 2026). About 203,000 players over Dec 2008 to Jan 2009; 10,000 sampled; 1,732 finished the whole game. Measures stopping point, completion time, time in specific locations, deaths by cause. Time is split by place, not by activity type. Trust: high as science, but it does not answer the question. Linear game, not open world.
- Dankoff, "Game telemetry with DNA tracking on Assassin's Creed", Game Developer, reprint 20 Mar 2014, written 2012. https://gamedeveloper.com/design/game-telemetry-with-dna-tracking-on-assassin-s-creed (read 20 Nov 2026). Shows what Ubisoft tracked: mission failures, kills by type, how missions ended, sync, economy. Example: 138 players, about 1,200 hours, 10 days after Brotherhood release. No activity time split. Trust: good for what is tracked, nothing for shares.
- Other hits, snippet only, not opened: Axios 18 Feb 2022 on Ubisoft playing times (https://www.axios.com/2022/02/18/ubisoft-cites-new-games-longer-playing-times-success); GDC "Assassin's Creed Origins: Monitoring and Validation of World Design Data" (https://gdcvault.com/play/1025452/contactUs); academic survey chapters (Springer 10.1007/978-3-642-24500-8_26; "Game data mining" PDF at um.edu.mt; Loria PhD thesis at iris.unitn.it). One of these may hold an open-world split; I did not check.

### Cut scene totals

- Den of Geek (Matthew Byrd), 26 Jun 2023, https://www.denofgeek.com/games/final-fantasy-16-total-cutscene-time/ (read 20 Nov 2026): says RDR2 has about 12 hours of story sequences if you leave out parts where you control the character. This is a secondhand figure in an article about Final Fantasy 16; the method and original source are not stated. Trust: low to medium. Nothing on GTA V.
- GTA V cut scene total: not found. The GTA Intel FAQ (https://gtaintel.com/faq/how-long-is-gta-5-story-mode, dated 27 May 2026, read 20 Nov 2026) gives no cut scene figure.

### Whole-game length (HowLongToBeat-style)

- GTA V, GTA Intel FAQ above: main story about 30 hours (55 missions), 22 to 25 speed run, 100 percent 75 to 85. No sources cited, "unverified editorial" in the reader's own words. Trust: low. The howlongtobeat.com game page appeared (a mirror, snippet only), not read.
- Mafia: Definitive Edition, Game Rant (William Parks), 25 Sep 2020, https://gamerant.com/mafia-definitive-edition-how-long-to-beat-hltb-length-chapters-list-hours/ (read 20 Nov 2026): about 15 hours main story, 20 chapters. No HLTB numbers or cut scene split despite the URL. Trust: low to medium.
- Kingdom Come: Deliverance II, GamesRadar, updated 10 Apr 2025, https://www.gamesradar.com/games/action-rpg/kingdom-come-deliverance-2-how-long-time-to-beat-length (read 20 Nov 2026): main story 40 to 50 hours, standard 50 to 70, 100 percent 90 to 110. Estimate, method not shown. Trust: medium-low.
- RDR2: Rockstar's own figure of about 60 hours (reported as 60 to 65) appears in Game Informer, 15 Oct 2018 (https://gameinformer.com/2018/10/15/rockstar-games-reveals-new-details-about-red-dead-redemption-ii-including-game-length) and others, snippet only. Developer-stated, but a marketing number.
- Sleeping Dogs: nothing found.

## Gaps to chase from this PC (not reached, so not evidence)

1. Eurogamer/Digital Foundry "The Lag Factor" (2009) and later Digital Foundry latency method pages.
2. Celia Wagar hit-stop writing; Steve Swink "Game Feel" (book); Capcom hit-stop talks.
3. Nesky's Journey camera talk; Naughty Dog and Ubisoft motion matching talks (run speed, start/stop times).
4. Any camera-tracking method for FOV from footage; test it on a known game.
5. Splinter Cell and Hitman detection-range tests; any chase measurement.
6. A direct HowLongToBeat page for each game; any timed playthrough of GTA V or Mafia with a cut scene total.
7. Open-world telemetry papers in the Springer chapter and Loria thesis listed above.
