using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE INVENTED SENTENCES TESTED AT THE SOURCE (his order of 27 October 2026, evening, 2: "Test at the source on the
/// same 617: the reply's instructions say to state only what is in the speaker's facts and to deflect in character
/// otherwise; then a version where each fact carries an ID and the reply names the facts each sentence uses").
///
///     dotnet run --project ledger/ClaimBench -c Release -- source --key --task invented-source-2026-10-27
///         --variant today|facts|cite [--from F:/LedgerTools/checkers/train3/TEST3.json] [--out OUT.jsonl]
///         [--every N] [--drop-every N] [--limit N] [--resume] [--name-rule] --cap DOLLARS --rules --moment [--parallel 4]
///
/// The 617 held first sentences answer 31 questions put to Sheila, Ron and Darren (about 20 answers each, written by
/// Gemini). Here each of the 617 rows asks its question again, as a newcomer's first question, of the game's own reply
/// model with the game's own prompt (built as the firsts mode builds a turn: the card with the street's facts, the
/// people, how they know him, where they stand, Monday 10:00, the model by moment), and keeps the raw first sentence
/// it writes, before any check or rewrite. That sentence then goes through the game's whole check
/// (ClaimCheck.CheckAsync on Haiku 5.5, against the same list the check always reads), unchanged in every variant.
///   today  the prompt as the game builds it;
///   facts  plus the check's own list of what they know, and: say only what it says, deflect in character otherwise;
///   cite   as facts, the list numbered, and each sentence followed by the numbers of the facts it uses in braces,
///          taken off before the sentence is checked.
/// Gemini labels each kept sentence afterwards (tools/checkers/source_test.py), as it labelled the 617.
static partial class Program
{
    const string FactsOnlyRule =
        "Say only what this list says, in your own words. Whatever it does not give, you do not know: deflect in character, " +
        "your own way, and add nothing of your own, no person, place, time or event it does not have.";

    static async Task<int> Source(string[] args, int parallel)
    {
        string variant = Arg(args, "--variant", null);
        if (variant != "today" && variant != "facts" && variant != "cite") { Console.WriteLine("refused: --variant takes today, facts or cite"); return 2; }
        string from = Arg(args, "--from", "F:/LedgerTools/checkers/train3/TEST3.json");
        string outPath = Arg(args, "--out", Path.Combine("F:/LedgerTools/checkers/source", "source-" + variant + ".jsonl"));
        Directory.CreateDirectory(Path.GetDirectoryName(outPath));
        using var doc = JsonDocument.Parse(File.ReadAllText(from));
        var rows = doc.RootElement.EnumerateArray().Select((e, i) => (i, card: e.GetProperty("card").GetString(),
                                                                      question: e.GetProperty("question").GetString(),
                                                                      half: e.TryGetProperty("half", out var hh) ? hh.GetString() : "?")).ToList();
        if (rows.Any(r => r.half != "held")) { Console.WriteLine("refused: a row that is not from the held half"); return 2; }
        int every = int.Parse(Arg(args, "--every", "1"));
        if (every > 1) rows = rows.Where(r => r.i % every == 0).ToList();
        // --drop-every N: rows whose index is N-1 past a multiple of N are left out, the same rows in every variant
        // (his $20 covers about two thirds of the 617 three ways once the facts list lengthens the prompt).
        int dropEvery = int.Parse(Arg(args, "--drop-every", "0"));
        if (dropEvery > 1) rows = rows.Where(r => r.i % dropEvery != dropEvery - 1).ToList();
        int limit = int.Parse(Arg(args, "--limit", "0"));
        if (limit > 0) rows = rows.Take(limit).ToList();
        // --resume: the rows already in the out file are kept and not asked again (27 October: the first runs stopped
        // at the bench's default $1 a run, a third of the way through)
        var kept = new List<string>();
        if (args.Contains("--resume") && File.Exists(outPath))
        {
            kept = File.ReadAllLines(outPath).Where(l => l.Trim().Length > 0).ToList();
            var done = new HashSet<int>(kept.Select(l => JsonDocument.Parse(l).RootElement.GetProperty("row").GetInt32()));
            rows = rows.Where(r => !done.Contains(r.i)).ToList();
            Console.WriteLine($"resume: {done.Count} rows kept, {rows.Count} to ask");
        }
        // The game's own switches, as the firsts runs set them.
        ConversationEngine.ChooseFirst = !args.Contains("--no-choose");
        ConversationEngine.UseRules = args.Contains("--rules");
        // the check as the first runs measured it, before the hard rule on names (27 October night); --name-rule adds it
        ClaimCheck.NameRule = args.Contains("--name-rule");
        bool byMoment = args.Contains("--moment");
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var cost = new CostTracker();
        using var client = (IDisposable)BenchClient(args, "the invented sentences at the source, " + variant + ", " + rows.Count + " first sentences");
        var llm = (ILlmClient)client;
        var now = new GameTime(0, 10, 0);
        var outRows = new List<object>();
        var gate = new SemaphoreSlim(parallel);
        int failed = 0, refused = 0, unformatted = 0;
        await Task.WhenAll(rows.Select(async r =>
        {
            await gate.WaitAsync();
            try
            {
                var card = StreetFacts.AddTo(CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, r.card + ".md"))), r.card);
                var engine = new ConversationEngine(llm, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = llm };
                if (byMoment) engine.Model = TalkMoment.ModelFor(TalkMoment.Of(r.question));
                engine.People = cast.PeopleFor(r.card, 0, 10);
                engine.HowYouKnowHim = new PlayerIdentity().HowTheyKnowHim(true, true, null);
                string where = cast.WhereWords(r.card, 0, 10);
                string scene = "Dry, grey." + (where != null ? " Where you are: " + where + "." : "");
                var system = engine.BuildSystemPrompt(r.question, now, scene);
                var known = engine.KnownForCheck(now, scene);
                var sb = new StringBuilder(system);
                if (variant != "today")
                {
                    sb.AppendLine();
                    sb.AppendLine(variant == "cite" ? "Everything you know, numbered:" : "Everything you know:");
                    foreach (var (id, text) in known) sb.AppendLine(variant == "cite" ? id + ": " + text : "- " + text);
                    sb.AppendLine(FactsOnlyRule);
                    if (variant == "cite")
                        sb.AppendLine("After every sentence you say, put the numbers of the facts it uses in curly braces, like this: " +
                                      "\"That's Mickey's door, that. {C1}\" A sentence that uses none of them (a feeling, a deflection, a question back) " +
                                      "gets {}. The braces are taken off before you are heard, so this overrides the rule against brackets; nothing else " +
                                      "goes in braces.");
                }
                var request = new LlmRequest { Model = engine.Model, System = sb.ToString(), MaxTokens = 150 };
                request.Messages.Add(new LlmMessage("user", r.question));
                var sw = Stopwatch.StartNew();
                var response = await llm.CompleteAsync(request);
                long draftMs = sw.ElapsedMilliseconds;

                string raw = response.Text ?? "";
                string spoken = raw;
                List<string> cited = null;
                bool formatted = true;
                if (variant == "cite")
                {
                    // the first sentence is what stands before the first braces; its numbers are inside them
                    var m = Regex.Match(raw, @"\{([^{}]*)\}");
                    formatted = m.Success;
                    if (m.Success)
                    {
                        cited = m.Groups[1].Value.Split(new[] { ',', ' ' }, StringSplitOptions.RemoveEmptyEntries).ToList();
                        spoken = raw.Substring(0, m.Index);
                    }
                    spoken = Regex.Replace(spoken, @"\{[^{}]*\}", "");
                }
                string first = ConversationEngine.FirstSentence(spoken.Trim()) ?? spoken.Trim();
                if (!formatted) Interlocked.Increment(ref unformatted);
                sw.Restart();
                var (invented, calls) = await ClaimCheck.CheckAsync(llm, "claude-haiku-5-5", known, first, CancellationToken.None);
                bool passed = invented != null && invented.Count == 0;
                if (!passed) Interlocked.Increment(ref refused);
                lock (outRows)
                    outRows.Add(new { row = r.i, r.card, r.question, variant, model = engine.Model, raw, sentence = first, cited, formatted, passed,
                                      found = invented?.ToList() ?? new List<string> { "(no answer)" }, checkCalls = calls.Count,
                                      draftMs, checkMs = sw.ElapsedMilliseconds, known = known.Select(k => k.id + ": " + k.text).ToList() });
            }
            catch (Exception e) { if (Interlocked.Increment(ref failed) <= 3) Console.WriteLine("failed: " + e.GetType().Name + ": " + e.Message); }
            finally { gate.Release(); }
        }));
        WriteJsonl(outPath, outRows.OrderBy(o => (int)o.GetType().GetProperty("row").GetValue(o)));
        if (kept.Count > 0)
        {
            var all = kept.Concat(File.ReadAllLines(outPath).Where(l => l.Trim().Length > 0))
                          .OrderBy(l => JsonDocument.Parse(l).RootElement.GetProperty("row").GetInt32()).ToList();
            File.WriteAllLines(outPath, all);
        }
        Console.WriteLine($"source {variant}: {outRows.Count} first sentences, {refused} refused by the check, {failed} failed" +
                          (variant == "cite" ? $", {unformatted} without braces" : "") + $" -> {outPath}");
        LogKeyRun(outRows.Count, failed > 0 ? failed + " rows failed" : null);
        return failed > 0 ? 1 : 0;
    }
}
