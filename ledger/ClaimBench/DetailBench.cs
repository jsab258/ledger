using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Json;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;
using Ledger.DevTools;

/// THE DETAIL BENCH (Jafar's list of 30 September afternoon, item 3; the
/// research note grounded-dialogue-selection, step 2): the check's judgement
/// of one detail against what the character knows, tuned on labelled details
/// and confirmed on questions it was never tuned on.
///   detailbench build --from dir1,dir2 --dir out   the details: every one the
///       check refused in those runs, a sample of those it passed (listed by
///       its own first look), and inventions planted by changing one number or
///       name of a passed one
///   detailbench label --dir out   two labellers apart, blind to the check:
///       stated, implied, added, contradicted or no claim, with the kind; a
///       third where they differ on supported or not; each question to the
///       tuning half or the held-out half
///   detailbench eval --variant v0 --dir out   a version of the judgement on
///       every labelled detail: how often it refuses a true one, and how often
///       it passes an invented one, on each half
static partial class Program
{
    sealed class DetailRow
    {
        public string Id, Card, Probe, Detail, Origin, Reply;
        public List<string> Known = new List<string>();
        public string Label, Kind, Half;
    }

    static async Task<int> DetailBench(string[] args, string dir, int parallel)
    {
        string sub = args.Length > 1 ? args[1] : "";
        Directory.CreateDirectory(dir);
        switch (sub)
        {
            case "build": return await DetailBuild(dir, Arg(args, "--from", ""), parallel);
            case "label": return await DetailLabel(dir, parallel, Arg(args, "--third", "claude-fable-5-1"));
            case "eval": return await DetailEval(dir, Arg(args, "--variant", "v0"), parallel);
        }
        Console.WriteLine("detailbench build --from dir1,dir2 | label | eval --variant v0|v1|v2|v3  (--dir out)");
        return 1;
    }

    static List<string> JsonList(JsonElement r, string name) =>
        r.TryGetProperty(name, out var v) && v.ValueKind == JsonValueKind.Array
            ? v.EnumerateArray().Where(x => x.ValueKind == JsonValueKind.String).Select(x => x.GetString()).ToList() : new List<string>();

    static string Numbered(List<string> known) => string.Join("\n", known) + "\n";

    // Every specific the check's first look lists for a line, with whether it
    // cited an item that exists.
    static List<(string detail, string kind, bool cited)> FirstLook(string answer, List<string> known)
    {
        var ids = new HashSet<string>(known.Select(k => k.Split(new[] { ": " }, 2, StringSplitOptions.None)[0]));
        var list = new List<(string, string, bool)>();
        int a = answer.IndexOf('{'), b = answer.LastIndexOf('}');
        if (a < 0 || b <= a) return list;
        try
        {
            using var d = JsonDocument.Parse(answer.Substring(a, b - a + 1));
            if (!d.RootElement.TryGetProperty("specifics", out var sp) || sp.ValueKind != JsonValueKind.Array) return list;
            foreach (var x in sp.EnumerateArray())
            {
                if (x.ValueKind != JsonValueKind.Object) continue;
                string detail = x.TryGetProperty("detail", out var dt) && dt.ValueKind == JsonValueKind.String ? dt.GetString() : null;
                if (string.IsNullOrWhiteSpace(detail)) continue;
                string kind = x.TryGetProperty("kind", out var k) && k.ValueKind == JsonValueKind.String ? k.GetString() : "";
                string src = x.TryGetProperty("source", out var s) && s.ValueKind == JsonValueKind.String ? s.GetString() : "none";
                bool cited = src.Split(new[] { ',', ' ' }, StringSplitOptions.RemoveEmptyEntries).Any(ids.Contains);
                list.Add((detail.Trim(), kind, cited));
            }
        }
        catch (JsonException) { }
        return list;
    }

    // An invention planted in a passed detail: one number or one name changed.
    static readonly string[][] Swaps =
    {
        new[] { "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven", "twelve" },
        new[] { "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday" },
        new[] { "Ron", "Sheila", "Darren", "June", "Rita", "Hal", "Ada", "Father Walsh" },
        new[] { "morning", "evening", "night", "afternoon" },
    };

    static string Plant(string detail, int salt)
    {
        var m = Regex.Match(detail, @"\b\d+\b");
        if (m.Success) return detail.Substring(0, m.Index) + (int.Parse(m.Value) + 1 + salt % 3) + detail.Substring(m.Index + m.Length);
        foreach (var set in Swaps)
            for (int i = 0; i < set.Length; i++)
            {
                var w = Regex.Match(detail, @"\b" + Regex.Escape(set[i]) + @"\b", RegexOptions.IgnoreCase);
                if (!w.Success) continue;
                string other = set[(i + 1 + salt % (set.Length - 1)) % set.Length];
                if (char.IsLower(w.Value[0])) other = other.ToLowerInvariant();
                return detail.Substring(0, w.Index) + other + detail.Substring(w.Index + w.Length);
            }
        return null;
    }

    static async Task<int> DetailBuild(string dir, string from, int parallel)
    {
        var refused = new List<DetailRow>();
        var passedLines = new List<(string card, string probe, string reply, List<string> known)>();
        foreach (var run in from.Split(',', StringSplitOptions.RemoveEmptyEntries))
        {
            var path = Path.Combine(run.Trim(), "firsts.jsonl");
            if (!File.Exists(path)) { Console.WriteLine("no run at " + path); return 1; }
            foreach (var line in File.ReadAllLines(path))
            {
                if (string.IsNullOrWhiteSpace(line)) continue;
                using var d = JsonDocument.Parse(line);
                var r = d.RootElement;
                var known = JsonList(r, "known");
                if (known.Count == 0) continue;
                string card = r.GetProperty("card").GetString(), probe = r.GetProperty("probe").GetString(), reply = r.GetProperty("reply").GetString();
                foreach (var det in JsonList(r, "invented").Concat(JsonList(r, "refusedAgain")))
                    if (!det.StartsWith("(", StringComparison.Ordinal))
                        refused.Add(new DetailRow { Card = card, Probe = probe, Detail = det, Origin = "refused", Known = known });
                bool fell = r.GetProperty("fell").GetBoolean();
                bool plain = r.TryGetProperty("saidPlainly", out var sp) && sp.ValueKind == JsonValueKind.True;
                if (!fell && !plain) passedLines.Add((card, probe, reply, known));
            }
        }
        // The details of the lines it passed, as its own first look lists them.
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        var passed = new List<DetailRow>();
        await Task.WhenAll(passedLines.Select(async x =>
        {
            await gate.WaitAsync();
            try
            {
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var ans = (await client.CompleteAsync(ClaimCheck.RequestItems(Models.Ambient, Numbered(x.known), x.reply))).Text;
                        lock (passed)
                            foreach (var (det, kind, _) in FirstLook(ans, x.known))
                                passed.Add(new DetailRow { Card = x.card, Probe = x.probe, Detail = det, Origin = "passed", Known = x.known, Reply = x.reply });
                        break;
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
            }
            finally { gate.Release(); }
        }));
        var rng = new Random(20260930);
        List<DetailRow> Distinct(IEnumerable<DetailRow> rows) =>
            rows.GroupBy(r => r.Card + "|" + r.Probe + "|" + r.Detail.ToLowerInvariant()).Select(g => g.First()).ToList();
        List<DetailRow> Sample(List<DetailRow> rows, int n) => rows.OrderBy(_ => rng.Next()).Take(n).ToList();
        var bench = new List<DetailRow>();
        bench.AddRange(Sample(Distinct(refused), 130));
        var passedSample = Sample(Distinct(passed), 90);
        bench.AddRange(passedSample);
        int salt = 0;
        foreach (var p in Distinct(passed).OrderBy(_ => rng.Next()))
        {
            if (bench.Count(r => r.Origin == "planted") >= 35) break;
            var planted = Plant(p.Detail, salt++);
            if (planted == null || planted == p.Detail) continue;
            bench.Add(new DetailRow { Card = p.Card, Probe = p.Probe, Detail = planted, Origin = "planted", Known = p.Known, Reply = p.Reply });
        }
        for (int i = 0; i < bench.Count; i++) bench[i].Id = "d" + (i + 1).ToString("000");
        WriteJsonl(Path.Combine(dir, "detail-bench.jsonl"), bench.Select(r => new { id = r.Id, card = r.Card, probe = r.Probe, detail = r.Detail, origin = r.Origin, known = r.Known }));
        Console.WriteLine($"detailbench build: {bench.Count} details ({bench.Count(r => r.Origin == "refused")} refused, {bench.Count(r => r.Origin == "passed")} passed, " +
                          $"{bench.Count(r => r.Origin == "planted")} planted) from {refused.Count} refused and {passed.Count} passed -> detail-bench.jsonl");
        return 0;
    }

    static List<DetailRow> ReadDetails(string path)
    {
        var rows = new List<DetailRow>();
        foreach (var line in File.ReadAllLines(path))
        {
            if (string.IsNullOrWhiteSpace(line)) continue;
            using var d = JsonDocument.Parse(line);
            var r = d.RootElement;
            string S(string n) => r.TryGetProperty(n, out var v) && v.ValueKind == JsonValueKind.String ? v.GetString() : null;
            rows.Add(new DetailRow { Id = S("id"), Card = S("card"), Probe = S("probe"), Detail = S("detail"), Origin = S("origin"), Known = JsonList(r, "known"),
                                     Label = S("label"), Kind = S("kind"), Half = S("half") });
        }
        return rows;
    }

    const string DetailRule =
        "You judge one detail a character in a small British port town in 1990 said, against everything they know, given as numbered items. " +
        "Label it: \"stated\" (an item says it, in any words); \"implied\" (a plain listener would take an item to mean the same thing, or it " +
        "follows directly from one); \"added\" (it gives something no item gives: a name, time, day, place, number, colour, size, manner, " +
        "habit, deed or happening); \"contradicted\" (an item says otherwise); \"noclaim\" (it states nothing that could be true or false: a " +
        "feeling, an opinion, a greeting). Also give its kind: name, number, time, day, place, vehicle, person, event, manner, habit, object " +
        "or other. Answer with JSON only: {\"label\": \"stated\", \"kind\": \"event\", \"item\": \"H3\"}.";

    static bool? Supported(string label) =>
        label == "stated" || label == "implied" ? true : label == "added" || label == "contradicted" ? false : (bool?)null;

    static async Task<int> DetailLabel(string dir, int parallel, string third)
    {
        var rows = ReadDetails(Path.Combine(dir, "detail-bench.jsonl"));
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        async Task<(string label, string kind)> One(string model, DetailRow r)
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = model, MaxTokens = 200, System = DetailRule };
                req.Messages.Add(new LlmMessage("user", "WHAT THEY KNOW:\n" + Numbered(r.Known) + "\nTHE DETAIL:\n" + r.Detail));
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var text = (await client.CompleteAsync(req)).Text;
                        int a = text.IndexOf('{'), b = text.LastIndexOf('}');
                        using var d = JsonDocument.Parse(text.Substring(a, b - a + 1));
                        var l = d.RootElement.GetProperty("label").GetString().Trim().ToLowerInvariant();
                        var k = d.RootElement.TryGetProperty("kind", out var kk) && kk.ValueKind == JsonValueKind.String ? kk.GetString().Trim().ToLowerInvariant() : "other";
                        if (new[] { "stated", "implied", "added", "contradicted", "noclaim" }.Contains(l)) return (l, k);
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return (null, null);
            }
            finally { gate.Release(); }
        }
        var a1 = await Task.WhenAll(rows.Select(r => One(Labellers[0], r)));
        var a2 = await Task.WhenAll(rows.Select(r => One(Labellers[1], r)));
        var need = Enumerable.Range(0, rows.Count).Where(i => a1[i].label == null || a2[i].label == null || Supported(a1[i].label) != Supported(a2[i].label)).ToList();
        var a3 = new Dictionary<int, (string label, string kind)>();
        foreach (var (i, l) in await Task.WhenAll(need.Select(async i => (i, await One(third, rows[i]))))) a3[i] = l;
        // Each question wholly to one half, so the check is confirmed on questions it never saw.
        string HalfOf(string probe)
        {
            uint h = 2166136261;
            foreach (char c in probe ?? "") { h ^= c; h *= 16777619; }
            return h % 2 == 0 ? "tune" : "held";
        }
        var outRows = new List<object>();
        for (int i = 0; i < rows.Count; i++)
        {
            var (label, kind) = a3.TryGetValue(i, out var t) && t.label != null ? t : a1[i].label != null ? a1[i] : a2[i];
            outRows.Add(new { id = rows[i].Id, card = rows[i].Card, probe = rows[i].Probe, detail = rows[i].Detail, origin = rows[i].Origin, known = rows[i].Known,
                              label, kind, half = HalfOf(rows[i].Probe), labels = new[] { a1[i].label, a2[i].label, a3.TryGetValue(i, out var t3) ? t3.label : null } });
        }
        WriteJsonl(Path.Combine(dir, "detail-gold.jsonl"), outRows);
        var labels = outRows.Select(o => (string)o.GetType().GetProperty("label").GetValue(o)).ToList();
        Console.WriteLine($"detailbench label: {rows.Count} details; supported {labels.Count(l => Supported(l) == true)}, unsupported {labels.Count(l => Supported(l) == false)}, " +
                          $"no claim {labels.Count(l => l == "noclaim")}, unread {labels.Count(l => l == null)}; the third settled {a3.Count} -> detail-gold.jsonl");
        return 0;
    }

    // VERSIONS OF THE JUDGEMENT. v0 is today's second look. v1 lets code decide
    // first: a closed-class specific (a number, day, clock time or name) that
    // no item carries is refused, and a detail stated in so many words in an
    // item is cleared (ClaimCheck.StatedIn); the rest go to today's second look.
    // v2 is v1 with the second look shown worked examples from the tuning half
    // only. v3 is v2 looked at twice, refused only when both looks refuse.
    // A number, a day or a clock time: code's to judge (the note: closed-class
    // specifics match a value in what they know, or they do not).
    static readonly Regex ClosedClass = new Regex(
        @"\b(\d+|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|twenty|thirty|forty|fifty|hundred|" +
        @"monday|tuesday|wednesday|thursday|friday|saturday|sunday)\b", RegexOptions.Compiled | RegexOptions.IgnoreCase);
    // What may sit round them in a detail that is only a time, a day or a count.
    static readonly HashSet<string> TimeGlue = new HashSet<string>(StringComparer.OrdinalIgnoreCase)
    {
        "a", "an", "the", "of", "at", "in", "on", "by", "and", "or", "to", "till", "until", "from", "past", "half", "quarter", "o'clock",
        "morning", "mornings", "evening", "evenings", "night", "nights", "afternoon", "afternoons", "day", "days", "week", "weeks", "year", "years", "ago", "back", "every",
    };

    static bool? ByCode(DetailRow r)
    {
        string knownText = string.Join(" ", r.Known).ToLowerInvariant();
        var values = ClosedClass.Matches(r.Detail).Select(m => m.Value.ToLowerInvariant()).ToList();
        if (values.Count == 0) return null;
        // A count, day or time no item carries is refused.
        if (values.Any(v => !Regex.IsMatch(knownText, @"\b" + Regex.Escape(v) + @"\b"))) return false;
        // A detail that is only such values is cleared; anything more is the model's.
        var rest = ClosedClass.Replace(r.Detail, " ").Split(new[] { ' ', ',', '.', '-' }, StringSplitOptions.RemoveEmptyEntries);
        return rest.All(w => TimeGlue.Contains(w)) ? true : (bool?)null;
    }

    static string TuningExamples(List<DetailRow> tune, int n)
    {
        // Balanced: true paraphrases it tends to refuse (implied first) and real
        // additions it must still stop, from the tuning half only.
        var sb = new StringBuilder("Examples from this town's own details, each a DETAIL and its label: ");
        var yes = tune.Where(r => r.Label == "implied").Concat(tune.Where(r => r.Label == "stated")).OrderBy(r => r.Label == "implied" ? 0 : 1).ThenBy(r => r.Id).Take(n / 2);
        var no = tune.Where(r => Supported(r.Label) == false).OrderBy(r => r.Id).Take(n - n / 2);
        foreach (var r in yes.Concat(no))
            sb.Append("\"" + r.Detail + "\" is " + (Supported(r.Label) == true ? "supported" : "not supported") + " (" + r.Label + "). ");
        return sb.ToString();
    }

    static async Task<int> DetailEval(string dir, string variant, int parallel)
    {
        var rows = ReadDetails(Path.Combine(dir, "detail-gold.jsonl")).Where(r => Supported(r.Label) != null).ToList();
        var tune = rows.Where(r => r.Half == "tune").ToList();
        string examples = variant == "v2" || variant == "v3" ? TuningExamples(tune, 12) : null;
        using var client = new ClaudeCodeClient();
        var gate = new SemaphoreSlim(parallel);
        async Task<bool?> Look(DetailRow r)
        {
            await gate.WaitAsync();
            try
            {
                var ids = r.Known.Select(k => k.Split(new[] { ": " }, 2, StringSplitOptions.None)[0]).ToList();
                var req = ClaimCheck.RequestVerify(Models.Ambient, Numbered(r.Known), new[] { r.Detail });
                // v2 and v3: today's examples, drawn from the questions it is tested on,
                // give way to examples from the tuning half.
                if (examples != null)
                {
                    int a = req.System.IndexOf("Examples, each a DETAIL", StringComparison.Ordinal), b = req.System.IndexOf("Answer with JSON only", StringComparison.Ordinal);
                    req.System = a >= 0 && b > a ? req.System.Substring(0, a) + examples + " " + req.System.Substring(b) : req.System + " " + examples;
                }
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var v = ClaimCheck.ParseVerify((await client.CompleteAsync(req)).Text, 1, ids);
                        if (v != null) return v[0];
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return null;
            }
            finally { gate.Release(); }
        }
        var verdicts = await Task.WhenAll(rows.Select(async r =>
        {
            if (variant != "v0" && ByCode(r) is bool code) return (bool?)code;
            var first = await Look(r);
            if (variant == "v3" && first == false) { var second = await Look(r); return second == true ? true : first; }
            return first;
        }));
        var outRows = rows.Select((r, i) => new { r.Id, r.Half, r.Label, r.Origin, gold = Supported(r.Label), passed = verdicts[i] }).ToList();
        WriteJsonl(Path.Combine(dir, "detail-eval." + variant + ".jsonl"), outRows);
        foreach (var half in new[] { "tune", "held" })
        {
            var h = outRows.Where(o => o.Half == half && o.passed != null).ToList();
            int trueN = h.Count(o => o.gold == true), falseN = h.Count(o => o.gold == false);
            int refusedTrue = h.Count(o => o.gold == true && o.passed == false), passedFalse = h.Count(o => o.gold == false && o.passed == true);
            Console.WriteLine($"detailbench eval {variant} {half}: true details refused {refusedTrue}/{trueN} ({(trueN > 0 ? 100.0 * refusedTrue / trueN : 0):0}%), " +
                              $"invented passed {passedFalse}/{falseN} ({(falseN > 0 ? 100.0 * passedFalse / falseN : 0):0}%), unread {outRows.Count(o => o.Half == half && o.passed == null)}");
        }
        return 0;
    }
}
