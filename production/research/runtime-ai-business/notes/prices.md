# LLM API prices: how fast they fall, and what to assume for Haiku-class dialogue

Research date 2026-09-24. Prices are USD per million tokens, input / output, standard (non-batch) tier unless marked.
"OPENED" = page fetched and read. "SNIPPET" = search-result text only, not opened. "DERIVED" = my arithmetic or judgement.
Some 2026 facts come from trade press and aggregators; where two sources disagree it is noted.

## 1. Our workload today (DERIVED from Anthropic's pricing page, OPENED)

Haiku 4.5: $1 / $5; batch 50% off; 5-minute cache write 1.25x input; cache read 0.1x input ($0.10).
Per dialogue line, assuming ~1,950 input (of which ~1,700 is a cacheable character card + rules and ~250 is fresh) and ~60 output:
- no caching: 1,950 x $1 + 60 x $5 = **$0.00225 per line**
- with cache hits: 1,700 x $0.10 + 250 x $1 + 60 x $5 = **~$0.00072 per line** (cache writes ignored; they amortise over reads)
- with cache hits and batch: ~$0.00036 (only if lines can wait; batch is not interactive)
With caching, output and the fresh part of the prompt are ~80% of the cost, so the OUTPUT price matters more than the headline input price.

## 2. Dated price points

### Anthropic
| Model | Effective | In / Out | Source | How |
|---|---|---|---|---|
| Claude Instant 1.2 | Aug 2023 release; on Nov 2023 price sheet | $1.63 / $5.51 | https://www-cdn.anthropic.com/1b1ea2c43d8dd058f6a331a8097e05ea40d626c6/model_pricing_nov2023.pdf | OPENED (PDF) |
| Claude 2.0 / 2.1 | 2023 | $8 / $24 | same PDF | OPENED |
| Claude Instant (cut) | Dec 2023 (HN thread) | $0.80 / $2.40 | https://news.ycombinator.com/item?id=38623199 | SNIPPET |
| Claude 3 Haiku | 2024-03-13 | $0.25 / $1.25 | https://openrouter.ai/anthropic/claude-3-haiku ; AWS model card | SNIPPET (price confirmed OPENED in caching post) |
| Prompt caching (beta) | Aug 2024 (the fetched page shows "August 14, 2025", which is very likely a re-dated repost; the feature launched Aug 2024) | Haiku 3: write $0.30, read $0.03 (read = 10% of input) | https://claude.com/blog/prompt-caching | OPENED |
| Claude 3.5 Haiku | 2024-11-04 | $1 / $5 (4x Haiku 3) — "to reflect its increase in intelligence" | https://simonwillison.net/2024/Nov/4/haiku/ | OPENED |
| Claude 3.5 Haiku (cut) | 2024-12-05 | $0.80 / $4 | same | OPENED |
| Claude Haiku 4.5 | 2025-10-15 | $1 / $5 | https://www.anthropic.com/news/claude-haiku-4-5 | SNIPPET; price OPENED on pricing page |
| Sonnet 3.x–4.6 | 2024–2026 | $3 / $15 throughout | https://platform.claude.com/docs/en/about-claude/pricing | OPENED |
| Sonnet 5 | 2026 (intro price through 2026-08-31, now made permanent) | $2 / $10 | same | OPENED |
| Opus 4/4.1 → Opus 4.5–5 → Opus 5.5 | → late 2025 → 2026-09-22 | $15/$75 → $5/$25 → $4/$20 (cache read $0.20, 60% cut) | pricing page; https://www.anthropic.com/claude-opus-5-5 | OPENED |
| **Haiku 5.5** | announced 2026-09-22, "in the coming weeks"; NO price, NO date | — | https://www.anthropic.com/claude-opus-5-5 ; https://www.orcarouter.ai/blog/claude-haiku-5-5-leak (2026-09-22) | OPENED |

Current pricing page note (OPENED): Claude 4.7 and later use a new tokenizer producing "approximately 30% more tokens for the same text". Haiku 4.5 uses the old one. **If Haiku 5.5 uses the new tokenizer at the same per-token price, the same prompt costs ~30% more.** Also: US-only inference is 1.1x for 4.6+ models.

### OpenAI
| Model | Effective | In / Out (cached in) | Source | How |
|---|---|---|---|---|
| GPT-4 | 2023-03 | $30 / $60 | https://developers.openai.com/api/docs/pricing (legacy row gpt-4-0613) | OPENED |
| GPT-3.5-turbo | 2023-06-13 | $1.50 / $2.00 | https://techcrunch.com/2023/06/13/openai-intros-new-generative-text-features-while-reducing-pricing/ | SNIPPET |
| GPT-3.5-turbo-1106 | 2023-11-06 | $1 / $2 | pricing page legacy row | OPENED |
| GPT-3.5-turbo-0125 | 2024-01-25 | $0.50 / $1.50 | pricing page; tech.co | OPENED / SNIPPET |
| GPT-4 Turbo | 2023-11 / 2024-04 | $10 / $30 | pricing page | OPENED |
| GPT-4o | 2024-05-13 → 2024-08-06 | $5 / $15 → $2.50 / $10 | pricing page | OPENED |
| GPT-4o mini | 2024-07-18 | $0.15 / $0.60 ($0.075) | pricing page; OpenRouter | OPENED / SNIPPET date |
| Prompt caching | 2024-10-01 | 50% off cached input, automatic >1,024 tokens | https://openai.com/index/api-prompt-caching/ | SNIPPET |
| GPT-4.1 / mini / nano | 2025-04-14 | $2/$8; $0.40/$1.60 ($0.10); $0.10/$0.40 ($0.025) — cache now 75% off | pricing page; Wikipedia GPT-4.1 | OPENED / SNIPPET date |
| GPT-5 / mini / nano | 2025-08-07 | $1.25/$10; $0.25/$2 ($0.025); $0.05/$0.40 ($0.005) — cache 90% off | https://simonwillison.net/2025/Aug/7/gpt-5/ | OPENED |
| GPT-5.4 mini / nano | 2026-03-17 | $0.75/$4.50; $0.20/$1.25 — **3x and 4x the GPT-5 mini/nano price** | pricing page; apiyi/buildfastwithai | OPENED / SNIPPET date |
| GPT-5.6 Luna | launched 2026-07-09 at $1/$6; cut 2026-07-30 | $0.20 / $1.20 | https://www.axios.com/2026/07/30/openai-cuts-prices-gpt-terra-luna5 ; CNBC; pricing page | SNIPPET; price OPENED |
| GPT-6 Luna / Sol / Astra | Luna+Sol 2026-09-22; Astra 2026-09-03 | Luna $0.10/$0.50 ($0.01); Sol $2/$10; Astra $10/$50. "permanent prices, not promotional" | https://venturebeat.com/technology/openai-releases-gpt-6-sol-and-luna-models-slashing-api-costs-50-or-more ; pricing page | OPENED |

HN, ~June 2026 (OPENED https://news.ycombinator.com/item?id=48689193): "GPT-5 mini costs $0.25/$2 and will be discontinued in December. GPT-5.4 mini costs $0.75/$4.5 and is supposed to be the replacement." Replies: GPT-5.4 nano ~30% worse than GPT-5 mini on one user's workload; one user left OpenAI after GPT-4.1 mini's retirement. **Cheap SKUs get retired and replaced at higher prices.**

### Google Gemini
| Model | Effective | In / Out | Source | How |
|---|---|---|---|---|
| Gemini 1.5 Flash | 2024-05 launch ~$0.35/$1.05; cut 2024-08-12 | $0.075 / $0.30 (<128k) | https://simonwillison.net/2024/Aug/8/gemini-15-flash-price-drop/ ; Google dev blog | SNIPPET |
| Gemini 2.0 Flash | 2025-02 | $0.10 / $0.40 | https://tokencost.app/blog/ai-price-index ; HN | SNIPPET |
| Gemini 2.0 Flash-Lite | 2025-02-25 | $0.075 / $0.30 | https://tokencost.app/blog/gemini-3-5-flash-lite-price-increase | OPENED |
| Gemini 2.5 Flash | 2025-06 | $0.30 / $2.50 (**3x/6x 2.0 Flash**) | https://ai.google.dev/gemini-api/docs/pricing ; xda | OPENED |
| Gemini 2.5 Flash-Lite | 2025-07-22 | $0.10 / $0.40 | pricing page; tokencost | OPENED |
| Implicit caching | 2025-05-08 (75% off), later raised to 90% | — | https://developers.googleblog.com/en/gemini-2-5-models-now-support-implicit-caching/ ; Logan Kilpatrick on X | SNIPPET |
| Gemini 3 Flash | 2025-12-17 | $0.50 / $3 | https://simonwillison.net/2025/Dec/17/gemini-3-flash/ ; xda | SNIPPET / OPENED |
| Gemini 3.1 Flash-Lite | 2026-05-07 | $0.25 / $1.50 (2.5x/3.75x 2.5 Flash-Lite) | pricing page; tokencost | OPENED |
| Gemini 3.5 Flash | 2026-05-19 | $1.50 / $9 (**3x Gemini 3 Flash**) | https://www.xda-developers.com/google-gemini-3-5-flash-costs-3x-model-replaced-cheap-ai-ending/ (2026-05-31) | OPENED |
| Gemini 3.5 Flash-Lite | 2026-07-21 | $0.30 / $2.50 | tokencost (2026-07-26); pricing page | OPENED |
| Gemini 3.6 / 3.7 / 3.8 Flash | 3.6 launched 2026-07-21 at $1.50/$7.50 | $0.75 / $3.75 **introductory through 2026-12-31, then $1.50 / $7.50** | pricing page; VentureBeat 3.7 Flash | OPENED / SNIPPET |

One aggregator (wavect.io, SNIPPET) claims "Gemini 3.1 Flash $0.10/$0.40 in April 2026"; Google's own page shows 3.1 Flash-Lite at $0.25/$1.50. Treat the wavect figure as wrong.

### Open-weight hosting (current pages OPENED 2026-09-24)
- DeepInfra (https://deepinfra.com/pricing): Llama 3.1 8B $0.02/$0.04; Llama 3.3 70B $0.10/$0.32; Mistral Small 24B $0.05/$0.08; Mistral Nemo $0.019/$0.03; Qwen3.5-9B $0.10/$0.15; DeepSeek-V4-Flash $0.06/$0.18 (cached $0.015); DeepSeek V3 $0.32/$0.89.
- Together (https://www.together.ai/pricing): Llama 3 8B Lite $0.14; Llama 3.3 70B $1.04; Qwen3.8 Flash $0.09/$0.28; DeepSeek V4.1 Flash $0.30/$1.20; gpt-oss-120B $0.15/$0.60.
- Groq pricing page carried no prices when fetched.
- History: a16z (Nov 2024) cheapest MMLU-42 model = Llama 3.2 3B on Together, $0.06; Epoch cites GPT-3-level MMLU at $0.07 (Oct 2024).
The same open model costs 2-10x more on one host than another; host choice is itself a lever.

## 3. Independent analyses of the decline rate

| Analysis | Date | Rate | Measured at | How |
|---|---|---|---|---|
| a16z "LLMflation", Guido Appenzeller — https://a16z.com/llmflation-llm-inference-cost/ | 2024-11-12 | **~10x/year** at equal MMLU; MMLU-42: $60 (Nov 2021) → $0.06 (1,000x in 3y); MMLU-83 (GPT-4 level): ~62x since Mar 2023. "its rate may slow down" | cheapest model at a fixed MMLU, blended in/out | OPENED |
| Epoch AI "LLM inference prices have fallen rapidly but unequally across tasks" — https://epoch.ai/data-insights/llm-inference-price-trends | 2025-03-12 | **9x to 900x/year** depending on threshold; GPT-4-level GPQA: 40x/year ($37.50 Mar 2023 → $0.12 Dec 2024); median ~50x/yr, ~200x/yr since Jan 2024 (SNIPPET). Caveat: fastest drops were in the latest year, "less clear that those will persist" | cheapest model above a benchmark threshold | OPENED |
| Epoch AI "The plunging price of thought", Emberson & Roodman — https://epoch.ai/publications/the-plunging-price-of-thought | 2026-09-22 | **~47%/quarter ≈ 13x/year** since 2023. Key for us: decline is fastest right after a capability first appears (**66%/quarter at SOTA debut, slowing to 32%/quarter two years later**, i.e. ~80x/yr → ~4.6x/yr). Caveats: benchmaxxing, users don't switch models, only 3 years of data | cost to reach fixed scores on math, GPQA, game puzzles | OPENED |
| Epoch "How persistent is the inference cost burden?", Denain — https://epoch.ai/gradient-updates/how-persistent-is-the-inference-cost-burden | 2026-02-16 | "roughly a 5–10x cost reduction per year" at fixed capability; distilled models "more brittle" | fixed capability | OPENED |
| MIT FutureTech "The Price of Progress", Gundlach et al. — https://arxiv.org/html/2511.23455v2 | v2 2026-03-23 | **5–10x/year** at fixed performance; ~3x/yr from algorithms alone; frontier cost-to-run rose 3–18x/yr | fixed benchmark performance | OPENED |
| TokenCost AI Price Index — https://tokencost.app/blog/ai-price-index | 2026-03-20 | cheapest-capable input $30 (Mar 2023) → ~$0.07-0.10 (2025); budget tier 200-300x, frontier ~12x in 3 years. "The floor drops faster than the ceiling." | cheapest capable model, input only | OPENED |
| Artificial Analysis — https://artificialanalysis.ai/trends ; X post Sep 2025 | 2025-09 | tracks cheapest price per intelligence band (7:2:1 cache:input:output blend); Sept 2025: Grok 4 Fast brought the >60 band to $0.20/$0.50 | per-band floor | trends page OPENED but numbers not in text; X post SNIPPET |
| xda-developers — see Gemini table | 2026-05-31 | counter-view: compute cost per capability still falls 5-10x/yr but labs "have stopped sharing these efficiency gains"; "The cheap prices were never the real prices" | list prices of Flash tier | OPENED |

What the rates mean: all fixed-capability rates (10x, 13x, 40x, 5-10x) are the price of the CHEAPEST model anywhere that clears a bar, usually a different vendor or an open model, not the price of the SKU you are on. Rates are fastest for newly-reached capability and slow as that capability ages. Frontier/flagship prices fell much less (~12x in 3 years at OpenAI) and the cost to run the frontier rose.

## 4. Counter-evidence (prices that went UP)
- Claude 3.5 Haiku launched at 4x Claude 3 Haiku (Nov 2024); Haiku 4.5 is 4x Haiku 3 input. Anthropic's small SKU: $0.25 (2024) → $0.80 → $1.00 (2025-26).
- Gemini: 2.5 Flash 3x/6x 2.0 Flash (2025); 3 Flash above 2.5; 3.5 Flash 3x 3 Flash (May 2026); Flash-Lite $0.075 → $0.10 → $0.25 → $0.30 in/ $0.30 → $2.50 out (2025-26). HN user: "gemini-3.5-flash is 15x more expensive for input tokens than gemini-2.0-flash."
- OpenAI GPT-5.4 mini/nano (Mar 2026) at 3-4x GPT-5 mini/nano; GPT-5 mini to be retired.
- Introductory prices revert: Gemini 3.6-3.8 Flash double on 2027-01-01. (Anthropic's Sonnet 5 intro price, by contrast, was made permanent.)
- New Claude tokenizer: ~30% more tokens for the same text.
- Reasoning/"thinking" tokens bill as output; newer small models often reason by default, raising cost per line even at the same list price.
- BUT in September 2026 the direction reversed again at the bottom: GPT-5.6 Luna cut 80% (Jul 30) and GPT-6 Luna $0.10/$0.50 (Sep 22, "permanent"); Opus 5.5 and Sonnet 5 cut. The pattern is a new small model launching HIGHER than its predecessor, then competition pushing it down.

## 5. DERIVED: Haiku-class price over time

Two definitions, because they tell different stories.

**A. The Anthropic small model we would actually be calling (list price, in / out):**
| Date | Model | Price |
|---|---|---|
| Sep 2023 | Claude Instant 1.2 | $1.63 / $5.51 |
| Sep 2024 | Claude 3 Haiku (+ caching from Aug 2024) | $0.25 / $1.25 |
| Sep 2025 | Claude 3.5 Haiku (Haiku 4.5 arrived 3 weeks later at $1/$5) | $0.80 / $4.00 |
| Sep 2026 | Claude Haiku 4.5 | $1.00 / $5.00 |
Net over three years: roughly flat in price, much higher in capability. The saving arrives as "more capability at the same price", not "same capability cheaper".

**B. Cheapest credible price for our CURRENT capability need (roughly Haiku 4.5 level; the Haiku 3 level shown for comparison):**
| Date | Haiku-3-level floor | Haiku-4.5-level floor | Basis |
|---|---|---|---|
| Sep 2023 | ~$1.50 / $2.00 (GPT-3.5-turbo; slightly below Haiku 3) | not available at any price below ~$10/$30 (GPT-4 Turbo class, Nov 2023) | dated prices above |
| Sep 2024 | ~$0.075-0.15 / $0.30-0.60 (Gemini 1.5 Flash, GPT-4o mini) | ~$2.50-3 / $10-15 (GPT-4o, Sonnet 3.5) | dated prices above |
| Sep 2025 | ~$0.05-0.10 / $0.30-0.40 (GPT-5 nano, 2.0 Flash-Lite, 4.1 nano) | ~$0.25-1.00 / $2-5 (GPT-5 mini, Gemini 2.5 Flash; Haiku 4.5 in Oct) | dated prices above |
| Sep 2026 | ~$0.02-0.06 / $0.04-0.40 (open 8-24B models on DeepInfra; GPT-5 nano) | ~$0.10-0.30 / $0.50-2.00 (GPT-6 Luna, Gemini 3.1 Flash-Lite, DeepSeek V4 Flash, GPT-5 mini) — capability parity for OUR dialogue NOT tested | dated prices above |
Haiku-3 level fell ~20x in year one, then ~1.5-2x a year: the floor flattens as the capability ages, which matches Epoch's 66% → 32% per quarter slowdown. Haiku-4.5 level fell ~3-10x in its first year, measured at the cheapest cross-vendor option, not at Anthropic.

**Projection for Haiku-4.5-level capability (in / out per million; cost per cached line in brackets, same workload as section 1):**
| | Low decline | Central | High decline |
|---|---|---|---|
| Sep 2027 | $1.00 / $5.00 [$0.00072] — stay on an Anthropic Haiku; Haiku 5.5 priced like 4.5, maybe +30% tokens | $0.25 / $1.25 [~$0.00018] — ~4x, a new Haiku or a switch priced like GPT-5 mini/GPT-6 Luna | $0.08 / $0.40 [~$0.00006] — ~12x, Epoch's 13x/yr average holds |
| Sep 2028 | $1.00 / $5.00 or higher [$0.00072+] — same | $0.08 / $0.40 [~$0.00006] — another ~3x as the capability ages (Epoch's ~32%/quarter aged rate is ~4.6x/yr) | $0.01-0.02 / $0.05-0.10 [<$0.00001] — near today's open-model floor for 8B-class |
Reasoning: (1) fixed-capability decline is real and averages 5-13x/yr across independent studies, but it slows as a capability ages and is measured at the cheapest vendor; (2) vendors' own small SKUs have not fallen in price over three years and new small models repeatedly launch higher; (3) the September 2026 cuts (GPT-6 Luna, Opus 5.5, Sonnet 5) show competition does push prices down again within months; (4) capturing the central case likely means either Anthropic cutting the Haiku price or us being able to switch vendor/model, which needs our dialogue tests to pass on the cheaper model.

**Planning recommendation (DERIVED):** budget at today's Haiku 4.5 price with caching (~$0.0007/line) and treat any decline as upside; keep the dialogue layer model-agnostic enough to swap to a cheaper model when one passes our quality tests; watch for the Haiku 5.5 price and tokenizer (expected within weeks of 2026-09-22).
