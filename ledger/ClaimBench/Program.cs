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
///     dotnet run --project ledger/ClaimBench -c Release -- smalltalk     # real names in small talk, the rule off and on
///     dotnet run --project ledger/ClaimBench -c Release -- tics          # a card's verbal tic over a conversation, before and after
///     dotnet run --project ledger/ClaimBench -c Release -- disguise      # inventions hidden in small talk, through the live check
///     dotnet run --project ledger/ClaimBench -c Release -- firsts        # a newcomer's first questions, through the real engine
///     dotnet run --project ledger/ClaimBench -c Release -- hours         # what is open when, without the street's hours and with them
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
            case "smalltalk": return await SmallTalk(dir, parallel);
            case "tics": return await Tics(dir, parallel);
            case "disguise": return await Disguise(dir);
            case "firsts": return await Firsts(dir, parallel);
            case "hours": return await Hours(dir, parallel);
            case "hourslook": return await HoursLook();
            case "check": _withPeople = args.Contains("--people"); return await Check(dir, args.Length > 1 ? args[1] : "v2", parallel, Arg(args, "--half", "all"));
            case "pipeline": return await Pipeline(dir, args.Length > 1 ? args[1] : "run", parallel, Arg(args, "--checker", "v3v"),
                                                   args.Contains("--early"));
            case "again":
            {
                // Some turns of the bench's drafts through the live check, each
                // several times, one try at a time, with the items as the check
                // builds them now and as they were before town list 6be (whole P
                // lines, no own name): whether a turn one run missed is a change
                // to the items or the checker's own run-to-run noise (town list
                // 6be tried a split of the P lines this way). `again id ... --times 3`.
                _withPeople = true;
                int times = int.Parse(Arg(args, "--times", "3"));
                var ids = args.Skip(1).TakeWhile(a => !a.StartsWith("--")).ToList();
                var drafts = ReadJsonl<Draft>(Path.Combine(dir, "drafts.jsonl")).Where(x => ids.Contains(x.id)).ToList();
                using var client = new AnthropicClient(Key());
                foreach (var d in drafts)
                {
                    var now = ItemsFor(d);
                    var nowT = now.Find(i => i.id == "T1").text;
                    var before = now.Where(i => i.id[0] != 'N' && i.id[0] != 'P' && !(i.id == "S2") && !i.text.StartsWith("Their own name")).ToList();
                    int day = int.Parse(System.Text.RegularExpressions.Regex.Match(nowT, @"D(\d+)").Groups[1].Value);
                    int hour = int.Parse(System.Text.RegularExpressions.Regex.Match(nowT, @"D\d+ (\d+):").Groups[1].Value);
                    int np = 0;
                    foreach (var p in _cast.PeopleFor(d.card, day, hour)) before.Add(("P" + (++np), "Somebody or somewhere on the street they know: " + p));
                    async Task<bool> Flagged(List<(string id, string text)> items)
                    {
                        var (found, calls) = await ClaimCheck.CheckAsync(client, Models.Ambient, items, d.reply, default);
                        foreach (var c in calls) Spend(Models.Ambient, c.InputTokens, c.OutputTokens);
                        // --show: what the check wrote each time it let the turn through.
                        if (args.Contains("--show") && (found == null || found.Count == 0))
                            Console.WriteLine("  passed, " + (ReferenceEquals(items, now) ? "now" : "before") + ": " +
                                              string.Join(" || ", calls.Select(c => System.Text.RegularExpressions.Regex.Replace(c.Text, @"\s+", " "))));
                        return found != null && found.Count > 0;
                    }
                    // One at a time, the two layouts in turn: the same request sent
                    // many at once came back alike, so those were not separate tries.
                    int a = 0, b = 0;
                    for (int t = 0; t < times; t++)
                    {
                        if (await Flagged(now)) a++;
                        if (await Flagged(before)) b++;
                    }
                    Console.WriteLine($"{d.id}: flagged {a}/{times} as now, {b}/{times} as before");
                }
                Console.WriteLine($"usd={_usd:0.00}");
                return 0;
            }
            case "rawline":
            {
                // One line said by one of the cast at 10:00 on the first day, with
                // who they know on the street, through the live check, every call
                // printed: `rawline sam "Mickey had a daughter, June."`.
                using var client = new AnthropicClient(Key());
                var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "cast", "cards", args[1] + ".md")));
                var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
                var items = ClaimCheck.KnownItems(card, new List<MemoryEvent>(), null, null, "Dry, grey.", new GameTime(0, 10, 0).ToldAs, null, cast.PeopleFor(args[1], 0, 10));
                Console.WriteLine(ClaimCheck.NumberedKnown(items.Where(i => i.id[0] == 'N' || i.text.StartsWith("Their own name")).ToList()));
                var (invented, calls) = await ClaimCheck.CheckAsync(client, Models.Ambient, items, args[2], default);
                foreach (var c in calls) Console.WriteLine("call: " + c.Text);
                Console.WriteLine("invented: " + (invented == null ? "(unchecked)" : string.Join(" | ", invented)));
                return 0;
            }
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
        WriteJsonl(Path.Combine(dir, $"check.{variant}.{half}{(_withPeople ? ".people" : "")}.jsonl"), results);
        ms.Sort();
        double recall = tp + fn > 0 ? tp * 1.0 / (tp + fn) : 0, falseAlarm = fp + tn > 0 ? fp * 1.0 / (fp + tn) : 0;
        Console.WriteLine($"check {variant} ({half}): invented turns caught {tp}/{tp + fn} ({recall * 100:0}%, 95% {Wilson(tp, tp + fn)}), " +
                          $"clean turns flagged {fp}/{fp + tn} ({falseAlarm * 100:0}%), unchecked={unchecked1}, " +
                          $"ms median={ms[ms.Count / 2]} p90={ms[(int)(ms.Count * 0.9)]}, usd={_usd:0.00}");
        return 0;
    }

    /// REAL NAMES IN SMALL TALK (town list 6ao): a dozen questions a friend will
    /// ask, to each character who talks, with the prompt's rule off and then on,
    /// through the real engine and its check. Counts the first drafts that named
    /// a real make, brand, club, programme, paper, public figure or later thing
    /// (asked again without, RealWorld), and the replies said that still do.
    static async Task<int> SmallTalk(string dir, int parallel)
    {
        var probes = new[]
        {
            "What are you smoking?", "Who do you support?", "What's on the telly tonight?", "Nice car that, what is it?",
            "Have you got a mobile I could borrow?", "What paper do you read?", "What do you make of Thatcher?", "Where do you do your shopping?",
            "What music are you into?", "What do you drive?", "Can I email you about it?", "What biscuits have you got in?",
        };
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var rows = new List<object>();
        var gate = new SemaphoreSlim(parallel);
        foreach (bool rule in new[] { false, true })
        {
            ConversationEngine.RealWorldRule = rule;
            int drafts = 0, said = 0, n = 0, failed = 0;
            var jobs = new List<(string card, string probe)>();
            foreach (var c in new[] { "lena", "rocco", "sam" }) foreach (var p in probes) jobs.Add((c, p));
            await Task.WhenAll(jobs.Select(async job =>
            {
                await gate.WaitAsync();
                try
                {
                    var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md")));
                    var engine = new ConversationEngine(client, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = client };
                    string reply;
                    try { reply = await engine.SayToAsync(job.probe, new GameTime(2, 18, 0), "Quay Street, early evening, dry.", default, null); }
                    catch (Exception) { Interlocked.Increment(ref failed); return; }
                    var inReply = RealWorld.Find(reply);
                    lock (rows)
                    {
                        n++;
                        if (engine.LastRealNames.Count > 0) drafts++;
                        if (inReply.Count > 0) said++;
                        rows.Add(new { rule, card = job.card, probe = job.probe, draftNamed = engine.LastRealNames, invented = engine.LastInvented, reply, replyNamed = inReply });
                    }
                }
                finally { gate.Release(); }
            }));
            Console.WriteLine($"smalltalk rule={(rule ? "on" : "off")}: first drafts naming a real name or later thing {drafts}/{n}; replies said that do {said}/{n}; failed {failed}");
        }
        ConversationEngine.RealWorldRule = true;
        WriteJsonl(Path.Combine(dir, "smalltalk.jsonl"), rows);
        Console.WriteLine($"smalltalk: usd={cost.EstimateUsd():0.00} (the engine's own rate card) -> smalltalk.jsonl");
        return 0;
    }

    /// A NEWCOMER'S FIRST QUESTIONS (town list 6be, the fourth sweep): with no
    /// instructions a friend's first lines go to the people in front of him,
    /// and every bench so far asked about a night's events or small talk. Twenty
    /// such questions to each character who talks, through the real engine and
    /// its check, each a first line to them; counts the answers that end in
    /// their "that's all I know" or a refusal, for reading by eye after.
    static async Task<int> Firsts(string dir, int parallel)
    {
        var probes = new[]
        {
            "Who are you?", "What is this place?", "What am I meant to do here?", "How did Mickey die?", "Sorry I missed the funeral.",
            "What's behind that door?", "Where do I sleep?", "Who runs things round here?", "Is there any money in the business?", "Did Mickey leave me anything?",
            "What was Mickey like?", "Who can I trust?", "How many drivers are there?", "Where's the office?", "What do you do here?",
            "Do you work for me now?", "Anything I should know?", "Where can I get something to eat?", "Who was Mickey's family?", "What happens now?",
        };
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var rows = new List<object>();
        var gate = new SemaphoreSlim(parallel);
        int fallback = 0, refused = 0, n = 0, failed = 0;
        var byCard = new Dictionary<string, int>();
        var jobs = new List<(string card, string probe)>();
        foreach (var c in new[] { "lena", "rocco", "sam" }) foreach (var p in probes) jobs.Add((c, p));
        await Task.WhenAll(jobs.Select(async job =>
        {
            await gate.WaitAsync();
            try
            {
                var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md")));
                var engine = new ConversationEngine(client, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = client };
                engine.People = cast.PeopleFor(job.card, 0, 10);
                engine.HowYouKnowHim = new PlayerIdentity().HowTheyKnowHim(true, true, null);
                string where = cast.WhereWords(job.card, 0, 10);
                string reply;
                try { reply = await engine.SayToAsync(job.probe, new GameTime(0, 10, 0), "Dry, grey." + (where != null ? " Where you are: " + where + "." : ""), default, null); }
                catch (Exception) { Interlocked.Increment(ref failed); return; }
                bool fell = ClaimCheck.IsKnownOnly(reply, card);
                bool refusedLine = ResponseValidator.IsDeflection(reply, card.Name);
                lock (rows)
                {
                    n++;
                    if (fell) { fallback++; byCard[job.card] = (byCard.TryGetValue(job.card, out var k) ? k : 0) + 1; }
                    if (refusedLine) refused++;
                    rows.Add(new { card = job.card, probe = job.probe, reply, fell, refused = refusedLine, invented = engine.LastInvented });
                }
            }
            finally { gate.Release(); }
        }));
        WriteJsonl(Path.Combine(dir, "firsts.jsonl"), rows);
        Console.WriteLine($"firsts: a newcomer's first questions, {n} answered ({failed} failed): \"that's all I know\" {fallback} (" +
                          string.Join(", ", byCard.Select(kv => kv.Key + " " + kv.Value)) + $"), refused {refused}; usd={cost.EstimateUsd():0.00} -> firsts.jsonl");
        return 0;
    }

    /// WHAT IS OPEN WHEN (town list 6bo): eight questions a friend asks about
    /// the street's shops, to Sheila, Ron and Darren on a Wednesday at half
    /// past two (the half day: Rita's, Hal's and the fish shop shut), through
    /// the real engine and its check, without the street's hours and with them
    /// (CastDay.HoursFor, the O item). Each reply is marked by what it says
    /// against the cast file: right, wrong, or no answer ("that's all I know",
    /// a refusal, or no hours given).
    static async Task<int> Hours(string dir, int parallel)
    {
        // A question, the words a right answer has (any), and the words a wrong one does (any).
        var probes = new (string ask, string[] right, string[] wrong)[]
        {
            ("Is Rita's open now?", new[] { "shut", "closed", "half day", "half-day", "early closing", "not open", "till one" }, new[] { "she's open", "it's open", "yes, open", "open till half five" }),
            ("What time does the cafe shut?", new[] { "ten" }, new[] { "three", "four", "five", "six", "two" }),
            ("Is the fish shop open on a Sunday?", new[] { "no", "shut", "closed" }, new[] { "yes" }),
            ("What days is the market on?", new[] { "tuesday" }, new[] { "monday", "wednesday", "thursday" }),
            ("Can I get a paper on a Sunday?", new[] { "yes", "kiosk", "newsagent", "paper shop", "seven" }, new[] { "no papers", "can't" }),
            ("Is the cab office open all night?", new[] { "three" }, new[] { "all night", "midnight", "twenty-four" }),
            ("When does the laundry open in the morning?", new[] { "eight" }, new[] { "seven", "nine", "six" }),
            ("Is Hal's open this afternoon?", new[] { "shut", "closed", "half day", "half-day", "early closing", "not", "till one" }, new[] { "yes", "he's open", "it's open" }),
        };
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var now = new GameTime(2, 14, 30);
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var rows = new List<object>();
        var gate = new SemaphoreSlim(parallel);
        var tally = new Dictionary<string, int[]>();   // with/without -> right, wrong, none
        int failed = 0;
        var jobs = new List<(string card, int probe, bool with)>();
        foreach (var with in new[] { false, true }) foreach (var c in new[] { "lena", "rocco", "sam" }) for (int i = 0; i < probes.Length; i++) jobs.Add((c, i, with));
        await Task.WhenAll(jobs.Select(async job =>
        {
            await gate.WaitAsync();
            try
            {
                var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, job.card + ".md")));
                var engine = new ConversationEngine(client, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost) { Checker = client };
                engine.People = cast.PeopleFor(job.card, now.Day, now.Hour);
                if (job.with) engine.StreetHours = cast.HoursFor(now.Day, now.Hour, now.Minute);
                engine.HowYouKnowHim = new PlayerIdentity().HowTheyKnowHim(true, true, null);
                string where = cast.WhereWords(job.card, now.Day, now.Hour);
                var (ask, right, wrong) = probes[job.probe];
                string reply;
                try { reply = await engine.SayToAsync(ask, now, "Dry, grey." + (where != null ? " Where you are: " + where + "." : ""), default, null); }
                catch (Exception) { Interlocked.Increment(ref failed); return; }
                var low = " " + reply.ToLowerInvariant().Replace('\u2019', '\'') + " ";
                bool fell = ClaimCheck.IsKnownOnly(reply, card) || ResponseValidator.IsDeflection(reply, card.Name);
                bool isWrong = !fell && wrong.Any(w => low.Contains(w));
                bool isRight = !fell && !isWrong && right.Any(w => low.Contains(w));
                string mark = isRight ? "right" : isWrong ? "wrong" : "none";
                lock (rows)
                {
                    var key = job.with ? "with" : "without";
                    if (!tally.TryGetValue(key, out var t)) tally[key] = t = new int[3];
                    t[isRight ? 0 : isWrong ? 1 : 2]++;
                    rows.Add(new { hours = job.with, card = job.card, ask, reply, mark, fell, invented = engine.LastInvented });
                }
            }
            finally { gate.Release(); }
        }));
        WriteJsonl(Path.Combine(dir, "hours.jsonl"), rows);
        foreach (var key in new[] { "without", "with" })
            if (tally.TryGetValue(key, out var t))
                Console.WriteLine($"hours {key} the street's hours: right {t[0]}, wrong {t[1]}, no answer {t[2]} (by the words; read hours.jsonl by eye)");
        Console.WriteLine($"hours: {failed} failed; usd={cost.EstimateUsd():0.00} -> hours.jsonl");
        return 0;
    }

    /// THE SECOND LOOK ON HOURS (town list 6bo): true and false details about
    /// the street's hours, each shown to the second look alone with the O item,
    /// its answer printed, to see why a true one is refused.
    static async Task<int> HoursLook()
    {
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cast = CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
        var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, "lena.md")));
        var now = new GameTime(2, 14, 30);
        var items = ClaimCheck.KnownItems(card, new List<MemoryEvent>(), null, null, "Dry, grey.", now.ToldAs, null, cast.PeopleFor("lena", now.Day, now.Hour), null, cast.HoursFor(now.Day, now.Hour, now.Minute));
        var known = ClaimCheck.NumberedKnown(items);
        using var client = new AnthropicClient(Key());
        foreach (var (detail, truth) in new[] { ("Hal's shuts at one on Wednesdays", true), ("the newsagent's opens seven till twelve on Sundays", true), ("the laundry opens at eight", true),
                                               ("the cafe shuts at twelve on Sundays", true), ("Rita's is shut now", true),
                                               ("the laundry opens at half eight", false), ("Rita's shuts at half five on Wednesdays", false), ("the fish shop is shut on Thursdays", false),
                                               ("the cafe shuts at half twelve on Sundays", false) })
        {
            var r = await client.CompleteAsync(ClaimCheck.RequestVerify(Models.Ambient, known, new[] { detail }), default);
            Spend(Models.Ambient, r.InputTokens, r.OutputTokens);
            var ok = ClaimCheck.ParseVerify(r.Text, 1, items.ConvertAll(i => i.id));
            Console.WriteLine($"  {(truth ? "true " : "false")} {(ok != null && ok[0] ? "cleared" : "REFUSED")}: {detail} -> {r.Text.Replace('\n', ' ')}");
        }
        Console.WriteLine($"hourslook: usd={_usd:0.00}");
        return 0;
    }

    /// INVENTIONS HIDDEN IN SMALL TALK (town list 6at): the check now leaves out
    /// a speaker's own everyday life and the street's ordinary fixtures, so each
    /// of these wraps an invented happening, person or vehicle in exactly that
    /// kind of texture; each must still be flagged. The live check (CheckAsync),
    /// with only a card's knowledge, so nothing in them is supported.
    static async Task<int> Disguise(string dir)
    {
        var lines = new[]
        {
            "I never learned to drive, but I saw a white van by the phone box on the corner at eleven.",
            "My usual, same as always. Rita's lad bought twenty off me last night.",
            "Plain ones in the tin. A fella called Dennis brought them round Tuesday.",
            "I get the evening paper. It had a bit about the pawn window being put in.",
            "Phone box on the corner, if you need it. Somebody was using it at midnight, shouting.",
            "I walk everywhere, me. Walked past a man in a donkey jacket running from the yard.",
            "Market for the veg. The fish van was there late, blue one, engine running.",
            "Kettle's on in the office. Sheila had the police in about the takings this morning.",
            "I stand here all day. Saw the new owner by the yard gate at two in the morning.",
            "Radio's on in the office. Heard Hal and Rita shouting about money on Monday.",
            "I don't drive nothing. Ron's cousin drove a Transit through here at night.",
            "Same stall these twenty years. The stall man said somebody broke in Sunday.",
        };
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var card = CharacterCard.Parse(File.ReadAllText(Path.Combine(cardsDir, "rocco.md")));
        var items = ClaimCheck.KnownItems(card, new List<MemoryEvent>(), null, null, "Quay Street, early evening, dry.", new GameTime(2, 18, 0).ToString());
        using var client = new AnthropicClient(Key());
        int flagged = 0, passed = 0;
        var rows = new List<object>();
        foreach (var line in lines)
        {
            IReadOnlyList<string> found = null;
            for (int attempt = 0; attempt < 3 && found == null; attempt++)
            {
                try
                {
                    var (f, calls) = await ClaimCheck.CheckAsync(client, Models.Ambient, items, line, default);
                    foreach (var c in calls) Spend(Models.Ambient, c.InputTokens, c.OutputTokens);
                    found = f;
                }
                catch (Exception) { await Task.Delay(2000); }
            }
            bool caught = found != null && found.Count > 0;
            if (caught) flagged++; else passed++;
            rows.Add(new { line, caught, flagged = found });
            Console.WriteLine($"  {(caught ? "caught" : "PASSED")}: {line}");
        }
        WriteJsonl(Path.Combine(dir, "disguise.jsonl"), rows);
        Console.WriteLine($"disguise: inventions hidden in small talk caught {flagged}/{lines.Length}; usd={_usd:0.00}");
        return 0;
    }

    /// A CARD'S VERBAL TIC OVER A CONVERSATION (town list 6ap): Darren opened 18
    /// of his 80 bench replies with "so listen" and Ron said "boss" in 49. Four
    /// six-turn conversations each, the first drafts as written (no check, so
    /// the drafts are what is measured), with the cards and the prompt as they
    /// were and as they are.
    static async Task<int> Tics(string dir, int parallel)
    {
        var talks = new[]
        {
            new[] { "Evening.", "Busy night?", "What's the word on the street?", "Anyone about earlier?", "Right. Anything else?", "See you, then." },
            new[] { "Alright?", "How's business?", "Seen anything odd lately?", "Who was that you were talking to?", "Fair enough.", "What's the weather doing?" },
            new[] { "Morning.", "You been here long?", "What do you know about the van?", "Who drives it?", "Where does it go?", "Cheers." },
            new[] { "Got a minute?", "What do you make of me?", "Heard anything about the window?", "Who told you that?", "You sure?", "Right, I'll leave you to it." },
        };
        var cardsDir = Path.Combine(RepoRoot(), "production", "cast", "cards");
        var cost = new CostTracker();
        using var client = new AnthropicClient(Key());
        var rows = new List<object>();
        var gate = new SemaphoreSlim(parallel);
        foreach (bool now in new[] { false, true })
        {
            ConversationEngine.TicRule = now;
            int samReplies = 0, samSoListen = 0, samTwice = 0, ronReplies = 0, ronBoss = 0;
            var jobs = new List<(string card, string[] says)>();
            foreach (var c in new[] { "sam", "rocco" }) foreach (var t in talks) jobs.Add((c, t));
            await Task.WhenAll(jobs.Select(async job =>
            {
                await gate.WaitAsync();
                try
                {
                    var text = File.ReadAllText(Path.Combine(cardsDir, job.card + ".md"));
                    if (!now)
                    {
                        text = text.Replace("Opens with 'so listen' when he has something to sell you, never twice running.", "Starts sentences with 'so listen'.")
                                   .Replace("calls people 'boss' or 'friend' now and then, not in every breath.", "calls people 'boss' or 'friend'.");
                    }
                    var card = CharacterCard.Parse(text);
                    var engine = new ConversationEngine(client, card, new MemoryStore(card.Id), new KnowledgeBase(), new SuspicionTracker(), cost);
                    bool lastSo = false;
                    for (int i = 0; i < job.says.Length; i++)
                    {
                        string reply;
                        try { reply = await engine.SayToAsync(job.says[i], new GameTime(2, 18, i), "Quay Street, early evening, dry.", default, null); }
                        catch (Exception) { break; }
                        bool so = reply.TrimStart().StartsWith("So listen", StringComparison.OrdinalIgnoreCase);
                        bool boss = System.Text.RegularExpressions.Regex.IsMatch(reply, @"\bboss\b", System.Text.RegularExpressions.RegexOptions.IgnoreCase);
                        lock (rows)
                        {
                            if (job.card == "sam") { samReplies++; if (so) samSoListen++; if (so && lastSo) samTwice++; }
                            else { ronReplies++; if (boss) ronBoss++; }
                            rows.Add(new { now, card = job.card, turn = i, said = job.says[i], reply });
                        }
                        lastSo = so;
                    }
                }
                finally { gate.Release(); }
            }));
            Console.WriteLine($"tics {(now ? "now" : "before")}: Darren opens with \"so listen\" {samSoListen}/{samReplies} (twice running {samTwice}); Ron says \"boss\" in {ronBoss}/{ronReplies}");
        }
        ConversationEngine.TicRule = true;
        WriteJsonl(Path.Combine(dir, "tics.jsonl"), rows);
        Console.WriteLine($"tics: usd={cost.EstimateUsd():0.00} -> tics.jsonl");
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
        // WITH WHO THEY KNOW ON THE STREET (--people, town list 6ad), as the
        // helper now gives it: the named cast file read for this card at this hour.
        IEnumerable<string> people = null;
        if (_withPeople)
        {
            _cast ??= CastDay.Parse(File.ReadAllText(Path.Combine(RepoRoot(), "production", "specs", "hook-cast.json")));
            people = _cast.PeopleFor(d.card, now.Day, now.Hour);
        }
        return ClaimCheck.KnownItems(card, ClaimCheck.WitnessedFor(memory), memory.Beliefs, null, scene, now.ToString(), null, people);
    }
    static JsonDocument _scenarios;
    static bool _withPeople;
    static CastDay _cast;

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
