using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Ledger.Core;

/// THE GAME'S OWN CHECK ON THE FAST CHECKER'S ENLARGED TEST (his page answer of 26 October night: "Enlarge the
/// held-out test with a few hundred more invented and true first sentences, labelled by Gemini and spot-checked, so
/// the bar is not decided by one sentence. The bar stays: no more invented details through than Haiku, on that
/// larger test").
///
///     dotnet run --project ledger/ClaimBench -c Release -- sentcheck --key --task slow-replies-2026-10-26
///         --from F:/LedgerTools/checkers/train3/TEST3.json [--out OUT.jsonl] [--limit N]
///
/// Each sentence (written by Gemini 3.8 Flash from the detail bench's HELD contexts, never trained on) goes through
/// the check exactly as the game runs it on a first sentence: ClaimCheck.CheckAsync on Haiku 5.5 with the speaker's
/// numbered facts (the list, the code's word-for-word clearing, the second look). A sentence passes when it names
/// nothing invented. Its time is kept. The checker's own
/// verdicts are added by tools/checkers/sentence_test.py, which lays the two side by side.
static partial class Program
{
    static async Task<int> SentCheck(string[] args)
    {
        string from = Arg(args, "--from", "F:/LedgerTools/checkers/train3/TEST3.json");
        string outPath = Arg(args, "--out", Path.Combine(Path.GetDirectoryName(from), "haiku-verdicts.jsonl"));
        int limit = int.Parse(Arg(args, "--limit", "0"));
        using var doc = JsonDocument.Parse(File.ReadAllText(from));
        var rows = doc.RootElement.EnumerateArray().Select(e => (
                known: e.GetProperty("context").EnumerateArray().Select(x => x.GetString()).ToList(),
                key: e.TryGetProperty("key", out var kk) ? kk.GetString() : "",
                sentence: e.GetProperty("answer").GetString(),
                half: e.TryGetProperty("half", out var hh) ? hh.GetString() : "?"))
            .ToList();
        if (rows.Any(r => r.half != "held")) { Console.WriteLine("refused: a sentence that is not from the held half"); return 2; }
        if (limit > 0) rows = rows.Take(limit).ToList();
        // --history-supports: the check's H items count as an event's support at the list (ClaimCheck.HistorySupports)
        ClaimCheck.HistorySupports = args.Contains("--history-supports");
        using var client = (IDisposable)BenchClient(args, "the game's check on the fast checker's enlarged held test, " + rows.Count + " sentences");
        var llm = (ILlmClient)client;
        var outRows = new List<object>();
        int refused = 0, failed = 0;
        foreach (var r in rows)
        {
            var items = r.known.Select(k =>
            {
                int c = k.IndexOf(": ", StringComparison.Ordinal);
                return c > 0 ? (k.Substring(0, c), k.Substring(c + 2)) : ("?", k);
            }).ToList();
            try
            {
                // THE WHOLE CHECK, AS THE GAME RUNS IT (ConversationEngine.CheckLine = ClaimCheck.CheckAsync): the list,
                // the details stated word for word cleared by code, then a second look at each detail still flagged.
                // The first run of this mode (26 October night) read the list alone, which flags every event not
                // backed by a belief, memory or report (B, M, W items) for the later steps to clear: 552 of 617 read
                // as refused. A null answer (the checker failed or answered out of shape) is refused, as in the game.
                var sw = Stopwatch.StartNew();
                var (invented, calls) = await ClaimCheck.CheckAsync(llm, "claude-haiku-5-5", items, r.sentence, System.Threading.CancellationToken.None);
                bool passed = invented != null && invented.Count == 0;
                if (!passed) refused++;
                outRows.Add(new { r.key, r.sentence, passed, found = invented ?? new List<string> { "(no answer)" }, calls = calls.Count, ms = sw.ElapsedMilliseconds });
            }
            catch (Exception e) { failed++; Console.WriteLine("failed: " + e.Message); }
        }
        WriteJsonl(outPath, outRows);
        Console.WriteLine($"sentcheck: {outRows.Count} sentences checked, {refused} refused, {failed} calls failed -> {outPath}");
        LogKeyRun(outRows.Count);
        return failed > 0 ? 1 : 0;
    }
}
