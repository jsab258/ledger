# Gemini's terms, free tier and cost for training the fast checker, 26 October 2026

His order of 26 October (item 3): Gemini 3.8 Flash writes LEDGER-style first sentences from the game's own facts and labels each one supported or not. The small checker (TinyLettuce 17M, MIT) learns from those labels and ships inside the sold game, doing only that check. Google's current Gemini API terms are to be read first. The free tier is fine if its limits allow; otherwise he is told the cost first.

**How this was read.** Every page was read on 26 October 2026 through a fetch tool that returns a model-written digest of the page, not its raw text. Wording was asked for word for word, in consecutive pieces. A digest is not the page itself, so the clause should be read on the page once more before the run. Nothing was called on Google's API, nothing was downloaded, nobody signed in, and the key file was not opened. UNVERIFIED means not confirmed on a primary page. "Judgement" means a reading made here. None of this is legal advice.

## Answers in short

1. **Yes.** The current terms (effective 23 March 2026) bar using Gemini only to build models that compete with Gemini's own services, or to copy Gemini itself. A small checker that only judges a game character's sentence does neither. The clause is the same, word for word, as in the November 2025 version. The free and paid tiers are the same on this point.
2. **For him in Switzerland, the free tier is treated like the paid one.** Google's terms say that for anyone in the EEA, Switzerland or the UK, the paid tier's data rules apply to free use too. So Google does not use his prompts or Gemini's answers to improve its products, and they are not read by human reviewers for that purpose. Switzerland is an available region. The game's invented town facts hold no personal data.
3. **About $4 at today's introductory price** for both jobs (writing the 5,000 sentences and labelling them), by his token figures. The Batch API would halve that to about $2. The price doubles from 1 January 2027, to about $8. A cautious case, with longer prompts and some thinking, is about $14. The free tier's limits are not published by Google. The only figure found (20 requests a day, a user's report) would cover the writing in 3 days but the labelling in 250. And his key is probably on a paid project already (section 3). So the cost goes to him first.

## 1. May Gemini's output train a small checker that ships in a sold game?

**The current version.** The Gemini API Additional Terms of Service are effective 23 March 2026, and the page was last updated 28 April 2026 [1]. The archive lists earlier versions, including 20 November 2025 and 18 December 2025 [2].

**The clauses that touch training or reuse:**

- **Competing models** (Use Restrictions). The Services may not be used to "develop models that compete with the Services" [1]. The examples given are the Gemini API and Google AI Studio. The 20 November 2025 version has the same sentence word for word [3], so his memory of it holds and nothing has changed since.
- **Copying Gemini** (the same paragraph). No reverse engineering, extracting or replicating any part of the Services, including the data or models underneath them; parameter weights are the example [1].
- **Search and Maps grounding.** Results grounded with Google Search or Google Maps may not be trained on [1]. This bites only if the run turns grounding on, so the run must leave it off.
- **Nothing else on training.** The fetch was asked to list every sentence about training, machine learning, competing or distilling:
  - The Google APIs Terms of Service (last modified 9 November 2021) have none [4].
  - The Generative AI Prohibited Use Policy (last modified 17 December 2024) has none either [5].
- **Ownership.** Google says it "won't claim ownership" of generated content [1]. The developer is responsible for how it is used.
- **One clause read and set aside.** Section 5(e) of the Google APIs Terms bars copying, adapting or distributing content returned from the APIs, unless its owner or the law permits [4]. Judgement: it does not bar this use.
  - Google disclaims ownership of Gemini's generated text [1].
  - The Additional Terms win wherever the two conflict [4].
  - The clause reads as aimed at other people's content, such as Search or Maps data.
  - In any case, only the checker's weights ship, not the labelled sentences.
- **New since November 2025.**
  - Use must be "for professional or business purposes, not for consumer use" [1]. A game studio's tooling is business use.
  - The developer is responsible for choosing safety settings and factuality tools [1].
  - Users must be 18 or over [1].

**Judgement: yes.** The checker has 17M parameters and decides only whether one game character's sentence is backed by that character's facts. It does not compete with the Gemini API or AI Studio, and it does not copy Gemini's weights or data. No clause read asks for Google's permission. That is the difference from Anthropic's Usage Policy, which asks for prior permission to train any model on its outputs (LOCAL-CHECKERS-2026-10-26.md, section 4).

**Free against paid: no difference here.** The Use Restrictions apply to "the Services", which include AI Studio and both the unpaid and paid API quota [1]. The tiers differ only in data use (section 2) and price (section 3).

## 2. The free tier's data use, and Switzerland

- **The general rule for unpaid use** [1]:
  - Google uses the prompts and Gemini's answers to provide, improve and develop its products and machine-learning technology.
  - Human reviewers may read, annotate and process the input and output. This happens after the data is separated from the account, the key and the project.
  - The terms warn: do not send sensitive, confidential or personal information.
  - The pricing page marks 3.8 Flash's free tier "Used to improve our products: Yes" and its paid tier "No" [6].
- **Paid use** [1]:
  - Google does not use prompts or answers to improve its products.
  - It logs them for a limited period, only to catch breaches of the Prohibited Use Policy and for legal disclosures. They may be stored briefly in any country.
- **Switzerland.** For anyone in the EEA, Switzerland or the UK, the paid tier's data rules apply to every Service, including AI Studio and the unpaid API quota, even though these are free [1]. The November 2025 version says the same [3]. So for him, free use is neither used to improve Google's products nor read by reviewers for quality. Only the limited abuse logging remains.
- **Is the free tier offered in Switzerland?** Yes, by reading.
  - Switzerland is on the list of available regions (page updated 22 October 2026) [7].
  - The Swiss data sentence above speaks of the unpaid quota there [1].
- **The paid-only rule.** The terms also say only paid Services may be used when making apps that use Gemini ("API Clients") available to users in the EEA, Switzerland or the UK [1]. Judgement: this is about apps that put Gemini in users' hands. The labelling script is his own development tool, and the game ships no Gemini client, so the rule does not apply here.
  - The terms do not define "user" outside the Maps section [1].
  - Read strictly, the answer is a paid project, which he probably has already (section 3).
- **The game's invented town facts.**
  - They hold no personal data, so the warning is met.
  - On any tier, section 5(b) of the Google APIs Terms gives Google a lasting, worldwide, royalty-free licence to submitted content. That licence is limited to providing, securing and improving the APIs [4].
  - Under the Swiss data rule above, the content is not used to improve products. What remains is that unreleased story facts sit in Google's abuse logs for a limited time. Low risk (judgement).
- **Safety filters.** Gemini's safety features may block some menace or crime lines, and getting around them is barred [1]. This is a practical matter for the writing step, not a legal one.

## 3. Gemini 3.8 Flash: model, limits, price and the run's cost

**The model.**
- The model id is `gemini-3.8-flash`, a stable model, released 2 September 2026 [8][9][10]. Gemini 3.7 Flash was deprecated on 8 October in its favour [9].
- It reads up to 1,048,576 tokens and writes up to 65,536 [8].
- Its thinking levels are low, medium and high; "minimal" returns an error [8]. Its default is listed as "On (medium)" [11].
- Thinking tokens are billed as output [11]. Google's launch post warns the model may use more tokens at higher effort [10].
- **How 22 October called it** (production/lab/talk-check/gemini_check.py): the v1beta `generateContent` endpoint, one call per detail, `thinkingBudget 0`, JSON output, temperature 0.

**Paid price, Standard tier, per million tokens** [6]; the launch post agrees [10]:

| | Input | Output (thinking included) |
|---|---|---|
| Through 31 December 2026 (introductory) | $0.75 | $3.75 |
| From 1 January 2027 | $1.50 | $7.50 |
| Batch API, through 31 December 2026 | $0.375 | $1.875 |

**Free tier.**
- 3.8 Flash is on the free tier: input and output are "Free of charge" [6].
- **Its limits are not published.** The rate-limits page (updated 15 October 2026) gives no requests-a-minute, tokens-a-minute or requests-a-day figure for any tier. It says each project's limits are shown in AI Studio [12]. Daily quotas reset at midnight Pacific time [12].
- **The only figure found** is a developer's post on Google's forum (3 September 2026). It gives 20 requests a day for 3.8 Flash against 500 for Flash-Lite [13]. No Google staff replied. UNVERIFIED.
- No requests-a-minute or tokens-a-minute figure was found anywhere.

**What 22 October shows (measured from its records).**
- The key made 127 calls to `gemini-3.8-flash` that day, 124 answered, at about 33 a minute. It made 127 to Flash-Lite at about 100 a minute, none lost.
- A free tier of 20 a day could not have allowed that. The likeliest reason is that the key's project already has billing linked. Every call through such a project is a paid Service [1]: charged, with no free tier. UNVERIFIED; he can see it in AI Studio, in the Plan column of the API keys page [14].
- At today's prices, 22 October's counted tokens cost about $0.21 on 3.8 Flash and $0.09 on Flash-Lite. The 22 October note left this unstated because the price page had not been read then.
- Thinking tokens may come on top. The script counted only the answer's tokens (`candidatesTokenCount`), not the thinking tokens (`thoughtsTokenCount`). Google's thinking page does not list a way to switch 3.8 Flash's thinking off [11]. So whether `thinkingBudget 0` really switched it off is UNVERIFIED. The 1.8 s median is slow for about 22 output tokens, which hints that it did not.

**The estimate (calculated, not measured), by his token figures:**

| Job | Calls | Input tokens | Output tokens | Now (to 31 Dec) | From 1 Jan 2027 | Batch, now |
|---|---|---|---|---|---|---|
| Write 5,000 sentences, 100 a call | 50 | 75,000 | 150,000 | $0.62 | $1.24 | $0.31 |
| Label 5,000 sentences, one a call | 5,000 | 3,000,000 | 300,000 | $3.38 | $6.75 | $1.69 |
| **Both** | 5,050 | 3,075,000 | 450,000 | **$3.99** | **$7.99** | **$2.00** |

**What could raise it:**
- **Thinking.** It is on at medium by default and billed as output. Every 100 thinking tokens per labelling call add $1.88 to the labelling. On the writing calls the same costs $0.02. The run should set the thinking level to low and record the thinking tokens.
- **Prompt length.** 22 October's calls carried about 2,190 input tokens each (instructions plus facts: 271,199 over 124 answered calls). If the labelling prompt is that long, labelling input rises from $2.25 to about $8.21.
- **A cautious case** (assumed, not measured):
  - Labelling: 2,190 tokens in, 60 out plus 200 thinking per call, about $13.10.
  - Writing: 1,000 thinking tokens per call, about $0.80.
  - Together: **about $14 now, about $28 from 1 January 2027, about $7 on the Batch API.**

**Billing limits, all far above this job** [12][14]:
- Tier 1 (billing linked) caps spending at $250 a month and $10 per 10 minutes.
- Prepaid credit starts at $5 and expires after 12 months.
- Tier 1 can queue 3,000,000 tokens at once for 3.8 Flash on the Batch API [12], so a batched labelling run goes in two or more parts. Whether that count includes output tokens is not stated.

**Does the free tier cover it?** Only if the 20-a-day figure is right, and even then not usefully:

| Job | Calls | Days at 20 a day |
|---|---|---|
| Writing | 50 | 3 |
| Labelling, one sentence a call | 5,000 | 250 |
| Labelling, 25 sentences of one speaker packed in a call | 200 | 10 (tokens-a-minute limit unknown) |

His key is probably on a paid project already. **So the cost goes to him first, as his order says:** about $4 by his figures, about $14 cautiously, half that on the Batch API, and double from 1 January 2027. Running before 31 December keeps the introductory price.

## Unverified / not reached

- **Free-tier limits for `gemini-3.8-flash`** (requests a minute, tokens a minute, requests a day).
  - Not published; the AI Studio page needs his sign-in.
  - "20 a day" is one user's forum post.
  - A search summary credited freellm.net with 15 a minute and 1,500 a day, but the page itself shows no figure. That is not evidence.
- **Billing on his key's project:** inferred from 22 October's call counts only. Not checked (it needs AI Studio).
- **Free quota on a billing-linked project:** whether any survives. The billing page is silent [14].
- **Thinking on 3.8 Flash:**
  - Whether `thinkingBudget 0` switched it off on 22 October.
  - How many thinking tokens labelling will use.
  - The default ("medium") comes from the thinking page's table only; the model page does not state it [8][11].
- **Batch API:**
  - Whether the free tier can use it (limits are listed for Tiers 1 to 3 only) [12].
  - What the 3,000,000 queued-token limit counts.
- **How long paid abuse logs are kept:** "a limited period", no number [1].
- **"Making API Clients available to users":** whether this covers a developer's own script. No definition outside the Maps section; judgement only.
- **Archived terms read:** only 20 November 2025 and the current version. The 18 December 2025 version and the others were not read.
- **Secondary sources**, seen but not used as evidence: usagebox (10 October 2026), apidog (16 September 2026) and eesel (edited 8 September 2026). None gives free-tier figures.

## Sources (all read 26 October 2026)

1. Gemini API Additional Terms of Service (effective 23 March 2026; page updated 28 April 2026): https://ai.google.dev/gemini-api/terms
2. Archive of earlier versions: https://ai.google.dev/gemini-api/terms-archive
3. The version effective 20 November 2025: https://ai.google.dev/gemini-api/terms-archive/terms_11_20_25
4. Google APIs Terms of Service (last modified 9 November 2021): https://developers.google.com/terms
5. Generative AI Prohibited Use Policy (last modified 17 December 2024): https://policies.google.com/terms/generative-ai/use-policy
6. Gemini API pricing (updated 22 October 2026): https://ai.google.dev/gemini-api/docs/pricing
7. Available regions (updated 22 October 2026): https://ai.google.dev/gemini-api/docs/available-regions
8. Model page (updated 22 October 2026): https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash ; model list: https://ai.google.dev/gemini-api/docs/models
9. Release notes (2 September and 8 October 2026 entries): https://ai.google.dev/gemini-api/docs/changelog
10. Google's launch post, 2 September 2026: https://blog.google/innovation-and-ai/models-and-research/gemini-models/3-8-flash-and-3-8-flash-cyber/
11. Thinking (updated 14 October 2026): https://ai.google.dev/gemini-api/docs/thinking
12. Rate limits (updated 15 October 2026), and its raw text: https://ai.google.dev/gemini-api/docs/rate-limits ; https://ai.google.dev/gemini-api/docs/rate-limits.md.txt
13. Google forum post, 3 September 2026 (one reply, 16 October 2026): https://discuss.ai.google.dev/t/gemini-3-8-flash-free-tier-20-rpd-is-too-limited-for-practical-evaluation/180609
14. Billing (updated 28 September 2026): https://ai.google.dev/gemini-api/docs/billing
15. The project's own 22 October evidence: production/research/voice-latency/GEMINI-CHECK-2026-10-22.md and gemini-2026-10-22/

Secondary, not used as evidence: https://usagebox.com/articles/gemini-3-8-flash-pricing-free-tier-2026 ; https://apidog.com/blog/how-to-use-gemini-3-8-flash-for-free/ ; https://eesel.ai/blog/gemini-3-8-flash-pricing ; https://freellm.net/models/google-gemini/gemini-3-8-flash
