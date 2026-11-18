# Talk bake-off, legs 2 to 5: which models to run (n16-6)

Lane research, 18 Nov 2026, 05:25 to 05:50 Swiss time. Machine-free; nothing called, bought or downloaded. Three helpers (Sonnet) read the web, the lane checked their weakest points itself. Builds on the main session's METHOD-NOTE-2026-11-16.md (the OpenAI-compatible client, its review's seven changes) and BAKEOFF-SONNET55-2026-11-16.md (leg 1). Every figure carries its source and the date read; "unverified" means no page that says so was read.

## The short answer

| Leg | Model to run | Why | Talk price (US$ per million in / cached / out) | Live first token, P50 24 h (Vercel AI Gateway, read 18 Nov) |
|---|---|---|---|---|
| 2 Google | gemini-3.5-flash-lite, thinking_level minimal | Google's small fast model; 3.5 Flash is already deprecated and routes to 3.6 Flash | 0.30 / 0.03 / 2.50 | 0.7 s, 435 tokens/s |
| 3 OpenAI | gpt-6-luna, reasoning_effort none | OpenAI's cheapest current model; there is no GPT-6 mini or nano | 0.10 / 0.01 / 0.50 | 2.6 s at its default effort (medium), 102 tokens/s |
| 4 Open model, fast host | openai/gpt-oss-120b on Groq, reasoning_effort low, include_reasoning false | Apache 2.0 weights, the fastest live first token found, documented no-retention default | 0.15 / 0.075 (method note's 50% rule; Vercel shows 0.08) / 0.60 | 0.2 s, 461 tokens/s |
| 5 Local, his RX 6700 | Qwen3-4B-Instruct-2507 at Q4_K_M, llama.cpp with Vulkan | Apache 2.0, about 2.5 to 3 GB, fits beside the game; the non-thinking variant | none (his card) | not published for this card |

Alternates: leg 2, gemini-3.6-flash if Flash-Lite fails the bar on quality (id and price unverified); leg 3, gpt-6-luna-fast (twice the price) only if Luna with none misses 2.0 s; leg 4, Cerebras for gpt-oss-120b (0.35 / 0.75), or qwen/qwen3.8-27b on Groq with reasoning_effort none (0.80 / 4.00, preview only, may be withdrawn at short notice); leg 5, Gemma 4 E4B (Apache 2.0 since 2 Apr 2026), then Gemma 4 E2B or Phi-4-mini (MIT) if memory is tighter.

For comparison, today's game: Haiku 4.5 at 1 / 5 for small talk, Sonnet 5 at 2 / 10 for real conversation (prices as on the project's card, BAKEOFF-SONNET55).

## Warnings that change how the legs are run

1. Thinking cannot be fully off on two of the four. Gemini 3.x: thinking_level takes minimal, low, medium (default), high; Google's own page warns "minimal does not guarantee that thinking is off" (whats-new-gemini-3.5, read 18 Nov). gpt-oss: Groq's and Cerebras' reasoning pages list only low, medium and high for it; whether "none" is refused with an error is not confirmed (test with one call). Low is the floor to plan for. So the bench's begunMs (first output, thinking included) and firstTextMs (first answer text) will differ for these two; only firstTextMs counts against the 2.0 s bar.
2. Gemini's OpenAI-compatible endpoint has a record of refusing reasoning_effort "minimal" on Gemini 3 Flash (two Google forum threads in search results, titles only, not read). If it refuses, send Google's own thinking setting through extra_body, as the method note's table says for caching. Test it with one call before the arm.
3. The published latency figures disagree because they measure different things. Artificial Analysis times the first answer token after all thinking at a high setting (gpt-oss-120b High: Groq 6.00 s, Cerebras 2.24 s; GPT-6 Luna Max: 67.90 s; Gemini 3.5 Flash-Lite: 4.78 s). Vercel's gateway times the first token of any kind on live traffic at whatever setting callers send. Neither is the bar; the bench's own firstTextMs with thinking at its lowest is the only figure that counts.
4. Hosts that keep billing after a cancel (the method note's review names Groq and Google): run these arms with the two-copies race off, or count both copies.
5. Streaming usage (stream_options include_usage) is unconfirmed on Gemini's compatible endpoint and on Groq; llama.cpp fixed its final usage chunk to match OpenAI's in Aug 2025 (issue 15443, closed). Every arm must report whether its usage came from the service or from the four-characters estimate (method note, section 5).
6. The local model's cost to the frame is unmeasured anywhere we could find. Its arm needs a second number beside the bench: frame time and card memory with the game running and llama-server answering (PresentMon is already on the allowlist as a measuring tool, item 12).

## Leg by leg

### Leg 2: Google, gemini-3.5-flash-lite

- Id google/gemini-3.5-flash-lite on Vercel (read 18 Nov); released 21 Jul 2026; 1M context, 65K output. Generally available or preview: unverified (Google's pricing and model pages refused the helper).
- Price 0.30 in, 0.03 cached, 2.50 out, thinking billed as output (Vercel, Artificial Analysis, read 18 Nov).
- Data: on a paid key (a Cloud project with billing) prompts are not used to improve Google's products and are logged "for a limited period" for abuse checks, no period stated; free use may be read by human reviewers (Gemini API Additional Terms, archived version of 18 Dec 2025; a newer version not checked). So, as the method note's review already ruled: a paid key only.
- Caching: 90% discount (Artificial Analysis); automatic or explicit, and minimum length, unverified.

### Leg 3: OpenAI, gpt-6-luna

- Id gpt-6-luna; released 22 Sep 2026 (per Vercel and Artificial Analysis; not on OpenAI's model page); described by OpenAI as its "most efficient model for focused, high-volume tasks". OpenAI's pricing page lists no mini or nano in the GPT-6 family; gpt-4.1-mini is marked deprecated (OpenAI model and pricing pages, read 18 Nov).
- Price 0.10 in, 0.01 cached, 0.50 out, cache write 0.125; fast mode twice; above 272K input tokens dearer (no game call comes near).
- reasoning_effort accepts none, low, medium (default), high, xhigh, max; send none explicitly (OpenAI model page, read 18 Nov). Vercel's 2.6 s live figure is at callers' settings, mostly the default, so none should be quicker: to measure.
- Data: API data not used for training unless opted in; abuse logs up to 30 days for chat completions; zero retention only for approved customers; prompt caching may keep encrypted key-value data up to 24 hours (OpenAI "your data" guide, read 18 Nov).

### Leg 4: open model on a fast host, gpt-oss-120b on Groq

- Id openai/gpt-oss-120b on Groq; also gpt-oss-20b at 0.075 / 0.30 if the 120b's reasoning floor is too slow (Groq models page, read 18 Nov). Groq lists no Llama 4.
- Live P50 on Vercel's gateway: Groq 0.2 s and 461 tokens/s; Baseten 0.3 s; Bedrock and Parasail 0.4 s; Nebius and Together 0.5 s; Cerebras not shown (read 18 Nov). The first token there may be a reasoning token, so firstTextMs will be later.
- Settings: reasoning_effort low, include_reasoning false (Groq reasoning page, read 18 Nov).
- Weights: Apache 2.0 per the Hugging Face model card; no separate use policy seen there; full licence text not read.
- Data: Groq keeps no inference data by default, may keep logs up to 30 days for reliability and abuse, any customer can switch on zero retention in Data Controls; storage in US Google Cloud; training use not stated; an EU region not documented (Groq "your data" page, read 18 Nov; a Helsinki data centre exists per a news snippet only).
- Not verified: Fireworks and SambaNova prices and terms; Together's retention.

### Leg 5: local on his RX 6700, Qwen3-4B-Instruct-2507

- Backend: llama.cpp with Vulkan. AMD does not officially support the RX 6700's chip (gfx1031) for ROCm; the override is experimental with no shown gain (bestllmfor.com guide, secondary; level1techs post of 18 Aug 2026 lists the 6700 XT as runtime-only on Windows).
- Speed: the only measured RDNA2 figures are old llama.cpp builds with Llama 2 7B Q4_0 on Vulkan: RX 6700 XT 1,051 tokens/s reading the prompt, 83.9 tokens/s writing (llama.cpp discussion 10879, started Dec 2024). A 4B model at Q4 should write faster than that and the plain 6700 is a little slower than the XT: both lane inferences, to measure.
- Memory: about 2.5 to 3 GB for the weights at Q4_K_M plus 0.3 to 0.5 GB for a few thousand tokens of context (estimate from parameter count).
- Licence: Apache 2.0 for Qwen3-4B-Instruct-2507 and Gemma 4, MIT for Phi-4-mini, all per secondary pages; the model cards themselves were not read, and a quantised copy can carry its own terms. The allowlist's rule (its line 29): a new tool needs a decision record citing the weights licence. Llama 3.2's community licence is the heaviest; skip it. Older Gemma 1 to 3 keep Google's prohibited-use terms; Gemma 4 does not.
- Fixed briefing reused across turns: send cache_prompt true explicitly (its default was not confirmed).
- RULINGS: a local model is already the planned offline fallback (24 Sep) and the small local checker exists (Speech line); this leg is for small talk only, as the order says.

## What each arm costs (the talk model's share, a lane estimate)

Leg 1's Haiku 4.5 arms cost US$0.19 to 0.25 for 60 turns at 1 / 5, the check on Haiku 5.5 included. (The talk share alone was not split out in BAKEOFF-SONNET55; split it from the leg 1 logs before quoting any figure.) Scaling only the talk model's prices, and assuming the same token counts as Haiku, gives roughly: Luna about a tenth of Haiku's talk share, gpt-oss on Groq about an eighth, Flash-Lite about a third to a half (its output price is half Haiku's, its input a third). This is a floor: gpt-oss at low effort and Flash-Lite at minimal still bill thinking as output, so their real share may be higher; measure it from each arm's own usage. The checker's cost is unchanged in every arm. Four arms, each run twice as in leg 1, stay well inside the task's US$4.00 cap (set in code, as BAKEOFF-SONNET55 records) and today's ceiling; the local arm costs only the checker.

## What the main session does with this

1. Add a Models.Cost row and a per-provider price function for the three cloud models (method note review, change 4), with the figures above re-read at source before any cost reaches his page.
2. One trial call per provider for the thinking setting and streaming usage (warnings 1, 2, 5), then the arms as leg 1 ran them: the held newcomer set, 60 turns an arm, --parallel 1, twice, same machine and network.
3. Keys: Google needs a paid Cloud project, Groq a key; both are sign-ups on his accounts, so one batched ACTION if no key exists (the order's taps rule). OpenAI's key may already exist (unverified here).
4. The local arm only after a decision record citing the chosen weights' licence read at the model card, and with frame time measured beside it.
5. Suggested order: gpt-oss on Groq and Flash-Lite first (fastest live first tokens), then Luna, then the local model.

## Decisions (the main session decides; none needs his page)

1. Leg 2's model: gemini-3.5-flash-lite (recommended) or gemini-3.6-flash.
2. Leg 4's host: Groq (recommended) or Cerebras.
3. Leg 5's model: Qwen3-4B-Instruct-2507 (recommended) or Gemma 4 E4B. Shipping a local model inside the game is a licence question for his page only if a local model wins.

## Sources (read 18 Nov 2026 unless marked)

- Vercel AI Gateway model pages: https://vercel.com/ai-gateway/models/gemini-3.5-flash-lite ; https://vercel.com/ai-gateway/models/gpt-6-luna ; https://vercel.com/ai-gateway/models/gpt-oss-120b
- Artificial Analysis: https://artificialanalysis.ai/models/gemini-3-5-flash-lite ; https://artificialanalysis.ai/models/gpt-6-luna-non-reasoning ; https://www.artificialanalysis.ai/models/gpt-oss-120b/providers ; https://www.artificialanalysis.ai/models/gpt-oss-120b-low/providers (fetched; it showed only the High figures)
- Google: https://ai.google.dev/gemini-api/docs/whats-new-gemini-3.5.md.txt ; https://ai.google.dev/gemini-api/terms-archive/terms_12_18_25 ; forum threads on reasoning_effort minimal (titles in search results only)
- OpenAI: https://developers.openai.com/api/docs/models/gpt-6-luna.md ; https://developers.openai.com/api/docs/pricing ; https://developers.openai.com/api/docs/guides/your-data/index.html
- Groq: https://console.groq.com/docs/models.md ; https://console.groq.com/docs/reasoning.md ; https://console.groq.com/docs/your-data.md
- Cerebras: https://inference-docs.cerebras.ai/api-reference/models/public-models.md ; https://inference-docs.cerebras.ai/capabilities/reasoning.md ; https://www.developersdigest.tech/models/data-retention/cerebras (third-party)
- Hugging Face: https://huggingface.co/openai/gpt-oss-120b
- Local: https://github.com/ggml-org/llama.cpp/discussions/10879 ; https://github.com/ggml-org/llama.cpp/issues/15443 ; https://bestllmfor.com/guide/llm-radeon-rx-6700-xt/ (secondary) ; https://github.com/lemonade-sdk/llama.cpp-builds ; https://the-decoder.com/googles-gemma-4-is-now-available-with-apache-2-0-licensing-for-the-first-time/ ; https://www.ertas.ai/blog/on-device-tool-calling-2026-qwen3-gemma4-phi4 (secondary, undated)
- Third-party proxy docs, used only where marked: https://docs.apiyi.com/en/api-capabilities/gemini-3-5-flash-lite/chat-completions.md

## Review

Fresh review 18 Nov (Sonnet helper): PASS WITH FIXES; five sources re-opened and matching; its six fixes applied (thinking floor wording, Luna's date source, cost estimate as a floor with leg 1's split owed, the cap's source, Groq's cache figure). Groq's data terms and the gpt-oss model card were read by a helper only, not re-opened by the reviewer.

## Not reached

Google's own pricing and model pages (refused); Gemini caching minimum and its cached-token field; OpenAI's caching guide for GPT-6; Fireworks and SambaNova; Groq's and Gemini's streaming usage; any measured figure for a 1B to 4B model on RDNA2; frame time with a model beside a game; the model cards' licence texts themselves.
