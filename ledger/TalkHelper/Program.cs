using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Text.Encodings.Web;
using System.Text.Json;
using System.Threading;
using System.Threading.Tasks;
using Ledger.Core;

/// THE SLICE'S TALKING, RUN BESIDE THE GAME, 23 September.
///
///     dotnet run --project ledger/TalkHelper -c Release              # serves lines on stdin/stdout
///     dotnet run --project ledger/TalkHelper -c Release -- --selftest
///
/// WHY IT EXISTS. The slice asks to "talk to 2-3 people in their cast voices",
/// and the conversation engine that does it is C#, tested, and already
/// carries the content rule and the output guard. The recommendation put to
/// Jafar (FOR-JAFAR, 23 September) is to run that code beside the game as a
/// small helper rather than rewrite it in C++; this is the helper, built on
/// that recommendation while the question waits. The game starts it, writes
/// one JSON line per thing the player says, and reads one JSON line back.
///
/// THE REAL ENGINE, NOT A COPY: ConversationEngine.SayToAsync with the same
/// prompt builder, memory and suspicion objects, then ResponseValidator,
/// which deflects any reply the content rule refuses (D18). One engine per
/// character, kept, so a conversation carries over between lines.
///
/// WHEN THE LINE IS DOWN OR SLOW (the recommendation put to Jafar, a):
/// without a key the character brushes the player off in a line of its own
/// and the reply says offline; a model that has not answered in eight seconds
/// is abandoned for the same brush-off, marked timedOut.
///
/// IN:  {"id":1,"to":"sam","say":"Morning.","hour":12,"scene":"..."}
/// OUT: {"id":1,"to":"sam","reply":"...","ms":812,"offline":false,"timedOut":false}
///
/// WHAT THE CHARACTER KNOWS COMES FROM THE GAME, 24 September. Until now every
/// engine started from an empty memory and knowledge store and every line was
/// day 1, so nobody could answer from what the simulation knew (the outside
/// audit's first finding). A request may now carry the character's state from
/// the running simulation, and the helper loads it before answering:
///   "day":3, "minute":10,
///   "memories":[{"day":3,"hour":14,"minute":5,"kind":"observation","importance":0.9,"text":"..."}],
///   "knows":[{"subject":"tom","predicate":"did","value":"..."}],
///   "suspicion":0.6, "suspicionWhy":"saw him do it"
/// Memories already held are not added twice. The reply carries "day" and
/// "heard": the memories retrieved into the prompt for this line, which is
/// the evidence that the answer came from the simulation's own memory.
///
/// OR THE EVIDENCE, AND THE CORE DECIDES THE SUSPICION, 24 September: instead
/// of a number, the game may send what the character holds about a deed, who
/// they know was near it, and how they know the player, and Suspecting.Derive
/// (Core, tested) sets the level and the reason the model is given:
///   "evidence":{"account":{"held":true,"seen":false,"rung":-1,"names":false,"confidence":0.45,"summary":"..."},
///               "near":{"sawHim":true,"heard":false,"others":0,"summary":"..."},"familiarity":0.2}
/// "who" keys the character's state when two people share a card, and
/// "noReply":true asks for the derived level alone, with no model call and no
/// cost. The reply then carries "suspicion", "level" and "why".
///
/// FAKE MODE, --fake (or LEDGER_TALK_FAKE=1), for the encounter's regression:
/// no key, no network, no cost. A stand-in model answers from the memories in
/// its prompt - it asks about the first one it was given, or passes the time
/// of day when it was given none - so a test can see knowledge arrive in the
/// answer without paying for a model.
/// The key is read from ANTHROPIC_API_KEY and never printed.
static class Program
{
    static readonly string[] BrushOffs =
    {
        "Not now, love. Busy.",
        "Catch me later, eh?",
        "Can't stop. Another time.",
    };

    // THE REPLY AS WRITTEN: apostrophes and accents stay themselves rather
    // than escape codes, so a log or a transcript reads as the line was said.
    static readonly JsonSerializerOptions Plain = new JsonSerializerOptions { Encoder = JavaScriptEncoder.UnsafeRelaxedJsonEscaping };

    sealed class Helper
    {
        public readonly Dictionary<string, CharacterCard> Cards = new Dictionary<string, CharacterCard>();
        readonly Dictionary<string, ConversationEngine> _engines = new Dictionary<string, ConversationEngine>();
        readonly ILlmClient _llm;
        readonly CostTracker _cost = new CostTracker();
        public CostTracker Cost => _cost;
        readonly TimeSpan _patience;

        public Helper(ILlmClient llm, TimeSpan patience) { _llm = llm; _patience = patience; }

        public bool Online => _llm != null;

        public ConversationEngine EngineFor(string to) => _engines.TryGetValue(to, out var e) ? e : null;

        public async Task<string> Answer(string line)
        {
            int id = 0;
            string to = "", say = "", scene = "";
            int hour = 12, day = 1, minute = 0;
            var memories = new List<MemoryEvent>();
            var knows = new List<Fact>();
            double? suspicion = null;
            string suspicionWhy = null;
            string who = null;
            bool noReply = false;
            (double value, SuspicionLevel level, string why)? derived = null;
            try
            {
                using var doc = JsonDocument.Parse(line);
                var r = doc.RootElement;
                if (r.TryGetProperty("id", out var v)) id = v.GetInt32();
                if (r.TryGetProperty("to", out v)) to = v.GetString() ?? "";
                if (r.TryGetProperty("say", out v)) say = v.GetString() ?? "";
                if (r.TryGetProperty("hour", out v)) hour = v.GetInt32();
                if (r.TryGetProperty("day", out v)) day = v.GetInt32();
                if (r.TryGetProperty("minute", out v)) minute = v.GetInt32();
                if (r.TryGetProperty("scene", out v)) scene = v.GetString() ?? "";
                if (r.TryGetProperty("memories", out v) && v.ValueKind == JsonValueKind.Array)
                    foreach (var m in v.EnumerateArray())
                    {
                        string text = m.TryGetProperty("text", out var t) ? t.GetString() ?? "" : "";
                        if (text.Length == 0) continue;
                        memories.Add(new MemoryEvent(
                            new GameTime(m.TryGetProperty("day", out var md) ? md.GetInt32() : day,
                                         m.TryGetProperty("hour", out var mh) ? mh.GetInt32() : hour,
                                         m.TryGetProperty("minute", out var mm) ? mm.GetInt32() : 0),
                            m.TryGetProperty("kind", out var mk) ? mk.GetString() ?? "observation" : "observation",
                            m.TryGetProperty("importance", out var mi) ? mi.GetDouble() : 0.5,
                            text));
                    }
                if (r.TryGetProperty("knows", out v) && v.ValueKind == JsonValueKind.Array)
                    foreach (var k in v.EnumerateArray())
                        knows.Add(new Fact(k.TryGetProperty("subject", out var ks) ? ks.GetString() ?? "" : "",
                                           k.TryGetProperty("predicate", out var kp) ? kp.GetString() ?? "" : "",
                                           k.TryGetProperty("value", out var kv) ? kv.GetString() ?? "" : ""));
                if (r.TryGetProperty("suspicion", out v) && v.ValueKind == JsonValueKind.Number) suspicion = v.GetDouble();
                if (r.TryGetProperty("suspicionWhy", out v)) suspicionWhy = v.GetString();
                if (r.TryGetProperty("who", out v)) who = v.GetString();
                if (r.TryGetProperty("noReply", out v) && v.ValueKind == JsonValueKind.True) noReply = true;
                if (r.TryGetProperty("evidence", out v) && v.ValueKind == JsonValueKind.Object)
                {
                    var acc = new DeedAccount();
                    var near = new Nearness();
                    double fam = 0.0;
                    if (v.TryGetProperty("account", out var a) && a.ValueKind == JsonValueKind.Object)
                    {
                        acc.Held = Bool(a, "held"); acc.SawItMyself = Bool(a, "seen"); acc.NamesHim = Bool(a, "names");
                        acc.Rung = a.TryGetProperty("rung", out var rg) && rg.ValueKind == JsonValueKind.Number ? rg.GetInt32() : -1;
                        acc.Confidence = a.TryGetProperty("confidence", out var c) && c.ValueKind == JsonValueKind.Number ? c.GetDouble() : 0.0;
                        acc.Summary = a.TryGetProperty("summary", out var sm) ? sm.GetString() : null;
                    }
                    if (v.TryGetProperty("near", out var n) && n.ValueKind == JsonValueKind.Object)
                    {
                        near.SawHimMyself = Bool(n, "sawHim"); near.HeardHeWasNear = Bool(n, "heard");
                        near.OthersNear = n.TryGetProperty("others", out var o) && o.ValueKind == JsonValueKind.Number ? o.GetInt32() : 0;
                        near.Summary = n.TryGetProperty("summary", out var ns) ? ns.GetString() : null;
                    }
                    if (v.TryGetProperty("familiarity", out var fv) && fv.ValueKind == JsonValueKind.Number) fam = fv.GetDouble();
                    derived = Suspecting.Derive(acc, near, fam);
                }
            }
            catch (Exception)
            {
                return JsonSerializer.Serialize(new { error = "bad-line" }, Plain);
            }
            if (noReply && !derived.HasValue)
                return JsonSerializer.Serialize(new { id, to, error = "no-evidence" }, Plain);
            if (derived.HasValue && noReply)
            {
                var dv = derived.Value;
                return JsonSerializer.Serialize(new { id, to, who, suspicion = Math.Round(dv.value, 3), level = dv.level.ToString(), why = dv.why }, Plain);
            }
            if (!Cards.TryGetValue(to, out var card))
                return JsonSerializer.Serialize(new { id, to, error = "no-card" }, Plain);
            string key = string.IsNullOrEmpty(who) ? to : who;

            var sw = Stopwatch.StartNew();
            string brush = BrushOffs[Math.Abs(id) % BrushOffs.Length];
            var now = new GameTime(day, hour, minute);

            if (!_engines.TryGetValue(key, out var engine))
            {
                engine = new ConversationEngine(_llm, card, new MemoryStore(card.Id), new KnowledgeBase(),
                    new SuspicionTracker(), _cost);
                // THE CLAIM CHECK ON THE REAL MODEL (ClaimCheck.cs, 24 September):
                // every reply is read for claims the character's knowledge does
                // not support before it is said. Not on the stand-in models,
                // which answer only from memory already.
                if (_llm is AnthropicClient) engine.Checker = _llm;
                _engines[key] = engine;
            }
            // THE SIMULATION'S STATE, loaded before the line is answered.
            foreach (var m in memories)
            {
                bool held = false;
                foreach (var e in engine.Memory.Events)
                    if (e.Time.Equals(m.Time) && e.Text == m.Text) { held = true; break; }
                if (!held) engine.Memory.Append(m);
            }
            foreach (var f in knows) engine.Knowledge.Learn(f);
            if (derived.HasValue)
            {
                suspicion = derived.Value.value;
                suspicionWhy = derived.Value.why;
            }
            if (suspicion.HasValue)
            {
                // THE REASON CARRIES THE MOVE, so it reads as the reason the
                // level is where it is (LatestReason takes only raising ones).
                if (string.IsNullOrEmpty(suspicionWhy)) engine.Suspicion.Restore(suspicion.Value);
                else { engine.Suspicion.Restore(0.0); engine.Suspicion.Raise(suspicion.Value, suspicionWhy); }
            }
            string level = engine.Suspicion.Level.ToString();
            double holds = Math.Round(engine.Suspicion.Value, 3);
            var heard = new List<string>();
            foreach (var m in MemoryRetrieval.Retrieve(engine.Memory, say, now)) heard.Add(m.Text);

            if (_llm == null)
                return JsonSerializer.Serialize(new { id, to, day, reply = brush, ms = 0L, offline = true, timedOut = false, heard, suspicion = holds, level, why = suspicionWhy }, Plain);
            string reply;
            bool timedOut = false;
            using (var cts = new CancellationTokenSource(_patience))
            {
                try
                {
                    var task = engine.SayToAsync(say, now, scene, cts.Token);
                    var done = await Task.WhenAny(task, Task.Delay(_patience));
                    if (done != task)
                    {
                        timedOut = true;
                        reply = brush;
                        // CANCEL WHAT IS ABANDONED (the independent check, 25
                        // September): the source was disposed without being
                        // cancelled whenever the delay won the race, so the
                        // reply ran on and the character remembered saying a
                        // line nobody heard (45 of 60 timeouts). Cancelled, the
                        // engine rolls the turn back; if it finished in the
                        // same instant it is remembered, so it is said.
                        cts.Cancel();
                        await Task.WhenAny(task, Task.Delay(1000));
                        if (task.Status == TaskStatus.RanToCompletion)
                        {
                            timedOut = false;
                            reply = ResponseValidator.Validate(task.Result, card.Name, card.AlsoCalled);
                        }
                    }
                    else
                    {
                        reply = ResponseValidator.Validate(await task, card.Name, card.AlsoCalled);
                    }
                }
                catch (Exception)
                {
                    timedOut = true;
                    reply = brush;
                }
            }
            // INVENTED: what the first draft claimed that nothing supports, kept
            // for the log (the line said is the second draft or the plain one).
            // UNCHECKED: the claim check failed or answered out of shape, so the
            // line was said as written; apart from a clean check in the log.
            var invented = timedOut ? new List<string>() : new List<string>(engine.LastInvented);
            bool @unchecked = !timedOut && engine.Checker != null && engine.LastUnchecked;
            return JsonSerializer.Serialize(new { id, to, day, reply, ms = sw.ElapsedMilliseconds, offline = false, timedOut, heard, suspicion = holds, level, why = suspicionWhy, invented, @unchecked }, Plain);
        }

        static bool Bool(JsonElement e, string name) =>
            e.TryGetProperty(name, out var v) && v.ValueKind == JsonValueKind.True;
    }

    /// THE STAND-IN MODEL FOR THE ENCOUNTER'S REGRESSION: it answers from the
    /// memories its prompt was given and nothing else, so what the simulation
    /// knew is visible in the reply without a key or a bill.
    sealed class KnowledgeFake : ILlmClient
    {
        public Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            string first = null;
            var sys = request.System ?? "";
            int at = sys.IndexOf("Relevant memories", StringComparison.Ordinal);
            if (at >= 0)
                foreach (var raw in sys.Substring(at).Split('\n'))
                {
                    var l = raw.Trim();
                    if (!l.StartsWith("- [")) continue;
                    int close = l.IndexOf(']');
                    first = close > 0 ? l.Substring(close + 1).Trim() : l;
                    break;
                }
            // IT QUESTIONS ONLY WHEN THE CORE GAVE IT A REASON, 24 September:
            // the level in the prompt decides, as it does for the real model.
            // And when it asks, it asks about the reason it was given, as the
            // real model is told to: the why line, not whichever memory
            // retrieval happened to rank first.
            bool suspects = sys.Contains("actively suspicious") || sys.Contains("caught this person");
            const string WhyKey = "Why you feel that way, in your own words: ";
            int wi = sys.IndexOf(WhyKey, StringComparison.Ordinal);
            string why = null;
            if (wi >= 0)
            {
                int end = sys.IndexOf('\n', wi);
                why = (end < 0 ? sys.Substring(wi + WhyKey.Length) : sys.Substring(wi + WhyKey.Length, end - wi - WhyKey.Length)).Trim();
            }
            string text = first == null && why == null ? "Morning. Quiet one today."
                : suspects ? "I know what happened. " + (why ?? first) + " Was that you?"
                : "Funny business round here. " + first;
            return Task.FromResult(new LlmResponse { Text = text, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model });
        }
    }

    static string CardsDir(string[] args)
    {
        for (int i = 0; i + 1 < args.Length; i++) if (args[i] == "--cards") return args[i + 1];
        var d = new DirectoryInfo(AppContext.BaseDirectory);
        while (d != null)
        {
            var c = Path.Combine(d.FullName, "production", "cast", "cards");
            if (Directory.Exists(c)) return c;
            d = d.Parent;
        }
        return Path.Combine("production", "cast", "cards");
    }

    static void LoadCards(Helper h, string dir)
    {
        if (!Directory.Exists(dir)) return;
        foreach (var f in Directory.GetFiles(dir, "*.md"))
        {
            var card = CharacterCard.Parse(File.ReadAllText(f));
            var key = Path.GetFileNameWithoutExtension(f).ToLowerInvariant();
            if (card != null) h.Cards[key] = card;
        }
    }

    static async Task<int> Main(string[] args)
    {
        if (Array.IndexOf(args, "--selftest") >= 0) return await SelfTest(CardsDir(args));
        var key = Environment.GetEnvironmentVariable("ANTHROPIC_API_KEY");
        bool fake = Array.IndexOf(args, "--fake") >= 0 || Environment.GetEnvironmentVariable("LEDGER_TALK_FAKE") == "1";
        ILlmClient llm = fake ? new KnowledgeFake() : (string.IsNullOrEmpty(key) ? null : new AnthropicClient(key));
        var helper = new Helper(llm, TimeSpan.FromSeconds(8));
        LoadCards(helper, CardsDir(args));
        Console.Out.WriteLine(JsonSerializer.Serialize(new { ready = true, cards = helper.Cards.Keys, online = helper.Online, fake }, Plain));
        Console.Out.Flush();
        string line;
        while ((line = Console.In.ReadLine()) != null)
        {
            if (line.Trim().Length == 0) continue;
            Console.Out.WriteLine(await helper.Answer(line));
            Console.Out.Flush();
        }
        // WHAT THE SESSION COST, when the game closes the helper's input: the
        // calls, the tokens by model and the dollars at the game's own price
        // table - the measure Jafar asked for of an hour of play (23 September).
        Console.Out.WriteLine(JsonSerializer.Serialize(new
        {
            cost = helper.Cost.Report(),
            usd = helper.Cost.EstimateUsd(),
            calls = helper.Cost.TotalCalls,
        }, Plain));
        return 0;
    }

    // ---------------------------------------------------------------- the selftest, no network

    sealed class FakeLlm : ILlmClient
    {
        public string Next = "Hm. Is that so.";
        public TimeSpan Delay = TimeSpan.Zero;
        public int Calls;
        public async Task<LlmResponse> CompleteAsync(LlmRequest request, CancellationToken ct = default)
        {
            Calls++;
            if (Delay > TimeSpan.Zero) await Task.Delay(Delay, ct);
            return new LlmResponse { Text = Next, StopReason = "end_turn", InputTokens = 400, OutputTokens = 20, Model = request.Model };
        }
    }

    static async Task<int> SelfTest(string cardsDir)
    {
        int passed = 0, failed = 0;
        void Ok(string name, bool cond, string detail = "")
        {
            if (cond) passed++; else { failed++; Console.WriteLine($"talkhelper selftest FAIL {name} {detail}"); }
        }
        string Reply(string json) { using var d = JsonDocument.Parse(json); return d.RootElement.TryGetProperty("reply", out var v) ? v.GetString() : null; }
        List<string> Heard(string json)
        {
            var o = new List<string>();
            using var d = JsonDocument.Parse(json);
            if (d.RootElement.TryGetProperty("heard", out var v) && v.ValueKind == JsonValueKind.Array)
                foreach (var e in v.EnumerateArray()) o.Add(e.GetString());
            return o;
        }
        bool Flag(string json, string f) { using var d = JsonDocument.Parse(json); return d.RootElement.TryGetProperty(f, out var v) && v.GetBoolean(); }

        var fake = new FakeLlm();
        var h = new Helper(fake, TimeSpan.FromSeconds(8));
        LoadCards(h, cardsDir);
        Ok("the slice's three talkers have cards", h.Cards.ContainsKey("rocco") && h.Cards.ContainsKey("lena") && h.Cards.ContainsKey("sam"),
           string.Join(",", h.Cards.Keys));

        var a = await h.Answer("{\"id\":1,\"to\":\"sam\",\"say\":\"Morning.\",\"hour\":12,\"scene\":\"the fish market's pavement\"}");
        Ok("a line goes to the real engine and its reply comes back", Reply(a) == "Hm. Is that so." && fake.Calls == 1 && !Flag(a, "offline"), a);

        fake.Next = "Fancy a pint down the Anchor after?";
        var b = await h.Answer("{\"id\":2,\"to\":\"sam\",\"say\":\"Busy tonight?\"}");
        Ok("a reply the content rule refuses is deflected, never passed on", Reply(b) != null && !Reply(b).Contains("pint"), b);

        var c = await h.Answer("{\"id\":3,\"to\":\"nobody\",\"say\":\"Hello?\"}");
        Ok("a line to someone with no card says so", c.Contains("no-card"), c);

        var d = await h.Answer("not json");
        Ok("a broken line is refused, not guessed at", d.Contains("bad-line"), d);

        var off = new Helper(null, TimeSpan.FromSeconds(8));
        LoadCards(off, cardsDir);
        var e = await off.Answer("{\"id\":4,\"to\":\"lena\",\"say\":\"Got a minute?\"}");
        Ok("with the line down the character brushes the player off and says offline",
           Flag(e, "offline") && Array.IndexOf(BrushOffs, Reply(e)) >= 0, e);

        var slow = new FakeLlm { Delay = TimeSpan.FromSeconds(2) };
        var s = new Helper(slow, TimeSpan.FromMilliseconds(300));
        LoadCards(s, cardsDir);
        var sw = Stopwatch.StartNew();
        var f = await s.Answer("{\"id\":5,\"to\":\"rocco\",\"say\":\"Alright?\"}");
        Ok("a slow model is abandoned for a brush-off at the patience limit",
           Flag(f, "timedOut") && Array.IndexOf(BrushOffs, Reply(f)) >= 0 && sw.ElapsedMilliseconds < 1800, f);
        await Task.Delay(2500);   // past the moment the abandoned reply would have landed
        int unheard = 0;
        foreach (var ev in s.EngineFor("rocco").Memory.Events) if (ev.Kind == "conversation") unheard++;
        Ok("an abandoned reply is cancelled, never remembered as said", unheard == 0, unheard.ToString());

        // THE SIMULATION'S STATE REACHES THE ANSWER, 24 September.
        var k = new Helper(new KnowledgeFake(), TimeSpan.FromSeconds(8));
        LoadCards(k, cardsDir);
        var g = await k.Answer("{\"id\":6,\"to\":\"sam\",\"say\":\"Morning.\",\"day\":3,\"hour\":16}");
        Ok("with nothing known, nothing is claimed", Reply(g) != null && !Reply(g).Contains("window"), g);
        var w = await k.Answer("{\"id\":7,\"to\":\"sam\",\"say\":\"What's the news?\",\"day\":3,\"hour\":17,\"memories\":[{\"day\":3,\"hour\":15,\"kind\":\"heard\",\"importance\":0.9,\"text\":\"Heard from Rita that the new owner put her window in.\"}]," +
            "\"suspicion\":0.6,\"suspicionWhy\":\"heard he put Rita's window in\"}");
        Ok("a memory sent by the game is in the answer", Reply(w) != null && Reply(w).Contains("window"), w);
        Ok("and in what the helper says it heard", Heard(w).Contains("Heard from Rita that the new owner put her window in."), w);
        Ok("the day is the game's, not day 1", w.Contains("\"day\":3"), w);
        await k.Answer("{\"id\":8,\"to\":\"sam\",\"say\":\"Anything else?\",\"day\":3,\"hour\":18,\"memories\":[{\"day\":3,\"hour\":15,\"kind\":\"heard\",\"importance\":0.9,\"text\":\"Heard from Rita that the new owner put her window in.\"}]}");
        int copies = 0;
        foreach (var ev in k.EngineFor("sam").Memory.Events) if (ev.Kind == "heard" && ev.Text == "Heard from Rita that the new owner put her window in.") copies++;
        Ok("a memory sent twice is held once", copies == 1, copies.ToString());

        // THE CORE DECIDES WHO HAS REASON TO ASK, 24 September.
        string Str(string json, string f) { using var dd = JsonDocument.Parse(json); return dd.RootElement.TryGetProperty(f, out var vv) && vv.ValueKind == JsonValueKind.String ? vv.GetString() : null; }
        var q = new Helper(new KnowledgeFake(), TimeSpan.FromSeconds(8));
        LoadCards(q, cardsDir);
        const string Mem = "\"memories\":[{\"day\":1,\"hour\":12,\"kind\":\"heard\",\"importance\":0.36,\"text\":\"I heard from the shopkeeper that the man that did the window ran\"}]";
        const string Acc = "\"account\":{\"held\":true,\"seen\":false,\"names\":false,\"confidence\":0.45,\"summary\":\"the man that did the window ran\"}";
        var lad = await q.Answer("{\"id\":9,\"to\":\"sam\",\"who\":\"n2\",\"say\":\"Evening.\",\"day\":4,\"hour\":18," + Mem +
            ",\"evidence\":{" + Acc + ",\"near\":{\"sawHim\":true,\"others\":0,\"summary\":\"a man came through the yard at a run\"},\"familiarity\":0.2}}");
        Ok("heard about it and saw him near it alone: suspicious, and he asks", Str(lad, "level") == "Suspicious" && Reply(lad).Contains("?"), lad);
        Ok("and the reason travels with it", Str(lad, "why") != null && Str(lad, "why").Contains("came through the yard"), lad);
        var mate = await q.Answer("{\"id\":10,\"to\":\"sam\",\"who\":\"r3\",\"say\":\"Evening.\",\"day\":4,\"hour\":18," + Mem +
            ",\"evidence\":{" + Acc + ",\"familiarity\":0.2}}");
        Ok("heard about it with nothing tying him: trusting, and he does not ask", Str(mate, "level") == "Trusting" && !Reply(mate).Contains("?"), mate);
        Ok("two people on one card keep their own state", q.EngineFor("n2") != null && q.EngineFor("r3") != null && q.EngineFor("n2") != q.EngineFor("r3"));
        var costBefore = q.Cost.TotalCalls;
        var only = await q.Answer("{\"id\":11,\"to\":\"sam\",\"who\":\"r3\",\"noReply\":true,\"evidence\":{" + Acc + ",\"near\":{\"heard\":true},\"familiarity\":0.2}}");
        Ok("the level alone, with no model call", Str(only, "level") == "Uneasy" && Str(only, "reply") == null && q.Cost.TotalCalls == costBefore, only);

        Console.WriteLine($"talkhelper selftest: passed={passed}/{passed + failed} failed={failed}");
        return failed == 0 ? 0 : 1;
    }
}
