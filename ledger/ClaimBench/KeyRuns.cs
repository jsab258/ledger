using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using Ledger.Core;
using Ledger.DevTools;

/// RUNS ON LEDGER'S OWN KEY, CAPPED AND LOGGED (the talk task of 7 October 2026:
/// "Spend at most three dollars of my LEDGER key in total, every run logged").
///
/// With --key a bench mode talks to the API itself, as the game does, instead of
/// through Claude Code on the subscription: the key is read from LEDGER's own
/// file (%LOCALAPPDATA%\LEDGER\live-talk-key.txt), never printed or written
/// anywhere, and the client is held by BudgetedClient to what is left of the
/// task's three dollars (every earlier run of the task in
/// production/playtest/talk-runs.jsonl subtracted), and to --cap for this run
/// if lower. A call whose worst case would pass it is refused, never sent.
/// When the run ends, one line is appended to that log: the date, the task,
/// what ran, its calls, tokens by model and dollars. Refused under CI.
static partial class Program
{
    const string KeyTask = "talk-2026-10-07";
    const double KeyTaskCap = 3.00;
    static string RunsLog => Path.Combine(RepoRoot(), "production", "playtest", "talk-runs.jsonl");

    /// What the task's key runs have spent so far, from the log.
    static double KeyTaskSpent()
    {
        double spent = 0;
        if (!File.Exists(RunsLog)) return 0;
        foreach (var line in File.ReadAllLines(RunsLog))
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            try
            {
                using var d = JsonDocument.Parse(line);
                var r = d.RootElement;
                if (r.TryGetProperty("task", out var t) && t.ValueKind == JsonValueKind.String && t.GetString() == KeyTask
                    && r.TryGetProperty("usd", out var u) && u.ValueKind == JsonValueKind.Number) spent += u.GetDouble();
            }
            catch (JsonException) { }
        }
        return spent;
    }

    sealed class KeyRun
    {
        public BudgetedClient Client;
        public readonly Dictionary<string, (int calls, long inTok, long outTok)> ByModel = new Dictionary<string, (int, long, long)>();
        public string What;
        public int Turns;
    }

    static KeyRun _keyRun;

    /// The client a bench mode talks through: LEDGER's key, capped, with --key;
    /// else Claude Code on the subscription, as every bench ran before.
    static ILlmClient BenchClient(string[] args, string what)
    {
        if (!args.Contains("--key")) return new ClaudeCodeClient();
        if (Environment.GetEnvironmentVariable("CI") != null || Environment.GetEnvironmentVariable("GITHUB_ACTIONS") != null)
            throw new InvalidOperationException("refused: an automated run may never use LEDGER's key");
        var path = Path.Combine(Environment.GetEnvironmentVariable("LOCALAPPDATA") ?? "", "LEDGER", "live-talk-key.txt");
        string key = File.Exists(path) ? File.ReadAllText(path).Trim() : null;
        if (string.IsNullOrEmpty(key)) throw new InvalidOperationException("no LEDGER key: nothing run");
        double left = KeyTaskCap - KeyTaskSpent();
        double cap = double.Parse(Arg(args, "--cap", "1.00"), System.Globalization.CultureInfo.InvariantCulture);
        double limit = Math.Max(0, Math.Min(left, cap));
        if (limit < 0.01) throw new InvalidOperationException($"refused: the task's key runs have spent US${KeyTaskCap - left:0.00} of its US${KeyTaskCap:0.00}");
        Console.WriteLine($"key run: the task has spent US${KeyTaskCap - left:0.000} of US${KeyTaskCap:0.00}; this run is held to US${limit:0.000}");
        _keyRun = new KeyRun { Client = new BudgetedClient(new AnthropicClient(key, TimeSpan.FromSeconds(60)), limit), What = what };
        return new Counted(_keyRun);
    }

    /// Counts every call's tokens by model on the way through, for the log.
    sealed class Counted : ILlmClient, IDisposable
    {
        readonly KeyRun _run;
        public Counted(KeyRun run) => _run = run;
        public async System.Threading.Tasks.Task<LlmResponse> CompleteAsync(LlmRequest request, System.Threading.CancellationToken ct = default)
        {
            var r = await _run.Client.CompleteAsync(request, ct).ConfigureAwait(false);
            lock (_run.ByModel)
            {
                _run.ByModel.TryGetValue(request.Model ?? "", out var b);
                _run.ByModel[request.Model ?? ""] = (b.calls + 1, b.inTok + r.InputTokens, b.outTok + r.OutputTokens);
            }
            return r;
        }
        public void Dispose() => _run.Client.Dispose();
    }

    /// The run's line in the log, once it has ended, however it ended.
    static void LogKeyRun(int turns, string note = null)
    {
        var run = _keyRun;
        if (run == null) return;
        _keyRun = null;
        var tokens = new Dictionary<string, object>();
        int calls = 0;
        foreach (var kv in run.ByModel)
        {
            tokens[kv.Key] = new Dictionary<string, object> { { "calls", kv.Value.calls }, { "in", kv.Value.inTok }, { "out", kv.Value.outTok } };
            calls += kv.Value.calls;
        }
        var row = new Dictionary<string, object>
        {
            { "date", DateTime.Now.ToString("yyyy-MM-dd") }, { "task", KeyTask }, { "what", run.What + (note != null ? "; " + note : "") },
            { "turns", turns }, { "calls", calls }, { "tokens", tokens }, { "usd", Math.Round(run.Client.SpentUsd, 4) },
            { "refused", run.Client.Refused },
        };
        File.AppendAllText(RunsLog, JsonSerializer.Serialize(row, Plain) + "\n");
        Console.WriteLine($"key run logged: US${run.Client.SpentUsd:0.0000}, {calls} calls, {run.Client.Refused} refused for the cap; the task has now spent US${KeyTaskSpent():0.000} of US${KeyTaskCap:0.00}");
    }
}
