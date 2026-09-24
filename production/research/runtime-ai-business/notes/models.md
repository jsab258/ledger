# How consumer products pay for AI while people use them: research notes

Compiled 2026-09-24. Nothing was bought, signed up for or downloaded.
Labels: **[O]** = I opened the page · **[S]** = search snippet only, page not opened · **[D]** = my own pull from a public API or page today.
**MEASURED** = counted data · **CLAIM** = stated by the company or a reviewer · **EST** = a third party's estimate.

---

## 1. One-time purchase, developer pays for the AI

- **Suck Up! (Proxima)**. Early access in April 2024 cost USD 15.99, sold on its own site. It came with **10,000 "AI Tokens", about 40-50 hours of play**, and one token was spent on every NPC interaction. The developers said they were "exploring ways to... top up tokens at a fair price" and expected tokens to stop being needed as PCs got stronger. Source: The Magic Rain, 2024-04-19, https://themagicrain.com/2024/04/suck-up-is-a-vampire-game-that-uses-a-i-to-interact-with-its-players/ [O] CLAIM.
  - Steam 1.0 came out on 2025-10-01 at about USD 16.99 / CHF 13.55. It needs broadband and uses OpenAI ChatGPT. Reviews are **Mixed, 62% of 208 positive**. https://store.steampowered.com/app/2726370/Suck_Up/ [O] MEASURED (review count).
  - Reviews say the **token system went away at 1.0 and the AI got much worse** (Oct 2025), that servers were down (Mar 2026), and that the game is "abandoned" (Jun 2026). https://steamcommunity.com/app/2726370/reviews/ [O] CLAIM by players. I found **no developer announcement** of removing the tokens: the Steam news page does not mention tokens [O]. This reads like a cheaper model replacing the capped one, but that is my inference and nobody has confirmed it.
  - Lesson: a hard cap on a paid game was a worry in early access. Removing the cap and dropping to a cheaper model then cost them in reviews.
- **Whispers from the Star (Anuttacon, a studio funded by miHoYo co-founder Cai Haoyu)**. Released 2025-08-14. USD 9.99 on Steam (CHF 10.99), USD 4.99 on iOS at launch. Needs broadband, no cap stated. Reviews **Very Positive, 80% of 1,661**. https://store.steampowered.com/app/3730100/Whispers_from_the_Star/ [O] MEASURED. Players think the developer is losing money on inference (Steam discussion, [S] CLAIM). AWS case study, 2025-08-14: launch traffic reached **10-50x normal** and the models are 50 GB. No cost figures given. https://aws.amazon.com/blogs/storage/how-anuttacon-scaled-ai-enhanced-gaming-workloads-for-whispers-from-the-star/ [O] CLAIM. Best seen as **publisher-subsidised**: a well-funded studio absorbing the cost for a short game.
- **Vaudeville (Bumblebee Studios)**. Released 2023-06-30 using Inworld, a paid cloud service. The developers named "high service costs", the risk of outages or of the service stopping, and the "black box" as reasons to move. An offline beta arrived 2024-10-03. **Local became the default release on 2025-11-28**, and the online version survives only on a beta branch for non-English players and low-end PCs, "to be discontinued". https://steamcommunity.com/app/2240920/allnews/ [O] CLAIM. Reviews Mixed, 48% of 283. Now needs 16 GB RAM minimum, GTX 1050 min, RTX 2070 recommended. https://store.steampowered.com/app/2240920/Vaudeville/ [O] MEASURED. **The closest match to us: a detective game that absorbed cloud costs, found them unsustainable and moved to local.**
- **Where Winds Meet (NetEase/Everstone, free-to-play, 2025)**. LLM chatbot NPCs, with the cost absorbed by F2P revenue. Reached 2M players in 24 hours. Players tricked NPCs into handing over quest rewards (the "Solid Snake method"). PCGamesN / Kotaku / GamesRadar, late 2025 [S]. Press guesses the model is cheap because of scale (EST).
- **AI Dungeon on Steam**. A one-time USD 10 purchase for the "Traveler" benefits, because Valve does not allow ad-supported F2P. **Retired from Steam 2024-03-12.** Wikipedia [O] for the retirement date; the one-time USD 10 and the Valve-ads reason come from a snippet [S] CLAIM.

## 2. Player brings their own API key (BYOK)

- **1001 Nights (Ada Eden)**, itch/Steam. Devlog 2024-05-02: players **must paste their own OpenAI key**. The team called it "the most feasible method" for a small team and says it earns nothing from OpenAI. It points players to OpenAI's USD 5 new-account credit and gpt-3.5-turbo as the cheap option. No alternative offered. https://ada-eden.itch.io/1001-nights-official/devlog/724545/1001-nights-llm-configuration [O] CLAIM.
- **AI Roguelite** (Steam, full release 2023-10-25, CHF 16.79, **Very Positive 83% of 599**). Works out of the box on a **free cloud default** (unofficial free text and image services). Also takes custom endpoints (OpenRouter, LM Studio), local Kobold/Ooba, and an **optional in-game-linked monthly subscription** for better models. https://store.steampowered.com/app/1889620/AI_Roguelite/ [O] MEASURED/CLAIM. It layers every model at once: free, BYOK, local and subscription.
- **Mantella (Skyrim mod)**. Defaults to OpenRouter with your own key. It "can be run completely for free" on OpenRouter's free models (about 100 requests/day) or on a local model. [S] CLAIM, from https://www.nexusmods.com/skyrimspecialedition/mods/98631 (Nexus returned 403, so download counts are **not verified**). There is now a **"Mantella – Player2 Edition"** (nexusmods 179902) [S], a sign that free platform inference is displacing BYOK.
- **Herika (Skyrim)**. OpenAI key, with a cost tracker built into its server, a suggested hard spending limit, and a hotkey to switch to local KoboldCPP. [S] CLAIM.
- **RimTalk (RimWorld workshop mod)**. Tells users to get a free Google AI Studio (Gemini) key. [S]. Workshop stats hit a 429 error and were **not verified**.
- **AIvy (Steam)** sells a separate "Cloud LLM unlock" DLC for BYOK to OpenAI/Anthropic/Gemini. https://store.steampowered.com/app/4805570/ [S]. A paid unlock for BYOK is a model in itself.
- **Scale of the BYOK power-user world**: SillyTavern alone put **369 billion tokens through OpenRouter in the last 30 days** (#4 in Roleplay). Its top models are cheap Chinese and Flash models (GLM, DeepSeek, Gemini Flash), with Claude Opus 4.6 eighth. https://openrouter.ai/apps/sillytavern [O] MEASURED, as displayed 2026-09-24.
- **How many players actually do BYOK: I found no published number.** Download counts for BYOK mods could not be verified (Nexus 403, Steam 429). This is a gap in the evidence.
- **Store policy**: I found no Steam rule against requiring a key or a third-party account. Valve's position in a forum snippet is that owners decide ([S]). Steam requires a **Live-Generated AI disclosure and a description of guardrails** (policy of 2024-01-10), and **bans live-generated adult sexual content**. Game World Observer 2024-01-10 https://gameworldobserver.com/2024/01/10/steam-ai-games-new-rules-pre-generated-live-generated [S] CLAIM.

## 3. Credits, consumables and tokens

- **AI Dungeon credits**. Pay for images and **temporary extra context**. Every tier gets a monthly grant and anyone can buy more. https://help.aidungeon.com/faq/what-are-image-credits [O]. The page gives no prices. Third-party figures: **1,200 credits for USD 9.99, 2,500 for USD 19.99** [S] EST.
- **AI Dungeon "Energy"** (announced 2020-11-06). Rationed free play to cover costs. Latitude expected only **about 7% of users** to be affected. Players reported running out after about 4 hours. It was replaced by **ads in June 2022** after backlash, and the ads were removed by the end of 2022. Blog (dead domain; snippet) [S] CLAIM; Wikipedia [O] for the ads dates.
- **Latitude's cost**: about **USD 200k/month on OpenAI + AWS at the 2021 peak**, falling below USD 100k after moving to AI21 plus subscriptions. CNBC 2023-03-13 (403, [S]) CLAIM by CEO Nick Walton.
- **NovelAI Anlas** buy images only; text is unlimited on every paid tier. Anlas refill each month, and unused ones reset on cancellation (from 31 days after V5). https://docs.novelai.net/en/subscription/ [O] CLAIM.
- **AI RPG platforms** (Arcanum RPGs round-up, 2026-08-21, updated 09-11) [O] CLAIM/EST:
  - ArcQuill: 2-7.1 credits per turn depending on the model.
  - Master of Dungeon: 15 free actions/day, Pro €7.49/mo for 70/day, packs from **€3.09 for 200 actions** up to €239.99 for 20,000.
  - Tabled: **USD 14.99 one-time plus USD 4.99 refills**.
  - NOPOTIONS: 1 credit = 1 turn, 10 free per day.
  - https://arcanumrpgs.com/blog/ai-rpg-cost/
- **Friends & Fables credits** pay only for premium narration and image models. The base AI GM stays unlimited on paid tiers. [O] (below).

## 4. Subscriptions

| Product | Price/month | What the tiers limit | Source |
|---|---|---|---|
| AI Dungeon | Free (Wanderer) / 14.99 / 29.99 / 49.99 / 99.99 | Context 4k / 8k / 16k / 32k / 32k; credits 0/760/1,650/2,750/5,200; memories 25-800; 6- and 12-month discounts; 1-week trial | help.aidungeon.com/memberships-benefits [O] CLAIM, undated |
| NovelAI | 10 / 15 / 25 | Text unlimited on all tiers; context grows by tier (Opus 28,672 tokens); Anlas 1,000 / 1,000 / 10,000; free trial = 50 text generations | docs.novelai.net/en/subscription [O] |
| Character.AI c.ai+ | 9.99 | Speed, priority, no ads, newest model, voice; c.ai+-only games added 2025 | [S]. Revenue about **USD 30M run-rate Jul 2025 → ~50M end 2025** (Sacra, EST) |
| Replika Pro | ~19.99 (69.99/yr); newer Plus 30 and Max 120 | | [S] EST; revenue estimates conflict (14M vs 35M per year), so treat as unreliable |
| Friends & Fables | Free / 19.95 / 29.95 / 39.95 (2 months free yearly) | Free = **5-25 AI turns/day**; paid = unlimited turns, with players per campaign (4/5/6) and credits (100/300/600) scaling by tier | fables.gg blog 2025-12-04 [O]. Raised from 14.95-34.95 in Dec 2025 [S] |
| Hidden Door | Free / 10 | Free = 5 worlds, 1 character chat/day | [S] |
| Steam's own view | | Recurring subscriptions are "not a fully supported feature". Valve: "customer appetite for signing up to be billed on a recurring basis is limited". Prices **cannot be raised**. Usually F2P base but "could also work" with a paid game | https://partner.steamgames.com/doc/store/pricing/subscriptions [O] CLAIM (Valve) |

What the tiers sell: **context and memory length, model quality, speed and priority, and extra modalities (images, voice)**. Message counts are only rationed on the free tiers. Every paid tier of the text-first services (NovelAI, F2F, AI Dungeon's base models) sells **"unlimited" text**.

## 5. Local models shipped with the game

- **inZOI Smart Zoi** (early access 2025-03-28). **0.5B Mistral-NeMo-Minitron**, GeForce RTX only, an optional experimental setting. Nvidia, 2025-03-13 https://www.nvidia.com/en-gb/geforce/news/nvidia-ace-naraka-bladepoint-inzoi-launch-this-month/ [O] CLAIM. Uses **about 1 GB VRAM**; minimum RTX 3060/4060 8 GB, recommended 12 GB cards (PC Gamer / TweakTown / simscommunity [S]). I found no figure for how many players turn it on.
- **PUBG Ally (Krafton + Nvidia ACE)**. On-device **2B Minitron** plus Parakeet speech-to-text plus Krafton's own TTS. **Minimum RTX 2080 Ti/3060 with 8 GB VRAM and 16 GB RAM**; RTX 4070 recommended. Beta ran 2026-06-17 to 07-01 [S] CLAIM.
- **Dead Meat (Meaning Machine)**. Murder-suspect interrogation running **fully on-device** on ACE small models (GDC 2025 talk [S]). Steam lists it for **2026, not yet out** [O].
- **Vaudeville**: see section 1. It went cloud → local, and local runs down to a GTX 1050 / Steam Deck / integrated GPUs [O].
- **Nvidia In-Game Inferencing SDK**: explicitly **hybrid**. Each plugin can run on CPU, GPU or CLOUD behind one API. It added a Qwen3-8B plugin in 2025. https://docs.nvidia.com/nvigi-sdk/1.7.0/docs/nvigi_core/docs/HybridAI.html [S].
- **Who has the hardware (Steam Hardware Survey, Aug 2026)** [D] MEASURED from https://store.steampowered.com/hwsurvey/:
  - **About 78% of Steam users have 8 GB VRAM or more; about 49% have 12 GB or more.** 8 GB alone is 25.7%, 12 GB 13.0%, 16 GB 26.9%, 24 GB 5.4%.
  - **About 20% have under 8 GB.**
  - The survey mixes Nvidia/AMD/Intel, so the RTX-only share is lower.

## 6. Hybrids

- **Free tier + paid tier**: AI Dungeon, F2F, Hidden Door, Character.AI, Master of Dungeon (above).
- **Free cloud default + BYOK + local + optional subscription**: AI Roguelite [O].
- **Local by default, cloud as fallback or legacy**: Vaudeville [O]. Nvidia IGI's CPU/GPU/CLOUD design [S].
- **Ad-supported**:
  - AI Dungeon ads in 2022, pulled within months after backlash [O].
  - Character.AI mid-chat ads: tested Oct 2025, wider rollout Feb 2026, with Reddit threads of 2,000+ upvotes against them [S] CLAIM.
  - **Steam does not permit ad-supported F2P**, which is why AI Dungeon charged a one-time fee there [S].
- **Capped allowance bundled with purchase, top-ups promised**: Suck Up! EA (40-50 h) [O]. Tabled (one-time + refills) [O via round-up].
- **Platform-subsidised**:
  - **Player2** (player2.game) gives games and mods free LLM, TTS and STT with **no API key**, through an app players run.
  - It is paid for by player **patron subscriptions (20% shared with creators) and ads (70% shared)**.
  - It is **distributing USD 2M to about 1,000 developers over 12 months**, weighted by playtime, with a floor of USD 200/month per active game (≥10 DAU and 12 h/day).
  - It has 11,000+ community members.
  - Blog 2025-05-13 and 2025-05-21: https://blog.player2.game/p/building-ai-npcs-with-player2-api , https://blog.player2.game/p/we-are-sharing-2m-revenue-with-1000 [O] CLAIM.
  - Snippet: a free gpt-oss-120b tier plus a daily recharge for premium models [S].
- **Season pass or "server fee" DLC**: **no real example found**. The nearest is AIvy's paid "Cloud LLM unlock" DLC [S]. Steam's season-pass rules mean refunds for undelivered content (Steamworks docs [S]).

## 7. Other models and forces

- **Vendor engineering subsidy**: Nvidia co-develops ACE titles (inZOI, PUBG Ally, Naraka, Dead Meat). The price is being tied to RTX hardware [O/S].
- **Middleware price cuts**: Inworld cut prices **more than 50%** on 2026-06-10 and said consumer AI was "priced out". One client (Wishroll) cut AI costs 95%. BusinessWire [S] CLAIM.
- **B2B revenue sharing with creators** (Hidden Door pays world-builders; Player2 pays developers) [S].
- **Shutdown and regulation risk for server-dependent games**:
  - The "Stop Destroying Videogames" EU citizens' initiative was submitted 2026-01-26 with **1,294,188 verified signatures**.
  - The Commission's reply of 2026-06-16 declined a legal duty to keep games playable but promised an **industry code of conduct process by end-2026** and guidance on consumer rights under the Digital Content Directive.
  - Lewis Silkin 2026-06-24 and EU ECI page [S] CLAIM.

## Player attitudes

- **Quantic Foundry** (n=1,799, Oct-Dec 2025, published 2025-12-18/22):
  - **85% negative on generative AI in games, 63% "very negative"**.
  - **AI-generated dialogue 83% negative**, quests 77%.
  - Dynamic difficulty is the only use viewed favourably.
  - Nick Yee calls the skew rare; blockchain games scored 79% negative in 2024.
  - Via gamesmarket.global [O]; quanticfoundry.com returned 403. MEASURED (survey).
- **arXiv 2608.11539** (Aug 2026): across 508,192 Steam reviews, games that disclose generative AI get **lower recommendation rates than procedural-generation games (a gap of about 17.9 points)**. Players read AI as "low developer investment". [O] for the abstract; the 17.9 figure is [S]. MEASURED.
- **Ownership and subscription backlash**: Ubisoft's Philippe Tremblay said players must get "comfortable" not owning games (GamesIndustry.biz, Jan 2024), and the reaction was overwhelmingly negative (Gizmodo/MobileSyrup 2024-01-17 [S]). Valve's own note on recurring billing (above) is the most direct evidence on appetite [O].
- **Preferences**: MIDiA 2024 (n=9,000): **53% of gamers prefer single-player** [S] MEASURED.
- I found **no survey that asks directly about a recurring fee on a single-player game**. This is a gap.

## Heavy players (these drive an absorbed-cost bill)

- **GameDiscoverCo, 2025-08-01**, lifetime Steam playtime of the top 250 games per tag. Medians against averages: **JRPG 7.5 h vs 21.4 h (2.9x); Grand Strategy 6.6 h vs 29.1 h (4.4x)**. Survival 7.0 h median, action RPG 5.9 h, base-building about 5 h, metroidvania 3.5 h. https://newsletter.gamediscover.co/p/which-game-genres-get-the-most-playtime [O] MEASURED. **An average 3-4x the median means a thin tail of very heavy players.**
- **Mobile, 118 billion hours** (Scientific Reports 2023): **the top 1% of players account for about 45% (±8%) of all playtime** in a region. https://www.nature.com/articles/s41598-022-26730-w [S] MEASURED.
- **Completion rates**, from Steam global achievement data for 19 single-player games (Two Average Gamers, Jun 2026): **median 36% finish**. Witcher 3 22%, Elden Ring 24%, Cyberpunk 36%, Stanley Parable 74%. https://www.twoaveragegamers.com/game-completion-rates/ [O] MEASURED (secondary compilation; percentages are of owners).
- My own pull today from Steam's public achievement stats [D] MEASURED:
  - **Detroit: Become Human**: 87.9% of owners "played the first chapter", mid-story achievements about 40-48%, the rarest endings under 7%.
  - **Disco Elysium FC**: the most common achievement is held by only 32.5% of owners; "Recruit Kim" 18.6%.
  - A **Crusader Kings III** achievement shows 61% of owners got far enough to earn it.
- **SteamSpy no longer reports playtime.** Today the API returns 0 for average and median playtime on every title I tried (Disco Elysium, inZOI, Stardew, RimWorld, CK3, Detroit, Balatro) [D]. SteamSpy medians are **not usable** now. HowLongToBeat pages were not pulled.
- **What this means for cost** (my arithmetic, not a source): if the median player plays X hours and the average is 3-4X, then **per-sale AI cost follows the average, not the median**, and the top 1-10% can make up a large share of the bill. That is why Suck Up! capped at 40-50 h, and why AI Dungeon's energy was aimed at the roughly 7% heaviest users.
