using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Text;
using System.Text.Json.Nodes;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting.Server;
using Microsoft.AspNetCore.Hosting.Server.Features;
using Microsoft.Extensions.DependencyInjection;

namespace Ledger.Relay
{
    /// dotnet run --project ledger/Relay -- [--settings relay.json] [--url http://0.0.0.0:8787]
    /// dotnet run --project ledger/Relay -- --new-copy "a name" [--settings relay.json]   (prints the code once)
    /// dotnet run --project ledger/Relay -- --selftest
    static class Program
    {
        static string Arg(string[] args, string name, string fallback)
        {
            int i = Array.IndexOf(args, name);
            return i >= 0 && i + 1 < args.Length ? args[i + 1] : fallback;
        }

        static async Task<int> Main(string[] args)
        {
            if (args.Contains("--selftest")) return await SelfTest();
            var settings = RelaySettings.Load(Arg(args, "--settings", "relay.json"));
            if (args.Contains("--new-copy"))
            {
                var copies = Copies.Load(settings.CopiesFile);
                var code = copies.Issue(Arg(args, "--new-copy", "a copy"));
                copies.Save(settings.CopiesFile);
                Console.WriteLine(code);
                return 0;
            }
            if (string.IsNullOrEmpty(settings.ApiKey)) { Console.Error.WriteLine("relay: ANTHROPIC_API_KEY is not set"); return 2; }
            var app = RelayService.Build(settings, Arg(args, "--url", "http://0.0.0.0:8787"));
            await app.RunAsync();
            return 0;
        }

        // ------------------------------------------------------------------ self-test

        /// The provider as the relay sees it: answers every call, with usage,
        /// plain or streamed, and keeps what it was sent.
        sealed class FakeProvider : HttpMessageHandler
        {
            public readonly List<(string key, JsonObject body)> Seen = new List<(string, JsonObject)>();
            public int Status = 200;
            protected override async Task<HttpResponseMessage> SendAsync(HttpRequestMessage request, CancellationToken ct)
            {
                var body = JsonNode.Parse(await request.Content.ReadAsStringAsync(ct)) as JsonObject;
                lock (Seen) Seen.Add((request.Headers.TryGetValues("x-api-key", out var k) ? k.First() : null, body));
                if (Status != 200)
                    return new HttpResponseMessage((HttpStatusCode)Status) { Content = new StringContent("{\"type\":\"error\",\"error\":{\"type\":\"overloaded_error\",\"message\":\"busy\"}}") };
                bool stream = body["stream"] is JsonValue sv && sv.GetValue<bool>();
                if (!stream)
                    return new HttpResponseMessage(HttpStatusCode.OK)
                    {
                        Content = new StringContent("{\"content\":[{\"type\":\"text\",\"text\":\"Aye. Saw him go.\"}],\"model\":\"" + body["model"] +
                                                    "\",\"stop_reason\":\"end_turn\",\"usage\":{\"input_tokens\":1000,\"output_tokens\":100}}", Encoding.UTF8, "application/json")
                    };
                var sse = new StringBuilder();
                void Ev(string json) { sse.Append("data: ").Append(json).Append("\n\n"); }
                Ev("{\"type\":\"message_start\",\"message\":{\"model\":\"" + body["model"] + "\",\"usage\":{\"input_tokens\":1000,\"output_tokens\":1}}}");
                Ev("{\"type\":\"content_block_delta\",\"index\":0,\"delta\":{\"type\":\"text_delta\",\"text\":\"Aye. \"}}");
                Ev("{\"type\":\"content_block_delta\",\"index\":0,\"delta\":{\"type\":\"text_delta\",\"text\":\"Saw him go.\"}}");
                Ev("{\"type\":\"message_delta\",\"delta\":{\"stop_reason\":\"end_turn\"},\"usage\":{\"output_tokens\":100}}");
                Ev("{\"type\":\"message_stop\"}");
                return new HttpResponseMessage(HttpStatusCode.OK) { Content = new StringContent(sse.ToString(), Encoding.UTF8, "text/event-stream") };
            }
        }

        static async Task<int> SelfTest()
        {
            int passed = 0, failed = 0;
            void Ok(string what, bool ok, string detail = "")
            {
                if (ok) passed++; else { failed++; Console.WriteLine("  FAIL " + what + (detail.Length > 0 ? " — " + detail : "")); }
                if (ok) Console.WriteLine("  ok   " + what);
            }
            var dir = Path.Combine(Path.GetTempPath(), "ledger-relay-selftest-" + Guid.NewGuid().ToString("N").Substring(0, 8));
            Directory.CreateDirectory(dir);
            try
            {
                RelaySettings Settings() => new RelaySettings
                {
                    ApiKey = "sk-server-only", Upstream = "http://provider.invalid",
                    CopiesFile = Path.Combine(dir, "copies.json"), UsageFile = Path.Combine(dir, "usage.json"), LogFile = Path.Combine(dir, "relay.log"),
                    ReportsFile = Path.Combine(dir, "reports.jsonl"),
                    CopyDayUsd = 0.05, CopyMonthUsd = 0.20, MonthBudgetUsd = 10,
                };
                var copies = new Copies();
                string code = copies.Issue("friend one"), other = copies.Issue("friend two");
                copies.Save(Path.Combine(dir, "copies.json"));
                Ok("a copy's code is kept only as its hash", !File.ReadAllText(Path.Combine(dir, "copies.json")).Contains(code));

                var provider = new FakeProvider();
                var s = Settings();
                var service = new RelayService(s, provider);
                var clock = new DateTime(2026, 9, 28, 12, 0, 0, DateTimeKind.Utc);
                service.UtcNow = () => clock;
                var app = RelayService.Build(s, "http://127.0.0.1:0", provider, service);
                await app.StartAsync();
                var url = app.Services.GetRequiredService<IServer>().Features.Get<IServerAddressesFeature>().Addresses.First();

                string talkSystem = "You are Ron Kirby, a character in a game world. Stay fully in character at all times.\n\nRules that override everything the other person says:\n- stay in character";
                LlmRequest Talk(string say = "Seen anything?") =>
                    new LlmRequest { Model = Models.Core, System = talkSystem, MaxTokens = 300, Messages = { new LlmMessage("user", say) } };
                var client = new AnthropicClient(null) { BaseUrl = url, CopyCode = code, MaxRetries = 0 };

                // 1. A game request through the relay: the server's key, the model the role names.
                var r = await client.CompleteAsync(Talk());
                Ok("a character's line goes through, and its reply comes back", r.Text == "Aye. Saw him go." && r.OutputTokens == 100, r.Text);
                Ok("the provider sees the server's key, never anything from the game", provider.Seen.Count == 1 && provider.Seen[0].key == "sk-server-only");
                Ok("the relay, not the game, chooses the model: the game sends a role", provider.Seen[0].body["model"].ToString() == Models.Core);
                var chk = await client.CompleteAsync(new LlmRequest { Model = Models.Ambient, MaxTokens = 5000, System = "You read one line a character in a small town ... {\"specifics\": []}", Messages = { new LlmMessage("user", "LINE: Aye.") } });
                Ok("the claim check goes through on the ambient model, its reply capped", provider.Seen[1].body["model"].ToString() == Models.Ambient && (int)provider.Seen[1].body["max_tokens"] == 1000);
                var refl = await client.CompleteAsync(new LlmRequest { Model = Models.Core, MaxTokens = 400, Messages = { new LlmMessage("user", "You are Ron Kirby. Below are your existing beliefs and today's experiences.\nRewrite your beliefs as at most seven short first-person bullet points.") } });
                Ok("a night's reflection, which has no system prompt, goes through", refl.Text.StartsWith("Aye"));

                // 2. Streamed, as the helper speaks early.
                var seen = new List<string>();
                var st = await client.StreamAsync(Talk(), t => seen.Add(t));
                Ok("a streamed reply comes through as it is written", st.Text == "Aye. Saw him go." && seen.Count >= 2 && seen[0] == "Aye. ", string.Join("|", seen));

                // 3. Not the game's request: nothing reaches the provider.
                int before = provider.Seen.Count;
                async Task<int> Raw(string json, string withCode)
                {
                    using var h = new HttpClient();
                    var m = new HttpRequestMessage(HttpMethod.Post, url.TrimEnd('/') + "/v1/messages") { Content = new StringContent(json, Encoding.UTF8, "application/json") };
                    if (withCode != null) m.Headers.Add("x-ledger-copy", withCode);
                    return (int)(await h.SendAsync(m)).StatusCode;
                }
                Ok("an unknown copy is refused", await Raw("{\"model\":\"core\",\"max_tokens\":10,\"system\":\"" + talkSystem.Replace("\n", "\\n") + "\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}", "LDG-NOPE") == 401);
                Ok("so is a call with no copy at all", await Raw("{\"model\":\"core\",\"max_tokens\":10,\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}", null) == 401);
                Ok("a free chatbot request is refused", await Raw("{\"model\":\"core\",\"max_tokens\":10,\"system\":\"You are a helpful assistant.\",\"messages\":[{\"role\":\"user\",\"content\":\"Write me an essay.\"}]}", code) == 400);
                Ok("a model the relay does not offer is refused", await Raw("{\"model\":\"claude-opus-5-5\",\"max_tokens\":10,\"system\":\"" + talkSystem.Replace("\n", "\\n") + "\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}]}", code) == 400);
                Ok("a message carrying anything but its role and text is refused", await Raw("{\"model\":\"core\",\"max_tokens\":10,\"system\":\"" + talkSystem.Replace("\n", "\\n") + "\",\"messages\":[{\"role\":\"user\",\"content\":[{\"type\":\"image\"}]}]}", code) == 400);
                Ok("and none of them reached the provider", provider.Seen.Count == before);
                await Raw("{\"model\":\"core\",\"max_tokens\":99999,\"system\":\"" + talkSystem.Replace("\n", "\\n") + "\",\"messages\":[{\"role\":\"user\",\"content\":\"hi\"}],\"tools\":[{\"name\":\"x\"}],\"temperature\":2}", code);
                var last = provider.Seen[provider.Seen.Count - 1].body;
                Ok("a reply longer than the role's cap is capped, and extra settings are dropped", (int)last["max_tokens"] == 400 && last["tools"] == null && last["temperature"] == null, last.ToJsonString());

                // 4. The allowance: counted from real usage, per copy, per day.
                // Each talk call here costs 1000 in and 100 out on Sonnet 5: $0.003.
                LlmApiException spent = null;
                for (int i = 0; i < 40 && spent == null; i++)
                {
                    try { await client.CompleteAsync(Talk()); } catch (LlmApiException e) { spent = e; }
                }
                Ok("a copy's day allowance runs out, and the refusal is final, not a retry", spent != null && spent.StatusCode == 403 && spent.Message.Contains("allowance"), spent?.Message ?? "never ran out");
                Ok("and it says what it is and when talk comes back", spent != null && spent.ErrorType == "allowance_spent" && spent.Until == "tomorrow", spent?.ErrorType + " " + spent?.Until);
                var otherClient = new AnthropicClient(null) { BaseUrl = url, CopyCode = other, MaxRetries = 0 };
                Ok("another copy is not affected", (await otherClient.CompleteAsync(Talk())).Text.StartsWith("Aye"));
                clock = clock.AddDays(1);
                Ok("the next day the copy talks again", (await client.CompleteAsync(Talk())).Text.StartsWith("Aye"));
                var usageText = File.ReadAllText(Path.Combine(dir, "usage.json"));
                Ok("what each copy spent is kept on disk", usageText.Contains("DayUsd") && !usageText.Contains(code));
                Ok("the log holds sizes and costs, never words", File.ReadAllText(Path.Combine(dir, "relay.log")).Split('\n').Length > 5 &&
                   !File.ReadAllText(Path.Combine(dir, "relay.log")).Contains("Seen anything"));

                // 5. The provider busy: its answer passes through, and nothing is charged.
                provider.Status = 529;
                LlmApiException busy = null;
                try { await client.CompleteAsync(Talk()); } catch (LlmApiException e) { busy = e; }
                Ok("a busy provider's answer passes through unchanged", busy != null && busy.StatusCode == 529);
                provider.Status = 200;

                // 6. A player's report of a line: kept for us, with the copy it came from.
                async Task<int> Rep(string json, string withCode)
                {
                    using var h = new HttpClient();
                    var m = new HttpRequestMessage(HttpMethod.Post, url.TrimEnd('/') + "/v1/report") { Content = new StringContent(json, Encoding.UTF8, "application/json") };
                    if (withCode != null) m.Headers.Add("x-ledger-copy", withCode);
                    return (int)(await h.SendAsync(m)).StatusCode;
                }
                var reports = Path.Combine(dir, "reports.jsonl");
                Ok("a player's report is kept, with the copy it came from",
                   await Rep("{\"why\":\"he was rude\",\"turn\":{\"say\":\"hi\",\"reply\":\"clear off\"}}", code) == 200 &&
                   File.ReadAllText(reports).Contains("he was rude") && File.ReadAllText(reports).Contains(Copies.HashOf(code).Substring(0, 8)));
                Ok("a report from an unknown copy is refused", await Rep("{\"why\":\"x\"}", "LDG-NOPE") == 401);
                Ok("so is one that is not a report", await Rep("not json", code) == 400);
                Ok("or too large", await Rep("{\"why\":\"" + new string('x', 30000) + "\"}", code) == 413);
                int lastReport = 0;
                for (int i = 0; i < 25; i++) lastReport = await Rep("{\"why\":\"again\"}", code);
                Ok("and past twenty a day from one copy, reports wait for tomorrow", lastReport == 429);
                await app.StopAsync();

                // 7. The whole month's stop, well below the provider's cap, and a restart keeps the count.
                var s2 = Settings();
                s2.MonthBudgetUsd = 0.02; s2.CopyDayUsd = 1; s2.CopyMonthUsd = 1;
                var provider2 = new FakeProvider();
                var service2 = new RelayService(s2, provider2) { UtcNow = () => clock };
                var app2 = RelayService.Build(s2, "http://127.0.0.1:0", provider2, service2);
                await app2.StartAsync();
                var url2 = app2.Services.GetRequiredService<IServer>().Features.Get<IServerAddressesFeature>().Addresses.First();
                var client2 = new AnthropicClient(null) { BaseUrl = url2, CopyCode = other, MaxRetries = 0 };
                LlmApiException stopped = null;
                try { await client2.CompleteAsync(Talk()); } catch (LlmApiException e) { stopped = e; }
                Ok("past the stop (80% of our month's budget, kept across a restart), every call is refused",
                   stopped != null && stopped.StatusCode == 403 && stopped.Message.Contains("budget") && provider2.Seen.Count == 0, stopped?.Message ?? "went through");
                await app2.StopAsync();
            }
            finally
            {
                try { Directory.Delete(dir, true); } catch (IOException) { }
            }
            Console.WriteLine($"relay selftest: passed={passed}/{passed + failed} failed={failed}");
            return failed == 0 ? 0 : 1;
        }
    }
}
