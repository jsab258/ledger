using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Runtime.CompilerServices;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

namespace Ledger.DevTools
{
    /// A SECOND PROVIDER FOR THE TALK BAKE-OFF (his order of 16 November 2026, item n16-6;
    /// production/research/talk-providers/METHOD-NOTE-2026-11-16.md and its review's binding changes): the OpenAI-style
    /// Chat Completions format, which OpenAI, Groq, OpenRouter, Gemini's compatibility route and a local llama.cpp server
    /// all speak. FOR THE BENCH ONLY, with direct keys: the game keeps the relay and ships no key (the note's change 6),
    /// which is why it lives in DevTools, outside the game's own scripts. AnthropicClient is not touched.
    ///
    /// It holds the same interfaces as AnthropicClient, so BudgetedClient, ConversationEngine and ClaimCheck take it
    /// unchanged. Differences, each per provider and set by the bench:
    /// - the system text goes as the first message (SystemRole: "system", or "developer" for hosts that want it);
    /// - the reply's length goes as MaxTokensField ("max_completion_tokens" at OpenAI, "max_tokens" elsewhere);
    /// - the cache is the host's own prefix cache (no cache_control) unless SendCacheBlocks, for OpenRouter to Anthropic;
    /// - prices: InputTokens counts a cached read at CacheReadPrice and a cache write at CacheWritePrice of plain input,
    ///   never LlmResponse.Billed, which is Anthropic's (change 4);
    /// - thinking: Effort goes as reasoning_effort to a model in ReasoningModels; Thinking "disabled" sends the model's
    ///   value in ReasoningOff, or nothing where the model cannot turn it off (change 3);
    /// - a stream stopped by its caller, or one whose host sends no usage, is priced from estimates: the prompt at four
    ///   characters a token, never 0, and the reply the same way (change 1); IsEstimated says which replies were.
    public class OpenAiCompatibleClient : IStartingLlmClient, IDisposable
    {
        readonly HttpClient _http;
        readonly string _apiKey;
        /// The host's base, ending before "/chat/completions" (for example "https://api.groq.com/openai/v1").
        public readonly string BaseUrl;
        /// The provider's name, written beside every measured call ("openai", "groq", "openrouter", "gemini", "llamacpp").
        public string Provider = "openai";
        public int MaxRetries = 3;
        public Func<int, TimeSpan> RetryDelay = attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)); // 2s,4s,8s
        /// How a retry waits (the tests' seam: a Retry-After of seconds need not be slept through).
        public Func<TimeSpan, CancellationToken, Task> Wait = (d, ct) => Task.Delay(d, ct);
        public string SystemRole = "system";
        public string MaxTokensField = "max_completion_tokens";
        /// Ask for the usage chunk at the stream's end (stream_options.include_usage).
        public bool SendStreamOptions = true;
        /// Send cached heads as content blocks marked cache_control (OpenRouter to Anthropic only).
        public bool SendCacheBlocks;
        /// A cached read's and a cache write's price as a share of plain input, as the provider's pricing page gives it.
        public double CacheReadPrice = 0.5, CacheWritePrice = 1.0;
        /// Hosts that keep billing a request after the caller stops it (OpenRouter names Groq and Google): the
        /// two-copies race must be off there, or both copies counted (change 2): here a stopped stream on such a host is
        /// priced as if it had written its whole MaxTokens, so a race's losing copy is counted, never free.
        public bool BillsAfterCancel;
        /// The longest Retry-After waited; a longer one (a daily limit) fails at once instead of sleeping it out.
        public TimeSpan MaxRetryAfter = TimeSpan.FromSeconds(60);
        /// Models that take reasoning_effort, and each one's value for "thinking off" where it has one.
        public HashSet<string> ReasoningModels = new HashSet<string>();
        public Dictionary<string, string> ReasoningOff = new Dictionary<string, string>();
        /// Fields merged into every body: OpenRouter's provider block ({"data_collection":"deny","order":[...],
        /// "allow_fallbacks":false}, change 6), a host's own switches.
        public Dictionary<string, object> ExtraBody = new Dictionary<string, object>();

        static readonly ConditionalWeakTable<LlmResponse, object> Estimated = new ConditionalWeakTable<LlmResponse, object>();
        /// Whether a reply's token counts came from estimates rather than the service's usage.
        public static bool IsEstimated(LlmResponse r) => r != null && Estimated.TryGetValue(r, out _);
        static LlmResponse MarkEstimated(LlmResponse r) { Estimated.AddOrUpdate(r, true); return r; }

        string CompletionsUrl => BaseUrl.TrimEnd('/') + "/chat/completions";

        /// apiKey may be null or empty for a local server without one. handler is the tests' seam, as AnthropicClient's.
        public OpenAiCompatibleClient(string baseUrl, string apiKey, TimeSpan? timeout = null, HttpMessageHandler handler = null)
        {
            BaseUrl = baseUrl;
            _apiKey = apiKey;
            _http = handler != null ? new HttpClient(handler)
                : new HttpClient(new SocketsHttpHandler { PooledConnectionIdleTimeout = TimeSpan.FromMinutes(6) });
            _http.Timeout = timeout ?? TimeSpan.FromSeconds(60);
        }

        void Authorise(HttpRequestMessage msg)
        {
            if (!string.IsNullOrEmpty(_apiKey)) msg.Headers.TryAddWithoutValidation("Authorization", "Bearer " + _apiKey);
            msg.Version = System.Net.HttpVersion.Version20;
            msg.VersionPolicy = HttpVersionPolicy.RequestVersionOrLower;
        }

        HttpRequestMessage Message(string json)
        {
            var msg = new HttpRequestMessage(HttpMethod.Post, CompletionsUrl);
            Authorise(msg);
            msg.Content = new StringContent(json, Encoding.UTF8, "application/json");
            return msg;
        }

        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            var json = MiniJson.Serialize(Body(request, false));
            for (int attempt = 0; ; attempt++)
            {
                using var msg = Message(json);
                string text;
                int status;
                TimeSpan? retryAfter;
                try
                {
                    using var resp = await _http.SendAsync(msg, ct).ConfigureAwait(false);
                    status = (int)resp.StatusCode;
                    retryAfter = RetryAfter(resp);
                    text = await resp.Content.ReadAsStringAsync().ConfigureAwait(false);
                }
                catch (Exception ex) when (ex is HttpRequestException || (ex is TaskCanceledException && !ct.IsCancellationRequested))
                {
                    if (attempt >= MaxRetries) throw new HttpRequestException("the request to " + Provider + " failed: " + ex.Message);
                    await Wait(RetryDelay(attempt + 1), ct).ConfigureAwait(false);
                    continue;
                }
                if (status == 429 || status >= 500)
                {
                    var error = ApiError(status, text);
                    if (attempt >= MaxRetries || IsBilling(error) || retryAfter > MaxRetryAfter) throw error;
                    await Wait(retryAfter ?? RetryDelay(attempt + 1), ct).ConfigureAwait(false);
                    continue;
                }
                if (status >= 400) throw ApiError(status, text);
                var root = MiniJson.AsObject(MiniJson.Deserialize(text));
                var inChoice = ChoiceError(root);
                if (MiniJson.GetObject(root, "error") != null || inChoice != null)
                    throw ApiError(status, text);
                return ParseResponse(root, request);
            }
        }

        public Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default) =>
            StreamAsync(request, onText, null, ct);

        /// The reply as it is written: onStart once at the first answer text or reasoning delta, onText with the whole
        /// text so far each time it grows. A stream that will not start falls back to the plain call, as AnthropicClient's.
        /// A finished reply needs a finish_reason of stop or length and the closing [DONE]; anything else is broken
        /// (change 5).
        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, Action onStart, CancellationToken ct = default)
        {
            var msg = Message(MiniJson.Serialize(Body(request, true)));
            HttpResponseMessage resp = null;
            try { resp = await _http.SendAsync(msg, HttpCompletionOption.ResponseHeadersRead, ct).ConfigureAwait(false); }
            catch (Exception ex) when (ex is HttpRequestException || (ex is TaskCanceledException && !ct.IsCancellationRequested)) { resp = null; }
            catch (OperationCanceledException) when (ct.IsCancellationRequested)
            {
                // Stopped before the reply began: the prompt was sent, so it is counted (and the whole reply on a host
                // that bills after a cancel).
                throw new LlmStreamStoppedException(MarkEstimated(new LlmResponse
                    { InputTokens = PromptEstimate(request), OutputTokens = BillsAfterCancel ? request.MaxTokens : 0 }), ct);
            }
            finally { msg.Dispose(); }
            if (resp != null && (int)resp.StatusCode >= 400 && (int)resp.StatusCode < 500 && (int)resp.StatusCode != 429)
            {
                // A refusal the plain call would only repeat (a bad request, a bad key): not sent twice.
                string refused;
                using (resp) refused = await resp.Content.ReadAsStringAsync().ConfigureAwait(false);
                throw ApiError((int)resp.StatusCode, refused);
            }
            if (resp == null || (int)resp.StatusCode != 200)
            {
                resp?.Dispose();
                var whole = await CompleteAsync(request, ct).ConfigureAwait(false);
                onStart?.Invoke();
                onText?.Invoke(whole.Text);
                return whole;
            }
            using (resp)
            {
                var result = new LlmResponse();
                var sb = new StringBuilder();
                using var stream = await resp.Content.ReadAsStreamAsync().ConfigureAwait(false);
                // The reader before the stop: a token already cancelled closes the stream at once, and a reader cannot be
                // opened on a closed stream; its first read then reports the stop.
                using var reader = new System.IO.StreamReader(stream, Encoding.UTF8);
                using var stop = ct.Register(() => stream.Dispose());
                bool done = false, begun = false, usage = false;
                string finish = null, error = null;
                long thought = 0;
                int promptEstimate = PromptEstimate(request);
                LlmResponse SoFar() => MarkEstimated(new LlmResponse
                {
                    Model = result.Model,
                    InputTokens = usage ? result.InputTokens : promptEstimate,
                    OutputTokens = BillsAfterCancel ? Math.Max(request.MaxTokens, result.OutputTokens)
                                                    : (int)Math.Max(result.OutputTokens, (sb.Length + thought + 3) / 4),
                    Text = sb.ToString(),
                });
                void Begin()
                {
                    if (begun) return;
                    begun = true;
                    onStart?.Invoke();
                }
                while (error == null && !done)
                {
                    string line;
                    try { line = await reader.ReadLineAsync().ConfigureAwait(false); }
                    catch (Exception) when (ct.IsCancellationRequested) { throw new LlmStreamStoppedException(SoFar(), ct); }
                    catch (Exception ex) when (ex is System.IO.IOException || ex is HttpRequestException)
                    {
                        throw new LlmStreamBrokenException("the connection dropped mid-reply: " + ex.Message);
                    }
                    if (ct.IsCancellationRequested) throw new LlmStreamStoppedException(SoFar(), ct);
                    if (line == null) break;
                    if (!line.StartsWith("data:")) continue;
                    var data = line.Substring(5).Trim();
                    if (data.Length == 0) continue;
                    if (data == "[DONE]") { done = true; break; }
                    Dictionary<string, object> chunk;
                    try { chunk = MiniJson.AsObject(MiniJson.Deserialize(data)); } catch { continue; }
                    if (chunk == null) continue;
                    var top = MiniJson.GetObject(chunk, "error");
                    if (top != null) { error = ErrorText(top) ?? data; break; }
                    var model = MiniJson.GetString(chunk, "model");
                    if (!string.IsNullOrEmpty(model)) result.Model = model;
                    var choices = MiniJson.GetList(chunk, "choices");
                    var choice = choices != null && choices.Count > 0 ? MiniJson.AsObject(choices[0]) : null;
                    if (choice != null)
                    {
                        var inChoice = MiniJson.GetObject(choice, "error");
                        if (inChoice != null) { error = ErrorText(inChoice) ?? data; break; }
                        var delta = MiniJson.GetObject(choice, "delta");
                        var reasoning = MiniJson.GetString(delta, "reasoning") ?? MiniJson.GetString(delta, "reasoning_content");
                        if (!string.IsNullOrEmpty(reasoning)) { Begin(); thought += reasoning.Length; }
                        var content = MiniJson.GetString(delta, "content");
                        if (!string.IsNullOrEmpty(content))
                        {
                            Begin();
                            sb.Append(content);
                            onText?.Invoke(sb.ToString());
                        }
                        var reason = MiniJson.GetString(choice, "finish_reason");
                        if (!string.IsNullOrEmpty(reason)) finish = reason;
                        if (finish == "error") { error = "the host reported an error mid-reply"; break; }
                    }
                    var u = MiniJson.GetObject(chunk, "usage");
                    if (u != null) { ReadUsage(result, u, request); usage = true; }
                }
                if (error != null) throw new LlmStreamBrokenException(error);
                if (!done || (finish != "stop" && finish != "length"))
                    throw new LlmStreamBrokenException(!done ? "the reply's stream ended before it was finished"
                        : "the reply ended without finishing (" + (finish ?? "no finish reason") + ")");
                result.Text = sb.ToString();
                result.StopReason = StopReasonOf(finish);
                if (usage) CountCache(result);
                if (!usage)
                {
                    result.InputTokens = promptEstimate;
                    result.OutputTokens = (int)((sb.Length + thought + 3) / 4);
                    MarkEstimated(result);
                }
                return result;
            }
        }

        /// The callers read one stop reason, "max_tokens", for a cut reply (ClaimCheck); the rest pass as the host gave them.
        public static string StopReasonOf(string finish) =>
            finish == "length" ? "max_tokens" : finish == "stop" ? "end_turn" : finish ?? "";

        /// The prompt at four characters a token, the same rule the streams use for a reply without usage.
        public static int PromptEstimate(LlmRequest request)
        {
            long chars = (request.System ?? "").Length;
            foreach (var m in request.Messages) chars += (m.Content ?? "").Length;
            return (int)Math.Max(1, (chars + 3) / 4);
        }

        /// Input tokens as this provider bills them, in plain-input tokens.
        public int Priced(int uncached, int written, int read) =>
            uncached + (int)Math.Ceiling(written * CacheWritePrice) + (int)Math.Ceiling(read * CacheReadPrice);

        /// The usage as the host gave it; a usage chunk repeated (cumulative) replaces the last one read. A prompt
        /// reported as 0 tokens is priced from the estimate, never as free.
        void ReadUsage(LlmResponse r, Dictionary<string, object> usage, LlmRequest request)
        {
            var details = MiniJson.GetObject(usage, "prompt_tokens_details");
            r.CacheReadTokens = MiniJson.GetInt(details, "cached_tokens");
            r.CacheWriteTokens = MiniJson.GetInt(details, "cache_write_tokens");
            int prompt = MiniJson.GetInt(usage, "prompt_tokens");
            if (prompt <= 0) { prompt = PromptEstimate(request); MarkEstimated(r); }
            int uncached = Math.Max(0, prompt - r.CacheReadTokens - r.CacheWriteTokens);
            r.InputTokens = Priced(uncached, r.CacheWriteTokens, r.CacheReadTokens);
            r.OutputTokens = MiniJson.GetInt(usage, "completion_tokens");
        }

        /// The bench's end line reads the run's totals (AnthropicClient's counters, shared by every provider): once a reply.
        static void CountCache(LlmResponse r)
        {
            Interlocked.Add(ref AnthropicClient.CacheReadTotal, r.CacheReadTokens);
            Interlocked.Add(ref AnthropicClient.CacheWriteTotal, r.CacheWriteTokens);
        }

        LlmResponse ParseResponse(Dictionary<string, object> root, LlmRequest request)
        {
            var result = new LlmResponse { Model = MiniJson.GetString(root, "model") ?? "" };
            var choices = MiniJson.GetList(root, "choices");
            var choice = choices != null && choices.Count > 0 ? MiniJson.AsObject(choices[0]) : null;
            result.Text = MiniJson.GetString(MiniJson.GetObject(choice, "message"), "content") ?? "";
            result.StopReason = StopReasonOf(MiniJson.GetString(choice, "finish_reason"));
            var usage = MiniJson.GetObject(root, "usage");
            if (usage != null) { ReadUsage(result, usage, request); CountCache(result); }
            else
            {
                result.InputTokens = PromptEstimate(request);
                result.OutputTokens = (result.Text.Length + 3) / 4;
                MarkEstimated(result);
            }
            return result;
        }

        /// The Chat Completions body for a request.
        public Dictionary<string, object> Body(LlmRequest request, bool stream)
        {
            static Dictionary<string, object> Block(string text, bool cached)
            {
                var b = new Dictionary<string, object> { { "type", "text" }, { "text", text } };
                if (cached) b["cache_control"] = new Dictionary<string, object> { { "type", "ephemeral" } };
                return b;
            }
            object Content(string whole, string head)
            {
                if (!SendCacheBlocks || string.IsNullOrEmpty(head) || whole == null || !whole.StartsWith(head, StringComparison.Ordinal)) return whole;
                // No empty text block: Anthropic refuses one, so a head that is the whole text goes as one marked block.
                return head.Length == whole.Length ? new List<object> { Block(whole, true) }
                    : new List<object> { Block(head, true), Block(whole.Substring(head.Length), false) };
            }
            var messages = new List<object>();
            if (!string.IsNullOrEmpty(request.System))
            {
                var head = request.CachedSystemHead ?? (request.CacheSystem ? request.System : null);
                messages.Add(new Dictionary<string, object> { { "role", SystemRole }, { "content", Content(request.System, head) } });
            }
            foreach (var m in request.Messages)
                messages.Add(new Dictionary<string, object> { { "role", m.Role }, { "content", Content(m.Content, m.CachedHead) } });
            var body = new Dictionary<string, object>
            {
                { "model", request.Model },
                { "messages", messages },
                { MaxTokensField, request.MaxTokens },
            };
            if (stream)
            {
                body["stream"] = true;
                if (SendStreamOptions) body["stream_options"] = new Dictionary<string, object> { { "include_usage", true } };
            }
            var effort = ReasoningFor(request);
            if (effort != null) body["reasoning_effort"] = effort;
            foreach (var kv in ExtraBody) body[kv.Key] = kv.Value;
            return body;
        }

        /// The thinking table (change 3): the callers say "disabled" or "adaptive" and an effort, as for Anthropic.
        string ReasoningFor(LlmRequest request)
        {
            if (request.Thinking == "disabled")
                return ReasoningOff.TryGetValue(request.Model ?? "", out var off) ? off : null;
            if (!string.IsNullOrEmpty(request.Effort) && ReasoningModels.Contains(request.Model ?? ""))
                return request.Effort;
            return null;
        }

        static TimeSpan? RetryAfter(HttpResponseMessage resp)
        {
            var ra = resp.Headers.RetryAfter;
            if (ra == null) return null;
            if (ra.Delta.HasValue) return ra.Delta.Value;
            if (ra.Date.HasValue) { var d = ra.Date.Value - DateTimeOffset.UtcNow; return d > TimeSpan.Zero ? d : TimeSpan.Zero; }
            return null;
        }

        /// Billing refusals come as 429 too; asking again never helps them (change 5). Judged by the error's type and
        /// code only, never its message: a per-minute limit's message may speak of quota and billing (Gemini) and is
        /// retried; a daily limit is caught by its long Retry-After (MaxRetryAfter).
        static bool IsBilling(LlmApiException e)
        {
            var t = (e.ErrorType ?? "").ToLowerInvariant();
            return t.Contains("insufficient_quota") || t.Contains("billing") || t.Contains("insufficient_credits") || t.Contains("payment");
        }

        static string Field(Dictionary<string, object> obj, string key) =>
            obj != null && obj.TryGetValue(key, out var v) && v != null
                ? (v is double d ? d.ToString(System.Globalization.CultureInfo.InvariantCulture) : v as string ?? v.ToString())
                : null;

        static string ErrorText(Dictionary<string, object> error) => Field(error, "message");

        static Dictionary<string, object> ChoiceError(Dictionary<string, object> root)
        {
            var choices = MiniJson.GetList(root, "choices");
            return choices != null && choices.Count > 0 ? MiniJson.GetObject(MiniJson.AsObject(choices[0]), "error") : null;
        }

        /// The error with its type and code: {"error":{"message","type","code"}} (OpenAI; OpenRouter's code is a
        /// number and its error may sit inside a choice). The type carries the code after a colon when both exist.
        /// Built from the body alone, so no key can reach a message.
        LlmApiException ApiError(int status, string body)
        {
            string message = body, type = null;
            try
            {
                var root = MiniJson.AsObject(MiniJson.Deserialize(body));
                var error = MiniJson.GetObject(root, "error") ?? ChoiceError(root);
                if (error != null)
                {
                    message = ErrorText(error) ?? body;
                    var t = Field(error, "type");
                    var c = Field(error, "code");
                    type = t != null && c != null ? t + ":" + c : t ?? c;
                }
            }
            catch { }
            // A key echoed back by a host never reaches a message; an unreadable body is cut short.
            if (!string.IsNullOrEmpty(_apiKey) && message != null) message = message.Replace(_apiKey, "[key]");
            if (message != null && message.Length > 300) message = message.Substring(0, 300) + "...";
            return new LlmApiException(status, message, type);
        }

        public void Dispose() => _http.Dispose();
    }
}
