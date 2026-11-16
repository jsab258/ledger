Method researched: OpenAI API reference (chat create, streaming events), OpenAI prompt-caching and rate-limits guides, Google Gemini OpenAI-compatibility page, Groq OpenAI-compatibility, prompt-caching and API-reference pages, OpenRouter overview and prompt-caching guide, llama.cpp server README
Reference: studies/03-dialogue-barks.md

# Item n16-6, provider-neutral step: method note (first pass, no decisions)

Read 16 Nov 2026. Nothing coded, run or called; no key read. Doc pages were fetched through a page-reading tool that returns an extract, not raw text; every doc claim below is that extract (the reading is therefore second-hand; a reviewer should re-open the links before a number is relied on). Study 03 (dialogue barks) covers bark pacing, not provider APIs: it gives the 2 s bar and reply length targets (line 88) but nothing on streaming clients; "none found" for a studied game's LLM client.

## 1. What every caller relies on (home files, ledger/Assets/Scripts/Core)

- Plain call: ILlmClient.CompleteAsync, LlmClient.cs:62-65. Used by ConversationEngine.cs:914, 1795, 1952, 2189, 2408; ClaimCheck.cs:372, 410, 481, 536; Director.cs:181; IntentRouter.cs:345; Suggest.cs:212.
- Streaming text, whole text so far on each growth: IStreamingLlmClient, LlmClient.cs:72-75; used at ConversationEngine.cs:1900 (fast draft) and 1922 (main), ClaimCheck.cs:480.
- First-token callback, once, fired by thinking or text: IStartingLlmClient, LlmClient.cs:82-85; AnthropicClient fires at content_block_start/delta (LlmClient.cs:267-272, 298-302). ClaimCheck.FirstOfTwo uses it to keep the copy the model starts first (ClaimCheck.cs:370-410). BudgetedClient falls back to first text when the inner client lacks it (BudgetedClient.cs:135-144).
- Cached heads: LlmMessage.CachedHead (LlmClient.cs:18, 20), LlmRequest.CacheSystem (39) and CachedSystemHead (42); sent as cache_control blocks (Body, 365-393), not sent through the relay (373). Callers: ClaimCheck.cs:183, 661; ConversationEngine.cs:1916, 2128, 2279.
- Token usage for cost: LlmResponse.InputTokens is billed-equivalent (Billed(), 58-59: write 1.25x, read 0.1x), OutputTokens, Model (45-60); read by BudgetedClient.Settle (BudgetedClient.cs:104-115) and ConversationEngine.cs:1929 (_cost.Record). Cost table Models.Cost (LlmClient.cs:96-111) is keyed by model name; an unknown model is settled as asked, and the relay prices unknown models at 15/75 (Relay.cs:92).
- Stop reason: only the check reads it, to detect a cut reply, "max_tokens" (ClaimCheck.cs:541). Any other provider must map "length" to "max_tokens".
- Thinking off/low: LlmRequest.Thinking, Effort (LlmClient.cs:34, 36), set by ClaimCheck.cs:186, 354, 662 and ConversationEngine.cs:1918, 2279; AddOptions (409-413).
- Stopped stream carries what it used: LlmStreamStoppedException.SoFar (473-477), caught at BudgetedClient.cs:155, ClaimCheck.cs:402, ConversationEngine.cs:1905, 1929. Output tokens estimated at four characters a token when no usage arrived (LlmClient.cs:263-266). OpenAI's own docs say an interrupted stream "may not receive the final usage chunk" (see 2), so this estimate path becomes the common case, not the edge.
- Broken stream: LlmStreamBrokenException (464-467), caught at ClaimCheck.cs:396, 403, 481 and ConversationEngine.cs:1932; the stream call itself falls back to CompleteAsync on a non-200 start (LlmClient.cs:243-250).
- Error kinds: LlmApiException.StatusCode, ErrorType, Until (445-459), parsed from an Anthropic-shaped error body at 338-349; the game reads it at ConversationHost.cs:172 (the relay's "allowance_spent" and "until"). Retries: 429 and 5xx, 3 times, 2/4/8 s (170-215). Retry-After is not read today (grep: none), so nothing to map.
- The relay (Relay.cs:231-239, 282-285) speaks Anthropic upstream only, picks the model by role (core, ambient), strips every field but model, max_tokens, system, messages, stream, and holds the key. A neutral client for the open game goes through the relay only if the relay gains a second upstream; that is outside this note.

## 2. OpenAI Chat Completions format (OpenAI API reference, read 16 Nov 2026)

Links: developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create; .../streaming-events; developers.openai.com/api/docs/guides/rate-limits. (platform.openai.com/docs/api-reference/chat/streaming returned HTTP 403: not reached.)
- Request: model; messages with roles developer, system, user, assistant, tool; max_tokens deprecated for max_completion_tokens (which counts reasoning tokens; max_tokens is not accepted by o-series); stream (default false); stream_options.include_usage; reasoning_effort (none ... max); temperature 0 to 2.
- Streaming: SSE, object "chat.completion.chunk", same id on each chunk, choices[].delta.content, choices[].finish_reason. finish_reason values: stop, length, tool_calls, content_filter, function_call (deprecated). With include_usage, an extra chunk before "data: [DONE]" carries usage for the whole request; usage is null on the others. If the stream is cut, the final usage chunk may not arrive.
- Usage: prompt_tokens, completion_tokens, total_tokens, completion_tokens_details.reasoning_tokens, prompt_tokens_details.cached_tokens (and cache_write_tokens).
- Errors: status, type, code (429 with type rate_limit_error, code slow_down; other errors also use 429, so check type and code together). The extract gave no sample body; the body shape {"error":{"message","type","code"}} is unverified from this read.
- Rate-limit headers: Retry-After (seconds, when present), x-ratelimit-limit/remaining/reset-requests and -tokens, plus -project-tokens variants. Retry-After does not make quota or billing errors retryable.
- OpenAI caching: automatic on supported models; min 1,024 tokens for GPT-5.6 and later (earlier varies); whole rendered prefix must match; GPT-5.6 and later in explicit mode caches only with explicit breakpoints. The caching guide names usage.input_tokens_details.cached_tokens (Responses API); the chat reference names prompt_tokens_details.cached_tokens. Read 16 Nov: developers.openai.com/api/docs/guides/prompt-caching.

## 3. Who speaks it (read 16 Nov 2026)

| | Base URL | Auth | Streaming usage | Caching | Cached tokens |
|---|---|---|---|---|---|
| Gemini | https://generativelanguage.googleapis.com/v1beta/openai/ | Authorization: Bearer key | Page's only example sets stream_options include_usage and prints chunk.usage; not documented as general (partly unverified) | Explicit via extra_body cached_content (Gemini content cache); implicit for 2.5 series per OpenRouter's guide | Not stated on the page: unverified |
| Groq (chosen: clearest OpenAI-compat page; Together and Cerebras not read) | https://api.groq.com/openai/v1 | Bearer key | Not confirmed: compat page silent; API-reference extract gives stream_options no sub-fields. Unverified | Automatic, cannot be disabled; only openai/gpt-oss-20b, -120b, -safeguard-20b; 128 to 1,024 min tokens by model; 50% discount | usage.prompt_tokens_details.cached_tokens |
| llama.cpp server | http://host:port, route /v1/chat/completions (path from README feature list and section) | optional --api-key or LLAMA_API_KEY, none by default | stream_options not mentioned in the 30,000 to 130,000 character range read; last 10,522 characters unread. Unverified | KV reuse, cache_prompt default true (on /completion) | usage.prompt_tokens_details.cached_tokens in the response example (0 shown); timings.cache_n |
| OpenRouter | https://openrouter.ai/api/v1/chat/completions | Bearer key | Usage once in the final chunk, with a non-empty choices array carrying an empty delta and the finish_reason (differs from OpenAI's empty choices) | Automatic for OpenAI, Grok, Groq, DeepSeek, Gemini 2.5 implicit and others; Anthropic and Qwen need cache_control: top-level field (breakpoint moves) or per content block, up to four, TTL 5 min or "1h" | prompt_tokens_details.cached_tokens and cache_write_tokens; cache_discount in body |

Differences that matter:
- Gemini: reasoning cannot be turned off on 2.5 Pro, 3 or 4; reasoning_effort "none" only on 2.5; reasoning_effort and thinking_level/budget cannot be combined; "still in beta". Thinking cost on first-token time is the main risk for a classifier on the voice's path (see Thinking, LlmClient.cs:29-34). Page also moved: ai.google.dev/gemini-api/docs/openai redirects 301 to aistudio.google.com/docs/openai (read there). The extract flagged inconsistencies in the page's own caching example (base URL without openai/, nested extra_body); unverified.
- Groq: logprobs, logit_bias, top_logprobs, messages[].name give 400; n must be 1; temperature 0 becomes 1e-8.
- llama.cpp: local, no cost and no billing; rate limits and Retry-After not read; whether the AMD card's backend serves the route is a separate hardware question (Vulkan not mentioned in the README text read).
- OpenRouter: errors as {code (number), message, metadata}, and may arrive inside a choice; rate-limit headers not documented on the overview page; it may fall back to another provider on 5xx or rate limit, so the model that answered must be recorded (response model field, standard in OpenAI shape).

## 4. The seam

One OpenAiCompatibleClient beside AnthropicClient in LlmClient.cs (or its own file), implementing IStartingLlmClient, taking base URL, key (or none for a local server), auth header builder and an optional HttpMessageHandler, as AnthropicClient does (LlmClient.cs:151). BudgetedClient, ConversationEngine and ClaimCheck need no change: they hold the interface.

Mapping:
- LlmRequest.System becomes a first message with role "system" (or "developer" for o-series; unverified for which target models want it).
- LlmMessage.Content maps directly. MaxTokens maps to max_completion_tokens for OpenAI; max_tokens for hosts that still use it (Groq, llama.cpp unverified): a per-provider setting.
- stream true plus stream_options.include_usage true; parse "data:" lines, choices[0].delta.content, finish_reason, a chunk with usage and any choices.
- StopReason: stop becomes "end_turn", length becomes "max_tokens" (the one value read, ClaimCheck.cs:541).
- onStart: first chunk with delta.content, or a reasoning delta where the host sends one (field names differ by host; unverified). Otherwise first text, as BudgetedClient already does for a client without it.
- Usage: prompt_tokens less cached_tokens is uncached; cached_tokens is CacheReadTokens; cache_write_tokens is CacheWriteTokens; InputTokens through LlmResponse.Billed, with the price ratios a per-provider setting, because Billed() hard-codes Anthropic's 1.25 and 0.1 (OpenAI reads at a different ratio; Groq 50% discount is the stated one). A per-model rate card entry in Models.Cost is needed for every candidate (unknown models are priced as asked or high).
- Errors: same LlmApiException; read error.message, error.type, error.code; Retry-After header becomes the retry delay where present (new; the Anthropic path does not read it). Mid-stream error chunk or EOF before [DONE] becomes LlmStreamBrokenException; cancellation becomes LlmStreamStoppedException with the four-characters estimate.
- Cannot map: explicit cache_control on CachedHead and CachedSystemHead as sent to Anthropic. Fallback: send the whole text in order (system first, stable head first) so providers with automatic prefix caching (OpenAI, Groq, llama.cpp KV reuse) can hit it; head-length ordering already puts the stable part first (LlmClient.cs:14-18). Through OpenRouter to Anthropic, cache_control per content block is documented, so the client may send blocks there only; Gemini explicit via cached_content is a separate object lifecycle and is not mapped (cost unmeasured). Whether Content-first ordering gives hits on each host is to be measured, not assumed.
- Thinking and Effort: map to reasoning_effort where the host accepts it; omit elsewhere. Anthropic-only body fields stay out.

## 5. Fair measurement in the bake-off

The existing bench (ledger/ClaimBench/FastFirst.cs:58-70) logs per call: sentMs, begunMs (first moment of any output, thinking included), firstTextMs (first answer text), endMs, ended, inTok, outTok, from one stopwatch (_clock) per run (FastFirst.cs:744). The new client should feed those same fields unchanged:
- sentMs at SendAsync start; begunMs at onStart; firstTextMs at the first non-empty onText; same clock for all providers; thinkMs is firstTextMs minus begunMs (FastFirst.cs:299).
- Report the provider's own response model name and whether usage came from the service or from the four-characters estimate, so a provider that omits streaming usage is visible, not silently equal.
- Cold and warm cache runs recorded apart (CacheReadTokens per call), since providers differ on automatic against none; connection reuse (HTTP/2 and 6-minute pool, LlmClient.cs:137-144, 162-163) is set per client, and local llama.cpp has no network leg: label it.
- Invented details: judge every provider's sentences with ClaimCheck.CheckAsync (the whole check, per the project's own record that RequestItems+ParseItems misjudges), same facts, same prompt text, same check model, so only the talk model changes. Counts by claim-check refusal and the hard rule on unnamed persons, places, events, numbers, years (RULINGS, Talk and AI, Speech line). How the bench counts invented details per turn was not read in full here: unverified; a reviewer should confirm the field.
- 2 s bar is a newcomer's real questions, small talk reported beside it (RULINGS Talk and AI).

## 6. Acceptance cases (fake HTTP handler)

Pattern: ScriptedHandler in ledger/CoreTests/Program.cs:6675-6691 (steps returning a response or null for a drop), DroppingStream at 6694; TestRetryAndErrors is called at line 229. AnthropicClient accepts a handler (LlmClient.cs:151). The same constructor seam goes on the new client.
Cases (each a CoreTests case):
1. Plain call: body has system as first message, model, max tokens field per setting; response text, StopReason mapping, billed tokens.
2. Stream: three delta chunks, a finish chunk, a usage-only chunk, [DONE]: onText grows, onStart once at the first content, usage read from the last chunk.
3. Stream without a usage chunk (cut or omitted): estimate used, marked estimated.
4. Cached tokens: prompt_tokens_details.cached_tokens 800 of 1,000 gives CacheReadTokens 800 and the Billed figure.
5. OpenRouter-shaped final chunk (non-empty choices plus usage) parses the same.
6. 429 with Retry-After then 200: waits the given delay (delay hook as RetryDelay at LlmClient.cs:149); 429 repeated gives LlmApiException with type and code; 400 not retried; non-200 stream start falls back to the plain call.
7. Mid-stream error chunk or EOF before [DONE] gives LlmStreamBrokenException; cancellation mid-stream gives LlmStreamStoppedException with SoFar.
8. Through BudgetedClient and ConversationEngine with the fake: one turn passes end to end.
9. Regression: the existing Anthropic tests (retry, stream, cache blocks, relay copy code) unchanged; Body() output byte-identical for a fixed LlmRequest before and after the change (capture the JSON now as a golden); no edits to AnthropicClient's code paths.
10. No key in any log or failure message from the new client.

## 7. Not reached

- platform.openai.com/docs/api-reference/chat/streaming (HTTP 403); the developers.openai.com mirror was read instead.
- llama.cpp README: last 10,522 characters, and the first 30,000 characters, not read; stream_options and Vulkan unconfirmed.
- Groq: streaming usage and error and rate-limit headers unconfirmed; Together and Cerebras docs not read.
- Gemini: cached-token field and error format not on the page read.
- OpenRouter error-handling page and rate-limit headers not read.
- Study 03 read by search of terms only, not in full; no provider content expected in it.

## Changes from the fresh review (16 Nov; these bind over the text above)

The review (METHOD-NOTE-REVIEW-2026-11-16.md, pass with fixes) is taken whole; each change gets a test in the acceptance list.

1. A stream stopped by its caller on an OpenAI-style host has no usage block: its input cost is the prompt estimate, never 0, so the budget cap, the cost record and the two-copies race do not undercount.
2. Hosts that keep billing after a cancel (OpenRouter names Groq and Google): the two-copies run is off there, or both copies are counted.
3. Thinking: a per-model reasoning setting with a table mapping the callers' disabled/adaptive to it (callers at ConversationEngine.cs:1879, TalkLadder.cs:122, ThreatRead.cs:22 as well as those listed).
4. Billed() stays as it is for Anthropic; a separate price function per provider, feeding the cache counters ClaimBench and TalkHelper read.
5. Errors: a finish_reason "error" chunk inside a 200 stream is a broken stream; a finished reply needs finish_reason stop or length, not only [DONE]; billing 429s are never retried.
6. Rulings: the new client is for the bench only, with direct keys; the game keeps the relay (no key ships). OpenRouter requests set data collection to deny and pin the provider. Gemini only on a paid key (its data terms unread, unverified).
7. The bench's invented-details field exists (FastFirst.cs:96 and 283): no longer unverified. Still unverified: Gemini's cached-token field and error format, Groq's streaming usage, OpenAI's full error body.
