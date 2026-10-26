using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Ledger.Core;

/// WHAT A FIRST SENTENCE'S CHECK TAKES ITS TIME ON (his question of 26 October evening: "Ron's check is the
/// slowest on real questions (about 3.3 s to pass): find out why, for example the length of his known-facts
/// list").
///
///     dotnet run --project ledger/ClaimBench -c Release -- checktime --key --task slow-replies-2026-10-26
///         --from RUN_DIR[,RUN_DIR...] [--per 10] [--short 15] [--model claude-haiku-5-5] [--out OUT.jsonl]
///
/// Takes first sentences that passed their check in earlier `firsts --early` runs (their rows keep the very
/// facts list the check was given, ConversationEngine.LastKnown), --per for each of the three characters, and
/// checks each again twice, one call at a time so nothing overlaps: with its whole list, and with the list cut to
/// its first --short items. The order alternates sentence by sentence. Each call's time, its tokens in and out and
/// how many specifics it listed are written, so the time can be laid on the list's length and on the answer's.
static partial class Program
{
    static async Task<int> CheckTime(string[] args)
    {
        var runs = Arg(args, "--from", "").Split(',', StringSplitOptions.RemoveEmptyEntries);
        int per = int.Parse(Arg(args, "--per", "10")), shortN = int.Parse(Arg(args, "--short", "15"));
        string model = Arg(args, "--model", "claude-haiku-5-5");
        string outPath = Arg(args, "--out", Path.Combine(runs.Length > 0 ? runs[0] : ".", "checktime.jsonl"));
        var picked = new List<(string card, string line, List<(string id, string text)> known)>();
        foreach (var card in new[] { "lena", "rocco", "sam" })
        {
            var mine = new List<(string, string, List<(string, string)>)>();
            foreach (var run in runs)
                foreach (var row in File.ReadAllLines(Path.Combine(run, "firsts.jsonl")).Where(l => l.Trim().Length > 0))
                {
                    using var d = JsonDocument.Parse(row);
                    var r = d.RootElement;
                    if (r.GetProperty("card").GetString() != card) continue;
                    var steps = r.GetProperty("steps").EnumerateArray().Select(s => s.GetProperty("step").GetString()).ToList();
                    if (!steps.Contains("first-passed")) continue;
                    string reply = r.GetProperty("reply").GetString() ?? "";
                    string first = System.Text.RegularExpressions.Regex.Split(reply.Trim(), @"(?<=[.!?])\s+")[0];
                    if (first.Length == 0) continue;
                    var known = r.GetProperty("known").EnumerateArray().Select(k => k.GetString()).Select(k =>
                    {
                        int c = k.IndexOf(": ", StringComparison.Ordinal);
                        return c > 0 ? (k.Substring(0, c), k.Substring(c + 2)) : ("?", k);
                    }).ToList();
                    if (mine.All(m => m.Item2 != first)) mine.Add((card, first, known));
                }
            picked.AddRange(mine.Take(per));
        }
        using var client = (IDisposable)BenchClient(args, "the first sentence's check timed, its whole facts list and its first " + shortN);
        var llm = (ILlmClient)client;
        var rows = new List<object>();
        int i = 0;
        foreach (var (card, line, known) in picked)
        {
            var conditions = new List<(string name, List<(string, string)> items)> { ("whole", known), ("short", known.Take(shortN).ToList()) };
            if (i++ % 2 == 1) conditions.Reverse();
            foreach (var (name, items) in conditions)
            {
                var req = ClaimCheck.RequestItems(model, ClaimCheck.NumberedKnown(items), line);
                var sw = Stopwatch.StartNew();
                LlmResponse resp;
                try { resp = await llm.CompleteAsync(req); }
                catch (Exception e) { Console.WriteLine("call failed: " + e.Message); continue; }
                sw.Stop();
                int listed = 0;
                try
                {
                    var t = resp.Text ?? "";
                    int a = t.IndexOf('{'), b = t.LastIndexOf('}');
                    if (a >= 0 && b > a)
                    {
                        using var j = JsonDocument.Parse(t.Substring(a, b - a + 1));
                        if (j.RootElement.TryGetProperty("specifics", out var sp)) listed = sp.GetArrayLength();
                    }
                }
                catch (JsonException) { }
                rows.Add(new { card, line, condition = name, items = items.Count, chars = items.Sum(x => x.Item2.Length), ms = sw.ElapsedMilliseconds,
                               inTokens = resp.InputTokens, outTokens = resp.OutputTokens, listed });
                Console.WriteLine($"{card} {name,-5} items={items.Count} ms={sw.ElapsedMilliseconds} in={resp.InputTokens} out={resp.OutputTokens} listed={listed} | {line}");
            }
        }
        WriteJsonl(outPath, rows);
        LogKeyRun(picked.Count * 2);
        return 0;
    }
}
