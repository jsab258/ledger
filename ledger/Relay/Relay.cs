using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net.Http;
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.Logging;

namespace Ledger.Relay
{
    /// THE SERVER OF OURS BETWEEN THE GAME AND THE MODEL (ROADMAP, "a
    /// thirty-minute build for his friends"; town list 6b, 28 September). The
    /// game never holds the key: it holds a copy code, and every live call goes
    /// through here, which
    ///   - knows the copy (a code issued per copy, kept only as its hash) and
    ///     counts its allowance, per day and per month, in dollars from real usage;
    ///   - chooses the model for each role ("core", "ambient"), so the model and
    ///     the provider change here and nowhere else;
    ///   - caps each reply's length and takes only the game's own requests (a
    ///     character's line, the claim check, its second look, a night's
    ///     reflection), so it cannot be used as a free chatbot (the research:
    ///     92 of 444 apps ran a server "that answers anyone");
    ///   - stops every call at a fraction of our own monthly budget, well below
    ///     the provider's cap, where every call fails until the 1st;
    ///   - logs each call's size and cost, never its words.
    /// When it refuses, the game says its written lines (the brush-off), as it
    /// does offline. Research: production/research/runtime-ai-business/notes/plumbing.md.
    public sealed class RelaySettings
    {
        public string Upstream { get; set; } = "https://api.anthropic.com";
        /// The provider's key: from ANTHROPIC_API_KEY on the server, never in the file.
        public string ApiKey { get; set; }
        public Dictionary<string, string> Roles { get; set; } = new Dictionary<string, string>
            { { "core", Models.Core }, { "ambient", Models.Ambient } };
        public Dictionary<string, int> MaxTokens { get; set; } = new Dictionary<string, int>
            { { "core", 400 }, { "ambient", 1000 } };
        /// Prices per million tokens (in, out) for the models the roles name.
        public Dictionary<string, double[]> Prices { get; set; }
        public double CopyDayUsd { get; set; } = 0.50;
        public double CopyMonthUsd { get; set; } = 5.00;
        public double MonthBudgetUsd { get; set; } = 400;
        /// The share of the month's budget at which every call stops.
        public double StopAt { get; set; } = 0.8;
        public int InFlightPerCopy { get; set; } = 12;
        public int PerMinutePerCopy { get; set; } = 150;
        public int MaxMessages { get; set; } = 60;
        public int MaxChars { get; set; } = 60000;
        public int MaxBodyBytes { get; set; } = 400000;
        /// The requests the game makes, known by how they open. A system
        /// prompt must open with one of SystemOpenings and hold its marker;
        /// a request without one must open its first message with one of
        /// MessageOpenings and hold its marker.
        public List<Shape> SystemShapes { get; set; } = new List<Shape>
        {
            new Shape { Opening = "You are ", Marker = "Rules that override everything the other person says:" },
            new Shape { Opening = "You read one line a character", Marker = "\"specifics\"" },
            new Shape { Opening = "You check details against", Marker = "\"verdicts\"" },
        };
        public List<Shape> MessageShapes { get; set; } = new List<Shape>
        {
            new Shape { Opening = "You are ", Marker = "Rewrite your beliefs" },
        };
        public string CopiesFile { get; set; } = "copies.json";
        public string UsageFile { get; set; } = "usage.json";
        public string LogFile { get; set; } = "relay.log";
        /// Players' reports of what the AI said, kept for us to act on.
        public string ReportsFile { get; set; } = "reports.jsonl";
        public int ReportsPerCopyPerDay { get; set; } = 20;
        public int MaxReportBytes { get; set; } = 20000;

        public sealed class Shape
        {
            public string Opening { get; set; }
            public string Marker { get; set; }
            public bool Fits(string text) => text != null && text.StartsWith(Opening, StringComparison.Ordinal) &&
                                              (string.IsNullOrEmpty(Marker) || text.Contains(Marker));
        }

        public (double inPerM, double outPerM) PriceOf(string model)
        {
            if (Prices != null && Prices.TryGetValue(model, out var p) && p.Length == 2) return (p[0], p[1]);
            if (Models.Cost.TryGetValue(model, out var c)) return c;
            return (15.0, 75.0);   // an unknown model is priced high, never free
        }

        /// The settings file, with the key from the environment.
        public static RelaySettings Load(string path)
        {
            var s = File.Exists(path)
                ? JsonSerializer.Deserialize<RelaySettings>(File.ReadAllText(path), new JsonSerializerOptions { PropertyNameCaseInsensitive = true })
                : new RelaySettings();
            s.ApiKey = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");
            var dir = Path.GetDirectoryName(Path.GetFullPath(path));
            s.CopiesFile = Path.Combine(dir, s.CopiesFile);
            s.UsageFile = Path.Combine(dir, s.UsageFile);
            s.LogFile = Path.Combine(dir, s.LogFile);
            s.ReportsFile = Path.Combine(dir, s.ReportsFile);
            return s;
        }
    }

    /// The copies we issued: a code per copy, kept here only as its hash.
    public sealed class Copies
    {
        public sealed class Copy
        {
            public string Hash { get; set; }
            public string Name { get; set; }
            public bool Revoked { get; set; }
        }
        public List<Copy> List { get; set; } = new List<Copy>();

        public static string HashOf(string code) =>
            Convert.ToHexString(SHA256.HashData(Encoding.UTF8.GetBytes((code ?? "").Trim()))).ToLowerInvariant();

        public Copy Find(string code)
        {
            if (string.IsNullOrWhiteSpace(code)) return null;
            var h = HashOf(code);
            foreach (var c in List) if (!c.Revoked && CryptographicOperations.FixedTimeEquals(Encoding.ASCII.GetBytes(c.Hash), Encoding.ASCII.GetBytes(h))) return c;
            return null;
        }

        /// A new code for a copy, returned once; only its hash is kept.
        public string Issue(string name)
        {
            var code = "LDG-" + Convert.ToHexString(RandomNumberGenerator.GetBytes(10));
            List.Add(new Copy { Hash = HashOf(code), Name = name });
            return code;
        }

        public static Copies Load(string path) =>
            File.Exists(path) ? JsonSerializer.Deserialize<Copies>(File.ReadAllText(path)) ?? new Copies() : new Copies();
        public void Save(string path) => Atomic(path, JsonSerializer.Serialize(this, new JsonSerializerOptions { WriteIndented = true }));

        internal static void Atomic(string path, string text)
        {
            var tmp = path + ".tmp";
            File.WriteAllText(tmp, text);
            File.Move(tmp, path, true);
        }
    }

    /// What each copy, and the whole relay, has spent this day and month.
    public sealed class Usage
    {
        public sealed class Spend
        {
            public string Day { get; set; }
            public double DayUsd { get; set; }
            public string Month { get; set; }
            public double MonthUsd { get; set; }
        }
        public string Month { get; set; }
        public double MonthUsd { get; set; }
        public Dictionary<string, Spend> Copies { get; set; } = new Dictionary<string, Spend>();

        public static Usage Load(string path) =>
            File.Exists(path) ? JsonSerializer.Deserialize<Usage>(File.ReadAllText(path)) ?? new Usage() : new Usage();
        public void Save(string path) => Ledger.Relay.Copies.Atomic(path, JsonSerializer.Serialize(this));

        /// The spend for one copy, rolled over to today and this month.
        public Spend For(string hash, DateTime utc)
        {
            string day = utc.ToString("yyyy-MM-dd"), month = utc.ToString("yyyy-MM");
            if (Month != month) { Month = month; MonthUsd = 0; }
            if (!Copies.TryGetValue(hash, out var s)) Copies[hash] = s = new Spend();
            if (s.Day != day) { s.Day = day; s.DayUsd = 0; }
            if (s.Month != month) { s.Month = month; s.MonthUsd = 0; }
            return s;
        }
    }

    public sealed class RelayService
    {
        readonly RelaySettings _s;
        readonly Copies _copies;
        readonly Usage _usage;
        readonly HttpClient _up;
        readonly object _gate = new object();
        readonly Dictionary<string, int> _inFlight = new Dictionary<string, int>();
        readonly Dictionary<string, Queue<DateTime>> _recent = new Dictionary<string, Queue<DateTime>>();
        readonly Dictionary<string, double> _reserved = new Dictionary<string, double>();
        double _reservedAll;
        /// The clock, a seam for tests (month and day rollover).
        public Func<DateTime> UtcNow = () => DateTime.UtcNow;

        public RelayService(RelaySettings s, HttpMessageHandler upstream = null)
        {
            _s = s;
            _copies = Copies.Load(s.CopiesFile);
            _usage = Usage.Load(s.UsageFile);
            _up = upstream != null ? new HttpClient(upstream) : new HttpClient();
            _up.Timeout = TimeSpan.FromSeconds(90);
        }

        static async Task Refuse(HttpContext ctx, int status, string type, string message, string until = null)
        {
            ctx.Response.StatusCode = status;
            ctx.Response.ContentType = "application/json";
            await ctx.Response.WriteAsync(until == null
                ? JsonSerializer.Serialize(new { type = "error", error = new { type, message } })
                : JsonSerializer.Serialize(new { type = "error", error = new { type, message, until } }));
        }

        public async Task Handle(HttpContext ctx)
        {
            var sw = System.Diagnostics.Stopwatch.StartNew();
            var copy = _copies.Find(ctx.Request.Headers["x-ledger-copy"].ToString());
            if (copy == null) { await Refuse(ctx, 401, "unknown_copy", "This copy is not known here."); return; }

            // THE REQUEST: the game's own, or nothing.
            JsonObject body;
            try
            {
                using var ms = new MemoryStream();
                await ctx.Request.Body.CopyToAsync(ms);
                if (ms.Length > _s.MaxBodyBytes) { await Refuse(ctx, 413, "too_large", "Request too large."); return; }
                body = JsonNode.Parse(ms.ToArray()) as JsonObject;
            }
            catch (Exception) { body = null; }
            var why = Unfit(body, out string role, out bool stream, out int chars);
            if (why != null) { await Refuse(ctx, 400, "not_a_game_request", why); return; }
            string model = _s.Roles[role];
            int cap = _s.MaxTokens.TryGetValue(role, out var c) ? c : 300;
            int asked = body["max_tokens"] is JsonValue mv && mv.TryGetValue<int>(out var a) ? a : cap;
            body["model"] = model;
            body["max_tokens"] = Math.Max(1, Math.Min(asked, cap));
            foreach (var extra in body.Select(kv => kv.Key).Where(k => k != "model" && k != "max_tokens" && k != "system" && k != "messages" && k != "stream").ToList())
                body.Remove(extra);

            // THE ALLOWANCE AND THE STOP, reserved before the call so calls side by
            // side cannot overshoot, settled from the real usage after it.
            var (inP, outP) = _s.PriceOf(model);
            double estimate = (chars / 3.0 * inP + (int)body["max_tokens"] * outP) / 1e6;
            string refusal = null, refusalType = null, refusalUntil = null; int refusalStatus = 0;
            lock (_gate)
            {
                var now = UtcNow();
                var spend = _usage.For(copy.Hash, now);
                _reserved.TryGetValue(copy.Hash, out var mine);
                _inFlight.TryGetValue(copy.Hash, out var flying);
                if (!_recent.TryGetValue(copy.Hash, out var q)) _recent[copy.Hash] = q = new Queue<DateTime>();
                while (q.Count > 0 && (now - q.Peek()).TotalSeconds >= 60) q.Dequeue();
                if (_usage.MonthUsd + _reservedAll + estimate > _s.MonthBudgetUsd * _s.StopAt)
                { refusalStatus = 403; refusalType = "relay_stopped"; refusal = "The month's budget is spent; the town speaks its written lines."; }
                else if (spend.DayUsd + mine + estimate > _s.CopyDayUsd || spend.MonthUsd + mine + estimate > _s.CopyMonthUsd)
                {
                    refusalStatus = 403; refusalType = "allowance_spent"; refusal = "This copy's allowance of live talk is spent for now.";
                    // When it comes back, so the player can be told (town list 6t).
                    refusalUntil = spend.MonthUsd + mine + estimate > _s.CopyMonthUsd ? "next month" : "tomorrow";
                }
                else if (flying >= _s.InFlightPerCopy || q.Count >= _s.PerMinutePerCopy)
                { refusalStatus = 429; refusalType = "too_busy"; refusal = "Too many calls at once."; }
                else
                {
                    _inFlight[copy.Hash] = flying + 1;
                    q.Enqueue(now);
                    _reserved[copy.Hash] = mine + estimate;
                    _reservedAll += estimate;
                }
            }
            if (refusal != null)
            {
                Log(copy, role, 0, 0, 0, refusalStatus, sw.ElapsedMilliseconds, refusalType);
                await Refuse(ctx, refusalStatus, refusalType, refusal, refusalUntil);
                return;
            }

            int inTok = 0, outTok = 0, status = 0;
            try
            {
                using var req = new HttpRequestMessage(HttpMethod.Post, _s.Upstream.TrimEnd('/') + "/v1/messages");
                req.Headers.Add("x-api-key", _s.ApiKey ?? "");
                req.Headers.Add("anthropic-version", "2023-06-01");
                req.Content = new StringContent(body.ToJsonString(), Encoding.UTF8, "application/json");
                using var resp = await _up.SendAsync(req, stream ? HttpCompletionOption.ResponseHeadersRead : HttpCompletionOption.ResponseContentRead, ctx.RequestAborted);
                status = (int)resp.StatusCode;
                ctx.Response.StatusCode = status;
                ctx.Response.ContentType = resp.Content.Headers.ContentType?.ToString() ?? "application/json";
                if (stream && status == 200)
                {
                    // Passed through line by line as it is written, the usage read on the way.
                    using var up = await resp.Content.ReadAsStreamAsync();
                    using var reader = new StreamReader(up, Encoding.UTF8);
                    string line;
                    while ((line = await reader.ReadLineAsync()) != null)
                    {
                        if (line.StartsWith("data:", StringComparison.Ordinal)) ReadUsage(line.Substring(5), ref inTok, ref outTok);
                        await ctx.Response.WriteAsync(line + "\n", ctx.RequestAborted);
                        if (line.Length == 0) await ctx.Response.Body.FlushAsync(ctx.RequestAborted);
                    }
                }
                else
                {
                    var text = await resp.Content.ReadAsStringAsync();
                    if (status == 200) ReadUsage(text, ref inTok, ref outTok);
                    await ctx.Response.WriteAsync(text, ctx.RequestAborted);
                }
            }
            catch (Exception) when (!ctx.RequestAborted.IsCancellationRequested && !ctx.Response.HasStarted)
            {
                status = 502;
                await Refuse(ctx, 502, "upstream_unreachable", "The model could not be reached.");
            }
            catch (Exception) { if (status == 0) status = 499; }
            finally
            {
                double cost = (inTok * inP + outTok * outP) / 1e6;
                lock (_gate)
                {
                    var spend = _usage.For(copy.Hash, UtcNow());
                    spend.DayUsd += cost;
                    spend.MonthUsd += cost;
                    _usage.MonthUsd += cost;
                    _reserved[copy.Hash] = Math.Max(0, _reserved[copy.Hash] - estimate);
                    _reservedAll = Math.Max(0, _reservedAll - estimate);
                    _inFlight[copy.Hash] = Math.Max(0, _inFlight[copy.Hash] - 1);
                    try { _usage.Save(_s.UsageFile); } catch (IOException) { }
                }
                Log(copy, role, inTok, outTok, cost, status, sw.ElapsedMilliseconds, null);
            }
        }

        readonly Dictionary<string, (string day, int count)> _reports = new Dictionary<string, (string, int)>();

        /// A PLAYER'S REPORT of a line (town list 6c): what was said and what
        /// came back, and why they reported it, as the helper sends it. Kept,
        /// with the copy it came from, for us to read and act on; the player
        /// chose to send these words, so unlike the call log they are kept.
        public async Task Report(HttpContext ctx)
        {
            var copy = _copies.Find(ctx.Request.Headers["x-ledger-copy"].ToString());
            if (copy == null) { await Refuse(ctx, 401, "unknown_copy", "This copy is not known here."); return; }
            JsonObject body;
            try
            {
                using var ms = new MemoryStream();
                await ctx.Request.Body.CopyToAsync(ms);
                if (ms.Length > _s.MaxReportBytes) { await Refuse(ctx, 413, "too_large", "Report too large."); return; }
                body = JsonNode.Parse(ms.ToArray()) as JsonObject;
            }
            catch (Exception) { body = null; }
            if (body == null) { await Refuse(ctx, 400, "not_a_report", "A report is a JSON object."); return; }
            lock (_gate)
            {
                var day = UtcNow().ToString("yyyy-MM-dd");
                _reports.TryGetValue(copy.Hash, out var seen);
                if (seen.day != day) seen = (day, 0);
                if (seen.count >= _s.ReportsPerCopyPerDay) body = null;
                else _reports[copy.Hash] = (day, seen.count + 1);
            }
            if (body == null) { await Refuse(ctx, 429, "too_many_reports", "Too many reports today."); return; }
            var line = new JsonObject { ["receivedAt"] = UtcNow().ToString("O"), ["copy"] = copy.Hash.Substring(0, 8), ["report"] = body };
            try { lock (_gate) File.AppendAllText(_s.ReportsFile, line.ToJsonString() + "\n"); }
            catch (IOException) { await Refuse(ctx, 503, "not_kept", "The report could not be kept."); return; }
            ctx.Response.ContentType = "application/json";
            await ctx.Response.WriteAsync("{\"ok\":true}");
        }

        /// Why a request is not one of the game's own; null when it is.
        string Unfit(JsonObject body, out string role, out bool stream, out int chars)
        {
            role = null; stream = false; chars = 0;
            if (body == null) return "Not JSON.";
            role = (body["model"] as JsonValue)?.TryGetValue<string>(out var r) == true ? r : null;
            if (role == null || !_s.Roles.ContainsKey(role)) return "Unknown role.";
            if (body["stream"] is JsonValue sv && sv.TryGetValue<bool>(out var st)) stream = st;
            string system = null;
            if (body["system"] != null)
            {
                if (!(body["system"] is JsonValue sys) || !sys.TryGetValue<string>(out system)) return "The system prompt must be text.";
                chars += system.Length;
            }
            if (!(body["messages"] is JsonArray msgs) || msgs.Count == 0 || msgs.Count > _s.MaxMessages) return "Messages missing or too many.";
            string first = null;
            foreach (var m in msgs)
            {
                if (!(m is JsonObject mo)) return "A message must be an object.";
                var roleOf = (mo["role"] as JsonValue)?.TryGetValue<string>(out var ro) == true ? ro : null;
                if (roleOf != "user" && roleOf != "assistant") return "A message's role must be user or assistant.";
                if (!(mo["content"] is JsonValue cv) || !cv.TryGetValue<string>(out var content)) return "A message's content must be text.";
                if (mo.Count != 2) return "A message holds a role and its text, nothing else.";
                first ??= content;
                chars += content.Length;
            }
            if (chars > _s.MaxChars) return "Too long.";
            bool fits = system != null ? _s.SystemShapes.Any(sh => sh.Fits(system)) : _s.MessageShapes.Any(sh => sh.Fits(first));
            return fits ? null : "Not one of the game's requests.";
        }

        static void ReadUsage(string json, ref int inTok, ref int outTok)
        {
            try
            {
                var n = JsonNode.Parse(json.Trim());
                var usage = n?["usage"] ?? n?["message"]?["usage"];
                if (usage == null) return;
                if (usage["input_tokens"] is JsonValue i && i.TryGetValue<int>(out var iv) && iv > 0) inTok = iv;
                if (usage["output_tokens"] is JsonValue o && o.TryGetValue<int>(out var ov) && ov > 0) outTok = ov;
            }
            catch (Exception) { }
        }

        void Log(Copies.Copy copy, string role, int inTok, int outTok, double usd, int status, long ms, string refused)
        {
            // Size and cost only: never the words.
            var line = $"{UtcNow():O}\t{copy.Hash.Substring(0, 8)}\t{role}\t{status}\t{inTok}\t{outTok}\t{usd:0.000000}\t{ms}\t{refused ?? "-"}\n";
            try { lock (_gate) File.AppendAllText(_s.LogFile, line); } catch (IOException) { }
        }

        /// The whole service, at `url` ("http://127.0.0.1:0" for any free port).
        public static WebApplication Build(RelaySettings s, string url, HttpMessageHandler upstream = null, RelayService service = null)
        {
            var builder = WebApplication.CreateSlimBuilder();
            builder.WebHost.UseUrls(url);
            builder.Logging.ClearProviders();
            var app = builder.Build();
            var relay = service ?? new RelayService(s, upstream);
            app.MapPost("/v1/messages", new RequestDelegate(relay.Handle));
            app.MapPost("/v1/report", new RequestDelegate(relay.Report));
            app.MapGet("/health", ctx => ctx.Response.WriteAsync("ok"));
            return app;
        }
    }
}
