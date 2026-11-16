# Fresh review: OpenAiCompatibleClient (n16-6), 16 Nov 2026

Verdict: PASS WITH FIXES. The tests were read, not run.

Game untouched: `git diff` on LlmClient.cs is empty. The client sits in ledger/DevTools, outside Assets. It is compiled only by CoreTests (named file) and by the bench projects that glob `../DevTools/*.cs`. Program.cs gained one line, the call to `TestProviderClient`.

## Findings, most severe first

1. **Change 2 is not implemented.** `BillsAfterCancel` (OpenAiCompatibleClient.cs:52) is a flag that nothing reads. A grep of all .cs and .csproj files finds no other use. The comment says "read by the bench", but no bench code does, and no test touches it. Scenario: the bench runs the two-copies race on Groq or Google through OpenRouter, and the cancelled copy is billed as well. Fix: have the bench honour the flag, or make the client refuse to start a race while it is set, and add a test.

2. **Billing check too broad, and no cap on a wait.** The check is at :342-346 and the wait at :118.
   - Gemini's compat route sends its per-minute 429 with "You exceeded your current quota... billing details". That matches `quota` and `billing`, so a transient rate limit is never retried and the bench records a false failure.
   - The reverse case is a Groq daily-token 429. It has a long Retry-After and no matching word. The client then sleeps the full header value, up to 3 times, with no ceiling.
   - Fix: match on the type or code (`insufficient_quota`, `billing_hard_limit_reached`) rather than free text, and cap the wait, for example at 30 s, then throw.
   - Neither case is tested.

3. **Empty content block when head equals whole text.** `Body` at :293-296 (head chosen at :300, `CacheSystem` case) makes `Block(whole.Substring(head.Length), false)` an empty text block when the whole equals the head. That happens when `CacheSystem` is true and the head is the whole system text. Anthropic rejects empty text blocks with a 400 through OpenRouter. Scenario: SendCacheBlocks on, CacheSystem true, so every request fails. Fix: skip the second block when it is empty. The test at Program.ProviderClient.cs:207-212 covers only a proper prefix.

4. **Usage counted per chunk.** :259-260 add to the shared `AnthropicClient.CacheReadTotal` and `CacheWriteTotal` on every chunk that carries usage. Some hosts send cumulative usage on each chunk, so the cache totals are overcounted. Fix: add once, after the loop.

5. **A usage object with prompt_tokens 0 or missing prices input at 0** (:261-262, :219). A host that sends an early zero-filled usage block bypasses the "never 0" rule and `IsEstimated` stays false. Fix: if the prompt count is 0, use the estimate and mark it.

6. **Cancel before the first byte is not a stopped-stream error.** At :142 a cancel during `SendAsync` throws a plain `TaskCanceledException`, with no `SoFar` and no prompt estimate. Change 1 is met only once the body is open. Scenario: a loser copy is cancelled early on a host that still bills the prompt, and the budget sees 0.

7. **Fallback resends everything.** A non-200 stream start (:144-151) falls back to `CompleteAsync`. A 400 or 401 is therefore sent twice, and a 429 ignores the stream's Retry-After on the first re-send. This wastes a request and may double a bill.

8. **Key leak claim is slightly overstated.** :363 says "no key can reach a message", yet an unparseable body becomes the message whole (:366), unbounded. A host or proxy that echoes the Authorization header would leak it. The test's handler never echoes, so case 10 passes without exercising this. Fix: truncate the body to about 500 characters and scrub the key string.

9. **No idle timeout on an open stream.** `HttpClient.Timeout` ends at the headers under ResponseHeadersRead. A stalled stream with no token hangs for ever.

## Acceptance cases (ProviderClient tests, lines)

Cases 1-7, 9 and 10 are implemented and would fail on wrong code.
- 1: :98-111. 2: :114-122. 3: :125-128. 4: :131-136. 5: :139-141. 6: :145-170. 7: :173-191. 9: :224-227. 10: :230-235.
- Case 4 and the cache-write price are weak. `cache_write_tokens` and `CacheWritePrice` have no test, and no stream-with-cache test exists.
- Case 8 (:215-221) is weak. `budget.SpentUsd >= 0` is always true, and nothing checks ClaimCheck's "max_tokens" reading through the client.
- Case 10 checks messages only. No case sets up a key echoed in a body.

## Binding changes

- 1 (prompt estimate on stop): done and tested (:189), except for the cancel-before-body case in finding 6.
- 2: missing (finding 1).
- 3 (thinking table): done and tested (:204).
- 4 (separate price function): done (`Priced`, :250). Tested only for the read price.
- 5 (finish "error" broken, finish needs stop or length, billing 429 never retried): done and tested (:179-182, :162). The billing match is flawed (finding 2).
- 6 (bench only, data_collection deny): bench-only holds. The `ExtraBody` provider block is tested (:206). Pinning the provider is left to the bench's settings.
- 7: a note only.
