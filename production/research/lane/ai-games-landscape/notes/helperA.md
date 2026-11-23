# Helper A: AI-agent-built games, factual record (researched 23 Nov 2026)
Method: WebSearch (standard) then WebFetch on URLs from my own results. "SR" = self-reported by the maker. Unreached: gamestar.de review article (fetch failed, client error); Steam homepage returned for app/4095390 (wrong page). No X posts read directly; X content is only as quoted by articles. Mafia games and GTA VI story not used. Time-limited: ~30 min, so several leads are thin.

## A. THE SIX LEAD PROJECTS

### 1. Age of Dragon
- Who: Mike Houser (says "no idea how to code"; works at Tesana, a platform named in his own pipeline; reportedly quit job 2 months earlier, spent last $1,400). 
- When: X thread ~10 Nov 2026; article 11 Nov 2026. Source: https://explainx.ai/blog/age-of-dragon-ai-open-world-rpg-vibe-coded-fable-5-2-opus-5-5-three-js-2026 (Yash Thakker, 11 Nov 2026; all figures SR, not verified by the article).
- Models/tools: Claude Fable 5.2 and Opus 5.5 (code, orchestration); three.js (browser); Blender driven by Claude (rigging/animation); Tripo (400+ models); ElevenLabs via fal (voice, SFX, music); Tesana.
- Team: 1 person. Time: about 4 days (SR). Cost: $1,400 personal spend (SR); models from one max-tier subscription (SR).
- Scale (SR): 12x12 km island (144 km2), 6 regions, 79 places, 9 dungeons, 34 quests, 56 enemy types, 20 bosses, 482 3D models, 694 animations, 544 voiced lines, 772 SFX, 37 music tracks, ~80,000 lines code, 85,000+ tool calls, 21B+ tokens. Article notes the "2x Skyrim" claim depends on the measure (could be ~4x).
- How: art first (each landmark began as a painting/concept image, then became a place); agent loop write module, run game, read console, fix; Claude rigged creatures in Blender on one shared skeleton, mocap library retimed per body. Number of agents, tests, drift controls: not found.
- Story/characters: regions named (Frostcrown Reach, The Ashen March); no story detail found.
- Quality evidence: 1:56 video, 150,000+ views in hours (SR). No public playable build or repo confirmed by the article. Evidence weak.
- What went wrong / caveats (article's, not the maker's): stats SR and maker works for a named vendor; flyby video cannot show combat feel, pathing, balance, bugs, load times; asset licences unchecked; audio tone drift over hundreds of files without a voice sheet; single-vendor dependency; security risk of unattended agents.
- Would do differently: not stated by Houser; article advises start small (one region, five quests, one boss, one skeleton), fix visual style first, many small fix cycles.

### 2. GT-Caliber
- Who: Ziwen Xu, 25, founder of Hyperecho (AI agent startup); solo.
- When: began 10 Jun 2026. Sources: Wccftech, Francesco De Meo, 19 Jun 2026 (updated 25 Jun) https://wccftech.com/dev-building-gta-6-ai-wrong-city-unreal-engine-5-8/ ; TweakTown, Hassam Nasir, 18 Jun 2026 https://www.tweaktown.com/news/112266/solo-dev-tries-to-make-his-own-gta-6-with-ai-as-he-got-tired-of-waiting-for-rockstar/index.html
- Models/tools: upgraded to Claude Max 20x (TweakTown); "AI agents in a loop"; Godot, then Unreal Engine 5 (day 7), tried UE 5.8 with its MCP (day 9). Specific coding tool not named in either article.
- Time: ~12 days at time of Wccftech piece; final outcome not found. Cost: only the Max 20x plan mentioned; no figures. Team: 1 plus agents; agent count not found.
- Timeline (Wccftech): day 1 a blue box on an empty plane (TweakTown); day 2 agents built Los Angeles instead of Miami; day 3 NPCs, traffic, shadows/reflections from community requests; day 7 Godot to Unreal; day 8 Mac crashed because all agents opened the game at once to screenshot, NPCs lost walk animations, agents added an in-game phone; day 9 UE 5.8 MCP slowed work.
- Workflow: public daily updates, open GitHub repo, agents take community feature requests and open pull requests (TweakTown). Art pipeline details: "AI tools produced much of the asset creation" (TweakTown), tools not named.
- Quality evidence: none independent beyond news coverage of progress; no playable build found.
- Went wrong: wrong city; machine crash from parallel screenshots; animation regression; UE 5.8 MCP slower. Xu quote: "The 5.8 MCP isn't like crazy good, and it actually slows the build down... The loop runs better without it." (Wccftech).
- TweakTown says he switched engines three times and ended on Unity; Wccftech says Godot to Unreal. The sources conflict; unresolved.

### 3. World of Claudecraft
- Who: Levy Street (New Zealand studio; GitHub levy-street/world-of-claudecraft per PC Games Hardware); dev.to account "WorldofClaudecraft".
- When: initial build over one weekend, press release 22 Jun 2026 (Notebookcheck). Claude Fable 5 launched 9 Jun 2026 and access was suspended 12 Jun 2026 per Notebookcheck.
- Sources: Notebookcheck 24 Jun 2026 https://www.notebookcheck.net/World-of-ClaudeCraft-AI-builds-MMO-in-2-days-here-s-why-gamers-aren-t-impressed.1327938.0.html ; PC Games Hardware 26 Jun 2026 https://www.pcgameshardware.de/Kuenstliche-Intelligenz-Hardware-279517/News/World-of-ClaudeCraft-MMORPG-WoW-KI-Browsergame-1546503/ ; dev.to post "Jun 23" (year inferred 2026) https://dev.to/woclaudecraft/i-have-been-building-an-open-source-mmorpg-mostly-with-claude-it-just-shipped-its-first-10-man-raid-59k1
- Models/tools: Claude Fable 5; TypeScript, Three.js, WebSockets, PostgreSQL (PCGH, from project docs). Free browser game, desktop and mobile; open source.
- Scale: 9 classes, 3 zones, nearly 90 quests, dungeons, PvP, trading, groups (Notebookcheck). v0.12.0 added Nythraxis, first 10-player raid (dev.to). "Over 30,000 active players" per PCGH (SR/developer, 26 Jun 2026). Lines of code and cost: not found.
- How: vibe coding; PCGH says many visible assets are free/licensed packs, terrain/effects/sound/icons procedural, so not 100% AI. Agents, tests, drift controls: not found. Content cadence: zones, then dungeons, then a raid (dev.to).
- Quality: independent coverage exists (Notebookcheck, PCGH, t3n, mein-mmo). Winfuture (cited by both) called code partly unstructured; Reddit commenters call it a proof of concept (scalability, netcode, DB, security). A Steam listing is mentioned in a playtoearn.com headline only (not fetched).
- Went wrong (dev.to author): loot broken for half the 10-man raid because PARTY_MAX was still hardcoded to 5 from dungeon code; no error or crash. 
- Author's lessons: scope, not speed, is the constraint; AI moved the bottleneck but diagnosing bugs is not fast; regular content releases beat one big launch.

### 4. Codex Mortis
- Who: GROLAF (solo dev); publisher CRUNCHFEST. Survivors-like deckbuilder / necromantic bullet-hell roguelite.
- When: first commit Jul 2025; free demo Steam 9 Dec 2025; Early Access 26 Mar 2026; v1.0 24 Sep 2026 (press release https://www.gamespress.com/The-AI-Made-Game-the-Internet-Told-You-to-Hate-Is-Out-of-Early-Access- ; publisher's, promotional).
- Steam reviews: 81% positive of 98 user reviews, "Very Positive" (Steam page https://store.steampowered.com/app/4084120, read 23 Nov 2026). Price $3.99. AI disclosure on page: "AI is used for entire code of the game, text, arts, sounds and music." Earlier: press release 21 May 2026 said "Very Positive", 80%+, count not given (https://www.gamespress.com/CODEX-MORTIS-Drops-Mutations-Update-at-80-Positive-on-Steam).
- Models/tools: Claude Code, mostly Opus 4.1 and 4.5 (TweakTown, undated, from a developer Reddit post); art made with GPT; TypeScript, PIXI.js, bitECS, Electron (TweakTown). Press release: custom JavaScript engine the AI could read and run through text, because an off-the-shelf editor/engine suited the workflow badly; an instruction file (the dev calls a blunt "angry user" one helpful).
- Time: ~3 months outside day job at the demo stage (TweakTown); ~3,450 commits and 350,000+ lines TypeScript Jul 2025 to Sep 2026 (press release, SR). Cost: not found.
- Scale at 1.0 (press): 10 magic schools, 200 spells, 31 heroes, 4 new levels, 4-player online co-op. 10,500 demo players, avg session 71 min, peak 322 concurrent (SR).
- Quality/coverage: PC Gamer, TweakTown (https://www.tweaktown.com/news/109355/codex-mortis-is-a-100-ai-made-roguelite-bullet-hell-and-its-proving-divisive-as-hell-too/index.html), Gigazine (15 Dec 2025), Creative Bloq, Xataka. Early reaction divisive: inconsistent art direction, poorly received AI promo video, "slop" objections. Reviews improved by 2026 per Steam count. Evidence of Steam rating: sure (read on page); count is small (98).
- Dev lessons (press): "Define the task, delegate it, review the result"; quality depends on the people, not the tool; 20+ community patches in 6 months of Early Access. Trailers' AI look was deliberate to provoke reaction.

### 5. Godot fishing game (Sept 2026)
Two overlapping sources, possibly the same project; not confirmed to be the same person.
- (a) Shazoo, 11 Sep 2026 https://shazoo.ru/2026/09/11/190442/za-sest-nedel-ii-na-dvizke-godot-sobral-polnocennuiu-igru-pro-rybnuiu-lovliu : creator "Hakim Eiqbal", no game-dev experience; playable build at week six; Claude wrote all Godot code; Claude and "GPT-6 Astra" (joined later) make 3D assets; Tripo3D for characters; new islands, docking, fishing progression, lighting; distributed via SwissTransfer, no store page; cost unknown; commenters praise water/atmosphere, suspect performance issues; others dismiss it. Evidence: weak (maker claims plus comments).
- (b) Reddit r/ClaudeAI "Week 3 of making my fishing game entirely with AI" by u/RUSuper, 18 Aug 2026, via https://explainx.ai/blog/r-claudeai-fishing-game-godot-blender-mcp-week-3-august-2026 (SR, unverified): Godot 4.7.1 + Godot MCP, Blender + Blender MCP; Claude Desktop weeks 1-2, Claude Code week 3; ChatGPT for concept art/mockups; Rodin mesh tool tried and dropped (heavy cleanup); $200 Max plan, first two weeks hit the limit. Workflow: separate sessions for art direction, geometry (Blender MCP scripts), integration (Godot), plus a dispatcher chat; in-game camera screenshots as the test; scored critics, ship only at 8+/10 with blind A/B; each decision tagged USER or AI in a log. Problems: islands approved from overhead looked like "pancakes" from player camera; resemblance to Dredge; HUD unfinished. Lessons: do not ask the model if an image is good, human approves; test from the real game camera; write critic criteria first; build UI last. No playable demo then; about 617 upvotes.
- Team: 1. Lines of code, map size: not found.

### 6. ~100k-line Unreal game, all-AI assets (Apple developer forums)
- Threads: https://developer.apple.com/forums/thread/834043 ("...Unreal Engine game in 2 months with all-AI assets") and https://developer.apple.com/forums/thread/834020 (shorter title). Author name and post date: not shown in fetched text.
- Content: solo dev, ~2 months; Unreal Engine C++ and pipelines, 100k+ lines; "thousands of 3D/UI assets" AI-generated; "various AI models", unnamed; iOS TestFlight closed beta. Game: tactical mobile match-3 puzzle with gimmick bosses, irregular/non-Euclidean boards. Dev designed the core math, pacing and boss counters; AI supplied "brute-force production muscle."
- Asks for feedback on thermals/performance in chain reactions, whether AI assets feel cohesive or "uncanny valley". No replies visible, no problems/lessons stated, cost not found. Evidence: none beyond the post (weak). (Not an open world; a mobile puzzle.)

## B. MORE PROJECTS FOUND

### 7. Fire Field / Firefield
- Who: Naoki Fujinaga, 45, Japan, no programming experience (Der Standard, ~21 May 2026, partial text) https://www.derstandard.at/story/3000000321527/firefield-angespielt-wenn-die-ki-diablo-programmiert ; Steam lists developer Robe of Fire, solo.
- Diablo-like action RPG, procedural dungeon, 8 floors in Early Access. Early Access 8 May 2026, $9.99. Steam: 70% positive of 24 reviews, "Mostly Positive" (https://store.steampowered.com/app/4527100/Firefield/, read 23 Nov 2026). Steam disclosure: most content made with AI generation tools, no AI during play, small share of hand-crafted assets, dev reviewed all AI content.
- Built in ~3 months by one person (Der Standard). Models/tools, cost, code size: not found. Der Standard teaser mentions "two catches", not read.

### 8. 100 Bodies in the Grass
- Reddit user Ok-Pirate5732 (r/ClaudeAI), via Shazoo 11 Nov 2026 https://shazoo.ru/2026/11/11/193847/entuziast-ii-bez-opyta-razrabotki-igr-s-pomoshhiu-claude-sozdal-kooperativnyi-eksen-o-mongolskom-vtorzenii-vo-vetnam-1287-goda
- 4-player co-op roguelike action, 1287 Mongol invasion of Vietnam, three acts; Godot; Claude Code wrote most code and could test and read Godot docs; Blender with Claude for small model fixes; Meshy for initial models (heavy manual rework); Steam networking. Steam page exists, no release date. Time/cost: not found.
- Problems: animation is Claude's weak point (done by hand or with ready-made animations); complex Blender work unreliable; game feel must be tuned by hand. Dev said architecture was surprisingly stable.

### 9. Battle Drones (Simon Willison) and other web games
- Simon Willison, 20 Oct 2026 https://simonwillison.net/2026/Oct/20/battledrones/ and 28 Oct 2026 https://simonwillison.net/2026/oct/28/vibe-game-development
- Battle Drones: C&C-style RTS, TypeScript; v1 July with Fable 5, later Opus 5.5 via Claude Code ("Ultracode" mode orchestrating many subagents); OpenAI image API for sprites; 12 iterations, 321 commits; 2-4 player multiplayer, replays, 7 maps, LLM-vs-LLM matches; author reviewed almost no code. Tests: 1,000+ simulated playtests used to rebalance; 1,200 AI-vs-AI matches cut undecided games after 25 min from 14% to 0.9%; replay/debug tools. Problems: audio-based multiplayer gave tester a headache; WebRTC failed so WebSocket relay on Fly.io (~$2.19/month est.); Math.sin/cos differed across browsers and desynced replays; Ultracode burns tokens. Open source Apache 2.0. Other projects (Emberwick RPG ~15 min story, Pumpkin Farmer ~2 days from a spec file) built in at most ~4 hours of his time each. Willison's lessons: playtesting still needed; story/state bugs (NPC in wrong place); expects backlash to AI assets.

### 10. SpaceMolt
- Ian Langworth; Decrypt 10 Feb 2026 https://decrypt.co/357657/spacemolt-multiplayer-game-built-exclusively-ai-agents?rand=52368
- Multiplayer game played by AI agents (humans watch). Claude Code wrote ~59,000 lines Go + 33,000 lines YAML over a weekend (SR); he has not read the code; bug reports are researched, fixed and deployed by Claude Code automatically. 350+ agents, 505 star systems at the time. Cost, model: not found. Risk (article): unseen code, auto-deployed fixes.

### 11. Era Online (1999 MMORPG revived)
- Kyle Easterly, Delve Group; Code w/ Claude, San Francisco, 7 May 2026 https://claude.com/code-with-claude/session/sf-ext-era-online-resurrecting-a-1999-mmorpg-with-claude-code
- One person plus Claude Code; original VB6 game; Claude explored the old game first, built its own tools, then ported to a modern stack "with remarkably little friction." Key lesson: up-front context-building. Metrics, cost, quality evidence: not found (talk abstract only).

### 12. Grumbulus (storm-cloud browser game)
- Grigory Sapunov (Gonzo ML) with his son, 25 Mar 2026 https://gonzoml.substack.com/p/how-we-built-a-full-browser-game
- Claude (version unnamed); vanilla JS/HTML5 Canvas; CLAUDE.md with rules; ~15,000 lines, 25 files; 24 pedestrian types, 35 achievements etc.; about two days. Files generated by parallel agents caused API mismatches; Claude caught 18 integration bugs pre-playtest. Bugs: bosses designed but never implemented (silent call to non-existent method), 15 behaviour flags never read, Thor drawn in wrong coordinate space (six attempts), CDN caching. Lessons: play early, describe the problem not the fix, integration audits, checklist beyond CLAUDE.md, analytics from day one. Cost: not found.

### 13. The Librarian 2
- Unnamed YouTuber; MindStudio 13 Aug 2026 https://www.mindstudio.ai/blog/librarian-2-vibe-coded-3d-game/
- 3D roguelite from a spoken prompt; Claude Code/Opus ran ~90 min, GPT Codex 5.6 for fixes and balance; markdown design doc as shared context between models; GitHub for restore; ~10,400 lines, 33 modules, no external assets. Claude Code took screenshots and fixed a camera bug itself. Bugs found by human: reversed controls, missing back button, soft lock, untested balance. No automated test suite mentioned.

### 14. Failed attempt: vibe-coded metroidvania (Godot)
- lpshred, Godot forum, 23 Apr 2026 https://forum.godotengine.org/t/post-mortem-of-my-failed-attempt-to-vibe-code-a-metroidvania-game/137567/1
- ~40 hours over months; Gemini planning, Replit then Cursor, Cline/Continue, Godot/HacknPlan/GitHub MCP servers; later separate AI personas, per-feature chats, milestone roadmap. Combat broke, hotfixes broke more, 16x16 to 32x32 migration broke code; player script grew too big, "state machine" was a global variable; abandoned. Lessons: full vibe-coding "largely a myth" for current models; agents struggled with more than 2-3 scripts; early success masks fragile foundation; adversarial AI review was useful.

### 15. Gangland-style RTS clone (Godot, Claude Code)
- Lucca Sanwald (datadeer), dev.to 22 Jun 2025 https://dev.to/datadeer/part-1-building-an-rts-in-godot-what-if-claude-writes-all-code-49f9
- Claude Code only (Pro plan, ~$20/month, likely Sonnet 4 per comment); markdown design files as ground truth; conflicting context broke the character controller; per a comment the author later scrapped it, having lost control of the code. ~8 hours at time of writing.

### 16. Unreal Engine 5 action RPG, AI-assisted (human-led)
- "Lirnith", Epic forums, 21 Jun 2026 https://forums.unrealengine.com/t/ai-assisted-solo-development-of-a-modular-unreal-engine-5-action-rpg/2730299 . AI for architecture, C++, review; human owns design and validation. 11 GitHub technical breakdowns. Models, problems, lessons: not found.

### Leads not read (for a later pass)
- Era-related and similar: "Chickens. Chickens? Chickens!" small Steam game (LinkedIn snippets only); Duckov Explorer (Product Hunt, WebGL roguelike); VibeGame (Hugging Face blog https://huggingface.co/blog/vibegame); Cinevva "solo devs shipping real games" (22-23 Mar 2026); Epic using AI to write Unreal Engine code (not a game); PC Gamer on AI stigma cutting Steam reviews ~53% (data-analyst claim, unread); GDC Vault 2026 AI sessions; "Opus 4.8 builds RPG" (Ethan Mollick demo, tabletop RPG, secondhand) https://dev.to/gentic_news/opus-48-builds-full-rpg-in-claude-code-with-zero-feedback-33jh .

## C. PATTERNS SEEN (facts only, from the sources above)
- Most numbers (days, lines, cost) are self-reported; only Codex Mortis and Fire Field have Steam ratings with counts (98 and 24 reviews).
- Only Codex Mortis shows a long-run (14 months, 3,450 commits) agent project with a shipped 1.0.
- Reported failure modes: hardcoded constants not updated across features (Claudecraft PARTY_MAX); features designed but never wired (Grumbulus); large single scripts defeating the agent (metroidvania); parallel agents crashing the machine and API mismatches (GT-Caliber, Grumbulus); engine MCP slowing work (GT-Caliber); overhead-only approval missing the player camera (fishing); animation and game feel left to humans (100 Bodies); cross-browser maths desync (Battle Drones).
- Controls reported: markdown ground-truth/design docs and CLAUDE.md (Grumbulus, datadeer, Librarian 2); instruction file (Codex Mortis); decision log tagged USER/AI and scored critics (fishing); simulated playtests and AI-vs-AI matches (Battle Drones); screenshots from the in-game camera (fishing, Librarian 2).
