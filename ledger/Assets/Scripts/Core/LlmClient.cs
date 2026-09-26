using System;
using System.Collections.Generic;
using System.Net.Http;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace Ledger.Core
{
    public class LlmMessage
    {
        public string Role;
        public string Content;
        public LlmMessage(string role, string content) { Role = role; Content = content; }
    }

    public class LlmRequest
    {
        public string Model;
        public string System;
        public List<LlmMessage> Messages = new List<LlmMessage>();
        public int MaxTokens = 1024;
    }

    public class LlmResponse
    {
        public string Text = "";
        public string StopReason = "";
        public int InputTokens;
        public int OutputTokens;
        public string Model = "";
    }

    public interface ILlmClient
    {
        Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default);
    }

    /// A CLIENT THAT HANDS OVER THE REPLY AS IT IS WRITTEN, 26 September
    /// (Jafar: about six seconds pass between his line and the character
    /// speaking). The same request and the same answer as CompleteAsync, and
    /// onText hears the whole text so far each time it grows, so the voice can
    /// start on the first sentence while the rest is still being written.
    public interface IStreamingLlmClient : ILlmClient
    {
        Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default);
    }

    /// Model tiering per design doc: cheap/fast for the ambient population,
    /// stronger for the authored core cast. Cost table used by CostTracker
    /// (USD per million tokens; sonnet uses post-intro sticker prices so
    /// estimates stay conservative).
    public static class Models
    {
        public const string Core = "claude-sonnet-5";
        public const string Ambient = "claude-haiku-4-5";

        public static readonly Dictionary<string, (double inPerM, double outPerM)> Cost =
            new Dictionary<string, (double, double)>
            {
                { Core, (3.0, 15.0) },
                { Ambient, (1.0, 5.0) },
            };
    }

    /// Raw-HTTP Anthropic Messages API client. Dependency-free by design so the
    /// identical code runs under Unity (Mono/IL2CPP) and plain .NET; the official
    /// C# SDK is not validated for Unity runtimes. Wire format per Anthropic docs.
    public class AnthropicClient : IStreamingLlmClient, IDisposable
    {
        readonly HttpClient _http;
        readonly string _apiKey;
        public int MaxRetries = 3;
        public Func<int, TimeSpan> RetryDelay = attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt)); // 2s,4s,8s

        public AnthropicClient(string apiKey, TimeSpan? timeout = null, HttpMessageHandler handler = null)
        {
            _apiKey = apiKey;
            // handler is a test seam: pass a fake to exercise the retry/error paths
            // deterministically. In production it is null and HttpClient uses its default.
            _http = handler != null ? new HttpClient(handler) : new HttpClient();
            _http.Timeout = timeout ?? TimeSpan.FromSeconds(60);
        }

        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            var messages = new List<object>();
            foreach (var m in request.Messages)
                messages.Add(new Dictionary<string, object> { { "role", m.Role }, { "content", m.Content } });

            var body = new Dictionary<string, object>
            {
                { "model", request.Model },
                { "max_tokens", request.MaxTokens },
                { "messages", messages },
            };
            if (!string.IsNullOrEmpty(request.System)) body["system"] = request.System;

            var json = MiniJson.Serialize(body);

            for (int attempt = 0; ; attempt++)
            {
                using var msg = new HttpRequestMessage(HttpMethod.Post, "https://api.anthropic.com/v1/messages");
                msg.Headers.Add("x-api-key", _apiKey);
                msg.Headers.Add("anthropic-version", "2023-06-01");
                msg.Content = new StringContent(json, Encoding.UTF8, "application/json");

                string text;
                int status;
                try
                {
                    // Send AND read-body are both inside the try: a network drop mid-body
                    // is a retryable HttpRequestException, and the using-scope disposes the
                    // response on every path (previously a mid-body failure leaked it).
                    using var resp = await _http.SendAsync(msg, ct).ConfigureAwait(false);
                    status = (int)resp.StatusCode;
                    text = await resp.Content.ReadAsStringAsync().ConfigureAwait(false);
                }
                catch (Exception ex) when (ex is HttpRequestException ||
                                           (ex is TaskCanceledException && !ct.IsCancellationRequested))
                {
                    // TaskCanceledException with the token NOT cancelled == HttpClient
                    // timeout (retryable); with it cancelled it falls through and throws.
                    if (attempt >= MaxRetries) throw;
                    await Task.Delay(RetryDelay(attempt + 1), ct).ConfigureAwait(false);
                    continue;
                }

                if (status == 429 || status >= 500)
                {
                    if (attempt >= MaxRetries)
                        throw new LlmApiException(status, ExtractErrorMessage(text));
                    await Task.Delay(RetryDelay(attempt + 1), ct).ConfigureAwait(false);
                    continue;
                }
                if (status >= 400)
                    throw new LlmApiException(status, ExtractErrorMessage(text));

                return ParseResponse(text);
            }
        }

        /// THE REPLY AS IT IS WRITTEN (IStreamingLlmClient): the Messages API with
        /// "stream": true, read event by event. A stream that will not start,
        /// or answers with an error status, falls back to the plain call and
        /// its retries, and hands the whole text over once.
        public async Task<LlmResponse> StreamAsync(LlmRequest request, Action<string> onText, CancellationToken ct = default)
        {
            var messages = new List<object>();
            foreach (var m in request.Messages)
                messages.Add(new Dictionary<string, object> { { "role", m.Role }, { "content", m.Content } });
            var body = new Dictionary<string, object>
            {
                { "model", request.Model },
                { "max_tokens", request.MaxTokens },
                { "messages", messages },
                { "stream", true },
            };
            if (!string.IsNullOrEmpty(request.System)) body["system"] = request.System;
            var msg = new HttpRequestMessage(HttpMethod.Post, "https://api.anthropic.com/v1/messages");
            msg.Headers.Add("x-api-key", _apiKey);
            msg.Headers.Add("anthropic-version", "2023-06-01");
            msg.Content = new StringContent(MiniJson.Serialize(body), Encoding.UTF8, "application/json");
            HttpResponseMessage resp = null;
            try
            {
                resp = await _http.SendAsync(msg, HttpCompletionOption.ResponseHeadersRead, ct).ConfigureAwait(false);
            }
            catch (Exception ex) when (ex is HttpRequestException || (ex is TaskCanceledException && !ct.IsCancellationRequested))
            {
                resp = null;
            }
            finally { msg.Dispose(); }
            if (resp == null || (int)resp.StatusCode != 200)
            {
                resp?.Dispose();
                var whole = await CompleteAsync(request, ct).ConfigureAwait(false);
                onText?.Invoke(whole.Text);
                return whole;
            }
            using (resp)
            {
                var result = new LlmResponse();
                var sb = new StringBuilder();
                using var stream = await resp.Content.ReadAsStreamAsync().ConfigureAwait(false);
                // A read waiting on the network hears cancellation by its stream closing.
                using var stop = ct.Register(() => stream.Dispose());
                using var reader = new System.IO.StreamReader(stream, Encoding.UTF8);
                string line;
                bool stopped = false;
                string error = null;
                while (error == null)
                {
                    try { line = await reader.ReadLineAsync().ConfigureAwait(false); }
                    catch (Exception) when (ct.IsCancellationRequested) { throw new OperationCanceledException(ct); }
                    // A connection dropped mid-reply is a broken stream, which the
                    // caller may ask again for, as the plain call retries a drop.
                    catch (Exception ex) when (ex is System.IO.IOException || ex is HttpRequestException)
                    {
                        throw new LlmStreamBrokenException("the connection dropped mid-reply: " + ex.Message);
                    }
                    ct.ThrowIfCancellationRequested();
                    if (line == null) break;
                    if (!line.StartsWith("data:")) continue;
                    var data = line.Substring(5).Trim();
                    if (data.Length == 0 || data == "[DONE]") continue;
                    Dictionary<string, object> ev;
                    try { ev = MiniJson.AsObject(MiniJson.Deserialize(data)); } catch { continue; }
                    if (ev == null) continue;
                    switch (MiniJson.GetString(ev, "type"))
                    {
                        case "message_start":
                            var start = MiniJson.GetObject(ev, "message");
                            result.Model = MiniJson.GetString(start, "model") ?? "";
                            result.InputTokens = MiniJson.GetInt(MiniJson.GetObject(start, "usage"), "input_tokens");
                            break;
                        case "content_block_delta":
                            var delta = MiniJson.GetObject(ev, "delta");
                            if (MiniJson.GetString(delta, "type") == "text_delta")
                            {
                                sb.Append(MiniJson.GetString(delta, "text"));
                                onText?.Invoke(sb.ToString());
                            }
                            break;
                        case "message_delta":
                            result.StopReason = MiniJson.GetString(MiniJson.GetObject(ev, "delta"), "stop_reason") ?? result.StopReason;
                            result.OutputTokens = MiniJson.GetInt(MiniJson.GetObject(ev, "usage"), "output_tokens");
                            break;
                        case "message_stop":
                            stopped = true;
                            break;
                        case "error":
                            error = MiniJson.GetString(MiniJson.GetObject(ev, "error"), "message") ?? data;
                            break;
                    }
                }
                // AN ERROR, OR A STREAM THAT ENDS UNFINISHED (the independent check,
                // 26 September): never passed off as the whole reply. The caller
                // decides whether to ask again (ConversationEngine does, with the
                // plain call, when nothing of it has been heard), so one failure is
                // not retried twice over. An error after the message's end leaves
                // the whole reply standing.
                if (!stopped)
                    throw new LlmStreamBrokenException(error ?? "the reply's stream ended before it was finished");
                result.Text = sb.ToString();
                return result;
            }
        }

        static string ExtractErrorMessage(string body)
        {
            try
            {
                var root = MiniJson.AsObject(MiniJson.Deserialize(body));
                var error = MiniJson.GetObject(root, "error");
                return MiniJson.GetString(error, "message") ?? body;
            }
            catch { return body; }
        }

        public static LlmResponse ParseResponse(string json)
        {
            var root = MiniJson.AsObject(MiniJson.Deserialize(json));
            var result = new LlmResponse
            {
                StopReason = MiniJson.GetString(root, "stop_reason") ?? "",
                Model = MiniJson.GetString(root, "model") ?? "",
            };
            var usage = MiniJson.GetObject(root, "usage");
            result.InputTokens = MiniJson.GetInt(usage, "input_tokens");
            result.OutputTokens = MiniJson.GetInt(usage, "output_tokens");

            var content = MiniJson.GetList(root, "content");
            if (content != null)
            {
                var sb = new StringBuilder();
                foreach (var blockObj in content)
                {
                    var block = MiniJson.AsObject(blockObj);
                    if (MiniJson.GetString(block, "type") == "text")
                        sb.Append(MiniJson.GetString(block, "text"));
                }
                result.Text = sb.ToString();
            }
            return result;
        }

        public void Dispose() => _http.Dispose();
    }

    public class LlmApiException : Exception
    {
        public int StatusCode { get; }
        public LlmApiException(int statusCode, string message) : base($"HTTP {statusCode}: {message}")
        {
            StatusCode = statusCode;
        }
    }

    /// A reply's stream that broke after it started (an error event, or an end
    /// before the message's end). Nothing retries it here: the caller knows
    /// whether any of it was already used, and so whether asking again is safe.
    public class LlmStreamBrokenException : LlmApiException
    {
        public LlmStreamBrokenException(string message) : base(500, message) { }
    }
}
