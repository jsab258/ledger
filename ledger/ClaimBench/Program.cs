using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Linq;
using System.Text;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE BENCH FOR INVENTED FACTS, 28 September (Jafar's town list, item 3: "A
/// character may only say what the simulation knows. Make the check catch it,
/// measured on a set of test conversations, with the failure rate before and
/// after").
///
///     dotnet run --project ledger/ClaimBench -c Release -- generate      # the drafts, no check
///     dotnet run --project ledger/ClaimBench -c Release -- label         # two labellers, independently
///     dotnet run --project ledger/ClaimBench -c Release -- gold          # agreement, and what to settle by hand
///     dotnet run --project ledger/ClaimBench -c Release -- check v2      # a checker on the same drafts
///     dotnet run --project ledger/ClaimBench -c Release -- pipeline v2   # the whole turn, as the game runs it
///
/// AGAINST THE REAL ENGINE: every draft comes from ConversationEngine.SayToAsync
/// with the card, memories and scene the game would send, and what the checker
/// is shown is ClaimCheck.KnownFor, exactly as the engine builds it. The set of
/// conversations is production/research/invented-claims/bench/scenarios.json;
/// everything this writes goes beside it, so a later run can be compared turn
/// for turn (a paired count, as the research advises).
///
/// THE LABELS: two models label each draft independently against one rule (a
/// detail is invented unless what the character knows states it or directly
/// implies it); where they disagree, a person settles it (adjudications.json),
/// and only then is a checker scored. The player's words are shown to the
/// labellers for context and are never evidence.
///
/// THE KEY is read from ANTHROPIC_API_KEY, or else from the game's own secrets
/// file (the AI tester's and the voice tools' source), and never printed.
static class Program
{
    static readonly JsonSerializerOptions Plain = new JsonSerializerOptions { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping };
    static readonly string[] Labellers = { "claude-opus-5-5", "claude-sonnet-5" };

    sealed class Draft
    {
        public string id { get; set; }
        public string card { get; set; }
        public string set { get; set; }
        public string line { get; set; }
        public int turn { get; set; }
        public bool probe { get; set; }
        public List<string> said { get; set; }
        public string reply { get; set; }
        public string known { get; set; }
    }

    sealed class LabelRow
    {
        public string id { get; set; }
        public string model { get; set; }
        public bool parsed { get; set; }
        public List<Detail> invented { get; set; }
    }

    sealed class Detail
    {
        public string detail { get; set; }
        public string kind { get; set; }
    }

    /// Spend at the published rates of 28 September (production/research/invented-claims,
    /// section 5), per million tokens in and out; Models.Cost carries only the game's two.
    static readonly Dictionary<string, (double inPerM, double outPerM)> Rates = new Dictionary<string, (double, double)>
    {
        { "claude-opus-5-5", (4.0, 20.0) }, { "claude-sonnet-5", (2.0, 10.0) }, { "claude-haiku-4-5", (1.0, 5.0) },
    };
    static double _usd;
    static void Spend(string model, int inTok, int outTok)
    {
        if (!Rates.TryGetValue(model, out var r)) return;
        lock (Rates) _usd += inTok / 1e6 * r.inPerM + outTok / 1e6 * r.outPerM;
    }

    static async Task<int> Main(string[] args)
    {
        string mode = args.Length > 0 ? args[0] : "";
        string dir = Arg(args, "--dir", Path.Combine(RepoRoot(), "production", "research", "invented-claims", "bench"));
        int parallel = int.Parse(Arg(args, "--parallel", "6"));
        switch (mode)
        {
            case "generate": return await Generate(dir, parallel);
            case "label": return await LabelAll(dir, parallel);
            case "gold": return Gold(dir);
            case "check": return await Check(dir, args.Length > 1 ? args[1] : "v2", parallel, Arg(args, "--half", "all"));
            case "pipeline": return await Pipeline(dir, args.Length > 1 ? args[1] : "run", parallel, Arg(args, "--checker", "v3v"),
                                                   args.Contains("--early"));
            case "raw":
            {
                // One draft's checker answer as written, for reading why it flagged.
                var d = ReadJsonl<Draft>(Path.Combine(dir, "drafts.jsonl")).First(x => x.id == args[1]);
                using var client = new AnthropicClient(Key());
                var items = ItemsFor(d);
                var known = ClaimCheck.NumberedKnown(items);
                var r = await client.CompleteAsync(ClaimCheck.RequestItems(Models.Ambient, known, d.reply));
                Console.WriteLine(d.reply);
                Console.WriteLine(r.Text);
                // And the second look at what it flagged, with the line and without.
                var flagged = ClaimCheck.ParseItems(r.Text, items.Select(i => i.id).ToList());
                Console.WriteLine("flagged: " + (flagged == null ? "(unreadable)" : string.Join(" | ", flagged)));
                if (flagged != null && flagged.Count > 0)
                {
                    var withLine = await client.CompleteAsync(ClaimCheck.RequestVerify(Models.Ambient, known, flagged, d.reply));
                    Console.WriteLine("second look, shown the line: " + withLine.Text);
                    var without = await client.CompleteAsync(ClaimCheck.RequestVerify(Models.Ambient, known, flagged));
                    Console.WriteLine("second look, details alone: " + without.Text);
                }
                return 0;
            }
            default:
                Console.WriteLine("modes: generate | label | gold | check <variant>");
                return 2;
        }
    }

    // ------------------------------------------------------------------ generate

    static async Task<int> Generate(string dir, int parallel)
    {
        using var doc = JsonDocument.Parse(File.ReadAllText(Path.Combine(dir, "scenarios.json")));
        var root = doc.RootElement;
        var nowE = root.GetProperty("now");
        var now = new GameTime(nowE.GetProperty("day").GetInt32(), nowE.GetProperty("hour").GetInt32(), nowE.GetProperty("minute").GetInt32());
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var jobs = new List<(string card, string scene, JsonElement set, string lineId, bool probe, List<string> says)>();
        foreach (var c in root.GetProperty("characters").EnumerateArray())
            foreach (var s in root.GetProperty("memorySets").EnumerateArray())
            {
                foreach (var l in root.GetProperty("lines").EnumerateArray())
                    jobs.Add((c.GetProperty("card").GetString(), c.GetProperty("scene").GetString(), s,
                              l.GetProperty("id").GetString(), l.GetProperty("probe").GetBoolean(),
                              new List<string> { l.GetProperty("say").GetString() }));
                foreach (var ch in root.GetProperty("chains").EnumerateArray())
                    jobs.Add((c.GetProperty("card").GetString(), c.GetProperty("scene").GetString(), s,
                              ch.GetProperty("id").GetString(), true,
                              ch.GetProperty("says").EnumerateArray().Select(x => x.GetString()).ToList()));
            }
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var drafts = new List<Draft>();
        var gate = new SemaphoreSlim(parallel);
        var failures = 0;
        var tasks = jobs.Select(async job =>
        {
            await gate.WaitAsync();
            try
            {
                var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md")));
                var memory = new MemoryStore(card.Id);
                foreach (var m in job.set.GetProperty("memories").EnumerateArray())
                    memory.Append(new MemoryEvent(new GameTime(m.GetProperty("day").GetInt32(), m.GetProperty("hour").GetInt32(), m.GetProperty("minute").GetInt32()),
                        m.GetProperty("kind").GetString(), m.GetProperty("importance").GetDouble(), m.GetProperty("text").GetString()));
                var engine = new ConversationEngine(client, card, memory, new KnowledgeBase(), new SuspicionTracker(), cost);
                var said = new List<string>();
                var minute = now;
                for (int t = 0; t < job.says.Count; t++)
                {
                    said.Add(job.says[t]);
                    string reply;
                    try { reply = await engine.SayToAsync(job.says[t], minute, job.scene); }
                    catch (Exception) { Interlocked.Increment(ref failures); return; }
                    var known = ClaimCheck.KnownFor(card, ClaimCheck.WitnessedFor(engine.Memory), engine.Memory.Beliefs, null, job.scene, minute.ToString());
                    lock (drafts)
                        drafts.Add(new Draft
                        {
                            id = $"{job.card}.{job.set.GetProperty("id").GetString()}.{job.lineId}.{t}",
                            card = job.card, set = job.set.GetProperty("id").GetString(), line = job.lineId, turn = t, probe = job.probe,
                            said = new List<string>(said), reply = reply, known = known,
                        });
                    minute = minute.AddMinutes(1);
                }
            }
            finally { gate.Release(); }
        }).ToList();
        await Task.WhenAll(tasks);
        drafts.Sort((a, b) => string.CompareOrdinal(a.id, b.id));
        WriteJsonl(Path.Combine(dir, "drafts.jsonl"), drafts);
        Console.WriteLine($"generate: jobs={jobs.Count} drafts={drafts.Count} failedJobs={failures} usd={cost.EstimateUsd() + _usd:0.00} (the engine's own rate card) -> drafts.jsonl");
        return failures == 0 ? 0 : 1;
    }

    // ------------------------------------------------------------------ label

    const string LabelRule =
        "You label one line that a character in a small British port town in 1990 said to somebody, for details it states that the " +
        "character's own knowledge does not support. KNOWN is everything the character knows: who they are, their memories with the " +
        "time each happened, and the scene and the time now. For context you are also shown what the other person said to them; that " +
        "is NOT evidence of anything.\n" +
        "A detail is INVENTED when the line states it as fact, as seen, heard or true, and KNOWN neither states it nor directly implies " +
        "it. Count specifics about events and people: a vehicle, a person present, named or described, a time or a day, a place, what " +
        "anyone looked like or wore, an object, an amount, what anyone did before or after, whether the police came. A detail KNOWN gives " +
        "about something else (a fish van this morning) does not support the same detail about a different event.\n" +
        "Not invented: feelings, opinions, idioms, guesses marked as guesses, questions, denials, saying they do not know, vague words " +
        "(somebody, talk, things), repeating KNOWN in other words, the character's own life, work and habits as KNOWN tells them, small " +
        "talk about the weather or the street that claims no event.\n" +
        "Answer with JSON and nothing else: {\"invented\": [{\"detail\": \"a white van\", \"kind\": \"vehicle\"}]} with kind one of " +
        "vehicle, person, time, place, appearance, object, amount, action, police, other; or {\"invented\": []}.";

    static async Task<int> LabelAll(string dir, int parallel)
    {
        var drafts = ReadJsonl<Draft>(Path.Combine(dir, "drafts.jsonl"));
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        foreach (var model in Labellers)
        {
            var rows = new List<LabelRow>();
            var gate = new SemaphoreSlim(parallel);
            await Task.WhenAll(drafts.Select(async d =>
            {
                await gate.WaitAsync();
                try
                {
                    var req = new LlmRequest { Model = model, MaxTokens = 600, System = LabelRule };
                    req.Messages.Add(new LlmMessage("user",
                        "KNOWN:\n" + d.known + "\nTHE OTHER PERSON SAID (not evidence):\n" + string.Join("\n", d.said.Select(s => "- " + s)) +
                        "\n\nTHE LINE THE CHARACTER SAID (the last reply above is this one):\n<<<\n" + d.reply + "\n>>>"));
                    LlmResponse r = null;
                    for (int attempt = 0; attempt < 3 && r == null; attempt++)
                    {
                        try { r = await client.CompleteAsync(req); } catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                    }
                    if (r != null) Spend(model, r.InputTokens, r.OutputTokens);
                    var parsed = ParseDetails(r?.Text);
                    lock (rows) rows.Add(new LabelRow { id = d.id, model = model, parsed = parsed != null, invented = parsed ?? new List<Detail>() });
                }
                finally { gate.Release(); }
            }));
            rows.Sort((a, b) => string.CompareOrdinal(a.id, b.id));
            WriteJsonl(Path.Combine(dir, $"labels.{model}.jsonl"), rows);
            Console.WriteLine($"label {model}: {rows.Count} rows, unparsed={rows.Count(x => !x.parsed)}, invented turns={rows.Count(x => x.invented.Count > 0)}");
        }
        Console.WriteLine($"label: usd={_usd:0.00}");
        return 0;
    }

    static List<Detail> ParseDetails(string text)
    {
        if (string.IsNullOrWhiteSpace(text)) return null;
        int a = text.IndexOf('{'), b = text.LastIndexOf('}');
        if (a < 0 || b <= a) return null;
        try
        {
            using var d = JsonDocument.Parse(text.Substring(a, b - a + 1));
            if (!d.RootElement.TryGetProperty("invented", out var inv) || inv.ValueKind != JsonValueKind.Array) return null;
            var list = new List<Detail>();
            foreach (var e in inv.EnumerateArray())
            {
                if (e.ValueKind == JsonValueKind.String) list.Add(new Detail { detail = e.GetString(), kind = "other" });
                else if (e.ValueKind == JsonValueKind.Object)
                    list.Add(new Detail
                    {
                        detail = e.TryGetProperty("detail", out var dd) ? dd.GetString() : "",
                        kind = e.TryGetProperty("kind", out var kk) ? kk.GetString() : "other",
                    });
            }
            return list;
        }
        catch (JsonException) { return null; }
    }

    // ------------------------------------------------------------------ gold

    /// The turns both labellers call invented or both call clean are settled;
    /// the rest are written to disagreements.jsonl for a person, whose rulings go
    /// in adjudications.json as {"id": {"invented": true, "why": "..."}}. gold.jsonl
    /// is written only when every disagreement has a ruling.
    static int Gold(string dir)
    {
        var drafts = ReadJsonl<Draft>(Path.Combine(dir, "drafts.jsonl")).ToDictionary(d => d.id);
        var a = ReadJsonl<LabelRow>(Path.Combine(dir, $"labels.{Labellers[0]}.jsonl")).ToDictionary(r => r.id);
        var b = ReadJsonl<LabelRow>(Path.Combine(dir, $"labels.{Labellers[1]}.jsonl")).ToDictionary(r => r.id);
        var rulings = new Dictionary<string, (bool invented, string why)>();
        var adjPath = Path.Combine(dir, "adjudications.json");
        if (File.Exists(adjPath))
        {
            using var adj = JsonDocument.Parse(File.ReadAllText(adjPath));
            foreach (var p in adj.RootElement.EnumerateObject())
                rulings[p.Name] = (p.Value.GetProperty("invented").GetBoolean(), p.Value.TryGetProperty("why", out var w) ? w.GetString() : "");
        }
        int agreeInv = 0, agreeClean = 0, open = 0;
        var gold = new List<object>();
        var dis = new List<object>();
        foreach (var id in drafts.Keys.OrderBy(k => k, StringComparer.Ordinal))
        {
            bool ia = a.TryGetValue(id, out var ra) && ra.invented.Count > 0;
            bool ib = b.TryGetValue(id, out var rb) && rb.invented.Count > 0;
            bool unparsed = ra == null || rb == null || !ra.parsed || !rb.parsed;
            bool? inv = null;
            string source;
            if (rulings.TryGetValue(id, out var ru)) { inv = ru.invented; source = "ruled"; }
            else if (!unparsed && ia == ib) { inv = ia; source = "agreed"; if (ia) agreeInv++; else agreeClean++; }
            else { source = "open"; open++; }
            if (source == "open" || (source == "ruled"))
                dis.Add(new { id, reply = drafts[id].reply, said = drafts[id].said, a = ra?.invented, b = rb?.invented, ruled = source == "ruled" ? (object)ru.invented : null });
            if (inv.HasValue)
                gold.Add(new { id, invented = inv.Value, source, details = (inv.Value ? (ia ? ra.invented : rb?.invented) : new List<Detail>()) });
        }
        WriteJsonl(Path.Combine(dir, "disagreements.jsonl"), dis);
        int n = drafts.Count;
        Console.WriteLine($"gold: turns={n} agreedInvented={agreeInv} agreedClean={agreeClean} ruled={rulings.Count} open={open} " +
                          $"agreement={(n - open - rulings.Count) * 100.0 / Math.Max(1, n):0.0}%");
        if (open > 0) { Console.WriteLine($"gold: {open} turns to settle in adjudications.json (see disagreements.jsonl); gold.jsonl not written"); return 1; }
        WriteJsonl(Path.Combine(dir, "gold.jsonl"), gold);
        Console.WriteLine($"gold: written, invented turns={gold.Count(g => (bool)g.GetType().GetProperty("invented").GetValue(g))}");
        return 0;
    }

    // ------------------------------------------------------------------ check

    sealed class GoldRow { public string id { get; set; } public bool invented { get; set; } public string source { get; set; } public List<Detail> details { get; set; } }

    /// THE TWO HALVES, so a checker is not tuned on the turns it is judged on:
    /// the checker's wording is worked on the "tune" half (four memory sets) and
    /// reported on the "held" half (the other four), and on all.
    static readonly string[] TuneSets = { "saw-window", "heard-vague", "ordinary-day", "the-rank" };

    static async Task<int> Check(string dir, string variant, int parallel, string half)
    {
        var drafts = ReadJsonl<Draft>(Path.Combine(dir, "drafts.jsonl")).ToDictionary(d => d.id);
        var gold = ReadJsonl<GoldRow>(Path.Combine(dir, "gold.jsonl"))
            .Where(g => half == "all" || (half == "tune") == TuneSets.Contains(drafts[g.id].set)).ToList();
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var results = new List<object>();
        var ms = new List<long>();
        int tp = 0, fn = 0, fp = 0, tn = 0, unchecked1 = 0;
        var gate = new SemaphoreSlim(parallel);
        await Task.WhenAll(gold.Select(async g =>
        {
            await gate.WaitAsync();
            try
            {
                var d = drafts[g.id];
                var sw = Stopwatch.StartNew();
                IReadOnlyList<string> flagged = await RunChecker(variant, client, cost, d);
                sw.Stop();
                lock (results)
                {
                    ms.Add(sw.ElapsedMilliseconds);
                    bool f = flagged != null && flagged.Count > 0;
                    if (flagged == null) unchecked1++;
                    if (g.invented && f) tp++; else if (g.invented) fn++; else if (f) fp++; else tn++;
                    results.Add(new { id = g.id, gold = g.invented, flagged = flagged, ms = sw.ElapsedMilliseconds });
                }
            }
            finally { gate.Release(); }
        }));
        results.Sort((x, y) => string.CompareOrdinal((string)x.GetType().GetProperty("id").GetValue(x), (string)y.GetType().GetProperty("id").GetValue(y)));
        WriteJsonl(Path.Combine(dir, $"check.{variant}.{half}.jsonl"), results);
        ms.Sort();
        double recall = tp + fn > 0 ? tp * 1.0 / (tp + fn) : 0, falseAlarm = fp + tn > 0 ? fp * 1.0 / (fp + tn) : 0;
        Console.WriteLine($"check {variant} ({half}): invented turns caught {tp}/{tp + fn} ({recall * 100:0}%, 95% {Wilson(tp, tp + fn)}), " +
                          $"clean turns flagged {fp}/{fp + tn} ({falseAlarm * 100:0}%), unchecked={unchecked1}, " +
                          $"ms median={ms[ms.Count / 2]} p90={ms[(int)(ms.Count * 0.9)]}, usd={_usd:0.00}");
        return 0;
    }

    /// The checkers compared. v2 is the one live since 25 September
    /// (ClaimCheck.Request and Parse on the ambient model).
    static async Task<IReadOnlyList<string>> RunChecker(string variant, ILlmClient client, CostTracker cost, Draft d)
    {
        switch (variant)
        {
            case "v2":
            {
                var req = ClaimCheck.Request(Models.Ambient, d.known, d.reply);
                var r = await Retry(() => client.CompleteAsync(req));
                if (r == null) return null;
                Spend(Models.Ambient, r.InputTokens, r.OutputTokens);
                return ClaimCheck.Parse(r.Text);
            }
            case "v3":
            case "v3s":
            {
                // The third version: every specific with the numbered item that
                // supports it; v3 on the ambient model, v3s on the core model.
                string model = variant == "v3" ? Models.Ambient : Models.Core;
                var items = ItemsFor(d);
                var req = ClaimCheck.RequestItems(model, ClaimCheck.NumberedKnown(items), d.reply);
                var r = await Retry(() => client.CompleteAsync(req));
                if (r == null) return null;
                Spend(model, r.InputTokens, r.OutputTokens);
                return ClaimCheck.ParseItems(r.Text, items.Select(i => i.id).ToList());
            }
            case "v3v":
            {
                // The list, then a second look at whatever it flagged: the live
                // check itself, so the bench measures what the game runs.
                var items = ItemsFor(d);
                for (int attempt = 0; attempt < 3; attempt++)
                {
                    try
                    {
                        var (found, calls) = await ClaimCheck.CheckAsync(client, Models.Ambient, items, d.reply, default);
                        foreach (var c in calls) Spend(Models.Ambient, c.InputTokens, c.OutputTokens);
                        return found;
                    }
                    catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
                }
                return null;
            }
            default: throw new ArgumentException("no such checker: " + variant);
        }
    }

    /// What the character knew at a draft, as the numbered items the third
    /// version reads, rebuilt from the scenario the draft came from: its card,
    /// its memory set, its scene and the minute of its turn.
    static List<(string id, string text)> ItemsFor(Draft d)
    {
        var dir = Path.Combine(RepoRoot(), "production", "research", "invented-claims", "bench");
        if (_scenarios == null) _scenarios = JsonDocument.Parse(File.ReadAllText(Path.Combine(dir, "scenarios.json")));
        var root = _scenarios.RootElement;
        var nowE = root.GetProperty("now");
        var now = new GameTime(nowE.GetProperty("day").GetInt32(), nowE.GetProperty("hour").GetInt32(), nowE.GetProperty("minute").GetInt32()).AddMinutes(d.turn);
        string scene = root.GetProperty("characters").EnumerateArray().First(c => c.GetProperty("card").GetString() == d.card).GetProperty("scene").GetString();
        var set = root.GetProperty("memorySets").EnumerateArray().First(s => s.GetProperty("id").GetString() == d.set);
        var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "cast", "cards", d.card + ".md")));
        var memory = new MemoryStore(card.Id);
        foreach (var m in set.GetProperty("memories").EnumerateArray())
            memory.Append(new MemoryEvent(new GameTime(m.GetProperty("day").GetInt32(), m.GetProperty("hour").GetInt32(), m.GetProperty("minute").GetInt32()),
                m.GetProperty("kind").GetString(), m.GetProperty("importance").GetDouble(), m.GetProperty("text").GetString()));
        return ClaimCheck.KnownItems(card, ClaimCheck.WitnessedFor(memory), memory.Beliefs, null, scene, now.ToString());
    }
    static JsonDocument _scenarios;

    static async Task<LlmResponse> Retry(Func<Task<LlmResponse>> call)
    {
        for (int attempt = 0; attempt < 3; attempt++)
        {
            try { return await call(); } catch (Exception) { await Task.Delay(2000 * (attempt + 1)); }
        }
        return null;
    }

    /// A 95% Wilson interval, as the research's baseline was stated.
    static string Wilson(int k, int n)
    {
        if (n == 0) return "n/a";
        double p = k * 1.0 / n, z = 1.96, d = 1 + z * z / n;
        double c = (p + z * z / (2 * n)) / d, h = z * Math.Sqrt(p * (1 - p) / n + z * z / (4.0 * n * n)) / d;
        return $"{(c - h) * 100:0}-{(c + h) * 100:0}%";
    }

    // ------------------------------------------------------------------ pipeline

    /// THE WHOLE TURN, AS THE GAME RUNS IT, on the held-out half: the reply,
    /// the claim check with its one redraft and its fixed line, exactly as
    /// ConversationEngine.SayToAsync does them with a checker set (the real
    /// model for both). What the player would hear is then labelled by the
    /// first labeller, and a turn FAILS when what is said carries an invented
    /// detail. `tag` names the run (before, after), so the two are compared on
    /// the same conversations.
    /// The checks a pipeline run can use: v3v, the live one (the list, then a
    /// second look); v3, the list alone; v2, the second version's wording read
    /// against the same numbered items.
    static async Task<(IReadOnlyList<string> invented, List<LlmResponse> calls)> ListOnly(ILlmClient c, string model,
        List<(string id, string text)> items, string line, CancellationToken ct)
    {
        var r = await c.CompleteAsync(ClaimCheck.RequestItems(model, ClaimCheck.NumberedKnown(items), line), ct);
        return (ClaimCheck.ParseItems(r.Text, items.Select(i => i.id).ToList()), new List<LlmResponse> { r });
    }
    static async Task<(IReadOnlyList<string> invented, List<LlmResponse> calls)> OldWording(ILlmClient c, string model,
        List<(string id, string text)> items, string line, CancellationToken ct)
    {
        var r = await c.CompleteAsync(ClaimCheck.Request(model, ClaimCheck.NumberedKnown(items), line), ct);
        return (ClaimCheck.Parse(r.Text), new List<LlmResponse> { r });
    }

    /// With `early`, the turn runs as the helper runs it with --early: the
    /// reply streamed, its first sentence checked on its own and handed over
    /// the moment it passes, the rest after. The run then also reports how
    /// long the player waits for that first sentence, which is the delay the
    /// voice starts from.
    static async Task<int> Pipeline(string dir, string tag, int parallel, string checker, bool early = false)
    {
        using var doc = JsonDocument.Parse(File.ReadAllText(Path.Combine(dir, "scenarios.json")));
        var root = doc.RootElement;
        var nowE = root.GetProperty("now");
        var now0 = new GameTime(nowE.GetProperty("day").GetInt32(), nowE.GetProperty("hour").GetInt32(), nowE.GetProperty("minute").GetInt32());
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var jobs = new List<(string card, string scene, JsonElement set, string lineId, List<string> says)>();
        foreach (var c in root.GetProperty("characters").EnumerateArray())
            foreach (var s in root.GetProperty("memorySets").EnumerateArray())
            {
                if (TuneSets.Contains(s.GetProperty("id").GetString())) continue;   // the held-out half only
                foreach (var l in root.GetProperty("lines").EnumerateArray())
                    jobs.Add((c.GetProperty("card").GetString(), c.GetProperty("scene").GetString(), s, l.GetProperty("id").GetString(),
                              new List<string> { l.GetProperty("say").GetString() }));
                foreach (var ch in root.GetProperty("chains").EnumerateArray())
                    jobs.Add((c.GetProperty("card").GetString(), c.GetProperty("scene").GetString(), s, ch.GetProperty("id").GetString(),
                              ch.GetProperty("says").EnumerateArray().Select(x => x.GetString()).ToList()));
            }
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var turns = new List<Draft>();
        var meta = new Dictionary<string, (long ms, bool fixedLine, bool redrafted)>();
        var firstHeardMs = new List<long>();
        int firstHeld = 0;
        var gate = new SemaphoreSlim(parallel);
        int failures = 0;
        await Task.WhenAll(jobs.Select(async job =>
        {
            await gate.WaitAsync();
            try
            {
                var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md")));
                var memory = new MemoryStore(card.Id);
                foreach (var m in job.set.GetProperty("memories").EnumerateArray())
                    memory.Append(new MemoryEvent(new GameTime(m.GetProperty("day").GetInt32(), m.GetProperty("hour").GetInt32(), m.GetProperty("minute").GetInt32()),
                        m.GetProperty("kind").GetString(), m.GetProperty("importance").GetDouble(), m.GetProperty("text").GetString()));
                var engine = new ConversationEngine(client, card, memory, new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = client };
                if (checker == "v3") engine.CheckLine = ListOnly;
                else if (checker == "v2") engine.CheckLine = OldWording;
                var said = new List<string>();
                var minute = now0;
                for (int t = 0; t < job.says.Count; t++)
                {
                    said.Add(job.says[t]);
                    var sw = Stopwatch.StartNew();
                    long heardAt = -1;
                    Func<string, Task<bool>> onFirst = null;
                    if (early) onFirst = s => { Interlocked.CompareExchange(ref heardAt, sw.ElapsedMilliseconds, -1); return Task.FromResult(true); };
                    string reply;
                    try { reply = await engine.SayToAsync(job.says[t], minute, job.scene, default, onFirst); }
                    catch (Exception) { Interlocked.Increment(ref failures); return; }
                    sw.Stop();
                    if (early)
                        lock (firstHeardMs)
                        {
                            // Held back: the first sentence failed its check, so the
                            // player waits for the whole turn instead.
                            if (heardAt >= 0) firstHeardMs.Add(heardAt);
                            else { firstHeld++; firstHeardMs.Add(sw.ElapsedMilliseconds); }
                        }
                    var id = $"{job.card}.{job.set.GetProperty("id").GetString()}.{job.lineId}.{t}";
                    var known = ClaimCheck.KnownFor(card, ClaimCheck.WitnessedFor(engine.Memory), engine.Memory.Beliefs, null, job.scene, minute.ToString());
                    lock (turns)
                    {
                        turns.Add(new Draft { id = id, card = job.card, set = job.set.GetProperty("id").GetString(), line = job.lineId, turn = t,
                            said = new List<string>(said), reply = reply, known = known });
                        meta[id] = (sw.ElapsedMilliseconds, ClaimCheck.IsKnownOnly(reply), engine.LastInvented.Count > 0);
                    }
                    minute = minute.AddMinutes(1);
                }
            }
            finally { gate.Release(); }
        }));
        turns.Sort((a, b) => string.CompareOrdinal(a.id, b.id));
        WriteJsonl(Path.Combine(dir, $"pipeline.{tag}.jsonl"), turns);
        // What the player heard, labelled by the first labeller (the same rule).
        var labels = new List<LabelRow>();
        await Task.WhenAll(turns.Select(async d =>
        {
            await gate.WaitAsync();
            try
            {
                var req = new LlmRequest { Model = Labellers[0], MaxTokens = 600, System = LabelRule };
                req.Messages.Add(new LlmMessage("user",
                    "KNOWN:\n" + d.known + "\nTHE OTHER PERSON SAID (not evidence):\n" + string.Join("\n", d.said.Select(s => "- " + s)) +
                    "\n\nTHE LINE THE CHARACTER SAID (the last reply above is this one):\n<<<\n" + d.reply + "\n>>>"));
                var r = await Retry(() => client.CompleteAsync(req));
                if (r != null) Spend(Labellers[0], r.InputTokens, r.OutputTokens);
                var parsed = ParseDetails(r?.Text);
                lock (labels) labels.Add(new LabelRow { id = d.id, model = Labellers[0], parsed = parsed != null, invented = parsed ?? new List<Detail>() });
            }
            finally { gate.Release(); }
        }));
        labels.Sort((a, b) => string.CompareOrdinal(a.id, b.id));
        WriteJsonl(Path.Combine(dir, $"pipeline.{tag}.labels.jsonl"), labels);
        int n = turns.Count, failed = labels.Count(l => l.invented.Count > 0), fixedLines = meta.Values.Count(m => m.fixedLine),
            redrafted = meta.Values.Count(m => m.redrafted), unparsed = labels.Count(l => !l.parsed);
        var ms = meta.Values.Select(m => m.ms).OrderBy(x => x).ToList();
        Console.WriteLine($"pipeline {tag} (check {checker}): turns={n} failedJobs={failures} said an invented detail={failed}/{n} ({failed * 100.0 / Math.Max(1, n):0}%, 95% {Wilson(failed, n)}), " +
                          $"redrafted={redrafted} fixed line={fixedLines} unlabelled={unparsed} turn ms median={ms[ms.Count / 2]} p90={ms[(int)(ms.Count * 0.9)]} " +
                          $"usd={cost.EstimateUsd() + _usd:0.00}");
        if (early && firstHeardMs.Count > 0)
        {
            firstHeardMs.Sort();
            Console.WriteLine($"pipeline {tag} first sentence heard at ms median={firstHeardMs[firstHeardMs.Count / 2]} " +
                              $"p90={firstHeardMs[(int)(firstHeardMs.Count * 0.9)]} held back={firstHeld}/{firstHeardMs.Count}");
        }
        return failures == 0 ? 0 : 1;
    }

    // ------------------------------------------------------------------ plumbing

    static string Key()
    {
        var env = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");
        if (!string.IsNullOrEmpty(env)) return env;
        var p = Path.Combine(Environment.GetFolderPath(Environment.SpecialFolder.UserProfile), "AppData", "LocalLow", "DefaultCompany", "ledger", "secrets.json");
        using var d = JsonDocument.Parse(File.ReadAllText(p));
        return d.RootElement.GetProperty("anthropic_api_key").GetString();
    }

    static void WriteJsonl<T>(string path, IEnumerable<T> rows)
    {
        var sb = new StringBuilder();
        foreach (var r in rows) sb.Append(JsonSerializer.Serialize(r, r.GetType(), Plain)).Append('\n');
        File.WriteAllText(path, sb.ToString());
    }

    static List<T> ReadJsonl<T>(string path) =>
        File.ReadAllLines(path).Where(l => l.Trim().Length > 0).Select(l => JsonSerializer.Deserialize<T>(l)).ToList();

    static string Arg(string[] args, string name, string fallback)
    {
        for (int i = 0; i + 1 < args.Length; i++) if (args[i] == name) return args[i + 1];
        return fallback;
    }

    static string RepoRoot()
    {
        var d = new DirectoryInfo(AppContext.BaseDirectory);
        while (d != null && !File.Exists(Path.Combine(d.FullName, "canon.md"))) d = d.Parent;
        return d?.FullName ?? ".";
    }
}
