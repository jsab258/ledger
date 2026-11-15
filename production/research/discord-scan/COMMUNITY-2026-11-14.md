# The ArtCraft community: what it does and thinks, and what LEDGER can learn (15 November 2026)

His question (14 Nov 22:10): the general conversation, new ideas, interesting approaches, ambitious projects, level of sophistication. Read by the advisor on his direct ask (15 Nov 07:07, pick A), in his PC's Chrome, read-only, 07:10 to 07:35. Own words only; no usernames; nothing posted, joined or downloaded. Everything below is what people said or showed there; nothing was measured.

Read: game-development in full (126 messages, 5 to 14 Nov; nothing older loads); general for the last 12 hours only (574 messages; the channel runs about 50 messages an hour, so two weeks would be some 15,000); announcements from 31 July to 13 November (42); craft-apps from 12 to 15 November (239); and the server-wide search for AAA, open world, MMORPG, Unreal Engine, subagents, workflow and parity (newest page of each, 136 messages after duplicates). Not read: share-your-artcrafts (mostly pictures), the forum threads beyond what search reached, introduce-yourself beyond search hits, anything older in general.

## 1. Who is there and how serious

- Huge and mixed. The server announced 170,000 members by 23 October; ArtCraft claims 33 million downloads and over 65,000 GitHub stars (9 October); about 4,000 people have contributed code (said in general; one app shows over 500 contributors).
- Most voices in general and craft-apps are users asking basic questions (how to export, will it run on Android) and requesting clones of other software. A visible minority are professionals: an AAA game designer, architects and CAD users with 20 years' experience, 3D artists, a UI/UX lead, people running game private servers.
- The serious work is in the tool threads, not the chat: people reporting parity percentages, fixing printer gradients against an industry test suite over several days, writing node-by-node parity tables.

## 2. The most ambitious projects

- ArtCraft itself: a clean-room, AI-written (Claude Code) rebuild of the Adobe and Microsoft suites in Rust: PhotoCraft, VectorCraft, FilmCraft, EffectCraft, WordCraft, GridCraft, CADCraft, AniCraft and more, plus Craft Anything (1 Nov), an app that reverse-engineers or builds any program clean-room. The founder said PhotoCraft is at about 60% parity with Photoshop (talk at the AI Engineer Code Summit, 13 Nov); a public parity tracker exists; one user notes the overall figure has sat at 62% for a month.
- Community apps on the same pattern, now in ArtCraft's launcher: SolidCraft (CAD), MailCraft (an Outlook-like client by a company), TextureCraft, UvCraft (a RizomUV-like UV editor), Penumbra (TouchDesigner-like), a VS Code rewrite in Rust, an ERP aiming at Odoo parity, a Paint.NET clone driven by parity tests.
- Games and engines: MistyEngine (open source, aiming at Unity's ease and Unreal's look; v0.3.1 claims early Lumen and Nanite-like features, world streaming, visual scripting, templates); an MMORPG in Unreal 5.8 by someone who already runs a long-lived private server with players to test on; a small engine with HTML and CSS interfaces and Python scripts; browser games, an EGA-to-WebGL remastering text adventure, retro conversions (a SNES game moved to Unreal with Claude Code).
- Said, not seen: the founder mentioned someone in the community using about 40 machines to rebuild Unreal Engine with AI; nobody in the threads knew who.
- Nobody shows an AI-built game anywhere near AAA. "One-shotting a playable AAA-style game" is used in the chat as the imagined test that would show the difference between frontier models, not something anyone has done.

## 3. Approaches and ways of working

- Clean-room by two teams of agents ("Chinese wall"): one team reads the original (code or behaviour) and writes a specification; a second team, which never sees the original, builds from the specification. Used to stay legally clean when learning from code they may not copy.
- Parity measured, not felt: parity tables per feature or node (MaterialCraft keeps them in markdown), parity tests that fail until matched (Paint.NET clone), standard industry test suites as the judge (PdfCraft against the Ghent print test pages), a public parity tracker for the whole suite.
- Their rule of thumb for parity: the first 80% is easy, the next 15% harder, and the last 5% needs a lot of human intervention; triage bugs (important ones first, the long tail last).
- Model split: a frontier model plans and writes the tests, cheaper models implement ("start with Fable 5.2, run the subagents as Opus 5.5 or less"); some put free or cheap models (DeepSeek and others) under a Claude orchestrator for small tasks. A counter-view: subagents lose context and do worse than one agent on the whole problem.
- Token savers they recommend: a code index server so the agent searches the codebase instead of reading it whole (jcodemunch-mcp), a test-first coding skill (superpowers), and loading fewer tools per step (the agent app's many tools burn tokens).
- Everything scriptable: new apps expose an MCP server, and one describes a single command bus so the interface, the command line and AI agents behave identically.
- Agents running around the clock on one app ("my agents keep working on it 24x7").

## 4. New ideas for LEDGER, Kiln and the recipe

1. Clean-room learning from code we may not copy: if FoldCraft (or any useful tool) turns out to be GPL, a helper reads it and writes a plain specification of the method; a fresh fixer that never saw the code builds Kiln's version from that specification. It fits our rule (GPL used as a tool only, never copied into Kiln). This is a known technique, not legal advice.
2. A parity list for Kiln against Marvelous: the capabilities LEDGER needs from Marvelous (layering, sewing, fabrics, pressing, poses, export), each passed or not, beside M7's garment count. It makes the 26 November decision concrete and shows the last 5% early.
3. A standard test suite as part of Kiln's judge, where one exists for cloth (published cloth benchmark scenes, ClothCraft's settling fixtures), beside our own garments.
4. Expect the last 5% to need more than the loop: plan for it (the sitting skirt, the cuffs) rather than be surprised.
5. A code index for the fixer helpers, so each fresh fixer searches Kiln's code instead of reading it whole: a cheap test of whether it cuts the fixers' cost.
6. A cheaper implementing model under the planner, already our rule (Opus plans, Sonnet extracts); the community goes further with free models, which our allowlist and his provider ruling would have to admit first.

## 5. Where LEDGER and Kiln stand

- Ahead: in ambition and rigour for a game. Nobody there is building anything like a photoreal 1990 port town with live talk; none shows specs, locked judges, held-back jobs, independent reviewers or a nightly packaged walk. Their quality checks are parity percentages and users' bug reports.
- Level: Kiln's loop is the same idea as their crafted apps (AI writes the tool, tests decide), and our judge is their parity test by another name.
- Behind: in scale. ArtCraft has thousands of contributors and machines running agents around the clock; a single person is said to use 40 machines. And in openness: they publish parity and progress, which brings in help and checks.
- Worth copying now: the clean-room split (idea 1) and the parity list (idea 2).

## 6. ArtCraft's direction and the debates of the moment

- Direction: from a video-generation service (summer announcements were about a paid video model) to the open-source suite (October), Craft Anything (1 November), a launcher open to community apps, Linux packages, a docs wiki, a public parity tracker and a founder's conference talk.
- Debates: whether AI-written software is "slop" (the common answer there: slop is a human failing, not an AI one); whether clean-room AI reverse engineering is legal and where it ends (games are raised); claims that Anthropic and OpenAI have banned reverse-engineering tools (unverified); how ArtCraft pays for its tokens (subscriptions plus thousands of contributors; a claim of 2.5 million dollars raised, unverified); "get it while it's cheap, subscriptions will reach 700 dollars a month"; Fable 5.2 against Opus 5.5 (Fable keeps the big picture better; Opus gives perfect results if wrangled well).
