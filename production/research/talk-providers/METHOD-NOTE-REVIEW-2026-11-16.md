# Fresh review: talk-providers METHOD-NOTE-2026-11-16 (n16-6, first step)

Reviewed 16 Nov 2026 by a fresh helper that did not write the note. Code read in full where cited; doc pages re-opened 16 Nov 2026 through a page-reading tool (extracts, not raw text). Nothing run, called or keyed.

**Verdict: pass with fixes.** The seam (one OpenAI-shaped client behind IStartingLlmClient, AnthropicClient untouched) is right. Five behaviours callers rely on would quietly change for the new client unless the note names them.

## (a) Citations
All cited lines say what the note claims (LlmClient.cs 18-20, 39-42, 58-59, 62-85, 149-151, 170-215, 243-250, 263-272, 298-302, 338-349, 365-413, 445-477; BudgetedClient.cs 104-115, 135-144, 155; ClaimCheck.cs 183-186, 354, 370-410, 480-481, 536, 541, 661-662; ConversationEngine.cs 914, 1795, 1900-1952, 2128, 2189, 2279, 2408; Director.cs:181; IntentRouter.cs:345; Suggest.cs:212; ConversationHost.cs:172; Relay.cs 92, 231-239, 282-285; CoreTests Program.cs 229, 6675-6694; FastFirst.cs 63-65, 299, 703-745). Fixes:
1. Line 17: the four-characters estimate covers only a stopped stream (SoFar), not a finished stream lacking usage. Say so.
2. Thinking is also set at ConversationEngine.cs:1879, TalkLadder.cs:122, ThreatRead.cs:22; add them.
3. The bench's invented-details field exists (FastFirst.cs:96, filled at 283 from engine.LastInvented); drop "unverified".

## (b) Provider facts
- OpenAI (chat create reference): confirmed include_usage chunk before [DONE], "may not receive the final usage chunk" if interrupted, cached_tokens and cache_write_tokens, max_tokens deprecated, finish_reason list, reasoning_effort none/minimal/low/medium/high/xhigh/max ("not all models support every value"). Error-codes guide (developers.openai.com/api/docs/guides/error-codes): 429 slow_down is type rate_limit_error; billing 429s carry codes credit_balance_exhausted, organization/project_spend_limit_exceeded, organization_usage_limit_exceeded, and "retrying billing, spend, or quota errors won't restore API access"; follow Retry-After on 429 and 503 (server_is_overloaded). Full error-body shape still unverified.
- Gemini (aistudio.google.com/docs/openai): confirmed base URL, beta status, "none" only on 2.5, Pro 2.5/3/4 cannot turn reasoning off. reasoning_effort list is minimal..xhigh. Cached-token field, error format, streaming usage and data use: still unverified.
- Groq: compat page confirmed; API reference collapses stream_options, so streaming usage and cached-token field stay unverified; caching facts not re-checked.
- llama.cpp README now read whole (both parts): no stream_options, include_usage or Vulkan anywhere; errors "in the same format as OAI" ({code, message, type}); reasoning via reasoning_content. Correct section 7 accordingly.
- OpenRouter (openrouter.ai/docs/api-reference/streaming): confirmed final usage chunk; also: comment lines ": OPENROUTER PROCESSING"; mid-stream errors arrive with status 200 as a chunk with top-level error and finish_reason "error"; cancelling stops billing only for OpenAI, Anthropic, Azure; Groq and Google "not currently supported", billed in full.

## (c) The seam
4. **Stopped stream loses its prompt cost.** Anthropic reports input at message_start, so SoFar carries it; OpenAI-shaped hosts report usage only at the end, so SoFar.InputTokens is 0 and BudgetedClient.Settle (155-157), _cost.Record (CE 1929) and FirstOfTwo's AddUse undercount. Fix: when no usage arrived, SoFar's input is the prompt estimate (share BudgetedClient.PromptTokens), marked estimated.
5. **Cancel may not stop the bill.** Per provider flag "bills after cancel"; when set, a stopped stream settles at MaxTokens output; the bake-off runs those hosts with ClaimCheck.TwoCopies off or counts both copies.
6. **Thinking never switched off.** Callers set Thinking only for Anthropic names (ClaimCheck.cs:174, CE 250-253), so Gemini/OpenAI models get null and reason by default, hurting first-token time. Fix: per-model default reasoning_effort in the client's settings (lowest accepted), and a mapping table: "disabled" to none/minimal, "adaptive"+Effort to Effort; record the setting per call.
7. Leave LlmResponse.Billed untouched (the Anthropic path uses it); add a separate per-provider pricing function.
8. Errors: finish_reason "error" or an error chunk becomes LlmStreamBrokenException; completion needs a finish_reason of stop/length (the usage chunk's repeat ignored), not just [DONE]; billing 429s are never retried.
9. Feed AnthropicClient.CacheReadTotal/CacheWriteTotal or a shared counter; ClaimBench Program.cs:1073 and TalkHelper Program.cs:1690 read them.

## (d) Acceptance cases
Add: (11) stopped stream with no usage gives input estimate; (12) OpenRouter error chunk, finish_reason "error", gives broken; comment lines skipped; (13) 429 credit_balance_exhausted not retried, 503 with Retry-After waits; (14) body carries the per-model reasoning_effort when Thinking is null; (15) bills-after-cancel settles at worst case; (16) cache counters fed. Case 9 should also run the whole CoreTests suite and assert Billed(1000,0,800) unchanged. Case 6 should state that the existing Anthropic 429 path stays as is (no Retry-After added there).

## (e) RULINGS, Talk and AI
10. "Key never ships": state the new client is bench-only with direct keys; the game path stays AnthropicClient with CopyCode through the relay until a relay upstream is decided; a check that the packaged game builds no direct-key client.
11. "No training on its answers": OpenRouter requests set provider data_collection "deny" (and zdr where offered) and pin the provider (order plus allow_fallbacks false) so the measured host is the named one (openrouter.ai/docs/features/provider-routing); Gemini through a paid key only (its data-use terms not read: unverified).
12. "Reply check on Haiku, not Gemini": the note keeps the check model fixed; keep it so.
