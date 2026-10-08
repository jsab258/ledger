using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE CHECK'S SUCCESSOR (the talk task of 7 October 2026): the claim check runs
/// on Claude Haiku 4.5, whose retirement may come any time from 15 October 2026.
/// Its likely successors judge the same labelled details, over the API on
/// LEDGER's key (--key), each call timed, so the choice rests on accuracy and on
/// speed measured the same way.
///
///     successors --key --cap 0.9 --models claude-haiku-4-5,claude-haiku-5-5:disabled,claude-sonnet-5-5:between_tools:low
///                [--half held] [--limit 60] [--drafts 40] --dir F:/LedgerTools/town-scratch/detail-bench
///
/// A model is "id[:thinking[:effort]]". THE DETAILS: detail-gold.jsonl (30
/// September; two labellers apart and a third, blind to the check), each
/// labelled detail put to the check's second look (ClaimCheck.RequestVerify)
/// as the live check puts it: true details refused, invented ones passed.
/// THE DRAFTS (--drafts N): the whole check (the list and its second looks,
/// ClaimCheck.CheckAsync) on N labelled replies of the 28 September bench's
/// held half, half of them invented: invented replies caught, honest ones flagged.
static partial class Program
{
    /// Every request through it carries the model's thinking and effort; the
    /// second looks their own, when the spec gives them ("id:list:effort:look:effort").
    sealed class Configured : ILlmClient
    {
        readonly ILlmClient _inner; readonly string _thinking, _effort, _lookThinking, _lookEffort;
        public Configured(ILlmClient inner, string thinking, string effort, string lookThinking = null, string lookEffort = null)
        { _inner = inner; _thinking = thinking; _effort = effort; _lookThinking = lookThinking ?? thinking; _lookEffort = lookThinking != null ? lookEffort : effort; }
        public Task<LlmResponse> CompleteAsync(LlmRequest r, CancellationToken ct = default)
        {
            bool look = r.System != null && r.System.StartsWith("You check details against", StringComparison.Ordinal);
            r.Thinking = look ? _lookThinking : _thinking; r.Effort = look ? _lookEffort : _effort;
            string _thinking1 = r.Thinking;
            // Thinking comes out of the same allowance as the answer: room for it,
            // so a look that thinks is not cut off before its verdict.
            if (_thinking1 == "adaptive" || _thinking1 == "enabled") r.MaxTokens += 4000;
            return _inner.CompleteAsync(r, ct);
        }
    }

    sealed class GoldDraft { public string id { get; set; } public bool invented { get; set; } }

    static async Task<int> Successors(string[] args, string dir, int parallel)
    {
        var specs = Arg(args, "--models", "claude-haiku-4-5,claude-haiku-5-5:disabled").Split(',', StringSplitOptions.RemoveEmptyEntries);
        string half = Arg(args, "--half", "held");
        int limit = int.Parse(Arg(args, "--limit", "0"));
        int draftsN = int.Parse(Arg(args, "--drafts", "0"));
        var rows = ReadDetails(Path.Combine(dir, "detail-gold.jsonl")).Where(r => Supported(r.Label) != null && (half == "all" || r.Half == half)).OrderBy(r => r.Id).ToList();
        // A limit takes the first of each label in turn, so the sample keeps the set's mix.
        if (limit > 0 && limit < rows.Count)
            rows = rows.GroupBy(r => Supported(r.Label) == true).SelectMany(g => g.Take((int)Math.Round(limit * (double)g.Count() / rows.Count))).OrderBy(r => r.Id).ToList();
        var benchDir = Path.Combine(RepoRoot(), "production", "research", "invented-claims", "bench");
        var drafts = new List<(Draft d, bool invented)>();
        if (draftsN > 0)
        {
            var all = ReadJsonl<Draft>(Path.Combine(benchDir, "drafts.jsonl")).ToDictionary(d => d.id);
            bool tuneDrafts = Arg(args, "--draft-half", "held") == "tune";
            var gold = ReadJsonl<GoldDraft>(Path.Combine(benchDir, "gold.jsonl")).Where(g => all.ContainsKey(g.id) && TuneSets.Contains(all[g.id].set) == tuneDrafts).OrderBy(g => g.id).ToList();
            drafts = gold.Where(g => g.invented).Take(draftsN / 2).Concat(gold.Where(g => !g.invented).Take(draftsN - draftsN / 2))
                         .Select(g => (all[g.id], g.invented)).ToList();
        }
        using var client = (IDisposable)BenchClient(args, $"the check's successors: {rows.Count} labelled details ({half} half) and {drafts.Count} labelled replies, on " + string.Join(", ", specs));
        var key = (ILlmClient)client;
        var report = new List<string>();
        var outRows = new List<object>();
        foreach (var spec in specs)
        {
            var parts = spec.Split(':');
            string model = parts[0], thinking = parts.Length > 1 && parts[1].Length > 0 ? parts[1] : null, effort = parts.Length > 2 && parts[2].Length > 0 ? parts[2] : null;
            string lookThinking = parts.Length > 3 && parts[3].Length > 0 ? parts[3] : null, lookEffort = parts.Length > 4 && parts[4].Length > 0 ? parts[4] : null;
            var c = new Configured(key, thinking, effort, lookThinking, lookEffort);
            var gate = new SemaphoreSlim(parallel);
            var ms = new List<long>();
            var verdicts = new bool?[rows.Count];
            await Task.WhenAll(rows.Select(async (r, i) =>
            {
                await gate.WaitAsync();
                try
                {
                    var ids = r.Known.Select(k => k.Split(new[] { ": " }, 2, StringSplitOptions.None)[0]).ToList();
                    for (int attempt = 0; attempt < 2 && verdicts[i] == null; attempt++)
                    {
                        var sw = Stopwatch.StartNew();
                        try
                        {
                            var resp = await c.CompleteAsync(ClaimCheck.RequestVerify(model, Numbered(r.Known), new[] { r.Detail }));
                            sw.Stop();
                            lock (ms) ms.Add(sw.ElapsedMilliseconds);
                            var v = ClaimCheck.ParseVerify(resp.Text, 1, ids);
                            if (v != null) verdicts[i] = v[0];
                        }
                        catch (BudgetSpentException) { return; }
                        catch (Exception) { await Task.Delay(1500); }
                    }
                }
                finally { gate.Release(); }
            }));
            int trueN = 0, falseN = 0, refusedTrue = 0, passedFalse = 0, unread = 0;
            for (int i = 0; i < rows.Count; i++)
            {
                bool gold = Supported(rows[i].Label) == true;
                if (verdicts[i] == null) { unread++; continue; }
                if (gold) { trueN++; if (verdicts[i] == false) refusedTrue++; }
                else { falseN++; if (verdicts[i] == true) passedFalse++; }
                outRows.Add(new { spec, part = "detail", rows[i].Id, rows[i].Half, rows[i].Label, gold, passed = verdicts[i] });
            }
            ms.Sort();
            string line = $"{spec}: details ({half}) true refused {refusedTrue}/{trueN} ({Pct(refusedTrue, trueN)}), invented passed {passedFalse}/{falseN} ({Pct(passedFalse, falseN)}), " +
                          $"unread {unread}; a look's time median {Med(ms)} ms, p90 {P90(ms)} ms";
            // THE WHOLE CHECK on labelled replies, each timed from its list to its last look.
            if (drafts.Count > 0)
            {
                var dms = new List<long>();
                int tp = 0, fn = 0, fp = 0, tn = 0, unchecked1 = 0;
                await Task.WhenAll(drafts.Select(async x =>
                {
                    await gate.WaitAsync();
                    try
                    {
                        var sw = Stopwatch.StartNew();
                        IReadOnlyList<string> found = null;
                        try { found = (await ClaimCheck.CheckAsync(c, model, ItemsFor(x.d), x.d.reply, default)).invented; }
                        catch (BudgetSpentException) { return; }
                        catch (Exception) { found = null; }
                        sw.Stop();
                        lock (dms)
                        {
                            dms.Add(sw.ElapsedMilliseconds);
                            bool f = found != null && found.Count > 0;
                            if (found == null) unchecked1++;
                            else if (x.invented && f) tp++; else if (x.invented) fn++; else if (f) fp++; else tn++;
                            outRows.Add(new { spec, part = "draft", x.d.id, gold = x.invented, flagged = found, ms = sw.ElapsedMilliseconds });
                        }
                    }
                    finally { gate.Release(); }
                }));
                dms.Sort();
                line += $"; whole check on {drafts.Count} replies: invented caught {tp}/{tp + fn} ({Pct(tp, tp + fn)}), honest flagged {fp}/{fp + tn} ({Pct(fp, fp + tn)}), " +
                        $"unchecked {unchecked1}; time median {Med(dms)} ms, p90 {P90(dms)} ms";
            }
            Console.WriteLine(line);
            report.Add(line);
        }
        WriteJsonl(Path.Combine(dir, "successors.jsonl"), outRows);
        File.WriteAllLines(Path.Combine(dir, "successors.txt"), report);
        LogKeyRun(rows.Count * specs.Length + drafts.Count * specs.Length);
        return 0;
    }

    static string Pct(int a, int b) => b == 0 ? "-" : (100.0 * a / b).ToString("0") + "%";
    static long Med(List<long> xs) => xs.Count == 0 ? 0 : xs[xs.Count / 2];
    static long P90(List<long> xs) => xs.Count == 0 ? 0 : xs[Math.Min(xs.Count - 1, (int)(xs.Count * 0.9))];
}
