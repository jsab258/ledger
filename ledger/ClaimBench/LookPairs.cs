using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Ledger.Core;

/// IS A SLOW CHECK CALL SLOW FOR BOTH OF TWO COPIES? (27 October 2026, his speech order: the check's own time.) A
/// hedged request (Dean and Barroso, "The Tail at Scale", CACM February 2013: a second copy sent after a short delay,
/// the first answer used) cuts the slow tail only when the slowness does not fall on both copies at once.
///
///     dotnet run --project ledger/ClaimBench -c Release -- lookpairs --key --task slow-replies-2026-10-26
///         --from AB.jsonl --test F:/LedgerTools/checkers/train3/TEST3.json [--limit N] [--out OUT.jsonl]
///
/// Takes the sentences of a `sentcheck --ab-early` run (AB.jsonl), each with its numbered facts from the test file.
/// For each, the check's list (ClaimCheck.RequestItems) is streamed twice at the same moment; then each detail the
/// run refused (its switch-off column) has its second look (ClaimCheck.RequestVerify, exactly as the check asks it)
/// streamed twice at the same moment. Each copy's first words (the moment a hedge would choose on, before any of the
/// answer can be read) and its end are timed, and each look's verdict kept, so the pairs show how often one copy is
/// slow while the other is not, and whether the copy that starts first leans to one verdict. Since the fresh review of
/// 27 October each copy's begin is kept too: the moment the model takes it up, its thinking included, before any of
/// its answer exists, which is what ClaimCheck.TwoCopies now races on.
static partial class Program
{
    static async Task<int> LookPairs(string[] args)
    {
        string from = Arg(args, "--from", ""), test = Arg(args, "--test", "F:/LedgerTools/checkers/train3/TEST3.json");
        int limit = int.Parse(Arg(args, "--limit", "0"));
        string outPath = Arg(args, "--out", Path.Combine(Path.GetDirectoryName(from) ?? ".", "lookpairs.jsonl"));
        const string model = "claude-haiku-5-5";
        var known = new Dictionary<string, List<(string, string)>>();
        using (var doc = JsonDocument.Parse(File.ReadAllText(test)))
            foreach (var e in doc.RootElement.EnumerateArray())
                known[e.GetProperty("key").GetString()] = e.GetProperty("context").EnumerateArray().Select(x => x.GetString()).Select(k =>
                {
                    int c = k.IndexOf(": ", StringComparison.Ordinal);
                    return c > 0 ? (k.Substring(0, c), k.Substring(c + 2)) : ("?", k);
                }).ToList();
        var sentences = new List<(string key, string sentence, List<string> refused)>();
        foreach (var line in File.ReadAllLines(from).Where(l => l.Trim().Length > 0))
        {
            using var d = JsonDocument.Parse(line);
            var r = d.RootElement;
            string key = r.GetProperty("key").GetString();
            if (!known.ContainsKey(key)) continue;
            var refused = r.GetProperty("foundOff").EnumerateArray().Select(f => f.GetString())
                           .Where(f => !string.IsNullOrEmpty(f) && f != "(no answer)").ToList();
            sentences.Add((key, r.GetProperty("sentence").GetString(), refused));
        }
        if (limit > 0) sentences = sentences.Take(limit).ToList();
        using var client = (IDisposable)BenchClient(args, "the check's list and refused looks each sent twice at once, " + sentences.Count + " sentences");
        var llm = (IStartingLlmClient)client;
        var rows = new List<object>();
        int failed = 0;

        // A copy's three moments: the model begins it (its thinking included; the moment ClaimCheck.TwoCopies races
        // on), its first words, its end.
        async Task<(long begin, long first, long end, string text)> Timed(LlmRequest request)
        {
            var sw = Stopwatch.StartNew();
            long first = -1, begin = -1;
            var resp = await llm.StreamAsync(request, t => { if (first < 0 && t.Length > 0) first = sw.ElapsedMilliseconds; },
                                             () => { if (begin < 0) begin = sw.ElapsedMilliseconds; });
            return (begin, first, sw.ElapsedMilliseconds, resp.Text ?? "");
        }

        foreach (var (key, sentence, refused) in sentences)
        {
            var numbered = ClaimCheck.NumberedKnown(known[key]);
            var ids = known[key].Select(k => k.Item1).ToList();
            try
            {
                var la = Timed(ClaimCheck.RequestItems(model, numbered, sentence));
                var lb = Timed(ClaimCheck.RequestItems(model, numbered, sentence));
                await Task.WhenAll(la, lb);
                rows.Add(new { key, call = "list", detail = (string)null, begin1 = la.Result.begin, first1 = la.Result.first, end1 = la.Result.end,
                               begin2 = lb.Result.begin, first2 = lb.Result.first, end2 = lb.Result.end, ok1 = (bool?)null, ok2 = (bool?)null });
                Console.WriteLine($"list {la.Result.first,5}/{la.Result.end,5}  {lb.Result.first,5}/{lb.Result.end,5} | {sentence}");
                foreach (var detail in refused)
                {
                    var a = Timed(ClaimCheck.RequestVerify(model, numbered, new[] { detail }));
                    var b = Timed(ClaimCheck.RequestVerify(model, numbered, new[] { detail }));
                    await Task.WhenAll(a, b);
                    bool? Ok(string text) { var v = ClaimCheck.ParseVerify(text, 1, ids.FindAll(x => x[0] != 'P')); return v == null ? (bool?)null : v[0]; }
                    var ok1 = Ok(a.Result.text);
                    var ok2 = Ok(b.Result.text);
                    rows.Add(new { key, call = "look", detail, begin1 = a.Result.begin, first1 = a.Result.first, end1 = a.Result.end,
                                   begin2 = b.Result.begin, first2 = b.Result.first, end2 = b.Result.end, ok1, ok2 });
                    Console.WriteLine($"look {a.Result.first,5}/{a.Result.end,5}  {b.Result.first,5}/{b.Result.end,5} {ok1}/{ok2} | {detail}");
                }
            }
            catch (Exception e) { failed++; Console.WriteLine("failed: " + e.Message); }
        }
        WriteJsonl(outPath, rows);
        Console.WriteLine($"lookpairs: {rows.Count} pairs, {failed} failed -> {outPath}");
        LogKeyRun(sentences.Count);
        return failed > 0 ? 1 : 0;
    }
}
