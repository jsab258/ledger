using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Ledger.DevTools;

namespace Ledger.CoreTests
{
    /// THE SECOND PROVIDER'S CLIENT (his order of 16 November 2026, n16-6): the ten acceptance cases of
    /// production/research/talk-providers/METHOD-NOTE-2026-11-16.md with its review's changes, on a fake HTTP handler.
    static partial class Program
    {
        /// A handler that answers by a function of the request's body, and keeps every body and Authorization header.
        class BodyHandler : HttpMessageHandler
        {
            readonly Func<string, int, HttpResponseMessage> _answer;
            public readonly List<string> Bodies = new List<string>();
            public readonly List<string> Auth = new List<string>();
            public BodyHandler(Func<string, int, HttpResponseMessage> answer) => _answer = answer;
            protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
            {
                var body = request.Content == null ? "" : await request.Content.ReadAsStringAsync().ConfigureAwait(false);
                int n;
                lock (Bodies)
                {
                    Bodies.Add(body);
                    Auth.Add(request.Headers.TryGetValues("Authorization", out var v) ? string.Join(",", v) : null);
                    n = Bodies.Count;
                }
                var resp = _answer(body, n);
                if (resp == null) throw new HttpRequestException("simulated network drop");
                return resp;
            }
        }

        /// A body that gives its text, then waits until it is closed (a caller's stop).
        class HangingStream : System.IO.Stream
        {
            readonly byte[] _first;
            bool _gave;
            readonly TaskCompletionSource<int> _closed = new TaskCompletionSource<int>(TaskCreationOptions.RunContinuationsAsynchronously);
            public HangingStream(string text) => _first = Encoding.UTF8.GetBytes(text);
            public override int Read(byte[] buffer, int offset, int count) => ReadAsync(buffer, offset, count, default).GetAwaiter().GetResult();
            public override async Task<int> ReadAsync(byte[] buffer, int offset, int count, CancellationToken ct)
            {
                if (!_gave) { _gave = true; Array.Copy(_first, 0, buffer, offset, _first.Length); return _first.Length; }
                await _closed.Task.ConfigureAwait(false);
                throw new ObjectDisposedException("stream");
            }
            public override ValueTask<int> ReadAsync(Memory<byte> buffer, CancellationToken ct = default)
            {
                if (!_gave) { _gave = true; _first.CopyTo(buffer); return new ValueTask<int>(_first.Length); }
                return new ValueTask<int>(_closed.Task.ContinueWith<int>(_ => throw new ObjectDisposedException("stream")));
            }
            protected override void Dispose(bool disposing) { _closed.TrySetResult(0); base.Dispose(disposing); }
            public override bool CanRead => true; public override bool CanSeek => false; public override bool CanWrite => false;
            public override long Length => throw new NotSupportedException();
            public override long Position { get => 0; set => throw new NotSupportedException(); }
            public override void Flush() { }
            public override long Seek(long o, System.IO.SeekOrigin s) => throw new NotSupportedException();
            public override void SetLength(long v) => throw new NotSupportedException();
            public override void Write(byte[] b, int o, int c) => throw new NotSupportedException();
        }

        static string Sse(params string[] chunks) => string.Concat(chunks.Select(c => "data: " + c + "\n\n"));
        static string Delta(string text) => "{\"id\":\"c1\",\"object\":\"chat.completion.chunk\",\"model\":\"m-1\",\"choices\":[{\"index\":0,\"delta\":{\"content\":" + MiniJson.Serialize(text) + "},\"finish_reason\":null}]}";
        static string Finish(string reason) => "{\"id\":\"c1\",\"model\":\"m-1\",\"choices\":[{\"index\":0,\"delta\":{},\"finish_reason\":\"" + reason + "\"}]}";
        static string UsageChunk(int prompt, int completion, int cached = 0) =>
            "{\"id\":\"c1\",\"model\":\"m-1\",\"choices\":[],\"usage\":{\"prompt_tokens\":" + prompt + ",\"completion_tokens\":" + completion
            + ",\"prompt_tokens_details\":{\"cached_tokens\":" + cached + "}}}";
        static HttpResponseMessage SseResponse(string text) => new HttpResponseMessage(HttpStatusCode.OK) { Content = new StringContent(text) };
        const string ProviderOk = "{\"id\":\"x\",\"model\":\"m-1\",\"choices\":[{\"index\":0,\"message\":{\"role\":\"assistant\",\"content\":\"Hm. Is that so.\"},\"finish_reason\":\"stop\"}],\"usage\":{\"prompt_tokens\":1000,\"completion_tokens\":7,\"prompt_tokens_details\":{\"cached_tokens\":800}}}";
        const string ProviderKey = "sk-test-SECRET-4242";

        static OpenAiCompatibleClient Provider(HttpMessageHandler h)
        {
            var c = new OpenAiCompatibleClient("https://host.test/v1", ProviderKey, handler: h);
            c.RetryDelay = _ => TimeSpan.Zero;
            return c;
        }

        static LlmRequest ProviderRequest() => new LlmRequest
        {
            Model = "m-1", System = "You are Lena.", MaxTokens = 300,
            Messages = { new LlmMessage("user", "Evening.") },
        };

        static async Task TestProviderClient()
        {
            Console.WriteLine("OpenAI-style provider client (bench only):");

            // 1. Plain call: the body, the reply, the stop reason, billed tokens.
            var h1 = new BodyHandler((b, n) => Http(HttpStatusCode.OK, ProviderOk));
            var c1 = Provider(h1);
            var r1 = await c1.CompleteAsync(ProviderRequest());
            var b1 = MiniJson.AsObject(MiniJson.Deserialize(h1.Bodies[0]));
            var msgs1 = MiniJson.GetList(b1, "messages");
            var first1 = MiniJson.AsObject(msgs1[0]);
            Check(MiniJson.GetString(first1, "role") == "system" && MiniJson.GetString(first1, "content") == "You are Lena.", "the system text is the first message");
            Check(MiniJson.GetString(b1, "model") == "m-1" && MiniJson.GetInt(b1, "max_completion_tokens") == 300 && !b1.ContainsKey("max_tokens"), "model and the length field as set");
            Check(!b1.ContainsKey("stream") && !b1.ContainsKey("system") && !b1.ContainsKey("thinking"), "no stream and no Anthropic-only fields on a plain call");
            Check(h1.Auth[0] == "Bearer " + ProviderKey, "the key goes as a Bearer header");
            Check(r1.Text == "Hm. Is that so." && r1.StopReason == "end_turn" && r1.Model == "m-1" && r1.OutputTokens == 7, "reply, stop reason and model read");
            c1.MaxTokensField = "max_tokens";
            await c1.CompleteAsync(ProviderRequest());
            Check(MiniJson.GetInt(MiniJson.AsObject(MiniJson.Deserialize(h1.Bodies[1])), "max_tokens") == 300, "a host's own length field (max_tokens)");

            // 2. Stream: deltas, a finish chunk, a usage-only chunk, [DONE].
            var h2 = new BodyHandler((b, n) => SseResponse(Sse(Delta("Hm."), Delta(" Is that"), Delta(" so."), Finish("stop"), UsageChunk(120, 5), "[DONE]")));
            int starts = 0;
            var grew = new List<string>();
            var r2 = await Provider(h2).StreamAsync(ProviderRequest(), t => grew.Add(t), () => { starts++; if (grew.Count > 0) starts += 100; });
            var b2 = MiniJson.AsObject(MiniJson.Deserialize(h2.Bodies[0]));
            Check(b2.ContainsKey("stream") && MiniJson.GetObject(b2, "stream_options") != null, "the stream asks for its usage chunk");
            Check(grew.Count == 3 && grew[2] == "Hm. Is that so." && grew[0] == "Hm.", "onText hears the whole text so far as it grows");
            Check(starts == 1, "onStart once, before the first text");
            Check(r2.InputTokens == 120 && r2.OutputTokens == 5 && !OpenAiCompatibleClient.IsEstimated(r2) && r2.StopReason == "end_turn", "usage read from the last chunk");

            // 3. No usage chunk: estimates, marked as such; the prompt never priced at 0.
            var h3 = new BodyHandler((b, n) => SseResponse(Sse(Delta("Twelve chars"), Finish("length"), "[DONE]")));
            var r3 = await Provider(h3).StreamAsync(ProviderRequest(), null);
            Check(OpenAiCompatibleClient.IsEstimated(r3) && r3.InputTokens == OpenAiCompatibleClient.PromptEstimate(ProviderRequest()) && r3.InputTokens > 0
                  && r3.OutputTokens == 3 && r3.StopReason == "max_tokens", "no usage: prompt and reply estimated, marked, length mapped to max_tokens");

            // 4. Cached tokens: 800 of 1,000 read from the cache, priced by the provider's own ratio.
            var c4 = Provider(new BodyHandler((b, n) => Http(HttpStatusCode.OK, ProviderOk)));
            c4.CacheReadPrice = 0.5;
            var r4 = await c4.CompleteAsync(ProviderRequest());
            Check(r4.CacheReadTokens == 800 && r4.InputTokens == 200 + 400, "800 cached of 1,000 at half price: 600 billed");
            c4.CacheReadPrice = 0.1;
            Check((await c4.CompleteAsync(ProviderRequest())).InputTokens == 280, "the same at a tenth: 280 billed (not Anthropic's Billed)");

            // 5. OpenRouter's final chunk: a non-empty choice with the finish and the usage together.
            var orFinal = "{\"id\":\"c1\",\"model\":\"vendor/m-1\",\"choices\":[{\"index\":0,\"delta\":{\"content\":\"\"},\"finish_reason\":\"stop\"}],\"usage\":{\"prompt_tokens\":50,\"completion_tokens\":2}}";
            var r5 = await Provider(new BodyHandler((b, n) => SseResponse(Sse(Delta("Aye."), orFinal, "[DONE]")))).StreamAsync(ProviderRequest(), null);
            Check(r5.Text == "Aye." && r5.InputTokens == 50 && r5.OutputTokens == 2 && r5.Model == "vendor/m-1", "OpenRouter's final chunk parses the same, the answering model kept");

            // 6. Retries: Retry-After honoured; repeated 429 keeps type and code; billing 429 and 400 not retried;
            //    a stream that will not start falls back to the plain call.
            var delays = new List<TimeSpan>();
            var h6 = new BodyHandler((b, n) =>
            {
                if (n == 1) { var r = Http((HttpStatusCode)429, "{\"error\":{\"message\":\"slow\",\"type\":\"rate_limit_error\",\"code\":\"slow_down\"}}"); r.Headers.RetryAfter = new System.Net.Http.Headers.RetryConditionHeaderValue(TimeSpan.FromSeconds(7)); return r; }
                return Http(HttpStatusCode.OK, ProviderOk);
            });
            var c6 = Provider(h6);
            c6.Wait = (d, ct) => { delays.Add(d); return Task.CompletedTask; };
            var r6 = await c6.CompleteAsync(ProviderRequest());
            Check(r6.Text == "Hm. Is that so." && h6.Bodies.Count == 2 && delays.Count == 1 && delays[0] == TimeSpan.FromSeconds(7), "429 with Retry-After: waits the given 7 s, then succeeds");
            var h6b = new BodyHandler((b, n) => Http((HttpStatusCode)429, "{\"error\":{\"message\":\"slow\",\"type\":\"rate_limit_error\",\"code\":\"slow_down\"}}"));
            var c6b = Provider(h6b); c6b.MaxRetries = 2;
            LlmApiException e6b = null;
            try { await c6b.CompleteAsync(ProviderRequest()); } catch (LlmApiException e) { e6b = e; }
            Check(e6b != null && e6b.StatusCode == 429 && e6b.ErrorType == "rate_limit_error:slow_down" && h6b.Bodies.Count == 3, "repeated 429: retries spent, type and code kept");
            var h6c = new BodyHandler((b, n) => Http((HttpStatusCode)429, "{\"error\":{\"message\":\"You exceeded your current quota\",\"type\":\"insufficient_quota\",\"code\":\"insufficient_quota\"}}"));
            try { await Provider(h6c).CompleteAsync(ProviderRequest()); } catch (LlmApiException) { }
            Check(h6c.Bodies.Count == 1, "a billing 429 is never retried");
            var h6d = new BodyHandler((b, n) => Http(HttpStatusCode.BadRequest, "{\"error\":{\"message\":\"bad\",\"code\":400}}"));
            LlmApiException e6d = null;
            try { await Provider(h6d).CompleteAsync(ProviderRequest()); } catch (LlmApiException e) { e6d = e; }
            Check(e6d != null && h6d.Bodies.Count == 1 && e6d.ErrorType == "400", "400 not retried; a numeric code (OpenRouter) read");
            var h6e = new BodyHandler((b, n) => b.Contains("\"stream\":true") ? Http(HttpStatusCode.ServiceUnavailable, "{}") : Http(HttpStatusCode.OK, ProviderOk));
            int starts6 = 0; string heard6 = null;
            var r6e = await Provider(h6e).StreamAsync(ProviderRequest(), t => heard6 = t, () => starts6++);
            Check(r6e.Text == "Hm. Is that so." && heard6 == r6e.Text && starts6 == 1, "a stream that will not start falls back to the plain call");

            // 7. Broken and stopped streams.
            async Task<bool> Broken(string sse)
            {
                try { await Provider(new BodyHandler((b, n) => SseResponse(sse))).StreamAsync(ProviderRequest(), null); return false; }
                catch (LlmStreamBrokenException) { return true; }
            }
            Check(await Broken(Sse(Delta("Hm"), "{\"error\":{\"message\":\"overloaded\",\"code\":502}}")), "an error chunk mid-stream is a broken stream");
            Check(await Broken(Sse(Delta("Hm"), Finish("error"), "[DONE]")), "finish_reason error inside a 200 stream is broken");
            Check(await Broken(Sse(Delta("Hm"), Finish("stop"))), "an end before [DONE] is broken");
            Check(await Broken(Sse(Delta("Hm"), "[DONE]")), "[DONE] without stop or length is not a finished reply");
            Check(await Broken(Sse(Delta("Hm"), Finish("content_filter"), "[DONE]")), "a filtered reply is not passed off as whole");
            var cts7 = new CancellationTokenSource();
            var h7 = new BodyHandler((b, n) => new HttpResponseMessage(HttpStatusCode.OK) { Content = new StreamContent(new HangingStream(Sse(Delta("Twelve chars")))) });
            LlmStreamStoppedException stopped7 = null;
            try { await Provider(h7).StreamAsync(ProviderRequest(), t => { if (t.Length > 0) cts7.Cancel(); }, cts7.Token); }
            catch (LlmStreamStoppedException e) { stopped7 = e; }
            catch (OperationCanceledException) { }
            Check(stopped7 != null && stopped7.SoFar.Text == "Twelve chars" && stopped7.SoFar.InputTokens == OpenAiCompatibleClient.PromptEstimate(ProviderRequest())
                  && stopped7.SoFar.InputTokens > 0 && stopped7.SoFar.OutputTokens == 3 && OpenAiCompatibleClient.IsEstimated(stopped7.SoFar),
                  "a caller's stop carries what it used: the prompt estimated, never 0");

            // Thinking table and the extra body (changes 3 and 6).
            var hT = new BodyHandler((b, n) => Http(HttpStatusCode.OK, ProviderOk));
            var cT = Provider(hT);
            cT.ReasoningModels.Add("m-1");
            cT.ReasoningOff["m-1"] = "none";
            cT.ExtraBody["provider"] = new Dictionary<string, object> { { "data_collection", "deny" }, { "allow_fallbacks", false } };
            var off = ProviderRequest(); off.Thinking = "disabled";
            var low = ProviderRequest(); low.Effort = "low";
            var other = ProviderRequest(); other.Model = "m-2"; other.Thinking = "disabled"; other.Effort = "low";
            await cT.CompleteAsync(off); await cT.CompleteAsync(low); await cT.CompleteAsync(other);
            var bT = hT.Bodies.Select(x => MiniJson.AsObject(MiniJson.Deserialize(x))).ToList();
            Check(MiniJson.GetString(bT[0], "reasoning_effort") == "none" && MiniJson.GetString(bT[1], "reasoning_effort") == "low" && !bT[2].ContainsKey("reasoning_effort"),
                  "thinking off and effort mapped per model; nothing sent to a model without the setting");
            Check(MiniJson.GetString(MiniJson.GetObject(bT[0], "provider"), "data_collection") == "deny", "OpenRouter's data collection deny goes in every body");
            var cached = ProviderRequest(); cached.CachedSystemHead = "You are"; cached.Messages[0] = new LlmMessage("user", "Even", "ing.");
            await cT.CompleteAsync(cached);
            Check(hT.Bodies[3].Contains("\"content\":\"You are Lena.\"") && !hT.Bodies[3].Contains("cache_control"), "cached heads go as whole text, head first, for the host's prefix cache");
            cT.SendCacheBlocks = true;
            await cT.CompleteAsync(cached);
            Check(hT.Bodies[4].Contains("cache_control") && hT.Bodies[4].Contains("\"text\":\"You are\""), "OpenRouter to Anthropic: cached heads as marked blocks when asked");

            // The review's fixes (CLIENT-REVIEW-2026-11-16.md).
            var cW = Provider(new BodyHandler((b, n) => Http(HttpStatusCode.OK,
                "{\"model\":\"m-1\",\"choices\":[{\"message\":{\"content\":\"x\"},\"finish_reason\":\"stop\"}],\"usage\":{\"prompt_tokens\":1000,\"completion_tokens\":1,\"prompt_tokens_details\":{\"cached_tokens\":0,\"cache_write_tokens\":400}}}")));
            cW.CacheWritePrice = 1.25;
            var rW = await cW.CompleteAsync(ProviderRequest());
            Check(rW.CacheWriteTokens == 400 && rW.InputTokens == 600 + 500, "a cache write priced at the provider's own ratio");
            var rZ = await Provider(new BodyHandler((b, n) => Http(HttpStatusCode.OK,
                "{\"model\":\"m-1\",\"choices\":[{\"message\":{\"content\":\"x\"},\"finish_reason\":\"stop\"}],\"usage\":{\"prompt_tokens\":0,\"completion_tokens\":1}}"))).CompleteAsync(ProviderRequest());
            Check(rZ.InputTokens == OpenAiCompatibleClient.PromptEstimate(ProviderRequest()) && OpenAiCompatibleClient.IsEstimated(rZ), "a prompt reported as 0 tokens is estimated, never free");
            var hG = new BodyHandler((b, n) => n == 1
                ? Http((HttpStatusCode)429, "{\"error\":{\"code\":429,\"message\":\"You exceeded your current quota, please check your plan and billing details.\",\"status\":\"RESOURCE_EXHAUSTED\"}}")
                : Http(HttpStatusCode.OK, ProviderOk));
            var cG = Provider(hG); cG.Wait = (d, ct) => Task.CompletedTask;
            Check((await cG.CompleteAsync(ProviderRequest())).Text == "Hm. Is that so." && hG.Bodies.Count == 2, "a per-minute limit speaking of quota and billing is still retried");
            var hD = new BodyHandler((b, n) => { var r = Http((HttpStatusCode)429, "{\"error\":{\"message\":\"daily limit\",\"type\":\"tokens\"}}"); r.Headers.RetryAfter = new System.Net.Http.Headers.RetryConditionHeaderValue(TimeSpan.FromHours(3)); return r; });
            var waitsD = new List<TimeSpan>();
            var cD = Provider(hD); cD.Wait = (d, ct) => { waitsD.Add(d); return Task.CompletedTask; };
            try { await cD.CompleteAsync(ProviderRequest()); } catch (LlmApiException) { }
            Check(hD.Bodies.Count == 1 && waitsD.Count == 0, "a Retry-After of hours is not slept out: it fails at once");
            var h401 = new BodyHandler((b, n) => Http(HttpStatusCode.Unauthorized, "{\"error\":{\"message\":\"bad key " + ProviderKey + "\",\"type\":\"invalid_request_error\"}}"));
            LlmApiException e401 = null;
            try { await Provider(h401).StreamAsync(ProviderRequest(), null); } catch (LlmApiException e) { e401 = e; }
            Check(e401 != null && e401.StatusCode == 401 && h401.Bodies.Count == 1, "a refused stream start (401) is not sent again as a plain call");
            Check(!e401.Message.Contains(ProviderKey) && e401.Message.Contains("[key]"), "a key echoed back by the host is struck from the message");
            var hC = new BodyHandler((b, n) => Http(HttpStatusCode.OK, ProviderOk));
            var cC = Provider(hC); cC.SendCacheBlocks = true;
            var whole = ProviderRequest(); whole.CacheSystem = true;
            await cC.CompleteAsync(whole);
            Check(hC.Bodies[0].Contains("cache_control") && !hC.Bodies[0].Contains("\"text\":\"\""), "a head that is the whole text goes as one marked block, never an empty one");
            var ctsB = new CancellationTokenSource(); ctsB.Cancel();
            LlmStreamStoppedException early = null;
            try { await Provider(new BodyHandler((b, n) => Http(HttpStatusCode.OK, ProviderOk))).StreamAsync(ProviderRequest(), null, ctsB.Token); }
            catch (LlmStreamStoppedException e) { early = e; }
            catch (OperationCanceledException) { }
            Check(early != null && early.SoFar.InputTokens > 0, "stopped before the reply began: the prompt still counted");
            var ctsA = new CancellationTokenSource();
            var cA = Provider(new BodyHandler((b, n) => new HttpResponseMessage(HttpStatusCode.OK) { Content = new StreamContent(new HangingStream(Sse(Delta("Twelve chars")))) }));
            cA.BillsAfterCancel = true;
            LlmStreamStoppedException stoppedA = null;
            try { await cA.StreamAsync(ProviderRequest(), t => ctsA.Cancel(), ctsA.Token); }
            catch (LlmStreamStoppedException e) { stoppedA = e; }
            catch (OperationCanceledException) { }
            Check(stoppedA != null && stoppedA.SoFar.OutputTokens == 300, "a host that bills after a cancel: the stopped copy counted at its whole length");

            // 8. End to end: through BudgetedClient and ConversationEngine.
            var h8 = new BodyHandler((b, n) => b.Contains("\"stream\":true")
                ? SseResponse(Sse(Delta("Hm. Is that so."), Finish("stop"), UsageChunk(900, 6), "[DONE]"))
                : Http(HttpStatusCode.OK, ProviderOk));
            var budget = new BudgetedClient(Provider(h8), 1.0);
            var engine = new ConversationEngine(budget, MakeLenaCard(), new MemoryStore("lena"), new KnowledgeBase(), new SuspicionTracker(), new CostTracker());
            var said = await engine.SayToAsync("Evening, Lena.", new GameTime(1, 18, 0));
            Check(said != null && said.Contains("Is that so") && h8.Bodies.Count >= 1 && h8.Bodies.All(x => x.Contains("\"model\"")), "one turn passes end to end through the budget and the engine");

            // 9. Regression: AnthropicClient's body for a fixed request, byte-identical to the golden taken before the change.
            var golden = new LlmRequest { Model = "claude-haiku-5-5", System = "You are Lena. Stay in 1990.", CachedSystemHead = "You are Lena.", MaxTokens = 200, Thinking = "disabled", Effort = "low",
                                          Messages = { new LlmMessage("user", "Facts: none. ", "Evening."), new LlmMessage("assistant", "Evening.") } };
            var anthropicBody = MiniJson.Serialize(new AnthropicClient("k").Body(golden, true));
            Check(anthropicBody == AnthropicBodyGolden, "AnthropicClient's body unchanged (golden of 16 Nov)", anthropicBody);

            // 10. No key in any failure message.
            var leaks = new List<string>();
            foreach (var h in new HttpMessageHandler[] { h6b, h6c, h6d })
                try { await Provider(h).CompleteAsync(ProviderRequest()); } catch (Exception e) { leaks.Add(e.ToString()); }
            try { await Provider(new BodyHandler((b, n) => null)).CompleteAsync(ProviderRequest()); } catch (Exception e) { leaks.Add(e.ToString()); }
            try { await Provider(new BodyHandler((b, n) => SseResponse(Sse(Delta("x"))))).StreamAsync(ProviderRequest(), null); } catch (Exception e) { leaks.Add(e.ToString()); }
            Check(leaks.Count == 5 && leaks.All(l => !l.Contains(ProviderKey) && !l.Contains("SECRET")), "no key in any failure message");
        }

        const string AnthropicBodyGolden =
            @"{""model"":""claude-haiku-5-5"",""max_tokens"":200,""messages"":[{""role"":""user"",""content"":[{""type"":""text"",""text"":""Facts: none. "",""cache_control"":{""type"":""ephemeral""}},{""type"":""text"",""text"":""Evening.""}]},{""role"":""assistant"",""content"":""Evening.""}],""stream"":true,""system"":[{""type"":""text"",""text"":""You are Lena."",""cache_control"":{""type"":""ephemeral""}},{""type"":""text"",""text"":"" Stay in 1990.""}],""thinking"":{""type"":""disabled""},""output_config"":{""effort"":""low""}}";
    }
}
