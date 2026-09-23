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
        readonly TimeSpan _patience;

        public Helper(ILlmClient llm, TimeSpan patience) { _llm = llm; _patience = patience; }

        public bool Online => _llm != null;

        public async Task<string> Answer(string line)
        {
            int id = 0;
            string to = "", say = "", scene = "";
            int hour = 12;
            try
            {
                using var doc = JsonDocument.Parse(line);
                var r = doc.RootElement;
                if (r.TryGetProperty("id", out var v)) id = v.GetInt32();
                if (r.TryGetProperty("to", out v)) to = v.GetString() ?? "";
                if (r.TryGetProperty("say", out v)) say = v.GetString() ?? "";
                if (r.TryGetProperty("hour", out v)) hour = v.GetInt32();
                if (r.TryGetProperty("scene", out v)) scene = v.GetString() ?? "";
            }
            catch (Exception)
            {
                return JsonSerializer.Serialize(new { error = "bad-line" }, Plain);
            }
            if (!Cards.TryGetValue(to, out var card))
                return JsonSerializer.Serialize(new { id, to, error = "no-card" }, Plain);

            var sw = Stopwatch.StartNew();
            string brush = BrushOffs[Math.Abs(id) % BrushOffs.Length];
            if (_llm == null)
                return JsonSerializer.Serialize(new { id, to, reply = brush, ms = 0L, offline = true, timedOut = false }, Plain);

            if (!_engines.TryGetValue(to, out var engine))
            {
                engine = new ConversationEngine(_llm, card, new MemoryStore(card.Id), new KnowledgeBase(),
                    new SuspicionTracker(), _cost);
                _engines[to] = engine;
            }
            string reply;
            bool timedOut = false;
            using (var cts = new CancellationTokenSource(_patience))
            {
                try
                {
                    var task = engine.SayToAsync(say, new GameTime { Day = 1, Hour = hour }, scene, cts.Token);
                    var done = await Task.WhenAny(task, Task.Delay(_patience));
                    if (done != task)
                    {
                        timedOut = true;
                        reply = brush;
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
            return JsonSerializer.Serialize(new { id, to, reply, ms = sw.ElapsedMilliseconds, offline = false, timedOut }, Plain);
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
        var helper = new Helper(string.IsNullOrEmpty(key) ? null : new AnthropicClient(key), TimeSpan.FromSeconds(8));
        LoadCards(helper, CardsDir(args));
        Console.Out.WriteLine(JsonSerializer.Serialize(new { ready = true, cards = helper.Cards.Keys, online = helper.Online }, Plain));
        Console.Out.Flush();
        string line;
        while ((line = Console.In.ReadLine()) != null)
        {
            if (line.Trim().Length == 0) continue;
            Console.Out.WriteLine(await helper.Answer(line));
            Console.Out.Flush();
        }
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

        var slow = new FakeLlm { Delay = TimeSpan.FromSeconds(5) };
        var s = new Helper(slow, TimeSpan.FromMilliseconds(300));
        LoadCards(s, cardsDir);
        var sw = Stopwatch.StartNew();
        var f = await s.Answer("{\"id\":5,\"to\":\"rocco\",\"say\":\"Alright?\"}");
        Ok("a slow model is abandoned for a brush-off at the patience limit",
           Flag(f, "timedOut") && Array.IndexOf(BrushOffs, Reply(f)) >= 0 && sw.ElapsedMilliseconds < 3000, f);

        Console.WriteLine($"talkhelper selftest: passed={passed}/{passed + failed} failed={failed}");
        return failed == 0 ? 0 : 1;
    }
}
