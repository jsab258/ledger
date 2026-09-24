# Business plumbing: a relay between the game and the model

Researched 2026-09-24. Nothing signed up for, bought, deployed or downloaded.

Labels on every fact:
- **OPENED** = I fetched and read the page itself. **SNIPPET** = search-result summary or a third-party write-up only; check it before relying on it.
- **VENDOR** = the seller's own claim or price list. **MEASURED** = somebody timed or counted it. **DERIVED** = my arithmetic, with the assumptions stated.
- Dates: the page's "last updated" date where it shows one, otherwise the date I read it (2026-09-24).

---

## 1. Why the key cannot ship, and what the standard setup looks like

### Anthropic's own position
- Anthropic's API-key help article (last updated 2026-03-16): "don't share your API key", and "if someone needs access to the Claude API, they should obtain their own key." GitHub scans public repositories for Claude keys and tells Anthropic, and Anthropic "automatically deactivates the exposed API key." It advises usage and spend limits "as a safeguard against unexpected usage due to leaked keys." The article does not mention client-side code specifically. OPENED, VENDOR. https://support.claude.com/en/articles/9767949-api-key-best-practices-keeping-your-keys-safe-and-secure
- Anthropic's TypeScript SDK refuses to run in a browser unless the developer sets `dangerouslyAllowBrowser`, because that "exposes your secret API credentials in the client-side code". SNIPPET (SDK README / issue #248), VENDOR. https://github.com/anthropics/anthropic-sdk-typescript
- **Commercial Terms: a game calling the API for its players is allowed.** "Anthropic gives Customer permission to use the Services, including to power products and services Customer makes available to its own customers and end users." The customer "is responsible for all activity under its account", must make sure its users follow the Usage Policy, and may not "resell the Services except as expressly approved." OPENED, VENDOR (read 2026-09-24). https://www.anthropic.com/legal/commercial-terms
- **A trap to avoid:** third-party articles (SitePoint and others) say Anthropic now says customers "may not pay for, resell, or intermediate Claude usage on their end users' behalf." I opened the source. That sentence sits under "Can customers offer Claude Code in their products?" and covers embedding the **Claude Code binary**. It also bars routing Free, Pro or Max consumer-plan logins through someone else's product. The same page says the rule "does not restrict how customers provision and manage their own API keys". **It does not cover a game that calls the Messages API with the studio's own paid key.** OPENED, VENDOR. https://code.claude.com/docs/en/legal-and-compliance . A game rated for children would also bring in Anthropic's guidelines for organisations serving minors (SNIPPET): https://support.claude.com/en/articles/9307344

### Keys taken out of shipped apps (evidence that this really happens)
- "Mind your key" (arXiv 2606.12212; covered by The Hacker News on 2026-06-30): the authors tested 444 iOS AI chatbot apps. **282 leaked access**: 54 sent keys in plain text, **92 ran their own backend "that answers anyone, with no check on who is asking"**, and 136 leaked replayable tokens. Three months after being told, only 28% had fixed it. OpenAI keys were the most common; the article names no Anthropic keys. OPENED (news write-up), MEASURED (academic study). https://thehackernews.com/2026/06/282-ios-apps-found-leaking-llm-api-keys.html ; https://arxiv.org/html/2606.12212v1
- **Lesson for us:** a relay with no player check is only a key leak moved one step along. The 92 "open proxy" apps did exactly that.
- Sysdig named "LLMjacking": attackers use stolen cloud credentials to run Claude at the victim's expense. Its estimate was up to about $46,000 a day on one account for Claude 2.x, and later cases went above $100,000 a day. SNIPPET, a vendor estimate rather than a measured bill. https://www.sysdig.com/blog/llmjacking-stolen-cloud-credentials-used-in-new-ai-attack
- The PAREA study (arXiv 2306.05499) found attackers using an LLM-backed app as a free LLM ("prompt abuse"), with an estimated loss of $259.2 a day. It found 30 other apps open to the same abuse. SNIPPET, MEASURED (academic). https://arxiv.org/pdf/2306.05499

### The standard setup
game client -> **our relay** (holds the Anthropic key, checks who the player is, counts their use, holds the system prompt) -> Anthropic API. The client never sees the key or the full prompt. It sends game state and gets text back.

### Identifying a player without a login screen
- **Steam** (the obvious choice for a PC game). The client calls `ISteamUser::GetAuthTicketForWebApi(identity)` and waits for `GetTicketForWebApiResponse_t`. The relay then calls `ISteamUserAuth/AuthenticateUserTicket` over HTTPS, and a valid ticket returns the player's 64-bit SteamID. The relay can then call `ISteamUser/CheckAppOwnership` to confirm the player owns the game. This needs a **Web API Publisher Key**, which stays on the relay and never goes in the client. The page lists no rate limit for this call. The practical approach is to check once per session and give the player a short-lived token of our own. OPENED, VENDOR. https://partner.steamgames.com/doc/features/auth ; https://partner.steamgames.com/doc/webapi/isteamuserauth
- **Epic Online Services (EOS):** free. The Connect interface logs in with outside credentials, Steam included, and gives a Product User ID. The client gets an ID token (a JWT) with `EOS_Connect_CopyIdToken`. The backend checks it against Epic's public keys (JWKS), or calls `EOS_Connect_VerifyIdToken` on a trusted server. SNIPPET, VENDOR. https://dev.epicgames.com/docs/api-ref/interfaces/connect ; https://dev.epicgames.com/docs/epic-online-services/accounts-and-social/eos-epic-account-services/auth-interface/retrieve-and-validate-id-tokens . "EOS are free" per https://dev.epicgames.com/en-US/services (SNIPPET, VENDOR).
- **Device ID / anonymous install ID:** no login is needed, but anyone can make up new IDs. It only holds if we also limit by IP address and require a proof-of-work or attestation step. It is fine for a demo and weak against scripted abuse. (My assessment; not sourced.)
- **Consoles, at a high level:** they all follow the same pattern. The platform gives the client a signed token, and our backend checks it.
  - Xbox/GDK: an XSTS token for a "relying party" set up in Partner Center. It is an encrypted JWT, valid for 4 hours by default. SNIPPET, VENDOR. https://learn.microsoft.com/en-us/gaming/gdk/docs/services/fundamentals/s2s-auth-calls/service-authentication/live-title-service-authentication
  - PlayStation: the client gets a PSN auth code, and the server exchanges it. SNIPPET (PlayFab LoginWithPSN docs). https://learn.microsoft.com/en-us/rest/api/playfab/server/authentication/login-with-psn
  - Switch: an NSA ID token (JWT) checked against Nintendo's public keys. SNIPPET (mod.io docs). https://docs.mod.io/restapi/docs/authenticate-via-switch
  - All of these details sit behind platform NDAs. Public pages only show the outline.

---

## 2. Limits per player, spend caps, abuse, and what happens when the budget runs out

### Anthropic's own limits (Console) — OPENED, VENDOR, https://platform.claude.com/docs/en/api/rate-limits (read 2026-09-24)
- **Monthly spend cap by tier: Start $500, Build $1,000, Scale $200,000.** The Custom tier has no cap and is arranged with sales. At the cap, every request returns HTTP 429 `enforced_spend_limit_reached` **until 00:00 UTC on the 1st of the next month**, with no retry-after. *That is a whole-game outage for every player, so our relay must stop well before the cap.*
- A lower organisation spend limit can be set on the Billing page. Hitting it returns HTTP 400 `invalid_request_error`.
- **Each workspace can have its own spend and rate limits**, but not the default workspace. Use one workspace for the shipped game, separate from development. Organisation limits always apply as well.
- Rate limits on the Start tier for Haiku 4.5 and Sonnet 5: 1,000 requests a minute, 2M input tokens a minute, 400k output tokens a minute. Build: 5,000 / 5M / 1M. Scale: 10,000 / 10M / 2M. **For most models, only uncached input counts toward the input-token limit**, so prompt caching also raises the effective ceiling. New organisations may start in an "Evaluation" tier below Start.
- Response headers (`anthropic-ratelimit-*`) let the relay see how much headroom is left.

### Model prices, for scale (OPENED, VENDOR, https://platform.claude.com/docs/en/about-claude/pricing, read 2026-09-24)
- Haiku 4.5: $1 input and $5 output per million tokens (MTok); cache read $0.10.
- Sonnet 5: $2 / $10; cache read $0.20. $2/$10 is now the standard price, and the planned rise to $3/$15 was cancelled.
- The 5-minute cache write costs 1.25× the input price. The newer tokenizer (models 4.7 and later) makes about 30% more tokens for the same text.
- Asking for US-only processing (`inference_geo: "us"`) costs 1.1× on Claude 4.6 and later.

### What the relay itself must enforce (standard practice; my synthesis)
1. **Token budget per player**, counted in tokens or dollars rather than calls. Keep a daily limit and a monthly one, e.g. 1.5× the expected 200 calls a month, with a daily ceiling so one binge cannot use it all. Count real `usage` from each response after it completes. Also reserve an estimate before the call, so running calls in parallel cannot overshoot.
2. **Rate limit per player** (e.g. no more than 1 call every 2–3 s, and 1 call in flight at a time) plus a **rate limit per IP address**. Cloudflare's rate-limit binding counts per key and per location. It is approximate, "built for cheap, fast abuse protection, not globally consistent quotas." It suits the per-minute limit. The budget itself needs a consistent store (a Durable Object or a database). SNIPPET, VENDOR. https://developers.cloudflare.com/workers/runtime-apis/bindings/rate-limit/
3. **Global circuit breaker:** a spend counter for the whole game that stops or degrades service at e.g. 80% of our own monthly budget, well before Anthropic's hard cap. Also trip it when the error rate or latency from Anthropic spikes.
4. **Fixed prompt on the server:** the client sends structured game state (which NPC, what happened, the player's short line with a length cap), and the relay builds the prompt. Never pass on a raw `messages` array from the client, and set `max_tokens` on the relay. This stops anyone using the relay as a general chatbot, which is what happened to the 92 "open proxy" iOS apps.
5. **Checks on replies:** cap output length, and check that replies stay in character, e.g. that they fit the game's shape. Prompt injection is #1 on OWASP's LLM Top 10 for 2025 (SNIPPET, https://genai.owasp.org/llmrisk/llm01-prompt-injection/). It cannot be fully prevented. The defence is that a successful injection gets only a short in-character reply inside a small per-player budget, so it is worth little.
6. **Against scripted abuse:** proof of ownership (Steam `CheckAppOwnership`) makes every abusive account cost the price of a game copy. Add bans per SteamID and anomaly flags, such as calls outside the game's normal pace or 24-hour play.
7. **When the budget runs out, the game still works:** authored fallback lines (written barks and templates driven by the simulation), a smaller cheaper model, or a local model on the player's PC. The game must be fully playable with the relay unreachable, because offline play, outages and the spend cap all cause the same failure.

---

## 3. Ready-made options and prices

### Managed LLM gateways (a proxy in front of the model; most still need our own code for Steam login)
| Option | Price | Notes | Label |
|---|---|---|---|
| **Cloudflare AI Gateway** | Core features free: analytics, caching, rate limiting. Provider prices passed through "with no markup". Unified Billing charges a 5% fee on credits. Log storage: accounts created on or after 24 Sep 2026 follow Workers Logs pricing; older accounts have the legacy caps (100k logs on Free, 10M per gateway on Paid). Logpush costs $0.05/M above 10M. | Page last updated 2026-09-24 (today). | OPENED, VENDOR https://developers.cloudflare.com/ai-gateway/reference/pricing/ |
| **Portkey** | Developer plan free with 10k logged requests a month. Production $49/month for 100k logs, then $9 per extra 100k. Enterprise on request. | Third-party summaries | SNIPPET https://www.truefoundry.com/blog/portkey-pricing-guide |
| **Helicone** | Hobby plan free, 10k requests; Pro $79/month; Team $799/month. **Bought by Mintlify in Mar 2026 and reportedly in "maintenance mode".** | Third-party | SNIPPET https://www.truefoundry.com/blog/helicone-pricing |
| **LiteLLM proxy** (self-hosted, open source) | Free software; we pay for the server. Has virtual keys with **budgets and rate limits per key or user**. Its own benchmark: 2–8 ms median overhead (P95 8 ms, P99 13 ms), 4 CPUs and 8 GB per instance, against a *fake provider*. | Vendor-run benchmark | OPENED, MEASURED by the vendor https://docs.litellm.ai/docs/benchmarks ; https://docs.litellm.ai/docs/proxy/users |
| **OpenRouter** | Model prices passed through, plus **a 5.5% fee on credit purchases** ($0.80 minimum). Bring-your-own-key is free up to $25k a month of list-price use, then 5%. Runs on Cloudflare Workers. | Third-party summaries | SNIPPET https://www.truefoundry.com/blog/openrouter-pricing |
| **Kong Konnect** | About $34.25 per million requests plus about $105 a month per "gateway service" (one analysis); Plus plan lists $200 per extra million. | Enterprise-shaped; too dear for us | SNIPPET https://zuplo.com/learning-center/api-gateway-pricing-comparison-2026 |
| **Apigee** | $20 per million standard proxy calls ($100 per million with scripting), plus $365–$3,431 a month per region. | Enterprise-shaped; too dear for us | SNIPPET https://docs.cloud.google.com/apigee/docs/api-platform/reference/pay-as-you-go-updated-overview |

### Serverless and small-server hosting
| Option | Price | Label |
|---|---|---|
| **Cloudflare Workers Paid** | $5/month includes 10M requests and 30M CPU-ms. Then $0.30 per million requests and $0.02 per million CPU-ms. **Wall-clock and I/O wait are not billed. Calls out to Anthropic are not billed. No egress fees.** No wall-clock limit on HTTP requests while the client stays connected; CPU limit 30 s by default, up to 5 min. KV: reads $0.50/M, writes $5/M. **Durable Objects:** 1M requests included then $0.15/M; 400k GB-s duration included then $12.50 per million GB-s; SQLite 50M rows written included then $1/M. D1 is the same for rows. Workers Logs: 20M events included then $0.60/M. Page updated 2026-08-28. | OPENED, VENDOR https://developers.cloudflare.com/workers/platform/pricing/ ; https://developers.cloudflare.com/workers/platform/limits/ |
| Cloudflare R2 (to archive logs) | $0.015 per GB-month; Class A $4.50/M, Class B $0.36/M; no egress fees; 10 GB free. | SNIPPET https://developers.cloudflare.com/r2/pricing |
| **AWS Lambda** (us-east-1) | $0.20 per million requests. $0.0000166667 per GB-s on x86, $0.0000133334 on Arm. Free every month: 1M requests and 400k GB-s. Streaming costs $0.008 per GB after 6 MB per request and 100 GB a month. **Lambda bills duration while the handler runs, including time waiting on Anthropic**, which matters for 1–2 s calls. | OPENED, VENDOR https://aws.amazon.com/lambda/pricing/ |
| AWS API Gateway | HTTP API $1.00 per million (first 300M), billed in 512 KB steps. REST API $3.50/M. Data out $0.09/GB. REST APIs gained response streaming in Nov 2025. | OPENED, VENDOR https://aws.amazon.com/api-gateway/pricing/ ; SNIPPET https://aws.amazon.com/about-aws/whats-new/2025/11/api-gateway-response-streaming-rest-apis |
| AWS DynamoDB on-demand (counters) | $0.625 per million writes, $0.125 per million reads (us-east-1). Sources disagree; one says $1.25/$0.25. | SNIPPET https://aws.amazon.com/dynamodb/pricing/on-demand |
| **Fly.io** (from 2026-10-01) | shared-cpu-1x with 256 MB: $2.19/month; 512 MB (2x): $4.39. RAM $6 per GB-month. Egress $0.02/GB in North America and Europe, $0.04 in Asia-Pacific, Oceania and South America, $0.12 in Africa and India. | OPENED, VENDOR https://fly.io/pricing-update/ |
| **Hetzner Cloud** (after 2026-06-15) | CX23 €5.49/month, CAX11 €5.99, CX33 €8.49 (Germany/Finland, not counting IPv4). About 20 TB of traffic included (SNIPPET). Two price rises in 2026: April and June. | OPENED, VENDOR https://docs.hetzner.com/general/infrastructure-and-availability/price-adjustment/ |

### Game-backend services (they give login and a place to run our code, and the relay code still has to be written)
| Option | Price | Label |
|---|---|---|
| **Epic Online Services** | Free; the Connect login accepts Steam and other outside credentials. | SNIPPET, VENDOR https://dev.epicgames.com/en-US/services |
| **PlayFab** | Development Mode free up to 1,000 lifetime players. Live games: pay-as-you-go, Standard $99/month, Premium $1,999/month. CloudScript executions are metered. Azure Functions CloudScript bills to *our own* Azure subscription. | SNIPPET https://playfab.com/pricing/ ; https://learn.microsoft.com/en-us/gaming/playfab/pricing/meters/meters |
| **Nakama / Heroic Cloud** | Nakama itself is open source and free to host ourselves. Heroic Cloud is priced by CPU and database size; the page shows no smallest price, and summaries say about $600/month and up. Support plans $2,000 and $6,000 a month. | OPENED https://heroiclabs.com/pricing/ ; SNIPPET for the $600 figure |
| **Unity Gaming Services, Cloud Code** | 1M invocations a month free, then $1.50 per million (SNIPPET). Also billed for compute seconds and egress. **15-second timeout per script**, which is too short for a long streamed reply and doesn't suit streaming. | OPENED (cost page) https://docs.unity.com/en-us/cloud-code/scripts/reference/cost ; SNIPPET for the rate |
| **AccelByte** | Free on shared cloud up to 30 peak concurrent users a day, then priced per peak user per day. Private cloud from $2,500/month. | SNIPPET https://accelbyte.io/pricing |

### AI-NPC middleware (runs the relay for us; we accept their stack and prices)
| Vendor | Published pricing | Label |
|---|---|---|
| **Inworld** | Pay-as-you-go plus credit plans: Creator $25, Builder $100, Developer $300, Growth $1,500 a month (the fee comes back as credits). **LLM Router "at cost"** with no markup. TTS-2 $25 → $5 per million characters; STT $0.15 an hour. No per-character or per-NPC runtime fee is published. | OPENED, VENDOR https://inworld.ai/pricing |
| **Convai** | An "interaction" is one player input plus one character reply. Free: 100 a month. Indie Dev about $22–29 for 3,000 (1,500 on flagship models). Professional about $69–99 for 10,000. Scale about $499; Business about $1,199. The FAQ says the Scale plan caps at **200 monthly active end users**, and larger audiences go to sales. For our 1k MAU (200k interactions a month) that means an enterprise deal. | OPENED (FAQ) https://convai.com/faqs ; SNIPPET for prices https://www.saasworthy.com/product/convai/pricing |
| **NVIDIA ACE / NIM** | No public ACE-for-games price found. NIM production needs NVIDIA AI Enterprise at **$4,500 per GPU per year, or $1 per GPU per hour** in the cloud. Development is free on up to 16 GPUs. ACE's on-device models are aimed at running on the player's RTX card rather than a cloud relay. | SNIPPET https://docs.api.nvidia.com/nim/docs/faq |

---

## 4. DERIVED: monthly cost of the relay at three sizes

### Assumptions (all mine unless marked)
- Each player: 10 hours a month × 20 calls an hour = **200 calls per player-month**.
- Calls a month: 1k MAU → **200k**; 20k MAU → **4M**; 200k MAU → **40M**.
- Each call: 8 KB request and 1 KB response, streamed, taking 1–2 s. I use **2 s** where time is billed.
- Relay requests = calls × 1.05 (+5% for login and token refresh). The Steam check runs once per session and is free.
- Relay CPU time: **5 ms per call** (check our token, look up the budget, build the prompt, pass the stream through). This is an assumption; it could be 2–10 ms.
- Per-player counter: **2 counter operations per call** (reserve before the call, settle actual tokens after), plus 1 row written.
- Durable Object billed time: **1 s of 128 MB active time per call** (conservative; 0.1 s would cut that line by 10×).
- Logging: **1 metadata event per call.** Full prompt and reply text is *not* stored by default. If it were, that is ~9 KB per call: 1.8 GB, 36 GB or 360 GB a month. At R2's $0.015 per GB-month that is pennies, then ~$5 a month as it builds up at the largest size.
- Busy-time traffic: average calls per second × 3. Monthly seconds: 2.592M.

### Option A: Cloudflare Workers + Durable Objects (the cheapest; bills only CPU, not waiting time)
| Line | 1k MAU | 20k MAU | 200k MAU |
|---|---|---|---|
| Base plan | $5 | $5 | $5 |
| Requests (10M included, then $0.30/M) | 0.21M → $0 | 4.2M → $0 | 42M → **$9.60** |
| CPU (30M ms included, then $0.02/M ms) | 1.05M ms → $0 | 21M → $0 | 210M → **$3.60** |
| Durable Object requests (1M included, then $0.15/M) | 0.4M → $0 | 8M → $1.05 | 80M → **$11.85** |
| Durable Object time (400k GB-s included, then $12.50/M) | 25k → $0 | 500k → $1.25 | 5M → **$57.50** |
| Durable Object rows written (50M included) | $0 | $0 | $0 |
| Workers Logs (20M included, then $0.60/M) | $0 | $0 | 40M → **$12** |
| Bandwidth | $0 (no egress fees) | $0 | $0 |
| **Total relay** | **≈ $5** | **≈ $7** | **≈ $100** (≈ $45 if Durable Object active time is 0.1 s) |
| Per player-month | $0.005 | $0.0004 | $0.0005 |

### Option B: AWS API Gateway (HTTP) + Lambda (256 MB, x86) + DynamoDB
Lambda duration per call = 2 s × 0.25 GB = 0.5 GB-s.
| Line | 1k MAU | 20k MAU | 200k MAU |
|---|---|---|---|
| API Gateway $1/M | $0.21 | $4.20 | $42 |
| Lambda requests $0.20/M (1M free) | $0 | $0.64 | $8.20 |
| Lambda time (400k GB-s free) | 105k → $0 | 2.1M → **$28** | 21M → **$343** |
| DynamoDB, 2 writes per call at $0.625/M | $0.25 | $5 | $50 |
| Data out (1–1.5 KB per reply; 100 GB free, not verified) | ~$0 | ~$0 | ~$5 |
| CloudWatch logs (not priced; assume) | ~$1 | ~$5 | ~$30 |
| **Total relay** | **≈ $2** | **≈ $45** | **≈ $480** |
Lambda's billing for waiting time is the main cost. Arm would take ~20% off.

### Option C: small servers (Hetzner) running our own relay, or LiteLLM with Redis or Postgres
Concurrency (DERIVED): 200k MAU × 10 h = 2M player-hours a month ≈ 2,740 players online on average, ~8k at the busiest. Calls: 15.4/s on average, **~46/s at the busiest**, so ~90 streams open at once at 2 s each. One small server can hold that. The reasons for a second machine are redundancy and deploying without downtime, not load.
| | 1k MAU | 20k MAU | 200k MAU |
|---|---|---|---|
| Machines | 1 × CX23 | 2 × CX23 | 2 × CX33 + a small database or Redis machine |
| Cost | ≈ €5.50 | ≈ €11 + load balancer (price not verified, assume ~€6) | ≈ €17 + €5.50 + load balancer ≈ **€30** |
| Traffic | under 2 GB | ~40 GB | ~400 GB, well inside ~20 TB |
- Cheapest at the largest size, but **one region** (Germany/Finland), so extra round-trip for American and Asian players. We run it, patch it and watch it ourselves.

### The model bill, for comparison: it is far bigger than the relay
Tokens per call: 8 KB ≈ 2,000 input tokens and 1 KB ≈ 250 output tokens (about 4 characters per token; the newer tokenizer adds about 30%).
| | per call | per player-month | 1k MAU | 20k MAU | 200k MAU |
|---|---|---|---|---|---|
| Haiku 4.5, no cache | $0.00325 | $0.65 | $650 | $13,000 | $130,000 |
| Haiku 4.5, 75% of input cached | ~$0.0019 | ~$0.38 | ~$380 | ~$7,600 | ~$76,000 |
| Sonnet 5, no cache | $0.0065 | $1.30 | $1,300 | $26,000 | $260,000 |
**The relay is under 1% of the model bill at every size.** Picking a relay host is about ease, latency and safety, not cost.

### Consequences of the tier caps (DERIVED from the OPENED rate-limits page)
- **1k MAU on uncached Haiku ($650 a month) is already over the Start-tier cap of $500**, and uncached Sonnet 5 ($1,300) is over the Build cap of $1,000. Moving up needs spending history, or asking.
- **20k MAU needs the Scale tier** (cap $200k).
- **200k MAU on uncached Sonnet 5 ($260k) is over the Scale cap**, so it needs the Custom tier through sales.
- Rate limits: 200k MAU at the busiest is about 2,800 requests a minute and 5.6M uncached input tokens a minute. That is over Build's 5M input tokens a minute, so it needs Scale, *or* caching (75% cached brings uncached input down to about 1.4M). 20k MAU at the busiest is about 280 requests a minute, which fits the Start tier.

---

## 5. Delay added by the relay
- **What adds delay:** one extra network leg (player → relay) plus the relay's own processing. The relay → Anthropic leg replaces the player → Anthropic leg. An edge relay (Cloudflare Workers) sits a few ms from most players, and its connection on to Anthropic comes from a data centre. A one-region relay adds that region's round-trip for far-away players: for example Europe → US and back is typically about 80–150 ms (general knowledge, not sourced here).
- LiteLLM's own measurement: **2–8 ms median overhead, P99 13 ms**, against a fake provider on 4 CPUs. OPENED, MEASURED by the vendor. https://docs.litellm.ai/docs/benchmarks
- LLM Gateway's own benchmark (2026-07-22): time to first token for claude-haiku-4.5 streaming, 75 cold and 75 warm runs from one home connection. **LLM Gateway 906 ms cold / 814 ms warm; OpenRouter 1,392 / 1,232 ms.** There was no direct-to-Anthropic baseline, and the benchmark was run by a competitor. OPENED, MEASURED (competitor-run). https://llmgateway.io/blog/openrouter-vs-vercel-vs-llmgateway-performance
- OpenRouter's own docs give no figure. They say it runs on Cloudflare Workers with caching at the edge, and that delay is higher for the first 1–2 minutes in a new region. Third parties report ~15, ~25 or ~40 ms from various OpenRouter pages. OPENED (docs, no number) https://openrouter.ai/docs/guides/best-practices/latency-and-performance ; SNIPPET for the numbers.
- Helicone claims about 50 ms; "most managed gateways" 3–15 ms. SNIPPET, VENDOR or third-party. https://www.helicone.ai/blog/top-llm-gateways-comparison-2025
- Cloudflare Workers: the start-up delay is effectively 0 ms, because the Worker warms up during the TLS handshake (Cloudflare blog, 2020). Smart Placement can run the Worker near the backend, i.e. near Anthropic, when that is faster overall. SNIPPET, VENDOR. https://blog.cloudflare.com/eliminating-cold-starts-with-cloudflare-workers/ ; https://developers.cloudflare.com/workers/configuration/placement/
- **Bottom line:** a relay adds about 5–50 ms to a first token that already takes about 800–1,400 ms. That is under 5% and not something a player would notice, *as long as* the game streams the reply and keeps a persistent connection (the cold→warm difference in the benchmark was about 90–160 ms).

---

## Open or unverified
- The price for Hetzner's load balancer and Convai's current prices were not opened.
- DynamoDB's current price: sources disagree by 2×.
- Durable Object active-time billing per call was not measured. It is the biggest uncertain line in Option A.
- No independent, measured "direct vs through a relay" test against Anthropic from Europe was found. It can be checked in an afternoon once a test relay exists.
- Steam's rate limit for `AuthenticateUserTicket` is not documented on the page; check it once per session and cache the result.
