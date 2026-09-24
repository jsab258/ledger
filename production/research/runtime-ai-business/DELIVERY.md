# Runtime AI as a business: cap what one copy can cost, sell the game once, and let design choices set the bill

STATUS: SPEC (research delivery). Branch `research/runtime-ai-business`.
Written 2026-09-24. Audited against `BRIEF.md`, which was written and committed
first.

NOTHING HERE IS AN INSTRUCTION. Nothing was bought, signed up for or deployed.

Labels: CITED (a page opened), CITED-SUMMARY (a search result only), DERIVED
(arithmetic or reasoning from cited things), ASSUMED, HOLE. MEASURED, REPORTED
(by the developer), ESTIMATE (a third party's), VENDOR CLAIM and DOCUMENTATION
say what kind of source a CITED figure is.

## 0. Sourcing

Five helpers each researched one of the brief's five questions, in parallel,
on 2026-09-24. Their full records are in `notes/`: games, models, prices,
stores and plumbing. There, every fact carries its link, its date, whether the
page was opened or only seen in a search result, and what kind of source it is.
This document cites the facts the recommendation rests on. For every other
figure, `notes/` is the source list. All pages were read through a fetch tool
that returns a model-written summary with quotes pulled out, so a figure that
will decide something should be checked against the live page once.

The spreadsheet is `runtime-ai-business-model.xlsx` in this folder. Every
result in it is a formula, and all 355 cells were evaluated with the
Python `formulas` library with zero errors. LibreOffice is not on this PC, so
the skill's own recalculation check could not run. The workbook is set to
recalculate when it is opened.

## 1. The answer, first

1. **No shipped game publishes what it pays per player-hour.** The few real
   figures are totals and anecdotes (section 2). Our own measured cost per
   hour will be better evidence than anything in the literature.
2. **Every game that paid for unlimited AI talk either had a rich backer or
   moved to cheaper or local models.** Adding metered charges on top of a
   one-time price did not survive anywhere it was tried. Subscriptions work
   only for open-ended AI products, and Steam supports them badly.
3. **The price of our model is not falling.** A fixed capability gets 5 to 13
   times cheaper a year, but only by moving to whichever model is cheapest.
   Anthropic's small model has held or raised its price for three years. The
   safe assumption is today's price. A fall only counts if the dialogue can
   change models.
4. **The store rules shape the model more than they forbid anything.**
   - Steam requires disclosure, a description of the guardrails, and an
     in-game way to report illegal content.
   - Purchases inside the game must go through Steam's payment system.
   - Subscriptions are "not a fully supported feature", and ads are banned.
   - Microsoft adds disclosure and reporting, and treats API keys as
     financial information.
   - The EU AI Act has required telling players they are talking to an AI
     since 2 August 2026.
5. **The relay is cheap and necessary.** It costs $5 to $100 a month even at
   200,000 players, under 1% of the model bill. The real risk is Anthropic's
   monthly spend caps: at the cap, the whole game goes quiet.
6. **Recommendation (section 8): one price, a generous cap on live talk per
   copy, and written lines after it.** The cap has to hold on our servers, not
   in the game. Offer the player's own key as an optional unlimited mode and a
   local model later as an upgrade. Let two design choices set the bill: how
   much of the talk is written ahead, and whether line-writing can run
   locally.

## 2. Games that shipped with live AI (question 1)

Full record: `notes/games.md`. The facts that bear on the decision:

| game | how it priced | what it paid | how it held costs | what went wrong | reviews |
|---|---|---|---|---|---|
| **AI Dungeon** (Latitude) | freemium, then subscriptions $15 to $100 a month; a $30 one-off Steam tier was scrapped, and it left Steam in 2024 | about US$200,000 a month at its 2021 peak, "about the same as payroll"; under $100,000 a month after moving to AI21's 17B and open models (CEO to CNBC, March 2023; CITED-SUMMARY) | smaller and open models; rationing the heaviest 7% through "energy"; ads briefly (2022) | 2021: OpenAI caught users generating sexual content involving minors; a rushed filter over-flagged, and humans read private stories | player revolt over the filter |
| **Suck Up!** (Proxima) | $15.99 including a hard cap of 10,000 AI turns, about 40 to 50 hours; top-ups promised | not published. DERIVED: the price allows at most about $0.0016 a turn, or $0.32 to $0.40 an hour | the cap | the cap was removed at 1.0 (October 2025); players say the AI got "MASSIVELY" worse; the supplier connection broke in March 2026 | Mixed, 62% of 208 |
| **Vaudeville** (detective) | one price | "a substantial bill" in the first month; the service went down when a big streamer played it | moved to a local, offline model as the default on 28 November 2025, citing "high service costs", outages and lack of control | 5 s to start speaking, 10 to 15 s to finish | 48% positive |
| **Retail Mage** (Jam & Tea) | one price | the prototype cost "the cost of a ticket to Disneyland" per 4-player session; a year later "dimes" (GDC write-up, April 2025, CITED) | open models on their own rented machines, and forced structured output | - | - |
| **Death by AI** (Discord) | free, Discord-hosted | 1.2 billion tokens a day at peak | became profitable only after leaving GPT-4 and ElevenLabs for cheaper models, volume deals and a different model per game mode (vendor case study) | - | - |
| **AI2U** | players' own OpenAI key, then paid turns, then one price with unlimited chat; refunded people who had bought turns | not published | - | - | 88% of 1,037 |
| **Whispers from the Star** | $9.99, no cap | not published; backed by miHoYo's co-founder | - | privacy is the top complaint | 80% of 1,661 |
| **Uncover the Smoking Gun** | $19.99, GPT-4 | not published | short and bounded | - | 96% of 414 |
| **inZOI, PUBG Ally** (Nvidia ACE, on-device) | part of the game | zero per hour | 0.5B and 2B models on the player's RTX card | needs 8 GB and costs frame rate; features thin enough that players switch them off | - |

Measured player attitudes, from `notes/models.md`:
- A survey of 1,799 players (late 2025): 83% negative on AI-generated dialogue
  specifically.
- A study of 508,192 Steam reviews: 17.9 points lower recommendation for games
  that disclose AI, except where the AI is the game's premise
  (ethics-and-reception, topic 24).
- Recurring complaints: delay, repetition, loops, always-online, extra
  accounts, and "abandoned".

DERIVED, the pattern:
- **The well-reviewed one-price games are short and bounded.**
- **The open-ended ones sell subscriptions**, at $10 to $50 a month, metered by
  memory length or model quality.
- **The ones that stayed alive moved to cheaper or local models.** Nobody
  sustained unlimited frontier-model talk on a one-time price without a
  patron.

## 3. The business models (question 2)

Full record: `notes/models.md`.

| model | seen in | suits | risks |
|---|---|---|---|
| **One price, cost absorbed, no cap** | Whispers from the Star (patron-backed), Uncover the Smoking Gun | short, bounded games; well-funded studios | heavy players cost more than they paid; the bill never stops while anyone plays; one streamer can swamp the service (Vaudeville) |
| **One price with included hours, then written lines** | Suck Up! at launch (10,000 turns) | a game whose world still works without live talk, which ours does (the brush-off is already ruled) | players resent visible rationing; Suck Up! dropped its cap, though no reason was published |
| **Included hours, then credits** | AI Dungeon credits (about $9.99 per 1,200), Master of Dungeon, Tabled | enthusiasts | on Steam, purchases must use the Steam Wallet, so Steam takes its cut; the ESRB "In-Game Purchases" label; per-use charges on top of a price did not survive anywhere |
| **Subscription** | AI Dungeon, NovelAI, Friends & Fables, Character.AI | open-ended AI products where the AI is the whole product | Valve: "not a fully supported feature", "customer appetite… is limited", prices can never be raised; players dislike recurring fees on single-player games (no direct survey found; HOLE) |
| **Player's own key** | 1001 Nights (required), AI Roguelite (optional), AIvy (a CHF 4.75 add-on on Steam), Skyrim and RimWorld mods | power users, and as an optional unlimited mode | no published take-up figure (HOLE); friction loses sales; a key is "financial information" on Microsoft's store; consoles unknown |
| **Local model** | inZOI, PUBG Ally, Vaudeville since November 2025 | players with capable cards; offline play | about 49% of Steam users have 12 GB or more of card memory and about 20% have under 8 GB (Steam survey, August 2026); quality lower; card memory shared with the game |
| **Hybrid** | Nvidia's toolkit is built for it; AI Roguelite (free cloud default, own key, local, optional subscription) | our case | two paths to build and test |
| **Others** | Player2 (a platform that gives AI to games, funded by player subscriptions and ads; says it is paying $2M to about 1,000 developers); middleware such as Inworld, which passes model costs through and cut prices by more than half in June 2026 | small studios | dependence on a third party's survival; Steam bans ad-funded games |

Heavy players drive the bill in any model where we pay. GameDiscoverCo's Steam
data puts average playtime at 3 to 4 times the median (for example, JRPGs 7.5
hours median against 21.4 average). About 36% of owners finish a typical
single-player game. Disco Elysium's most common achievement is held by 32.5% of
owners.

## 4. Prices, past and next two years (question 3)

Full record: `notes/prices.md`.

- CITED, the analyses: a16z (November 2024) found about 10x cheaper a year at
  equal capability. Epoch AI found 9x to 900x a year by task (March 2025), and
  about 47% a quarter, roughly 13x a year (22 September 2026). That fall is
  fastest when a capability first appears (66% a quarter) and slows to 32% a
  quarter after two years. MIT FutureTech (March 2026): the cost of running
  the newest, most capable models rose 3 to 18x a year.
- CITED, what those rates measure: the cheapest model anywhere that clears a
  bar, usually another vendor or an open model. Not the price of the model
  already in use.
- CITED, Anthropic's small model:
  - Claude Instant 1.2: $1.63 / $5.51 per million tokens in and out (2023).
  - Haiku 3: $0.25 / $1.25 (March 2024).
  - Haiku 3.5: $1 / $5, later $0.80 / $4.
  - Haiku 4.5: $1 / $5.
  - Google's Flash line also rose with each release, and Gemini 3.5 Flash costs
    3x Gemini 3 Flash.
  - In the other direction, OpenAI's GPT-6 Luna launched on 22 September 2026 at
    $0.10 / $0.50.
- CITED, what is coming:
  - Anthropic announced Haiku 5.5 on 22 September 2026, with no price or date
    yet.
  - Claude 4.7 and later count the same text as about 30% more tokens. At an
    unchanged price per token, that is 30% more per line.
- DERIVED, projection for Haiku 4.5's level of capability:

| | low (stay on Anthropic's Haiku) | central (move models, about 4x then 3x a year) | high (Epoch's 13x a year holds) |
|---|---|---|---|
| Sep 2027 | $1 / $5 | $0.25 / $1.25 | $0.08 / $0.40 |
| Sep 2028 | $1 / $5 or more | $0.08 / $0.40 | $0.01-0.02 / $0.05-0.10 |

DERIVED: **budget at today's price, and treat any fall as the reward for being
able to switch models.** That makes model portability a business requirement,
not an engineering nicety. The central case also needs our dialogue to pass
its quality tests on a cheaper model, which nobody has checked (HOLE).

## 5. What the stores permit and require (question 4)

Full record: `notes/stores.md`.

- **Steam, CITED (Content Survey; updated 16 January 2026):**
  - Live-generated content is "any kind of content created with the help of AI
    tools while the game is running".
  - It must be disclosed, and the developer must describe the guardrails that
    stop it producing illegal content.
  - Live-generated adult sexual content is banned outright.
  - Since the January 2024 rules, players have an overlay button to report
    illegal content.
  - Store pages carry "Connects to 3rd-Party Service for AI Content
    Generation" and "Requires 3rd-Party Account" notices.
- **Steam pricing, CITED (Steamworks documentation):**
  - Purchases inside the game must use the Steam Wallet.
  - Subscriptions are "not a fully supported feature" and developers are urged
    to reconsider them.
  - Ad-funded games are banned.
  - Since October 2024, checkout says a purchase is a licence.
  - A player's own key exists in practice (AIvy's add-on), and no Valve rule
    was found for or against it.
- **Microsoft Store Policies v7.20 (14 September 2026), CITED:**
  - Rule 11.16 requires disclosing live generative AI in the listing and the
    submission, keeping its output within policy, and an in-game way to report
    bad output that is acted on.
  - Rule 10.8.1: in-game purchases must use Microsoft's system.
  - Rule 10.8.3 treats "API secret keys" as financial information.
- **Sony and Nintendo:** nothing public; their requirements are under
  non-disclosure agreements (HOLE until we sign up).
- **Ratings:**
  - Paid credits trigger ESRB's "In-Game Purchases" label.
  - Under PEGI's March 2026 rules, open communication with no blocking or
    reporting makes a game PEGI 18.
- **Law, CITED:**
  - EU AI Act Article 50 has applied since 2 August 2026: players must be told
    they are talking to an AI, at their first conversation at the latest.
    Machine-readable marking of AI text is required where feasible, with a
    deadline of 2 December 2026 for systems already on sale.
  - The EU Digital Services Act most likely does not apply to a single-player
    game.
  - UK: Ofcom puts one-to-one chatbots out of scope. The Crime and Policing Act
    2026 s.248 lets the government bring AI services under the illegal-content
    rules by regulation (none confirmed).
  - The EU declined, in June 2026, to legislate against games being shut down,
    and promised an industry code by the end of 2026 instead.
  - Switzerland was not researched (HOLE).

DERIVED, for us:
- The content rule already has to be enforced on the live path: the
  ethics-and-reception topic found nothing checks what a character says live.
- Now Steam, Microsoft and PEGI all require a way for players to report output.
  That is floor, whatever the business model.

## 6. The plumbing (question 5)

Full record: `notes/plumbing.md`.

- **The key must not ship.** A June 2026 study found 282 of 444 iOS AI apps
  leaking access, and 92 of them through their own server that answered
  anyone. A relay that does not check who is calling is still a leak.
- **Identity without a login:** the game gets a Steam session ticket, and the
  relay checks it with Steam (ISteamUserAuth). That returns the Steam ID and
  can confirm ownership, so each abusive account costs a copy of the game.
  Epic Online Services is free and accepts Steam logins.
- **Limits:**
  - a budget per player per day and per month;
  - a rate limit per player and per address;
  - the prompt built on the server with a fixed reply length, so the relay
    cannot be used as a free chatbot;
  - its own stop at about 80% of the monthly budget.
- **Anthropic's monthly spend caps:** Start $500, Build $1,000, Scale $200,000,
  and beyond that a sales deal. At the cap every call fails until the 1st of
  the month. DERIVED: 1,000 players on uncached Haiku at 10 hours a month is
  already over the Start cap.
- **Cost, DERIVED at 10 hours and 200 calls per player-month:** Cloudflare
  Workers about $5 / $7 / $45-100 a month at 1k / 20k / 200k players. AWS about
  $2 / $45 / $480, because Lambda bills the wait on Anthropic. Hetzner about
  €5.50 / €17 / €30. **The model bill is 100 times the relay bill or more.**
- **Delay:** a relay adds about 5 to 50 ms to a first word that takes 0.8 to 1.4
  s, provided the reply is streamed and the connection kept open.
- **Ready-made:** LiteLLM is free and self-hosted with per-user budgets built
  in. Cloudflare's AI Gateway core is free. Middleware (Inworld, Convai) adds a
  dependency; Convai's Scale plan stops at 200 monthly players.

## 7. The model (the spreadsheet)

`runtime-ai-business-model.xlsx`: Read me, Inputs, Models, Grid, Prices. Blue
cells are inputs and yellow cells are key assumptions. **The cost per hour is a
placeholder**, $0.14: topic 19's estimate with prompt caching, until the slice
measures ours.

The design choices are inputs too, so their effect on the bill shows directly:
the share of talk written ahead, and whether action-picking or line-writing
runs locally. Line-writing is about 70% of the cost per hour (DERIVED from the
prompt sizes).

What it shows at the default inputs (DERIVED; $24.99, 30% store share, typical
15 h, heavy 120 h, 20% heavy):

| cost per hour at launch | hours one sale pays for | average cost per copy (36 h) | heavy player (120 h), absorbed |
|---|---|---|---|
| $0.14 (cached, placeholder) | 125 | $5.04 of $17.49 | +$0.69 |
| $0.36 (uncached, topic 19) | 49 | $12.96 | -$25.71 |

With a 40-hour cap on live talk, one copy can cost at most $5.60 at $0.14 an
hour, or $14.40 at $0.36. **The cap turns an open-ended liability into a
known cost per copy**, which is the whole point.

## 8. Recommendation, and the design choices it depends on

**Sell the game once. Include a generous amount of live talk per copy,
enforced on our relay, not in the game. Past it, the street carries on with
written lines and the brush-off already ruled for a dropped connection. Offer
an optional own-key mode for the few who want unlimited talk, and a local
model as a later upgrade for capable cards.**

Why:
- It is the only shape that caps what a copy can cost us.
- It works within Steam's rules without subscriptions or wallet credits.
- It matches the only precedent that held its price for a while (Suck Up!'s
  40 to 50 hours).
- It degrades into a game that still works.
- Credits and subscriptions have the worst record, and Steam supports them
  poorly.
- A required own key loses sales.

Which design choices money should drive, most leverage first:

1. **How much of the talk is written ahead.** Every point of talk moved to
   written barks, remarks and stock replies cuts the bill by the same share.
   It is also what makes the capped model graceful, because the world keeps
   talking after the cap.
2. **Whether line-writing can run locally.** It is about 70% of the cost per
   hour. If it can, the bill for a capable card falls to the action-picking
   alone. This is the queued blind test, L01.
3. **The cost per call itself:** prompt size, prompt caching (topic 19: about
   60% off), and how many calls an hour. The slice's measurement settles this,
   and it is what the spreadsheet waits for.
4. **Model portability.** Future price falls only arrive if the dialogue can
   move to a cheaper model. Keep the paid model behind the one-method
   interface it already has, and keep the quality tests that would show a
   cheaper model is good enough.
5. **The cap.** Set it from the measured cost and the price, so the worst copy
   costs a known share of what it earned.

Floor, whatever the business model:
- the in-game way to report output;
- the AI disclosure at the first conversation;
- the Steam guardrail description;
- the content rule enforced on the live path;
- the relay's own budget stop below Anthropic's cap.

## 9. What could not be established

1. **What any shipped game pays per player-hour.** None publishes it.
2. **How many players set up their own key.** No figure anywhere.
3. **Why Suck Up! dropped its cap.** Only players' accounts.
4. **Player attitudes to a monthly fee on a single-player game.** No direct
   survey.
5. **Whether a cheaper model passes our dialogue's quality bar.** Untested.
6. **Sony's and Nintendo's rules.** Under non-disclosure agreements.
7. **Swiss law.** Not researched.
8. **Our own cost per hour.** Waiting on the slice, as the brief says.

Denominator: five questions and five research passes. Nine shipped games with
facts, three with any cost figure, and none with a figure per player-hour.
