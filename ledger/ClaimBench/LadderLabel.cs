using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Ledger.DevTools;

/// THE LADDER, LABELLED (the talk task of 7 October 2026): for one `firsts
/// --ladder` run, the question bench's fixed labels say where the character
/// could answer (firsts-answerable*.jsonl and the rulings, labelled 30 September
/// by two labellers and a third, before the ladder existed), and the two
/// labellers apart judge every line the ladder said: whether it answers him
/// (answers, partly, declines, beside the point; the lower reading stands), and
/// whether it states anything the character does not know (invented only when
/// both find a detail, as the bench has always counted).
///
///     ladder-label [--set held] --dir <the run>    -> ladder-labelled.jsonl
static partial class Program
{
    sealed class LadderRow
    {
        public string card { get; set; }
        public string probe { get; set; }
        public string reply { get; set; }
        public string before { get; set; }
        public bool beforeFell { get; set; }
        public bool empty { get; set; }
        public string rung { get; set; }
        public bool fell { get; set; }
    }

    static Dictionary<string, string> AnswerableLabels()
    {
        var benchDir = Path.Combine(RepoRoot(), "production", "research", "invented-claims", "bench");
        var answerable = new Dictionary<string, string>();
        foreach (var line in File.ReadAllLines(Path.Combine(benchDir, "firsts-answerable" + SetSuffix + ".jsonl")))
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            using var d = JsonDocument.Parse(line);
            var r = d.RootElement;
            answerable[r.GetProperty("card").GetString() + "|" + r.GetProperty("probe").GetString()] =
                r.TryGetProperty("gold", out var g) && g.ValueKind == JsonValueKind.String ? g.GetString() : null;
        }
        var rulings = Path.Combine(benchDir, "firsts-answerable-rulings" + SetSuffix + ".json");
        if (File.Exists(rulings))
            using (var rd = JsonDocument.Parse(File.ReadAllText(rulings)))
                foreach (var p in rd.RootElement.EnumerateObject()) answerable[p.Name] = p.Value.GetString();
        return answerable;
    }

    static async Task<int> LadderLabel(string dir, int parallel)
    {
        var rows = ReadJsonl<LadderRow>(Path.Combine(dir, "firsts.jsonl")).ToList();
        var answerable = AnswerableLabels();
        var said = rows.Where(r => r.rung == "fact" || r.rung == "ask" || r.rung == "told").ToList();
        var known = new Dictionary<string, string>();
        foreach (var c in rows.Select(r => r.card).Distinct()) known[c] = FirstsKnown(c);
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        async Task<string> Relevance(string model, LadderRow r)
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = model, MaxTokens = 10, System = RelevanceRule };
                req.Messages.Add(new LlmMessage("user", "HE SAID:\n" + r.probe + "\n\nTHE REPLY:\n" + r.reply));
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
        async Task<int> Invented(string model, LadderRow r)
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = model, MaxTokens = 600, System = LabelRule };
                req.Messages.Add(new LlmMessage("user", "KNOWN:\n" + known[r.card] + "\nTHE OTHER PERSON SAID (not evidence):\n- " + r.probe +
                    "\n\nTHE LINE THE CHARACTER SAID:\n<<<\n" + r.reply + "\n>>>"));
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try { var p = ParseDetails((await client.CompleteAsync(req)).Text); if (p != null) return p.Count; }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return -1;
            }
            finally { gate.Release(); }
        }
        var rel = new List<string[]>();
        var inv = new List<int[]>();
        foreach (var r in said)
        {
            rel.Add(new[] { await Relevance(Labellers[0], r), await Relevance(Labellers[1], r) });
            inv.Add(new[] { await Invented(Labellers[0], r), await Invented(Labellers[1], r) });
        }
        int Rank(string w) => w == "answers" ? 3 : w == "partly" ? 2 : w == "declines" ? 1 : w == "beside" ? 0 : -1;
        var outRows = new List<object>();
        int i = 0;
        var relevance = new Dictionary<LadderRow, string>();
        var invented = new Dictionary<LadderRow, string>();
        foreach (var r in said)
        {
            int x = Rank(rel[i][0]), y = Rank(rel[i][1]);
            int m = x < 0 ? y : y < 0 ? x : Math.Min(x, y);
            relevance[r] = m == 3 ? "answers" : m == 2 ? "partly" : m == 1 ? "declines" : m == 0 ? "beside" : "unread";
            invented[r] = inv[i][0] < 0 || inv[i][1] < 0 ? "unread" : inv[i][0] > 0 && inv[i][1] > 0 ? "invented" : inv[i][0] > 0 || inv[i][1] > 0 ? "disputed" : "grounded";
            i++;
        }
        foreach (var r in rows)
        {
            answerable.TryGetValue(r.card + "|" + r.probe, out var ans);
            outRows.Add(new { r.card, r.probe, answerable = ans, r.rung, r.reply, r.before, r.beforeFell, r.empty,
                              relevance = relevance.TryGetValue(r, out var rv) ? rv : null, invented = invented.TryGetValue(r, out var iv) ? iv : null });
        }
        WriteJsonl(Path.Combine(dir, "ladder-labelled.jsonl"), outRows);
        bool Can(LadderRow r) { answerable.TryGetValue(r.card + "|" + r.probe, out var a); return a == "yes" || a == "partly"; }
        bool Cannot(LadderRow r) { answerable.TryGetValue(r.card + "|" + r.probe, out var a); return a == "no"; }
        int couldN = rows.Count(Can), noneN = rows.Count(Cannot);
        Console.WriteLine($"ladder labelled ({(Set.Length == 0 ? "the sixty" : Set)}): {rows.Count} replies, {couldN} where they could answer, {noneN} where they could not; " +
                          $"empty where they could answer: today {rows.Count(r => Can(r) && r.beforeFell)}, with the ladder {rows.Count(r => Can(r) && r.empty)}; " +
                          $"empty where they could not: today {rows.Count(r => Cannot(r) && r.beforeFell)}, with the ladder {rows.Count(r => Cannot(r) && r.empty)}");
        Console.WriteLine($"  the ladder's {said.Count} lines: answers {said.Count(r => relevance[r] == "answers")}, partly {said.Count(r => relevance[r] == "partly")}, " +
                          $"declines {said.Count(r => relevance[r] == "declines")}, beside the point {said.Count(r => relevance[r] == "beside")}, unread {said.Count(r => relevance[r] == "unread")}; " +
                          $"where they could answer: answers or partly {said.Count(r => Can(r) && (relevance[r] == "answers" || relevance[r] == "partly"))} of {said.Count(Can)}; " +
                          $"where they could not: beside {said.Count(r => Cannot(r) && relevance[r] == "beside")} of {said.Count(Cannot)}; " +
                          $"invented (both labellers) {said.Count(r => invented[r] == "invented")}, disputed {said.Count(r => invented[r] == "disputed")}, unread {said.Count(r => invented[r] == "unread")}");
        return 0;
    }
}
