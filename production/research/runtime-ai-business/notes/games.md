# Shipped games with live LLM / generative AI during play — pricing, costs, failures, reception

Research date: 2026-09-24. Bounded web research; nothing bought, signed up for or downloaded.

Legend for each figure:
- OPENED = page fetched and read; SNIPPET = search-result text only, page not opened (or opened but blocked/truncated).
- DEV = measured/reported by the developer (or their vendor quoting them); 3RD = estimate by a third party; PLAYER = player report; DERIVED = my own arithmetic from cited numbers.
- Steam figures read from the Steam store page on 2026-09-24 unless stated (prices shown in CHF because the fetch came from Switzerland).

---

## 0. The few hard cost numbers that exist (all of them)

| Game / product | Figure | Kind | Source, date | Status |
|---|---|---|---|---|
| AI Dungeon (Latitude) | ~US$200,000/month on OpenAI + AWS at the 2021 peak; "about as much" as payroll; under US$100,000/month after moving to AI21 + open models by end 2021 | DEV (CEO Nick Walton to CNBC) | CNBC, 2023-03-13, https://www.cnbc.com/2023/03/13/chatgpt-and-generative-ai-are-booming-but-at-a-very-expensive-price.html | SNIPPET (CNBC returned 403; quoted consistently in two search summaries) |
| Retail Mage (Jam & Tea) | early prototype: a 4-player session cost "the cost of a ticket to Disneyland" ("hundreds of dollars"); after a year of work "dimes" — ~1000x reduction | DEV (CTO J. Aaron Farr, GDC 2025 panel) | GameMakers write-up, 2025-04-02, https://www.gamemakers.com/p/ai-native-games-revolution-or-evolution ; studio blog 2024-03-13, https://www.jamandtea.studio/news/making-retail-mage-a-new-approach-to-ai-in-games | OPENED both |
| Status (Wishroll, AI social sim app) | beta architecture cost US$12–15 per user per DAY; >95% cut after re-architecture; 500K+ DAU, ~1h36m/day | DEV-via-VENDOR (Inworld case study quoting Wishroll) | Inworld, 2025-10-09, https://inworld.ai/case-study/wishroll-status-cutting-ai-costs-by-95-percent | OPENED |
| Death by AI (Playroom, Discord) | peak 1.2 billion text tokens/day and 35M TTS characters/day; 20M players, 3M play-hours in 3 months; reached profitability only after moving off GPT-3.5/4 + ElevenLabs to Inworld + enterprise volume deals | DEV-via-PLATFORM/VENDOR | Discord case study (undated page), https://discord.com/build-case-studies/playroom ; Inworld case study (c.2025), https://inworld.ai/customers/death-by-ai | OPENED both. No dollar figure. |
| Suck Up! (Proxima), early access | 10,000 "AI tokens" per purchase = one per NPC interaction ≈ 40–50 hours; price US$15.99 | DEV | The Magic Rain, 2024-04-19, https://themagicrain.com/2024/04/suck-up-is-a-vampire-game-that-uses-a-i-to-interact-with-its-players/ | OPENED |
| Suck Up! implied ceiling | ≈200–250 interactions per hour; if the whole US$15.99 went on AI, ≤ ~US$0.0016 per interaction, ≤ ~US$0.32–0.40 per hour | DERIVED | from row above | — |
| AI2U (AlterStaff), BYO-key era | a player spending "as much as 9 dollars PER DAY" on his own OpenAI key | PLAYER | itch.io comment (c.2024), https://itch.io/post/9902898 | OPENED |
| Vaudeville (Bumblebee) | "a substantial bill from Inworld" in the first month; no number | DEV (postmortem) | Game Developer, 2024-01-31, https://www.gamedeveloper.com/design/vaudeville-pre-mortem | OPENED |

No shipped game found publishes a cost per player-hour. Every "per player-hour" figure in circulation is a third-party estimate (section 4).

---

## 1. Game-by-game

### AI Dungeon — Latitude (cloud; freemium subscription)
- History (Wikipedia, OPENED, https://en.wikipedia.org/wiki/AI_Dungeon): GPT-2 hackathon May 2019; AI Dungeon 2 Dec 2019 ran up >US$20,000 bandwidth in days and was temporarily shut; Patreon ~US$15k/month (Dec 2019); "Dragon" premium on GPT-3 from July 2020, free tier on smaller "Griffin"; energy system for free players; ads-for-actions June 2022 (backlash), ads removed end 2022.
- Cost: ~US$200k/month peak 2021 → <US$100k/month after switch (see table). AI21 case study (OPENED, 2022-12-19, https://www.ai21.com/blog/latitude-case-study/): moved from Jurassic-1 Jumbo 178B to Grande 17B for speed and cost; no % disclosed.
- Steam: launched July 2022 with a US$30 one-time "Traveler" tier; Dec 2022 "optimized AI costs to the point where we could let ALL free players play unlimited"; Traveler withdrawn Sept 2023; Steam app retired early 2024 (delisted 12 Mar 2024 per Wikipedia). Latitude help page OPENED: https://help.aidungeon.com/faq/what-happened-to-the-travelers-tier. The one-time-price experiment on Steam was abandoned; the business is subscription.
- Pricing 2026 (Arcanum, 2026-08-21/updated 09-11, OPENED, https://arcanumrpgs.com/blog/ai-rpg-cost/ — 3RD reading of the live price page): Free (4k context, ads, unlimited small models) / Journey US$14.99 (8k, 760 credits) / Legend US$29.99 (16k) / Mythic US$49.99 (32k) / Ultimate US$99.99 (32k, 5,200 credits); unadvertised "Shadow" tiers US$246.66–996.66/month. Context length is the main thing metered — i.e. price scales with tokens per call.
- Models now: "a mix of open models — Llama, DeepSeek, Gemma, GLM", which Walton called the best move they made (Arcanum interview, 2026-08-10, OPENED, https://arcanumrpgs.com/blog/nick-walton-interview/). They also fine-tune and open-source their own (Wayfarer 12B/70B, Harbinger 24B on Hugging Face — SNIPPET).
- New product Voyage (TechCrunch 2026-04-21, SNIPPET): free expanded beta; subscriptions US$15/30/50 planned; Gemini Flash + Gemma via Google AI Futures Fund. Walton: pricing is "mostly inference cost"; Latitude "is betting on model prices continuing to fall"; if not, prices rise or margins suffer (OPENED, above).
- What went wrong: April 2021 OpenAI's monitoring caught users generating sexual content involving minors; OpenAI demanded action; Latitude's filter over-flagged ("eight-year-old laptop") and human moderators read private stories; review-bombing and exodus; by Aug 2021 flagged requests were rerouted to Latitude's own weaker models instead of blocked (Techdirt 2021-11-17, OPENED, https://www.techdirt.com/2021/11/17/content-moderation-case-study-game-developer-deals-with-sexual-content-generated-users-own-ai-2021/). Lesson: the platform provider's content policy is a hidden dependency that can force product changes overnight.

### NovelAI — Anlatan (cloud, own models on own rented GPUs; subscription)
- Tiers Tablet US$10 / Scroll US$15 / Opus US$25 per month (NovelAI docs + reviews, SNIPPET). Own models (Kayra; Erato = Llama 3 70B continued-pretrained) served on CoreWeave H100s (CoreWeave 2023-03-21, OPENED — no GPU count or cost).
- Sept 2026: said image model V5 costs "more than twice as much" to run as V4.5, so chose a usage limit ("battery") over roughly doubling Opus; subscription Anlas now expire at period end from 2026-09-21 (NovelAI blog — 403; SNIPPET + dev.to write-up OPENED).
- Outage: compute shortage from 2026-09-18; Kayra and Erato text models temporarily unavailable, restoration hoped for 2026-09-22 (SNIPPET from NovelAI docs/status). A live example of GPU supply risk even for a company that runs its own models.

### Suck Up! — Proxima (cloud: OpenAI; premium one-time price)
- EA on own website from late Dec 2023 at US$15.99 with 10,000 AI tokens (≈40–50h); devs said PCs "not powerful enough" for their models and planned "fair" top-ups (Magic Rain 2024-04-19, OPENED).
- 1.0 on Steam 2025-10-01 at US$16.99; tokens gone. Steam page (OPENED 2026-09-24): "Connects to 3rd-Party Service for AI Content Generation: ChatGPT from OpenAI", broadband required, Mixed 62% of 208. Dev (Hypergrid, 2025-10-31, OPENED): moved from GPT-3.5 after its deprecation, "bounced around many" models, 1.0 on "ChatGPT 5"; no cost figures.
- Sales: ~12K Steam copies / ~US$132K gross since 1.0 (GameRevenueData, 3RD estimate, SNIPPET).
- Went wrong: players say the token-free 1.0 AI is much worse than EA ("early access version was MASSIVELY better", 2025-10-02), dialogue loops, "abandoned" (Steam reviews, OPENED); Steam news 26 Mar 2026 "Server Issues Resolved" — "AI integration that broke with our provider that we didn't catch in time" (OPENED). Pattern: removing the per-use meter appears to have been paid for with a cheaper/weaker model, and players noticed.

### AI2U: With You 'Til The End — AlterStaff (cloud; premium one-time)
- Started on itch requiring players' own OpenAI keys, then paid token packs (~US$9.99 refills per a comment); 2024-10-23 "NO MORE TOKENS": one-time US$14.99, "endless chats", compensation to those who bought refills (itch devlog, OPENED, https://alterstaff.itch.io/ai2u/devlog/730914/leave-nothing-unsaid-no-more-tokens-v052-update). Reason given: players disliked both tokens and API keys.
- Steam 1.0 2026-08-12 (EA from 2025-01-23); Steam lists Azure OpenAI / Gemini LLM / MiniMax TTS; broadband required; 88% of 1,037 all-time, 78% of 169 recent (OPENED 2026-09-24). Critics: repetitive. No cost disclosed. Itch buyers may still use own OpenAI key (SNIPPET).
- This is the clearest shipped case of premium + unlimited cloud chat that is still well reviewed; how the unit economics work is not disclosed.

### Vaudeville — Bumblebee Studios (cloud: Inworld on a GPT model; premium)
- EA 2023-06-30, 1.0 2025-11-28; US$19.99; Mixed 48% of 283 (Steam OPENED). Dev on model: "a human creativity layer built on top of a GPT model" (Steam forum 2023-06-30, OPENED).
- Postmortem (Game Developer 2024-01-31, OPENED): ~7,500 sales; first month "substantial bill from Inworld", Inworld deferred billing a month (Steam pays a month late) then "changed their pricing model immediately afterwards"; service "unreachable on several occasions", notably when MoistCr1TiKal streamed and "hit all the caps"; reviews "evenly split".
- 1.0 review (Drastik Measure 2026-02-25, OPENED, 2/10): 5 s to first sentence, 10–15 s to finish speaking.

### Retail Mage — Jam & Tea (cloud, self-hosted open models on AWS; premium)
- Released 2024-11-12; US$4.99 (CHF 5.49); Mostly Positive 79% of 44 (Steam OPENED). US$3.15M seed (TechCrunch, SNIPPET).
- Cost: "Disneyland ticket" per 4-player session → "dimes", ~1000x, via own GPU fleet, structured generation, sglang (OPENED, see table). AI not used for personalities/quests — authored content, AI only for runtime response.

### Uncover the Smoking Gun — ReLU Games / Krafton (cloud: GPT-4 + Krafton TTS; premium)
- Released 2024-06-23; US$19.99; Very Positive 96% of 414; Metacritic 80; broadband required (Steam OPENED). Short, bounded game (interrogation of robots). No cost disclosed. Best-reviewed cloud-LLM premium title found — short and bounded, so the per-buyer AI bill is capped by design (my inference, not stated).

### Whispers from the Star — Anuttacon (cloud, own fine-tuned model; premium)
- Released 2025-08-14; US$9.99; Very Positive 80% of 1,661; Anuttacon account and broadband required; voice/text/video input (Steam OPENED). Founded by miHoYo co-founder Cai Haoyu (~40 staff, SNIPPET).
- Complaints (Steam reviews OPENED): privacy policy/voice-data rights (most frequent), linear story with few real decisions, character asks too many personal questions. No cost disclosed.

### Where Winds Meet — Everstone / NetEase (cloud; free-to-play MMO-ish)
- LLM chat only on a subset of side NPCs; outputs tied to fixed flags (affection, weekly gifts, some side objectives) (allthings.how 2025-11-18, OPENED; Cinevva, SNIPPET). Model said to be DeepSeek (SNIPPET only, unconfirmed).
- Went wrong: "Solid Snake method" — repeating the NPC's words as questions skips quest conditions (PCGamesN etc., SNIPPET); erotic role-play screenshots with an NPC (Kotaku 2025-12-03, OPENED). No cost disclosed; paid for by F2P cosmetics.

### Fortnite — Darth Vader (Epic; cloud: Gemini + ElevenLabs-style voice; F2P)
- May 2025: live AI Vader answered players; tricked into swearing and slurs within hours; hotfix within ~30 minutes; SAG-AFTRA unfair-labour-practice charge (PinkNews 2025-05-21, PC Gamer, Forbes, SNIPPET). Shows jailbreak speed at scale and union exposure for AI voice.

### Death by AI — Playroom (Discord; cloud; freemium)
- See table. Monetised through Discord subscriptions, one-time purchases and credits; "thousands of subscribers" in month one; profitability credited to lower-cost models + volume deals + routing different game modes to different models (OPENED).

### inZOI Smart Zoi — Krafton (ON-DEVICE, NVIDIA ACE; premium, feature optional)
- EA 2025-03-28. Mistral-NeMo-Minitron 0.5B, on GeForce RTX only (NVIDIA 2025-03, OPENED). ~1 GB VRAM (PC Gamer, SNIPPET); runs on 8 GB RTX 3060/4060, recommends 12 GB (SNIPPET). Developers tried bigger models, settled on 0.5B for responsiveness and performance (SNIPPET).
- Reception (Steam forums, SNIPPET): thought bubbles that don't change behaviour, wrong thoughts, crashes in long sessions, players turn it off for frame rate. Zero server cost; the cost is moved to the player's GPU and the feature is thin.

### PUBG Ally / Ally Duo — Krafton (ON-DEVICE, NVIDIA ACE; inside F2P game)
- Ally Duo beta 17–30 June 2026 in PUBG Arcade (Krafton/press, SNIPPET). Mistral-NeMo-Minitron-2B quantised, min 8 GB VRAM; chose on-device because "network latency and model inference latency often made responses feel too slow" for squad voice comms (NVIDIA dev blog 2026-06-25, OPENED). Not a permanent shipped feature yet.

### Mecha BREAK — Amazing Seasun (NVIDIA ACE demo, Nemotron-4 4B / Minitron 4B, ~2 GB VRAM)
- Shown Aug 2024 (Gamescom). Launched 2025-07-01 F2P, Mixed ~63% (SNIPPET). Studio told Screen Rant (2024-08-23, OPENED) release would have "a full cast of human voice actors". I found no confirmation the AI mechanic NPC is in the live game — treat as NOT SHIPPED unless shown otherwise.

### Verbal Verdict (ON-DEVICE local LLM via LLMUnity; premium EA)
- EA 2024-03-23, US$9.99, min RTX 2060, 9 reviews, no update in 2+ years (Steam OPENED). A local-model premium game that found almost no audience.

### AI Roguelite (hybrid: free cloud tier, optional subscription, BYO key, local models)
- EA 2022-03-02, 1.0 2023-10-25; ~US$14.99 (CHF 16.79); Very Positive 83% of 599 (Steam OPENED). Free cloud models by default; optional monthly subscription for better LLM/images; BYO key via OpenRouter; local via KoboldCpp/LM Studio. Sub price not found.

### Wanderfolk (cloud: xAI Grok; premium EA)
- Steam page (OPENED): EA "2026", price TBD (search says US$6.99, SNIPPET), broadband required, no subscription mentioned. Not yet reviewed.

### EmemeTown (cloud: OpenAI + Llama; F2P EA)
- Steam page (OPENED) shows not yet released; planned F2P with paid content; separate SNIPPET claims EA 2025-06-24 and free — conflicting, unresolved.

### The Oversight Bureau — Iconic Interactive (ON-DEVICE; premium, demo only)
- Full release "2026"; demo on Steam; claims full stack runs on a Steam Deck and "zero ongoing inference costs per player"; article also says ~30% of Steam users have a GPU able to run the full stack (Deconstructor of Fun, June 2026, OPENED — figures not sourced, treat as 3RD/DEV claim).

### Dead Meat — Meaning Machine (NVIDIA ACE on-device SLM per GDC 2025 session title)
- Steam (OPENED 2026-09-24): still unreleased, "2026", yet lists broadband required. Was announced for 2025. Not shipped.

### 1001 Nights / Book of Infinity (cloud: DeepSeek V4 Pro/Flash; F2P planned)
- Steam (OPENED): not released, F2P, broadband required. Earlier builds used Qwen (SNIPPET). Not shipped.

### Hidden Door (cloud; freemium web platform)
- Public launch Aug 2025 (Variety, SNIPPET). Free: unlimited stories/turns in 5 worlds, 1 character chat/day; paid sub price set in-app (not found). Keeps cost and coherence down with authored "trope cards" rather than free generation; pays licensed-IP creators (Arcanum 2026-07-02, OPENED).

### Friends & Fables (cloud; subscription)
- Free 25 turns/day; US$19.95 / 29.95 / 39.95 per month; mix of Gemini, Llama, GPT, Grok and own fine-tunes by task; premium models cost credits (Dungeons Deep 2026-07-20, OPENED).

### Origins — Inworld (cloud; free tech demo)
- Free on Steam 2023-07-27; ~71% of 349 (wasdland, SNIPPET). Complaints: NPCs stop responding, crashes (Steam community, OPENED). Demo, never a product.

### Covert Protocol (Inworld + NVIDIA) and Ubisoft NEO NPC
- GDC 2024 tech demos / prototypes; never shipped (SNIPPET, multiple).

### Character.AI games
- Speakeasy and War of Words, in-app, rolled to paid subscribers and some free users (SNIPPET, undated). No economics.

### Skyrim mods — Mantella, CHIM
- Free mods; player pays their own API (OpenRouter default, free models ~100 requests/day) or runs local (Mantella docs, SNIPPET). No paid commercial Skyrim AI mod found.

### Inworld (vendor) pricing
- Charged per interaction / per production minute (Naavik 2024-12-01, OPENED). Vaudeville shows a price change after launch (2023). June 2026: cut prices >50%, now positioned mostly as voice/TTS + LLM router; Realtime TTS-2 from US$25 → as low as US$5 per million characters (~half a cent per audio minute) (BusinessWire 2026-06-10, 403; SNIPPET).

---

## 2. Patterns (what the record shows)

1. Every cloud title that tried a per-use meter on a one-time price removed it: AI Dungeon Steam (US$30 Traveler → free, then delisted), AI2U (BYO key → tokens → one-time unlimited, with refunds), Suck Up! (10k tokens → unlimited at 1.0). Players disliked keys and tokens; developers then had to lower model cost to survive. In Suck Up!'s case players saw a quality drop.
2. The survivors with real scale moved off the frontier API to cheaper or own models: Latitude (OpenAI → AI21 17B → open models Llama/DeepSeek/Gemma/GLM), Death by AI (GPT-4/ElevenLabs → Inworld + routing), Status (12–15 US$/user/day → cents), Retail Mage (self-hosted, structured generation, 1000x).
3. Subscriptions are the norm where play is open-ended (AI Dungeon, NovelAI, Friends & Fables, Hidden Door, Voyage): US$10–50/month typical, metering by context length or credits for premium models.
4. Premium one-time titles that are well reviewed are short and bounded (Uncover the Smoking Gun 96%, Whispers from the Star 80%, AI2U 88%). None discloses cost.
5. On-device (NVIDIA ACE: inZOI 0.5B, PUBG Ally 2B, Mecha BREAK 4B demo) gives zero server cost and low latency but needs RTX/8 GB VRAM, costs frame rate, and so far delivers thin features that players switch off.
6. Failure modes seen: provider outages at stream spikes (Vaudeville), provider integration breaking (Suck Up! Mar 2026), model deprecation forcing change (Suck Up! GPT-3.5), provider content policy forcing a filter (AI Dungeon 2021), jailbreaks within hours at scale (Fortnite Vader, Where Winds Meet), GPU shortage outage (NovelAI Sept 2026), privacy backlash (Whispers from the Star), union action over AI voice (Fortnite).
7. Recurring player complaints: latency (Vaudeville 5–15 s), repetition (AI2U), loops/quality (Suck Up! 1.0), always-online/accounts, privacy, "abandoned" when updates stop.

## 3. What is NOT known
- No developer-published cost per player-hour for any shipped premium game.
- No disclosed economics for Uncover the Smoking Gun, Whispers from the Star, AI2U's unlimited model, Where Winds Meet, Wanderfolk.
- Suck Up! 1.0's cost per player and why tokens were dropped: not stated by the developer.

## 4. Third-party unit-economics estimates (ESTIMATES — not from shipped games)
- Studios "target US$0.005–0.02 per player-hour" for mid-engagement AI features; heavy NPC dialogue + voice "US$0.05–0.10 per player-hour"; single exchange US$0.001–0.005 (Respan / The Neural Base, 2026, SNIPPET; unsourced course material).
- Lyfe Agents paper (arXiv 2310.02172, 2023, SNIPPET): earlier generative-agent systems ~US$25 per agent per human-hour; their design much lower.
- a16z "Generative AI Revolution in Games" (2022, SNIPPET): about asset generation, not runtime dialogue.
- Naavik "AI NPCs" (2024-12-01, OPENED): no numbers; notes usage-based vendor pricing and emerging fixed-cost/rev-share deals.
- Deconstructor of Fun (June 2026, OPENED): cloud LLM cost "scales linearly with player engagement"; argues for on-device; no numbers.
- Frisson Labs (2026-05-21, OPENED): "the more the player chats → the more the dev has to pay"; qualitative.
- Totally Human (2025-07-13, OPENED): 7,818 Steam games (7%) disclose GenAI, ~20% of 2025 releases; mostly assets, few runtime.
