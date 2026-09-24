# Stores and live AI: what Steam, the consoles, Epic and GOG allow and require

Research date: 2026-09-24. Nothing was downloaded. Labels used below:
- **OPENED**: I fetched the page and the quote comes from its text. The fetch tool summarises pages, so short quotes are reliable but long passages may be trimmed.
- **SNIPPET**: the wording comes from a search result or from a secondary article, and the primary page was not read.
- **UNVERIFIED**: taken from general or industry knowledge and not confirmed in this pass.

This is not legal advice. Anything that affects money or a launch platform should be checked with Valve through Steamworks support, or with a lawyer, before it is relied on.

---

## 1. Steam: AI content disclosure

### 1a. Content Survey, the current wording (the live policy)
- URL: https://partner.steamgames.com/doc/gettingstarted/contentsurvey (OPENED 2026-09-24; the page shows no "last updated" date)
- Scope sentence, which is the January 2026 clarification: "We are aware that many modern game development environments have AI powered tools built into them. Efficiency gains through the use of these tools is not the focus of this section." The survey covers AI-made content delivered to players, "artwork, sound, narrative, localization, etc."
- Pre-Generated: "Any kind of content that ships with your game and is consumed by players that is created with the help of AI tools during development."
- Live-Generated: "Any kind of content created with the help of AI tools while the game is running." It follows the same rules as pre-generated content, plus developers must disclose the guardrails that stop illegal content from being generated.
- Adult: "we don't want to ship Live-Generated AI Adult Only Sexual Content at this time."
- **What this means for us:** a live LLM conversation counts as Live-Generated. The survey must describe our guardrails, meaning the moderation or filter layer, prompt constraints, refusal handling and logging. Sexual content from the live model must be blocked outright.

### 1b. The original announcement, 10 January 2024
- URL: https://steamcommunity.com/groups/steamworks/announcements/detail/3862463747997849619 (the page renders with JavaScript and the fetch returned no text, so this is SNIPPET). The same text appears on store.steampowered.com/news/group/4145017/view/3862463747997849618, which also returned no body.
- Valve's quotes as carried by GamingOnLinux, https://www.gamingonlinux.com/2024/01/valve-announces-new-rules-for-games-with-ai-content-on-steam/ (OPENED; article dated 2024-01-10, updated 2025-02-20):
  - Live-Generated: "...in the Content Survey, you'll need to tell us what kind of guardrails you're putting on your AI to ensure it's not generating illegal content."
  - Store page: Valve will "include much of your disclosure on the Steam store page for your game, so customers can also understand how the game uses AI".
  - Reporting: a new system lets players "report illegal content inside games that contain Live-Generated AI content", accessed through the Steam Overlay.
  - "Adult Only Sexual Content created with Live-Generated AI is not currently allowed on Steam."
- Consequence (SNIPPET from PCGamesN and legalmoveslawfirm): the overlay report button is live. If a game's guardrails fail, Valve can remove the game.

### 1c. Change on 16 January 2026
- SNIPPET, from multiple outlets: biggo.com 2026-01-17, PC Gamer, Notebookcheck, and respawn.outlookindia.com. Valve narrowed disclosure to content "consumed by players", which includes store and marketing assets. Internal efficiency tools such as code assistants are exempt. The live-generated guardrail requirement did not change. The Content Survey wording in 1a matches this.
- The Conversation, 2026-02-11 (OPENED): https://theconversation.com/are-video-game-developers-using-ai-players-want-to-know-but-the-rules-are-patchy-274850. It says the disclosure is a free-text field with no searchable tag.

### 1d. How live-LLM games actually disclose on Steam today (store pages OPENED 2026-09-24)
- **Suck Up!** (app 2726370, released 2025-10-01, CHF 13.55)
  - Store notice: "Connects to 3rd-Party Service for AI Content Generation: ChatGPT from OpenAI".
  - Broadband internet is required.
  - The page lists no in-game purchases.
  - Earlier, outside Steam, it sold AI tokens (SNIPPET: store.playsuckup.com).
- **Whispers from the Star** (app 3730100, Anuttacon, released 2025-08-14, CHF 10.99)
  - "Requires 3rd-Party Account: Anuttacon Account (Supports Linking to Steam Account)".
  - Broadband internet is required.
  - Its guardrail text is a good model for ours. In paraphrase: safety filters and moderation block explicit sexual content, self-harm promotion and hate speech, and it warns that open interaction may still produce responses "not appropriate for all audiences".
  - Players report caps of about 40 to 60 minutes of play per day, which the developer uses to control API cost (SNIPPET: Steam discussions).
- **AIvy Cloud LLM unlock** (app 4805570, a DLC released 2026-06-19, CHF 4.75). **This is BYOK on Steam, in practice.**
  - "You need an account with one of the supported providers (OpenAI / Anthropic / Google) and the ability to generate an API key".
  - The key is stored locally with Windows DPAPI and requests go directly from the PC to the provider.
  - Store notice: "Connects to 3rd-Party Service for AI Content Generation".
  - The base game runs a local LLM, and the BYOK unlock is sold as paid DLC.
- **Translate Lens: BYOK & Local LLM Unlock** (app 4454390) is a second BYOK DLC (SNIPPET).
- Conclusion: Steam has a store-page field for "Connects to 3rd-Party Service for AI Content Generation" and a separate "Requires 3rd-Party Account" notice. BYOK is accepted in practice. I found no Valve rule that forbids it, and I found no Valve rule that explicitly allows it either.

## 2. Steam: pricing models and consumer rules

### 2a. In-game purchases must go through Steam
- URL: https://partner.steamgames.com/doc/features/microtransactions (OPENED)
- "For any in-game purchases, you'll need to use the microtransaction API so Steam customers can only make purchases from the Steam Wallet."
- On what can be sold: "Whether that is items, in-game currency, or anything else that you can think up..."
- Implementation page (OPENED): its purpose is to let users "easily spend their Steam wallet value on your products."
- **What this means for us:** AI credits or consumables sold inside the Steam build must go through the Steam Microtransaction API, which takes Valve's cut. We should not sell credits through our own web shop to Steam players. Pointing players to an external shop from the Steam build is not explicitly quoted as forbidden in what I read, but the sentence above is plain. It would need confirming with Valve (UNVERIFIED).

### 2b. Subscriptions
- URL: https://partner.steamgames.com/doc/store/pricing/subscriptions (OPENED)
- "Recurring Subscriptions is not a fully supported feature."
- "In many cases, we urge you to consider whether recurring subscription is really the right path for your product."
- Subscriptions are "configured and managed entirely by the game".
- Recurring In-Game Billing page, https://partner.steamgames.com/doc/features/microtransactions/recurring_billing (OPENED):
  - "A user may only have one active billing agreement per game."
  - "Users can elect to cancel an agreement at any time from within their Steam account."
  - The feature needs a backend that calls ISteamMicroTxn/ProcessAgreement.
  - Search snippet: a subscription "cannot charge more than the agreed amount in the period".
- Conclusion: a subscription is technically possible through Steam billing and our own server, but Valve discourages it and treats it as not fully supported.

### 2c. Onboarding: what Steam forbids outright
- URL: https://partner.steamgames.com/doc/gettingstarted/onboarding (OPENED)
- Forbidden: "Applications built on blockchain technology that issue or allow exchange of cryptocurrencies or NFTs", "Applications with advertising-based business models", "Adult content that isn't appropriately labeled and age-gated", and "Nude or sexually explicit images of real people".
- An advertising-funded model is out.
- July 2025, SNIPPET (automaton-media): Steam added a rule against content that breaks the rules of payment processors and card networks.

### 2d. Third-party accounts and online-only
- Steam store pages show "Requires 3rd-Party Account: X" and "Connects to 3rd-Party Service" notices. I saw both on the pages in 1d.
- I found **no public Steamworks page** in this pass with the exact disclosure rule for third-party accounts. The Store Page Written Description page (OPENED) does not cover it. The requirement is enforced through the store admin fields and review, and it was widely discussed after the Helldivers 2 / PSN episode of May 2024 (SNIPPET). For us: a BYOK key or an account with our backend must be declared in those fields.
- September 2024 (SNIPPET: Shacknews, Game World Observer): links are banned in store page descriptions.

### 2e. Digital purchases are licences
- California AB 2426 (in force 2025). Steam now shows at checkout: "A purchase of a digital product grants a license for the product on Steam." (SNIPPET: howtogeek, fkks/Lexology, October 2024.) Valve shows this to all customers, not only Californians. Steam handles this at checkout. We should still state clearly on the page that the game needs an online AI service.
- EU, "Stop Destroying Videogames" citizens' initiative (SNIPPET: Lewis Silkin 2026-06-24 and others). On 2026-06-16 the Commission declined to legislate. It will start a code-of-conduct process with the industry by the end of 2026 and raise awareness of rights under the existing Digital Content Directive. Campaigners are pushing for rules through the coming Digital Fairness Act, whose draft has no end-of-life provision yet.
- Practical point: our game depends on a paid online model. If the service is ever shut down, the game dies, and that risk falls on us. A BYOK or local-model fallback reduces both the consumer-law risk and the "killed game" reputational risk.

## 3. Consoles: Sony, Microsoft, Nintendo

- **None of the three has a public AI-disclosure rule for its storefront comparable to Steam's.** The Conversation, 2026-02-11 (OPENED): "There's currently no clear AI disclosure on mobile app stores or console storefronts." tech-insider.org 2026 (SNIPPET) says the same.
- **Sony and Nintendo TRC / lotcheck are under NDA.** I found no public text on live-generated AI.
- Sony, May 2026 (SNIPPET: Push Square, Variety): Sony is pro-AI in development. "Human creativity must remain at the centre."
- Nintendo, Furukawa, July 2026 shareholder Q&A (SNIPPET: Nintendo Life): "Regardless of whether generative AI is used, if Nintendo determines that something infringes on Nintendo IP, our policy is to respond appropriately." Nintendo does not use generative AI in its own development.
- **Microsoft Store Policies v7.20, ms.date 2026-09-14** (OPENED: https://learn.microsoft.com/en-us/windows/apps/publish/store-policies). This is the only public platform-holder rule on live AI:
  - 11.16 Live Generative AI Content. "Products that contain dynamic content created by generative AI models in response to user inputs must: Disclose the use of live generative AI in the metadata. Note the use of live generative AI in Partner Center during the submission process. Ensure that dynamic content created by generative AI models complies with all applicable Store Policies. Provide a means for users to report inappropriate content to the developer. You must take appropriate actions based on those reported concerns."
  - 10.8.1: "Games (excluding games made available through a subscription in PC gaming subscription products...)" and "Products offered on XBOX consoles" must use the Microsoft Store in-product purchase API for digital goods, and "must not direct users to a purchase mechanism other than the Microsoft Store in-product purchase API".
  - **10.8.3, which matters for BYOK:** "Financial information includes, but is not limited to, ... API secret keys, private keys, or recovery phrases." A product that requires financial information "must" be submitted from a company account, and "Products from individual accounts cannot require financial information for primary functionality." So on the Microsoft Store and Xbox, BYOK is treated as financial information, and the game must be published by a company.
  - Note: the Xbox console certification requirements (XRs) are covered by the ID@Xbox NDA. Whether a console build may ask for an API key or link to an external subscription is not public. UNVERIFIED: consoles generally require first-party commerce for digital goods, and typing an API key on a pad would be poor UX in any case.
- **Consoles and BYOK / external subscriptions:** no public policy found. Industry practice (UNVERIFIED) is that all digital goods on console go through first-party commerce, and external accounts are allowed only with linking. Treat BYOK on console as unlikely to pass without platform approval. Ask at the platform onboarding stage.

### Ratings (IARC, ESRB, PEGI)
- **ESRB Interactive Elements** (OPENED: https://www.esrb.org/ratings-guide/):
  - "Users Interact: Indicates possible exposure to unfiltered/uncensored user-generated content, including user-to-user communications..." Single-player AI chat is not user-to-user. Whether IARC or ESRB would apply it to live AI text is unclear. I found no ESRB statement on AI-generated content; the only item on ESRB's AI tag is a 2023 privacy post (OPENED).
  - "In-Game Purchases: ... including ... virtual coins and other forms of in-game currency, subscriptions..." AI credits would trigger this.
- **PEGI "interactive risk categories"** (OPENED: https://pegi.info/news/pegi-expands-age-rating-criteria-interactive-risk-categories), announced 2026-03-12, applying to titles newly submitted from June 2026:
  - "games with time-limited or quantity-limited offers will be classified with a PEGI 12".
  - "if games contain entirely unrestricted communication features (e.g. no blocking or reporting), they will be PEGI 18".
  - There is nothing on AI. Unlimited, non-random credit purchases appear to add only the descriptor. Do not use time-limited offers.
- IARC questionnaire and AI: SNIPPET (promise.legal blog). It claims the IARC questionnaire "includes questions about AI-generated content". This is unconfirmed; check it when we submit. The same blog's "July 15, 2026" labelling rule is **Google Play**, not a console rule.

### Epic and GOG
- Epic: no AI disclosure rule. Tim Sweeney has mocked the idea (The Conversation, OPENED). Since June 2025, Epic takes 0% of the first US$1M of revenue per app per year, then 12% (SNIPPET: GamingOnLinux 2025-05). Epic has long allowed developers to use their own in-game payment processing (UNVERIFIED in this pass; check the Epic distribution agreement). Epic is the friendliest store for selling our own credits.
- GOG: no AI rule. February 2026 AMA: "We're not planning on making absolute statements in either direction" (SNIPPET: PC Gamer / GamingOnLinux). It is loosening curation. GOG's DRM-free identity and a game that is always online through a paid API fit together poorly, and GOG may decline it (UNVERIFIED).

## 4. Legal content-screening obligations

- **Steam** (binding by contract): guardrails against illegal content must be described in the Content Survey, players can report through the overlay, and live-generated adult sexual content is banned. See 1a and 1b.
- **Microsoft Store**: 11.16 above requires an in-game way to report and action on those reports.
- **EU AI Act, Article 50** (OPENED text: https://artificialintelligenceact.eu/article/50/)
  - 50(1), providers: AI systems "intended to interact directly with natural persons" must be designed so that people "are informed that they are interacting with an AI system", unless that is obvious from the context.
  - 50(2), providers: synthetic audio, image, video and text must be "marked in a machine-readable format and detectable as artificially generated or manipulated", as far as is technically feasible.
  - 50(4), deployers: deep fakes, and text published to inform the public on matters of public interest. For evidently artistic, creative or fictional works, disclosure is limited so it does not hamper the enjoyment of the work.
  - 50(5): the information must be given "at the latest at the time of the first interaction or exposure".
  - **Dates:** applicable from **2 August 2026**. The AI Omnibus (entered into force 2026-07-27) did not amend Article 50. Systems already on the market before 2026-08-02 have until **2 December 2026** to meet the 50(2) marking duty. The Commission adopted Article 50 guidelines on 2026-07-20. (SNIPPET: Goodwin 2026-08-03 OPENED as a secondary source; also Plesner, Gibson Dunn, usercentrics.)
  - Who is who: we would most likely be the *deployer*, or the provider of the "AI system" if we build the system around a third-party model. The model vendor is the GPAI provider. Minimum steps: a clear in-game notice that the characters talk through an AI, shown before the first conversation. Also ask the vendor about machine-readable marking of text, or add our own metadata or logging. The "obvious from context" and fiction carve-outs help but do not remove the notice. This needs a lawyer's view (UNVERIFIED for games specifically).
- **EU Digital Services Act:** a standalone generative service does not fit the three intermediary categories (conduit, caching, hosting) (SNIPPET: LSE blog 2024, Verfassungsblog). A single-player game in which AI text is shown only to the player who asked for it, with no sharing, is very probably **outside the DSA**. Steam as a platform is inside it. If we added sharing of transcripts or screenshots to other users, that would change.
- **UK Online Safety Act:**
  - Ofcom open letter, 2024-11-08 (SNIPPET: https://www.ofcom.org.uk/online-safety/illegal-and-harmful-content/open-letter-to-uk-online-service-providers-regarding-generative-ai-and-chatbots; the Ofcom explainer page returned 403). Chatbots that "only allow people to interact with the chatbot itself and no other users", do not search multiple websites or databases, and "cannot generate pornographic content" are **not in scope**.
  - **Change coming:** the Crime and Policing Act 2026, s.248 (OPENED: https://www.legislation.gov.uk/ukpga/2026/20/part/17/crossheading/power-to-amend-online-safety-act-2023). The Secretary of State may amend the OSA by regulations to reduce harms from illegal AI-generated content. "AI service" means an internet service capable of generating AI-generated content. The power is in force from Royal Assent, which was around late April 2026 (SNIPPET).
  - The Prime Minister announced this on 2026-02-16 (SNIPPET: Lewis Silkin, TechPolicy.Press). No regulations had been made as of this search, and I did not confirm that either way.
  - A single-player game that calls an online LLM could later fall under illegal-content duties in the UK. Watch for this.
- **Switzerland (our seat):** not researched in this pass. There is no AI Act equivalent in force. The Federal Council's approach, announced in February 2025, is to ratify the Council of Europe AI Convention and make sector-specific amendments (UNVERIFIED here).

## Open questions for Valve and the platforms
1. Valve: may a Steam build sell AI credits only through the Steam Microtransaction API, and never link to an external shop? Is BYOK acceptable as a *main* mode, or only as optional DLC as in AIvy's model?
2. Valve: is there a recommended text for the guardrail disclosure? Whispers from the Star's wording is a reasonable template.
3. Microsoft, Sony, Nintendo: ask about live-LLM and BYOK policy at onboarding, under NDA. On the Microsoft Store, BYOK requires a company account (10.8.3).
