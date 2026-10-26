using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text.Json;
using System.Threading.Tasks;
using Ledger.Core;

/// A REFUSED FIRST SENTENCE REWRITTEN ALONE, BENCHED BEFORE IT REACHES SPEECH (his answer of 26 October, speech
/// 2: "When one fails, rewrite only that sentence"; production/research/voice-latency/SENTENCE-REPAIR-2026-10-26.md:
/// a repair's pass rate is benched offline before it is wired to speech, thinking off, the refused details named).
///
///     dotnet run --project ledger/ClaimBench -c Release -- repair --key --task slow-replies-2026-10-26
///         [--from F:/LedgerTools/checkers/train/TRAIN.json] [--n 40] [--out OUT.jsonl]
///
/// THE SENTENCES: Gemini 3.8 Flash's first sentences in each character's voice, written for the fast checker's
/// training from the detail bench's tuning contexts only (the held contexts stay that checker's test), with the
/// facts that speaker was given; --n of those Gemini marked unsupported, by a fixed seed. Each goes through the
/// game's own check (ClaimCheck.RequestItems on Haiku 5.5, as the game sets it); the ones it refuses are repaired
/// two ways and each repair checked again the same way:
///   named:       the refused details named, as a repair made after the refusal would be;
///   alongside:   nothing named, as a repair started at the same moment as the check would be (used only if the
///                check refuses), so that a refusal needs one more check instead of a draft and a check.
/// Each call's time is kept. A repair passes only when the check finds nothing it refuses.
static partial class Program
{
    const string RepairModel = "claude-haiku-5-5";
    /// --strict, the second try: only one item's own facts, nothing inferred from who the speaker is.
    static bool Strict;

    static LlmRequest RepairRequest(string numberedKnown, string question, string sentence, IReadOnlyList<string> refused)
    {
        var r = new LlmRequest { Model = RepairModel, MaxTokens = 120, Thinking = "disabled" };
        r.System =
            "You fix one sentence a character in a small British port town in 1990 is about to say aloud. KNOWN is everything " +
            "they know, as numbered items, and nothing else is. " +
            (refused != null
                ? "The sentence states details KNOWN does not support; they are listed under REFUSED. "
                : "The sentence may state details KNOWN does not support. ") +
            (Strict
                ? "Rewrite it so it states only what one KNOWN item says, in that item's own facts: never add a reason, place, " +
                  "time, person, amount or explanation that the items do not give, and nothing you infer from who the speaker is. " +
                  "When in doubt, leave it out; shorter is better. If no item answers what was asked, say in a few words, in the " +
                  "speaker's manner, that they don't know. "
                : "Rewrite it so it states only what KNOWN states or directly implies: take each unsupported detail out, or have " +
                  "the speaker say plainly they don't know it. Keep the speaker's own words, manner and length as far as you can; " +
                  "add nothing new; answer only what was asked. ") +
            (refused != null ? "" : "If it already says only what KNOWN supports, give it back unchanged. ") +
            "Answer with the one sentence only, no quotation marks.";
        r.Messages.Add(new LlmMessage("user", "KNOWN:\n" + numberedKnown + "\nTHEY WERE ASKED: " + question + "\nSENTENCE: " + sentence +
                                              (refused != null ? "\nREFUSED:\n" + string.Join("\n", refused.Select(x => "- " + x)) : "")));
        return r;
    }

    static async Task<int> Repair(string[] args)
    {
        Strict = args.Contains("--strict");
        string from = Arg(args, "--from", "F:/LedgerTools/checkers/train/TRAIN.json");
        int n = int.Parse(Arg(args, "--n", "40"));
        string outPath = Arg(args, "--out", "F:/LedgerTools/town-scratch/slow-replies/repair/repair.jsonl");
        Directory.CreateDirectory(Path.GetDirectoryName(outPath));
        using var doc = JsonDocument.Parse(File.ReadAllText(from));
        var pool = doc.RootElement.EnumerateArray().Where(e => e.GetProperty("labels").ValueKind == JsonValueKind.Array && e.GetProperty("labels").GetArrayLength() > 0)
            .Select(e => (known: e.GetProperty("context").EnumerateArray().Select(x => x.GetString()).ToList(),
                          question: e.GetProperty("question").GetString(), sentence: e.GetProperty("answer").GetString()))
            .ToList();
        var rnd = new Random(1026);
        var picked = pool.OrderBy(_ => rnd.Next()).Take(n).ToList();
        using var client = (IDisposable)BenchClient(args, "a refused first sentence rewritten alone, named and alongside, " + picked.Count + " sentences");
        var llm = (ILlmClient)client;
        var rows = new List<object>();
        int refusedN = 0, namedPass = 0, alongPass = 0;
        foreach (var (knownText, question, sentence) in picked)
        {
            var items = knownText.Select(k =>
            {
                int c = k.IndexOf(": ", StringComparison.Ordinal);
                return c > 0 ? (k.Substring(0, c), k.Substring(c + 2)) : ("?", k);
            }).ToList();
            var numbered = ClaimCheck.NumberedKnown(items);
            var ids = items.Select(i => i.Item1).ToList();
            async Task<(IReadOnlyList<string> found, long ms)> Check(string line)
            {
                var sw = Stopwatch.StartNew();
                var resp = await llm.CompleteAsync(ClaimCheck.RequestItems(RepairModel, numbered, line));
                return (ClaimCheck.ParseItems(resp.Text, ids), sw.ElapsedMilliseconds);
            }
            async Task<(string text, long ms)> Fix(IReadOnlyList<string> refused)
            {
                var sw = Stopwatch.StartNew();
                var resp = await llm.CompleteAsync(RepairRequest(numbered, question, sentence, refused));
                return ((resp.Text ?? "").Trim().Trim('"'), sw.ElapsedMilliseconds);
            }
            try
            {
                var first = await Check(sentence);
                if (first.found.Count == 0)
                {
                    rows.Add(new { question, sentence, refused = false, checkMs = first.ms });
                    continue;
                }
                refusedN++;
                var named = await Fix(first.found);
                var namedCheck = await Check(named.text);
                var along = await Fix(null);
                var alongCheck = await Check(along.text);
                if (namedCheck.found.Count == 0) namedPass++;
                if (alongCheck.found.Count == 0) alongPass++;
                rows.Add(new { question, sentence, refused = true, found = first.found, checkMs = first.ms,
                               named = named.text, namedMs = named.ms, namedFound = namedCheck.found, namedCheckMs = namedCheck.ms,
                               alongside = along.text, alongsideMs = along.ms, alongsideFound = alongCheck.found, alongsideCheckMs = alongCheck.ms });
                Console.WriteLine($"refused: {sentence}\n   named ({(namedCheck.found.Count == 0 ? "pass" : "refused")}): {named.text}\n   alongside ({(alongCheck.found.Count == 0 ? "pass" : "refused")}): {along.text}");
            }
            catch (Exception e) { Console.WriteLine("failed: " + e.Message); }
        }
        WriteJsonl(outPath, rows);
        Console.WriteLine($"repair: {picked.Count} sentences, the check refused {refusedN}; repaired and passed: named {namedPass}/{refusedN}, alongside {alongPass}/{refusedN} -> {outPath}");
        LogKeyRun(picked.Count);
        return 0;
    }
}
