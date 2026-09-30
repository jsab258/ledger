using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Ledger.DevTools;

/// DOES THE PLAIN LINE ANSWER HIM? (Jafar's list of 30 September afternoon,
/// item 2, measured under item 5): for every reply in the given labelled runs
/// that was the chosen facts said plainly, the two labellers apart say
/// whether it answers what he said, answers part of it, or is beside the
/// point; where they differ the lower reading stands. Prints the counts per
/// run and in all.
static partial class Program
{
    const string RelevanceRule =
        "You judge whether a character's reply answers what the other person said to them. Answer with one word only: " +
        "\"answers\" (it gives what he asked or responds to what he said), \"partly\" (it gives some of it, or something plainly " +
        "related), \"declines\" (it says they do not know, or will not say, and gives nothing else), or \"beside\" (it is about " +
        "something else and leaves what he asked unanswered).";

    static async Task<int> PlainRelevance(string dirs, int parallel, bool all = false)
    {
        var rows = new List<(string run, string card, string probe, string reply, string answerable)>();
        foreach (var run in dirs.Split(',', StringSplitOptions.RemoveEmptyEntries))
        {
            var path = Path.Combine(run.Trim(), "firsts-labelled.jsonl");
            if (!File.Exists(path)) { Console.WriteLine("no labelled run at " + path); return 1; }
            foreach (var line in File.ReadAllLines(path))
            {
                if (string.IsNullOrWhiteSpace(line)) continue;
                using var d = JsonDocument.Parse(line);
                var r = d.RootElement;
                if (!all && !(r.TryGetProperty("saidPlainly", out var sp) && sp.ValueKind == JsonValueKind.True)) continue;
                string ans = r.TryGetProperty("answerable", out var a) && a.ValueKind == JsonValueKind.String ? a.GetString() : null;
                rows.Add((Path.GetFileName(run.Trim().TrimEnd('/', '\\')), r.GetProperty("card").GetString(), r.GetProperty("probe").GetString(), r.GetProperty("reply").GetString(), ans));
            }
        }
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        async Task<string> One(string model, int i)
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = model, MaxTokens = 10, System = RelevanceRule };
                req.Messages.Add(new LlmMessage("user", "HE SAID:\n" + rows[i].probe + "\n\nTHE REPLY:\n" + rows[i].reply));
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var t = (await client.CompleteAsync(req)).Text.Trim().ToLowerInvariant();
                        foreach (var w in new[] { "answers", "partly", "declines", "beside" }) if (t.Contains(w)) return w;
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return null;
            }
            finally { gate.Release(); }
        }
        var a1 = await Task.WhenAll(Enumerable.Range(0, rows.Count).Select(i => One(Labellers[0], i)));
        var a2 = await Task.WhenAll(Enumerable.Range(0, rows.Count).Select(i => One(Labellers[1], i)));
        // Where they differ the lower reading stands: answers, partly, declines, beside.
        int Rank(string w) => w == "answers" ? 3 : w == "partly" ? 2 : w == "declines" ? 1 : w == "beside" ? 0 : -1;
        var final = Enumerable.Range(0, rows.Count).Select(i =>
        {
            int x = Rank(a1[i]), y = Rank(a2[i]);
            int m = x < 0 ? y : y < 0 ? x : Math.Min(x, y);
            return m == 3 ? "answers" : m == 2 ? "partly" : m == 1 ? "declines" : m == 0 ? "beside" : "unread";
        }).ToList();
        var outRows = rows.Select((r, i) => new { r.run, r.card, r.probe, r.answerable, r.reply, relevance = final[i], labels = new[] { a1[i], a2[i] } }).ToList();
        WriteJsonl(Path.Combine(Path.GetDirectoryName(dirs.Split(',')[0].Trim().TrimEnd('/', '\\')) ?? ".", all ? "reply-relevance.jsonl" : "plain-relevance.jsonl"), outRows);
        foreach (var g in outRows.GroupBy(o => o.run))
            Console.WriteLine($"relevance {g.Key}: {g.Count()} lines; where they could answer: answers {g.Count(o => o.answerable != "no" && o.relevance == "answers")}, " +
                              $"partly {g.Count(o => o.answerable != "no" && o.relevance == "partly")}, declines {g.Count(o => o.answerable != "no" && o.relevance == "declines")}, " +
                              $"beside {g.Count(o => o.answerable != "no" && o.relevance == "beside")}; where nobody could: declines {g.Count(o => o.answerable == "no" && o.relevance == "declines")}, " +
                              $"other {g.Count(o => o.answerable == "no" && o.relevance != "declines")}");
        Console.WriteLine($"plain relevance, all: {outRows.Count}; answers {outRows.Count(o => o.relevance == "answers")}, partly {outRows.Count(o => o.relevance == "partly")}, " +
                          $"beside the point {outRows.Count(o => o.relevance == "beside")}, unread {outRows.Count(o => o.relevance == "unread")}");
        return 0;
    }
}
